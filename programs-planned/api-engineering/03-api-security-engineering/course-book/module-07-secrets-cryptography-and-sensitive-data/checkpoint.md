# Checkpoint — Module 07: Secrets, Cryptography, and Sensitive Data

## Required result

Add secret-provider boundaries, non-rendering values, redaction, pseudonymization, rotation, and privacy-bounded audit records.

## Demonstrate

- Distinguish hashing, HMAC, encryption, and password hashing.
- Keep secret values out of representation and logs.
- Rotate signing and verification keys with overlap.
- Redact nested structures and embedded credentials.
- Minimize, retain, and delete sensitive data deliberately.

## Commands

```bash
make module-proof MODULE=07 TRACK=python
make module-proof MODULE=07 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Secrets, Cryptography, and Sensitive Data** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Secrets, Cryptography, and Sensitive Data**
- focused result for: Distinguish hashing, HMAC, encryption, and password hashing.
- public, durable, security, or operational observation showing: Secrets become non-rendering values, audit records are privacy-bounded, and key rotation is testable.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **purpose-bound secrets and sensitive-data handling**
- a limitation statement naming every live dependency required to support the strongest **Secrets, Cryptography, and Sensitive Data** claim but not exercised

## Defend the design

1. Answer the central question: **How do we use cryptographic mechanisms without exposing keys, inventing protocols, or leaking sensitive data through diagnostics?**
2. Demonstrate this capstone result: Secrets become non-rendering values, audit records are privacy-bounded, and key rotation is testable.
3. Show the **Secrets, Cryptography, and Sensitive Data** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: secrets never render, keys are separated by purpose, redaction is recursive, and rotation has explicit overlap and retirement.
5. State which environment-backed **Secrets, Cryptography, and Sensitive Data** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Secrets become non-rendering values, audit records are privacy-bounded, and key rotation is testable.—all focused checks pass, the **Secrets, Cryptography, and Sensitive Data** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
