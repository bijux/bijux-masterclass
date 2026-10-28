# Module 03 — Delivery Semantics, Ordering, Partitioning, and Acknowledgement

> **Program stage:** Course 6 of 6 — Extend the promise across asynchronous time.

> **Central question:** What do acknowledgement, redelivery, ordering, partitioning, lag, and consumer groups actually guarantee?

## Where this module fits

A contract can state which messages exist, but it does not make delivery reliable. The moment a producer and
consumer are separated by a broker, several independent states exist: the producer’s durable state, the
broker’s accepted record, the consumer’s in-flight delivery, the consumer’s durable effect, and the
acknowledgement position. Failure can occur between any two of them.

Marketing phrases such as “exactly once,” “ordered queue,” or “durable messaging” are dangerous unless the
scope is explicit. A broker may store one record once and still deliver it several times. It may preserve
order within one partition while interleaving records across partitions. An acknowledgement may be lost
after a consumer committed its effect. A consumer group can share work without providing global sequence.

This module uses a deterministic broker before a live broker so every failure window can be reproduced.
The model is deliberately small: channels contain partitioned append-only records; groups maintain next
offsets; one record per partition may be in flight; acknowledgement advances; negative acknowledgement
delays redelivery; acknowledgement expiry redelivers; termination skips a poison record under explicit
policy. The purpose is semantic clarity, not a toy replacement for NATS.

## Capstone result

Implement deterministic delivery attempts, partition order, group independence, acknowledgement expiry, negative acknowledgement, and redelivery.

Implement and prove the Analysis Events delivery profile using:

```text
capstone/tracks/python-fastapi/src/event_engineering/broker.py
capstone/tracks/typescript-fastify/src/event-engineering/broker.ts
capstone/event-case/channel-policy.yaml
capstone/shared/vectors/delivery.json
capstone/broker/nats/
```

The deterministic profile establishes per-partition ordering, explicit acknowledgement, bounded redelivery,
and group-local progress. An optional NATS JetStream route maps the same semantics to a live transport.

## Learning outcomes

- distinguish storage, publication, delivery, processing, effect, and acknowledgement
- state at-most-once and at-least-once semantics without hiding loss or duplication
- explain why broker-level exactly-once does not automatically create exactly-once business effects
- choose a partition key from the smallest domain requiring order
- reason about per-partition ordering and cross-partition interleaving
- model consumer groups, offsets, in-flight records, acknowledgement deadlines, and redelivery
- bound retry and distinguish negative acknowledgement from terminal rejection
- measure lag as both record count and age rather than one misleading number

## Core event model

### 1. Delivery has several commit points

The producer first changes domain state. It then records or publishes a message. The broker accepts and
persists a record. A consumer receives a delivery. The handler may commit a database effect. Finally,
the consumer acknowledges the delivery and the group advances.

A crash after receive but before effect should redeliver. A crash after effect but before acknowledgement
also redelivers, even though the business work already happened. Acknowledging before the effect avoids
duplication but permits loss. No acknowledgement order eliminates both hazards without a transactional
relationship between the effect store and delivery position.

The course therefore treats at-least-once delivery plus idempotent effect as the default. Module 04
supplies the transactional inbox boundary that makes the repeated delivery harmless.

### 2. At-most-once and at-least-once are trade-offs, not quality ranks

At-most-once processing can be implemented by advancing or acknowledging before work. It avoids
redelivery but loses work when the handler crashes afterward. This may be acceptable for disposable
telemetry, not for authoritative artifact publication.

At-least-once processing keeps the message eligible until work is acknowledged. It protects against
loss but creates duplicates. The consumer must define a stable effect identity and store deduplication
state durably.

A design document must say which layer the phrase applies to: broker record, delivery attempt, handler
invocation, or business effect. “Exactly once” without a noun and boundary is not an engineering claim.

### 3. Ordering exists only inside an explicit domain

Most scalable brokers partition a stream. Records sharing a partition have a stable order; records in
different partitions can be processed concurrently and observed in either order. A global sequence
would force all work through one serialized path and often creates unnecessary coupling.

The partition key should be the smallest identity whose events require order. Run lifecycle events use
run ID because `requested → started → completed` must be ordered for one run. Partitioning by tenant
would serialize unrelated runs and create hot tenants. Partitioning by random event ID would destroy
run order.

Even within a partition, order of delivery does not prove order of effects if a consumer starts
concurrent asynchronous work and acknowledges out of order. The handler concurrency model must respect
the ordering promise.

### 4. Consumer groups create independent progress

A consumer group represents one logical subscription and effect. Multiple instances in the same group
share partitions for scale and failover. Different groups independently consume the same records.
Notification, analytics, and audit use separate groups because each owns a different effect.

Duplicating a group name across unrelated effects is a serious bug: the consumers would divide records
instead of each receiving all of them. Creating a new group without a start policy can replay an entire
retained stream unexpectedly.

Group identity, start position, acknowledgement policy, maximum delivery attempts, and retention
interaction are release-controlled configuration, not anonymous runtime defaults.

### 5. Acknowledgement is a protocol decision

An explicit acknowledgement says that the consumer has completed the effect required for this delivery
and may advance. A negative acknowledgement says the attempt failed transiently and should become
eligible after a delay. Letting the acknowledgement deadline expire models a crashed or hung consumer.
Terminal rejection says repeated delivery will not make the record processable under the current policy.

The deterministic broker issues an opaque delivery token. A token may be settled once. This prevents a
stale handler from acknowledging a newer delivery attempt accidentally.

The acknowledgement deadline must exceed expected handler time but remain short enough for useful
recovery. Long-running work should renew a lease or split acceptance from completion rather than set an
unbounded deadline.

### 6. Redelivery delay and attempt count are part of overload behavior

Immediate retry can create a tight loop that consumes a partition, database pool, or external quota.
Exponential backoff with jitter is useful for shared transient dependencies; deterministic tests inject
a delay function so the outcome is reproducible.

Attempt counts must be scoped to a group and record position. A new delivery token does not reset the
attempt history. When the maximum is reached, the consumer records a dead letter with safe failure
metadata and terminates or parks the record under policy.

Retrying forever is not reliability. It converts one poison record into permanent lag and resource
consumption.

### 7. Retention, acknowledgement, and replay solve different problems

Acknowledgement advances one consumer group. It does not delete the broker record immediately when
retention allows replay for other groups. Retention decides how long records remain available.
Replay deliberately creates or resets a consumption path to reapply historical facts.

A short retention period can make recovery impossible even if consumers use explicit acknowledgement.
Infinite retention creates privacy, storage, and schema-understanding obligations. Each channel needs a
retention rationale connected to replay and audit requirements.

Progress events may have shorter retention than terminal completion facts. The policy is based on
consumer recovery needs, not on one global broker default.

### 8. Lag requires count and age

Lag count is the number of records not yet acknowledged by a group. Oldest-message age measures how long
the oldest pending fact has waited. A low count can still be critical if one event has been stuck for
hours. A high count may be acceptable during a brief known burst if age remains within the service
objective and drain capacity is sufficient.

The course classifies lag with both dimensions and records channel, group, partition, and consumer
version. High-cardinality event IDs do not belong in metrics; they belong in logs or traces.

Lag is evidence about delivery progress, not proof that business effects are correct. Durable projection
counts and reconciliation remain separate oracles.

## Engineering requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Explicit semantic level | Every delivery claim names broker record, attempt, handler invocation, or business effect. | Exactly-once language hides duplicates or loss. | Failure-window table |
| Partition rationale | Partition key matches the smallest domain requiring order. | Unrelated work serializes or required order disappears. | Catalogue and partition vectors |
| One in-flight per ordered partition | The teaching profile prevents out-of-order effects inside one partition. | Concurrent handlers violate lifecycle order. | Broker state and tests |
| Settle once | Ack, nack, or terminate consumes one opaque delivery token. | Stale or duplicate settlement corrupts group progress. | Token-state tests |
| Bounded redelivery | Retries have delays, maximum attempts, and terminal policy. | Poison records retry forever. | Attempt history and dead-letter proof |
| Independent groups | Each logical effect owns a stable group and start policy. | Consumers steal records from unrelated effects. | Consumer catalogue |
| Lag by count and age | Operational health evaluates both dimensions. | A single old blocked record looks healthy. | Lag vectors and alerts |

## Worked failures

### Case 1 — acknowledge before commit

The notification consumer acknowledges, then writes its delivery record. A process crash between those
steps permanently loses the notification. Move acknowledgement after the durable effect or use a
transactionally coupled inbox/effect boundary.

### Case 2 — global ordering was assumed

Two runs use different partition keys. `run-B completed` is observed before `run-A started`, and a
dashboard labels the stream corrupt. There was no cross-run ordering promise. The projection must order
within each subject or use event time and explicit aggregation semantics.

### Case 3 — group names were shared

Audit and notification instances both join `analysis-consumers`. Each receives only some completion
events, so neither effect is complete. Give each logical effect its own group; replicas of the same
effect share a group.

### Case 4 — poison event blocked a partition

A schema-invalid record is negatively acknowledged immediately forever. It monopolizes the head of the
ordered partition. Validate before handler dispatch, classify the failure as permanent after bounded
attempts, record a dead letter, and advance under an approved runbook.

## Python implementation

The deterministic Python broker is an executable state machine.

```text
capstone/tracks/python-fastapi/src/event_engineering/broker.py
capstone/tracks/python-fastapi/tests_event/test_broker_delivery.py
```

A channel contains fixed partitions. `publish()` hashes the declared partition key, appends an immutable
record, and assigns a partition-local offset. `poll()` creates deliveries for eligible group positions.
`ack()`, `nack()`, and `term()` settle one token.

```python
broker.create_channel("analysis.events", partitions=4)
record = broker.publish("analysis.events", event.partitionkey, event)
[delivery] = broker.poll("analytics-v1", "analysis.events", ack_wait=timedelta(seconds=10))
broker.ack(delivery.token)
```

Inject a controllable clock. Advance it beyond `deadline` to reproduce redelivery without sleeping. The
second delivery has the same record identity and a higher attempt number but a new token.

## TypeScript implementation

The TypeScript broker preserves integer offsets safely and keeps per-group state separate.

```text
capstone/tracks/typescript-fastify/src/event-engineering/broker.ts
capstone/tracks/typescript-fastify/test-event-core/delivery.test.mjs
```

The code does not use `setTimeout` to prove redelivery. Tests provide a deterministic clock and call `poll`
after advancing it. This avoids flaky timing assertions.

Partition hashing and event canonicalization use shared vectors. The TypeScript implementation may use maps
and readonly objects rather than Python dataclasses; observable delivery order, attempt count, settlement,
and lag must match.

## Cross-language invariant

For identical records, channels, group operations, and clock advances, both tracks must produce the same
partition, offset sequence, delivery eligibility, attempt count, and terminal group position. Delivery
tokens may differ because they are opaque attempt identities.

`capstone/shared/vectors/delivery.json` specifies the semantic trace. A live NATS route is comparative
evidence; the deterministic trace is the repeatable course oracle.

## Design review

Review delivery semantics by drawing the state transitions:

```text
available → in-flight → acknowledged
                   ↘ negative-acknowledged → delayed → available
                   ↘ deadline-expired → available
                   ↘ terminated → advanced/dead-lettered
```

Then mark every crash point between receive, validation, effect commit, and acknowledgement. If the design
cannot say what happens at each point, its reliability claim is incomplete.

## End-to-end worked example

`AnalysisRunCompleted` at partition 2 offset 41 is delivered to `notification-v1`. The consumer writes a
notification row but crashes before acknowledgement. The deadline expires. The broker delivers the same
record at attempt 2 with a new token.

Without an inbox, a second notification may be created. With the Module 04 transaction, the event ID already
exists in the inbox; the consumer returns the stored effect result and acknowledges. Analytics and audit
groups have independent offsets and are unaffected by notification’s crash.

Another run can progress in another partition while partition 2 waits, but later events for the same run
remain behind offset 41. This is the deliberate ordering domain.

## Failure patterns

- **Exactly-once slogan.** A transport feature is treated as a complete business-effect guarantee.
- **Ack before effect.** Loss is traded for lower duplicate risk without acknowledging the trade-off.
- **Random partition key.** Required lifecycle order is destroyed.
- **Overbroad partition key.** An entire tenant or event type becomes a hot serialized partition.
- **Shared group identity.** Independent effects split records instead of each observing them.
- **Unbounded retry.** One poison record consumes a partition indefinitely.
- **Count-only lag.** Old blocked work is hidden by a small queue.

## Module synthesis

Implement deterministic delivery attempts, partition order, group independence, acknowledgement expiry, negative acknowledgement, and redelivery. The central distinction is this: what do acknowledgement, redelivery, ordering, partitioning, lag, and consumer groups actually guarantee? The checkpoint is complete only when the mechanism, failure, oracle, and evidence limitation can all be explained together.

## Next in the story

At-least-once delivery deliberately creates the crash-after-effect duplicate. Module 04 addresses that
failure window with transactional publication on the producer side and transactional inbox/effect
processing on the consumer side. The goal is not exactly-once delivery; it is one committed business
effect despite repeated delivery.
