# Veridian Identity, Inc.: Company Profile

> **This is a fictional company.** It exists solely to give a full
> ISO/IEC 27001:2022 Annex A control automation program a realistic subject
> to build against and prove out. No legal entity, product, employees, or
> customer data exist behind it. See
> [`docs/ISO27001_PROGRAM.md`](docs/ISO27001_PROGRAM.md) for the full
> purpose and scope statement.

## Why this company, why this shape

You asked for a company "real enough to actually implement ISO 27001
against." That requires two things most fictional exercises skip: (1) a
data type sensitive enough that ISO 27001 is a genuine business
requirement, not a nice-to-have, and (2) an in-house software development
function, since half of Annex A (8.25 to 8.34, plus chunks of 5.8/5.9/8.4)
only exists to govern a company that *writes and ships its own code*.

**Picked profile: B2B identity verification (KYC/IDV) platform.**

Reasoning:
- **Sensitive data is unambiguous.** Government ID images, biometric
  templates (face match), full PII (name, DOB, national ID/SSN, address),
  and verification-decision data. There's no "is this actually sensitive"
  debate: this is precisely the data ISO 27001 exists to protect.
- **ISO 27001 is a real sales requirement here, not a vanity cert.** Banks,
  fintechs, and marketplaces who buy identity verification will not sign a
  contract without it (often SOC 2 too). This gives every control a genuine
  business reason to exist, not just "the exercise says so."
- **It forces a real SDLC.** The product *is* software: a verification API,
  document OCR/liveness pipeline, and a customer-facing dashboard. That
  means A.8.25 to 8.34 (secure development lifecycle) aren't hypothetical;
  there's actually a repo, a CI pipeline, environments, and code to secure.
- **It's the same technical shape as your capstones**, generalized: instead
  of one flawed Lambda API mapped to one framework's subset of controls,
  this is a real (if small) SaaS system, and the full 93-control Annex A
  catalog gets mapped against it.

If this profile is wrong for what you actually want to build, say so before
we go further. The ISMS scope, risk register, and Terraform baseline all
key off this identity.

## Company facts (assume these unless corrected)

| | |
|---|---|
| Name | Veridian Identity, Inc. |
| Product | `veridian-verify`: API + dashboard for identity verification (ID document capture, liveness/selfie match, PII record checks, sanctions/watchlist screening) sold to fintech, marketplace, and banking customers |
| Stage | Early-stage startup, roughly 8 to 15 people, fully remote |
| Customers | B2B only; other companies embed the API into their own onboarding flows |
| Data handled | Government ID images, biometric face templates, full PII (name, DOB, national ID, address), verification decisions/audit trail, customer API credentials |
| Data classification | RESTRICTED (ID images, biometrics), CONFIDENTIAL (PII, decisions), INTERNAL (product telemetry), PUBLIC (marketing site) |
| Regulatory context | GDPR/UK GDPR plus US state privacy law (as data processor for customers' end users). ISO 27001 is the primary security framework; SOC 2 Type II is a near-term secondary goal reusing the same evidence |
| Why ISO 27001 | Enterprise/bank customers require it pre-contract; it's the fastest way to make "trust us with your users' government IDs" a verifiable claim instead of a marketing line |
| Cloud/infra | AWS, single primary region to start (`eu-west-1`, since most customers and their end users are EU/UK, and it keeps data-residency questions simple), single AWS account today with a separate account planned for the evidence vault (see architecture doc) |
| Environments | `dev`, `staging`, `prod`: physically separate AWS accounts (A.8.31) |
| Repo / SCM | GitHub, this repo tree functions as the ISMS and automation monorepo; the product codebase is assumed to live in a sibling repo (`veridian-verify-app`, not yet created, out of scope for now, referenced but not built here) |
| Status | Pre-ISMS. Nothing certified yet. This repo is where the ISMS gets built, gap by gap, control by control, with evidence generated as we go, not written up after the fact |

## Roles (minimal, for a company this size)

| Role | Who (for now) | ISO 27001 relevance |
|---|---|---|
| CEO / Management representative | You | Management commitment (Clause 5), risk acceptance |
| GRC/Security engineer | You | Owns this repo: control implementation, policy-as-code, evidence pipeline (this is the role your capstones trained for) |
| Engineering | (placeholder, future hires) | Subject to SDLC controls (8.25 to 8.34), access controls (8.2 to 8.4) |
| Everyone (once hired) | (placeholder) | People controls (6.1 to 6.8): screening, training, NDAs |

## What this repo is going to contain, built incrementally

1. `docs/ISMS_SCOPE.md`: formal scope statement (Clause 4.3)
2. `docs/STATEMENT_OF_APPLICABILITY.md`: all 93 Annex A controls, applicability, and **automation tier**
3. `docs/CONTINUOUS_EVIDENCE_ARCHITECTURE.md`: how evidence stays valid continuously instead of going stale the moment it's captured
4. `terraform/`: the real AWS baseline for `veridian-verify`'s infrastructure
5. `policies/`: OPA/Rego policies enforcing and detecting control state, mapped to Annex A control IDs
6. `oscal/`: machine-readable component definitions mapping implementation to Annex A
7. `.github/workflows/`: CI gate (per-change) **and** scheduled re-attestation (per-day/week) pipelines
8. `evidence/`: evidence manifests, signed and hash-chained
9. A risk register and internal policies (Clause 6/organizational controls) as we reach the controls that require them

We build this the same way the capstones were graded: gap by gap, prevention
(Terraform), then detection (Rego), then attestation (OSCAL), then evidence
(signed, continuously re-verified), then written up (WRITEUP-style rationale
per control).
