# Statement of Applicability: ISO/IEC 27001:2022 Annex A

**Scope:** see [`ISMS_SCOPE.md`](ISMS_SCOPE.md). **Organization:** Veridian
Identity, Inc. **Status:** draft v0. Applicability and automation tier
assigned; implementation not yet built (tracked separately as we go,
gap by gap, in the style of the capstones).

## Automation tier legend

This is the key idea this whole program is built around: **the tier is not
about whether the control matters, it's about how its evidence is
produced**, so that evidence stays true instead of expiring the moment it's
captured.

| Tier | Meaning | Evidence characteristic |
|---|---|---|
| **T1: Control-as-code** | The control is *enforced* by Terraform/OPA/CI: a non-compliant state either can't be created or is blocked at the gate. Evidence is a signed, timestamped artifact produced by the same pipeline that enforces it, re-verified on a schedule (not just at deploy time). | Continuous, machine-verified, self-invalidating if drift occurs |
| **T2: Automated evidence, human-operated control** | The control itself requires a human decision or action (hiring, training, incident triage), but proof that it happened is pulled automatically from a system of record (HRIS/LMS/ticketing API) on a schedule and hash-chained into the same evidence vault. | Continuous collection, but the underlying action is manual |
| **T3: Documentary / periodic manual** | No reliable API/system of record exists yet to automate collection. Control is implemented via written policy plus scheduled manual review/attestation, version-controlled in this repo so at least the *policy's* history is auditable. Candidate to promote to T2 once a system of record exists. | Point-in-time, refreshed on a fixed cadence, explicitly dated |
| **N/A** | Not applicable given current scope (see justification column) | n/a |

A "screenshot taken once, stale immediately" evidence model is exactly what
T1/T2 are designed to eliminate: every T1/T2 control's evidence has a
**freshness SLA** (re-checked automatically at a defined interval) and an
**alerting path** if a re-check fails, so drift is caught between audits,
not discovered by the auditor.

---

## A.5: Organizational controls (37)

| ID | Control | Applicable | Tier | Mechanism / evidence source |
|---|---|---|---|---|
| 5.1 | Policies for information security | Y | T3 to T2 | Policy doc in `docs/controls/governance/A.5.1-...md`; promote to T2 once tracked via a policy-management tool with read-receipts API |
| 5.2 | Information security roles and responsibilities | Y | T3 | RACI doc in `docs/controls/governance/A.5.2-...md`; reviewed at each org change |
| 5.3 | Segregation of duties | Y | T1 | IAM policy structure (no single role can both approve *and* apply Terraform changes) enforced via OPA on IAM/role definitions plus branch protection (required PR approval, approver is `github-actions[bot]`, never the human author) - see `docs/controls/governance/A.5.3-...md` |
| 5.4 | Management responsibilities | Y | T3 | Management review minutes, versioned in `docs/management-reviews/` |
| 5.5 | Contact with authorities | Y | T3 | Documented contact list plus trigger criteria in incident response plan |
| 5.6 | Contact with special interest groups | Y | T3 | Membership record (e.g., ISACs, cloud security forums) |
| 5.7 | Threat intelligence | Y | T2 | Automated feed ingestion (e.g., AWS GuardDuty threat intel, CISA KEV feed) logged with timestamp of last pull |
| 5.8 | Information security in project management | Y | T2 | CI/PR template requiring a security-review checkbox before merge; evidence is a GitHub API pull of PR metadata |
| 5.9 | Inventory of information and other associated assets | Y | T1 | Terraform state plus AWS Config aggregator equals live asset inventory, queried on schedule, diffed against expected |
| 5.10 | Acceptable use of information and other associated assets | Y | T3 to T2 | Policy doc; promote to T2 via e-signature/HRIS acknowledgment API |
| 5.11 | Return of assets | Y | T2 | Offboarding checklist ticket plus MDM "device wiped/returned" API status pulled at closure |
| 5.12 | Classification of information | Y | T1 | Data classification tags enforced as required Terraform tags on all S3/DynamoDB resources; OPA policy fails plan if untagged |
| 5.13 | Labelling of information | Y | T1 | Same tagging mechanism as 5.12; OPA validates tag values against the approved classification set |
| 5.14 | Information transfer | Y | T1 | TLS-only bucket/API policies enforced via OPA (reuses the PayVault-style "deny non-TLS" pattern) |
| 5.15 | Access control | Y | T1 | IAM policies as Terraform, least-privilege enforced by OPA (denies wildcard actions/resources, reusing the PayVault PV-06 / Acme GAP-07 pattern) |
| 5.16 | Identity management | Y | T1 | Single IdP (AWS IAM Identity Center / SSO) as the sole identity source, enforced; no local IAM users allowed except break-glass, OPA-checked |
| 5.17 | Authentication information (secrets/credentials) | Y | T1 | No long-lived static keys in CI (OIDC federation only); OPA/CI check fails a workflow that references static AWS keys; secrets manager for app secrets |
| 5.18 | Access rights | Y | T2 | Quarterly access review: script pulls current IAM/SSO assignments, diffs against an approved roster, produces a signed review artifact |
| 5.19 | Information security in supplier relationships | Y | T3 | Vendor security review checklist per subprocessor, stored in `docs/vendors/` |
| 5.20 | Addressing information security within supplier agreements | Y | T3 | DPA/security addendum on file per vendor |
| 5.21 | Managing information security in the ICT supply chain | Y | T1 | Dependency/SBOM scanning in CI (e.g., Dependabot/Trivy) gates merges on critical CVEs |
| 5.22 | Monitoring, review and change management of supplier services | Y | T2 | Automated subprocessor status-page/uptime polling plus annual review ticket |
| 5.23 | Information security for use of cloud services | Y | T1 | This entire repo (Terraform baseline plus OPA plus Config rules) *is* the control |
| 5.24 | Information security incident management planning and preparation | Y | T3 | Incident response plan doc, tabletop exercise log |
| 5.25 | Assessment and decision on information security events | Y | T2 | GuardDuty/Security Hub findings auto-create tickets with severity; evidence is the ticket system API |
| 5.26 | Response to information security incidents | Y | T2 | Incident tickets with timestamps (detect, triage, contain, resolve) pulled from ticketing API for MTTR evidence |
| 5.27 | Learning from information security incidents | Y | T3 | Post-incident review doc per incident |
| 5.28 | Collection of evidence | Y | T1 | This is the evidence pipeline itself: SHA-256 plus Cosign plus Object Lock (the mechanism this whole program is built on) |
| 5.29 | Information security during disruption | Y | T1 | Backup/DR Terraform (cross-region replication, tested restore) plus automated restore-test evidence |
| 5.30 | ICT readiness for business continuity | Y | T2 | Scheduled DR game-day; evidence is the automated restore-test job result, signed |
| 5.31 | Legal, statutory, regulatory and contractual requirements | Y | T3 | Legal/regulatory register doc, reviewed with counsel |
| 5.32 | Intellectual property rights | Y | T3 | License compliance scan in CI (e.g., license-checker); could promote to T1 |
| 5.33 | Protection of records | Y | T1 | Object Lock (WORM) on evidence vault plus backup retention policy enforced via Terraform |
| 5.34 | Privacy and protection of PII | Y | T1 | Data classification tagging (5.12) plus encryption (8.24) plus retention/deletion jobs (8.10): a composite of other T1 controls, with a DPIA doc for the biometric-data special-category question |
| 5.35 | Independent review of information security | Y | T3 | External audit/pen test report, annually |
| 5.36 | Compliance with policies, rules and standards for information security | Y | T2 | OPA policy-pass rate across all repos, pulled from CI history as a compliance dashboard metric |
| 5.37 | Documented operating procedures | Y | T3 to T2 | Runbooks in `docs/runbooks/`; promote to T2 via "last reviewed" metadata check in CI |

## A.6: People controls (8)

| ID | Control | Applicable | Tier | Mechanism / evidence source |
|---|---|---|---|---|
| 6.1 | Screening | Y | T2 | Background-check vendor API status ("cleared" / date) pulled per new hire |
| 6.2 | Terms and conditions of employment | Y | T2 | HRIS e-signature status API (contract includes security responsibilities clause) |
| 6.3 | Information security awareness, education and training | Y | T2 | LMS completion-rate API, pulled on schedule, per employee |
| 6.4 | Disciplinary process | Y | T3 | HR policy doc; case records are confidential/manual by nature |
| 6.5 | Responsibilities after termination or change of employment | Y | T2 | Offboarding automation: IdP account disable timestamp vs. termination date, pulled from IdP API (a strong automation candidate, since time-to-deprovision is a classic finding) |
| 6.6 | Confidentiality or non-disclosure agreements | Y | T2 | E-signature API status per employee/contractor |
| 6.7 | Remote working | Y | T2 | MDM compliance status API (disk encryption on, screen lock on, OS patched) per company-issued device; Veridian is fully remote, so this control carries unusual weight |
| 6.8 | Information security event reporting | Y | T2 | Ticketing system: count/timestamp of employee-reported events, pulled for trend evidence |

## A.7: Physical controls (14)

Scope note: Veridian has no company-controlled office; these are scoped to
**home-working environments and company-issued endpoints** per
`ISMS_SCOPE.md`.

| ID | Control | Applicable | Tier | Mechanism / evidence source |
|---|---|---|---|---|
| 7.1 | Physical security perimeters | N/A | n/a | No company facility. Cloud provider's physical security (AWS data centers) covered by AWS's own ISO 27001/SOC 2 certs, referenced as a subprocessor control (5.19), not re-audited by Veridian |
| 7.2 | Physical entry | N/A | n/a | Same as 7.1 |
| 7.3 | Securing offices, rooms and facilities | N/A | n/a | Same as 7.1 |
| 7.4 | Physical security monitoring | N/A | n/a | Same as 7.1 |
| 7.5 | Protecting against physical and environmental threats | N/A | n/a | Same as 7.1 (data-center side); no equivalent requirement for home offices under this scope |
| 7.6 | Working in secure areas | N/A | n/a | No secure area designated |
| 7.7 | Clear desk and clear screen | Y | T2 | MDM policy: auto-lock timeout enforced and status pulled per device |
| 7.8 | Equipment siting and protection | Y | T3 | Remote-work policy (no public-space handling of unlocked devices with customer data visible) |
| 7.9 | Security of assets off-premises | Y | T2 | MDM device-encryption plus remote-wipe capability status per device |
| 7.10 | Storage media | Y | T1 | No removable media permitted by policy; enforced via MDM device policy plus no local persistence of ID images (processed in-memory/short-TTL S3 only), verified via S3 lifecycle policy in Terraform |
| 7.11 | Supporting utilities | N/A | n/a | Cloud provider responsibility (power/cooling), covered by AWS's own certifications |
| 7.12 | Cabling security | N/A | n/a | Cloud provider responsibility |
| 7.13 | Equipment maintenance | Y | T2 | MDM OS/patch-level status per device, pulled on schedule |
| 7.14 | Secure disposal or re-use of equipment | Y | T2 | MDM remote-wipe confirmation on offboarding, tied to 6.5 |

## A.8: Technological controls (34)

This is the automation core, where the capstone pattern (Terraform plus OPA
plus CI plus signed evidence) applies most directly.

| ID | Control | Applicable | Tier | Mechanism / evidence source |
|---|---|---|---|---|
| 8.1 | User endpoint devices | Y | T2 | MDM compliance API (encryption, patch, screen-lock) per device |
| 8.2 | Privileged access rights | Y | T1 | IAM policy-as-code: privileged roles require MFA and are time-bound (session policies); OPA denies standing privileged access |
| 8.3 | Information access restriction | Y | T1 | Least-privilege IAM (reuses 5.15 mechanism), OPA-checked |
| 8.4 | Access to source code | Y | T1 | GitHub branch protection plus required reviews plus no direct pushes to `main`, checked via GitHub API/Rego against repo settings |
| 8.5 | Secure authentication | Y | T1 | MFA enforced org-wide via IAM Identity Center policy; OPA/Config rule fails if any IAM principal lacks MFA |
| 8.6 | Capacity management | Y | T1 | CloudWatch autoscaling plus alarms defined in Terraform; evidence is an alarm-history query |
| 8.7 | Protection against malware | Y | T2 | Endpoint/EDR agent status API (for laptops); GuardDuty malware-protection for S3/EC2 findings as the infra-side equivalent |
| 8.8 | Management of technical vulnerabilities | Y | T1 | AWS Inspector / Trivy / Dependabot scans gate CI; unresolved criticals beyond SLA fail a scheduled re-check |
| 8.9 | Configuration management | Y | T1 | Terraform is the sole change path (no console changes); enforced via AWS Config rule detecting drift from Terraform-managed state |
| 8.10 | Information deletion | Y | T1 | S3 lifecycle policies (short TTL on raw ID images/biometrics post-verification) as Terraform, verified by a scheduled job confirming no objects exceed retention |
| 8.11 | Data masking | Y | T1 | PII masked in logs via structured logging filters (OPA/code-review-enforced pattern: no raw PAN/PII-shaped fields in log statements, static check in CI) |
| 8.12 | Data leakage prevention | Y | T2 | Macie scan results (S3 PII/sensitive-data detection) pulled on schedule |
| 8.13 | Information backup | Y | T1 | AWS Backup plans in Terraform plus scheduled automated restore-test producing signed proof-of-restore evidence |
| 8.14 | Redundancy of information processing facilities | Y | T1 | Multi-AZ Terraform config; evidence is an AZ count check against expected |
| 8.15 | Logging | Y | T1 | CloudTrail (org-wide, immutable to evidence vault) plus application logs; OPA checks CloudTrail is enabled and multi-region on every account |
| 8.16 | Monitoring activities | Y | T1 | GuardDuty plus Security Hub enabled via Terraform; scheduled check confirms still-enabled (not silently disabled) |
| 8.17 | Clock synchronization | Y | T1 | NTP/AWS Time Sync Service default on all compute; Config rule checks drift |
| 8.18 | Use of privileged utility programs | Y | T2 | Session Manager (no SSH) logs reviewed; use-of-break-glass-role events pulled from CloudTrail |
| 8.19 | Installation of software on operational systems | Y | T1 | Immutable Lambda/container deploys only (no in-place package installs on running prod compute); architecture-level control, checked via a "no SSH/no mutable EC2 in prod" OPA rule |
| 8.20 | Networks security | Y | T1 | VPC/security-group-as-code, OPA denies overly broad ingress (0.0.0.0/0 on non-public resources) |
| 8.21 | Security of network services | Y | T1 | TLS-only ALB/API Gateway listeners enforced via Terraform plus OPA |
| 8.22 | Segregation of networks | Y | T1 | Private subnets for data-tier resources, VPC gateway endpoints (reuses the Acme Health capstone pattern), OPA checks no data-tier resource has a public IP |
| 8.23 | Web filtering | Y | T3 | DNS-filtering policy on managed endpoints (via MDM); low priority given B2B API product with minimal general web browsing risk surface |
| 8.24 | Use of cryptography | Y | T1 | Customer-managed KMS keys on all data stores, enforced via OPA (denies default/AWS-owned keys, reusing the PayVault PV-01/PV-03 and Acme GAP-01/02 pattern); TLS 1.2+ minimum |
| 8.25 | Secure development life cycle | Y | T1 | This CI pipeline itself: plan, then policy gate, then test, then sign, then deploy, defined in `.github/workflows/` |
| 8.26 | Application security requirements | Y | T2 | Threat-model doc per feature (template in `docs/`), tracked as a required PR label; evidence is PR metadata |
| 8.27 | Secure system architecture and engineering principles | Y | T3 | Architecture decision records (ADRs) in `docs/adr/` |
| 8.28 | Secure coding | Y | T1 | SAST (e.g., Semgrep/CodeQL) required check in CI, blocking merge on high-severity findings |
| 8.29 | Security testing in development and acceptance | Y | T1 | CI test suite plus SAST/dependency scan plus (planned) periodic DAST/pen test, all gating the same pipeline |
| 8.30 | Outsourced development | N/A | n/a | No outsourced development at current company size; revisit if contractors are engaged |
| 8.31 | Separation of development, test and production environments | Y | T1 | Separate AWS accounts per environment (Terraform workspace/account-per-env), OPA checks prod resources never reference dev/staging ARNs |
| 8.32 | Change management | Y | T1 | PR plus required review plus CI gate equals the change management control; evidence is the merged-PR plus CI-run record itself |
| 8.33 | Test information | Y | T1 | Synthetic-only data in dev/staging enforced via seed-data policy plus OPA check that no production KMS key/ARN appears in non-prod Terraform |
| 8.34 | Protection of information systems during audit testing | Y | T2 | Pen-test scoping doc plus rate-limited/read-only credentials issued per engagement, logged via CloudTrail for the engagement window |

---

## Automation tier summary

| Tier | Count (approx.) | Where they cluster |
|---|---|---|
| T1 (control-as-code) | ~40 | Almost all of A.8 (Technological), plus the A.5 controls that are really infrastructure (5.9, 5.12 to 5.17, 5.21, 5.23, 5.28 to 5.29, 5.33 to 5.34) |
| T2 (automated evidence, manual control) | ~35 | Most of A.6 (People), most physical controls once endpoints are in scope, and A.5 controls tied to HR/vendor/incident process |
| T3 (documentary) | ~15 | Governance/strategic controls (policy existence, management review, legal register, ADRs) that are inherently human-authored documents. The goal is to keep these versioned and dated, not fully automate them away |
| N/A | 3 | 7.1 to 7.6 physical-facility subset (no office) minus 7.7/7.9/7.10/7.13/7.14 which are kept as endpoint-scoped; 8.30 (no outsourced dev) |

**Build order (next steps, to be executed the same gap-by-gap way as the
capstones):** start with the T1 Technological cluster (8.2 to 8.5, 8.8 to
8.9, 8.13, 8.15 to 8.17, 8.20 to 8.22, 8.24) since it's the highest-leverage,
most capstone-familiar work. Terraform baseline first, then the matching
Rego policies, then the CI gate, then the evidence chain, then OSCAL
mapping. People/physical (T2) automation comes next once real HRIS/MDM/LMS
tooling is chosen (not yet selected, flag when we get there).
