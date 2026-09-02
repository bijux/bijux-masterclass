---
module_id: DE-034
program: Data Engineering
level: 1
module_number: 34
title: Partitioned Processing
status: complete
last_verified: 2026-09-02
---

# Partitioned Processing

## One-Page Review

### Governing question

How can a dataset be divided and processed concurrently so every intended occurrence is covered exactly once logically, cross-partition operations preserve semantics, skew and resources remain bounded, retries do not duplicate output, and consumers see one complete generation?

### Essential definitions

- An **input partition** is a bounded subset of a source generation selected by an exact manifest or predicate.
- An **execution partition** is a unit scheduled to one task; it may combine, split, or redistribute input partitions.
- An **output/data partition** is a physical grouping used for storage, pruning, lifecycle, or write parallelism; it need not match execution partitioning.
- A **partition function** $p(x)$ maps an occurrence $x$ to a partition identity under a named version and null/error policy.
- **range partitioning** assigns values to ordered, usually half-open intervals; **hash partitioning** assigns canonical keys through a stable hash and modulus/bucket rule.
- **coverage** means every intended input occurrence belongs to an assigned partition; **disjointness** means it belongs to no more than one logical input partition.
- A **partition-local transformation** can compute each partition independently and combine results without changing the declared output.
- A **shuffle** redistributes records among execution partitions, commonly to colocate equal keys for grouping or joining.
- **skew** is uneven distribution of rows, bytes, computation, state, or output that makes a small number of partitions dominate the job.
- A **small-file problem** occurs when excessive physical files create disproportionate listing, metadata, scheduling, open/close, and planning overhead.
- A **partition manifest** records the complete expected partition set, selected input objects, successful attempt outputs, statistics, and digests for one generation.
- **partition pruning** avoids reading partitions/files proven irrelevant to a predicate under trusted partition metadata.
- **atomic publication** exposes one validated complete manifest/snapshot rather than making directory contents trustworthy piecemeal.

### Central model, mechanism, or theorem

For source occurrence bag $D$ and partition assignment $p:D\rightarrow\{0,\ldots,q-1\}$, define

$$
P_i=\{x\in D:p(x)=i\}.
$$

Correct assignment requires occurrence-level conservation:

$$
\biguplus_{i=0}^{q-1}P_i=D,
$$

where the bag union encodes both coverage and disjointness. Parallel evaluation is semantically composable when transformation $F$ has mergeable state $(A,\oplus,e)$ and local map $f$ such that

$$
F(D)=\bigoplus_{i=0}^{q-1}f(P_i).
$$

Counts and exact integer sums satisfy this with additive state. A mean requires `(sum,count)`, not a mean of partition means. Global distinct, median, total ordering, windows, and joins may require richer state, a shuffle, or another coordination boundary.

If partition durations are $T_i$, idealized stage completion is bounded below by

$$
T_{stage}\geq\max_i T_i.
$$

Adding workers cannot make the slowest hot partition disappear; skew control is a semantic and capacity design problem.

### Critical invariants

- Source generation, input object versions, expected occurrence population, and partition-function/spec version are immutable for a run.
- Partition assignment is total and deterministic for valid inputs; null/invalid keys have an explicit quarantine or bucket policy.
- Input partitions cover the intended occurrence bag without overlap, gaps, or accidental duplicate discovery.
- Range boundaries use one time role, time zone, precision, and interval convention; hash keys use canonical bytes and a stable named algorithm.
- Every operation is classified as partition-local, mergeable, or globally coordinating; no local computation silently substitutes for a global result.
- Join strategies prove key colocation or deliberately broadcast/shuffle, with cardinality, missing-key, and skew controls.
- Each task writes attempt-specific output and a receipt; retries/speculative attempts never share an unversioned output path.
- The generation manifest selects at most one accepted attempt per logical output partition and exactly the expected partition set.
- Per-partition and global reconciliation prove input/output/quarantine counts, identities, schema, keys, measures, and boundary ownership.
- Publication changes one trusted manifest/snapshot/pointer only after all gates pass; file listing is not a commit protocol.
- Partition size/count, hot-key distribution, shuffle/spill, file size/count, metadata load, and recovery fit measured operating envelopes.
- Partition-spec evolution remains distinguishable from logical data semantics and preserves old/new reader correctness.

### Common failures

Common failures include confusing source files with execution partitions; processing a live directory listing without a manifest; overlapping inclusive range ends; deriving event-date partitions in different time zones; using runtime-randomized hash functions; sending null keys to arbitrary workers; assuming per-partition uniqueness implies global uniqueness; averaging partition averages; local top-N presented as global top-N; joining independently partitioned datasets without compatible key placement; salting hot keys without a correct desalt/recombine proof; collecting all state on the driver; choosing one partition per core as a universal rule; creating millions of tiny files; trusting path text over validated partition metadata; overwriting trusted partitions as tasks finish; accepting both speculative attempts; retrying after an ambiguous commit; mixing partition specs without metadata; pruning on ingestion date when the predicate is event time; and publishing because the expected number of paths happens to exist.

### Compact example

Eight immutable events across five customer keys are assigned by a stable teaching hash to three execution partitions with row counts `(2,3,3)`. Each partition computes customer `(count,sum)` state; merging gives `c1=(2,80)`, `c2=(2,100)`, `c3=(2,25)`, `c4=(1,5)`, and `c5=(1,30)`, totaling eight events and 240 cents. Repartitioning into four buckets yields the same canonical result. A retry produces two identical candidates for one logical partition, but the generation manifest selects one attempt, so its events appear once.

### Connections

[DE-021](021-full-and-incremental-extraction.md) through [DE-030](030-designing-replayable-raw-ingestion.md) define source bounds and replay; [DE-032](032-sql-transformation-pipelines.md) defines model graphs and publication; [DE-033](033-dataframe-transformation-pipelines.md) defines local/lazy/distributed dataframe semantics. DE-035 next treats incremental models; DE-036 through DE-040 extend merge, backfill, correction, determinism, and batch-testing behavior.

## Governing Question

What must remain true when one logical dataset becomes many independently scheduled pieces and then one trusted output again?

Partitioning is more than “split the data.” It creates new identities and boundaries: which source occurrences belong to which input unit, where computation runs, which keys must meet, what state can combine, which files represent output, and when the set becomes visible. Every one of those boundaries can lose, duplicate, misclassify, or expose data.

The first discipline is to separate three notions. Input partitioning describes source coverage. Execution partitioning describes task parallelism and data placement during computation. Output partitioning describes physical storage and query pruning. An engine may scan one large file into many execution tasks, combine many small files into one task, shuffle records twice, and write a different number of output files arranged by a table partition spec. Calling all of these “the partitions” hides the system.

The second discipline is algebraic. Some transformations map independently over occurrence partitions. Some produce mergeable partial state. Others require equal keys, total order, cross-boundary windows, or global coordination. A correct design classifies the operator before optimizing it.

The third discipline is transactional. Task execution is normally at-least-once under retry and speculation. Logical output can still be exactly-once in one committed generation when attempts write isolated objects and a manifest/snapshot selects one accepted result per logical partition. Exactly-once execution is neither necessary nor usually the right claim.

## Why This Matters

Partitioning makes large processing feasible. It enables parallel scans, local transformations, bounded working sets, predicate pruning, independent retry, and lifecycle management. It can reduce a multi-hour single-worker job to a tractable distributed pipeline and prevent irrelevant data from being read.

It also distributes failure. A file listing can change during discovery. Two workers can own the same boundary record. A hot customer can make one partition 100 times larger than the rest. A join can reshuffle terabytes because inputs are partitioned on different keys. A retry can produce duplicate files. A backfill can overwrite a live partition. A reader can observe half the new day before the remaining tasks finish.

Boundary defects are especially quiet. Daily ranges written as inclusive start and inclusive end duplicate midnight. Local-time partitioning produces 23- or 25-hour days around daylight-saving changes. Hash assignment changes after a runtime/library upgrade. A source object replaced at the same path changes content while retaining its apparent partition name. Per-partition counts can all look plausible even when the expected partition set is incomplete.

Parallel aggregation needs correct state. Counts and integer sums merge naturally. Averages do not: the unweighted mean of partition means gives equal weight to unequal partitions. Approximate distinct or quantile algorithms require documented sketches and error bounds. Global sort and windows require range knowledge, overlap/halo, shuffle, or a second stage.

Physical layout has a lifecycle. Fine partitions improve selective reads until directories, manifests, files, tasks, and metadata overwhelm the system. Coarse partitions reduce metadata but scan too much and concentrate retries. The right shape follows data size, skew, access predicates, engine/storage behavior, latency, concurrency, and maintenance evidence—not a permanent magic number.

## Prerequisites and Retrieval

Retrieve the business/output contract; source owners and immutable snapshot/manifests; source objects, versions/digests, record identities and expected counts; input formats, splittability, compression, row groups and statistics; current physical partition layout and spec/history; partition columns/transforms and derivation time zone; execution engine/version/configuration; operator graph and plans; key distributions, nulls, cardinalities and heavy hitters; data sizes before/after decoding and each transformation; worker CPU/memory/disk/network; scheduler/task overhead; locality; join sides and strategies; aggregation state and algebra; ordering/window boundaries; output schema, table format/catalog and commit rules; target file/row-group sizes and counts; retry/speculation/timeouts; concurrent runs, backfills and compaction; partition overwrite modes; validation/reconciliation; lineage/metrics; access/residency/tenant policy; SLOs/cost; retention/rollback; incidents; and disaster-recovery evidence.

Distinguish source object from logical input partition; object path from immutable object version; row group from file; input split from execution task; execution partition ID from business/data partition value; repartition from coalesce; hash bucket from range; record key from partition key; event time from ingestion/process time; logical day from local calendar label; local computation from mergeable global result; map-side combination from final aggregation; colocation from sort order; broadcast from shuffle join; worker retry from logical output retry; task success from accepted attempt; file existence from committed generation; directory partition column from hidden table transform; pruning from semantic filtering; compacted file from changed data; and balanced row count from balanced bytes/compute/state.

Before implementation, create a partition contract:

| Field | Required content |
|---|---|
| Source population | Generation/cut, exact object versions, schema, occurrence identity, exclusions |
| Input assignment | Partition function/spec version, key/type/encoding, bounds, null/error policy |
| Operator class | Local, mergeable state, key-colocated, overlap/halo, broadcast, shuffle, global |
| Execution | Engine/runtime/config, task IDs, resources, retry/speculation, plan and shuffle stages |
| Skew | Row/byte/key/state distributions, heavy hitters, mitigation and recombination proof |
| Output layout | Logical partition values, file format, target sizes/counts, sorting/clustering |
| Attempt protocol | Logical partition ID, attempt ID, isolated objects, receipt and cleanup |
| Validation | Expected set, coverage/disjointness, schema/key, boundary and reconciliation gates |
| Publication | Manifest/snapshot/pointer, expected prior generation, receipt, rollback/retention |
| Evolution | Spec ID/history, reader compatibility, rewrite/compaction and deprecation plan |

Use exact input manifests for production and experiments. If candidate strategies read different live directory listings, their performance and output comparisons are confounded.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish input, execution, shuffle, and output/data partitions and identify their owners;
2. define deterministic hash, range, time, composite, and hidden partition assignments;
3. prove occurrence-level coverage and disjointness under explicit boundary and null policies;
4. classify transformations as local, mergeable, colocated, overlap-dependent, or global;
5. derive correct partial aggregation state and recognize non-composable local results;
6. select broadcast, colocated, or shuffle joins from size, key, cardinality, and skew evidence;
7. diagnose and mitigate row/byte/compute/state skew without corrupting semantics;
8. size partitions/files from measured task, memory, shuffle, metadata, pruning, and retry costs;
9. make retries/speculation safe through attempt isolation and exact generation manifests; and
10. validate, publish, evolve, compact, observe, secure, and recover partitioned datasets.

## Core Exposition

### Separate input, execution, and output partitioning

An input partition names a portion of one immutable source generation. It may be an object version, row-group set, database key range, log offset interval, or table snapshot scan task. Its identity must survive retry.

An execution partition is scheduled work. Engines may derive several tasks from one splittable object, combine small objects, coalesce tasks, or repartition records after filters. Its numeric ID is operational and may change with the plan.

An output partition groups written records by a physical table transform or directory convention. Several task attempts may produce files for one output partition; one task may write several output partition values. Output partition value is not a proof of task or source lineage.

Draw each layer separately. Record mappings from source object/record occurrence to scan task, shuffle stage, writer attempt, output file, data partition value, and committed snapshot. This prevents an operator from using execution IDs as stable business identifiers or treating one-file-per-task as a durable interface.

### Freeze the source before dividing it

List exact input objects with immutable versions or digests, sizes, schemas, statistics, and expected record controls. Database/log inputs use snapshot IDs, key bounds, offsets, or other source-native cuts. The list itself belongs to the run manifest.

Never let each worker independently enumerate a live directory. Objects can arrive, disappear, or be replaced between listings, producing gaps or duplicates. A coordinator resolves the source generation once and assigns immutable entries.

File paths are names, not versions. On object stores, bind version/generation/ETag/checksum according to provider guarantees. For mutable table paths, use a table-format snapshot/catalog commit rather than recursive listing.

Compressed or encoded files may not split arbitrarily. Retrieve format/block/codec behavior and validate record framing across split boundaries. A task must not start in the middle of an unsplittable compression stream or decode the same logical record from overlapping byte ranges.

### Define the partition function as a versioned contract

For valid occurrence $x$, partition assignment $p(x)$ must be total, deterministic, and single-valued. Specify key columns, logical/physical types, canonical byte encoding, normalization/collation, null/error behavior, algorithm, seed, bucket count or range bounds, and spec version.

Do not use a language runtime’s randomized/default object hash as durable assignment. Use a stable named algorithm or a table/engine partition transform whose versioned semantics are part of the platform contract. Changing bucket count normally reassigns keys; treat it as repartitioning/spec evolution.

Null partition keys need a deliberate bucket or quarantine. An implicit default directory can combine unknown, malformed, redacted, and missing records and become a hot/sensitive partition. Preserve reason distinctions where they matter.

Partition metadata can be derived from data, but it must not contradict it. If writers place `event_time=2026-09-02T00:05Z` under `event_date=2026-09-01`, readers that prune by date can silently miss it. Validate transforms or use a table format that owns hidden partition derivation.

### Prove coverage and disjointness

For occurrence bag $D$, partitions $P_i$ must satisfy bag union $\biguplus_iP_i=D$. This means each occurrence appears exactly once in the logical assignment, not that equal payload values occur once.

Range partitions should be half-open: $[b_i,b_{i+1})$. Adjacent ranges then share no ordinary point and cover their combined interval. Define the first/last bounds, nulls, out-of-range values, precision, and conversion before comparison.

Verify with identities, not counts alone. Maintain expected source occurrence IDs or per-source range controls; compare duplicate assignments, missing assignments, out-of-domain rows, and boundary samples. Counts can match when one occurrence is duplicated and another omitted.

For very large populations, exact identity reconciliation may use sorted/partitioned anti-joins or governed canonical digests plus count/sum controls. Hashes require collision and canonicalization policy and do not replace key-level investigation when a control fails.

### Make time partitions unambiguous

Name the time role: event, effective, transaction, ingestion, extraction, or publication time. A partition labeled `date=2026-09-02` is meaningless without role and zone.

Convert instants to the governed zone before deriving calendar partitions. UTC days are always 24 hours in the civil representation; named local days can cover 23 or 25 elapsed hours around daylight-saving transitions. Do not assume fixed seconds per local day.

Use half-open instant bounds and preserve source precision. A record exactly at midnight belongs to the new day, not both. Timestamp truncation before zone conversion can assign a different date than conversion before truncation.

Late events can write to old event-time partitions even when the current ingestion partition is new. Track both roles if operations need them. Retention and backfill must not infer event completeness solely from recent ingestion paths.

### Classify every operator

A row-local map/filter can usually process each occurrence partition independently, provided side inputs, errors, and ordering do not introduce cross-partition state. The union of local outputs then matches the whole-dataset transformation.

Aggregations are composable when a sufficient partial state combines associatively with an identity element. Count uses integer addition; sum uses an appropriate exact or numerically governed addition; min/max combine extrema; mean uses `(sum,count)`. Variance needs count/mean/second-moment state under a numerically stable method.

`distinct`, exact median/quantile, global sort, dense ranking, top-N, many windows, and graph algorithms require global or richer coordination. Local distinct followed by union is not globally distinct unless another deduplication stage occurs. Local top ten per partition contains candidates for global top ten, but only a second global selection establishes the answer.

Windowed operations near range boundaries may need halos/overlap. Define which partition owns each output row, how neighboring context is fetched, and how duplicated context is discarded. Overlap in execution input does not permit duplicate logical output.

### Prove partial aggregation

Let local state be $s_i=f(P_i)$ and combine operation $\oplus$. To parallelize safely, the state must be sufficient and combination must be associative for the execution grouping; commutativity is also needed when arrival order is arbitrary unless the runtime preserves order.

For mean, compute

$$
(S,N)=\bigoplus_i(S_i,N_i)=\left(\sum_i S_i,\sum_i N_i\right),\qquad \bar{x}=S/N.
$$

If partition A contains one value 0 and partition B contains nine values 10, partition means are 0 and 10. Their unweighted mean is 5, but the global mean is 9. State design is semantic correctness.

Floating addition is mathematically associative but not generally associative in finite precision. If repeatability or error is material, use exact integer/decimal units, compensated/pairwise strategies, bounded error/tolerance, and recorded reduction behavior. Do not promise bit identity across arbitrary repartitioning without evidence.

### Understand shuffle boundaries

A shuffle redistributes records so keys or ranges required by the next operator become colocated. It can involve serialization, network transfer, map-side files/state, reduce-side buffers, sorting, spilling, and recovery artifacts.

Spark’s current RDD guide describes shuffle as data redistribution that is complex/costly and can consume heap/spill to disk. The principle is general, but exact mechanics are engine/version-specific. Inspect the actual physical plan and metrics.

Reduce shuffle volume through semantically safe projection/filter, map-side partial aggregation, compatible existing partitioning, and broadcast of truly bounded sides. Avoid `groupByKey`-like materialization when a mergeable aggregate can combine early, but verify UDF/aggregation algebra.

Shuffle partition count trades task overhead against per-task state. The count is not a correctness control by itself. Measure bytes and hot keys after filters, not only input file count.

### Engineer joins by placement and cardinality

A colocated join requires both sides to assign equal canonical keys compatibly and makes corresponding partitions available together. Same bucket count or similarly named columns does not prove compatible hash, type, null, normalization, or spec.

A broadcast join sends a bounded relation to workers processing the large side. It avoids repartitioning the large side but multiplies memory/network distribution and risks executor failure if estimates are wrong. Bind the exact broadcast generation and enforce a hard size/capacity gate.

A shuffle join repartitions one or both sides by join key. It is robust for large relations but expensive and sensitive to skew. Pre-aggregate many sides where output grain permits, validate key multiplicity, and record unmatched/fanout distributions.

Range and sort-merge joins need compatible ordering/bounds and handling for boundary keys. Null/missing matching is library-specific. Many-to-many joins can create quadratic hot-key output even if input partitions are balanced; estimate per-key cross-products.

### Detect skew in several dimensions

Skew is not only row count. Measure compressed and decoded bytes, variable-width payload, records, distinct keys, per-key frequency, join expansion, aggregation state, CPU cost, UDF latency, output bytes/files, spill, and task duration.

Report distributions: min, median, high percentiles, max, top heavy hitters, and fraction held by top keys/partitions. The maximum often determines completion. A stage with 99 fast tasks and one two-hour task takes at least about two hours absent a correct split.

Diagnose cause: natural tenant dominance, null/default key, coarse time bucket, bad hash/canonicalization, one huge compressed file, many-to-many join, variable algorithmic cost, or downstream storage throttling. Different causes require different remedies.

Adaptive execution may split skewed shuffle partitions or change join strategy. Spark documents such capabilities in its current performance guide. Treat adaptive plan choices as versioned physical behavior and retain semantic/resource evidence.

### Mitigate skew without changing meaning

Increase partition count for broadly distributed load, use range bounds learned from representative/current distributions, isolate known heavy keys, pre-aggregate, broadcast a bounded side, or split oversized source objects where formats permit.

Salting adds a sub-key to split one logical key across tasks. It requires a second combine/desalt stage for aggregations. For joins, one side may need controlled replication across salts. Prove that every intended pair appears once and that replicated measures are not double-counted.

Handle null/default keys separately rather than letting them form one accidental hotspot. Preserve null semantics and security classifications; distributing missing keys randomly may destroy the ability to diagnose them.

Skew mitigations can move cost elsewhere: more tasks, replicated data, larger metadata, another shuffle, and complicated recovery. Benchmark end-to-end including failure, not only the once-successful hot task.

### Choose partition and file size empirically

Target enough tasks to use available parallelism without overwhelming scheduling, listing, or metadata services. Each task needs input, decoded state, joins/aggregates, spill, output buffers, and failure headroom within worker limits.

Small partitions create short tasks but increase scheduler overhead and output files. Huge partitions reduce overhead but increase stragglers, memory/spill, retry cost, and lost parallelism. Splittability, compression, row groups, and locality matter.

Output data partitions and files are separate. A day partition can contain several appropriately sized files; one task can write several values; compaction can change file layout without changing logical rows. Do not encode “one partition equals one file” as a consumer contract.

Apache Arrow’s dataset guide gives current practical file/partition extremes for its implementation, but those numbers are not universal. Measure your reader/catalog/object store/query engine and workload. Record file-count and metadata/listing SLOs along with scan bytes.

### Design output for pruning

Choose data partition transforms from common selective predicates, data distribution, update/backfill behavior, retention, privacy, and engine support. Low-cardinality time buckets are common; high-cardinality identifiers can create excessive directories/files.

Partition pruning is physical elimination based on trusted metadata. It must not change query semantics. Readers still apply the logical predicate to rows. Missing or corrupt statistics may reduce pruning but must not omit qualifying records.

Arrow documents that hive-like partition fields can be inferred/declared from paths and used to avoid loading irrelevant files. Explicit schemas are safer than path type inference. Validate that path values, embedded data, and manifests agree.

Parquet organizes data into row groups and pages with metadata that readers can use for selective scans. Row-group/file sizing and statistics complement, not replace, table/data partitioning. Sensitive statistics also require access consideration.

### Separate logical columns from physical partition transforms

Exposing a manually maintained `event_date` column can couple queries and writers to physical layout. Writers may derive it from the wrong timestamp/zone; readers may forget the redundant predicate; changing layout can break code.

Apache Iceberg documents hidden partition transforms and partition evolution, separating logical query columns from physical layout. That is a product capability, not a reason to assume every table format evolves partitions safely.

Record partition spec ID with every data file/snapshot where the table format requires it. During evolution, old and new files can use different specs; planning metadata must interpret both. Do not rewrite path names without table metadata and commit semantics.

Changing partitioning should preserve logical rows and schema. Validate key multisets, counts, additive controls, predicate results, pruning plans, and reader compatibility before and after. Physical rewrite receipts and old snapshots support rollback.

### Make retries and speculation safe

Let logical partition ID identify the intended input/bounds/output responsibility; let attempt ID identify one execution. Every attempt writes to an isolated path/object set containing both IDs and never mutates the trusted generation.

On success, an attempt produces a receipt: input manifest slice, code/config/runtime, schema, row/byte counts, rejects, output object versions/digests, metrics, and completion state. A coordinator validates and selects at most one acceptable attempt per logical partition.

Speculative duplicates are expected. They may execute the same pure transformation twice, but only one output enters the committed generation. Do not rename both attempts into a shared directory or rely on last writer wins.

External side effects inside tasks break replay. Do not send emails, charge accounts, update unkeyed services, or use mutable remote lookups per record. Materialize/version side inputs and keep processing pure; move necessary effects behind an idempotent outbox/commit boundary.

### Build an exact generation manifest

Before execution, define expected logical input/output partition identities or a rule that resolves to an immutable set. After execution, assemble exactly one accepted receipt for each required logical partition, plus explicit empty-partition representation where needed.

The generation manifest includes dataset/contract/schema/partition-spec versions; source generation and object list; code/runtime/config; accepted attempt/output objects; per-partition counts/statistics/digests; quarantine; aggregate controls; and prior generation.

Validate no missing, extra, duplicate, overlapping, unowned, or stale output objects. Directory listing is supporting observation, not authority. Files from failed/retried jobs can coexist physically but stay unreachable from the manifest until garbage collection.

Readers resolve the committed manifest/snapshot. They do not glob a prefix whose contents change during writes. This converts at-least-once task execution into once-selected logical data effects for the generation.

### Publish the whole dataset atomically

Candidate partitions can finish in any order. None becomes trusted merely because its path exists. Run partition-level gates early for feedback, then whole-generation controls that need the exact set.

Publish via a table-format snapshot/catalog transaction, atomic metadata rename where actually supported, or conditional pointer update from expected prior generation to candidate manifest. A compare-and-swap condition prevents a late job/backfill from overwriting a newer generation.

Record publication receipt with prior/new snapshot, manifest digest, transaction/job ID, gate summary, publisher, and commit time. On timeout, look it up before retrying. A client exception does not prove that the server/catalog failed to commit.

Rollback selects a retained prior valid manifest or governed compensating snapshot. Never “roll back” by deleting new files while readers might still reference them. Garbage collection follows reachability, retention, active-run leases, and audit policy.

### Coordinate concurrent runs and backfills

Scheduled runs, reruns, backfills, repairs, compaction, and schema/spec evolution can target overlapping logical partitions. Declare ownership and serialization rules. Partition-disjoint physical writes may still conflict at the table manifest/pointer.

Never let a backfill overwrite an entire dynamic partition set inferred from whatever rows it produced; a missing input slice could delete good data. Bind the exact intended replacement scope and compare prior identities.

If live and historical jobs can both update one table, use branches/staging snapshots or conditional commits and reconcile conflicts. A later wall-clock attempt is not automatically semantically newer; source/event/version authority decides.

Compaction should preserve logical content while replacing physical files. Treat it as a snapshot change with before/after equality checks under the contract. Keep lineage from old to new objects and respect concurrent readers.

### Validate locally and globally

Partition gates check readability, schema/spec, bounds, occurrence identity, null/invalid keys, count/bytes, key distributions, local duplicates, output files, digest, and resource limits. Boundary fixtures include exactly-at-lower/upper, time-zone transitions, min/max values, and nulls.

Global gates check expected partition set, overlap/gaps, global duplicate keys/occurrences, cross-partition relationships, additive reconciliation, global distinct/top-N/window outcomes, schema consistency, file counts/sizes, quarantine totals, security, and consumer questions.

Per-partition uniqueness does not prove global uniqueness unless the partition function colocates equal keys. State that premise and test it. Likewise, every partition passing its own count cannot prove the expected set is complete.

Metamorphic tests repartition the same immutable input with several bucket counts/orders and compare canonical outputs for partition-invariant operations. They split/merge files, retry attempts, insert empty partitions, and move boundary records. Differences localize hidden partition dependence.

### Observe data and control planes

Record source objects/versions, scan partitions, execution stages/tasks/attempts, shuffle read/write, spill, skew, cache, broadcast, input/output rows/bytes, rejects, per-key/fanout distributions, file/row-group sizes, metadata/listing latency, pruning ratio, and cost.

Control-plane state includes run/attempt IDs, expected/accepted partitions, leases, plan/config/runtime, receipts, manifest assembly, validation, publication, rollback, compaction, and garbage collection. Metrics without these dimensions cannot distinguish two attempts or generations.

Alert on missing/duplicate expected partitions, unresolved attempts, broken reconciliation, hot-partition SLOs, excessive spill/shuffle, small-file growth, failed commits, stale pointers, and rollback-window risk. Use SLO burn and invariant breaches rather than noisy per-task variation alone.

Retain plan and distribution histograms across upgrades. Adaptive engines may change partition counts/joins; data distribution can shift even when code does not. Performance drift can be the first evidence of a semantic key/default problem.

### Secure partitioned processing

Partition paths and values can expose tenant, date, region, diagnosis, or other sensitive categories through metadata even if file contents are encrypted. Choose transforms and catalog visibility under privacy policy.

Do not assign one tenant per task and then share credentials/logs/caches without isolation. Enforce source/object/table permissions, tenant predicates, encryption, spill/temp cleanup, and least-privilege candidate/publish roles. Test cross-tenant joins and output placement.

Quarantine partitions may be more sensitive than accepted output because they retain raw values and error reasons. Restrict and retain them separately. Logs should report bounded protected identifiers/digests, not dump records.

Broadcast side inputs are copied across workers and may expand exposure. Verify authorization, encryption, memory cleanup, and necessity. Partition pruning is a performance feature, not an authorization control; a reader allowed only one tenant must be denied access independently of filters.

### Evolve and recover deliberately

Schema and partition-spec changes require compatibility across all concurrently readable files and engines. Pin reader/writer/table-format versions, validate old/new mixtures, and keep exact snapshot history. Avoid partial rewrites that leave ambiguous path conventions.

Recovery restores metadata and data. A successful catalog restore pointing to missing objects is not recovery; intact files without the authoritative manifest are also insufficient. Test manifest/catalog backup, object retention/versioning, credentials, and engine replay.

Run a full drill: resolve an old immutable input, execute with recorded partition contract/runtime, accept exactly one attempt per logical partition, validate global equality or approved differences, publish to isolation, and measure recovery time/cost.

After incidents, strengthen durable mechanisms. A missed midnight row calls for half-open bound generators and boundary tests; duplicate retry files call for attempt isolation/manifest selection; a hot null bucket calls for explicit null policy and skew gates.

## Definitions and Notation

Let:

- $D$ be the intended source occurrence bag for one immutable generation;
- $q$ be the number of logical execution/input buckets under a named plan;
- $p(x)$ be a deterministic single-valued assignment for valid occurrence $x$;
- $P_i=\{x\in D:p(x)=i\}$ be logical partition $i$;
- $f(P_i)$ be partition-local partial state;
- $(A,\oplus,e)$ be a merge-state algebra with associative combine and identity;
- $T_i$ be duration of the critical task path for partition $i$;
- $r$ be logical run identity and $a$ an attempt identity;
- $O_{i,a}$ be objects written by attempt $a$ for logical output partition $i$; and
- $M_r$ be the candidate generation manifest selecting accepted attempts.

Coverage and disjointness at occurrence level are jointly written as

$$
\biguplus_{i=0}^{q-1}P_i=D.
$$

For adjacent ordered bounds $b_0<\cdots<b_q$, define $P_i=[b_i,b_{i+1})$. Then $P_i\cap P_{i+1}=\varnothing$ and their union covers $[b_0,b_q)$, subject to explicit null/out-of-range policy and one comparison type/precision.

A mergeable transformation satisfies

$$
F(D)=\bigoplus_i f(P_i).
$$

This is a homomorphism obligation for the chosen state, not a property of every final statistic. Mean state combines as `(sum,count)`; unweighted partition means generally fail.

If key $k$ has $a_k$ left and $b_k$ right occurrences, an equality join can produce $a_kb_k$ pairs. Partitioning changes placement, not multiplicity. Skewed keys can therefore dominate output/state even with equal input row counts.

With sufficient workers and no other bottleneck,

$$
T_{stage}\geq\max_iT_i.
$$

Scheduling, dependency, resource, and network constraints normally make actual duration larger.

Manifest acceptance requires exactly the expected logical partition identities $I$ and one chosen attempt each:

$$
\operatorname{keys}(M_r)=I,\qquad \forall i\in I:\left|\operatorname{acceptedAttempts}(i)\right|=1.
$$

Multiple physical attempt outputs may exist, but only selected $O_{i,a}$ objects are reachable from the published snapshot.

## Mechanisms, Invariants, or Proof Structure

A partitioned-processing review should:

1. freeze the exact source generation/object versions and occurrence population;
2. define/version partition key, type/encoding, hash/ranges/time zone, null/error policy, and expected identities;
3. prove coverage/disjointness with boundary cases and occurrence-level reconciliation;
4. classify each operator as local, mergeable, colocated, halo-dependent, broadcast, shuffle, or global;
5. prove partial-state combine, join cardinality/placement, and any salt/desalt or overlap/output-ownership scheme;
6. measure rows, bytes, keys, cross-products, CPU, state, shuffle, spill, skew, task time, and file/metadata effects;
7. write every retry/speculative attempt to isolated objects with immutable receipts;
8. assemble exactly one accepted attempt for every expected logical output partition into a complete manifest;
9. run partition and global schema/key/reconciliation/security/performance gates, then publish conditionally/atomically; and
10. retain source, plans, receipts, prior/new manifests, files, lineage, and metrics for rollback, evolution, and recovery.

The finite model below uses a deliberately simple stable teaching hash (sum of Unicode code points modulo bucket count) so its arithmetic is visible. Production hashing needs a named canonical byte encoding and suitable stable distribution algorithm. It demonstrates partition coverage, mergeable `(count,sum)` state, repartition equivalence, and manifest selection of one retry attempt. It does not model distributed engines, collisions/adversarial distribution, files, shuffles, speculation races, transactions, performance, or production publication.

<!-- bijux-verify: {"id":"partition-coverage-and-manifest","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"events=8\nunique_events=8\npartition_counts_3=(2, 3, 3)\npartition_counts_4=(3, 2, 2, 1)\ncustomers=((\u0027c1\u0027, 2, 80), (\u0027c2\u0027, 2, 100), (\u0027c3\u0027, 2, 25), (\u0027c4\u0027, 1, 5), (\u0027c5\u0027, 1, 30))\ntotal_cents=240\nrepartition_equivalent=True\nmanifest_exact_once=True\n","stderr":""}} -->
```python
from collections import defaultdict

EVENTS = (
    ("e1", "c1", 100),
    ("e2", "c2", 40),
    ("e3", "c1", -20),
    ("e4", "c3", 10),
    ("e5", "c2", 60),
    ("e6", "c4", 5),
    ("e7", "c3", 15),
    ("e8", "c5", 30),
)

def bucket_for(customer_id, count):
    return sum(ord(character) for character in customer_id) % count

def divide(events, count):
    buckets = [[] for _ in range(count)]
    for event in events:
        buckets[bucket_for(event[1], count)].append(event)
    return tuple(tuple(bucket) for bucket in buckets)

def partial(bucket):
    state = defaultdict(lambda: [0, 0])
    for _, customer_id, cents in bucket:
        state[customer_id][0] += 1
        state[customer_id][1] += cents
    return tuple((key, *state[key]) for key in sorted(state))

def merge(partials):
    state = defaultdict(lambda: [0, 0])
    for part in partials:
        for customer_id, count, cents in part:
            state[customer_id][0] += count
            state[customer_id][1] += cents
    return tuple((key, *state[key]) for key in sorted(state))

three = divide(EVENTS, 3)
four = divide(EVENTS, 4)
result_three = merge(tuple(partial(bucket) for bucket in three))
result_four = merge(tuple(partial(bucket) for bucket in four))

# Logical partition 1 ran twice. The manifest selects only attempt 2.
attempts = {
    (0, 1): three[0],
    (1, 1): three[1],
    (1, 2): three[1],
    (2, 1): three[2],
}
manifest = {0: 1, 1: 2, 2: 1}
accepted_events = tuple(
    event
    for partition_id in sorted(manifest)
    for event in attempts[(partition_id, manifest[partition_id])]
)

expected_ids = sorted(event[0] for event in EVENTS)
accepted_ids = sorted(event[0] for event in accepted_events)
print(f"events={len(EVENTS)}")
print(f"unique_events={len(set(expected_ids))}")
print(f"partition_counts_3={tuple(len(bucket) for bucket in three)}")
print(f"partition_counts_4={tuple(len(bucket) for bucket in four)}")
print(f"customers={result_three}")
print(f"total_cents={sum(row[2] for row in result_three)}")
print(f"repartition_equivalent={result_three == result_four}")
print(f"manifest_exact_once={accepted_ids == expected_ids}")
```

The example uses exact integer state, so partition regrouping is exact. Replacing cents with floating values can change low-order bits under another reduction tree. The manifest equality compares occurrence IDs; comparing only eight rows could miss one duplicated and one omitted event.

## Alternatives and Trade-Offs

**Hash versus range.** Hashing often balances ordinary key distributions and colocates equality keys but destroys locality and changes assignment with bucket-count/spec changes. Ranges support ordered scans and pruning but need boundaries, skew monitoring, and explicit edge ownership.

**Time versus categorical partitioning.** Time aligns retention and common temporal scans. Categories/tenants can improve isolation/pruning but create skew, sensitive metadata, and high cardinality. Composite transforms may help while multiplying partition counts.

**Visible versus hidden partitions.** Visible directory columns are simple and widely compatible but couple writers/readers to physical layout. Table-managed hidden transforms reduce that coupling and support evolution when the chosen format/engines implement them correctly.

**Many small versus fewer large partitions.** Small units increase parallelism and reduce individual retry cost, while increasing scheduling, listing, manifests, files, and open overhead. Large units reduce overhead and increase scan, straggler, memory/spill, and retry cost.

**Repartition versus coalesce/combine.** Full repartition can improve distribution and key placement at shuffle cost. Coalescing reduces tasks/files with less movement but may retain skew and lose parallelism. Verify engine semantics and downstream requirements.

**Broadcast versus shuffle join.** Broadcast avoids moving the large side when the small side is truly bounded and authorized on every worker. Shuffle handles two large sides but costs network/disk and exposes skew. Estimates require hard runtime guards.

**Static bounds versus adaptive partitioning.** Stable bounds improve predictability/reuse. Adaptive plans respond to current sizes/skew but complicate plan reproducibility and can change task/file layout. Semantic output must remain invariant.

**Salting versus heavy-key isolation.** Salting distributes one key generically but needs replication/recombination proof. Isolating known heavy keys can be simpler and more observable but requires detection and a separate path.

**Local partial state versus raw shuffle.** Combining early reduces network/state for associative sufficient statistics. It is invalid for arbitrary functions or incomplete state. Prove the algebra before optimizing.

**File listing versus table manifest.** Listing is broadly available but mutable, costly, and not transactional. Table manifests/snapshots establish exact membership and evolution at catalog/format complexity. Trusted large datasets benefit from explicit membership.

**In-place partition overwrite versus new generation.** In-place overwrite uses less temporary storage but exposes gaps/races and weak rollback. Isolated snapshots/generations cost storage yet provide validation and atomic publication.

**Global exact versus approximate result.** Exact distinct/quantiles can demand large coordination/state. Sketches bound resources but add approximation/error/merge-version contracts. Use them only when consumers approve the semantics.

**Compaction on write versus asynchronous compaction.** On-write sizing yields cleaner immediate layout and longer/heavier writes. Asynchronous compaction separates latency but creates concurrent snapshots, extra storage, and another correctness workflow.

## Failure Modes and Misconceptions

- **“A file is a partition.”** A file can contain row groups and feed many tasks; tasks can combine files; one data partition can hold many files.
- **“Execution partition ID is stable.”** Optimization, retries, stage changes, or engine versions can renumber/split/coalesce it.
- **“Partitioning is only performance.”** Assignment controls coverage, joins, retries, lifecycle, security metadata, and publication.
- **“Equal counts prove coverage.”** One duplicated and one missing occurrence preserve the count. Compare identities/bounds.
- **“Inclusive daily ends are intuitive.”** Adjacent inclusive intervals overlap at midnight. Use half-open bounds.
- **“A day is 86,400 seconds.”** Named local days can differ around civil-time transitions. Define time role/zone.
- **“Default hash is deterministic.”** Language/runtime hashes may be randomized or change. Name algorithm/encoding/spec.
- **“Per-partition uniqueness is global uniqueness.”** Only when equal keys are provably colocated by the partition contract.
- **“Partition means can be averaged.”** Unequal partition sizes require sum/count state.
- **“Local distinct is distinct.”** Equal values in different partitions survive without a global dedup stage.
- **“Local top-N is global top-N.”** It supplies candidates; a second selection is needed, with tie/order rules.
- **“Partitioning both sides makes a join local.”** Keys, types, hash/range, bucket counts, nulls, and spec must be compatible.
- **“Broadcast is free.”** It replicates bytes/state and sensitive data and can exceed each worker’s memory.
- **“More partitions fix skew.”** A single unsplit hot key may still land in one task and dominate.
- **“Salting changes only performance.”** Incorrect replication/desalting can omit or duplicate pairs/measures.
- **“Lazy/adaptive execution always balances work.”** Engine mechanisms have limits and versioned triggers; inspect metrics.
- **“One file per task is desirable.”** It couples physical output to execution and can generate small files.
- **“Path partitions are trustworthy.”** A wrong path transform can make pruning omit qualifying rows.
- **“Pruning is authorization.”** It is an optimization; access policy must deny unauthorized data independently.
- **“All task successes mean the generation is complete.”** Expected partition set, accepted attempts, and global gates still need proof.
- **“Retry output can use the same path.”** Concurrent/speculative attempts can corrupt or overwrite one another.
- **“Exactly once means each task ran once.”** Tasks may repeat; manifest selection can still expose each logical occurrence once.
- **“Directory listing is a commit.”** Readers can observe partial/stale/failed attempt files. Resolve a committed manifest.
- **“Overwrite partition is isolated.”** Dynamic scope, concurrent writers, and product commit rules can delete or race.
- **“Compaction changes no data by definition.”** It is a new physical snapshot that requires equality and commit evidence.

## Worked Examples

### Example 1

A source manifest has four object versions, but each worker also expands a wildcard. A fifth object arrives mid-run and is read by only later tasks. The repair assigns manifest slices centrally, rejects unlisted objects, records object versions/digests, and proves occurrence identity union equals the manifest population.

### Example 2

Daily tasks use `[00:00,24:00]` for both neighboring dates. An event at exactly midnight appears twice. Half-open `[start,next_start)` bounds assign it to the later day exactly once. Tests cover precision immediately before, at, and after every boundary in the governed zone.

### Example 3

Partitions contain one value 0 and nine values 10. Local means are 0 and 10; their mean is 5. Combining states `(0,1)` and `(90,9)` gives `(90,10)` and global mean 9. The state, not final mean, is the mergeable object.

### Example 4

Orders are hash-bucketed with one algorithm/modulus; refunds use another runtime’s default hash and equal bucket count. Same order IDs are not necessarily colocated. The engine must repartition both on one canonical key/spec or use an alternative join. Bucket number equality alone proves nothing.

### Example 5

One null customer key holds 35% of rows and all lands in one reducer. The team first separates invalid/missing identities into governed quarantine/recovery flows. If legitimate unknown grouping remains, it uses an explicit strategy and preserves reason/state rather than randomly scattering records and losing semantics.

### Example 6

A huge tenant causes a many-to-many join cross-product. Increasing partitions does not split the single key. The team resolves unintended duplicates, pre-aggregates at the intended grain, estimates $a_kb_k$, and only then considers salting with controlled replication and a proven recombination stage.

### Example 7

One logical partition has two successful speculative attempts. Both wrote isolated object sets. The coordinator validates receipts, selects attempt 2 in the candidate manifest, and leaves attempt 1 unreachable. Readers see one set; later garbage collection removes the unreferenced objects after safety/retention checks.

### Example 8

All expected data partitions have paths, but one path contains files from an old failed run and another lacks an empty-partition receipt. A listing-count gate passes incorrectly. Exact manifest assembly rejects stale run IDs, missing accepted attempt, unexpected objects, and absent emptiness evidence.

### Example 9

A table changes from monthly to daily partition transforms. Old files remain monthly while new files are daily. A format supporting spec-aware planning reads both through metadata. The team validates logical equality and pruning across both specs and does not force consumers to add both physical predicates.

### Example 10

Two thousand tasks each write a 1 MB Parquet file, making scans metadata-bound. Compaction produces appropriately sized files in a new snapshot, compares key multisets/counts/sums/schema, conditionally publishes, and retains the old snapshot for rollback. It never rewrites files under the active manifest in place.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partitions, retries, speculation, idempotent effects, consistency, conditional writes, failure detection, and distributed transactions. Partitioned data processing is a concrete distributed system.

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects stable hashing, range indexes, heaps/top-N, mergeable summaries, sketches, columnar buffers, sort/merge, and external-memory algorithms.

[Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) connects work/span, lower bounds, hashing, sorting, selection, aggregation, and the fact that parallelism cannot remove sequential/global dependencies or worst hot partitions.

[Database Engineering](../../18-database-engineering/ROADMAP.md) connects partitioning, pruning, statistics, joins, aggregation, transactions, indexes, table formats, query planning, and schema evolution.

[Operating Systems](../../22-operating-systems/ROADMAP.md) connects scheduling, memory, paging, filesystems, caches, I/O, processes, resource isolation, and failure. Task/partition sizing ultimately meets these physical limits.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects requirements, interface boundaries, capacity, hazards, verification evidence, configuration control, recovery, and lifecycle evolution.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects schedulers, runtimes, object stores, catalogs, managed table formats, quotas, observability, policy, cost governance, and safe self-service defaults.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects tenant isolation, path/metadata leakage, least privilege, encryption, sensitive spill/quarantine, audit, and recovery access.

## References

1. Apache Spark, [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html). Documents datasets partitioned across nodes, transformations/actions, partition counts, key-value operations, shuffle redistribution, memory/spill, persistence, and recovery. Accessed 2026-09-02.
2. Apache Spark, [Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html). Documents file/partition planning, repartition/coalesce hints, join strategies, adaptive coalescing, and skew handling. Accessed 2026-09-02.
3. Dask project, [DataFrame Design](https://docs.dask.org/en/stable/dataframe-design.html). Documents partition graph keys, metadata, partitions, known/unknown index divisions, pruning, grouping, and output partition choices. Accessed 2026-09-02.
4. Apache Arrow, [Tabular Datasets](https://arrow.apache.org/docs/python/dataset.html). Documents multi-file datasets, scanning, filtering/projection, partition schemes, writing partitioned datasets, and layout/file-count trade-offs. Accessed 2026-09-02.
5. Apache Iceberg, [Partitioning](https://iceberg.apache.org/docs/latest/partitioning/). Explains partition transforms, hidden partitioning, pruning, layout correctness concerns, and partition evolution. Accessed 2026-09-02.
6. Apache Iceberg, [Table specification](https://iceberg.apache.org/spec/#partitioning). Specifies partition specs/fields/transforms, data-file partition tuples, evolution, manifests, snapshots, and commit-related metadata. Accessed 2026-09-02.
7. Apache Hadoop, [MapReduce Tutorial](https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html). Documents input splits, mapper/reducer partitions, partitioners, sorting/grouping, task execution, counters, and output commit concepts. Accessed 2026-09-02.
8. Apache Parquet, [File format](https://parquet.apache.org/docs/file-format/). Describes hierarchical file, row-group, column-chunk, page, and footer metadata layout supporting columnar processing. Accessed 2026-09-02.
9. OpenLineage, [Object model](https://openlineage.io/docs/spec/object-model/). Defines Job, Run, Dataset, run events, dataset facets, and input/output relationships useful for partition-attempt lineage. Accessed 2026-09-02.

## Exercises

### Exercise 1

Define hourly range partitions over UTC instants from `2026-09-02T00:00Z` through `2026-09-02T03:00Z`. Assign events at `00:00`, `00:59:59.999`, `01:00`, `02:59:59.999`, and `03:00`. State the covered population, boundary convention, ownership, and how you would prove no event was duplicated or omitted.

### Exercise 2

Partition A contains values `(0)` and partition B contains nine values each equal to `10`. Compute the unweighted mean of partition means and the correct global mean. Give mergeable state and combine rule. Explain how floating arithmetic can affect repartition reproducibility even when the algebra is correct.

### Exercise 3

A join key `hot` occurs 4,000 times on the left and 2,000 times on the right. All other keys are balanced. Compute the potential output pairs for `hot`, explain why increasing ordinary hash bucket count does not split it, and design two semantically safe mitigation candidates with required proofs.

### Exercise 4

A job expects logical partitions `{0,1,2,3}`. Attempts `(0,a)`, `(1,a)`, `(1,b)`, and `(3,a)` succeed; partition 2 has no receipt, and both partition-1 attempts wrote visible files. Design candidate-manifest validation, publication behavior, retry, and cleanup. Explain why four successful attempt directories do not imply completeness.

### Exercise 5

A table currently uses a visible local-date directory derived manually from `event_time`; the team wants a hidden `day(event_time)` transform and larger compacted files. Design a migration/verification plan covering time zone, old/new specs, logical equality, pruning, concurrency, publication, rollback, security metadata, and reader compatibility.

## Answers to the Exercises

### Answer 1

Use `[00:00,01:00)`, `[01:00,02:00)`, and `[02:00,03:00)` in UTC at the declared source precision. `00:00` and `00:59:59.999` belong to partition 0; `01:00` belongs to partition 1; `02:59:59.999` belongs to partition 2. `03:00` is outside this covered population and belongs to the next interval if it is included in a following run.

Freeze the exact source occurrence manifest, assign each ID through one bound generator, and compare the bag union of assigned IDs with expected in-range IDs. Assert one assignment for each in-range occurrence, none for out-of-range occurrence, and test exact boundaries plus representable instants immediately before/after. Counts alone cannot prove this.

### Answer 2

Partition means are 0 and 10, so their unweighted mean is 5. Global sum is $0+9(10)=90$ over 10 values, so the correct mean is 9. Use state `(sum,count)`, identity `(0,0)`, and componentwise addition; divide the final sum by final count under the empty policy.

Floating addition is not generally associative in finite precision. Different partition/reduction trees can round in different orders. Use exact integer/decimal units when required, a numerically stable combine, or declared tolerances/error bounds and canonical tests. Algebraic sufficiency does not by itself guarantee bit-identical floating output.

### Answer 3

The hot key can produce $4{,}000\times2{,}000=8{,}000{,}000$ pairs. Ordinary hash partitioning sends all equal canonical keys to the same bucket, so a larger bucket count does not split the key within one run/spec.

First ask whether the many-to-many relation is intended. If duplicates or pre-aggregatable measures exist, resolve identity and aggregate each side to the required join grain; prove keys, fanout, and measure conservation. If every pair is truly required, salt the hot key across controlled subkeys: distribute left records, replicate or compatibly assign right records so every intended pair appears exactly once, retain original identity, and validate pair-count/set equality during desalt/output. Alternatively isolate `hot` into a dedicated bounded algorithm/resource path and union it with ordinary keys, proving disjoint key coverage and output equality. All candidates need memory/output-volume gates because eight million pairs are semantically large even when balanced.

### Answer 4

The expected set is not satisfied: logical partition 2 is missing, while logical partition 1 has two physical attempts. The coordinator validates receipts but selects at most one acceptable attempt for partition 1; it does not infer acceptance from visibility. It blocks publication until partition 2 succeeds or the contract supplies an explicit valid empty receipt.

Retry only logical partition 2 against the same immutable input slice/code/config, writing a new isolated attempt. Assemble manifest keys exactly `{0,1,2,3}`, one accepted attempt/object set each, and run global reconciliation before conditional publication. Leave the unselected partition-1 attempt unreachable; garbage-collect it only after active-run, retention, and rollback checks. Four attempt directories count executions, not complete logical ownership.

### Answer 5

Freeze a source/table snapshot and define whether the logical day is UTC or a named zone, including DST and timestamp precision. Audit the existing manual directories against event timestamps and quarantine discrepancies. Pin a table format/engine combination that supports the hidden transform and mixed partition-spec planning; register a new spec rather than rewriting paths outside metadata.

Write/compact candidate files under the new spec and isolated snapshot. Compare canonical occurrence/business-key multisets, schemas, null/time values, counts, additive measures, both set differences, boundary-day queries, and business outputs against the old logical snapshot. Verify readers plan both old and new specs and that logical `event_time` predicates prune correctly. Measure files, metadata, scans, tasks, and cost.

Serialize or conditionally reconcile concurrent writes/compaction; publish the new snapshot atomically with expected-prior identity and a receipt. Retain the old snapshot/files for rollback. Review whether old visible paths or new partition metadata reveal sensitive calendar/tenant information, enforce access independently of pruning, test every supported reader version, and deprecate manual partition predicates only after consumer evidence.
