---
control_id: "5.4"
title: "Management Review Minutes: 2026-09-14"
owner: "CEO / Management representative"
version: "1.0"
last_reviewed: "2026-09-14"
review_cadence_months: 12
next_review_due: "2027-09-14"
---

# Management Review Minutes: 2026-09-14

**Attendees:** CEO / Management representative, GRC/Security engineer
(same person today; see the known-limitation note in
[`A.5.4-...md`](../controls/governance/A.5.4-management-responsibilities.md)).
**Type:** Inaugural review - first management review since the ISMS
build began.

## 1. Status of actions from previous reviews

N/A - first review.

## 2. Changes in external/internal issues relevant to the ISMS

- **Internal**: the evidence-vault AWS account's bootstrap credential
  (`tf-bootstrap-evidence`) was found dead (`InvalidClientTokenId`)
  during this build cycle. Migrated the vault to a new account
  (`699575760023`, IAM user `terraform-lab`) rather than leaving
  evidence collection blocked. See
  `terraform/evidence-vault/variables.tf` version history.
- **External**: none identified this cycle.

## 3. Changes in needs/expectations of interested parties

None new. Standing driver remains unchanged: enterprise/bank/fintech
customers require ISO 27001 pre-contract (see `COMPANY.md`).

## 4. Information security performance

- **Build progress**: 3 of 93 Annex A controls implemented (5.1
  Policies, 5.2 Roles/RACI, 5.3 Segregation of duties), all in the
  Governance section, per `docs/IMPLEMENTATION_CHECKLIST.md`.
- **Nonconformities / corrective actions**: none logged yet - no
  formal internal audit has been performed against the ISMS (5.35 not
  yet built).
- **Monitoring / measurement results**: the evidence pipeline is
  operating - `check_policy_freshness.py` and
  `check_segregation_of_duties.py` both report PASS as of this review,
  with signed manifests in `evidence/controls/governance/` and
  mirrored into the live evidence vault.
- **Audit results**: none - no internal or external audit has occurred
  (control 5.35, not yet built; Governance section isn't finished).
- **Objective fulfillment**: on track against the stated build order
  (one checklist section at a time), no schedule commitment missed
  since none has been set yet.

## 5. Feedback from interested parties

None received - no customers or auditors engaged yet (status: Pre-ISMS,
per `COMPANY.md`).

## 6. Risk assessment results and risk treatment plan status

**Gap, logged honestly rather than skipped over**: no formal risk
assessment methodology or risk register exists yet (Clause 6.1.2/6.1.3).
`COMPANY.md` lists a risk register as a planned artifact but it hasn't
been started. This is a real, undone piece of the ISMS, not an
oversight to bury in a review - see action items below.

## 7. Opportunities for continual improvement

- Stand up a risk assessment methodology and register before too many
  more controls accumulate without one to justify their tier/priority
  against (see action items).
- The CEO/GRC-engineer role collapse (same gap noted in 5.2's RACI and
  5.3's segregation-of-duties doc) should be revisited the moment a
  second person joins - not a decision needed today, just a standing
  watch item.

## Decisions and action items

| # | Action | Owner | Target |
|---|---|---|---|
| 1 | Continue building Governance section (5.5, 5.6, 5.8) before moving to Identity and access management, per checklist build order | GRC/Security engineer | Ongoing |
| 2 | Stand up a risk assessment methodology + register (Clause 6.1.2/6.1.3) | GRC/Security engineer | Before Governance section is marked done |
| 3 | Rotate the AWS access keys that were shared in plaintext during this build cycle (tf-bootstrap-admin, tf-bootstrap-evidence, terraform-lab), since a chat transcript isn't a secure long-term credential store | CEO / Management representative | Next practical opportunity |
| 4 | Re-review CEO/GRC role segregation once a second team member exists | CEO / Management representative | On next hire |

## Next review

Due **2027-09-14** (annual cadence, per control 5.4 frontmatter), or
sooner if a material trigger occurs (a security incident, a new hire
changing the RACI, or the ISMS reaching a certification-readiness
milestone).
