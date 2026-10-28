# Checkpoint — Streaming RPCs, Flow Control, and Backpressure

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/shared/vectors/streaming.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/shared/vectors/flow-control.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-06-streaming-proof.json` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How do we design long-lived and bulk-transfer RPCs so that slow peers, reconnects, oversized messages, and stale attempts cannot exhaust memory or corrupt state?**
- [ ] Identify one tempting but incorrect implementation and the failure it causes.
- [ ] State which property is not established by the dependency-light proof.
- [ ] Compare Python and TypeScript boundary behavior without demanding identical internals.

## Non-compensable gate

No stream may have an unbounded queue, byte count, lifetime, or authority path; durable state and integrity checks must remain correct under reconnect and cancellation.

Record the result in your learning journal before proceeding.
