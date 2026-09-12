# ISMS Scope Statement (ISO/IEC 27001:2022 Clause 4.3)

## Scope declaration

The Information Security Management System (ISMS) of **Veridian Identity,
Inc.** covers:

> The people, processes, and technology involved in the design, development,
> operation, and support of the `veridian-verify` identity verification
> platform (API and customer dashboard), including all AWS infrastructure
> that stores, processes, or transmits customer end-user identity data
> (government ID images, biometric templates, PII, and verification
> results), and the software development lifecycle used to build and
> deploy that platform.

## In scope

- Production, staging, and development AWS environments (accounts) hosting `veridian-verify`
- The source code repositories, CI/CD pipeline, and build/release process for `veridian-verify`
- Identity and access management for all systems in scope (employee and service identities)
- The evidence vault and compliance-automation tooling itself (this repo's Terraform/policies/CI), since a compromise of the tooling that *proves* control operation is itself a security risk
- Company-managed employee endpoints used to access in-scope systems
- Third-party/subprocessor relationships where the subprocessor touches in-scope data (cloud provider, any OCR/liveness ML vendor, email/support tooling that touches customer data)

## Out of scope (for now, explicitly, not by omission)

- Marketing website and blog (no customer/end-user data processed there)
- Internal-only tooling with no path to customer data (e.g., a future internal wiki), until such a path exists
- Physical offices. Veridian is fully remote; no company-controlled office space exists. Physical controls (Annex A clause 7) are scoped to **employee home-working environments and company-issued endpoints only**, not to a facility.
- Customers' own systems downstream of the API response (Veridian controls its side of the boundary; customer-side handling of the verification result is the customer's own ISMS problem)

## Interested parties and their requirements (Clause 4.2, feeds scope)

| Interested party | Requirement relevant to scope |
|---|---|
| Enterprise/bank customers | ISO 27001 certification as a contractual precondition; SOC 2 Type II as a near-term secondary ask |
| End users (data subjects, not Veridian's direct customers) | GDPR/UK GDPR rights over their PII and biometric data, processed by Veridian as a processor on behalf of its customers (controllers) |
| Regulators (EU/UK data protection authorities) | Lawful processing of biometric data (special category under GDPR Art. 9) |
| Employees | Clear security responsibilities, screening, training (People controls) |
| Cloud/subprocessors (AWS, any OCR/liveness vendor) | Contractual security requirements flow down via supplier controls (5.19–5.22) |

## Boundary diagram (textual, until a real one is drawn)

```
[Customer's app] --(HTTPS, API key/OAuth)--> [veridian-verify API, AWS prod account]
                                                 |-- Lambda/ECS verification service
                                                 |-- S3 (ID images/biometrics, encrypted, short TTL)
                                                 |-- DynamoDB/RDS (verification records)
                                                 |-- KMS (customer-managed keys)
                                                 |-- CloudTrail/Config/GuardDuty (logging/detection)
                                                 '-- Evidence vault (separate account, planned) <- signed control evidence
[Employee laptop] --(SSO/MFA)--> [AWS IAM Identity Center] --> scoped access to dev/staging/prod
[GitHub: veridian-verify-app repo] --(CI/CD)--> [prod account, via OIDC role, gated by OPA/Conftest]
```

## Scope review

This statement is reviewed whenever: a new AWS account/service is added, a
new subprocessor is engaged, a new data type is collected, or at minimum
annually alongside management review (Clause 9.3). Track changes to this
file via git history: that history *is* the scope-review evidence trail.
