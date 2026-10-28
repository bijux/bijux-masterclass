---
module_id: SYSENG-036
program: Systems Engineering
level: 1
module_number: 36
title: Subsystem Decomposition
status: complete
last_verified: 2026-08-31
---

# Subsystem Decomposition

## One-Page Review

### Governing question

How can a selected physical architecture be decomposed into subordinate systems and implementable elements while preserving parent outcomes, exposing integration work, and avoiding boundaries that merely mirror teams, vendors, or familiar technologies?

### Essential definitions

- A **subsystem** is a system element viewed as a subordinate part of a selected parent system; it can itself be treated as a system of interest at the next recursive level.
- **Subsystem decomposition** defines the parent’s immediate child elements, their responsibilities, interfaces, budgets, configurations, lifecycle obligations, ownership, and realization evidence.
- **Recursive application** applies systems-engineering processes to the next-lower product layer; **iteration** revisits the same layer to correct, mature, or reconcile it.
- A **composition hierarchy** represents whole–part ownership or containment. It does not replace peer-interface, deployment, behavior, requirement, or dependency structures.
- A **partition** divides a selected set into non-overlapping subsets under a stated criterion. Logical responsibilities can still be shared, replicated, or cross-cutting even when physical usages have one composition parent.
- A **child specification** defines the child’s allocated requirements, external interfaces, assumptions, guarantees, constraints, verification, and acceptance evidence.
- A **derived requirement** arises from architecture or design decisions needed to satisfy parent obligations, even when not stated directly at the parent level.
- An **integration obligation** is work or behavior needed to make children operate as the parent, including adapters, paths, assembly, synchronization, configuration, arbitration, end-to-end qualities, and verification.
- **Budget allocation** assigns parent resource/performance limits, reserves, overhead, and margins among children and integration while preserving the parent constraint.
- A **cross-cutting concern** affects several children—such as safety, security, time, data, power, thermal control, human factors, configuration, or diagnostics—and needs an integrating owner and trace.
- A **leaf element** is defined sufficiently to be made, bought, coded, configured, staffed, trained, or reused and verified in its intended context; “leaf” is relative to the governing decomposition.
- **Decomposition closure** means child specifications and integration obligations jointly cover the parent requirements, interfaces, behavior, qualities, lifecycle, and evidence needs without contradiction or unowned residue.

### Central model, mechanism, or theorem

For parent (S), let immediate children be $C(S)=\{c_1,\ldots,c_n\}$, parent obligations (Q_S), child allocations $Alloc\subseteq Q_S\times C(S)$, parent-retained obligations (Q_R), and integration obligations (Q_I). Declaration coverage requires:

$$
\forall q\in Q_S:\quad q\in Q_R\ \lor\ \exists c\in C(S):(q,c)\in Alloc
\ \lor\ q\text{ is satisfied by a traced set in }Q_I.
$$

Coverage marks are necessary but do not prove satisfaction. Compositional correctness requires:

$$
\left(\bigwedge_{c\in C(S)} G_c\right)\land G_I\land A_{system}
\Rightarrow G_S,
$$

while child assumptions must be discharged by sibling/integration guarantees or exported environmental constraints.

For a conserved parent budget (B_r) of resource (r):

$$
\sum_c b_r(c,k,m)+b_r(integration,k,m)+reserve_r(k,m)\le B_r(k,m)
$$

for every applicable configuration (k) and mode (m). Decomposition is not valid merely because each child is locally feasible; the parent must close after interfaces, packaging, conversion, shared services, and integration overhead are included.

### Critical invariants

- The selected parent, boundary, architecture baseline, configurations, lifecycle interval, and decision purpose are explicit.
- Every immediate child has stable identity, role, owner, scope, location/deployment, lifecycle, requirements, interfaces, budgets, assumptions, verification, and acceptance path.
- Every parent requirement, behavior, quality, interface, hazard control, and lifecycle obligation is allocated, jointly realized, or deliberately retained at the parent with rationale.
- External parent interfaces are assigned to child endpoints while parent-level end-to-end ownership remains visible.
- New internal interfaces, conversions, shared resources, common causes, and integration obligations created by decomposition are identified and controlled.
- Child budgets plus integration overhead and reserve close within parent budgets for all relevant modes/configurations and consistent measurement planes.
- Physical child usages have unambiguous composition ownership; shared definitions/services are referenced rather than duplicated in ways that double-count responsibility or resources.
- Cross-cutting concerns have integrating policies, owners, models, and evidence across child boundaries.
- Supplier, organization, contract, and team boundaries inform governance but do not substitute automatically for sound technical boundaries.
- Child specifications are mutually compatible and collectively sufficient to support parent verification and validation.
- Decomposition stops by branch only when the element is sufficiently defined to implement/acquire/reuse and verify, not at an arbitrary uniform depth.
- Changes propagate upward, downward, and laterally through allocations, interfaces, budgets, hazards, integration, verification, suppliers, and configurations.

### Common failures

Common failures include calling every component a subsystem; decomposing by the current organization chart; turning vendor packages into unquestioned architecture; forcing every branch to the same depth; allocating each parent requirement to exactly one child even when it is emergent; forgetting parent-retained and integration obligations; treating interface requirements as belonging only to one side; omitting packaging, cabling, protocols, test points, configuration, and human work; allocating the full parent margin to multiple children; hiding common power, time, identity, data, cooling, or operator dependencies; duplicating a shared service under several parents; defining children without acceptance evidence; optimizing children at the expense of end-to-end outcomes; and believing a complete hierarchy proves the system can be integrated.

### Compact example

A temperature-control unit decomposes into sensing, control/compute, cooling/airflow, power, communications/data, enclosure/structure, and operations/support subsystems. Cargo temperature performance is not assigned to cooling alone: sensors provide bounded measurements; control computes commands; power supports transients; enclosure limits heat gain; airflow distributes cooling; operators maintain configuration; interfaces carry data, energy, heat, material, and authority. The parent retains end-to-end temperature outcome and integrated verification. Calibration rigs, update services, maintenance tools, and procedures are enabling elements. This decomposition exposes both child work and the “glue” needed to produce the parent.

### Connections

SYSENG-035 selects the physical architecture to decompose. SYSENG-031–034 provide the interface identities and contracts that become child boundaries. SYSENG-037 derives integration order and dependency from the child/interface graph; SYSENG-038 evaluates readiness; SYSENG-039–040 develop integration and verification planning. Later requirements, configuration, risk, supplier, specialty-engineering, operations, and lifecycle modules recursively govern the child products and their composition.

## Governing Question

Which immediate child boundaries allow teams to build, buy, reuse, integrate, verify, operate, change, and retire the parent system while preserving end-to-end responsibilities and controlling the interactions that create system value and risk?

The answer is not “split until small.” Start with the selected physical architecture, identify candidate whole–part boundaries, allocate responsibilities and resources, derive child and interface requirements, expose cross-cutting integration, challenge lifecycle scenarios, and revise boundaries when they create excessive coupling, common cause, unclear authority, infeasible budgets, untestable behavior, or unmanageable change. Apply the process recursively to each branch only to the depth required for implementation and assurance.

## Why This Matters

Complex systems cannot be designed or realized as one undifferentiated object. Decomposition enables specialized engineering, parallel work, procurement, configuration control, verification, maintenance, and accountability. Yet every boundary also creates interfaces, assumptions, coordination, latency, packaging, documentation, integration, and failure opportunities. The goal is not maximum modularity or minimum child count; it is a structure whose local work composes into the parent outcome.

NASA's current Systems Engineering Handbook distinguishes recursive application to next-lower products from iteration at the same product layer. It describes applying system design from the top down until lowest products can be built, bought, or reused, then applying realization bottom-up to integrate, verify, validate, and transition them. NASA's current Design Solution Definition guidance says that baselined derived and allocated requirements become the higher-level requirements for decomposed elements and that refinement should proceed far enough for analytical validation, cost/operations modeling, and credible feasibility with margins.

NASA's current Logical Decomposition guidance describes architecture as the structure of hardware, software, humans, support personnel, communications, and operations; calls for decomposition and allocation to lower levels; and requires functional/subsystem interfaces. NASA's Product Integration guidance emphasizes that lower-level products must be assembled into higher products while managing physical, functional, and data interactions and natural/induced environments. These sources make decomposition and recomposition a coupled discipline.

A product breakdown structure is useful because it names the recursive product layers. A work breakdown structure adds the work needed to produce and integrate those products. Neither alone proves technical sufficiency. The hierarchy must connect to peer interfaces, states, deployment, resource budgets, requirements, verification, suppliers, people, enabling products, and operational configurations. “Glue” is not incidental work; it is architecture and systems engineering.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. the selected physical architecture, alternatives, rationale, assumptions, configurations, and evidence;
2. parent stakeholder outcomes, technical requirements, qualities, constraints, ConOps, and lifecycle scenarios;
3. logical-to-physical allocations, end-to-end flows, states/modes, physical paths, and interface contracts;
4. product, specification, drawing, deployment, organization, supplier, and work structures and their different purposes;
5. resource budgets, measurement planes, reserves, uncertainty, concurrency, fault/degraded behavior, and margins;
6. safety, reliability, security, privacy, human, manufacturing, integration, operations, maintenance, and retirement concerns;
7. requirement derivation, bidirectional traceability, verification methods, acceptance criteria, and configuration control;
8. graph boundaries, coupling, cohesion, common cause, shared resources, and change propagation.

As a retrieval test, inspect a decomposition `System -> Front End, Back End, Database`. Ask whether those are logical roles, deployable physical elements, software packages, supplier products, teams, or runtime instances. Ask where identity, networking, observability, configuration, operators, data ownership, backup, recovery, security, facilities/cloud services, and client interfaces belong. Ask which versions/configurations exist and how the pieces integrate. Familiar technical nouns do not establish a complete subsystem structure.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish subsystem, component, element, module, assembly, segment, service, product layer, definition, and instance by declared context rather than name;
2. distinguish recursive decomposition from iteration and product hierarchy from interface, deployment, requirement, organization, supplier, and work structures;
3. select child boundaries using cohesion, coupling, technology, location, fault, trust, supplier, lifecycle, verification, maintenance, and change criteria;
4. allocate parent requirements, behaviors, qualities, interfaces, hazards, resources, authority, and lifecycle obligations to children and integration;
5. derive child requirements and identify parent-retained and cross-cutting responsibilities;
6. expose internal interfaces, conversions, shared resources, common causes, integration work, and enabling products created by decomposition;
7. close mass, power, thermal, compute, data, staffing, performance, and other budgets with overhead and reserve;
8. define child specifications, acceptance evidence, integration points, and configuration applicability;
9. choose branch-specific stopping criteria for make, buy, reuse, configuration, staffing, and verification;
10. audit decomposition closure and manage changes across layers and peer dependencies.

## Core Exposition

**Declare the parent.** Name the system element being decomposed, its parent context, boundary, baseline/version, configurations, lifecycle interval, external interfaces, owner, requirements, and decision supported. `Subsystem` is relative: a communications subsystem at vehicle level becomes a system of interest when its own radios, processors, networks, people, software, and support are decomposed.

**Separate definition, usage, and instance.** A child definition describes a reusable kind; a usage places it in one parent architecture; an instance is an as-built/as-deployed occurrence. Two redundant uses of one sensor definition are distinct physical children with separate location and interface identities. Confusing these levels causes double counting and ambiguous evidence.

**Start from the selected architecture, not a blank tree.** Candidate children should already be suggested by physical elements, locations, paths, technology, fault/trust boundaries, suppliers, lifecycle concepts, and allocations. Decomposition refines this architecture. It should not quietly replace it with a new vendor or organizational grouping.

**Generate alternative child boundaries.** Compare partitions by outcome/mission thread, technology, physical location, energy/material path, information/control path, safety/fault containment, security/privacy, supplier, integration sequence, manufacturing, maintenance/replacement, update cadence, or operations. A good boundary often balances several. Preserve alternative rationale for irreversible or high-coupling choices.

**Use cohesion and coupling as questions, not magic scores.** A child should contain responsibilities that need common state, timing, technology, environment, authority, lifecycle, or change. External coupling should be necessary, explicit, stable enough to govern, and testable. Low interface count alone is not optimal: combining unrelated responsibilities can hide internal coupling and enlarge failure/change scope.

**Define immediate children completely.** Record stable ID/name, purpose, boundary, composition parent, physical type, owner, supplier, location/deployment, lifecycle, configurations, allocated/derived requirements, logical responsibilities, external and sibling interfaces, budgets, assumptions/guarantees, hazards/controls, make/buy/reuse strategy, maturity, verification, acceptance, and lower-level decomposition status.

**Allocate parent requirements with semantics.** Do not copy each parent statement blindly. Some requirements allocate wholly to one child; some need apportioned performance; some are satisfied jointly; some derive several child and interface requirements; some remain verified only at the parent. Preserve rationale and upward/downward trace. Avoid duplicating one obligation in several children without defining joint composition and acceptance.

**Retain parent responsibilities deliberately.** End-to-end outcome, emergent qualities, cross-cutting policy, external-interface coordination, system modes, integration, validation, configuration compatibility, hazard acceptance, and stakeholder acceptance commonly remain at the parent even when contributions allocate downward. Parent retention is not “unassigned”; it has an owner and evidence plan.

**Derive child requirements.** Architecture creates needs not explicit at parent level: data conversion, synchronization, mounting, heat rejection, initialization, diagnostics, test points, configuration identification, fault containment, secure update, maintenance access, or supplier evidence. Record source as architecture/design decision and trace to the parent outcome or constraint.

**Allocate external interfaces.** A parent external interface terminates on one or more child endpoints and may traverse internal children. Allocate the implementation obligations, but retain parent-level semantic and compatibility ownership. For example, a system network interface may physically terminate at a gateway while identity, policy, application semantics, audit, power, and operations span other children.

**Identify new internal interfaces.** Every split creates boundaries. Register data/control, electrical, mechanical, thermal, fluid, material, environmental, human, procedural, organizational, and supplier interfaces. Define both endpoints, plane, direction, conversions, assumptions/guarantees, modes/configurations, owner, verification, and change authority. Count is a review aid, not a design goal.

**Model the potential pair space.** With (n) immediate children, there are (n(n-1)/2) unordered pairs or (n(n-1)) directed cells to review. Most pairs need not interact. Record `no consequential interface` only after considering desired and unintended coupling, shared resources, environment, and lifecycle conditions. Omitted child types remain invisible to the matrix.

**Expose shared resources.** Common power, ground, clock, network, compute, storage, identity, key, configuration, cooling, structure, space, spectrum, data source, operator, facility, supplier, and test equipment create multi-child constraints and common causes. Give the shared resource a governed element/service or parent-level integration owner, allocation policy, arbitration, failure behavior, and evidence.

**Allocate budgets conservatively and consistently.** Translate parent mass, volume, power, energy, thermal, compute, memory, storage, bandwidth, latency, reliability, safety, staffing, cost, and schedule limits into child allocations, explicit integration overhead, uncertainty/growth, and retained reserve. Use the same planes and configurations. Never let every child treat parent reserve as its own.

**Allocate performance end to end.** Latency, accuracy, probability, availability, response time, temperature control, and human workload may not add linearly or decompose independently. State the composition model, dependence, conversion, measurement events, and system verification. Where allocation is provisional, record sensitivity and closure condition.

**Design cross-cutting concerns.** Safety, security, privacy, reliability, human factors, diagnostics, time, configuration, observability, data governance, quality, manufacturing, and sustainment cross child boundaries. Define system policy and architecture, then allocate local controls and evidence. A `security subsystem` cannot absorb every security obligation; a `safety subsystem` does not make other children safe.

**Align fault and trust containment.** Choose boundaries that support isolation, independent power/state, least privilege, controlled data movement, safe failure, and recovery where required. Analyze common cause across supposedly independent children. A shared boot chain, library, operator, rack, cooling loop, or supplier can defeat nominal partitions.

**Include people and enabling products.** Operators, maintainers, administrators, trainers, support, logistics, facilities, simulators, test rigs, calibration equipment, deployment services, monitoring, recovery tools, and disposal systems can be children of the system context or external enabling products with interfaces. Decide ownership and boundary; never omit them because they are not delivered hardware.

**Respect supplier boundaries without surrendering architecture.** A supplier product can align with a child when technical cohesion, interface stability, acceptance, data rights, configuration, evidence, and lifecycle support justify it. If one supplier spans several architectural children, preserve their technical identities. If several suppliers realize one child, name the integration owner. Contract boundaries do not prove technical independence.

**Plan child verification and acceptance.** Each child specification maps requirements to inspection, analysis, demonstration, or test; names article/configuration/environment; defines pass criteria; and identifies delivered evidence. Parent integration needs simulators, stubs, fixtures, test data, instrumentation, interface checks, and anomaly procedures. Child acceptance is not parent acceptance.

**Preserve vertical and horizontal traceability.** Vertical trace connects parent outcomes/requirements to child contributions and evidence. Horizontal trace connects sibling assumptions, interfaces, shared budgets, versions, and integration tests. A perfect requirement tree can still miss peer incompatibility; a perfect interface table can still lack stakeholder rationale.

**Use hierarchy plus peer graphs.** Composition hierarchy identifies who contains whom and prevents double-counting physical usage. Interface/dependency graphs represent peer and cross-level interaction. Deployment maps software/data/humans to nodes/locations. Requirement and verification graphs represent obligation/evidence. Do not force all relations into one tree.

**Manage branches at different depth.** A commercial sensor may be a leaf while custom control electronics require several layers and a human operations element decomposes into roles/procedures/tools/training. Uniform depth creates meaningless wrappers or hides needed design. Review sibling interface maturity even when internal depths differ.

**Apply a stopping rule.** Stop a branch when the element is sufficiently bounded to make, buy, reuse, configure, staff/train, and verify; its interfaces and resources are controlled; residual risks are acceptable; cost/schedule/operations models are credible; and the responsible organization can execute. Resume decomposition if evidence reveals infeasibility, hidden coupling, supplier ambiguity, untestability, or lifecycle gaps.

**Plan bottom-up recomposition while decomposing.** Derive integration sequence, prerequisites, test doubles, safe intermediate configurations, verification levels, logistics, facilities, data, staffing, and anomaly isolation from the child graph. The decomposition is suspect if no credible path recomposes children into the parent.

**Audit closure.** Review every parent requirement, function, flow, mode, external interface, budget, quality, hazard/threat, human task, enabling need, lifecycle scenario, configuration, and verification objective. Confirm an owner and composition rationale. Check every child has a reason and every internal interface has endpoint agreement. Record gaps explicitly.

**Manage changes bidirectionally.** A parent change flows to affected children; a child constraint or failure may force parent architecture change; a sibling interface change affects both sides and integration; a supplier substitution changes evidence and lifecycle; a budget transfer alters reserve and other allocations. Traverse dependency graphs and rebaseline coherent views.

**Avoid local optimization.** Child teams naturally optimize their own mass, performance, schedule, or assurance. Maintain parent trade authority and shared measures. A heavier child may reduce system wiring; slower local processing may improve accuracy; a separate module may improve maintenance but reduce reliability through connectors. Evaluate parent outcome.

**State evidence limits.** Decomposition reviews show declared coverage and plausibility. They do not prove child implementations, interface compatibility, production capability, integrated qualities, or validation. Early supplier estimates, simulations, prototypes, and heritage each have bounded domains. Carry uncertainty into the baseline.

The following checker finds selected governance gaps in six child-element records. It does not prove decomposition closure or parent satisfaction.

<!-- bijux-verify: {"id":"subsystem-decomposition-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"children_total=6\nwell_formed_declared=1\nmissing_requirements=CH-002\nmissing_interfaces=CH-003\nmissing_budgets=CH-004\nmissing_owner=CH-005\nmissing_verification=CH-006\nunresolved=CH-002,CH-003,CH-004,CH-005,CH-006\nevidence=declared_fields_only\n","stderr":""}} -->
```python
children = [
    {"id": "CH-001", "requirements": ["REQ-SENSE-12"],
     "interfaces": ["IF-DATA-2", "IF-MECH-3"], "budgets": {"power_w": 12},
     "owner": "Sensing Lead", "verification": ["inspection", "environmental test"]},
    {"id": "CH-002", "requirements": [], "interfaces": ["IF-PWR-4"],
     "budgets": {"power_w": 80}, "owner": "Power Lead", "verification": ["load test"]},
    {"id": "CH-003", "requirements": ["REQ-STORE-8"], "interfaces": [],
     "budgets": {"storage_gb": 64}, "owner": "Data Lead", "verification": ["analysis"]},
    {"id": "CH-004", "requirements": ["REQ-ALERT-5"], "interfaces": ["IF-HUMAN-1"],
     "budgets": {}, "owner": "Operations Lead", "verification": ["human-in-loop test"]},
    {"id": "CH-005", "requirements": ["REQ-COOL-9"], "interfaces": ["IF-THERM-6"],
     "budgets": {"mass_kg": 24}, "owner": "", "verification": ["thermal test"]},
    {"id": "CH-006", "requirements": ["REQ-RECOVER-3"], "interfaces": ["IF-CTRL-7"],
     "budgets": {"latency_ms": 250}, "owner": "Recovery Lead", "verification": []},
]
fields = ("requirements", "interfaces", "budgets", "owner", "verification")
valid = [child for child in children if all(child[field] for field in fields)]
print(f"children_total={len(children)}")
print(f"well_formed_declared={len(valid)}")
for field in fields:
    print(f"missing_{field}=" + ",".join(c["id"] for c in children if not c[field]))
print("unresolved=" + ",".join(c["id"] for c in children if c not in valid))
print("evidence=declared_fields_only")
```

`CH-001` may still have wrong allocations, incompatible interfaces, inadequate budgets, or weak verification. Populated declarations are not sufficient evidence.

## Definitions and Notation

Let parent (S), immediate physical child usages $C(S)=\{c_1,\ldots,c_n\}$, parent requirements (Q_S), parent external interfaces (I_S), internal child interfaces (I_C), configurations (K), and modes (M).

Composition ownership relation:

$$
partOf\subseteq C\times S,
$$

with each physical usage having one composition parent in a selected baseline:

$$
\forall c:\quad |\{s:(c,s)\in partOf\}|=1.
$$

Reusable definitions can be instantiated in several parents; the usages remain distinct.

Requirement allocation relation:

$$
Alloc_Q\subseteq Q_S\times(C(S)\cup\{Parent,Integration\}).
$$

Declaration coverage:

$$
C_Q=\frac{|\{q\in Q_S:\exists x,(q,x)\in Alloc_Q\}|}{|Q_S|}.
$$

(C_Q=1) does not prove correct allocation, requirement completeness, child satisfaction, or parent composition.

For (n) children, unordered pair review opportunities are:

$$
N_u=\frac{n(n-1)}{2},
$$

and directed cells are (N_d=n(n-1)). A pair may host multiple interfaces; omitted children and shared/environmental couplings are outside these counts.

For parent resource budget (B_r(k,m)):

$$
Margin_r(k,m)=B_r(k,m)-Reserve_r(k,m)-Integration_r(k,m)
-\sum_{c\in C(S)} Allocation_r(c,k,m).
$$

The invariant requires $Margin_r(k,m)\ge0$ for every applicable configuration/mode under the declared composition model.

Let child contracts (C_c=(A_c,G_c)) and integration contract (C_I=(A_I,G_I)). Parent contract closure requires internal assumptions be discharged and:

$$
A_S\land\bigwedge_c G_c\land G_I\Rightarrow G_S.
$$

This predicate relation is an assurance obligation. Physical realizability, causality, uncertainty, and model completeness need separate evidence.

## Mechanisms, Invariants, or Proof Structure

The core mechanism is decompose–allocate–interface–budget–specify–recompose:

1. fix the parent architecture, baseline, scope, configurations, external contracts, and lifecycle;
2. generate alternative immediate-child boundaries and compare system consequences;
3. allocate parent requirements, behaviors, qualities, resources, hazards, authority, and lifecycle obligations;
4. derive child and interface requirements plus parent-retained and integration obligations;
5. define child specifications, owners, suppliers, verification, and acceptance;
6. test horizontal compatibility, shared resources, common causes, and cross-cutting policies;
7. construct bottom-up integration and parent verification paths;
8. audit closure, refine boundaries, baseline, and repeat recursively where needed.

**Parent invariant.** The parent system identity, external obligations, and acceptance remain visible throughout decomposition. Children do not replace the stakeholder outcome.

**Ownership invariant.** Each physical usage has unambiguous composition ownership; each requirement/derived requirement/interface/budget/hazard/control/test has accountable governance; shared definitions do not create duplicate physical ownership.

**Coverage invariant.** Every parent obligation is allocated, jointly realized, or retained with trace and rationale; every child responsibility contributes to an identified parent or lifecycle need.

**Interface invariant.** Each split-induced and external-interface allocation has controlled endpoints, planes, semantics, assumptions/guarantees, modes, versions, and evidence. Parent end-to-end semantics remain owned.

**Budget invariant.** Children, integration overhead, uncertainty/growth, and reserve fit the parent constraint in every relevant configuration/mode. Allocations use consistent planes and do not reuse margin.

**Composition invariant.** Child and integration guarantees jointly entail parent guarantees under discharged/exported assumptions. Pairwise conformance cannot substitute for shared-resource and system-scenario analysis.

**Cross-cutting invariant.** Qualities and policies spanning children have parent authority, local allocations, interface obligations, system models, and integrated evidence.

**Lifecycle invariant.** Children and their interfaces can be manufactured/configured/staffed, assembled, integrated, verified, transported, operated, maintained, updated, recovered, and retired with identified enabling products and safe intermediate states.

**Stopping invariant.** Each leaf is implementable/acquirable/reusable and verifiable with controlled interfaces, resources, risks, and ownership. Depth may differ by branch.

**Evidence invariant.** Allocation, compatibility, feasibility, maturity, and acceptance claims name baseline, model/article, environment, method, criterion, result, anomalies, and limitations.

Adversarial review constructs missing or conflicting allocations, simultaneous budget peaks, duplicate physical ownership, unowned integration, circular child assumptions, shared common cause, crosscutting-policy inconsistency, supplier boundary gaps, configuration mismatch, unavailable test equipment, inaccessible maintenance, unsafe assembly state, and a parent requirement that no child/integration evidence can verify. Any witness invalidates the corresponding closure claim.

## Alternatives and Trade-Offs

**Functional versus physical decomposition.** Functional groups preserve outcome logic and technology freedom; physical decomposition supports build/integration. Conflating them can force one-to-one allocation. Maintain trace between them.

**Technology-oriented versus mission-thread boundaries.** Technology children concentrate expertise and reuse but create end-to-end interfaces. Mission-thread children localize outcomes but duplicate platforms and standards. Hybrid shared platforms plus bounded mission services need explicit ownership and capacity.

**Fine versus coarse decomposition.** Fine children support parallel work, replacement, and specialized verification but multiply interfaces and integration. Coarse children reduce external interfaces while increasing internal complexity, failure/change scope, and supplier opacity. Choose by lifecycle evidence, not a target box count.

**Supplier-aligned versus architecture-aligned.** Supplier packages simplify contracting and acceptance but can lock interfaces and obscure system logic. Architecture-aligned children preserve technical integrity but may cross contracts. Map both structures and name integration authority.

**Shared versus dedicated services.** Shared power, compute, time, data, identity, cooling, or diagnostics improve reuse and utilization but create contention, common cause, policy coupling, and widespread change. Dedicated services isolate at resource cost. Parent-level contracts and failure handling govern either choice.

**Parent-retained versus child-allocated qualities.** Retaining all quality ownership at parent can leave child teams without actionable constraints. Fully allocating emergent quality can create false arithmetic. Use child contributions/budgets plus parent models and integrated acceptance.

**Uniform versus branch-specific depth.** Uniform depth looks tidy and aligns management reporting but creates artificial wrappers or hides unresolved custom work. Branch-specific depth follows make/buy/reuse and evidence maturity while requiring disciplined cross-level interfaces.

**Stable interface versus coordinated co-development.** Stable boundaries enable parallel work and suppliers. Early systems may need joint iteration to discover feasible contracts. Use controlled provisional interfaces with owners, bounds, and freeze criteria rather than pretending stability.

**Bottom-up reuse versus top-down allocation.** Reuse can reduce development, but forcing parent obligations into existing product envelopes can distort architecture. Compare reuse context and retain authority to change the parent design only through traceable trade.

**Local versus integrated verification.** Child verification finds defects early and supports acceptance; parent integration reveals interactions and emergent behavior. Plan both. Duplicative tests can sometimes be reduced through credited evidence, but only with configuration and method equivalence.

## Failure Modes and Misconceptions

**“Subsystem is an intrinsic size class.”** It is a child relative to a selected parent. The same element can be a system of interest in its own decomposition.

**“Decomposition means functional breakdown.”** Physical subsystem decomposition uses architecture realization and maps many-to-many to functional/logical structures.

**“The hierarchy shows all relationships.”** Peer interfaces, shared resources, deployment, requirements, states, suppliers, work, and evidence need other linked structures.

**“One requirement belongs to one child.”** End-to-end and emergent requirements often need multiple contributions, integration, and parent verification.

**“Every requirement should flow down.”** Some stakeholder/system outcomes are retained and verified at parent level while child requirements derive from them.

**“Interfaces are just lines between children.”** They require semantics, planes, modes, conversions, assumptions/guarantees, owners, versions, and evidence.

**“Fewer interfaces means better decomposition.”** A coarse monolith can hide harmful coupling and enlarge failure/change scope. Evaluate quality of boundaries.

**“The WBS defines technical boundaries.”** It organizes work and cost. Technical architecture should inform it, but work packages, organizations, and products are not identical structures.

**“A supplier owns integration inside its box.”** The acquirer/system authority still needs interface, evidence, change, safety/security, and parent-outcome assurance appropriate to risk.

**“Shared services require no allocation.”** They need capacity, priority, failure, security, change, and ownership contracts across all consumers.

**“All branches stop at the same level.”** Stop where each branch can be implemented and verified; commercial, custom, and human branches mature differently.

**“Child acceptance proves parent acceptance.”** Composition, shared conditions, end-to-end qualities, external interfaces, operations, and validation remain.

**“Baselined children cannot force parent change.”** Lower-level evidence can reveal an infeasible architecture. Controlled upward iteration is essential.

## Worked Examples

### Example 1

**Cold-chain unit decomposition.** The parent is a fielded refrigeration unit, not the entire fleet. Immediate children are sensing, controller, cooling/airflow, power, enclosure/structure, communications/data, and local human interface. Cloud analytics and depot calibration are external enabling systems in this boundary choice.

Cargo-temperature performance stays parent-owned. Sensing contributes accuracy/freshness; enclosure heat-leak limit and airflow distribution are allocated; controller and cooling receive response/bounds; power covers startup; communications supports remote evidence but is not required for local control; human interface handles alarm/recovery. Internal thermal, power, data, control, mounting, calibration, and maintenance interfaces are registered. The boundary enables disconnected operation and testable child evidence.

### Example 2

**Technology grouping creates an end-to-end gap.** A service system is decomposed into UI, middleware, and database. The parent requires user-visible confirmation within 500 ms and no duplicate action. Each child receives a local latency target, but retry/idempotency authority and end-to-end timing events remain unowned.

The revised decomposition retains parent transaction semantics, assigns stable operation identity to middleware, conditional write to data child, rendering state to UI, and retry/duplicate contracts at interfaces. Latency budget includes network, queue, processing, persistence, and display events. Technology boundaries remain, but system outcome and integrated verification are explicit.

### Example 3

**Power budget fails after integration overhead.** Parent capacity is 1,000 W. Controlled reserve is 150 W. Child allocations are 240, 180, 260, and 120 W; conversion, wiring, control, and cooling overhead is 60 W.

$$
Margin=1000-150-(240+180+260+120)-60=-10\text{ W}.
$$

Every child is within its allocation, yet the parent does not close. The team must reduce allocations/overhead, increase capacity, change reserve with evidence, or sequence loads if the parent requirement permits. Omitting “glue” would falsely report 50 W margin.

### Example 4

**Installed mass allocation.** A parent mass cap is 200 kg with 20 kg reserve. Four children receive installed-mass allocations 45, 50, 55, and 22 kg; parent-level structure, harness, fluids, and fasteners require 12 kg.

$$
Margin=200-20-(45+50+55+22)-12=-4\text{ kg}.
$$

The hierarchy cannot assign integration mass nowhere. Each child allocation states its interface plane and inclusions. Rebalancing considers center of mass, strength, thermal, supplier uncertainty, and access; reducing a bracket locally might raise harness or integration mass elsewhere.

### Example 5

**Shared time service defeats nominal independence.** Two redundant control children use separate processors and power but share one network time service. Both reject commands when time uncertainty grows. A time-service outage disables both, although the redundancy view shows no shared box.

The decomposition represents time as a cross-cutting service with local holdover guarantees, independent monitoring, degradation, authority, and recovery. Common-cause analysis includes network, protocol, certificates, configuration, and operator. Redundancy evidence is updated. A shared logical dependency mattered more than composition hierarchy.

### Example 6

**Supplier boundary and acceptance.** A vendor delivers an integrated navigation child. Its contract exposes position and health, but not raw sensor data or fault-isolation evidence. Parent safety analysis requires detecting a class of common-mode errors.

Options include a stronger vendor interface/evidence obligation, independent monitor, alternate supplier/product, or parent architecture change. Procurement defines versions, environment, data rights, change notice, verification credit, anomaly support, and obsolescence. Treating the sealed vendor package as a complete child without assurance would leave the parent hazard control unverified.

### Example 7

**Human operations child.** A facility system initially decomposes only equipment. Yet startup, hazardous-energy isolation, alarm diagnosis, sampling, recovery authorization, and maintenance are allocated partly to people.

The physical structure adds an operations work-system child: roles, staffing, consoles, tools, procedures, training, communication, protective equipment, environment, shifts, and handoff. Its interfaces with control, safety, maintenance, and management are controlled. Human-in-the-loop and operational-readiness evidence complement equipment verification. “Operator” is not a free external dependency.

### Example 8

**Safety partition crosses product boundaries.** Hazard containment requires independent shutdown of energy supply, actuator inhibition, sensor voting, and operator indication. Creating a `Safety Subsystem` box would not make the other children safe.

The parent retains safety architecture and hazard acceptance. Local shutdown mechanisms allocate to power/control/actuation, diagnostics to sensing, indication/action to human interface and operations, and independence constraints to physical paths and suppliers. Integrated fault injection verifies the safety function. The cross-cutting concern has local owners plus one system owner.

### Example 9

**Branch-specific stopping.** The selected system has a commercial display, custom controller, and technician work system. The display is treated as a leaf after exact product/version, mounting, electrical/data, environment, cybersecurity, support, and acceptance are controlled. The custom controller decomposes into compute, I/O, power, firmware, enclosure, and test support. The work system decomposes into roles, procedures, tools, training, and facility only as far as staffing/acquisition and evaluation need.

Uniform extra wrappers around the display would add no value; stopping the controller at one box would leave it unimplementable. Each branch meets the same stopping principle through different depth.

### Example 10

**Child change forces parent reallocation.** A communications child changes radio technology. It meets its own throughput requirement but adds 30 W, changes antenna location, emits in a new band, requires a different network driver, and shortens vendor support.

Impact reaches power/thermal budgets, enclosure geometry, EMC, safety coexistence, software deployment, security accreditation, human installation, regional variants, integration fixtures, tests, spares, operations, and retirement. Parent authority compares alternatives and transfers budget, changes physical paths, or rejects the change. Local conformance did not make it locally contained.

## Cross-Program Connections

**Platform engineering.** Platform decomposition separates control/data planes, compute, network, storage, identity, policy, observability, delivery automation, support, and regions while retaining cross-cutting SLO, security, and operability ownership.

**API and service engineering.** Service boundaries resemble subsystem boundaries: each needs responsibility, state/data ownership, contracts, resource budgets, failure behavior, versioning, observability, and integration tests. Team boundaries are not automatically good service boundaries.

**Data engineering.** Pipeline, storage, catalog, quality, governance, orchestration, and serving children share schemas, lineage, time, identity, capacity, replay, and retention. Parent data outcomes remain end to end.

**Object-oriented programming.** Composition and encapsulation help localize responsibility, but inheritance/package/module hierarchies do not represent runtime deployment or all dependencies. Behavioral contracts and integration remain necessary.

**Functional programming.** Functional decomposition and composition make transformations explicit; physical subsystem decomposition additionally assigns effects, state, resources, failures, people, and lifecycle ownership.

**Organization and procurement.** PBS, WBS, teams, contracts, suppliers, and cost accounts should map to technical structure without replacing it. Misalignment needs explicit integration and authority.

**Safety, security, and reliability.** Fault/trust containment, independence, shared resources, common cause, hazard controls, privilege, and recovery determine good boundaries and cross-cutting obligations.

**Verification and integration.** Decomposition creates the product layers and peer graph from which verification levels, test doubles, integration sequence, acceptance evidence, anomaly isolation, and readiness criteria are derived.

## References

1. NASA, *Systems Engineering Handbook, Section 2.0: Fundamentals of Systems Engineering*, current web edition. <https://www.nasa.gov/reference/2-0-fundamentals-of-systems-engineering/>
2. NASA, *Systems Engineering Handbook, Section 4.4: Design Solution Definition*, current web edition, updated 2023. <https://www.nasa.gov/reference/4-4-design-solution-definition/>
3. NASA, *Systems Engineering Handbook, Section 4.3: Logical Decomposition*, current web edition, updated 2023. <https://www.nasa.gov/reference/4-3-logical-decomposition/>
4. NASA, *Systems Engineering Handbook, Section 5.2: Product Integration*, current web edition, updated 2023. <https://www.nasa.gov/reference/5-2-product-integration/>
5. NASA, *Systems Engineering Handbook, Section 6.1: Technical Planning*, current web edition, updated 2023. <https://www.nasa.gov/reference/6-1-technical-planning/>
6. NASA, *Work Breakdown Structure Handbook*, NASA/SP-2010-3404, current official PDF. <https://www.nasa.gov/wp-content/uploads/2023/08/nasa-work-breakdown-structure-handbook.pdf>
7. BKCASE Editorial Board, *SEBoK: Applying Life Cycle Processes*, current online edition. <https://sebokwiki.org/wiki/Applying_Life_Cycle_Processes>
8. Object Management Group, *Systems Modeling Language Version 2.0*, formal specification, 2025. <https://www.omg.org/spec/SysML/2.0>
9. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>

## Exercises

### Exercise 1

A parent has six requirements. `Q1` and `Q2` allocate to child A; `Q3` allocates jointly to B and C; `Q4` is retained at parent; `Q5` allocates to integration; `Q6` has no trace. Compute declaration coverage and explain why even 100% would not prove decomposition closure. Propose a disposition for `Q6` without assuming it must belong to one child.

### Exercise 2

A parent compute budget is 240 units. Reserve is 30; integration platform overhead is 18; four children request 48, 62, 55, and 34 units. Compute margin. A fifth diagnostic child needs 20 units only in maintenance mode, while two operational children are inactive then. Describe the mode-specific analysis needed before accepting it.

### Exercise 3

A decomposition has seven immediate children. Compute unordered pair and directed-cell review opportunities. A register lists nine directed data/control interfaces, three bidirectional physical interfaces, and two shared-resource dependencies. Explain why these numbers cannot be compared directly to the cell counts as a completeness percentage.

### Exercise 4

Critique the decomposition `Autonomous Vehicle -> Hardware, Software, AI, Safety`. Identify at least ten boundary, allocation, interface, lifecycle, or assurance problems. Propose a better first-level decomposition or explain what evidence is needed to choose one.

### Exercise 5

Design a decomposition-closure review for a hospital medication-delivery system. Cover parent-retained outcomes, child elements, people/procedures/facilities, external and internal interfaces, shared resources, budgets, hazards/security/privacy, suppliers, verification, integration, configurations, and branch stopping criteria.

## Answers to the Exercises

### Answer 1

Five of six parent requirements have a recorded disposition: child, joint children, parent retained, or integration. Thus:

$$
C_Q=5/6\approx0.8333=83.33\%.
$$

`Q6` is the structural gap. Review its semantics and parent rationale. It may allocate to one child; derive contributions across several children and an interface; remain a parent-level emergent outcome; become an integration obligation; be invalid/duplicate; or reveal a missing child. The disposition needs authority and trace.

Even 100% declaration coverage would not prove requirements are correct/complete, allocations are sufficient and noncontradictory, children can satisfy them, interfaces compose, budgets close, shared resources work, hazards are controlled, or parent verification/validation is feasible. Coverage is a search aid.

### Answer 2

Operational demand is:

$$
D=48+62+55+34+18=217.
$$

Available after reserve is (240-30=210), so:

$$
Margin=240-30-18-(48+62+55+34)=-7.
$$

The operational allocation already fails by seven units and cannot be repaired by saying the diagnostic child runs only in maintenance. First resolve normal/operational closure.

For maintenance, define exactly which children are inactive and what residual demand, shutdown/startup, monitoring, safety, security, storage, and overhead remains. Suppose the 62- and 55-unit children are truly inactive and their resources are reclaimable; maintenance demand would include 48, 34, diagnostic 20, integration 18, plus any maintenance-specific overhead. The calculation must use maintenance capacity and reserve, not automatically the operational values. Check scheduling, memory, bandwidth, power, latency, diagnostic stimulus/data, isolation, authority, configuration, and transitions. Mode exclusivity and safe intermediate states need verification.

### Answer 3

For (n=7):

$$
N_u=7(6)/2=21
$$

unordered pairs, and:

$$
N_d=7(6)=42
$$

directed cells.

Nine directed interfaces occupy at most nine directed endpoint relations, but several interfaces can share one cell and one interface can include several flows. Three bidirectional physical interfaces may correspond to six directions, mutual coupling without a producer direction, or one controlled boundary each. Two shared-resource dependencies can relate more than two children and may not be represented as pairwise endpoint interfaces. Counts also omit external actors, environment, enabling products, lower-level paths, mode-specific interactions, unintended coupling, and omitted children. Therefore `14/42` or any similar ratio is not a completeness percentage. Review every known pair/direction and discovery source with explicit dispositions.

### Answer 4

Problems include:

1. `Hardware` and `Software` are implementation categories, not outcome-coherent physical children;
2. `AI` likely overlaps software, compute, sensors, data, training, and operations;
3. `Safety` is cross-cutting and cannot absorb every hazard control;
4. sensors, localization, planning, control, actuation, power, structure, communications, human interface, and data ownership are not allocated;
5. runtime versus development/training AI is unclear;
6. physical locations/deployments and vehicle/cloud/facility boundary are absent;
7. command/data/power/mechanical/thermal/human interfaces are absent;
8. fault containment and common causes are hidden;
9. cybersecurity/privacy and trust boundaries are absent;
10. operator, passenger, maintainer, fleet support, procedures, tools, and facilities are absent;
11. manufacturing, calibration, integration, test, update, recovery, and retirement are absent;
12. suppliers, versions, variants, resources, verification, and acceptance are absent.

A candidate first level might include perception/sensing, localization/state estimation, behavior/trajectory management, motion control/actuation, vehicle platform/power/structure, communications/data services, human interaction/operations, and lifecycle support/enabling systems—with system safety/security/configuration retained cross-cutting. This is not automatically correct. Evidence should compare alternative centralization, compute/deployment, sensor/actuator topology, fault/trust zones, supplier products, vehicle types, autonomy scope, operational design domain, regulations, maintenance, update, integration, and resource/hazard models.

### Answer 5

Start with the parent outcome: deliver the right medication/dose/rate to the right patient under authorized clinical intent, detect/respond to faults, preserve privacy/audit, and support safe setup, operation, cleaning, maintenance, update, and retirement. Retain end-to-end clinical outcome, hazard acceptance, configuration compatibility, integrated verification, and validation at parent level.

Candidate children may include medication container/fluid path; pump/actuator; sensing; embedded controller/software; power/battery; enclosure/mechanical; display/controls/alarms; connectivity/gateway; identity/configuration/audit data; and clinical/biomedical work system. External/enabling elements include prescribing/record systems, pharmacy, network/identity/time services, consumables, charging, cleaning, calibration/test equipment, training, maintenance, cybersecurity operations, and disposal.

The review should:

- trace dose, rate, occlusion/air detection, alarm, availability, privacy, cybersecurity, usability, biocompatibility, cleaning, and regulatory obligations to child contributions, interfaces, integration, and parent evidence;
- inspect medication, fluid, mechanical, electrical, data, command, timing, identity, human, cleaning, supplier, and organizational interfaces in setup, normal, alarm, degraded, transport, charging, maintenance, update, recovery, and disposal;
- analyze shared power, time, identity, network, drug library, patient context, operator attention, consumables, and facilities for capacity/common cause;
- close mass/volume, battery/energy, flow/pressure, timing, storage/network, alarm workload, staffing, consumable, and maintenance budgets by configuration/mode;
- link hazards such as wrong patient/drug/dose, free flow, occlusion, air, battery loss, stale library, unauthorized change, alarm overload, contaminated path, and update failure to local and integrated controls;
- pin suppliers, disposable compatibility, software/data versions, evidence, change notice, obsolescence, and field support;
- define child verification/acceptance plus interface, fault-injection, interoperability, human-in-the-loop, cleaning, environmental, cybersecurity, and clinical-use validation;
- derive integration order, simulators, safe fluids, test fixtures, representative networks/records, trained participants, anomaly process, and configuration capture;
- permit different depths: a qualified commercial battery may be a leaf; custom fluid control may decompose further; the work system decomposes until roles/procedures/tools/training can be staffed and evaluated.

Closure is supported only when every parent obligation and lifecycle scenario has accountable child/integration contributions and credible evidence, with residual assumptions and risks explicit. It is not proven by a complete product tree.
