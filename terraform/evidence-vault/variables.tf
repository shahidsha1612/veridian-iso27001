variable "aws_region" {
  description = "Region for the evidence vault account."
  type        = string
  default     = "eu-west-1"
}

variable "aws_profile" {
  description = "Local AWS CLI profile for the evidence-vault account."
  type        = string
  default     = "veridian-evidence"
}

variable "evidence_account_id" {
  description = "AWS account ID of the dedicated evidence-vault account (037048679942, provisioned 2026-09-12)."
  type        = string
  default     = "037048679942"
}

variable "bucket_name" {
  description = "Evidence vault bucket name. Must be globally unique in S3."
  type        = string
  default     = "veridian-iso27001-evidence-vault"
}

variable "object_lock_retention_days" {
  description = "Minimum retention period (days) for every evidence object, enforced by Object Lock default retention."
  type        = number
  default     = 2555 # ~7 years, matching typical audit/records-retention expectations (5.33)
}

variable "workload_account_writer_role_arn" {
  description = <<-EOT
    ARN of the IAM role in the workload account (e.g. iso27001-tf-apply,
    or a narrower CI evidence-writer role) allowed to PutObject into this
    vault. Write-only: never granted Delete permissions, per architecture
    principle 5. No default: workload account doesn't exist yet either.
  EOT
  type        = string
  default     = ""
}
