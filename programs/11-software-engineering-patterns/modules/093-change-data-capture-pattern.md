---
module_id: SEPAT-093
program: Software Engineering: Patterns
level: 2
module_number: 93
title: Change Data Capture Pattern
status: complete
last_verified: 2026-08-29
---

# Change Data Capture Pattern

## One-Page Review

### Governing question

How can a system turn committed changes in an authoritative data store into a replayable change stream without missing history, inventing transaction guarantees, exhausting the source log, or confusing physical row mutations with business events?

### Essential definitions

- **Change Data Capture (CDC)** observes inserts, updates and deletes in a source and represents them for downstream processing.
- **log-based CDC** reads the database's ordered recovery/replication log rather than querying base tables repeatedly.
- A **change record** identifies the source, object, operation, source position, transaction context, key, schema and available before/after images.
- A **source position**—for example a log sequence number (LSN)—is the source-specific resume coordinate, not necessarily a globally comparable timestamp.
- A **snapshot** is a bounded image of existing rows; **streaming** follows changes after a chosen log boundary.
- The **snapshot–stream handoff** combines those paths without an unobserved interval. Duplicate delivery at the boundary is acceptable only when applying records is idempotent.
- A **checkpoint/offset** records how far a capture pipeline can safely resume after failure.
- A **replication slot** is PostgreSQL state that retains required WAL and tracks a consumer position; an abandoned or lagging slot can retain storage indefinitely.
- A **tombstone/delete record** communicates removal; dropping it can resurrect stale downstream state.
- A **business event** states domain meaning and intent. A row-change record states storage mutation; one does not imply the other.
- **reconciliation** independently compares source truth with a projection to detect omissions, corruption and semantic drift.

### Central model, mechanism, or theorem

Let a committed source log be (L=\langle r_1,r_2,\ldots\rangle), ordered by source positions (p(r_i)). A consumer resumes after durable checkpoint (c), emits records with (p>c), and advances (c) only after the configured downstream handoff is durable. A crash after handoff but before checkpoint creates a duplicate; a checkpoint before handoff creates loss. Therefore practical CDC normally promises at-least-once delivery plus idempotent application, not magical end-to-end exactly-once behavior.

For bootstrap, take a consistent source image at boundary (p_0), emit its rows, then apply log records after (p_0). Correctness requires a precise snapshot definition, retained log history covering the scan, gap-free handoff, schema history, and a duplicate-safe sink. Order is guaranteed only in the documented transaction/key/partition scope.

### Critical invariants

- Only committed facts become durable downstream changes; aborted transactions do not.
- A checkpoint never advances beyond the strongest durable handoff actually obtained.
- Every record has stable source identity, position, operation, key and schema interpretation.
- Snapshot plus stream covers the intended source interval without gaps; overlap is handled idempotently.
- Transaction boundaries and ordering scope are explicit and preserved where consumers depend on them.
- Inserts, updates, key changes and deletes have defined sink semantics.
- Schema history remains available for old records and compatible evolution is governed.
- Capture lag, source-log retention and slot/binlog health have limits, alerts and recovery procedures.
- Sensitive columns are minimized before broad distribution; capture credentials and topics follow least privilege.
- Reconciliation can detect a plausible but wrong projection independently of the streaming path.

### Common failures

Frequent failures include starting at “now” and silently omitting existing rows; a snapshot/stream gap; advancing offsets before delivery; assuming one global order; partitioning a transaction across consumers; replaying non-idempotent side effects; ignoring deletes; lacking a stable key; treating a primary-key update as an ordinary update; allowing an inactive slot to fill source storage; losing binlog/WAL before recovery; decoding old records with only the newest schema; publishing raw PII; exposing storage refactors as public events; using timestamps as offsets; mistaking connector “exactly once” for end-to-end effect uniqueness; and operating without reconciliation.

### Compact example

A projection snapshots accounts at source position 100. It then receives update `101:a1=15`, delete `102:a2`, a duplicate of 102 after a crash, and insert `103:a3=30`. The sink identifies changes by source and position, so the duplicate delete is harmless; it checkpoints 103 only after durable application. Final rows are `a1=15,a3=30`. This demonstrates bootstrap overlap and idempotent projection, not database or broker correctness.

### Connections

[Transactional Outbox](088-transactional-outbox.md) can place a governed business message in the same transaction as domain state and use CDC for transport. [Idempotent Consumer](089-idempotent-consumer.md) handles replay at the sink. [Data Transfer Object](092-data-transfer-object.md) clarifies why row envelopes are boundary representations rather than domain models. The successor [Event Sourcing](../ROADMAP.md) makes an event log the authoritative model; CDC usually derives a technical stream from another authoritative store.

## Governing Question

How should engineers select, specify and operate CDC so downstream copies are complete and repairable while the source remains safe and the emitted meaning remains honest?

CDC is not merely a connector configuration. It is a distributed protocol spanning a source database, its recovery log and retention rules, a capture reader, offsets, optional broker partitions, evolving schemas, sinks and operators. Correctness is a property of that whole path. A green connector process does not prove that existing history was captured, deletes were applied, old schemas remain decodable, or a projection still equals the intended source relation.

The pattern is valuable when independent systems need timely changes without making every writer perform dual writes. It can feed replicas, search indexes, caches, analytical ingestion, audit infrastructure and outbox relays. It is dangerous when raw physical changes are presented as stable domain facts, when source retention is unbounded, or when teams cannot state the recovery and reconciliation model.

## Why This Matters

Polling `updated_at > last_seen_time` seems simple, but timestamps can collide, clocks and commit order differ, transactions can update a row without changing the field, and deleted rows disappear before being observed. Trigger-maintained change tables improve explicitness but add write-path work and ownership. Application dual writes can commit the database and fail before publishing, or publish before the database rolls back. Log-based CDC exploits the database's existing durable commit sequence and can observe all participating writers without adding a second action to each request.

That benefit comes with operational coupling to internals. A capture stream reflects table layout, keys, transaction behavior, DDL and source-engine failover rules. A long-running PostgreSQL replication slot may retain WAL; an expired MySQL binary log or SQL Server capture retention window can eliminate a resume point. A full snapshot can pressure storage and locks. Large transactions create latency and memory spikes. A sink can be “caught up” to an offset yet still be semantically wrong because filters, mappings or delete rules were incorrect.

CDC therefore requires evidence at four layers: source-log completeness, transport delivery, deterministic interpretation, and projected-state reconciliation. It also demands a semantic decision. Internal replication may legitimately expose row changes. A public integration API normally needs a stable business contract, often written to an outbox and transported using CDC.

## Prerequisites and Retrieval

Learners should retrieve:

- ACID transactions, commit/rollback, write-ahead logging and crash recovery;
- primary keys, unique constraints, foreign keys, DDL and schema migration;
- ordered logs, offsets, partitions, retention and consumer groups;
- at-most-once, at-least-once and effect-once/idempotent processing;
- consistent snapshots and isolation levels;
- transactional outbox, message envelopes and idempotent consumers;
- backpressure, lag, service-level objectives and capacity limits;
- data classification, least privilege and deletion obligations;
- checksums, row counts, invariants and independent reconciliation.

Before continuing, trace the two crash windows in “emit a change, then save its offset.” Explain why reversing those actions changes duplication into loss but does not create exactly-once effects.

## Learning Objectives

After this module, learners can:

1. distinguish log-based CDC, trigger/change-table capture, timestamp polling and application publication;
2. specify source positions, transaction metadata, ordering scope and checkpoint durability;
3. design a gap-free, duplicate-safe snapshot–stream handoff;
4. model insert, update, primary-key change, delete and truncation semantics;
5. distinguish physical changes, domain events and outbox records;
6. govern schema evolution and retain decoder history;
7. bound capture lag and prevent CDC from exhausting source storage;
8. design idempotent sinks, replay and poison-record handling;
9. test failures at each durability boundary and reconcile projected state;
10. decide when CDC is justified and when polling, batch snapshots or direct events are simpler.

## Core Exposition

### Define the captured fact and authority

Begin with an authoritative source relation and a bounded consumer purpose. “Stream the database” is not a contract. Name databases, schemas/tables, operations, columns, keys, transaction metadata, initial-history policy, latency objective, retention, destinations and prohibited data. Identify which system remains authoritative and whether consumers may make business decisions from eventual projections.

A row update can result from a user command, migration, trigger, repair, scheduled job or cascade. Its before/after images reveal what storage changed, not why. One domain action may modify several tables; several domain facts can share one row; an update may not correspond to a business fact at all. Use raw CDC for infrastructure replication or private transformation. If consumers need `OrderApproved`, let the domain-owning transaction write that named fact to an outbox; CDC then transports an explicit record without interpreting arbitrary tables.

### Prefer commit logs when their contract is operable

Databases already record enough information for recovery and replication. PostgreSQL logical decoding extracts persistent table changes from WAL and replication slots retain position/resource state. MySQL CDC commonly follows the binary log. SQL Server CDC uses capture processes/tables and log sequence numbers. Products differ in snapshot, failover, DDL, before-image and retention behavior; “supports CDC” is not a portable semantic guarantee.

Log-based capture usually avoids table scans on every poll and observes changes from all writers. It needs privileges, engine-specific decoding, retained logs and upgrade/failover compatibility. Trigger capture is database-portable only superficially: triggers alter write cost and failure behavior and must cover every table/operation. Incremental polling is acceptable for low-value, low-rate, append-only data with a monotonic key and reconciliation, but ordinary timestamps do not reliably encode deletes or commit order. Periodic full snapshots can be safest for small datasets when freshness allows.

### Model records and positions explicitly

A useful technical envelope includes:

- source instance and database/schema/table identity;
- operation: create, update, delete, read/snapshot, and any supported truncate/message operation;
- stable record/event identifier derived from source position and record index;
- transaction identifier and sequence within transaction where available;
- key before and after, because keys can change;
- before and after images with documented availability;
- source schema/version and event-envelope version;
- source commit/log position and capture/processing timestamps;
- snapshot marker and headers needed for traceability/classification.

The source position is authoritative for resume. Wall-clock timestamps are diagnostic: they can repeat, skew, have insufficient precision and differ from commit order. A multi-record transaction may share an LSN-like boundary and require an additional sequence. Positions from different database instances or failover timelines may not be comparable. Never sort them as bare integers without source identity and engine rules.

### Checkpoint only durable handoff

Suppose capture reads (r), sends it, then stores (p(r)). Failure after send and before checkpoint causes replay. If it stores (p(r)) first, failure before send loses (r). The safe default is at-least-once: retain the old checkpoint until the downstream system acknowledges its defined durable handoff, then tolerate duplicate delivery.

The phrase “exactly once” must name boundaries. A connector and broker may coordinate offsets and records transactionally, while a sink database and an email service remain outside that transaction. Uniqueness can be enforced at a sink by atomically recording a stable change identifier with the projection mutation. Non-idempotent external effects require their own ledger/outbox and business policy. Replaying a raw update must not resend money or email merely because those effects once followed the source transaction.

### Bootstrap without gaps

A new consumer needs both current rows and future changes. A robust bootstrap establishes boundary (p_0), holds or records sufficient log history, reads a consistent snapshot corresponding to the boundary, and continues streaming changes beyond it. Implementations may buffer concurrent changes, interleave chunks with streaming, or use database snapshot primitives. The invariant is coverage, not a particular algorithm.

If the stream begins after the scan, writes during the scan can be lost. If it begins before and overlaps, records may be duplicated or appear before their snapshot row; the sink needs deterministic precedence using source positions. Chunked/incremental snapshots reduce long transactions and restart cost, but require stable chunk keys, low/high watermarks and careful treatment of concurrent key changes. A snapshot without deletes cannot by itself remove records that disappeared since an older projection; replacement, mark-and-sweep or reconciliation semantics are required.

### Preserve transaction and ordering semantics

The source log has an engine-specific order. A transaction can atomically change many rows, yet a broker may partition records by row key and expose them independently. A consumer that requires transaction-level consistency needs transaction metadata, buffering or a different materialization boundary. Most downstream systems should require order per entity/key rather than a global total order because global serialization limits scale.

State the scope: within one source partition, one database transaction, one table, or one entity key. Repartitioning can reorder records. Multiple source databases have no shared commit order absent an explicit distributed protocol. Capture time is not occurrence time. Sinks should compare source coordinates within their valid namespace and reject/regard stale changes according to policy.

### Give every operation precise sink behavior

An insert usually upserts a keyed projection. An update applies an after image or a field delta; the sink must know whether absent means unchanged or unavailable. A delete removes or tombstones the key. A primary-key change may appear as delete-plus-insert and can break foreign references. Tables without stable keys force brittle full-row keys or append-only behavior. Truncate may be unsupported or represented without individual keys; ignoring it leaves stale state.

Before images depend on source configuration and log richness. Do not calculate a domain transition from a missing/partial before image. Compacted topics need tombstone policies that preserve deletion long enough for every projection. Privacy deletion is not solved by broadcasting a delete: immutable logs, backups, caches and derived datasets require their own retention/legal design.

### Evolve schemas as a temporal contract

CDC records persist while schemas evolve. The decoder may need historical table schema to interpret an old log segment. Sinks may replay old envelopes after new code deploys. Govern source DDL, connector envelope versions and consumer schema compatibility separately.

Additive nullable columns are often easier but still affect snapshots, defaults and old consumers. Renames can look like remove-plus-add and lose semantic continuity. Type narrowing, precision/timezone changes, key changes and reinterpretation are dangerous. Backfill migrations can emit enormous technical updates unrelated to new business activity. Deploy expand/migrate/contract sequences, retain schema history, test old-record/new-reader and new-record/old-reader combinations, and isolate bulk repairs from customer-event metrics.

### Operate source safety and backpressure

CDC couples consumer health to source retention. PostgreSQL documents that replication slots can retain WAL and other resources; operators must monitor retained bytes and slot activity, not only connector uptime. Every engine needs thresholds for lag in time and bytes, available disk, oldest recoverable position and retention headroom. Establish what happens at limits: throttle producers, scale sinks, pause optional consumers, advance/drop a slot and resnapshot, or fail over through a tested procedure.

Backpressure should stop at a bounded buffer, not accumulate invisibly until the source fails. Large transactions and poison records need quarantine/retry policy without skipping unknown data silently. Offset backups alone may be insufficient after source failover or log expiration. Recovery rehearsals must include restoring connector configuration, schema history, credentials, position lineage and sink deduplication state.

### Secure and reconcile the pipeline

The database log may contain columns never intended for analytics or broad messaging. Use least-privilege capture accounts, allow-list tables/columns, encrypt paths, separate classifications, protect schema/offset stores and redact observability. Filtering at sinks after raw publication multiplies exposure. Record lineage and deletion/retention responsibilities.

Reconciliation is a separate evidence path. Compare partitioned counts, keyed hashes, sums under known semantics, missing/extra keys and domain invariants at a stated source boundary. Investigate mismatches; do not overwrite blindly when a projection intentionally transforms data. Periodic rebuilds prove replayability only if compared before cutover. Monitor lag, throughput and errors for timeliness; reconcile for correctness.

### A deterministic handoff model

The executable model applies one consistent snapshot and an overlapping at-least-once delivery sequence using source positions as idempotency keys.

<!-- bijux-verify: {"id":"sepat-093-snapshot-stream-handoff","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"snapshot-position=100\ndeliveries=101:update:a1,102:delete:a2,102:delete:a2,103:insert:a3\napplied=101,102,duplicate-102,103\nrows=a1:15,a3:30\ncheckpoint=103\n","stderr":""}} -->
```python
rows = {"a1": 10, "a2": 20}
snapshot_position = 100
deliveries = [
    (101, "update", "a1", 15),
    (102, "delete", "a2", None),
    (102, "delete", "a2", None),
    (103, "insert", "a3", 30),
]
seen = set()
trace = []
checkpoint = snapshot_position

for position, operation, key, value in deliveries:
    if position in seen:
        trace.append("duplicate-" + str(position))
        continue
    if operation == "delete":
        if key in rows:
            del rows[key]
    else:
        rows[key] = value
    seen.add(position)
    checkpoint = position
    trace.append(str(position))

delivery_text = ",".join(
    str(position) + ":" + operation + ":" + key
    for position, operation, key, _ in deliveries
)
row_text = ",".join(key + ":" + str(rows[key]) for key in sorted(rows))
print("snapshot-position=" + str(snapshot_position))
print("deliveries=" + delivery_text)
print("applied=" + ",".join(trace))
print("rows=" + row_text)
print("checkpoint=" + str(checkpoint))
```

The run proves only this pure transition function and expected output. It does not implement a consistent database snapshot, log decoder, transaction grouping, durable checkpoint, broker, concurrency, schema evolution, authorization, retention management or reconciliation.

## Definitions and Notation

Let:

- (S) be the authoritative source state;
- (L=\langle r_1,r_2,\ldots\rangle) be committed logical change records;
- (p(r)) be a source-specific total coordinate within one declared log lineage;
- (tx(r)) and (seq(r)) identify transaction and within-transaction sequence where available;
- (p_0) be the snapshot boundary;
- (c) be the last durably handed-off checkpoint;
- (A(P,r)) be deterministic application of record (r) to projection (P);
- (id(r)) be a stable deduplication identity such as source lineage plus position and record index;
- (H_K(X)) be a reconciliation digest over a declared key range (K), canonicalized consistently.

**Safety** means the projection does not claim a source change unsupported by committed log history and policy. **Completeness through (q)** means every in-scope committed change at or before source position (q) is reflected. **Timeliness** is bounded delay from commit to usable projection. **Convergence** means replaying all required changes from a valid snapshot yields the same projection despite duplicate delivery.

For idempotent application, require

$$
A(A(P,r),r)=A(P,r).
$$

For gap-free bootstrap, the intended history is

$$
P_q=fold(A, snapshot(S,p_0),\{r\in L\mid p_0<p(r)\le q\}).
$$

This is a model, not a proof that an engine snapshot corresponds to one (p_0). That correspondence must be established from official engine/connector semantics and tested. A keyed reconciliation claim might be (H_K(S_q)=H_K(P_q)), but only after projecting source fields into exactly the sink's intended representation.

## Mechanisms, Invariants, or Proof Structure

1. **Scope the contract.** Enumerate source lineage, objects, columns, operations, keys, consumers, latency, retention and classification. Evidence: reviewed capture specification.
2. **Establish position semantics.** Document commit visibility, transaction sequencing, failover lineage and resume rules. Evidence: official engine/connector references plus failure tests.
3. **Bootstrap at a boundary.** Produce a consistent snapshot tied to retained log history. Evidence: concurrent-write tests proving no missing keys/versions.
4. **Hand off at least once.** Advance checkpoints only after the promised durable destination acknowledgement. Evidence: injected crashes before/after send and checkpoint.
5. **Apply idempotently.** Store stable change identity or compare source version atomically with projection mutation. Evidence: duplicates, reordered/stale records and restart tests.
6. **Preserve required atomicity/order.** Carry transaction metadata or explicitly accept row-level visibility. Evidence: multi-row transaction and repartition tests.
7. **Govern operation semantics.** Test insert, update, partial images, key change, delete, truncate and tables without keys. Evidence: per-operation vectors.
8. **Govern temporal schemas.** Retain schema history and test compatibility/replay across migrations. Evidence: expand/backfill/contract rehearsals.
9. **Bound source impact.** Alert on time/byte lag, retained-log volume, disk headroom and inactive consumers; rehearse resnapshot. Evidence: capacity thresholds and runbooks.
10. **Reconcile independently.** Compare keyed ranges at explicit source positions and investigate discrepancies. Evidence: mismatch drill and signed results.

The convergence argument assumes deterministic mapping and duplicate suppression. By induction over the ordered unique records after (p_0), base projection is the snapshot; applying the next required record yields the next source-derived state; duplicate application is neutral by idempotency. The argument fails with a missing record, wrong order where operations do not commute, nondeterministic mapping, unavailable historical schema or an external side effect. Therefore it is a conditional proof sketch, not universal proof of a deployed pipeline.

## Alternatives and Trade-Offs

**Application-published events** provide domain meaning and explicit payloads, but naïve dual writes are not atomic. Use an outbox when state and message must commit together.

**Transactional outbox plus CDC** combines domain-owned records with log-based reliable relay. It adds outbox lifecycle, ordering and cleanup work but avoids reverse-engineering arbitrary row changes.

**Trigger/change tables** make before/after records queryable and can work where logs are inaccessible. They add write latency, migration complexity and risk that triggers are disabled or inconsistent.

**Incremental polling** is operationally simple for append-only or low-rate tables with a monotonic cursor. It has freshness/query-cost trade-offs and needs tie-breaking, delete capture and overlap/reconciliation.

**Periodic full snapshots** are easy to reason about for small datasets and can replace rather than mutate a projection. They increase bandwidth/work and deliver coarse freshness.

**Database-native replication** is preferable for faithful same-engine replicas and recovery. CDC provides logical, selective, heterogeneous integration but usually weaker fidelity.

**Query federation/on-demand reads** avoid copied state but couple availability/latency and may overload the source. Use when consumers need current answers infrequently.

**Event sourcing** stores domain events as authority and rebuilds state from them. CDC derives technical observations from current-state persistence. Neither is a drop-in substitute for the other.

Choose using required meaning, freshness, completeness, source access, write cost, schema ownership, consumer count, repairability, retention and operational maturity. For a 5,000-row reference table refreshed nightly, a full replacement may dominate a continuously operated CDC fleet.

## Failure Modes and Misconceptions

- **“CDC means exactly once.”** It does not define sink or external-effect atomicity. State the transactional boundary and make sinks idempotent.
- **“An offset proves correctness.”** It proves progress under one reader's rules. Bad filters, mappings and skipped deletes can advance offsets while corrupting state.
- **“Timestamps are positions.”** Equal/skewed timestamps and commit reordering create omissions; use source coordinates or monotonic composite cursors.
- **“Start streaming now; backfill later.”** Without a boundary, concurrent updates create gaps or stale overwrites.
- **“Every row update is an event.”** It is a technical fact without domain cause, privacy minimization or stable semantic intent.
- **“One order exists.”** Parallel partitions and multiple databases provide scoped orders. Define the order consumers require.
- **“Latest schema decodes all history.”** Old logs/envelopes may require historical schema; renames and type changes are not automatically compatible.
- **“Updates contain full rows.”** Logs/connectors can emit changed columns or lack before images. Never infer unavailable values.
- **“Delete is just an empty update.”** Deletes need key/tombstone semantics and retention. Missing deletes accumulate phantom state.
- **“A connector can lag harmlessly.”** Retained logs can exhaust source storage or expire, forcing outage or resnapshot.
- **“Restarting is recovery.”** Lost source history, schema history or dedupe state requires an explicit rebootstrap plan.
- **“A snapshot is consistent by default.”** Long/chunked scans need engine-specific boundary semantics under concurrent writes.
- **“Replaying raw CDC is harmless.”** Projections may be idempotent; emails, payments and webhooks are not without separate effect ledgers.
- **“Filtering downstream protects secrets.”** Raw topics/logs already broaden exposure. Minimize near capture and govern all copies.
- **“Zero lag means equality.”** Only independent reconciliation tests content correctness.

## Worked Examples

### Example 1

**Situation.** A poller runs every minute using `updated_at > last_time`. Two rows commit with the same one-second timestamp; the poller sees one and saves that timestamp.

**Reasoning.** On the next query, strict `>` excludes the second row. Changing to `>=` prevents this omission but repeatedly returns boundary rows, requiring a stable tie-breaker and idempotency. Neither form observes physical deletes. A composite monotonic cursor may help only if every mutation updates it transactionally.

**Conclusion.** Ordinary timestamps are insufficient CDC offsets; use a source commit coordinate or a proven composite cursor plus delete and reconciliation mechanisms.

### Example 2

**Situation.** A team scans ten million customer rows, then starts the log reader at the scan's finish time.

**Reasoning.** Customer A changes midway through the scan after A's old row was read. That update occurred before streaming began and is absent from the snapshot, creating a permanent gap. Start-at-beginning may instead overlap; source positions and idempotent application can resolve overlap safely.

**Conclusion.** Snapshot and streaming must share a defensible log boundary; sequential “scan then subscribe” is not gap-free.

### Example 3

**Situation.** Capture sends record 450 to a broker, crashes before saving offset 450, then resumes from 449.

**Reasoning.** Record 450 is delivered twice. A projection transaction inserts change identity `(source-lineage,450,record-index)` with its update; the second insert conflicts and the second mutation is skipped. If the offset were saved before broker durability, the crash would lose 450.

**Conclusion.** Prefer replay with stable identity over premature checkpointing; at-least-once delivery requires atomic idempotency at each effect boundary.

### Example 4

**Situation.** One transaction debits account A and credits B, but records are partitioned by account and consumed separately.

**Reasoning.** Each partition preserves its own key order, not atomic visibility across both keys. A dashboard may temporarily show only the debit. If that violates requirements, the consumer must buffer using transaction metadata, materialize through a transactional sink, or use an aggregate-level/outbox event. Global ordering alone would not necessarily provide atomic sink application.

**Conclusion.** Preserve the smallest required consistency scope explicitly; row-level CDC does not automatically preserve multi-row transactional observation downstream.

### Example 5

**Situation.** `surname` is renamed to `family_name`, and a consumer reads replayed records produced before the migration using only the latest schema.

**Reasoning.** It can interpret the old field as missing and erase values. Treating rename as add/backfill/dual-read/contract preserves compatibility. Decoder schema history and envelope versioning are separate from table migration.

**Conclusion.** CDC is a temporal schema system: verify old-record/new-reader and migration-backfill behavior before contracting old fields.

### Example 6

**Situation.** Search removes products only when it receives delete records, but topic compaction/retention discards tombstones before the offline consumer recovers.

**Reasoning.** The consumer rebuild retains products that no longer exist. Longer tombstone retention, authoritative snapshot replacement or reconciliation mark-and-sweep can restore correctness. An update with null fields is not an unambiguous delete.

**Conclusion.** Delete observability must live at least as long as the recovery horizon or be reconstructible by snapshot/reconciliation.

### Example 7

**Situation.** A connector is paused for six days while its PostgreSQL replication slot remains active; WAL grows until the volume nears exhaustion.

**Reasoning.** The slot deliberately prevents removal of required WAL. Connector process health is irrelevant while its confirmed position stalls. Operators need byte/time-lag and disk-headroom alerts, a maximum retention policy, and a rehearsed decision to catch up, expand temporarily, or abandon the position and resnapshot.

**Conclusion.** CDC consumers consume source retention capacity; their lag is a source-availability risk, not merely stale analytics.

### Example 8

**Situation.** A billing consumer interprets any `orders.status` update to `paid` as authorization to charge a card.

**Reasoning.** A repair script, replay or manual correction can produce the same row image without a new charge intent. CDC also redelivers. Payment authorization must be an owned command/fact with stable effect identity, not inferred from an arbitrary physical update. An outbox record written by the domain can express `PaymentCaptureRequested` under an explicit policy.

**Conclusion.** Do not derive irreversible business effects directly from ambiguous row mutations.

### Example 9

**Situation.** A source table has no primary key and allows identical rows. The connector uses all columns as an identity-like key.

**Reasoning.** Updating one duplicate cannot identify which projection record to change; before images may be incomplete; key width leaks sensitive values. Adding a stable surrogate/business key is the durable fix. Otherwise the consumer must use append-only semantics or periodic full replacement with explicit limitations.

**Conclusion.** Stable identity is a prerequisite for reliable mutable projections; a connector cannot synthesize missing domain identity safely.

### Example 10

**Situation.** A regulated customer projection reports zero lag and matching total row count after a backfill.

**Reasoning.** A filter accidentally swapped two tenant identifiers; totals and offsets still look correct. Reconciliation by tenant/keyed digest and authorization invariants reveals cross-tenant misplacement. Because this claim affects regulated isolation, a named human data/security reviewer must inspect the mapping, sampled mismatches, classification and signed reconciliation evidence before production acceptance.

**Conclusion.** Progress metrics and aggregate counts are necessary but not sufficient; high-stakes CDC requires granular independent reconciliation and recorded human review.

## Cross-Program Connections

- **Database Engineering:** WAL/binlog, MVCC snapshots, logical decoding, replication slots, keys and DDL determine what capture can promise.
- **Distributed Systems Engineering:** checkpoints, replay, partial failure, partition order, idempotency and convergence explain end-to-end behavior.
- **Data Engineering:** CDC feeds incremental pipelines, but watermarks, late data, backfills, lineage and quality reconciliation remain required.
- **Security Engineering:** log access can expose every historical sensitive value; minimization, credentials, classification and erasure policy span all copies.
- **Software Architecture:** CDC creates an asynchronous boundary and ownership dependency; it should not leak a service's private schema as an accidental public API.
- **Testing and Quality Engineering:** fault injection at durability boundaries and oracle-independent reconciliation are stronger than happy-path connector tests.
- **Software Delivery and Reliability Engineering:** lag budgets, storage headroom, schema rollout, rollback/resnapshot and disaster drills make the pattern operable.
- **API and Service Engineering:** outbox records and governed integration-event schemas translate domain meaning before public consumption.

## References

- PostgreSQL Global Development Group, [Logical Decoding Concepts](https://www.postgresql.org/docs/current/logicaldecoding-explanation.html), PostgreSQL 18 current documentation, retrieved 2026-08-29. Defines logical decoding, replication slots, WAL retention and crash-related slot behavior.
- Debezium Project, [Debezium Connector for PostgreSQL](https://debezium.io/documentation/reference/stable/connectors/postgresql.html), stable documentation, retrieved 2026-08-29. Documents snapshots, streaming, logical decoding, offsets, transaction metadata, schema and operational properties.
- Microsoft, [What Is Change Data Capture (CDC)?](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-data-capture-sql-server?view=sql-server-ver17), SQL Server documentation, retrieved 2026-08-29. Describes capture instances, change tables, LSN query functions and cleanup.
- Apache Software Foundation, [Kafka Connect](https://kafka.apache.org/documentation/#connect), Apache Kafka documentation, retrieved 2026-08-29. Defines source/sink connector tasks, offset management and distributed operation.
- Chris Richardson, [Pattern: Transaction Log Tailing](https://microservices.io/patterns/data/transaction-log-tailing.html), Microservices.io, retrieved 2026-08-29. Relates transaction-log reading to reliable publication and transactional outbox implementations.
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017, chapters 5 and 11. Durable treatment of replication logs, stream processing, ordering, fault tolerance and derived data.
- Greg Young, [CQRS Documents](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf), 2010. Useful contrast among event logs, state representations and projections; CDC is not equivalent to an event-sourced domain history.
- Martin Fowler, [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html), 2005. Defines state reconstruction from a sequence of events, clarifying the authority distinction from derived database changes.

## Exercises

### Exercise 1

Define source position, checkpoint, snapshot boundary, tombstone and reconciliation. For each, state one thing it does not prove.

### Exercise 2

A snapshot begins at position 700 and scans keys A then B. A changes at 701 after A was scanned; B changes at 702 before B is scanned. The stream intentionally begins at 700. Trace a safe sink policy when snapshot rows and stream records can overlap.

### Exercise 3

Diagnose a pipeline that reports low broker lag while PostgreSQL retained WAL grows and the search index contains deleted records. Propose measurements and corrective controls.

### Exercise 4

Compare raw table CDC, transactional outbox plus CDC, trigger/change-table capture and hourly full replacement for publishing order information to search, analytics and customer notifications. Select per consumer and justify the boundaries.

### Exercise 5

Design CDC for an unfamiliar multi-tenant clinical scheduling database undergoing a primary-key migration. Include bootstrap, schema/key transition, privacy, ordering, recovery, reconciliation and evidence required before cutover.

## Answers to the Exercises

### Answer 1

A **source position** locates progress in one source log lineage; it does not prove downstream application or comparability across sources. A **checkpoint** records the strongest declared durable handoff; it does not prove transformation correctness. A **snapshot boundary** relates a consistent image to a log coordinate; it does not by itself prove the implementation retained and applied every later record. A **tombstone** communicates deletion for a key; it does not erase all historical copies. **Reconciliation** independently compares intended source-derived state and projection at a stated boundary; it does not prove timeliness between comparisons or validate an incorrectly specified mapping. A correct specification states each scope and limitation.

### Answer 2

Record a consistent snapshot boundary of 700 and retain all records after 700. Attach snapshot/boundary metadata or initialize each row at version 700. Apply stream records only if their source version exceeds the stored version, using stable change IDs for duplicates. If snapshot A=old arrives, then update 701 sets A=new. If B's scan reflects the 702 value and its snapshot row arrives before/after stream 702, the version rule ensures 702 wins or duplicate-equivalent application is neutral. The exact connector algorithm may buffer/interleave differently; tests must inject both orders and verify no key ends below its greatest committed position. If snapshot rows cannot carry a defensible version, stage the snapshot then replay retained stream before publication rather than racing writes directly into the visible sink.

### Answer 3

Low broker lag measures only broker-to-consumer distance. Growing WAL implies the source connector/slot confirmed position is stalled or a different abandoned slot exists. Deleted search rows imply tombstones were filtered, expired, mis-keyed or not applied. Measure each replication slot's active state, restart/confirmed positions, retained bytes/time and source disk headroom; connector source-to-broker lag; per-partition sink offsets; delete counts; dead letters; and keyed source/search reconciliation. Correct by identifying the owning slot, repairing/quarantining poison records, restoring delete handling and idempotently replaying while capacity permits. If required WAL is gone or retention risk exceeds limits, record the discontinuity, drop/advance only under approved recovery policy, and perform a boundary-controlled resnapshot plus reconciliation. Add ownership, retention thresholds, inactive-slot alarms and a tested resnapshot runbook.

### Answer 4

Search can consume private raw order/item CDC if it needs storage-level projection, schema coupling is accepted, deletes/transactions are handled and reconciliation rebuilds it. Analytics may ingest raw governed CDC into a restricted landing zone because broad transformation/history is its purpose, with column minimization and schema lineage. Customer notifications should not infer meaning from rows: the order domain should write stable `OrderShipped`-like outbox facts atomically, and CDC should relay them to an idempotent notification workflow. Trigger/change tables are a fallback where logs are inaccessible but require write-cost and migration review. Hourly full replacement may dominate for a small reference/search subset whose freshness allows it, but not timely notifications. The choice differs because consumer meaning, freshness, privacy and effect risk differ; one enterprise-wide mechanism is not automatically best.

### Answer 5

Create a source/capture inventory limited to scheduling fields; exclude clinical notes and identifiers unnecessary to the projection, use least-privilege credentials and tenant-isolated/encrypted destinations. Establish an engine-supported consistent snapshot boundary and retained-log budget; stage and reconcile the initial image before exposure. Introduce the new key additively: emit old and new stable identifiers with an explicit mapping version, backfill in bounded batches, make consumers dual-read/idempotently alias identities, then switch authority only after old/new keyed reconciliation. Preserve transaction metadata for appointment/provider changes and define order per appointment; do not claim cross-database global order. Handle deletes and key changes explicitly rather than as ordinary updates.

Test concurrent writes throughout snapshot, duplicate/redelivered and reordered records, crash before/after checkpoint, large transactions, schema changes, failover lineage, expired-history resnapshot and tenant-boundary attacks. Monitor log retention, lag in bytes/time, disk headroom, schema errors, delete rates and quarantine. Reconcile counts and canonical keyed digests per tenant and source position, plus invariants such as no appointment referencing an unknown provider. Before cutover require successful automated tests, signed reconciliation at the cutover boundary, restoration rehearsal, privacy/security review, and a named human database/domain reviewer for migration semantics. The human record must identify reviewer, evidence and unresolved risks; this internal chapter does not claim that external review occurred.
