# Checkpoint — Unary RPCs, Metadata, Status, and Rich Errors

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/shared/vectors/status.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-04-unary-proof.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/rpc-case/status-policy.yaml` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How should a unary RPC expose success and failure so that generated clients receive stable application meaning rather than transport accidents or leaked internals?**
- [ ] Identify one tempting but incorrect implementation and the failure it causes.
- [ ] State which property is not established by the dependency-light proof.
- [ ] Compare Python and TypeScript boundary behavior without demanding identical internals.

## Non-compensable gate

Every expected application outcome must have one safe status mapping, and ambiguous committed outcomes must be reconcilable without duplicate effects.

Record the result in your learning journal before proceeding.
