---
module_id: CONPAR-050
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 50
title: Measuring Speedup, Efficiency, and Scalability
status: complete
last_verified: 2026-08-29
---

# Measuring Speedup, Efficiency, and Scalability

## One-Page Review

### Governing question

How can engineers make reproducible, correctness-preserving claims about parallel speedup, efficiency, and scalability while separating mathematical bounds from measured hardware and workload behavior?

### Essential definitions

- **Baseline time** `T_1(n)` is elapsed time for a declared correct reference implementation/configuration on problem size `n`.
- **Parallel time** `T_P(n)` is elapsed time with `P` declared processing resources under otherwise controlled conditions.
- **Speedup** is `S_P(n)=T_1(n)/T_P(n)`.
- **Parallel efficiency** is `E_P(n)=S_P(n)/P` only when the resource count and capacity are meaningfully comparable.
- **Strong scaling** increases `P` while holding the total problem fixed.
- **Weak scaling** increases problem size with `P` while holding a declared work/load quantity per resource approximately fixed.
- **Work** `T_1` is total operations/time in an abstract computation model; **span** `T_infinity` is its critical-path length.
- **Cost** is `P*T_P`; a parallel algorithm is cost-optimal relative to a baseline when this remains asymptotically comparable to useful sequential work.
- **Isoefficiency** describes how problem size must grow with `P` to maintain a target efficiency under an overhead model.
- **Superlinear speedup** means measured `S_P>P`; it requires explanation such as cache/regime change, baseline defect, pruning, or noise.

### Central model, mechanism, or theorem

Amdahl's fixed-work model with serial fraction `f` and perfectly parallel remainder gives `S_P<=1/(f+(1-f)/P)`, so the ideal limit is `1/f` for `f>0`. Gustafson's scaled-work model answers a different question: if parallel elapsed time is normalized and workload grows with `P`, scaled speedup is `P-f(P-1)` under its assumptions. Work/span scheduling gives the lower bound `T_P>=max(T_1/P,T_infinity)` and idealized upper bounds for specific schedulers. These models diagnose assumptions; measurements establish behavior on declared systems.

### Critical invariants

Baseline and parallel runs compute equivalent outputs under one semantic oracle and comparable accuracy. Timed boundaries include the same necessary work or explicitly report exclusions. Problem size, data distribution, seeds, code/build, dependencies, hardware, topology, placement, frequency/power policy, and workload state are recorded. `P` counts the relevant comparable capacity, not an ambiguous mix of threads and devices. Warm-up, trials, order, outliers, and uncertainty are declared. Strong and weak curves are never mixed. Failures, retries, dropped work, approximation, batching, and preprocessing remain visible. Raw observations are retained.

### Common failures

Engineers compare optimized parallel code to an unoptimized serial version; omit process startup or data transfer only from the parallel path; time different outputs or accuracy; benchmark tiny work below clock resolution; take the best of many parallel runs against one baseline; ignore warm-up, turbo, thermal throttling, affinity, NUMA, and other tenants; divide by logical threads as if all were independent cores; call throughput gain latency speedup; treat Amdahl's fraction as immutable; claim weak scaling while changing algorithm or bytes per worker; or publish a superlinear result without investigating cache and baseline regimes.

### Compact example

With normalized baseline 100 and modeled serial work 10, ideal times for `P=1,2,4,8,16` are `100,55,32.5,21.25,15.625`. Speedups are `1,1.818,3.077,4.706,6.4`; efficiencies are `1,0.909,0.769,0.588,0.4`; the asymptotic limit is 10. These are exact values of a model with zero overhead and a fixed fraction, not benchmark predictions.

### Connections

[Work Partitioning and Granularity](045-work-partitioning-and-granularity.md) determines useful work per task. [Load Balance and Scheduling Overheads](046-load-balance-and-scheduling-overheads.md) supplies causal overhead categories. [Work Stealing](047-work-stealing.md) scopes work/span bounds. [Pipeline Parallelism](048-pipeline-parallelism.md) separates latency and throughput.

## Governing Question

How should an engineer design, execute, analyze, and communicate parallel performance experiments so every speedup or scalability claim is mathematically coherent, empirically reproducible, and semantically fair?

A ratio is easy to compute; a trustworthy ratio requires a complete comparison contract.

## Why This Matters

Parallel systems can reduce time, increase throughput, solve larger problems, or meet deadlines. Those are different goals. A fourfold throughput increase may coexist with worse item latency. A weak-scaling curve may look flat while total resource cost grows linearly. A GPU kernel may run 100 times faster while transfers and preprocessing leave the application only twice as fast.

Performance is also an experimental science. Scheduler noise, dynamic frequency, cache state, runtime compilation, garbage collection, allocator state, network contention, and thermal limits alter results. Selecting one favorable run can manufacture a claim. Yet excessive statistical ceremony cannot repair an unfair baseline or wrong output.

Mathematical models provide counterfactual structure: what if a fraction were perfectly parallel, what if work grew with resources, what if span were the only dependency limit? They reveal ceilings and overhead, but their parameters are workload- and implementation-dependent. Amdahl's law does not measure `f`; Gustafson's law does not promise that larger problems are useful; work/span does not include every hardware cost automatically.

## Prerequisites and Retrieval

Retrieve:

- concurrency versus parallelism from [Concurrency, Parallelism, and Asynchrony](001-concurrency-parallelism-and-asynchrony.md);
- dependency graphs from [Task Parallelism and Dependency Graphs](041-task-parallelism-and-dependency-graphs.md);
- work/span structure from [Fork-Join Computation](043-fork-join-computation.md);
- reduction correctness from [Parallel Loops and Reductions](044-parallel-loops-and-reductions.md);
- grain from [Work Partitioning and Granularity](045-work-partitioning-and-granularity.md);
- overhead classification from [Load Balance and Scheduling Overheads](046-load-balance-and-scheduling-overheads.md); and
- pipeline metrics from [Pipeline Parallelism](048-pipeline-parallelism.md).

Retrieval prompt: for one parallel benchmark, state the exact semantic oracle, baseline, timed boundary, problem size/distribution, resource definition, and whether the experiment is strong or weak scaling.

## Learning Objectives

After completing this module, a learner can:

1. compute and interpret time, throughput, speedup, efficiency, cost, and overhead;
2. distinguish fixed-work, scaled-work, strong-scaling, and weak-scaling questions;
3. derive and scope Amdahl, Gustafson, and work/span relationships;
4. identify fair baselines and equivalent timed boundaries;
5. design controlled trials with warm-up, randomization, replication, and uncertainty;
6. diagnose efficiency loss through serial work, imbalance, communication, contention, and resource saturation;
7. interpret superlinear and negative speedup without sensational claims;
8. compare heterogeneous resources using workload outcomes rather than naive processor counts;
9. retain reproducible raw evidence and machine-readable experiment metadata; and
10. reject performance claims that sacrifice correctness, accuracy, reliability, or safety.

## Core Exposition

### Define the outcome before the stopwatch

Performance begins with a semantic contract. State input domain, output, accuracy/tolerance, error behavior, ordering, determinism, and resource constraints. A parallel approximation that drops difficult inputs is not faster at the same task. A reduction with different floating order may be acceptable within a declared tolerance but not bitwise identical.

Choose the metric matching value. Batch elapsed time and makespan answer “when is the set done?” Item latency answers “how long did one request wait?” Throughput answers “how many terminal outcomes per time?” Time-to-solution includes required setup and communication. Energy-to-solution, cost, peak memory, and resource-hours can matter more than time.

Declare the timed boundary. End-to-end often includes input acquisition, parsing, allocation, data transfer, computation, output materialization, synchronization, and cleanup. Kernel-only measurement is useful for mechanism analysis if labeled. Compare like with like and provide both when transfers/setup materially affect decisions.

### Baseline selection

`T_1` is not necessarily the parallel program forced to one worker. That configuration may retain queueing, synchronization, partition, and runtime overhead. It is useful for scaling the implementation, while a best practical sequential algorithm is useful for algorithmic speedup. Report both when they answer different questions.

Optimize baselines comparably. Use the same language/toolchain opportunities, algorithmic quality, data format, precision, and I/O boundary. Do not compare a vectorized GPU implementation against intentionally scalar naive code and call all gain parallelism. Decompose algorithmic, compiler/vector, batching, cache/layout, and parallel effects where possible.

Correctness precedes timing. Run an oracle outside or within the timed boundary consistently. If checking is excluded, verify every measured configuration's results and report the check cost separately. Stable hashes can catch corruption but need canonical outputs and do not establish domain validity alone.

### Speedup, efficiency, cost, and overhead

For fixed problem `n`, `S_P=T_1/T_P`. If `T_1=20s` and `T_4=6s`, speedup is `3.33`. Efficiency `E_4=3.33/4=0.833` under comparable four-resource capacity. Parallel cost is `C_P=P*T_P=24` resource-seconds versus 20 sequential. Overhead relative to sequential work is `O_P=P*T_P-T_1=4` resource-seconds.

Overhead aggregates serial sections, imbalance, communication, synchronization, scheduling, redundant/speculative work, cache/coherence, memory/network contention, idle search, and measurement effects. `O_P` says extra cost exists, not its cause. Use timelines, counters, and controlled variants to classify it.

Efficiency can mislead on simultaneous multithreading, asymmetric cores, GPUs, clusters, or elastic services. A “processor” may not have equal capacity. Report actual resource composition, occupancy/utilization, energy/cost, and outcome curves rather than forcing one efficiency denominator.

### Amdahl's fixed-work model

Normalize baseline work/time to one. Suppose fraction `f` remains serial and `1-f` parallelizes perfectly over `P`. Ideal time is `f+(1-f)/P`, so

`S_P=1/(f+(1-f)/P)`.

For `f=0.1`, infinite-resource limit is 10. At `P=8`, speedup is `1/(0.1+0.9/8)=4.706`. This is not “90% CPU utilization.” It is a two-part idealized decomposition relative to a particular baseline/problem.

Real parallelization can change both work and serial portion. Initialization may grow with `P`; parallel algorithms may use extra operations; a faster parallel representation may improve the nominally serial part; cache may change. Use Amdahl to explore sensitivity and explain a plateau, not to declare a universal constant from one profile.

The serial fraction inferred from measurements can include all nonideal effects. The Karp–Flatt-style effective serial fraction for `P>1` is `e=(1/S_P-1/P)/(1-1/P)`. If `e` grows with `P`, communication/contention/imbalance likely increases; it is not proof of source-code serialization.

### Gustafson's scaled-work model

Fixed-work scaling eventually offers too little work per processor. Some scientific and analytic workloads use more resources to solve larger/higher-resolution problems in about the same elapsed time. Normalize the parallel run to one, with observed serial fraction `f` and parallel portion `1-f`. The equivalent scaled single-resource work is `f+P(1-f)`, giving scaled speedup

`S_G=P-f(P-1)`.

This answers “how much larger useful work fits in a fixed parallel time?” It does not contradict Amdahl because the workload changes. The scaling rule must be meaningful: grid resolution, samples, simulated years, users, or records per worker. Growing an irrelevant loop solely to inflate speedup is not weak-scaling value.

Scaled work can change memory hierarchy, convergence, communication surface, numerical error, or algorithm. State which properties remain equivalent and which intentionally scale.

### Work, span, and parallelism

For a computation DAG, `T_1` is total work and `T_infinity` its longest dependency path. Any `P`-processor execution satisfies

`T_P>=T_1/P` and `T_P>=T_infinity`,

so `T_P>=max(T_1/P,T_infinity)`. Average parallelism is `T_1/T_infinity`, an upper-scale indicator under the model. Brent-style bounds show that a DAG schedule can often achieve time on the order of `T_1/P+T_infinity`; specific runtime guarantees require their assumptions.

Work/span reveals parallelism unavailable because of dependencies, while Amdahl represents a serial fraction of a fixed decomposition. Neither automatically models memory bandwidth, cache, communication, OS preemption, runtime overhead, or heterogeneous processing. Measured span tools also have instrumentation and cost models.

### Strong scaling

Strong scaling holds problem size and semantics fixed while increasing resources. Record `T_P`, `S_P`, `E_P`, cost, memory, energy, and correctness for a resource series such as `1,2,4,8,...`. A curve often improves, then flattens, then worsens as work per resource shrinks and overhead/resource contention dominates.

The fixed input must truly be fixed: same records, mesh, random seed policy, precision, iterations/convergence condition, and output. If parallel execution changes convergence order, compare the same stopping criterion and solution tolerance, and report iteration counts.

Use resource placement deliberately. One socket versus two changes NUMA and bandwidth. Logical CPUs differ from physical cores. Node counts change network topology and per-node memory. A scaling curve with these regime boundaries should annotate them rather than fit one smooth story.

### Weak scaling and isoefficiency

Weak scaling keeps a declared load per resource approximately fixed: e.g., cells per process or requests per worker, while total load grows with `P`. Weak-scaling efficiency may be expressed as `T_1(n_1)/T_P(n_P)` when `n_P/P=n_1`, but only with comparable per-unit work and outputs. Ideally time remains constant; communication and global coordination often grow.

Not every algorithm has constant per-item work as size grows. Graph density, solver iterations, cache misses, and global reductions can change. State input distributions and algorithmic complexity. A flat time obtained by reducing accuracy or dropping work violates the contract.

Isoefficiency asks how `n` must grow with `P` so useful work dominates overhead enough to maintain target efficiency. Derivation begins with an explicit overhead function `O(n,P)=P*T_P(n)-T_1(n)`. It is model-specific; empirical curves can estimate rather than prove it.

### Saturation and rooflines

Scaling stops when a shared resource saturates. CPU-bound work can exhaust execution capacity; memory-bound work reaches bandwidth; synchronization hits a contended line; I/O reaches storage; distributed shuffle reaches network. More workers increase queueing and interference without increasing useful rate.

Arithmetic intensity—operations per byte moved—helps reason about compute versus memory bounds. A roofline-style upper bound is the minimum of peak compute and bandwidth times intensity, under its measurement/model. Real kernels also face latency, cache, instruction mix, occupancy, and access patterns.

Measure relevant counters but avoid reverse causality. High bandwidth near a known sustainable benchmark plus flat operation rate supports a bandwidth hypothesis. One counter snapshot alone does not prove it. Use algorithm/layout variants or placement controls.

### Experimental design

Freeze or record code commit, build mode and flags, compiler/runtime/libraries, OS/kernel, firmware, hardware model, core/socket/NUMA/GPU topology, memory, storage/network, power/frequency governor, container/resource limits, affinity, and other load. Record input version/generator and seeds.

Warm up runtime compilation, caches, pools, and steady state when representative; also measure cold behavior if production is cold. Randomize or counterbalance configuration order so thermal drift and background load do not always favor one configuration. Use separate process trials when state leakage matters.

Take enough independent observations to show distribution and uncertainty. Median and quantiles resist some outliers but do not excuse deleting inconvenient runs. Means are useful for additive expectations with confidence intervals under appropriate sampling. Predeclare exclusion rules, retain raw data, and inspect multimodality. Autocorrelated request samples are not independent replicates.

Do not blindly subtract empty-loop overhead from small values; subtraction can amplify error and create negative times. Increase work per sample, batch repeated operations carefully, and ensure batching does not change cache/algorithm behavior. Use monotonic high-resolution clocks and synchronize completion.

### Throughput and latency experiments

Closed-loop load generators wait for responses and can hide overload by reducing offered load as latency rises. Open-loop arrivals better test queueing under a declared rate but require accurate scheduling and dropped-arrival accounting. Coordinated omission can omit precisely the long waits of interest.

Report offered, admitted, completed, failed, timed-out, and shed rates separately. Throughput achieved by rejecting more requests is not equivalent service. Measure latency percentiles over the correct population and interval, including queue time. Saturation curves plot throughput and latency across offered load and resource counts.

For pipelines, distinguish first-item latency, steady completion interval, batch makespan, and drain. For async I/O, concurrency may raise throughput without CPU parallelism. For distributed jobs, successful task percentage can conceal a hot final partition.

### Superlinear and negative speedup

`S_P>P` is possible as a measurement. Aggregate caches may fit a working set that thrashes in the baseline; partitioning may reduce algorithmic search/pruning work; more memory may prevent spilling; frequency or library paths may differ. It may also reflect a slow/unoptimized baseline, error, noise, or different output.

Reproduce across trials and sizes. Compare per-resource work and hardware counters, a cache-sized baseline, optimized sequential implementation, and fixed-frequency/placement controls. Label the cause supported by evidence. Superlinear result is not a violation of mathematics because the simple equal-work equal-resource assumptions changed.

Negative speedup (`T_P>T_1`) is valuable. It locates grain too small, overhead, contention, false sharing, serialization, imbalance, or resource mismatch. The correct result may be to keep the sequential path below a measured threshold.

### Heterogeneous and economic scaling

Comparing a CPU core count with GPU “cores” is rarely meaningful. Compare time-to-correct-solution, throughput at service level, energy, cost, memory, and accuracy on fully specified systems. Include host-device transfer and preprocessing according to the intended boundary.

Cloud instances vary through shared tenancy, turbo, storage/network credits, placement, and pricing. Repeat across instances/times and record allocation. Cost speedup is `cost_baseline/cost_parallel` for equivalent output, not time speedup. A faster run using 16 times the resource may be economically worse.

Reliability changes effective performance. If large parallel jobs fail more often, expected time/cost includes retries and checkpoint recovery. Report successful-run timing and operational expected outcome separately.

### Evidence and communication

Retain machine-readable raw trials, environment manifest, input checksums, commands, stdout/stderr, correctness results, and analysis code under governed artifacts. Tables should include absolute times alongside ratios; ratios alone hide tiny/noisy baselines. Graph axes, units, error displays, and resource/topology transitions must be explicit.

State what the evidence supports: “median end-to-end time fell from X to Y on system Z for input I” is stronger and narrower than “scales linearly.” Give uncertainty and trial count. Report failed configurations and limits. Separate measured claims, model projections, and hypotheses.

Reproduction on another system is valuable; external peer review is a named human process and cannot be inferred from passing automation. High-stakes latency/safety claims require domain, real-time, systems, and regulatory evidence beyond benchmarks.

## Definitions and Notation

For problem size `n`, baseline time `T_1(n)` and `P`-resource time `T_P(n)` yield speedup `S_P(n)=T_1(n)/T_P(n)` and, for comparable resources, efficiency `E_P(n)=S_P(n)/P`. Cost is `C_P=P*T_P`; overhead relative to the baseline is `O_P=C_P-T_1`.

Amdahl ideal speedup is `1/(f+(1-f)/P)`. Gustafson scaled speedup is `P-f(P-1)` under normalized scaled-run assumptions. Effective serial fraction is `e=(1/S_P-1/P)/(1-1/P)` for `P>1`.

For a computation DAG, work `T_1`, span `T_infinity`, and average parallelism `T_1/T_infinity` imply `T_P>=max(T_1/P,T_infinity)`. These use abstract compatible cost units.

Strong scaling holds `n` fixed. Weak scaling chooses `n_P` by a declared rule such as `n_P/P=n_1`. Throughput is terminal successful work per time; latency is elapsed time per item over a declared boundary and population.

## Mechanisms, Invariants, or Proof Structure

Audit a parallel performance claim in this order:

1. define semantic equivalence, accuracy, terminal outcomes, and a correctness oracle;
2. choose value metric and identical or explicitly decomposed timed boundaries;
3. select optimized baseline(s) and distinguish implementation from algorithmic speedup;
4. state fixed/scaled workload, input distribution, seeds, and convergence rules;
5. define `P`, topology, placement, build/runtime, resource limits, and system state;
6. derive relevant Amdahl, Gustafson, work/span, capacity, or overhead hypotheses with assumptions;
7. predeclare warm-up, trial independence/order, sample size, exclusions, and uncertainty analysis;
8. collect absolute times, outputs, raw trials, resource counters, failures, retries, and costs;
9. diagnose serial work, imbalance, communication, contention, saturation, and regime transitions causally;
10. investigate negative or superlinear results rather than filtering them;
11. reproduce across sizes/configurations and retain commands/environment/raw evidence; and
12. communicate measured findings separately from model projections and deployment claims.

The executable model computes ideal Amdahl times, speedups, and efficiencies for a fixed 10% serial fraction.

<!-- bijux-verify: {"id":"amdahl-speedup-table","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"serial_fraction=0.10\nworkers=[1, 2, 4, 8, 16]\nideal_times=[100.0, 55.0, 32.5, 21.25, 15.625]\nspeedups=[1.0, 1.818, 3.077, 4.706, 6.4]\nefficiencies=[1.0, 0.909, 0.769, 0.588, 0.4]\nasymptotic_limit=10.0\ntime_decreases=True\nefficiency_nonincreasing=True\n","stderr":""}} -->
```python
baseline = 100.0
serial_fraction = 0.10
workers = [1, 2, 4, 8, 16]
ideal_times = []
speedups = []
efficiencies = []

for count in workers:
    elapsed = baseline * (serial_fraction + (1 - serial_fraction) / count)
    speedup = baseline / elapsed
    ideal_times.append(elapsed)
    speedups.append(speedup)
    efficiencies.append(speedup / count)

print(f"serial_fraction={serial_fraction:.2f}")
print(f"workers={workers}")
print(f"ideal_times={[round(value, 3) for value in ideal_times]}")
print(f"speedups={[round(value, 3) for value in speedups]}")
print(f"efficiencies={[round(value, 3) for value in efficiencies]}")
print(f"asymptotic_limit={1 / serial_fraction:.1f}")
print(f"time_decreases={all(ideal_times[i] < ideal_times[i - 1] for i in range(1, len(ideal_times)))}")
print(f"efficiency_nonincreasing={all(efficiencies[i] <= efficiencies[i - 1] for i in range(1, len(efficiencies)))}")
```

Limitations: this arithmetic model assumes fixed total work, fixed 10% serial fraction, perfectly divisible remainder, identical resources, zero communication/scheduling/contention, stable frequency, no failures, and exact comparable output. It validates formula calculations, not a hardware benchmark or scalability prediction.

## Alternatives and Trade-Offs

- **Kernel benchmark:** isolates one mechanism and supports optimization; may omit application-dominant transfers/setup.
- **End-to-end benchmark:** supports operational decisions; causal diagnosis is harder.
- **Implementation baseline at `P=1`:** isolates scaling overhead of one design; may be weaker than best sequential code.
- **Best sequential baseline:** supports algorithmic speedup; requires comparably optimized semantics.
- **Strong scaling:** reveals fixed-work latency limits; efficiency declines when work per resource shrinks.
- **Weak scaling:** tests growing capacity; changes total problem and resource cost.
- **Elapsed time:** direct time-to-solution; omits energy/cost and service quality.
- **Throughput:** useful for services/streams; can hide worse latency, drops, or approximation.
- **Median:** robust summary for skewed noise; does not describe tails/multimodality alone.
- **Mean:** supports expected additive cost; sensitive to outliers and sampling dependence.
- **Fixed placement/frequency:** improves control; may differ from production policies.
- **Production-like dynamism:** improves ecological relevance; requires more repetitions and metadata.
- **Homogeneous efficiency:** intuitive for equal processors; inappropriate for heterogeneous device “core” counts.

## Failure Modes and Misconceptions

1. **“Speedup is parallel time divided by serial time.”** It is the inverse: `T_1/T_P`.
2. **“Efficiency below one proves bad code.”** Fixed-work efficiency usually falls; value depends on time, cost, and goal.
3. **“Amdahl predicts measured performance.”** It is an ideal scoped model whose fraction must be justified.
4. **“Gustafson refutes Amdahl.”** It asks a scaled-work rather than fixed-work question.
5. **“Weak scaling means any larger input.”** Per-resource work and semantic scaling rule must be declared.
6. **“Best-of-N is representative.”** It selectively reports favorable noise unless explicitly analyzing a lower bound.
7. **“More samples repair an unfair baseline.”** Statistics cannot fix different algorithms, outputs, or boundaries.
8. **“All cores are equivalent.”** SMT, asymmetric CPUs, GPUs, NUMA, and throttling violate naive counts.
9. **“Superlinear speedup is impossible.”** It signals changed cache/work/regime or experimental defect requiring explanation.
10. **“Faster means production-ready.”** correctness, tails, failures, cost, energy, and safety remain required.

## Worked Examples

### Example 1

For baseline 120 seconds and `P=8` time 30 seconds, speedup is 4, efficiency 0.5, cost 240 resource-seconds, and overhead 120 relative resource-seconds. The job is faster but consumes twice the baseline resource-time. Whether that is acceptable depends on deadline and economic/energy goals.

### Example 2

With `f=0.05`, Amdahl ideal speedups at 16 and infinite resources are `1/(.05+.95/16)=9.143` and 20. If measured speedup is six, the gap includes communication, imbalance, extra work, contention, or a wrong fraction. The law alone cannot identify which.

### Example 3

A weak-scaling mesh keeps one million cells per process while increasing processes from one to 64. Elapsed time rises from 10 to 14 seconds, giving weak efficiency about 0.714 under that definition. If solver iterations also rise due to a larger physical domain, report that change; it is algorithmic scaling, not pure communication overhead.

### Example 4

A GPU kernel is 50 times faster than CPU compute, but host-device transfers and conversion make end-to-end times 100 and 20 ms. Application speedup is five. Both numbers are valid at different boundaries; reporting only 50 would mislead the deployment decision.

### Example 5

A four-thread result shows 5.2 speedup. Validation finds the partitioned data fits aggregate caches while the serial run spills beyond cache. Repeat a cache-blocked optimized serial baseline and measure misses/bytes. The superlinear observation is real for the original configurations but is attributed to cache regime, not “more than perfect parallelism.”

### Example 6

Twenty trials are run in configuration blocks: all serial first, then all parallel. Machine temperature rises, lowering parallel frequency. Randomizing/counterbalancing trial order and recording frequency/temperature reveals the bias. Independent process trials reset runtime state; raw distributions remain available.

### Example 7

An HTTP benchmark doubles throughput by rejecting 30% of requests. Offered, admitted, successful, rejected, timed-out rates and latency population expose the semantic change. It is not a twofold equivalent-service speedup. A fair comparison holds success policy and service-level output constant.

### Example 8

A fork-join DAG has work 1,000 units and span 80. On eight processors, any schedule takes at least `max(125,80)=125` abstract units, so ideal speedup cannot exceed eight from work and 12.5 from span; work bound dominates at eight. This ignores hardware costs and does not promise the lower bound is achievable.

### Example 9

A reproducible suite records commit, compiler flags, CPU/NUMA topology, governor, affinity, input checksum, command, warm-up, randomized trial order, absolute raw times, output digest/tolerance, counters, failures, and analysis version. A plot links to the raw table and marks crossing from one to two sockets.

### Example 10

An emergency weather model finishes before deadline on average at 512 nodes. Deployment still requires named numerical-weather, meteorology, HPC, reliability, real-time, infrastructure, cybersecurity, emergency-management, human-factors, quality, independent verification, and regulatory reviewers; model/data provenance and uncertainty; forecast-skill validation; worst-case timing/resource analysis; correlated-failure, network/storage, checkpoint/recovery, saturation, and degraded-mode tests; redundant authoritative workflows; operator drills; and signed residual-risk acceptance. Average speedup is not public-warning authorization.

## Cross-Program Connections

- **Algorithms:** work, span, asymptotics, approximation, and data distributions determine useful scaling.
- **Statistics:** sampling, uncertainty, experiment order, outliers, autocorrelation, and effect sizes govern evidence.
- **Computer architecture:** caches, bandwidth, vector units, SMT, NUMA, accelerators, and power limit curves.
- **Operating systems:** affinity, preemption, frequency policy, page placement, I/O, and isolation create variance.
- **Distributed systems:** network topology, stragglers, failures, retries, checkpoints, and consistency affect elapsed work.
- **Programming languages:** runtimes, garbage collection, JIT, compilation, synchronization, and semantics alter comparisons.
- **Data systems:** throughput, tail latency, query plans, skew, and admission define workload outcomes.
- **Economics/sustainability:** instance cost, resource-hours, energy, carbon, and opportunity cost qualify speedup.
- **Formal methods:** semantic equivalence and invariant checks prevent benchmarks from optimizing the wrong result.
- **Safety engineering:** worst-case deadlines and independently reviewed hazards exceed average performance evidence.

## References

1. G. M. Amdahl. “Validity of the Single Processor Approach to Achieving Large-Scale Computing Capabilities.” AFIPS, 1967. <https://doi.org/10.1145/1465482.1465560>.
2. J. L. Gustafson. “Reevaluating Amdahl's Law.” Communications of the ACM 31(5), 1988. <https://doi.org/10.1145/42411.42415>.
3. R. P. Brent. “The Parallel Evaluation of General Arithmetic Expressions.” Journal of the ACM 21(2), 1974. <https://doi.org/10.1145/321812.321815>.
4. R. D. Blumofe and C. E. Leiserson. “Scheduling Multithreaded Computations by Work Stealing.” Journal of the ACM 46(5), 1999. <https://doi.org/10.1145/324133.324234>.
5. S. Williams, A. Waterman, and D. Patterson. “Roofline: An Insightful Visual Performance Model for Multicore Architectures.” Communications of the ACM 52(4), 2009. <https://doi.org/10.1145/1498765.1498785>.
6. Lawrence Livermore National Laboratory. “Introduction to Parallel Computing Tutorial.” <https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-computing-tutorial>.
7. SPEC. “CPU 2017 Run and Reporting Rules.” <https://www.spec.org/cpu2017/Docs/runrules.html>.
8. Google. “Benchmark User Guide.” <https://google.github.io/benchmark/user_guide.html>.
9. OpenJDK. “Java Microbenchmark Harness.” <https://github.com/openjdk/jmh>.
10. Python Project. “pyperf Documentation.” <https://pyperf.readthedocs.io/en/latest/>.

## Exercises

### Exercise 1

For `T_1=80s` and measured `T_8=14s`, compute speedup, efficiency, cost, overhead, and effective serial fraction. Explain what the fraction does and does not prove.

### Exercise 2

With modeled serial fraction `f=0.08`, compute Amdahl speedup at `P=16` and the infinite limit; compute Gustafson scaled speedup at `P=16`. Reconcile the different values.

### Exercise 3

Design strong- and weak-scaling experiments for a stencil solver, including semantic equivalence, topology, convergence, raw trials, uncertainty, and resource counters.

### Exercise 4

A GPU implementation reports 80-fold kernel speedup and 6-fold application speedup. Define experiments that attribute transfer, batching, algorithm, precision, cache, and measurement effects without weakening correctness.

### Exercise 5

An aircraft collision-avoidance computation meets mean latency and shows strong scaling. Explain why this is insufficient for deployment and enumerate required human evidence.

## Answers to the Exercises

### Answer 1

`S_8=80/14=5.714`; `E_8=5.714/8=0.714`; cost is `8*14=112` resource-seconds; overhead is `112-80=32`. Effective serial fraction is `(1/5.714-1/8)/(1-1/8)=(0.175-0.125)/0.875≈0.0571`. It summarizes deviation from ideal scaling at eight under the formula; it may include serial work, imbalance, communication, contention, extra work, topology, or measurement error and does not prove 5.71% of source code is inherently serial.

### Answer 2

Amdahl at 16 is `1/(.08+.92/16)=1/.1375≈7.273`; its infinite limit is `12.5`. Gustafson is `16-.08(15)=14.8`. Amdahl holds fixed total work and asks how its time falls; Gustafson holds normalized parallel time while useful parallel work grows with processors. They describe different workload-scaling counterfactuals and are consistent when assumptions and normalization are explicit.

### Answer 3

Strong scaling fixes mesh/domain, boundary conditions, precision, input, stopping tolerance, and output-error oracle while sweeping placements from cores to sockets/nodes. Weak scaling keeps declared cells per rank and scales the physical/numerical problem meaningfully, recording changed iteration/convergence behavior. For both, pin topology/affinity, record build/runtime/hardware/network, randomize trial order, warm up deliberately, run independent repetitions, retain raw times and confidence/quantile summaries, and verify every output. Measure compute, halo communication, global reductions, imbalance, memory bandwidth/cache misses, network, energy/cost, failures, and checkpoint time; annotate topology transitions.

### Answer 4

Use identical inputs, algorithms or explicitly separated algorithm variants, precision/tolerance, output oracle, and end-to-end boundaries. Measure CPU reference, GPU compute-only, transfers/conversion, and complete application with synchronized completion. Sweep batch and input sizes using matched batching controls; compare cold/warm data; record CPU/GPU utilization, bandwidth, cache, allocation, launch, transfer, and energy. Include an optimized vectorized CPU baseline and fixed precision. Randomize repeated trials and retain raw evidence. Attribute 80-fold only to the kernel boundary and sixfold to application outcome; do not subtract required transfers or accept lower accuracy silently.

### Answer 5

Mean latency and scaling omit worst-case deadlines, rare encounter geometries, sensor/model validity, numeric error, hardware faults, schedule variance, overload, cybersecurity, degraded modes, and pilot/controller interaction. Require named aviation surveillance/navigation, collision-avoidance, control, real-time, hardware, software-safety, cybersecurity, human-factors, operations, quality, independent verification, certification, and regulatory reviewers; requirements/hazard traceability; validated operating domain/data/model; deterministic/tolerance and worst-case execution/resource analysis; simulation, hardware-in-the-loop, adversarial geometry, saturation, fault-injection, failover, recovery, environmental, interoperability, and flight-test evidence; independent protective logic; operator training; and signed residual-risk acceptance. This answer is not flight authorization.
