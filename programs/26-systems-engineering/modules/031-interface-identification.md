---
module_id: SYSENG-031
program: Systems Engineering
level: 1
module_number: 31
title: Interface Identification
status: complete
last_verified: 2026-08-31
---

# Interface Identification

## One-Page Review

### Governing question

How can a team systematically discover and register every consequential interaction across system, element, human, organization, enabling-system, and environmental boundaries—without treating visible connectors, current organizational charts, or nominal data flows as a complete interface inventory?

### Essential definitions

- An **interface** is a governed boundary relationship through which elements interact, exchange items or effects, share resources, impose conditions, or coordinate responsibilities.
- An **interaction** is actual or possible mutual influence between entities; it may occur through data, control, material, energy, force, motion, environment, human action, procedure, or authority.
- An **interface candidate** is a discovered boundary interaction requiring classification and disposition; it is not yet a fully baselined interface definition.
- An **interface endpoint** is an interacting system, element, actor, organization, environment, or enabling system with defined boundary responsibilities.
- An **interface plane** is the conceptual or physical boundary at which responsibilities and measurable conditions are assigned to each side.
- An **internal interface** lies among elements within the selected system boundary; an **external interface** crosses that boundary to another system, actor, authority, or environment.
- A **horizontal interface** connects peer elements at a selected hierarchy level; a **vertical interface** crosses levels or connects parent/child responsibilities.
- A **direct interface** joins named endpoints; an **indirect interface/dependency** arises through a shared resource, intermediary, environment, policy, supplier, or common service.
- An **interface item** is what crosses or couples at the boundary: information, command, signal, material, fluid, energy, load, motion, heat, service, task, decision, or evidence.
- An **interface register** is the controlled inventory of candidate and governed interfaces, identities, endpoints, kinds, sources, applicability, owners, criticality, maturity, and status.
- An **interface owner** is accountable for coordinating the boundary contract and resolution; endpoint owners retain responsibility for their respective sides.
- An **interface assumption** is a provisional claim about an endpoint, environment, capacity, semantics, authority, or realization that needs an owner and validation.
- An **unintended interaction** is a coupling not required for desired behavior but capable of affecting outcomes, such as electromagnetic interference, thermal conduction, shared timing, or operator confusion.

### Central model, mechanism, or theorem

Let architecture entities be (N), system boundary (B), scenarios (S), modes/configurations (M), and typed interaction observations (X). Identify candidates as boundary-crossing relations:

$$
I_C=\{\langle id,n_s,n_t,k,x,m,s,r,h\rangle\mid n_s\neq n_t,\ CrossesBoundary(x,B),\ Consequential(x)\},
$$

where endpoints $n_s,n_t\in N\cup Environment$, kind (k), item/effect (x), applicability (m), discovering scenario/source (s), rationale (r), and assumptions (h) are explicit. Identification is adequate only when:

$$
Adequate(I_C)\Rightarrow ScenarioCoverage\land AllocationCrossingCoverage\land
ContextCoverage\land LifecycleCoverage\land SharedDependencyCoverage\land
UnintendedCouplingReview\land Ownership\land ControlledDisposition.
$$

This is an assurance obligation, not a graph theorem. A complete adjacency matrix for known nodes cannot identify an omitted external actor, environment, failure mode, or enabling system.

### Critical invariants

- Every interface candidate has stable identity, two or more explicit endpoints, directionality where meaningful, kind, discovered source, modes/configurations, owner, rationale, maturity, and disposition.
- The system boundary and architecture level are explicit; internal/external classification changes when the boundary changes, while the interaction identity and semantics remain traceable.
- Every cross-element functional allocation and control/data/material/energy/human flow produces an interface candidate or an explicit no-interface rationale.
- Every external actor, system, authority, natural environment, induced environment, and shared service in context is examined for interactions in both directions.
- Nominal, degraded, emergency, maintenance, integration, test, update, recovery, transport, storage, support, transition, and retirement scenarios are considered where applicable.
- Interface categories extend beyond software/data to control, electrical, mechanical, structural, fluid, thermal, electromagnetic, acoustic, optical, human, procedural, organizational, security, and environmental coupling.
- Shared resources and intermediaries do not hide logical endpoint responsibilities, fan-out, common causes, or trust/fault boundaries.
- Each side’s provided/required obligations, authority, assumptions, and evidence remain distinguishable; the interface owner does not absorb endpoint accountability.
- Unintended interactions and absence/loss of expected interaction are analyzed alongside desired exchanges.
- Candidate duplication, aggregation, decomposition, supersession, and rejection preserve trace and rationale.
- Criticality and maturity guide analysis priority but do not erase low-frequency or lifecycle interfaces.
- Identification evidence is bounded by examined models, scenarios, stakeholders, configurations, environments, and physical knowledge.

### Common failures

Common failures include identifying only external interfaces; equating interfaces with cables or APIs; copying current organizational handoffs; finding only nominal producer–consumer flows; omitting operators, maintainers, test equipment, facilities, suppliers, regulators, and natural environments; ignoring shared clocks, power, identity, cooling, structures, radio spectrum, or policy; representing bidirectional interaction as one ambiguous arrow; treating a bus or broker as the only endpoint; missing cancellation, acknowledgement, fault, recovery, calibration, disposal, and evidence flows; confusing a connection with the item that crosses it; allowing both sides to assume the other owns conversion or validation; assigning a generic `integration` owner; deduplicating similar interfaces that have different modes or authority; and freezing the register before physical architecture exposes new coupling.

### Compact example

A refrigerated container’s nominal model shows Sensor-to-Controller data and Controller-to-Compressor commands. Systematic identification adds electrical power and grounding; sensor mounting and thermal conduction; refrigerant and airflow; door-force and latch interactions; clock/configuration/key dependencies; operator display, alarm acknowledgement, and maintenance override; calibration and diagnostic equipment; depot lifting/transport loads; external carrier telemetry; ambient heat, moisture, vibration, electromagnetic interference, and drainage; disposal/refrigerant recovery; and shared power/common-cause effects. Each candidate records endpoints, kind, direction, modes, discovery scenario, owner, assumptions, criticality, and maturity. The register is not yet an ICD: detailed values, tolerances, protocols, and verification will be developed under control.

### Connections

SYSENG-021–030 provide functions, flows, states/modes, scenarios, logical elements, allocations, alternatives, and integrity checks that reveal boundary crossings. This module establishes the interface inventory. SYSENG-032 controls formal interface information; SYSENG-033 examines interface kinds; SYSENG-034–040 cover physical architecture, integration, and verification preparation. Later performance, safety, security, human-factors, operations, configuration, and risk work will discover and refine additional interfaces.

## Governing Question

Which interactions are consequential enough to be governed as interfaces, and what repeatable discovery process gives reasonable confidence that the inventory covers the system context, allocated behavior, lifecycle, failures, humans, environments, shared dependencies, and emerging physical realization?

The answer is triangulation. No single diagram or workshop is sufficient. Derive candidates from context boundaries, scenarios, functional allocation, flows, state/mode changes, quality analyses, hazards/threats, physical adjacency, lifecycle and enabling systems, organizational/supplier boundaries, and stakeholder walkthroughs. Register candidates early, classify and disposition them, then revisit continuously as architecture and evidence mature.

## Why This Matters

Interfaces concentrate integration risk because separate owners, models, schedules, evidence, and assumptions must agree at a boundary. A missing interface often appears late as an integration anomaly: incompatible dimensions, an unowned conversion, unexpected load, stale command, unsafe human handoff, common power fault, regulatory approval gap, or test fixture that cannot connect.

NASA’s current Interface Management guidance calls for defining internal and external functional and physical interfaces, identifying their characteristics—including human interfaces—ensuring compatibility, controlling change, and supporting product integration. NASA’s current Product Integration guidance lists mechanical, fluid, thermal, electrical, data, logical, and human interfaces and warns that interactions can be subtle and unintended. NASA’s Appendix L interface outline includes responsibility, coordinate systems, units, tolerances, structural, fluid, electrical, signal, data, environmental, electromagnetic, acoustic, load, and human-operability concerns. OMG SysML 2.0 distinguishes ports, connections, directed features, and flows. ISO/IEC/IEEE 42010:2022 supplies viewpoint discipline; ISO/IEC/IEEE 15288:2023 supplies iterative lifecycle process context. These sources support systematic discovery but do not define one universal interface taxonomy or prove inventory completeness.

Interface identification begins during problem framing and continues through retirement. Logical allocation reveals interactions before physical realization. Physical architecture later reveals contact surfaces, power, heat, loads, routing, interference, and shared infrastructure. Integration and operations reveal temporary, support, and recovery interactions. The register therefore evolves under configuration control rather than becoming a one-time spreadsheet.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. the system context defines actors, external systems, authorities, environments, and boundary assumptions;
2. functions and scenarios reveal inputs, controls, outputs, failures, and end-to-end paths;
3. states and modes determine when interactions exist, change, or become prohibited;
4. logical elements and function allocations create internal boundary crossings;
5. control/data flows require semantic, timing, authority, failure, and evidence contracts;
6. architecture alternatives and integrity checks reveal hidden coupling and shared dependencies;
7. quality properties emerge across element interactions and common resources;
8. interface identification is distinct from detailed specification, agreement, verification, and change control.

As a retrieval test, inspect a diagram showing `Mobile App -> Platform API`. Ask about identity/key issuance, time, policy, push notifications, app-store distribution, accessibility, user consent, device storage, offline behavior, telemetry, support, incident response, data deletion, network/DNS/certificate dependencies, operating-system changes, and regulatory authority. The visible API is only one part of the interface landscape.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish interface, interaction, connection, flow, port, boundary, endpoint, and interface plane;
2. define system/element boundaries and classify internal, external, horizontal, vertical, direct, indirect, temporary, and lifecycle interfaces;
3. derive interface candidates from context, scenarios, allocation, flows, states/modes, quality analysis, and physical adjacency;
4. identify data, control, material, energy, mechanical, electrical, thermal, environmental, human, organizational, and authority interactions;
5. expose shared-resource, intermediary, common-cause, trust, fault, and unintended couplings;
6. build an interface register with stable identity, ownership, applicability, source, assumptions, criticality, maturity, and disposition;
7. use context diagrams, N-squared matrices, interaction tables, sequence/state views, and physical walkthroughs without overclaiming completeness;
8. distinguish interface owner from endpoint responsibilities and establish joint discovery/validation;
9. prioritize critical interfaces while preserving coverage of enabling and lifecycle interactions;
10. govern discovery, refinement, duplication, change, and evidence limits throughout architecture evolution.

## Core Exposition

**Frame the identification effort.** State system/entity of interest, architecture level, boundary, lifecycle interval, variants, configurations, modes, environments, decisions supported, stakeholders, available models, and evidence threshold. An interface inventory for concept selection differs in detail from one supporting integration, but critical semantics cannot be deferred merely because design is early.

**Define boundaries deliberately.** Draw the system boundary and selected element boundaries. Record why each boundary exists and what remains external. Boundaries can be functional, logical, physical, organizational, contractual, jurisdictional, trust, fault, data, or lifecycle boundaries. An interaction can cross several at once. When boundaries change, reclassify and recheck interfaces rather than silently moving responsibilities.

**Start with the context.** Enumerate users, operators, maintainers, administrators, acquirers, suppliers, regulators, partner systems, infrastructure, facilities, natural environments, induced environments, and enabling systems. For each, ask what the system receives, provides, shares, constrains, senses, commands, supports, or is affected by in every applicable mode.

**Walk stakeholder outcomes.** Trace each need and operational scenario from trigger to outcome. At every transition between actors/elements, capture items/effects, direction, timing significance, authority, failure, and evidence. Include alternate, exception, cancellation, timeout, degraded, emergency, and recovery paths. Outcome walkthroughs find interfaces that static structure misses.

**Derive from functional allocation.** Whenever contributing functions reside on different logical elements, register the crossing. Include inputs/outputs, controls, state access, coordination, resources, and evidence. If no interface is required because contributions are co-owned or abstractly composed, record the reasoning; later physical separation may create one.

**Derive from control and data flows.** Convert each cross-element flow to candidate interface obligations, preserving distinct directions and flow roles. Identify occurrence/notification, query/response, command/acknowledgement/disposition, snapshot/delta, cancellation/compensation, and observability. A broker, bus, or file transfer is a realization/intermediary, not a reason to omit producer–consumer semantics.

**Derive from state and mode transitions.** Ask what enables, inhibits, synchronizes, and evidences each transition; what configuration/policy/state must cross; and what interactions are added, removed, or restricted by mode. Transition into maintenance or emergency often changes human authority and physical interlocks.

**Derive from hierarchy.** Examine parent–child and peer boundaries at each relevant level. External interfaces of a child may be internal to its parent, but they still need identity and ownership. Avoid flattening every lower-level interaction into the system-level register; use hierarchy and trace while surfacing critical cross-level effects.

**Use N-squared analysis.** Place candidate elements on both axes. For each ordered pair, ask what flows or coupling exists. The diagonal describes element scope, not interfaces. An $n$-element directed matrix has (n(n-1)) off-diagonal cells; the number is a search space, not an expected interface count. Grouping can manage scale, but cross-group review is essential.

**Use interaction tables.** For every candidate, record stable ID, names/aliases, source/target endpoints, direction, kind, item/effect, purpose, source requirement/scenario/decision, modes/configurations, criticality, owner, endpoint representatives, assumptions, maturity, status, related candidates, and next evidence. Do not wait for all detailed values before assigning identity.

**Distinguish connection, port, and flow.** A port describes an interaction point and allowed features; a connection permits interaction; a flow identifies what transfers in a context. One connection may carry several flows, and one logical flow may later use several physical paths. Preserve these relationships rather than using `interface` for every concept.

**Identify directionality explicitly.** Many interfaces are bidirectional in aggregate but asymmetric in obligations. Split command, acknowledgement, status, and evidence unless a compound contract is clearer. For mechanical/thermal/environmental interfaces, direction may reverse or be mutual; describe loads/effects and sign/reference conventions rather than forcing a software-arrow metaphor.

**Classify interaction kinds.** Consider functional/service, data/information, command/control, event/signal, electrical power/grounding, mechanical/structural/load/motion, fluid/material, thermal, optical, radio/electromagnetic, acoustic/vibration, environmental, human physical/cognitive, procedure/process, organizational/contractual, policy/authority, and shared-resource interactions. Classification guides specialists but should not fragment one coupled boundary into unrelated records without trace.

**Find shared-resource interfaces.** Search for common power, ground, clock/time, network, compute, storage, identity, key, policy, data source, cooling, structure, workspace, spectrum, facility, supply chain, operator, and test equipment. Two elements may not exchange directly yet still interfere or fail together through the shared resource.

**Find environmental coupling.** The environment can be an endpoint and a transmission medium. Examine temperature, pressure, humidity, contamination, radiation, vibration, acoustics, electromagnetic fields, weather, terrain, biological/chemical exposure, illumination, and physical occupancy. Identify both system effects on the environment and environmental effects on the system.

**Find unintended interactions.** Ask how energy, information, force, heat, vibration, emissions, leakage, privilege, operator attention, or state can cross despite no desired flow. Hazard, threat, FMEA, fault-tree, privacy, and common-cause analyses are discovery methods. Register or explicitly disposition consequential couplings.

**Find absence interfaces.** The loss, delay, or corruption of an expected interaction changes behavior. Register monitoring, timeout, fallback, safe state, recovery, reconciliation, and evidence needs. “No message” is ambiguous unless absence detection and time basis are defined.

**Include humans as endpoints.** Identify physical controls, displays, alarms, information, procedures, communication, workload, authority, handoff, confirmation, accessibility, protective equipment, maintenance access, and recovery. Do not reduce a human interface to screen layout; tools, environment, staffing, training, and organizational communication shape performance.

**Include organizations and authorities.** Supplier/acquirer boundaries, certification, regulatory approval, data stewardship, incident notification, operational command, and change authority can create interfaces even before physical realization. Contractual boundaries do not remove system responsibility for technical compatibility and outcome.

**Include enabling systems.** Integration rigs, test equipment, simulators, calibration tools, manufacturing, deployment, configuration services, training systems, maintenance tools, logistics, support desks, security operations, backup/recovery, migration, and disposal systems interact with the target system. Temporary interfaces can create lasting constraints or hazards.

**Walk the lifecycle.** Examine fabrication, assembly, transport, storage, installation, commissioning, operation, maintenance, update, repair, recovery, upgrade, migration, decommissioning, data disposition, and disposal. Interfaces may exist only during one interval; qualify them rather than omitting them.

**Identify interface responsibilities.** Name the interface owner/change forum and responsible representative for each endpoint. Clarify who proposes, specifies, supplies, consumes, validates, verifies, monitors, resolves anomalies, and approves change. Joint agreement does not mean accountability is shared vaguely.

**Capture assumptions early.** Record provisional endpoint capabilities, standards, loads, environments, rates, units, authority, availability, technology, and supplier behavior. Link each assumption to owner, basis, risk, validation date, and affected candidates. Assumptions often reveal interfaces before formal requirements exist.

**Assess criticality.** Consider safety, mission/essential function, security/privacy, performance, coupling, uncertainty, novelty, supplier/organization boundary, change rate, integration sequence, recovery, observability, and verification difficulty. Use categories with operational definitions. Criticality prioritizes work; it is not a reason to ignore low-ranked interfaces.

**Assess maturity.** Suggested states include discovered, triaged, endpoints agreed, semantics bounded, requirements drafted, jointly agreed, baselined, verified, monitored, and retired. Define exit evidence for each. Percent-complete labels without conditions hide incompatible interpretations.

**Deduplicate carefully.** Candidates may be duplicates, views of one interface, subinterfaces, bundles, or separate mode-specific contracts. Merge only when endpoints, purpose, authority, applicability, and change/verification ownership align. Preserve aliases and source traces. Split when one record becomes too broad to own or verify.

**Use architecture viewpoints together.** Context diagrams reveal externals; functional/sequence/state views reveal behavior; logical/component views reveal allocation boundaries; N-squared matrices reveal overlooked pairs; data models reveal semantic dependencies; physical layouts reveal contact/coupling; hazard/threat views reveal unintended paths; lifecycle maps reveal temporary interfaces. Reconcile identities across them.

**Validate with both sides.** Review every candidate with knowledgeable endpoint representatives and system integrators. Confirm endpoints, direction, purpose, modes, responsibility, assumptions, and missing interactions. One side’s inventory is not agreement; an external party may use different boundary, vocabulary, version, or authority.

**Prioritize early integration knowledge.** Interface identification should inform architecture decisions, prototypes, standards selection, supplier engagement, integration sequence, test equipment, and risk retirement. Target high-criticality/high-uncertainty boundaries for early evidence rather than waiting for final documents.

**Govern additions and changes.** New scenarios, element splits/merges, allocation changes, physical mapping, supplier decisions, hazard/threat findings, failures, or operational evidence can create or change interfaces. Assess related requirements, endpoints, owners, evidence, integration plans, and retired records. Never silently reuse an old ID for new semantics.

**State evidence limits.** A context workshop cannot reveal all physical interference. An N-squared matrix cannot find omitted nodes. A model query cannot find semantics not represented. Supplier confirmation may not establish system-level performance. Record which discovery lenses ran and what physical/operational knowledge remains unavailable.

The following checker finds selected declaration defects in five interface-candidate records. It cannot establish inventory completeness or compatibility.

<!-- bijux-verify: {"id":"interface-candidate-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidates_total=5\nwell_formed_declared=1\nmissing_endpoints=IF-002\nmissing_kind=IF-003\nmissing_modes=IF-004\nmissing_owner=IF-005\nunresolved=IF-002,IF-003,IF-004,IF-005\nevidence=declared_fields_only\n","stderr":""}} -->
```python
candidates = [
    {"id": "IF-001", "endpoints": ["Sensor", "Control Policy"],
     "kind": "data", "modes": ["normal", "degraded"], "owner": "Control Integration"},
    {"id": "IF-002", "endpoints": [], "kind": "electrical power",
     "modes": ["all"], "owner": "Power Integration"},
    {"id": "IF-003", "endpoints": ["Operator", "Controller"], "kind": "",
     "modes": ["maintenance"], "owner": "Human Systems Integration"},
    {"id": "IF-004", "endpoints": ["Container", "Ambient Environment"],
     "kind": "thermal", "modes": [], "owner": "Thermal Integration"},
    {"id": "IF-005", "endpoints": ["Calibration Rig", "Sensor"],
     "kind": "test/calibration", "modes": ["maintenance"], "owner": ""},
]
required = ("endpoints", "kind", "modes", "owner")
valid = [candidate for candidate in candidates if all(candidate[field] for field in required)]
print(f"candidates_total={len(candidates)}")
print(f"well_formed_declared={len(valid)}")
for field in required:
    print(f"missing_{field}=" + ",".join(c["id"] for c in candidates if not c[field]))
print("unresolved=" + ",".join(c["id"] for c in candidates if c not in valid))
print("evidence=declared_fields_only")
```

IF-001 may still omit semantic, timing, quality, security, failure, or physical-path interactions. Populated fields are discovery evidence only.

## Definitions and Notation

Let entities $N=N_{internal}\cup N_{external}\cup N_{environment}$, scenarios (S), modes/configurations (M), and interface candidates (I_C). Directed adjacency matrix (A\in\{0,1\}^{n\times n}) can record discovered interaction from (n_i) to (n_j):

$$
A_{ij}=1\iff\exists i_c\in I_C:(source(i_c)=n_i\land target(i_c)=n_j).
$$

There are (n(n-1)) off-diagonal ordered cells or (n(n-1)/2) unordered pairs. These counts define review opportunities, not expected interface totals; multiple kinds can exist per pair and omitted nodes remain invisible.

For scenario-mode discovery coverage:

$$
C_{SM}=\frac{|\{(s,m)\in S\times M:reviewed(s,m)\}|}
{|\{(s,m)\in S\times M:applicable(s,m)\}|}.
$$

A 100% declaration indicates all known applicable cells were reviewed, not that scenarios or modes are complete or review was adequate.

Candidate record:

$$
i_c=\langle id,endpoints,direction,kind,item,purpose,source,modes,owner,
criticality,maturity,assumptions,status,version\rangle.
$$

Detailed values and verification methods may mature later, but identity, endpoints, source, ownership, applicability, and disposition should not remain implicit.

## Mechanisms, Invariants, or Proof Structure

Use an interface-identification loop:

1. **Frame boundaries:** declare system, element, lifecycle, organizational, trust/fault, and environmental boundaries plus configurations and evidence threshold.
2. **Discover from behavior/context:** walk actors, needs, scenarios, functions, allocations, states/modes, flows, hierarchy, and architecture alternatives.
3. **Discover coupling:** inspect shared resources, physical adjacency, environments, humans, organizations, hazards/threats, common causes, enabling systems, and lifecycle transitions.
4. **Register and classify:** assign identity, endpoints, direction, kind, source, applicability, owner, assumptions, criticality, maturity, and disposition.
5. **Triangulate:** compare context, N-squared, sequence/state, logical, data, physical, quality, risk, and lifecycle views; inspect negative space.
6. **Validate and prioritize:** review with both endpoint representatives and integrators; target critical/uncertain candidates for early definition and evidence.
7. **Govern evolution:** control merges/splits/supersession, boundary/allocation/physical changes, anomalies, evidence, and retirement.

The assurance argument is bounded: the inventory is adequate for named decisions because defined discovery lenses covered controlled scenarios, elements, modes, environments, and lifecycle stages; candidates have ownership and disposition; and independent endpoint review occurred. It does not prove no unknown interaction exists.

## Alternatives and Trade-Offs

**Top-down versus bottom-up discovery.** Top-down context/function/scenario work preserves purpose but can miss implementation coupling. Bottom-up physical/product analysis finds real contact and protocols but can inherit accidental design. Iterate both and reconcile.

**Central register versus federated registers.** One register aids identity, dependency, and reporting. Federated domain registers preserve specialist detail and supplier control. Federation requires shared IDs, ownership, configuration, and cross-register queries.

**Fine-grained versus bundled interfaces.** Fine records improve ownership and verification but can overwhelm governance. Bundles aid navigation but can hide different criticality, modes, or change authority. Use hierarchy with trace.

**Early broad capture versus late precise capture.** Early candidates expose risk while uncertain; late capture has detail but loses architecture influence. Register provisional assumptions and maturity rather than waiting.

**Endpoint pair versus interaction-centric identity.** Pair-based records are simple but one pair may carry unrelated contracts. Interaction-centric records preserve semantics; a parent boundary record can group them for coordination.

**Risk-prioritized versus uniform analysis.** Uniform review improves coverage but spends deeply on trivial boundaries. Risk-based depth focuses evidence while a minimum inventory obligation prevents low-ranked omissions.

**Logical versus physical interface focus.** Logical discovery supports alternative solutions; physical discovery exposes real loads, paths, and interference. Preserve mappings so one does not masquerade as the other.

## Failure Modes and Misconceptions

- **Connector inventory:** only drawn lines are registered. Derive from scenarios, allocations, environments, and lifecycle.
- **API tunnel vision:** interfaces are assumed digital. Review energy, matter, force, heat, humans, authority, and environment.
- **External-only scope:** peer internal boundaries disappear. Inspect every relevant level and allocation crossing.
- **Nominal-path bias:** failure, cancellation, maintenance, recovery, and retirement interactions are absent. Use scenario-mode coverage.
- **Bus endpoint fallacy:** the intermediary replaces producer/consumer semantics. Preserve end-to-end and intermediary responsibilities.
- **Bidirectional blob:** opposite flows have different authority/timing/failure semantics. Identify them distinctly.
- **Shared-resource blindness:** elements appear independent while sharing power, clock, identity, cooling, or operator. Register indirect dependencies.
- **Human-as-display:** cognitive, physical, procedural, workload, authority, accessibility, and environment are omitted.
- **Environment-as-constraint only:** system emissions/effects on environment and environment-mediated coupling are missed.
- **Interface-owner catch-all:** one coordinator becomes responsible for both endpoint implementations. Preserve side-specific accountability.
- **Supplier-boundary assumption:** contract lines define architecture truth. System integration retains technical outcome responsibility.
- **Premature deduplication:** similar names merge distinct modes, jurisdictions, or authorities. Compare semantics and ownership first.
- **Maturity by percentage:** status lacks exit evidence. Define controlled maturity states.
- **Criticality as deletion:** low score removes lifecycle interaction. Prioritize depth without losing inventory coverage.
- **Frozen discovery:** the register stops evolving after concept review. Re-run after allocation, physical, supplier, hazard, integration, and operational changes.
- **Completeness claim:** matrix coverage is treated as proof. State omitted-node and model limitations.

## Worked Examples

### Example 1

An emergency-notification architecture initially registers one API between Warning Coordination and a carrier. Scenario walking adds identity/authorization, policy update, message dispatch, disposition, cancellation, duplicate suppression, operator escalation, clock, audit, billing, incident, and support interactions. Carrier loss also creates fallback and reconciliation candidates. Each direction has distinct authority and timing.

### Example 2

A pump skid’s control diagram omits mechanical base loads, pipe forces, fluid pressure/chemistry, electrical power/ground, heat, vibration, drainage, access clearance, lifting points, operator controls, and maintenance isolation. A physical walkthrough with civil, mechanical, electrical, controls, safety, and maintenance specialists produces the interface inventory before detailed tolerances are set.

### Example 3

Two redundant controllers have no direct connection, so an adjacency diagram suggests independence. Shared-resource review identifies one time source, power converter, sensor bus, configuration service, cooling path, and operator. These indirect interfaces become common-cause candidates; later physical evidence must justify any independence claim.

### Example 4

A six-element directed N-squared matrix has (6(5)=30) off-diagonal review cells or 15 unordered pairs. Review finds interactions in eight ordered cells and two pairs with multiple kinds. “Eight of 30” is not interface completeness: external actors and environment were absent, and one pair carries power, data, and thermal coupling.

### Example 5

A medical device UI record covers display data but not alarm sound, physical control force, gloved use, color-independent coding, language, confirmation, workload, cleaning, protective equipment, training, or clinician handoff. Human-centered scenario review adds candidates and evidence needs. Clinical and accessibility authorities must validate fitness; the register itself does not.

### Example 6

A satellite maintenance scenario uses a ground calibration rig only before launch. The team had omitted it because it is not part of flight. The temporary calibration, power, mechanical fixture, software/configuration, time, data custody, and evidence interfaces directly affect flight accuracy, so they receive lifecycle-qualified identities and verification plans.

### Example 7

A data platform connects through a broker. Treating the broker as both endpoint and owner hides producer schema authority, consumer purpose, replay/retention, tenant isolation, and end-to-end latency. Records separate producer–broker, broker-service, and producer–consumer semantic relationships with trace among them.

### Example 8

A battery enclosure meets data and power requirements but overheats adjacent equipment through structural conduction. Thermal/environmental discovery adds contact conductance, radiative view, airflow obstruction, temperature limits, sensor evidence, and fault-mode heat. The unintended interface changes placement and test plans.

### Example 9

A supplier contract assigns an external navigation unit. The system register still identifies coordinate frame, units, timing, uncertainty, integrity, initialization, degraded behavior, cybersecurity, export/data rights, configuration, update, support, and anomaly-resolution interfaces. Procurement ownership does not replace technical ownership.

### Example 10

Retirement analysis of a tenant platform finds export, deletion, key destruction, legal hold, audit transfer, identity revocation, billing closure, support communication, and supplier termination interfaces missing from operational diagrams. Adding them exposes a retained backup dependency and changes the decommissioning architecture.

## Cross-Program Connections

- **Platform engineering:** shared control planes, identity, policy, networks, cells, observability, tenants, and operators create direct and indirect interfaces.
- **API and service engineering:** APIs, events, schemas, retries, errors, and versioning refine information interfaces but do not cover power, humans, organization, or environment.
- **Data engineering:** source authority, lineage, event time, quality, retention, deletion, and custody are interface-discovery concerns across pipelines and owners.
- **Object-oriented programming:** collaborations and dependency inversion expose code interfaces; system boundaries still require lifecycle and physical/human analysis.
- **Functional programming:** typed composition highlights flows and effects, while runtime resources, external state, timing, and organizational authority add interfaces.
- **Safety and security:** hazard/threat paths reveal unintended interaction, control authority, common cause, trust boundaries, and emergency interfaces.
- **Integration and test:** interface inventory drives integration order, simulators, test equipment, observability, anomaly ownership, and verification coverage.
- **Operations:** monitoring, support, maintenance, update, recovery, and retirement reveal interfaces absent from nominal product behavior.

## References

1. NASA, *Systems Engineering Handbook, Section 6.3: Interface Management*, current web edition, updated 2023. <https://www.nasa.gov/reference/6-3-interface-management/>
2. NASA, *Systems Engineering Handbook, Appendix L: Interface Requirements Document Outline*, current web edition, updated 2023. <https://www.nasa.gov/reference/appendix-l-interface-requirements-document-outline/>
3. NASA, *Systems Engineering Handbook, Section 5.2: Product Integration*, current web edition, updated 2023. <https://www.nasa.gov/reference/5-2-product-integration/>
4. NASA, *Systems Engineering Handbook, Section 4.3: Logical Decomposition*, current web edition, updated 2023. <https://www.nasa.gov/reference/4-3-logical-decomposition/>
5. Object Management Group, *Systems Modeling Language Version 2.0*, formal specification, 2025. <https://www.omg.org/spec/SysML/2.0>
6. Object Management Group, *Systems Modeling Language Version 2.0, Part 1: Language Specification*, current formal document. <https://www.omg.org/spec/SysML/2.0/Language/PDF>
7. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2022. <https://www.iso.org/standard/74393.html>
8. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>

## Exercises

### Exercise 1

Identify and register interface candidates for an autonomous greenhouse across normal, storm, communications-loss, maintenance, update, recovery, and retirement scenarios. Include at least eight endpoints and ten interaction kinds, plus indirect/unintended couplings and evidence limits.

### Exercise 2

For nine candidate logical elements, compute the number of ordered off-diagonal N-squared cells and unordered pairs. If 18 ordered cells contain discovered interactions, calculate declaration occupancy and explain why it is not completeness.

### Exercise 3

Review an interface register containing only endpoint names, protocol, and owner for production operation. Identify at least twelve missing discovery/management fields or lenses and propose a controlled maturity path.

### Exercise 4

A safety controller and primary controller have no direct flow but share power, clock, sensor, configuration source, cooling, enclosure, and maintainer. Classify the interfaces/common causes, state what should enter the logical register now, and distinguish later evidence obligations.

### Exercise 5

Design an interface-identification review for splitting a monolithic regional platform into cells. Include boundaries, scenarios/modes, N-squared and flow analysis, humans/organizations, shared resources, migration, security/privacy, criticality, ownership, validation with both sides, and re-review triggers.

## Answers to the Exercises

### Answer 1

Endpoints can include Sensor Network, Environmental Interpretation, Control Policy, Heating, Ventilation, Irrigation, Power, Operator, Maintenance Technician, Weather Service, Communications Provider, Configuration/Identity Service, Calibration Rig, Facility Structure, Ambient Environment, and Disposal Provider. Register observation data; control commands/status/evidence; electrical power/ground; water/nutrient fluid; heat/airflow; structural mounting/load; vibration/acoustics; radio/network; clock/configuration/key; operator display/control/alarm; maintenance access/isolation; calibration; weather/policy; drainage; incident/support; update/rollback; export/deletion; and material disposal interactions.

Qualify storm, disconnected local control, sensor disagreement, maintenance override, partial update, recovery reconciliation, and retirement. Indirect couplings include shared power, clock, network, cooling/air volume, operator attention, and structure. Unintended effects include electromagnetic interference, condensation, heat conduction, water leakage, airflow short-circuit, and conflicting commands. Each record needs endpoints, direction, kind/item, purpose/source, modes, owner/representatives, assumptions, criticality, maturity, status, and evidence action. Workshops and models cannot establish physical coupling magnitudes, human workload, provider behavior, or field performance; physical inspection, supplier agreement, simulation, prototypes, and representative trials remain necessary.

### Answer 2

For (n=9), ordered off-diagonal cells are:

$$
n(n-1)=9(8)=72.
$$

Unordered pairs are:

$$
n(n-1)/2=9(8)/2=36.
$$

If 18 ordered cells contain at least one discovered interaction, occupancy is $18/72=25\%$. This is not completeness: empty cells may be correct, one cell can contain multiple interfaces, direction and kinds differ, external/environment/enabling nodes may be omitted, hierarchy may hide crossings, and discovery adequacy depends on scenarios, modes, lifecycle, shared resources, and unintended coupling. The matrix organizes questions; it does not prescribe density.

### Answer 3

Missing fields include stable ID, aliases, endpoint roles/representatives, direction, interaction kind, item/effect, purpose, source requirement/scenario/decision, modes/configurations, lifecycle interval, internal/external/hierarchy classification, assumptions, criticality rationale, maturity, status/disposition, related/superseded IDs, trust/fault boundary, next evidence, version, and change authority. Missing lenses include alternate/failure/recovery, human, physical/environmental, shared-resource, enabling-system, migration, support, and retirement analysis.

A controlled path can use discovered, triaged, endpoints agreed, semantics bounded, requirements drafted, jointly agreed, baselined, verified, monitored, and retired states, each with exit evidence. First assign identity/source/owner/applicability and triage; then validate candidates with both sides; bound semantics/qualities and assumptions; derive requirements; jointly approve; baseline; verify under applicable scenarios; monitor anomalies/changes; and retire with residual dependencies closed. Protocol is a later realization attribute, not sufficient identification.

### Answer 4

The controllers have indirect interfaces through electrical power/ground, shared time, sensor/data authority, configuration/policy provenance, thermal path/cooling, mechanical/environmental enclosure, and human maintenance/procedure. These are common-cause paths and may also be trust, fault, and authority interfaces. The logical register should identify shared-service dependencies, required independence or bounded sharing, endpoint responsibilities, modes, failure consequences, assumptions, criticality, and planned evidence without asserting physical independence.

Later physical architecture must map supplies, routing, clocks, sensor diversity, configuration distribution, cooling zones, structural/fire/environmental separation, tools/procedures, and organizational access. Evidence may include schematics/layout, fault tree/common-cause analysis, FMEA, power/thermal/environmental tests, clock and data-fault injection, diverse sensor validation, configuration/security review, maintenance trials, and integrated fault tests. Logical separation alone proves none of those.

### Answer 5

Frame tenant, region, control/data, trust, fault, jurisdiction, organizational, and migration boundaries. Compare current monolith, cell internals, shared/global services, external providers, operators, tenants, regulators, and environments. Walk provisioning, request routing, authorization, data operations, policy/configuration update, observability, billing, incident, overload, regional partition, identity/key failure, partial deployment, rollback, tenant migration, recovery/rejoin, support, and retirement modes.

Use a context diagram, function-allocation crossings, directed N-squared matrix, sequence/state/flow views, data authority/lineage, threat/privacy analysis, physical/cloud-region topology, and lifecycle map. Register API/event/state, identity/key/policy, network/DNS/time, storage/backup, compute/capacity, telemetry, operator/admin, supplier, data-residency, billing, migration/export/deletion, and support interfaces. Expose shared control plane, deployment pipeline, artifact registry, identity, keys, policy source, telemetry, suppliers, and administrators as common dependencies.

Assign an interface owner and representatives on both sides; define criticality from tenant isolation, authority, availability, uncertainty, change rate, integration sequence, and evidence difficulty. Validate with cell, shared-service, operations, security/privacy, data, tenant, supplier, and regulatory representatives. Trigger re-review on cell split/merge, shared-service change, new region/jurisdiction, supplier/protocol change, threat/hazard finding, migration anomaly, load/failure evidence, ownership change, or retirement. The conclusion is bounded to reviewed topologies, scenarios, providers, and evidence; production scale and physical/cloud independence require later verification.
