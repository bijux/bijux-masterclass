# Checkpoint — Module 10: Incremental Extraction, Strangler Migration, and Final Architecture Defense

## Required result

Extract Notification Delivery and Artifact Delivery through shadow, compare, backfill, cutover, and decommission phases; retain Analysis Control; and publish the Course 9 graph-access handoff.

## Demonstrate

- [ ] Sequence extraction from low-coupling evidence rather than organizational pressure.
- [ ] Use strangler routing, shadow comparison, and read/write cutover safely.
- [ ] Migrate data without uncontrolled dual writes.
- [ ] Define decommission, rollback, and merge-back criteria.
- [ ] Defend the final architecture against shared-database and distributed-monolith critiques.
- [ ] Publish a sanitized service and query boundary for graphql without bypassing service ownership.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/architecture/extraction-plan.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/final-defense/architecture-summary.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/handoff/` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-10-final-defense.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How do we extract services incrementally, preserve every existing contract, and retain a safe path to stop, roll back, or merge a service back into the platform?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Incremental Extraction, Strangler Migration, and Final Architecture Defense** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
