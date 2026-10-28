# Lab — Module 07: Secrets, Cryptography, and Sensitive Data

> **Module 07:** Secrets, Cryptography, and Sensitive Data

## Objective

Add secret wrappers/providers, recursive redaction, keyed pseudonyms, and audit chaining. Run a canary-secret scan across logs, exceptions, reports, and handoff. Plant a secret-bearing dataclass/default object representation and prove the canary leaks before repair.

## Why this lab matters

This lab turns the module’s governing question—**How should secrets, cryptographic keys, sensitive fields, logs, retention, and audit evidence be handled?**—into a falsifiable experiment. A secret is not merely a string hidden from Git. It is created, distributed, held in memory, used for one purpose, rotated, revoked, audited, and eventually destroyed. Design that lifecycle before choosing whether the local adapter reads a file, environment variable, operating-system key store, or managed secret service.

It advances the cumulative Analysis Runs Platform by requiring this result: **Add secret-provider boundaries, non-rendering values, redaction, pseudonymization, rotation, and privacy-bounded audit records**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Webhook registration and delivery resist SSRF, body alteration, stale messages, and duplicate replay.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we use cryptographic mechanisms without exposing keys, inventing protocols, or leaking sensitive data through diagnostics?*

## Hypothesis

The clean implementation should satisfy this claim: **secret-provider boundary; non-rendering values; purpose-separated keys; explicit algorithm profiles; structural redaction; pseudonymized audit; rotation overlap proof; no private material in handoff.** When the lab introduces this fault—**Remove or bypass the central control for Secrets, Cryptography, and Sensitive Data in a temporary branch**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Implement and test: Distinguish hashing, HMAC, encryption, and password hashing.
2. Implement and test: Keep secret values out of representation and logs.
3. Implement and test: Rotate signing and verification keys with overlap.
4. Implement and test: Redact nested structures and embedded credentials.
5. Implement and test: Minimize, retain, and delete sensitive data deliberately.

### Required planted defect

Remove or bypass the central control for **Secrets, Cryptography, and Sensitive Data** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Remove or bypass the central control for Secrets, Cryptography, and Sensitive Data in a temporary branch**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Add secret wrappers/providers, recursive redaction, keyed pseudonyms, and audit chaining. Run a canary-secret scan across logs, exceptions, reports, and handoff. Plant a secret-bearing dataclass/default object representation and prove the canary leaks before repair**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- secret-provider boundary
- non-rendering values
- purpose-separated keys
- explicit algorithm profiles
- structural redaction
- pseudonymized audit
- rotation overlap proof
- no private material in handoff

## Required evidence

- baseline transcript proving the previous checkpoint before **Secrets, Cryptography, and Sensitive Data** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Secrets, Cryptography, and Sensitive Data**
- focused result for: Distinguish hashing, HMAC, encryption, and password hashing.
- public, durable, security, or operational observation showing: Secrets become non-rendering values, audit records are privacy-bounded, and key rotation is testable.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **purpose-bound secrets and sensitive-data handling**
- a limitation statement naming every live dependency required to support the strongest **Secrets, Cryptography, and Sensitive Data** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Secrets, Cryptography, and Sensitive Data**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Remove or bypass the central control for Secrets, Cryptography, and Sensitive Data in a temporary branch** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Secrets, Cryptography, and Sensitive Data**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Secrets, Cryptography, and Sensitive Data** experiment.
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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Secrets, Cryptography, and Sensitive Data**. A green command without the negative case and causal explanation does not satisfy this gate.
