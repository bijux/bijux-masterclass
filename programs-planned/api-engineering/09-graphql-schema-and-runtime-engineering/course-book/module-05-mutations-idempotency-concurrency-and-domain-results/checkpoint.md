# Checkpoint — Module 05: Mutations, Idempotency, Concurrency, and Domain Results

## Required result

Expose idempotent create/start/cancel mutations over owning services.

## Demonstrate

- [ ] Distinguish mutation serialization from transactionality.
- [ ] Design input and payload types.
- [ ] Preserve source idempotency.
- [ ] Delegate optimistic concurrency.
- [ ] Model domain results separately from execution errors.

## Commands

```bash
make core-proof
```

## Evidence to retain

Create `reports/module-05-mutations.json` with hashed command key, semantic input digest, source-call outcome, run identity, replay flag, version transitions, result union member, and gateway persistence inspection. Do not store the raw key.

## Defend the design

1. Answer the central question in one paragraph: How do graph mutations preserve the durable command guarantees of the owning service?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Mutations, Idempotency, Concurrency, and Domain Results** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
