---
module_id: DARCH-036
program: Data Architecture Engineering
level: 1
module_number: 36
title: Change Data Capture Architecture
status: complete
last_verified: 2026-09-03
---

# Change Data Capture Architecture

## One-Page Review

### Governing question

When should an organization derive integration feeds from committed source changes, and how can it preserve transaction order, snapshot continuity, schema meaning, delete and correction behavior, protection, recovery, and ownership without mistaking physical row mutations for durable domain facts?

### Essential definitions

- **Change data capture (CDC)** observes committed inserts, updates, deletes, or log records and publishes a representation of those changes for downstream use.
- **Log-based CDC** reads a database transaction log; **trigger-based CDC** records changes through database triggers; **query-based CDC** discovers changes by polling a marker or comparing state.
- A **change record** represents a physical or logical source mutation, including operation, object, key, before or after values, position, transaction context, schema, and time where available.
- A **log position** is a source-specific ordering or resume token. It is not inherently a portable event identifier or business time.
- An **initial snapshot** captures baseline source state before or alongside incremental changes.
- A **snapshot-change handoff** establishes a position relationship so changes committed around snapshot creation are neither silently lost nor irreconcilably duplicated.
- A **replication slot, checkpoint, or offset** records consumer progress and can cause retained source logs to grow when capture stalls.
- A **tombstone** or delete record communicates removal under a declared key and semantics; absence of a row is not always equivalent to a business deletion.
- **Schema history** preserves enough data-definition context to interpret old change records and transitions.
- A **transaction boundary** groups source changes that committed atomically; downstream systems may or may not preserve that atomic visibility.
- A **derived integration event** translates low-level changes into a governed cross-domain fact under a named semantic owner.
- **CDC lag** measures distance between committed source progress and captured or consumed progress, expressed in time, log positions, bytes, or transactions under declared conventions.

### Central model, mechanism, or theorem

Represent a CDC product as:

`C = (source, capture, snapshot, position, transaction, schema, change, delivery, transformation, service, protection, observability, ownership, recovery, lifecycle)`

CDC can externalize committed changes with less source-query load and lower latency than repeated full extracts. Its native truth is usually “this source representation changed,” not “this business occurrence happened.” A responsible design preserves source position and transaction context, connects the baseline snapshot to incrementals, makes schema and delete semantics explicit, and assigns ownership for any derived business meaning.

### Critical invariants

- Capture includes only committed changes under a declared source boundary, and documents how rollbacks, savepoints, long transactions, and distributed commits appear.
- Every change has a stable source, object or product, key, operation, schema context, position, transaction context, and observable capture state.
- Initial state and incremental changes share a provable handoff position or an explicit reconciliation procedure.
- Ordering claims are scoped to source log, transaction, table, key, partition, or delivery channel; no broader order is inferred.
- Deletes, soft deletes, key changes, truncation, compaction, and retention have explicit downstream semantics.
- Schema evolution preserves interpretable history and coordinates capture tooling, serializers, transformations, consumers, snapshots, and recovery.
- Checkpoints advance only at a boundary consistent with downstream effects, duplication policy, replay, and recovery.
- Capture lag, source-log retention, queue growth, backpressure, retries, poison records, and replay are bounded so consumers cannot endanger the source.
- Credentials, logs, before images, deleted values, schema history, snapshots, dead letters, and derived stores obey purpose, minimization, security, privacy, residency, retention, and deletion obligations.
- CDC migration and retirement close connectors, slots, triggers, accounts, checkpoints, topics, snapshots, schemas, copies, alerts, and consumer obligations after verified handoff.

### Common failures

Common failures are calling every row mutation a domain event; reading uncommitted or incomplete transactions; starting incrementals after a snapshot with an unmeasured gap; assuming a connector snapshot is transactionally consistent; treating log position as global business order; partitioning away source transaction order without disclosure; dropping before images needed for key change; treating missing rows as deletion; failing on schema change after the source log can no longer be replayed; allowing stalled replication slots to exhaust source storage; advancing offsets before durable consumer effects; replaying into non-idempotent sinks; copying protected columns because they exist in the log; and deleting a connector while slots, triggers, credentials, topics, and downstream copies remain.

### Compact example

A Customer database publishes log-based changes for an analytical current-state view. A consistent snapshot records source position `p0`; the connector buffers changes after `p0`, loads the snapshot, then applies incrementals in position order. Stable customer keys and schema history interpret updates and deletes. The consumer commits state and checkpoint atomically, tolerates duplicate delivery, and exposes lag. A domain-owned transformation separately emits `CustomerStatusChanged`; the raw CDC feed does not claim that semantic fact.

### Connections

[DARCH-018](018-temporal-and-historical-modeling.md) supplies time and history, [DARCH-019](019-model-versioning.md) governs model change, and [DARCH-035](035-event-driven-data-integration.md) distinguishes domain events from transport records. This module prepares [DARCH-039](../ROADMAP.md) on replication and synchronization and [DARCH-040](../ROADMAP.md) on selecting integration styles.

## Governing Question

Committed database logs already contain ordered evidence that physical state changed. CDC makes that evidence available without repeatedly scanning source tables or modifying every application write path. This efficiency can seduce architects into treating implementation records as stable cross-domain contracts.

The governing question is not “Can the connector capture this table?” It is “Which consumers legitimately need source changes, what semantics and time can those changes support, and can snapshot continuity, schema history, delivery, recovery, protection, and lifecycle be governed without harming the operational source?”

## Why This Matters

Polling full tables wastes source capacity, increases latency, and struggles to identify deletes. Application-published events may require changes to systems that cannot be modified. Log-based CDC can expose committed mutations with low application intrusion, making it valuable for replication, caches, search indexes, analytical ingestion, migrations, and event derivation.

PostgreSQL's [Logical Decoding Concepts](https://www.postgresql.org/docs/current/logicaldecoding-explanation.html) explains extracting persistent changes from the write-ahead log and the roles of replication slots and exported snapshots. MySQL's [Binary Log](https://dev.mysql.com/doc/refman/8.4/en/binary-log.html) documentation describes a log used for replication and recovery. These are database-specific mechanisms, so guarantees must be stated for the selected source and configuration.

The [Debezium documentation](https://debezium.io/documentation/reference/stable/) describes connectors, snapshots, change-event records, schemas, and operational behavior across supported sources. [CloudEvents 1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md) and [AsyncAPI 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0) can help standardize integration envelopes and interfaces after architects decide what the change means.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) provides concepts for derivation. Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) addresses overload propagation, and NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames secure-system trustworthiness across lifecycles. CDC needs all three perspectives because it creates powerful copies from a sensitive source dependency.

## Prerequisites and Retrieval

You should understand database transactions, write-ahead and binary logs, snapshots, isolation, primary keys, schemas, events, queues, ordering, idempotency, replication, distributed failure, data products, lineage, provenance, service objectives, privacy, and lifecycle.

Retrieve insert, update, delete, before image, after image, transaction ID, commit, log position, LSN, binlog coordinate, offset, replication slot, checkpoint, snapshot, handoff, watermark, schema history, DDL, primary key, tombstone, truncation, compaction, lag, backpressure, replay, outbox, reconciliation, and retirement.

As a retrieval test, inspect “CDC sends Customer changes in real time.” Ask which database and tables, committed boundary, key, operation, before and after values, transaction and order, snapshot position, schema version, delete behavior, lag objective, retained log, authorization, consumer purpose, derived meaning, correction, and recovery apply. The phrase does not yet define a product.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish log-based, trigger-based, query-based, timestamp-based, and application-outbox capture mechanisms;
2. separate physical change records from domain events, source-aligned products, audit evidence, and replicated state;
3. model source, capture, snapshot, position, transaction, schema, change, delivery, service, protection, recovery, ownership, and lifecycle;
4. design a gap-free or explicitly reconciled handoff between initial snapshots and incremental changes;
5. state ordering and transaction boundaries precisely across capture, partitioning, delivery, and consumer application;
6. handle inserts, partial and full updates, deletes, key changes, truncation, compaction, and source correction;
7. evolve tables and schemas while preserving interpretable change history, consumer compatibility, and rollback;
8. engineer checkpoints, idempotent sinks, lag, retained logs, capacity, backpressure, retries, replay, and disaster recovery;
9. protect broad log access, before images, deleted values, schema history, snapshots, metadata, and derived copies;
10. choose CDC, outbox events, APIs, batch snapshots, replication, or direct application publication from semantic and operational evidence.

## Core Exposition

**Define the required downstream outcome.** A cache needs current state, an audit process needs historical evidence, analytics needs changes and backfills, and a domain consumer needs business facts. These are different products even if one log supplies them.

Record consumer purpose, assertions, latency, completeness, history, ordering, volume, correction, protection, and lifetime. Choose capture only after the requirement is visible.

**Understand log-based capture.** Databases record changes for durability, recovery, and replication. A logical decoding or binary-log reader converts source-specific records into consumable change representations.

The log was designed first for database invariants. Its retention, formats, permissions, transaction markers, and schema information reflect that purpose. A connector must translate these mechanisms without overstating them.

**Understand trigger-based capture.** Triggers write change rows or invoke capture logic within source transactions. They can collect tailored before and after images and business context near the write.

Triggers add write-path cost, deployment coupling, permissions, recursion hazards, and failure modes. Govern their code and schema as production source logic. Test bulk operations and disabled-trigger scenarios.

**Understand query-based capture.** Polling a modification timestamp, sequence, or status is broadly available but can miss deletes, equal timestamps, clock anomalies, uncommitted visibility, and changes outside the marker.

Use stable tie-breakers and overlap windows with deduplication where appropriate. Periodic full reconciliation may be necessary. A timestamp column is not a log position unless the application enforces that invariant.

**Consider the transactional outbox.** The application writes a business event or publication intent in the same transaction as domain state. A relay publishes the outbox asynchronously.

This provides clearer semantics than deriving them from arbitrary table mutations, but relay delivery can duplicate and schema evolution remains. It requires application participation and disciplined outbox lifecycle.

**Separate mutation from meaning.** An update can reflect a business event, a correction, normalization, backfill, compaction, operational repair, or no semantic change. Several rows may implement one invariant.

Raw CDC should be labeled as physical or source-log evidence. Translate it into a domain event only when an accountable owner defines occurrence, grouping, time, source authority, and correction.

**Define source scope.** Name database instance or cluster, tables, columns, schemas, transaction types, included operations, and effective interval. Record whether generated, temporary, partitioned, or system tables appear.

Avoid wildcard capture that silently expands when new protected columns or tables are added. Use allowlists and change review. Capture scope is an access and capacity decision.

**Require stable keys.** Consumers need a durable key to apply inserts, updates, and deletes. Source primary keys may be composite, mutable, surrogate, reused, or absent.

Define key semantics and changes. A primary-key update may appear as delete plus insert or before-and-after update depending on source and connector. Keyless tables can require full before images or append-only treatment.

**Define before and after images.** Full after state simplifies current projections but increases payload and exposure. Changed-columns-only records reduce volume but require prior state and schema-aware merging.

Before images support key changes, delete reconstruction, audit, and comparisons, while duplicating sensitive prior values. Select representation from use, source capability, protection, and correction needs.

**Respect transaction commit.** Consumers generally need committed changes, not intermediate writes later rolled back. State how the connector buffers or identifies transaction completion and handles long transactions.

A large transaction can delay visibility or overwhelm buffers. Rollbacks, savepoints, prepared transactions, and distributed commits vary by database. Test actual source behavior.

**Preserve transaction context.** Attach source transaction identifier, commit position, order within transaction, and commit time where trustworthy and available. This lets consumers group changes that formed one atomic source update.

Downstream brokers may split one transaction across partitions and consumers. If atomic downstream visibility matters, provide a transaction envelope, staging and commit marker, or reconciliation protocol.

**State ordering boundaries.** A source log has an order under its engine's rules. Conversion, parallel tasks, partitioning, retries, and multiple source shards can weaken or split that order.

Promise only what the end-to-end path preserves: perhaps per source partition, table, or key. A log position from one primary is not a global order across independent databases.

**Model log position precisely.** Source positions support resume and comparison within a declared log lineage. Failover, restore, log rotation, connector upgrade, or source recreation can change their interpretation.

Do not use positions as business identifiers. Pair them with source identity and epoch. Preserve checkpoints, but validate that a restored checkpoint belongs to the current source history.

**Design the initial snapshot.** Incremental changes alone cannot reconstruct rows that existed before capture began. A snapshot establishes baseline state for a new consumer.

State isolation, start and end time, included objects, filters, key ranges, schema, source position, chunking, retries, duplicates, deletes during scan, and validation. “Initial load complete” needs evidence.

**Create a snapshot-change handoff.** One approach records a log position associated with a consistent snapshot, buffers later changes, loads snapshot rows, then applies changes after the position.

Source mechanisms differ. If an atomic relationship is unavailable, overlap snapshot and capture, deduplicate, and reconcile counts, keys, checksums, and state. Never assume starting a connector after export introduces no gap.

**Handle chunked snapshots.** Large tables may require chunks to limit locks and resource use. Rows can change while chunks are read, producing mixed-time state.

Use a database-consistent snapshot where feasible or record chunk boundaries and overlay incremental changes correctly. Monitor source load, transaction age, log retention, and completion.

**Represent inserts.** An insert record declares key, after image, schema, transaction, position, and time. Upserts and duplicate keys need clear downstream behavior.

Consumers should not infer that insert means the entity first existed globally; it means the captured source created a row in this history. Imports and restores may insert old business entities.

**Represent updates.** Define whether after image is full or partial, whether unchanged fields are present, how null differs from absent, and whether before image exists.

No-op physical updates can still produce log records. Consumers deriving business events must compare meaning under the correct schema and time rather than treating every update as a change of every field.

**Represent deletes.** A hard delete may provide only a key, a before image, or a tombstone. A soft delete is usually an update to a status or timestamp. Truncation may have separate semantics.

Define whether deletion means business erasure, archival move, correction, deduplication, or physical cleanup. Downstream state removal, evidence preservation, and legal duties depend on that meaning.

**Handle key changes.** If a key changes, consumers must remove old state and create or update new state atomically enough for their use. Preserve old and new keys and transaction context.

Avoid changing durable business identifiers casually. If source keys are unstable, translate to a stable product identity before broad publication.

**Handle schema evolution.** Add, remove, rename, reorder, split, combine, and type changes affect decoding, serializers, transforms, consumers, snapshots, and replay. DDL and data changes can share one deployment.

Maintain schema history tied to source positions or effective intervals. Test connector support and rollback. A consumer replaying old records needs the schema that produced them, not only today's table definition.

**Separate syntax and semantics.** Adding a nullable column may be structurally compatible but can expose protected data or change source meaning. Renaming may preserve meaning while breaking physical consumers.

Publish data-product changes separately from raw source evolution when downstream users need stable semantics. Use transformation versions and provenance to bridge changes.

**Define change envelopes.** Include source identity, object, operation, key, before and after data as selected, transaction, log position, schema reference, capture time, and connector version.

If translating to CloudEvents, map context deliberately. Do not overload event `time` with an ingestion timestamp when consumers expect business occurrence time. Name extensions and limitations.

**Design delivery.** Captured records commonly flow through queues or logs. Specify persistence, acknowledgement, partitioning, ordering, duplication, retention, expiry, replay, dead letters, and consumer bootstrap.

Connector exactly-once claims are bounded. Source read, broker write, consumer effect, and external side effects may span separate transactions. State each boundary.

**Checkpoint safely.** A checkpoint records capture or consumer progress. Advancing before durable downstream publication or application can lose records after failure; advancing after can duplicate.

Use atomic transactions when supported or accept at-least-once behavior with idempotent sinks. Persist source identity, position, epoch, schema context, and ownership with the checkpoint.

**Make sinks idempotent.** Apply change records by stable key and source position or event identity. Reject stale positions when ordering is reliable, and handle retries without duplicate side effects.

An upsert alone is not always idempotent: increments, notifications, and audit append can repeat. Define business effect, transaction boundary, deduplication, and reconciliation.

**Measure lag in several ways.** Time lag is understandable but depends on clocks and long transactions. Position or byte lag reflects source-log distance but not consumer processing cost. Transaction and record counts provide other views.

Measure capture, broker, and consumer lag separately. A connector can be current while a materialized view is stale. Define alert thresholds from business consequence and retained-log margin.

**Protect source-log retention.** Replication slots or equivalent checkpoints may force a source to retain logs until consumers advance. A stalled connector can exhaust disk and threaten the primary.

Monitor retained bytes, age, disk headroom, slot state, and consumer progress. Define maximum lag, pause or drop decisions, snapshot rebuild, escalation, and accountable authority before an incident.

**Apply backpressure without harming the source.** If downstream slows, buffer within declared limits, reduce capture work where safe, shed noncritical derived work, or rebuild from a later snapshot under contract.

Do not blindly stop acknowledgement if it will exhaust source storage. The recovery policy must balance completeness, source safety, service, and consumer consequence.

**Plan capacity.** Include change rate, transaction size, before and after images, schemas, fan-out, serialization, transformations, broker replication, retention, snapshots, replays, network, and sink writes.

Use burst and bulk-update scenarios, not daily averages. Schema migrations and backfills can create extraordinary logs. Reserve recovery headroom and coordinate with database operations.

**Bound retries and poison changes.** Connector, broker, transform, and sink retries can multiply work. Use backoff, jitter, budgets, circuit breakers, and deterministic invalid-record handling.

Quarantine with source position, schema, reason, owner, protected payload reference, retention, correction, replay, and closure. Skipping a record must be an explicit consistency decision.

**Plan replay and resnapshot.** Replaying from retained logs preserves change history within the available window. Resnapshotting reconstructs current state but may lose intermediate transitions and audit evidence.

Choose based on consumer product semantics. Validate schema compatibility and idempotency, isolate recovery traffic, checkpoint progress, and compare final state or history.

**Handle source failover and restore.** A promoted replica or restored backup may create a new log lineage. Old positions can become invalid or refer to different history.

Use source epochs, failover-aware connectors, reconciliation, and documented recovery. Detect rewind, gaps, and duplicates. Do not resume from a token merely because its syntax parses.

**Protect broad database access.** CDC accounts often require log or replication privileges and can observe every change in configured scope. Apply least privilege, network segmentation, workload identity, secret rotation, audit, and incident response.

Separate connector administration from consumption. Test whether a compromised connector can modify the source, expand capture, read unrelated schemas, or exhaust logs.

**Minimize captured data.** Logs may contain protected columns, prior values, deleted content, and transaction metadata. Select tables and columns by consumer purpose where source and connector support it.

Filter as early as safely possible, while preserving keys and correction. Ensure filters do not silently break transaction or delete interpretation. Review new columns before automatic inclusion.

**Govern every copy.** Snapshots, topics, schema history, connector buffers, dead letters, logs, traces, backups, test fixtures, and sink tables all carry retention, residency, access, records, deletion, provider, and incident duties.

Deleting the source row does not erase the log or downstream copies. Propagate erasure or document lawful retention and collect evidence from registered consumers.

**Observe end to end.** Track source position, captured position, published position, consumer checkpoint, lag, retained bytes, transaction duration, records, bytes, schema versions, retries, duplicates, gaps, dead letters, snapshot progress, and sink state.

Protect metadata and payload samples. Monitor missing telemetry. Link technical positions to product freshness and consumer outcomes where feasible.

**Maintain lineage and provenance.** Relate sink rows or derived events to source object, key, transaction, position, schema, connector, transform version, and capture execution.

Provenance supports reconstruction and correction but does not turn a row mutation into a domain fact. Record semantic derivation ownership separately.

**Design correction.** Source corrections produce new changes; they do not automatically repair derived reports, models, exports, or decisions. Identify affected keys, positions, intervals, schemas, and consumers.

Consumers replay, restate, or preserve original evidence according to contract. If an erroneous change was deleted from a topic, retain sufficient protected audit evidence for accountable correction where required.

**Assign ownership.** Database teams own source-log health and supported access. Platform teams own connector and delivery capability. Domains own source semantics and derived integration facts. Consumers own sink fitness and effects.

Define incident command, schema change notification, slot-drop authority, resnapshot decisions, correction, and retirement. Shared tooling does not erase these boundaries.

**Choose CDC for physical fidelity.** It is strong for replication, materialized views, search indexes, cache updates, migrations, and analytical ingestion when source changes are the needed input.

It is weak as a raw public contract when physical schemas change frequently or consumers require business intent. Add a product transformation or application event boundary.

**Compare application events.** Application publication can carry business context and occur close to invariants, but dual writes can create gaps unless an outbox or equivalent mechanism is used.

CDC can relay the outbox, combining transaction atomicity with semantic intent. The outbox itself needs schema, retention, cleanup, identity, and operations.

**Compare batch snapshots.** Snapshots give a coherent population and simplify recovery for consumers that need periodic state. They can be expensive and lose intermediate changes.

CDC lowers latency and transfer volume but increases ordered state and replay complexity. A snapshot-plus-changes product often supports both bootstrap and continuous updates.

**Plan migration.** Inventory source objects, keys, transactions, schemas, workloads, consumers, purposes, protections, current extracts, and failure history. Establish a source epoch, initial snapshot, handoff, and observable checkpoints.

Run old and new paths in parallel within bounded time. Compare counts, keys, values, nulls, deletes, transactions, order, time, schema, lag, protection, and consumer outcomes. Define rollback and resnapshot.

**Retire completely.** Stop connectors and polling; drop slots and triggers safely; revoke accounts and network paths; remove topics, checkpoints, schemas, snapshots, buffers, dead letters, alerts, provider resources, and obsolete sink logic.

Update catalogs and lineage. Preserve required records, provenance, holds, and correction. Verify source-log release and consumer closure. Disabled capture with a retained slot is an operational hazard, not retirement.

**Measure value.** Track source query reduction, capture completeness, lag, retained-log margin, snapshot duration, gaps, duplicates, schema failures, recovery time, consumer freshness, incidents, protection exceptions, costs, and closure.

CDC volume alone is not value. Success means downstream products receive the right source changes with intelligible semantics, bounded source risk, recoverable state, effective protection, and sustainable ownership.

## Definitions and Notation

Represent CDC architecture $C=(S,K,N,P,X,T,H,D,M,Q,Z,O,R,L)$, where $S$ is source scope, $K$ keys, $N$ capture mechanism, $P$ source position and epoch, $X$ snapshot and handoff, $T$ transaction semantics, $H$ schema history and change representation, $D$ delivery, $M$ transformations and products, $Q$ service and capacity, $Z$ protection, $O$ observability and ownership, $R$ recovery and correction, and $L$ lifecycle.

Let source commit position be $p_s$, captured position $p_c$, published position $p_b$, and consumer-applied position $p_a$ within one comparable source epoch. A healthy ordered path often expects $p_a\leq p_b\leq p_c\leq p_s$, but positions from different partitions or engines may not be numerically comparable.

For snapshot baseline $X$ associated with position $p_0$, a current-state reconstruction conceptually applies committed changes with positions after $p_0$ in the declared order. Correctness depends on snapshot consistency, complete capture, key and delete semantics, schema history, and consumer application—not the inequality alone.

Let lag margin be $M_r=R_{source}-L_{capture}$, where $R_{source}$ is safe retained-log capacity or time and $L_{capture}$ current lag in compatible units. Positive margin is necessary but not sufficient because bursts, disk consumption, long transactions, and recovery rate vary.

Define `JustifiedCDC(C,t)` as a review predicate requiring a valid physical-change need, committed source boundary, stable keys and positions, snapshot continuity, interpretable schemas, bounded source and delivery risk, effective protection, recoverable consumers, accountable meaning, and funded lifecycle at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every material CDC product.

**1. Purpose gate.** Define consumers, source changes, required meaning, latency, completeness, history, workload, protection, consequence, and alternatives.

**2. Source gate.** Name database, epoch, tables, columns, keys, operations, transaction behavior, logs, privileges, configurations, owners, and constraints.

**3. Snapshot gate.** Specify isolation, chunks, filters, schema, source position, buffering, handoff, validation, retries, resource impact, and completion evidence.

**4. Change gate.** Define inserts, updates, before and after images, null and absence, deletes, tombstones, key changes, truncation, compaction, and correction.

**5. Ordering gate.** Preserve transaction, position, partition, checkpoint, epoch, acknowledgement, duplication, idempotency, gap detection, and meaningful downstream atomicity.

**6. Schema gate.** Govern DDL, schema history, serialization, mappings, compatibility, versions, snapshots, replay, rollout, rollback, and consumer evidence.

**7. Capacity gate.** Model change and transaction distributions, snapshots, fan-out, logs, storage, lag, slots, retries, backpressure, replay, failover, and source safety.

**8. Protection gate.** Apply least privilege, purpose, minimization, before-image controls, metadata protection, residency, providers, retention, deletion, records, audit, and incidents.

**9. Evidence gate.** Observe positions, epochs, lag, retained logs, transactions, snapshot progress, records, bytes, schemas, duplicates, gaps, retries, dead letters, sink state, and outcomes.

**10. Lifecycle gate.** Discover, authorize, snapshot, capture, operate, correct, resnapshot, migrate, revoke, drop slots and triggers, remove copies, retire, and verify closure.

The executable example applies ordered changes once per source position to a current-state projection.

<!-- bijux-verify: {"id":"cdc-positioned-state-reduction","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"deliveries=5\napplied_positions=4\nsuppressed_duplicate_positions=1\nfinal_customer_ids=102\ncustomer_102_status=active\n","stderr":""}} -->
```python
changes = [
    (101, "insert", 101, "active"),
    (101, "insert", 101, "active"),
    (102, "update", 101, "inactive"),
    (103, "insert", 102, "active"),
    (104, "delete", 101, None),
]

state = {}
applied_positions = set()
for position, operation, customer_id, status in changes:
    if position in applied_positions:
        continue
    if operation == "delete":
        state.pop(customer_id, None)
    else:
        state[customer_id] = status
    applied_positions.add(position)

print(f"deliveries={len(changes)}")
print(f"applied_positions={len(applied_positions)}")
print(f"suppressed_duplicate_positions={len(changes) - len(applied_positions)}")
print(f"final_customer_ids={','.join(str(key) for key in sorted(state))}")
print(f"customer_102_status={state[102]}")
```

The example proves only that this ordered, single-epoch, in-memory reducer ignores one repeated position and produces one remaining row. It does not prove durable checkpointing, transaction atomicity, complete capture, stable key or position semantics, correct schema interpretation, concurrent safety, gap absence, business meaning, or recovery after restart. Those require source-specific mechanisms, durable state, failure tests, reconciliation, protection, and accountable review.

## Alternatives and Trade-Offs

**Log-based versus trigger-based CDC.** Log reading minimizes application changes and sees committed mutations, but uses source-specific privileges and formats. Triggers capture tailored context but add write-path logic and operational coupling.

**CDC versus application events.** CDC faithfully reports physical changes and can retrofit legacy systems. Application events express business intent but require publication design and application ownership.

**Raw CDC versus derived event product.** Raw records support replication and reconstruction. Derived events provide stable cross-domain meaning while adding transformation, ownership, versioning, and correction duties.

**CDC versus polling.** CDC reduces repeated scans and observes deletes; polling is widely available and simpler for low-rate, low-consequence needs but can miss or duplicate changes.

**Incremental log versus periodic snapshot.** Logs preserve transitions and reduce transfer. Snapshots provide coherent baseline and simple current-state recovery while losing intermediate history.

**Full versus partial images.** Full images simplify stateless sinks but increase bytes and exposure. Partial images are efficient but require prior state, schema-aware merging, and delete or key-change care.

**One global stream versus table or domain streams.** One stream can preserve source transactions but mixes access and workloads. Separate streams improve isolation and purpose controls while weakening cross-stream ordering.

**Retain logs versus resnapshot.** Long retention enables replay but consumes source and platform storage. Resnapshot releases history pressure but may lose intermediate changes and burden the source.

**Source checkpoint versus sink transaction.** Early checkpointing improves throughput but risks loss; later checkpointing duplicates. Atomic sink-and-checkpoint or idempotent application plus reconciliation provides safer boundaries.

**Managed connector versus self-operated capture.** Managed tooling reduces implementation effort but introduces provider access, supported-version limits, pricing, location, observability, upgrades, and exit obligations.

## Failure Modes and Misconceptions

1. **Every captured mutation is a domain event.** Physical changes may lack business intent or group boundaries.
2. **The source log is a public contract.** Its schema and positions belong to database mechanisms.
3. **A snapshot plus later capture has no gap.** The handoff position must be proven or reconciled.
4. **Committed order is globally meaningful.** Ordering usually belongs to one source lineage and can be weakened downstream.
5. **Log position is an event ID.** It needs source and epoch and does not express business identity.
6. **Primary keys never change.** Updates, restores, reuse, and physical redesign require explicit handling.
7. **Missing row means business deletion.** Archival moves, filtering, correction, and cleanup can look similar.
8. **After images are enough for every delete.** Keys, prior values, and downstream semantics may be required.
9. **Schema registries solve semantic evolution.** Structure does not preserve meaning or authority.
10. **Connector acknowledgement means sink success.** Publication and consumer effects are separate boundaries.
11. **An upsert makes every sink idempotent.** Increments, alerts, and append-only effects can repeat.
12. **Replication slots are passive metadata.** Stalled slots can retain logs until the primary exhausts storage.
13. **Stopping capture protects the source.** It may increase retained-log pressure depending on mechanism.
14. **Replay is always equivalent to resnapshot.** One preserves transitions; the other reconstructs state.
15. **Deleting source data removes captured copies.** Topics, before images, snapshots, and sinks persist.
16. **Low capture lag proves a fresh product.** Broker, transformation, and consumer lag remain.
17. **Deleting the connector retires CDC.** Slots, triggers, accounts, topics, checkpoints, copies, and duties remain.

## Worked Examples

### Example 1

A Customer row update changes an index-maintenance timestamp but no business field. Raw CDC records an update; a domain transformation compares governed assertions and emits no `CustomerChanged` event. **Conclusion:** physical fidelity and business occurrence semantics are different products.

### Example 2

A team exports a table at noon and starts log capture at 12:10. Deletes during the gap never appear in either output. It replaces this with a consistent snapshot tied to position `p0`, buffering changes after `p0`. **Conclusion:** temporal adjacency is not a snapshot-change handoff proof.

### Example 3

A primary-key change appears as delete of key 41 and insert of key 92 in one transaction. The consumer preserves transaction context and a stable domain ID, preventing temporary double identity. **Conclusion:** key mutation semantics require more than independent row operations.

### Example 4

A connector applies a change to its sink and crashes before checkpointing. Redelivery repeats the position. The sink commits state and highest applied position atomically, so the duplicate has no second effect. **Conclusion:** checkpoint placement and sink transaction define recovery behavior.

### Example 5

A replication slot stalls while a consumer is offline. Retained logs grow by 80 GB per hour with 300 GB headroom. Alerts, escalation, a maximum-lag decision, and a tested resnapshot plan protect the primary. **Conclusion:** capture completeness must be balanced against source survival through explicit policy.

### Example 6

A nullable field is added containing health information. Wildcard capture would expose it to every downstream consumer. Allowlists, schema-change review, purpose checks, and explicit product versions prevent automatic distribution. **Conclusion:** DDL is also a protection and contract change.

### Example 7

A log has four ordered source positions but the broker partitions by table. Two rows from one transaction become visible at different times. A consumer needing atomic balance transfer stages records until a transaction completion marker. **Conclusion:** source atomicity is not preserved automatically through partitioned delivery.

### Example 8

A connector resumes position 540 after database restore, but that position belongs to the pre-restore log lineage. Source epoch validation detects the mismatch and forces reconciliation plus a new snapshot. **Conclusion:** resume tokens require source identity and history, not syntax alone.

### Example 9

A two-year replay includes records encoded under three table schemas. Schema history and versioned transformations reconstruct them; today's schema alone misreads a renamed unit. **Conclusion:** replayability includes historical interpretation, not only retained bytes.

### Example 10

After migration, engineers stop a connector but leave its slot and account. The primary continues retaining logs. Retirement drops the slot safely, revokes identity, removes topics and snapshots, updates lineage, and verifies consumers. **Conclusion:** operational closure includes source-side capture resources.

## Cross-Program Connections

- **Database engineering:** transaction logs, recovery, snapshots, isolation, keys, DDL, replication slots, failover, and storage pressure anchor CDC.
- **Data engineering:** ingestion, streams, checkpoints, state, backfills, schemas, quality, lineage, and serving implement downstream products.
- **Distributed systems:** ordering, duplication, partial failure, idempotency, backpressure, epochs, replay, and reconciliation shape guarantees.
- **Event and service engineering:** outboxes, envelopes, AsyncAPI contracts, domain events, APIs, compatibility, and consumer tests define boundaries.
- **Platform engineering:** connectors, brokers, identity, schemas, observability, quotas, self-service, upgrades, and support sustain capture capability.
- **Cybersecurity and privacy:** log privilege, before images, protected metadata, purpose, residency, retention, deletion, providers, and incidents constrain copying.
- **Software architecture:** domain boundaries, anti-corruption layers, events, adapters, legacy seams, ownership, and coupling locate transformation.
- **Systems engineering:** interface assurance, configuration, capacity, fault analysis, recovery, trade studies, verification, and lifecycle govern the whole path.

## References

1. PostgreSQL Global Development Group, *Logical Decoding Concepts*, PostgreSQL Documentation. <https://www.postgresql.org/docs/current/logicaldecoding-explanation.html>
2. Oracle, *The Binary Log*, MySQL 8.4 Reference Manual. <https://dev.mysql.com/doc/refman/8.4/en/binary-log.html>
3. Debezium, *Debezium Documentation, Stable Reference*. <https://debezium.io/documentation/reference/stable/>
4. Cloud Native Computing Foundation, *CloudEvents Specification 1.0.2*, 2022. <https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md>
5. AsyncAPI Initiative, *AsyncAPI Specification 3.0.0*, 2023. <https://www.asyncapi.com/docs/reference/specification/v3.0.0>
6. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
7. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Addressing Cascading Failures*, Google, 2016. <https://sre.google/sre-book/addressing-cascading-failures/>
8. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Define a complete CDC product for a Customer table. Include source boundary, keys, operations, transaction and position, snapshot, schema, delivery, service, protection, ownership, and lifecycle.

### Exercise 2

Design and justify a snapshot-change handoff for a one-terabyte table that cannot tolerate a long lock. Include chunking, source position, buffering, reconciliation, and failure recovery.

### Exercise 3

Trace insert, duplicate delivery, update, key change, delete, and replay through a current-state sink. Define checkpoint and idempotency boundaries.

### Exercise 4

Compare log-based CDC, triggers, timestamp polling, transactional outbox events, and daily snapshots for a legacy order system. Recommend a mixed design.

### Exercise 5

Plan CDC recovery after a source restore invalidates positions while three consumers have different checkpoints and retained histories. Include source safety, evidence, correction, and communication.

## Answers to the Exercises

### Answer 1

Name the database instance and epoch, allowed schema and table, captured columns, insert/update/delete and truncation behavior, stable customer and physical keys, transaction identifiers, source positions, commit semantics, before and after images, and effective interval. Label records as physical source changes. If deriving Customer facts, create a separately owned transformation with definitions, time, provenance, and correction.

Define snapshot isolation, chunks, filters, schema, baseline position, buffering, handoff, validation, retries, and completion. Maintain schema history tied to positions. Delivery declares envelope, partitions, ordering, acknowledgement, duplication, retention, replay, dead letters, and bootstrap. Service covers capture and consumer lag, retained-log margin, completeness, recovery, correction, capacity, and support. Protection covers replication identity, purpose, allowlisted columns, before images, topics, snapshots, metadata, regions, retention, deletion, audit, and providers. Assign source, platform, domain, and consumer owners. Lifecycle includes schema change, resnapshot, slot decisions, migration, account revocation, topic and copy removal, evidence preservation, and verified closure.

### Answer 2

Use the database's consistent snapshot and exported position mechanism where available. Record source epoch, schema, snapshot identifier, position `p0`, included key range, and start time. Begin capturing or retaining changes after `p0`. Read stable key ranges in bounded chunks while monitoring transaction age, source I/O, log growth, and locks. Load each chunk idempotently and checkpoint chunk evidence. After baseline load, apply buffered committed changes after `p0` in valid order, including deletes and key changes.

If one consistent snapshot cannot span the load, record per-chunk positions and overlay captured changes, then reconcile source and sink keys, counts, checksums, sampled values, deletes, schemas, and high-risk populations. Failure recovery resumes verified chunks or rebuilds affected ranges; it never guesses a position. Bound buffer retention and define what happens if source-log margin becomes unsafe. Validate final consumer state and freshness before declaring handoff. The design trades one long lock for longer mixed-time processing plus explicit overlay and reconciliation.

### Answer 3

Represent each committed change with source epoch, position, transaction, operation, old and new key where relevant, schema, and images. Insert creates state if its position has not been applied. Redelivery of the same position produces no second effect. Update merges a full or partial image under schema rules. Key change removes the old key and writes the new key within the transaction boundary. Delete removes or marks state according to product semantics.

Commit the sink state change and highest safe applied position or deduplication record atomically. If transaction records span partitions, stage until a completion marker or use reconciliation. Replay within retained deduplication can reuse the boundary; an older full rebuild should target a fresh projection or replay epoch. Reject positions from another source epoch, stale out-of-order changes where order is guaranteed, and reused positions with different content. Test crash before effect, after effect before acknowledgement, concurrent delivery, missing record, schema mismatch, and restart. An upsert alone does not protect append-only side effects or notifications.

### Answer 4

Log-based CDC is appropriate for broad committed physical changes, low application intrusion, and migration or analytical ingestion, but requires source-specific privileges, log retention, schema history, and connector operations. Triggers can add tailored context but burden the write path and deployment. Timestamp polling is simple for low-rate tables yet needs overlap, stable tie-breaking, delete detection, and reconciliation. A transactional outbox is best for new domain events because the application writes business intent with state, though a relay and cleanup remain. Daily snapshots efficiently serve complete reporting populations but omit intermediate transitions.

Use an outbox relayed by CDC for new `OrderAccepted` and `OrderCancelled` facts. Use raw log-based CDC internally for current-state analytical ingestion and migration, transformed behind a source-aligned contract. Use daily versioned snapshots with manifest and checksum for consumers that need coherent bulk state. Retain polling only for a small unsupported auxiliary table with explicit limitations and reconciliation. Avoid triggers unless source capability prevents safer choices and required context justifies write-path cost.

### Answer 5

Stop automatic resume and identify the new source epoch, restore point, old log lineage, available archives, current database state, and each consumer's last applied position, schema, product semantics, and retained history. Protect the source by assessing slots, disk, log-generation rate, workload, and recovery headroom. Preserve old checkpoints and evidence; do not reinterpret their numbers under the new epoch.

If archived logs bridge the restore consistently, replay under validated lineage and deduplicate. Otherwise create a new consistent snapshot tied to a new position. Current-state consumers can rebuild or reconcile keys, values, deletes, and versions. Historical consumers may need archived old-log replay plus explicit gap or restatement records. Consumers with side effects require impact analysis and correction rather than blind reapplication. Compare source and sink counts, checksums, high-risk values, transactions, time, and outcomes. Communicate affected intervals, confidence, service degradation, and correction obligations. Resume only after source epoch, handoff, capacity, protection, rollback, and consumer acceptance are approved; retain incident and provenance evidence.
