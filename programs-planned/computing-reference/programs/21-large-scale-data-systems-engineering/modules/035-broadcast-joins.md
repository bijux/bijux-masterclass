---
module_id: LSDS-035
program: Large-Scale Data Systems Engineering
level: 1
module_number: 35
title: Broadcast Joins
status: complete
last_verified: 2026-09-03
---

# Broadcast Joins

## One-Page Review

### Governing question

When is it correct and economical to replicate one join input to every worker processing the other input, and how should an engine estimate, distribute, build, reuse, validate, fall back, and govern that replica under real memory, network, statistics, duplicate-key, null, outer-join, concurrency, and failure constraints?

### Essential definitions

- A **broadcast join** replicates one input, the **build side**, to workers or task processes that scan partitions of the **probe side**.
- A **broadcast hash join** constructs a local hash table from the replicated build rows and probes it for each streamed probe row.
- The **preserved side** of an outer join is the side whose unmatched rows must appear in output.
- **serialized size** is bytes transferred or cached in encoded form; **expanded size** includes decoded rows, hash buckets, pointers, duplicate lists, allocator overhead, and workspaces.
- A **broadcast exchange** materializes, validates, distributes, and versions the build-side snapshot.
- A **replica scope** says whether one copy exists per cluster node, worker process, executor, task slot, operator instance, or concurrent task.
- A **broadcast threshold** is a planning guard, not proof that the input fits at runtime.
- **build cardinality** is row count; **build distinctness** and **duplicate multiplicity** determine hash-table and output behavior.
- A **fallback** replaces an unsafe planned broadcast with repartition, sort-merge, nested-loop, or a failed-plan response before incorrect partial output is committed.
- A **broadcast cache** reuses a compatible immutable build artifact across tasks or queries under explicit snapshot and lifecycle identity.

### Central model, mechanism, or theorem

Let build bytes after filtering/projection be $B_s$ serialized. Let expansion factor be $e$ and additional hash/index/workspace memory be $H$, giving per-replica memory estimate $B_m=eB_s+H$. With $W$ replica scopes, aggregate resident memory is about $WB_m$, not $B_m$. A direct source-to-every-worker broadcast transfers roughly $WB_s$ from the source; a tree reduces source fan-out, but the cluster still transmits at least $(W-1)B_s$ to create $W$ copies from one initial copy, excluding retries, compression differences, replicas, and control data.

Correctness for equijoin uses a hash table mapping each normalized build key to all matching build rows. Each probe row looks up its normalized key and emits the Cartesian matches required by join semantics. Duplicate build rows must not be overwritten. Null matching follows the language/SQL predicate, not ordinary map equality. Outer, semi, and anti joins constrain which side may be broadcast and how unmatched rows are emitted.

### Critical invariants

- Build snapshot, filters, projection, schema, key normalization/equality/hash, null semantics, code, and security identity are pinned.
- Runtime build bytes and expanded hash-table memory are measured before or during allocation; stale catalog estimates cannot silently override hard limits.
- Replica scope and concurrent builds are included in worker/container memory admission.
- Every replica receives one complete validated immutable build generation before probing or follows a defined streaming-build protocol.
- Hash entries retain every build row required for duplicate-key multiplicity and join predicates.
- Each probe partition is processed exactly under one compatible build generation for committed output.
- Outer/semi/anti join preserved-side semantics are supported by the chosen broadcast orientation.
- Failed, partial, stale, unauthorized, or incompatible replicas never produce committed output.
- Broadcast transport, retries, decompression, hash construction, cache retention, and eviction are bounded and observable.
- Sensitive build rows follow access, purpose, residency, encryption, retention, and deletion requirements on every replica.

### Common failures

Common failures include selecting from unfiltered table size instead of the post-filter build, comparing compressed storage bytes with heap capacity, ignoring decoded/hash-table expansion, counting one copy per node when the runtime builds one per process/task, forcing hints past hard safety limits, broadcasting several “small” inputs concurrently, overwriting duplicate build keys, treating null as an ordinary equality match, broadcasting the wrong side of an outer/semi/anti join, claiming no shuffle when build distribution still moves data, collecting the build through one memory-constrained coordinator, retrying a failed broadcast while old replicas remain charged, reusing a stale snapshot, exposing restricted dimension data on every worker, and falling back only after probe-side effects have escaped.

### Compact example

An 80 MiB serialized build expands by 1.6 times and needs another 32 MiB for hash/index workspace, so one replica needs about 160 MiB. Across 24 worker processes, aggregate resident memory is 3,840 MiB. Creating 24 copies from one initial copy requires at least 1,840 MiB of cluster data transmission under a simple uncompressed lower bound, even if a distribution tree protects the source from 23 direct sends. Three concurrent compatible-sized builds would require about 480 MiB per worker before probe/operator memory.

### Connections

[LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md) supplies scale accounting, [LSDS-023](023-partitioners-and-combiners.md) supplies key semantics, [LSDS-027](027-task-retry-and-speculation.md) supplies attempt identity, [LSDS-030](030-tracing-a-batch-job-through-a-cluster-engine.md) supplies causal evidence, and [LSDS-031](031-shuffle-architecture.md) through [LSDS-034](034-hash-based-shuffle.md) define alternative exchange/build mechanics. [LSDS-036](../ROADMAP.md) develops repartition joins, the usual large-input alternative.

## Governing Question

Joining two large partitioned relations normally moves both inputs so equal keys meet. If one input is genuinely small, moving the large input can be wasteful. Broadcast the small input everywhere, build a local lookup, and scan each large-input partition in place. The optimization can remove one or two large shuffle exchanges.

“Small” is not a table label. Filters and projection may turn a large source into a tiny build, or data expansion may turn a small compressed file into a large hash table. A 100 MiB estimate can become many gigabytes when replicated across workers and concurrent queries. Duplicate keys, wide variable rows, skew, codecs, object overhead, and allocator behavior matter.

Join semantics constrain orientation. An inner join can usually build either input. A left outer join can broadcast the right/non-preserved side easily because each left probe row can emit matches or one unmatched result locally. Broadcasting the preserved left side while the right is partitioned requires global knowledge to emit unmatched left rows exactly once. Full outer join is harder still.

The governing question is therefore both economic and semantic: can the build be materialized and replicated safely, does the join type permit the chosen orientation, and will the avoided shuffle outweigh distribution/build cost without weakening snapshot, failure, security, or correctness guarantees?

## Why This Matters

Broadcast join can be transformational. A terabyte fact table already partitioned across workers can stream locally while a 20 MiB dimension is distributed once. Avoiding fact repartition reduces network, spill, stage barriers, and tail risk. Reused replicas can serve many probe partitions.

A wrong broadcast plan can terminate the cluster. Expanded build tables compete with probe batches, shuffle buffers, user code, caches, and other joins. Multiple tasks may build duplicate tables in one process. Garbage collection or native allocation can hide the approach to the hard limit. Network incast and coordinator collection can become bottlenecks before worker memory.

Statistics are fallible. Catalog row counts can be stale, filters correlated, variable-width columns misestimated, and user-defined functions opaque. Runtime adaptive planning can make a better decision after materialization, but it needs a safe threshold, an uncommitted plan boundary, and a valid alternative.

Security exposure grows with replication. A restricted lookup table copied to every general-purpose worker expands access surface, residual storage, logs, crash dumps, and deletion obligations. Optimization does not override purpose or residency constraints.

## Prerequisites and Retrieval

Retrieve partitioning, locality, serialization, failure assumptions, and scale accounting from [LSDS-002](002-horizontal-partitioning.md) through [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md). Retrieve block distribution, checksums, metadata, and lifecycle from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md).

Review key/equality and attempts in [LSDS-023](023-partitioners-and-combiners.md) and [LSDS-027](027-task-retry-and-speculation.md), plan construction in [LSDS-025](025-lazy-evaluation-and-plan-construction.md), and shuffle/sort/hash paths in [LSDS-031](031-shuffle-architecture.md) through [LSDS-034](034-hash-based-shuffle.md). You should understand relational inner/outer/semi/anti joins, hash tables, multiplicity, null predicates, serialization expansion, cost estimates, memory admission, tree distribution, immutable snapshots, and fallback planning.

## Learning Objectives

After this module, you should be able to:

1. distinguish build/probe, preserved/non-preserved, serialized/expanded, and per-replica/aggregate sizes;
2. determine valid broadcast orientation for inner, outer, semi, and anti equijoins;
3. estimate worker memory, aggregate replicas, transport lower bounds, and concurrent-build pressure;
4. specify build snapshot, key, duplicate, null, schema, code, and authorization identity;
5. compare driver collection, peer tree, object-store, node cache, executor cache, and per-task distribution;
6. build a correct duplicate-preserving hash table and stream probe-side joins;
7. select static, hinted, runtime-adaptive, cached, or repartition fallback behavior safely;
8. diagnose skew, estimate error, network fan-out, allocation, cache, retry, and stale-data failures;
9. validate join multiplicity and semantics with differential and fault-injection tests; and
10. govern replicated build data through minimization, isolation, encryption, retention, deletion, and access audit.

## Core Exposition

### Logical join semantics before distribution

For inner equijoin, output contains every build/probe pair whose key predicate is true. If one key appears $m$ times on build and $n$ times on probe, it produces $mn$ pairs. A build hash table therefore maps a key to a collection, not one overwritten row.

Left outer join emits those matches plus one null-extended right row for every unmatched left row. Left semi emits each qualifying left row once, regardless of right multiplicity. Left anti emits left rows with no right match. Full outer also emits unmatched rows from both inputs.

SQL null equality normally evaluates unknown, so null join keys do not match under ordinary `=`. Null-safe equality differs. Pin the predicate, key normalization, types/coercions, collation, NaN behavior, and residual non-key condition before choosing physical strategy.

### Choose the build and probe sides

The build should usually be the smaller post-filter/post-projection input because every replica materializes it. The probe side streams or batches through local partitions. Cardinality alone is insufficient: wide rows, duplicates, key width, object representation, and hash load factor determine memory.

Inner join can often swap sides, though output column order and residual predicates still matter. For left outer, semi, and anti joins, broadcasting the right side supports local decisions for each left probe row. For right outer, broadcast the left. Straightforward local broadcast hash join does not support full outer because unmatched build rows seen by no probe must be emitted once globally.

Some engines implement additional bookkeeping or different operators. Record exact engine support and do not infer legality from a hint name.

### Reduce the build before broadcasting

Push filters and required-column projection below the exchange when semantics allow. Avoid broadcasting columns unused by join or output. Deduplicate only if relational multiplicity permits it; a dimension asserted unique can be validated, not assumed.

Preaggregation can reduce rows when the query algebra allows. Bloom filters can reduce probe work but do not replace exact build rows for match output. Compressing the transfer reduces network bytes but not necessarily expanded table memory.

The build artifact records input snapshot, applied filters, projection/schema, row count, serialized bytes, content digest, key contract, and plan/code versions. This makes reuse and reconciliation possible.

### Estimate memory honestly

Measure at least encoded payload, decoded columns/objects, normalized keys, hash bucket array, entry headers/pointers, duplicate lists, load-factor slack, allocator alignment, codec buffers, deserialization workspace, and output-match buffers. Off-heap/native structures still count against container limits.

Expansion varies with schema and runtime. Small strings or boxed numbers can expand many times. Columnar build formats may reduce overhead; hash structures still add indexes. Sample representative rows and validate runtime actuals.

Per-replica estimate must be multiplied by replica scope. If one executor holds one table shared by tasks, count executors; if each operator instance builds independently, count concurrent instances. Include simultaneous queries/joins and retained cache generations.

### Static threshold and cost planning

A planner may broadcast when estimated build bytes fall under a threshold. That threshold is a guard informed by memory and network budgets, not a theorem. It should account for expansion, replica scope, concurrency, probe work, and safety reserve rather than raw source file size.

Cost compares build collection/materialization, distribution, hash construction, probe scan, and cache benefits against repartitioning both sides, sorting/spilling, and stage barriers. Existing co-partitioning or ordering may make a nonbroadcast join cheaper even when build is small.

Statistics confidence matters. Track source snapshot/date, row/byte estimates, distinct counts, width, filters, correlations, and uncertainty. A hint can express knowledge but must not bypass memory, authorization, join-legality, or correctness gates.

### Runtime adaptive choice

An adaptive engine can materialize the candidate build, measure bytes/rows, and choose broadcast before probe-side output commits. This corrects stale estimates and data-dependent filters. It also adds a materialization boundary and delayed decision.

Define hard abort/fallback thresholds for serialized bytes, expanded estimate/actual allocation, rows, distinct keys, largest row, build duration, and distribution time. Fallback must reuse valid materialization when possible without mixing plan generations.

If probe tasks have already emitted irreversible effects, switching strategies can duplicate output. Keep candidate output isolated under plan/attempt identity until one plan generation commits.

### Materialize and validate the build

Read the exact build snapshot and apply pinned transforms. Serialize into bounded chunks with lengths/checksums, or build a transportable columnar artifact. Avoid collecting an unbounded build into one driver heap; use distributed collection or spillable materialization where supported.

Validate row/byte counts, schema, digest, key contract, chunk completeness, access policy, and hard thresholds. Mark the generation complete atomically. Partial chunks are never probeable.

The transport representation can differ from local hash representation. Record both sizes and codec. A decompression bomb or giant row must hit bounded validation before worker allocation.

### Distribution topologies

Direct distribution sends the build from one source to every worker. It is simple and can overload source network/CPU. A tree or peer-assisted broadcast fans out in rounds, reducing source load and critical depth at the cost of coordination and peer trust.

Workers can fetch immutable chunks from replicated object/block storage. This offloads the coordinator but may create synchronized reads against storage. Node-local agents can cache one copy for several executors if isolation and access allow. Executors can deserialize/build once and share read-only state across tasks.

Bound concurrent downloads, bytes, decompression, and table builds. Stagger or tree distribution to avoid cluster-wide allocation spikes. Record topology and retry amplification.

### Build the local hash table

Normalize and hash every admitted build key under pinned semantics. The table stores all matching build rows or compact row references. Choose load factor and collision resolution; verify full key equality after hash match.

Duplicate-heavy keys require lists or ranges and can make output explode during probe. Account for duplicate storage and cap output buffers while preserving semantics. Unique-key optimization is valid only after enforced/validated uniqueness.

The table is immutable during probe. Publishing it to task threads requires safe initialization. A failed build frees all charged memory and cannot leave a partially visible cache entry.

### Probe execution

Stream each probe row, normalize/hash its key, inspect candidates, evaluate full key and residual predicates, and emit according to join type. Backpressure bounds match output, especially for many-to-many keys.

For left outer with right build, no match emits one null-extended row. Semi emits the probe row once after first qualifying match. Anti emits only after proving no qualifying match. Inner emits every qualifying candidate. Null handling follows the predicate.

Probe partitions can run independently because each has a complete compatible build. Exactly-once output still depends on task attempts and sink commit, not broadcast alone.

### Build-side skew and output explosion

Broadcast avoids repartition skew on the probe side, but hot keys still produce large duplicate lists and $mn$ outputs. One probe partition with many hot-key rows can dominate. A tiny build with one duplicated key can generate enormous result data.

Measure build frequency distribution, maximum duplicates, probe frequency, predicted/actual matches, and output per key/partition. Statistics must protect sensitive values through controlled sketches or hashes.

Mitigate only within semantics: validate uniqueness, preaggregate, filter, split hot-key probe work, or choose another strategy. No join algorithm can avoid emitting a required Cartesian multiplicity.

### Cache and reuse

Reuse amortizes distribution and build cost across probe stages or queries. Cache keys include build snapshot/digest, filters/projection, schema, key/equality/hash/null semantics, code/runtime, authorization/tenant, encryption, and representation version.

Never reuse by table name alone. A refreshed dimension, policy change, or schema-compatible-but-semantically-different transform needs a new generation. Pin one generation per query for snapshot consistency.

Charge cached tables against memory admission. Eviction must coordinate readers; reference counting or leases prevent use-after-free. Sensitive replicas follow expiry and deletion across heap, off-heap, disk, and crash dumps.

### Failure and retry

Chunk checksum failure triggers bounded refetch from a verified source. Worker loss rebuilds its replica on replacement. Distribution-service failure may retry or cause strategy fallback before probe commit. Auth failures do not retry indefinitely.

Attempts identify plan/build generation. A probe retry uses the same compatible snapshot, or the entire dependent plan advances to a new generation. Do not let some partitions join against old dimension data and others against new data in one committed output.

Cancellation stops downloads/builds and fences late callbacks. Partial cache entries remain invisible. Cleanup occurs after no tasks, retries, audits, or retained-query artifacts reference the generation.

### Fallback behavior

Fallback targets include repartition hash join, distributed sort-merge join, partitioned nested-loop for non-equijoins, or explicit failure. Repartition is usually the safe large equijoin alternative developed in [LSDS-036](../ROADMAP.md).

Define the decision boundary before effects. Preserve input/build materialization when compatible, but create new plan/stage/attempt identity. Record reason: runtime size, expansion, allocation, timeout, unsupported join type, authorization, or service failure.

Forced broadcast hints should be rejectable when correctness or hard safety would fail. A hint is optimizer input, not permission to crash or leak.

### Observability

Record estimated and actual filtered rows, serialized bytes, expanded/hash bytes, largest row/key, distinct/duplicate counts, expansion factor, projection, snapshot, plan decision/reason/confidence, threshold, and fallback.

For distribution track chunks, topology, source/peer/storage bytes, compression, retries, duration, slow workers, checksums, cache hits/misses, generations, and evictions. For local build track allocation, load factor, collisions/probes, build time, table scope, and concurrent builds.

For probe track rows, matches, unmatched, output multiplicity, hot keys under safe representation, CPU, blocked/output time, and attempt outcomes. Relate all to worker/container memory and other workloads.

### Validation and fault injection

Differentially compare with a trusted join implementation. Test empty sides, one row, unique and duplicate keys, all duplicates, many-to-many output, null and null-safe predicates, NaNs, type coercion, Unicode/collation, residual predicates, and each join type/orientation.

Vary serialized-to-expanded ratio, giant rows, stale/wrong statistics, exact thresholds, multiple simultaneous broadcasts, cache generations, and worker counts. Assert memory admission at per-worker and aggregate scopes.

Inject missing/corrupt chunks, slow distribution, object-store throttling, decompression failure, allocation failure, worker/coordinator death, auth expiry, cancellation, stale cache, probe retry, fallback, and speculative output. No partial or mixed-generation output may commit.

### Security, privacy, and governance

Broadcast expands the audience and number of copies. Confirm every target worker, region, tenant boundary, operator, and cache is authorized for the build fields. Project/minimize before distribution. Use scoped credentials, transport/storage encryption, memory isolation where required, and audit downloads/cache access.

Do not expose raw keys or rows in plan strings, metric labels, traces, error messages, or cache filenames. Hashes may remain identifying. Protect manifests/digests and chunk metadata according to classification.

Retention ends when query/retry/cache policy releases the generation. Verify eviction/deletion from heap, off-heap, local spill, object caches, peer caches, replicas, and keys. Legal/incident holds are explicit and reviewed, not accidental cache persistence.

## Definitions and Notation

Let $S$ be the candidate build input and $L$ the probe input after logically valid filter/projection. Let $B_s$ be serialized build bytes, $e$ observed/estimated expansion, $H$ hash/index/workspace bytes, and $B_m=eB_s+H$ per-replica memory.

Let $W$ be actual replica scopes and $C$ concurrent build generations per scope. A simplified total resident estimate is $M=WC B_m$; per-scope admission needs at least $CB_m$ plus probe/operator/runtime reserve.

Starting from one source copy, creating $W$ replicas requires at least $(W-1)B_s$ additional uncompressed payload transmission across some links. A tree changes source load and depth, not the information replicated; compression, locality, preexisting caches, multicast, erasure/replication, and retries change physical accounting.

For key $k$, let $m_k$ and $n_k$ be qualifying build and probe multiplicities. Inner equijoin output contribution is $m_kn_k$. Semi output is $n_k$ when $m_k>0$ and each probe row is emitted once; anti output is $n_k$ when $m_k=0$.

## Mechanisms, Invariants, or Proof Structure

Audit a broadcast join in this order:

1. Pin join type/predicate, preserved side, key normalization/equality/hash/null semantics, residual condition, schema, and snapshot.
2. Choose legal build orientation and reduce it through safe filters/projection without changing multiplicity.
3. estimate and then measure serialized, expanded, hash/workspace, largest-row, duplicate, per-replica, concurrent, and aggregate sizes.
4. Compare broadcast distribution/build/probe/reuse cost with existing partitioning and repartition/sort alternatives under uncertainty.
5. Materialize, chunk, validate, authorize, and atomically complete one immutable build generation.
6. Distribute through a bounded topology and build immutable duplicate-preserving tables under worker admission.
7. Probe with correct inner/outer/semi/anti, null, residual-predicate, multiplicity, backpressure, and attempt semantics.
8. Define runtime abort/fallback before effects and preserve one plan/build generation in committed output.
9. Reconcile estimates, chunks, replicas, memory, rows, matches, attempts, and output against authoritative evidence.
10. Fault-inject distribution/build/cache/retry/fallback and review every replicated copy’s access, retention, and deletion.

For inner equijoin, correctness follows because every build row is inserted under its normalized key, retaining duplicates. Each probe row inspects all build candidates at that key and emits exactly those satisfying full key and residual predicates. Processing every probe row once therefore emits the relational multiset join. Outer/semi/anti rules add or suppress output according to match existence.

The network lower bound is a copy-count argument: with one initial complete build and $W$ target replicas, $W-1$ new complete copies must receive the information. A tree can reduce bottleneck fan-out and distribute concurrently; it cannot make the aggregate payload disappear. Preexisting compatible cached replicas change the initial condition.

Memory safety remains conditional on accurate/guarded expansion, replica scope, concurrency admission, bounded output, and hidden allocator/native use. Runtime measurement and hard limits are required even after a successful cost estimate.

## Alternatives and Trade-Offs

**Broadcast versus repartition.** Broadcast moves one small side to every scope and leaves the large side local. Repartition distributes both sides and supports much larger builds using aggregate memory.

**Compile-time versus runtime decision.** Compile-time planning avoids a decision barrier but trusts estimates. Runtime adaptation measures actual build output and needs safe materialization/fallback.

**Automatic choice versus hint.** Optimizers combine statistics and cost. Hints add domain knowledge but can become stale and never override correctness, authorization, or hard limits.

**Direct versus tree/object-store distribution.** Direct is simple and stresses the source. Trees reduce source fan-out; shared storage decouples the source but can create synchronized fetch load.

**Per-task versus shared replica.** Per-task tables simplify isolation and multiply memory/build CPU. Per-executor/node sharing amortizes cost and needs concurrency-safe immutability, authorization, and eviction.

**Row versus columnar build.** Row hash tables support fast tuple lookup with object overhead. Columnar storage can reduce expansion/cache misses but needs an index and materialization strategy.

**Cache versus query-scoped build.** Cache amortizes repeated use and risks stale generations, memory pressure, and sensitive-data persistence. Query scope is simpler and repeats work.

**Fail versus fallback.** Failure preserves predictability when fallback would violate deadlines or semantics. Fallback improves robustness when an uncommitted compatible alternative exists.

## Failure Modes and Misconceptions

**“Small on disk means small in memory.”** Compression, decoding, objects, keys, hash buckets, duplicates, and allocators expand data.

**“The threshold proves safety.”** It is based on estimates and one configured measure; runtime hard limits still apply.

**“There is only one build copy per worker.”** Scope may be node, process, slot, task, or operator; inspect the runtime.

**“Broadcast join has no network.”** It avoids large-side repartition but distributes the build to all replica scopes.

**“A hash map stores one row per key.”** Relational duplicates require lists/ranges and $mn$ output multiplicity.

**“Either side can always be broadcast.”** Preserved-side semantics restrict outer, semi, anti, and full joins.

**“Null is just another hash key.”** Predicate semantics determine whether nulls match; ordinary SQL equality does not.

**“A hint must be obeyed.”** Safety, support, authorization, and correctness gates can reject it.

**“Broadcast removes skew.”** It removes a repartition step but hot duplicate keys and probe partitions can still dominate.

**“A cache keyed by table name is reusable.”** Snapshot, filters, projection, schema, semantics, code, and authorization must match.

**“A distribution tree reduces total copied bytes below one replica each.”** It reduces source fan-out, while every new complete replica still receives the payload.

**“Fallback can happen at any time.”** Once irreversible or committed effects occur, switching plans can duplicate or mix output.

## Worked Examples

### Example 1

A 2 TiB fact table filters locally by date; a 12 MiB projected dimension is broadcast. Only the exact dimension snapshot and required columns travel. Comparing against the unfiltered dimension’s 3 GiB storage size would miss the opportunity.

### Example 2

A 70 MiB compressed build expands to 350 MiB rows plus a 110 MiB hash index. A 100 MiB transfer threshold does not prove it fits a 400 MiB operator budget.

### Example 3

Eight executor processes each run four join tasks. If tables are per executor, there are eight replicas; if per task, up to 32. The plan records and tests actual scope before admission.

### Example 4

Build key `b` has two rows and probe key `b` has three. Inner join produces six pairs. A map that overwrites the first build row produces only three and is incorrect.

### Example 5

For left outer join, broadcast the right side and probe the left: each worker can emit left matches or one null-extended row. Broadcasting the left does not locally prove which left build rows are unmatched across all right partitions.

### Example 6

A cost planner estimates 40 MiB, while runtime materialization measures 480 MiB. Before probe output, adaptive planning selects repartition join, advances plan generation, and records `runtime_build_limit` rather than crashing workers.

### Example 7

A tree broadcast sends from coordinator to four peers, which fan out. Source sends fewer copies concurrently, but the cluster still creates one complete replica at every required worker and accounts all transmitted bytes/retries.

### Example 8

A cached dimension refreshes between probe stages. The query pins the old compatible digest for snapshot consistency; a later query uses the new generation. Table-name reuse would silently mix time.

### Example 9

A restricted employee dimension is small enough technically but workers span unauthorized regions. The optimizer rejects broadcast on policy grounds and selects an authorized co-located/repartitioned plan.

### Example 10

This fixture demonstrates duplicate-preserving join output and the compact memory/network arithmetic. It is not a distributed transport, allocator, SQL optimizer, or failure simulation.

<!-- bijux-verify: {"id":"broadcast-join-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"inner_rows=5 left_outer_rows=6 unmatched_probe=1\nper_worker_mib=160.0 aggregate_mib=3840.0\nminimum_new_copy_mib=1840\n","stderr":""}} -->
```python
build = {"a": ("gold",), "b": ("silver", "bronze")}
probe = ((1, "a"), (2, "b"), (3, "x"), (4, "b"))
inner = [(row_id, key, value) for row_id, key in probe for value in build.get(key, ())]
left_outer = [
    (row_id, key, value)
    for row_id, key in probe
    for value in (build.get(key) or (None,))
]
unmatched = sum(key not in build for _, key in probe)

serialized_mib = 80
expansion = 1.6
hash_workspace_mib = 32
workers = 24
per_worker = serialized_mib * expansion + hash_workspace_mib
aggregate = workers * per_worker
minimum_new_copy = (workers - 1) * serialized_mib

print(
    f"inner_rows={len(inner)} left_outer_rows={len(left_outer)} "
    f"unmatched_probe={unmatched}"
)
print(f"per_worker_mib={per_worker:.1f} aggregate_mib={aggregate:.1f}")
print(f"minimum_new_copy_mib={minimum_new_copy}")
```

## Cross-Program Connections

- **Database systems:** build/probe orientation, outer/semi/anti semantics, duplicate multiplicity, cost models, statistics, and physical properties define the join.
- **Distributed systems:** dissemination trees, immutable generations, retries, caching, failure domains, and attempt commits govern execution.
- **Data structures:** hash tables, collision resolution, duplicate lists, columnar indexes, Bloom filters, and load factors determine local cost.
- **Networking:** source fan-out, tree depth, chunking, compression, synchronized fetch, retries, and topology shape broadcast time.
- **Operating systems:** heap/off-heap/native allocation, sharing, garbage collection, page cache, and process scope determine actual fit.
- **Security:** replication expands access surface; scoped credentials, authorization, encryption, residency, audit, and deletion are core constraints.
- **Statistics:** row width, distinctness, correlations, confidence, and runtime measurement determine whether threshold decisions are credible.
- **Performance engineering:** per-replica versus aggregate cost, concurrency, output explosion, cache reuse, and tail workers guide tuning.
- **Query optimization:** filter/projection pushdown, join reordering, hints, adaptive plans, and fallback determine when broadcast appears.
- **Governance:** replicated dimension data can encode classifications or decisions whose freshness, access, and correction affect people.

## References

1. Apache Spark, [SQL Performance Tuning: Broadcast Join](https://spark.apache.org/docs/latest/sql-performance-tuning.html), accessed 2026-09-03.
2. Apache Spark, [SQL Hints](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-hints.html), accessed 2026-09-03.
3. Apache Spark, [Configuration](https://spark.apache.org/docs/latest/configuration.html), accessed 2026-09-03.
4. Apache Spark, [RDD Programming Guide: Broadcast Variables](https://spark.apache.org/docs/latest/rdd-programming-guide.html), accessed 2026-09-03.
5. Apache Spark, [PySpark DataFrame.hint](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.hint.html), accessed 2026-09-03.
6. Apache Flink, [Join Hints](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/sql/queries/hints/), accessed 2026-09-03.
7. Apache Flink, [JoinOperatorBase.JoinHint API](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/api/common/operators/base/JoinOperatorBase.JoinHint.html), accessed 2026-09-03.
8. Apache Flink, [Table Configuration: Adaptive Broadcast Join](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/config/), accessed 2026-09-03.
9. Apache Flink, [Adaptive Batch: Adaptive Broadcast Join](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/adaptive_batch/), accessed 2026-09-03.
10. Trino, [Cost-Based Optimizations: Join Distribution](https://trino.io/docs/current/optimizer/cost-based-optimizations.html), accessed 2026-09-03.
11. Trino, [General Properties: Join Distribution Type](https://trino.io/docs/current/admin/properties-general.html), accessed 2026-09-03.
12. Dask, [Shuffling Performance: Joins](https://docs.dask.org/en/latest/dataframe-groupby.html), accessed 2026-09-03.

## Exercises

### Exercise 1

A filtered build is 150 MiB serialized, expands 2.2 times, and needs 70 MiB hash/workspace. There are 40 executor replicas and two concurrent build generations. Compute per-replica build memory, per-executor concurrent memory, aggregate resident memory, and the minimum new-copy payload from one source for one generation.

### Exercise 2

For inner, left outer, right outer, full outer, left semi, and left anti equijoins, state the straightforward legal broadcast side(s) for local hash probing and explain the preserved/unmatched-row constraint.

### Exercise 3

A build key has 400 rows and a probe key has 3,000 rows. Compute inner output multiplicity. Design memory/backpressure and validation controls that preserve semantics rather than dropping duplicates.

### Exercise 4

Specify a runtime adaptive broadcast decision and fallback protocol when compile-time statistics are stale. Include materialization, thresholds, plan identity, effects, cache, metrics, and failure cases.

### Exercise 5

Design a security and lifecycle review for broadcasting a 30 MiB regulated lookup to 500 worker processes across several regions and tenants.

## Answers to the Exercises

### Answer 1

Per replica is $150\times2.2+70=400$ MiB. Two concurrent generations require 800 MiB per executor before probe/operator/runtime reserve. Aggregate resident build memory is $40\times2\times400=32{,}000$ MiB, or 31.25 GiB. For one generation and one initial source copy, the simple lower bound for 40 target copies is $39\times150=5{,}850$ MiB transmitted. Two generations double payload if neither is already cached. Compression, topology, retries, and existing replicas change physical accounting, not the need to admit actual copies.

### Answer 2

Inner can normally broadcast either side. Left outer can straightforwardly broadcast right/non-preserved and probe left; right outer can broadcast left. Left semi and left anti broadcast right because output/existence decisions are for left probe rows. Straightforward local full outer cannot simply broadcast one side: unmatched rows from the broadcast build require global knowledge and exactly-once emission across probe workers. Engines may implement extra coordination or different operators, so verify support. Residual predicates and null-safe semantics remain part of match existence.

### Answer 3

The key produces $400\times3{,}000=1{,}200{,}000$ result pairs. Store all 400 build references under the key, stream/batch each probe row’s matches through bounded output buffers, and propagate sink backpressure. Track largest duplicate list, per-key probe frequency, predicted/actual pairs, bytes, spill if the output operator supports it, and deadline/capacity risk. Differential tests verify exact pair identities/multiplicity. If policy imposes an output limit, expose it as query semantics or fail explicitly; silently truncating duplicates is incorrect.

### Answer 4

Materialize the exact post-filter/project candidate under immutable snapshot and plan generation, recording row/byte/schema/digest/key/security metadata. Validate chunks, then measure serialized size, representative/actual expansion, largest row, duplicates, hash workspace, replica scope, concurrent builds, distribution time, and worker reserve. If hard guards pass, distribute/build and publish the chosen plan generation before probing. Otherwise choose repartition/sort alternative under a new generation, reusing compatible materialization. Candidate probe/sink output remains uncommitted until choice. Cache keys include all identity/security fields; partial builds never enter cache. Record estimate error and fallback reason. Inject oversized build, allocation, corruption, timeout, worker/service/auth failure, cancellation, and retry.

### Answer 5

Confirm purpose and minimize columns/rows before broadcast. Map every worker/process, region, tenant boundary, runtime operator, cache, spill/crash-dump path, and administrator that can access a replica; reject unauthorized destinations. Use workload identity, scoped expiring credentials, per-tenant/query generations, encrypted transport/storage, appropriate memory/process isolation, and audited cache/download access. Redact rows/keys from plans and telemetry. Admit aggregate memory/network and rate-limit distribution. Define snapshot freshness/correction, retention, incident/legal holds, and deletion/cryptographic erasure across heap, off-heap, local/peer/object caches, spill, dumps, replicas, and keys. Verify with access-denial, cross-region, cross-tenant, key-rotation, eviction, deletion, worker-loss, and forensic audits involving data owner, platform, security, privacy/legal/records, regional authorities, and affected-service representatives.
