---
module_id: DE-026
program: Data Engineering
level: 1
module_number: 26
title: Database Change Data Capture
status: complete
last_verified: 2026-09-02
---

# Database Change Data Capture

## One-Page Review

### Governing question

How can a data pipeline turn a database's finite transaction/change history into a complete, ordered, replayable stream of committed inserts, updates, and deletes without losing transaction meaning, exhausting source retention, or acknowledging progress before durable effect?

### Essential definitions

- **Change data capture (CDC)** observes database mutations from a supported log, change table, change stream, trigger journal, or version query and emits governed change records.
- A **source position** is an engine-scoped resume coordinate such as an LSN, log file/offset, GTID set, CDC LSN, sequence, or opaque resume token.
- A **change event identity** uniquely identifies one captured occurrence; it is distinct from the row/entity key that the occurrence changes.
- A **transaction envelope** groups changes that committed atomically at the source and records transaction identity, order, and commit boundary.
- A **before image** is relevant row state before a mutation; an **after image** is state after it. Availability depends on source configuration and operation.
- A **tombstone/delete event** explicitly represents removal; absence from a later query is not equivalent evidence.
- A **replication/capture slot** or capture instance is source-managed state retaining or materializing changes for a consumer under product-specific semantics.
- A **durable raw change log** stores immutable source envelopes before downstream projection so decoding and materialization can be replayed.
- A **committed offset** is the greatest source position whose required raw record and governed effects are durable.
- **retention headroom** is the distance or time between the consumer's required position and the oldest change still recoverable from the source.

### Central model, mechanism, or theorem

Let $S_c$ be current state at a consistent snapshot cut $c$, and let committed source transactions after $c$ through position $t$ be $T_{(c,t]}=(T_1,\ldots,T_n)$. Each transaction is an ordered set of row operations. If capture includes every required committed operation, schema/identity decoding is correct, and `applyTx` is transaction-atomic and replay-idempotent, then

$$
S_t=applyTx^*(S_c,T_{(c,t]}).
$$

This equivalence fails with a snapshot/stream gap, missing log history, filtered mutations, invisible deletes, incomplete transactions, wrong per-key order, missing schema, or an offset advanced beyond durable effects.

For committed connector offset $C$ and greatest source position durably represented by raw records and required receipts $D$, safety requires

$$
C\preceq D.
$$

Lag or crash can cause replay when $C\prec D$; stable event identities make that recoverable. $C\succ D$ can create silent loss.

### Critical invariants

- Source identity, engine/topology epoch, captured database/table scope, filters, schemas, log format, and start position are explicit and versioned.
- Only committed source changes enter the trusted stream; transaction boundaries/order are preserved to the degree the consumer contract requires.
- Each event carries stable occurrence identity, entity key, operation, source position, transaction identity/order, schema identity, and before/after availability.
- Source positions are compared only within their documented stream/topology domain; wall-clock and connector arrival time never replace source order.
- Initial snapshot and streaming changes meet at one exact retained boundary with no gap; any overlap is idempotent.
- Raw change records and transaction/batch receipts become durable before source feedback or connector offsets advance.
- Duplicate delivery yields one effect, while a conflicting event under the same identity fails closed; newer per-key source versions cannot be overwritten by older arrivals.
- Deletes, primary-key changes, truncates, DDL, and unsupported operations have explicit behavior rather than silent omission.
- Replication slots, logs, CDC tables, schema history, and before-image history retain enough data for worst-case lag and recovery, with alerting and hard safety thresholds.
- Reconciliation and rebootstrap remain available because a running connector and monotonic offset do not prove source completeness.

### Common failures

Treating a connector as exactly once by name; starting the stream after the baseline scan; recording only timestamps; sharing or recreating a slot without continuity proof; acknowledging the source after fetch but before raw commit; applying uncommitted transaction fragments; using arrival order across partitions; deduplicating by entity key and losing legitimate versions; assuming every update carries a full row; looking up “current” state and calling it the event image; missing hard deletes, key changes, truncate, or DDL; advancing across an undecodable event; letting a stalled slot fill source storage; jumping to the newest position after retention loss; logging sensitive before images; and using database CDC events as if they were stable business-domain events.

### Compact example

A baseline at position 100 contains `a=10,b=20`. Change 101 updates `a` to 11. Transaction 8 contains positions 102–103, deleting `b` and inserting `c=30`. Delivery repeats events 101 and 102. The consumer validates all positions, groups complete transactions, stores three unique raw events, applies transaction 8 atomically, and commits offset 103 only after publication. Replay produces the same `a,c` state. Missing position 102 blocks the modeled batch; an older update at 99 cannot regress `a`.

### Connections

[DE-021](021-full-and-incremental-extraction.md) defines baseline-plus-change equivalence, [DE-022](022-watermarks-and-high-water-marks.md) constrains progress, [DE-023](023-file-arrival-and-manifest-processing.md) supplies atomic publication, and [DE-025](025-database-snapshot-extraction.md) produces the baseline cut. The next modules develop idempotent loads, record identity, quarantine, and replay; [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies logs, replication, MVCC, and recovery semantics.

## Governing Question

What evidence allows a CDC system to claim that every in-scope committed source mutation after a known baseline has been durably captured and can reconstruct the same governed state, even when connectors crash, events repeat, transactions span many rows, schemas change, and source history is finite?

CDC is often introduced as “read the database log and publish events.” The hard part lies in the nouns. Which log and topology epoch? Which tables, operations, transactions, and schemas are represented? What position is safe to resume? What does the source retain, and until when? What happens between publication and offset acknowledgement? Which ordering is preserved after downstream partitioning?

The database commit log is designed first for the database's recovery or replication protocol. Logical decoding, binary-log readers, CDC tables, and change streams translate that internal history into supported consumer records. Each translation has scope, configuration, retention, and version limits. A connector adds its own buffering, serialization, transport, offsets, retries, transformations, and failures.

Therefore a trustworthy CDC design is an end-to-end protocol. It defines the source boundary, preserves raw evidence and transaction context, commits output before progress, applies stable identity/version rules, monitors retention, and periodically verifies materialized results against an independent source cut.

## Why This Matters

Incremental capture can reduce extraction from billions of current rows to the thousands that changed. It can expose hard deletes, commit order, transaction identity, and low-latency updates that timestamp polling misses. It is also the foundation for database replication, cache/index refresh, audit feeds, streaming analytics, and zero-downtime migrations.

Those benefits depend on continuity. Source change history is finite. PostgreSQL WAL, MySQL binary logs, SQL Server capture tables, and MongoDB oplogs or pre/post-image collections can be recycled or cleaned. A connector that falls behind may keep running until it reaches an unavailable position—or may be configured to skip forward. Silent reset changes “temporarily stale” into permanent data loss.

Delivery is usually replay-prone. A connector can write an event and crash before recording its offset; on restart it reads the event again. Avoiding re-delivery entirely is harder than making it harmless. Stable occurrence identity, immutable raw records, conditional receipts, and source-version-aware sinks convert at-least-once delivery into one governed effect.

Transactions complicate streaming. A source transaction may update orders, inventory, payments, and an audit table atomically. Publishing or applying one row before the commit boundary can expose a state the source never committed. Buffering the full transaction preserves atomic materialization but creates memory, latency, and oversized-transaction risks. The required boundary must be chosen explicitly.

Schema determines event meaning. A byte sequence at position 500 may require table metadata from that point, not today's schema. Before/after columns depend on replica identity or row-image settings. A new enum value, type conversion, table rename, primary-key change, or column drop can make old events undecodable or semantically different.

Finally, a database change is not automatically a domain event. Five low-level row writes might implement one business action, while one row change might be maintenance. CDC preserves what the database logged; consumers should not infer stable product intent that the source contract never promised.

## Prerequisites and Retrieval

Retrieve source owner, engine/distribution/version and topology; primary/replica/failover model; transaction/log implementation; supported logical decoding, binary log, CDC table, or change stream interface; database/table/column/publication/filter scope; engine and connector privileges; network/TLS and credential policy; source position format/domain/order; log/capture retention and cleanup; slot/capture-instance lifecycle; source storage limits; initial snapshot protocol and paired start position; current offsets; transaction identity/boundaries/order; multi-table and multi-shard behavior; row/event identity; primary-key/replica-identity rules; insert/update/delete/truncate/DDL representations; before/after/full-document availability; schema/catalog history; type mapping; time and time-zone fields; connector/version/configuration; transport topics/partitions; serialization and schema registry; producer acknowledgements; raw landing; output/idempotency transaction; checkpoint/feedback mechanism; concurrency/rebalance; retry/backoff; heartbeat/idle progress; backpressure; large transaction handling; data classification; before-image retention; downstream materializations; reconciliation; rebootstrap; upgrade/failover runbooks; alerting; recovery objectives; and incident history.

Distinguish physical redo/WAL record from logical row event; transaction ID from event position; event occurrence identity from entity key; database commit time from connector processing/arrival time; position order from wall-clock order; one stream's LSN/offset from another topology's coordinate; fetched event from durably published event; source slot feedback from downstream effect; transport exactly-once feature from end-to-end semantic effect; snapshot record from later change; update delta from after image; current lookup from event-time image; delete from absence; primary-key update from ordinary update; truncate from enumerated deletes; DDL notification from compatible schema; heartbeat/progress record from data event; running connector from advancing recoverable position; lag in seconds from retention bytes; stalled empty table from healthy whole-source capture; and CDC record from business event.

Build a source contract matrix before enabling capture:

| Concern | Evidence to record |
|---|---|
| Identity | Engine/cluster/database, topology epoch, slot/capture instance, connector name/version |
| Scope | Publications/tables/columns/filters, tenant/security context, unsupported objects |
| Position | Token format/domain, ordering, start/end, feedback/ack rule, failover mapping |
| Transaction | Begin/commit/abort representation, event count/order, large-transaction policy |
| Rows | Stable key, operation, before/after image, key update, delete/truncate semantics |
| Schema | Source schema ID/history, DDL handling, type/time/decimal mapping, compatibility policy |
| Retention | Current oldest/newest positions, slot/log/CDC cleanup, maximum lag and storage thresholds |
| Output | Raw envelope, immutable identity, topic/partition/order, manifest/receipt, checkpoint |
| Recovery | Duplicate/rebalance/crash behavior, invalid position, failover/upgrade, rebootstrap |
| Assurance | Reconciliation scope/cut, counts/keys/digests/controls, ownership and escalation |

## Learning Objectives

After completing this module, you should be able to:

1. compare native log-based CDC, change tables/streams, triggers, and query polling;
2. define source positions, topology epochs, transaction boundaries, and event identities without relying on wall-clock order;
3. coordinate an initial snapshot with streaming at one gap-free retained boundary;
4. model insert, update, delete, key change, truncate, and DDL envelopes including before/after limitations;
5. preserve source transactions or document weaker row/event-level visibility;
6. make raw publication, downstream effects, and offset feedback replay-safe;
7. manage log/slot/capture retention, lag, backpressure, heartbeats, and large transactions;
8. evolve schemas and connectors without silently skipping undecodable history;
9. recover safely from crash, rebalance, failover, upgrade, missing history, and position conflict; and
10. reconcile CDC materialization against a compatible source snapshot and state its evidence limits.

## Core Exposition

### Choose a capture mechanism from required evidence

Native log-based CDC reads a supported logical view of a transaction/replication log. It usually captures committed inserts, updates, and deletes with durable source positions and low application overhead. It needs privileged configuration, log retention, schema decoding, and careful failover/upgrade operations.

Database-provided change tables materialize mutations into queryable tables with source LSN/time mappings and cleanup jobs. They can be operationally accessible but introduce capture latency and finite table retention. Change streams expose a supported cursor/resume-token API, sometimes spanning shards and including metadata or pre/post images under configuration.

Application triggers can write an audit/outbox table in the same transaction. They provide explicit logical fields and broad engine support, but add write-path cost, deployment coupling, recursion/disable/bypass risk, and their own retention. Query polling is simplest when a complete monotonic version and tombstones exist, but it often misses hard deletes and intermediate changes.

Select from required operations, latency, transaction/order fidelity, source impact, privileges, retention, schema evolution, and recovery—not from connector availability alone. Preserve a full snapshot/reconciliation path even when CDC is primary.

### Treat the database interface as the source of truth

Use the engine's documented logical interface or supported connector protocol. Do not parse physical WAL/binlog files with an unversioned custom decoder unless ownership includes format evolution, corruption handling, encryption, compression, recovery, and upgrade compatibility.

PostgreSQL's [logical decoding concepts](https://www.postgresql.org/docs/current/logicaldecoding-explanation.html) describe decoding WAL changes into application-specific form and replication slots as ordered streams from one database. MySQL's [binary log documentation](https://docs.oracle.com/cd/E17952_01/mysql-8.4-en/binary-log.html) describes events recording data and schema changes for replication and recovery-related use. These mechanisms are engine-specific and not interchangeable.

Record exact engine, server/plugin, connector, driver, protocol, and output schema versions. Test upgrades from retained historical positions before production rollout.

### Define stream identity and position domain

Represent a source position as

$$
p=(e,d,o,x),
$$

where $e$ is engine/cluster and topology epoch, $d$ is database/shard/channel, $o$ is origin or slot/stream identity, and $x$ is the engine-specific coordinate. Only compare positions when their domains are compatible.

An integer-looking LSN fragment or file offset is not globally ordered across failover timelines, servers, databases, or shards. A GTID set can represent executed transactions rather than one scalar. An opaque resume token must be stored exactly, not decoded and reconstructed by the client.

Persist both source position and source identity. A reused connector name pointed at a restored database can otherwise resume into unrelated history.

### Start only from a proven position

First startup requires one of:

- a consistent baseline snapshot paired with a stream position;
- a retained source position known to precede all required history;
- an explicit “from now” contract that admits no historical state; or
- a trusted prior raw log/checkpoint whose source history remains resumable.

Never infer a start from current time. Never choose “latest” merely because an earlier offset fails. Latest discards an unknown interval. If the materialized sink needs current state, rebootstrap with a new consistent snapshot and coordinated stream position.

Validate the start against oldest/newest available positions, slot state, source epoch, schema history, and downstream receipt. Record the decision and approval when intentionally excluding history.

### Coordinate snapshot and stream

Let baseline $S_c$ represent source cut $c$ and change stream begin after paired position $p_c$. The protocol must retain all changes committed after the cut while the snapshot is read. Start/capture the log boundary using the engine/connector facility, scan the consistent snapshot, publish it, then apply buffered changes in source order.

Starting the stream after the scan creates a gap. Applying changes immediately and later overwriting them with older snapshot rows creates regression. A documented overlap is acceptable only with source positions and idempotent version rules.

Debezium's [PostgreSQL connector documentation](https://debezium.io/documentation/reference/stable/connectors/postgresql.html) gives a concrete connector example: initial snapshot/LSN, streaming, replication slots, event envelopes, replica identity, transaction metadata, and duplicate possibilities. Treat its exact behavior as configuration/version-specific and validate the deployed connector.

### Capture only committed changes

Database logs may contain records for uncommitted or aborted work. A logical interface normally buffers/decodes according to transaction semantics, but the connector must understand begin/commit/abort behavior. Do not publish aborted mutations as trusted changes.

For transaction $T_j=(e_{j,1},\ldots,e_{j,m})$, preserve transaction ID, event order, total/order metadata when available, and commit position/time. Decide whether raw consumers may see events before the end marker. A current-state sink requiring atomic cross-row visibility must stage all $m$ events and publish/apply them in one destination transaction or versioned batch.

Very large transactions may exceed memory or broker limits. Spill immutable fragments with transaction identity and ordinals, then publish a commit manifest only after all fragments arrive. Bound transaction age/bytes/events and alert rather than silently splitting semantics.

### Design a complete change envelope

At minimum include source engine/cluster/database/schema/table, topology epoch, slot/stream, source position, transaction ID/order/commit position, operation, stable event identity, entity key before/after as needed, schema ID/version, before/after/delta fields with availability flags, source commit time if reliable, connector processing time, snapshot indicator, trace/request metadata if approved, and raw digest/version.

Distinguish unavailable from null. If a before-image column is not logged, encode absence explicitly; do not fill `null` and imply the old value was null. If a large/toasted/blob value is omitted or unchanged, preserve that status.

Separate source envelope from transport metadata such as topic, partition, offset, producer timestamp, and retry attempt. Both matter for diagnosis, but transport offset is not database order.

### Establish stable event identity

Prefer a source occurrence identifier composed from compatible stream identity, transaction/position, and row ordinal or provider resume token. It must distinguish multiple changes to the same key within one transaction and remain stable on replay.

Entity key identifies the row/materialized object. It is not sufficient for deduplicating a history stream because updates 7 and 8 to account A are distinct occurrences. Payload hash alone is also unsafe: separate legitimate events can have equal bytes, while semantically identical events can serialize differently.

If the source emits one position for multiple row changes, add the documented within-position/transaction ordinal. Never invent uniqueness from arrival order, which changes on replay.

### Model row operations explicitly

Insert establishes a key and after image. Update may carry before+after, changed columns, or an after image. Delete needs old key and perhaps before image. Replace can differ from patch. Truncate/drop can affect unenumerated rows and must either be represented, forbidden, or trigger rebootstrap.

A primary-key update can appear as one update, delete+insert, or another engine-specific sequence. Preserve old and new identity so the sink removes the old key and creates the new without duplicating state.

Define upsert conflicts and impossible histories: update for absent row, insert over live row, delete absent, older version after newer, schema/key mismatch. Some are valid after filtering or partial bootstrap; classify rather than guess.

### Configure row identity and images

Logical decoders need a way to identify updated/deleted rows. Primary/unique keys and engine replica-identity or row-image settings determine what old columns appear. Capture configuration changes as contract changes.

MySQL's [binary logging options](https://docs.oracle.com/cd/E17952_01/mysql-8.4-en/replication-options-binary-log.html) documents row-based format and `binlog_row_image` choices including full/minimal/noblob. PostgreSQL publications/replica identity and other engines have different rules. Verify every table, especially keyless tables.

Full images simplify downstream reconstruction but increase source log, network, raw storage, privacy exposure, and schema coupling. Minimal images reduce cost but require stable baseline/current-state lookup and schema-aware patch semantics. A later lookup returns later current state, not necessarily the after image at event commit.

### Preserve source transaction and per-key order

Within one source stream, retain engine position and transaction ordinal. Across database shards or independent logs, there may be no total order; model a partial order plus per-key/transaction constraints rather than sorting by timestamps.

Downstream partitioning by entity key preserves per-key transport order in many brokers but splits multi-key transactions. Partitioning by transaction keeps its changes together but can skew and complicate current-state locality. A transaction-aware manifest/coordinator can stage fragments before atomic publication.

Consumers apply only events newer than their stored source version within a compatible position domain. Arrival timestamp and broker offset from a different partition cannot establish source recency.

### Treat time fields as observations

Database commit timestamp, statement time, row business time, connector processing time, broker time, and sink time answer different questions. Not every engine records commit time, and clocks can skew. Source position—not time—usually governs resume/order.

Use commit/processing time for lag diagnostics with known clock assumptions. Do not checkpoint `max(ts_ms)` or reorder transactions solely by time. Multiple commits can share precision; one transaction can contain rows with many business times.

### Retain schema history by position

Decode each event using schema valid at its source position. Store schema IDs/definitions or an independently versioned catalog history. A current schema cannot reliably decode a dropped/renamed/type-changed column in old retained raw data.

Define additive and breaking behavior for column add/drop/rename, null/default, precision/scale, enum/domain, generated columns, collation, key changes, table rename, partition movement, and DDL. Preserve unknown fields in raw envelopes; quarantine unknown required meaning without advancing beyond it.

PostgreSQL's [logical replication restrictions](https://www.postgresql.org/docs/current/logical-replication-restrictions.html) documents product-specific schema-definition handling and other restrictions. Connector schema registries and converters add another compatibility layer; validate both database and serialized contracts.

Do not assume DDL is emitted in the same stream. If it is absent, observe catalogs/migrations through a coordinated channel and fence deployments. If DDL events exist, consuming them safely still requires authorization, compatibility, and application order.

### Understand full-document lookups

Some change streams provide only an update delta and optionally query current state for a full document. MongoDB's [change-stream documentation](https://www.mongodb.com/docs/manual/changeStreams/) explains resume tokens and notes that an update lookup can return a later majority-committed document rather than the document at event time.

Label looked-up state with lookup time/position and never merge it into the immutable source event as if it were the original after image. A deletion or key change before lookup can make it missing. Use pre/post-image facilities when their retention and required/optional semantics fit, or reconstruct from baseline plus ordered deltas.

### Land raw changes before projection

Write immutable raw events or transaction fragments immediately after validation. Include source and transport envelopes, exact schema reference, body digest, connector/config version, and receipt. Encrypt and restrict before images according to classification.

Raw landing decouples finite source retention from slower transformations. Once raw history is durable and complete through $p$, the database slot can potentially advance even if a derived view is rebuilding—only if the raw system and replay SLA are authoritative and verified.

Organize raw files/topics by source identity and bounded positions, not only ingestion date. Publish batch/transaction manifests with first/last positions, event/transaction counts, schemas, checksums, gaps, and prior manifest linkage.

### Advance offsets after durable evidence

Let $D_r$ be greatest position durably stored raw, $D_s$ greatest required sink effect, and policy require both. Then safe progress is

$$
C\preceq\min(D_r,D_s).
$$

If raw is the authoritative replay boundary and sinks are independently checkpointed, source feedback may follow $D_r$ while each sink tracks its own progress. State this architecture explicitly and monitor raw durability/retention.

Batch fetch, raw write, transport publish, offset storage, slot feedback, and sink commit rarely share one database transaction. Use idempotent event keys, transactional transport when supported, conditional receipts, and recovery reconciliation. After ambiguous failure, read receipts/offsets before advancing.

Never acknowledge a position merely because it was fetched or placed in memory. A crash after feedback but before durable output can make the source discard the only remaining copy.

### Expect duplicate delivery

A crash after event publication and before offset commit causes replay. Rebalance, server recovery, slot checkpointing, network response loss, or operator rewind can do the same. Duplicate delivery is normal.

For event identity $I(e)$ and state $S$, effect idempotence requires

$$
apply(e,apply(e,S))=apply(e,S).
$$

Implement unique event receipts and source-version-aware current-state updates atomically with effects. The same identity and digest returns the prior result; same identity with different content is corruption/conflict. Do not discard a later distinct version because its entity key was seen before.

Framework “exactly once” features have topology, mode, connector, transaction, and consumer constraints. They do not prove database-to-all-external-side-effects exactly once. Verify the entire boundary and retain idempotence.

### Manage slots and retained history

Replication slots or capture instances are durable source resources, not harmless bookmarks. They may retain WAL/log/catalog state or change rows until feedback/cleanup. Inventory owner, consumer, scope, creation, current/restart/confirmed positions, active session, lag bytes/time, retention limit, alert thresholds, and removal procedure.

Never share a single-consumer slot unless the product explicitly supports fan-out semantics. Never drop/recreate a slot as routine troubleshooting; a new slot cannot reconstruct already recycled history. Use one capture into durable raw transport, then fan out downstream consumers there.

SQL Server's [CDC monitoring documentation](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/administer-and-monitor-change-data-capture-sql-server?view=sql-server-ver17) describes retention-based cleanup of capture tables. The [change-data query documentation](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/work-with-change-data-sql-server?view=sql-server-ver17) exposes validity intervals through minimum/maximum LSN functions. Configure and monitor the actual product/version.

### Measure retention headroom

Let $p_c$ be consumer-required position, $p_{old}$ oldest recoverable position, and $p_{new}$ source head. Position subtraction may be meaningful only through engine APIs. Track both recoverable distance and observed time, plus generation rate.

If history capacity is $H$ bytes, current generation rate $r>0$ bytes/s, and current retained backlog $b$, a crude remaining time is

$$
t_{remaining}=\frac{H-b}{r}.
$$

This assumes stable rate and usable full capacity, so alert conservatively with peak rate and safety margin. Lag in seconds can look small while a large transaction consumes disk rapidly; bytes can look small on an idle stream while cleanup age is near expiry.

Throttle downstream work, but never let backpressure silently threaten source availability. Land raw changes quickly, scale consumers, shed optional projections, expand approved retention, or pause source writes through incident authority. If safety limits are breached, choose source availability versus capture continuity explicitly.

### Use heartbeats without inventing data

Idle captured tables can make the last data-event position appear stale even while the connector is healthy or unrelated WAL accumulates. A heartbeat/progress record can prove stream liveness and advance offsets under connector-specific behavior.

Label heartbeats as control records, not mutations. Verify whether they cause source log activity, operate in the captured database, advance slot feedback for unrelated changes, and preserve ordering. Monitor end-to-end canary changes for stronger coverage when appropriate.

A heartbeat received downstream proves one path at one time, not completeness of every table/filter/schema. Combine it with source slot/log metrics and reconciliation.

### Handle backpressure and large transactions

Bound connector queues, poll/fetch sizes, transaction spill, broker request sizes, raw object sizes, memory, and retry buffers. Propagate downstream congestion before out-of-memory failure, but keep source-retention headroom visible.

Large transactions delay commit visibility and can create bursts far above average. Estimate maximum transaction bytes/events, not only events per second. Spill safely while retaining uncommitted status; abort fragments never publish.

Do not split a transaction into independently acknowledged source offsets if recovery could lose later fragments or expose partial effect. If consumers only require per-row eventual state, document the weaker boundary and still preserve transaction metadata in raw history.

### Handle filters and scope changes

Capture filters reduce volume and exposure but can break meaning. A child table without its parent, an update moving a row into/out of filter scope, or missing DDL can make events ambiguous. Define whether transitions produce insert/delete-like boundary events.

Changing table/column filters, publication membership, tenant scope, transformation predicates, or topic routing changes the source contract. Fence at a source position, publish a new configuration generation, backfill newly included state, retain removed-object deletion policy, and reconcile.

Never update filters in place while reusing the same offset and call the stream continuous. The new scope lacks prior history unless explicitly bootstrapped.

### Plan failover and upgrades

Record source cluster identity, origin/server UUID, timeline/epoch, slot/capture-instance failover support, and position mapping. Before promotion, prove the new primary contains all acknowledged source history and can resume the exact stream. A position that exists numerically on another timeline is not sufficient.

Test connector, plugin, engine, serializer, schema registry, broker, and offset-store upgrades against retained events. Preserve rollback readers and avoid writing new envelopes that old recovery tooling cannot read before the rollback horizon closes.

If slot/capture state is lost, compare durable raw high position, old/new source histories, and snapshots. Do not trust whichever coordinate is larger. Freeze publication and rebootstrap when continuity cannot be proven.

### Recover from missing history honestly

An invalid/expired LSN, GTID, CDC low watermark, or resume token is evidence of a gap. Moving the checkpoint to the oldest/current available point merely hides it.

Create a new generation: acquire a consistent snapshot at cut $c'$, pair it with a new retained stream position, land/validate the baseline, apply all changes after the cut, reconcile, and atomically publish. Preserve the prior gap incident and supersession lineage.

If only one partition/table lost history, use an independently consistent partial rebootstrap only when key/table relationships and ordering make it safe. Otherwise rebuild the governed aggregate.

### Keep database changes distinct from domain events

CDC exposes persistence implementation: table names, normalization, retries, maintenance, and transaction patterns. Domain consumers need stable business intent, actor, command identity, and semantics that row deltas may not contain.

Use a transactional outbox when the application can write an explicit domain integration event in the same transaction as state. CDC can transport the outbox rows reliably. Govern event schema, unique ID, aggregate order, publication, retention, and privacy; outbox does not eliminate duplicate delivery or consumer idempotence.

Do not expose raw operational tables broadly as public event contracts. Maintain access boundaries and allow internal analytical consumers to use raw CDC with its lower-level semantics.

### Reconcile current state and history

At a source snapshot cut $c$, materialize baseline plus CDC through paired position and compare exact source/destination key sets, source versions, selected payload digests, counts, and business controls. Apply pending transactions consistently on both sides.

Reconcile stream properties too: monotonic positions per domain, transaction begin/end/counts, no unknown schema gaps, event identity uniqueness, delete/key-update behavior, and raw manifest linkage. A correct current state can conceal duplicated or missing intermediate history that later updates happened to overwrite.

Use independent queries/export paths so the connector does not validate itself. Repair through immutable replay or a new snapshot generation, not manual untracked sink edits.

### Secure and govern captured history

CDC can expose every changed value, including secrets later removed, old personal data, and administrative corrections. Minimize captured columns, restrict before images, encrypt transport/storage, isolate credentials, audit access, and apply deletion/retention obligations to raw history and schema metadata.

Grant narrowly scoped replication/capture and table access rather than broad superuser/admin roles. Protect slot management, offset reset, connector configuration, topic creation, schema registration, quarantine, replay, and rebootstrap as privileged operations with review and audit.

Treat source values and schema names as untrusted data. Bound payload/decompression/nesting, avoid dynamic code/deserialization, sanitize logs, and prevent source-controlled topic/path/SQL injection.

### Observe the full continuity chain

Monitor source head/oldest/slot/capture positions, lag bytes/time, disk/change-table usage, active consumer, transaction age/size, connector fetch/publish/error/restart/rebalance, raw first/last positions and gaps, transport partition/offset, schema decode/quarantine, committed source/raw/sink offsets, current-state apply, reconciliation drift, heartbeat/canary, credentials, and deprecation/upgrade status.

Alert on missing advance relative to source changes, decreasing retention headroom, source feedback ahead of raw receipt, raw position ahead of schema availability, incomplete transaction, event identity conflict, unexpected scope/schema/topology change, and current-state version regression.

Runbooks must distinguish transient pause, slow consumer, invalid credential, source disk emergency, lost position, failover divergence, schema incompatibility, oversized transaction, corrupt raw event, sink regression, and reconciliation drift. “Restart connector” is not a recovery strategy until the safe position and retained history are proven.

## Definitions and Notation

Let:

- $p=(e,d,o,x)$ be a source position with engine/topology, database/channel, origin/stream, and coordinate;
- $S_c$ be the complete baseline state at cut $c$;
- $T_j=(e_{j,1},\ldots,e_{j,m_j})$ be committed source transaction $j$;
- $T_{(c,t]}$ be every required committed transaction after cut $c$ through position $t$;
- $I(e)$ be stable event occurrence identity;
- $K(e)$ be affected entity/row identity;
- $V(e)$ be source position/version used for per-key monotonicity;
- $R$ be the immutable raw event/transaction log;
- $D_r$ and $D_s$ be greatest source positions durably represented raw and in a required sink;
- $C$ be committed source feedback/connector offset;
- $H$ be usable retained-history capacity, $b$ current retained backlog, and $r$ generation rate.

State reconstruction is

$$
S_t=applyTx^*(S_c,T_{(c,t]}),
$$

under completeness, ordering, schema, identity, and atomicity premises. Offset safety is

$$
C\preceq\min(D_r,D_s)
$$

when both raw and sink durability are required before source progress. If raw is the authoritative replay boundary, source $C\preceq D_r$ while every sink maintains its own checkpoint against $R$.

Event-effect idempotence is

$$
apply(e,apply(e,S))=apply(e,S),
$$

while transaction atomicity means no published materialization exposes a strict nonempty subset of the operations of a committed source transaction when the contract promises transaction visibility.

A crude capacity horizon is

$$
t_{remaining}=\frac{H-b}{r},\qquad r>0,
$$

subject to variable generation, reserved capacity, cleanup policy, and engine-specific position/retention behavior.

## Mechanisms, Invariants, or Proof Structure

**Baseline-stream equivalence theorem, conditional.** If $S_c$ is a complete consistent baseline, the stream contains every required committed transaction after $c$ through $t$ exactly once by identity (duplicates allowed by delivery but removed by effect), transaction/per-key order is preserved, schemas and row operations decode correctly, and application is atomic as required, then repeated transaction application yields source state $S_t$.

**Proof sketch.** Base state equals source at $c$. Assume applied state equals source after transaction $T_j$. The next complete committed transaction contains the same source operations in their required order, so atomic `applyTx` yields the source state after $T_{j+1}$. Replay is a no-op by identity. Induction reaches $t$. A missing, reordered, misdecoded, aborted, or partial transaction breaks the inductive step.

**Position-domain invariant.** $p_1\preceq p_2$ is meaningful only when engine/topology/database/origin domains are compatible under the source contract. Numeric or timestamp comparison cannot bridge incompatible epochs.

**Commit-only invariant.** Aborted/uncommitted operations never enter trusted manifests/materializations. Transaction fragments remain staged until an authenticated/validated commit boundary and complete ordinal set exist.

**Offset-safety invariant.** $C$ never exceeds the durability boundary required by architecture. If feedback is lost after durable write, replay occurs; if feedback advances before durable write, unique source history can be lost.

**Identity invariant.** Repeated $I(e)$ with the same digest returns the existing receipt; conflicting content fails. Distinct $I(e)$ values for the same $K(e)$ remain legitimate versions and are ordered by compatible $V(e)$.

**Per-key monotonicity.** A materialized row/tombstone accepts $e$ only if $V(e)$ is newer than stored version in the same domain. Older delayed/replayed events cannot regress or resurrect state.

**Snapshot-handoff invariant.** Baseline cut and stream start share one engine-proven boundary; all later transactions remain retained during bootstrap. Any overlap is deduplicated and no interval is unrepresented.

**Schema-by-position invariant.** Every event references the schema/row-image contract valid at its position. Unknown required meaning blocks progress rather than being silently coerced.

**Retention invariant.** Oldest recoverable source/raw/schema position never advances beyond the earliest position required by every governed recovery consumer without an explicit superseding baseline.

**Reconciliation boundary.** Compatible-cut key/version/payload equality supports current-state fidelity for covered fields. It cannot establish intermediate-history completeness; stream identity/transaction/gap evidence is separately required.

<!-- bijux-verify: {"id":"transactional-cdc-replay","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"unique_events=3\nduplicate_deliveries=2\ntransactions=2\ncheckpoint=103\ncurrent_keys=a,c\ndelete_propagated=True\ntransaction_atomic=True\nreplay_idempotent=True\ncrash_before_checkpoint_replays=True\ngap_detected=True\nolder_event_ignored=True\n","stderr":""}} -->
```python
events = {
    101: {"tx": "tx-7", "tx_size": 1, "key": "a", "op": "update", "value": 11},
    102: {"tx": "tx-8", "tx_size": 2, "key": "b", "op": "delete", "value": None},
    103: {"tx": "tx-8", "tx_size": 2, "key": "c", "op": "insert", "value": 30},
}
deliveries = (101, 102, 103, 101, 102)

def consume(delivered, publish=True):
    raw = {}
    duplicates = 0
    for position in delivered:
        event = events[position]
        if position in raw:
            assert raw[position] == event
            duplicates += 1
        raw[position] = event

    positions = sorted(raw)
    continuous = positions == list(range(101, positions[-1] + 1)) if positions else False
    grouped = {}
    for position in positions:
        grouped.setdefault(raw[position]["tx"], []).append((position, raw[position]))
    complete = continuous and all(len(items) == items[0][1]["tx_size"] for items in grouped.values())

    state = {"a": 10, "b": 20}
    versions = {"a": 100, "b": 100}
    committed_states = []
    if complete:
        for items in sorted(grouped.values(), key=lambda group: group[0][0]):
            candidate = dict(state)
            candidate_versions = dict(versions)
            for position, event in items:
                if position <= candidate_versions.get(event["key"], -1):
                    continue
                if event["op"] == "delete":
                    candidate.pop(event["key"], None)
                else:
                    candidate[event["key"]] = event["value"]
                candidate_versions[event["key"]] = position
            state, versions = candidate, candidate_versions
            committed_states.append(dict(state))

    manifest = tuple((position, raw[position]) for position in positions) if complete and publish else None
    checkpoint = positions[-1] if manifest is not None else 100
    return state, versions, raw, duplicates, grouped, committed_states, checkpoint, manifest, complete

state, versions, raw, duplicates, grouped, commits, checkpoint, manifest, complete = consume(deliveries)
replay = consume(deliveries)
crashed = consume(deliveries, publish=False)
gap = consume((101, 103))

older = {"tx": "old", "tx_size": 1, "key": "a", "op": "update", "value": 9}
state_after_older = dict(state)
if 99 > versions.get(older["key"], -1):
    state_after_older[older["key"]] = older["value"]
older_ignored = state_after_older == state

print(f"unique_events={len(raw)}")
print(f"duplicate_deliveries={duplicates}")
print(f"transactions={len(grouped)}")
print(f"checkpoint={checkpoint}")
print(f"current_keys={','.join(sorted(state))}")
print(f"delete_propagated={'b' not in state}")
print(f"transaction_atomic={commits[-1] == {'a': 11, 'c': 30}}")
print(f"replay_idempotent={state == replay[0] and manifest == replay[7]}")
print(f"crash_before_checkpoint_replays={crashed[6] == 100 and crashed[7] is None}")
print(f"gap_detected={not gap[8]}")
print(f"older_event_ignored={older_ignored}")
```

The execution demonstrates one finite integer-position model, two transactions, duplicate delivery, one gap, and in-memory publication. It does not prove that real database positions are contiguous integers, that a connector emits complete transactions, or that production storage and offset commits are atomic.

## Alternatives and Trade-Offs

**Native log CDC versus triggers.** Native logs minimize application coupling and preserve commit positions but require engine privileges/format support. Triggers create explicit rows transactionally but add write latency, can be disabled/bypassed, and need deployment/retention ownership.

**CDC tables versus streaming decoder.** Queryable change tables simplify access and range reads but add capture jobs/latency/storage cleanup. Streaming decoders reduce latency but demand long-lived connections, slot/log management, and immediate backpressure handling.

**Query polling versus log capture.** Polling is portable with a reliable version/tombstone and modest volume. Logs capture intermediate changes and hard deletes more completely but increase operational complexity.

**Full versus minimal row images.** Full images ease independent consumers and replay while increasing log, bandwidth, storage, and privacy cost. Minimal deltas are compact but require baseline/schema/order and cannot be replaced by later current lookup.

**Row-level versus transaction-level publication.** Row publication lowers latency/memory but can expose partial source transactions. Transaction manifests preserve atomic visibility at the cost of buffering, skew, and large-transaction limits.

**One source slot per consumer versus raw fan-out.** Direct slots isolate progress but multiply source retention/resources and operational risk. One governed capture into durable raw transport lets many downstream consumers replay independently.

**Entity-key versus transaction partitioning.** Entity key preserves per-key ordering and balance. Transaction key preserves multi-row grouping but may skew; a coordinator can reconstruct transaction boundaries from fragments.

**At-least-once plus idempotence versus framework exactly once.** Replay-tolerant design crosses heterogeneous boundaries and remains necessary for recovery. Framework transactions can reduce duplicates within supported topology but require connector/configuration/consumer proof.

**Source offset after raw versus after every sink.** Advancing after durable raw protects source capacity and decouples slow sinks, but makes raw storage an authoritative recovery system. Waiting for all sinks couples retention to the slowest and increases source risk.

**Strict schema stop versus tolerant raw capture.** Strict decode protects semantics but can exhaust source retention during deployment. Raw byte/envelope capture can preserve history for later decode only if schema/format and security make it safely replayable.

**Current-state table versus immutable history.** Current state serves reads cheaply but cannot answer full mutation history. Immutable raw events support audit/rebuild but expand privacy, cost, and schema-retention obligations.

**CDC as integration event versus transactional outbox.** Raw CDC is immediate and broad but couples consumers to persistence. Outbox records intentional domain events in the source transaction but requires application changes and its own cleanup/idempotence.

**Rewind versus new baseline.** Rewind is ideal while all source/raw/schema history exists and identities are stable. When history or topology continuity is lost, a new consistent snapshot is safer than guessed offsets.

**Capture on primary versus replica/managed service.** Primary has authoritative log access but direct operational impact. Replica/service can isolate capture but adds lag, slot synchronization/failover, feature, and trust constraints.

## Failure Modes and Misconceptions

- **“CDC means exactly once.”** Capture and transport can replay around offset commits.
- **“The connector offset is the database state.”** It is one consumer's progress under a source-domain contract.
- **“A bigger LSN is always newer.”** Positions from different epochs/streams may be incomparable.
- **“Timestamp order equals commit order.”** Clocks/precision and transaction timing differ.
- **“Arrival order is source order.”** Parallel transport and retries reorder deliveries.
- **“Entity key deduplicates events.”** It collapses legitimate versions.
- **“Payload hash is event identity.”** Equal events can be distinct and encodings can differ.
- **“Updates always include full after rows.”** Images depend on engine/configuration.
- **“Null means column was null.”** It may mean unavailable or unchanged.
- **“Current lookup recovers the after image.”** It can observe later state or deletion.
- **“Deletes appear as missing rows.”** CDC needs explicit delete semantics.
- **“Primary-key change is a normal update everywhere.”** Representations differ.
- **“Truncate produces one delete per row.”** Many systems encode it separately or not at all.
- **“DDL automatically accompanies DML.”** Logical streams may not carry schema changes.
- **“Today's schema decodes historical events.”** Dropped/changed metadata can be required.
- **“Start at latest if offset fails.”** That discards an unknown interval.
- **“Start CDC after snapshot.”** Writes during snapshot form a gap.
- **“Apply stream then snapshot.”** Older baseline rows can overwrite newer state.
- **“Overlap is duplication failure.”** Idempotent overlap can make handoff safe.
- **“Commit offset after fetch.”** Memory is not durable output.
- **“Transport acknowledgement proves sink effect.”** External materializations can still fail.
- **“Framework exactly once covers every side effect.”** Its boundary is narrower and conditional.
- **“One slot can feed arbitrary consumers.”** Slot semantics and position ownership may be single-consumer.
- **“Dropping and recreating a slot repairs it.”** Recycled history does not reappear.
- **“Lag seconds alone protects retention.”** Generation bursts/bytes and cleanup horizons matter.
- **“Heartbeat proves every table is captured.”** It proves a control path at one time.
- **“Empty stream means no changes.”** Filter, permission, slot, or decode failures can hide them.
- **“Pause is harmless.”** Source logs/change tables can fill or expire.
- **“Large transaction is just many events.”** Atomicity and buffering create distinct risk.
- **“Schema error can be skipped.”** Later events may depend on the missing mutation/schema.
- **“Dead-letter then advance preserves completeness.”** It explicitly creates a gap unless governed repair fills it.
- **“Failover retains the same stream automatically.”** Slot/epoch/position continuity needs proof.
- **“Current-state reconciliation proves event history.”** Intermediate losses can be overwritten.
- **“CDC events are business events.”** They express persistence changes unless designed otherwise.
- **“Before images are safe audit data.”** They can retain secrets and erased personal values.
- **“Superuser is easiest.”** Excess privilege magnifies compromise and mistakes.
- **“Restarting is recovery.”** Only a proven resumable position makes restart safe.

## Worked Examples

### Example 1

A baseline scan starts at 01:00 and finishes at 03:00. The connector creates its log position only at 03:00. An order committed at 02:00 is newer than the row chunk read at 01:30 but older than the stream start.

The corrected engine-native bootstrap creates/captures the stream boundary with the consistent snapshot and retains changes while scanning. **Conclusion:** baseline and stream must meet at one source position.

### Example 2

Event 900 is published to raw storage, but the connector crashes before storing offset 900. Restart emits 900 again.

The raw writer uses `(source epoch, stream, position, ordinal)` as occurrence identity; identical replay returns the prior receipt, while downstream source-version merge is a no-op. **Conclusion:** duplicate delivery is expected and harmless by design.

### Example 3

One transaction debits account A and credits B. Key-partitioned consumers apply A immediately while B is delayed, exposing a broken total.

Raw records retain transaction ID, ordinals, expected count, and commit marker. A transaction assembler publishes one complete manifest and the balance view swaps/applies atomically. **Conclusion:** per-key order alone cannot preserve multi-key transaction visibility.

### Example 4

MySQL capture switches from full to minimal row images. A downstream processor interprets absent `currency` as null and overwrites a valid value.

Configuration and schema fingerprint changes fence the stream; the decoder represents “unchanged/unavailable” distinctly and patches only present fields. **Conclusion:** row-image policy is part of the data contract.

### Example 5

MongoDB update event 10 changes status to `PAID`; before the connector's full-document lookup, event 11 adds a refund flag. The lookup returns state after 11.

The pipeline keeps event 10's delta immutable and labels lookup output with its observation point rather than calling it event 10's after image. **Conclusion:** later lookup does not time-travel to event commit.

### Example 6

A connector is stopped for two days while a source produces 300 GB/day and has 500 GB free retention space. Required history is purged or the source disk enters emergency before restart.

Capacity/peak-rate alerts would have shown less than two days of headroom. Operators rebootstrap after continuity loss; they never advance to current and call the missing interval processed. **Conclusion:** retention is a correctness deadline and source-availability risk.

### Example 7

A column changes from decimal scale 2 to scale 4 at position 5,000. The consumer decodes events 4,900–5,100 using only the new schema and multiplies older values incorrectly.

Raw envelopes reference schema by position, and the decoder applies scale 2 before the boundary and scale 4 after it. **Conclusion:** historical schemas are executable data dependencies.

### Example 8

A PostgreSQL primary fails. A connector reconnects to a promoted server with a new slot whose numeric LSN is higher than its stored offset, so an operator chooses the maximum.

The system compares cluster/timeline and synchronized slot history, not scalar magnitude. Without continuity proof it freezes publication and creates a new snapshot/stream generation. **Conclusion:** failover positions require compatible provenance.

### Example 9

The current customer table reconciles perfectly, but a compliance consumer needs every consent transition. Two intermediate events were lost and a later snapshot overwrote state to the correct final value.

The team adds transaction/position continuity, raw identity counts, and source audit-range reconciliation; current-state equality alone cannot certify history. **Conclusion:** state and occurrence completeness are different requirements.

### Example 10

Checkout changes five internal tables for one purchase. Consumers infer a “PurchaseCompleted” domain event from one row, then a schema refactor breaks them.

The application writes an explicit versioned outbox event with business ID/actor/meaning in the same source transaction. CDC transports the outbox while raw internal changes remain private. **Conclusion:** transactional capture can carry domain intent but does not invent it.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md): WAL/redo, LSNs, transactions, logical decoding, replication slots, failover, backup, MVCC, and schema catalogs determine source semantics.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): system-of-record ownership, domain events, lineage, contracts, retention, and privacy define allowed capture.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): logs, partitions, ordering, backpressure, compaction, replay, and stateful processing shape transport/materialization.
- [Operating Systems](../../22-operating-systems/ROADMAP.md): files, buffers, crash/durability, clocks, disk capacity, and process/network failure underlie source and connector behavior.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): replication privileges, secrets, network isolation, unsafe payloads, before-image exposure, and erasure constrain the stream.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): partial orders, consistent cuts, idempotence, checkpoints, leases, failover, and exactly-once boundaries explain correctness.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): domain event contracts, compatibility, idempotency, async delivery, and authorization govern external consumers.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): connector lifecycle, credential delivery, schema services, quotas, observability, incident response, and rebootstrap workflows operationalize CDC.

## References

1. PostgreSQL Global Development Group, [Logical Decoding Concepts](https://www.postgresql.org/docs/current/logicaldecoding-explanation.html). Documents WAL logical decoding, replication slots, ordered change streams, persistence, and resource implications.
2. PostgreSQL Global Development Group, [Logical Replication Restrictions](https://www.postgresql.org/docs/current/logical-replication-restrictions.html). Documents product-specific schema, sequence, object, and operation restrictions relevant to logical change capture.
3. Debezium, [PostgreSQL Connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html). Documents snapshot/stream handoff, LSN offsets, slots, event keys/envelopes, replica identity, transaction metadata, duplicates, and operational recovery considerations.
4. Oracle, [MySQL 8.4 Binary Log](https://docs.oracle.com/cd/E17952_01/mysql-8.4-en/binary-log.html). Documents binary-log change events, purposes, formats, filtering, and purge behavior.
5. Oracle, [MySQL 8.4 Binary Logging Options and Variables](https://docs.oracle.com/cd/E17952_01/mysql-8.4-en/replication-options-binary-log.html). Documents row-based logging and before/after row-image configuration.
6. Microsoft, [Work with Change Data](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/work-with-change-data-sql-server?view=sql-server-ver17). Documents SQL Server CDC validity intervals, LSN endpoints, query functions, and change enumeration.
7. Microsoft, [Administer and Monitor Change Data Capture](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/administer-and-monitor-change-data-capture-sql-server?view=sql-server-ver17). Documents capture/cleanup jobs and retention-based management.
8. MongoDB, [Change Streams](https://www.mongodb.com/docs/manual/changeStreams/). Documents change events, resume tokens, oplog-history requirements, invalidation, transaction/shard behavior, and full-document lookup timing.

## Exercises

### Exercise 1

Design a CDC contract for PostgreSQL orders, payments, and order items using an initial snapshot and logical decoding. Specify publications/slot, identity/images, transaction handling, raw envelope, offset feedback, retention, schema changes, failover, and reconciliation.

### Exercise 2

A baseline at position 50 has `x=10,y=20`. Transaction A at positions 51–52 sets `x=15,y=15`; transaction B at 53 deletes `y`; event 51 and all of transaction B are delivered twice, while transport partitions reorder 52 before 51. Derive a correct raw/transaction/current-state process and final result.

### Exercise 3

A source has 2 TB usable log capacity, current retained backlog 800 GB, average generation 50 MB/s, peak 150 MB/s, and a four-hour recovery objective. Compute average and peak crude headroom using decimal units. Decide whether the objective is safe and identify omitted factors.

### Exercise 4

At position 900, a connector's stored offset is behind a recreated source slot that begins at 950. An operator proposes trusting the slot and advancing the offset. Explain the possible data loss and design a safe rebootstrap with evidence and publication boundaries.

### Exercise 5

Design fault-injection and mutation tests for a CDC pipeline covering source abort, duplicate delivery, crash before/after raw commit and offset feedback, incomplete/oversized transaction, row-image reduction, key update, truncate, DDL/type change, filter expansion, slot storage pressure, heartbeat-only activity, failover, schema-history loss, and current/history reconciliation.

## Answers to the Exercises

### Answer 1

Create a dedicated least-privilege replication role and explicit publication containing only approved columns/tables; inventory keyless/partitioned tables and configure replica identity adequate for updates/deletes. Give the connector a unique governed slot/publication and stable logical source identity. Record PostgreSQL/connector/plugin versions, database/cluster/timeline, scope, schema history, and LSN domain.

Acquire a consistent DE-025 baseline and its exact starting LSN through the supported connector protocol. Retain WAL while the snapshot lands; raw-stream changes after the cut under immutable occurrence IDs such as source+LSN+transaction ordinal. Preserve transaction ID/order/end/count, operation, old/new key, schema ID, before/after availability, source and connector times, raw digest, and transport metadata. Assemble multi-table transactions for any view requiring source atomicity; otherwise document row-level eventual visibility.

Write raw events/transaction manifests and receipts before advancing connector offsets/slot feedback. Fan downstream consumers from durable raw storage with independent checkpoints, unique event receipts, and source-version-aware merges. Monitor WAL retained bytes/time, restart/confirmed positions, connector/raw/sink lag, transaction size, schema failures, heartbeats, slot activity, disk thresholds, and reconciliation. Coordinate DDL with schema capture/fencing. Test synchronized failover slot/timeline behavior; without proof, rebootstrap. Periodically compare a compatible-cut source snapshot to baseline+CDC exact keys/versions/controls and separately audit position/transaction/event continuity.

### Answer 2

Raw ingestion uses source occurrence identity and positions, so the reordered arrival is staged rather than applied by transport order. It deduplicates repeated 51 and 53 only after verifying identical content. It groups 51–52 as transaction A and waits for the commit boundary/complete ordinal set, sorts by source transaction order, then publishes/applies both atomically. Transaction B at 53 is a complete one-event delete and its duplicate returns the same receipt.

Starting from `x=10,y=20`, transaction A produces `x=15,y=15`; transaction B removes `y`, leaving only `x=15`. Raw history retains three unique occurrences 51, 52, 53 plus delivery-attempt metadata. Offset 53 advances only after both transaction manifests/effects required by policy are durable. A crash before offset commit replays safely; an arrival of 52 without 51 cannot expose half of transaction A in an atomic materialization.

### Answer 3

With decimal units, usable capacity is 2,000 GB and backlog 800 GB, leaving 1,200 GB or 1,200,000 MB. At average 50 MB/s, headroom is 24,000 seconds = 400 minutes = 6 hours 40 minutes. At peak 150 MB/s, it is 8,000 seconds = 133 minutes 20 seconds = 2 hours 13 minutes 20 seconds.

The four-hour recovery objective is not safe at peak; history can exhaust about 1 hour 46 minutes 40 seconds sooner, before safety margin. Even average headroom leaves only 2 hours 40 minutes margin. The calculation omits reserved filesystem space, segment granularity, existing consumers, large transactions, cleanup/checkpoint behavior, compression, growth variability, restore/replay time, source disk SLO, schema history, raw/sink throughput, and detection/operator delay. Alert from conservative peak percentiles and shorten recovery/land raw faster or expand approved capacity.

### Answer 4

Durable downstream/raw state at 900 says changes after 900 are required. A recreated slot at 950 can no longer supply 901–949. Advancing the offset asserts those missing effects exist and lets the source discard evidence, causing silent loss. Numeric comparison does not prove the new slot shares the old topology/history either.

Freeze downstream publication and source feedback; preserve old offset, raw high position, slot/source epoch, schemas, logs, and incident evidence. Determine whether 901–949 exist in another retained archive/replica and replay them only with authoritative identities. If continuity cannot be proven, acquire a new consistent snapshot at cut $c'$ paired with a new slot/LSN, buffer all later changes, land/validate a new baseline manifest, apply changes after the boundary, and reconcile exact keys/versions/control totals at a compatible cut.

Conditionally supersede the old published generation only after baseline and stream handoff pass. Record the gap and new lineage; do not call it a resume. Protect future operations with slot-change audit, retention/headroom alarms, failover rehearsals, and a policy forbidding unreviewed offset/slot reset.

### Answer 5

Abort a source transaction and assert no trusted raw/materialized events appear. Duplicate events/transactions before and after raw commit; exact identities return prior receipts and distinct versions remain. Crash after fetch, partial raw write, raw commit, manifest, sink apply, offset store, and source feedback; assert restart either replays or resumes without missing/duplicate effect and feedback never exceeds the chosen durability boundary.

Split/delay a transaction, exceed memory/message limits, and verify spill fragments stay unpublished until complete commit; abort safely. Switch full to minimal images and require explicit unavailable/unchanged behavior. Change a primary key and validate old removal/new insert; inject truncate and unsupported DDL so policy rejects/rebootstraps rather than ignores. Add/drop/rename/type/scale/enum fields and remove schema history; decoding must use position schema or stop before progress.

Expand filters/publications and prove newly included prior state is backfilled under a fenced configuration generation. Stall sinks and fill slot/log/change tables toward thresholds; alarms and source-safety action occur before loss. Emit only heartbeats while an in-scope canary change is blocked; table/path monitoring must catch the false comfort. Promote a replica with/without synchronized history and require epoch/position proof. Finally compare compatible-cut current keys/versions/payload controls and independently assert event identities, transaction boundaries, positions, deletes, and schemas so correct final state cannot hide lost intermediate history.
