# Reference Answers — Module 04: Worked answers — Module 04 — Transactional Publication, Inbox Deduplication, and Exactly-Once Effects

Read after attempting all twelve Transactional Publication, Inbox Deduplication, and Exactly-Once Effects exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Place the outbox transaction

Create the outbox row in the same database transaction that changes the run to completed and commits artifact references. That transaction has enough semantic knowledge to construct the final fact. Writing it in the worker before the authoritative transition or in a later polling job reintroduces uncertainty.

## 2. Enumerate producer crash windows

Before commit: no fact and no outbox. After commit before relay: fact and pending outbox survive; relay publishes later. After broker accept before mark: fact survives and duplicate publication is expected on recovery. After mark: the row is complete and should not republish except by an explicit replay/repair action.

## 3. Design an outbox row

Include event ID, type, source/channel, partition key, canonical bytes or immutable payload, digest, created time, state, attempt count, next-attempt time, lease owner/generation/expiry, published time, broker metadata, and safe failure code. Add uniqueness on event ID and indexes for claimable rows.

## 4. Choose an inbox key

`(consumer, effectVersion, eventId)` is correct. Event ID alone suppresses other consumers; delivery token changes on redelivery; broker offset is transport-specific and can change on republish. The chosen key names the logical effect on one immutable fact.

## 5. Prove one effect

Record broker records, delivery attempts, handler invocations, inbox insert successes/conflicts, and projection revisions. The crash experiment may produce two records and attempts, but exactly one successful inbox insert and one projection revision. A single final value without intermediate counters cannot prove the path.

## 6. Handle concurrent duplicates

Both transactions attempt the same unique inbox key. One inserts and applies the effect, then commits. The other blocks or conflicts, rolls back its attempted effect, reads the existing outcome, and acknowledges without mutation. The effect and inbox must be in the same transaction.

## 7. Protect an email side effect

In one consumer transaction, insert the completion inbox row, update notification state, and insert a `SendCompletionEmail` outbound outbox row with stable command/idempotency ID. Commit, then acknowledge the event. A dispatcher calls the provider using that stable ID and records delivery separately.

## 8. Version an effect

Give v2 an effect identity such as `analytics-completion:v2` and a new projection target. Replay events with side effects disabled into the new target, validate it, then switch readers. Keep v1 inbox and projection until rollback/reconciliation windows close.

## 9. Freeze event bytes

The event represents facts at the original commit. Re-reading after schema or state changes can publish a different payload with the same ID, violating immutability and signature/deduplication assumptions. Store canonical bytes or an immutable versioned payload in the outbox transaction.

## 10. Reconcile a missing inbox

First verify the broker/group acknowledgement evidence and whether it can be stale or misread. Then inspect consumer logs/traces, transaction failures, manual offset changes, and schema/version mismatches. Do not immediately replay with side effects enabled. Use a dry-run repair plan and a stable repair ID.

## 11. Reject distributed-transaction magic

`try/except` controls one process flow but cannot roll back a broker acceptance or email accepted by remote systems when PostgreSQL later fails. Atomicity requires a shared transaction coordinator supported by all parties or, here, local transactions plus durable outboxes and idempotent boundaries.

## 12. State an honest exactly-once claim

“For event profile 1.0, the `analytics-completion:v1` PostgreSQL projection commits at most one update per event ID because inbox identity and projection mutation share one transaction under a unique constraint. Broker records, deliveries, handler attempts, logs, and external notifications may occur more than once.”
