# Cost tripwire, not a cost control: alerts the instant this account spends
# anything beyond a trivial threshold, rather than silently accumulating
# spend on a "should be near-zero" assumption.

variable "budget_alert_email" {
  description = "Email notified when this account's actual spend crosses the near-zero threshold. No default on purpose (this repo is public): set it in a local terraform.tfvars (gitignored), see terraform.tfvars.example."
  type        = string
}

resource "aws_budgets_budget" "zero_cost_alert" {
  name         = "iso27001-evidence-vault-zero-cost-alert"
  budget_type  = "COST"
  limit_amount = "1"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 1
    threshold_type             = "PERCENTAGE" # 1% of $1 = $0.01: alert on almost any real spend
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.budget_alert_email]
  }
}
