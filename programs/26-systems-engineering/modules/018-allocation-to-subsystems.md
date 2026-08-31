---
module_id: SYSENG-018
program: Systems Engineering
level: 1
module_number: 18
title: Allocation to Subsystems
status: complete
last_verified: 2026-08-31
---

# Allocation to Subsystems

## One-Page Review

### Governing question

How can a team assign requirements, functions, qualities, budgets, and verification responsibilities to subsystem and enabling-system elements so the selected architecture is feasible and accountable, without losing system-level ownership at interfaces, shared concerns, human work, or emergent behavior?

### Essential definitions

- A **system element** is a member of a system structure that can be considered separately; a **subsystem** is a system element that is itself a system within the chosen hierarchy.
- **Allocation** assigns a requirement or defined contribution role to one or more selected logical or physical elements at the next appropriate architecture level.
- A **direct allocation** assigns an obligation substantially unchanged to an element able to satisfy it; **partitioned allocation** assigns distinct child contributions across elements.
- An **allocation role** states how an element contributes: primary behavior, supporting behavior, data/material provision, constraint, budget share, monitoring, recovery, interface, integration, or evidence.
- A **responsibility boundary** identifies what an element controls and what it assumes from peers, humans, suppliers, external systems, or environment.
- An **allocated baseline** is the controlled set of approved requirements and interfaces assigned to system elements, with rationale, budgets, and verification responsibility.
- A **shared requirement** needs coordinated contributions from multiple elements; it is not satisfied by tagging every element with the parent text.
- An **integration owner** has authority to establish and verify the cross-element behavior needed for a system-level outcome.
- An **enabling system** supports development, production, deployment, training, operation, maintenance, verification, or retirement but may lie outside the delivered end product.
- **Unallocated**, **overallocated**, and **misallocated** requirements respectively lack a needed owner, assign redundant/conflicting ownership, or assign an obligation to an element that cannot control or verify it.

### Central model, mechanism, or theorem

Represent an allocation edge as:

$$
a=\langle requirement,element,role,conditions,inputs,outputs,
interfaces,budget,rationale,authority,verification,status\rangle.
$$

For requirement $r$, allocation coverage requires:

$$
RequiredRoles(r)\subseteq\bigcup_{a\in Alloc(r)}Roles(a),
$$

and element feasibility requires:

$$
\forall e:\ Feasible\left(e,\{a\mid Element(a)=e\},constraints_e\right).
$$

System satisfaction requires more than element satisfaction:

$$
ElementEvidence+InterfaceEvidence+IntegrationEvidence
\xRightarrow{composition\ argument} SystemRequirementEvidence.
$$

The relations structure review; they do not automatically prove correct architecture, complete roles, feasible integration, or system acceptance.

### Critical invariants

- Allocation follows a selected, versioned architecture alternative and records why each element is capable and appropriate.
- Every allocated edge names a contribution role, controlled boundary, interfaces, conditions, rationale, and verification responsibility.
- The original system-level requirement remains owned and verified at its own level; it is not replaced by child allocations.
- Shared qualities and end-to-end behavior have named integration authority and explicit interface/integration requirements.
- Humans, organizations, suppliers, external systems, and enabling systems are modeled without assigning them obligations the project cannot control.
- Budgets preserve system boundary, units, operating profile, margin/reserve, composition assumptions, and coupled change control.
- Allocation considers combined workload, resources, hazards, security, maintainability, support, transition, and retirement—not function alone.
- Organizational team boundaries do not silently become architecture boundaries, and architecture boundaries do not automatically establish accountability.
- Child and element evidence is configuration-controlled and combined with integrated/system evidence before parent acceptance.
- Changes to requirements, architecture, suppliers, interfaces, or evidence trigger bidirectional allocation impact analysis.

### Common failures

Failures include one owner column without contribution semantics; allocating every requirement to software; assigning organization duties to products; copying a shared parent to all subsystems; leaving interfaces to “integration”; distributing numerical budgets equally; ignoring common resources and common-cause failure; selecting an element before comparing architecture alternatives; allocating to a supplier without evidence/change rights; matching architecture to the org chart; verifying each element in isolation; and deleting the system-level requirement after flowdown.

### Compact example

System requirement: during emergency shutdown, the industrial system reaches and reports a defined safe physical state. Allocation may give control logic the authorized transition decision, communications the command/feedback transport, actuators the isolation action, mechanical/energy elements stored-energy release, sensors independent state evidence, the human interface status and reset authorization, and maintenance the bypass/return-to-service process. A safety/integration owner controls timing, common-cause assumptions, interface contracts, fault response, and end-to-end verification. No single subsystem can claim the parent.

### Connections

Retrieve decomposition and coverage arguments from SYSENG-017, quality/testability from SYSENG-016, and source requirements from SYSENG-011–015. Continue to bidirectional traceability and requirement change/conflict. Later logical components, function-to-element allocation, physical architecture, interfaces, integration, configuration baselines, architecture trades, and verification deepen the allocation mechanism.

## Governing Question

Decomposition identifies lower-level obligations. Architecture identifies candidate elements and relationships. Allocation connects them by deciding which elements have which roles in realization and evidence. That decision creates local autonomy, coupling, supplier boundaries, interfaces, budgets, and integration risk. A careless allocation can make every local specification plausible while leaving the system outcome ownerless.

The governing question therefore concerns controllability and composition. Can the assigned element observe and control what the requirement asks? What must it receive and provide? Which peer and environmental assumptions does it rely on? Who owns behavior spanning elements? What evidence can be produced locally, and what must remain system-level? Allocation is an architectural decision with requirements consequences, not clerical tagging.

## Why This Matters

System failures frequently occur at allocation seams. Software is blamed for a sensor-quality issue it cannot observe. A supplier meets an interface syntax but violates timing semantics. Two teams each assume the other preserves audit provenance. A human is assigned “monitoring” without information, time, competence, or authority. Allocation quality determines whether obligations become achievable specifications or institutional ambiguity.

ISO/IEC/IEEE 29148:2018 treats requirement hierarchy, derivation, allocation, and traceability as lifecycle requirements-engineering concerns. NASA's logical-decomposition process iterates functions, performance, behavior, time, data, interfaces, architecture, derived requirements, allocation, conflict resolution, and baselining. SEBoK 2.14 defines allocation as assigning higher-level requirements to next-level architecture elements according to each element's implementation role and emphasizes coupled parameter budgets.

An allocation matrix is useful but incomplete. A mark at row `safe operation`, column `software` says nothing about sensors, actuators, human authority, support, interface assumptions, common cause, or system evidence. Each allocation edge needs semantics, and the whole allocation needs a composition argument.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. decomposition derives lower-level obligations and a coverage argument without necessarily selecting implementation elements;
2. allocation assigns obligations/contributions to selected architecture elements and iterates with decomposition;
3. parent satisfaction requires explicit assumptions, interface behavior, and integration evidence beyond child passes;
4. performance/resource budgets are coupled constraints, not independent targets;
5. requirements need correct subjects, sources, conditions, feasibility, and verification concepts;
6. systems include humans, enabling systems, suppliers, and external dependencies where relevant;
7. architecture alternatives should be compared before allocation is baselined.

As a retrieval test, allocate “protect customer data” to the security subsystem. Ask who collects, transforms, stores, transmits, backs up, exports, supports, deletes, monitors, and recovers data. Protection responsibilities cross every path, while a security element may provide identity, policy, key, or monitoring services. The single allocation is structurally incomplete.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish decomposition, direct/partitioned allocation, function allocation, requirement allocation, responsibility, and organizational assignment;
2. select an allocation level and candidate architecture using requirements and operational evidence;
3. define typed allocation roles, boundaries, interfaces, assumptions, budgets, and evidence responsibilities;
4. allocate functional, performance, resource, quality, constraint, safety, security, and lifecycle obligations;
5. model shared requirements and establish integration authority without copying parent text;
6. include humans, suppliers, external systems, and enabling systems with correct controllability and agreements;
7. analyze combined element feasibility, common cause, coupling, and crosscutting concerns;
8. construct allocation coverage and parent verification composition arguments;
9. govern allocation baselines, variants, supplier boundaries, and change impact;
10. state evidence limits and escalate high-consequence decisions to applicable authority.

## Core Exposition

**Begin from a controlled architecture alternative.** Record the logical/physical view, system boundary, hierarchy level, configuration, decision, and rationale. Candidate elements must be defined by stable responsibility, not current team names. Allocate against more than one plausible architecture during trade studies when the decision remains open; otherwise the first matrix silently selects the design.

**Distinguish what is allocated.** A parent requirement can be directly assigned, partitioned into child requirements, or supported through several typed contributions. Functions can be allocated to elements; performance/resource budgets can be apportioned; qualities and constraints can apply across several elements; verification tasks/evidence can have owners. Do not treat these allocation objects as interchangeable.

**Choose the proper level.** Allocate to the next level with design authority and a controllable, verifiable boundary. Too high leaves implementation ambiguity; too low freezes internals and creates needless management. A service requirement may allocate to an application/service element, while detailed retry behavior belongs lower only after state and interface decisions.

**Define element capability and control.** For each candidate, ask what it can sense, decide, change, store, communicate, and prove; its resource/environment limits; lifecycle owner; and failure modes. An element cannot guarantee data correctness it never observes, a network it does not own, or a human decision. Convert uncontrollable dependencies into interface agreements, assumptions with triggers, or higher-level responsibilities.

**Use typed contribution roles.** Common roles include primary transformation, input/data/material provision, authorization, control, enforcement, monitoring, reporting, recovery, support, evidence production, and integration. One element may carry several roles; one requirement may span many elements. Type edges so reviewers can see missing functions rather than count assignments.

**Retain system ownership.** The parent requirement remains in the system baseline with a system owner and verification concept. Lower-level specifications describe element contributions. Deleting the parent destroys the outcome boundary and makes local evidence appear sufficient. The system authority owns residual gaps, assumptions, and acceptance.

**Create child requirements for element control.** A broad system statement copied into a subsystem specification may be neither controllable nor verifiable. Derive child obligations that state what that element must do/provide under its local boundary while preserving source and contribution rationale. SYSENG-017's coverage argument links them back.

**Make interfaces first-class allocation products.** For every cross-element dependency define provider/consumer, direction, semantics, units, timing, quality, authority, protocol/physical form where justified, modes, capacity, version, failure behavior, recovery, configuration, and verification. Assign each side's obligations and an interface owner. “A sends data to B” is not a contract.

**Assign integration authority.** Shared behavior needs an owner able to reconcile requirements, budgets, interface changes, and end-to-end evidence. The integrator may be a system element, system team, or contractual authority, but must have decision rights and resources. A RACI table can aid governance; it cannot substitute for technical allocation semantics.

**Allocate functions without losing flows.** Use functional flow, state, scenario, and data/material/energy models. Ensure every input has a provider, every output a consumer, every state transition authority, every resource acquisition/release, and every error/recovery path. After grouping functions into elements, create interfaces at every cut edge and analyze added latency, failure, security, and organizational handoff.

**Allocate performance and resources through budgets.** For additive quantities, define allocations and reserve such that the justified composition meets the parent. Track predicted value, required limit, uncertainty, margin, owner, and configuration separately. For latency percentiles, reliability, availability, accuracy, or risk, use architecture-specific models rather than equal division. Shared infrastructure capacity must include combined workload and interference.

**Allocate qualities as scenarios and responsibilities.** Reliability includes prevention, detection, containment, recovery, repair, and evidence across elements. Security/privacy follow assets and flows. Accessibility spans interaction, content, devices, support, and workflow. Maintainability spans diagnostics, access, tools, spares, configuration, documentation, and return-to-service. Tagging one element with the quality name is not allocation.

**Allocate safety/hazard controls by control path.** Identify hazardous states, control actions, sensors, decision logic, actuators, energy/material, human authority, interfaces, diagnostics, and common cause. Assign independence and assurance obligations where justified. Retain system hazard ownership and integrated verification; no component can accept system residual risk alone.

**Allocate human-system work responsibly.** For human roles, define information, perception, decision, action, time, workload, competence, accessibility, authority, error/recovery, and support. For automated elements, define uncertainty, monitoring, override, and safe fallback. Do not allocate to “operator” merely because automation is difficult; validate work in representative conditions.

**Model external and enabling systems.** External identity, payment, network, utility, regulator, responder, supplier, training, test, maintenance, and disposal systems influence requirements but may be outside project authority. Allocate internal responsibilities for interface, monitoring, degraded behavior, evidence, and exit; govern external expectations through agreements and assumptions.

**Handle suppliers and acquisitions.** Flow down exact requirements, interfaces, evidence deliverables, configuration/version, change notification, vulnerability/anomaly reporting, audit/access rights, acceptance, warranty/support, obsolescence, and exit. Supplier certification is inherited evidence within scope, not transfer of system accountability. Avoid allocating obligations the contract does not let the project observe.

**Check combined feasibility per element.** Aggregate all functions, qualities, constraints, budgets, modes, workloads, lifecycle tasks, and verification burdens assigned to each element. Local requirements may conflict or exceed capacity together. Include development and support skills, facilities, schedule, supply, safety, and regulatory evidence—not just runtime resources.

**Check cross-element feasibility.** Analyze timing, capacity, state consistency, data ownership, security/trust, fault containment, startup/shutdown, update compatibility, migration, and recovery across interfaces. A feasible collection of elements can form an infeasible system if their assumptions conflict.

**Challenge allocation with loss and substitution tests.** Remove or degrade one element and walk each parent thread: which required role disappears, who detects the loss, what mode begins, what state/data transfers, and what outcome remains? Then substitute a candidate element with the same advertised function and ask whether interface semantics, assurance, timing, operational support, evidence, and lifecycle rights remain sufficient. These tests reveal hidden responsibilities embedded in a product name, team habit, or supplier relationship. They also identify which characteristics belong in the element/interface specification versus the architecture decision record.

**Consider organizational and ownership boundaries.** Conway effects and contract boundaries shape communication, but do not let an org chart dictate the architecture without trade analysis. If one technical element spans teams, define one accountable design authority. If one team owns several elements, retain interface contracts where independent evolution or assurance needs them.

**Define allocation verification closure.** Each element requirement has a verification owner, method, configuration, and evidence artifact. Interface requirements have both-side and integrated evidence. The parent composition argument states how element, interface, integration, and system evidence combine. Preserve test article/simulator/supplier evidence pedigree and limitations.

**Baseline with unresolved risk visible.** Record unallocated requirements, shared roles without integrator, TBD/TBR budgets, assumptions, external agreements, supplier gaps, rejected allocations, and review decisions. Baseline only for a named commitment and retain open-item owners/deadlines/consequences. A matrix with no blank cells can still be wrong.

**Preserve allocation decision records.** For consequential edges, record alternatives considered, decision criteria, evidence, assumptions, rejected options, reversibility, affected stakeholders, authority, and triggers for reconsideration. The requirement trace answers why an obligation exists; the allocation rationale answers why this element has this role. Keeping both prevents later maintainers from treating current placement as fundamental system truth and supports reallocation during technology refresh, supplier exit, organizational change, or incident learning.

**Align ownership of evidence with independence needs.** The implementing element team may generate detailed verification artifacts, while interface, integration, safety, security, or acceptance authorities review or independently reproduce evidence proportional to consequence. Record who executes, witnesses, reviews, approves, stores, and may invalidate each artifact. “Subsystem verified” without configuration, reviewer, and parent-composition role cannot support a durable allocated baseline.

**Control variants and evolution.** Product variants, market profiles, deployment modes, and supplier substitutions may use different allocation sets. Version allocation edges and budgets by configuration. A change triggers parent, child, interface, architecture, supplier, test, operations, and support impact analysis; rebalance coupled budgets under system authority.

**Use automated checks as bounded triage.** Tools can detect absent requirement, element, role, rationale, verification, or integrator fields. They cannot judge element capability, proper architecture, shared-quality completeness, contract enforceability, or system satisfaction. The executable example reports declared metadata only.

<!-- bijux-verify: {"id":"subsystem-allocation-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"allocations_total=5\nwell_formed_declared=1\nmissing_requirement=AL-002\nmissing_element=AL-003\nmissing_role=AL-004\nmissing_rationale=AL-005\nmissing_verification=AL-003\nshared_without_integrator=AL-004\nallocation_set_ready=false\nevidence=declared_fields_only\n","stderr":""}} -->
```python
allocations = [
    {"id": "AL-001", "requirement": "R-shutdown-command", "element": "control",
     "role": "primary", "rationale": "decides authorized state transition",
     "verification": ["state test"], "shared": False, "integrator": "system-safety"},
    {"id": "AL-002", "requirement": "", "element": "sensors", "role": "evidence-provider",
     "rationale": "reports physical isolation state", "verification": ["interface test"],
     "shared": False, "integrator": "system-safety"},
    {"id": "AL-003", "requirement": "R-safe-state", "element": "", "role": "actuation",
     "rationale": "isolates hazardous energy", "verification": [],
     "shared": False, "integrator": "system-safety"},
    {"id": "AL-004", "requirement": "R-safe-state", "element": "control+actuation",
     "role": "", "rationale": "coordinates end-to-end transition",
     "verification": ["integrated fault test"], "shared": True, "integrator": ""},
    {"id": "AL-005", "requirement": "R-shutdown-status", "element": "human-interface",
     "role": "status-provider", "rationale": "", "verification": ["system demonstration"],
     "shared": False, "integrator": "system-safety"},
]

required = ("requirement", "element", "role", "rationale", "verification")
complete = [a for a in allocations if all(a[k] for k in required) and (not a["shared"] or a["integrator"])]
print(f"allocations_total={len(allocations)}")
print(f"well_formed_declared={len(complete)}")
for field in ("requirement", "element", "role", "rationale", "verification"):
    missing = sorted(a["id"] for a in allocations if not a[field])
    print(f"missing_{field}={','.join(missing)}")
shared_gap = sorted(a["id"] for a in allocations if a["shared"] and not a["integrator"])
print("shared_without_integrator=" + ",".join(shared_gap))
print(f"allocation_set_ready={str(len(complete) == len(allocations)).lower()}")
print("evidence=declared_fields_only")
```

## Definitions and Notation

Let $R$ be requirements, $E$ system elements, $F$ functions, $Q$ quality concerns, $B$ budgets, $I$ interfaces/integration obligations, and $V$ evidence.

Define an allocation relation:

$$
Alloc\subseteq R\times E\times Role.
$$

For element $e$, $Req(e)=\{r\mid\exists role:(r,e,role)\in Alloc\}$. For requirement $r$, $Elements(r)=\{e\mid\exists role:(r,e,role)\in Alloc\}$. These sets express assignment, not satisfaction.

Let $Controls(e,x)$ mean element $e$ can observe or change property $x$ sufficiently for its role. Let $Assumes(e,p)$ record dependency on peer/environment property $p$. An allocation is suspect when the role requires $x$ but neither `Controls` nor a governed interface/assumption supplies it.

An **allocation matrix** is a view of `Alloc`; an **allocated baseline** includes requirement texts, child derivations, architecture identities, interface definitions, budgets, rationale, authority, and verification concepts. A **specification owner** controls an element's obligations; a **system requirement owner** retains parent accountability.

## Mechanisms, Invariants, or Proof Structure

The mechanism has seven passes: select architecture alternative; define elements/boundaries; map requirements/functions/qualities; assign typed roles and budgets; derive child/interface requirements; check local and cross-element feasibility; establish verification closure and baseline. Discovery at any pass can reopen the architecture or parent.

Use an allocation readiness predicate:

$$
Ready(A)=RoleCoverage\land Controllability\land InterfaceClosure
\land ElementFeasibility\land SystemFeasibility\land IntegrationAuthority
\land VerificationClosure.
$$

This is a review structure, not an algorithmic proof. Architecture suitability, controllability, and feasibility require evidence and judgment.

Maintain five invariants. **Parent invariant:** system obligation remains owned at system level. **Role invariant:** every allocation edge states a controllable contribution. **Interface invariant:** every cross-boundary dependency has governed semantics and ownership. **Composition invariant:** shared behavior has integration authority and evidence. **Configuration invariant:** allocation, budgets, suppliers, and evidence refer to the same versioned architecture.

## Alternatives and Trade-Offs

**Centralized versus distributed allocation.** Centralization simplifies authority and consistency but can bottleneck and create a critical dependency. Distribution improves locality/resilience but increases interfaces, reconciliation, and assurance. Compare outcome, failure, evolution, and organization effects.

**Hardware, software, or human allocation.** Hardware can offer deterministic physical enforcement; software offers adaptability; humans offer judgment and recovery. Each brings failure, workload, competence, update, assurance, and lifecycle costs. Hybrid allocations require explicit handoffs.

**Direct versus partitioned requirement allocation.** Direct allocation preserves a self-contained obligation; partitioning exposes element-specific control. Avoid direct copy when the element cannot satisfy the system meaning, and avoid fragmentation when one element truly owns it end to end.

**Dedicated versus shared element.** Dedicated elements improve isolation and tailored assurance; shared services improve reuse and cost but create contention, common cause, governance, and multi-tenant evidence challenges.

**Internal versus supplier element.** Suppliers can provide mature capability and certification; integration, opacity, change, dependency, and exit risk increase. Allocate only with enforceable interface/evidence rights.

**Static versus dynamic allocation.** Some systems shift responsibility by mode, health, location, or load. Dynamic allocation improves resilience but requires authority, state agreement, transfer, observability, and verification for every transition.

## Failure Modes and Misconceptions

1. **“One matrix cell establishes ownership.”** It lacks role, boundary, interface, rationale, and evidence semantics.
2. **“Every requirement must belong to exactly one subsystem.”** Shared and integration requirements can span elements; one authority must still own closure.
3. **“Software can handle it.”** Software cannot directly control unavailable sensing, physics, human authority, or external organizations.
4. **“Allocating the parent means no child is needed.”** Element specifications need controllable, verifiable obligations.
5. **“All elements passed, so the system passed.”** Interfaces, common cause, emergence, and end-to-end outcomes remain.
6. **“Equal budgets are objective.”** They embed unreviewed feasibility, risk, and cost assumptions.
7. **“The supplier owns compliance.”** System integrators retain applicability, configuration, and integration accountability.
8. **“The org chart is the architecture.”** It can conceal technical coupling or institutionalize accidental structure.
9. **“Shared means everyone is responsible.”** Without decision authority, shared often means nobody closes the gap.
10. **“Allocation is permanent.”** Architecture, requirements, evidence, suppliers, and operational learning change.

## Worked Examples

### Example 1

**Situation.** Allocate emergency shutdown. **Reasoning.** Control decides authorized transition; communications carries command/status; actuators isolate; physical elements release energy; sensors provide independent evidence; human interface exposes state/reset; maintenance controls bypass. A safety integrator owns timing, faults, and end-to-end safe-state evidence. **Conclusion.** Typed roles and integration authority replace a vague “controller owns shutdown.”

### Example 2

**Situation.** Allocate a 500 ms response budget. **Reasoning.** Assign measurable contributions to admission, processing, dependencies, transport, presentation, and integration reserve under one workload/boundary. Shared queues and concurrency make local maxima interact. Retain end-to-end verification and coupled rebalance authority. **Conclusion.** Timing allocation is a system model and change-controlled budget, not independent team targets.

### Example 3

**Situation.** Allocate data protection to a security service. **Reasoning.** The service may own identity, policy, keys, or detection; every producer, store, interface, backup, export, support tool, and deletion path owns local controls. Privacy/security integration owns flow coverage and incident evidence. **Conclusion.** Crosscutting quality follows assets and flows, not one box.

### Example 4

**Situation.** Allocate clinical triage between AI and clinician. **Reasoning.** AI provides recommendation, uncertainty, provenance, abstention, and monitoring; clinician retains defined judgment/override; workflow supplies context and escalation; governance owns model/data/change and incident review. Validate workload and information under representative conditions. **Conclusion.** Human/system allocation requires authority and cognitive-work evidence, not “human in the loop.”

### Example 5

**Situation.** Two available services share identity and network. **Reasoning.** Local availability objectives omit shared dependencies, failure detection, degraded authentication, failover state, recovery, and regional common cause. Assign dependency monitoring and system availability integration. **Conclusion.** Shared infrastructure invalidates naive independent subsystem allocation.

### Example 6

**Situation.** Allocate a supplier navigation component. **Reasoning.** Flow down operating domain, input/output semantics, accuracy/uncertainty, timing, faults, configuration, evidence, update/change, vulnerability, support, and exit. System owns fusion, degraded behavior, hazards, and validation. **Conclusion.** Supplier scope is an interface/evidence boundary, not transferred system accountability.

### Example 7

**Situation.** Allocate regulated record retention. **Reasoning.** Applications create/provide provenance; record service stores/retrieves; identity controls access; backup/migration preserves; governance decides holds/disposition; support and audit provide evidence. An information-lifecycle owner reconciles privacy deletion. **Conclusion.** Retention crosses product, data, process, and authority elements.

### Example 8

**Situation.** A platform offers shared deployment capability. **Reasoning.** Platform owns safe primitives, policy enforcement, evidence, quotas, and support; application teams own workload configuration and service outcome; security/operations own cross-platform governance. Define degraded/exit behavior and tenant interference. **Conclusion.** Shared services need explicit consumer/provider responsibilities and system-level outcome owners.

### Example 9

**Situation.** Allocate mass and power for a field robot. **Reasoning.** Give each element a versioned profile-specific budget, uncertainty, and owner; retain harness/conversion/integration items and separate reserve. Analyze simultaneous peaks, thermal coupling, battery aging, payload variants, and emergency mode. **Conclusion.** Physical budgets require configuration and operating-profile coherence.

### Example 10

**Situation.** Allocate rail-crossing safety. **Reasoning.** Trackside sensing, signaling, barriers, warning devices, control center, network/power, maintainer, and responders have distinct roles. System safety owns train/road state, common cause, bypass, degraded mode, cyber protection, and integrated physical tests. **Conclusion.** Public-safety acceptance cannot be reduced to component allocation or internal review.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) helps align responsibility boundaries with domain ownership without equating code packages to system elements.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) compares candidate structures, quality tradeoffs, and composition before baselining allocations.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) allocates data ownership, transformations, quality, provenance, retention, and evidence across pipelines and platforms.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) maintains crosscutting asset/flow protection and assurance across element boundaries.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) formalizes provider/consumer interface obligations, failures, state, timing, and compatibility.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) governs shared capability allocations and consumer responsibilities across organizational boundaries.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, 2018. Consulted 2026-08-31.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, 2023. Consulted 2026-08-31.
3. NASA. [Logical Decomposition](https://www.nasa.gov/reference/4-3-logical-decomposition/), requirement and function allocation guidance. Consulted 2026-08-31.
4. NASA. [System Design Processes](https://www.nasa.gov/reference/4-0-system-design-processes/), recursive architecture and allocation guidance. Consulted 2026-08-31.
5. NASA Software Engineering Handbook. [Software Requirements](https://swehb.nasa.gov/spaces/7150/pages/16449651/SWE-050%2B-%2BSoftware%2BRequirements), system-to-software flowdown and allocation guidance. Consulted 2026-08-31.
6. SEBoK Editorial Board. [System Requirements Definition](https://sebokwiki.org/wiki/System_Requirements_Definition), allocation, child requirements, and budgeting, version 2.14. Consulted 2026-08-31.
7. SEBoK Editorial Board. [Physical Architecture](https://sebokwiki.org/wiki/Physical_Architecture), function-to-element allocation and interface considerations, version 2.14. Consulted 2026-08-31.
8. SEBoK Editorial Board. [Configuration Baselines](https://sebokwiki.org/wiki/Configuration_Baselines), allocated baseline discussion, version 2.14. Consulted 2026-08-31.

## Exercises

### Exercise 1

Distinguish allocation of requirements, functions, budgets, verification responsibility, and organizational work using a public-warning system. Identify what remains system-owned.

### Exercise 2

Build an allocation matrix with typed roles for account revocation across identity, application, session/cache, notification, audit, support, and governance elements. Add interfaces and integration authority.

### Exercise 3

Compare hardware, software, and human allocations for collision avoidance in an industrial vehicle. Analyze sensing, decision, action, workload, failure, safety, maintenance, and evidence.

### Exercise 4

Evaluate internal versus supplier allocation of a payment-fraud capability. Cover data, model/rules, latency, privacy, recourse, monitoring, change, evidence, outages, and exit.

### Exercise 5

Develop and review allocations for a home medical-monitoring capability. Include patient/caregiver, device, mobile/edge, cloud, clinician, support, supplier, emergency services, data, security/privacy, network/power loss, maintenance, and regulatory evidence.

## Answers to the Exercises

### Answer 1

Requirement allocation assigns controlled obligations or contribution roles to elements; function allocation assigns transformations such as authorize, compose, distribute, display, acknowledge, and recover; budgets assign coupled shares of timing, capacity, power, or another parameter; verification allocation assigns who produces which evidence; organizational assignment identifies teams/contracts but does not define the technical boundary by itself. A warning service may own channel dispatch, a carrier the governed delivery interface, a device presentation, an operator authorization, and support recovery.

System ownership remains for affected-population outcome, authority model, end-to-end semantics/timing, accessibility across channels, common/dependency failure, updates/cancellation, audit closure, system security/privacy, integrated validation, and residual risk. Each allocation edge names role, conditions, input/output, interface, rationale, evidence, and authority. The system requirement remains in the baseline even after child specifications exist.

### Answer 2

Identity has primary role for credential/identity-state revocation and status. Applications enforce current authorization for new actions. Session/cache elements invalidate or reject existing/session-cached authority under defined propagation semantics. Notification provides governed user/owner status without leaking sensitive detail. Audit records source, authority, time, affected identity/credentials/sessions, results, and exceptions. Support handles recourse and unresolved states under authorized controls; governance owns policy, legal/privacy interpretation, emergency override, and acceptance.

Interfaces define revocation identity/version, effective time, ordering, acknowledgment, stale/duplicate behavior, failure/timeout, reconciliation, and observability. A named revocation integrator owns end-to-end completion, budgets, conflict, and evidence. Verification covers each child plus interface traces, cached/offline sessions, concurrency, restart, partial outage, repeated revocation, reauthorization, notification failure, audit reconciliation, and end-to-end prevention of post-effective unauthorized action. No cell alone satisfies the parent.

### Answer 3

Hardware allocation can provide proximity sensing, interlocks, independent braking, and deterministic physical enforcement, but faces sensor coverage, wear, calibration, environmental, and common-cause limits. Software can fuse inputs, predict paths, adapt speed, and coordinate modes, but relies on data/timing/configuration and needs safe failure/update behavior. Humans contribute situational judgment and recovery but have perception, reaction, fatigue, workload, training, visibility, and authority limits.

A defensible hybrid assigns sensing with diagnostics and coverage evidence; bounded decision/control with uncertainty and minimum-risk behavior; independent actuation/interlock where hazard analysis justifies it; human status, override, emergency action, and recovery under representative workload; and maintenance calibration/bypass/return-to-service. Safety integration owns hazard controls, latency, mode transitions, interfaces, common cause, and physical collision outcome. Verification combines analysis, inspection, simulation, fault injection, environmental and integrated tests, and human-factors evaluation. Safety authority, not a subsystem owner, accepts residual risk.

### Answer 4

Internal allocation offers data/control transparency, tailored policy, fast incident response, and direct change governance but requires expertise, model/rule maintenance, monitoring, assurance, and scale. A supplier may offer broader signals and mature operations but creates data-transfer/privacy, opacity, latency, availability, lock-in, change, dispute, audit, and exit risks. Compare outcomes and total lifecycle obligations, not purchase price alone.

Typed roles cover transaction/context provision; detection/scoring with uncertainty; policy/decision authority; customer challenge/recourse; monitoring and subgroup/error analysis; records; privacy/security; incident/change notification; and degraded/manual behavior. Contract interfaces define semantics, freshness, decision deadline, errors, version, evidence, data purpose/retention, audit rights, material change, outages, and termination/export/deletion. The payment organization retains wrongful-block, fraud-loss, legal, fairness, and customer outcome ownership. Validate with representative data/workflows and do not infer acceptability from supplier metrics or certification.

### Answer 5

The home device senses and presents local state, supports safe local operation, records provenance, and provides defined degraded/emergency behavior. Mobile/edge may relay, cache, authenticate, and present status but cannot be assumed present. Cloud ingests, validates, stores, trends, routes alerts, monitors, and supports configuration under declared boundaries. Clinicians interpret clinical context and decide interventions; patient/caregiver roles include consent, setup, observation, response, and recourse with accessibility/workload constraints. Support distinguishes technical and clinical triage; suppliers provide components, evidence, change/vulnerability notification, and lifecycle support. Emergency services receive only governed handoff information and remain external authorities.

Interface/integration allocations cover identity/time, data quality/uncertainty, alarm state/acknowledgment/escalation, network/power loss, buffering/reconciliation, privacy/security, updates/rollback, calibration, maintenance, incident evidence, and retirement. A clinical-safety/system integrator owns end-to-end outcome, hazard controls, common cause, workload, and verification composition. Evidence combines element tests, interface/fault tests, cybersecurity/privacy review, human-factors/accessibility studies, representative home/clinical scenarios, maintenance demonstrations, supplier evidence, and system validation. Internal allocation cannot establish clinical benefit, informed consent, regulatory conformity, or acceptable residual risk; patient/caregiver, clinical, safety, human-factors, privacy/security, quality, maintenance, supplier, emergency, and applicable regulatory authorities must review. No external review is claimed.
