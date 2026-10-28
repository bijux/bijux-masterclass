---
module_id: CA-031
program: Computer Architecture
level: 1
module_number: 31
title: Locality and the Memory Wall
status: complete
last_verified: 2026-09-04
---

# Locality and the Memory Wall

## One-Page Review

### Governing question

How do access order, working set, transfer granularity, available concurrency and computation per byte determine whether a program is served by nearby storage or limited by latency, bandwidth, traffic amplification and the growing cost gap between computation and data movement?

### Essential definitions

- **locality** is predictable concentration of references in address and time; it is a workload property relative to an execution/memory system.
- **temporal locality** is reuse of recently accessed data or instructions.
- **spatial locality** is access to addresses near a recent reference, often exploited by fixed-size blocks.
- A **working set** is the data/instruction footprint actively reused over a declared interval or reuse window.
- **reuse distance** is the amount of distinct intervening data referenced between accesses to the same item/block under a defined model.
- A **cache line/block** is the granularity transferred and managed by a cache level.
- **hit rate** is the fraction of accesses found at a level under a stated denominator; **miss rate** is its complement for that classification.
- **miss penalty** is additional service time/work after a miss, including lower levels and queuing under the chosen model.
- **average memory access time** (`AMAT`) combines hit time and conditional miss behavior; it does not describe tails or overlap by itself.
- **memory-level parallelism** (`MLP`) is the number of useful memory operations/misses overlapped.
- **bandwidth** is data transferred per unit time; usable bandwidth depends on direction, concurrency, size and system conditions.
- **arithmetic intensity** is useful operations divided by bytes transferred across a named memory boundary.
- The **roofline bound** is `min(peak compute, arithmetic intensity * sustainable bandwidth)` under explicit units/scope.
- **traffic amplification** is transferred bytes divided by useful bytes.
- The **memory wall** describes performance/energy pressure when processor capability outpaces effective memory access, making data movement dominant.

### Central model, mechanism, or theorem

For an exclusive outcome model with access classes `i`, probabilities `p_i` summing to one, and end-to-end latencies `L_i`, serial mean latency is `AMAT=sum_i p_i L_i`. This applies only when the classified latency is not hidden by overlap. Throughput is separately bounded by available MLP, queue/service limits and sustainable bandwidth. For a kernel transferring `B` bytes and doing `O` useful operations, intensity `AI=O/B`; attainable operation rate is bounded by `min(P_peak, AI*BW_sust)`. Locality improves these bounds when reuse or useful neighboring bytes reduce lower-level traffic, but line overfetch, conflicts, coherence and prefetch can increase traffic.

### Critical invariants

- Locality claims name address stream, block/page granularity, cache/topology and observation window.
- Working-set and reuse metrics distinguish logical objects from transferred blocks.
- Hit/miss rates use consistent access denominators and conditional level semantics.
- AMAT latency terms match whether lower-level time is incremental or end-to-end.
- Serial-latency models are not used as throughput models when misses overlap.
- Bandwidth uses bytes crossing the named boundary, not only useful source bytes.
- Arithmetic intensity and compute/bandwidth peaks use compatible operations, bytes and seconds.
- Prefetch/coherence/writeback traffic is included where it consumes the constrained boundary.
- Optimizations preserve program results and compare identical useful work.
- Conclusions bind to exact working sets, access patterns, hardware/software state and uncertainty.

### Common failures

Common failures include calling sequential access local without naming line/page size, equating small arrays with cache residency, computing miss rate from misses per instruction while comparing accesses, adding unconditional miss penalties twice, using AMAT to predict bandwidth-saturated throughput, calling advertised channel rate sustainable bandwidth, counting requested bytes instead of transferred lines, ignoring write allocation/writeback/coherence/prefetch traffic, assuming MLP helps pointer chasing, increasing arithmetic intensity on paper without reducing boundary bytes, measuring a warmed cache while claiming cold behavior, and diagnosing “memory-bound” from one high cache-miss counter.

### Compact example

An illustrative exclusive distribution of 92% L1 service at 1 ns, 6% lower-cache service at 5 ns and 2% memory service at 80 ns gives serial AMAT 2.82 ns, or 354.61 million dependent accesses/s. Eight-way MLP could expose more concurrency, but 40 GB/s divided by 64-byte fills caps line service at 625.00 million/s. A kernel at 0.5 operations/byte on 40 GB/s has a 20 GOPS bandwidth roof under a 200 GOPS compute peak; tiling to 4 operations/byte raises the roof to 160 GOPS if boundary traffic really falls. A stride-one 8 KiB useful scan transfers 128 lines; a same-work stride-eight pattern can transfer 1,024 lines, eightfold amplification.

### Connections

Locality connects cache mapping/replacement, virtual memory/TLBs, prefetching, memory controllers, compiler loop/data layout, data structures, NUMA/coherence, roofline analysis, energy and workload measurement.

## Governing Question

Processors can execute arithmetic far faster than a dependent access to distant memory. Hierarchies exploit locality by keeping useful data near computation and transferring blocks. Their effectiveness depends on the actual address stream and concurrency.

“Memory-bound” is not one state. A program may be latency-bound by a dependency chain, bandwidth-bound by streaming traffic, capacity/conflict-bound by working set, translation-bound, coherence-bound or limited by insufficient outstanding requests. Remedies differ.

## Why This Matters

Data movement costs time, bandwidth and energy. Faster compute raises the fraction of time spent waiting unless memory service, reuse or concurrency improves. A high hit rate can still hide expensive rare misses; high bandwidth can coexist with long dependent latency.

Software structure matters as much as nominal hardware. Loop order, layout, blocking, allocation, page placement and sharing determine whether transfers contain useful work.

Measurement must follow real boundaries. Cache counters and bandwidth tools use model-specific definitions; simulation, microbenchmarks and applications answer different questions.

## Prerequisites and Retrieval

Before studying this module, be able to:

- distinguish latency from throughput and arithmetic work from data movement;
- compute weighted expectations and unit conversions;
- reason about arrays, pointers, strides and address ranges;
- interpret counters and workload measurement boundaries;
- explain basic pipeline stalls and overlap.

Retrieve exact processor/memory hierarchy and topology; cache/TLB sizes, associativity, line/page sizes, inclusivity, write/replacement/prefetch policies; memory channels/ranks/banks and sustainable bandwidth; request/queue/MSHR limits; load/store/atomic mix and sizes; address/stride/reuse/working-set traces; instruction/data traffic; read-for-ownership, writeback and coherence traffic; virtual/physical placement, NUMA and huge pages; compiler/runtime/binary/data layout; cold/warm protocol; frequency/power/thermal state; counter event semantics and multiplexing; raw latency/bandwidth/traffic/operations data; benchmark inputs/seeds; simulation/model assumptions; correctness checks; hardware/firmware/kernel/tool versions and errata.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish temporal and spatial locality at explicit granularities;
2. characterize working sets, strides and reuse distance;
3. compute AMAT with correct conditional/exclusive semantics;
4. separate dependent latency from MLP and bandwidth limits;
5. compute arithmetic intensity, traffic amplification and roofline bounds;
6. explain cache-line overfetch, write and coherence traffic;
7. select loop/data-layout/blocking/prefetch remedies for diagnosed limits;
8. design cold/warm, footprint and concurrency experiments;
9. avoid causal claims from ambiguous counter correlations;
10. bind memory-wall conclusions to exact systems and workloads.

## Core Exposition

### Start with the address stream

The memory hierarchy sees instruction and data addresses, operation types, sizes, timing and context—not source-level variable names. Construct or measure the reference stream for the region of interest.

Compiler transformations, allocation and virtual-to-physical mapping can change the stream. Inspect generated code and runtime layout when conclusions depend on it.

### Define temporal locality

Temporal locality exists when a referenced block is reused before eviction or invalidation. Reuse time in cycles is less portable than reuse distance over distinct intervening blocks, but both need a declared block granularity.

A frequently reused object can still miss if competing blocks map to the same set or other agents invalidate it.

### Define spatial locality

Spatial locality means transferred neighboring bytes are likely to be used before eviction. Sequential access often exploits a line after the first miss; a sparse stride may fetch mostly unused bytes.

Larger blocks capture more nearby data but increase miss latency, capacity pressure, traffic and false sharing. Spatial is not automatically beneficial.

### Define the working set

A working set is the distinct footprint actively needed over a window. “Fits in cache” requires usable capacity after associativity, other data/instructions, metadata, sharing and policy—not only nominal bytes.

Sweep footprint and repetition to locate transitions. Report line/page/object footprints separately where relevant.

### Measure reuse distance

For each repeated block reference, count distinct intervening blocks under the chosen trace model. A fully associative LRU cache of capacity greater than reuse distance would retain it, aside from coherence/prefetch effects.

Real set-associative/random/pseudo-LRU caches differ, but reuse-distance curves provide a workload-centered baseline.

### Distinguish compulsory, capacity and conflict effects

Compulsory misses fetch a block not previously resident in the considered execution. Capacity misses arise when the active distinct footprint exceeds usable storage. Conflict misses arise from mapping restrictions.

This classification depends on a reference model and can become ambiguous with prefetch, coherence and multiple levels. State the classifier rather than treating names as hardware facts.

### Understand hierarchy latency

Each level includes lookup/access and possible lower-level service. Define whether `L2 latency` is additional after L1 miss or total from original request. Mixing the two double-counts.

Queueing, bank conflicts, translation, coherence and memory-controller scheduling make latency a distribution. AMAT is a mean model, not a tail guarantee.

### Compute AMAT carefully

A nested model can be `T_L1 + m_L1*(T_L2 + m_L2*T_mem)` when miss rates are conditional and penalties incremental. An exclusive outcome model uses total probabilities and end-to-end latencies.

Validate probabilities sum correctly. Report which access classes, writes and prefetches are included.

### Separate latency from overlap

A pointer chain exposes dependent latency because the next address awaits the current load. Independent array streams can maintain many outstanding misses, hiding individual latency until queue/bandwidth limits.

AMAT times access count overpredicts elapsed time when overlap is substantial and underrepresents queueing under saturation.

### Measure memory-level parallelism

MLP is useful outstanding concurrency, not simply queue depth. Dependencies, branch uncertainty and issue windows limit how many misses can coexist.

Measure outstanding-request distribution and service overlap. Increasing MSHRs helps only if software/core can generate independent requests and downstream capacity exists.

### Define sustainable bandwidth

Peak pin/channel rate is an upper interface bound. Sustainable application bandwidth is lower due to protocol overhead, direction changes, bank conflicts, refresh, controller policy, topology and other traffic.

Measure read, write and mixed patterns across concurrency, sizes, placement and duration. Record whether bytes are payload, cache-line transfers or controller traffic.

### Compute traffic amplification

If an 8-byte load causes a 64-byte line fill and no neighbor is used, read traffic amplification is eight before page-table/coherence effects. Reuse can amortize the fill across several loads.

Writes may trigger read-for-ownership plus later writeback. Non-temporal/streaming policies can reduce allocation traffic when semantics and alignment permit.

### Define arithmetic intensity

Arithmetic intensity is useful operations per byte transferred across a named boundary. Algorithmic source bytes, L1 bytes and DRAM bytes yield different intensities.

Count operations consistently—FLOPs, integer operations or domain work—and preserve correctness. Inflating operation count without useful output does not improve performance value.

### Apply the roofline bound

At low `AI`, `AI*BW` is below compute peak and the model predicts a bandwidth roof. At high `AI`, compute peak dominates. The ridge point is `P_peak/BW`.

Use sustainable workload-relevant bandwidth and achievable compute peak under the same data type/instruction mix. A roofline is an upper-bound model, not a prediction of measured performance.

### Add ceilings deliberately

Instruction mix, vectorization, issue width, cache bandwidth, NUMA links or dependency constraints can add ceilings below the simple roof. Each ceiling needs measured/validated capacity and applicability.

Avoid drawing many ceilings from unrelated benchmarks. Same hardware state and units are essential.

### Explain the memory wall

As compute throughput improves faster than effective dependent memory service, even small miss probabilities consume growing processor-time equivalents. Hierarchies, speculation and concurrency mitigate but do not erase data-movement cost.

Energy and capacity scaling strengthen the issue: moving data far can cost more than arithmetic. Architecture/software co-design targets reuse, placement, compression and near-data work.

### Improve loop order

Traverse the contiguous dimension innermost for row/column-major layout as appropriate. Interchange can convert large-stride misses into line reuse.

Check dependencies before reordering. Vectorization and parallel scheduling interact with cache lines and false sharing.

### Block or tile reuse

Tiling processes chunks sized so reused operands remain in a target cache/register level. It reduces lower-boundary bytes and raises arithmetic intensity when the algorithm reuses data.

Choose tile sizes using actual associativity, multiple arrays, line/page mapping and thread sharing. Edge tiles and packing overhead count.

### Improve data layout

Array-of-structures helps when most fields of each object are consumed together; structure-of-arrays helps vectorized/field-specific scans. Padding/alignment can prevent conflicts or waste capacity.

Pointer-rich structures create dependent, scattered accesses. Compact indices, arenas or reordered nodes can improve locality while changing update/complexity trade-offs.

### Use prefetch carefully

Hardware/software prefetch can hide predictable latency by fetching before demand. It needs enough lead time and accuracy without exhausting bandwidth, cache capacity or request entries.

Report coverage, accuracy, timeliness and pollution. Wrong-path/useless prefetches consume shared resources and may affect security.

### Increase useful concurrency

Unroll, software pipeline, batch or use independent streams to create MLP. Wider out-of-order windows and more request entries can overlap misses.

Concurrency cannot break a true address dependency. It also increases queueing and may saturate bandwidth, worsening tail latency.

### Manage instruction locality

Large code footprints, inlining and layout affect instruction caches/TLBs and branch prediction. An optimization reducing data misses can grow code enough to shift the bottleneck.

Measure instruction and data paths separately and jointly. Front-end misses reduce the core's ability to generate MLP.

### Include translation

TLB misses trigger page walks whose accesses use caches/memory. Page size changes reach, fragmentation, fault cost and placement.

Huge pages can reduce translation misses but do not guarantee data-cache locality and may complicate NUMA/memory management.

### Include coherence and sharing

Multiple cores can invalidate/transfer lines. False sharing moves a line when threads update unrelated words within it; logical independence does not imply physical independence.

Measure coherence traffic and placement. Padding can help false sharing while increasing footprint and TLB/cache pressure.

### Include NUMA/topology

Remote memory has different latency/bandwidth and shares links. First-touch/allocation/migration policy determines physical placement, while threads may move.

Record CPU/memory affinity and topology. Aggregate bandwidth can hide one socket's remote bottleneck.

### Measure latency regimes

Use dependency chains for exposed latency, random/stride/footprint sweeps for hierarchy transitions, and distributions for queue/tail behavior. Prevent compiler elimination and validate loads.

Subtract overhead only when independently characterized. Pointer construction can itself change layout/prefetch predictability.

### Measure bandwidth regimes

Use sufficiently long streaming kernels, several operation mixes and concurrency sweeps. Confirm working set exceeds the level whose bandwidth is being tested and account for write allocation.

Report useful and transferred bytes. Validate counter events and compare wall-time rates against controllers/sockets.

### Measure applications

Microbenchmarks establish capacities; applications establish relevance. Capture working-set phases, address/operation distributions and service constraints.

Do not apply a STREAM number directly to irregular pointer-chasing or a single-core workload without testing applicability.

### Attribute without overclaiming

Cache/TLB/memory counters correlate with execution. Use controlled interventions—tile size, layout, footprint, prefetch, placement—to test a suspected mechanism.

One miss can overlap another or useful compute. Stall-cycle and bandwidth observations need timeline/queue context.

### Preserve reproducibility

Record CPU/topology/cache/memory, firmware/microcode, kernel, mitigations, compiler/runtime, binary, data layout/input, affinity/NUMA, governor/frequency, thermal state, commands, counters, seeds and raw traces.

Report repetitions, uncertainty, cold/warm rules and failures. Scope conclusions to tested systems and phases.

### Verify correctness and safety

Loop/layout/prefetch changes must preserve results, memory ordering and bounds. Padding/packing must not break ABI/persistence/wire formats.

Speculative/prefetch and shared-cache behavior can expose side channels. Performance evidence does not establish security noninterference.

## Definitions and Notation

- `p_i`: probability/fraction of exclusive memory-service outcome `i`.
- `L_i`: end-to-end latency for outcome `i` in the chosen model.
- `AMAT=sum_i p_i L_i`: serial expected service time under stated assumptions.
- `MLP`: useful overlapped memory-operation count/distribution.
- `BW_sust`: sustainable transferred-byte rate at a named boundary.
- `O`, `B`: useful operations and transferred bytes.
- `AI=O/B`: arithmetic intensity at that boundary.
- `P_peak`: applicable achievable compute-rate ceiling.
- `P_roof=min(P_peak,AI*BW_sust)`.
- `A=bytes_transferred/bytes_useful`: traffic amplification.
- **block/line:** transfer and cache-management granularity.
- **footprint:** distinct bytes/blocks/pages touched in a region.
- **stride:** address increment between successive logical accesses.
- **reuse window:** interval over which active reuse is characterized.
- **ridge point:** arithmetic intensity where bandwidth and compute roofs intersect.

## Mechanisms, Invariants, or Proof Structure

1. **Stream obligation:** claims derive from the actual instruction/data address-operation stream.
2. **Granularity obligation:** locality, footprint, reuse and traffic use explicit byte/line/page boundaries.
3. **Probability obligation:** hit/miss/outcome rates share correct denominators and conditional/exclusive semantics.
4. **Latency obligation:** AMAT components are incremental or end-to-end consistently and include stated queue effects.
5. **Overlap obligation:** dependent latency and MLP/bandwidth throughput models are not conflated.
6. **Traffic obligation:** fills, write allocation/writeback, prefetch, coherence and page-walk bytes are included as scoped.
7. **Intensity obligation:** useful operations and boundary bytes use compatible units and identical work.
8. **Roof obligation:** compute/bandwidth ceilings are sustainable/applicable to the same system state.
9. **Placement obligation:** mapping, associativity, banks, pages, NUMA and sharing are identified.
10. **Optimization obligation:** loop/layout/tile/prefetch changes preserve correctness and measure overhead.
11. **Measurement obligation:** cold/warm state, footprint, concurrency, frequency and counters are controlled/validated.
12. **Attribution obligation:** causal bottleneck claims use interventions or remain explicitly correlational.
13. **Distribution obligation:** latency/bandwidth variation, tails and phase behavior accompany averages.
14. **Security/order obligation:** speculative movement and transformations respect memory/ABI/security constraints.
15. **Evidence obligation:** conclusions bind to exact hardware/software/workload identities and raw artifacts.

## Alternatives and Trade-Offs

1. **Latency versus bandwidth optimization:** dependency chains need lower latency; streams need sustainable bandwidth/concurrency.
2. **Small versus large lines:** small lines reduce overfetch; large lines exploit spatial reuse/amortize tags.
3. **Capacity versus access time:** larger caches hold more working set and can cost latency/energy.
4. **Associativity versus simplicity:** associativity reduces conflicts; direct mapping shortens lookup and may thrash.
5. **Hardware versus software prefetch:** hardware adapts transparently; software expresses intent with portability/timing risk.
6. **Prefetch versus demand-only:** prefetch hides latency; useless requests consume traffic/capacity.
7. **Blocking versus streaming:** blocking raises reuse; streaming can simplify bandwidth-efficient one-pass work.
8. **AoS versus SoA:** object grouping favors whole-record access; field arrays favor scans/vectorization.
9. **Pointer versus compact-index structures:** pointers ease updates; compact layout improves locality and relocation complexity.
10. **Replication versus sharing:** replication gives local reads; coherence/space/update cost grows.
11. **Huge versus base pages:** huge pages extend TLB reach; base pages reduce fragmentation and migration granularity.
12. **Local versus remote NUMA placement:** local minimizes latency; interleaving may spread bandwidth.
13. **More MLP versus queue control:** concurrency hides latency; saturation raises queueing/tails.
14. **Peak versus sustainable rates:** peak bounds communicate hardware potential; sustainable rates model workloads.
15. **Microbenchmark isolation versus application realism:** isolation diagnoses limits; applications validate relevance.

## Failure Modes and Misconceptions

1. “Locality means nearby source-code variables.” It concerns executed address references at a granularity.
2. “Sequential access always hits.” First touches and footprints still miss.
3. “Small data fits in cache.” Associativity, sharing and other occupants reduce usable capacity.
4. “Temporal reuse guarantees a hit.” Eviction/invalidation can intervene.
5. “Spatial locality makes larger lines better.” Overfetch and capacity pressure can dominate.
6. “Hit rate alone determines speed.” Miss cost, overlap and bandwidth matter.
7. “L1/L2 miss rates have the same denominator.” Local/global/conditional rates differ.
8. “AMAT times accesses always predicts runtime.” Overlap and queueing violate serial assumptions.
9. “Low AMAT means high bandwidth.” Latency and sustained transfer capacity differ.
10. “Many outstanding requests guarantee MLP.” Dependencies or serialization can prevent useful overlap.
11. “Peak channel bandwidth is available to one kernel.” Protocol/topology/contention reduce it.
12. “Bytes requested equal bytes transferred.” Lines, ownership, writeback, prefetch and walks amplify traffic.
13. “Stores only write their payload.” Write allocation/read ownership and eviction add traffic.
14. “Arithmetic intensity is intrinsic to an algorithm.” Boundary, implementation and reuse determine it.
15. “More FLOPs improve intensity.” Only useful equivalent work counts.
16. “Roofline predicts performance exactly.” It supplies bounds under assumptions.
17. “Below a roof proves the named bottleneck.” Other ceilings/dependencies can dominate.
18. “Prefetch always helps regular accesses.” Timing, bandwidth and pollution determine value.
19. “Pointer chasing can be fixed with more bandwidth.” True address dependencies expose latency.
20. “Tiling works if one tile is below cache size.” Multiple arrays, sets and sharing matter.
21. “Huge pages improve data-cache locality.” They primarily change translation reach/placement.
22. “Padding always removes false sharing profitably.” It increases footprint and may shift limits.
23. “STREAM predicts every memory workload.” It measures specific streaming regimes.
24. “One cache-miss counter proves memory-bound.” Semantics/overlap/intervention are needed.
25. “Warm results describe cold start.” State protocols answer different questions.
26. “One machine's hierarchy result generalizes.” topology, memory, firmware and workload vary.

## Worked Examples

### Example 1

A loop repeatedly sums one 4 KiB array. After warm-up, temporal reuse can keep lines resident if conflicts and other occupants do not evict them.

### Example 2

A stride-one scan of 8-byte elements uses all eight values in each 64-byte line; a stride-eight scan can use one value per line and amplify traffic eightfold.

### Example 3

A linked-list traversal has one dependent next pointer per node. More memory channels do not expose concurrency without independent lists or lookahead.

### Example 4

Eight independent streams create MLP and hide some 80 ns latency until line-rate bandwidth or request queues saturate.

### Example 5

Loop interchange converts a column traversal of row-major data into row traversal, reducing line/page churn after dependency validation.

### Example 6

Matrix tiling reuses blocks in cache, reducing DRAM bytes and raising arithmetic intensity; packing/edge overhead is included.

### Example 7

A prefetcher covers most demand misses but doubles transferred bytes and slows a bandwidth-saturated peer. Accuracy alone is insufficient.

### Example 8

Two threads update separate counters on one line. Coherence transfers show false sharing despite no source-level shared field.

### Example 9

A page-walk-heavy workload improves with larger pages, but NUMA misplacement then raises remote data latency; measurement must cover both.

### Example 10

This deterministic model computes serial AMAT, MLP/bandwidth and roofline bounds plus stride traffic amplification.

<!-- bijux-verify: {"id":"locality-memory-wall-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"amat_ns=2.82 serial_mops=354.61 mlp8_bandwidth_limited_mops=625.00\nlow_intensity_roof_gops=20.00 measured_efficiency_pct=75.00\ntiled_roof_gops=160.00 measured_efficiency_pct=75.00\nstride1_lines=128 traffic_bytes=8192 amplification=1.00\nstride8_lines=1024 traffic_bytes=65536 amplification=8.00\n"}} -->
```python
outcomes = [(0.92, 1.0), (0.06, 5.0), (0.02, 80.0)]
amat_ns = sum(probability * latency for probability, latency in outcomes)
serial_mops = 1000 / amat_ns
bandwidth_gbs = 40.0
line_bytes = 64
line_rate_mops = bandwidth_gbs * 1000 / line_bytes
mlp8_mops = min(8 * serial_mops, line_rate_mops)

compute_peak_gops = 200.0
low_ai = 0.5
tiled_ai = 4.0
low_roof = min(compute_peak_gops, low_ai * bandwidth_gbs)
tiled_roof = min(compute_peak_gops, tiled_ai * bandwidth_gbs)

useful_bytes = 8192
stride1_lines = useful_bytes // line_bytes
stride8_lines = useful_bytes // 8
stride1_traffic = stride1_lines * line_bytes
stride8_traffic = stride8_lines * line_bytes

print(f"amat_ns={amat_ns:.2f} serial_mops={serial_mops:.2f} mlp8_bandwidth_limited_mops={mlp8_mops:.2f}")
print(f"low_intensity_roof_gops={low_roof:.2f} measured_efficiency_pct={100 * 15 / low_roof:.2f}")
print(f"tiled_roof_gops={tiled_roof:.2f} measured_efficiency_pct={100 * 120 / tiled_roof:.2f}")
print(f"stride1_lines={stride1_lines} traffic_bytes={stride1_traffic} amplification={stride1_traffic / useful_bytes:.2f}")
print(f"stride8_lines={stride8_lines} traffic_bytes={stride8_traffic} amplification={stride8_traffic / useful_bytes:.2f}")
```

The probabilities, latencies, peaks and measured rates are invented. The model establishes arithmetic and limiting relationships only.

## Cross-Program Connections

- **Data Structures:** layout, indirection and traversal determine locality and dependency chains.
- **Algorithms:** blocking/reuse can change boundary traffic without changing asymptotic operation count.
- **Compilers:** loop transformations, vectorization, inlining and prefetch change streams and code footprint.
- **Operating Systems:** page size, allocation, NUMA placement and scheduling shape physical locality.
- **Concurrent Systems:** sharing/coherence, queueing and contention alter latency/bandwidth.
- **Security Engineering:** shared caches, prefetch and speculation can expose timing information.
- **Performance Engineering:** roofline, counters, microbenchmarks and interventions support bounded diagnosis.
- **Systems Engineering:** topology, firmware, software, workload and evidence ownership jointly bound claims.

## References

1. Wm. A. Wulf and Sally A. McKee, [Hitting the Memory Wall: Implications of the Obvious](https://libraopen.lib.virginia.edu/public_view/k35694375), University of Virginia repository record for the foundational report; retrieved 2026-09-04 (HTTP 202 accepted response).
2. Lawrence Berkeley National Laboratory, [The Roofline Model: Visualizing and Optimizing Performance](https://amcr.lbl.gov/departments/computer-science-department/ppan/roofline-performance-model/), current model overview and applications; retrieved 2026-09-04.
3. John D. McCalpin, [STREAM: Sustainable Memory Bandwidth in High Performance Computers](https://www.cs.virginia.edu/stream/), benchmark source, rules and results context; retrieved 2026-09-04.
4. Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), current architectural memory/counter foundations; retrieved 2026-09-04.
5. Standard Performance Evaluation Corporation, [SPEC CPU 2017 Overview](https://www.spec.org/cpu2017/Docs/overview.html), benchmark workload and run/rate context; retrieved 2026-09-04.
6. Linux perf community, [Perf Tutorial](https://perf.wiki.kernel.org/index.php/Tutorial), cache/PMU counting and sampling usage; retrieved 2026-09-04.
7. RISC-V International, [Vector Extension](https://docs.riscv.org/reference/isa/unpriv/v-st-ext.html), current vector memory-access and strided/indexed operation semantics; retrieved 2026-09-04.
8. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), memory-hierarchy teaching resources; retrieved 2026-09-04.

## Exercises

### Exercise 1

Characterize temporal/spatial locality, line traffic and reuse distance for stride-one, stride-eight and linked-list traversals.

### Exercise 2

Construct nested and exclusive-outcome AMAT models for a three-level hierarchy and state when neither predicts elapsed throughput.

### Exercise 3

Use roofline reasoning to compare an untiled and tiled kernel, including useful work, boundary bytes, sustainable bandwidth and compute peak.

### Exercise 4

Extend the executable model with write allocation and writeback traffic, then recompute amplification and the bandwidth roof.

### Exercise 5

Write a measurement/assurance plan to distinguish latency-, bandwidth-, capacity-, translation- and coherence-limited behavior.

## Answers to the Exercises

### Answer 1

At 8-byte elements/64-byte lines, stride one consumes eight adjacent elements per fill, so a long scan has strong spatial use but little temporal reuse unless repeated. Stride eight touches one element per line, yielding roughly eightfold line traffic for equal useful elements. Reuse distance for a repeated scan approximates the number of distinct lines in its footprint.

A linked list's spatial use depends on allocator layout; random nodes can use few bytes per line. It has temporal reuse only if nodes repeat before eviction and exposes dependent latency. Measure physical lines/pages, not source nodes alone.

### Answer 2

Nested incremental form is `T1 + m1*(T2 + m2*Tmem)` when `m2` is conditional on L1 miss. Exclusive form sums total outcome probability times end-to-end latency. Translate between them carefully and include translation/coherence/queue terms as scoped.

Neither predicts elapsed throughput when independent misses overlap substantially, bandwidth/queues saturate, latency distributions/tails dominate or access phases differ. Add MLP/service-capacity/queue models and validate with traces.

### Answer 3

For each version count identical useful operations and bytes crossing the selected boundary. Compute `AI=O/B`, measure sustainable bandwidth and applicable compute peak in compatible units, then roof `min(Ppeak,AI*BW)`. Tiling is supported only if measured boundary bytes fall and overhead/results are accounted.

Compare measured rate to each roof and other ceilings. A higher roof is opportunity, not proof of achieved speedup; verify cache capacity/associativity, vectorization, instruction count, clock, energy and end-to-end time.

### Answer 4

For stores that miss and write-allocate, add one full ownership/fill line even if only a word changes; add a later dirty full-line writeback. Combine with demand-load, prefetch, coherence and page-walk bytes. Amplification is total constrained-boundary traffic divided by useful bytes.

Recompute `AI` using the expanded denominator and then `AI*BW`. If streaming/non-temporal stores legally avoid allocation, model their protocol overhead separately and validate actual mapped behavior/counters.

### Answer 5

Sweep dependent-chain latency across footprints/pages; stream read/write/mixed bandwidth across threads/placement; sweep cache-sized footprints/strides/associativity stress; vary pages/TLB reach; and run true/false-sharing patterns. Capture outstanding requests, queueing, cache/TLB/coherence/traffic counters with validated semantics and wall-time latency/throughput.

Use controlled interventions: independent streams for MLP, tiling/layout for reuse, page size/placement for translation/NUMA, padding/ownership for coherence, and prefetch toggles. Preserve correctness, raw traces, cold/warm rules, repetitions/tails and exact CPU/topology/memory/firmware/kernel/compiler/binary/input/affinity/frequency/thermal/tool identities. State counter/model limits and make no independent certification claim.
