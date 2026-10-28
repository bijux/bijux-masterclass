# Checkpoint — RPC Boundaries, Service Ownership, and Interaction Choice

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/rpc-case/interaction-decisions.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/rpc-case/service-ownership.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-01-boundary-proof.json` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **Which interactions deserve a typed RPC boundary, and which should remain HTTP requests, durable events, or local function calls?**
- [ ] Identify one tempting but incorrect implementation and the failure it causes.
- [ ] State which property is not established by the dependency-light proof.
- [ ] Compare Python and TypeScript boundary behavior without demanding identical internals.

## Non-compensable gate

The boundary proof passes and you can defend one rejection as clearly as one approval.

Record the result in your learning journal before proceeding.
