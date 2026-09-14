# Control: 5.3 (Segregation of duties).
#
# Two IAM roles, assumable only via GitHub Actions OIDC (no static
# long-lived AWS keys anywhere, control 5.17), scoped so that no single
# actor -- human or role -- can both plan/approve *and* apply a
# Terraform change:
#
#   - gha-terraform-plan: assumable on ANY ref (every PR run). Read-only.
#     Runs `terraform plan` so a reviewer can see the diff before merge.
#   - gha-terraform-apply: assumable ONLY when the OIDC token's `sub`
#     claim matches a push to refs/heads/master -- i.e. only after a PR
#     has already been reviewed and merged, per
#     .github/workflows/segregation-of-duties.yml. No human ever holds
#     apply credentials directly; only the CI pipeline does, and only
#     post-merge.
#
# The Rego policy in policies/segregation_of_duties.rego encodes and
# tests these same invariants (no write actions on the plan role, no
# self-escalation actions on the apply role, at least two distinct
# roles) against a JSON snapshot of these role definitions; see
# scripts/evidence/check_segregation_of_duties.py, which builds that
# snapshot and re-runs the policy on a schedule.

data "aws_iam_openid_connect_provider" "github_actions" {
  count = var.create_oidc_provider ? 0 : 1
  url   = "https://token.actions.githubusercontent.com"
}

resource "aws_iam_openid_connect_provider" "github_actions" {
  count           = var.create_oidc_provider ? 1 : 0
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]

  tags = {
    "iso27001:control" = "5.3 5.17"
  }
}

locals {
  oidc_provider_arn = var.create_oidc_provider ? aws_iam_openid_connect_provider.github_actions[0].arn : data.aws_iam_openid_connect_provider.github_actions[0].arn
  repo_subject_base = "repo:${var.github_org}/${var.github_repo}"
}

# --- Plan role: every PR run, read-only, any ref ---------------------

data "aws_iam_policy_document" "plan_trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [local.oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    # Any ref: this role runs on every pull_request, before review.
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["${local.repo_subject_base}:*"]
    }
  }
}

resource "aws_iam_role" "plan" {
  name               = "gha-terraform-plan"
  assume_role_policy = data.aws_iam_policy_document.plan_trust.json

  tags = {
    "iso27001:control" = "5.3"
  }
}

# Read-only. AWS's managed ReadOnlyAccess is intentionally broad but
# contains zero write/mutate actions, which is exactly what the Rego
# policy checks for; a narrower custom policy is a fine future
# tightening, not required for the segregation invariant itself.
resource "aws_iam_role_policy_attachment" "plan_read_only" {
  role       = aws_iam_role.plan.name
  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}

# --- Apply role: only on push to master, i.e. only post-merge --------

data "aws_iam_policy_document" "apply_trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [local.oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    # Only a push to master -- never a pull_request-triggered run.
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["${local.repo_subject_base}:ref:refs/heads/master"]
    }
  }
}

resource "aws_iam_role" "apply" {
  name               = "gha-terraform-apply"
  assume_role_policy = data.aws_iam_policy_document.apply_trust.json

  tags = {
    "iso27001:control" = "5.3"
  }
}

# Deliberately excludes iam:PutRolePolicy / AttachRolePolicy /
# CreatePolicyVersion / UpdateAssumeRolePolicy on either role: the apply
# role can build infrastructure but can never rewrite its own or the
# plan role's permissions, closing the privilege-escalation path the
# Rego policy's self_escalation_actions check exists to catch.
data "aws_iam_policy_document" "apply_permissions" {
  statement {
    sid    = "InfrastructureWrite"
    effect = "Allow"
    actions = [
      "ec2:*", "s3:*", "kms:CreateKey", "kms:CreateAlias", "kms:TagResource",
      "budgets:*", "cloudtrail:*", "guardduty:*", "config:*",
    ]
    resources = ["*"]
  }

  statement {
    sid    = "DenySelfEscalation"
    effect = "Deny"
    actions = [
      "iam:PutRolePolicy",
      "iam:AttachRolePolicy",
      "iam:CreatePolicyVersion",
      "iam:UpdateAssumeRolePolicy",
      "iam:DeleteRolePolicy",
      "iam:DetachRolePolicy",
    ]
    resources = [
      aws_iam_role.apply.arn,
      aws_iam_role.plan.arn,
    ]
  }
}

resource "aws_iam_role_policy" "apply_permissions" {
  name   = "terraform-apply-permissions"
  role   = aws_iam_role.apply.id
  policy = data.aws_iam_policy_document.apply_permissions.json
}
