# Checkpoint — Wire Format, Unknown Fields, and Compatibility Discipline

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/releases/rpc-1.1/compatibility-report.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/shared/golden/analysis-run-v1.bin` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-03-wire-proof.json` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How can an RPC contract evolve without corrupting old data, breaking generated clients, or creating behavior that is wire-readable but operationally unsafe?**
- [ ] Identify one tempting but incorrect implementation and the failure it causes.
- [ ] State which property is not established by the dependency-light proof.
- [ ] Compare Python and TypeScript boundary behavior without demanding identical internals.

## Non-compensable gate

No release may be labeled compatible without separate wire, source, ProtoJSON, behavioral, and consumer evidence.

Record the result in your learning journal before proceeding.
