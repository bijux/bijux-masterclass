---
module_id: LSDS-034
program: Large-Scale Data Systems Engineering
level: 1
module_number: 34
title: Hash-Based Shuffle
status: complete
last_verified: 2026-09-03
---

# Hash-Based Shuffle

## One-Page Review

### Governing question

When should a shuffle producer route records directly into hash-selected destination buckets, and how can it bound bucket buffers, files, spills, metadata, skew, retries, and cleanup without relying on sort order or confusing hash partitioning with a particular physical writer?

### Essential definitions

- A **hash partitioner** maps a normalized key to destination $p(k)=norm(h(k),R)$ for $R$ partitions.
- A **hash-based shuffle writer** routes each emitted record directly to destination-specific state without first sorting all records by destination or key.
- A **bucket** is the logical state for one destination within one producer attempt.
- A **partition writer** serializes and appends bucket records to a file, page chain, chunk, or shared indexed container.
- A **sparse bucket table** allocates state only for destinations actually observed by a producer.
- A **bucket spill** flushes one or more destination buffers when memory or pressure thresholds are reached.
- **hash skew** is imbalance caused by key frequency, hash quality, adversarial keys, or too few destinations.
- A **collision** is two distinct keys sharing a hash value or table slot; collision handling inside an aggregation table differs from multiple keys legitimately mapping to one shuffle destination.
- A **hash flood** is adversarial concentration that makes hash-table work or one destination pathologically expensive.
- A **writer bypass** selects direct partition writers because no sort/merge ordering or map-side aggregation requires a sort path.

### Central model, mechanism, or theorem

For $N$ records independently and uniformly assigned to $R$ destinations, expected occupied destinations are $R(1-(1-1/R)^N)$ and expected empty destinations are $R(1-1/R)^N$. A dense design reserving buffer $b$ for every destination consumes roughly $Rb$ memory per active producer task before record/index/codec overhead. With $T$ concurrent producers on a worker, this becomes $TRb$. Sparse allocation reduces empty-bucket overhead but adds maps, page metadata, and unpredictable growth.

The correctness model is simpler than the performance model. For producer input $I_i$, each record is appended exactly once to bucket $B_{i,p(k)}$ under the pinned hash/equality/normalization/version contract. Finalization validates every nonempty bucket and proves emptiness for the rest. Only the accepted attempt publishes its bucket map. Consumer $j$ reads exactly one accepted contribution $B_{i,j}$ from every producer $i$; order inside $B_{i,j}$ is unspecified unless another mechanism establishes it.

### Critical invariants

- Partition count, hash algorithm/seed, key normalization, equality, null handling, serializer, and format are pinned by exchange identity.
- Keys equal under grouping semantics always map to the same destination.
- Each producer record is appended once to exactly one destination bucket.
- Bucket state is attempt-scoped; speculative or failed attempts cannot overwrite or publish winners.
- Buffer/file/page allocation is charged and bounded across destinations and concurrent tasks.
- A spill snapshot is immutable while written, and subsequent segments retain the same bucket identity.
- Final metadata distinguishes empty buckets from missing or incomplete buckets.
- Data/index/chunk lengths, checksums, codec/encryption, and destination identity match stored bytes.
- Consumers do not infer key order, global order, or deterministic equal-key order from direct bucket append.
- Cleanup waits until final publication, downstream retry/recovery, and applicable holds no longer reference bucket artifacts.

### Common failures

Frequent failures are calling every hash-partitioned exchange a hash-based physical shuffle, allocating one large buffer and file per destination, assuming sparse keys make worst-case memory sparse, using language-process-randomized hashes across attempts, applying absolute value incorrectly to the minimum signed integer, letting equal normalized keys hash differently, assuming a good hash fixes hot-key skew, mixing hash collisions with destination collisions, opening $R$ writers for every task, publishing absent metadata as an empty block, losing previously flushed bucket segments, combining without safe algebra, treating append order as stable, accepting a speculative loser, and tuning only total bytes while inode, descriptor, random-write, or metadata limits fail first.

### Compact example

Twenty integer keys routed by `key mod 8` occupy all eight destinations, with counts `(3,3,3,3,2,2,2,2)`. A dense design using 64 KiB per destination reserves 512 KiB for one producer even before records, indexes, and codecs. Under an independent uniform model, the expected occupied count is only about 7.45 and expected empty count 0.55; that expectation does not bound a particular producer or adversarial input. With 32 concurrent tasks, dense buffer reservation alone would be 16 MiB.

### Connections

[LSDS-003](003-range-hash-and-consistent-partitioning.md) defines hash routing, [LSDS-023](023-partitioners-and-combiners.md) supplies grouping and combination contracts, [LSDS-031](031-shuffle-architecture.md) defines logical blocks and fetch, [LSDS-032](032-map-side-buffering-and-spill.md) defines bounded spilling, and [LSDS-033](033-sort-based-shuffle.md) provides the principal physical contrast. [LSDS-036](../ROADMAP.md) and [LSDS-038](../ROADMAP.md) reuse hash partitioning and aggregation.

## Governing Question

A producer can avoid sorting if it already knows each record’s destination and the consumer does not require keys in order. Compute a hash partition, append to that destination’s buffer or stream, flush when needed, and publish the destination outputs. For small destination counts and fast storage, this direct path can save comparison and merge work.

The apparent simplicity hides scaling. If every task owns a buffer and file for every destination, resources grow with producer concurrency times destination count. Thousands of reducers can produce millions of files, buffers, streams, and metadata entries. Interleaved writes become random I/O. Sparse allocation helps when producers touch few destinations but not when all-to-all data is dense.

Hash semantics also become part of persisted execution. The same logical key must map identically across tasks, retries, languages, and versions. Hash seeds, normalization, array/object equality, signed arithmetic, nulls, and serialization are not implementation trivia.

The governing question is when direct bucket routing beats sort-based clustering and how to make the hash path correct under bounded resources, skew, spill, attempts, and failure. The answer depends on destination count, record/key distribution, storage, memory, aggregation, ordering requirements, and downstream reuse.

## Why This Matters

Direct routing can reduce CPU when comparison sorting would add no useful property. A record needs a hash, normalization, and append rather than $O(\log n)$ comparisons in an in-memory run. For bounded destination counts, independent sequential writers can be effective.

At large scale, the same design can collapse. A thousand tasks each reserving a thousand buffers is one million buffers. Per-destination files consume inodes and descriptors. Rotating among many streams destroys locality on spinning disks and taxes SSD metadata. Tiny blocks amplify checksums, RPCs, and fetches.

Hash skew controls tails. Uniform hashing spreads distinct random keys in expectation, but it cannot split multiple records for one hot key if grouping requires them together. Low-entropy or adversarial keys can concentrate buckets. One destination’s disk, network, hash table, and reducer work then dominate completion.

Correctness failures often look like skew or missing data. A retry with a different seed reroutes keys. An empty marker published before a late buffer flush omits records. Direct append segments concatenated in callback order change output bytes. A losing attempt’s file can shadow the winner. Strong identity and reconciliation are essential.

## Prerequisites and Retrieval

Retrieve horizontal, range, hash, and consistent partitioning from [LSDS-002](002-horizontal-partitioning.md) and [LSDS-003](003-range-hash-and-consistent-partitioning.md), plus locality, serialization, failures, and scale accounting from [LSDS-004](004-data-locality.md) through [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md). Retrieve block/index/metadata integrity from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md).

Review partitioner/combiner safety in [LSDS-023](023-partitioners-and-combiners.md), attempt/materialization identity in [LSDS-027](027-task-retry-and-speculation.md) and [LSDS-028](028-intermediate-data-materialization.md), and shuffle buffering/sorting in [LSDS-031](031-shuffle-architecture.md) through [LSDS-033](033-sort-based-shuffle.md). You should understand hashing, modular arithmetic, occupancy, load factors, collision resolution, bounded buffers, immutable attempt artifacts, and atomic publication.

## Learning Objectives

After this module, you should be able to:

1. distinguish hash partitioning from hash-organized shuffle writing and hash-table aggregation;
2. specify stable hash, seed, normalization, equality, destination-count, null, and format contracts;
3. derive dense buffer/file scaling and expected occupied/empty destination counts;
4. compare dense, sparse, page-based, consolidated, and per-destination physical layouts;
5. design bounded bucket spill, segment consolidation, indexing, and final publication;
6. reason about hot keys, poor hashes, adversarial inputs, and skew-aware mitigation;
7. preserve exact routing across retry, speculation, cross-language code, and upgrades;
8. select hash, sort, or bypass paths from ordering, aggregation, cardinality, memory, and storage evidence;
9. validate routing, multiplicity, emptiness, bounds, integrity, and cleanup with fault injection; and
10. govern sensitive keys and intermediate buckets through isolation, encryption, retention, deletion, and access review.

## Core Exposition

### Separate three uses of hashing

Hash partitioning chooses a destination. A sort-based writer can still use a hash partitioner, then sort record pointers by destination. Hash-based physical organization means it routes directly to bucket state instead of globally clustering with a sort.

A hash aggregation table is a third concept: it groups equal keys to combine values. A direct writer can append records without such a table, or it can aggregate within each destination. The table needs collision resolution and equality checks; partition routing only needs a destination number.

State these choices independently in plans and telemetry. Otherwise a label such as “hash shuffle” cannot explain whether the system avoided sorting, built aggregation tables, or merely used hashed destinations.

### Stable partition function

Define $p(k)=norm(h(normalize(k),seed),R)$. Pin hash algorithm and version, seed, normalization, key schema, equality, destination count, and signed-to-nonnegative mapping. Language default hashes may depend on process identity, random seeds, mutable object state, or runtime version and can be unsuitable.

Keys equal under grouping must share normalization and destination. Hash equality is weaker: distinct keys can share hashes legitimately. A destination holds many hash values and keys. Reducers still compare full keys if grouping matters.

Avoid `abs(hash) % R` in fixed-width signed arithmetic unless the minimum negative value is handled. Prefer a defined unsigned or floor-mod normalization. Test boundary values in every implementation language.

### Dense destination writers

A dense design creates $R$ bucket states per producer. Each may own a serialization buffer, stream, checksum, codec state, and file. It offers constant-time indexed access and simple finalization. It is attractive when $R$ is small and most destinations are active.

Memory is not only $Rb$: include bucket objects, indexes, codec/encryption workspaces, file-stream buffers, allocator granularity, and frozen spills. Descriptors may be $R$ per task if writers remain open. Across $T$ tasks, multiply before comparing with worker limits.

Closing/reopening writers reduces descriptors but adds seeks and metadata operations. A shared consolidated file can append framed bucket segments and maintain an index, trading per-destination files for segment metadata and final consolidation.

### Sparse bucket allocation

A sparse map creates bucket state on first use. Expected occupied destinations under independent uniform assignment are $R(1-(1-1/R)^N)$. When $N\ll R$, this can be far smaller than $R$. When $N$ is large relative to $R$, nearly all buckets appear.

Expectation is not a safety bound. A producer may touch every destination, and adversarial input can target costly patterns. Capacity planning uses worst permitted active buckets plus measured distributions. Sparse maps themselves have load-factor, resizing, pointer, and hash costs.

Reclaiming an inactive bucket after flush can reduce memory, but later records may recreate it and multiply segments. Hysteresis or page pools can balance churn against reservation.

### Page-based shared buffering

Instead of one fixed buffer per destination, allocate pages from one bounded pool. Each bucket owns a chain of pages or framed segments. This gives active/skewed buckets capacity proportional to their output while bounding total pages.

The pool needs reserve for the next record, indexes, codecs, spill writer, and control progress. A giant record uses a bounded streaming path or fails clearly. Backpressure applies when no page can be safely reclaimed.

Page fragmentation and small tails waste capacity. Track allocated versus used bytes. Shared pages must remain attempt/tenant scoped or be securely erased before reuse.

### Direct append and file layout

The simplest physical design writes one file per producer-destination pair. It avoids a final partition-clustering sort and enables direct fetch. Its worst-case file count is $MR$ across $M$ producers and $R$ consumers.

Consolidation alternatives include one producer file containing bucket segments, a bounded number of striped files, or destination-oriented remote chunks. Index entries map logical buckets to one or several ranges. Multiple segments for one bucket may be concatenated or fetched as a list if the consumer format supports it.

Every frame identifies exchange, attempt, destination, segment sequence, lengths, codec/encryption, and checksum scope. Never recover identity from filename parsing alone.

### Bucket spill

When a buffer/page pool crosses its soft threshold, select buckets to flush. Largest-first frees memory quickly but can repeatedly favor a hot bucket. Round-robin improves fairness but writes tiny segments. Cost-aware selection considers reclaimable bytes, segment size, age, device locality, and outstanding writers.

Freeze selected segments before asynchronous write. New records for the same destination go to a new active segment; the writer owns frozen pages until completion. Bound concurrent spills and segment queues. If production exceeds write service, block or slow input.

A completed spill is immutable attempt-scoped state. Record per-bucket segment sequence and validation. Disk-full, partial write, or cancellation cannot appear as an empty successful bucket.

### Consolidation without semantic sort

Multiple segments for one destination can be concatenated in a deterministic or arbitrary declared order. No key comparisons are required. If one final producer file must contain destinations contiguously, copy bucket segments destination by destination and build offsets.

This final copy is physical grouping, not sort-based key ordering. It may add one full read/write pass. A striped or multi-segment fetch format can avoid the copy at the cost of more consumer requests and metadata.

Choose based on total bytes, destination count, segment count, storage, and downstream protocol. Measure both producer I/O and consumer small-request amplification.

### Hash aggregation inside buckets

When safe combining is valuable, each destination can hold a hash table from key to partial aggregate, or one shared table whose entries retain destination. Expected lookup is constant under a suitable hash/load factor, but collisions require equality and worst-case behavior can degrade.

Memory grows with distinct keys and aggregate size, not record count alone. High cardinality can make aggregation larger than direct serialized append. Spill tables by destination or hash range, or switch strategies, while preserving combine algebra.

Collision handling—chaining, open addressing, probing, overflow structures—must compare full normalized keys. Hash equality alone never establishes key equality.

### Ordering semantics

Direct append preserves only the writer’s local append sequence for one segment, and even that may change under concurrency. Multiple producers, spill callbacks, segment consolidation, retry, and speculation make no distributed stable order.

Reducers needing sorted keys must sort after fetch or use the sort-based shuffle contract from [LSDS-033](033-sort-based-shuffle.md). A hash join/aggregation may not need order. Do not expose incidental order as API behavior.

Reproducible output requires an explicit ordering/tie-break step, not simply a stable hash seed. Deterministic destinations do not imply deterministic byte order.

### Skew and hot keys

Uniform-hash occupancy assumes independent keys, not real frequency. A hot grouping key must go to one destination, so an ideal hash cannot split it without changing the algorithm. Many distinct keys can also cluster due to poor hash quality, correlated low bits, or adversarial construction.

Measure records, logical/physical bytes, distinct keys, largest group, active buckets, segment counts, spills, CPU, and final consumer work by destination. Hash distribution tests on sampled safe digests can reveal poor spread, but protect raw keys.

Mitigations include more partitions for distinct-key imbalance, stronger/seeded hashes against adversarial inputs, hot-key salting plus second-stage aggregation, preaggregation, skew-aware splitting, and alternate join strategies. Salting changes grouping and requires a correct recombination plan.

### Hash quality and security

A fast noncryptographic hash may be sufficient for trusted data and throughput. Adversarial inputs can create collision/flood behavior in hash tables or destination concentration if the mapping is predictable. A secret per-exchange seed can make attacks harder but must be propagated consistently and recoverably.

Cryptographic hashing costs more and does not solve natural hot keys. Choose according to threat model, key volume, compatibility, and performance. Never use unstable language object identity as semantic hash.

Hashing personal data does not anonymize it, especially for small domains. Treat hashes, seeds, and bucket summaries as potentially sensitive.

### Attempts, retry, and publication

Every bucket file, shared container, segment, and index belongs to one run/exchange/producer attempt. Speculative attempts can use identical destination/segment numbers because their namespaces differ. The exchange directory accepts exactly one final producer output.

Finalization waits for all outstanding segment writes, proves each destination complete or empty, validates lengths/checksums/format, and publishes an immutable manifest/index. A late spill callback after cancellation is fenced from publication.

Retry uses the same pinned partition function or creates a new exchange generation. Consumers invalidate stale locations and never combine old and new accepted contributions.

### Resource model

Track per-task fixed bucket memory, active page pool, frozen pages, aggregation entries, codec/writer buffers, descriptors, files, segments, metadata, direct/native memory, and disk bytes. Multiply by admitted task concurrency and account for shuffle serving plus other workloads.

Hash writers often trade comparison CPU for resource multiplicity and random I/O. SSDs reduce seek penalty but not inode, descriptor, write-amplification, or metadata cost. Encryption can disable zero-copy paths or add buffer pressure.

Use hard caps and a fallback/sort writer when $R$, active buckets, segment count, or resource estimates exceed safe limits. The fallback choice is part of physical planning and evidence.

### Observability

Record hash/seed/normalization identity, destination count, records/bytes, active/empty buckets, occupancy, maximum/quantiles, largest group estimate, buffer/page allocation and utilization, aggregation load/collisions/probes, spill count/segments, per-destination files, descriptors, write pattern, consolidation I/O, and publication time.

Report failed and losing-attempt work separately. Correlate hot destinations to safe heavy-hitter evidence, producer attempts, disks, and reducers. Unique key hashes belong in controlled traces or artifacts, not metric labels.

Record selected writer, bypass/fallback reason, and comparison with sort path. “Hash shuffle time” without routing, spilling, consolidation, and downstream fetch components is not actionable.

### Validation and fault injection

Use an independent partition oracle. Test empty input, one record, $R=1$, $N\ll R$, $N\gg R$, all destinations, one hot key, identical hashes with unequal keys, minimum signed hash, nulls, arrays/objects, Unicode normalization, cross-language encodings, and seed/version changes.

Verify each input record appears once in the expected destination for the accepted attempt. Verify explicit empty buckets, segment sequence/coverage, data/index ranges, checksums, and final manifest. Compare dense, sparse, page, spill, and consolidation paths semantically.

Inject writer delay, pool exhaustion, disk-full, short writes, corruption, descriptor exhaustion, cancellation, process/node loss, duplicate callbacks, retry, speculation, and stale directory caches. Confirm bounded backpressure and no omission, duplication, cross-attempt mixing, or leaked sensitive artifacts.

### Security, governance, and lifecycle

Bucket files contain intermediate data and may concentrate all records for one user or entity. Isolate tenant/run/attempt namespaces, permissions, quotas, and encryption keys. Authenticate remote writers/readers and bind authorization to exact exchange operations.

Protect hash seeds where they mitigate attacks; pin them in recoverable controlled metadata. Validate frame lengths, indexes, decompression bounds, record sizes, and bucket identity before allocation. Custom hash/equality/combiner code is untrusted execution.

Cleanup partial, loser, completed, and orphan artifacts only after I/O ends and downstream retry/recovery or approved holds release them. Verify deletion across files, shared containers, indexes, remote chunks, caches, and keys.

## Definitions and Notation

Let $R\ge1$ be destination count, $N\ge0$ records emitted by one producer, and $h_E$ the exchange-pinned hash of normalized key. Let $p_E(k)=norm(h_E(k),R)$ map into $\{0,\ldots,R-1\}$.

Under independent uniform assignments, probability a fixed destination is empty after $N$ records is $(1-1/R)^N$. Therefore:

$$
\mathbb{E}[empty]=R(1-1/R)^N,
$$

and $\mathbb{E}[occupied]=R-\mathbb{E}[empty]$. These expectations do not bound skewed or adversarial inputs.

For dense buffer reservation $b$ per destination and $T$ concurrent producers, base reservation is $M_b=TRb$, excluding records, maps, indexes, codecs, frozen spills, allocators, and native memory.

Let $n_j$ be record count for destination $j$; then $\sum_j n_j=N$. A count-skew ratio can be $\max_j n_j/(N/R)$ for $N>0$, but byte, distinct-key, CPU, segment, and reducer-work skew require separate measures.

## Mechanisms, Invariants, or Proof Structure

Audit hash-based shuffle in this order:

1. Distinguish hash partitioning, hash-organized writing, and hash aggregation in plan and telemetry.
2. Pin key schema, normalization/equality, algorithm, seed, signed normalization, destination count, serializer, and format.
3. Prove grouping-equivalent keys colocate and every admitted key maps to exactly one valid destination.
4. Choose dense, sparse, page, per-file, striped, or consolidated layout from worst-case worker resource bounds.
5. Define bucket append, spill selection, frozen ownership, segment validation, and backpressure.
6. Validate optional hash combining and collision handling using full keys and safe algebra.
7. Define final completeness/empty evidence, segment consolidation, index/checksum, and accepted-attempt publication.
8. Preserve correctness under disk failure, cancellation, retry, speculation, directory invalidation, and cleanup.
9. Measure occupancy, skew, collisions, resource multiplicity, I/O, attempts, and downstream fetch cost.
10. Fault-inject boundaries and review adversarial hashing, tenant isolation, access, retention, and deletion.

Routing correctness follows if $p_E$ is deterministic, total, and returns exactly one destination. Each record is appended once to that bucket. Because grouping-equivalent keys share normalization/hash behavior, they colocate. Final consumer union over exactly one accepted bucket per producer preserves the intended partitioned multiset.

This proof fails if callbacks duplicate append, partial spills publish, empty is confused with missing, attempts mix, or consumers read stale generations. The state machine and authoritative manifest establish those premises.

Dense memory boundedness follows from finite $T$, $R$, and per-bucket charge only if all other scalable allocations and frozen buffers are also capped. Sparse expected occupancy is not a proof of a bound; enforce a hard active-bucket/page budget and fallback/backpressure.

## Alternatives and Trade-Offs

**Hash writer versus sort writer.** Hash avoids global comparison/order work but multiplies destination state and offers no key order. Sort consolidates resources and provides clustering/order at comparison/merge cost.

**Dense versus sparse buckets.** Dense arrays offer fast lookup and predictable allocation for small $R$. Sparse maps avoid empty state and add overhead/unpredictability.

**Per-bucket files versus shared containers.** Separate files simplify direct fetch and explode files/descriptors. Containers reduce objects but need segment indexes or final copying.

**Fixed buffers versus page pool.** Fixed buffers isolate destinations and waste empty capacity. Shared pages adapt to output and require ownership, fairness, fragmentation, and spill policy.

**Direct append versus hash combine.** Direct append preserves records with low table overhead. Combining reduces bytes when valid but grows with distinct keys and needs collision/equality logic.

**Deterministic public seed versus secret seed.** Public fixed seeds simplify compatibility. Secret scoped seeds mitigate selected adversarial attacks but add distribution, recovery, and protection duties.

**Consolidate producer-side versus multi-segment fetch.** Consolidation adds a copy and fewer downstream requests. Multi-segment fetch avoids copy and raises metadata/request/merge overhead.

**Spill hot versus cold buckets.** Hot buckets free substantial memory and may create many segments; cold flushing improves fairness but can create tiny I/O. Measure workload and device behavior.

## Failure Modes and Misconceptions

**“Hash partitioner means hash-based shuffle.”** A sort writer can sort hash destinations; routing and physical organization differ.

**“Expected occupancy bounds memory.”** Expectation under uniform independence is not a worst-case or adversarial guarantee.

**“A good hash solves skew.”** It spreads distinct keys but cannot split one hot grouping key without semantic changes.

**“Hash collision means records are equal.”** Tables must compare full normalized keys; destinations intentionally contain many unequal keys.

**“One buffer per destination is cheap.”** Multiply by destinations, task concurrency, codecs, frozen spills, and allocator granularity.

**“Sparse allocation stays sparse.”** Dense all-to-all records eventually activate nearly every destination.

**“Stable seed gives stable output bytes.”** Destination stability does not order records or asynchronous segments.

**“Empty and missing are equivalent.”** Empty is a validated outcome; missing may represent incomplete publication or loss.

**“SSD eliminates hash-shuffle scaling limits.”** Files, descriptors, metadata, memory, amplification, and service contention remain.

**“Direct append never merges.”** Multiple spill segments may need consolidation or downstream multi-segment handling.

**“Language default hash is portable.”** Runtime, process, identity, type, or version behavior may differ.

**“Hashing keys removes privacy risk.”** Low-entropy values are reversible/enumerable and bucket concentration itself may reveal information.

## Worked Examples

### Example 1

A plan uses hash partitioning and then sorts pointers by destination. It is hash-routed but sort-organized. Telemetry records both fields instead of labeling the whole operation merely “hash shuffle.”

### Example 2

With 2,000 destinations, 32 KiB buffers, and 16 concurrent producers, dense reservation is 1,000 MiB before records and other workspaces. A page pool or sort fallback is required under a smaller worker budget.

### Example 3

One producer emits only ten records into 10,000 destinations. Sparse allocation is valuable. Another emits ten million uniformly distributed records and activates virtually all buckets; sparse maps no longer avoid destination multiplicity.

### Example 4

Two distinct keys share a 32-bit hash. They land in the same destination, which is valid. A hash combiner table compares full keys and keeps separate aggregates; treating the hash as identity corrupts results.

### Example 5

A hot customer key accounts for 40 percent of records. Changing to a stronger hash does not split it because equal keys must colocate. Salting plus a second aggregation can, if the operation is safely decomposable.

### Example 6

A bucket spills three segments. Final metadata lists all three in sequence with lengths and checksums, or consolidates them. Publishing only the latest segment silently loses earlier records.

### Example 7

A runtime randomizes string hashes per process. A retry maps the same key to another reducer. Pinning an exchange hash algorithm/seed and normalized encoding removes process-local variation.

### Example 8

An asynchronous spill freezes pages for destination 9. New records use new pages. The frozen writer releases ownership only after completion; reuse before then can mutate bytes on disk.

### Example 9

Two speculative attempts both write `bucket-3`. Attempt-scoped namespaces prevent collision. Only the winner’s validated manifest is registered; the loser’s files are later erased.

### Example 10

This fixture computes a deterministic bucket distribution and the uniform-occupancy expectation. It is not a hash-quality, spill, storage, or concurrency benchmark.

<!-- bijux-verify: {"id":"hash-bucket-occupancy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"destinations=8 records=20 counts=(3, 3, 3, 3, 2, 2, 2, 2)\nactive_buckets=8 buffer_kib=512\nexpected_active_uniform=7.45 expected_empty_uniform=0.55\n","stderr":""}} -->
```python
destinations = 8
keys = tuple(range(20))
counts = [0] * destinations
for key in keys:
    counts[key % destinations] += 1
active = sum(count > 0 for count in counts)
buffer_kib = destinations * 64
expected_empty = destinations * (1 - 1 / destinations) ** len(keys)
expected_active = destinations - expected_empty

print(f"destinations={destinations} records={len(keys)} counts={tuple(counts)}")
print(f"active_buckets={active} buffer_kib={buffer_kib}")
print(
    f"expected_active_uniform={expected_active:.2f} "
    f"expected_empty_uniform={expected_empty:.2f}"
)
```

## Cross-Program Connections

- **Algorithms and data structures:** hashing, occupancy, load factors, open addressing/chaining, page pools, heavy hitters, and external partitioning define the core.
- **Probability:** balls-into-bins expectations describe idealized occupancy and tails but do not cover correlated or adversarial data.
- **Distributed systems:** deterministic routing, attempt fencing, immutable segments, stale metadata, retry, and failure domains protect correctness.
- **Operating systems:** descriptors, allocator/page behavior, memory mapping, filesystems, random writes, and device queues constrain direct writers.
- **Database systems:** hash aggregation, hash joins, partitioned hash tables, grace spill, and skew handling reuse the same mechanics.
- **Networking:** many tiny buckets amplify requests; framing, batching, compression, and flow control determine fetch behavior.
- **Security:** keyed hashes, flood resistance, untrusted hash code, bucket isolation, encryption, and secret lifecycle follow the threat model.
- **Programming languages:** object equality, array identity, randomized hashes, signed arithmetic, Unicode, and serialization affect portability.
- **Performance engineering:** dense/sparse bounds, occupancy, collision probes, segment counts, disk patterns, and tails guide writer selection.
- **Governance:** hashed identifiers and concentrated buckets remain sensitive and require minimization, access control, and deletion.

## References

1. Jeffrey Dean and Sanjay Ghemawat, [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), 2004.
2. Apache Hadoop, [MapReduce Tutorial](https://hadoop.apache.org/docs/stable3/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html), accessed 2026-09-03.
3. Apache Hadoop, [HashPartitioner API](https://hadoop.apache.org/docs/stable/api/org/apache/hadoop/mapreduce/lib/partition/HashPartitioner.html), accessed 2026-09-03.
4. Apache Spark, [Partitioner API](https://spark.apache.org/docs/latest/api/java/org/apache/spark/Partitioner.html), accessed 2026-09-03.
5. Apache Spark, [HashPartitioner API](https://spark.apache.org/docs/latest/api/java/org/apache/spark/HashPartitioner.html), accessed 2026-09-03.
6. Apache Spark, [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html), accessed 2026-09-03.
7. Apache Spark, [Configuration: Shuffle Behavior](https://spark.apache.org/docs/latest/configuration.html), accessed 2026-09-03.
8. Apache Flink, [Batch Shuffle: Hash and Sort Shuffle](https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/ops/batch/batch_shuffle/), accessed 2026-09-03.
9. Apache Flink, [Batch Shuffle Troubleshooting](https://nightlies.apache.org/flink/flink-docs-release-1.19/docs/ops/batch/batch_shuffle/), accessed 2026-09-03.
10. Apache Flink, [Configuration](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/config/), accessed 2026-09-03.
11. Dask, [Shuffling Performance](https://docs.dask.org/en/latest/dataframe-groupby.html), accessed 2026-09-03.
12. Dask, [DataFrame.shuffle API](https://docs.dask.org/en/latest/generated/dask.dataframe.DataFrame.shuffle.html), accessed 2026-09-03.

## Exercises

### Exercise 1

Compute dense base buffer memory for 12 concurrent producers, 1,500 destinations, and 48 KiB per destination. List at least six excluded memory/resource categories and propose a safer physical alternative.

### Exercise 2

For $N=5$ records and $R=100$ destinations under independent uniform routing, compute expected occupied and empty destinations. Explain why neither number is a capacity bound.

### Exercise 3

Specify a cross-language partition contract for strings used by Java and Python producers, including normalization, encoding, hash, seed, signed mapping, equality, nulls, versioning, and test vectors.

### Exercise 4

Design a bounded page-pool and bucket-spill state machine for one producer. Cover giant records, asynchronous writers, same-bucket new records, disk-full, cancellation, segment completeness, final publication, and cleanup.

### Exercise 5

Choose hash-based or sort-based physical organization for: 32 destinations with no key-order requirement; 50,000 destinations on HDD; and 500 destinations with safe high-reduction key aggregation but adversarial keys. Justify evidence and safeguards.

## Answers to the Exercises

### Answer 1

$12\times1{,}500\times48$ KiB is 864,000 KiB, about 843.75 MiB. Excluded costs include serialized records, bucket objects/maps, indexes, codec/encryption workspaces, frozen spill buffers, writer buffers, direct/native memory, descriptors, allocator granularity, file metadata, and other worker tasks. A bounded shared page pool with sparse bucket metadata plus consolidated/striped files can limit memory and descriptors; a sort-based fallback may be better when most destinations activate. Capacity uses the full worker concurrency model, not the base figure alone.

### Answer 2

Expected empty is $100(0.99)^5\approx95.10$ and expected occupied is about 4.90. Collisions make occupied slightly less than five. These are expectations across independent uniform trials. One producer could occupy one through five buckets, real hashes/keys may be correlated or adversarial, and per-bucket/page metadata plus giant records still matters. Enforce hard active-bucket/page and process limits rather than allocating from expectation.

### Answer 3

Normalize strings with a named Unicode form and pinned version, encode UTF-8 with a specified invalid-input policy, and hash exact bytes using a named algorithm/version plus exchange seed. Convert the fixed-width result to an unsigned integer or defined floor-mod, then reduce by pinned $R$. Define equality on normalized strings, ensuring equal values hash identically. Give null a specified separate encoding/destination rule. Persist contract/version/seed securely with exchange metadata. Publish test vectors including empty, ASCII, non-ASCII, canonically equivalent forms, emoji, invalid sequences, long strings, boundary hash values, and several $R$ values; Java and Python must match exactly.

### Answer 4

Give the attempt a finite page pool, reserve for one maximum record/index and control progress, and maintain sparse bucket chains. On pressure, atomically detach chosen complete segments; new same-bucket records receive other pages. A bounded writer queue owns frozen pages until validated write completion. Oversized records use a bounded framed streaming path or fail. Disk-full quarantines partial data, stops/reduces production, and uses only approved alternate capacity. Cancellation fences late callbacks. Finalization waits for writers, validates segment identities/sequences/lengths/checksums, proves each destination complete or empty, optionally consolidates, and publishes only if the attempt wins. Cleanup is idempotent after I/O and recovery/hold references end.

### Answer 5

For 32 destinations and no order, direct hash buckets or bypass can avoid comparisons if dense buffers/files fit and SSD/storage behavior is healthy. For 50,000 destinations on HDD, sort-based clustering or bounded consolidated pages is preferable because per-destination buffers/files and random I/O explode. For 500 destinations with high-reduction safe aggregation, hash tables may reduce bytes substantially, but use a flood-resistant scoped hash/seed, load/probe limits, bounded spill partitions, full-key equality, and fallback; compare sort-based streaming combine. In all cases measure active buckets, memory, descriptors, segments, comparison/hash CPU, reduction ratio, skew, disks, output/fetch requests, failure recovery, and downstream order needs.
