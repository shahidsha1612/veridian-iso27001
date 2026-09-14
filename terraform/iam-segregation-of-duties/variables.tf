variable "aws_region" {
  description = "Region for the workload account these roles are created in."
  type        = string
  default     = "eu-west-1"
}

variable "aws_profile" {
  description = "Local AWS CLI profile for the workload account."
  type        = string
  default     = "veridian-workload"
}

variable "github_org" {
  description = "GitHub org/user that owns the repo these OIDC roles trust."
  type        = string
  default     = "shahidsha1612"
}

variable "github_repo" {
  description = "Repo name these OIDC roles trust."
  type        = string
  default     = "veridian-iso27001"
}

variable "create_oidc_provider" {
  description = <<-EOT
    Whether to create the GitHub Actions OIDC provider in this account.
    Set false if it already exists (an AWS account can only have one
    provider per URL; a second `aws_iam_openid_connect_provider` for the
    same URL fails to apply).
  EOT
  type        = bool
  default     = true
}
