---
module_id: SYSENG-003
program: Systems Engineering
level: 1
module_number: 3
title: Stakeholders and Value
status: complete
last_verified: 2026-08-30
---

# Stakeholders and Value

## One-Page Review

### Governing question

Whose conditions make a system valuable or unacceptable, how are their authority and exposure different, and what evidence lets engineers reason about value across a whole lifecycle without collapsing it into price, preference, or one sponsor's score?

### Essential definitions

- A **stakeholder** is an individual, group, organization, or other party with an interest in, influence over, responsibility for, dependence on, or exposure to a system and its lifecycle outcomes.
- A **stakeholder role** describes a relationship to the system—user, beneficiary, operator, maintainer, acquirer, owner, supplier, regulator, adversary, affected non-user, or future steward—not a fixed identity.
- A **need** is a condition or capability necessary to address a stakeholder problem or opportunity; a **preference** ranks acceptable alternatives but is not automatically mandatory.
- **Value** is the context-dependent worth of consequences to stakeholders relative to objectives, resources, risks, alternatives, and time.
- A **value object** is what is valued: safety, mission effect, accessibility, privacy, maintainability, revenue, ecological condition, or another consequence.
- A **measure of effectiveness** indicates mission or operational success; a **measure of performance** characterizes how a system performs. Neither is automatically a complete value measure.
- A **constraint** excludes alternatives regardless of compensating benefit; an **objective** expresses a direction of preference; a **criterion** supports comparison.
- A **value model** makes objectives, measures, directions, thresholds, trade assumptions, stakeholders, time, and uncertainty explicit.
- **distribution** asks who receives benefits, bears costs, or experiences risks; an aggregate can improve while a subgroup is harmed.
- **decision authority**, **domain expertise**, **operational responsibility**, and **consequence exposure** are separate dimensions.

### Central model, mechanism, or theorem

Represent a stakeholder-value claim as:

\[
V=(S,C,O,M,T,D,U,A,E),
\]

where \(S\) identifies stakeholder roles, \(C\) the system context, \(O\) objectives, \(M\) measures and directions, \(T\) thresholds and time horizon, \(D\) distribution, \(U\) uncertainty, \(A\) authority and conflict rules, and \(E\) evidence. A proposed system alternative is acceptable only if it satisfies noncompensatory constraints and has an adequately evidenced consequence profile. A high aggregate score cannot compensate for a violated safety, legal, rights, or mission threshold unless the governing authority explicitly and lawfully defined it as compensatory.

### Critical invariants

- Identify stakeholders from lifecycle interactions and consequences, not only from the organization chart.
- Record roles, authority, expertise, responsibility, dependence, and exposure separately.
- State value as a consequence in context; a feature, subsystem, vendor, schedule, or technology is usually a means.
- Keep objectives distinct from measures and measures distinct from evidence quality.
- Express thresholds and noncompensatory constraints before combining preferences.
- Report distributions and affected groups; an average does not establish universal benefit.
- Include operation, maintenance, support, supply, security, emergency, retirement, and disposal consequences.
- Trace disagreements to assumptions, objectives, measures, time horizons, or authority instead of averaging unlike claims.
- Preserve uncertainty and dissent; false precision does not create agreement.
- Automated calculations reproduce declared value rules only. They cannot establish legitimacy, completeness, or ethical acceptability.

### Common failures

Failures include equating stakeholder with buyer; treating the loudest executive as the domain; listing everyone without role boundaries; calling a feature “value”; using cost as the universal denominator; counting users while excluding maintainers and affected non-users; converting legal or safety constraints into small negative weights; hiding subgroup harm in an average; double-counting correlated criteria; choosing measures because data are easy; treating a survey preference as a need; ignoring future operation and disposal; using one-time acquisition value for a long-lived system; and claiming a weighted spreadsheet made the decision objective.

### Compact example

A city evaluates electric buses. Riders value reliable, accessible journeys; drivers value safe workload and ergonomics; maintainers value diagnosability and parts access; the operator values fleet availability and lifecycle cost; residents value lower noise and emissions; emergency services need evacuation capability; the regulator owns safety and accessibility constraints. “Buy the cheapest bus” ignores the system. Engineers first impose braking, accessibility, and emergency constraints; then compare route coverage, charging resilience, maintenance exposure, noise, emissions, labor, cost, and uncertainty by stakeholder and time. A bus with the best mean score but an infeasible cold-weather route is rejected.

### Connections

Retrieve [systems, boundaries, environments, and context](001-systems-boundaries-environments-and-context.md) and [purpose, mission, and measures of effectiveness](002-purpose-mission-and-measures-of-effectiveness.md). Continue to elements, relationships, emergence, feedback, uncertainty, context scenarios, and problem framing. Modules 011–020 turn justified stakeholder needs into managed requirements; Modules 041–050 develop formal trade studies and decisions.

## Governing Question

A system is valuable only through consequences in a world containing many parties, timescales, and authorities. The acquiring organization may gain capacity while operators inherit unsafe workload. Users may gain speed while nearby communities bear noise. A safety improvement may cost schedule and money; a cheap design may create decades of support burden. How can systems engineers make these value claims inspectable without pretending that every consequence is commensurable?

The answer is a stakeholder-value model, not a stakeholder list followed by a weighted sum. The model identifies relationships to the system, objectives and constraints, measures, consequence distributions, evidence, uncertainty, lifecycle time, and decision rights. It distinguishes what is desired from who may decide and what cannot lawfully or ethically be traded away.

## Why This Matters

Systems cross organizational and physical boundaries. Their effects are jointly produced by hardware, software, people, procedures, supply chains, infrastructure, policy, and environment. A technically correct subsystem can reduce whole-system value by moving work to operators, creating brittle maintenance, excluding users, or increasing common-cause risk.

ISO/IEC/IEEE 15288:2023 treats stakeholder needs and requirements definition as a technical process within the system lifecycle. ISO/IEC/IEEE 29148:2018 provides requirements-engineering guidance spanning business or mission analysis and stakeholder needs. The INCOSE Systems Engineering Handbook, fifth edition, connects stakeholder needs, measures of effectiveness, lifecycle concepts, architecture, verification, and validation. These sources do not authorize engineers to invent stakeholder values; they require disciplined elicitation, analysis, resolution, and traceability.

Stakeholders are relational. The same person may be a user during normal operation, an emergency operator during failure, a maintainer during service, and an affected resident after disposal. Organizations can be stakeholders, but organizational labels hide internal conflict. “Operations” contains dispatchers, supervisors, field technicians, and incident commanders with different evidence.

Value is broader than economic price and narrower than vague goodness. It describes worth relative to objectives and alternatives in a context. Monetary analysis is useful where costs and benefits are meaningfully monetized, but safety, rights, ecological thresholds, mission survival, and legitimacy may be noncompensatory or require separate governance. Refusing an invalid conversion is more rigorous than assigning a guessed dollar value.

Value also changes through time. Acquisition may favor low purchase price; operation reveals energy and staffing cost; maintenance exposes parts availability; evolution creates compatibility burden; retirement creates data, waste, and remediation duties. Discounting can compare time-distributed monetary flows, but it cannot silently erase long-term safety or environmental obligations.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. a system boundary is chosen for a purpose and can hide transferred consequences;
2. a mission statement names intended change in an operational context;
3. measures of effectiveness support mission judgments but remain evidence with assumptions;
4. a stakeholder goal is not a system requirement until analyzed and accepted through authority;
5. a necessary constraint differs from a preferred objective;
6. correlation between a system measure and an outcome does not establish causation;
7. lifecycle activities include operation, maintenance, evolution, and retirement, not only acquisition and development.

Draw one context diagram and mark every flow of material, energy, information, control, money, labor, risk, and responsibility. Each source, sink, controller, bearer, or dependent party is a stakeholder candidate. This does not prove inclusion is complete; it makes omissions challengeable.

## Learning Objectives

After completing this module, you should be able to:

1. identify stakeholder roles from system context and lifecycle consequences;
2. distinguish authority, expertise, responsibility, dependence, influence, and exposure;
3. separate value objects, objectives, constraints, criteria, measures, and evidence;
4. transform solution requests into consequence-oriented value hypotheses;
5. construct a stakeholder-value map across normal, degraded, emergency, maintenance, and retirement contexts;
6. distinguish compensatory preferences from noncompensatory thresholds;
7. detect double counting, proxy error, distributional harm, and time-horizon bias;
8. analyze conflicts without averaging incompatible authority or units;
9. use bounded multi-criteria calculations and sensitivity checks honestly;
10. define human review and evidence limits for high-consequence decisions.

## Core Exposition

**Identify relationships, not generic people.** Start with the system context. Who supplies inputs? Who receives outputs? Who operates, maintains, secures, transports, certifies, funds, insures, depends on, attacks, cleans up, or is involuntarily exposed? Repeat for normal, degraded, emergency, maintenance, upgrade, and retirement scenarios. A party can occupy several roles, and one role can contain heterogeneous parties.

Classify each relationship along separate axes:

| Axis | Question | Example |
|---|---|---|
| Authority | What decision may this party lawfully or organizationally make? | safety regulator approves operation |
| Expertise | What domain knowledge or evidence can this party contribute? | technician knows field repair reality |
| Responsibility | What outcome must this party achieve or restore? | operator maintains service continuity |
| Dependence | What capability does this party rely upon? | hospital relies on grid and oxygen supply |
| Exposure | What benefit, burden, or risk can this party experience? | resident bears noise without using service |
| Influence | What resources or leverage can this party exercise? | supplier controls a scarce component |

Do not infer authority from influence or legitimacy from authority alone. A sponsor can authorize budget but cannot redefine physical law. A regulator can set binding constraints in scope but may not know detailed operator workload. A highly exposed group deserves representation even when it has little formal power.

**Find value objects.** Ask what conditions matter if every proposed solution name is removed. “We value a mobile application” is usually a solution preference. Underneath may be timely access, independence, lower operator workload, auditability, or reach during network disruption. Retain the application as an alternative, not the value definition.

Organize value objects in a hierarchy only when the relationships are meaningful. A top objective such as “provide trustworthy emergency communication” may decompose into reach, timeliness, intelligibility, authenticity, accessibility, and recoverability. Avoid counting the parent and every child as independent benefits in one aggregate; that double-counts the same consequence.

**Separate constraints from objectives.** A legal accessibility requirement, maximum hazardous exposure, minimum braking distance, or mission survival threshold can eliminate an alternative. A preference for lower energy use or easier training may permit trade. Classification comes from governing authority and consequence, not from whether a number exists.

Some thresholds are conditional. An aircraft may accept one performance envelope under normal mode and another during a declared emergency. State context, transition, duration, and recovery. “Safety first” is not an executable rule; named hazard constraints and decision authority are.

**Define measures without confusing them with value.** For each objective, specify measure, unit, direction, population, scenario, time window, data source, uncertainty, and decision use. “Availability” might mean probability of being operational when demanded, proportion of scheduled time, or mission completion despite degraded components. Each yields different conclusions.

A proxy is acceptable only with a stated relationship to the value object. Number of alerts sent is not population warned. Test coverage is not safety. Deployment frequency is not mission value. Cost variance is not lifecycle affordability. Maintain a chain from value object through hypothesized mechanism to observed evidence, and look for counterexamples.

**Model distribution.** For stakeholder \(s\), scenario \(q\), time \(t\), and alternative \(a\), define a consequence profile \(x_{s,q,t}(a)\). Do not aggregate until the profile is visible. Report who benefits, who pays, who performs extra work, who bears residual risk, and who is missing from evidence.

Distribution matters even within one stakeholder class. A transport system's average journey time can improve while wheelchair users face longer transfers. A maintenance mean can improve while rare repair actions become impossible in protective equipment. Predeclare relevant subgroups and scenarios based on mechanisms and consequences, not after-the-fact metric mining.

**Represent time and lifecycle.** Distinguish acquisition, transition, operation, maintenance, evolution, and retirement consequences. An alternative with low purchase cost can depend on a sole-source component, proprietary diagnostic access, high energy use, and hazardous disposal. Record who owns each future obligation and what happens if assumptions fail.

Time preference is a value-policy choice. Discounting future money requires a rate and rationale. Do not apply the same arithmetic automatically to fatalities, irreversible ecological loss, legal duties, or intergenerational effects. Where consequences cannot be validly commensurated, present a vector, constraints, scenarios, and accountable judgment.

**Resolve conflict diagnostically.** When stakeholders disagree, locate the disagreement:

1. different system boundary or scenario;
2. different objective or value object;
3. different measure definition or data;
4. different prediction of consequences;
5. different uncertainty tolerance;
6. different time horizon or distribution;
7. competing rights or authority.

Evidence can resolve factual disagreements. Design alternatives can reduce conflicts. Governance must decide genuine preference conflicts. Engineers document the distinction and do not disguise the last category as a technical optimization.

**Construct an accountable value model.** A minimal record contains stakeholder and role; source; objective; rationale; measure and direction; threshold; scenario and time; distribution; evidence; uncertainty; constraint/compensatory classification; decision authority; conflicts; and review trigger. Version it when contexts or policies change.

**Use aggregation cautiously.** A multi-attribute score can make declared preferences reproducible. Normalize measures only over justified ranges. Weights require a stated elicitation method and interpretation. Additive scoring assumes preferential independence and compensation. Correlated criteria can double-count. Thresholds must be checked before scoring.

Suppose normalized values \(v_j(a)\in[0,1]\) and weights \(w_j\ge0\), \(\sum w_j=1\). An illustrative score is:

\[
S(a)=\sum_j w_jv_j(a).
\]

The arithmetic proves only the result of the declared model. It does not prove objectives are complete, normalization is valid, weights are legitimate, forecasts are accurate, or the highest score is acceptable. Modules 041–050 develop utility, trade studies, sensitivity, uncertainty, and decision rationale in depth.

The executable example applies two noncompensatory constraints before a toy score and then varies weights. Alternative B has the highest base score but fails accessibility; it is never selected. The example is deliberately small and not a real procurement decision.

<!-- bijux-verify: {"id":"constraint-first-value-screen","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"A feasible=true score=0.750\nB feasible=false score=0.838\nC feasible=true score=0.688\nselected=A\nweight_case=mission selected=A\nweight_case=maintainer selected=C\nweight_case=cost selected=A\nB_rejected_for=accessibility\nscore_proves_legitimacy=false\nevidence=declared_toy_model_only\n","stderr":""}} -->
```python
alternatives = {
    "A": {"safety": True, "accessibility": True,
          "mission": 0.80, "maintainability": 0.65, "cost": 0.75},
    "B": {"safety": True, "accessibility": False,
          "mission": 0.90, "maintainability": 0.70, "cost": 0.85},
    "C": {"safety": True, "accessibility": True,
          "mission": 0.65, "maintainability": 0.90, "cost": 0.55},
}

base_weights = {"mission": 0.50, "maintainability": 0.25, "cost": 0.25}
cases = {
    "mission": {"mission": 0.70, "maintainability": 0.15, "cost": 0.15},
    "maintainer": {"mission": 0.30, "maintainability": 0.60, "cost": 0.10},
    "cost": {"mission": 0.30, "maintainability": 0.20, "cost": 0.50},
}

def feasible(values):
    return values["safety"] and values["accessibility"]

def score(values, weights):
    return sum(weights[name] * values[name] for name in weights)

for name, values in alternatives.items():
    print(f"{name} feasible={str(feasible(values)).lower()} "
          f"score={score(values, base_weights):.3f}")

eligible = {name: values for name, values in alternatives.items() if feasible(values)}
selected = max(eligible, key=lambda name: score(eligible[name], base_weights))
print(f"selected={selected}")
for case, weights in cases.items():
    chosen = max(eligible, key=lambda name: score(eligible[name], weights))
    print(f"weight_case={case} selected={chosen}")
print("B_rejected_for=accessibility")
print("score_proves_legitimacy=false")
print("evidence=declared_toy_model_only")
```

**Perform sensitivity and uncertainty review.** If small plausible weight or forecast changes reverse the selection, the decision is fragile. That does not mean “collect data forever.” It means identify the uncertainty driving the decision, seek targeted evidence, preserve options, or choose a robust alternative. Record scenarios where no option is acceptable.

**Close the loop.** After deployment, observe whether consequences match forecasts. Update value and system models when operator burden, distributional effects, incidents, costs, or mission outcomes differ. A value model that exists only for acquisition becomes a justification artifact rather than an engineering control.

## Definitions and Notation

Let:

- \(S\) be stakeholder roles rather than a set of named meeting attendees;
- \(A\) be candidate system alternatives;
- \(Q\) be operational and lifecycle scenarios;
- \(T\) be relevant times or lifecycle stages;
- \(O\) be objectives and noncompensatory constraints;
- \(x_{s,q,t}(a)\) be the consequence profile for stakeholder \(s\), scenario \(q\), time \(t\), and alternative \(a\);
- \(E\) be evidence supporting predicted or observed consequences;
- \(U\) represent uncertainty and limitations.

An alternative is **feasible** when every applicable mandatory constraint holds:

\[
Feasible(a)=\bigwedge_{c\in Constraints} c(a).
\]

Only feasible alternatives enter a compensatory comparison. This ordering prevents an attractive score from laundering a forbidden condition.

A **fundamental objective** states a valued end in the decision context. A **means objective** describes a way to advance another objective. “Minimize response time” may be fundamental for emergency effect; “increase processor speed” is usually a means. The distinction depends on the decision boundary.

A **value function** maps a consequence to a preference scale under explicit assumptions. It is not a physical measurement. A **utility function** additionally represents attitudes to uncertainty under its elicitation model. This chapter uses only a deterministic illustrative value score; utility theory belongs later.

## Mechanisms, Invariants, or Proof Structure

Use this stakeholder-value procedure:

1. **Set the decision context.** Name mission, system boundary, alternatives, lifecycle horizon, and excluded decisions.
2. **Map stakeholder relationships.** Traverse context flows and scenarios; distinguish authority, expertise, responsibility, dependence, exposure, and influence.
3. **Elicit consequences before solutions.** Ask what conditions matter, why, to whom, when, and under which failure modes.
4. **Structure objectives.** Separate ends from means, remove duplicate consequences, and expose conflicts.
5. **Classify constraints.** Cite legal, safety, rights, mission, contractual, or policy authority; state modes and exceptions.
6. **Operationalize carefully.** Define measures, units, directions, populations, thresholds, scenarios, uncertainty, and evidence sources.
7. **Preserve distributions and time.** Report stakeholder- and scenario-indexed consequences before aggregation.
8. **Compare and test sensitivity.** Apply constraints first, inspect dominance and trade-offs, vary disputed assumptions, and identify fragile choices.
9. **Assign decision rights.** Record who recommends, supplies evidence, approves, accepts residual risk, and can revisit the decision.
10. **Validate in operation.** Compare observed consequences with forecasts and revise system, value model, or governance.

Five invariants organize review.

**Representation invariant.** Every materially exposed stakeholder role has a representation or justified evidence route; meeting attendance alone does not establish coverage.

**Authority invariant.** Evidence, recommendation, approval, and residual-risk acceptance are attributed to the correct roles. A calculation has no decision authority.

**Constraint invariant.** Mandatory thresholds are evaluated before compensatory preference models and cannot disappear through normalization.

**Distribution invariant.** Aggregate improvement never entails improvement for every stakeholder, mode, geography, or time.

**Evidence invariant.** Each value claim states whether it is elicited preference, expert judgment, modeled prediction, test result, operational observation, or causal inference. Stronger conclusions require stronger evidence.

An adequacy argument must show that stakeholder discovery is credible, objectives represent consequences, measures validly support those objectives, constraints have authority, predictions state uncertainty, trade rules fit the decision, and operational evidence can revise the result. Arithmetic is one small link.

## Alternatives and Trade-Offs

**Interviews versus operational observation.** Interviews reveal goals and reasoning; observation reveals workarounds and tacit constraints. Use both and reconcile contradictions with concrete scenarios.

**Named representatives versus broad participation.** Representatives make decisions tractable but can miss internal diversity. Define constituency, selection, feedback route, and dissent; expand participation with consequence and irreversibility.

**Qualitative narratives versus quantitative models.** Narratives preserve mechanisms and exceptions. Quantitative models compare scale and sensitivity. Translate only where construct validity and units justify it; keep irreducible claims visible.

**Monetization versus multi-criteria profiles.** Monetary measures support budgets and lifecycle cost. They can distort rights, safety, environment, and low-frequency catastrophe. Use constraints and consequence vectors where conversion lacks legitimacy.

**Consensus versus governed conflict.** Consensus can improve commitment but may suppress minority harm or statutory duties. Resolve evidence disagreements collaboratively; escalate genuine authority conflicts through declared governance.

**Current users versus future and affected parties.** Current users offer direct evidence. Future operators, maintainers, communities, and ecosystems cannot always participate. Use lifecycle scenarios, representatives, standards, hazard analysis, and conservative assumptions while stating limitations.

**Single optimum versus robust portfolio.** One score yields a simple answer. Robust alternatives perform acceptably across plausible scenarios; portfolios or staged options preserve learning. Prefer robustness where uncertainty and reversal cost dominate small expected-score gains.

## Failure Modes and Misconceptions

1. **Stakeholder means requester.** Requesters are one relationship among many.
2. **The sponsor defines value.** Sponsors own decisions in scope, not every fact, right, or consequence.
3. **More stakeholders means better engineering.** Unbounded lists without roles and decisions create noise.
4. **A feature is value.** Features are mechanisms; value lies in consequences under assumptions.
5. **Every value needs one KPI.** Some constructs require multiple measures, qualitative evidence, or noncompensatory review.
6. **A number is objective.** Measure selection, normalization, thresholds, and missing data embody judgments.
7. **Weights convert constraints into preferences.** A small safety weight is not a safety argument.
8. **The average represents everyone.** Distribution and intersectional cases can reverse the conclusion.
9. **Survey demand proves need.** Stated preference can differ from behavior, rights, feasibility, and mission necessity.
10. **Cost captures lifecycle value.** Money omits many consequences and can shift cost between parties.
11. **Sensitivity means indecision.** It identifies which assumptions deserve evidence or contingency.
12. **Approval completes value engineering.** Operation can falsify consequence predictions and expose missing stakeholders.

## Worked Examples

### Example 1

**Question:** Who are stakeholders for an autonomous warehouse vehicle besides its purchaser and operator?

**Reasoning:** Trace lifecycle and context flows. Pickers share aisles and bear collision/workload effects; safety representatives and regulators own constraints; maintenance technicians need isolation and diagnostics; facilities owns floor loading and charging; IT/security owns network and update exposure; emergency responders need safe disablement; nearby workers may never use the vehicle but remain exposed; supplier and insurer influence availability and risk; future disposal handlers receive battery hazards. Record each role's authority, evidence, dependence, and exposure separately.

**Conclusion:** Stakeholder discovery follows consequences and lifecycle interfaces, not the procurement organization chart.

### Example 2

**Question:** Rewrite “stakeholders value an AI dashboard” as a system-value model.

**Reasoning:** Ask which decisions fail today. Suppose dispatchers cannot identify unstable loads before assignment. Fundamental objectives are correct early detection, understandable evidence, timely intervention, bounded false alarms, and preserved operator authority. The dashboard is one means alongside alerts, workflow rules, training, or sensor changes. Measures include missed unstable loads, intervention lead time, false-alarm burden, subgroup/route coverage, and safe override. A model prediction supports feasibility; an operational trial supports selected workflow claims; neither proves long-term safety alone.

**Conclusion:** Remove the solution noun to reveal decision consequences, guardrails, alternatives, and evidence needs.

### Example 3

**Question:** Alternative B scores highest but fails the minimum accessibility condition. Can exceptional mission benefit compensate?

**Reasoning:** First inspect authority: if accessibility is a binding legal or accepted system constraint, B is infeasible under the current decision. Its 0.83 score is irrelevant because additive scoring applies only after feasibility. If a lawful emergency exception exists, define its trigger, duration, affected population, alternative access, authorization, and recovery; do not silently lower the weight. Revisit B only by changing the governing context through the authorized process.

**Conclusion:** Constraint-first screening prevents attractive aggregate value from laundering an unacceptable condition.

### Example 4

**Question:** A transit design reduces mean journey time by 8% but increases wheelchair journeys by 20%. Did value improve?

**Reasoning:** The aggregate answers only a population-weighted time question. Inspect denominators, route changes, sample coverage, causal assumptions, and an accessibility non-degradation threshold. Riders using wheelchairs bear a systematically transferred cost and may also face missed connections not represented by time. If the threshold is binding, reject or redesign. If it is a trade under legitimate governance, present the distribution and mitigation explicitly rather than reporting only the mean.

**Conclusion:** Aggregate improvement does not establish distributed value; subgroup mechanism and authority determine acceptability.

### Example 5

**Question:** Finance wants lowest purchase price; maintenance wants common parts; mission leadership wants maximum range. How is conflict analyzed?

**Reasoning:** Separate objectives, predictions, and authority. Calculate lifecycle cost rather than purchase price; quantify parts lead time and fleet commonality; define route scenarios and required range reserve. Check mandatory mission and safety thresholds first. Then compare feasible alternatives and vary fuel, failure, and usage assumptions. If rankings change under plausible assumptions, gather targeted evidence or preserve an option. Budget authority decides affordability, technical authority validates evidence, and mission authority accepts operational trade-offs in scope.

**Conclusion:** Conflict becomes tractable when unlike claims are separated into constraints, consequences, uncertainty, and decision rights.

### Example 6

**Question:** Operators prefer manual control while management predicts automation will reduce staffing. Whose value wins?

**Reasoning:** Neither preference settles the system question. Observe workload, error recovery, skill degradation, staffing assumptions, exceptional modes, safety, throughput, and accountability. Prototype representative normal and degraded scenarios with trained operators. Management owns some resource decisions; safety and labor authorities own others; operators contribute indispensable work evidence. Alternatives may automate routine control while preserving meaningful intervention, or change staffing without removing expertise. Record unresolved distributional effects.

**Conclusion:** Influence does not substitute for evidence, and expertise does not automatically confer budget authority; governance must integrate both.

### Example 7

**Question:** A low-cost sensor lasts five years, while a costly one lasts twelve. Which has higher value?

**Reasoning:** Define system horizon, replacement access, downtime, labor, calibration, supply risk, energy, failure consequences, and disposal. In an accessible warehouse, repeated replacement may be economical. Embedded under a bridge, replacement closure and safety exposure may dominate. Discount justified monetary flows, but keep safety and environmental thresholds separate. Test lifetime uncertainty and failure correlation. A single component price or service-life number cannot answer the system alternative.

**Conclusion:** Lifecycle context and consequence distribution determine value; component attributes do not rank themselves.

### Example 8

**Question:** The toy value model selects A under base weights and C under maintainer-heavy weights. What does that prove?

**Reasoning:** Recompute: only A and C are feasible. Changing declared weights changes their additive scores and reverses selection, so the choice is sensitive to stakeholder preference assumptions. The run proves the implementation matches those inputs. It does not prove additive independence, legitimate weights, correct forecasts, or complete objectives. Investigate maintainability evidence, negotiate authority, present both consequence profiles, and consider a staged trial or robust alternative.

**Conclusion:** Sensitivity is a diagnostic for assumptions and evidence priorities, not an automated decision.

### Example 9

**Question:** A hospital alarm reduces response time in simulation. Is system value established?

**Reasoning:** Simulation supports behavior under its cases and models. It may omit alarm fatigue, staffing, acoustics, device failure, accessibility, training, cybersecurity, escalation, and clinical outcomes. No external medical, regulatory, academic, or practitioner review is claimed. Named clinical, human-factors, safety, biomedical, software, security, operations, patient, and regulatory authorities must review objectives, hazards, evidence, workflow, residual risk, rollout, and monitoring.

**Conclusion:** One favorable performance measure cannot authorize a high-consequence system or establish clinical value.

### Example 10

**Question:** When should an approved stakeholder-value model be revised?

**Reasoning:** Trigger review when system boundary, mission, law, stakeholder population, operational scenario, supplier, hazard, cost structure, evidence validity, or consequence distribution changes; also when incidents and observations contradict forecasts. Preserve the version used for each decision and do impact analysis before replacing it. Do not rewrite history to make the prior decision look better. Close the loop by testing whether corrective changes alter the intended consequences without violating guardrails.

**Conclusion:** A value model is a versioned engineering hypothesis and governance record, not permanent truth or a one-time acquisition worksheet.

## Cross-Program Connections

- [Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) turns stakeholder goals into bounded software models; systems engineering spans the whole capability and lifecycle.
- [Software Engineering: Methods & Evolution](../../10-software-engineering-methods-and-evolution/ROADMAP.md) manages lifecycle work and organizational learning.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) translates quality-attribute concerns into software-wide structures and decisions.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) constructs evidence for selected software claims.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) identifies adversaries, assets, trust, rights, and security risk within the value model.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) governs shared semantics and evidence data used across organizational decisions.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, May 2023. Consulted 2026-08-30.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, November 2018. Consulted 2026-08-30.
3. INCOSE. [*Systems Engineering Handbook: A Guide for System Life Cycle Processes and Activities*](https://www.incose.org/publications/se-handbook-v5), fifth edition, 2023. Consulted 2026-08-30.
4. SEBoK Editorial Board. [Stakeholder Needs and Requirements](https://sebokwiki.org/wiki/Stakeholder_Needs_and_Requirements), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-30.
5. Ralph L. Keeney. *Value-Focused Thinking: A Path to Creative Decisionmaking*. Harvard University Press, 1992.
6. Ralph L. Keeney and Howard Raiffa. *Decisions with Multiple Objectives: Preferences and Value Tradeoffs*. Cambridge University Press, 1993.
7. National Academies of Sciences, Engineering, and Medicine. [*Application of Value Methods in Systems Engineering*](https://doi.org/10.17226/26215). National Academies Press, 2021.
8. ISO. [ISO 9241-210:2019 — Human-centred design for interactive systems](https://www.iso.org/standard/77520.html), second edition, July 2019. Consulted 2026-08-30.

## Exercises

### Exercise 1

For a municipal flood-warning system, identify at least ten stakeholder roles and distinguish authority, expertise, responsibility, dependence, influence, and exposure.

### Exercise 2

Transform “install smart cameras to create value” into a hierarchy of fundamental and means objectives with constraints, measures, scenarios, and counterexamples.

### Exercise 3

Diagnose a trade study that scores safety, purchase price, user satisfaction, compliance, and lifecycle cost with equal weights and selects the highest total.

### Exercise 4

Design a stakeholder-value comparison for two remote-power alternatives: diesel generation and solar-plus-storage. Include lifecycle stages, distribution, uncertainty, thresholds, and sensitivity.

### Exercise 5

Construct the stakeholder and value assurance process for an autonomous railway inspection system. Separate automated evidence from named human authority and state what cannot be concluded without field and external review.

## Answers to the Exercises

### Answer 1

Roles include residents in flood zones, people outside digital channels, emergency dispatch, first responders, municipal leadership, drainage engineers, meteorological and river-data providers, telecommunications and power providers, accessibility/language representatives, hospitals and care facilities, schools, transport operators, neighboring municipalities, privacy/security staff, maintainers, regulators, and future recovery investigators. Emergency authorities decide warnings and evacuation in scope; hydrologists supply domain evidence; operators own timely dissemination; providers control dependencies; residents depend on and are exposed to false negatives, false positives, privacy, and evacuation burden. Vulnerable residents may have high exposure and low influence. A complete answer repeats the mapping for normal, degraded-power, network-loss, false-alarm, extreme-event, maintenance, and post-event scenarios.

### Answer 2

Remove the camera solution. Fundamental objectives might be reduce preventable harm, provide timely trustworthy situational awareness, preserve lawful privacy and civil rights, support accessible response, maintain responder safety, and minimize unjustified surveillance burden. Means objectives include improve detection coverage, evidence quality, communications, dispatch coordination, and auditability. Cameras are one alternative alongside lighting, staffing, sensors, call channels, or environmental redesign.

Constraints include legal authority, prohibited identification uses, retention/access rules, accessibility, and safety. Measures require defined populations and scenarios: detection-to-response latency, verified missed events, false interventions, subgroup/geographic coverage, unauthorized access, operator workload, and outcome guardrails. Counterexamples include more detections with no response capacity, biased coverage, displacement to unobserved areas, and technically successful recording that increases harm. Authority and affected-community review must be explicit.

### Answer 3

The study mixes likely constraints with preferences, double-counts purchase price inside lifecycle cost, assumes equal weights have a neutral meaning, and omits measurement scales, uncertainty, stakeholder distribution, scenarios, and authority. Treat applicable safety and compliance requirements as feasibility gates. Define lifecycle cost without duplicate acquisition terms. Establish value functions and weights through a justified process only for compensatory criteria; inspect preferential independence and correlated satisfaction evidence. Report consequence profiles, missing stakeholders, and sensitivity. A high total cannot rescue unsafe or unlawful alternatives.

### Answer 4

Set context: remote clinic power across construction, operation, maintenance, emergency, refresh, and disposal. Stakeholders include patients, clinicians, technicians, community, owner, fuel suppliers, battery handlers, regulators, and emergency logistics. Hard thresholds include critical-load continuity, electrical safety, emissions/noise rules, and minimum autonomy. Consequences include reliability by season, outage duration, fuel dependence, maintenance access, operator workload, emissions, noise, land, theft/security, purchase and lifecycle cost, battery/fuel disposal, and local capability.

Model solar irradiance, load growth, battery degradation, fuel price/availability, transport disruption, component failure, and repair time with ranges and adversarial scenarios. Report which groups bear noise, air quality, land, and maintenance burdens. Screen infeasible designs, compare remaining profiles, vary discount rate and uncertain inputs, and consider a hybrid or staged measurement. No one score establishes clinical continuity or community legitimacy.

### Answer 5

Stakeholders include track workers, drivers, traffic control, maintainers, infrastructure owner, passengers, nearby communities, sensor/data suppliers, cybersecurity, investigators, safety regulator, labor representatives, and emergency services. Automated evidence can check sensor provenance and calibration, software/configuration identity, coverage, localization error, missed-defect and false-alarm test sets, timing, communications loss, fail-safe behavior, access control, signed updates, traceability, simulation, regression, and bounded field-trial telemetry.

Automation cannot establish acceptable hazard risk, worker role legitimacy, operational fit, community impact, regulatory sufficiency, or whether test distributions represent future track conditions. No external railway, regulatory, academic, or practitioner review is claimed. Named railway-domain, safety, human-factors, worker, software, hardware, cybersecurity, data, operations, accessibility, and regulatory reviewers must assess objectives, hazards, evidence independence, degraded modes, override, training, rollout, residual risk, monitoring, and recall. Decision records must distinguish technical recommendation, operational acceptance, regulatory authorization, and residual-risk ownership.
