# Checkpoint — Module 07: Demand Control, Persisted Operations, and Caching

## Required result

Admit only bounded trusted operations and record cost evidence.

## Demonstrate

- [ ] Separate validity from affordability.
- [ ] Analyze aliases, fragments, and lists.
- [ ] Operate a trusted-document registry.
- [ ] Design authorization-aware caching.
- [ ] Reject overload truthfully.

## Commands

```bash
make core-proof
```

## Evidence to retain

Create `reports/module-07-demand.json` with case, last phase, expanded occurrences, depth, aliases, cardinality estimate, cost, service set, registry outcome, cache identity, and source calls. Do not store raw untrusted documents in production-shaped telemetry; attach them only to local lab evidence.

## Defend the design

1. Answer the central question in one paragraph: How can a client-shaped query language remain bounded under adversarial and accidental demand?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Demand Control, Persisted Operations, and Caching** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
