---
control_id: "5.5"
title: "Contact with Authorities"
owner: "CEO / Management representative"
version: "1.0"
last_reviewed: "2026-09-14"
review_cadence_months: 12
next_review_due: "2027-09-14"
---

# Contact with Authorities

## Purpose

Ensures appropriate contacts with relevant authorities are maintained,
per ISO/IEC 27001:2022 control 5.5, so that legal/regulatory
notification obligations and requests for assistance don't have to be
figured out for the first time during an actual incident.

## Scope note

This doc covers the "who, and under what trigger" for control 5.5
specifically. The fuller Incident Response Plan (control 5.24, section
14 - Information security event management, not yet built) will fold
this same contact list into its detect/triage/contain/notify workflow.
Building 5.5 now, standalone, isn't duplicated work: the list itself
doesn't change when 5.24 is built later, only its surrounding process
does.

## Authority contact list and trigger criteria

| Authority | Relevance to Veridian | Trigger criteria |
|---|---|---|
| **Data Protection Commission (Ireland)** - lead EU supervisory authority candidate, since AWS infrastructure is hosted in `eu-west-1` (Ireland) | GDPR enforcement for EU personal data (government ID images, biometric templates, PII processed on behalf of customers) | A personal data breach likely to result in a risk to individuals' rights and freedoms: notify within **72 hours** of becoming aware, per GDPR Art. 33 |
| **Information Commissioner's Office (UK)** | UK GDPR enforcement - Veridian's customers and their end users are predominantly EU/UK per `COMPANY.md` | Same 72-hour breach-notification trigger, under UK GDPR, for UK-related personal data |
| **UK National Cyber Security Centre (NCSC)** | National CSIRT; voluntary/sector cyber-incident reporting and threat-intel sharing | A significant cyber incident (e.g., confirmed intrusion, ransomware, large-scale credential compromise) meeting NCSC's reporting guidance thresholds |
| **Local law enforcement (Action Fraud / national police cybercrime unit)** | Criminal activity affecting Veridian or its customers | Suspected criminal activity: unauthorized access, fraud, extortion, or theft of company/customer data |
| **AWS Trust & Safety / AWS Abuse (`abuse@amazonaws.com`, AWS Support)** | Not a government authority, but the critical first call for any incident involving the underlying cloud infrastructure | Any suspected compromise of AWS account credentials, abuse originating from Veridian's AWS resources, or need for AWS-side forensic/log assistance |

## Who initiates contact

Per the RACI matrix in
[`A.5.2-...md`](A.5.2-information-security-roles-and-responsibilities.md),
the CEO / Management representative is Accountable for Governance and
is the one who authorizes and makes contact with external authorities;
the GRC/Security engineer prepares the factual basis (what happened,
scope, evidence) beforehand.

## Known limitation, stated plainly

No incident has ever triggered this list (status: Pre-ISMS, nothing
certified, no incidents to date). This is a prepared-but-untested
contact path, not a proven one - the same honest framing already used
for the RACI (5.2) and segregation-of-duties (5.3) gaps. It gets
exercised for real, or as a tabletop exercise, once control 5.24
(Incident response planning) is built.

## Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-09-14 | Initial contact list and trigger criteria |
