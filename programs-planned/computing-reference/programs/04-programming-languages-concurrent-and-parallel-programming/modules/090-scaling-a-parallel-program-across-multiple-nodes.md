---
module_id: CONPAR-090
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 90
title: Scaling a Parallel Program Across Multiple Nodes
status: complete
last_verified: 2026-08-29
---

# Scaling a Parallel Program Across Multiple Nodes

## One-Page Review

### Governing question

How can a team demonstrate that a correct parallel program converts additional nodes into faster time-to-valid-solution or greater validated throughput, while identifying the computation, communication, memory, I/O, imbalance, placement, and system effects that limit the scaling range?

### Essential definitions

- **strong scaling** holds the global problem and required result fixed while increasing resources.
- **weak scaling** increases global work with resources while holding stated work per resource approximately fixed.
- **speedup** is `S_p=T_1/T_p` for comparable validated runs; the baseline need not literally use one process, but its resource count must be explicit.
- **parallel efficiency** relative to baseline b is `E_p=(T_b/T_p)/(p/b)` when p and b are comparable resource units.
- **cost** is `C_p=p*T_p` in resource-time units; cost optimality and monetary/energy costs need separate definitions.
- **throughput** is validated work/results per unit time; **latency** is time for one defined result.
- **time-to-solution** includes the stated initialization, computation, communication, I/O, and finalization window; **time-to-valid-solution** additionally requires output and convergence checks.
- A **scaling envelope** is the tested range of problem sizes, resource shapes, placements, configurations, and correctness conditions over which a claim holds.
- **surface-to-volume growth** describes communication becoming large relative to owned work as local subdomains shrink.
- **granularity** is useful work between coordination events; insufficient granularity exposes latency and overhead.
- **placement** maps ranks, threads, memory, NICs, and accelerators to hardware; **topology awareness** aligns communication with machine locality.
- A **scaling knee** is the region after which marginal resources yield too little benefit or raise cost/risk beyond policy.

### Central model, mechanism, or theorem

For a fixed validated problem, decompose `T_p` into useful compute, communication, synchronization/imbalance, memory, I/O, runtime, and measurement terms on the critical path. `S_p=T_b/T_p` and `E_p=S_p/(p/b)` describe observed strong scaling; they do not prove causality or future scale. Weak scaling compares a precisely defined per-resource workload and output-quality contract, usually against `T_b`, while also reporting total work and communication. A defensible claim retains input, code/toolchain, hardware allocation/topology, process/thread/device mapping, configuration, repetitions/distributions, region maxima, traffic/resource metrics, and result validation.

### Critical invariants

Compared runs solve the same declared problem for strong scaling or an explicitly scaled problem family for weak scaling; algorithms, convergence/stopping criteria, precision, output, and validation remain comparable; resource units and actual allocation are recorded; timing boundaries and clocks are consistent; initialization/warm-up/I/O inclusion is stated; per-rank maxima/distributions and full-job time are preserved; ranks/threads/devices are pinned intentionally; memory fits without unreported spill; network/filesystem contention and node health are observed; repetitions quantify variance; no failed or invalid run is silently omitted; and claims remain inside the measured scaling envelope.

### Common failures

Teams change problem size while calling a result strong scaling, change tolerance or algorithm at larger p, compare elapsed time from different boundaries, report the fastest trial, divide by requested rather than used resources, hide startup/I/O, use averages when the slowest rank controls completion, run fewer iterations because numerical order changed, oversubscribe CPUs or GPUs, ignore NUMA/NIC affinity, infer network cost from aggregate MPI time, benchmark cache-sized weak-scaling cases that are not equivalent, omit invalid outputs, extrapolate beyond measured nodes, or optimize a microbenchmark unrelated to the application bottleneck.

### Compact example

A fixed validated workload takes `[80,43,24,16]` seconds on `[1,2,4,8]` nodes. Speedups are `[1,1.8605,3.3333,5]`, efficiencies `[1,.9302,.8333,.625]`, and costs `[80,86,96,128]` node-seconds. Eight nodes are faster but consume 60% more node-time; whether that is desirable depends on deadline, allocation, energy, queue, and cost policy. These four points establish no result beyond their recorded environment and problem.

### Connections

[Load Imbalance Across Nodes](088-load-imbalance-across-nodes.md) separates stragglers from other tails. [Communication-Computation Overlap](086-communication-computation-overlap.md) identifies exposed versus hidden transfer. [Bulk-Synchronous and Asynchronous Iterations](089-bulk-synchronous-and-asynchronous-iterations.md) controls synchronization semantics. The [program roadmap](../ROADMAP.md) next formalizes upper bounds through Amdahl, Gustafson, and work-span models.

## Governing Question

For which problem family, result contract, resource unit, hardware placement, and measurement interval does adding nodes improve the objective—and which critical-path term becomes dominant at the next scale?

“It ran on 1,024 nodes” is a capacity statement. “It scales” requires comparable valid results, measured performance and resources across multiple points, uncertainty, causal diagnosis, and a bounded claim.

## Why This Matters

Multi-node execution introduces latency, finite bandwidth, collectives, network topology, partition boundaries, remote I/O, clock/trace issues, scheduler placement, and more opportunities for one rank or node to be late. Local work shrinks under strong scaling until fixed overhead or communication dominates. Under weak scaling, global communication, reductions, metadata, imbalance, and solver iteration count can still grow.

Scaling is also economic and operational. A run may finish 20% sooner using four times the nodes, delaying other jobs and raising energy or monetary cost. Conversely, a deadline may justify low efficiency. One large run can be impossible on fewer nodes because of memory. The correct objective may be ensemble throughput, turnaround including queue time, energy-to-solution, or deadline probability rather than raw kernel seconds.

Reliable scaling studies prevent costly folklore. They expose whether the next improvement belongs in decomposition, algorithm, collectives, data layout, affinity, progress, I/O, load balance, or measurement itself.

## Prerequisites and Retrieval

Retrieve:

- rank/communicator topology, message matching, collective order, and progress from [Processes and Ranks in Distributed-Memory Programs](081-processes-and-ranks-in-distributed-memory-programs.md), [Point-to-Point Message Passing](082-point-to-point-message-passing.md), and [Collective Communication](083-collective-communication.md);
- partition, halo, overlap, I/O, and imbalance metrics from [Domain Decomposition](084-domain-decomposition.md) through [Load Imbalance Across Nodes](088-load-imbalance-across-nodes.md); and
- reproducibility, floating reductions, random streams, and statistical comparison from [Reproducible Randomness in Parallel Programs](069-reproducible-randomness-in-parallel-programs.md) and [Parallel Loops and Reductions](044-parallel-loops-and-reductions.md).

Retrieval prompt: name the scientific/business workload and validity oracle; strong/weak/throughput objective; baseline and scale points; actual nodes/ranks/threads/devices/memory; host/node/socket/NUMA/core/NIC/GPU mapping; scheduler allocation; code/dependencies/compiler/MPI/runtime versions and flags; input/decomposition/iterations/tolerance/precision; timing window; phase/communication/I/O/resource instrumentation; repetitions and environment controls; expected bottleneck; acceptance threshold; and artifact/rollback policy.

## Learning Objectives

After completing this module, a learner can:

1. define strong, weak, throughput, memory-capacity, and ensemble scaling experiments precisely;
2. compute speedup, efficiency, cost, weak-scaling ratios, and uncertainty-aware comparisons;
3. preserve workload, algorithm, convergence, precision, and output validity across resource counts;
4. instrument critical-path computation, communication, synchronization, memory, I/O, and runtime costs;
5. diagnose granularity, surface-to-volume, collectives, imbalance, placement, topology, and system noise;
6. design rank/thread/device mappings for NUMA, NIC, and accelerator locality;
7. distinguish application, runtime, scheduler, network, and storage limits using controlled experiments;
8. select a scaling knee against deadline, throughput, resource, energy, and cost policies;
9. make bounded, reproducible scaling claims with complete provenance; and
10. scope security, operations, scientific, and high-stakes human review.

## Core Exposition

### Define the objective and problem family

Strong scaling fixes the global semantic workload: domain, resolution, observations, model, time horizon, samples, tolerance, precision, required outputs, and validity checks. If p changes floating order and convergence iterations, retain actual iteration count and final residual/error; do not silently cap work differently.

Weak scaling defines a family `W(p)`, often constant cells, particles, graph edges, samples, or requests per rank. That local count is insufficient when boundary area, graph degree, global reductions, nonlinear difficulty, dataset distribution, or I/O layout changes. Record total useful work and problem difficulty indicators. Validate outputs using a size-aware oracle.

Throughput scaling may run independent cases concurrently. Define completed valid cases per second and latency distribution, isolation, memory, I/O, and failure policy. Packing jobs can improve utilization even when one case cannot strong-scale. Memory scaling asks what problem becomes feasible, but must still report time, resource cost, and validity.

Choose the resource denominator. Nodes can differ; GPUs can have partitions; ranks can share cores; SMT threads are not cores. Report nodes, CPU sockets/cores/threads, ranks, GPUs/slices, memory, and allocation. If heterogeneous, a single p may be misleading; document capacity and compare like allocations or use an explicit weighted resource model.

### Measurement protocol

Build once per intended comparison unless build configuration is the experimental variable. Record source revision, dirty state, compiler and flags, libraries, MPI/runtime, container/module environment, input digest, and application configuration. Record scheduler job/partition/QoS, allocated nodes, node types, placement/binding, frequencies/power modes where available, network/filesystem, and relevant environment variables.

Define the clock interval. End-to-end usually begins after scheduler launch is outside application control but includes application initialization, data read, setup, iterations, required output, and finalization. Also instrument named regions. State whether one-time setup, JIT, cache warm-up, checkpoint, verification, and teardown are included. Use a monotonic clock for local durations; cross-rank timestamp correlation requires clock evidence. A maximum rank duration often governs a collective phase.

Run enough repetitions to expose variance and order points to reduce temporal bias—randomize or interleave scales when allocations permit. Retain all valid/invalid attempts and explain exclusions prospectively. Report median plus distribution/confidence interval and tails, not only best time. Warm-up must match production semantics and cannot erase real startup cost from an end-to-end claim.

Correctness is part of every measurement. Verify convergence, checksums/invariants, conservation, residual/backward error, statistical tolerance, or domain reference as applicable. Record NaN/Inf, warnings, retries, dropped work, missing output, and failure. Fast invalid runs do not count.

### Executable scaling summary

This deterministic Python calculation derives strong-scaling metrics for one exact dataset. It does not measure an application, model uncertainty, normalize heterogeneous nodes, or prove causality, portability, energy efficiency, or future scaling.

<!-- bijux-verify: {"id":"strong-scaling-metrics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"nodes=1 time_s=80 speedup=1.000000 efficiency=1.000000 cost_node_s=80\nnodes=2 time_s=43 speedup=1.860465 efficiency=0.930233 cost_node_s=86\nnodes=4 time_s=24 speedup=3.333333 efficiency=0.833333 cost_node_s=96\nnodes=8 time_s=16 speedup=5.000000 efficiency=0.625000 cost_node_s=128\nfastest_nodes=8\nfastest_time_s=16\nfastest_cost_increase_fraction=0.600000\n","stderr":""}} -->
```python
nodes = [1, 2, 4, 8]
times = [80, 43, 24, 16]
baseline_nodes = nodes[0]
baseline_time = times[0]

for count, elapsed in zip(nodes, times):
    speedup = baseline_time / elapsed
    efficiency = speedup / (count / baseline_nodes)
    cost = count * elapsed
    print(
        f"nodes={count} time_s={elapsed} speedup={speedup:.6f} "
        f"efficiency={efficiency:.6f} cost_node_s={cost}"
    )

fastest_index = times.index(min(times))
fastest_cost = nodes[fastest_index] * times[fastest_index]
baseline_cost = baseline_nodes * baseline_time
print(f"fastest_nodes={nodes[fastest_index]}")
print(f"fastest_time_s={times[fastest_index]}")
print(f"fastest_cost_increase_fraction={(fastest_cost / baseline_cost) - 1:.6f}")
```

### Decompose the critical path

For each iteration/phase, separate useful compute, packing/copy, point-to-point transfer/progress, collective communication, synchronization/arrival wait, memory stalls, accelerator kernels/transfers, I/O, runtime/scheduler overhead, and instrumentation. These terms overlap, so a simple sum can double-count; use traces/dependency reasoning for the critical path and profiles/counters for attribution.

Retain min/median/max and distributions across ranks/nodes. Aggregate “MPI time” may be waiting by early ranks for late compute, while compute regions may contain memory stalls. Pair call times with message counts/bytes, collective identities, arrival timestamps, hardware counters, and topology. Measure full job and per-region scaling: a shrinking compute phase can expose an unchanged setup or output phase.

Compute cost `p*T_p` reveals resource-time growth. For baseline b, relative overhead is `p*T_p/(b*T_b)-1`. It collects serial work, communication, imbalance, and other overhead without identifying them. Monetary and energy cost require actual rates/power measurements; node-seconds are not joules or currency.

### Strong-scaling limits

As p increases for fixed W, useful work per worker shrinks. Fixed launch/setup, latency, serial sections, reductions, and final I/O become a larger fraction. Messages often get smaller while counts or neighbors remain, reducing bandwidth efficiency. Local subdomain volume falls faster than boundary communication for common decompositions.

Granularity must exceed scheduling and communication costs. Overdecomposition can improve balance but adds metadata and boundaries. Aggregation reduces message count at latency cost. Communication avoidance or a different algorithm may beat tuning. Module 091 develops formal serial and work-span bounds; this module requires measurements before fitting them.

Memory can improve or regress. More nodes provide capacity and cache aggregate, sometimes superlinear-looking speedup when the baseline spills or has worse cache behavior. That is real for the tested hierarchy but must be explained, not called impossible or universal. Conversely, replicated metadata, buffers, communicators, and per-rank structures can grow until memory or initialization dominates.

Find the knee by marginal value: compare `T_p-T_q` with extra nodes, node-time, energy, queue/availability, and deadline risk. A fixed efficiency threshold is policy, not physics. Preserve all points so others can choose differently.

### Weak-scaling limits

Idealized weak scaling holds time constant as work/resources grow proportionally. Define weak efficiency, for example `Ew_p=T_b/T_p` when per-resource work and units are comparable. Also show total problem size, achieved work rate, iterations, communication, memory, and output. If the larger problem is harder or more accurate, elapsed time alone is ambiguous.

Nearest-neighbor communication can remain roughly constant per rank for carefully scaled local domains, while global reductions often grow with process count and topology. Network contention and bisection limits emerge. Graph/adaptive partitions can increase degree/cut or skew. Metadata services and parallel filesystems face larger client counts. Solver iteration counts can change with global size or preconditioner quality.

Weak scaling may change cache residency or per-node I/O distribution. Keep local geometry/data distribution comparable and disclose deviations. Validate the scaled family, not against the small output byte-for-byte.

### Placement and topology

Map ranks to cores, sockets, NUMA nodes, NICs, and GPUs intentionally. Verify actual binding rather than trusting requested flags. Match CPU threads to allocated cores and disable accidental oversubscription. First-touch or explicit NUMA allocation should align memory with compute; GPU ranks should use intended devices and NIC locality.

Use node-local shared-memory communicators/hierarchical algorithms when they preserve semantics and improve locality. Process topologies can express graph or Cartesian neighborhoods, but an MPI implementation is not required to produce the mapping you imagined. Record hostname/rank/core/NUMA/GPU/NIC mapping and inspect it.

Compare compact versus spread allocations, rank ordering, ranks per node, threads per rank, and collective/runtime algorithms through controlled experiments. A better result on one fabric topology is environment-specific. Do not encode undocumented runtime switches without version and fallback.

### Communication, collectives, and progress

For point-to-point phases record per-rank/per-peer message count, bytes, size distribution, post/completion, and exposed wait. For collectives record operation, communicator size, datatype/count, frequency, arrival skew, and duration. The same collective algorithm may cross thresholds as p or message size changes.

Nonblocking operations overlap only with independent work and actual progress. Assume MPI weak progress for portability; test polling/progress thread/offload and its CPU/NUMA effects. Complete requests and respect buffer lifetime. Persistent or neighborhood collectives may amortize setup for stable patterns, but benchmark representative iterations.

Congestion depends on concurrent traffic, mapping, topology, and other jobs. Microbenchmarks establish local latency/bandwidth context but cannot predict an application's pattern alone. Compare isolated repeated runs, application traces, and system telemetry where authorized.

### I/O, initialization, and finalization

At scale, directory/metadata operations, file-per-rank patterns, shared-file contention, data redistribution, compression skew, and close/sync can dominate. Measure input, preprocessing, checkpoint, required output, validation, and teardown separately and end to end. Parallel I/O correctness and layout remain primary.

Avoid excluding I/O because it looks bad unless the claim is explicitly compute-kernel scaling. A production time-to-solution claim includes required data movement. Cache effects require cold/warm labeling. Generate synthetic inputs only when they preserve application work and are clearly separated from production claims.

Initialization may contain rank-zero parsing/broadcast, mesh generation, communicator construction, library autotuning, JIT, or memory allocation. Optimize or amortize based on actual run length. Final reductions and serial output can set the floor.

### Diagnose regressions systematically

First reproduce correctness and provenance. Then locate the earliest scale/region where critical time stops shrinking. Ask whether useful work per rank changed, iteration count rose, max/mean widened, messages became smaller/more numerous, collective arrivals spread, memory bandwidth/cache/NUMA changed, progress disappeared, I/O clients grew, or one node was unhealthy.

Run controls: same p on different nodes; different rank/thread placement; data-to-node rotation; point-to-point/collective microbenchmarks; compute/memory kernels; I/O layout variants; instrumentation off/on; and repeated allocations. Change one primary variable per comparison. Correlation guides a hypothesis; a targeted perturbation and recovered performance strengthen causality.

Do not tune away correctness. Changing partition, collective reduction, solver, tolerance, precision, compression, or output is a new configuration requiring equivalence and possibly a separate scaling curve.

### Reproducibility and claim shape

A scaling report includes tables/plots of actual resources versus distribution of validated wall time, speedup/efficiency/cost, work/iterations, per-region maximum, traffic, memory, I/O, and result error. Include baselines and raw artifact identifiers. Axes begin appropriately and uncertainty is visible.

State: “For input I, revision R, configuration C, precision/tolerance V, on system H under allocations A, median validated time over n runs improved from X at b nodes to Y at p nodes; efficiency was E and node-time changed Z; bottleneck evidence indicates Q.” Do not say “linearly scalable” from two points or extrapolate.

Record unavailable counters, failed jobs, noisy co-tenancy, queue constraints, and source limitations. Rerun after hardware, runtime, compiler, algorithm, or input changes before carrying a claim forward.

### Security, operations, and high-stakes limits

Scaling traces can reveal topology, hostnames, workload sizes, traffic, sensitive region names, patient/customer density, or timing side channels. Minimize/redact identifiers, authorize counters, protect artifacts, and set retention. Validate scheduler parameters, paths, input sizes, and ranks to prevent resource exhaustion; bound per-rank buffers and output.

Operationally monitor placement, node/NIC/GPU health, phase maxima, arrival skew, traffic, memory, I/O, progress, failures/retries, output validation, energy where available, and budget. Define abort/checkpoint/restart and safe partial-output behavior. Ordinary faster completion does not prove reliability.

High-stakes studies require named domain, numerical, performance, infrastructure, security/privacy, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers. Scaling evidence cannot establish model validity, safety, fairness, or authorization.

## Definitions and Notation

- `p`, `b`: tested and baseline comparable resource counts.
- `W`: fixed global work for strong scaling; `W(p)`: declared weak-scaling family.
- `T_p`: chosen statistic of validated elapsed time at p, with distribution retained.
- `S_p=T_b/T_p`: speedup relative to baseline b.
- `E_p=S_p/(p/b)`: parallel efficiency relative to b.
- `C_p=p*T_p`: resource-time cost under homogeneous units.
- `Ew_p=T_b/T_p`: one stated weak-scaling efficiency when local work is comparable.
- `R_p=W(p)/T_p`: validated useful-work throughput.
- `T_comp`, `T_comm`, `T_sync`, `T_mem`, `T_io`, `T_runtime`: attributed terms; overlap/critical-path rules must be stated.
- `I=max_r T_r/mean_r T_r`: phase time imbalance indicator.
- `Obs`: result validity, performance, resource, environment, and provenance record.

Metrics describe the observed experiment; they are not an extrapolation theorem.

## Mechanisms, Invariants, or Proof Structure

### Comparability proof

Strong points share semantic input/work, algorithm, stopping, precision, required output, validity oracle, code/toolchain, and timing boundary. Weak points follow a declared size function with comparable local work and size-aware validity. Differences are explicit experimental variables.

### Resource and placement proof

Requested and actual nodes/cores/threads/ranks/devices/memory match; no accidental oversubscription; CPU/NUMA/GPU/NIC binding and host topology are recorded; heterogeneous capacity and system interference are disclosed.

### Measurement-validity proof

Monotonic timing, phase nesting, instrumentation overhead, repetitions/order, warm/cold policy, maxima/distributions, exclusions, and uncertainty are documented. Every timed point passes result/convergence checks, and invalid/failed runs remain visible.

### Causal diagnosis proof

Critical-path region/counter/traffic evidence identifies a hypothesis. Placement/data rotations, microbenchmarks, or one-variable perturbations distinguish application work, imbalance, hardware, network, runtime, and I/O explanations. Improvement after targeted change is revalidated end to end.

### Claim-boundary proof

The report names problem, revision/configuration, system/allocation, range, statistic/repetitions, metric values, correctness result, limitations, and non-extrapolation. Resource/energy/cost and time objectives remain distinct.

## Alternatives and Trade-Offs

| Study/objective | Reveals | Principal limitation |
|---|---|---|
| strong scaling | latency reduction for fixed work | granularity/fixed overhead dominate |
| weak scaling | capacity under proportional work | problem family may change difficulty |
| throughput/ensembles | valid results per time | individual latency can remain high |
| memory scaling | newly feasible problem sizes | not necessarily efficient |
| kernel microbenchmark | local mechanism ceiling | may not represent application |
| application phase profile | bottleneck attribution | instrumentation/overlap complexity |
| end-to-end study | operational outcome | less diagnostic alone |
| compact placement | locality, fewer links | contention within nodes/groups |
| spread placement | memory/bandwidth per rank | more network distance/resources |

Use complementary studies; no single curve answers correctness, cause, capacity, cost, and operational value.

## Failure Modes and Misconceptions

- **“More nodes means scaling.”** execution capacity is not speedup evidence.
- **“Changing N is strong scaling.”** strong scaling fixes the semantic workload.
- **“Constant cells per rank guarantees weak equivalence.”** boundaries, reductions, difficulty, and I/O can grow.
- **“Requested resources equal used resources.”** verify allocation and binding.
- **“Ranks are comparable resource units.”** oversubscription and heterogeneity break that assumption.
- **“Best time is representative.”** retain repetitions, variance, and exclusions.
- **“Average rank time controls completion.”** critical phases often follow the maximum.
- **“MPI time is network time.”** it can include arrival wait or progress behavior.
- **“Collectives synchronize identically.”** rely only on specified semantics.
- **“Efficiency below 100% is failure.”** deadlines/capacity may justify resource cost.
- **“Superlinear speedup is impossible.”** cache/memory/spill and baseline effects can explain it.
- **“Node-seconds equal energy or price.”** measure/rate them separately.
- **“Kernel scaling predicts application scaling.”** whole critical paths and I/O matter.
- **“Fewer solver iterations at p is free speed.”** validate numerical comparability.
- **“Warm cache is always cheating.”** label and match the operational workload.
- **“One machine's curve is portable.”** placement, topology, runtime, and versions matter.
- **“Two points establish linearity.”** retain multiple points and avoid extrapolation.
- **“Fast output is valid output.”** every point requires result validation.

## Worked Examples

### Example 1

**Strong scaling.** A fixed mesh/tolerance runs at 100, 56, and 34 seconds on 4, 8, and 16 nodes. Relative speedups are 1, 1.786, 2.941; efficiencies 1, .893, .735. **Conclusion:** state the non-one-node baseline.

### Example 2

**Invalid strong curve.** The 64-node run halves solver tolerance to finish. Put it on a separate algorithm/accuracy curve. **Conclusion:** preserve the result contract.

### Example 3

**Weak-scaling iteration growth.** Cells/rank stay fixed, but global solver iterations rise 40%. Report both time/iteration and time/valid-solution. **Conclusion:** local size does not fix problem difficulty.

### Example 4

**Arrival skew.** Average compute shrinks, but one rank hits an adaptive region and reaches all-reduce late. Per-rank traces, not aggregate MPI time, identify it. **Conclusion:** locate the critical producer.

### Example 5

**Placement regression.** Ranks use GPUs across the wrong NUMA/NIC path. Correct binding restores transfer overlap. **Conclusion:** verify physical mapping.

### Example 6

**Message granularity.** Halo bytes fall with local domains, but message count stays fixed and latency dominates. Aggregation or a different decomposition is tested. **Conclusion:** bandwidth alone is incomplete.

### Example 7

**Superlinear point.** The one-node baseline spills beyond memory while four nodes fit. Report memory high-water and paging; do not generalize cache benefit. **Conclusion:** explain the hierarchy transition.

### Example 8

**I/O wall.** Compute scales to 256 nodes, while file-per-rank metadata makes finalization slower. Collective layout and fewer files improve end-to-end time. **Conclusion:** required I/O belongs in time-to-solution.

### Example 9

**Economic knee.** Moving from 64 to 128 nodes saves two minutes but adds 40% node-time and misses budget policy; 64 is chosen absent a harder deadline. **Conclusion:** optimize the declared objective.

### Example 10

**Coastal flood ensemble.** Scaling must preserve terrain/bathymetry/mesh/weather/tide/structure/time/unit/model/scenario/partition versions, conservation and numerical tolerances, uncertainty/ensemble completeness, sensor provenance, privacy for population/mobility data, deadline/missing-member/failure behavior, restart/audit, and publication gates. Named coastal-hydrology/oceanography/meteorology, civil/emergency-management, geospatial, numerical/HPC/performance, privacy/security, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers must approve evidence; none is claimed here. **Conclusion:** faster multi-node execution does not establish a valid forecast or safe evacuation decision.

## Cross-Program Connections

- **Algorithms:** work, span, partitioning, communication lower bounds, and granularity predict pressure points.
- **Architecture:** cache, bandwidth, NUMA, accelerators, NIC locality, and power shape node performance.
- **Operating systems/schedulers:** allocation, binding, noise, topology, and queue policy shape experiments.
- **Networks:** latency, bandwidth, topology, bisection, congestion, and collectives limit scale.
- **Storage/data engineering:** parallel I/O, metadata, partition layout, and checkpointing enter end-to-end time.
- **Numerical computing:** conditioning, solver iterations, precision, residual, and reduction order preserve comparability.
- **Statistics:** repetitions, randomization, uncertainty, censoring, and outliers support honest comparisons.
- **Testing:** reference results, metamorphic invariants, fault injection, and provenance make performance valid.
- **Security/privacy:** traces and topology require minimization/access control; inputs and resources require bounds.
- **Operations/economics:** deadline, throughput, allocation, energy, price, recovery, and budget determine the knee.

## References

1. MPI Forum, *MPI: A Message-Passing Interface Standard, Version 5.0*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report.pdf>
2. MPI Forum, *MPI-5.0: Processes*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node48.htm>
3. MPI Forum, *MPI-5.0: Progress*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node50.htm>
4. MPI Forum, *MPI-5.0: Collective Communication Introduction*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node116.htm>
5. MPI Forum, *MPI-5.0: Process Topologies*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node209.htm>
6. Lawrence Livermore National Laboratory, *Caliper: A Performance Analysis Toolbox in a Library*, 2.15 documentation; retrieved 2026-08-29. <https://software.llnl.gov/Caliper/>
7. Lawrence Livermore National Laboratory, *Caliper Basics: Runtime Reports and Rank Statistics*, current documentation; retrieved 2026-08-29. <https://software.llnl.gov/Caliper/CaliperBasics.html>
8. Lawrence Livermore National Laboratory, *Caliper MPI Profiling*, current documentation; retrieved 2026-08-29. <https://software.llnl.gov/Caliper/MPIProfiling.html>
9. HPCG Project, *High Performance Conjugate Gradients Benchmark Overview*. <https://www.hpcg-benchmark.org/downloads/sc14/HPCG-Overview.pdf>
10. Open MPI Project, *Process Placement, Process Affinity, and Binding*, current documentation; retrieved 2026-08-29. <https://docs.open-mpi.org/en/main/tuning-apps/affinity.html>

## Exercises

### Exercise 1

For validated times 120, 68, 40, and 30 seconds at 2, 4, 8, and 16 nodes, compute speedup, efficiency, and node-second cost relative to two nodes. Identify the fastest and lowest-cost points without choosing policy for the reader.

### Exercise 2

Design strong- and weak-scaling studies for a distributed 3D stencil. Fix semantic workload, scaled family, validity, timing, placement, communication, I/O, repetitions, and claimed envelope.

### Exercise 3

A curve regresses only beyond four nodes. Give a controlled diagnostic sequence that distinguishes insufficient granularity, imbalance, NUMA/NIC placement, collectives/progress, network contention, and I/O.

### Exercise 4

Define a selection policy among 32, 64, and 128 nodes for a nightly ensemble with latency deadline, throughput, node-hour, energy, queue, and failure objectives. State required evidence and tie/rollback rules.

### Exercise 5

Transfer the framework to a multi-hospital genomic outbreak pipeline. Specify workload/validity, weak and throughput scaling, privacy/security, clinical/data, failure/restart, resource, publication, and named reviewer invariants without claiming review.

## Answers to the Exercises

### Answer 1

With b=2 and `T_b=120`: at 2 nodes, `S=1`, `E=1`, cost 240; at 4, `S=120/68≈1.764706`, `E≈.882353`, cost 272; at 8, `S=3`, `E=.75`, cost 320; at 16, `S=4`, `E=.5`, cost 480 node-seconds. Sixteen nodes minimize measured elapsed time; two minimize node-second cost. Deadline, queue, energy, monetary rates, uncertainty, and capacity can change the chosen point.

### Answer 2

Strong scaling fixes global grid, time steps, boundary conditions, precision, update/solver method, tolerance, required checkpoints/output, and conservation/reference oracle; test several actual node counts with verified rank/thread/NUMA/NIC binding. Weak scaling fixes local 3D dimensions per rank and defines global geometry growth, boundary conditions, time horizon and size-aware conservation/reference checks; record changing surface, global reductions and iterations. For both retain revision/toolchains/input/config, full and phase timing, rank maxima/distributions, halo messages/bytes, collective arrivals, memory/counters, I/O, output error, all repetitions/failures, and environment. Interleave/repeat points where possible and state that claims cover only tested grids, node shapes, placement, system, and tolerance.

### Answer 3

First revalidate output/config and locate the first nonshrinking critical region with per-rank maxima/traces. Compute useful work/rank and message size/count; a fixed latency term with balanced arrivals supports insufficient granularity. Compare max/mean work and rotate data/node mappings for imbalance. Verify binding and test ranks/threads per node plus local versus remote NUMA/GPU/NIC placement. Record collective operation/count/arrival/progress; test polling or supported progress configuration without changing semantics. Repeat on different allocations/times and run authorized point-to-point/collective controls for network contention. Separate input/checkpoint/output/metadata and test governed layouts. Change one variable at a time, require the predicted metric and end-to-end validated time to recover, and treat correlation as provisional.

### Answer 4

For each point retain distributions of valid ensemble completion and member latency, completed members/hour, node-hours, measured energy, queue/start behavior, failures/retries, memory/I/O/network, and result equality/tolerance under representative nights. Reject points whose confidence-bound deadline probability, validity, capacity, privacy, or recovery SLO fails. Among survivors apply explicit weighted or lexicographic policy—e.g. meet deadline and validity first, then minimize expected node-hour/energy subject to throughput. Use uncertainty margins and workload-season strata; ties choose the lower-resource/simpler point. Roll back when output validation, deadline tail, failure rate, budget, energy, or placement envelope breaches sustained thresholds.

### Answer 5

Define a deidentified specimen/site/run/reference/database/pipeline/toolchain/consent epoch, read-quality and coverage work, variant/lineage outputs, clinical interpretation boundary, and independent truth/reference plus reproducibility checks. Weak scaling fixes authorized samples/work per site while reporting genome/read distribution and database/aggregation growth; throughput scaling measures complete valid cases with latency tails. Record actual compute/accelerator/memory/network/storage placement, resource cost, iterations, failures, all exclusions, and time-to-validated-result. Enforce least privilege, consent/purpose/locality, encryption/authentication, pseudonymous IDs, minimum cohorts, bounded/redacted telemetry, retention/audit, and no cross-site raw-data leakage. Version references/models, validate schema/units/provenance/deduplication, checkpoint idempotently, fail closed on missing/stale sites or partial aggregation, and gate publication. Named infectious-disease/genomics, clinical microbiology/epidemiology, bioinformatics/biostatistics, privacy/security, distributed/HPC/data, operations, data-governance, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers are required. No external review, clinical validity, privacy guarantee, approval, or deployment authorization is claimed.
