# Checkpoint — Module 05: Distributed Workflows, Sagas, Compensation, and Process Managers

## Required result

Implement the artifact-publication and run-completion saga with durable step identity, semantic locks, compensation, timeout handling, and operator-visible reconciliation.

## Demonstrate

- [ ] Distinguish local acid transactions from distributed workflow guarantees.
- [ ] Choose orchestration or choreography from ownership and visibility needs.
- [ ] Design idempotent saga steps and stable command identities.
- [ ] Write compensations that restore business meaning rather than pretend to erase history.
- [ ] Handle timeout, duplicate, reordering, and crash recovery in process managers.
- [ ] Identify workflows that should be redesigned instead of wrapped in a saga.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/architecture/saga-catalog.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-05-saga-proof.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-05-reconciliation.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How do we preserve business intent when one workflow crosses services that cannot share a transaction?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Distributed Workflows, Sagas, Compensation, and Process Managers** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
