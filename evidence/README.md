# How to read this folder

This folder holds proof that Veridian Identity's security controls were
actually checked, automatically, on real dates, and that nobody edited
the results afterward. Written for an auditor reviewing evidence, not
assuming familiarity with how the underlying tooling works.

## Folder structure

```
evidence/
  controls/
    <section name>/                    e.g. "governance"
      <control number>-<control name>/  e.g. "5.1-policies-for-information-security"
        <date>_evidence-record.json     <- what was checked, and the result
        <date>_fingerprint.sha256       <- a checksum of that result
        <date>_signature.bundle.json    <- cryptographic proof it's untouched
```

Each control gets its own folder, named with both its official ISO
27001 Annex A number (e.g. `5.1`) and its control name (e.g. "policies
for information security"), so you can find a control either by number
or by browsing.

## What each file means

- **`..._evidence-record.json`**: the actual finding. Open it in any text
  editor. It says which control was checked, exactly when, and whether
  the result was `PASS`, `WARN` (needs attention soon), or `FAIL`. It
  also lists which specific policy/document/system was looked at.
- **`..._fingerprint.sha256`**: a short code that's mathematically unique
  to the evidence-record file above. If even one character in that file
  changed after the fact, this fingerprint would no longer match it.
- **`..._signature.bundle.json`**: proof of *when* and *by what process*
  the evidence-record was created, in a form nobody can fake or quietly
  edit after the fact. This is what lets you trust the record wasn't
  altered, backdated, or written by a person pretending a check happened
  when it didn't.

## How to independently verify a record (no trust required)

If you have `cosign` installed and the public key
(`scripts/evidence/.keys/local-dev.pub`, safe to share, contains no
secret), you can check any record yourself:

```
cosign verify-blob \
  --key scripts/evidence/.keys/local-dev.pub \
  --bundle evidence/controls/<section>/<control>/<date>_signature.bundle.json \
  evidence/controls/<section>/<control>/<date>_evidence-record.json
```

`Verified OK` means: this exact file, byte for byte, is what the
automated check produced on that date. Anything else means don't trust
the record.

## Why there's more than one file per check

Splitting "the finding," "its fingerprint," and "its signature" into
three files (rather than one) means the signature can prove the other
two haven't been tampered with, independently of anyone's word for it,
including ours.

## A note on the current signing method

Records right now are signed with a locally-generated key pair
(`signing_mode: "local-key-dev"` inside each evidence-record), because
there is no live CI pipeline running these checks yet. Once the
scheduled GitHub Actions workflow is in place, records switch to
"keyless" signing tied to that pipeline's own identity, which removes
even the small trust requirement of "we didn't leak the private key."
Every record states which signing mode produced it.
