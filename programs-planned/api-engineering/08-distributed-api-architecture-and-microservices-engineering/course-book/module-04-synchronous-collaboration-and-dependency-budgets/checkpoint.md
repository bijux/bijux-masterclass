# Checkpoint — Module 04: Synchronous Collaboration, API Composition, and Dependency Budgets

## Required result

Publish an acyclic synchronous dependency graph, one edge-owned deadline budget, bounded fan-out rules, and a gateway composition path that degrades truthfully.

## Demonstrate

- [ ] Model the complete synchronous dependency graph and detect cycles.
- [ ] Calculate compounded latency and availability across serial and parallel calls.
- [ ] Propagate one absolute deadline instead of multiplying independent timeouts.
- [ ] Place retries, hedging, and circuit behavior at one accountable layer.
- [ ] Design api composition without chatty per-row remote calls.
- [ ] Separate unavailable, stale, partial, and authoritative responses explicitly.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/architecture/dependency-graph.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-04-dependency-proof.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-04-partial-response.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How do we keep synchronous service collaboration bounded so that fan-out, retries, and version skew do not make the public request path fragile?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Synchronous Collaboration, API Composition, and Dependency Budgets** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
