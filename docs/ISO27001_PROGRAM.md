# ISO 27001 Program Index

This repo doubles as Veridian Identity's ISMS (Information Security
Management System) and control automation program, built the same way
you'd grade a GRC engineering capstone: gap by gap, with real Terraform,
real policy-as-code, real signed evidence. Except this time it's a full
ISO/IEC 27001:2022 Annex A implementation for a real company, not a
training exercise, documented as we go rather than written up after the
fact.

## Program documents

1. [`../COMPANY.md`](../COMPANY.md): who Veridian is, what it does, why it
   needs ISO 27001, and why this profile was chosen.
2. [`ISMS_SCOPE.md`](ISMS_SCOPE.md): formal ISMS scope (Clause 4.3)
3. [`STATEMENT_OF_APPLICABILITY.md`](STATEMENT_OF_APPLICABILITY.md): all 93
   Annex A controls, applicability, and **automation tier** (T1
   control-as-code / T2 automated-evidence / T3 documentary)
4. [`CONTINUOUS_EVIDENCE_ARCHITECTURE.md`](CONTINUOUS_EVIDENCE_ARCHITECTURE.md):
   why point-in-time screenshots fail as evidence, and the signed, scheduled,
   immutable pipeline design that replaces them

There's also a local-only `automated-controls/` build checklist (the 40
controls that meet the strict 100%-automatable bar), kept out of this repo
intentionally; it's a working tracker, not something published here.

## Repo layout (filling in as we build)

```
iso27001/
├── COMPANY.md                          # who Veridian is
├── docs/
│   ├── ISO27001_PROGRAM.md             # this file
│   ├── ISMS_SCOPE.md                   # Clause 4.3 scope
│   ├── STATEMENT_OF_APPLICABILITY.md   # all 93 controls + automation tier
│   ├── CONTINUOUS_EVIDENCE_ARCHITECTURE.md
│   ├── policies/                       # (planned) T3 policy documents
│   ├── vendors/                        # (planned) subprocessor security reviews
│   ├── runbooks/                       # (planned) operating procedures
│   └── adr/                            # (planned) architecture decision records
├── terraform/                           # (next) AWS baseline: VPC, KMS, evidence vault, CloudTrail, Config, GuardDuty
├── policies/                            # (next) Rego, one file per control cluster, tagged by Annex A control ID
├── oscal/                               # (next) component definitions mapping to Annex A
├── .github/workflows/                   # (next) event-triggered CI gate + scheduled re-attestation
├── evidence/                            # signed evidence manifests land here (or in a separate AWS account vault)
└── scripts/                             # verify-evidence.sh and similar
```

## Status

Pre-implementation. Company profile, scope, SoA, and evidence architecture
are drafted (v0); no Terraform/policy/CI has been written yet. Next step
per the SoA's build order: the T1 Technological control cluster (8.2 to 8.5,
8.8 to 8.9, 8.13, 8.15 to 8.17, 8.20 to 8.22, 8.24), starting with the
Terraform baseline.
