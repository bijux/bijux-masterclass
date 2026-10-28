# Lab — Module 04: Transactions, Concurrency, ETags, and Idempotency

## Objective

Prove one hundred concurrent identical submissions create one logical run, stale ETags fail atomically, changed-body key reuse conflicts, and replay survives process restart.

## Setup conditions

The previous baseline is: **Projects, datasets, runs, jobs, artifacts, idempotency records, and subscriptions survive restart.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do public guarantees survive simultaneous requests, retries, lost responses, and process restart?*

## Failure action and investigation

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

## Operational oracle

One hundred synchronized identical requests produce exactly one run, one job, one idempotency record, and one original logical response; all others replay it.

## Required evidence

- baseline transcript proving the previous checkpoint before **Transactions, Concurrency, ETags, and Idempotency** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Draw the transaction boundary for each use case.
- public, durable, security, or operational observation showing: One hundred concurrent identical submissions create one run; stale ETags fail atomically; replay survives restart.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **transactional idempotency and conditional mutation**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Transactions, Concurrency, ETags, and Idempotency**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
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
