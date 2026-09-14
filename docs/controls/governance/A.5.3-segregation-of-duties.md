---
control_id: "5.3"
title: "Segregation of Duties"
owner: "GRC/Security engineer"
version: "1.0"
last_reviewed: "2026-09-14"
review_cadence_months: 6
next_review_due: "2027-03-14"
---

# Segregation of Duties

## Purpose

Ensures conflicting duties and areas of responsibility are separated,
per ISO/IEC 27001:2022 control 5.3, so no single person can both
initiate and approve a change unchecked. This is the first T1 control
built in this repo: code (Terraform + Rego), a CI gate, and a signed,
scheduled evidence check, not just a document.

## The problem this control actually solves here

Veridian is, today, a genuinely solo operation: the CEO / Management
representative and the GRC/Security engineer are the same person (see
[`COMPANY.md`](../../../COMPANY.md) and the RACI matrix in
[`A.5.2-...md`](A.5.2-information-security-roles-and-responsibilities.md)).
GitHub also shows exactly one collaborator on this repo. Classic
"segregation of duties" advice (different people do different jobs)
doesn't apply when there's only one person. The honest options were:

1. Require human PR approval and lock the owner out of merging their
   own work (self-approval is impossible on GitHub) - unworkable.
2. Require human PR approval but let admins bypass it - technically
   "on," but toothless, since the one person who needs separating from
   themselves can just bypass the requirement. Evidence theater.
3. **Make the approving identity a machine, not a second human**, and
   make that machine's approval conditional on deterministic, versioned
   checks rather than a person's judgment call.

Option 3 is what's built here.

## What's built

### 1. IAM role split (Terraform, code-complete, not yet applied)

[`terraform/iam-segregation-of-duties/`](../../../terraform/iam-segregation-of-duties/)
defines two IAM roles, both assumable only via GitHub Actions OIDC (no
static long-lived AWS keys anywhere, control 5.17):

- **`gha-terraform-plan`**: assumable on *any* ref (every pull request
  run, before human review). Attached policy is read-only
  (`ReadOnlyAccess`) - it can show a reviewer what would change, but
  cannot change anything.
- **`gha-terraform-apply`**: assumable *only* when the OIDC token's
  `sub` claim is `repo:shahidsha1612/veridian-iso27001:ref:refs/heads/master` - i.e. only after a PR has already been merged. Its inline policy
  explicitly denies `iam:PutRolePolicy` / `AttachRolePolicy` /
  `CreatePolicyVersion` / `UpdateAssumeRolePolicy` on both roles, so it
  can build infrastructure but can never rewrite either role's own
  permissions (no privilege-escalation path).

**Not yet applied**: there's no AWS workload account/credentials in
this environment (same gap as the evidence-vault module before it).
The Terraform is valid (`terraform validate` passes) and this doc's
evidence check evaluates a JSON snapshot mirroring it; the moment real
credentials exist, `scripts/evidence/check_segregation_of_duties.py`
should be switched from that hand-mirrored snapshot to parsing
`terraform show -json` of the real plan/state.

### 2. Rego policy, unit-tested

[`policies/segregation_of_duties.rego`](../../../policies/segregation_of_duties.rego)
encodes three invariants over a JSON snapshot of IAM role definitions:

- no role assumable outside `refs/heads/master` (i.e. a PR-time role)
  may grant any write/mutate action,
- no `refs/heads/master`-only (apply) role may grant an action that
  modifies IAM roles/policies (self-escalation),
- at least two distinct roles must exist at all (one role can't be
  both plan and apply).

[`policies/segregation_of_duties_test.rego`](../../../policies/segregation_of_duties_test.rego)
proves the policy actually catches violations (4/4 tests: a clean
input, a plan role with a write action, an apply role that
self-escalates, and a single collapsed role - each denied as
expected), not just that it exists.

### 3. CI gate + machine approver

[`.github/workflows/segregation-of-duties.yml`](../../../.github/workflows/segregation-of-duties.yml)
runs on every PR into `master`:

- `required-checks` job: runs the T3 policy-freshness check and the
  full OPA test suite (`opa test policies/ -v`).
- `auto-approve` job: only if `required-checks` succeeds, submits an
  **approving review as `github-actions[bot]`** - a machine identity
  structurally distinct from any human author. Its approval logic is
  itself version-controlled and only changeable through this same
  gate.

Repo setting `can_approve_pull_request_reviews` was enabled (via
`gh api -X PUT repos/.../actions/permissions/workflow`) so that bot
approval counts toward a required review at all.

### 4. Branch protection on `master` (live, real, verified)

Applied via `gh api -X PUT repos/.../branches/master/protection`:

| Setting | Value |
|---|---|
| Required approving reviews | 1 |
| Enforced for admins | Yes (no bypass) |
| Required status check | `required-checks` |
| Dismiss stale reviews on new commits | Yes |
| Require last-push approval | Yes |
| Force pushes to master | Blocked |
| Branch deletion | Blocked |
| Linear history | Required |
| Conversation resolution before merge | Required |

`enforce_admins: true` is the important one: the sole admin (owner)
cannot bypass the required review, so the only path to merge is via
the bot's automated approval after checks pass.

### 5. Signed, scheduled evidence check

[`scripts/evidence/check_segregation_of_duties.py`](../../../scripts/evidence/check_segregation_of_duties.py)
checks, on demand today and on a schedule once wired into CI:

1. The OPA unit test suite still passes (policy logic hasn't
   regressed).
2. The OPA policy still passes against the IAM role snapshot (no
   segregation violation in the designed roles).
3. GitHub branch protection on `master` still requires 1+ approving
   review, still enforces it for admins, still requires the
   `required-checks` context, and still blocks force-push/deletion.

Writes one signed manifest (SHA-256 + Cosign) per run to
`evidence/controls/governance/5.3-segregation-of-duties/`, same
pattern as every other control's evidence.

## Known limitation, stated plainly

The IAM/Terraform half of this control is designed and policy-tested
but **not evaluating live infrastructure**, because no AWS workload
account exists yet in this environment. The evidence for that half
today proves the design is sound, not that it's running. The GitHub
branch-protection half has no such gap: it's live, and the evidence
check queries the real API every run.

## Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-09-14 | Initial build: Terraform IAM role split, Rego policy + tests, CI gate with bot auto-approval, live branch protection, signed evidence check |
