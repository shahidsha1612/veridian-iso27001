terraform {
  required_version = ">= 1.9.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile

  # This vault must live in a dedicated AWS account, separate from the
  # `veridian-verify` workload account, per CONTINUOUS_EVIDENCE_ARCHITECTURE.md
  # principle 5. No default here: applying this against the wrong account
  # is exactly the mistake this separation exists to prevent.
  allowed_account_ids = [var.evidence_account_id]
}
