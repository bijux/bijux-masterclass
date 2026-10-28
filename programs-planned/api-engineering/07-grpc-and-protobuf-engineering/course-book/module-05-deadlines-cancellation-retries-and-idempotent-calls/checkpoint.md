# Checkpoint — Deadlines, Cancellation, Retries, and Idempotent Calls

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/shared/vectors/deadlines.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/shared/vectors/retries.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-05-deadline-proof.json` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How can callers bound remote work and recover from transient failure without multiplying timeouts or duplicating durable effects?**
- [ ] Identify one tempting but incorrect implementation and the failure it causes.
- [ ] State which property is not established by the dependency-light proof.
- [ ] Compare Python and TypeScript boundary behavior without demanding identical internals.

## Non-compensable gate

Every retryable mutation must be durably idempotent, every call must be bounded by one absolute deadline, and every ambiguous outcome must have an authoritative reconciliation path.

Record the result in your learning journal before proceeding.
