---
module_id: SYSENG-041
program: Systems Engineering
level: 1
module_number: 41
title: Decision Criteria and Utility
status: complete
last_verified: 2026-08-31
---

# Decision Criteria and Utility

## One-Page Review

### Governing question

How can decision objectives be translated into measurable criteria and explicit preference functions so alternatives are compared without hiding mandatory constraints, double counting, arbitrary normalization, stakeholder conflict, or uncertainty behind one score?

### Essential definitions

- A **decision frame** states the decision, authority, system/lifecycle context, objectives, alternatives, constraints, timing, stakeholders, evidence, uncertainty, and consequences.
- An **objective** is a desired direction or outcome such as improve mission availability or reduce lifecycle burden.
- A **criterion** is a property used to evaluate alternatives. A good criterion is relevant, operationally defined, discriminating, nonredundant enough for the method, and supported by evidence.
- A **measure/attribute** is the observed or predicted quantity used for a criterion, including unit, direction, reference conditions, and uncertainty.
- A **mandatory criterion/constraint** defines feasibility or prohibition. Failure normally removes or redesigns an alternative rather than being offset by strengths elsewhere.
- An **enhancing criterion** differentiates feasible alternatives by preference.
- A **value function** maps a certain outcome on one attribute to a preference scale. A **utility function** incorporates preference over uncertain outcomes; engineering practice often uses the words loosely, so declare the convention.
- A **single-attribute value function** (u_i(x_i)) maps attribute outcome (x_i) to a dimensionless preference under defined anchors and shape.
- A **weight** represents the importance of moving across the specified value range of a criterion in the chosen aggregation model; it is not a context-free importance percentage.
- **Preferential independence** is a condition under which tradeoffs among one set of attributes do not depend on fixed levels of others; additive models require strong independence assumptions.
- **Dominance** means one alternative is no worse on all valued criteria and better on at least one, with feasibility and uncertainty treated consistently.
- **Sensitivity analysis** varies weights, value functions, performance estimates, constraints, and assumptions to see whether the recommendation changes.
- A **robust recommendation** remains preferred across credible uncertainty/preferences or has explicit triggers for reopening the decision.

### Central model, mechanism, or theorem

For feasible alternative (a), certain attribute outcomes (x_i(a)), single-attribute value functions (u_i\in[0,1]), and normalized swing weights (w_i\ge0,\sum_i w_i=1), an additive model is:

$$
V(a)=\sum_{i=1}^{n}w_i u_i(x_i(a)).
$$

This model is legitimate only when criteria/scales and independence assumptions support additive compensation. A mandatory-feasibility predicate is evaluated first:

$$
Feasible(a)=\bigwedge_{j\in M}g_j(a).
$$

Under uncertainty with states (\omega) and defensible probabilities:

$$
EU(a)=\sum_{\omega}P(\omega\mid a)\,U(x(a,\omega)).
$$

Expected utility differs from applying value to an expected outcome:

$$
E[U(X)]\ne U(E[X])
$$

for nonlinear (U). Neither expression should be used when probabilities, consequences, or preference assumptions are unsupported.

### Critical invariants

- Decision, authority, context, scope, lifecycle, alternatives, stakeholders, time, and consequences are explicit before criteria are scored.
- Objectives and criteria trace to stakeholder outcomes, requirements, measures, risks, and lifecycle effects.
- Mandatory constraints are screened visibly and cannot be compensated by enhancing scores without authorized reframing.
- Every measure states unit, direction, observation/reference conditions, range, uncertainty, data/model source, and applicability.
- Value/utility functions state anchors, shape, thresholds, saturation, discontinuities, and eliciting authority.
- Weights refer to specified swings on specified value scales; changing an anchor/range requires weight reconsideration.
- Criteria do not knowingly double count the same outcome, causal chain, cost, or risk; dependencies are modeled or limitations declared.
- Additive aggregation is used only with an explicit preference-independence rationale; noncompensatory or interactive preferences use another method.
- Evidence truth and stakeholder preference remain separate: analysis estimates outcomes; authorized decision makers own value judgments.
- Uncertainty, correlation, scenario dependence, model error, and evidence limitations are propagated or shown, not replaced by point scores.
- Dominated/infeasible alternatives are handled transparently; considered and pruned alternatives and rationale remain in the record.
- Sensitivity includes weights, value-function shape, performance estimates, constraints, scenarios, and structural assumptions.
- Recommendation, analyst result, and final authority decision remain distinguishable, especially when the selected alternative is not top-scoring.
- Changes to objectives, criteria, alternatives, evidence, constraints, or preferences trigger controlled reassessment.

### Common failures

Common failures include choosing criteria after seeing which alternative wins; copying a generic criteria list; mixing objectives, means, constraints, risks, and costs in one flat table; scoring nonmeasurable labels; normalizing the current best and worst alternatives to 1 and 0 so adding an option changes prior preferences; using linear value for threshold or saturation behavior; treating weights as independent importance votes; assigning equal weights without examining swings; double counting reliability, availability, downtime, and mission success; using a compensatory score for safety/legal constraints; multiplying ordinal scores; averaging across stakeholders without authority; hiding missing data behind midpoint scores; comparing expected values under nonlinear preferences; ignoring correlation and common cause; reporting several decimal places from subjective inputs; selecting the highest total without dominance, uncertainty, or sensitivity review; and rewriting criteria to justify a preselected answer.

### Compact example

Two feasible cooling alternatives are compared on installed mass (40–80 kg) and lifecycle energy (100–300 MWh), with lower better. Linear value functions use fixed decision-relevant anchors: (u_m=(80-m)/40) and (u_e=(300-e)/200). Alternative A has 50 kg and 240 MWh: values 0.75 and 0.30. Alternative B has 65 kg and 140 MWh: values 0.375 and 0.80. With swing weights 0.4 mass and 0.6 energy, (V_A=0.48) and (V_B=0.63). The ranking is conditional on linear functions, anchors, weights, estimates, feasibility, and additive independence; it is not a physical proof that B is “63% good.”

### Connections

SYSENG-029 compares architecture alternatives; SYSENG-035–040 create integration and configuration evidence that updates outcomes and risks. This module defines decision criteria and preference modeling; SYSENG-042 applies weighted trade studies; SYSENG-043 integrates cost, schedule, performance, and risk; SYSENG-044–050 deepen uncertainty, risk, decisions, and technical reviews. Requirements, measures, ConOps, human factors, sustainability, safety, security, suppliers, operations, and lifecycle cost supply objectives and evidence.

## Governing Question

Which outcomes distinguish the alternatives, how much are different outcome levels preferred, which conditions are nonnegotiable, whose preferences govern, and how stable is the recommendation to uncertainty and reasonable changes in judgment?

The analyst's job is not to turn judgment into apparently objective decimals. It is to make the structure of judgment inspectable: objectives, measures, evidence, functions, weights, constraints, uncertainty, sensitivity, and limits. The decision authority remains responsible for the choice.

## Why This Matters

Engineering decisions combine quantities that cannot be added directly: latency, mass, cost, schedule, safety, reliability, workload, emissions, maintainability, and supplier risk. A decision model can clarify tradeoffs, expose missing evidence, and test robustness. It can also launder bias if scales and weights are arbitrary or if one score hides constraints and disagreement.

NASA's current Decision Analysis guidance begins with the decision context, criteria, and alternatives; calls for objective, measurable, discriminating criteria; distinguishes mandatory and enhancing criteria; and requires assumptions, uncertainty, sensitivity, recommendation, final decision, and rationale in the record. It notes that uncertainty matters to a ranking when reducing it could credibly change the selection. NASA Design Solution Definition guidance recommends open, inclusive trade studies covering performance, lifecycle cost, schedule, risk, maturity, and subjective factors.

NASA risk-informed decision guidance treats analysis as input to a deliberative decision rather than an automatic selector. That distinction matters because utility reflects preferences, not natural law. Analysts can estimate fuel use or failure probability; authorized stakeholders decide the relative value of outcomes, acceptable constraints, risk tolerance, and distributional effects.

Single-number aggregation is useful only when its assumptions fit. A linear scale implies every equal physical increment has equal preference value. An additive model implies compensation and independence. Expected utility requires meaningful probabilities and preference over uncertain consequences. When these assumptions fail, use thresholds, outranking, Pareto sets, scenario tables, lexicographic rules, or direct deliberation and preserve the multi-dimensional profile.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. system/mission context, decision authority, stakeholder outcomes, ConOps, lifecycle, boundary, alternatives, schedule, and reversibility;
2. requirements/constraints, measures of effectiveness/performance, budgets/margins, costs, risks, hazards, human/environmental effects, and verification evidence;
3. distinction among objectives, criteria, attributes, alternatives, constraints, assumptions, uncertainties, preferences, and evidence;
4. basic functions, units, normalization, probability, expected value, nonlinear utility, dominance, correlation, and sensitivity;
5. data/model provenance, uncertainty ranges/distributions, scenario applicability, confidence, and evidence limitations;
6. stakeholder roles, affected groups, preference/decision authority, dissent, conflicts of interest, and governance;
7. change/configuration control and decision records so results remain reproducible when inputs change.

As a retrieval test, inspect “Choose the safest and cheapest design.” Ask which hazards and affected people, safety measure and conditions, mandatory safety thresholds, lifecycle costs and price basis, uncertainty/tails, risk transfer, time horizon, distributional effects, and authority apply. Safety is not one universal scalar, and cheap acquisition can increase operation, maintenance, disposal, or consequence cost.

## Learning Objectives

After completing this module, you should be able to:

1. frame a decision with objectives, alternatives, constraints, authority, evidence, uncertainty, and timing;
2. build an objective hierarchy and operational, discriminating criteria without double counting;
3. distinguish physical measurement, normalization, value, utility, weight, and aggregate score;
4. construct and critique linear, piecewise, threshold, saturating, and nonlinear single-attribute value functions;
5. elicit swing weights that refer to explicit ranges rather than context-free importance;
6. assess feasibility, dominance, compensation, and preferential-independence assumptions;
7. evaluate alternatives with a bounded additive value model and expected utility when warranted;
8. propagate uncertainty and run sensitivity on performance, functions, weights, constraints, and scenarios;
9. represent stakeholder conflict, noncompensatory values, and distributional effects without averaging them away;
10. document recommendation, final decision, rationale, limitations, dissent, and reopening triggers.

## Core Exposition

**Frame the decision before modeling it.** Record decision ID/question, authority, system/lifecycle scope, affected stakeholders, objectives, constraints, candidate actions including status quo where meaningful, decision deadline, reversibility, downstream commitments, evidence, and required record. A model cannot repair an ambiguous decision.

**Separate analysis and authority.** Technical teams characterize alternatives and uncertainty. Stakeholders provide needs and perspectives. Decision analysts structure preferences and methods. The decision authority owns tradeoffs and selection within delegated scope. Record conflicts and dissent; do not let spreadsheet authors become implicit value authorities.

**Build a means–ends objective hierarchy.** Begin with fundamental ends—what matters in the decision—then distinguish means objectives that help achieve them. For example, redundant pumps may be a means to availability, not a separate outcome deserving weight alongside availability unless it has independent value. Ask “why is this important?” upward and “how achieved?” downward.

**Derive criteria from objectives.** Each criterion should trace to an objective, be defined for all alternatives, have meaningful direction/range, discriminate, and be measurable or estimable at decision time. Include lifecycle, human, safety, security, environmental, supplier, operations, and enabling-system effects where relevant.

**Screen mandatory constraints first.** Define requirement, applicability, evidence, uncertainty allowance, and authority. An infeasible alternative may be rejected, redesigned, or retained only as a clearly labeled reference. Do not award a high score elsewhere to compensate for an unwaivable constraint.

**Avoid criteria overlap.** Draw causal maps. Reliability affects downtime and availability, which affects mission outcome and cost. Weighting all four can count the same benefit repeatedly. Either model the chain explicitly, choose the decision-relevant endpoint, or define nonoverlapping contributions and test sensitivity.

**Define attributes operationally.** State unit, event/plane, population, time horizon, environment, modes/configurations, inclusions/exclusions, direction, source/model, uncertainty, and update event. “Maintainability: 8/10” is not a measure until the scale has repeatable observable meaning.

**Use natural and constructed measures carefully.** Natural measures include kg, seconds, currency, energy, failures/hour. Constructed scales may be necessary for usability, maturity, or flexibility. Each level needs observable anchors and scoring rules. Ordinal levels support ordering, not arbitrary addition or ratios.

**Choose fixed decision-relevant anchors.** Define worst and best/reference outcomes from stakeholder meaning, constraints, or credible ranges—not automatically from the alternatives currently in the table. Alternative-dependent min–max normalization changes existing values when a new option appears and can distort preferences.

**Elicit single-attribute value shape.** Ask whether equal physical increments have equal value. Common patterns include linear, diminishing returns, increasing urgency near a limit, threshold/step, target with penalties on both sides, and saturation. Use piecewise functions where policy or physics has breakpoints. Review continuity and boundary behavior.

**Distinguish value from utility under risk.** Value over certain consequences ranks deterministic outcomes. Utility over uncertain outcomes represents risk attitude and enables expected utility under axioms and meaningful probabilities. Many engineering matrices call normalized value `utility`; declare the convention to prevent false risk conclusions.

**Interpret weights as swings.** Compare the value of moving criterion (i) from its worst anchor to best while other criteria remain at a reference. A 0.4 weight means that defined swing contributes 40% of the aggregate range under the model—not that the criterion is universally 40% important. If the range changes, repeat or adjust elicitation.

**Test independence and compensation.** Ask whether preference for a latency improvement depends on reliability, or whether cost can compensate for safety. If tradeoffs change by levels, additive independence fails. Use interaction terms, multiplicative/multiattribute utility, conditional models, outranking, constraints, or scenario-specific deliberation.

**Evaluate dominance before aggregation.** If one feasible alternative is no worse on every criterion and better on one under consistent uncertainty, investigate why another would be selected. Dominance can reveal data/scale errors. With overlapping uncertainty, use probabilistic/interval dominance cautiously.

**Populate performance before preference where possible.** Maintain a matrix of physical/operational outcomes with evidence and uncertainty, then apply value functions. This keeps model predictions distinct from preferences and allows future authorities to reassess without rewriting evidence.

**Aggregate transparently.** For an additive model, publish formulas, values, weights, rounding, missing-data treatment, assumptions, and calculation code/spreadsheet version. Do not hide raw measures behind colored cells. Retain criterion-level profiles with totals.

**Treat missing evidence as missing.** Do not insert neutral scores automatically. Use intervals/scenarios, seek information, exclude from aggregation with disclosed limitation, or delay/reframe. An arbitrary midpoint can decide a close ranking while appearing harmless.

**Represent uncertainty.** Use ranges, distributions, scenarios, confidence bounds, evidence grades, or qualitative limitations appropriate to knowledge. Propagate through value functions. Preserve correlation: cost, schedule, mass, performance, and reliability errors often share drivers.

**Use expected utility only when warranted.** Define states, probabilities conditional on alternative, consequence vectors, utility, and risk attitude. Rare catastrophic or prohibited outcomes may require constraints or risk profiles beyond expectation. Compare (E[U(X)]) rather than (U(E[X])) under nonlinear utility.

**Analyze sensitivity structurally.** Vary one and multiple weights, anchors, shapes, performance estimates, probabilities, correlations, constraints, scenarios, discount rates, horizons, and alternative definitions. Identify break-even values and rank reversals. Sensitivity to an arbitrary modeling choice is a warning, not a nuisance.

**Consider value of information.** If uncertainty can change the decision, estimate which evidence would discriminate alternatives, cost/time of obtaining it, deadline, and consequence of waiting. Additional analysis has value only if it can improve the decision enough within constraints.

**Represent stakeholder differences.** Show separate value profiles for affected groups before aggregating. Aggregation requires legitimate governance and may need equity, rights, minimum protections, or distributional constraints. A majority average cannot erase severe burden on a subgroup.

**Use noncompensatory rules where appropriate.** Lexicographic order, satisficing thresholds, veto/out-ranking, robust feasibility, and Pareto presentation can fit decisions with rights, safety, or strategic minimums. Hybrid methods often screen constraints, show Pareto tradeoffs, then use bounded aggregation.

**Challenge gaming and bias.** Freeze criteria/method governance before final results when possible; disclose sponsors/conflicts; blind identities where useful; invite independent review; test alternate plausible models; retain rejected alternatives; and prevent selective evidence/precision from favoring a preferred option.

**Recommend with limits.** State feasible/dominated alternatives, criterion profiles, ranking, uncertainty, sensitivity, key assumptions, tradeoffs, stakeholder impacts, evidence gaps, and value-of-information options. A close or unstable result should yield conditional recommendation or more evidence, not invented decimals.

**Record final decision separately.** The authority may choose differently due to information outside the model, changed values, portfolio constraints, or accountability. Record decision, rationale, accepted consequences/risks, dissent, conditions, configuration, implementation, monitoring, and reopening triggers. If the model contradicts sound judgment, inspect the model rather than silently overriding it.

**State evidence limits.** A utility score is conditional preference synthesis. It does not measure objective goodness, moral worth, probability of success, requirement compliance, or percentage completion. Mathematical consistency cannot prove criteria complete, predictions correct, preferences legitimate, or stakeholders treated fairly.

The following checker computes a small additive model whose assumptions remain unverified.

<!-- bijux-verify: {"id":"additive-value-model-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"weights_sum=1.000\nscore_A=0.705\nscore_B=0.720\nscore_C=0.700\nranking=B,A,C\nmargin_B_over_A=0.015\nevidence=declared_values_only\n","stderr":""}} -->
```python
weights = {"reliability": 0.40, "latency": 0.35, "lifecycle": 0.25}
values = {
    "A": {"reliability": 0.80, "latency": 0.60, "lifecycle": 0.70},
    "B": {"reliability": 0.70, "latency": 0.90, "lifecycle": 0.50},
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
print(f"margin_B_over_A={scores['B'] - scores['A']:.3f}")
print("evidence=declared_values_only")
```

The 0.015 lead is smaller than many plausible elicitation and performance uncertainties. The checker proves arithmetic only; it does not validate feasibility, values, weights, independence, evidence, or selection.

## Definitions and Notation

Let alternatives be (A), mandatory constraints (M), enhancing criteria (C), attribute vector (x(a)), uncertain state (\omega), evidence (E), and decision authority (d).

Feasible set:

$$
A_F=\{a\in A:\forall m\in M,\ g_m(a)=true\}.
$$

Single-attribute value:

$$
u_i:X_i\rightarrow[0,1],
$$

with fixed anchor semantics. Additive value:

$$
V(a)=\sum_iw_i u_i(x_i(a)),\quad w_i\ge0,\quad\sum_iw_i=1.
$$

Dominance for higher-is-better values:

$$
a\succeq_D b\iff \forall i:u_i(x_i(a))\ge u_i(x_i(b))
\land\exists j:u_j(x_j(a))>u_j(x_j(b)).
$$

Under state uncertainty:

$$
EU(a)=\sum_{\omega\in\Omega}P(\omega\mid a)U(x(a,\omega)).
$$

Sensitivity region for alternative (a):

$$
\mathcal R_a=\{\theta:Score(a;\theta)\ge Score(b;\theta),\forall b\in A_F\},
$$

where (\theta) contains weights, functions, estimates, probabilities, constraints, and scenarios. Mapping (\mathcal R_a) is often more useful than one nominal rank.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—decision framing.** Define authority, ends, constraints, alternatives, context, uncertainty, timing, evidence, affected groups, and decision/implementation records.

**Mechanism 2—objective/criterion design.** Build means–ends hierarchy, trace fundamental objectives, select operational measures, check completeness, discrimination, overlap, independence, and feasibility.

**Mechanism 3—preference elicitation.** Set fixed anchors, elicit function shape and swing weights, test consistency/independence, represent stakeholder variation, and choose compensatory/noncompensatory rules.

**Mechanism 4—evidence modeling.** Estimate every alternative/criterion under exact scenarios/configurations with provenance, uncertainty, dependence, and limitations; keep physical outcomes separate from preference values.

**Mechanism 5—evaluation/challenge.** Screen constraints, inspect dominance, calculate profiles/totals, propagate uncertainty, run sensitivity/break-even/alternate-model tests, and identify valuable new evidence.

**Mechanism 6—decision/control.** Recommend with limits, record authority choice/rationale/dissent, implement/monitor, and reopen on triggers.

The integrity argument requires that criteria represent the decision, measures and predictions are credible, preference mappings are authorized and internally consistent, aggregation assumptions fit, uncertainty/sensitivity are visible, and the final decision is not confused with model output. No score proves these premises.

## Alternatives and Trade-Offs

**Direct deliberation** is transparent for few clear attributes. **Formal MCDA** improves consistency for complex profiles but adds elicitation/model risk. Use the least machinery that clarifies rather than obscures.

**Additive value models** are simple and auditable. **Multiplicative/interaction models** represent dependencies but are harder to elicit. **Outranking/Pareto methods** preserve incomparability and vetoes but may not yield one rank.

**Natural measures** retain physical meaning. **Constructed scales** cover qualitative outcomes but need careful operational anchors and ordinal discipline.

**Point estimates** are easy to communicate. **Intervals/distributions/scenarios** expose uncertainty but require more data and deliberation. Never trade honest uncertainty for decimal appearance.

**One authority preference model** produces a clear decision basis. **Multiple stakeholder profiles** expose conflicts and distributional effects. Legitimate governance, not arithmetic convenience, determines aggregation.

**Expected utility** handles risk attitude under probabilistic conditions. **Robust/satisficing methods** suit deep uncertainty or mandatory resilience. Match the method to knowledge and consequence.

## Failure Modes and Misconceptions

**“Utility is normalized performance.”** A normalized measure becomes value only through an explicit preference interpretation; utility under uncertainty is stricter still.

**“Weights are importance percentages.”** They depend on criterion scale and swing. A criterion with narrow anchors may receive different weight than the same concept with broad anchors.

**“Equal weights are neutral.”** They encode equal value for specified swings and can be highly consequential.

**“The highest score is objectively best.”** It is highest under the model's evidence and preferences. Feasibility, uncertainty, sensitivity, and authority still govern.

**“More criteria make the analysis complete.”** Redundant and weak criteria dilute meaning and invite double counting.

**“Safety can be weighted heavily.”** If a minimum is mandatory, weighting still permits compensation. Screen it as a constraint or veto.

**“Min–max normalization is harmless.”** Alternative-dependent anchors make values/rankings change when options are added.

**“Expected outcome is enough.”** Nonlinearity, tails, risk attitude, common cause, and prohibited consequences matter.

**“Stakeholder averages are fair.”** They can hide concentrated harm, rights, authority differences, or unrepresented groups.

**“Sensitivity means changing one weight.”** Structural choices, functions, estimates, correlation, constraints, scenarios, and alternatives also drive results.

## Worked Examples

### Example 1

**Fixed-anchor linear value.** Lower latency is better between 100 ms (value 1) and 500 ms (value 0):

$$
u(L)=\frac{500-L}{400}.
$$

At 220 ms, (u=280/400=0.70). At 80 ms, cap or redefine behavior rather than report 1.05 automatically. Anchors express preference range, not physical impossibility.

### Example 2

**Threshold safety constraint.** Alternatives must keep peak surface temperature below 60 °C under configuration K and fault F. A design predicting 62 °C is infeasible under the current evidence; excellent cost and mass cannot compensate. Uncertainty near 60 °C needs margin/evidence, not a nearly-full safety score.

### Example 3

**Diminishing value.** Availability improvement from 0.90 to 0.99 may matter more than from 0.99 to 0.999 for one low-consequence service, while the reverse may hold for a critical mission. Elicit operational consequence and use a nonlinear/piecewise function. Do not copy `nines` into a universal linear scale.

### Example 4

**Double counting.** A matrix weights reliability 0.25, availability 0.25, downtime 0.20, mission success 0.20, and cost 0.10. Reliability drives the next three through repair and mission models.

Build the causal chain and use fundamental mission availability/outcome plus independent maintenance/cost effects, or explicitly model interactions. Five labels do not represent five independent benefits.

### Example 5

**Swing weight reversal.** Two criteria have weights 0.6/0.4. A scores values 0.8/0.3: (V_A=0.60). B scores 0.5/0.9: (V_B=0.66). If the first weight rises to 0.7 and second falls to 0.3, (V_A=0.65), (V_B=0.62); ranking reverses. Report the break-even and why weights might vary.

### Example 6

**Expected utility differs from utility of expectation.** Outcome is 0 or 100 with equal probability and (U(x)=\sqrt{x}). Then:

$$
E[U(X)]=0.5(0)+0.5(10)=5,
$$

but:

$$
U(E[X])=\sqrt{50}\approx7.071.
$$

The difference follows from nonlinearity. Whether square-root utility is legitimate requires elicitation and meaningful consequence units.

### Example 7

**Dominated alternative.** Feasible A has cost 10, latency 50, and availability 0.99; B has cost 12, latency 60, availability 0.98, with lower cost/latency and higher availability preferred and comparable uncertainty. B is dominated. If B remains recommended, search for an omitted objective, data error, or false comparability.

### Example 8

**Missing evidence interval.** Supplier C's lifecycle cost is estimated 8–20 while A is 11–13. A midpoint of 14 makes C look worse but hides possible dominance. Propagate the interval, find the cost break-even, and decide whether supplier evidence has value before commitment.

### Example 9

**Stakeholder conflict.** Operators prefer low workload and rapid recovery; acquisition prefers low upfront cost; maintainers prefer access/standard parts; affected communities prioritize noise/environment. Show separate profiles and minimum protections. An average weight set needs explicit legitimate authority and cannot erase a veto or regulatory constraint.

### Example 10

**Decision differs from rank.** Alternative A scores 0.74 and B 0.72, but A depends on an unresolved export license with a decision deadline after design commitment. The authority selects B.

The record does not quietly alter A's score. It states model result, missing criterion/constraint or changed context, authority rationale, accepted tradeoffs, and whether criteria/model should be revised for future decisions.

## Cross-Program Connections

**Platform engineering.** Platform choices trade developer experience, reliability, security, cost, portability, operability, lock-in, and migration; raw SLO and workload evidence should remain separate from preference.

**API and service engineering.** Protocol/style, consistency, latency, availability, evolvability, security, consumer burden, and cost require constraints, scenario-specific measures, and avoidance of double counting.

**Data engineering.** Freshness, correctness, completeness, latency, cost, lineage, privacy, and replay often interact; utility cannot turn a prohibited privacy outcome into compensation.

**Object-oriented programming.** Design alternatives trade cohesion, coupling, substitutability, complexity, performance, and change cost. Code metrics need decision-relevant operational interpretations.

**Functional programming.** Purity, type guarantees, composability, performance, ecosystem, effects, and team capability are means/end mixes that benefit from an objective hierarchy.

**Risk and economics.** Expected utility, value of information, lifecycle cost, discounting, tail consequence, and risk acceptance connect preference to uncertain outcomes.

**Human and ethical considerations.** Distribution, accessibility, workload, consent, environmental burden, rights, and affected-group participation may require constraints or separate profiles.

## References

1. NASA, *Systems Engineering Handbook, Section 6.8: Decision Analysis*, current web edition. <https://www.nasa.gov/reference/6-8-decision-analysis/>
2. NASA, *Systems Engineering Handbook, Section 4.4: Design Solution Definition*, current web edition. <https://www.nasa.gov/reference/4-4-design-solution-definition/>
3. NASA, *NASA Risk-Informed Decision Making Handbook*, NASA/SP-2010-576. <https://ntrs.nasa.gov/citations/20100021361>
4. NASA, *NASA Risk Management Handbook*, NASA/SP-2011-3422. <https://ntrs.nasa.gov/citations/20120000033>
5. NASA, *Systems Engineering “Toolbox” for Design-Oriented Engineers*, NASA RP-1358. <https://ntrs.nasa.gov/citations/19950012517>
6. NASA, *Systems Engineering Handbook, Appendix B: Glossary*, current web edition. <https://www.nasa.gov/reference/appendix-b-glossary/>
7. NASA, *NPR 8000.4A: Agency Risk Management Procedural Requirements*. <https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_8000_004A_&page_name=main>
8. NASA, *NPR 8705.4B: Risk Classification for NASA Payloads*. <https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_8705_004B_&page_name=main>
9. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>
10. NIST, *Decision Support System for Material and Manufacturing Process Selection*, official publication record. <https://www.nist.gov/publications/decision-support-system-material-and-manufacturing-process-selection>

## Exercises

### Exercise 1

Lower mass is preferred with fixed anchors 40 kg (value 1) and 100 kg (value 0). Lower lifecycle energy is preferred with anchors 200 MWh (value 1) and 600 MWh (value 0). Alternative A is 55 kg/500 MWh; B is 80 kg/260 MWh. With swing weights 0.35 mass and 0.65 energy, compute values and totals. State assumptions.

### Exercise 2

Alternatives A and B have criterion values: A=(0.9,0.4), B=(0.6,0.8). Let weight on criterion 1 be (w) and criterion 2 be (1-w). Derive the break-even weight and preferred alternative on each side. Explain what elicitation question the weight must answer.

### Exercise 3

An uncertain benefit is 0 with probability 0.25 and 100 with probability 0.75. Compute expected benefit, expected utility for (U(x)=\sqrt{x}), and utility of expected benefit. Explain why they differ and what evidence is required before using the result.

### Exercise 4

Critique a trade matrix using cost, development cost, lifecycle cost, schedule, time to market, reliability, availability, downtime, safety score, and “risk” with equal weights and 1–10 expert scores. Redesign the criteria/decision method.

### Exercise 5

Frame criteria and preference treatment for choosing a hospital medication-delivery architecture among centralized smart pumps, distributed pumps with local control, and a hybrid. Include clinical outcomes, mandatory constraints, lifecycle, humans, privacy/security, interoperability, uncertainty, affected groups, and decision record.

## Answers to the Exercises

### Answer 1

Mass value:

$$
u_m(m)=\frac{100-m}{60}.
$$

Thus:

$$
u_m(A)=45/60=0.75,\qquad u_m(B)=20/60=0.3333.
$$

Energy value:

$$
u_e(e)=\frac{600-e}{400},
$$

so:

$$
u_e(A)=100/400=0.25,\qquad u_e(B)=340/400=0.85.
$$

Totals:

$$
V_A=0.35(0.75)+0.65(0.25)=0.425,
$$

$$
V_B=0.35(0.3333)+0.65(0.85)\approx0.6692.
$$

B ranks higher. Assumptions include both alternatives satisfy mandatory constraints; lower is preferred; anchors/ranges are authorized and fixed; linear value is appropriate; weights refer to those swings; additive preferential independence/compensation is acceptable; measures use consistent configurations/lifecycle boundaries; estimates are accurate enough; and uncertainty or omitted criteria do not reverse the result. The totals are conditional values, not percentages of quality.

### Answer 2

$$
V_A=0.9w+0.4(1-w)=0.4+0.5w,
$$

$$
V_B=0.6w+0.8(1-w)=0.8-0.2w.
$$

Set equal:

$$
0.4+0.5w=0.8-0.2w\Rightarrow0.7w=0.4\Rightarrow w=4/7\approx0.5714.
$$

For (w>4/7), A is preferred; for (w<4/7), B; equal at break-even. The elicitation question compares the value of moving criterion 1 from its defined worst anchor to best against the corresponding specified swing on criterion 2, under the additive model and a stated reference—not “which criterion sounds more important?” Changes to anchors or interaction require re-elicitation.

### Answer 3

Expected benefit:

$$
E[X]=0.25(0)+0.75(100)=75.
$$

Expected utility:

$$
E[U(X)]=0.25\sqrt0+0.75\sqrt{100}=7.5.
$$

Utility of expected benefit:

$$
U(E[X])=\sqrt{75}\approx8.6603.
$$

They differ because square root is nonlinear/concave; averaging before applying it is not the same as applying it before averaging. Use requires a well-defined benefit unit/domain; a legitimately elicited utility function representing the decision authority's risk preference; defensible conditional probabilities; complete consequence states including adverse/tail/distributional effects; and evidence/uncertainty/correlation. Square root chosen for convenience does not establish risk attitude.

### Answer 4

Problems include nested/double-counted cost and time criteria; reliability/availability/downtime causal overlap; `safety score` may improperly compensate a constraint; generic risk combines multiple uncertain consequences; equal weights are not neutral; 1–10 scales lack operational anchors and may be ordinal; expert evidence/preference roles are mixed; alternatives/configurations/time horizon/authority/uncertainty are absent.

Redesign by framing the decision and fundamental objectives. Screen mandatory safety, legal/regulatory, security/privacy, interoperability, and performance constraints with evidence/margin. Define lifecycle cost once with acquisition, integration, operation, maintenance, downtime/consequence, and retirement breakdown shown separately for diagnosis rather than each weighted. Define decision-relevant delivery/availability dates without duplicate market labels. Model reliability/repair into operational availability and mission/clinical outcome, retaining independent maintainability/workload effects only where distinct. Separate risk profiles by consequence and scenario; do not collapse prohibited tails.

Use natural measures and fixed value anchors/functions. Elicit swing weights from the authority after scales are defined, test preferential independence, retain criterion profiles, model uncertainty/correlation, inspect dominance/Pareto tradeoffs, and run multi-way sensitivity/break-even/value-of-information analysis. Use constraints/outranking or scenario deliberation where compensation is invalid. Document evidence, preferences, assumptions, dissent, recommendation, final decision, and reopening triggers.

### Answer 5

Frame the decision around safe and effective medication delivery over the full lifecycle, named care settings/populations, deployment scale, decision authority, regulatory/institutional obligations, alternatives/configurations, transition, reversibility, and affected patients, nurses, pharmacy, biomedical, IT/security, caregivers, and operations.

Mandatory constraints include correct patient/drug/dose/rate/order; safe control under network/service loss; occlusion/air/free-flow and hazardous failure controls; alarm and human-factors minimums; electrical/fluid/biocompatibility/cleaning requirements; clinical interoperability; privacy/security/authorization/audit; availability/recovery; regulatory/certification; and feasible facilities/staffing. Uncertain near-threshold designs require margin/evidence, not compensating score.

Fundamental enhancing criteria can include clinical error/outcome profile; resilience/recovery across nominal/degraded modes; nurse/pharmacy/biomedical workload and usability; lifecycle cost/resources; maintainability/calibration/cleaning; deployment/update/migration burden; interoperability/evolvability; supply/obsolescence; and environmental impact. Avoid double counting device reliability, availability, alarm burden, and clinical outcomes without a causal model.

Define measures by patient/care context, observation events, time horizon, mode, population, and configuration. Use human-in-the-loop evidence, hazard/risk profiles, reliability/maintenance models, cybersecurity/privacy analysis, integration tests, operational data, supplier evidence, and cost/schedule uncertainty with provenance/limitations. Present separate affected-group profiles and distributional impacts; do not average away accessibility or concentrated patient risk.

Choose value functions with clinical/policy anchors, thresholds, saturation, and asymmetry. Use swing weights only for feasible enhancing ranges and with authorized governance. Model interactions or use noncompensatory/Pareto/scenario methods where outcomes depend on network state, staffing, or centralized common cause. Analyze uncertain failure/common cause, adoption, workload, cost, schedule, supplier, cyber, and migration effects; run sensitivity and identify evidence that can change the choice before commitment.

Report feasibility, profiles, uncertainty, sensitivity, residual risks, transition/rollback, dissent, and value-of-information. Record analyst recommendation separately from the clinical/institutional authority's final decision, rationale, conditions, monitoring, configuration, and reopening triggers. A decision model supports but does not prove clinical safety, regulatory acceptance, cybersecurity, equitable usability, or patient benefit.
