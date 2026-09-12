---
control_id: "5.1"
title: "Information Security Policy"
owner: "CEO / Management representative"
version: "1.0"
last_reviewed: "2026-09-12"
review_cadence_months: 12
next_review_due: "2027-09-12"
---

# Information Security Policy

## Purpose

This policy states Veridian Identity's commitment to protecting the
confidentiality, integrity, and availability of the information it
processes on behalf of itself and its customers, in support of the
ISO/IEC 27001:2022 ISMS defined in
[`ISMS_SCOPE.md`](../ISMS_SCOPE.md).

## Scope

Applies to all systems, data, and personnel within the ISMS scope: the
`veridian-verify` product, its supporting AWS infrastructure, and
everyone with access to RESTRICTED or CONFIDENTIAL data as classified in
[`COMPANY.md`](../../COMPANY.md).

## Policy statements

1. Information security objectives are set and reviewed at least
   annually by management (Clause 6.2, 9.3).
2. Every Annex A control's applicability and implementation is recorded
   in the [Statement of Applicability](../STATEMENT_OF_APPLICABILITY.md)
   and kept current as the system changes.
3. Controls are implemented as code wherever a control-as-code mechanism
   exists (Tier 1); where it doesn't, they are implemented as a
   documented, owned, dated process (Tier 2/3), never left undocumented.
4. All personnel with ISMS responsibilities are made aware of this
   policy and the specific policies/runbooks relevant to their role.
5. Non-conformities are tracked and corrected per Clause 10.1; repeat
   non-conformities trigger a policy or control redesign, not just
   another fix.
6. This policy, and every subordinate policy in `docs/policies/`, is
   reviewed at the cadence declared in its frontmatter
   (`review_cadence_months`) and re-dated on every review, whether or
   not content changed.

## Enforcement

Reviewed on a fixed cadence rather than left to expire silently: see
[`docs/IMPLEMENTATION_CHECKLIST.md`](../IMPLEMENTATION_CHECKLIST.md) for
the automation that checks `next_review_due` on a schedule and raises a
finding if this document (or any policy in this directory) goes stale.

## Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-09-12 | Initial policy, drafted as part of the Governance section build-out |
