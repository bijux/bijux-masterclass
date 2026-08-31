---
module_id: SYSENG-035
program: Systems Engineering
level: 1
module_number: 35
title: Physical Architecture
status: complete
last_verified: 2026-08-31
---

# Physical Architecture

## One-Page Review

### Governing question

How can a team transform logical responsibilities, interface contracts, and quality constraints into a buildable, deployable, operable, maintainable, and retireable arrangement of real system elements without prematurely freezing detail or losing system-level integrity?

### Essential definitions

- A **physical architecture** is the governed arrangement of realized system elements, locations, paths, interfaces, and organizing principles that implements the logical architecture and satisfies lifecycle requirements.
- A **physical element** is an identifiable realized part of the system or enabling context, including hardware, software execution units, data stores, people/roles, procedures, facilities, organizations, materials, or services when they participate in system outcomes.
- A **logical-to-physical allocation** maps functions, behaviors, information, performance, constraints, and responsibilities to physical elements. It is commonly many-to-many.
- A **physical interface** is the implemented boundary relationship through which data, control, energy, material, force, heat, motion, human action, or authority passes or couples.
- A **physical path** is the sequence of elements and interfaces that carries an interaction between endpoints.
- **Partitioning** groups responsibilities and realization into elements using criteria such as technology, cohesion, coupling, location, trust, fault containment, environment, organization, manufacture, integration, maintenance, and change.
- A **deployment view** maps software, data, people, or services to execution nodes, devices, facilities, networks, and locations.
- A **product breakdown structure (PBS)** is a hierarchical product decomposition used for planning and control; it is not a complete architecture because peer connections, paths, deployment, modes, and emergent interactions may be absent.
- An **enabling system/product** supports development, manufacture, integration, verification, deployment, training, operation, maintenance, recovery, or retirement of the system of interest.
- A **heritage or reused element** is an existing product or design considered for a new context; heritage is evidence to investigate, not proof of suitability.
- A **configuration** is an identified arrangement and version set valid for a declared purpose, environment, and lifecycle interval.
- A **physical architecture baseline** is an approved, configuration-controlled set of views, allocations, interfaces, budgets, rationale, and evidence at a declared resolution.

### Central model, mechanism, or theorem

Let logical elements be (L), physical elements (P), required logical interactions (F\subseteq L\times L), physical connections (E_P\subseteq P\times P), and allocation relation (A\subseteq L\times P). A candidate physical architecture is structurally adequate only if:

$$
\forall l\in L_{required},\ \exists p\in P:\ (l,p)\in A,
$$

and every required logical interaction has at least one permitted physical path between allocated endpoints:

$$
\forall(l_i,l_j)\in F,\ \exists p_i,p_j:\ (l_i,p_i)\in A\land(l_j,p_j)\in A
\land Path_{E_P}(p_i,p_j).
$$

This graph condition is necessary, not sufficient. Each path must also satisfy semantic, timing, capacity, safety, security, physical, human, environmental, and lifecycle contracts. For resource (r) on physical element (p):

$$
\sum_{l:(l,p)\in A} demand_r(l,p,c,m) + overhead_r(p,c,m)
\le capacity_r(p,c,m)-reserve_r(p,c,m)
$$

for every applicable configuration (c) and mode (m). Architecture quality is conjunctive; an elegant block diagram cannot compensate for an infeasible load, unowned path, unsafe maintenance action, or unavailable enabling product.

### Critical invariants

- Every required logical responsibility and flow is allocated or explicitly deferred with owner, bound, rationale, and decision condition.
- Every physical element has stable identity, purpose, owner, type, location, configuration, lifecycle, allocated responsibilities, interfaces, budgets, and evidence state.
- Allocation preserves end-to-end behavior and qualities, not only function names; shared, replicated, migrated, or human responsibilities remain explicit.
- Every required logical interaction maps to controlled physical endpoints and paths with compatible interface contracts.
- Resource budgets include overhead, concurrency, transient/fault/degraded behavior, uncertainty, and reserve using consistent planes and configurations.
- Fault-containment, trust, safety, privacy, regulatory, organizational, supplier, and physical-environment boundaries are represented where they affect architecture.
- Hardware, software, data, people, procedures, facilities, networks, and enabling systems are included when needed for outcomes.
- Reuse and commercial products are assessed in the new architecture, environment, load, interface, assurance, supply, and lifecycle context.
- Physical hierarchy, connectivity, spatial layout, deployment, behavior, lifecycle, and configuration views describe the same governed identities.
- Assembly, integration, verification, operation, maintenance, update, recovery, transport, storage, and retirement are feasible for the architecture.
- Variants and versions identify permitted configurations; diagrams do not silently combine incompatible alternatives.
- The physical baseline remains traceable to stakeholder needs, requirements, logical architecture, decisions, assumptions, contracts, hazards, verification, and change history.

### Common failures

Common failures include equating physical architecture with hardware; turning the organization chart or vendor catalog into the design; forcing one logical function into one box; copying the PBS as architecture; choosing technology before comparing alternatives; drawing connections without path capacity or failure behavior; omitting data stores, networks, operators, procedures, facilities, test equipment, and maintenance tools; assuming reused equipment works in a new environment; counting nominal load without overhead or simultaneous peaks; optimizing each subsystem separately; hiding common power, clock, identity, cooling, structure, or operator dependencies; mixing variants in one picture; specifying components without locations; ignoring assembly and access; and baselining attractive diagrams whose allocations, contracts, budgets, and evidence do not agree.

### Compact example

A refrigerated-container logical architecture contains sense temperature, estimate cargo state, select cooling, actuate compressor, alert operator, record evidence, and recover from faults. A physical architecture maps sensing to redundant probes and an edge controller; estimation/control to edge software; durable records and fleet analytics to a cloud service; cooling to compressor, power electronics, refrigerant loop, insulation, and airflow; alerts and recovery to the controller, gateway, operator console, technician, and procedures. Power, network, thermal, mounting, calibration, data, human, and supplier paths are explicit. When connectivity is lost, essential control remains local; when one probe disagrees, the controller degrades and alerts. The physical architecture is the governed arrangement and allocation, not just the enclosure drawing.

### Connections

SYSENG-026–030 establish logical components, allocations, alternatives, and integrity; SYSENG-031–034 establish interfaces and contracts. This module realizes those abstractions. SYSENG-036 decomposes the physical architecture into subsystems; SYSENG-037 orders integration from its dependencies; SYSENG-038–040 develop plans, reviews, and verification around the selected configuration. Later specialty and lifecycle modules challenge the same architecture from performance, safety, reliability, security, human, manufacturing, operational, and sustainment viewpoints.

## Governing Question

Which physical elements, locations, paths, interfaces, technologies, allocations, configurations, and lifecycle arrangements can jointly realize the logical architecture and stakeholder outcomes with adequate performance, margin, evidence, and evolvability?

The answer is iterative synthesis and analysis. Generate materially different candidate arrangements; allocate logical responsibilities and qualities; define physical paths and interface contracts; build resource and lifecycle budgets; analyze fault, trust, environment, supplier, human, integration, and maintenance consequences; compare alternatives; prototype high-risk assumptions; select with rationale; then refine and baseline only to the resolution needed for the decision and lifecycle stage. Physical architecture is a coherent system model, not early detailed design and not an inventory.

## Why This Matters

Logical architecture establishes what responsibilities and interactions are necessary while preserving realization freedom. Physical architecture spends that freedom. Decisions about distribution, technology, location, redundancy, partitioning, suppliers, paths, people, facilities, and interfaces create real cost, schedule, performance, safety, security, and lifecycle consequences. They also become progressively expensive to reverse.

NASA's current Design Solution Definition guidance describes translating validated requirements and logical decomposition into alternative design solutions, comparing them, selecting a preferred alternative, increasing its resolution, fully defining the solution, securing enabling products, and baselining under configuration control. It explicitly warns against premature focus on one design and calls attention to cabling and maintainer repair. NASA's current Product Integration guidance treats subsystem interactions and natural/induced environments as central from concept through lifecycle, including mechanical, fluid, thermal, electrical, data, logical, and human interfaces.

The current SEBoK physical-architecture treatment describes a concrete arrangement that accommodates logical architecture and system requirements, with logical-to-physical allocation and partitioning guided by technology, flows, control, dependability, environments, and enterprise constraints. ISO/IEC/IEEE 42010:2022 provides architecture-description discipline; ISO/IEC/IEEE 15288:2023 provides lifecycle process context. OMG SysML 2.0 provides parts, ports, connections, interfaces, allocations, flows, states, constraints, requirements, cases, and views. None of these sources makes one diagram or notation sufficient.

Physical architecture determines what can be built and integrated. A logical “store record” might become local flash, replicated databases, a human log, or all three. A logical “control” might become embedded firmware, a remote service, a mechanical governor, an operator, or a hybrid. Each choice changes timing, failure, trust, power, thermal, staffing, update, and recovery behavior. The systems engineer keeps these consequences connected to the original outcomes and contracts.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. stakeholder outcomes, operational scenarios, system boundary, environments, and lifecycle concept;
2. validated technical requirements, constraints, measures, margins, and verification intent;
3. logical functions/components, behaviors, states/modes, data/control/material/energy flows, and end-to-end qualities;
4. architecture alternatives and their decision rationale rather than only the selected concept;
5. interface identities, planes, contracts, assumptions, paths, and change authority;
6. basic graph, resource-budget, geometric, physical, and uncertainty reasoning;
7. product, work, organizational, and configuration structures and their distinct purposes;
8. safety, security, reliability, human, manufacturing, supplier, operations, maintenance, and retirement concerns.

As a retrieval test, inspect a logical component named `Identity and Access`. Ask whether it becomes one service, distributed policy engines, device credentials, human administrators, enrollment stations, key-management hardware, recovery procedures, audit stores, vendor infrastructure, and network dependencies. Ask where it executes in disconnected, degraded, maintenance, and emergency modes; who owns each path; which trust/fault boundaries exist; and how it is integrated and recovered. A single “IAM box” is not yet physical architecture.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish logical architecture, physical architecture, detailed design, inventory, PBS, organization chart, and deployment view;
2. identify physical elements across hardware, software, data, human, procedure, facility, organization, service, and enabling-system domains;
3. construct and review many-to-many logical-to-physical allocation with behavior and quality traceability;
4. map logical interactions to physical endpoints and paths with controlled contracts;
5. partition using cohesion, coupling, technology, location, fault, trust, environment, supplier, lifecycle, and change criteria;
6. build resource, performance, mass, power, thermal, network, staffing, and spatial budgets by configuration and mode;
7. represent hierarchy, connectivity, location, deployment, lifecycle, configuration, and rationale in consistent views;
8. evaluate reuse, commercial products, technology maturity, supply, enabling products, assembly, integration, maintenance, and retirement;
9. compare candidate physical architectures and identify decisive prototypes or analyses;
10. baseline a selected architecture at appropriate resolution with assumptions, margins, evidence, and change control.

## Core Exposition

**Frame the architecture decision.** Declare system of interest, boundary, lifecycle interval, configurations, environments, stakeholder decisions, required resolution, available evidence, constraints, and authority. A concept architecture may identify classes of elements and technology options; an implementation baseline needs producible definitions, interfaces, versions, and enabling products. Do not demand detailed part numbers before the decision needs them, but do not use abstraction to hide feasibility.

**Preserve logical independence initially.** Begin from logical responsibilities and contracts rather than current components or preferred vendors. Logical architecture provides a check against solution fixation. Physical synthesis can then combine, split, replicate, migrate, or assign responsibilities to humans and automation with explicit rationale.

**Generate candidate physical strategies.** Vary centralization/distribution, local/remote execution, hardware/software/human allocation, active/passive implementation, topology, redundancy, technology, supplier, location, packaging, power/thermal architecture, communication, maintenance concept, and upgrade strategy. Candidates must be comparable at consistent scope and maturity. Cosmetic variants of one favored design do not explore the decision space.

**Identify physical elements broadly.** Include processors, sensors, actuators, structures, mechanisms, wiring, power sources, thermal paths, fluid systems, networks, software processes, data stores, models, people/roles, procedures, facilities, organizations, external services, manufacturing tools, integration rigs, simulators, calibration equipment, training systems, support systems, and disposal services when they bear system responsibility.

**Give elements durable identities and types.** Record definition versus usage/instance, owner, supplier, location, lifecycle, variant/version, parent/composition, allocated logical responsibilities, interfaces, resources, criticality, technology/maturity, assumptions, and evidence. Avoid naming a physical element after a temporary team or delivery sequence. Distinguish a product definition from its serial-numbered instances and deployed copies.

**Allocate logical responsibilities many-to-many.** A logical function may be split across sensor, software, operator, and procedure. One physical processor may host several logical functions. Redundancy maps one logical responsibility to several physical instances. Migration maps it differently by mode or configuration. Record primary/supporting/backup roles, mode applicability, performance allocation, and evidence—not only a Boolean matrix mark.

**Check allocation coverage.** Every required logical function, state responsibility, data ownership, control authority, quality contribution, hazard control, and recovery action needs a physical home. Every physical element needs rationale from a function, quality, constraint, interface, enabling need, or lifecycle obligation. Unallocated logical rows reveal gaps; unjustified physical columns reveal accidental scope or hidden design decisions.

**Map flows to physical paths.** For each logical data, control, material, energy, force, heat, motion, human, and authority interaction, identify source and destination elements, intermediate elements, physical media, locations, interface planes, conversions, protocols, routing, redundancy, and failure behavior. A path may change by mode. Preserve producer–consumer semantics even when a bus, broker, harness, structure, or operator mediates the interaction.

**Partition deliberately.** Group responsibilities with high internal cohesion and govern necessary external coupling. Criteria include shared technology, rates, data, resources, environment, location, latency, safety, security, privacy, fault containment, supplier, certification, manufacture, integration, maintenance, update cadence, ownership, and replaceability. No single criterion dominates every system.

**Define hierarchy without losing peer structure.** Composition/hierarchy supports ownership, procurement, cost, and recursive design. Connectivity graphs show peer interactions. Deployment maps show execution and location. Sequence/state views show behavior. A PBS captures product containment but not all of these relationships. Use linked views with one identity model.

**Choose boundaries for fault and trust.** Physical partitions influence failure propagation, common cause, attack surface, privilege, data exposure, and recovery. Identify fault-containment regions, power domains, network zones, safety partitions, cryptographic boundaries, privacy domains, fire zones, pressure boundaries, structural load paths, and human authority boundaries. Redundancy inside one common dependency may not provide independence.

**Allocate quality properties.** Performance, availability, reliability, maintainability, safety, security, privacy, usability, resilience, manufacturability, sustainability, and cost emerge from relationships. Allocate budgets and design responsibilities without pretending qualities decompose perfectly. Retain system-level scenarios and models to test composition.

**Build resource budgets.** For each applicable configuration/mode, budget mass, center of mass, volume, power, energy, current/inrush, thermal dissipation, cooling, compute, memory, storage, bandwidth, latency, spectrum, staffing, attention, consumables, spares, floor area, and schedule where relevant. Include conversion loss, protocol overhead, wiring, packaging, structure, software services, growth, uncertainty, transient, simultaneous load, fault/degraded operation, and reserve.

**Keep measurement planes consistent.** Power available at a source differs from power delivered after harness/converter loss. Payload bandwidth differs from line rate. component mass differs from installed mass with brackets and cable. Thermal dissipation at a chip differs from heat rejected at a facility boundary. State planes, units, conditions, and inclusions for every budget.

**Analyze spatial architecture.** Define locations, coordinate frames, envelopes, adjacency, separation, routing corridors, access, fields of view, coverage, keep-out zones, thermal zones, vibration, radiation, contamination, acoustics, electromagnetic coupling, fire/pressure zones, human reach, egress, and tool paths. Topology without geometry cannot prove fit, access, or environment compatibility.

**Analyze deployment.** Map software components, data stores, models, keys, policies, human roles, and operational services to processors, devices, clouds, networks, facilities, and organizations. Define startup, migration, failover, scaling, update, rollback, backup, restore, and disconnected behavior. A software component name is not a deployment decision.

**Make configuration explicit.** Define allowable product variants, regional/site differences, optional equipment, redundant trains, maintenance substitutions, software/firmware/data versions, supplier alternates, and operational configurations. Use applicability rules and compatibility matrices. Never create a “complete” diagram by showing mutually exclusive choices simultaneously without notation.

**Include states and dynamic reconfiguration.** Physical architecture changes behavior and sometimes arrangement across startup, normal, degraded, emergency, maintenance, transport, storage, update, recovery, and retirement. Elements may power down, migrate, isolate, connect, release, fold, deploy, or transfer authority. Represent permitted transitions and invariants.

**Assess technology maturity in context.** Evaluate readiness at the intended function, scale, environment, interfaces, manufacture, verification, supply, operations, and support—not in isolation. A laboratory technology may work physically but lack production yield, certification evidence, maintainers, or secure update. Plan maturation and off-ramps.

**Assess heritage and commercial products.** Pin exact model/version/options and compare its guaranteed envelope with the new architecture. Analyze environmental differences, duty cycle, interfaces, modifications, data rights, cybersecurity, safety evidence, obsolescence, supply chain, vendor change, licensing, export/regulatory constraints, repair, and second source. Prior flight or market use is evidence only for its original context.

**Design enabling systems concurrently.** Manufacturing, assembly, transport, integration, test, calibration, deployment, training, operations, maintenance, monitoring, recovery, and disposal systems need interfaces, facilities, schedules, owners, and resources. Long-lead chambers, rigs, tooling, simulators, ground equipment, or qualified staff can determine the feasible product architecture.

**Design assembly and integration.** Define build hierarchy, mating sequence, access, alignment, lifting/handling, cleanliness, power-up, initialization, test points, simulators, fault containment, safe intermediate states, and anomaly isolation. Architecture should permit incremental evidence. A system that can only be tested after final assembly carries avoidable discovery risk.

**Design for verification.** Allocate observability, controllability, instrumentation, test interfaces, emulation, calibration, data capture, configuration identification, and replaceable test doubles. Verification hooks have security, mass, power, cost, and operational implications; control them rather than removing them late or leaving unsafe backdoors.

**Design operation and human work.** Map operator, maintainer, administrator, logistics, safety, support, and emergency responsibilities to physical locations, displays, controls, tools, procedures, staffing, communication, and authority. Evaluate workload, access, protective equipment, training, shift, handoff, and recovery. People are part of the physical realization and organization, not external noise.

**Design maintenance and evolution.** Define line-replaceable boundaries, diagnostics, isolation, access, spares, repair level, calibration, software/data update, key rotation, compatibility, rollback, obsolescence, supplier substitution, and growth. Partition boundaries should align with plausible change and repair where other constraints permit. Excess coupling turns local evolution into system replacement.

**Design retirement.** Identify hazardous energy discharge, data/key disposition, material handling, environmental obligations, supplier/service termination, record retention, reusable elements, facilities, tools, skills, and interfaces for decommissioning. Retirement architecture can influence materials, modularity, data placement, and contracts early.

**Analyze candidate integrity.** For each alternative, run allocation coverage, path continuity, contract compatibility, budgets, scenarios, states/modes, hazards/threats, failure/common-cause, human tasks, spatial fit, assembly, integration, verification, operations, maintenance, update, and retirement reviews. Record counterexamples and unresolved assumptions. One aggregate score should not hide a mandatory failure.

**Prototype decisive uncertainties.** Use breadboards, digital models, emulation, mockups, hardware/software/human-in-the-loop, supplier samples, manufacturing trials, or environmental tests to retire architecture risks. Tie each prototype to a decision, assumption, configuration, method, criterion, result, and limitation. A demonstration is not a production qualification.

**Select with traceable trade reasoning.** Compare feasible alternatives against stakeholder value, mandatory constraints, lifecycle cost, performance, margin, maturity, risk, schedule, integration, supply, operations, and evolution. Analyze sensitivity and uncertainty. Preserve rejected alternatives and decision drivers so later changes can reopen the right question.

**Control resolution and baseline.** Refine until the architecture supports analytical validation, credible cost/schedule/operations models, interface and subsystem definition, integration/verification planning, and the lifecycle review's success criteria. Baseline identities, views, allocations, interfaces, budgets, configurations, assumptions, decisions, and evidence together. Do not baseline detailed drawings before architecture alternatives have been adequately explored.

**Manage changes as architecture changes.** A component, location, supplier, software placement, path, capacity, environment, or maintenance change can alter allocations, interfaces, budgets, hazards, tests, configurations, and enabling products. Traverse dependencies, update all governed views, re-evaluate system scenarios, and rebaseline with rationale.

The following checker finds selected declaration gaps in six physical-element records. It cannot establish architecture adequacy, compatibility, or feasibility.

<!-- bijux-verify: {"id":"physical-element-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"elements_total=6\nwell_formed_declared=1\nmissing_allocations=PE-002\nmissing_location=PE-003\nmissing_interfaces=PE-004\nmissing_owner=PE-005\nmissing_lifecycle=PE-006\nunresolved=PE-002,PE-003,PE-004,PE-005,PE-006\nevidence=declared_fields_only\n","stderr":""}} -->
```python
elements = [
    {"id": "PE-001", "allocations": ["sense temperature"],
     "location": "cargo-zone mount Z3", "interfaces": ["IF-DATA-7", "IF-MECH-2"],
     "owner": "Sensing Product Lead", "lifecycle": ["integration", "operation", "maintenance"]},
    {"id": "PE-002", "allocations": [], "location": "equipment bay B",
     "interfaces": ["IF-PWR-3"], "owner": "Power Lead", "lifecycle": ["operation"]},
    {"id": "PE-003", "allocations": ["retain audit record"], "location": "",
     "interfaces": ["IF-DATA-9"], "owner": "Data Lead", "lifecycle": ["operation", "retirement"]},
    {"id": "PE-004", "allocations": ["remove heat"], "location": "rear plenum",
     "interfaces": [], "owner": "Thermal Lead", "lifecycle": ["operation", "maintenance"]},
    {"id": "PE-005", "allocations": ["authorize recovery"], "location": "operations center",
     "interfaces": ["IF-HUMAN-4"], "owner": "", "lifecycle": ["operation", "recovery"]},
    {"id": "PE-006", "allocations": ["calibrate probe"], "location": "service facility",
     "interfaces": ["IF-CAL-1"], "owner": "Calibration Lead", "lifecycle": []},
]
fields = ("allocations", "location", "interfaces", "owner", "lifecycle")
valid = [element for element in elements if all(element[field] for field in fields)]
print(f"elements_total={len(elements)}")
print(f"well_formed_declared={len(valid)}")
for field in fields:
    print(f"missing_{field}=" + ",".join(e["id"] for e in elements if not e[field]))
print("unresolved=" + ",".join(e["id"] for e in elements if e not in valid))
print("evidence=declared_fields_only")
```

`PE-001` may still be incompatible, under-capacity, inaccessible, or unsupported. Populated metadata is only a structural declaration.

## Definitions and Notation

Let required logical elements (L), physical elements (P), logical interactions (F_L\subseteq L\times L\times K) by kind (K), physical connections (E_P\subseteq P\times P\times K_P), configurations (C), modes (M), and locations (Z).

Allocation matrix:

$$
A_{lp}=1\iff \text{physical element }p\text{ realizes or supports logical responsibility }l.
$$

Coverage indicator:

$$
Coverage_L=\frac{|\{l\in L_{required}:\sum_p A_{lp}\ge1\}|}{|L_{required}|}.
$$

(Coverage_L=1) proves only that every listed logical row has an allocation mark. It does not prove the logical set is complete, allocation is feasible, responsibility is sufficient, or qualities compose.

For physical element (p), resource (r), configuration (c), and mode (m):

$$
D_r(p,c,m)=\sum_l A_{lp}d_r(l,p,c,m)+o_r(p,c,m),
$$

$$
Margin_r(p,c,m)=Cap_r(p,c,m)-Reserve_r(p,c,m)-D_r(p,c,m).
$$

Nonnegative margin is necessary for that modeled budget. Capacity, demand, overhead, and reserve require compatible planes, units, conditions, and simultaneity rules.

For component masses (m_i) at positions (x_i) along one controlled axis:

$$
m_{total}=\sum_i m_i,\qquad x_{cm}=\frac{\sum_i m_i x_i}{\sum_i m_i}.
$$

Installed masses must include brackets, harness, fluids, fasteners, insulation, and uncertainty if those lie inside the budget plane.

Logical flow (f=(l_s,l_t,k)) is physically realized only if allocated endpoints and a compatible physical path exist:

$$
Realized(f)\iff\exists p_s,p_t:\ A_{l_sp_s}=1\land A_{l_tp_t}=1
\land CompatiblePath_k(p_s,p_t,c,m).
$$

Let trace relations include:

$$
allocates\subseteq L\times P,\quad deploysTo\subseteq Software\times P,
\quad locatedAt\subseteq P\times Z,
$$

$$
connects\subseteq P\times P,\quad verifies\subseteq Evidence\times(P\cup E_P).
$$

Architecture consistency requires views to refer to the same identities and applicable configurations. It is not inferred merely because every relation is individually well-typed.

## Mechanisms, Invariants, or Proof Structure

The core synthesis mechanism is allocate–connect–budget–challenge–select–baseline:

1. frame the architecture scope and preserve logical/contract independence;
2. generate candidate physical elements, partition strategies, locations, paths, technologies, and configurations;
3. allocate logical responsibilities, qualities, and authority to physical elements;
4. map interactions to physical paths and controlled interfaces;
5. construct resource, spatial, human, lifecycle, supplier, integration, and verification models;
6. challenge nominal, boundary, fault, degraded, maintenance, and change scenarios;
7. compare feasible alternatives and collect decisive evidence;
8. select, justify, refine, and baseline the coherent model at appropriate resolution.

**Coverage invariant.** Every required logical responsibility, flow, quality contribution, hazard control, and recovery behavior has an accountable physical realization or a governed unresolved disposition.

**Rationale invariant.** Every physical element exists because it realizes a function, quality, interface, constraint, enabling need, or lifecycle obligation. Inventory inheritance is not sufficient rationale.

**Identity invariant.** Hierarchy, connectivity, spatial, deployment, behavior, budget, lifecycle, and configuration views use the same physical identities or controlled mappings among definition, usage, and instance.

**Path invariant.** Every logical interaction has a physical path whose endpoints, intermediate transformations, contracts, capacity, failure behavior, and mode applicability support the intended semantics.

**Budget invariant.** For every relevant configuration/mode/extreme, demands plus overhead plus controlled reserve fit available capacity at consistent planes. Negative margin is a counterexample, not a negotiation result.

**Boundary invariant.** Physical, fault, trust, safety, privacy, supplier, organizational, and environmental boundaries align with allocated authority and interface control or their crossings are explicitly engineered.

**Configuration invariant.** Every claimed architecture property and evidence result applies to an identified, permitted set of element versions, options, locations, and connections. Incompatible alternatives never coexist accidentally in one baseline.

**Lifecycle invariant.** The architecture can be produced, assembled, integrated, verified, transported, stored, deployed, operated, maintained, updated, recovered, and retired with identified enabling systems and safe intermediate states.

**Human invariant.** Human roles, locations, information, controls, tools, access, staffing, training, workload, authority, and recovery are part of the physical architecture and are feasible for the declared population and environment.

**Evidence invariant.** Feasibility and conformance claims name model/article, configuration, method, environment, instruments/data, criterion, result, anomalies, and limitations. Heritage and prototype evidence is not silently generalized.

Adversarial review constructs counterexamples: unallocated function; connected diagram with no compatible path; simultaneous peak demand; single common resource defeating redundancy; hidden conversion; failed startup order; maintenance access blocked; operator in the wrong location; network partition; supplier change; environmental extreme; mixed versions; unavailable test facility; unsafe intermediate assembly; recovery without authority; or retirement with live energy/data. One counterexample invalidates the corresponding universal claim.

## Alternatives and Trade-Offs

**Centralized versus distributed.** Centralization simplifies coordination, consistency, and management but can create latency, bandwidth, scale, and common-failure concentration. Distribution improves locality and resilience but adds synchronization, versioning, security, resource duplication, and operational complexity.

**Hardware versus software versus human realization.** Hardware can provide deterministic speed and isolation; software offers adaptability and update; humans offer judgment and novel recovery. Each brings failure, assurance, resource, lifecycle, and interface costs. Hybrid allocation must define authority and transitions.

**Integrated versus modular packaging.** Integration can reduce size, mass, connectors, and unit cost while increasing coupling, repair scope, qualification impact, and supplier dependence. Modularity improves replacement/evolution and parallel work but adds interfaces, packaging, overhead, and potential performance loss.

**Active versus passive implementation.** Active control adapts and optimizes but needs sensing, power, software, authority, and fault handling. Passive structures, cooling, or safety features can be simple and robust but less flexible or heavier. Prefer the architecture that meets lifecycle outcomes, not the one with more technology.

**Dedicated versus shared resources.** Shared compute, networks, power, cooling, data, facilities, or operators improve utilization but create contention, interference, security, change coupling, and common cause. Dedicated resources isolate but add cost and idle capacity. Explicit allocation and arbitration are essential.

**Local versus remote service.** Remote/cloud elements offer scale and centralized evolution but depend on networks, identity, latency, jurisdiction, vendor, and outage response. Local elements support autonomy but require deployed resources, synchronization, update, and field support. Mode-dependent hybrid designs need explicit source of truth.

**Custom versus commercial/heritage.** Existing products reduce initial development but constrain interfaces, evidence, supply, change authority, and lifecycle. Custom design improves fit and control but adds development, maturity, verification, and production risk. Compare total architecture consequences.

**Physical redundancy versus diversity.** Replication improves availability only if common causes and shared paths are controlled. Diversity can reduce common design faults but adds integration, maintenance, spares, training, and behavior differences. Define failure independence rather than counting boxes.

**Worst-case margin versus adaptive capacity.** Static margin is simple and auditable but costly. Dynamic scheduling, load shedding, scaling, or reconfiguration uses capacity efficiently but adds monitors, control, latency, and failure modes. Critical guarantees need behavior when adaptation fails.

**Early detail versus option preservation.** Detailed choices improve estimates and supplier engagement but can prematurely lock architecture. Abstract candidates preserve options but may hide physical infeasibility. Increase resolution around irreversible/high-risk decisions and record open parameters with bounds.

## Failure Modes and Misconceptions

**“Physical means hardware.”** Software deployments, data stores, people, procedures, facilities, organizations, and external services can be essential realized elements.

**“The PBS is the architecture.”** It represents containment/ownership hierarchy. Architecture also needs peer connections, paths, locations, behavior, deployment, modes, configurations, and principles.

**“One function belongs in one component.”** Allocation can be split, shared, replicated, migrated, or jointly realized by technology and people. The mapping must preserve accountability.

**“If every function is allocated, the architecture is complete.”** Paths, qualities, resources, faults, lifecycle, environments, and enabling systems may still fail.

**“A line between boxes is an interface.”** It omits endpoints, planes, semantics, medium, conversions, capacity, timing, failure, ownership, and evidence.

**“Nominal budgets close.”** Transients, overhead, uncertainty, concurrent demand, fault/degraded operation, path loss, growth, and reserve can create negative margin.

**“Reuse is low risk.”** New context, environment, load, modification, interfaces, supplier, evidence, security, and support can erase heritage benefits.

**“Redundant boxes are independent.”** They may share power, clock, cooling, network, software, data, location, supplier, maintenance action, or operator.

**“Cloud is a location.”** Region, zone, account, tenancy, network path, identity, data jurisdiction, control plane, version, capacity, and failure domain require specification.

**“People are external users.”** Operators, maintainers, installers, administrators, trainers, and support staff realize allocated functions and interact with physical environments and tools.

**“Detailed CAD proves architecture.”** It may prove geometry for one configuration while allocations, contracts, states, quality, supplier, operation, and evolution remain incoherent.

**“The selected alternative no longer needs rationale.”** Preserved trade evidence supports reviews and lets later changes reopen the correct decision rather than repeat history.

**“Baseline means immutable.”** It means changes are controlled, assessed, approved, communicated, and traceable.

## Worked Examples

### Example 1

**Edge–cloud–human allocation.** A fleet-monitoring logical architecture includes sense, filter, detect anomaly, control locally, aggregate history, optimize fleet, authorize maintenance, and audit. One candidate places everything in cloud services. Network loss would remove local control and anomaly response.

The selected physical architecture places sensing, filtering, essential control, bounded history, and safe degradation on an edge controller; fleet aggregation/optimization in regional services; authorization across local safety rules and a remote maintenance role; durable audit in replicated stores; and recovery in edge/cloud procedures. The allocation matrix is mode-specific. Data synchronization, identity, time, update, fallback, and human authority paths are controlled. Distribution follows outcome and fault requirements, not fashion.

### Example 2

**Redundant sensing with hidden common cause.** A safety function is allocated to two identical sensors and a voter. Initial reliability review counts two sensors. Physical review reveals both share one mounting bracket, connector, harness route, power converter, calibration procedure, and software driver.

The architecture separates mounting locations and harness routes, assigns independent power domains, diversifies sensing principles where justified, isolates drivers, adds disagreement monitoring, and controls common calibration evidence. Some dependencies remain shared and are modeled. Redundancy is described by failure independence and coverage, not “two of everything.”

### Example 3

**Mass and center of mass.** Three installed elements lie along axis x: battery 40 kg at 0.5 m, controller assembly 20 kg at 1.5 m, and payload with bracket 60 kg at 2.0 m. Total mass is 120 kg and:

$$
x_{cm}=\frac{40(0.5)+20(1.5)+60(2.0)}{120}
=\frac{170}{120}=1.4167\text{ m}.
$$

If the allowable center is 1.2–1.4 m, the candidate exceeds the upper bound by about 0.0167 m despite meeting total mass. Moving the controller is not necessarily sufficient; cable mass, uncertainty, other axes, dynamic fluids, and attachment loads belong in the real model. A scalar budget exposes the architecture issue early.

### Example 4

**Compute and power capacity by mode.** A node provides 100 compute units and 500 W. Reserve allocations are 15 compute and 50 W. In normal mode, functions demand 70 compute plus 8 overhead and 390 W plus 25 W conversion/cooling allocation. Margins are 7 compute and 35 W. During recovery, demand becomes 86 compute plus 8 overhead and 430 W plus 25 W.

Recovery margins are (100-15-94=-9) compute and (500-50-455=-5) W. Nominal architecture closes; recovery fails. Options include moving diagnostics, sequencing recovery, adding capacity, reducing reserve with justification, or changing recovery guarantee. The architecture cannot average normal and recovery modes.

### Example 5

**Heritage controller in a new environment.** A controller has operated successfully indoors. A new architecture places it near a motor in an outdoor enclosure. Interfaces appear identical.

Context review finds wider temperature/humidity, condensation, vibration, electromagnetic susceptibility, dirt, different grounding, higher duty cycle, remote updates, inaccessible reset, and a vendor end-of-support date. The team adds environmental enclosure/control, routing and bonding, remote recovery, qualification, spares, and an obsolescence off-ramp—or selects another element. “Heritage” informed evidence selection but did not waive new-context compatibility.

### Example 6

**Human and procedure as physical realization.** A logical `isolate hazardous energy` function was assigned to a breaker. The breaker interrupts power but does not identify sources, secure against re-energization, verify zero energy, or coordinate multiple workers.

The physical architecture includes disconnect hardware, lock/tag points, labels, test instrument, maintainer role, authorization, procedure, lighting/access, protective equipment, training, and shift handoff. Interface identities connect equipment and work system. Human-in-the-loop maintenance evaluation and electrical verification address the full allocation. The breaker is necessary but not the complete physical element set.

### Example 7

**Physical path and routing.** A logical camera-to-processor flow needs 800 Mbit/s and 20 ms freshness. A 1 Gbit/s link seems adequate. The physical path includes camera serialization, two switches, encryption gateway, shared trunk, and processor queue. At peak, other allocated traffic is 300 Mbit/s; protocol/security overhead consumes 12%; routing crosses a high-interference cable corridor.

Payload capacity, latency, jitter, buffer, retransmission, EMI, power, connector, route length, and fault path are modeled at each plane. The shared trunk cannot carry 800+300 Mbit/s before overhead on a 1 Gbit/s raw link. The architecture adds a dedicated high-rate path or changes compression/rate with verified image-quality impact. A line labeled 1 GbE was not a capacity proof.

### Example 8

**Maintenance-driven partition.** An integrated electronics module minimizes mass and connectors but contains a high-failure fan beside long-life avionics. Replacing the fan removes the complete certified module, disconnects many interfaces, and causes lengthy recalibration.

An alternative isolates the fan tray as a line-replaceable element with keyed power/control, guarded access, diagnostic identity, filter service, and safe hot/cold replacement rules. It adds connector mass and interfaces but reduces downtime, spares cost, and certification scope. The trade uses failure rate evidence, mission access, replacement time, interface reliability, and lifecycle cost rather than assuming modularity is always better.

### Example 9

**Variant and configuration control.** Regional variants use different radio modules and power supplies. A single architecture diagram shows both radios and both supplies, making reviewers assume four physical elements coexist. Software deployment also supports only specific radio firmware.

The architecture defines common platform elements plus Variant R1 and R2 applicability, exact radio/power/interface pairs, firmware compatibility, regional constraints, factory configuration, field identification, test sets, spares, and transition rules. Common requirements trace to both; variant requirements and evidence remain separate. Generated views show one valid configuration at a time.

### Example 10

**Integrated cold-storage architecture.** Requirements call for cargo temperature control through network loss, auditable history, safe maintenance, and 15-year service. Candidate architecture includes redundant probes, edge controller, compressor/power electronics, refrigerant/airflow paths, insulation, local display, gateway, cloud analytics/store, operator and technician roles, calibration rig, spares, update service, and disposal process.

Logical allocation, physical paths, state/mode behavior, power/thermal/network/storage budgets, probe independence, control contracts, cybersecurity, alarm workload, enclosure fit, service access, supplier support, integration order, test points, calibration, disconnected operation, data reconciliation, recovery, and refrigerant/end-of-life obligations are linked. Cold-chamber and network-fault prototypes retire decisive assumptions. The selected baseline records variants, margins, residual risks, and enabling-facility commitments. That coherent evidence set—not the block diagram alone—is physical architecture.

## Cross-Program Connections

**Platform engineering.** Physical platform architecture maps control planes, data planes, identity, observability, deployment automation, people, regions/zones, networks, compute, storage, and vendor services into fault and trust domains. Logical services must map to real capacity and operational ownership.

**API and service engineering.** Service boundaries become deployed processes, queues, databases, gateways, networks, certificates, schemas, and operator procedures. Latency, availability, consistency, and security depend on physical paths and configurations.

**Data engineering.** Logical datasets and transformations map to stores, compute engines, partitions, regions, networks, catalogs, keys, schedulers, and recovery infrastructure. Data gravity, locality, replay, retention, privacy, and cost are physical-architecture concerns.

**Object-oriented programming.** Classes and interfaces describe software structure, but runtime objects, processes, nodes, storage, networks, threads, and resource limits determine deployment behavior. Software abstraction does not erase physical constraints.

**Functional programming.** Pure transformations support logical reasoning, while execution still requires processors, memory, data movement, schedulers, effects, services, and operators. A physical architecture realizes the effectful system around functional cores.

**Security and safety.** Trust zones, privilege, key custody, network boundaries, hazardous-energy paths, fault containment, redundancy, monitoring, safe states, and recovery are architectural allocations. Controls added after partitioning may be infeasible.

**Manufacturing and supply.** Material, process, tolerances, tooling, facilities, lead times, suppliers, yield, inspection, data rights, and obsolescence influence feasible partitions and baselines.

**Operations and sustainment.** Locations, staffing, procedures, spares, diagnostics, access, updates, monitoring, support contracts, recovery, and retirement are part of the realized system and drive lifecycle value.

## References

1. NASA, *Systems Engineering Handbook, Section 4.4: Design Solution Definition*, current web edition, updated 2023. <https://www.nasa.gov/reference/4-4-design-solution-definition/>
2. NASA, *Systems Engineering Handbook, Section 4.3: Logical Decomposition*, current web edition, updated 2023. <https://www.nasa.gov/reference/4-3-logical-decomposition/>
3. NASA, *Systems Engineering Handbook, Section 5.2: Product Integration*, current web edition, updated 2023. <https://www.nasa.gov/reference/5-2-product-integration/>
4. NASA, *Systems Engineering Handbook, Section 6.3: Interface Management*, current web edition, updated 2023. <https://www.nasa.gov/reference/6-3-interface-management/>
5. NASA, *Systems Engineering Handbook, Appendix R: HSI Plan Content Outline*, current web edition, updated 2023. <https://www.nasa.gov/reference/appendix-r-hsi-plan-content-outline/>
6. BKCASE Editorial Board, *SEBoK: Physical Architecture*, current online edition. <https://sebokwiki.org/wiki/Physical_Architecture>
7. Object Management Group, *Systems Modeling Language Version 2.0*, formal specification, 2025. <https://www.omg.org/spec/SysML/2.0>
8. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2022. <https://www.iso.org/standard/74393.html>
9. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>

## Exercises

### Exercise 1

A logical architecture has responsibilities (L_1) sense, (L_2) estimate, (L_3) decide, (L_4) actuate, (L_5) audit, and (L_6) recover. Candidate physical elements allocate: sensor (P_1:\{L_1\}); controller (P_2:\{L_2,L_3\}); actuator (P_3:\{L_4\}); cloud store (P_4:\{L_5\}). Compute declared logical coverage and identify the structural gap. Then propose at least two physically different allocations for recovery and discuss their consequences.

### Exercise 2

A compute node has capacity 160 units and reserve 20. In degraded mode, allocations demand 55, 42, 28, and 18 units, with platform overhead 10. Compute margin. A proposal moves the 18-unit function away but adds 6 units of communication/security overhead locally. Recompute and state what the arithmetic does not establish.

### Exercise 3

Four installed masses lie on one axis: 30 kg at 0.2 m, 25 kg at 1.0 m, 45 kg at 1.8 m, and 10 kg at 2.4 m. Compute total mass and center of mass. The allowed interval is 1.0–1.3 m. Determine margin to each bound and name missing physical evidence.

### Exercise 4

Critique a “physical architecture” consisting only of a PBS with `System -> Sensor Subsystem, Compute Subsystem, User Interface Subsystem`. Identify at least twelve missing views, relations, or analyses needed before it supports an architecture baseline.

### Exercise 5

Design a review strategy for two candidate emergency-notification physical architectures: centralized cloud control versus local site control with cloud coordination. Cover allocation, paths, modes, resource budgets, fault/trust boundaries, people, enabling systems, integration, evidence, and decision criteria. State how you would avoid prematurely declaring either universally superior.

## Answers to the Exercises

### Answer 1

Five of six listed logical responsibilities have at least one allocation:

$$
Coverage_L=5/6\approx0.8333=83.33\%.
$$

(L_6) recover is unallocated. The matrix also needs flows, qualities, modes, and feasibility; 83.33% is only row declaration coverage.

One allocation places recovery logic, configuration snapshot, and watchdog in a separate local safety controller, with technician authority/procedure and local display. This can recover during network loss and isolate failure from the main controller, but adds hardware, power, interfaces, state synchronization, qualification, and maintenance.

Another allocation places recovery orchestration in the existing controller with a minimal immutable recovery partition plus cloud-held backups and remote operator authorization. It reduces hardware but shares processor/power failure and depends on network/cloud for some cases. A hybrid may keep safe-state/local rollback at site while cloud/operator handles restoration. Select by hazards, failure independence, response time, trust, staffing, connectivity, update, and lifecycle evidence—not by allocating the word `recover` to one box.

### Answer 2

Initial demand plus overhead is:

$$
D=55+42+28+18+10=153.
$$

Available capacity after reserve is (160-20=140), so:

$$
Margin=160-20-153=-13.
$$

The degraded-mode architecture is over capacity by 13 units. After moving the 18-unit function and adding 6 units local overhead:

$$
D'=55+42+28+10+6=141,
$$

$$
Margin'=160-20-141=-1.
$$

It still does not close. The arithmetic also does not establish that demands peak simultaneously, capacity is sustained in the degraded environment, units are commensurate, scheduling/latency works, memory/network/power fit, communication failure is handled, remote capacity exists, security is sufficient, or reserve is correctly justified. Moving computation changes paths and contracts.

### Answer 3

Total mass is:

$$
m=30+25+45+10=110\text{ kg}.
$$

First moment is:

$$
30(0.2)+25(1.0)+45(1.8)+10(2.4)=6+25+81+24=136\text{ kg m}.
$$

Thus:

$$
x_{cm}=136/110=1.23636\text{ m}.
$$

Margin above the 1.0 m lower bound is about 0.23636 m; margin below the 1.3 m upper bound is about 0.06364 m. The nominal one-axis result fits.

Missing evidence includes installed brackets/harness/fluids/fasteners, mass and position tolerances, other axes, changing consumables or moving parts, configurations, thermal deformation, dynamic loads, coordinate datum, measurement uncertainty, supplier mass growth, and verified as-built properties. The small upper margin may be consumed by uncertainty.

### Answer 4

The PBS identifies three containment branches but omits, at minimum:

1. logical-to-physical allocation;
2. end-to-end behavior and state/mode responsibility;
3. peer physical connections and controlled interface identities;
4. data, control, power, thermal, mechanical, human, and environmental paths;
5. locations, spatial envelopes, routing, access, and environment zones;
6. software/data deployment to execution and storage nodes;
7. people, procedures, facilities, organizations, and external services;
8. fault-containment, common-cause, redundancy, and recovery architecture;
9. trust, privilege, privacy, key, and supplier boundaries;
10. resource/performance budgets, overhead, uncertainty, reserve, and modes;
11. product variants, versions, options, and compatibility;
12. manufacturing, assembly, integration order, safe intermediate states, and test points;
13. verification/validation methods and evidence state;
14. operations, maintenance, diagnostics, spares, updates, and rollback;
15. enabling systems for test, calibration, training, support, and disposal;
16. assumptions, decisions, alternatives, rationale, risks, and change authority.

The PBS remains useful for product ownership and recursive definition, but it must link to these architecture views rather than be renamed as a complete architecture.

### Answer 5

First hold scope constant: sites, hazards, notification outcomes, message classes, latency/availability, population, regions, lifecycle, cost horizon, regulatory/privacy constraints, and evidence maturity. Build two internally coherent candidates rather than a detailed favorite and vague straw alternative.

For each candidate:

- allocate detection, policy, authorization, composition, delivery, acknowledgement, audit, monitoring, support, and recovery across site hardware/software, cloud services, operators, and procedures;
- map identity, time, command, message, status, evidence, power, and human paths with planes, latency/capacity, versions, and failure behavior;
- analyze normal, network loss, cloud/site outage, degraded power, clock/identity failure, emergency override, maintenance, update, recovery, and regional disaster modes;
- budget compute, storage, bandwidth, queue, latency, power, battery, staffing, attention, and reserve under simultaneous emergencies;
- identify site, region, account, network, supplier, software, power, operator, and physical common causes; trust/privacy and command-authority boundaries;
- define operator/site maintainer/support roles, locations, workload, training, communication, and handoff;
- include simulators, test tenants, notification endpoints, load/fault injection, backup communication, deployment/update services, training facilities, and long-term support;
- plan incremental integration and verification using emulators, site pilots, failure injection, human-in-the-loop scenarios, security testing, and representative regional trials;
- retain exact assumptions, models, versions, raw results, anomalies, and evidence limits.

Decision criteria include mandatory safety/regulatory constraints, delivery and recovery outcomes, local autonomy, global consistency, latency, availability, correlated failures, security/privacy, scalability, operating burden, lifecycle cost, supplier control, maintainability, deployment, and evolution. Sensitivity analysis should vary connectivity, site count, staffing, incident concurrency, and cloud/site failure. A hybrid may dominate in some contexts. The decision should state the chosen operational envelope and residual risks, not claim centralized or local control is universally superior.
