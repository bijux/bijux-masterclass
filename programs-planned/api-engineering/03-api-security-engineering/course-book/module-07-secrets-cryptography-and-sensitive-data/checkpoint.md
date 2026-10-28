# Checkpoint — Module 07: Secrets, Cryptography, and Sensitive Data

## Required result

Secrets become non-rendering values, audit records are privacy-bounded, and key rotation is testable.

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

## Defend the design

1. Answer the central question: **How do we use cryptographic mechanisms without exposing keys, inventing protocols, or leaking sensitive data through diagnostics?**
2. Demonstrate this capstone result: Secrets become non-rendering values, audit records are privacy-bounded, and key rotation is testable.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: secrets never render, keys are separated by purpose, redaction is recursive, and rotation has explicit overlap and retirement.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Secrets become non-rendering values, audit records are privacy-bounded, and key rotation is testable.—all focused checks pass, the **Secrets, Cryptography, and Sensitive Data** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
