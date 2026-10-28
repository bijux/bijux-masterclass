---
module_id: PLAT-044
program: Platform Engineering
level: 1
module_number: 44
title: Event-Driven Workload Templates
status: complete
last_verified: 2026-09-02
---

# Event-Driven Workload Templates

## One-Page Review

### Governing question

How should a platform turn event-producer, subscription, and consumer intent into maintained workload paths that preserve event meaning, tolerate redelivery, respect ordering and leases, scale from useful signals, quarantine poison work, support safe replay, and retire every destination and effect without claiming transport-level exactly-once business outcomes?

### Essential definitions

- An **occurrence** is a fact or state transition in a source domain; an **event** is an immutable record describing that occurrence and its context.
- A **message** is a transport envelope carrying one or more events through a protocol or broker; message identity and event identity need not be identical.
- A **delivery** is one broker-to-consumer presentation of a message; the same message or event can have several deliveries and processing attempts.
- A **producer contract** defines event meaning, identity, schema, publication boundary, compatibility, security, and support.
- A **subscription contract** defines source/destination, selection, consumer ownership, delivery, ordering, acknowledgement, retry, replay, capacity, security, and lifecycle.
- A **consumer template** is a versioned platform product that instantiates a supported event-processing archetype, not merely a Deployment plus broker credentials.
- **settlement** is the protocol action that accepts, rejects, releases, negatively acknowledges, or otherwise changes broker delivery state.
- A **visibility or acknowledgement lease** is a bounded interval in which a consumer is expected to process or extend ownership before redelivery becomes possible.
- A **poison event** is validly delivered work that repeatedly fails deterministically for the current consumer; a **dead-letter destination** is quarantine, not resolution.
- **replay** is deliberate re-delivery from retained history or quarantine under an explicit scope, revision, effect, capacity, and audit contract.

### Central model, mechanism, or theorem

Let occurrence $o$ produce event $e=(s,i,t,v,d)$ with source $s$, source-scoped identifier $i$, type $t$, schema revision $v$, and data $d$. Broker state may produce deliveries $\delta_1,\ldots,\delta_m$, each with processing attempts. Consumer effect function $F(e,k)$ uses domain operation key $k=h(s,i,c)$ for consumer contract $c$. At-least-once transport permits $m\geq1$; safe accepted effects require an idempotent/fenced $F$, a transaction that couples effect and progress, or reconciliation before settlement. Envelope conformance, broker acknowledgement, offset commit, and effect acceptance are distinct evidence.

### Critical invariants

- Event identity names a source fact; message, delivery, attempt, trace, correlation, partition, and consumer-effect identities remain distinct and correlatable.
- Producers publish immutable facts after a defined commit boundary; consumers do not interpret mutable command state as historical fact without a version/snapshot contract.
- Schema, semantic meaning, owner, compatibility, privacy, retention, and deprecation are governed independently of topic or queue creation.
- Duplicate and out-of-order delivery are assumed unless the complete producer-broker-consumer-effect path proves a narrower scope.
- Acknowledgement or offset commit occurs only at the boundary consistent with durable effect/recovery; early settlement can lose work and late settlement can repeat it.
- Ordering guarantees have an explicit scope, normally a partition/key, and consumers preserve or deliberately relax that scope.
- Visibility/lease duration, heartbeat/extension, shutdown, rebalance, and retry behavior cover worst-case processing without permitting unbounded stuck ownership.
- Backlog age and arrival/service rates govern scaling; queue depth or CPU alone cannot prove deadline health.
- Parallelism is bounded by partitions, downstream capacity, ordering, quota, and safe in-flight work—not only available replicas.
- Poison work has bounded attempts, classification, quarantine ownership, alerting, repair, replay, retention, and privacy controls.
- Replay uses explicit event range and consumer/effect revision; it is never an unreviewed “send all again” operation.
- Event infrastructure, subscriptions, credentials, retained data, quarantine, schemas, telemetry, and accepted external effects each have retirement ownership.

### Common failures

Calling every message an event; generating random event IDs on retry; publishing before the source transaction commits; dual-writing a database and broker without outbox/reconciliation; acknowledging before the effect; assuming a broker’s exactly-once feature covers an external API; ordering globally when only per partition exists; changing a partition key silently; scaling on CPU while oldest-message age grows; scaling beyond partition or database capacity; allowing leases to expire mid-effect; terminating consumers without drain; retrying invalid schemas forever; using dead-letter count as resolution; replaying with new non-idempotent logic; logging sensitive payloads; treating CloudEvents conformance as schema compatibility; and deleting a topic while subscriptions, quarantine, credentials, lineage, or legal retention remain.

### Compact example

An orders service commits order `8842` and an outbox row in one database transaction. A relay publishes immutable CloudEvent `(source=/commerce/orders, id=8842-confirmed-7, type=com.example.order.confirmed.v1)` and marks the outbox row only after broker confirmation. A payment consumer group partitions by customer, validates the pinned schema, and derives effect key from event source/id plus consumer contract. It records an inbox claim and payment request atomically where possible, calls a provider with the same idempotency key, reconciles ambiguous timeouts, then commits its broker progress. Redelivery returns the prior accepted result. Backlog age drives capacity within partition and provider limits. Invalid events quarantine after bounded attempts with owner and repair workflow. Replay selects an audited range and preserves original event IDs.

### Connections

This module specializes the asynchronous consumer archetype from [PLAT-041](041-workload-archetypes.md), applies the general creation/evolution contract from [PLAT-042](042-service-templates.md), and distinguishes continuously running consumers from event-triggered Jobs in [PLAT-043](043-batch-and-scheduled-workload-templates.md). It composes runtime, scheduling, configuration, secret, connectivity, observability, and data-access capabilities from earlier platform modules.

## Governing Question

What maintained platform contract can connect an owned event producer to one or more owned consumers while making fact identity, schema, delivery, processing, effects, scaling, recovery, and retirement explicit across broker and application boundaries?

An event-driven path is not “choose a topic and deploy a worker.” A broker can durably store bytes, route them, and track delivery progress, yet know nothing about whether the bytes describe a true occurrence, whether the schema is compatible, whether a payment was charged, or whether replay is safe.

The platform must standardize the repeated infrastructure and operational mechanics without erasing domain semantics. It can provision destinations, identities, policies, telemetry, autoscaling, retry routes, schema checks, and lifecycle automation. Producer and consumer owners still define facts, effect correctness, ordering needs, reconciliation, and business acceptance.

The contract spans three products: producer publication, broker/subscription, and consumer processing. A complete golden path composes all three and exposes their independent state. Optimizing one boundary while leaving the others implicit moves rather than removes failure.

## Why This Matters

Events decouple availability and time. A producer may complete without waiting for every consumer, and consumers may process at different rates or be added later. That flexibility creates retained obligations: schemas must remain interpretable, replay must remain safe, and ownership cannot disappear when the producing request ends.

Delivery is intentionally repeatable in many systems. Amazon SQS standard queues document at-least-once delivery; Kafka distinguishes publishing and consuming guarantees; JetStream consumers track acknowledgements and redelivery. These mechanisms protect against loss under failures by permitting duplicates. Application effects must therefore tolerate repetition.

Ordering is local and costly. A partitioned log can order records within a partition, but adding partitions, changing keys, retrying through another destination, or processing concurrently can change observed order. Requiring global order reduces throughput and availability; omitting necessary entity order corrupts state.

Autoscaling can amplify harm. More consumers may increase throughput, but they can also trigger rebalances, exhaust database pools, violate API quotas, or multiply an event storm. Backlog count lacks age, arrival rate, item cost, partition distribution, and downstream health.

Events also carry data beyond the source system. Payloads, headers, dead-letter copies, broker retention, logs, traces, and replay archives can extend privacy and security exposure. A self-service path needs classification, minimization, encryption, authorization, residency, retention, erasure, and audit at every copy.

## Prerequisites and Retrieval

Retrieve immutable records, transactions, write-ahead logs, commit boundaries, message brokers, queues and logs, publish/subscribe, consumer groups, partitions, acknowledgements, offsets, visibility leases, redelivery, at-most-once and at-least-once delivery, idempotency, deduplication, inbox/outbox, sagas, reconciliation, ordering, causality, schema evolution, JSON Schema or equivalent, API contracts, backpressure, queueing theory, autoscaling, graceful shutdown, network partitions, observability, tracing context, authentication, authorization, encryption, data classification, retention, privacy deletion, supply-chain provenance, incident response, and platform product lifecycle.

You should distinguish occurrence from event; event from command; event from message; event ID from message ID; delivery from processing attempt; correlation from causation; ordering from consistency; acknowledgement from business commit; retry from replay; quarantine from resolution; schema compatibility from semantic compatibility; topic retention from domain retention; queue depth from backlog age; replica count from useful concurrency; broker exactly-once scope from end-to-end effect uniqueness; and infrastructure deletion from lifecycle completion.

## Learning Objectives

After completing this module, you should be able to:

1. specify producer, event, destination, subscription, and consumer contracts as separate maintained products;
2. model occurrence, event, message, delivery, attempt, progress, and effect identities;
3. place acknowledgement/offset commit relative to durable effects and ambiguous outcomes;
4. design idempotency, inbox/outbox, fencing, transactions, and reconciliation for redelivery;
5. define partition keys, ordering scope, consumer groups, rebalances, and graceful drain;
6. size and autoscale consumers using backlog age, arrival/service rates, partitions, downstream limits, and cost;
7. govern invalid and poison events through bounded retry, quarantine, repair, and replay;
8. establish schema, semantic, security, observability, retention, and compatibility controls; and
9. test, migrate, deprecate, and retire event-driven paths without orphaning retained obligations.

## Core Exposition

### Begin with occurrences and responsibilities

Ask what happened in the source domain, who is authoritative for that fact, and at which commit boundary it becomes publishable. “Order confirmed” is a fact after the order authority commits confirmation. “Confirm this order” is a command asking an owner to act. Treating commands as facts confuses authority, retry, and failure reporting.

Identify producer owner, event-type owner, broker/destination owner, subscription owner, consumer owner, schema owner, data steward, security owner, and support escalation. One team may fill several roles, but the contract should not assume it.

Define the user outcome. It might be “publish an owned fact with durable confirmation,” “process every eligible order within five minutes,” or “add an independently replayable analytics consumer.” Topic creation is an intermediate resource, not the outcome.

List non-guarantees. Publication does not prove every consumer processed; delivery does not prove a unique attempt; acknowledgement does not prove an external effect unless the consumer contract makes it so; schema validity does not prove truth; trace correlation does not prove causal order.

### Model occurrence, event, message, and delivery

An occurrence belongs to the domain. An event is an immutable representation of it. CloudEvents 1.0.2 defines a vendor-neutral event format and requires `id`, `source`, `specversion`, and `type`; the combination of source and ID identifies distinct events under the producer contract.

A message is how an event traverses a protocol. One message may wrap one event, batch several, or add broker metadata. Gateways may re-encode it. Do not replace stable event identity with broker-specific message identity during a bridge.

A delivery is a presentation to a consumer. It has broker destination, subscription/group, partition or shard, offset/sequence where applicable, delivery attempt, lease, and settlement state. Processing adds consumer revision, effect key, trace, timestamps, and outcome.

Preserve all identities in telemetry without using high-cardinality event IDs as unrestricted metric labels. Event IDs belong in scoped traces, logs, inbox records, or sampled exemplars; metrics aggregate by owned low-cardinality dimensions.

### Write a producer contract

Specify event type and version, semantic description, source, identity construction, occurrence time, publication time, subject/key, schema, examples, field classification, owner/support, commit boundary, publication mechanism, delivery expectation, retention assumption, volume/burst, compatibility, deprecation, and incident behavior.

Event IDs must be stable across publish retries. Creating a fresh UUID after a timeout makes one occurrence appear as several distinct events and defeats consumer deduplication. If the source naturally has an aggregate ID and revision, combine them under an explicit namespace.

State whether the event is a notification with references, a full state snapshot, or a delta. References minimize payload but couple consumers to source availability and authorization. Snapshots improve temporal independence but increase size and privacy copies. Deltas are compact but require ordered complete history or repair snapshots.

Do not claim ownership of consumer outcomes. A producer guarantees what it can observe: source commit, outbox durability, publish confirmation, schema, and support. Consumer completion needs separate status or reconciliation.

### Couple source commit and publication

Writing a database then publishing separately creates two failure windows: the transaction commits but no event publishes, or the event publishes but the transaction rolls back. Reversing the order only swaps which inconsistency appears.

The transactional outbox records the source mutation and publish intent in the same local transaction. A relay publishes the event with stable identity and marks progress after broker confirmation. Relay retries can duplicate publication, so consumers still need duplicate safety or the broker must deduplicate within an explicit bounded scope.

Change-data capture can derive events from a database log and reduce application relay work. It exposes storage representation, ordering, schema, filtering, and operational coupling; translating change records into stable domain events still needs ownership.

Some brokers and databases support transactions across a bounded broker workflow. Use them where the entire effect and progress remain in that supported transaction. Do not extrapolate a Kafka read-process-write transaction to a payment provider, email service, or unrelated database.

Monitor outbox age, relay lag, failed publication, unknown confirmation, duplicate rate, schema rejection, and source-to-broker latency. A healthy producer process with a stuck outbox is not a healthy publication path.

### Define the event envelope and schema

Adopt a stable envelope such as CloudEvents when interoperability benefits justify it. Required context supports identity, source, type, and spec version; optional time, subject, data content type, and data schema improve routing and interpretation.

Envelope standardization is not the domain schema. Govern payload schemas by immutable identifiers or versioned references, compatibility rules, fixtures, and ownership. Validate at production and consumption boundaries appropriate to risk without turning every consumer into a network-dependent registry client.

Separate syntactic from semantic compatibility. Adding an optional field can be structurally backward compatible while changing the meaning of an existing status. Reusing a field with new units or changing whether omission means zero is breaking even if validation passes.

Prefer additive evolution, stable meanings, explicit defaults, tolerant readers within policy, and new event types for incompatible semantics. Avoid unbounded “metadata” maps that evade classification and compatibility.

AsyncAPI can describe channels, operations, messages, schemas, servers, and bindings for asynchronous APIs. Treat a checked contract as useful design and tooling input, not proof that deployed producers, brokers, and consumers conform.

### Write the subscription contract

Specify subscribed event types and revisions, source/destination, filter, consumer group or fan-out identity, partition/key behavior, starting position, acknowledgement/offset rule, lease and extension, batch size, concurrency, ordering, retry/backoff, terminal classification, quarantine, replay, retention assumptions, throughput and latency SLO, scaling, shutdown, security, telemetry, owner, and retirement.

A competing-consumer queue gives one logical subscription work sharing across instances. Publish/subscribe fan-out gives independent subscription state per consumer. Do not make unrelated consumers share one group merely to reduce broker objects; they will divide rather than each receive events.

Filter ownership matters. Broker-side filtering saves bandwidth and compute but may hide events needed after a rule change. Consumer-side filtering preserves a broad stream but transfers cost and data access. Version and audit filters, and define what happens to previously excluded history.

Starting position—new only, earliest retained, timestamp, explicit offset, or imported checkpoint—is a business decision. Defaulting incorrectly can silently skip history or trigger a production-scale replay.

### Place settlement after the correct boundary

At-most-once behavior can arise when progress is committed before processing: a crash loses work but avoids redelivery. At-least-once arises when progress is committed after processing: a crash after effect but before progress can repeat the effect.

There is no universally correct acknowledgement point. For a cache refresh, duplicate work may be harmless and late acknowledgement is appropriate. For a non-idempotent external charge, the consumer needs an idempotency key or authoritative reconciliation before acknowledging.

For a transactional local database, an inbox row keyed by event/effect identity can be committed with the domain change. A duplicate sees the inbox result. Broker acknowledgement follows the transaction; if acknowledgement is lost, redelivery returns the stored result.

For an external service, pass the same consumer-effect key when it enforces idempotency. On timeout, query by that key. If the result cannot be determined, quarantine the processing state as ambiguous and stop automatic replay.

Auto-commit based only on elapsed time can advance progress for records still in memory or being processed. A platform template should default to explicit progress aligned with the application contract and test crash points around effect and settlement.

### Treat exactly once as a scoped claim

At-most-once, at-least-once, and exactly-once describe boundaries and failure assumptions, not marketing adjectives for an entire system. Ask: exactly once for which record, which state, within which broker/store, under which transaction and retention, and visible to whom?

Kafka documents exactly-once support for Kafka Streams and transactional read-process-write flows on Kafka topics with appropriate consumer isolation. This does not automatically include external databases, APIs, files, notifications, or human actions.

“Effectively once” commonly means transport can redeliver but accepted domain effects converge to one through stable identity, deduplication, idempotency, fencing, transactions, or reconciliation. State the mechanism and retention window; never use the phrase without them.

Deduplication has memory. If inbox keys expire after seven days, a later replay can repeat effects. Bind deduplication retention to maximum broker retention, quarantine retention, replay horizon, and business correction policy.

### Define ordering and partitioning

Determine the smallest domain scope requiring order: per account, device, aggregate, workflow, or partition. Global order is rarely necessary and constrains availability and throughput.

Choose a stable partition key from that scope. Every producer for the event type must apply the same canonicalization and hashing/binding rules. A null or malformed key must have explicit rejection or fallback behavior.

Partition order is not causal truth across event types or sources. Use aggregate revisions, expected predecessor, vector/logical mechanisms where warranted, or state reconciliation when consumers observe gaps or inversions.

Increasing partitions may change key placement depending on the broker/partitioner. Changing partition count, hash algorithm, or key semantics is a compatibility migration, not a routine capacity edit.

Consumers should process one ordered key serially where required while allowing concurrency across independent keys. Batch APIs and async handlers can accidentally reorder completion even if poll order is stable.

### Own leases, heartbeats, rebalances, and drain

Visibility or acknowledgement timeout must exceed normal processing or be safely extended. Too short causes concurrent redelivery while the first worker still acts; too long delays recovery after failure. Extensions need a cap and progress evidence so a stuck worker cannot hide work forever.

Consumer groups redistribute partitions when members join, leave, fail, or subscriptions change. Rebalance handling stops acquisition, finishes or aborts in-flight work according to lease, commits safe progress, releases ownership, and fences stale workers.

Shutdown begins by stopping new receives or pausing partitions. It waits within a bounded grace period for effects and settlement, extends leases when appropriate, checkpoints progress, then exits. Readiness becomes false before capacity is removed.

Autoscaling and rolling deployment can cause rebalance churn. Stabilization windows, cooperative protocols where supported, maximum in-flight work, and rollout surge constraints should be tuned with processing time and partition count.

Push consumers need equivalent admission and acknowledgement semantics through request deadlines, response codes, authentication, retry headers, and concurrency limits. Returning success before durable effect loses work; timing out after commit can redeliver.

### Classify retry and poison work

Classify decode/schema failure, unauthorized data, unsupported version, transient dependency, rate limit, lease loss, deterministic domain rejection, conflicting order, consumer defect, and ambiguous effect. A generic exception is insufficient policy input.

Retry transient failures with exponential backoff and jitter, respecting broker lease and downstream retry advice. Cap attempts, elapsed time, and in-flight concurrency. Immediate retry storms can extend an upstream outage into platform saturation.

A poison event repeatedly fails for the current contract. Move it to quarantine only after preserving original event identity, source destination/partition/offset, schema, failure class, attempt history, consumer revision, trace, and restricted payload or reference.

A dead-letter queue is an operational work queue. It needs owner, SLO, alert, access control, dashboards, inspection/redaction tooling, repair decision, replay or discard approval, retention, privacy deletion, and evidence. Merely counting it transfers toil invisibly.

Separate invalid producer data from consumer defects. Producers should receive conformance feedback and stop emitting invalid types; consumers should not normalize arbitrary corruption silently.

### Make replay a governed operation

Define replay source, exact range/filter, original event identities, destination or shadow destination, consumer revision, effect mode, dry-run behavior, rate/concurrency, downstream limits, authorization, approval, observability, abort, result, and audit.

Replay can recompute state, repair missed effects, validate a new consumer, or migrate a projection. Those goals have different safety. A shadow projection may accept duplicate reads; re-sending customer notifications is rarely acceptable.

Preserve occurrence time and original identity. Add replay execution context separately. Rewriting event IDs makes deduplication fail; rewriting occurrence time changes domain meaning.

Run compatibility and effect analysis before replay. Old payloads may not satisfy a new schema reader, and new consumer logic may interpret them differently. Pin a compatible consumer or perform an explicit versioned transformation with lineage.

Throttle by downstream capacity and monitor oldest replay age separately from live traffic. Prefer separate capacity, priority, or destination when replay could violate live-event SLOs.

### Scale from work and constraints

Let backlog be $B$, arrival rate $\lambda$, effective per-consumer service rate $\mu$, and active consumers $n$. Under an ideal stationary model with $n\mu>\lambda$, approximate drain time without new arrivals is $B/(n\mu)$; with arrivals it is

$$
T_{drain}\approx\frac{B}{n\mu-\lambda}.
$$

The denominator shows the instability boundary: if $n\mu\leq\lambda$, backlog does not drain. Variance, partitions, batching, retries, rebalances, downstream saturation, and heterogeneous event cost make this a sizing model, not a guarantee.

Backlog age directly reflects user waiting and detects a low-count expensive message. Track count, oldest age, arrival rate, completion rate, processing duration, retry/quarantine, partition skew, in-flight leases, and downstream saturation.

Maximum useful replicas are bounded by assigned partitions or queue concurrency, downstream connection/API limits, resource quota, safe in-flight effects, cost, and shutdown recovery. Scaling beyond that adds churn or overload.

KEDA can translate supported event-source signals into scaling for Deployments, StatefulSets, custom resources, or Jobs. Activation threshold governs moving from zero; scaling threshold influences replica count. These are control mechanisms, not proof of correct acknowledgement, ordering, effect, or deadline.

Scale-to-zero requires durable buffering, acceptable activation latency, credential/config availability, cold-start capacity, and a scaler that can observe demand. Keep minimum capacity when latency, leases, partition ownership, or control-plane failure makes zero unsafe.

### Apply backpressure end to end

Consumers limit poll/receive batch, in-flight messages, concurrent handlers, downstream calls, memory, and retry concurrency. Pausing acquisition is often safer than accumulating unbounded local work whose leases expire.

Producers need quotas, bounded buffers, publish timeouts, and explicit behavior when the broker is unavailable. Dropping, blocking, local spooling, or rejecting source requests have different domain consequences.

Event storms can originate from retry loops, feedback cycles, mass state changes, schema defects, or replay. Detect rate changes by source/type/tenant and offer circuit breakers or quarantine without discarding evidence.

Prevent feedback loops by defining causal lineage and rate budgets. A consumer that emits an event which triggers itself needs a terminating state transition or deduplication rule, not only autoscaling.

Capacity tests must include skewed keys, large payloads, slow dependencies, poison events, rebalances, broker throttling, and recovery surge—not just uniform steady-state messages.

### Secure event paths

Authenticate producers, consumers, platform controllers, schema tooling, replay operators, and quarantine inspectors separately. Authorize publish, subscribe, group membership, offset reset, destination management, schema registration, quarantine access, replay, and deletion.

Use workload identities and narrowly scoped short-lived credentials. A consumer should read only required destinations and write only its output/effect resources. The scaler may need read-only metrics rather than payload access.

Classify context attributes and payload fields. Minimize personal, regulated, tenant, and secret data; prefer references when temporal coupling and authorization can be managed. Encrypt in transit and at rest, and consider field-level protection for mixed audiences.

Broker ACLs do not replace application authorization. An event asserting `tenant_id` is untrusted unless the producer authority and integrity bind it. Validate source, signature where required, schema, tenant, and subject before effect.

Prevent payloads and credentials from leaking through logs, trace attributes, error text, dead-letter copies, metrics labels, dashboards, or support tickets. Provide controlled inspection and redaction workflows.

### Observe the complete path

Correlate source transaction/outbox, publish attempt, broker destination, event identity, delivery, consumer group/partition/offset, processing attempt, effect key, settlement, quarantine, replay, and result. Keep sensitive and high-cardinality values out of broad telemetry.

OpenTelemetry messaging semantic conventions distinguish create, send, receive, process, and settle operations and use span links for message contexts in fan-out and batch scenarios. The current messaging conventions are marked development; pin emitted versions and plan migration rather than treating attribute names as timeless.

Metrics include publication success/unknown, outbox age, broker ingress/egress, retention headroom, consumer lag/count/age, arrival and completion rates, processing latency, lease extension/loss, retry, quarantine, replay, partition skew, rebalance, effect ambiguity, and cost.

Alert on user outcomes: oldest eligible event exceeds SLO, no feasible drain capacity, producer outbox stale, retained history near loss before recovery, repeated poison class, ambiguous effect, quarantine unowned, replay harming live traffic, and deletion/retirement incomplete.

Trace continuity is evidence for diagnosis, not delivery or causality proof. Sampling must retain errors and representative slow/duplicate/replay paths without storing prohibited payloads.

### Test contracts and failure windows

Test producer identity stability, source transaction/outbox crash points, publish timeout, duplicate publication, envelope/schema, incompatible semantics, authorization, payload limits, broker unavailability, and outbox recovery.

Test consumers with duplicate and reordered delivery, gaps, partition skew, lease expiry, acknowledgement loss, crash before effect, crash after effect before settlement, ambiguous external result, rebalance, rolling shutdown, scale up/down, invalid schema, poison event, quarantine outage, and downstream throttling.

Replay tests use retained old fixtures, deduplication near and beyond its window, shadow effects, abort/resume, rate controls, and live-traffic isolation. Privacy tests find all copies and prove deletion or justified retention.

Contract tests validate AsyncAPI/schema artifacts and representative broker bindings, but integration tests exercise real identity, ACL, partition, transaction, lease, and settlement behavior. Fault injection locates the exact failure windows that mocks conceal.

Conformance is current evidence over producer, event types, broker policy, subscriptions, consumer revision, effect mechanism, telemetry, and lifecycle. Generated repository ancestry does not prove it.

### Design template outputs

A producer path creates or binds catalog identity, source/event contracts, schema artifacts, outbox/relay capability where selected, least-privilege publisher identity, destination binding, telemetry, tests, support, and deprecation metadata.

A consumer path creates or binds subscription identity, selected event contracts, group/fan-out mode, starting position, ordering key, settlement adapter, inbox/effect mechanism, retry/quarantine, scaling profile, graceful drain, telemetry, runbook, cost, tests, and retirement handle.

Generate minimal domain entry points and maintained libraries/workflows. Broker clients are subtle; reusable adapters can implement envelope validation, context propagation, bounded polling, settlement, redaction, and metrics while leaving effect boundaries explicit to application code.

Do not generate one template per broker, language, team, or topic if controlled provider/runtime adapters can satisfy the same archetype. Split only when semantic behavior, security boundary, or lifecycle differs materially and is tested.

Make unsupported combinations explicit: global total order, arbitrary unreviewed images, unbounded retention, raw secret parameters, non-fenced non-idempotent replay, host-level brokers, or a payload/classification the platform cannot protect.

### Retain, migrate, and retire every obligation

Inventory producers, event types/revisions, schemas, destinations, partitions, subscriptions/groups, offsets/checkpoints, quarantine, replay archives, identities, keys, ACLs, dashboards, runbooks, consumers, effects, owners, and retention.

Schema and semantic deprecation accounts for the longest retained/replayable event plus consumer migration. Removing an old reader while old events remain makes recovery fail precisely when needed.

Destination migration can dual-publish or bridge, but both create duplicate and ordering risks. Use stable event identity, reconciliation, observed cutover, bounded compatibility, and rollback evidence. Never silently reset consumer progress.

Retirement stops new producers or routes them to the replacement, drains outbox, inventories retained events and legal obligations, migrates/ends subscriptions, resolves quarantine and ambiguous effects, disables replay, revokes credentials/ACLs, removes telemetry last, deletes data by policy, and preserves audit evidence.

Deleting a topic does not undo accepted consumer effects. Domain owners retain responsibility for compensating, correcting, or retaining those outcomes.

### Operate the portfolio as a platform product

Catalog template revisions, broker adapters, supported delivery/ordering profiles, event contracts, consumers, SLOs, costs, exceptions, dependencies, conformance, incidents, and deprecation. Provide discovery by domain meaning rather than raw destination names.

Measure source-to-accepted-effect latency, deadline success, duplicate-effect prevention, outbox and quarantine age, recovery/replay time, safe schema adoption, user effort, support load, cost, and retirement completion. Topic and message counts alone do not measure value.

Canary new runtime libraries, settlement adapters, scaler rules, schema policies, and broker versions with controlled producers/consumers. Preserve recovery for in-flight and retained old events during rollback.

The following executable inventory is synthetic review evidence. It counts declared contract controls and does not prove source truth, broker durability, effect idempotency, end-to-end ordering, schema meaning, autoscaling stability, privacy compliance, or production reliability.

<!-- bijux-verify: {"id":"event-template-control-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"paths 10\nevent_identity_schema 10\npublication_atomicity 9\nsettlement_effect 9\nordering_partition 8\nretry_quarantine 9\nreplay_governed 8\nscaling_backpressure 9\nsecurity_observability 9\nretirement_owned 8\n","stderr":""}} -->
```python
paths = [
    ("order-events", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("payment-consumer", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("inventory-projection", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("device-telemetry", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("notification-fanout", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("fraud-stream", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("audit-sink", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("legacy-queue", 1, 1, 1, 0, 1, 1, 1, 1, 0),
    ("partner-webhook", 1, 1, 1, 1, 1, 0, 1, 1, 1),
    ("experimental-feed", 1, 0, 0, 0, 0, 0, 0, 0, 0),
]
fields = [
    "event_identity_schema", "publication_atomicity", "settlement_effect",
    "ordering_partition", "retry_quarantine", "replay_governed",
    "scaling_backpressure", "security_observability", "retirement_owned",
]
print("paths", len(paths))
for index, field in enumerate(fields, start=1):
    print(field, sum(row[index] for row in paths))
```

## Definitions and Notation

Let occurrence $o$ be represented by event $e=(s,i,t,v,d)$: source $s$, source-scoped ID $i$, event type $t$, schema/semantic revision $v$, and data $d$. CloudEvents duplicate identity is the pair $(s,i)$ under its producer contract.

Let transport message $m$ carry event set $E(m)$ plus protocol metadata. A delivery $\delta=(m,g,p,q,a,\ell)$ includes consumer group/subscription $g$, partition $p$, position $q$, delivery attempt $a$, and lease/settlement state $\ell$.

For consumer contract $c$, effect key $k=h(s,i,c)$ scopes deduplication to the event and intended consumer effect. Effect state $X(k)$ may be absent, pending, committed, rejected, or unknown. Settlement is safe only when it agrees with the recovery policy for $X(k)$.

Let backlog $B$, arrival rate $\lambda$, effective per-consumer service rate $\mu$, and consumers $n$ yield the ideal drain model $T_{drain}\approx B/(n\mu-\lambda)$ for $n\mu>\lambda$. Partition count $P$, downstream concurrency $D$, quota capacity $Q$, and effect safety bound $S$ imply useful concurrency $n\leq\min(P,D,Q,S)$ for a partition-bound consumer.

Let replay $R=(A,Z,c',r,L)$ select event range/filter $A$, target $Z$, consumer revision $c'$, effect mode $r$, and limits $L$. It is a new governed execution over original event identities, not new occurrences.

## Mechanisms, Invariants, or Proof Structure

The event-path assurance chain is:

1. define an authoritative occurrence, producer commit boundary, stable event identity, semantic/schema contract, owner, and non-guarantees;
2. couple source state and publication through an outbox, bounded transaction, CDC contract, or explicit reconciliation;
3. provision a destination and subscription whose fan-out, filter, partition, start, delivery, lease, retry, retention, and security semantics match the consumer;
4. validate envelope/schema/source and derive a stable consumer-effect identity before processing;
5. commit idempotent/fenced/transactional effects or reconcile ambiguous outcomes before settlement;
6. preserve required key ordering, bounded in-flight work, safe rebalance, graceful drain, and observable progress;
7. scale from backlog age and rates within partition, downstream, quota, effect, and cost bounds;
8. classify failures, bound retry, quarantine poison work with ownership, and repair or discard explicitly;
9. replay only an authorized range under pinned compatible logic, preserved identities, isolated capacity, audited effects, and abort/recovery; and
10. test, observe, migrate, deprecate, drain, revoke, delete, and retain every producer, event, destination, subscription, consumer, quarantine, and effect obligation.

The duplicate-safety argument is conditional: if retries preserve $(s,i)$, consumer $c$ derives the same $k$, authoritative effect storage makes repeated $F(e,k)$ return or converge to one accepted result, unknown outcomes are reconciled, and settlement follows durable state, then repeated deliveries do not require repeated accepted effects. Broker delivery alone proves none of these premises.

The invariants are identity separation, commit-bound publication, governed meaning/schema, duplicate and reorder tolerance, effect-aligned settlement, scoped ordering, bounded leases/drain, outcome-based scaling, capacity-bounded concurrency, owned poison repair, governed replay, and complete retirement.

## Alternatives and Trade-Offs

**Notification versus snapshot versus delta:** notifications minimize data but couple consumers to source reads. Snapshots decouple time but copy data. Deltas are efficient but demand complete ordered history and repair.

**Transactional outbox versus CDC versus direct publish:** outbox gives application-owned intent and local atomicity with relay lag. CDC reduces application code but couples to storage logs. Direct publish is simple but needs an explicit dual-write recovery story.

**Queue versus pub/sub log:** a queue naturally shares work among consumers and may remove acknowledged messages. A retained log supports independent groups and replay but requires partition/offset and retention governance.

**Pull versus push:** pull gives consumers control over batching and backpressure. Push reduces polling and can suit webhooks/serverless handlers, but receiver deadlines and responses become lease/settlement signals.

**Early versus late acknowledgement:** early acknowledgement reduces duplicates but risks loss. Late acknowledgement avoids loss under recoverable failure but repeats effects unless they are safe.

**Broker transaction versus inbox/idempotency:** broker transactions can provide strong semantics inside one supported ecosystem. Inbox/idempotency extends across application stores but adds state, retention, and reconciliation.

**Per-entity ordering versus maximum throughput:** ordered keys simplify state transitions but serialize hot entities. Relaxing order improves concurrency only when consumers can reconcile versions or operations commute.

**Broker-side versus consumer-side filtering:** broker filtering saves capacity and exposure. Consumer filtering retains future flexibility but sends more data and cost to the consumer.

**Long-running consumer versus event-triggered Job:** long-running consumers reuse connections and manage partitions efficiently. Jobs isolate expensive bounded work but add startup, Job churn, and separate acknowledgement coordination.

**Retry topic versus delayed broker redelivery:** retry topics expose stages and free leases but can alter ordering and duplicate metadata. Native delay preserves destination semantics but may hold capacity or offer limited policies.

**Dead-letter versus pause-in-place:** quarantine keeps healthy traffic moving but creates another sensitive queue and can reorder repair. Pausing preserves position/order but blocks the partition and SLO.

**Replay in place versus shadow projection:** in-place replay repairs production effects but carries high duplicate risk. Shadow processing supports comparison and migration while doubling data/capacity and requiring cutover.

## Failure Modes and Misconceptions

- **“An event is any asynchronous payload.”** commands, facts, snapshots, deltas, and transport messages have different authority.
- **“CloudEvents guarantees delivery.”** it standardizes event representation, not broker or effect semantics.
- **“A valid schema means a true fact.”** structural validation cannot prove domain truth.
- **“A new UUID per retry is safer.”** it destroys duplicate identity for one occurrence.
- **“Publish after database commit is atomic enough.”** a crash between them loses publication without outbox/reconciliation.
- **“Broker acknowledgement means the customer outcome occurred.”** settlement and business effect are different systems.
- **“Exactly once applies end to end.”** claims are scoped to named transactions, stores, and failure assumptions.
- **“Deduplication works forever.”** key retention bounds replay safety.
- **“One topic preserves global order.”** partitions, consumers, bridges, retries, and concurrency narrow order.
- **“Adding partitions is operational only.”** it can change key placement and observed order.
- **“Consumer groups broadcast events.”** instances in one group normally share work rather than each receiving it.
- **“Visibility timeout locks the effect.”** the first consumer can still act after lease loss.
- **“Auto-commit reflects completed processing.”** buffered records may not have durable effects.
- **“More replicas always reduce lag.”** partitions, downstream capacity, rebalances, and skew cap useful concurrency.
- **“CPU is the event autoscaling signal.”** idle-looking consumers can have old backlog while blocked downstream.
- **“Dead-lettering resolves poison work.”** it only moves ownership and retention.
- **“Replay is just resetting an offset.”** effect, version, capacity, privacy, and audit decisions remain.
- **“Trace parentage proves causation.”** propagation provides correlation evidence, not domain causal proof.
- **“Deleting the topic deletes the data.”** replicas, archives, DLQs, logs, traces, and effects may remain.
- **“Template ancestry proves current safety.”** current contracts, policies, consumers, and retained events need conformance evidence.

## Worked Examples

### Example 1

An order service commits an order, then crashes before direct publish. No consumer learns of the order. A transactional outbox commits source change and stable event intent together; a relay retries publication and tracks confirmation. Conclusion: local atomicity plus retry closes the missing-event window, while duplicate-safe consumers close the repeated-publish window.

### Example 2

The relay times out and creates a new event UUID on retry. Consumers see two distinct facts and send two emails. Reusing `(source, id)` for the original occurrence lets a notification inbox return the prior effect. Conclusion: event identity follows the occurrence, not the publish attempt.

### Example 3

A payment consumer charges an external provider and crashes before acknowledging. Redelivery charges twice. It instead derives `payment-consumer/<source>/<event-id>`, sends it as provider idempotency key, records the observed result, and acknowledges. Ambiguous timeout triggers provider lookup. Conclusion: late acknowledgement requires an effect-level uniqueness or reconciliation mechanism.

### Example 4

Account events are keyed by account, but one code path uses email address. Events for the same account land in different partitions and update a balance out of order. The producer contract canonicalizes account ID and rejects missing keys; migration drains the old scheme and reconciles revisions. Conclusion: partition-key semantics are an API compatibility surface.

### Example 5

Backlog $B=9{,}000$, arrival $\lambda=50$ events/s, worker rate $\mu=15$ events/s, and $n=10$. Net drain is $150-50=100$ events/s, so ideal $T=90$ seconds. Only six partitions exist, limiting effective service to $90$ events/s and net drain to 40, so ideal time becomes 225 seconds before skew or retries. Conclusion: partition capacity must constrain scaling math.

### Example 6

A handler takes 90 seconds at the 99th percentile but visibility timeout is 30 seconds. Three consumers concurrently process one slow message. A progress-bound extension with two-minute base, capped total lease, fenced effect, and cancellation after lease loss removes uncontrolled overlap. Conclusion: lease design must cover processing tails without hiding stuck work indefinitely.

### Example 7

An invalid currency code retries immediately 1,000 times and overloads the database. Schema/domain classification marks it non-retryable, quarantines after one verified failure, alerts the producer owner, and preserves identity and restricted evidence. Conclusion: deterministic invalid work should not consume transient-failure budget.

### Example 8

A dead-letter queue contains 40,000 customer records but has no owner. A repair script generates new IDs and replays at full speed, duplicating notifications and starving live traffic. The corrected workflow assigns owner/SLO, preserves IDs, selects an audited range, uses dry-run/shadow mode, caps capacity, validates dedup retention, and records results. Conclusion: quarantine and replay are production products.

### Example 9

Kafka transactional processing reads topic A and writes topic B exactly once within configured Kafka semantics. The consumer also calls an email API outside the transaction, and a crash repeats email. The design writes an email-intent event transactionally to B; a separate email consumer uses provider idempotency. Conclusion: strong broker semantics do not cross unnamed external boundaries.

### Example 10

A team deletes an unused topic. A CDC relay still publishes, two service accounts retain broad ACLs, one consumer group holds offsets, a DLQ contains regulated payloads, and analytics archived copies. Retirement first stops/redirects producers, drains, inventories consumers and retention, resolves DLQ, revokes identities, verifies deletion, and removes telemetry last. Conclusion: destination deletion is not event-path retirement.

## Cross-Program Connections

- **Distributed systems:** partial failure, durable logs, leases, fencing, idempotency, transactions, and reconciliation determine delivery-effect correctness.
- **API and service engineering:** AsyncAPI, CloudEvents, compatibility, idempotency keys, long-running status, and deprecation make asynchronous interfaces governable.
- **Data engineering:** CDC, stream processing, watermarks, partitions, late data, replay, lineage, and projections extend the event path into pipelines.
- **Databases:** transactional outbox/inbox, isolation, unique constraints, log sequence, and materialized views supply atomicity and progress mechanisms.
- **Concurrency:** work sharing, ordering, race conditions, locks, leases, and shutdown explain consumer-group behavior.
- **Algorithms:** hashing, partition skew, work queues, backoff, and queueing models shape throughput and tail latency.
- **Security engineering:** producer authenticity, tenant boundaries, payload minimization, encryption, quarantine access, and audit protect retained data.
- **Reliability engineering:** lag/age SLOs, poison work, failure injection, backpressure, replay, and incident recovery expose user outcomes.
- **Systems engineering:** authority, interface boundaries, hazards, lifecycle inventory, and assurance claims prevent local broker features from being overgeneralized.
- **Governance:** schema ownership, data retention, replay approval, priority, cost, and retirement assign obligations across organizational boundaries.

## References

1. Cloud Native Computing Foundation, “CloudEvents Specification,” version 1.0.2, February 2022. https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md
2. AsyncAPI Initiative, “AsyncAPI Specification,” version 3.1.0, January 2026. https://www.asyncapi.com/docs/reference/specification/v3.1.0
3. Apache Kafka Project, “Design: Message Delivery Semantics,” version 4.1 documentation, retrieved 2026-09-02. https://kafka.apache.org/41/design/design/#message-delivery-semantics
4. Apache Kafka Project, “KafkaConsumer API,” clients 4.1.2, retrieved 2026-09-02. https://kafka.apache.org/41/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html
5. Amazon Web Services, “Amazon SQS At-Least-Once Delivery,” current documentation, retrieved 2026-09-02. https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html
6. Amazon Web Services, “Amazon SQS Visibility Timeout,” current documentation, retrieved 2026-09-02. https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html
7. NATS Authors, “JetStream Pull Consumers,” current documentation, retrieved 2026-09-02. https://docs.nats.io/learn/jetstream/pull-consumers
8. KEDA Authors, “Scaling Deployments, StatefulSets and Custom Resources,” documentation version 2.20, retrieved 2026-09-02. https://keda.sh/docs/2.20/concepts/scaling-deployments/
9. KEDA Authors, “Scaling Jobs,” documentation version 2.20, retrieved 2026-09-02. https://keda.sh/docs/2.20/concepts/scaling-jobs/
10. OpenTelemetry Authors, “Semantic Conventions for Messaging Systems,” semantic conventions 1.44.0, development status, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/semconv/messaging/
11. Chris Richardson, “Pattern: Transactional Outbox,” Microservices Patterns, current pattern catalog, retrieved 2026-09-02. https://microservices.io/patterns/data/transactional-outbox.html
12. CNCF Platforms Working Group, “Platforms White Paper,” April 2023. https://tag-app-delivery.cncf.io/whitepapers/platforms/
13. NIST, “Secure Software Development Framework (SSDF) Version 1.1,” SP 800-218, February 2022. https://csrc.nist.gov/pubs/sp/800/218/final

## Exercises

### Exercise 1

Define occurrence, event, message, delivery, processing attempt, producer contract, subscription contract, settlement, visibility lease, poison event, quarantine, replay, and effect key. For each, name one adjacent concept it must not be confused with.

### Exercise 2

Trace one order-confirmed occurrence through source transaction, outbox, relay timeout, duplicate publication, partitioned delivery, consumer rebalance, external effect timeout, reconciliation, acknowledgement, telemetry, and retention. Identify every stable and attempt-specific identity.

### Exercise 3

A template publishes directly after database commit with a new UUID per retry, uses one consumer group for three independent applications, auto-commits, scales on CPU without partition bounds, retries all failures immediately, stores full payloads in a public DLQ dashboard, and offers unaudited offset reset. Diagnose at least fifteen defects and correct them.

### Exercise 4

Design a platform portfolio supporting Kafka logs, SQS-style queues, partner webhooks, continuous consumers, and event-triggered Jobs in four languages. Define common contracts, provider adapters, identity, schemas, ordering, effects, scaling, quarantine, replay, observability, testing, and escape conditions without multiplying templates by every combination.

### Exercise 5

A partition-key change was deployed during a broker migration; some events dual-published, a consumer’s deduplication window expired, an old schema is no longer readable, quarantine contains regulated records, and live backlog age is rising. Produce a safe containment, reconciliation, replay, migration, and retirement sequence.

## Answers to the Exercises

### Answer 1

An occurrence is a domain fact and differs from its representation. An event is an immutable fact record and differs from a command asking for action. A message is a transport envelope and differs from event identity. A delivery is one presentation and differs from the message/event. A processing attempt is consumer execution and differs from delivery when a handler retries internally. A producer contract governs fact meaning/publication and differs from a topic configuration. A subscription contract governs one consumer’s selection and progress and differs from a shared destination. Settlement changes broker delivery state and differs from business commit. A visibility lease grants temporary processing opportunity and differs from a fenced domain lock. A poison event deterministically fails a consumer revision and differs from a transient broker failure. Quarantine retains failed work for owned resolution and differs from resolution itself. Replay is a governed re-delivery execution and differs from an occurrence or ordinary automatic retry. An effect key names one intended consumer outcome and differs from broker offset or trace ID.

### Answer 2

The source commits order state and outbox intent atomically with stable event `(source,id)`, aggregate revision, type/schema, occurrence time, and partition key. Relay execution has its own attempt ID; after an ambiguous publish timeout it retries the same event identity, so the broker may hold duplicate messages with distinct broker IDs/positions. Both map to the same event. A consumer group assigns the partition; each delivery carries destination, group, partition, position, delivery attempt, and lease. A rebalance stops acquisition, drains or releases in-flight work, and gives a new consumer execution identity without changing event/effect identity. The consumer validates schema/source and derives effect key from source, event ID, and consumer contract. An external timeout yields unknown effect; it queries the provider using the same key. If committed, it stores/returns that result and settles broker progress; if absent, it retries within policy; if unknowable, it stops automatic settlement/replay and escalates reconciliation. Trace/span IDs correlate publish, receive, process, and settle but do not replace identities. Metrics aggregate type/group/status; scoped logs/inbox retain event/effect keys. Broker data, outbox, inbox/dedup, external effect evidence, logs/traces, quarantine, and audit each follow explicit retention long enough for recovery/replay.

### Answer 3

Direct post-commit publish has a crash gap and unknown-confirmation duplication; use transactional outbox, CDC contract, bounded transaction, or reconciliation. New UUID per retry makes one occurrence distinct; preserve source-scoped event identity. One group shared by independent applications load-balances events instead of broadcasting them; create independent subscriptions/groups and owners. Auto-commit can advance before durable effects; explicitly settle after transactional/idempotent effect or reconciliation. CPU ignores backlog age, arrival rate, partitions, skew, and downstream limits; scale on outcome-related signals within all bounds. Immediate universal retry amplifies deterministic invalid data, authorization failures, poison events, and outages; classify, back off with jitter, cap attempts/time, and quarantine non-retryable work. Full payload in a public dashboard violates least privilege, minimization, privacy, and retention; restrict quarantine, redact or reference payloads, audit access, and provide deletion. Unauthenticated/unaudited offset reset is replay authority; require exact range, compatible revision, preserved identity, effect mode, approval, capacity isolation, monitoring, abort, and audit. Additional missing controls include stable schema/meaning, partition-key contract, ordering scope, lease/shutdown/rebalance behavior, external-effect idempotency, dedup retention, source authenticity, workload identity, telemetry correlation, owner/SLO, DLQ repair, contract tests, lifecycle inventory, and deprecation/retirement.

### Answer 4

Define common producer/event/subscription/consumer contracts independent of provider: source and stable identity, semantic/schema revision, commit/publication, classification, destination binding, selection/fan-out, ordering key, start/progress, lease/settlement, effect mechanism, retry/quarantine/replay, scaling/backpressure, identity, telemetry, support, retention, and retirement. Provider adapters map retained Kafka partitions/groups/transactions, SQS queue/visibility/redelivery, and authenticated webhook request/response retries without claiming identical guarantees. Runtime libraries in four languages implement CloudEvents/envelope/schema validation, identity propagation, bounded receive, explicit settlement hooks, trace/redaction, and graceful drain; domain effects remain explicit. Continuous consumers suit high-throughput partition ownership and connection reuse; Jobs suit expensive bounded isolated work only when acknowledgement/effect coordination is defined. KEDA adapters use supported signals but cap replicas by partitions/downstream/quota and preserve minimum capacity when needed. Shared conformance tests cover duplicate, order, lease, crash windows, rebalance, scale, poison, replay, security, and cleanup for every supported provider/runtime profile. Escape review covers global ordering, unsupported protocols, exotic transactions, unbounded retention, high-privilege networking, or effects without safe repetition/reconciliation. Team and event type are parameters/catalog relationships, not template-fork reasons.

### Answer 5

Pause partition changes, migration cutover, broad replay, and unsafe autoscaling while preserving live processing that is known correct. Inventory both brokers, dual-publish interval, event `(source,id)`, old/new partition keys, positions, consumer revisions, effect keys/results, schema versions, dedup expiry, quarantine, and regulated copies. Protect live backlog with bounded capacity and oldest-age alerts; isolate investigative/replay capacity. Reconstruct a canonical event set by stable identity and source authority, not broker message ID; identify gaps, duplicates, and per-entity order violations. Restore a trusted old-schema reader or versioned transformation with fixtures and lineage rather than guessing fields. For each consumer effect, query authoritative state; expired dedup makes absence/commit analysis mandatory, and unknown non-idempotent outcomes must not replay automatically. Quarantine sensitive records under restricted access and meet deletion/retention obligations without destroying required incident evidence. Repair partition state using aggregate revisions/snapshots and a tested canonical key. Replay only missing/safe events through a shadow or controlled destination, preserving IDs, pinning compatible logic, throttling below downstream/live limits, and validating outcomes. Cut consumers to one authoritative stream after parity and rollback evidence, drain outbox/bridges, resolve groups and quarantine, revoke old ACLs/credentials, delete retained data by policy, and remove old telemetry last. Record the incident, migration, reconciliation decisions, and residual uncertainty.
