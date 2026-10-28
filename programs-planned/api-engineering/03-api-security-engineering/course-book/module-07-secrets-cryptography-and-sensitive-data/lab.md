# Lab — Module 07: Secrets, Cryptography, and Sensitive Data

## Objective

Add secret wrappers/providers, recursive redaction, keyed pseudonyms, and audit chaining. Run a canary-secret scan across logs, exceptions, reports, and handoff. Plant a secret-bearing dataclass/default object representation and prove the canary leaks before repair.


## Setup conditions

The previous baseline is: **Webhook registration and delivery resist SSRF, body alteration, stale messages, and duplicate replay.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we use cryptographic mechanisms without exposing keys, inventing protocols, or leaking sensitive data through diagnostics?*

## Failure action and investigation

1. Implement and test: Distinguish hashing, HMAC, encryption, and password hashing.
2. Implement and test: Keep secret values out of representation and logs.
3. Implement and test: Rotate signing and verification keys with overlap.
4. Implement and test: Redact nested structures and embedded credentials.
5. Implement and test: Minimize, retain, and delete sensitive data deliberately.

### Required planted defect

Remove or bypass the central control for **Secrets, Cryptography, and Sensitive Data** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

The system satisfies the chapter’s central question: How do we use cryptographic mechanisms without exposing keys, inventing protocols, or leaking sensitive data through diagnostics? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Secrets, Cryptography, and Sensitive Data** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Distinguish hashing, HMAC, encryption, and password hashing.
- public, durable, security, or operational observation showing: Secrets become non-rendering values, audit records are privacy-bounded, and key rotation is testable.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **purpose-bound secrets and sensitive-data handling**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Secrets, Cryptography, and Sensitive Data**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=07`.
4. Confirm the system again provides this result: Secrets become non-rendering values, audit records are privacy-bounded, and key rotation is testable.

## Completion gate

- secret-provider boundary
- non-rendering values
- purpose-separated keys
- explicit algorithm profiles
- structural redaction
- pseudonymized audit
- rotation overlap proof
- no private material in handoff
