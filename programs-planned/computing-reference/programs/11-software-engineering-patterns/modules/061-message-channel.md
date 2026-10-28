---
module_id: SEPAT-061
program: Software Engineering: Patterns
level: 2
module_number: 61
title: Message Channel
status: complete
last_verified: 2026-08-29
---

# Message Channel

## One-Page Review

### Governing question

How can independently executing components exchange messages through a channel whose addressing, delivery, ordering, durability, capacity, security, schema, lifecycle, and operational semantics are explicit under delay, duplication, loss, crash, partition, and overload?

### Essential definitions

- A **message** is an immutable transmission unit with identity, type/schema, payload, metadata, and provenance.
- A **Message Channel** is a logical path by which a sender publishes messages for one or more receivers without direct invocation.
- A **point-to-point channel** assigns each message to at most one competing consumer attempt at a time; redelivery may create later attempts.
- A **publish-subscribe channel** makes a publication available to each subscribed consumer group according to retention/subscription rules.
- **delivery attempt** is one handoff; **processing** is the consumer's domain effect; **acknowledgement** transfers responsibility only at a defined boundary.
- **publisher confirmation** reports broker acceptance under a stated durability policy; it does not report consumer processing.
- **at-most-once**, **at-least-once**, and **effectively-once** describe end-to-end outcomes under premises—not marketing labels attached to a transport.
- A **partition/key** selects an ordered substream and parallelism unit; global order rarely follows from per-partition order.
- **backpressure/flow control** limits production or admission when receivers/storage cannot keep up.
- A **dead-letter/quarantine channel** retains messages requiring diagnosis; it is not automatic business recovery.

### Central model, mechanism, or theorem

For message identity $m$, let $P_m$ be publish attempts, $D_m$ delivery attempts, and $E_m$ committed domain effects. With acknowledgement after an atomic/idempotent effect boundary and redelivery after uncertainty, a typical channel targets

$$
P_m\ge1,\qquad D_m\ge1,\qquad E_m=1.
$$

The channel can make $D_m\ge1$ under its availability/durability premises, but $E_m=1$ requires the consumer to bind message identity to its effect using a uniqueness constraint, inbox, naturally idempotent transition, or equivalent protocol. Exactly-once business effect is not implied by one broker delivery.

Queue backlog evolves as

$$
B_{t+1}=\max(0,B_t+A_t-C_t-X_t),
$$

where admitted messages $A_t$, completed messages $C_t$, and expirations/drops $X_t$ must be governed. If long-run arrival rate exceeds sustainable completion rate, backlog, latency, rejection, or loss must grow.

### Critical invariants

- Channel purpose, owner, producers, consumer groups, message types, partition key, and lifecycle are documented.
- Producer database change and publication use outbox/transactional mechanism or explicitly tolerate their dual-write gap.
- Publisher confirmation and consumer acknowledgement have distinct meanings and are correlated to message identity.
- Consumers acknowledge only after the required durable/idempotent effect boundary; uncertain work may redeliver.
- Ordering promises name their scope and interaction with concurrency, retry, requeue, and poison messages.
- Capacity, admission, retention, expiry, replay, lag, and overload policy are explicit and tested.
- Every message carries stable identity, type/schema version, occurred/recorded time, source, correlation/causation, and trusted tenant/security context as appropriate.
- Authentication, authorization, encryption, integrity, secrets, tenant isolation, and payload minimization apply at publish and consume.
- Schema evolution supports deployed producer/consumer overlap; unknown messages are not silently discarded.
- Operations can observe publish/confirm/delivery/ack/failure/age/lag/retry/quarantine without exposing payload secrets.

### Common failures

Common failures include treating a channel as a reliable pipe, database/message dual writes, acknowledging before effect, confusing confirm with processing, non-idempotent consumers, unbounded retry storms, global ordering assumptions, hot partition keys, slow consumers hidden by growing retention, silent expiry, dead letters never owned, replaying irreversible commands, shared catch-all topics, schema changes without overlap, trusting tenant/actor headers, secrets in payload/logs, request-response over a channel without deadlines, autoscaling that overloads a database, and green happy-path tests without broker/consumer crash injection.

### Compact example

A capacity-two in-memory point-to-point channel admits `m-1` and `m-2`, rejects `m-3` with backpressure, delivers `m-1`, then requeues it after simulated failure. The redelivery is processed once using a consumer identity set and acknowledged. The trace demonstrates duplicate delivery with one local effect—not broker durability or distributed exactly-once behavior.

### Connections

[SEPAT-060](060-choosing-an-enterprise-domain-and-persistence-pattern.md) selected enterprise boundaries; [SEPAT-062](../ROADMAP.md) routes messages among channels. Message channels connect to [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md), [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), [Security Engineering](../../25-security-engineering/ROADMAP.md), and [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

What guarantees does a channel actually provide between a producer's decision and a consumer's durable business effect, and how should its failure, overload, evolution, and security boundaries be designed and verified?

A channel creates temporal and location decoupling: producer and consumer need not execute together or know direct addresses. It does not eliminate coupling. They still share message meaning, ownership, timing expectations, security premises, capacity, and failure protocols.

## Why This Matters

Messaging enables buffering, asynchronous work, fan-out, independent deployment, and resilience to temporary receiver unavailability. It also creates distributed state: a producer may not know whether publish succeeded, a consumer can crash after effect but before acknowledgement, and old messages outlive code versions.

Most serious messaging defects occur between layers. Database commits without events, confirmed events without processing, acknowledgements before durable effects, retries after unknown outcomes, and schema/security drift are end-to-end protocol failures rather than queue API mistakes.

## Prerequisites and Retrieval

You should understand processes, networks, queues/logs, transactions, idempotency, outbox/inbox, schemas, clocks, authorization, encryption, capacity, and observability. Retrieve these facts:

1. A socket write does not prove broker acceptance, and broker acceptance does not prove consumer processing.
2. A consumer can commit an effect and crash before acknowledging; redelivery is then correct transport behavior.
3. Ordering within one partition does not imply order across partitions or concurrent consumer effects.
4. Durable queue/topic configuration and durable/persistent messages are separate choices in many brokers.
5. Infinite retry under a permanent defect consumes capacity and can block useful work.
6. A message captured from a request cannot safely replay ephemeral authentication/authorization forever.
7. Retention permits replay but increases storage, privacy, deletion, and schema-compatibility obligations.

## Learning Objectives

After completing this module, you should be able to:

- distinguish logical channel semantics from broker/product mechanisms;
- choose point-to-point, publish-subscribe, queue, stream/log, or direct invocation for a use case;
- reason end to end about publish confirmation, delivery, effect, acknowledgement, retry, and uncertainty;
- implement outbox/inbox or equivalent idempotent boundaries for important state transitions;
- define ordering, partitioning, concurrency, capacity, backpressure, retention, expiry, and replay;
- govern retry, poison messages, quarantine, redrive, and operator ownership;
- design message identity, envelope, schema compatibility, provenance, and time semantics;
- enforce authentication, authorization, tenant isolation, confidentiality, integrity, and minimization;
- instrument service level indicators for publish, lag, age, processing, failure, and recovery;
- verify channels through deterministic protocol models plus real broker/database/concurrency/fault/load tests.

## Core Exposition

### Start with channel intent

Name the business fact/command/query carried, authoritative producer, permitted publishers, consumer groups, response expectations, loss/duplicate/order tolerance, latency objective, retention, and owner. A channel named `events` or `misc` hides contracts; use stable domain intent such as `billing.invoice-issued` with governance independent of one deployment sequence.

Do not put unrelated message types on one channel solely for operational convenience. Datatype-specific contracts improve authorization, compatibility, routing, retention, and observability.

### Separate logical topology from technology

A logical channel may be implemented by a broker queue, topic, partitioned log, cloud service, database outbox poller, or in-process queue. Product terms differ. Document semantic requirements first, then map configuration and client behavior to them.

The broker is one participant in an end-to-end protocol. Producer storage, network, broker replication/storage, consumer runtime, effect database, and downstream calls each have separate failure/acknowledgement boundaries.

### Choose point-to-point for competing work

A point-to-point channel delivers each message to one consumer attempt from a competing group. It supports load distribution and work queues. With failure/redelivery, several attempts may occur sequentially and occasionally overlap under lease/visibility timeout behavior.

Use stable message identity and idempotent effects. Concurrency, prefetch, visibility/ack deadlines, and retry affect order and load. A single active consumer can preserve more order but limits throughput/availability.

### Choose publish-subscribe for independent reactions

Publish-subscribe lets distinct subscriptions/groups independently observe a fact. Each group owns its checkpoint, lag, retry, and effect. One group's acknowledgement must not erase another group's obligation.

Late subscribers see history only if retention and subscription semantics provide it. A transient broadcast and a retained log are materially different channels. Define whether the message is a past-tense fact or an imperative command; broadcasting a command can create ambiguous ownership.

### Distinguish queue from retained log

A queue commonly removes/forgets a message after acknowledgement/retention policy. A log retains records and consumers advance positions, enabling replay and multiple views. Both can implement point-to-point-like consumer groups and pub/sub-like fan-out depending on product.

Logs require partition/offset, compaction/retention, replay, deletion, and schema rules. Queues require acknowledgement, redelivery, dead-letter, expiry, and depth rules. Choose by semantics, not brand category.

### Close the producer dual-write gap

Updating business state and separately publishing can yield committed-without-message or message-without-commit. Prefer a transactional outbox written with business state, then relay and mark/track publication idempotently. Broker/database transaction integration is product-specific and may still expose uncertain commit.

The relay uses publisher confirmation, retains unconfirmed records, and retries with the same stable message identity. Confirmation establishes broker responsibility under configured premises, not consumer outcome. Monitor outbox age and publish uncertainty.

### Bind consumer effect and acknowledgement

The consumer validates envelope/schema/security, begins an effect transaction, claims message identity through an inbox/unique constraint or checks a naturally idempotent transition, commits effect plus any outbox, then acknowledges. If crash occurs after commit before ack, redelivery sees the identity and returns success without repeating the effect.

If effect is a remote call without an idempotency protocol, exactly-one outcome may be unknowable. Use provider idempotency keys, durable workflow state, reconciliation, or explicit at-least/at-most-once business semantics.

### Define delivery claims precisely

At-most-once usually acknowledges/removes before or without retry: duplicates decrease but loss is possible. At-least-once retries uncertain deliveries: loss decreases under premises but duplicates are expected. “Exactly once” may mean one log transaction, one consumer state update within a broker ecosystem, or one deduplicated business effect; state scope and failure assumptions.

End-to-end effect safety combines transport with application state. Do not promise universal exactly-once across arbitrary external systems.

### Scope ordering

State order by channel, partition/key, producer session, or entity. Parallel partitions provide throughput but no global order. Multiple producers, network retries, redelivery, dead-letter/redrive, priority, and concurrent processing can alter observed/effect order.

If one entity's transitions require order, route by stable scoped entity key and ensure one effective sequencer or use version/precondition checks. Handle gaps, duplicates, stale versions, and late events; do not wait forever for an event that may never arrive.

### Choose partition keys from correctness and load

Keys should co-locate messages requiring ordered processing and distribute load. A tenant ID may preserve tenant order but one large tenant becomes a hot partition; a random key balances load but destroys entity order. Composite/hash strategies require migration and collision/ownership analysis.

Partition count affects parallelism and key-to-partition mapping. Repartitioning can disrupt ordering and consumer state; test resharding and skew with representative distributions.

### Govern capacity and backpressure

No channel has infinite useful capacity. Bound producer rate, queue depth/bytes, message size, consumer concurrency, prefetch, in-flight leases, retention, and downstream connections. When saturated, block, reject, shed, spool, expire, sample, or degrade according to business priority.

Autoscaling consumers can overwhelm the effect database/API. Use end-to-end concurrency budgets and adaptive admission. Track oldest-message age and completion rate, not depth alone; a stable deep retained log differs from an aging work queue.

### Design retry as a policy

Classify transient, throttled, conflict, malformed, unauthorized, expired, and permanent domain failures. Retry only safe/retriable classes with bounded attempts/time, exponential backoff and jitter where appropriate, and respect deadlines/`retry-after`.

Do not hold a partition behind a poison message indefinitely unless strict order requires an explicit incident policy. Quarantine with reason/evidence, alert an owner, provide inspect/redact/correct/redrive tooling, and preserve identity/attempt history.

### Treat dead-letter channels as operations

A dead-letter message is unfinished business or intentionally discarded input under policy. Define ownership, access controls, retention, payload privacy, alert thresholds, diagnosis, correction, replay destination, and closure evidence.

Blindly redriving a batch recreates outage or duplicates effects. Revalidate current authorization/schema/business applicability and rate-limit redrive. Some expired commands should be cancelled/reconciled, not executed late.

### Design a durable envelope

Include globally/stably scoped message ID, message type and schema version, source, occurred-at and recorded/published-at with time semantics, correlation and causation IDs, tenant/partition key, trace linkage, content type, and policy-relevant expiry. Keep transport delivery attempt outside immutable event identity.

Do not copy arbitrary request headers. Actor tokens expire and may expose secrets. Carry minimal claims/provenance and reauthorize current sensitive actions; a past fact records who/what caused it under audit semantics.

### Evolve schemas for overlap

Producers and consumers deploy independently and retained messages outlive both. Prefer additive compatible changes, stable field meanings, defaults that preserve semantics, and explicit type/version evolution. Test old producer/new consumer, new producer/old consumer, replayed historical messages, and unknown future variants.

A schema registry validates shape/compatibility but not domain meaning. Renaming/reusing a field with changed units or semantics can be wire-compatible and wrong. Use new fields/types and migration translators with provenance.

### Protect the channel

Authenticate workloads; authorize publish/subscribe/admin per channel and tenant; isolate credentials and namespaces; encrypt in transit and at rest according to threat model; verify integrity where broker trust is insufficient; rotate secrets/keys; minimize payloads; and audit configuration/access.

Consumer authorization cannot blindly trust mutable headers. Prevent confused-deputy effects, cross-tenant keys, replay of privileged commands, injection/deserialization hazards, oversized/decompression payloads, and sensitive data in telemetry/quarantine.

### Handle request-reply cautiously

Messaging request-reply needs correlation, reply channel, deadline, cancellation/abandonment, duplicate replies, late replies, responder idempotency, and backpressure. It may reproduce synchronous coupling with harder failure semantics.

Use direct synchronous calls when the caller truly waits and both sides share availability/latency needs. Use asynchronous commands/status/workflows when completion is long-running or uncertain.

### Observe end-to-end progress

Measure producer enqueue/outbox age, publish attempts/confirms/nacks/unroutable, broker availability/replication, depth/bytes, oldest age, partition/group lag, delivery/redelivery, processing/transaction duration, ack/nack, retry/quarantine, dedupe hit, effect/outbox completion, and reconciliation mismatch.

Trace with bounded IDs and sampling; metrics use low-cardinality channel/group/outcome labels. Logs redact payload/credentials/personal data. Service levels should express business completion time and loss/duplicate/recovery evidence, not merely broker uptime.

### Test real failure boundaries

Unit/property-test envelope, schema, idempotency, version/order/gap, retry classification, expiry, and state transitions. Integration-test real clients/broker/database for confirms, routing, durability, ack timing, redelivery, leases/prefetch, consumer rebalance, transactions, auth, and schema compatibility.

Crash producer before/after business/outbox commit and before/after confirm; crash consumer before/during/after effect commit and before ack. Partition network, restart/lose broker nodes under documented durability configuration, throttle downstreams, inject poison/large/duplicate/out-of-order messages, replay history, rotate credentials, and restore/reconcile. Load-test skew and backlog recovery without overwhelming downstream dependencies.

### Executable model: capacity, redelivery, and local deduplication

This finite channel models admission, one in-flight delivery, requeue after failure, and consumer deduplication. It is not a durable broker, does not model concurrency or transactions, and cannot establish distributed delivery guarantees.

<!-- bijux-verify: {"id":"message-channel-redelivery","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"publish=m-1:accepted m-2:accepted m-3:backpressure depth=2\nfirst=m-1 attempt=1\nredelivery=m-1 attempt=2 effect=applied\nafter_ack=queued:1 in_flight:0 effects:1\n","stderr":""}} -->
```python
class Channel:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = []
        self.in_flight = {}
        self.attempts = {}

    def publish(self, message):
        if len(self.queue) + len(self.in_flight) >= self.capacity:
            return "backpressure"
        self.queue.append(message)
        return "accepted"

    def deliver(self):
        message = self.queue.pop(0)
        message_id = message["id"]
        self.attempts[message_id] = self.attempts.get(message_id, 0) + 1
        self.in_flight[message_id] = message
        return message

    def requeue(self, message_id):
        message = self.in_flight.pop(message_id)
        self.queue.insert(0, message)

    def acknowledge(self, message_id):
        self.in_flight.pop(message_id)


channel = Channel(2)
first_status = channel.publish({"id": "m-1", "value": 7})
second_status = channel.publish({"id": "m-2", "value": 9})
third_status = channel.publish({"id": "m-3", "value": 11})
print(f"publish=m-1:{first_status} m-2:{second_status} m-3:{third_status} depth={len(channel.queue)}")
message = channel.deliver()
print(f"first={message['id']} attempt={channel.attempts[message['id']]}")
channel.requeue(message["id"])
message = channel.deliver()
processed = set()
effect = "duplicate"
if message["id"] not in processed:
    processed.add(message["id"])
    effect = "applied"
print(f"redelivery={message['id']} attempt={channel.attempts[message['id']]} effect={effect}")
channel.acknowledge(message["id"])
print(f"after_ack=queued:{len(channel.queue)} in_flight:{len(channel.in_flight)} effects:{len(processed)}")
```

### Finite invariant argument

Capacity two admits the first two messages; the third sees two queued/in-flight and is rejected. First delivery removes `m-1` from queue, records it in flight, and sets attempt one. Requeue removes it from flight and inserts it before `m-2`; second delivery therefore returns `m-1` and increments attempt two.

The initially empty `processed` set admits one local effect for `m-1`; acknowledgement removes its in-flight entry. Final state has only `m-2` queued, no in-flight entries, and one processed identity. The trace demonstrates that redelivery count two can coexist with local effect count one. It assumes serialized, failure-free dictionary/list operations and places dedupe outside a transaction; a real crash between effect and durable identity would invalidate the claim.

### Evidence classification

The snippet report is empirical evidence for this deterministic trace. Counts and branch transitions are recomputable. It provides no broker persistence, network, replication, transaction, security, ordering under concurrency, performance, or distributed exactly-once evidence.

## Definitions and Notation

Let message envelope be $m=(id,type,version,source,tenant,key,t_o,t_r,correlation,causation,payload)$. Occurred time $t_o$ describes the source event; recorded/published time $t_r$ describes capture. Neither is assumed globally synchronized.

Let channel state contain ordered/partitioned retained messages $Q$, in-flight attempts $F$, consumer-group positions $Z$, and quarantine $L$. `publish`, `deliver`, `acknowledge`, `negative-acknowledge`, `expire`, `redrive`, and `commit-position` have product-specific atomicity; document exact mapping.

$P_m,D_m,E_m$ count publish attempts, delivery attempts, and committed business effects for identity $m$. An acknowledgement may attest receipt or completed durable processing; the contract must choose. Publisher confirmation is denoted $K_m$ and has no implication $E_m>0$.

Arrival rate $\lambda$, sustainable completion rate $\mu$, backlog $B$, oldest age $W$, and partition skew characterize capacity. Long-run $\lambda>\mu$ is unstable without admission/drop/expiry; autoscaling changes $\mu$ only until a downstream bottleneck binds.

## Mechanisms, Invariants, or Proof Structure

The end-to-end mechanism is:

1. Producer validates/authorizes a domain decision and atomically stores state plus outbox identity.
2. Relay publishes with the same identity and waits/tracks broker confirmation.
3. Broker durably routes/retains according to channel configuration.
4. Consumer receives an attempt and validates envelope/schema/security/expiry/order.
5. Consumer atomically claims identity and commits effect plus outgoing outbox, or recognizes a prior effect.
6. Consumer acknowledges only after that boundary; uncertainty leads to redelivery.
7. Operators reconcile outbox, broker, inbox/effect, and downstream outcomes.

Safety invariants include no accepted business decision without eventually visible outbox under its database premises; no acknowledgement before durable effect/dedupe boundary; at most one committed effect per stable message identity; tenant/type authorization on every attempt; monotone version/order policy per key; bounded resource admission; immutable original identity/provenance across retry/redrive; and auditable terminal state for expired/quarantined work.

Liveness claims require availability, retention, retry budget, fair scheduling, consumer capacity, valid schemas/credentials, and recoverable dependencies. A safety design can intentionally stop on poison data; it must alert and expose recovery rather than claim eventual completion unconditionally.

Proof obligations decompose: finite state/protocol review for transitions; database uniqueness/transaction evidence for dedupe/effect; broker tests for confirm/durability/routing/order scope; fault injection for crash boundaries; load tests for capacity/skew/recovery; schema/security review; and reconciliation over authoritative records. No broker-only test proves the whole protocol.

## Alternatives and Trade-Offs

| Mechanism | Strong fit | Main cost/risk |
|---|---|---|
| Direct synchronous call | Immediate result, simple topology | Temporal/availability coupling |
| In-process queue | One process async work | Process loss/scaling boundary |
| Durable work queue | Competing background tasks | Redelivery/idempotency/poison work |
| Publish-subscribe topic | Independent reactions | Per-subscriber lag/effects/governance |
| Partitioned retained log | Ordered substreams, replay, projections | Partition/schema/retention operations |
| Database outbox polling | Close producer dual-write gap | Relay lag/table maintenance |
| Workflow engine | Long-lived explicit state/timers | Platform/model complexity |
| File/batch transfer | Large scheduled datasets | Latency, partial/reconciliation handling |

Channels can be combined, but each bridge is another consumer-producer transaction with dedupe, schema, security, capacity, and observability obligations.

## Failure Modes and Misconceptions

- **“The broker guarantees delivery.”** Guarantees depend on producer confirms, routing, persistence/replication, retention, consumer acknowledgements, and recovery.
- **“Confirmed means processed.”** It means broker responsibility under stated policy, not domain effect.
- **“Acknowledged means success.”** Only if consumer acknowledges after the correct durable effect boundary.
- **“Exactly once is a switch.”** Scope may stop at a broker transaction; external effects need identity/idempotency/reconciliation.
- **“FIFO means effects are ordered.”** Partitions, concurrent processing, retry, and commit timing can reorder effects.
- **“More partitions always scale.”** They affect key order, rebalancing, state, overhead, and downstream bottlenecks.
- **“Depth zero means healthy.”** Messages may be dropped, expired, stuck in outbox, or processing slowly in flight.
- **“Retry eventually works.”** Permanent defects cause storms and head-of-line blocking.
- **“Dead letter is handled.”** Without owner/tooling/reconciliation it is an ignored data-loss queue.
- **“Schema registry proves compatibility.”** Shape compatibility cannot prove unchanged units/meaning.
- **“Events are public facts.”** Sensitive facts still require purpose, minimization, retention, and access controls.
- **“A signed actor token can replay forever.”** Authority and context expire/change; current actions need current authorization.
- **“Async means decoupled.”** Business semantics, capacity, response deadlines, and ownership still couple systems.
- **“Autoscale consumers to drain backlog.”** The effect database/provider may collapse first.
- **“Happy-path integration tests are enough.”** Crash windows and ambiguous outcomes define messaging correctness.

## Worked Examples

### Example 1

**Situation.** Order commit succeeds but process crashes before publishing `OrderPlaced`.

**Reasoning.** Separate writes lose the fact. Store state and outbox in one transaction; relay retries same identity until confirmed and reconciliation alerts old outbox rows.

**Conclusion.** The producer boundary needs a transactional publication protocol.

### Example 2

**Situation.** Consumer charges a card, crashes before ack, then receives the message again.

**Reasoning.** Redelivery is expected. Use provider idempotency key tied to stable message/business operation, durable workflow outcome, and reconciliation for ambiguous provider responses.

**Conclusion.** Broker delivery count and payment effect count are separate.

### Example 3

**Situation.** Customer events are keyed randomly for balance, and `Closed` is processed before `Opened`.

**Reasoning.** Random keys discard entity order. Key by scoped customer when order matters, validate versions/gaps, and address hot tenants separately.

**Conclusion.** Partition key is a correctness and capacity decision.

### Example 4

**Situation.** A consumer acks immediately, then database write fails.

**Reasoning.** Broker may delete delivery and effect is lost. Commit inbox/effect/outbox first, then acknowledge; on ack uncertainty redelivery deduplicates.

**Conclusion.** Acknowledgement marks responsibility transfer after durable work.

### Example 5

**Situation.** Publish-subscribe has billing, search, and email groups; email ack occurs.

**Reasoning.** Email progress cannot satisfy billing/search positions. Each subscription owns lag, retry, effect, quarantine, and SLO independently.

**Conclusion.** Fan-out creates multiple obligations.

### Example 6

**Situation.** One malformed message retries instantly and blocks its ordered partition.

**Reasoning.** Classify permanent schema/domain failure, quarantine with access-controlled evidence, alert owner, and decide whether later versions can proceed or strict order requires intervention.

**Conclusion.** Retry policy must distinguish transient from poison data.

### Example 7

**Situation.** A new producer changes amount from cents integer to decimal dollars under the same field name.

**Reasoning.** Wire shape may remain numeric while meaning changes catastrophically. Introduce a versioned field/type with explicit currency/unit, overlap tests, translator, and reconciliation.

**Conclusion.** Semantic compatibility exceeds schema syntax.

### Example 8

**Situation.** Queue depth falls after messages silently expire at one hour.

**Reasoning.** Dashboard appears healthy while work is lost. Expiry must produce governed metric/audit/terminal outcome and business cancellation/reconciliation.

**Conclusion.** Capacity relief is not successful completion.

### Example 9

**Situation.** Consumer autoscaling from 10 to 500 drains queue into a database limited to 80 concurrent writes.

**Reasoning.** Connection contention/timeouts amplify retries. Bound prefetch/concurrency at downstream capacity and use admission/rate feedback.

**Conclusion.** Channel throughput is end-to-end, not consumer-count-only.

### Example 10

**Situation.** A clinical alert channel delivers an allergy alert after the medication order was cancelled and clinician authorization changed.

**Reasoning.** Consumer verifies message provenance/schema but must also check current order/version, patient/tenant/purpose, authority, expiry, and approved late-alert workflow; audit stale outcome rather than blindly acting.

**Conclusion.** Delayed high-stakes commands require current-state and human-reviewed safety policy.

## Cross-Program Connections

- [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md) supplies delivery, consensus/replication, time, consistency, retry, and partition reasoning.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) develops commands/events, idempotency, asynchronous operations, and contract evolution.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) grounds outbox/inbox transactions, constraints, isolation, logs, and reconciliation.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies workload identity, channel ACLs, tenant isolation, cryptography, privacy, and audit.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) operates brokers, capacity, deployment, telemetry, recovery, and cost.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) provides protocol, contract, fault, load, security, and recovery evidence.
- [SEPAT-060](060-choosing-an-enterprise-domain-and-persistence-pattern.md) frames boundary choice; [SEPAT-062](../ROADMAP.md) adds message routing.

## References

1. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns*, Addison-Wesley, 2003. Message Channel and related channel/message/endpoint patterns.
2. Enterprise Integration Patterns, [“Introduction”](https://www.enterpriseintegrationpatterns.com/patterns/messaging/Introduction.html), accessed 2026-08-29. Pattern language and channel taxonomy.
3. Apache Kafka, [“Introduction”](https://kafka.apache.org/documentation/), current documentation accessed 2026-08-29. Topics, partitions, keys, ordering, producers, and consumers.
4. RabbitMQ, [“Consumer Acknowledgements and Publisher Confirms”](https://www.rabbitmq.com/docs/confirms), current documentation accessed 2026-08-29. Distinct producer/broker and broker/consumer acknowledgement boundaries.
5. RabbitMQ, [“Reliability Guide”](https://www.rabbitmq.com/docs/reliability), current documentation accessed 2026-08-29. Connection recovery, acknowledgements, confirms, clustering, and data safety.
6. Clemens Vasters et al., [“CloudEvents Specification”](https://github.com/cloudevents/spec), current specification repository accessed 2026-08-29. Interoperable event context attributes.
7. AsyncAPI Initiative, [“AsyncAPI Specification”](https://www.asyncapi.com/docs/reference/specification/latest), current specification accessed 2026-08-29. Machine-readable asynchronous API/channel/message contracts.
8. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Logs, streams, delivery, transactions, and derived data.
9. Chris Richardson, *Microservices Patterns*, Manning, 2018. Transactional outbox, idempotent consumer, sagas, and messaging patterns.
10. NIST, [“Zero Trust Architecture”](https://csrc.nist.gov/pubs/sp/800/207/final), SP 800-207, 2020. Resource/workload access principles and continuous policy evaluation.

## Exercises

### Exercise 1

Trace five crash points across producer state/outbox/confirm and consumer effect/ack. State possible duplicates/loss and the evidence needed for recovery.

### Exercise 2

Design a partitioned channel for tenant-scoped account transitions. Choose key/partition count, ordering/version/gap policy, capacity, hot-tenant mitigation, rebalance, and resharding evidence.

### Exercise 3

Specify an envelope and compatibility policy for invoice-issued facts retained seven years. Cover identity, types/units/time, provenance, schema overlap, replay, privacy/deletion, authorization, and reconciliation.

### Exercise 4

Diagnose a system with immediate infinite retries, 30-day dead-letter accumulation, early acknowledgements, no publisher confirms, and autoscaling consumers. Produce an incremental correction and verification plan.

### Exercise 5

Review a high-stakes clinical alert channel. Cover source transaction, current-state checks, delivery/effect semantics, order/expiry, authorization/privacy, degraded workflows, accessibility/human factors, operations, tests, and named human review.

## Answers to the Exercises

### Answer 1

Before business/outbox commit, neither should exist after rollback; retry command under idempotency. After atomic commit but before relay, state/outbox exist and relay/reconciliation must publish. After broker accepts but before confirm reaches relay, relay republishes same identity, so duplicate publication/delivery is possible and consumers deduplicate. Consumer crash before effect commit leaves no effect and delivery must redeliver. Crash after effect/inbox commit but before ack redelivers; inbox identity returns prior success without repeating effect, then ack.

Evidence includes database atomicity/unique constraints, relay leasing and stable IDs, broker routing/durability/confirm configuration, consumer transaction and ack order, provider idempotency for remote effects, fault tests at every boundary, outbox/inbox/effect reconciliation, and recovery runbooks. Without outbox or post-effect dedupe, some windows necessarily permit loss or duplicate effects.

### Answer 2

Key by `(tenant, account)` so one account's versioned transitions share a partition; hash across enough partitions for planned parallelism. Consumer accepts next version, ignores exact duplicate identity/version, quarantines conflicting duplicate, and buffers/requests repair or stops according to bounded gap policy. It never assumes global tenant order. Guard effects by account/version in database.

Measure real tenant/account skew; isolate exceptionally hot accounts/tenants only through a versioned routing change that preserves per-key ownership. Bound message size, producer admission, per-partition/group lag and oldest age, consumer concurrency/prefetch, and downstream writes. Rebalance tests cover duplicate in-flight delivery and state/checkpoint transfer. Reshard with documented key mapping epoch, drain/fence or version guards, dual-routing prohibition, shadow verification, backlog/recovery load tests, and reconciliation proving no missing/conflicting account versions.

### Answer 3

Envelope uses immutable globally scoped ID, type `billing.invoice-issued` with schema version, authoritative source, tenant/invoice partition key, occurred/recorded UTC instants plus source timezone where meaningful, correlation/causation, trace link, and expiry only if business-valid. Payload uses decimal/string minor-unit representation with ISO currency, invoice/version, totals by named category, policy/tax version, and references rather than unnecessary personal data.

Use additive evolution, never reuse field meanings/units, test old/new producer-consumer combinations and historical fixtures, register shape plus semantic contract, and introduce new type/version with translator/provenance for breaking change. Seven-year replay requires executable/upcastable schema history, deterministic consumer policy or recorded policy versions, projection rebuild/reconciliation, retention/backup/restore drills, and controlled replay rate. Apply tenant/group ACLs, encryption/key rotation, minimization, legal retention/deletion strategy, redacted observability/quarantine, and audit. Reconciliation compares authoritative invoice versions/counts/amounts with channel/projections.

### Answer 4

First stop loss: move acknowledgement after durable inbox/effect transaction, enable/verify publisher confirms and unroutable handling, and reconcile producer state against missing publications—introducing transactional outbox if absent. Add stable IDs and dedupe before redriving. Classify errors; bounded exponential/jitter retry for transient failures, respect throttling/deadlines, quarantine permanent malformed/unauthorized/domain failures with reason.

Assign dead-letter owner, access/privacy/retention, alert by rate/age, inspect/correct/cancel/redrive tooling, and reconcile every terminal item. Rate-limit redrive. Cap consumer concurrency/prefetch to database/downstream capacity; autoscale from end-to-end throughput/lag/oldest age and saturation, not depth alone. Gate changes with real broker/database crash-window tests, duplicate/poison/out-of-order/schema/security cases, representative skew/load and backlog recovery, confirm/ack telemetry, outbox-inbox-effect reconciliation, credential rotation, and disaster recovery.

### Answer 5

Clinical source operation validates authoritative patient/order/alert rule evidence and atomically stores state, provenance/policy version, audit, and outbox. Relay confirms durable scoped publication. Consumer deduplicates identity and rechecks current tenant/patient/purpose, clinician/system authority, order/version/status, alert expiry, supersession, consent/privacy, and clinical policy before committing presentation/escalation state and outbox, then acknowledges. Stale/cancelled/conflicting alerts enter an audited reviewed terminal/escalation path rather than blind action.

Per-patient/order keys and versions govern order; strict global order is unnecessary. UI distinguishes urgent, stale, unavailable, acknowledged, overridden, and unresolved states; uses keyboard/screen-reader/color-independent cues, prevents alert flooding, records reason, and escalates under approved downtime workflow. Minimize/encrypt payload, restrict channel/quarantine/admin access, rotate credentials, and redact telemetry.

Test source/outbox crashes, broker durability/partition/restart, duplicate/gap/reorder/late/expired/superseded alerts, consumer effect/ack crashes, current authorization changes, cross-tenant guesses, source outage, alert fatigue/accessibility, load/backlog/recovery, replay/redrive, privacy/retention, audit and reconciliation. Named prescribing clinicians, pharmacists, clinical safety/informatics, nursing/workflow users, patients or representatives, privacy/legal/regulatory, security, accessibility/human-factors, database/messaging/SRE, and incident-response owners review real rules. Automated delivery evidence cannot establish clinical safety.
