# Worked Answers — Module 04: Transactional Publication, Inbox Deduplication, and Exactly-Once Effects

Use these solutions to audit your reasoning for **Transactional Publication, Inbox Deduplication, and Exactly-Once Effects**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Place the outbox transaction

Create the outbox row in the same database transaction that changes the run to completed and commits artifact references. That transaction has enough semantic knowledge to construct the final fact. Writing it in the worker before the authoritative transition or in a later polling job reintroduces uncertainty.

The chapter’s decisive distinction is this: The run-completion transaction updates the run, inserts artifact metadata, and writes one outbox row whose body is the final AnalysisRunCompleted envelope. The relay publishes it and crashes before marking the row. A recovered relay republishes the same event ID and bytes.

## 2. Enumerate producer crash windows

Before commit: no fact and no outbox. After commit before relay: fact and pending outbox survive; relay publishes later. After broker accept before mark: fact survives and duplicate publication is expected on recovery. After mark: the row is complete and should not republish except by an explicit replay/repair action.

In the cumulative capstone, the rule becomes concrete: To avoid duplicates, the relay sets published=true and then sends. A crash after the mark loses the event permanently. Mark only after broker acceptance and accept that the opposite crash window creates duplicates.

## 3. Design an outbox row

Include event ID, type, source/channel, partition key, canonical bytes or immutable payload, digest, created time, state, attempt count, next-attempt time, lease owner/generation/expiry, published time, broker metadata, and safe failure code. Add uniqueness on event ID and indexes for claimable rows.

A useful way to reason about the boundary is: A robust row contains event ID, event type, channel, partition key, canonical body, creation time, status, attempt count, next-attempt time, lease owner/generation, publication metadata, and safe last error. Rows move through pending, leased, retryable, published, or terminal states.

## 4. Choose an inbox key

`(consumer, effectVersion, eventId)` is correct. Event ID alone suppresses other consumers; delivery token changes on redelivery; broker offset is transport-specific and can change on republish. The chosen key names the logical effect on one immutable fact.

The implementation consequence is: Keying only by event ID can incorrectly suppress independent consumers. Keying by delivery token fails because each redelivery has a new token. Keying by broker offset ties identity to one transport and does not survive republishing or migration.

## 5. Prove one effect

Record broker records, delivery attempts, handler invocations, inbox insert successes/conflicts, and projection revisions. The crash experiment may produce two records and attempts, but exactly one successful inbox insert and one projection revision. A single final value without intermediate counters cannot prove the path.

The important nuance is: analytics-v1 receives the first record, inserts inbox identity, increments completion counters, and commits. Its acknowledgement is lost. The second broker record or redelivery reaches the same consumer. The unique inbox identity reports “already applied,” so the projection remains one increment. The notification consumer has a different effect identity and is not suppressed.

## 6. Handle concurrent duplicates

Both transactions attempt the same unique inbox key. One inserts and applies the effect, then commits. The other blocks or conflicts, rolls back its attempted effect, reads the existing outcome, and acknowledges without mutation. The effect and inbox must be in the same transaction.

Under concurrency or failure, the distinction becomes: The correct local boundary inserts the inbox row and applies the projection in one transaction. A unique constraint arbitrates concurrent duplicate deliveries. One transaction wins; the other observes the existing inbox record and does not repeat the effect.

## 7. Protect an email side effect

In one consumer transaction, insert the completion inbox row, update notification state, and insert a `SendCompletionEmail` outbound outbox row with stable command/idempotency ID. Commit, then acknowledge the event. A dispatcher calls the provider using that stable ID and records delivery separately.

The design remains honest only if: The database transaction rolls back after the email provider accepts. Redelivery sends a second email. Commit a SendCompletionEmail outbox row with the inbox/projection transaction and use a stable downstream idempotency key in the dispatcher.

## 8. Version an effect

Give v2 an effect identity such as `analytics-completion:v2` and a new projection target. Replay events with side effects disabled into the new target, validate it, then switch readers. Keep v1 inbox and projection until rollback/reconciliation windows close.

The consumer-facing consequence is: A projection may change its algorithm. If version 2 intentionally recomputes a different result from the same event history, it needs a new effect identity or isolated target. Reusing the version 1 inbox would skip all historical events; deleting the inbox would risk repeating external side effects.

## 9. Freeze event bytes

The event represents facts at the original commit. Re-reading after schema or state changes can publish a different payload with the same ID, violating immutability and signature/deduplication assumptions. Store canonical bytes or an immutable versioned payload in the outbox transaction.

The operational consequence is: Python and TypeScript must agree on canonical event bytes, outbox identity, relay outcomes, inbox keys, duplicate classification, and projection revision. The same shared vector simulates a crash after publish and requires two broker records but one committed effect.

## 10. Reconcile a missing inbox

First verify the broker/group acknowledgement evidence and whether it can be stale or misread. Then inspect consumer logs/traces, transaction failures, manual offset changes, and schema/version mismatches. Do not immediately replay with side effects enabled. Use a dry-run repair plan and a stable repair ID.

The strongest engineering interpretation is: An inbox records that a logical consumer effect has handled an event. A useful uniqueness key is (consumer name, effect version, event id). Including effect version allows a deliberately new projection version to replay history without pretending the old effect row applies.

## 11. Reject distributed-transaction magic

`try/except` controls one process flow but cannot roll back a broker acceptance or email accepted by remote systems when PostgreSQL later fails. Atomicity requires a shared transaction coordinator supported by all parties or, here, local transactions plus durable outboxes and idempotent boundaries.

The defect-oriented view is: Draw two timelines—producer and consumer—and mark each durable commit. For every arrow crossing systems, ask whether a retry can repeat it and which stable identity makes repetition safe. Then inspect the transaction boundaries in code and SQL; folder names do not prove atomicity.

## 12. State an honest exactly-once claim

“For event profile 1.0, the `analytics-completion:v1` PostgreSQL projection commits at most one update per event ID because inbox identity and projection mutation share one transaction under a unique constraint. Broker records, deliveries, handler attempts, logs, and external notifications may occur more than once.”

Across the Python and TypeScript tracks, the invariant is: TransactionalProjection.apply() uses (consumer, effect version, event id) as its logical inbox key. The dependency-light implementation holds state in one critical section; the PostgreSQL migration supplies the real unique constraint and transaction shape.
