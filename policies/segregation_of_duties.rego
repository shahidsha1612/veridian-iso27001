# Control: 5.3 (Segregation of duties).
#
# Nobody who can apply infrastructure changes should also be able to
# approve them on their own, and nobody holding standing "plan"
# credentials (the role every pull request runs under, before human
# review) should ever be able to mutate anything. This validates a JSON
# snapshot of the IAM role definitions in
# terraform/iam-segregation-of-duties/ against those invariants.
#
# input shape:
# {
#   "iam_roles": [
#     {
#       "name": "gha-terraform-plan",
#       "assume_condition": {"ref": "*"},
#       "actions": ["ec2:Describe*", ...]   # every action this role's policy grants
#     },
#     ...
#   ]
# }
package segregation_of_duties

write_action_prefixes := {"Create", "Put", "Delete", "Update", "Attach", "Detach", "Modify", "Terminate", "Apply", "Write"}

is_write_action(action) if {
	parts := split(action, ":")
	verb := parts[1]
	some prefix in write_action_prefixes
	startswith(verb, prefix)
}

self_escalation_actions := {"iam:PutRolePolicy", "iam:AttachRolePolicy", "iam:CreatePolicyVersion", "iam:UpdateAssumeRolePolicy"}

# Deny: any role assumable outside master (i.e. on pull_request runs,
# before human review/merge) that also grants a write action.
deny contains msg if {
	some role in input.iam_roles
	role.assume_condition.ref != "refs/heads/master"
	some action in role.actions
	is_write_action(action)
	msg := sprintf("role %q is assumable outside master (ref=%q) but grants write action %q; plan/PR-time roles must be read-only", [role.name, role.assume_condition.ref, action])
}

# Deny: any master-only (apply) role that can also modify IAM roles or
# policies, i.e. escalate or rewrite its own permissions after the fact.
deny contains msg if {
	some role in input.iam_roles
	role.assume_condition.ref == "refs/heads/master"
	some action in role.actions
	action in self_escalation_actions
	msg := sprintf("apply role %q grants %q, letting it modify its own permissions; this defeats segregation of duties", [role.name, action])
}

# Deny: fewer than two distinct roles present at all. Segregation
# requires at least a separate plan role and apply role; a single role
# doing both collapses the whole point of this control.
deny contains msg if {
	names := {role.name | some role in input.iam_roles}
	count(names) < 2
	msg := "fewer than two distinct IAM roles defined; a single role cannot both plan and apply without collapsing segregation of duties"
}
