# Checkpoint — Module 02: Deadlines, Cancellation, and Retry Budgets

## Required result

Ingress requests, database calls, artifact operations, and webhooks share finite budgets without retry amplification.

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

## Defend the design

1. Answer the central question: **How does one request carry a finite time budget through dependencies without multiplying work or reporting success too late?**
2. Demonstrate this capstone result: Ingress requests, database calls, artifact operations, and webhooks share finite budgets without retry amplification.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: one caller budget is partitioned across attempts and dependencies without resetting at each layer or retrying unsafe effects.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Ingress requests, database calls, artifact operations, and webhooks share finite budgets without retry amplification.—all focused checks pass, the **Deadlines, Cancellation, and Retry Budgets** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
