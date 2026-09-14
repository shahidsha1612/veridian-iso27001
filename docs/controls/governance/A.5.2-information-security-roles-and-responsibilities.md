---
control_id: "5.2"
title: "Information Security Roles and Responsibilities (RACI)"
owner: "CEO / Management representative"
version: "1.0"
last_reviewed: "2026-09-14"
review_cadence_months: 6
next_review_due: "2027-03-14"
---

# Information Security Roles and Responsibilities (RACI)

## Purpose

Assigns who is **R**esponsible (does the work), **A**ccountable (answers
for the outcome; exactly one per domain), **C**onsulted (asked for
input before a decision), and **I**nformed (told after the fact) for
each information security control domain, per ISO/IEC 27001:2022
control 5.2.

## Scope

Applies to the same roles defined in
[`COMPANY.md`](../../../COMPANY.md#roles-minimal-for-a-company-this-size):
CEO / Management representative, GRC/Security engineer, Engineering,
and Everyone (once hired).

## RACI matrix

Uses the same 15-section grouping as
[`docs/IMPLEMENTATION_CHECKLIST.md`](../../IMPLEMENTATION_CHECKLIST.md)
so this table and the build tracker stay in sync as controls get built.

| # | Domain | CEO / Mgmt rep | GRC/Security engineer | Engineering | Everyone |
|---|---|---|---|---|---|
| 1 | Governance | A | R | I | I |
| 2 | Identity and access management | I | A | R | C |
| 3 | Asset management | I | A | R | R |
| 4 | Information protection | I | A | R | C |
| 5 | Human resources security | A | R | C | R *(as subject)* |
| 6 | Physical security | I | A | C | R |
| 7 | System and network security | I | A | R | I |
| 8 | Application security | I | A | R | C |
| 9 | Secure configuration | I | A | R | I |
| 10 | Threat and vulnerability management | I | A | C | I |
| 11 | Continuity | A | R | C | I |
| 12 | Supplier relationships security | A | R | C | I |
| 13 | Legal and compliance | A | R | C | I |
| 14 | Information security event management | I | A | C | R *(reporting)* |
| 15 | Information security assurance | A | R | I | I |

## Known gap this table makes explicit, not hidden

Today the CEO / Management representative and GRC/Security engineer
rows are the same person, so several domains show that one person as
both Accountable and Responsible. That is a real segregation-of-duties
gap for a company this size; it is tracked and compensated for at the
technical layer (no single person can both approve and apply a change)
rather than by role separation, in control 5.3 (Segregation of duties),
not papered over here.

## Review trigger

Re-reviewed immediately on any role change, new hire, or org
restructure - not only at the calendar cadence in this file's
frontmatter, which exists as a backstop in case no such change occurs.

## Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-09-14 | Extracted from `COMPANY.md`'s roles table into its own control document under `docs/controls/governance/` |
