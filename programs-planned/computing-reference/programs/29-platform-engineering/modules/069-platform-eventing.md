---
module_id: PLAT-069
program: Platform Engineering
level: 2
module_number: 69
title: Platform Eventing
status: complete
last_verified: 2026-09-02
---

# Platform Eventing

## One-Page Review

### Governing question

How should an internal developer platform publish and consume events so independently evolving components can react, recover, replay, and prove outcomes without turning a message broker into a source of truth, promising impossible global ordering, or leaking sensitive tenant data?

### Essential definitions

- An **event** is an immutable statement that a producer-authoritative occurrence happened; it is named in the past tense and cannot be refused retroactively.
- A **command** asks a named authority to attempt an action and has an accept/reject/result lifecycle; it is not an event merely because it travels through a broker.
- A **notification** says that something may be worth retrieving; it can deliberately carry less state than the authoritative resource.
- An **event envelope** carries transport-independent identity and context such as specification version, event ID, source, type, subject, occurrence time, schema, tenant, and correlation.
- A **channel** is an addressable logical destination through which messages are sent or received; a topic, queue, stream, or webhook route is a transport realization.
- A **subscription** is a governed consumer interest plus filter, authorization, delivery, retry, retention, and lifecycle policy.
- A **consumer group** shares work among members while retaining its own progress; a second group represents a distinct logical consumption, not extra replicas of the first.
- An **offset** or **cursor** is transport progress, not proof that a business side effect committed.
- **idempotent consumption** makes repeated delivery of one event occurrence converge on one intended externally visible effect.
- A **transactional outbox** commits domain state and an event-to-publish record in one local transaction, then relays the record asynchronously.
- A **dead-letter or quarantine stream** isolates messages that cannot be processed under policy while preserving evidence and an authorized recovery path.
- **replay** deliberately redelivers retained historical events to a fresh or reset consumer; it is a production change with capacity, compatibility, and side-effect risk.

### Central model, mechanism, or theorem

Represent an event as

$$
e=(s,i,t,u,\tau,v,k,d),
$$

where source $s$ and event ID $i$ form occurrence identity, $t$ is semantic type, $u$ is subject, $\tau$ is occurrence time, $v$ is schema revision, $k$ is an ordering/partition key, and $d$ is data. For logical consumer $c$, processing attempt $a$ computes transition $F_c(x,e)$ from local state $x$. Safe redelivery requires a durable receipt or business uniqueness constraint keyed by $(c,s,i)$ in the same atomic boundary as the consumer effect. Transport acknowledgement follows that commit. The platform may promise ordered observation only inside the declared ordering scope $k$ and retained interval; it may not infer business completion from publication, broker acknowledgement, cursor advancement, or elapsed time.

### Critical invariants

- Producer authority, event source, and schema owner are explicit; intermediaries do not silently rewrite event meaning.
- $(source,id)$ identifies one immutable occurrence; a retry preserves it, while a new occurrence receives a new ID.
- Event, command, notification, audit record, trace, metric, log, current state, and change-data-capture record remain distinct contracts.
- Event type and schema evolve compatibly for existing consumers, or a new type/revision and migration coexistence are introduced.
- Tenant and authorization filters apply before delivery, replay, browse, metrics labels, dead-letter inspection, and payload disclosure.
- Ordering is promised only for a documented key/partition and producer protocol; unrelated keys remain unordered.
- Consumers tolerate redelivery; deduplication state and business effect share an atomic boundary or use an effect-specific idempotency key.
- Progress is committed only after the intended durable effect; failure before acknowledgement must be safely repeatable.
- Retry is bounded with backoff and jitter; poison, permanent, unauthorized, and incompatible messages do not block healthy traffic forever.
- Retention, compaction, deletion, legal hold, encryption, restore, and regional replication match data classification and recovery objectives.
- Replay identifies exact source interval, schema set, target consumer generation, side-effect mode, rate limit, and completion evidence.
- Broker availability and lag are observed independently from producer truth and consumer business correctness.

### Common failures

Calling commands events; one topic per team with no contract; mutable payload under an unchanged type; ID regenerated on retry; timestamp used as an ordering guarantee; global-order promises over partitions; “exactly once” applied to external effects; acknowledging before commit; dedup cache without durable scope; infinite retries; dead-letter queue as permanent trash; replay into live email or billing; secrets and personal data in envelopes; tenant filtering only in consumers; tracing context treated as authorization; broker log treated as audit or database; dual-writing database and broker; outbox relay deleting before publication evidence; CDC internals exposed as domain events; consumer lag as the only health signal; unbounded cardinality; and retiring a topic while lagging or offline consumers still depend on it.

### Compact example

Environment vending commits environment `env-82` and outbox row for event `(source=/platform/environments, id=evt-991, type=io.bijux.platform.environment.ready.v1, subject=env-82, key=env-82)` in one database transaction. The relay publishes the same occurrence until the broker confirms it. Catalog and cost consumers use different groups and durable receipts keyed by their group plus `(source,id)`. A duplicate delivery updates neither twice. A later `environment.suspended.v1` for `env-82` uses the same key, so that partition preserves per-environment order. A billing replay targets a shadow ledger with outbound charges disabled, bounded rate, an immutable interval, schema fixtures, and reconciliation before cutover.

### Connections

This module carries durable workflow outcomes from [PLAT-065](065-workflow-and-orchestration-layers.md), policy decisions from [PLAT-066](066-policy-decision-and-enforcement-points.md), vending lifecycle from [PLAT-067](067-environment-and-account-vending.md), and broker operations from [PLAT-068](068-service-broker-and-marketplace-models.md). PLAT-070 composes platform components using these boundaries. API, distributed-systems, data-engineering, security, observability, and reliability programs supply complementary contract and operations reasoning.

## Governing Question

How can platform components exchange facts asynchronously while remaining independently deployable, recoverable, secure, and honest about delivery guarantees?

Platform eventing is not “install a broker.” It is a governed integration capability: semantic contracts, producer authority, transport topology, subscription ownership, identity, delivery behavior, schema evolution, security, observability, recovery, replay, and retirement.

A platform commonly connects portals, catalogs, workflow engines, policy services, environment vendors, service brokers, identity systems, cost systems, deployment controllers, and evidence stores. Direct synchronous chains make each user action depend on every downstream component. Events can decouple availability and pace, but introduce delay, duplicates, reordering, retained sensitive data, invisible backlogs, and recovery complexity.

The design goal is selective decoupling. Publish facts where multiple independently owned consumers need them or where durable asynchronous reaction improves resilience. Keep commands directed, queries authoritative, and critical invariants inside a single consistency boundary whenever possible.

## Why This Matters

Platform teams often begin with a small notification bus and accidentally create a second, undocumented API estate. Consumers parse fields no producer promised, topic names become business interfaces, access accumulates, and replay later triggers real side effects.

Delivery language is especially dangerous. “Exactly once” may describe a bounded broker-to-broker or transactional read-process-write path. It does not automatically cover email, cloud provisioning, payment, DNS, or another database. A platform must state the boundary of every guarantee.

Events also amplify security mistakes. One overbroad topic can distribute account IDs, repository data, vulnerability findings, cost, or personal information to many consumers and backups. Unlike an authorization failure on a synchronous request, unauthorized retained delivery may persist for months.

Recovery determines whether eventing is an asset or liability. Consumers will be offline, schemas will change, brokers will fail, regions will partition, and operators will need replay. Those cases require contracts and rehearsal before an incident.

Well-designed eventing makes platform state changes observable and composable without making the event stream authoritative for facts it cannot prove. It turns asynchronous integration into a supported product rather than shared infrastructure folklore.

## Prerequisites and Retrieval

Retrieve event-driven architecture, publish-subscribe and work-queue semantics, API contracts, distributed transactions, idempotency, retries, backoff and jitter, partitioning, consensus and replication, schema evolution, serialization, authorization, multi-tenancy, data classification, audit, observability, SLOs, disaster recovery, change-data capture, state machines, and lifecycle retirement.

You should distinguish event from command; event from notification; occurrence time from publish and processing time; source from broker; event identity from aggregate identity; schema version from envelope specification version; channel from physical topic; subscription from consumer process; consumer group from replica; cursor from completed side effect; retry from replay; dead-letter from deletion; outbox row from domain event; CDC record from business fact; broker durability from end-to-end correctness; and correlation from authorization.

## Learning Objectives

After completing this module, you should be able to:

1. classify events, commands, notifications, queries, audit records, telemetry, state snapshots, and CDC records;
2. define producer authority, event taxonomy, envelope, schema, and compatibility ownership;
3. select channel, partition, ordering, retention, compaction, and delivery semantics deliberately;
4. publish domain state changes without unsafe database/broker dual writes;
5. implement idempotent consumers with atomic progress and business effects;
6. operate retry, quarantine, replay, backpressure, quotas, and poison-message recovery;
7. secure tenant routing, subscription authorization, payloads, metadata, browse, and administrative operations;
8. instrument producer, intermediary, and consumer behavior without confusing telemetry with proof;
9. design regional recovery, restore, bootstrap, schema migration, and topic retirement; and
10. test event contracts under duplication, loss ambiguity, reordering, skew, outage, overload, and malicious input.

## Core Exposition

### Decide whether asynchronous eventing belongs in the path

Use an event when a producer can authoritatively state a completed or durably recorded occurrence and does not need to know every future consumer. Good examples include environment request accepted, environment ready, service binding revoked, policy bundle published, or catalog entity ownership changed.

Do not use an event to disguise a directed request. `CreateEnvironment` is a command to an authority. `EnvironmentCreated` states an outcome. The command can be transported asynchronously, but it still needs target, authorization, acceptance, rejection, deduplication, deadline, and result correlation.

Keep hard consistency together. If quota decrement and resource allocation must never disagree, an event between them may be the wrong boundary. Asynchrony is not a substitute for modeling the invariant.

Prefer synchronous lookup when a caller needs current authoritative state and can tolerate coupling to that authority. An event-derived view is explicitly stale and must expose its observation time and completeness.

### Establish semantic authority

Every event type has one semantic owner. That owner defines what occurrence makes the event true, which fields are contractual, what identifiers mean, how corrections appear, and how long compatibility is supported.

The application that knows the domain fact should create its identity and payload. A generic broker, connector, or portal must not infer `EnvironmentReady` from an arbitrary row update or HTTP 200 unless that mapping is a governed contract.

Intermediaries may validate, authorize, route, encode, encrypt, compress, enrich approved context, and translate protocol bindings. If they transform domain semantics, the result is a new event with a new source and occurrence identity, plus causation provenance.

Record ownership in the software catalog: event type, producer, schema repository, support channel, classification, lifecycle state, known channels, consumers, SLO, retention, and retirement policy. Discovery does not override runtime authorization.

### Classify messages before designing transport

An event is a past fact. A command expresses intent. A notification signals that a consumer should fetch details. A query asks an authority for information. An audit record proves a security-relevant action under controlled integrity and retention. A log helps diagnose execution. A metric summarizes measurements. A trace relates operations. A snapshot represents state at a point. CDC describes storage mutations.

These can be correlated but are not interchangeable. An event stream can feed an audit store only if the event and pipeline meet audit requirements. A Kubernetes watch can drive reconciliation but is not automatically a long-retention business event stream. A trace header connects work but grants no permission.

Choose the weakest payload that serves consumers. A notification with resource ID and revision may reduce sensitive replication, but increases synchronous lookup and authorization load. A domain event with selected facts improves autonomy, but creates duplicated data obligations and compatibility commitments.

### Standardize a transport-independent envelope

CloudEvents separates common context from data and defines required `specversion`, `id`, `source`, and `type`. In its model, source plus ID identifies an occurrence. Optional subject, time, data content type, and data schema improve routing and interpretation.

Adopt a constrained platform profile rather than inventing an incompatible wrapper. Require occurrence time when known; producer-assigned source and ID; stable reverse-domain type; subject for routable aggregate identity; immutable schema URI or registry reference; content type; tenant routing attribute where safe; and correlation/causation fields with explicit definitions.

Keep envelope version separate from payload schema version. CloudEvents `specversion` explains the event format. The event `type` and `dataschema` explain domain compatibility. Do not increment envelope version because one payload field changed.

Bound every field. Limit header count, string length, payload size, nesting, decompressed size, and extension allowlist. Validate before routing. Metadata can leak just as payloads can; subject, tenant, type, trace, and error descriptions need classification.

### Preserve occurrence identity

The uniqueness scope is $(source,id)$. When a publisher retries an ambiguous send, it reuses both. When the same aggregate changes again, it creates a new event ID even if subject and type repeat.

Do not use timestamp as identity. Clocks collide and move. Do not use broker offset as portable identity; it changes across topics, clusters, mirrors, and republishing. Do not use correlation ID; one business interaction may cause several distinct events.

If an event is republished after transformation, decide whether it is transport forwarding or a new semantic production. Transparent forwarding preserves event identity and content. Semantic transformation assigns a new source/ID and carries original identity as causation or provenance.

Deduplication storage has a scope and retention. A consumer that forgets receipts after seven days cannot claim deduplication for a replay from last year unless business constraints still reject duplicates.

### Design event types and schemas for evolution

Name types by stable business meaning, commonly past tense: `environment.ready`, `binding.revoked`, or `policy.bundle.published`. Avoid implementation names such as `database-row-updated` unless storage mutation is truly the contract.

Define required and optional fields, null versus absent, formats, bounds, identifiers, units, timezone, classification, defaults, and invariants. Supply positive, boundary, redacted, and invalid fixtures.

For a compatible additive change, preserve existing meaning and type according to the declared format and consumer policy. A breaking semantic or structural change needs a new event type or schema revision that consumers can distinguish. Run old and new during a migration window.

Compatibility tooling is necessary but insufficient. A schema checker may accept an optional field whose meaning changes a consumer's decision. Review semantic compatibility, generated clients, routing filters, storage projections, and privacy impact.

### Describe the asynchronous API

AsyncAPI documents message-driven application interfaces using servers, channels, messages, operations, schemas, security, and protocol bindings. Model the API from an application's perspective: what it sends or receives, on which logical channel, under which server and security contract.

Keep semantic contracts portable and bindings explicit. Partition count, Kafka key, AMQP exchange, webhook acknowledgement, or queue settlement belong to protocol/runtime profiles. Consumers need both the portable event meaning and the actual delivery contract.

Publish machine-readable documents into the portal with owner and lifecycle metadata. Validate examples and compatibility in producer CI. Generate scaffolding only where generated code does not hide acknowledgement, retry, and transaction boundaries.

Treat the specification as governed source, not a diagram exported after implementation. Runtime inventories should compare observed producers, subscriptions, schemas, and ACLs against declared contracts.

### Select channel topology deliberately

A logical channel groups messages that share access, retention, scaling, ordering, and lifecycle characteristics. A physical topic may implement one or more channels only when those policies truly align.

Avoid one enterprise topic: it couples authorization, capacity, schema, and failure. Avoid one topic per tiny event by reflex: it creates operational sprawl. Group by bounded domain and compatible governance, then separate high-volume, sensitive, high-retention, or independently recoverable traffic.

Name channels by durable domain responsibility, not team name or delivery sequence. Maintain an immutable internal channel ID if physical names may change. Record cluster, region, partitions, replication, retention, compaction, classification, owners, quotas, and lifecycle.

Do not encode authorization solely in a predictable topic name. Broker ACLs, subscription control, event filters, and payload-level policy must enforce the actual tenant and event contract.

### Define partitioning and ordering scope

Kafka preserves order within a topic partition, not across every partition. A key such as environment ID can route related occurrences to one partition, enabling per-environment ordering while allowing different environments to progress independently.

Partition key choice is domain design. It determines ordering scope, load distribution, rebalance cost, and maximum hot-key throughput. Tenant ID may preserve tenant order but create hot tenants; random keys distribute well but remove aggregate order.

Document what creates order: producer serialization, idempotent/transactional settings, key mapping, partition expansion behavior, failover, and retry. Multiple independent producers for the same key need a domain sequence or authoritative conflict rule if their relative order matters.

Sequence numbers detect gaps or stale updates but do not by themselves recover missing events. Consumers define whether to pause, fetch current state, wait within a bounded reorder window, or quarantine.

### State delivery guarantees with their boundaries

At-most-once may lose work but avoids transport redelivery. At-least-once retries until acknowledgement and therefore can deliver duplicates. Exactly-once processing requires a precisely defined system boundary, protocol, failure model, and atomic read-process-write behavior.

Broker acknowledgement proves only what the broker contract says—perhaps acceptance by a leader or durable replication. It does not prove every subscriber processed an event or an external side effect succeeded.

Kafka idempotent producers and transactions can support exactly-once semantics for covered Kafka records and offsets under correct configuration. They cannot atomically include an arbitrary cloud API, email, or unrelated database without another protocol.

Prefer honest at-least-once delivery plus idempotent effects. Where loss is acceptable, say why. Where duplicates are dangerous, prove the consumer's atomicity or use the destination's idempotency contract.

### Publish without the dual-write gap

Writing a database row and then publishing can fail after the row commit, losing the event. Publishing first can expose an event for state that later rolls back. Retrying either side can duplicate.

The transactional outbox writes domain state and an immutable outbox row in the same local transaction. A relay or CDC connector publishes rows, marks progress or relies on log position, and retries ambiguities with the original event identity.

The outbox closes the local state/event atomicity gap; it does not make downstream side effects exactly once. Monitor unpublished age, relay lag, malformed rows, duplicate publication, table/log retention, connector checkpoints, and restore behavior.

Do not let the outbox become an unbounded shadow database. Define dispatch evidence, cleanup, archival, schema ownership, and recovery. A database restore can resurrect old rows; relay recovery must know which identities may be republished.

### Use change-data capture without leaking storage semantics

CDC faithfully reports database log changes according to connector semantics. That is valuable for replication, caches, analytics, and outbox relay. A raw row-change stream is usually not a stable domain API.

Storage schemas contain joins, internal flags, migrations, tombstones, and sensitive columns. One business transaction may produce many row changes. Consumers coupled to them prevent the producer from changing persistence design.

Map CDC to governed events only through an owned anti-corruption layer or use an explicit outbox whose payload is authored by the domain. Preserve source log coordinates as operational provenance, not domain identity.

Snapshot and streaming phases differ. Consumers must understand snapshot markers, transaction boundaries, tombstones, schema changes, and a handoff from snapshot to live log without gaps.

### Build idempotent consumers

For logical consumer $c$, store receipt $(c,s,i)$ and perform the business effect in one transaction when both reside in the same database. A unique constraint prevents two workers from committing the same effect.

If the effect is an external API, pass a stable idempotency key derived from the consumer and occurrence when the API supports it. Otherwise model a durable workflow: intent, attempt, provider receipt, reconciliation, and terminal evidence.

Do not acknowledge before durable effect. A crash between acknowledgement and commit loses work. A crash after commit but before acknowledgement causes redelivery, which the receipt/effect boundary must tolerate.

Do not acknowledge and then enqueue only in volatile memory. If processing fans out, atomically persist durable successor work before settling the input.

### Separate offset progress from business truth

An offset says how far a group told the broker it progressed. It does not reveal whether the right handler ran, whether a database commit was correct, or whether an external provider completed.

Track received, validated, deduplicated, processing, effect committed, acknowledged, retried, quarantined, and reconciled as distinct observations where risk warrants it. Avoid storing unbounded per-message telemetry forever; keep durable business receipts according to the dedup/replay horizon.

Consumer lag combines production and consumption rates, partition positions, and time. Record both record lag and age of oldest actionable message. A low-volume stuck partition can have small record lag but severe time lag.

Business completeness needs domain measures: environments absent from catalog, cost events unmatched to resources, revocations not applied, or policy publications not activated.

### Bound retry and isolate poison messages

Classify failures: transient dependency, throttling, consumer defect, invalid schema, unauthorized tenant, permanent business rejection, and unknown. Their recovery actions differ.

Use exponential backoff with jitter, per-dependency budgets, and a terminal deadline. Maintain order where necessary without letting one poison message halt unrelated keys. Retry topics can break ordering unless the design accounts for it.

Quarantine records the original immutable message, failure class, consumer version, attempt count, first/last time, safe diagnostic, and provenance. Access is tightly controlled because quarantines collect malformed and sensitive data.

Redrive is a governed operation. Fix or select compatible consumer code, choose exact messages, define dedup behavior, rate limit, record operator/approval, and reconcile outcomes. Editing a failed payload creates a new derived event with provenance; it is not the original occurrence.

### Control backpressure, fairness, and quotas

When arrival rate $\lambda$ exceeds sustainable service rate $\mu$, backlog grows. More partitions or consumers help only until a downstream bottleneck, hot key, quota, or serialized ordering scope dominates.

Apply producer quotas, payload limits, per-tenant fairness, consumer concurrency, batch bounds, dependency bulkheads, and admission control. Avoid a noisy tenant exhausting broker storage or a replay starving live traffic.

Autoscaling from lag needs damping and downstream capacity awareness. Scaling consumers can trigger rebalances and duplicate in-flight work. Maximum parallelism is bounded by partitions for one group in partitioned transports.

Define overload behavior: delay, shed an explicitly lossy class, pause a subscription, reject publishes, spill to governed storage, or degrade optional consumers. Never silently drop contractual events.

### Secure publish, subscribe, and administration

Authenticate workload identity and authorize producer-to-type/channel, consumer-group-to-subscription, tenant/filter, replay interval, browse, schema access, dead-letter access, and administrative mutations separately.

Validate that producer identity is allowed to claim the event source and tenant. Do not trust a tenant header because it is syntactically valid. Broker ACLs may need a trusted routing gateway or per-tenant destinations for enforceable isolation.

Encrypt in transit and at rest, manage keys by classification/tenant where necessary, rotate credentials, and limit broker administrator access. Avoid shared application credentials and wildcard subscriptions.

Trace context, correlation IDs, subjects, and schema errors are attacker-controlled input at trust boundaries. Sanitize logs and metrics, bound cardinality, and never use trace context as authentication or authorization.

### Minimize retained data

Every copied event expands the data estate: broker replicas, mirrors, caches, consumer databases, quarantine, backups, local logs, and test fixtures. Classify payload and envelope before publication.

Prefer stable references or tokenized values when consumers can authorize a lookup. But references reduce historical reproducibility and increase source dependency, so make the trade-off explicit.

Retention must reflect consumer outage tolerance, replay objectives, legal hold, privacy deletion, cost, and restore. Compaction retains a latest keyed record according to transport rules; it is not a universal deletion or history guarantee.

Crypto-shredding, field encryption, tombstones, or topic deletion each have limitations across backups and derived copies. Maintain a data inventory and subject-deletion propagation contract where regulated data is involved.

### Observe the asynchronous path

Instrument publish creation/send, broker acknowledgement, receive, process, and settle. OpenTelemetry messaging conventions distinguish these operations and use span links because fan-out and batching do not fit a single parent chain reliably.

Propagate W3C trace context only across trusted boundaries with validation and privacy limits. A consumer processing span may link to the producer's creation context while retaining its ambient transport parent.

Measure publish success/latency, rejected messages, broker under-replication, storage, partition skew, consumer lag/age, processing latency, retries, quarantine rate/age, schema failures, auth denials, replay volume, and business reconciliation gaps.

Control metric cardinality. Event ID, subject, user, and raw error must not become metric labels. Use sampled logs/traces and bounded categorical attributes, with secure drill-down to exact occurrences.

### Design replay as a controlled migration

Replay is not “reset the offset and see.” Specify source channel and immutable interval, event/schema versions, target consumer code/configuration, receipt namespace, side-effect policy, output destination, ordering, concurrency, rate, abort criteria, and evidence.

Prefer shadow replay into a fresh projection. Compare counts, checksums, invariants, and sampled records before cutover. Disable irreversible outbound effects or route them to a simulator unless intentional redelivery is the goal.

For an in-place rebuild, stop or fence live consumption, record the boundary, bootstrap snapshot if required, replay to that boundary, then resume without gap or overlap beyond the consumer's dedup contract.

Preserve replay provenance. Operators must distinguish original processing from a recovery or experiment, while the underlying event occurrence identity remains unchanged.

### Bootstrap consumers with snapshot plus stream

Retention may not cover the entire state history, and event history may not be a complete state model. New consumers often need an authoritative snapshot followed by changes.

Establish a consistent boundary $b$: obtain a snapshot corresponding to $b$, load idempotently, then consume events after $b$. The exact mechanism may use database log positions, broker transactions, or an authority-provided export.

Validate schema and authorization for snapshot and stream. A snapshot is bulk data with its own encryption, expiry, checksum, and deletion requirements.

If no consistent boundary exists, reconcile after bootstrap against authoritative state and quantify the uncertainty. Do not claim gap-free initialization from two unrelated timestamps.

### Plan broker and regional failure

Define replication acknowledgement, failure domains, quorum, leader election, maximum data loss, failover time, and producer/consumer behavior during partition. A nominal multi-zone label does not establish these properties.

Cross-region active-active eventing complicates identity, ordering, duplicate suppression, loop prevention, conflict, and data residency. Prefer a single authority per ordering key or an explicit merge rule. Preserve original occurrence identity through mirrors.

Backups must include broker configuration, schemas, ACLs, subscription metadata, offsets/checkpoints, encryption dependencies, and sufficient event data—or document which are reconstructed. Restoring messages without consumer receipts can repeat effects.

Exercise loss of leader, zone, registry, identity provider, network path, consumer state store, and whole region. Test failback and duplicate windows, not only failover.

### Govern the platform eventing product

Offer paved-road libraries and templates for envelope validation, identity, outbox publication, consumer transactions, tracing, retry, and tests. Keep their semantics visible; convenience must not acknowledge too early or retry forever.

Provide self-service channel and subscription requests backed by policy: owner, purpose, producer, consumers, tenant scope, classification, schema, expected rate/size, partition key, retention, SLO, region, and expiry/review.

Charge back or at least expose cost for throughput, retention, replication, egress, and idle topics. Capacity reservations and quotas should reflect criticality without letting low-priority replay disrupt control-plane events.

Measure adoption alongside outcomes: lead time to publish/subscribe, contract conformance, compatible change rate, duplicate safety, recovery time, stale subscriptions, unknown consumers, and avoided synchronous coupling.

### Retire events, subscriptions, and channels

Deprecate an event type before removing it. Inventory declared and observed consumers, including offline groups, mirrors, connectors, exports, replayers, and retained decoders. Publish replacement and compatibility window.

Stop new consumers, migrate existing ones, observe zero reads/lag under an agreed window, and retain the old schema/decoder as long as replay obligations require. Producer cessation does not mean retained events disappeared.

Drain or delete subscriptions deliberately. Revoke ACLs and credentials, dispose quarantines and snapshots according to policy, update catalogs and AsyncAPI documents, and preserve required audit evidence.

Delete a channel only after no producers, consumers, mirrors, restore procedures, legal holds, or recovery dependencies remain. A quiet dashboard is not proof of zero dependency.

## Definitions and Notation

Let a platform event be

$$
e=(s,i,t,u,\tau_p,\tau_o,v,k,d,m),
$$

where:

- $s$ is the producer-defined source URI;
- $i$ is occurrence identity unique within $s$;
- $t$ is stable semantic type;
- $u$ is subject/aggregate reference;
- $\tau_p$ is producer occurrence time and $\tau_o$ is broker observation time;
- $v$ is immutable payload schema reference/revision;
- $k$ is the declared partition/ordering key;
- $d$ is domain data; and
- $m$ is bounded context such as content type, tenant-routing claim, correlation, and causation.

Let $C$ be logical consumers, $P$ partitions, and $pos_p(e)$ the position of event $e$ in partition $p$. The transport ordering promise is

$$
e_1,e_2 \in p \land pos_p(e_1)<pos_p(e_2)
\Rightarrow observe_c(e_1)\preceq observe_c(e_2),
$$

only for the specific transport, producer, and consumer conditions documented. It says nothing about events in distinct partitions or about completion of their effects.

For consumer $c$, define durable receipt set $R_c$ and intended business state transition $F_c$. Processing is duplicate-safe when

$$
(s,i)\in R_c \Rightarrow F_c(x,e)=x
$$

for a redelivery, and when adding $(s,i)$ to $R_c$ is atomic with the intended local effect. For a remote effect, an equivalent destination idempotency key or reconciled workflow is required.

Let $q_c(t)$ be the position of the oldest unprocessed actionable event at time $t$. Age lag is

$$
L_c(t)=t-\tau_o(q_c(t)).
$$

Record lag and age lag should be reported together because throughput and event arrival are uneven.

For a processing tier with effective arrival rate $\lambda$ and service rate $\mu$, sustained stability requires $\lambda<\mu$ plus headroom for variance, rebalances, retry, replay, and downstream limits. This is a capacity condition, not a latency guarantee.

## Mechanisms, Invariants, or Proof Structure

### End-to-end event path

1. Domain authority completes or durably records an occurrence.
2. Producer assigns immutable source/ID, type, subject, time, schema, key, and bounded data.
3. Domain state and outbox intent commit atomically when a database is involved.
4. Relay validates, authorizes, serializes, and publishes with the same identity across retries.
5. Broker applies authentication, ACL, quota, partition, replication, retention, and acknowledgement policy.
6. Subscription delivers to a logical consumer group under explicit filter and settlement semantics.
7. Consumer validates envelope/schema/tenant and classifies incompatible or unauthorized input.
8. Consumer checks durable receipt and performs the intended effect atomically or through an idempotent workflow.
9. Consumer commits progress only after durable effect, then acknowledges/settles.
10. Retry handles transient failure; quarantine isolates terminal/unknown failure; reconciliation verifies business completeness.
11. Telemetry relates producer, intermediary, consumer, and business outcome without acting as authority.
12. Replay, restore, migration, and retirement use the same identities and governed contracts.

### Core invariants

**Occurrence identity.** For fixed source $s$, one ID $i$ denotes one immutable occurrence. Retransmission preserves identity; correction or later change is a new occurrence.

**Authority.** Only the domain authority asserts the semantic fact. Broker receipt, CDC observation, and consumer projection cannot strengthen the claim.

**Scoped order.** Ordering claims name their channel, partition/key, producer constraints, and interval. No global order is inferred.

**Consumer atomicity.** Receipt/progress never becomes durable before the intended effect. Duplicate delivery converges through a shared atomic boundary, destination idempotency, or reconciliation.

**Compatibility.** A consumer receives only a type/schema it declares compatible with; incompatible messages do not become guessed partial state.

**Tenant confinement.** Producer claim, routing, subscription, replay, browse, quarantine, telemetry, and retained copies preserve authorized tenant scope.

**Bounded recovery.** Retries terminate or quarantine under explicit policy. Replay is bounded and attributable. Live traffic retains protected capacity.

**Source independence.** Event infrastructure is a transport and retention authority only for its own records; current domain truth remains with the producer-authoritative system.

### Proof sketch: broker exactly-once cannot prove an external effect occurs once

Assume a broker delivers event $e$ to consumer $c$. The consumer calls an external provider, which commits effect $y$, but the response is lost before $c$ durably records completion and acknowledges $e$.

The observable consumer state before retry is indistinguishable from an execution in which the provider never committed. If $c$ retries, a non-idempotent provider may perform $y$ twice. If $c$ does not retry, the second execution may perform it zero times.

Therefore broker delivery/transaction guarantees alone cannot establish exactly-one external effect. The ambiguity is resolved only by including the provider in an atomic protocol, using a stable provider idempotency key, or reconciling provider state with a durable operation identity. This is a proof sketch under the stated crash and lost-response model, not a claim that all transports behave identically.

### Executable consumer audit

The following synthetic audit classifies eight delivery observations. It treats receipts as logical-consumer plus source/event identity, detects duplicates, checks per-key domain sequence gaps, and separates retryable, quarantined, and committed outcomes. It demonstrates local classification only; it does not prove broker delivery, transaction atomicity, schema compatibility, or production capacity.

<!-- bijux-verify: {"id":"event-consumer-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"committed=4\nduplicate=1\ngap=1\nretry=1\nquarantine=1\n"}} -->
```python
deliveries = [
    ("catalog", "/platform/env", "e-1", "env-a", 1, "ok"),
    ("catalog", "/platform/env", "e-1", "env-a", 1, "ok"),
    ("catalog", "/platform/env", "e-2", "env-a", 2, "ok"),
    ("catalog", "/platform/env", "e-3", "env-b", 1, "ok"),
    ("catalog", "/platform/env", "e-4", "env-a", 4, "ok"),
    ("catalog", "/platform/env", "e-5", "env-c", 1, "transient"),
    ("catalog", "/platform/env", "e-6", "env-d", 1, "invalid"),
    ("cost", "/platform/env", "e-1", "env-a", 1, "ok"),
]

receipts = set()
last_sequence = {}
counts = {name: 0 for name in ("committed", "duplicate", "gap", "retry", "quarantine")}

for consumer, source, event_id, key, sequence, outcome in deliveries:
    receipt = (consumer, source, event_id)
    if receipt in receipts:
        counts["duplicate"] += 1
        continue
    if outcome == "transient":
        counts["retry"] += 1
        continue
    if outcome == "invalid":
        counts["quarantine"] += 1
        continue
    expected = last_sequence.get((consumer, key), 0) + 1
    if sequence != expected:
        counts["gap"] += 1
        continue
    receipts.add(receipt)
    last_sequence[(consumer, key)] = sequence
    counts["committed"] += 1

for name in counts:
    print(f"{name}={counts[name]}")
```

### Verification strategy

Verify envelope conformance with fixtures and fuzzing. Verify schema syntax and semantic compatibility against every supported consumer generation. Inject duplicate, delayed, reordered, missing, oversized, malformed, unauthorized, cross-tenant, and decompression-bomb messages.

Crash producers before/after domain commit and before/after publish acknowledgement. Restore a database containing outbox rows. Crash consumers before effect, after effect, before receipt, and before acknowledgement. Confirm one intended local result or safe provider reconciliation.

Load hot keys, uneven partitions, rebalance storms, dependency throttling, broker storage pressure, and retry amplification. Measure oldest-event age and business gaps, not only throughput.

Exercise schema registry outage, identity-provider outage, key rotation, ACL revocation, quarantine redrive, snapshot/stream handoff, shadow replay, zone loss, regional failover/failback, broker restore, consumer-state loss, and topic retirement.

## Alternatives and Trade-Offs

- **Synchronous API versus event.** Synchronous calls provide immediate outcome and simpler reasoning; events decouple pace and availability but add delayed consistency and recovery state.
- **Event versus notification.** Rich events enable autonomous consumers but replicate sensitive facts; notifications reduce payload but couple consumers to authoritative lookup.
- **Domain event versus CDC.** Domain events preserve meaning and compatibility; raw CDC is efficient for data movement but exposes storage semantics.
- **Transactional outbox versus distributed transaction.** Outbox fits local database atomicity and asynchronous relay; distributed transactions can cover participating systems but add coordination and limited ecosystem support.
- **Shared channel versus type-specific channel.** Sharing limits topology sprawl; separation improves ACL, retention, capacity, and independent lifecycle.
- **Aggregate-key partitioning versus random distribution.** Aggregate keys preserve scoped order; random keys improve balance but require consumers to tolerate reorder.
- **At-most-once versus at-least-once.** At-most-once avoids redelivery at the cost of loss; at-least-once protects delivery at the cost of idempotency work.
- **Broker transaction versus consumer database transaction.** Broker transactions atomically cover broker records/offsets within their contract; database transactions protect local business state. Neither automatically spans the other.
- **Schema registry versus repository-only schemas.** A registry supports runtime identity and enforcement; a repository supports review and history. Mature systems often integrate both.
- **Retry in place versus retry channel.** In-place retry may preserve order but block a partition; retry channels isolate delay but complicate order and lifecycle.
- **Dead-letter versus pause.** Quarantine lets healthy traffic continue; pausing preserves strict order but widens outage. Choose by domain invariant.
- **Full history versus snapshot plus stream.** Full replay maximizes derivability but costs retention and assumes complete event semantics; snapshots bootstrap faster but require a consistent boundary.
- **Central gateway versus direct broker access.** A gateway standardizes auth, validation, and quotas; direct access reduces hops and bottlenecks but distributes policy enforcement.
- **Single region versus replicated regions.** One authority simplifies order; replication improves locality/recovery while adding duplicates, conflicts, residency, and failover complexity.
- **Payload encryption versus destination isolation.** Field/payload encryption limits broker/operator visibility but complicates routing and key distribution; isolated channels simplify consumption but expand topology.
- **Build versus managed service.** Managed brokers reduce infrastructure toil; the platform still owns semantic contracts, identity integration, policy, recovery, and consumer experience.

## Failure Modes and Misconceptions

- “Everything asynchronous is an event” erases command acceptance and result semantics.
- “Published means completed” confuses broker acknowledgement with consumer business effect.
- “CloudEvents defines my domain schema” confuses envelope interoperability with payload meaning.
- “The event ID is the aggregate ID” prevents multiple occurrences for one subject.
- “A new retry gets a new event ID” defeats deduplication after ambiguous publication.
- “Timestamps establish order” ignores clock skew, batching, network delay, and partitions.
- “Kafka gives global order” ignores partition-scoped ordering.
- “Exactly once means an email/cloud call happens once” extends a bounded guarantee past its transaction boundary.
- “Offset committed means effect committed” ignores early acknowledgement and consumer defects.
- “An in-memory dedup cache is enough” loses history on restart and cannot cover long replay.
- “The broker is the source of truth” confuses retained claims with current authoritative state.
- “CDC rows are domain events” couples consumers to persistence and transaction artifacts.
- “Outbox means downstream exactly once” solves publication atomicity, not every consumer effect.
- “More consumers always reduce lag” ignores partitions, hot keys, downstream quotas, and rebalances.
- “Retry forever is reliable” converts permanent defects into resource exhaustion.
- “Dead-letter queues prevent loss” is false if nobody owns, alerts, repairs, and redrives them.
- “Replay is read-only” ignores emails, provisioning, billing, webhooks, and destructive effects.
- “Compaction deletes sensitive history” overstates transport-specific cleanup across replicas and backups.
- “Tenant field is authorization” trusts producer-controlled metadata without identity binding.
- “Trace context proves caller identity” treats observability input as a security credential.
- “One channel simplifies governance” often creates coupled ACL, retention, schema, and blast radius.
- “One topic per event is always clean” can create unowned operational sprawl.
- “Consumer lag proves correctness” misses validation drops, bad projections, and external failures.
- “No current traffic means safe deletion” misses offline consumers and replay/restore dependencies.
- “Multi-region mirroring is transparent” ignores loops, conflict, duplicate, order, and residency.
- “A schema-compatible change is semantically compatible” ignores changed units, meanings, and defaults.

## Worked Examples

### Example 1

An environment API receives command `CreateEnvironment`. It persists request identity and desired state, then emits `environment.requested.v1`. A vendor controller consumes the event as work only if its contract explicitly owns that command-like subscription. After provider readiness evidence, the environment authority emits `environment.ready.v1`. Portal notification and current status remain separate.

This naming makes acceptance, intent, and observed readiness distinct. A failed vendor attempt emits or records an operation outcome under the workflow contract; it does not rewrite the original requested occurrence.

### Example 2

A service broker finishes binding `bind-5`. Broker database update and outbox event commit together. The event contains binding ID, instance ID, identity reference, generation, and expiry but never secret value. Catalog and evidence consumers receive the same occurrence in independent groups.

If publication response is lost, relay resends identical source/ID. Each group deduplicates in its own namespace. A later credential rotation is a new occurrence with a new ID and causation reference to the requested rotation.

### Example 3

Policy platform publishes bundles. All events for bundle subject `prod-baseline` use that subject as key, and payload contains immutable digest and version. Consumers reject sequence gaps, fetch the immutable bundle by digest, verify signature, stage it, then report activation through a separate status authority.

Delivery does not prove enforcement. The platform measures published, downloaded, verified, activated, and effective policy independently and reconciles workload coverage.

### Example 4

A cost consumer calls a billing provider after receiving `account.vended.v1`. Provider commits charge record but its response times out. The consumer cannot safely mark failure or blindly retry with a new token.

It passes stable idempotency key derived from consumer plus event identity. On retry, provider returns the original charge. Consumer records provider receipt and event receipt atomically, then acknowledges. Without provider idempotency, it would enter a reconciliation workflow.

### Example 5

A vulnerability stream includes tenant, repository, advisory identifier, severity, and resource reference. Payload excludes source code and credentials. Subscription controller binds workload identity to authorized tenant filters; browse and quarantine require separate roles.

A malicious producer cannot claim another tenant because gateway maps authenticated identity to allowed source/tenant. Metrics use severity and bounded result labels, never repository or advisory text.

### Example 6

One tenant generates 70% of deployment events using tenant ID as partition key. Its partition is hot while others idle. Adding consumers cannot split that key.

The team changes the ordering requirement to deployment ID, retaining per-deployment order while distributing the tenant. A new channel/version migrates consumers because changing key mapping in place would alter ordering semantics. Tenant fairness remains enforced by quotas.

### Example 7

A consumer version rejects a newly required enum value despite schema checks claiming compatibility. Messages enter quarantine with original identity, schema reference, consumer version, and safe error. Operators stop producer rollout, ship a tolerant reader, and shadow-redrive selected events.

They do not edit originals. If a corrected semantic event is needed, the producer authority emits a new correction occurrence referencing the original.

### Example 8

A catalog projection must be rebuilt from two years of events, but the topic retains 30 days. The catalog authority exports a signed snapshot at boundary `b`, and the consumer loads it into a shadow database. It then consumes after `b`, validates counts and ownership invariants, and cuts traffic over.

Two timestamps would not guarantee a gap-free handoff. The authority's boundary connects snapshot state to stream position.

### Example 9

Regional broker failure triggers mirror promotion. Mirrored events retain original source/ID and carry mirror provenance outside domain identity. Producers for each environment key are fenced so two regions do not concurrently author relative order.

Consumer receipts survive or replicate consistently. During failback, duplicate windows are expected and measured. Reconciliation compares provider environments with processed ready/suspended/deleted projections.

### Example 10

The platform retires `environment.ready.v1` in favor of `v2`. Producers dual-publish distinct occurrence identities connected by causation under documented semantics; consumers migrate and prove compatible output. The old type stops after the window, but its schema and decoder remain for required replay.

Only after observed and declared consumers, lag, mirrors, exports, quarantines, restore procedures, and legal retention are resolved does the team revoke ACLs and delete the old channel.

## Cross-Program Connections

- **API and Service Engineering:** event envelopes and AsyncAPI documents are public contracts with versioning, compatibility, authentication, quotas, and deprecation like synchronous APIs.
- **Distributed Systems:** partitions, retries, failure ambiguity, consensus, replication, clocks, and idempotency bound every delivery claim.
- **Data Engineering:** CDC, schemas, stream processing, watermarking, snapshots, replay, and data quality connect operational events to governed data products.
- **Database Engineering:** local transactions, uniqueness constraints, outbox tables, log positions, isolation, and restore determine producer/consumer atomicity.
- **Security Engineering:** workload identity, source claims, tenant filters, least privilege, encryption, redaction, key rotation, and admin separation protect retained fan-out.
- **Reliability Engineering:** SLOs, backpressure, retry budgets, poison isolation, lag, reconciliation, capacity, failover, and recovery exercises make eventing operable.
- **Observability Engineering:** messaging spans, trace links, metrics, logs, and bounded cardinality reveal the path but do not replace business evidence.
- **Software Architecture:** bounded contexts, authority, anti-corruption layers, coupling, event choreography, and directed orchestration determine component boundaries.
- **Cloud and Kubernetes Engineering:** controller watches, managed brokers, identity, autoscaling, zones, regions, and operator reconciliation provide runtime mechanisms with narrower semantics than domain truth.
- **Governance and Compliance:** classification, purpose limitation, retention, legal hold, audit integrity, deletion propagation, and evidence govern every replicated event copy.

## References

1. CNCF CloudEvents. [CloudEvents Specification](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md). Retrieved 2026-09-02.
2. CNCF CloudEvents. [CloudEvents Primer](https://github.com/cloudevents/spec/blob/main/cloudevents/primer.md). Retrieved 2026-09-02.
3. CNCF CloudEvents. [JSON Event Format](https://github.com/cloudevents/spec/blob/main/cloudevents/formats/json-format.md). Retrieved 2026-09-02.
4. AsyncAPI Initiative. [AsyncAPI Specification 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0). Retrieved 2026-09-02.
5. Apache Kafka. [Introduction and Core Concepts](https://kafka.apache.org/documentation/). Retrieved 2026-09-02.
6. Apache Kafka. [Design: Message Delivery Semantics](https://kafka.apache.org/40/design/design/). Retrieved 2026-09-02.
7. Debezium. [Outbox Event Router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html). Retrieved 2026-09-02.
8. Debezium. [Exporting CloudEvents](https://debezium.io/documentation/reference/stable/integrations/cloudevents.html). Retrieved 2026-09-02.
9. OpenTelemetry. [Semantic Conventions for Messaging Spans](https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/). Retrieved 2026-09-02; development-status guidance is qualified.
10. W3C. [Trace Context Recommendation](https://www.w3.org/TR/trace-context/). November 2021. Retrieved 2026-09-02.
11. Kubernetes. [Kubernetes API Concepts: Efficient Detection of Changes](https://kubernetes.io/docs/reference/using-api/api-concepts/). Retrieved 2026-09-02.
12. NIST. [SP 800-204A: Building Secure Microservices-based Applications Using Service-Mesh Architecture](https://csrc.nist.gov/pubs/sp/800/204/a/final). May 2020. Retrieved 2026-09-02.
13. IETF. [RFC 8949: Concise Binary Object Representation](https://datatracker.ietf.org/doc/html/rfc8949). December 2020. Retrieved 2026-09-02.
14. Kleppmann, Martin. [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/). O'Reilly Media, 2017.

## Exercises

### Exercise 1

Classify `CreateAccount`, `AccountRequested`, `AccountReady`, an audit login record, a Kubernetes watch update, a database row change, a trace span, and a portal badge. For each, identify authority, consumer expectation, and whether replay may cause an effect.

### Exercise 2

Design the event contract and topology for environment lifecycle across portal, vendor controller, catalog, cost, security evidence, and notification consumers. Specify envelope, schemas, keys, groups, ACLs, retention, and business completeness checks.

### Exercise 3

Prove or refute: “A transactional Kafka consumer guarantees exactly one cloud account is created for every account event.” State the failure model and design the safe boundary.

### Exercise 4

Design recovery after the producer database and broker are restored to different points. Include outbox identity, duplicate windows, consumer receipts, external effects, reconciliation, and live-traffic protection.

### Exercise 5

Plan migration and retirement of a sensitive event type used by 43 known groups, unknown direct consumers, two regional mirrors, a 90-day replay obligation, offline analytics, and quarantined messages.

## Answers to the Exercises

### Answer 1

`CreateAccount` is a command: requester expresses intent to the account authority, which may reject it; replay is unsafe without command identity and idempotency. `AccountRequested` is an event only when the authority durably accepted a distinct request occurrence. `AccountReady` is an event after readiness evidence under the account contract. Both can be replayed to duplicate-safe projections, but effectful subscribers require receipts.

An audit login record is purpose-built evidence with integrity, access, and retention requirements; it may describe an occurrence but ordinary event transport does not automatically satisfy audit. A Kubernetes watch update is an API change observation with resource-version/watch semantics, useful for reconciliation but not automatically a durable domain event. A row change is CDC under database/log authority and may not express business meaning.

A trace span is diagnostic telemetry, not business authority and not authorization. A portal badge is a derived presentation state, normally from a query or projection. Rebuilding it may replay input safely only if its update is idempotent. Each artifact retains its own truth and lifecycle boundary.

### Answer 2

The environment authority owns requested, provisioning, ready, suspended, failed, and deleted semantics; vendor controller owns provider-attempt observations only if distinct. Use CloudEvents-profile source/ID/type/subject/time/schema/content type, authenticated tenant route, causation, and environment ID as partition key. Use immutable versioned schemas with bounded non-secret payloads.

Separate sensitive lifecycle from broad notifications if ACL/retention differ. Portal catalog, cost, evidence, and notification each receive an independent logical group; replicas share within a group. Vendor work is a directed command/subscription contract rather than pretending every event listener may provision.

ACLs bind producer workload to source/type/tenant and each group to required types/tenants; browse, replay, schema, quarantine, and administration are distinct. Retention covers maximum supported outage and 90-day replay only if classification permits; longer rebuild uses snapshot plus stream. Quotas isolate replay and noisy tenants.

Checks include environment authority versus catalog projection, provider inventory versus ready/deleted state, requested-to-terminal age, unmatched cost records, evidence activation, notification terminal failure, oldest lag, schema/auth rejection, and orphaned subscriptions. Broker publication alone satisfies none of these business checks.

### Answer 3

Refute the unqualified statement. Kafka can atomically cover consumed offsets and Kafka-produced records under its transaction contract. Suppose the cloud provider commits account creation, then its response or the consumer process is lost before Kafka transaction commit. Redelivery cannot distinguish provider commit from no commit.

Retry with a fresh provider request can create two accounts; suppressing retry can create zero in the no-commit execution. The indistinguishable executions establish the ambiguity.

Use stable account request/operation identity as provider idempotency key. Persist command/event receipt, provider request identity, provider account reference, and workflow state durably. On ambiguity, query/reconcile provider resources by immutable metadata rather than generate a new identity. Commit input progress only after durable workflow handoff, and emit outcome through an outbox or covered Kafka transaction. Exactly-once wording must name this provider protocol and boundary.

### Answer 4

Record restore points for domain database, outbox log/checkpoint, broker partitions, schemas/ACLs, consumer offsets, receipt stores, and provider systems. Fence producers and effectful consumers until identity and interval analysis is complete. The database may contain outbox rows already published before the broker restore, or omit rows for broker events that survived.

Relay republishes restored outbox occurrences with original source/ID, never freshly generated IDs. Determine duplicate/loss windows from transaction/log positions and broker restore boundary. Consumers retain or restore receipts; where receipt state is older than events, rebuild it from business uniqueness constraints or reconcile effects before redelivery.

Inventory external effects by stable operation/idempotency metadata. Adopt committed effects, retry confirmed absent ones, and quarantine ambiguity. Compare authoritative environment/account inventory with events and projections. Resume bounded shadow consumers first, rate-limit replay below reserved live capacity, then reopen live production and effectful groups with monitoring and abort criteria. Record all recovery provenance.

### Answer 5

Freeze incompatible change and register owner, classification, replacement type/schema, compatibility window, and 90-day decoder obligation. Inventory declared groups plus observed principals, ACLs, offsets, traffic, mirrors, connectors, exports, schema fetches, quarantines, and offline owners. Direct consumers must register or lose access by a published deadline.

Dual-publish old/new under explicit semantic mapping or provide a governed translator with new source/IDs and causation. Migrate cohorts using shadow consumption and projection comparison. Sensitive payload minimization, tenant ACLs, regional residency, mirror deletion, and quarantine access/expiry are verified for both versions.

After producers stop the old type, wait through the agreed outage window and prove known groups drained or were deliberately abandoned. Preserve schema/decoder and authorized retained data through the 90-day replay obligation; offline analytics receives a bounded migration or snapshot contract. Redrive or dispose quarantines under owner approval before deleting their decoder.

Then revoke old publish/subscribe/browse/replay ACLs, stop mirrors and connectors, delete retained copies/backups according to policy, remove catalog/AsyncAPI entries or mark retired, and retain required audit evidence. Zero live traffic alone is insufficient because replay, offline, mirror, and quarantine obligations remain.
