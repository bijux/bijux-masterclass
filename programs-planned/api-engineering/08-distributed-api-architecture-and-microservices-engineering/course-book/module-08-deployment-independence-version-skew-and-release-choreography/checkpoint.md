# Checkpoint — Deployment Independence, Version Skew, and Release Choreography

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/architecture/release-policy.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/architecture/version-ledger.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-08-release-proof.json` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How can services release independently while old and new clients, events, schemas, and database migrations coexist safely?**
- [ ] Identify one tempting but rejected design and the failure it creates.
- [ ] State what the dependency-light proof does not establish.
- [ ] Compare Python and TypeScript behavior without demanding identical internals.

## Non-compensable gate

Release proof passes accepted skew and rejects all incompatible candidates with exact reasons.
