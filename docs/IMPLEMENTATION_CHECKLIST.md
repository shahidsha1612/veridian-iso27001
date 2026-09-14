# Implementation Checklist

Working build tracker for turning the [Statement of
Applicability](STATEMENT_OF_APPLICABILITY.md) into actual Terraform, Rego,
CI, evidence, and policy documents. Grouped the way the internal audit
cheat sheet groups Annex A (by practitioner topic, not by Annex A's own
5/6/7/8 numbering), because that's the order we're building in: **one
tagged section at a time, top to bottom, finished before moving to the
next.**

"Finished" for a section means every control in it, regardless of tier,
has its full artifact in place, not just the Tier 1 ones:

- **T1** control: Terraform + Rego/OPA policy + CI gate + signed,
  scheduled evidence check.
- **T2** control: the automated evidence pull (script/API call against a
  system of record) + the doc describing the human process it's
  evidencing.
- **T3** control: the actual policy/runbook/register document, dated and
  version-controlled, not a stub.

Nothing gets left as a placeholder inside a section that's marked done.

After a section's checklist is fully checked, we write up the section as
a LinkedIn post (drafted in `docs/linkedin/`) before moving to the next
section.

## Progress

| # | Section | Controls | Status |
|---|---|---|---|
| 1 | [Governance](#1-governance) | 7 | Done |
| 2 | [Identity and access management](#2-identity-and-access-management) | 8 | Not started |
| 3 | [Asset management](#3-asset-management) | 6 | Not started |
| 4 | [Information protection](#4-information-protection) | 8 | Not started |
| 5 | [Human resources security](#5-human-resources-security) | 6 | Not started |
| 6 | [Physical security](#6-physical-security) | 14 | Not started |
| 7 | [System and network security](#7-system-and-network-security) | 7 | Not started |
| 8 | [Application security](#8-application-security) | 7 | Not started |
| 9 | [Secure configuration](#9-secure-configuration) | 3 | Not started |
| 10 | [Threat and vulnerability management](#10-threat-and-vulnerability-management) | 2 | Not started |
| 11 | [Continuity](#11-continuity) | 5 | Not started |
| 12 | [Supplier relationships security](#12-supplier-relationships-security) | 5 | Not started |
| 13 | [Legal and compliance](#13-legal-and-compliance) | 4 | Not started |
| 14 | [Information security event management](#14-information-security-event-management) | 9 | Not started |
| 15 | [Information security assurance](#15-information-security-assurance) | 1 | Not started |

---

## 1. Governance

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 5.1 | Policies for information security | T3→T2 | [x] | [x] | Policy doc in `docs/controls/governance/A.5.1-...md` + automated freshness check; evidence in `evidence/controls/governance/5.1-.../` |
| 5.2 | Information security roles and responsibilities | T3 | [x] | [x] | RACI matrix in `docs/controls/governance/A.5.2-...md`, linked from `COMPANY.md`; freshness-checked by the same script as 5.1, evidence in `evidence/controls/governance/5.2-.../` |
| 5.3 | Segregation of duties | T1 | [x] | [x] | Terraform IAM role split (not yet applied, no AWS account) + OPA policy/tests + CI gate with bot auto-approval + live branch protection; evidence in `evidence/controls/governance/5.3-.../`; see `docs/controls/governance/A.5.3-...md` |
| 5.4 | Management responsibilities | T3 | [x] | [x] | Management review minutes in `docs/management-reviews/`; control doc in `docs/controls/governance/A.5.4-...md`; evidence in `evidence/controls/governance/5.4-.../` |
| 5.5 | Contact with authorities | T3 | [x] | [x] | Authority contact list + trigger criteria in `docs/controls/governance/A.5.5-...md`; evidence in `evidence/controls/governance/5.5-.../` |
| 5.6 | Contact with special interest groups | T3 | [x] | [x] | Membership record in `docs/controls/governance/A.5.6-...md`; evidence in `evidence/controls/governance/5.6-.../` |
| 5.8 | Information security in project management | T2 | [x] | [x] | Issue form (kickoff) + PR template (delivery) + GitHub API evidence pull; see `docs/controls/governance/A.5.8-...md`; evidence in `evidence/controls/governance/5.8-.../` |

**LinkedIn write-up:** [ ] `docs/linkedin/01-governance.md`

## 2. Identity and access management

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 5.15 | Access control | T1 | [ ] | [ ] | Least-privilege IAM as Terraform, OPA-checked |
| 5.16 | Identity management | T1 | [ ] | [ ] | Single IdP/SSO, no local IAM users except break-glass |
| 5.17 | Authentication information | T1 | [ ] | [ ] | No static long-lived keys in CI (OIDC only) |
| 5.18 | Access rights | T2 | [ ] | [ ] | Quarterly access review script + signed artifact |
| 8.2 | Privileged access rights | T1 | [ ] | [ ] | MFA + time-bound sessions, OPA denies standing access |
| 8.3 | Information access restriction | T1 | [ ] | [ ] | Least-privilege IAM (reuses 5.15) |
| 8.4 | Access to source code | T1 | [ ] | [ ] | Branch protection + required reviews via GitHub API/Rego |
| 8.5 | Secure authentication | T1 | [ ] | [ ] | Org-wide MFA, Config rule fails ungated principals |

**LinkedIn write-up:** [ ] `docs/linkedin/02-identity-and-access-management.md`

## 3. Asset management

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 5.9 | Inventory of assets | T1 | [ ] | [ ] | Terraform state + AWS Config aggregator |
| 5.10 | Acceptable use policy | T3→T2 | [ ] | [ ] | Policy doc |
| 5.11 | Return of assets | T2 | [ ] | [ ] | Offboarding checklist + MDM wipe/return status |
| 5.37 | Documented operating procedures | T3→T2 | [ ] | [ ] | Runbooks in `docs/runbooks/` |
| 6.7 | Remote working | T2 | [ ] | [ ] | MDM compliance status API |
| 8.1 | User endpoint devices | T2 | [ ] | [ ] | MDM compliance API (encryption, patch, screen-lock) |

**LinkedIn write-up:** [ ] `docs/linkedin/03-asset-management.md`

## 4. Information protection

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 5.12 | Classification of information | T1 | [ ] | [ ] | Required classification tags, OPA-enforced |
| 5.13 | Labelling of information | T1 | [ ] | [ ] | Tag-value validation against approved set |
| 5.14 | Information transfer | T1 | [ ] | [ ] | Deny non-TLS transfer, OPA-enforced |
| 5.34 | Privacy and protection of PII | T1 | [ ] | [ ] | Composite of 5.12 + 8.24 + 8.10, plus DPIA doc |
| 8.10 | Information deletion | T1 | [ ] | [ ] | S3 lifecycle TTL, scheduled retention-compliance job |
| 8.11 | Data masking | T1 | [ ] | [ ] | Static check blocking raw PII in logs |
| 8.12 | Data leakage prevention | T2 | [ ] | [ ] | Macie scan results pulled on schedule |
| 8.33 | Test information | T1 | [ ] | [ ] | Synthetic-only data, OPA checks no prod ARN in non-prod |

**LinkedIn write-up:** [ ] `docs/linkedin/04-information-protection.md`

## 5. Human resources security

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 6.1 | Screening | T2 | [ ] | [ ] | Background-check vendor API status |
| 6.2 | Terms and conditions of employment | T2 | [ ] | [ ] | HRIS e-signature status API |
| 6.3 | Information security awareness, education and training | T2 | [ ] | [ ] | LMS completion-rate API |
| 6.4 | Disciplinary process | T3 | [ ] | [ ] | HR policy doc |
| 6.5 | Responsibilities after termination or change of employment | T2 | [ ] | [ ] | IdP disable timestamp vs. termination date |
| 6.6 | Confidentiality or non-disclosure agreements | T2 | [ ] | [ ] | E-signature API status |

**LinkedIn write-up:** [ ] `docs/linkedin/05-human-resources-security.md`

## 6. Physical security

Scope note: Veridian has no company-controlled office; scoped to
home-working environments and company-issued endpoints per
[`ISMS_SCOPE.md`](ISMS_SCOPE.md).

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 7.1 | Physical security perimeters | N/A | - | - | AWS data center, covered by AWS certs (5.19) |
| 7.2 | Physical entry | N/A | - | - | Same as 7.1 |
| 7.3 | Securing offices, rooms and facilities | N/A | - | - | Same as 7.1 |
| 7.4 | Physical security monitoring | N/A | - | - | Same as 7.1 |
| 7.5 | Protecting against physical and environmental threats | N/A | - | - | Same as 7.1 |
| 7.6 | Working in secure areas | N/A | - | - | No secure area designated |
| 7.7 | Clear desk and clear screen | T2 | [ ] | [ ] | MDM auto-lock timeout status |
| 7.8 | Equipment siting and protection | T3 | [ ] | [ ] | Remote-work policy |
| 7.9 | Security of assets off-premises | T2 | [ ] | [ ] | MDM encryption + remote-wipe status |
| 7.10 | Storage media | T1 | [ ] | [ ] | No removable media (MDM), no local persistence (S3 lifecycle) |
| 7.11 | Supporting utilities | N/A | - | - | Cloud provider responsibility |
| 7.12 | Cabling security | N/A | - | - | Cloud provider responsibility |
| 7.13 | Equipment maintenance | T2 | [ ] | [ ] | MDM OS/patch-level status |
| 7.14 | Secure disposal or re-use of equipment | T2 | [ ] | [ ] | MDM remote-wipe confirmation, tied to 6.5 |

**LinkedIn write-up:** [ ] `docs/linkedin/06-physical-security.md`

## 7. System and network security

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 8.7 | Protection against malware | T2 | [ ] | [ ] | EDR agent status API + GuardDuty malware findings |
| 8.18 | Use of privileged utility programs | T2 | [ ] | [ ] | Session Manager logs, break-glass events from CloudTrail |
| 8.20 | Networks security | T1 | [ ] | [ ] | Security-group-as-code, OPA denies broad ingress |
| 8.21 | Security of network services | T1 | [ ] | [ ] | TLS-only listeners, Terraform + OPA |
| 8.22 | Segregation of networks | T1 | [ ] | [ ] | Private subnets for data tier, OPA checks no public IP |
| 8.23 | Web filtering | T3 | [ ] | [ ] | DNS-filtering policy via MDM |
| 8.34 | Protection of information systems during audit testing | T2 | [ ] | [ ] | Pen-test scoping doc + scoped credentials, CloudTrail-logged |

**LinkedIn write-up:** [ ] `docs/linkedin/07-system-and-network-security.md`

## 8. Application security

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 8.25 | Secure development life cycle | T1 | [ ] | [ ] | The CI pipeline itself: plan, gate, test, sign, deploy |
| 8.26 | Application security requirements | T2 | [ ] | [ ] | Threat-model doc per feature, required PR label |
| 8.27 | Secure system architecture and engineering principles | T3 | [ ] | [ ] | ADRs in `docs/adr/` |
| 8.28 | Secure coding | T1 | [ ] | [ ] | SAST required check, blocks merge on high severity |
| 8.29 | Security testing in development and acceptance | T1 | [ ] | [ ] | CI test suite + SAST/dependency scan gate |
| 8.31 | Separation of development, test and production environments | T1 | [ ] | [ ] | Account-per-environment, OPA checks no cross-env ARNs |
| 8.32 | Change management | T1 | [ ] | [ ] | PR + required review + CI gate is the control |

**LinkedIn write-up:** [ ] `docs/linkedin/08-application-security.md`

## 9. Secure configuration

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 8.9 | Configuration management | T1 | [ ] | [ ] | Terraform-only change path, Config detects drift |
| 8.19 | Installation of software on operational systems | T1 | [ ] | [ ] | Immutable Lambda/container deploys only |
| 8.24 | Use of cryptography | T1 | [ ] | [ ] | Customer-managed KMS required, TLS 1.2+ minimum |

**LinkedIn write-up:** [ ] `docs/linkedin/09-secure-configuration.md`

## 10. Threat and vulnerability management

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 5.7 | Threat intelligence | T2 | [ ] | [ ] | Automated feed ingestion, timestamped last pull |
| 8.8 | Management of technical vulnerabilities | T1 | [ ] | [ ] | Inspector/Trivy/Dependabot gate CI, scheduled re-scan |

**LinkedIn write-up:** [ ] `docs/linkedin/10-threat-and-vulnerability-management.md`

## 11. Continuity

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 5.29 | Information security during disruption | T1 | [ ] | [ ] | Cross-region backup/DR Terraform + automated restore-test |
| 5.30 | ICT readiness for business continuity | T2 | [ ] | [ ] | Scheduled DR game-day, signed restore-test result |
| 8.6 | Capacity management | T1 | [ ] | [ ] | CloudWatch autoscaling/alarms, alarm-history evidence |
| 8.13 | Information backup | T1 | [ ] | [ ] | AWS Backup plans + scheduled automated restore-test |
| 8.14 | Redundancy of information processing facilities | T1 | [ ] | [ ] | Multi-AZ Terraform, AZ-count check |

**LinkedIn write-up:** [ ] `docs/linkedin/11-continuity.md`

## 12. Supplier relationships security

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 5.19 | Information security in supplier relationships | T3 | [ ] | [ ] | Vendor security review checklist in `docs/vendors/` |
| 5.20 | Addressing information security within supplier agreements | T3 | [ ] | [ ] | DPA/security addendum on file |
| 5.21 | Managing information security in the ICT supply chain | T1 | [ ] | [ ] | SBOM/dependency scan gates CI |
| 5.22 | Monitoring, review and change management of supplier services | T2 | [ ] | [ ] | Subprocessor status-page polling + annual review ticket |
| 5.23 | Information security for use of cloud services | T1 | [ ] | [ ] | This repo's baseline is the control |

**LinkedIn write-up:** [ ] `docs/linkedin/12-supplier-relationships-security.md`

## 13. Legal and compliance

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 5.31 | Legal, statutory, regulatory and contractual requirements | T3 | [ ] | [ ] | Legal/regulatory register, reviewed with counsel |
| 5.32 | Intellectual property rights | T3 | [ ] | [ ] | License compliance scan in CI |
| 5.33 | Protection of records | T1 | [ ] | [ ] | Object Lock (WORM) on evidence vault, Terraform-enforced |
| 5.36 | Compliance with policies, rules and standards for information security | T2 | [ ] | [ ] | OPA policy-pass rate pulled from CI history |

**LinkedIn write-up:** [ ] `docs/linkedin/13-legal-and-compliance.md`

## 14. Information security event management

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 5.24 | Information security incident management planning and preparation | T3 | [ ] | [ ] | Incident response plan + tabletop exercise log |
| 5.25 | Assessment and decision on information security events | T2 | [ ] | [ ] | GuardDuty/Security Hub auto-creates tickets by severity |
| 5.26 | Response to information security incidents | T2 | [ ] | [ ] | Incident tickets with detect/triage/contain/resolve timestamps |
| 5.27 | Learning from information security incidents | T3 | [ ] | [ ] | Post-incident review doc per incident |
| 5.28 | Collection of evidence | T1 | [ ] | [ ] | SHA-256 + Cosign + Object Lock evidence pipeline |
| 6.8 | Information security event reporting | T2 | [ ] | [ ] | Ticketing system count/timestamp of reported events |
| 8.15 | Logging | T1 | [ ] | [ ] | CloudTrail org-wide/immutable, OPA checks enabled + multi-region |
| 8.16 | Monitoring activities | T1 | [ ] | [ ] | GuardDuty + Security Hub, scheduled still-enabled check |
| 8.17 | Clock synchronization | T1 | [ ] | [ ] | AWS Time Sync default, Config rule checks drift |

**LinkedIn write-up:** [ ] `docs/linkedin/14-information-security-event-management.md`

## 15. Information security assurance

| Control | Name | Tier | Built | Evidence wired | Notes |
|---|---|---|---|---|---|
| 5.35 | Independent review of information security | T3 | [ ] | [ ] | External audit/pen test report, annually |

**LinkedIn write-up:** [ ] `docs/linkedin/15-information-security-assurance.md`

---

## How to use this file

1. Pick the first section with unchecked boxes (we go in the order above,
   top to bottom).
2. Build every control in it end to end: Terraform/Rego for T1, the
   automated evidence pull for T2, the actual policy/runbook/register
   document for T3.
3. Check off "Built" once the artifact exists and is reviewable in this
   repo, and "Evidence wired" once there's a signed/scheduled artifact
   (or, for T3, a dated document) proving it, not just code that could
   theoretically produce one.
4. Mark the section's row in the Progress table `Done` once every control
   in it is checked.
5. Write the LinkedIn post for the section, save it to
   `docs/linkedin/`, check that box, then move to the next section.
