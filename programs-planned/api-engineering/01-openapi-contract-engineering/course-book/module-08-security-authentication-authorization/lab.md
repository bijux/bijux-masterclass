# Lab — Module 08: Security in the Public Contract

## Objective

Prove every operation’s anonymous, authentication, scope, ownership, and scheme-alternative behavior in both providers using one generated security matrix.

## Setup conditions

The previous baseline is: **Mock, generated-client, consumer, negative, and stateful checks exercise the same contract.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does the contract state who may call an operation and what failures clients can observe without pretending that documentation enforces policy?*

## Failure action and investigation

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

## Operational oracle

The system satisfies the chapter’s central question: How does the contract state who may call an operation and what failures clients can observe without pretending that documentation enforces policy? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Security in the Public Contract** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Model API-key and bearer security schemes.
- public, durable, security, or operational observation showing: Every operation has an explicit security decision and cross-owner artifact access is rejected.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Security in the Public Contract**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Security in the Public Contract**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=08`.
4. Confirm the system again provides this result: Every operation has an explicit security decision and cross-owner artifact access is rejected.

## Completion gate

- health is explicitly anonymous
- each documented credential alternative works independently
- missing/invalid/insufficient credentials are distinct
- scope does not bypass ownership
- webhook SSRF constraints execute
- reports and examples contain only synthetic/redacted credentials
