---
module_id: LSDS-007
program: Large-Scale Data Systems Engineering
level: 1
module_number: 7
title: Narrow and Wide Transformations
status: complete
last_verified: 2026-09-03
---

# Narrow and Wide Transformations

## One-Page Review

### Governing question

Given a physical dataflow edge, which parent partitions must supply each child partition, can adjacent work remain in one pipeline, and what redistribution, materialization, recovery, and skew costs follow?

### Essential definitions

- A **partition dependency relation** is the set of directed pairs `(parent partition, child partition)` required to compute an edge.
- **Parent fan-out** is the number of child partitions that consume one parent partition.
- **Child fan-in** is the number of parent partitions required by one child partition.
- A **narrow dependency**, in the classic resilient distributed dataset sense, uses each parent partition by at most one child partition.
- A **wide dependency** lets at least one parent partition contribute to multiple child partitions, usually through redistribution.
- A **shuffle** partitions records into target buckets, transfers or exposes those buckets to consumers, and normally materializes exchange state.
- **Co-partitioned inputs** use compatible partition functions, counts, key semantics, and epochs so corresponding partitions can be consumed together without repartitioning.
- A **recovery cone** is the set of upstream partition work and artifacts needed to reconstruct a lost result.

### Central model, mechanism, or theorem

For parent partitions `P`, child partitions `C`, and dependency relation `E subset P x C`, define `fanout(p)=|{c in C : (p,c) in E}|` and `fanin(c)=|{p in P : (p,c) in E}|`. The dependency is narrow when every `fanout(p) <= 1`; it is wide when some `fanout(p) > 1`.

Width is not child fan-in. A coalesced child can read several parents while every parent feeds only one child, so the dependency remains narrow. An aligned join can likewise read one partition from each of two parents without a shuffle. Classification belongs to the realized physical relation and engine contract, not merely to names such as `join`, `coalesce`, or `map`.

### Critical invariants

- Classify an exact physical edge version, not a logical operator name.
- Record both parent fan-out and child fan-in; they answer different questions.
- Preserve partitioner metadata only when key, function, partition count, and epoch remain compatible.
- A wide edge defines deterministic target ownership for every transferable record.
- A consumer reads one complete compatible exchange generation, never mixed attempts.
- Map-side combination can reduce bytes but does not make a wide dependency narrow.
- Adaptive coalescing, splitting, or join changes create a new graph and partition mapping.
- Narrow does not imply cheap; wide does not imply incorrect or always blocking.

### Common failures

Frequent failures are calling every join wide, defining width by child fan-in, assuming `map` always preserves partitioning, trusting stale partitioner metadata, treating broadcast as an ordinary all-to-all shuffle, ignoring hot-key skew, confusing stage boundaries with dependency width, estimating shuffle from row count alone, mixing exchange generations during retry, and using averages that hide one dominant target partition.

### Compact example

Four parent partitions can coalesce into two children as `{p0,p1}->c0` and `{p2,p3}->c1`. Each child has fan-in two, but each parent has fan-out one, so the edge is narrow. If three target children each require buckets from all four parents, each parent has fan-out three; the twelve-edge relation is wide and its recovery and transport surface are larger.

### Connections

[LSDS-005](005-distributed-task-graphs.md) supplies logical and physical graphs; [LSDS-006](006-stages-tasks-and-dependencies.md) supplies stage, task, and attempt identity. [LSDS-008](../ROADMAP.md) develops serialization boundaries, while later shuffle, skew, join, and recovery modules deepen the mechanisms introduced here.

## Governing Question

A transformation describes a result, but an execution engine must map that result onto partitions. The consequential question is not whether an API method sounds global. It is which parent partition supplies which child partition in the selected physical plan. That relation determines whether records can stay with one task pipeline, must be split among destinations, or can be read locally from already compatible layouts.

The familiar narrow-versus-wide vocabulary comes from Spark's resilient distributed dataset design. It is useful beyond one engine when stated precisely: narrow width restricts the number of children that use any one parent partition; wide width allows parent output to fan out. Other systems use terms such as one-to-one, partitioned, pointwise, all-to-all, shuffle, or exchange. Translate their actual edge semantics into the relation before comparing them.

The governing question therefore has several parts. What is the exact dependency relation? Which records cross worker or storage boundaries? Is exchange output pipelined, blocking, or hybrid? What state is materialized? Which partitions must be recomputed after loss? Can skew or adaptive execution alter the mapping? A sound design answers all of them rather than treating “wide” as a complete performance diagnosis.

## Why This Matters

Wide dependencies are often the largest discontinuities in a distributed job. A local record can be serialized, hashed, buffered, spilled, written, announced, transferred, fetched, deserialized, and combined at a remote target. Those steps consume CPU, memory, network, disk, file handles, metadata, and scheduler time. They also introduce correlated recovery: losing one shuffle block can pull upstream producers back into execution.

Narrow dependencies enable per-partition pipelines. A scan, parse, filter, and projection can often run in one task without materializing each intermediate dataset. Recovery can reproduce only the bounded parents of a missing child. Yet narrow is not synonymous with fast. One narrow partition may contain terabytes, call a slow external service, exhaust memory, or execute expensive code. Dependency shape is one cost dimension.

The distinction affects correctness. A keyed aggregation needs every record for a key at the responsible target. An inconsistent hash function, key normalization rule, partition count, or partitioner epoch silently splits the group. An aligned join that trusts false co-partitioning metadata can miss matches. A retry that combines blocks from incompatible shuffle attempts can duplicate, omit, or misclassify data.

It also affects operations. Stage graphs normally cut at materialized shuffle boundaries; dashboards attribute shuffle write, read, fetch wait, spill, and remote bytes to those cuts. Skew creates long-tail tasks and can defeat speculative execution because every copy receives the same oversized logical partition. Adaptive systems may coalesce small targets, split skewed ones, or switch join strategies after observing runtime statistics, so graph version belongs in evidence.

## Prerequisites and Retrieval

Recall from [LSDS-003](003-range-hash-and-consistent-partitioning.md) that a partitioner includes key semantics, function, partition count, and version. Recall from [LSDS-004](004-data-locality.md) that locality is an eligibility and cost relation, not a filename property. Retrieve from [LSDS-005](005-distributed-task-graphs.md) the distinction between logical and physical plans, and from [LSDS-006](006-stages-tasks-and-dependencies.md) the distinction between tasks and attempts.

You should understand sets, relations, directed graphs, hashing, range partitioning, joins, aggregation, serialization, materialization, idempotency, percentiles, and failure recovery. Keep two questions separate: “How many parents does this child read?” and “How many children use this parent?”

## Learning Objectives

After completing this module, you should be able to:

- represent a physical partition dependency as a relation;
- compute parent fan-out, child fan-in, edge count, and recovery parents;
- distinguish narrow and wide dependencies without relying on operation names;
- explain why coalescing and aligned joins can have narrow multi-parent dependencies;
- identify when map, union, join, and aggregation preserve or replace partitioning;
- describe shuffle write, transfer, fetch, materialization, and recovery mechanics;
- reason about compatible partitioners and false metadata;
- diagnose hot keys, skewed target buckets, spill, fetch wait, and long tails;
- separate width from blocking, broadcast, barriers, locality, and computational cost;
- version and validate adaptive dependency rewrites;
- design evidence for retry-safe exchange consumption; and
- specify high-consequence review beyond graph validation.

## Core Exposition

### The partition dependency relation

Let `P` be the set of partitions produced by one or more parent datasets and `C` the partitions of one child dataset. The edge relation `E subset P x C` contains `(p,c)` exactly when computing child `c` requires some output from parent `p`. Record parent dataset identity when partition numbers overlap; `left[0]` and `right[0]` are distinct vertices.

For a parent `p`, `fanout(p)` counts its dependent children. For a child `c`, `fanin(c)` counts its required parents. Total edge count `|E|` describes metadata and potential connection surface, but bytes on edges can be radically unequal. A useful implementation records bytes, records, locations, attempts, and validation state in addition to adjacency.

The classic narrow rule quantifies over parents: every parent partition is used by at most one child. The rule does not require every child to have one parent. This direction matters because a parent read by one child can often be consumed within one recovery/pipeline region even if that child concatenates several parent partitions.

A wide dependency exists when at least one parent partition supplies multiple children. Record-level routing may split one parent's records across every target. A compact graph often draws one arrow per partition pair, while the runtime produces many blocks or subpartitions per arrow.

### One-to-one, many-to-one, and all-to-all shapes

A one-to-one map has edges `p_i -> c_i`. Parent fan-out and child fan-in are both one. A filter normally keeps the same relation even though output record counts change. A partition-preserving map can retain the parent's partitioner only if it cannot alter key membership or ordering assumptions.

A narrow coalesce can map several old partitions into one new partition without splitting any parent: `p0,p1 -> c0` and `p2,p3 -> c1`. Child fan-in is two while parent fan-out is one. This shape reduces parallelism and can create large children, but it need not redistribute individual records across targets.

Union can also be narrow. A child partition may correspond directly to a partition from either input, or an engine may construct a child that reads a bounded partition from each parent. The precise implementation controls the relation. The fact that a node has two parent datasets does not by itself make the edge wide.

An all-to-all shuffle with `m` parents and `n` targets can expose as many as `m*n` partition edges. Empty blocks may be optimized away, but logical target ownership still covers every record. Sparse routing can have fewer nonempty edges while remaining wide because some parent feeds multiple children.

### Operator names do not determine width

`map` and `filter` are commonly narrow, but a library operation named map could invoke repartitioning or a remote lookup. `coalesce` is narrow when it groups existing partitions without shuffle and can be wide when a shuffle option redistributes records. `repartition`, global `distinct`, global sort, and unaligned keyed grouping usually require wide exchange.

An aggregation illustrates the logical/physical distinction. `groupByKey` needs all values for each key at one target and normally shuffles raw values. `reduceByKey` can combine values locally before the shuffle, reducing transferred records, but parent partitions still feed multiple targets. The dependency remains wide.

A join may be narrow, wide, or mixed. If both inputs have compatible hash or range partitioners, child `i` can read `left[i]` and `right[i]`; every parent partition feeds one child. If neither input is compatible, both sides redistribute. If one is already compatible, only the other side may need a wide dependency. A broadcast join uses a distinct replicated-data exchange for the small side and a narrow scan of the large side.

Query optimizers can insert, remove, or reuse exchanges. Therefore “this SQL join is wide” is incomplete until the physical plan, runtime rewrite, and partition metadata are known. Persist plan identity and examine the realized execution graph.

### Partitioner compatibility

Co-partitioning is a proof obligation, not a hint to trust casually. Compatible inputs need equivalent key extraction and canonicalization, equivalent equality and hash/range semantics, compatible partition counts and boundary definitions, and data produced under the claimed partitioner version. The same function name is insufficient if code, locale, seed, null handling, or range samples differ.

For an aligned equi-join, every equal key must route to the same partition index on both sides. If one side lowercases identifiers and the other preserves case, or one hash implementation changes its seed, corresponding partition numbers do not prove co-location. The engine must repartition or reject the compatibility claim.

Partition-preserving metadata can be invalidated by transformations. A value-only map may preserve keyed placement; a key-changing map generally cannot. Filtering preserves placement of retained records but can make sizes uneven. Sampling can preserve membership rules while changing distribution. Custom operators should declare preservation only under explicit contracts and tests.

Range partitioners require compatible ordered key domains and identical boundaries. Approximate sampling can produce different boundaries across runs. Save the boundary set or its digest with the graph and dataset. Hash partitioners require stable serialization or hashing across languages and versions.

### Shuffle mechanics

At a wide edge, a producer evaluates records, derives each target partition, optionally combines or sorts them, buffers target segments, and emits exchange blocks. The runtime registers block locations and attempt identity. Consumers fetch the blocks for their target, merge or sort them as required, deserialize records, and run downstream logic.

Memory pressure causes producer buffers or consumer aggregations to spill. Network transfer may be direct between workers, routed through an exchange service, or read from durable/object storage. Fetch can overlap computation or wait for a blocking completion condition. These choices change latency and recovery but not the abstract routing relation.

Estimate shuffle volume from serialized post-combine bytes, not input row count alone. Variable records, compression, skew, encoding, map-side aggregation, and empty targets matter. Network amplification can exceed logical bytes because of retries, replication, failed fetches, checksums, and protocol overhead.

Exchange output needs an identity such as `(job, graph_version, exchange, producer_partition, producer_attempt, target_partition, block)`. A target should accept blocks from one compatible producer-result set. Attempt-qualified candidates and authoritative registrations prevent late or speculative producers from replacing accepted blocks.

### Width, materialization, and stage boundaries

Width and blocking are related but not identical. Spark's classic batch scheduler materializes shuffle outputs and forms stage boundaries at wide dependencies. Other engines can pipeline a partitioned exchange, persist it fully, or use a hybrid mode that spills and supports selective recovery. A narrow edge can still be materialized because of checkpointing, reuse, memory limits, side effects, or policy.

Describe at least four properties independently: partition movement, streaming/blocking behavior, materialization durability, and scheduling coordination. Barrier or gang-scheduled work can be narrow in data dependency yet synchronized in execution. A broadcast has fan-out but differs from hash-partitioned all-to-all movement because every recipient gets the same artifact rather than a disjoint target bucket.

Pipeline fusion across narrow edges saves serialization and launch overhead. It also couples backpressure and makes a failed downstream computation rerun upstream logic unless an intermediate is persisted. Materializing a narrow edge can be rational when computation is expensive, nondeterministic, reusable, or isolated by a failure boundary.

A blocking shuffle decouples producer and consumer resource waves and creates reusable recovery state, but delays consumers and requires storage. A pipelined exchange reduces first-result latency but couples resource availability and failure. Hybrid designs trade disk, simultaneous capacity, and replay scope.

### Recovery cones

Lineage recovery asks which upstream partitions can reconstruct a missing child. Under a one-to-one narrow edge, lost `c7` needs only `p7`. Under narrow coalescing, it needs the bounded parent group assigned to `c7`. Under an aligned join, it needs corresponding partitions from both inputs.

For a shuffled target, the target's complete contents may draw blocks from every producer partition. Losing the target result can require refetching all surviving blocks; losing one producer's shuffle files can require recomputing that producer and regenerating its blocks for many targets. Thus parent fan-out enlarges the correlated consumer surface of producer loss.

Materialization changes the recovery cone. Durable exchange blocks can stop lineage replay at the exchange. Ephemeral blocks lost with a worker reopen their producing lineage. Checkpoints, replicas, remote shuffle services, and deterministic recomputation provide different cost, durability, and consistency contracts.

Recovery must retain graph and partitioner versions. An adaptive plan that split target 9 into 9a and 9b cannot combine old unsplit blocks with new split blocks without an explicit compatibility transformation. Consumers need a complete mapping and accepted generation.

### Skew and hot keys

Uniform partition count does not imply uniform work. A hot key maps all its records to one target under ordinary keyed semantics. That task may dominate elapsed time, memory, spill, and recovery even when other targets are empty. Range skew similarly follows unequal key density or a changed distribution after boundaries were sampled.

Measure per-partition records, serialized bytes, CPU, memory peak, spill, fetch wait, remote bytes, and duration. Compare median, upper percentiles, and maximum; stage averages erase the gating partition. Distinguish source-size skew, post-filter skew, key-frequency skew, join fan-out, and computational skew because remedies differ.

Map-side combining helps associative aggregation by reducing repeated values before exchange. It cannot distribute one indivisible hot-key reduce state across targets unless the computation is decomposed. Salting can split a hot key for a two-level associative combine, but it changes key semantics and requires a correct merge. A many-to-many hot-key join may produce a genuinely huge output that partition tuning cannot eliminate.

Speculation duplicates the same skewed target and usually does not reduce its intrinsic input. Adaptive skew handling may split one large shuffle partition and replicate the matching side of a join. That can reduce the tail while increasing reads and task count; evidence must show semantics, new mappings, and resource trade-offs.

### Adaptive execution and graph versions

Runtime statistics can justify coalescing many small post-shuffle partitions, splitting a skewed partition, changing a sort-merge join to broadcast, or selecting a different shuffled join implementation. These are physical rewrites, not mere metric annotations.

Assign a new graph or plan version and persist why the rewrite occurred, which statistics were used, the old-to-new partition mapping, and which artifacts remain compatible. Metrics should carry both original logical operator identity and realized physical edge identity so comparisons remain possible.

Adaptive decisions need stability controls. A threshold near observed size can cause plan oscillation across runs. Broadcast conversion can overload worker memory if estimates omit expansion. Aggressive coalescing can remove useful parallelism. Skew splitting can replicate too much data. Test threshold boundaries and retain the decision record.

### Observability and retained evidence

For every physical edge retain parent and child counts, nonempty edge count, maximum and distribution of parent fan-out and child fan-in, partitioner identity, graph version, exchange mode, and materialization policy. For every partition retain records, bytes, block count, locations, attempt generation, checksum/validation, and accepted state as appropriate.

Runtime metrics include shuffle bytes written/read, local and remote fetch bytes, fetch wait, transfer failures, serialization/deserialization time, spill bytes, peak execution memory, task duration, scheduler delay, and retry amplification. Attribute values per edge and partition rather than only per job.

Evidence for a no-shuffle claim includes compatible partitioner records for every input and a physical plan without a replacing exchange. Evidence for a completed shuffle includes one accepted producer result per required parent, a target mapping, registered and validated blocks, and consumer completion against one compatible generation.

Alerts should focus on ratios and tails: maximum-to-median partition bytes, p99 fetch wait, spill-to-input ratio, remote-to-total fetch ratio, failed-fetch rate, and repeated producer recomputation. Correlate a long child with its parent blocks and key distribution before choosing a remedy.

## Definitions and Notation

Let parent datasets be `D_1,...,D_k`, with disjoint qualified partition sets `P_i`; let `P` be their union. Let child partitions be `C`. A physical dependency relation is `E subset P x C`.

For each parent `p`, define `F_out(p)={c in C | (p,c) in E}` and `fanout(p)=|F_out(p)|`. For each child `c`, define `F_in(c)={p in P | (p,c) in E}` and `fanin(c)=|F_in(c)|`.

In the classic RDD lineage sense:

- `E` is narrow iff `max_{p in P} fanout(p) <= 1`;
- `E` is wide iff there exists `p in P` with `fanout(p) > 1`.

This definition classifies a dependency relation. A multi-input transformation can have one narrow and one wide parent dependency. Some engines define dependency per parent dataset rather than over their qualified union; state the granularity used.

Let `b(p,c)` be serialized bytes sent or exposed from `p` to `c`. Logical exchange bytes are `B=sum_(p,c in E) b(p,c)`. Physical network and storage bytes can exceed `B` through replication, retries, headers, checksums, and spills. Empty logical routes may be represented without physical blocks.

Let `R(c)={p | (p,c) in E}` be the immediate recovery parents of `c`. The transitive recovery cone follows these parents until it reaches durable valid materializations or source partitions. Let `V` identify graph/partitioner version; all adjacency, block, and recovery claims are relative to `V`.

A partitioner contract can be written `Q=(key_extractor, canonicalization, equality, routing_function, partition_count, parameters, code_version, epoch)`. Two inputs are co-partitioned for a keyed operation only when the required components of `Q` are compatible and their data actually satisfy the contract.

## Mechanisms, Invariants, or Proof Structure

To classify and validate a transformation:

1. Select the realized physical plan and graph version.
2. Qualify every parent partition by dataset and generation.
3. Enumerate or derive the parent-to-child relation.
4. Compute parent fan-out and child fan-in separately.
5. Classify width using parent fan-out under the stated engine definition.
6. Verify partitioner compatibility and target ownership for keyed edges.
7. Specify pipeline/blocking, materialization, and recovery independently.
8. Measure bytes and skew rather than inferring cost from width alone.
9. Fence attempts and accept one compatible exchange generation.
10. Review domain consequences independently of dataflow mechanics.

The following executable fixture checks four small dependency relations. It demonstrates classification and immediate recovery parents; it does not benchmark a runtime or prove production exchange correctness.

<!-- bijux-verify: {"id":"narrow-wide-dependency-relations","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"one_to_one kind=narrow edges=4 max_parent_fanout=1 max_child_fanin=1\ncoalesce kind=narrow edges=4 max_parent_fanout=1 max_child_fanin=2\naligned_join kind=narrow edges=4 max_parent_fanout=1 max_child_fanin=2\nshuffle kind=wide edges=12 max_parent_fanout=3 max_child_fanin=4\nrecovery_one_to_one_c1=('p1',)\nrecovery_coalesce_c1=('p2', 'p3')\nrecovery_aligned_join_c1=('left1', 'right1')\nrecovery_shuffle_c1=('p0', 'p1', 'p2', 'p3')\n","stderr":""}} -->
```python
from collections import defaultdict

patterns = {
    "one_to_one": {
        "c0": ("p0",), "c1": ("p1",), "c2": ("p2",), "c3": ("p3",)
    },
    "coalesce": {"c0": ("p0", "p1"), "c1": ("p2", "p3")},
    "aligned_join": {
        "c0": ("left0", "right0"), "c1": ("left1", "right1")
    },
    "shuffle": {
        f"c{i}": tuple(f"p{j}" for j in range(4)) for i in range(3)
    },
}

for name, children in patterns.items():
    fanout = defaultdict(int)
    for parents in children.values():
        for parent in parents:
            fanout[parent] += 1
    edges = sum(map(len, children.values()))
    kind = "narrow" if max(fanout.values(), default=0) <= 1 else "wide"
    print(
        f"{name} kind={kind} edges={edges} "
        f"max_parent_fanout={max(fanout.values(), default=0)} "
        f"max_child_fanin={max(map(len, children.values()), default=0)}"
    )

for name in patterns:
    print(f"recovery_{name}_c1={patterns[name]['c1']}")
```

The coalesce and aligned-join cases are the critical counterexamples. Both have maximum child fan-in two, yet remain narrow because no parent partition feeds more than one child. The shuffle has parent fan-out three and is wide. Its `c1` immediate recovery set includes every parent.

Correctness for a keyed wide edge requires a routing invariant: for every input record `r` with key `k`, exactly one target partition `q_V(k)` owns `r` for graph version `V`, and every record equivalent under the operation's key semantics uses the same target. Completion requires every accepted producer partition to account for every routed record and every consumer to use compatible accepted blocks.

Correctness for an aligned join requires more: equal keys from both parents must select the same corresponding child; all required parent partitions must be complete; and no key-changing transformation may have falsely retained partitioner metadata. Matching partition indices alone do not prove the invariant.

Recovery safety requires a compatible cut. Starting from a lost child, follow `R(c)` until valid durable artifacts are found. Every reused artifact must match `V`, input snapshot, code, schema, partitioner, and accepted attempt contract. Recompute the missing cone, then publish one complete generation.

Performance claims require empirical dimensions. Width predicts a potential redistribution structure, not bytes, duration, or bottleneck. Report workload distribution, block sizes, compression, placement, concurrency, spills, retries, and percentile/tail results with the exact plan.

## Alternatives and Trade-Offs

Keeping the current partitioner avoids exchange when future operations share its key and parallelism. It can also preserve a poor partition count or severe skew. Repartition when downstream savings exceed the immediate shuffle and when the new layout has a durable reuse horizon.

Hash partitioning balances many ordinary keys and supports equality operations, but hot keys remain concentrated and layout changes when partition count or hash semantics change. Range partitioning supports ordered scans and global order construction, but sampled boundaries can become stale and uneven. Random repartitioning balances records but destroys key locality.

`groupByKey` preserves all values for arbitrary group processing but transfers and holds more data. Associative `reduceByKey` or combiner designs reduce exchange volume, but require correct associativity, identity, and sometimes commutativity assumptions. Floating-point or order-sensitive reductions may change results when combination order changes.

A shuffle join is general and distributes both inputs according to join key, but pays exchange and sort/hash cost. A co-partitioned join avoids redistribution when its compatibility proof is sound. A broadcast join avoids repartitioning the large side, but replicates the small side and risks memory pressure. Adaptive selection can improve uncertain plans but complicates reproducibility and evidence.

Narrow coalescing lowers output count without full redistribution, yet can create uneven partitions because only adjacent or assigned parents combine. Shuffle coalescing can rebalance more freely at exchange cost. Splitting a hot target adds parallelism only when the operation permits decomposing its state or output.

Pipelined exchange lowers first-record latency and storage, while coupling producer/consumer resources, backpressure, and recovery. Blocking exchange adds materialization and delay while isolating waves and supporting replay. Hybrid exchange chooses between them based on resources or failure path and needs explicit operational semantics.

Remote/durable shuffle services protect blocks from executor loss and reduce recomputation, but add infrastructure, storage, security, lifecycle, and consistency obligations. Lineage-only recovery is simpler for bounded cheap computation but can amplify replay through many wide edges.

## Failure Modes and Misconceptions

1. **Every child with several parents is wide.** Width is defined by parent fan-out, not child fan-in.
2. **Every join is wide.** Compatible co-partitioned inputs can join by corresponding partitions.
3. **Every coalesce is narrow.** A shuffle-enabled coalesce or rebalance can redistribute records.
4. **Every map preserves partitioning.** A key-changing map invalidates keyed placement.
5. **Every filter balances work.** Selectivity can be extremely uneven across partitions.
6. **Union is necessarily wide.** Its dependency can map each parent partition to only one child.
7. **A combiner makes aggregation narrow.** It reduces transferred values but not target fan-out.
8. **More target partitions remove hot keys.** One key still selects one target under ordinary grouping.
9. **Speculation fixes skew.** Copies repeat the same oversized logical work.
10. **Wide means blocking.** Engines can pipeline or hybridize partitioned exchange.
11. **Narrow means pipelined.** Checkpointing, reuse, policy, or resources can materialize it.
12. **Narrow means cheap.** A single partition can dominate compute, I/O, or memory.
13. **Wide means bad design.** Correct grouping, joins, sorting, and repartitioning often require it.
14. **Partition number proves compatibility.** Key semantics and partitioner versions must also match.
15. **A function name proves compatibility.** Parameters, code, seeds, boundaries, and epochs can differ.
16. **Row count estimates shuffle bytes.** Serialization, compression, combination, and width vary.
17. **Average partition size is enough.** Maximum and tail distributions gate completion.
18. **Empty block suppression changes width.** It changes physical sparsity, not the routing contract.
19. **Broadcast is an ordinary shuffle.** It replicates one artifact rather than disjoint keyed buckets.
20. **A stage boundary proves a wide edge.** Checkpoints, barriers, and resource changes also create cuts.
21. **A wide edge always crosses machines.** Co-location can make some or all fetches local.
22. **Process success makes a shuffle block durable.** Executor loss can remove ephemeral output.
23. **Any available block generation can be fetched.** Consumers need one compatible accepted set.
24. **Adaptive rewrites preserve identity automatically.** Split/coalesced mappings need a new plan version.
25. **A valid graph proves domain safety.** Consequence-specific semantics and review remain independent.

## Worked Examples

### Example 1

**Question:** Four parents map one-to-one to four children. What are maximum fan-out and fan-in?

**Reasoning:** Each parent appears in one edge and each child has one parent.

**Conclusion:** Both maxima are one; the dependency is narrow.

### Example 2

**Question:** Can two parents feed one coalesced child without making the edge wide?

**Reasoning:** Yes, if neither parent feeds another child. Child fan-in is two while each parent fan-out is one.

**Conclusion:** Many-to-one can be narrow.

### Example 3

**Question:** Two hash-partitioned inputs have eight partitions and the same verified partitioner. Does their equi-join need a shuffle?

**Reasoning:** Child `i` reads `left[i]` and `right[i]`; every parent partition feeds one child.

**Conclusion:** The join dependencies can be narrow, subject to a valid compatibility proof.

### Example 4

**Question:** One join input has the target partitioner and the other does not. How should the edge be described?

**Reasoning:** The compatible side can remain narrow; the incompatible side redistributes and is wide.

**Conclusion:** Multi-input transformations can mix dependency types.

### Example 5

**Question:** Does local aggregation before `reduceByKey` change a wide edge into a narrow one?

**Reasoning:** It can shrink bytes per destination, but a producer may still emit combined values to several targets.

**Conclusion:** Combination changes volume, not dependency width.

### Example 6

**Question:** A shuffle has 100 producers and 200 targets. Must it create 20,000 nonempty blocks?

**Reasoning:** That is the maximum partition-pair surface. Sparse keys and empty-block elision can reduce physical blocks.

**Conclusion:** Distinguish logical routing capacity, nonempty edges, and actual block count.

### Example 7

**Question:** Why can one lost producer affect many downstream targets?

**Reasoning:** Its parent fan-out includes every target to which it emitted a block. Those targets lose part of their required input.

**Conclusion:** Wide fan-out creates correlated recovery surface.

### Example 8

**Question:** Ninety-nine targets finish in 30 seconds and one hot-key target takes 20 minutes. Will speculation solve it?

**Reasoning:** A speculative copy receives the same hot-key partition. Split/decompose the key's computation or change semantics-aware routing instead.

**Conclusion:** Diagnose intrinsic skew before duplicating attempts.

### Example 9

**Question:** AQE coalesces 400 post-shuffle targets into 80. What identity must change?

**Reasoning:** The realized physical graph and old-to-new target mapping changed. Metrics, blocks, and recovery must refer to that version.

**Conclusion:** Adaptive partition rewrites require explicit graph identity.

### Example 10

**Question:** Can a narrow dependency proof approve redistribution of national benefits records?

**Reasoning:** No. Eligibility meaning, identity matching, jurisdiction, corrections, appeals, accessibility, privacy, security, retention, audit, outage behavior, and disparate-impact consequences require named benefits-policy, legal, casework, accessibility, privacy/security, data-governance, operations, and independent assurance review. No external approval is claimed here.

**Conclusion:** Execution correctness is necessary but not sufficient for high-consequence systems.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies graphs, maps, hashing, external sorting, and sketches. [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies work/span, sorting, hashing, and probabilistic sampling. [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies buffering, memory, files, processes, and I/O scheduling.

[Data Engineering](../../19-data-engineering/ROADMAP.md) owns pipeline intent, transforms, data quality, and published products. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns canonical keys, dataset contracts, partitioning strategy, and lineage. This program owns the runtime partition relation and its execution consequences.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) develops failure models, retries, leases, consistency, and idempotency. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns cluster resources, workload placement, storage/network services, and telemetry. [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) connects when services expose asynchronous jobs, plan identity, progress, and retry-safe results.

MapReduce makes the shuffle boundary explicit between map and reduce partitions. Dryad generalizes computation to vertices and channels. Spark formalizes narrow and wide lineage dependencies. Tez exposes edge movement, source, and scheduling properties. Flink distinguishes pipelined, blocking, and hybrid data exchange. Beam requires grouping operations to bring values for a key together. Dask graphs make dependencies explicit while leaving execution and materialization strategy to schedulers and collections.

## References

- Matei Zaharia et al., [*Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing*](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf), NSDI, 2012. Primary narrow/wide dependency, stage, pipeline, co-partitioned join, and lineage recovery design.
- Jeffrey Dean and Sanjay Ghemawat, [*MapReduce: Simplified Data Processing on Large Clusters*](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), OSDI, 2004. Primary map partition, shuffle, reduce partition, locality, retry, and backup execution design.
- Michael Isard et al., [*Dryad: Distributed Data-Parallel Programs from Sequential Building Blocks*](https://www.microsoft.com/en-us/research/publication/dryad-distributed-data-parallel-programs-from-sequential-building-blocks/), EuroSys, 2007. Primary computation-graph vertex and channel model.
- Apache Spark Project, [*RDD Programming Guide*](https://spark.apache.org/docs/latest/rdd-programming-guide.html), checked 2026-09-03. Official current transformation, shuffle, persistence, and broadcast documentation.
- Apache Spark Project, [*Performance Tuning*](https://spark.apache.org/docs/latest/sql-performance-tuning), checked 2026-09-03. Official current adaptive partition coalescing, skew splitting, and join conversion documentation.
- Apache Flink Project, [*Jobs and Scheduling*](https://nightlies.apache.org/flink/flink-docs-stable/docs/internals/job_scheduling/), checked 2026-09-03. Official current job/execution graphs, parallel subtasks, pipelining, and scheduling documentation.
- Apache Flink Project, [*Configuration: Batch Shuffle Mode*](https://nightlies.apache.org/flink/flink-docs-master/docs/deployment/config/#execution-batch-shuffle-mode), checked 2026-09-03. Official current pipelined, blocking, and hybrid exchange semantics.
- Apache Tez Project, [*EdgeProperty API*](https://tez.apache.org/releases/0.10.3/tez-api-javadocs/org/apache/tez/dag/api/EdgeProperty.html), checked 2026-09-03. Official edge data-movement, source, and scheduling property model.
- Apache Beam Project, [*Programming Guide: GroupByKey*](https://beam.apache.org/documentation/programming-guide/#groupbykey), checked 2026-09-03. Official keyed grouping, windowing, and trigger constraints.
- Dask Project, [*Task Graphs*](https://docs.dask.org/en/stable/graphs.html), checked 2026-09-03. Official graph representation and dependency documentation.

## Exercises

### Exercise 1

For `c0={p0,p1}`, `c1={p2}`, and `c2={p3,p4}`, compute edge count, maximum parent fan-out, maximum child fan-in, width, and immediate recovery parents of `c2`.

### Exercise 2

Two datasets each have 64 partitions and claim the same hash partitioner name. List the evidence required before planning a narrow equi-join.

### Exercise 3

A 50-producer, 100-target aggregation shuffles 2 TB. One target receives 600 GB, median target size is 8 GB, map-side combining is enabled, and three speculative copies of the large target fail with OOM. Diagnose and propose a semantics-preserving response.

### Exercise 4

Compare a blocking durable shuffle, a pipelined exchange, and a hybrid exchange across latency, simultaneous resources, storage, backpressure, and recovery.

### Exercise 5

A public-health system groups laboratory reports by person before issuing outbreak notifications. Specify partition, compatibility, exchange, retry, evidence, and named review requirements.

## Answers to the Exercises

### Answer 1

There are five edges. Every parent appears in exactly one child set, so maximum parent fan-out is one and the dependency is narrow. Maximum child fan-in is two. The immediate recovery parents of `c2` are `{p3,p4}`. This example proves that child fan-in greater than one does not by itself imply width.

### Answer 2

Require qualified dataset and snapshot identities; identical key extraction, canonicalization, equality, null handling, serialized key representation, routing function, seed/parameters, partition count, code version, and partitioner epoch; evidence that both writers enforced that contract; compatible schema and join-key types; complete validated partitions; and a physical-plan check that no exchange replaces the claimed alignment. Test adversarial equal keys across languages, versions, case/Unicode forms, nulls, and boundary values. A shared name or matching count is insufficient.

### Answer 3

The 600-GB target is at least 75 times the 8-GB median and is the gating skewed partition. Combination has already reduced combinable values but does not alter keyed target ownership; speculation duplicates the same memory requirement and worsens contention. Inspect key frequencies, record expansion, memory/spill, and whether one hot key or many collisions dominate. For an associative aggregate, split a hot key into deterministic salted subkeys, aggregate each, and merge with the same valid algebra; otherwise isolate the key, increase appropriate resources, or redesign the exact computation. Validate result equivalence, new partition mappings, retry behavior, and downstream compatibility before rollout.

### Answer 4

A blocking durable shuffle completes and stores producer outputs before consumers, increasing first-result latency and storage while decoupling resource waves and narrowing replay when artifacts survive. A pipelined exchange overlaps producers and consumers, reducing latency and storage but requiring simultaneous capacity, live backpressure, and more coordinated recovery. A hybrid exchange permits overlap when resources allow and spills/materializes according to policy, offering flexibility at the cost of more complex state and failure semantics. Width alone does not select among them; workload, latency, capacity, durability, and failure objectives do.

### Answer 5

Identify report snapshot, person-linkage rule/model version, canonical person key, partitioner contract, graph/exchange generation, producer and target partitions, task attempts, accepted blocks, grouped record, notification decision, and delivery receipt. Prove equivalent person keys co-locate while explicitly handling uncertain or corrected identity links; consume one complete compatible exchange generation; use attempt-fenced blocks and idempotent notification keys; retain source-to-group-to-decision lineage; and test duplicates, late/corrected reports, key collisions, skew, missing blocks, mixed attempts, regional loss, replay, and suppression/withdrawal. Named reviewers include epidemiologists, laboratory and public-health informatics owners, identity/data-quality specialists, notification operations, accessibility and language-access experts, privacy/governance, cybersecurity, distributed-systems and disaster-recovery engineers, legal/public-health authority, affected-community representation, and independent safety/ethics assurance. Local graph checks do not constitute external approval.
