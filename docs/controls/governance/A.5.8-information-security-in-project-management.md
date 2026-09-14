---
control_id: "5.8"
title: "Information Security in Project Management"
owner: "GRC/Security engineer"
version: "1.0"
last_reviewed: "2026-09-14"
review_cadence_months: 12
next_review_due: "2027-09-14"
---

# Information Security in Project Management

## Purpose

Per ISO/IEC 27002:2022 guidance for control 5.8, "integrated into
project management" requires more than reviewing each code change at
merge time:

1. Security objectives are included in project objectives.
2. A security risk assessment happens **early** in the project.
3. Security is addressed **throughout all phases**, not just at
   delivery, with responsibilities allocated to defined roles.

A PR checkbox alone only covers the delivery moment, which is really
the territory of control 8.32 (Change management, built later). This
control covers the full lifecycle, in the tool project management
actually happens in here: GitHub.

## Mechanism (T2: human-operated control, automated evidence pull)

### Kickoff: `.github/ISSUE_TEMPLATE/project.yml`

Every new project/feature/epic uses the "New project / feature" issue
form, which requires, before the issue can even be submitted:

- **Project objective** - satisfies "security objectives included in
  project objectives" by forcing the objective to be stated at all.
- **Early risk check** - a checklist of security-relevant categories
  (RESTRICTED/CONFIDENTIAL data, new access/permissions, new external
  dependency, authentication/cryptography/key management).
- **Security considerations and planned controls** - required text; if
  the risk check flagged anything, this must describe the risk and
  which Annex A control addresses it. If nothing was flagged, "N/A" is
  the correct, instructed answer - not a rejected placeholder (see
  known-limitation note in the evidence script for why this matters).
- **Security reviewer consulted** - ties to the RACI in
  [`A.5.2-...md`](A.5.2-information-security-roles-and-responsibilities.md):
  the GRC/Security engineer should be consulted for anything flagged.

### Delivery: `.github/PULL_REQUEST_TEMPLATE.md`

Every PR requires engaging with a security-review checkbox (data
classification, access/permissions, secrets, third-party dependencies)
before merge, and links back to the originating project issue when one
exists, so kickoff-time considerations can be cross-checked against
what actually shipped.

### Evidence: `scripts/evidence/check_project_management_security_review.py`

Pulls both Issues (labeled `project`) and PRs from the real GitHub
repo via `gh`, determines each template's adoption date from git
history (so pre-existing items aren't unfairly evaluated against a
control that didn't apply to them yet), and checks:

- every project issue since adoption has non-empty security
  considerations and reviewer fields (accepting "N/A" as a legitimate,
  correctly-instructed answer, not a placeholder to reject),
- every PR since adoption engaged with the security-review checkbox.

Writes one signed manifest per run, same pattern as every other
control.

## Verified against real GitHub data, not just written

The evidence script was tested against two real issues created in this
repo: one with the security fields correctly filled in with "N/A"
(confirmed PASS), and one with the fields deliberately left as `_No
response_` after flagging CONFIDENTIAL data (confirmed FAIL) - proving
the check actually distinguishes engaged-with from skipped, not just
that it runs without error.

This verification caught a real bug before it shipped: the first
version compared `git log`'s local-timezone timestamp (`%aI`, e.g.
`13:34:46+01:00`) against GitHub API's UTC timestamps (`Z` suffix) as
raw strings. `"12:35Z" >= "13:34+01:00"` is false as a string
comparison even though the first instant is *after* the second in
real time - so every issue/PR would have been silently excluded as
"before adoption" forever. Fixed by parsing both into aware `datetime`
objects before comparing. See the evidence manifest history for
`check_project_management_security_review` (the FAIL-then-PASS
sequence around 2026-09-14T12:35-12:36Z) for the record of catching
and fixing this.

## Known limitation, stated plainly

This control governs how new projects/features get scoped from here
forward. It has no retroactive effect on work already done (5.1
through 5.6 were built before this existed) - the adoption-date
filtering in the evidence script is deliberate, not a gap: evidence
against a control can only start from when the control actually
applied.

## Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-09-14 | Initial build: issue form + PR template + evidence script, verified against real test issues |
