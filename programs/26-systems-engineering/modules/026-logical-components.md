---
module_id: SYSENG-026
program: Systems Engineering
level: 1
module_number: 26
title: Logical Components
status: complete
last_verified: 2026-08-31
---

# Logical Components

## One-Page Review

### Governing question

How can a team organize system responsibilities, state, policies, provided/required capabilities, and interactions into logical components that make architecture alternatives analyzable and allocatable—without prematurely equating those components with hardware, software services, teams, suppliers, processes, or deployment units?

### Essential definitions

- A **logical component/element** is an implementation-independent architectural unit that groups coherent responsibilities, state/policy ownership, and provided/required interactions for analysis and later allocation.
- A **responsibility** is an accountable behavioral or information obligation owned by a logical component; it is not merely a function copied into another box.
- A **provided interface/capability** states what a component offers at its boundary; a **required interface/capability** states what it needs from another role or environment.
- A **logical interface** is a governed interaction between logical elements, independent of the final physical transport or deployment mechanism.
- **Cohesion** is the degree to which responsibilities within a component share purpose, state, authority, change drivers, or quality constraints.
- **Coupling** is dependency between components through data, matter, energy, control, timing, shared state/resources, faults, authority, or lifecycle change.
- A **logical partition** groups responsibilities into elements according to explicit architecture criteria; alternative partitions may satisfy the same functional behavior.
- A **logical configuration item** is a controlled logical element with allocated functions/properties/interfaces suitable for decisions or specification, still distinct from a specific physical realization.
- **Allocation** maps functions, requirements, logical components, and physical elements many-to-many with rationale; identity across views must never be inferred from identical names.
- A **trust/fault/authority boundary** identifies where assumptions, privileges, failure containment, or decision rights change; one logical boundary may serve several concerns.
- An **architecture viewpoint** frames models for particular stakeholders and concerns; the model is an architecture description, not the architecture or system itself.
- A **facade/adaptor/coordinator** is justified only when it owns a durable boundary transformation or policy—not because a diagram needs another layer.

### Central model, mechanism, or theorem

Represent the logical architecture as a typed directed multigraph:

\[
G_L=(C,I),\qquad
c=\langle id,R,S,P^+,P^-,Q,A,H,V\rangle,
\]

where components \(C\) own responsibilities \(R\), state/policy \(S\), provided interfaces \(P^+\), required interfaces \(P^-\), quality constraints \(Q\), authority/applicability \(A\), assumptions \(H\), and verification rationale \(V\). Edges \(I\) have typed semantics, contracts, direction, version, and failure behavior.

For provided port \(p_i^+\) and required port \(p_j^-\), compatibility requires:

\[
Compatible(p_i^+,p_j^-)=Semantics\land Type\land Unit\land Range
\land Timing\land Quality\land Security\land Mode\land Version.
\]

A partition is acceptable only conditionally:

\[
Accept(P)\Rightarrow Coverage\land CoherentOwnership\land
CompatibleInteractions\land QualityComposition\land FeasibleAllocation
\land AcceptedTradeoffs.
\]

No graph shape or partition score proves those semantic predicates.

### Critical invariants

- Every logical component has stable identity, purpose, responsibilities, owned state/policy, provided/required interactions, quality constraints, owner, rationale, and applicability.
- Every responsibility traces to functions, requirements, hazards/threats, interfaces, lifecycle needs, or an approved architecture decision.
- Logical boundaries derive from explicit concerns such as cohesion, change, authority, trust, fault containment, timing, locality, resources, reuse, or acquisition—not existing organization alone.
- Logical, functional, physical, organizational, supplier, process, and deployment views remain distinguishable and connected by typed allocations.
- Required and provided ports agree semantically or use an explicit transformation/adaptor with owned behavior and evidence.
- State has one authoritative logical owner or a governed replication/consistency model; shared mutable state is never implicit.
- Crosscutting behavior—safety, security, timing, observability, configuration, recovery—is allocated without creating an unaccountable catch-all component.
- Logical elements cover relevant nominal, degraded, emergency, maintenance, update, recovery, and retirement behavior.
- End-to-end qualities are composed across component interactions, shared resources, and environment; local targets do not automatically prove system outcomes.
- Alternative partitions are compared against the same controlled scenarios, requirements, constraints, and evidence basis.
- Mapping to physical realization records cardinality, configuration, rationale, residual dependencies, and changes rather than relying on naming coincidence.
- Executable/model checks remain bounded by encoded component/edge attributes and do not establish architecture correctness, safety, or organizational feasibility.

### Common failures

Failures include copying a functional hierarchy into a component hierarchy; naming components after current teams or products; treating every function as a component; creating `manager`, `utility`, or `core` catch-alls; hiding shared state in a database box; drawing request/response arrows without semantic contracts; optimizing for low edge count while concentrating risk; making safety/security one isolated component instead of allocating crosscutting responsibilities; assuming one component becomes one microservice or hardware item; duplicating state for availability without consistency/recovery semantics; making logical boundaries equal supplier contracts before trade study; and claiming an architecture is modular because boxes are visually separate.

### Compact example

For emergency messaging, candidate logical components include Request Authority, Message Policy, Delivery Coordination, Channel Adaptation, Durable Evidence, and Operational Escalation. Request Authority owns identity/authorization decisions; Message Policy owns classification and deadline policy; Delivery Coordination owns message lifecycle/idempotency and route state; adapters translate channel-specific semantics; Durable Evidence owns immutable disposition records; Escalation owns human handoff. These are not necessarily services or teams. A centralized alternative combines policy and coordination; a federated alternative distributes route autonomy. Both are evaluated against the same degraded-network, duplicate-acknowledgement, privacy, timing, and recovery scenarios before physical allocation.

### Connections

Logical components synthesize function/decomposition, FFBD, state/mode, and scenario models from SYSENG-021–025. SYSENG-027 allocates functions to them; SYSENG-028 details control/data flows; SYSENG-029 compares alternatives. Later modules address interfaces, physical architecture, trades, verification, safety, security, operations, and configuration.

## Governing Question

Functions say what transformations occur; scenarios and behavioral models say how they unfold. Architecture also needs stable places to own responsibilities, state, policies, and boundary contracts. Logical components provide those places before the team commits them to a processor, service, person, vehicle, facility, supplier, or organizational unit.

The abstraction is valuable only if it preserves alternatives while exposing consequences. A component too abstract to state ownership or interfaces cannot guide design. A component named after a selected database, cloud service, department, or part number has already become physical/organizational. The governing question asks how to draw responsibility boundaries at the decision-relevant level and keep mappings to other views honest.

## Why This Matters

Bad logical boundaries harden into integration and governance problems. Shared mutable state has no owner. A failure propagates across a supposedly independent module. One team must coordinate every change. Security authorization is repeated inconsistently. A human is given leftover exceptions. Suppliers deliver locally compliant elements whose interactions cannot satisfy the system outcome.

ISO/IEC/IEEE 42010:2022 is the current published architecture-description standard; it distinguishes an architecture from its description and structures descriptions around concerns, viewpoints, and model kinds without prescribing a method. ISO/IEC/IEEE 15288:2023 supplies the current lifecycle process context. NASA’s current Logical Decomposition guidance emphasizes strategic organization of functional elements, relationships, dependencies, and interfaces, iterative alternatives, and later partitioning/allocation. SEBoK 2.14 describes logical elements as technology-independent structural elements with allocated functions, properties, interfaces, and later physical realization. These sources support disciplined description, not a universal definition that every domain uses identically.

Logical architecture is also a trade space. Centralizing state can simplify consistency but create a fault/trust bottleneck. Distributing authority can improve autonomy but increase coordination and evidence burden. A defensible component model retains the reasons for its boundaries and the conditions under which they should change.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. functions are purposeful transformations, not components;
2. functional decomposition and FFBD/state/scenario views describe behavior at complementary abstractions;
3. interfaces require typed semantic, timing, quality, failure, and authority contracts;
4. requirements allocation is many-to-many and needs contribution/coverage rationale;
5. traceability and configuration link exact versions of needs, functions, decisions, components, realization, and evidence;
6. crosscutting qualities such as safety, security, reliability, privacy, accessibility, and maintainability emerge from interactions;
7. architecture alternatives must be evaluated against common controlled criteria and scenarios;
8. models are evidence-bearing descriptions with abstraction limits.

As a retrieval test, inspect components named `Frontend`, `Backend`, `Database`, and `Admin Team`. They mix deployment/software technology, storage mechanism, and organization. They do not say who owns authorization, session state, business policy, evidence, recovery, or external semantics. The boxes may depict an existing realization, but they are not yet a clear logical responsibility model.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish logical component from function, physical element, software unit, deployment unit, organization, supplier, and process;
2. define component purpose, responsibilities, state/policy ownership, provided/required interactions, and qualities;
3. partition functions using explicit cohesion, coupling, authority, trust, fault, timing, locality, resource, reuse, and change criteria;
4. represent logical architecture as governed typed components and interactions across viewpoints;
5. expose and resolve shared state, circular dependency, orchestration, and crosscutting-responsibility problems;
6. compare centralized, distributed, layered, pipeline, event-driven, and federated logical alternatives;
7. compose end-to-end performance, reliability, safety, security, privacy, and operability arguments across boundaries;
8. define testable logical interfaces without committing prematurely to transport/technology;
9. map logical components to physical/organizational realizations many-to-many with rationale;
10. review high-consequence logical architecture with bounded model and empirical evidence.

## Core Exposition

**Frame the architecture description.** Identify entity/system of interest, stakeholders, concerns, viewpoint/model kind, lifecycle phase, configuration, assumptions, decisions, and notation/metamodel. A logical component view for security differs from one for procurement or timing, though governed elements and relationships should remain consistent.

**Start from controlled behavior.** Use function contracts, decompositions, FFBDs, state/mode models, and scenario portfolio. Inventory transformations, persistent state, policies, external interactions, failures, timing, and lifecycle functions. Do not invent boxes first and force behavior into them.

**Identify responsibility clusters.** Group behavior that shares purpose, state, invariants, authority, quality constraints, change drivers, or specialized knowledge. State each responsibility as an accountable obligation. A component may perform several functions; a function may require collaboration among components.

**Define purpose and scope.** A logical component’s purpose explains why the boundary exists and what concern it stabilizes. List included and explicitly excluded responsibilities. If the scope can grow whenever ownership is unclear, the component is a catch-all rather than an architecture boundary.

**Analyze negative space and competing ownership.** Build a responsibility-to-component matrix that distinguishes accountable owner, contributor, consumer, reviewer, and external authority. Search for responsibilities with no accountable owner, multiple conflicting owners, or ownership that changes silently by mode or failure. Inspect boundary work such as validation, reconciliation, cancellation, version negotiation, recovery, evidence, and disposal; these are frequently omitted because no nominal function “owns” them. Conversely, two components may both claim policy or state authority and produce divergent decisions. Resolve the semantic authority first, then define collaboration and escalation. A matrix cell is not proof that an actor can perform the responsibility under load, fault, or legal constraints; scenario and evidence review remain necessary.

**Preserve identity through boundary evolution.** Logical components should change when responsibility rationale changes, not whenever a deployment or team is reorganized. Record splits, merges, supersession, state migration, interface compatibility, and trace impact. A split must allocate every former responsibility and invariant; a merge must analyze increased trust, fault, change, and verification scope. Historical evidence remains applicable only through an explicit equivalence argument. Track architecture debt such as provisional boundaries, duplicated policy, bypass interfaces, and unresolved state ownership with risk, owner, deadline, and removal criteria rather than allowing the temporary realization to redefine the logical model silently.

**Assign state and policy ownership.** Identify authoritative state variables, lifecycle, persistence, consistency, version, access, retention, recovery, and derived replicas. Identify policies and decision rights. A shared database does not make all writers co-owners; define who may change meaning and who materializes copies.

**Define provided capabilities.** State what other components/actors may rely on: semantic operation or flow, preconditions, inputs, outputs/effects, postconditions, errors, idempotency, timing, quality, security/privacy, modes, version, and evidence. Keep technology-neutral until a selected constraint requires protocol detail.

**Define required capabilities.** State dependencies rather than assuming they exist. Include required semantic behavior, quality, authority, availability/degradation, and failure handling. Required ports make external assumptions visible and allow alternative providers/realizations to be assessed.

**Type logical interactions.** Distinguish command, query, event, stream, material/energy flow, state synchronization, resource use, and governance/authority relations. Direction, initiation, response, ownership, timing, version, and failure semantics matter. One line labeled “data” is not an interface.

**Separate orchestration and collaboration.** Central orchestration can own end-to-end progression; choreography distributes reactions according to contracts. Orchestration simplifies visibility but can concentrate coupling/failure. Choreography improves autonomy but can create emergent loops and unclear outcome ownership. Record who owns the system-level outcome either way.

**Seek cohesion without dogma.** Responsibilities that change together for the same reason, use the same authoritative state, or enforce one invariant often belong together. Splitting them may create chatty interfaces and inconsistent policy. Excessive cohesion claims can also hide a monolith; challenge independent change, scaling, assurance, and authority needs.

**Characterize coupling.** Record semantic, temporal, state, resource, failure, security, organizational, and lifecycle coupling. Counted edges alone are misleading: one synchronous safety-critical dependency can dominate ten low-risk events. Ask whether a component can be reasoned about, changed, verified, degraded, and recovered without hidden coordination.

**Control shared mutable state.** Prefer a clear owner and versioned access semantics. Where replication is necessary, define source of truth, consistency model, conflict resolution, partition behavior, staleness bounds, reconciliation, audit, and deletion. Availability gained through copies can reduce integrity or privacy unless governed.

**Define authority and trust boundaries.** Identify authentication, authorization, privilege, data classification, assurance level, audit, and policy ownership at crossings. Trust boundary is not synonymous with network hop. A single process can contain mutually untrusted responsibilities; separate machines can belong to one trust domain.

**Define fault-containment boundaries.** Analyze failure propagation through calls, shared power, clocks, data, physical coupling, operators, suppliers, and recovery mechanisms. A logical boundary supports containment only when realization preserves the necessary independence. Record common-cause assumptions and degraded contracts.

**Allocate safety and security responsibilities.** Crosscutting concerns require component-owned controls plus system-level coordination/assurance. A `Safety Manager` or `Security Service` cannot make unsafe components safe by presence. Trace prevention, detection, containment, response, recovery, evidence, and residual-risk authority across all relevant elements.

**Allocate observability and evidence.** Define what each component reports, with provenance, time, configuration, integrity, privacy, and diagnostic limits. Self-reported health is not independent proof. End-to-end evidence correlates component observations and physical outcomes without centralizing all sensitive data unnecessarily.

**Compose performance.** Allocate latency, throughput, capacity, jitter, accuracy, and resource budgets across components/interactions with path and concurrency semantics. Include queueing, serialization, contention, retries, and physical response. A component meeting its local target does not prove the end-to-end scenario.

**Compose reliability and availability.** Determine serial/parallel dependencies, redundancy, failover detection, state transfer, common cause, repair, and degraded success criteria. Independence assumptions need architectural and physical evidence. Availability of component instances is not stakeholder service availability.

**Include human logical components carefully.** Model human roles/responsibilities, authority, information, workload, capability, training, and error/recovery. Do not assign automation leftovers to an `Operator` box. Later allocation may divide one logical role among people and automation or combine several roles under one person.

**Include enabling/lifecycle components.** Configuration, update, calibration, identity/key management, diagnostics, maintenance, training, provisioning, migration, backup, support, and disposal may need logical ownership. Avoid hiding them under `Operations` if their interfaces/invariants drive design.

**Use hierarchy only where meaningful.** Logical systems, subsystems, assemblies, or components can nest for viewpoint and control. Parent-child means structural containment, not necessarily function decomposition or runtime call. Preserve crosscutting interactions and do not force every graph relation into a tree.

**Detect cycles and layering violations.** Dependency cycles can prevent independent change, startup, recovery, or verification. Some feedback/control cycles are intentional. Type edges and assess whether cycles are semantic, temporal, state, or deployment concerns. Break harmful cycles with responsibility changes, stable contracts, events, or explicit coordination—not arbitrary facades.

**Justify adaptors and facades.** An adaptor owns translation of semantics, units, versions, timing, or trust; a facade stabilizes a provided contract; a coordinator owns progression/policy. Each has state, failure, quality, and evidence obligations. Avoid pass-through layers that conceal coupling without changing it.

**Explore alternative partitions.** Compare centralized versus federated state, layered versus peer collaboration, pipeline versus event-driven flow, shared versus separate assurance, and human/automation boundaries. Keep behavior/scenarios and external contract stable so the architecture difference is clear.

**Evaluate alternatives across concerns.** Use stakeholder outcomes, performance, resilience, safety, security, privacy, human workload, adaptability, operability, testability, acquisition, cost/schedule, technology maturity, and retirement. Preserve assumptions, sensitivity, noncompensatory constraints, dissent, and evidence limits.

**Map to physical realization explicitly.** A logical component may be deployed redundantly across hardware/software/personnel; one physical item may realize several logical components; a function may span both. Record mapping, configuration, performance/independence effects, make/buy decisions, and trace. Do not rename a logical element to a product after selection; preserve view distinctions.

**Map to organization and suppliers cautiously.** Team boundaries can align with responsibility/change authority but are not architecture truth. Conway-like pressures can be considered without freezing today’s chart. Supplier boundaries introduce contract, evidence, interface, change, data-rights, and integration concerns; system authority retains outcome responsibility.

**Derive logical requirements.** Derive component/interface performance, state, fault, trust, observability, lifecycle, and compatibility requirements with source/rationale. Validate necessity, feasibility, verifiability, and authority. Architecture-derived requirements are not parent requirements disguised as facts.

**Verify the logical architecture.** Check component/port identity, allowed relation types, responsibility coverage, state ownership, required/provided compatibility, unresolved dependencies, cycles, trace, mode applicability, and view consistency. Execute/simulate critical paths and failures. Empirical verification ultimately targets realizations and system outcomes.

**Govern evolution.** Baseline component semantics, interfaces, allocation decisions, and views. When behavior, state, scenario, hazard, supplier, or technology changes, traverse impacts and reconsider boundaries. A stable logical component can survive realization changes; if its rationale no longer holds, change it through architecture governance.

The following checker detects selected missing declarations in five logical-component records. It cannot judge architectural quality.

<!-- bijux-verify: {"id":"logical-component-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"components_total=5\nwell_formed_declared=1\nmissing_responsibilities=LC-002\nmissing_provided=LC-003\nmissing_required=LC-004\nmissing_rationale=LC-005\nunresolved=LC-002,LC-003,LC-004,LC-005\nevidence=declared_fields_only\n","stderr":""}} -->
```python
components = [
    {"id": "LC-001", "responsibilities": ["own request authority"],
     "provided": ["authorization decision"], "required": ["identity evidence"],
     "rationale": "separate authority and trust boundary"},
    {"id": "LC-002", "responsibilities": [], "provided": ["classification"],
     "required": ["validated request"], "rationale": "own message policy"},
    {"id": "LC-003", "responsibilities": ["coordinate delivery"], "provided": [],
     "required": ["classified message"], "rationale": "own lifecycle state"},
    {"id": "LC-004", "responsibilities": ["adapt channel semantics"],
     "provided": ["channel attempt"], "required": [], "rationale": "isolate variants"},
    {"id": "LC-005", "responsibilities": ["retain evidence"],
     "provided": ["disposition record"], "required": ["delivery events"], "rationale": ""},
]
required = ("responsibilities", "provided", "required", "rationale")
valid = [item for item in components if all(item[field] for field in required)]
print(f"components_total={len(components)}")
print(f"well_formed_declared={len(valid)}")
for field in required:
    print(f"missing_{field}=" + ",".join(item["id"] for item in components if not item[field]))
print("unresolved=" + ",".join(item["id"] for item in components if item not in valid))
print("evidence=declared_fields_only")
```

Even LC-001 may be the wrong boundary. Nonempty lists do not establish semantic coverage, cohesion, compatibility, or feasible realization.

## Definitions and Notation

Let function set \(F\), logical components \(C\), physical elements \(P\), and organizations \(O\) remain separate domains. Allocation relations are:

\[
A_{FC}\subseteq F\times C,\quad A_{CP}\subseteq C\times P,
\quad A_{CO}\subseteq C\times O.
\]

None is assumed one-to-one or identity. Each edge carries contribution/responsibility, configuration, authority, and evidence.

For a logical path \(p=(c_1,i_{12},c_2,\ldots,c_n)\), end-to-end property \(Q_p\) is computed by property-specific composition \(\Phi_Q\):

\[
Q_p=\Phi_Q(Q_{c_1},Q_{i_{12}},\ldots,Q_{c_n},H,Environment).
\]

Latency may add/max; reliability may multiply only under assumptions; security and safety rarely reduce to scalar arithmetic. Always name \(\Phi_Q\) and its evidence.

For candidate partition \(P_k\), a decision vector can record scored/preference criteria, but hard constraints remain noncompensatory. Sensitivity analysis checks whether plausible weights/assumptions reverse preference; the score does not authorize safety, legal, or stakeholder tradeoffs by itself.

## Mechanisms, Invariants, or Proof Structure

Use a logical-architecture loop:

1. **Frame concerns/viewpoints:** identify stakeholders, decisions, system boundary, lifecycle, configuration, constraints, and modeling semantics.
2. **Inventory behavior/state:** collect functions, scenarios, modes, interfaces, resources, failures, policies, and lifecycle responsibilities.
3. **Partition:** propose coherent responsibility/state/authority clusters and typed provided/required interactions; retain alternatives.
4. **Analyze composition:** examine coupling, state consistency, timing/resources, failure/trust boundaries, humans, crosscutting qualities, and scenario outcomes.
5. **Compare:** evaluate alternatives against common controlled criteria, expose assumptions/sensitivity, and obtain competent decisions.
6. **Allocate and derive:** map many-to-many to physical/organizational realizations and derive justified component/interface requirements.
7. **Verify and govern:** check model consistency, simulate/execute bounded cases, validate realization/system outcomes, baseline, and revisit after change/evidence.

This mechanism produces a reviewable architecture description and rationale. It cannot prove that all responsibilities were discovered, organizational incentives align, supplier evidence is sufficient, or a future realization preserves logical independence.

## Alternatives and Trade-Offs

**Capability/domain grouping** aligns responsibilities with stakeholder concepts and change. **Layering** controls dependency direction and abstraction but can add latency/pass-through behavior. **Pipelines** clarify transformations but can couple sequence and error handling. **Event-driven collaboration** decouples time but adds eventual consistency and emergent behavior.

**Centralized state/policy** simplifies consistency, audit, and authority but creates bottleneck/fault/trust concentration. **Federated ownership** supports autonomy and locality but needs versioning, conflict resolution, and global-outcome coordination.

**Fine-grained components** allow targeted allocation/change but increase interfaces, latency, and governance. **Coarse-grained components** reduce crossings but concentrate responsibilities and scaling/assurance burden. Choose by concerns, not a universal component count.

**Shared logical services** promote reuse/consistency but couple consumers to common evolution and failure. **Duplicated local responsibility** improves autonomy but risks policy divergence. Stable semantic contracts and product-line analysis guide the choice.

**Human-centered logical roles** expose authority/workload before automation. **Automation-first boundaries** can optimize machine flow but hide operational recovery. Explore allocation alternatives while preserving human-system outcome evidence.

## Failure Modes and Misconceptions

- **“Logical component means software module.”** It may later map to software, hardware, people, facilities, or combinations.
- **“One function, one component.”** Functions and components have many-to-many relations.
- **“Fewer arrows means lower coupling.”** Edge semantics and consequence dominate count.
- **“A database owns the data.”** Storage mechanism is not semantic authority or policy ownership.
- **“The security component handles security.”** Trust and control responsibilities cross all relevant elements.
- **“Team boundaries define architecture.”** Organization is one allocation/view and can change.
- **“Independent logical boxes imply fault independence.”** Physical/shared-resource/common-cause evidence must preserve independence.
- **“A passing interface schema proves compatibility.”** Meaning, timing, quality, modes, authority, and failure behavior remain.
- **“Logical equals technology-free forever.”** Constraints/decisions increase detail; view distinctions still remain explicit.
- **“The architecture model is the architecture.”** It is a controlled description with abstraction and fidelity limits.

## Worked Examples

### Example 1

**Cold-chain system.** Logical elements include Thermal-State Knowledge, Thermal Control Policy, Heat-Transfer Coordination, Payload Evidence, and Operator Escalation. Sensors/controllers/compressors are later realizations. State ownership and uncertainty are explicit. Chamber evidence supports selected physical allocations/configurations, not the logical partition universally.

### Example 2

**Flood warning.** Observation Authority, Forecast/Uncertainty, Warning Decision Authority, Dissemination Coordination, and Public Response Evidence separate data production from legal/operational authority. Central versus regional decision is an alternative. Historical replay cannot establish unprecedented weather or public response.

### Example 3

**Aircraft braking.** Demand Interpretation, Ground-State Knowledge, Brake Allocation, Actuation Coordination, and Independent Effect Monitoring form a logical control structure. Fault containment requires later physical independence. Safety/certification evidence cannot be inferred from separated boxes.

### Example 4

**Account recovery.** Identity Evidence, Risk Policy, Recovery Orchestration, Channel Adaptation, Credential Authority, and Dispute/Audit own distinct trust/state boundaries. Email is a physical/channel choice. Security tests cover modeled attacks and realizations, not universal identity proof.

### Example 5

**Water treatment.** Source Acceptance, Treatment Policy, Process Coordination, Quality Authority, Distribution Release, and Residual Management expose release authority separately from treatment mechanism. Regulatory laboratory evidence constrains decisions. Local pass states do not prove distributed potability.

### Example 6

**Warehouse fulfillment.** Order Authority, Inventory State, Fulfillment Planning, Execution Coordination, Item Evidence, and Exception Resolution separate authoritative inventory from robot/team allocation. Peak-load tests support named layouts/resources; organization mapping may change.

### Example 7

**Satellite operations.** Mission Intent, Vehicle State Knowledge, Activity Planning, Execution Coordination, Fault Protection, and Ground Interaction can be centralized or federated. Common clocks/power can defeat logical independence. Simulation remains bounded by orbit/fault models.

### Example 8

**Clinical alert.** Clinical Data Authority, Risk Estimation, Clinical Policy, Workflow Coordination, Presentation/Escalation, and Outcome Evidence clarify that a model score does not own treatment authority. Clinical, human-factors, safety, privacy, security, and regulatory evidence remain necessary.

### Example 9

**Regional service.** Desired-State Authority, Deployment Coordination, Traffic Policy, Data-Migration Authority, Health Evidence, and Recovery Coordination make rollout/migration coupling visible. These are not automatically microservices. Chaos evidence covers injected topologies/failures only.

### Example 10

**Autonomous shuttle door.** Boarding Context, Door-State Knowledge, Motion Authority, Door Control, Independent Interlock, and Human/Emergency Coordination define responsibilities. Later allocation must preserve independence and accessibility. Fixture tests cannot establish all rider/environment outcomes.

## Cross-Program Connections

- **Platform Engineering:** platform capabilities need logical ownership of policy, desired state, evidence, provisioning, recovery, and developer interaction before service/team boundaries.
- **API and Service Engineering:** bounded contexts and service contracts can realize logical components, but service topology is a later allocation with runtime coupling.
- **Data Engineering:** semantic ownership, lineage, quality policy, orchestration, and storage realization must remain distinct.
- **Object-Oriented Programming:** classes/objects can realize responsibilities; object decomposition should not replace system architecture concerns.
- **Functional Programming:** modules/effect boundaries can realize logical contracts while distributed state, time, authority, and physical effects remain architectural.
- **Safety/security:** logical trust/fault/control/evidence boundaries provide inputs to assurance, but physical independence and competent authority must be demonstrated.

## References

1. ISO, “ISO/IEC/IEEE 42010:2022 — Software, systems and enterprise — Architecture description,” second edition, published 2022-11. https://www.iso.org/standard/74393.html
2. ISO, “ISO/IEC/IEEE 15288:2023 — Systems and software engineering — System life cycle processes,” second edition, published 2023-05. https://www.iso.org/standard/81702.html
3. NASA, “4.3 Logical Decomposition,” NASA Systems Engineering Handbook. https://www.nasa.gov/reference/4-3-logical-decomposition/
4. NASA, “4.0 System Design Processes,” NASA Systems Engineering Handbook. https://www.nasa.gov/reference/4-0-system-design-processes/
5. NASA, “System Engineering Handbook: Appendix,” architecture and system-definition review definitions. https://www.nasa.gov/reference/system-engineering-handbook-appendix/
6. NASA, “5.2 Product Integration,” interface and interaction integration guidance. https://www.nasa.gov/reference/5-2-product-integration/
7. SEBoK Editorial Board, “Logical Architecture,” *Guide to the Systems Engineering Body of Knowledge*, version 2.14. https://sebokwiki.org/wiki/Logical_Architecture
8. SEBoK Editorial Board, “Logical Architecture (glossary),” version 2.14. https://sebokwiki.org/wiki/Logical_Architecture_%28glossary%29
9. SEBoK Editorial Board, “System Architecture Design Definition,” logical and physical structural elements, version 2.14. https://sebokwiki.org/wiki/System_Architecture_Design_Definition
10. NASA, *Systems Architecture*, NASA/CR-20250007048, logical element metamodel example. https://ntrs.nasa.gov/api/citations/20250007048/downloads/CR-20250007048.pdf

## Exercises

### Exercise 1

Replace the proposed components `Mobile App`, `Cloud Backend`, `Database`, and `Support Team` for an emergency-message system with logical responsibility components. Explain mappings that remain undecided.

### Exercise 2

An end-to-end path has component bounds 40, 55, and 35 ms; interface bounds 15 and 20 ms; queue bound 25 ms; required margin 10%. Compute the additive bound and determine compliance with a 200 ms deadline, stating assumptions.

### Exercise 3

Compare centralized and federated logical ownership of patient identity and clinical policy across hospitals. Analyze consistency, autonomy, privacy, authority, failure, and evidence.

### Exercise 4

Review a logical architecture containing `Core Manager`, `Shared Database`, `Security Service`, and ten client components. Identify architectural smells and propose a more accountable analysis process without assuming microservices.

### Exercise 5

Construct a logical architecture assurance plan for autonomous medication delivery. Include responsibilities, state, interfaces, fault/trust boundaries, human authority, quality composition, physical allocation, and bounded evidence.

## Answers to the Exercises

### Answer 1

Use Request Authority (identity/authorization), Message Policy (classification, urgency, deadline), Delivery Coordination (message lifecycle, idempotency, route progress), Channel Adaptation (channel-specific translation/failure), Durable Evidence (immutable disposition/provenance), and Operational Escalation (human handoff/recovery). External identity, directory, channel, recipient, and policy authorities appear as required capabilities or actors. State ownership is explicit: Delivery Coordination owns lifecycle state; Durable Evidence owns accepted records; Message Policy owns rule versions.

The mobile app could realize presentation, local evidence collection, and degraded queue pieces; cloud resources could realize several logical components; a local device and cloud might redundantly realize Delivery Coordination; databases store state owned semantically elsewhere; support staff can realize Escalation roles. One component may span deployments and one deployment may host several components. These mappings, supplier choices, trust/fault independence, protocols, scale, and organizational ownership remain trade decisions. Scenario and interface evidence must compare alternatives before selection.

### Answer 2

Under a fully sequential additive bound with no overlap:

\[
T=40+15+55+20+35+25=190\text{ ms}.
\]

If 10% required margin means the architecture bound must not exceed 90% of the 200 ms deadline, allowed consumption is \(0.9\times200=180\) ms. The 190 ms path therefore misses the margin criterion by 10 ms, although it is 10 ms below the raw deadline.

This conclusion assumes compatible worst-case bounds, one occurrence of each interface/queue, no retries, no physical response, synchronized observation, fixed configuration/load, and additive sequential execution. Confirm whether margin applies to deadline or estimated path, whether branches overlap, and whether queue/resource contention is bounded. Options include reallocation, architecture change, stronger evidence, or controlled requirement/margin decision. Local component compliance alone cannot establish end-to-end timing.

### Answer 3

Central ownership provides one patient-identity resolution and policy-version authority, simplifying consistency, audit, and cross-site evidence. It concentrates privacy/trust, availability, jurisdiction, latency, and outage risk; hospitals may lack safe autonomy during partition. Federated ownership keeps data and clinical authority local, supports jurisdiction/site workflow, and can fail independently. It introduces identity matching, policy equivalence/version, consent, conflict, handoff, and cross-site outcome challenges.

A hybrid might use local authoritative clinical records/policy with governed federation identifiers, minimal disclosures, signed policy provenance, and explicit cross-site reconciliation. Define what may be stale, who resolves conflicts, emergency break-glass, partition behavior, revocation, deletion, audit, and patient correction. Logical independence requires physical/organizational evidence. Compare controlled clinical scenarios, privacy/security threats, latency/availability, regulatory authority, and representative workflows. No aggregate score can trade away law or patient safety; affected clinical/privacy authorities decide within jurisdiction.

### Answer 4

`Core Manager` suggests concentrated orchestration and policy without bounded purpose. `Shared Database` hides semantic state ownership and couples ten clients through schema, consistency, availability, privacy, and change. `Security Service` falsely isolates crosscutting authentication/authorization, secure behavior, and evidence. Client count says nothing about interaction criticality. Inspect functions, scenarios, state, interfaces, hazards/threats, changes, and ownership rather than immediately splitting services.

Identify authoritative state/policy domains, durable responsibilities, required/provided contracts, and system-outcome owner. Type dependencies and examine cycles, synchronous failure, shared resources, trust, authority, and change coupling. Propose candidate partitions such as domain policy/state owners, coordination, evidence, and adaptors; compare centralized/federated alternatives against common cases. Security responsibilities remain allocated across components with a possible identity/key service. Map selected logical elements to processes/services/teams later. Verify semantic compatibility, state consistency, degraded behavior, timing, and evidence on chosen realization.

### Answer 5

Logical responsibilities include Prescription/Patient Authority, Clinical Policy, Dose Determination, Delivery Coordination, Physical-Effect Knowledge, Independent Safety Interlock, Clinician Interaction/Authority, Alarm/Escalation, Configuration/Update Authority, and Outcome Evidence. Define authoritative state, uncertainty, provided/required interfaces, modes, timing, units, provenance, errors, and lifecycle for each. Separate command, estimated delivery, and measured physical dose. Trace hazard/threat controls and residual-risk authority.

Analyze fault/trust boundaries, common sensors/power/clocks, stale/contradictory data, partial execution, cybersecurity/privacy, clinician workload, emergency/manual behavior, maintenance, update, and recovery. Compose dose accuracy, latency, availability, and safe degradation across interactions. Map logical components many-to-many to hardware, software, people, facilities, and suppliers; demonstrate claimed independence physically. Evidence combines model/property checks, interface/schema/unit tests, timing/resource analysis, physical metrology, fault injection, cybersecurity/privacy assessment, usability/human-factors work, representative clinical validation, configuration audit, and monitored operation. Each conclusion is bounded by authorized configurations, patients, contexts, faults, and evidence; boxes and local tests do not establish safe medication delivery.
