---
module_id: SYSENG-042
program: Systems Engineering
level: 1
module_number: 42
title: Weighted Trade Studies
status: complete
last_verified: 2026-08-31
---

# Weighted Trade Studies

## One-Page Review

### Governing question

How can a weighted trade study compare feasible alternatives reproducibly while preserving raw evidence, scale and weight meaning, uncertainty, sensitivity, stakeholder authority, and the distinction between a matrix result and the final decision?

### Essential definitions

- A **trade study** is a controlled comparison of alternatives against decision-relevant objectives, constraints, measures, evidence, preferences, and uncertainty.
- A **study charter** fixes the decision question, authority, scope, schedule, objectives, constraints, alternatives process, method, roles, evidence expectations, and deliverables before results are known.
- A **trade space** is the set of candidate alternatives and combinations within the declared decision boundary.
- A **trade tree/morphological structure** organizes design choices and combinations so alternatives can be generated and pruned transparently.
- A **screening criterion** determines feasibility or admissibility before compensatory scoring.
- A **performance matrix** contains raw measured or predicted outcomes and uncertainty for every feasible alternative and criterion.
- A **value matrix** maps raw outcomes through declared value/utility functions to comparable preference scales.
- A **weighted score** is an aggregation such as (V(a)=\sum_iw_i u_i(x_i(a))) under explicit assumptions; it is not an objective percentage of merit.
- A **local weight** allocates importance within an objective branch. A **global weight** equals the product of weights along the hierarchy and must reconcile at the leaves.
- **Rank reversal** is a change in relative ordering after adding/removing alternatives or changing method inputs; it may reveal alternative-dependent normalization or method behavior.
- A **break-even analysis** finds the input or preference value at which alternatives tie.
- A **study baseline** identifies the exact charter, alternatives, criteria, data/models, functions, weights, computations, uncertainty, sensitivities, reviews, recommendation, and decision.
- **Independent review** challenges the study method and evidence without owning the preferred alternative or final decision.

### Central model, mechanism, or theorem

After mandatory screening, let feasible alternatives be (A_F), criteria (i=1,\ldots,n), raw performance (x_i(a)), value functions (u_i), and swing weights (w_i\ge0,\sum_iw_i=1):

$$
V(a)=\sum_{i=1}^{n}w_i u_i(x_i(a)).
$$

For an objective hierarchy, leaf/global weight is:

$$
w_{leaf}=\prod_{h\in path(root,leaf)}w_{h\mid parent(h)}.
$$

The leaf weights should sum to one when every sibling set is normalized and the hierarchy is complete.

For two alternatives (a,b), score difference is:

$$
\Delta V_{ab}=\sum_iw_i\left(u_i(x_i(a))-u_i(x_i(b))\right).
$$

Solving (\Delta V_{ab}=0) gives a break-even boundary. A nominal positive difference is meaningful only relative to uncertainty in performance, functions, weights, evidence, and model structure.

### Critical invariants

- The charter, authority, decision deadline, configuration, scope, stakeholders, study team, review roles, and method are controlled before final scoring.
- Alternatives are generated broadly enough for the decision, described at comparable scope/maturity, and include status quo/no-action when meaningful.
- Pruning and infeasibility decisions name criteria, evidence, uncertainty, authority, and reconsideration triggers.
- Mandatory constraints are screened before enhancing scores and cannot be offset silently.
- Raw performance and uncertainty remain visible separately from normalized values and weighted totals.
- Every cell traces to an operational measure, configuration/scenario, source/model, analyst, date, evidence strength, uncertainty, and limitation.
- Value functions use fixed meaningful anchors and shapes; alternative-dependent normalization is not used without understanding rank effects.
- Weights are elicited for specified swings on specified scales from legitimate preference authority; equal weights are treated as a substantive choice.
- Hierarchical local/global weights reconcile, and decomposition does not duplicate an outcome across branches.
- Additive compensation and preference-independence assumptions are reviewed; constraints, interactions, or other methods are used when needed.
- Missing values are never disguised as neutral midpoint scores; intervals, scenarios, information actions, or explicit incompleteness are used.
- Dominance, Pareto tradeoffs, uncertainty, correlation, break-even values, and multi-way sensitivity are examined before recommendation.
- Calculation artifacts are reproducible, versioned, checked independently, and protected from hidden formulas, stale links, rounding, or manual overwrite.
- Recommendation, matrix result, and final authority decision are distinct; a lower-scoring selection has visible rationale and model implications.
- New alternatives, changed evidence/preferences/constraints, or implementation learning trigger controlled update rather than silent spreadsheet edits.

### Common failures

Common failures include beginning with a favored design; defining alternatives at unequal maturity; pruning without records; using criteria selected after preliminary scores; mixing requirements and preferences; entering expert 1–10 guesses instead of raw measures; normalizing best/worst to the current alternatives; applying linear scales to thresholds; treating weights as context-free votes; weighting categories and subcriteria without multiplying them; double counting cost, schedule, reliability, risk, and mission effects; filling missing cells with 0.5; ignoring evidence quality and correlation; reporting a winner separated by less than rounding uncertainty; varying one weight while holding an invalid model fixed; hiding formulas and overrides in a spreadsheet; excluding affected stakeholders; and treating the highest score as the decision.

### Compact example

Three feasible alternatives are valued on reliability, latency, and lifecycle burden with swing weights 0.45, 0.35, and 0.20. A has values 0.80/0.50/0.70 and scores 0.675. B has 0.60/0.90/0.60 and scores 0.705. C has 0.90/0.40/0.80 and also scores 0.705. The result is a tie under the nominal model, not permission to declare one winner by extra decimals. Criterion profiles, uncertainty, dominance, break-even weights, stakeholder differences, and valuable new evidence determine the recommendation.

### Connections

SYSENG-041 defines criteria, value/utility functions, weights, constraints, dominance, and sensitivity. This module turns them into an auditable study workflow. SYSENG-043 adds integrated cost/schedule/performance/risk treatment; SYSENG-044–045 deepen sensitivity and uncertainty; SYSENG-046–048 address readiness and risk; SYSENG-049–050 govern rationale and stakeholder-value architecture selection. Configuration and evidence from earlier modules make each alternative comparison reproducible.

## Governing Question

What study process makes the comparison fair enough to inform a consequential choice, and what evidence shows that the ranking is robust rather than an artifact of framing, normalization, weights, missing data, or spreadsheet construction?

A weighted matrix is the middle of the process, not the beginning or end. The work starts by framing the decision and generating comparable alternatives; it ends with challenge, recommendation, authority decision, implementation, and monitoring. The arithmetic is often the easiest part.

## Why This Matters

Trade studies are used because engineering alternatives differ across incompatible dimensions and incomplete evidence. Done well, a study exposes tradeoffs and tells decision makers why one option fits their objectives under current knowledge. Done poorly, it gives a predetermined choice a numerical costume.

NASA's current Decision Analysis guidance calls for decision framing, operational criteria, a sufficiently broad set of alternatives, appropriate methods, evaluation with uncertainty, robustness assessment, recommendation, final decision, and a durable report. It identifies weighted trade-off matrices as one possible method, not the universal default. NASA Design Solution Definition guidance calls for open and inclusive comparisons of technical performance, lifecycle cost, schedule, risk, maturity, operations, and enabling products.

NASA's Systems Engineering Toolbox describes weighted scoring and sensitivity while warning that close totals should be reconsidered relative to confidence. GAO analyses of alternatives emphasize stakeholder roles, validated/protected data, feasibility screening, weighted comparison, sensitivity to key assumptions, and independent review. These are governance controls as much as mathematical ones.

The strongest study preserves three layers: raw physical/operational outcomes; preference mappings; and decision. If the preference authority changes, raw outcomes remain. If evidence changes, value functions remain inspectable. If the authority chooses differently, the reason is recorded rather than backfit into cells.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. decision frame, authority, objectives, stakeholders, ConOps, lifecycle, configurations, constraints, deadlines, reversibility, and implementation consequences;
2. alternative-generation methods, trade trees, architecture/design/operational options, status quo, supplier/reuse options, and comparable maturity definitions;
3. requirements, measures, value/utility functions, swing weights, evidence, uncertainty, dependence, dominance, sensitivity, and value of information;
4. cost, schedule, performance, risk, human, safety, security, environmental, supplier, manufacturing, operations, maintenance, and retirement models;
5. configuration, provenance, technical data, peer/independent review, change control, and decision-record practices;
6. basic matrix arithmetic, hierarchical weights, break-even algebra, intervals/distributions, correlation, and reproducible computation.

As a retrieval test, inspect a matrix that rates alternatives `good`, `fair`, and `poor`. Ask for operational definitions, raw outcomes, evidence, uncertainty, value anchors, evaluator authority, configuration, and whether the scale is ordinal. If `good=3` and `poor=1` are added, the arithmetic assumes interval meaning not supplied by the words.

## Learning Objectives

After completing this module, you should be able to:

1. charter a weighted trade study with decision, authority, scope, roles, methods, review, and records;
2. generate and prune a broad, comparable alternative set transparently;
3. separate screening constraints, raw performance, value mapping, weights, and aggregate scores;
4. construct flat and hierarchical weighted matrices with reconciled swing weights;
5. populate cells with traceable evidence and uncertainty instead of unsupported ordinal guesses;
6. detect alternative-dependent normalization, double counting, missing-data substitution, and rank reversal;
7. calculate nominal scores, score differences, break-even weights, dominance, and sensitivity;
8. design reproducible spreadsheets/code with independent calculation and data review;
9. communicate ties, close rankings, uncertainty, stakeholder conflict, and lower-scoring decisions honestly;
10. baseline, update, and audit a trade study through implementation learning.

## Core Exposition

**Write the charter.** Include study ID/title, decision/question, authority, sponsors, system/lifecycle/configuration boundary, objectives, mandatory constraints, affected stakeholders, schedule/deadline, alternatives-generation scope, methods, team roles, evidence standards, uncertainty/sensitivity, independent review, deliverables, approvals, and change rules. Prevent result-driven method drift.

**Separate roles.** Technical experts produce evidence; decision analysts structure the method; stakeholders articulate outcomes; preference authority approves value functions/weights; configuration/data owners preserve inputs; independent reviewers challenge; decision authority selects. Participants may hold multiple roles on small efforts, but conflicts remain visible.

**Generate alternatives before heavy scoring.** Use trade trees, morphological combinations, architecture variants, supplier/reuse options, operational concepts, centralization/distribution, technology, human/automation, schedule/phasing, and status quo. Include combinations only when physically/organizationally coherent. Avoid several cosmetic versions of the favored concept.

**Describe alternatives comparably.** Each alternative needs boundary, configuration, architecture, interfaces, operating concept, lifecycle, enabling products, maturity, assumptions, risks, cost/schedule basis, and evidence level. A detailed preferred design will otherwise appear riskier than a vague competitor whose problems remain unstated.

**Screen feasibility transparently.** Apply mandatory requirements, safety/legal/security boundaries, resource limits, schedule windows, technology/supplier viability, and compatibility. Use uncertainty/margin. Record whether an option is infeasible, conditionally feasible, redesignable, or pruned for study economy, and who authorized it.

**Build an objective hierarchy.** Trace fundamental outcomes to criteria. Use categories for cognition/ownership, then check leaf criteria for completeness, overlap, causal dependence, and meaningful swings. Category labels are not automatically scoreable.

**Define the raw performance matrix.** Rows/columns show criteria and alternatives; each cell includes estimate/measurement, unit, direction, configuration/scenario, source/model, uncertainty, evidence strength, analyst/date, and limitations. Keep narrative or linked evidence adjacent to numbers.

**Freeze scale semantics before mapping.** Value functions state fixed anchors, direction, shape, threshold/saturation, clipping/extrapolation, and authority. Do not normalize to the observed alternatives unless the method and rank-reversal implications are deliberately accepted.

**Elicit weights after scales.** Ask the authority to compare defined worst-to-best swings, not criterion names. Use direct swing ranking, ratio judgments, lotteries, pairwise methods, or facilitated deliberation appropriate to rigor. Check consistency and document disagreements.

**Calculate hierarchical weights.** Normalize siblings locally. Multiply parent and child weights to obtain global leaf weights, then verify leaves sum to one. Example: performance branch 0.60, latency local 0.40 gives latency global 0.24. Do not apply 0.60 and 0.40 independently as if both were global.

**Control compensation.** Confirm a gain on one criterion may compensate a loss on another across declared ranges. Move noncompensatory conditions to constraints/veto rules or use a different model. Add interactions when preferences depend on combinations, but recognize added elicitation/data complexity.

**Handle qualitative evidence without fake intervals.** Use constructed scales with observable level descriptions. If only ordinal, use methods that respect order or scenario deliberation; do not assume the gap between levels 1 and 2 equals 4 and 5. Record assessor reasoning and uncertainty.

**Do not hide missing data.** Represent missing/indeterminate, bound with intervals, evaluate best/worst cases, collect information, or suspend ranking. A neutral midpoint is a preference and performance claim with no evidence.

**Inspect dominance and Pareto structure.** Before totals, show which alternatives are dominated and the tradeoff frontier. Dominance analysis can reveal formula errors, duplicated alternatives, or omitted objectives. Retain dominated options in the audit trail with disposition.

**Compute reproducibly.** Use locked formulas or versioned code, explicit input tables, units/schema checks, named functions, deterministic rounding, automated weight/range/missingness checks, and generated outputs in controlled artifacts. Independently recompute sample/full cases. Avoid hidden cells, macros, external links, and manual score overrides.

**Show contribution profiles.** Report (w_i u_i) by criterion, not only totals. A total can hide that two alternatives have fundamentally different strengths and risks. Contribution charts/tables also expose one criterion or duplicate cluster dominating.

**Analyze break-even values.** Solve for the weight, performance, cost, probability, or threshold where alternatives tie. Compare it to credible ranges and authority preferences. This converts “sensitive” into an actionable question.

**Propagate uncertainty.** Evaluate intervals, scenarios, distributions, and correlation through performance and value functions. Show score/rank ranges or probability of preference only when underlying probability semantics are valid. Do not treat independent cell uncertainty when shared models drive several cells.

**Run sensitivity beyond weights.** Vary anchors, function shapes, performance estimates, cost/schedule horizons, discounting, risk assumptions, constraints, evidence scenarios, correlation, alternative definitions, and aggregation method. Use plausible joint variations, not just one-at-a-time extremes.

**Test rank reversal.** Add/remove irrelevant or dominated alternatives and observe whether relative order changes. Alternative-dependent min–max normalization commonly causes it. Method-specific rank reversal is not always automatically wrong, but it must be understood and consistent with preference meaning.

**Assess value of information.** For unstable rankings, identify which cell/function/weight uncertainty causes reversal, what evidence could reduce it, cost/schedule of acquisition, and whether it arrives before commitment. Do not commission broad studies when one discriminating prototype would resolve the decision.

**Perform independent review.** Review charter compliance, alternative breadth/equality, criteria/constraints, data/model validity, value/weight authority, calculations, uncertainty/correlation, sensitivity, stakeholder inclusion, conflicts, and report reproducibility. Independence does not mean uninformed; reviewers need domain and method competence.

**Make recommendation proportional to evidence.** If one alternative dominates robustly and constraints hold, recommend it with limits. If scores overlap, present close alternatives and decision drivers. If evidence is insufficient, recommend information or reversible option. Never manufacture separation by extra decimals.

**Record the authority decision.** Preserve study result, recommendation, selected alternative, rationale, accepted tradeoffs/risks, dissent, conditions, implementation/configuration, monitoring, and reopening triggers. If a lower-scoring option is selected, record whether the model omitted/incorrectly represented a factor or whether authority used an external portfolio constraint.

**Baseline and update the study.** Version charter, alternatives, criteria, raw data, functions, weights, code/spreadsheet, uncertainty, sensitivity, review findings, recommendation, and decision. On change, show exact deltas and whether prior evidence/ranking remains valid. Do not overwrite history.

**State evidence limits.** A correctly calculated matrix proves arithmetic under its inputs. It cannot prove alternative completeness, performance predictions, legitimate preferences, independence, ethical distribution, or final choice. Independent review reduces but does not eliminate model risk.

The following checker reproduces a small nominal matrix and deliberately reports a tie.

<!-- bijux-verify: {"id":"weighted-trade-matrix-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"weights_sum=1.000\nscore_A=0.675\nscore_B=0.705\nscore_C=0.705\nranking=B,C,A\ntop_tie=1\nmargin_top_over_A=0.030\nevidence=declared_values_only\n","stderr":""}} -->
```python
weights = {"reliability": 0.45, "latency": 0.35, "lifecycle": 0.20}
values = {
    "A": {"reliability": 0.80, "latency": 0.50, "lifecycle": 0.70},
    "B": {"reliability": 0.60, "latency": 0.90, "lifecycle": 0.60},
    "C": {"reliability": 0.90, "latency": 0.40, "lifecycle": 0.80},
}
scores = {
    alternative: sum(weights[name] * profile[name] for name in weights)
    for alternative, profile in values.items()
}
ranking = sorted(scores, key=lambda name: (-scores[name], name))
print(f"weights_sum={sum(weights.values()):.3f}")
for alternative in ("A", "B", "C"):
    print(f"score_{alternative}={scores[alternative]:.3f}")
print("ranking=" + ",".join(ranking))
print(f"top_tie={int(scores[ranking[0]] == scores[ranking[1]])}")
print(f"margin_top_over_A={scores[ranking[0]] - scores['A']:.3f}")
print("evidence=declared_values_only")
```

Alphabetical order breaks the displayed tie only for deterministic output; it is not a preference rule.

## Definitions and Notation

Let alternatives (A), feasible subset (A_F), criteria (C), raw performance (x_{ai}), value (v_{ai}=u_i(x_{ai})), global weights (w_i), evidence (e_{ai}), and model/configuration version (b).

Screening:

$$
A_F=\{a\in A:\forall m\in M,g_m(a)=true\}.
$$

Score and contribution:

$$
V_a=\sum_iw_iv_{ai},\qquad contribution_{ai}=w_iv_{ai}.
$$

Hierarchical global weight:

$$
w_i=\prod_{h\in path(root,i)}w_{h\mid parent(h)}.
$$

For intervals (v_{ai}\in[\underline v_{ai},\overline v_{ai}]) with fixed nonnegative weights, a conservative independent-envelope bound is:

$$
V_a\in\left[\sum_iw_i\underline v_{ai},\sum_iw_i\overline v_{ai}\right].
$$

It is not a probability interval and may be too wide or invalid under coupled feasibility; preserve dependence.

Break-even between (a,b) for parameter (\theta):

$$
V_a(\theta)-V_b(\theta)=0.
$$

The study baseline (b) identifies every object used to evaluate this equation.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—charter and governance.** Fix decision scope, roles, alternative process, method, evidence, review, authority, schedule, and controlled outputs.

**Mechanism 2—trade-space construction.** Generate, describe, screen, and prune alternatives with comparable boundaries/maturity and traceable rationale.

**Mechanism 3—criteria and evidence.** Build fundamental-objective hierarchy, operational measures, raw performance matrix, uncertainty, and evidence provenance.

**Mechanism 4—preference model.** Define fixed value functions, swing weights, global hierarchy weights, compensation/independence, stakeholder authority, and noncompensatory rules.

**Mechanism 5—reproducible evaluation.** Compute values/contributions/totals, verify formulas, inspect dominance/Pareto, propagate uncertainty, and run break-even/rank-reversal/sensitivity tests.

**Mechanism 6—challenge and decision.** Conduct independent review, recommend proportionally, record authority decision/dissent, baseline artifacts, and reopen on triggers.

The study integrity argument requires comparable alternatives, complete enough objectives, valid evidence, meaningful scales/weights, suitable aggregation, correct calculations, visible uncertainty/sensitivity, and legitimate authority. A high score cannot prove these premises.

## Alternatives and Trade-Offs

**Flat matrices** are easy to audit but cognitively difficult with many criteria. **Hierarchical matrices** improve structure but can hide double counting and local/global weight mistakes.

**Weighted additive scoring** is transparent and compensatory. **Outranking, lexicographic, goal-programming, Pareto, and scenario methods** better fit vetoes, interactions, or deep uncertainty but can be harder to explain.

**Spreadsheets** are accessible and reviewable at small scale. **Versioned code/notebooks/models** improve automation and reproducibility but require environment/dependency control and accessible outputs. Both need independent checks.

**Expert judgment** covers sparse evidence. **Empirical/model data** provide traceable performance. Structured elicitation should separate evidence estimation from preference and quantify disagreement/limitations.

**One comprehensive study** aligns system tradeoffs. **Linked focused studies** allow domain depth. Link scope, assumptions, common data, and decision authority to prevent inconsistent local optima.

## Failure Modes and Misconceptions

**“The matrix makes the decision objective.”** It makes selected evidence/preferences explicit under assumptions; it does not remove judgment.

**“All alternatives are treated equally because rows are identical.”** Unequal definition maturity, evidence quality, or hidden assumptions can bias cells.

**“Scores 1–10 are data.”** Without operational interval-scale meanings, they are labels with unsupported arithmetic.

**“Weights sum to 100, so they are valid.”** Sum checks arithmetic, not swing semantics, authority, independence, or overlap.

**“Subcriterion weights already include the parent.”** Only if defined as global; local weights must be multiplied.

**“Missing means average.”** Missing evidence can decide the result; show it as missing or bounded.

**“A 0.01 lead is a winner.”** Compare it to uncertainty, elicitation precision, sensitivity, and rounding.

**“Sensitivity only means ±10% weights.”** Vary credible evidence, models, anchors, functions, constraints, scenarios, dependence, and method.

**“Independent review validates the decision.”** It challenges method/evidence; authority still owns preferences and choice.

## Worked Examples

### Example 1

**Nominal matrix with a tie.** The embedded checker gives B and C both 0.705 and A 0.675. B emphasizes latency; C emphasizes reliability/lifecycle. The study reports a tie under displayed precision and profiles, then tests uncertainty and preference break-even rather than using alphabetical order.

### Example 2

**Hierarchical weights.** Top objectives are performance 0.50, lifecycle 0.30, and risk 0.20. Under performance, throughput local weight is 0.60 and latency 0.40. Global weights are 0.30 and 0.20. If lifecycle leaves total 0.30 and risk leaves total 0.20, all leaves sum to one.

### Example 3

**Mandatory screening.** An option scores highly but violates a 60 °C safety limit with credible lower bound 61 °C. It is infeasible; cost and schedule cannot compensate. Keep its analysis as a redesign/reference and document whether requirement relief is legally/technically possible.

### Example 4

**Alternative-dependent normalization reverses meaning.** With lower cost better and current costs 10 and 20, min–max gives values 1 and 0. Adding a cost-100 dominated option changes the cost-20 value to (100-20)/(100-10)=0.8889 without any change in preference or performance. Fixed anchors prevent the irrelevant option from improving an existing alternative.

### Example 5

**Double counting in a hierarchy.** `Operational effectiveness` includes availability; separate leaves also weight reliability, maintainability, downtime, and availability. The model may reward the same causal outcome repeatedly. Restructure using mission outcome plus independent resource/human effects or an explicit causal model.

### Example 6

**Score intervals overlap.** A is [0.62,0.76], B [0.68,0.72]. B's interval is narrower, but neither robustly dominates because A can be lower or higher. Identify drivers/correlation and decision value of new evidence; do not compare midpoints only.

### Example 7

**Break-even weight.** A values (0.9,0.4), B (0.6,0.8), weights (w,1-w). As SYSENG-041 derived, tie occurs at (w=4/7\approx0.5714). The authority's credible swing-weight interval determines whether the nominal choice is robust.

### Example 8

**Missing supplier evidence.** Alternative C lacks validated maintenance labor. Entering 0.5 may let it win. Instead use a defensible interval based on analogous systems, show best/worst rank, request a maintainability demonstration, or retain C as indeterminate.

### Example 9

**Separate technical and preference roles.** Engineers estimate mass/performance/reliability with evidence; maintainers/operators/patients describe impacts; analysts construct scales; the authorized body approves swings and decides; an independent team audits method/data. Voting experts should not silently alter technical cells to express preference.

### Example 10

**Alternative changes after scoring.** A supplier changes firmware, price, support term, and interface. The study creates a new alternative/configuration or revision, updates affected raw cells/evidence/risks, reruns sensitivity, and records delta. It does not overwrite old scores and retain the old recommendation label.

## Cross-Program Connections

**Platform engineering.** Platform matrices compare developer experience, SLOs, security, portability, cost, operations, migration, and lock-in; pilots and workload evidence should populate raw cells.

**API and service engineering.** Protocol/architecture choices trade semantics, latency, reliability, consistency, evolvability, security, provider/consumer burden, and operations.

**Data engineering.** Storage/pipeline choices trade correctness, freshness, latency, capacity, replay, lineage, privacy, cost, and operational complexity with correlated evidence.

**Object-oriented and functional programming.** Paradigm/design decisions need workload, defect/change, team, ecosystem, performance, and lifecycle evidence rather than aesthetic 1–10 ratings.

**Risk, cost, and schedule.** These are profiles with uncertainty and dependence, not catch-all penalty scores; SYSENG-043 deepens their joint treatment.

## References

1. NASA, *Systems Engineering Handbook, Section 6.8: Decision Analysis*, current web edition. <https://www.nasa.gov/reference/6-8-decision-analysis/>
2. NASA, *Systems Engineering Handbook, Section 4.4: Design Solution Definition*, current web edition. <https://www.nasa.gov/reference/4-4-design-solution-definition/>
3. NASA, *Systems Engineering “Toolbox” for Design-Oriented Engineers*, NASA RP-1358. <https://ntrs.nasa.gov/citations/19950012517>
4. NASA, *NASA Risk-Informed Decision Making Handbook*, NASA/SP-2010-576. <https://ntrs.nasa.gov/citations/20100021361>
5. U.S. GAO, *DOE and NNSA Project Management: Analysis of Alternatives Could Be Improved by Incorporating Best Practices*, GAO-15-37. <https://www.gao.gov/products/gao-15-37>
6. U.S. GAO, *Defense Acquisitions: Analysis of Processes Used to Evaluate Active Protection Systems*, GAO-07-759. <https://www.gao.gov/products/gao-07-759>
7. NASA, *Systems Engineering Handbook, Section 6.7: Technical Assessment*, current web edition. <https://www.nasa.gov/reference/6-7-technical-assessment/>
8. NASA, *Systems Engineering Handbook, Section 6.6: Technical Data Management*, current web edition. <https://www.nasa.gov/reference/6-6-technical-data-management/>
9. NIST, *Decision Support System for Material and Manufacturing Process Selection*, official publication record. <https://www.nist.gov/publications/decision-support-system-material-and-manufacturing-process-selection>
10. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>

## Exercises

### Exercise 1

Weights are performance 0.50, maintainability 0.30, lifecycle cost 0.20. Value profiles are A=(0.8,0.4,0.7), B=(0.6,0.9,0.5), C=(0.7,0.6,0.8). Compute totals, rank, contributions, and nominal margins. State what must be reviewed before recommending.

### Exercise 2

Top-level weights are mission 0.55, lifecycle 0.30, risk 0.15. Mission local leaves are effectiveness 0.70 and availability 0.30; lifecycle leaves are cost 0.60 and maintainability 0.40; risk has safety 0.50 and security 0.50. Compute global leaf weights and verify their sum.

### Exercise 3

Lower latency is better. Alternatives A/B have 100/200 ms and are min–max normalized against current alternatives. Then a dominated 500 ms alternative C is added. Compute A/B values before and after. Explain why fixed 50–500 ms anchors behave differently.

### Exercise 4

Critique a study that uses five alternatives proposed by one supplier, 25 equal-weight 1–5 criteria, missing values filled with 3, formulas hidden in a shared spreadsheet, no uncertainty, and a winner ahead by 0.4%. Design the corrective review.

### Exercise 5

Design an auditable weighted trade study for centralized, distributed, and hybrid hospital medication-delivery architectures. Cover charter, roles, alternatives, screening, raw evidence, preference, uncertainty, affected groups, independent review, recommendation, decision, and reopening.

## Answers to the Exercises

### Answer 1

$$
V_A=0.50(0.8)+0.30(0.4)+0.20(0.7)=0.66.
$$

Contributions are 0.40, 0.12, 0.14.

$$
V_B=0.50(0.6)+0.30(0.9)+0.20(0.5)=0.67,
$$

with contributions 0.30, 0.27, 0.10.

$$
V_C=0.50(0.7)+0.30(0.6)+0.20(0.8)=0.69,
$$

with contributions 0.35, 0.18, 0.16. Nominal rank is C, B, A; margins are C–B 0.02, B–A 0.01, C–A 0.03.

Before recommendation review mandatory feasibility, alternative comparability, raw measures/evidence/configurations, value anchors/shapes, swing-weight authority, independence/compensation, double counting, missingness, uncertainty/correlation, dominance/Pareto profiles, break-even/sensitivity, stakeholder distributions, calculation reproducibility, and whether new evidence could reverse the close ranking. Extra decimals cannot establish separation.

### Answer 2

Mission leaves:

$$
w_{effectiveness}=0.55(0.70)=0.385,
$$

$$
w_{availability}=0.55(0.30)=0.165.
$$

Lifecycle leaves:

$$
w_{cost}=0.30(0.60)=0.18,
$$

$$
w_{maintainability}=0.30(0.40)=0.12.
$$

Risk leaves:

$$
w_{safety}=0.15(0.50)=0.075,
$$

$$
w_{security}=0.15(0.50)=0.075.
$$

Sum is (0.385+0.165+0.18+0.12+0.075+0.075=1.0). Arithmetic reconciliation does not prove independence or that safety/security are compensatory; mandatory minima or separate risk profiles may still be required.

### Answer 3

With only A=100 and B=200 ms, lower-better min–max gives:

$$
u(A)=(200-100)/(200-100)=1,
$$

$$
u(B)=(200-200)/(200-100)=0.
$$

After adding C=500:

$$
u(A)=(500-100)/(500-100)=1,
$$

$$
u(B)=(500-200)/(500-100)=300/400=0.75,
$$

and C=0. B improved from 0 to 0.75 without changing latency or stakeholder preference. With fixed 50–500 anchors:

$$
u(A)=(500-100)/450=0.8889,
$$

$$
u(B)=(500-200)/450=0.6667,
$$

before and after C is added. Fixed anchors preserve scale meaning; their choice/shape still requires authority and operational rationale.

### Answer 4

Problems include supplier-shaped trade space; potentially cosmetic/nonindependent alternatives; absent status quo/other technologies; 25-criterion dilution/overlap; equal weights masquerading as neutrality; ordinal arithmetic; unsupported midpoint imputation; hidden formulas/overrides; no raw evidence/provenance/configuration; no constraints; no uncertainty/correlation/sensitivity; absent stakeholder/authority roles and independent review; and 0.4% separation likely below model precision.

Corrective review pauses recommendation; recharters decision and independent roles; broadens/comparably defines alternatives; builds fundamental objective hierarchy; screens mandatory constraints; reduces/operationalizes nonoverlapping criteria; populates raw evidence with uncertainty; establishes fixed value functions and swing weights under legitimate authority; handles missing cells with bounds/information actions; reconstructs calculations in controlled transparent code/spreadsheet; independently recomputes; inspects dominance/Pareto, contributions, break-even, rank reversal, multi-way sensitivity, correlation, stakeholder profiles, and value of information; records conflicts/dissent; then issues a proportional recommendation or declares no robust winner.

### Answer 5

Charter the exact care settings/populations, lifecycle horizon, architecture boundary, clinical/institutional authority, affected patients/nurses/pharmacy/biomedical/IT/security/facilities, regulatory obligations, decision date, transition/reversibility, methods, evidence, review, and records. Separate technical, clinical, preference, analysis, review, and final-decision roles.

Define centralized, distributed-local, hybrid, status quo, and credible supplier/operational variants at comparable maturity, including network-loss modes, safe local control, library/order/patient/record paths, alarms, staffing, maintenance, update, facilities, suppliers, and migration. Screen mandatory correct patient/drug/dose/rate/order; safe fluid/control/fault behavior; alarm/human minimums; privacy/security/audit; interoperability; electrical/biocompatibility/cleaning; availability/recovery; regulatory; and feasible operations.

For feasible alternatives build raw evidence on clinical outcome/error risk profiles, resilience/common cause, nurse/pharmacy/biomedical workload/usability, lifecycle cost/resource, maintainability/calibration/cleaning, deployment/update/migration, interoperability/evolvability, cybersecurity/privacy, supplier/obsolescence, and environmental effects. Use hazard analysis, bench/integration/human tests, operational data, reliability/maintenance/cost/schedule models, supplier evidence, and uncertainty with exact configurations/provenance.

Define fixed clinical/policy/lifecycle anchors and nonlinear/threshold functions. Elicit swing weights only for compensatory enhancing ranges; show affected-group profiles and distributional effects before legitimate aggregation. Model interactions such as network state × control allocation, or use scenario/Pareto/noncompensatory rules. Propagate common-cause, adoption, workload, cost, schedule, supplier, cyber, and migration uncertainty; inspect dominance, score contributions, break-even, rank reversal, multi-way sensitivity, and information value.

Independent clinical, safety, security/privacy, human-factors, biomedical, systems, and decision-method reviewers examine evidence and governance. Report feasible profiles, totals only where justified, uncertainty/sensitivity, close alternatives, residual risks, transition/rollback, dissent, and evidence gaps. Preserve analyst recommendation separately from authority decision/rationale/conditions. Baseline every artifact and reopen for changed clinical requirements, regulations, supplier/service behavior, evidence, configuration, cost/schedule, incident, or stakeholder values. The matrix cannot itself prove clinical safety, regulatory compliance, cybersecurity, equitable usability, or patient benefit.
