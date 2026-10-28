---
module_id: CONPAR-092
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 92
title: Roofline and Operational-Intensity Analysis
status: complete
last_verified: 2026-08-29
---

# Roofline and Operational-Intensity Analysis

## One-Page Review

### Governing question

At a named kernel, precision, device, and memory-hierarchy boundary, is achieved useful performance primarily constrained by attainable compute throughput, data traffic, another ceiling, or a measurement/model mismatch—and which transformation can move the point while preserving the result?

### Essential definitions

- **performance** P is useful operations per elapsed second under a declared operation convention.
- **operational intensity** `I=W/Q` is useful work W divided by bytes Q transferred across a named boundary.
- **arithmetic intensity** is often used synonymously for floating operations per byte; this chapter uses operational intensity when work may be defined more broadly.
- **compute ceiling** `P_peak` is a theoretical or empirically attainable throughput for a stated operation mix, precision, vector/tensor mode, frequency, and resource allocation.
- **bandwidth ceiling** B is bytes per second across a stated memory/cache/interconnect boundary under representative access/concurrency conditions.
- The basic **roofline bound** is `P <= min(P_peak, B*I)`.
- The **ridge point** is `I*=P_peak/B`, where compute and bandwidth ceilings intersect.
- A **hierarchical roofline** includes separate L1/L2/last-level/device-memory or other boundaries and corresponding traffic/ceilings.
- **headroom** is the gap between achieved performance and the applicable measured ceiling; it is opportunity only if model assumptions and bottleneck attribution hold.
- **compulsory traffic** is data that must cross a boundary at least once; capacity/conflict/coherence, write allocate, eviction, and redundant loads add traffic.
- **code balance** is bytes per unit work, the reciprocal of intensity when nonzero.
- **attainable ceiling** is measured with a relevant microbenchmark/configuration; a marketing peak is not automatically attainable by a kernel.

### Central model, mechanism, or theorem

If a kernel performs W counted useful operations, transfers Q bytes across boundary H, and takes t seconds, then `P=W/t`, `I=W/Q`, and the bandwidth-implied bound is `B*I`. Together with a compute ceiling, `P_roof=min(P_peak,B*I)`. When `I<I*=P_peak/B`, the basic roof slopes with intensity; above it, the compute ceiling is lower. This is an upper-bound model, not proof of the active bottleneck: instruction dependencies, latency, occupancy, vectorization, cache behavior, load imbalance, synchronization, and measurement error can keep a point below both roofs.

### Critical invariants

Work and byte counters cover the same kernel invocation and elapsed interval; operations are counted by an explicit precision/type/FMA/tensor/special-function convention; bytes name a specific hierarchy boundary and distinguish requested from actual traffic; hardware, clocks, power mode, allocation, placement, problem, code/toolchain, and configuration are recorded; ceilings match precision/operation mix and are measured under representative locality/concurrency; profiling replay and overhead are understood; output and numerical policy remain valid; multiple repetitions retain variation; hierarchical points never mix bytes from one level with bandwidth from another; and claims remain bounded to the measured workload/device.

### Common failures

Teams divide algorithmic FLOPs by DRAM bytes from a different scope, count FMA inconsistently, compare FP64 work with an FP32/tensor peak, use datasheet bandwidth as achieved bandwidth, label every left-of-ridge point memory-bound, ignore cache levels and write traffic, measure a whole application against a kernel roof, let profiling replay change behavior, optimize FLOPs downward and call lower FLOP/s a regression, raise intensity through recomputation without checking energy/time, confuse occupancy with utilization, overlook latency/dependencies/imbalance, trust a counter unsupported on the device, or change precision/result to reach a higher roof.

### Compact example

A kernel performs 24 GFLOP, transfers 6 GB from device memory, and takes .02 s: `I=4 FLOP/byte` and `P=1.2 TFLOP/s`. With attainable FP64 compute 4 TFLOP/s and device-memory bandwidth 500 GB/s, `I*=8 FLOP/byte` and the roof is `min(4,2)=2 TFLOP/s`; achieved is 60% of that roof. The model suggests examining traffic/locality and the remaining gap, but it does not prove memory saturation.

### Connections

[Amdahl, Gustafson, and Work-Span Models](091-amdahl-gustafson-and-work-span-models.md) supplies global/dependency ceilings. [Data Layout for Vectorization](072-data-layout-for-vectorization.md) changes traffic and reuse. [Explicit Vector Intrinsics](074-explicit-vector-intrinsics.md) changes compute ceilings. The [program roadmap](../ROADMAP.md) next makes allocation and placement NUMA-aware.

## Governing Question

What are the matching numerator, denominator, boundary, precision, scope, and attainable machine ceilings, and which controlled change improves time-to-valid-solution rather than merely moving a plotted point?

The roofline is a disciplined upper bound and communication device. It is strongest when its measurements are internally consistent and paired with deeper counters and experiments.

## Why This Matters

Processors can issue far more arithmetic than memory can feed for low-reuse kernels. Roofline connects application work/data movement to machine compute/bandwidth limits, quickly showing whether reuse, representation, fusion, vectorization, or instruction throughput deserves investigation.

Modern hardware complicates the simple roof. Multiple cache levels, NUMA, HBM, host-device links, tensor units, mixed precision, sparse acceleration, throttling, and concurrent kernels create multiple ceilings. Applications contain kernels with different intensities and time shares. The chart guides, but does not replace, critical-path profiling.

Bad rooflines are persuasive. A mismatched FLOP count, boundary, peak, or interval can manufacture a conclusion. Production-grade analysis records definitions, validates counters and ceilings, preserves correctness, and confirms optimization with complete elapsed time and resources.

## Prerequisites and Retrieval

Retrieve:

- validated scale/placement/timing distributions from [Scaling a Parallel Program Across Multiple Nodes](090-scaling-a-parallel-program-across-multiple-nodes.md);
- cache lines, reuse, layout, false sharing, vectorization, GPU hierarchy, and transfer from [Data Layout for Vectorization](072-data-layout-for-vectorization.md), [False Sharing and Cache-Line Contention](029-false-sharing-and-cache-line-contention.md), [SIMD Execution and Vector Lanes](071-simd-execution-and-vector-lanes.md), and [GPU Memory Hierarchies](076-gpu-memory-hierarchies.md); and
- numerical equivalence and reduction policy from [Parallel Loops and Reductions](044-parallel-loops-and-reductions.md).

Retrieval prompt: name kernel/range/scope; input/result oracle; useful work and counting convention; memory boundary and byte-event definition; elapsed interval; precision/instruction mix; hardware/device/NUMA/clock/power/allocation; theoretical and empirical compute/bandwidth ceilings; profiler/tool/metric/version/replay; repetitions; cache/occupancy/dependency/latency/imbalance evidence; candidate transformation; and correctness/performance acceptance.

## Learning Objectives

After completing this module, a learner can:

1. derive the roofline bound, ridge point, intensity, and headroom with correct units;
2. define useful operations consistently across precision, FMA, tensor, integer, and mixed kernels;
3. measure bytes at a named memory-hierarchy boundary without mixing scopes;
4. construct empirical compute and bandwidth ceilings appropriate to a kernel;
5. interpret basic and hierarchical rooflines without treating regions as causal proof;
6. diagnose vectorization, dependencies, latency, occupancy, cache, NUMA, and imbalance below the roof;
7. choose transformations that reduce traffic, increase reuse, or improve compute execution;
8. validate profiler/replay/counter limitations and uncertainty;
9. compare complete valid elapsed time, energy/resources, and numerical outcomes after optimization; and
10. scope security, scientific, operations, and high-stakes review.

## Core Exposition

### Derive the basic roof

Let W be counted useful operations, Q bytes crossing boundary H, and t elapsed seconds for exactly that work/traffic scope. Achieved `P=W/t`; intensity `I=W/Q`. Since Q bytes require at least `Q/B` seconds at bandwidth B, `P<=W/(Q/B)=B*I`. Compute throughput also imposes `P<=P_peak`, yielding `P<=min(P_peak,B*I)`.

Units verify the model: `(byte/s)*(operation/byte)=operation/s`. The ridge `I*=P_peak/B` has operations/byte. Below the ridge, the bandwidth line is the lower basic ceiling; above it, compute is lower. Equality requires idealized utilization; most real points sit below.

The lower roof does not prove the resource is saturated. A low-intensity kernel may be latency-bound and achieve little bandwidth. A high-intensity kernel may suffer dependencies, branch divergence, poor instruction mix, low occupancy, or serialization. Add evidence.

### Define work honestly

Choose algorithmic or executed work and say which. Algorithmic counts aid cross-implementation efficiency; executed instruction/counter counts expose extra work. Retain both when optimization changes operations. FMA may be counted as two floating operations by convention; transcendental, integer, tensor/matrix, sparse, and mixed-precision operations need explicit categories rather than forced equivalence.

Match the ceiling. FP64 scalar/add-heavy code cannot be compared to an FP32 FMA or tensor-core marketing peak. Peak depends on active cores, vector width, instruction issue mix, frequency, throttling, and allocation. For mixed kernels, multiple roofs or instruction-specific ceilings are clearer.

Useful performance can fall after an algorithm reduces work even as elapsed time improves. Report time-to-valid-solution and work count alongside FLOP/s. Never add useless arithmetic to look faster.

### Define bytes and boundary

Q must name a boundary: registers-L1, L1-L2, last-level-memory, device HBM, host-device link, NUMA interconnect, or network. Cache hits mean algorithmic data volume differs from DRAM traffic. Hardware counters may count sectors, transactions, requests, fills, evictions, or bytes; translate only according to tool/device documentation.

Include reads and writes, write allocation/read-for-ownership, writebacks, coherence, metadata, compression, and replay as relevant. Requested bytes can differ from transferred bytes through coalescing, cache-line granularity, sparse/compressed representations, or partial transactions.

Hierarchical rooflines pair each Q_H with B_H. Reuse can raise DRAM intensity while L1 intensity remains low. Moving a point right at one boundary may increase traffic elsewhere. Record all chosen levels and never pair L2 bytes with HBM bandwidth.

### Executable roofline arithmetic

This deterministic decimal-scale model calculates one point. It does not read counters, estimate ceilings, model hierarchy/latency, or prove a bottleneck or optimization.

<!-- bijux-verify: {"id":"roofline-point","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"work_gflop=24.000000\ntraffic_gb=6.000000\ntime_s=0.020000\nintensity_flop_per_byte=4.000000\nachieved_tflop_s=1.200000\ncompute_ceiling_tflop_s=4.000000\nbandwidth_gb_s=500.000000\nridge_flop_per_byte=8.000000\nroof_tflop_s=2.000000\nroof_efficiency=0.600000\n","stderr":""}} -->
```python
work_gflop = 24
traffic_gb = 6
time_s = 0.02
compute_tflop_s = 4
bandwidth_gb_s = 500

intensity = work_gflop / traffic_gb
achieved = (work_gflop / 1000) / time_s
ridge = (compute_tflop_s * 1000) / bandwidth_gb_s
bandwidth_roof = (bandwidth_gb_s * intensity) / 1000
roof = min(compute_tflop_s, bandwidth_roof)

print(f"work_gflop={work_gflop:.6f}")
print(f"traffic_gb={traffic_gb:.6f}")
print(f"time_s={time_s:.6f}")
print(f"intensity_flop_per_byte={intensity:.6f}")
print(f"achieved_tflop_s={achieved:.6f}")
print(f"compute_ceiling_tflop_s={compute_tflop_s:.6f}")
print(f"bandwidth_gb_s={bandwidth_gb_s:.6f}")
print(f"ridge_flop_per_byte={ridge:.6f}")
print(f"roof_tflop_s={roof:.6f}")
print(f"roof_efficiency={achieved / roof:.6f}")
```

### Construct empirical ceilings

Theoretical peak is a useful sanity bound: active units times operations/cycle times frequency, respecting precision and instruction mix. But sustained frequency and issue balance vary. Record whether turbo/boost, power/thermal limits, ECC, partitioning, and concurrent use apply.

Measure attainable compute using a kernel with enough independent operations, representative instruction type/precision/vector/tensor path, occupancy/concurrency, and minimal relevant memory limitation. Prevent compiler elimination and validate output. Measure bandwidth with representative read/write mix, working-set size, strides, NUMA/device placement, concurrency, and duration. A streaming read roof is not a write-heavy gather roof.

Repeat and retain distributions. Microbenchmark ceilings must use the same resource allocation and stable environment. They are empirical for that setup, not permanent device constants. Separate L1/L2/memory roofs with appropriate benchmarks/counters.

### Gather a trustworthy point

Mark the exact kernel/range and capture W, Q_H, and t for the same invocations. Warm-up/cache state must be explicit. Record input shape, sparsity, alignment, strides, batch, precision, compiler flags, library/runtime, device, clocks/power, placement, and concurrent activity.

Profilers may replay kernels to collect incompatible counter sets. Replay can alter cache state, allocation, synchronization, dynamic input, or nondeterministic behavior. Read tool documentation, restrict metrics/ranges, make replay-safe inputs, and compare unprofiled/profiled time/results. Some counters require permissions or are approximate/unsupported.

Use repetitions and distributions. Counter multiplexing/sampling adds uncertainty. Cross-check derived bytes with known minimum/maximum and another metric/tool when high stakes. If a point exceeds its roof, first suspect mismatched scopes/units/count conventions/ceilings before announcing impossible hardware.

### Read the gap, not only the region

A point near the bandwidth roof with adequate achieved bandwidth supports traffic/reuse investigation. A point far below it may be limited by latency, insufficient memory-level parallelism, irregular accesses, page/NUMA placement, synchronization, or imbalance. Examine outstanding transactions, cache/TLB misses, coalescing, stalls, concurrency, and rank/thread distributions.

A point right of the ridge but far below compute peak may lack vectorization, use the wrong instruction mix, suffer dependencies/branches, low occupancy/register pressure, instruction-cache/front-end limits, or launch/synchronization overhead. Examine executed instructions, vector/tensor utilization, IPC/issue, dependency stalls, occupancy limits, divergence, and critical path.

Additional ceilings—no vectorization, limited FMA mix, instruction bandwidth, cache bandwidth, NUMA, PCIe/NVLink, network—can make the model more diagnostic when measured. Do not decorate a chart with unverifiable lines.

### Raise intensity or lower traffic

Loop interchange, tiling/blocking, fusion, temporal blocking, cache/shared-memory reuse, register reuse, structure-of-arrays, compression, sparse representation, and avoiding intermediates can reduce boundary traffic. Fusion may increase register pressure, reduce occupancy, change cache behavior, or duplicate work. Tiling adds edge handling and synchronization.

Algorithmic minimum traffic provides a target, but actual hardware traffic includes line/transaction granularity. Measure before/after Q at each relevant boundary. A transformation can raise `I=W/Q` by increasing W; only accept recomputation if valid elapsed time/resource/energy improves under policy.

Distributed intensity can include network bytes with a network roof, but do not mix it into DRAM roof without a defined multilevel model. Domain decomposition, halo fusion, communication avoidance, and aggregation change network and memory traffic differently.

### Improve compute execution

When compute-side evidence dominates, enable legal vectorization, use appropriate intrinsics/libraries, improve instruction mix, expose independent operations, remove divergence, tune launch/block/task geometry, reduce register spills, and balance occupancy against per-thread resources. Match precision and rounding requirements.

Peak FLOP/s is irrelevant if the algorithm uses divides/transcendentals or mixed instructions whose throughput differs. Construct a ceiling for the limiting mix or use instruction/port models. On GPUs, occupancy enables latency hiding but maximum occupancy is not always maximum performance.

Changing precision, approximate math, associativity, tensor modes, or sparsity semantics is an algorithm/result change. Revalidate error, convergence, determinism/reproducibility policy, and domain outcomes.

### Kernel versus application

Optimize points weighted by complete critical-path time. A spectacular 2x speedup in a 2% kernel yields little total gain. Kernel fusion can remove launch/traffic but shift time. Reprofile the whole valid application after every meaningful transformation.

Applications have several points, not one average. Plot dominant kernels and aggregate only with a clearly meaningful numerator/denominator. Initialization, communication, I/O, scheduling, and synchronization may sit outside a compute-memory roof; use Amdahl/work-span/scaling and traces too.

At multi-node scale, per-rank roofs/points may differ due to imbalance, NUMA, device mapping, and problem partition. Retain max/distribution and identify the critical rank/device. Average FLOP/s can hide a late participant.

### Validation experiment

Establish an unprofiled baseline with result oracle and distributions. Capture a minimally perturbing profile and empirical ceilings. Form one mechanism hypothesis: excess DRAM traffic, low vector issue, latency, occupancy, or placement. Apply one controlled transformation.

Compare exact problem, stopping, precision, output, allocation, and environment. Report W, Q by level, I, t, achieved P, roof/efficiency, deeper counters, full application time, energy/resources when relevant, and numerical result. Retain compilation/vectorization reports and code changes.

Test sizes/alignments/strides/sparsity/batches, cold/warm states, placements, thread/rank/device counts, and repeated allocations. Reject an optimization that only wins the training input, violates memory limits, or harms tails. Bound the claim.

### Security, operations, and high-stakes limits

Counters and kernel names can expose model architecture, data shape, activity, co-tenants, or sensitive algorithms. Restrict profiler permissions, minimize/redact labels, protect reports, and define retention. Profiling can destabilize deadlines; use isolated authorized environments.

Bound allocations, working sets, tile sizes, counters, report volume, and replay. Validate numeric inputs and generated configuration. Monitor clocks/power/thermal state, correctable errors, memory/NUMA/device placement, performance drift, result checks, and regression envelopes.

High-stakes transformations require named domain, numerical, hardware/performance, security/privacy, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation review. A point nearer a roof does not establish scientific or deployment safety.

## Definitions and Notation

- W: counted useful operations for the named scope.
- `Q_H`: bytes crossing memory-hierarchy boundary H for that scope.
- t: elapsed time for the identical scope.
- `P=W/t`: achieved useful performance.
- `I_H=W/Q_H`: operational intensity at H.
- `B_H`: attainable bandwidth at H.
- `P_peak`: matching attainable/theoretical compute throughput.
- `P_roof,H=min(P_peak,B_H*I_H)`: basic roof at H.
- `I*=P_peak/B_H`: ridge point.
- `eta_roof=P/P_roof`: descriptive roof efficiency for matching quantities.
- **FMA convention**: explicit decision whether one fused multiply-add counts as two FLOPs.
- Obs: provenance, counter definitions, ceilings, performance, validity, and limitations.

No roofline quantity is boundary- or convention-free.

## Mechanisms, Invariants, or Proof Structure

### Dimensional and scope proof

W, Q, and t cover identical invocations; operations/precision and byte event/boundary are documented; units reduce correctly; the compute and bandwidth ceilings use the same allocation and relevant operation/access mix.

### Bound proof

Compute capacity implies `t>=W/P_peak`; bandwidth implies `t>=Q/B`; therefore `P=W/t<=min(P_peak,BW/Q)`. State omitted latency, dependencies, hierarchy, concurrency, and overhead; never infer equality.

### Counter/ceiling evidence proof

Validate tool/version/metric support, replay/overhead, clock/power/placement, and counter plausibility. Reproduce empirical ceilings with representative microbenchmarks and distributions. Investigate above-roof points as mismatches.

### Transformation equivalence proof

Before/after share semantic input, algorithm or declared change, precision/policy, convergence/output oracle, allocation, and environment. Traffic/instruction mechanism moves as predicted; full valid time/resources improve across representative cases.

### Claim-boundary proof

Name kernel, device, hierarchy, precision, work/byte conventions, ceilings, tool/version, problem/configuration, repetitions, result checks, headroom, deeper causal evidence, and tested envelope. Record unavailable evidence.

## Alternatives and Trade-Offs

| Technique | Main benefit | Principal limitation |
|---|---|---|
| theoretical roof | quick hardware sanity bound | may be unattainable for mix |
| empirical roof | realistic for measured setup | microbenchmark specificity |
| hierarchical roof | localizes cache/memory traffic | more counters/scope complexity |
| algorithmic intensity | portable minimum-data reasoning | differs from actual traffic |
| counter-derived intensity | observes executed traffic | tool/replay/event limitations |
| traffic reduction | raises intensity/lowers time | capacity, complexity, synchronization |
| recomputation | trades bandwidth for compute | energy/time/numeric cost |
| vector/tensor optimization | approaches compute ceiling | precision/mix/portability constraints |
| kernel fusion | removes traffic/launch | registers, occupancy, modularity |
| whole-application profiling | prioritizes impact | less compact than one roof |

## Failure Modes and Misconceptions

- **“Left of ridge proves memory-bound.”** saturation and other bottlenecks need evidence.
- **“Right of ridge proves compute-bound.”** dependencies/latency/occupancy may dominate.
- **“FLOP is unambiguous.”** FMA, precision, tensor, special and integer operations need convention.
- **“Bytes are input size.”** actual boundary traffic includes hierarchy and write/coherence effects.
- **“There is one intensity.”** every hierarchy boundary has one.
- **“Datasheet peak is attainable.”** mix, frequency, allocation, and throttling matter.
- **“Any bandwidth benchmark defines B.”** access mix, size, concurrency, and placement must match.
- **“Above roof means exceptional optimization.”** first audit units/scopes/counters/ceilings.
- **“Near roof means optimal algorithm.”** a lower-work algorithm may be faster below it.
- **“More FLOP/s means faster.”** work can change; report time-to-valid-solution.
- **“Higher intensity is always better.”** recomputation/register pressure can lose.
- **“Maximum occupancy is maximum performance.”** it is one latency-hiding constraint.
- **“Profiler counters are ground truth.”** support, approximation, multiplexing, and replay matter.
- **“One kernel represents the application.”** communication/I/O/other kernels can dominate.
- **“Average rank roof predicts completion.”** critical ranks/devices and imbalance matter.
- **“Reduced precision is a free optimization.”** error/convergence/domain results change.
- **“A chart diagnoses causality.”** use deeper counters and controlled perturbation.
- **“Roof proximity proves safety.”** validity and review remain independent.

## Worked Examples

### Example 1

**Unit check.** 300 GB/s times 2 FLOP/byte yields 600 GFLOP/s. **Conclusion:** dimensional analysis catches scale errors.

### Example 2

**FMA mismatch.** Tool counts each FMA as two FLOPs but hand model counts one. Intensity/performance disagree by two. **Conclusion:** declare convention.

### Example 3

**Hierarchy.** Tiling reduces DRAM Q fourfold but increases L1 traffic slightly; DRAM point moves right. **Conclusion:** reuse is boundary-specific.

### Example 4

**Latency below roof.** Sparse gathers achieve low bandwidth despite low intensity. TLB/cache misses and little concurrency dominate. **Conclusion:** low intensity does not prove bandwidth saturation.

### Example 5

**Compute mix.** A divide-heavy kernel is far below FMA peak but near a measured divide ceiling. **Conclusion:** match roof to instructions.

### Example 6

**Replay distortion.** Multi-pass profiling warms cache and halves measured Q. Single-pass/range controls expose it. **Conclusion:** validate collection semantics.

### Example 7

**Recomputation trade.** Avoiding a large temporary raises W 20% and cuts Q 50%; elapsed time improves 25%. **Conclusion:** evaluate valid time/resources, not intensity alone.

### Example 8

**Precision change.** FP16 tensor mode reaches a higher roof but changes convergence. Put it on a separate validated algorithm curve. **Conclusion:** roofs do not authorize numeric changes.

### Example 9

**Small hotspot.** A kernel moves near its roof and halves time but was 3% of the application. End-to-end gain is small. **Conclusion:** prioritize critical time.

### Example 10

**Real-time radiation transport.** Optimization must preserve patient/plan/anatomy/material/beam/time/coordinate/unit/calibration/model/mesh/random-stream/precision epochs, dose conservation and uncertainty, convergence and reference checks, hardware error/deadline/fallback behavior, privacy/security, audit/restart, and treatment-publication gates. Named radiation-oncology, medical-physics/dosimetry, numerical/Monte-Carlo, accelerator/HPC/performance, safety, security/privacy, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers must approve evidence; none is claimed here. **Conclusion:** higher roof efficiency does not validate dose or authorize treatment.

## Cross-Program Connections

- **Algorithms:** communication lower bounds, blocking, fusion, recomputation, and sparse formats determine W/Q.
- **Architecture:** caches, memory channels, vector/tensor units, issue ports, TLBs, and power define ceilings.
- **Compilers:** vectorization, instruction selection, fusion, aliasing, and reports connect code to execution.
- **GPUs:** coalescing, occupancy, divergence, shared memory, registers, HBM, and tensor units create hierarchical roofs.
- **NUMA/distributed systems:** placement and network traffic require boundary-specific models.
- **Numerical computing:** precision, FMA/order, convergence, conditioning, and error constrain transformations.
- **Performance engineering:** profiling, counters, empirical ceilings, replay controls, and regression envelopes provide evidence.
- **Statistics:** repetitions and uncertainty prevent false roof/headroom claims.
- **Security/operations:** counter access, trace sensitivity, thermals, and drift require governance.
- **Safety:** time and throughput remain subordinate to valid domain outcomes.

## References

1. Samuel Williams, Andrew Waterman, and David Patterson, “Roofline: An Insightful Visual Performance Model for Multicore Architectures,” *Communications of the ACM* 52(4), 2009. <https://doi.org/10.1145/1498765.1498785>
2. Lawrence Berkeley National Laboratory, *The Roofline Model: Visualizing and Optimizing Performance*, current documentation; retrieved 2026-08-29. <https://amcr.lbl.gov/departments/computer-science-department/ppan/roofline-performance-model/>
3. NERSC, *Roofline Performance Model*, current documentation; retrieved 2026-08-29. <https://docs.nersc.gov/tools/performance/roofline/>
4. NVIDIA, *Nsight Compute Profiling Guide: Roofline Charts*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html#roofline-charts>
5. NVIDIA, *Nsight Compute User Guide: Rooflines*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/nsight-compute/NsightCompute/>
6. NVIDIA, *Nsight Compute Release Notes*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/nsight-compute/ReleaseNotes/>
7. Intel, *Advisor User Guide: Analyze CPU Roofline*. <https://www.intel.com/content/www/us/en/docs/advisor/user-guide/2023-1/analyze-cpu-roofline.html>
8. Lawrence Berkeley National Laboratory, *Empirical Roofline Tool*, current documentation; retrieved 2026-08-29. <https://amcr.lbl.gov/departments/computer-science-department/ppan/roofline-performance-model/empirical-roofline-tool-ert/>
9. Lawrence Livermore National Laboratory, *Caliper: Performance Analysis Toolbox*, current documentation; retrieved 2026-08-29. <https://software.llnl.gov/Caliper/>
10. LIKWID Project, *Performance Monitoring and Benchmarking*, current documentation; retrieved 2026-08-29. <https://github.com/RRZE-HPC/likwid>

## Exercises

### Exercise 1

A kernel performs 90 GFLOP, transfers 30 GB at DRAM, and takes .05 s. With 6 TFLOP/s compute and 400 GB/s bandwidth ceilings, compute intensity, achieved performance, ridge, roof, roof efficiency, and basic region. State what is not proved.

### Exercise 2

Define operation and byte-count conventions for a mixed FP64/FP32/FMA/transcendental GPU kernel at L2 and HBM boundaries. Include matching ceilings and sanity checks.

### Exercise 3

A point is below both roofs. Design controlled tests distinguishing bandwidth saturation, latency/MLP, vector/instruction mix, occupancy/register pressure, imbalance, and profiler replay.

### Exercise 4

Compare tiling, fusion, compression, recomputation, vectorization, and precision change for one kernel. Specify predicted roof movement, side effects, and acceptance evidence.

### Exercise 5

Transfer roofline analysis to accelerated emergency cardiac ultrasound reconstruction. Specify work/traffic, numeric/clinical, device/deadline/failure, privacy/security, validation, publication, and named reviewer invariants without claiming review.

## Answers to the Exercises

### Answer 1

`I=90/30=3 FLOP/byte`. Achieved `P=(90/1000)/.05=1.8 TFLOP/s`. Ridge is `6000/400=15 FLOP/byte`. Bandwidth roof is `400*3=1200 GFLOP/s=1.2 TFLOP/s`, so the claimed achieved point exceeds the matching roof and roof efficiency would be 1.5. Do not label the region/bottleneck; audit decimal/binary units, scope, work/FMA convention, byte counter/boundary, time, ceiling, compression/cache, allocation, and replay. With matching correct inputs, the bound cannot be exceeded. The nominal left-of-ridge position alone would not prove bandwidth saturation.

### Answer 2

Count FP64/FP32 add/multiply separately; state FMA as two operations or retain FMA instructions; report transcendental calls separately rather than assigning arbitrary FLOP equivalents. For each identical invocation, obtain L2 and HBM transferred bytes from documented device metrics including read/write transaction semantics. Compute separate intensities per work category and boundary. Use FP64, FP32/FMA, and special-function attainable ceilings matching mix, active device, clocks and occupancy; measure L2/HBM bandwidth with representative sizes/read-write/stride/coalescing/concurrency. Sanity-check algorithmic minimum bytes, transaction granularity, W/t, Q/t versus attainable bandwidth, counter support/replay, and unprofiled result/time.

### Answer 3

First validate matching scope/counters/ceilings and compare profiled/unprofiled runs. Bandwidth saturation needs Q/t near a representative empirical B; vary working set and channels/placement. Latency/MLP is supported by low bandwidth plus long memory stalls and improves with more independent requests/prefetch without changing Q much. Inspect vector/tensor instruction mix, IPC/issue/dependencies and compare a matching compute microkernel. Vary block/task geometry and registers/shared memory to test occupancy/spills, noting occupancy alone is not goal. Retain per-thread/rank/device distributions and rebalance/rotate data for skew. Collect fewer metrics/single-pass or replay-safe ranges and compare cache state for replay. Require predicted counter movement and full valid time improvement across repetitions.

### Answer 4

Tiling/fusion should reduce Q at selected levels and move right/up, but can raise code size, synchronization, registers and spills. Compression reduces Q but adds W/branches and changes representation; validate lossless/lossy semantics. Recomputation raises W while reducing Q/storage; accept only lower valid time/resource/energy. Vectorization raises achieved compute toward a matching vector ceiling but may alter tails/order. Precision change selects a different roof and is a separate numerical algorithm requiring error/convergence/domain approval. For each predict W/Q/ceiling effects, retain exact input/allocation/environment, measure hierarchy traffic/instructions/stalls/time/resources, validate output/numerics, test representative shapes/placements, and reprofile whole application.

### Answer 5

Define useful operations by precision/FMA/transform/interpolation convention and L2/HBM/host-device bytes over the exact acquisition-to-image kernels; construct attainable ceilings for the deployed device and clock/power mode. Preserve patient/study/probe/frame/time/coordinate/unit/calibration/model/algorithm/precision/device epochs, image geometry, reconstruction residual/reference/quality and diagnostic boundary. Enforce deadline, dropped/corrupt frame, device error/throttle, memory bound, watchdog, checkpoint/fallback and fail-closed display. Protect consent/purpose, authenticated encrypted least-privilege data, pseudonymous IDs, bounded redacted counters/traces, retention/audit. Validate phantoms and independent clinical cases, higher-precision/reference outputs, adversarial shapes/motion/devices/thermals/failures, restore, subgroup/artifact sensitivity, security/privacy, and clinical workflow. Named cardiology/emergency medicine, ultrasound imaging/medical physics, numerical/reconstruction, accelerator/HPC/performance, clinical data/privacy/security, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers are required. No external review, diagnostic validity, privacy guarantee, approval, or deployment authorization is claimed.
