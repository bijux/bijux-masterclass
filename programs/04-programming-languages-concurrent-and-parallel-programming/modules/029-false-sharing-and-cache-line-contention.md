---
module_id: CONPAR-029
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 29
title: False Sharing and Cache-Line Contention
status: complete
last_verified: 2026-08-29
---

# False Sharing and Cache-Line Contention

## One-Page Review

### Governing question

How can logically independent concurrent accesses interfere through cache-coherence granularity, and how can engineers prove the responsible layout and traffic before spending memory on separation?

### Essential definitions

- A **cache line** is a hardware-managed block transferred and tracked as a unit by a cache/coherence system.
- **Coherence** keeps participating caches' views of a memory block consistent according to the architecture.
- **True sharing** occurs when agents access the same logical datum and at least one writes.
- **False sharing** occurs when agents access different data in one coherence block and at least one writes, causing unnecessary coherence traffic.
- **Cache-line contention** is competition for a line's writable ownership or shared data, whether sharing is true or false.
- **Invalidation** removes or downgrades other cached copies after a write request under an invalidation protocol.
- **HITM** denotes a load satisfied from a line modified in another cache in common performance-counter terminology.
- **Padding/alignment** changes offsets or stride to separate destructive-sharing candidates.
- **Sharding** gives agents separate update locations and reconciles later.
- **Constructive interference** places data used together close enough to exploit locality.

### Central model, mechanism, or theorem

Map each hot address `a` to a hardware coherence block `line(a)=floor(a/B)` for measured block size `B`. If two cores repeatedly access distinct objects `x≠y` with `line(x)=line(y)` and at least one stream writes, line ownership may migrate even though the source-level objects do not share an invariant. Separating their lines can remove that traffic; it cannot remove true sharing, serial work, bandwidth limits, imbalance, or another bottleneck.

### Critical invariants

The program is already functionally race-free. Hot access streams, writer identities, addresses, offsets, and topology are measured. The coherence granule is obtained for the target rather than assumed universally. True sharing is distinguished from false sharing. Alignment includes allocation base and array stride, not only member size. Separation preserves ABI, ownership, and correctness. Memory/cache/TLB costs are counted. Thread placement and NUMA location are controlled. The same workload is measured before and after. New bottlenecks are checked.

### Common failures

Teams blame false sharing from a scaling curve alone; pad a truly shared counter; align a type but allocate an unaligned array; hard-code 64 bytes for every target; confuse read/read sharing with false sharing; weaken atomic ordering but retain ownership traffic; measure debug builds; change scheduling and layout simultaneously; ignore allocator neighbors; pad cold objects and inflate working sets; or claim success from one noisy timing run without coherence evidence.

### Compact example

Eight 8-byte per-thread counters begin at offsets 0,8,...,56 in one assumed 64-byte block. Eight writers update distinct counters, yet each write competes with seven peers for the block: 56 directed writer-peer relationships. With verified 64-byte stride and aligned base, the eight counters map to eight blocks and those relationships fall to zero, at 8× footprint before allocator overhead.

### Connections

[Relaxed Atomics](028-relaxed-atomics.md) shows that weak ordering does not eliminate modification traffic; [Compiler and Processor Reordering](021-compiler-and-processor-reordering.md) separates source semantics from hardware mapping. The [program roadmap](../ROADMAP.md) next integrates the block's weak-memory reasoning.

## Governing Question

How should engineers move from a parallel scaling regression to an evidence-backed false-sharing diagnosis, select a layout or ownership mitigation, and verify that the improvement survives target, allocator, topology, ABI, and workload variation?

False sharing is a performance defect, not a source-level data race. Correct code can scale badly because hardware owns memory in blocks larger than its logical fields.

## Why This Matters

Per-thread counters, queue indices, allocator metadata, reference counts, lock fields, work descriptors, statistics arrays, and adjacent object headers often place independent writers close together. One core's write can invalidate a line another core needs, forcing cache-to-cache transfers and serializing ownership.

The symptom resembles many other bottlenecks: throughput plateaus, latency rises, CPU utilization remains high, and adding threads hurts. Locks, true-sharing atomics, memory bandwidth, NUMA, load imbalance, oversubscription, frequency throttling, or serial code can look similar. Layout inspection alone is also insufficient because cold adjacent fields cause no important traffic.

A production diagnosis needs three facts together: agents touch different logical data, those addresses share the target coherence block, and sampled traffic/timing shows expensive write/read or write/write interaction. Only then should padding, alignment, sharding, batching, or ownership changes be evaluated.

## Prerequisites and Retrieval

Retrieve:

- concurrency versus parallel speedup from [Concurrency, Parallelism, and Asynchrony](001-concurrency-parallelism-and-asynchrony.md);
- progress and starvation distinctions from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- shared-state invariants from [Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md);
- atomic modification traffic from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md);
- contention/retry behavior from [Compare-and-Swap Loops](026-compare-and-swap-loops.md); and
- advisory counter sharding from [Relaxed Atomics](028-relaxed-atomics.md).

Retrieval prompt: explain why two race-free atomic counters can interfere even when neither counter's value or correctness depends on the other.

## Learning Objectives

After completing this module, a learner can:

1. distinguish true sharing, false sharing, races, and ordinary capacity misses;
2. map addresses and offsets to a target coherence granule;
3. explain ownership migration under write/read and write/write streams;
4. design a controlled scaling and placement experiment;
5. use layout and cache-to-cache evidence to localize a candidate line;
6. evaluate padding, alignment, sharding, batching, and ownership transfer;
7. quantify memory, cache, TLB, ABI, NUMA, and locality trade-offs;
8. avoid portable-source claims based on one assumed line size; and
9. verify improvements without hiding a new bottleneck.

## Core Exposition

### Functional correctness comes first

False sharing assumes accesses are legal under the language model. If two threads perform conflicting non-atomic accesses without hb, diagnose a data race first. Padding may make the race appear rarer while leaving undefined or invalid behavior.

Atomic fields can be race-free and falsely share. Mutex-protected fields can also share with a lock or spinner. Coherence traffic is below source-level object boundaries; the hardware does not know two words represent independent metrics.

Keep the claims separate:

- race freedom: language-model safety;
- coherence: architectural consistency for cached blocks;
- false sharing: unnecessary performance interaction from block placement;
- scalability: measured workload behavior.

### Why writes matter

Multiple cores can usually hold read-only copies of one line without ownership ping-pong. Harmful false sharing needs at least one write stream. With two writers to different words, each write may request writable ownership and invalidate the other's copy. With one writer and one reader of a different word, the reader repeatedly reacquires data after writer invalidations.

True sharing produces similar transfers when agents intentionally update/read the same datum. Padding cannot separate one counter from itself. Redesign true sharing with sharding, batching, combining, ownership, or fewer updates.

Unconditional writes can create traffic even when the value does not change. Read-check-write may avoid redundant ownership requests in some protocols, but it adds loads/branches and races must still be correct. Measure.

### Address-to-line reasoning

For a simplified fixed block size `B`, addresses `a` and `b` share a block when `floor(a/B)=floor(b/B)`. The offset is `a mod B`.

This arithmetic is diagnostic, not a portable language theorem. Hardware can have several cache levels, sectoring, directory granules, or target-specific coherence properties. Virtual and physical indexing details matter to tools. Obtain the architecture/tool definition.

For a structure, inspect actual compiled offsets and size. For an array, also inspect:

- base alignment;
- element stride;
- whether an element crosses a boundary;
- allocator headers or neighboring allocations;
- compiler/ABI layout; and
- field attributes actually honored by the toolchain.

A 64-byte-sized element does not ensure line separation if the allocation begins at offset 32.

### Coherence ownership traffic

In a common invalidation-based protocol, a core writing a shared line obtains an exclusive/modified state. Other cached copies are invalidated or downgraded. A later access by another core can require interconnect messages, cache-to-cache data transfer, or a shared-cache lookup.

The exact MESI-family states and costs vary. Do not prove application performance from a cartoon protocol. The durable mechanism is that writes are managed at a block granularity, so unrelated words can cause block transfers.

Remote-socket transfers can be much more expensive than within-core-cluster traffic. Simultaneous multithreading siblings may share cache levels differently. Thread migration changes the path. Placement is part of the experiment.

### Symptom is not diagnosis

A classic microbenchmark gives each thread one adjacent counter and repeats increments. One-thread performance is good; throughput stops scaling. Padding restores scaling. This is useful calibration but production evidence requires more.

Alternative causes include:

- all threads update one truly shared counter;
- a lock or allocator serializes;
- the working set exhausts memory bandwidth;
- load imbalance leaves cores idle;
- task granularity is too small;
- NUMA pages are remote;
- oversubscription causes context switches;
- turbo/frequency changes distort per-thread comparisons;
- the compiler removed or transformed work.

Use a hypothesis table and falsify competitors.

### Evidence chain

An evidence-backed workflow:

1. establish a repeatable throughput/latency regression over thread counts;
2. control input, warmup, duration, affinity, NUMA placement, and frequency policy;
3. profile CPU, lock, scheduler, and memory behavior;
4. identify cache lines with cache-to-cache/modified-line events;
5. map sampled addresses and instruction PCs to allocation, type, field offset, and source;
6. confirm different agents access different fields/objects with at least one writer;
7. change only layout or ownership;
8. repeat enough trials and report distributions/confidence;
9. compare coherence events and application outcomes; and
10. inspect the next bottleneck.

Linux `perf c2c` can attribute sharing to lines, offsets, functions, and local/remote HITM on supported platforms. `pahole` and symbols help decode layouts. Intel VTune and Arm SPE-based tooling offer target-specific alternatives. Event availability and interpretation vary.

### Padding and alignment

Padding creates distance; alignment chooses a boundary. Often both are needed. In C++, `hardware_destructive_interference_size` is an implementation-defined recommended minimum offset between concurrently accessed objects to avoid destructive interference, and is at least `alignof(max_align_t)`. It is a hint for the implementation, not a universal measured cache-line constant.

Language attributes affect type layout, but dynamic allocation must satisfy the over-alignment. Containers and foreign ABIs may impose constraints. Verify `sizeof`, `alignof`, member offsets, base addresses, and array stride in the deployed build.

Padding fields manually with a magic byte count is fragile across architectures and future member changes. Encapsulate the layout intent and assert what the supported build promises.

### Space and locality costs

Separating an 8-byte counter into a 64-byte or larger slot can multiply memory by eight or more. Large arrays then consume more cache capacity, memory bandwidth, pages, TLB entries, and NUMA placement. Initialization and scans slow down.

Padding can destroy constructive interference when one thread usually consumes several fields together. A lock and the data its owner immediately uses may benefit from proximity under light contention yet suffer when waiters spin on the same line.

Choose separation by access phase and writer identity:

- group mostly read-only data;
- group fields written together by one owner;
- separate independently hot writers;
- separate a hot writer from widely read cold data;
- do not pad cold paths without evidence.

### Sharding and batching

Sharding removes a global write hotspot by giving each thread, core, NUMA node, or partition local state. Padding between hot shards prevents the shards themselves from falsely sharing. Aggregation trades instantaneous exactness for scalable updates.

Batching performs several logical updates locally and periodically transfers a delta to shared state. It reduces ownership transfers but changes freshness, crash loss, overflow, and reconciliation semantics.

Per-core designs must handle thread migration and hotplug. Per-thread shards need registration, retirement, and final drain. NUMA shards require placement and hierarchical aggregation. Layout is only one part of ownership.

### Partition arrays by lines, not merely elements

Parallel loops can falsely share at chunk boundaries when adjacent threads write neighboring small elements. Static contiguous chunks usually confine interaction to boundary lines; cyclic scheduling can make many lines bounce among threads.

Remedies include line-aligned chunk starts, minimum chunk sizes, block partitioning, private output followed by merge, or changing array-of-structures to structure-of-arrays according to access.

Partitioning interacts with load balance. Large chunks reduce boundary sharing but can worsen imbalance. Measure full execution, not just the memory kernel.

### Atomics and memory order

Changing sequentially consistent atomics to relaxed may reduce ordering constraints, but every write/RMW still modifies the cache line. Coherence ownership traffic remains. A hot relaxed fetch-add can scale poorly.

Conversely, padding cannot make an invalid relaxed publication protocol correct. Ordering and placement answer different questions:

- ordering: which effects one operation makes available to another;
- placement: which logical objects share hardware transfer granularity.

Optimize only after both proofs are sound.

### Locks and waiting

A lock word shared with protected data can cause waiters spinning on the lock to reload when the owner writes nearby data. Separating lock and data may help, but the owner then touches another line. Parking rather than spinning reduces active readers; queue locks give waiters more local state.

If the lock itself is truly contended, padding it does not remove serialization. Reduce critical-section time, partition ownership, change the algorithm, or use a scalable lock appropriate to topology.

Lock metrics, scheduler traces, and cache-sharing evidence should be read together.

### Allocators and object adjacency

Two independently allocated hot objects may land in one line. General allocators optimize density and locality, not per-object writer separation. Small-object slabs can pack many headers or counters together.

Options include an aligned allocator, size class/layout change, per-thread arenas, object grouping by owner, or separating hot metadata from cold bodies. Intel oneTBB provides a cache-aligned allocator specifically for this concern, with explicit space cost.

Reallocation or compaction can change addresses. Managed runtimes may move objects or hide layout. Use runtime-supported mechanisms and profiling; do not assume source declaration order equals stable physical adjacency.

### Portability and ABI

Cache and coherence granules vary. A public structure's padding changes size, alignment, serialization assumptions, shared-memory ABI, FFI, and binary compatibility. Over-aligned types can be unsupported by an allocator or stack convention.

Keep performance layout private where possible. Version shared-memory formats. Avoid exposing padded representation over networks/storage. Test all supported architectures and compilers.

Some languages lack stable layout without annotations; runtimes can change field layout. Prefer ownership/sharding abstractions when exact placement cannot be guaranteed.

### Measurement design

Report:

- hardware model, sockets, cores, SMT, caches, NUMA;
- OS, runtime/compiler, flags, build type;
- thread affinity and page placement;
- workload/data distribution and read/write ratio;
- duration, warmup, trials, summary distribution;
- throughput, latency percentiles, CPU time, energy if relevant;
- cache-to-cache/HITM/contested-access events with tool caveats;
- object addresses/offsets/stride; and
- before/after memory footprint.

Use a correctness oracle in both variants. Faster wrong accounting is not an optimization. Retest at one thread: a padded version may regress locality even if high-core scaling improves.

### Security and isolation

False sharing is primarily performance, but shared-cache behavior can affect timing and denial-of-service surfaces. An attacker controlling adjacent updates may amplify contention. Padding is not a general side-channel defense: caches, predictors, memory controllers, SMT, and shared resources remain.

Security isolation requires a threat model, scheduling/resource policy, constant-time review where applicable, and target measurement. Do not turn a performance fix into a security claim.

## Definitions and Notation

Let target coherence block size be `B` for the measured mechanism and `line(a)=floor(a/B)`. For accesses to distinct logical data `x` and `y`:

`x≠y ∧ line(addr(x))=line(addr(y)) ∧ (write(x)∨write(y))`

is a false-sharing candidate, not proof of material cost.

For `n` equal-sized counters of size `s` packed into one block when `ns≤B`, each of `n` writers has `n-1` potential peer writers, or `n(n-1)` directed relationships. This is a descriptive upper-bound model, not a count of hardware invalidations.

Let `T_p` be measured runtime at `p` workers and `S_p=T_1/T_p`. Poor `S_p` motivates diagnosis but does not identify false sharing.

## Mechanisms, Invariants, or Proof Structure

Use this workflow:

1. **Prove race freedom and correctness.**
2. **Reproduce scaling loss** with controlled builds, inputs, placement, and trials.
3. **Classify sharing:** same datum (true), different datum/same block (false), or read-only.
4. **Resolve layout:** addresses, offsets, base alignment, stride, allocator, and ABI.
5. **Gather traffic evidence:** line-level samples and local/remote ownership events.
6. **Map agents and instructions** to the candidate offsets.
7. **Choose mitigation:** separation, sharding, batching, ownership, scheduling, or fewer writes.
8. **Quantify costs:** footprint, locality, TLB, NUMA, complexity, and portability.
9. **Change one causal variable.**
10. **Re-run correctness and performance** across thread counts and targets.
11. **Confirm traffic falls** and identify the next limiter.
12. **Document durable layout intent and supported assumptions.**

The executable arithmetic maps eight packed or padded counters into assumed 64-byte blocks and counts potential directed writer-peer relationships.

<!-- bijux-verify: {"id":"false-sharing-line-layout-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"line_size=64\nworkers=8\ncounter_size=8\npacked_lines=1\npacked_directed_peers=56\npadded_stride=64\npadded_lines=8\npadded_directed_peers=0\nfootprint_ratio=8\n","stderr":""}} -->
```python
line_size = 64
workers = 8
counter_size = 8

packed_lines = []
padded_lines = []
for worker in range(workers):
    packed_lines.append((worker * counter_size) // line_size)
    padded_lines.append((worker * line_size) // line_size)

packed_peers = 0
padded_peers = 0
for left in range(workers):
    for right in range(workers):
        if left != right and packed_lines[left] == packed_lines[right]:
            packed_peers += 1
        if left != right and padded_lines[left] == padded_lines[right]:
            padded_peers += 1

print(f"line_size={line_size}")
print(f"workers={workers}")
print(f"counter_size={counter_size}")
print(f"packed_lines={len(set(packed_lines))}")
print(f"packed_directed_peers={packed_peers}")
print(f"padded_stride={line_size}")
print(f"padded_lines={len(set(padded_lines))}")
print(f"padded_directed_peers={padded_peers}")
print(f"footprint_ratio={line_size // counter_size}")
```

Limitations: the model assumes an aligned base, one 64-byte granule, fixed stride, simultaneous hot writers, and no allocator header. It counts address relationships, not cache states, invalidations, transfers, latency, NUMA paths, compiler layout, or application speedup. Target profiling must establish material false sharing.

## Alternatives and Trade-Offs

**Padding/alignment** preserves direct per-owner access but increases footprint and depends on target/toolchain allocation.

**Sharding** removes a shared update hotspot and supports hierarchical aggregation, at snapshot and lifecycle cost.

**Batching** amortizes shared writes, trading freshness and crash-loss bounds.

**Ownership transfer** moves whole objects/messages between agents and can eliminate concurrent writers, with queueing cost.

**Structure re-layout** separates hot writers from readers or groups fields used together, but can move the problem elsewhere.

**Scheduling/partitioning** reduces cross-thread line boundaries while trading load balance and runtime flexibility.

**Parking or scalable locks** reduces active sharing on lock state but does not parallelize a true critical section.

**Accepting the issue** is rational for cold paths when separation costs more memory and complexity than measured benefit.

## Failure Modes and Misconceptions

1. **False sharing is a data race.** It can occur in fully race-free code.
2. **Any shared line is harmful.** Read/read sharing is normally not destructive.
3. **A scaling plateau proves false sharing.** Many bottlenecks look the same.
4. **A hot line proves false sharing.** It may be true sharing.
5. **Member size equal to line size guarantees separation.** Base alignment and stride matter.
6. **Every machine uses 64-byte coherence lines.** Target properties vary.
7. **Language alignment guarantees allocator support.** Verify actual allocation and container behavior.
8. **Relaxed atomics avoid line ownership.** RMW writes still contend.
9. **Padding a shared counter makes it scalable.** True sharing remains.
10. **Padding is free.** Footprint, caches, pages, TLB, and locality change.
11. **More separation is always better.** Constructive locality can be lost.
12. **One benchmark run is evidence.** Noise, frequency, placement, and warmup distort it.
13. **HITM always means false sharing.** Inspect addresses and logical access.
14. **One architecture's counters are portable.** Event names/meaning/support differ.
15. **Per-thread shards have no lifecycle.** Registration, migration, retirement, and drain matter.
16. **A fix cannot move the bottleneck.** Optimization exposes the next limiter.
17. **Source declaration fixes physical layout forever.** ABI, allocator, runtime, and build matter.
18. **Padding provides security isolation.** Other shared microarchitectural resources remain.

## Worked Examples

### Example 1

**Situation.** Two threads increment adjacent atomic counters in one line.

**Reasoning.** Values are independent and race-free, but each RMW requests writable ownership of their shared block.

**Conclusion.** This is a false-sharing candidate requiring traffic evidence.

### Example 2

**Situation.** Two threads increment the same atomic counter.

**Reasoning.** They intentionally share one datum; no layout can separate it from itself.

**Conclusion.** This is true sharing; shard, batch, or redesign ownership.

### Example 3

**Situation.** Many threads read separate immutable fields in one line.

**Reasoning.** Without writes, shared copies need not repeatedly invalidate.

**Conclusion.** Proximity may be constructive rather than false sharing.

### Example 4

**Situation.** Each array element is 64 bytes, but the allocation begins 32 bytes into a line.

**Reasoning.** Every element straddles two lines and neighboring elements share one.

**Conclusion.** Verify base alignment and stride, not size alone.

### Example 5

**Situation.** Replacing SC with relaxed atomics leaves scaling unchanged.

**Reasoning.** Ordering constraints changed, but every increment still migrates the same line.

**Conclusion.** Memory ordering is not a false-sharing mitigation.

### Example 6

**Situation.** Padding eight 8-byte counters to 64-byte stride removes packed adjacency.

**Reasoning.** Under the assumed aligned 64-byte target, lines rise from one to eight and footprint grows eightfold.

**Conclusion.** Compare measured traffic gain with space/locality cost.

### Example 7

**Situation.** A spin lock shares a line with data its owner updates.

**Reasoning.** Waiters repeatedly read the line while owner writes nearby data, amplifying invalidation. Separate or park waiters, then measure.

**Conclusion.** Lock placement and wait policy interact.

### Example 8

**Situation.** Cyclic loop scheduling assigns adjacent elements to different workers.

**Reasoning.** Many output lines receive writes from several cores. Contiguous blocks confine sharing to boundaries but may reduce balance.

**Conclusion.** Partition at coherence-aware granularity and measure imbalance.

### Example 9

**Situation.** `perf c2c` reports remote HITM on one address.

**Reasoning.** Map the line's offsets and PCs. Same offset indicates true sharing; different hot offsets suggest false sharing; placement explains remote cost.

**Conclusion.** Counter, address, layout, and logical-owner evidence must agree.

### Example 10

**Situation.** A real-time controller pads state and claims its deadline is guaranteed.

**Reasoning.** Removing one coherence source does not bound scheduling, interrupts, NUMA, devices, thermal effects, WCET, or fault recovery.

**Conclusion.** Named real-time, hardware, controls, security, domain, quality, and functional-safety reviewers need target evidence; this chapter makes no timing approval.

## Cross-Program Connections

- **Computer architecture:** coherence protocols, cache hierarchy, interconnect, NUMA, and counters create the mechanism/evidence.
- **Operating systems:** affinity, migration, scheduling, page placement, and perf tooling shape diagnosis.
- **Programming languages:** layout, alignment, atomics, allocation, and ABI define source control.
- **Algorithms:** partitioning, aggregation, and ownership determine communication.
- **Performance engineering:** experimental design separates causal improvement from noise.
- **Data systems:** sharded counters trade update scale for snapshot/reconciliation complexity.
- **Security:** shared-resource contention can become denial-of-service or timing surface.
- **Software engineering:** private representations and durable layout comments limit regression.

## References

1. William J. Bolosky and Michael L. Scott. “False Sharing and Its Effect on Shared Memory Performance.” USENIX SEDMS, 1993.
2. David A. Patterson and John L. Hennessy. *Computer Organization and Design*, sixth edition. Morgan Kaufmann, 2020.
3. Maurice Herlihy and Nir Shavit. *The Art of Multiprocessor Programming*, revised first edition. Morgan Kaufmann, 2012.
4. ISO C++ working draft. “Hardware interference size.” Current draft accessed 2026-08-29.
5. Linux Kernel documentation. “False Sharing.” Current documentation accessed 2026-08-29.
6. Intel. *Intel 64 and IA-32 Architectures Optimization Reference Manual*, volume 1, version 050. 2024.
7. Intel. “VTune Profiler Performance Analysis Cookbook: False Sharing.” Accessed 2026-08-29.
8. Intel oneAPI Threading Building Blocks. “Memory Allocation and `cache_aligned_allocator`.” Accessed 2026-08-29.
9. Arm. “Statistical Profile Extension” and false-sharing analysis with `perf c2c`. Accessed 2026-08-29.
10. Ulrich Drepper. “What Every Programmer Should Know About Memory.” 2007.

## Exercises

### Exercise 1

Define true sharing, false sharing, cache-line contention, and the necessary read/write access condition for destructive false sharing.

### Exercise 2

Assume an aligned 64-byte base and eight 8-byte per-thread counters. Map packed and 64-byte-strided addresses to lines, count directed writer-peer relationships, and state the footprint ratio.

### Exercise 3

Diagnose a benchmark that pads a 64-byte structure but uses an unaligned array, changes thread scheduling simultaneously, and reports one faster run without counter evidence. Design a valid experiment.

### Exercise 4

Compare padding, per-thread sharding, batching, block partitioning, and ownership transfer for a hot statistics array and a truly shared work index.

### Exercise 5

A low-latency trading service finds local and remote HITM around risk counters and authorization state. Specify correctness, diagnosis, mitigation, security, and human-review boundaries.

## Answers to the Exercises

### Answer 1

True sharing is concurrent access to the same logical datum with at least one writer. False sharing is access by different agents to distinct logical data that occupy one coherence block, with at least one writer, causing unnecessary block traffic. Cache-line contention includes both intentional and false competition for the block.

Read/read sharing generally permits shared cached copies and is not destructively false sharing. Write/write or write/read interaction is the necessary access pattern, but material cost still requires hot frequency, placement, topology, and measured traffic.

### Answer 2

Packed addresses are 0,8,16,24,32,40,48,56; floor(address/64) is zero for all, so one line. Each of eight writers shares with seven peers: `8×7=56` directed relationships.

With aligned 64-byte stride, addresses are 0,64,...,448 and line indices 0..7, so eight lines and zero such relationships. Slot footprint rises from 8 to 64 bytes, an 8× ratio before allocator/array overhead. These counts model placement, not actual invalidations.

### Answer 3

A 64-byte element from an unaligned base can straddle two lines and share with its neighbor. Changing scheduling also changes access ownership/load balance, so the faster run has two causes. One run gives no noise distribution or traffic evidence.

Build optimized correctness-equivalent variants. Record target granule, `sizeof`/`alignof`/offsets/stride and actual base addresses. Hold scheduling, data, affinity, NUMA placement, frequency policy, warmup, and duration constant. Run multiple trials over thread counts. Profile line addresses, PCs, local/remote HITM or supported equivalents; map offsets to fields. Change only aligned allocation/layout, then compare correctness, throughput/latency distributions, traffic, and footprint. Separately test scheduling afterward.

### Answer 4

For independent hot statistics, per-thread shards plus verified separation reduce both true and false sharing; batch deltas to reduce aggregation traffic. Padding alone helps adjacent shards but not a single global statistic. Accept approximate live sums and reconcile after shard retirement/quiescence, or use locked snapshots if exactness is required.

For array output, contiguous block partitioning and line-aware boundaries reduce cross-worker lines; private output plus merge is another ownership design. For a truly shared work index, padding cannot remove its modification order. Allocate work in batches/ranges, use work stealing with mostly local queues, or transfer ownership through tasks. Measure balance, freshness, footprint, and tail latency.

### Answer 5

First prove source correctness: atomics/locks and authorization invariants must remain valid; never “fix” a race with layout. Reproduce latency under controlled affinity, socket/page placement, workload, and optimized builds. Map local/remote HITM samples to exact lines, PCs, offsets, allocation, and writer identities; distinguish the truly shared authorization state from independent risk counters.

Mitigate independent counters with per-thread/NUMA shards, batching, alignment, or owner grouping, then reconcile authoritatively. Treat shared authorization as a correctness boundary: partition by account/instrument, use immutable snapshots or ownership transfer only if semantics permit; padding cannot remove true sharing. Quantify footprint, staleness, migration, restart, and failover.

HITM patterns may expose contention/denial-of-service or timing signals, but padding is no general isolation proof. Named concurrency, architecture, OS/NUMA, performance, security, risk/domain, reliability, compliance, and production-operations reviewers must approve target evidence and rollout/rollback thresholds. This answer makes no financial, security, or deployment guarantee.
