# Checkpoint — Module 04: Transactions, Concurrency, ETags, and Idempotency

## Required result

One hundred concurrent identical submissions create one run; stale ETags fail atomically; replay survives restart.

## Demonstrate

- Draw the transaction boundary for each use case.
- Implement compare-and-swap for `If-Match`.
- Persist idempotency scope, fingerprint, and response.
- Handle simultaneous duplicate requests with one logical winner.
- Prove rollback leaves no partial state.

## Commands

```bash
make predecessor-proof
make operation-proof
make module-proof MODULE=04 TRACK=python
make module-proof MODULE=04 TRACK=typescript
make core-proof
```

## Defend the design

1. Answer the central question: **How do public guarantees survive simultaneous requests, retries, lost responses, and process restart?**
2. Demonstrate this capstone result: One hundred concurrent identical submissions create one run; stale ETags fail atomically; replay survives restart.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: one key and fingerprint produce one durable outcome, while a stale version fails atomically.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—One hundred concurrent identical submissions create one run; stale ETags fail atomically; replay survives restart.—all focused checks pass, the **Transactions, Concurrency, ETags, and Idempotency** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
