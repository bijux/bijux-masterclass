---
module_id: SARCH-008
program: Software Engineering: Software Architecture
level: 1
module_number: 8
title: Architecture Versus Detailed Design
status: complete
last_verified: 2026-09-05
---

# Architecture Versus Detailed Design

## One-Page Review

### Governing question

Which design decisions need system-wide architectural treatment, and which should remain local so teams can implement and evolve without unnecessary central control?

### Essential definitions

- **architecture** comprises the fundamental concepts or properties of a system in its environment, embodied in elements, relationships, and principles of design and evolution.
- **detailed design** specifies local structures, algorithms, data representations, interfaces, and implementation choices within architectural responsibilities.
- An **architectural decision** has consequences broad, durable, risky, or difficult to reverse enough to require cross-boundary reasoning.
- A **local decision** can be made and changed within one owned boundary while preserving its external contracts and system invariants.
- **abstraction** deliberately suppresses details irrelevant to a concern; it does not mean vagueness.
- **encapsulation** hides changeable decisions behind stable responsibilities or interfaces.
- A **design constraint** restricts local choices; an **architecture principle** guides recurring decisions under declared scope and rationale.
- **decision reach** is the set of stakeholders, structures, interfaces, qualities, teams, and lifecycle states materially affected by a decision.

### Central model, mechanism, or theorem

Classify decisions by consequence rather than artifact type. For a decision $d$, examine its reach, reversibility, coupling, quality effects, uncertainty, authority, and lifecycle cost. Treat $d$ architecturally when local optimization could violate end-to-end requirements or when coordination and evidence must cross ownership boundaries. Delegate it when an owner can change it while maintaining published contracts, invariants, and budgets.

Architecture establishes constraints and freedoms. Detailed design realizes those constraints and may reveal evidence that architecture must reopen.

### Critical invariants

- classification depends on system context and consequence, not diagram level or job title;
- architectural descriptions include only detail needed for named concerns and decisions;
- local decisions preserve allocated requirements, contracts, invariants, and evidence obligations;
- every centralized decision has explicit reach, rationale, authority, and review trigger;
- every delegated boundary states the freedom granted and the obligations retained;
- implementation evidence can invalidate architectural assumptions;
- code, deployment, data, organization, and runtime structures may require different views;
- recurring local coordination pain can reveal a missing architectural decision;
- architecture does not become complete before detailed design begins;
- change propagates through traceable decisions rather than document hierarchy alone.

### Common failures

Common failures include calling all early decisions architecture; calling all code choices detail; equating architecture with boxes and arrows; prescribing class names in a system view; leaving security or recovery to “implementation”; centralizing reversible preferences; treating databases, frameworks, or clouds as inherently architectural; assuming microservices eliminate detailed design; allowing local optimizations to violate end-to-end budgets; freezing architecture before feedback; and using “not architectural” to avoid documenting a risky decision.

### Compact example

Choosing that each order has exactly one authoritative writer and that retries use stable operation identities is architectural when several services and teams coordinate payment and fulfillment. Choosing the internal map type used to cache order lookups is detailed design if it preserves latency, memory, concurrency, and correctness obligations. If the map choice changes distributed consistency or exhausts shared memory at peak load, its reach has expanded and the decision must be escalated.

### Connections

[SARCH-003](003-functional-scope-and-system-context.md) sets system boundaries; [SARCH-004](004-quality-attributes-as-architectural-drivers.md) identifies cross-cutting qualities; [SARCH-006](006-architecturally-significant-requirements.md) identifies formative obligations; and [SARCH-007](007-trade-offs-and-competing-objectives.md) evaluates broad choices. [SARCH-009](../ROADMAP.md) records architectural decisions durably.

## Governing Question

Architecture and design are not separate substances. Both involve choosing structures and behavior under constraints. The useful distinction is scope and consequence: which decisions demand system-level coordination and durable evidence, and which should be delegated to the smallest capable owner?

If everything is architecture, review becomes a bottleneck and implementation loses autonomy. If architecture is only a high-level diagram, essential decisions about data authority, failure, security, deployment, change, and operation occur accidentally. The boundary must therefore be explicit, contextual, and revisable.

## Why This Matters

Misclassification creates two opposite risks. Over-architecting fixes local details before evidence exists, increases coordination cost, and makes harmless changes slow. Under-architecting lets teams independently choose mechanisms whose interaction violates end-to-end qualities, duplicates authority, or makes later correction expensive.

The distinction also shapes documentation. Architecture views should expose the structures and decisions needed by stakeholders, not every implementation element. Detailed designs can change frequently behind stable architectural contracts. This separation keeps descriptions usable while preserving accountability for consequential decisions.

Finally, implementation is a source of learning. Algorithms, data distributions, toolchain behavior, incidents, and delivery constraints can reveal that an architectural assumption was wrong. A healthy process allows evidence to flow upward and decisions to be reclassified.

## Prerequisites and Retrieval

Retrieve system of interest, environment, stakeholder, concern, view, viewpoint, architecture decision, ASR, constraint, assumption, risk, trade-off, element, relationship, responsibility, interface, invariant, abstraction, encapsulation, coupling, cohesion, allocation, verification, and validation.

From prior modules, retrieve decision significance, context boundaries, quality scenarios, explicit assumptions, requirement allocation, and sensitivity. Be able to distinguish a conceptual responsibility from its runtime process, deployment unit, source repository, and organizational owner.

## Learning Objectives

After completing this module, you should be able to:

1. explain architecture and detailed design as a continuum of consequential decisions;
2. classify a decision by reach, reversibility, quality effect, uncertainty, and authority;
3. choose the appropriate abstraction and view for a concern;
4. separate architectural obligations from implementation freedom;
5. define delegation boundaries with contracts, invariants, and budgets;
6. recognize under- and over-architecting;
7. trace architectural decisions into detailed designs and evidence;
8. use implementation feedback to reopen architecture;
9. distinguish system, module, runtime, deployment, data, and organizational structures;
10. govern cross-boundary change without centralizing every local choice.

## Core Exposition

**Architecture is design with system-level significance.** The ISO/IEC/IEEE 42010:2022 vocabulary distinguishes the architecture of an entity from the architecture description that expresses it. Architecture is not the diagram or document. It concerns fundamental properties embodied in elements, relationships, and evolution principles. Detailed design is not unimportant; it realizes and tests those properties.

Use consequence rather than size. A one-line configuration deciding whether authorization fails open may be architectural. A large internal parsing subsystem may remain local if it is replaceable behind a stable contract and cannot materially affect external qualities. File size, layer, programming language, and meeting attendance do not classify a decision.

**Assess decision reach.** Identify affected stakeholder outcomes, capabilities, data authorities, interfaces, runtime interactions, deployment and failure domains, security boundaries, teams, suppliers, costs, and lifecycle states. Broad reach increases the need for architectural treatment. Hidden reach is common: a local serialization choice becomes an external compatibility contract once persisted or transmitted.

Assess reversibility and option loss. A choice may be locally implemented yet hard to reverse because data accumulates, clients depend on it, staff specialize, or contracts lock it in. Conversely, an apparently broad decision can remain reversible when adapters, automated migration, and stable semantics preserve options.

**Match abstraction to concern.** Abstraction suppresses irrelevant detail while preserving semantics needed for analysis. A context view shows people and neighboring systems; internal classes would obscure the boundary. A deployment view needs processes, nodes, zones, and communication paths; business capability labels alone are insufficient. A module view needs implementation responsibility and dependency semantics.

“High level” is not a synonym for architecture. A vague cloud drawing can omit every significant decision, while a precise state transition may be architectural because payment correctness depends on it. Select model kinds and detail according to stakeholder concerns and analytical purpose.

**Architecture constrains and enables.** An architectural boundary should specify what local owners must preserve and what they may choose. Obligations may include interface semantics, data authority, dependency direction, latency or resource budgets, security policy, failure behavior, observability, compatibility, and evidence. Freedoms may include algorithms, internal decomposition, libraries, data structures, refactoring, and release timing within those bounds.

This contract prevents architecture from becoming central approval of every implementation decision. Delegation is real only when owners can exercise meaningful choices and receive feedback. A rule with no rationale or exception path becomes cargo-cult governance.

**Several structures coexist.** Source modules, runtime components, deployment units, database ownership, teams, and business capabilities are not one hierarchy. One module can support several processes; one process can deploy in many nodes; one team can own several modules; one capability can cross systems. Architectural descriptions need multiple related views and correspondence rules.

Do not infer architectural boundaries directly from repositories or organization charts. These are evidence about realized design, but they may expose drift, accidental coupling, or a mismatch that the architecture should address.

**Distinguish mechanism from policy.** Architecture often establishes policy and responsibility while detailed design chooses a mechanism. “Only the account authority may change the legal owner, and every change must be auditable” is architectural. Transaction syntax, indexing, or an internal command class may be local. Sometimes mechanism is also architectural—for example, a mandated interoperable protocol or a consensus scheme central to safety and availability.

**Allocate without losing outcomes.** End-to-end ASRs are decomposed into budgets and responsibilities. Local teams may implement within budgets, but an outcome owner must preserve composition. Four components each meeting a local latency target do not prove the user path meets its percentile; local uptime does not compose automatically into workflow availability.

Use guardrails that can be checked: dependency rules, contract tests, schemas, policy checks, resource limits, architecture fitness functions, and review triggers. Automated checks support conformance to selected rules, not architecture fitness or stakeholder validation.

**Let detailed design challenge architecture.** During implementation, a team may discover a protocol cannot express required semantics, a library has unsafe failure behavior, a data partition creates unacceptable contention, or a local change touches many modules. Record evidence and reopen the relevant decision, requirement, or assumption. Do not force implementation to conform to an invalid premise merely because the document was approved.

Detailed design also creates new commitments. A schema becomes architectural when independent consumers rely on it. An internal retry becomes architectural when it duplicates externally visible work. Escalate before reach expands silently.

**Use proportional governance.** Establish thresholds for review: new cross-team contracts, authoritative data, trust-boundary change, persistent format, failure-domain change, new supplier, material ASR impact, irreversible migration, or high residual risk. Keep local changes local when automated evidence confirms obligations remain satisfied.

Architecture owners should steward cross-boundary coherence, not own all design. Component owners remain accountable for implementation correctness, evidence, and notifying when assumptions fail. Decision authority follows consequence and governance, not the “architect” title.

## Definitions and Notation

Let $D$ be the set of known design decisions. For $d\in D$, define decision reach

$$
Reach(d)=S_d\cup Q_d\cup I_d\cup T_d\cup L_d,
$$

where $S_d$ is affected stakeholders or systems, $Q_d$ affected quality scenarios, $I_d$ interfaces and invariants, $T_d$ teams or authorities, and $L_d$ lifecycle states. The union is a conceptual inventory, not a cardinal score.

Define a classification profile

$$
profile(d)=(reach,reversalCost,qualityEffect,uncertainty,authority,optionLoss).
$$

Classification $class(d,c,e)$ depends on context $c$ and evidence $e$. It may return architectural, local, or unresolved. This is a governed judgment; no universal numerical boundary separates architecture from design.

Let $Obl(b)$ be obligations and $Free(b)$ freedoms for owned boundary $b$. Sound delegation requires that freedoms not contradict obligations:

$$
Free(b)\cap Forbidden(Obl(b))=\varnothing.
$$

This expression states a consistency goal. Establishing the sets completely is generally impossible; contracts and checks provide bounded evidence.

Trace relations $realizes\subseteq D_{detail}\times D_{arch}$ and $challenges\subseteq E_v\times D_{arch}$ connect local designs and implementation evidence to architectural decisions. They make feedback explicit rather than one-way.

## Mechanisms, Invariants, or Proof Structure

Use this classification and delegation mechanism.

1. **Frame:** identify the system, concern, decision horizon, owners, and affected ASRs.
2. **Describe the decision:** state alternatives, mechanism or policy, assumptions, and current evidence.
3. **Map reach:** trace stakeholders, structures, interfaces, qualities, teams, suppliers, and lifecycle states.
4. **Assess commitment:** examine reversal cost, data/client accumulation, uncertainty, and option loss.
5. **Classify:** mark architectural, local, or unresolved with rationale and authority.
6. **Choose the view:** include only detail needed for the concern and analysis.
7. **Delegate:** state obligations, freedoms, budgets, evidence, exception process, and escalation triggers.
8. **Realize and verify:** connect detailed designs and checks to architectural decisions.
9. **Observe feedback:** detect drift, coordination pain, failed assumptions, and expanded reach.
10. **Reclassify and evolve:** reopen decisions and preserve history when evidence or context changes.

The governing invariants are consequence-based classification, concern-appropriate abstraction, explicit obligations and freedoms, end-to-end ownership, multiple-view semantics, traceable realization, bounded conformance evidence, reciprocal feedback, legitimate authority, and lifecycle revision.

Passing a dependency rule or contract test establishes only the encoded predicate. It cannot prove that every architectural decision was identified, the abstraction is sufficient, local design is correct, or stakeholder outcomes are served.

## Alternatives and Trade-Offs

**Central architecture approval** can coordinate cross-system qualities and risk but creates delay, context loss, and weak local ownership. **Fully decentralized design** improves speed and context but can create inconsistent contracts, duplicated authority, and systemic risk. Use federated authority with explicit escalation conditions and shared evidence.

**Prescriptive architecture** improves repeatability and can reduce known hazards, but freezes mechanisms and suppresses learning. **Principle- and outcome-based architecture** preserves freedom but requires mature measurement and judgment. Prescribe where consequence and interoperability demand it; otherwise specify outcomes and guardrails.

**Up-front models** expose risk before commitment but rely on uncertain premises. **Emergent design** incorporates implementation learning but can harden accidental choices. Establish minimum viable architecture for irreversible and cross-boundary decisions, then evolve with evidence.

**Stable interfaces** enable independent change but impose versioning, compatibility, and semantic discipline. **Shared internals** reduce short-term translation but widen change reach. Choose boundaries according to likely change, authority, and quality scenarios rather than a universal preference for services or modules.

## Failure Modes and Misconceptions

- **“Architecture is high-level design.”** Abstraction is concern-specific; precise low-level semantics can be architectural.
- **“Detailed design begins after architecture ends.”** They overlap and exchange evidence throughout the lifecycle.
- **“Anything hard to code is architectural.”** Difficulty and system-wide significance differ.
- **“Anything in code is implementation.”** Persistent formats, authorization defaults, and retry semantics can be architectural.
- **“A framework choice is always architectural.”** Its reach, lock-in, qualities, and authority determine significance.
- **“A diagram is the architecture.”** It is one architecture-description artifact with limited semantics.
- **“Architecture owns all interfaces.”** Local interfaces can remain within owned boundaries; cross-boundary semantics need broader governance.
- **“Delegation means no constraints.”** It grants choices within explicit obligations and evidence duties.
- **“Standards eliminate design.”** Standards constrain some choices and introduce interpretation, integration, and exception decisions.
- **“Automated conformance proves fitness.”** Checks cover encoded rules, not complete stakeholder concerns.
- **“Organizations define architecture.”** Team boundaries influence communication but do not determine system responsibility automatically.
- **“Approved architecture cannot change.”** Evidence and context must reopen invalid decisions.
- **“Local optimization is harmless.”** Shared resources and end-to-end paths can turn local choices into system effects.
- **“Not architectural means undocumented.”** Local decisions still need proportionate tests, rationale, and ownership.

## Worked Examples

### Example 1

**Question:** Is choosing an in-memory map an architectural decision?

**Reasoning:** If it is private, replaceable, bounded by allocated memory and concurrency requirements, and invisible outside one module, it is detailed design. If it becomes the authoritative state, determines failover, or exhausts shared memory under peak load, its reach includes availability and recovery and must be escalated.

**Conclusion:** The same mechanism changes classification when its consequences cross boundaries.

### Example 2

**Question:** Is a database choice automatically architectural?

**Reasoning:** A database can be local when one component owns it behind stable semantics and migration is routine. It is architectural when it establishes cross-team data authority, transaction boundaries, persistent external formats, recovery topology, licensing lock-in, or system-wide qualities. Analyze decisions, not product category.

**Conclusion:** Technology names do not determine architectural significance.

### Example 3

**Question:** Where should retry policy be decided?

**Reasoning:** A local retry of an idempotent internal read may be detailed design within latency and load budgets. Retrying payment authorization or message publication changes duplicate, unknown-outcome, capacity, and reconciliation behavior across systems. Stable operation identity and ownership become architectural obligations.

**Conclusion:** Retry semantics escalate when externally visible effects and shared budgets are involved.

### Example 4

**Question:** Should architecture prescribe every class in a module?

**Reasoning:** Usually no. State module responsibility, allowed dependencies, critical invariants, interfaces, and quality budgets. Let the owning team choose classes and algorithms. Prescribe internal structure only when it is necessary evidence for a material concern, such as enforced separation of safety-critical and noncritical code.

**Conclusion:** Architecture should preserve required properties while leaving meaningful implementation freedom.

### Example 5

**Question:** A JSON field was intended as internal but clients persisted it. What changed?

**Reasoning:** Operational evidence shows the field has become an external compatibility commitment. Its removal now affects clients, migration, support, and data semantics. Reclassify the decision, establish version and deprecation policy, and correct the boundary that allowed undocumented dependence.

**Conclusion:** Realized reach can turn a detailed choice into an architectural decision.

### Example 6

**Question:** Can a team independently spend its 400 ms latency budget?

**Reasoning:** Yes within defined workload, percentile, observation, retry, failure, and resource obligations, provided the end-to-end owner monitors composition and margin. A local optimization that shifts load or tail latency to another component violates delegation even if the local metric passes.

**Conclusion:** Budgets enable autonomy only with composition and shared-effect rules.

### Example 7

**Question:** Is one repository evidence of a monolith architecture?

**Reasoning:** It proves a source-control arrangement. Modules may have strong boundaries and independent runtime deployment; conversely, many repositories may share a database and release process, forming a distributed monolith. Inspect module dependencies, runtime calls, data authority, deployment, ownership, and change coupling.

**Conclusion:** Source layout is one view and cannot substitute for architecture analysis.

### Example 8

**Question:** When should implementation challenge an approved protocol decision?

**Reasoning:** Escalate when tests show the protocol cannot preserve required ordering, identity, accessibility, failure, security, performance, or version semantics; when dependencies differ from assumptions; or when workarounds create broader coupling. Record reproducible evidence and affected ASRs rather than bypassing governance silently.

**Conclusion:** Approval does not override contradictory implementation evidence.

### Example 9

**Question:** Is a platform golden path architecture or detailed design?

**Reasoning:** Shared identity, telemetry, deployment, and policy interfaces can be architectural across consuming systems. The platform’s internal orchestration and libraries may be detailed design. Consumers need explicit obligations, freedoms, service expectations, escape paths, and failure boundaries; adoption alone does not establish fit.

**Conclusion:** Classification can differ on either side of a platform boundary.

### Example 10

**Question:** Who classifies a dosing-controller decision as architectural?

**Reasoning:** Analyze its influence on clinical intent, hazards, timing, sensing, human override, cybersecurity, verification independence, and lifecycle evidence. A tiny numeric type or rounding rule may be safety-significant. No external clinical, safety, regulatory, human-factors, cybersecurity, or practitioner review is claimed; named qualified authorities must approve applicable classifications, constraints, evidence, and residual risk.

**Conclusion:** Consequence and authority, not implementation size or architect title, govern high-consequence classification.

## Cross-Program Connections

- [Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) develops local decomposition, invariants, interfaces, and domain boundaries within architectural constraints.
- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) applies recurring design structures at both architectural and detailed scales when forces justify them.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies conformance, component, integration, and end-to-end evidence.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) reveals deployment, operation, recovery, and feedback consequences.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) relates system architecture, allocation, detailed design, interfaces, verification, and lifecycle baselines.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) develops cross-boundary contracts while preserving internal implementation freedom.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) governs shared architectural capabilities and team-local design choices.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 42010:2022, Software, systems and enterprise—Architecture description](https://www.iso.org/standard/74393.html), edition 2, November 2022. Current distinction between architecture and architecture description and requirements for concerns, views, viewpoints, model kinds, and correspondence; consulted 2026-09-05.
2. Software Engineering Institute. [Software Architecture](https://www.sei.cmu.edu/software-architecture/), Carnegie Mellon University. Current overview of architecture as design decisions about overall structure and behavior supporting early quality analysis and evolution; consulted 2026-09-05.
3. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. Architecture structures, quality attributes, significant decisions, tactics, evaluation, and evolution.
4. Humberto Cervantes and Rick Kazman. *Designing Software Architectures: A Practical Approach*, Addison-Wesley, 2016. Architecture design, drivers, structures, decisions, and iterative realization.
5. Paul Clements et al. *Documenting Software Architectures: Views and Beyond*, second edition, Addison-Wesley, 2010. Concern-driven views, interfaces, element catalogs, context, rationale, and variability.
6. David L. Parnas. “On the Criteria To Be Used in Decomposing Systems into Modules.” *Communications of the ACM* 15(12), 1972. Information hiding and decomposition around changeable design decisions.
7. Dewayne E. Perry and Alexander L. Wolf. “Foundations for the Study of Software Architecture.” *ACM SIGSOFT Software Engineering Notes* 17(4), 1992. Elements, form, rationale, styles, and distinctions in architecture study.
8. Richard N. Taylor, Nenad Medvidović, and Eric M. Dashofy. *Software Architecture: Foundations, Theory, and Practice*, Wiley, 2009. Architectural models, design spaces, implementation, analysis, and evolution.

## Exercises

### Exercise 1

Classify these decisions for an online bookstore and justify context: sorting algorithm inside search, canonical book identifier, checkout timeout, internal variable naming, and deployment region.

### Exercise 2

Define obligations and freedoms for a team owning an inventory component under end-to-end order correctness, latency, availability, and audit requirements.

### Exercise 3

Diagnose an architecture document containing one cloud diagram, every source class, no runtime or data view, and a rule requiring central approval for all library upgrades.

### Exercise 4

Compare treating event-schema evolution as centralized architecture versus delegated detailed design. Define when each is appropriate and how evidence should trigger escalation.

### Exercise 5

Design classification and delegation governance for an unfamiliar autonomous warehouse safety system. Separate automated conformance, implementation evidence, qualified authority, and blockers.

## Answers to the Exercises

### Answer 1

The search sorting algorithm is local if it remains behind relevance, latency, and resource obligations; it becomes architectural if ranking is a regulated or shared contract. A canonical book identifier is likely architectural because data, partners, persistence, and migration depend on it. Checkout timeout is architectural when it changes payment unknown outcomes, inventory reservations, and user promises. Internal variable naming is local unless a generated or certified interface gives it external semantics. Deployment region is architectural when latency, residency, availability, supplier, or recovery objectives depend on it.

Full credit requires naming the bookstore boundary, clients, data authority, partners, qualities, and reversal cost. Mechanism category alone never settles classification.

### Answer 2

Obligations: one declared authority for inventory reservation state; stable operation identities; no double allocation; explicit reserved, rejected, pending, expired, and reconciled states; compatible API/event semantics; allocated latency and availability budgets; audit evidence; authorization; timeout and duplicate behavior; monitoring; recovery; schema/version policy; and escalation when assumptions fail. The end-to-end order owner retains composition and customer-outcome responsibility.

Freedoms can include internal algorithms, indexes, table layout, module decomposition, programming language or libraries within supported constraints, caching within freshness rules, tests, refactoring, and release scheduling within compatibility policy. Evidence includes invariant and concurrency tests, contract tests, load/failure tests, recovery exercises, dependency checks, and production indicators. A local choice that changes authority, external semantics, shared resources, or budgets crosses the boundary and requires architectural review.

### Answer 3

The cloud diagram is one deployment-oriented artifact and cannot express all module, runtime, data, interface, operational, and context concerns. Including every source class destroys abstraction and maintainability while still omitting meaningful correspondence. Add purpose-specific views with defined semantics and only decision-relevant details. Link architecture decisions, ASRs, assumptions, interfaces, and evidence.

Central approval for all upgrades treats reversible local implementation as architecture, creates delay, and shifts ownership. Define supported security, compatibility, licensing, platform, evidence, and deployment obligations; automate relevant checks; let owners upgrade within them; escalate changes affecting cross-boundary contracts, shared runtime, significant qualities, suppliers, or residual risk. Retain a justified exception process and feedback route.

### Answer 4

Central treatment is appropriate when schemas are durable cross-team or external contracts, persisted for long periods, carry regulated meaning, affect replay or migration, or require coordinated compatibility. Architecture should define authority, semantic versioning, compatibility windows, identity, ordering, privacy, retention, migration, and retirement. Local fields inside one owned boundary can evolve as detailed design if no external consumer, stored contract, or shared evidence depends on them.

Delegation requires schema visibility analysis, contract tests, consumer discovery, compatibility checks, and publication rules. Evidence of independent consumers, persisted payloads, failed upgrades, broad coordination, or legal meaning triggers escalation. Evidence that a schema is fully private and migratable may support delegation. Central governance should set semantic obligations, not approve every harmless field refactoring.

### Answer 5

Map safety functions, sensors, motion control, human presence, emergency stop, identity, networks, power, maintenance, diagnostics, updates, degraded operation, and recovery. Classify decisions by hazard consequence, reach, timing, independence, reversal cost, evidence, and applicable authority. Small numeric, scheduling, or default choices can be architectural when they affect protective behavior.

Automated checks can enforce dependency isolation, interface schemas, timing budgets in specified models, configuration bounds, trace links, evidence digests, and selected invariants. Tests, simulation, fault injection, hardware-in-the-loop work, field trials, and operational monitoring provide bounded evidence. They do not establish hazard completeness or acceptable risk alone. No external warehouse, machinery-safety, regulatory, human-factors, cybersecurity, or practitioner review is claimed. Named qualified authorities must own hazards, safety requirements, independence, validation, release, and residual-risk acceptance. Unclear emergency authority, violated protective timing, unverified sensors, unsafe degraded behavior, or unresolved high-severity hazards block the corresponding readiness claim.
