---
module_id: SARCH-003
program: Software Engineering: Software Architecture
level: 1
module_number: 3
title: Functional Scope and System Context
status: complete
last_verified: 2026-09-05
---

# Functional Scope and System Context

## One-Page Review

### Governing question

What capabilities belong to the software system under design, what remains in its environment, and which actors, neighboring systems, flows, constraints, and responsibilities cross the boundary?

### Essential definitions

- **functional scope** is the set of externally meaningful capabilities and responsibilities assigned to the system for a stated purpose and lifecycle stage.
- The **system of interest** is the entity whose boundary and architecture are being reasoned about.
- A **boundary** distinguishes responsibilities controlled as part of that system from environmental responsibilities; it is a design and governance claim, not a drawn rectangle alone.
- **context** comprises external people, systems, organizations, physical conditions, policies, and events that interact with or materially influence the system.
- An **external actor** initiates, receives, or governs behavior across the boundary; it may be human, organizational, or automated.
- A **neighboring system** is an external computational system with an in-scope relationship.
- An **external interface** is a governed interaction point across the boundary, including information, control, material, energy, or human procedure where relevant.
- A **context view** represents the system of interest and relevant external relationships for named concerns; it is not a deployment or component view.
- **ownership** is accountable authority for behavior and change; physical hosting, procurement, operation, and data authority may have different owners.

### Central model, mechanism, or theorem

Model context as a typed directed multigraph $G=(V,E)$ with distinguished system node $s$. Each external node has a role and owner. Each edge records direction, exchanged meaning, trigger, interface, trust/failure boundary, service expectation, and evidence. Functional scope assigns each capability to $s$, an external node, shared responsibility, or explicitly unresolved state.

The boundary is adequate for a decision only when every material scenario can be traced through owned capabilities and boundary crossings, and every crossing has semantics and responsibility. This is a review obligation, not a proof that discovery is complete.

### Critical invariants

- name one system of interest, purpose, lifecycle stage, decision, and abstraction level;
- distinguish capability from implementation, organization, deployment, and product name;
- identify direct and indirect actors, neighboring systems, governing authorities, and operational humans;
- label relationships with direction and business meaning rather than “uses”;
- record ownership of capability, interface, data, operation, failure response, and change;
- include inbound, outbound, scheduled, asynchronous, administrative, observability, recovery, and exceptional flows;
- expose trust, failure, jurisdiction, and responsibility crossings;
- trace scope to stakeholder concerns, scenarios, assumptions, constraints, and acceptance evidence;
- version the context and reopen it after dependency, ownership, regulation, incident, or lifecycle change.

### Common failures

Common failures include treating a product name as a boundary; drawing the organization chart; listing only happy-path users; hiding administrators and batch jobs; showing databases and queues inside a context view; labeling every arrow “uses”; omitting outbound data and callbacks; confusing vendor hosting with transferred accountability; treating a shared database as one system; ignoring manual recovery and support; assuming a context diagram is complete because it is tidy; and allowing an unresolved boundary to become an undocumented implementation choice.

### Compact example

For an appointment service, “schedule appointment” is in scope. A patient and clinic staff are actors; identity verification, payment, messaging, and a clinical record are neighboring systems. The appointment service owns slot policy and booking identity but does not own authentication or clinical data. “Sends reminder” is insufficient: the edge must state appointment identifier, permitted contact channel, consent state, timing, delivery acknowledgement, data minimization, failure handling, and owners. A message provider outage must not silently cancel the appointment.

### Connections

[SARCH-001](001-architecture-as-significant-design-decisions.md) identifies significant decisions; [SARCH-002](002-stakeholders-and-architectural-concerns.md) supplies stakeholder concerns. The successor [SARCH-004](../ROADMAP.md) turns context scenarios into quality-attribute drivers. [SDDM-003](../../09-software-engineering-software-design-and-domain-modeling/modules/003-domain-language-and-terminology.md) supports domain meaning, while [SYSENG-009](../../26-systems-engineering/modules/009-system-context-and-operational-scenarios.md) treats wider system and operational context.

## Governing Question

A team is asked to build “the customer platform.” Does that include identity, billing, fulfillment, reporting, support, fraud decisions, consent, data deletion, and disaster recovery? Are existing services dependencies, components, or temporary migration sources? Who owns correctness when two organizations share a workflow?

Architecture cannot answer these questions by naming technologies. It must establish a functional boundary and context precise enough to assign responsibility, discover interfaces, analyze failure and trust, and test whether end-to-end scenarios have an owner.

## Why This Matters

Boundary mistakes become architecture mistakes. Scope that is too broad creates accidental platforms, duplicated authority, and delivery paralysis. Scope that is too narrow exports essential invariants into “the environment,” producing gaps between teams. A system can meet all local tests while an end-to-end outcome fails because no owner covers the crossing.

Context also determines risk. An external identity service changes authentication availability; a payment processor introduces uncertain outcomes; a human approval creates delay and accessibility concerns; a data export creates retention obligations. These effects exist even when the neighboring system is contractually managed.

A durable context description lets product, engineering, operations, security, data, legal, and suppliers challenge the same boundary. It must remain useful when implementations change, so it emphasizes capabilities, semantics, authority, and evidence before protocols and products.

## Prerequisites and Retrieval

Retrieve system, environment, actor, interface, dependency, capability, responsibility, authority, invariant, scenario, constraint, assumption, risk, trust boundary, failure domain, service objective, and lifecycle. Distinguish a system from its architecture description and a concern from a proposed solution.

From prior modules, retrieve architectural significance, stakeholder discovery, concern records, views and viewpoints, traceability, and intended versus operational architecture. You should be able to explain why “use provider X” is not functional scope and why “verify a claimant before releasing account data” is a responsibility even when an external provider supplies identity evidence.

## Learning Objectives

After completing this module, you should be able to:

1. name a system of interest and decision-relevant abstraction level;
2. define functional scope through capabilities, responsibilities, exclusions, and unresolved ownership;
3. discover external actors, neighboring systems, authorities, and environmental influences;
4. specify typed directional boundary interactions and their semantics;
5. distinguish system, organization, repository, deployment, trust, data-authority, and failure boundaries;
6. trace end-to-end scenarios across capabilities and interfaces;
7. identify gaps, overlaps, shared responsibilities, and circular dependencies;
8. construct and review a context view without implying unearned completeness;
9. manage boundary evolution, migration, retirement, and supplier change;
10. connect functional context to quality attributes, security, data, operations, and verification.

## Core Exposition

**Fix the question and level.** State the entity of interest, purpose, lifecycle stage, and decision. “Payments” may denote a business domain, capability, product, service, team, or deployed process. Choose one and define its externally observable responsibilities. If several levels matter, create related contexts instead of mixing enterprise, system, container, and component nodes.

**Describe outcomes before features.** Begin with stakeholder outcomes and operational scenarios. Decompose only enough to assign responsibility: accept an order, determine price, reserve stock, authorize payment, notify a customer, reconcile settlement, recover accepted work. Avoid turning the scope into a screen list or internal class model.

Classify each capability as in scope, external, shared under an explicit protocol, or unresolved. Record rationale, owner, acceptance condition, data authority, and change trigger. “Shared” is not a substitute for ownership: divide decisions and failure response explicitly.

**Treat the boundary as a responsibility claim.** Code may run in a vendor cloud while your organization owns user outcomes. A database may share a process while another team owns its schema. A library is compiled inside the system but governed externally. Repository and deployment boundaries are evidence, not definitions.

Use multiple boundary lenses: functional responsibility, change authority, runtime/process, deployment, data authority, trust, failure containment, legal jurisdiction, funding, and operations. Misalignment is not automatically wrong, but it creates interfaces and coordination costs that must be visible.

**Discover context systematically.** Walk lifecycle and scenarios: acquisition, enrollment, ordinary use, peak load, denied action, correction, cancellation, support, administration, monitoring, deployment, incident, failover, restore, audit, data access/deletion, migration, and retirement. For every step ask who or what sends, receives, authorizes, observes, stores, pays, changes, supports, or is affected.

Include actors without a user interface: schedulers, event producers, administrators, support staff, auditors, incident commanders, backup operators, downstream analysts, regulators, and data subjects. Include environmental conditions when they influence behavior even without a software interface.

**Type every crossing.** An arrow needs source, destination, direction, trigger, semantic payload or control, frequency/volume, timing, ordering, identity, authorization, confidentiality, integrity, availability, retries, duplicate/unknown outcome policy, versioning, and owner as applicable. Put detail in an interface inventory rather than crowding the diagram.

Separate business context from technical context. Business context says “submits claim” and what a claim means. Technical context may say HTTPS, event schema, batch file, manual queue, or physical device. A protocol can change while the responsibility remains; semantic change requires architectural review.

**Trace scenarios end to end.** For each material scenario, walk from stimulus through boundary crossings to observable response. Assign the invariant at the component that can enforce it. If no owner can prevent duplicate payment across a timeout and retry, the functional context has found a gap before detailed design.

Record exceptional paths: dependency rejects, times out, returns stale/conflicting data, sends duplicates, changes version, is compromised, or disappears. Define degradation and reconciliation responsibility. “External” never means “cannot affect architecture.”

**Represent the context honestly.** A context view normally centers one system and shows directly relevant people and external systems. Give it a title, scope, legend, date/version, descriptions, and directional labeled relationships. Do not expose internal containers unless the concern requires a different view.

The context view is an index into evidence, not the evidence itself. Link nodes and edges to capability, interface, data, ownership, SLO, contract, threat, runbook, and decision records. State omissions and unresolved items. Visual simplicity must not erase material complexity.

**Test boundary quality.** Ask whether every in-scope capability has one accountable owner; every external dependency has an owner and failure policy; every authoritative datum has one declared source at a time; every flow has semantics and direction; and every stakeholder scenario terminates in observable evidence. Check overlaps and gaps with neighboring teams.

Run adversarial reviews from operations, security, privacy, data, accessibility, support, and supplier perspectives. Compare described context with runtime traffic, identity grants, schemas, deployment inventory, incidents, invoices, and support procedures. Differences reveal drift or missing context, not automatically which artifact is correct.

**Evolve the boundary deliberately.** Record current, target, and transition contexts for migration. Dual running creates temporary authorities, synchronization, routing, rollback, and retirement obligations. A target diagram alone hides the risky state.

Reopen context after new capabilities, acquisitions, supplier changes, incidents, regulation, geography, data use, ownership transfer, or decommissioning. Remove retired edges only after traffic, data, access, contracts, and recovery dependencies are gone.

## Definitions and Notation

Let the system of interest be the distinguished node $s$ in a typed directed multigraph

$$
G=(V,E), \qquad s\in V.
$$

$V$ contains people, organizations, neighboring systems, devices, and relevant environmental entities. Multiple edges may connect the same nodes because a dependency can carry different meanings in opposite directions. Define an edge as

$$
e=(u,v,kind,semantics,trigger,owner,evidence),
$$

where $u$ is the source, $v$ the destination, and the remaining fields make the relationship reviewable. An unlabeled line is not an adequate edge: it does not say whether data, money, authority, control, notification, or physical material crosses the boundary.

Let $C$ be the declared capability inventory. A scope assignment is a total function over the known inventory,

$$
scope:C\rightarrow\{in,external,shared,unresolved\}.
$$

“Total” means every known capability receives a disposition; it does not mean discovery is complete. A shared capability also requires a responsibility partition $part(c)$ that identifies which party decides, performs, verifies, recovers, and accepts residual risk. If $part(c)$ is absent, `shared` is merely a warning label.

For a material scenario $q$, let $trace(q)=\langle e_1,\ldots,e_n\rangle$ be the ordered boundary crossings from stimulus to observable outcome. A trace is *closed* when every crossing has compatible endpoint semantics, an accountable owner, and a defined normal or exceptional continuation. Closed traces support review; they do not prove the implemented system behaves correctly.

For the dated known inventory, define declared scope coverage as

$$
Cov_C=\frac{|\{c\in C:scope(c)\neq unresolved\}|}{|C|}
$$

when $|C|>0$. If $C$ is empty, report “no inventory.” $Cov_C=1$ means only that every discovered capability has a disposition. It does not prove that all capabilities, actors, dependencies, or obligations were discovered.

## Mechanisms, Invariants, or Proof Structure

Use this repeatable mechanism to establish and maintain context.

1. **Frame the entity:** name the system of interest, purpose, lifecycle stage, abstraction level, decision, and time horizon.
2. **Collect outcomes:** elicit externally observable responsibilities, exclusions, constraints, and success or failure conditions.
3. **Walk scenarios:** traverse ordinary, denied, degraded, recovery, administrative, migration, audit, and retirement paths.
4. **Discover neighbors:** identify people, systems, authorities, suppliers, physical conditions, and affected parties at each step.
5. **Assign capabilities:** mark each known capability in, external, shared, or unresolved, with rationale and authority.
6. **Type crossings:** record direction, semantics, trigger, identity, data authority, timing, failure policy, version, and owner.
7. **Trace end to end:** connect stimulus to observable result, including timeout, duplicate, rejection, stale-data, and reconciliation paths.
8. **Compare lenses:** inspect functional, organizational, deployment, trust, data-authority, jurisdictional, and failure boundaries for consequential misalignment.
9. **Challenge with evidence:** compare the description with traffic, schemas, identities, contracts, incidents, runbooks, inventories, and stakeholder observation.
10. **Version and reopen:** preserve current, target, and transition contexts and define events that invalidate prior assumptions.

The following invariants govern a reviewable context description:

- **Identity invariant:** exactly one entity of interest and abstraction level are explicit per context view.
- **Responsibility invariant:** every known in-scope capability has an accountable authority; shared responsibility is partitioned.
- **Crossing invariant:** every material boundary crossing has direction, semantics, endpoints, and ownership.
- **Authority invariant:** authoritative data and decisions have an identified source for each operational state, including migration.
- **Scenario invariant:** every material scenario reaches an observable outcome or a named unresolved gap.
- **Failure invariant:** every critical external dependency has timeout, rejection, duplicate, unknown-outcome, degradation, and recovery responsibilities as applicable.
- **Traceability invariant:** capabilities, crossings, constraints, decisions, and evidence use stable references.
- **Honesty invariant:** omissions, assumptions, unresolved ownership, evidence limits, and effective dates are visible.

These are architecture-description invariants, not runtime guarantees. They can establish that the recorded model satisfies declared predicates. They cannot establish that the model is complete, that contracts are honored, or that production behavior matches it. Those claims require stakeholder validation, implementation evidence, and operational observation.

A useful adversarial check is edge reversal: for every edge $u\rightarrow v$, ask whether a response, acknowledgement, callback, error, revocation, reconciliation, or operational control returns from $v$ to $u$. Another is boundary displacement: move one capability across the boundary and enumerate the new contracts, authority transfers, failure modes, security exposures, and coordination costs. If the analysis does not change, the original edge or capability semantics were probably underspecified.

## Alternatives and Trade-Offs

**Capability-centered scope** remains stable across implementation change and clarifies responsibility, but can hide concrete integrations if used alone. **Interface-centered scope** exposes protocols and traffic, but can mistake the present integration topology for enduring purpose. Maintain both, with traceable links.

**One concise context view** communicates the big picture quickly. A single view becomes misleading when it mixes business actors, technical services, organizational ownership, trust zones, and deployment nodes without a legend. Prefer one primary system context plus concern-specific overlays or related views when semantics differ.

**Organization-aligned boundaries** reduce coordination within teams and make accountability legible. They can fragment end-to-end capabilities or preserve an obsolete structure. **Domain-aligned boundaries** can improve semantic cohesion but still require operational ownership, funding, and migration authority. Neither organizational charts nor domain models decide scope automatically.

**Build inside the boundary** increases direct control and may simplify outcome ownership, while increasing implementation, staffing, and lifecycle burden. **Buy or delegate externally** may accelerate delivery and transfer some work, while introducing contracts, supply risk, data movement, exit cost, and uncertain failure behavior. Delegation moves mechanisms; it rarely eliminates responsibility for the integrated outcome.

**Synchronous interactions** provide an immediate result and simpler local reasoning, but couple latency and availability. **Asynchronous interactions** decouple time and absorb bursts, but require identity, ordering, deduplication, expiry, observation, and reconciliation semantics. Context must expose these responsibilities without prematurely selecting a broker or protocol.

**Shared data stores** reduce initial integration work but blur schema authority, access, change control, and failure containment. **Owned stores with explicit exchange** strengthen boundaries and independent change at the cost of replication, staleness, reconciliation, and more interfaces. The decisive question is which consistency and authority obligations the capability needs.

## Failure Modes and Misconceptions

- **“The box is the application.”** A repository, process, cluster, product name, or team boundary may not match the responsibility boundary.
- **“External means out of scope.”** External mechanisms remain part of the system context and can determine the delivered outcome.
- **“A user is anyone with a screen.”** Batch producers, support staff, schedulers, auditors, devices, affected non-users, and regulators can be actors.
- **“The diagram is self-explanatory.”** Shape and line semantics vary; title, scope, legend, descriptions, directions, and labels are required.
- **“Bidirectional” is a sufficient label.** Requests, acknowledgements, callbacks, revocations, errors, and reconciliations usually have different meanings and guarantees.
- **“Shared means both teams own it.”** Without decision, operation, verification, recovery, and risk partitions, shared ownership often means no accountable owner.
- **“The authoritative database is obvious.”** Authority can differ by field, event, jurisdiction, lifecycle state, or migration interval.
- **“The API defines the contract.”** Transport syntax does not fully define business meaning, timing, authorization, failure, version, or reconciliation.
- **“Current traffic proves scope.”** Dormant emergency paths, manual recovery, legal duties, planned migration, and missing integrations may not appear in traffic.
- **“No arrow means no dependency.”** Funding, certificates, DNS, time, identity, human approval, legal authority, and physical infrastructure can be decisive dependencies.
- **“Target context is enough.”** Migration introduces temporary routing, duplicate authority, synchronization, rollback, and retirement responsibilities.
- **“100% inventory coverage proves completeness.”** It proves a declared predicate over a dated known inventory only.
- **“A supplier SLA is our user guarantee.”** Definitions, exclusions, dependency composition, detection, recovery, and end-to-end evidence differ.
- **“Removing traffic retires an interface.”** Data, credentials, contracts, callbacks, backups, audit evidence, and recovery procedures may survive.

## Worked Examples

### Example 1

**Question:** What belongs inside the boundary of a clinic appointment service?

**Reasoning:** Frame the system as the service responsible for presenting eligible slots, accepting a booking request, preventing conflicting confirmed appointments, and returning a durable result. Patients and staff are actors. The clinical scheduling system is the authority for practitioner calendars; identity and notification services are neighbors. “Render the web page” is an implementation activity, while “confirm one eligible slot or explain rejection” is an observable responsibility. Trace search, selection, hold, confirmation, cancellation, and reminder paths. A reminder failure may degrade notification without invalidating a confirmed booking; a calendar timeout must not invent availability.

**Conclusion:** Functional scope follows appointment outcomes and invariants, not the web process or team repository.

### Example 2

**Question:** Is payment complete when a processor request times out?

**Reasoning:** A timeout says the caller lacks a response; it does not say authorization failed. The context needs separate edges for authorization request, processor decision, later status inquiry or callback, and settlement/reconciliation evidence. Assign the service responsibility to avoid a second charge while the outcome is unknown, persist an idempotency identity, and reconcile before promising failure or retrying. The processor owns its authorization decision, but the system of interest owns how that uncertainty affects the customer order.

**Conclusion:** Typed exceptional crossings reveal an unknown-outcome responsibility hidden by a single “payments” arrow.

### Example 3

**Question:** Two services write a shared customer table. Has the customer-profile capability been assigned?

**Reasoning:** Physical access does not establish semantic authority. Enumerate name, contact preferences, legal identity, delivery address, and deletion state; each may have a different legitimate authority. If either service can alter every field without coordination, schema and decision ownership overlap. Partition the capability, establish one authority per field and lifecycle state, define change propagation and reconciliation, or mark ownership unresolved. A box labeled “shared database” describes deployment, not responsibility.

**Conclusion:** Shared storage requires explicit data and decision authority; otherwise the scope contains an ownership defect.

### Example 4

**Question:** Should human support appear in the context when it uses no dedicated API?

**Reasoning:** During an account-lock incident, support authenticates the caller through a controlled procedure, inspects evidence, requests an unlock, and communicates the result. Those actions affect security, latency, auditability, accessibility, and recovery. Model the support role, the authorized control crossing, its evidence, and the escalation authority. Hiding the role because it acts through an existing console erases a material system interaction.

**Conclusion:** Humans with operational or decision effects are context actors even when their mechanism is indirect.

### Example 5

**Question:** A report service publishes an event and receives no immediate response. Is its responsibility finished?

**Reasoning:** Trace event creation, stable identity, publication acceptance, consumer processing, rejection, expiry, duplicate delivery, and eventual observation. If the business outcome is “regulator receives the report by midnight,” broker acceptance is intermediate evidence only. Assign monitoring and reconciliation, specify what happens to poison messages, and decide which system can declare the report delivered. A one-way arrow without outcome evidence would truncate the scenario.

**Conclusion:** Asynchrony changes timing and failure semantics; it does not remove end-to-end outcome ownership.

### Example 6

**Question:** A team buys a hosted identity service. Is authentication now outside its system boundary?

**Reasoning:** The provider operates credential verification, but the relying service chooses when authentication is required, which claims it accepts, how sessions expire, how provider unavailability degrades behavior, and how account recovery or revocation works. Record the provider as a neighbor and partition responsibility. Hosting location and contractual operation are not equivalent to responsibility for releasing protected data.

**Conclusion:** Delegating identity mechanisms creates an external dependency while leaving integration and authorization responsibilities inside.

### Example 7

**Question:** How should context represent migration from a legacy order service to a replacement?

**Reasoning:** The current context has the legacy service as order authority. The target context assigns authority to the replacement. The transition context must state how routing chooses a writer, how historical orders move, whether reads merge sources, how duplicates and divergent updates reconcile, how rollback works, and when legacy credentials, queues, data, and support procedures retire. Declaring both systems authoritative during dual running violates the authority invariant unless authority is partitioned by an explicit rule.

**Conclusion:** Current, target, and transition contexts expose risks that a target-only diagram conceals.

### Example 8

**Question:** An analytics export crosses from a product service to a warehouse. What security scope is required?

**Reasoning:** Identify subjects, fields, purpose, lawful or policy authority, minimization, transfer identity, confidentiality, integrity, retention, deletion propagation, access review, and incident ownership. The product boundary, data-authority boundary, trust boundary, and organizational boundary may not coincide. An encrypted transport protects one crossing but does not establish destination authorization or permitted use.

**Conclusion:** A context edge must expose authority and lifecycle semantics, not merely “TLS to warehouse.”

### Example 9

**Question:** A service has no runtime traffic to the disaster-recovery account. Can that account be omitted?

**Reasoning:** Recovery depends on credentials, replicated artifacts or data, DNS or routing control, capacity, runbooks, and authorized operators. These dependencies may be dormant during normal operation yet determine restoration. Include the recovery environment or control systems in the concern-specific context, state activation conditions, and link to tested recovery evidence. Absence from ordinary telemetry is not absence from architecture.

**Conclusion:** Scenario discovery finds dormant but critical context that traffic discovery misses.

### Example 10

**Question:** Define the context of an emergency-dispatch recommendation service without claiming it owns dispatch.

**Reasoning:** Frame the entity as producing ranked resource recommendations from authorized incident, location, capability, and availability inputs. Call takers and dispatchers remain decision actors; dispatch control, radio, mapping, identity, incident records, vehicle telemetry, and audit authorities are neighbors. State that a qualified dispatcher authorizes deployment, define stale or missing-data behavior, make overrides observable, and preserve degraded manual operation. The context must identify safety, jurisdiction, latency, cybersecurity, and human-factors concerns. No external emergency-services, safety, regulatory, or practitioner review is claimed; named qualified authorities must validate the boundary, hazards, decision allocation, evidence, and residual risk before operational use.

**Conclusion:** Precise scope can support a high-consequence human decision without silently transferring authority to software.

## Cross-Program Connections

- [Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) provides domain boundaries, capabilities, aggregates, and observable behavior used to test functional cohesion.
- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) examines recurring collaboration structures once forces and boundaries are explicit.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) turns context scenarios and crossings into verification scopes and contract tests.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) develops data authority, lineage, lifecycle, and governance across system boundaries.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) analyzes assets, identities, trust boundaries, threats, and authorization at crossings.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) situates the software system within wider operational, human, physical, and lifecycle contexts.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) specifies durable interface semantics, evolution, idempotency, and failure behavior for context edges.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 42010:2022, Software, systems and enterprise—Architecture description](https://www.iso.org/standard/74393.html), edition 2, November 2022. Current architecture-description standard for entities of interest, environments, stakeholders, concerns, viewpoints, views, model kinds, and correspondence; consulted 2026-09-05.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018, Systems and software engineering—Life cycle processes—Requirements engineering](https://www.iso.org/standard/72089.html), second edition, November 2018. Requirements and interface information across system lifecycle processes; consulted 2026-09-05.
3. Simon Brown. [C4 model: System context diagram](https://c4model.com/diagrams/system-context), official C4 documentation. Guidance on centering the system, showing directly connected people and systems, and avoiding low-level detail; consulted 2026-09-05.
4. Simon Brown. [C4 model: Notation](https://c4model.com/diagrams/notation), official C4 documentation. Titles, scope, legends, element descriptions, and directional labeled relationships; consulted 2026-09-05.
5. arc42. [Section 3: Context and Scope](https://docs.arc42.org/section-3/), official arc42 documentation. Business and technical context, external interfaces, and boundary communication partners; consulted 2026-09-05.
6. INCOSE Systems Engineering Body of Knowledge. [Introduction to System Fundamentals](https://sebokwiki.org/wiki/Introduction_to_System_Fundamentals), SEBoK. System boundary, environment, and context as external elements and interactions; consulted 2026-09-05.
7. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. System context, business goals, quality-attribute scenarios, architecture drivers, and evaluation.
8. Paul Clements et al. *Documenting Software Architectures: Views and Beyond*, second edition, Addison-Wesley, 2010. Context diagrams, views, interfaces, variability, and documentation obligations.
9. Nick Rozanski and Eoin Woods. *Software Systems Architecture: Working With Stakeholders Using Viewpoints and Perspectives*, second edition, Addison-Wesley, 2011. System context, functional view, information, deployment, operational concerns, and cross-cutting perspectives.
10. Eric Evans. *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003. Bounded contexts, context maps, responsibility, and explicit relationships among models.

## Exercises

### Exercise 1

For a library lending service, distinguish the system of interest, four capabilities, three actors or neighboring systems, and three boundary lenses. Explain why a deployment boundary alone is insufficient.

### Exercise 2

Trace an online order from submission through inventory reservation and payment authorization when the payment response times out. Identify every material crossing, authority, observable outcome, and unresolved responsibility.

### Exercise 3

Diagnose this context description: one box named “Platform,” arrows labeled “uses,” a shared customer database, no humans except “user,” and a target-state replacement service shown beside the legacy service. State the corrections needed before architectural decisions depend on it.

### Exercise 4

Compare keeping notification delivery inside an account service with delegating it to an external provider. Define the stable functional responsibility, partition ownership, and analyze latency, availability, security, observability, change, and exit trade-offs.

### Exercise 5

Construct a review approach for the context of an unfamiliar municipal flood-warning service. Separate automated model checks from qualified human validation, decision authority, operational evidence, and stop conditions.

## Answers to the Exercises

### Answer 1

Name the entity “library lending service,” responsible for determining loan eligibility, recording checkout/return, exposing current loan state, and initiating overdue notice requests. Actors and neighbors can include patron, librarian, catalogue/item authority, identity service, and notification service. Functional responsibility asks who decides and records a loan; data authority asks which source owns item, patron, and loan facts; trust/organizational/deployment lenses ask where identities, control, teams, and processes differ.

A deployment boundary only says where processes or resources run. It cannot establish whether the service or catalogue owns item availability, whether the library or an identity provider authorizes a patron, or who repairs a missed return event. A complete answer may choose different actors, but it must name one abstraction level, express externally observable responsibilities, and make at least three non-equivalent boundary lenses explicit.

### Answer 2

The customer sends an order command to the order service, which validates identity and records a stable order identity. The order service requests a reservation from the inventory authority and receives reserved, rejected, or unknown status. It sends an authorization with an idempotency identity to the payment processor. A timeout produces an unknown observation, not a decline. The service must query status or accept a signed callback, correlate the result, prevent duplicate authorization, release inventory on a terminal failure according to policy, and reconcile if messages arrive late.

Inventory owns reservation truth; the processor owns authorization truth; the order service owns the customer-visible order state and coordination policy. The observable outcome may be confirmed, rejected with a reason, or explicitly pending with a bounded follow-up. If no party owns reconciliation between a late authorization and a released reservation, record an unresolved responsibility and do not claim the trace is closed.

### Answer 3

Replace “Platform” with a named entity, purpose, lifecycle state, and abstraction level. Define capabilities and exclusions before implementation nodes. Replace every “uses” edge with direction, trigger, semantic payload or control, owner, timing, and failure behavior. Partition customer-data authority by fact and lifecycle state; shared physical access is not shared accountability. Add administrators, support, operators, auditors, affected data subjects, and other actors discovered from scenarios.

Create separate current, target, and transition contexts. During replacement, declare routing, writer/read authority, synchronization, rollback, reconciliation, credentials, and retirement conditions. Add title, scope, legend, descriptions, effective date, unresolved items, and evidence links. Review the result against scenarios and operational evidence. These repairs make the model reviewable but still do not prove discovery completeness or production correspondence.

### Answer 4

The stable responsibility is to request an authorized notification for a declared purpose and make its delivery state visible enough for the account outcome. Keeping delivery inside provides direct implementation and telemetry control, but adds channel expertise, supplier relations, abuse controls, compliance, scaling, and on-call burden. Delegation can provide reach and operational specialization, but creates provider availability, rate, data-transfer, credential, contract, observability, semantic-version, and exit dependencies.

With delegation, the account service owns recipient/purpose authorization, request identity, template or semantic correctness, response to unavailable/unknown delivery, user-visible status, and reconciliation. The provider owns channel submission under its contract; neither an acceptance response nor an SLA alone proves user receipt. Evaluate end-to-end latency and availability, minimization and retention, region and subprocessor constraints, callback authenticity, duplicate suppression, monitoring, portability, and fallback. An acceptable alternative partition is possible, but the answer must assign each decision and failure response explicitly.

### Answer 5

Frame the service: geographic and jurisdictional scope, warning recommendation versus legal warning authority, sensors and forecasts, affected residents, accessibility and language needs, emergency operations, telecom channels, maintenance, and retirement. Model normal, sensor-loss, conflicting-forecast, network-partition, false-positive, missed-event, manual-override, evacuation, recovery, and post-incident scenarios. Identify weather and hydrology authorities, municipal emergency command, operators, residents and legitimate representatives, accessibility experts, infrastructure owners, security/privacy authorities, and independent assurance.

Automated checks may enforce unique identities, typed edges, one declared authority per datum/state, trace closure under a specified predicate, unresolved-item visibility, version/digest integrity, and evidence freshness. Simulation and exercises can provide bounded operational evidence for stated conditions. They cannot validate hazard completeness, hydrological assumptions, public communication, lawful authority, human behavior, or acceptable residual risk. No external municipal, hydrology, emergency-services, safety, accessibility, regulatory, or practitioner review is claimed. Named qualified authorities must validate those matters and own issuance, override, deployment, and risk-acceptance decisions. Missing critical sensor provenance, unclear warning authority, an untested degraded path, or unresolved high-severity hazard blocks the corresponding readiness claim.
