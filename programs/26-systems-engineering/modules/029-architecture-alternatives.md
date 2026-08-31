---
module_id: SYSENG-029
program: Systems Engineering
level: 1
module_number: 29
title: Architecture Alternatives
status: complete
last_verified: 2026-08-31
---

# Architecture Alternatives

## One-Page Review

### Governing question

How can a team generate, characterize, compare, and select among genuinely different architecture alternatives so that stakeholder value, hard constraints, uncertainty, risk, evidence, and reversibility remain visible—without disguising preference as arithmetic or declaring the highest weighted score universally “best”?

### Essential definitions

- An **architecture alternative** is a coherent candidate organization of responsibilities, elements, interactions, allocations, qualities, and lifecycle strategies intended to satisfy the same framed need.
- A **decision frame** defines the decision, authority, scope, timing, stakeholders, objectives, constraints, assumptions, configurations, and evidence threshold.
- A **decision criterion** is an operationally defined basis for differentiating alternatives; it may be mandatory, preference-bearing, or informational.
- A **hard constraint** is a noncompensatory condition: failure makes an alternative infeasible regardless of strengths elsewhere.
- A **measure** is an observable or computed quantity used to assess a criterion under stated conditions.
- A **value model** maps measures and preferences into an evaluation structure; its shape encodes stakeholder judgments.
- A **trade space** is the set of feasible combinations of architecture decisions and resulting outcomes considered by the analysis.
- **Dominance** means one alternative is no worse on every relevant criterion and better on at least one, under the same evidence basis.
- A **Pareto frontier** contains alternatives not dominated within the examined set; it does not identify one preferred choice.
- **Uncertainty** is incomplete knowledge about models, parameters, outcomes, contexts, or preferences; **variability** is inherent variation in conditions or outcomes.
- **sensitivity analysis** tests whether plausible changes to inputs, weights, scales, assumptions, or models alter conclusions.
- A **robust decision** remains acceptable across a declared range of plausible conditions and preferences, not merely at one nominal point.
- **value of information** compares the expected decision benefit of reducing uncertainty with the cost, delay, and opportunity cost of obtaining evidence.
- A **reversal criterion** states what future evidence or condition should reopen the decision.

### Central model, mechanism, or theorem

Let alternatives be (A={a_1,\ldots,a_n}), criteria (C={c_1,\ldots,c_m}), mandatory feasibility predicates (H_j(a)), measures (x_{ij}), normalized value functions (v_j), weights (w_j), and uncertainty state (\theta). First form the feasible set:

$$
A_F=\{a\in A\mid \bigwedge_j H_j(a,\theta)=true\}.
$$

Only then may an additive value model be considered, and only when criteria are preferentially independent and scales are valid:

$$
V(a\mid\theta,w)=\sum_{j=1}^{m}w_jv_j(x_{aj}\mid\theta),
\qquad w_j\geq0,\quad\sum_jw_j=1.
$$

Selection is defensible only if framing, feasibility, common-basis evidence, model validity, uncertainty, sensitivity, stakeholder authority, and rationale are explicit. A score is decision support—not a proof, fact of nature, or substitute for accountable judgment.

### Critical invariants

- Alternatives address the same controlled need, stakeholder outcomes, system boundary, lifecycle scope, scenarios, modes, configurations, and constraints.
- Each alternative is coherent enough to expose elements, allocations, interfaces, state/authority, qualities, enabling systems, operations, support, and retirement.
- The status quo, defer/no-action option, and credible hybrids are considered where meaningful.
- Mandatory constraints are screened before compensatory scoring; safety, legality, mission success, and required independence are not traded away by convenience.
- Criteria are complete enough for the decision, nonduplicative enough to avoid hidden double counting, operationally defined, and approved by the decision authority before results are known.
- Measures use consistent units, reference conditions, time horizon, configuration, and evidence quality across alternatives.
- Normalization and value functions preserve preference meaning; arbitrary ordinal ratings are not treated as ratio-scale quantities.
- Cost, schedule, risk, performance, human factors, security, privacy, safety, resilience, operability, support, and retirement effects are included where applicable.
- Uncertainty, correlation, common causes, model-form limits, and evidence gaps remain visible rather than collapsed into point estimates.
- Sensitivity tests weights, thresholds, scales, assumptions, scenarios, and uncertain measures; close or unstable rankings are reported honestly.
- Stakeholder conflicts, dissent, distributional effects, ethical/legal limits, and decision authority are documented.
- The final decision records recommendation, selected alternative, rationale, residual risk, commitments, evidence plan, and reversal criteria.

### Common failures

Failures include comparing a mature incumbent with sketch-level challengers; generating cosmetic variants of one favored concept; excluding no-action or hybrid options; allowing late-emerging preferences to rewrite weights; treating mandatory criteria as weighted; double-counting reliability through availability, downtime, and resilience scores; normalizing against the candidate set so scores change when a weak option is added; multiplying ordinal ratings; using expected cost without tail consequences; assuming uncertain estimates are independent; hiding supplier, operator, enabling-system, migration, and retirement burdens; presenting one decimal place as precision; selecting the highest score despite overlapping uncertainty; optimizing a proxy that stakeholders do not value; ignoring who receives benefit or harm; and recording the winning slide without rejected alternatives, assumptions, or reversal conditions.

### Compact example

A regional warning system compares centralized, federated, and hybrid architectures. Hard constraints require an authorized warning within 30 seconds, operation through a 20-minute regional network partition, auditable cancellation, and jurisdictional data protection. The centralized option fails partition autonomy; it is not rescued by low operating cost. The federated option meets autonomy but has uncertain policy-consistency and staffing burden. The hybrid option uses signed policy baselines, local bounded authority, central coordination when connected, and controlled reconciliation. Common scenarios, timing/load simulations, security analysis, operator trials, migration estimates, and lifecycle costs populate measures. Weighted values favor hybrid at nominal weights, but sensitivity shows federation wins if autonomy weight rises modestly. The recommendation selects hybrid conditionally, funds a policy-reconciliation prototype, retains federation as a fallback, and defines reversal criteria based on measured update latency and operator workload.

### Connections

SYSENG-021–025 define behavior; SYSENG-026–028 define logical elements, allocations, and flows. This module compares different coherent arrangements of those decisions. SYSENG-030 checks completeness and consistency of the selected logical architecture. Later trade-study, modeling, risk, cost, verification, safety, security, human-factors, and governance modules deepen the evidence. Platform, API/service, data, object-oriented, and functional programs use the same reasoning when choosing centralization, decomposition, state ownership, protocols, processing models, and migration strategies.

## Governing Question

How can architecture alternatives be generated and evaluated on a common, evidence-bearing basis so that infeasible options are excluded, value judgments remain explicit, uncertainty is not hidden, and the accountable decision can be revisited when its assumptions change?

The answer is a controlled decision process. Frame the decision before evaluating solutions; generate structurally meaningful candidates; describe each to comparable maturity; screen hard constraints; select measurement and value models appropriate to the criteria; quantify uncertainty and correlations; test sensitivity and robustness; expose distributional effects and dissent; then record a decision whose scope and reversal conditions are explicit.

## Why This Matters

Architecture decisions shape most downstream requirements, interfaces, integration risk, supplier commitments, operations, and lifecycle cost. A weak comparison can make a preferred concept look inevitable by controlling which alternatives exist, how evidence is normalized, which uncertainties disappear, or whose values become weights. Once contracts, teams, and physical assets align around the selection, reversal becomes expensive.

NASA’s current Design Solution Definition guidance calls for creating alternatives, analyzing them through trade studies, considering technology maturity, effectiveness, cost, schedule, risk, and robustness, and retaining uncertainty. NASA’s current Decision Analysis guidance defines the decision context, criteria, alternatives, methods, evaluation, uncertainty, sensitivity, recommendation, and decision record; it also states that mandatory criteria disqualify options and that tool assumptions and limitations must be documented. SEBoK 2.14 presents analysis and selection as quantified comparison of cost, risk, and effectiveness while acknowledging trade-study limits. ISO/IEC/IEEE 15288:2023 supplies iterative lifecycle processes without prescribing one decision method. These sources support disciplined comparison; none makes a weighted matrix automatically valid.

Architecture choice is often a portfolio decision under partial knowledge. An alternative may be slightly worse nominally but safer under uncertain demand. A modular option may cost more initially but preserve future choices. A centralized option may reduce policy inconsistency but concentrate failure and trust. A decision process should show these structures, not erase them in a single score.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. stakeholder needs and operational concepts define outcomes and constraints, not a favored solution;
2. requirements have authority, applicability, rationale, and verification conditions;
3. scenarios and modes provide a common behavioral basis for comparison;
4. logical elements, allocations, and flows create performance, state, trust, failure, and lifecycle consequences;
5. end-to-end qualities require property-specific composition and evidence;
6. risk combines uncertain events, consequences, exposure, and response—not one color or score;
7. models are purposeful abstractions with calibration and applicability limits;
8. decision authority and engineering analysis are connected but distinct responsibilities.

As a retrieval test, compare `monolith` and `microservices` using only “scalability, simplicity, flexibility” rated 1–5. The exercise lacks workload, failure, state, deployment, team, regulatory, migration, and cost context; no operational definitions exist; maturity differs; values and weights are unknown; the options may not even be coherent system architectures. Arithmetic on those labels would manufacture precision rather than provide evidence.

## Learning Objectives

After completing this module, you should be able to:

1. frame an architecture decision with authority, scope, stakeholders, outcomes, constraints, assumptions, and evidence threshold;
2. generate diverse, coherent architecture alternatives rather than cosmetic variants;
3. establish comparable maturity and a common scenario/configuration basis;
4. separate mandatory feasibility screens from preference-bearing criteria;
5. define measures, scales, value functions, and weights without invalid arithmetic or hidden double counting;
6. identify dominance and Pareto-efficient candidates without claiming the frontier selects one winner;
7. represent uncertainty, variability, correlation, tail consequences, evidence quality, and model-form limits;
8. perform sensitivity, threshold, scenario, and robustness analyses;
9. assess value of information, reversibility, option value, migration, and lifecycle commitments;
10. present and govern a transparent recommendation, accountable decision, residual risks, and reversal criteria.

## Core Exposition

**Trigger and classify the decision.** State why a decision is needed now, what outcome it controls, who decides, who recommends, who supplies evidence, who is affected, and what happens if the decision is deferred. Classify consequence, reversibility, urgency, uncertainty, and required independence. Tailor rigor to consequence without skipping traceability.

**Freeze the frame before scoring.** Control the system boundary, lifecycle interval, operational environments, scenarios, modes, configurations, stakeholder outcomes, mandatory requirements, assumptions, constraints, resources, and decision date. Record permitted tailoring. Changing the frame after results appear is a decision change and must be visible.

**Separate problem and solution claims.** A constraint may genuinely limit the trade space; an inherited product choice may only appear to. Challenge whether “must use vendor X,” “must be cloud,” or “must preserve every interface” has authority and rationale. Treat current architecture as an alternative, not as the neutral baseline of nature.

**Generate alternatives by decision dimensions.** Explore responsibility partition, function allocation, state/policy ownership, control/data flows, human–automation authority, central/federated organization, active/standby redundancy, synchronous/asynchronous interaction, local/remote control, make/buy/reuse, physical distribution, deployment, support, and transition. A morphological matrix or trade tree can combine meaningful choices, but impossible or incoherent combinations need explicit pruning rationale.

**Seek structural diversity.** Strong alternatives embody different mechanisms or boundaries likely to produce different outcome profiles. Three products implementing the same architecture are acquisition alternatives, not necessarily architecture alternatives. Conversely, one product can support several architectural configurations. Preserve the distinction.

**Include status quo, no-action, defer, and hybrids.** The current system provides a baseline for incremental value and migration risk. No-action may violate future constraints but should be shown. Deferral can buy information at opportunity cost. Hybrid or staged alternatives can preserve options, though they also add coexistence and transition complexity.

**Describe each alternative coherently.** Provide scope, context, elements, responsibilities, allocations, interfaces/flows, state and authority, scenarios/modes, quality budgets, failure/trust boundaries, humans, enabling systems, operations, support, migration, retirement, dependencies, assumptions, technology maturity, and verification concept. Do not score a one-page challenger against a detailed incumbent.

**Equalize analysis maturity.** Establish a minimum evidence package and common level of abstraction. Use the same demand, environment, cost year, currency, schedule basis, mission duration, scenarios, failure assumptions, and measurement definitions. Where maturity cannot be equalized, represent the evidence-quality difference rather than giving unsupported estimates equal status.

**Identify stakeholders and concerns.** Include customers, users, operators, maintainers, acquirers, suppliers, integrators, safety/security/privacy authorities, regulators, affected communities, and retirement owners as applicable. Record conflicts and decision rights. Aggregated value can conceal that one alternative transfers risk to a less powerful group.

**Define mandatory criteria.** Derive hard constraints from authoritative requirements, law, policy, physical limits, mission thresholds, safety limits, ethical boundaries, interoperability obligations, and resource ceilings. Define pass/fail and uncertainty treatment before evaluation. An alternative whose confidence interval crosses a hard limit may require more evidence, mitigation, or rejection; a weighted strength elsewhere cannot compensate.

**Define preference criteria.** Criteria should differentiate alternatives and relate to stakeholder outcomes. Examples include effectiveness, responsiveness, resilience, adaptability, operability, human workload, maintainability, security exposure, privacy, environmental effect, acquisition flexibility, lifecycle cost, schedule, and retirement burden. Organize them in a value hierarchy to expose overlap and omissions.

**Prevent double counting.** Availability, downtime, mission continuity, and recovery may share causal evidence. Development cost, staffing, and schedule can also overlap. Draw criterion definitions and causal relationships. Either combine dependent measures, model their joint effect, or justify separate stakeholder value without counting the same benefit repeatedly.

**Operationalize measures.** State unit, direction of preference, measurement/model method, conditions, time horizon, population, configuration, uncertainty, source, and acceptance threshold. “High maintainability” becomes repair-time distribution, skills, access, diagnostic coverage, spares, and representative maintenance scenarios—not a 1–5 adjective.

**Distinguish natural and constructed scales.** Dollars, seconds, kilograms, and probabilities have defined quantitative meanings, though uncertainty remains. Ordinal categories only establish order. Do not average or multiply ordinal labels as though differences and ratios were meaningful. If converting measures to value, elicit an operational value function.

**Define value functions.** Stakeholder value is rarely linear. Reducing response from 30 to 20 seconds may matter greatly while 300 to 290 seconds may not, or vice versa. Define thresholds, saturation, diminishing returns, discontinuities, and direction. Validate the function with decision stakeholders using concrete consequence comparisons.

**Elicit weights carefully.** In an additive model, weights depend on the criterion ranges and value scales; they are not free-floating statements that “safety is 40%.” Use swing comparisons or equivalent anchored questions. Record participants, method, disagreements, and approval. Re-eliciting weights after seeing winners invites motivated reasoning.

**Check model assumptions.** Additive aggregation generally assumes preferential independence. Criteria with interactions—such as latency and availability, automation and workload, or security and usability—may need multiattribute, scenario, constraint, or simulation models. A simple matrix is appropriate only when its assumptions fit the decision.

**Screen dominance.** If one feasible alternative is no worse on all relevant measures and strictly better on at least one using comparable evidence, it is dominated and can usually be removed. Uncertainty may prevent a dominance conclusion. Document pruning so excluded options do not disappear without rationale.

**Use Pareto analysis.** Plot or calculate non-dominated candidates across key objectives. The frontier reveals trade structure and where improvements require sacrifice. It does not decide how much cost is worth a reliability improvement or whose risk matters; preferences and constraints still govern selection.

**Represent uncertainty explicitly.** Separate parameter uncertainty, model-form uncertainty, scenario uncertainty, technology maturity, cost/schedule estimate uncertainty, and preference uncertainty. Use intervals, distributions, confidence/credibility statements, qualitative evidence grades, or scenario bounds appropriate to knowledge. Do not assign distributions merely to create numerical output.

**Model correlations and common causes.** Costs, schedules, and technical performance share drivers. Redundant elements may share suppliers, environments, software, data, or power. Treating uncertain variables as independent can understate tails. Record dependence assumptions and test plausible correlation structures.

**Analyze risk and opportunity.** Show event/condition, cause, probability or plausibility, consequence distribution, exposure, detectability where relevant, affected stakeholders, mitigation, owner, triggers, and residual risk. Expected value can hide rare catastrophic outcomes or upside. Preserve noncompensatory risk limits and authority for acceptance.

**Include lifecycle cost and schedule.** Compare development, acquisition, integration, verification, deployment, transition, infrastructure, licenses, training, operations, staffing, maintenance, updates, incident response, obsolescence, decommissioning, data migration, and disposal. State currency year, discount/escalation assumptions, quantities, demand, reserves, and estimate class. Schedule includes evidence and transition, not only construction.

**Evaluate migration and coexistence.** A target architecture is incomplete without a path from current state. Analyze data/state transfer, interfaces, dual operation, cutover, rollback, workforce, supplier, certification, and temporary safety/security exposure. Migration may dominate near-term risk even when steady-state value is attractive.

**Assess technology and evidence maturity.** Distinguish existence, demonstrated capability, scale, environment, integration, producibility, supportability, supplier viability, and assurance evidence. “Used elsewhere” is relevant only through an applicability argument. A prototype can reduce one uncertainty while leaving lifecycle or scale risks open.

**Run common scenarios.** Exercise the same normal, peak, degraded, emergency, maintenance, update, recovery, attack, transition, and retirement scenarios. Measure stakeholder outcomes, not only component properties. Keep environmental and demand assumptions controlled; report where an alternative changes the operational concept.

**Perform sensitivity analysis.** Vary weights, value functions, thresholds, uncertain measures, correlations, scenarios, demand, cost, schedule, and model choices across plausible ranges. Find break-even points and ranking reversals. One-at-a-time variation is easy but can miss interactions; use joint scenarios or sampling where justified.

**Assess robustness.** Ask whether each alternative remains feasible and acceptably valuable across plausible futures, not whether it has the highest nominal score. Minimax regret, satisficing, scenario coverage, safety margins, adaptive pathways, or probabilistic dominance may be useful. Name the robustness definition and stakeholder preference it embodies.

**Calculate value of information selectively.** Identify uncertainties capable of changing the decision. Estimate how additional prototype, test, survey, analysis, or market evidence could change actions and outcomes. Compare expected benefit with evidence cost, schedule delay, and lost opportunity. Do not delay merely because uncertainty exists; some uncertainty is irreducible or decision-irrelevant.

**Consider reversibility and option value.** A modular interface, staged commitment, pilot, lease, or dual-source strategy may preserve future choices. Option value is not free: interfaces, parallel capability, and delay cost resources. Record what is reversible, by when, at what cost, and which signals trigger adaptation.

**Use independent challenge.** Include domain, operations, integration, cost, schedule, human-factors, safety, security, privacy, reliability, test, supplier, and affected-stakeholder competence appropriate to consequence. Have reviewers search for missing alternatives, frame bias, inconsistent maturity, optimistic assumptions, hidden constraints, double counting, and evidence asymmetry.

**Make the recommendation transparent.** Show feasible set, measures, uncertainties, sensitivity, Pareto structure, risk, dissent, unresolved evidence, and why the recommended alternative best fits authorized preferences. If alternatives are practically tied or ranking is unstable, say so and recommend evidence collection, staged commitment, or a decision among the tied set.

**Separate recommendation from decision.** Analysts characterize and recommend; the named authority decides and accepts residual commitments within its authority. If the authority selects a lower-scoring or nonrecommended alternative, capture the legitimate rationale and revisit whether the value model omitted a criterion. Do not manipulate weights retrospectively to make the decision appear mathematically inevitable.

**Baseline and revisit.** Record the decision frame, alternatives, pruning, evidence versions, criteria, measures, normalization, value functions, weights, models, uncertainty, sensitivity, recommendation, decision, dissent, residual risks, commitments, and reversal criteria. Monitor assumptions. Reopen when thresholds are crossed, not whenever someone dislikes the outcome.

The following checker finds selected declaration defects in five architecture-alternative records. It cannot judge feasibility, preference validity, or decision quality.

<!-- bijux-verify: {"id":"architecture-alternative-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"alternatives_total=5\nwell_formed_declared=1\nmissing_scope=ALT-002\nmissing_assumptions=ALT-003\nmissing_evidence=ALT-004\nmissing_migration=ALT-005\nunresolved=ALT-002,ALT-003,ALT-004,ALT-005\nevidence=declared_fields_only\n","stderr":""}} -->
```python
alternatives = [
    {"id": "ALT-001", "scope": "regional warning architecture",
     "assumptions": ["signed policy available"], "evidence": ["partition simulation"],
     "migration": "pilot two regions then controlled cutover"},
    {"id": "ALT-002", "scope": "", "assumptions": ["central connectivity"],
     "evidence": ["load model"], "migration": "retain current integration"},
    {"id": "ALT-003", "scope": "federated warning", "assumptions": [],
     "evidence": ["operator trial"], "migration": "train and deploy local authorities"},
    {"id": "ALT-004", "scope": "hybrid warning", "assumptions": ["local autonomy"],
     "evidence": [], "migration": "dual run and reconcile"},
    {"id": "ALT-005", "scope": "defer decision", "assumptions": ["legacy support"],
     "evidence": ["support forecast"], "migration": ""},
]
required = ("scope", "assumptions", "evidence", "migration")
valid = [item for item in alternatives if all(item[field] for field in required)]
print(f"alternatives_total={len(alternatives)}")
print(f"well_formed_declared={len(valid)}")
for field in required:
    print(f"missing_{field}=" + ",".join(item["id"] for item in alternatives if not item[field]))
print("unresolved=" + ",".join(item["id"] for item in alternatives if item not in valid))
print("evidence=declared_fields_only")
```

ALT-001 may still be unacceptable: nonempty declarations do not establish common-basis feasibility, complete lifecycle effects, valid preferences, or real partition performance.

## Definitions and Notation

Let (A) be candidates, (H) mandatory constraints, (C) preference criteria, (X) measures, (V) value functions, (W) weights, (S) scenarios, and (\Theta) uncertain states. Keep natural measures, stakeholder values, evidence quality, and decision authority distinct.

Alternative (a) dominates (b) for benefit-oriented criteria when:

$$
(\forall j,\ x_{aj}\geq x_{bj})\land(\exists k,\ x_{ak}>x_{bk}),
$$

after directions, uncertainty, and comparability are handled. A Pareto set contains alternatives for which no examined alternative establishes that relation.

For a nominal additive example with value scores (v_j\in[0,100]):

$$
V(a)=0.35v_{effectiveness}+0.25v_{resilience}+0.20v_{operability}
+0.20v_{lifecycle\ cost}.
$$

Weights have meaning only with those defined ranges and value functions. A score difference is not meaningful without uncertainty and sensitivity.

Expected value of perfect information can be represented as:

$$
EVPI=E_{\theta}[\max_a U(a,\theta)]-\max_a E_{\theta}[U(a,\theta)],
$$

but its validity depends on probability and utility models. Practical value of a specific imperfect study is lower and must be compared with its full cost and delay.

## Mechanisms, Invariants, or Proof Structure

Use an architecture-decision assurance loop:

1. **Frame:** define decision, authority, scope, outcomes, constraints, stakeholders, assumptions, urgency, reversibility, and evidence threshold.
2. **Generate:** explore meaningful architecture dimensions; retain status quo, no-action/defer, hybrids, and pruning rationale.
3. **Characterize:** bring candidates to comparable maturity across structure, behavior, qualities, humans, lifecycle, migration, and evidence.
4. **Measure and screen:** operationalize criteria, enforce hard constraints, assess evidence quality, and remove only justified dominated/infeasible candidates.
5. **Value and analyze:** apply valid value/risk/cost models; represent uncertainty/correlation; run common scenarios, sensitivity, thresholds, robustness, and value-of-information analysis.
6. **Challenge and decide:** expose dissent and distributional effects; independently review; recommend transparently; record the accountable decision and residual commitments.
7. **Govern:** baseline inputs/models/evidence, monitor assumptions, preserve alternatives, and reopen only under controlled reversal criteria.

The conclusion is conditional: given the framed need, authorized preferences, feasible candidate set, current evidence, and declared uncertainty, one alternative is recommended. It is not a universal ranking or proof that unexamined architectures are inferior.

## Alternatives and Trade-Offs

**Qualitative deliberation versus formal value model.** Structured expert/stakeholder deliberation can address nuance and limited data but risks undocumented bias. Formal models improve traceability and sensitivity but can encode false precision. Consequence and available evidence determine the blend.

**Additive value versus outranking or constraints.** Additive models support compensatory preferences under independence assumptions. Outranking can represent vetoes and incomparability. Constraint/satisficing approaches select any acceptable option. Choose the method from preference structure, not tool availability.

**Expected value versus robust/safety-first choice.** Expected value uses probabilities and utilities but may hide tails. Robust approaches protect across plausible states but can be conservative and encode regret preferences. Safety/legal constraints remain separate.

**Commit now versus gather information.** Immediate commitment avoids delay and captures opportunity; additional evidence may prevent costly error. Value-of-information analysis targets uncertainty that could change the choice.

**Single target versus staged/adaptive pathway.** A single target can simplify delivery and assurance. Staging preserves options and learning but adds transition, coexistence, and governance complexity.

**Optimize steady state versus transition.** A superior steady-state architecture may impose unacceptable migration risk. Incremental alternatives can deliver lower ultimate value but better continuity, reversibility, and learning.

**Best nominal versus most robust.** Nominal optimization can excel in the forecast center. Robust designs may sacrifice peak value to remain acceptable across demand, technology, supplier, policy, or threat futures.

## Failure Modes and Misconceptions

- **Favored-solution framing:** constraints and alternatives are written around one concept. Revalidate authority and generate dimensions independently.
- **Cosmetic alternatives:** products or diagrams vary while architecture mechanisms do not. Seek structural differences.
- **Unequal maturity:** incumbent evidence is compared with challenger aspiration. Apply a common evidence package or model maturity explicitly.
- **Compensating a hard constraint:** a weighted strength offsets an infeasible safety or legal result. Screen first.
- **Ordinal arithmetic:** low/medium/high or 1–5 labels are averaged as cardinal values. Define operational scales/value functions.
- **Weight theater:** percentages are elicited without criterion ranges or changed after results. Use anchored preference elicitation and governance.
- **Double counting:** correlated criteria reward the same outcome repeatedly. Use a value hierarchy and causal review.
- **Candidate-dependent normalization:** adding/removing an option changes everyone’s value. Anchor scales to stakeholder consequences.
- **Point-estimate certainty:** uncertain cost/performance is shown as exact. Preserve ranges, distributions, evidence quality, and model limits.
- **Independent-tail fantasy:** shared drivers are modeled independently. Analyze correlation and common causes.
- **Expected-value blindness:** catastrophic or distributional harm disappears in the mean. Preserve constraints, tails, and affected groups.
- **Steady-state tunnel vision:** migration, coexistence, support, and retirement are omitted. Compare full lifecycle pathways.
- **Score-as-decision:** highest total is treated as mandatory. Keep recommendation, authority, rationale, and residual risk explicit.
- **Sensitivity ritual:** weights vary by arbitrary ±10% but important assumptions do not. Find plausible thresholds and joint scenarios.
- **Missing dissent:** disagreement is averaged away. Record concerns, evidence, and authority.
- **Irreversible baseline:** no reversal criteria or monitoring exist. Govern assumptions and reopen triggers.

## Worked Examples

### Example 1

A warning system compares centralized, federated, and hybrid authority. Partition autonomy is mandatory, so centralized fails despite lower cost. Hybrid and federated remain Pareto candidates. Hybrid leads nominally; federation wins under higher autonomy preference. A prototype targets reconciliation uncertainty, and the decision record preserves a fallback rather than claiming a universal winner.

### Example 2

A spacecraft instrument compares one high-capability unit with two diverse lower-capability units. Simple expected science favors the single unit. Common-cause and launch mass assumptions shape redundancy value, while diversity increases integration and calibration cost. The team reports a frontier of science yield, mission-loss exposure, mass, and schedule; authority chooses diversity because a noncompensatory mission-continuity policy applies.

### Example 3

A hospital compares local clinical-decision support, a central service, and a hybrid cache. The central service has better model-governance consistency but fails a network-outage constraint. Local deployment meets availability but increases update and monitoring workload. Hybrid is retained only after clinician trials, privacy review, bounded cache validity, rollback, and outcome surveillance. Software metrics alone cannot authorize clinical use.

### Example 4

Three warehouse architectures receive value scores for effectiveness, resilience, operability, and lifecycle cost. Alternative A scores 90, 60, 55, 80; B scores 78, 82, 75, 65; C scores 72, 70, 88, 70. With weights 0.35, 0.25, 0.20, 0.20, totals are A 73.5, B 75.8, C 74.3. B’s nominal 1.5-point lead over C is too small to interpret without uncertainty and sensitivity.

### Example 5

A water utility’s candidate-dependent normalization makes an existing option’s score fall when an obviously poor fourth option is added. The team replaces min–max normalization over candidates with stakeholder-anchored value functions: unacceptable, minimally acceptable, target, and saturation points. Scores now remain stable when irrelevant alternatives enter the set.

### Example 6

A platform compares one supplier with dual sourcing. Procurement scores cost, availability, and “supplier resilience” separately, double-counting outage reduction. Causal review separates service continuity, switching feasibility, correlated regional dependency, commercial concentration, and lifecycle cost. Dual sourcing loses its artificial score advantage but remains valuable when exit lead time exceeds the business continuity threshold.

### Example 7

A rail operator prefers a target architecture with the lowest steady-state cost, but migration requires a twelve-month dual-control interval with an unproven reconciliation path. The incremental alternative costs more in steady state yet permits reversible region-by-region cutover. Transition risk makes the target infeasible until a hardware-in-loop migration demonstration closes the gap.

### Example 8

An autonomous inspection system can commit now or fund a field trial. Current evidence yields a 40% chance that autonomy meets the workload target; otherwise redesign costs are high. A focused trial could materially change the architecture choice before supplier commitment. The team estimates study benefit, cost, delay, and opportunity, funds the trial, and sets a decision date rather than demanding perfect knowledge.

### Example 9

A disaster-response network compares maximum expected coverage with minimax regret across mild, regional, and nationwide infrastructure-loss scenarios. A centralized design leads expected coverage under forecast probabilities; a mesh design has lower worst-case regret. Because probabilities are weak and minimum emergency coverage is mandatory, mesh becomes the recommendation. The choice reflects authorized robustness preference, not mathematical inevitability.

### Example 10

A data platform recommends event sourcing over current-state storage based on auditability and replay. Review finds deletion obligations, derived-data erasure, schema evolution, rebuild duration, and operator skill were omitted. After lifecycle scenarios and privacy constraints, a hybrid immutable operational ledger plus governed deletable projections is selected. Reversal criteria include rebuild time, storage growth, deletion verification, and operational incident rate.

## Cross-Program Connections

- **Platform engineering:** central/federated control planes, tenancy, cell architectures, supplier strategies, and migration pathways are architecture decisions under uncertainty.
- **API and service engineering:** service boundaries, synchronous/events, orchestration/choreography, and compatibility strategies need common-basis trade studies.
- **Data engineering:** batch/stream, lake/warehouse, state/log, consistency, retention, and lineage choices expose lifecycle and privacy tradeoffs.
- **Object-oriented programming:** class and responsibility organizations can be compared, but code metrics alone do not capture system lifecycle value.
- **Functional programming:** purity, effects, laziness, streaming, and state models create measurable performance, reasoning, and integration consequences.
- **Risk and economics:** uncertainty, correlation, tail consequences, lifecycle cost, option value, and value of information connect engineering to accountable investment.
- **Human factors:** workload, situation awareness, skill, trust, handoff, accessibility, and organizational transition are criteria and evidence domains.
- **Verification:** prototypes, simulations, trials, and tests should target uncertainties capable of changing feasibility or preference.

## References

1. NASA, *Systems Engineering Handbook, Section 4.4: Design Solution Definition*, current web edition, updated 2023. <https://www.nasa.gov/reference/4-4-design-solution-definition/>
2. NASA, *Systems Engineering Handbook, Section 6.8: Decision Analysis*, current web edition, updated 2023. <https://www.nasa.gov/reference/6-8-decision-analysis/>
3. NASA, *Systems Engineering Handbook, Section 4.0: System Design Processes*, current web edition, updated 2023. <https://www.nasa.gov/reference/4-0-system-design-processes/>
4. Systems Engineering Body of Knowledge, *Analysis and Selection between Alternative Solutions*, SEBoK version 2.14, 2026. <https://sebokwiki.org/wiki/Systems_Analysis_Approach>
5. Systems Engineering Body of Knowledge, *System Analysis*, SEBoK version 2.14, 2026. <https://sebokwiki.org/wiki/System_Analysis>
6. Systems Engineering Body of Knowledge, *Synthesizing Possible Solutions*, SEBoK version 2.14, 2026. <https://sebokwiki.org/wiki/Synthesizing_Possible_Solutions>
7. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>
8. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2022. <https://www.iso.org/standard/74393.html>

## Exercises

### Exercise 1

Frame and generate at least four architecture alternatives for a remote water-monitoring capability. Include authority, common scenarios, mandatory constraints, meaningful architecture dimensions, status quo/defer, evidence package, and pruning rules.

### Exercise 2

Using the Example 4 scores and weights, recompute all totals. Then find the resilience-weight value at which B and C tie when the other three weights retain their relative proportions and sum to the remaining weight. Interpret the result cautiously.

### Exercise 3

Review a trade study that rates safety, reliability, availability, downtime, cost, and schedule from 1–5; assigns weights after seeing results; uses min–max normalization across candidates; and reports the highest score to two decimals. Identify at least ten defects and propose a defensible redesign.

### Exercise 4

A prototype costs $0.4 million. Without it, Alternative A is chosen and has expected utility 72. With perfect information, the team would choose A in 60% of states with utility 78 and B in 40% with utility 84. Compute EVPI in utility points, then explain why this does not establish that the prototype should be funded.

### Exercise 5

Design an assurance review for choosing centralized, federated, or hybrid authorization for a multi-region platform. Include constraints, criteria, measures, uncertainty/correlation, scenarios, migration, sensitivity, robustness, decision authority, residual risks, and reversal criteria.

## Answers to the Exercises

### Answer 1

Frame the decision as selecting a logical/operational architecture that produces trusted observations from remote sites for authorized users across normal, disconnected, maintenance, sensor-fault, cyberattack, extreme-weather, update, recovery, and retirement scenarios. Name the water authority as decision owner and include operators, maintainers, communities, regulators, security/privacy, communications, suppliers, and data users. Mandatory constraints might include observation validity, maximum alert delay, local retention during a 48-hour outage, authenticated configuration, environmental limits, worker safety, privacy, and a lifecycle cost ceiling.

Alternatives include current manual collection/status quo; centralized interpretation with raw telemetry; local interpretation with summary/event transmission; hybrid local safety alerts plus central analytics; and defer while piloting communications. Describe sensors, state/authority, flows, humans, power, communications, calibration, maintenance, security, migration, and retirement to common maturity. Prune only physical or mandatory infeasibility with recorded evidence. Require common field/load/fault scenarios, timing/energy models, operator trials, security review, calibration evidence, lifecycle estimates, and migration plans. No-action remains visible even if it fails future timeliness.

### Answer 2

The totals are:

$$
V_A=.35(90)+.25(60)+.20(55)+.20(80)=73.5,
$$

$$
V_B=.35(78)+.25(82)+.20(75)+.20(65)=75.8,
$$

$$
V_C=.35(72)+.25(70)+.20(88)+.20(70)=74.3.
$$

Let resilience weight be (r). Original non-resilience proportions are 0.35:0.20:0.20, so normalized within the remaining weight they are (7/15,4/15,4/15). The B-minus-C value is:

$$
r(82-70)+(1-r)\left[\frac7{15}(78-72)+\frac4{15}(75-88)+\frac4{15}(65-70)\right].
$$

The bracket equals (-2), so (12r-2(1-r)=0), yielding (r=1/7\approx0.1429). Above that value B leads C under this model; below it C leads. The current 0.25 resilience weight is above the threshold. This is a model sensitivity result, not proof: score uncertainty, value functions, weight elicitation, dependencies, and hard constraints still govern interpretation.

### Answer 3

Defects include ordinal arithmetic; missing operational definitions; possible overlap among safety, reliability, availability, and downtime; no hard-constraint screen; weights chosen after results; candidate-dependent normalization; false two-decimal precision; absent stakeholders/authority; no common scenario/configuration basis; no evidence quality; no uncertainty or correlation; no sensitivity; no lifecycle/migration effects; no distributional impact; and score-as-decision behavior.

Redesign by framing the decision and authority first. Define mandatory safety/legal/mission constraints. Build a nonoverlapping value hierarchy tied to outcomes. Define natural measures and anchored value functions; elicit range-dependent weights before results. Characterize candidates to common maturity and run common scenarios. Model reliability/availability causally rather than counting them repeatedly. Preserve cost/schedule distributions, tails, correlation, and evidence grades. Use anchored scales independent of candidates. Screen feasibility, assess dominance/Pareto structure, run sensitivity and robustness analyses, document dissent, and present a recommendation separately from the accountable decision.

### Answer 4

With perfect information, expected utility is:

$$
0.60(78)+0.40(84)=80.4.
$$

Without information, the chosen action has expected utility 72, so:

$$
EVPI=80.4-72=8.4\text{ utility points}.
$$

This is an upper bound for perfect information, not the value of the proposed prototype. Funding requires the prototype’s likelihood of producing each observation, how those observations change the decision, posterior outcomes, implementation consequences, cost converted into the same value framework, schedule delay, opportunity cost, residual uncertainty, and model validity. A $0.4 million cost cannot be compared directly with 8.4 utility points without a valid multiattribute/value model and decision authority.

### Answer 5

Mandatory constraints should cover tenant isolation, authorization correctness, revocation deadline, partition behavior, audit reconstruction, privacy/data residency, administrative authority, minimum availability, and recovery. Preference criteria may cover decision latency, policy consistency, resilience, blast radius, operability, change lead time, workload, lifecycle cost, migration risk, and supplier dependence. Define measures with region count, demand/burst, threat, policy-change, failure, time, and cost conditions.

Compare centralized authority, federated regional authority, and a hybrid with signed policy distribution and bounded local decisions. Model correlated region failures, shared identity/key/policy dependencies, common software, network partitions, compromise, clock faults, stale cache, urgent revocation, partial rollout, rollback, overload, region evacuation, migration, and rejoin. Include security/privacy analysis, load/fault tests, policy-reconciliation prototypes, administrator trials, audit exercises, and lifecycle estimates. Screen hard limits before valuation; test weights, staleness bounds, demand, failure correlation, staffing, and migration duration jointly. Assess expected and worst-plausible outcomes plus option value of staged rollout.

The recommendation should show feasible/Pareto candidates, unstable thresholds, evidence gaps, dissent, residual risk, and owner. The platform authority records the decision and acceptance within its remit. Reversal criteria include measured revocation or reconciliation beyond bounds, workload above staffing capacity, new residency constraints, repeated policy divergence, compromise propagation, cost thresholds, or evidence that partition assumptions changed. Conclusions apply only to the evaluated scale, threat, topology, policy, and operational configurations.
