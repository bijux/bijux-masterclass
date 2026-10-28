---
module_id: DBE-054
program: Database Engineering
level: 2
module_number: 54
title: Hash Joins
status: complete
last_verified: 2026-08-30
---

# Hash Joins

## One-Page Review

### Governing question

How can an execution engine transform equality-compatible join work into build-and-probe hash operations while preserving bags, nulls, residual predicates, outer/semi/anti semantics, memory bounds, and failure safety under collisions, spill, skew, and parallelism?

### Essential definitions

A **hash join** builds a hash table from one input's join keys and probes it with the other input. A **hash bucket** holds build occurrences whose hash values map to the same location; hash equality identifies candidates, not necessarily equal keys. A **residual equality/recheck** compares full keys and any remaining join condition after bucket lookup. The **build side** populates the table; the **probe side** streams lookups. **Grace hash join** partitions both inputs by hash so corresponding partitions can be joined within memory. **Hybrid hash join** retains one or more build partitions in memory while spilling others. A **batch** is a corresponding build/probe partition pair. **Skew** is nonuniform key or partition frequency. A **dynamic/Bloom filter** can conservatively reject probe rows whose keys are definitely absent; false positives are rechecked.

### Central model, mechanism, or theorem

For equality relation ∼ and hash function (h), correctness requires (x ∼ y ⇒ h(x)=h(y)); the converse is not required. Insert every eligible build occurrence into its bucket. For each probe occurrence, inspect its bucket and emit every candidate pair whose full equality and join qualification are TRUE. Partitioned execution is correct when the same deterministic partition function sends every equal build/probe key to the same batch and every batch is processed exactly once. Cost is approximately linear only under bounded hashing/equality work, manageable skew, sufficient memory or bounded repartitioning, and accountable I/O.

### Critical invariants

- Every build occurrence is retained or durably assigned to exactly one recoverable partition; duplicates are never collapsed accidentally.
- Equal join keys use compatible type, collation, normalization, equality, and hash semantics.
- Hash collisions trigger equality and residual rechecks; hash-value equality is never final qualification.
- Ordinary SQL equality does not match NULL; null-safe equality uses a deliberately compatible key representation.
- Inner/outer/semi/anti output and match tracking operate per row occurrence, including unmatched build rows for right/full joins.
- Spill partitions use the same logical key semantics on both inputs and are neither skipped nor processed twice.
- Memory accounting includes buckets, tuples, metadata, allocator overhead, filters, parallel workers, and concurrent operators.
- Hash joins promise no application-visible ordering unless a later operator establishes it.

### Common failures

Failures include assuming hash joins support arbitrary predicates; choosing equality-incompatible hashing; returning all bucket residents without recheck; storing only one row per key; matching NULLs accidentally; building on the physically larger or wider side from bad estimates; treating `work_mem` as a query-wide budget; losing rows during batch growth or recursive spill; infinite repartitioning on one heavy key; using a Bloom filter with false negatives; failing to track unmatched build rows for full join; assuming bucket order is stable; and raising memory globally after one spill without modeling concurrency.

### Compact example

A deliberately weak parity hash places keys 1, 3, and probe key 5 in the same bucket. Two duplicate outer rows with key 1 match two build rows with key 1, yielding four rows; key 3 yields one, key 2 yields one. Full equality rejects seven colliding candidates, while NULL and absent key 5 remain unmatched. The executable proves this finite bag and collision discipline, not the safety or performance of a production hash table.

### Connections

Retrieve [Hash Functions and Distribution](../../17-data-structures-engineering/modules/021-hash-functions-and-distribution.md), [Joins and Join Semantics](012-joins-and-join-semantics.md), [Snapshot Visibility](047-snapshot-visibility.md), [Logical and Physical Plans](051-logical-and-physical-plans.md), and [Nested-Loop Joins](053-nested-loop-joins.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to single-node sort-merge joins and aggregation.

## Governing Question

What semantic, state-machine, partitioning, and resource proofs make in-memory, spilled, parallel, and distributed hash joins correct and predictable?

## Why This Matters

Hash join is a foundational bulk equality operator. It can scan two unsorted inputs, build one compact search structure, and probe in expected constant time per row. Unlike index nested loop, it does not require a persistent inner index or repeat a lookup tree for every probe. Unlike merge join, it does not require ordered inputs. For broad equijoins, these properties often make it an excellent default.

Its friendly (O(n+m)) summary hides consequential assumptions. Hash functions collide; duplicate keys need multiple stored occurrences; SQL NULL usually does not equal NULL; composite equality must agree with hashing across types and collations. The build may exceed memory and partition to temporary storage. Skew can create one enormous bucket or batch that repartitioning cannot shrink. Parallel workers can duplicate private hash tables or coordinate one shared table, changing memory, synchronization, and data movement.

Hash join also changes pipeline behavior. It ordinarily blocks probe output until the build side is consumed enough to construct a table or partition state. It does not naturally deliver sorted results. A small first-row latency requirement or existing useful order can make nested loop or merge superior even if a local hash cost is lower. A final sort, exchange, or spill belongs in the global comparison.

In production, a spill is evidence rather than an automatic defect. A bounded, sequentially accessed partition spill can be safer than memory overcommit across many concurrent joins. Conversely, a planner that badly underestimates build rows can create many batches, extra writes/reads, long tails, and storage exhaustion. The right response combines semantic verification, plan/cardinality evidence, memory accounting, concurrency, temporary-storage capacity, and alternative algorithms.

## Prerequisites and Retrieval

You should understand SQL bag/null join semantics, hash tables, collision resolution, pages/buffers, external-memory algorithms, snapshots, physical plans, cardinality estimation, and parallel/distributed data exchange. Retrieve build, probe, hash key, bucket, candidate chain, residual recheck, load factor, cardinality, row width, memory budget, batch, fanout partitioning, recursive repartition, skew/heavy hitter, Bloom/dynamic filter, matched bitmap, spill, broadcast, repartition exchange, barrier, and cleanup.

DBE-053 derived nested-loop semantics and multiplicative costs. Hash join retains the same logical result while replacing repeated inner evaluation with a bulk key structure. DBE-055 will compare this unordered equality specialization with ordered merge processing.

## Learning Objectives

After this module, you can:

1. state the equality-hash compatibility law and explain why collision recheck is mandatory;
2. derive in-memory hash join for inner, left/right/full outer, semi, and anti joins under bag/null semantics;
3. trace build/probe state, duplicate chains, matched flags, residual predicates, and cleanup;
4. derive Grace and hybrid partitioning correctness and approximate I/O costs;
5. diagnose load factor, bucket-chain, build-size, batch, spill, skew, and cardinality failures;
6. compare private versus shared parallel hash tables and broadcast versus repartitioned distributed joins;
7. reason about conservative dynamic filters and their lifecycle/false-positive contract;
8. account for operator, worker, query, and workload memory rather than one nominal setting;
9. design differential, property, spill, skew, fault, and concurrency tests; and
10. choose hash, nested-loop, or merge strategies using global properties and representative evidence.

## Core Exposition

**Begin with equality semantics.** Let build bag (B), probe bag (P), join equality ∼, and remaining qualification (q(b,p)). A valid hash function satisfies the compatibility implication (b ∼ p Rightarrow h(b)=h(p)). If equal values can hash differently because of inconsistent collation, normalization, coercion, NaN rules, endianness, or versioning, the algorithm can silently omit matches. Collision safety requires no converse: unequal keys may share a hash, but full equality and (q) must reject them.

Ordinary SQL `=` returns UNKNOWN when either input is NULL, so nullable equality keys usually need not enter/probe a matching bucket for inner join. `IS NOT DISTINCT FROM` or another null-safe comparator treats nulls differently and requires a compatible hash/key encoding. Composite keys apply component semantics and coercions consistently. Equality must behave sufficiently like an equivalence relation for the chosen hash operator class; engine-specific exceptional values need explicit contracts.

**In-memory build and probe preserve occurrences.** Choose a build input, allocate bucket metadata, and consume build rows. For every eligible row, compute a hash, choose a bucket, and store the row or needed payload plus hash/key metadata. Do not overwrite an existing equal key: a join hash table is commonly a multimap because every build occurrence can contribute output.

After build completion, consume probe occurrences. Compute the compatible hash, visit the corresponding bucket, cheaply compare stored hash where useful, then evaluate full equality and residual join qualification. Emit every TRUE pair for inner join. Hash table collision strategy—chaining, open addressing plus duplicate storage, Swiss-table-like groups, radix partitioning, or another layout—is an implementation decision constrained by these semantics.

Build cost includes hashing, allocation, copying/reference retention, and possible visibility/materialization work. Probe cost includes hashing, bucket lookup, candidates examined, equality/residual CPU, and output. A simplified expected model is


(C_{mem}=C_B+C_P+|B|c_{insert}+|P|c_{probe}+N_c c_{recheck}+|J|c_{emit}),


where (N_c) counts bucket candidates and |J| output occurrences. Expected linearity assumes controlled bucket occupancy; adversarial collisions or one heavy key can make (N_c) approach |B||P| even though hashing itself is fast.

**Join kind changes state, not the equality core.** Left outer join with probe as preserved side emits a null-extended probe occurrence when its complete bucket scan finds no TRUE join qualification. Left semi join emits the probe occurrence once at the first TRUE match; left anti emits it only after no TRUE match exists. If the build side is preserved for right/full join, store a matched bit per build occurrence—not merely per key—and after all probes emit each unmatched occurrence once. A post-join filter remains distinct from join qualification and null extension.

Early termination is legal for semi/anti bucket search as in nested loops, but not for inner/outer joins that require every duplicate pair. If one build key occurs (m) times and one probe key (n) times, inner output contains (mn) occurrences. A hash table that stores a single representative row is suitable only for explicitly uniqueness-proven or existence semantics.

The finite executable below deliberately uses parity hashing to create collisions. It compares full keys after lookup, preserves duplicates, applies ordinary SQL-like NULL equality, and derives left/semi/anti output. It omits types/collations, MVCC, memory limits, spill, parallelism, faults, and real performance.

<!-- bijux-verify: {"id":"hash-join-collision-and-bag-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"bucket_sizes=((0, 1), (1, 3))\ninner_rows=(('A', 'x'), ('A', 'y'), ('A', 'x'), ('A', 'y'), ('B', 'z'), ('C', 'c'))\nleft_rows=(('A', 'x'), ('A', 'y'), ('A', 'x'), ('A', 'y'), ('B', 'z'), ('C', 'c'), ('N', None), ('D', None))\nsemi_rows=('A', 'A', 'B', 'C')\nanti_rows=('N', 'D')\ncandidates_examined=13\ncollision_rejections=7\nfull_equality_rechecked=True\nevidence=finite_collision_and_bag_model\n","stderr":""}} -->
```python
build = (("x", 1), ("y", 1), ("z", 2), ("null", None), ("c", 3))
probe = (("A", 1), ("A", 1), ("B", 2), ("C", 3), ("N", None), ("D", 5))


def sql_equal(left, right):
    return left is not None and right is not None and left == right


def weak_hash(key):
    return key % 2


buckets = {}
for name, key in build:
    if key is not None:
        buckets.setdefault(weak_hash(key), []).append((name, key))

inner_rows = []
left_rows = []
semi_rows = []
anti_rows = []
candidates = 0
collisions = 0

for probe_name, probe_key in probe:
    bucket = () if probe_key is None else buckets.get(weak_hash(probe_key), ())
    matches = []
    for build_name, build_key in bucket:
        candidates += 1
        if sql_equal(probe_key, build_key):
            matches.append(build_name)
        else:
            collisions += 1
    inner_rows.extend((probe_name, build_name) for build_name in matches)
    left_rows.extend((probe_name, build_name) for build_name in matches or [None])
    (semi_rows if matches else anti_rows).append(probe_name)

print(f"bucket_sizes={tuple(sorted((key, len(rows)) for key, rows in buckets.items()))}")
print(f"inner_rows={tuple(inner_rows)}")
print(f"left_rows={tuple(left_rows)}")
print(f"semi_rows={tuple(semi_rows)}")
print(f"anti_rows={tuple(anti_rows)}")
print(f"candidates_examined={candidates}")
print(f"collision_rejections={collisions}")
print(f"full_equality_rechecked={candidates == len(inner_rows) + collisions}")
print("evidence=finite_collision_and_bag_model")
```

**Memory is part of the algorithm.** Estimate build occurrences times stored row width, hash/key metadata, tuple headers, alignment, allocator/chunk overhead, bucket array, load-factor slack, matched flags, and optional Bloom/skew structures. Account for expression and child-operator memory too. A configuration named per-operation memory is not necessarily a whole-query or whole-server cap: multiple hash/sort operators, partitionwise plans, workers, and sessions can multiply it.

PostgreSQL 18 currently documents `work_mem` as a base amount before operations such as hash tables write temporary files and `hash_mem_multiplier` as the multiplier used for hash-operation limits. Its EXPLAIN output can show buckets, batches, and memory usage. These are product/version observations, not a portable sizing formula. Capacity planning must use the exact engine/build and concurrency topology.

**Grace partitioning turns memory pressure into external work.** Choose partition function (g(h(key))) and write each build row to build partition (B_k), each probe row to corresponding (P_k). Because equal keys share compatible hashes, they share (k). Process each pair ((B_k,P_k)) with an in-memory hash table when it fits. Every pair that could match is colocated; partitions with one side empty can be skipped where join-kind semantics allow.

If both inputs are first read and partitioned, then partitions are read for join, a simplified Grace cost is about (3(B_B+B_P)) pages: one initial read, one partition write, one partition read. Output, temporary metadata, cache, and recursion are extra. Hybrid hashing keeps an in-memory partition, avoiding its spill I/O. If a partition still exceeds memory, repartition it with a different hash bit/radix/seed; otherwise recursive repartition repeats the same imbalance.

Partition correctness requires durable ownership. During dynamic batch growth, every already-built tuple and every future build/probe tuple must map to exactly one processed batch. Temporary files need checksummed/validated records as appropriate, explicit errors, and cleanup on cancellation. Disk-full, corrupted spill, or worker death cannot silently become an empty partition. Retrying a batch must prevent duplicate output or restart at a transactionally safe operator boundary.

**Skew defeats average-case comfort.** A heavy join key creates a huge bucket and potentially (mn) legitimate output; no repartitioning on that same key can split equality work without adding another dimension. Hash-value skew can also concentrate unequal keys due to poor functions. Detect heavy hitters and partition-size imbalance. Remedies include a dedicated skew table, broadcasting/replicating heavy-key build rows while distributing probe rows, splitting heavy-key work by row ranges with careful output ownership, switching algorithms, or rejecting resource-explosive queries under policy.

There is a lower bound hidden by tuning: if the logical result contains billions of duplicate pairs, the executor must represent/stream that output or a higher logical operator must reduce it. More buckets do not remove (mn) output. Semi/anti joins can compress build state to key existence and early-stop; inner/outer joins cannot unless downstream semantics support proven aggregation or late materialization.

**Dynamic filters reduce upstream work only conservatively.** A Bloom filter built from hash keys may be pushed toward the probe scan. A negative result can discard a probe only if the filter has no false negatives for every eligible build key and its equality/hash semantics match. Positive results remain candidates because Bloom filters have false positives. For outer joins, preserved-side filtering can be illegal: an unmatched preserved probe row may still need null extension. Distributed arrival, incomplete build, version mismatch, and filter corruption require barriers or safe fallback.

**Parallel hash join has two broad shapes.** With private tables, each worker may build its own copy from a complete build input, simplifying local probes but multiplying memory/build work. With a shared table, workers cooperate in build and probe, paying shared allocation, synchronization, barriers, skew contention, and failure coordination. PostgreSQL 18 distinguishes ordinary parallel-oblivious hash join, where each worker builds a private table, from Parallel Hash, where workers share construction; exact behavior remains version-specific.

Distributed hash join adds network placement. A broadcast join sends a sufficiently small build relation to each probe partition; network/memory cost scales with recipients but preserves probe placement. A repartition/shuffle join sends both inputs by compatible join-key partition, enabling local hash joins but paying network serialization, buffering, barriers, and skew. Bucket/partition functions must agree across language/runtime/version boundaries; deterministic canonical key encoding is part of correctness.

Partial failures complicate output. A worker cannot simply replay an already emitted partition without deduplication or downstream transactional boundaries. Systems may materialize shuffle partitions, checkpoint batch completion, or make stages retryable before externally visible output. Specify exactly-once, at-least-once plus deduplication, or restart semantics instead of assuming “query retry” is harmless.

**Ordering and pipelining are explicit trade-offs.** A conventional hash join blocks on build and emits in probe/bucket traversal order, which is not a SQL promise. Resizing, batch count, parallel scheduling, hash seed, and spill can change it. Required `ORDER BY` needs a compatible later sort or other proven property. A hash join can stream probe output after build, but spilled batches delay their rows; full/right unmatched-build output often waits until probing completes.

Compare startup and total cost. A selective index nested loop can return early; merge may exploit existing order; hash may win total broad equality work. A final order, `LIMIT`, downstream grouping, vectorization, exchange, and materialization make the choice global. Hash join is usually unsuitable as the sole mechanism for non-equality theta predicates, though an equality subset may hash candidates before residual range/spatial conditions.

**Estimation and observability close the loop.** Estimate build rows/width, distinct keys, null fraction, most-common values, probe rows, join fanout, residual selectivity, bucket/partition distribution, memory overhead, and concurrency. Wrong side choice or underestimated width can trigger spill. Correlated composite keys and cross-table skew can make independence estimates especially poor.

Capture structured plan and actual build/probe rows, widths where possible, buckets/load/chain distribution, batch count and growth, memory peak, temporary bytes/files/read/write, skew buckets, dynamic-filter rows removed, worker participation/waits, exchange bytes, output rows, first/last-row time, cancellation cleanup, and estimates at each boundary. Explain fields differ by engine/version; missing counters are not zeros.

**Verification needs semantic and resource adversaries.** Compare hash output with a simple nested-loop oracle for empty inputs, duplicates, nulls, null-safe comparators, composite/collated keys, deliberate collisions, unequal values with equal hashes, residual predicates, every join kind, huge fanout, and errors. Property-test equality-hash compatibility. Plant an inconsistent hash implementation and ensure tests detect missing pairs.

Force one-batch, multi-batch, dynamic growth, recursive repartition, heavy-key skew, empty partitions, spill corruption/disk-full, worker loss, cancellation at state transitions, and parallel/distributed retry. Compare bags and required order separately. Performance tests sweep memory, build orientation, rows/width, distinctness/skew, spill medium, concurrency, worker count, network, and downstream demand. Validate results before timing and gate memory/temp quotas, p95/p99, throughput, fairness, recovery, and cleanup.

## Definitions and Notation

- (B,P): build and probe bags; |B| and |P| count occurrences.
- ∼: join-key equality relation; (q(b,p)): remaining join qualification.
- (h): equality-compatible hash; (g): partition selector derived from hash bits/value.
- **Bucket**: candidate collection sharing a table location/hash prefix, not a proof of equality.
- (N_c): bucket candidates examined; |J|: emitted join occurrences.
- **Load factor**: stored entries relative to bucket/table capacity.
- **Build/probe**: physical table-construction and lookup roles.
- **Batch/partition**: corresponding build/probe subsets processed together.
- **Grace hash**: external partition-then-join strategy.
- **Hybrid hash**: partitioning that retains some build state in memory.
- **Skew/heavy hitter**: disproportionate bucket, partition, or key frequency.
- **Matched bitmap/flag**: per-build-occurrence state for unmatched-build emission.
- **Dynamic/Bloom filter**: conservative membership summary; negative exclusion requires no false negatives.
- **Broadcast/repartition**: distributed placement of one build everywhere or both sides by key.

## Mechanisms, Invariants, or Proof Structure

For an in-memory inner join, after building, invariant one states every eligible build occurrence appears once in the bucket selected by its compatible hash. While probing row (p), invariant two states emitted rows include exactly TRUE-qualified pairs between (p) and the inspected prefix of its bucket plus all pairs for previous probes. Compatibility proves every equal build key is in that bucket; full equality/residual recheck proves collision soundness. Exhaustion proves the bag result.

Outer/semi/anti proofs add per-occurrence match state and the transitions from DBE-053. Partition proof defines (B_k={b:g(h(b))=k}) and (P_k={p:g(h(p))=k}). Equal pairs share (k); disjoint batches cover inputs exactly once, so the union of local join bags equals the global join. Spill/retry mechanisms must implement that mathematical partition ownership without loss or duplication.

Cost claims are conditional expected or external-I/O models. They do not prove bounded collision chains, uniform partitions, memory residency, or performance. Measure those assumptions and treat adversarial skew/output as first-class.

## Alternatives and Trade-Offs

In-memory hash offers expected linear equality work and unordered inputs but needs build memory/startup. Grace/hybrid hash bounds memory through temp I/O and batch latency. Radix/partitioned hash improves cache/parallel locality but adds passes and tuning. Nested loops support arbitrary predicates, parameterization, and low startup but may multiply inner work. Merge handles equality/range-like ordered processing and can deliver order but requires compatible ordering/sorts. Persistent index joins reuse maintained structures at write/storage cost. Distributed broadcast avoids shuffling the large probe only when replicated build size and memory are safe; repartition handles two large sides but pays network/barrier/skew.

Select by semantics, input properties, build size/width, fanout/skew, memory/temp/network budgets, concurrency, startup/order requirements, reuse, and failure model. Global memory increases, hints, and forced join toggles are scoped diagnostics or governed mitigations, not automatic durable fixes.

## Failure Modes and Misconceptions

1. **“Same hash means equal.”** Hash equality gives candidates; full key and residual checks decide matches.
2. **“Hash join is always linear.”** Collisions, skew, recursive spill, output fanout, and expensive equality can dominate.
3. **“One row per key is enough.”** Inner/outer bag joins preserve every build occurrence unless uniqueness is proven.
4. **“NULLs belong in one matching bucket.”** Ordinary equality yields UNKNOWN; null-safe equality is a distinct contract.
5. **“Build the smaller table by name.”** Use post-filter actual/estimated rows, widths, state overhead, and semantic role constraints.
6. **“Spill means failure.”** Bounded spill may be correct capacity control; uncontrolled batches/temp exhaustion are the failure.
7. **“Rehashing fixes every oversized partition.”** A single heavy equality key remains heavy and may produce unavoidable (mn) output.
8. **“A Bloom filter may drop probable misses.”** Only definite negatives under a no-false-negative contract are safe.
9. **“Per-operation memory caps the query.”** Operators, partitions, workers, and sessions multiply aggregate consumption.
10. **“Parallel workers only speed the join.”** They add memory, synchronization, exchange, skew, and retry complexity.
11. **“Hash output order is stable.”** Bucket layout, seed, resizing, spill, and scheduling can change it.
12. **“Raise memory until batches disappear.”** Model concurrent workload, temp trade-offs, fairness, and safer plan/schema/statistics remedies.

## Worked Examples

### Example 1

Build key 1 occurs twice and probe key 1 occurs three times. The bucket stores two occurrences; each probe scans both and emits six rows. Conclusion: hash tables for bag joins are multimaps and output multiplicity is (2×3).

### Example 2

Keys 1 and 3 share parity hash 1. Probe key 5 reaches their bucket but equals neither. Returning bucket residents would create false rows; equality recheck returns none. Conclusion: collisions affect cost, never permitted semantics.

### Example 3

Both sides contain NULL under ordinary `=`. Neither forms a TRUE equality match; a preserved probe NULL becomes null-extended in a left join. Under `IS NOT DISTINCT FROM`, a compatible null token may match. Conclusion: hash-key treatment follows the chosen comparator.

### Example 4

A right/full join builds three duplicate rows for key K; one probe K matches all. Marking only “key K matched” happens to cover this case, but per-row flags are required generally when residual predicates can match only some occurrences. Conclusion: unmatched-build state belongs to occurrences.

### Example 5

Build and probe occupy 1,000 and 4,000 pages and cannot fit memory. Simplified Grace processing reads both, writes partitions, then reads them: (3×5,000=15,000) page transfers before output. Conclusion: external hashing trades bounded memory for approximately two extra full-input transfers.

### Example 6

One partition remains too large because tenant “global” owns 60% of rows. Repartitioning solely on the same tenant key repeats the imbalance. Isolate the heavy key, split work with a second ownership dimension, or use another plan while preserving pair uniqueness. Conclusion: skew needs explicit treatment.

### Example 7

A Bloom filter built from completed inner keys rejects 80% of probe rows and has false positives among the rest. Rejected rows are safe only for an inner/semi context; filtering the preserved side of a left join would lose required unmatched rows. Conclusion: dynamic-filter placement depends on join semantics.

### Example 8

Four workers each build a 500 MB private table: roughly 2 GB plus overhead, not 500 MB. A shared parallel hash may reduce duplication but adds barriers and contention. Conclusion: account for the actual parallel architecture and peak overlap.

### Example 9

Estimated build is 100,000 narrow rows; actual is 20 million wide rows. EXPLAIN shows batch growth and large temporary writes. Fix stale/correlated statistics or predicate semantics, reconsider build side/join order, and validate temp/memory rather than globally disabling hash joins. Conclusion: spill diagnosis starts with estimate provenance.

### Example 10

A distributed broadcast sends a “small” dimension to 200 workers, but tenant policy expansion makes it 2 GB, exhausting aggregate memory. Repartitioning both sides or prefiltering the dimension is safer. Conclusion: broadcast cost is build size times recipients and must include authorization-dependent cardinality.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies hash tables, collision resolution, Bloom filters, cache layouts, and adversarial hashing.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies expected versus worst-case analysis, external-memory models, partitioning, and skew experiments.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies cache/TLB locality, SIMD probing, memory bandwidth, NUMA, and contention.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies memory accounting, temporary I/O, page cache, asynchronous writes, quotas, and cleanup.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies shuffle, broadcast, barriers, retries, deterministic partitioning, and partial failure.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies collision-denial resistance, tenant isolation, spill confidentiality, and resource-abuse controls.

## References

1. PostgreSQL Global Development Group, [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; hash build/probe plans, buckets, batches, memory, and runtime interpretation.
2. PostgreSQL Global Development Group, [Query Planning Configuration](https://www.postgresql.org/docs/current/runtime-config-query.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; hash-join planner controls and diagnostic scope.
3. PostgreSQL Global Development Group, [Resource Consumption](https://www.postgresql.org/docs/current/runtime-config-resource.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; per-operation work memory, hash multiplier, concurrency, and parallel resource multiplication.
4. PostgreSQL Global Development Group, [Parallel Plans](https://www.postgresql.org/docs/current/parallel-plans.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; private versus shared parallel hash construction.
5. PostgreSQL Global Development Group, [`nodeHashjoin.c`](https://github.com/postgres/postgres/blob/REL_18_STABLE/src/backend/executor/nodeHashjoin.c), PostgreSQL 18 stable source, retrieved 2026-08-30; serial/parallel state machine, join kinds, batches, and rescan behavior.
6. PostgreSQL Global Development Group, [`nodeHash.c`](https://github.com/postgres/postgres/blob/REL_18_STABLE/src/backend/executor/nodeHash.c), PostgreSQL 18 stable source, retrieved 2026-08-30; bucket/batch sizing, growth, skew, memory, and parallel coordination.
7. Oracle, [Hash Join Optimization](https://dev.mysql.com/doc/refman/8.4/en/hash-joins.html), MySQL 8.4 Reference Manual, retrieved 2026-08-30; current hash-join applicability and explain evidence.
8. Goetz Graefe, [“Query Evaluation Techniques for Large Databases”](https://web.stanford.edu/class/cs346/2014/graefe.pdf), *ACM Computing Surveys* 25(2), 1993; in-memory, partitioned, hybrid, overflow, and parallel hash join foundations.
9. Andy Pavlo, [“Join Algorithms”](https://15445.courses.cs.cmu.edu/fall2023/slides/11-joins.pdf), CMU 15-445/645 lecture notes, Fall 2023; hash table, Grace hash, cost, and comparison derivations.
10. PostgreSQL Global Development Group, [Comparison Functions and Operators](https://www.postgresql.org/docs/current/functions-comparison.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; ordinary NULL comparison and distinctness semantics.

## Exercises

### Exercise 1

For build bag `[1a,1b,2,NULL]` and probe bag `[1x,1y,3,NULL]`, derive inner, probe-preserving left, semi, and anti hash-join output under ordinary equality. State bucket and match invariants.

### Exercise 2

Derive in-memory state and simplified Grace I/O for a 12-million-row, 96-byte build plus 24 bytes per entry overhead, a 40-million-row probe, 8 KiB pages, and a 512 MiB operator budget. State why the estimate is incomplete.

### Exercise 3

Design a spill-capable full outer hash join state machine with dynamic batch growth. Specify per-row ownership/match tracking, files, transitions, retry/cancellation, and correctness evidence.

### Exercise 4

Diagnose a parallel hash join whose batch count, temp writes, worker imbalance, and p99 rise after a new dominant tenant arrives. Compare memory, statistics, skew, join order, algorithm, and workload controls.

### Exercise 5

Design a secure distributed hash join between a large event fact and authorization-filtered tenant dimension. Address key canonicalization, broadcast/repartition choice, dynamic filters, skew, spill confidentiality, failures, exactly-once output, and release gates.

## Answers to the Exercises

### Answer 1

Store build occurrences `1a`, `1b`, and `2`; ordinary NULL cannot match. Each probe `1x` and `1y` checks the key-1 bucket and matches both build occurrences, so inner output has `(1x,1a)`, `(1x,1b)`, `(1y,1a)`, `(1y,1b)`. Probe 3 and NULL do not match. Probe-preserving left adds `(3,null-extended)` and `(NULL,null-extended)`. Semi output preserves probe occurrences `[1x,1y]`; anti is `[3,NULL]`. Every eligible build occurrence exists once in its hash-selected bucket; every equal key reaches that bucket; equality recheck admits exactly TRUE pairs; match state is per probe occurrence. Hash collisions would add candidates but not output.

### Answer 2

Modeled entry bytes are (12,000,000×(96+24)=1,440,000,000) bytes, about 1.34 GiB, already above 512 MiB before bucket-array slack, alignment, allocator chunks, matched flags, expression state, child buffers, and skew/filter metadata. The build therefore cannot be claimed in-memory. To estimate Grace pages, probe row width and exact stored/projected widths are missing. If build bytes are 1.44 GB, build pages are `ceil(1,440,000,000/8192)=175,782`; derive probe pages only after its row width. Simplified partition-and-read I/O is three times total input pages, plus output and recursive/metadata I/O. The estimate remains incomplete without key distribution, nulls, load factor, compression/serialization, memory implementation, page utilization, concurrency/workers, temp storage/cache, residual CPU, fanout, and actual engine policy.

### Answer 3

Assign every build/probe occurrence a stable operator-local identity and batch from the same compatible partition function. Persist records with batch, identity, key/hash, needed payload, and integrity/version metadata; track a per-build-occurrence matched bit for full join. Build a batch table, probe its corresponding records, recheck full equality/residuals, emit pairs once, and mark exact build occurrences. After probe exhaustion, emit unmatched probe rows as required; after the batch, emit unmatched build occurrences. Dynamic growth atomically migrates or assigns each record to one new child batch before the old batch becomes complete. Maintain batch states such as created, build durable, probe durable, joining, output committed, complete; retry only from a boundary whose output is discarded or idempotently identified. On cancellation/disk-full/corruption/worker loss, fail explicitly and clean owned files after readers stop. Evidence compares every forced-growth/failure schedule with a tuple-loop full-join oracle and reconciles input ownership, pair output, unmatched output, and temporary cleanup.

### Answer 4

Capture exact engine/build/settings, SQL/parameters, schema, build/probe choice, estimates/actual rows and widths, tenant frequency/extended statistics, buckets/batches/growth, memory peak, temp reads/writes/files/latency, worker rows/time/waits, exchange bytes, output fanout, concurrency, and result bags. A dominant tenant can create one unsplittable key partition and output explosion; more memory may not cure it and per-worker limits can overcommit. Correct statistics and tenant correlations, filter earlier, change join order/build side, isolate heavy keys with proven output ownership, reduce/bound parallelism, use merge or indexed strategy where properties favor it, or schedule/resource-govern the tenant. Increase memory only from aggregate capacity evidence. Gate correctness, p95/p99, temp capacity, worker balance, fairness, other-workload impact, cancellation cleanup, and rollback; do not suppress the tenant or disable hash globally without semantic/operational proof.

### Answer 5

Canonicalize tenant and join keys with versioned type/collation/equality/hash rules shared by every worker. Apply authorization on the dimension before distribution and bind policy/snapshot identity. Broadcast only if the filtered dimension's high-confidence size times recipients fits aggregate memory and privacy rules; otherwise repartition both inputs by tenant/key, with explicit heavy-tenant handling and deterministic partition version. A completed-build Bloom filter may reject fact rows only for join contexts where absence permits dropping; it must have no false negatives and cannot remove preserved outer rows. Encrypt and access-control shuffle/spill, avoid sensitive raw keys in logs, checksum records, quota temp/memory/network, and erase files after safe completion. Give partitions and output records stable identities; checkpoint input durability and output commit so retries do not duplicate or omit. Test adversarial collisions, cross-tenant equal IDs, policy changes, NULLs, duplicates, skew, worker loss, corrupt/missing spill, retries, and cancellation. Release gates reconcile bags/authorization, prove no cross-tenant leakage, and bound memory/temp/network, p99, source impact, recovery, cleanup, and rollback.
