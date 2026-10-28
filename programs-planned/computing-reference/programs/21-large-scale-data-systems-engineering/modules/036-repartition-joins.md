---
module_id: LSDS-036
program: Large-Scale Data Systems Engineering
level: 1
module_number: 36
title: Repartition Joins
status: complete
last_verified: 2026-09-03
---

# Repartition Joins

## One-Page Review

### Governing question

How should a distributed engine move two join inputs into compatible key partitions, exploit trustworthy existing partitioning, choose a local join algorithm, contain skew and spill, and publish exact multiset results under retries, changing statistics, heterogeneous resources, and sensitive data?

### Essential definitions

- A **repartition join** routes rows from one or both inputs so rows that can match arrive at the same logical destination.
- A **partition contract** fixes key expressions, normalization, equality, null treatment, hash/range function and version, seed, partition count, and destination mapping.
- A **symmetric repartition** exchanges both inputs; a **one-sided repartition** exchanges only the input lacking a compatible reusable partitioning.
- A **co-partitioned join** consumes both inputs locally because their existing partition contracts and physical placement are compatible.
- A **shuffled hash join** builds a local hash table after repartitioning; a **shuffle sort-merge join** sorts compatible buckets and merges them.
- The **build side** is materialized into the local lookup structure; the **probe side** streams through it.
- A **hot key** contributes disproportionate input or output to one join bucket; **partition skew** can also arise from many keys, wide rows, or uneven placement.
- **salting** extends a hot key with a subpartition identifier, usually requiring controlled replication or an extra aggregation to preserve semantics.
- A **shuffle boundary** materializes attempt-scoped bucket contributions before downstream join tasks consume accepted winners.
- A **partitioning claim** is reusable only when proven by metadata and validation, not inferred from filenames, table labels, or equal partition counts.

### Central model, mechanism, or theorem

Let $L$ and $R$ be input multisets joined on equality key $k$. A total deterministic partition function $p(k)\in\{0,\ldots,P-1\}$ is compatible with join equality when every two matchable non-null keys route to the same partition. Route each row exactly once to its side's bucket, then evaluate the declared join independently for each bucket pair $(L_j,R_j)$. For an inner equijoin,

$$L\bowtie R=\biguplus_{j=0}^{P-1}(L_j\bowtie R_j),$$

provided routing, equality, multiplicity, accepted-attempt, and completeness premises hold. If key $x$ occurs $m_x$ times in $L$ and $n_x$ times in $R$, it contributes $m_xn_x$ output pairs; partitioning cannot erase this required multiplicity.

If serialized post-filter/project sizes are $B_L$ and $B_R$, a full symmetric exchange moves approximately $B_L+B_R$ logical payload bytes. If fractions $f_L$ and $f_R$ are already reusable without movement, payload becomes $(1-f_L)B_L+(1-f_R)B_R$, before replication, compression, protocol, spill, retry, and skew overhead. More partitions reduce average bucket size but increase tasks, connections, files, metadata, scheduling, and fixed buffers. The largest actual bucket, not the mean, governs tail and local build feasibility.

### Critical invariants

- Join predicate, key types, coercions, collation, normalization, equality, hash/range function, seed, null semantics, partition count, and version are pinned.
- Every accepted input row is routed exactly once to one logical bucket per required routing branch.
- Keys that can match under the predicate are co-located; hash collisions still use full equality and residual predicates.
- Both bucket streams use the same partition epoch and compatible snapshot/plan identity.
- Empty, complete, missing, corrupt, late, failed, and losing-attempt bucket states are distinguishable.
- Each local join preserves duplicate multiplicity and the unmatched-row ownership required by inner, outer, semi, or anti semantics.
- Build, probe, sort, spill, output, network, descriptor, task, and metadata resources are bounded per worker and across concurrent joins.
- Skew handling is semantics-preserving: salting, splitting, replication, and aggregation do not omit or duplicate logical pairs.
- Downstream effects remain attempt-scoped until one complete compatible join generation commits.
- Intermediate partitions obey tenant, region, encryption, retention, deletion, and audit policy.

### Common failures

Common failures include calling any join with a shuffle a “repartition join” without stating the partition contract; assuming equal partition counts imply compatibility; using process-randomized hashes; changing normalization or null rules across sides; repartitioning both sides when one is already valid; trusting stale bucketing metadata; selecting partition count from total bytes while ignoring the largest key; overwriting duplicate build rows; treating hash collision as equality; assuming more partitions split a single hot key; salting one side without matching replication; using a local hash table that cannot spill; publishing an empty bucket before all producers finish; accepting two speculative producers; retrying a join against a different partition epoch; claiming co-location when matching buckets live on different workers; and exposing sensitive join keys in shuffle paths or telemetry.

### Compact example

Suppose filtered inputs are 600 GiB and 250 GiB. Symmetric repartition moves about 850 GiB of logical payload. If trustworthy existing placement lets 35% of the left and 20% of the right remain local, the remaining logical payload is $0.65(600)+0.80(250)=590$ GiB. With 4,000 destinations, the mean is only about 212.5 MiB under full exchange, but a hot key with 90 GiB still lands in one ordinary hash bucket. Raising the count does not split that key.

### Connections

[LSDS-003](003-range-hash-and-consistent-partitioning.md) defines partition functions, [LSDS-023](023-partitioners-and-combiners.md) defines grouping contracts, [LSDS-027](027-task-retry-and-speculation.md) defines accepted attempts, and [LSDS-031](031-shuffle-architecture.md) through [LSDS-034](034-hash-based-shuffle.md) define exchange mechanics. [LSDS-035](035-broadcast-joins.md) provides the replicated-build alternative, while [LSDS-037](../ROADMAP.md) develops sort-merge execution after repartitioning.

## Governing Question

A distributed equijoin needs all rows capable of matching to meet. When neither relation is small enough to broadcast, a common answer is to repartition by the join key: every producer routes its left and right rows to compatible destinations, and each destination performs a local join. This spreads build state across the cluster rather than replicating a whole input on every worker.

The phrase hides two separate choices. Distribution decides where rows meet. The local algorithm decides what happens after they meet: build a hash table, sort and merge, use an index, or apply another operator. “Hash-partitioned” does not prove “hash join,” and “sort-merge join” can still require a hash-selected shuffle destination before local sorting.

Movement is not automatically symmetric. If both inputs already share a trustworthy partitioning and placement contract, no network exchange may be needed. If only one does, the other can be routed to it. If counts match but algorithms, seeds, key expressions, bucket transforms, or placements differ, both may require exchange. An optimizer must reason from physical properties, not names.

Correctness is relational and operational. Duplicate keys require Cartesian multiplicity. Outer joins require exactly-once unmatched-row ownership. Shuffle retries require one accepted producer contribution. A join task cannot silently combine left bucket generation 12 with right generation 13. Partial fetches, speculative attempts, skew splits, and fallback must retain identity.

The governing question is therefore how to establish a compatible, complete, bounded, and policy-compliant partition contract at the least total cost, then select a local join path that preserves semantics under actual bucket sizes rather than optimistic averages.

## Why This Matters

Repartition joins are the general large-input workhorse. Unlike broadcast, local build memory contains only one fraction of a build relation. Aggregate cluster memory can accommodate inputs far larger than any single node. Both sides can stream and spill through a durable exchange, isolating failures at stage boundaries.

The price is an all-to-all data movement. Producers serialize, buffer, spill, and publish contributions to many consumers. Consumers fetch from many producers, validate blocks, and materialize local state. Network bytes, disk passes, descriptors, metadata, and barrier latency can dominate the actual key comparison work.

Partition reuse can remove much of that cost, but false reuse corrupts results. Two tables described as “bucketed into 256 partitions” might use different hash versions, column order, null encoding, or bucket-to-worker assignment. Even identical logical buckets may still require network movement if matching buckets are not co-located at execution time.

Skew turns averages into dangerous fiction. One popular account ID can send billions of rows to one destination and produce trillions of required pairs. Increasing partition count helps many-key imbalance but not one indivisible equality group. Skew repair may split work and replicate the opposite side, which changes movement, attempt identity, and output reconciliation.

These joins also create broad intermediate copies. Join keys and payloads cross worker, disk, remote shuffle, and retry boundaries. Correct engineering accounts for access scope, region, encryption, deletion, and observability at the exchange, not only at source and sink.

## Prerequisites and Retrieval

Retrieve horizontal, range, hash, and consistent partitioning from [LSDS-002](002-horizontal-partitioning.md) and [LSDS-003](003-range-hash-and-consistent-partitioning.md). Retrieve locality, serialization, failure assumptions, and scale accounting from [LSDS-004](004-data-locality.md) through [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md).

Review distributed block integrity and metadata from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md), partitioner and equality contracts in [LSDS-023](023-partitioners-and-combiners.md), plan/attempt identity in [LSDS-025](025-lazy-evaluation-and-plan-construction.md) through [LSDS-030](030-tracing-a-batch-job-through-a-cluster-engine.md), and shuffle mechanics in [LSDS-031](031-shuffle-architecture.md) through [LSDS-035](035-broadcast-joins.md). You should understand relational multiset joins, null predicates, hashing, sorting, spill, checksums, backpressure, retries, snapshot identity, and output commit.

## Learning Objectives

After this module, you should be able to:

1. distinguish repartition distribution from shuffled hash, sort-merge, broadcast, and co-located local join algorithms;
2. specify a portable partition contract covering keys, normalization, equality, nulls, hash/range version, seed, count, and placement;
3. prove bucket-local inner-join correctness from co-location, completeness, multiplicity, and accepted-attempt premises;
4. estimate symmetric, one-sided, and partially reusable movement plus local build, sort, spill, and output pressure;
5. validate whether existing source bucketing is reusable rather than relying on labels or equal counts;
6. select partition count from bucket tails, concurrency, fixed overheads, and downstream reuse;
7. diagnose and mitigate many-key, hot-key, byte-width, output, placement, and adversarial skew;
8. preserve inner, outer, semi, and anti semantics across skew splits, retries, and adaptive plan changes;
9. validate exchanges and local joins with differential, property, boundary, and fault-injection tests; and
10. govern intermediate partitions through minimization, isolation, encryption, retention, deletion, and audit.

## Core Exposition

### Start from relational semantics

Define the join before choosing transport. For an inner equijoin, every pair satisfying the key and residual predicate appears with multiset multiplicity. If key $x$ occurs $m_x$ times on the left and $n_x$ times on the right, it can contribute $m_xn_x$ pairs. A local hash map that overwrites duplicate rows is incorrect.

Left outer join adds one null-extended right row for each unmatched left row. Left semi emits a qualifying left row once, even if many right matches exist. Left anti emits it only when no right row satisfies the full predicate. Full outer owns unmatched rows on both sides.

Ordinary SQL equality does not match null with null; null-safe equality does. Types, coercion, collation, Unicode normalization, decimal scale, timestamps, NaNs, and residual predicates affect matchability. The partition function may place nulls anywhere, but the local operator must apply the declared semantics.

### Define one compatible partition contract

Let $p(k)=normalizeDestination(h(normalizeKey(k),seed),P)$. Pin key expressions and order, schemas/types, normalization, equality, hash algorithm/version, seed, signed arithmetic, null encoding, destination count $P$, and partition epoch. Both inputs must implement the same contract for the join keys.

Compatibility requires only that matchable keys co-locate, not that different keys separate. Hash collisions are normal; local equality rejects false matches. Composite keys must serialize boundaries unambiguously. Concatenating strings without lengths can make `(ab,c)` collide semantically with `(a,bc)` before hashing.

Range partitioning can also co-locate matches when both sides share exact boundaries, comparison, collation, and null placement. A hash-selected destination is more common because equality needs co-location rather than order. Do not inherit a language runtime's randomized object hash as persisted exchange behavior.

### Symmetric repartition

When neither input exposes reusable partitioning, route both through exchanges using the common contract. Every left producer emits $L_{i,j}$ for destination $j$; every right producer emits $R_{q,j}$. Join task $j$ reads one accepted contribution from every relevant producer on each side.

Logical payload movement is approximately $B_L+B_R$ after pushed filters and projections. Physical cost includes serialization, compression, encryption, checksums, indexes, local spill, remote writes, fetch, decompression, retries, and possibly replication. Count producer and consumer disk passes separately from network.

Symmetry concerns movement, not local roles. After exchange, a shuffled hash join can build the smaller local side and probe the other. A sort-merge join can sort both buckets. Outer-join semantics can constrain build/probe logic without changing the requirement that matchable rows meet.

### One-sided repartition

If the left input already satisfies the target partition contract and its buckets can be placed with matching join tasks, route only the right. This can halve movement. The target $P$ and hash/range semantics come from the reusable left property unless the cost of retaining them exceeds a fresh symmetric layout.

Logical compatibility is not physical locality. If left bucket 17 is stored on node A but join task 17 runs on node B, the left data still moves. Storage replicas may permit locality-aware scheduling; otherwise the optimizer should call the property partition-compatible but not co-located.

One-sided reuse may create poor parallelism. A table bucketed into eight partitions cannot keep 1,000 workers busy without splitting buckets, and arbitrary splitting can require corresponding replication or subpartitioning of the other side. Compare avoided bytes with tail and occupancy.

### Co-partitioned and storage-partitioned joins

When both sources expose the same trustworthy contract and corresponding buckets can be processed together, join locally without an exchange. This is powerful for recurring fact-to-fact joins or shared dimensional layouts.

Proof requires authoritative metadata: table snapshots, partition transform/version, key columns/order, count, hash seed and implementation, boundary set, null rules, schema evolution, bucket completeness, and physical placement/replicas. Validate that all buckets exist or have explicit empty evidence.

Maintenance can invalidate reuse. Rewrites, compaction, rebucketing, connector upgrades, or mixed writer versions may leave partitions whose labels agree but semantics differ. Version partition properties and reject ambiguous mixtures. A corrective exchange is cheaper than silent wrong results.

### Push reduction below exchange

Apply semantics-preserving filters and required-column projection before repartition. Moving unused payload wastes network and disk. Derive normalized join keys once when safe to avoid repeated expensive expressions, but retain source columns needed for residual predicates or output.

Preaggregation or deduplication is legal only under query algebra. Semi join may require only existence; an inner join generally preserves right multiplicity. A uniqueness constraint can enable reduction if it is enforced for the exact snapshot. Approximate distinct estimates cannot authorize row removal.

Bloom or runtime filters can reduce probe-side work and perhaps exchange bytes when applied safely. They are membership approximations: false positives retain extra rows, false negatives are forbidden. Their generation and application snapshot must be compatible with the join.

### Choose partition count from constraints

For total shuffled bytes $B$ and $P$ destinations, $B/P$ is only the mean. Select an initial count from target bucket bytes, available parallelism, build/sort memory, expected skew, storage throughput, and downstream partition requirements. Leave room for adaptive coalescing or splitting if supported.

Too few partitions make large local builds, long sorts, deep spills, and idle workers. Too many create tiny tasks, $M\times P$ logical producer blocks, connection churn, metadata, scheduler load, small I/O, fixed buffer multiplication, and slow barrier coordination.

Count active tasks per worker. A 512 MiB safe build bucket is unsafe if four concurrent tasks each allocate one plus probe and output buffers. Heterogeneous workers require admission against the smallest eligible resource class or explicit placement.

### Cost movement and reuse honestly

With reusable fractions $f_L$ and $f_R$, logical payload movement is approximately $(1-f_L)B_L+(1-f_R)B_R$. Fractions must mean bytes that remain on their processing worker under the exact target contract, not merely bytes already grouped somewhere.

Add write/read amplification, replication, compression ratios, remote versus local paths, retry rates, and the cost of repartitioning an otherwise reusable downstream output. An exchange may be worthwhile if its result feeds several joins or aggregations, but reuse needs immutable snapshot and lineage identity.

Compare with broadcast using aggregate memory and transport, and with sort-merge using order/spill benefits. Cost models should retain uncertainty intervals for stale sizes, selectivity, width, distinctness, and skew rather than producing one falsely precise score.

### Build a shuffled hash join

After both bucket streams arrive, select the smaller feasible side as local build. Construct a duplicate-preserving hash table using the same normalized equality contract. Probe the other side and apply full key equality plus residual predicates after hash lookup.

Local build size is distribution-dependent. A globally smaller relation can have a larger bucket for one destination. Plan from per-bucket statistics when available and measure actual bytes before unsafe allocation. Hybrid hash join can recursively partition/spill build and matching probe rows when memory is exceeded.

Spill is not free. It adds serialization, disk capacity, partition fan-out, file handles, later reads, and recursive-skew risk. A single giant key may remain indivisible. Bound recursion and provide a giant-partition path or explicit failure rather than looping.

### Use sort-merge after repartition

A repartition sort-merge join sorts each left and right destination by compatible key order, then advances through equal-key runs. It handles inputs larger than memory through external runs and sequential merge I/O. Existing order can reduce work.

Sort-merge still preserves duplicate Cartesian products: equal runs of sizes $m$ and $n$ produce $mn$ pairs. Buffer or rescan strategies for large runs must bound memory and I/O. Residual predicates are evaluated per candidate pair.

Ordering costs comparisons and spill passes but avoids one large in-memory hash table. It may support full outer semantics naturally by emitting unmatched runs from either side. [LSDS-037](../ROADMAP.md) treats its detailed mechanics.

### Skew has several dimensions

Key-count skew means one destination receives more records. Byte skew can occur with equal counts but variable-width rows. Build skew threatens memory; probe skew threatens CPU. Output skew arises from $m_xn_x$ even when both inputs are small. Placement skew arises when many heavy buckets share a worker.

Measure per-destination rows and encoded/expanded bytes on both sides, distinct keys, largest groups, expected pairs, spill, fetch sources, CPU, output, and task duration. Report median, upper quantiles, maximum, and ratios; means hide tails.

Adversarial keys may target weak hashes. Use a stable keyed hash when threat models require resistance, while pinning its version and protecting the seed. Strong hashing spreads distinct keys; it cannot split repeated occurrences of one equality key.

### Split hot keys without changing semantics

For a hot inner-join key, salt one side's rows across $S$ subpartitions and replicate the opposite key group to all $S$, so every required pair appears in exactly one salted task. Which side to replicate depends on group sizes, output, and memory. Replicating both sides arbitrarily loses pairs; salting both with the same row-derived salt also loses cross-salt pairs.

An alternative splits one probe group while each split reads the complete build group. For semi/anti joins, existence can sometimes avoid full multiplicity, but unmatched decisions still require complete evidence. Outer joins require unique ownership of unmatched replicated rows; a designated salt or reconciliation stage can emit once.

Heavy-key detection must use the exact snapshot or conservative runtime evidence. False-negative detection leaves skew; false positives add replication. Skew plans carry key/salt/version identity and must be fenced across retry.

### Handle nulls and non-equijoins explicitly

Under ordinary equality, null-key rows never match. They need not share a bucket for inner join, though deterministic routing simplifies accounting. For outer/anti joins they must be emitted as unmatched according to preserved-side semantics. Null-safe equality requires all nulls to meet and can create a severe hot bucket.

Pure range or inequality predicates do not reduce to one hash destination. Interval joins may need range overlap replication, indexes, sweep algorithms, or nested loops. A residual inequality attached to an equijoin is evaluated after co-location on the equality key.

Do not force a `SHUFFLE_HASH` hint onto a non-equijoin. Current Spark and Flink documentation both characterize hints as strategy guidance with applicability constraints, not a replacement for predicate analysis.

### Exchange materialization and completeness

Each producer attempt writes immutable, destination-labeled contributions with exchange/side/partition/attempt identity, byte and record counts, checksum, codec/encryption, and segment index. A manifest distinguishes explicit empty from missing. Only the accepted attempt becomes visible.

Join task $j$ starts only when it can prove complete compatible left and right bucket manifests, or it follows a streaming protocol with equivalent fencing and replay guarantees. Fetch validates lengths, checksums, identity, and authorization before decode.

Remote shuffle services can outlive executors and reduce recomputation, but expand trust, storage, and cleanup surfaces. Local shuffle improves locality but worker loss may require producer replay. Choose through failure-domain and cost evidence.

### Retry, speculation, and adaptive changes

A failed producer may create multiple physical attempts; consumers read one accepted winner. A failed join task may replay local computation and output under a new attempt without changing the partition epoch. Speculative join attempts cannot both commit.

If adaptive execution coalesces adjacent partitions, it must preserve complete bucket sets and avoid merging incompatible contracts. Splitting a skewed bucket creates explicit subpartition ownership and any required replication. Changing $P$, hash seed, normalization, or skew map creates a new exchange generation.

Never let some tasks consume old left buckets and new right buckets. Plan fallback occurs before irreversible output, or downstream effects use transactional attempt commit. Cancellation fences late transfers and deletes only artifacts no accepted/recoverable consumer still references.

### Observability

Record estimated and actual rows/bytes/distinctness/width per side before and after filters, chosen contract and version, reusable property evidence, partition count, local versus remote fractions, plan reason/confidence, and alternative costs.

At exchange, measure producer blocks, active destinations, bytes by side/destination/path, compression, spill, files/segments, descriptors, network connections, fetch retries, corruption, locality, barrier time, and accepted/losing attempts. At join, measure build/probe bytes, expanded memory, sort runs, spill passes, hash collisions, duplicate groups, output pairs, unmatched rows, backpressure, and per-task duration.

Correlate metrics by query, plan, exchange, side, partition, attempt, worker, and snapshot without putting raw sensitive keys in labels. Keep estimate-versus-actual error so planners improve rather than merely explaining the last incident.

### Validation and fault injection

Differentially compare every supported join type with a trusted single-node implementation. Test empty inputs, one-sided empty, unique keys, duplicates on either/both sides, many-to-many keys, null and null-safe equality, collisions, composite keys, coercion, Unicode/collation, NaNs, residual predicates, and outer/semi/anti unmatched ownership.

Property tests verify every input row routes once, matchable keys co-locate, local bucket unions equal the global join multiset, losing attempts contribute nothing, and output is independent of producer completion order. Vary partition counts including one and greater than row count.

Inject skew, giant rows, disk full, short write, corrupt/missing/duplicated blocks, fetch timeout, network partition, worker/shuffle-service loss, stale partition metadata, mixed hash versions, cancellation, retry, speculation, adaptive coalescing/splitting, fallback, auth expiry, and cleanup races. Assert bounded memory/disk/network and no partial or mixed-generation commit.

### Security, privacy, and governance

Minimize fields before exchange. Every shuffle worker, remote service, disk, cache, replica, operator, and administrator touching a bucket must be authorized for its classification, tenant, region, and purpose. Co-location optimization cannot cross forbidden boundaries.

Use workload identity, scoped expiring credentials, encrypted transport and storage, tenant/attempt namespaces, integrity checks, and auditable fetch/publication. Protect keys, counts, digests, skew summaries, plans, errors, filenames, and traces; hashed keys may remain identifying.

Define retention from query/retry/recovery needs, then erase accepted and losing artifacts, spill, caches, replicas, logs, and encryption keys when leases and holds end. Verify deletion and access denial. Bring data owners, platform, security, privacy/legal/records, regional authorities, and affected tenants into high-risk design review.

## Definitions and Notation

- $L,R$: left and right input multisets after semantics-preserving filter/projection.
- $B_L,B_R$: serialized logical payload bytes considered for exchange.
- $P$: logical join destination count.
- $p(k)$: pinned partition function for normalized key $k$.
- $L_j,R_j$: complete accepted input buckets for destination $j$.
- $m_x,n_x$: multiplicities of key $x$ in left and right inputs.
- $f_L,f_R$: byte fractions reusable in place under the exact target contract.
- $S$: number of explicitly owned subpartitions for a skewed key/bucket.
- **partition epoch**: immutable identity of contract, plan, snapshots, skew map, and accepted bucket set.
- **local join**: the hash, sort-merge, index, or other operator executed after compatible rows meet.

## Mechanisms, Invariants, or Proof Structure

1. Freeze join type, equality/residual predicate, key types, coercion, nulls, collation, and multiplicity.
2. Discover source physical properties and validate exact contract, snapshot, completeness, and placement evidence.
3. Choose symmetric, one-sided, co-located, broadcast, or another distribution from bounded cost and legality.
4. Pin key normalization, hash/range algorithm/version/seed, count, skew map, side, and partition epoch.
5. Push safe filters/projection and estimate rows, bytes, widths, distinctness, group sizes, output, and uncertainty.
6. Select partition count, local algorithm, memory/disk/network admission, spill, and giant/skew paths.
7. Produce immutable side/destination/attempt blocks; validate and publish exactly one accepted contribution.
8. Prove both bucket manifests complete and compatible before local join or use equivalently fenced streaming.
9. Preserve duplicates, equality/residual checks, null behavior, and unmatched-row ownership locally.
10. Commit one join attempt, retain recovery evidence, measure estimates versus actuals, and delete after references/holds end.

For inner join, take any required output pair $(l,r)$. Its keys match, so compatibility gives $p(k_l)=p(k_r)=j$; exact routing places both in $L_j,R_j$, where correct local join emits the pair. Conversely every locally emitted pair passes full predicate, so it belongs to the global join. Disjoint row routing plus accepted-attempt fencing prevents a logical input pair from appearing through two ordinary buckets. Multiset union retains duplicate pair counts.

Outer, semi, and anti proofs add ownership. A task may declare a preserved row unmatched only after its complete opposite bucket is known and the full predicate finds no match. If skew replication creates several candidate tasks, exactly one designated owner emits the unmatched result or a reconciliation stage deduplicates by stable row identity under a proven rule.

The movement equation is accounting, not correctness. It excludes protocol and physical amplification. The mean bucket is also not a bound: a valid partition can contain all bytes. Safety requires measured maxima, enforced resource limits, spill/fallback, and explicit treatment of indivisible groups.

## Alternatives and Trade-Offs

**Symmetric repartition** is general and balances both sides under one fresh contract, but moves nearly all payload and creates two exchanges. **One-sided repartition** saves movement when one side's contract and placement are reusable, but can inherit poor partition count or skew.

**Co-partitioned join** minimizes exchange and can exploit storage locality. It demands strong metadata, compatible snapshots/transforms, and sufficient parallelism. Maintaining shared physical layouts has ingestion and compaction cost.

**Shuffled hash join** avoids sorting and is fast when each build bucket fits or a robust hybrid spill path exists. It is sensitive to build skew, expansion, collision behavior, and random spill. **Repartition sort-merge** adds comparison and run I/O but offers bounded external-memory behavior and useful ordering.

**Broadcast join** avoids moving the large side and is excellent for a genuinely small authorized build. It multiplies build memory/copies and fails for large builds. **Index/connector pushdown** can avoid engine exchange when a trusted source supports the predicate and capacity, but changes failure, consistency, and observability boundaries.

**More partitions** lower ordinary average bucket size and expose parallelism, while raising fixed overhead, tiny I/O, task/metadata count, and connection pressure. **Fewer partitions** improve sequential efficiency but increase tails and memory.

**Salting/skew splitting** reduces one task's load at the cost of opposite-side replication, extra planning, potential reconciliation, and harder outer semantics. **Preaggregation/filtering** can reduce movement dramatically when algebraically legal; approximate statistics never justify semantic loss.

## Failure Modes and Misconceptions

1. **“Both tables have 256 buckets, so the join is local.”** Count alone says nothing about keys, hash version, seed, boundaries, snapshot, or placement.
2. **“Repartition join means hash join.”** Repartition describes distribution; local execution can hash, sort-merge, or use another operator.
3. **“Every repartition join shuffles both sides.”** Valid one-sided or co-partitioned reuse can avoid one or both exchanges.
4. **“Hashing evenly solves skew.”** It can spread distinct keys but cannot split one repeated equality key.
5. **“Average partition size proves memory safety.”** The maximum bucket and concurrent tasks control local admission.
6. **“More partitions always help.”** Tasks, blocks, files, buffers, scheduling, and metadata can dominate.
7. **“A hash match is a join match.”** Full equality and residual predicates must still be evaluated.
8. **“One row per key is enough in the build table.”** Inner duplicates require $m_xn_x$ outputs.
9. **“Salt both sides by row number.”** Independent salts omit cross-salt pairs; a correct plan replicates or reconciles explicitly.
10. **“Full outer is just inner plus nulls.”** Exactly-once unmatched ownership is a global completeness problem under replication/splitting.
11. **“An empty file and a missing block are equivalent.”** Missing may mean failed/incomplete production; emptiness needs accepted evidence.
12. **“Speculation only changes speed.”** Two accepted producer or join attempts duplicate data.
13. **“Existing bucket labels are trustworthy forever.”** Writer upgrades, compaction, or partial rewrites can mix contracts.
14. **“Spill guarantees any hash join finishes.”** Giant groups, recursive skew, disk limits, and file fan-out still need bounds.
15. **“Nulls can use host-language map equality.”** SQL ordinary and null-safe predicates require explicit semantics.
16. **“Retries can read whichever generation is available.”** Mixed snapshots or partition epochs produce inconsistent output.
17. **“Shuffle encryption completes governance.”** Authorization, locality, minimization, telemetry, retention, and verified deletion remain.

## Worked Examples

### Example 1

Two unpartitioned relations of 600 GiB and 250 GiB require about 850 GiB of logical payload under symmetric repartition. Compression can lower network bytes while spill adds disk I/O; neither changes the logical accounting baseline.

### Example 2

The same relations have 35% and 20% respectively already reusable on the final processing workers. Remaining movement is $0.65(600)+0.80(250)=590$ GiB, saving 260 GiB before physical overhead.

### Example 3

Both sources report 128 buckets, but one uses MurmurHash with seed 7 over `(tenant,id)` and the other uses a connector-specific hash over `(id,tenant)`. Equal counts do not co-locate matchable composite keys; a corrective exchange is required.

### Example 4

An 800 GiB total exchange over 4,000 destinations averages about 204.8 MiB per bucket. One 90 GiB hot key still creates a destination at least 90 GiB before other rows. Doubling $P$ barely affects that key.

### Example 5

A key occurs 2,000 times left and 50,000 times right. The inner result contains 100 million pairs. Input buckets can look modest while output buffers, CPU, and sink capacity become the bottleneck.

### Example 6

A one-sided join reuses a table's 16 storage buckets on a 400-worker cluster. It avoids 2 TiB of exchange but exposes at most 16 ordinary join tasks. Repartitioning or compatible subpartition splitting may win on elapsed time despite extra bytes.

### Example 7

A hot left group has one million rows and its right group has 20 rows. Split left into 100 salts and replicate the 20 right rows to each. Every pair appears once, adding only 2,000 replicated right rows instead of leaving one massive task.

### Example 8

For left outer join with skew-split left rows, each left row belongs to one salt and can emit unmatched locally after receiving the complete replicated right group. If the preserved row itself is replicated instead, unmatched emission needs a designated owner.

### Example 9

One local shuffled-hash task receives a 9 GiB encoded build bucket that expands to 22 GiB, above its 12 GiB budget. A hybrid path spills subpartitions and their probes, or the engine switches to sort-merge before committed output; average-size estimates cannot authorize allocation.

### Example 10

The following fixture uses a defined byte-sum partitioner, preserves duplicate multiplicity, treats null as nonmatching under ordinary equality, and compares full symmetric with partially reusable logical movement.

<!-- bijux-verify: {"id":"repartition-join-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"partitions=4 inner_rows=4 left_outer_rows=6\nleft_counts=(1, 2, 1, 0) right_counts=(1, 2, 0, 1)\nfull_shuffle_gib=850 reusable_shuffle_gib=590\n","stderr":""}} -->
```python
from collections import defaultdict

left = [("a", "L1"), ("a", "L2"), ("b", "L3"), (None, "L4")]
right = [("a", "R1"), ("a", "R2"), ("c", "R3"), (None, "R4")]
partition_count = 4


def destination(key):
    if key is None:
        return 0
    return sum(key.encode("utf-8")) % partition_count


def repartition(rows):
    buckets = defaultdict(list)
    for row in rows:
        buckets[destination(row[0])].append(row)
    return buckets


left_buckets = repartition(left)
right_buckets = repartition(right)
inner = []
left_outer = []

for bucket_id in range(partition_count):
    build = defaultdict(list)
    for key, value in right_buckets[bucket_id]:
        if key is not None:
            build[key].append(value)
    for key, left_value in left_buckets[bucket_id]:
        matches = [] if key is None else build.get(key, [])
        inner.extend((key, left_value, value) for value in matches)
        if matches:
            left_outer.extend((key, left_value, value) for value in matches)
        else:
            left_outer.append((key, left_value, None))

left_counts = tuple(len(left_buckets[i]) for i in range(partition_count))
right_counts = tuple(len(right_buckets[i]) for i in range(partition_count))
full_shuffle_gib = 600 + 250
reusable_shuffle_gib = round(600 * 0.65 + 250 * 0.80)

print(f"partitions={partition_count} inner_rows={len(inner)} left_outer_rows={len(left_outer)}")
print(f"left_counts={left_counts} right_counts={right_counts}")
print(f"full_shuffle_gib={full_shuffle_gib} reusable_shuffle_gib={reusable_shuffle_gib}")
```

The deterministic toy hash is deliberately not a production recommendation. The example checks routing compatibility, multiplicity, null behavior, and arithmetic, not hash quality, spill, concurrency, or network performance.

## Cross-Program Connections

- **Data Structures Engineering:** Hash tables, collision resolution, external sorting, buffers, bloom filters, and immutable manifests determine local join mechanics.
- **Algorithms Engineering:** Partition correctness, multiset algebra, skew splitting, heavy-hitter detection, and cost models connect proof with performance.
- **Database Systems Engineering:** Join order, physical properties, histograms, null semantics, outer joins, and adaptive execution drive optimizer choice.
- **Distributed Systems Engineering:** Attempt fencing, checksummed exchanges, leases, replay, consensus-backed metadata, and failure domains govern materialization.
- **Data Engineering:** Bucketing, clustering, compaction, schema evolution, and recurring pipelines determine whether physical layouts are reusable.
- **Platform Engineering:** Scheduler placement, network topology, remote shuffle, disk quotas, credentials, observability, and multi-tenant admission shape capacity.
- **Security Engineering:** Repartition expands intermediate exposure and demands authorization, isolation, encryption, minimization, and verifiable deletion.
- **Systems Engineering:** A local optimization changes network, storage, memory, scheduler, recovery, governance, and downstream behavior as one coupled system.

## References

1. Apache Spark, [Performance Tuning: Adaptive Query Execution and Skew Joins](https://spark.apache.org/docs/latest/sql-performance-tuning.html), accessed 2026-09-03.
2. Apache Spark, [SQL Hints: Repartition and Join Strategies](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-hints.html), accessed 2026-09-03.
3. Apache Spark, [Configuration: Shuffle Partitions and Shuffled Hash Join](https://spark.apache.org/docs/latest/configuration.html), accessed 2026-09-03.
4. Apache Spark, [RDD Programming Guide: Shuffle Operations](https://spark.apache.org/docs/latest/rdd-programming-guide.html), accessed 2026-09-03.
5. Apache Spark, [PySpark DataFrame.repartition](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.repartition.html), accessed 2026-09-03.
6. Apache Flink, [SQL Join Hints](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/sql/queries/hints/), accessed 2026-09-03.
7. Apache Flink, [JoinOperatorBase.JoinHint API](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/api/common/operators/base/JoinOperatorBase.JoinHint.html), accessed 2026-09-03.
8. Apache Flink, [Table Configuration](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/config/), accessed 2026-09-03.
9. Apache Flink, [Deployment Configuration: Hash Join Spill](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/config/), accessed 2026-09-03.
10. Trino, [Cost-Based Optimizations: Join Distribution](https://trino.io/docs/current/optimizer/cost-based-optimizations.html), accessed 2026-09-03.
11. Trino, [General Properties: Partitioned Joins](https://trino.io/docs/current/admin/properties-general.html), accessed 2026-09-03.
12. Trino, [Optimizer Properties: Co-located Joins](https://trino.io/docs/current/admin/properties-optimizer.html), accessed 2026-09-03.

## Exercises

### Exercise 1

Two filtered inputs are 1.2 TiB and 0.5 TiB. Under a candidate contract, 25% of the left bytes and 60% of the right bytes are provably reusable on their final processing workers. Compute symmetric logical movement and movement with reuse. State major excluded physical costs.

### Exercise 2

Prove bucket-local inner equijoin correctness for duplicate-bearing multisets. State the partition, routing, completeness, local-predicate, and attempt premises explicitly.

### Exercise 3

A hot key occurs 900,000 times on the left and 30 times on the right. Design a 60-way skew split, compute required right-row replication and logical output pairs, and explain why independently salting both sides is wrong.

### Exercise 4

Design an audit that decides whether two supposedly 512-bucket tables can use a co-partitioned join after years of compaction and writer upgrades.

### Exercise 5

Design runtime admission, fallback, validation, and governance for a repartition join whose mean bucket is 300 MiB, largest estimated bucket is 5 GiB, local build budget is 4 GiB, and inputs contain regulated tenant keys.

## Answers to the Exercises

### Answer 1

Full symmetric movement is $1.2+0.5=1.7$ TiB. Reuse movement is $0.75(1.2)+0.40(0.5)=0.9+0.2=1.1$ TiB, a 0.6 TiB logical saving. The formula excludes serialization/encoding changes, compression, encryption, checksums, headers/indexes, source read, producer spill writes, remote replication, consumer reads, retries, skew replication, local movement, and output. The reuse fractions require exact contract and final-worker locality evidence; mere pre-bucketing does not count.

### Answer 2

Pin a total deterministic $p$ compatible with equality, and route each accepted row exactly once to its side's one bucket. Require complete manifests for both sides at one snapshot/partition epoch and exactly one accepted contribution per producer. For any global matching pair $(l,r)$, equality compatibility gives a common destination $j$, so complete exact routing places both in $(L_j,R_j)$ and a correct local operator evaluating full equality/residual predicate emits it. Conversely, anything emitted locally satisfies the global predicate. Disjoint ordinary routing and attempt fencing prevent cross-bucket/attempt duplication. Multiset local operators retain $m_xn_x$ pairs, so union over buckets preserves duplicates.

### Answer 3

Assign every left occurrence to exactly one of 60 salts and replicate all 30 right rows to each salt. This creates $60\times30=1{,}800$ routed right rows, while each task receives about 15,000 left rows plus 30 right rows. Logical inner output remains $900{,}000\times30=27{,}000{,}000$ pairs. If left and right rows choose salts independently, only same-salt combinations meet and roughly 59/60 of required cross-salt pairs disappear. Replication of one complete group, or an equivalent coverage construction, is necessary.

### Answer 4

Read authoritative metadata for exact snapshots, join columns/order/types, normalization, equality/collation/null rules, partition transform, hash/range algorithm and version, seed, count, bucket mapping, writer version, and physical locations/replicas. Inventory every data file and compaction lineage; detect mixed writers, partial rewrites, schema evolution, missing/duplicate buckets, and stale statistics. Sample/recompute destinations and use controlled canary/differential joins, including nulls, composite/boundary keys, duplicates, and collisions. Verify matching buckets can be scheduled together and policy permits it. If any contract or completeness fact is ambiguous, perform a corrective exchange rather than claiming reuse.

### Answer 5

Do not admit from the 300 MiB mean. Materialize/measure per-destination encoded and expanded build/probe bytes, group sizes, predicted output, concurrent tasks, sort/hash workspace, spill disk, descriptors, network, and worker heterogeneity. A 5 GiB estimate already exceeds the 4 GiB local build budget before expansion, so choose a spill-capable hybrid or sort-merge plan, split the bucket with a proved coverage/ownership rule, increase eligible resources, or fail before effects. Validate complete accepted bucket manifests, predicate/multiplicity, skew plan, checksums, retry/fallback generations, and differential output. Minimize regulated fields; constrain tenant/region placement; use scoped identity, encryption, redacted telemetry, audit, attempt namespaces, retention/holds, and verified deletion across shuffle, spill, cache, replicas, losing attempts, and keys.
