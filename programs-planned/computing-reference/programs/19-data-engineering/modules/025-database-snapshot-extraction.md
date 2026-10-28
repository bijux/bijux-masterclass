---
module_id: DE-025
program: Data Engineering
level: 1
module_number: 25
title: Database Snapshot Extraction
status: complete
last_verified: 2026-09-02
---

# Database Snapshot Extraction

## One-Page Review

### Governing question

How can a data pipeline extract a large, multi-object database state from one declared source cut, parallelize and serialize it without mixing histories, bound its impact on the source, and publish only a complete, validated, replayable snapshot?

### Essential definitions

- A **logical database snapshot** is the in-scope rows and metadata visible under one documented database read point and isolation contract.
- A **source cut** is the engine-specific transaction snapshot, sequence, log position, cluster time, SCN, backup identity, or equivalent that fixes visibility.
- A **snapshot holder** is the transaction/session/job that keeps a source cut valid while readers use it.
- A **synchronized reader** is a worker proven to read the same cut as the coordinator, not merely one that starts at a nearby wall-clock time.
- A **partition plan** maps the full key domain into disjoint, exhaustive extraction ranges under fixed predicates and schema.
- A **fuzzy scan** is a multi-statement or multi-worker read without one proven source cut; it can be useful but is not transactionally consistent.
- A **logical export** serializes selected rows and metadata; a **physical backup/snapshot** captures database storage/recovery state. They have different portability and restore guarantees.
- A **snapshot manifest** identifies source cut, scope, schema, partitions, files, counts, digests, controls, and publication state for one generation.
- **source impact** includes I/O, CPU, cache displacement, locks, version/history retention, replica lag, network, and interference with maintenance or failover.
- **compatible-cut reconciliation** compares source and extracted evidence representing the same scope and source point.

### Central model, mechanism, or theorem

Let $R_c$ be all rows visible in extraction scope $R$ at source cut $c$. Let predicates $q_1,\ldots,q_n$ define worker partitions. A complete partitioned snapshot requires

$$
R_c=\biguplus_{i=1}^{n}\{r\in R_c\mid q_i(r)\},
$$

where $\biguplus$ means the sets are disjoint and their union is exhaustive. Every worker must evaluate its $q_i$ against the same cut $c$ and the same schema/filter/authorization context.

If workers use cuts $c_i$ independently, disjoint key ranges alone do not imply a possible database state: a transaction moving value or relationships across ranges can be observed partly before and partly after commit. The resulting union may equal no $R_c$.

Publication safety adds a second condition: trusted pointer $P$ changes from prior generation to new manifest $M_c$ only after every planned partition and snapshot-level invariant validates.

### Critical invariants

- Snapshot scope names databases/schemas/tables/views, columns, filters, tenants, row identity, exclusions, and metadata required for interpretation.
- Every exported partition resolves to one proven source cut, or the output is explicitly labeled fuzzy with bounded assurance.
- Partition predicates are total over the intended domain, mutually exclusive, stable during the cut, and represented in the manifest.
- Parallel workers do not start independent “repeatable” transactions and assume their snapshots match; they use an engine-supported synchronization/export facility or a source-native export job.
- Queries are read-only, bounded, deterministic, and free from unsafe volatile/external side effects under the extraction contract.
- Schema, collation, time zone, session settings, permissions, and serialization rules are fixed and recorded.
- Source load and version/history retention remain within pre-agreed limits; timeout or cancellation leaves the trusted destination unchanged.
- Every file is immutable and carries partition identity, row/byte counts, schema fingerprint, checksum, and source-cut lineage.
- Snapshot-wide keys, counts, relationships, control totals, and manifest completeness pass before atomic publication.
- Failed or partial generations remain unpublished and recover through replay/restart; no checkpoint or CDC handoff claims data beyond durable snapshot evidence.

### Common failures

Calling multiple `READ COMMITTED` statements a snapshot; launching independent transactions per chunk; recording only start time; using mutable or nullable partition keys; overlapping range endpoints; omitting empty planned partitions; chunking with `OFFSET` while rows move; running `COUNT(*)` at a different cut; reading replica partitions at different replay positions; allowing DDL midway; exporting volatile views or external tables without qualification; holding an unbounded MVCC snapshot; assuming nonblocking reads have no writer/maintenance cost; trusting a dump exit code without file manifests; truncating the destination first; treating equal row counts as equality; and starting change capture after the snapshot without an exact handoff position.

### Compact example

Four account rows total 100 at cut 10. At cut 11, one committed transaction moves five units from row 3 in the upper key range to row 2 in the lower range; total remains 100. A lower partition read at cut 10 plus upper partition read at cut 11 totals 95—a state that never existed. When both workers import cut 10, their disjoint ranges yield all four keys and total 100. The system verifies both partition receipts and controls, publishes one manifest, and makes replay idempotent.

### Connections

[DE-021](021-full-and-incremental-extraction.md) establishes full/incremental equivalence, [DE-022](022-watermarks-and-high-water-marks.md) defines source progress, [DE-023](023-file-arrival-and-manifest-processing.md) defines manifest publication, and [DE-024](024-api-based-ingestion.md) contrasts remote API cuts. [Database Engineering](../../18-database-engineering/ROADMAP.md) develops MVCC, isolation, backup, and replication; the next Data Engineering module develops database change capture.

## Governing Question

What observable evidence lets an operator say “these files represent this entire governed database scope at this exact source state” rather than “each query succeeded at some point during the export”?

Database snapshot extraction connects an online mutable system to an immutable analytical boundary. A full export may run for hours and issue thousands of statements. During that time applications continue to insert, update, and delete rows; schema deployments occur; replicas apply changes; maintenance reclaims obsolete versions; and worker failures cause retries.

The extractor must therefore separate four claims:

1. the database supplied one visibility cut;
2. the partition plan covered the intended logical scope exactly once;
3. serialization preserved the values and metadata needed downstream; and
4. all output became durable and trusted as one generation.

No single command name proves all four. `REPEATABLE READ`, `SNAPSHOT`, flashback, read concern, dump, backup, export, and consistent read have engine-, object-, session-, and version-specific meanings. The design must retrieve those meanings, encode them as premises, and test them under concurrent writes, DDL, failure, and resource pressure.

## Why This Matters

A fuzzy database scan can construct an impossible state. Suppose a committed transaction moves money between accounts, moves an order between statuses, or replaces a parent/child relationship. One chunk read before commit and another after commit can observe one side twice or neither side. Individual queries and file checksums remain valid while cross-row invariants fail.

Parallelism increases this risk. Separate sessions often acquire separate snapshots. Starting them within the same second is not synchronization. Even a transaction-level repeatable view is local to one session unless the engine provides snapshot export/import, an explicit read timestamp, or a coordinated export facility.

Consistency also affects schema. Rows read from one cut but decoded with changing column order, collation, time zone, generated expression, or enum/domain definition can be semantically inconsistent. Some databases version row data but restrict concurrent DDL or do not version all metadata. An extractor must freeze or capture the interpretive contract.

Long-lived snapshots are not free. MVCC engines preserve old row versions needed by active readers. This can grow undo/version stores, delay cleanup, increase table/index bloat, consume transaction IDs, lengthen recovery, or destabilize replicas. A nonblocking `SELECT` can still saturate disks, evict hot pages, consume CPU/network, and prolong lag.

Logical and physical extraction solve different problems. A logical export is selective and portable but pays parsing/serialization cost and may omit grants, sequences, large objects, extensions, or exact types unless specified. A physical storage snapshot can support disaster recovery with engine tooling but is not automatically queryable analytics data, crash-consistent across volumes, application-consistent, portable, or filtered.

Finally, publication must be atomic at the dataset level. Hundreds of correct files are not one trusted snapshot until their expected set, source cut, schema, counts, checksums, and controls reconcile. Consumers must never see an in-progress generation as complete.

## Prerequisites and Retrieval

Retrieve the source owner and workload criticality; engine/distribution/version; topology, primary/replicas/shards, failover, and replication positions; supported isolation levels and exact visibility semantics; snapshot export/import or read-timestamp facility; maximum snapshot/history retention; source log position paired with the snapshot; transaction boundaries; object scope; table/view definitions; primary and business keys; partitioning; row-level security and tenant scope; grants; schema/catalog visibility; DDL behavior; generated/virtual columns; triggers; sequences/identity values; large objects; external/foreign tables; materialized views; volatile functions; collations; character encodings; time zone/session settings; numeric/temporal precision; null/default semantics; binary formats; table size/change rate; indexes and query plans; I/O/CPU/network budgets; connection/concurrency limits; locks; version/undo store; vacuum/purge/garbage collection; replica lag and read consistency; export/compression/encryption; file size targets; object storage; snapshot manifest; source and output counts; control totals/digests; privacy/classification; credentials; audit; raw retention; restart behavior; publication transaction; rollback horizon; CDC handoff; recovery objectives; and maintenance/deployment windows.

Distinguish statement snapshot from transaction snapshot; transaction start from first snapshot acquisition; coordinator snapshot from independently started worker views; snapshot identifier from durable long-term bookmark; wall-clock from log/transaction position; primary cut from replica replay point; data visibility from metadata/DDL visibility; ordinary read from locking read; database state from external/foreign source state; logical export from physical backup; crash consistency from application consistency; storage-volume time from database commit cut; row identity from physical tuple/page location; key-range coverage from value-frequency balance; repeatable read from serializable execution; `COUNT(*)` at another time from snapshot control; exit success from semantic completeness; raw files from published generation; and snapshot completion from snapshot-to-change-stream continuity.

Before selecting tooling, create an evidence matrix:

| Concern | Required evidence |
|---|---|
| Source cut | Engine facility, cut identifier/position, acquisition event, validity horizon |
| Visibility | Isolation/read concern, transaction/session rules, primary/replica/shard scope |
| Logical scope | Objects, columns, predicates, tenant/security context, exclusions |
| Interpretation | Catalog/schema digest, types, collation, encoding, time zone, session settings |
| Partitioning | Stable key/domain, complete disjoint predicates, planned empty ranges, assignment |
| Impact | Estimated/scanned rows/bytes, plan, concurrency, duration, version-store/lag budgets |
| Output | Format, compression, file bounds, row identity, per-file counts/digests |
| Validation | Exact key/partition set, totals, relationships, domain controls, source comparison |
| Publication | Immutable manifest, conditional pointer/commit, prior generation and rollback |
| Continuity | CDC/log position, retention, handoff rule, failure/rebootstrap procedure |

## Learning Objectives

After completing this module, you should be able to:

1. distinguish transactionally consistent snapshots, fuzzy scans, logical exports, and physical backups;
2. translate engine isolation/read-timestamp facilities into an explicit source-cut contract;
3. synchronize parallel readers or explain why their views may differ;
4. design disjoint and exhaustive partition predicates over stable identity;
5. preserve schema, type, collation, encoding, time, and session semantics in serialization;
6. estimate and bound source I/O, concurrency, locks, version retention, and replica impact;
7. handle DDL, volatile views, external tables, large objects, sequences, and cross-database scope honestly;
8. stage, validate, manifest, and atomically publish a complete snapshot generation;
9. recover from worker, coordinator, storage, validation, and publication failures without partial trust; and
10. join the snapshot to later change capture at one retained source position.

## Core Exposition

### Define the logical snapshot scope

Start with consumer meaning, not `SELECT *`. Name included databases, schemas, tables, partitions, views, columns, row predicates, tenants, and record identities. Record intentionally excluded audit tables, transient rows, deleted subjects, historical partitions, binary objects, or privileged fields.

Decide whether the snapshot represents authoritative current state, a subset for one product purpose, or a physical recovery image. A complete export of an incorrectly filtered role is still incomplete for the intended dataset; a full physical backup may contain far more than policy permits in analytics.

For each object specify primary/business key, expected grain, types, null/default rules, generated fields, relationships, delete meaning, and canonical output. Include schema/catalog objects needed to interpret data: enums/domains, collation, time zone, sequences where relevant, and source engine/version.

### Name the source cut precisely

Represent the source cut as

$$
c=(e,d,s,p,t),
$$

where $e$ is engine/cluster identity, $d$ is database/shard scope, $s$ is engine snapshot or commit/log position, $p$ is primary/replica provenance, and $t$ is observed acquisition time. Wall-clock $t$ helps operations but does not replace $s$.

Record when the cut is actually acquired. Some systems establish it at transaction start; others at the first consistent read. Starting workers before the coordinator has materialized/exported the cut can produce ambiguity.

Snapshot identifiers may be valid only while a holder transaction remains open or while history is retained. They are coordination capabilities, not permanent replay positions. Persisting the identifier after expiry does not make the database able to serve it again.

### Choose the right visibility contract

`READ COMMITTED` commonly supplies a fresh statement-level view. A multi-query export can therefore see several source cuts. A transaction-level snapshot/repeatable-read facility can keep ordinary reads on one view, but exact anomalies, metadata behavior, and read/write interaction are engine-specific.

Serializable isolation is not automatically required for a read-only point-in-time export. A stable MVCC snapshot can reproduce committed state without proving that a hypothetical set of concurrent read/write operations is serializable. Conversely, a label `REPEATABLE READ` cannot be assumed identical across engines.

Use read-only mode where supported to prevent accidental effects and enable engine optimizations. Enforce SQL allowlists or a narrowly privileged extraction role; read-only transaction flags are defense in depth, not substitutes for permission control.

### Synchronize parallel PostgreSQL readers

PostgreSQL's current [snapshot synchronization documentation](https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION) explains that independently started transactions can see different contents and that an exporting transaction can share its snapshot while it remains open. A coordinator begins the required isolation, acquires and exports a snapshot, and stays open. Workers begin compatible transactions and import that identifier before their first query.

The PostgreSQL [SET TRANSACTION documentation](https://www.postgresql.org/docs/current/sql-set-transaction.html) specifies import constraints, including that `SET TRANSACTION SNAPSHOT` occurs at the beginning before the first query and uses `REPEATABLE READ` or `SERIALIZABLE` as applicable. Encode these ordering requirements in connector state and test a deliberately early worker query.

Keep the holder alive until every worker has successfully imported the snapshot; determine from engine behavior whether it must remain through all reads and choose the conservative documented lifecycle. If the holder disconnects before imports, fail the generation rather than letting workers silently start new views.

### Interpret other engine facilities locally

MySQL's [consistent nonlocking read documentation](https://docs.oracle.com/cd/E17952_01/mysql-8.4-en/innodb-consistent-read.html) describes InnoDB snapshot reads and distinguishes `REPEATABLE READ`, where consistent reads share the view established by the first such read, from `READ COMMITTED`, where each read gets a fresh view. It also documents DDL limitations. Do not infer PostgreSQL-style cross-session import from similar terminology.

Microsoft's [transaction locking and row versioning guide](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide?view=sql-server-ver17) distinguishes statement-level read consistency under read-committed snapshot from transaction-level `SNAPSHOT` and notes metadata restrictions. Confirm database options and multi-database behavior before design.

MongoDB's [snapshot read concern documentation](https://www.mongodb.com/docs/manual/reference/read-concern-snapshot/) describes majority-committed point-in-time reads across shards for supported operations, `atClusterTime`, and a bounded snapshot-history window. An extractor must finish or recover within that actual window.

Oracle Data Pump's [FLASHBACK_SCN documentation](https://docs.oracle.com/en/database/oracle/oracle-database/26/sutil/parameters-available-command-line-mode-export-oracle-data-pump.html#GUID-D408B112-1A81-4F68-BEFF-7403A9588DDB) defines an SCN-based consistent export. Confirm current product/version restrictions and object support rather than treating wall-clock start as the SCN.

These are calibration examples. The durable rule is to retrieve the exact engine/version contract and prove the connector exercises it.

### Separate logical export from physical backup

A logical export queries rows and serializes types into SQL, delimited text, JSON, Avro, Parquet, or a native logical dump. It supports selective scope, cross-version migration, and direct analytics, but can lose engine-specific type, constraint, sequence, privilege, collation, large-object, or extension semantics unless included.

A physical backup captures pages/files/logs needed by an engine to restore storage state. Filesystem, volume, or storage snapshots may need database quiescence, write barriers, coordinated multi-volume consistency, and transaction logs for crash recovery. They do not become safe logical tables merely by mounting them.

Use backup tooling for disaster recovery and migration when restore fidelity is the goal. Use logical extraction for governed data interchange. If both are required, maintain separate manifests and verification: a successful logical row comparison does not prove a physical restore, and a restorable backup does not prove the analytical projection.

### Acquire schema and data coherently

Capture the catalog/schema under a contract compatible with the data cut. Record object identifiers and qualified names, column order, type names/parameters, nullability, defaults, generated expressions, primary/unique/foreign keys, enum/domain values, collation, encoding, time zone, and view definition hashes.

Decide DDL policy: block/coordinate schema changes during extraction, use a source facility that versions metadata coherently, or detect catalog changes and fail/restart. Do not stitch old rows to a new schema because parsing still succeeds.

Some DDL invalidates a snapshot or changes physical objects. Some metadata is not row-versioned. Test rename, add/drop column, type change, index rebuild, partition attach/detach, view replacement, and table replacement under the selected engine/tool.

### Avoid volatile and external surprises

Views may call current time, random/sequence functions, session settings, remote services, security-definer functions, or mutable configuration. Multiple evaluation can produce values that never belonged to the source row cut.

Foreign/external tables and federated queries can read systems with independent clocks and transactions. A database snapshot generally cannot freeze those external sources. Either materialize them into the same governed cut, acquire coordinated source-native snapshots, or label them as separately observed inputs.

Generated columns can be stored or evaluated on read. Record which. Prefer exporting authoritative base fields plus the agreed generated value when reproducibility requires both; validate definitions and avoid unintended side effects.

### Design a complete partition plan

Partition to bound query time, output size, retries, and parallelism. Candidate strategies include primary-key ranges, source partitions, time partitions under stable membership, hash buckets over immutable keys, or engine-native parallel export segments.

Write the predicates before reading. For ordered non-null unique key $k$, half-open ranges

$$
[b_0,b_1),[b_1,b_2),\ldots,[b_{n-1},b_n)
$$

avoid boundary overlap, with explicit unbounded endpoints or minimum/maximum coverage. If null is possible, allocate a separate `IS NULL` partition. If keys can mutate, the fixed snapshot still stabilizes membership, but restart outside that cut needs a new generation.

For hash partitioning, define canonical key bytes, hash algorithm/version, signedness, modulo, and null behavior. Database and client hashes may differ by version/collation. Compute predicates in the source using a documented stable expression and test every key against exactly one bucket.

### Prove partition disjointness and exhaustiveness

For predicates $q_i$, require

$$
\forall r\in R_c:\sum_{i=1}^{n}\mathbf{1}[q_i(r)]=1.
$$

A sum of zero means an omitted row; greater than one means overlap. The manifest lists every planned partition, including an empty partition with zero rows. Missing output cannot be confused with valid emptiness.

Validate range endpoints, types, collation, and predicate text/fingerprint. Compare the union's exact keys or partitioned key digests to a control read at the same cut. A total row count alone can hide one missing and one duplicate row.

Do not use `OFFSET` to define worker ownership. It binds to positional results and can be inefficient; without one stable total order/cut it can drift. Keyset/range predicates express ownership independently.

### Balance partitions without changing coverage

Equal numeric ranges can be badly skewed. Use source statistics only as planning hints, sample under bounded load, or recursively split oversized ranges. Preserve parent-to-child coverage evidence so dynamic splitting cannot introduce gaps.

Never change the partition plan silently after some outputs commit. Version the plan and record superseded attempts. A worker split of `[a,z)` into `[a,m)` and `[m,z)` is safe only if the parent is unpublished, both children use the same cut, and endpoints use the same comparator.

Cap rows, bytes, execution time, and response buffering. A single giant row or hot key range may still exceed bounds; quarantine/handle large objects through explicit policy rather than skipping them.

### Keep every reader on the same cut

Worker metadata should include generation, coordinator/holder identity, source cut, imported/read timestamp, database node, schema fingerprint, partition ID/predicate, session settings, start/end time, attempts, and result receipt.

After connection pooling or failover, prove the transaction and cut remain active. A driver reconnect that transparently starts a new session invalidates the worker. Treat it as partition failure and restart the entire cut or use a source-native job whose snapshot survives clients.

Do not mix primary and replica reads unless a distributed facility guarantees the same cut and each replica has reached it. “Replica lag under one second” is not equality. Pin node/epoch and replay position; failover can change history availability and session state.

### Extract deterministically

Select explicit columns in deterministic order. Qualify tables and avoid dependence on search path. Set and record time zone, date style, numeric/locale formatting, collation behavior, character encoding, floating-point representation, null encoding, binary encoding, and statement timeout.

Use a stable row order within each output when deterministic files/digests are valuable. SQL result order is unspecified without `ORDER BY`. Align order and predicates with indexes where possible, but do not expose physical row addresses as durable identity.

PostgreSQL's [COPY documentation](https://www.postgresql.org/docs/current/sql-copy.html) supports exporting a table or query result. COPY improves transfer efficiency but inherits the transaction's visibility and the selected serialization options; it does not create a multi-session snapshot by itself.

### Preserve type fidelity

Map exact integers/decimals without binary-float coercion; retain decimal precision/scale and reject overflow. Preserve timestamp type, zone/offset, precision, and source text where needed. Distinguish database date/time/infinity/sentinel values from application nulls.

Define text encoding, normalization, collation identity, trailing spaces, fixed versus variable strings, and binary/blob representation. JSON/XML/spatial/array/range/vendor types need versioned conversions with fixtures and loss checks.

Record whether defaults/generated values were materialized. Missing fields do not exist in relational rows the same way as JSON; null, default, empty, and unavailable must not collapse.

### Handle relationships and transaction boundaries

A transactionally consistent cut makes each included table visible at the same committed point under the facility's scope. This enables meaningful referential and control checks, but only for included objects and constraints actually enforced at that cut.

Export parent and child tables independently for throughput, then validate relationships after all partitions land. Do not reject a child merely because its parent file has not arrived yet. Deferrable constraints, soft deletes, filtered scope, historical facts, and intentionally orphaned source data need explicit rules.

If the source transaction atomically updates several databases or external systems without a common snapshot facility, one database cut cannot prove global application consistency. Capture transaction/event coordination evidence or label the boundary.

### Capture sequences, identities, and auxiliary state

Current row state may not include future identity allocation. If the snapshot is intended for operational restore/migration, capture sequences/identity generators at a compatible point and define safe restoration relative to maximum values. For analytics, sequence state may be irrelevant and should be omitted deliberately.

Similarly decide on grants, owners, policies, triggers, procedures, indexes, statistics, large objects, materialized views, and extension configuration. “Database snapshot” without an object inventory is ambiguous.

Never execute dumped code automatically in an untrusted environment. Logical dump files can contain DDL, functions, paths, or ownership commands; review and restore under least privilege.

### Bound source impact

Estimate rows, bytes, query plans, index scans, CPU, I/O, cache effects, version retention, network, and duration before production. Coordinate maintenance windows and define abort thresholds with source owners.

Use read-only credentials, statement/transaction timeouts, bounded connections, fetch sizes, compression, and adaptive but capped parallelism. A read replica reduces primary query load only if its lag, snapshot support, capacity, failover, and retention satisfy the cut. It can still be overloaded or fall behind.

Long MVCC snapshots can hold back cleanup. PostgreSQL's [routine vacuuming documentation](https://www.postgresql.org/docs/current/routine-vacuuming.html) describes MVCC cleanup/freeze concerns; the exact effect of an active extraction must be monitored in the deployed engine. MySQL undo, SQL Server version store, and MongoDB snapshot history have different controls.

Measure goodput, not just worker count. More readers may contend on the same disks, evict application pages, expand versions, saturate network, and increase retries. Pause or abort safely before source health violates its SLO.

### Plan snapshot duration and history

Let expected bytes be $B$, sustainable end-to-end throughput $g>0$, startup/validation time $a$, and contingency factor $f>1$. A simple duration budget is

$$
T_{budget}=f\left(a+\frac{B}{g}\right).
$$

Require the source snapshot/history facility, credential, network, and output reservation to remain valid beyond $T_{budget}$ with operational margin. This is planning arithmetic, not a performance guarantee; skew, compression, query plans, throttling, and failures change $g$.

If the feasible duration exceeds safe version retention, do not merely increase timeouts. Use a native export/backup, smaller independently consistent source partitions, a snapshot-to-CDC bootstrap, a restored replica/clone, or a maintenance-coordinated cut.

### Stage immutable outputs

Write each partition to a generation/attempt-scoped immutable path. Close the stream, verify byte length and checksum, then write a partition receipt. Never let object existence alone mean success.

Partition metadata includes planned predicate, source cut, schema fingerprint, worker/attempt, row/byte count, key min/max, null counts, control sums, file format/compression, object version, and digest. Separate potentially sensitive statistics from broadly readable manifests.

On retry, reuse the logical partition identity but create a new attempt object or conditionally reuse identical content. If two successful attempts differ under the same cut and contract, fail closed; nondeterministic serialization or source inconsistency needs diagnosis.

### Validate at partition and snapshot levels

Per partition, validate schema, parseability, record count, key uniqueness/range, ordering if declared, type bounds, checksums, and domain controls. Across partitions, validate every planned ID appears once, object identities are immutable, predicates are nonoverlapping/exhaustive, keys are unique, and schema/source cut match.

Recompute snapshot totals from partition receipts. Check exact key sets/digests where feasible, source-declared counts, monetary/quantity conservation, parent-child relationships, min/max continuity, null distributions, and application invariants.

Run source controls at the same cut. A `COUNT(*)` after the holder commits observes another state and cannot prove the old export. Have the coordinator compute controls within the shared snapshot or use a source-native export manifest.

### Publish one snapshot generation

Create a DE-023-style immutable manifest only after all planned partitions and snapshot controls pass. The manifest names source cut/engine/node, logical scope, schema, partition plan, files, totals, controls, extractor/tool versions, validation, and any explicit limitations.

Atomically or conditionally update a small trusted pointer/catalog entry from prior generation to the new manifest. Consumers resolve only published manifests. Keep the prior generation through rollback and reconciliation horizons.

Never truncate or overwrite the trusted destination before new validation. A failed generation remains staged/unpublished with retention and cleanup policy. Corrections create a superseding generation; they do not rewrite forensic evidence.

### Recover from failure deliberately

If a worker fails while the shared source cut remains valid, retry its exact partition under that cut and record a new attempt. If the holder, transaction, read timestamp, schema contract, or history expires, fail the generation and acquire a new cut; do not combine old successful files with new-cut retries.

If output storage fails after source read, retry under the same cut if possible. If a partition receipt exists, validate and reuse it. If manifest publication fails, reconstruct from receipts and conditionally publish the same manifest. If pointer update succeeds but response is lost, read the pointer/receipt before retry.

Cancellation closes all transactions promptly, revokes leases, and leaves no publication. Cleanup does not delete evidence still needed for diagnosis, replay, audit, or privacy workflow.

### Join snapshot to change capture

For ongoing replication, pair the snapshot with an engine-native log/change position $l_c$. Changes during the long scan must remain retained. The downstream state becomes the baseline at $c$ plus every committed change after the agreed position, with a documented overlap boundary.

Starting CDC after the scan creates a gap. Applying CDC before baseline publication can let older snapshot rows overwrite newer changes. Buffer/land changes, publish the baseline, then apply source-ordered changes strictly after the cut or use version-aware idempotent overlap.

DE-026 develops capture mechanics. DE-025's obligation is to produce both a valid baseline manifest and the exact source position/contract needed for handoff.

### Reconcile and rehearse restore

For logical extraction, compare compatible-cut exact key sets, partition digests, row counts, control sums, and semantic samples. For physical backups, perform isolated restore drills, engine recovery, consistency checks, object inventory, and recovery-time/recovery-point measurement.

Validation should be independent of the extractor path where possible. If the same partition predicate bug produces files and expected counts, it can bless its own omission. Use source-native counts, alternative key bucketing, constraints, business ledgers, or later snapshot comparison.

Record evidence limitations. Matching keys and selected fields at one cut does not prove omitted columns, external systems, historical changes, future runs, or physical restorability.

### Secure the extraction boundary

Use a least-privilege read-only account scoped to approved objects/rows, strong transport authentication/encryption, controlled egress, secret rotation, and query auditing. Separate snapshot coordination privileges from broad administrative or filesystem rights.

Database roles can change visibility. Pin/record role, tenant/session claims, row-level security, and policy revision. A role rotation halfway through parallel work requires failure/restart unless identical scope is proven.

Encrypt staging and manifests as classification requires; restrict sensitive counts/key ranges; scan output/logs for secrets; apply retention and subject deletion. Avoid exporting password hashes, keys, tokens, or operational secrets merely because the database account can read them.

Native dump formats and SQL scripts are active/untrusted input during restore. Restore in isolation with allowlisted extensions/paths/owners, no uncontrolled network, and reviewed code execution.

### Observe and test the protocol

Monitor source cut age, holder/worker sessions, imported-cut acknowledgements, query/partition duration, rows/bytes, plan changes, I/O/CPU/cache, locks, version/undo store, vacuum/purge, replica lag, CDC retention headroom, output throughput, retries, file checks, validation drift, publication, and cleanup.

Inject concurrent cross-partition transactions, same-key updates, deletes, schema changes, holder loss, worker reconnect, replica failover, timeouts, disk/network failure, corrupt/truncated output, duplicate attempts, missing/extra partition, manifest/pointer response loss, and CDC handoff lag.

The decisive test is not that the dump exits zero. It is that every failure either yields one fully validated published generation at one cut or leaves the prior trusted generation unchanged with enough evidence to recover.

## Definitions and Notation

Let:

- $c$ be the engine-specific source cut;
- $R_c$ be all in-scope rows visible at $c$;
- $q_i$ be the predicate for planned partition $i$;
- $R_{c,i}=\{r\in R_c\mid q_i(r)\}$ be that partition's rows;
- $K(r)$ be stable logical row identity;
- $\sigma_c$ be the captured schema/interpretation contract at $c$;
- $F_i$ be the immutable output/receipt for partition $i$;
- $M_c$ be the validated snapshot manifest;
- $P$ be the trusted published-generation pointer;
- $l_c$ be the source log/change position coordinated with $c$;
- $B$ be estimated source bytes, $g$ sustainable goodput, $a$ fixed time, and $f$ contingency factor.

Exact partition coverage requires

$$
R_c=\biguplus_{i=1}^{n}R_{c,i}
$$

or equivalently

$$
\forall r\in R_c:\sum_{i=1}^{n}\mathbf{1}[q_i(r)]=1.
$$

Snapshot integrity requires every $F_i$ to name the same $(c,\sigma_c)$, to match its planned $q_i$, and to pass per-file controls. Snapshot publication is a transition

$$
P:M_{old}\rightarrow M_c
$$

only after the complete expected file/partition set and snapshot-level controls validate.

A duration planning estimate is

$$
T_{budget}=f\left(a+\frac{B}{g}\right),\qquad g>0,\ f>1.
$$

Define fuzzy union $U=\bigcup_i R_{c_i,i}$ when workers use independent cuts. Even if predicates are disjoint in key space, $U$ need not equal $R_c$ for any $c$ because transactions can move values/relationships across partitions.

## Mechanisms, Invariants, or Proof Structure

**Single-cut invariant.** Every included row, source control, and schema interpretation resolves to the same documented $c$ within the facility's supported scope. A separately observed replica time or wall-clock timestamp is not substitution evidence.

**Partition theorem.** If all $q_i$ evaluate over one fixed $R_c$, every row satisfies exactly one predicate, and each worker exports all rows satisfying its predicate, then the disjoint union of worker outputs equals $R_c$.

**Proof.** For any $r\in R_c$, the indicator condition assigns it to one partition, proving union coverage and excluding duplication. Every exported row is required to belong to $R_c$ and its predicate, so no out-of-scope row enters. Equality follows by both inclusions.

**Independent-cut counterexample.** Let cut 10 contain values `(2,20)` and `(3,30)`. One transaction at cut 11 changes them to `(2,25)` and `(3,25)`, conserving their sum. Reading lower keys at cut 10 and upper keys at cut 11 yields 20+25 rather than 50 for those rows, so the union represents neither committed cut.

**Schema-coherence invariant.** Every output identifies the same schema/serialization fingerprint $\sigma_c$. A DDL/policy/session change that alters interpretation invalidates the generation unless the engine/export contract proves compatible versioning.

**Holder-liveness condition.** When snapshot validity depends on a coordinator transaction or retained history, every reader imports/uses the cut within that lifetime. Loss/expiry forces a new generation, not a new-cut retry of one partition.

**Immutable-attempt invariant.** A logical partition can have multiple attempts, but each object is immutable and content-addressed/versioned. Only one validated receipt per partition enters $M_c$; differing successful contents under identical $(c,\sigma_c,q_i)$ trigger investigation.

**Publication invariant.** $P$ never references a manifest with missing, extra, duplicate, corrupt, wrong-cut, wrong-schema, or failed-control partitions. Before pointer change, consumers retain $M_{old}$.

**Source-impact invariant.** Connections, query time, transaction age, I/O, version/history pressure, replica lag, and CDC retention remain within named abort thresholds. Snapshot consistency does not authorize unbounded source harm.

**Handoff invariant.** Snapshot $M_c$ and captured change position $l_c$ refer to one coordinated boundary; subsequent current state applies all required committed changes after that boundary once by effect.

**Evidence boundary.** Passing exact keys/counts/digests proves only the captured scope/fields under their canonicalization and cut. Restore success, external-source consistency, omitted metadata, historical completeness, and future extraction correctness require separate evidence.

<!-- bijux-verify: {"id":"shared-snapshot-partition-publication","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"snapshot_rows=4\nsnapshot_total=100\npartitions_disjoint=True\npartitions_complete=True\nmixed_total=95\nmixed_snapshot_possible=False\nmanifest_partitions=2\nduplicate_partition_idempotent=True\npublished_after_validation=True\nfailed_validation_not_published=True\n","stderr":""}} -->
```python
states = {
    10: {1: 10, 2: 20, 3: 30, 4: 40},
    11: {1: 10, 2: 25, 3: 25, 4: 40},
}

def read_partition(cut, lower, upper):
    return {
        key: value
        for key, value in states[cut].items()
        if lower <= key < upper
    }

lower = read_partition(10, 1, 3)
upper = read_partition(10, 3, 5)
snapshot = dict(lower)
snapshot.update(upper)

lower_keys = set(lower)
upper_keys = set(upper)
all_keys = lower_keys | upper_keys
mixed = dict(lower)
mixed.update(read_partition(11, 3, 5))

receipts = {}
for partition_id, rows in (("lower", lower), ("upper", upper)):
    receipts.setdefault(partition_id, tuple(sorted(rows.items())))
first_lower = receipts["lower"]
receipts.setdefault("lower", ((1, 999),))

expected_partitions = {"lower", "upper"}
valid = (
    set(receipts) == expected_partitions
    and all_keys == set(states[10])
    and not (lower_keys & upper_keys)
    and sum(snapshot.values()) == 100
)
published = "snapshot-10" if valid else None
failed_published = "snapshot-bad" if set(receipts) == {"lower"} else None

print(f"snapshot_rows={len(snapshot)}")
print(f"snapshot_total={sum(snapshot.values())}")
print(f"partitions_disjoint={not bool(lower_keys & upper_keys)}")
print(f"partitions_complete={all_keys == set(states[10])}")
print(f"mixed_total={sum(mixed.values())}")
print(f"mixed_snapshot_possible={sum(mixed.values()) in {sum(s.values()) for s in states.values()}}")
print(f"manifest_partitions={len(receipts)}")
print(f"duplicate_partition_idempotent={receipts['lower'] == first_lower}")
print(f"published_after_validation={published == 'snapshot-10'}")
print(f"failed_validation_not_published={failed_published is None}")
```

The finite execution demonstrates a four-row model with two cuts and in-memory receipts. It does not prove any engine's snapshot, transaction, schema, storage, resource, security, or durability behavior.

## Alternatives and Trade-Offs

**Logical export versus physical backup.** Logical output is selective and portable but may lose engine features and costs serialization. Physical backup preserves engine storage/recovery semantics but needs engine restore tooling and may overcapture sensitive data.

**Primary versus replica.** Primary offers authoritative current progress but shares production resources. Replica offloads reads but adds lag, retention, failover, and read-position constraints; it needs a proven cut, not “close enough.”

**One transaction versus synchronized workers.** One transaction is simple and inherently one view but may underuse capacity and run long. Synchronized readers improve throughput but require exact snapshot sharing, coordination, and more source pressure.

**Source-native export versus custom queries.** Native export can coordinate snapshot, schema, parallelism, and metadata robustly. Custom queries offer precise projection and output formats but make cut/partition/recovery correctness the pipeline's responsibility.

**Range versus hash partitions.** Ranges support ordered files, pruning, and explainable boundaries but skew with clustered keys. Hash buckets balance irregular keys but require stable canonical hashing and reduce range locality.

**Static versus adaptive splitting.** Static plans are reproducible and easy to audit. Adaptive splitting handles skew but needs parent/child lineage and immutable coverage under the same cut.

**Repeatable/snapshot versus serializable read-only.** A repeatable point-in-time view is often sufficient and cheaper. Serializable read-only modes can add anomaly protection or safe-snapshot waiting in some engines, but semantics/costs are product-specific.

**Short chunks at separate cuts versus long shared cut.** Separate cuts reduce version retention but produce fuzzy state. One long cut provides consistency but may harm cleanup. Use native snapshots/clones or CDC bootstrap when the trade-off is infeasible.

**Rows versus query-derived views.** Base rows preserve source facts and allow re-derivation. Views centralize business semantics but can be volatile, security-sensitive, expensive, or dependent on external state.

**Text versus binary/native output.** Text is inspectable and portable but needs precise escaping/locale/type mapping. Binary/native paths preserve more fidelity and throughput but couple readers to versions and toolchains.

**One file versus bounded files.** One file simplifies consumption but limits retry/parallelism and may exceed object/reader constraints. Partition files improve scalability but require manifest-level atomicity.

**Fail generation versus partial publication.** Full failure protects snapshot semantics. Partial availability may be valid only for independently complete, explicitly versioned partitions whose consumers understand absence; never silently weaken a global snapshot.

**Source controls versus downstream-only checks.** Source controls at the shared cut are stronger for completeness. Downstream controls are essential but can repeat extractor defects. Combine independent paths.

**Rebuild versus resume.** Resume under the still-valid same cut saves work. Once cut/schema validity is lost, rebuilding a new generation is safer than mixing histories.

## Failure Modes and Misconceptions

- **“Full scan means snapshot.”** Multiple statements can see multiple committed states.
- **“Transactions started together share a snapshot.”** Independent sessions generally need explicit synchronization.
- **“Transaction start time is the cut.”** Some engines acquire a view at the first read.
- **“Wall-clock identifies the database state.”** Commit/log/snapshot coordinates are stronger.
- **“Repeatable read means the same thing everywhere.”** Engine semantics differ.
- **“Serializable is always the strongest export choice.”** It may add cost without changing read-only snapshot needs.
- **“Read-only means no production impact.”** Reads consume I/O, CPU, cache, network, and versions.
- **“MVCC never blocks writers.”** Metadata locks, schema operations, storage pressure, and engine details still matter.
- **“A replica is an exact copy now.”** Lag and failover create distinct replay positions.
- **“All replicas at low lag are one cut.”** Similar time is not identical position.
- **“Parallel workers are only a performance choice.”** They change snapshot coordination and source load.
- **“Key ranges cannot overlap.”** Endpoint inclusivity and null/collation errors commonly overlap or gap.
- **“Min/max covers the domain.”** Sparse, negative, composite, null, and new keys need explicit semantics.
- **“OFFSET divides a table.”** It divides a result position under one execution, not durable ownership.
- **“Physical row ID is a stable key.”** Maintenance and rewrites can change it.
- **“Equal ranges balance work.”** Data and row widths are skewed.
- **“Missing file means empty partition.”** Empty requires an explicit successful receipt.
- **“Counts add up, so rows match.”** Missing and duplicate keys can cancel.
- **“COUNT at the end validates the start cut.”** It observes another state unless tied to the snapshot.
- **“Checksums prove source completeness.”** They prove captured bytes against a trusted value.
- **“Schema is just column names.”** Types, defaults, collation, time zone, and generated meaning matter.
- **“MVCC versions all metadata.”** DDL/catalog behavior is engine-specific.
- **“A view is frozen by the row snapshot.”** Volatile and external dependencies may not be.
- **“Foreign tables join the database snapshot.”** Their remote source may have a different cut.
- **“COPY creates consistency.”** It transfers data under existing transaction semantics.
- **“Dump exit zero means complete.”** Scope, files, controls, and publication still require evidence.
- **“Physical volume snapshot is application-consistent.”** It may be only crash-consistent or inconsistent across volumes.
- **“Logical dump is a full backup.”** It may omit operational objects and restore fidelity.
- **“Keep the snapshot open until done, no matter how long.”** History pressure can endanger the source.
- **“Reconnect and retry one chunk.”** A new session may use a new cut.
- **“DDL error can be retried locally.”** Other partitions may still embody the old schema.
- **“Truncate then load is replacement.”** Failure exposes empty/partial trusted state.
- **“Publish files as they finish.”** Consumers can combine incomplete partitions.
- **“Snapshot alone starts CDC safely.”** The exact change position/handoff is required.
- **“Matching one restored sample proves backup.”** Restore scope and recovery objectives need rehearsal.
- **“Read access authorizes every column.”** Data minimization and purpose still apply.

## Worked Examples

### Example 1

A customer export runs 50 queries under default `READ COMMITTED`. A customer moves from segment A to B between the A and B queries and appears in both output files.

The team acquires a transaction-level read cut and evaluates all segment predicates within it. The old fuzzy output is labeled invalid and never published. **Conclusion:** repeatable visibility is a dataset property, not a query-success property.

### Example 2

Eight PostgreSQL workers each begin `REPEATABLE READ` independently. A payment transaction commits between worker starts, so some files see it and others do not.

A coordinator materializes/exports one snapshot, workers import it before any query, and receipts record the same identifier. Loss of the holder before import aborts the generation. **Conclusion:** identical isolation labels do not synchronize sessions.

### Example 3

Ranges are defined as `id >= 0 AND id <= 100` and `id >= 100 AND id <= 200`. Key 100 appears twice, while null IDs appear nowhere.

The plan uses half-open `[0,100)`, `[100,201)` plus an explicit null partition if null is in scope. Snapshot validation proves every exact key appears once. **Conclusion:** endpoint and null semantics are part of coverage.

### Example 4

An export reads a lagging replica and records only wall-clock 02:00. Failover midway reconnects workers to a newer replica. Files now contain different replay positions.

The connector pins replica/node epoch and source cut; transparent reconnect fails the generation. A new cut and manifest are acquired after failover. **Conclusion:** topology provenance belongs in snapshot identity.

### Example 5

A deployment adds a non-null column with a default while half the table is already exported. Old files omit it; new files contain it, and downstream fills omission inconsistently.

The schema fingerprint mismatch blocks publication. The team coordinates DDL, acquires a new cut/schema, and reruns every partition. **Conclusion:** successful row reads under mixed schema do not form one snapshot contract.

### Example 6

A six-hour MVCC scan does not block application updates, but obsolete versions grow rapidly, vacuum/purge falls behind, and storage latency threatens production.

Source owners set transaction-age and version-store abort thresholds, reduce projection/bytes, use a restored clone/native export, and capture CDC for continuity. **Conclusion:** nonblocking is not zero-impact.

### Example 7

A view includes `current_timestamp` and a remote exchange-rate table. Each partition has a different extraction time and remote state even though base database rows share one snapshot.

The design materializes one governed rate cut, supplies a fixed as-of parameter, or exports base facts and rates separately with explicit lineage. **Conclusion:** a database row snapshot does not freeze volatile/external computation.

### Example 8

All 32 partition files exist and sum to the source row count, but partition 17 is a retry from a later cut and partition 18 is missing one key offset by a duplicate in partition 19.

The manifest validator checks source cut, schema, planned IDs, exact key bucket digests, and uniqueness—not counts alone—and rejects the generation. **Conclusion:** plausible totals can mask mixed history and identity defects.

### Example 9

A pipeline truncates the serving table and streams snapshot rows directly. The source snapshot expires at 70%, leaving consumers with partial current state.

The replacement writes immutable staged files, validates a manifest, builds a new versioned destination, and conditionally swaps the serving pointer. The prior generation remains trusted. **Conclusion:** extraction completion and publication must be separate.

### Example 10

A baseline snapshot finishes at log position 8,000, but CDC starts only afterward at 8,500. Changes 8,001–8,499 are absent from both inputs.

The corrected source-native protocol captures snapshot cut and log position together, retains changes during the scan, then applies all changes after the boundary idempotently. **Conclusion:** a valid snapshot is necessary but insufficient for ongoing continuity.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md): MVCC visibility, isolation, transactions, logs, replication, vacuum/version stores, backup, restore, and DDL supply source guarantees.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): system-of-record scope, data contracts, lineage, retention, and privacy define what belongs in the snapshot.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): partition planning, skew, parallel I/O, backpressure, manifests, and replay determine scale.
- [Operating Systems](../../22-operating-systems/ROADMAP.md): filesystem durability, process failure, virtual memory/cache, clocks, and storage snapshots affect observed behavior.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): least privilege, transport security, dump-file handling, secret exclusion, and restore isolation constrain extraction.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): consistent cuts, partial failure, leases, idempotence, replication lag, and atomic publication explain the protocol.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): asynchronous export APIs, compatibility, error handling, and quotas may wrap database snapshot facilities.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): connector runtimes, credential delivery, clone services, observability, policy, and recovery workflows operationalize snapshots.

## References

1. PostgreSQL Global Development Group, [Snapshot Synchronization Functions](https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION). Documents snapshot export/import, identical cross-session visibility, exporter lifetime, and coordination limits.
2. PostgreSQL Global Development Group, [SET TRANSACTION](https://www.postgresql.org/docs/current/sql-set-transaction.html). Documents isolation/read-only modes and requirements for importing an exported snapshot before the first statement.
3. PostgreSQL Global Development Group, [COPY](https://www.postgresql.org/docs/current/sql-copy.html). Documents bulk transfer of tables or query results and serialization options.
4. PostgreSQL Global Development Group, [Routine Vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html). Documents MVCC cleanup/freeze responsibilities relevant to monitoring long-running source activity.
5. Oracle, [MySQL 8.4 Consistent Nonlocking Reads](https://docs.oracle.com/cd/E17952_01/mysql-8.4-en/innodb-consistent-read.html). Documents InnoDB read views under `REPEATABLE READ` and `READ COMMITTED` plus DDL limitations.
6. Microsoft, [Transaction Locking and Row Versioning Guide](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide?view=sql-server-ver17). Distinguishes statement-level read-committed row versioning from transaction-level snapshot behavior and records metadata restrictions.
7. MongoDB, [Read Concern `snapshot`](https://www.mongodb.com/docs/manual/reference/read-concern-snapshot/). Documents majority-committed point-in-time reads, `atClusterTime`, supported operations, and bounded snapshot history.
8. Oracle, [Data Pump Export `FLASHBACK_SCN`](https://docs.oracle.com/en/database/oracle/oracle-database/26/sutil/parameters-available-command-line-mode-export-oracle-data-pump.html#GUID-D408B112-1A81-4F68-BEFF-7403A9588DDB). Documents SCN-based consistent export behavior and restrictions.

## Exercises

### Exercise 1

Design a parallel logical snapshot of `customers`, `orders`, and `order_lines` from an MVCC database. Include cut acquisition, schema capture, partition predicates, worker lifecycle, source-impact limits, output receipts, cross-table validation, publication, and failure recovery.

### Exercise 2

At cut 20, lower-range account balances are `{1:40,2:60}` and upper-range balances `{3:70,4:30}`. One transaction at cut 21 transfers 10 from account 2 to account 3. Show the totals for lower@20 plus upper@21 and lower@21 plus upper@20. Explain why disjoint keys do not repair independent cuts.

### Exercise 3

A 12 TB source can sustain 250 MB/s of extraction without SLO harm. Startup/validation takes 30 minutes, contingency factor is 1.5, and the database's safe snapshot/history window is 16 hours. Recompute the planning duration and decide whether the plan is feasible before accounting for skew and failures.

### Exercise 4

Review a physical cloud-volume snapshot proposal spanning database data, transaction log, and key-management volumes. Distinguish crash consistency, database/application consistency, encryption/key availability, restore evidence, and suitability as an analytical logical extract.

### Exercise 5

Design failure-injection tests for snapshot holder loss, one worker reconnecting to another replica, DDL during export, skew-driven dynamic splitting, output corruption, duplicate partition success with different bytes, missing empty partition, manifest publication response loss, and CDC retention exhaustion.

## Answers to the Exercises

### Answer 1

Define one database/tenant/object scope and capture qualified table definitions, columns/types/null/default/generated rules, keys/relationships, collation, encoding, time zone, and a schema fingerprint. Begin a read-only transaction-level snapshot using the engine facility, materialize/export its cut, record the coordinated log position, and retain the holder as required.

Partition `customers` and `orders` by disjoint half-open stable primary-key ranges or a versioned hash. Partition `order_lines` by its own stable key or by order ranges with explicit coverage; never assume parent and child numeric domains align. List every planned partition, including empty results. Each worker imports the cut before any query, applies fixed session settings and schema, exports explicit columns deterministically, and writes an immutable file plus cut/schema/predicate/count/bytes/key bounds/digest receipt.

Limit connections, statement/transaction age, I/O, version-store/undo pressure, replica lag, network, and CDC retention headroom with source-owner abort thresholds. Across receipts verify expected partitions exactly once, source cut/schema equality, exact key uniqueness/coverage, counts/control totals, and customer–order–line relationships under declared filters. Publish one manifest and conditionally swap the trusted pointer only after validation. Retry a failed partition only while the same cut remains valid; holder loss, schema change, or history expiry abandons the generation and starts a new cut. Preserve old trusted generation and buffered changes for rollback/handoff.

### Answer 2

At cut 20, lower totals $40+60=100$ and upper totals $70+30=100$, so database total is 200. At cut 21, account 2 is 50 and account 3 is 80; each range is still 90 and 110 respectively, and total remains 200.

Lower@20 plus upper@21 is $100+110=210$, double-observing the transferred 10. Lower@21 plus upper@20 is $90+100=190$, observing neither side. The key predicates remain disjoint and exhaustive over identities, but value/relationship state crosses the cut atomically. Only evaluating all predicates over the same $R_c$ preserves transaction consistency.

### Answer 3

Using decimal units, 12 TB is 12,000,000 MB. Transfer time is $12{,}000{,}000/250=48{,}000$ seconds, or 800 minutes (13 hours 20 minutes). Adding 30 minutes yields 830 minutes. Applying factor 1.5 gives 1,245 minutes, or 20 hours 45 minutes.

That exceeds the 16-hour safe history window by 4 hours 45 minutes before skew, retries, compression behavior, validation variability, or source incidents. The plan is infeasible under its premises. Do not raise the timeout and hope. Use an engine-native snapshot/export or restored clone, reduce bytes/projection, create independently consistent source partitions, increase approved sustainable goodput only with measurement, or coordinate snapshot plus CDC so the baseline does not depend on one 12 TB live transaction.

### Answer 4

A simultaneous-looking storage snapshot may capture each volume at different instants; database pages/logs can require crash recovery, and key material may not correspond. Establish whether the cloud group snapshot supplies write-order and cross-volume atomicity, whether the database was quiesced or has a supported backup protocol, and whether logs cover recovery to one cut. That is crash/database consistency evidence, not application consistency across other databases/services.

Record engine/version/configuration, volume set, snapshot IDs/times/order, database checkpoint/log position, quiesce/barrier commands, encryption key versions and restore authorization. Never snapshot key material broadly merely for convenience; test that governed key access survives disaster. Restore into isolated infrastructure, run engine recovery/consistency checks, inventory objects, validate application controls, measure RPO/RTO, and repeat after topology/engine changes.

The result remains a physical recovery artifact. It is not a safe analytical logical extract until restored through trusted engine tooling and projected with explicit schema, row/column/security scope, type conversion, validation, and publication. Conversely, a logical row export cannot replace the physical recovery drill.

### Answer 5

For holder loss before imports, workers must fail and no output publish; after imports, behavior follows documented engine lifetime and a forced reconnect must never silently acquire a new cut. Pin node/epoch/position so a worker moved to another replica is rejected. Inject add/drop/type/view changes; schema fingerprints or engine errors must invalidate the entire generation.

Split an oversized parent range into exact half-open children under the same cut, then assert their union equals the parent and no parent file enters the manifest. Corrupt/truncate a file and require digest/parse/count failure. Produce two successful attempts for one logical partition with different bytes; fail closed rather than choose latest. Omit a planned zero-row partition; manifest completeness must fail because absence is not an empty receipt.

After pointer update, lose the response; retry reads the conditional pointer/receipt and returns the existing publication without creating another generation. Exhaust the coordinated log history before baseline publication; do not advance CDC or call the baseline continuous—abandon/rebootstrap with a new cut and retained position. At every injection assert the old trusted pointer remains unless exactly one complete, same-cut, same-schema manifest is durably published.
