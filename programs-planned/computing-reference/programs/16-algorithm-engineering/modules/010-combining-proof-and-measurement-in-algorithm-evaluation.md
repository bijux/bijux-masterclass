---
module_id: ALGE-010
program: Algorithm Engineering
level: 1
module_number: 10
title: Combining Proof and Measurement in Algorithm Evaluation
status: complete
last_verified: 2026-09-04
---

# Combining Proof and Measurement in Algorithm Evaluation

## One-Page Review

### Governing question

How can mathematical analysis, executable checks, instrumentation, controlled experiments, and reproducible artifacts be combined so each supports the claims it can actually justify?

### Essential definitions

- A **claim ledger** records each conclusion, its scope, required evidence, observed evidence, and limitations.
- **Analytical evidence** follows from a stated contract and mathematical model through derivation or proof.
- **Executable evidence** runs a concrete example or checker in a recorded environment and establishes observed behavior only there.
- **instrumentation** counts modeled mechanisms such as comparisons, bytes, allocations, calls, cache misses, or retries.
- A **benchmark** is a defined workload and measurement procedure for a system under test, not merely a timing loop.
- An **experimental unit** is the smallest independently assigned or sampled entity supporting inference; repeated iterations within one process may not be independent units.
- A **confounder** changes with the treatment and can offer an alternative explanation for an observed effect.
- **warm-up** is execution before the measured regime used to expose or stabilize effects such as compilation, cache population, or adaptive optimization.
- **randomization** assigns or orders treatments by a recorded random procedure to reduce systematic bias.
- An **effect size** describes the magnitude of a difference or ratio; **uncertainty** describes the precision or variability of its estimate.
- **reproducible artifacts** include enough code, data, configuration, environment, and procedure for another investigator to exercise or reconstruct evidence.

### Central model, mechanism, or theorem

Evaluation is a chain rather than one score:

$$
\text{contract}
\longrightarrow
\text{proof/model}
\longrightarrow
\text{instrumented mechanism}
\longrightarrow
\text{controlled observation}
\longrightarrow
\text{bounded decision}.
$$

For paired baseline times $b_i$ and candidate times $c_i$ measured under a design that justifies pairing, useful descriptive quantities include

$$
\bar d=\frac1m\sum_{i=1}^{m}(b_i-c_i),
\qquad
S=\frac{\bar b}{\bar c},
\qquad
R=100\left(1-\frac{\bar c}{\bar b}\right)\%.
$$

$S$ is speedup by the ratio-of-means convention and $R$ is percent time reduction. These arithmetic summaries do not establish causality, independence, asymptotic growth, or production benefit without the experimental design and workload scope.

### Critical invariants

- Validate output equivalence and contract compliance before comparing speed.
- State every claim with algorithm/version, inputs, environment, metric, statistic, and case/quantifier.
- Keep theorem premises, model-to-code correspondence, measured observations, and operational decisions as separate links.
- Use instrumentation to test mechanisms predicted by the model; timing alone rarely identifies a cause.
- Define experimental units and preserve hierarchy among rebuilds, processes, runs, iterations, requests, and inputs.
- Randomize or counterbalance treatment order and record seeds/procedures.
- Separate setup, warm-up, steady-state, teardown, and one-time lifecycle costs according to the decision.
- Choose input sizes and distributions before inspecting favorable results; include boundaries and adversarial families relevant to the claim.
- Report effect size and uncertainty, not only a winning mean, minimum, or significance label.
- Never discard outliers, failed runs, timeouts, or inconvenient configurations without a predeclared rule and explanation.
- Capture source revision, toolchain, dependencies, flags, machine, operating system, configuration, data identity, and raw observations.
- A finite experiment can refute a universal claim with a valid counterexample but cannot prove universal correctness or asymptotic complexity.
- Matching analytical and empirical trends strengthens correspondence; disagreement triggers investigation rather than selective reporting.
- Artifact availability, successful execution, result reproduction, and external review are different achievements.

### Common failures

Common failures include benchmarking wrong outputs; selecting only favorable inputs; timing setup in one variant but not another; treating loop iterations as independent samples; taking the minimum and hiding variability; fixing one random seed and claiming randomized performance; allowing thermal, power, background-load, placement, or treatment-order drift; ignoring JIT compilation and garbage collection; letting compilers delete unused work; comparing different compiler flags or precision; changing multiple factors at once; reporting speedup with the ratio reversed; averaging incomparable raw times; dropping timeouts; extrapolating a log-log slope from a narrow range; calling a local run reproducible; treating a benchmark as proof; and treating an asymptotic proof as a latency forecast.

### Compact example

Suppose five paired synthetic observations in milliseconds have baseline mean $\bar b=102$ and candidate mean $\bar c=83$. Then

$$
S=\frac{102}{83}\approx1.229,
\qquad
R=100\left(1-\frac{83}{102}\right)\%\approx18.6\%.
$$

The candidate is about $1.229$ times as fast by this convention, or uses about $18.6\%$ less time over these summaries. The calculation alone does not say the pairs were independent, representative, correctly warmed, unbiased, or precise. Those are design and uncertainty questions.

### Connections

[ALGE-001](./001-problem-statements-inputs-outputs-and-constraints.md) supplies the contract; [ALGE-005](./005-asymptotic-time-and-space.md) supplies growth claims; [ALGE-006](./006-best-worst-expected-and-amortized-cost.md) supplies quantifiers; [ALGE-009](./009-machine-models-and-hidden-constants.md) supplies machine and finite-cost models. [ALGE-011](../ROADMAP.md) begins applying this evaluation discipline to concrete algorithms.

## Governing Question

A proof can establish correctness for every admitted input or bound abstract cost as $n$ grows. A benchmark can observe one implementation on selected inputs and machines. Neither evidence type can safely impersonate the other. How should they be joined into an evaluation that is mathematically defensible, experimentally credible, operationally relevant, and possible to revisit?

The core move is to decompose the conclusion. “Algorithm B is better” is not one claim. It may contain output equivalence, an operation bound, a model-to-code mapping, a finite performance difference, a causal attribution, a workload forecast, and a deployment decision. Each part needs different evidence and has different failure modes.

## Why This Matters

Algorithm choices frequently fail at the seam between theory and experiment. A theoretically superior method can lose throughout the product's finite range because of constants or locality. A benchmark winner can fail on adversarial inputs, larger scales, another distribution, or a different machine. A measured speedup can disappear when setup is balanced, outputs are checked, treatment order is randomized, or independent processes replace correlated inner-loop iterations.

Good evaluation does more than rank implementations. It explains why they differ, under which premises, how uncertain the estimate is, and what would invalidate the decision. Counters connect an asymptotic model to code. Size sweeps challenge predicted slopes and crossovers. Boundary inputs challenge correctness and complexity. Environment capture and artifacts make later diagnosis possible.

This discipline also prevents false universality. A locally reproduced result is not external peer review. A public repository is not automatically exercisable. A passing microbenchmark is not production latency evidence. Precise labels make the work stronger because readers know exactly what survived which check.

## Prerequisites and Retrieval

Retrieve:

- problem contracts, correctness proofs, invariants, and boundary cases;
- asymptotic functions, exact counts, lower bounds, cost models, and crossover points;
- worst-case, expected, amortized, work, span, and output-sensitive quantifiers;
- mean, median, variance, ratios, percent change, sampling, and basic confidence intervals;
- compiler/runtime effects, caches, allocation, concurrency, and system noise;
- version control, dependency locking, executable checks, logs, and structured data.

You should be able to state why $T(n)\in\Theta(n\log n)$ does not predict a duration in seconds, why ten repeated timings in one process may not be ten independent experimental units, and why a faster wrong answer is not a candidate optimization.

## Learning Objectives

After completing this module, you should be able to:

1. decompose an evaluation conclusion into contract, analytical, correspondence, empirical, and decision claims;
2. design a benchmark with declared treatments, experimental units, workloads, metrics, and controls;
3. verify correctness and semantic equivalence before measuring performance;
4. instrument mechanisms predicted by an algorithmic or machine model;
5. handle warm-up, treatment order, random seeds, caching, setup, and runtime adaptation explicitly;
6. compute and interpret paired differences, speedup, and percent reduction correctly;
7. report variability and uncertainty without pretending correlated repetitions are independent;
8. diagnose common microbenchmark, workload, and selection biases;
9. package source, data, environment, commands, and raw results for reproducible evaluation;
10. make a bounded engineering decision and state what evidence would reverse it.

## Core Exposition

### Build a claim ledger before an experiment

For every planned conclusion, record:

| Claim | Example | Evidence that can support it |
|---|---|---|
| Contract | both variants return the same required stable ordering | specification, oracle, proof, tests |
| Analytical | comparisons are at most $an\log n+bn$ | derivation or proof in a stated model |
| Correspondence | one counter increment represents one key comparison | code inspection and instrumented checks |
| Empirical | candidate median latency is lower on workload $W$ and environment $E$ | controlled observations and uncertainty |
| Causal | changing layout caused the reduction | experimental control/randomization and mechanism evidence |
| Operational | deploy candidate under service objective $S$ | representative load, risk, rollback, and monitoring evidence |

The rows prevent evidence laundering. Unit tests do not prove an asymptotic theorem. A derivation does not show compiler behavior. Performance counters do not prove functional correctness. A controlled benchmark does not guarantee future workload stationarity.

Write limitations alongside the claim, not after someone challenges it. If only one processor, distribution, precision, or runtime version was evaluated, include that scope in the sentence.

### Correctness is the first benchmark gate

Before comparing costs:

1. run both variants on the same admitted inputs;
2. check outputs against a trusted oracle or independent implementation;
3. verify mutation, stability, ordering, precision, side effects, errors, and cancellation;
4. include empty, minimum, maximum, duplicate, malformed, and adversarial cases;
5. verify that compiler/runtime optimization cannot remove required work;
6. retain failing inputs and exact versions.

Equality of one output hash is evidence only under the hash and serialization assumptions. Approximate algorithms need a quality/error metric and acceptance threshold, not byte equality. Nondeterministic outputs need a semantic equivalence relation.

Performance changes can introduce overflow, altered floating reduction order, races, stale indexes, skipped validation, or weaker error handling. Treat these as contract changes unless explicitly accepted.

### Derive predictions that measurements can challenge

An analysis should produce observable consequences. If a loop is modeled as $3n+2$ comparisons, instrument comparisons and sweep $n$. If a cache-aware method predicts $\Theta(n/B)$ transfers, collect traffic or miss proxies and vary data across capacity thresholds. If an amortized method predicts linear sequence total, record every operation and prefix sum, not only average latency.

Useful predeclared predictions include:

- exact operation count for controlled inputs;
- upper or lower envelope;
- slope over a scale where the asymptotic term should dominate;
- crossover from an explicit finite model;
- input family that triggers worst behavior;
- allocation, bytes, calls, depth, or retry count;
- invariants relating two counters;
- qualitative regime change near a threshold.

When a counter disagrees, inspect the mapping before fitting another coefficient. Hidden copies, library fallbacks, duplicate work, short-circuit branches, vector width, memoization, and runtime services can change the recurrence or primitive cost.

### Define treatments and one fair baseline

A **treatment** is a controlled variant whose effect is being studied: algorithm, representation, compiler flag, thread count, or configuration. Change one factor when making a causal attribution. If multiple factors must change as a package, claim only the package effect.

A fair baseline:

- implements the same contract;
- receives the same input instances in an order justified by the design;
- uses comparable compiler/runtime optimization and precision;
- includes or excludes setup by the same lifecycle rule;
- has access to the same preprocessing allowance;
- is not intentionally untuned or obsolete;
- records failures and resource exhaustion.

Compare against both a meaningful incumbent and, when useful, a simple reference. A sophisticated candidate beating a deliberately poor baseline says little.

### Define experimental units and sampling hierarchy

Measurements are often nested:

$$
\text{build}
\supset
\text{process}
\supset
\text{warm-up/steady-state phase}
\supset
\text{iteration}
\supset
\text{operation}.
$$

Iterations in one process share compiled code, heap history, cache state, address layout, and operating-system conditions. Treating them as independent can make uncertainty appear artificially small. The appropriate unit depends on the variation the conclusion targets.

If deployment starts a fresh process per job, process launches matter. If a service stays warm for weeks, steady-state requests matter but restarts and redeployments remain separate risk. If code generation or address layout changes per build, rebuilds may be an experimental level.

Use enough independently repeated upper-level units to estimate their variation. More inner iterations improve timing resolution but cannot manufacture independent replications.

### Separate setup, warm-up, and steady state

Setup may include parsing, allocation, index construction, data loading, compilation, cache population, and connection establishment. Decide whether the product pays it:

- include it for one-shot jobs;
- amortize it over a declared reuse count;
- report it separately for long-lived services;
- never include it for one treatment and exclude it for another without saying so.

Warm-up is not a ritual number of discarded iterations. Inspect mechanisms: JIT compilation, adaptive optimization, lazy linking, page faults, cache population, allocator growth, and frequency/thermal state. A regime may never stabilize, or the cold regime may be the product-relevant one.

Predeclare the warm-up rule. Report cold and warm results when both matter. Do not scan the data and discard an arbitrary prefix that makes the preferred treatment stable.

### Randomize or counterbalance order

Running all baseline trials before all candidate trials confounds treatment with time. Temperature, background load, battery/power state, cloud placement, caches, and data evolution may drift. Randomize treatment order with a recorded seed or use a counterbalanced schedule such as alternating which treatment runs first within pairs.

Randomization does not remove noise; it makes systematic association less likely and supports the intended inference. Blocking groups comparable units—same input, host, process generation, or time window—so paired analysis can remove shared variation.

One fixed seed supports exact replay of one schedule. Multiple independently sampled seeds support claims across randomized inputs or algorithmic randomness. Record both the seed-selection procedure and realized seeds.

### Prevent the benchmark from changing the work

Microbenchmarks are programs subject to optimization. A compiler or runtime may:

- constant-fold known inputs;
- eliminate unused results;
- hoist invariant work;
- inline away an abstraction;
- specialize on constant types or values;
- merge repeated operations;
- choose a fallback unlike production.

Consume results through a correctness-checked path and inspect generated behavior or counters when the risk is material. Keep timer calls outside the smallest operation if timer overhead dominates, but do not batch so aggressively that overflow, caching, or adaptation changes the workload.

Measure long enough for timer resolution, yet short enough to avoid unexamined thermal or system regime changes. Record clock semantics. Wall time, process CPU time, cycles, and service latency answer different questions.

### Choose inputs as part of the claim

Input size alone rarely describes difficulty. Record:

- distributions, ordering, duplicates, skew, and key width;
- sparsity, graph shape, locality, compression, and output size;
- adversarial and boundary families;
- real trace provenance, filtering, privacy, and drift;
- random generator and seed;
- preprocessing and cache state.

Use synthetic inputs to isolate mechanisms and representative inputs to estimate product behavior. Neither substitutes for the other. A real trace is one historical sample, not proof of future stationarity. An adversarial family establishes resilience only within its construction.

Avoid selecting workloads after seeing results. If exploration is necessary, label it exploratory and validate conclusions on held-out or newly generated cases.

### Select metrics that match the decision

Possible metrics include:

- comparisons, instructions, bytes, allocations, and I/O operations;
- total work and span;
- throughput, mean latency, median latency, and tail quantiles;
- peak live memory, retained memory, and cumulative allocation;
- energy, cost, failure rate, and output quality;
- startup, steady-state, update, and recovery time.

Throughput and latency can conflict under batching and queueing. A mean can hide a tail. A high percentile requires enough observations and a method that accounts for dependence. Peak memory and cumulative allocation are not interchangeable.

Prefer a small set of primary metrics declared before collection. Secondary diagnostics explain mechanisms. Optimizing many metrics/configurations and reporting only the winner creates selection bias.

### Summarize effects with direction and units

For lower-is-better time, speedup is commonly

$$
S=\frac{T_{\mathrm{baseline}}}{T_{\mathrm{candidate}}}.
$$

$S>1$ favors the candidate. Percent time reduction is

$$
R=100\frac{T_{\mathrm{baseline}}-T_{\mathrm{candidate}}}
{T_{\mathrm{baseline}}}\%.
$$

A candidate taking half the time has $S=2$ and $R=50\%$, not a $100\%$ time reduction. “Twice as fast” is often ambiguous; report the ratio and raw units.

For paired observations, inspect differences $d_i=b_i-c_i$ or ratios whose aggregation matches the scientific question. Ratio of arithmetic means, arithmetic mean of ratios, median ratio, and geometric mean of normalized ratios are not generally equal. Declare the convention.

Do not average raw times across unrelated benchmarks with different units of work. Normalize to a justified baseline and keep per-benchmark effects visible.

### Report variability and uncertainty honestly

For observations $y_1,\ldots,y_m$, the sample variance is

$$
s^2=\frac{1}{m-1}\sum_{i=1}^{m}(y_i-\bar y)^2
$$

when $m>1$. But inserting a formula does not make correlated samples independent or identically distributed. Plot or tabulate distributions, process-level variation, failures, and time order.

Confidence intervals, bootstrap intervals, or model-based intervals require assumptions and a sampling unit. State the method. A frequentist $95\%$ interval is produced by a procedure with long-run coverage under its assumptions; after observing one interval, it is not automatically a $95\%$ posterior probability that the fixed parameter lies inside.

Statistical significance is not practical importance. Report effect magnitude, uncertainty, resource trade-offs, and a decision threshold. Multiple configurations and repeated peeking increase false discovery risk; predeclare primary comparisons or adjust/validate them.

### Outliers and failures are data

Outliers may be measurement errors, interrupts, collection pauses, thermal throttling, contention, or the behavior users experience. Predeclare rules based on identifiable invalidity, not distance from a desired mean. Report results with and without a justified exclusion when sensitivity matters.

Timeouts, crashes, incorrect outputs, and resource exhaustion must not disappear from a latency average. Use censored/failure-aware reporting or mark the treatment invalid for the contract. A faster median among successful requests can conceal a worse success rate.

Retain raw observations and an exclusion log. Aggregates alone prevent later diagnosis.

### Executable evidence checks effect arithmetic, not performance

The following deterministic calculation uses five synthetic paired timings. It verifies descriptive arithmetic only.

<!-- bijux-verify: {"id":"paired-effect-arithmetic","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"pairs=5\nbaseline_mean=102.0\ncandidate_mean=83.0\nbaseline_median=102\ncandidate_median=83\nmean_paired_difference=19.0\nspeedup=1.229\nreduction_percent=18.6\n","stderr":""}} -->
~~~python
from statistics import mean, median


baseline = (105, 101, 99, 103, 102)
candidate = (84, 83, 82, 85, 81)
differences = tuple(
    baseline_time - candidate_time
    for baseline_time, candidate_time in zip(baseline, candidate, strict=True)
)

baseline_mean = mean(baseline)
candidate_mean = mean(candidate)
speedup = baseline_mean / candidate_mean
reduction = 100 * (1 - candidate_mean / baseline_mean)

print(f"pairs={len(baseline)}")
print(f"baseline_mean={baseline_mean:.1f}")
print(f"candidate_mean={candidate_mean:.1f}")
print(f"baseline_median={median(baseline)}")
print(f"candidate_median={median(candidate)}")
print(f"mean_paired_difference={mean(differences):.1f}")
print(f"speedup={speedup:.3f}")
print(f"reduction_percent={reduction:.1f}")
~~~

The values are invented and make no empirical claim. A real evaluation must preserve raw observations, units, sampling hierarchy, order, environment, failures, and uncertainty.

### Relate observed slopes to theory cautiously

If theory predicts $T(n)=c n^\alpha$, then

$$
\log T(n)=\log c+\alpha\log n.
$$

A log-log slope near $\alpha$ can be a diagnostic over a regime. It is not a proof of $\Theta(n^\alpha)$: startup terms, cache thresholds, limited range, correlated noise, and competing functions can mimic a slope. Use sizes spanning meaningful regimes and check modeled counters.

Normalize by a prediction, such as plotting $T(n)/(n\log n)$. Stabilization may support a correspondence hypothesis; systematic drift may reveal lower terms or model failure. Still report the finite domain.

### Investigate disagreement instead of averaging it away

When proof and measurement disagree, possible causes include:

- the implementation violates the analyzed recurrence;
- a primitive has size-dependent cost;
- input generation does not match the quantified case;
- setup or output dominates;
- compiler/runtime transformations change the work;
- memory hierarchy introduces a new regime;
- measurement order or environment is biased;
- counters are misconfigured or multiplexed;
- the correctness contract differs;
- the asymptotic regime is not reached.

Form hypotheses and collect discriminating evidence. Do not simply increase repetitions until an average resembles the expected line.

### Package evidence for exercise and reuse

A durable evaluation artifact should include:

- source revision and uncommitted-change status;
- build/run commands and scripts;
- compiler/interpreter/runtime and dependency versions;
- flags, environment variables, machine topology, OS/kernel, firmware/power settings when relevant;
- input generators, exact seeds, datasets, licenses, identities, and preprocessing;
- raw observations in a documented machine-readable format;
- analysis code that regenerates tables and figures;
- correctness checks and failure/exclusion records;
- expected duration/resource requirements;
- limitations and supported platforms.

ACM's current artifact policy distinguishes availability, evaluated functionality/reusability, and independently validated results. These are independent evidence properties. A link alone does not establish that an artifact runs or supports a claim, and a local self-check is not independent reproduction.

### Turn evidence into a bounded decision

An engineering decision should read like:

> For inputs $D$, sizes $N$, contract $C$, environment family $E$, and metric $M$, candidate $B$ met correctness checks and reduced the primary cost by estimated effect $R$ with uncertainty $U$, while changing secondary resources $V$. We choose $B$ subject to rollback and monitoring condition $K$.

State risks outside the sample: distribution drift, larger scales, platform changes, adversarial inputs, numerical changes, tail events, and maintenance cost. Define a reversal rule—for example, error, p99 latency, memory, or throughput crossing a threshold in a canary.

The decision may rationally reject a statistically clear microbenchmark improvement if it is operationally negligible or increases risk. It may accept a modest estimate when the change is reversible and monitoring is strong. Evidence informs judgment; it does not remove it.

## Definitions and Notation

- $b_i,c_i$: paired baseline and candidate observations in a shared unit.
- $m$: number of paired experimental units, not automatically the number of inner iterations.
- $\bar b,\bar c$: arithmetic sample means; $\bar d$: mean paired difference.
- $S=\bar b/\bar c$: ratio-of-means speedup for lower-is-better time.
- $R$: percent reduction relative to baseline.
- A **primary outcome** is the predeclared metric used for the main comparison.
- A **blocking factor** groups units sharing a source of variation.
- **steady state** is a defined regime supported by mechanism and evidence, not “late iterations” by default.
- A **raw observation** is retained before aggregation and linked to treatment, unit, time/order, input, and environment.
- An **exclusion rule** declares when an observation is invalid and how exclusion is reported.
- A **counterfactual** is the outcome that would have occurred for the same unit under another treatment; experimental design estimates contrasts without observing both simultaneously.
- A **reproduction package** is evidence material; external reproduction additionally requires another person/team and an applicable definition.

Use one direction convention consistently. For higher-is-better throughput, candidate/baseline may be natural; for lower-is-better time, baseline/candidate makes speedup above one favorable. Always label it.

## Mechanisms, Invariants, or Proof Structure

Use this evaluation worksheet:

1. **Decision and claim:** write the bounded conclusion and reversal criterion.
2. **Contract:** state semantic equivalence, errors, precision, side effects, and failures.
3. **Analysis:** derive expected counts, bounds, regimes, and model premises.
4. **Treatments:** define exact revisions/configurations and the factor being changed.
5. **Inputs:** predeclare sizes, distributions, boundaries, adversarial families, outputs, and provenance.
6. **Experimental units:** identify builds, hosts, processes, runs, requests, and nested repetitions.
7. **Controls:** balance setup, preprocessing, flags, resources, and environment.
8. **Order:** randomize or counterbalance and record procedures/seeds.
9. **Regimes:** define cold, warm-up, steady-state, teardown, failure, and recovery handling.
10. **Metrics:** declare primary/secondary resources, units, timers, counters, and quality measures.
11. **Correctness gate:** run oracles, properties, differential checks, and retained failures.
12. **Collection:** preserve raw data, timestamps/order, logs, versions, and exclusions.
13. **Analysis:** report per-unit effects, summaries, uncertainty, sensitivity, and multiplicity policy.
14. **Correspondence:** compare counters, slopes, thresholds, and failures with model predictions.
15. **Artifacts:** package commands, code, data, environments, analysis, and limitations.
16. **Decision:** state scope, effect, uncertainty, trade-offs, monitoring, and rollback.

The durable invariant is evidential traceability: every conclusion points to a contract, claim type, procedure, raw observation or proof step, analysis transformation, and explicit scope.

## Alternatives and Trade-Offs

**Proof versus measurement.** Proof covers all cases represented by premises; measurement covers concrete cases with physical detail. Combine them by testing correspondence, not by asking one to replace the other.

**Operation counters versus wall time.** Counters can isolate algorithmic mechanisms and be deterministic. Wall time captures end-to-end effects but is noisy and confounded. Use both when the decision connects a mechanism to user-observed cost.

**Microbenchmark versus application benchmark.** Microbenchmarks isolate a primitive and support diagnosis. Applications preserve interactions and relevance. A layered evaluation uses the former to explain and the latter to validate impact.

**Synthetic versus trace inputs.** Synthetic families control shape and expose boundaries. Traces represent one historical workload but include confounders and drift. Report both scopes rather than calling either “realistic” without evidence.

**Cold versus steady state.** Cold measurements matter for one-shot tools and autoscaled instances; steady state matters for long-lived services. Separating them is more informative than declaring one correct.

**Paired versus unpaired design.** Pairing can remove input/host variation when units genuinely correspond, but order/carryover must be controlled. Independent groups avoid carryover but often need more units.

**Mean versus median versus quantile.** The mean supports additive capacity accounting, the median describes a central request, and tails reflect service risk. The workload and decision select the statistic.

**Fixed environment versus platform sample.** Tight control improves causal isolation on one setup. Sampling machines/regions/versions supports broader generalization at higher cost. Do not generalize beyond the sampled level.

**Full reproducibility versus practical cost.** Capturing containers, data, and scripts helps, but proprietary hardware, large datasets, or long runs can limit portability. Document faithful smaller checks without claiming they reproduce the full result.

## Failure Modes and Misconceptions

1. **“Correctness tests slow the benchmark, so omit them.”** Validate outside timed regions and consume results safely.
2. **“Equal output length means equal semantics.”** Values, order, stability, precision, and side effects still matter.
3. **“The theorem predicts seconds.”** It predicts a modeled resource under premises.
4. **“A timing curve proves Big-O.”** A finite range cannot prove an eventual universal bound.
5. **“More inner iterations mean more independent samples.”** Shared process and environment state induce dependence.
6. **“Always discard the first ten runs.”** Warm-up needs a mechanism and predeclared regime rule.
7. **“Always take the minimum.”** It suppresses variability and changes the estimand.
8. **“Outliers are noise.”** They may be failures, pauses, contention, or real tail behavior.
9. **“Run baseline first for fairness.”** Fixed order can confound treatment with drift.
10. **“One seed is enough for randomized performance.”** It supports replay, not inference across randomness.
11. **“The compiler executes the source literally.”** It may remove, hoist, inline, or specialize benchmark work.
12. **“Setup never belongs in timing.”** One-shot and lifecycle decisions may pay it.
13. **“The mean describes user latency.”** Queueing and tails can dominate experience.
14. **“A small p-value means a useful speedup.”** Practical magnitude and costs remain.
15. **“No significant difference means equivalence.”** Equivalence needs a margin and appropriate design.
16. **“Average the benchmark times.”** Unrelated workloads need justified normalization and visible per-case effects.
17. **“Drop timeouts before computing latency.”** This rewards failure and biases the result.
18. **“Performance counters identify causes automatically.”** Events can be proxies, multiplexed, or misattributed.
19. **“A public repository is a reproduced result.”** Availability, exercisability, and independent validation differ.
20. **“The benchmark winner should ship.”** Correctness, risk, maintenance, rollback, and production objectives still govern.

## Worked Examples

### Example 1

**Question:** A new search returns the right index on sampled inputs and is twice as fast. What remains unproved?

**Reasoning:** Sampled equality does not prove the first-occurrence contract, termination, mutation frame, or all boundaries. Timing does not prove asymptotic cost, and speed scope lacks inputs/environment/statistic.

**Conclusion:** Separate correctness, analytical, correspondence, empirical, and deployment claims before accepting the result.

### Example 2

**Question:** Analysis predicts exactly $2n-1$ comparisons, but instrumentation reports $3n+O(1)$. What should happen?

**Reasoning:** Inspect whether validation, comparator wrappers, duplicate checks, or library calls add comparisons and whether the counter maps one-to-one to the modeled primitive. More timing repetitions cannot repair correspondence.

**Conclusion:** Revise the implementation or recurrence before interpreting its performance.

### Example 3

**Question:** Synthetic paired means are $102$ ms and $83$ ms. What are speedup and reduction?

**Reasoning:** $S=102/83\approx1.229$. Reduction is $100(1-83/102)\%\approx18.6\%$.

**Conclusion:** Report both direction and raw means; the arithmetic alone carries no uncertainty or causal claim.

### Example 4

**Question:** Why can discarding exactly ten warm-up iterations be wrong?

**Reasoning:** Compilation may finish earlier, later, repeatedly, or never; a cold-start product may care about those iterations. Cache, allocator, and thermal regimes can move independently.

**Conclusion:** Define warm-up from mechanisms and decision scope, then retain evidence for the chosen boundary.

### Example 5

**Question:** A baseline always runs in the morning and a candidate in the afternoon. Can 1000 samples fix the design?

**Reasoning:** Treatment is confounded with time and any correlated load, power, or temperature drift. More observations repeat the same bias.

**Conclusion:** Interleave, randomize, or block order; sample count cannot undo systematic confounding.

### Example 6

**Question:** A microbenchmark's result is unused and its measured loop nearly vanishes at optimization level three. Why?

**Reasoning:** The compiler may prove the computation has no observable effect and eliminate or hoist it. The benchmark no longer represents production work.

**Conclusion:** Consume and validate results, inspect mechanism evidence, and keep benchmark scaffolding from dominating.

### Example 7

**Question:** A hash algorithm is fast on uniform keys but stalls on one collision family. What should the report say?

**Reasoning:** The uniform experiment estimates one distribution; the collision case is a counterexample to a universal claim and may represent a security/adversary risk. Expected and worst-case guarantees differ.

**Conclusion:** Report both scopes and the hash/adversary assumptions instead of averaging them together.

### Example 8

**Question:** Is a p99 latency estimate trustworthy after 100 requests?

**Reasoning:** The nominal 99th percentile lies at the extreme order statistic with almost no tail resolution, and dependence/queueing may reduce effective information further.

**Conclusion:** Use a sample/design adequate for the tail decision, report uncertainty and failures, and avoid false precision.

### Example 9

**Question:** A finite model predicts a crossover at $n=32768$, but measured order flips near $n=80000$. Is theory disproved?

**Reasoning:** The asymptotic dominance may remain correct while coefficients, startup terms, cache thresholds, or primitive mappings differ. Instrument counts and fit/validate coefficients on held-out sizes.

**Conclusion:** The disagreement rejects the calibrated finite model, not automatically the asymptotic theorem.

### Example 10

**Question:** A candidate improves warm median latency by $8\%$ but doubles cold startup and peak memory. Should it deploy?

**Reasoning:** The answer depends on service lifetime, autoscaling frequency, memory limit, tail behavior, effect uncertainty, and rollback. One metric cannot decide.

**Conclusion:** Apply a predeclared multi-resource decision rule and validate with a monitored canary.

## Cross-Program Connections

- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns test design, oracles, statistical testing, performance testing, and quality evidence.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns canaries, SLOs, production telemetry, capacity, rollback, and reliability decisions.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns hardware counters, caches, pipelines, branch behavior, frequency, and topology.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) owns scheduling, virtual memory, timers, resource isolation, and process behavior.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns synchronization, parallel speedup, contention, and nondeterministic execution.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns provenance, data pipelines, data-quality controls, and reproducible transformation of measurement datasets.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Mathematical algorithm analysis, model assumptions, and experimental context.
2. Raj Jain. *The Art of Computer Systems Performance Analysis*. Wiley, 1991. Experimental design, metrics, measurement, simulation, and statistical interpretation for computer systems.
3. Andy Georges, Dries Buytaert, and Lieven Eeckhout. [“Statistically Rigorous Java Performance Evaluation”](https://doi.org/10.1145/1297027.1297033), *OOPSLA 2007*, pp. 57–76. Managed-runtime warm-up, nondeterminism, repetition, and statistical methodology.
4. Tomas Kalibera and Richard E. Jones. [“Rigorous Benchmarking in Reasonable Time”](https://doi.org/10.1145/2464157.2464160), *ISMM 2013*, pp. 63–74. Hierarchical variation, experimental repetitions, and uncertainty-aware benchmarking.
5. Todd Mytkowicz, Amer Diwan, Matthias Hauswirth, and Peter F. Sweeney. [“Producing Wrong Data Without Doing Anything Obviously Wrong!”](https://doi.org/10.1145/1508244.1508275), *ASPLOS 2009*, pp. 265–276. Primary evidence on measurement bias and setup randomization.
6. Torsten Hoefler and Roberto Belli. [“Scientific Benchmarking of Parallel Computing Systems”](https://doi.org/10.1145/2807591.2807644), *SC 2015*, Article 73, pp. 1–12. Experimental design, statistics, reporting, and reproducibility for parallel performance.
7. Association for Computing Machinery. [“Artifact Review and Badging, Version 1.1”](https://www.acm.org/publications/policies/artifact-review-and-badging-current), current policy checked 2026-09-04. Official distinctions among artifact availability/evaluation and independently validated results.
8. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for empirical and relative measurement, input size, primitive operations, and time/space analysis.

## Exercises

### Exercise 1

Classify each claim as primarily requiring proof, executable/correctness evidence, controlled measurement, or operational evidence: (a) a loop returns the maximum for every nonempty array; (b) a concrete run made 999 comparisons; (c) comparison maximum needs at least $n-1$ comparisons; (d) candidate p95 latency is lower on a stated workload; (e) the candidate should replace the incumbent.

### Exercise 2

For paired millisecond observations baseline $(120,100,110,130)$ and candidate $(90,95,100,105)$, compute means, paired differences, ratio-of-means speedup, and percent time reduction. State what cannot be concluded from four pairs.

### Exercise 3

Design an evaluation comparing linear and binary search. Specify contracts, input families, experimental units, setup, correctness checks, counters, timing metrics, order controls, and predictions.

### Exercise 4

Diagnose this study: one process warms the candidate for 1000 iterations, then measures it 10000 times; a fresh process measures the baseline once including file loading; the fastest candidate value is compared with the baseline value; incorrect candidate outputs and two timeouts are removed.

### Exercise 5

An unfamiliar deduplication service can use exact sorting or a probabilistic filter followed by verification. Design a proof-and-measurement evaluation covering correctness/error, expected and worst cost, data distributions, memory, throughput, tail latency, failures, reproducible artifacts, and a bounded deployment decision.

## Answers to the Exercises

### Answer 1

(a) The universal functional claim primarily requires a proof from the contract, though tests and executable checks can find defects. (b) The one-run count requires executable instrumentation with a validated counter mapping and environment record. (c) The problem lower bound requires a comparison-model proof such as the candidate-elimination adversary. (d) The finite p95 comparison requires a controlled experiment with enough appropriate units, a percentile/uncertainty method, and workload/environment scope. (e) Replacement is an operational decision combining all earlier evidence with secondary resources, maintainability, rollout, monitoring, and rollback.

No category is isolated: correctness gates precede timing, counters test proof correspondence, and operational evidence cannot repair a contract violation.

### Answer 2

The baseline mean is

$$
\bar b=(120+100+110+130)/4=115.
$$

The candidate mean is

$$
\bar c=(90+95+100+105)/4=97.5.
$$

Paired differences are $(30,5,10,25)$ with mean $\bar d=17.5$ ms. Ratio-of-means speedup is

$$
S=115/97.5\approx1.179,
$$

and time reduction is

$$
R=100(1-97.5/115)\%\approx15.2\%.
$$

Four pairs do not establish independence, representativeness, causality, precision, tail behavior, correctness, asymptotic growth, or production impact. We also need the pairing factor, order, raw units, setup/warm-up policy, failures, environment, and an uncertainty analysis appropriate to the experimental units.

### Answer 3

Use one contract—for example, return the first matching index or $-1$ without mutation. Validate both implementations against an independent oracle on empty, singleton, duplicates, absent targets, first/last matches, and malformed inputs.

Choose sorted arrays for binary search; either give linear search the same sorted arrays or clearly make input representation a treatment. Cross sizes over powers and cache thresholds. Include present positions, absence, duplicate runs, and key-width/distribution families. Predict linear comparisons by target position and logarithmic binary-search comparisons; instrument actual key comparisons and visited indices.

Generate inputs outside timed regions unless generation belongs to the product decision. Pair treatments on the same immutable input, randomize which runs first, separate cold and steady-state regimes, and repeat across independent processes if process/runtime variation is in scope. Consume and validate results outside timing. Record source, toolchain, flags, machine, OS, seeds, data identities, raw per-unit observations, setup, and exclusions.

Report comparison counts first to test correspondence, then latency/throughput distributions and uncertainty. Do not infer asymptotic classes from timings alone. Investigate crossover differences through key-comparison cost, branches, caches, and setup.

### Answer 4

The treatments are not comparable. Candidate warm-up is excluded while baseline startup and file loading are included. Candidate has 10000 correlated inner observations while baseline has one fresh-process unit. Taking the fastest candidate changes the estimand and hides variability. Fixed treatment/process order permits drift and environment confounding. Removing incorrect outputs rewards semantic failure; removing timeouts biases latency and reliability.

Redesign with the same contract and retained correctness gate; balance file loading/setup according to one lifecycle policy; use comparable fresh-process or steady-state units; define warm-up mechanistically for both; randomize/counterbalance order; preserve all raw observations, failures, and timeouts; summarize the same statistic; and report uncertainty at the independent-unit level. If the candidate remains incorrect, it is not a valid performance treatment.

### Answer 5

Define exact deduplication semantics first: key equality, retained representative/order, streaming versus batch output, false-positive/negative policy, mutation, and failure/retry behavior. Exact sorting can be proved correct under its comparator and analyzed as $O(n\log n)$ comparisons plus movement/output. A probabilistic filter must specify false-positive probability, whether verification removes false positives, seed/hash assumptions, adversary visibility, and whether any false negative is possible. If all positives are verified and the filter has no false negatives under its model, prove the composed exact result.

Instrument comparisons, hashes, filter probes, verification candidates, bytes moved, allocations, peak memory, spills, retries, and outputs. Predeclare sizes, duplicate ratios, skew, key width, ordered/random/adversarial keys, memory pressure, and real trace provenance. Sample independent processes/hosts or long-lived service windows according to deployment, randomize treatment order, capture seeds, and separate build/cold/steady/recovery costs.

Report throughput, latency distribution including tails/timeouts, peak memory, output quality/error intervals, and failure rate. Test hash-collision and saturation families, malformed inputs, restarts, partial state, and resource exhaustion. Package exact revisions, dependencies, commands, generators/data identities, raw observations, analysis, correctness checks, and limitations.

Deploy only within the sampled environment/workload if the chosen option meets the exact/error contract and predeclared thresholds for throughput, tail latency, memory, and failure. Use a canary, monitor duplicate escapes/filter saturation/distribution drift, and retain rollback. The decision should reverse when any contract or resource threshold is crossed.
