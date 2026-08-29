---
module_id: CONPAR-091
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 91
title: Amdahl, Gustafson, and Work-Span Models
status: complete
last_verified: 2026-08-29
---

# Amdahl, Gustafson, and Work-Span Models

## One-Page Review

### Governing question

Which performance model matches the question being asked—fixed-work latency, scaled-work capacity, or dependency-limited scheduling—and how can its assumptions be tested without mistaking a fitted fraction for a law of the implementation?

### Essential definitions

- **work** `T1` is the total execution time/operations of a computation on one ideal processor in the work-span model.
- **span** `Tinf` is the longest dependency-path time, equivalently ideal time with unbounded processors under the model.
- **parallelism** is `T1/Tinf`, an upper bound on useful average processor count in the dependency DAG.
- **fixed-work speedup** compares the same work on different processor counts.
- The **serial fraction** f in the elementary Amdahl model is the normalized part that receives no speedup under its assumptions.
- **Amdahl speedup** is `S_A(p)=1/(f+(1-f)/p)` for fixed work, ideal division of the parallel part, and zero added overhead.
- **scaled speedup** compares a scaled workload completed in a reference time; if s is its serial-time fraction on p processors, **Gustafson scaled speedup** is `S_G(p)=p-s(p-1)`.
- A **dependency DAG** represents operations as weighted vertices/edges and precedence constraints as directed edges.
- **Brent's scheduling bound** gives a finite-processor schedule within work/p plus span terms under its abstract assumptions.
- **slackness** compares available parallelism with processors; low slackness makes scheduling/imbalance more damaging.
- **overhead** includes communication, synchronization, scheduling, extra work, memory, I/O, and contention introduced or exposed by parallel execution.
- **Karp-Flatt-like inference** estimates an effective serial/overhead fraction from observed speedup; it is diagnostic, not a literal code fraction.

### Central model, mechanism, or theorem

Amdahl asks how fixed work accelerates when fraction f remains serial: `T_p/T_1=f+(1-f)/p`, so `S_p<=1/f` as p grows. Gustafson asks how much serial-equivalent work is accomplished when elapsed time is normalized at p processors and serial fraction s occupies that parallel run: `S_G=s+p(1-s)=p-s(p-1)`. Work/span ignores a single fraction and uses dependencies: every schedule satisfies `T_p>=max(T1/p,Tinf)`, while greedy/Brent-style scheduling supplies an upper bound of work/p plus span-scale overhead under the stated model. These answer different workload and structure questions; real communication, memory, I/O, scheduling, imbalance, and changing algorithms must be measured separately.

### Critical invariants

The modeled workload, result, algorithm, precision, stopping rule, and timing boundary are explicit; processor/resource units are comparable; serial and parallel fractions are measured for the same reference execution; f and s are not substituted across fixed/scaled contexts; work counts useful plus declared extra work consistently; the DAG contains all correctness dependencies and weighted costs; span is the longest legal dependency path rather than the longest measured rank; lower and upper bounds retain their directions; overhead is not hidden inside “serial code” without labeling; predictions are checked against validated measurements and uncertainty; and claims remain within observed problem/resource regimes.

### Common failures

Teams call every overhead “serial fraction,” derive f from one noisy point, use Amdahl on a growing workload, present Gustafson as refuting fixed-work bounds, assume p processors divide parallel time perfectly, confuse span with critical observed rank, omit communication/memory/I/O from work, count task creation but not execution dependencies, quote `T1/p+Tinf` as exact time, apply work-stealing bounds outside fully strict/randomized/model assumptions, claim superlinear measurements violate lower bounds despite cache/work differences, optimize a tiny fraction based on percentage alone, or extrapolate fitted models beyond validated scale.

### Compact example

With f=.1, ideal Amdahl speedup at p=8 is `1/(.1+.9/8)=4.705882`, efficiency .588235, and infinite-p limit 10. With scaled serial fraction s=.1 at p=8, Gustafson speedup is `8-.1*7=7.3`; it describes a larger parallel workload, not the same fixed job. For a DAG with `T1=80` and `Tinf=12`, every 8-processor schedule takes at least `max(10,12)=12`, so speedup cannot exceed `80/12=6.6667` in that model.

### Connections

[Scaling a Parallel Program Across Multiple Nodes](090-scaling-a-parallel-program-across-multiple-nodes.md) supplies validated measurements. [Parallel Loops and Reductions](044-parallel-loops-and-reductions.md) creates DAG structure. [Work Stealing](047-work-stealing.md) implements a scheduler with conditional bounds. The [program roadmap](../ROADMAP.md) next combines compute ceilings with data-movement ceilings through roofline analysis.

## Governing Question

Is the engineering decision about accelerating one fixed result, solving a proportionally larger problem within a time budget, or scheduling a particular dependency graph—and what observed costs violate the ideal model before its bound becomes actionable?

Models are lenses. A correct formula with the wrong workload definition yields a precise but irrelevant answer.

## Why This Matters

Parallel performance discussions often collapse three constraints into one “serial percentage.” Fixed work is limited by nonaccelerated time and overhead. Scaled problems may use more processors productively by increasing parallel work. Even with no textually serial region, dependencies impose a span. Meanwhile real systems add communication, scheduling, memory, imbalance, and extra work that vary with p.

These models guide investment. Amdahl can show that optimizing an already-parallel kernel cannot rescue fixed latency dominated elsewhere. Gustafson can justify larger resolution or ensembles when the useful workload legitimately grows. Work/span identifies dependency edges or task granularity worth redesigning. Each can also mislead if fractions are treated as constants, measurements are invalid, or algorithm changes are hidden.

Graduate-level practice derives bounds, maps code to assumptions, performs sensitivity analysis, and tests predictions against complete valid runs rather than worshiping a curve.

## Prerequisites and Retrieval

Retrieve:

- strong/weak workload definitions, speedup/efficiency/cost, measurement provenance, and validity from [Scaling a Parallel Program Across Multiple Nodes](090-scaling-a-parallel-program-across-multiple-nodes.md);
- DAGs, task granularity, scheduling, stealing, reductions, and imbalance from [Task Parallelism and Dependency Graphs](041-task-parallelism-and-dependency-graphs.md), [Work Stealing](047-work-stealing.md), and [Load Imbalance Across Nodes](088-load-imbalance-across-nodes.md); and
- critical paths, synchronization, overlap, and asynchronous semantics from [Communication-Computation Overlap](086-communication-computation-overlap.md) and [Bulk-Synchronous and Asynchronous Iterations](089-bulk-synchronous-and-asynchronous-iterations.md).

Retrieval prompt: state the decision; fixed or scaled workload; semantic work/result/oracle; baseline and p; timing boundary; region times and extra work; dependency DAG and weights; T1 and Tinf definition; communication/memory/I/O/scheduling/imbalance; algorithm/tolerance/precision changes; repetitions/uncertainty; target deadline/cost; model assumptions; sensitivity range; and empirical validation plan.

## Learning Objectives

After completing this module, a learner can:

1. derive and interpret Amdahl fixed-work speedup and its limit;
2. derive Gustafson scaled speedup without claiming it overturns fixed-work reasoning;
3. compute work, span, parallelism, lower bounds, and Brent-style upper bounds for DAGs;
4. distinguish model serial fraction, scaled serial fraction, dependency span, and observed overhead;
5. infer and cautiously interpret an effective serial/overhead fraction from measurements;
6. analyze sensitivity to fractions, processor count, overhead growth, and problem size;
7. map tasks, dependencies, granularity, communication, and scheduling to model terms;
8. test predictions against validated scaling data and diagnose residuals;
9. select an optimization using absolute critical-path benefit rather than percentages alone; and
10. scope scientific, security, operations, and high-stakes review.

## Core Exposition

### Amdahl's fixed-work model

Normalize the best comparable one-processor time to 1. Let f be time that receives no speedup and `1-f` be perfectly divisible across p identical processors. Then

`T_p=f+(1-f)/p`, and `S_A(p)=1/T_p`.

As `p->infinity`, the second term vanishes and `S_A->1/f` for f>0. Efficiency `S_A/p` declines as the nonaccelerated term dominates. The derivation is algebra, not an empirical assertion that f is constant or identifiable as particular source lines.

Use f for the same work and timing boundary. It can represent unavoidable sequential dependencies in the ideal model, but observed effective f also absorbs overhead, imbalance, and resource effects. Initialization excluded from T1 cannot appear honestly in Tp. If algorithms differ, the comparison needs a broader work/result model.

Sensitivity matters. Reducing f from .1 to .05 doubles the asymptotic ceiling from 10 to 20; reducing .001 to .0005 doubles 1,000 to 2,000, but other overhead will likely dominate first. Optimize absolute time and the targeted p, not the dramatic asymptote.

Add overhead explicitly: `T_p=fT_1+(1-f)T_1/p+O(p,N)`. O may include messages, collectives, scheduling, extra/redundant work, contention, memory, I/O, and imbalance and may overlap other terms. Once O is added, the elementary closed form no longer predicts without measuring/modeling O.

### Gustafson's scaled-work model

Normalize elapsed time on p processors to 1. Let s be the fraction spent in the serial part during that parallel run; parallel time is `1-s`. The serial-equivalent work is s for the serial portion plus `p(1-s)` for work performed concurrently, giving

`S_G(p)=s+p(1-s)=p-s(p-1)`.

This answers: how much one-processor-equivalent work was completed in the fixed parallel elapsed time, assuming the parallel portion scales with p and costs map ideally. It does not predict fixed-job latency. Amdahl and Gustafson use different normalization/workload assumptions and can both be true.

Scaled work must be useful. Increasing samples, grid resolution, domain, search space, requests, or ensemble members is legitimate if it improves the declared result/capacity objective and remains validated. Repeating irrelevant arithmetic is not scaling. Global difficulty may change iteration counts; memory, communication, and I/O may not scale ideally; report them.

The serial fraction s can change with p and N. Do not measure it once and extrapolate. Use the same parallel run boundary and separate overhead. A rank-zero bottleneck that grows with input is not constant serial work.

### Work and span

Represent a computation by a weighted acyclic dependency graph. Work `T1` is the sum of vertex costs under the model. Span `Tinf` is the maximum weight of a directed path. On p processors,

`T_p >= T1/p` because p processors cannot perform more than p units per time, and `T_p >= Tinf` because dependencies on a path serialize. Therefore `T_p>=max(T1/p,Tinf)` and `S_p<=min(p,T1/Tinf)`.

Parallelism `T1/Tinf` describes average capacity along an ideal schedule, not guaranteed speedup. If p greatly exceeds parallelism, span dominates. If parallelism greatly exceeds p, there is slack for a scheduler to absorb imbalance. But locality, communication, task overhead, and finite resources are absent unless included in weights/edges.

Brent's lemma/scheduling principle shows that a computation with work and depth can be scheduled on p processors in roughly `T1/p+Tinf` time (the exact form depends on the model, such as `Tinf+(T1-Tinf)/p` in a step simulation). Together with the lower bound, this is within a constant factor in the abstract model. It is an existence/greedy-scheduling result, not a promise that any runtime attains exact equality.

### Executable comparison

This deterministic Python model computes exact formulas for one parameter set. It does not fit real data, build a DAG, include overhead, prove scheduler assumptions, or predict hardware performance.

<!-- bijux-verify: {"id":"parallel-performance-models","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"processors=8\namdahl_serial_fraction=0.100000\namdahl_speedup=4.705882\namdahl_efficiency=0.588235\namdahl_infinite_limit=10.000000\ngustafson_serial_fraction=0.100000\ngustafson_scaled_speedup=7.300000\nwork=80\nspan=12\nparallelism=6.666667\nwork_span_lower_bound=12.000000\nwork_span_speedup_ceiling=6.666667\nbrent_upper_bound=20.500000\n","stderr":""}} -->
```python
p = 8
serial_fraction = 0.1
amdahl_speedup = 1 / (serial_fraction + (1 - serial_fraction) / p)
gustafson_speedup = p - serial_fraction * (p - 1)
work = 80
span = 12
lower_bound = max(work / p, span)
brent_upper_bound = span + (work - span) / p

print(f"processors={p}")
print(f"amdahl_serial_fraction={serial_fraction:.6f}")
print(f"amdahl_speedup={amdahl_speedup:.6f}")
print(f"amdahl_efficiency={amdahl_speedup / p:.6f}")
print(f"amdahl_infinite_limit={1 / serial_fraction:.6f}")
print(f"gustafson_serial_fraction={serial_fraction:.6f}")
print(f"gustafson_scaled_speedup={gustafson_speedup:.6f}")
print(f"work={work}")
print(f"span={span}")
print(f"parallelism={work / span:.6f}")
print(f"work_span_lower_bound={lower_bound:.6f}")
print(f"work_span_speedup_ceiling={work / lower_bound:.6f}")
print(f"brent_upper_bound={brent_upper_bound:.6f}")
```

### Build and analyze a DAG

Choose vertex granularity carefully. Vertices may be instructions, tasks, kernels, messages, or phases. Too coarse a DAG hides internal parallelism; too fine a DAG ignores task creation/scheduling and communication. Weight vertices using an abstract unit for theory or validated cost distributions for prediction, and state which.

Edges include data, control, resource/ordering, reduction, message, and synchronization dependencies required for correctness. Do not add accidental implementation serialization to the algorithmic DAG unless analyzing the implementation; do not omit a mutex, queue, collective, memory-capacity, or device-stream constraint when predicting it.

Compute T1 by summing each required vertex once. Compute Tinf by dynamic programming in topological order: longest predecessor distance plus vertex weight. A measured critical path can include scheduling and resource stalls not in the logical DAG. Compare them to find missing model costs.

Transformations reduce work, span, or overhead differently. Parallelizing a serial vertex reduces span but may add work. Tree reductions reduce linear span to logarithmic depth under associativity/numeric policy. Tiling can increase locality while adding dependencies. Speculation can reduce span on likely paths but adds work and rollback. Task coarsening reduces scheduler overhead but may lengthen span or imbalance.

### Work stealing and conditional bounds

Blumofe and Leiserson analyze randomized work stealing for fully strict multithreaded computations, obtaining expected time of the form `T1/P+O(Tinf)` plus stated space/communication results under their model. “Expected,” “fully strict,” randomized victim selection, cost assumptions, and computation structure matter.

Real runtimes add deque operations, unsuccessful steals, NUMA movement, cache misses, priority, blocking I/O, oversubscription, nested pools, memory limits, and external synchronization. Measure steal attempts/success, ready-task counts, task sizes, idle time, locality, span proxy, and critical path. Do not cite the theorem for arbitrary futures, cyclic graphs, blocking tasks, or distributed messages without a mapping proof.

Slackness `T1/(p*Tinf)` above one suggests enough average parallelism; near/below one indicates span pressure. It does not guarantee ready work at every moment or locality. Profile parallelism over time, not just the average.

### Relate fractions to DAGs

An Amdahl f is not generally `Tinf/T1`. If a DAG has span fraction `Tinf/T1`, its ideal speedup is bounded by parallelism, but Amdahl assumes a serial portion plus perfectly divisible remainder and yields a particular curve. Different DAG shapes with identical work/span can schedule differently on finite p; communication and resource constraints differ.

Likewise, source lines are not fractions. A short lock/collective on the critical path can dominate, while much sequential initialization off the timed path does not. Dynamic inputs and scheduling change time shares. Profile the critical path and dependency structure.

Fractions are ratios, so optimizing one part changes all percentages. Use absolute time deltas. If region A is 20% and sped up 2x, total ideal time becomes .9 and total speedup 1.111..., assuming no overhead/interaction. Re-measure after transformation.

### Infer effective overhead cautiously

From observed fixed-work speedup S at p under the elementary Amdahl form, solve

`f_eff=(1/S-1/p)/(1-1/p)` for p>1.

This effective fraction includes serial work and any overhead expressed in normalized time. If it grows with p, communication/imbalance/resource effects likely grow; it does not identify code causally. Measurement noise can make it negative under superlinear/cache effects or otherwise nonsensical. Report uncertainty and reject literal interpretation.

Fit multiple points only after preserving comparability. Inspect residuals rather than forcing a law. Add candidate terms—log p collective latency, bytes/bandwidth, surface terms, task overhead, imbalance—based on mechanisms, not curve convenience. Validate on held-out scale points; avoid extrapolation.

### Optimization decisions

For fixed latency at target p, compute maximum possible total benefit from eliminating a region using its critical-path contribution and interaction. A 1% region cannot yield more than about 1.01x if it alone is eliminated under fixed conditions; a span vertex may unblock parallel work and have broader effect, requiring DAG analysis.

Compare options: reduce work (better algorithm/vectorization), reduce span (parallelize dependency/tree), reduce overhead (coarsen/aggregate/avoid synchronization), increase useful scaled work, improve balance/locality, or choose fewer resources. Include engineering, verification, portability, memory, numeric, and operations costs.

Performance models guide hypotheses. The decision is made by validated measurements at relevant p/N and by the actual objective—latency, throughput, capacity, energy, cost, or deadline probability.

### Empirical validation

Use the scaling protocol from module 090. Retain valid T1 or baseline and Tp distributions, work/problem size, iteration count, algorithm, precision/tolerance, result oracle, allocation/placement, region maxima, task/DAG metrics, messages/bytes, memory/I/O, scheduler/steal data, and failures.

For fixed work compare observed speedup with Amdahl and work/span bounds. A lower-bound violation means inconsistent measurement/model: changed work, faster single-core algorithm, cache/spill, heterogeneous units, timing boundary, or error. For scaled work verify useful-result growth and compare serial/parallel time plus overhead.

Perturb the predicted limiter. Reduce a serial critical section, restructure a dependency chain, coarsen tasks, alter p, or remove a communication round while preserving correctness. If the target metric and complete time respond as predicted across repetitions, confidence grows. Still bound the claim.

### Security, operations, and high-stakes limits

Task graphs, traces, serial fractions, and workload sizes may expose algorithms, topology, tenants, patient/customer distributions, or sensitive control phases. Minimize labels, authorize instrumentation, protect artifacts, and retain only needed data. Bound DAG/task creation, recursion, queues, and speculative work to resist exhaustion.

Operational models include failure/retry/checkpoint and degraded resources. A theoretical speedup bound does not promise deadline reliability. Monitor phase/critical-path time, ready parallelism, steals, overhead, memory, progress, failures, validity, and drift from predicted envelope; define fallback/rollback.

High-stakes optimization requires named domain, numerical, performance, safety, security/privacy, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers. A smaller modeled span or serial fraction does not establish scientific validity or safe deployment.

## Definitions and Notation

- `p`: comparable processors/resources; `N`: problem-size descriptor.
- `f`: elementary fixed-work Amdahl nonaccelerated fraction, `0<=f<=1`.
- `s`: scaled-run serial-time fraction, `0<=s<=1`.
- `S_A(p)=1/(f+(1-f)/p)`: ideal fixed-work speedup.
- `S_G(p)=p-s(p-1)`: ideal scaled-work speedup.
- `G=(V,E)`: weighted acyclic computation graph.
- `T1`: work, sum of modeled operation costs.
- `Tinf`: span, maximum dependency-path cost.
- `T_p`: p-processor completion time in the stated model/measurement.
- `T1/Tinf`: average parallelism.
- `T_p>=max(T1/p,Tinf)`: work/span lower bound.
- `O(p,N)`: explicitly defined overhead, not generic unexplained residual.
- `f_eff=(1/S-1/p)/(1-1/p)`: effective Amdahl-form inference for p>1.

Fractions, work, span, and elapsed measurements are meaningful only with their workload, cost model, and boundary.

## Mechanisms, Invariants, or Proof Structure

### Amdahl derivation proof

Normalize identical fixed work to T1; partition into fT1 unaccelerated and `(1-f)T1` ideally divided by p; add and divide T1 by Tp. Check f=0, f=1, p=1, and p approaching infinity. Add measured overhead separately.

### Gustafson derivation proof

Normalize the p-processor elapsed scaled run to `s+(1-s)=1`; map parallel work to p times its elapsed share and serial work to s; sum. Check p=1, s=0, s=1, and useful scaled-work equivalence.

### Work/span bound proof

Total capacity gives `p*T_p>=T1`; every dependency path requires at least its sum, so `T_p>=Tinf`. A step-by-step greedy simulation schedules at most p ready operations and charges full rounds to work and incomplete rounds to progress along a critical path, yielding a work/p plus span upper form under the abstract assumptions.

### Implementation-mapping proof

Map code/tasks/messages/synchronization to vertices, edges, weights, scheduler assumptions, and resource constraints. Preserve semantic work/result and include extra work/overhead. Validate DAG critical structure against traces and runtime metrics.

### Empirical-bound proof

Every measurement passes provenance/result checks and retains uncertainty. Compare observed data to conditional predictions; investigate violations as assumption/model mismatches; perturb the proposed limiter; validate held-out points; and bound the claim.

## Alternatives and Trade-Offs

| Model | Best question | Principal limitation |
|---|---|---|
| elementary Amdahl | fixed-work ideal speedup sensitivity | f/overhead may vary with p |
| Gustafson scaled speedup | useful scaled work in fixed parallel time | not fixed-job latency |
| work/span DAG | dependency-limited parallelism | omits unmodeled resources/communication |
| Brent/greedy bound | schedulability with finite p | abstract conditional upper bound |
| work-stealing theorem | expected strict-task scheduling | structure/random/runtime assumptions |
| effective serial fraction | summarize measured overhead trend | not causal code fraction |
| empirical scaling curve | observed system/application outcome | bounded to tested envelope |
| mechanistic cost model | diagnose communication/memory/etc. | more parameters and validation |

Use multiple models when the decision spans ideal structure and actual systems.

## Failure Modes and Misconceptions

- **“Amdahl says parallelism is pointless.”** it bounds a declared fixed workload under assumptions.
- **“Gustafson disproves Amdahl.”** it asks a scaled-work question.
- **“f is the percentage of sequential source code.”** it is a time/model fraction.
- **“f is constant.”** algorithms, N, p, and overhead change it.
- **“All nonideal time is serial code.”** communication, imbalance, memory, and extra work differ.
- **“p divides the parallel part perfectly.”** elementary Amdahl assumes it.
- **“Span is the slowest rank.”** span is a dependency-path property.
- **“Work is the measured one-core time in every model.”** weights/model/hardware must be stated.
- **“Parallelism guarantees speedup.”** scheduler/locality/overhead can prevent it.
- **“T1/p+Tinf is exact runtime.”** it is a bound form under assumptions.
- **“Any work-stealing runtime gets the theorem.”** strictness and scheduler/cost assumptions matter.
- **“More tasks always reduce span.”** overhead/dependencies can grow.
- **“Superlinear data violates theory.”** changed memory/work/resource assumptions explain it.
- **“A fitted effective f identifies the bottleneck.”** it summarizes, not diagnoses.
- **“Two points estimate a universal law.”** retain uncertainty and held-out validation.
- **“Largest percentage deserves optimization.”** use absolute critical-path benefit and cost.
- **“Scaled work is automatically useful.”** result value and validity must be stated.
- **“A mathematical ceiling proves safety.”** domain and operational validation remain separate.

## Worked Examples

### Example 1

**Amdahl boundary.** With f=.25 and p=4, speedup is `1/(.25+.75/4)=16/7≈2.286`; limit is 4. **Conclusion:** fixed nonaccelerated work bounds latency.

### Example 2

**Gustafson scaling.** With s=.05 at p=32, scaled speedup is `32-.05*31=30.45`. **Conclusion:** name the larger useful workload.

### Example 3

**DAG bound.** Work 200, span 25, p=10 gives lower time at least 25 and speedup at most 8, not 10. **Conclusion:** dependencies can dominate capacity.

### Example 4

**Low slackness.** Work/span=16 on 16 workers leaves little scheduling slack; one delayed ready task exposes span. **Conclusion:** average parallelism equal to p is fragile.

### Example 5

**Tree reduction.** Replacing a legal linear association chain with a balanced tree reduces abstract span, but floating result/order changes require policy. **Conclusion:** dependency transformations include numerical review.

### Example 6

**Task coarsening.** Combining tiny tasks lowers scheduler work but lengthens the longest indivisible task. Measure overhead and span. **Conclusion:** granularity trades work against parallelism.

### Example 7

**Effective fraction drift.** Inferred f rises with p. A trace reveals collective arrival skew, not added serial source. **Conclusion:** inference is diagnostic, not causal.

### Example 8

**Useful scaled work.** More nodes increase ensemble members within one hour and reduce uncertainty under a predefined estimator. **Conclusion:** validate value, not operation count.

### Example 9

**Model residual.** Predicted speedup exceeds observation; adding measured bytes/bandwidth and imbalance explains held-out points. **Conclusion:** extend models by mechanisms.

### Example 10

**Seismic early-warning inversion.** Work/span optimization must preserve sensor/event/waveform/station/time/coordinate/unit/calibration/model/mesh/solver/partition epochs, conditioning/residual/uncertainty, missing/corrupt sensor and deadline behavior, authenticated provenance, restart/audit, false-alarm/missed-event evaluation, and alert gates. Named seismology/geophysics, emergency-management, numerical/inverse-problems, parallel/performance, safety/human-factors, security/privacy, operations, quality/regulatory, accessibility/ethics, and independent validation reviewers must approve evidence; none is claimed here. **Conclusion:** a better theoretical speedup does not validate an earthquake alert.

## Cross-Program Connections

- **Algorithms:** DAGs, lower bounds, greedy scheduling, reductions, and approximation define work/span.
- **Architecture:** vector width, caches, memory, accelerators, and contention change operation weights.
- **Operating systems/runtimes:** scheduling, stealing, blocking, priorities, and oversubscription realize or violate models.
- **Distributed systems/networks:** communication edges, latency, bandwidth, failure, and consistency add constraints.
- **Numerical computing:** associativity, conditioning, tolerance, precision, and extra iterations preserve semantic work.
- **Performance engineering:** profiles, traces, scaling curves, residuals, and perturbations test hypotheses.
- **Statistics:** uncertainty, fitting, held-out validation, and censored failures prevent overclaiming.
- **Economics/operations:** deadline, cost, energy, reliability, and queueing choose useful p/N.
- **Security/privacy:** task/trace/workload metadata needs bounds and access control.
- **Safety:** theoretical acceleration never substitutes for domain outcome validation.

## References

1. Gene M. Amdahl, “Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities,” *AFIPS Spring Joint Computer Conference*, 1967. <https://doi.org/10.1145/1465482.1465560>
2. John L. Gustafson, “Reevaluating Amdahl's Law,” *Communications of the ACM* 31(5), 1988. <https://doi.org/10.1145/42411.42415>
3. Richard P. Brent, “The Parallel Evaluation of General Arithmetic Expressions,” *Journal of the ACM* 21(2), 1974. <https://maths-people.anu.edu.au/~brent/pub/pub022.html>
4. Robert D. Blumofe and Charles E. Leiserson, “Scheduling Multithreaded Computations by Work Stealing,” *Journal of the ACM* 46(5), 1999. <https://doi.org/10.1145/324133.324234>
5. Robert D. Blumofe and Charles E. Leiserson, “Space-Efficient Scheduling of Multithreaded Computations,” *SIAM Journal on Computing* 27(1), 1998. <https://doi.org/10.1137/S0097539793259471>
6. OpenMP Architecture Review Board, *OpenMP API Specification 6.0*, 2024. <https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-6-0.pdf>
7. OpenMP Architecture Review Board, *OpenMP API 6.0 Reference Guide*, 2024. <https://www.openmp.org/wp-content/uploads/OpenMP-RefGuide-6.0-OMP60SC24-web.pdf>
8. oneTBB Project, *How Task Scheduler Works*, current documentation; retrieved 2026-08-29. <https://uxlfoundation.github.io/oneTBB/main/tbb_userguide/How_Task_Scheduler_Works.html>
9. Lawrence Livermore National Laboratory, *Caliper: A Performance Analysis Toolbox in a Library*, current documentation; retrieved 2026-08-29. <https://software.llnl.gov/Caliper/>
10. OpenCilk Project, *OpenCilk Language Extension Specification: Tasking Constructs*, current documentation; retrieved 2026-08-29. <https://cilk.mit.edu/docs/OpenCilkLanguageExtensionSpecification.htm>

## Exercises

### Exercise 1

For f=.08, compute Amdahl speedup and efficiency at p=4,16,64 and the infinite limit. Then recompute with overhead `O(p)=.002(p-1)` added to normalized time.

### Exercise 2

A scaled run on 32 processors spends 4% of elapsed time serially. Compute Gustafson speedup. Explain why it cannot answer how a fixed small input runs on 32 processors.

### Exercise 3

A DAG has work 240 and span 30. For p=4,8,16 compute the work/span lower bound, speedup ceiling, and `span+(work-span)/p` Brent-style upper bound. Interpret the gap.

### Exercise 4

Design an evidence plan to determine whether a scaling limit comes from algorithmic span, scheduling overhead, communication, or load imbalance. Include DAG mapping, measurements, perturbations, and claim boundaries.

### Exercise 5

Transfer the three-model framework to real-time distributed cardiac-image reconstruction. Specify work/result, scaled value, DAG/numeric, deadline/failure, privacy/security, validation, publication, and named reviewer invariants without claiming review.

## Answers to the Exercises

### Answer 1

Without overhead, `S=1/(.08+.92/p)`: p=4 gives `1/.31≈3.225806`, efficiency .806452; p=16 gives `1/.1375≈7.272727`, efficiency .454545; p=64 gives `1/.094375≈10.596026`, efficiency .165563; limit 12.5. With overhead added to time: p=4 denominator .316, `S≈3.164557`, E≈.791139; p=16 denominator .1675, `S≈5.970149`, E≈.373134; p=64 denominator .220375, `S≈4.537166`, E≈.070893. Growing overhead can reverse speedup even though elementary f is unchanged.

### Answer 2

With s=.04 and p=32, `S_G=32-.04*31=30.76`. This converts the parallel elapsed work into a serial-equivalent scaled-work amount under ideal mapping. The fixed small input may not contain the additional parallel work, may be dominated by its fixed serial/communication costs, and requires its own fixed-work measurements/model.

### Answer 3

`T1=240`, `Tinf=30`, parallelism 8. At p=4, lower bound `max(60,30)=60`, speedup ceiling 4, upper `30+210/4=82.5`. At p=8, lower 30, ceiling 8, upper 56.25. At p=16, lower 30, ceiling 8, upper 43.125. The interval is not measured runtime: it brackets what capacity/dependency constraints and a generic finite-p schedule allow in the abstract model. At and beyond eight processors span sets the lower bound; better exact scheduling/DAG structure can narrow the gap, while real overhead can exceed the upper model because its assumptions omit costs.

### Answer 4

Construct a correctness-complete DAG with task weights and data/control/synchronization edges; calculate work/span and record ready parallelism. Trace validated runs with task create/execute/queue/steal/idle, critical path, per-rank useful work/max/mean, messages/bytes/post-complete/collective arrivals, and full time. Coarsen tasks while holding DAG semantics to test scheduler overhead; restructure one dependency chain to test span; alter placement/message aggregation or remove one communication round safely to test communication; rotate data and rebalance to test skew. Keep input/algorithm/tolerance/precision/output/resources comparable, repeat with uncertainty, and require both predicted local metric and end-to-end valid time to respond. Claim only tested sizes, p, scheduler/runtime/system, and configurations.

### Answer 5

Fixed work holds patient/study/images/coils/geometry/calibration/model/objective/iterations or convergence, precision and diagnostic output fixed. Scaled work must name useful value—higher resolution, more temporal frames, uncertainty samples, or patients within authorized latency—without weakening image-quality or clinical checks. The DAG includes acquisition readiness, calibration, transforms, coil combination, iterative dependencies, reductions, device transfers, and publication; weights include scheduling/communication and numerical-order policy. Enforce study/patient/consent/model/epoch identity, coordinates/units, finite/range checks, residual and reference-image metrics, deadline/missing/corrupt data, bounded memory/queues, authenticated encrypted least-privilege transport, redacted telemetry, checkpoint/idempotent restart, conservative fallback, and fail-closed publication. Validate phantoms and independently curated cases, high-precision/reference reconstruction, adversarial schedules/failures, subgroup/artifact sensitivity, restore, security/privacy, and workflow. Named radiology/cardiology, MR/CT imaging and medical physics, numerical/inverse-problems, distributed/HPC/performance, clinical data/privacy/security, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers are required. No external review, diagnostic validity, privacy guarantee, approval, or deployment authorization is claimed.
