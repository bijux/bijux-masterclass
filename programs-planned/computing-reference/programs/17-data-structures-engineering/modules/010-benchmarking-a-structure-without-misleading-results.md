---
module_id: DSE-010
program: Data Structures Engineering
level: 1
module_number: 10
title: Benchmarking a Structure Without Misleading Results
status: complete
last_verified: 2026-08-29
---

# Benchmarking a Structure Without Misleading Results

## One-Page Review

### Governing question

How can an engineer measure a data structure so that the workload, implementation, environment, statistics, and conclusion remain aligned—and another engineer can reproduce or challenge the result?

### Essential definitions

- A **benchmark claim** names a subject, comparator, workload population, metric, environment, and scope of inference.
- The **benchmark unit** is the exact operation or operation sequence whose cost is included in one observation.
- An **estimand** is the quantity a study intends to estimate, such as median lookup latency for a declared hit/miss mix or throughput at a declared concurrency.
- A **measurement iteration** performs one or more benchmark units between timer reads; batching can reduce timer/harness overhead.
- A **trial/repetition** is a separately observed run; a **process fork** or fresh runtime can capture variation hidden within one process.
- **warm-up** is untimed or separately analyzed execution used to reach a declared state such as compiled code, populated caches, or allocator equilibrium.
- **steady state** is a modeled operating regime, not a universal point that every runtime necessarily reaches.
- **randomized interleaving** varies candidate/baseline order to reduce confounding from drift; **blocking** groups comparable observations by machine, process, or time window.
- An **effect size** quantifies the magnitude of a difference or ratio; an **uncertainty interval** describes inferential uncertainty under stated assumptions.
- **representativeness** is the relationship between the benchmark workload/environment and the real decision population. It cannot be inferred from low measurement variance.
- A **regression threshold** combines measurement uncertainty with a practically important change, rather than treating any tiny statistically detectable change as operationally meaningful.

### Central model, mechanism, or theorem

An observed time can be decomposed conceptually as

$$
Y_{e,p,r,i}=\mu + E_e + P_{e,p} + R_{e,p,r} + \varepsilon_{e,p,r,i},
$$

where $E$ captures environment or machine/session variation, $P$ process/runtime variation, $R$ repetition-level variation, and $\varepsilon$ within-repetition noise. Thousands of loop iterations in one process do not replace independent process or environment repetitions when inference includes those sources.

For paired baseline $B_j$ and candidate $C_j$ measured in comparable block $j$, an effect can be reported as $q_j=C_j/B_j$ or speedup $s_j=B_j/C_j$, with raw pairs and an interval from an explicitly justified analysis. The ratio direction, aggregation rule, and unit must be stated.

### Critical invariants

1. Correctness and equivalent work are verified before timing comparisons.
2. Setup, input generation, copying, cleanup, and validation are either intentionally included or explicitly outside the timed unit.
3. Results are consumed so optimizing compilers/runtimes cannot erase, fold, or hoist the intended work.
4. Baseline and candidate see the same declared data distributions, states, and operation mix under randomized or counterbalanced order.
5. Raw observations, failures, exclusions, versions, flags, and environment metadata are retained.
6. Statistical units match independent experimental units; loop iterations are not misreported as independent machines or process runs.
7. Conclusions do not extend beyond tested sizes, keys, layouts, cache states, runtimes, hardware, concurrency, or resource limits.

### Common failures

- Timing a single call with a wall clock and reporting the result as typical.
- Benchmarking construction for one implementation but only lookup for another.
- Allowing dead-code elimination, constant folding, hoisting, or cached results.
- Using sorted/easy keys while claiming random, adversarial, or production behavior.
- Reporting only the minimum, fastest configuration, favorable machine, or successful run.
- Pooling millions of inner-loop iterations as though they were independent replications.
- Ignoring warm-up, JIT compilation, garbage collection, allocator state, thermal throttling, frequency scaling, NUMA placement, or background work.
- Comparing means without raw distributions, uncertainty, practical significance, and workload context.
- Measuring latency under closed-loop load and claiming open-loop tail behavior.
- Treating hardware-counter correlation as causal explanation.

### Compact example

To compare two map implementations, pre-generate identical key/query streams with a declared size, key distribution, hit ratio, load factor, and update mix. Verify equal answers. In each fresh process, randomize which implementation runs first, warm according to a documented rule, measure several sufficiently long repetitions, and retain each raw value. Report the paired effect and interval, allocation/footprint results from separate or accounted-for instrumentation, environment metadata, and anomalies. The conclusion is “candidate was faster for this workload and environment,” not “candidate maps are faster.”

### Connections

[DSE-002](002-representation-invariants.md) and [DSE-003](003-operation-contracts.md) protect equivalent semantics, [DSE-004](004-time-space-and-allocation-cost.md) supplies cost models, [DSE-005](005-contiguous-and-linked-layouts.md) and [DSE-006](006-memory-locality-and-cache-behavior.md) supply representation hypotheses, and [DSE-009](009-property-based-testing-of-data-structures.md) supplies generated correctness evidence. Later modules apply this protocol to arrays, lists, trees, hashes, graphs, persistent structures, external memory, and concurrency.

## Governing Question

What experimental contract, harness design, environment control, statistical analysis, and reporting evidence are necessary before a measured difference between data structures supports a defensible engineering decision?

## Why This Matters

Performance results are unusually easy to produce and unusually easy to misinterpret. A timer returns a number even when the compiler removed the work, the setup dominates, the inputs favor one representation, the machine is throttling, or the sample units are not independent. A polished chart can conceal that only one process ran, correctness was never checked, inconvenient trials were discarded, or the comparator performed different work.

Data structures amplify these risks because cost depends on state and history. Dynamic-array append alternates cheap operations with growth events. Hash lookup depends on occupancy, hash quality, hit ratio, key cost, tombstones, and collision structure. Tree performance depends on shape, comparison cost, allocation, and traversal. Concurrent structures depend on contention and offered load. A benchmark must therefore be designed like an experiment: begin with a decision and estimand, control or record relevant factors, validate work, preserve raw evidence, and limit the conclusion to the sampled population.

## Prerequisites and Retrieval

Before this module, retrieve:

- abstraction functions, observational equivalence, and invariants from [DSE-001](001-abstract-data-types-and-concrete-representations.md) and [DSE-002](002-representation-invariants.md);
- preconditions, postconditions, mutation, error, and resource contracts from [DSE-003](003-operation-contracts.md);
- time, space, allocation, amortized, and tail-cost distinctions from [DSE-004](004-time-space-and-allocation-cost.md);
- layout and memory-access mechanisms from [DSE-005](005-contiguous-and-linked-layouts.md) and [DSE-006](006-memory-locality-and-cache-behavior.md);
- generated semantic checking and finite-evidence limits from [DSE-009](009-property-based-testing-of-data-structures.md);
- descriptive statistics, probability, sampling, confidence intervals, and experimental variables.

## Learning Objectives

After completing this module, you should be able to:

1. write a falsifiable, scoped benchmark claim and derive its workload, metrics, comparator, and estimand;
2. define equivalent benchmark units and separate or intentionally include setup, mutation, validation, and teardown;
3. prevent common optimization artifacts and verify that the intended work occurred;
4. construct representative data-structure workloads across size, shape, state, keys, operations, and lifecycle events;
5. design warm-up, batching, process, session, interleaving, randomization, and blocking protocols;
6. distinguish inner iterations from independent repetitions and model hierarchical sources of variation;
7. report raw data, effect sizes, uncertainty, practical thresholds, distributions, and exclusions without cherry-picking;
8. benchmark latency, throughput, memory, allocation, energy, and hardware counters without conflating their meanings;
9. design concurrent and tail-latency experiments with explicit load and sampling semantics;
10. make a narrow performance claim and document what the experiment cannot establish.

## Core Exposition

**Write the claim before the harness.** “Structure A is faster than B” is not a testable engineering claim. A usable version is: “On hardware H and runtime R, for maps containing $10^5$ immutable 16-byte keys at load factors 0.55–0.75, with 90% successful lookup and 10% update drawn from distribution W, candidate C has lower median per-operation elapsed time than baseline B by at least 8%, without increasing peak resident memory by more than 5%.” This statement exposes the subject, comparator, workload, environment, primary metric, practical threshold, and resource constraint. It can be wrong, refined, or reproduced.

The decision controls the benchmark level. A microbenchmark isolates a mechanism such as lookup, traversal, or insertion. A component benchmark measures a realistic sequence through an API. An application benchmark includes integration effects. Microbenchmarks diagnose mechanisms but often omit serialization, synchronization, allocation pressure, and surrounding work; application benchmarks are representative but harder to attribute. Use a ladder rather than forcing one benchmark to answer every question.

**Correctness precedes timing.** Establish that baseline and candidate implement the same abstract operation over the same input and state. Validate results outside the timed region when validation is not part of production cost, but do validate every benchmark configuration. Compare checksums, models, or exact outputs; confirm operation counts and final states. A faster implementation that skips work, changes collision semantics, mutates fewer records, or returns stale results is not a performance win.

**Specify the timed unit.** Let one unit include exactly the operations relevant to the claim. State whether it includes input decoding, allocation, key hashing, structure construction, cache reset, cleanup, and result validation. If a lookup benchmark generates a random key inside the timer, it measures random generation plus lookup. If one candidate reuses a built index and the other rebuilds it, the comparison answers a lifecycle question—not pure lookup. Both can be legitimate if named honestly.

Timer overhead and resolution can dominate tiny operations. Batch $k$ units between reads, compute per-unit cost only when operations are independent enough and batching does not change the behavior of interest, and choose duration well above timer resolution and scheduler granularity. Do not blindly subtract an “empty loop”: harness overhead may interact with the subject, and subtraction magnifies error when two similar noisy quantities are differenced. Prefer established language/runtime benchmark harnesses that calibrate loops and record metadata.

**Ensure the work survives optimization.** In compiled and managed environments, unused results can be removed, constant inputs folded, invariant work hoisted, loops vectorized, or calls inlined into a nonrepresentative form. Consume outputs through framework facilities or an observable checksum, vary inputs in a controlled way, inspect generated code or profiles for critical claims, and test that changing the implementation changes observations. Anti-optimization barriers themselves have cost; apply equivalent barriers and understand whether they alter the production path. A professional harness reduces pitfalls but does not make experimental judgment automatic.

**Workload state is part of the independent variable.** For each structure, define at least:

- logical size and physical capacity;
- fill/load factor, tombstone count, fragmentation, or slack;
- key/value size, lifetime, equality/hash/comparison cost, duplication, skew, and locality;
- structure shape, depth, balance, clustering, and insertion history;
- operation mix, ordering, dependency, hit/miss ratio, and mutation frequency;
- cold, warmed, steady, growth, resize, rehash, compaction, recovery, and teardown regimes;
- read/write sharing, contention, thread count, affinity, and offered load where applicable.

Do not use one “random” dataset as a proxy for all workloads. Uniform random keys can be valuable, but production may be Zipf-skewed, sequential, time-correlated, prefix-sharing, collision-prone, or adversarial. Include named synthetic populations plus sampled and privacy-reviewed production-derived distributions where authorized. Preserve seeds and concrete workload files or generators. Verify that both candidates receive equivalent data without accidental cache priming from always running one first.

**Vary size to reveal regimes.** One $n$ cannot distinguish constant factors from scaling or expose cache/translation/capacity thresholds. Choose sizes around empty/small fast paths, inline capacity, allocator classes, cache levels, page/translation reach, growth boundaries, and realistic maxima. Plot raw observations and summaries against $n$; fit complexity only when the theoretical and statistical model justifies it. A straight line on a log plot is not proof of asymptotic complexity, and a microbenchmark range cannot establish behavior beyond measured sizes.

Amortized operations need both aggregate and tail views. For dynamic-array append, report long-run work per append, latency distribution, and individual resize spikes. If the production requirement is a maximum pause, an average hides the decision variable. Pre-sizing changes the workload and should be a separate configuration, not a silent optimization for one candidate.

**Control and disclose the environment.** Record CPU/architecture, core topology, memory, firmware where relevant, OS/kernel, runtime/compiler and flags, allocator, dependencies, benchmark commit, power mode, frequency/turbo policy, thermal state, affinity, NUMA placement, page settings, container/virtual-machine limits, background load, and date. Isolation may reduce noise through dedicated hosts, fixed affinity, disabled background services, stable power configuration, and thermal conditioning, but each intervention changes external validity and must be disclosed.

Never claim that an observed ranking is a hardware invariant. A contiguous traversal often benefits from spatial locality, yet ranking and ratios can reverse with element size, prefetching, compiler, vectorization, cache state, allocator, architecture, or workload. Treat microarchitectural explanations as hypotheses supported by measurements, not universal laws.

**Warm-up must match the runtime and question.** Managed runtimes may interpret, compile, recompile, deoptimize, collect garbage, or change profiles. Native code still experiences page faults, caches, branch predictors, allocator state, dynamic linking, and frequency changes. Define whether cold start, transition behavior, or warmed performance is the target. Inspect time series rather than deleting an arbitrary number of iterations. Use fresh process forks to sample runtime-layout and compilation variation when relevant. If no stable regime is visible, report phases or the entire distribution rather than manufacturing “steady state.”

**Design repetitions at every relevant level.** Inner iterations reduce timer noise but are often correlated. Repetitions within a process capture short-term variation. Fresh processes capture runtime, address-layout, compilation, and allocator variation. Sessions across time or hosts capture environment variation. The experimental unit for a claim is the independently assigned or sampled unit at the relevant level. Reporting ten million loop iterations as $n=10{,}000{,}000$ is pseudoreplication if only one process/environment was sampled.

Use blocking and randomized or counterbalanced order. Pair baseline and candidate within comparable process/session blocks where doing so does not cause cross-contamination. Random interleaving helps distribute time drift; alternating order balances simple order effects. When one run warms shared caches or changes thermal state for the next, isolate or model carryover. Store execution order so anomalies can be diagnosed.

**Choose statistics after naming the estimand.** Retain and publish raw observations where possible. Report counts at each hierarchy, units, central tendency, dispersion, tails where relevant, and uncertainty intervals. Means answer additive total-time questions; medians describe a distribution's midpoint; quantiles describe tail positions but require enough observations and careful uncertainty. A median is not automatically “robust truth,” and a minimum is not automatically “machine potential.”

Compare effects, not isolated significance tests. Report candidate/baseline ratio or absolute difference with direction clearly defined, an interval from an analysis compatible with the design, and the practical threshold chosen before seeing results. If the interval spans both meaningful improvement and meaningful regression, the result is inconclusive. Statistical significance can make a negligible difference detectable with large samples; practical significance asks whether it changes the engineering decision.

Do not remove outliers merely because they are inconvenient. Investigate them against predeclared exclusion rules: a documented unrelated system interruption may justify exclusion with both raw and filtered analyses, while garbage collection or resize pauses may be intrinsic to the workload. Repeatedly tuning parameters, selecting sizes, or comparing many structures raises multiplicity and researcher-degrees-of-freedom risks; disclose all comparisons and distinguish exploratory from confirmatory work.

**Ratios require care.** `candidate/baseline < 1` means lower time; `baseline/candidate > 1` means speedup. State which. The ratio of arithmetic means, mean of paired ratios, and ratio of medians are different estimands. Use pairing when observations share a block, preserve the pairs, and avoid averaging normalized scores without a justified aggregation rule. For multi-workload suites, an aggregate can hide regressions; always report each workload alongside any aggregate.

**Metrics answer different questions.** Elapsed latency includes waiting; CPU time does not. Throughput counts completed work per time but can rise while individual latency degrades. Allocation counts, peak live memory, resident set, cache misses, cycles, instructions, branch misses, energy, and bandwidth illuminate mechanisms but may require separate instrumentation. Profilers and counters perturb execution, can multiplex, and vary in availability/meaning across hardware. First establish the performance effect with minimal instrumentation, then run diagnostic experiments and state that they are separate observations.

Hardware counters do not prove causation. If candidate A has fewer cache misses and lower time, both may arise from another factor. Use controlled perturbations, profiles, source/assembly inspection, and multiple metrics to build a mechanism argument. Normalize counters by operations or useful work where appropriate, report multiplexing/scaling, and record counter definitions.

**Concurrent benchmarking needs a load model.** Specify threads, cores, affinity, shared/private data, read/write mix, contention/key distribution, synchronization, and work outside the structure. A closed-loop worker submits the next operation only after completion; this couples offered load to response time and can underrepresent queueing tails. An open-loop design schedules arrivals independently and must record overload and dropped work. Avoid coordinated omission: latency sampling must account for requests that should have occurred during stalls when the target workload calls for them.

Check concurrent correctness during or around the benchmark without silently excluding failed operations. Throughput from an incorrect structure is invalid. Report scaling relative to one thread, absolute throughput, latency distributions, CPU utilization, and saturation. Pinning all threads to one core or allowing migration can both be legitimate only for corresponding claims.

**Regression automation needs governance.** Run cheap noise-tolerant checks frequently and higher-rigor benchmarks on controlled workers. Compare against a rolling or versioned baseline using predeclared practical thresholds and uncertainty. Quarantine infrastructure failures separately from performance regressions, but do not auto-retry until a regression disappears. Store raw results and environment fingerprints. Confirm important changes on fresh runs and inspect correctness, profiles, code, and system state before attribution.

**Report an evidence package.** Include claim, workload generator/data digest, correctness checks, benchmark code and commit, compiler/runtime/dependency versions and flags, machine/environment record, warm-up and repetition hierarchy, ordering, raw data, analysis code, exclusions, figures/tables, effect/uncertainty, anomalies, and limitations. A result is an observation under conditions, not an intrinsic scalar attached permanently to a data structure.

The following executable analyzes fixed synthetic paired observations. It verifies arithmetic and reporting mechanics deterministically; it intentionally performs no runtime benchmark.

<!-- bijux-verify: {"id":"paired-benchmark-analysis","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"blocks=8\nbaseline_mean_ns=101.000\ncandidate_mean_ns=92.000\nratio_candidate_over_baseline=0.911\nspeedup_baseline_over_candidate=1.098\npaired_improvements=8/8\nevidence=synthetic_analysis_not_runtime_benchmark\n","stderr":""}} -->
```python
from statistics import fmean


baseline_ns = (105, 100, 98, 102, 101, 99, 103, 100)
candidate_ns = (92, 91, 90, 94, 93, 89, 95, 92)

assert len(baseline_ns) == len(candidate_ns)
assert all(value > 0 for value in baseline_ns + candidate_ns)

baseline_mean = fmean(baseline_ns)
candidate_mean = fmean(candidate_ns)
ratio = candidate_mean / baseline_mean
speedup = baseline_mean / candidate_mean
improvements = sum(candidate < baseline for baseline, candidate in zip(baseline_ns, candidate_ns))

print(f"blocks={len(baseline_ns)}")
print(f"baseline_mean_ns={baseline_mean:.3f}")
print(f"candidate_mean_ns={candidate_mean:.3f}")
print(f"ratio_candidate_over_baseline={ratio:.3f}")
print(f"speedup_baseline_over_candidate={speedup:.3f}")
print(f"paired_improvements={improvements}/{len(baseline_ns)}")
print("evidence=synthetic_analysis_not_runtime_benchmark")
```

These synthetic values imply a ratio of means near 0.911 and reciprocal speedup near 1.098 for this table only. They provide no evidence that any real implementation is faster and no uncertainty interval. A real report would retain the raw hierarchy, justify its interval procedure, include correctness and environment evidence, and avoid treating eight pairs as universally representative.

## Definitions and Notation

Let $W$ be the workload population, $H$ the hardware/software environment, $A$ and $B$ the implementations, and $Y(A,W,H)$ a measurement distribution. An **observation** is one recorded value with its experimental-unit identity. The **estimand** $\theta$ might be $E[Y]$, a median, a quantile, a throughput, an absolute difference, or a ratio under a specified design.

Use $n$ for logical structure size, $k$ for batched operations per timer interval, $i$ for inner iteration, $r$ for repetition, $p$ for fresh process, and $e$ for session/environment. A **factor** is a controlled or observed variable; a **confounder** changes with the candidate and can also change the outcome.

For paired time observations, define $q_j=C_j/B_j$ and $s_j=B_j/C_j=1/q_j$. Values $q<1$ favor the candidate for lower-is-better time; values $s>1$ indicate speedup. A **confidence interval** is a procedure with repeated-sampling coverage under a model, not a probability that a fixed parameter lies in one realized interval.

## Mechanisms, Invariants, or Proof Structure

Equivalent-work validation establishes that measured subjects compute the same declared abstract result. Timing decomposition assigns setup, work, and cleanup to explicit regions. Anti-optimization observations establish that the work remains observable under the compiled runtime. Workload hashes and operation counters establish comparable inputs and volumes.

Randomized pairing supports a within-block effect when both candidates share relevant block conditions and carryover is controlled. Hierarchical repetition supports inference only at levels actually sampled: inner iterations estimate within-run behavior, while fresh processes or environments are needed to estimate their variation. Independence is an assumption to defend, not a property conferred by a large row count.

Asymptotic reasoning and benchmarking answer different propositions. A proof may bound abstract operation counts as $n\to\infty$; a benchmark estimates realized costs over finite regimes. Neither replaces the other. Mechanism attribution proceeds from a predeclared hypothesis through controlled contrasts and corroborating observations; one counter correlation is insufficient.

## Alternatives and Trade-Offs

- **Microbenchmarks** isolate mechanisms and regressions; end-to-end benchmarks improve representativeness but weaken attribution.
- **Cold-start measurement** captures startup/page/JIT effects; warmed measurement captures a later regime. Report whichever matches the decision, often both.
- **Same-process pairing** controls many factors; fresh-process comparison captures runtime variation and reduces contamination.
- **System tuning/pinning** reduces variance; default environments may better represent users. Disclose and justify the choice.
- **Wall time** captures experienced latency; CPU time isolates processor consumption but omits waits and can aggregate threads differently.
- **Means** support additive totals; medians and quantiles describe distribution locations. None is universally best.
- **More iterations** reduce timer error; more independent processes/machines expand the inference population. They are not substitutes.
- **Automatic regression gates** give fast feedback; rigorous controlled confirmation costs more but protects high-impact decisions.
- **Hardware counters/profilers** aid diagnosis; their overhead and semantics can perturb the primary measurement.
- **Synthetic workloads** provide control and reproducibility; production-derived workloads improve relevance but raise privacy, drift, licensing, and sharing constraints.

## Failure Modes and Misconceptions

1. **“The fastest observed run is true performance.”** It may be a lucky noise realization or a selected condition.
2. **“Low variance means representative.”** It can mean a precisely measured irrelevant workload.
3. **“A harness prevents misleading benchmarks.”** It handles mechanics; workload and inference judgment remain human responsibilities.
4. **“Warm-up means discard the first N iterations.”** Transition length is runtime-, code-, and environment-dependent.
5. **“Native code needs no warm-up.”** Caches, pages, linking, allocators, predictors, frequency, and thermal state still evolve.
6. **“Millions of operations give millions of samples.”** Batched operations within one process are often correlated subsamples.
7. **“Median is always safer than mean.”** The correct summary depends on the estimand and distribution.
8. **“A small p-value means an important speedup.”** Magnitude, uncertainty, and practical threshold decide usefulness.
9. **“Outliers are noise.”** They may be resize, collection, contention, paging, or failures intrinsic to the system.
10. **“Same Big-O means same performance.”** Constants and finite memory/runtime regimes matter.
11. **“A measured slope proves Big-O.”** Finite curves do not establish asymptotic theorems.
12. **“Fewer cache misses caused the speedup.”** Correlation and instrumentation do not establish causation.
13. **“One machine establishes portability.”** Rankings and ratios can change across hardware and software contexts.
14. **“Higher throughput means lower latency.”** Queueing and batching can improve one while harming the other.
15. **“Retries make CI benchmarks reliable.”** Retrying until green biases evidence and conceals infrastructure or product instability.
16. **“A benchmark score belongs to the structure.”** It belongs to a versioned subject-workload-environment-method tuple.

## Worked Examples

### Example 1

Benchmark vector append across sizes straddling each growth boundary. Preconstruct identical initial states, time only append for the operation claim, verify final content, and separately report long-run mean work and individual resize latency. A pre-reserved vector is a distinct configuration.

### Example 2

Compare linked and contiguous traversal using identical abstract values at several element sizes and footprints. Consume a checksum, randomize order, record allocator and placement, and profile separately. Conclude only for observed regimes; locality does not make the ranking universal.

### Example 3

For a hash map, cross size with load factor, successful/unsuccessful lookup, key length, hash cost, skew, collisions, tombstones, and mutation history. A uniform integer-key lookup benchmark cannot justify claims about string keys or adversarial traffic.

### Example 4

For a balanced tree, generate valid shapes through multiple insertion orders, verify order and membership, and measure search, update, and traversal separately. Compare against a sorted array only under a workload containing both lookup and mutation costs relevant to the decision.

### Example 5

For small-stack representations, include empty, inline-capacity, spill, and shrink-back regimes. Compiler escape analysis and allocation removal must be inspected; otherwise the “allocation benchmark” may allocate nothing observable.

### Example 6

To test a 5% regression threshold, collect paired process-level repetitions on a controlled worker. Report raw pairs and candidate/baseline effect interval. If the interval spans 0.95 to 1.08, it includes meaningful improvement and regression; classify the result as inconclusive rather than selecting the favorable point estimate.

### Example 7

Measure memory footprint through allocated bytes, peak live bytes, and resident set as separate estimands. A compact representation may allocate less but retain pages; instrumentation can alter allocation and timing. Run or account for each tool separately.

### Example 8

Benchmark a concurrent queue with declared producer/consumer counts, affinity, item work, capacity, arrival model, and saturation range. Validate item conservation/order, report throughput and latency quantiles, and preserve stalls instead of omitting scheduled arrivals.

### Example 9

When a counter shows fewer last-level-cache misses, perturb structure size across cache regimes and inspect profiles/assembly. If time and miss changes co-vary as predicted, the mechanism argument strengthens, but it remains scoped and may have alternatives.

### Example 10

For a medication-priority index, benchmark synthetic records at declared sizes and operation mixes only after semantic validation. Tail latency, resource bounds, audit overhead, and failure behavior may be relevant, but clinical safety thresholds, deployment capacity, privacy, quality, and regulatory acceptance require named owners and representative system-level evidence.

## Cross-Program Connections

- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) relates experimental curves to operation counts, complexity hypotheses, and workload families.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns regression policy, correctness evidence, flakiness, and quality gates.
- [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns controlled workers, telemetry, capacity, tail latency, and release decisions.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) explains scheduling, affinity, timers, pages, allocators, NUMA, and resource accounting.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains caches, predictors, counters, pipelines, frequency, and memory bandwidth.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies contention, synchronization, scalability, histories, and memory-model constraints.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies benchmark infrastructure, environment fingerprints, artifact retention, and governed automation.

## References

1. Google Benchmark maintainers, [User Guide](https://github.com/google/benchmark/blob/main/docs/user_guide.md). Setup/teardown, repetitions, warm-up, optimization barriers, counters, complexity, interleaving, metadata, and output formats.
2. OpenJDK, [Java Microbenchmark Harness](https://github.com/openjdk/jmh). Official JMH project, samples, generated harness requirements, pitfalls, and peer-review warning.
3. Python `pyperf` maintainers, [Run a Benchmark](https://pyperf.readthedocs.io/en/latest/run_benchmark.html). Calibration, worker processes, warm-ups, loops, jitter, metadata, and stability analysis.
4. Go Project, [`testing` Package](https://pkg.go.dev/testing#hdr-Benchmarks). Official benchmark-loop, allocation, elapsed-time, and parallel benchmark contract.
5. Criterion.rs maintainers, [Criterion.rs Book](https://bheisler.github.io/criterion.rs/book/). Rust measurement, warm-up, resampling analysis, plots, baselines, and profiling workflow.
6. Tomas Kalibera and Richard E. Jones, [Rigorous Benchmarking in Reasonable Time](https://kar.kent.ac.uk/33611/45/p63-kaliber.pdf). Hierarchical variation, repetition design, and statistically rigorous summarization.
7. Andy Georges, Dries Buytaert, and Lieven Eeckhout, [Statistically Rigorous Java Performance Evaluation](https://users.elis.ugent.be/~leeckhou/papers/oopsla07-stat.pdf). Managed-runtime iterations, process invocations, confidence intervals, and experimental methodology.
8. Todd Mytkowicz et al., [Producing Wrong Data Without Doing Anything Obviously Wrong](https://sape.inf.usi.ch/publications/asplos09.html). Primary publication record on hidden experimental bias and causal ambiguity.
9. SPEC Open Systems Group, [SPEC CPU 2026 Run and Reporting Rules](https://www.spec.org/cpu2026/docs/runrules.html). Current observation, reproducibility, method, configuration, disclosure, and reporting rules.
10. Linux kernel documentation, [Perf Security](https://docs.kernel.org/admin-guide/perf-security.html). Access control, monitoring scope, and security/resource implications of performance counters.
11. NIST/SEMATECH, [e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/). Experimental design, exploratory analysis, confidence intervals, process variation, and statistical terminology.

## Exercises

### Exercise 1

Write a benchmark contract comparing dynamic-array and linked-list insertion. Define decision, workload population, timed unit, metrics, environment, repetitions, correctness, and claim limits.

### Exercise 2

Design a hash-map benchmark matrix that can distinguish load-factor, hit-ratio, key-cost, collision, tombstone, and resize effects without an unmanageable experiment.

### Exercise 3

Given nested measurements from iterations, processes, and three machines, define the experimental units and analysis for a candidate/baseline comparison. Explain why pooling all iterations is invalid.

### Exercise 4

Design a concurrent queue benchmark that reports throughput and latency without coordinated omission and that preserves correctness evidence.

### Exercise 5

Prepare the evidence and review plan for a performance claim about a clinical data structure. Separate mechanical benchmarking from deployment and safety decisions.

## Answers to the Exercises

### Answer 1

Choose a real decision, for example inserting at a known position in collections of 10²–10⁶ fixed-size immutable values under a declared position distribution and mutation history. Define whether locating the position is included; otherwise a list iterator and array index do unequal work. Preconstruct equivalent states, verify final sequences, consume results, and time the same insertion-plus-required shift/link work; measure allocation and footprint separately. Cross sizes and positions, randomize paired order, use sufficient batch duration, multiple repetitions and fresh processes, and retain environment/raw data. Report effects and uncertainty per regime. Do not generalize to lookup, traversal, unknown positions, other allocators, hardware, element types, or concurrent use.

### Answer 2

Use a fractional or staged matrix rather than every Cartesian combination. First screen representative low/mid/high sizes and load factors with hit ratios 0/0.5/1, cheap integer and realistic string keys, uniform/skewed access, clean/tombstone-heavy states, and ordinary/deliberate-collision hashes. Then focus confirmatory runs on interactions indicated by mechanisms, including pre/post resize boundaries. Generate identical streams, validate exact responses/final maps, label operation counts, randomize candidate order, and block by process/session. Predeclare primary workloads and treat exploration separately. Retain per-cell raw effects; no aggregate may hide a severe cell regression.

### Answer 3

Inner iterations within a repetition mostly reduce timer error and estimate within-process behavior; they share code, runtime, environment, and history. Fresh processes are independent units for process-layout/JIT/allocator variation, and machines are units for the three-machine population. Pair candidate and baseline within process or machine blocks when carryover is controlled, summarize within-process measurements, then analyze process-level paired effects nested in machine. To generalize beyond the three machines requires an explicit sampling population and more machines. Pooling all iterations treats correlated subsamples as independent, understates uncertainty, and cannot manufacture machine-level replication.

### Answer 4

Declare queue capacity, item size/work, producer/consumer counts, affinity, shared topology, arrival model, read/write mix, run duration, warm-up, and saturation sweep. For open-loop arrivals, schedule independently of completion, retain intended timestamps, and record late/dropped/unfinished requests so stalls do not erase their own latency. For each operation retain start/end or sampled latency with an unbiased policy; report throughput, latency distributions, utilization, overload, and scaling. Verify item identity, conservation, allowed ordering, duplicates, failures, and shutdown. Use repeated fresh processes and controlled hosts, preserve schedules/seeds and raw events, and do not infer correctness or production capacity from one stress run.

### Answer 5

Use synthetic non-identifying data and a versioned workload based on authorized demand assumptions. Validate semantics before timing; measure relevant sizes, mixes, cold/warm behavior, failure/recovery, tail latency, memory, and audit overhead on representative controlled systems with raw hierarchical repetitions, environment records, practical thresholds, and uncertainty. Clinical/domain owners validate priority semantics and workload; safety/reliability owners review hazards and capacity margins; privacy/security review data and instrumentation; human-factors, accessibility, quality, operations, and regulatory owners review their scopes. A microbenchmark can support a narrow component-performance claim but cannot establish patient safety, end-to-end latency, privacy compliance, capacity, certification, or deployment fitness.
