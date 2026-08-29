---
module_id: CONPAR-045
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 45
title: Work Partitioning and Granularity
status: complete
last_verified: 2026-08-29
---

# Work Partitioning and Granularity

## One-Page Review

### Governing question

How should work and data be partitioned into scheduling units large enough to amortize overhead and preserve locality, yet numerous and balanced enough to expose parallelism, tolerate skew, and bound cancellation and memory?

### Essential definitions

- A **partition** is a subset of a logical domain assigned one ownership, placement, or scheduling role.
- **Granularity/grain size** is the amount of useful work represented by one task or chunk.
- **Decomposition** identifies independently executable work; **mapping** assigns it to execution resources.
- **Overdecomposition** creates more logical partitions/tasks than workers so a scheduler can rebalance.
- A **static partition** is chosen before execution; a **dynamic partition** is created or reassigned as work is discovered.
- **Block partitioning** assigns contiguous regions; **cyclic partitioning** distributes positions round-robin; **block-cyclic** combines both.
- A **halo/ghost region** duplicates or communicates boundary data needed by a neighboring partition.
- **Load imbalance** is the gap between the most heavily loaded resource and ideal/average useful work.
- **Scheduling overhead** includes task creation, enqueue/dequeue, stealing, synchronization, and bookkeeping.
- **Surface-to-volume ratio** relates inter-partition boundary/communication to useful interior work.

### Central model, mechanism, or theorem

For work items with costs `c_i` partitioned into worker loads `L_j`, ideal average load is `W/P`, where `W=sum c_i`; makespan is at least `max(W/P,max_i c_i)` and a fixed assignment completes no sooner than `max_j L_j`. Finer grain can lower imbalance and expose more ready work, but raises task/scheduling metadata and may damage locality. Coarser grain amortizes overhead and communication, but raises the indivisible-tail and cancellation-latency bounds. The optimum depends on cost distribution, topology, data movement, runtime, input, and service objectives; it is measured, not universal.

### Critical invariants

Partitions cover the required domain and are disjoint unless overlap/replication has declared merge semantics. Each partition has one owner for mutable state and stable identity independent of worker. Boundary/halo data belongs to a versioned epoch. Grain never changes public result semantics. Task/partition count, metadata, retained bytes, output expansion, retries, and discovery are bounded. No partition waits while holding a resource its successor/neighbor requires. Repartitioning transfers ownership atomically or by an explicit versioned protocol. Completion accounts for every partition and cleans abandoned work.

### Common failures

Code divides item count by CPU count and calls it balanced; creates fewer partitions than workers; creates one task per byte; ignores task cost variance or hot keys; partitions mutable data with overlapping aliases; uses a hash partition that destroys range locality; chooses contiguous blocks for periodic expensive items; makes tiles too small and communicates mostly halos; makes chunks too large to cancel; prebuilds millions of tasks; rebalances data without moving ownership/version; pins work to stale NUMA placement; or benchmarks one cutoff and records it as universal truth.

### Compact example

Nine independent costs `[9,8,7,6,5,4,3,2,1]` split into three contiguous equal-count blocks yield loads `[24,15,6]`, so makespan is at least 24. A deterministic largest-cost-first greedy assignment yields partitions `[9,4,3]`, `[8,5,2]`, and `[7,6,1]` with loads `[16,15,14]`. Total work 45 gives ideal load 15 and imbalance factor `16/15=1.067`. The improvement is model evidence, not a universal scheduling guarantee; locality or migration can reverse it.

### Connections

[Parallel Loops and Reductions](044-parallel-loops-and-reductions.md) supplies chunk scheduling and aggregation; [Backpressure in Asynchronous Pipelines](040-backpressure-in-asynchronous-pipelines.md) supplies bounded admission. The [program roadmap](../ROADMAP.md) next isolates load-balance and scheduling-overhead analysis.

## Governing Question

How can engineers choose and adapt partition boundaries and grain so correctness ownership remains stable while useful work dominates scheduling, communication, imbalance, and retained-state costs?

Partitioning is a semantic ownership decision before it is a tuning knob.

## Why This Matters

Parallel hardware executes finite resources, but applications often expose millions of records, pixels, vertices, cells, queries, or recursive subproblems. The system must convert that logical domain into work units. Those boundaries govern who may mutate data, which bytes move, which failures isolate, where queues form, and how much work a scheduler can redistribute.

Poor granularity defeats an otherwise correct parallel algorithm. Tasks that are too fine spend more time allocating, queueing, stealing, synchronizing, and missing caches than computing. Tasks that are too coarse leave workers idle behind a straggler, retain large buffers, and respond slowly to cancellation. Equal item counts can hide orders-of-magnitude cost variation.

Partitioning also links algorithms to architecture. Contiguous ranges exploit cache and storage locality; hash partitions balance keys but scatter ranges; geometric tiles trade interior work against halos; graph cuts trade balance against crossing edges; GPU blocks trade occupancy against registers/shared memory. A durable design states its cost and ownership hypotheses and validates them for target environments.

## Prerequisites and Retrieval

Retrieve:

- ownership from [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md);
- false sharing from [False Sharing and Cache-Line Contention](029-false-sharing-and-cache-line-contention.md);
- bounded admission from [Backpressure in Asynchronous Pipelines](040-backpressure-in-asynchronous-pipelines.md);
- task work/span from [Task Parallelism and Dependency Graphs](041-task-parallelism-and-dependency-graphs.md);
- data partition laws from [Data Parallelism and Bulk Operations](042-data-parallelism-and-bulk-operations.md);
- fork/join cutoffs from [Fork-Join Computation](043-fork-join-computation.md); and
- loop chunks from [Parallel Loops and Reductions](044-parallel-loops-and-reductions.md).

Retrieval prompt: draw every place a work item and its bytes can reside, assign an owner and cost estimate, then predict what changes when grain is halved and doubled.

## Learning Objectives

After completing this module, a learner can:

1. separate decomposition, partition, mapping, scheduling, and placement;
2. prove partition coverage, disjointness, ownership, and halo semantics;
3. compare block, cyclic, block-cyclic, hash, range, graph, geometric, and recursive partitions;
4. derive ideal load, assignment makespan, imbalance, and simple overhead bounds;
5. choose overdecomposition and grain from balance, overhead, locality, and cancellation needs;
6. handle weighted, skewed, expanding, and dynamically discovered work;
7. reason about cache, NUMA, accelerator, storage, and network placement;
8. specify safe repartitioning, migration, versioning, and failure cleanup;
9. bound task metadata, live frontier, retained memory, retries, and outputs; and
10. test and benchmark partition policies without turning one measurement into a universal rule.

## Core Exposition

### Decomposition, partition, mapping, scheduling

Decomposition finds logical work that can proceed independently under a dependency model. Partitioning groups that work and usually defines ownership or data locality. Mapping associates partitions with resource classes or placements. Scheduling chooses when/where an eligible unit runs. Conflating them makes design brittle.

A matrix may be decomposed into independent tiles, partitioned into larger tile groups, mapped so GPU-capable work goes to a device, and dynamically scheduled within each CPU/GPU queue. A worker can execute many partitions and a partition can migrate if its ownership protocol permits. Worker identity should not become result identity.

Semantic boundaries should survive scheduling changes. Give partitions stable logical IDs/ranges/epochs. Store results by those identities, not completion sequence or thread number.

### Coverage and ownership proof

For domain `D`, partitions `{P_k}` must cover required elements: their union equals `D`. For exclusive mutation, they must be pairwise disjoint. Overlap is legitimate for read-only replicated inputs, stencil halos, speculative work, or reductions only when merge/discard/version semantics are explicit.

Half-open ranges simplify adjacent coverage. For `n` elements and `q` blocks, quotient/remainder formulas can distribute sizes differing by at most one. Test `n=0`, `n<q`, exact division, remainder one, maximum indices, and overflow in `start+length`.

Language ownership can help prove disjointness, but unsafe pointers, shared object graphs, allocator metadata, external files, and devices may remain shared. Partitioning a list of references does not partition the referenced mutable objects.

### Cost is not count

Let item `i` have useful cost `c_i`. Equal cardinality balances only when costs are sufficiently uniform. Sparse matrix rows vary in nonzeros; files vary in bytes and parse difficulty; graph vertices vary in degree; queries vary in plans; compression varies with content.

Cost estimates may use size, historical measurements, sampled features, static complexity, or online elapsed work. Estimation itself costs time and can be adversarially wrong. Prefer robust bounds and adaptive fallback rather than assuming perfect prediction.

Multi-resource cost is a vector: CPU, bytes read/written, memory retained, GPU registers, remote requests, or deadlines. A scalar score can hide the actual bottleneck. Partition policy should name which resource it balances.

### Lower bounds and imbalance metrics

Total work `W=sum c_i` on `P` identical processors has lower bound `W/P`. No schedule completes before the largest indivisible item `max c_i`. For a fixed assignment with load `L_j`, idealized compute makespan is `max L_j`.

Imbalance factor can be `max L_j/(W/P)`; efficiency from assignment alone is `W/(P*max L_j)`. Define whether overhead/communication is included. Ratios with empty work require explicit convention.

These metrics do not predict cache, synchronization, communication, or dependency span. Two partitions with equal cost estimates can contend for one lock and serialize. Use metrics as diagnostics, not proofs of runtime.

### Block and cyclic partitions

Contiguous block partitioning keeps neighboring data together. It works well for arrays, range scans, sequential storage, cache lines, and geometric regions. It suffers when expensive items cluster.

Cyclic partitioning assigns item `i` to `i mod P`, spreading periodic or clustered cost but producing strided access and fragmented I/O. Block-cyclic uses blocks of size `b` round-robin, balancing at block granularity while retaining local runs.

Worker-count-based partitions couple result/data ownership to deployment size. Prefer logical partitions independent of workers when stable recovery, caching, or deterministic output matters; map many logical partitions onto current workers.

### Hash and range partitions

Hash partitioning distributes keys by a stable hash and partition count. It usually balances many well-distributed keys and co-locates equal keys, but destroys order/range locality. Hash version/seed and partition-count changes remap data; consistent-hashing or explicit migration can reduce movement, not remove ownership transfer.

Range partitioning preserves order and supports scans. Balanced boundaries require distribution knowledge; skew/hot ranges cause imbalance. Samples/histograms can choose quantiles, with uncertainty and drift.

A hot key cannot be balanced by ordinary hash if all equal keys require one owner. Split by secondary dimension with an associative merge, replicate read-only state, or redesign the key protocol. Never silently break single-key ordering/transactions for balance.

### Geometric tiles and halos

Multidimensional grids use slabs, pencils, blocks, or tiles. Smaller tiles expose parallelism and cache reuse choices but increase boundary count. Stencil partitions require halo/ghost cells from neighbors for one epoch.

If a `d`-dimensional tile has characteristic size `s`, interior volume grows roughly `s^d` while boundary grows `s^(d-1)`, so boundary-to-volume decreases as tiles grow. Exact constants and topology matter. Tiny tiles can spend most time exchanging halos or synchronizing.

Version halos by simulation step. A partition must not mix neighbor data from different epochs. Double buffering and explicit exchange/barrier or dependency events establish readiness. Ownership of physical boundaries and corner cells must be defined.

### Graph and irregular partitions

Graph workloads balance vertex/edge weights while minimizing cut edges and respecting memory. Optimal partitioning is generally hard; heuristics use multilevel coarsening, streaming assignment, community structure, or domain knowledge.

Vertex count is a weak proxy when degree varies. Edge-cut affects communication; vertex-cut can replicate high-degree vertex state and needs reconciliation. Dynamic frontiers change active work each iteration, so a static whole-graph balance may not balance the frontier.

Irregular tree/search problems often use recursive decomposition and work stealing. Stable subproblem identity, deduplication, depth/fan-out bounds, and deterministic result policy remain necessary.

### Granularity and overhead

Suppose a task contains useful work `g` and incurs overhead `h` for creation, queue, scheduling, and join. Useful fraction in the simplest model is `g/(g+h)`. When `g` approaches `h`, efficiency collapses. Real `h` varies with contention, allocation, locality, runtime, and task structure.

Coarsening combines items, reducing task count and synchronization. It can improve vectorization/cache locality and reduce result partials. It also raises maximum indivisible cost, skew tail, retained bytes per task, and time between cancellation checks.

Fine grain increases scheduler choice and fault isolation but increases metadata, queue traffic, steals, closure captures, and partial results. Choose a range where tasks outnumber workers enough to absorb expected variance without creating runaway overhead.

### Overdecomposition

Exactly `P` partitions leave no scheduling flexibility: one slow partition controls completion. Creating `kP` logical units lets idle workers take additional work. The useful `k` depends on variance and overhead; it is not always large.

Overdecomposition also supports heterogeneous workers because faster workers consume more units. Yet partitions too small can destroy locality or require repeated setup. Affinity hints, locality-aware queues, or larger steal units can preserve placement.

Bound the number of outstanding units. Lazy generation/recursive spawning keeps a frontier rather than materializing every possible task. Admission/backpressure applies to parallel runtimes too.

### Cutoffs and adaptive grain

Recursive algorithms stop spawning below a cutoff. Loop frameworks choose chunk size. Streaming pipelines batch items. Each is a granularity control with different lifecycle semantics.

A cutoff is a performance hypothesis constrained by correctness/resource bounds. It can depend on input size/cost class, runtime worker availability, device, or measured throughput. Adaptive policies need hysteresis/stability, hard minimum/maximum, observability, and deterministic semantic results despite different partition trees.

Do not put unvalidated autotuning on safety-critical result paths without governance. Cache learned thresholds by hardware/software/workload identity and invalidate them when assumptions change.

### Locality and memory hierarchy

Spatial locality favors contiguous data; temporal locality favors keeping repeated accesses on one worker/cache. Partition working sets to fit relevant cache levels when computation permits. Layout and tiling interact: a square tile may be geometrically balanced but strided in column-major storage.

False sharing occurs when workers own different words in one coherence line. Align boundaries/pad hot per-partition state or assign whole lines. Padding can increase footprint and cache pressure; verify architecture and allocation.

NUMA locality favors allocation near the worker that uses data. First-touch placement, explicit allocation, and affinity can help. Dynamic migration trades balance for remote access; measure remote bytes and migrations, not just idle time.

### Heterogeneous partitioning

CPUs, GPUs, accelerators, and remote nodes have different throughput, memory, capabilities, and transfer costs. Equal item counts are rarely appropriate. Map work by estimated completion including staging, launch, synchronization, and return.

GPU grain includes grid/block dimensions and per-thread work. Too few blocks underutilize; too many/tiny blocks add scheduling/launch costs. Register/shared-memory use constrains occupancy. CPU and device partitions may require different algorithms yet must preserve one result contract.

Dynamic weighted partitioning can adjust ratios from observed rates, but delayed feedback can oscillate. Inputs may vary so yesterday's ratio fails. Bound work per device and retain a safe fallback.

### Communication-aware partitioning

Distributed partitions pay serialization, network, storage, and coordination. Minimize bytes/edges crossing boundaries while balancing compute and state. Co-locate items that communicate heavily, subject to fault-domain and hot-spot constraints.

Larger batches amortize fixed RPC/storage overhead but increase latency, retry scope, duplicate work, and memory. A failed 1-GiB partition is expensive to replay; smaller checkpoints improve recovery at overhead.

Data placement can be more important than CPU balance. Moving computation to data may beat even worker loads. Record partition-to-location provenance and distinguish durable data ownership from transient compute assignment.

### Dynamic repartitioning

Skew and drift can require split, merge, or migration. Repartitioning is a state transition, not an array reassignment. Stop/route new work, snapshot or version state, transfer, validate, update authority/routing atomically, drain old ownership, and reclaim only after readers/requests no longer depend on it.

Concurrent migration needs epochs, leases, forwarding, or dual-read/write reconciliation. Duplicate and missing processing are correctness concerns. Metrics should show current owner, movement bytes/time, stale routing, and pending cleanup.

For pure finite computation, stealing a not-yet-started task is simpler because no mutable state has committed. Once processing/effects begin, migration becomes cancellation/retry/lease semantics.

### Failure, cancellation, and progress

Partition size controls failure blast radius and retry cost. One enormous unit can repeatedly fail near completion; extremely small units multiply checkpoint/commit overhead. Stable partition and item identity supports deduplication and exact terminal accounting.

Cancellation is observed at partition checkpoints. Bound worst-case uninterruptible work/time. Splitting mutable in-place work may leave partial state; use owned candidates plus commit, or define prefix/partial validity.

A partition holding a lock, connection, or memory permit while waiting to enqueue children can deadlock downstream. Release peer-needed resources before blocking and include resources in the wait graph.

### Verification and tuning evidence

Structural tests assert coverage, disjointness, stable IDs, halo version, migration transitions, and result equivalence for empty/small/remainder/maximum/skewed inputs. Property tests generate partition counts and reconstruct the domain. Fault injection fails before/during/after ownership transfer.

Cost tests use synthetic uniform, clustered, periodic, heavy-tail, hot-key, expanding, and adversarial distributions. Compare maximum load, variance/quantiles, steals, queue delay, migration, communication, cache/NUMA, memory high-water, cancellation latency, and recovery.

Benchmarks record hardware/topology, runtime/version, workers, policy, cutoff/chunk, input distribution, task count, bytes, warm-up, repetitions, uncertainty, and verified output. Sweep grain rather than test one point. Retain a sequential baseline and identify the break-even region, not a universal optimum.

## Definitions and Notation

Let domain `D` contain items with nonnegative modeled costs `c_i`; total `W=sum_i c_i`. `P` is resource count. Partition assignment `A_j` has load `L_j=sum_{i in A_j}c_i` and ideal average `W/P` when `P>0`.

Idealized assignment makespan is `C_max=max_j L_j`. Lower bound is `LB=max(W/P,max_i c_i)`. Imbalance factor is `beta=C_max/(W/P)` for nonempty `W`; assignment efficiency is `eta=W/(P*C_max)`.

Partitions cover when `union_j A_j=D`; exclusive ownership requires pairwise disjointness. Replicated or halo elements carry read/write and epoch/merge contracts rather than satisfying exclusive disjointness.

In a simplified constant-overhead model with `q` tasks and overhead `h` each, overhead work is `q*h`. This model excludes contention, cache, communication, and variable runtime costs.

For a geometric partition, surface-to-volume is `S/V` at a named boundary representation; it approximates communication opportunity but not actual bytes, latency, or topology.

## Mechanisms, Invariants, or Proof Structure

Audit partitioning and grain in this order:

1. define domain, stable item/partition identity, mutable ownership, and result semantics;
2. prove coverage, disjointness or overlap/halo replication and merge rules;
3. estimate cost vectors and identify skew, hot keys, expansion, and indivisible items;
4. choose block/cyclic/hash/range/geometric/graph/recursive policy from locality/communication;
5. compute total, ideal load, maximum assignment load, imbalance, and lower bounds;
6. select overdecomposition and grain from overhead, balance, locality, memory, and cancellation;
7. map partitions to cache/NUMA/device/storage/network placement with one resource budget;
8. bound tasks, live frontier, metadata, scratch, retained bytes, output, retries, and logs;
9. specify migration/repartition epochs, routing authority, reconciliation, and reclamation;
10. define failure, retry, cancellation checkpoint, partial commit, and shutdown semantics;
11. test structural invariants and adversarial cost distributions; and
12. sweep policies/grain on recorded environments while preserving a sequential semantic oracle.

The executable model compares equal-count contiguous blocks with deterministic largest-cost-first greedy assignment across three abstract workers.

<!-- bijux-verify: {"id":"weighted-partition-granularity-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"costs=[9, 8, 7, 6, 5, 4, 3, 2, 1]\ncontiguous_loads=[24, 15, 6]\ngreedy_partitions=[[9, 4, 3], [8, 5, 2], [7, 6, 1]]\ngreedy_loads=[16, 15, 14]\ntotal_work=45\nideal_load=15.0\ncontiguous_makespan=24\ngreedy_makespan=16\nimbalance=1.067\ncoverage=True\nunique=True\n","stderr":""}} -->
```python
costs = [9, 8, 7, 6, 5, 4, 3, 2, 1]
worker_count = 3
contiguous = [costs[0:3], costs[3:6], costs[6:9]]
contiguous_loads = [sum(partition) for partition in contiguous]

greedy_partitions = [[] for _ in range(worker_count)]
greedy_loads = [0 for _ in range(worker_count)]
for cost in sorted(costs, reverse=True):
    target = min(range(worker_count), key=lambda index: (greedy_loads[index], index))
    greedy_partitions[target].append(cost)
    greedy_loads[target] += cost

assigned = [cost for partition in greedy_partitions for cost in partition]
total_work = sum(costs)
ideal_load = total_work / worker_count

print(f"costs={costs}")
print(f"contiguous_loads={contiguous_loads}")
print(f"greedy_partitions={greedy_partitions}")
print(f"greedy_loads={greedy_loads}")
print(f"total_work={total_work}")
print(f"ideal_load={ideal_load}")
print(f"contiguous_makespan={max(contiguous_loads)}")
print(f"greedy_makespan={max(greedy_loads)}")
print(f"imbalance={max(greedy_loads) / ideal_load:.3f}")
print(f"coverage={sorted(assigned) == sorted(costs)}")
print(f"unique={len(assigned) == len(set(assigned))}")
```

Limitations: costs are unique scalar estimates; the greedy algorithm runs sequentially with complete foreknowledge and models identical workers, zero dependencies, zero scheduling/communication/migration/cache cost, and indivisible tasks. It does not establish optimality, real parallel performance, ownership transfer, fault tolerance, cancellation, NUMA/device behavior, or safety.

## Alternatives and Trade-Offs

**One partition per worker** minimizes scheduling but cannot rebalance; **overdecomposition** exposes flexibility at metadata/locality cost.

**Contiguous blocks** preserve locality/ranges; **cyclic/block-cyclic** spread patterned costs with striding/fragmentation.

**Hash partitioning** balances/co-locates equal keys; **range partitioning** preserves order/scans; both need skew and resize policy.

**Static weighted assignment** uses predictions and stable placement; **dynamic queues/stealing** respond to actual cost with runtime overhead and migration.

**Fine grain** improves balance/cancellation/fault isolation; **coarse grain** amortizes setup and communication while increasing tails.

**Geometric tiling** improves locality but needs halos; **graph partitioning** targets cut cost but is expensive/heuristic.

**Affinity/local placement** reduces data movement; **free migration** uses idle workers but can pay cache/NUMA/network costs.

**Adaptive tuning** follows workload drift; **fixed governed thresholds** improve repeatability and operational review.

## Failure Modes and Misconceptions

- “Divide `n` by `P`.” Count does not imply cost or locality balance.
- “Partitions are scheduling chunks only.” They often encode mutable ownership and recovery identity.
- “Exactly P partitions uses P processors efficiently.” One straggler leaves no alternate work.
- “More partitions always balance better.” Overhead, memory, communication, and locality can dominate.
- “One element per task maximizes parallelism.” It can maximize bookkeeping.
- “A measured cutoff is universal.” Runtime, hardware, input, and objectives change it.
- “Hashing removes skew.” A hot equal key still maps to one owner.
- “Cyclic is balanced.” Periodic costs matching the stride can be worse.
- “Equal loads imply equal time.” Dependencies and resource contention remain.
- “Halo data is harmless duplication.” Epoch and update ownership must be exact.
- “Stealing a task migrates state safely.” Started/effecting work needs a protocol.
- “NUMA affinity always wins.” It may preserve locality while leaving capacity idle.
- “Repartition means change a routing table.” State, in-flight work, epochs, and reclamation must move safely.
- “Large batches improve throughput without cost.” Latency, retry blast radius, and memory grow.
- “Task metadata is negligible.” Millions of closures/futures can exhaust memory before work starts.

## Worked Examples

### Example 1

An array of 10 elements split into three balanced blocks can use `[0,4)`, `[4,7)`, `[7,10)`. The ranges cover once and sizes differ by one. If element costs cluster at the start, correctness remains but balance does not.

### Example 2

Costs `[9,8,7,6,5,4,3,2,1]` in three equal-count contiguous blocks load 24,15,6. Largest-first greedy loads 16,15,14. This reduces modeled makespan but scatters original order; if data reads are sequential, movement/locality may offset the gain.

### Example 3

A sparse matrix partitions equal row counts, but one row contains half the nonzeros. Balance by nonzero estimates, split the heavy row with a reduction if semantics permit, or use dynamic row blocks. Row count was the wrong cost metric.

### Example 4

Stencil tiles shrink from 128x128 to 8x8. More tasks expose balance, but halos/boundaries grow relative to interiors and synchronization explodes. Choose tile shape from cache, vector layout, boundary bytes, topology, and available work; version every halo epoch.

### Example 5

One task per log byte creates millions of tasks whose useful work is a comparison. Batch contiguous byte ranges with overlap sufficient for record boundaries, then reconcile boundary records once. Bound batch bytes and preserve source offsets.

### Example 6

A hash partition spreads ordinary customers but one tenant owns 60% of traffic. Splitting by tenant violates its ordered ledger. Preserve one authority and shed/scale within that protocol, or introduce subkeys plus a proved ordered merge; balance cannot silently weaken transactions.

### Example 7

CPU and GPU split equal image tiles. GPU compute is faster but each tile pays transfer/launch, so equal counts leave CPU/GPU imbalanced. Estimate end-to-end completion, batch GPU tiles, retain data on device, and adapt within bounded ratios while preserving indexed output.

### Example 8

A migration changes key routing before state transfer completes. New requests see empty state while old in-flight updates hit prior owner. Use epochs/leases, snapshot plus change log, cutover authority, forwarding or rejection, validation, drain, and delayed reclamation.

### Example 9

A recursive search eagerly materializes ten million future nodes. Memory fails before execution. Generate children lazily under an outstanding-work budget, use a bounded deque/frontier, deduplicate identities, and make termination/cancellation settle discovered nodes.

### Example 10

An electrical-grid protection analysis partitions simulation contingencies by estimated compute cost and treats balanced runtime as proof of operational adequacy. Partition balance says nothing about model coverage or physical safety. Named power-systems, protection/control, numerical, real-time, cybersecurity, human-factors, operations, quality, verification, and regulatory reviewers must approve contingency completeness, models, thresholds, timing, fault behavior, validation evidence, standards, and residual risk. This chapter cannot authorize grid operation.

## Cross-Program Connections

- **Algorithms:** bin packing, scheduling, graph partitioning, space-filling curves, and divide-and-conquer guide decomposition.
- **Data structures:** arrays, trees, graphs, sparse formats, and ownership layouts constrain legal cuts.
- **Computer architecture:** caches, cache lines, NUMA, accelerators, and bandwidth make placement part of cost.
- **Operating systems:** affinity, queues, preemption, and migration affect locality and balance.
- **Distributed systems:** sharding, consistent hashing, leases, epochs, and rebalancing extend ownership across failures.
- **Data engineering:** partitions, skew, shuffle, range scans, hot keys, and batch sizes dominate jobs.
- **Cloud/platform engineering:** autoscaling, quotas, instance heterogeneity, and data locality change mapping.
- **Reliability:** stable IDs, bounded retries, checkpoint grain, migration reconciliation, and cleanup control blast radius.
- **Security:** adversarial skew/expansion and tenant isolation require quotas independent of average balance.
- **Performance:** grain sweeps, break-even, cache/NUMA, communication, and tail load make hypotheses falsifiable.

## References

1. I. Foster. “Designing and Building Parallel Programs.” Addison-Wesley, 1995. <https://www.mcs.anl.gov/~itf/dbpp/>.
2. G. Karypis and V. Kumar. “A Fast and High Quality Multilevel Scheme for Partitioning Irregular Graphs.” SIAM Journal on Scientific Computing 20(1), 1998. <https://doi.org/10.1137/S1064827595287997>.
3. B. Hendrickson and R. Leland. “A Multilevel Algorithm for Partitioning Graphs.” Sandia National Laboratories, 1995. <https://www.osti.gov/biblio/10115003>.
4. OpenMP Architecture Review Board. “OpenMP API Specification 6.0.” November 2024. <https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-6-0.pdf>.
5. Intel oneAPI Threading Building Blocks. “Controlling Chunking.” <https://uxlfoundation.github.io/oneTBB/main/tbb_userguide/Controlling_Chunking_os.html>.
6. Intel oneAPI Threading Building Blocks. “Partitioner Summary.” <https://uxlfoundation.github.io/oneTBB/main/tbb_userguide/Partitioner_Summary.html>.
7. Rayon Project. “ParallelIterator: with_min_len and with_max_len.” <https://docs.rs/rayon/latest/rayon/iter/trait.IndexedParallelIterator.html>.
8. NVIDIA. “CUDA C++ Best Practices Guide.” <https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html>.
9. MPI Forum. “MPI 4.1 Standard.” 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf>.
10. METIS Project. “METIS: Serial Graph Partitioning and Fill-reducing Matrix Ordering.” <https://karypislab.github.io/METIS/>.

## Exercises

### Exercise 1

Partition `[0,17)` into four balanced contiguous blocks. Prove coverage/disjointness and identify behavior when workers exceed elements.

### Exercise 2

For costs `[12,11,7,6,5,4,3]` and three workers, compute equal-count contiguous loads and a deterministic largest-first greedy assignment. Compare lower bound and imbalance without claiming optimality.

### Exercise 3

Design tiles and halos for a two-dimensional five-point stencil. Specify epochs, boundary ownership, communication, grain hypotheses, and correctness tests.

### Exercise 4

Specify a safe dynamic split/migration protocol for a hot range partition with in-flight requests and retryable effects.

### Exercise 5

A railway interlocking verifier partitions scenarios evenly and meets throughput targets. Explain why this is insufficient for deployment and define required human evidence.

## Answers to the Exercises

### Answer 1

Using quotient four and remainder one, assign sizes `[5,4,4,4]`: `[0,5)`, `[5,9)`, `[9,13)`, `[13,17)`. Adjacent endpoints meet, starts are nondecreasing, union is `[0,17)`, and no index lies in two half-open ranges. General tests include zero and overflow-safe formulas. When `P>n`, use `n` singleton nonempty partitions plus explicit empty partitions only if the API supports them, or create only `n` logical units; do not compute zero chunk size and loop forever.

### Answer 2

Contiguous equal-count grouping might use `[12,11,7]`, `[6,5]`, `[4,3]`, loads 30,11,7. Total is 48, ideal 16, largest-item lower bound 12, so lower bound is 16 and imbalance factor is `30/16=1.875`. Largest-first greedy assigns 12 to worker 0, 11 to 1, 7 to 2, then 6 to 2 (13), 5 to 1 (16), 4 to 0 (16), and 3 to 2 (16): loads 16,16,16, meeting the lower bound in this scalar model. It may sacrifice input locality and does not prove real optimality with communication/resources.

### Answer 3

Partition output cells into disjoint rectangular interiors. For epoch `t`, each tile reads immutable grid `t`, including one-cell halo above/below/left/right, and writes only its interior in grid `t+1`. Physical boundaries have explicit fixed/periodic/domain policy; corner accesses are defined. Exchange/copy halos tagged with epoch and begin only after neighbor `t` data is complete; never mix epochs. Sweep tile shapes against cache/vector layout, halo bytes, task overhead, skew, and worker supply. Tests reconstruct complete coverage, assert no overlapping writes, compare sequential oracle, check small/nondivisible grids/boundaries, and inject delayed/missing/wrong-epoch halos.

### Answer 4

Create a new routing epoch and child range identities while old owner remains authoritative. Stop or journal new mutations at a cut, snapshot state, transfer with digest/version, replay ordered changes/effects by stable operation ID, and validate. Atomically publish new epoch/ranges; clients with stale epoch are forwarded or rejected/retried under one policy. Drain old in-flight requests, reconcile duplicates, retain tombstone/forwarding until leases expire, then reclaim. Bound migration bytes/time/log, preserve per-key ordering, expose status, and roll back before cutover if validation fails.

### Answer 5

Even scenario counts and throughput do not prove complete hazard coverage, correct interlocking models, independence, worst-case timing, or safe physical state. Production requires named railway signalling/interlocking, systems, safety, real-time, software, hardware, cybersecurity, human-factors, operations, quality, independent verification, and regulatory reviewers; requirements/hazard traceability; applicable-standard assessment; scenario/model completeness and provenance; independent formal/model review; worst-case timing, saturation, fault-injection, hardware-in-the-loop, failover/recovery, environmental, and operational evidence; and signed residual-risk acceptance. This answer is not deployment authorization.
