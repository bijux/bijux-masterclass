---
module_id: SYSENG-054
program: Systems Engineering
level: 2
module_number: 54
title: Structure Models
status: complete
last_verified: 2026-08-31
---

# Structure Models

## One-Page Review

### Governing question

How can engineers represent system context, kinds, configured usages, composition, interfaces, connections, allocation, deployment and variants precisely enough to support design and integration—without mistaking hierarchy, diagram placement or type compatibility for a complete or correct architecture?

### Essential definitions

- A **structure model** is a governed semantic representation of system elements, kinds/definitions, usages/instances, properties, containment, references, interfaces, connections and allocations for a declared boundary, configuration and concern.
- A **definition/type** specifies reusable characteristics and constraints of a kind of element. A **usage/instance** applies a definition in a particular owning context, role, multiplicity and configuration.
- A **system context** identifies the system of interest, external actors/systems/environments, boundary and exchanges. External does not mean irrelevant or uncontrolled.
- **Composition/containment** establishes lifecycle/identity ownership of a part or nested usage by a whole. It is not the same as visual nesting, classification or organizational reporting.
- A **reference** points to an element owned elsewhere without transferring ownership; references require identity and configuration semantics.
- A **port** is a modeled interaction point on an owning occurrence/part. Its features specify what can be exchanged and, where applicable, direction, protocol, quantity, units and constraints.
- An **interface** is a governed agreement across a boundary, including exchanged items/energy/information, physical/logical characteristics, behavior, timing, quality, responsibility, assumptions and verification—not a connector line alone.
- A **connection/connector** relates endpoints so interaction is permitted under defined compatibility and topology. Assembly connects peer parts; delegation binds an outer boundary feature to an inner part feature.
- An **item flow** states what traverses a connection, with source/destination, type/schema/quantity, direction and conditions.
- **Multiplicity/cardinality** states how many usages or endpoints may exist in a configured context; it does not select actual serial-numbered instances by itself.
- **Allocation** maps functions, requirements, resources, risks or responsibilities to structural elements. It neither changes containment nor proves adequacy.
- A **logical structure** groups solution-independent responsibilities and interactions; a **physical/deployment structure** identifies realized hardware, software, people, facilities, locations or nodes. Their mapping is many-to-many.
- A **failure/trust boundary** groups elements sharing failure exposure or authority/security assumptions; it may cut across product hierarchy.
- A **configured structure** resolves variants, multiplicities, versions, suppliers, deployment and external dependencies for a baseline or individual product.

### Central model, mechanism, or theorem

Represent configured structure as a typed attributed multigraph

\[
G_S=(V,E_C,E_R,E_K,E_A,P,\Gamma),
\]

where $V$ are elements/usages, $E_C$ containment, $E_R$ references, $E_K$ connections, $E_A$ allocations, $P$ ports/properties and $\Gamma$ configuration/applicability.

For ordinary composition, each non-root owned usage has one owner and containment is acyclic:

\[
\forall v\ne root:\ |parent_C(v)|=1,\qquad (V,E_C)\text{ is acyclic}.
\]

For connection $k=(p_i,p_j)$, structural compatibility is a predicate over direction, item type, units, protocol, multiplicity, state/mode and configuration:

\[
Compatible(k,\Gamma)=D\land T\land U\land Q\land M\land C.
\]

Compatibility is necessary for integration but does not prove performance, safety, security, timing, reliability or operational effectiveness.

### Critical invariants

- Every view names the system/entity of interest, concern, boundary, lifecycle, configuration, abstraction, viewpoint/model kind and authoritative source.
- Definitions and usages/instances are distinguishable; changing a type does not silently redefine every configured usage without impact review.
- Each composed usage has one lifecycle/identity owner in a configuration, containment is acyclic, and references do not masquerade as ownership.
- The structure includes hardware, software, people, procedures, facilities, data/services, suppliers and enabling products as required by the concern—not hardware boxes alone.
- External actors, services, environments and dependencies remain explicit with owned versus assumed responsibilities.
- Ports/interfaces identify endpoints, direction, exchanged items, semantics, units, timing/quality, responsibility, state/mode and verification obligations.
- Assembly and delegation semantics are distinct; connection lines do not imply unmodeled protocols or physical paths.
- Logical, physical, deployment, organizational, trust, failure and product-breakdown views are related but never conflated.
- Functional/behavioral allocation is complete enough for the declared scope, includes shared/integration responsibility and exposes unallocated or overconcentrated behavior.
- Multiplicity, redundancy, voting, replication and failover express configured topology and common-cause assumptions rather than decorative duplicate boxes.
- Variants and options use explicit applicability/configuration rules; copied diagrams do not become independent authorities.
- Model checks detect duplicate identity, orphan elements, containment cycles, invalid endpoints, direction/type/unit/protocol mismatch, unresolved multiplicity and prohibited cross-boundary connections.
- Structure baselines align with requirements, behavior, interfaces, budgets, hazards, verification and as-built/as-deployed configuration.
- Model completeness and interface compatibility remain bounded claims; integration and operational evidence can contradict the structure model.

### Common failures

Common failures include treating a block diagram as a bill of material; confusing type with instance; using composition for every association; giving one element two containment parents; encoding reporting lines as product hierarchy; omitting external dependencies; placing items near each other instead of connecting ports; drawing connectors without exchanged items or contracts; using bidirectional arrows to avoid ownership; copying interface properties into both endpoints; confusing delegation with peer assembly; assuming compatible types imply compatible behavior; allocating a function to a box and declaring it satisfied; hiding integration responsibility between components; modeling redundancy without failure independence; collapsing logical, physical and deployment structures; ignoring people/procedures/facilities; letting variants drift in copied diagrams; importing supplier components without identity/version; and reconciling an as-built mismatch by silently changing the design model.

### Compact example

An emergency-water system owns controller, pump, sensor and power usages and relates to an external environment. Thirteen ports and eight typed connections represent two external boundary exchanges, two parent-to-child delegations and four internal assembly connections. A checker confirms one containment parent, no cycle, valid endpoints, type/direction rules and four function allocations. It cannot establish pipe size, electrical margin, protocol timing, common-cause failure, environmental suitability or that the allocated elements actually perform their functions.

### Connections

SYSENG-051 governs authority, SYSENG-052 defines obligations and SYSENG-053 defines behavior. Structure assigns configured performers and interaction points. SYSENG-055 adds quantitative constraints; SYSENG-056–060 add language, trace, consistency, simulation, review and tool integration. Earlier system boundary, architecture, interface, modularity, integration, risk and verification modules provide the engineering questions behind each structural view.

## Governing Question

For a selected baseline, can an engineer identify every relevant internal and external element, distinguish reusable definition from actual role/instance, determine ownership and configuration, traverse every governed interaction through explicit endpoints, and explain how behavior, requirements, resources and risks are allocated—without relying on diagram geometry or tribal knowledge?

If not, the drawing may communicate a concept but cannot yet govern integration. A strong structure model is not the most detailed picture; it is a coherent semantic graph whose views answer stakeholder concerns and whose configured claims survive interface and realization evidence.

## Why This Matters

Many costly failures occur between well-designed components. The wrong physical connector fits, two services interpret the same field differently, a shared power or identity provider defeats redundancy, an operator or facility was absent from the boundary, or a logical responsibility has no deployed owner. Structure models make those interaction and ownership assumptions reviewable before assembly and operation.

NASA defines a system as hardware, software, equipment, facilities, personnel, processes and procedures working together. Logical Decomposition creates structural relationships across these elements and allocates functions down the product structure. Design Solution Definition turns logical models and requirements into alternative and selected designs with external and end-product interface specifications. Interface Management requires origin, destination and physical, electrical, mechanical, data, logical and human characteristics to remain controlled across parties and lifecycle.

NASA-HDBK-1009A supplies current system-model planning, metamodel and construction guidance. SysML 2.0 distinguishes definitions and usages and defines ports as connection points whose features specify exchanges. ISO/IEC/IEEE 42010:2022 distinguishes architecture from its description and governs viewpoints/model kinds around stakeholder concerns. These semantics enable precision, but the project must still govern meaning, configuration and evidence.

## Prerequisites and Retrieval

Before constructing a structure model, retrieve:

1. system/entity of interest, context/boundary, lifecycle, ConOps, scenarios, external actors/systems/environments, stakeholders and enabling systems;
2. baselined requirements, functions/behaviors/states/modes, qualities, hazards/threats, decisions and architecture alternatives;
3. logical, product, physical, software, data, deployment, organizational, trust/failure and operations structures with ownership;
4. interface agreements/requirements, ports/endpoints, exchanged item definitions, units, schemas, protocols, timing/quality, responsibilities and versions;
5. function/requirement/resource/risk/verification allocations, budgets, margins, shared responsibilities and integration ownership;
6. variants/features/options, multiplicities, redundancy/voting/failover, suppliers, part/software versions and as-built/as-deployed instances;
7. modeling language/profile/metamodel, libraries, namespaces/IDs, connection/compatibility rules, validation/generation and configuration baselines;
8. integration/test results, nonconformances, operational inventory/telemetry, interface incidents, shadow diagrams and known structure debt.

Use a retrieval test: “Two redundant controllers connect to a shared bus.” Ask whether these are definitions or configured usages; who owns them; power, clock, network, software, sensor, operator and update dependencies; port/protocol/item semantics; arbitration/voting/failover; state/timing; physical deployment; common-cause zones; exact versions; and tests. Duplicate boxes and two lines do not establish redundancy.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish definitions/types, usages/roles, configured instances and realized serial/deployed items;
2. model system context, internal composition, references and external dependencies with stable identity;
3. define ports, interfaces, item flows, connections and delegation with explicit semantics;
4. relate logical, physical, deployment, organizational, trust, failure and product structures without conflation;
5. allocate behavior, requirements, resources, risk and verification responsibility to structure;
6. model multiplicity, variants, redundancy, shared services and common-cause exposure;
7. check containment, endpoints, direction, type, units, multiplicity, configuration and boundary rules;
8. integrate supplier and enabling-system structure with contracts, rights, versions and exit paths;
9. reconcile design structure with as-built/as-deployed evidence through controlled change;
10. communicate structural conclusions with explicit concern, scope, assumptions, evidence and limitations.

## Core Exposition

**Start with context.** Define system of interest and external entities before internal decomposition. Name what crosses the boundary and who controls each side. Include natural/induced environment and organizations or services that can affect outcomes. A boundary is an engineering decision with lifecycle and responsibility consequences.

**Choose a concern and viewpoint.** Context, logical responsibility, product breakdown, physical assembly, software/service composition, deployment, trust, failure and organization answer different questions. State model kind and view-selection rule. Do not pile them into one diagram whose lines mean several things.

**Distinguish definitions from usages.** A definition describes a reusable kind such as `Pump`. A usage `primaryPump: Pump` has an owning context, role, multiplicity, property values and configuration. Two usages of one definition are not the same item. A realized serial-numbered pump adds manufacturing/maintenance identity and evidence.

**Model composition deliberately.** Use containment when the whole owns the part's identity/lifecycle in the modeled context. Enforce one owner and acyclicity. Use reference for shared/external elements, allocation for responsibility, and association for other relations. Visual nesting must render semantic containment, not create it accidentally.

**Use stable identity and namespaces.** Names such as “controller” repeat across levels and variants. Give definitions, usages, ports, interfaces and connections stable IDs; manage rename, split, merge and retirement. Pin external references to compatible configurations. Never reuse an ID for a different element.

**Treat hierarchy as one projection.** Product structures help acquisition, integration and configuration, but real dependency, information, trust and failure graphs cross branches. Preserve both hierarchy and crosscutting relationships. Avoid forcing shared services or people into misleading product ownership merely to make a tree.

**Include all necessary element kinds.** A complete concern may require hardware, software, data, models, humans, procedures, facilities, networks, suppliers and support/maintenance/test equipment. Treat operators as participating performers with interfaces, not labels outside the border. Include lifecycle-enabling products when they determine realization or support.

**Define ports as owned interaction points.** Name port role, direction relative to owner, item/energy/information types, multiplicity, protocol, units, quality/timing, security/classification and state/mode availability. Separate provided/required capabilities where useful. Port compatibility is richer than matching names.

**Model interfaces as agreements.** An interface includes endpoints and authority plus physical form/fit, electrical/thermal/fluid, data schema/encoding, behavior/protocol, timing, error/recovery, quality, security/privacy, human use, environmental constraints and verification. Store authority once and derive endpoint views; do not maintain two contradictory copies.

**Use assembly and delegation correctly.** Assembly connects interaction points of peer parts. Delegation connects a boundary port of a whole to a port of an internal part, with direction interpreted relative to each owner. Define transformation or routing elements when delegation is not identity-preserving. Do not draw a line across boundary and assume semantics.

**State item flows.** For each connection identify possible/required exchanged items, direction/source/destination, schema/type/quantity, units, rate/volume, classification, freshness and modes. One physical bus may carry many logical flows; one logical flow may traverse several physical connections. Preserve mappings.

**Check connection compatibility.** Validate endpoints exist in the configured baseline; directions are permitted for assembly/delegation/external context; types/schema/units and protocols match or have an explicit adapter; multiplicities/capacity allow topology; and modes/states overlap. Then analyze timing, performance, safety, security and reliability separately.

**Model logical structure before premature realization.** Group responsibilities and interactions without assuming hardware/software/vendor where appropriate. Explore alternative partitioning. Later map logical elements/functions many-to-many onto physical/software/human performers. Retain rationale and architecture decision, not only the selected deployment.

**Model deployment explicitly.** Show software/artifacts/services on nodes, locations/regions/zones, network paths, replicas, versions and operational ownership. A service definition does not reveal which release is running where. Connect desired design to configuration/runtime inventory without allowing telemetry to silently redefine authority.

**Allocate with evidence obligations.** Map functions/behaviors and requirements to responsible performers; resources/budgets to consumers/providers; hazards/controls and verification cases to accountable elements. Identify shared/integration responsibility. Allocation is a design hypothesis that needs feasibility, satisfaction and verification evidence.

**Represent multiplicity and topology.** Define allowed cardinality and configured count. State whether instances are interchangeable, uniquely addressed, ordered or replicated. Model quorum/voting, leader/follower, load balancing and failover behaviors in behavior views. A `[2]` multiplicity does not establish independence or availability.

**Expose failure and trust domains.** Link elements sharing power, clock, cooling, network, identity, software/configuration, supplier, location or operator. Model containment/security zones separately from product hierarchy. Analyze boundary crossings, least privilege and common cause. Redundancy within one zone may provide little resilience.

**Handle variants and options.** Define features/applicability and constraints, then generate configured structures. Avoid independent copied diagrams. Validate required ports/connections/allocations for each permitted combination and prohibit impossible combinations. Trace regional/regulatory/supplier-specific elements and evidence.

**Integrate suppliers.** Specify structural deliverables, stable IDs, native/neutral formats, interfaces, versions, parts/BOM, configuration, provenance, change notice, rights, validation and lifecycle support. Treat black-box internals honestly; model the contractual boundary and evidence without inventing inaccessible structure.

**Use modularity as a trade, not a picture.** Assess cohesion, coupling, interface complexity, change propagation, deployment, ownership, verification, reuse, performance and failure isolation. More boxes can increase coordination and common infrastructure. Fewer boxes can concentrate change and failure. Measure relevant outcomes.

**Check graph integrity and semantics.** Detect duplicate IDs, orphan/unused elements, multi-parent containment, cycles, dangling endpoints, illegal connection kinds, incompatible types/directions/units, unused or exposed ports, unallocated behavior, invalid cross-zone edges and variant gaps. Define waivers with rationale and expiry.

**Reconcile with realization.** Compare design baseline to as-built/as-configured/as-deployed parts, versions, connections and interfaces. Investigate discrepancy: implementation deviation, model error, approved change not propagated, measurement/inventory error or emergent dependency. Preserve both observations and resolve through authority.

**Propagate change.** A structural change affects requirements, behavior, interfaces, budgets, hazards, suppliers, tests, integration sequence, operations, maintenance, training and decisions. Traverse impact before authorization; rebaseline and regenerate views. Preserve prior configurations for builds and evidence.

The following checker audits a declared emergency-water structure. Direction rules differ for assembly, inbound/outbound delegation and external context. It cannot establish capacity, timing, protocol behavior, physical fit, safety, security or real integration.

<!-- bijux-verify: {"id":"structure-model-integrity-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"elements=6\ninternal_elements=4\nexternal_elements=1\ncontainment_edges=4\nunique_containment_parent=1\ncontainment_cycle=0\nports=13\nconnections=8\nendpoint_errors=0\ntype_mismatches=0\ndirection_errors=0\nexternal_boundary_connections=2\nfunctions_allocated=4\nstatus=structure_model_consistent\nevidence=declared_structure_only\n","stderr":""}} -->
```python
elements = {"system", "controller", "pump", "sensor", "power", "environment"}
internal = {"controller", "pump", "sensor", "power"}
external = {"environment"}
contains = [("system", child) for child in sorted(internal)]
ports = {
    "system.supply_in": ("in", "Water"),
    "system.delivery_out": ("out", "Water"),
    "controller.cmd_out": ("out", "Command"),
    "controller.pressure_in": ("in", "PressureSample"),
    "controller.power_in": ("in", "DC28"),
    "pump.cmd_in": ("in", "Command"),
    "pump.power_in": ("in", "DC28"),
    "pump.water_in": ("in", "Water"),
    "pump.water_out": ("out", "Water"),
    "sensor.pressure_out": ("out", "PressureSample"),
    "power.bus_out": ("out", "DC28"),
    "environment.supply_out": ("out", "Water"),
    "environment.delivery_in": ("in", "Water"),
}
connections = [
    ("external", "environment.supply_out", "system.supply_in"),
    ("delegation_in", "system.supply_in", "pump.water_in"),
    ("delegation_out", "pump.water_out", "system.delivery_out"),
    ("external", "system.delivery_out", "environment.delivery_in"),
    ("assembly", "controller.cmd_out", "pump.cmd_in"),
    ("assembly", "sensor.pressure_out", "controller.pressure_in"),
    ("assembly", "power.bus_out", "controller.power_in"),
    ("assembly", "power.bus_out", "pump.power_in"),
]
allocations = {"control": "controller", "move-water": "pump",
               "sense-pressure": "sensor", "supply-power": "power"}

parents = {}
for parent, child in contains:
    parents.setdefault(child, []).append(parent)

def containment_cycle(edges):
    parent = {child: owner for owner, child in edges}
    for start in parent:
        seen, node = set(), start
        while node in parent:
            if node in seen:
                return True
            seen.add(node)
            node = parent[node]
    return False

direction_rules = {
    "assembly": ("out", "in"),
    "external": ("out", "in"),
    "delegation_in": ("in", "in"),
    "delegation_out": ("out", "out"),
}
endpoint_errors = sum(source not in ports or target not in ports
                      for _, source, target in connections)
type_mismatches = sum(ports[source][1] != ports[target][1]
                      for _, source, target in connections)
direction_errors = sum((ports[source][0], ports[target][0]) != direction_rules[kind]
                       for kind, source, target in connections)

print(f"elements={len(elements)}")
print(f"internal_elements={len(internal)}")
print(f"external_elements={len(external)}")
print(f"containment_edges={len(contains)}")
print(f"unique_containment_parent={int(all(len(value) == 1 for value in parents.values()))}")
print(f"containment_cycle={int(containment_cycle(contains))}")
print(f"ports={len(ports)}")
print(f"connections={len(connections)}")
print(f"endpoint_errors={endpoint_errors}")
print(f"type_mismatches={type_mismatches}")
print(f"direction_errors={direction_errors}")
print(f"external_boundary_connections={sum(kind == 'external' for kind, *_ in connections)}")
print(f"functions_allocated={len(allocations)}")
consistent = all(len(value) == 1 for value in parents.values())
consistent &= not containment_cycle(contains) and not endpoint_errors
consistent &= not type_mismatches and not direction_errors
print("status=" + ("structure_model_consistent" if consistent else
                   "structure_model_needs_work"))
print("evidence=declared_structure_only")
```

The checker treats exact type strings as compatibility, which is intentionally weaker than real interface compatibility. It also does not check multiplicity, capacity or whether one power source creates a common-cause risk.

## Definitions and Notation

Let definition $D$ constrain features $F_D$ and usage $u:D$ apply that definition in owner/context $o$, configuration $\gamma$ and multiplicity $m$:

\[
u=(id,D,o,role,m,values,\gamma).
\]

Containment relation $owns(o,u)$ governs identity/lifecycle. Reference $ref(x,u)$ does not. Allocation $alloc(f,u)$ assigns responsibility for function $f$ but does not imply $owns$, $implements$ or $verifies$.

Boundary cut for system-owned set $V_{sys}$ is

\[
\delta(V_{sys})=\{(p_i,p_j)\in E_K:owner(p_i)\in V_{sys}\oplus owner(p_j)\in V_{sys}\},
\]

where $\oplus$ is exclusive-or. Every cut connection should correspond to a governed external interface or explicit exception for the declared baseline.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—context and viewpoints.** Define system/external boundary, concerns, structures and authoritative configuration.

**Mechanism 2—identity and ownership.** Separate definitions, usages, instances, containment, reference, multiplicity and lifecycle.

**Mechanism 3—interaction semantics.** Define ports, interfaces, item flows, assembly/delegation, compatibility, trust/failure boundaries and external dependencies.

**Mechanism 4—allocation and realization.** Relate logical, product, physical, software, deployment, human and enabling structures; allocate functions/resources/risks/evidence.

**Mechanism 5—assurance and evolution.** Check graph/configuration, integrate suppliers/variants, reconcile realization and propagate controlled changes.

Graph consistency establishes only declared structural rules. Architecture adequacy needs behavioral, quantitative, risk, integration and outcome evidence.

## Alternatives and Trade-Offs

**Hierarchical decomposition** clarifies ownership/integration but hides crosscutting dependencies. **Network views** expose connections/failure/trust but can obscure lifecycle authority. Maintain both over shared identities.

**One integrated model** improves consistency but can overload tools and access. **Federated domain structures** preserve specialist semantics but require authority, mappings and configuration alignment.

**Early logical separation** preserves solution freedom. **Early physical constraints** improve realism and supplier planning. Iterate with explicit decisions and maturity.

**Fine-grained components/services** can isolate change and deployment but increase interface, coordination and operational burden. **Coarse elements** reduce boundaries but concentrate coupling/failure. Evaluate scenarios and evidence.

**Typed strict ports** catch incompatibility but require library governance. **Flexible generic connectors** ease exploration but defer risk. Mature semantics with lifecycle stage and consequence.

**Black-box supplier structure** protects IP and simplifies acquisition but limits analysis and sustainment. Contract for the semantic/evidence detail needed by risk and lifecycle.

## Failure Modes and Misconceptions

**“The hierarchy is the architecture.”** It is one ownership/integration view; behavior, interactions, trust and deployment cross it.

**“A block is a component.”** It may be a definition, logical role, usage, instance, organization or conceptual grouping; state the kind.

**“Nested means owned.”** Diagram nesting only has meaning if the metamodel declares composition.

**“A connector is an interface.”** It relates endpoints; the governed agreement includes far more semantics and evidence.

**“Matching type names prove compatibility.”** Versions, units, protocol, timing, quality, state, security and physical characteristics may differ.

**“Allocation proves implementation.”** It assigns responsibility; realization and verification remain open.

**“Two replicas are resilient.”** Shared zones, state, software, control and operators can create common cause.

**“Logical equals software.”** Logical responsibility can map to hardware, software, people or combinations.

**“Runtime inventory is design authority.”** It is essential observed/configuration evidence to reconcile, not an automatic rewrite.

**“More boxes mean more modularity.”** Modularity depends on cohesion, coupling, ownership, interfaces and change/failure outcomes.

## Worked Examples

### Example 1

**Definition versus usage.** `Sensor` defines capabilities; `inletSensor: Sensor` and `outletSensor: Sensor` are distinct roles with different locations/calibration/configurations and later serial identities.

### Example 2

**Shared service reference.** Several products reference enterprise identity rather than contain copies. The model exposes external ownership, SLA, protocol, trust and common-cause dependency.

### Example 3

**Delegation.** A system fluid-in port delegates to an internal valve port. Direction is inward relative to both owners; treating delegation as ordinary out-to-in assembly would be wrong.

### Example 4

**Adapter.** Two data ports use different schema versions. A transformation service owns explicit mappings, loss/error behavior and verification; a direct connector is rejected despite similar names.

### Example 5

**Logical-to-physical mapping.** Detect, decide and actuate responsibilities map across sensor electronics, controller software, operator and pump hardware. No one-to-one assumption hides the human or shared processor.

### Example 6

**Deployment.** Three service replicas span two zones but share one database, identity provider and release pipeline. The failure-domain view prevents a false three-zone availability claim.

### Example 7

**Multiplicity.** Four batteries are configured 2s2p. Count alone does not establish voltage/capacity/current sharing, balancing, isolation, replacement or failure behavior; parametric and behavior models complete the claim.

### Example 8

**Variant gap.** Removing an optional radio leaves an emergency-alert function and port unallocated in one variant. Configuration validation catches it before generated build artifacts.

### Example 9

**Supplier black box.** The internal converter remains opaque, but boundary ports, performance, hazards, software/version, maintenance and verification evidence are governed contractually.

### Example 10

**As-built mismatch.** Field inventory shows a different network switch version/path. Engineers preserve observed/design states, assess interface/security/performance impact and authorize correction or model change with history.

## Cross-Program Connections

**Platform engineering.** Control planes, shared services, tenant boundaries, clusters, regions, templates and runtime inventory require definition/usage, deployment and failure/trust views.

**API and service engineering.** Services, endpoints, schemas, topics and dependencies form typed structure whose connections need behavioral compatibility and ownership.

**Data engineering.** Datasets, stores, pipelines, catalogs and consumers require authority, lineage/reference, deployment, privacy zones and schema/version interfaces.

**Object-oriented programming.** Class/type versus object/instance, composition versus reference and interface contracts echo structural semantics, but runtime/deployment and sociotechnical elements remain wider.

**Functional programming.** Types/modules and composition can express structural contracts; effectful runtime resources, topology and external systems still require configured views.

## References

1. NASA, *Systems Engineering Handbook, Section 2.0: Fundamentals of Systems Engineering*, current web edition. <https://www.nasa.gov/reference/2-0-fundamentals-of-systems-engineering/>
2. NASA, *Systems Engineering Handbook, Section 4.3: Logical Decomposition*, current web edition. <https://www.nasa.gov/reference/4-3-logical-decomposition/>
3. NASA, *Systems Engineering Handbook, Section 4.4: Design Solution Definition*, current web edition. <https://www.nasa.gov/reference/4-4-design-solution-definition/>
4. NASA, *Systems Engineering Handbook, Section 6.3: Interface Management*, current web edition. <https://www.nasa.gov/reference/6-3-interface-management/>
5. NASA, *Systems Engineering Handbook, Section 5.2: Product Integration*, current web edition. <https://www.nasa.gov/reference/5-2-product-integration/>
6. NASA, *NASA Systems Modeling Handbook for Systems Engineering*, NASA-HDBK-1009A, active 2025. <https://standards.nasa.gov/standard/NASA/NASA-HDBK-1009>
7. Object Management Group, *Systems Modeling Language Specification Version 2.0*, 2025. <https://www.omg.org/spec/SysML/2.0>
8. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2022. <https://www.iso.org/standard/74393.html>
9. NASA, *Systems Engineering Handbook, Appendix H: Integration Plan Outline*, current web edition. <https://www.nasa.gov/reference/appendix-h-integration-plan-outline/>
10. NASA, *Systems Engineering Handbook, Section 6.5: Configuration Management*, current web edition. <https://www.nasa.gov/reference/6-5-configuration-management/>

## Exercises

### Exercise 1

Design complementary context, logical, physical/deployment, interface and failure/trust structure views for a remote health-monitoring service with home devices, patients, clinicians, cloud services and emergency responders.

### Exercise 2

Audit a model containing two containment parents for one component, a cycle, six dangling connectors, generic bidirectional ports, copied interface values, unallocated functions, three undeclared externals and “redundant” services in one zone.

### Exercise 3

Model definition, usages, configured instances, ports, delegation and verification for a modular battery pack available in 2s2p and 4s1p variants.

### Exercise 4

Plan structural integration of a proprietary supplier subsystem whose internal model cannot be delivered, while retaining lifecycle authority and exit capability.

### Exercise 5

Runtime inventory contradicts the approved deployment model after an emergency change. Define reconciliation, risk decisions, structural updates and evidence preservation.

## Answers to the Exercises

### Answer 1

Define the monitored-care system boundary, service populations/conditions, lifecycle and decision authority. Context includes patient and household/caregiver, home device/sensors/network/power, clinician/health organization, cloud/platform/identity/notification providers, emergency dispatch/responders, regulator and natural/threat environment. Show exchanges: measurements, alerts, acknowledgments, clinical decisions, emergency requests, device updates, identity/consent and support—not vague arrows.

Logical structure separates acquire/qualify, local safe behavior, synchronize, analyze, triage, notify/escalate, clinician review, consent/access, audit and device/fleet operations. Allocate later rather than assuming cloud execution. Physical/deployment views show device types/usages and serial/configuration, gateways, networks, regions/zones, services/versions, stores, identity, clinical workstations and responder channels. Include humans/procedures and low-connectivity/manual fallbacks.

Define ports/interfaces with schemas/units/time stamps/quality, identity/authorization, timing/freshness, error/retry, privacy/classification, consent, device update and emergency protocol/version. Delegate device boundary features to sensor/storage/radio parts and service APIs to internal performers with explicit transformations. Map logical functions many-to-many, including clinician and support workload.

Failure/trust views expose shared device power/network, cloud region/control plane, identity, notification provider, model/release pipeline, staffing and emergency telecom. Analyze household/privacy boundary, clinical authority, common cause and wrong-patient/data risks. Variants cover devices, conditions, jurisdictions, access/connectivity and care organizations. Validate containment, endpoints, versions, allocations and configurations; then use behavior, parametric, hazard/security and field evidence to assess timeliness, clinical safety, privacy, workload and emergency outcomes.

### Answer 2

Freeze and identify the baseline, view semantics and configured variant. Resolve two containment parents by determining actual lifecycle/identity owner; replace the other edge with reference/allocation/association or create distinct usages if two roles truly exist. Analyze the cycle for definition recursion, mistaken direction, shared reference or product-organization conflation; do not merely delete the least visible edge. Preserve decisions and downstream IDs.

For six dangling connectors, recover versioned endpoints or mark/remove obsolete connections through change control after impact analysis. Generic bidirectional ports must be decomposed or typed with provided/required exchanges, direction relative to owner, items/schema/units/protocol, multiplicity, mode and quality/timing. Identify authority for copied interface values; create one controlled interface definition and generated endpoint views, resolving conflicts with both parties.

Trace every scoped function to accountable performers and integration responsibility; assess whether missing allocation exposes absent elements or invalid boundary. Identify three undeclared externals, ownership, assumptions, interfaces, SLA/contract, access and failure/trust dependency; expand context rather than silently absorbing them. For redundant services, show configured replicas, nodes/zones, state, database, identity, network, control/release and operator dependencies and analyze common cause/failover behavior.

Re-run duplicate/identity, parent/cycle, endpoint, connection-kind, direction/type/unit/protocol, multiplicity, variant and boundary-cut checks. Review with product/interface/deployment/security/safety/operations/supplier owners. Update requirements, behavior, budgets, hazards, tests, integration and configuration, then validate actual deployment/integration evidence. A clean graph is necessary, not proof of resilience.

### Answer 3

Define reusable Cell, Module, BMS, Enclosure, Contactor, Fuse, Sensor and Pack kinds with governed electrical/thermal/mechanical/data/service port definitions and quantity units. A Pack definition owns role usages such as modules, BMS, enclosure and protection; module owns cell usages. Keep definition identity separate from primary/secondary module roles and later serialized cell/module/pack instances.

Model variant configurations. For 2s2p, resolve four module usages and exact series/parallel topology; for 4s1p, resolve four in series. Do not rely on multiplicity `[4]`. Configure voltage/current/capacity, harness/busbar, sensors, contactors, balancing and BMS channel mappings. Define pack boundary charge/discharge, communication, cooling, mechanical and service ports. Use inbound/outbound delegation to internal protection/BMS/bus structure and assembly between peer parts, with explicit polarity, connector, pin, protocol/schema, units and ratings.

Allocate energy storage, isolation, sensing, balancing, state estimation, thermal control, communication and service behaviors. Map hazards/controls and verification responsibilities. Parametric models compute nominal/min/max voltage, capacity/current, loss/thermal and tolerances with correlation; behavior models define startup, precharge, charging, discharge, imbalance, fault/isolation and maintenance. Failure views expose common cells/modules, cooling, BMS, contactor and sensing.

Configured instances bind serial/lot, chemistry, firmware/calibration, supplier, manufacture/test evidence and maintenance history. Verify type/direction/endpoints, topology, polarity, isolation, dimensional/thermal/mechanical fit, interface/protocol, configured calculations and variant-specific behavior. Execute component, module and pack tests under correct configuration/environment; reuse evidence only with equivalence rationale. Preserve baseline and supersession across replacements.

### Answer 4

Define the contractual system boundary and claims needed for acquisition, integration, verification, operation, maintenance, incident response and retirement. Accept internal opacity only after risk analysis. Require a stable subsystem definition/usage and configured part/software identifiers; external ports and complete interface agreements; form/fit, electrical/thermal/fluid/data/logical/human behavior; modes/states/timing/error/recovery; performance and resource envelopes; hazards/controls; security/privacy/SBOM/vulnerability/change obligations; environmental/qualification evidence; maintenance, diagnostics and life limits.

Contract for native or neutral deliverables to the extent rights allow, stable IDs, schemas/units/protocol versions, configuration lists, provenance, validation rules, test models/stubs, integration fixtures, acceptance criteria, change notice and backward/migration support. Establish one authority for each boundary claim and supplier/customer interface concurrence. Protect IP through controlled access rather than inventing undocumented internals.

Create an internal black-box structural usage referencing the supplier-controlled configuration. Model boundary ports, expected behaviors/properties, failure/trust dependencies and allocated responsibilities. Include supplier tooling/cloud/licensing/support as externals where they affect lifecycle. Use adapters only with explicit semantics and ownership. Avoid copying supplier interface data into a competing source.

Verify interface and contract compliance through document/model validation, inspection, representative integration, fault/timing/security/environment tests and delivered configuration evidence. Preserve anomalies and waivers. Plan exit: data/model export, replacement boundary, escrow/source or diagnostic rights where justified, spares, knowledge transfer, archived tools/readers and migration test. Monitor supplier/version/ownership/support/vulnerability and performance triggers; update the configured authority and downstream artifacts through controlled change.

### Answer 5

Preserve the approved pre-change deployment baseline, emergency authorization, commands/tickets, actor/time, runtime inventory snapshots, logs/telemetry, images/configuration, network/identity/policy state and incident evidence. Stabilize service and security/safety risk first under emergency rules. Do not silently update design to match runtime or roll back without understanding current consequences.

Reconcile element-by-element: service/artifact versions and digests, replicas, nodes/zones/regions, databases/queues/caches, schemas, network paths, identity/secrets/policies, feature flags, external providers, monitoring and operational ownership. Validate inventory accuracy and clock/configuration scope. Classify each delta as authorized emergency implementation, failed/partial change, drift, discovery of previously unmodeled dependency, model error or observation error.

Assess requirements/SLO, behavior/state/data migration, interface compatibility, capacity/timing, safety/security/privacy, failure/trust domains, rollback feasibility, supplier/contract, cost and operator workload. Identify common cause and retained old/new mixed states. Decide with technical/service/risk authority whether to complete, modify, retain temporarily with bounded acceptance, or restore. Preserve dissent and rationale.

Update the controlling design/configuration only for authorized conclusions, creating a new baseline/supersession with effective time and exact deployment manifest. Propagate to requirements, interfaces, allocations, hazards, tests, runbooks, monitoring and decision records. Verify desired-versus-observed convergence and representative recovery/security/performance behavior. Conduct after-action review, correct emergency tooling/authority gaps and define drift/incident/version/topology triggers. Retain prior model and evidence for audit and future rollback reasoning.
