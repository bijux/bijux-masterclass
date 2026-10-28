# Lab — Module 08: Security in the Public Contract

> **Module 08:** Security in the Public Contract

## Objective

Prove every operation’s anonymous, authentication, scope, ownership, and scheme-alternative behavior in both providers using one generated security matrix.

## Why this lab matters

This lab turns the module’s governing question—**What can the public contract say about authentication and authorization, and what remains a runtime responsibility?**—into a falsifiable experiment. The capstone uses global bearer-or-API-key authentication and explicit anonymous health. Diagnostics overrides the root with an administrator scope. A mechanical matrix checks that no operation’s security decision is merely accidental omission. 4. Authentication, scope authorization, and ownership are separate gates

It advances the cumulative Analysis Runs Platform by requiring this result: **Describe API-key and OAuth-style schemes, scopes, anonymous overrides, and documented security failures**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Mock, generated-client, consumer, negative, and stateful checks exercise the same contract.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does the contract state who may call an operation and what failures clients can observe without pretending that documentation enforces policy?*

## Hypothesis

The clean implementation should satisfy this claim: **health is explicitly anonymous; each documented credential alternative works independently; missing/invalid/insufficient credentials are distinct; scope does not bypass ownership; webhook SSRF constraints execute; reports and examples contain only synthetic/redacted credentials.** When the lab introduces this fault—**Translate all security failures to documented Problem Details and add required challenge headers**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Extract effective root and operation-level security requirements into the scope matrix and translate each to plain Boolean logic.
2. Define deterministic principals for anonymous, invalid, read-only, write, other-owner, API-key, and administrator cases.
3. Implement one authentication adapter and reusable scope guards per provider; keep domain authorization in owner-aware store methods.
4. Translate all security failures to documented Problem Details and add required challenge headers.
5. Constrain webhook destinations and prove loopback/private/userinfo/unsupported-scheme cases are rejected before storage.
6. Run matrix-driven live tests against both providers, including same-scope wrong-owner artifact access.
7. Scan examples and reports for credential leakage and document the production identity-system boundary.

### Required planted defect

Choose one defect from Failure Modes. Before fixing it, keep:

```text
defect:
predicted first failing gate:
actual first failing gate:
minimal request/instance/diff:
root cause:
repair:
permanent regression location:
```

### Investigation notes

Before editing code, predict the first observable divergence caused by **Translate all security failures to documented Problem Details and add required challenge headers**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Prove every operation’s anonymous, authentication, scope, ownership, and scheme-alternative behavior in both providers using one generated security matrix**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- health is explicitly anonymous
- each documented credential alternative works independently
- missing/invalid/insufficient credentials are distinct
- scope does not bypass ownership
- webhook SSRF constraints execute
- reports and examples contain only synthetic/redacted credentials

## Required evidence

- baseline transcript proving the previous checkpoint before **Security in the Public Contract** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Security in the Public Contract**
- focused result for: Model API-key and bearer security schemes.
- public, durable, security, or operational observation showing: Every operation has an explicit security decision and cross-owner artifact access is rejected.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Security in the Public Contract**
- a limitation statement naming every live dependency required to support the strongest **Security in the Public Contract** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Security in the Public Contract**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Translate all security failures to documented Problem Details and add required challenge headers** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Security in the Public Contract**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Security in the Public Contract** experiment.
3. Rerun the focused regression and `make module-proof MODULE=08`.
4. Confirm the system again provides this result: Every operation has an explicit security decision and cross-owner artifact access is rejected.

## Completion gate

- health is explicitly anonymous
- each documented credential alternative works independently
- missing/invalid/insufficient credentials are distinct
- scope does not bypass ownership
- webhook SSRF constraints execute
- reports and examples contain only synthetic/redacted credentials

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Security in the Public Contract**. A green command without the negative case and causal explanation does not satisfy this gate.
