---
module_id: DE-067
program: Data Engineering
level: 2
module_number: 67
title: Compaction and Small-File Management
status: complete
last_verified: 2026-09-03
---

# Compaction and Small-File Management

## One-Page Review

### Governing question

How can a data platform prevent and repair harmful small-file accumulation while ingestion, updates, deletes, historical snapshots, streaming consumers, schema and partition evolution, concurrent writers, catalogs, and cleanup continue—without changing the logical table, resurrecting deleted rows, publishing partial rewrites, or spending more on maintenance than compaction saves?

### Essential definitions

- A **small file** is a data file whose size is materially below the workload-specific efficient range; it is not defined by one universal byte threshold.
- **File compaction** rewrites a set of data files into fewer appropriately sized files while preserving the visible logical relation.
- **Bin packing** groups input files or rows into output groups near a target size without intentionally changing logical clustering.
- **Target file size** is a planning goal for encoded output, not an exact guarantee; compression ratio, row width, row-group boundaries, and task behavior affect actual size.
- **Write-time sizing** shapes files during ingestion through distribution, shuffle, task sizing, rolling, and adaptive writer behavior.
- **Post-write compaction** repairs layout after commit through a snapshot/timeline rewrite.
- **Manifest or log compaction** combines metadata/log artifacts to reduce planning or replay work; it is distinct from data-file compaction.
- **Merge-on-read compaction** merges base files with update/delete logs into new file slices; its semantic obligations differ from merely combining immutable data files.
- **Clustering** rewrites layout by sort/range/space-filling locality as well as size; it is addressed in DE-068 and should not be called plain bin packing.
- A **rewrite group** is an independently planned set of input files whose replacement outputs are committed together or under explicit partial-progress semantics.
- **Rewrite amplification** is bytes read plus bytes written relative to useful logical change or future I/O saved.
- **File amplification** is the number of files a logical amount of data occupies relative to an intended layout.
- A **small-file debt** is the measured future planning/read/write/metadata cost attributable to fragmented layout.
- **Partial progress** publishes successful rewrite groups in multiple commits; it limits retry cost but exposes intermediate states and complicates accounting.
- **Cleanup** physically removes old or failed files only after snapshot, reader, stream, rollback, retention, and active-writer reachability permit it.

### Central model, mechanism, or theorem

For snapshot $S$, let $V(S)$ be the visible row multiset after applying all delete semantics. A compaction plan selects input files $I\subseteq Files(S)$ and writes outputs $O$. Correctness requires

$$
\mathcal{M}(Visible(I,S))=\mathcal{M}(Visible(O,S')),
$$

under the declared schema, sequence, and delete rules. Publication is an atomic compare-and-swap-like transition:

$$
Files(S')=(Files(S)\setminus I)\cup O,
$$

only if every required input remains live and no conflicting commit invalidates the plan. The economic gate compares discounted future savings with rewrite, temporary storage, conflict, cleanup, and operational costs. Fewer files is beneficial only when this entire contract holds.

### Critical invariants

- Compaction preserves the visible logical row multiset, field identities, null/default semantics, and authorized ordering contract.
- Position deletes, equality deletes, deletion vectors, merge logs, and sequence numbers are applied, retained, or translated according to the table format.
- Input selection is pinned to an immutable snapshot or timeline instant; a moving `latest` is never the rewrite source.
- Candidate outputs are durable and invisible until a valid atomic snapshot/timeline commit replaces exact inputs.
- A retry never publishes outputs derived from inputs that were concurrently removed or semantically changed.
- Old snapshots keep their old files until retention expires; replacing current membership is not immediate physical deletion.
- Output files carry the correct current or explicitly selected schema, partition spec, sort order, statistics, encryption, and protocol metadata.
- Rewrite scope does not cross partition/spec boundaries in ways the format forbids or mislabel output partition tuples.
- Target sizing accounts for encoded bytes, compression, row groups, variable-width rows, task skew, and maximum file limits.
- Write-time prevention and post-write repair are measured together; compaction does not excuse a permanently pathological writer.
- Data-file, manifest, transaction-log, merge-log, and clustering maintenance have separate goals and metrics.
- Scheduling respects ingestion/query capacity, commit rate, object-store requests, catalogs, quotas, locks, and failure recovery.
- Cleanup proves files are unreachable from every protected snapshot/reference and outside all active-operation horizons.
- Success is demonstrated by correctness controls and end-to-end cost/latency improvement, not only a lower file count.

### Common failures

Common failures include choosing 128 MiB as a universal optimum; compacting already healthy files every hour; using row counts as a byte proxy for variable-width data; coalescing the entire table to one file; crossing partition boundaries; ignoring old partition specs; reading current state while it changes; carrying stale position deletes to replacement files; dropping equality-delete or merge-log effects; setting “no data change” on a rewrite that changes rows; publishing each output before its group is complete; blindly retrying after input conflicts; deleting old files immediately; counting orphans as active inputs; confusing manifest rewrite with data compaction; calling sort/Z-order clustering bin packing; starving ingestion with inline maintenance; accepting hundreds of tiny tail files from skew; and claiming savings without measuring planning, scan, request, shuffle, temporary-storage, and rewrite costs.

### Compact example

Five same-partition files have encoded sizes 70, 40, 30, 20, and 10 units. First-fit decreasing with target 100 creates groups `(70,30)` and `(40,20,10)`, producing two files of 100 and 70 units. The file count drops by three, but that arithmetic proves only packing. Before commit, the job must also show identical visible key/value multiplicities after deletes, correct schema/spec/statistics, exact input liveness, and atomic replacement. A concurrent update to one input invalidates that group even if its size plan remains attractive.

### Connections

[DE-034](034-partitioned-processing.md) introduces physical partition work, [DE-036](036-merge-and-upsert-semantics.md) supplies mutation semantics, [DE-055](055-delivery-semantics-in-streaming-pipelines.md) governs streaming effects, [DE-063](063-table-metadata-and-snapshots.md) defines atomic membership, [DE-064](064-schema-evolution.md) governs mixed schemas, [DE-065](065-partition-evolution-in-data-pipelines.md) governs mixed specs, and [DE-066](066-time-travel-and-reproducible-reads.md) protects historical files. DE-068 adds clustering/data skipping; DE-069/070 cover catalog and table-format operations.

## Governing Question

Small files are a systems symptom, not a moral failing. Low-latency streams commit small micro-batches. Highly partitioned writes fan one task into many destinations. Updates rewrite fragments. Late arrivals touch cold partitions. Skew leaves some writers nearly empty. Failure recovery and speculative execution can further fragment output.

Each file has fixed costs: metadata entry, catalog or manifest work, object request, file open, footer read, split planning, scheduler task, credential check, encryption context, and reader initialization. Ten thousand 1 MiB files usually cost more to plan and scan than twenty 500 MiB files containing the same bytes. But very large files reduce parallelism, widen update conflicts, lengthen retry units, and can exceed memory or row-group goals.

Compaction trades current write and storage cost for lower future overhead. It reads existing state, applies deletes/logs as required, groups data, writes replacement files, and atomically changes table membership. The operation should be logically data-preserving even though physical files and statistics change.

The word “compaction” is overloaded. Data-file bin packing combines small immutable files. A merge-on-read compaction folds delta logs into base files. Log compaction combines log blocks. Manifest/log compaction reduces metadata replay. Clustering changes data locality. These operations need different correctness checks and schedules.

The governing decision is not “when do we run OPTIMIZE?” It is: what layout debt exists, what caused it, which files can be safely rewritten, which semantics must be preserved, how will conflicts and partial progress work, and do measured future savings exceed the complete cost and risk?

## Why This Matters

Fragmentation taxes every consumer. Query planning reads more metadata; object stores receive more GET/HEAD requests; compute schedulers launch more tasks; readers open more footers; caches hold more entries; catalogs and manifests grow; scans spend less time on useful sequential I/O. Interactive tail latency often suffers before average throughput looks alarming.

Writers suffer too. Upserts search or touch more files. Commits manipulate larger metadata sets. Garbage collection lists and evaluates more objects. Replication and backup handle more keys. Encryption and access logging produce more control-plane events. A million cheap objects can create an expensive system.

Naive repair threatens correctness. A compactor that reads base files without position/equality deletes resurrects rows. A stale plan can replace a file updated by another writer. A direct directory overwrite can expose both generations or neither. A rewrite using the newest partition spec but old path assumptions can mislabel data.

Historical readers constrain cleanup. A current snapshot may use compacted outputs while yesterday's retained snapshot still references old inputs. Deleting those inputs immediately breaks time travel and long-running readers. Temporary storage amplification is therefore intrinsic to immutable snapshot designs.

Economics prevent cargo culting. Compacting 80 MiB files into 128 MiB files may cost more than it saves. Rewriting a cold petabyte for a tiny request reduction is wasteful. Conversely, allowing a high-frequency stream to produce one file per partition per minute can overwhelm metadata. Decisions need workload evidence and a break-even horizon.

The durable solution combines prevention and repair. Writers aim for healthy layout without unacceptable latency; background maintenance handles unavoidable fragmentation; observability closes the loop; retention eventually removes replaced artifacts safely.

## Prerequisites and Retrieval

Retrieve table authority: stable table ID, catalog/location, format/protocol, current and retained snapshots or instants, schema IDs, partition specs, sort orders, sequence rules, data/delete/log file types, branches/tags/savepoints, and retention/cleanup policy.

Retrieve file inventory from authoritative metadata, not directory listing: path, content type, live snapshots, partition tuple and spec ID, schema context, sequence number, encoded size, record count, row groups, compression, column bounds/nulls, encryption key, commit age, and delete/log attachments.

Retrieve distributions by partition and time: file-size p1/p10/p50/p90/p99/max, count, bytes, rows, compression ratio, row-width distribution, files per commit, files per writer task, small-file fraction by count and bytes, empty files, oversized files, and old-spec files.

Retrieve query costs: metadata/manifests read, planning latency, files and bytes considered/pruned/scanned, object requests, task launch time, footer time, cache behavior, scan throughput, CPU, memory, spill, queue time, p50/p95/p99 latency, concurrency, and predicate cohorts.

Retrieve write causes: micro-batch interval and volume, partition fan-out, late partitions, writer distribution/sort, shuffle partitions, adaptive execution, target and maximum file sizes, rolling policy, open-file cap, task failures/speculation, merge/update/delete behavior, schema/spec changes, and commit cadence.

Retrieve maintenance mechanics: supported bin-pack/sort strategies, eligibility thresholds, minimum inputs, maximum group size, target size, output bounds, filtering, concurrency, partial-progress commits, job ordering, delete handling, dangling-delete cleanup, rewrite result metrics, retry semantics, and cache invalidation.

Retrieve merge-on-read specifics: base-file/file-group identity, delta/log blocks, ordering/precombine rules, delete representation, compaction plan/instant, inline versus asynchronous execution, pending plans, read-optimized versus snapshot readers, and cleaning dependencies.

Retrieve concurrency: active append/update/delete/merge jobs, conflict validation, lock provider where required, plan scheduling ownership, stale-plan behavior, commit retry identity, maximum job duration, streaming checkpoints, reader ages, and maintenance overlap.

Retrieve cost/capacity: object request prices/quotas, read/write bytes, temporary storage, shuffle/network, compute, catalog calls, commit rate, peak ingestion/query reservations, maintenance window, carbon or budget constraints, and incident opportunity cost.

Retrieve governance: sensitive column/path exposure, encryption/key rotation, regional placement, retention/legal holds, privacy erasure, audit evidence, change approval, access for compactor principal, and cleanup authority.

Distinguish data-file count from manifest count; file bytes from in-memory row bytes; partitioning from task distribution; bin packing from clustering; data-file compaction from merge/log compaction; current replacement from physical deletion; snapshot input from object listing; correctness from performance; planned target from actual output; and full atomic completion from explicitly bounded partial progress.

Create a compaction contract:

| Concern | Required decision and evidence |
|---|---|
| Objective | Planning, request, scan, merge-log, update, or storage problem and quantified SLO |
| Eligibility | Snapshot, partitions/specs, size/age/delete thresholds, exclusions, minimum benefit |
| Semantics | Schema, partition, sort, key, null/default, delete/log, sequence and change-feed rules |
| Packing | Target/min/max bytes, group cap, row groups, compression estimate, skew handling |
| Concurrency | Pinned base, exact inputs, conflict validation, locks/fences, retry and partial progress |
| Publication | Isolated outputs, validation, atomic replacements, commit identity and result metrics |
| Lifecycle | Historical reachability, rollback, stream/reader horizon, cleanup and orphan handling |
| Economics | Rewrite bytes/compute/requests/storage versus measured future savings and horizon |
| Operations | Capacity, schedule, timeout, alerts, ownership, runbook and recovery drill |

Write a falsifiable claim: “Run 451 pins snapshot 918 and selects 38,420 files below 96 MiB in specs 4/7 across partitions older than two hours; delete-aware bin packing targets 512 MiB with 384–640 MiB acceptance and 2 TiB group caps; 64 rewrite groups preserve ordered key/value multiplicity, schema IDs, partition tuples, sequence applicability, nulls, totals, and control digests; exact-input conflict validation rejects changed groups; 38,420 inputs become 4,830 outputs in four atomic partial-progress commits; p95 planning falls 41%, GET requests fall 72%, and break-even is 11 days; old files remain through the 30-day snapshot/stream horizon before reachability-based cleanup.”

## Learning Objectives

After completing this module, you should be able to:

1. explain the fixed and variable costs that make small files harmful;
2. diagnose whether fragmentation comes from cadence, partition fan-out, skew, mutations, failure, or writer configuration;
3. distinguish data-file bin packing, merge-on-read compaction, log compaction, manifest compaction, and clustering;
4. choose evidence-based target sizes and eligibility thresholds rather than universal constants;
5. design delete-, schema-, partition-, and sequence-correct rewrite groups;
6. execute isolated, pinned, conflict-safe, atomic replacements with controlled partial progress;
7. preserve historical snapshots and clean old or orphan files only after reachability horizons;
8. model rewrite amplification, temporary storage, future savings, and break-even;
9. prevent small files at write time without violating freshness and ingestion SLOs; and
10. validate logical equivalence and operate compaction with metrics, alerts, runbooks, and drills.

## Core Exposition

### Define small relative to the system

No byte value is universally small. Efficient size depends on object-store latency, format/footer overhead, compression, row-group size, query selectivity, split planning, compute parallelism, network throughput, update frequency, and failure recovery.

A 32 MiB file may be healthy for a low-volume hourly partition and pathological in a multi-petabyte scan. A 2 GiB file may scan efficiently but make selective copy-on-write updates and failed-task retries expensive. Define an acceptable band rather than one exact target.

Measure fragmentation two ways. Count fraction

$$
SmallCountFraction=\frac{|\{f:size(f)<L\}|}{|F|}
$$

reveals control-plane burden. Byte fraction

$$
SmallByteFraction=\frac{\sum_{f:size(f)<L}size(f)}{\sum_{f\in F}size(f)}
$$

reveals how much data must be rewritten. Thousands of tiny files can dominate count but represent few bytes, making compaction cheap and valuable.

Segment by partition, spec, age, and workload. Global percentiles can hide one hot partition producing nearly all fragmentation.

### Diagnose production before repairing symptoms

Low input volume per commit naturally yields small files. Shorter micro-batches improve freshness while increasing file rate. The sustainable cadence must balance freshness with downstream overhead or use automatic accumulation/compaction.

Partition fan-out is common. If 200 tasks each touch 100 partitions, a single batch can attempt 20,000 files. Distribute or sort by partition before writing, limit simultaneous destinations, or revisit over-granular partition design.

Skew produces a few full outputs and a long tail of tiny outputs. Track bytes per writer destination and task, not only average file size. Adaptive coalescing can help, but engine behavior and target file properties must be tested.

Updates and merges fragment files because small changed regions can cause replacement files, new delete artifacts, or per-partition outputs. Late data repeatedly touches cold partitions. Compaction cadence should account for a settling delay so it does not rewrite a partition after every late record.

Failures, retries, and speculative tasks should not make uncommitted candidates live, but poorly integrated pipelines may commit fragmented batches. Diagnose commit lineage and writer versions before buying endless repair compute.

### Choose target size from constraints

Start with the desired scan split and row-group structure. A target file should contain enough row groups for useful statistics and sequential I/O while remaining divisible across expected parallelism. Encoded file target must account for compression; a 512 MiB in-memory partition is not necessarily a 512 MiB object.

Set minimum $L$, target $T$, and maximum $U$. Writers roll near $T$ but accept $[L,U]$ because boundaries, skew, and record indivisibility prevent exact sizes. One record can exceed $U$; define quarantine or oversized-record behavior.

Estimate outputs for group bytes $B$:

$$
n_{out}=\max\left(1,\left\lceil\frac{B}{T}\right\rceil\right),\qquad target_{group}=\frac{B}{n_{out}}.
$$

If $target_{group}<L$, combine more eligible inputs where partition/spec semantics allow. If group size exceeds retry or memory limits, split it even if packing becomes less efficient.

Use sampled rewrites to calibrate encoded output under real schema, compression, and sort behavior. Recalibrate when row width or codec changes.

### Plan eligible rewrite groups

Pin an immutable snapshot. Select live data files using metadata predicates: partition, spec, size below threshold, age, delete count, and perhaps files above a maximum that need splitting. Exclude files in protected operations, corrupt/quarantined scopes, active migration, or unsupported specs.

Require minimum benefit. Rewriting one 90 MiB and one 100 MiB file into one 190 MiB file may help little if $T=512$ MiB and new writes will soon fill the partition. Prefer partitions with high file count, sustained query cost, or stable/cold data.

Group only files that can legally share outputs. All records in one output must satisfy one partition tuple/spec. Schema projection and delete semantics must be valid. Encryption, residency, tenant isolation, or sort requirements may further restrict grouping.

Bin packing is an optimization problem; exact optimum is often unnecessary. First-fit decreasing is a practical heuristic: order by descending size and place each input in the first group that stays under capacity. Production writers often repartition rows rather than concatenate files, so output count/size is estimated rather than equal to file-bin arithmetic.

Record plan ID, base snapshot, exact input file IDs and digests, expected bytes/rows/deletes, group membership, target settings, engine/runtime, and expiration. A plan is evidence and retry identity.

### Preserve deletes, updates, and sequences

Visible rows are not necessarily raw rows. Position deletes address positions in a particular data file; after rewriting, positions and paths change. The compactor must apply them or produce correctly translated delete artifacts. Carrying an old position delete to a new file is invalid.

Equality deletes or deletion vectors have format-specific scope and sequence rules. An equality delete may need to remain if it should also apply to other data files, while a fully materialized delete effect may permit safe removal only through a format-aware action.

Merge-on-read tables add log records to a base file slice. Compaction merges them using the table's record-key, ordering/precombine, tombstone, and timeline rules. Reading only the base file resurrects or loses updates. Snapshot and read-optimized views can differ before compaction; define which relation the operation materializes.

The invariant is

$$
VisibleRows(inputs,deletes,logs)=VisibleRows(outputs,remaining\ deletes,remaining\ logs).
$$

Validate stable key multiplicity and values, not merely counts. Ensure change feeds or incremental consumers treat layout-only actions correctly under the format; misuse of a `dataChange=false`-like marker for an actual logical change can corrupt downstream state.

### Publish through table metadata

Write candidates to isolated object keys. Close and validate every output: format footer, schema/field IDs, partition tuple, spec ID, row groups, statistics, record count, size, checksum, encryption, and sampled/full logical controls.

Commit one rewrite group by atomically removing exact inputs and adding outputs. The old files remain physical for historical snapshots. A directory rename or overwrite is not equivalent because readers may observe partial movement and transactional metadata will not describe it.

Optimistic validation asks whether every input is still live and whether concurrent operations conflict with the rewrite scope. Disjoint appends may be compatible. An update/delete/rewrite of an input is not. Re-plan the affected group from the new snapshot rather than forcing stale candidates.

The successful commit receives new snapshot/version/sequence identity. Outputs must inherit or receive sequence semantics required to avoid making old delete files apply incorrectly or cease applying incorrectly. Use the table format's rewrite operation, not a home-grown file-set edit.

### Bound partial progress

One atomic commit for a huge rewrite provides simple all-or-nothing semantics but increases conflict scope, commit size, retry waste, and elapsed time. Partial progress divides work into independently validated groups or batches and publishes successful subsets.

Partial progress is acceptable when each commit preserves the full table relation, progress is idempotently recorded, failed groups remain safely old, and readers support the resulting mixed layout. Set maximum commits and concurrency to protect catalogs and snapshot growth.

Never call partial output success silently. Report planned, attempted, rewritten, failed, skipped, and conflicted input files/bytes; added outputs; commits; and remaining debt. A run with 90% bytes complete may leave the hottest 10% unresolved.

Retries use group identity and current input liveness. Candidate files from failed attempts are not reused unless their provenance and inputs remain exactly valid. Otherwise they become cleanup candidates only after the active-operation horizon.

### Separate maintenance categories

Data-file bin packing reduces data objects and aims primarily at size. Sorting or Z-ordering also changes locality/statistics; DE-068 treats its query-design trade-offs. A size rewrite may incidentally reorder rows, but it should not claim a stable clustering benefit without contract and evidence.

Manifest compaction rewrites metadata files so planning touches fewer manifests and their ranges align better. It does not make data files larger. Transaction-log/checkpoint or log-compaction operations reduce metadata replay under their own protocols.

Merge-on-read compaction merges row-oriented update logs into columnar base files. Hudi distinguishes that from clustering, which can combine small file groups and change sort layout. The correct name matters because readers, concurrency, scheduling, and incremental-change behavior differ.

Track each debt separately: data-file count/bytes, manifest count/bytes, log actions since checkpoint, delta-log blocks per file group, delete-file ratio, and clustering quality. Do not trigger the wrong rewrite because dashboards collapse everything into `small_files`.

### Prevent small files while writing

Increase micro-batch interval or accumulate input when freshness allows. Reduce unnecessary partition cardinality. Repartition/distribute by table partitions so fewer tasks write each destination. Choose shuffle parallelism from bytes and target size rather than cluster cores alone.

Use adaptive or optimized writers where supported; retrieve exact engine behavior. Write-time binning can combine small inputs within a partition. Auto compaction can run after successful writes. Both add shuffle, latency, memory, and coupling to the ingestion cluster.

Avoid unconditional `coalesce(1)`. It serializes output, can create oversized files, and collapses parallelism. Likewise, a fixed `repartition(200)` produces too many files for small batches and too few for huge ones. Estimate from bytes by partition and cap with operational constraints.

Target size is a soft outcome. Observe actual encoded file distribution after every writer/runtime/schema change. A prevention policy is successful when it lowers ongoing debt without missing freshness, throughput, memory, or failure-recovery SLOs.

### Schedule maintenance economically

Estimate one run's cost:

$$
C_{rewrite}=C_{read}(B)+C_{shuffle}(B)+C_{write}(B')+C_{requests}+C_{temporary}+C_{conflict}+C_{operations}.
$$

Estimate daily savings across query, planning, metadata, requests, merges, and future maintenance. Break-even days are

$$
D_{break}=\frac{C_{rewrite}}{Savings_{daily}}.
$$

Use measured workload cohorts and sensitivity ranges. Savings decay or grow with table traffic and new file production. Include temporary double storage until old snapshots expire.

Prioritize partitions by expected net present benefit, SLO breach, file-count pressure, and stability. Avoid compacting the newest hot window repeatedly; delay until late/update rates fall unless current read latency requires it.

Reserve capacity. Inline compaction simplifies orchestration but extends write latency and shares failure fate. Asynchronous/offline services isolate resources and smooth load but require coordination, locks or optimistic concurrency, monitoring, and backlog control.

### Validate logical and operational outcomes

Before commit, compare input-visible and output-visible row count, stable key multiset, duplicate multiplicities, null counts, min/max, domain totals, delete controls, and deterministic sampled/full row digests. Validate schema IDs and meanings, partition tuples/specs, sort declarations, file statistics, encryption, and format readers.

After commit, pin the new snapshot and rerun controls. Query boundary predicates, deleted keys, old/new specs, evolved schemas, time travel, incremental/CDC consumers, and every supported engine. Confirm old snapshot remains readable through policy.

Measure file-count reduction, size percentiles, manifest/planning time, files/requests/bytes scanned, task duration/skew, query latency, update latency, and cost. Compare against a pre-run cohort; cache warmth and concurrent workload can confound a single benchmark.

Compaction can worsen selective queries if it mixes previously localized values and broadens min/max statistics. File-size success does not imply data-skipping success. DE-068 develops clustering choices for that case.

### Clean only after reachability expires

The commit logically removes inputs from the new snapshot. Retained old snapshots, branches/tags/savepoints, long readers, lagging streams, rollback, backup, legal holds, and concurrent work can still require their physical bytes.

Use format-aware snapshot expiration, vacuum, cleaning, and orphan removal. Configure retention longer than the maximum active operation and promised historical horizon. Very short orphan retention can delete candidates belonging to an in-flight writer.

Distinguish replaced files from failed candidate files. Both may eventually be unreachable, but reachability proof and minimum age remain required. Never delete by filename prefix, job date, or absence from current snapshot alone.

Verify cleanup metrics and current/historical reads. Record files/bytes deleted, protected, missing, failed, and deferred; snapshot/reference decisions; key handling; and recovery evidence.

### Operate with feedback and ownership

Dashboards should segment by table, partition, spec, writer, and commit age. Track file counts and bytes; size percentiles; small/large count and byte fractions; files per GiB; files per commit; manifest/log/delete counts; planning and scan costs; compaction backlog and age; rewrite throughput/amplification; conflicts; partial failures; temporary storage; cleanup lag; and break-even realization.

Alert on explosive file-rate change, empty files, p50 below the lower band, excessive oversized files, partition fan-out, skew, backlog age, compaction failure loops, unknown plan/input, high conflict waste, cleanup inside active horizons, logical-control divergence, or missing old-snapshot files.

Ownership spans producers, table product, platform maintenance, catalog, storage, security, and governance. Producers own prevention signals. The table owner defines logical correctness and service priorities. Platform owns safe mechanics/capacity. Governance owns retention/holds. One runbook names decision and rollback authority.

## Definitions and Notation

Let $F_S$ be active data files in snapshot $S$. For file $f$, $b(f)$ is encoded bytes, $r(f)$ raw rows, $p(f)$ partition/spec identity, and $d_S(f)$ applicable deletes/log semantics.

The visible multiset of a file set $I$ is

$$
V_S(I)=\mathcal{M}\left(Apply\left(\bigcup_{f\in I}r(f),\{d_S(f):f\in I\}\right)\right).
$$

A rewrite group $g=(I_g,O_g,base,policy)$ is valid when inputs are live, outputs are format-valid, and $V_{base}(I_g)=V_{candidate}(O_g)$ under declared projection.

File-count reduction is $\Delta N=|I|-|O|$. Rewrite byte amplification can be recorded as

$$
A_B=\frac{bytes_{read}+bytes_{written}}{bytes_{logical\ output}}.
$$

For a layout-only full rewrite of compressed bytes with similar encoding, $A_B$ is often near 2 before shuffle/temporary overhead, but deletes, codec changes, and compression ratio alter it.

Files per GiB is $N/(B/2^{30})$ for $B>0$. Planning cost can be modeled empirically as $C_{plan}=\alpha M+\beta N+\gamma$, where $M$ is metadata units and coefficients come from measurement, not assumption.

Debt priority for partition $p$ may be

$$
Priority(p)=ExpectedSavings(p)-RewriteCost(p)-RiskCost(p),
$$

subject to correctness, capacity, retention, and SLO constraints.

## Mechanisms, Invariants, or Proof Structure

Proof sketch for atomic compaction transparency:

1. Pin base snapshot $S$ and choose exact live inputs $I$.
2. Read those inputs under $S$'s schema, partition, sequence, delete, and log semantics to obtain visible multiset $V_S(I)$.
3. Write isolated outputs $O$ and verify $V(O)=V_S(I)$ plus required metadata invariants.
4. Before commit, validate every input in $I$ is still live and no conflicting operation invalidates the semantic scope.
5. Atomically publish $S'$ with files $(F_S\setminus I)\cup O$; readers can observe $S$ or $S'$, not a partially replaced group.
6. Files outside $I$ are identical in both snapshots, and outputs represent exactly the visible rows removed with $I$.
7. Therefore $V(S')=V(S)$ as a multiset under the declared schema/delete semantics.
8. Retaining old inputs while $S$ is protected preserves historical readers without adding them to $S'$.

The proof does not establish performance benefit, bitwise file identity, stable physical row order, or correctness if the compactor bypasses table-format delete/sequence rules. Partial progress applies the proof independently to each committed group.

The executable demonstrates deterministic first-fit-decreasing packing and logical preservation after applying a key delete. Sizes are abstract encoded units; it is not an implementation of Iceberg, Delta Lake, Hudi, Parquet, delete files, object stores, or a distributed writer.

<!-- bijux-verify: {"id":"small-file-bin-packing","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input_files=5\ninput_bytes=170\ngroups=(('f5', 'f3'), ('f4', 'f2', 'f1'))\noutput_sizes=(100, 70)\noutput_files=2\nfile_reduction=3\nvisible_before=(('a', 10), ('c', 30), ('d', 40), ('e', 50), ('f', 60))\nvisible_after=(('a', 10), ('c', 30), ('d', 40), ('e', 50), ('f', 60))\ndeleted_key_absent=True\nlogical_rows_preserved=True\n","stderr":""}} -->
```python
files = {
    "f1": (10, (("a", 10), ("b", 20))),
    "f2": (20, (("c", 30),)),
    "f3": (30, (("d", 40),)),
    "f4": (40, (("e", 50),)),
    "f5": (70, (("f", 60),)),
}
deleted_keys = {"b"}
target = 100


def pack(file_map):
    groups = []
    for name in sorted(file_map, key=lambda item: (-file_map[item][0], item)):
        size = file_map[name][0]
        placed = False
        for group in groups:
            if group[0] + size <= target:
                group[0] += size
                group[1].append(name)
                placed = True
                break
        if not placed:
            groups.append([size, [name]])
    return tuple((size, tuple(names)) for size, names in groups)


def visible(rows):
    return tuple(sorted(row for row in rows if row[0] not in deleted_keys))


packed = pack(files)
groups = tuple(names for _, names in packed)
before = visible(row for _, rows in files.values() for row in rows)
output_rows = tuple(
    visible(row for name in names for row in files[name][1])
    for _, names in packed
)
after = tuple(sorted(row for rows in output_rows for row in rows))

print(f"input_files={len(files)}")
print(f"input_bytes={sum(size for size, _ in files.values())}")
print(f"groups={groups}")
print(f"output_sizes={tuple(size for size, _ in packed)}")
print(f"output_files={len(packed)}")
print(f"file_reduction={len(files) - len(packed)}")
print(f"visible_before={before}")
print(f"visible_after={after}")
print(f"deleted_key_absent={all(key != 'b' for key, _ in after)}")
print(f"logical_rows_preserved={before == after}")
```

The model packs physical bytes independently of visible row count, then materializes the deletion while rewriting. Production formats may retain or translate delete artifacts instead. The important property is visible-relation equality, not this teaching implementation's chosen mechanism.

## Alternatives and Trade-Offs

**Write-time sizing versus background compaction.** Write-time sizing prevents debt and makes fresh data efficient, but adds shuffle/latency to ingestion. Background compaction preserves low-latency writes but leaves a performance window and consumes separate capacity.

**Inline versus asynchronous maintenance.** Inline operation is simple and immediately bounds debt but couples write success/latency to maintenance. Async operation isolates latency and scales independently but needs coordination, backlog alerts, and concurrency control.

**Bin packing versus clustering.** Bin packing targets size with relatively low shuffle. Clustering targets locality and pruning, potentially yielding larger benefits at greater rewrite cost and sensitivity to workload drift.

**Large versus small targets.** Large files reduce fixed overhead and metadata but limit parallelism and enlarge update/retry units. Small files improve parallelism and selective mutation but increase opens, tasks, requests, and metadata.

**One atomic run versus partial progress.** One commit simplifies audit and rollback but magnifies conflict and retry cost. Partial progress bounds failures but creates more snapshots and demands exact per-group accounting.

**Hot-window versus cold-window compaction.** Hot compaction improves current reads but conflicts and re-rewrites frequently. Cold compaction is stable and cheap but leaves recent queries fragmented.

**Byte-based versus row-based sizing.** Bytes track I/O/object behavior; rows can stabilize tuple-balanced clustering. Variable-width records make either an imperfect proxy for the other, so measure both.

**Append accumulation versus freshness.** Longer batches create healthier files but delay visibility. Low-latency commits need adaptive write sizing or prompt background repair.

**Rewrite deletes into data versus retain delete artifacts.** Materializing deletes can speed reads and remove dangling artifacts but increases rewrite work and must honor sequences. Retention avoids work but keeps merge cost.

**Compaction filter versus full-table rewrite.** Narrow predicates reduce cost/conflicts and prioritize debt. Full rewrites can normalize everything but often waste resources and contend with production.

**Fixed schedule versus threshold/economic trigger.** Cron is predictable but can run uselessly or miss bursts. Measured triggers adapt to debt, though they need robust metrics, hysteresis, and capacity arbitration.

**Historical retention versus rapid cleanup.** Retention preserves time travel/readers/rollback at temporary storage cost. Early cleanup saves bytes but can irreversibly break active and historical reads.

## Failure Modes and Misconceptions

1. **“Anything below 128 MiB is bad.”** Efficient size is workload, format, engine, storage, and mutation dependent.
2. **“Average file size is enough.”** Long tails and partition hotspots disappear in a global mean.
3. **“Fewer files always wins.”** Oversized files reduce parallelism and increase retry/update cost.
4. **“Row count predicts bytes.”** Variable-width values and compression can differ drastically.
5. **“Target size is exact.”** Encoded output varies with rows, codec, grouping, and writer behavior.
6. **“Compaction fixes partitioning.”** It cannot repair an unsuitable partition contract unless combined with explicit evolution/rewrite.
7. **“Bin packing improves data skipping.”** It can broaden bounds unless locality is intentionally preserved or improved.
8. **“Clustering is just compaction.”** It changes layout locality and has distinct costs and evidence.
9. **“Manifest rewrite compacts data.”** It reduces metadata artifacts, not data file sizes.
10. **“Merge-on-read compaction is concatenation.”** It must merge logs, ordering, updates, and tombstones.
11. **“Raw base files equal visible rows.”** Deletes/logs can change the logical relation.
12. **“Position deletes survive file replacement unchanged.”** Their file/position targets no longer match.
13. **“A data-preserving flag makes it true.”** Mislabeling a changed rewrite corrupts incremental consumers.
14. **“Read latest throughout the job.”** The source can fracture across commits.
15. **“Stale inputs can be force-committed.”** Concurrent updates make candidate outputs obsolete.
16. **“Retries may reuse any completed candidates.”** Their exact input snapshot and semantics must still be valid.
17. **“Partial progress means best effort.”** Each published group must independently preserve the table.
18. **“Ninety percent complete is success.”** Failed files may contain the hottest or most dangerous debt.
19. **“Delete old inputs after commit.”** Retained snapshots and active readers may still need them.
20. **“Not current means orphan.”** Protected history or in-flight writers can reference the object.
21. **“Inline compaction is free.”** It consumes writer latency, memory, shuffle, and failure budget.
22. **“coalesce(1) solves small files.”** It serializes work and can create an oversized bottleneck.
23. **“Fixed shuffle partitions fit every batch.”** Volume and fan-out vary over time.
24. **“Cold data never needs compaction.”** Audit and rare scans may still breach cost/SLOs; measure demand.
25. **“File reduction proves value.”** Measure end-to-end latency, requests, bytes, cost, and break-even.
26. **“Compaction can run unowned.”** Conflicts, cleanup, privacy, capacity, and rollback require accountable operators.

## Worked Examples

### Example 1

A stream commits every minute to 24 active partitions, producing 34,560 files/day despite only 600 GiB/day. Increasing trigger interval violates freshness. Optimized write groups rows by partition and an async compactor waits two hours for late arrivals, reducing the steady-state file rate while preserving minute-level visibility.

### Example 2

One partition contains 9,000 files with p50 3 MiB, but those files total only 28 GiB. Count fraction is severe while byte fraction is small. A targeted rewrite is cheap and cuts planning requests substantially; no full-table operation is justified.

### Example 3

Files average 490 MiB against a 512 MiB target, yet an operator schedules hourly compaction. The operation repeatedly rewrites healthy hot files, creates conflicts, and never reaches break-even. Eligibility adds a lower threshold, minimum inputs, settling age, and measured-benefit gate.

### Example 4

A rewrite reads base files but omits equality deletes. Counts rise by 1,204 and previously erased keys return. Publication is blocked. The corrected format-aware action evaluates delete sequence scope and validates an explicit deleted-key control set before commit.

### Example 5

A position delete points to file A row 19. Compaction creates file B with new ordering. Rather than attach the old position delete to B, the job materializes visible rows and lets the table-format action remove the now-dangling delete when safe.

### Example 6

A 20 TiB plan runs while a merge updates one input group. Exact-input validation commits 49 disjoint groups and rejects the conflicted one under bounded partial progress. The rejected group is replanned from the new head; reports distinguish completed bytes from failed hot debt.

### Example 7

Daily partitions contain 20 MiB tail files because each of 200 tasks opens every partition. Sorting/distributing by partition before write lowers concurrent destinations; adaptive task sizing creates fewer, fuller files. Background compaction handles only the unavoidable tails.

### Example 8

A merge-on-read table has few base files but hundreds of log blocks per hot file group. Ordinary bin packing would not solve snapshot merge latency. Log compaction reduces blocks, and full compaction later merges logs into base files; clustering remains a separate locality decision.

### Example 9

Compaction reduces 1,000 files to 100 but mixes customer ranges, broadening file min/max. Full scans improve while selective customer queries regress. The next design preserves range ordering or uses deliberate clustering from DE-068; file size alone was not the complete objective.

### Example 10

After atomic replacement, old inputs double storage for 30 days because audit tags and lagging streams retain them. Cleanup uses snapshot reachability and reader horizons, deletes only unprotected objects, and validates both current and tagged reads. The business case included that temporary storage from the start.

## Cross-Program Connections

- **Algorithms and Data Structures:** bin packing, scheduling, approximation heuristics, histograms, quantiles, hashing, and skew analysis govern grouping and sizing.
- **Database Systems:** pages, extents, LSM compaction, MVCC, vacuum, indexes, delete records, clustering, and cost-based optimization provide close analogies and important differences.
- **Distributed Systems:** immutable files, optimistic concurrency, atomic commits, idempotent retries, partial progress, locks, leases, and consistent snapshots make rewrites safe.
- **Operating Systems:** sequential versus random I/O, page cache, file descriptors, read-ahead, scheduling, and memory pressure explain local file-size effects.
- **Cloud Engineering:** object request pricing/limits, multipart writes, temporary capacity, lifecycle rules, catalogs, autoscaling, and regional bandwidth shape economics.
- **Reliability Engineering:** backlogs, SLOs, capacity reservations, canaries, fault injection, runbooks, rollback, and cleanup drills turn maintenance into a service.
- **Software Engineering:** immutable artifacts, transaction boundaries, content identity, separation of concerns, feature flags, and contract tests structure compactor design.
- **Formal Methods:** multiset equivalence, refinement, invariants, preconditions, conflict validation, and proof composition support layout transparency.
- **Security Engineering:** compactor privileges, encryption keys, object reachability, audit trails, supply-chain identity, and destructive cleanup need least privilege.
- **Privacy Engineering:** delete preservation, historical reachability, erasure verification, legal holds, metadata exposure, and retention constrain physical optimization.
- **Platform Engineering:** shared scheduling, quotas, noisy-neighbor isolation, golden configurations, observability, self-service controls, and ownership govern fleet scale.
- **Finance and Sustainability:** break-even, discounted savings, opportunity cost, temporary storage, network use, and waste avoidance make optimization accountable.

## References

1. Apache Iceberg. [Table specification](https://iceberg.apache.org/spec/). Accessed 2026-09-03. Primary specification for snapshots, data/delete files, sequence numbers, manifests, rewrite validation, optimistic commits, and retention semantics.
2. Apache Iceberg. [Spark procedures](https://iceberg.apache.org/docs/latest/spark-procedures/). Accessed 2026-09-03. Primary engine documentation for `rewrite_data_files`, bin-pack/sort strategies, sizing, filters, concurrency, partial progress, output metrics, deletes, and manifest rewrites.
3. Apache Iceberg. [Maintenance](https://iceberg.apache.org/docs/latest/maintenance/). Accessed 2026-09-03. Primary documentation for data-file compaction, snapshot expiration, metadata cleanup, and orphan-file safety.
4. Apache Iceberg. [Structured Streaming](https://iceberg.apache.org/docs/latest/spark-structured-streaming/). Accessed 2026-09-03. Primary documentation linking frequent streaming commits to small files, compaction, manifest rewrite, and snapshot maintenance.
5. Apache Iceberg. [Reliability](https://iceberg.apache.org/docs/latest/reliability/). Accessed 2026-09-03. Primary documentation for atomic metadata operations, reader isolation, optimistic concurrency, and safe retries.
6. Delta Lake. [Optimizations](https://docs.delta.io/optimizations-oss/). Accessed 2026-09-03. Primary documentation for bin-packing compaction, idempotence scope, snapshot-isolated readers, auto compaction, optimized writes, metrics, and clustering distinctions.
7. Delta Lake. [Best practices](https://docs.delta.io/best-practices/). Accessed 2026-09-03. Primary documentation for small-file effects, repartition-based compaction, partition-scoped replacement, and the danger of misusing no-data-change markers.
8. Delta Lake. [Concurrency control](https://docs.delta.io/concurrency-control/). Accessed 2026-09-03. Primary documentation for compaction concurrency, read/write conflicts, partitions, and transaction behavior.
9. Delta Lake. [Table utility commands](https://docs.delta.io/delta-utility/). Accessed 2026-09-03. Primary documentation for optimize history metrics, vacuum, retention, old files, active operations, and restore implications.
10. Apache Hudi. [Compaction](https://hudi.apache.org/docs/compaction/). Accessed 2026-09-03. Primary documentation for merge-on-read base/log compaction, inline/asynchronous/offline scheduling, coordination, and log compaction.
11. Apache Hudi. [Clustering](https://hudi.apache.org/docs/clustering/). Accessed 2026-09-03. Primary documentation distinguishing compaction from clustering and covering small-file plans, groups, target sizes, sorting, concurrency, and replace commits.
12. Apache Hudi. [Technical specification](https://hudi.apache.org/learn/tech-specs/). Accessed 2026-09-03. Primary specification for file groups/slices, timeline actions, compaction, log compaction, clustering, cleaning, and snapshot isolation.
13. Apache Hudi. [Write operations](https://hudi.apache.org/docs/write_operations/). Accessed 2026-09-03. Primary documentation for write-path file sizing, atomic commit, cleaning, compaction, and archival stages.

## Exercises

### Exercise 1

A 60 TiB table receives 1 TiB/day in five-minute batches across 120 active partitions. Its file-size p50 is 18 MiB, p95 190 MiB, target 512 MiB, and late updates continue for 48 hours. Diagnose causes and design prevention plus a compaction eligibility, grouping, scheduling, and success policy.

### Exercise 2

Design a delete-correct compaction for files affected by position deletes, equality deletes, and concurrent merges. Specify pinned state, visible relation, sequence rules, outputs, conflict validation, logical checks, commit, historical retention, and cleanup.

### Exercise 3

Compare one-commit and partial-progress execution for a 500 TiB backlog with a four-hour maintenance window, high update conflicts in the newest 5%, and strict catalog commit limits. Choose a design and define idempotency, retry, reporting, and rollback.

### Exercise 4

Construct an economic break-even model using rewrite read/write/shuffle compute, object requests, temporary 30-day storage, conflict waste, planning savings, scan savings, and workload growth. State which measurements would cause you to cancel a proposed rewrite.

### Exercise 5

A team says one “compaction” service should handle tiny Parquet files, excess manifests, merge-on-read log blocks, and poor customer-range pruning. Decompose the work into correct maintenance categories with separate triggers, invariants, metrics, and interactions.

## Answers to the Exercises

### Answer 1

The low median with broad tail suggests batch volume divided across many partitions/tasks plus skew; retrieve files per commit/task/partition, distribution, shuffle, late routing, row width, and failures. Preserve five-minute visibility, but distribute/sort by partition, size writer tasks from bytes, cap open destinations, and test optimized/adaptive writes. Async compaction excludes the newest 48-hour correction window unless SLOs demand otherwise, selects same-spec/partition files below a calibrated lower band, requires multiple inputs and positive measured benefit, targets 512 MiB within an accepted range, caps group bytes/retry duration, and prioritizes high count/request cost. It pins a snapshot, validates deletes and exact inputs, commits groups atomically, and retains old files. Success requires logical equality plus improved size percentiles, files/GiB, planning, requests, query latency, bounded conflict rate, freshness, and actual break-even—not target-size appearance alone.

### Answer 2

Pin table/snapshot/schema/spec and enumerate exact data and delete artifacts with sequence applicability. Compute $V_S(I)$ through the format reader: apply position deletes to their original file positions, equality deletes only to eligible data sequences, and every merged update/tombstone. Write isolated correctly partitioned outputs; either materialize delete effects or retain/translate delete artifacts exactly as the format permits. Validate stable-key multiset, duplicate counts, values, nulls, domain totals, deleted-key absence, schema/spec/stats, and candidate readability. At commit, require every input still live and reject/replan groups touched by concurrent merges/deletes. Atomically remove inputs/add outputs with correct new sequence metadata. Keep old inputs/deletes while retained snapshots/readers need them, then expire/clean through authoritative reachability and verify current plus protected historical reads.

### Answer 3

One 500 TiB commit is unlikely to fit four hours and magnifies retry/conflict/catalog risk. Divide the pinned plan into bounded independent groups, process stable 95% first, throttle concurrent rewrites and commits below catalog limits, and leave the hot 5% until settled or use smaller conflict windows. Each group has deterministic plan/input identity, isolated candidates, full logical validation, exact-input conflict checks, and one atomic commit. A retry checks whether the group already committed, whether inputs remain live, and otherwise replans; it never blindly reuses candidates. Cap total partial commits and snapshot growth. Report planned/attempted/completed/conflicted/failed/skipped files and bytes plus remaining debt and benefit by partition. Rollback points to prior snapshots per commit; mixed old/new layout remains logically equivalent, while cleanup waits through the shared retention horizon.

### Answer 4

Measure source bytes and requests, shuffle/network/compute time and price, encoded output, candidate failures, operator time, and temporary old-plus-new byte-days. Estimate conflict probability and wasted group work. From representative query cohorts, measure daily reductions in metadata planning, object requests, scanned bytes, task overhead, merge cost, and incident/SLO exposure; project workload and new-file production with ranges. Compute break-even and discounted savings before the layout becomes fragmented again or data expires. Cancel or narrow the rewrite if logical validation is uncertain, predicted savings are below cost, break-even exceeds useful data/layout lifetime, healthy files dominate inputs, hot conflicts consume the window, temporary storage violates quota, compaction starves higher-value work, or canary queries show worse pruning/latency despite fewer files.

### Answer 5

Use data-file bin packing for tiny Parquet objects, triggered by size/count/age and validated by visible-row equality plus file-cost improvements. Use manifest rewrite for excess manifest metadata, triggered by planning/manifest metrics and validated by identical file membership plus lower planning work. Use merge/log compaction for merge-on-read file slices, triggered by delta commits/log bytes/blocks and validated by record-key ordering, updates, tombstones, and snapshot/read-optimized semantics. Use deliberate range clustering for customer pruning, triggered by scan-to-return/statistics overlap and validated by logical equality plus bounds/pruning gains; it belongs to DE-068. Coordinate capacity and snapshot conflicts, avoid rewriting the same hot files concurrently, preserve historical reachability, and report separate backlogs so success in one category cannot mask failure in another.
