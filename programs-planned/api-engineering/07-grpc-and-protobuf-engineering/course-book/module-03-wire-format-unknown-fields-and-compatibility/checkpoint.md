# Checkpoint — Module 03: Wire Format, Unknown Fields, and Compatibility Discipline

## Required result

Publish Analysis RPC compatibility policy 1.0, golden wire fixtures, and a release report that accepts one additive candidate while rejecting unsafe tag, enum, and method-shape changes.

## Demonstrate

- [ ] Explain how field numbers and wire types determine binary compatibility.
- [ ] Reserve removed field numbers and names and reject reuse.
- [ ] Classify changes across wire, source, json, and behavioral dimensions.
- [ ] Reason about unknown-field preservation and loss in proxies, stores, and language runtimes.
- [ ] Evaluate enum, oneof, map, service, method, and streaming-shape changes.
- [ ] Combine local semantic checks, golden bytes, generated-client builds, and buf compatibility evidence.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/releases/rpc-1.1/compatibility-report.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/shared/golden/analysis-run-v1.bin` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-03-wire-proof.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How can an RPC contract evolve without corrupting old data, breaking generated clients, or creating behavior that is wire-readable but operationally unsafe?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Wire Format, Unknown Fields, and Compatibility Discipline** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
