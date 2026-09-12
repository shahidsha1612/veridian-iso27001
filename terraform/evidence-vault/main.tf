# Control: 5.28 (Collection of evidence), 5.33 (Protection of records)
#
# This is the vault every T1/T2 control's evidence manifest is written
# into: SHA-256 hash + Cosign signature land here as a pair of objects,
# never edited, never deleted before retention expires. See
# ../../docs/CONTINUOUS_EVIDENCE_ARCHITECTURE.md for the full design.

resource "aws_kms_key" "evidence" {
  description             = "CMK for the ISO 27001 evidence vault (control 8.24: customer-managed keys only, no AWS-owned/default keys)."
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    "iso27001:control" = "5.28 5.33 8.24"
  }
}

resource "aws_kms_alias" "evidence" {
  name          = "alias/iso27001-evidence-vault"
  target_key_id = aws_kms_key.evidence.key_id
}

resource "aws_s3_bucket" "evidence" {
  bucket = var.bucket_name

  # Object Lock can only be set at creation time; this is why it's not a
  # separate "enable later" step.
  object_lock_enabled = true

  tags = {
    "iso27001:control" = "5.28 5.33"
  }
}

resource "aws_s3_bucket_versioning" "evidence" {
  bucket = aws_s3_bucket.evidence.id
  versioning_configuration {
    status = "Enabled" # required for Object Lock
  }
}

resource "aws_s3_bucket_object_lock_configuration" "evidence" {
  bucket = aws_s3_bucket.evidence.id

  rule {
    default_retention {
      mode = "GOVERNANCE" # tamper-evident against ordinary callers; a break-glass role can still manage lifecycle (architecture principle 4)
      days = var.object_lock_retention_days
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "evidence" {
  bucket = aws_s3_bucket.evidence.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.evidence.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "evidence" {
  bucket = aws_s3_bucket.evidence.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "aws_iam_policy_document" "evidence_bucket_policy" {
  # Deny any non-TLS access (control 5.14).
  statement {
    sid       = "DenyInsecureTransport"
    effect    = "Deny"
    actions   = ["s3:*"]
    resources = [aws_s3_bucket.evidence.arn, "${aws_s3_bucket.evidence.arn}/*"]

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }

  # Deny writes that don't use this bucket's CMK (control 8.24).
  statement {
    sid       = "DenyPutWithoutVaultKMSKey"
    effect    = "Deny"
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.evidence.arn}/*"]

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    condition {
      test     = "StringNotEquals"
      variable = "s3:x-amz-server-side-encryption-aws-kms-key-id"
      values   = [aws_kms_key.evidence.arn]
    }
  }

  # Write-only for the workload account's evidence-writer role: PutObject
  # allowed, DeleteObject deliberately not granted (architecture principle
  # 5). Empty principal list is intentionally invalid until a real
  # workload account/role exists; this statement is inert (no principal)
  # rather than silently permissive.
  dynamic "statement" {
    for_each = var.workload_account_writer_role_arn != "" ? [1] : []
    content {
      sid       = "WorkloadAccountWriteOnly"
      effect    = "Allow"
      actions   = ["s3:PutObject"]
      resources = ["${aws_s3_bucket.evidence.arn}/*"]

      principals {
        type        = "AWS"
        identifiers = [var.workload_account_writer_role_arn]
      }
    }
  }
}

resource "aws_s3_bucket_policy" "evidence" {
  bucket = aws_s3_bucket.evidence.id
  policy = data.aws_iam_policy_document.evidence_bucket_policy.json
}
