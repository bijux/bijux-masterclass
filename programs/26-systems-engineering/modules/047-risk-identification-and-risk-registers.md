---
module_id: SYSENG-047
program: Systems Engineering
level: 1
module_number: 47
title: Risk Identification and Risk Registers
status: complete
last_verified: 2026-08-31
---

# Risk Identification and Risk Registers

## One-Page Review

### Governing question

How can a systems team identify credible future shortfall scenarios early and continuously, express them causally, and maintain a risk register that supports analysis and action rather than becoming a stale list of vague concerns?

### Essential definitions

- An **objective** is an explicitly established outcome or performance requirement whose shortfall gives risk meaning.
- **Risk** is the potential for future shortfall relative to objectives; it combines one or more credible scenarios with uncertain likelihood and consequence.
- A **condition** is a present fact, state, assumption, dependency, or circumstance that makes a future departure credible.
- A **departure** is a possible future deviation from the baseline or expected behavior.
- An **asset** is the mission, product, capability, person, organization, resource, environment, stakeholder outcome, or other valued object affected.
- A **consequence** is the credible effect on objectives if the scenario unfolds; it is not merely a restatement of the departure.
- A **risk statement** is a concise causal form such as: “Given [condition], there is a possibility of [departure] affecting [asset], leading to [consequence].”
- A **risk narrative** supplies context, causal pathway, evidence, assumptions, uncertainty, scope, interfaces, and alternative scenarios behind the concise statement.
- A **risk register** is the configuration-controlled system of record for risk identity, scenario, evidence, analysis, ownership, dependencies, response, status, decisions, and history.
- An **issue/problem** is an adverse state or event already realized. Its uncertain downstream consequences can remain risks, but the current fact is managed as an issue.
- A **hazard** is a source or state with potential harm; risk scenarios connect hazards to exposure/events and consequences. Hazard analysis and risk management overlap but are not interchangeable.
- A **threat** is a potential cause—often intentional in security contexts; **vulnerability** is a weakness or susceptibility. Neither alone is a complete risk statement.
- An **opportunity** is an uncertain favorable departure relative to objectives and should be managed with semantics distinct from threats where governance requires.
- A **risk owner** is accountable for understanding, reporting, coordinating, and bringing decisions forward; owners need authority/access but do not necessarily execute every response action.
- **Inherited**, **interface**, and **cross-cutting risks** arise from providers, acquirers, shared services, external organizations, or coupled system elements and require explicit coordination/elevation.

### Central model, mechanism, or theorem

Represent individual risk (r_i) as a scenario family plus evidence and governance:

\[
r_i=(O_i,S_i,L_i,C_i,U_i,E_i,T_i,G_i),
\]

where (O_i) is the affected objective set, (S_i) credible event sequences, (L_i) likelihood model, (C_i) consequence vector, (U_i) uncertainty, (E_i) evidence/provenance, (T_i) timeframe/triggers, and (G_i) governance/ownership.

A simplified causal sequence is

\[
condition\rightarrow departure\rightarrow asset/objective\ shortfall\rightarrow consequences.
\]

When likelihoods are calibrated probabilities and consequences are cardinal on a common basis, expected consequence may be

\[
E[C]=\sum_sP(s)C(s).
\]

This does not justify multiplying ordinal likelihood and consequence categories or aggregating dependent risks independently. Identification precedes quantitative/qualitative analysis and preserves uncertainty.

### Critical invariants

- Risks trace to explicit current objectives, requirements, success criteria, constraints, stakeholders, baselines, and decision horizons.
- Identification is continuous across lifecycle, hierarchy, disciplines, interfaces, suppliers, operations, changes, incidents, and external conditions.
- Statements distinguish present condition, possible future departure, affected asset/objective, and credible consequence.
- A realized condition/event is recorded as an issue; uncertain additional departures/consequences are separately formulated as risks.
- Each risk has a stable unique identifier and preserves origin, dates, configuration, revisions, merges/splits, decisions, and closure/elevation history.
- Narratives capture causal paths, assumptions, evidence, uncertainty, scope, boundaries, dependencies/common causes, and missing information.
- Likelihood, consequence, timeframe, proximity, velocity, detectability, reversibility, and confidence use governed definitions appropriate to the decision.
- Ordinal categories are not multiplied or averaged as though they were ratio-scale numbers.
- Risk ownership, response-action ownership, risk acceptance authority, provider/acquirer responsibilities, escalation, and communication are explicit.
- Dependencies, common causes, cascades, mutually exclusive scenarios, double counting, and aggregate/portfolio effects are represented.
- Sensitive security, privacy, personnel, procurement, legal, or safety information is access-controlled without hiding necessary decision content.
- Register quality is measured by current evidence, decision/action usefulness, closure integrity, and learning—not number of rows or green cells.

### Common failures

Common failures include brainstorming without objectives; writing topics such as “supplier,” “cyber,” or “schedule” as risks; embedding the proposed mitigation in the statement; confusing a current issue with a possible event; listing only consequences without causes; using “may impact cost/schedule/performance” for every row; failing to name whose objective is affected; copying old registers without application checks; treating assumptions as facts; excluding human, organizational, ethical, environmental, security, operations, retirement, or external risks; assigning a single color before writing scenarios; multiplying 1–5 ordinal scores; averaging unrelated domains; splitting one causal chain into double-counted rows; combining distinct scenarios into an unmanageable mega-risk; omitting dependencies; naming owners without authority; closing risks because a task completed rather than evidence changed; deleting history; and suppressing uncomfortable risks to keep dashboards green.

### Compact example

Weak: “Supplier delay—high.” Stronger: “Given that the sole-source radiation-tolerant converter has not completed process qualification and its replacement lead time exceeds six months, there is a possibility that qualified flight units will arrive after integrated environmental-test entry, affecting the power subsystem and system verification sequence, leading to launch-window delay, extended team/facility cost, and reduced time for anomaly correction.” The narrative cites supplier/process evidence, dates, interfaces, alternative source constraints, dependent tests, likelihood/consequence uncertainty, triggers, owner, escalation, and information needs.

### Connections

SYSENG-041–046 establish objectives, decisions, trade studies, integrated forecasts, uncertainty, sensitivity, and technology gaps. This module turns potential shortfalls into governed scenarios. SYSENG-048 plans mitigation and evidence-based retirement; SYSENG-049–050 preserve acceptance and architecture decisions. Requirements, interfaces, integration, configuration, verification, operations, suppliers, human factors, safety, security, and sustainability are identification lenses.

## Governing Question

What can credibly happen between the current state and an objective shortfall, why might it happen, when would it matter, how would we know, and who has the authority and information to act?

Risk registers fail when they answer only “what are we worried about?” A worry can be useful input, but management needs an explicit causal hypothesis connected to evidence and objectives. A good record is revisable: new evidence may change the condition, split scenarios, reveal common cause, turn a risk into an issue, reduce likelihood, worsen consequence, or show that the original framing was wrong.

## Why This Matters

Unidentified risk cannot be deliberately analyzed, mitigated, monitored, accepted, transferred/elevated, or included in cost/schedule/performance forecasts. Poorly formulated risk creates a different problem: teams spend effort debating colors, owners, and mitigations without agreeing on the future scenario. The register becomes administrative inventory rather than decision infrastructure.

NASA's current objectives-driven Risk Management Handbook defines individual risk through scenarios, likelihood, and consequences and gives a structured condition–departure–asset–consequence statement with narrative context. NPR 8000.4C requires attention to safety, mission success, security, cost, schedule, and other relevant domains; it also emphasizes cross-cutting and inherited/provider risks, analysis uncertainty, communication, elevation, and accountable acceptance.

NASA Technical Risk Management calls for continual identification using requirements, baselines, measures, experience, and programmatic inputs. Its current active GSFC risk-assessment handbook recognizes that likelihood/consequence scales may be locally governed. The lesson is not to copy one matrix: define the objectives, scenarios, evidence, scales, and authority for this system, then maintain them as the system changes.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. organizational/mission/stakeholder objectives, ConOps, success criteria, requirements, constraints, risk tolerance/acceptance criteria, decision authority, and escalation paths;
2. current system/product/work breakdowns, architecture, interfaces, configurations, lifecycle, environments, schedules/resources, suppliers, operations/support, and retirement;
3. assumptions, margins, technical performance measures, readiness gaps, models/simulations, uncertainty/sensitivity, trade studies, verification/validation, and evidence provenance;
4. hazards, threats, vulnerabilities, controls, safety/security/privacy/environmental analyses, human/organizational factors, ethics/equity impacts, and applicable regulations;
5. issues, anomalies, defects, nonconformances, incidents/near misses, changes, waivers, lessons, audits, independent reviews, supplier/external risks, and prior registers;
6. risk plan with definitions, categories, likelihood/consequence/time scales, aggregation, reporting cadence, ownership, access control, closure/acceptance, and record retention;
7. facilitation methods, causal/event modeling, probability/uncertainty, schedule/cost networks, interviewing, dissent, and psychological safety.

As a retrieval test, inspect the row “integration risk—yellow—owner: chief engineer.” Ask for current condition, possible departure, affected interface/asset/objective, causal sequence, credible consequences, evidence, uncertainty, timing/triggers, dependencies, response authority, and why yellow. If those cannot be recovered, the row is not yet a managed risk.

## Learning Objectives

After completing this module, you should be able to:

1. frame risk identification around explicit objectives, baselines, decisions, and governance;
2. distinguish risk from issue, hazard, threat, vulnerability, assumption, uncertainty, and opportunity;
3. write concise causal risk statements and substantive narratives;
4. identify risks systematically across product, work, lifecycle, interface, human, supplier, operational, and external lenses;
5. design a complete, versioned risk-register schema with traceability and access control;
6. select and use qualitative/quantitative scales without invalid ordinal arithmetic;
7. model risk dependencies, common causes, cascades, aggregation, and double counting;
8. assign ownership, action roles, elevation, inherited-risk coordination, and acceptance authority;
9. audit register completeness, freshness, evidence, decisions, closure integrity, and learning;
10. facilitate candid identification and turn new evidence/change into controlled register updates.

## Core Exposition

**Start from objectives and shortfalls.** List mission, safety, security, technical, human, cost, schedule, operational, environmental, legal, ethical, and stakeholder outcomes that matter. Define performance requirements and thresholds. Ask how each could be missed, delayed, degraded, made inequitable, or achieved with unacceptable collateral consequence. A risk category without an objective is only a filing label.

**Establish risk semantics and authority.** The plan defines risk, issue, opportunity, assumption, likelihood, consequence, timeframe, proximity/velocity, tolerance, escalation, acceptance, closure, and sensitive handling. Name who owns the process, individual risk, response actions, resources, technical evidence, and final acceptance. Local tailoring must preserve governance and applicable mandatory rules.

**Build a causal statement.** Write the present condition as evidence, not anxiety. State a possible future departure, not the current fact. Name the affected asset/objective. Describe foreseeable consequence in outcome terms. Avoid “because X, X may happen” tautologies. Do not write the response as the risk (“if we do not add redundancy…”); first state the mechanism, then compare responses.

**Add a narrative.** Capture scope/configuration, discovery source/originator, event sequence, initiating conditions, barriers/controls, exposure, affected requirements/stakeholders, scenarios, evidence, assumptions, uncertainty, likelihood/consequence bases, timing, indicators/triggers, dependencies, alternative interpretations, information needed, and limitations. The statement supports scanning; the narrative supports analysis.

**Distinguish risks from issues.** “The test fixture failed calibration yesterday” is an issue. Future schedule delay, invalid prior data, retest cost, or undetected product escape remain uncertain risk scenarios. Manage the repair/correction in issue/change systems while retaining linked risks. Do not reduce apparent risk by relabeling adverse facts as future possibilities.

**Distinguish hazards, threats, and vulnerabilities.** A flammable material is a hazard; ignition/exposure scenarios plus consequences form risk. An adversary is a threat and weak authentication a vulnerability; intentional scenarios may require conditional likelihood given attack rather than an unjustified unconditional frequency. Preserve domain analysis and trace its scenarios/controls into enterprise/project risk decisions.

**Treat assumptions as monitored claims.** Each material assumption needs evidence, owner, validity interval, sensitivity, verification date, and trigger. A fragile assumption can be a condition in several risks. Do not duplicate its full consequence in every row without representing common cause and aggregation.

**Use multiple identification lenses.** Traverse objectives/requirements; stakeholder and lifecycle scenarios; PBS/WBS/OBS; architecture/interfaces; integration/verification/validation; technology readiness; cost/schedule/resource networks; suppliers/contracts; facilities/tools/data; manufacture/quality; operations/maintenance/retirement; safety/security/privacy; human/organizational factors; sustainability/environment; regulatory/legal/ethics; external geopolitical/economic/weather; and portfolio/shared services.

**Apply complementary techniques.** Use structured interviews, facilitated workshops, pre-mortems, assumption challenge, scenario analysis, causal diagrams, FMEA/FMECA, fault/event trees, HAZOP, STPA, threat modeling, bow-ties, checklists/taxonomies, schedule risk, Monte Carlo traces, sensitivity, red teams, audits, lessons, and field observation as appropriate. No single technique covers every causal class.

**Create psychological and organizational safety.** Invite dissent from junior staff, operators, maintainers, suppliers, affected groups, and independent reviewers. Separate identification from blame and immediate scoring. Record minority concerns and evidence needs. Incentives that punish bad news cause risk blindness; anonymous routes can complement but not replace accountable investigation.

**Identify interface and inherited risks.** Ask what assumptions each side makes, who owns shared functions/data/resources, which provider risks affect acquirer objectives, and what is outside local control. Link reciprocal records rather than asserting “transferred.” Define communication, evidence, action, decision, and elevation at the level able to manage common cause.

**Decompose and combine carefully.** Split a mega-risk when scenarios have different conditions, likelihood models, consequences, owners, triggers, or responses. Combine duplicates that describe the same causal event. Preserve one source risk with several consequences when appropriate. Use parent/child and dependency links so decomposition does not inflate aggregate exposure.

**Choose register fields by decision need.** Core fields include stable ID, title, status/disposition, statement, narrative, objective/requirement/asset, originator/source, owner, action owners, acceptance authority, configuration/scope, category/taxonomy, causes/conditions, event sequences, consequences by domain/stakeholder, evidence/assumptions/uncertainty, likelihood/consequence/timeframe, confidence, priority rationale, dependencies/common causes, indicators/triggers, responses/contingency, residual/target state, resources/dates, escalation, decisions/rationale, created/reviewed/next-review dates, history, links, and access classification.

**Use stable identity and history.** IDs survive title/score/owner changes. A split creates new linked children; a merge preserves source links. Do not reuse IDs or delete closed records. Store who changed what, when, why, on which evidence/configuration, and under whose authority. Snapshots support audits and model reconciliation.

**Analyze after adequate formulation.** Estimate likelihood and consequence with uncertainty, timeframe, velocity, detectability, reversibility, and evidence strength as decision requires. Use ranges/distributions/scenarios where supported. Separate inherent/pre-response, current, residual/target, and realized states. SYSENG-048 develops response and retirement discipline.

**Respect scale semantics.** Ordinal likelihood level 4 and consequence level 5 do not yield a cardinal “20.” A matrix cell can route attention under governed definitions, but equal products need not mean equal risk and categories may differ across domains. Do not average safety, cost, schedule, mission, equity, or environmental consequence into a number that erases vetoes/authority.

**Prioritize transparently.** Consider scenario likelihood/consequence/uncertainty, timeframe and decision lead, reversibility, affected stakeholders, risk tolerance, aggregation/common cause, controllability, information value, response resources, and escalation. Low-likelihood catastrophic or legal/safety risks may demand action even when a simple score ranks them below frequent cost variance.

**Represent dependence and aggregation.** Build a risk network connecting common conditions, event sequences, resources, schedule activities, requirements, interfaces, suppliers, and consequences. Distinguish mutually exclusive from co-occurring scenarios. Model correlations/conditional probabilities when evidence supports them; otherwise use joint stress scenarios/bounds. Do not sum maximum consequences or multiply probabilities blindly.

**Define owner and authority correctly.** The risk owner keeps the scenario understood, coordinated, current, analyzed, and presented for decision. Action owners deliver named work. The acceptance authority bears accountability at the appropriate level. A person without budget, access, cross-boundary authority, or decision path cannot meaningfully own a risk alone.

**Elevate without abandonment.** Elevation moves or shares decision authority to a level able to manage cross-cutting consequence. The originating team continues local actions, evidence, and communication unless explicitly reassigned. Maintain linked local/parent views so elevation does not become disappearance.

**Protect sensitive information.** Separate broadly shareable decision summary from restricted detail when necessary. Apply least privilege, secure storage, approved marking/retention, and need-to-know escalation. Redaction must not prevent responsible authorities from understanding consequence or acting.

**Review for freshness.** At event-driven and scheduled reviews, confirm condition, objective/baseline, scenario, evidence, assumptions, analysis, dependencies, owner/authority, actions, triggers, dates, and disposition. Review frequency follows risk velocity and decision lead—not a universal monthly ritual. Automated stale-date warnings help but cannot judge causal validity.

**Audit coverage and blind spots.** Compare risk distribution to objectives, PBS/WBS/lifecycle, interface inventory, hazard/threat analyses, suppliers, schedule critical paths, assumptions, changes, anomalies, and stakeholder groups. Empty categories may mean low risk or missing participation. Sample closed/accepted/green risks for evidence and look for repeated generic language.

**Measure register health.** Useful indicators include statement/narrative completeness, objective links, evidence recency, owner/authority coverage, overdue reviews/actions, trigger observability, dependency/orphan links, issue conversion, accepted-risk rationale, closure evidence, reopened risks, and forecast reconciliation. A falling row count is not inherently improvement.

**Communicate uncertainty and dissent.** Present scenario profiles, drivers, timing, dependencies, range/confidence, actions, residual state, decisions, and evidence gaps—not only heat maps. Show sensitive information through governed channels. Preserve disagreements about plausibility or consequence and state how they will be resolved or accepted.

**Update from change and learning.** New requirement, design/interface, supplier, schedule/resource, environment, operation, regulation, incident, anomaly, test, model, or stakeholder evidence triggers identification and reanalysis. Feed outcomes into lessons and taxonomies without copying stale scenarios into unrelated programs.

The following checker audits structural integrity of a small declared register. It does not estimate or validate the risks themselves.

<!-- bijux-verify: {"id":"risk-register-structure-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"risk_count=3\nissue_count=1\nunique_ids=1\nstructured_statements=3\nobjective_links=3\nowners=3\ntriggers=3\ndependency_edges=2\norphan_edges=0\ncurrent_records=3\nstatus=register_structurally_complete\nevidence=declared_records_only\n","stderr":""}} -->
```python
required = ("condition", "departure", "asset", "consequence", "objective", "owner", "trigger")
risks = [
    {"id": "R-01", "condition": "sole source unqualified", "departure": "late units",
     "asset": "integration", "consequence": "window delay", "objective": "launch date",
     "owner": "supply lead", "trigger": "qualification misses review", "current": True},
    {"id": "R-02", "condition": "interface timing unverified", "departure": "control instability",
     "asset": "integrated system", "consequence": "performance shortfall", "objective": "stability",
     "owner": "integration lead", "trigger": "margin below threshold", "current": True},
    {"id": "R-03", "condition": "operator model lacks adverse trials", "departure": "late takeover",
     "asset": "safe operation", "consequence": "hazard exposure", "objective": "safety",
     "owner": "human-systems lead", "trigger": "trial response exceeds limit", "current": True},
]
issues = [{"id": "I-01", "fact": "test fixture calibration expired"}]
edges = [("R-01", "R-02"), ("R-02", "R-03")]
ids = {risk["id"] for risk in risks}

print(f"risk_count={len(risks)}")
print(f"issue_count={len(issues)}")
print(f"unique_ids={int(len(ids) == len(risks))}")
print(f"structured_statements={sum(all(risk.get(field) for field in required[:4]) for risk in risks)}")
print(f"objective_links={sum(bool(risk.get('objective')) for risk in risks)}")
print(f"owners={sum(bool(risk.get('owner')) for risk in risks)}")
print(f"triggers={sum(bool(risk.get('trigger')) for risk in risks)}")
print(f"dependency_edges={len(edges)}")
print(f"orphan_edges={sum(a not in ids or b not in ids for a, b in edges)}")
print(f"current_records={sum(risk['current'] for risk in risks)}")
complete = all(all(risk.get(field) for field in required) for risk in risks)
complete &= len(ids) == len(risks) and all(a in ids and b in ids for a, b in edges)
print("status=" + ("register_structurally_complete" if complete else "register_needs_work"))
print("evidence=declared_records_only")
```

The checker separates the realized issue from future risks and verifies fields/links only. It cannot establish scenario credibility, completeness of identification, analysis quality, or acceptable risk.

## Definitions and Notation

Let objectives (O), baseline state (B_t), scenario set (S), evidence (E_t), likelihood model (L), consequence vector (C), uncertainty (U), timeframe (T), and governance (G).

Risk identity at time (t):

\[
r_t=(id,O,B_t,S,E_t,L,C,U,T,G,status,history).
\]

For a statement:

\[
condition(B_t,E_t)\Rightarrow possibility(departure)\Rightarrow impact(asset,O)\Rightarrow consequence.
\]

The arrow denotes a causal hypothesis requiring analysis; it is not deterministic implication.

Risk dependency graph is (G_R=(V_R,E_R)) where vertices are risks/conditions/events/objectives and edges encode causal, shared-resource, temporal, or informational dependence. Edge type/direction/evidence must be explicit.

If scenarios are mutually exclusive and probabilities/cardinal consequences are valid:

\[
E[C]=\sum_sP(s)C_s.
\]

For dependent or non-cardinal cases, use appropriate joint models, bounds, scenarios, or ordered decision rules; do not force this formula.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—objective and governance framing.** Define shortfalls, semantics, scales, authority, ownership, escalation, communication, and records.

**Mechanism 2—multi-lens identification.** Traverse lifecycle/products/work/interfaces/stakeholders and apply complementary causal, hazard, threat, schedule, human, supplier, and field methods.

**Mechanism 3—causal formulation.** Separate condition, possible departure, asset/objective and consequence; add evidence, uncertainty, timing, assumptions, and narrative.

**Mechanism 4—register/network control.** Maintain stable identity, dependencies/common causes, owners/triggers/actions/decisions, sensitive access, history, and linked issues.

**Mechanism 5—continuous challenge and learning.** Audit coverage/freshness, reconcile to changes/evidence/forecasts, preserve dissent, elevate, and reopen when conditions change.

Identification completeness cannot be proven by row count. Diverse systematic search, independent challenge, operational learning, and resilient design reduce—but cannot eliminate—the possibility of omitted scenarios.

## Alternatives and Trade-Offs

**Free-form workshops** surface tacit concerns rapidly. **Structured decomposition/checklists/analyses** improve coverage and traceability but can constrain imagination. Combine them.

**One concise statement** supports communication. **Detailed narrative/causal model** supports analysis. Link them rather than overloading either.

**Central register** enables portfolio aggregation and governance. **Domain tools** retain safety/security/supplier detail. Federate through stable IDs, mappings, ownership, and synchronized dispositions.

**Qualitative scales** support sparse evidence and rapid routing. **Quantitative models** support coherent aggregation/decision analysis when calibrated data and cardinal consequence exist. False numbers are not superior to explicit judgment.

**Broad access** improves shared awareness. **Restricted access** protects sensitive information. Use tiered views and accountable access, not secrecy by default.

**Risk decomposition** creates actionable ownership. **Aggregation** reveals common cause and portfolio consequence. Preserve graph links to avoid double counting or fragmentation.

## Failure Modes and Misconceptions

**“A risk is anything bad.”** Risk is uncertain future shortfall; present bad states are issues and hazards/threats need scenarios.

**“Risk statements should include the fix.”** That anchors the team before causal analysis and alternatives; formulate risk first.

**“The matrix score is the risk.”** A cell is a routing summary under definitions, not the scenario, evidence, uncertainty, timing, or consequence distribution.

**“Probability times impact always works.”** Ordinal categories and dependent scenarios do not support ordinary multiplication/aggregation.

**“The owner is responsible for preventing everything.”** The owner coordinates understanding and decisions; action and acceptance roles are distinct.

**“Transferred risk is gone.”** Contractual or organizational transfer rarely removes system consequence; inherited/interface coordination remains.

**“Closed means it never mattered.”** Closure retains evidence, rationale, residual conditions, lessons, and reopening triggers.

**“A long register is comprehensive.”** It may contain duplicates, vague topics, stale rows, and miss systemic risks.

**“A short register proves control.”** Incentives, weak participation, or premature closure can suppress identification.

**“Unknown risks can be entered as a percentage reserve.”** Reserve supports resilience but cannot identify or quantify omitted mechanisms.

## Worked Examples

### Example 1

**Topic to scenario.** “Cybersecurity” becomes: given an unsupported authentication library and exposed maintenance interface, a crafted credential may obtain privileged access, affecting control configuration and safe operation, leading to unsafe commands, outage, investigation, and regulatory consequence. Threat analysis supplies branches and controls.

### Example 2

**Issue and residual risk.** A supplier misses today's delivery—issue. Continued process instability may delay replacement lots and compress qualification—risk. Link them; do not keep “supplier may be late” in future tense as if nothing happened.

### Example 3

**Assumption as common condition.** Three subsystem plans assume a shared facility is available. Create one facility condition/source with linked schedule/test risks, not three independent probabilities whose aggregation exaggerates or misses common cause.

### Example 4

**Mega-risk split.** “New battery may fail causing cost, delay, fire, low endurance, supplier loss” contains different mechanisms and authorities. Split thermal propagation, aging/performance, qualification schedule, and sole-source/process scenarios while linking shared chemistry/supplier evidence.

### Example 5

**Ordinal matrix caution.** Likelihood 2/consequence 5 and likelihood 5/consequence 2 both multiply to 10, but one may be catastrophic safety exposure requiring different authority while the other is frequent recoverable cost. Preserve domain thresholds and scenario profiles.

### Example 6

**Interface risk.** Provider guarantees average throughput; acquirer assumes worst-case burst latency. Neither owns queue behavior. Form an interface scenario, define workload/evidence and reciprocal owners, and elevate if shared architecture authority is needed.

### Example 7

**Opportunity separation.** A new supplier process might reduce mass and cost but requires qualification and may increase variability. Record favorable opportunity and threat scenarios with shared evidence and decision; do not net them into a neutral score.

### Example 8

**Sensitive security risk.** The broad register says an access-control weakness could affect operational integrity and names owner/decision deadline. Restricted linked detail contains exploit path and assets. Responsible authorities see enough to act while disclosure is controlled.

### Example 9

**False closure.** Mitigation test ran, but acceptance failed under one boundary load. Completing the task does not close risk. Update evidence, issue/anomaly, scenario likelihood/consequence and next action; closure requires governed criteria.

### Example 10

**Register health audit.** Twenty percent of rows have no objective link, fifteen are past review date, four owners left, and several closed items lack evidence. Repair governance and causal records before claiming aggregate risk is falling.

## Cross-Program Connections

**Platform engineering.** Identify shared-control-plane, tenant isolation, capacity, cloud/provider, upgrade, adoption, organizational and incident-response scenarios with common service dependencies.

**API and service engineering.** Contract/version, retry amplification, dependency, consistency, security, client migration, observability and ownership boundaries create coupled service risks.

**Data engineering.** Schema/quality/lineage, late data, replay, privacy, retention, model drift, supplier feeds and shared compute create risks often hidden by pipeline-local registers.

**Object-oriented programming.** Risks arise through mutable shared state, dependency/runtime changes, inheritance/contract fragility, test gaps, ownership and evolution—not a paradigm label itself.

**Functional programming.** Effect/runtime/concurrency, laziness/resource behavior, type boundary, interoperability, ecosystem, migration and team-learning assumptions need causal scenarios and evidence.

## References

1. NASA, *Risk Management Handbook Version 2.0, Part 1*, NASA/SP-20240014019, 2024. <https://ntrs.nasa.gov/citations/20240014019>
2. NASA, *Risk Management Handbook Version 2.0, Part 2*, NASA/SP-20240014326, 2024. <https://ntrs.nasa.gov/citations/20240014326>
3. NASA, *Agency Risk Management Procedural Requirements*, NPR 8000.4C, current directive. <https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_8000_004C_&page_name=Chapter1>
4. NASA, *NPR 8000.4C Appendix C: Risk Statement and Event Sequence Guidance*. <https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_8000_004C_&page_name=AppendixC>
5. NASA, *NPR 8000.4C Chapter 3: Roles, Cross-Cutting Risks, Communication, and Acceptance*. <https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_8000_004C_&page_name=Chapter3>
6. NASA, *Systems Engineering Handbook, Section 6.4: Technical Risk Management*, current web edition. <https://www.nasa.gov/reference/6-4-technical-risk-management/>
7. NASA Goddard, *Guideline for Performing Risk Assessments*, GSFC-HDBK-8005 Rev. A, active 2024. <https://standards.nasa.gov/node/1951>
8. NASA Safety and Mission Assurance, *Risk Management*, current Objectives-Driven Risk Management Framework overview. <https://sma.nasa.gov/sma-disciplines/risk-management>
9. NASA Software Engineering Handbook, *SWE-086 Continuous Risk Management*. <https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604571/SWE-086+-+Continuous+Risk+Management>
10. NASA, *NODIS Library*, current directive status index. <https://nodis3.gsfc.nasa.gov/npr_sort.cfm>

## Exercises

### Exercise 1

Rewrite “Database migration—red—may affect the project” as a structured risk statement and narrative. Include condition, departure, asset/objective, consequence, evidence, uncertainty, timeframe, dependencies, owner, trigger, and issue distinction.

### Exercise 2

Classify and connect these: an expired certificate caused yesterday's outage; a shared certificate service remains poorly monitored; a threat actor may exploit renewal gaps; the organization assumes renewal is automatic; and a proposed redundant service may reduce downtime but adds configuration complexity.

### Exercise 3

Critique a 5×5 register that multiplies ordinal likelihood and consequence, ranks safety/cost/schedule together, treats equal products as equal, has no uncertainty or timeframe, and reports total portfolio risk as the sum of scores. Design a defensible alternative.

### Exercise 4

Design a risk-register schema and quality audit for a multi-supplier rail signaling system. Include stable identity, causal records, objectives, dependencies, interfaces, issues, hazards/security, evidence, scales, owners/authority, sensitive access, change/history, and health measures.

### Exercise 5

Conduct an identification plan for a regional heat-health warning and response system involving forecasts, sensors, public health, hospitals, utilities, employers, schools, transport, communications, housing, languages, disability access, and unequal exposure. Cover objectives, stakeholders, methods, scenario formulation, dependencies, ethics, governance, and blind spots.

## Answers to the Exercises

### Answer 1

Example statement: “Given that production data mappings were derived from incomplete lineage and two high-volume legacy fields have not passed representative reconciliation, there is a possibility that cutover transforms or omits valid records, affecting the authoritative customer ledger and continuity objective, leading to incorrect balances, service interruption, rollback/recovery work, regulatory notification, and loss of trust.”

The narrative names migration/configuration and cutover window; requirements for completeness/correctness/recovery; affected customer groups; evidence from lineage review and reconciliation sample; uncertainty about unobserved formats/late writes; causal branches involving freeze, CDC, transformation, validation and rollback; linked security/privacy and availability hazards; schedule/resource dependencies; and current controls. The migration owner coordinates; data owners validate mappings; operations owns rollback; compliance and decision authority govern acceptance.

Indicators include unreconciled-field count, mismatch rate by segment, replay lag, late-write volume and rollback rehearsal. Trigger might be any critical-field mismatch or mismatch above a declared bound at readiness review. If actual corrupt records have already been found, record that fact as an issue and link the uncertain extent, recurrence, cutover and consequence risks. Preserve evidence dates, assumptions, range/confidence, response alternatives and next review.

### Answer 2

The expired certificate and yesterday's outage are issues: realized condition/event/consequence requiring restoration and incident analysis. The poorly monitored shared service is a present condition and common cause. Form future operational risk: given inadequate inventory/expiry monitoring and shared renewal dependence, certificates may expire unnoticed, affecting authenticated services and availability, causing recurrent outage and recovery/regulatory consequences.

The threat actor plus renewal/control gaps forms a security scenario; likelihood may be conditional on attack and evidence from threat modeling. “Renewal is automatic” is an assumption requiring configuration evidence, owner, test and expiry trigger; its falsification contributed to the issue. The redundant service is an opportunity scenario for lower downtime and separate threats involving divergent configuration, expanded attack surface, failover failure and operational burden. Link all records to the same certificate-management condition, affected services/objectives and incident.

Do not net favorable and adverse effects into one score. Assign risk/issue/action owners and acceptance authority; create inventory, monitoring, rehearsed renewal/failover, access control and incident actions; model shared dependencies; preserve sensitive exploit detail in controlled links; and update from observed recurrence/coverage evidence.

### Answer 3

Ordinal labels describe ordered bins, not equal intervals or ratios, so multiplication and summation lack the claimed arithmetic meaning. A 2×5 and 5×2 equality can hide catastrophic versus frequent recoverable cases, different timeframes, confidence and authority. Mixing domains erases safety/legal vetoes and stakeholder distribution. Summing dependent/duplicate scores double counts; mutually exclusive and common-cause scenarios need different aggregation.

Retain causal statements/narratives and governed domain-specific likelihood/consequence definitions with evidence, uncertainty, timeframe/velocity, reversibility, stakeholders, dependencies and confidence. Use the matrix only as transparent routing if policy requires. Apply mandatory escalation/acceptance criteria for safety, security, legal or other domains. Prioritize using scenario profiles, decision lead, tolerance, controllability, information value and resource constraints.

For quantitative aggregation, use calibrated probabilities, cardinal consequence metrics and joint/conditional scenario models where justified; show cost/date/performance/safety distributions separately and avoid monetizing noncompensatory harm without legitimate policy. Otherwise use bounds, stress scenarios, partial ordering and portfolio narratives/networks. Report duplicates/common causes, marginal versus aggregate effects, sensitivity, uncertainty and dissent. Independent authority owns trade and acceptance.

### Answer 4

Schema includes immutable risk ID, title/status/disposition, structured statement and narrative; affected safety/mission/technical/cost/schedule/security/accessibility/environmental objectives and requirements; system/train/site/version/configuration; origin/source; conditions/causes, departure/event sequence, asset, consequence vector and affected passengers/workers/communities; evidence/assumptions/uncertainty; likelihood/consequence/time/proximity/velocity/confidence under named scales; dependencies/common causes/parent-child; indicators/triggers; owner, supplier/action owners, railway acceptance/elevation authority; response/contingency/residual state; resources/dates; decisions/rationale; created/review/next-review; issue/hazard/threat/vulnerability links; artifacts; classification/access; and complete revision/merge/split/closure/reopen history.

Federate system safety/hazard log, cybersecurity threat records, supplier registers, interfaces, requirements, WBS/schedule, defects/incidents and assurance cases through stable IDs. Suppliers cannot unilaterally close acquirer consequence. Model common signaling protocols, time synchronization, radio/network, track data, power, rolling-stock interfaces, human dispatch/driving, maintenance, construction staging, certification and shared subcontractors. Provide restricted technical exploit/safety detail with decision-capable summaries.

Audit unique/stable IDs; required causal fields; objective/requirement/configuration/evidence links; scale correctness; owner/authority access; provider/acquirer reciprocity; dependency/orphan/double-count links; overdue reviews/actions; stale assumptions; observable triggers; issue conversions; hazard/security reconciliation; changed interfaces; sensitive marking/access; accepted-risk rationale; closure evidence; reopenings; and forecast/incident consistency. Sample green/closed risks and seek operator/maintainer/passenger/accessibility/regulator dissent. Register health is actionable current evidence and decisions, not low row count.

### Answer 5

Define objectives by population/location/time: prevent heat illness/death, deliver timely understandable warnings, maintain clinical/utility/transport capacity, protect workers/students/unhoused/isolated people, preserve privacy and trust, and distribute resources equitably. Define thresholds, authority, legal obligations, operating/response timelines and risk tolerance with public-health, meteorological, emergency, municipal and community leadership.

Map system and stakeholders: forecast/data/sensor providers, public health, hospitals/EMS, utilities, water, housing/cooling centers, employers, schools/care facilities, transport, telecom/media/platforms, social services, languages, disability/accessibility, community organizations and individuals. Traverse forecast uncertainty/bias, urban heat/islands/indoor exposure, sensor placement/failure, data latency, thresholds, message comprehension/trust, channel outage, power/water failure, hospital/staff capacity, medicine/health, transport/access, employer compliance, housing, immigration/privacy fears, funding/procurement, compound wildfire/smoke/storm, and post-event learning.

Use scenario workshops with affected groups, pre-mortems, causal maps, hazard/public-health analysis, forecast backtests, field observation, accessibility/language testing, infrastructure dependencies, hospital/utility exercises, schedule/resource stress, incident/near-miss data and independent red teams. Form risks as current condition → possible departure → affected people/service/objective → consequence, with evidence, uncertainty, timeframe, geographic/demographic distribution, owner, trigger and dependencies. Record current lack of cooling capacity as an issue while treating future demand/cascade consequences as risks.

Model common heat event causing grid load/outage, indoor exposure, transport failure, communications/device loss and hospital demand; do not assign independent probabilities. Preserve forecast false-negative/false-positive and alert-fatigue/trust tradeoffs. Identify inherited weather/platform/utility risks, escalation and reciprocal ownership. Protect health/location data while ensuring authorized action.

Audit blind spots through geographic and demographic coverage, renters/unhoused/outdoor workers, older people, children, chronic illness, medication, disability, language/literacy, digital access, institutionalized people and informal caregivers. Avoid stigmatizing groups or shifting responsibility to individuals without resources. Community members help define consequence and acceptable communication. Maintain dissent and unknown compound scenarios. Update after forecast changes, exercises, outages, health outcomes, near misses, policy/infrastructure change and each heat event; register completeness cannot be inferred from a green dashboard.
