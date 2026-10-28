---
module_id: ALGE-095
program: Algorithm Engineering
level: 2
module_number: 95
title: Parameter Tuning Without Overfitting
status: complete
last_verified: 2026-09-05
---

# Parameter Tuning Without Overfitting

## One-Page Review

### Governing question

How do we tune algorithm thresholds, heuristics, resource allocations, and strategy choices for a target workload without converting finite benchmark noise and quirks into brittle configuration?

### Essential definitions

- A **configuration** assigns values to algorithm, implementation, compiler, and resource parameters under a declared contract.
- A **configuration space** is the set of legal assignments, including conditional parameters.
- A **tuning set** selects configurations; a **confirmation set** evaluates the frozen selection without informing it.
- **configuration overfitting** occurs when selection exploits noise or idiosyncrasies in the tuning evidence rather than stable target structure.
- **selection bias** is optimism caused by reporting the best observed tuning score as though it were untouched evaluation.
- A **budget** limits trials, time, CPU, memory, or evaluations.
- **incumbent** is the currently preferred configuration under the tuning rule.
- **nested evaluation** repeats the complete tuning procedure inside each outer evaluation split or block.

### Central model, mechanism, or theorem

Let $\Lambda$ be the configuration space and $\hat R_T(\lambda)$ the tuning-set risk. Selection produces

$$
\hat\lambda=\arg\min_{\lambda\in\Lambda}\hat R_T(\lambda).
$$

Even if each $\hat R_T(\lambda)$ is individually unbiased for its target risk, the minimum over many noisy estimates is generally optimistic. The confirmation estimate must use evidence $H$ not consulted by the search: $\hat R_H(\hat\lambda)$. The object being evaluated is the entire procedure—space, search, budget, stopping, seeds, and refitting—not merely the final values.

### Critical invariants

- Correctness, quality, safety, and resource constraints filter configurations before performance ranking.
- Tuning and confirmation identities are disjoint at the workload dependency unit.
- The search space, parameter transformations, budget, objective, seeds, failure policy, and stopping rule are versioned.
- Every trial, including failure, timeout, prune, and duplicate, remains recorded.
- Confirmation evidence never feeds back into the same reported selection.
- Baselines receive comparable tuning opportunity and budget.
- Search cost and configuration complexity are part of the decision.
- A deployed configuration includes a supported domain, fallback, monitoring, and retuning trigger.

### Common failures

Reporting the best tuning score; repeatedly checking holdout results and adjusting; tuning on near-duplicate inputs across splits; searching thousands of settings for a candidate but using defaults for a baseline; optimizing mean time while ignoring failures or memory; treating timed-out trials as missing; changing ranges mid-search without versioning; using linear grids for orders-of-magnitude parameters; comparing optimizers by their best cherry-picked run; retaining only the incumbent; overfitting machine-specific noise; and deploying a narrow optimum without fallback or drift monitoring.

### Compact example

Configuration A scores 10 and 10 ms on two tuning workloads but 20 ms on holdout. B scores 11 and 11, then 11. Tuning selects A with mean 10; holdout honestly reports 20. Combining holdout into the search and switching to B would consume the holdout. A new untouched set is required to evaluate that revised choice.

### Connections

[ALGE-091](./091-representative-workload-construction.md) defines target splits, [ALGE-092](./092-benchmark-design-and-reproducibility.md) governs trials, and [ALGE-094](./094-adversarial-and-pathological-inputs.md) supplies non-negotiable robustness panels. ALGE-096 next compares frozen implementations statistically.

## Governing Question

For a target population, constraints, and finite evaluation budget, what configuration-selection procedure will generalize across new workloads, seeds, runs, and machines, and how will its optimism and failure modes be measured?

## Why This Matters

Production algorithms are rarely parameter free. Sorting switches algorithms at a cutoff; graph engines choose frontier representation; indexes choose fanout and compaction; schedulers choose batch and queue limits; randomized methods choose restart and sample budgets. Defaults encode some target, often not yours.

Tuning is itself an optimization problem over noisy measurements. More trials increase the chance of finding a genuinely good region and the chance of finding a lucky configuration. Adaptive optimizers intensify this feedback by choosing new trials from prior outcomes. Honest engineering separates discovery from confirmation and evaluates the selection procedure under the same constraints that deployment will face.

## Prerequisites and Retrieval

Retrieve empirical evidence from [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md), randomized search reasoning from [ALGE-029](./029-randomization-as-a-design-tool.md), approximate-quality constraints from [ALGE-061](./061-approximation-ratios-and-guarantees.md), representative splits from [ALGE-091](./091-representative-workload-construction.md), benchmark protocol from [ALGE-092](./092-benchmark-design-and-reproducibility.md), profiling from [ALGE-093](./093-profiling-time-memory-and-i-o.md), and adversarial panels from [ALGE-094](./094-adversarial-and-pathological-inputs.md).

## Learning Objectives

After this module, you should be able to:

1. define legal conditional configuration spaces and stable parameter transformations;
2. separate hard constraints, primary objective, secondary metrics, and tie-breaking;
3. split workloads, seeds, sessions, and machines without dependency leakage;
4. compare manual, grid, random, racing, model-based, and multi-fidelity search;
5. explain selection optimism and evaluate a complete tuning procedure with holdout or nesting;
6. govern timeouts, failures, early stopping, censoring, and adaptive budgets;
7. assess sensitivity, plateaus, interactions, transfer, and operational complexity; and
8. deploy a configuration with fallback, monitoring, drift triggers, and preserved provenance.

## Core Exposition

### Define the decision and configuration contract

Name the target population, platform class, deployment horizon, and consequences. Separate algorithmic parameters—pivot rule, batch size, restart limit—from compiler, runtime, and resource parameters. Define units, types, ranges, conditional activation, and legality. Logarithmic parameters should often be searched on a log scale; categorical values have no numeric distance unless the method defines one.

Some settings change semantics. Approximation tolerance, floating-point mode, timeout, and consistency policy cannot enter a speed objective without quality constraints. A configuration is feasible only if it passes correctness and hard resource limits. Penalizing an incorrect answer with a finite runtime risks selecting wrong-but-fast behavior.

### Specify the objective before searching

A scalar objective might be target-weighted latency subject to zero correctness failures and a peak-memory ceiling. Multi-objective tuning may retain a Pareto set over latency, memory, quality, energy, and cost. If the final decision uses a scalar, publish the weights and sensitivity.

Choose aggregation consciously. Arithmetic mean time emphasizes absolute work; geometric means often summarize ratios under specific positivity and weighting assumptions; tails need quantile-aware evidence; worst-case panels may be constraints rather than frequency-weighted terms. Predeclare tie-breaking, missing outcomes, and minimum practical differences.

### Split at the dependency and decision unit

Workloads derived from one graph, trace, tenant, generator base, or time window are dependent. Assign the entire group to tuning or confirmation. Seeds can also leak: selecting a configuration on fixed favorable random seeds does not estimate new-seed behavior. Split or resample seeds according to deployment.

Use time-separated confirmation when population drift matters and machine-separated confirmation when portability matters. Stratify where necessary, but never inspect confirmation outcomes to repair tuning gaps while continuing to call it untouched. After feedback, create a new version and new confirmation evidence.

### Establish untuned and simple-search baselines

Record the default, expert baseline, and a simple systematic or random search. They reveal whether optimization complexity earns its cost. Search all competing algorithms with comparable expertise, spaces, and budgets; otherwise “algorithm A beats B” may mean “A was tuned and B was not.”

Manual tuning can encode insight but is difficult to audit unless every trial and rule is recorded. Grid search is reviewable but wastes trials when only a few dimensions matter and scale is inappropriate. Random search is a strong baseline for bounded spaces and supports independent trial scheduling [2].

### Make selection optimism visible

Suppose measured tuning scores are true risks plus noise. Selecting the minimum favors negative noise. Increasing candidate count or estimate variance increases this opportunity. Repeating a benchmark until one seed wins has the same problem even when parameter values never change.

Estimate optimism by frozen holdout, repeated outer splits, nested evaluation, or a fresh future window. In nested evaluation, each outer training portion runs the complete tuner from scratch; the corresponding outer holdout evaluates its selected configuration. The result estimates the tuning procedure under that split design, not one globally fixed configuration.

### Demonstrate clean selection and confirmation

The reference selects only from tuning values, freezes the winner, and then reveals holdout. It also shows the invalid post-hoc winner obtained by pooling confirmation into selection.

<!-- bijux-verify: {"id":"tune-confirm-separation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"tuning means: [('A', 10.0), ('B', 11.0), ('C', 11.0)]\nfrozen winner: A\nholdout of frozen winner: 20.0\ninvalid pooled winner: C\n","stderr":""}} -->
```python
from statistics import mean


scores = {
    "A": {"tune": [10.0, 10.0], "holdout": [20.0]},
    "B": {"tune": [11.0, 11.0], "holdout": [11.0]},
    "C": {"tune": [9.0, 13.0], "holdout": [10.0]},
}
tuning_means = [(name, mean(values["tune"])) for name, values in sorted(scores.items())]
winner = min(tuning_means, key=lambda item: (item[1], item[0]))[0]
pooled_winner = min(
    scores,
    key=lambda name: (mean(scores[name]["tune"] + scores[name]["holdout"]), name),
)
print("tuning means:", tuning_means)
print("frozen winner:", winner)
print("holdout of frozen winner:", mean(scores[winner]["holdout"]))
print("invalid pooled winner:", pooled_winner)
```

The code verifies deterministic selection logic on fixtures. It does not quantify uncertainty or prove that the holdout represents deployment. The “invalid” result is computed only to explain leakage; it must not replace the reported frozen evaluation.

### Design the search space

Use theory, profiling, boundaries, and operational limits to bound parameters. Avoid ranges whose only purpose is to include a known winner. Express conditional structure: a partition parameter may exist only when partition strategy is selected. Reject illegal configurations before execution with exact reasons.

Ranges are hypotheses. A winner at a boundary suggests expanding the range in a new tuning version or that a monotone resource trade-off is being optimized. Dense sampling around one noisy incumbent can overfit. Preserve the original space and all subsequent revisions.

### Choose search by dimension, cost, and noise

Grid search suits very small, meaningful discrete spaces. Random search is parallel, simple, and covers more distinct values per dimension. Racing allocates small initial evidence and eliminates clearly inferior configurations, saving cost but risking premature elimination under noise or heterogeneous workloads.

Model-based optimization predicts promising configurations and uncertainty from previous trials. It can exploit interactions and expensive objectives but inherits surrogate assumptions and selection feedback. Multi-fidelity methods use smaller inputs, shorter runs, fewer seeds, or cheaper machines; low fidelity must correlate with the target and may reverse rankings at thresholds.

### Replicate and block trials

Do not give every configuration one timing. Use benchmark blocks from ALGE-092, with randomized order and appropriate process/session/machine replication. Adaptive tuners must receive a stable summary with uncertainty or repeated observations rather than arbitrary last values.

Common random numbers—using the same workload/seed block across configurations—can improve paired comparison, but preserve independence between tuning and confirmation. Record the actual execution order, failures, and resource state. Reevaluate promising candidates with stronger replication before selection.

### Treat failures as outcomes

Timeout, crash, wrong answer, memory breach, invalid configuration, and infrastructure interruption are distinct. Predeclare penalties or feasibility rules. A timeout gives a lower bound, not missing data. Early-stopping decisions are censored observations and can bias the search toward fast-starting configurations.

Racing and pruning need minimum evidence across important strata. A configuration poor on common small inputs may be essential for rare large inputs or safety constraints. Retain all partial curves and reasons. Infrastructure reruns use linked identities and symmetric rules.

### Budget adaptive search honestly

Fix the search budget in trials and relevant resource units. Wall time alone favors parallel capacity; evaluation count ignores heterogeneous costs. Report CPU/GPU/host time, failed trial consumption, preprocessing, tuner overhead, and human intervention.

Compare search methods over multiple independent optimizer seeds using the same configuration space, benchmark protocol, and budgets. An optimizer’s best run is itself selected. Use anytime performance curves and final frozen procedure performance, not one lucky trajectory.

### Examine sensitivity and plateaus

Plot performance against important parameters and interactions using held-back diagnostic or tuning evidence. A broad near-optimal plateau is usually safer than a sharp minimum: it tolerates noise, drift, and machine differences. Prefer a simpler configuration within the smallest practical difference when operational cost is lower.

Perform local perturbations around the incumbent, boundary checks, and adversarial panels. Profile changes to confirm the intended mechanism. If tiny changes reverse ranking, increase evidence and consider robust optimization across workloads or machines rather than trusting the nominal optimum.

### Guard against workload and machine overfit

Weight tuning cases by the declared target population and report strata. A configuration optimized for the mean can sacrifice tails. Use constraints or robust objectives when rare cases matter. Confirm on new workload identities, future windows, and machine classes required by the claim.

If one setting cannot serve all regimes, an algorithm portfolio or adaptive selector may be appropriate, but that expands the configuration procedure and introduces classification overhead and failure modes. Evaluate it as a new procedure on untouched evidence.

### Freeze, reproduce, and deploy

The tuning artifact contains code/build identity, space/schema, objective, constraints, workload/split manifest, trial schedule, seeds, raw measurements, failures, search state, selection rule, incumbent, and confirmation report. Store every trial, not only a visualization or optimizer database with mutable external dependencies.

Deploy the exact configuration with supported-domain checks and fallback. Monitor workload features, correctness, quality, latency, memory, failures, and distance from tuning coverage. Predeclare drift or regression triggers for retuning. Retuning creates a new candidate and consumes new confirmation evidence before promotion.

## Definitions and Notation

Let $\Lambda$ be legal configurations, $T$ tuning evidence, $H$ untouched confirmation evidence, $R(\lambda)$ target risk, and $\hat R_D(\lambda)$ empirical risk on data $D$. Let $B$ be search budget and $S(T,B,s)$ a tuning procedure with optimizer seed $s$. The evaluation target may be the procedure $S$, not just one selected $\hat\lambda$.

A **fidelity** is a cheaper approximation to the target evaluation. A **racing rule** stops or eliminates candidates using partial evidence. A **plateau** is a region within a declared practical tolerance of the best supported value. **Drift** changes target workload or environment after tuning.

## Mechanisms, Invariants, or Proof Structure

### Selection-optimism mechanism

Write $\hat R_T(\lambda)=R(\lambda)+\epsilon_\lambda$. Minimization favors configurations with low $R$ and negative noise $\epsilon$. Even when $E[\epsilon_\lambda]=0$ separately, the selected error $\epsilon_{\hat\lambda}$ need not have zero expectation. Untouched confirmation breaks this feedback for the frozen selection.

### Nested-procedure integrity

For each outer split, construct the configuration using only its outer-training evidence, including all preprocessing, feature decisions, range changes allowed by the frozen procedure, and tuning. Evaluate once on that outer holdout. Pool outer results according to the design; never tune globally before the outer loop.

### Trial-ledger integrity

Every proposed configuration receives a stable identity and terminal or partial status. The incumbent is a derived view over immutable trials under a versioned selection rule. Search recovery can resume from the ledger but cannot erase failed or superseded observations.

## Alternatives and Trade-Offs

| Strategy | Strength | Risk | Appropriate use |
|---|---|---|---|
| expert/manual | embeds mechanism knowledge | undocumented adaptation | small reviewed spaces |
| grid | deterministic coverage | dimensional waste, scale error | tiny discrete spaces |
| random | simple, parallel baseline | ignores prior outcomes | broad bounded spaces |
| racing | saves weak-candidate cost | premature censoring | reliable early evidence |
| model-based | adaptive sample efficiency | surrogate/search overfit | expensive structured spaces |
| multi-fidelity | large cost reduction | rank reversal | validated fidelities |
| robust/minimax | protects regimes | conservative typical cost | high-consequence tails |
| per-instance selector | adapts regimes | classifier and overhead risk | separable observable regimes |

Search sophistication is justified only by better confirmed decision outcomes after its cost and complexity are included.

## Failure Modes and Misconceptions

- **“The lowest validation score is the expected result.”** It is a selected noisy estimate.
- **“A holdout can be checked occasionally.”** Any feedback consumes it for that selection process.
- **“More trials cannot hurt.”** They can increase selection opportunity without fresh confirmation.
- **“Defaults are a fair baseline.”** Not when the candidate received material tuning advantage.
- **“Timeouts are missing.”** They are censored or infeasible outcomes under a declared budget.
- **“Early stopping is free.”** It favors learning curves compatible with its fidelity and rule.
- **“A boundary winner proves the optimum.”** It says the chosen space may truncate the response.
- **“The best exact value is safest.”** Broad plateaus can generalize better than noisy sharp minima.
- **“Optimizer seed does not matter.”** Adaptive search trajectories can vary materially.
- **“Retuning is maintenance only.”** It creates a new selected artifact needing new confirmation.

## Worked Examples

### Example 1

**Situation.** A tunes three configurations and A has the best tuning mean, 10 ms, but 20 ms on holdout.

**Reasoning.** Selection used only tuning evidence, so 20 ms is the honest holdout observation. Switching to B after seeing its 11 ms holdout consumes that evidence. Evaluate the revised procedure on a fresh set.

**Conclusion.** Disappointing confirmation must remain visible.

### Example 2

**Situation.** A threshold is searched at 1, 10, 100, and 1,000, while useful behavior changes around 16–64.

**Reasoning.** A coarse logarithmic grid brackets but does not resolve the transition. Use theory/pilot evidence to define a new version with values around the transition, then confirm independently. Do not insert 32 after seeing holdout.

**Conclusion.** Range refinement belongs to tuning-version governance.

### Example 3

**Situation.** The selected batch size is the maximum allowed value.

**Reasoning.** Check whether latency, memory, or fairness constraints bind. Expand the range only if legal and operationally meaningful, in a new tuning run. A monotone throughput objective may otherwise select unbounded batching.

**Conclusion.** Boundary optima often expose a missing constraint or truncated space.

### Example 4

**Situation.** Candidate A receives 1,000 optimizer trials; baseline B uses vendor defaults.

**Reasoning.** The comparison confounds algorithm and tuning effort. Give B a reviewed space and comparable budget, or frame the claim as “tuned A versus default B” and include tuning cost.

**Conclusion.** Tuning opportunity is part of treatment fairness.

### Example 5

**Situation.** A racing method drops a configuration after two small inputs, but it dominates large inputs.

**Reasoning.** The early fidelity did not preserve target ranking. Require minimum evidence per size stratum, use target weights, or design a fidelity validated for large-case behavior. Retain the censored trial.

**Conclusion.** Cheap evidence is useful only when its relation to the target is known.

### Example 6

**Situation.** Ten near-identical query traces derived from one tenant are split across tuning and confirmation.

**Reasoning.** The configuration can learn tenant-specific skew and locality. Group by tenant/base trace or time window before splitting. Sample count does not restore independence.

**Conclusion.** Split identity follows derivation and deployment generalization.

### Example 7

**Situation.** A configuration is 0.2% faster than several alternatives but highly sensitive to a one-unit threshold change.

**Reasoning.** If 0.2% is below practical importance, prefer a stable plateau configuration with simpler operations. Confirm across seeds, workloads, and machines; profile the discontinuity.

**Conclusion.** Robust near-optimality can beat a fragile nominal minimum.

### Example 8

**Situation.** An optimizer treats timeout as absent and averages only completed cases.

**Reasoning.** This rewards configurations that fail on hard inputs. Mark them infeasible or use the predeclared censoring/penalty rule, preserving timeout lower bounds and stratum identities.

**Conclusion.** Failure semantics shape the objective.

### Example 9

**Situation.** One optimizer seed finds a strong configuration and four do not.

**Reasoning.** Reporting the best trajectory selects optimizer noise. Compare procedures over independent seeds at equal resource budgets, show anytime curves, and confirm their selected configurations separately.

**Conclusion.** The optimizer is also a randomized algorithm under evaluation.

### Example 10

**Situation.** Production input sizes drift above the tuning range.

**Reasoning.** Detect coverage drift from recorded features. Activate a safe fallback or supported-domain guard, run a new versioned tuning campaign including the new regime, and use fresh confirmation before promotion.

**Conclusion.** Deployment monitoring closes the tuning lifecycle.

## Cross-Program Connections

- [Data Structures Engineering DSE-010](../../17-data-structures-engineering/modules/010-benchmarking-a-structure-without-misleading-results.md) supplies representation-level tuning context.
- [Software Testing and Quality Engineering STQE-002](../../13-software-engineering-testing-and-quality-engineering/modules/002-specifications-expectations-and-test-oracles.md) protects semantic constraints during optimization.
- [Large-Scale Data Systems Engineering LSDS-097](../../21-large-scale-data-systems-engineering/modules/097-cluster-benchmarking.md) exposes configuration transfer across cluster states.
- [Concurrent and Parallel Programming CONPAR-092](../../04-programming-languages-concurrent-and-parallel-programming/modules/092-roofline-and-operational-intensity-analysis.md) provides model-based parameter bounds.
- [Platform Engineering PLAT-091](../../29-platform-engineering/modules/091-platform-discovery-and-product-research.md) connects configuration choices to supported platform products.
- [Systems Engineering SYSENG-043](../../26-systems-engineering/modules/043-cost-schedule-performance-and-risk.md) places tuning budget inside broader decision cost.

## References

1. Gavin C. Cawley and Nicola L. C. Talbot, “On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation,” *Journal of Machine Learning Research* 11, 2010, 2079–2107. [JMLR record](https://www.jmlr.org/papers/v11/cawley10a.html). Checked 2026-09-05.
2. James Bergstra and Yoshua Bengio, “Random Search for Hyper-Parameter Optimization,” *Journal of Machine Learning Research* 13, 2012, 281–305. [JMLR record](https://www.jmlr.org/papers/v13/bergstra12a.html). Checked 2026-09-05.
3. Frank Hutter, Holger H. Hoos, Kevin Leyton-Brown, and Thomas Stützle, “ParamILS: An Automatic Algorithm Configuration Framework,” *Journal of Artificial Intelligence Research* 36, 2009, 267–306. [doi:10.1613/jair.2861](https://doi.org/10.1613/jair.2861). Checked 2026-09-05.
4. Frank Hutter, Holger H. Hoos, and Kevin Leyton-Brown, “Sequential Model-Based Optimization for General Algorithm Configuration,” *LION 5*, 2011, 507–523. [doi:10.1007/978-3-642-25566-3_40](https://doi.org/10.1007/978-3-642-25566-3_40). Checked 2026-09-05.
5. Sudhir Varma and Richard Simon, “Bias in Error Estimation When Using Cross-Validation for Model Selection,” *BMC Bioinformatics* 7:91, 2006. [doi:10.1186/1471-2105-7-91](https://doi.org/10.1186/1471-2105-7-91). Checked 2026-09-05.
6. Matthias Feurer and Frank Hutter, “Hyperparameter Optimization,” in *Automated Machine Learning*, Springer, 2019, 3–33. [doi:10.1007/978-3-030-05318-5_1](https://doi.org/10.1007/978-3-030-05318-5_1). Checked 2026-09-05.
7. Thomas Bartz-Beielstein et al., *Experimental Methods for the Analysis of Optimization Algorithms*, Springer, 2010. ISBN 978-3-642-02537-2.
8. Raj Jain, *The Art of Computer Systems Performance Analysis*, Wiley, 1991. ISBN 978-0-471-50336-1.

## Exercises

### Exercise 1

Define configuration space, tuning set, confirmation set, incumbent, budget, selection bias, and nested evaluation for choosing a sorting cutoff.

### Exercise 2

Configurations A, B, and C have tuning times [10, 12], [9, 14], and [11, 11] ms. Apply mean-time selection with lexicographic tie-breaking, then explain how to use one holdout observation per configuration.

### Exercise 3

A tuner prunes every run exceeding 10 seconds on small inputs and reports only completed scores. Diagnose the statistical and operational defects and repair the policy.

### Exercise 4

Compare grid, random, racing, and model-based search for six parameters with a 200-trial budget and heterogeneous evaluation costs.

### Exercise 5

Design an end-to-end tuning procedure for an external sort’s memory limit, run size, fan-in, compression, parallelism, and fallback. Include constraints, splits, objectives, search, replication, failures, confirmation, deployment, and retuning.

## Answers to the Exercises

### Answer 1

The space enumerates legal cutoff values and any conditional strategy settings. The tuning set supplies workload/run evidence used to select; confirmation remains untouched until the winner is frozen. The incumbent is the best configuration under the current declared rule, and budget limits trials or resources. Selection bias is optimism from treating the minimum tuning estimate as fresh evaluation. Nested evaluation repeats the full cutoff search within each outer training split and measures its selected cutoff on that split’s outer holdout, thereby evaluating the procedure.

### Answer 2

Means are A=11, B=11.5, and C=11 ms. With lexicographic tie-breaking, A is selected over C. Freeze A, reveal and report A’s holdout result as the primary confirmation. Results for B and C may be retained for prespecified secondary diagnostics, but using them to switch the winner consumes the holdout for that revised choice. A new untouched set or outer evaluation is required to assess a new selection rule. The small sample also demands uncertainty and practical-effect caution.

### Answer 3

The policy censors hard cases, rewards configurations that fail to finish, and provides no lower bounds or failure rates. Define timeout as a terminal censored outcome and either make any timeout infeasible, use a predeclared penalty at least consistent with the bound, or use censoring-aware selection. Require minimum evidence across target strata before pruning, preserve partial observations and reasons, and distinguish infrastructure interruption from algorithm timeout. Apply the rule symmetrically, validate cheap-fidelity ranking, and confirm the frozen procedure on untouched cases.

### Answer 4

A full grid is infeasible unless each dimension has very few meaningful levels, and it poorly covers continuous six-dimensional space. Random search is the required simple, parallel baseline and handles failures cleanly with recorded independent proposals. Racing can move budget away from weak candidates but needs reliable partial evidence and stratum floors. Model-based search can exploit interactions and heterogeneous costs, but surrogate assumptions and adaptive overfit require multiple optimizer seeds. Use mechanism-informed transforms/conditions, a random baseline, then racing or cost-aware model-based proposals only after validating fidelity; compare procedures at equal CPU/host/trial budgets with untouched confirmation.

### Answer 5

Define legal ranges and conditional fallback, with correctness/permutation/stability, memory, storage, and failure constraints preceding time. Group derived files and machine sessions into tuning and confirmation; preserve rare spill/adversarial panels as constraints. Optimize target-weighted end-to-end wall time with secondary CPU, I/O, peak memory, and cost, using log scales for capacities and categorical compression. Start with default/expert and random baselines, then a budgeted conditional optimizer. Use randomized matched blocks, multiple processes/sessions and relevant machines; retain timeouts, ENOSPC, wrong answers, prunes, and interruptions. Reevaluate finalists with stronger replication, freeze the selection rule/winner, and evaluate once on untouched workloads/time/machines. Deploy exact values with range guards and conservative fallback; monitor feature coverage, memory, I/O, correctness, and tails. Any drift-triggered retuning creates a new artifact and requires fresh confirmation.
