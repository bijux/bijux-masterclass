# Lab — Module 05: Production HTTP API Design

> **Module 05:** Production HTTP API Design

## Objective

Simulate twenty retries and two stale project writers, proving one logical run, body-bound idempotency, and no lost update in both providers.

## Why this lab matters

This lab turns the module’s governing question—**How should an HTTP API express asynchronous work, retries, conflicts, conditional updates, and machine-readable failures?**—into a falsifiable experiment. POST can be made safely retryable through an application-level idempotency key. The server scopes the key to a principal, binds it to a canonical request-body fingerprint, stores the logical result, and replays it for the same request. A changed body under the key is a conflict.

It advances the cumulative Analysis Runs Platform by requiring this result: **Add the analysis-run workflow, idempotency key, status resource, ETags, cancellation, and Problem Details**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **The contract becomes a modular source tree with deterministic baseline and frontier bundles.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How should an API express asynchronous work, retries, conflicts, pagination, and conditional mutation honestly?*

## Hypothesis

The clean implementation should satisfy this claim: **202 identifies status monitoring; same key/body creates one logical run; changed body under key is rejected; missing/stale/current If-Match branches are distinct; terminal states are stable; problem type/media type are consistent.** When the lab introduces this fault—**Plant a race-prone check-then-create implementation or remove the fingerprint check; prove a focused test fails, then repair it**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant a race-prone check-then-create implementation or remove the fingerprint check; prove a focused test fails, then repair it**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Simulate twenty retries and two stale project writers, proving one logical run, body-bound idempotency, and no lost update in both providers**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- 202 identifies status monitoring
- same key/body creates one logical run
- changed body under key is rejected
- missing/stale/current If-Match branches are distinct
- terminal states are stable
- problem type/media type are consistent

## Required evidence

- baseline transcript proving the previous checkpoint before **Production HTTP API Design** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Production HTTP API Design**
- focused result for: Use `202 Accepted` with a status resource.
- public, durable, security, or operational observation showing: The API can submit, monitor, cancel, and retrieve analysis runs and artifacts with explicit lifecycle semantics.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Production HTTP API Design**
- a limitation statement naming every live dependency required to support the strongest **Production HTTP API Design** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Production HTTP API Design**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant a race-prone check-then-create implementation or remove the fingerprint check; prove a focused test fails, then repair it** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Production HTTP API Design**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Production HTTP API Design** experiment.
3. Rerun the focused regression and `make module-proof MODULE=05`.
4. Confirm the system again provides this result: The API can submit, monitor, cancel, and retrieve analysis runs and artifacts with explicit lifecycle semantics.

## Completion gate

- 202 identifies status monitoring
- same key/body creates one logical run
- changed body under key is rejected
- missing/stale/current If-Match branches are distinct
- terminal states are stable
- problem type/media type are consistent

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Production HTTP API Design**. A green command without the negative case and causal explanation does not satisfy this gate.
