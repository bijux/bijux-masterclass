# Checkpoint — Module 09: Distributed Verification, Fault Injection, and Operability

## Required result

Build a distributed proof ladder spanning contract, component, topology, fault, reconciliation, and operator evidence, then use it to reject ten planted architecture defects.

## Demonstrate

- [ ] Separate service unit tests, contract tests, topology tests, and end-to-end outcome proofs.
- [ ] Test failure timing before invocation, after commit, during delivery, and during recovery.
- [ ] Use traces and durable state together rather than treating telemetry as authority.
- [ ] Design bounded fault injection with abort and cleanup conditions.
- [ ] Verify dependency graphs, ownership, and version matrices mechanically.
- [ ] Diagnose distributed incidents from one critical journey without requiring omniscient logs.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/planted-defects/` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-09-distributed-proof.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-09-fault-plan.yaml` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How do we prove system behavior when individual services pass their tests but network partitions, version skew, and cross-service timing still create failures?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Distributed Verification, Fault Injection, and Operability** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
