# Lab — Module 05: Production HTTP API Design

## Objective

Simulate twenty retries and two stale project writers, proving one logical run, body-bound idempotency, and no lost update in both providers.

## Setup conditions

The previous baseline is: **The contract becomes a modular source tree with deterministic baseline and frontier bundles.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How should an API express asynchronous work, retries, conflicts, pagination, and conditional mutation honestly?*

## Failure action and investigation

1. Draw the run state machine and enumerate every legal action/status pair before coding.
2. Add `202`, monitor Location, Retry-After, replay evidence, 409 branches, and artifact availability to the canonical contract.
3. Implement principal-scoped body-bound idempotency under an atomic training lock in both stores.
4. Implement ETag generation and If-Match evaluation at the project adapter/store boundary.
5. Add a retry-storm test, key-mismatch test, missing/stale/current precondition tests, and terminal-state cancellation tests.
6. Run provider-neutral live conformance and compare all response fields, not only object counts.
7. Plant a race-prone check-then-create implementation or remove the fingerprint check; prove a focused test fails, then repair it.

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

The system satisfies the chapter’s central question: How should an API express asynchronous work, retries, conflicts, pagination, and conditional mutation honestly? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Production HTTP API Design** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Use `202 Accepted` with a status resource.
- public, durable, security, or operational observation showing: The API can submit, monitor, cancel, and retrieve analysis runs and artifacts with explicit lifecycle semantics.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Production HTTP API Design**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Production HTTP API Design**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=05`.
4. Confirm the system again provides this result: The API can submit, monitor, cancel, and retrieve analysis runs and artifacts with explicit lifecycle semantics.

## Completion gate

- 202 identifies status monitoring
- same key/body creates one logical run
- changed body under key is rejected
- missing/stale/current If-Match branches are distinct
- terminal states are stable
- problem type/media type are consistent
