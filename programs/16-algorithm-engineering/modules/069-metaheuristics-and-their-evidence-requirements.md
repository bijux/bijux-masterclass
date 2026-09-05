---
module_id: ALGE-069
program: Algorithm Engineering
level: 2
module_number: 69
title: Metaheuristics and Their Evidence Requirements
status: complete
last_verified: 2026-09-05
---

# Metaheuristics and Their Evidence Requirements

## One-Page Review

### Governing question

How can a metaheuristic be specified, tuned, compared, and deployed when its practical value may be substantial but its solution quality is usually supported by conditional empirical evidence rather than a universal approximation theorem?

### Essential definitions

- A **heuristic** is a problem-solving rule intended to produce useful solutions without necessarily proving optimality or a uniform quality bound.
- A **metaheuristic** is a higher-level search framework that coordinates construction, local improvement, memory, randomization, intensification, and diversification.
- A **trajectory method** evolves one incumbent; a **population method** evolves several candidates and information among them.
- **Intensification** searches near promising states; **diversification** directs work toward underexplored regions.
- A **fixed-budget** experiment compares quality after the same declared resource budget; a **fixed-target** experiment compares resources required to attain the same target.
- A **run** is one algorithm-instance-configuration-seed execution with an immutable input and complete outcome, including timeout or failure.
- An **instance distribution** is the operational or scientific population about which conclusions are intended.
- A **tuning set**, **validation set**, and **test set** serve configuration selection, design decisions, and final estimation respectively.
- An **anytime trace** records best verified objective versus consumed resource.
- **Selection bias** arises when the same observations are used both to choose a method or configuration and to estimate its performance.

### Central model, mechanism, or theorem

For minimization, simulated annealing proposes a neighbor with objective change $\Delta=f(S')-f(S)$ and accepts it with probability

$$
P(\text{accept})=
\begin{cases}
1,&\Delta\le0,\\
e^{-\Delta/T},&\Delta>0,
\end{cases}
$$

for temperature $T>0$. This mechanism can cross local barriers, but a finite schedule does not by itself prove global optimality.

If $k$ independent runs return continuous identically distributed objective values uniformly on $[0,1]$, their expected minimum is $1/(k+1)$ rather than the single-run mean $1/2$. Reporting only the best of many runs therefore changes the algorithmic budget and creates optimism. Compare equal run portfolios, report the whole distribution, and preserve every run.

No-free-lunch results average over highly broad function classes under specific closure and weighting assumptions. Their engineering implication is to state the problem structure a method exploits—not that all algorithms perform equally on a relevant operational distribution.

### Critical invariants

- Every published incumbent is feasible under the original model and has an independently recomputed objective.
- The best-so-far trace is monotone in the correct direction, even when the current search state worsens.
- Budgets include initialization, repair, preprocessing, evaluation, parallel resources, and failures under one declared accounting rule.
- Tuning never consumes final test outcomes; configuration count and selection rule are recorded.
- Every algorithm sees the same immutable instance and equivalent information.
- Stochastic comparisons use enough independent runs and preserve paired blocks where pairing is justified.
- Timeouts, crashes, infeasibility, and missing results remain in the dataset.
- Claims name the instance population, metric, budget, uncertainty, hardware, code, and limits of generalization.

### Common failures

Common failures include treating biological or physical metaphor as evidence; comparing a tuned method against default baselines; giving one method more objective evaluations or cores; reporting only best seeds; tuning on the test set; counting repaired infeasible proposals as free; using different stopping tolerances; dropping timeouts; substituting a solver's claimed objective for independent recomputation; applying an unpaired test to paired instances without justification; interpreting a nonsignificant result as equivalence; running many comparisons and reporting only winners; and claiming universal superiority from one convenient benchmark suite.

### Compact example

For a worsening move $\Delta=2$ at $T=2$, the acceptance threshold is $e^{-1}\approx0.367879$. A uniform draw 0.2 accepts it; draw 0.8 rejects it. This verifies one transition rule. It does not show that the cooling schedule, neighborhood, or whole algorithm finds high-quality solutions.

### Connections

[ALGE-065](./065-local-search.md) supplies neighborhoods, deltas, and local-optimum semantics. [ALGE-068](./068-monte-carlo-and-las-vegas-algorithms.md) reserves Monte Carlo for proved error bounds. [ALGE-070](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) chooses among exact, approximate, and heuristic solution routes.

## Governing Question

Given a difficult optimization problem and a metaheuristic candidate, how do we define its search state and resource contract, prevent tuning and benchmark bias, quantify stochastic performance, compare credible alternatives, and report only conclusions supported by the tested instance population?

A metaheuristic is not made rigorous by a long name, natural metaphor, or pseudocode. Rigor comes from executable semantics and disciplined evidence. The neighborhood, proposal distribution, memory, update order, repair, initialization, stopping rule, parameter schedule, and random stream jointly define the method. The instance sampling, baselines, budgets, replications, metrics, analysis, and held-out evaluation jointly define what can be learned about it.

## Why This Matters

Production optimization often contains nonlinear business rules, large combinatorial spaces, uncertain data, and hard deadlines. Exact solvers may not prove optimality in time; known approximation algorithms may not fit the model; simple local search may stall. Metaheuristics can provide strong feasible incumbents, exploit domain structure, and improve continuously under a budget.

Their flexibility creates a large researcher degree of freedom. A method can look excellent after enough parameter trials, seeds, instance exclusions, baselines, and metrics. Wall-clock comparisons can hide hardware and parallelism. A tiny mean improvement can coexist with damaging tail failures. A repair operator can silently solve most of the problem. Without a governed experiment, apparent progress may be tuning luck.

The durable discipline is to treat a metaheuristic as a conditional engineering hypothesis: under a specified workload and budget, this completely specified implementation has a measured distribution of verified outcomes relative to named alternatives.

## Prerequisites and Retrieval

Retrieve [ALGE-065](./065-local-search.md), [ALGE-068](./068-monte-carlo-and-las-vegas-algorithms.md), stochastic processes, experimental design, confidence intervals, hypothesis tests, optimization gaps, exact feasibility checking, random streams, performance measurement, and reproducible builds.

This chapter surveys simulated annealing, tabu search, evolutionary methods, and ant-colony methods only far enough to expose their common specification and evidence obligations. It does not claim that one family dominates. Detailed statistical algorithm comparison and automated parameter tuning recur in ALGE-095 and ALGE-096; domain-specific optimization models remain with their owning programs.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a heuristic, metaheuristic, approximation algorithm, and Monte Carlo algorithm;
2. specify trajectory and population search as reproducible state machines;
3. explain intensification, diversification, memory, acceptance, and repair without relying on metaphor;
4. validate feasibility, objective values, and best-so-far traces independently;
5. design fair fixed-budget and fixed-target comparisons;
6. separate tuning, validation, and final test data;
7. analyze stochastic runs with paired effects, uncertainty, failures, and multiplicity;
8. identify best-of-run, survivor, benchmark, and baseline bias;
9. build evidence for ablations, scaling, robustness, and operational drift; and
10. state a bounded conclusion that identifies its instance population and deployment risks.

## Core Exposition

### Specify the optimization and evidence targets first

Define feasible set $F$, objective $f:F\to\mathbb R$, minimization or maximization direction, constraint and objective arithmetic, and tie semantics. If the real goal includes risk, fairness, churn, or constraint-violation cost, encode it explicitly rather than optimizing one surrogate and describing another outcome.

Define the estimand: expected verified gap after $10^6$ objective evaluations on next quarter's order distribution; probability of reaching a 2% gap within 30 seconds on a declared hardware class; or median time to a certified target on a public suite. “Algorithm A is better” omits instances, metric, budget, and aggregation.

A known optimum gives gap $g=(f-f^*)/\max(1,|f^*|)$ for minimization only when this normalization is meaningful. If only a lower bound $L\le f^*$ is known, $f-L$ is a certified absolute gap but not the unknown optimality gap. For maximization, signs and denominator choices must be re-derived. Publish raw objectives and bounds so alternative normalizations can be checked.

### Define the metaheuristic state machine

A trajectory method maintains current state $S_t$, incumbent $B_t$, memory $M_t$, control parameters $\theta_t$, and random-stream state. A complete transition specifies proposal, evaluation, feasibility or repair, acceptance, incumbent update, memory update, parameter update, and termination.

Tabu search uses adaptive memory to prohibit or penalize attributes of recent moves, commonly with an aspiration rule. The tabu tenure, attribute identity, expiration order, and aspiration tie rule are semantics. Simulated annealing sometimes accepts worsening moves using temperature. Evolutionary methods select, recombine, mutate, evaluate, and replace populations. Ant-colony methods construct solutions from pheromone and heuristic information, then update pheromone. Names do not fix any of these operators.

The incumbent invariant for minimization is $B_t\in F$ and $f(B_{t+1})\le f(B_t)$. The current state may worsen or become temporarily infeasible if the method permits it, but published best-so-far data must be independently feasible and monotone. Transactionally commit candidate, objective, feasibility proof, and trace event so cancellation cannot publish mismatched state.

### Understand one mechanism without inflating its claim

Simulated annealing accepts every nonworsening move and accepts a worsening change $\Delta>0$ when uniform $U<e^{-\Delta/T}$. Temperature therefore controls exploration relative to objective scale. Multiplying all objective values by 100 while retaining $T$ changes behavior drastically. Units, scaling, schedule, reheating, and minimum temperature belong to the configuration.

<!-- bijux-verify: {"id":"annealing-acceptance-and-incumbent","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"worse threshold=0.367879 low=True high=False\nimproving=True frozen_worse=False\nbest=(12, 9, 9, 7)\ninvalid_draw=rejected\n","stderr":""}} -->
```python
from math import exp


def accept(delta, temperature, draw):
    if not 0.0 <= draw < 1.0:
        raise ValueError("draw outside [0,1)")
    if delta <= 0:
        return True
    if temperature <= 0:
        return False
    return draw < exp(-delta / temperature)


def best_so_far(values):
    best = values[0]
    trace = []
    for value in values:
        best = min(best, value)
        trace.append(best)
    return tuple(trace)


threshold = exp(-2 / 2)
print(f"worse threshold={threshold:.6f} low={accept(2, 2, 0.2)} high={accept(2, 2, 0.8)}")
print(f"improving={accept(-1, 0, 0.9)} frozen_worse={accept(1, 0, 0.0)}")
print(f"best={best_so_far((12, 9, 11, 7))}")
try:
    accept(1, 1, 1.0)
except ValueError:
    print("invalid_draw=rejected")
```

The executable transcript verifies the stated rule and incumbent trace on CPython. It provides no global convergence or comparative quality evidence. Classical asymptotic convergence results require specific Markov-chain and cooling assumptions; a finite production schedule needs empirical evaluation on the relevant workload.

### Treat domain structure as the source of advantage

Metaheuristics succeed by exploiting structure: useful neighborhoods, decomposable constraints, correlated nearby objectives, meaningful recombination, informative memory, or repair that maps proposals to good feasible regions. The no-free-lunch results do not say every method is equal on a structured instance distribution. They warn that superiority cannot be universal without assumptions about the function class and sampling measure.

Document those assumptions. A routing neighborhood assumes exchanging or reversing arcs exposes useful local gradients. Genetic recombination assumes candidate components can be inherited without destroying most value. Pheromone learning assumes repeated components convey information across constructed solutions. Test these claims through ablations and instance features, not metaphor.

If a repair operator converts arbitrary strings into feasible schedules, measure its time and its standalone quality. Repair may be the dominant constructive heuristic. Comparing a repaired population method with an unrepaired baseline confounds framework and repair.

### Fix the budget as part of the algorithm

Common budgets include objective evaluations, neighbor evaluations, exact-solver calls, CPU time, wall time, energy, memory, and cores. None is universally fair. Objective evaluations can have unequal cost; wall time is hardware-sensitive; CPU time undercounts accelerators; equal iterations mean different work across population sizes.

Report at least one machine-independent work counter and observed wall time when practical. Include preprocessing, compilation or warmup policy, initialization, feasibility repair, objective recomputation, communication, checkpointing, and cleanup according to a declared boundary. If parallel methods use $p$ workers, report both wall time and aggregate resource consumption.

Fixed-budget experiments compare final or anytime quality at a common resource limit. Fixed-target experiments compare time or evaluations to the same verified target. Targets must not favor one method's stopping tolerance. If a target is never reached, the observation is right-censored, not missing and not equal to the timeout unless the chosen estimator explicitly defines a penalized runtime.

### Design the instance population

A benchmark suite is a sample, not the universe. State how instances were generated or collected, their feature ranges, duplicates, scaling, provenance, and relationship to deployment. Include easy, hard, small, large, structured, adversarial, and edge cases in proportions connected to the intended conclusion.

Split at the correct unit. If many instances derive from one customer, graph, day, or generator seed, random row splitting leaks family information. Hold out entire groups or time periods. Deduplicate near-identical instances across tuning and test sets. Freeze test instances and their optimal values or bounds before final evaluation.

Public benchmarks support comparison but invite community-level overfitting. Complement them with procedurally generated held-out instances or a protected operational sample. Report benchmark exclusions and parse failures rather than silently shrinking the suite.

### Separate development, tuning, and estimation

Use tuning data to select configuration, validation data for limited design choices, and a untouched test set for final estimation. Repeatedly checking the test set during development converts it into validation data; obtain a new holdout or narrow the claim.

Configuration budget matters. Selecting the best of 1,000 parameter settings gives a method more search over algorithms than a baseline tested once. Match tuning effort, use strong published or carefully tuned baselines, and report search space, tuner, budget, seeds, early stopping, and selected configuration. Nested evaluation keeps configuration choice inside each training fold and estimates it outside.

Avoid changing the hypothesis after seeing outcomes. Predeclare primary metric, aggregation, comparison family, exclusion rules, stopping rule, and uncertainty method. Exploratory analyses are valuable when labeled exploratory and confirmed on new data.

### Respect stochastic replication and pairing

One run estimates one draw, not a distribution. Choose repetitions using the precision or power needed for the primary estimand, informed by pilot variance that is not reused as final evidence without adjustment. Retain every seed and outcome.

Block by instance because instance difficulty often dominates algorithm differences. For each instance, compare methods under a balanced run plan. Common random numbers can reduce variance when they induce positive correlation, but “seed 7” need not represent comparable random decisions across different algorithms. Pair on the experimental unit that has a defensible shared disturbance; otherwise use independent streams and instance-level pairing.

Analyze paired differences and effect sizes with uncertainty. Means answer an expectation question but can be tail-sensitive; medians answer a different question and can hide catastrophic failures. Quantiles, success probabilities, empirical attainment curves, and fixed-target distributions often expose operational behavior. A nonsignificant difference is not evidence of equivalence; equivalence requires a practical margin and suitable design.

Multiple instances, metrics, variants, and pairwise tests create multiplicity. Declare the primary comparison and use appropriate family-wise or false-discovery control for confirmatory secondary claims. Do not report only favorable subsets.

### Prevent best-of-run and survivor bias

If $X_1,\ldots,X_k$ are independent uniform values on $[0,1]$ for minimization, then

$$
\Pr[\min_iX_i>x]=(1-x)^k,
\qquad
\mathbb E[\min_iX_i]=\int_0^1(1-x)^kdx=\frac1{k+1}.
$$

Twenty runs therefore have expected best $1/21$, despite each run having mean $1/2$. Best-of-20 is a legitimate portfolio if its 20-run cost is included and every competitor receives an equivalent portfolio. It is misleading when presented as a typical single run.

Dropping crashes or infeasible outputs creates survivor bias. Treat them as outcomes. For quality-at-budget, define the penalty or failure category before results. For time-to-target, use methods that retain censoring. Report denominator counts so success rates cannot silently exclude failures.

### Compare across heterogeneous instances

Raw objective values across unrelated instances may not be commensurate. Use verified relative gaps when reliable references exist, within-instance ranks with appropriate caution, or target attainment. Performance profiles define, for each method, the fraction of instances whose performance ratio is within factor $\tau$ of the best observed method. They visualize robustness and efficiency but inherit metric, failure-penalty, and benchmark choices.

Do not reduce the entire study to average rank without effect magnitude. Report per-instance or grouped effects and identify features associated with wins and failures. If instance classes were discovered after results, label the subgroup analysis exploratory.

Scaling experiments vary one or more size/structure dimensions and measure work, memory, and quality. A log-log line over a narrow range is not a complexity proof. Separate initialization from search and show whether solution quality degrades as size grows under fixed and scaled budgets.

### Use ablation and mechanism checks

An ablation removes or replaces one component while holding the rest fixed: tabu memory, crossover, pheromone evaporation, reheating, adaptive penalties, or domain repair. Factorial designs reveal interactions that one-at-a-time ablations miss. Use the same tuning discipline for variants; an untuned ablation versus a tuned full method exaggerates contribution.

Mechanism traces can falsify stories. Measure accepted worsening moves across temperature, tabu overrides, population diversity, repair frequency, pheromone entropy, neighborhood hit rates, and incumbent improvements. A component that never activates cannot explain gains. A diversity metric that changes without predicting useful exploration is descriptive, not causal.

Oracle studies on small instances compare against exact optima and enumerate neighborhoods. They test implementation and expose gap distributions, but small-instance conclusions may not transfer. Metamorphic tests preserve known relations under relabeling, objective scaling, duplicated neutral elements, and equivalent representations.

### Move from benchmark to production cautiously

Shadow evaluation uses immutable production snapshots and prevents search output from affecting the data used to judge it. Before actuation, enforce independent feasibility, objective recomputation, safety constraints, and rollback. Compare against the incumbent policy using decision-relevant outcomes, not only the optimizer's surrogate objective.

Monitor instance features, feasibility failures, objective distributions, latency, budget exhaustion, fallback, and regret proxies for drift. A configuration selected last quarter may degrade when constraints or data collection change. Predetermine rollback thresholds and retain the prior solver path.

Reproducibility requires source revision, build, dependencies, hardware, compiler/interpreter, configuration, instance digests, seed derivation, run order, budget counters, raw results, and analysis code. A seed without generator version and immutable input is not a replay recipe. Privacy or licensing may prevent raw instance release; publish generators, schemas, hashes, and controlled-access procedures where possible.

## Definitions and Notation

| Term | Precise use in this chapter |
|---|---|
| $F$ | Feasible solution set under the original model |
| $f(S)$ | Independently recomputable objective of solution $S$ |
| $S_t$ | Current search state at transition $t$ |
| $B_t$ | Best verified feasible incumbent through transition $t$ |
| $\theta$ | Complete algorithm configuration, including schedules and ties |
| $\Delta$ | Proposed objective change $f(S')-f(S)$ for minimization |
| $T$ | Annealing temperature, not elapsed time |
| fixed budget | Quality comparison at equal declared resource consumption |
| fixed target | Resource comparison to equal verified quality |
| censoring | Target time is known only to exceed the observation budget |
| paired difference | Within-block outcome difference for two methods |
| ablation | Controlled removal or replacement of a method component |
| estimand | Exact population quantity an experiment aims to estimate |

A **model** defines feasible solutions, objectives, instances, and target population. A **mechanism** proposes, accepts, repairs, remembers, and updates. A **guarantee** may establish feasibility or termination but usually not global quality. An **implementation** fixes data structures, parallel order, arithmetic, and random streams. A **policy** selects budgets, tuning, fallback, and deployment thresholds. **Evidence** is conditional on experimental design and cannot be expanded beyond the sampled population without assumptions.

## Mechanisms, Invariants, or Proof Structure

### Search-state invariants

- configuration and immutable instance digest bind every event;
- current state follows the declared transition and memory rules;
- every incumbent is feasible and independently rescored;
- best-so-far objective is monotone in the declared direction;
- budget counters advance for every charged operation, including rejected and repaired proposals;
- random substreams are uniquely derived and replayable; and
- cancellation or crash cannot publish an uncommitted candidate.

### Confirmatory experiment checklist

1. Define the instance population and sampling unit.
2. Freeze primary estimand, metric, budget, baselines, and hypotheses.
3. Isolate tuning, validation, and test groups at the leakage-resistant unit.
4. Match configuration opportunity and compute resources.
5. Choose independent repetitions and defensible paired blocks.
6. Retain failures and censoring; recompute feasibility and objectives.
7. Estimate effect size and uncertainty; control confirmatory multiplicity.
8. Publish raw run ledger, analysis, versions, exclusions, and limitations.

### Evidence hierarchy

Universal proofs may establish feasibility preservation, finite termination under a move budget, or properties of a transition kernel. Exact small-instance oracles test correctness and gap. Controlled held-out experiments estimate performance for a sampled distribution. Shadow production validates a closer distribution without proving future behavior. Live monitoring detects drift after deployment. These layers complement rather than replace one another.

## Alternatives and Trade-Offs

| Method family | Exploration mechanism | Main strength | Main evidence risk |
|---|---|---|---|
| Multi-start local search | Independent or diversified starts | Simple, parallel, strong baseline | Best-of-many budget hidden |
| Simulated annealing | Temperature-controlled worsening moves | Escapes barriers with compact state | Schedule and scale dominate behavior |
| Tabu search | Adaptive prohibition and aspiration memory | Avoids short cycles; uses search history | Attribute/tenure choices underreported |
| Evolutionary search | Population selection, recombination, mutation | Combines diversity and building blocks | Population cost and operator tuning hidden |
| Ant-colony method | Learned component trails plus construction | Shares information across solutions | Metaphor substitutes for mechanism evidence |
| Large-neighborhood search | Destroy and repair substantial regions | Strong domain integration | Repair may be the real solver |
| Exact solver | Bounds, proof, systematic search | Optimality or certified gap | May miss deadline; configuration still matters |
| Approximation algorithm | Proven worst-case quality | Distribution-independent factor | Bound may be loose or model-specific |

A strong experimental baseline suite often includes simple construction, local search, multi-start, a mature exact solver with time limit, and the best relevant published approach. Complexity is justified only by held-out effect, robustness, or operational value after equal accounting.

## Failure Modes and Misconceptions

- **“Nature-inspired means effective.”** Inspiration proposes operators; only proof or controlled evidence supports performance.
- **“Metaheuristic means Monte Carlo.”** Without a proved error event and probability bound, the correct label is randomized heuristic.
- **“Best known means optimal.”** It is an incumbent relative to searched methods and budgets unless certified.
- **“Same seconds is always fair.”** Hardware, cores, warmup, language, and evaluation boundaries must also match.
- **“Same number of iterations is fair.”** Iterations can contain radically different populations, evaluations, and repairs.
- **“More seeds solve uncertainty.”** Biased instances, test leakage, or correlated streams remain biased with more runs.
- **“The test set can guide tuning once.”** Any guidance consumes holdout information.
- **“Timeout is missing data.”** It is an observed failure or censored target time and must remain in analysis.
- **“Nonsignificant means equal.”** Lack of evidence for difference is not evidence within a practical equivalence margin.
- **“Average rank shows magnitude.”** Ranks discard how large and operationally meaningful differences are.
- **“Ablation proves causality automatically.”** Retuning and component interactions can confound the comparison.
- **“No free lunch means stop comparing.”** It means advantages depend on a declared, structured problem distribution.

## Worked Examples

### Example 1

**Situation.** A worsening annealing move has $\Delta=2$ and $T=2$; draws are 0.2 and 0.8.

**Reasoning.** The acceptance threshold is $e^{-2/2}=e^{-1}\approx0.367879$. Since $0.2$ is below it, that transcript accepts. Since $0.8$ is above it, the other rejects. At $T=0$, the defined implementation rejects every worsening move rather than dividing by zero.

**Conclusion.** Transition behavior is reproducible, but two transitions do not establish solution quality.

### Example 2

**Situation.** Objective units change from dollars to cents while the annealing schedule is unchanged.

**Reasoning.** Every positive $\Delta$ is multiplied by 100, so $e^{-\Delta/T}$ may become nearly zero. The method changes from exploratory to nearly greedy even though the business problem is equivalent. Scaling $T$ by 100 preserves the acceptance ratio, subject to numerical representation.

**Conclusion.** Temperature has objective units; normalization and schedule belong to reproducible semantics.

### Example 3

**Situation.** Twenty independent minimization runs have uniform outcome on $[0,1]$, and a paper reports only their best.

**Reasoning.** A single run has expectation $1/2$. The expected minimum of 20 is $1/(20+1)=1/21\approx0.0476$. The apparent gain comes entirely from spending 20-run budget and selecting an extreme.

**Conclusion.** Best-of-20 is a portfolio result and must be compared with equal portfolios, not typical single runs.

### Example 4

**Situation.** Configuration A wins on a benchmark after 200 settings were tried; baseline B used its default.

**Reasoning.** The comparison confounds algorithm family with configuration-search budget and benchmark overfitting. Give both methods credible matched tuning, isolate configuration selection from a held-out final test, and report all search spaces and trials.

**Conclusion.** The observed win does not isolate A's algorithmic contribution.

### Example 5

**Situation.** On five held-out instances, A-minus-B gaps are $(-4,-1,0,2,3)$ percentage points for minimization.

**Reasoning.** Pairing by instance removes the common instance level. The mean paired effect is zero, but the distribution reveals heterogeneous wins and losses. Five blocks give wide uncertainty and little power; reporting only the mean would hide operational variation.

**Conclusion.** Preserve paired effects, uncertainty, and instance features rather than announcing a tie from one aggregate.

### Example 6

**Situation.** At a 60-second fixed-target test, run times are 12, 20, 41, and two timeouts.

**Reasoning.** The last two observations mean time exceeds 60; they are right-censored. Averaging only 12, 20, and 41 creates survivor bias. Replacing each timeout by 60 is a declared penalized-runtime metric, not the observed mean hitting time.

**Conclusion.** Retain censoring and report success probability as well as conditional successful times.

### Example 7

**Situation.** Costs for A and B on one instance are 30 and 10 seconds; on another they are 40 and timeout at 100.

**Reasoning.** On the first instance, ratios to best are 3 and 1. On the second, A's ratio is 1 and B receives the predetermined failure ratio or infinity. A performance profile at $\tau=1$ shows each method best on half the instances; at $\tau=3$, A covers both while B still has one failure.

**Conclusion.** Profiles expose efficiency and robustness but depend on failure and ratio definitions.

### Example 8

**Situation.** An evolutionary method repairs infeasible schedules with a greedy scheduler, while its baseline discards infeasible proposals.

**Reasoning.** Repair consumes compute and embeds strong domain decisions. Measure its calls and cost, test greedy repair alone, and compare a baseline with access to the same repair. Otherwise the experiment attributes repair quality to evolutionary recombination.

**Conclusion.** Shared supporting components and ablations are necessary for a causal mechanism claim.

### Example 9

**Situation.** Removing either tabu memory or adaptive tenure hurts little, but removing both hurts greatly.

**Reasoning.** The components interact: either can supply sufficient diversification alone. One-at-a-time ablations from the full method understate their substitutable contribution. A $2\times2$ factorial design estimates main effects and interaction, with variants tuned under the same budget.

**Conclusion.** Component value may be conditional on other components; factorial evidence can reveal it.

### Example 10

**Situation.** A routing metaheuristic improves offline distance by 3% but in shadow production produces 8% more late deliveries.

**Reasoning.** Distance was an incomplete surrogate or the data distribution shifted. Independently recompute constraints and decision outcomes, segment by instance features, keep the incumbent route active, and revise the model before actuation. Do not tune directly on the shadow holdout and report it as final evidence.

**Conclusion.** Deployment requires decision-valid outcomes, rollback, and new confirmation—not loyalty to benchmark gains.

## Cross-Program Connections

- **Software Testing and Quality Engineering:** experiment plans, oracles, metamorphic properties, uncertainty, equivalence, and multiplicity govern credible comparison.
- **Data Engineering:** immutable instance snapshots, provenance, leakage-resistant splits, and complete run ledgers protect evidence lineage.
- **Data Architecture Engineering:** objective and constraint semantics must match governed business meaning rather than a convenient surrogate.
- **Software Delivery and Reliability Engineering:** resource isolation, timeouts, fallback, shadowing, rollback, and telemetry control production risk.
- **Systems Engineering:** hardware, concurrency, memory, and energy determine the real cost of a search portfolio.
- **Security Engineering:** adversarial instances, seed exposure, benchmark poisoning, and artifact integrity can invalidate evaluation assumptions.
- **Algorithm Engineering:** [ALGE-065](./065-local-search.md) provides local mechanisms; [ALGE-068](./068-monte-carlo-and-las-vegas-algorithms.md) defines theorem-backed randomized classes; [ALGE-070](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) governs solution-method selection.

## References

1. S. Kirkpatrick, C. D. Gelatt Jr., and M. P. Vecchi, “Optimization by Simulated Annealing,” *Science* 220(4598), 1983, 671–680. DOI: [10.1126/science.220.4598.671](https://doi.org/10.1126/science.220.4598.671). Primary source for the simulated-annealing optimization framework; publisher record checked 2026-09-05.
2. Fred Glover, “Future Paths for Integer Programming and Links to Artificial Intelligence,” *Computers & Operations Research* 13(5), 1986, 533–549. DOI: [10.1016/0305-0548(86)90048-1](https://doi.org/10.1016/0305-0548(86)90048-1). Primary source introducing tabu-search directions; publisher record checked 2026-09-05.
3. Marco Dorigo, Vittorio Maniezzo, and Alberto Colorni, “Ant System: Optimization by a Colony of Cooperating Agents,” *IEEE Transactions on Systems, Man, and Cybernetics—Part B* 26(1), 1996, 29–41. DOI: [10.1109/3477.484436](https://doi.org/10.1109/3477.484436). Primary source for Ant System; bibliographic record checked 2026-09-05.
4. A. E. Eiben and J. E. Smith, *Introduction to Evolutionary Computing*, 2nd ed., Springer, 2015. DOI: [10.1007/978-3-662-44874-8](https://doi.org/10.1007/978-3-662-44874-8). Textbook reference for evolutionary algorithm components, parameter control, and evaluation; publisher record checked 2026-09-05.
5. John N. Hooker, “Testing Heuristics: We Have It All Wrong,” *Journal of Heuristics* 1, 1995, 33–42. DOI: [10.1007/BF02430364](https://doi.org/10.1007/BF02430364). Primary methodological critique of heuristic testing; record checked 2026-09-05.
6. Elizabeth D. Dolan and Jorge J. Moré, “Benchmarking Optimization Software with Performance Profiles,” *Mathematical Programming* 91, 2002, 201–213. DOI: [10.1007/s101070100263](https://doi.org/10.1007/s101070100263). Primary source for performance profiles; publisher record checked 2026-09-05.
7. David H. Wolpert and William G. Macready, “No Free Lunch Theorems for Optimization,” *IEEE Transactions on Evolutionary Computation* 1(1), 1997, 67–82. DOI: [10.1109/4235.585893](https://doi.org/10.1109/4235.585893). Primary source for no-free-lunch results and their assumptions; record checked 2026-09-05.

## Exercises

### Exercise 1

Classify these statements as a mechanism, theorem, empirical claim, or policy: (a) worsening moves are accepted with probability $e^{-\Delta/T}$; (b) every published incumbent is feasible; (c) median held-out gap was 1.8% on the sampled workload; (d) production falls back after 500 ms. State what evidence each needs.

### Exercise 2

Derive the expected best objective from $k$ independent uniform $[0,1]$ minimization runs. Compute it for $k=9$ and explain the fair comparison against a deterministic method.

### Exercise 3

A study reports 30 successful runs per method but omits 7 crashes for A and 1 crash for B. Diagnose the bias and propose fixed-budget and fixed-target records that retain every outcome.

### Exercise 4

Design a fair comparison of tabu search and simulated annealing for a scheduling workload. Specify instances, tuning, budgets, replications, pairing, primary metric, failures, and uncertainty.

### Exercise 5

A metaheuristic is tuned on historical customer weeks and will be deployed next month. Design a leakage-resistant evaluation and rollout that addresses customer grouping, temporal drift, surrogate mismatch, safety, and rollback.

## Answers to the Exercises

### Answer 1

(a) is a mechanism; verify its formula, units, edge cases, draw range, and executable transitions. It is not a quality theorem. (b) is a universal invariant/theorem about implementation behavior; prove preservation or enforce a sound independent verifier and test fault paths. (c) is an empirical claim; retain the held-out sampling frame, raw runs, gap definition, failures, aggregation, and uncertainty. (d) is policy; specify the timer boundary, cancellation, fallback semantics, and operational tests. A policy can change which empirical distribution matters but is not itself evidence that the selected threshold is beneficial.

### Answer 2

For $M=\min(X_1,\ldots,X_k)$, $\Pr[M>x]=(1-x)^k$ on $0\le x\le1$. Therefore

$$
\mathbb E[M]=\int_0^1\Pr[M>x]dx=\int_0^1(1-x)^kdx=\frac1{k+1}.
$$

For $k=9$, the expected best is $1/10$. Compare this nine-run portfolio—including parallel resources and selection—with a deterministic method given an equivalent total budget or with its explicitly costed portfolio. Also report the distribution, not only expected best.

### Answer 3

Conditioning on success removes the worst reliability outcomes and favors A more because A has more omitted crashes. The denominator must be 37 runs for A and 31 for B if those were all attempted. For fixed budget, record final verified objective, feasibility, consumed resources, and a predetermined failure category or penalty for every run. For fixed target, record hitting time when reached and censoring at the full budget otherwise; crashes are failures at their observed resource point, not missing rows. Report success/crash rates with uncertainty alongside conditional quality or time.

### Answer 4

Sample or hold out scheduling instances at the source-group level and describe size, tightness, and provenance. Give both methods the same separate tuning budget and freeze selected configurations before test. Compare equal objective-evaluation and wall-time budgets, reporting cores and aggregate compute. Run a predeclared number of independent seeds for every method-instance block; pair by instance and use shared randomness only where it represents a defensible common disturbance. Choose one primary estimand such as mean verified gap at 60 seconds, then report paired effects and a confidence interval plus success, tail, and anytime summaries. Independently check feasibility/objectives; retain timeout, crash, and infeasible outcomes. Adjust or label secondary multiplicity and publish the complete ledger and versions.

### Answer 5

Group historical rows by customer and week so related schedules cannot cross tuning and evaluation. Tune only on earlier groups, validate design on a later window, and reserve the latest predeployment customers/weeks for one final estimate; next-month drift remains a limitation. Evaluate both optimizer objective and real decision outcomes such as lateness, churn, and constraint violations. Shadow the frozen method on immutable live snapshots, prevent its decisions from changing its evaluation data, and use independent safety/feasibility gates. Roll out to a small randomized or otherwise defensible cohort with guardrails, monitor instance and outcome drift, and predetermine rollback thresholds. Retain the incumbent path. If shadow or rollout results drive retuning, treat them as development data and require a new confirmation window.
