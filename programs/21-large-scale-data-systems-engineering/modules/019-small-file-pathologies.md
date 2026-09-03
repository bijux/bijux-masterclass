---
module_id: LSDS-019
program: Large-Scale Data Systems Engineering
level: 1
module_number: 19
title: Small-File Pathologies
status: complete
last_verified: 2026-09-03
---

# Small-File Pathologies

## One-Page Review

### Governing question

Why can a dataset with modest payload become expensive or slow when divided into many small files, and how can engineers prevent or repair the pathology without breaking visibility, concurrency, provenance, retention, or recovery?

### Essential definitions

- A **small file** is a file whose fixed metadata, open, planning, scheduling, and commit costs dominate useful transfer/compute for the target workload; it has no universal byte threshold.
- **Metadata amplification** is the growth of namespace, block, manifest, catalog, statistics, and lineage records per payload byte.
- **open cost** is fixed work to discover, authorize, locate, open, and initialize decoding for a file before useful sequential reading.
- A **split** is one schedulable input range; a file can create one or many splits depending on format and compression.
- **rolling policy** decides when a writer closes its current file by size, time, inactivity, checkpoint, or record count.
- **compaction** rewrites several valid input files into fewer output files while preserving a declared logical dataset.
- **bin packing** groups inputs into bounded output-size targets without necessarily improving data clustering.
- **write amplification** is bytes written or rewritten divided by logical new/changed bytes.
- A **table snapshot/manifest commit** atomically changes visible file membership without requiring atomic multi-file rename.

### Central model, mechanism, or theorem

For total payload `B` in `F` files, a first-order read-cost model is `B/r + F*(l_open + c_plan + c_sched)`, plus metadata/index work and format decoding. Reducing average file size while holding `B` constant increases `F`, so fixed per-file terms eventually dominate. The correct target size depends on query selectivity, splitability, storage request latency/cost, scheduler capacity, writer memory, partition skew, recovery granularity, and freshness objectives.

Safe compaction reads an immutable input snapshot, writes uniquely named outputs, validates row/byte/domain invariants, then conditionally commits a new manifest that removes exact input versions and adds exact output versions. Readers use either old or new snapshot membership. Physical input deletion follows retention and reachability rules later; output creation alone does not authorize it.

### Critical invariants

- File-size policy is derived from measured end-to-end workload costs, not folklore.
- Payload bytes, file count, block/row-group count, table-manifest count, and partition count are measured separately.
- Writer parallelism, rolling triggers, checkpoint cadence, and partition cardinality have bounded product.
- Files are immutable after publication; membership changes through a versioned manifest or equivalent transaction.
- Compaction binds exact input versions and rejects concurrent membership conflicts.
- Output preserves schema, rows, ordering promises, partition values, delete semantics, checksums, encryption, provenance, and statistics.
- Readers never infer committed membership from a temporary/output prefix alone.
- Old files remain protected while any retained snapshot, lease, clone, backup, or legal hold references them.
- Compaction backlog, rewrite bytes, query benefit, failures, and orphan cleanup are observable.

### Common failures

Frequent failures are defining “small” by one universal size, blaming object storage capacity rather than per-object work, equating files with compute partitions, creating one file per event/tenant/minute, multiplying sink parallelism by partitions and checkpoints, compacting across incompatible schemas or security domains, publishing outputs before validation, deleting inputs before manifest commit, retrying with reused output names, ignoring equality/position deletes, compacting hot partitions continuously, retaining every table snapshot forever, and optimizing scan throughput while making selective reads, freshness, recovery, or governance worse.

### Compact example

One TiB stored as 1-MiB files requires 1,048,576 objects; at 256 MiB it requires 4,096, a 256-fold reduction. With a modeled 8-ms serial open cost, fixed open time falls from about 8,388.6 seconds to 32.8 seconds before reading any payload. Real readers parallelize and coalesce files, but request, metadata, planning, footer, credential, and task costs do not vanish. The example motivates measurement rather than declaring 256 MiB universally optimal.

### Connections

[LSDS-012](012-metadata-servers-and-namespace.md) supplies namespace pressure. [LSDS-014](014-read-and-write-pipelines.md) supplies throughput and backpressure. [LSDS-018](018-consistency-of-listings-and-metadata.md) supplies discovery and snapshot membership. [LSDS-020](../ROADMAP.md) generalizes storage layout selection.

## Governing Question

Distributed storage can hold billions of objects, but capacity is not the only constraint. Each file has an identity, authorization check, metadata record, list row, open request, block/extent mapping, footer, decoder setup, catalog entry, statistics record, task-planning decision, and lifecycle history. A one-kilobyte object and a one-gigabyte object can incur similar fixed work along several of these paths.

The pathology appears when fixed work dominates useful work. A query may spend minutes listing and planning, launch tens of thousands of tiny tasks, and finish each task before scheduling overhead is amortized. A metadata service can exhaust memory or lock throughput even while data nodes remain mostly empty. An object-store bill can be driven by request count rather than stored bytes.

The cure is not simply “make files large.” Oversized files can reduce parallelism, increase recovery/rewrite units, make selective reads expensive, require large writer buffers, and delay streaming visibility. Unsplittable compression can turn one large file into one straggling task. Highly selective queries may benefit from smaller well-clustered files.

The governing question is how to balance fixed cost, sequential I/O, pruning, parallelism, freshness, recovery, and governance—and how to compact transactionally once the current layout no longer serves that balance.

## Why This Matters

Small files often arise from reasonable local choices. Streaming jobs checkpoint frequently for recovery. Each parallel writer emits files for every active partition. Late data reopens old time buckets. Microservices write one object per request. Dynamic partitioning isolates tenants. Failed attempts leave candidates. A low-volume partition never reaches its size trigger before a time trigger closes it.

These local choices multiply. With `W` writers, `Q` active logical partitions per writer, and `C` successful checkpoints, a loose upper exposure is `W*Q*C` output files when every combination receives data and rolls per checkpoint. Skew, idle partitions, rescaling, retries, and sink semantics change the actual count, but the product reveals why a small checkpoint interval can explode metadata.

Downstream effects cross boundaries. Storage services handle request bursts; metastores and table manifests grow; query coordinators allocate memory; schedulers launch tasks; executors open connections and parse footers; security services authorize requests; encryption key services see more calls; lifecycle engines evaluate more objects; audits and inventories become larger.

Compaction is therefore both a performance optimization and a data-changing workflow. It can reorder rows, rewrite encryption, alter statistics, remove tombstones, affect time travel, and create deletion obligations. Correctness and governance must be designed before automation.

## Prerequisites and Retrieval

Recall horizontal partitioning from [LSDS-002](002-horizontal-partitioning.md), serialization and format boundaries from [LSDS-008](008-serialization-across-workers.md), failure assumptions from [LSDS-009](009-cluster-failure-assumptions.md), and state/work accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md).

Retrieve metadata ownership and snapshots from [LSDS-012](012-metadata-servers-and-namespace.md), read/write pipelines from [LSDS-014](014-read-and-write-pipelines.md), object versions and immutable-manifest publication from [LSDS-016](016-object-storage-semantics.md), multipart commit from [LSDS-017](017-multipart-upload-and-commit.md), and listing/pagination consistency from [LSDS-018](018-consistency-of-listings-and-metadata.md).

You should understand file formats, row groups, compression, partitions, object requests, schedulers, checkpoints, immutable versions, optimistic concurrency, set membership, checksums, tombstones, retention, and garbage collection.

## Learning Objectives

After completing this module, you should be able to:

- define a small file in workload-relative rather than universal terms;
- model fixed per-file costs separately from payload scan cost;
- explain namespace, object request, manifest, planning, scheduling, and decoder amplification;
- distinguish storage files, blocks, row groups, pages, input splits, and tasks;
- diagnose how writer parallelism, partitioning, checkpoints, and rolling policy create files;
- select target size from measured read/write/freshness/recovery constraints;
- design snapshot-safe bin-pack, sort, or clustering compaction;
- preserve schema, delete semantics, provenance, encryption, and statistics;
- publish compacted membership atomically and garbage-collect safely;
- prioritize compaction from cost and benefit rather than file count alone;
- test concurrency, failure, skew, late data, and retention boundaries; and
- quantify whether maintenance reduces total system cost.

## Core Exposition

### There is no universal small-file size

A file is small when fixed cost is material for the workload. On a local NVMe filesystem, metadata lookup may be cheap. Across an object API, one open can include DNS, TLS/session setup, authorization, rate limiting, request latency, and a footer range request. A query engine may assign an open-cost weight larger than the file itself.

Format and access pattern matter. A 16-MiB Parquet file with useful min/max statistics can be efficient for selective reads. The same file can be wasteful in a full-table scan across millions of objects. A 1-GiB gzip file may be operationally “too large” because it is unsplittable.

Define a target interval, not one magic value: minimum useful size, preferred target, and maximum acceptable size. Reevaluate it when storage, engine, compression, query, SLA, or workload distribution changes.

### Fixed and variable cost model

Let file `i` have payload `b_i`. Approximate total scan time as payload transfer/decoding plus fixed work:

`T_scan ~= sum(b_i)/r_effective + F*(l_list + l_open + c_auth + c_footer + c_plan + c_sched) + T_skew`.

Not every term is serial, so this is an accounting model rather than a wall-clock prediction. Parallelism overlaps requests until it encounters coordinator CPU, connection, request-rate, metadata, executor, or downstream limits.

Use measurements from query plans and storage telemetry: listing duration, open/HEAD/GET count, bytes per request, task duration distribution, scheduler delay, footer bytes, metadata memory, decoder time, throttles, and billed operations.

### Namespace and metadata amplification

HDFS-style namespace services maintain per-file and per-block records. More files increase NameNode memory, edit-log traffic, checkpoint/restart work, locks, listings, permission checks, and block reports. Replication multiplies block placement metadata even if small files occupy only one partial block each.

Object stores distribute metadata differently but still meter and execute per-object operations. Billions of tiny objects increase LIST pages, GET/HEAD/PUT/DELETE calls, lifecycle evaluations, inventory rows, replication events, and audit records. Prefix capacity does not make these costs free.

Table formats add snapshots, manifest lists, manifests, data-file entries, delete-file entries, statistics, and sequence numbers. Small data files can create small manifest files too, making planning hierarchical but still expensive.

### File, block, row group, split, and task

A storage file is an object/namespace entry. HDFS blocks or object byte ranges are physical access units. A Parquet file contains row groups and pages. An input format turns files or byte ranges into logical splits. The scheduler turns splits into tasks, sometimes packing many small files together.

Therefore `files != blocks != row groups != tasks`. Coalescing small files into one scan partition reduces task count without reducing file opens, metadata entries, or requests. Splitting a large splittable file increases task parallelism without increasing stored file count.

Compression matters. Splittable columnar formats preserve parallel ranges. Stream compression formats may require reading from the beginning, so combining inputs by concatenation can produce an invalid or poorly splittable result unless the format supports members.

### Read-path pathology

Query planning first discovers files, filters partitions, reads table manifests and file statistics, and creates splits. Millions of candidates can overload a driver/coordinator before executors read data. Planning memory and garbage collection become bottlenecks.

Execution then pays open and authorization cost per file. Tiny tasks have low useful CPU and high launch/serialization overhead. Speculation can duplicate opens. Many concurrent range requests can hit connection pools, request quotas, key-management quotas, or adaptive throttling.

Small row groups also reduce compression and encoding efficiency. Dictionaries, headers, footers, checksums, indexes, and bloom filters consume a larger fraction of bytes. Conversely, row groups too large for memory or pruning create different problems.

### Write-path causes

Distributed writers normally create at least one part file per active writer/partition combination over a commit interval. Excess sink parallelism, high-cardinality dynamic partitions, frequent checkpoints, and small rolling thresholds are multiplicative.

Late and sparse data are especially damaging. A writer receiving a few records for thousands of tenant/day/hour keys can close thousands of tiny files. Repartitioning by a skewed key gives hot writers huge files and cold writers tiny ones.

Retries and speculative attempts can create duplicate or orphan candidates if the commit protocol is weak. Object stores lack atomic directory rename, so path-based output committers can add copy/list/delete work or visibility hazards.

### Streaming freshness trade-off

A streaming sink must eventually close and commit files so readers see data and checkpoints can recover. Short checkpoint/rolling intervals reduce recovery and visibility delay but increase file count. Longer intervals improve size and can hold more in-progress state.

Let average bytes per active bucket per commit interval be `mu`. If `mu` is far below target size, tuning only the size threshold does nothing because checkpoint or time triggers close first. Reduce active buckets per writer, lower writer parallelism, increase interval within SLA, or compact pending/committed outputs safely.

Compaction before final visibility can avoid exposing small files but delays visibility and can backpressure checkpoint completion. Post-commit compaction keeps ingestion fast and requires table-snapshot replacement plus later cleanup.

### Partition cardinality and skew

Partitioning should enable meaningful pruning and operational ownership. Partitioning by high-cardinality IDs or minute timestamps can create directories/prefixes containing one or a few records. Empty and sparse combinations multiply catalog work.

Estimate distribution, not just average. Measure file-size percentiles per logical partition, files per partition, bytes per partition, and writer fan-out. One target cannot serve a 10-TiB daily partition and a 20-KiB daily partition equally.

Bucket/hash within large partitions to bound parallelism, but do not create more buckets than data can fill. Evolve partition specifications through table metadata rather than rewriting names blindly.

### Writer-side prevention

First control record distribution. Coalesce or repartition before the sink based on expected bytes, not an arbitrary executor count. Use adaptive partitioning when available, and isolate extreme skew keys.

Second align rolling policy with target bytes, maximum age, inactivity, and checkpoint rules. Measure actual compressed bytes because input row size and output compression vary. Cap open writers and spill safely rather than keeping one buffer per unbounded partition.

Third make publication transactional. Writers create unique immutable files; a committer validates successful attempts and publishes only selected file identities. Failed/speculative files remain candidates for audited orphan cleanup.

### Choosing a target size

Start from engine guidance as a hypothesis, not a mandate. Consider maximum scan split, format row-group guidance, object multipart thresholds, executor memory, typical predicate selectivity, network bandwidth, open latency, recovery unit, and desired task duration.

A useful target yields tasks long enough to amortize launch cost and enough splits to occupy the cluster. If target file scan time is `t_target` and effective throughput per task is `r_task`, approximate bytes as `r_task*t_target`, capped by memory and format constraints.

Validate with representative full scans, selective filters, joins, writes, failures, and concurrency. Report median and tail planning/runtime plus storage request count and total maintenance cost.

### Compaction strategies

Bin-pack compaction groups small files toward a target size while mostly preserving existing order. It is inexpensive and improves open/file count. Sort compaction rewrites records into a declared order, improving min/max pruning at higher shuffle cost.

Clustering or multidimensional ordering targets common predicates and can reduce files read. It may degrade other queries and becomes stale as data distribution evolves. Partition-local compaction limits shuffle and preserves partition boundaries.

Merge-on-read tables can compact data files, delete files, or both. Applying positional/equality deletes during rewrite changes what files and sequence numbers mean; use the table format's supported maintenance procedure.

### Selecting candidates

Do not rewrite every file on every run. Select file groups by size distribution, delete density, overlap, age/coldness, query heat, expected bytes saved, manifest pressure, and available maintenance budget.

Avoid hot partitions still receiving frequent updates unless the table protocol resolves conflicts efficiently. A quiet-window rule reduces churn but must account for late data and event-time semantics.

Bound group input bytes, input file count, output count, shuffle memory, and concurrent groups. Partial-progress commits improve operability and create more snapshots/conflict surfaces; track exactly which groups committed.

### Snapshot-safe compaction protocol

Read table snapshot `s` and select exact input file identities `I`. Plan groups whose partition/spec/schema/delete compatibility is valid. Write outputs `O` under unique attempt names; validate row counts, aggregates, key constraints, checksums, partition values, statistics, and encryption.

Commit a new snapshot with predicate “all inputs in `I` are still live as expected.” The atomic metadata change removes `I` and adds `O`. On conflict, determine whether groups remain valid, rebase through the table protocol, or abandon outputs for later cleanup.

Readers pinned to `s` continue reading `I`; readers of the new snapshot read `O`. Do not delete `I` until snapshot retention, reader leases, branches/tags, clones, backups, holds, and recovery policy permit. Do not expose `O` as dataset members before metadata commit.

### Validation invariants

Row count alone is weak: a duplicate and omission can cancel. Validate domain keys or multiset hashes where appropriate, null counts, min/max, partition values, schema IDs, sort bounds, delete application, and representative query equivalence.

Floating-point aggregation and nondeterministic serialization require carefully chosen comparisons. Encryption rewrites need key/version/nonce correctness. Compression changes physical bytes, so logical record identity matters more than identical file hashes.

Preserve provenance from each output to input file versions, compaction operation, software/config version, and validation evidence. This supports incident reconstruction and targeted rollback.

### Concurrency and retry

Two compactors can select overlapping inputs. Optimistic snapshot commit should allow at most a valid nonconflicting outcome. A stale compactor must not resurrect removed rows or discard concurrent appends/deletes.

Retry uses a durable operation ID and unique output identities. After an ambiguous commit response, query table history for the operation before writing or committing again. Reusing a destination name with different bytes destroys idempotency.

Leases can reduce duplicate work but are not correctness unless fenced. The manifest/table transaction remains authority.

### Garbage collection

Uncommitted outputs, failed attempt files, and superseded inputs consume space. Garbage collection traces live references from retained snapshots, branches, tags, clones, manifests, and recovery windows. Age alone is not proof of orphanhood.

Use minimum age greater than maximum commit/retry/listing delay, compare normalized scheme/authority carefully, support dry run, batch/rate limit deletes, and revalidate exact versions. An incorrect prefix or credential scope can turn cleanup into data loss.

Snapshot expiration and orphan removal are separate. Expiring a snapshot can make files eligible; the cleanup operation establishes and executes reachability decisions under policy.

### Compaction economics

Let read savings per period be avoided opens, planning CPU, task launches, bytes through improved pruning, and latency/SLA value. Maintenance cost includes reading inputs, shuffle, output writes, requests, temporary and retained duplicate storage, catalog commits, validation, and cleanup.

Prioritize groups where expected discounted read benefit exceeds rewrite cost and risk. Frequently rewritten hot data can have high write amplification with little stable benefit. Cold high-query partitions often yield better returns.

Charge maintenance transparently to platform or dataset budgets. Otherwise query teams benefit while ingestion teams absorb hidden cost, or vice versa.

### Observability

Track payload bytes, live data files, average/percentile file size, files per logical partition, row groups, manifests, delete files, snapshots, orphan candidates, and retained superseded bytes.

Read metrics include planning time, files selected/opened, GET/HEAD/LIST count, bytes read/returned, task count/duration, scheduler delay, throttles, and cache hit rate. Write metrics include files per checkpoint, bytes/file, open writers, roll reason, commit delay, and failed candidates.

Compaction metrics include groups, input/output files and bytes, amplification, conflict/retry, validation failure, snapshot commit latency, query improvement, backlog age, and cleanup lag. File-count reduction without query or cost improvement is not success.

### Security and governance

Compaction reads and rewrites entire data domains. Scope principals to intended tables/partitions, protect temporary paths, preserve encryption/residency/retention, and prevent mixing tenants or classifications in one object when that changes access boundaries.

Row-level and column-level policy may be enforced by catalogs rather than file ACLs. A compacted file must remain addressable only through policy-aware membership. Statistics and filenames can leak sensitive values.

Destructive cleanup requires approval, audit, rollback/recovery plan, and evidence across replicas/backups. For research or regulated data, technical equivalence is not permission to rewrite or erase.

### Testing

Generate controlled distributions: many empty/tiny files, mixed sizes, skewed partitions, large unsplittable files, dense delete files, late data, schema evolution, and encryption-key changes. Benchmark full and selective queries.

Inject worker crash during output, coordinator crash before/after snapshot commit, lost commit response, concurrent append/delete/compaction, token/list failure, throttling, and cleanup retry. Assert readers see old or new snapshot membership, never an uncommitted mixture.

Test snapshot retention, time travel, branch/tag references, clones, backup restore, legal holds, and orphan-cleaner boundaries. Verify metrics can explain both improvement and regression.

## Definitions and Notation

- `B` is total logical/physical payload bytes under the stated compression scope.
- `F` is live data-file count and `b_i` is bytes in file `i`.
- `S_avg=B/F` is average file size; percentiles remain necessary under skew.
- `l_open` is observed fixed open latency and `c_file` aggregates other per-file work.
- `r_effective` is useful aggregate payload scan rate under the measured workload.
- `W` is writer parallelism, `Q` active logical partitions per writer, and `C` commit/checkpoint intervals.
- `s` is an immutable table snapshot; `I` and `O` are exact input and output file-version sets.
- `T_target` is target output size and `G` is one bounded compaction group.
- `A_write=bytes_written/logical_new_or_changed_bytes` is write amplification under a declared window.
- `R_saved` is expected read cost avoided and `C_rewrite` is maintenance cost.

The exposure `W*Q*C` is not a guaranteed file count: some combinations receive no records, one writer may emit multiple rolled files, and sink retry/commit semantics vary. It is a diagnostic upper-shape that identifies multiplicative controls.

## Mechanisms, Invariants, or Proof Structure

Use this small-file diagnosis and compaction audit:

1. Measure file-size distribution, file/manifest count, partitions, row groups, requests, planning, tasks, and payload.
2. Identify producer factors: writers, active partitions, checkpoints, roll reasons, late data, retry, and speculation.
3. Model fixed per-file versus variable byte cost for representative read and write workloads.
4. Define a target size interval plus freshness, recovery, memory, splitability, and pruning constraints.
5. Prevent new pathology with bounded writers, partition design, adaptive distribution, and rolling policy.
6. Select immutable compatible input versions from one table snapshot and bound each group.
7. Write unique outputs and validate logical equivalence, schema, deletes, partitions, security, and provenance.
8. Conditionally commit membership replacement; resolve ambiguity and conflicts from table history.
9. Retain inputs while referenced, then garbage-collect by proven reachability and policy.
10. Measure read benefit, write amplification, backlog, failures, cost, and governance outcomes.

The fixture compares one TiB represented by 1-MiB and 256-MiB files. Its serial-open and abstract planner weights illustrate fixed-cost amplification; they are not production predictions or universal tuning values.

<!-- bijux-verify: {"id":"small-file-cost-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"dataset_bytes=1099511627776\nsmall_files=1048576 target_files=4096 reduction=256x\nserial_open_seconds_small=8388.608 serial_open_seconds_target=32.768\nopen_weight_bytes_small=5497558138880 open_weight_bytes_target=1116691496960\n","stderr":""}} -->
```python
MIB = 1024 * 1024
TIB = 1024 * 1024 * MIB

dataset_bytes = TIB
small_file_bytes = MIB
target_file_bytes = 256 * MIB
open_latency_seconds = 0.008
open_cost_bytes = 4 * MIB

small_files = (dataset_bytes + small_file_bytes - 1) // small_file_bytes
target_files = (dataset_bytes + target_file_bytes - 1) // target_file_bytes

print(f"dataset_bytes={dataset_bytes}")
print(
    f"small_files={small_files} target_files={target_files} "
    f"reduction={small_files // target_files}x"
)
print(
    f"serial_open_seconds_small={small_files * open_latency_seconds:.3f} "
    f"serial_open_seconds_target={target_files * open_latency_seconds:.3f}"
)
print(
    f"open_weight_bytes_small={dataset_bytes + small_files * open_cost_bytes} "
    f"open_weight_bytes_target={dataset_bytes + target_files * open_cost_bytes}"
)
```

The payload is identical. The smaller layout adds four TiB of abstract open weight, while the target layout adds 16 GiB. Real engines may pack files, split large files, parallelize opens, cache metadata, or use different weights; measure their actual plan.

Correctness proof is separate from the cost model. Safe rewrite proves exact snapshot inputs, equivalent logical output, conditional membership commit, old-reader preservation, and reference-aware cleanup.

## Alternatives and Trade-Offs

Writer-side coalescing avoids later rewrite and can create shuffle, skew, slower checkpoints, or too few files. Post-write compaction decouples ingestion and adds maintenance latency, duplicate storage, and transactions.

Bin packing minimizes file count cheaply. Sorting or clustering spends shuffle to improve pruning. Query-specific materialization can outperform both and multiplies storage and governance surfaces.

Larger files amortize fixed cost and reduce parallel scheduling granularity. Smaller files support selective access, independent recovery, low-volume partitions, and lower rewrite units. Splittable formats soften the parallelism trade-off.

Time-based rolling bounds visibility and recovery delay but produces tiny files during low traffic. Size-based rolling improves file size and can leave data pending indefinitely without an age trigger. Combine size, age, inactivity, and checkpoint rules deliberately.

High writer parallelism raises ingestion throughput and file count. A downstream repartition lowers file count and costs network/shuffle. Adaptive skew handling is preferable when supported.

Fine-grained partitioning improves pruning when filters align and creates sparse directories/files when they do not. Coarser partitions rely more on file statistics and clustering.

Table-format compaction preserves snapshot semantics and requires compatible readers/catalog. Ad hoc prefix rewriting is portable and lacks a safe membership transaction unless an explicit manifest is built.

Aggressive snapshot expiration frees space and reduces recovery/time-travel windows. Long retention protects rollback and keeps superseded small files plus metadata alive.

## Failure Modes and Misconceptions

- **“Anything below 128 MiB is a small file.”** Threshold depends on engine, storage, format, query, and SLA.
- **“Total bytes are small, so the dataset is cheap.”** Fixed per-object and per-file costs scale with count.
- **“Object storage supports billions of objects, so count is irrelevant.”** Capacity, request economics, listing, catalogs, and planners are different limits.
- **“One file equals one task.”** Engines can pack small files and split large splittable files.
- **“Task coalescing fixes the files.”** It can reduce tasks while preserving every open, manifest entry, and lifecycle object.
- **“Set the target size and writers will reach it.”** Time/checkpoint/inactivity triggers and sparse partitions may close first.
- **“More writer parallelism is always faster.”** It multiplies files and can deepen skew and commit pressure.
- **“Partition by every common filter.”** High-cardinality combinations can create sparse layout and metadata explosion.
- **“Compaction is concatenation.”** Formats, schemas, compression, ordering, statistics, encryption, and deletes require semantic rewrite.
- **“Equal row counts prove equivalence.”** Duplicates and omissions can cancel.
- **“Output files exist, so compaction committed.”** Only manifest/table membership establishes publication.
- **“Delete inputs immediately after output.”** Retained snapshots and readers may still reference them.
- **“Age proves orphanhood.”** Slow/ambiguous commits, retries, clones, and holds can retain old-looking live files.
- **“Two compactors only waste work.”** Without conditional commit, they can lose updates or resurrect data.
- **“Compaction always improves queries.”** Poor clustering, huge files, or a selective workload can regress.
- **“File-count reduction proves ROI.”** Measure planning, execution, requests, rewrite, storage, and maintenance together.
- **“Frequent streaming checkpoints and large files are independent.”** Bulk formats commonly roll at checkpoint boundaries.
- **“Technical equivalence permits deletion.”** Retention, legal, ethical, backup, and recovery requirements still govern.

## Worked Examples

### Example 1

**Situation:** One TiB is stored in 1-MiB objects. **Reasoning:** There are 1,048,576 objects. Rewriting near 256 MiB yields 4,096, reducing fixed per-file exposure 256-fold while payload stays one TiB.

### Example 2

**Situation:** A streaming sink has 200 writers, touches 40 buckets each, and commits 60 times per hour. **Reasoning:** The multiplicative exposure is 480,000 writer-bucket-commit combinations per hour. Measure nonempty combinations, then reduce fan-out, interval, parallelism, or compact.

### Example 3

**Situation:** Spark launches fewer tasks after packing tiny files but planning remains slow. **Reasoning:** Task coalescing reduces scheduler count, not namespace listing, object opens, footer reads, catalog entries, or driver planning. Repair physical/table layout too.

### Example 4

**Situation:** A 10-GiB gzip file creates one straggler. **Reasoning:** Large is not automatically healthy; the codec may be unsplittable. Rewrite to a splittable format with bounded row groups and enough files/splits for useful parallelism.

### Example 5

**Situation:** Low-volume tenants each receive one daily file of a few KiB. **Reasoning:** Tenant/day physical partitioning is too fine for scans. Preserve tenant as a column, use coarser partitioning plus statistics/clustering, while retaining required security isolation.

### Example 6

**Situation:** A compactor sees 2,000 small files, but concurrent deletes modify the table. **Reasoning:** Bind exact input and delete-file sequence semantics to snapshot `s`; commit conditionally through the table format or replan. Ad hoc replacement can resurrect deleted rows.

### Example 7

**Situation:** The compaction commit response is lost. **Reasoning:** Query table history for durable operation ID and output membership. Do not immediately write new names or delete inputs; resolve committed, conflicted, or absent outcome first.

### Example 8

**Situation:** Query latency improves 30%, but maintenance rewrites the hot partition every ten minutes. **Reasoning:** Measure write amplification and stable benefit. Add quiet windows, prioritize colder groups, compact delete files selectively, or change writer layout.

### Example 9

**Situation:** An orphan cleaner finds outputs older than one day. **Reasoning:** Trace retained snapshot/branch/clone/backup references and unfinished operations, enforce a safe minimum age, dry-run, revalidate exact versions, and rate-limit deletion. Age is only a filter.

### Example 10

**Situation:** Compaction combines records from two regulated tenants into one encrypted file. **Reasoning:** Verify the policy engine can preserve tenant authorization and residency at file/table access. If physical isolation is required, group only within that boundary and retain provenance and key context.

## Cross-Program Connections

[Data Engineering](../../19-data-engineering/ROADMAP.md) supplies streaming sinks, batch files, partition design, table formats, compaction, and data-quality validation. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns dataset identity, schema, provenance, retention, catalogs, and authoritative membership.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies snapshot transactions, optimistic concurrency, retries, fencing, and garbage collection. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies scheduler economics, storage quotas, observability, maintenance orchestration, and cost ownership.

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies LSM compaction analogies, indexes, MVCC, tombstones, write amplification, and query planning. [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies files, blocks, page cache, system calls, sequential I/O, and memory pressure.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies authorization boundaries, encryption/key lifecycle, temporary-path protection, audit, and safe erasure. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies workload boundaries, trade studies, hazard review, and evidence-based optimization.

Apache Spark documents file-open cost, maximum scan-partition bytes, parallel partition discovery, and output coalescing controls. Apache Iceberg documents data-file and manifest rewrite maintenance. Apache Flink documents rolling/checkpoint file lifecycle and compaction visibility. These mechanisms illustrate trade-offs; their defaults are not universal targets.

## References

- Apache Spark, [*SQL Performance Tuning*](https://spark.apache.org/docs/latest/sql-performance-tuning), checked 2026-09-03. Official current file open-cost, scan partition-byte, listing parallelism, adaptive partition, and coalesce/repartition guidance.
- Apache Spark, [*Tuning Guide*](https://spark.apache.org/docs/latest/tuning.html), checked 2026-09-03. Official current task parallelism, scheduler overhead context, object allocation, and parallel input listing guidance.
- Apache Hadoop, [*HDFS NameNode Fine-Grained Locking*](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/NamenodeFGL.html), checked 2026-09-03. Official current NameNode in-memory namespace/block metadata and listing/read request architecture.
- Apache Parquet, [*File Format Configurations*](https://parquet.apache.org/docs/file-format/configurations/), checked 2026-09-03. Official row-group, page, block, buffering, sequential I/O, and example size guidance.
- Apache Iceberg, [*Spark Procedures — rewrite_data_files*](https://iceberg.apache.org/docs/latest/spark-procedures/#rewrite_data_files), checked 2026-09-03. Official current small-file metadata/open-cost motivation, bin-pack/sort rewrite, sizing, partial progress, and concurrency options.
- Apache Iceberg, [*Structured Streaming*](https://iceberg.apache.org/docs/latest/spark-structured-streaming/), checked 2026-09-03. Official current streaming snapshot, small data file, data compaction, manifest rewrite, and maintenance guidance.
- Apache Flink, [*FileSystem Connector*](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/filesystem/), checked 2026-09-03. Official current rolling policy, checkpoint file lifecycle, compaction, visibility delay, and backpressure behavior.
- Amazon Web Services, [*Best Practices Design Patterns: Optimizing Amazon S3 Performance*](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html), checked 2026-09-03. Official current request scaling, prefix parallelism, latency, throttling, and large analytical scan context.
- Amazon Web Services, [*Organizing Objects Using Prefixes*](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html), checked 2026-09-03. Official current flat-key prefix/delimiter organization and listing projection semantics.
- Apache Iceberg, [*Flink Table Maintenance*](https://iceberg.apache.org/docs/latest/flink-maintenance/), checked 2026-09-03. Official current automated small-file compaction, snapshot expiration, rewrite sizing, limits, and partial-progress controls.

## Exercises

### Exercise 1

Compare one TiB stored in 2-MiB files with a 256-MiB target. Calculate file counts, reduction factor, and modeled serial open time at 6 ms per file. State why the result is not a wall-clock prediction.

### Exercise 2

A streaming sink uses 120 writers, each touches up to 25 active partitions, and rolls bulk files at every 30-second checkpoint. Calculate one-hour multiplicative exposure and propose controls while preserving a two-minute freshness objective.

### Exercise 3

Design snapshot-safe compaction when equality deletes and concurrent appends can occur. State membership and validation invariants.

### Exercise 4

Define an evidence-based target-file-size experiment for full scans and selective queries. Include metrics that can reject compaction as uneconomic.

### Exercise 5

Specify safe orphan cleanup and named review for compacted regulated data with retained snapshots, cross-region replication, backups, and legal holds.

## Answers to the Exercises

### Answer 1

One TiB contains 1,048,576 MiB, so 2-MiB files yield 524,288 files; 256-MiB files yield 4,096. The count/open reduction is 128-fold. Modeled serial open time is `524,288*0.006=3,145.728` seconds versus `4,096*0.006=24.576` seconds. It is not wall-clock prediction because engines parallelize and coalesce opens, cache metadata, split larger files, overlap I/O, and encounter request/coordinator/executor limits. It isolates one fixed-cost term; benchmark actual planning, requests, bytes, tasks, and tail latency.

### Answer 2

There are 120 checkpoints/hour. The loose exposure is `120 writers * 25 partitions * 120 checkpoints = 360,000` writer-partition-checkpoint combinations per hour. Actual nonempty/rolled files can be lower or higher. A two-minute objective permits testing checkpoint/visibility coordination up to that bound, but recovery checkpoint need not equal final file publication if the sink supports pending compaction. Reduce writer-to-partition fan-out, route sparse partitions through fewer writers, cap open buckets, choose coarser physical partitions, use adaptive coalescing, and compact pending files across several checkpoints if semantics permit. Measure checkpoint latency/backpressure, recovery state, bytes/file percentiles, and late-data behavior.

### Answer 3

Read immutable snapshot `s`; select exact data and equality-delete file versions with sequence semantics; restrict each group to compatible partition spec/schema/security boundaries. Apply deletes exactly once while rewriting rows, then validate key/multiset evidence, counts, null/min/max, partitions, sort bounds, schema, encryption, and provenance. Write uniquely named outputs. Commit conditionally so selected inputs/deletes remain valid and concurrent appends are preserved; use the table format's rewrite isolation rather than replacing a prefix. On conflict, replan or perform a supported rebase. Old snapshot readers retain old files; cleanup waits for snapshot/lease/branch/backup/hold reachability.

### Answer 4

Sample representative hot/cold, dense/sparse, skewed, and delete-heavy partitions. Produce candidate layouts across a target interval with compatible row groups and clustering. Run full scans, selective filters, joins, and failure/retry cases at production-like concurrency. Measure planning time/memory, manifests/files selected, LIST/HEAD/GET, bytes read, pruning, tasks, scheduler delay, executor memory, median/tail runtime, request/storage cost, and result equivalence. Measure rewrite input/output bytes, shuffle, amplification, temporary/retained storage, conflict, backlog, cleanup, and compute cost. Reject or narrow compaction where discounted read/SLA benefit does not exceed recurring rewrite and risk, or where selective queries/freshness/recovery regress.

### Answer 5

Start from table/catalog reachability across retained snapshots, branches/tags, clones, reader leases, incomplete compaction operations, replica manifests, backups, and holds. Generate an immutable candidate manifest with exact object versions, provenance, reason, minimum age, retention/policy version, and approval. Dry-run and compare counts/bytes/domains; revalidate each version and hold before conditional deletion; use canaries, bounded batches, mismatch stop thresholds, and immutable logs. Reconcile primary, replicas, backup expiry, inventory, and key lifecycle afterward. Named review includes data owner/steward, records/privacy/legal/compliance, affected community or research-ethics/IRB where applicable, security/key management, table-format and storage operators, disaster recovery/backup owners, accessibility, finance/sustainability where material, and independent assurance. Logical unreachability does not alone prove lawful physical erasure.
