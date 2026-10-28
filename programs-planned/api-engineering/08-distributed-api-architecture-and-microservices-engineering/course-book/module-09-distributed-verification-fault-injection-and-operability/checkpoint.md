# Checkpoint — Distributed Verification, Fault Injection, and Operability

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/planted-defects/` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-09-distributed-proof.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-09-fault-plan.yaml` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How do we prove system behavior when individual services pass their tests but network partitions, version skew, and cross-service timing still create failures?**
- [ ] Identify one tempting but rejected design and the failure it creates.
- [ ] State what the dependency-light proof does not establish.
- [ ] Compare Python and TypeScript behavior without demanding identical internals.

## Non-compensable gate

Ten defects are rejected and the post-clean baseline plus reconciliation proof passes.
