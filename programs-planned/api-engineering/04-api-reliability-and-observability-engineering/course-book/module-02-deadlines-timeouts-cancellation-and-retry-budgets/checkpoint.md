# Checkpoint — Module 02: Deadlines, Cancellation, and Retry Budgets

## Required result

Implement monotonic deadlines, child budgets, safe retry classification, backoff, Retry-After handling, and cancellation.

## Demonstrate

- Distinguish absolute deadlines from per-call timeouts.
- Budget connect, pool, transaction, read, write, and cleanup waits.
- Preserve committed durable work after caller cancellation.
- Retry only safe or idempotent effects.
- Use bounded backoff, jitter, and `Retry-After` inside the remaining budget.

## Commands

```bash
make module-proof MODULE=02
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Deadlines, Cancellation, and Retry Budgets** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Deadlines, Cancellation, and Retry Budgets**
- focused result for: Distinguish absolute deadlines from per-call timeouts.
- public, durable, security, or operational observation showing: Ingress requests, database calls, artifact operations, and webhooks share finite budgets without retry amplification.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **absolute deadline propagation**
- a limitation statement naming every live dependency required to support the strongest **Deadlines, Cancellation, and Retry Budgets** claim but not exercised

## Defend the design

1. Answer the central question: **How does one request carry a finite time budget through dependencies without multiplying work or reporting success too late?**
2. Demonstrate this capstone result: Ingress requests, database calls, artifact operations, and webhooks share finite budgets without retry amplification.
3. Show the **Deadlines, Cancellation, and Retry Budgets** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: one caller budget is partitioned across attempts and dependencies without resetting at each layer or retrying unsafe effects.
5. State which environment-backed **Deadlines, Cancellation, and Retry Budgets** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Ingress requests, database calls, artifact operations, and webhooks share finite budgets without retry amplification.—all focused checks pass, the **Deadlines, Cancellation, and Retry Budgets** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
