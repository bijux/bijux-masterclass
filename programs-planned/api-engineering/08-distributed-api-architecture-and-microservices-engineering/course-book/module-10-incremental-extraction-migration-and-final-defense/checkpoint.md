# Checkpoint — Incremental Extraction, Strangler Migration, and Final Architecture Defense

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/architecture/extraction-plan.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/final-defense/architecture-summary.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/handoff/` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-10-final-defense.json` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How do we extract services incrementally, preserve every existing contract, and retain a safe path to stop, roll back, or merge a service back into the platform?**
- [ ] Identify one tempting but rejected design and the failure it creates.
- [ ] State what the dependency-light proof does not establish.
- [ ] Compare Python and TypeScript behavior without demanding identical internals.

## Non-compensable gate

Final defense and handoff proofs pass, with zero shared writers, zero sync cycles, and zero unexplained reconciliation findings.
