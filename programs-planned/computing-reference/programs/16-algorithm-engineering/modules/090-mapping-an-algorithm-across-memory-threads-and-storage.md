---
module_id: ALGE-090
program: Algorithm Engineering
level: 2
module_number: 90
title: Mapping an Algorithm Across Memory, Threads, and Storage
status: complete
last_verified: 2026-09-05
---

# Mapping an Algorithm Across Memory, Threads, and Storage

## One-Page Review

### Governing question

How do we turn one correct abstract algorithm into an executable plan whose work, dependencies, working sets, ownership, communication, storage traffic, recovery, and measurements agree with a real deployment?

### Essential definitions

- A **computational DAG** has operations as vertices and required precedence as edges.
- **Work** $T_1$ is total operation cost; **span** $T_\infty$ is the longest dependency-path cost.
- A **working set** is live data at a named phase and hierarchy boundary, including replicas, buffers, metadata, and temporaries.
- **Partitioning** assigns logical data/work; **placement** maps it to addresses, memory domains, workers, devices, or services.
- An **owner** has authority to mutate or publish an output; replicas need a reconciliation rule.
- **Operational intensity** is useful operations per byte moved at a specified boundary.
- A **bottleneck lower bound** is a necessary time implied by one resource ceiling, not a complete runtime prediction.

### Central model, mechanism, or theorem

For $P$ processors, any execution needs at least

$$
T_P\ge\max(T_1/P,T_\infty).
$$

If a plan must move $D_m$ memory bytes through sustainable bandwidth $\beta_m$ and $D_s$ storage bytes through $\beta_s$, then an optimistic combined lower bound is

$$
T\ge\max\!\left(\frac{T_1}{P\rho},\frac{T_\infty}{\rho},\frac{D_m}{\beta_m},\frac{D_s}{\beta_s}\right),
$$

where $\rho$ is a compatible per-worker operation rate. The maximum assumes perfect overlap and no contention; summing assumes serialization. Real time lies behind a resource schedule, so both are bounds or scenarios, not predictions. Mapping improves a plan by changing locality, parallelism, placement, or dataflow while preserving semantics.

### Critical invariants

- Every required operation executes once, or repeated execution is reconciled under an explicit idempotence/exactly-once policy.
- Dependencies are respected; no consumer observes an incomplete producer result.
- Each mutable output has exclusive ownership, atomic updates, or a proved reduction.
- Aggregate live state fits capacity after multiplying per-task buffers and replicas by concurrency.
- Transfers preserve identity, order, checksums, and snapshot/version where required.
- Durable publication occurs only after all reachable state meets the promised durability.
- Metrics name boundaries and do not mix operations, cache lines, memory bytes, storage bytes, messages, or elapsed time.

### Common failures

Parallelizing a memory-bound loop and expecting linear speedup; fitting one task while overcommitting $P$ tasks; partitioning by item count instead of work/bytes; ignoring NUMA first touch and false sharing; choosing tiny tasks whose scheduling exceeds useful work; spilling without counting read/write amplification; overlapping phases that compete for the same bandwidth; assuming work stealing preserves locality; treating peak compute or device bandwidth as sustainable application bandwidth; publishing before flush; and tuning from one unrepresentative input.

### Compact example

A plan with 8 billion operations on eight workers at 2 billion operations/s each, 1.2 billion-operation span, and 120 GB memory traffic at 40 GB/s has lower-bound components 0.5 s, 0.6 s, and 3 s. Memory movement is the largest modeled lower bound. That does not predict a three-second run; it identifies where an optimization must act before extra threads can help.

### Connections

[ALGE-081](./081-work-span-and-parallel-dependency.md) supplies work/span, [ALGE-085](./085-external-memory-cost-models.md) supplies transfer models, [ALGE-087](./087-blocked-matrix-and-graph-algorithms.md) supplies blocking, [ALGE-088](./088-cache-oblivious-design.md) supplies recursive locality, and [ALGE-089](./089-i-o-efficient-search-and-index-construction.md) supplies persistent page construction. ALGE-091 next develops representative workloads.

## Governing Question

Given a proved algorithm, workload distribution, machine topology, memory and storage hierarchy, concurrency and failure model, and service objective, which decomposition, layout, ownership, schedule, and publication protocol forms the simplest plan whose correctness and performance claims can be defended?

## Why This Matters

Algorithm analysis often stops at work and asymptotic space. Production execution cannot. The same $O(N)$ scan may be one contiguous stream, many random page reads, or remote requests. The same parallel reduction may use private cache-resident accumulators or a contended shared atomic. The same external sort may exploit sequential devices or overload one path. Mapping is the bridge from an abstract computation to resource-specific behavior.

This bridge is not a bag of optimizations. It is a refinement process. Start with semantics and a dependency graph. Identify data objects and lifetimes. Partition work and data together. Assign owners and placement. Schedule transfers and computation. Add recovery and publication. Only then evaluate against resource ceilings and measurements.

The deepest trade-offs cross boundaries. Replication can remove reads but consume memory and require reconciliation. Larger tasks improve locality and amortize scheduling but reduce load balance. More concurrent I/O can hide latency until it saturates bandwidth or queues. Spill reduces capacity pressure but adds durable bytes and failure states. No single model captures all of this, so evidence must remain layered and conditional.

## Prerequisites and Retrieval

Retrieve proof obligations from [ALGE-002](./002-preconditions-postconditions-and-correctness.md), evidence design from [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md), work/span and scheduling from [ALGE-081](./081-work-span-and-parallel-dependency.md), memory/concurrency reasoning from [ALGE-082](./082-parallel-prefix-and-reduction.md), external transfer accounting from [ALGE-085](./085-external-memory-cost-models.md), blocking from [ALGE-087](./087-blocked-matrix-and-graph-algorithms.md), and cache-oblivious and index designs from [ALGE-088](./088-cache-oblivious-design.md) and [ALGE-089](./089-i-o-efficient-search-and-index-construction.md).

## Learning Objectives

After this module, you should be able to:

1. convert an algorithm into a computational DAG, data-lifetime graph, and phase plan;
2. derive work/span, capacity, bandwidth, storage, and optimistic bottleneck bounds;
3. distinguish partitioning, placement, scheduling, ownership, replication, and publication;
4. choose task and block granularity using locality, balance, overhead, and recovery costs;
5. diagnose memory bandwidth, NUMA, cache coherence, storage, queueing, and tail-latency limits;
6. design spill, checkpoint, retry, and atomic publication protocols;
7. compare alternative mappings without double-counting overlap or mixing boundaries; and
8. build a measurement plan that can falsify the proposed bottleneck explanation.

## Core Exposition

### Begin with semantics and the computational DAG

List input snapshot, output, comparator or algebra, numeric policy, ordering, duplicate behavior, and failure guarantees. Express operations and dependencies as a DAG. The DAG constrains legal schedules but does not decide where data lives. Two mappings of the same DAG may have identical work and radically different communication.

Let $T_1$ sum operation costs and $T_\infty$ be the heaviest dependency path. The lower bound $T_P\ge\max(T_1/P,T_\infty)$ follows because $P$ workers perform at most $P$ units per unit time and the critical path cannot be shortened by executing independent work. Greedy-scheduling and work-stealing results provide stronger qualified guarantees for structured computations [1]; arbitrary blocking, I/O, contention, or failure does not inherit them automatically.

### Add a data-lifetime graph

For each object, record creator, readers, mutator/owner, size distribution, layout, first and last use, persistence, replication, and version. This reveals peak capacity and transfer opportunities. A buffer that is small per task can dominate after multiplying by worker count, pipeline depth, and retry replicas.

Distinguish immutable inputs, mutable partials, durable checkpoints, and published outputs. Immutable partitions are easy to share. Mutable destinations need ownership or synchronization. Durable objects need identity, checksum, and lineage. Reusing a buffer safely depends on the last consumer, not merely the producer’s completion.

### Partition work and data together

Partitioning only work can leave all workers contending for the same data. Partitioning only data can produce uneven work. Choose units that expose parallelism, reuse resident data, balance expected cost, and align with recovery boundaries. Weight units by operations, bytes, active edges, expected skew, or measured time—not just item count.

Static partitioning minimizes scheduling overhead and preserves affinity when costs are predictable. Dynamic queues and work stealing adapt to skew but move tasks away from data, expand cache footprints, and make execution order less reproducible. Hybrid schemes assign coarse locality domains statically and balance within them dynamically.

### Choose granularity

Let useful work per task cost $g$ seconds and scheduling/coordination cost $o$. To keep overhead below fraction $\epsilon$, require $o/(g+o)\le\epsilon$, or $g\ge o(1-\epsilon)/\epsilon$. This is necessary but not sufficient: large tasks can reduce parallel slack and worsen tails.

Granularity also controls working set and failure replay. A large block offers reuse and sequential transfer but monopolizes memory and makes retries expensive. A small block balances well but adds descriptors, queues, fences, partial outputs, and requests. Sweep sizes around model-derived candidates rather than selecting a folklore constant.

### Map the memory hierarchy

For every hot phase, write a byte balance: compulsory input/output, capacity reloads, coherence transfers, packed copies, temporary writes, and allocator metadata. Operational intensity $I=W/D_m$ relates useful work $W$ to memory bytes $D_m$ at a specified boundary. A Roofline-style ceiling is

$$
R\le\min(R_{peak},I\beta_m),
$$

where $R$ is operation rate, $R_{peak}$ a compatible compute ceiling, and $\beta_m$ sustainable bandwidth [2]. This identifies a ceiling, not achieved performance.

Use [ALGE-087](./087-blocked-matrix-and-graph-algorithms.md) to increase reuse explicitly or [ALGE-088](./088-cache-oblivious-design.md) to expose many scales recursively. Include cache associativity, TLB reach, alignment, packing, and concurrent working sets before claiming fit.

### Place across NUMA domains

On a nonuniform-memory machine, access cost depends on which domain owns physical pages. First-touch allocation, thread pinning, migration, and interleaving policy affect placement. Partition data so the common owner initializes and consumes it locally. Replicate read-mostly state only when memory cost and update protocol are acceptable.

False sharing occurs when independent mutable fields share a coherence line. Logical disjointness does not prevent line bouncing. Align or pad per-worker state, batch updates, or use private partials and a reduction. Measure remote bytes and coherence events where reliable; thread count alone cannot diagnose NUMA behavior.

### Map threads and dependencies

Choose exclusive ownership when possible. For reductions, compare atomics, locks, per-worker partials, tree reductions, and owner-routed messages. State algebraic properties: associativity and commutativity may permit reorder; idempotence may permit duplicate attempts; floating-point addition is not exactly associative.

Bounded queues enforce capacity and backpressure. Unbounded task or result queues turn transient skew into memory exhaustion. Pipeline stages need explicit rates and buffer limits. Increasing stage concurrency can worsen end-to-end time when stages share memory bandwidth or storage queues.

Work stealing is effective for qualified fully strict computations, with expected time near work-per-processor plus span under the analyzed scheduler [1]. It can still lose locality, grow space, and conflict with NUMA placement. Preserve task affinity or steal coarse units when data movement is expensive.

### Map storage

If live state exceeds memory or must survive failure, define spill units, file/object layout, buffering, checksums, and deletion. Sequential runs and batched pages amortize request overhead. Random small writes often need logging, copy-on-write, buffering, or merge structures.

Count storage bytes read and written, not merely logical input. External sorting writes initial runs and each merge pass. LSM compaction rewrites levels. Compression changes bytes and CPU; its expansion bound matters for buffers. Direct I/O, buffered I/O, memory mapping, and remote object access have different alignment, caching, and durability semantics.

The external-memory model [3] and red-blue pebble framework [4] provide transfer lower bounds under explicit assumptions. These bounds rule out impossible movement targets but do not predict queue depth, latency, device firmware, filesystem behavior, or cloud-service throttling.

### Combine lower bounds carefully

For a candidate plan, compute separate ideal components: compute work, span, memory traffic, storage traffic, network traffic, and serialization. If resources could overlap perfectly, their maximum is a lower bound. If phases are provably serialized, sum those phase bounds. If resources contend—for example, storage DMA and computation share memory bandwidth—neither naive maximum nor sum is exact.

The executable reference below compares three hypothetical plans with the optimistic maximum. It is a screening model, not a simulator.

<!-- bijux-verify: {"id":"mapping-bottleneck-reference","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"resident-blocked: 3.00 s, memory\nstorage-streaming: 10.00 s, storage\noverdecomposed: 6.00 s, memory\nselected lower bound: resident-blocked\n","stderr":""}} -->
```python
def optimistic_bound(plan, workers, operation_rate, memory_bandwidth, storage_bandwidth):
    name, work, span, memory_bytes, storage_bytes = plan
    components = [
        (work / (workers * operation_rate), "work"),
        (span / operation_rate, "span"),
        (memory_bytes / memory_bandwidth, "memory"),
        (storage_bytes / storage_bandwidth, "storage"),
    ]
    seconds, bottleneck = max(components)
    return name, seconds, bottleneck


plans = [
    ("resident-blocked", 8e9, 1.2e9, 120e9, 0),
    ("storage-streaming", 8e9, 1.0e9, 60e9, 20e9),
    ("overdecomposed", 10e9, 0.8e9, 240e9, 0),
]
bounds = [optimistic_bound(plan, 8, 2e9, 40e9, 2e9) for plan in plans]
for name, seconds, bottleneck in bounds:
    print(name + ":", format(seconds, ".2f"), "s,", bottleneck)
print("selected lower bound:", min(bounds, key=lambda item: item[1])[0])
```

The result says only that `resident-blocked` has the smallest stated lower bound under these compatible units and assumptions. It does not prove feasibility, overlap, or observed superiority.

### Design capacity and backpressure

Peak memory is a schedule property. Sum immutable resident inputs, outputs, per-worker scratch, in-flight I/O, queues, replicas, runtime overhead, and reserve. A theoretical scheduler may use $P$ times serial space for structured work [5]; a real design must calculate actual objects.

Use bounded admission. Before launching a task, reserve its worst credible buffer and output footprint. Release on a defined lifecycle event. If variable records can exceed bounds, stream them, store payload out of line, or reject them. Backpressure must propagate to producers rather than moving overload into another queue.

### Add failure and publication

Choose retry units aligned with immutable inputs and independently verifiable outputs. A retry can be at-least-once if outputs use unique identities and idempotent publication; otherwise duplicates must be detected. Exactly-once effects usually require transactional state or deduplication, not a scheduler promise.

Checkpoint only states from which dependencies and ownership can be reconstructed. Make output bytes durable, verify checksum/count/schema, then publish metadata that makes them reachable. Do not delete predecessors until the successor and lineage record meet the required durability. On restart, trust committed identities, not leftover filenames.

### Build a falsifiable performance plan

Predict which resource limits each workload region and what observation would disprove it. If memory bandwidth is limiting, adding workers should saturate, operational intensity should be low, and blocking that reduces measured bytes should help. If span limits, work may be balanced yet critical-path idle time remains. If storage limits, device throughput/queue metrics and spill bytes should correlate with time.

Benchmark representative sizes, distributions, skew, and failure states. Record toolchain, machine, topology, affinity, frequency policy, memory placement, device/filesystem, cache state, input identity, repetitions, and uncertainty. Use end-to-end time plus per-phase metrics. A counter supports a mechanism only if event semantics and attribution are credible.

## Definitions and Notation

Let $T_1$ be work, $T_\infty$ span, $P$ workers, $S_1$ serial space, $G$ task granularity, $D_m,D_s,D_n$ bytes moved at memory, storage, and network boundaries, and $\beta_m,\beta_s,\beta_n$ sustainable bandwidths. Let $R_{peak}$ be compatible peak operation rate and $I=W/D$ operational intensity at one named boundary.

A **mapping** assigns DAG vertices and data objects to resources and times. **Affinity** prefers a task-resource relationship. **Backpressure** bounds upstream production when downstream capacity is exhausted. **Spill** moves live/intermediate state to a slower tier. **Checkpoint** is a validated recoverable state. **Publication** makes a result discoverable under a visibility contract.

## Mechanisms, Invariants, or Proof Structure

### Refinement proof obligations

1. Show task decomposition covers every abstract operation and preserves dependencies.
2. Show partition and placement preserve data identity and required order.
3. Show each mutation is exclusive, atomic, or part of a valid reduction.
4. Show buffers and queues remain within aggregate capacity for every legal schedule.
5. Show retry/replay cannot create an ungoverned duplicate effect.
6. Show published metadata reaches only complete durable objects.

### Lower-bound discipline

Work, span, movement, and serialization bounds are necessary conditions. The maximum of simultaneously overlap-capable components is optimistic. A sum is justified only across nonoverlapping phases or resources that cannot operate concurrently by design. Measured time below a claimed lower bound signals inconsistent units, boundaries, rates, or traffic estimates—not a faster-than-proof system.

### Measurement invariant

Every reported metric binds to module/implementation revision, input identity, machine and topology, tool version, command/configuration, repetitions, and boundary. Derived ratios record numerator and denominator. Missing or multiplexed counters are labeled; a successful run proves only observed behavior.

## Alternatives and Trade-Offs

| Decision | Benefit | Cost or risk | Evidence |
|---|---|---|---|
| static partitions | locality and low overhead | skew and stragglers | per-owner work distribution |
| dynamic work stealing | adapts to uneven work | locality loss and steals | steal count, remote bytes, tails |
| fine tasks | parallel slack and cheap retry | scheduling and metadata | task-time distribution |
| coarse tasks | reuse and amortization | imbalance and memory peaks | concurrency and resident bytes |
| shared atomics | simple direct updates | contention and order variance | collision/coherence metrics |
| private reductions | local writes | replica memory and merge | peak space and reduction time |
| spilling | bounded fast memory | storage amplification and recovery | read/write bytes and restart tests |
| replication | local reads and availability | capacity and reconciliation | replica traffic and staleness |
| pipelining | latency overlap | shared-resource contention | timeline and queue occupancy |

The best mapping may be heterogeneous: CPU orchestration, accelerator kernels, NUMA-local partitions, storage streaming, and durable merge. Every boundary needs serialization, identity, capacity, and failure semantics; otherwise performance decomposition hides correctness gaps.

## Failure Modes and Misconceptions

- **“More workers reduce $T_1/P$ indefinitely.”** Span, bandwidth, contention, and overhead remain.
- **“Each task fits, so the run fits.”** Concurrent scratch, queues, replicas, and output coexist.
- **“Balanced items mean balanced work.”** Cost and bytes can be skewed.
- **“Work stealing is locality neutral.”** A stolen task may pull remote state and expand space.
- **“Peak bandwidth belongs in the bound.”** Use compatible sustainable bandwidth for the access pattern.
- **“Maximum component time predicts runtime.”** It assumes perfect overlap and omits overhead.
- **“Summing all ceilings is conservative truth.”** Independent resources may overlap substantially.
- **“Spill solves memory pressure.”** It exchanges capacity for traffic, temporary space, and failure states.
- **“Retry gives exactly-once output.”** Effects need identity, idempotence, or transactions.
- **“One benchmark reveals the bottleneck.”** Sizes and distributions can move the limiting resource.

## Worked Examples

### Example 1

**Situation.** A computation has $T_1=120$ seconds, $T_\infty=8$ seconds, and $P=16$. What is the work/span lower bound?

**Reasoning.** Work gives $120/16=7.5$ seconds; span gives 8 seconds. The maximum is 8 seconds. Even perfect scheduling cannot go below the critical path, so theoretical parallelism $T_1/T_\infty=15$ is already below 16 workers.

**Conclusion.** The sixteenth worker cannot lower the ideal bound unless the DAG/span changes.

### Example 2

**Situation.** Each of 24 workers needs 300 MiB scratch, queues hold 2 GiB, immutable input is 8 GiB, output is 4 GiB, and reserve is 3 GiB. Does a 24 GiB host fit?

**Reasoning.** Scratch is 7.2 GiB. Total is $7.2+2+8+4+3=24.2$ GiB, already over capacity before runtime overhead. Reduce concurrency, stream state, or shrink buffers.

**Conclusion.** Per-worker feasibility does not imply aggregate feasibility.

### Example 3

**Situation.** A kernel performs 400 billion operations and moves 200 GB from memory. Sustainable bandwidth is 50 GB/s and compute ceiling is 200 billion operations/s.

**Reasoning.** Intensity is 2 operations/byte. The bandwidth ceiling is $2\cdot50=100$ billion operations/s, below compute peak. The optimistic time lower bound is at least $400/100=4$ seconds; compute alone would suggest two seconds.

**Conclusion.** Reducing bytes or increasing reuse is necessary before peak arithmetic can matter.

### Example 4

**Situation.** Scheduling costs 40 microseconds per task. Keep scheduling below 2% of task-plus-overhead time.

**Reasoning.** Require $g\ge o(1-0.02)/0.02=49o=1.96$ milliseconds of useful work. This only bounds overhead fraction; tasks may need to be smaller for balance or larger for locality.

**Conclusion.** About two milliseconds is a lower granularity candidate, not an optimum.

### Example 5

**Situation.** Eight equal item partitions contain work weights `[1,1,1,1,1,1,1,93]`.

**Reasoning.** Item counts are balanced but one partition owns 93% of 100 total work units. Static execution has a 93-unit straggler. Splitting the heavy unit may help only if its dependencies and data permit division; otherwise the span itself is large.

**Conclusion.** Weight distributions and divisibility govern balance.

### Example 6

**Situation.** Two threads update separate counters that occupy one cache line.

**Reasoning.** Logical ownership is disjoint, so there is no data race if each counter has one owner. Coherence still moves the shared line between cores on writes, causing false sharing. Padding counters to separate lines or accumulating privately can remove traffic at a memory cost.

**Conclusion.** Correctness isolation does not guarantee physical locality.

### Example 7

**Situation.** The executable model selects `resident-blocked`. Is it proven fastest?

**Reasoning.** No. Three seconds is the largest ideal component from supplied rates/bytes. The plan might exceed capacity, fail to overlap, underuse bandwidth, or pay unmodeled scheduling and synchronization. Another plan might compress data or use a different rate. The model prioritizes measurement.

**Conclusion.** A lower-bound comparison filters designs; execution evidence chooses among feasible implementations.

### Example 8

**Situation.** A pipeline reads at 3 GB/s, transforms at 5 GB/s, and writes at 2 GB/s with bounded buffers.

**Reasoning.** In steady state its throughput cannot exceed 2 GB/s because the writer is slowest. Enlarging buffers only delays backpressure and increases memory. Parallel writers help only if the storage path has unused sustainable bandwidth and ordering/durability remain valid.

**Conclusion.** Pipeline throughput is constrained by the slowest sustained stage, not the sum of rates.

### Example 9

**Situation.** A worker writes an output file, publishes its name, then records a checksum; it crashes between publication and checksum.

**Reasoning.** Readers can observe unverified bytes, and restart cannot distinguish complete output from a partial file. Write under an immutable temporary identity, close/flush to the required boundary, verify length/count/checksum, record durable metadata, then atomically publish the committed identity.

**Conclusion.** Visibility must follow validation and required durability.

### Example 10

**Situation.** Adding workers speeds a phase through eight threads, plateaus at twelve, and slows at twenty-four.

**Reasoning.** Candidate causes include memory-bandwidth saturation, NUMA remote traffic, coherence, queue contention, oversubscription, and task overhead. Measure useful work distribution, span/idle time, memory bytes/bandwidth, remote/coherence events, affinity, queues, and frequency. Repeat across working-set sizes; a cache-capacity crossing may move the plateau.

**Conclusion.** The scaling curve diagnoses nothing alone; targeted evidence discriminates mechanisms.

## Cross-Program Connections

- [Concurrent and Parallel Programming CONPAR-009](../../04-programming-languages-concurrent-and-parallel-programming/modules/009-message-passing-and-ownership-transfer.md) develops ownership transfer and message semantics.
- [Computer Architecture CA-031](../../23-computer-architecture/modules/031-locality-and-the-memory-wall.md) supplies hierarchy and bandwidth context.
- [Operating Systems OS-031](../../22-operating-systems/modules/031-address-translation.md) connects placement to pages and translation.
- [Operating Systems OS-040](../../22-operating-systems/modules/040-diagnosing-memory-pressure-and-thrashing.md) develops aggregate working-set failures.
- [Distributed Systems DIST-001](../../27-distributed-systems-engineering/modules/001-why-distribution-changes-the-problem.md) extends ownership and failure across network boundaries.
- [Systems Engineering SYSENG-040](../../26-systems-engineering/modules/040-planning-system-integration-around-interface-risk.md) frames cross-boundary integration evidence.

## References

1. Robert D. Blumofe and Charles E. Leiserson, “Scheduling Multithreaded Computations by Work Stealing,” *Journal of the ACM* 46(5), 720–748, 1999. [doi:10.1145/324133.324234](https://doi.org/10.1145/324133.324234). Checked 2026-09-05.
2. Samuel Williams, Andrew Waterman, and David Patterson, “Roofline: An Insightful Visual Performance Model for Multicore Architectures,” *Communications of the ACM* 52(4), 65–76, 2009. [doi:10.1145/1498765.1498785](https://doi.org/10.1145/1498765.1498785). Checked 2026-09-05.
3. Alok Aggarwal and Jeffrey Scott Vitter, “The Input/Output Complexity of Sorting and Related Problems,” *Communications of the ACM* 31(9), 1116–1127, 1988. [doi:10.1145/48529.48535](https://doi.org/10.1145/48529.48535). Checked 2026-09-05.
4. Jia-Wei Hong and H. T. Kung, “I/O Complexity: The Red-Blue Pebble Game,” *STOC 1981*, 326–333, 1981. [doi:10.1145/800076.802486](https://doi.org/10.1145/800076.802486). Checked 2026-09-05.
5. Robert D. Blumofe and Charles E. Leiserson, “Space-Efficient Scheduling of Multithreaded Computations,” *SIAM Journal on Computing* 27(1), 202–229, 1998. [doi:10.1137/S0097539793259471](https://doi.org/10.1137/S0097539793259471). Checked 2026-09-05.
6. John D. McCalpin, “Memory Bandwidth and Machine Balance in Current High Performance Computers,” *IEEE Computer Society Technical Committee on Computer Architecture Newsletter*, December 1995. [Author’s record](https://www.cs.virginia.edu/~mccalpin/papers/bandwidth/bandwidth.html). Checked 2026-09-05.
7. Dror Irony, Sivan Toledo, and Alexander Tiskin, “Communication Lower Bounds for Distributed-Memory Matrix Multiplication,” *Journal of Parallel and Distributed Computing* 64(9), 1017–1026, 2004. [doi:10.1016/j.jpdc.2004.03.021](https://doi.org/10.1016/j.jpdc.2004.03.021). Checked 2026-09-05.
8. Peter Sanders, Kurt Mehlhorn, Martin Dietzfelbinger, and Roman Dementiev, *Sequential and Parallel Algorithms and Data Structures: The Basic Toolbox*, Springer, 2019. [doi:10.1007/978-3-030-25209-0](https://doi.org/10.1007/978-3-030-25209-0). Checked 2026-09-05.

## Exercises

### Exercise 1

Distinguish work partitioning, data placement, task scheduling, and output ownership using a parallel matrix multiplication as the example.

### Exercise 2

A plan has $T_1=600$ core-seconds, $T_\infty=18$ seconds, $P=32$, 1.2 TB memory traffic at 60 GB/s, and 100 GB storage traffic at 2.5 GB/s. Compute the four optimistic components and lower bound, assuming compatible units and rates for work/span.

### Exercise 3

A 32-thread program is correct but becomes slower than its eight-thread version and uses four times the memory. Give a diagnosis plan that separates task overhead, span, bandwidth, NUMA, false sharing, and replicated scratch.

### Exercise 4

Compare static NUMA-local partitions with global work stealing for a skewed graph traversal. State a hybrid and the evidence needed to select it.

### Exercise 5

Design an execution map for externally sorting 4 TB on a two-socket host with limited memory and two storage devices. Include tasks, placement, capacity, ownership, pipeline/backpressure, recovery, publication, and falsifiable performance claims.

## Answers to the Exercises

### Answer 1

Work partitioning divides output tiles and reduction ranges into tasks. Data placement chooses where matrix panels, packed copies, and output tiles reside in address/NUMA/device space. Scheduling chooses when and on which worker tasks execute. Ownership determines who may mutate each output tile or how partial tiles reduce. One design can keep partitioning fixed while changing scheduling; correctness fails only when dependencies or ownership are violated, while performance may change from placement alone.

### Answer 2

Work per processor is $600/32=18.75$ seconds. Span is 18 seconds. Memory time is $1200/60=20$ seconds using decimal GB/TB as stated. Storage time is $100/2.5=40$ seconds. The optimistic maximum is 40 seconds, so storage is the largest modeled component. This is not a runtime prediction: overlap, contention, rate compatibility, and unmodeled overhead remain. A strong answer states those qualifications.

### Answer 3

Record task counts, task durations, scheduler/steal time, critical-path or idle profile, useful operations, memory bytes/bandwidth, per-domain allocations and remote traffic, coherence/line invalidations, and scratch/queue/replica bytes per worker. Pin threads and compare first-touch local, interleaved, and controlled placements. Pad suspected shared lines. Hold total work/input constant and sweep 1, 2, 4, 8, 16, 32 threads. Cap concurrency without changing partitioning to isolate replicated space. The evidence should distinguish rising overhead, bandwidth saturation, remote access, false sharing, and simple $P$-scaled scratch rather than guessing from slowdown.

### Answer 4

Static NUMA-local partitions preserve adjacency and vertex-state locality with low scheduling overhead but suffer when active edges are skewed. Global stealing balances tasks but can move them away from pages and produce remote updates. A hybrid assigns coarse vertex/edge blocks to sockets, uses local queues and stealing within a socket, and permits cross-socket steals only above a straggler threshold or for data-light tasks. Compare active work and tail per owner, steal counts, remote bytes, coherence/messages, queue idle time, memory capacity, and step/end-to-end time across graph/frontier families.

### Answer 5

Freeze input snapshot, comparator, stability, record encoding, and output durability. Partition input into memory-bounded run-generation tasks pinned so buffers are socket-local; stripe or assign runs across devices based on measured paths without concurrent oversubscription. Reserve per-worker input, sort scratch, output buffers, decoder state, and global queue capacity before admission. Runs are immutable and owned by unique IDs with counts, bounds, comparator version, and checksums. Merge tasks consume disjoint run groups, use bounded asynchronous buffers, and publish successors only after verification and required durability; backpressure stops run producers when temporary capacity or merge queues fill. Checkpoint committed lineage, retry incomplete groups from immutable predecessors, and retain old runs until successors commit. Publish the final verified run through a documented atomic metadata primitive. Predict run counts, passes, logical bytes, peak space, and per-device time; falsify with measured bytes, bandwidth, queue depth, CPU, imbalance, overlap timeline, failure injection, restart, and sorted-permutation/stability checks. Accept alternatives only when they provide equally explicit capacity, ownership, recovery, and evidence.
