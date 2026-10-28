# Checkpoint — Protobuf Modeling, Presence, and Semantic Types

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/shared/vectors/presence.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/shared/vectors/int64.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-02-model-proof.json` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How do we encode domain meaning in Protobuf without allowing language defaults, JSON conventions, or storage models to erase important distinctions?**
- [ ] Identify one tempting but incorrect implementation and the failure it causes.
- [ ] State which property is not established by the dependency-light proof.
- [ ] Compare Python and TypeScript boundary behavior without demanding identical internals.

## Non-compensable gate

No field whose absence changes behavior may lack explicit presence semantics, and no supported TypeScript path may coerce a 64-bit contract value to an unsafe number.

Record the result in your learning journal before proceeding.
