---
module_id: SYSENG-022
program: Systems Engineering
level: 1
module_number: 22
title: Functional Decomposition
status: complete
last_verified: 2026-08-31
---

# Functional Decomposition

## One-Page Review

### Governing question

How can a team refine a parent function into a coherent set of child functions that collectively preserves the parent’s purpose, boundary transformation, modes, performance, failures, and evidence obligations—without mistaking a hierarchy for behavior, splitting words instead of engineering transformations, or prematurely mirroring the physical design?

### Essential definitions

- **Functional decomposition** examines a function to identify the subfunctions, relationships, and interfaces necessary to accomplish it.
- A **parent function** is the transformation being refined; a **child/subfunction** is a lower-abstraction transformation that contributes to the parent.
- A **decomposition relation** states how a child contributes and whether children are all required, alternatives, conditional, repeated, or optional within a named scope.
- An **AND decomposition** requires all applicable children for parent completion; an **OR/XOR decomposition** represents alternatives whose selection and exclusivity semantics must be explicit.
- A **leaf function** is a function not further decomposed in the current viewpoint because it is sufficiently understood for the next decision—not because it is intrinsically atomic.
- **Boundary preservation** requires the composed child network to accept, transform, and emit the parent’s external flows and effects under the parent’s admissible conditions.
- **Behavioral composition** explains ordering, concurrency, synchronization, feedback, state, and modes among children; a tree alone states containment, not execution.
- A **derived function** becomes necessary through analysis, architecture, risk controls, interfaces, or lifecycle needs rather than direct wording in a parent requirement.
- **Functional cohesion** asks whether a child owns a clear transformation; **coupling** describes dependencies among functions through flows, shared state, timing, resources, or control.
- A **stopping rule** defines when refinement is sufficient for allocation, interface definition, estimation, risk analysis, and verification at the current lifecycle stage.

### Central model, mechanism, or theorem

Let parent contract \(P\) have allowed boundary behavior \(\mathcal{B}_P\). Let child network \(N=\langle C,L,\Sigma\rangle\) contain child contracts \(C\), typed internal flows \(L\), and composition semantics \(\Sigma\) for state, order, concurrency, modes, and failures. Hide internal flows with projection \(\pi_{\partial P}\). A refinement obligation is:

\[
\pi_{\partial P}(Behavior(N,H))\subseteq \mathcal{B}_P
\]

under stated assumptions \(H\), while every required parent outcome remains reachable for the specified operational cases.

Structural coverage is necessary but insufficient:

\[
Covered(P)=BoundaryFlows\land Scenarios\land Modes\land
Performance\land Failures\land Lifecycle\land Trace.
\]

Each predicate needs semantic evidence. Box count, child links, or an executable graph check cannot prove behavioral preservation.

### Critical invariants

- The parent function, system boundary, viewpoint, configuration, assumptions, and source obligations are stable during a decomposition review.
- Children use action-object intent and have typed input/output contracts, state, controls, resources, modes, performance, and failure semantics where relevant.
- Every child traces to parent contribution, derived rationale, hazard/threat control, interface, or lifecycle obligation; unjustified children are reviewed as possible design excess.
- Every parent input/output is consumed, produced, forwarded, stored, or deliberately transformed by the child network.
- Internal flows have legitimate producers and consumers; they are not invented arrows with ambiguous semantics.
- A decomposition hierarchy is paired with behavioral views that express order, choice, concurrency, feedback, and state.
- AND, OR, XOR, optional, repeated, and conditional relations are distinguished; “contains” is not a universal composition rule.
- Parent timing, accuracy, capacity, reliability, safety, security, and resource constraints are allocated or preserved with composition rationale and margin.
- Nominal, alternate, degraded, emergency, startup, shutdown, maintenance, update, recovery, and disposal cases are considered according to scope.
- Functional and physical breakdowns remain distinguishable; alternative child networks may map many-to-many to later system elements.
- Refinement stops by decision readiness and risk, not arbitrary depth or a fixed number of children.
- Review conclusions remain bounded by model fidelity, scenario coverage, evidence, configuration, and competent authority.

### Common failures

Failures include decomposing “monitor and control temperature” into the nouns “monitor” and “control” without defining the feedback loop; copying the organizational chart; using software services or hardware parts as child functions; forcing every decomposition into AND semantics; omitting internal conversion, storage, arbitration, synchronization, or diagnostics; losing a parent output; adding children with no source; distributing a parent deadline equally without path reasoning; decomposing only nominal operation; creating one giant child plus trivial helpers; refining until functions become implementation steps; stopping while interfaces remain untestable; and calling a graph structurally complete when semantics, modes, failures, or end-to-end behavior are absent.

### Compact example

Parent `deliver authenticated emergency message` accepts an authorized request and message, then produces timely, intelligible presentation and disposition evidence. A useful child network receives and validates the request, authenticates authority, assigns identity/priority, protects content, selects routes, queues durably, transmits, validates acknowledgement, reconciles duplicates, escalates deadlines, presents to recipients, and records disposition. It specifies nominal, delayed, duplicate, corrupted, and unavailable-network behavior. Children collectively preserve security and timing; neither “send packet” nor a hierarchy alone does. Alternative centralized and federated routing networks remain candidates until trade evidence supports allocation.

### Connections

This module refines the function-contract foundation of SYSENG-021 using requirements decomposition, allocation, traceability, and change governance from SYSENG-011–020. Subsequent modules add functional flow, state and mode analysis, interfaces, logical architecture, physical allocation, trade studies, verification, safety, security, and configuration evidence.

## Governing Question

A high-level function is intentionally compact. “Provide safe transportation” or “maintain payload environment” names an outcome-generating transformation but cannot yet expose every interface, risk, verification point, or design choice. Refinement is needed so teams can understand behavior and later allocate work. Yet decomposition can destroy meaning: a parent becomes a checklist of locally plausible children whose combined behavior does not reproduce its boundary contract.

The governing question therefore concerns justified composition, not tree drawing. A good decomposition explains why each child exists, how children cooperate, which alternatives were considered, and why the network preserves the parent across relevant states and failures. It provides enough detail for the next engineering decision while retaining implementation freedom.

## Why This Matters

Architecture defects often begin as decomposition defects. Missing arbitration creates conflicting commands. An omitted time-synchronization function corrupts sensor fusion. A parent availability target is allocated to components without common-cause or recovery reasoning. A human receives an unexamined “handle exception” child. Teams later discover these defects during integration, when organization, contracts, and physical interfaces already reflect the flawed structure.

NASA’s current Logical Decomposition guidance calls functional analysis recursive and iterative, describes functions by inputs, outputs, failure modes, consequences, and interfaces, and notes that alternative decompositions are expected. Its handbook glossary defines functional decomposition as examining a function to identify necessary subfunctions and functional relationships/interfaces. ISO/IEC/IEEE 15288:2023 remains the current published system lifecycle process standard and explicitly does not prescribe one methodology or modeling technique. SEBoK 2.14 warns that a static functional hierarchy alone does not express input/output exchange effectively and recommends cycles of analysis and synthesis coordinated with scenarios and behavioral views.

Good decomposition also makes uncertainty visible. If reviewers cannot tell whether a child is necessary, whether two children are alternatives, or how a derived function traces to source intent, the architecture is not ready to baseline. That discovery is valuable: it identifies a decision or evidence gap before it hardens into implementation.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. functions are purposeful transformations with typed inputs, outputs, controls, resources, state, environment, performance, and failure behavior;
2. stakeholder outcomes and operational scenarios define the context in which functional behavior matters;
3. requirements decomposition needs contribution and coverage rationale, not textual splitting;
4. many-to-many allocation does not prove that allocated elements compose to meet a parent obligation;
5. traceability links sources, functions, interfaces, realization, and evidence through explicit rationale;
6. baselines and changes are configuration-specific;
7. functional architecture differs from physical architecture even when feasibility knowledge informs both;
8. executable structural checks are bounded observations rather than semantic or safety proofs.

As a retrieval test, inspect a decomposition of `protect account` into `login`, `database`, and `email`. `Database` is a component, `login` covers only one interaction, and `email` is a mechanism. Missing transformations may include establish identity, authorize action, protect credentials, manage session, detect abuse, recover access, notify securely, audit, revoke, and dispose data. The original list does not preserve the parent contract.

## Learning Objectives

After completing this module, you should be able to:

1. frame a parent function with exact boundary contract, source trace, viewpoint, modes, assumptions, and risks;
2. discover child functions from scenarios, flows, states, failures, lifecycle cases, and enabling needs;
3. distinguish functional containment from sequence, data flow, control flow, allocation, and physical composition;
4. specify AND, OR/XOR, optional, conditional, and iterative decomposition semantics;
5. construct parent-child contribution and coverage arguments;
6. preserve boundary inputs, outputs, performance, quality, invariants, and failures through refinement;
7. identify derived, crosscutting, enabling, human, and lifecycle functions without hiding design choices;
8. compare alternative decompositions using cohesion, coupling, observability, risk, and lifecycle trade-offs;
9. apply decision-based stopping rules and avoid over- or under-decomposition;
10. review a high-consequence child network with bounded executable and empirical evidence.

## Core Exposition

**Freeze the review frame, not the design.** Identify parent ID/version, source requirements and needs, boundary, viewpoint, operational configurations, modes, environment, assumptions, risks, and expected evidence. The parent can change through control, but a review cannot assess preservation against a moving or unnamed target.

**Restate the parent contract.** Record purpose, typed boundary inputs/outputs, preconditions, triggers, state, controls, enabling resources, performance, quality, postconditions, exceptions, and failure behavior. Separate what is mandatory from what remains a design degree of freedom. If the parent is ambiguous, resolve or explicitly carry the uncertainty before inventing children.

**Use scenarios to discover behavior.** Walk nominal, alternate, degraded, emergency, maintenance, startup, shutdown, update, recovery, and retirement scenarios. Convert meaningful steps into candidate action-object functions, but do not assume every narrative step deserves a permanent child. Scenarios reveal order and actors; cross-scenario synthesis reveals reusable transformations.

**Follow transformations and flows.** For every parent input, ask what must validate, transform, store, route, combine, or reject it before an output can emerge. Trace matter, energy, data, information, control, resources, and unintended effects separately. Internal flows reveal conversion, buffering, synchronization, estimation, arbitration, or feedback functions that a verb-only breakdown misses.

**Use state and mode analysis.** Ask which functions establish, observe, change, persist, and recover state. A child may be active only in one mode or may enforce an invariant across all modes. Define guards and ownership rather than duplicating nominal children into disconnected mode trees. Transitions can require functions such as prepare, verify readiness, isolate, reconcile, or restore.

**Use failure and misuse analysis.** For the parent and candidate children, examine omission, commission, early/late, wrong value, wrong destination, stale/duplicate, partial, unauthorized, unavailable resource, and contradictory inputs. Derive detection, containment, fallback, safe-state, recovery, evidence, and operator-support functions when justified. Label the source analysis; do not pretend the parent wording explicitly required every derived control.

**Include enabling and lifecycle behavior.** Calibration, configuration, authentication, key management, time synchronization, monitoring, diagnosis, maintenance, software/data update, backup, training, provisioning, manufacturing support, deployment, and disposal can be necessary for sustained parent behavior. Review whether they belong within the parent boundary, another functional branch, or an enabling system.

**Synthesize children at coherent abstraction.** Combine fragments that own one intelligible transformation and separate children that have distinct outcomes, state, authority, timing, failure semantics, or allocation alternatives. Siblings should usually be at comparable decision granularity. One child that restates the parent beside several trivial bookkeeping steps indicates weak synthesis.

**Name contribution semantics.** `C1 contributes-to P` is incomplete unless the edge explains the contribution, applicable cases, and companions. Record whether all children are jointly necessary, alternatives provide the same sub-outcome, a child is conditional on a mode, or repetition continues until a condition. A tree renderer may show one shape even when composition semantics differ.

**Model AND decomposition.** In an AND refinement, all applicable children and their interactions are needed. “All” does not imply sequential order; children can execute concurrently or conditionally within the parent. Define completion conditions and failure propagation. Missing one child may make the parent unreachable, but redundancy can allow alternative satisfaction paths.

**Model alternatives explicitly.** OR means one or more alternatives may execute; XOR means exactly one in the stated decision scope. Identify selector, selection authority, criteria, fallback, and configuration. Architecture candidates should usually live as controlled alternatives rather than simultaneous mandatory children. Do not blend incompatible alternatives into a fictitious average design.

**Represent optional and repeated behavior.** “Optional” must name the condition and show that parent obligations still hold when absent. Iterative functions define termination, progress, timeout, maximum attempts, accumulated state, and failure disposition. A retry loop without idempotency or resource bounds can violate the parent even if each child appears valid.

**Pair hierarchy with behavior.** A functional hierarchy answers what subfunctions are contained. Activity, sequence, state, data/energy/material flow, timing, control, and scenario views explain how they interact. Maintain semantic consistency among views. Never infer temporal order from indentation or left-to-right placement unless the notation defines it.

**Preserve boundary flows.** Construct a boundary-accounting table. For each parent input, name child consumer, transformation, storage, or forwarded output. For each parent output/effect, identify producing path. Check new internal flows for sources and consumers. A child network that creates a required external input not present at the parent boundary has derived a dependency that must be authorized.

**Preserve state and invariants.** Map parent pre-state to child initialization and guards; map child post-state to parent postconditions. Identify shared-state ownership and synchronization. Show that invariants such as “never issue motion while access is open” hold during internal transitions, not only at the final state.

**Compose performance.** End-to-end latency may include sequential execution, communication, queues, retries, synchronization, and physical response. Throughput can be limited by bottlenecks or contention. Accuracy and reliability often compose nonlinearly. Allocate budgets with assumptions, covariance/common-cause considerations, margin, and authority; equal division is rarely a rationale.

**Preserve failure obligations.** Map every parent failure and degraded outcome to child detection, containment, response, recovery, and evidence. Analyze new internal failure modes and interactions created by refinement. A network can meet nominal output yet increase unsafe behavior through partial execution, stale state, or inconsistent recovery.

**Trace children and derived rationale.** Each child has an upward path to parent contribution, a hazard/threat/interface/lifecycle source, or an approved derived-function decision. A child can serve multiple parents; a parent can need multiple networks across modes. Preserve many-to-many relations rather than forcing one owner or duplicating functions until they diverge.

**Avoid premature physical mirroring.** `sense temperature`, `estimate thermal state`, and `determine heat-transfer command` are functional. `thermistor`, `controller service`, and `compressor` are physical/logical solution elements. Feasibility constraints may require candidate mechanisms, but label them in alternative architecture and allocation views rather than renaming functions after components.

**Explore alternatives.** Vary centralization, distribution, sequence, feedback, redundancy, buffering, human participation, and degraded strategy. An alternative decomposition should preserve the same parent boundary so comparisons are meaningful. If one changes the parent outcome, treat it as a requirements change rather than an architecture trade.

**Evaluate cohesion and coupling.** High cohesion gives a child a clear transformation, state, authority, and evidence boundary. Coupling arises through data, matter, energy, control, timing, shared resources, shared state, failure propagation, and organizational coordination. Low coupling is not absolute virtue: closed-loop control needs deliberate coupling. Seek explicit, stable, verifiable dependencies.

**Evaluate observability and controllability.** Can verification stimulate relevant child and parent conditions and observe required effects? Are diagnostics authentic and independent enough to locate failure? Adding a test point can improve evidence but also change security, mass, cost, or behavior. Do not optimize testability while losing the parent outcome.

**Choose a stopping rule.** Stop refining a branch when its contract is clear enough for the next allocation/design decision; interfaces and failures are defined; estimates and risks are credible; verification can be planned; ownership is possible; and further refinement would mainly encode a chosen implementation. Continue when a child remains ambiguous, crosses incompatible authorities, hides major state, bundles independent risks, or cannot be verified.

**Use recursive analysis and synthesis.** Decompose downward, then recombine upward. Ask whether the assembled children still explain the parent; revise both child grouping and sometimes the controlled parent/requirements when new knowledge reveals infeasibility. Decomposition is not one-way derivation. Baseline only when internal consistency and decision readiness meet declared criteria.

**Review structural completeness mechanically.** Tools can find missing parent/child IDs, duplicate children, uncovered declared boundary flows, unjustified children, cycles prohibited by the hierarchy, and missing attributes. They cannot decide whether children are semantically necessary, behaviorally sufficient, or safe.

The following checker evaluates five declared child records against a small policy. It is intentionally not a refinement proof.

<!-- bijux-verify: {"id":"functional-decomposition-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"children_total=5\nwell_formed_declared=1\nmissing_contribution=C-002\nmissing_inputs=C-003\nmissing_outputs=C-004\nmissing_modes=C-005\nunresolved=C-002,C-003,C-004,C-005\nevidence=declared_fields_only\n","stderr":""}} -->
```python
children = [
    {"id": "C-001", "contribution": "validate request", "inputs": ["request"],
     "outputs": ["validated request"], "modes": ["nominal", "degraded"]},
    {"id": "C-002", "contribution": "", "inputs": ["validated request"],
     "outputs": ["priority"], "modes": ["nominal"]},
    {"id": "C-003", "contribution": "protect content", "inputs": [],
     "outputs": ["protected message"], "modes": ["nominal"]},
    {"id": "C-004", "contribution": "transmit message", "inputs": ["protected message"],
     "outputs": [], "modes": ["nominal", "degraded"]},
    {"id": "C-005", "contribution": "record disposition", "inputs": ["acknowledgement"],
     "outputs": ["evidence"], "modes": []},
]

required = ("contribution", "inputs", "outputs", "modes")
valid = [child for child in children if all(child[field] for field in required)]
print(f"children_total={len(children)}")
print(f"well_formed_declared={len(valid)}")
for field in required:
    print(f"missing_{field}=" + ",".join(child["id"] for child in children if not child[field]))
print("unresolved=" + ",".join(child["id"] for child in children if child not in valid))
print("evidence=declared_fields_only")
```

Even C-001 may be semantically wrong, and the checker cannot determine boundary preservation, ordering, failure coverage, or whether any child is missing.

## Definitions and Notation

Let a decomposition be \(D(P)=\langle C,L,\Sigma,R,A\rangle\): parent \(P\), child set \(C\), internal typed flows \(L\), composition semantics \(\Sigma\), contribution rationales \(R\), and assumptions/applicability \(A\). Define boundary input and output port sets \(I_P,O_P\). A structural accounting predicate may require:

\[
\forall i\in I_P:\ Consumer(i)\lor Forward(i),
\]

\[
\forall o\in O_P:\ ProducerPath(o),
\]

plus source/target existence for every \(l\in L\). These are necessary declarations, not proof of correct transformations.

Let \(Scenarios_P\) be required scenario/mode cases and \(Paths_N(s)\) the admissible child behaviors for case \(s\). A coverage obligation is:

\[
\forall s\in Scenarios_P:\exists p\in Paths_N(s):
ObservedBoundary(p)\models Contract_P(s).
\]

Evidence must justify the model, reachability, timing, uncertainty, and observation relation. One successful path does not prove absence of forbidden paths, so safety/security invariants require separate universal or risk-bounded analysis where applicable.

Decomposition depth \(d\) is not a maturity measure. Define a decision-readiness vector \(Q(f)\) over contract clarity, interface definition, risk, estimability, allocability, and verifiability. A branch stops when policy thresholds are met for the intended decision and consequence; the thresholds and evidence are project-specific.

## Mechanisms, Invariants, or Proof Structure

The practical mechanism is a preservation loop:

1. **Frame parent:** freeze version, boundary, cases, source obligations, assumptions, risks, and evidence goal.
2. **Discover children:** use scenarios, flows, state/modes, failures, controls, lifecycle, humans, and enabling needs.
3. **Synthesize structure:** group coherent transformations, specify AND/alternative/conditional/repeated semantics, and retain candidate networks.
4. **Connect behavior:** type flows and model sequence, concurrency, feedback, state, timing, resources, and failure propagation.
5. **Recompose upward:** account for boundary flows and show how child behavior, performance, and evidence support the parent contract.
6. **Challenge:** search for missing, excessive, duplicated, premature, unobservable, tightly coupled, and high-consequence behavior.
7. **Stop or iterate:** apply decision-readiness rules, record rationale and limitations, baseline when justified, and reopen after change or new evidence.

This is an assurance argument, not a theorem that any finite review produces complete architecture. Formal refinement can prove properties within a formal semantics; tests can observe configurations; analyses can estimate behavior. None automatically covers omitted environment, incorrect assumptions, human adaptation, supplier opacity, or unknown failure interactions.

## Alternatives and Trade-Offs

**Top-down decomposition** protects parent intent and boundary but can overlook realization knowledge. **Bottom-up synthesis** finds reusable or feasible functions but can preserve accidental design. Alternate between them and trace every imported constraint.

**Functional trees** communicate hierarchy and ownership simply. They obscure many-to-many contribution, alternatives, feedback, and temporal behavior. **Functional graphs/models** express richer relationships but require precise semantics and controlled views. Generate a tree as one view rather than making it the sole truth.

**Scenario-first decomposition** grounds behavior in use and modes but may duplicate functions across scenarios. **Flow-first decomposition** exposes transformations/interfaces but can underrepresent human goals and state. **Failure-first decomposition** strengthens resilience but can dominate nominal purpose. Synthesize across all three.

**Deep decomposition** can improve estimation, allocation, and verification but increases interfaces, governance, and false precision. **Shallow decomposition** preserves flexibility but can hide risk and produce unmanageable allocations. Stop at decision-relevant clarity.

**One canonical decomposition** simplifies baselines. **Multiple candidate decompositions** preserve alternatives and reveal trade space but cost analysis effort. Carry multiple candidates only while their decision value exceeds maintenance burden.

**Formal refinement** supports rigorous consistency and property checking but is bounded by semantics and model fidelity. **Structured review** accommodates human, physical, and organizational knowledge but is less mechanically exhaustive. Combine proportional to consequence.

## Failure Modes and Misconceptions

- **“The hierarchy is the behavior.”** Containment does not define sequence, concurrency, choice, state, or feedback.
- **“All children are required.”** AND semantics must be declared; some children are alternatives, conditional, optional, or repeated.
- **“Leaf means atomic.”** It means sufficiently refined for this viewpoint and decision.
- **“Each child maps to one component.”** Functional-to-physical allocation is commonly many-to-many.
- **“Every derived function is gold plating.”** Some are necessary for safety, interfaces, lifecycle, or feasibility; record rationale and authority.
- **“Every box has a parent, so coverage is complete.”** Boundary flows, scenarios, modes, performance, failures, and semantics may still be missing.
- **“Equal budget allocation is neutral.”** It encodes a design decision and may ignore path structure, sensitivity, and feasibility.
- **“More levels mean maturity.”** Depth can encode premature implementation while core behavior remains unresolved.
- **“No cycles are allowed.”** Hierarchical containment should be acyclic, while behavioral feedback may be essential.
- **“Executable checks validate the decomposition.”** They validate encoded structural predicates only.

## Worked Examples

### Example 1

**Cold-chain control.** Parent `maintain payload thermal condition` refines into sense state, estimate condition, determine action, transfer heat, circulate medium, verify response, record evidence, and enter degraded operation. Boundary accounting distinguishes sensor information, electrical energy, heat flow, and payload state. Alternatives use active cooling or thermal storage. Chamber evidence supports named loads/configurations, not every packing arrangement; allocation remains open.

### Example 2

**Flood warning.** `provide timely flood warning` decomposes into acquire observations, validate provenance, estimate water state, forecast threshold crossing, assess uncertainty, determine warning, authorize issuance, disseminate, confirm reach, and update/cancel. Human authority and public communication are functional, not afterthoughts. Historical replay bounds known events; it cannot prove performance under unprecedented weather or communication loss.

### Example 3

**Aircraft braking.** `decelerate aircraft safely` needs interpret demand, estimate ground state, allocate braking, command actuators, generate forces, prevent skid, monitor effect, detect failure, and provide alternate/emergency response. A static tree misses the feedback loop. Safety conclusions require dynamic, hardware, human, and certification evidence beyond functional preservation.

### Example 4

**Secure account recovery.** Children establish claimant evidence, assess risk, authorize recovery, protect channel, change credentials, revoke sessions, notify independently, audit, and handle dispute. Email and SMS are candidate mechanisms, not child identity. Adversarial analysis exposes attacker-controlled contact data. Tests support specified attacks and configurations, not universal identity assurance.

### Example 5

**Water delivery.** Parent `deliver potable water` refines source acceptance, treatment, quality verification, storage, pressure control, distribution, contamination isolation, consumer notification, and residual handling. Mass balance reveals leakage/storage; regulatory evidence constrains quality. A treatment function alone cannot cover network recontamination or outage behavior.

### Example 6

**Warehouse fulfillment.** Receive order, validate inventory, reserve items, plan pick, retrieve, verify identity/quantity, pack, route, hand over, reconcile exceptions, and update state. Concurrent orders create shared-state and reservation behavior. A software service map is one allocation, not the functional decomposition. Load tests bound declared demand and data, not holiday disruption or human adaptation.

### Example 7

**Satellite survival.** `preserve spacecraft during safe mode` decomposes detect anomaly, establish safe state, prioritize loads, orient for energy/thermal needs, maintain communication opportunity, monitor resources, recover conditionally, and retain evidence. Some children execute concurrently; recovery is conditional. Simulations depend on failure set and environment assumptions, so mission assurance remains bounded.

### Example 8

**Clinical triage.** Acquire patient information, validate identity/provenance, detect immediate danger, assess acuity, quantify uncertainty, route care, communicate rationale, monitor waiting state, escalate deterioration, and record outcome. “AI classifier” improperly combines mechanism and several functions. Clinical validation must cover representative populations/workflows and cannot infer safety solely from retrospective accuracy.

### Example 9

**Data deletion.** `remove personal data when authorized` refines authenticate request, resolve subject and scope, locate replicas/derivatives, apply holds, authorize, delete or irreversibly transform, propagate action, verify outcomes, report exceptions, retain permissible evidence, and expire backups according to policy. A database DELETE is insufficient. Proof remains bounded by lineage and systems actually discovered.

### Example 10

**Autonomous shuttle door operation.** Interpret stop/mode, detect boarding context, authorize motion, warn, command, move, sense obstruction, limit force, reverse/stop, confirm closure, and record anomalies. Accessibility and emergency cases change conditions but not core safety invariants. Test fixtures cover modeled obstructions; representative human validation and independent safety review remain necessary.

## Cross-Program Connections

- **Platform Engineering:** platform capabilities decompose into policy, provisioning, delivery, observability, recovery, and support transformations before mapping to services or teams.
- **API and Service Engineering:** service boundaries are later allocations; functional decomposition first clarifies semantic operations, orchestration, failure, and idempotency.
- **Data Engineering:** transformation DAGs resemble functional graphs, while lineage, late data, replay, state, quality, and governance expose missing children.
- **Object-Oriented Programming:** responsibility decomposition can inform classes, but class hierarchies should not be mistaken for system functional hierarchies.
- **Functional Programming:** function composition offers precise transformation reasoning; systems decomposition additionally covers effects, state, time, people, physics, and lifecycle.
- **Safety and security:** hazard/threat analysis derives detection, prevention, containment, recovery, and evidence functions whose source and independence must remain visible.

## References

1. ISO, “ISO/IEC/IEEE 15288:2023 — Systems and software engineering — System life cycle processes,” second edition, published 2023-05. https://www.iso.org/standard/81702.html
2. NASA, “4.3 Logical Decomposition,” NASA Systems Engineering Handbook. https://www.nasa.gov/reference/4-3-logical-decomposition/
3. NASA, “System Engineering Handbook: Appendix,” entries for Functional Analysis, Functional Decomposition, Functional Baseline, and Functional Flow Block Diagram. https://www.nasa.gov/reference/system-engineering-handbook-appendix/
4. NASA, “4.0 System Design Processes,” NASA Systems Engineering Handbook. https://www.nasa.gov/reference/4-0-system-design-processes/
5. NASA, “4.2 Technical Requirements Definition,” NASA Systems Engineering Handbook. https://www.nasa.gov/reference/4-2-technical-requirements-definition/
6. SEBoK Editorial Board, “Functional Architecture,” *Guide to the Systems Engineering Body of Knowledge*, version 2.14. https://sebokwiki.org/wiki/Functional_Architecture
7. SEBoK Editorial Board, “Functional Architecture (glossary),” *Guide to the Systems Engineering Body of Knowledge*, version 2.14. https://sebokwiki.org/wiki/Functional_Architecture_%28glossary%29
8. SEBoK Editorial Board, “Logical Architecture,” *Guide to the Systems Engineering Body of Knowledge*, version 2.14. https://sebokwiki.org/wiki/Logical_Architecture
9. SEBoK Editorial Board, “System Architecture Design Definition,” *Guide to the Systems Engineering Body of Knowledge*, version 2.14. https://sebokwiki.org/wiki/System_Architecture_Design_Definition

## Exercises

### Exercise 1

Critique this decomposition of `maintain secure facility access`: `badge reader`, `door`, `database`, and `guard`. Replace it with a functional child network and identify derived functions, composition semantics, and evidence limits.

### Exercise 2

Parent `deliver verified measurement within 500 ms` has children with worst-case times: acquire 120 ms, validate 90 ms, estimate 160 ms, and publish 80 ms. Communication adds 70 ms. Determine whether the parent deadline is met under fully sequential execution, then analyze why that arithmetic is insufficient for a real decision.

### Exercise 3

Design two alternative decompositions of `restore service after regional failure`: one centralized and one federated. Preserve the same parent boundary, and compare coupling, state, authority, observability, and failure behavior.

### Exercise 4

Create a stopping rule for decomposing `provide authenticated medication dose`. Identify branches that require deeper refinement than others and explain why equal tree depth is inappropriate.

### Exercise 5

Review a clinical alert decomposition containing `collect data`, `calculate risk`, and `display alert`. Construct a high-consequence coverage argument that includes scenarios, modes, failures, humans, lifecycle functions, and bounded evidence.

## Answers to the Exercises

### Answer 1

The proposed nodes are physical elements/actors rather than transformations, so they freeze allocation and omit behavior. A functional network includes receive access request; establish claimant identity; acquire credential evidence; validate authenticity/freshness; determine authorization for location/time/mode; assess abnormal context; grant or deny access; command boundary state; verify physical state; detect tailgating/forced entry; notify/respond; log tamper-evident evidence; revoke/update authority; provide emergency egress; operate during communication/power degradation; and maintain/calibrate the access capability.

Derived functions include time synchronization, anti-replay, degraded authority cache, intrusion detection, privacy retention, and emergency override, each traced to threat, safety, interface, or lifecycle analysis rather than falsely to the parent wording. Nominal access uses AND-style cooperation; alternative credentials and online/offline authorization use explicit selection/conditional semantics; emergency egress has invariant priority. Evidence includes protocol/security analysis, physical tests, fault injection, accessibility/human validation, and configuration audit. It remains bounded by tested attacks, sites, credentials, power/network failures, populations, and applicable authority; no function list establishes facility security.

### Answer 2

Under the stated fully sequential additive model:

\[
120+90+160+80+70=520\ \text{ms},
\]

so the network exceeds the 500 ms deadline by 20 ms. The arithmetic is a useful counterexample to compliance under that model, not a complete system decision. Confirm whether communication is one or several intervals, whether acquisition and validation overlap, whether times are compatible worst cases, which queues and scheduling delays are omitted, whether physical settling or timestamp age matters, and whether uncertainty/margin is required.

Alternatives include pipelining, parallel validation, faster estimation, local publication, or a controlled parent change. Recompute end-to-end distribution/bounds for named modes and loads, examine resource contention/retries/failures, and test the integrated configuration with synchronized observation points. A nominal average below 500 ms cannot replace worst-case or percentile semantics specified by the parent. Authority must approve any reallocation or requirement change.

### Answer 3

Both alternatives accept a declared regional-loss event plus service/configuration state and produce restored bounded service, user/operator status, reconciled durable state, and recovery evidence within the same conditions. The centralized network detects region failure, validates authority, selects a recovery region, restores shared state, redirects traffic, verifies service, reconciles divergence, and communicates status. It concentrates decision/state authority and observability but creates control-plane and shared-state dependencies.

The federated network has each cell detect isolation, elect/confirm local authority, restore a bounded local service, exchange signed recovery state when links return, resolve conflicts by governed rules, and converge to global service. It improves local autonomy and can reduce central dependency, but adds consensus, split-brain, identity, conflict-resolution, and evidence complexity. Compare recovery objectives, data-loss bounds, authority during partition, security, operator workload, state ownership, testability, and common-cause failure. Neither is preferred without workload, topology, regulatory, threat, and failure evidence; simulations only cover encoded partitions and timing.

### Answer 4

Use a readiness vector: source/contribution clarity; typed interfaces; state/mode/failure definition; performance and dose-accuracy composition; hazard/threat controls; allocation alternatives; estimability; and verifiability. A branch may stop when all criteria meet thresholds appropriate to clinical consequence and the next design decision. `record administrative audit metadata` may be ready at a relatively shallow level if semantics, retention, access, and evidence are clear.

`determine authorized dose`, `deliver fluid`, `measure delivered volume`, `limit unsafe delivery`, and `respond to occlusion` require deeper refinement because calculation, units, calibration, actuator/physical dynamics, feedback delay, independent interlocks, human authority, and failure interactions carry high consequence. Depth is not uniform because uncertainty, coupling, allocation choice, and evidence differ. Stop before prescribing unjustified component internals, but continue while a safety-critical transformation lacks observable contracts or credible composition. Clinical, safety, cybersecurity, human-factors, regulatory, and source authorities review relevant branches.

### Answer 5

First restate the parent outcome: deliver a timely, intelligible, appropriately prioritized clinical alert to an authorized decision-maker for a defined population/context without unacceptable missed-harm or alert-burden risk. Expand children to establish patient/context identity; acquire timestamped/provenanced data; validate quality; normalize units; manage missing/conflicting inputs; estimate risk with versioned logic; characterize uncertainty; apply clinical policy/contraindications; prioritize; select recipient/channel; present rationale/action; receive acknowledgement/action; escalate; monitor deterioration; suppress duplicates safely; record outcome; and govern configuration, update, privacy, retention, and rollback.

Cover nominal, degraded data, downtime, emergency, handoff, duplicate, late, and unavailable-recipient cases. Model false positive/negative, wrong patient, stale data, distribution shift, alert fatigue, unauthorized access, and failed escalation. Trace every derived function to clinical need, hazard, privacy/security, interface, or lifecycle rationale. Evidence combines data-quality tests, unit/property checks, retrospective analysis, prospective representative workflow/clinical validation, fault injection, usability/accessibility review, security assessment, monitoring, and configuration audit. Each result is bounded to population, site, workflow, model/version, thresholds, data, and failure set. External clinical/regulatory authorization and independent safety review remain necessary; decomposition and accuracy alone do not establish safe care.
