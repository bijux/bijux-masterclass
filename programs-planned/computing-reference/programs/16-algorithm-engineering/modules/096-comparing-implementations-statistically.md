---
module_id: ALGE-096
program: Algorithm Engineering
level: 2
module_number: 96
title: Comparing Implementations Statistically
status: complete
last_verified: 2026-09-05
---

# Comparing Implementations Statistically

## One-Page Review

### Governing question

How do we compare algorithm implementations using a statistical analysis that matches the experiment, preserves pairing and hierarchy, reports practical magnitude and uncertainty, and remains honest about population and model assumptions?

### Essential definitions

- An **estimand** is the population quantity the comparison seeks, such as mean paired latency difference over workload-machine sessions.
- An **estimate** is its value computed from observed data.
- An **effect size** expresses magnitude in natural or standardized terms.
- A **confidence interval** is produced by a procedure with stated repeated-sampling coverage under assumptions; it is not a posterior probability about one fixed parameter.
- A **paired design** observes treatments within matched blocks; an **independent design** samples separate units.
- A **permutation/randomization test** compares an observed statistic with assignments allowed by the null and design.
- **multiplicity** arises when many algorithms, workloads, metrics, or hypotheses create multiple selection opportunities.
- **practical significance** evaluates an effect against costs, risks, and a predeclared meaningful threshold.

### Central model, mechanism, or theorem

For paired observations, define $D_b=Y_{b,B}-Y_{b,A}$ so positive values favor A when lower is better. The estimated mean effect is

$$
\bar D=\frac{1}{n}\sum_{b=1}^{n}D_b.
$$

Pairing retains shared block conditions and analyzes $n$ contrasts rather than pretending $2n$ independent observations. Uncertainty must reflect the sampled assignment units and population. A test against zero does not answer whether $|D|$ exceeds a practically meaningful threshold $\delta$.

### Critical invariants

- The analysis follows the frozen benchmark, workload, tuning, exclusion, and stopping protocols.
- Correctness failures, timeouts, and censored observations remain visible.
- The statistical unit matches treatment assignment; inner iterations are not promoted to independent replicas.
- Paired data remain paired, hierarchy remains identified, and missing pairs are handled under a declared rule.
- Effect direction, units, denominator, aggregation, and weighting are explicit.
- Assumptions are checked with domain reasoning and diagnostics, not accepted from a test name.
- All planned comparisons and exploratory searches are disclosed.
- Conclusions remain bounded to sampled workloads, seeds, machines, sessions, and time.

### Common failures

Running an unpaired test on paired data; treating thousands of loop timings as $n$; testing log values but reporting an unrelated arithmetic effect; declaring “equal” after failure to reject; reporting only p-values; interpreting a 95% confidence interval as 95% probability; averaging percentages with incompatible denominators; using geometric means with zero or negative values; deleting timeouts or outliers; selecting the best benchmark subset; ignoring multiplicity; choosing a test after inspecting which one gives a desired result; and generalizing from one host to a platform population.

### Compact example

Across four matched sessions, baseline/candidate times are 10/8, 20/17, 30/29, and 40/36 ms. Baseline-minus-candidate differences are 2, 3, 1, and 4 ms, so $\bar D=2.5$ ms. The aggregate ratio is $(25-22.5)/25=10\%$, while the mean of pairwise percentage reductions is about 12.1%. Both are computable; they estimate different weighted quantities.

### Connections

[ALGE-092](./092-benchmark-design-and-reproducibility.md) supplies the assignment design, [ALGE-093](./093-profiling-time-memory-and-i-o.md) explains mechanisms, and [ALGE-095](./095-parameter-tuning-without-overfitting.md) freezes configurations before comparison. ALGE-097 next builds portfolios when effects vary predictably by instance.

## Governing Question

For a frozen pair or set of implementations, what effect, uncertainty, and decision rule are justified by the observed experimental units, dependencies, failures, and target population?

## Why This Matters

Performance observations vary across workloads, process states, machines, and time. Statistics compress that variation, but compression can discard the structure that made the experiment credible. A narrow interval based on ten thousand correlated iterations is worse than a wider interval based on honestly identified sessions.

The goal is a decision, not a ritual threshold. An implementation can be measurably faster yet operationally irrelevant; another can have uncertain mean benefit but eliminate catastrophic tails. Statistical analysis must sit beside correctness, resource limits, mechanism evidence, and the costs of change.

## Prerequisites and Retrieval

Retrieve expected-cost reasoning from [ALGE-006](./006-best-worst-expected-and-amortized-cost.md), empirical scope from [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md), representative weights from [ALGE-091](./091-representative-workload-construction.md), blocking and run hierarchy from [ALGE-092](./092-benchmark-design-and-reproducibility.md), profile attribution from [ALGE-093](./093-profiling-time-memory-and-i-o.md), adversarial panels from [ALGE-094](./094-adversarial-and-pathological-inputs.md), and clean selection from [ALGE-095](./095-parameter-tuning-without-overfitting.md).

## Learning Objectives

After this module, you should be able to:

1. define an estimand, experimental unit, effect direction, and practical threshold;
2. preserve paired, blocked, nested, repeated, and censored structure;
3. report natural-unit, relative, ratio, and stochastic-superiority effects appropriately;
4. choose and qualify parametric, bootstrap, permutation, rank, and hierarchical analyses;
5. distinguish confidence, compatibility, evidence, practical importance, equivalence, and non-inferiority;
6. handle multiple algorithms, workloads, metrics, and exploratory analyses transparently;
7. diagnose sensitivity to weighting, transformations, exclusions, and dependence; and
8. turn statistical output into a bounded engineering decision with replication needs.

## Core Exposition

### Define the estimand and decision threshold

Write the population, unit, metric, treatment contrast, and aggregation. “Mean runtime difference across target-weighted workload-machine sessions” differs from “median per-workload speed ratio” and “probability candidate beats baseline on a randomly selected workload.” None is universally primary.

Choose a smallest effect of practical importance $\delta$ before viewing the final comparison. It can reflect latency budgets, capacity, energy, migration cost, or risk. For lower-is-better time and $D=B-A$, superiority might require $D>\delta$; non-inferiority might require $D>-m$ for margin $m$ while candidate improves another constraint.

### Preserve design structure

If A and B run in the same workload-machine-session block, compute paired contrasts. Blocking cancels shared additive conditions and makes heterogeneity visible. If treatments run on different independent machines, use an independent design. Clustered observations from one tenant, graph, process, or machine require aggregation or a hierarchical model matching assignment.

Inner iterations estimate within-run behavior. Process repetitions estimate startup/layout variation. Machine repetitions support cross-machine inference. Increasing inner loops improves timing precision but does not create new machines. Record missing pairs and why; complete-case analysis assumes something about their missingness.

### Inspect raw data before compressing

Plot observations, paired connections, contrasts, order, workload features, and failures. Check skew, multimodality, variance changes, trends, warm-up, ceiling/timeout censoring, and influential units. Diagnostics do not license outcome-based deletion; they reveal model limits and planned sensitivity analyses.

Show sample counts at every hierarchy. A box plot can hide pairing and small $n$; a bar with standard error can hide distributions. Preserve raw or granular machine-readable evidence so summaries can be recomputed.

### Report effects in decision units

Natural-unit differences are often easiest to value. Relative reduction uses a named denominator, such as $(B-A)/B$. A ratio $A/B$ is positive and multiplicative, but reciprocal direction changes interpretation. Log ratios make reciprocals symmetric: $\log(A/B)=-\log(B/A)$.

Aggregate ratios only with a defined weighting. Ratio of arithmetic means weights units by baseline magnitude; mean per-unit percentage weights units equally; geometric mean ratio estimates a multiplicative center for positive ratios. Zero, negative, timeout, or failed values require another method, not an arbitrary epsilon.

### Quantify uncertainty at the right unit

An interval procedure should resample or model independent assignment units. For paired bootstrap, resample complete blocks with replacement and recompute the full statistic, including target weights. A hierarchical bootstrap resamples machines, then workloads or sessions within machines when that matches population sampling.

Small samples and heavy tails challenge normal approximations. Bootstrap intervals also have assumptions and can behave poorly with very small $n$, extreme statistics, or dependent data. Report the method, seed, repetitions, interval type, and limitations. Analytical models are strong when their premises and variance structure fit.

### Use randomization tests through the design

Under a sharp paired null with exchangeable treatment labels, signs of paired differences can be flipped. Enumerate all $2^n$ sign assignments for small $n$ or sample them reproducibly for large $n$. The p-value is the fraction whose statistic is at least as extreme under the prespecified rule.

Exchangeability is a substantive condition. Carryover, fixed order, missingness, unequal treatment state, or a null about distributions rather than fixed unit outcomes may invalidate simple sign flips. A randomization test must mirror the actual assignment scheme.

### Execute an exact paired illustration

The reference reports paired magnitude and an exact two-sided sign-randomization p-value for four blocks. The coarse p-value illustrates why tiny $n$ cannot yield arbitrary evidence.

<!-- bijux-verify: {"id":"paired-comparison-reference","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"differences_ms: [2, 3, 1, 4]\nmean_difference_ms: 2.5\nmedian_difference_ms: 2.5\naggregate_reduction_percent: 10.0\nmean_pair_reduction_percent: 12.1\nexact_two_sided_sign_p: 0.125\n","stderr":""}} -->
```python
from itertools import product
from statistics import mean, median


pairs = [(10, 8), (20, 17), (30, 29), (40, 36)]  # baseline, candidate
differences = [baseline - candidate for baseline, candidate in pairs]
observed = abs(mean(differences))
null_statistics = [
    abs(mean(sign * difference for sign, difference in zip(signs, differences)))
    for signs in product([-1, 1], repeat=len(differences))
]
p_value = sum(value >= observed for value in null_statistics) / len(null_statistics)
aggregate = 100 * (mean(b for b, _ in pairs) - mean(c for _, c in pairs)) / mean(b for b, _ in pairs)
pair_percent = mean(100 * (b - c) / b for b, c in pairs)
print("differences_ms:", differences)
print("mean_difference_ms:", mean(differences))
print("median_difference_ms:", median(differences))
print("aggregate_reduction_percent:", round(aggregate, 1))
print("mean_pair_reduction_percent:", round(pair_percent, 1))
print("exact_two_sided_sign_p:", p_value)
```

The result is not “no effect”: the observed mean is 2.5 ms. Under the exact sign-flip model, only two of sixteen assignments are at least as extreme, giving 0.125. With four blocks the test is coarse and uncertainty about the target population remains large.

### Understand p-values narrowly

A p-value measures compatibility of data and a specified model through a chosen statistic. It is not the probability that the null is true, the probability results are chance, or the magnitude/importance of the effect [6]. Threshold crossing does not repair design bias or multiplicity.

Report the exact value with effect and interval when a test is useful. A large p-value can reflect small effect, high noise, small sample, or a poor statistic. “No statistically detected difference” is not equivalence. Equivalence requires a predeclared region and evidence excluding effects outside it.

### Choose tests by assumptions and estimand

A paired t procedure targets a mean contrast under conditions supporting its sampling model. Rank or sign procedures target different functionals and assumptions; they are not assumption-free replacements. Welch-style independent comparisons address unequal variance for independent groups but discard legitimate pairing if misapplied.

Permutation methods are exact relative to their assignment/exchangeability model. Bootstrap methods approximate sampling variation under their resampling scheme. Bayesian models can express posterior uncertainty given likelihood and prior. Select through the question and design, document decisions before outcomes, and perform sensitivity analyses where plausible models differ.

### Address heterogeneity

An overall mean can hide reversals. Report effects by predeclared workload strata, size, machine, and relevant mechanisms. Model interactions when evidence supports them. Avoid declaring a universal winner when one algorithm dominates small sparse graphs and another large dense graphs.

Target weights determine an aggregate. Show sensitivity to plausible weight changes. A forest-style display of per-stratum effects and uncertainty is often more informative than one score. Heterogeneity may motivate the portfolio in ALGE-097, but that selector requires fresh evaluation.

### Handle failures and censoring

Wrong answers make a configuration infeasible unless the decision explicitly permits an error-quality trade. Timeouts reveal runtime above a threshold; out-of-memory reveals a resource failure. Dropping them selects survivors. Report failure probabilities and use failure-aware, censored, or lexicographic decisions as predeclared.

A two-stage rule can require zero correctness violations, then compare successful performance, but finite testing cannot prove zero population failures. Sensitivity to timeout assignment and competing failure types should be visible. Do not invent exact times beyond censoring limits.

### Govern multiplicity and selection

Thirty workloads, five metrics, four implementations, and many parameter settings create many possible stories. Identify primary comparisons and outcomes before analysis. Adjustment procedures control particular error notions under assumptions; they do not turn exploratory selection into confirmation automatically.

Report the full family, exclusions, and all material outcomes. Hierarchical questions or simultaneous intervals may fit the design. Exploratory findings generate new hypotheses for independent evidence. The tuned winner from ALGE-095 must be frozen before this comparison.

### Validate robustness of the conclusion

Recompute under justified alternatives: natural-unit and ratio effects, target weights, robust summaries, inclusion of censored lower bounds, planned outlier rules, and hierarchical versus aggregated units. A conclusion that reverses under plausible choices is itself a result.

Use profile evidence to see whether the measured effect matches the proposed mechanism. Replicate across new workloads, sessions, machines, or time when the intended claim spans them. Reproduction under one environment strengthens a scoped claim, not universal superiority.

### Make the decision explicit

Combine correctness, effect magnitude, uncertainty, tails, resources, adversarial behavior, operational cost, and reversibility. Possible outcomes include adopt, reject, gather more evidence, restrict to a regime, or deploy behind a guard. State the loss of each error.

Publish the analysis code, environment, raw run ledger, estimand, models, seeds, diagnostics, deviations, and limitations. Statistical fluency is not a substitute for a defensible experimental protocol; it makes the protocol’s evidence legible.

## Definitions and Notation

Let $Y_{b,A}$ and $Y_{b,B}$ be lower-is-better observations in block $b$, $D_b=Y_{b,B}-Y_{b,A}$, $\theta=E[D]$ the target mean contrast, $\hat\theta=\bar D$ its estimate, and $\delta$ the smallest practical benefit. Let $R_b=Y_{b,A}/Y_{b,B}$ be a positive ratio when defined.

A **null model** specifies data/assignment behavior under a hypothesis. **Coverage** is the long-run property of an interval procedure. **Power** is probability of a defined rejection under a specific alternative. **Equivalence margin** bounds differences considered practically interchangeable. **Sensitivity analysis** evaluates dependence on plausible analytical choices.

## Mechanisms, Invariants, or Proof Structure

### Pairing argument

Under $Y_{b,t}=\mu_t+\beta_b+\epsilon_{b,t}$, the paired contrast cancels additive block effect $\beta_b$. An unpaired analysis includes between-block variation and loses matching. Pairing does not cancel treatment-by-block interaction; the distribution of $D_b$ exposes it.

### Exact sign enumeration

For $n$ paired differences and an exchangeable sharp null, each of $2^n$ sign vectors represents an allowed assignment. The exact p-value counts statistics at least as extreme as observed, including the observed assignment. With $n=4$, attainable two-sided tail probabilities are coarse; no asymptotic approximation changes the information content.

### Ratio non-equivalence

In general, $\frac{\bar B-\bar A}{\bar B}$ is not equal to $\frac{1}{n}\sum_b\frac{B_b-A_b}{B_b}$. The first weights absolute contributions through aggregate baseline; the second weights units equally. Neither is wrong without an estimand, but substituting one for the other changes the question.

## Alternatives and Trade-Offs

| Method | Targets/uses | Strength | Main risk |
|---|---|---|---|
| paired mean model | mean contrast | direct natural units | tail/model sensitivity |
| paired sign/rank method | signs/ranks | resistant to magnitudes | different estimand, ties |
| randomization test | assignment null | design-based logic | exchangeability/carryover |
| block bootstrap | sampling distribution | flexible statistic | small-$n$/dependence limits |
| hierarchical model | nested variation | partial pooling, transfer | model complexity |
| ratio/geometric summary | multiplicative effect | scale comparison | positivity/weighting |
| equivalence/non-inferiority | margin decision | matches bounded question | margin justification |
| descriptive report | observed units | minimal assumptions | limited generalization |

Use the simplest analysis that preserves the design and answers the estimand; add methods only when they illuminate a real uncertainty.

## Failure Modes and Misconceptions

- **“Each iteration is a sample.”** Independence follows assignment and population, not row count.
- **“Paired and unpaired tests are interchangeable.”** They encode different designs and variance.
- **“A p-value is the chance the null is true.”** It is computed assuming a specified null model.
- **“$p>0.05$ proves equality.”** Absence of rejection is not equivalence evidence.
- **“95% CI means 95% probability for this interval.”** Frequentist coverage concerns repeated procedures.
- **“Percent faster is symmetric.”** Denominator and direction matter.
- **“Geometric mean is always right.”** It needs positive ratios and a multiplicative estimand.
- **“Nonparametric means assumption-free.”** Exchangeability, independence, and target functional still matter.
- **“Multiplicity correction validates exploration.”** It controls a named error notion, not hidden selection.
- **“Statistics generalize beyond the sample automatically.”** Population sampling and design define scope.

## Worked Examples

### Example 1

**Situation.** Four paired differences are 2, 3, 1, and 4 ms.

**Reasoning.** Mean and median are both 2.5 ms. These describe the observed blocks; uncertainty and population scope require the sampling/assignment design.

**Conclusion.** Lead with the natural-unit paired effect.

### Example 2

**Situation.** A loop records 100 timings in each of two processes and an analyst uses $n=200$.

**Reasoning.** Treatment assignment and important state are process-level, so the independent sample may be two processes, with inner timings nested. More process/session/machine replications are required.

**Conclusion.** Pseudo-replication fabricates precision.

### Example 3

**Situation.** The aggregate reduction is 10%, while mean pair reduction is 12.1%.

**Reasoning.** Aggregate reduction weights large baseline times more; mean pair percentage weights blocks equally. Select based on whether total work or a random block is the target.

**Conclusion.** Different percentage summaries answer different questions.

### Example 4

**Situation.** A 95% interval for benefit is [-1, 6] ms and $p=0.12$ against zero.

**Reasoning.** The data/model remain compatible with small harm and material benefit. This is not proof of equality. Compare the interval with the practical margin and decide whether more units are worth collecting.

**Conclusion.** Inconclusive evidence should produce an explicit decision, not a false binary.

### Example 5

**Situation.** An interval is [0.1, 0.4] ms with tiny p-value, but $\delta=2$ ms.

**Reasoning.** Evidence supports a small positive mean under the model, yet the entire interval is below practical importance. Operational costs may dominate.

**Conclusion.** Statistical detectability is not engineering value.

### Example 6

**Situation.** Candidate times out on two large workloads; the analyst compares only completed pairs.

**Reasoning.** Missingness depends on treatment performance. Report timeouts as censored/failure outcomes and use the predeclared decision rule. Completed-case speed is conditional on survival.

**Conclusion.** Failure-aware comparison prevents survivor bias.

### Example 7

**Situation.** Candidate wins nine small workloads and loses one large workload that carries 60% of production work.

**Reasoning.** A win count weights workloads equally and ignores magnitude. Compute target-weighted effects and report strata; check capacity and tail consequences.

**Conclusion.** Population weights can reverse a majority-of-benchmarks story.

### Example 8

**Situation.** Twenty metrics are explored and one has $p=0.03$.

**Reasoning.** The chosen result is selected from a family. Disclose all metrics, distinguish the prespecified primary outcome, apply a justified family procedure if confirmatory, and validate exploration on new evidence.

**Conclusion.** The selection path belongs in the statistical model and report.

### Example 9

**Situation.** A paired sign-flip test is used despite always running A before B.

**Reasoning.** If time trend or carryover changes B, treatment labels are not exchangeable within blocks. Redesign with randomized/counterbalanced order or model credible order effects; arithmetic enumeration cannot repair assignment.

**Conclusion.** Exact computation is only exact under the design premises.

### Example 10

**Situation.** Mean benefit is positive, but effects reverse by graph density.

**Reasoning.** Report the interaction and predeclared strata. If density is observable before choice, propose a selector and evaluate the entire new policy on untouched workloads. Do not retrofit it to the same data.

**Conclusion.** Heterogeneity can motivate a portfolio, not a universal-winner claim.

## Cross-Program Connections

- [Data Structures Engineering DSE-010](../../17-data-structures-engineering/modules/010-benchmarking-a-structure-without-misleading-results.md) applies comparison discipline to representations.
- [Large-Scale Data Systems Engineering LSDS-097](../../21-large-scale-data-systems-engineering/modules/097-cluster-benchmarking.md) introduces nested machine and cluster variation.
- [Software Testing and Quality Engineering STQE-002](../../13-software-engineering-testing-and-quality-engineering/modules/002-specifications-expectations-and-test-oracles.md) keeps correctness evidence ahead of performance.
- [Concurrent and Parallel Programming CONPAR-092](../../04-programming-languages-concurrent-and-parallel-programming/modules/092-roofline-and-operational-intensity-analysis.md) supplies model-derived performance expectations.
- [Systems Engineering SYSENG-043](../../26-systems-engineering/modules/043-cost-schedule-performance-and-risk.md) connects uncertainty to decision consequences.
- [Data Engineering DE-099](../../19-data-engineering/modules/099-versioning-and-deprecating-datasets.md) illustrates decisions that combine measured effects with compatibility, migration, and operational risk.

## References

1. Tomas Kalibera and Richard Jones, “Rigorous Benchmarking in Reasonable Time,” *ISMM 2013*, 63–74. [doi:10.1145/2464157.2464160](https://doi.org/10.1145/2464157.2464160). Checked 2026-09-05.
2. Andy Georges, Dries Buytaert, and Lieven Eeckhout, “Statistically Rigorous Java Performance Evaluation,” *OOPSLA 2007*, 57–76. [doi:10.1145/1297027.1297033](https://doi.org/10.1145/1297027.1297033). Checked 2026-09-05.
3. Torsten Hoefler and Roberto Belli, “Scientific Benchmarking of Parallel Computing Systems,” *SC 2015*. [doi:10.1145/2807591.2807644](https://doi.org/10.1145/2807591.2807644). Checked 2026-09-05.
4. Bradley Efron and Robert J. Tibshirani, *An Introduction to the Bootstrap*, Chapman & Hall/CRC, 1993. ISBN 978-0-412-04231-7.
5. András Vargha and Harold D. Delaney, “A Critique and Improvement of the CL Common Language Effect Size Statistics of McGraw and Wong,” *Journal of Educational and Behavioral Statistics* 25(2), 2000, 101–132. [doi:10.3102/10769986025002101](https://doi.org/10.3102/10769986025002101). Checked 2026-09-05.
6. Ronald L. Wasserstein and Nicole A. Lazar, “The ASA Statement on p-Values: Context, Process, and Purpose,” *The American Statistician* 70(2), 2016, 129–133. [doi:10.1080/00031305.2016.1154108](https://doi.org/10.1080/00031305.2016.1154108). Checked 2026-09-05.
7. Philip J. Fleming and John J. Wallace, “How Not to Lie with Statistics: The Correct Way to Summarize Benchmark Results,” *Communications of the ACM* 29(3), 1986, 218–221. [doi:10.1145/5666.5673](https://doi.org/10.1145/5666.5673). Checked 2026-09-05.
8. David C. Howell, *Statistical Methods for Psychology*, 8th ed., Cengage, 2012. ISBN 978-1-111-83548-4.

## Exercises

### Exercise 1

Define estimand, assignment unit, paired contrast, effect size, confidence-interval coverage, practical threshold, equivalence margin, and multiplicity for comparing two graph engines.

### Exercise 2

For baseline/candidate pairs (12,10), (20,18), (40,30), and (8,9) ms, compute paired differences, mean difference, aggregate reduction percentage, and mean pair reduction percentage. Explain the difference.

### Exercise 3

An experiment has 50 inner iterations in each of three processes on one host, with two timeouts deleted. Diagnose the analysis and specify a defensible unit/failure treatment.

### Exercise 4

Compare a paired t interval, block bootstrap, exact sign-randomization test, and hierarchical model for workloads nested within machines.

### Exercise 5

Design a statistical comparison of two external-memory graph implementations across graph classes and machines. Include estimand, assignment, weights, failures, effects, uncertainty, multiplicity, diagnostics, sensitivity, and decision.

## Answers to the Exercises

### Answer 1

The estimand names the target population quantity, such as mean baseline-minus-candidate latency over target-weighted graph-machine sessions. The assignment unit is the independently randomized block or machine-session, not each loop timing. A paired contrast subtracts outcomes within the same block. Effect size gives magnitude in ms, ratio, or another decision unit. A 95% confidence procedure has 95% long-run coverage under its assumptions; it does not assign 95% posterior probability automatically. A practical threshold is the smallest worthwhile benefit. An equivalence margin bounds effects treated as operationally interchangeable. Multiplicity is the family of graph classes, metrics, algorithms, and hypotheses that creates selection opportunities.

### Answer 2

Differences $B-C$ are 2, 2, 10, and -1 ms; their mean is $13/4=3.25$ ms. Baseline mean is 20 ms and candidate mean is 16.75 ms, so aggregate reduction is $100(20-16.75)/20=16.25\%$. Pair reductions are $16.67\%,10\%,25\%,$ and $-12.5\%$, whose mean is about $9.79\%$. The aggregate weights blocks through baseline magnitude; the pair mean weights each block equally. Choose the statistic from whether total work or a random block is the estimand, and report heterogeneity.

### Answer 3

The 150 iterations are nested within three processes and one host; they are not 150 independent deployment units. Analyze process-level summaries or a hierarchy while acknowledging that cross-host variation is unobserved. The two deleted timeouts create survivor bias, especially if treatment-related. Restore them with process/run identities as censored or failure outcomes under the frozen rule, report rates and lower bounds, and use failure-aware comparison. Add independently randomized processes, sessions, and hosts required by the claim rather than merely extending loops.

### Answer 4

A paired t interval directly targets mean within-block difference when independent machine-level or otherwise appropriate contrasts support its variance assumptions. A block bootstrap resamples complete assignment units and can recompute weighted nonlinear statistics, but very few machines make it unstable. An exact sign-randomization test aligns with randomized within-block labels under exchangeability and a sharp null, yet mainly tests compatibility rather than magnitude. A hierarchical model represents machine and workload variation and partial pooling, supporting transfer questions but adding distributional/prior choices. Preserve pairing in all methods, make machine the outer sampling level when generalizing across machines, report natural effects, and compare sensitivity rather than selecting the most favorable method.

### Answer 5

Define mean paired wall-time and I/O difference over target-weighted graph classes and supported machines, with a practical threshold and memory/failure constraints. Randomize both implementations within graph-machine-session blocks, repeat independent sessions/machines, and retain inner timing as nested. Freeze tuned configurations and weights. Report per-class and weighted natural-unit effects, ratios with explicit denominator, and tails. Treat wrong answers as infeasible and timeouts/OOM as censored failures. Use machine-aware paired or hierarchical intervals and a design-compatible randomization analysis for a prespecified primary contrast. Declare secondary CPU/I/O/memory metrics and multiple class comparisons; show raw paired plots, order, failures, and dependence diagnostics. Recompute under plausible weights, censoring rules, robust summaries, and leave-one-machine-out views. Adopt only if correctness holds, benefit is practically supported, resource/tail risks pass, and profile evidence matches mechanism; otherwise restrict by observable regime or collect new machines/graphs.
