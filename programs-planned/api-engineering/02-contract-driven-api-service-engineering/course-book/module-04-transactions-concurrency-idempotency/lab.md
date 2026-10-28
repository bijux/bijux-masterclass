# Lab — Module 04: Transactions, Concurrency, ETags, and Idempotency

> **Module 04:** Transactions, Concurrency, ETags, and Idempotency

## Objective

Prove one hundred concurrent identical submissions create one logical run, stale ETags fail atomically, changed-body key reuse conflicts, and replay survives process restart.

## Why this lab matters

This lab turns the module’s governing question—**How do idempotency and conditional updates remain atomic under concurrent requests and process restarts?**—into a falsifiable experiment. Write transaction diagrams for analysis submission and project conditional update. Implement scoped idempotency reservation, fingerprint binding, and stored response in the primary repository. Implement atomic ETag update with resource-bound parsing. Inject failure after each statement of submission and prove rollback. Run sequential replay, changed-body conflict, cross-principal reuse, and restart replay.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement persistent request fingerprints, replayed outcomes, version columns, ETags, and transaction rollback**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Projects, datasets, runs, jobs, artifacts, idempotency records, and subscriptions survive restart.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do public guarantees survive simultaneous requests, retries, lost responses, and process restart?*

## Hypothesis

The clean implementation should satisfy this claim: **One hundred synchronized identical requests produce exactly one run, one job, one idempotency record, and one original logical response; all others replay it.** When the lab introduces this fault—**Plant a pre-read/unconditional-update path, capture the double-success counterexample, repair, and retain the race test**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. **Write transaction diagrams for analysis submission and project conditional update.**
2. **Implement scoped idempotency reservation, fingerprint binding, and stored response in the primary repository.**
3. **Implement atomic ETag update with resource-bound parsing.**
4. **Inject failure after each statement of submission and prove rollback.**
5. **Run sequential replay, changed-body conflict, cross-principal reuse, and restart replay.**
6. **Run 100 barrier-synchronized duplicate submissions and assert one run/job/idempotency record.**
7. **Run two PATCH requests with one ETag and assert one success and one precondition failure.**
8. **Plant a pre-read/unconditional-update path, capture the double-success counterexample, repair, and retain the race test.**

### Required planted defect

> Replace the conditional update with `SELECT version` followed by `UPDATE ... WHERE id`. The two-request barrier must demonstrate double success.

Preserve the following evidence:

```text
prediction:
change introduced:
minimal setup:
first failing command:
public symptom:
durable/process state:
root cause:
repair:
regression path:
remaining limitation:
```

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant a pre-read/unconditional-update path, capture the double-success counterexample, repair, and retain the race test**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Prove one hundred concurrent identical submissions create one logical run, stale ETags fail atomically, changed-body key reuse conflicts, and replay survives process restart**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

One hundred synchronized identical requests produce exactly one run, one job, one idempotency record, and one original logical response; all others replay it.

## Required evidence

- baseline transcript proving the previous checkpoint before **Transactions, Concurrency, ETags, and Idempotency** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Transactions, Concurrency, ETags, and Idempotency**
- focused result for: Draw the transaction boundary for each use case.
- public, durable, security, or operational observation showing: One hundred concurrent identical submissions create one run; stale ETags fail atomically; replay survives restart.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **transactional idempotency and conditional mutation**
- a limitation statement naming every live dependency required to support the strongest **Transactions, Concurrency, ETags, and Idempotency** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Transactions, Concurrency, ETags, and Idempotency**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant a pre-read/unconditional-update path, capture the double-success counterexample, repair, and retain the race test** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Transactions, Concurrency, ETags, and Idempotency**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Transactions, Concurrency, ETags, and Idempotency** experiment.
3. Rerun the focused regression and `make module-proof MODULE=04`.
4. Confirm the system again provides this result: One hundred concurrent identical submissions create one run; stale ETags fail atomically; replay survives restart.

## Completion gate

- single logical submission
- persistent replay
- body mismatch conflict
- principal scoping
- atomic ETag
- resource-bound validator
- no partial rollback
- bounded safe retry

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Transactions, Concurrency, ETags, and Idempotency**. A green command without the negative case and causal explanation does not satisfy this gate.
