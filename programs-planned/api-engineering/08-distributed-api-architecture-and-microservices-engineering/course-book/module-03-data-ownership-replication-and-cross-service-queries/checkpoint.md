# Checkpoint — Data Ownership, Replication, and Cross-Service Query Design

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/architecture/consistency-policy.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/database/` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-03-data-proof.json` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How can each service own its writes while the system still answers cross-capability questions without shared tables or hidden distributed transactions?**
- [ ] Identify one tempting but rejected design and the failure it creates.
- [ ] State what the dependency-light proof does not establish.
- [ ] Compare Python and TypeScript behavior without demanding identical internals.

## Non-compensable gate

Data and reconciliation proofs pass with no hidden shared-table access.
