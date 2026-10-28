# Reference Answers — Module 04: Transactions, Concurrency, ETags, and Idempotency

Read after attempting all twelve Transactions, Concurrency, ETags, and Idempotency exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why is an in-process mutex insufficient for idempotency?

It coordinates only one process and disappears on restart. The durable unique key must arbitrate across all instances.

## 2. What belongs in the idempotency scope?

At least authenticated owner/principal, stable operation identifier, and client key; the request fingerprint binds content.

## 3. Why store the original response instead of only the run ID?

The response may include the accepted lifecycle snapshot and headers that differ from current state. Replay promises the original logical outcome, not a fresh GET.

## 4. Which headers should be replayed?

Stable operation headers such as `Location` and an explicit replay marker. Volatile transport headers such as `Date`, connection, and request correlation should be regenerated or excluded.

## 5. How can canonical JSON avoid object-key-order differences?

Recursively sort object keys, preserve array order, use a defined number/string encoding, and hash a structure that includes operation and principal.

## 6. What does zero rows from conditional UPDATE mean?

Either resource is absent/foreign or expected version is stale. A follow-up ownership-concealed existence check distinguishes the documented outcomes without exposing foreign state.

## 7. Why not send a webhook before commit?

The database could roll back after the receiver accepts, creating an event for state that never became durable.

## 8. When is transaction retry safe?

When the closure’s inputs are stable, all effects are transactional or pure, retry count is bounded, and no irreversible effect escaped.

## 9. How do you test rollback at every statement boundary?

Inject a controlled exception after each mutation in turn, then assert all participating table counts and invariants are unchanged.

## 10. Why can `SERIALIZABLE` not replace correct unique constraints?

Isolation can detect anomalies but does not define business identity; a unique constraint directly represents the one-record invariant and remains necessary.

## 11. Trace transactional idempotency and conditional mutation in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/postgres.py` and `capstone/tracks/typescript-fastify/src/repository.ts`. The required invariant is that one key and fingerprint produce one durable outcome, while a stale version fails atomically.

## 12. Compare transactional idempotency and conditional mutation across Python and TypeScript

Both tracks must preserve this invariant: one key and fingerprint produce one durable outcome, while a stale version fails atomically. The intentional difference is that context-manager transactions and promise-scoped clients differ without changing the commit boundary.
