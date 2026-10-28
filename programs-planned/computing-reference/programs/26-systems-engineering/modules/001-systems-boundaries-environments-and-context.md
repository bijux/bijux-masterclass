---
module_id: SYSENG-001
program: Systems Engineering
level: 1
module_number: 1
title: Systems, Boundaries, Environments, and Context
status: complete
last_verified: 2026-08-29
---

# Systems, Boundaries, Environments, and Context

## One-Page Review

### Governing question

What must be inside the system of interest, what remains outside it, which relationships cross the boundary, and under which operational, organizational, physical, regulatory, and lifecycle conditions must the resulting system succeed?

### Essential definitions

- A **system** is a set of interacting elements organized to achieve outcomes in an environment. Elements may include people, hardware, software, data, facilities, procedures, services, and natural features.
- The **system of interest** is the system whose lifecycle is presently under consideration. It is selected for an engineering purpose; it is not a uniquely pre-existing box waiting to be discovered.
- A **boundary** distinguishes the system of interest from its environment for a stated scope and viewpoint.
- The **environment** comprises external conditions and entities that affect, constrain, enable, use, or are affected by the system.
- An **external entity** lies outside the chosen boundary but interacts with the system or matters to an outcome.
- An **interface** is a shared boundary across which matter, energy, information, control, authority, responsibility, money, or human action passes.
- An **enabling system** supports a lifecycle activity—such as development, production, deployment, training, operation, maintenance, or retirement—without necessarily belonging to the operational system of interest.
- A **context description** records the system of interest, relevant external entities, environments, interfaces, assumptions, constraints, scenarios, ownership, and unresolved questions.

### Central model, mechanism, or theorem

Treat boundary selection as a reviewable hypothesis. For a concern \(c\), lifecycle stage \(l\), and viewpoint \(v\), define a bounded context

\[
C_{c,l,v}=(S,E,B,I,A,K,O),
\]

where \(S\) is the system of interest, \(E\) relevant environment, \(B\) boundary rule, \(I\) crossing interfaces, \(A\) assumptions, \(K\) constraints, and \(O\) owners or authorities. The boundary is adequate only if it permits the intended claims and decisions without hiding a material dependency, consequence, control, lifecycle obligation, or stakeholder.

### Critical invariants

Every boundary has a named purpose, scope, lifecycle stage, viewpoint, owner, and revision trigger. Every material crossing has direction, content, semantics, timing, units, quality, failure behavior, security/safety classification, and responsible authorities appropriate to its risk. External does not mean irrelevant or uncontrollable; internal does not mean fully controlled. Context covers normal, degraded, emergency, maintenance, evolution, and retirement conditions. Assumptions are testable and owned rather than silently embedded in diagrams.

### Common failures

Teams draw the organization chart or procurement contract and call it the system boundary; include only technology while omitting people and procedures; treat a cloud service or operator as “outside scope” and therefore harmless; show arrows without semantics; model only nominal operation; confuse a component boundary with a security, safety, legal, or responsibility boundary; freeze context while suppliers and environments change; or select a boundary that makes an inconvenient outcome disappear from the analysis.

### Compact example

A smart-building heating controller could be framed narrowly as embedded hardware and firmware. For energy optimization, the useful system may include sensors, actuators, building zones, occupants, tariffs, weather data, maintenance procedures, and the control service. The electricity grid, weather provider, building owner, fire-safety system, and occupants can remain external, but their exchanges and authority cannot vanish. A cybersecurity authorization boundary may differ from the operational system boundary; both must be related explicitly.

### Connections

The next modules refine purpose, effectiveness, stakeholders, interactions, emergence, feedback, uncertainty, assumptions, and operational scenarios. Requirements engineering turns the bounded context into traceable needs and constraints. Architecture assigns functions and structures within and across the boundary. Security, safety, reliability, human factors, integration, verification, validation, operation, and retirement each impose additional views of the same evolving system.

## Governing Question

Which boundary makes the present engineering decision honest and tractable while preserving every external relationship, lifecycle dependency, and consequence needed to judge the system in use?

A boundary is necessary because no model can include the universe. It is also dangerous because moving a line can move cost, risk, responsibility, or evidence out of view. Systems engineering therefore asks not only “what is inside?” but “who chose this line, for which claim, at what lifecycle stage, and what becomes invisible because of it?”

## Why This Matters

Many severe defects are context defects before they are design defects. A technically correct device fails because maintenance cannot access it. A service meets its internal uptime target while its identity provider fails. An automated process is safe in nominal conditions but operators cannot recover it during degraded operation. A product is delivered, yet training, disposal, legal authorization, supplier data, or environmental conditions were never engineered.

ISO/IEC/IEEE 15288:2023 establishes lifecycle processes applicable to systems of interest, elements, and systems of systems from conception through retirement. It deliberately does not prescribe one development method. ISO/IEC/IEEE 42010:2022 distinguishes an entity's architecture from its architecture description and organizes descriptions around stakeholders and concerns. The INCOSE and NASA handbooks turn these ideas into multidisciplinary practice. NIST SP 800-160 v1r1 demonstrates why trustworthiness and security must be engineered in the system's operational environment, not appended to a component.

Boundary work creates the first shared evidence surface. It lets disciplines disagree about something concrete: entities, exchanges, conditions, owners, assumptions, and consequences. A context diagram alone is insufficient, but a governed context model prevents local teams from optimizing different imagined systems.

## Prerequisites and Retrieval

Retrieve sets, directed graphs, functions, ownership, lifecycle, and basic risk vocabulary. You should distinguish a product from the organization that makes it, an implementation from its environment, and verification from validation at an introductory level. No modeling language is required. Plain tables and diagrams are acceptable when their semantics and authority are explicit.

## Learning Objectives

By the end of this module, you should be able to:

1. define a system, system of interest, element, boundary, environment, external entity, interface, and enabling system;
2. select and defend a boundary for a stated concern, lifecycle stage, and viewpoint;
3. distinguish operational, organizational, physical, security, safety, legal, data, responsibility, and analytical boundaries;
4. inventory human, technical, natural, institutional, and lifecycle context;
5. specify boundary crossings with direction, semantics, timing, quality, failure, and authority;
6. identify hidden dependencies, displaced harms, unowned assumptions, and context changes;
7. use nested and alternative boundaries without confusing their claims;
8. check a context description for structural completeness and internal consistency; and
9. explain why context evidence cannot by itself prove stakeholder value, safety, legality, security, or operational success.

## Core Exposition

A system is identified by relationships and outcomes, not merely by physical proximity. A pile of components is not automatically a system, and one system can contain people, procedures, services, facilities, data, and natural elements as well as engineered artifacts. What counts as an element depends on the level of analysis. A vehicle may be the system of interest for a design team, an element of a transport service for an operator, and part of an urban mobility system for a municipality.

The **system of interest** focuses lifecycle responsibility. Selection answers: whose outcomes are at issue, which changes are possible, which evidence is required, and which authority accepts the result? It is not synonymous with the thing being purchased. A contract may cover one subsystem while the operational outcome depends on several independently managed systems and human organizations. Procurement boundaries remain relevant, but they cannot substitute for operational context.

A boundary is a rule of membership. A simple set \(S\) lists internal elements; the environment contains relevant nonmembers. In practice, one line rarely answers every concern. A physical boundary can follow an enclosure. A network authorization boundary can follow managed identities and connections. A safety boundary can include independent protection and human response. A legal boundary may follow jurisdiction and data responsibility. A responsibility boundary follows decision authority. Relate these views rather than forcing them into one misleading line.

Good boundary statements name inclusion and exclusion criteria. “The payment system includes the checkout service, ledger, settlement orchestration, operator console, and runbooks used to recover committed transactions. It excludes card networks and bank systems, which are external interacting systems governed through named interfaces and assumptions.” This is stronger than a rectangle labeled `Payments` because it explains why operators and procedures are inside while financial networks remain external.

The environment is more than weather or location. It includes natural conditions; infrastructure; other products and services; users, operators, maintainers, attackers, bystanders, and affected communities; laws and regulators; markets and suppliers; organizational incentives; information ecosystems; electromagnetic and mechanical conditions; and lifecycle settings. Relevant means capable of changing an outcome, constraint, assumption, risk, or evidence need—not merely directly connected.

Separate **external entity** from **external condition**. A utility is an entity with interfaces, policies, and possible authority. Ambient temperature is a condition. A regulation is an institutional constraint with an interpreting authority and jurisdiction. A market price is an environment variable sourced from some institution. Treating every external item as the same kind of box obscures how it can be observed, negotiated, controlled, or changed.

An interface is a contract surface, not just an arrow. For each crossing, record source, destination, direction, trigger, content, representation, units, range, rate, timing, ordering, quality, confidentiality, integrity, availability, error behavior, degraded behavior, ownership, versioning, and verification evidence as applicable. Human interfaces also carry meaning, workload, authority, attention, and accessibility obligations. Mechanical interfaces carry geometry, load, tolerance, and environmental conditions. The exact fields vary, but unnamed semantics are a risk.

Boundaries allocate responsibilities but do not create control. An internal supplier component may be opaque and weakly controlled. An external regulator can exert strong authority. A team can operate an external cloud service through a contract while lacking control over its implementation. Record **influence**, **control**, **ownership**, **operation**, **liability**, and **acceptance authority** separately. “We own it” does not prove we can change it, and “third party” does not remove accountability for choosing it.

Enabling systems deserve explicit treatment. Development tools, manufacturing equipment, test ranges, deployment pipelines, training systems, spare-parts supply, maintenance diagnostics, incident coordination, and disposal services may sit outside the delivered operational system. They still determine whether it can be produced, verified, introduced, sustained, modified, and retired. A system that works once in a prototype environment but cannot be calibrated or repaired is not lifecycle-ready.

Context is temporal. During development, simulators and test equipment dominate. During deployment, migration tools and legacy coexistence matter. During operation, users, support, suppliers, weather, traffic, and adversaries matter. During emergency mode, fallback communications and manual authority change. During retirement, data retention, hazardous materials, records, and replacement systems appear. Maintain context by lifecycle stage and operating mode instead of accumulating one timeless diagram.

Black-box analysis views the system through external behavior and constraints. White-box analysis exposes internal elements and relationships. Both are necessary. Begin black-box when defining outcomes and interfaces so that an early implementation does not become the requirement. Open the box when allocating functions, managing interaction, integrating, and verifying. At every decomposition level, restate the relevant environment: a subsystem interacts with sibling elements and enabling systems that were internal at the parent level.

Systems can be nested, overlapping, and federated. In a system of systems, constituent systems may retain independent ownership, objectives, evolution, and operation. A hospital, ambulance service, public network, and regional record exchange can cooperate in emergency care without one authority owning them all. Context must show governance, negotiation, incompatibility, and independent change—not disguise them as components under a fictional controller.

Assumptions bridge knowledge gaps: maximum operator response time, supplier availability, input distribution, environmental range, user training, stable regulation, or external-service behavior. Give each assumption an owner, rationale, evidence, confidence, expiration or trigger, and consequence if false. Convert critical assumptions into constraints, interface agreements, monitoring, tests, design margins, or contingency plans. An assumption register disconnected from architecture and decisions is administrative theater.

Constraints limit acceptable solutions: physical laws, sites, legacy compatibility, budgets, standards, policy, regulation, scarce skills, schedule, or mandated interfaces. Some constraints are negotiable and others are not; some are facts and others are inherited decisions. Identify source and authority. A preference described as law blocks alternatives; a legal obligation described as preference creates noncompliance risk.

Context models are decision instruments. A context diagram communicates topology, while a companion inventory supplies semantics. Scenario overlays show which entities and interfaces participate during a particular mission, fault, maintenance action, attack, or retirement event. An N-squared matrix or interface table exposes missing pairs. Maps, deployment views, organizational responsibility models, data-flow models, and hazard models contribute different context evidence. No single notation is universally complete.

The executable checker below evaluates a deliberately small context inventory. It requires every boundary-crossing interaction to identify an owner, contract, assumption, and operating mode, and every entity to have an authority. One external weather service and one maintenance interaction are intentionally incomplete.

<!-- bijux-verify: {"id":"system-context-consistency-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"entities=6\ncrossings=5\ncomplete_crossings=3\nfindings=maintenance_tool->controller.assumption,maintenance_tool->controller.contract,maintenance_tool.authority,weather_service->controller.assumption,weather_service.authority\n","stderr":""}} -->
```python
entities = {
    "controller": {"side": "inside", "authority": "product-owner"},
    "operator_console": {"side": "inside", "authority": "operations"},
    "sensors": {"side": "inside", "authority": "hardware-owner"},
    "utility": {"side": "outside", "authority": "grid-operator"},
    "weather_service": {"side": "outside", "authority": ""},
    "maintenance_tool": {"side": "outside", "authority": ""},
}

crossings = [
    {"source": "utility", "target": "controller", "owner": "energy-integration", "contract": "tariff-v2", "assumption": "updates-hourly", "mode": "normal"},
    {"source": "weather_service", "target": "controller", "owner": "forecast-integration", "contract": "forecast-v1", "assumption": "", "mode": "normal"},
    {"source": "operator_console", "target": "controller", "owner": "operations", "contract": "override-v3", "assumption": "trained-operator", "mode": "emergency"},
    {"source": "controller", "target": "utility", "owner": "energy-integration", "contract": "demand-response-v1", "assumption": "ack-within-30s", "mode": "degraded"},
    {"source": "maintenance_tool", "target": "controller", "owner": "service-engineering", "contract": "", "assumption": "", "mode": "maintenance"},
]

findings = []
for name, entity in entities.items():
    if not entity["authority"]:
        findings.append(f"{name}.authority")

complete = 0
for crossing in crossings:
    label = f"{crossing['source']}->{crossing['target']}"
    missing = [field for field in ("owner", "contract", "assumption", "mode") if not crossing[field]]
    findings.extend(f"{label}.{field}" for field in missing)
    complete += not missing

print(f"entities={len(entities)}")
print(f"crossings={len(crossings)}")
print(f"complete_crossings={complete}")
print(f"findings={','.join(sorted(findings))}")
```

This run establishes only consistency with four declared metadata rules in one synthetic inventory. It does not prove that the boundary is appropriate, entities are real, authorities are legitimate, contracts are adequate, assumptions hold, interfaces behave as modeled, or the heating system is safe, secure, lawful, usable, sustainable, or valuable.

## Definitions and Notation

Let \(U\) be the modeled universe for a stated concern and \(S\subset U\) the system-of-interest elements. The relevant environment is \(E\subseteq U\setminus S\), not necessarily every nonmember. A boundary-crossing relation \(I\subseteq(S\times E)\cup(E\times S)\) identifies directed interactions. Internal interactions lie in \(S\times S\); environmental relationships can also exist within \(E\) and still influence the system.

Let \(c\) denote concern, \(l\) lifecycle stage, \(m\) operating mode, and \(v\) viewpoint. Boundary membership can therefore be written \(B_{c,l,v}(x)\in\{inside,outside\}\). The notation makes an important point: a different legitimate concern can yield another boundary. Differences must be reconciled, not declared errors merely because lines differ.

An **operational context** describes use and interaction in intended operation. A **development context** covers creation and qualification. A **business or mission context** covers value, authority, and institutional environment. A **system context** is the relevant external relationship description for the selected system of interest. An **architecture description** expresses architecture for concerns; it is not the architecture or the actual system itself.

## Mechanisms, Invariants, or Proof Structure

Construct a bounded context through a repeatable reasoning chain:

1. **Name the decision and concern.** State why a system boundary is needed now.
2. **Select the system of interest.** Give inclusion and exclusion rules, owner, lifecycle stage, modes, and level of decomposition.
3. **Inventory environments.** Include technical, human, natural, organizational, economic, regulatory, security, and lifecycle factors.
4. **Identify external entities and enabling systems.** Record roles, authorities, independence, change cadence, and evidence sources.
5. **Specify crossings.** Give direction, content, semantics, units, timing, quality, failures, controls, and ownership proportional to risk.
6. **Overlay scenarios.** Test normal, peak, degraded, emergency, maintenance, transition, attack, recovery, and retirement cases.
7. **Audit assumptions and constraints.** Trace each to source, authority, evidence, monitoring, expiry, and consequence.
8. **Challenge the line.** Move candidate elements across the boundary and ask which cost, risk, responsibility, or outcome changes visibility.
9. **Baseline and evolve.** Version the context, connect it to decisions and requirements, and define change triggers.

The **closure invariant** is not that the system contains everything it depends on. It is that every material dependency and consequence is either governed inside or represented at the boundary with sufficient semantics, authority, assumptions, evidence, and contingency. Labeling something external never discharges the obligation to reason about it.

The **claim-scope invariant** says evidence supports only claims within the boundary and conditions it observes. A component test cannot prove a mission outcome. A laboratory test cannot prove behavior in an unmodeled climate. An interface schema cannot prove the supplier's operational availability. Trace the claim outward through enabling systems and context evidence until its actual limit is explicit.

The **no-displaced-harm invariant** asks whether moving an element or effect outside the system line merely moves an unwanted outcome out of the success measure. Waste, operator burden, inaccessible service, privacy impact, downstream risk, maintenance exposure, and retirement liability remain system consequences when stakeholders experience them.

## Alternatives and Trade-Offs

**Narrow versus broad boundaries.** Narrow scope improves ownership and tractability but creates more external dependencies. Broad scope captures outcomes and interactions but can become analytically and managerially unwieldy. Use nested models and explicit interfaces rather than choosing either extreme universally.

**Product versus capability framing.** Product boundaries align with engineering and procurement. Capability framing includes people, doctrine, facilities, data, and partner systems needed for an outcome. Preserve product accountability inside a broader operational capability context.

**Control versus influence.** Including an element suggests stronger design authority but may be organizationally false. Keeping it external can clarify independence while still modeling incentives, contracts, regulation, monitoring, and contingency.

**Stable baseline versus living context.** Baselines enable coordination and audit. A frozen model becomes false as suppliers, threats, law, use, and environments change. Version context and trigger review rather than editing history silently.

**Diagram versus model repository.** A diagram is accessible and reviewable. Structured models enable queries, traceability, consistency checks, and multiple views. Neither is automatically accurate; choose the smallest governed representation that supports decisions and evidence.

**One boundary versus boundary portfolio.** One line is easy to communicate but conflates concerns. Several related boundaries represent physical, operational, security, safety, data, authority, and lifecycle realities more faithfully, at the cost of reconciliation work.

## Failure Modes and Misconceptions

- **“The product is the system.”** The useful system of interest depends on the outcome and lifecycle concern.
- **“Outside scope means irrelevant.”** External dependencies and consequences often dominate success.
- **“Inside means controlled.”** Ownership, authority, influence, operation, and changeability differ.
- **“The context diagram is complete.”** Unlabeled arrows and absent conditions cannot support interface or assurance claims.
- **“People are users outside the technical system.”** Operators, maintainers, decision-makers, and affected people can be elements or essential context.
- **“The boundary is objective.”** It is a purposeful modeling and governance decision that needs rationale.
- **“One boundary serves every discipline.”** Safety, security, legal, physical, operational, and responsibility scopes frequently differ.
- **“Suppliers own supplier risk.”** Acquirers retain responsibility for selection, integration, monitoring, fallback, and outcome.
- **“Normal operation defines the environment.”** Degraded, emergency, transition, maintenance, attack, recovery, and retirement expose different entities and interfaces.
- **“An assumption is documentation, not design.”** Critical assumptions drive margins, monitoring, tests, contingencies, and acceptance.
- **“A standard diagram proves conformance.”** A notation or template can structure evidence but cannot establish substantive truth.
- **“Expanding scope always improves the model.”** Unbounded scope prevents decisions; relevance and nested abstraction remain necessary.

## Worked Examples

### Example 1

**Question:** Is a mobile banking application the system of interest?

**Reasoning:** It can be for a client engineering decision. For successful money movement, the useful context includes identity, APIs, ledgers, payment networks, devices, users, fraud operations, notifications, and dispute procedures. Several remain external but need explicit interfaces and authority.

**Conclusion:** Name the decision before naming “the system.”

### Example 2

**Question:** Should an operator be inside an industrial control system boundary?

**Reasoning:** For equipment procurement, perhaps external. For safe operation, operator perception, authority, workload, training, procedures, and recovery actions are part of the sociotechnical system behavior. Use related product and operational boundaries.

**Conclusion:** Human membership follows the claim, not a technology-only habit.

### Example 3

**Question:** A team says its hosted database is external because a vendor operates it. What is missing?

**Reasoning:** Record data and control interfaces, identity, regions, performance, backup/restore, failure notification, support, change policy, evidence, exit, jurisdiction, cost, and shared responsibility. External operation does not erase architectural dependence.

**Conclusion:** Third-party status changes governance, not relevance.

### Example 4

**Question:** Why maintain both a security authorization boundary and operational boundary?

**Reasoning:** The authorization boundary may include managed components and connections under one security authority. The operational boundary may include people, facilities, suppliers, and partner capabilities needed for outcomes. Mapping crossings exposes inherited controls and residual dependencies.

**Conclusion:** Related boundaries answer distinct acceptance questions.

### Example 5

**Question:** Is a test simulator part of the delivered system?

**Reasoning:** Usually not operationally, but it is an enabling system whose fidelity and configuration affect verification claims. Record which phenomena it models, excludes, calibrates, and how evidence transfers to the real environment.

**Conclusion:** Enabling systems constrain the credibility of lifecycle evidence.

### Example 6

**Question:** A context arrow says `weather -> controller`. Is that an interface definition?

**Reasoning:** No. Identify provider, observation type, units, geography, timestamps, update cadence, uncertainty, authentication, missing/stale behavior, authority, contractual quality, and fallback. Weather itself and a forecast service are different context items.

**Conclusion:** Arrows locate questions; contracts answer them.

### Example 7

**Question:** What changes when a system moves from pilot to national operation?

**Reasoning:** Jurisdictions, languages, accessibility, scale, support tiers, suppliers, threat exposure, data residency, training, maintenance, interoperability, and public consequences can change. Reusing the pilot boundary without review invalidates assumptions.

**Conclusion:** Scale and lifecycle change context, not merely quantities.

### Example 8

**Question:** Can a waste stream be excluded because disposal occurs after delivery?

**Reasoning:** Physical disposal can be external, but hazardous content, handling, records, liability, recyclability, retirement cost, and affected communities remain relevant lifecycle consequences.

**Conclusion:** A boundary must not hide displaced harm or retirement obligations.

### Example 9

**Question:** An autonomous passenger ferry is defined as vessel hardware and autonomy software. Is that adequate for safety approval?

**Reasoning:** No. Navigation waters, weather, charts, communications, ports, passengers, crew/remote operators, other vessels, rescue, maintenance, cybersecurity, regulations, accessibility, degraded control, evacuation, and organizational authority matter. Named naval architecture, marine operations, navigation, autonomy/software, electrical/mechanical, human-factors, accessibility, cybersecurity, functional-safety, environmental, search-and-rescue, port, regulator, passenger, maintenance, and independent assurance reviewers must judge the context and evidence. No external review is claimed.

**Conclusion:** High-stakes system boundaries require multidisciplinary authorization.

### Example 10

**Question:** When is a boundary good enough to baseline?

**Reasoning:** When it supports the current decisions; includes all material entities, conditions, crossings, assumptions, and authorities found by scenarios; identifies unknowns; relates other concern boundaries; has owners and review triggers; and records its claim limits.

**Conclusion:** A baseline is controlled current knowledge, not permanent truth.

## Cross-Program Connections

[Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) chooses software/domain boundaries inside a broader sociotechnical context. [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) structures software-intensive systems around concerns and decisions. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) maps data structure, flow, authority, and policy across organizational boundaries.

[Security Engineering](../../25-security-engineering/ROADMAP.md) identifies assets, adversaries, trust and authorization boundaries. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies directional communication context. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) shows how external nodes, networks, clocks, and failures change what can be known. [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) makes selected machine interfaces contractual.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) and [Cloud Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) often move operational responsibility across team and provider boundaries. Systems engineering retains ownership of whole-lifecycle outcomes, multidisciplinary interfaces, stakeholder validation, enabling systems, integration, trade-offs, risk, and evolution.

## References

- ISO/IEC/IEEE, [*15288:2023 — Systems and software engineering—System life cycle processes*](https://www.iso.org/standard/81702.html), second edition, 2023. Current common lifecycle-process framework for systems of interest, elements, and systems of systems.
- ISO/IEC/IEEE, [*42010:2022 — Software, systems and enterprise—Architecture description*](https://www.iso.org/standard/74393.html), second edition, 2022. Current requirements for architecture descriptions, stakeholders, concerns, viewpoints, and model kinds.
- ISO/IEC/IEEE, [*29148:2018 — Life cycle processes—Requirements engineering*](https://www.iso.org/standard/72089.html), confirmed current in 2024. Requirements and information-item guidance connected to system context and lifecycle processes.
- INCOSE, [*Systems Engineering Handbook: A Guide for System Life Cycle Processes and Activities*, fifth edition](https://www.incose.org/resource/incose-systems-engineering-handbook-a-guide-for-system-life-cycle-processes-and-activities-5th-edition/), Wiley, 2023. Current professional state-of-good-practice reference aligned with ISO/IEC/IEEE 15288:2023.
- NASA, [*NASA Systems Engineering Handbook*, NASA/SP-2016-6105 Rev 2](https://www.nasa.gov/reference/systems-engineering-handbook/), 2016. Public multidisciplinary lifecycle, design, realization, and technical-management guidance.
- Ron Ross, Mark Winstead, and Michael McEvilley, [*Engineering Trustworthy Secure Systems*](https://doi.org/10.6028/NIST.SP.800-160v1r1), NIST SP 800-160 Vol. 1 Rev. 1, 2022. Trustworthiness and security engineering in contested operational environments.
- IEEE Computer Society and INCOSE, [*Guide to the Systems Engineering Body of Knowledge (SEBoK)*](https://sebokwiki.org/wiki/Main_Page), living community-governed reference checked 2026-08-29. Systems knowledge, operational environment, lifecycle, and practice context.

## Exercises

### Exercise 1

Choose a university course-registration service. Define two legitimate systems of interest for different concerns, their inclusion/exclusion rules, and at least six context entities or conditions. Explain why neither boundary is universally correct.

### Exercise 2

Audit the claim “the payment processor is out of scope.” Produce an interface/context record covering authority, semantics, timing, failure, evidence, security, operations, change, and exit. Identify three assumptions that require owners.

### Exercise 3

For a home battery system, distinguish the product, operational capability, security authorization, safety, and lifecycle-support boundaries. Name at least one element that changes membership across views and explain the consequence.

### Exercise 4

Design a context-change review for a hospital scheduling pilot expanding to five regions. Include triggers, scenarios, model owners, evidence, and criteria for rejecting the old boundary.

### Exercise 5

A regional flood-warning capability combines river sensors, forecasts, telecommunications, public alerts, local authorities, and evacuation decisions. Define the system of interest, related boundaries, environments, interfaces, degraded modes, enabling systems, and named human-review roles required before operational acceptance.

## Answers to the Exercises

### Answer 1

For software delivery, the system of interest might include registration UI/API, rule engine, enrollment store, identity adapter, notification jobs, operator console, and recovery procedures; identity, payment, learning platforms, students, instructors, policy offices, networks, academic calendar, and law are context. For successful enrollment, a broader sociotechnical system may include students, advisers, registrars, accessibility support, academic policy, identity and payment coordination, communications, and exception procedures, while vendor infrastructure remains external. The first supports implementation accountability; the second supports outcome validation and equity. Neither answers every security, legal, organizational, or lifecycle concern, so related boundaries must be maintained.

### Answer 2

Record source/destination parties, transaction identifiers and meanings, currencies/units, idempotency, authorization, ordering, deadlines, reconciliation, disputes, duplicate/late responses, outage behavior, confidentiality/integrity, authentication, audit, retention, service levels, incident notification, evidence access, support, versioning, regulatory authority, ownership, cost, data location, portability, termination, and migration. Critical assumptions might be settlement completes within an agreed window, provider identifiers remain stable and unique, and evidence is available for disputes; each needs a named product/finance, integration, legal/compliance, or operational owner, monitoring, and contingency. “Out of scope” can delimit implementation but cannot erase dependency or accountability.

### Answer 3

The product boundary can include inverter, battery modules, controller, enclosure, local sensors, and firmware. Operational capability adds installer, homeowner interaction, utility signals, premises loads, network service, tariffs, and support. A security authorization boundary may include managed cloud/mobile identities and communication endpoints. A safety boundary includes protection devices, wiring, fire behavior, isolation, emergency responders, installation, ventilation, and physical environment. Lifecycle support includes manufacturing tests, logistics, installer tools, diagnostics, spares, software signing/update, recycling, and hazardous-material handling. The mobile/cloud service can be external to the physical product yet inside a managed security boundary; treating it only as external would hide compromise and availability obligations.

### Answer 4

Trigger review on new jurisdiction, hospital/EHR interface, language, accessibility population, clinical workflow, identity authority, regulation, hosting region, supplier, scale threshold, incident, or material assumption failure. Re-run normal, peak, downtime, emergency override, correction, privacy request, cyber incident, staff change, maintenance, upgrade, and retirement scenarios with clinicians, schedulers, patients, accessibility, privacy/legal, security, operations, integration, regional and independent reviewers. Owners update entity/interface inventories, authority maps, assumptions, hazards, requirements and evidence links. Reject the pilot boundary if it omits a material stakeholder or consequence, assumes one-region authority, lacks cross-region correction/recovery, cannot assign interface ownership, or cannot support validation and compliance claims.

### Answer 5

One defensible system of interest is the regional warning capability: sensing, data quality, fusion/forecast interpretation, warning decision, alert composition/distribution, authority coordination, public feedback, monitoring, fallback and learning procedures. Related technical, security/data, public-authority, safety, geographic and lifecycle boundaries should be mapped. Environment includes watersheds, weather, terrain, power, telecoms, communities, languages, disability/access needs, roads, media, jurisdictions, adversaries and climate change. Interfaces carry measurements, uncertainty, forecasts, thresholds, authorization, alert content, acknowledgements and observations with units, timing, provenance, quality and failure semantics. Test sensor loss/bias, forecast outage, power/network/site failure, conflicting authorities, delayed or false alerts, overload, inaccessible channels, misinformation, night staffing and recovery. Enabling systems include calibration, maintenance, training, exercises, mapping, telecom agreements, public education, incident command, records and post-event analysis. Named reviewers include hydrologists, meteorologists, geospatial specialists, sensor/telecom/software engineers, emergency management, local authorities and responders, dam/water operators where relevant, safety/risk, cybersecurity, privacy/legal/records, human-factors and accessibility experts, multilingual/public communication, community representatives, maintenance/operations, environmental authorities, regulators and independent assurance. Models and automated checks cannot authorize evacuation policy, establish public comprehension, prove forecast validity, resolve jurisdiction, or replace field exercises and named review; no external acceptance is claimed.
