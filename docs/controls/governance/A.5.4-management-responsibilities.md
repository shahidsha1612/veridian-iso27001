---
control_id: "5.4"
title: "Management Responsibilities"
owner: "CEO / Management representative"
version: "1.0"
last_reviewed: "2026-09-14"
review_cadence_months: 12
next_review_due: "2027-09-14"
---

# Management Responsibilities

## Purpose

Ensures management actively requires and supports information security
across the organization, per ISO/IEC 27001:2022 control 5.4 and Clause
9.3 (Management review). The mechanism is a real, dated management
review meeting held at least annually, with minutes kept in
[`docs/management-reviews/`](../../management-reviews/), each one
carrying the same frontmatter as every other control doc so
`scripts/evidence/check_policy_freshness.py` picks them up
automatically (it scans that directory alongside `docs/controls/`).

## Who's accountable

Per the RACI matrix in
[`A.5.2-...md`](A.5.2-information-security-roles-and-responsibilities.md),
the CEO / Management representative is Accountable for Governance
(domain 1), and is the one who convenes and chairs this review.

## Known limitation, stated plainly

Same shape as the gap already documented in 5.2 and 5.3: today the CEO
/ Management representative and GRC/Security engineer are the same
person, so a "management review" is one person reviewing their own
work, not independent management oversight of a separate security
function. That's real, not papered over - see each review's minutes
for how it's handled (mainly: sticking to Clause 9.3's actual required
agenda, dated and recorded, rather than skipping the review because
there's no one else to review it with).

## What each review covers (Clause 9.3 required inputs)

Every minutes document in `docs/management-reviews/` addresses:

1. Status of actions from previous management reviews
2. Changes in external/internal issues relevant to the ISMS
3. Changes in needs/expectations of interested parties
4. Information security performance: nonconformities/corrective
   actions, monitoring/measurement results, audit results, objective
   fulfillment
5. Feedback from interested parties
6. Risk assessment results and risk treatment plan status
7. Opportunities for continual improvement

And produces: decisions on continual improvement, and any decided
changes to the ISMS.

## Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-09-14 | Initial control doc; first management review held same day, see `docs/management-reviews/2026-09-14-management-review.md` |
