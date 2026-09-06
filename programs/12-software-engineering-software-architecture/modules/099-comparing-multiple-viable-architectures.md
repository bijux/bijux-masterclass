---
module_id: SARCH-099
program: Software Engineering: Software Architecture
level: 2
module_number: 99
title: Comparing Multiple Viable Architectures
status: complete
last_verified: 2026-09-06
---

# Comparing Multiple Viable Architectures

## One-Page Review

### Governing question

When several architectures can plausibly satisfy the mission, how do decision-makers compare them without hiding infeasibility, double-counting preferences, pretending uncertain estimates are facts, or converting legitimate stakeholder conflict into a spurious score?

### Essential definitions

- a **candidate** is a coherent architecture with scope, decisions, interfaces, deployment, data, operation, evolution, and assumptions—not a product name;
- a **feasibility gate** is a noncompensatory condition: failure cannot be offset by strengths elsewhere;
- a **scenario** states source, stimulus, environment, affected artifact, response, and measure;
- a **criterion** is one decision-relevant property with an operational definition, direction, scale, and evidence rule;
- a **trade-off point** is a decision that affects multiple qualities in tension; a **sensitivity point** has an unusually strong effect on one or more outcomes;
- **dominance** means one candidate is no worse on every compared criterion and better on at least one;
- a **Pareto frontier** contains nondominated candidates; it does not identify one universal winner;
- **uncertainty** concerns an unknown value; **variability** is real dispersion; **ambiguity** is unclear meaning;
- **robustness** is acceptable performance across plausible conditions; **reversibility** limits the cost of being wrong;
- a **decision record** preserves context, candidates, evidence, uncertainty, dissent, authority, and review triggers.

### Central model, mechanism, or theorem

First define feasible candidates:

$$
F=\{a\in A\mid g_k(a)=\mathrm{pass}\text{ for every mandatory gate }k\}.
$$

Only then may a transparent additive model summarize compensatory criteria:

$$
S(a)=\sum_{i=1}^{m}w_i v_i(a),\qquad w_i\ge0,\quad\sum_i w_i=1.
$$

Here $v_i$ is a directionally normalized value supported by evidence, not a label such as “scalable.” A score is a decision aid only if criteria are preferentially independent enough for addition, scales are meaningful, and uncertainty/sensitivity are shown. It never overrides a failed gate or legitimate authority.

Candidate $a$ dominates $b$ when $v_i(a)\ge v_i(b)$ for every benefit criterion and $>$ for at least one. Removing dominated candidates is justified under those fixed criteria and evidence. Choosing among nondominated candidates requires stakeholder priorities, risk, uncertainty, and judgment.

### Critical invariants

- compare coherent end-to-end candidates at the same scope, workload, horizon, and quality contract;
- reject infeasible candidates before weighted scoring;
- derive criteria from stakeholder concerns and concrete scenarios;
- use one direction per criterion and avoid double-counting correlated consequences;
- record raw evidence before normalization, aggregation, or rounding;
- attach range, confidence, provenance, date, and assumption to every estimate;
- distinguish measured, simulated, analytically derived, supplier-claimed, and judged evidence;
- run sensitivity on weights, uncertain inputs, workload, failure, price, and time horizon;
- include operations, migration, security, data, organization, exit, and reversibility;
- preserve minority concerns and veto authority instead of averaging them away;
- select an owner and review trigger for every material assumption;
- a recommendation identifies residual risk and next evidence, not guaranteed correctness.

### Common failures

Common failures include comparing diagrams with different scope; keeping a noncompliant option in the score; inventing weights after seeing a favorite; scoring “security” from 1–5 without scenarios; double-counting latency, performance, and responsiveness; treating ordinal ranks as arithmetic; hiding missing evidence at the midpoint; using averages that conceal tail or cohort harm; trusting vendor benchmarks; ignoring migration and exit; evaluating happy path only; false precision; winner-take-all workshops; and freezing a decision after assumptions change.

### Compact example

Three designs pass privacy, recovery, and accessibility gates. On normalized benefit criteria availability, change cost, and lifecycle affordability, A=(0.8,0.5,0.6), B=(0.7,0.8,0.7), and C=(0.6,0.4,0.5). B dominates C, so C can be removed under this model. With weights (0.5,0.3,0.2), A scores 0.67 and B 0.73. If availability weight rises and evidence intervals overlap, the recommendation may change; therefore the record shows raw measures, ranges, sensitivity, and the decision authority rather than “B is 9% better.”

### Connections

[SARCH-004](004-quality-attributes-as-architectural-drivers.md), [SARCH-007](007-trade-offs-and-competing-objectives.md), [SARCH-061](061-architecture-tradeoff-analysis-method.md), [SARCH-062](062-quality-attribute-scenarios.md), [SARCH-063](063-risk-sensitivity-and-trade-off-points.md), and [SARCH-070](070-running-an-evidence-based-architecture-review.md) supply the evaluation mechanics. [SARCH-091](091-architecture-for-regulated-and-safety-critical-systems.md) supplies hard assurance boundaries, and [SARCH-098](098-architecture-under-severe-cost-constraints.md) supplies feasibility under cost. [SARCH-100](../ROADMAP.md) next defends a recommendation before adversarial review.

## Governing Question

Architecture rarely has one technically possible answer. A modular monolith, services, event pipeline, purchased platform, and hybrid can all meet a superficial feature list. Their consequences appear under change, failure, scale, attack, migration, and operation. Comparison is therefore an exercise in structured uncertainty and legitimate choice, not diagram aesthetics.

A rigorous method must be decisive enough to act yet honest about evidence. It eliminates candidates that cannot meet mandatory obligations, exposes trade-offs among viable candidates, identifies which assumptions control the result, and records who may accept residual risk.

## Why This Matters

Weak comparison launders preference into numbers. A team can assign weights that favor its familiar technology, score missing evidence optimistically, and present a decimal winner. The arithmetic makes the choice look objective while concealing value judgments and uncertainty.

ISO/IEC/IEEE 42010:2022 distinguishes architecture from its description and specifies how concerns, viewpoints, and models structure an architecture description [1]. ISO/IEC/IEEE 42030:2019 frames architecture evaluation [2]. ATAM uses stakeholder scenarios to expose risks, sensitivity points, and trade-off points [3]. These provide structure; none supplies a context-free winner.

## Prerequisites and Retrieval

Retrieve stakeholder, concern, quality attribute, scenario, constraint, invariant, candidate, baseline, criterion, metric, scale, normalization, weight, utility, dominance, Pareto frontier, uncertainty, sensitivity, robustness, reversibility, option, expected value, risk, evidence, confidence, residual risk, and decision authority.

From SARCH-001 through SARCH-010 retrieve architectural decisions and drivers; SARCH-021 through SARCH-030 provide comparable views; SARCH-040 provides style selection; SARCH-061 through SARCH-070 provide evaluation; SARCH-073 through SARCH-080 provide evolution; and SARCH-091 through SARCH-098 provide difficult domain constraints.

## Learning Objectives

After completing this module, you should be able to:

1. construct comparable, coherent architecture candidates;
2. separate mandatory feasibility gates from compensatory preferences;
3. derive criteria and measures from prioritized scenarios;
4. normalize direction and scale without erasing raw evidence;
5. identify dominated and nondominated candidates;
6. use weighted models without overstating their assumptions;
7. represent uncertainty, correlation, and sensitivity;
8. compare lifecycle transition, organization, and reversibility as well as steady state;
9. facilitate legitimate disagreement and preserve dissent;
10. write an auditable recommendation with triggers for reopening it.

## Core Exposition

**Frame the decision.** State the entity, decision deadline, operational horizon, authorities, affected groups, business or mission outcomes, constraints, workload, environments, current system, sunk commitments, and reasons a decision is needed. Define what remains outside scope. Without one frame, teams compare different problems.

Specify the baseline as a real candidate, including doing nothing, repair, or delay. “Current state” has migration advantage but accumulated risk. Delay can buy evidence or lose an opportunity. Sunk cost influences transition but must not be counted as future benefit.

**Build coherent candidates.** Describe each candidate through the same views: context, responsibilities, runtime interactions, data authority, deployment/failure domains, security, operations, delivery, organization, migration, and exit. Include necessary supporting components. Comparing “managed database” to “self-hosted database” while omitting backup and staffing from one side is invalid.

Name variants only when a decision materially changes consequences. Five near-identical diagrams create false diversity. Conversely, one label such as “microservices” hides boundary, data, deployment, ownership, and consistency decisions. Require enough detail to analyze scenarios, not implementation completion.

**Establish gates first.** Mandatory legal, safety, security, privacy, interoperability, accessibility, data-integrity, schedule, budget, and recovery conditions are noncompensatory. State the evidence needed to pass, conditional pass, or fail. An inaccessible design cannot offset exclusion with low latency.

Unknown gate evidence is not an average score. Mark it unresolved, commission a proof, reduce scope, or reject the option by the decision deadline. Only legitimate authorities can waive or revise a gate, and the exception needs scope, expiry, and residual risk.

**Derive scenarios from concerns.** A quality word is too vague. Turn “available” into a source, stimulus, environment, affected artifact, response, and measure: during loss of one region at peak traffic, accepted payments recover within five minutes with zero acknowledged loss. Turn modifiability into a named change and bounded effort; security into threat and protected response; usability into task and population.

Prioritize with stakeholders, including operators and affected users. Scenarios reveal that candidates optimize different futures. Include ordinary, peak, failure, attack, change, recovery, migration, retirement, and organization-loss conditions.

**Define nonoverlapping criteria.** Each criterion has definition, direction, unit or scale, data source, horizon, uncertainty, owner, and relationship to scenarios. Prefer direct measures: p99 latency under workload W, recovery minutes after fault F, engineer-days for change C, or five-year lifecycle cost.

Avoid double-counting. Availability, resilience, recovery, and durability may represent distinct phenomena or the same consequence repeated. Draw a value tree and place each consequence once. Shared causes can remain correlated even when labels differ.

**Preserve raw evidence.** Keep measurements, models, assumptions, samples, environment, date, supplier claim, and review notes. Normalize only for comparison. A 0.8 value must resolve to something meaningful. Do not let a colored cell become the only durable record.

Evidence types have different strength. Production observation is context-specific; a benchmark is workload-specific; analytical proof depends on premises; simulation depends on model; prototype explores a slice; supplier documentation states a contract or claim; expert judgment is fallible but sometimes necessary. Label each.

**Normalize direction carefully.** Benefit criteria rise with preference; cost criteria fall. Map values with explicit thresholds, not arbitrary min-max ranges that change when a poor candidate is added. Ordinal labels such as low/medium/high do not support addition unless the decision group defines a defensible value function.

Thresholds can encode diminishing value: reducing recovery from 60 to 10 minutes may matter more than 10 to 5. Document the curve. Never use normalization to conceal an infeasible raw value.

**Use dominance before weights.** If one candidate is no better on any relevant criterion and worse on at least one, it is dominated under the declared evidence. Removing it simplifies discussion. With uncertainty intervals, dominance may be unresolved. A candidate may remain for an unmodeled concern, which signals that the criteria are incomplete.

The Pareto frontier shows viable trade-offs. It does not say every frontier point is equally desirable. Stakeholders choose among them using priority, risk tolerance, transition, and authority.

**Treat weights as value judgments.** Weights express marginal preference on the chosen value scales, not intrinsic importance of labels. Elicit them before reviewing aggregate scores where practical. Test whether participants understand the trade being made: how much recovery improvement compensates for migration cost?

Additive scoring assumes criteria are sufficiently preferentially independent. When security and availability interact, or a threshold changes the value of another criterion, use scenario analysis, conditional models, or explicit portfolios. Never average away a catastrophic tail.

**Represent uncertainty.** Use intervals, distributions when justified, confidence categories, and unresolved assumptions. Separate measurement error, forecast uncertainty, workload variability, model inadequacy, and ambiguity. One wide interval should not become a precise midpoint.

Run sensitivity over weights and uncertain inputs. Find break-even points and rank reversals. If a 2% weight shift changes the winner, the decision is fragile; gather evidence, choose a reversible option, or present the tie honestly. Robust choice can be more valuable than highest expected score.

**Compare failure and recovery.** Trace each candidate through dependency loss, overload, bad deployment, credential compromise, data corruption, region loss, supplier outage, and operator error. Identify detection, containment, degraded service, recovery, reconciliation, and evidence. Common dependencies can make two “independent” paths one failure domain.

Measure recovery with tested procedures. Replication without restore, failover without data reconciliation, and multi-region without control-plane analysis are incomplete. State residual correlated failure.

**Compare security and privacy as mechanisms.** Use threat scenarios, assets, actors, trust boundaries, identities, authorization, isolation, secrets, audit, response, and data lifecycle. Counting controls is weak: two candidates may have the same controls with different attack surfaces.

Consider migration exposure, support access, backups, derived data, and exit. Security teams and legitimate data authorities own acceptance. A weighted “security score” cannot authorize unlawful processing.

**Compare change and organization.** Run representative changes through code, contracts, data, deployment, tests, coordination, release, and rollback. Count cognitive and organizational dependencies, not merely repositories. Independent deployment is useful only if ownership and data allow it.

Conway effects mean candidate feasibility depends on teams and skills. Include hiring, training, on-call, specialist concentration, vendor support, and governance. Architecture can change organization, but that transition has cost and risk.

**Compare economics over lifecycle.** Include build, run, people, incidents, migration, dual running, contracts, compliance, growth, and exit. Use scenarios rather than one average. CBAM explicitly brings benefits, costs, schedule, and uncertainty into architecture choice [4]. Monetization is a model, not a way to price dignity or mandatory duty.

Avoid double-counting benefit already represented by quality measures. Use currency and date, price source, allocation, discount rule, and ranges. Separate cash, effort, opportunity, and risk when aggregation would mislead.

**Compare transition, not only destination.** A superior steady state can be infeasible because migration exceeds outage, funding, compatibility, staffing, or risk limits. Model intermediate architectures, data authority, dual operation, rollback boundary, customer impact, and decommissioning.

Reversibility favors learning under uncertainty. A lower-scoring candidate may be chosen because it can be tested cheaply and exited safely. Record the option and review date, not a fictional permanent answer.

**Prototype the controlling uncertainty.** Do not build three systems. Identify assumptions with high sensitivity and low evidence: write throughput, policy latency, restore time, vendor portability, change effort, or operator workload. Design the smallest discriminating experiment with acceptance criteria.

A benchmark should resemble production data, skew, concurrency, failure, and environment. A prototype passing one query proves that slice only. Preserve code, inputs, versions, outputs, and limitations.

**Facilitate conflict legitimately.** Separate facts, forecasts, values, authority, and interests. Anonymous scoring can reduce hierarchy effects but cannot resolve missing stakeholders. Record dissent and the condition under which it matters. A security veto, statutory authority, or affected-community concern is not one more vote.

Use independent facilitation for high-stakes choices. Let candidate advocates challenge each other’s assumptions symmetrically. Avoid allowing the most detailed proposal to win merely because it has more documented rows.

**Make the recommendation auditable.** State chosen candidate, why it is feasible, alternatives rejected, trade-offs accepted, evidence, uncertainty, residual risks, dissent, decision authority, implementation constraints, experiments, and review triggers. Include what would reverse the decision.

Triggers include workload thresholds, price changes, incidents, regulation, team capacity, missed SLOs, vendor terms, or failed migration evidence. A decision record preserves reasoning; it does not prevent revision.

## Definitions and Notation

Let $A$ be candidate set, $F\subseteq A$ feasible candidates, $g_k(a)$ mandatory gate $k$, $v_i(a)$ normalized benefit value for criterion $i$, $w_i$ its weight, and $S(a)$ aggregate score. Let $[l_i(a),u_i(a)]$ be an uncertainty interval, $\theta$ the vector of assumptions, and $S(a;\theta,w)$ the conditional score. Let $T(a)$ be transition risk/cost and $R(a)$ reversibility or option value.

For cost criterion raw value $x$ bounded by meaningful best $b$ and worst $d>b$, one possible linear value is $v=(d-x)/(d-b)$ clipped to $[0,1]$. This mapping asserts constant marginal value within the range; it is not neutral.

## Mechanisms, Invariants, or Proof Structure

**Dominance proposition.** If all relevant compensatory criteria use the same preferred direction and $v_i(a)\ge v_i(b)$ for every $i$, with strict inequality for at least one positively weighted criterion, then $S(a)>S(b)$ for nonnegative weights summing to one. Proof: every weighted difference is nonnegative and at least one is positive. The conclusion fails if a criterion is missing, a gate differs, uncertainty reverses an inequality, or weights can be zero on every strict difference.

**Weight sensitivity.** For two candidates, score difference is $\Delta(w)=\sum_iw_i(v_i(a)-v_i(b))$. A break-even surface satisfies $\Delta=0$. Evaluating plausible weights and raw-value intervals reveals rank stability; one nominal vector does not.

**Executable comparison.** This finite checker applies gates, removes one dominated candidate, and ranks remaining candidates at two weight vectors. It illustrates mechanics only; production comparison needs valid value functions, uncertainty, stakeholders, and complete criteria.

<!-- bijux-verify: {"id":"compare-viable-architectures","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"feasible=['A', 'B', 'C']\nnondominated=['A', 'B']\nbase=B:0.730\navailability-heavy=A=B:0.720\n","stderr":""}} -->
```python
candidates = {
    "A": {"gates": True, "values": (0.8, 0.5, 0.6)},
    "B": {"gates": True, "values": (0.7, 0.8, 0.7)},
    "C": {"gates": True, "values": (0.6, 0.4, 0.5)},
    "D": {"gates": False, "values": (1.0, 1.0, 1.0)},
}
feasible = {k: v["values"] for k, v in candidates.items() if v["gates"]}
def dominates(x, y):
    return all(a >= b for a, b in zip(x, y)) and any(a > b for a, b in zip(x, y))
nondominated = [k for k, x in feasible.items()
                if not any(dominates(y, x) for j, y in feasible.items() if j != k)]
def best(weights):
    scored = {k: sum(w*x for w, x in zip(weights, v))
              for k, v in feasible.items()}
    high = max(scored[k] for k in nondominated)
    names = "=".join(k for k in nondominated if abs(scored[k] - high) < 1e-12)
    return f"{names}:{high:.3f}"
print(f"feasible={list(feasible)}")
print(f"nondominated={nondominated}")
print(f"base={best((0.5, 0.3, 0.2))}")
print(f"availability-heavy={best((0.7, 0.2, 0.1))}")
```

## Alternatives and Trade-Offs

**Narrative analysis versus matrix.** Narrative preserves causal reasoning but is harder to scan; matrices expose symmetry but compress nuance. Use raw evidence and narrative beneath a matrix.

**Additive utility versus outranking.** Additive models are transparent when trade-offs and scales are defensible. Outranking or rule-based methods better express vetoes and incomparability but are harder to explain. Gates handle mandatory vetoes before either.

**Point estimates versus scenarios.** Points are simple and fragile. Ranges and named futures reveal uncertainty but demand more work. Use a few decision-relevant scenarios rather than invented distributions.

**Expected value versus robustness.** Expected value can favor high upside with severe tails. Minimax regret, safety margins, or robust feasibility may better suit irreversible or safety-critical decisions.

**Build evidence versus preserve reversibility.** A prototype can reduce uncertainty; it also spends time and biases teams toward sunk work. Test only decision-controlling assumptions and retain exit options.

## Failure Modes and Misconceptions

- **“The highest score is objectively best.”** It is conditional on criteria, scales, weights, evidence, and authority.
- **“Everything belongs in the matrix.”** Mandatory duties are gates, not tradeable points.
- **“More criteria improve rigor.”** Correlated criteria double-count values.
- **“A 1–5 scale is quantitative.”** Ordinal labels do not justify arithmetic.
- **“Unknown means average.”** Missing evidence is uncertainty, not a midpoint.
- **“Equal weights are neutral.”** They embed a preference on chosen scales.
- **“Stakeholder voting grants authority.”** Some obligations and rights are not majority preferences.
- **“Production data is universal evidence.”** It reflects one workload and history.
- **“Vendor benchmark settles performance.”** Workload, configuration, and incentives differ.
- **“Pareto-optimal means optimal.”** It only means nondominated in the modeled set.
- **“A dominated option can stay for fairness.”** If it matters, a criterion or constraint is missing.
- **“Transition cost is temporary and ignorable.”** It can make a destination infeasible.
- **“Reversibility is indecision.”** It is valuable under uncertainty.
- **“Consensus removes risk.”** Shared belief can share one blind spot.
- **“A decision record freezes architecture.”** It defines triggers for responsible revision.

## Worked Examples

### Example 1

**Gate before score.** Candidate D has perfect nominal performance, cost, and change scores but cannot meet required data residency. Candidate B scores lower but passes. D is excluded before aggregation; only the authorized legal/data authority can change the gate. **Conclusion:** mandatory compliance cannot be compensated by technical attractiveness.

### Example 2

**Dominance.** A=(0.8,0.5,0.6), B=(0.7,0.8,0.7), and C=(0.6,0.4,0.5). Both A and B dominate C; neither dominates the other. C is removed, while A and B form the frontier. **Conclusion:** dominance simplifies without inventing weights.

### Example 3

**Sensitivity exposes a tie.** At weights (0.5,0.3,0.2), A scores 0.67 and B 0.73. At availability-heavy (0.7,0.2,0.1), A gives $0.56+0.10+0.06=0.72$, while B gives $0.49+0.16+0.07=0.72$. Reporting whichever candidate happens to occur first would invent a winner, so the executable example reports both. **Conclusion:** independent recomputation must challenge polished tables and expose ties.

### Example 4

**Double-counting.** A matrix gives separate 20% weights to latency, responsiveness, and interactive performance, all measured by the same p99 scenario. The 60% combined influence is hidden. The team keeps one scenario-based latency value and adds distinct throughput and operator criteria. **Conclusion:** a value tree prevents three labels from voting for one consequence.

### Example 5

**Uncertain restore.** Managed candidate restore is measured at 42–55 minutes; self-hosted is estimated 20 minutes by its advocate. The recovery gate is 30 minutes. The latter does not pass from opinion; a representative restore test shows 68 minutes. Both fail, so the team changes topology or legitimately revises the contract. **Conclusion:** missing evidence cannot be scored as favorable.

### Example 6

**Migration changes the result.** A service architecture has better steady-state team autonomy but needs 18 months of dual writes with an unproven reconciliation path. A modular monolith meets the same current scenarios in four months and preserves extraction seams. Under a nine-month deadline, the service candidate is infeasible. **Conclusion:** compare reachable architectures, not ideal destinations.

### Example 7

**Cohort hidden by average.** Two login designs have equal mean latency. One has 12-second p99 on older assistive devices due to a large client bundle. Adding population-specific accessibility scenarios changes the evidence and eliminates that candidate. **Conclusion:** averages and missing stakeholders can make an invalid design look viable.

### Example 8

**Prototype the uncertainty.** Database candidates differ mainly on a predicted hot-key workload. Instead of building both systems, the team generates production-shaped skew, tests concurrency, recovery, and cost, and records versions. The favored supplier fails at the 99.9th percentile. **Conclusion:** a discriminating experiment targets the sensitivity point.

### Example 9

**Organization fit.** Event sourcing scores well on audit and replay but the only experienced operator leaves in three months, hiring is frozen, and the chosen store requires specialist response. Training and simplification scenarios expose concentration risk. A simpler append history wins temporarily with a review trigger. **Conclusion:** team capability is a system constraint, not an implementation detail.

### Example 10

**Public warning system.** Central, federated, and hybrid candidates all meet basic alert delivery. Scenarios cover local network loss, false warning correction, multilingual accessibility, compromised issuer, and regional autonomy. A weighted score does not choose warning authority; law and emergency governance define gates. The hybrid remains nondominated and has the strongest reversible pilot. **Conclusion:** structured comparison supports, but cannot replace, legitimate public authority.

## Cross-Program Connections

- [Software Engineering: Software Patterns](../../11-software-engineering-patterns/ROADMAP.md) supplies recurring solution forms, not context-free winners.
- [Software Engineering: Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns operational experiments and production evidence.
- [Software Engineering: Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns measurement, sampling, uncertainty, and experimental validity.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns data-governance criteria and authority.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns threat and control evidence.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns system-wide alternatives, stakeholders, and lifecycle trade studies.

## References

1. ISO/IEC/IEEE, *42010:2022 — Architecture Description*, edition 2, November 2022. [ISO record](https://www.iso.org/standard/74393.html). Published status checked 2026-09-06.
2. ISO/IEC/IEEE, *42030:2019 — Architecture Evaluation Framework*, 2019. [ISO record](https://www.iso.org/standard/72193.html).
3. Rick Kazman et al., *The Architecture Tradeoff Analysis Method*, CMU/SEI-98-TR-008, 1998. [SEI record](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/).
4. Software Engineering Institute, “Cost Benefit Analysis Method (CBAM),” 2018. [SEI record](https://www.sei.cmu.edu/library/cost-benefit-analysis-method-cbam/).
5. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
6. Ralph L. Keeney and Howard Raiffa, *Decisions with Multiple Objectives*, Cambridge University Press, 1993.
7. Valerie Belton and Theodor Stewart, *Multiple Criteria Decision Analysis*, Springer, 2002.
8. Daniel Kahneman, Paul Slovic, and Amos Tversky, eds., *Judgment under Uncertainty: Heuristics and Biases*, Cambridge University Press, 1982.
9. Douglas W. Hubbard, *How to Measure Anything*, 3rd ed., Wiley, 2014.
10. David J. Snowden and Mary E. Boone, “A Leader’s Framework for Decision Making,” *Harvard Business Review*, 2007.
11. Martin Kleppmann and Chris Riccomini, *Designing Data-Intensive Applications*, 2nd ed., O’Reilly Media, February 2026. [Publisher record](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/).
12. David L. Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM* 15(12), 1972. [DOI record](https://doi.org/10.1145/361598.361623).

## Exercises

### Exercise 1

**Separate gates and preferences.** Classify residency law, maximum outage, preferred programming language, five-year cost, accessibility, and team familiarity as gate or criterion for a public benefit system. Explain what additional context can change each classification.

### Exercise 2

**Compute dominance and score.** Candidates X=(0.9,0.4,0.6), Y=(0.7,0.8,0.7), and Z=(0.6,0.5,0.5) pass gates. Identify dominance. Score the frontier at weights (0.4,0.35,0.25), then explain why the arithmetic is insufficient.

### Exercise 3

**Diagnose a deceptive matrix.** A team uses 25 criteria scored 1–5, fills unknowns with 3, gives equal weights, and reports a winner by 0.04. Identify at least six validity defects and design the next evidence step.

### Exercise 4

**Compare transition paths.** Compare modular-monolith, service, and purchased-platform candidates for a five-year system replacement. Specify common views, scenarios, transition states, economics, organization, exit, uncertainty, and review triggers.

### Exercise 5

**Transfer to regional blood supply.** Design a comparison process for architectures coordinating blood inventory, hospitals, mobile collection, intermittent links, privacy, expiry, disaster surge, and regulatory evidence. State gates, scenarios, criteria, evidence, sensitivity, governance, residual risk, and a reversible next step.

## Answers to the Exercises

### Answer 1

Residency law and accessibility are gates when binding law and legitimate policy require them. Maximum outage is a gate if mission authority sets a hard limit; otherwise availability levels may be compensatory. Five-year cost is a gate under a hard funding ceiling and a criterion within it. Programming language and team familiarity are usually criteria or evidence affecting change/operation, not gates, unless an explicit support, certification, or staffing constraint makes alternatives infeasible. Context must name jurisdiction, population, mission consequence, funding authority, support horizon, and available mitigations. No team preference can waive a right or legal duty.

### Answer 2

Y dominates Z because 0.7≥0.6, 0.8≥0.5, and 0.7≥0.5 with strict improvement. X does not dominate Y and Y does not dominate X, so X and Y form the frontier. $S(X)=0.4(0.9)+0.35(0.4)+0.25(0.6)=0.65$. $S(Y)=0.4(0.7)+0.35(0.8)+0.25(0.7)=0.735$. Y leads by 0.085 conditionally. The decision still requires raw measures, scale/value functions, uncertainty, correlation, sensitivity, transition, residual risk, stakeholder priorities, and authority.

### Answer 3

Defects include ordinal arithmetic, arbitrary equal weights, unknown-as-midpoint optimism, likely correlated criteria, no gates, no raw evidence, false precision, no uncertainty, no sensitivity, and a tiny unexplained margin. Rebuild a value tree from prioritized scenarios, identify mandatory gates, consolidate duplicated consequences, define direct measures and meaningful value functions, and retain unknowns. The next experiment should target the uncertain input with greatest ability to reverse the decision—such as representative restore, workload, migration, or accessibility evidence—with predeclared acceptance criteria.

### Answer 4

Describe all three through the same context, responsibility, runtime, data, deployment, security, operation, delivery, organization, migration, and exit views. Gate on mandatory integrity, privacy, accessibility, recovery, schedule, and budget. Exercise peak, failure, attack, representative changes, data correction, staff loss, supplier outage, migration, rollback, and retirement.

Measure lifecycle cost, recovery, change coordination, performance, operational load, security exposure, data-authority complexity, skills, and portability from raw evidence with ranges. Model intermediate states: module extraction, service dual operation, or platform data migration; identify authority transfer and last reversible point. Include contracts, price, hiring, training, support, decommissioning, and data exit. Run sensitivity across growth, staff, incident, price, weights, and deadline. Record dissent and triggers such as scale, missed change time, vendor terms, or failed restore. A valid answer may recommend different candidates but must compare equivalent scope and reachable transitions.

### Answer 5

Regulatory traceability, patient privacy, authenticated hospital authority, blood-type and unit identity integrity, no double allocation, expiry enforcement, accessible clinical workflows, bounded acknowledged loss, and tested recovery are gates. Scenarios cover routine allocation, mobile offline collection, concurrent request for the last compatible unit, recall, correction, refrigeration evidence, hospital/link loss, malicious issuer, regional disaster surge, restore, schema change, and supplier exit.

Compare coherent central, federated, and hybrid candidates through inventory/data authority, reservation rights, causal events, deployment, trust, operations, organization, migration, and reconciliation. Criteria use raw measures for allocation latency, offline duration, recovery, stale risk, change effort, operator burden, five-year cost, surge capacity, and reversibility. Clinical and regulatory experts validate semantics; privacy/security teams evaluate threats; hospitals, mobile teams, accessibility experts, disaster authorities, and affected communities supply scenarios. Prototypes test the controlling uncertainties with production-shaped skew and failure.

Exclude failed gates, remove dominated options, then show the frontier, weight/value assumptions, uncertainty intervals, break-even points, and common causes. Do not let a score authorize allocation policy or patient-data use. Preserve residual risks, dissent, owners, and review triggers. A reversible next step is a bounded regional pilot with parallel authoritative reconciliation, preallocated offline rights, no irreversible legacy shutdown, explicit abort criteria, and independent recovery and accessibility testing. Real deployment remains subject to legitimate clinical, regulatory, privacy, operational, and public authorities.
