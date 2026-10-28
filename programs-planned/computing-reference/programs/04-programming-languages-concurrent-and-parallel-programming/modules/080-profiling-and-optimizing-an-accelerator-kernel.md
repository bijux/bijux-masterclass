---
module_id: CONPAR-080
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 80
title: Profiling and Optimizing an Accelerator Kernel
status: complete
last_verified: 2026-08-29
---

# Profiling and Optimizing an Accelerator Kernel

## One-Page Review

### Governing question

How can a team identify the true limiter of an accelerator workload, make one semantics-preserving change, and produce reproducible evidence that explains—not merely reports—the improvement?

### Essential definitions

- A **performance question** names a workload, target, objective, observation boundary, and suspected limiting mechanism.
- A **baseline** is a version and measurement protocol against which candidates are compared.
- **Wall-clock/end-to-end time** spans the user-relevant boundary; **kernel time** spans device execution under a declared event/profiler boundary.
- A **timeline trace** records CPU, runtime, copies, kernels, synchronization, and idle/queue intervals.
- A **hardware counter** counts or samples a target-specific event; its name is not a portable semantic quantity.
- **Profiler replay** re-executes a kernel/application/range to collect counters that cannot be observed simultaneously.
- **Operational intensity** is useful operations divided by measured/modelled bytes at a named hierarchy boundary.
- A **roofline bound** is `min(peak_compute, bandwidth × intensity)` under the model's assumptions.
- **Latency**, **throughput**, **utilization**, **occupancy**, **efficiency**, and **speedup** are different quantities.
- A **warm-up** establishes compilation, allocation, cache, power/clock, and runtime state according to protocol.
- A **controlled experiment** changes one causal factor while holding relevant semantics and conditions constant.
- **Uncertainty** includes run variation, measurement error, sampling, counter/replay effects, and workload variation.

### Central model, mechanism, or theorem

Optimization is an evidence loop: define required outputs and objective; capture reproducible baseline; use a system timeline to locate the dominant boundary; form one falsifiable hypothesis; collect the smallest relevant kernel metrics; predict which counters and time should move; implement one change; revalidate values, races, bounds, resources, and failures; repeat timing outside intrusive profiling; and retain artifacts. Roofline and utilization metrics narrow hypotheses but do not prove causality or headroom. A candidate is accepted only when correctness holds and the intended end-to-end objective improves across representative workloads without unacceptable tails, capacity, energy, portability, privacy, or reliability regressions.

### Critical invariants

Baseline and candidate process identical logical inputs and produce equivalent declared outputs; target, binary, compiler flags, libraries, driver/runtime, clocks/power, concurrency, and data state are recorded; asynchronous work is timed through completion; warm-up and sample exclusion are declared; units and metric definitions are checked; replayed workloads are deterministic or use a suitable mode; counter collection perturbation is separated from production timing; operations and bytes name their boundary; transformations preserve ownership, synchronization, numeric, error, and lifetime contracts; final resource/spill reports are captured; and every claim includes distributions, provenance, limitations, and rollback evidence.

### Common failures

Teams optimize the longest-looking source line, time enqueue calls, compare different inputs or build modes, trust one run, delete outliers without policy, hide warm-up, mix clock states, collect every counter at once, ignore profiler replay/serialization, treat percentages as additive or causal, use peak specifications as achieved ceilings, call low occupancy the bottleneck, confuse requested with transferred bytes, count FLOPs inconsistently, change several factors, accept wrong results within a loose tolerance, profile debug binaries, overlook spills/launches/transfers, expose sensitive traces, or publish a microbenchmark gain while service tails regress.

### Compact example

A deterministic teaching record has baseline times `[10.2,10.0,10.1,10.3,10.1]` and candidate `[7.9,8.0,8.1,8.0,7.8]`. Their medians are 10.1 and 8.0, giving 1.2625× median speedup. With 4,096 operations, 2,048 boundary bytes, 1,000 ops/unit compute peak, and 300 bytes/unit bandwidth, modeled intensity is 2 and roofline is 600 ops/unit. These arithmetic facts do not validate the measurements or candidate.

### Connections

[Heterogeneous CPU-GPU Pipelines](079-heterogeneous-cpu-gpu-pipelines.md) defines end-to-end stages and event timing. [Coalescing, Divergence, and Occupancy](077-coalescing-divergence-and-occupancy.md) supplies transaction/mask/residency ledgers. [Kernel Fusion and Data Movement](078-kernel-fusion-and-data-movement.md) supplies transformation trade-offs. The [program roadmap](../ROADMAP.md) next begins distributed-memory programming.

## Governing Question

Under a frozen workload and correctness contract, what measured mechanism limits the chosen objective, which transformation should move the corresponding evidence, and did it do so without moving cost or risk outside the observation boundary?

The disciplined answer is a reproducible experiment bundle, not a screenshot. Profilers provide observations conditioned on target and collection mode. Interpretation joins those observations with source/IR, hardware documentation, workload semantics, and counterfactual changes.

## Why This Matters

Accelerator performance is multidimensional. A kernel can wait on memory dependencies despite low DRAM bandwidth, issue sparse lanes despite high occupancy, saturate a special-function pipeline at low arithmetic throughput, or run quickly while host submission and transfers dominate. Metric chasing often optimizes the wrong layer.

Profiling itself changes execution: tools may serialize kernels, lock counters, replay work, save/restore memory, flush caches, stabilize clocks, inject code, or sample. A production-grade method understands these effects, uses profiling to diagnose, and measures final latency separately.

Correctness remains the hard constraint. Layout, fusion, fast math, atomics, work reordering, precision, and launch changes can alter identities, races, exceptions, and numerical results. Every tuning commit therefore carries semantic and performance evidence.

## Prerequisites and Retrieval

Retrieve:

- end-to-end DAGs, completion timing, backpressure, concurrency, and failure from [Heterogeneous CPU-GPU Pipelines](079-heterogeneous-cpu-gpu-pipelines.md);
- transactions, active masks, occupancy/readiness, resource cliffs, ILP/MLP, and causal experiments from [Coalescing, Divergence, and Occupancy](077-coalescing-divergence-and-occupancy.md);
- memory boundaries, tiling, caches, spills, migration, and byte ledgers from [GPU Memory Hierarchies](076-gpu-memory-hierarchies.md); and
- fusion/fission, compiler resources, graphs, and fallback from [Kernel Fusion and Data Movement](078-kernel-fusion-and-data-movement.md).

Retrieval prompt: write the exact objective, workload distribution, output oracle, target/build manifest, observation boundary, timing method, warm-up/repetition policy, system timeline, top three limiting hypotheses, and evidence that would falsify each. Which data is measured, derived, modeled, or assumed?

## Learning Objectives

After completing this module, a learner can:

1. define a reproducible accelerator baseline and user-relevant objective;
2. distinguish system tracing, API/event timing, kernel profiling, sampling, counters, and static resource reports;
3. account for warm-up, clocks, caches, concurrency, replay, serialization, and tool overhead;
4. calculate median speedup, variation summaries, operational intensity, and simple roofline bounds with limitations;
5. map timeline, memory, scheduler, pipeline, instruction, occupancy, divergence, and stall evidence to hypotheses;
6. design one-variable counterfactual experiments and expected counter movement;
7. preserve semantic, numeric, synchronization, bounds, lifetime, failure, and high-stakes correctness;
8. automate profiler artifacts and performance regression checks without brittle universal thresholds;
9. assess portability, capacity, energy, tails, multi-tenancy, privacy, rollout, and rollback; and
10. communicate what improved, why, where it applies, and what remains unverified.

## Core Exposition

### Freeze the question and baseline

Choose an objective: per-item latency, batch throughput, deadline misses, energy, cost, capacity, or a constrained combination. Name start/end: API request to validated response, pipeline stage, or kernel event. An optimization outside that boundary cannot satisfy the objective merely because a local metric rises.

Version inputs and their size/distribution/skew; shapes/layouts/dtypes; output/numeric/determinism policy; source/commit; compiler and flags; generated binary/IR; libraries; driver/runtime/firmware; device UUID/model/features; clocks/power/thermal mode; host/NUMA; queue/concurrency; and environment. Use release-like binaries with debug/line correlation appropriate to the profiler.

Warm compilation, allocation, page migration, caches, and clocks only as the intended production state dictates. Cold-start and steady-state are separate workloads. Predeclare sample count, exclusions, timeout, summary statistics, and comparison threshold. Retain raw samples.

### Locate the boundary before counters

Measure end-to-end with completion, then collect a system timeline showing host threads, runtime calls, transfers, kernels, waits, queues, and idle gaps. Determine whether time lies in CPU preparation, submission, transfer/migration, one kernel, synchronization, validation, queueing, or contention. A detailed kernel profile is waste when the accelerator is mostly idle between launches.

Use device events for kernel/stream intervals when supported, but understand clock domain, resolution, queue placement, and synchronization. Host timers around an asynchronous launch measure enqueue overhead. OpenCL/SYCL event timestamps distinguish queued, submitted, start, and end according to supported profiling semantics. Never compare timestamps across domains without a calibrated relation.

### Form a falsifiable hypothesis

Examples: “misaligned strided loads inflate DRAM sectors; structure-of-arrays will lower transferred bytes and time”; “a dependency chain leaves few eligible warps; processing two independent items per thread will raise readiness”; “fusion removes an intermediate but spills; a smaller fusion group will lower local traffic”; “small kernels are launch-bound; graph replay will reduce CPU gaps but not kernel duration.”

For each, predict what should remain invariant, which source/IR changes, which metrics move, and how time responds if the mechanism is causal. Also state a falsifier. Change one factor; otherwise attribution becomes ambiguous.

### Read metrics as target-specific evidence

Metric names, units, aggregation, normalization, availability, and collection mode vary. Read the current profiler metric documentation for the exact target/tool. Percent-of-peak metrics can refer to active cycles, elapsed cycles, subpartitions, instances, or a model; two percentages usually cannot be added.

Correlate source with generated instructions and static compiler resources. A source load can become multiple operations; an apparent local scalar can spill. Inspect launches, registers, local/shared memory, barriers, block shape, and occupancy limits before dynamic counters.

Memory evidence includes requested/actual bytes or transactions at named levels, cache hits/misses, sectors, TLB/fault/migration, bank conflicts, and throughput. High bandwidth can mean useful streaming or waste. Low bandwidth can mean dependency-limited latency. Pair traffic with useful work, eligible issue, stalls, and timing.

Scheduler evidence includes active/eligible/issued execution groups, active lanes, divergence, occupancy, and stall reasons. Stall labels are symptoms categorized by tool, not automatic prescriptions. A “memory dependency” stall can be reduced by locality, MLP, ILP, or less work; increasing occupancy may spill and worsen it.

Pipeline/instruction evidence includes instruction mix, issue/throughput, tensor/vector/scalar/special-function utilization, dependencies, and branch/source sampling. Peak utilization on one pipeline can identify a bound; low values everywhere can mean short workload, latency, imbalance, synchronization, or missing concurrency.

### Roofline with declared accounting

Let useful work W use operations defined consistently with the peak P. Let Q be bytes crossing a named boundary and `I=W/Q`. With bandwidth B, a simple upper bound is `min(P,B·I)`. The ridge intensity is `P/B`. Multiple cache levels, mixed precisions/instructions, imbalance, latency, and non-overlapped pipelines require hierarchical or richer models.

Do not count algorithm FLOPs one way and hardware peak another. Fused multiply-add conventions, tensor operations, sparsity, integer work, and transcendental instructions matter. Q may be algorithm-minimum, compiler-modelled, or counter-derived; label it. A point below a roof does not prove reachable headroom or identify the cause.

### Replay and perturbation

Hardware counters are limited, so profilers may collect multiple passes. Kernel replay may save/restore written memory and cannot safely reproduce host-interactive or nondeterministic behavior. Application replay duplicates the full program and requires matchable deterministic launches. Range replay and sampling have other limits.

Profilers may serialize concurrent kernels, flush caches, stabilize clocks, or inject instrumentation. These choices improve some reproducibility while departing from production. Record mode, passes, cache control, clock behavior, filters, dropped samples, and warnings. Use minimal metric sets and a narrow representative region. Measure unprofiled time separately.

### Transform and revalidate

Select the smallest transformation supported by evidence: layout/alignment; tiling/reuse; branch/work grouping; block/launch shape; register live ranges/unroll; fusion/fission; batching/graphs; async overlap; precision/library/algorithm—only within contract.

Run reference/differential tests across zero/small/large, alignment/tile tails, random/adversarial data, numeric extremes, dynamic shapes, target variants, concurrency, and pressure. Use race/bounds/uninitialized tools. Capture compiler resources and reject new spills or cliffs unless measured and justified. Test failures, cancellation, and fallback for structural changes.

Then repeat timing without intrusive collection. Report raw and summarized distributions, speedup `T_baseline/T_candidate`, absolute savings, tails, confidence/uncertainty approach, and practical effect. A statistically detectable microsecond change may be operationally irrelevant; a mean gain with tail/capacity regression may be unacceptable.

### Variation, comparison design, and regression decisions

GPU timings vary with temperature, frequency, power limits, background activity, allocation, address placement, cache history, queue interference, and input-dependent work. Repeating a poorly controlled experiment estimates a mixture rather than the effect of the change. Stabilize what production actually stabilizes, record what cannot be fixed, and deliberately sample the operating range that the claim covers.

When drift is plausible, interleave or randomize baseline and candidate runs instead of completing all baseline trials first. Pair trials that share an input, device state, and time neighborhood, then retain the pair identity. For deterministic microbenchmarks on an isolated target, median and robust spread may communicate the center adequately; service workloads also need quantiles, deadline misses, throughput under offered load, and queue/capacity behavior. State whether intervals come from a justified parametric model, bootstrap, repeated independent runs, or only descriptive summaries.

Do not repeatedly try variants and report the luckiest result as if it were a preplanned comparison. Exploration is legitimate, but separate it from confirmation: discover candidates on one input/target set, freeze the winning hypothesis and implementation, then evaluate on held-out workloads and supported targets. If many metrics or variants were screened, record the multiplicity and avoid overinterpreting small changes.

A regression gate needs a practical tolerance derived from user/service budgets and laboratory noise. It may combine “no correctness failure,” an absolute latency budget, a relative slowdown band, minimum repetitions, and an inconclusive state that triggers rerun rather than pass/fail. Architecture-specific expected bands are clearer than one universal percentage. Track the baseline intentionally when hardware, compiler, or workload changes; never silently bless a regression by regenerating reference numbers.

Performance claims should include both ratio and absolute change. A 2× speedup from two microseconds to one may not affect end-to-end behavior, while a 5% reduction in a dominant hour-long stage can be substantial. Translate the result into the chosen objective—requests per second at bounded tail, energy per result, device count, or deadline margin—while keeping the kernel evidence available for causal explanation.

### Executable evidence arithmetic

This Python model recomputes medians, speedup, intensity, and a simple roofline from supplied numbers. It does not measure hardware, validate sample independence, estimate confidence, define profiler counters, or prove causality/correctness.

<!-- bijux-verify: {"id":"accelerator-evidence-arithmetic","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"baseline_samples=[10.2, 10.0, 10.1, 10.3, 10.1]\ncandidate_samples=[7.9, 8.0, 8.1, 8.0, 7.8]\nbaseline_median=10.100\ncandidate_median=8.000\nmedian_speedup=1.262500\noperational_intensity=2.000\ncompute_ceiling=1000.000\nbandwidth_ceiling=600.000\nroofline_bound=600.000\nachieved_fraction_of_bound=0.667\noutputs_equivalent=True\n","stderr":""}} -->
```python
baseline = [10.2, 10.0, 10.1, 10.3, 10.1]
candidate = [7.9, 8.0, 8.1, 8.0, 7.8]

def median(values):
    ordered = sorted(values)
    return ordered[len(ordered) // 2]

baseline_median = median(baseline)
candidate_median = median(candidate)
operations = 4096
boundary_bytes = 2048
compute_peak = 1000.0
bandwidth = 300.0
achieved = 400.0
intensity = operations / boundary_bytes
bandwidth_ceiling = bandwidth * intensity
roofline_bound = min(compute_peak, bandwidth_ceiling)

print(f"baseline_samples={baseline}")
print(f"candidate_samples={candidate}")
print(f"baseline_median={baseline_median:.3f}")
print(f"candidate_median={candidate_median:.3f}")
print(f"median_speedup={baseline_median / candidate_median:.6f}")
print(f"operational_intensity={intensity:.3f}")
print(f"compute_ceiling={compute_peak:.3f}")
print(f"bandwidth_ceiling={bandwidth_ceiling:.3f}")
print(f"roofline_bound={roofline_bound:.3f}")
print(f"achieved_fraction_of_bound={achieved / roofline_bound:.3f}")
print("outputs_equivalent=True")
```

### Automation, operations, and ethics

Store scripts/configuration, manifests, raw timings, profiler reports, parsed summaries, stdout/stderr, tool versions, and environment under governed artifacts. CI should run stable correctness and modest performance sentinels on controlled targets; noisy shared runners need broad signals, not brittle percent thresholds. Periodic lab runs can perform deeper profiling.

Counter names evolve, so parsers fail closed on missing/renamed metrics and retain raw reports. Compare like targets or normalize only with an explicit model. Performance budgets should distinguish expected architecture bands.

Profiler artifacts can contain source, symbols, addresses, kernel/model shapes, timing patterns, and data-derived control behavior. Minimize scope, redact, encrypt/access-control, expire, and never profile sensitive production input without authorization.

Roll out by target/workload class with canaries. Monitor correctness sentinels, latency/throughput distributions, memory, errors, resets, energy/cost, and fairness. Keep a verified rollback/fallback. High-stakes acceptance requires named human review beyond internal profiling.

## Definitions and Notation

- `T_b,T_c`: baseline and candidate time distributions.
- `S=stat(T_b)/stat(T_c)`: speedup for a declared statistic.
- `W`: useful work under a declared operation convention.
- `Q_q`: bytes at hierarchy boundary q.
- `I_q=W/Q_q`: operational intensity at q.
- `P`: compatible peak compute rate.
- `B_q`: bandwidth ceiling at q.
- `R_q=min(P,B_q I_q)`: simple roofline bound.
- `U_m`: profiler metric m under its documented unit/normalization.
- `C`: complete configuration/provenance manifest.
- `H`: falsifiable performance hypothesis.
- `Obs`: declared semantic observations and oracle.

Equal `Obs` is required before S is meaningful; a derived R is not a measured time.

## Mechanisms, Invariants, or Proof Structure

### Measurement validity argument

Define boundary, clock/event method, completion, warm-up, samples/exclusions, workload, target/build, state, and tool perturbation. Raw records reproduce the summary calculation. Baseline and candidate differ only in declared factors and are interleaved/randomized when drift warrants it.

### Semantic equivalence argument

For every relevant input/target, compare identity, bounds, ownership, synchronization, numeric/error behavior, output, and side effects under the declared oracle. Sanitizer/race and resource evidence address mechanisms not captured by value samples.

### Roofline derivation

Use compatible definitions for W and P and a named boundary for Q/B. Compute I and both ceilings with units. Interpret only as a conditional upper envelope; add hierarchy ceilings or abandon the model when assumptions fail.

### Causal optimization argument

H predicts a transformation, source/IR effect, metric movement, and time response. The experiment preserves Obs and conditions. Evidence matching all predictions supports H; mismatch refutes or weakens it. One correlation or rule suggestion is insufficient.

### Deployment argument

Candidate passes representative correctness/performance, target, concurrency, capacity, failure, privacy, and rollback gates. Scope and limitations are documented; monitoring can distinguish regression and trigger safe fallback.

## Alternatives and Trade-Offs

| Method | Best use | Principal limitation |
|---|---|---|
| Host end-to-end timer | user-visible objective | needs explicit completion; coarse attribution |
| Device events | queue/kernel intervals | clock/domain/API constraints |
| System timeline | CPU-runtime-transfer-kernel gaps | overhead and limited microarchitecture detail |
| Kernel counters | mechanism diagnosis | target-specific, replay/perturbation |
| Sampling | long/live workloads | statistical loss and attribution |
| Static compiler report | resources/instructions | no dynamic workload behavior |
| Roofline | compute/byte ceiling orientation | simplified assumptions/accounting |
| Microbenchmark | isolate mechanism/ceilings | representativeness risk |
| Differential benchmark | candidate causal comparison | controls/drift/uncertainty required |
| Production telemetry | real workload/SLO | confounding, privacy, limited counters |

Use the least intrusive method that answers the current question; triangulate when stakes are high.

## Failure Modes and Misconceptions

- **“The profiler tells me the bottleneck.”** it reports evidence under a collection mode.
- **“Kernel duration is application duration.”** launches, transfers, queues, and CPU stages remain.
- **“Host launch timing measures the kernel.”** asynchronous submission returns early.
- **“One run is representative.”** variation and state remain unknown.
- **“Warm-up should always be discarded.”** cold start may be the real objective.
- **“All counters are simultaneous.”** collection often replays.
- **“Replay is transparent.”** state, host interaction, caches, and concurrency can differ.
- **“A high percentage is good.”** it may measure useless or wrong work.
- **“Low occupancy causes every stall.”** readiness and limiter matter.
- **“High bandwidth means memory efficient.”** traffic can be wasteful.
- **“Roofline distance is guaranteed headroom.”** other ceilings and dependencies intervene.
- **“Peak specs match my operations.”** dtype, instruction, clocks, and conventions differ.
- **“A rule recommendation proves causality.”** test its predicted mechanism.
- **“Multiple changes save time.”** they destroy attribution.
- **“Tolerance means correctness.”** it must be scientifically/domain justified.
- **“A mean speedup is enough.”** tails, failures, capacity, energy, and fairness matter.
- **“Profiler reports are harmless.”** they may expose source and sensitive workload structure.

## Worked Examples

### Example 1

**Enqueue illusion.** A host timer reports 8 microseconds around a 2-millisecond asynchronous kernel launch. **Conclusion:** wait/event at the required completion boundary.

### Example 2

**System gap.** Timeline shows 40% idle time between 20-microsecond kernels due to serial host submission. Graph replay improves the gaps. **Conclusion:** profile the system before kernel internals.

### Example 3

**Bandwidth waste.** DRAM throughput is high but useful/actual bytes is 0.3 from stride. Layout lowers bytes and time. **Conclusion:** saturation can reveal inefficiency, not success.

### Example 4

**Dependency latency.** DRAM bandwidth is low while long-scoreboard stalls dominate and few warps are eligible. More independent loads help. **Conclusion:** low bandwidth need not mean compute-bound.

### Example 5

**Occupancy regression.** A register cap raises theoretical occupancy but spills and slows the kernel. **Conclusion:** treat calculators as candidate generators.

### Example 6

**Replay mismatch.** Kernel replay hangs because the kernel exchanges state with the host. Application replay or sampling is required. **Conclusion:** collection mode is part of validity.

### Example 7

**Cold versus warm.** JIT compilation dominates first request but disappears in steady state. Precompilation helps cold latency; kernel tuning does not. **Conclusion:** optimize the declared workload phase.

### Example 8

**Fusion trade-off.** Fusion removes global traffic but doubles registers and creates spills. A smaller group wins end-to-end. **Conclusion:** inspect final resources and all boundaries.

### Example 9

**Tail regression.** Candidate improves median 20% but worsens p99 under concurrency due to memory pressure. **Conclusion:** the acceptance objective includes tails/capacity.

### Example 10

**Cardiac image reconstruction.** A faster kernel must preserve patient/series/geometry identity, calibration, units, sampling trajectory, coil maps, precision/reduction and convergence policy, uncertainty, artifacts, failure/fallback, privacy, and audit. Named cardiology/radiology, medical physics, reconstruction/numerical, GPU/compiler, software-safety, security/privacy, operations, quality/regulatory, human-factors, and independent validation reviewers must approve requirements and evidence; none is claimed here. **Conclusion:** profiler evidence establishes neither diagnostic validity nor clinical safety.

## Cross-Program Connections

- **Scientific method:** hypotheses, controls, falsifiers, replication, uncertainty, and scope structure optimization.
- **Statistics:** distributions, paired/interleaved designs, effect sizes, drift, and multiplicity govern inference.
- **Computer architecture:** counters expose caches, memory, schedulers, pipelines, instructions, and power states.
- **Compilers:** IR, code generation, register allocation, fusion, vectorization, and fast math mediate source changes.
- **Numerical computing:** operation counts, rounding, convergence, and tolerance define valid equivalence.
- **Distributed systems:** queueing, contention, tails, telemetry, canaries, and rollback shape service results.
- **Testing:** oracles, adversarial inputs, sanitizers, metamorphic checks, and target matrices protect behavior.
- **Security:** traces, symbols, addresses, shapes, and timing can leak implementation or data properties.
- **Operations:** automation, provenance, regression bands, capacity, energy/cost, and failure evidence sustain gains.
- **Communication:** causal claims must distinguish measurement, derivation, model, assumption, and limitation.

## References

1. Samuel Williams, Andrew Waterman, and David Patterson, “Roofline: An Insightful Visual Performance Model for Multicore Architectures,” *Communications of the ACM* 52(4), 2009. <https://doi.org/10.1145/1498765.1498785>
2. NVIDIA, *Nsight Compute Profiling Guide*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html>
3. NVIDIA, *Nsight Compute User Guide*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/nsight-compute/NsightCompute/>
4. NVIDIA, *Nsight Systems User Guide*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/nsight-systems/UserGuide/index.html>
5. NVIDIA, *CUDA C++ Best Practices Guide*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html>
6. AMD, *ROCprofiler Compute Documentation*, current documentation; retrieved 2026-08-29. <https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/>
7. AMD, *ROCprofiler SDK Documentation*, current documentation; retrieved 2026-08-29. <https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/latest/>
8. AMD, *HIP Performance Guidelines*, current documentation; retrieved 2026-08-29. <https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/performance_guidelines.html>
9. Khronos OpenCL Working Group, *clGetEventProfilingInfo*, current reference; retrieved 2026-08-29. <https://registry.khronos.org/OpenCL/specs/unified/refpages/man/html/clGetEventProfilingInfo.html>
10. Khronos SYCL Working Group, *SYCL 2020 Specification*, revision 12, event profiling, 2026. <https://registry.khronos.org/SYCL/specs/sycl-2020/html/sycl-2020.html>

## Exercises

### Exercise 1

Design a reproducible baseline protocol for a kernel used in a latency-sensitive service, covering correctness, workload, build/target, warm/cold state, timing, samples, concurrency, and artifacts.

### Exercise 2

Recompute the compact-example median speedup and roofline, check units, find the ridge intensity, and list why the bound does not prove optimization headroom.

### Exercise 3

A trace shows GPU idle gaps; a kernel profile shows low occupancy and high memory stalls. Create competing hypotheses and controlled experiments that decide which boundary matters first.

### Exercise 4

Plan an evidence-driven optimization of an irregular gather/reduction kernel, including counter selection, replay hazards, transformations, semantic checks, and acceptance gates.

### Exercise 5

A regulated genomic risk pipeline proposes mixed precision and fusion after profiling. Specify numerical, domain, privacy, compiler/device, failure, performance, and human-review evidence before release.

## Answers to the Exercises

### Answer 1

Define request-to-validated-response and kernel-event boundaries and the latency/tail objective. Version inputs/distributions, oracle/tolerance/determinism, source/binary/IR, compiler/flags/libraries, driver/runtime, device UUID/features, host/NUMA, clocks/power/thermal, queues and tenants. Measure cold start separately from warmed steady state; complete asynchronous work; interleave baseline/candidate when drift matters; predeclare repetitions, exclusions, timeout, statistics, and effect threshold; retain raw samples. Capture a system timeline, stage durations, resources, errors, memory high water, and correctness/race/bounds results. Store scripts/config, manifests, reports, outputs, tool versions, and limitations; test concurrency/pressure/failure and rollback.

### Answer 2

Sorted baseline median is 10.1; candidate median is 8.0; speedup is `10.1/8=1.2625`. Intensity is `4096 ops/2048 bytes=2 ops/byte`. Compute ceiling is 1000 ops/unit-time; bandwidth ceiling is `300 bytes/unit-time × 2 ops/byte=600 ops/unit-time`; roofline is 600 and ridge intensity is `1000/300=3.333... ops/byte`. Achieved 400 is two-thirds of the modeled bound. The calculation does not validate operation/byte counting, measured peaks, hierarchy, sample independence, target clocks, other pipelines, latency/dependencies, imbalance, profiler perturbation, correctness, or attainability; it cannot identify a transformation alone.

### Answer 3

Hypothesis A: host submission/dependencies create gaps, so batching or graph replay reduces timeline idle intervals and end-to-end time while kernel counters/duration remain similar. Hypothesis B: within launched kernels, low ready work exposes memory latency, so layout/MLP or reviewed block/resource changes reduce relevant transactions/stalls or raise eligible issue and kernel time. First quantify end-to-end contribution of gaps; if dominant, test graph/batched submission with identical kernels/results. Then profile a representative kernel narrowly outside concurrency distortion and test one kernel transformation. Low occupancy plus memory stalls does not prove raising occupancy. Accept only predicted metric/time movement and preserved correctness across production concurrency.

### Answer 4

Freeze graph inputs/identity, exact integer and declared floating/reduction order, ownership/atomics, and output oracle. Timeline first; then collect requested/actual bytes and cache level, gather transactions, active masks/branch/source, atomics/contention, eligible/issued groups, stalls, resources/spills, and duration using minimal documented metrics. Ensure replay is safe for atomics/nondeterminism or choose application/range replay/sampling; record cache/clock/serialization effects. Test layout/bucketing, local aggregation, work grouping, tile/cache reuse, or algorithm/library alternatives one at a time. Revalidate races, bounds, order/tolerance, extremes, tails, devices, compiler modes, pressure and failure. Accept on end-to-end distributions plus intended evidence, resource/capacity/fairness limits, and rollback.

### Answer 5

Define sample/patient/reference/feature/model identity, biological/statistical specification, units, preprocessing, missing/duplicate policy, exact integer and floating/reduction/convergence semantics, mixed-precision error budgets by stratum, uncertainty/calibration, bias and action threshold. Differentially validate unfused/full-precision and candidate intermediates/finals across extremes, populations, targets, compilers and repeated orders; inspect IR/instructions/resources/spills and race/bounds evidence. Key and validate generated artifacts; control fast-math and fallback. Benchmark complete cold/warm/concurrent pipelines with raw distributions, counter/replay provenance, capacity, errors and device loss. Encrypt/minimize genomic inputs and profiler artifacts; isolate access, audit, retain/erase. Named genomics, bioinformatics/statistics, clinical/laboratory, numerical, compiler/GPU, security/privacy, operations/SRE, quality/regulatory, human-factors, and independent validation reviewers approve validity, bias, limitations and residual risk. Profiling, fusion, and tolerance tests alone establish no biological or clinical validity.
