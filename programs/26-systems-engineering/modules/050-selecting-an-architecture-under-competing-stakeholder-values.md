---
module_id: SYSENG-050
program: Systems Engineering
level: 1
module_number: 50
title: Selecting an Architecture Under Competing Stakeholder Values
status: complete
last_verified: 2026-08-31
---

# Selecting an Architecture Under Competing Stakeholder Values

## One-Page Review

### Governing question

How can accountable decision makers select an implementable architecture when stakeholders legitimately value different outcomes, some constraints cannot be traded, evidence is incomplete, benefits and burdens are distributed unevenly, and every feasible choice sacrifices something important?

### Essential definitions

- An **architecture alternative** is a coherent system concept: boundary, responsibilities, elements, interfaces, allocation, states/modes, deployment, data/control flows, operations, lifecycle and enabling systems—not a product label or diagram alone.
- A **stakeholder** is a person, group or organization affected by, interested in, contributing to, governing, operating, sustaining or bearing risk from the system.
- A **stakeholder value** is an outcome or principle a stakeholder has reason to care about, such as safety, access, mission effectiveness, autonomy, privacy, affordability, maintainability or environmental impact.
- A **concern** is a stakeholder interest relevant to the system; a **quality-attribute scenario** makes a concern assessable through source, stimulus, environment, affected artifact, response and response measure.
- A **constraint** is a mandatory boundary that eliminates an alternative when violated. A **criterion** differentiates feasible alternatives. Treating one as the other can hide unacceptable harm.
- A **value model** maps evidence about architecture consequences into explicit measures, preference functions and trade logic authorized for the decision.
- A **risk taker** is a stakeholder who bears a consequence if assumptions fail or residual risk is realized; this may not be the budget or decision authority.
- A **Pareto-dominated** alternative is no better on every relevant comparable outcome and worse on at least one, within stated uncertainty and constraints.
- **Distributional analysis** shows who receives each benefit, burden, exposure and option—not merely the population average.
- A **robust** architecture remains acceptable across material evidence, scenario and legitimate preference variations. Robust does not mean optimal everywhere.
- A **decision authority** has the mandate and accountability to choose within scope. Stakeholder participation, technical analysis, recommendation, concurrence and risk acceptance remain distinct roles.
- A **reopening trigger** is an observable change in requirements, values, evidence, architecture, operations, risk or outcomes that requires reassessment.

### Central model, mechanism, or theorem

Let alternatives be $A=\{a_1,\ldots,a_n\}$, stakeholders $S$, scenarios $\Omega$, concerns $C$, evidence state $E$, and decision baseline $B$. First define feasibility:

\[
F(B,E)=\{a\in A: g_j(a,B,E,\omega)\ge \tau_j
\text{ for every mandatory constraint }j\text{ and applicable }\omega\}.
\]

Only then compare value consequences. For stakeholder $s$, a transparent teaching model is

\[
V_s(a,\omega)=\sum_{k=1}^{m} w_{s,k}\,u_{s,k}(x_k(a,\omega)),
\qquad \sum_k w_{s,k}=1,
\]

where $x_k$ is evidence about an outcome, $u_{s,k}$ is a declared preference scale and $w_{s,k}$ is an authorized trade weight. This additive form is valid only when its independence, scale and compensation assumptions are defensible. Selection is a governed judgment over feasibility, stakeholder-specific values, distributions, uncertainty, risk, reversibility and evidence—not simply $\arg\max$ of one averaged score.

### Critical invariants

- The decision question, authority, scope, configured baseline, lifecycle, deadline, reversibility and consequences of deferral are fixed before comparing architectures.
- Stakeholder discovery includes users, non-users, operators, maintainers, integrators, acquirers, regulators, communities, enabling-system owners and people who bear residual risk or lack effective voice.
- Stakeholders are not treated as homogeneous labels; relevant subgroups, conditions, locations and operating contexts remain visible.
- Needs, values, objectives, constraints, requirements, concerns, scenarios, measures and preferences are linked but not conflated.
- Safety, security, privacy, legality, accessibility, human-rights or mission constraints are noncompensatory when governing authority makes them mandatory.
- Architecture alternatives have comparable scope, fidelity, ConOps, allocation, interfaces, enabling systems, maturity and lifecycle descriptions.
- Status quo, defer/information, staged/reversible and fallback alternatives are considered when feasible.
- Evidence retains configuration, population, environment, provenance, uncertainty, conflicts, limitations and applicability; unsupported precision is not created by scoring.
- Preference elicitation identifies whose values are represented, by whom, using what scale, under what authority, and with what conflicts or missing voices.
- Averages never erase worst-case, subgroup, threshold, common-cause, irreversible or catastrophic consequences.
- Recommendation and authority decision explain decisive tradeoffs, rejected alternatives, uncertainty, dissent, accepted residual risk and distributional consequences.
- The selected architecture is translated into requirements, interfaces, controls, work, resources, verification, validation, operations and configuration baselines.
- Implementation completion and stakeholder outcome effectiveness are evaluated separately.
- The decision record preserves evidence and rationale and is superseded—not rewritten—when triggers change its premises.

### Common failures

Common failures include asking stakeholders to vote for diagrams; letting the loudest or paying stakeholder stand for all affected people; treating desires as requirements or constraints as weighted criteria; scoring before defining comparable architectures; using a single nominal scenario; describing a favored alternative in greater detail; hiding enabling systems, labor or transition; normalizing incompatible ordinal scores; double-counting correlated qualities; averaging away an excluded subgroup; allowing cost or schedule points to compensate for safety failure; fabricating consensus; treating an architecture review as democratic authorization; optimizing a proxy rather than outcomes; changing weights after seeing results; choosing the highest mean despite severe tail risk; omitting status quo, staging or information acquisition; ignoring organizational feasibility; documenting only the selected design; and declaring the decision successful when deployment completes rather than when stakeholder outcomes are demonstrated.

### Compact example

A regional clinical-support platform must serve hospitals, small clinics and mobile teams during network disruption. A centralized architecture scores well for maintainability and cost but violates the approved outage-access threshold. A fully edge architecture scores well for local access and privacy but misses a safety-consistency threshold under stale models. A governed hybrid passes safety, disrupted-access and privacy constraints and has the best minimum stakeholder-specific score, although operators still prefer centralization. The authority selects hybrid with signed safety/privacy concurrence, staged pilots, synchronization controls, workload staffing, rollback and outcome thresholds. The record preserves operator dissent and reopens if synchronization incidents, subgroup access, clinician workload, cost or model-update evidence crosses a threshold.

### Connections

SYSENG-001–040 establish system boundary, stakeholders, ConOps, requirements, functions, architecture views, interfaces, realization, verification and integration. SYSENG-041–049 establish values, trade models, programmatic consequences, sensitivity, uncertainty, readiness, risk response and decision records. This capstone joins them: architecture is a governed lifecycle commitment whose acceptability depends on evidence and people, not a diagram or scalar score.

## Governing Question

Can the team show that the selected architecture is feasible under mandatory boundaries, meaningfully addresses the concerns of all materially affected stakeholders across representative and adverse scenarios, makes unavoidable conflicts explicit, and remains a responsible choice under uncertainty—while preserving who disagreed, who bears each consequence and what evidence would reopen the decision?

The goal is not universal satisfaction. Some values conflict structurally: central control can improve consistency while reducing local autonomy; redundancy can improve continuity while raising cost, attack surface and maintenance burden; data sharing can improve coordination while increasing privacy exposure; rapid delivery can defer learning and accessibility. Good systems engineering makes these conflicts decidable without laundering them into a falsely objective total.

## Why This Matters

Architecture allocates more than functions. It allocates control, failure, information, workload, cost, expertise, exposure, recovery capability and future options. Those allocations determine who benefits during nominal service, who struggles during degradation, who must respond at 03:00, who can inspect or contest an automated result, and who pays when assumptions fail. A technically elegant structure can therefore be operationally unusable or socially unacceptable.

NASA's Stakeholder Expectations Definition guidance begins with identifying who stakeholders are and how they intend to use the product, including interested parties affected by use or lifecycle support. It stresses ConOps, scenarios, measurable objectives and decision authority for resolving conflicts. NASA's Design Solution Definition guidance requires alternative concepts to be iteratively reconciled with architecture, ConOps, derived requirements, programmatic constraints and stakeholder expectations before hard-to-reverse choices are made.

ISO/IEC/IEEE 42010:2022 distinguishes an architecture from its description and organizes descriptions around stakeholders, concerns, viewpoints and models. That discipline helps expose incompatible views; it does not choose whose concern prevails. SEI architecture-analysis methods use concrete quality-attribute scenarios and stakeholder participation to reveal sensitivity points, tradeoffs and risks. NIST SP 800-160 Vol. 1 Rev. 1 integrates trustworthy-security concerns through the system lifecycle rather than treating security as a late score. GAO alternatives-analysis findings add comparable alternatives, status quo, impartiality, evidence and independent review. Together these sources support a disciplined process while leaving the legitimate value decision with accountable governance.

## Prerequisites and Retrieval

Before selecting an architecture, retrieve:

1. mission/problem statement, system-of-interest and enabling-system boundary, lifecycle, ConOps, use/misuse/maintenance/emergency scenarios, operating environments and configurations;
2. stakeholder map with users and non-users, subgroups, risk takers, operators, maintainers, integrators, suppliers, regulators, communities, decision authority, technical authorities, reviewers and missing or represented voices;
3. stakeholder expectations, objectives, measures of effectiveness, requirements, constraints, policies, laws, standards, ethical commitments, acceptance criteria and preference authority;
4. functional, behavioral, data, state/mode, physical, deployment, operational, organizational, security, safety and lifecycle views with traceability;
5. architecture alternatives at comparable fidelity, including status quo, staged/defer/information and fallback where meaningful;
6. workload, field, human-factors, accessibility, safety, security, privacy, reliability, performance, cost, schedule, supplier, staffing, sustainability and community evidence with provenance;
7. uncertainty, sensitivity, correlations, tail/common-cause conditions, disagreements, evidence gaps, maturity and reversibility;
8. prior trade studies, risks/hazards, waivers, decisions/dissent, interface agreements, validation results and downstream commitments.

Use a retrieval probe: “We chose microservices because teams value autonomy.” Ask which teams, which users and operators, which workload and release topology, which failure/security/data/transaction scenarios, what autonomy means operationally, which constraints apply, what alternatives were compared, how on-call and cognitive load were distributed, which evidence supports predicted outcomes, and who accepted residual risk. A slogan is not an architecture decision.

## Learning Objectives

After completing this module, you should be able to:

1. frame architecture selection as a configured, authoritative lifecycle decision;
2. identify stakeholders, subgroups, risk takers, missing voices and legitimate representatives;
3. translate needs and concerns into objectives, constraints, scenarios and measurable outcomes;
4. distinguish noncompensatory feasibility from compensatory preference comparison;
5. define genuinely comparable architecture alternatives and expose hidden enabling systems;
6. construct and challenge stakeholder-specific value models without manufacturing consensus;
7. analyze distributions, thresholds, tail/common-cause conditions, sensitivity, uncertainty and reversibility;
8. integrate technical, programmatic, organizational, safety, security, privacy, accessibility and ethical evidence;
9. recommend and authorize an architecture with explicit rationale, dissent, residual risk and conditions;
10. baseline implementation, validate outcomes, monitor triggers and supersede the decision when premises change.

## Core Exposition

**Frame the decision event.** State exactly which architecture commitment is needed, for which system/configuration and lifecycle, by when and under whose authority. Define what “architecture” includes: boundaries, responsibilities, element/interface allocation, deployment, data/control, states/modes, operations, supply, sustainment and disposal. State consequences of deferral and whether the choice can be staged or reversed. Architecture selection is not complete when a workshop ends; it creates downstream commitments.

**Build a stakeholder system, not a contact list.** Identify who receives capabilities, who interacts indirectly, who is excluded, who supplies enabling services, who integrates and sustains, who regulates, who pays, who can halt work and who bears harm. Decompose broad labels such as “users,” “operations” and “the public” when conditions differ. A rural clinic during an outage, an urban hospital under nominal connectivity and a mobile responder with one hand available are not interchangeable samples.

**Clarify representation and power.** Record whether input is direct, sampled, delegated, statutory, expert, contractual or inferred. A product owner can prioritize backlog work but may not legitimately accept patient safety risk. A security authority can define protective constraints but cannot infer community trust. Capture conflicts of interest, participation barriers, dissent protection and who makes the final value judgment. Participation informs authority; it does not silently transfer it.

**Separate need, value, objective and solution.** “We need cloud” is a solution. “Clinicians need current decision support at every care location, including a 30-minute network loss” is an outcome context. Trace values to objectives and measures before proposing structures. Keep stakeholder expectations distinct from contractual requirements, and make constraints explicit rather than hiding them in weights.

**Use scenario-based concerns.** Express qualities under stimulus and environment: “During a regional network loss, an authorized rural clinician requests a current medication warning; the local service responds within two seconds, identifies data/model age and preserves an auditable action.” Scenario detail reveals coupled qualities: availability, consistency, safety, privacy, usability and operations. Measure both desired response and unacceptable boundary.

**Classify constraints before scoring.** Legal prohibitions, minimum safety margins, accessibility duties, security boundaries and mission-critical timing may define feasibility. Record source, applicability, threshold, margin, verification evidence and waiver/acceptance authority. A weighted score must not allow cheapness to compensate for an unlawful or unsafe result. Where a threshold is uncertain, analyze the uncertainty and escalation; do not quietly convert it into preference.

**Construct whole alternatives.** Each alternative needs comparable boundary, functions, logical/physical allocation, data/control, interfaces, states/modes, failure and recovery, trust zones, deployment, staffing, supply, maintenance, migration, retirement, cost/schedule and maturity. Include platform, network, identity, training, monitoring, help desk, manual procedures and other enabling systems. An architecture whose reliability depends on extra people or duplicated infrastructure must carry those burdens.

**Preserve the trade-space search.** Explain how alternatives were generated, combined, pruned and matured. Include status quo, no action, defer for evidence, pilot, staged commitment, modular option and fallback when credible. Record why infeasible alternatives failed and what would reopen them. Do not compare one engineered design with two labels.

**Establish a common evidence baseline.** Evaluate alternatives against the same requirements, workload, population, threat, failure, cost horizon, schedule basis and lifecycle. Bind datasets, experiments, simulations, prototypes, field observations, expert judgments and supplier claims to versions/configurations. Reconcile conflicting evidence. Record applicability: a nominal benchmark does not establish disaster performance, and a laboratory user study does not establish every community outcome.

**Model consequences by stakeholder.** Create an alternative-by-scenario-by-stakeholder consequence table before aggregation. Show who experiences response time, workload, autonomy, exposure, failure, cost and recovery. Report subgroup and condition distributions, not only averages. Identify transferred burdens: automation may reduce central staff while increasing local troubleshooting; redundancy may protect clients while doubling configuration work.

**Define preference functions carefully.** Convert measures to value only when scale meaning is stated. A linear 0–100 function may be inappropriate near a safety cliff, a response-time saturation point or an affordability ceiling. Record whose preference curve and trade weight is represented, how it was elicited, and whether preferential independence supports additive aggregation. Ordinal rankings do not justify arithmetic distance.

**Keep stakeholder views plural.** Compute stakeholder-specific results where useful instead of averaging people into a fictional representative. A portfolio authority may approve an overarching model, but the record should retain each material group's result and dissent. Consensus is neither required nor presumed. A robust compromise can be defensible because it avoids unacceptable downside even when no group ranks it first.

**Apply dominance and constraints before fine scoring.** Remove alternatives that demonstrably violate mandatory constraints or are Pareto-dominated, accounting for uncertainty. Do not prematurely prune an option whose evidence intervals overlap. Document each exclusion and its reconsideration trigger. Compare remaining options using transparent multi-criteria, outranking, scenario, cost-effectiveness, optimization or structured judgment methods appropriate to the evidence.

**Test distribution and noncompensation.** Inspect worst-served subgroup, minimum scenario value, catastrophic outcomes, irreversibility, common cause and cumulative burden. Ask whether a benefit to one stakeholder is being used to compensate for harm to another without legitimate authority. Equity does not require identical outcomes, but relevant differences and reasons must be visible and governable.

**Analyze uncertainty and sensitivity.** Vary evidence, model structure, weights, preference curves, correlations, scenarios, threshold margins, adoption, demand, supplier performance and lifecycle costs. Identify rank reversals, feasibility flips and break-even surfaces. Use adversarial conditions and value-of-information analysis. If the decision turns on an untested synchronization failure, a focused prototype may be better than a more elaborate score.

**Include organizational feasibility.** Architecture and organization interact. Evaluate skills, cognitive load, on-call ownership, decision rights, procurement, suppliers, funding profile, learning curve, governance, incentives and change capacity. “Teams can operate it” is an empirical claim. Do not solve a coordination problem by drawing a distributed architecture whose authority and staffing do not exist.

**Integrate risk and readiness.** Carry hazard, threat, failure, privacy, supplier, schedule, cost, technology and transition scenarios into the comparison. Distinguish inherent, current, planned and residual states. Credit controls only with implementation and effectiveness evidence. A mature component in a novel integration or operating context may still impose high system risk.

**Use independent challenge.** Invite affected stakeholders and domain reviewers to challenge scenarios, constraint interpretations, evidence, model structure and hidden burdens. Protect technical nonconcurrence. Independence improves detection of blind spots but does not confer decision authority or guarantee correctness. Record unresolved objections and their disposition.

**Form the recommendation.** State which architecture is recommended, for which baseline, and why. Name decisive objectives and constraints, evidence and uncertainty, key rejected alternatives, stakeholder distributions, robustness, residual risks, assumptions, implementation conditions and confidence. If no alternative is acceptable, say so and recommend reframing, requirement/value negotiation, information acquisition or new concepts.

**Make the authority decision explicit.** Record the selected action, authority, concurrences, conditions, funding/schedule bounds, risk acceptances, dissent and reasons for any departure from the technical recommendation. The decision authority may make a legitimate portfolio or policy judgment outside the analysis; it must be visible rather than backfit into weights.

**Baseline and propagate.** Translate the decision into architecture descriptions/views, requirements, interfaces, allocations, budgets, safety/security/privacy controls, contracts, team responsibilities, plans, verification/validation, risk responses and configuration items. Identify invalidated assumptions and superseded downstream decisions. A choice that cannot be propagated is not yet implementable.

**Verify implementation and validate outcomes.** Verify that architectural elements, interfaces, controls, staffing and processes match the decision. Then validate whether stakeholder outcomes occur across representative and adverse scenarios. Measure access, safety events, response, workload, recovery, privacy, cost and satisfaction by relevant groups. Deployment, test pass or architecture conformance alone does not prove value.

**Monitor and reopen.** Assign owners and cadence for requirements, stakeholder/value, workload/population, threat, technology/supplier, cost/schedule, incident, equity, staffing and outcome indicators. Set thresholds and decision lead time. Reopen when a constraint fails, evidence changes recommendation, an unrepresented group experiences harm, organizational assumptions fail, or a credible superior/reversible option emerges. Create a superseding record; never edit history to make the old choice appear timeless.

The following executable teaching case evaluates three declared architectures on five normalized outcomes. It applies three mandatory thresholds before comparing three stakeholder-specific additive models. These declared numbers are illustrative; the checker does not establish real clinical safety, representativeness, lawful authority or acceptable values.

<!-- bijux-verify: {"id":"stakeholder-architecture-constraint-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"alternatives=3\nmandatory_constraints=3\ncentral_failures=outage_access\nedge_failures=safety\nhybrid_failures=none\neligible=hybrid\nauthority_winner=hybrid:84.3\noperator_winner=central:84.6\ncommunity_winner=hybrid:83.8\ncentral_min_stakeholder=77.6\nedge_min_stakeholder=74.3\nhybrid_min_stakeholder=82.2\nselected=hybrid\nstatus=constraints_before_preferences\nevidence=declared_teaching_values_only\n","stderr":""}} -->
```python
outcomes = {
    "central": {"safety": 90, "outage_access": 58, "privacy": 88,
                "maintainability": 92, "affordability": 84},
    "edge": {"safety": 79, "outage_access": 95, "privacy": 92,
             "maintainability": 58, "affordability": 61},
    "hybrid": {"safety": 88, "outage_access": 84, "privacy": 86,
               "maintainability": 78, "affordability": 75},
}
constraints = {"safety": 80, "outage_access": 75, "privacy": 80}
weights = {
    "authority": {"safety": .35, "outage_access": .25, "privacy": .20,
                  "maintainability": .10, "affordability": .10},
    "operator": {"safety": .25, "outage_access": .15, "privacy": .15,
                 "maintainability": .30, "affordability": .15},
    "community": {"safety": .25, "outage_access": .35, "privacy": .20,
                  "maintainability": .05, "affordability": .15},
}

def failures(architecture):
    return [name for name, minimum in constraints.items()
            if outcomes[architecture][name] < minimum]

def value(architecture, stakeholder):
    return round(sum(outcomes[architecture][name] * weight
                     for name, weight in weights[stakeholder].items()), 1)

print(f"alternatives={len(outcomes)}")
print(f"mandatory_constraints={len(constraints)}")
for architecture in outcomes:
    failed = failures(architecture)
    print(f"{architecture}_failures=" + (",".join(failed) if failed else "none"))
eligible = [architecture for architecture in outcomes if not failures(architecture)]
print("eligible=" + ",".join(eligible))
for stakeholder in weights:
    ranked = [(value(architecture, stakeholder), architecture) for architecture in outcomes]
    score, winner = max(ranked)
    print(f"{stakeholder}_winner={winner}:{score:.1f}")
for architecture in outcomes:
    minimum = min(value(architecture, stakeholder) for stakeholder in weights)
    print(f"{architecture}_min_stakeholder={minimum:.1f}")
selected = max(eligible,
               key=lambda architecture: min(value(architecture, stakeholder)
                                             for stakeholder in weights))
print(f"selected={selected}")
print("status=constraints_before_preferences")
print("evidence=declared_teaching_values_only")
```

The operator model ranks central highest, and that dissent remains relevant to staffing and maintainability. It cannot waive the approved outage-access constraint. Hybrid's selection is conditional on the declared thresholds, scales, weights and evidence; real decisions require validated scenarios, authorized preferences, uncertainty analysis and accountable acceptance.

## Definitions and Notation

Let the decision frame be

\[
\mathcal{D}=(Q,B,A,S,C,\Omega,X,E,P,R,H),
\]

where $Q$ is the question, $B$ baseline, $A$ authority structure, $S$ stakeholders, $C$ concerns/constraints, $\Omega$ scenarios, $X$ alternatives, $E$ evidence, $P$ preference structures, $R$ risks and $H$ decision history.

Architecture consequence $x_{a,s,c,\omega}$ is the evidenced outcome of alternative $a$ for stakeholder $s$, concern $c$ and scenario $\omega$. It carries an interval, distribution or evidence class when uncertainty matters; a point score must not erase that metadata.

The feasible set is $F\subseteq X$. For two feasible alternatives, $a$ dominates $b$ only if $a$ is no worse for every relevant comparable outcome and strictly better for at least one, with direction and uncertainty handled explicitly.

Stakeholder-specific regret in scenario $\omega$ can be inspected as

\[
r_s(a,\omega)=\max_{b\in F}V_s(b,\omega)-V_s(a,\omega).
\]

Minimizing maximum regret or maximizing minimum stakeholder value can illuminate robustness, but neither is automatically the authorized social-choice rule. Any aggregation rule embeds values and must be justified.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—frame and govern.** Fix the decision, baseline, authority, stakeholder/risk-taker system, participation and decision rules.

**Mechanism 2—translate values.** Link needs and concerns to scenarios, objectives, mandatory constraints, measures, preference functions and success conditions.

**Mechanism 3—create comparable architectures.** Develop whole alternatives with common boundary, fidelity, lifecycle and evidence basis; retain status quo, staging and pruning logic.

**Mechanism 4—challenge consequences.** Apply feasibility, stakeholder-specific values, distributions, risk, uncertainty, sensitivity, dominance, robustness, organizational feasibility and independent review.

**Mechanism 5—decide and learn.** Preserve recommendation, authority rationale, dissent and acceptance; baseline implementation; validate outcomes; monitor and supersede on triggers.

The reasoning supports a bounded conclusion only if stakeholder discovery, authority, evidence, scales, constraint classification and architecture descriptions are credible. No mathematical aggregator can repair excluded stakeholders, biased evidence, unlawful constraints, unsafe options or illegitimate authority.

## Alternatives and Trade-Offs

**Single aggregate value models** are compact and auditable when scales and trade assumptions hold. **Plural stakeholder models** expose disagreement and distribution but require accountable conflict resolution. Use a portfolio model only with legitimate authority and retain disaggregated results.

**Constraint-first screening** protects noncompensatory boundaries. It can also discard promising options when thresholds are poorly evidenced. Audit source, margin, uncertainty, waiver authority and redesign paths rather than weakening a boundary for convenience.

**Scenario workshops and qualitative matrices** discover concerns quickly. **Models, prototypes and field trials** provide stronger consequence evidence but cost time and can still omit rare conditions. Match evidence to decision consequence and use value of information.

**Centralized architectures** can improve consistency and operations efficiency but concentrate authority and failure. **Distributed architectures** can improve locality, autonomy and disrupted operation but multiply configuration, coordination and security burden. **Hybrid architectures** may balance conditions while adding synchronization and boundary complexity. Judge actual alternatives, not stereotypes.

**Early irreversible commitment** can protect schedule and price. **Staged modular commitment** preserves learning and exit options but can cost more and leave prolonged transition states. Treat reversibility and option value as architecture consequences.

**Broad transparency** enables participation and trust. **Controlled detail** protects privacy, security and procurement. Publish decision-capable rationale while restricting exploit, personal or commercial detail under accountable governance.

## Failure Modes and Misconceptions

**“All stakeholders are equal decision makers.”** Participation and impact matter, but authority, expertise, concurrence and risk acceptance have different legal and ethical roles.

**“The customer is the stakeholder.”** Customers do not exhaust users, operators, communities, regulators, maintainers, non-users or risk takers.

**“A weighted score resolves values objectively.”** Weights, scales, compensation and inclusion are value judgments; evidence uncertainty still applies.

**“Constraints are just high weights.”** A finite weight permits compensation. A mandatory boundary defines feasibility unless properly waived by authority.

**“The architecture with the best average is fairest.”** Averages can conceal an excluded subgroup, catastrophic tail or transferred labor.

**“Consensus validates the architecture.”** Agreement can reflect missing voices, power, vague options or shared error. Preserve dissent and evidence.

**“Technical authority owns stakeholder values.”** Technical authority protects technical integrity; legitimate preference and public-risk authority may sit elsewhere.

**“More views mean more stakeholder coverage.”** Views help only when concerns, scenarios, evidence and affected people are traced.

**“Hybrid is always the compromise.”** Hybrid can inherit both failure modes and add synchronization complexity. It must earn selection.

**“The decision ends at baseline.”** Implementation, outcomes and changed premises determine whether the rationale continues to hold.

## Worked Examples

### Example 1

**Rural clinical access.** Centralization meets cost and maintenance goals but fails a defined disrupted-care threshold for rural clinics. The failure remains visible rather than averaged against urban performance; hybrid staging tests synchronization, data age and local workload before commitment.

### Example 2

**Rail control.** Dispatch values network optimization; station staff value local degraded operation; safety authority imposes separation and fail-safe constraints. A federated fallback is selected with bounded local authority, configuration control and drills, not because stakeholder votes were equal.

### Example 3

**Public identity.** Agencies value fraud prevention and reuse; residents value minimization, contestability and service access. A centralized biometric option is rejected on legal/privacy constraints even though its aggregate convenience score is highest. Non-biometric fallback and appeal remain architectural elements.

### Example 4

**Microservices.** Product teams value release autonomy, while operators face incident coordination and users face cross-service latency. Workload traces, failure injection and on-call evidence reveal that a modular monolith dominates premature distribution for the current scale; a measured trigger preserves future decomposition.

### Example 5

**Flood warning.** Emergency managers value central message control, communities value multilingual accessible local relays, and telecom providers face congestion. A layered architecture is tested by geography, disability and outage condition; message transmission alone is not accepted as warning-to-action validation.

### Example 6

**Scientific data platform.** Researchers value open rapid access; participants and Indigenous data stewards require consent and governed reuse. Federated access controls and provenance add cost but satisfy noncompensatory obligations; a general openness score cannot override them.

### Example 7

**Factory maintenance.** Management prefers predictive cloud analytics; technicians need offline diagnosis and safe manual authority. Edge-safe control with advisory cloud models separates safety action from optimization, records added local maintenance and validates cognitive workload.

### Example 8

**Power microgrid.** Central optimization improves efficiency, but hospitals and shelters require islanding. A hierarchical architecture carries common-mode cyber, synchronization and operator-training risks; drills and black-start outcomes govern acceptance.

### Example 9

**Supplier platform.** Procurement prefers one discounted provider; engineering values portability; finance values cost certainty; operations values managed service. The decision includes contract, exit test, data egress, skill, concentration and acquisition-change triggers instead of treating price as architecture-neutral.

### Example 10

**No acceptable option.** Every proposed autonomous inspection architecture either misses worker-safety constraints or lacks evidence in the actual environment. The team recommends a protected pilot and new alternatives. A deadline does not turn an infeasible architecture into a responsible choice.

## Cross-Program Connections

**Platform engineering.** Platform topology distributes control, tenancy, toil, security, cost and developer autonomy. Treat adopter segments and operating teams as stakeholders and validate paved-road outcomes plus escape paths.

**API and service engineering.** Service boundaries and protocols allocate consistency, latency, ownership, compatibility and failure. Consumer groups, providers and operators require scenario-specific consequences and migration obligations.

**Data engineering.** Central lake, warehouse, mesh and federated designs distribute stewardship, access, privacy, quality, compute cost and incident burden. Data subjects and downstream decision takers matter alongside producers.

**Object-oriented programming.** Module boundaries, inheritance/composition and framework choices encode change authority and coupling. Quality scenarios and maintainer evidence prevent pattern preference from masquerading as architecture value.

**Functional programming.** Effect, state, type and concurrency architecture trades correctness arguments against ecosystem, performance, learning and operations. Preserve formal claims separately from workload and team evidence.

## References

1. NASA, *Systems Engineering Handbook, Section 4.1: Stakeholder Expectations Definition*, current web edition. <https://www.nasa.gov/reference/4-1-stakeholder-expectations-definition/>
2. NASA, *Systems Engineering Handbook, Section 4.2: Technical Requirements Definition*, current web edition. <https://www.nasa.gov/reference/4-2-technical-requirements-definition/>
3. NASA, *Systems Engineering Handbook, Section 4.3: Logical Decomposition*, current web edition. <https://www.nasa.gov/reference/4-3-logical-decomposition/>
4. NASA, *Systems Engineering Handbook, Section 4.4: Design Solution Definition*, current web edition. <https://www.nasa.gov/reference/4-4-design-solution-definition/>
5. NASA, *Systems Engineering Handbook, Section 6.8: Decision Analysis*, current web edition. <https://www.nasa.gov/reference/6-8-decision-analysis/>
6. NASA, *Systems Engineering Handbook, Section 6.7: Technical Assessment*, current web edition. <https://www.nasa.gov/reference/6-7-technical-assessment/>
7. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2022. <https://www.iso.org/standard/74393.html>
8. Carnegie Mellon Software Engineering Institute, *Architecture Analysis Techniques and When to Use Them*, CMU/SEI-2002-TN-005. <https://www.sei.cmu.edu/library/sei-architecture-analysis-techniques-and-when-to-use-them/>
9. NIST, *SP 800-160 Vol. 1 Rev. 1: Engineering Trustworthy Secure Systems*, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>
10. U.S. GAO, *DOE and NNSA Project Management: Analysis of Alternatives Could Be Improved by Incorporating Best Practices*, GAO-15-37. <https://www.gao.gov/products/gao-15-37>

## Exercises

### Exercise 1

The clinical-support example has only normalized point scores. Design the evidence and governance package required before an authority could use its safety, outage-access, privacy, maintainability and affordability values for a real regional decision.

### Exercise 2

A city selects between centralized, neighborhood-federated and hybrid heat-emergency response architectures. Cover older residents, unhoused people, multilingual communities, dispatch, clinics, utilities and privacy regulators. Define constraints, scenarios, distributions, evidence, authority, dissent and reopening.

### Exercise 3

An operator model ranks architecture A highest, a community model ranks B highest, and only architecture C passes all mandatory constraints. Explain when selecting C is justified, what cannot be inferred, and what conditions or evidence should accompany the choice.

### Exercise 4

Audit an architecture study with one detailed preferred alternative, two one-paragraph competitors, a 100-point weighted score, no status quo, averages across all users, supplier benchmarks, no operator model, and a statement that “stakeholders reached consensus.”

### Exercise 5

Design a supersession decision after a selected hybrid architecture experiences synchronization incidents, doubles operator workload, improves rural access, and faces a new privacy rule. Include preservation of competing values and downstream propagation.

## Answers to the Exercises

### Answer 1

Fix the question, authority, regional baseline, clinical functions, participating organizations, decision deadline, effective scope, reversibility and consequences of deferral. Identify clinicians by care setting and role, patients and advocates, rural/urban/mobile locations, safety and clinical governance, privacy/security, operations/on-call, maintainers, integrators, funders, suppliers, regulators and people unable to use digital services. State representation and missing voices; distinguish recommender, decision authority, safety/privacy concurrence and risk takers.

Turn the five labels into scenarios and measures. Safety evidence includes correct/incorrect/missed/late alerts, stale-model behavior, interaction effects and severity under representative and rare clinical conditions. Outage access covers duration, region, device, local data/model age, response and safe fallback. Privacy covers data flows, minimization, access, inference, retention, breach and lawful basis. Maintainability includes change failure, patch/configuration latency, cognitive load, on-call pages, diagnostic time and skill. Affordability uses lifecycle acquisition, integration, connectivity, staffing, incident, migration, exit and decommissioning cost with uncertainty.

Define mandatory clinical-safety, access, privacy, security and legal constraints with sources, margins, evidence and waiver/acceptance roles. Build central, edge, hybrid, status-quo, staged and fallback architectures at comparable fidelity: ConOps, allocation, trust boundaries, synchronization, failure/recovery, deployment, staffing, training and migration. Use controlled workload/clinical datasets, hazard analysis, threat/privacy assessment, prototypes, outage/failure injection, field observation, accessibility/usability studies, cost/schedule models and independent review. Record provenance, population/configuration, conflicts, uncertainty and limitations.

Do not treat the normalized teaching values as measurements. Define scales and preference functions, elicit stakeholder-specific weights under legitimate authority, test compensation/independence, retain distributions, and analyze thresholds, correlation, tails, rank reversal and value of information. Preserve operator and community results even under a portfolio model. Recommendation and final decision must explain tradeoffs, dissent, residual risks and conditions.

Implementation needs owners, funding, architecture/configuration artifacts, requirements/interfaces, safety/security/privacy controls, synchronization and data-age indicators, staffing/training, staged sites, contingency/rollback and communication. Verify conformance; validate safety, access, privacy, workload and lifecycle cost by group and adverse scenario. Reopen on incident/near miss, constraint breach, subgroup harm, model/data/workload/site/provider/regulatory change, workload threshold, cost overrun or better evidence. Preserve the signed record and source snapshots.

### Answer 2

Frame the capability as preventing heat illness/death and connecting people to cooling, clinical and emergency support across specified neighborhoods, temperatures, durations and service states—not as choosing an app. Name emergency/public-health authority, municipal service owners, clinical and utility roles, privacy/legal/security concurrence, community representatives and actual people bearing access, surveillance and response risk. Establish urgent-decision and dissent escalation paths.

Baseline heat/humidity and urban-island maps, housing, language/literacy, disability, health vulnerability, homelessness and informal occupancy, phone/connectivity, power, transport, cooling centers/capacity, clinic/EMS demand, field staff, privacy law, trust and misinformation. Scenarios include forecast escalation, grid/cellular outage, night, simultaneous neighborhoods, cooling-center saturation, unreachable residents, false positive/negative, data error, hostile misuse and recovery. Measure warning-to-action, reach/comprehension, safe transport/cooling, clinical load, subgroup delay, false dispatch, privacy exposure, staff workload, reliability and lifecycle cost.

Noncompensatory constraints might include timely life-safety response for defined high-risk conditions, accessible multilingual alternatives, non-digital access, safe worker dispatch, lawful/minimized data use, authenticated commands and protection of clinical data. Specify sources and authorities. Compare centralized dispatch, neighborhood federation, hybrid coordination, status quo/manual augmentation, staged pilots and fallback at common fidelity, including community partners, utilities, clinics, transport, staffing, training and power/communications dependencies.

Evidence includes historical incidents, environmental and health data, coverage/propagation, queue and capacity simulation, outage exercises, delivery telemetry, field accessibility/comprehension studies, community evidence, privacy threat assessment, staffing/cost schedules and uncertainty/sensitivity. Report distributions by geography, housing, language, disability and connectivity; do not let excellent central averages compensate for an unreached high-risk group.

Record stakeholder-specific models and conflicts. Dispatch may prefer central visibility; neighborhoods may prefer trusted local action; privacy authority may constrain individual tracking. Preserve recommendation, final authority rationale, dissent, accepted false-negative/positive, overload, privacy, worker-safety and inequity risks, plus funding and conditions. Validate end-to-end health/access outcomes through drills and heat events. Reopen on climate/hazard, population, infrastructure, law, capacity, trust, incident, inequity, workload, cost or evidence change.

### Answer 3

Selecting C is justified only if the constraints are validly sourced, applicable, sufficiently evidenced and authorized; C is demonstrably feasible with adequate margin; A and B cannot be redesigned or properly waived within the decision; and C's residual risks and implementation burdens are acceptable to the responsible authorities and risk takers. Constraint-first selection prevents one stakeholder's preference benefit from compensating for a mandatory failure.

It does not prove that C is globally optimal, fair, successful, robust or preferred by a majority. It does not establish that the stakeholder models are representative, that the point evidence is accurate, that constraint thresholds are ethical, or that C will work organizationally. It cannot erase the operator's A rationale or community's B rationale. If the constraints were mislabeled preferences, politically manipulated, or based on weak evidence, automatic selection would be unsound.

Record each constraint's source, threshold, margin, evidence, uncertainty, applicability, concurrence and waiver path. Show A/B failure modes, redesign attempts and reopen triggers. For C, preserve stakeholder-specific consequences, worst group/scenario, tail/common-cause risks, readiness, staffing/cognitive load, lifecycle cost and reversible staging. Conditions can include targeted prototypes, representation gaps closed, safety/privacy review, training/resources, fallback/rollback, monitoring and outcome thresholds. The authority explains why feasibility governs now, dispositions dissent without inventing consensus, and schedules reassessment when evidence or constraints change.

### Answer 4

Stop the selection claim. The study has asymmetric alternative maturity, so its scores compare description quality as well as architecture. Define a common system boundary, baseline, ConOps, scenarios, functions, interfaces, enabling systems, maturity, operations, transition and lifecycle for every alternative. Add status quo, defer/information, staged/reversible, combination and fallback options; reconstruct generation/pruning without fabricating missing history.

Audit the 100-point model: criterion definitions and direction, constraint misclassification, scale/utility meaning, preference authority, weight elicitation, double counting/correlation, additive independence, normalization, missing data, false precision, uncertainty and sensitivity. Preserve raw evidence and calculations. A total cannot replace architecture-specific failure, risk and rationale.

Disaggregate “all users” by materially different context, access, geography, ability, workload and exposure. Inspect minimum, distribution, threshold, tail and common-cause outcomes. Add operators, maintainers, integrators, non-users, regulators and risk takers. Supplier benchmarks require workload/configuration equivalence, methods, raw data, conflicts and independent replication; marketing results are not neutral field evidence.

Determine who participated, who was absent, how representatives were chosen and what “consensus” meant. Locate attributable disagreements and protect dissent; do not backfill unanimity. Re-run comparable scenario evaluation, constraint screening, stakeholder-specific preference analysis, organizational feasibility, risk/readiness, sensitivity and independent challenge. Preserve the old study as evidence with limitations. Create a governed new recommendation and authority decision, implementation/outcome plan and triggers rather than editing the record until it appears credible.

### Answer 5

Create a new decision ID that cites and potentially supersedes the original; retain the earlier record, its baseline, evidence, values, choice and historical validity. State exact incident configurations, frequency/severity, affected data/actions/sites and causal uncertainty; quantify operator workload by role/shift and consequences; measure rural access gains by population/condition; cite the new privacy rule, effective date, interpretation and authority. Distinguish implementation defect, operating drift, scale effect and architecture premise failure.

Reopen the original alternatives and generate redesigns: corrected synchronization protocol, bounded-local-authority changes, central fallback, redesigned edge or hybrid partitions, privacy-preserving data allocation, staffing/automation, staged rollback, supplier changes, and information acquisition. Keep safety/access/privacy constraints separate from preferences. Re-elicit only values legitimately changed; do not alter old weights to justify current preferences. Preserve rural benefits, operator dissent/burden, privacy-risk takers, clinical safety and affordability distributions.

Use controlled incident traces, fault injection/model checking where applicable, field access outcomes, workflow/cognitive studies, privacy threat and legal assessment, staffing/cost models and migration tests. Analyze common cause, stale/conflicting state, recovery, peak workload, subgroup loss, uncertainty and sensitivity. Record technical recommendation, authority decision, privacy/safety concurrence, dissent, residual risks, conditions and whether a temporary containment is an acceptance or mitigation.

Propagate the superseding decision through stakeholder expectations, ConOps, requirements, architecture views/models, allocations, data/control/interface contracts, privacy/security/safety cases, configurations, code/infrastructure, supplier contracts, staffing/training, verification/validation, migration/rollback, risks and downstream decisions. Verify the new configuration, then validate synchronization safety, rural access, operator workload, privacy compliance, lifecycle cost and recovery. Monitor incident, near-miss, workload, access inequity, privacy finding, scale, provider and evidence triggers; retain both records and their signed approvals.
