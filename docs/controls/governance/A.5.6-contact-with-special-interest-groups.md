---
control_id: "5.6"
title: "Contact with Special Interest Groups"
owner: "GRC/Security engineer"
version: "1.0"
last_reviewed: "2026-09-14"
review_cadence_months: 12
next_review_due: "2027-09-14"
---

# Contact with Special Interest Groups

## Purpose

Ensures appropriate contact with special interest groups, security
forums, and professional associations is maintained, per ISO/IEC
27001:2022 control 5.6. Distinct from control 5.5 (Contact with
authorities): this is about improving security knowledge and getting
early warning of vulnerabilities/attacks through voluntary community
membership, not regulatory/legal notification obligations.

## What membership is actually for

Per the control's intent, this isn't membership for its own sake. Each
group below is tied to a concrete reason:

- Early warning of relevant vulnerabilities and attack techniques
- Access to specialist information security advice
- Sharing/exchanging information about new technologies, products,
  threats, and vulnerabilities
- An established liaison point for cross-community coordination if an
  incident needs it

## Groups and status

| Group | Relevance to Veridian | Status |
|---|---|---|
| **FIDO Alliance** | Standards body for authentication, including the face-match/liveness biometric verification at the core of `veridian-verify`. Early warning on authentication-related vulnerabilities directly affects the product. | Tracked, not yet joined (Pre-ISMS/pre-launch; see `COMPANY.md`) |
| **Cloud Security Alliance (CSA)** | Cloud security best practices and threat intelligence, directly relevant given the AWS-based infrastructure (`terraform/`). | Tracked, not yet joined |
| **OWASP** | Web application security community; feeds directly into the secure development lifecycle controls (8.25-8.29, not yet built). Participation is free/community-level, no formal membership required to consume advisories. | Following advisories informally; no formal membership needed |
| **UK NCSC's CiSP (Cyber Security Information Sharing Partnership)** | Voluntary threat-intelligence sharing community. Distinct from NCSC's role as a regulatory contact in [`A.5.5-...md`](A.5.5-contact-with-authorities.md) - this is the information-sharing side, not the incident-notification side. | Tracked, not yet joined |

## Known limitation, stated plainly

None of these are active memberships yet - Veridian is pre-launch
(status: Pre-ISMS, per `COMPANY.md`), so there's no live product
surface yet that would make membership operationally urgent. This
control is satisfied by having identified the right groups and the
concrete reason for each, tracked here with an owner and a review
cadence, rather than joining prematurely for the sake of a checkbox.
Actual membership should be revisited once the product has a real
external attack surface (i.e., once controls 8.25-8.32 are built and
`veridian-verify` exists as more than a referenced sibling repo).

## Who owns this

Per the RACI matrix in
[`A.5.2-...md`](A.5.2-information-security-roles-and-responsibilities.md),
the GRC/Security engineer is Accountable for this domain and
responsible for initiating any of the above memberships when the time
comes.

## Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-09-14 | Initial group identification and rationale |
