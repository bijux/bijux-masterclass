---
module_id: API-070
program: API & Service Engineering
level: 2
module_number: 70
title: Designing an Asynchronous API for Replay and Evolution
status: complete
last_verified: 2026-09-02
---

# Designing an Asynchronous API for Replay and Evolution

## One-Page Review

### Governing question

How should an asynchronous API expose immutable facts, commands, channels, schemas, delivery behavior, ordering, replay, migration, failure recovery, and operations so that new consumers can evolve or rebuild state without repeating unsafe business effects?

### Essential definitions

- An **asynchronous API** is the governed contract through which applications send/receive messages over channels with named operations, semantics, bindings, and lifecycle.
- A **live path** carries newly accepted messages under normal latency and delivery policy; a **replay path/run** deliberately reprocesses an explicit historical range for a stated purpose.
- A **replay range** is bounded by source/channel/partition and time/offset/event/subject high-water coordinates plus inclusion rules.
- A **projection rebuild** reconstructs derived state from retained events/snapshots without re-executing unrelated business effects.
- A **replay run identity** names one authorized execution, while every original event retains its logical identity and occurred time.
- A **snapshot plus delta** restores a validated state snapshot at high-water $h$, then applies compatible later events.
- A **migration epoch** identifies a coordinated coexistence/cutover of channel, key, schema, or event-type topology.
- **parity** is verified agreement between authoritative facts and old/new projections or publications under declared invariants.

### Central model, mechanism, or theorem

An asynchronous API is safe for replay/evolution only if its contract closes the loop

$$
source\ state\rightarrow outbox\rightarrow channel\rightarrow inbox/effect\rightarrow derived\ state\rightarrow reconciliation,
$$

while preserving event identity $m$, type/schema $	au,s$, subject key/version $(k,v)$, and lineage across live, retry, dead-letter, bridge, and replay attempts. Replay run $r$ adds provenance and control metadata but never changes $m$ into a new business occurrence. Effecting consumers either isolate replay or deduplicate stable effect identities.

### Critical invariants

Commands, events, queries/replies, and notifications have distinct semantics and owners. Channel names/topology, message types, envelope/application headers, schema/compatibility, identity, partition key/order, retention/compaction, delivery/ack/retry/DLQ, security, quotas, and lifecycle are explicit in machine and human contracts. Source state and publication use an outbox/equivalent durable bridge; consumers use inbox/idempotency/effect ledgers.

Replay specifies who, why, exact source/range, preserved identity/time/order, consumer/artifact/schema/upcaster, destination/isolation, authorization, deadline policy, effect mode, capacity/rate/fairness, checkpoint/resume, observability, validation, stop/rollback, and disposition. Historical schemas/upcasters/snapshots remain available. Breaking evolution uses compatible readers, new types/channels/epochs, dual publication from one source, parity, high-water cutover, and evidence-based retirement.

### Common failures

Calling a topic name the whole API; mixing commands and facts; one envelope field named `version`; producer DB commit separate from publish; correlation ID used as event ID; partition key omitted; claiming topic-wide order; ack before durable state; external effects without stable IDs; retry and DLQ lose identity; retention shorter than recovery promise; compaction mistaken for complete history; offset reset with no run record; replay into live effecting consumer group; new IDs/timestamps on replay; old authorization/deadline ignored; full-speed replay starves live traffic; current schema cannot read archives; dual publication creates two facts/effects; no parity/rollback; and deleting old contracts before dormant/archive consumers migrate.

### Compact example

An order-search projection needs rebuilding after a bug. The API contract identifies the compacted snapshot topic, event delta topic, schema registry, original event IDs and order versions, and replay-only consumer scope. A run loads snapshot high-water, applies later events per order, writes a new isolated index, checkpoints source ranges, and compares counts/checksums/queries. Payment and email handlers cannot subscribe to the replay destination. Reads cut over only after parity; rollback restores old index routing. **Conclusion:** replay is a controlled projection deployment, not a broadcast of “new” orders.

### Connections

[Commands, Events, and Messages](061-commands-events-and-messages.md) through [Event Versioning](069-event-versioning.md) supply the component contracts: schemas, channels, ordering, delivery, idempotency, dead letters, and evolution. This capstone assembles them into one reviewable asynchronous API and prepares the reliability/performance modules that follow.

## Governing Question

What complete machine-readable and operational contract lets independent producers and consumers deploy, fail, retry, replay, migrate, and retire while preserving domain truth, bounded delivery behavior, safe effects, and verifiable recovery?

## Why This Matters

An event payload schema is not an asynchronous API. Consumers also depend on who emits the message and why, which channels carry it, how identity and order work, whether duplicates/gaps occur, when acknowledgement is safe, how long data remains, how authentication/authorization apply, and what operators do during replay, dead letter, migration, or disaster.

Replay amplifies every omission. Resetting an offset can resend millions of facts, reorder them relative to live traffic, exceed quotas, exhaust downstream databases, invoke payments/emails again, expose historical personal data, and fail when old writer schemas are gone. A provider archive or rewind facility transports events; it does not determine business safety.

Evolution creates mixed systems across time and topology. New schemas coexist with old consumers. A partition-key migration places one subject's history in two routes. Dual publication can create duplicate business facts. Compacting a log retains latest keyed state but may remove intermediate transitions. Snapshot and delta can disagree at their boundary. Rollback must tolerate events already emitted under the candidate version.

The design goal is not to eliminate asynchronous uncertainty. It is to allocate each invariant to a specific producer, broker, consumer, store, control plane, and operator; preserve evidence; and verify the full lifecycle. AsyncAPI can describe applications, operations, channels, messages, schemas, security, and protocol bindings, while companion human/operational contracts carry semantics and runbooks that the specification does not prove.

## Prerequisites and Retrieval

Retrieve [Commands, Events, and Messages](061-commands-events-and-messages.md), [Event Schema Design](062-event-schema-design.md), [AsyncAPI Contracts](063-asyncapi-contracts.md), [Topic and Channel Design](064-topic-and-channel-design.md), [Ordering and Partition Keys](065-ordering-and-partition-keys.md), [Delivery and Acknowledgment](066-delivery-and-acknowledgment.md), [Idempotent Consumers](067-idempotent-consumers.md), [Dead-Letter Handling](068-dead-letter-handling.md), and [Event Versioning](069-event-versioning.md).

Retrieve the domain state machines and owners; source transaction/outbox; selected broker/provider/bindings; topology/configuration/IAM/encryption; AsyncAPI and schema artifacts; registry subjects/fingerprints/history; all producers/consumers/bridges; retention/compaction/snapshot/archive behavior; offsets/checkpoints; idempotency/effect ledgers; retry/DLQ/redrive; replay tooling/approvals; SLOs/quotas/cost; and disaster restore evidence.

## Learning Objectives

After completing this module, you can:

1. derive an asynchronous API from domain intents, facts, invariants, and ownership;
2. describe applications, operations, channels, messages, schemas, bindings, security, and lifecycle;
3. design identity, causation, correlation, partitioning, order, delivery, and effects together;
4. select retention, compaction, archive, snapshot, and delta mechanisms for recovery claims;
5. specify replay runs with exact scope, isolation, authorization, rate, checkpoint, and closure;
6. rebuild projections without executing payments, notifications, or other unrelated effects;
7. evolve schemas, types, channels, keys, and regions through mixed-version coexistence;
8. control dual publication, translation, parity, high-water cutover, rollback, and retirement;
9. secure and observe live/retry/DLQ/replay/migration control and data planes; and
10. verify the API with contract matrices, model/property tests, fault injection, replay, and reconciliation.

## Core Exposition

### Start from domain semantics and ownership

List business intents, state transitions, immutable facts, outcomes, and observers before choosing topics. A command requests one authority to decide; an event states a completed fact; a reply/outcome correlates to an intent; a notification is an effect request or delivery fact with its own semantics. Do not use one vague `OrderMessage` for all four.

For each message define producer/source-of-truth, authorized senders, intended consumers, subject, trigger, preconditions, occurred/recorded time, identity, causation/correlation, finality/correction, privacy/retention, and domain invariants. State whether consumers may treat it as transition/delta, complete state, signal to query current state, or workflow command.

Assign owners for contract, producer correctness, channel/platform, registry/schema, consumer effects, retry/DLQ, replay approval/execution, privacy, and incident response. Consumers cannot safely evolve against an unowned event whose meaning changes informally.

Write non-goals. If the stream is not an audit ledger, source of truth, global chronology, or legal record, say so. If consumers must query authoritative state for current truth, document availability and reconciliation behavior.

### Model applications, operations, channels, and messages

AsyncAPI 3.0 describes application send/receive operations separately from channels and reusable messages. Model the API from each application's perspective: which operation sends or receives which message on which channel/server. Use protocol bindings only for protocol-specific details and keep domain semantics portable.

Channel address/name is durable infrastructure API. Specify environment/tenant/region scope, ownership, allowed message set, partition count/change policy, retention/compaction, max payload, throughput/quota, encryption, access policy, replication/failover, lifecycle, and retry/DLQ/replay companions. Avoid embedding temporary implementation or team names.

One channel can carry multiple message types only with an unambiguous discriminator and compatible retention/order/security/consumer needs. Split when ownership, sensitivity, retention, scale, ordering key, failure isolation, or lifecycle differ. Do not create one topic per consumer when one fact contract serves independent subscriptions; do not force unrelated facts into one topic for convenience.

AsyncAPI validation can confirm document structure/references/examples and channel-message declarations. It cannot prove broker resources/configuration match the file. Reconcile deployed topology/IAM/config with contract as code.

### Define a stable event envelope

Use distinct fields for envelope spec/version, source, stable logical event ID, event type/major, occurred/recorded time, subject/tenant, subject version, causation/correlation, data schema/fingerprint/content type, partition/ordering key version, producer artifact, deadline where meaningful, and trace context. Optional extensions have owner and format.

CloudEvents supplies interoperable context attributes such as `id`, `source`, `type`, `specversion`, `subject`, `time`, `datacontenttype`, and `dataschema`. Its specification leaves domain payload semantics/versioning to the producer. Map application identity and tenant/order versions explicitly; do not overload `specversion` or correlation ID.

Message ID remains stable across producer retry, broker redelivery, retry/DLQ, bridge, archive, and replay. If one occurrence is deliberately represented by v1/v2 events, document whether they use distinct event IDs with shared causation/occurrence ID; never let the same ID resolve to different semantic content.

Canonical fingerprint binds identity to immutable semantic input. Limit and validate metadata, protect sensitive identifiers, and ensure bridges preserve required fields. Trace headers help diagnosis but do not authorize processing or deduplicate effects.

### Contract payloads and evolution

Bind every message type/revision to an immutable writer schema identity and human semantic contract. State serialization/dialect, required/optional/default/unknown behavior, units/precision/timezone, identifiers, enums, constraints, examples, privacy, and compatibility direction/history.

Registry subject naming aligns with event ownership/type; compatibility is enforced in CI and server-side. Retain writer schemas for the data horizon. Test actual serializers/readers/upcasters across languages, encodings, active/rollback versions, and archives. A schema that passes structural checks still needs domain review.

Compatible additive changes keep stable event type when old readers tolerate them and new readers interpret absence honestly. Breaking meaning/wire/key uses a new type/major or channel/migration epoch. Upcasters are deterministic and preserve original ID/time/version/evidence; missing historical facts stay unknown.

Document deprecation from introduction: replacement, compatibility window, producer/consumer adoption evidence, backlog/archive/replay boundary, stop date conditions, rollback, and schema retention. Time alone cannot prove dormant consumers migrated.

### Align publication with source state

When a state change and event must agree, persist domain state plus an outbox/log record in one source transaction. The publisher sends the same event ID/content until broker acceptance is known and marks publication state idempotently. Lost responses do not generate new facts.

Define source-to-event completeness reconciliation: each committed relevant state transition has exactly the expected outbox/event set; each published event maps to a source transition; schemas/types/versions match. Monitor unpublished age, attempts, broker confirmation, duplicates, and high-water.

CDC can publish committed changes, but raw row changes are not automatically stable domain events. Define transaction grouping, before/after semantics, deletion/tombstone, ordering, schema change, snapshot, and privacy. A broker log is source of truth only if the domain explicitly assigns that authority and durability/recovery support the claim.

Multi-region writers need one authority/fencing epoch or a proven conflict/merge model. Mirroring preserves application IDs/types/keys/versions even if offsets and provider IDs change.

### Specify delivery, acknowledgement, and effects

State producer durability settings, broker replication/retention, subscription/group model, at-most/at-least/exactly-once scope, lease/visibility, ack/nack, retry/backoff/attempt/age, deadline/expiry, DLQ, redrive, batch/cumulative checkpoint, and provider/version limitations.

Choose consumer acknowledgement after the earliest durable recoverable boundary. A short local transaction atomically claims inbox, checks fingerprint/subject version, mutates projection/domain state, stores outcome, writes derived outbox, and commits. Long work durably stages an inbox/work record then acknowledges; application owns later retry/backlog.

External effects use stable effect IDs, durable ledgers, provider idempotency/query where available, uncertain states, and reconciliation. Broker exactly-once or transactional output does not automatically include payment, email, search, or another database.

Define what duplicates, stale events, gaps, conflicts, validation/domain rejection, timeout, and cancellation mean. Delivery metrics, application acceptance, effect completion, and workflow outcome remain separate.

### Specify partitioning and order

Derive the smallest stable domain subject whose noncommutative transitions require order. Define canonical key bytes/normalization/tenant, partitioner/version/count, subject sequence authority, multi-writer fencing, and provider order scope. “The topic is ordered” is incomplete.

Consumers serialize or correctly merge per key, atomically maintain last subject version/inbox/state/checkpoint, and classify duplicate/stale/next/gap. Concurrent processing across keys is bounded. Retry/DLQ cannot silently let a later required transition overtake.

Partition count/partitioner/key changes are migrations, not transparent capacity knobs. Use routing epochs/new channels, preserve event IDs/subject versions, dual route from one source, backfill, shadow state, parity, high-water cutover, rollback, and retirement.

Cross-subject workflows use explicit transaction/workflow/causation state, not offset/timestamp comparison across partitions. Global display order is not necessarily a total domain order.

### Design retention, compaction, archive, and snapshots

Start from recovery questions: how far back must a consumer replay; must every transition remain, only current keyed state, or a legal audit; what is RPO/RTO; how are deletes represented; what schemas/keys/encryption must survive; and who pays for storage/egress/reprocessing?

Time/size deletion retention provides a bounded event history. Compaction retains selected/latest records by key but can remove intermediate transitions; it is appropriate for restoring latest keyed state only when key/tombstone semantics are correct. Kafka documents that consumers can rewind offsets and that compaction preserves at least final keyed state while offsets may point over removed records. Do not call a compacted changelog complete audit history.

Archive can extend replay beyond hot broker retention. Provider replay facilities may restrict destination and add metadata; application identity/effect policy still governs. Verify archive selection, encryption, schema availability, index/search, restore throughput, and retention/deletion/legal policy.

A snapshot records complete projection/domain state at source high-water $h$ with schema/version, source ranges, counts/checksums, creation method, encryption, and validation. Replay loads snapshot then applies events strictly after $h$ under compatible semantics. Snapshot and delta must share a consistent cut; otherwise missing/double-applied boundary records corrupt state.

### Define the replay contract

Every replay request/run records:

1. run ID, requester/approver, purpose, ticket/change, risk tier, and expiry;
2. source environment/region/channel/subscription/partitions and immutable range/high-waters;
3. selection/filter and whether source retention/compaction makes it complete;
4. original event IDs/types/times/keys/subject versions/schema identities and preserved bytes;
5. target application/consumer artifact/config/upcasters and isolated destination/state;
6. effect mode: projection-only, compare-only, explicitly allowed idempotent effects, or prohibited;
7. current authorization/privacy/deletion/deadline policy and historical-context rules;
8. rate, concurrency, bytes, per-tenant/key fairness, quotas, cost, and live-traffic budget;
9. checkpoint/resume/cancel, retry/DLQ, operator ownership, and retention;
10. expected invariants/counts/checksums/parity, stop/rollback, final disposition, and audit.

Replay transport adds `replayRunId`/provider metadata without replacing logical event identity or occurred time. Recorded/ingest time can reflect replay attempt separately. Consumers must never interpret replay as a new customer action.

Use a separate consumer scope/group and isolated output when rebuilding. Do not broadcast an archive back to all live effecting subscribers unless each is explicitly eligible and idempotency/effect retention covers the range. Prefer source archive→controlled replay channel→named rebuild consumer.

### Bound replay capacity and time

If replay contains $N$ events averaging $b$ bytes and sustainable replay processing rate is $\mu_r$ events/s, ideal duration is $N/\mu_r$ and source read volume is about $Nb$, before compression, indexes, retries, output writes, and validation. Safe $\mu_r$ is spare end-to-end capacity, not maximum broker throughput.

Model broker egress, registry/cache, network, consumer CPU/memory, database IOPS/locks/log, downstream services, DLQ/case store, and output/index capacity. Limit global and per-tenant/key concurrency/bytes/age. Preserve live SLO/error-budget headroom and cost budget.

Start representative canaries across age/schema/partition/tenant/failure classes. Ramp in stages only while decode/upcast, duplicates/gaps, processing latency, state invariants, live traffic, DLQ, and resource saturation remain healthy. Automatically pause on divergence or uncertainty.

Checkpoint at durable target boundaries with source coordinates and state checksum/high-water. Resume idempotently after crash; cancellation stops new work and accounts for in-flight/committed results. Estimate remaining time from measured throughput and skew, not nominal rate.

### Isolate and validate projection rebuilds

Projection rebuild creates a new target namespace/index/table/version. It consumes snapshot/history with a dedicated consumer identity whose credentials cannot charge, email, ship, or publish business commands. Derived non-effecting outputs remain run-scoped until promotion.

Validate per-subject last version/gaps, record counts, key cardinality, aggregates, checksums, referential/domain invariants, deletion/tombstone handling, representative queries, performance, and privacy filters. Compare old/new at aligned high-water; aggregate equality alone can hide swapped/missing records.

Use shadow reads/dual queries before cutover. Promotion changes read routing/alias atomically where possible; old projection remains for rollback through observation window. Any live delta accumulated during rebuild is caught up at an explicit high-water barrier or continuously dual-applied with parity.

Record run artifact/schema/upcaster/source range/checksums and final disposition. Retire old projection only after cutover/rollback window and data-retention policy.

### Evolve types, channels, and keys

For compatible schema evolution, deploy readers first, register immutable candidate, shadow/canary producer, observe writer-version adoption, and preserve rollback. For breaking event type, consumers accept old/new before source dual publication; one outbox transaction produces representations with shared occurrence lineage and stable effect identity policy.

For channel/key migration, create new epoch/channel, backfill retained history in subject order, dual route live from one authoritative source, and use consumer inbox to deduplicate across paths. Compare counts/fingerprints/versions/gaps/state at source/new high-waters. Do not use independent producers that can diverge.

Pause cutover on parity gaps, hot-key overload, region lag, schema conflicts, unknown consumers, DLQ growth, or external-effect divergence. Rollback routes reads/consumers to old path while dual publication still covers both. After migration, stop old writes, drain, reconcile, observe maximum dormant/replay window, then retire policy/config/schema only when history no longer needs them.

Replay during migration uses an explicit routing epoch and target. A historical event should not be consumed by both old and new effecting paths unintentionally. Document bridge/translator idempotency and lineage.

### Secure control and data planes

Authenticate producers and consumers with least-privilege channel permissions; authorize message intent/domain subject, not only broker connection. Bind tenant/source identity and validate envelope/schema/signature where required. Encrypt transport/storage/archive/snapshots/DLQ and govern keys through restore horizon.

Replay/redrive/schema registration/channel creation/compatibility weakening/retention deletion are privileged control-plane actions. Use approved service workflows, immutable ranges/destinations, separation of inspect versus execute, time-bound credentials, rate limits, multi-party approval for high-risk effects, and complete audit.

Historical replay must apply deletion/legal hold/purpose limitation and current vulnerability controls. Do not resurrect deleted personal data from an archive without lawful policy. Inspection and schema/upcaster parsing treat payload as hostile: size/decompression/time limits, no active rendering or arbitrary URL fetch.

Prevent cross-tenant selection, outcome enumeration, destination injection, schema poisoning, replay forgery, and forged `replayRunId`. Metadata inside an event cannot authorize its own replay.

### Publish one coherent contract package

The package includes AsyncAPI document; schemas and compatibility policy; semantic catalog/examples; topology/binding/config/IAM declarations; producer/consumer identity/order/delivery tables; SLO/quotas/cost; retry/DLQ/redrive; replay/snapshot/retention; evolution/deprecation/migration; security/privacy; dashboards/alerts; runbooks; and test/reconciliation evidence.

Trace each domain invariant to producer, broker, consumer, store, control, and verification. Mark what is normative contract, provider behavior, configuration, recommendation, or measured SLO. Pin versions and retrieval dates for external semantics.

Generate client/docs/config where useful but review generated artifacts. Keep deployed channel/registry/IAM inventories reconciled. Changes follow ownership, compatibility/impact review, staged rollout, and rollback—not ad hoc console mutation.

### Verify the complete lifecycle

Contract tests validate AsyncAPI, references, schemas/examples, compatibility matrix, serializer/deserializer/upcaster, canonical keys, and envelope invariants. Model/property tests generate duplicates, gaps, reorder, unknown fields/types, and subject transitions while asserting idempotency/order/domain state.

Integration/fault tests cover source/outbox crash windows, broker failover, ack loss, lease/rebalance, retry/DLQ forwarding, poison, registry unavailable/stale, bridge/mirror metadata, region partition, external timeout-after-success, retention/compaction edges, snapshot cut, archive replay, cancellation/resume, dual-publication partial failure, migration rollback, and disaster restore.

Load tests mix live, duplicate, retry, dead-letter, and replay traffic with realistic key skew and payload/schema distributions. Verify backpressure, live SLO isolation, quotas, cost, checkpoint progress, and no control-plane bypass.

Reconciliation proves source transitions↔outbox↔broker/archive↔inbox/effect/outbox↔derived state plus final workflow/dispositions. Successful broker metrics alone do not prove API correctness.

## Definitions and Notation

Let logical event $m$ have source/type/schema $(src,\tau,s)$, subject key/version $(k,v)$, occurred time $t_o$, and effects $e_j(m)$. Let live attempts be $a_i$ and replay run $r$ re-deliver the same $m$ with separate attempt/recorded metadata.

Let replay range contain $N$ events of mean size $b$, sustainable end-to-end replay rate $\mu_r$, live arrival $\lambda_l$, and shared safe service capacity $\mu$. Stability with headroom requires $\lambda_l+\mu_r<\mu$ at every bottleneck, not only broker. Ideal replay duration is $N/\mu_r$; raw source bytes are approximately $Nb$ before compression/overheads.

Let snapshot $S_h$ represent state at verified source high-water vector $h$ across partitions. Correct restore applies $S_h$ once and each eligible event strictly after its coordinate in $h$, preserving per-subject version invariants.

## Mechanisms, Invariants, or Proof Structure

1. Derive commands/events/outcomes from domain authority, state machines, effects, and owners.
2. Describe application operations, channels/messages, protocol bindings, schemas, security, and lifecycle.
3. Preserve stable identity/fingerprint, causation, key/version, time, and schema across every path.
4. Atomically bridge source/outbox and consumer inbox/state/outbox; isolate external effect identity/reconciliation.
5. Specify delivery, acknowledgement, retry/DLQ, ordering, retention/compaction/archive, and snapshot boundaries.
6. Treat replay as an authorized immutable range/run with isolated consumer/effects, bounded capacity, checkpoints, and closure.
7. Evolve readers/schemas/types/channels/keys through compatible coexistence or explicit epochs and one-source dual publication.
8. Prove parity at aligned high-waters, preserve rollback, and retire only after live/dormant/replay evidence.
9. Secure data/control planes and apply privacy/deletion policy to historical processing.
10. Verify contracts, state properties, crash windows, load/fault/replay/migration, and end-to-end reconciliation.

Proof sketch: if source transition and outbox are atomic, each event identity/content is immutable, consumer local state/inbox/outbox are atomic and external effects are identity-protected, then redelivery/replay does not create additional intended effects within retained evidence. If replay range is complete relative to a verified snapshot/high-water and consumers deterministically apply compatible ordered events, rebuilt state equals the specified fold of source facts. Missing retained events/schemas, compaction of required transitions, nonisolated effects, inconsistent snapshot cut, or semantic incompatibility invalidates the conclusion.

## Alternatives and Trade-Offs

**Event log from origin versus snapshot plus delta.** Full log offers arbitrary point history but costs storage/time/schema support. Snapshot accelerates RTO but introduces high-water consistency and validation.

**Hot retention versus archive.** Hot log enables low-latency rewind at broker cost. Archive reduces hot cost but adds retrieval throughput, indexing, schema/key longevity, and restore operations.

**Deletion history versus compaction.** Deletion retention preserves transitions for bounded time. Compaction preserves latest keyed state but not every transition; use based on rebuild semantics, often separate topics.

**Replay to original bus versus isolated replay channel.** Original bus uses existing routing but risks every subscriber/effect. Isolated path is safer/auditable but requires explicit target consumer/tooling.

**Effect suppression flag versus credential/topology isolation.** Flag is flexible but can be ignored/misconfigured. Separate credentials/destination makes prohibited effects structurally harder; use both for high risk.

**Dual publication versus centralized translation.** Dual publish eases consumers but increases producer/topology/duplicate risk. Translator centralizes mapping but becomes critical lag/failure/lineage component.

**Compatible type evolution versus new type/channel.** Compatible minimizes migration surface but constrains meaning. New type/channel makes break visible at coexistence/retirement cost.

**Live-priority throttling versus dedicated capacity.** Throttling shares resources efficiently but makes replay duration variable. Dedicated capacity isolates SLO/cost but may sit idle and still share downstream bottlenecks.

## Failure Modes and Misconceptions

1. Topic address and payload schema are presented as the entire asynchronous API.
2. Commands, facts, outcomes, and notifications share ambiguous message semantics.
3. Event ID, correlation ID, trace ID, schema version, and subject version are conflated.
4. Source state commits separately from publication without outbox/reconciliation.
5. Broker delivery guarantee is extended to arbitrary database/payment/email effects.
6. Topic-wide/global ordering is claimed from per-partition order.
7. Retry/DLQ/bridge/mirror/replay changes logical ID, key, version, or time.
8. Retention promise ignores registry schemas, encryption keys, payload objects, inbox/effect history, or archives.
9. Compaction is assumed to preserve all transitions/audit history.
10. Snapshot high-water is inconsistent, causing boundary gaps or double application.
11. Offset reset/replay has no immutable run range, owner, checkpoint, or disposition.
12. Replay broadcasts into live consumers and repeats payments/emails/notifications.
13. Replay ignores current authorization, expiry, deletion, or purpose limitation.
14. Nominal broker rate overwhelms database/downstream or starves live traffic.
15. Current reader cannot decode/upcast oldest retained events.
16. Dual publication creates divergent facts or two effects.
17. Migration compares aggregate counts without per-key/version/checksum parity.
18. Old path/schema/contract retires before dormant, archive, rollback, and disaster consumers are proven migrated.

## Worked Examples

### Example 1

`SubmitRefund` is a command to one payment authority with deadline/idempotency key; `RefundAuthorized` is an immutable outcome fact. They use separate types/operations and consumers cannot treat redelivery of the fact as a new command.

### Example 2

An order topic uses `(tenant,orderId)` key and `orderVersion`. Retry preserves both; a version gap pauses only that order lane. Cross-order analytics processes concurrently and makes no global-order claim.

### Example 3

A source database transaction writes order state and event outbox. Publisher times out after broker acceptance but retries the same ID/fingerprint. Consumer inbox suppresses duplicate projection/outbox effects.

### Example 4

A compacted customer-snapshot topic restores latest profiles, while a deletion-retained customer-lifecycle event topic supports time-bounded transition replay. The API does not promise historical sequence from the compacted topic.

### Example 5

Snapshot covers partition highs `[120,95,301]`. Restore loads its checksum then consumes strictly after each coordinate, not one scalar offset. Per-customer versions catch a missing/double boundary event.

### Example 6

An archive replay adds provider replay metadata/new delivery attempts but keeps CloudEvent source+ID, type, occurred time, schema, and subject version. Dedicated projection consumer writes isolated index and cannot call notification provider.

### Example 7

One billion archived events at safe end-to-end 25,000/s require at least 40,000 seconds, about 11.1 hours, before retries/skew/validation. Live-priority throttling and checkpoints make elapsed time longer but protect SLOs.

### Example 8

Breaking `InvoiceIssued.v2` dual publishes with v1 from one outbox. Both carry a common invoice occurrence/effect identity but distinct event IDs/types. Each consumer selects one representation; parity compares amounts/statuses before v1 retirement.

### Example 9

Partition key migrates customer→order. New routing epoch/channel backfills by order version, dual routes original IDs, shadows state, and cuts at aligned high-water. Random resharding in place would have split order history.

### Example 10

A disaster restores broker data but not matching registry mapping/encryption key. Fingerprint resolution fails closed and recovery halts. The runbook restores the log, registry, keys, inbox/effect state, snapshots, and contracts as one verified recovery set.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies logs, replication, partial failure, ordering, consensus, leases, and exactly-once boundaries. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies transactions, outbox/inbox, snapshots, CDC, migrations, and recovery.

[Data Engineering](../../19-data-engineering/ROADMAP.md) uses replay, backfill, checkpoints, compaction, stateful processing, data contracts, and parity. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns brokers, registries, IAM, quotas, observability, replay tooling, and disaster restoration.

[Security Engineering](../../25-security-engineering/ROADMAP.md) contributes producer/consumer authorization, control-plane privilege, data protection, deletion, hostile-input handling, and audit. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes requirements allocation, interface control, failure/hazard analysis, configuration management, verification matrices, and lifecycle closure.

## References

1. AsyncAPI Initiative. “AsyncAPI Specification 3.0.0.” <https://www.asyncapi.com/docs/reference/specification/v3.0.0>
2. Cloud Native Computing Foundation. “CloudEvents Specification 1.0.2.” <https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/spec.md>
3. Cloud Native Computing Foundation. “CloudEvents Primer 1.0.2.” <https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/primer.md>
4. Apache Software Foundation. “Apache Kafka 4.2 Design.” <https://kafka.apache.org/42/design/design/>
5. Apache Software Foundation. “Apache Kafka 4.2 Broker Configurations.” <https://kafka.apache.org/42/configuration/broker-configs/>
6. Amazon Web Services. “Archiving and Replaying Events in Amazon EventBridge.” Retrieved 2026-09-02. <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-archive.html>
7. Apache Software Foundation. “Apache Avro 1.12.0 Specification.” <https://avro.apache.org/docs/1.12.0/specification/>
8. Confluent. “Schema Evolution and Compatibility for Schema Registry.” Retrieved 2026-09-02. <https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html>

## Exercises

### Exercise 1

Design an asynchronous API contract for order fulfillment covering `SubmitOrder`, order facts, shipment commands/outcomes, notifications, and queryable status. Specify applications/operations, channels, envelope, schemas, identity/causation, keys/order, delivery/ack, effects, retry/DLQ, security, SLOs, retention, and ownership.

### Exercise 2

A replay contains 720 million events averaging 1.4 KiB. Live traffic is 18,000 events/s. The shared target safely sustains 42,000 events/s with required headroom. Compute maximum replay rate without violating that bound, ideal duration, and approximate raw read volume in decimal TB and TiB. Explain why the actual plan should start lower.

### Exercise 3

Design snapshot-plus-delta recovery for a 96-partition account projection. Define a consistent high-water vector, snapshot schema/checksum, event eligibility, per-account versions, parallelism, gaps/duplicates, checkpoint/resume, validation, RPO/RTO, and failure tests.

### Exercise 4

Plan a breaking event-type and partition-key migration for invoices while live traffic, retries, dead letters, two regions, and archived replay coexist. Include source authority/outbox, types/schemas, routing epochs, backfill, dual publication, identity/idempotency, parity, cutover/rollback, and retirement.

### Exercise 5

Write a replay safety design for rebuilding search and analytics from three years of orders while payments, emails, and shipments must never repeat. Include authorization, immutable range, schema/upcasting, isolation, rate/fairness, current deletion policy, checkpointing, dead letters, observability, reconciliation, promotion, rollback, and audit.

## Answers to the Exercises

### Answer 1

Model storefront as sender of `SubmitOrder` command to one order authority; order service receives/decides and sends facts such as `OrderAccepted`, `OrderRejected`, `OrderCancelled`; fulfillment receives a stable `PrepareShipment` command and sends `ShipmentPrepared|Failed`; notification service receives selected facts and records notification outcome. Queryable current status remains synchronous/read-model API or explicit request/reply with separate semantics, not an event masquerading as query.

Define AsyncAPI applications/operations and channel/message maps for command and fact channels. Each channel declares owner, address/bindings, tenant/region, allowed types, partition/retention/compaction, payload/throughput limits, encryption/IAM, replication/failover, retry/DLQ/replay companions, and lifecycle. Commands and events do not share a channel if authority, retention, sensitivity, or retry semantics differ.

Envelope uses source+event/command ID, type/major, occurred/recorded time, tenant/subject, order/shipment version, causation/correlation, dataschema/content type, canonical key version, producer artifact, command deadline, and trace context. Schemas are immutable registry subjects with semantic units/defaults/privacy and transitive policy matching replay. Key order facts/commands by scoped order or shipment subject; source assigns contiguous versions and multi-writer epoch.

Order state+outbox and fulfillment state+outbox are atomic. Consumers atomically use inbox/state/outbox and acknowledge after durable acceptance; external carrier/email uses stable effect ID/ledger/provider query. At-least-once duplicates are expected. Retry classifies transient versus invalid/expired/domain; DLQ retains identity/evidence with owned redrive. Gaps pause key, not all traffic.

Authenticate/authorize each producer/consumer and intent, isolate tenants, encrypt, cap payload/rate, protect PII, and audit schema/replay/redrive. Define publish-to-accept and outcome SLOs, lag/age/duplicate/DLQ/effect metrics, quotas/backpressure, retention/recovery horizon, replay effect isolation, and reconciliation source→outbox→channel→inbox/effect→workflow. Assign contract, domain, platform, registry, consumer, security, DLQ/replay, and incident owners.

### Answer 2

Maximum arithmetic replay rate at the shared target is $42{,}000-18{,}000=24{,}000$ events/s. Ideal duration is

$$
720{,}000{,}000/24{,}000=30{,}000\text{ s}=8.333\text{ hours}.
$$

At 1.4 KiB=$1.4\times1024=1433.6$ bytes, raw read volume is $720{,}000{,}000\times1433.6=1{,}032{,}192{,}000{,}000$ bytes, about 1.032 TB decimal. Dividing by $2^{40}$ gives about 0.939 TiB.

Start materially below 24,000/s because the 42,000 bound may be an average/bottleneck-specific estimate and live traffic bursts/skews. Replay also consumes registry/cache, network, database IOPS/locks/log, output/index, DLQ, and validation capacity; retries/duplicates increase work. Canary across schemas/partitions/tenants, reserve live error-budget headroom, apply per-key/tenant fairness, ramp by measured bottleneck, checkpoint, and pause on live SLO/invariant/DLQ/saturation signals.

### Answer 3

Pause or use a source-consistent snapshot protocol that records a 96-element high-water vector $h[p]$ in the same logical cut as exported projection/source state. Snapshot metadata includes ID, creation time/method, source topology epoch, each partition coordinate, schema/model/upcaster versions, account cardinality, per-shard and global checksums, deletion/tombstone policy, encryption/key, and validation status.

Restore snapshot into isolated target, then consume each partition strictly after $h[p]$. Preserve original IDs and account keys/versions. Bounded workers parallelize partitions and accounts but serialize noncommutative transitions per account. Inbox suppresses duplicates; lower versions are stale; expected next applies; higher is gap and pauses that account while retrieving retained event/authorized snapshot. Checkpoints atomically record durable target progress per partition plus target state/checksum epoch.

On crash, reload snapshot only if target generation is new; otherwise resume checkpoints idempotently. Cancellation stops new fetch and drains/accounts for in-flight. Validate every account's contiguous last version against authoritative sample/full reconciliation, counts/balances/invariants, deletions, per-partition source range/checksum, and representative queries. Catch live delta continuously or establish a barrier and final high-water before promotion.

RPO is the latest source coordinate included in snapshot+retained delta; RTO includes snapshot restore, delta volume/rate, validation, and cutover. Test crash at snapshot boundary, missing/double event, corrupt shard/checksum, schema/upcaster failure, partition resize, duplicate/reorder/gap, tombstone expiry, hot account, registry/KMS loss, region failover, checkpoint corruption, live catch-up, and rollback. Never replace vector with one scalar offset.

### Answer 4

Choose one authoritative invoice database/home-region epoch. Invoice transaction writes one outbox occurrence containing stable invoice ID/version and data sufficient to generate old/new representations. Introduce explicit `InvoiceIssued.v2` and new immutable schema/registry subject for changed meaning; keep v1 stable. Define new key/routing epoch and channel if partition subject changes. One publisher transaction/workflow derives both representations with common occurrence/causation and stable downstream effect identity, never two independent facts.

Deploy consumers that accept/select v2 first in both regions, including retry/DLQ/redrive, bridges, archives, rollback binaries, and dormant jobs. Create new topic with planned partitions. Backfill retained/archive history in invoice-version order using original occurrence IDs/evidence and migration-run metadata; do not execute invoice/payment/email effects. Consumer inbox deduplicates across backfill, dual route, retry, and DLQ.

Dual publish live v1/old-key and v2/new-key from one outbox. Shadow new projections and compare per-invoice IDs/versions/status/amounts, counts/checksums, gaps, DLQs, latency, and region high-waters. Route effecting consumers to exactly one type/epoch and share effect IDs. Reconcile dead letters/uncertain effects before cutover. Multi-region failover fences stale publisher/consumer ownership and preserves application IDs despite changed offsets.

Cut at explicit source old/new high-water parity with new consumers caught up; keep dual publication and old reads for rollback. Pause on divergence, hot-key overload, schema/region lag, unknown consumer, or effect conflict. Rollback switches reads/consumer route while both paths remain covered. Retire v1/old channel only after no producers, all registered/observed/dormant/replay consumers migrated, retries/DLQ/backlog drained/dispositioned, archive strategy/upcaster proven, rollback window passed, and contracts/schemas retained as long as old data references them.

### Answer 5

Create a high-risk replay request with immutable archive/source ranges per region/channel/partition, inclusive rules/high-waters, event counts/digests, requester/approvers, purpose limited to search/analytics, expiry, consumer artifacts, destination generations, cost/rate budget, stop/rollback, and final disposition. Replay service has read access to approved archive and write access only to isolated search/analytics ingress/state—no payment, email, shipment, live command, or business-event credentials/routes.

Preserve original event IDs/types/occurred times/keys/order versions/writer schema fingerprints/bytes; add signed run ID as attempt metadata. Restore exact schemas and pure deterministic upcasters for every retained version. Apply current deletion/erasure, tenant, legal hold, and purpose rules before target write; do not resurrect forbidden data. Unknown/corrupt/incompatible messages go to run-scoped quarantine with evidence and no effect.

Load verified snapshots when applicable, then events strictly after vector high-water. Use dedicated consumer scopes and isolated versioned indexes/tables. Limit global/per-tenant/key concurrency, bytes, and database/index load; give live traffic priority. Canary representative ages/schemas/tenants/regions, then ramp. Checkpoint source coordinates atomically with durable target state/run generation; resume idempotently and account for cancellation/in-flight.

Observe source/read/upcast/process rates, lag/ETA, schema/unknown/gap/duplicate/quarantine, resource/cost, live SLOs, and per-target counts/checksums. Reconcile authoritative order facts to per-order last version, deletions, cardinality, aggregates, representative queries, search/analytics checksums, and aligned high-water. Explicitly verify payment/email/shipment effect-ledger counts unchanged.

Shadow old/new reads and performance. Promote by atomic read alias/routing only after parity and security/privacy validation; keep old targets for rollback through observation window while catching live delta. Audit ranges/digests, artifacts/config/upcasters, approvals/actions, checkpoints, exceptions/dispositions, validation, promotion/rollback, and final deletion/retention. A failed invariant or live-impact signal pauses the run rather than “finishing” at any cost.
