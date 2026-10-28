# Checkpoint — Module 03: Data Ownership, Replication, and Cross-Service Query Design

## Required result

Split authoritative data ownership, build versioned projections for cross-service reads, define staleness budgets, and prove reconciliation for missing, duplicate, and out-of-order updates.

## Demonstrate

- [ ] Enforce one authoritative writer for each business fact.
- [ ] Distinguish owned data, replicated views, caches, and derived analytics.
- [ ] Design event-fed projections with version and gap handling.
- [ ] Choose api composition, local read models, or asynchronous reports from latency and consistency needs.
- [ ] State staleness and monotonicity guarantees in contracts and user experience.
- [ ] Reconcile orphaned, missing, and divergent records without bypassing service ownership.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/architecture/consistency-policy.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/database/` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-03-data-proof.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How can each service own its writes while the system still answers cross-capability questions without shared tables or hidden distributed transactions?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Data Ownership, Replication, and Cross-Service Query Design** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
