---
module_id: DSE-006
program: Data Structures Engineering
level: 1
module_number: 6
title: Memory Locality and Cache Behavior
status: complete
last_verified: 2026-08-29
---

# Memory Locality and Cache Behavior

## One-Page Review

### Governing question

How does a data structure's access stream interact with cache lines, translation, prefetching, bandwidth, dependency chains, and coherence—and how can engineers validate those effects without turning one machine's counters into universal law?

### Essential definitions

- **spatial locality** is reuse of nearby addresses within a relevant storage-transfer unit and time window.
- **temporal locality** is reuse of the same data before it is displaced or invalidated.
- A **cache line** is a hardware-managed transfer/coherence unit whose size and behavior are platform-specific.
- A **working set** is the data actively needed during a computation phase under a stated time/operation window.
- A **cache hit** is served by a given cache level; a **miss** requires lookup/fill from another level, subject to implementation details.
- **memory-level parallelism (MLP)** overlaps independent outstanding memory operations.
- **pointer chasing** creates address dependencies when the next load address is produced by the current load.
- A **hardware prefetcher** predicts future accesses and requests data before explicit demand.
- A **translation lookaside buffer (TLB)** caches virtual-to-physical address translations.
- **false sharing** occurs when cores write distinct logical data that occupies one coherence unit, causing unnecessary coherence traffic.

### Central model, mechanism, or theorem

For a simplified cache-line model with line size (B), address stream $a_0,\ldots,a_{m-1}$ touches modeled line numbers

$$
\ell_i=\left\lfloor\frac{a_i}{B}\right\rfloor.
$$

The distinct-line footprint of a phase is $|\{\ell_i\}|$, but actual misses additionally depend on cache capacity, associativity, mapping, replacement, earlier state, prefetching, coherence, translation, and concurrent activity. A latency lower bound for a strict dependent chain differs from the throughput of independent misses:

$$
time_{dependent}\gtrsim hops\times exposed\ latency,
$$

whereas independent accesses may overlap until constrained by MLP, queues, or bandwidth. This is a reasoning model, not a cycle-accurate theorem.

### Critical invariants

- Every locality claim names the accessed fields, order, working-set size, element layout, machine, and execution mode.
- Logical contiguity is separated from physical residency, translation, cache mapping, and referenced-object placement.
- Cache-line utilization counts useful bytes for the operation, not merely transferred bytes.
- Dependent pointer chains are distinguished from random independent gathers.
- Latency, bandwidth, MLP, prefetch, translation, and coherence are analyzed as different mechanisms.
- Hardware-counter event names and meanings are pinned to CPU/PMU, privilege scope, and tool configuration.
- Counter multiplexing, sampling, speculation, skid, system noise, and instrumentation overhead are reported.
- AoS, SoA, and blocked/AoSoA comparisons use equivalent code generation and isolate layout from language/runtime effects.
- Padding/alignment changes preserve representation correctness and do not introduce unchecked arithmetic or ABI breakage.
- Benchmark and counter evidence is local empirical evidence, not proof of a universal speed ratio.

### Common failures

Common failures are claiming “contiguous is always faster”; using Python objects versus vectorized native arrays to prove AoS versus SoA; calling a random gather pointer chasing; assuming every line fill is a DRAM access; dividing payload bytes by time and labeling it physical bandwidth; interpreting cache misses without instructions/accesses; ignoring TLB and page faults; disabling optimization or accidentally eliminating benchmark work; treating counter names as portable; padding every field without measuring; and confusing false sharing with ordinary data races.

### Compact example

With four modeled element slots per cache line, scanning 16 contiguous slots touches four distinct lines, while visiting indices `0,4,8,12` touches four lines for only four useful values. For records of four fields, reading only field `x` from eight AoS records can touch eight modeled lines when each record occupies one line; an SoA `x` array can touch two. This footprint model predicts a hypothesis. It does not predict actual misses, cycles, vectorization, or speedup.

### Connections

[DSE-004](004-time-space-and-allocation-cost.md) separates proof from measurement and [DSE-005](005-contiguous-and-linked-layouts.md) supplies layout mechanisms. DSE-010 owns full benchmark practice; DSE-071 onward develops external-memory/cache-oriented structures. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns cache and processor design in depth.

## Governing Question

Why can two implementations with the same asymptotic work and abstract behavior differ dramatically on one workload and machine, yet reverse under another field set, data size, mutation pattern, compiler, or hardware generation?

The answer is not one slogan about “cache friendliness.” A processor executes an address and instruction stream through several caches, translation structures, prefetchers, queues, coherence protocols, memory controllers, and compiler-generated transformations. Data-structure layout influences that stream, but the machine and workload determine how the influence becomes time.

## Why This Matters

Modern data structures often spend more time moving and waiting for data than performing arithmetic. Dense scans can use wide transfers, prefetching, vector instructions, and many independent requests. A dependent chain can serialize misses. Sparse updates can generate coherence traffic. A compact representation can fit a working set in a smaller cache or TLB reach.

But simplistic locality rules create poor designs. Linked nodes allocated from a dense arena can outperform a shifting array under update-heavy work. SoA can waste bandwidth when every operation needs complete records. Prefetching random independent indices differs from following unknown next pointers. Production judgment requires mechanisms, measurements, and honest uncertainty.

## Prerequisites and Retrieval

You should know binary/hexadecimal addressing, arrays, linked nodes, virtual memory at a basic level, and DSE-004/DSE-005. Retrieve:

1. Big-O does not model memory hierarchy unless the cost model explicitly does.
2. A contiguous container can contain pointers to noncontiguous objects.
3. Cache hardware moves units larger than many scalar values.
4. Independent operations can overlap; dependent operations constrain issue order.
5. One benchmark describes one implementation/workload/environment.
6. Correctness and resource evidence remain separate obligations.

## Learning Objectives

After completing this module, you should be able to:

- derive line-footprint and useful-byte hypotheses from address streams;
- distinguish spatial/temporal locality from mere adjacency;
- reason separately about capacity, mapping, translation, prefetch, MLP, and bandwidth;
- explain why dependent pointer chasing differs from random independent access;
- compare AoS, SoA, and blocked hybrids for an explicit field-access workload;
- identify false sharing and separate it from data races and true sharing;
- design locality experiments with equivalent implementations and controlled working sets;
- collect and qualify hardware-counter evidence without assuming event portability;
- connect locality optimizations to invalidation, alignment, ABI, and security constraints;
- reject universal ratios and select layouts from target evidence.

## Core Exposition

**Begin with the access stream.** A data structure does not “have locality” in isolation. An operation produces an ordered stream of instruction fetches, data reads/writes, addresses, widths, and dependencies. The same array has strong spatial locality under a full scan, poor useful-byte density under a wide stride, and temporal locality under repeated access to a small hot subset.

Describe the phase: construction, lookup, update, traversal, compaction, iteration, or destruction. Name fields touched and whether accesses read, write, or perform atomic operations. Include metadata: a hash-table lookup touches control bytes, keys, and possibly values; a tree walk reads child links and comparison fields.

**Cache lines and useful bytes.** Caches normally transfer/manage aligned lines, not individual application fields. If an operation reads eight useful bytes from each 64-byte line, naive payload utilization is one eighth for that stream. Yet a later operation may reuse the remaining bytes, and prefetched/evicted/write-allocated traffic can change physical transfer volume.

Line size is a machine property. Do not bake a presumed value into persistent format or correctness logic. Alignment to a line can reduce crossing or false sharing on a target, but over-alignment adds padding and may vary across CPUs. Query/document the deployed ABI and measure.

The distinct-line footprint counts unique line identifiers in a window. It is a lower-level improvement over element count but still not a miss count. If the footprint fits and mapping/reuse cooperate, later references may hit. If several addresses map to the same limited set, conflict evictions can occur even before total capacity is exhausted.

**Compulsory, capacity, conflict, and coherence effects.** Textbooks classify first-reference misses as compulsory, working-set overflow as capacity, and set-mapping collisions as conflict. Real replacement/prefetch/coherence makes classification approximate, but it remains diagnostic language. Coherence invalidations create misses/traffic even when capacity is ample.

Cold and warm states answer different questions. Startup or sporadic tasks may be cold. A steady service may keep hot metadata warm while large payload streams through. Explicitly prime state only if the target workload does.

**Hierarchy and access time.** A demand can be satisfied from several cache levels, another core's cache, local/remote memory, mapped storage, or device memory depending on platform. Out-of-order execution may overlap lookup and useful work. Therefore “a miss costs N cycles” is not a portable constant.

Average memory-access-time equations can organize hypotheses:

$$
T\approx t_{L1}+m_{L1}(t_{L2}+m_{L2}(\cdots)),
$$

but miss rates are conditional, latencies overlap, fills queue, and prefetch/coherence complicate the product. Use the equation as a model and validate with counters/experiments.

**Dependency chains and MLP.** In `node = node.next`, the next address is unavailable until the current node arrives. A long chain exposes latency when little independent work exists. A random gather with all indices already available can issue several independent misses and exploit MLP. It may be bandwidth/queue limited and often creates a result buffer; it is not a faithful lower or upper bound for all pointer-chasing structures.

Trees can expose limited parallelism by traversing several queries together. Graph frontiers can batch neighbors. Software prefetch may help predictable future nodes, but too-short lead time, wrong-path requests, bandwidth pressure, and unsafe pointer dereference constrain it.

**Hardware prefetching.** Prefetchers recognize some sequential/strided/correlated patterns and vary across microarchitectures. A sequential scan commonly benefits, but not invariantly: tiny data is already hot; streams can exceed bandwidth; multiple streams can overwhelm tracking; backward/irregular strides differ; prefetch can evict useful lines.

Do not call prefetched data “free.” It consumes bandwidth, fill buffers, cache capacity, and energy. Counter events may count demand and prefetch separately or not, depending on PMU.

**Bandwidth versus latency.** A dense stream with enough parallel work can approach a bandwidth ceiling. A strict dependency chain is latency sensitive and may transfer little total data. Arithmetic intensity—operations per byte moved—helps decide whether computation or data movement limits a kernel.

The Roofline model bounds attainable arithmetic throughput by compute peak and memory bandwidth times arithmetic intensity. It is useful for bulk kernels, less direct for branchy single-operation latency. State which bandwidth level and byte definition are used.

Payload bandwidth (payload\ bytes/time) is an application-level rate. It can exceed or understate physical traffic because of cache reuse, stores, write allocate, compression, temporaries, or multiple passes. Label it honestly.

**Working-set size and phase changes.** As a structure grows, active data may cease fitting in a cache or TLB reach. Timings can change across broad regions rather than at one exact size because of associativity, prefetch, page mapping, shared use, frequency, and access distribution.

Plot normalized time and counters across sizes that cross relevant capacities, but do not infer undocumented cache capacity from one timing cliff. Query authoritative topology where available and corroborate with targeted experiments.

**Translation locality.** Virtual addresses require translation. TLB entries cover pages; large/huge pages extend reach but affect allocation, fragmentation, latency, permissions, and deployment. Random nodes across many pages can incur translation misses even if line footprint is similar.

Page faults are not cache misses. Minor faults establish mappings without storage I/O; major faults may require I/O. Warm-up that touches every page changes the workload by removing first-touch behavior. NUMA first-touch can also place pages near one thread and remote from another; DSE treats NUMA-aware distributed placement later, while this module requires reporting it.

**AoS, SoA, and AoSoA.** Array of structures places fields of one record together. It benefits operations consuming most fields of each record and supports simple identity. Structure of arrays groups one field across records, increasing useful density for field-wise scans and often enabling vectorization. It requires synchronized lengths/permutations and makes whole-record insert/delete more complex.

Array of structures of arrays (AoSoA) groups records into fixed-size blocks whose fields are stored in small arrays. It can balance vector width, cache working set, and record grouping. Block size is a target/workload tuning parameter, not a universal constant.

Compare layouts with equivalent native loops, algorithms, compiler flags, data types, alignment, and work. A pure-language object loop versus a vectorized library routine confounds dispatch, boxing, vectorization, allocation, and layout. Such a comparison can be operationally relevant, but it cannot isolate layout causality.

**Padding and packing.** Reorder fields or pad records to control alignment, line crossing, and false sharing only under a stable layout/ABI contract. Packed representations reduce footprint but can create unaligned access, extra instructions, or illegal accesses on some targets. Serialization formats must define byte layout independently from native in-memory padding.

Padding hot counters onto separate lines may reduce false sharing, but can inflate working sets and hurt scans. Group read-mostly fields separately from frequently written fields when measurements show coherence pressure.

**False, true, and destructive sharing.** Two threads writing different variables on the same coherence line can repeatedly invalidate each other's copies: false sharing. If they access the same logical variable, that is true sharing. A data race is a language-level synchronization violation; false sharing can occur in fully synchronized, race-free code.

Read-only sharing is generally not false sharing. Adjacent allocator objects owned by different threads can accidentally share a line. Detect it with per-thread scaling, coherence events where supported, address/layout inspection, and padding experiments—never from timing alone.

**Branching and locality interaction.** A dense representation can still be slow if control flow is unpredictable or if it forces unnecessary fields. A branchless scan can do more work but vectorize/overlap better. Binary search has logarithmic comparisons but nonsequential probes; branch and cache behavior change with size and implementation.

Separate effects using controlled variants: same layout with branch strategy changes; same algorithm with layout changes; same field set with ordering changes. Compiler reports and assembly help establish what ran.

**Compaction, tiling, and blocking.** Pool/arena allocation can place linked nodes densely while preserving link semantics. Periodic compaction improves density but invalidates addresses and costs movement. Stable handles/indices mitigate invalidation as DSE-005 described.

Blocking partitions work so a tile's active fields fit a target level, increasing reuse before eviction. Cache-aware designs tune block sizes; cache-oblivious layouts recursively arrange data to provide locality across unknown levels under an ideal-cache model. Neither eliminates measurement or platform constraints.

**Hardware-counter evidence.** Performance-monitoring units expose events such as cycles, instructions, cache/TLB accesses/misses, branches, stalls, and coherence traffic, but availability/semantics differ by model. Generic tool aliases can map differently or be unsupported. Read the processor event reference and record raw/event encoding when needed.

Counters may include speculative or non-retired activity, count at varying hierarchy points, multiplex when too many events are requested, and include kernel/hypervisor/other-thread work depending on scope. Sampling attributes events imprecisely (“skid”). Derived metrics such as MPKI require a meaningful denominator and confidence in both counts.

Use repeatable process/core affinity where authorized, record competing load and frequency/power state, isolate setup, validate results, and keep raw outputs under artifacts. Do not disable production-relevant mechanisms merely to get a cleaner number without reporting the changed environment.

Cache simulation can compare traces under an explicit model and offer reproducibility. It may not represent a target's prefetch, replacement, nonblocking behavior, coherence, or speculative execution. Simulation is model evidence, hardware counters are target evidence, and wall time is end-to-end evidence.

**Benchmark design.** Select sizes below, around, and above anticipated working-set boundaries. Test sequential, strided, shuffled-independent, dependent-chain, update, and mixed workloads separately. Keep logical work and result validation equivalent. Report cold and warm cases if both matter.

Use enough iterations for timer resolution, independent samples for variability, and claim-scaled statistics. Avoid hard-coded claims like “30 runs always suffice.” Preserve code/data seed, raw samples, machine topology, toolchain, counter commands, and counter multiplex ratios.

**Security and determinism.** Cache state and timing can reveal access patterns. Constant-time security code avoids secret-dependent memory access and branches under a defined threat/model; ordinary cache-friendly optimization is not a constant-time proof. Prefetchers, shared caches, speculative execution, and compiler transformation complicate validation.

Randomizing layout can mitigate some attacks while harming locality. Keyed hashing reduces collision attacks but does not remove cache side channels. Security review must define attacker capability and observations.

**Operational choice.** Choose a layout after meeting correctness, capacity, invalidation, concurrency, and safety constraints. Then use workload-specific models and target measurements. Report trade-offs: one layout may improve scan throughput while worsening point-update latency, memory footprint, tail behavior, or evolvability.

The executable model below computes line footprints for simple slot streams. It does not inspect Python addresses, execute hardware loads, or predict cache misses.

<!-- bijux-verify: {"id":"cache-line-footprint-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"sequential_accesses=16 unique_lines=4\nstride4_accesses=4 unique_lines=4\naos_x_records=8 modeled_lines=8\nsoa_x_records=8 modeled_lines=2\nevidence=line_footprint_model_not_cache_measurement\n","stderr":""}} -->
```python
def unique_lines(slot_indices, slots_per_line):
    return len({index // slots_per_line for index in slot_indices})


slots_per_line = 4
sequential = tuple(range(16))
stride_four = tuple(range(0, 16, 4))
print(
    f"sequential_accesses={len(sequential)} "
    f"unique_lines={unique_lines(sequential, slots_per_line)}"
)
print(
    f"stride4_accesses={len(stride_four)} "
    f"unique_lines={unique_lines(stride_four, slots_per_line)}"
)

records = 8
fields_per_record = 4
aos_x_slots = tuple(record * fields_per_record for record in range(records))
soa_x_slots = tuple(range(records))
print(f"aos_x_records={records} modeled_lines={unique_lines(aos_x_slots, slots_per_line)}")
print(f"soa_x_records={records} modeled_lines={unique_lines(soa_x_slots, slots_per_line)}")
print("evidence=line_footprint_model_not_cache_measurement")
```

## Definitions and Notation

Let access trace $A=\langle(a_i,w_i,d_i)\rangle$, where address (a_i), width (w_i), and dependency information (d_i) are relative to one execution. For modeled line size (B), an access can intersect multiple lines; simple aligned slot examples use $lfloor a_i/B\rfloor$.

For operation phase (P), useful-byte ratio can be modeled as

$$
U(P)=\frac{useful\ bytes\ consumed}{modeled\ transferred\ bytes},
$$

provided numerator/denominator scope is declared. Working set $W(P,\Delta)$ is the set of cache/translation units reused within window (Delta); no single universal window exists.

Arithmetic intensity is operations per transferred byte under a named hierarchy boundary. MPKI is misses per thousand instructions for named events and instruction denominator; it is not portable without event semantics.

## Mechanisms, Invariants, or Proof Structure

**Line-footprint derivation.** Map every addressed byte interval to modeled line identifiers, form the union, and count useful bytes. This supplies a transfer lower-bound hypothesis under the model, not actual misses.

**Dependency analysis.** Draw address-production edges. A chain limits simultaneous issue; independent addresses permit overlap subject to machine resources. Randomness alone does not identify dependency.

**Working-set analysis.** Partition the operation into phases, enumerate touched lines/pages and reuse distances, then compare with declared cache/TLB models. Validate boundaries empirically.

**Layout equivalence.** Prove AoS/SoA/AoSoA implementations produce the same abstract results and access the same logical fields before comparing generated code, counters, and time.

**False-sharing diagnosis.** Establish distinct logical ownership, shared physical coherence line, concurrent writes, invalidation traffic, and improvement after an otherwise equivalent separation experiment.

**Counter provenance.** Bind event, CPU/PMU, encoding, privilege/thread/process scope, duration, multiplex scaling, tool version, and raw output before deriving ratios.

**Finite evidence boundary.** The snippet proves arithmetic over modeled slot indices only. It makes no claim about real addresses, line size, prefetching, misses, bandwidth, counters, or time.

## Alternatives and Trade-Offs

**Dense versus pointer-linked layout.** Dense storage often improves transfer utilization and MLP; linked topology supports local structural changes and stable nodes. Pools/indices combine properties.

**AoS versus SoA versus AoSoA.** AoS serves whole-record access, SoA field-wise bulk work, and AoSoA tiled/vector work. Mutation, identity, code complexity, and target width trade against locality.

**Compaction versus stable addresses.** Compaction improves density and page reach but moves objects. Handles add indirection while preserving logical identity.

**Prefetch versus demand loading.** Prefetch may hide latency for predictable streams; inaccurate/early prefetch consumes bandwidth and capacity. Software hints are target-specific and advisory.

**Padding versus footprint.** Separation can reduce false sharing and crossings; padding enlarges working sets and may hurt read scans.

**Huge versus ordinary pages.** Huge pages increase TLB reach but affect availability, fragmentation, startup, sharing, and operations. Measure under deployment policy.

**Counters versus simulation.** Counters observe a target imperfectly; simulation explains an explicit model reproducibly. Use both with wall time and correctness checks when claims justify it.

## Failure Modes and Misconceptions

1. **“Contiguous is always faster.”** Updates, field selection, size, compiler, and hardware can reverse outcomes.
2. **“Random gather is pointer chasing.”** Precomputed independent addresses can overlap; linked addresses are dependent.
3. **“A line footprint equals cache misses.”** Capacity, mapping, prior state, prefetch, and coherence intervene.
4. **“Every cache miss reaches DRAM.”** Another cache level/core can satisfy it.
5. **“Payload GB/s is memory-controller bandwidth.”** Physical traffic can differ substantially.
6. **“SoA beats AoS.”** Only for stated field-access/vector/workload conditions.
7. **“Python versus NumPy isolates layout.”** It confounds runtime, dispatch, vectorization, and representation.
8. **“False sharing is a data race.”** Race-free variables can still share a coherence line.
9. **“Warm-up removes noise.”** It changes cold/page/first-touch behavior and cannot remove all variance.
10. **“Cache sizes produce exact timing cliffs.”** Transitions are workload- and mapping-dependent regions.
11. **“Generic counter names are portable.”** PMU event semantics and availability vary.
12. **“More misses prove slower code.”** Overlap, useful work, frequency, and bandwidth determine time.
13. **“Padding is a free optimization.”** It increases footprint and changes ABI/layout.
14. **“Timing success proves constant time.”** Security claims require threat-specific analysis and stronger evidence.

## Worked Examples

### Example 1

**Question:** Why can a sequential 64-bit scan use most of each modeled 64-byte line?

**Reasoning:** Eight adjacent values occupy the line, and the scan consumes all before moving on, absent padding/indirection.

**Conclusion:** Spatial locality is useful-byte reuse within transfer units.

### Example 2

**Question:** Why does stride equal to one line lower useful density?

**Reasoning:** Each access consumes one scalar from a new line; unless other fields are reused later, most transferred bytes are unused by the phase.

**Conclusion:** Access order and field set determine utilization.

### Example 3

**Question:** Why can independent random reads beat a linked chain with similar line count?

**Reasoning:** Their addresses are ready together, allowing MLP; each linked next address awaits the prior load.

**Conclusion:** Dependency structure is separate from spatial randomness.

### Example 4

**Question:** When does AoS beat SoA?

**Reasoning:** If every operation consumes nearly all small-record fields together, AoS brings one record in few lines and avoids coordinating multiple arrays.

**Conclusion:** SoA is not a universal default.

### Example 5

**Question:** What does a cache-miss counter need before interpretation?

**Reasoning:** Identify exact event/PMU, level, demand/prefetch, load/store, speculative/retired scope, process/privilege scope, multiplex scaling, and denominator.

**Conclusion:** A raw number without provenance is not evidence.

### Example 6

**Question:** Why can node pooling help a linked traversal?

**Reasoning:** Nodes may occupy fewer pages/lines and allocation metadata can shrink, while logical successor dependencies remain.

**Conclusion:** Placement improves locality without changing linked semantics.

### Example 7

**Question:** How is false sharing demonstrated?

**Reasoning:** Show independent per-thread writes land on one coherence line, observe scaling/coherence traffic, then separate fields without changing logic and reproduce improvement.

**Conclusion:** Timing suspicion alone is insufficient.

### Example 8

**Question:** Why can huge pages help and hurt?

**Reasoning:** They expand translation reach but can increase allocation latency, fragmentation, memory commitment, and operational complexity.

**Conclusion:** Translation optimization has system-level costs.

### Example 9

**Question:** What does the executable model's 8-versus-2 AoS/SoA line count prove?

**Reasoning:** Only that its assumed four-slot records and four-slot lines map selected `x` slots to those distinct identifiers.

**Conclusion:** It predicts a controlled hypothesis, not speed.

### Example 10

**Question:** A cache-tuned structure supports a medical device. What exceeds local counter evidence?

**Reasoning:** Engineers need worst-case timing/memory, hardware/firmware/toolchain identity, cold/warm/fault/concurrency traces, interrupt/DMA effects, cache/translation/coherence behavior, and safe fallback. Clinical, safety, security, human-factors, quality, and regulatory reviewers validate the integrated hazard case. This chapter claims none.

**Conclusion:** Microarchitectural optimization cannot establish medical safety or certification.

## Cross-Program Connections

- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns cache, TLB, prefetch, speculation, vectorization, coherence, and PMU design.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies paging, faults, scheduling, affinity, NUMA, and performance interfaces.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops false sharing, atomics, memory ordering, and scalable layout.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) connects cost models, cache-aware algorithms, and experiment design.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) governs reproducibility, statistics, and evidence.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns cache/timing side-channel threat models and mitigations.

## References

1. Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html). Architecture, memory hierarchy, performance monitoring, and event-model foundations.
2. AMD, [AMD uProf](https://www.amd.com/en/developer/uprof.html). Official profiling, CPU/event, memory, power, and analysis tooling/documentation portal.
3. Arm, [*Software Optimization Guide for the Arm Neoverse N-Series Processors*](https://developer.arm.com/documentation/102336/latest/). Official cache, prefetch, memory, vectorization, and tuning guidance.
4. Linux `perf`, [`perf stat` manual](https://man7.org/linux/man-pages/man1/perf-stat.1.html). Event counting, grouping, scope, interval, metric, and aggregation behavior.
5. Linux kernel community, [`perf` tutorial](https://perf.wiki.kernel.org/index.php/Tutorial). Counter collection, sampling, reporting, and event usage.
6. University of Tennessee, [Performance Application Programming Interface](https://icl.utk.edu/projects/papi/). Portable performance-counter API and component/event model.
7. Valgrind Project, [Cachegrind manual](https://valgrind.org/docs/manual/cg-manual.html). Explicit cache/branch simulation model, events, annotation, and limitations.
8. LLVM Project, [Auto-Vectorization in LLVM](https://llvm.org/docs/Vectorizers.html). Loop/SLP vectorization, legality, profitability, diagnostics, and runtime checks.
9. Google Benchmark Project, [User Guide](https://google.github.io/benchmark/user_guide.html). Benchmark timing, repetitions, counters, complexity, and reporting.
10. Samuel Williams, Andrew Waterman, and David Patterson, [*Roofline: An Insightful Visual Performance Model for Multicore Architectures*](https://doi.org/10.1145/1498765.1498785). Arithmetic intensity and bandwidth/compute performance ceilings.

## Exercises

### Exercise 1

For line size (B), element size (s), and aligned array of (n) elements, derive distinct-line footprints for sequential access and stride (k). State alignment/crossing caveats.

### Exercise 2

Design equivalent AoS, SoA, and AoSoA layouts for particles with six numeric fields when a kernel reads four fields and writes three. Predict useful-byte footprints and identify confounders before benchmarking.

### Exercise 3

Construct two traces with the same distinct-line set: one independent gather and one dependent successor chain. Explain why runtime can differ and how to measure dependency effects.

### Exercise 4

Prepare a false-sharing investigation for per-thread counters. Include correctness, layout evidence, events, equivalent controls, statistics, and alternative explanations.

### Exercise 5

Prepare a production review plan for changing a critical structure from pointer nodes to compact indices for locality. Cover semantics, handles, measurement, hardware diversity, concurrency, security, rollout, and human review.

## Answers to the Exercises

### Answer 1

If the base and every element are aligned so elements do not cross lines and $s$ divides (B), let (q=B/s) elements fit per line. Sequential indices `0..n-1` touch $\lceil n/q\rceil$ lines. Stride (k) visits $m=\lceil n/k\rceil$ elements and touches the cardinality of ${\lfloor jk/q\rfloor:0\le j<m}$; when $k\ge q$, usually each access has a distinct line, while smaller strides reuse according to the set. A misaligned base, elements crossing lines, padding, fields rather than whole elements, and virtual/page mapping require interval-based calculation and can add lines.

### Answer 2

AoS stores six fields per record; a kernel needing four reads and three writes may transfer unused fields/padding but keeps record fields together. SoA stores six field arrays and touches only the required arrays, enabling dense field streams, but issues several streams and synchronizes indices. AoSoA stores six small field arrays per block sized for vector/cache goals. Calculate line intervals from actual field width, record padding, alignment, block size, read-for-ownership/write policy, and reuse. Before causal comparison, equalize algorithm, native language, data type, compiler/flags, vectorization, alignment, initialization, result validation, threads, working set, and target; inspect generated code and allocations.

### Answer 3

Choose one address in each of (m) lines. The gather receives all (m) addresses in an index array before loads; the chain stores the next address in the current node. Both touch the same modeled line set, but the gather can maintain several outstanding misses while the chain cannot reveal load (i+1) until load (i) completes. Implement equivalent native kernels, validate sums, randomize layout identically, pin environment, vary independent stream count, and record cycles, instructions, target-specific outstanding/stall/cache/TLB events plus wall-time distributions. The experiment remains target-specific and counter semantics must be documented.

### Answer 4

First prove counters are race-free and independently owned. Inspect/record addresses, sizes, alignment, and coherence-line assumptions showing multiple writers share a line. Benchmark scaling across threads with affinity and controlled work, collecting wall time and target-supported coherence/cache events with raw provenance. Create an equivalent padded/separated variant preserving algorithm and synchronization; also test read-only, one-thread, and intentionally true-shared controls. Repeat across placements and working sets, report distributions and memory increase. Rule out contention on locks/atomics, scheduler migration, NUMA placement, frequency, allocator adjacency, and benchmark bugs. Improvement plus reduced coherence evidence supports diagnosis but is not universal proof.

### Answer 5

Freeze abstract behavior, ordering, errors, capacity, serialization, iterator/view and handle semantics. Define index bounds, generation/reuse, compaction, overflow, allocation/failure, and corruption validation; migrate external raw addresses through a compatibility layer or reject the change if stable address identity is contractual. Prove representation correspondence and concurrency/reclamation behavior. Differentially model-test traces and stale/forged handles; fuzz corrupt persisted data; inject allocation/cancellation/failure. Benchmark target workloads across supported CPU/OS/topology classes with cold/warm sizes, scans, updates, tails, counters, memory and energy where relevant, preserving raw evidence. Review side-channel and adversarial locality changes. Use versioned rollout, telemetry, rollback, mixed-version testing, and artifact identity. Independent data-structure, architecture, concurrency, systems, security, operations, domain, safety/quality and regulatory reviewers approve their scopes; no local speedup alone justifies production release.
