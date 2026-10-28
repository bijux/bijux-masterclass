# Checkpoint — Distributed Workflows, Sagas, Compensation, and Process Managers

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/architecture/saga-catalog.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-05-saga-proof.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-05-reconciliation.json` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How do we preserve business intent when one workflow crosses services that cannot share a transaction?**
- [ ] Identify one tempting but rejected design and the failure it creates.
- [ ] State what the dependency-light proof does not establish.
- [ ] Compare Python and TypeScript behavior without demanding identical internals.

## Non-compensable gate

Saga proof passes every shared schedule and reconciliation has zero unexplained findings.
