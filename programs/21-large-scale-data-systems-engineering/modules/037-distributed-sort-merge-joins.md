---
module_id: LSDS-037
program: Large-Scale Data Systems Engineering
level: 1
module_number: 37
title: Distributed Sort-Merge Joins
status: complete
last_verified: 2026-09-03
---

# Distributed Sort-Merge Joins

## One-Page Review

### Governing question

How can a distributed engine repartition, externally sort, and merge two large join inputs with compatible comparison semantics, bounded memory and disk, exact duplicate and outer-join behavior, safe retries, and evidence that existing partitioning or ordering is genuinely reusable?

### Essential definitions

- A **distributed sort-merge join** co-locates matchable keys, orders each local input by a compatible join comparator, then advances through the two ordered streams.
- A **sort key contract** fixes expressions, types, coercion, normalization, collation, comparator, ascending/descending direction, null placement, NaN behavior, and version.
- A **run** is an immutable sorted sequence produced when an in-memory sort buffer spills.
- A **merge fan-in** is the maximum number of runs merged in one pass under memory and file-descriptor limits.
- An **equal-key group** is the contiguous run of rows equivalent under join equality after sorting.
- A **group cross product** emits all $mn$ pairs for left and right group sizes $m$ and $n$ in an inner join.
- A **streaming merge** compares current keys, advances the smaller key, and processes equal groups without building a whole-partition hash table.
- A **materialized merge pass** reads sorted runs and writes fewer larger runs; a final merge may feed the join directly.
- **order reuse** avoids sorting only when authoritative ordering covers the needed key prefix under the exact comparator and partition contract.
- A **tie-break order** orders rows equal on the join key for reproducibility; it is not required for relational equality correctness unless exposed as a contract.

### Central model, mechanism, or theorem

For each logical partition $j$, let $L_j$ and $R_j$ be complete input multisets sorted by compatible comparator $\preceq$. When current keys differ, advancing the smaller stream cannot skip a match because all later keys on the other stream are no smaller. When keys are equal, collect or otherwise replay their groups and emit the join-specific result. For inner join, groups of sizes $m_x$ and $n_x$ contribute $m_xn_x$ pairs. Union across compatible partitions equals the global multiset join.

For one side with $B$ bytes and usable sort memory $M$, an idealized initial-run count is $r=\lceil B/M\rceil$. With fan-in $F>1$, fully materializing until one run needs about $q=\lceil\log_F r\rceil$ merge rounds. If initial source read/run write, all $q$ merge read/write rounds, and a final join read are counted, the simple upper accounting is $2B(1+q)$ bytes. A fused final merge, compression, uneven runs, replacement selection, and partial order change this amount. Descriptor and buffer budgets constrain $F$; the formula is not a performance guarantee.

### Critical invariants

- Join equality, residual predicate, key types, comparator, collation, null/NaN semantics, direction, and version are pinned on both sides.
- Matchable rows are co-located under one complete partition epoch before local merge.
- Every sorted run is internally ordered, immutable, checksummed, attempt-scoped, and complete for its declared input range.
- Merge output is a sorted multiset union of its input runs: no row is omitted, duplicated, or mutated.
- Equal join keys are contiguous under a comparator consistent with join equality.
- Duplicate groups emit exact Cartesian multiplicity; semi/anti joins and outer unmatched rows follow declared ownership.
- Sort buffers, run writers/readers, fan-in, descriptors, disk, group buffers, output buffers, and concurrent tasks are admitted and bounded.
- A giant row or group has an explicit streaming/spooling path or fails without partial commit.
- Only accepted producer/sort/join attempts contribute; mixed snapshots, comparators, partitions, or generations cannot commit.
- Intermediate runs and output obey authorization, isolation, encryption, retention, deletion, and audit policy.

### Common failures

Common failures include assuming repartition also sorts; merging streams whose collations, null placement, direction, or type coercion differ; trusting file order without authoritative metadata; using a comparator inconsistent with equality; buffering an unbounded duplicate group; emitting one pair instead of $mn$; treating stable equal-key order as automatic; counting only sort memory and ignoring merge buffers or concurrent tasks; choosing fan-in above descriptor limits; losing rows during partial final run flush; treating missing runs as empty; accepting speculative duplicates; reusing sorted data after schema/collation evolution; splitting a hot key across tasks without coverage; emitting outer unmatched rows before the opposite stream is complete; and exposing sensitive keys in run names, samples, or skew metrics.

### Compact example

A 960 MiB partition sorted with 120 MiB usable memory creates at least eight idealized initial runs. Fan-in four needs two fully materialized merge rounds. The deliberately conservative accounting $2B(1+q)$ gives $2(960)(3)=5{,}760$ MiB of local source/run/final-read traffic. Fusing the last merge into the join can avoid its output write and later read. If an equal key has 2,000 left rows and 30,000 right rows, it still produces 60 million inner pairs regardless of sort efficiency.

### Connections

[LSDS-023](023-partitioners-and-combiners.md) defines equality/grouping contracts, [LSDS-027](027-task-retry-and-speculation.md) defines attempt fencing, and [LSDS-031](031-shuffle-architecture.md) through [LSDS-033](033-sort-based-shuffle.md) define exchange and external-sort runs. [LSDS-036](036-repartition-joins.md) proves co-location; [LSDS-039](../ROADMAP.md) develops heavy-hitter control.

## Governing Question

When two join inputs are too large for a replicated build and local hash tables are risky, sorting offers a bounded external-memory path. Route matchable keys to the same destination, sort each side of each destination, and merge the ordered streams. The merge scan uses sequential access and needs only current records plus equal-key group state—until duplicates make that group state large.

The name contains three separate contracts. “Distributed” defines partitions, placement, and attempt completeness. “Sort” defines a comparator, runs, spill, and order evidence. “Merge join” defines the relational scan across equal and unequal key groups. A valid plan must make all three compatible.

Existing order can be extremely valuable. Bucketed tables sorted by the join keys may avoid both exchange and local sort. Yet “sorted by customer” is too weak: collation, null ordering, type coercion, key prefix, direction, writer version, within-file guarantees, and cross-file range metadata matter. Concatenating individually sorted files is not globally sorted unless their ranges are monotone.

External sorting bounds ordinary memory by spilling runs, but it shifts risk to disk, file descriptors, merge passes, checksums, and cleanup. Equal-key groups can still exceed memory, and required output can dwarf both inputs. A robust design spools or rescans groups, applies backpressure, and reports output explosion rather than silently truncating.

The governing question is when the order and spill properties outweigh hash construction, how to prove the ordering contract, and how to keep the complete distributed operation correct through skew, failures, retries, and policy constraints.

## Why This Matters

Sort-merge joins handle relations much larger than memory with predictable sequential I/O. External runs allow progress under a fixed memory budget. Sorted streams support inner and outer joins without retaining an entire input partition, and an ordered result may benefit later aggregation, windowing, deduplication, or another merge.

That durability has cost. Each side may write initial runs, perform several read/write merge passes, and read again for the join. CPU pays comparison, decoding, normalization, and possibly compression. Slow disks, limited ephemeral storage, or excessive run count can dominate the network exchange.

Comparator errors are correctness errors. One side sorting accented strings under a locale-aware collation and the other using binary UTF-8 can make the two-pointer scan advance past valid matches. A comparator that returns equality for keys the join predicate considers unequal can still work if full equality is checked within a group, but it can enlarge candidate work; the reverse—separating join-equal keys—is fatal.

Duplicates are the algorithm's sharp edge. A million-by-million equal-key pair implies a trillion outputs. The inputs may sort easily while the group cross product overwhelms buffers, disk, sinks, and deadlines. Semi and anti joins can short-circuit differently, but their existence decisions still require complete opposite-side evidence.

Operational evidence matters as much as the algorithm. Partial runs, losing attempts, disk-full truncation, mixed comparator versions, and early unmatched emission can produce plausible but wrong output. Integrity manifests and transactional output commit are part of the join.

## Prerequisites and Retrieval

Retrieve partitioning, data locality, serialization, failures, and scale accounting from [LSDS-002](002-horizontal-partitioning.md) through [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md). Retrieve block integrity and metadata from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md).

Review comparator/grouping contracts in [LSDS-023](023-partitioners-and-combiners.md), attempt/materialization identity in [LSDS-027](027-task-retry-and-speculation.md) and [LSDS-028](028-intermediate-data-materialization.md), batch tracing in [LSDS-030](030-tracing-a-batch-job-through-a-cluster-engine.md), and shuffle/sort/repartition mechanics in [LSDS-031](031-shuffle-architecture.md) through [LSDS-036](036-repartition-joins.md). You should understand multiset joins, total ordering, external merge sort, logarithms, buffering/spill, checksums, backpressure, snapshots, and commit protocols.

## Learning Objectives

After this module, you should be able to:

1. separate distributed partitioning, local external sorting, and merge-join semantics;
2. specify compatible equality, comparator, collation, direction, null, NaN, type, and version contracts;
3. prove two-stream inner-join soundness and completeness under sorted and co-located inputs;
4. derive idealized run count, fan-in rounds, and materialized I/O while stating exclusions;
5. implement inner, outer, semi, and anti merge behavior with exact duplicate multiplicity;
6. bound equal-key groups using smaller-side buffering, spool/replay, block nesting, or explicit failure;
7. validate whether partition/order properties are reusable across files, snapshots, writers, and upgrades;
8. diagnose skew, giant rows/groups, descriptor pressure, disk exhaustion, corruption, and output explosion;
9. test run ordering, multiset conservation, attempts, adaptation, and cleanup with fault injection; and
10. govern sensitive sorted intermediates through minimization, isolation, encryption, retention, deletion, and audit.

## Core Exposition

### Freeze relational semantics first

Define join type, key expressions, equality, residual predicates, projection, and multiplicity before physical planning. Inner emits every qualifying pair. Left outer adds one null-extended result for each unmatched left row. Full outer does so for both sides. Semi emits each qualifying preserved row once; anti emits only rows with no qualifying opposite row.

For key $x$ with left group $A_x$ and right group $B_x$, inner output is the filtered Cartesian product. Pure equijoin cardinality is $|A_x||B_x|$. Residual predicates can reduce it but generally require examining candidate pairs. Uniqueness may simplify only when enforced for the exact snapshot.

Ordinary SQL null keys do not match; null-safe equality does. NaN behavior, timestamp zones, decimals, string collation, and implicit coercion vary by language/engine. Do not let a storage sort order silently define query equality.

### Require comparator compatibility

Each side needs a total ordering for the join key representation. The crucial compatibility property is: if a left and right key can match, neither comparator may order another occurrence so that the matching groups become separated or differently sequenced. Cross-type comparison must agree across sides.

A practical contract pins key fields/order, logical/physical types, coercion, normalization, comparator algorithm/version, locale/collation version, ascending/descending direction, null placement, NaN and signed-zero treatment, and byte decoding. Composite keys compare fields lexicographically under explicit boundaries.

Comparator equality and join equality need not be identical only if the engine groups a superset and evaluates full equality within it. If comparator separates keys that join equality equates, the merge can skip matches. Test antisymmetry, transitivity, totality, and equality compatibility.

### Establish compatible partitions

Sorting does not bring keys from different workers together. First partition both sides so all matchable keys share a destination, as proved in [LSDS-036](036-repartition-joins.md). Hash destinations may have no global range order; local sorting inside each destination is enough for independent joins.

Range partitioning can provide globally ordered destination ranges, but boundaries and comparator must match on both sides. Boundary sampling error causes skew, not incorrect matching, if both sides use the same exact boundaries. Differing boundary sets break co-location.

Co-partitioned sources can avoid shuffle when exact contract, snapshot, completeness, and physical placement are proven. One-sided exchange can target the other's partitions. Record the partition epoch alongside sort identity.

### Generate initial sorted runs

Read rows into a bounded sort arena. Store normalized keys and compact row references where possible; account for decoded objects, pointers, comparison scratch, serializers, compression, encryption, and allocator overhead. Sort when the soft threshold is reached, then write an immutable run.

Every run header names query/plan, side, partition, producer/sort attempt, comparator version, schema, key projection, codec/encryption, sequence, row count, byte length, minimum/maximum key where safe, and checksum. Finalize data before publishing metadata.

A row larger than the arena needs a large-record path: stream payload separately while sorting a bounded key/reference, or reject it under an explicit limit. One giant object must not deadlock progress waiting for impossible contiguous memory.

### Estimate run count and merge passes

The ideal $r=\lceil B/M\rceil$ treats byte sizes as uniform and all memory as payload capacity. Real runs vary with row width, normalized keys, object expansion, reserved workspace, and early spill thresholds. Measure actual rows and bytes per run.

Fan-in $F$ is limited by one input buffer per run, an output buffer, codec/encryption state, file descriptors, storage queue depth, and memory. With $r$ runs, approximately $\lceil\log_F r\rceil$ rounds reduce to one if every round is balanced and materialized.

Large fan-in reduces rounds but increases simultaneous readers and random access. Small fan-in increases sequential passes and write amplification. Choose from actual device, remote-store, descriptor, memory, and concurrency evidence.

### Merge runs without losing rows

A k-way merge holds each run's current key in a priority queue, emits the least, then advances that run. The invariant is that emitted output is sorted and is the multiset union of consumed prefixes; all unread records are no smaller than the last emitted key.

Short read, checksum failure, decoder error, or disk full fails the attempt. A partial output run stays invisible. Retries create new attempt-scoped runs rather than appending ambiguously. Input runs remain referenced until the output is durably validated and recovery no longer needs them.

When several runs share equal keys, tie order depends on run/heap behavior unless explicitly stabilized. Relational join correctness does not require stable equal-key order, but reproducible bytes or downstream APIs may. Add a durable tie-break identifier if required.

### Fuse the final merge into the join

Fully materializing one sorted run per side simplifies recovery and reuse. Alternatively, the final k-way merge of each side can stream directly into the join, avoiding final run writes and later reads. This lowers I/O and latency.

Fusion couples lifetimes and failure. A join retry may need to replay many input runs. Backpressure from large output stalls merge readers and retains buffers. If downstream fails after long processing, recomputation can be expensive. Decide whether a materialization boundary improves expected recovery.

The I/O equation must state whether source reads, initial writes, intermediate reads/writes, final writes, final reads, and output are counted. Quoting “two passes” without boundaries is meaningless.

### Perform the two-stream merge

Read current non-null key groups from left and right. If left key is smaller, it cannot match the current or later right keys; emit it as unmatched only for left/full outer, then advance left. If right is smaller, apply the symmetric rule. If equal, process both groups and advance both.

The no-skipped-match argument follows order: when $a<b$, every remaining right key is at least $b$, so none equals $a$. This relies on compatible total ordering. A single out-of-order record invalidates the inference.

At end, remaining groups are unmatched. Inner drops them; the relevant outer join emits them; semi drops left groups without a match; anti emits them. Null groups follow predicate-specific handling rather than ordinary comparator equality.

### Preserve duplicate groups

For equal groups of sizes $m$ and $n$, emit every required pair. Buffering both groups is simplest but unbounded. Buffer the smaller group and stream/replay the larger when possible. If neither fits, spool one or both groups to disk and use block-nested cross products.

With block capacity $C$, read a left group block, replay the complete right group, emit matches, then continue. This bounds memory but rereads data. Residual predicates still evaluate every candidate unless an additional valid index/filter helps.

Output backpressure is mandatory. Buffer limits cannot justify dropping pairs. A policy row limit changes query semantics and must be explicit; otherwise fail clearly before partial commit if required output cannot be served.

### Implement outer, semi, and anti joins

Left outer emits matched pairs for equal groups. If no candidate passes residual predicates, each left row emits once with null right fields. Therefore key equality alone cannot decide matched status when residual predicates exist.

Left semi needs emit each left row once if any right candidate passes. It may stop testing that left row after its first match but must handle predicates that vary by pair. Left anti emits only after exhausting all right candidates for that row.

Full outer must track which rows in both equal-key groups found a qualifying partner; unmatched members from either group emit once. Bitmaps or stable group row identifiers can bound tracking relative to group sizes, with spill for giant groups.

### Handle nulls, NaNs, and sentinels

Sorting typically places nulls first or last, but ordinary SQL equality treats them as nonmatching. Outer joins emit them as unmatched; inner drops them. Null-safe equality treats them as one equal group, potentially enormous. Do not infer match from comparator returning zero.

NaNs and signed zero need specified sort and equality behavior. A comparator must be total even if the query language's relational operators are partial. Normalize or use explicit category tags while retaining the full predicate check.

Sentinel encoding must not collide with real values. Cross-language runs must share canonical encoding and comparator tests, including minimum/maximum numbers, invalid Unicode policy, timezone transitions, and decimal scales.

### Reuse existing ordering cautiously

An input is reusable if every partition is sorted by a sufficient prefix under the exact comparator and files/segments can be consumed in monotone range order. Individually sorted files with overlapping ranges need a k-way merge even if no re-sort is needed.

Storage metadata must identify writer/comparator version, sort columns/order/direction, null rules, collation, min/max, snapshot, and completeness. Compaction can preserve, strengthen, weaken, or destroy order. Schema evolution and locale library upgrades can invalidate old claims.

Sampling can detect violations but cannot prove universal order. Validate metadata lineage and, where risk warrants, scan boundary/monotonicity evidence. If uncertain, feed segments into an external merge or sort again.

### Manage skew and heavy groups

Partition skew creates larger sort input and more runs. Equal-key skew creates giant groups and output. Range sampling may create uneven byte ranges when row widths vary. Worker placement can co-locate several heavy partitions.

Measure per-side partition bytes/rows, run count/sizes, merge rounds, comparator CPU, group sizes, predicted/actual pairs, spool bytes, output, blocked time, and worker disk. Report tails and maxima, not only averages.

Adaptive skew splitting must preserve group coverage. Splitting at key boundaries is easy when many distinct keys exist. Splitting inside one hot key requires replication or coordinated subproducts as in [LSDS-036](036-repartition-joins.md), plus exact outer unmatched ownership.

### Compare with shuffled hash join

Sort-merge offers external-memory behavior, sequential I/O, natural ordered scanning, and possible order reuse. It pays comparisons and run I/O even when a local build would fit. Hash join can be faster without required ordering but depends on hash-table memory/collision behavior or hybrid spill.

Inputs already sorted favor merge. A much smaller local side favors hash. Full outer and repeated downstream order may favor merge. Hardware matters: memory, SSD bandwidth, remote shuffle, CPU comparison cost, compression, and concurrent disk use.

A hint is optimizer input, not proof. Current Spark and Flink documentation exposes merge/shuffle hints while noting strategy support constraints. Admission and correctness gates must remain authoritative.

### Failure, retry, and commit

Attempt identity spans producer blocks, sort runs, merge outputs, local join, and sink output. Only one accepted producer/sort contribution per logical input range is consumed. Speculative sort or join attempts cannot both publish.

A retry uses the same snapshot, partition epoch, comparator, and run set, or the dependent plan advances coherently to a new generation. Never combine a newly compacted right ordering with an old left snapshot silently.

Cancellation fences late callbacks, closes descriptors, stops downloads, and leaves partial artifacts unreferenced. Cleanup follows reference/lease state and recovery policy, including losing attempts and fused-run inputs.

### Observability

Record plan decision, alternatives, statistics/confidence, partition and comparator identities, source order evidence, chosen memory/fan-in, expected runs/rounds/I/O, and whether final merges are fused.

Measure actual input/run bytes and rows, sort/compare CPU, spill threshold, run count, merge fan-in/rounds, read/write/local/remote bytes, compression, descriptors, checksums, corruption, disk wait/capacity, retries, and cleanup.

For the join measure groups, largest left/right group, candidate and emitted pairs, unmatched rows, residual selectivity, spool/replay, output bytes, backpressure, per-partition duration, and attempts. Use safe digests or controlled sketches for sensitive keys; metric labels must remain bounded.

### Validation and fault injection

Differentially compare with a trusted relational implementation. Test empty sides, one row, unique/duplicate/all-equal groups, inner/left/right/full/semi/anti joins, ordinary/null-safe nulls, NaNs, signed zero, composite keys, collation, coercion, residual predicates, and output multiplicity.

Property tests verify each run is sorted, merge conserves the exact input multiset, current-key advancement never skips a possible match, local partition unions equal the global result, and accepted attempts contribute once. Randomly vary run cuts and fan-in; output multiset must not change.

Inject giant rows/groups, disk full, descriptor exhaustion, short writes, corrupt/truncated/reordered runs, remote throttling, worker loss, cancellation, retry, speculation, stale/mixed comparator metadata, skew splitting, adaptive plan change, sink backpressure, and cleanup races. No partial, missing, duplicate, or mixed-generation result may commit.

### Security, privacy, and governance

Projection and filtering before sort reduce both exposure and cost. Normalize sensitive keys in controlled memory; do not include raw values in run filenames, errors, plan text, samples, traces, or high-cardinality metrics. Hashes may remain personal or confidential data.

Authorize every worker, disk, remote shuffle service, replica, operator, and administrator. Use scoped workload identity, encrypted transport/storage, integrity/authenticity, tenant and attempt namespaces, region-aware scheduling, quotas, and audited fetch/publication.

Retention covers initial/intermediate/final runs, spooled groups, caches, lost attempts, crash dumps, manifests, logs, and encryption keys. Delete only after active/recoverable readers and holds release, then verify deletion. High-risk joins require data-owner, platform, security, privacy/legal/records, regional, and affected-tenant review.

## Definitions and Notation

- $L_j,R_j$: complete left and right multisets in join partition $j$.
- $\preceq$: pinned compatible total comparator for ordered join keys.
- $B$: encoded bytes on one side of one partition entering external sort.
- $M$: usable sort payload memory after all reserves.
- $r=\lceil B/M\rceil$: idealized minimum initial-run count.
- $F$: bounded merge fan-in greater than one.
- $q=\lceil\log_F r\rceil$: idealized fully materialized merge rounds.
- $A_x,B_x$: equal-key groups for key $x$; $m_x=|A_x|$, $n_x=|B_x|$.
- **partition epoch**: immutable distribution/snapshot/attempt compatibility identity.
- **comparator identity**: key schema, normalization, order, collation, null/NaN behavior, and implementation version.

## Mechanisms, Invariants, or Proof Structure

1. Freeze join type, equality/residual predicate, keys, null/NaN behavior, multiplicity, and output contract.
2. Prove matchable rows co-locate under one complete partition epoch.
3. Pin comparator identity and verify it is total and compatible across sides and with join equality.
4. Validate reusable partition/order properties; otherwise exchange and generate bounded immutable sorted runs.
5. Admit memory, fan-in, descriptors, disk, I/O, group spool, output, and concurrent tasks.
6. Merge runs while proving sortedness and exact multiset conservation; optionally fuse final merges.
7. Advance unequal groups only under the compatible-order invariant; process equal groups by exact join semantics.
8. Bound duplicate groups and output using spool/replay/backpressure without semantic truncation.
9. Fence producer, sort, merge, join, and sink attempts; validate complete artifacts before commit.
10. Compare estimates with measurements, preserve recovery evidence, and delete after references and holds end.

For inner join soundness, every emitted pair comes from co-located rows and passes full predicate, so it belongs globally. For completeness, take a matching pair. Partition compatibility places both in one $j$; sort compatibility makes their equality groups appear at the same merge position. The scan cannot advance either group past the other because neither compares smaller. Exact group cross product emits the pair. Multiset-preserving runs and one accepted attempt preserve its multiplicity exactly.

For outer joins, the scan may emit a row unmatched only after ordered advancement or stream exhaustion proves no opposite equal-key group exists, or after all residual candidates in an equal group fail. Skew replication adds an ownership/reconciliation premise. Semi and anti proofs replace pair multiplicity with per-preserved-row existence.

The I/O model is conditional. It assumes ideal run fill, balanced fan-in, full materialization, and byte stability. Production review separates source, spill, merge, final-read, network, and output bytes and reports fused passes explicitly.

## Alternatives and Trade-Offs

**Fully materialized sort-merge** creates durable final runs and clean recovery/reuse boundaries, but adds final write/read. **Fused final merge** saves I/O and latency while coupling join backpressure and retry to many runs.

**Shuffled hash join** avoids comparison sorting and often wins when a local build fits. **Hybrid hash** spills partitions but can recurse under skew. **Sort-merge** offers sequential external processing and ordering reuse but pays merge passes.

**Hash partition plus local sort** balances equality groups without global ranges. **Range partition plus local sort** can produce global partition order and enable downstream ordered work, but boundary sampling and width skew require care.

**Buffer smaller equal group** is efficient when one side is bounded. **Spool and block-nest** handles two giant groups with bounded memory but rereads and cannot avoid required output. **Validated uniqueness** collapses group handling only when enforced.

**Stable tie order** improves reproducibility and byte comparisons but adds identifier/storage/comparison cost. Relational results are unordered unless an explicit output `ORDER BY` contract exists.

**Reusing stored sort order** avoids repeated work for recurring joins. Maintaining clustered layouts costs ingestion, compaction, metadata governance, and possibly write amplification.

## Failure Modes and Misconceptions

1. **“Repartitioned means sorted.”** Co-location and order are separate physical properties.
2. **“Both sides are ascending, so merge is safe.”** Comparator, type, collation, nulls, and version must also match.
3. **“Comparator zero proves join equality.”** Full equality/residual predicates may be stricter.
4. **“Sorting removes duplicates.”** A join must preserve $m_xn_x$ multiplicity unless query semantics say otherwise.
5. **“Merge join uses constant memory.”** Giant groups, fan-in buffers, codecs, and output require bounded state or spool.
6. **“External sort means disk cannot fill.”** Multiple runs/rounds, both sides, concurrency, retries, and output amplify bytes.
7. **“Maximum fan-in is fastest.”** Descriptors, memory, random reads, remote requests, and contention can worsen.
8. **“One sorted file per producer can be concatenated.”** Overlapping key ranges require a merge.
9. **“Stable hash partitions imply global order.”** Hash destination numbers carry no key-range order.
10. **“Equal-key output order is deterministic.”** Run generation, fan-in, retries, and heap tie behavior can reorder peers.
11. **“A hot key is fixed by more ordinary partitions.”** One equality group remains together unless explicitly split.
12. **“Semi join emits one row per key.”** It emits each qualifying preserved-side row once.
13. **“Outer unmatched rows can stream immediately.”** Complete opposite-side evidence and residual evaluation are required.
14. **“Missing and empty runs are equivalent.”** Empty requires accepted evidence; missing may mean incomplete work.
15. **“A retry can use newer sorted files.”** Snapshot/comparator/partition generations must advance coherently.
16. **“A merge hint overrides safety.”** Hints cannot make predicates, resources, or engine support compatible.
17. **“Encrypted spill is fully governed.”** Placement, identity, telemetry, retention, deletion, and audit remain.

## Worked Examples

### Example 1

A 960 MiB input with 120 MiB usable payload memory creates at least eight ideal initial runs. At fan-in four, two materialized merge rounds suffice: eight to two to one.

### Example 2

Using the chapter's conservative full-materialization accounting, the preceding sort performs $2(960)(1+2)=5{,}760$ MiB of source/run/final-read traffic. Fusing the last merge into the join removes a write/read boundary but changes retry behavior.

### Example 3

Left sorts strings under case-insensitive collation while right uses binary order. `A` and `a` can be grouped/ordered differently, so a two-pointer scan may skip a query-defined match. Normalize and pin one contract or sort again.

### Example 4

Key 17 has 2,000 left and 30,000 right rows. A pure equality inner join produces 60 million pairs. Buffering the 2,000-row side and streaming the other bounds group memory but not output.

### Example 5

Four individually sorted files have ranges `[1,20]`, `[8,30]`, `[31,40]`, and `[35,50]`. Concatenation is not sorted because ranges overlap; a four-way merge is valid if their comparator identities match.

### Example 6

For left outer join, left key 5 and right key 5 share a group, but a residual timestamp predicate rejects all pairs. Every left key-5 row must still emit once with null right fields; key equality alone is insufficient.

### Example 7

Ordinary SQL nulls placed first on both sides compare into adjacent groups but do not match. Inner drops them; full outer emits each left and right null row separately as unmatched.

### Example 8

A worker runs four join tasks. Each reserves 256 MiB sort memory, 96 MiB merge/group workspace, and 64 MiB output buffer. Admission is $4(256+96+64)=1{,}664$ MiB before runtime reserve and other operators.

### Example 9

A sort attempt writes six valid runs and a truncated seventh, then fails. The manifest remains incomplete; the consumer cannot reinterpret the absent checksum/final length as an empty run. A new accepted attempt supplies the logical input once.

### Example 10

This fixture implements ordinary-null inner and full-outer group merge and computes the idealized run model.

<!-- bijux-verify: {"id":"sort-merge-join-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"inner_rows=5 full_outer_rows=9\ninitial_runs=8 merge_rounds=2 full_io_mib=5760\n","stderr":""}} -->
```python
from itertools import groupby
from math import ceil, log

left = [(1, "L1"), (1, "L2"), (2, "L3"), (None, "L4"), (4, "L5")]
right = [(1, "R1"), (1, "R2"), (3, "R3"), (None, "R4"), (4, "R5")]


def groups(rows):
    ordered = sorted((row for row in rows if row[0] is not None), key=lambda row: row[0])
    return [(key, list(values)) for key, values in groupby(ordered, key=lambda row: row[0])]


left_groups = groups(left)
right_groups = groups(right)
inner = []
full_outer = [(key, value, None) for key, value in left if key is None]
full_outer += [(key, None, value) for key, value in right if key is None]
i = j = 0

while i < len(left_groups) and j < len(right_groups):
    left_key, left_rows = left_groups[i]
    right_key, right_rows = right_groups[j]
    if left_key < right_key:
        full_outer.extend((left_key, row[1], None) for row in left_rows)
        i += 1
    elif right_key < left_key:
        full_outer.extend((right_key, None, row[1]) for row in right_rows)
        j += 1
    else:
        pairs = [(left_key, l[1], r[1]) for l in left_rows for r in right_rows]
        inner.extend(pairs)
        full_outer.extend(pairs)
        i += 1
        j += 1

for key, rows in left_groups[i:]:
    full_outer.extend((key, row[1], None) for row in rows)
for key, rows in right_groups[j:]:
    full_outer.extend((key, None, row[1]) for row in rows)

bytes_mib = 960
memory_mib = 120
fan_in = 4
initial_runs = ceil(bytes_mib / memory_mib)
merge_rounds = ceil(log(initial_runs, fan_in))
full_io_mib = 2 * bytes_mib * (1 + merge_rounds)

print(f"inner_rows={len(inner)} full_outer_rows={len(full_outer)}")
print(f"initial_runs={initial_runs} merge_rounds={merge_rounds} full_io_mib={full_io_mib}")
```

The fixture validates group advancement, duplicate multiplicity, ordinary-null handling, outer emission, and arithmetic. It is not an external sorter, distributed exchange, collation test, or performance benchmark.

## Cross-Program Connections

- **Data Structures Engineering:** Priority queues, external sorting, run indexes, bitmaps, buffers, and block-nested products implement the operator.
- **Algorithms Engineering:** Total orders, loop invariants, multiset proofs, logarithmic merge depth, and output-sensitive complexity explain correctness and cost.
- **Database Systems Engineering:** Physical properties, join selection, collations, nulls, residual predicates, outer semantics, and cardinality estimation shape plans.
- **Data Engineering:** Clustering, bucketing, compaction, schema evolution, and recurring sorted layouts determine reuse.
- **Distributed Systems Engineering:** Immutable attempts, checksummed materialization, replay, fencing, leases, and transactional sinks preserve results under failure.
- **Platform Engineering:** Ephemeral disk, remote shuffle, descriptors, schedulers, quotas, backpressure, and observability determine safe concurrency.
- **Security Engineering:** Sorted intermediates expose values and distributions, requiring minimization, isolation, encryption, access control, and deletion.
- **Systems Engineering:** Network, CPU, memory, disk, metadata, recovery, and governance trade through one end-to-end join design.

## References

1. Apache Spark, [Performance Tuning: Adaptive Query Execution and Skew Join](https://spark.apache.org/docs/latest/sql-performance-tuning.html), accessed 2026-09-03.
2. Apache Spark, [SQL Hints: Merge Join](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-hints.html), accessed 2026-09-03.
3. Apache Spark, [Configuration: Shuffle and Sort-Merge Join](https://spark.apache.org/docs/latest/configuration.html), accessed 2026-09-03.
4. Apache Spark, [RDD Programming Guide: Shuffle and Sorting](https://spark.apache.org/docs/latest/rdd-programming-guide.html), accessed 2026-09-03.
5. Apache Spark, [PySpark DataFrame.sortWithinPartitions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.sortWithinPartitions.html), accessed 2026-09-03.
6. Apache Spark, [PySpark DataFrame.repartitionByRange](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.repartitionByRange.html), accessed 2026-09-03.
7. Apache Flink, [SQL Join Hints: SHUFFLE_MERGE](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/sql/queries/hints/), accessed 2026-09-03.
8. Apache Flink, [JoinOperatorBase.JoinHint API](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/api/common/operators/base/JoinOperatorBase.JoinHint.html), accessed 2026-09-03.
9. Apache Flink, [Deployment Configuration: External Merge Fan-In and Sort Spill](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/config/), accessed 2026-09-03.
10. Apache Flink, [AbstractMergeInnerJoinIterator API](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/runtime/operators/sort/AbstractMergeInnerJoinIterator.html), accessed 2026-09-03.
11. Apache Hadoop, [MapReduce Tutorial: Shuffle, Sort, and Merge](https://hadoop.apache.org/docs/stable3/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html), accessed 2026-09-03.
12. Dask, [DataFrame Joins: Sorted and Unsorted Layouts](https://docs.dask.org/en/stable/dataframe-joins.html), accessed 2026-09-03.

## Exercises

### Exercise 1

A 3.6 TiB local side is processed with 180 GiB usable sort memory and fan-in five. Under the ideal full-materialization model, compute initial runs, merge rounds, and $2B(1+q)$ I/O. State why this is not a bound on elapsed time or physical bytes.

### Exercise 2

Prove that advancing the smaller current key in an inner merge join cannot skip a match. State comparator, sortedness, equality, partition, completeness, and attempt premises.

### Exercise 3

An equal key has 120,000 left rows of 200 bytes and 80,000 right rows of 300 bytes. Compute group bytes and output pair count. Design bounded processing with a 16 MiB group-memory allowance.

### Exercise 4

Design a review that decides whether 2,000 allegedly sorted files produced across three writer versions may be reused without re-sorting for a locale-sensitive composite-key join.

### Exercise 5

Specify validation and failure tests for a full outer distributed sort-merge join with residual predicates, adaptive skew splits, remote encrypted runs, retries, and an exactly-once sink.

## Answers to the Exercises

### Answer 1

$3.6$ TiB divided by $0.18$ TiB gives 20 ideal initial runs. Fan-in five reduces 20 to four and four to one, so $q=2$. The model gives $2(3.6)(1+2)=21.6$ TiB across source read/initial write, two materialized read/write rounds, and final read under the stated convention. Real bytes depend on usable versus advertised memory, uneven rows/runs, compression, metadata, partial order, fused final merge, retries, storage replication, and output; elapsed time also depends on CPU, concurrency, devices, locality, and contention.

### Answer 2

Assume both complete accepted bucket streams are sorted under compatible total comparator, matchable keys compare into the same ordered equivalence position, and both belong to one partition/snapshot/comparator epoch. If current left key $a$ is smaller than right key $b$, every unread right key is at least $b$, hence strictly greater than $a$ and cannot equal it under the join contract. Advancing the left group therefore skips no match. The symmetric case follows. Exact run multiset conservation and one accepted attempt ensure rows are neither absent nor duplicated before this reasoning.

### Answer 3

Left group bytes are $120{,}000\times200=24{,}000{,}000$ bytes; right group bytes are $80{,}000\times300=24{,}000{,}000$ bytes. Pure equality output is $120{,}000\times80{,}000=9.6$ billion pairs. Neither group fits a 16 MiB allowance. Spool both as immutable group files, read bounded blocks from one, replay bounded blocks or the complete file from the other, and stream results under backpressure. Charge spool/replay/output, validate checksums and row counts, and preserve attempt identity. No buffering strategy removes the required 9.6 billion outputs.

### Answer 4

Inventory exact file snapshots, partition ranges, key fields/order/types, coercion, direction, null/NaN rules, locale/collation name and library/data version, normalization, comparator implementation, writer version, min/max metadata, and checksums. Prove each file is internally monotone and determine whether file ranges are nonoverlapping/ordered; overlapping valid files need k-way merge. Test cross-version comparator properties and boundary keys including accents, case, normalization forms, nulls, numbers, and composite prefixes. Check compaction/schema lineage and missing/duplicate files. If any version cannot be proven compatible, normalize and sort it under a new comparator epoch.

### Answer 5

Differentially test full-outer multiplicity and row identities for duplicates, nulls, equal keys with all/some/no residual matches, and giant groups. Property-test run order and multiset conservation, partition co-location, unique unmatched ownership, and sink attempt fencing. Inject skew split before/during retry, missing/corrupt/reordered encrypted chunks, key rotation/auth expiry, remote throttling, disk/descriptor exhaustion, worker/service loss, cancellation, speculative sort/join/sink attempts, and mixed epochs. Require complete manifests and checksums before processing, one comparator/partition/snapshot generation, designated unmatched ownership across splits, attempt-scoped output, atomic sink commit, bounded resources/backpressure, audited access, and reference-aware verified deletion.
