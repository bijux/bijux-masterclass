---
module_id: DE-065
program: Data Engineering
level: 2
module_number: 65
title: Partition Evolution in Data Pipelines
status: complete
last_verified: 2026-09-03
---

# Partition Evolution in Data Pipelines

## One-Page Review

### Governing question

How can a long-lived analytical table change its partition strategy while old and new files, specifications, snapshots, writers, readers, deletes, overwrite jobs, and maintenance operations coexist—without missing rows, duplicating rows, pruning valid data, or mistaking object paths for the table's logical contract?

### Essential definitions

- A **partition specification** is a versioned list of source-field identities, transforms, partition-field identities, and names that maps a row to a partition tuple.
- A **partition transform** derives a value such as identity, bucket, truncate, year, month, day, or hour from a source value.
- A **specification ID** identifies the partition specification used for a data file; it lets one snapshot contain files written under different layouts.
- **Hidden partitioning** lets users filter logical source columns while the table implementation derives and applies partition predicates.
- **Partition evolution** creates a new specification for future writes while retaining enough metadata to interpret older files under their original specifications.
- **Inclusive projection** maps a row predicate to a partition predicate that may admit false positives but must not exclude a partition containing a matching row.
- A **residual predicate** is the original or simplified row-level condition evaluated after coarse partition/file pruning.
- **Metadata-native evolution** changes authoritative table metadata without eagerly rewriting existing data files.
- **Repartitioning** physically rewrites rows into files organized by a target layout; it is separate from changing the default specification.
- **Mixed-spec planning** projects the same logical query through each specification represented in a snapshot and unions the safely selected files.
- **Static overwrite** replaces data named by an explicit logical predicate; **dynamic partition overwrite** infers replacement partitions from rows written and can change meaning after partition evolution.
- **Spec convergence** is the optional maintenance process that rewrites old-spec files under the current specification.
- **Physical path** is an object key or directory convention. It may expose partition-like values, but it is not authoritative when table metadata governs membership.

### Central model, mechanism, or theorem

For partition specification $s$, let

$$
\pi_s:r\mapsto (t_{s,1}(r[c_{s,1}]),\ldots,t_{s,k_s}(r[c_{s,k_s}])).
$$

Every live file $f$ records a specification identity $s(f)$ and partition tuple $p_f=\pi_{s(f)}(r)$ for every row $r$ in that file. For query predicate $P$, an inclusive projection $I_s(P)$ is sound when

$$
\forall r,\quad P(r)\Rightarrow I_s(P)(\pi_s(r)).
$$

The planner may reject file $f$ only when $I_{s(f)}(P)(p_f)$ is false. Selected files are then evaluated with residual $P$. Therefore mixed-spec planning remains correct even when a coarse old transform selects more files than a fine new transform. Evolution changes the default for new writes; rewrite is an independent snapshot transition that must preserve the logical row multiset and applicable deletes.

### Critical invariants

- Every file is interpreted using the immutable partition specification identified by its metadata, never merely the current default specification or its path.
- Source columns and partition fields use stable identities across rename and equivalent reuse; retired identities are not reassigned to different meanings.
- An inclusive projection never produces a false negative; residual evaluation supplies exact row correctness.
- Changing the default specification does not silently relocate, reinterpret, or delete old files.
- Old and new specifications may coexist in a snapshot, and planning evaluates each represented specification separately.
- Writers derive partition values from logical source values under the specification they commit and record its identity atomically with file membership.
- Schema, partition, sort, delete, statistics, and snapshot metadata remain mutually compatible.
- Explicit logical predicates define overwrite intent; inferred physical partitions are not treated as stable intent across evolution.
- A physical rewrite publishes replacement files atomically, preserves the logical row multiset and delete semantics, and leaves the previous snapshot available through the rollback horizon.
- Time-travel reads use the specifications and files referenced by the selected historical snapshot.
- Every active reader, writer, catalog, optimizer, maintenance tool, and rollback version supports all specifications and transforms it may encounter.
- Partition paths and metadata receive classification, access, retention, and erasure review because derived values can disclose sensitive facts.
- Skew, small files, pruning quality, metadata volume, old-spec backlog, rewrite progress, and conflicts are observable by specification.

### Common failures

Common failures include reading every file with the newest transform; renaming directories instead of committing metadata; assuming metadata evolution repartitions history; filtering only a visible partition column; using a noninclusive projection; omitting the residual predicate; changing bucket count and treating bucket numbers as comparable; interpreting day and hour values in inconsistent time zones; overwriting inferred dynamic partitions after a spec change; allowing stale writers to commit unknown specs; forgetting old specs in delete/update planning; mixing data from two rewrite generations; listing object storage to infer table membership; dropping old snapshots before rollback evidence exists; publishing a new transform unsupported by one engine; creating millions of tiny partitions; putting high-cardinality secrets into paths; and declaring success from row counts while key multiplicities or delete effects differ.

### Compact example

An old specification partitions `event_hour` by day. A new specification partitions it by hour. For query $5\le event\_hour<7$, the old day projection selects the whole day-0 file containing hours 5 and 18; the new hour projection selects only hour-6. Residual filtering returns hours 5 and 6 and rejects 18. Rewriting the old file into hour-5 and hour-18 files improves future pruning but does not change query results. The specification change was correct before the rewrite; the rewrite is a performance operation with a row-preservation obligation.

### Connections

[DE-008](008-schemas-nullability-and-type-fidelity.md) establishes stable schemas and time semantics, [DE-030](030-designing-replayable-raw-ingestion.md) supplies replayable evidence, [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) governs late routing, [DE-061](061-object-storage-as-a-data-substrate.md) separates object keys from logical membership, [DE-063](063-table-metadata-and-snapshots.md) defines atomic snapshots, and [DE-064](064-schema-evolution.md) develops field identity and mixed-schema reasoning. DE-066 uses snapshot and specification identity for reproducible historical reads; DE-068 applies the same atomicity to compaction; DE-069/070 cover catalog and table-format operations.

## Governing Question

Partitioning is a physical optimization with logical consequences. It controls which rows are colocated, how many objects a write opens, how much metadata a scan visits, and how precisely a predicate can eliminate files. Workloads change: a daily event partition becomes too large, a customer bucket count becomes skewed, a once-selective region becomes nearly constant, or a new access pattern needs a different transform.

The naive answer—change a configuration and rewrite the directories—confuses at least three things. The logical table contract is the schema and snapshot-visible rows. A partition specification maps logical rows to derived tuples. Physical layout is the set of data objects and keys produced under a specification. A robust table format connects them with versioned metadata.

Metadata-native evolution lets files written under old and new specifications coexist. Each file carries or is associated with the specification that produced its partition tuple. A query on logical columns is projected through every applicable specification. This is why a day-partitioned 2025 file and an hour-partitioned 2026 file can answer one time-range query correctly.

That convenience creates obligations. Projection must be conservative. Writers and maintenance tools must commit the right specification identity. Deletes and overwrites must express logical intent across layouts. Old readers must understand every live transform. Historical snapshots must retain the old definitions. An optional rewrite must reconcile exact rows and deletes rather than merely matching counts.

The governing claim is therefore: partition evolution is safe only when specification identity, inclusive pruning, residual filtering, atomic snapshot publication, mixed-version fleet compatibility, and logical rewrite equivalence all hold together.

## Why This Matters

A bad partition design rarely fails immediately. It accumulates costs: thousands of tiny objects per batch, hot writer tasks, overloaded catalog calls, slow manifest planning, broad scans, delayed compaction, and expensive object-store requests. Evolution is the mechanism for correcting the design without replacing the logical table.

Incorrect evolution can silently lose data. Suppose a planner assumes all files use `hour(ts)` after a change. An old file stores only `day(ts)=20431`; comparing that integer to an hour transform is meaningless. If it is pruned, valid rows disappear. If an overwrite replaces only the new hour partitions, older daily files in the same logical interval can survive and produce duplicates or stale values.

Partition transforms are not interchangeable. Bucket 3 under `bucket[16]` does not identify the same population as bucket 3 under `bucket[64]`. A truncated prefix does not prove exact equality. A day value depends on the specified timestamp semantics. A null transform result and a missing partition field must be interpreted under the owning specification.

Object storage intensifies the distinction. Rename is copy plus delete in many object stores, listings can be stale or expensive, and directory names can be arbitrary. A transactional table's metadata, not recursive listing, determines which files belong to a snapshot. Moving keys without an atomic metadata transition risks two visible generations or neither.

Good evolution also protects reproducibility. A time-travel query must plan the snapshot's files under their historical specs, even after the current table uses a different layout. A result should record snapshot ID, schema ID, specification IDs encountered, query predicate, engine version, and relevant timezone/transform rules.

Partition values can be sensitive. Paths like `diagnosis=hiv`, `tenant=acme-merger`, or fine-grained location/time reveal information to object-store inventory, access logs, and operators who cannot read encrypted payloads. Evolution is a governance decision as well as a performance change.

## Prerequisites and Retrieval

Retrieve authoritative table state: table UUID, catalog and location, format/protocol version, current metadata file, current and retained snapshot IDs, schema IDs, partition specifications, default specification ID, sort orders, properties, refs/branches/tags, retention, and encryption.

Retrieve every specification exactly: specification ID; ordered partition fields; source field ID and type; partition field ID and name; transform name and parameter; null behavior; timestamp/timezone semantics; introduction snapshot; retirement/default interval; and engines that wrote it. Do not reconstruct old specs from directory names.

Retrieve file evidence by snapshot and spec: data/delete file path, content type, format, spec ID, partition tuple, record count, size, column bounds/null counts, sequence numbers, encryption key, and commit lineage. Measure files, bytes, and rows per partition and per specification.

Retrieve workload evidence: query predicates and frequency, bytes/files scanned versus returned, pruning stages, latency percentiles, concurrent scans, join/filter patterns, seasonal access, retention windows, time-travel use, and consumers that address physical partition columns or paths directly.

Retrieve writer behavior: engine/library version, cached table metadata lifetime, target spec selection, transform implementation, distribution/shuffle, task parallelism, target file size, maximum open files, retry/conflict behavior, late-data routing, overwrite mode, and stale-writer fencing.

Retrieve reader behavior: engine/version, catalog integration, transform support, mixed-spec planning, metadata/statistics pruning, residual evaluation, delete support, timezone settings, vectorization, caching, and snapshot pinning. Include BI extractors, export jobs, disaster-recovery tools, and direct file readers.

Retrieve mutation and maintenance behavior: append, merge, update, delete, equality/position deletes, copy-on-write or merge-on-read, compaction, clustering, manifest rewrite, orphan cleanup, snapshot expiration, replication, backup, restore, and rollback.

Retrieve governance: data classification, whether derived partition values appear in paths, object-list permissions, cross-tenant isolation, retention and legal holds, deletion obligations, audit logging, approval owner, and allowed maintenance windows.

Retrieve the proposed change and alternatives: add/drop/rename/reorder field; identity/bucket/truncate/time transform; old and new bucket/width/granularity; expected selectivity; projected file rate; skew; rewrite necessity; compute/storage/request cost; rollback boundary; and success thresholds.

Separate the following explicitly: logical predicate from partition predicate; source field ID from name; partition field ID from source ID; spec change from file rewrite; current default from a file's spec; logical partition value from object directory; metadata pruning from row filtering; dynamic partition overwrite from explicit predicate overwrite; time-travel correctness from current performance; and row equality from count equality.

Create an evolution contract:

| Concern | Required evidence |
|---|---|
| Identity | Table, schema, source-field, partition-field, spec, snapshot, and file identities |
| Transform | Exact algorithm, parameter, input type, null/timezone behavior, and engine support |
| Planning | Inclusive projection, residual predicate, file statistics, and mixed-spec tests |
| Writing | Default spec, writer refresh/fence, distribution, size, skew, retry, and conflict behavior |
| Mutation | Append/update/delete/merge and explicit overwrite semantics across every live spec |
| Rewrite | Pinned input, isolated output, row/delete equivalence, atomic commit, and rollback |
| Fleet | Reader, writer, catalog, maintenance, backup, and recovery compatibility matrix |
| Operations | Costs, capacity, observability, alerts, retention, and old-spec convergence policy |
| Governance | Classification, path leakage, permissions, erasure, holds, lineage, and approval |

Write a falsifiable claim: “Snapshot 918 changes the default from spec 4 `day(event_time), bucket(16, customer_id)` to spec 7 `hour(event_time), bucket(64, customer_id)` using stable source identities and supported transforms; all 14 readers, 8 writers, 3 maintenance tools, and rollback versions plan mixed specs 1/4/7 correctly; explicit predicate overwrite replaces the intended logical interval; shadow queries reconcile key multiplicity and aggregates; new writes meet file-size/skew limits; optional rewrite run 451 preserves rows and delete effects before atomic publication; snapshot 917 remains the rollback point; and old-spec backlog is measured rather than assumed.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish logical schema, partition specification, partition tuple, object path, and snapshot membership;
2. model specifications with stable source and partition field identities;
3. derive sound inclusive partition projections and explain the role of residual predicates;
4. plan queries correctly across files written under multiple specifications;
5. evaluate add, drop, rename, reorder, time-granularity, bucket-count, and truncate-width changes;
6. identify dynamic overwrite, stale writer, timezone, delete, and direct-path hazards;
7. choose metadata-only evolution, lazy coexistence, targeted rewrite, full repartition, or new-table cutover;
8. design a pinned, isolated, atomic, reversible repartition workflow;
9. validate logical equivalence beyond row counts and quantify cost, skew, file size, and pruning quality; and
10. operate evolution with fleet gates, observability, governance, retention, and reproducibility evidence.

## Core Exposition

### Treat the specification as a versioned function

A partition spec is not “the folders under the table.” It is an ordered collection of fields. Each field identifies one source column, one transform, a stable partition-field identity, and a human-facing name. The table metadata assigns the collection a spec ID.

An identity transform preserves a source value. `bucket[N]` applies the format's exact hash and modulo rule. `truncate[W]` groups numeric or string/binary values under exact width semantics. Temporal transforms produce year, month, day, or hour offsets according to the table specification. Implementations must use the specified algorithms; a programming language's default hash is not an interchangeable bucket function.

Field identity matters through schema evolution. Renaming source column `event_time` must not disconnect an existing transform from the same logical field. Likewise, renaming a partition field should retain its partition-field ID where the format requires identity stability. A name is presentation; an ID is the durable join across metadata versions.

Specification order can affect tuple representation and metadata schemas even when pruning meaning appears similar. Treat reorder as a real metadata change and test consumers of metadata tables.

### Separate hidden partitioning from directory partitioning

In explicit directory partitioning, writers materialize columns such as `event_date`, place files below `event_date=2026-09-03`, and users may need to filter that column. Logical queries become coupled to physical layout. A change can require new columns, query rewrites, directory migration, and catalog partition repair.

Hidden partitioning retains the relationship `day(event_time)` in table metadata. Writers derive it consistently; readers transform `event_time` predicates for pruning. Users state logical intent. That separation permits multiple physical layouts to serve one table contract.

Hidden does not mean invisible to operations. Partition tuples occur in manifests/metadata tables, object paths may encode them, and access patterns depend on them. It means the application query need not manufacture or maintain the derived value.

Never infer authoritative table membership from object listing. Orphaned files can exist; current files can use unexpected paths; copied objects can be uncommitted. Read the chosen metadata snapshot. Direct path readers bypass deletes, schemas, encryption metadata, and spec evolution and should not be advertised as equivalent table readers.

### Evolve metadata without pretending history moved

In a metadata-native format, adding, removing, renaming, or reordering partition fields creates a new specification and changes the default used by new writes. Existing files retain their original spec association and partition tuples. No eager rewrite is required for correctness.

This yields a transition interval with multiple specs. A daily historical file remains daily. A new hourly file is hourly. The table can be correct indefinitely in this state if all operations understand it. Performance may motivate convergence, but “old spec remains” is not corruption.

Dropping a field from the new default does not erase the field from old tuples, metadata tables, paths, or snapshots. Adding a field gives old files no value under their original spec; readers must not fabricate one by applying the new transform to unavailable row data during metadata planning.

Changing day to hour is commonly represented by adding/replacing the transform according to format rules. Changing `bucket[16]` to `bucket[64]` creates a different mapping. Old bucket values cannot be rescaled or compared as if they belonged to the new domain. Each file is planned under its own transform.

### Plan mixed specifications with inclusive projection

Let $P$ be a row predicate and $I_s(P)$ its inclusive projection under spec $s$. Inclusion means every matching row maps to a partition tuple accepted by $I_s(P)$. The converse need not hold. A selected partition can contain nonmatching rows.

For query $05{:}00\le ts<07{:}00$, `day(ts)` can select the containing day but cannot eliminate its other 22 hours. `hour(ts)` can select hours 5 and 6. Both are sound; one is less selective. The planner evaluates old daily files with the daily projection and new hourly files with the hourly projection.

The file selection set is

$$
F_P=\{f\in F:I_{s(f)}(P)(p_f)\land StatsMayMatch(f,P)\}.
$$

Statistics may further eliminate files only under their own conservative rules. The scan evaluates residual $P$ over rows surviving deletes. A false positive costs I/O; a false negative changes the answer.

Not every predicate projects precisely. Bucket partitioning supports useful equality/in-set pruning but does not preserve order. Truncation groups ranges/prefixes and needs boundary care. Non-deterministic functions, session time zones, casts with failure, or mutable lookup transforms are unsuitable unless the format defines deterministic semantics.

### Preserve time semantics

Temporal evolution is deceptively hard. Determine whether the source is a date, local timestamp, or instant; its precision; the transform's epoch and timezone behavior; and how each engine serializes it. A local wall time in a daylight-saving fold can represent two instants. Metadata cannot recover a missing zone.

For instant/timestamp-with-zone fields, format specifications commonly define UTC-based transforms. For local timestamps, partitioning follows local value semantics. Do not configure session timezone as an undocumented part of a durable partition function. Test boundaries at midnight, month/year rollover, leap day, negative epoch, daylight gaps/folds, and maximum supported precision.

Late events route by event-time transform if that is the specification, not ingestion date. An arrival today for an event yesterday belongs with yesterday's logical partition tuple. Late-data rates and the number of simultaneously open destination partitions affect writer memory and file fragmentation.

### Coordinate writers and distribution

Changing the default specification changes writer routing. Refresh or fence writers that cache table metadata. The commit protocol should reject files associated with an unknown or incompatible spec and validate that their partition tuple matches their declared spec where practical.

Partition transform and writer distribution are related but distinct. Partitioning constrains all rows in a file to one partition tuple. Distribution decides which tasks receive those rows; sorting controls clustering within partitions. Hash distribution can balance partitions across writers, while range distribution can cluster query keys, but either can suffer skew.

Estimate expected file production before rollout:

$$
files\_per\_interval\approx\sum_{p\in active}\left\lceil\frac{bytes_p}{target\_file\_bytes}\right\rceil,
$$

subject to task/checkpoint fragmentation. A useful skew ratio is

$$
Skew_B=\frac{\max_p bytes_p}{\operatorname{mean}_{p:bytes_p>0}bytes_p}.
$$

Track percentiles too; one ratio cannot describe a long tail. Increasing granularity can reduce scan bytes yet create many sub-target files, open-file pressure, and metadata amplification. Bucket count should reflect cardinality, distribution, write rate, file size, and query patterns—not a round number chosen in isolation.

### Make overwrite intent logical and explicit

Overwrite is the most dangerous interaction. Dynamic partition overwrite infers which partitions to replace from the output rows. After day-to-hour evolution, the same code replaces hours rather than whole days. Old daily files overlapping those hours may remain. Conversely, a coarse inferred partition can delete unrelated rows.

Prefer an explicit row predicate such as `event_time >= A AND event_time < B`, evaluated by a table operation that detects all files/data affected across specifications. Validate the engine's exact semantics: some operations replace whole files that may contain rows outside the predicate unless they rewrite/filter them; others reject partial overlap.

For replace, merge, update, and delete, reason in logical keys and predicates. Conflict detection must account for concurrent files under any live spec. Do not use directory deletion as a transactional overwrite. Record the predicate, input/output snapshot, files removed/added, key counts, and conflict result.

### Integrate row-level deletes and updates

Position deletes refer to particular file positions; rewriting a data file requires applying or translating them according to the format operation. Equality deletes match field values and may apply according to sequence/snapshot rules. A repartition job that copies only visible base rows but ignores delete semantics can resurrect records.

Define the logical visible relation for snapshot $S$ as

$$
V(S)=ApplyDeletes(DataFiles(S),DeleteFiles(S),sequence\ rules).
$$

Rewrite equivalence is $V(S_{before})=V(S_{after})$ as a key-aware multiset under the same schema and semantics, not equality of raw file row counts. Duplicate keys may be legitimate, so select set or multiset comparison intentionally.

Concurrent updates complicate long rewrites. Pin an input snapshot, isolate outputs, then commit with conflict validation or rebase/reconcile intervening changes. Never silently publish output calculated from a moving table head.

### Repartition through an atomic rewrite

A safe rewrite proceeds as a controlled generation:

1. pin the source snapshot, schema, specs, delete semantics, and target specification;
2. define logical row scope and exclusions, including holds and corrupt/quarantined data;
3. calculate capacity, request rate, temporary storage, target files, and deadline;
4. write replacement files into isolated, non-authoritative locations with target spec IDs;
5. validate schema, partition derivation, file sizes, statistics, keys, nulls, aggregates, ordering, and delete effects;
6. compare visible rows/key multiplicities between pinned input and candidate output;
7. validate concurrent commits and reconcile or restart affected scope;
8. atomically commit file removals and additions as one new snapshot;
9. canary/shadow reads, monitor performance and correctness, and retain the old snapshot through rollback;
10. expire snapshots and remove unreachable files only after retention, legal hold, and rollback gates.

The rewrite can be incremental. Select old-spec files by bounded scope, rewrite each group, and commit conflict-safe batches. Maintain a backlog by bytes/files/spec, but remember that partial convergence leaves mixed-spec planning mandatory.

Atomic publication prevents readers from seeing half a generation. Isolation prevents uncommitted output from being mistaken for table data. Validation before commit reduces rollback events; retained snapshots make rollback possible until expiration and physical deletion.

### Gate every engine and catalog

Partition evolution is a protocol feature. Build a compatibility matrix whose rows are specifications/transforms and whose columns are reader, writer, catalog, optimizer, mutation, compaction, cleanup, replication, backup, and restore versions. A successful query in one engine does not qualify another engine's writer.

Test mixed-spec fixture tables, not only newly created tables. Include null partitions, negative and boundary transform values, renamed source fields, removed partition fields, different bucket widths, deletes, concurrent writes, metadata tables, time travel, and cached metadata refresh.

Some systems expose partition columns directly or store layout in catalog directory registrations. They may require a new table/location and controlled backfill/cutover instead of native coexistence. Preserve one logical authority during migration: dual-reading two locations without an exact union/deduplication contract invites gaps and duplicates.

Catalog caches can make a compatible engine stale. Define refresh/fence behavior before switching the default spec. The committed table metadata is authoritative; catalog views and metadata tables must display historical spec values without type/name collisions.

### Observe performance and correctness by specification

Measure files, bytes, rows, median and percentile file size, partitions, and null partition values by spec ID and time. Track writer tasks, open files, spill, shuffle, retry, conflict, throughput, and late-partition fan-out.

For reads, record manifests/files/bytes considered, pruned by partition, pruned by statistics, scanned, and returned. Define file pruning selectivity

$$
Selectivity_f=1-\frac{files_{scanned}}{files_{eligible\ before\ pruning}},
$$

with the denominator and query cohort named. Lower scan bytes is useful only if planning latency, metadata reads, and correctness remain acceptable.

Track old-spec backlog, rewrite throughput, validation failures, candidate bytes, committed bytes, orphan candidates, snapshot age, and rollback horizon. Alert on unknown spec IDs, unsupported transforms, partition-tuple mismatch, sudden skew, tiny-file bursts, zero-file overwrites, unexpected predicate scope, and divergence between logical controls and table results.

Use control queries at boundaries and across mixed regions: counts by logical date/hour, distinct keys, duplicate multiplicities, sums, null cohorts, min/max event time, deleted-key absence, and sampled row digests. Compare independent planners where possible.

### Govern lifecycle, security, and reproducibility

Partition design belongs in a reviewed data contract: purpose, owner, expected workload, transform, identity, granularity, sensitive derivation, cost budget, evolution policy, and deprecation horizon. Performance tuning does not bypass change control when it affects paths, retention, or access patterns.

Avoid raw sensitive values in partitions when a coarser non-identifying transform suffices. Bucketing can reduce obvious readability but is not anonymization; small domains are reversible by enumeration. Protect metadata files, inventory, logs, and metrics. Ensure tenant partitioning is backed by authorization rather than used as authorization itself.

Time travel is reproducible only while referenced metadata, specs, files, schemas, deletes, transform implementations, and keys remain available. Record snapshot ID rather than “latest.” After snapshot expiration, state that the old result is no longer reproducible; do not imply object backups automatically restore table semantics.

Retire an old spec operationally only after no live snapshot/file requires it, no rollback or historical reader needs it, and metadata retention permits removal. Physical cleanup uses reachability from authoritative metadata plus retention/hold rules, never name patterns alone.

## Definitions and Notation

Let $R$ be the logical row domain and $C$ the stable source-field identities. A partition field is

$$
q=(field\_id,source\_id,transform,name).
$$

A specification $s=(spec\_id,q_1,\ldots,q_k)$ induces $\pi_s:R\rightarrow P_s$, where $P_s$ is the tuple domain. Different specs may have different tuple arity and types.

Let $F(S)$ be the live data files in snapshot $S$. File metadata includes

$$
f=(path,s(f),p_f,stats_f,rows_f,sequence_f).
$$

The partition invariant is

$$
\forall f\in F(S),\forall r\in rows_f,\quad \pi_{s(f)}(r)=p_f.
$$

For row predicate $P:R\to\{true,false\}$, inclusive projection $I_s(P):P_s\to\{true,false\}$ satisfies

$$
P(r)\Rightarrow I_s(P)(\pi_s(r)).
$$

A strict projection, where supported, provides the opposite useful implication: if the strict partition predicate is true, all rows in that partition satisfy the row predicate. Inclusive projection is the essential requirement for safe pruning; strict projection can help decide whole-file operations.

The candidate files for $P$ are $F_P$. Exact query output is

$$
Q(S,P)=\{r:r\in V(S),\ file(r)\in F_P,\ P(r)\}.
$$

Let $S_0\to S_1$ be a rewrite. Logical equivalence under projection $A$ is

$$
\mathcal{M}(project_A(V(S_0)))=\mathcal{M}(project_A(V(S_1))),
$$

where $\mathcal{M}$ is a multiset. Choose $A$ to include stable keys and every semantically relevant value; aggregates alone are insufficient.

Define file amplification $A_f=files_{after}/files_{before}$, metadata density $D_m=metadata\ bytes/data\ bytes$, and old-spec backlog $B_o=\sum_{f:s(f)\ne default}|f|$. These are operational indicators, not universal optimization targets.

## Mechanisms, Invariants, or Proof Structure

Proof sketch for sound mixed-spec pruning:

1. Choose any row $r$ in snapshot $S$ such that query predicate $P(r)$ is true.
2. The row belongs to some live data file $f$ with recorded spec $s(f)$ and tuple $p_f=\pi_{s(f)}(r)$.
3. By inclusive-projection soundness, $P(r)$ implies $I_{s(f)}(P)(p_f)$.
4. Therefore partition pruning cannot reject $f$ because of its partition tuple.
5. Sound file statistics likewise cannot reject a file containing a matching value.
6. The scan reads $f$ and applies deletes plus residual $P$; row $r$ remains if it is visible.
7. The argument depends only on the file's own spec, so it applies independently to every spec represented in $S$.
8. Taking the union of selected files across specifications therefore cannot lose a visible matching row.

The result proves absence of pruning false negatives under the premises. It does not prove efficient pruning, correct transform implementations, sound statistics, delete handling, or fleet compatibility. Those are separate obligations.

The rewrite invariant follows from atomic replacement. Candidate files remain invisible until commit. If candidate visible rows equal the removed files' visible rows within the rewrite scope, concurrent changes are rejected or reconciled, and one snapshot atomically removes old files and adds candidates, then readers see either the before relation or the equivalent after relation—not a partial mixture.

The executable below models daily-to-hourly evolution. Integer hours avoid library timezone ambiguity. It deliberately uses only `day` and `hour`; it is not an implementation of Iceberg, Delta Lake, Hudi, Spark, object storage, manifests, statistics, or deletes.

<!-- bijux-verify: {"id":"mixed-partition-spec-planning","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"specs=((1, 'day'), (2, 'hour'))\nselected_files=('new-hour-6', 'old-day-0')\nresult_rows=(('a', 5), ('d', 6))\nresidual_filtered=(('b', 18),)\nrewrite_files=('new-hour-30', 'new-hour-6', 'old-day-1', 'rewritten-hour-18', 'rewritten-hour-5')\nlogical_rows_preserved=True\nold_spec_remaining=('old-day-1',)\n","stderr":""}} -->
```python
specs = {1: "day", 2: "hour"}
files = {
    "old-day-0": (1, 0, (("a", 5), ("b", 18))),
    "old-day-1": (1, 1, (("c", 30),)),
    "new-hour-6": (2, 6, (("d", 6),)),
    "new-hour-30": (2, 30, (("e", 30),)),
}


def inclusive_match(spec_id, partition, start, end):
    if specs[spec_id] == "hour":
        return start <= partition < end
    first_day = start // 24
    last_day = (end - 1) // 24
    return first_day <= partition <= last_day


def visible_rows(file_map):
    return sorted(row for _, _, rows in file_map.values() for row in rows)


start, end = 5, 7
selected = tuple(sorted(
    name for name, (spec_id, partition, _) in files.items()
    if inclusive_match(spec_id, partition, start, end)
))
scanned = [row for name in selected for row in files[name][2]]
result = tuple(sorted(row for row in scanned if start <= row[1] < end))
residual_filtered = tuple(sorted(row for row in scanned if not start <= row[1] < end))

rewritten = dict(files)
_, _, old_rows = rewritten.pop("old-day-0")
for row in old_rows:
    rewritten[f"rewritten-hour-{row[1]}"] = (2, row[1], (row,))

print(f"specs={tuple(sorted(specs.items()))}")
print(f"selected_files={selected}")
print(f"result_rows={result}")
print(f"residual_filtered={residual_filtered}")
print(f"rewrite_files={tuple(sorted(rewritten))}")
print(f"logical_rows_preserved={visible_rows(files) == visible_rows(rewritten)}")
print(f"old_spec_remaining={tuple(sorted(name for name, value in rewritten.items() if value[0] == 1))}")
```

The old day-0 file is necessarily a false-positive container for hour 18. Residual filtering removes that row. After rewrite, hour-level pruning can avoid it, all logical rows remain, and one unrelated old-spec file demonstrates partial convergence.

## Alternatives and Trade-Offs

**Metadata-native evolution versus new table.** Native evolution preserves table identity and avoids mandatory rewrite, but requires complete mixed-spec support. A new table works for systems without that support and isolates risk, but needs backfill, dual-run, consumer cutover, and ownership of two surfaces.

**Lazy coexistence versus eager convergence.** Coexistence minimizes migration cost and preserves immutable files. Eager rewrite makes current pruning consistent and can reduce old-spec metadata, but consumes compute/storage, conflicts with writes, and shortens rollback only if old snapshots are later expired.

**Fine temporal granularity versus coarse granularity.** Hour partitions improve narrow time-range pruning at sufficient volume. Day/month partitions reduce partition and file fan-out. File statistics and clustering can sometimes deliver narrow pruning without finer partitions.

**Identity versus bucket.** Identity supports range/equality interpretation and readable values but exposes/high-cardinality values and can skew. Bucketing bounds partition cardinality and distributes high-cardinality keys but loses range ordering and must use the exact stable algorithm.

**Larger versus smaller bucket count.** More buckets can reduce per-bucket size and improve equality pruning but fragment writes and metadata. Fewer buckets make larger files easier but increase scans and hotspots. Changing $N$ creates a distinct mapping.

**Truncate versus bucket.** Truncate preserves coarse order/prefix and benefits range/prefix access, but skewed prefixes remain skewed and may leak values. Bucket distributes values more uniformly but cannot support ordered range pruning.

**Partition versus sort/cluster.** Partitioning is a hard file boundary and metadata dimension. Sorting/clustering can improve statistics and compression with less fan-out. Use partitioning for consistently selective, sufficiently large groups and sorting for secondary locality.

**Dynamic overwrite versus explicit predicate overwrite.** Dynamic overwrite is convenient when the physical partition scheme is stable and fully understood. Explicit predicates preserve logical intent through evolution and are safer for mixed specs, at the cost of more deliberate APIs and conflict checks.

**Full rewrite versus incremental rewrite.** Full rewrite gives one clean cutover but demands peak capacity and large conflict scope. Incremental batches reduce blast radius and can pause, but extend mixed-spec operations and require progress accounting.

**In-place rewrite versus isolated generation.** In-place mutation appears storage-efficient but exposes partial output and complicates recovery. Isolated immutable files plus atomic metadata replacement temporarily duplicate bytes but provide validation and rollback.

**Event-time versus ingestion-time partitioning.** Event time aligns analytical predicates and historical truth but sends late data to old partitions. Ingestion time stabilizes current writes but broadens event-time scans. A deliberate combination may use one as partition and the other as sort/statistics.

**Partition path values versus opaque keys.** Readable paths help operators and compatibility with directory tools, but leak metadata and tempt direct reads. Opaque keys reinforce metadata authority but require capable tooling.

**Permanent old-spec support versus retirement.** Retaining old snapshots improves audit and rollback but forces clients to support old specs and retains bytes. Expiration reduces cost only after policy, legal hold, reproducibility, and rollback requirements are met.

## Failure Modes and Misconceptions

1. **“The current spec describes every file.”** Each file must be interpreted by its recorded spec.
2. **“Changing the spec repartitions history.”** Metadata evolution changes future writes; existing files stay put until rewritten.
3. **“A folder is a partition contract.”** Authoritative metadata, not a path string, establishes file membership and transform meaning.
4. **“Rename the directories.”** Object moves are nontransactional copies/deletes unless coordinated through a table operation.
5. **“Bucket 3 remains bucket 3.”** Different bucket counts create different populations even when the displayed number matches.
6. **“Day-to-hour is a numeric conversion.”** Old daily tuples and new hourly tuples belong to different transform domains/specs.
7. **“Projection must be exact.”** Inclusive projection may return false positives; residual filtering restores exactness.
8. **“False positives are correctness failures.”** They are performance costs; false negatives are correctness failures.
9. **“Partition pruning replaces the WHERE clause.”** The logical residual predicate must still be evaluated unless strict proof removes it.
10. **“Statistics are always trustworthy.”** Bounds, null/NaN handling, truncation, encryption, corruption, and implementation bugs require conservative interpretation.
11. **“Session timezone is harmless.”** It can route the same wall time differently and break deterministic transforms.
12. **“Late data belongs to today's partition.”** Event-time partitioning routes by event value, not arrival date.
13. **“More partitions means faster queries.”** Tiny files, metadata, open-file limits, and planning overhead can dominate.
14. **“Uniform key cardinality means uniform bytes.”** Frequency skew and variable row size can create hotspots.
15. **“Dynamic overwrite keeps its meaning.”** The inferred replacement unit changes with the default specification.
16. **“Deleting a directory is an overwrite.”** It bypasses snapshot atomicity, concurrent commits, deletes, and rollback.
17. **“Row counts prove rewrite equality.”** Duplicates, substitutions, nulls, deleted rows, and offsetting amounts can preserve counts.
18. **“Copying base files preserves deletes.”** Position/equality delete semantics must be applied or translated deliberately.
19. **“A stale writer will refresh eventually.”** It can commit old or malformed layout during the transition unless fenced/validated.
20. **“One engine passed, so the table is compatible.”** Every reader, writer, optimizer, and maintenance/recovery tool has an independent gate.
21. **“Compaction automatically converges specs.”** It may preserve an old spec, use a stale default, or rewrite only selected files.
22. **“Time travel uses today's partition rules.”** Historical snapshots require their referenced historical specifications.
23. **“Dropped partition fields disappear.”** Old metadata, paths, snapshots, logs, and backups can retain their values.
24. **“Buckets anonymize sensitive IDs.”** Small domains can be enumerated and membership itself can disclose information.
25. **“Listing finds all table data.”** It includes orphans and may omit/lag objects; the snapshot is authoritative.
26. **“Rollback is always a metadata pointer.”** Once snapshots/files/keys are expired or clients cannot read old specs, restoration needs more than pointer reversal.

## Worked Examples

### Example 1

A click table changes from `day(event_time)` to `hour(event_time)`. New writers use spec 9; files under spec 4 remain daily. A 20-minute query selects one old day file but one new hour partition, then applies the same timestamp residual. Correctness is immediate; an incremental rewrite is approved only if saved scan cost exceeds rewrite and metadata cost.

### Example 2

An account table changes `bucket(16, account_id)` to `bucket(64, account_id)`. The team never maps old bucket 5 to new bucket 5. Equality predicates are hashed separately under each spec. Metrics show new buckets average 480 MiB per day instead of 1.8 GiB, while file-size p50 remains above the 256 MiB floor.

### Example 3

A source column is renamed from `created_at` to `event_time` while retaining field ID 17. The partition transform still references source ID 17. The partition-field name is separately renamed with its own stable identity. ID-aware readers succeed; SQL against metadata-table column names receives a compatibility view during migration.

### Example 4

An hourly backfill uses dynamic overwrite after a table formerly partitioned daily. It writes hours 10 and 11, replacing only inferred new hourly partitions; an old daily file still contains stale rows for those hours. The corrected operation expresses the logical interval, identifies every overlapping file across specs, rewrites partial overlaps, and commits replacements atomically.

### Example 5

A local timestamp `2026-11-01 01:30` occurs twice in `America/New_York`. The source lacks offset and zone authority. The pipeline does not pretend it can derive a unique UTC hour. It preserves the local value, records ambiguity, and quarantines or applies a versioned source-specific rule before partitioning an instant.

### Example 6

A high-cardinality `device_id` identity partition creates 900,000 tiny objects daily and exposes identifiers in keys. The replacement uses a specified bucket transform and sorts by event time within buckets. The rollout verifies hash compatibility across engines, access leakage, bucket skew, file size, and equality-query pruning.

### Example 7

An incremental rewrite pins snapshot 700 and rewrites 2 TiB of spec-2 files. Concurrent appends create snapshot 701 outside its scope; an update touches one selected key. Commit validation accepts the disjoint appends but rejects the conflicting group. The job recomputes that group from the new head instead of publishing stale data.

### Example 8

A position-delete file removes row 481 in data file A. Repartitioning A without applying the delete would resurrect the row because positions change. The table's rewrite operation reads the visible relation with delete semantics, writes only visible rows, and atomically replaces both affected artifacts according to the format protocol.

### Example 9

Region identity partitioning creates a 40:1 byte skew because one region holds most traffic. Adding customer buckets under region lowers maximum writer load but increases partition fan-out. The team compares region+bucket, bucket-only, and region sorting using representative query and write traces, then chooses the smallest layout meeting both pruning and file-size SLOs.

### Example 10

A historical audit pins snapshot 412, schema 6, and specs 1 and 3. Even though current writes use spec 8, the engine retrieves the historical spec definitions and delete files. The evidence records engine and table-format versions plus snapshot ID; after planned expiration, governance explicitly marks the reproduction horizon closed.

## Cross-Program Connections

- **Database Systems:** indexes, clustered storage, predicate implication, optimizer statistics, MVCC, logical deletes, and online table reorganization explain partition planning and rewrite publication.
- **Distributed Systems:** immutable objects, optimistic concurrency, stale metadata, atomic pointers, retries, split-brain writers, and mixed-version protocols shape every transition.
- **Algorithms and Data Structures:** hashing, modulo, range partitioning, prefix truncation, histograms, bloom filters, skew, and bin packing determine distribution and pruning.
- **Formal Methods:** function identity, implication, conservative abstraction, refinement, invariants, and multiset equivalence distinguish sound pruning from empirical confidence.
- **Systems Engineering:** fleet inventories, interface control, hazards, verification evidence, rollback envelopes, capacity, and lifecycle management turn a DDL change into a system change.
- **Reliability Engineering:** canaries, shadow reads, error budgets, fault injection, observability, incident rollback, and recovery drills qualify the operational path.
- **Security Engineering:** object-key disclosure, metadata authorization, tenant isolation, immutable audit logs, encryption keys, and cleanup reachability apply beyond payload files.
- **Privacy Engineering:** minimization, derived identifiers, location/time granularity, retention, erasure, legal holds, and backup scope constrain partition choice.
- **API and Service Engineering:** explicit logical predicates, stable identifiers, version negotiation, idempotency, compatibility matrices, and deprecation mirror service-contract evolution.
- **Cloud and Platform Engineering:** object request cost, catalog services, IAM, workload scheduling, autoscaling, quotas, and multi-region replication bound feasible rewrites.
- **Software Engineering:** migration adapters, feature gates, contract tests, immutable releases, semantic naming, and ownership keep mixed versions maintainable.
- **Statistics and ML:** sampling bias from pruned files, time leakage, feature backfills, training snapshot identity, and distribution skew rely on reproducible table reads.

## References

1. Apache Iceberg. [Table specification](https://iceberg.apache.org/spec/). Accessed 2026-09-03. Primary specification for partition fields and IDs, transforms, partition evolution, manifest specification identity, projection, files, snapshots, and sequence semantics.
2. Apache Iceberg. [Partitioning](https://iceberg.apache.org/docs/latest/partitioning/). Accessed 2026-09-03. Primary documentation contrasting explicit directory partitioning with hidden partitioning and logical predicate planning.
3. Apache Iceberg. [Evolution](https://iceberg.apache.org/docs/latest/evolution/). Accessed 2026-09-03. Primary documentation for coexisting partition layouts, split planning, metadata-only evolution, and new-write behavior.
4. Apache Iceberg. [Spark DDL](https://iceberg.apache.org/docs/latest/spark-ddl/). Accessed 2026-09-03. Primary engine documentation for partition transforms, add/drop/replace fields, and dynamic overwrite hazards after evolution.
5. Apache Iceberg. [Performance](https://iceberg.apache.org/docs/latest/performance/). Accessed 2026-09-03. Primary documentation for manifest- and data-file-level partition/statistics pruning.
6. Apache Iceberg. [Maintenance](https://iceberg.apache.org/docs/latest/maintenance/). Accessed 2026-09-03. Primary documentation for data-file rewrite, manifest rewrite, snapshot expiration, and orphan-file lifecycle operations.
7. Apache Iceberg. [Reliability](https://iceberg.apache.org/docs/latest/reliability/). Accessed 2026-09-03. Primary documentation for atomic metadata operations, optimistic concurrency, retries, and serializable isolation.
8. Apache Spark. [SQL performance tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html). Accessed 2026-09-03. Primary engine documentation for partitioning, shuffle, file sizing, statistics, and adaptive execution considerations.
9. Apache Spark. [Data source options](https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html). Accessed 2026-09-03. Primary engine documentation for save modes and partitioned file layout behavior.
10. Delta Lake. [Table batch reads and writes](https://docs.delta.io/latest/delta-batch.html). Accessed 2026-09-03. Primary documentation for partitioned tables, replaceWhere, dynamic partition overwrite, validation, and overwrite behavior.
11. Delta Lake. [Delta Transaction Log Protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md). Accessed 2026-09-03. Primary protocol specification for table metadata, partition columns, files, logical/physical column mapping, actions, and atomic versions.
12. Apache Hudi. [SQL DDL](https://hudi.apache.org/docs/sql_ddl/). Accessed 2026-09-03. Primary documentation for partitioned table definitions, partition folders, and partition operations in Hudi engine integrations.
13. Apache Hudi. [Table metadata](https://hudi.apache.org/docs/metadata/). Accessed 2026-09-03. Primary documentation for cloud-scale file listing, partition metadata, and column-statistics data skipping.

## Exercises

### Exercise 1

A table has spec 3 `day(ts), bucket(8, customer_id)` and proposes spec 6 `hour(ts), bucket(32, customer_id)`. Design mixed-spec planning for a 90-minute time range and one customer. State transforms, inclusive projections, residual, compatibility tests, and why equal bucket numbers across specs cannot be joined.

### Exercise 2

Design an incremental physical convergence of 400 TiB while writes, updates, position/equality deletes, and time-travel queries continue. Include snapshot pinning, grouping, isolation, conflict handling, logical equivalence, publication, capacity, rollback, retention, and progress metrics.

### Exercise 3

A streaming pipeline writes 2 TiB/day with 30-day late arrivals. Compare day, hour, identity region, bucketed customer, and sorting alternatives. Use file-size, open-partition, skew, pruning, privacy, and metadata considerations to propose an experiment and decision gate.

### Exercise 4

Diagnose a dynamic-overwrite incident after day-to-hour evolution: new hourly files coexist with an old daily file, causing duplicate current rows. Specify containment, evidence preservation, logical repair predicate, concurrency controls, validation, rollout correction, and prevention tests.

### Exercise 5

Build a production observability and governance contract for a table with three live specs, six engines, sensitive tenant/time values in paths, legal-hold snapshots, and a two-week rollback requirement. Define metrics, alerts, compatibility gates, access controls, evidence, and retirement criteria.

## Answers to the Exercises

### Answer 1

Retain source and partition field identities plus exact spec definitions. For each file, hash the customer using that file's bucket count and project the time interval using its time granularity. Spec 3 selects every touched day and bucket $h_8(customer)$; spec 6 selects touched hours and $h_{32}(customer)$. Union candidates, apply conservative statistics, then evaluate exact time and customer residuals plus deletes. Test boundary hours/days, nulls, hash vectors, negative/Unicode identifiers, old/new files, all engines, and metadata caching. Bucket 5 under eight partitions contains hashes congruent modulo 8; bucket 5 under 32 is a strict different subset, so the labels do not establish common membership.

### Answer 2

Pin a source snapshot and define stable logical/file scopes. Apply all delete and schema semantics while writing target-spec files to isolated locations. Size groups so they fit capacity and conflict windows; throttle object requests and preserve headroom. Validate partition tuples, schema, file sizes, visible key multiplicity, nulls, aggregates, sampled row digests, and deleted-key absence. At commit, reject or reconcile intersecting appends/updates/deletes and atomically remove old files/add candidates. Record before/after snapshots per batch, retain old snapshots for rollback, and delay orphan cleanup until retention/holds permit. Track bytes/files by old spec, throughput, ETA, conflicts, retries, candidate waste, validation failures, scan improvement, and storage amplification. Mixed-spec support remains required until no live retained snapshot depends on an old spec.

### Answer 3

Replay representative write and query traces into candidate tables. Day partitioning limits late destinations to roughly 30 day buckets per routing dimension but broadens sub-day scans. Hour raises potential late destinations toward 720 and risks small files/open-writer pressure. Region identity is useful only if non-sensitive, selective, and not severely skewed. Customer bucketing bounds cardinality and supports equality pruning; sorting by event time/customer may improve file bounds without extra hard partitions. Measure file-size p10/p50/p90, files/day, open writers, spill/shuffle, max/mean and percentile skew, manifests/requests, scan-to-return bytes, latency, late fan-out, and path disclosure. Choose the least complex candidate meeting stated write, query, cost, and privacy thresholds under peak data—not an average-only benchmark.

### Answer 4

Pause/fence the faulty writer and preserve table metadata, snapshots, job configuration, commit actions, query evidence, and affected logical interval. Pin the last known-good and current snapshots; identify all old/new files whose row domains overlap the interval, including deletes and concurrent commits. Repair through an explicit logical predicate or key-based merge that rewrites partial old-file overlaps and atomically publishes one visible relation. Reconcile key multiplicities, timestamps, aggregates, deleted keys, and downstream controls before resume; retain the pre-repair snapshot through rollback. Replace dynamic overwrite with an explicit predicate API, add mixed-spec fixtures and old-file overlap tests, require cached-writer refresh/fencing, and alert when removed file scope does not cover the declared logical interval.

### Answer 5

Inventory specs/transforms and require every one of the six engines—reader, writer, mutation, maintenance, backup, and restore modes—to pass mixed-spec, null/boundary, delete, time-travel, cache, and rollback fixtures. Emit files/bytes/rows/size percentiles/skew and pruning stages per spec; unknown IDs, unsupported transforms, tiny-file bursts, conflict spikes, tuple mismatches, control-query divergence, expiring rollback snapshots, and legal-hold violations alert. Restrict metadata and object-list access, treat bucket values as potentially identifying, remove tenant/time values from future paths where feasible, and retain audited approvals and snapshot/spec/query lineage. An old spec is retireable only when no live file or retained/held snapshot references it, all required results have passed their reproduction horizon, clients no longer need it, rollback exceeds two weeks, and authorized snapshot expiration plus reachability-based cleanup has completed.
