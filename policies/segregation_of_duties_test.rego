package segregation_of_duties_test

import data.segregation_of_duties.deny

good_input := {"iam_roles": [
	{
		"name": "gha-terraform-plan",
		"assume_condition": {"ref": "*"},
		"actions": ["ec2:DescribeInstances", "s3:GetObject", "iam:GetRole"],
	},
	{
		"name": "gha-terraform-apply",
		"assume_condition": {"ref": "refs/heads/master"},
		"actions": ["ec2:CreateTags", "s3:PutObject", "kms:CreateKey"],
	},
]}

test_good_input_has_no_denies if {
	count(deny) == 0 with input as good_input
}

bad_plan_role_has_write := {"iam_roles": [
	{
		"name": "gha-terraform-plan",
		"assume_condition": {"ref": "*"},
		"actions": ["ec2:DescribeInstances", "s3:PutObject"],
	},
	{
		"name": "gha-terraform-apply",
		"assume_condition": {"ref": "refs/heads/master"},
		"actions": ["ec2:CreateTags"],
	},
]}

test_plan_role_with_write_action_is_denied if {
	count(deny) > 0 with input as bad_plan_role_has_write
}

bad_apply_role_self_escalates := {"iam_roles": [
	{
		"name": "gha-terraform-plan",
		"assume_condition": {"ref": "*"},
		"actions": ["ec2:DescribeInstances"],
	},
	{
		"name": "gha-terraform-apply",
		"assume_condition": {"ref": "refs/heads/master"},
		"actions": ["ec2:CreateTags", "iam:PutRolePolicy"],
	},
]}

test_apply_role_self_escalation_is_denied if {
	count(deny) > 0 with input as bad_apply_role_self_escalates
}

single_role_input := {"iam_roles": [
	{
		"name": "gha-terraform-everything",
		"assume_condition": {"ref": "*"},
		"actions": ["ec2:CreateTags"],
	},
]}

test_single_role_is_denied if {
	count(deny) > 0 with input as single_role_input
}
