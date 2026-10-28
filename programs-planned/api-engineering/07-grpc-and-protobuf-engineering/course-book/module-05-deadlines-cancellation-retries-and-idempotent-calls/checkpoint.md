# Checkpoint — Module 05: Deadlines, Cancellation, Retries, and Idempotent Calls

## Required result

Implement deadline-aware CreateRun and GetRun clients, persistent retry semantics, deterministic retry vectors, and fault-injection evidence for failures before invocation, before commit, after commit, and during response delivery.

## Demonstrate

- [ ] Derive child rpc budgets from one absolute edge deadline.
- [ ] Separate caller cancellation from application rollback.
- [ ] Classify transparent and configured retries without assuming all transient statuses are safe.
- [ ] Bind mutation retries to durable idempotency records and semantic fingerprints.
- [ ] Apply bounded backoff, jitter, attempt limits, and retry throttling.
- [ ] Reconcile ambiguous outcomes when a deadline or connection fails after commit.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/shared/vectors/deadlines.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/shared/vectors/retries.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-05-deadline-proof.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How can callers bound remote work and recover from transient failure without multiplying timeouts or duplicating durable effects?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Deadlines, Cancellation, Retries, and Idempotent Calls** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
