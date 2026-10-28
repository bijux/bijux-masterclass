---
module_id: DARCH-035
program: Data Architecture Engineering
level: 1
module_number: 35
title: Event-Driven Data Integration
status: complete
last_verified: 2026-09-03
---

# Event-Driven Data Integration

## One-Page Review

### Governing question

When should domains integrate by publishing and consuming events, and how can they preserve fact semantics, time, ordering, identity, delivery, replay, correction, protection, ownership, and lifecycle when producers do not coordinate each consumer interaction synchronously?

### Essential definitions

- An **event** is an immutable record that a named occurrence or observation happened, with explicit source, meaning, identity, and time.
- An **event notification** signals that something changed and may require a later lookup; an **event-carried state transfer** includes enough state for a consumer to update a local view.
- A **domain event** expresses a fact meaningful within a bounded domain; an **integration event** is a governed representation published across a boundary.
- An **event envelope** carries common context such as identifier, source, type, subject, time, schema, correlation, classification, and trace data.
- **Event time** is when the represented occurrence happened; **publication time** is when a producer exposed it; **ingestion time** is when infrastructure accepted it; **processing time** is when a consumer handled it.
- **Ordering scope** states which events have a meaningful sequence, commonly per entity or partition rather than globally.
- **At-least-once delivery** may deliver duplicates; **at-most-once delivery** may lose events. Any stronger guarantee applies only within named boundaries.
- **Idempotent consumption** ensures repeated processing of the same business event does not create an unintended additional effect.
- A **replay** re-delivers retained events or regenerates a range for recovery, new consumers, correction, or recomputation.
- A **watermark** is evidence that events through a declared event-time boundary are believed complete subject to a lateness policy.
- A **dead-letter path** retains or references events that could not be processed under declared rules for investigation, correction, and controlled replay.
- **Event debt** is the future burden created by ambiguous facts, unstable schemas, weak ownership, hidden consumers, lost history, unbounded replay, or indefinite exceptional data.

### Central model, mechanism, or theorem

Represent an event product as:

`E = (fact, source, identity, keys, time, envelope, payload, schema, delivery, ordering, service, protection, observability, ownership, change, lifecycle)`

Event-driven integration decouples producer execution from consumer processing and can support independent subscribers, but it does not remove semantic, temporal, operational, or organizational coupling. Every consumer must know what fact occurred, which version and time apply, how duplicates, gaps, reordering, lateness, replay, and correction behave, and what evidence establishes safe use.

### Critical invariants

- Every published event names one durable fact or observation, its authoritative producer, stable identity, subject or keys, relevant times, schema, version, and limitations.
- Events are immutable records; corrections append explicit superseding, reversal, or restatement facts rather than silently rewriting prior deliveries.
- Delivery guarantees state exact boundaries, acknowledgements, persistence, retention, expiry, duplication, and failure behavior.
- Ordering is promised only within a declared scope and partition-key history; consumers tolerate or detect arrivals outside that scope.
- Consumer effects are idempotent or explicitly reconciled, and deduplication scope and retention match replay and business consequence.
- Producers and brokers bound retries, fan-out, queues, backpressure, poison events, replay rate, and slow-consumer impact.
- Schemas and meaning evolve compatibly or through governed parallel versions, consumer evidence, notices, migration, and retirement.
- Purpose, minimization, classification, access, residency, retention, deletion, records, licensing, and incidents apply to logs, topics, replays, dead letters, and derived state.
- Observability distinguishes publication, acceptance, delivery, processing, outcome, lag, gaps, duplicates, late events, correction, and telemetry failure.
- Topic or stream retirement closes publishers, subscribers, identities, schemas, retained records, copies, monitors, contracts, and support after verified migration.

### Common failures

Common failures are naming commands in the past tense and calling them events; publishing database row changes without domain meaning; assuming broker acceptance proves consumer success; promising global order unnecessarily; changing partition keys without migration; treating event identifiers as business idempotency; claiming exactly-once outcomes across arbitrary side effects; retaining events forever by default; replaying at unlimited rate; placing personal data in topic names or headers; silently correcting old payloads; allowing incompatible schema and semantic changes; using dead-letter queues as permanent archives; measuring low broker latency while consumers are hours behind; and deleting a topic while derived stores, credentials, schemas, and correction duties remain.

### Compact example

An Order domain publishes `OrderAccepted` with stable event and order IDs, source authority, business-effective and publication time, schema version, classification, and per-order ordering key. Consumers acknowledge independently and make effects idempotent by event and business operation. A correction references the affected event. Retention supports a thirty-day replay, while older rebuilds use a governed snapshot. Bulk replay is rate-limited and isolated from live traffic. The event stream decouples processing time without pretending that delivery alone guarantees consumer outcomes.

### Connections

[DARCH-017](017-event-schemas-and-information-models.md) supplies event-model foundations, [DARCH-027](027-producer-and-consumer-contracts.md) defines obligations, and [DARCH-028](028-cross-domain-dependencies.md) exposes fan-out. [DARCH-034](034-api-led-data-access.md) provides request-driven access; this module prepares [DARCH-036](../ROADMAP.md) on change data capture, [DARCH-039](../ROADMAP.md) on replication, and [DARCH-040](../ROADMAP.md) on selecting integration styles.

## Governing Question

Events allow a producer to publish a fact without knowing every downstream action. Consumers can process later, keep local views, and evolve independently within a stable contract. The same decoupling makes failures and dependencies less visible: a producer may succeed while one consumer silently falls behind or misinterprets an old fact during replay.

The governing question is not “Should the architecture be event driven?” It is “Which facts benefit from asynchronous publication, and can the organization govern their meaning, time, delivery, consumer state, correction, protection, and lifecycle across independent processing?”

## Why This Matters

Polling APIs creates repeated load and may miss intermediate transitions. Bilateral messages require a producer to coordinate recipients. A reusable event product can publish a durable source fact once for several authorized consumers. That advantage depends on a stable semantic boundary and sufficient platform operation.

The [CloudEvents Specification 1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md) defines common event context attributes and bindings. The [AsyncAPI Specification 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0) describes message-driven interfaces. They improve interoperable envelopes and contracts without deciding domain meaning, retention, or consumer fitness.

Gregor Hohpe and Bobby Woolf's [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/patterns/messaging/) provides vocabulary for channels, routers, transformations, endpoints, and messaging behavior. [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) specifies an Internet date-and-time profile, and [RFC 9562](https://www.rfc-editor.org/rfc/rfc9562) defines UUID formats. Syntax for time and identity does not establish which occurrence a timestamp represents or which business operation an identifier scopes.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) describes entities, activities, agents, and derivation. Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) explains overload propagation. NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy security across system lifecycles. Together they reinforce that event flows require provenance, bounded failure, and protection beyond message transport.

## Prerequisites and Retrieval

You should understand domain events, data products, producer-consumer contracts, schemas, queues, logs, partitions, distributed failure, APIs, time, identity, service objectives, quality, lineage, provenance, privacy, and lifecycle.

Retrieve occurrence, fact, command, notification, state transfer, envelope, payload, source, subject, event ID, correlation, causation, event time, publication time, ingestion time, processing time, partition, offset, ordering, acknowledgement, duplicate, idempotency, retention, replay, watermark, lateness, dead letter, backpressure, correction, tombstone, and retirement.

As a retrieval test, inspect “CustomerUpdated is published exactly once.” Ask which fact and fields changed, who owns them, which event time applies, how identity and versions work, what boundary promises exactly once, which consumers and effects are covered, how correction and replay behave, and how long evidence remains. The sentence is not yet a usable contract.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish facts, commands, notifications, state-transfer events, audit records, and raw change records;
2. model event products through source authority, identity, keys, time, envelope, payload, schema, delivery, ordering, service, protection, ownership, and lifecycle;
3. define business-effective, publication, ingestion, processing, and system times without collapsing them;
4. design delivery, acknowledgement, duplication, idempotency, ordering, retention, replay, dead-letter, and correction behavior;
5. choose partition keys and ordering scopes from domain invariants and migration needs;
6. evolve schemas and semantics with compatibility analysis, consumer tests, parallel versions, and bounded deprecation;
7. engineer fan-out, capacity, quotas, isolation, backpressure, retries, poison-event handling, and replay safety;
8. apply purpose, minimization, access, residency, retention, deletion, audit, and incident controls to event histories and derived state;
9. observe end-to-end publication, delivery, processing, lag, outcomes, gaps, late events, replays, and corrections;
10. combine events with APIs, snapshots, CDC, batch, and analytical products according to fact semantics and workload.

## Core Exposition

**Begin with a fact.** A useful event states that an occurrence happened: an order was accepted, a payment settled, or a sensor reading was observed. Use past-tense names when they clarify completed facts, but judge semantics rather than grammar.

An instruction such as `ApproveOrder` is a command, not evidence that approval occurred. Commands have an intended recipient and may be rejected. Events record outcomes or observations under a named authority.

**Name the authoritative producer.** The publisher must be entitled to assert the fact. Infrastructure that relays a message does not become the semantic source. If an integration layer derives an event, assign ownership to the derived product and preserve input provenance.

One event may combine facts from several systems. State aggregation rules, time, uncertainty, correction, and owner. Do not call a convenient join a domain event without authority.

**Choose event granularity.** A coarse `CustomerUpdated` notification minimizes contract surface but forces consumers to fetch and compare state. A specific `CustomerAddressChanged` event carries clearer meaning but increases event types and evolution work.

Choose granularity from consumer decisions, source invariants, protection, volume, and stability. Avoid one event per database column and one universal update event with an optional payload.

**Distinguish notification from state transfer.** A notification carries identity and change signal; consumers call an API or read a product for detail. This keeps payloads small but adds availability and race dependencies.

Event-carried state transfer enables local reads and temporal decoupling but duplicates data and requires field minimization, retention, correction, and schema evolution. Hybrid designs can include a bounded snapshot of relevant assertions.

**Define the envelope.** Common context can include event ID, source, type, subject, data content type, schema reference, occurrence time, publication time, correlation, causation, trace, classification, tenant, and version.

CloudEvents standardizes a useful context vocabulary. Extensions still need ownership and collision rules. Keep protected personal or secret data out of routable metadata when it is not essential.

**Define payload assertions.** Record key, grain, field meaning, type, unit, codes, nulls, source, effective interval, quality, classification, and limitations. Schema shape alone is insufficient.

Separate source facts from technical metadata and consumer derivations. A payload can be self-contained enough for intended uses without containing every source attribute.

**Use stable event identity.** Event ID identifies one published event within a declared source scope. A UUID format can reduce collision risk but does not define business sameness.

Retries of the same event should preserve identity. Corrections are usually new events that reference affected identity. Define generation, scope, immutability, collision handling, and retention.

**Separate business identity.** Order ID, payment ID, operation idempotency key, message ID, trace ID, and event ID serve different purposes. A consumer may deduplicate delivery by event ID and separately prevent duplicate payment effects by business operation.

Document identifier relationships. Avoid using broker offsets as portable business identifiers; offsets belong to a topic, partition, and log history.

**Model time explicitly.** Event time states when the occurrence happened. Publication time records when the producer exposed it. Ingestion and processing time describe platform and consumer progress.

Use an interoperable timestamp syntax such as RFC 3339, while recording timezone, precision, clock source, uncertainty, and which time concept applies. A formatted timestamp does not prove clock accuracy.

**Handle late and out-of-order events.** Network delay, retries, mobile devices, source batching, and recovery can make arrival order differ from event time. Consumers need a lateness policy and correction behavior.

Watermarks summarize believed completeness under assumptions; they do not prove no older event will appear. Retain provenance and allow exceptional late corrections where consequence requires.

**Define ordering scope.** Global total order is expensive and often unnecessary. Many invariants need order only per account, order, device, or aggregate.

Choose a partition key that preserves the required sequence and distributes load. State tie-breaking, key changes, repartitioning, and cross-entity behavior. Hot keys can defeat capacity even with many partitions.

**Do not infer causality from arrival order.** Two events can arrive sequentially without one causing the other. Preserve causation and correlation identifiers where meaningful.

Distributed clocks and brokers cannot recover unrecorded business causality. Process logic should use explicit prerequisites, versions, or state checks rather than timestamp comparison alone.

**Define publication atomicity.** An application may commit state and fail before publishing, or publish before rolling back. Use a transactional outbox, log-based capture, or reconciliation pattern suited to the source.

Each mechanism has a boundary. An outbox atomically records application state and publication intent in one transaction, but relay delivery can duplicate. Consumers still need idempotency and gap detection.

**Distinguish domain events from CDC.** Change data capture reports mutations in a source log or table. It can reliably expose low-level changes without conveying why they occurred or which domain invariant completed.

Translate CDC to domain or integration events under explicit ownership when consumers need business meaning. Some replication uses can consume raw changes directly under a physical contract; do not mislabel them.

**Define delivery boundaries.** State where persistence begins, when acknowledgement occurs, when data can be lost, how long it is retained, and which producer, broker, network, and consumer failures are covered.

At-least-once delivery implies possible duplicates. At-most-once implies possible loss. Claims of exactly once need a named transaction or processing boundary and do not automatically cover arbitrary external effects.

**Design idempotent consumers.** Define the effect, event identity, business key, deduplication store, atomicity, retention, duplicate result, concurrency, and recovery. Recording an ID before an effect can lose work; recording after can duplicate it.

Use a transaction where the effect and deduplication record share a boundary, or reconcile uncertain outcomes. Test crash points and lost acknowledgements rather than only repeated happy-path calls.

**Size deduplication retention.** Retain identities at least as long as plausible redelivery or replay for the protected effect, unless another invariant prevents duplicates. Unlimited retention has storage and privacy costs.

For replays beyond the live window, use isolated rebuild stores, epochs, or explicit reset protocols. Do not assume a consumer's ordinary deduplication table supports all historical reconstruction.

**Define retries.** Producers and consumers need timeout, exponential backoff, jitter, maximum attempts, concurrency, retry budgets, and circuit breakers. Retries should not keep invalid events in a hot loop.

Layered client, broker, framework, and consumer retries multiply work. Assign end-to-end ownership and observe original versus retry traffic separately.

**Handle poison events.** Schema-invalid, semantically invalid, unauthorized, or repeatedly failing events need deterministic classification. Reject, quarantine, dead-letter, or pause according to consequence.

Preserve reason, event reference, versions, attempts, owner, retention, access, correction, replay, and closure. A dead-letter topic without a work process is delayed data loss.

**Provide backpressure.** A durable broker can absorb temporary imbalance, not infinite demand. Monitor queue or log lag, age, storage, consumer throughput, and downstream saturation.

Apply quotas, admission, partitions, workload classes, pause, shedding, or producer feedback. Define which events may expire and which require preserved delivery. Do not silently discard consequential facts.

**Isolate consumers.** Independent consumer groups prevent one subscriber from blocking others, but they share broker storage, network, partitions, schemas, and operating teams. One high-volume replay can still harm live workloads.

Use quotas, reserved capacity, separate topics or clusters where consequence warrants, and replay rate limits. Document common failure domains and cost allocation.

**Plan capacity for fan-out.** Egress work can approximate ingress multiplied by subscriber count, payload size, replication, transformation, and retry factors. Actual cost depends on broker architecture and access pattern.

Use rate and size distributions, bursts, hot keys, retention, compression, network, storage, consumer lag, and disaster recovery. Reserve headroom for failover and backlog recovery.

**Design retention from purpose.** Retention supports retries, replays, audit, new consumers, or reconstruction, but it also increases cost, exposure, residency, deletion, and records duties.

Choose duration per event product and use governed snapshots or archives for longer history. “The log is the database” is only responsible when its semantics, protection, indexes, correction, and lifecycle fit that role.

**Plan replay as a production operation.** State source range, schema and semantic versions, target consumer state, deduplication mode, rate, priority, protection, validation, rollback, and owner.

Old events may not work with new code. Preserve compatible readers, transformation versions, or reproducible rebuild logic. Isolate replay from live traffic and observe consumer consequences.

**Define bootstrap.** A new consumer often needs current state before processing new changes. Coordinate a snapshot with an event position or watermark so no gap or duplicate remains unexplained.

State snapshot time, included population, schema, position, late events, correction, and cutover. Buffering events during snapshot load is not enough unless the position relationship is valid.

**Evolve schemas deliberately.** Adding an optional field can break strict readers or change payload size and authorization. Removing or redefining a field is usually more consequential.

Validate producer and consumer fixtures, defaults, enum expansion, precision, nulls, ordering, classification, and behavior. Use parallel versions or new event types when meaning changes incompatibly.

**Evolve semantics explicitly.** Stable syntax can conceal a changed business definition. Publish definition, authority, effective time, impact, examples, correction, and migration.

Avoid reusing an event type name for a different occurrence. A new version may still require consumers to rebuild state or retain old interpretation for historical events.

**Govern consumer discovery.** Register intended subscriptions, purpose, fields, owner, service, protection, versions, and lifecycle. Compare declared consumers with broker authorization and runtime observations.

Unknown use complicates changes and correction. Observation does not authorize use; registration does not prove activity. Reconcile both with accountable owners.

**Protect topics and metadata.** Authenticate publishers and consumers, authorize event types and partitions by purpose, encrypt transport and storage, rotate identities, segment administration, and audit access.

Topic names, keys, headers, schemas, lag metrics, and traces can reveal protected facts. Minimize and classify them. Avoid embedding personal identifiers in infrastructure names.

**Apply deletion and records policy.** Immutable delivery does not mean permanent retention. Deletion may require topic compaction, tombstones, cryptographic erasure, expiry, downstream notification, or documented legal constraints.

Consumers own derived stores and exports. A producer cannot prove ecosystem deletion solely by expiring its topic. Track obligations and evidence across registered consumers.

**Observe end to end.** Measure created, published, accepted, rejected, delivered, acknowledged, processed, succeeded, failed, duplicated, late, replayed, corrected, and expired states where consequence warrants.

Track event-time and processing-time lag, gaps, partition skew, retry rate, dead-letter age, schema versions, consumer outcomes, and missing telemetry. Broker throughput alone is not integration health.

**Maintain provenance.** Relate events to source entities, activities, agents, inputs, transformations, schema versions, and prior events. Preserve split, aggregation, enrichment, replay, correction, and derivation relationships.

Provenance supports impact and correction but does not prove truth. Combine it with source authority, validation, quality, and consumer fitness evidence.

**Design correction.** Never silently mutate already consumed history. Publish a correction, reversal, superseding fact, or restatement with affected identities, fields, intervals, reasons, and versions.

Consumers need procedures to update projections, reports, models, exports, and decisions. Some historical records must preserve both original evidence and later correction.

**Compose service objectives.** Producer availability, publication delay, broker durability, delivery latency, consumer lag, processing correctness, and correction time are separate dimensions.

Define objectives by event product and consumer consequence. Measure at boundaries users care about. A producer can meet publication latency while a consumer remains unusably stale.

**Choose event versus API.** Use an event when consumers benefit from asynchronous notification, independent processing, or a history of facts. Use an API for bounded request-response access or commands.

They often complement one another. Define race behavior when an event tells a consumer to query state, including whether the API representation is guaranteed to include the event's change.

**Choose event versus batch.** Events reduce latency and preserve individual changes, while batch snapshots can provide coherent populations and efficient bulk transfer. High event volume can overwhelm consumers that only need daily state.

Offer a fit-for-purpose product. Do not force event reconstruction when a governed snapshot is simpler, or poll snapshots when a timely fact matters.

**Avoid event-driven slogans.** Asynchrony moves coordination into contracts, queues, consumer state, and operations. It can improve autonomy but also makes end-to-end reasoning harder.

Choose it for evidenced semantic and temporal needs. A direct API, file, CDC feed, or database product may be better for a particular boundary.

**Plan migration.** Inventory current flows, facts, consumers, ordering, timing, workloads, protection, and outcomes. Introduce stable events, IDs, schemas, and telemetry alongside old paths.

Dual publish with an authoritative source and deduplicated effects. Compare values, order, time, gaps, duplicates, service, protection, and consumer decisions. Define rollback and correction before cutover.

**Retire completely.** Stop publishers and subscriptions; revoke identities; remove topics, routes, schemas, connectors, caches, derived stores, alarms, dashboards, providers, and fallback jobs; update catalogs and lineage.

Preserve required records and provenance. Verify consumer migration and post-shutdown absence. A topic with no recent messages but live access and correction obligations is not retired.

**Measure value.** Track reuse, known consumers, contract coverage, publication-to-outcome lag, duplicates, gaps, late events, replay success, correction time, schema changes, saturation, incidents, protection exceptions, cost, and closure.

Event volume is not value. The architecture succeeds when authoritative facts reach intended consumers with understandable time, bounded failure, effective protection, and manageable evolution.

## Definitions and Notation

Represent event product $E=(F,S,I,K,T,H,D,O,Q,Z,V,G,L)$, where $F$ is the fact, $S$ source authority, $I$ event and business identity, $K$ subject and partition keys, $T$ time semantics, $H$ envelope and payload schema, $D$ delivery, $O$ ordering, $Q$ service and quality, $Z$ protection, $V$ observability and provenance, $G$ ownership and change governance, and $L$ lifecycle.

For event $e$, let $t_e$, $t_p$, $t_i$, and $t_c$ denote event, publication, ingestion, and consumer-processing times. Publication delay is $t_p-t_e$ under compatible clocks; consumer lag can be expressed by time or by a declared log position. Negative or uncertain differences require clock and provenance analysis, not silent clamping.

For consumer $c$, define deduplication key function $d_c(e)$ and retention interval $R_c$. Duplicate protection holds only for events whose key remains recorded through plausible redelivery or replay and whose effect update is atomic or reconciled.

For input rate $\lambda$, subscriber fan-out $f$, and expected delivery-attempt factor $a\geq1$, a simple egress-attempt quantity is $W=\lambda f a$. It is not a capacity guarantee because payload sizes, partitions, compression, transformations, burstiness, dependencies, and shared resources vary.

Define `JustifiedEventProduct(E,t)` as a review predicate requiring an authoritative fact, explicit identities and times, bounded delivery and ordering, safe consumer effects, governed evolution, effective protection, observable outcomes, appropriate alternatives, accountable ownership, and funded lifecycle at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every material event product.

**1. Fact gate.** Define occurrence, authority, grain, assertions, keys, identity, time, quality, provenance, purpose, and limitations.

**2. Contract gate.** Specify envelope, payload, schema, examples, versions, publisher and consumer obligations, errors, service, correction, and lifecycle.

**3. Publication gate.** Establish source transaction relationship, outbox or capture, validation, identity reuse, ordering key, acknowledgement, gaps, and reconciliation.

**4. Delivery gate.** Define persistence, duplication, ordering scope, retention, expiry, retries, dead letters, replay, bootstrap, and meaningful consumer completion.

**5. Consumer gate.** Design idempotency, state, deduplication retention, concurrency, late events, gaps, correction, rebuild, outcome evidence, and retirement.

**6. Capacity gate.** Model rate, size, fan-out, partitions, hot keys, bursts, retry, replay, storage, quotas, isolation, backpressure, recovery, and downstream limits.

**7. Protection gate.** Apply publisher and subscriber identity, purpose, minimization, metadata protection, access, residency, providers, retention, deletion, records, audit, and incidents.

**8. Evolution gate.** Govern schema and semantic compatibility, event types, partition changes, fixtures, consumer evidence, parallel versions, notices, migration, and deprecation.

**9. Evidence gate.** Observe creation, publication, acceptance, delivery, processing, outcomes, lag, duplicates, gaps, lateness, replay, correction, provenance, and telemetry gaps.

**10. Lifecycle gate.** Discover, publish, subscribe, operate, correct, revise, migrate, revoke, remove, archive, retire, and verify closure.

The executable example demonstrates bounded duplicate suppression for one replay window.

<!-- bijux-verify: {"id":"event-replay-deduplication-boundary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"deliveries=8\naccepted_unique_events=5\nsuppressed_duplicates=3\naccepted_order=evt-101,evt-102,evt-103,evt-104,evt-105\n","stderr":""}} -->
```python
deliveries = [
    "evt-101", "evt-102", "evt-102", "evt-103",
    "evt-101", "evt-104", "evt-105", "evt-104",
]

seen = set()
accepted = []
for event_id in deliveries:
    if event_id not in seen:
        seen.add(event_id)
        accepted.append(event_id)

print(f"deliveries={len(deliveries)}")
print(f"accepted_unique_events={len(accepted)}")
print(f"suppressed_duplicates={len(deliveries) - len(accepted)}")
print(f"accepted_order={','.join(accepted)}")
```

The example proves only that an in-memory set suppresses three repeated identifiers within this eight-delivery sequence. It does not prove business idempotency, durable or atomic effects, collision-free IDs, correct ordering, gap absence, safe concurrent consumers, sufficient retention, or replay correctness after restart. Production evidence needs durable state, declared scope, failure tests, business invariants, retention, and reconciliation.

## Alternatives and Trade-Offs

**Event versus API.** Events decouple processing time and distribute facts; APIs provide bounded request-response and current lookup. Combining them can add useful recovery or create races that need explicit contracts.

**Notification versus state transfer.** Notifications minimize payload and duplicated data but require lookup availability. State transfer supports local views and autonomy while increasing exposure, storage, evolution, and correction work.

**Domain event versus CDC record.** Domain events express business occurrences under domain ownership. CDC captures physical changes faithfully but couples consumers to storage structures and may omit intent.

**Log versus queue.** A retained log supports independent positions and replay; a work queue distributes items among workers. Products may combine traits, so specify semantics instead of relying on labels.

**Per-entity versus global ordering.** Per-entity order scales and matches many invariants. Global order simplifies some reconstruction while concentrating throughput, availability, and coordination cost.

**Long retention versus snapshot bootstrap.** Long logs enable replay from origin but increase cost and protection duties. Snapshots plus a position support faster bootstrap while adding synchronization and publication complexity.

**Shared broker versus domain platform.** Shared infrastructure reuses operations and controls. Domain-aligned partitions or platforms preserve autonomy but need interoperable envelopes, identity, discovery, and end-to-end evidence.

**Exactly-once mechanism versus idempotent effects.** Bounded transactional processing can simplify a defined pipeline. Idempotent effects and reconciliation remain necessary at boundaries outside that transaction.

**Immutable correction versus rewritten history.** Append-only corrections preserve evidence and consumer notification. Restated snapshots simplify current use but need lineage back to prior assertions and decisions.

**Central schema governance versus federated contracts.** Central review can promote interoperability but create queues. Automated compatibility with accountable domain approval balances autonomy and shared safety.

## Failure Modes and Misconceptions

1. **Past tense makes a message an event.** Authority and completed fact semantics matter.
2. **Every database change is a domain event.** Physical mutation may lack business meaning.
3. **Broker acceptance proves integration success.** Consumers can lag, reject, misapply, or fail.
4. **Asynchrony removes coupling.** Semantics, versions, ordering, time, and service still couple participants.
5. **One timestamp is enough.** Event, publication, ingestion, and processing time answer different questions.
6. **UUID syntax proves business uniqueness.** Generation scope and business identity remain.
7. **Partition order is global order.** Guarantees usually stop at the partition boundary.
8. **Arrival order proves causality.** Explicit causation or state prerequisites are needed.
9. **At-least-once plus a set proves idempotency.** Atomic business effects and retention matter.
10. **Exactly once covers external side effects.** Guarantees end at declared transaction boundaries.
11. **A durable log has unlimited capacity.** Storage, lag, replay, and downstream throughput are finite.
12. **Dead letters preserve safety automatically.** They need owners, protection, correction, and closure.
13. **Optional fields never break consumers.** Strict readers, payload cost, meaning, and authorization can change.
14. **Immutable means retain forever.** Purpose, records, deletion, cost, and risk still govern retention.
15. **Replay is ordinary traffic.** Historical schemas, duplicate effects, load, and priority require a plan.
16. **Low broker latency means fresh consumers.** Processing and outcome lag may dominate.
17. **Deleting a topic retires the product.** Publishers, consumers, copies, schemas, identities, and duties remain.

## Worked Examples

### Example 1

A message named `ApproveOrder` asks a service to decide and can be rejected. `OrderApproved` records the completed decision with authority, order ID, policy version, effective time, and outcome. **Conclusion:** commands express intent; events assert occurrences.

### Example 2

An update notification contains only customer ID. A mobile device receives it before the read replica serving the API. The contract says the event's publication position must be visible to the API or the client retries against a version precondition. **Conclusion:** event-plus-API patterns need an explicit read-after-notification relationship.

### Example 3

Payments are partitioned by customer, but refunds require order order. Two related events land in different partitions and arrive reversed. The design changes the key to order for that invariant and defines a migration epoch. **Conclusion:** partition keys must follow required ordering, not convenient load distribution alone.

### Example 4

An application commits an order and crashes before ordinary publication. A transactional outbox records state and publication intent together. The relay later publishes twice, and the consumer deduplicates atomically with its effect. **Conclusion:** the outbox closes one publication gap but does not remove duplicate delivery.

### Example 5

Eight deliveries contain five event IDs and three duplicates. An in-memory set suppresses duplicates in one process, but restart loses it. A durable deduplication record in the same transaction as the projection update supplies the required boundary. **Conclusion:** algorithmic filtering is not production idempotency without durable atomic state.

### Example 6

A slow consumer accumulates ten hours of lag while broker publish latency remains five milliseconds. Consumer-visible freshness alarms on event-time lag, and the owner pauses noncritical work before retention expires. **Conclusion:** transport latency and consumer outcome lag are distinct service measures.

### Example 7

A replay of two years of events saturates the broker and delays live fraud signals. The operation uses an isolated consumer group, rate and byte quotas, reserved live capacity, version-compatible code, and progress checkpoints. **Conclusion:** replay is a governed production workload, not a free broker feature.

### Example 8

A customer-erasure request expires the live topic but personal identifiers remain in headers, dead letters, backups, and three derived stores. The product contract routes deletion or legal exceptions to each owner and collects evidence. **Conclusion:** producer retention alone cannot prove ecosystem deletion.

### Example 9

An optional `riskBand` field is added. One consumer logs whole payloads and a second strict decoder rejects unknown properties. Compatibility review catches both protection and operational impact. **Conclusion:** additive schema syntax can still be incompatible in use.

### Example 10

A corrected exchange rate cannot rewrite prior consumed events. A new correction event references the original ID, affected currencies and interval, and corrected value. Consumers restate reports while preserving evidence used for completed decisions. **Conclusion:** immutable histories require explicit correction workflows.

## Cross-Program Connections

- **Distributed systems:** logs, partitions, ordering, clocks, delivery, idempotency, backpressure, partial failure, and recovery define event behavior.
- **Data engineering:** streaming ingestion, watermarks, windows, state, checkpoints, replay, quality, lineage, and backfills implement event pipelines.
- **API and service engineering:** commands, events, AsyncAPI contracts, identity, versioning, consumer tests, reliability, and developer experience shape boundaries.
- **Database engineering:** transactions, outboxes, logs, CDC, snapshots, constraints, temporal data, and isolation anchor publication and consumer state.
- **Platform engineering:** brokers, schemas, quotas, tenancy, workload identity, observability, self-service, and capacity sustain shared event capabilities.
- **Cybersecurity and privacy:** topic authorization, protected metadata, purposes, copies, residency, retention, deletion, providers, and incidents constrain streams.
- **Software architecture:** bounded contexts, choreography, orchestration, aggregates, domain events, anti-corruption layers, and coupling locate meaning.
- **Systems engineering:** interface contracts, fault propagation, assurance, configuration, trade studies, verification, and lifecycle make event products governable.

## References

1. Cloud Native Computing Foundation, *CloudEvents Specification 1.0.2*, 2022. <https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md>
2. AsyncAPI Initiative, *AsyncAPI Specification 3.0.0*, 2023. <https://www.asyncapi.com/docs/reference/specification/v3.0.0>
3. Hohpe, G., and Woolf, B., *Enterprise Integration Patterns: Messaging Patterns Overview*, 2003. <https://www.enterpriseintegrationpatterns.com/patterns/messaging/>
4. Klyne, G., and Newman, C., *Date and Time on the Internet: Timestamps*, RFC 3339, 2002. <https://www.rfc-editor.org/rfc/rfc3339>
5. Davis, K., Peabody, B., and Leach, P., *Universally Unique IDentifiers (UUIDs)*, RFC 9562, 2024. <https://www.rfc-editor.org/rfc/rfc9562>
6. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
7. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Addressing Cascading Failures*, Google, 2016. <https://sre.google/sre-book/addressing-cascading-failures/>
8. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Define a complete `OrderAccepted` event product, including fact, authority, identity, time, payload, delivery, ordering, service, protection, correction, ownership, and lifecycle.

### Exercise 2

Trace eight deliveries with three duplicate event IDs through a consumer. Design a durable idempotency boundary and explain retention, concurrency, crash, and replay cases.

### Exercise 3

Design partitioning, capacity, isolation, backpressure, dead-letter, replay, and observability for one million device events per minute with skewed devices and three consumers.

### Exercise 4

Compare event notification, event-carried state transfer, CDC, API lookup, and daily snapshot for Customer changes. Choose a mixed architecture for mobile, fraud, analytics, and archive consumers.

### Exercise 5

Plan migration from bilateral messages to governed event products across twenty producers and forty consumers. Include discovery, contracts, dual publication, semantic validation, rollback, correction, and retirement.

## Answers to the Exercises

### Answer 1

`OrderAccepted` records completion of the Order domain's acceptance decision, not an instruction. The domain is authoritative; order ID identifies the aggregate, event ID identifies this immutable publication, and policy version identifies the decision basis. Grain is one acceptance occurrence. Record business-effective time, source-observation time where different, publication time, timezone, precision, and clock limitations. The envelope includes source, type, subject, schema, correlation, causation, classification, and tenant only where needed. Payload fields define amounts, currency, status, nulls, codes, provenance, and limitations.

The contract declares source transaction and outbox behavior, per-order ordering, persistence and acknowledgement boundary, at-least-once duplicates, retention, expiry, replay, dead-letter, and bootstrap. Consumers make effects idempotent and report outcome lag. Service covers publication delay, availability, completeness, schema validity, consumer freshness, recovery, correction, and support. Protection covers publisher and subscriber identities, purpose, minimization, headers, payloads, regions, all retained copies, audit, deletion, and incidents. Corrections are new referenced events. Schema and semantic evolution use fixtures, consumer evidence, versions, notice, migration, and bounded retirement with accountable producer, platform, and consumer owners.

### Answer 2

Delivery deduplication uses stable event ID within source scope. A durable table stores consumer name, event ID, result, and processed time. In one transaction, the consumer checks or inserts the ID and applies its projection or outbox update. A duplicate returns the stored outcome without another effect. A unique constraint handles concurrent attempts. If the effect is external to that transaction, use an idempotent downstream business key or an outgoing transactional record plus reconciliation.

Retain IDs through the maximum redelivery and ordinary replay window for the protected effect. For older rebuilds, use a fresh projection or explicit replay epoch rather than assuming the live table suffices. Test crash before transaction, during work, after commit but before acknowledgement, and during duplicate concurrency. Record collisions and reject an ID reused with incompatible content. Three repeated IDs can be suppressed mechanically, but correctness also requires durable atomicity, business-effect scope, retention, and recovery evidence.

### Answer 3

One million per minute is about 16,667 events per second before replication, fan-out, and retries. Partition by device only if per-device order is required; hash distributes ordinary devices, while known hot devices may require bounded subkeys plus sequence reconciliation. Model event-size distributions, burst rate, three-way consumer fan-out, compression, broker replication, storage retention, network, validation, retry, and replay. Reserve critical consumer capacity and recovery headroom.

Use independent consumer groups, quotas, resource pools, per-topic or tenant limits, producer admission, finite retention, and alerts on event-time lag and storage. Backpressure or rejection behavior must reach producers; no consequential event is silently discarded. Invalid or repeatedly failing events go to a protected dead-letter workflow with reason, owner, retention, correction, replay, and closure. Replays use rate and byte limits, checkpoints, compatible code, and isolation from live traffic. Observe publication, acceptance, partition skew, hot keys, bytes, retry, duplicates, gaps, queue age, consumer processing and outcome lag, dead letters, replay, saturation, and telemetry loss.

### Answer 4

Notifications minimize data and tell the mobile client that state changed; the API supplies authorized current detail, with an explicit relationship between event position and read visibility. Fraud needs prompt facts and local state, so a minimized state-transfer event includes stable identifiers, relevant assertions, versions, time, ordering, and correction. Raw CDC can feed a controlled internal replication or derivation stage but should not become the cross-domain Customer contract because storage mutations lack durable meaning.

Analytics needs complete populations, history, joins, and reproducibility; use a governed daily snapshot or analytical product combined with incremental events. The archive needs versioned immutable evidence, manifests, checksums, provenance, retention, holds, and correction records. All products share source authority, identifiers, vocabulary, classification, quality, lineage, and consumer registration. The mixed architecture avoids placing every attribute in every event or forcing scans through an operational API.

### Answer 5

Assign stable producer, consumer, flow, fact, schema, route, credential, and owner identifiers. Discover bilateral messages from code, brokers, network records, schedulers, contracts, schemas, logs, traces, incidents, tickets, and interviews. Record purposes, facts, commands, source authority, consumers, keys, time, transformations, order, delivery, workload, service, protection, cost, versions, and observed confidence. Resolve unknown use through monitoring and accountable review.

Group reusable source facts into bounded event products; retain legitimate commands and consumer-specific derivations outside them. Define envelopes, payload semantics, schemas, identities, outbox or publication boundary, ordering, duplicates, idempotency, retention, replay, dead letters, correction, service, protection, ownership, and lifecycle. Introduce adapters, dual publication, consumer registrations, and end-to-end telemetry as seams. Migrate cohorts with one named authoritative path and deduplicated effects. Compare values, keys, grain, time, order, gaps, duplicates, errors, service, protection, and consumer decisions; test rollback and correction.

After acceptance, stop old publishers and subscriptions, revoke identities and network paths, remove routes, schemas, connectors, queues, copies, alerts, providers, and fallback jobs, update catalogs and lineage, preserve required history and holds, and verify inactivity. Measure known consumers, contract reuse, lag, incidents, schema changes, replay, correction, migration, and closure rather than only message volume.
