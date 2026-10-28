# Module 04 — Transactional Publication, Inbox Deduplication, and Exactly-Once Effects

> **Program stage:** Course 6 of 6 — Extend the promise across asynchronous time.

> **Central question:** How do producers avoid dual writes and consumers obtain exactly-once effects on top of at-least-once delivery?

## Where this module fits

Module 03 made the hardest duplicate visible: a consumer commits its effect, crashes before acknowledgement,
and receives the same broker record again. It also exposed the producer-side dual write: domain state can
commit while publication fails, or publication can succeed while the domain transaction rolls back.

Distributed transactions across application databases, brokers, email providers, object stores, and
third-party APIs are usually unavailable or operationally inappropriate. The practical design is to move
each boundary into one local transaction and make the bridge retryable. The producer writes domain state
and an outbox record atomically. A relay repeatedly publishes unsent rows. The consumer records inbox
identity and business effect atomically. Acknowledgement occurs after that local transaction.

This pattern does not create exactly-once delivery. The relay may publish the same outbox row more than once,
and the broker may redeliver. It creates **exactly-once committed effects within a declared effect store**
when deduplication identity, transaction isolation, and side-effect boundaries are correct. External calls
require their own idempotency or another outbox.

## Capstone result

Implement transactional outbox publication, inbox deduplication, effect-version identity, and atomic consumer effects.

Extend the Analysis Events capstone with a producer transaction, outbox relay, consumer inbox, and
projection transaction. Reproduce both critical crash windows:

```text
domain commit → relay publish → relay mark-published
consumer effect commit → broker acknowledgement
```

Demonstrate that one logical run-completion effect is committed even when the message is published or
delivered more than once.

## Learning outcomes

- explain the producer dual-write problem and why ordinary exception handling cannot close it
- design an outbox row with stable event identity, payload bytes, state, attempts, and leasing
- separate broker acceptance from outbox publication completion
- make relay retries safe under crash after broker acceptance
- design an inbox uniqueness key from event and effect identity
- commit inbox state and projection/effect in one local transaction
- distinguish one handler invocation, one message delivery, and one committed business effect
- extend idempotency across external side effects using a downstream key or another outbox

## Core event model

### 1. The producer dual write has two unacceptable orders

If the application commits domain state and then publishes, a crash between those steps loses the
integration event. If it publishes first and then commits, consumers may observe a fact that never became
true. Retrying either sequence cannot infer safely whether the other side completed.

The outbox places publication intent in the same transaction as the authoritative state transition.
Once committed, the fact is durable even if the broker is unavailable. A relay can retry independently
until the broker accepts the record.

The event payload or canonical bytes must be frozen at transaction time. Reconstructing later from a
changed database can publish a different fact under the same event ID.

### 2. An outbox is a state machine, not a boolean flag

A robust row contains event ID, event type, channel, partition key, canonical body, creation time,
status, attempt count, next-attempt time, lease owner/generation, publication metadata, and safe last
error. Rows move through pending, leased, retryable, published, or terminal states.

Multiple relay instances claim rows with database locking or a lease. A stale relay must not mark a row
published after a newer owner has recovered it. Course 2’s worker fencing lessons apply again.

Deleting immediately after publication removes useful audit and reconciliation evidence. Retention and
compaction should be policy-driven.

### 3. Crash after broker acceptance creates duplicate publication

The relay sends a record; the broker persists it; the process crashes before updating the outbox. On
restart, the row is still pending and is published again. This is the unavoidable uncertainty window
unless broker and database share a transaction.

Stable event ID and canonical body make the two records recognizable as one logical event. Consumers
must not assume broker offsets are event identities. A broker-side duplicate window can reduce repeated
records but does not replace consumer idempotency or permanent event identity.

The deterministic relay test intentionally raises after `publish()` and before `mark_published()`.

### 4. Inbox identity belongs to the effect, not merely the process

An inbox records that a logical consumer effect has handled an event. A useful uniqueness key is
`(consumer_name, effect_version, event_id)`. Including effect version allows a deliberately new
projection version to replay history without pretending the old effect row applies.

Keying only by event ID can incorrectly suppress independent consumers. Keying by delivery token fails
because each redelivery has a new token. Keying by broker offset ties identity to one transport and does
not survive republishing or migration.

The inbox may store outcome metadata or the resulting projection revision so repeated handling can
return an auditable “already applied” result.

### 5. Inbox and effect must share a transaction

Writing the inbox first and the projection second can suppress work after a crash: the retry finds the
inbox and skips an effect that never committed. Writing the effect first and inbox second can repeat the
effect after a crash.

The correct local boundary inserts the inbox row and applies the projection in one transaction. A unique
constraint arbitrates concurrent duplicate deliveries. One transaction wins; the other observes the
existing inbox record and does not repeat the effect.

An in-memory set is useful for a semantic laboratory but is not durable evidence. The live PostgreSQL
route proves the same invariant with a unique constraint.

### 6. External side effects remain a second dual write

A consumer transaction cannot include an arbitrary email provider or payment API. If it writes the inbox
and then calls the provider, a crash may lose the call. If it calls first, a crash may repeat it.

Prefer a downstream idempotency key when the provider supports one. Otherwise, commit an outbound-command
outbox in the inbox/effect transaction and let a dispatcher perform the call. The downstream effect then
has its own delivery and idempotency boundary.

“The handler is idempotent” must identify every external side effect; database projection idempotency
alone is not enough.

### 7. Effect identity needs semantic versioning

A projection may change its algorithm. If version 2 intentionally recomputes a different result from the
same event history, it needs a new effect identity or isolated target. Reusing the version 1 inbox would
skip all historical events; deleting the inbox would risk repeating external side effects.

Replay plans declare consumer/effect version and side-effect mode. Projection rebuilds write to a new
table or namespace, validate, then switch readers. Notification or billing effects are normally disabled
during replay.

This makes “idempotent” a versioned business statement rather than a property of a function name.

### 8. Reconciliation closes silent gaps

Outbox status, broker records, inbox rows, and projection state can diverge because of defects or manual
operations. Reconciliation compares durable identities: committed domain fact versus outbox, outbox
versus publication evidence, event versus inbox, inbox versus effect.

Telemetry can locate the gap but is not the source of truth. A repair action uses a stable repair key and
is itself auditable.

Course 4 introduced reconciliation for service state. This module extends the technique across the
asynchronous publication and consumption chain.

## Engineering requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Atomic producer intent | Domain fact and outbox row commit in one database transaction. | Committed state has no publishable fact or a fact is published for rolled-back state. | Transaction test and foreign/unique constraints |
| Frozen event bytes | Outbox stores canonical event content and identity at commit time. | Retry reconstructs a changed event. | Outbox payload digest |
| Safe relay claim | Concurrent relays use locking/lease and stale-owner fencing. | Rows are raced, lost, or marked by stale workers. | Claim and lease proof |
| Duplicate publication tolerated | Same event ID and body may appear more than once. | Crash after broker accept causes repeated effects. | Relay crash test and inbox proof |
| Effect-scoped inbox | Uniqueness includes consumer/effect version and event ID. | Independent effects suppress each other or redelivery bypasses dedupe. | Inbox key schema |
| Atomic consumer effect | Inbox and durable effect share one local transaction. | Crash creates skipped or duplicated effect. | Injected-failure database test |
| External effect boundary | Provider call uses idempotency or an outbound outbox. | Database dedupe hides repeated email/payment calls. | Dispatcher and downstream key evidence |

## Worked failures

### Case 1 — publish after commit was considered reliable

The API commits a completed run, calls the broker, and returns success. During a broker outage, the call
fails and no durable publication intent remains. Add the event outbox row to the completion transaction;
returning success then means the fact and its publication obligation are durable.

### Case 2 — relay marked before publish

To avoid duplicates, the relay sets `published=true` and then sends. A crash after the mark loses the
event permanently. Mark only after broker acceptance and accept that the opposite crash window creates
duplicates.

### Case 3 — inbox was inserted before effect

The consumer commits the inbox row, then updates analytics. A crash between them causes all retries to
skip the missing analytics update. Move both writes into one transaction and let uniqueness arbitrate.

### Case 4 — email was sent inside the projection transaction

The database transaction rolls back after the email provider accepts. Redelivery sends a second email.
Commit a `SendCompletionEmail` outbox row with the inbox/projection transaction and use a stable
downstream idempotency key in the dispatcher.

## Python implementation

The dependency-light Python implementation models the two local transactions:

```text
capstone/tracks/python-fastapi/src/event_engineering/outbox.py
capstone/tracks/python-fastapi/src/event_engineering/inbox.py
capstone/tracks/python-fastapi/tests_event/test_outbox_inbox.py
```

`DomainOutboxStore.commit()` records domain state and an `OutboxRow`. `OutboxRelay.step()` publishes one
pending row and then marks it. The test injects a crash after publish so the same event is published again.

`TransactionalProjection.apply()` uses `(consumer, effect_version, event_id)` as its logical inbox key. The
dependency-light implementation holds state in one critical section; the PostgreSQL migration supplies the
real unique constraint and transaction shape.

The important assertion is not “handler called once.” It is:

```python
assert broker_record_count == 2
assert handler_attempt_count == 2
assert committed_projection_updates == 1
```

## TypeScript implementation

The TypeScript track uses the same logical keys and outcomes:

```text
capstone/tracks/typescript-fastify/src/event-engineering/outbox.ts
capstone/tracks/typescript-fastify/src/event-engineering/inbox.ts
capstone/tracks/typescript-fastify/test-event-core/core.test.mjs
```

It keeps event IDs and database-like counters as strings where precision matters. A `Map` is acceptable for
the deterministic proof, but the course labels it non-durable and separately validates migrations 010–012.

Avoid promise chains that publish outside the owning transaction without recording intent. `await` orders
operations in one process; it does not make two systems atomic.

## Cross-language invariant

Python and TypeScript must agree on canonical event bytes, outbox identity, relay outcomes, inbox keys,
duplicate classification, and projection revision. The same shared vector simulates a crash after publish
and requires two broker records but one committed effect.

Language-specific locking primitives may differ; the database constraint is the final arbitration in a
live deployment.

## Design review

Draw two timelines—producer and consumer—and mark each durable commit. For every arrow crossing systems,
ask whether a retry can repeat it and which stable identity makes repetition safe. Then inspect the
transaction boundaries in code and SQL; folder names do not prove atomicity.

Reject any “exactly once” claim that does not name the effect store, consumer/effect version, and external
side-effect policy.

## End-to-end worked example

The run-completion transaction updates the run, inserts artifact metadata, and writes one outbox row whose
body is the final `AnalysisRunCompleted` envelope. The relay publishes it and crashes before marking the
row. A recovered relay republishes the same event ID and bytes.

`analytics-v1` receives the first record, inserts inbox identity, increments completion counters, and
commits. Its acknowledgement is lost. The second broker record or redelivery reaches the same consumer.
The unique inbox identity reports “already applied,” so the projection remains one increment. The
notification consumer has a different effect identity and is not suppressed.

Notification’s outbound email is represented by a second outbox row, not a direct call inside the analytics
or inbox transaction.

## Failure patterns

- **Direct dual write.** Domain state and broker publication are attempted as independent operations.
- **Mutable reconstruction.** Relay rebuilds payload from current tables instead of publishing committed bytes.
- **Mark-before-send.** Duplicate avoidance is traded for silent message loss.
- **Delivery-token dedupe.** A redelivery receives a new token and repeats the effect.
- **Inbox-before-effect.** A crash permanently suppresses an uncommitted effect.
- **Effect-before-inbox.** A crash repeats a committed effect.
- **One inbox for all consumers.** Independent logical effects suppress each other.
- **External-call blindness.** Database idempotency is assumed to make email or payment calls idempotent.

## Module synthesis

Implement transactional outbox publication, inbox deduplication, effect-version identity, and atomic consumer effects. The central distinction is this: how do producers avoid dual writes and consumers obtain exactly-once effects on top of at-least-once delivery? The checkpoint is complete only when the mechanism, failure, oracle, and evidence limitation can all be explained together.

## Next in the story

Durable publication and one committed effect solve the immediate duplicate windows. They do not guarantee
that an event schema will remain intelligible after producers and consumers evolve independently. Module 05
treats historical events as long-lived public data: compatibility direction, semantic changes, versioning,
upcasting, bounded replay, and release gates.
