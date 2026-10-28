---
module_id: SARCH-021
program: Software Engineering: Software Architecture
level: 1
module_number: 21
title: Context Views
status: complete
last_verified: 2026-09-06
---

# Context Views

## One-Page Review

### Governing question

How can an architecture description show the system of interest in its environment so that stakeholders agree on scope, external responsibilities, crossings, dependencies, and consequences before discussing internal structure?

### Essential definitions

- The **system of interest** is the entity whose architecture is being described.
- A **boundary** distinguishes responsibilities assigned to the system from those assigned to its environment; it is a decision, not merely a box.
- An **external entity** is a person, role, organization, device, service, system, authority, or environment that interacts materially with the system of interest.
- A **relationship** states a meaningful interaction, dependency, influence, or exchange between entities.
- A **boundary crossing** transfers information, control, material, energy, authority, money, or responsibility across the system boundary.
- An **interface** is a governed point or set of points through which a crossing occurs.
- A **context viewpoint** defines conventions for constructing and interpreting context views; a **context view** applies them to one system and concerns.
- A **legend** defines notation, direction, scope, line meaning, and status.
- A **scope claim** states what the view includes, excludes, and leaves unresolved.

### Central model, mechanism, or theorem

Model a context view as a labeled directed multigraph $G=(V,E)$ with distinguished system node $s\in V$, external nodes $V_{ext}=V\setminus\{s\}$, and crossings $e=(u,v,\lambda)$. Label $\lambda$ identifies semantics, direction, trigger, authority, sensitivity, timing, and failure expectations appropriate to the concern. Multiple edges may connect the same entities because request, response, notification, money, and operational control have different meanings.

A view is adequate only relative to declared stakeholders, concerns, scenarios, lifecycle state, and evidence. Diagram neatness does not prove boundary correctness or completeness.

### Critical invariants

- name exactly one system of interest and the purpose and lifecycle state of the view;
- distinguish owned responsibility from external dependency and shared responsibility;
- show every material human, organizational, software, device, and environmental entity needed by the scoped scenarios;
- label relationships with domain meaning rather than generic “uses” arrows;
- make direction, initiation, authority, and trust interpretation unambiguous;
- identify critical, sensitive, regulated, safety-related, or failure-prone crossings;
- preserve asynchronous, batch, event, manual, and physical interactions—not only APIs;
- reconcile the view with scope, contracts, quality scenarios, data flows, deployment, and operations;
- record assumptions, exclusions, unknowns, owners, evidence, and review triggers;
- split views by concern when one diagram can no longer be read honestly.

### Common failures

Common failures include drawing the organization instead of the system; showing databases and modules inside a context view; omitting people, operators, regulators, physical processes, files, and support; using unlabeled bidirectional arrows; confusing caller with authority; treating a supplier as controlled; hiding shared identity and network dependencies; depicting an API without callbacks or failure; mixing current and target states; claiming completeness because all visible boxes fit; and copying a context diagram that no longer matches production.

### Compact example

For a payroll system, the boundary encloses payroll calculation and payment-instruction preparation. Employee, payroll administrator, HR system, time-recording system, identity provider, bank, tax authority, and support operator remain external. Label crossings such as “approved employment and tax data,” “validated time records,” “signed payment instruction,” “bank acceptance or rejection,” and “statutory report.” This exposes authority and failure far better than arrows labeled “data.”

### Connections

[SARCH-002](002-stakeholders-and-architectural-concerns.md) supplies stakeholders and concerns; [SARCH-003](003-functional-scope-and-system-context.md) establishes functional scope; [SARCH-009](009-architecture-decision-records.md) records boundary decisions; [SARCH-020](020-resolving-quality-attribute-conflicts.md) resolves competing boundary consequences. [SARCH-022](../ROADMAP.md) and [SARCH-023](../ROADMAP.md) introduce internal module and runtime structures.

## Governing Question

Architecture discussions often begin with boxes and arrows, yet participants silently assign different meanings to the outer box. One person thinks payment belongs inside the product; another thinks it is a supplier service. Operations includes manual correction; development ignores it. Security sees the identity provider as external; product treats sign-in as guaranteed infrastructure.

The governing problem is how to describe the system as one entity among people, organizations, technologies, authorities, and physical conditions. A useful context view makes boundary choices and crossings reviewable without prematurely decomposing the system into internal parts.

## Why This Matters

The system boundary allocates responsibility. If tax calculation is outside payroll, a supplier contract, failure response, reconciliation path, and change mechanism become architecturally significant. If it is inside, the system owns rules, evidence, release, and jurisdictional change. Moving a line changes more than drawing.

Many serious failures occur between systems: duplicated payment after an ambiguous timeout, inaccessible identity recovery, stale files, callbacks blocked by a firewall, an operator unable to override automation, or a cloud dependency unavailable during regional failure. Internal component diagrams cannot establish that the end-to-end task is covered.

Context views also shape communication. Executives need mission and organizational dependencies; engineers need semantic crossings; security reviewers need trust and authority; privacy reviewers need data subjects, controllers, processors, and jurisdictions; operators need control and escalation paths. One base model can support several concern-specific projections without forcing all information into one unreadable picture.

## Prerequisites and Retrieval

Retrieve architecture, architecture description, stakeholder, concern, system of interest, environment, scope, responsibility, boundary, external entity, relationship, dependency, interface, contract, authority, trust, data flow, control flow, lifecycle state, current state, target state, scenario, evidence, and residual risk.

From earlier modules, retrieve stakeholder representation, functional scope, quality scenarios, constraints, ASRs, decisions, and conflict resolution. You should be able to distinguish the conceptual system boundary from a process, repository, deployment, network, legal, or organizational boundary.

## Learning Objectives

After completing this module, you should be able to:

1. state the purpose, audience, concerns, and lifecycle state of a context view;
2. choose and name one system of interest;
3. identify material human, organizational, software, device, and environmental entities;
4. label boundary crossings with domain semantics, direction, trigger, and authority;
5. distinguish responsibility, dependency, interface, trust, and deployment boundaries;
6. represent synchronous, asynchronous, batch, manual, and physical interactions;
7. project one context model into readable concern-specific views;
8. check context coverage against scenarios and other architecture views;
9. detect ambiguous, stale, overloaded, or misleading context diagrams;
10. maintain boundary decisions and evidence through system evolution.

## Core Exposition

**State the view's job.** An architecture view addresses named concerns for named stakeholders using conventions defined by a viewpoint. ISO/IEC/IEEE 42010:2022 is the current published edition of the architecture-description standard as checked on 2026-09-06; it distinguishes an architecture from the work product that expresses it and defines viewpoints as conventions for constructing and using views [1]. A context view is therefore not “the architecture.” It is a purposeful representation.

Record title, system of interest, version or time, current or target state, lifecycle conditions, audience, concerns, notation, and exclusions. A diagram without this framing invites readers to infer incompatible meanings.

**Choose one system of interest.** Name the product, service, platform, enterprise capability, device, or system-of-systems element being described. Avoid ambiguous labels such as “backend” or “solution.” If the subject is a payment capability, do not alternate between one service, the entire commerce estate, and the owning department.

The system can be shown as one opaque node in a context view. Internal databases, services, modules, threads, and deployment nodes belong in later views. Showing them early anchors discussion on a current solution and makes the outer boundary harder to see.

**Treat the boundary as responsibility.** Ask what outcomes, rules, data, decisions, failures, evidence, and operations the system owns. A repository boundary says where code lives; a deployment boundary says what is released; a network boundary says where traffic is controlled; a legal boundary says who has obligations. These may align, but none automatically defines the conceptual system boundary.

Some responsibilities are shared. Mark the split explicitly: the identity provider authenticates a credential; the application authorizes a payroll action; a bank accepts a payment instruction; payroll reconciles the outcome. “External” means outside direct system responsibility, not unimportant or untrusted.

**Discover external entities from scenarios.** Walk intent, normal completion, rejection, timeout, cancellation, recovery, dispute, audit, maintenance, and retirement. Include people in roles rather than only software: customer, operator, administrator, support agent, auditor, affected non-user, and emergency authority. Include organizations when contracts or duties matter.

Include devices, sensors, actuators, networks, files, message brokers, external services, physical environments, clocks, and manual processes when they influence outcomes. A weather service may be an external software system; rainfall and river level are environmental phenomena; a gate actuator is a physical entity. Collapsing these hides different evidence and control.

**Label relationships semantically.** “Uses,” “calls,” and “data” seldom explain responsibility. Prefer “submits signed payment instruction,” “publishes allocation decision,” “receives revocation event,” or “operator authorizes emergency stop.” State direction from producer to consumer and distinguish initiation from authority. The caller is not necessarily the source of truth.

Because context is a multigraph, one pair of entities can have several crossings. A provider receives requests, returns acknowledgments, later emits settlement events, and sends invoices. Combining these into one bidirectional arrow erases timing, failure, and reconciliation.

For each material crossing, maintain details outside or beside the diagram: semantic payload, trigger, protocol or medium, frequency and volume, latency, ordering, identity, authorization, confidentiality, integrity, retention, error, retry, idempotency, availability, owner, version, evidence, and change process. Show only the details needed for the view's concern.

**Distinguish interaction modes.** Synchronous request-response couples availability and latency during a call. Asynchronous messages introduce delivery, ordering, duplication, and lag. Batch files introduce schedule, completeness, naming, encryption, partial processing, and reconciliation. Manual interactions introduce hours, training, workload, authority, accessibility, and error. Physical crossings add units, sampling, calibration, actuation, delay, and safety.

Do not draw a logical exchange as if it proves a transport. “Provides employment status” may be implemented through an API, event, file, or manual approval. State abstraction level. If protocol choice is architecturally fixed, label it as a constraint or link to the contract.

**Expose dependency without surrendering responsibility.** A supplier can be external while the system remains accountable for user outcome. Record assumptions, service expectations, failure modes, exit, monitoring, fallback, and reconciliation. External services are not reliable merely because their boxes lie outside the line.

Shared infrastructure deserves explicit treatment when it can fail or change independently. Identity, DNS, certificate authorities, network transit, time synchronization, secrets, support, and deployment control planes are commonly omitted because teams call them “platform.” Include them in the view that addresses availability, security, recovery, or operation.

**Project concerns rather than overload.** Maintain a common context model, then create projections. A functional projection emphasizes actors and capabilities. A data projection emphasizes categories, purposes, stores outside the boundary, and jurisdictions. A security projection emphasizes trust, identity, privilege, and adversarial crossings. An operational projection emphasizes telemetry, control, escalation, and supplier support.

Projections must preserve entity identity and relationship semantics. If the same external system has three names across diagrams, reviewers cannot reconcile it. A legend should explain line types and omissions. Color alone must not carry meaning.

The C4 model's official guidance positions the system context diagram as the highest-level view of a software system, showing users and other systems while deliberately omitting internal detail [5]. This is a useful lightweight convention, not a proof that every stakeholder concern or boundary crossing is covered.

**Check coverage with scenarios.** Let each scenario identify participants and crossings. For every required external interaction, locate a corresponding node and edge. For every edge, find at least one scenario, requirement, decision, or operational obligation that justifies it. Unmapped scenarios suggest omissions; unjustified edges suggest accidental scope or stale content.

Coverage is relative to known scenarios. Stakeholder discovery can be incomplete, and a view can omit indirect affected parties. Review incidents, complaints, contracts, data inventories, threat models, support procedures, deployment dependencies, and physical walkthroughs to challenge the known set.

**Reconcile other views.** Internal module and component views should implement responsibilities assigned inside. Runtime views should realize crossings with compatible direction and semantics. Deployment views should locate endpoints without changing logical ownership. Data views should agree on categories and authorities. Operational views should include monitoring and control for critical dependencies.

A mismatch is a finding, not an invitation to silently edit the picture. Determine whether scope, implementation, contract, or documentation is wrong. Record the decision and consequences.

**Show uncertainty and evolution.** Mark proposed, existing, deprecated, unknown, and conditional relationships distinctly. Never mix current and target state without a legend. If a migration temporarily supports old and new providers, show both and state traffic, authority, reconciliation, rollback, and removal conditions.

Assign owners and review triggers. Revisit context after a new supplier, jurisdiction, user group, protocol, identity mechanism, operational model, acquisition, incident, or scope change. Validate critical crossings against observed configuration and contracts; a diagram generated from traffic alone misses dormant, manual, denied, and failure paths.

## Definitions and Notation

Represent a context model as a labeled directed multigraph

$$
G=(V,E,s),\qquad s\in V,\qquad V_{ext}=V\setminus\{s\}.
$$

Each edge $e=(u,v,\lambda)$ is a crossing or material influence. Label $\lambda$ may contain

$$
\lambda=(meaning,trigger,mode,authority,sensitivity,timing,failure,owner).
$$

The tuple is a review schema, not a requirement to print every field on one diagram. Multiple edges between $u$ and $v$ preserve distinct semantics.

Let $Q_K$ be known scoped scenarios and $cross(q)$ the crossings required by scenario $q$. Structural scenario coverage is

$$
Coverage(G,Q_K)\iff \forall q\in Q_K,\ cross(q)\subseteq E.
$$

This predicate checks modeled correspondence only. It does not prove that $Q_K$ is complete, edges are implemented, contracts are correct, or users achieve outcomes.

Let $R(s)$ be responsibilities assigned inside the system and $R(x)$ those assigned to external entity $x$. A shared responsibility should be decomposed into accountable parts rather than appearing in both sets without explanation. The sets are governance claims, not facts inferred from a deployment diagram.

## Mechanisms, Invariants, or Proof Structure

Use this context-view mechanism.

1. **Frame:** name the system, purpose, audience, concerns, lifecycle state, and notation.
2. **Bound:** state owned, external, shared, excluded, conditional, and unresolved responsibilities.
3. **Walk scenarios:** trace normal, rejection, failure, recovery, support, operation, and retirement.
4. **Identify entities:** include people, organizations, systems, devices, environments, and authorities.
5. **Label crossings:** state domain meaning, direction, initiation, authority, mode, and consequence.
6. **Annotate risks:** record sensitivity, trust, timing, volume, failure, evidence, ownership, and change.
7. **Project:** create readable concern-specific views from one reconciled context model.
8. **Cross-check:** map scenarios to edges and edges to justified obligations.
9. **Reconcile:** compare scope, contracts, data, runtime, deployment, security, and operational descriptions.
10. **Govern:** validate with stakeholders, record unknowns, assign owners, and define update triggers.

The governing invariants are one named system, explicit purpose, responsibility-based boundaries, material-entity coverage, semantic directed crossings, visible authority and dependency, concern-appropriate projection, scenario traceability, cross-view consistency, and lifecycle maintenance.

If $Coverage(G,Q_K)$ holds, every crossing already identified by every known scoped scenario appears in the model. The proof follows directly from the subset condition. It cannot establish discovery completeness or behavioral correctness; those require independent stakeholder, domain, implementation, and operational evidence.

## Alternatives and Trade-Offs

**One context diagram** is easy to find and can establish a shared base. It becomes unreadable across functional, security, data, operational, and physical concerns. **Several projections** improve focus but can drift. Generate or review them against stable entity and relationship identities.

**Informal boxes and arrows** are accessible and fast. Their semantics depend heavily on labels and legends. **Formal models** support queries, consistency, and generation but cost more to learn and maintain. Choose rigor proportional to consequence and change rate.

**Organization-based boundaries** clarify budgets and teams but can fossilize a temporary structure. **Responsibility-based boundaries** better express system behavior but may cross funding or supplier lines. Show organizational ownership as an annotation, not a substitute for system scope.

**Static documentation** supports deliberate review and includes dormant or manual paths. It becomes stale. **Discovery from code, configuration, or traffic** supports current observations but misses intended, conditional, denied, offline, and human interactions. Reconcile declared and observed models.

**Logical relationships** remain durable across protocol change. **Physical or protocol detail** is necessary for deployment, security, and operation. State abstraction and link related views instead of mixing levels invisibly.

## Failure Modes and Misconceptions

- **“The outer box is obvious.”** Stakeholders often disagree about ownership, suppliers, and manual work.
- **“External means someone else's problem.”** The system can remain accountable for end-to-end outcome and fallback.
- **“A context view shows the major components.”** Internal decomposition belongs to module or component-and-connector views.
- **“One arrow is one API call.”** A relationship may be logical, asynchronous, batch, manual, or physical.
- **“Bidirectional arrows save space.”** They usually hide distinct authority, timing, and failure semantics.
- **“Users are outside the technical architecture.”** Human interaction and operational authority are material crossings.
- **“The platform need not be shown.”** Shared identity, network, time, and control planes can dominate failure.
- **“Trust follows the network boundary.”** Identity, authority, data, organization, and execution have different boundaries.
- **“Traffic discovery produces the context.”** It observes selected runtime paths, not intent, denial, dormant recovery, or manual processes.
- **“C4 level 1 proves completeness.”** A notation organizes communication; evidence and stakeholder review establish bounded adequacy.
- **“Current and target can share a picture.”** Only with explicit status and transition semantics.
- **“More detail is more accurate.”** Mixed abstraction can obscure the boundary and create false authority.
- **“A clean diagram is correct.”** Visual quality cannot prove scope, contracts, behavior, or current production state.

## Worked Examples

### Example 1

**Question:** What belongs on the context view for an online shop's checkout system?

**Reasoning:** Show checkout as one system. External entities include shopper, catalog/pricing authority, inventory system, identity provider, payment provider, fraud service, fulfillment system, notification provider, support agent, and tax authority or service where material. Label “reserves stock,” “submits authorized payment,” “returns acceptance or rejection,” and “creates fulfillment order.” Do not show checkout's internal database or services yet.

**Conclusion:** Context describes owned capability and external crossings before internal structure.

### Example 2

**Question:** A context diagram contains web tier, worker, queue, and three databases. What is wrong?

**Reasoning:** It mixes internal component and deployment detail into a view intended to establish system/environment scope. Collapse those nodes into the system of interest. Restore omitted users, suppliers, operators, authorities, and physical or manual dependencies. Link to internal views for the decomposition.

**Conclusion:** Mixing abstraction levels can make a detailed diagram context-poor.

### Example 3

**Question:** A payroll application calls an identity provider. Does the caller own authorization?

**Reasoning:** Not necessarily. The provider may authenticate a credential and assert identity attributes; payroll still decides whether that identity may approve a run. Use separate crossings for authentication request/result and administrative provisioning. Label identity evidence, payroll authorization, revocation, outage, and recovery responsibilities.

**Conclusion:** Direction of a call does not determine authority.

### Example 4

**Question:** A privacy view shows “customer data” flowing to analytics. Is that sufficient?

**Reasoning:** No. Identify data categories, subjects, purpose, controller or responsible owner, processor, jurisdiction, retention, aggregation, access, deletion, and opt-out or legal basis as applicable. Separate telemetry necessary for operation from product analytics. Link the crossing to a data inventory and governing decision.

**Conclusion:** Domain labels must expose the semantics needed by the concern.

### Example 5

**Question:** Why show shared DNS and identity in an availability context projection?

**Reasoning:** Both can fail independently while every application component remains healthy. Map resolution, token issuance, validation keys, cached behavior, expiry, monitoring, control, and recovery. Determine whether a regional or control-plane failure removes all user paths. “Platform owned” does not remove dependency.

**Conclusion:** Shared infrastructure belongs in a view when it shapes the scoped outcome.

### Example 6

**Question:** How should a nightly supplier file be represented?

**Reasoning:** Use separate directed crossings for the encrypted input file, receipt acknowledgment, validation report, correction, and reconciliation. Record schedule, timezone, naming, schema version, completeness marker, checksum, key ownership, duplicate handling, partial processing, retention, and escalation. A single “supplier integration” arrow hides the workflow.

**Conclusion:** Batch crossings require timing, completeness, and recovery semantics.

### Example 7

**Question:** A support agent manually corrects a failed booking. Is the agent part of context?

**Reasoning:** Yes. Show the support role, authenticated case access, evidence reviewed, permitted corrections, customer confirmation, audit, and escalation. The internal support tool remains opaque unless it is a separate system. Include hours, accessibility, privacy, workload, and dependency failure in relevant projections.

**Conclusion:** Manual recovery is architectural behavior, not an invisible exception.

### Example 8

**Question:** A payment provider returns an HTTP timeout. What context relationships are missing if the diagram only shows “send payment”?

**Reasoning:** Add immediate acknowledgment or ambiguity, later status query, settlement event, reconciliation report, refund or reversal, dispute, and support escalation as applicable. Label operation identity and authority. Timeout means the caller lacks a response; it does not prove the provider performed no side effect.

**Conclusion:** Failure and reconciliation crossings complete the end-to-end relationship.

### Example 9

**Question:** During migration, provider A and B appear without status. What must the view say?

**Reasoning:** Mark current and target use, traffic allocation, authoritative record, dual-write or translation, comparison, fallback, rollback, and removal conditions. State which scenarios use each provider and how inconsistent outcomes reconcile. Do not imply both are permanently equivalent.

**Conclusion:** Lifecycle state and transition semantics prevent a context view from lying during change.

### Example 10

**Question:** What belongs in a railway-crossing control context view?

**Reasoning:** Show controller as the system of interest; external train-detection equipment, barrier actuator, road signals, train signaling authority, operator, maintenance personnel, power, communications, clock, physical crossing, road users, and emergency services as relevant. Label sensed occupancy, commanded and observed barrier state, manual authority, alarms, fail-safe behavior, and degraded operation. No external railway, civil, control-systems, accessibility, emergency, safety, regulatory, security, human-factors, or practitioner review is claimed; named qualified authorities and affected operators and communities must validate scope, hazards, evidence, and release.

**Conclusion:** Physical, human, software, and authority boundaries must coexist in high-consequence context.

## Cross-Program Connections

- [Software Engineering: Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) owns domain concepts and code-level responsibility design inside and across bounded models.
- [Software Engineering: Methods & Evolution](../../10-software-engineering-methods-and-evolution/ROADMAP.md) owns stakeholder discovery, requirements, and lifecycle change that reveal context entities.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns enterprise data authority, conceptual information structures, lineage, and data governance.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) owns transport paths and network boundaries used by logical crossings.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns trust, identity, threat, privilege, and protection analysis across the context.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns system boundaries across software, people, organizations, physical elements, lifecycle, and assurance.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 42010:2022, Software, systems and enterprise—Architecture description](https://www.iso.org/standard/74393.html), edition 2, November 2022. Architecture descriptions, stakeholders, concerns, viewpoints, views, model kinds, and correspondence; consulted 2026-09-06.
2. Paul Clements, Felix Bachmann, Len Bass, David Garlan, James Ivers, Reed Little, Paulo Merson, Robert Nord, and Judith Stafford. *Documenting Software Architectures: Views and Beyond*, 2nd edition. Addison-Wesley, 2010. View selection, context diagrams, interfaces, variability, and documentation packages.
3. Nick Rozanski and Eoin Woods. *Software Systems Architecture: Working With Stakeholders Using Viewpoints and Perspectives*, 2nd edition. Addison-Wesley, 2011. Context viewpoint, stakeholders, concerns, perspectives, and cross-view consistency.
4. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, 4th edition. Addison-Wesley, 2021. Architectural structures, stakeholders, quality attributes, interfaces, and evaluation.
5. Simon Brown. [System context diagram](https://c4model.com/diagrams/system-context), C4 model official documentation. People, software systems, scope, and intentionally omitted internal detail; consulted 2026-09-06.
6. Gernot Starke and Peter Hruschka. [arc42 Template: Context and Scope](https://docs.arc42.org/section-3/), arc42 documentation. Business and technical context, external interfaces, and scope; consulted 2026-09-06.
7. Ron Ross, Mark Winstead, and Michael McEvilley. [NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final), November 2022. System boundaries, environments, protection needs, trustworthiness, and lifecycle engineering; consulted 2026-09-06.

## Exercises

### Exercise 1

Define system of interest, boundary, external entity, crossing, interface, viewpoint, and view for a university course-registration capability.

### Exercise 2

Given known scenarios with crossing sets $\{a,b\}$, $\{b,c,d\}$, and $\{a,d\}$, determine coverage for context edge sets $E_1=\{a,b,c\}$ and $E_2=\{a,b,c,d\}$. State what the result cannot prove.

### Exercise 3

Diagnose a context diagram that mixes services and databases, omits users and operations, uses unlabeled bidirectional arrows, hides a shared identity provider, combines current and target suppliers, and claims completeness from traffic discovery.

### Exercise 4

Design functional, security, data, and operational context projections for a payroll system while preserving one reconciled model.

### Exercise 5

Construct and assure a context view for an unfamiliar municipal drinking-water dosing system. Include physical, human, organizational, software, authority, failure, evidence, and readiness concerns.

## Answers to the Exercises

### Answer 1

The system of interest is the named registration capability responsible for validating and committing course selections, not automatically the whole university. Its boundary assigns schedule search, selection rules, enrollment state, rejection, and confirmation according to the declared scope. External entities may include student, registrar, identity provider, course catalog, prerequisite-record authority, capacity authority, billing, notification, accessibility support, and audit or reporting systems.

Crossings include authenticated identity evidence, course and prerequisite facts, selection command, authoritative acceptance or rejection, billing consequence, and confirmation. An interface is the governed API, message, file, or human procedure through which a crossing occurs. The context viewpoint defines how such entities and crossings are modeled for stakeholder concerns; the context view is the actual current or target representation for this registration capability.

### Answer 2

For $E_1$, scenario one is covered, but scenario two requires $d$ and scenario three also requires $d$; therefore $Coverage(G,Q_K)$ is false. $E_2$ contains every crossing in all three sets, so modeled structural coverage is true.

The result cannot prove that the scenario set is complete, the edge semantics are correct, the interfaces exist, implementations conform, dependencies behave, or users complete registration. It also says nothing about quality responses, authority, failure, or evidence unless those are modeled and reviewed separately.

### Answer 3

First name one system and collapse internal services and databases into it; preserve decomposition in linked module, component, and deployment views. Restore users, operators, support, auditors, organizations, devices, and environments revealed by scenarios. Replace bidirectional arrows with separate directed, semantically labeled crossings. Add shared identity because its availability, security, and recovery shape system outcomes.

Mark current and target suppliers, traffic, authority, migration, reconciliation, rollback, and removal separately. Treat traffic discovery as one observation source: it misses denied, dormant, offline, batch, manual, failure, recovery, and future paths. Cross-check scenarios, contracts, configuration, data inventories, threat models, support procedures, incidents, and stakeholder review. Record unknowns rather than claim completeness.

### Answer 4

Maintain stable IDs for payroll, employee, payroll administrator, HR authority, time-recording authority, identity provider, bank, tax authority, notification provider, support, and audit parties. The functional projection shows employment and time facts, payroll initiation, calculation outcome, payment instruction, statutory report, and correction. The security projection adds authentication, authorization, key or certificate authority, privileged operation, revocation, audit, and adversarial crossings.

The data projection identifies payroll, identity, bank, tax, telemetry, and support categories; purposes; authorities; jurisdictions; retention; and deletion or correction. The operational projection shows health and outcome telemetry, alert routing, supplier support, control, manual recovery, reconciliation, deployment control dependencies, and escalation. Each projection uses the same entity and relationship identities, declares omissions, and links detailed contracts. Reconcile conflicting direction, ownership, lifecycle state, and failure assumptions before approval.

### Answer 5

Name the dosing controller or broader dosing capability precisely. External entities can include raw-water sensors, laboratory results, flow meters, chemical tanks, pumps and valves, treatment operator, maintenance technician, supervisory control, power, network, time source, water-quality authority, public-health authority, incident command, downstream distribution, and affected communities. Label measured values and units, sample time and validity, commanded dose, observed actuation, manual authority, alarms, calibration, inventory, reporting, and emergency communication.

Create safety, security, data, operational, and accessibility projections. Trace normal, sensor disagreement, stale sample, pump failure, communication loss, power loss, unauthorized command, over-dose, under-dose, maintenance, manual operation, recovery, and public warning. Reconcile context with hazard analysis, control logic, physical diagrams, procedures, contracts, deployment, and observed configuration.

No external water-treatment, chemistry, public-health, civil, control-systems, accessibility, environmental, safety, regulatory, security, human-factors, or practitioner review is claimed. Named qualified authorities, operators, and affected communities must validate boundary, units, safe limits, authority, alarms, tests, emergency procedures, release, and residual risk. Unknown safe bounds, ambiguous authority, unverified sensor or actuator crossings, inaccessible alarms, absent manual control, or unresolved emergency communication blocks readiness.
