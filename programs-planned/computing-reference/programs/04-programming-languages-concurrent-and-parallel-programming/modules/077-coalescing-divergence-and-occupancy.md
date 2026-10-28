---
module_id: CONPAR-077
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 77
title: Coalescing, Divergence, and Occupancy
status: complete
last_verified: 2026-08-29
---

# Coalescing, Divergence, and Occupancy

## One-Page Review

### Governing question

How can a GPU kernel turn lane-level work into useful memory transactions and instructions while retaining enough resident, ready work to hide latency—without treating any single utilization metric as the objective?

### Essential definitions

- **Coalescing** combines memory requests from active lanes into the transactions required by the target memory system.
- **Useful-byte efficiency** is useful requested bytes divided by bytes transferred at a declared memory boundary.
- A **memory transaction** is a target-specific transfer unit; its segment, sector, cache-line, and request behavior must not be universalized.
- **Divergence** occurs when lanes in an execution group follow different control paths or take different amounts of work.
- An **active mask** identifies lanes participating in an issued instruction or collective.
- **Predication** issues an operation under a lane mask instead of taking an ordinary control-flow branch.
- **Static or theoretical occupancy** is resident active warps/waves divided by the architectural maximum, under a particular kernel and launch configuration.
- **Achieved occupancy** is a measured average of active warps/waves relative to the target maximum during execution.
- **Latency hiding** schedules other ready instructions or execution groups while one operation waits.
- **Instruction-level parallelism (ILP)** supplies independent operations within a lane/thread; **memory-level parallelism (MLP)** supplies multiple outstanding memory operations.
- A **resource cliff** is a small change in block size, registers, shared memory, or allocation granularity that lowers resident blocks/waves discretely.
- **Tail effect** is underutilization when the final scheduling waves contain too few blocks or lanes to fill the device.

### Central model, mechanism, or theorem

Analyze three separate ledgers. The transaction ledger maps every active lane address to target transactions and computes useful versus transferred bytes. The control ledger records active masks and useful lane-instructions for each path. The residency ledger computes legal resident blocks from thread, warp/wave, block, register, shared-memory, and target-specific constraints. These ledgers interact but cannot be multiplied into a universal speed formula. Coalescing may reduce requests; less divergence may increase useful issued work; sufficient residency may hide a remaining latency. Actual time still depends on cache hits, dependencies, instruction mix, pipelines, memory concurrency, scheduling, tails, and the measured bottleneck.

### Critical invariants

Every active lane address is valid and belongs to the intended logical item; inactive lanes cause no invalid memory effect; alignment, width, stride, pitch, and transaction assumptions name the target; stores preserve ownership and do not create races; collective masks name exactly the participating lanes; work-group barriers remain convergent; control transformations preserve exceptions, numeric semantics, and side effects; launch arithmetic and all resource limits are checked; at least one legal block can reside; correctness never depends on simultaneous block residency or target occupancy; resource reports match the shipped binary; and every performance claim retains correctness evidence, target/build provenance, repetitions, uncertainty, and end-to-end context.

### Common failures

Teams equate contiguous source indices with coalesced transactions, ignore misalignment or element width, optimize reads while scattering writes, count logical bytes instead of transferred sectors, call every branch divergent, replace safe branches with unsafe speculative loads, assume branchless code is cheaper, use a stale warp/wave size, confuse static and achieved occupancy, maximize occupancy by forcing spills, overlook shared-memory or block-count cliffs, infer latency hiding from resident-warps alone, compare kernels with different outputs, profile only one launch, ignore tails and cache state, or treat a profiler's derived percentage as a correctness or causal proof.

### Compact example

In a declared eight-lane teaching model with 4-byte words and 16-byte aligned transactions, addresses `[0,4,...,28]` occupy two transactions: 32 useful bytes/32 transferred bytes. Addresses `[0,16,...,112]` occupy eight transactions: the same 32 useful bytes/128 transferred bytes. This 1.0 versus 0.25 ratio is a model result, not a claim about an unspecified GPU or cache level.

### Connections

[GPU Memory Hierarchies](076-gpu-memory-hierarchies.md) defines address spaces, caches, and scratchpads. [GPU Execution Grids, Blocks, and Warps](075-gpu-execution-grids-blocks-and-warps.md) defines execution groups and barriers. [Data Layout for Vectorization](072-data-layout-for-vectorization.md) supplies strides and useful-byte reasoning. The [program roadmap](../ROADMAP.md) next treats kernel fusion and heterogeneous pipelines.

## Governing Question

For a specific kernel, input family, binary, device, and operating state, which loss is limiting useful throughput: excessive memory transactions, inactive lanes, insufficient ready work, dependency latency, resource cliffs, tail imbalance, or something else?

The question demands a causal experiment. Coalescing, divergence, and occupancy are explanatory dimensions, not grades. A kernel can have perfect coalescing while doing unnecessary work, zero branch divergence while suffering load imbalance, and maximum theoretical occupancy while spilling so heavily that it slows down.

## Why This Matters

GPU hardware amortizes control and memory machinery across execution groups. Adjacent lane accesses may be combined, and one ready warp or wave may execute while another waits. Software that exposes regular addresses and independent work can use this machinery efficiently. Software that scatters a few useful bytes across many transfers, serializes paths under sparse masks, or consumes all registers/shared memory for one block can strand throughput.

These are also correctness surfaces. Reordering records for coalescing can detach values from identities. Predicating both paths can evaluate an invalid pointer, divide by zero, alter floating exceptions, or duplicate a side effect. Reducing resources to raise occupancy can change numeric order or introduce spills holding sensitive data. Changing block size can invalidate collective membership, shared-memory indexing, or assumptions about full tiles.

A production investigation therefore begins with equivalence and invariants, identifies a measured limiting mechanism, changes one causal variable, and verifies both semantics and the intended counter movement.

## Prerequisites and Retrieval

Retrieve:

- execution groups, masks, launch geometry, barriers, and asynchronous timing from [GPU Execution Grids, Blocks, and Warps](075-gpu-execution-grids-blocks-and-warps.md);
- address spaces, cache/scratchpad distinctions, spills, tiling, and byte ledgers from [GPU Memory Hierarchies](076-gpu-memory-hierarchies.md);
- layout, alignment, stride, tails, and gather/scatter reasoning from [Data Layout for Vectorization](072-data-layout-for-vectorization.md); and
- branch masks and vector cost models from [SIMD Execution and Vector Lanes](071-simd-execution-and-vector-lanes.md).

Retrieval prompt: select one shipped kernel and record lane-to-address equations, active masks, block dimensions, compiler registers/local/shared bytes, target limits and allocation granularities, number of blocks, dependency graph, profiler counters, output oracle, and timing protocol. Which observations establish legality, which suggest a bottleneck, and which remain hypotheses?

## Learning Objectives

After completing this module, a learner can:

1. derive transaction sets and useful-byte efficiency for aligned, misaligned, strided, masked, gathered, and scattered accesses;
2. distinguish source contiguity, hardware coalescing, caching, and application-level reuse;
3. derive active masks and useful lane-instruction ratios for divergent paths;
4. decide when branching, predication, partitioning, or persistent work distribution preserves semantics and may reduce waste;
5. compute a simplified occupancy bound from independent resource ceilings and allocation granularity;
6. distinguish theoretical, achieved, and sufficient occupancy from latency hiding and utilization;
7. explain interactions among registers, spills, shared memory, block shape, ILP, MLP, and resident work;
8. diagnose tail effects and intra-group divergence separately from inter-group load imbalance;
9. design controlled target-specific tuning experiments with correctness and uncertainty evidence; and
10. review portability, privacy, operational, and high-stakes risks of GPU utilization changes.

## Core Exposition

### Coalescing is a transaction mapping

For one issued memory instruction, collect the byte ranges requested by active lanes. Map those ranges to the target's transaction units at the declared hierarchy boundary. The number and size of transactions determine transferred bytes; requested bytes that the algorithm actually uses determine useful bytes. Alignment, access width, masks, cache policy, stores, and architecture all matter.

An array index `base + lane` often helps because adjacent lanes request adjacent elements, but it does not prove optimal transactions. The base may be misaligned, elements may straddle segments, only sparse lanes may be active, a vector load may widen each request, or a two-dimensional row pitch may shift alignment. Conversely, a non-contiguous logical layout can still have acceptable transactions through caching or a target's request combining.

Modern CUDA guidance describes coalescing in terms of the device transactions needed for a warp's requested words; exact rules vary by compute capability and caching behavior. HIP guidance similarly recommends adjacent-lane adjacent-address mappings. OpenCL and SYCL specify program semantics, not one universal transaction size. Treat vendor examples as target evidence, never language law.

### Useful bytes, stores, and reuse

Let `U` be useful bytes and `X_q` bytes transferred across boundary q. Efficiency `eta_q=U/X_q` lies in `(0,1]` only under a clearly defined accounting that excludes or separately counts reuse and protocol effects. A sector fetched once and reused by later instructions complicates per-instruction ratios. Report both request/transaction counters and cache-level byte estimates rather than hiding the boundary.

Stores deserve equal attention. Sparse writes may allocate or read a line before modification, combine imperfectly, or create ownership conflicts. Structure-of-arrays can let lanes load one field contiguously; array-of-structures may interleave unused fields. Transposition or staging can convert a strided phase into coalesced transfers, but adds tile traffic, barriers, capacity, and conversion cost.

Gather/scatter is sometimes intrinsic to graphs, sparse matrices, indexes, or particles. Sorting or bucketing by destination may improve locality and branch coherence but changes order, needs temporary storage, and may conflict with stable/deterministic semantics. Compression reduces bytes but adds decoding and may introduce divergence. The right objective is total verified pipeline cost.

### Divergence is mask evolution

An execution group begins an instruction with some active mask. If a condition differs by lane, hardware may execute multiple paths with corresponding masks, use predicated instructions, or apply target-specific control mechanisms. Reconvergence details are architecture/compiler facts. Portable correctness relies on the programming model's control and collective rules, not assumed lockstep.

For paths p, a simple useful-lane ratio is `sum useful_active_lanes_p / sum issued_lane_slots_p`. It exposes sparse masks but omits instruction costs, memory stalls, overlap, predication, and path lengths. Two equal four-lane paths in an eight-lane group yield eight useful lane-instructions across sixteen issued slots if each path has one equal-cost instruction. Unequal path lengths require weighting by issued instructions or cycles.

Do not label a branch divergent merely because it is data-dependent. If all lanes in each group choose the same outcome, it is uniform for that group. A branch on block ID may divide blocks without intra-warp divergence. Conversely, a loop with lane-dependent trip counts diverges even without an obvious `if`: completed lanes become inactive while the longest lane continues.

### Branches, predication, and work reorganization

Short, side-effect-free alternatives may be predicated by the compiler. This can avoid branch machinery but still issues work for inactive results. Manually computing both sides is legal only if both evaluations are safe and their extra effects are absent. Speculative loads must remain in bounds; exceptional arithmetic, atomics, random-state changes, logging, and volatile/device I/O cannot be casually duplicated.

Partitioning records by predicate can produce coherent groups, but incurs classification, prefix sum, scatter, storage, synchronization, and possibly unstable ordering. Separate kernels make phase boundaries explicit and may improve instruction/cache specialization; they add launch and data-movement cost. Persistent queues can balance variable work dynamically; their atomics, fairness, termination, watchdog, and occupancy assumptions require review.

Before rewriting, determine whether the measured issue is branch serialization, instruction imbalance, memory latency, or inter-block skew. A profiler's branch statistic without source correlation and timing is only a clue.

### Occupancy is a resource feasibility calculation

For one compute unit, derive resident-block limits from maximum threads, warps/waves, blocks, registers, shared/local memory, barriers, and any architecture-specific scheduling or cluster constraints. Apply allocation granularities and kernel attributes. The legal resident-block count is the minimum of those ceilings, and resident warps follow from block size and execution-group rounding.

If `B` threads form `ceil(B/W)` warps of width W, resource ceilings in a simplified model include `floor(T_max/B)`, `floor(W_max/ceil(B/W))`, `B_max`, `floor(R_total/R_block_allocated)`, and `floor(S_total/S_block_allocated)`. Zero use requires a separately defined unlimited ceiling rather than division by zero. Real calculators incorporate target-specific granularity and reserved resources; use the runtime/compiler calculator for the shipped binary.

Theoretical occupancy is resident warps divided by the target maximum. Achieved occupancy is sampled/averaged active residency during a run and can be lower due to grid size, tails, scheduling, or workload phases. Neither says how many warps are ready to issue, how many memory requests are outstanding, or which pipeline is saturated.

### More occupancy can be worse

Occupancy helps hide latency only until sufficient independent ready work exists. A compute-bound kernel may saturate its pipelines at modest occupancy. A memory kernel may need both resident warps and enough independent requests. Dependency chains can leave many resident warps unready.

Reducing registers to admit another block may create local-memory spills. Shrinking shared tiles may reduce reuse and coalescing. Increasing block size may waste tail lanes, reduce block-level distribution, or cross an allocation cliff. Decreasing per-thread work may reduce ILP and amortization. Thus optimize execution time or service objective subject to correctness, not the occupancy percentage.

Launch-bounds annotations and register caps are contracts with compilers and target limits, not harmless hints. Rebuilds can change register counts. Record the compiler version/options and fail qualification when resources exceed an established safe envelope; retune per supported target rather than freezing one magic block size.

### ILP, MLP, readiness, and tails

Latency hiding draws from multiple sources: another warp/wave can issue, the same lane can execute an independent instruction, or multiple memory operations can be in flight. Too little ILP produces dependency stalls; too much live state raises registers. Too few requests underuse memory; too many can pressure queues/caches. Occupancy alone cannot resolve this balance.

The grid must also contain enough blocks to distribute across compute units. If it has only one block per unit, block-level imbalance or a long final block creates a tail. The final scheduling wave may leave units idle even when per-block theoretical occupancy is high. Variable-length records can create both intra-wave divergence and inter-block skew; measure duration distributions and consider size classes, work queues, or finer tasks.

Concurrent kernels can use complementary resources, but introduce stream dependencies, cache interference, priorities, admission, and latency isolation. Per-kernel occupancy calculators do not prove safe co-residency or service-level behavior.

### A causal tuning workflow

First freeze semantics: exact output ownership, bounds, numeric tolerance/order, synchronization, errors, and representative inputs. Capture binary/compiler/driver/device/power state. Measure end-to-end and kernel time with warm-up and repeated samples; retain distributions, not one number.

Second classify the limiter using multiple observations: requested/actual bytes, sectors/transactions, cache hit rates, active lanes, branch/source counters, issued versus active warps, eligible/ready warps, stall reasons, instruction mix, memory throughput, pipeline utilization, registers, spills, shared bytes, block residency, waves, and tail duration. Counter names and meanings are profiler/architecture-specific; read the current profiling guide.

Third form one falsifiable hypothesis. To test coalescing, change layout/alignment while holding work and results constant, then expect fewer relevant transactions and lower time if that boundary was limiting. To test divergence, group predicates or isolate paths and expect denser masks or fewer issued instructions without unsafe speculation. To test residency, sweep block size, dynamic shared memory, or reviewed launch bounds and observe resource cliffs, ready warps, spills, throughput, and time.

Finally repeat across sizes, distributions, cold/warm states, devices, concurrency, pressure, and failure modes. Reject a change if outputs, race/sanitizer evidence, resource legality, or operational tails regress—even if a narrow mean time improves.

### Executable ledger model

The following deterministic Python model uses fictional limits: eight-lane execution groups, 16-byte transactions, and one tiny compute unit. It illustrates the three ledgers. It does not emulate a GPU, cache, compiler, scheduler, allocation granularity, timing, or profiler.

<!-- bijux-verify: {"id":"gpu-utilization-ledgers","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"contiguous_segments=[0, 1]\ncontiguous_transferred=32\ncontiguous_efficiency=1.000\nstrided_segments=[0, 1, 2, 3, 4, 5, 6, 7]\nstrided_transferred=128\nstrided_efficiency=0.250\ndivergent_path_lane_counts=[4, 4]\ndivergent_lane_efficiency=0.500\nresident_block_limits={'threads': 4, 'warps': 4, 'blocks': 4, 'registers': 3, 'shared': 2}\nresident_blocks=2\nactive_warps=4\ntheoretical_occupancy=0.500\n","stderr":""}} -->
```python
lanes = list(range(8))
word_bytes = 4
segment_bytes = 16

def transaction_stats(addresses):
    segments = sorted({address // segment_bytes for address in addresses})
    useful = len(addresses) * word_bytes
    transferred = len(segments) * segment_bytes
    return segments, transferred, useful / transferred

contiguous = [lane * word_bytes for lane in lanes]
strided = [lane * segment_bytes for lane in lanes]

for name, addresses in (("contiguous", contiguous), ("strided", strided)):
    segments, transferred, efficiency = transaction_stats(addresses)
    print(f"{name}_segments={segments}")
    print(f"{name}_transferred={transferred}")
    print(f"{name}_efficiency={efficiency:.3f}")

path_masks = [
    [True, True, False, False, True, True, False, False],
    [False, False, True, True, False, False, True, True],
]
path_lane_counts = [sum(mask) for mask in path_masks]
useful_lane_instructions = sum(path_lane_counts)
issued_lane_slots = len(lanes) * len(path_masks)
print(f"divergent_path_lane_counts={path_lane_counts}")
print(f"divergent_lane_efficiency={useful_lane_instructions / issued_lane_slots:.3f}")

block_threads = 16
warp_size = 8
warps_per_block = (block_threads + warp_size - 1) // warp_size
registers_per_thread = 10
shared_per_block = 48

limits = {
    "threads": 64 // block_threads,
    "warps": 8 // warps_per_block,
    "blocks": 4,
    "registers": 512 // (block_threads * registers_per_thread),
    "shared": 128 // shared_per_block,
}
resident_blocks = min(limits.values())
active_warps = resident_blocks * warps_per_block
print(f"resident_block_limits={limits}")
print(f"resident_blocks={resident_blocks}")
print(f"active_warps={active_warps}")
print(f"theoretical_occupancy={active_warps / 8:.3f}")
```

The model's shared-memory ceiling binds at two blocks and yields 0.5 theoretical occupancy. It does not imply that removing shared memory would improve real time: the storage might be responsible for reuse that matters more than additional resident warps.

### Correctness, portability, and operations

Run value, race, bounds, uninitialized-memory, and collective tests before performance comparison. Include zero/one, alignment-minus-one/alignment/alignment-plus-one, group and grid tails, sparse masks, all-true/all-false conditions, extreme loop lengths, pitch/subviews, aliasing, allocation cliffs, and maximum sizes. Compare CPU/reference results and exact ownership, including NaN, infinities, signed zero, overflow, and reproducibility policy where applicable.

Qualify every supported device/compiler combination. Warp/wave/subgroup size, transaction rules, register allocation, shared-memory capacity, scheduling, counter definitions, and optimal launch shape vary. Query capabilities; record resource reports from the final binary; retain portable fallbacks. Do not use warp-synchronous communication outside documented collectives and masks.

Operations review includes multi-tenant contention, clock/power/thermal state, dynamic frequency, profiling overhead, device partitioning, concurrent kernels, queues, watchdogs, timeouts, device loss, rollout/canary, regression thresholds, and rollback. Counters and profiler traces can expose addresses, kernels, model shapes, or workload distributions; minimize, access-control, redact, and expire them.

High-stakes kernels require domain evidence beyond these metrics. Validate units, formats, calibration, boundary rules, numeric tolerances, subgroup/device determinism, fallback equivalence, error propagation, monitoring, human override, and independent review. A faster utilization profile establishes neither scientific validity nor safety.

## Definitions and Notation

- `W`: execution-group width for the declared target/model.
- `M_p`: active-lane mask for path or instruction p.
- `a_l`: byte address requested by lane l.
- `S_q(a_l)`: transaction unit at boundary q containing address a_l.
- `U_q`: useful algorithm bytes attributed to boundary q.
- `X_q`: bytes transferred at boundary q.
- `eta_q=U_q/X_q`: useful-byte efficiency under the declared accounting.
- `B`: threads/work-items per block/work-group.
- `R_t`: compiler-reported registers per thread.
- `R_b`: allocated registers per block after target granularity.
- `S_b`: static plus dynamic shared/local bytes allocated per block.
- `N_b`: legal resident blocks per compute unit, the minimum resource ceiling.
- `N_w`: resident warps/waves; `O=N_w/N_w,max` is theoretical occupancy.
- `L`: latency of a dependency; `Q`: ready independent work available to cover it.
- `T`: measured elapsed time under a declared protocol.

Every symbol is conditional on a target, binary, launch, and workload. A ratio without that context is not portable evidence.

## Mechanisms, Invariants, or Proof Structure

### Transaction coverage proof

For an issued memory instruction, enumerate every active lane's valid requested byte interval. Map each interval to all target transaction units it intersects. Their union covers every requested byte; deduplicate units to avoid double counting. Compute useful bytes from algorithm-consumed fields, not merely load width. Stores additionally require unique ownership or a valid atomic protocol.

### Control equivalence proof

For every input and lane, transformed control executes the same required effects and no forbidden effects under the language's numeric, exception, synchronization, and I/O rules. Predication may evaluate both expressions only when both are valid and side-effect-free. Reordered/partitioned work preserves identity and any declared stability/determinism.

### Residency feasibility proof

Use compiler-reported allocated resources and current target limits/granularities. Each candidate resident-block count satisfies all thread, warp/wave, block, register, shared-memory, barrier, cluster, and kernel limits. Select their minimum. Establish at least one legal block; never infer cross-block progress or correctness from the resulting count.

### Causal performance argument

State baseline, invariant workload/results, target/build, hypothesis, changed variable, expected counter movement, measured counter movement, time distribution, and confounders. Accept causal support only when correctness holds and observations align. A correlation between occupancy and time alone is insufficient.

### Operational safety argument

The selected configuration remains legal across supported binaries/devices, bounded under adversarial sizes and skew, isolated under concurrency, observable without sensitive leakage, recoverable after failure, and equivalent under fallback. High-stakes acceptance remains assigned to named humans.

## Alternatives and Trade-Offs

| Technique | Potential gain | Principal cost or risk |
|---|---|---|
| Contiguous lane mapping | fewer memory transactions | layout/conversion constraints |
| Structure-of-arrays | coalesced field access | fragmented object semantics |
| Shared transpose/tile | coalescing plus reuse | loads, barriers, banks, capacity |
| Predicate grouping | coherent execution groups | classify/scan/scatter and order |
| Predication | avoids short branch control | executes masked work; unsafe speculation |
| Separate kernels | specialized uniform phases | launches, storage, phase movement |
| Dynamic work queue | balances variable tasks | atomics, fairness, termination |
| More resident blocks | more latency-hiding candidates | registers/shared/reuse/ILP trade-offs |
| More work per thread | ILP and amortization | registers, imbalance, lower occupancy |
| Register cap/launch bounds | controls residency target | spills, target coupling, rebuild drift |
| Smaller blocks | distribution and fewer tail lanes | fewer collaboration opportunities |
| Concurrent kernels | complementary utilization | interference, dependency and SLO risk |

Select only after measuring the relevant boundary. Keep a correct, comprehensible baseline for differential tests and fallback.

## Failure Modes and Misconceptions

- **“Adjacent indices prove coalescing.”** base alignment, width, masks, pitch, and target transactions still matter.
- **“One transaction rule applies to every GPU.”** architecture and cache path differ.
- **“High load efficiency proves low traffic.”** reuse, stores, other levels, and protocol traffic remain.
- **“Caches repair every stride.”** working set, conflicts, TLBs, and reuse distance intervene.
- **“Every branch diverges.”** group-uniform branches do not split masks.
- **“Branchless is always faster.”** it can issue more work and unsafe effects.
- **“Predication is semantically free.”** speculative evaluation can fault or mutate.
- **“Divergence is the same as load imbalance.”** one is intra-group masks; the other can be inter-group duration.
- **“All active lanes are useful.”** they may compute discarded or redundant results.
- **“Occupancy is utilization.”** resident work can be stalled or target the wrong pipeline.
- **“Maximum occupancy is optimal.”** spills or lost reuse/ILP can dominate.
- **“Low occupancy always means slow.”** sufficient readiness may exist for the limiter.
- **“Block size alone determines occupancy.”** registers, shared memory, granularities, and kernel limits bind.
- **“A calculator predicts runtime.”** it establishes resource feasibility/candidates.
- **“The compiler resource count is stable.”** code, flags, compiler, target, and link decisions change it.
- **“Kernel time proves service improvement.”** transfers, queues, interference, and tails remain.
- **“A counter is ground truth.”** definitions, sampling, replay, and profiler perturbation require review.
- **“A faster result is equivalent.”** races, numeric order, identity, or boundaries may have changed.

## Worked Examples

### Example 1

**Aligned versus offset.** Eight 4-byte lane loads fit two 16-byte teaching segments at base zero; shifting the base by four can touch three. **Conclusion:** identical stride does not imply identical transfers.

### Example 2

**Strided field.** Each lane reads one 4-byte field from a 64-byte record, spreading useful words across transactions. A structure-of-arrays view packs the field. **Conclusion:** layout is part of the access algorithm.

### Example 3

**Sparse store.** A filter writes output at atomically assigned positions. Reads are coalesced but destinations are scattered and order is unstable. **Conclusion:** review both directions and semantic ordering.

### Example 4

**Uniform branch.** A condition on block ID sends entire blocks to different code. Groups remain internally coherent though blocks have unequal durations. **Conclusion:** measure inter-block skew separately from divergence.

### Example 5

**Unsafe branchless rewrite.** Replacing `valid ? data[i] : 0` by unconditional `data[i]` plus a mask reads out of bounds for tail lanes. **Conclusion:** masked results do not retroactively legalize effects.

### Example 6

**Loop divergence.** Lanes traverse linked lists of lengths one through sixty-four; early finishers idle. Bucketing similar lengths helps masks but costs preprocessing. **Conclusion:** optimize total pipeline, not one kernel statistic.

### Example 7

**Register cliff.** A new unroll raises allocated registers enough to reduce resident blocks from three to two and adds spills. **Conclusion:** inspect discrete resource allocation and time together.

### Example 8

**Useful low occupancy.** A compute-heavy kernel has independent arithmetic and saturates its target pipeline at half occupancy. Forcing smaller register use slows it. **Conclusion:** sufficient occupancy is bottleneck-specific.

### Example 9

**Grid tail.** A fast first scheduling wave fills every compute unit, while a few long blocks form a sparse final wave. Median block time looks healthy but kernel tail is poor. **Conclusion:** distributions and wave count matter.

### Example 10

**Digital pathology inference.** Reordering image tiles or grouping model branches must preserve patient/slide/tile identity, color calibration, dimensions, overlap/halo, preprocessing, numeric and deterministic policy, model/version provenance, confidence and abstention, failure/fallback, privacy, and audit trails. Named pathology, laboratory/clinical, imaging/calibration, ML/statistics, GPU/compiler, software-safety, security/privacy, operations, quality/regulatory, human-factors, and independent validation reviewers must approve requirements and evidence; none is claimed here. **Conclusion:** coalescing, dense masks, occupancy, and faster inference do not establish diagnostic validity or safety.

## Cross-Program Connections

- **Computer architecture:** transaction formation, caches, schedulers, scoreboards, registers, and pipelines price lane work.
- **Programming languages:** control equivalence, exceptions, aliasing, atomics, and collective semantics constrain transformations.
- **Algorithms:** partitioning, scans, tiling, compression, work queues, and size classes reshape regularity.
- **Data structures:** record layout and graph/sparse representations determine addresses and skew.
- **Compilers:** if-conversion, unrolling, vectorization, register allocation, and spills alter all three ledgers.
- **Numerical computing:** reassociation, predication, and reordering affect exceptions, precision, and reproducibility.
- **Performance engineering:** controlled experiments and multi-counter causal arguments replace metric chasing.
- **Testing:** differential oracles, tail/alignment/resource boundaries, race tools, and target matrices protect semantics.
- **Security:** speculative accesses, stale spills, traces, and workload shapes can leak sensitive information.
- **Operations:** concurrency, thermal state, partitioning, tails, rollback, and device loss determine service behavior.

## References

1. Sunpyo Hong and Hyesoon Kim, “An Analytical Model for a GPU Architecture with Memory-Level and Thread-Level Parallelism Awareness,” ISCA 2009. <https://doi.org/10.1145/1555754.1555775>
2. Vasily Volkov and James W. Demmel, “Benchmarking GPUs to Tune Dense Linear Algebra,” SC 2008. <https://doi.org/10.1109/SC.2008.5214359>
3. NVIDIA, *CUDA C++ Best Practices Guide: Coalesced Access to Global Memory*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#coalesced-access-to-global-memory>
4. NVIDIA, *CUDA C++ Best Practices Guide: Occupancy*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#occupancy>
5. NVIDIA, *CUDA Programming Guide: Writing CUDA SIMT Kernels*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html>
6. NVIDIA, *Nsight Compute Profiling Guide*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html>
7. AMD, *HIP Performance Guidelines*, current documentation; retrieved 2026-08-29. <https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/performance_guidelines.html>
8. AMD, *HIP Runtime API Reference: Occupancy*, current documentation; retrieved 2026-08-29. <https://rocm.docs.amd.com/projects/HIP/en/latest/doxygen/html/group___occupancy.html>
9. Khronos SYCL Working Group, *SYCL 2020 Specification*, revision 12, Section 4.9.1.8, 2026. <https://registry.khronos.org/SYCL/specs/sycl-2020/html/sycl-2020.html>
10. Khronos OpenCL Working Group, *OpenCL 3.0 Unified Specification*, current documentation; retrieved 2026-08-29. <https://registry.khronos.org/OpenCL/specs/3.0-unified/html/OpenCL_API.html>

## Exercises

### Exercise 1

For eight 4-byte active lanes and 16-byte aligned teaching transactions, derive transaction sets and useful-byte efficiency for bases 0 and 4 with unit stride, then for base 0 with 16-byte stride. State why the result is not portable hardware evidence.

### Exercise 2

Analyze an eight-lane group whose true path has two instructions for lanes 0–3 and false path has six instructions for lanes 4–7. Compute a simple issued-slot efficiency, then list the facts it omits and assess predication versus partitioning.

### Exercise 3

Using a fictional compute unit with 2048 threads, 64 warps, 16 blocks, 65,536 registers, and 64 KiB shared memory, calculate simplified occupancy for 256-thread blocks using 40 registers/thread and 20 KiB shared/block. State required granularity caveats.

### Exercise 4

Design a causal experiment to determine whether an irregular gather kernel is limited by coalescing, divergence, occupancy/readiness, or block-tail imbalance. Include equivalence and uncertainty evidence.

### Exercise 5

A multi-tenant genomic variant caller groups reads and changes block size/register limits to improve GPU utilization. Specify identity, numeric, memory, synchronization, privacy, fairness, capacity/failure, performance, and human-review evidence required before release.

## Answers to the Exercises

### Answer 1

At base 0, byte ranges start 0,4,...,28 and touch segments 0 `[0,16)` and 1 `[16,32)`: 32 useful/32 transferred = 1.0. At base 4, ranges start 4 through 32 and touch segments 0,1,2: 32/48 = 2/3. With 16-byte stride, starts 0,16,...,112 touch eight segments: 32/128 = 0.25. This assumes each 4-byte request lies within one declared 16-byte unit, no cache reuse or protocol/store traffic, all lanes active, and an aligned base. Real GPUs have target-, generation-, instruction-, cache-, and architecture-specific request/sector behavior; obtain current documentation and counters.

### Answer 2

True issues 2 instructions across eight lane slots and uses 4·2=8; false issues 6 across eight and uses 4·6=24. Simple efficiency is `(8+24)/(8·(2+6))=32/64=0.5`. It omits instruction latency/throughput, memory stalls, overlap, reconvergence, compiler predication, dependencies, cache effects, and different operation value. Predicating both paths issues at least the same equalized work and is legal only if every evaluation/effect is safe. Partitioning can make full groups but pays classify/scan/scatter/storage/order costs. Measure end-to-end on representative predicate distributions after equivalence tests.

### Answer 3

With warp width 32, each block has 8 warps. Thread ceiling is `floor(2048/256)=8`; warp ceiling `floor(64/8)=8`; block ceiling 16; raw register ceiling `floor(65536/(256·40))=6`; shared ceiling `floor(65536/20480)=3`. Shared memory binds at three blocks, 24 warps, theoretical occupancy `24/64=0.375`. A real result must apply register/shared allocation granularity, reserved resources, architecture/kernel limits, static plus dynamic shared memory, compiler allocation, cluster/barrier constraints, and runtime calculator rules. It predicts feasibility, not performance.

### Answer 4

Freeze input identities, exact/tolerant output oracle, order/numeric policy, launch legality, and timing protocol. Record binary/compiler/driver/device/power and repeat warm/cold sizes/distributions. Baseline requested versus actual bytes/transactions by level, cache behavior, active masks/source branches, issued/eligible/active warps, stall reasons, registers/spills/shared bytes/resident blocks, per-block duration, scheduling waves, and end-to-end/kernel distributions. Test one change at a time: layout/bucketing for transactions, predicate grouping for masks, block/resource sweep for readiness, finer tasks/queue for tails. Require predicted counter direction plus statistically/operationally meaningful time change and unchanged value/race/bounds evidence. Include profiler perturbation, cache, clocks, compilation, transfers, and concurrency as confounders.

### Answer 5

Preserve sample/read/patient identity through grouping, stable-coordinate and duplicate policy, reference/build/model versions, exact integer and declared floating/reduction semantics, bounds, unique output ownership, collective masks/barriers, and event-bound lifetimes. Qualify target wave/subgroup behavior, resource reports, alignment/tails, register spills, shared capacity, and all supported block configurations. Isolate tenants and allocations/queues, encrypt/minimize data, prohibit sensitive trace/address leakage, audit access, bound profiling, and define retention/erasure. Establish per-tenant admission, fairness, quotas, oversubscription fallback, timeouts, device-loss/idempotent retry, deterministic reconciliation, monitoring, canary, rollback, and CPU/reference path. Benchmark realistic read lengths, allele distributions, skew, concurrency, pressure, and failures with full distributions/counters and correctness. Named genomics, bioinformatics/statistics, clinical/laboratory where applicable, numerical, GPU/compiler, security/privacy, multi-tenant platform, operations/SRE, quality/regulatory, human-factors, and independent validation reviewers approve requirements, biological/clinical limits, bias, and residual risk. No utilization metric establishes variant validity or clinical safety.
