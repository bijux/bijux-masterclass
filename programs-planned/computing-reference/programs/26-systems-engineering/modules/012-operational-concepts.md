---
module_id: SYSENG-012
program: Systems Engineering
level: 1
module_number: 12
title: Operational Concepts
status: complete
last_verified: 2026-08-30
---

# Operational Concepts

## One-Page Review

### Governing question

How can stakeholders describe an envisioned way of operating—across people, organizations, systems, modes, environments, support, failure, transition, and retirement—deeply enough to govern requirements and validation without prematurely selecting the design?

### Essential definitions

- An **operational concept** is a verbal and graphical statement of organizational intent and assumptions about an operation or related operations from user and operator perspectives.
- A **concept of operations (ConOps)** is the governed description of how an organization expects a system or related systems to be employed to achieve objectives in an operational environment.
- **Current operations** describe the evidenced present situation, including workarounds and inherited constraints; **target operations** describe the intended future situation; **transition operations** connect them.
- An **operational role** groups responsibilities, authority, information, workload, and competence independently of a named person or implementation component.
- An **operational mode** is a condition in which allowed behavior, interfaces, responsibilities, measures, or constraints differ materially.
- An **operational thread** is an end-to-end sequence of roles, interactions, decisions, resources, and states that produces or protects an outcome.
- An **operational measure** evaluates mission or stakeholder outcome; it is not automatically a technical performance requirement.
- A **support concept** explains how the capability is provisioned, staffed, trained, supplied, monitored, maintained, recovered, upgraded, and retired.
- A **design commitment** selects a realization; an **operational commitment** constrains behavior or responsibility because the operating model requires it.
- An **operational baseline** is a versioned concept accepted by named authority as adequate for a defined decision, not a claim of permanent completeness.

### Central model, mechanism, or theorem

Model the concept as a decision-bounded set:

$$
C=\langle purpose,scope,stakeholders,roles,context,current,target,transition,
modes,threads,interfaces,support,measures,assumptions,constraints,risks,trace,evidence\rangle.
$$

For every important operational claim $c_i$, preserve:

$$
c_i \Leftarrow source_i + rationale_i + authority_i,
\qquad c_i \Rightarrow needs_i + requirements_i + validation_i.
$$

Concept adequacy is conditional:

$$
Adequate(C,D) \iff Coverage(C,D) \land Consistency(C)
\land FeasibilityEvidence(C,D) \land Authorized(C,D),
$$

where $D$ is the named decision. The predicate disciplines review; populated fields do not prove that stakeholders, conditions, or futures are complete.

### Critical invariants

- State whose concept it is, which system/organization boundary it addresses, and which decision it supports.
- Separate observed current operations, proposed target operations, and transition operations.
- Keep stakeholder outcomes and operational responsibilities visible while preserving multiple realizations.
- Cover nominal, peak, degraded, emergency, maintenance, update, migration, shutdown, and retirement where relevant.
- Assign decision rights, handoffs, information, workload, and recovery to roles; do not hide human work behind “the user.”
- Include enabling systems, facilities, supply, staffing, training, data, energy, communications, authority, and disposal.
- Trace claims to sources and trace resulting needs, requirements, architecture questions, hazards, and validation evidence back to the concept.
- Record assumptions, unresolved issues, risks, dissent, and feasibility evidence beside the operation they affect.
- Use measures tied to stakeholder outcomes and operational context, including distribution and adverse consequences.
- Rebaseline when mission, stakeholders, environment, law, dependencies, architecture, or operational evidence changes materially.

### Common failures

Failures include treating ConOps as a glossy vision; documenting only the product rather than the operating system; copying current procedures into the target; writing a UI walkthrough; confusing a scenario set with the whole concept; selecting vendors or components without authority; omitting support and transition; assuming unlimited staff, data, network, power, or competence; hiding authority at handoffs; covering only happy paths; using averages that conceal vulnerable populations or peaks; turning every concept sentence into a requirement; and freezing an early concept after operations invalidate it.

### Compact example

A hospital requests “automated discharge.” A defensible operational concept describes the outcome—safe, timely continuity of care—and the coordinated future operation among patient, caregiver, clinician, pharmacy, transport, home-care provider, insurer, records, interpreter, support, and emergency services. It covers consent, medication reconciliation, accessibility, pending results, unavailable services, failed contact, readmission, audit, staffing, training, downtime, and transition from present work. Automation remains one allocation candidate. The concept exposes what must happen and who remains accountable before architecture selects how.

### Connections

Retrieve context and scenarios from SYSENG-009, problem framing from SYSENG-010, and stakeholder needs from SYSENG-011. Continue to functional, performance, regulatory, quality, decomposition, allocation, traceability, and change modules. Later architecture, human factors, safety, resilience, validation, lifecycle, and systems-of-systems modules deepen the concept.

## Governing Question

Requirements assign obligations to a system, but stakeholders first need a shared account of the operation in which those obligations make sense. Who acts? What do they know? Which organization decides? What resources and enabling systems exist? How does work change across modes? What happens before deployment, during degraded service, after an incident, and at retirement? An operational concept joins these questions into a coherent future operation.

The governing question is not “what document template should we fill?” It is how to create decision-quality agreement about intended operation without pretending that a narrative guarantees feasibility or smuggling architecture into needs. A useful concept is simultaneously descriptive, exploratory, traceable, challengeable, and revisable.

## Why This Matters

Systems fail operationally even when individual components meet their specifications. A queue forms because staffing and arrival assumptions disagree. An alarm is correct but no role owns acknowledgment. A cloud service is available while identity, network, or support is not. A medical device reports a value but nobody knows who evaluates drift. These are failures of the envisioned operating model and its translation, not merely component defects.

ISO/IEC/IEEE 29148 treats operational concepts and scenarios as important requirements-engineering information. NASA places ConOps after initial stakeholder expectations and before detailed requirements and architecture: walking through intended operations can reveal missing functions, human/system allocation, interfaces, support, facilities, staffing, and safeguards. NASA's annotated outline spans background, scope, assumptions, envisioned elements, interfaces, modes, capabilities, physical and support environments, nominal and off-nominal scenarios, impacts, risks, and closeout.

Terminology varies. Some communities distinguish organization-level ConOps from a system-focused operational concept or later operations plan; others use the terms interchangeably. Define local meanings and artifact relationships. The durable test is whether readers can understand, challenge, and trace the intended operation at the appropriate level without mistaking it for design or procedure.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. a system boundary is chosen for a concern, viewpoint, configuration, and lifecycle stage;
2. stakeholder needs state outcomes in context and preserve source, rationale, conflict, and uncertainty;
3. scenarios animate roles and interfaces through time but do not alone define governance, support, or the complete concept;
4. assumptions and external dependencies need owners, evidence, triggers, and consequences;
5. measures of effectiveness address mission or stakeholder outcomes, not component performance alone;
6. solution neutrality preserves alternatives unless a justified operational or external constraint narrows them;
7. validation evaluates the realized capability in representative operational context.

As a retrieval test, consider “the platform operates continuously.” Ask which outcome requires continuity, which populations and regions matter, which dependencies are assumed, which degraded services remain acceptable, who declares incidents, who can isolate a tenant, how maintenance occurs, what records survive, and how users recover. Until those questions are answered, “continuous” is neither an operational concept nor a testable requirement.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish operational concept, ConOps, scenario, use case, procedure, operations plan, requirement, and architecture;
2. set the purpose, scope, viewpoints, decision, authority, and baseline for a concept;
3. separate current, target, and transition operations using evidence and explicit assumptions;
4. model roles, responsibilities, decision rights, information, workload, and handoffs;
5. integrate modes, threads, interfaces, environments, support, and lifecycle concerns;
6. expose human/system allocation questions without prematurely making design commitments;
7. derive and trace candidate needs, requirements, hazards, architecture questions, and validation conditions;
8. evaluate operational feasibility, consistency, coverage, and outcome measures;
9. govern alternatives, dissent, risk, change, and operational learning;
10. state the limits of documents, models, automated checks, and internal review.

## Core Exposition

**Begin with artifact purpose and decision.** A concept prepared to align stakeholders differs from one supporting a concept review, acquisition boundary, architecture trade, regulatory engagement, or operational transition. Record owner, approving authority, intended readers, system and organizational scope, lifecycle horizon, decisions supported, exclusions, and update triggers. “Describe the future service” is too vague to govern depth.

**Define local terminology.** State whether ConOps is organization-level intent, operational concept is system-focused elaboration, and operations plan is the later executable plan. Explain relationships to mission/business analysis, stakeholder needs, scenarios, architecture, requirements, validation, procedures, and training. Terminology disputes matter less than ambiguous ownership or hidden gaps.

**Establish the current operational baseline.** Use observation, interviews, process and data traces, incident reports, workload studies, policies, interfaces, support records, and outcomes. Distinguish prescribed work from work as performed. Record workarounds because they reveal resilience and unmet need, but do not canonize unsafe or inequitable practice. State evidence periods and missing populations.

**Describe the target as an operating model.** Start with mission outcomes and principles, then identify roles, responsibilities, authority, information, resources, locations, timing, modes, external relationships, and end states. Describe what must be operationally true, not screens, classes, deployment products, or favored vendors. Where a physical or technical choice is already constrained, cite its authority and retain the underlying outcome.

**Design transition operations explicitly.** Current and target operations do not connect automatically. Cover pilots, parallel operation, migration cohorts, data and identity reconciliation, training, certification, supplier onboarding, facilities, temporary staffing, cutover authority, rollback, legacy support, communication, incident response, and decommissioning. Transition may have greater risk and workload than steady state.

**Model roles rather than generic users.** For each role, record objectives, responsibilities, decision rights, required information, outputs, competence, workload, location, tools, collaboration, escalation, and liability. One individual can hold several roles and one role can be distributed. Include beneficiaries, affected non-users, operators, maintainers, responders, administrators, auditors, suppliers, and authorities.

**Make authority observable.** A handoff must state who may initiate, approve, reject, override, suspend, and close an operation; what evidence they receive; and how conflicts escalate. Responsibility without authority creates delay and moral hazard. Automation does not eliminate authority: it reallocates decision, monitoring, intervention, and accountability.

**Structure operational modes.** Modes exist when permissions, behavior, interfaces, staffing, measures, or risk controls change. Define entry and exit events, guards, responsible role, allowable/prohibited capabilities, information continuity, observability, and failed transitions. Include initialization, normal, peak, degraded, emergency, maintenance, calibration, update, training, migration, shutdown, and disposal only where material.

**Use end-to-end operational threads.** A thread begins with a meaningful trigger and ends when outcomes, records, resources, hazards, custody, and obligations are settled. Connect roles, decisions, interfaces, modes, timing, alternate paths, failure, and recovery. Scenario detail from SYSENG-009 supports the thread; the concept also supplies the surrounding governance, support, measures, and lifecycle rationale.

**Cover the operational ecosystem.** Include other systems, organizations, facilities, natural environments, networks, energy, material, transport, identity, payment, data sources, policy, markets, supply, emergency services, and disposal. State ownership, service assumptions, interface semantics, capacity, quality, timing, failure behavior, and exit options. Calling an element “external” does not remove its impact.

**Develop the support concept.** Explain provisioning, configuration, monitoring, staffing, scheduling, training, help, spares, consumables, calibration, repair, patching, recovery, audit, incident investigation, knowledge transfer, upgrade, obsolescence, and disposal. State what support can observe and control, access constraints, service horizons, and return-to-service authority. Support is system operation, not overhead.

**Expose human/system allocation questions.** For each activity, ask what judgment, perception, dexterity, adaptation, speed, consistency, memory, or scale is required; what information is available; and what failure consequences follow. Keep “human decides” and “system decides” as alternatives until evidence supports allocation. If automation is proposed, include supervision, uncertainty, override, deskilling, workload migration, and recovery.

**Describe information and material custody.** Operational success depends on semantics, provenance, timeliness, quality, access, consent, retention, reconciliation, and deletion—not data flow alone. Physical systems also transfer material, energy, waste, samples, tools, and hazardous items. At every handoff, state custody, condition, acceptance evidence, exceptions, and unresolved obligations.

**Define measures in context.** Link each measure to an outcome, stakeholder, scenario/mode, population, time window, observation method, uncertainty, target direction, and adverse guardrail. Average completion time can conceal abandoned users or unsafe shortcuts. Pair effectiveness with resource, distribution, safety, security, environmental, and recovery measures where appropriate. Provisional thresholds remain explicitly unresolved.

**Record assumptions, constraints, risks, and issues.** An assumption is not true because it appears in a baseline. Give each item source, rationale, confidence, owner, validation method, deadline, trigger, consequence, and mitigation. Separate true external constraints from preferences. Link risks to affected threads and decisions so a narrative cannot hide infeasibility.

**Explore alternatives at operational level.** Compare centralized versus local authority, staffed versus self-service operation, continuous versus scheduled service, preventive versus corrective support, progressive versus single cutover, and manual versus automated allocation. Evaluate outcome, burden, feasibility, resilience, distribution, governance, lifecycle cost, and reversibility before selecting architecture.

**Derive downstream obligations carefully.** A concept statement can produce candidate needs, functions, performance conditions, interface questions, hazards, constraints, support requirements, architecture decisions, verification cases, and validation environments. Preserve transformation rationale. Do not convert every narrative sentence into a `shall`; background, assumption, example, objective, and requirement play different roles.

**Review with operational evidence.** Use role walkthroughs, tabletop exercises, prototypes, models, simulations, workload analysis, dependency and hazard review, supplier/authority consultation, pilot operations, and representative user evaluation. Challenge missing roles, peak load, contradictory authority, degraded dependencies, exceptional populations, transition burden, and recovery. High-consequence claims need applicable independent domain review.

**Baseline conditionally and evolve.** Record unresolved items and the decision for which the concept is adequate. Configuration-control the artifact and its models. Revisit it when needs, regulation, environment, suppliers, architecture, incidents, workload, measures, or organizational authority change. Actual operations provide evidence that may invalidate the original concept.

**Use automated checks only for declared structure.** The checker below identifies absent current/transition views, modes, support, measures, and unresolved assumptions in four concept records. It cannot judge whether the operation is desirable, feasible, representative, safe, legal, or complete.

<!-- bijux-verify: {"id":"operational-concept-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"concepts_total=4\nwell_formed_declared=1\nmissing_current=C-transit\nmissing_transition=C-clinical\nmissing_modes=C-transit\nmissing_support=C-warehouse\nmissing_measures=C-clinical\nunresolved_assumptions=C-warehouse\nconcept_set_ready=false\nevidence=declared_fields_only\n","stderr":""}} -->
```python
concepts = [
    {"id": "C-water", "current": ["manual sampling"], "target": ["risk-based response"],
     "transition": ["parallel validation"], "modes": ["normal", "contamination"],
     "support": ["laboratory", "field maintenance"], "measures": ["safe restoration time"],
     "assumptions": []},
    {"id": "C-transit", "current": [], "target": ["equitable fare access"],
     "transition": ["dual media"], "modes": [], "support": ["rider support"],
     "measures": ["successful journeys"], "assumptions": []},
    {"id": "C-clinical", "current": ["manual triage"], "target": ["supported triage"],
     "transition": [], "modes": ["normal", "surge"], "support": ["clinical governance"],
     "measures": [], "assumptions": []},
    {"id": "C-warehouse", "current": ["picker-directed work"], "target": ["coordinated work"],
     "transition": ["zoned pilot"], "modes": ["normal", "evacuation"], "support": [],
     "measures": ["safe fulfilled orders"], "assumptions": ["network always available"]},
]

required = ("current", "target", "transition", "modes", "support", "measures")
complete = [c["id"] for c in concepts if all(c[field] for field in required) and not c["assumptions"]]
missing_by_field = {
    field: sorted(c["id"] for c in concepts if not c[field])
    for field in ("current", "transition", "modes", "support", "measures")
}
unresolved = sorted(c["id"] for c in concepts if c["assumptions"])

print(f"concepts_total={len(concepts)}")
print(f"well_formed_declared={len(complete)}")
for field, missing in missing_by_field.items():
    print(f"missing_{field}={','.join(missing) or 'none'}")
print(f"unresolved_assumptions={','.join(unresolved) or 'none'}")
print(f"concept_set_ready={str(len(complete) == len(concepts)).lower()}")
print("evidence=declared_fields_only")
```

## Definitions and Notation

Let $C$ be an operational-concept baseline and $D$ its supported decision. Let $R_o$ be operational roles, $M$ modes, $T$ operational threads, $E$ external/enabling entities, $S$ support capabilities, and $Q$ operational measures.

For a role $r$:

$$
r=\langle objectives,responsibilities,authority,information,actions,
competence,workload,handoffs,escalation,evidence\rangle.
$$

For a mode transition $m_i\rightarrow m_j$:

$$
\tau=\langle trigger,guard,authority,actions,stateTransfer,observability,
failure,recovery,endState\rangle.
$$

Let $Trace(x,y,\rho)$ mean artifact element $x$ supports element $y$ with recorded rationale $\rho$. A link without rationale is navigational, not evidence of faithful transformation. Let $Obs(q,p,t)$ mean measure $q$ is observed for population/context $p$ over horizon $t$; it does not imply causal attribution.

Use **ConOps** only with the locally declared meaning. **OpsCon**, **operational concept**, and **operations concept** have community-specific meanings. A **use case** emphasizes actor/system interaction for a goal; a **scenario** is a concrete sequence; a **procedure** directs executable work; an **operations plan** assigns detailed resources and schedules. None substitutes automatically for the whole concept.

## Mechanisms, Invariants, or Proof Structure

The principal mechanism is iterative translation. Stakeholder outcomes constrain the intended operation; operational walkthroughs expose missing or conflicting needs; the agreed operation motivates requirements and architecture questions; feasibility evidence may revise the concept; validation later evaluates the realized operation against outcomes.

For each critical thread $t$, require coverage across roles, modes, interfaces, environment, support, hazards, measures, and lifecycle:

$$
Cover(t)=Roles(t)\land Modes(t)\land Interfaces(t)\land Support(t)
\land Failure(t)\land Measures(t)\land Trace(t).
$$

This is an audit schema, not a completeness theorem. Review must still ask whether the thread set and axes omit unknown or politically excluded concerns.

Maintain five invariants. **Purpose invariant:** content remains tied to the named decision. **Temporal invariant:** current, transition, and target claims never blur. **Responsibility invariant:** every important action and handoff has accountable authority. **Lifecycle invariant:** operation includes enabling and support work through retirement. **Evidence invariant:** claims, assumptions, selections, and validation conditions retain provenance and limits.

Feasibility is multi-dimensional. Operational, technical, organizational, economic, schedule, legal, ethical, safety, security, environmental, and supplier feasibility can fail independently. A simulation may support capacity while saying nothing about training time or legitimate authority. Evidence should therefore be typed and matched to the claim.

## Alternatives and Trade-Offs

**Narrative versus model.** Narrative conveys intent and rationale; diagrams expose structure; scenarios expose time; tables expose consistency; executable models explore dynamics. Use a coherent set with authoritative ownership rather than expecting one representation to do everything.

**One concept versus viewpoint set.** A compact product may use one artifact. A complex socio-technical system benefits from mission, user, operator, support, security, safety, data, transition, and retirement views. Multiple views improve focus but require terminology, identity, and consistency control.

**Current-led versus outcome-led design.** Current-led concepts preserve feasibility and local knowledge but can fossilize dysfunction. Outcome-led concepts open alternatives but can ignore real constraints and transition burden. Use evidence from current work to inform, not dictate, an outcome-led target.

**Broad versus detailed.** Too broad hides decisions; too detailed hardens design and becomes obsolete. Select depth by decision and risk. Detail high-consequence handoffs, modes, dependencies, and support while leaving realization alternatives open.

**Single target versus alternatives.** One target communicates clearly but may manufacture consensus. Parallel operational concepts expose genuine choices in authority, staffing, service level, automation, and transition. Narrow only with explicit criteria, evidence, affected stakeholders, and authority.

**Document baseline versus living model.** A controlled baseline supports accountability; a living model supports learning. Combine them through versioned baselines, change records, synchronized views, and operational triggers rather than choosing stasis or uncontrolled editing.

## Failure Modes and Misconceptions

1. **“ConOps is a vision statement.”** A slogan lacks roles, modes, interfaces, support, measures, risk, and traceability.
2. **“The scenario chapter already is the ConOps.”** Scenarios are dynamic views; the concept also governs intent, scope, authority, ecosystem, support, transition, and measures.
3. **“Current procedure defines need.”** Current work contains valuable evidence and inherited dysfunction; distinguish both.
4. **“Solution-neutral means technically empty.”** State required operational behavior, responsibility, information, timing, and conditions without selecting unjustified realization.
5. **“External systems are out of scope.”** They remain operational dependencies with assumptions, interfaces, failure, and ownership.
6. **“Automation removes human work.”** It shifts work into supervision, exception handling, training, governance, maintenance, and recovery.
7. **“Nominal operation establishes feasibility.”** Peak, degraded, emergency, transition, support, and retirement can dominate outcome and cost.
8. **“A signed baseline is true.”** Approval establishes authority for a decision, not empirical truth or permanent completeness.
9. **“Every sentence becomes a shall.”** Distinguish context, rationale, objective, assumption, constraint, example, and obligation.
10. **“The checker validated the concept.”** It inspected declared fields only; semantic and consequential judgments remain human and evidence-dependent.

## Worked Examples

### Example 1

**Situation.** A city proposes app-only transit fares. The draft describes registration, purchase, and inspection screens. **Reasoning.** That is a solution walkthrough. Reframe the outcome as equitable access to valid travel. Model riders with and without banking, smartphones, connectivity, language fluency, or dexterity; inspectors, support, finance, privacy, accessibility, and operations. Current cash/card practices, target access, dual-media transition, network-loss mode, refunds, device failure, fraud disputes, settlement, staffing, and retirement belong in the concept. **Conclusion.** The app can remain an alternative only after the operating model preserves access, authority, support, and degraded operation.

### Example 2

**Situation.** A warehouse automation concept assumes the network is continuously available. **Reasoning.** Trace the assumption into allocation, worker direction, collision avoidance, inventory custody, evacuation, and restart. Define degraded and emergency modes, local authority, observable state, work suspension, manual recovery, reconciliation, and maintenance. Test network partitions under peak workload; do not infer safety from nominal throughput. **Conclusion.** “Always available” becomes a governed assumption with evidence and mitigation, not an invisible premise.

### Example 3

**Situation.** A hospital wants automated clinical triage. **Reasoning.** Separate current intake evidence from target outcomes: timely, equitable prioritization with clinical accountability. Model patient, caregiver, nurse, physician, interpreter, emergency, privacy, support, and model-governance roles. Cover missing data, uncertainty, surge, conflicting indicators, override, appeal, monitoring, drift, downtime, and incident review. Compare advisory, bounded automation, and autonomous allocations under clinical authority. **Conclusion.** The concept may justify decision support; it cannot establish clinical safety or benefit without representative clinical evidence and applicable review.

### Example 4

**Situation.** A utility replaces a water-quality process in one cutover. **Reasoning.** The target concept is plausible, but transition lacks sample correlation, instrument calibration, staff qualification, laboratory interfaces, historical baseline, public communication, rollback, and legacy record custody. A parallel-validation period with discrepancy authority and acceptance criteria makes transition observable. **Conclusion.** Transition operation is a first-class concept, not a project-management footnote.

### Example 5

**Situation.** A platform team promises developer self-service. **Reasoning.** “Self-service” can transfer toil and risk. Specify consumer journeys, permitted autonomy, policy evidence, quotas, costs, support, escalation, incident ownership, exception paths, deprecation, and offboarding. Measure lead time together with failure recovery, support demand, accessibility, security exceptions, and team distribution. **Conclusion.** The operational concept defines a product relationship and shared responsibility before portal architecture.

### Example 6

**Situation.** A railway alarm is delivered to the control room, but two roles assume the other acknowledges it. **Reasoning.** Model issuance, receipt, interpretation, acknowledgment, escalation, intervention, clearance, and audit across normal, handoff, overload, and communication-loss modes. Assign authority and time bounds; expose what each role can observe. Derive candidate interface, staffing, training, and verification obligations. **Conclusion.** Message delivery is not operational closure; ownership and end state complete the thread.

### Example 7

**Situation.** A disaster-response concept uses average cellular coverage. **Reasoning.** Average coverage hides geography, congestion, device access, power loss, disability, institutional settings, and displaced populations. Define affected populations and emergency contexts; compare cellular, broadcast, local relay, physical outreach, and responder-assisted alternatives. Measure receipt, comprehension, action, false-alert harm, and recovery distributions. **Conclusion.** Operational measures must be context- and population-indexed; a network average cannot validate public warning.

### Example 8

**Situation.** A supplier-operated identity service is labeled “external” and omitted. **Reasoning.** Authentication, authorization, revocation, support, audit, privacy, outage, compromise, contract change, migration, and exit affect every protected thread. Record provider and acquirer roles, service assumptions, evidence, escalation, degraded behavior, data/key custody, and replacement concept. **Conclusion.** External ownership changes authority and control; it does not remove operational responsibility.

### Example 9

**Situation.** Two operational alternatives compete: central approval versus bounded local authority for field repairs. **Reasoning.** Central approval improves consistency and specialist oversight but adds communication dependency and delay. Local authority improves resilience and speed but requires competence, limits, evidence, and later reconciliation. Evaluate consequence, reversibility, environment, connectivity, workload, training, audit, and escalation. A hybrid can pre-authorize bounded actions with safe-state rules. **Conclusion.** Compare operating models before encoding either authority structure in architecture.

### Example 10

**Situation.** A satellite mission ConOps ends after normal operations. **Reasoning.** Add commissioning, safe mode, ground/flight handoff, anomaly response, patching, fuel and orbital constraints, knowledge transfer, end-of-mission data custody, passivation, disposal, and long-term tracking. Trace roles and evidence when contact is intermittent and recovery irreversible. Internal analysis cannot certify orbital safety or regulatory compliance. **Conclusion.** Whole-lifecycle operation includes closeout obligations, and high-consequence claims require independent applicable authority.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) translates operational language, roles, policies, and events into bounded domain models.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) uses operational scenarios, quality concerns, constraints, and deployment/support assumptions to compare structures.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) governs information provenance, quality, custody, reconciliation, retention, and operational observability.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) introduces adversarial conditions, protection authority, incident operation, and recovery into every relevant mode.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) turns cross-boundary operational interactions into explicit service responsibilities and contracts.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) treats developers, operators, governance, and support as participants in a platform operating model.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, 2023. Consulted 2026-08-30.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, 2018. Consulted 2026-08-30.
3. NASA. [*NASA Systems Engineering Handbook*, Rev. 2](https://www.nasa.gov/reference/systems-engineering-handbook/), NASA/SP-2016-6105 Rev2, 2016. Consulted 2026-08-30.
4. NASA. [System Design Processes](https://www.nasa.gov/reference/4-0-system-design-processes/), including Concept of Operations and Support Strategies. Consulted 2026-08-30.
5. NASA. [Systems Engineering Handbook Appendix](https://www.nasa.gov/reference/system-engineering-handbook-appendix/), Appendix S: Concept of Operations Annotated Outline. Consulted 2026-08-30.
6. SEBoK Editorial Board. [Operational Concept](https://sebokwiki.org/wiki/Operational_Concept_%28glossary%29), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-30.
7. SEBoK Editorial Board. [Business or Mission Analysis](https://sebokwiki.org/wiki/Business_or_Mission_Analysis), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-30.
8. NIST. [*Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final), SP 800-160 Volume 1 Revision 1, November 2022. Consulted 2026-08-30.

## Exercises

### Exercise 1

Distinguish an operational concept from a scenario, use case, requirement, architecture, procedure, and operations plan. State what each contributes and one failure caused by substitution.

### Exercise 2

Build current, target, and transition views for replacing manual university laboratory access with a governed digital capability. Include roles, authority, modes, support, measures, and rollback.

### Exercise 3

Diagnose a delivery-drone concept that covers normal flight but assumes positioning, communications, weather data, and landing access. Derive the missing operational content without selecting a particular design.

### Exercise 4

Compare centralized and bounded local incident authority for a multi-region service. Give conditions, measures, risks, evidence, and a defensible selection rule.

### Exercise 5

Develop a reviewable operational concept for remote home dialysis. Include stakeholder outcomes, current/target/transition, roles, modes, ecosystem, human/system allocation, support, measures, assumptions, hazards, traceability, and review authority.

## Answers to the Exercises

### Answer 1

An operational concept integrates intent, boundary, current/target/transition operations, roles, authority, modes, ecosystem, support, measures, assumptions, risk, and representative threads. A scenario instantiates a time-ordered path; a use case focuses actor/system interaction toward a goal; a requirement assigns a necessary verifiable obligation; architecture organizes realization; a procedure directs repeatable work; an operations plan assigns detailed resources, timing, and control for actual operation. Substitution loses information: UI use cases omit support and affected non-users; prose concepts cannot replace verifiable requirements; architecture presented as concept forecloses alternatives; early concepts used as procedures lack executable safety detail. The artifacts should trace and constrain one another without collapsing their meanings.

### Answer 2

Current evidence covers keys/cards, issue authority, visitor process, after-hours access, safety training, lost credentials, door failures, incident records, accessibility, staffing, and workarounds. The target outcome is authorized, timely, accessible entry with laboratory-specific competence and auditable emergency control—not “install an app.” Roles include student/researcher, supervisor, safety officer, security, facilities, accessibility, identity administration, support, responder, auditor, and supplier. Modes include normal, after-hours, exam/restricted work, emergency/evacuation, network/power loss, maintenance, and suspension.

Transition uses inventory and identity reconciliation, authorization playback, accessibility testing, staged buildings/cohorts, dual credential periods, staff training, support surge, discrepancy handling, privacy/security review, and named cutover/rollback authority. Support covers provisioning, revocation, device/door maintenance, logs, incident recovery, supplier escalation, and eventual credential retirement. Measures include legitimate entry success and time by population/mode, unauthorized access, emergency egress, revocation latency, recovery, support burden, and false denial. Roll back a cohort when safety, authorization integrity, or accessible-entry criteria fail; preserve reconciled records and communicate status.

### Answer 3

Treat positioning, communications, weather, maps, energy, airspace authority, landing permission, and retrieval as external/enabling capabilities with owners, semantics, quality, timing, failure behavior, and evidence. Add modes for degraded positioning, lost communications, severe weather, unsafe landing, low energy, restricted airspace, maintenance, update, emergency, and retirement. Model customer, operator, maintainer, bystander/property owner, authority, responder, supplier, and privacy/environment roles.

Threads must cover mission authorization, loading/custody, launch, navigation, handoff, alternate landing, diversion, abort, recovery, incident evidence, notification, repair, return to service, and disposal. State outcome measures and guardrails for delivery, injury/property risk, privacy/noise, workload, failed recovery, and distribution. Derive candidate needs and architecture questions—such as sufficient state awareness and safe action during dependency loss—without prescribing a sensor, radio, or landing mechanism. Flight and public-safety adequacy require applicable aviation, operational, safety, and community authority.

### Answer 4

Central authority supports consistent policy, cross-region visibility, scarce expertise, and coordinated external communication, but depends on communication, shared context, and timely capacity. Bounded local authority supports rapid containment and resilience under partition but risks inconsistent action, wider privilege, local overload, and reconciliation debt. Define incident classes, reversibility, blast radius, time-to-harm, evidence available, competence, permissions, mandatory notification, escalation, and post-action reconciliation.

Measure containment and restoration time, harmful delay, unauthorized or excessive intervention, recurrence, coordination failures, operator workload, audit completeness, and regional distribution. Use exercises, historical incidents, access simulations, failure injection, and organizational/legal review. A defensible rule grants pre-authorized local actions when delay consequence exceeds bounded-action risk and actions are observable, reversible where possible, competence-backed, and later reconciled; otherwise escalate centrally. Safety, privacy, contractual, or regulatory constraints remain non-compensable and require their authorities.

### Answer 5

The outcome is safe, effective treatment at home with patient autonomy, comprehensible burden, clinical continuity, privacy, and recourse. Current evidence includes clinic treatment, home-care work, incidents, training, supplies, housing/network/power conditions, caregiver load, and excluded populations. Target operation coordinates patient/caregiver, nephrology team, pharmacy/laboratory, trainer, support, maintenance, supplier, delivery, emergency service, utility/network, privacy/security, quality, and regulator. Transition covers clinical eligibility, home assessment, consent, training/competence, installation, baseline data, supervised sessions, supply continuity, support readiness, and rollback to clinic care.

Modes include setup, treatment, pause, alarm, degraded sensing/network/power, contamination, emergency, cleaning, maintenance, calibration, update, travel, and retirement. Allocation questions include setup verification, treatment adjustment, alarm interpretation, escalation, and override; do not automate them without clinical/human-factors evidence. Support includes 24-hour clinical versus technical triage boundaries, consumables, sterile handling, repair, calibration, software/configuration control, incident evidence, replacement, and safe disposal. Measures cover clinical outcomes, adverse events, completion, alarms, escalation, workload, accessibility, subgroup distribution, supply interruption, recovery, support, and privacy/security harm.

Assumptions about competence, housing, caregiver availability, connectivity, power, delivery, and clinical response receive owners, evidence, triggers, and mitigations. Trace needs through threads to requirements, hazards, interfaces, training, verification, and representative home validation. Review requires patient/caregiver, clinical, nursing, human-factors/accessibility, safety, infection-control, privacy/security, maintenance, operations, quality, ethics, supplier, emergency, and applicable regulatory authority. Internal analysis cannot establish clinical benefit, informed consent, regulatory conformity, or acceptable residual risk; no external review is claimed.
