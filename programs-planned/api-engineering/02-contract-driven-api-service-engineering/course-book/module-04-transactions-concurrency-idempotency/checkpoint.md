# Checkpoint — Module 04: Transactions, Concurrency, ETags, and Idempotency

## Required result

Implement persistent request fingerprints, replayed outcomes, version columns, ETags, and transaction rollback.

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

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Transactions, Concurrency, ETags, and Idempotency** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Transactions, Concurrency, ETags, and Idempotency**
- focused result for: Draw the transaction boundary for each use case.
- public, durable, security, or operational observation showing: One hundred concurrent identical submissions create one run; stale ETags fail atomically; replay survives restart.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **transactional idempotency and conditional mutation**
- a limitation statement naming every live dependency required to support the strongest **Transactions, Concurrency, ETags, and Idempotency** claim but not exercised

## Defend the design

1. Answer the central question: **How do public guarantees survive simultaneous requests, retries, lost responses, and process restart?**
2. Demonstrate this capstone result: One hundred concurrent identical submissions create one run; stale ETags fail atomically; replay survives restart.
3. Show the **Transactions, Concurrency, ETags, and Idempotency** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: one key and fingerprint produce one durable outcome, while a stale version fails atomically.
5. State which environment-backed **Transactions, Concurrency, ETags, and Idempotency** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—One hundred concurrent identical submissions create one run; stale ETags fail atomically; replay survives restart.—all focused checks pass, the **Transactions, Concurrency, ETags, and Idempotency** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
