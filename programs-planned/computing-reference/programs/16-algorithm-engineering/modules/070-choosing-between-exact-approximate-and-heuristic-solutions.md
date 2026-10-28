---
module_id: ALGE-070
program: Algorithm Engineering
level: 2
module_number: 70
title: Choosing Between Exact, Approximate, and Heuristic Solutions
status: complete
last_verified: 2026-09-05
---

# Choosing Between Exact, Approximate, and Heuristic Solutions

## One-Page Review

### Governing question

Given an optimization decision, which solution route—exact, approximation, heuristic, or a governed portfolio—meets the actual obligation with the least total decision risk?

### Essential definitions

- An **exact algorithm** returns an optimal feasible solution when it terminates successfully; a complete exact solver may also prove infeasibility or unboundedness.
- An **anytime exact method** maintains a feasible incumbent and a valid bound, so interruption can leave a certified gap even before optimality is proved.
- An **approximation algorithm** has a theorem bounding solution quality for every instance in a stated class under explicit assumptions.
- An **approximation scheme** accepts an accuracy parameter $\epsilon$ and proves a corresponding bound; its time dependence on input size and $1/\epsilon$ matters.
- A **heuristic** seeks useful solutions without a uniform worst-case quality guarantee. Its support is empirical and conditional on the evaluated workload.
- A **certificate** is independently checkable evidence for feasibility, an objective, a bound, infeasibility, or optimality.
- A **decision loss** measures the consequence of deploying a returned solution, not merely its optimization objective.
- A **service contract** specifies deadline, resources, feasibility, quality, confidence, fallback, and audit obligations.
- A **portfolio** schedules several methods and shares incumbents, bounds, or certificates under one total resource budget.
- A **selection policy** maps observable instance and operating features to a method, configuration, and fallback before unavailable outcome information is known.

### Central model, mechanism, or theorem

For minimization, let a feasible incumbent have value $U$ and a valid lower bound be $L\le OPT\le U$, with $U>0$. Then

$$
\frac{U}{OPT}\le\frac{U}{L}
$$

when $L>0$. Thus $U/L\le1+\epsilon$ certifies a $(1+\epsilon)$ approximation for that instance, regardless of whether the incumbent came from an exact solver, approximation algorithm, or heuristic. When signs or zeros make ratios unsafe, use an explicitly justified additive gap or another scale.

The engineering choice is constrained optimization over methods. For instance features $x$, method $a$, budget $b$, and requirement set $R$, choose only among routes satisfying hard obligations, then minimize expected total loss:

$$
a^*(x)\in\arg\min_{a\in A_R(x)}
\mathbb E[C_{\text{compute}}+C_{\text{delay}}+C_{\text{decision}}+C_{\text{failure}}\mid x,a,b].
$$

This is a policy model, not a theorem that historical estimates remain valid after drift.

### Critical invariants

- The mathematical model, objective direction, units, and feasibility checker are identical across routes.
- Every deployed solution is independently validated before actuation.
- A claimed bound is valid for the actual instance and implementation assumptions.
- Exact means proved optimal, not “returned by an exact solver.”
- Approximate means theorem-backed for the stated class, not merely near a best-known value.
- Heuristic evidence names its workload, budget, uncertainty, failures, and limits.
- Preprocessing, warm starts, tuning, parallelism, retries, and verification count toward declared resources.
- Fallback is feasible, tested, and reachable when the primary route times out or fails.
- Selection uses only features available at decision time and is evaluated out of sample.
- Logs preserve incumbent, bound, certificate, version, input identity, elapsed resources, and termination reason.

### Common failures

Typical errors are deciding from complexity class alone; demanding optimality when a certified gap suffices; calling a solver incumbent exact before proof; applying an approximation ratio outside its assumptions; treating a best-known value as an optimum; comparing unlike models or budgets; ignoring verification and integration cost; selecting by mean runtime while tail deadlines matter; leaking solved outcomes into algorithm selection; hiding timeouts; accepting numerically infeasible output; omitting a fallback; and letting a portfolio consume more total compute than its baseline.

### Compact example

A minimization solver returns feasible value $U=106$ and a sound lower bound $L=100$. Because $100\le OPT\le106$, the instance-specific ratio is at most $106/100=1.06$. If policy requires a certified ratio no worse than 1.10, deployment may stop now; waiting for an optimality proof spends latency without changing compliance.

### Connections

[ALGE-061](./061-approximation-ratios-and-guarantees.md) defines approximation guarantees, [ALGE-065](./065-local-search.md) supplies heuristic incumbents, and [ALGE-069](./069-metaheuristics-and-their-evidence-requirements.md) governs empirical claims. [ALGE-071](../ROADMAP.md#block-08--online-streaming-and-dynamic-algorithms) begins decisions made before all input is known.

## Governing Question

How should an engineer turn computational complexity, instance structure, mathematical guarantees, empirical distributions, operational deadlines, and consequence severity into a defensible choice among exact, approximate, heuristic, and hybrid solution methods?

The answer is not a ranking in which exact is always best, approximation is second, and heuristic is last. Those labels describe different evidence obligations. A five-second exact proof can dominate every alternative. A linear-time approximation may be the only method with a useful worst-case promise. A heuristic may produce the best feasible schedule before a hard dispatch deadline. A portfolio may obtain a heuristic incumbent immediately while an exact engine tightens a bound. The appropriate route is the one whose guarantees and evidence satisfy the decision contract at acceptable total risk.

## Why This Matters

Optimization output often controls money, capacity, safety, fairness, or customer commitments. A one-percent objective improvement can be irrelevant if it arrives after the decision deadline, violates a hidden constraint, or consumes excessive compute. Conversely, routinely accepting an unexplained heuristic gap can accumulate large losses or conceal systematic harm.

Worst-case complexity is indispensable but incomplete. NP-hardness does not imply every operational instance is difficult, nor does polynomial time imply an implementation fits memory or latency. Approximation theorems can be powerful but may assume nonnegative weights, metric distances, monotonicity, or exact arithmetic absent from the production model. Empirical superiority can be real but remains conditional on instance sampling, tuning, hardware, and future stability.

Method selection therefore belongs inside system design. It requires an explicit decision deadline, loss model, verification gate, observability, escalation path, and evidence refresh policy. The result should be explainable to a reviewer without appealing to solver branding or the word “advanced.”

## Prerequisites and Retrieval

Retrieve [ALGE-061](./061-approximation-ratios-and-guarantees.md), [ALGE-062](./062-greedy-approximation.md), [ALGE-063](./063-linear-programming-rounding.md), [ALGE-064](./064-primal-dual-approximation.md), [ALGE-065](./065-local-search.md), and [ALGE-069](./069-metaheuristics-and-their-evidence-requirements.md). You should be comfortable with asymptotic complexity, NP-hardness, optimization bounds, probability, confidence intervals, timeouts, and independent feasibility checking.

This chapter owns the selection decision and its operational governance. It does not re-prove each approximation theorem, survey solver internals, or replace domain validation. Automated configuration and statistical implementation comparison return in ALGE-095 and ALGE-096.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish method-family guarantees from observed implementation behavior;
2. translate stakeholder needs into a testable optimization service contract;
3. derive and interpret incumbent-bound certificates safely;
4. screen approximation guarantees against their hypotheses;
5. decide when proof, bounded quality, or empirical quality is necessary;
6. construct sequential and parallel portfolios with honest resource accounting;
7. design out-of-sample algorithm-selection policies without leakage;
8. account for verification, integration, tail latency, and failure costs;
9. define escalation, fallback, monitoring, and evidence-refresh rules; and
10. communicate a bounded recommendation and the evidence that could reverse it.

## Core Exposition

### Begin with the decision contract

Write the contract before choosing an algorithm. Specify the immutable input, model version, objective direction and units, hard and soft constraints, decision deadline, resource ceiling, required quality evidence, failure behavior, reproducibility, audit retention, and consequence of a wrong or late answer.

Separate hard obligations from preferences. “Must never exceed vehicle capacity” is a feasibility invariant. “Prefer routes within 3% of optimal” is meaningful only if a trustworthy bound or optimum is available. “Respond within 500 ms at the 99.9th percentile” is a service requirement, not an average-runtime request. “Minimize expected total operating cost” needs a definition that includes downstream effects.

The contract defines acceptable terminal states: proved optimal; feasible with a certified gap; feasible with empirically characterized quality; safe fallback; declared no-decision; or fault. It also defines who may relax which condition. Without this separation, a timeout can silently turn a proof obligation into an unreviewed heuristic decision.

### Classify guarantees precisely

An exact algorithm's semantic promise is conditional: under its model and arithmetic assumptions, successful completion returns an optimum or another proved terminal result. An exact solver interrupted with only an incumbent has produced a heuristic solution unless its bound already certifies the required quality. The engine family does not transfer optimality to every intermediate output.

An approximation algorithm proves a relation such as $f(S)\le\rho OPT$ for minimization, on every valid instance in a declared class. Check all hypotheses. A metric traveling-salesperson guarantee cannot be applied when distances violate the triangle inequality. A nonnegative submodular maximization result cannot simply absorb negative values. A floating-point implementation must preserve the comparisons and feasibility assumptions used by the proof.

A heuristic provides no such uniform theorem. It can still be the rational choice if a deadline is hard, consequences are bounded, outputs are verified, and held-out evidence shows useful performance. Its claim must remain empirical: on this population, under this budget and implementation, outcomes followed this measured distribution.

Randomization is orthogonal. Exact, approximation, and heuristic methods may each be randomized. Ask whether randomness affects correctness, quality, runtime, or only search order, then state the probability and independence assumptions.

### Use instance-specific certificates

Global classification can be less informative than evidence available on the current instance. For minimization, a valid lower bound $L$ and feasible upper bound $U$ bracket $OPT$. The absolute gap $U-L$ is always interpretable in objective units. If $L>0$, $U/L$ is a multiplicative certificate. A relative gap convention such as $(U-L)/\max(1,|U|)$ is useful operationally but must not be mislabeled as a standard approximation ratio.

Bounds may come from relaxations, dual solutions, branch-and-bound, problem-specific inequalities, or independently checked certificates. Verify direction and validity. A stale lower bound from a different model version does not certify the new incumbent. A best-known feasible value is an upper bound for minimization, not a lower bound and not proof of optimality.

For maximization, a feasible incumbent is a lower bound and a valid relaxation may be an upper bound. Re-derive signs instead of copying minimization formulas. If objectives can be zero or negative, multiplicative ratios can reverse or explode; choose an additive or domain-scaled criterion with stakeholder justification.

### Estimate tractability from structure, not labels alone

Complexity results describe families and scaling. Selection needs instance features: size, density, graph width, constraint tightness, coefficient range, symmetry, decomposition, dynamic change, warm-start similarity, and available memory. Fixed-parameter or pseudo-polynomial algorithms may be excellent when their controlling parameter is small. Preprocessing may reduce industrial instances dramatically, while adversarial families remain hard.

Run bounded probes on development data: relaxation strength, primal and dual progress, search-tree growth, memory slope, incumbent discovery time, and tail behavior. Use censored observations rather than deleting timeouts. Extrapolation is a risk model, not a proof. Establish a cutoff and fallback before production.

Polynomial time is not a latency guarantee. An $O(n^3)$ method can be unusable at scale; an exponential method can be ideal for $n=30$. Constants, cache behavior, parallel efficiency, data movement, numerical stability, and verification cost matter.

### Price the value of optimality

Optimality has value only through the decision. Let $\Delta_d$ be the plausible decision loss from a suboptimal solution and $\Delta_c$ the extra compute, delay, and operational cost needed for stronger evidence. Seek more proof when its expected value exceeds its cost and when the deadline permits it.

High-consequence, irreversible, or regulated decisions often demand stronger certificates, conservative fallback, and human authority. Repeated low-consequence decisions may justify a fast heuristic, but small per-decision losses accumulate; estimate volume. If the objective is a weak surrogate for real outcomes, a perfect optimizer can be precisely wrong. Improving the model or measurement may dominate improving the solver.

Do not express every consequence as an invented monetary number. A lexicographic contract can require safety and legality first, service deadline second, certified quality third, and compute cost fourth. Expected-loss models are decision aids whose uncertainty and ethical limits must be visible.

### Build a staged portfolio

A robust pattern is construct, improve, certify, and escalate. A deterministic constructive algorithm supplies a feasible fallback. A local or metaheuristic improves the incumbent. An approximation algorithm supplies a theorem-backed option when applicable. An exact engine consumes the incumbent as a warm start and attempts to tighten the bound or prove optimality. At any cutoff, the system publishes only independently verified state.

Sequential portfolios spend budget conditionally: stop as soon as the contract is met. Parallel portfolios reduce latency but consume aggregate cores and energy. Record total work, not only wall time. Shared incumbents and bounds need versioned, atomic updates; a bound for one model cannot be paired with an incumbent for another.

Portfolio diversity should be causal, not cosmetic. Two methods with correlated failure modes add little resilience. Combine routes that exploit different structure, and measure complementarity on held-out instances. Count portfolio design and configuration effort in the evidence.

### Make the acceptance gate executable

The gate should operate on verified facts and explicit policy. The following small function illustrates minimization with positive bounds; it does not choose or run an optimizer.

<!-- bijux-verify: {"id":"certified-minimization-gate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"optimal:accept:optimal\nwithin_ratio:accept:certified_ratio=1.060000\nweak_bound:escalate:certified_ratio=1.250000\nno_bound:fallback:no_valid_bound\ninfeasible:reject:infeasible_incumbent\ninvalid:reject:inconsistent_bound\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    feasible: bool
    incumbent: float | None
    lower_bound: float | None
    proved_optimal: bool = False


def gate(e: Evidence, required_ratio: float = 1.10):
    if not e.feasible or e.incumbent is None:
        return "reject", "infeasible_incumbent"
    if e.proved_optimal:
        return "accept", "optimal"
    if e.lower_bound is None or e.lower_bound <= 0:
        return "fallback", "no_valid_bound"
    if e.lower_bound > e.incumbent:
        return "reject", "inconsistent_bound"
    ratio = e.incumbent / e.lower_bound
    action = "accept" if ratio <= required_ratio else "escalate"
    return action, f"certified_ratio={ratio:.6f}"


cases = {
    "optimal": Evidence(True, 83, 83, True),
    "within_ratio": Evidence(True, 106, 100),
    "weak_bound": Evidence(True, 125, 100),
    "no_bound": Evidence(True, 91, None),
    "infeasible": Evidence(False, None, 80),
    "invalid": Evidence(True, 90, 100),
}
for name, evidence in cases.items():
    action, reason = gate(evidence)
    print(f"{name}:{action}:{reason}")
```

The checker rejects inconsistent evidence, distinguishes lack of a usable certificate from infeasibility, and escalates a weak certificate. Production code also needs model identity, exact arithmetic or tolerances, certificate provenance, deadline state, policy version, and transaction semantics. Passing this example proves only its observed cases in the recorded environment.

### Learn selection policies without outcome leakage

Algorithm selection maps pre-solve features to a route. Features may include instance dimensions, sparsity, relaxation statistics from a fixed probe, historical family, and current resource state. The target can be contract satisfaction probability, expected decision loss, or a risk-sensitive metric—not merely fastest successful run.

Train and evaluate at the source-group level. Instances derived from the same customer, graph, generator, or time window must not leak across splits. Include feature-computation time in the budget. If a feature requires solving the instance, it is unavailable at selection time. Preserve failures and censored runtimes. Compare the learned selector with a single best method and simple rules on an untouched test population.

Selection uncertainty needs a safe default. Out-of-distribution features, missing telemetry, or low confidence should route to a conservative portfolio or fallback. Monitor both feature drift and contract outcomes. Retuning converts monitoring observations into development data and requires fresh confirmation.

### Compare implementations under one protocol

First verify semantic equivalence: same input, objective, constraints, precision, preprocessing boundary, stopping condition, and feasible-output checker. Then compare equal declared budgets and realistic configurations. Include licensing, startup, data conversion, memory, accelerators, cores, remote latency, and operator burden where they matter.

Use fixed-budget quality and fixed-target resource distributions. Report tail latency, timeouts, infeasibility, crashes, and certificate rates. Averages alone can select a method that frequently misses a hard deadline. Paired instance-level comparisons reduce nuisance variation; uncertainty and practical effect sizes prevent small benchmark differences from becoming sweeping claims.

Benchmark the whole service path. An optimizer that solves in 20 ms but requires 800 ms of serialization loses a 500 ms contract. A slower route may win through warm starts, incremental updates, or simpler verification. Measure deployment behavior in shadow mode before actuation.

### Govern runtime decisions and evidence decay

Bind each run to input digest, model version, algorithm and configuration, random stream if any, hardware, resource limit, incumbent, bound, certificate, termination reason, and checker result. Make cancellation preserve the last atomic verified state. Never publish a candidate while its objective or certificate belongs to a previous state.

Escalation policy can be deterministic: heuristic until 100 ms; exact bound tightening until the ratio is at most 1.05 or 450 ms; then verified fallback at 500 ms. Test every boundary using controlled clocks and injected failures. Recovery must not restart unbounded work after the external deadline.

Evidence decays when workload, model, implementation, compiler, hardware, or business loss changes. Revalidate on a cadence driven by risk and drift. A method choice is a versioned decision with a review date, not permanent truth.

## Definitions and Notation

Let $I$ be an instance, $F(I)$ its feasible set, $f_I$ its objective, and $OPT(I)$ the optimum. For minimization, $U$ denotes a verified feasible value and $L$ a valid lower bound. The absolute gap is $U-L$; the certified ratio $U/L$ is used only for $L>0$. For maximization, bound directions reverse.

Let $A$ be the set of candidate methods, $x(I)$ the features observable before selection, $b$ the total resource budget, and $R$ the hard service requirements. $A_R(I)$ contains routes whose guarantees or governed evidence can satisfy $R$ for $I$. A selection policy $\pi(x)$ chooses a route or portfolio. Its loss includes compute, delay, deployed decision quality, and failure consequence under an explicitly stated aggregation or risk measure.

“Exact,” “approximation,” and “heuristic” classify guarantees, not software brands. “Certified” refers to evidence independently checked for the current input and model. “Best known” records current knowledge and is not synonymous with optimal. “Empirically competitive” is bounded to a sampled population and protocol.

## Mechanisms, Invariants, or Proof Structure

### Certificate derivation

For minimization, feasibility gives $OPT\le U$ and a sound relaxation or dual argument gives $L\le OPT$. If $L>0$, dividing $U\le (U/L)OPT$ follows because $OPT\ge L$:

$$
\frac{U}{OPT}\le\frac{U}{L}.
$$

Therefore $U/L\le1+\epsilon$ proves the incumbent meets that ratio on the current instance. This is a proof, conditional on feasibility, bound validity, shared model identity, correct direction, and positive scale. It says nothing about unseen instances or the time needed to obtain the pair.

### Selection invariant

At decision time $t$, the selector may use only $\mathcal F_t$, the information available by then. Using final optimum, eventual solve time, or future demand in $x(I)$ leaks outcome information. Formally, $\pi_t$ must be measurable with respect to $\mathcal F_t$. An offline oracle is useful as an upper benchmark for selection potential, but it is not deployable.

### Publication invariant

Every publishable record is a tuple

$$
(h_I,h_M,h_A,S,f_I(S),L,t,r,c),
$$

where hashes bind input, model, and algorithm configuration; $S$ is feasible; objective and bound use the same model; $t$ and $r$ record time and resources; and checker result $c$ validates the claimed state. Updates are atomic. A partial tuple is telemetry, not a deployable decision.

### Portfolio accounting

For parallel components $j$, wall latency is approximately $\max_j t_j$ while aggregate CPU work is $\sum_j p_jt_j$ for $p_j$ cores. Reporting only the former can make a portfolio appear free. Sequential work accumulates until a stop condition. Both comparisons must include feature extraction, verification, coordination, and fallback.

### Evidence hierarchy

A proof establishes a stated property under hypotheses. A certificate establishes a property for one instance. Tests establish observed behavior for tested cases. A benchmark estimates performance on its sampling frame. Shadow operation estimates behavior under a non-actuating production path. None automatically entails the next. Selection should use the strongest relevant evidence available and label its boundary.

## Alternatives and Trade-Offs

| Route | Strongest typical evidence | Primary strength | Primary risk | Good fit |
|---|---|---|---|---|
| Exact | Optimality, infeasibility, or bound certificate | Decisive proof and strong diagnostics | Unpredictable time or memory | Moderate instances, strong structure, high value of proof |
| Approximation | Uniform quality theorem under hypotheses | Predictable quality and often scalable runtime | Model may violate assumptions; bound may be loose | Large instances with a relevant theorem-backed structure |
| Heuristic | Held-out empirical outcome distribution | Flexible modeling and strong early incumbents | No uniform quality protection; drift | Hard deadlines with bounded, monitored consequences |
| Anytime exact | Feasible incumbent plus improving bound | Graceful continuum from heuristic to proof | Tail behavior and weak early bounds | Variable budgets where certificates add value |
| Sequential portfolio | Contract-driven stopping | Spends extra work only when needed | Integration and state-consistency complexity | Tiered quality/deadline contracts |
| Parallel portfolio | First acceptable verified result | Lower latency and failure diversity | Higher aggregate compute and contention | High-value decisions with spare resources |

A simple deterministic rule is easier to audit than a learned selector. A learned policy can exploit heterogeneous instances but adds training data, leakage, drift, and explanation risks. Human escalation can handle rare high-consequence cases but introduces queueing and consistency concerns. The choice should be proportional to both opportunity and failure severity.

## Failure Modes and Misconceptions

- **“NP-hard means exact is impossible.”** Hardness is asymptotic and worst-case; operational structure and size can make exact solution routine.
- **“Exact solver means exact answer.”** Only a valid proof of optimality supports that label; an interrupted incumbent is not exact.
- **“Polynomial means fast.”** Degree, constants, memory, and implementation can violate the service budget.
- **“Approximation means observed closeness.”** It means a proved bound for a stated instance class; experiments answer a different question.
- **“Best known is optimal.”** It is merely the best recorded feasible value unless accompanied by a matching bound or proof.
- **“A 5% solver gap means 5% business loss.”** Objective normalization and downstream decision loss may differ greatly.
- **“One ratio formula fits all objectives.”** Zero, negative, maximization, and multiobjective cases require re-derived semantics.
- **“The fastest mean wins.”** Tail deadlines, failure probability, solution quality, and verification may dominate the mean.
- **“Portfolio wall time is its total cost.”** Parallel work consumes aggregate compute, memory, energy, and coordination.
- **“The selector can use any benchmark feature.”** Features unavailable before the choice create leakage and impossible deployment.
- **“Fallback can be added later.”** Failure semantics shape feasibility, deadlines, tests, and operational authority from the start.
- **“A permanent winner exists.”** Workloads, models, implementations, and hardware change; evidence requires versioning and refresh.

## Worked Examples

### Example 1

**Situation.** A minimization route returns $U=106$ with sound $L=100$; the contract accepts a certified ratio at most 1.10.

**Reasoning.** Feasibility gives $OPT\le106$ and the bound gives $100\le OPT$. Because $L>0$, $U/OPT\le U/L=1.06\le1.10$. The solver has not proved optimality, but it has proved the required instance-specific quality.

**Conclusion.** Accepting now satisfies the contract; calling the solution optimal would still be false.

### Example 2

**Situation.** A metric-TSP approximation is proposed for travel times that can violate triangle inequality because of one-way restrictions and time windows.

**Reasoning.** The guarantee's hypothesis is not a cosmetic detail. If $d(a,c)>d(a,b)+d(b,c)$, the shortcut argument behind metric-tour bounds can fail. One may construct a metric closure only if its paths map back to feasible original decisions and preserve all constraints.

**Conclusion.** The named approximation ratio is unavailable until the transformed model and theorem hypotheses are proved applicable.

### Example 3

**Situation.** An exact branch-and-bound engine times out with incumbent 820 and lower bound 800.

**Reasoning.** It did not return an exact solution. It did return a feasible candidate with instance certificate $820/800=1.025$, assuming minimization and a sound positive bound. If the service requires 3%, the result passes; if it requires optimality, it does not.

**Conclusion.** Classify the returned evidence, not the engine's marketing category.

### Example 4

**Situation.** Method E has median runtime 40 ms but a 99.9th percentile of 900 ms; method A always finishes near 120 ms. The deadline is 200 ms.

**Reasoning.** Median optimization selects E while deadline compliance may favor A. The relevant metric is probability of an acceptable verified solution by 200 ms, including timeout fallback and quality. A staged policy can run E with a cutoff and retain A's result only if resource contention is controlled.

**Conclusion.** Tail-aware contract satisfaction, not mean or median runtime alone, governs selection.

### Example 5

**Situation.** A learned selector uses the number of branch-and-bound nodes eventually explored as a feature.

**Reasoning.** That value is known only after running the exact solve, so it is not measurable at selection time. It leaks the outcome and understates selector cost. A fixed 20 ms probe may provide early bound slope, but its time and censoring must enter the budget.

**Conclusion.** Replace post-outcome features with bounded pre-decision observations and reevaluate out of sample.

### Example 6

**Situation.** A parallel portfolio reports 2 seconds wall time using eight cores, while a baseline reports 3 seconds on one core.

**Reasoning.** The portfolio used roughly 16 core-seconds before overhead, versus 3 core-seconds. It may still be preferable under a latency objective, but not under equal compute cost. Report latency, aggregate work, memory, and interference, and compare under the contract's resource dimension.

**Conclusion.** Parallel speed is valuable but does not erase consumed resources.

### Example 7

**Situation.** A minimization objective can be negative: incumbent $U=-90$ and lower bound $L=-100$.

**Reasoning.** $U/L=0.9$ looks “better than one,” yet the incumbent is not better than the lower bound; $-100\le OPT\le-90$. Multiplicative minimization ratios are not safely interpretable under this sign convention. The absolute certified gap is 10 objective units; a domain-defined scale may convert it meaningfully.

**Conclusion.** Check sign and scale before using ratio gates.

### Example 8

**Situation.** A dispatch system runs a heuristic for 100 ms, exact bound tightening for another 350 ms, and must respond by 500 ms.

**Reasoning.** Reserve time for parsing, independent verification, and publication—say 50 ms—rather than assigning the whole deadline to search. If the heuristic candidate is infeasible, use a preverified constructive fallback. Stop exact work early when the certificate meets policy; cancellation publishes the last atomic verified tuple.

**Conclusion.** A portfolio is an end-to-end deadline protocol, not a list of solvers.

### Example 9

**Situation.** A heuristic saves 0.2% objective cost per decision and runs one million times per month; stronger certification costs 20 ms more.

**Reasoning.** Neither percentage nor latency alone determines value. Convert the objective difference to bounded operational consequence, include the monthly volume, tail capacity, and risk of rare failures, and compare with the compute and delay cost. If the objective is only a surrogate, validate downstream outcomes before multiplying.

**Conclusion.** Price optimality and approximation at decision scale, while preserving uncertainty and nonmonetary constraints.

### Example 10

**Situation.** A route selected on last year's sparse graphs now receives dense graphs and its timeout rate doubles.

**Reasoning.** The original evidence was conditional on a feature distribution. Detect drift, route out-of-distribution instances to the conservative portfolio, retain the old safe path, and collect governed outcomes. Retuning on those outcomes makes them development data, so final claims need a fresh holdout.

**Conclusion.** Method selection is versioned and monitored; historical victory is not permanent authority.

## Cross-Program Connections

- **Theory of Computation and Complexity:** hardness, reductions, parameterization, and lower bounds delimit what algorithm families can promise.
- **Software Architecture:** the optimizer, independent checker, portfolio coordinator, and policy gate require explicit trust and failure boundaries.
- **Software Testing and Quality Engineering:** property tests, fault injection, controlled clocks, held-out comparisons, and uncertainty validate the service contract.
- **Software Delivery and Reliability Engineering:** deadlines, tail latency, load shedding, circuit breaking, rollback, and observability shape operational choice.
- **Data Engineering:** immutable instances, group-aware splits, provenance, and drift telemetry protect selection evidence.
- **Security Engineering:** adversarial instances, certificate tampering, resource exhaustion, and unsafe fallback expand the threat model.
- **Systems Engineering:** cores, memory, energy, data movement, accelerators, and cancellation determine total resource cost.
- **Algorithm Engineering:** ALGE-061 through ALGE-069 supply the guarantee and evidence classes; [ALGE-071](../ROADMAP.md#block-08--online-streaming-and-dynamic-algorithms) changes the setting by revealing inputs over time.

## References

1. Richard M. Karp, “Reducibility Among Combinatorial Problems,” in *Complexity of Computer Computations*, Plenum Press, 1972, 85–103. DOI: [10.1007/978-1-4684-2001-2_9](https://doi.org/10.1007/978-1-4684-2001-2_9). Primary source for classical polynomial reductions and NP-completeness foundations; publisher record checked 2026-09-05.
2. Michael R. Garey and David S. Johnson, *Computers and Intractability: A Guide to the Theory of NP-Completeness*, W. H. Freeman, 1979. Durable reference for hardness interpretation and problem transformations; bibliographic record checked 2026-09-05.
3. David P. Williamson and David B. Shmoys, *The Design of Approximation Algorithms*, Cambridge University Press, 2011. DOI: [10.1017/CBO9780511921735](https://doi.org/10.1017/CBO9780511921735). Textbook reference for approximation guarantees, hypotheses, and design techniques; publisher record checked 2026-09-05.
4. John R. Rice, “The Algorithm Selection Problem,” *Advances in Computers* 15, 1976, 65–118. DOI: [10.1016/S0065-2458(08)60520-3](https://doi.org/10.1016/S0065-2458(08)60520-3). Primary framework for mapping problem features to algorithms; record checked 2026-09-05.
5. Kevin Leyton-Brown, Eugene Nudelman, Galen Andrew, Jim McFadden, and Yoav Shoham, “A Portfolio Approach to Algorithm Selection,” *IJCAI 2003*, 1542–1543. [Proceedings record](https://www.ijcai.org/Proceedings/03/Papers/268.pdf). Primary portfolio-selection reference; proceedings checked 2026-09-05.
6. Carla P. Gomes and Bart Selman, “Algorithm Portfolios,” *Artificial Intelligence* 126(1–2), 2001, 43–62. DOI: [10.1016/S0004-3702(00)00081-3](https://doi.org/10.1016/S0004-3702(00)00081-3). Primary source for portfolio methods and complementary runtime behavior; publisher record checked 2026-09-05.
7. Catherine C. McGeoch, *A Guide to Experimental Algorithmics*, Cambridge University Press, 2012. DOI: [10.1017/CBO9780511843747](https://doi.org/10.1017/CBO9780511843747). Monograph on defensible algorithm experiments, measurement, and conclusions; publisher record checked 2026-09-05.
8. John N. Hooker, “Testing Heuristics: We Have It All Wrong,” *Journal of Heuristics* 1, 1995, 33–42. DOI: [10.1007/BF02430364](https://doi.org/10.1007/BF02430364). Primary methodological critique of heuristic evaluation; record checked 2026-09-05.

## Exercises

### Exercise 1

Classify the strongest evidence in each case: (a) a feasible value with a matching lower bound; (b) a theorem proving $f(S)\le2OPT$ on metric instances; (c) median held-out gap at a fixed budget; (d) a solver executable labeled “exact” that times out with only an incumbent.

### Exercise 2

For minimization, derive the certificate from $L\le OPT\le U$ when $L>0$. Evaluate $U=414$, $L=400$ against a 1.05 ratio requirement, then explain why the same division is unsafe for $U=-90$, $L=-100$.

### Exercise 3

A production job has a 300 ms deadline. Parsing takes 20 ms, verification at most 25 ms, and publication 5 ms. An engineer gives an exact engine a 300 ms timeout and has no fallback. Diagnose the design and specify a safe timing policy.

### Exercise 4

Design a comparison among exact, approximation, and heuristic routes for a large scheduling workload. Include model equivalence, instance sampling, budgets, metrics, certificates, failures, tail behavior, and a selection rule.

### Exercise 5

A hospital proposes a learned selector for a high-consequence allocation model. Design a governance plan covering feature availability, distribution shift, feasibility and fairness, evidence strength, human authority, fallback, audit records, and conditions for retraining.

## Answers to the Exercises

### Answer 1

(a) is an instance-specific optimality certificate if feasibility and bound validity are independently checked and the values match. (b) is a uniform approximation theorem conditional on metric hypotheses and faithful implementation. (c) is empirical evidence limited to the held-out population, implementation, budget, and uncertainty. (d) is only a heuristic incumbent unless its accompanying valid bound certifies some stated quality; the engine category does not prove the interrupted output optimal.

### Answer 2

Since $OPT\ge L>0$, $U/OPT\le U/L$. For $U=414$ and $L=400$, $U/L=1.035$, which meets 1.05. It does not prove optimality; it proves at most a 3.5% multiplicative gap under the assumptions. For negative values, $(-90)/(-100)=0.9$ misleadingly appears below one even though $-90$ is the worse feasible minimization value. Use the certified interval $[-100,-90]$, its 10-unit absolute gap, or a justified domain scale.

### Answer 3

The search timeout consumes time required by the rest of the service, so even a timely solver return can miss the external deadline. With worst-case nonsearch work of 50 ms, the search budget is at most 250 ms and should include a safety margin for scheduling and cancellation. Establish a feasible constructive fallback before or within that budget, preserve a verified incumbent atomically, stop earlier when the quality contract is met, and test timeout, cancellation, checker failure, and publication at boundary times. The external deadline—not the solver timer—has authority.

### Answer 4

Freeze one mathematical model and use the same parser, objective recomputation, feasibility checker, precision, and input digests. Sample held-out instances by source group and cover relevant sizes and tightness. Give routes matched development and tuning opportunity. Compare fixed-budget verified quality, fixed-target time, certificate rate, 99th-percentile latency, memory, aggregate compute, infeasibility, timeout, and crash outcomes. Retain censored and failed runs. A defensible rule might accept exact proofs immediately, accept any verified incumbent whose bound meets the required ratio, use the approximation route when its hypotheses hold and deadline risk is high, and otherwise deploy a validated heuristic with safe fallback. Estimate the whole rule out of sample, not just each component in isolation.

### Answer 5

Use only features available before selection and include their acquisition time; split evaluation by hospital, cohort, and later time so related cases do not leak. Independently validate every hard constraint and define fairness requirements as governed constraints or review criteria rather than an unchecked surrogate. Require stronger certificates or mandatory human review for high-consequence cases, while bounding queue delay. Provide a conservative feasible fallback and a no-actuation state when data or checks fail. Log input/model/configuration digests, selected route, incumbent, bound, checker results, protected-group assessments under authorized privacy controls, timing, override, and outcome. Monitor feature, constraint, fairness, and outcome drift. Predetermine stop and rollback thresholds. Retraining occurs only under approved change control; used monitoring data become development data, and release requires fresh temporal and site-level confirmation.
