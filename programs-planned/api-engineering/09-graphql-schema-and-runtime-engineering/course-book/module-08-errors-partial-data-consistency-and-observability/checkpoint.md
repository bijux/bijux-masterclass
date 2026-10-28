# Checkpoint — Module 08: Errors, Partial Data, Consistency, and Observability

## Required result

Return truthful partial data with path-specific errors and traces.

## Demonstrate

- [ ] Separate request and execution errors.
- [ ] Use error paths and stable codes.
- [ ] Predict null bubbling.
- [ ] Disclose staleness and partiality.
- [ ] Trace graph execution without cardinality explosions.

## Commands

```bash
make core-proof
```

## Evidence to retain

Create `reports/module-08-partial-data.json` with source state, data path, returned value class, error code, bubble target, unaffected siblings, consistency metadata, and trace outcome. Include one client decision for each case: render partial, refetch, retry, or stop.

## Defend the design

1. Answer the central question in one paragraph: How does the graph tell the truth when some fields succeed, some fail, and some are stale?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Errors, Partial Data, Consistency, and Observability** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
