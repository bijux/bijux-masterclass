---
module_id: LSDS-028
program: Large-Scale Data Systems Engineering
level: 1
module_number: 28
title: Intermediate Data Materialization
status: complete
last_verified: 2026-09-03
---

# Intermediate Data Materialization

## One-Page Review

### Governing question

When should a large-scale computation retain an intermediate result, in what storage and representation, and under which identity, integrity, visibility, recovery, reuse, security, and lifecycle contract?

### Essential definitions

- **materialization** turns a computed intermediate into retained data that later work can read instead of immediately pipelining or recomputing it.
- A **pipelined edge** passes records without first completing and retaining the whole intermediate.
- A **blocking exchange** retains partitioned producer output until downstream consumers can fetch it; it need not be durable beyond the run.
- A **cache** keeps reusable partitions in a faster tier and may be incomplete or evicted.
- **persistence** requests retention under an engine storage level; its durability and timing are engine-specific.
- A **checkpoint** establishes a recovery boundary with a defined state/data snapshot and lineage cut.
- A **published intermediate** is a governed dataset with durable identity, manifest, ownership, and consumer contract.
- A **materialization manifest** binds plan/input/schema/partition identities to the authoritative object set, sizes, checksums, and commit state.
- **recomputation amplification** is repeated upstream work caused by multiple consumers, cache loss, or downstream failure.
- **lifetime** spans creation through last authorized consumer and verified reclamation.

### Central model, mechanism, or theorem

Materialization is worthwhile only when avoided recomputation or coordination risk exceeds write, validation, storage, read, serialization, operational, and governance costs. A simple deterministic comparison for `u` uses is `C_recompute=u*C` versus `C_materialize=C+W+V+u*R+S`, where `C` is upstream compute, `W` write, `V` validation/commit, `R` read per use, and `S` retained-storage/lifecycle cost in compatible units. Production decisions use distributions, failure probabilities, concurrency, capacity, and critical-path effects rather than one scalar average.

Correctness requires stronger conditions than favorable cost. The retained result must name exact inputs, code/plan, schema, partitioning, ordering, encoding, and policy context; attempts write isolated candidates; validation covers completeness and integrity; one atomic manifest makes a consistent object set visible. Ephemeral shuffle and cache blocks may use weaker durability only when lineage can reproduce them safely.

### Critical invariants

- The materialized representation is semantically equivalent to the declared upstream result under pinned input and plan identities.
- Consumers never infer completeness from directory listing, file count alone, or producer process success.
- Attempt objects remain invisible until one authoritative manifest or transaction commits them.
- Schema, partitioning, ordering, compression, encryption, and serialization versions are explicit and consumer-compatible.
- Cache eviction or worker loss triggers valid recomputation, fallback, or terminal failure according to the storage contract.
- Shared reuse requires matching data, code, configuration, security/purpose, and freshness identities.
- Reference/lifetime accounting cannot delete data while an authorized consumer, retry, audit, or rollback still requires it.
- Partial writes, stale generations, duplicate attempts, corrupt objects, and mixed-run partitions are rejected.
- Cost evidence includes producer/consumer concurrency, spill/network, small files, recovery, validation, retention, and deletion.
- Sensitive intermediates receive least privilege, encryption, minimization, residency, retention, and auditable destruction.

### Common failures

Frequent failures are treating cache as durable publication, assuming a persistence call eagerly computes all partitions, materializing every edge, recomputing a costly fan-out ancestor for every action, relying on mutable directory listings, mixing attempt outputs, omitting schema or partition metadata, using local shuffle as cross-run recovery, caching under an incomplete key, retaining sensitive decoded data indefinitely, deleting after one consumer while another retries, selecting a compressed format without measuring CPU, producing millions of tiny files, and celebrating saved compute while write/read/storage or critical-path cost grows.

### Compact example

A heavy ancestor costs 120 units and has three uses. Recomputing costs 360; materializing once with write 35, validation 5, and read 15 per use costs 205, a modeled saving of 155. A small ancestor costs 12 with two uses: recomputation costs 24, while materialization costs 27, so retention loses under this model. A three-partition manifest totaling 600 bytes is complete only when all expected partition IDs and checksums exist. The model omits concurrency, failures, capacity, and governance and is not a universal threshold.

### Connections

[LSDS-014](014-read-and-write-pipelines.md) supplies I/O mechanics, [LSDS-017](017-multipart-upload-and-commit.md) supplies commit, and [LSDS-019](019-small-file-pathologies.md) supplies layout risks. [LSDS-024](024-directed-acyclic-graph-execution.md) supplies lineage/fan-out, [LSDS-025](025-lazy-evaluation-and-plan-construction.md) distinguishes persistence hints from actions, and [LSDS-029](../ROADMAP.md) deepens checkpoints.

## Governing Question

Between every pair of operators lies a choice: stream records directly, retain local exchange data, cache partitions, checkpoint state, or publish a durable dataset. These choices affect performance, parallelism, recovery, reproducibility, cost, and data exposure. The word “materialize” is often used for all of them, masking radically different guarantees.

A fused pipeline minimizes intermediate I/O but couples producer and consumer lifetimes and failures. A blocking exchange lets stages run at different times but consumes local disk and may disappear with a worker. A cache accelerates reuse but can be partial or evicted. A checkpoint bounds lineage and recovery. A published intermediate supports independent jobs and audits but needs ownership, compatibility, commit, retention, and deletion.

The governing question is how to choose the weakest mechanism that satisfies correctness, recovery, reuse, and governance while demonstrating that its whole-system cost is acceptable.

## Why This Matters

Large intermediate datasets frequently exceed both input and output. Writing them unnecessarily can double or triple network and storage traffic. Refusing to retain them can be just as expensive when three branches or actions recompute the same joins and normalization.

Materialization changes resource overlap. A blocking boundary lets upstream resources release before downstream tasks start and can reduce simultaneous memory/network needs. Pipelining lowers latency and disk I/O but may create backpressure and co-failure. Durable publication decouples schedules and teams but lengthens data lifetime and attack surface.

Recovery depends on boundaries. Losing an ephemeral producer may force a whole lineage replay. A valid retained exchange partition or checkpoint can preserve progress. But reusing a stale or mixed-run intermediate can silently produce a wrong result that appears faster and healthier.

Intermediates also become accidental products. A “temporary” table acquires downstream consumers, no owner, permissive access, undocumented schema, and indefinite retention. Engineering must either keep it run-scoped and reclaimable or promote it deliberately to a governed dataset.

## Prerequisites and Retrieval

Recall partition identity and locality from [LSDS-003](003-range-hash-and-consistent-partitioning.md) and [LSDS-004](004-data-locality.md), dependency and stage boundaries from [LSDS-005](005-distributed-task-graphs.md) through [LSDS-007](007-narrow-and-wide-transformations.md), serialization from [LSDS-008](008-serialization-across-workers.md), and work/movement/state accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md).

Retrieve distributed storage, replication, read/write, object semantics, multipart commit, metadata consistency, and small-file behavior from [LSDS-011](011-distributed-block-storage.md) through [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md). Retrieve attempt commit from [LSDS-021](021-mapreduce-execution-model.md), DAG lineage from [LSDS-024](024-directed-acyclic-graph-execution.md), lazy persistence semantics from [LSDS-025](025-lazy-evaluation-and-plan-construction.md), and retry/failover from [LSDS-027](027-task-retry-and-speculation.md).

You should understand immutable snapshots, manifests, checksums, partitions, schemas, serialization/compression, caches, retries, probability/expected cost, access control, retention, and atomic visibility.

## Learning Objectives

After this module, you should be able to:

1. distinguish pipelining, blocking shuffle, cache, persistence, checkpoint, and published intermediate contracts;
2. model recomputation, write, validation, storage, read, failure, and lifecycle cost;
3. choose materialization boundaries from fan-out, lineage, failure, resource overlap, and governance evidence;
4. specify immutable identity and manifest metadata for reusable intermediates;
5. design attempt-isolated creation, validation, atomic visibility, and corruption handling;
6. select representation, compression, partitioning, file sizing, and storage tier for consumers;
7. define partial cache, eviction, fallback, freshness, invalidation, and cross-run reuse behavior;
8. prevent premature deletion, reference races, orphan leaks, and accidental permanent datasets;
9. evaluate materialization using end-to-end latency, movement, resource, recovery, cost, and correctness metrics; and
10. govern sensitive intermediate data through minimization, isolation, residency, retention, deletion, and named review.

## Core Exposition

### A spectrum of retained state

**Pipelined records** may live only in buffers. They minimize stored bytes and can begin consumption early, but producer and consumer overlap and may co-fail.

**Spill files** extend task memory. They are internal attempt state, not a reusable dataset. Their format and lifetime can change with engine version.

**Blocking shuffle output** is partitioned intermediate data retained long enough for downstream fetch. It separates stages and can preserve progress if the runtime records and retains it, but local worker loss may remove it.

**Cached/persisted partitions** accelerate later uses. Some partitions may be absent, evicted, or recomputed. A storage level can choose memory, serialized memory, disk, or replication; it still does not automatically create a governed cross-run product.

**Checkpoint data** is a recovery snapshot with a lineage or state boundary. Its completeness, coordination, compatibility, and retention are tied to recovery semantics.

**Published intermediate datasets** expose a durable contract to independent consumers. They need stable ownership, catalog identity, compatibility, service expectations, and lifecycle governance.

### Boundary selection

Candidate boundaries often occur after expensive deterministic normalization, joins, wide aggregations, model features, or before multiple sinks. Materialize when it reduces repeated work, breaks a long recovery chain, decouples resource-heavy stages, supports audit/inspection, or provides a deliberate sharing boundary.

Do not materialize merely because an operator is expensive. If there is one consumer, failures are rare, the data is huge, and producer/consumer pipeline efficiently, write plus read can dominate. A boundary can also lengthen the critical path even while reducing total work.

### Cost and uncertainty

The compact formula compares compatible cost units. Expand it with probability that each consumer runs, probability and scope of failure, number of retries, concurrent versus serial reads, compression CPU, storage tier, retention duration, cache hit/loss, egress, validation, control-plane operations, and deletion.

Use distributions. A median 10-minute recomputation does not represent p99 skew or a recovery during degraded storage. Model critical-path time separately from total CPU/bytes/money. Sensitivity analysis should show where the choice flips.

### Identity and reproducibility

A reusable intermediate identity includes producer logical and physical plan digests, code and dependencies, input and side-input snapshots, schema, key/partition/order semantics, configuration, locale/timezone/numeric policy, nondeterminism/seed, engine/format versions, tenant/purpose/security context, and creation policy.

Human names such as `clean_customers_latest` are aliases, not immutable identities. Resolve aliases to a version and record the mapping. Never key a shared cache only by SQL text or output path.

### Representation and layout

Choose row or column encoding based on access. Columnar formats favor projection and compression for analytical scans; row-oriented forms may favor whole-record streaming. Serialized in-memory objects trade CPU for memory differently from encoded byte blocks.

Partitioning should match likely consumers while avoiding one layout for every possible query. Record partition function/count/boundaries and sort order. File sizes balance parallelism and locality against metadata, open, listing, and scheduling overhead. Compact small files before promoting an intermediate to durable shared status.

Compression reduces bytes and can increase CPU/latency. Measure codec, level, data distribution, read selectivity, worker hardware, encryption, and downstream support. Format and codec are compatibility contracts, not tuning details.

### Attempt isolation and commit

Each producer attempt writes under a unique generation and never directly mutates the final visible manifest. It reports expected partition, object identity, length, record count, checksum, schema/format, input/plan identity, and validation evidence.

The coordinator selects one valid candidate per logical partition and atomically commits a manifest containing the complete expected partition set. Object stores may not provide atomic directory rename; manifest publication supplies the visibility boundary. Consumers read the committed manifest, not an open-ended prefix listing.

### Completeness and integrity

Completeness means every required logical partition is represented exactly as the contract specifies; an empty partition may need an explicit entry. Integrity means content matches recorded length/checksum and, where required, structural/schema validation. Semantic validation can check counts, key ranges, uniqueness, distributions, and reference results.

Checksum success does not prove semantic correctness, and row-count equality does not prove byte integrity. Layer the evidence. On corruption, quarantine the candidate, trace its attempt/storage domain, and recompute from valid pinned inputs or fail explicitly.

### Cache semantics

A persistence call may only mark a lazy handle. The first action computes and retains partitions. Later actions can mix cache hits with recomputation for missing partitions. Eviction policies and executor loss make residency dynamic.

Track materialized partition fraction, bytes, hit/miss, eviction reason, recomputation, replication, serialization, and unpersist completion. If a cache is correctness-critical, it is the wrong mechanism unless the engine contract elevates it to durable state.

### Shuffle materialization

Blocking shuffle persists producer data before downstream consumption, reducing simultaneous stage resources and giving the scheduler a boundary. Hash shuffle can create many producer-by-consumer files; sort-based organization can consolidate writes. Hybrid/pipelined designs trade earlier consumption against retention and failure coupling.

Shuffle artifacts normally belong to one run and physical plan. Reusing them across runs requires explicit identity and compatibility; internal file names are not a public dataset interface. Protect shuffle data in transit and at rest because it often contains decoded or repartitioned sensitive records.

### Fan-out and repeated actions

When one ancestor feeds multiple branches, joint submission may share it without durable retention. Separate actions may recompute unless cached or materialized. Consumers with very different schedules or failure domains often benefit from a committed boundary.

Count actual uses, not graph outdegree alone. A branch can be pruned; an action can retry; a speculative attempt can reread; a late consumer can arrive after eviction. Estimate consumer probability and concurrency.

### Failure and recovery

Materialization narrows recomputation only if it remains available and its metadata survives coordinator failure. Local shuffle on a lost node does not help. Replication or remote storage improves survival but costs bytes and commit complexity.

Recovery must reject partial/mixed generations. Persist manifests and producer progress in a recoverable state store, reconcile surviving objects, and fence stale producers. A checkpoint in LSDS-029 adds consistent recovery-state semantics beyond generic retained data.

### Lifetime and garbage collection

Define owner, creation time, last-access evidence, minimum/maximum retention, active consumers, retry/rollback/audit holds, legal holds, deletion method, and verification. Reference counts need transactional acquisition/release or leases; a crash between reading and incrementing can cause premature deletion.

Use mark-and-sweep reconciliation from authoritative manifests and active runs to find orphans. Quarantine before irreversible deletion when uncertainty exists. Deletion must cover replicas, caches, indexes, manifests, keys, and backups according to policy.

### Accidental data products

Repeated cross-run use signals that an “intermediate” may be a product. Promotion requires stable name, owner, schema/version policy, documentation, quality objectives, lineage, access/purpose policy, retention/deletion, cost allocation, and incident support.

Conversely, do not publish internals merely for debugging convenience. Intermediate schemas expose implementation details and can freeze optimizer choices. Keep run-scoped artifacts private unless an enduring consumer contract justifies promotion.

### Observability and evaluation

Record decision inputs and alternative estimate; producer compute; write/read/validation bytes and time; serialization/compression CPU; partition/file distribution; cache residency/hit/eviction; storage tier/duration/cost; fan-out; retries/recovery; object operations; critical path; and cleanup.

Validate values against an unmaterialized reference on empty, singleton, duplicate, null, skewed, corrupt, partial, mixed-generation, retry, and schema-evolution cases. Benchmark cold/warm cache, concurrent consumers, storage degradation, node loss, and coordinator restart.

### Security, governance, and human impact

Intermediates may be less protected than sources while containing more sensitive joined, decoded, or scored data. Apply minimization before retention, separate tenants/purposes, encrypt data and manifests, scope worker/consumer identities, redact diagnostics, enforce residency, rotate/revoke keys, and audit access.

Retention must match consent, purpose, records, correction, appeal, and deletion obligations. If an intermediate affects human decisions, preserve versioned lineage and subgroup quality evidence long enough for legitimate review without retaining raw sensitive data indefinitely. Named reviewers decide that balance.

## Definitions and Notation

- `C`: one upstream computation cost in a declared unit.
- `u`: number of expected materialized or recomputed uses under a stated horizon.
- `W`, `R`, `V`, `S`: write, per-use read, validation/commit, and retained-storage/lifecycle costs.
- `C_recompute=u*C`: simple repeated-computation model.
- `C_materialize=C+W+V+u*R+S`: simple materialization model.
- **candidate boundary**: graph edge considered for retaining the complete logical intermediate.
- **storage level**: memory/disk/serialized/replicated behavior declared by an engine.
- **manifest generation**: unique publication attempt fenced from older/newer runs.
- **expected partition set**: complete logical partition IDs, including explicit empty partitions if required.
- **cache residency**: current retained subset, distinct from logical dataset completeness.
- **reference hold**: active consumer/retry/audit/legal reason preventing reclamation.
- **promotion**: deliberate conversion from run-internal artifact to governed shared dataset.

## Mechanisms, Invariants, or Proof Structure

Audit a materialization boundary in this order:

1. Name producer result, exact consumers, use probability/concurrency, recovery need, and candidate lifetime.
2. Compare pipelining/recomputation against write, validation, storage, read, recovery, and governance costs with uncertainty.
3. Pin producer plan/code/configuration, inputs/side inputs, schema, partition/order, nondeterminism, engine, and policy identity.
4. Select storage tier, representation, codec, encryption, partitioning, file sizing, replication, and locality contract.
5. Isolate attempt writes and define expected partition metadata, completeness, checksums, structural and semantic validation.
6. Commit one authoritative immutable manifest and require consumers to resolve only through it.
7. Define cache partiality/eviction, shuffle loss, fallback/recomputation, coordinator recovery, fencing, and corruption response.
8. Define owner, access/purpose/residency, references/leases, retention, audit/rollback holds, garbage collection, and verified deletion.
9. Test cold/warm, multiple consumers, failures, mixed attempts, schema/plan drift, small files, overload, and unauthorized reuse.
10. Promote to a governed product only when durable independent consumers justify the contract.

The correctness proof has two layers. First, the producer computation under pinned identities is semantically correct. Second, the publication protocol exposes exactly one complete validated generation whose manifest binds every authoritative partition. Cache and ephemeral shuffle may weaken availability, but not silently change values.

The economic argument remains conditional: compare end-to-end distributions and critical-path effects under representative use/failure patterns. A positive scalar saving in one fixture is evidence for that fixture only.

<!-- bijux-verify: {"id":"materialization-cost-and-manifest","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"heavy_recompute=360 heavy_materialize=205 saving=155 choose=True\nsmall_recompute=24 small_materialize=27 saving=-3 choose=False\nmanifest_complete=True partitions=3 bytes=600\n","stderr":""}} -->
```python
def compare(compute, uses, write, read, validate, storage):
    recompute = compute * uses
    materialize = compute + write + validate + read * uses + storage
    return recompute, materialize, recompute - materialize


heavy = compare(compute=120, uses=3, write=35, read=15, validate=5, storage=0)
small = compare(compute=12, uses=2, write=5, read=4, validate=2, storage=0)
expected = {0, 1, 2}
manifest = {
    0: {"bytes": 100, "checksum": "a1"},
    1: {"bytes": 200, "checksum": "b2"},
    2: {"bytes": 300, "checksum": "c3"},
}
complete = set(manifest) == expected and all(entry["checksum"] for entry in manifest.values())

print(
    f"heavy_recompute={heavy[0]} heavy_materialize={heavy[1]} "
    f"saving={heavy[2]} choose={heavy[2] > 0}"
)
print(
    f"small_recompute={small[0]} small_materialize={small[1]} "
    f"saving={small[2]} choose={small[2] > 0}"
)
print(
    f"manifest_complete={complete} partitions={len(manifest)} "
    f"bytes={sum(entry['bytes'] for entry in manifest.values())}"
)
```

The manifest fixture checks IDs and nonempty checksum fields, not checksum contents or semantic validity. A production validator recomputes cryptographic checksums and verifies identities, schema, format, counts, ranges, and commit generation.

## Alternatives and Trade-Offs

**Pipeline versus block.** Pipelining lowers latency and storage but couples resources/failures. Blocking releases producers and supports later fetch at I/O and latency cost.

**Recompute versus cache.** Recompute avoids retained state and staleness. Cache helps repeated deterministic work but consumes capacity and can disappear.

**Memory versus serialized memory versus disk.** Objects are fast but large; serialized bytes save memory at CPU cost; disk expands capacity with higher latency. Measure actual workload.

**Local versus replicated/remote retention.** Locality is fast and cheap but shares worker failure. Replication or remote storage improves availability while adding network, storage, and consistency work.

**Ephemeral shuffle versus durable intermediate.** Shuffle fits one run and internal physical plan. Durable data decouples runs/teams but requires public compatibility, ownership, and governance.

**Materialize before versus after exchange.** Before exchange may preserve reusable local work; after exchange may preserve expensive repartition/join results. Size, recovery scope, and consumers differ.

**Row versus column representation.** Row formats support whole-record flows; columnar formats support projections/analytics. Neither wins independent of access and encoding cost.

**Automatic caching versus explicit boundary.** Automatic caching adapts to observed reuse but complicates predictability and policy. Explicit materialization is reviewable but can become stale boilerplate.

## Failure Modes and Misconceptions

**"Materialized means durable."** Local spill, shuffle, memory cache, checkpoint, and published data provide different guarantees.

**"Calling persist writes everything now."** In lazy systems it may mark a plan; action and partition execution determine what is retained.

**"Cache hit means correct reuse."** The cache key must include every relevant semantic and policy identity.

**"Directory contents are a manifest."** Listings can include partial, stale, duplicate, or losing-attempt objects and lack an atomic generation.

**"Checksums prove the dataset is correct."** They detect certain integrity failures, not wrong input, plan, schema, or semantics.

**"Every wide edge should be durable."** Blocking shuffle may be enough; durable publication adds cost and contract surface.

**"Recomputation is free fault tolerance."** Long lineages, nondeterminism, mutable inputs, and repeated failure can make it expensive or invalid.

**"More compression always saves money."** Codec CPU, latency, hardware, selectivity, and compatibility can outweigh bytes.

**"Reference count zero means delete."** Crashed/acquiring consumers, retries, rollback, audits, and legal holds require transactional or reconciled lifetime logic.

**"Temporary data needs weak security."** Joined or decoded intermediates can be more sensitive than sources.

**"A faster warm-cache benchmark proves improvement."** Cold start, eviction, write/materialization, concurrent use, failure, and cleanup belong in the comparison.

**"Popular intermediates can remain informal."** Independent consumers create a product contract and ownership obligation.

## Worked Examples

### Example 1

A filter and projection feed one immediate aggregate. Pipelining avoids a large write and has bounded memory. Materializing adds no reuse or recovery value. Keep it fused and measure backpressure rather than inserting a file boundary reflexively.

### Example 2

An expensive deterministic join feeds three independently scheduled sinks. The retained join reduces repeated input scans and exchange, and decouples sink retries. Commit one partition manifest and charge write/read/storage/security cost before concluding it wins.

### Example 3

An RDD is marked memory-only. The first action retains computed partitions; two do not fit and are absent. A later action reads hits and recomputes misses. Logical completeness remains true through lineage, while cache residency is partial.

### Example 4

A blocking shuffle writes producer partitions to local worker disks. Downstream can run after producers release slots. Losing one worker deletes several shuffle partitions and invalidates dependent progress unless remote/replicated recovery exists. The shuffle is materialized but not a durable cross-run dataset.

### Example 5

Two attempts write partition 17 under unique paths. One passes checksum/schema/range checks and wins the manifest entry. The late loser cannot mutate the generation. Consumers never list the prefix to choose the newest object.

### Example 6

A columnar intermediate halves read bytes for projection-heavy consumers but costs more CPU to encode once. With ten reads it wins; with one whole-row consumer it may not. Benchmark codec/level, selectivity, CPU architecture, encryption, and cold storage.

### Example 7

Ten thousand tasks each emit a 20-KiB file. Data volume is only 200 MiB, but metadata/open/scheduling costs dominate. Coalesce or compact under a manifest while preserving partition/key semantics and parallelism requirements.

### Example 8

An intermediate is retained for an audit for 30 days and used by a retry on day two. A naive job-end cleanup deletes it early; an unbounded “temporary” policy keeps it forever. Explicit retry/audit holds, maximum retention, legal policy, and verified deletion resolve the lifecycle.

### Example 9

Two tenants submit textually identical plans over row-filtered tables. Shared cache reuse keyed only by plan text exposes data. Include tenant, purpose, row-policy, snapshot, and encryption domain in identity or isolate caches entirely.

### Example 10

A clinical feature intermediate becomes a dependency for reporting and model review. Promotion requires an owner, stable schema, data-quality and timeliness objectives, affected-population validation, access/purpose controls, correction lineage, retention/deletion, accessibility, and incident support—not merely a permanent bucket path.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies materialized views, buffer/cache management, transactions, schemas, indexes, and query reuse.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies datasets, lineage, orchestration, data products, quality, retention, and publication.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies replication, failure boundaries, fencing, atomic visibility, and garbage collection.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies memory caches, virtual memory, filesystems, page cache, spill, and reclamation.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies representations, indexing, locality, compression structures, and cache policies.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies shuffle flow, congestion, egress, topology, and backpressure.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies storage classes, quotas, observability, workload identities, catalogs, and lifecycle automation.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies encryption, integrity, least privilege, isolation, key lifecycle, and deletion.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies cost models, caching algorithms, probabilistic failure analysis, and sensitivity testing.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies lifecycle thinking, coupled trade-offs, recovery economics, and emergent risk.

## References

1. Apache Spark. [RDD Programming Guide: RDD Persistence](https://spark.apache.org/docs/latest/rdd-programming-guide.html#rdd-persistence). Accessed 2026-09-03.
2. Apache Spark. [Tuning: Memory and Serialization](https://spark.apache.org/docs/latest/tuning.html). Accessed 2026-09-03.
3. Apache Spark. [Configuration: Compression and Checkpoint Storage](https://spark.apache.org/docs/latest/configuration.html). Accessed 2026-09-03.
4. Dask. [Persist](https://docs.dask.org/en/stable/generated/dask.bag.Bag.persist.html). Accessed 2026-09-03.
5. Dask. [Opportunistic Caching](https://docs.dask.org/en/stable/caching.html). Accessed 2026-09-03.
6. Dask Distributed. [Worker Memory Management](https://distributed.dask.org/en/stable/worker-memory.html). Accessed 2026-09-03.
7. Apache Flink. [Batch Shuffle](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/batch/batch_shuffle/). Accessed 2026-09-03.
8. Apache Flink. [Batch Job Progress Recovery](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/batch/recovery_from_job_master_failure/). Accessed 2026-09-03.
9. Apache Beam. [Execution Model: Bundling and Persistence](https://beam.apache.org/documentation/runtime/model/). Accessed 2026-09-03.
10. Apache Hadoop. [MapReduce Tutorial](https://hadoop.apache.org/docs/stable3/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html). Accessed 2026-09-03.
11. Apache Hadoop. [OutputCommitter API](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/OutputCommitter.html). Accessed 2026-09-03.
12. Michael Isard et al. [Dryad: Distributed Data-Parallel Programs from Sequential Building Blocks](https://www.microsoft.com/en-us/research/publication/dryad-distributed-data-parallel-programs-from-sequential-building-blocks/). EuroSys 2007. Accessed 2026-09-03.

## Exercises

### Exercise 1

Recompute the compact cost comparison and manifest totals. State every omitted factor that could reverse either decision.

### Exercise 2

Classify a fused buffer, task spill, blocking shuffle, memory cache, disk persistence, checkpoint, and published table by visibility, durability, completeness, reuse, and recovery.

### Exercise 3

Design an attempt-isolated materialization manifest and commit/recovery protocol for 10,000 partitions on object storage.

### Exercise 4

Choose boundaries, formats, partitions, storage tiers, and lifetimes for an expensive join feeding interactive, nightly, audit, and machine-learning consumers.

### Exercise 5

Specify named review and evidence for a sensitive intermediate that may become a durable data product.

## Answers to the Exercises

### Answer 1

Heavy recomputation is `120*3=360`; materialization is `120+35+5+15*3+0=205`, modeled saving 155. Small recomputation is `12*2=24`; materialization is `12+5+2+4*2=27`, saving -3. The manifest IDs exactly equal `{0,1,2}`, all checksum strings are nonempty, and bytes sum `100+200+300=600`. Decisions can reverse with consumer probability/concurrency, critical path, failures/retries, cache eviction, compression CPU, bandwidth/contention, egress, object operations, storage duration/tier, validation, small files, replication, cleanup, security, carbon/cost pricing, and uncertainty. Nonempty checksum fields do not prove integrity.

### Answer 2

Fused buffers are attempt-local, partial, transient, and co-failing. Spill is attempt-local disk state and not consumer-facing. Blocking shuffle is run-scoped partition data, often complete per producer before consumption but tied to worker/runtime durability. Memory cache is reusable within engine/session identity, may be partial/evicted, and relies on lineage. Disk persistence expands residency but may remain worker/run scoped. A checkpoint is a coordinated recovery boundary with defined completeness/compatibility. A published table is durable, manifest/catalog visible, independently reusable, owned, versioned, quality-governed, retained, and deleted under policy. Exact guarantees must come from the concrete engine/storage contract.

### Answer 3

Pin run/plan/input/schema/format/partition/policy generation and expected IDs 0–9999. Each attempt writes a unique immutable object and candidate record with task/attempt/generation, length/count, cryptographic checksum, key range/statistics, and validation. A recoverable coordinator chooses at most one valid candidate per partition using conditional state updates. After all expected IDs—including empty partitions—are present, it writes and atomically publishes one immutable manifest/digest; consumers resolve only that manifest. On restart, reconcile durable decisions and objects, fence stale generations, recompute missing/corrupt candidates, reject mixed identities, and idempotently quarantine/collect unreferenced losers after diagnostic holds.

### Answer 4

Materialize the expensive deterministic join once only if measured joint/repeated use and recovery savings exceed its large write/read/lifecycle cost. Use columnar encoded partitions for projection-heavy interactive/nightly/ML reads, with canonical join key and possibly consumer-specific derived layouts rather than one overpartitioned compromise. Publish an immutable validated manifest to durable replicated storage because consumers are independent and audit requires retention; optionally cache hot partitions for interactive use. Record freshness and schema compatibility. Give nightly/ML shorter references, audit a justified hold, and interactive cache eviction; compact file sizes, enforce tenant/purpose access, and reassess whether the shared artifact is now a governed product.

### Answer 5

Pin producer/consumer purpose, plans/code, snapshots, schema/partition/format, quality and subgroup metrics, access/residency/encryption/key policy, freshness, ownership, catalog/version compatibility, incident objectives, correction/appeal lineage, retention/legal holds, and verified deletion. Test completeness/integrity, mixed attempts, corruption, schema drift, unauthorized reuse, small groups, cache loss, and replay; compare retained data minimization against audit needs. Named review includes data-product/domain owners, stewards, affected communities or ethics oversight, privacy/legal/records/jurisdiction authorities, fairness/statistics, security/identity/key management, platform/storage/runtime/network operators, accessibility, incident/recovery, cost/sustainability, and independent assurance. Popularity alone cannot authorize promotion or indefinite retention.
