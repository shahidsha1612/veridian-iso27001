# 100% Automatable Controls: ISO/IEC 27001:2022 Annex A

Extracted from [`../docs/STATEMENT_OF_APPLICABILITY.md`](../docs/STATEMENT_OF_APPLICABILITY.md).
This file lists **only controls where both enforcement and evidence are
fully machine-driven, with zero ongoing human action**: what the SoA
calls Tier 1 (control-as-code). Nothing here needs a person to check a box,
take a screenshot, sign off, or remember to do anything on a recurring
basis; a policy engine evaluates live state and a pipeline produces signed
proof, on its own, forever, until the code that defines it changes.

**40 of 93 Annex A controls (approximately 43%) meet that bar.**

The other 53 controls are excluded here on purpose, not by oversight. See
"Why the rest can't hit 100%" below. They're still tracked (and most are
still worth automating the *evidence collection* for) in the SoA under
Tier 2/3, just not claimed as 100% here.

One honest caveat that applies to all 40: a human writes the Terraform/Rego
that defines each control once, at build time. "100% automatable" here
means **zero human action in the control's ongoing operation and
attestation**, not that no engineer ever touches a keyboard. If someone
edits the underlying `.tf`/`.rego` file, that's itself a change-managed,
reviewed action captured by 8.32 (change management), which is on this list.

---

## Organizational (14)
- [ ] 5.3: Segregation of duties. IAM role split (approve is not the same role as apply), OPA-checked
- [ ] 5.9: Inventory of information and other associated assets. Terraform state plus AWS Config aggregator equals live asset inventory
- [ ] 5.12: Classification of information. Required classification tags on all data-store resources, OPA-enforced
- [ ] 5.13: Labelling of information. Tag-value validation against approved classification set
- [ ] 5.14: Information transfer. Deny non-TLS transfer, OPA-enforced on S3/API policies
- [ ] 5.15: Access control. Least-privilege IAM as Terraform, OPA-checked
- [ ] 5.16: Identity management. Single IdP enforced, no local IAM users except break-glass
- [ ] 5.17: Authentication information. No static long-lived keys in CI (OIDC only), OPA-checked
- [ ] 5.21: Managing information security in the ICT supply chain. SBOM/dependency scan gates CI
- [ ] 5.23: Information security for use of cloud services. This repo's baseline is the control
- [ ] 5.28: Collection of evidence. The evidence pipeline itself (SHA-256 plus Cosign plus Object Lock)
- [ ] 5.29: Information security during disruption. Cross-region backup/DR Terraform plus automated restore-test
- [ ] 5.33: Protection of records. Object Lock (WORM) on evidence vault, Terraform-enforced retention
- [ ] 5.34: Privacy and protection of PII. Composite of tagging (5.12) plus encryption (8.24) plus deletion (8.10)

## Physical (1)
- [ ] 7.10: Storage media. No removable media (MDM-enforced) plus no local persistence of ID images, S3 lifecycle-enforced

## Technological (25)
- [ ] 8.2: Privileged access rights. MFA plus time-bound session policies, OPA denies standing privileged access
- [ ] 8.3: Information access restriction. Least-privilege IAM, OPA-checked
- [ ] 8.4: Access to source code. Branch protection plus required reviews, checked via GitHub API/Rego
- [ ] 8.5: Secure authentication. Org-wide MFA via IdP policy, Config rule fails on any principal without MFA
- [ ] 8.6: Capacity management. CloudWatch autoscaling/alarms in Terraform, alarm-history evidence
- [ ] 8.8: Management of technical vulnerabilities. Inspector/Trivy/Dependabot gate CI, scheduled re-scan
- [ ] 8.9: Configuration management. Terraform-only change path, AWS Config detects console drift
- [ ] 8.10: Information deletion. S3 lifecycle TTL on raw ID/biometric data, scheduled retention-compliance job
- [ ] 8.11: Data masking. Static check blocking raw PII-shaped fields in log statements
- [ ] 8.13: Information backup. AWS Backup plans in Terraform plus scheduled automated restore-test
- [ ] 8.14: Redundancy of information processing facilities. Multi-AZ Terraform, AZ-count check
- [ ] 8.15: Logging. CloudTrail org-wide/immutable, OPA checks enabled plus multi-region
- [ ] 8.16: Monitoring activities. GuardDuty plus Security Hub enabled via Terraform, scheduled still-enabled check
- [ ] 8.17: Clock synchronization. AWS Time Sync default, Config rule checks drift
- [ ] 8.19: Installation of software on operational systems. Immutable Lambda/container deploys only, OPA denies mutable EC2/SSH in prod
- [ ] 8.20: Networks security. Security-group-as-code, OPA denies broad ingress (0.0.0.0/0 on non-public resources)
- [ ] 8.21: Security of network services. TLS-only listeners enforced via Terraform plus OPA
- [ ] 8.22: Segregation of networks. Private subnets for data tier plus VPC gateway endpoints, OPA checks no public IP on data-tier resources
- [ ] 8.24: Use of cryptography. Customer-managed KMS keys required, OPA denies default/AWS-owned keys; TLS 1.2+ minimum
- [ ] 8.25: Secure development life cycle. The CI pipeline itself (plan, policy gate, test, sign, deploy)
- [ ] 8.28: Secure coding. SAST (Semgrep/CodeQL) required check, blocks merge on high-severity findings
- [ ] 8.29: Security testing in development and acceptance. CI test suite plus SAST/dependency scan gate the pipeline
- [ ] 8.31: Separation of development, test and production environments. Account-per-environment, OPA checks no cross-env ARN references
- [ ] 8.32: Change management. PR plus required review plus CI gate *is* the control; merged-PR/CI-run record is the evidence
- [ ] 8.33: Test information. Synthetic-only data in dev/staging, OPA checks no prod KMS key/ARN in non-prod Terraform

---

## Why the rest can't hit 100%

Two different reasons, and they matter differently:

**53 controls involve an irreducible human decision.** No amount of
tooling removes the person: hiring/screening (6.1), signing an NDA (6.6),
judging whether an incident was handled well (5.27), a legal register
review (5.31), an independent audit (5.35), a management review meeting
(5.4). You can automate the *paper trail* around these (that's the SoA's
Tier 2), but not the decision itself. Claiming otherwise to an auditor
would be a misrepresentation, not an automation win.

**A smaller set is automatable in principle but blocked on a missing
system of record.** For example, 6.3 (training) or 6.7 (remote-work device
compliance) could become near-100% evidence-wise once an LMS/MDM with a
usable API is chosen. They're just not there yet because that tooling
decision hasn't been made. These are the best candidates to promote later,
tracked in the SoA's Tier 2 section, not claimed here until they actually
clear the bar.

## Build order

Straight down the list above, Technological first (most direct extension
of the capstone pattern: Terraform baseline, then Rego detection, then CI
gate, then signed evidence), then the Organizational/Physical items that
ride on the same infrastructure (asset inventory, classification tagging,
evidence pipeline itself).
