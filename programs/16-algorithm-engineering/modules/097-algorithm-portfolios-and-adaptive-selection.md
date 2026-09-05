---
module_id: ALGE-097
program: Algorithm Engineering
level: 2
module_number: 97
title: Algorithm Portfolios and Adaptive Selection
status: complete
last_verified: 2026-09-05
---

# Algorithm Portfolios and Adaptive Selection

## One-Page Review

### Governing question

When no single implementation dominates across the target instances, how can we construct, select, schedule, and govern a portfolio whose end-to-end benefit survives feature cost, prediction error, resource contention, distribution shift, and failure?

### Essential definitions

- An **algorithm portfolio** is a governed set of candidate algorithms plus a selection, scheduling, or racing policy.
- **Per-instance algorithm selection** maps features available for a new instance to a candidate or schedule.
- The **single best solver** (SBS) is the one candidate with lowest aggregate loss on an evaluation population.
- The **virtual best solver** (VBS) is an oracle that retrospectively chooses the best candidate for every instance.
- The **oracle gap** is the performance difference between SBS and VBS; it is an upper opportunity bound for a selector under the same loss table, not an attainable promise.
- **Selection overhead** includes feature extraction, inference, dispatch, warm-up, verification, coordination, and fallback.
- A **presolver** runs before feature-dependent selection, often to solve easy instances or bound feature cost.
- An **adaptive policy** changes allocation after observing safe runtime signals from the current execution.

### Central model, mechanism, or theorem

Let candidate set $A$, target instances $I\sim P$, loss $L(a,I)$, selection-time features $x(I)$, and policy $\pi$ be fixed. The deployed loss is

$$
L_{\pi}(I)=c_x(I)+c_{\pi}(I)+L(\pi(x(I)),I)+c_v(I)+c_f(I),
$$

where the terms cover features, dispatch, selected execution, verification, and failure/fallback. A selector is useful only when its held-out end-to-end risk improves the SBS under the same correctness and resource contract. The VBS gives $\mathbb E[\min_a L(a,I)]$; because it uses outcomes unavailable at decision time, comparing a learned selector only with VBS can hide whether it beats a deployable baseline.

### Critical invariants

- Every portfolio member implements the same declared problem semantics or exposes an explicit translation and verification boundary.
- Only features available, safe, and affordable at selection time may drive a decision.
- Candidate, feature, selector, presolver, schedule, budget, timeout, fallback, and loss versions are frozen for confirmation.
- Training, tuning, and evaluation split at the instance-family dependency unit.
- End-to-end accounting includes overhead, parallel work, memory, energy, failures, and contention.
- Correctness and hard constraints gate candidates before optimization.
- Missing, invalid, out-of-domain, or low-confidence features route deterministically to a safe fallback.
- Adaptation uses signals that cannot corrupt semantics or leak unavailable answers.

### Common failures

Calling a list of solvers a portfolio without a policy; reporting VBS as achieved performance; optimizing classification accuracy instead of decision loss; excluding feature time; training on censored runtimes as though they were exact; splitting near-duplicate instances across folds; selecting on post-run features; comparing a parallel race by wall time while hiding core-seconds; allowing candidates to mutate shared state incompatibly; learning from production outcomes without exploration or fresh confirmation; silently dropping failed candidates; letting confidence choose an unsafe route; and retaining a selector after feature or workload drift invalidates its evidence.

### Compact example

On five instances, solver A costs 4, 20, 10, 18, and 9 ms; B costs 7, 8, 13, 16, and 5 ms. SBS is B at 49 ms and VBS costs 43 ms. A density selector chooses A on three sparse instances and B on two dense instances, giving 45 ms execution. With 0.5 ms feature cost per instance, end-to-end cost is 47.5 ms. It closes $(49-47.5)/(49-43)=25\%$ of the oracle gap, not the larger apparent $(49-45)/6$ obtained by hiding features.

### Connections

[ALGE-070](./070-choosing-between-exact-approximate-and-heuristic-solutions.md) defines route obligations, [ALGE-091](./091-representative-workload-construction.md) defines the population, [ALGE-095](./095-parameter-tuning-without-overfitting.md) governs selection tuning, and [ALGE-096](./096-comparing-implementations-statistically.md) supplies held-out comparison. ALGE-098 next examines numerical behavior that can make apparently interchangeable members semantically different.

## Governing Question

What portfolio and policy should be deployed for a stated instance population and resource contract, and what evidence shows that its diversity is useful rather than merely additional complexity?

## Why This Matters

Algorithm performance is often heterogeneous. Sparse and dense graphs favor different representations; structured and random constraint instances favor different search procedures; warm-cache and external-memory workloads favor different layouts. A universal winner may not exist on the population engineers actually serve.

A portfolio can convert complementary strengths into lower loss or lower tail risk. It also creates a second algorithmic system: feature extraction, prediction, scheduling, cancellation, verification, fallback, training data, and drift monitoring. A selector that chooses perfectly after expensive preprocessing, or a race that uses sixteen times the compute, may be worse than the SBS. The portfolio must therefore be evaluated as one end-to-end implementation.

## Prerequisites and Retrieval

Retrieve randomized behavior from [ALGE-029](./029-randomization-as-a-design-tool.md), decision routes from [ALGE-070](./070-choosing-between-exact-approximate-and-heuristic-solutions.md), parallel work accounting from [ALGE-081](./081-work-span-and-parallel-dependency.md), workload populations from [ALGE-091](./091-representative-workload-construction.md), benchmark hierarchy from [ALGE-092](./092-benchmark-design-and-reproducibility.md), adversarial panels from [ALGE-094](./094-adversarial-and-pathological-inputs.md), selection discipline from [ALGE-095](./095-parameter-tuning-without-overfitting.md), and statistical comparison from [ALGE-096](./096-comparing-implementations-statistically.md).

## Learning Objectives

After this module, you should be able to:

1. formalize a portfolio scenario using instances, features, candidates, losses, and resource constraints;
2. compute and interpret SBS, VBS, oracle gap, regret, and gap closed;
3. distinguish static choice, per-instance selection, schedules, restarts, races, and within-run adaptation;
4. design cheap, causal, versioned features and a constraint-first fallback policy;
5. train and evaluate selectors without family leakage, tuning reuse, or censored-outcome distortion;
6. account for feature, inference, verification, parallel, cancellation, and contention costs;
7. diagnose uncertainty, out-of-domain inputs, feedback, drift, and correlated candidate failures; and
8. deploy a portfolio with bounded authority, monitoring, rollback, and fresh confirmation.

## Core Exposition

### Specify the scenario and loss

Define instance space, target distribution, candidate set, observable feature schema, resource budget, semantic contract, and loss. Runtime alone is rarely sufficient. A lexicographic loss may first reject incorrect or infeasible output, then minimize deadline violation, latency, memory, energy, or solution-quality regret. Scalar penalties for timeout or wrong answers must reflect the actual decision; a convenient constant such as ten times the cutoff is a comparison convention, not elapsed time.

Use one row per independent instance-family unit and preserve repeated runs, seeds, machines, censoring, and failures beneath it. Candidate versions include parameters, compiler, libraries, hardware assumptions, and preprocessing. If two candidates solve different variants, their apparent complementarity is invalid until translation and output verification establish common semantics.

### Establish deployable and oracle baselines

Compute every candidate's target-weighted held-out loss. The minimum aggregate candidate is SBS. Compute VBS by taking the lowest valid candidate loss on each instance. The difference is the oracle gap. A zero gap leaves no retrospective opportunity for per-instance selection under that table. A large gap demonstrates complementarity but says nothing about whether cheap pre-run features identify the winner.

Report a simple static rule and a trivial feature baseline as well. A complex model should beat not only SBS but also transparent policies such as size threshold, presolve-then-default, or a short fixed schedule. Evaluate with natural units, failures, and distributions; normalized gap closed is useful only beside the denominator and absolute loss.

### Build diversity that changes outcomes

Diversity means complementary conditional loss, not different branding. Two solvers that fail on the same instance families and contend for the same bottleneck add little. Candidate construction may vary algorithmic paradigm, branching rule, representation, precision, random seed, restart schedule, preprocessing, or hardware path, provided the variants remain independently useful and auditable.

Measure marginal contribution on held-out data: remove a member and recompute the frozen portfolio. A candidate that never changes feasible decisions may still be a safety fallback, but that role must be explicit. Portfolio size increases measurement, integration, patching, and attack surface; prune by end-to-end value rather than training wins.

### Design selection-time features

Features must exist before the selection deadline. Examples include input size, sparsity, degree summaries, constraint ratios, numeric range, and bounded probe results. Solver completion time, final search-tree size, or a statistic produced only by the winning algorithm is leakage. Feature code is production code: specify units, missingness, cost, determinism, overflow behavior, privacy, version, and adversarial limits.

Feature groups can have conditional cost. Cheap syntactic features may choose a route immediately; expensive probing should run only when its expected value exceeds cost. Include feature timeout and failure in the policy. Ensure feature computation does not mutate input or warm one candidate unfairly unless that shared preprocessing is part of every route's accounted state.

### Choose a portfolio geometry

A static choice always runs one candidate. Per-instance selection predicts one candidate from features. A sequential schedule allocates slices and may stop on a verified result. A restart policy reruns a randomized method with new seeds. A parallel race starts members together and cancels losers. A cooperative portfolio exchanges incumbents, bounds, or learned clauses. Within-run adaptation changes representation, heuristic, or allocation from safe telemetry.

Each geometry changes the evidence. Parallel racing can reduce wall time but raises core-seconds, memory pressure, license use, and interference. Sequential schedules need safe suspend/resume or restart semantics. Cooperative members need compatible model and bound identities. Adaptation adds state-machine invariants: a transition must preserve feasible incumbents, valid certificates, numeric conventions, and cancellation safety.

### Train for decision loss

Predicting the fastest label treats a 0.1 ms and a 100 second mistake equally. Train or tune against the deployment loss: cost-sensitive classification, per-candidate performance regression followed by argmin, pairwise preference, ranking, or direct policy optimization. Include feature and dispatch cost, timeouts, solution quality, and constraints.

Censored runtimes are lower bounds, not exact cutoff values. Replacing every timeout by the cutoff can make a solver with many unknown long runs appear too good; a penalty such as PAR10 encodes a declared deadline cost but not a recovered runtime distribution. Preserve censoring and compare sensitivity to defensible failure treatments.

### Split the complete selection procedure

Instances from one generator seed, graph family, trace, customer, or time window can be near duplicates. Group them into the same split. Preprocessing, feature selection, imputation, candidate pruning, presolver design, model choice, hyperparameter tuning, threshold tuning, and calibration all occur inside training. Outer holdout evaluates the complete frozen procedure.

If portfolio members were created or tuned using the same evaluation table, VBS and selector estimates are optimistic. Record the search lineage. Compare with SBS chosen only inside the training portion for each outer fold; using globally selected SBS leaks evaluation outcomes into the baseline.

### Execute an end-to-end illustration

The reference computes SBS, VBS, a transparent selector, feature-inclusive loss, oracle-gap closure, and fastest-label accuracy. The selector's one wrong label is a small decision error, illustrating why accuracy is secondary.

<!-- bijux-verify: {"id":"portfolio-gap-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"single_best: B 49.0\nvirtual_best_cost: 43.0\nselector_execution_cost: 45.0\nselector_end_to_end_cost: 47.5\nselector_regret_to_oracle: 4.5\noracle_gap_closed_percent: 25.0\nfastest_label_accuracy_percent: 80.0\n","stderr":""}} -->
```python
instances = [
    ("small-sparse", 0.10, {"A": 4.0, "B": 7.0}),
    ("large-dense", 0.90, {"A": 20.0, "B": 8.0}),
    ("medium-sparse", 0.20, {"A": 10.0, "B": 13.0}),
    ("large-sparse", 0.10, {"A": 18.0, "B": 16.0}),
    ("small-dense", 0.80, {"A": 9.0, "B": 5.0}),
]
feature_cost = 0.5

candidate_totals = {
    candidate: sum(costs[candidate] for _, _, costs in instances)
    for candidate in ("A", "B")
}
single_best = min(candidate_totals, key=candidate_totals.get)
virtual_best = sum(min(costs.values()) for _, _, costs in instances)

choices = ["B" if density >= 0.5 else "A" for _, density, _ in instances]
execution = sum(costs[choice] for choice, (_, _, costs) in zip(choices, instances))
end_to_end = execution + feature_cost * len(instances)
correct_labels = sum(
    choice == min(costs, key=costs.get)
    for choice, (_, _, costs) in zip(choices, instances)
)
oracle_gap = candidate_totals[single_best] - virtual_best
gap_closed = 100 * (candidate_totals[single_best] - end_to_end) / oracle_gap

print("single_best:", single_best, candidate_totals[single_best])
print("virtual_best_cost:", virtual_best)
print("selector_execution_cost:", execution)
print("selector_end_to_end_cost:", end_to_end)
print("selector_regret_to_oracle:", end_to_end - virtual_best)
print("oracle_gap_closed_percent:", gap_closed)
print("fastest_label_accuracy_percent:", 100 * correct_labels / len(instances))
```

The 47.5 ms selector beats SBS by only 1.5 ms and remains 4.5 ms above the oracle. Its 80% label accuracy does not reveal that the single error costs only 2 ms. Confirmation must decide whether 1.5 ms total improvement exceeds uncertainty, engineering complexity, and future drift.

### Govern uncertainty and fallback

A point prediction is not authority. Calibrate uncertainty on grouped held-out data and define abstention. Missing fields, invalid ranges, feature timeout, ambiguous scores, novel combinations, or distance from supported training regions route to a safe default or conservative schedule. A fallback must meet correctness and resource obligations independently of model availability.

Thresholds should reflect asymmetric consequences. Low confidence might justify extra probing for an offline batch but must not consume an interactive deadline. For safety-critical output, independent verification gates every member; selector confidence cannot waive verification.

### Adapt during execution carefully

Runtime signals can include progress, incumbent quality, bound gap, queue growth, memory pressure, frontier density, or stagnation. Define which are trustworthy, when they are sampled, and how transitions preserve state. A progress metric can be misleading across algorithms, and a candidate can game a learned termination rule.

Adaptation can be modeled as a policy over observable state, but production feedback is selective: only the chosen route's outcome is observed unless the system safely explores or shadows alternatives. Naively retraining on logged choices creates confounding and blind spots. Logged propensities, randomized exploration, off-policy assumptions, or new controlled experiments are required for causal comparisons.

### Account for schedules, restarts, and races

For heavy-tailed randomized runtimes, independent restarts can improve completion time. Restart theory depends on fresh randomness, correct Las Vegas behavior, and restart overhead; retaining corrupted state or changing problem semantics breaks the argument. A universal schedule has bounded theoretical performance in its model [7], not a guarantee for arbitrary stateful production solvers.

For a parallel race with candidate core counts $p_j$ and cancellation time $t_j$, approximate CPU work is $\sum_j p_jt_j$, while wall latency is the first acceptable verified completion plus cancellation and verification. Report both. Contention can slow every member, so isolated runtimes cannot simply be combined to predict the race.

### Monitor and retire responsibly

Log feature schema/version, candidate set, chosen route, scores or uncertainty, presolve result, execution/cancellation, verification, fallback, costs, failures, and policy version. Avoid sensitive raw features when aggregates suffice. Monitor outcome regret where counterfactual evidence exists, plus feature drift, route shares, abstention, failures, tail latency, resource use, and semantic discrepancies.

Define rollback and retirement conditions. Candidate vulnerabilities, library changes, hardware shifts, workload drift, or loss changes invalidate old evidence. Retuning or adding a solver creates a new selection procedure and requires fresh confirmation. Keep a simple deployable baseline so portfolio complexity must continue earning its place.

## Definitions and Notation

Let $I\sim P$ be a target instance, $A=\{a_1,\ldots,a_k\}$ the frozen candidates, $x(I)$ pre-decision features, $L(a,I)$ deployment loss, and $\pi(x)$ a policy. Let $C_x,C_d,C_v,C_f$ denote feature, dispatch, verification, and failure/fallback cost. SBS minimizes aggregate candidate loss; VBS uses $\min_a L(a,I)$ per observed instance.

For lower-is-better aggregate risks $R_{\mathrm{SBS}}>R_{\mathrm{VBS}}$, gap closed is

$$
G(\pi)=\frac{R_{\mathrm{SBS}}-R_{\pi}}{R_{\mathrm{SBS}}-R_{\mathrm{VBS}}}.
$$

It can be negative when a selector loses to SBS and exceed one only when its accounted mechanism outperforms the recorded VBS table, which signals different resources, stochastic outcomes, or inconsistent accounting that must be explained.

## Mechanisms, Invariants, or Proof Structure

### Oracle-bound argument

For every recorded instance $i$, $\min_a L(a,i)\le L(a',i)$ for any fixed $a'$. Summing with nonnegative weights gives VBS no greater recorded execution loss than SBS. This inequality excludes feature and policy costs because the oracle does not deploy; adding those costs only to a real selector is necessary, not unfair.

### Feature-value inequality

Let a feature group cost $c$ and reduce expected selected execution loss from $r_0$ to $r_1$. Under an additive risk model it has positive net value only if $r_0-r_1>c$, subject to uncertainty and hard constraints. Predictive accuracy alone cannot establish this inequality.

### Selection invariants

All decisions use pre-run versioned inputs; constraints filter candidates before score comparison; ties are deterministic; invalid or uncertain states fall back; total budget includes features and verification; paired evaluation retains instance identity; and updates never reuse confirmation evidence while claiming the same confirmation.

### Adaptation invariants

Every transition preserves problem identity, feasible incumbent validity, bound provenance, numeric semantics, remaining budget, and cancellation ownership. Only one result is published under an idempotent gate, and late losers cannot overwrite it. Cooperative sharing validates message version and certificate scope.

## Alternatives and Trade-Offs

| Geometry | Strength | Main cost or risk | Best fit |
|---|---|---|---|
| SBS | simple, auditable, cheap | misses heterogeneity | small oracle gap |
| threshold rule | transparent and fast | brittle boundary | strong one-feature regimes |
| learned selector | nonlinear per-instance choice | leakage, drift, uncertainty | stable predictive features |
| sequential schedule | bounded conditional work | restart/state overhead | deadline tiers |
| restart policy | controls heavy runtime tails | repeated setup and model assumptions | randomized Las Vegas search |
| parallel race | low completion latency | aggregate work and contention | valuable latency with spare resources |
| cooperative portfolio | shares progress | complex trust and state compatibility | compatible exact/anytime solvers |
| within-run adaptation | reacts to observed regime | policy feedback and invariant risk | informative safe progress signals |

One large universal model reduces operational variety but may obscure regimes. Specialized selectors clarify domains but multiply ownership. A small diverse portfolio with a deterministic fallback is often easier to defend than a large library whose marginal members were selected from the evaluation data.

## Failure Modes and Misconceptions

- **“The VBS is our expected deployment.”** It uses retrospective outcomes unavailable at selection time.
- **“High winner accuracy proves value.”** Decision loss and overhead, not label count, determine value.
- **“Features are free.”** They consume latency, work, memory, privacy budget, and failure surface.
- **“Different implementations guarantee diversity.”** Correlated conditional losses can make them redundant.
- **“Timeout equals the cutoff.”** It is censored unless the declared loss assigns a deadline penalty.
- **“Cross-validation fixes leakage.”** Only if the complete procedure and related instance families stay inside folds.
- **“Parallel is faster.”** Wall latency may fall while core-seconds, memory, energy, and contention rise.
- **“Adaptation always learns.”** Selective feedback can reinforce a bad policy without controlled counterfactual evidence.
- **“Uncertainty can choose the risky route.”** Uncertainty should reduce authority and trigger fallback or more evidence.
- **“A frozen selector stays valid.”** Feature semantics, candidates, workloads, hardware, and consequences drift.

## Worked Examples

### Example 1

**Situation.** Three candidates have held-out total losses 120, 135, and 150; per-instance minima total 120.

**Reasoning.** SBS and VBS are both 120, so the oracle gap is zero. No per-instance selector can improve this recorded loss table by switching candidates. A portfolio might still add resilience under a separate failure objective, but that is a different loss and needs evidence.

**Conclusion.** Establish an oracle opportunity before funding selection complexity.

### Example 2

**Situation.** A model achieves 95% fastest-label accuracy, but its five mistakes each cost 100 seconds; a 75% model makes only 1-second mistakes.

**Reasoning.** Over 100 equally weighted instances, the first model's error loss is 500 seconds and the second model's is at most 25 seconds under the stated pattern. Accuracy discards consequence magnitude. Train and compare using the deployment loss, then report label metrics diagnostically.

**Conclusion.** Cost-sensitive decisions can favor a less accurate classifier.

### Example 3

**Situation.** A graph selector saves 3 ms of execution on average, while degree-histogram extraction costs 5 ms.

**Reasoning.** Ignoring other overhead, end-to-end loss rises by 2 ms. Cache reuse is valid only if the histogram already exists for the target request and its production ownership is included. Otherwise the feature group has negative net value.

**Conclusion.** A predictive feature is useful only when its decision value exceeds its real cost.

### Example 4

**Situation.** Random train/test row splitting places graphs produced from the same base graph and perturbation seed in both partitions.

**Reasoning.** Structural near duplicates let the selector memorize family identity and overstate transfer. Group by base graph and generator lineage before any preprocessing or tuning. If deployment includes new graph families, hold out entire families.

**Conclusion.** Split at the dependency unit the deployment claim requires.

### Example 5

**Situation.** A solver times out at 60 seconds on 40% of training instances; the table records every timeout as exactly 60.

**Reasoning.** Actual runtimes are only known to exceed 60. Treating them as exact understates execution time and can distort regression. Use a declared deadline loss, censor-aware analysis, failure probability, or bounded schedule objective, and test sensitivity.

**Conclusion.** Censoring is information about a bound, not an observed completion time.

### Example 6

**Situation.** Four one-core solvers race and a winner returns after 2 seconds; a one-core SBS returns after 5 seconds.

**Reasoning.** The race used about 8 core-seconds before cancellation overhead versus 5 for SBS. It wins a latency objective but loses raw CPU work. Shared memory and cache contention can change both numbers, so benchmark the integrated race under its real limits.

**Conclusion.** Parallel portfolios require wall-time and aggregate-resource accounting.

### Example 7

**Situation.** An input lacks one feature and the imputer produces a confident score for an exact solver that is unsafe on negative weights.

**Reasoning.** Semantic admissibility is a hard gate, not a model probability. Detect negative-weight capability directly; exclude unsafe members. Missing or invalid selection data routes to a solver whose contract covers the input or rejects it explicitly.

**Conclusion.** Constraint-first dispatch prevents confidence from authorizing an invalid algorithm.

### Example 8

**Situation.** A randomized complete solver shows a heavy runtime tail, and independent short restarts often finish earlier.

**Reasoning.** Restarts preserve correctness only if every run is Las Vegas, uses fresh randomness, and publication accepts a verified result. Include initialization and repeated work. A theorem about universal restart schedules applies only under its runtime and independence model.

**Conclusion.** Restart gains are conditional algorithmic claims, not folklore.

### Example 9

**Situation.** A running solver reports no incumbent improvement for 10 seconds, so an adaptive policy switches to another solver.

**Reasoning.** Validate that the stagnation signal is comparable and cannot discard a uniquely valuable bound. Transfer any incumbent only with matching model, objective, numeric tolerance, and provenance. Charge switching cost and preserve the total deadline.

**Conclusion.** Safe adaptation is a state transition with invariants, not an unconstrained model action.

### Example 10

**Situation.** The selector increasingly sends difficult cases to fallback; retraining data contain mostly easy outcomes from the primary route.

**Reasoning.** Logged outcomes are policy-selected and do not reveal counterfactual candidate performance. Rising fallback share may signal drift. Freeze the old safe policy, collect controlled shadow or exploration evidence under authorization, group by time, and confirm the revised procedure on a future window.

**Conclusion.** Production feedback needs causal and temporal governance before it can train a selector.

## Cross-Program Connections

- [Data Structures Engineering DSE-010](../../17-data-structures-engineering/modules/010-benchmarking-a-structure-without-misleading-results.md) supplies structure-aware benchmark discipline.
- [Testing and Quality Engineering STQE-002](../../13-software-engineering-testing-and-quality-engineering/modules/002-specifications-expectations-and-test-oracles.md) develops partial-oracle portfolios and independent verification.
- [Concurrent and Parallel Programming CONPAR-041](../../04-programming-languages-concurrent-and-parallel-programming/modules/041-task-parallelism-and-dependency-graphs.md) supplies cancellation and task-lifecycle mechanics for races.
- [Systems Engineering SYSENG-043](../../26-systems-engineering/modules/043-cost-schedule-performance-and-risk.md) places performance benefit beside resource and decision risk.
- [Data Engineering DE-089](../../19-data-engineering/modules/089-auditability-and-provenance.md) supplies lineage for features, training tables, decisions, and outcomes.
- [Platform Engineering PLAT-097](../../29-platform-engineering/modules/097-capability-lifecycle-and-retirement.md) connects portfolio members to versioning and retirement.

## References

1. John R. Rice, “The Algorithm Selection Problem,” *Advances in Computers* 15, 1976, 65–118. [doi:10.1016/S0065-2458(08)60520-3](https://doi.org/10.1016/S0065-2458(08)60520-3). Primary formulation of features, algorithms, performance mappings, and selection; publisher record checked 2026-09-05.
2. Carla P. Gomes and Bart Selman, “Algorithm Portfolios,” *Artificial Intelligence* 126(1–2), 2001, 43–62. [doi:10.1016/S0004-3702(00)00081-3](https://doi.org/10.1016/S0004-3702(00)00081-3). Primary portfolio and runtime-distribution study; publisher and author records checked 2026-09-05.
3. Lin Xu, Frank Hutter, Holger H. Hoos, and Kevin Leyton-Brown, “SATzilla: Portfolio-Based Algorithm Selection for SAT,” *Journal of Artificial Intelligence Research* 32, 2008, 565–606. [JAIR paper](https://jair.org/index.php/jair/article/view/10509). Primary per-instance selection system; journal record checked 2026-09-05.
4. Marius Lindauer, Holger H. Hoos, Frank Hutter, and Torsten Schaub, “AutoFolio: An Automatically Configured Algorithm Selector,” *Journal of Artificial Intelligence Research* 53, 2015, 745–778. [doi:10.1613/jair.4726](https://doi.org/10.1613/jair.4726). Primary work on configuring selection procedures; journal record checked 2026-09-05.
5. Bernd Bischl et al., “ASlib: A Benchmark Library for Algorithm Selection,” *Artificial Intelligence* 237, 2016, 41–58. [doi:10.1016/j.artint.2016.04.003](https://doi.org/10.1016/j.artint.2016.04.003). Primary benchmark-scenario format and evaluation reference; publisher record checked 2026-09-05.
6. Lars Kotthoff, “Algorithm Selection for Combinatorial Search Problems: A Survey,” *AI Magazine* 35(3), 2014, 48–60. [doi:10.1609/aimag.v35i3.2460](https://doi.org/10.1609/aimag.v35i3.2460). Survey connecting selection, portfolios, schedules, features, and evaluation; journal record checked 2026-09-05.
7. Michael Luby, Alistair Sinclair, and David Zuckerman, “Optimal Speedup of Las Vegas Algorithms,” *Information Processing Letters* 47(4), 1993, 173–180. [doi:10.1016/0020-0190(93)90029-9](https://doi.org/10.1016/0020-0190(93)90029-9). Primary universal-restart result and assumptions; publisher record checked 2026-09-05.
8. Catherine C. McGeoch, *A Guide to Experimental Algorithmics*, Cambridge University Press, 2012. [doi:10.1017/CBO9780511843747](https://doi.org/10.1017/CBO9780511843747). Monograph for experimental design, measurement, and bounded conclusions; publisher record checked 2026-09-05.

## Exercises

### Exercise 1

Define portfolio, per-instance selection, SBS, VBS, oracle gap, selection overhead, presolver, and adaptive policy for a shortest-path service.

### Exercise 2

Three instances have A/B costs (4,7), (12,5), and (8,9) ms. A size rule chooses A, B, B and costs 0.5 ms per instance. Compute SBS, VBS, selector execution and end-to-end cost, regret to VBS, and oracle gap closed.

### Exercise 3

A selector is trained with random row folds, post-run node-expansion count, timeouts recorded at the cutoff, and global feature normalization. Diagnose every evidence defect and specify a valid evaluation.

### Exercise 4

Compare a static solver, feature selector, sequential schedule, four-way race, and adaptive cooperative portfolio for a hard-search service with latency and core-hour budgets.

### Exercise 5

Design a production portfolio for external-memory graph analytics across sparse, dense, small, huge, benign, and adversarial graphs. Include semantics, candidates, features, training, loss, uncertainty, fallback, resources, adaptation, verification, monitoring, drift, and retirement.

## Answers to the Exercises

### Answer 1

A portfolio is the versioned set of admissible shortest-path implementations plus dispatch or scheduling policy. Per-instance selection maps pre-run graph features to a member or schedule. SBS is the one implementation with lowest target-weighted evaluation loss; VBS retrospectively takes the best valid member per graph. Their difference is the oracle gap. Overhead includes feature extraction, inference, dispatch, verification, cancellation, and fallback. A presolver performs a bounded early attempt before later selection. An adaptive policy changes allocation using safe current-run signals. Negative-edge capability remains a hard gate, and missing or novel features route to a semantically valid fallback.

### Answer 2

Totals are A $=4+12+8=24$ ms and B $=7+5+9=21$ ms, so SBS is B at 21 ms. VBS is $4+5+8=17$ ms. The rule A, B, B executes in $4+5+9=18$ ms; features add 1.5 ms, giving 19.5 ms end to end. Regret to VBS is 2.5 ms. The oracle gap is 4 ms and the rule closes $(21-19.5)/4=37.5\%$. Without feature cost it would appear to close 75%, which answers a different question.

### Answer 3

Random rows can leak related instance families; group by generator, base instance, tenant, or trace lineage. Post-run expansion count is unavailable at selection and must be removed or replaced by a bounded pre-run probe whose cost is included. Timeout values are censored; retain censoring or apply a declared deadline loss rather than regress them as exact completion. Global normalization uses evaluation rows; fit every transform within each training fold. Candidate pruning, feature selection, imputation, model and threshold tuning, presolver design, and SBS choice also occur inside training. Evaluate the complete frozen procedure on grouped outer folds or untouched future/family holdout, including overhead, failures, uncertainty, fallback, and resource use.

### Answer 4

The static solver is the auditable baseline and suits a small oracle gap. A feature selector can exploit stable regimes but must repay feature cost and handle uncertainty. A sequential schedule bounds extra work and can exploit easy presolve, but needs restart or resumable-state semantics. A four-way race may minimize tail latency while consuming roughly four times the active core work and adding contention/cancellation. A cooperative adaptive portfolio can share bounds or incumbents and react to progress, but requires compatible model identities, atomic state, trusted telemetry, and a much larger verification surface. Compare all under the same deadline, total core-hour, memory, correctness, and quality contract on held-out families; deploy the simplest route whose effect and risks clear practical thresholds.

### Answer 5

Define one graph problem, numeric semantics, output certificate, and failure contract. Include structurally diverse in-memory, blocked, external-memory, and conservative adversarial routes, each versioned and tuned only on development data. Use bounded pre-run size, density, degree, weight-range, storage-layout, and memory-budget features; never use final I/O or runtime. Group graph families and generator lineages across training and confirmation. Optimize a lexicographic loss: correctness and memory/deadline feasibility, then target-weighted latency, I/O, energy, and quality. Include feature, coordination, verification, and aggregate parallel cost. Calibrate abstention and route missing, invalid, out-of-domain, or low-confidence cases to a conservative supported method. Permit adaptation only on versioned progress and pressure signals while preserving incumbents, certificates, numeric rules, budget, and cancellation. Independently verify output and publish once. Monitor route share, fallback, drift, errors, censored outcomes, latency, I/O, memory, energy, and counterfactual evidence. Roll back on semantic discrepancy or budget breach; retire redundant, unsafe, unsupported, or noncontributing members. Any new member, feature, loss, threshold, or retraining creates a new policy requiring fresh confirmation.
