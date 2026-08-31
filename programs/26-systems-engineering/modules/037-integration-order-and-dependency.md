---
module_id: SYSENG-037
program: Systems Engineering
level: 1
module_number: 37
title: Integration Order and Dependency
status: complete
last_verified: 2026-08-31
---

# Integration Order and Dependency

## One-Page Review

### Governing question

In what order should system elements, interfaces, environments, people, data, and evidence be brought together so that each integration step is safe, diagnosable, reversible where needed, and informative about the highest-consequence dependencies?

### Essential definitions

- An **integration item** is a controlled product, service, dataset, model, human work element, external system, or enabling product that participates in an integration step.
- An **integration step** transforms a declared starting configuration into a new integrated configuration by mating, loading, connecting, activating, synchronizing, migrating, or rehearsing selected items under a controlled procedure.
- A **technical dependency** is a condition in which one item, interface, state, resource, decision, environment, or evidence product must exist or satisfy a criterion before another step can validly start or finish.
- A **precedence relation** states that one integration activity must occur before another for a named reason. It is not merely a convenient calendar ordering.
- An **integration increment** is a controlled, internally coherent subset of the intended system assembled to expose selected behaviors and interfaces and produce evidence.
- An **integration state** is the exact configuration after a step: identities and versions, connections, data, calibration, modes, open anomalies, evidence, and permitted next actions.
- A **readiness condition** is an objective entry criterion for an item, environment, team, procedure, interface, or evidence set.
- A **topological order** is a linear ordering of a directed acyclic dependency graph in which every predecessor appears before its successor. Several valid orders may exist.
- A **dependency cycle** is a directed cycle in which every member appears to require another member first. It may reveal bad logic, an inseparable joint increment, or a real iterative maturation loop requiring explicit break conditions.
- A **test double** is a controlled simulator, emulator, stub, mock, fixture, surrogate, or human role-play used in place of an unavailable or unsafe participant, with stated fidelity and limitations.
- **Progressive integration** increases realism, scope, load, authority, environmental stress, and operational consequence in evidence-producing increments.
- **De-integration** is planned separation, rollback, removal, isolation, data restoration, or safe disposal needed after a step, anomaly, replacement, or lifecycle transition.

### Central model, mechanism, or theorem

Let integration activities be vertices (V), with a directed edge ((u,v)\in E) when activity (u) must precede (v). A valid linear sequence (\pi) satisfies:

$$
\forall(u,v)\in E:\quad \pi(u)<\pi(v).
$$

Such a sequence exists exactly when the declared precedence graph is acyclic. For duration (d(v)) and immediate predecessors (Pred(v)), earliest times on a DAG are:

$$
ES(v)=\max_{u\in Pred(v)} EF(u),\qquad EF(v)=ES(v)+d(v),
$$

with (ES(v)=0) when (Pred(v)=\varnothing). This exposes a modeled longest path, but only if activities, dependencies, calendars, resources, and durations are credible.

An activity is executable only when its readiness predicate holds:

$$
Ready(v,k,e,t)=R_{items}\land R_{interfaces}\land R_{configuration}
\land R_{environment}\land R_{procedure}\land R_{people}
\land R_{safety}\land R_{evidence},
$$

for configuration (k), environment (e), and time (t). Graph order is therefore necessary but insufficient: a topologically eligible step can still be technically unready.

### Critical invariants

- Every precedence edge has a technical rationale, owner, applicability, verification method, and change authority.
- Product hierarchy, technical dependency, integration sequence, verification sequence, work schedule, organization, and delivery schedule remain distinguishable and linked.
- Every step declares its starting and ending configurations, items, versions, interfaces, environment, procedure, personnel, hazards, observations, pass/hold/abort criteria, and records.
- No item is connected, energized, loaded, pressurized, moved, authorized, or exposed before required prechecks and protections are satisfied.
- Internal and external interfaces are checked at the correct plane before mating and under representative interaction after mating.
- Configuration identity and evidence remain traceable across hardware, software, firmware, data, models, procedures, tools, facilities, people, and external services.
- High-consequence and high-uncertainty interactions are exposed early enough to change the design, using bounded-fidelity doubles when necessary.
- Each increment is observable and diagnosable enough to localize anomalies; simultaneous uncontrolled changes do not destroy attribution.
- Irreversible or hard-to-access assembly occurs only after the obscured interfaces and required evidence are complete.
- Cycles are resolved by correcting false dependencies, combining inseparable work, providing a bootstrapping asset, or governing an explicit iteration with convergence and exit criteria.
- Parallel activities are allowed only when they do not violate technical, resource, safety, configuration, evidence, or shared-environment constraints.
- Integration anomalies, waivers, deviations, repairs, rework, and retests are recorded against the exact integration state.
- The plan includes de-integration, safe state, rollback, recovery, replacement, and re-entry paths.
- Sequence changes trigger impact analysis across interfaces, facilities, logistics, staffing, test assets, hazards, configuration, verification credit, and downstream evidence.

### Common failures

Common failures include copying the product tree into a calendar; integrating in supplier-delivery order; treating a topological sort as an optimal plan; hiding missing logic with fixed dates; calling every information flow a hard predecessor; ignoring power, clock, identity, data, calibration, environment, operator, and facility dependencies; connecting unverified interfaces because each item passed standalone tests; postponing risky cross-boundary behavior until final assembly; changing several items at once without diagnostic observability; using a mock without a fidelity envelope; sealing inaccessible interfaces before evidence is captured; energizing before grounding, isolation, polarity, limits, and emergency response are ready; treating a dependency cycle as “agile”; confusing product acceptance with integration readiness; failing to version procedures and test data; allowing open anomalies to migrate silently; and planning assembly without rollback or de-integration.

### Compact example

A controller, actuator, power unit, and time service must form an operational increment. Receipt inspection precedes interface prechecks. Protected power and grounding precede energization. The controller can be loaded before the real actuator arrives using an actuator emulator, while the real actuator undergoes mechanical and electrical prechecks. Time synchronization and controller startup precede closed-loop timing tests. Only after polarity, limit, safe-state, command-authority, and emergency-stop checks may the real actuator replace the emulator. This order exposes protocol and timing risk early, preserves safe activation, and delays consequential motion until the required controls and evidence exist.

### Connections

SYSENG-031–034 define interface identities and contracts; SYSENG-035–036 define physical elements and child boundaries. This module converts those structures into dependency and integration-state logic. SYSENG-038 assesses whether a candidate next step is ready; SYSENG-039 controls the configurations being assembled; SYSENG-040 develops the risk-driven integration plan. Verification, validation, risk, configuration, suppliers, human integration, operations, and lifecycle transition all consume the same sequence and evidence.

## Governing Question

Which integration activities truly depend on which others, and how should the available valid orders be shaped to discover dangerous incompatibilities early without creating unsafe, unrepresentative, irreversible, or diagnostically opaque states?

Answering requires more than drawing arrows. Derive dependencies from interface contracts, physical mating, energy and material paths, initialization, data and trust roots, calibration, behavior, environment, human authority, logistics, verification credit, and safe-state needs. Then distinguish hard technical precedence from preference, resource contention, delivery forecast, and organizational convention. Finally select progressive increments that balance risk exposure, representativeness, observability, reversibility, access, cost, schedule, and learning.

## Why This Matters

Subsystems do not spontaneously become a system when delivered to one room or deployed to one cluster. They must be received, identified, inspected, configured, connected, loaded, aligned, calibrated, activated, exercised, diagnosed, corrected, and evidenced in a coherent order. The order changes both safety and knowledge. A bad sequence can damage hardware, corrupt data, invalidate verification credit, conceal an interface mismatch behind several simultaneous changes, or discover an architectural flaw only after it becomes expensive to correct.

NASA's current Product Integration guidance describes developing integration sequences and procedures, confirming configuration documentation, preparing enabling products and the environment, checking received products, and assembling lower-level products into higher-level products while controlling physical, functional, and data interfaces. It says the integration strategy should identify the sequence of receipt, assembly, and activation and should be revisited when production or delivery changes undermine its assumptions. NASA's Integration Plan outline asks what happens in each step and which resources are required when and where.

Current NASA Technical Planning guidance connects the product breakdown structure to technical schedules, workflows, facilities, long-lead resources, responsibilities, reviews, risks, and replanning. NASA Interface Management guidance requires interface prechecks before connection, compatibility evaluation after assembly, interface discrepancy handling, and controlled dissemination of interface changes. NASA Configuration Management guidance emphasizes a true representation of the product through design, assembly, test, integration, operation, and sustainment. These disciplines prevent “integration order” from becoming an isolated Gantt-chart exercise.

A dependency graph helps reason about permissible order. NIST defines topological sorting as arranging partially ordered items; the essential application here is that technical predecessors must precede successors. GAO schedule guidance warns that missing or incorrect dependencies corrupt float and critical-path conclusions. Yet integration engineering is not reducible to schedule mathematics. A DAG omits fidelity, safety, authority, configuration, evidence quality, physical access, common resources, uncertain durations, and human readiness unless engineers model them.

The most informative order is not always bottom-up by product hierarchy. A critical end-to-end protocol may be exercised early through models and emulators before flight hardware exists. A hazardous physical connection may wait until protective functions are verified. An inaccessible connector may require inspection and continuity evidence before enclosure closure. A new supplier interface may be integrated before familiar internal functions. Integration progresses across several ladders—scope, realism, environmental stress, load, authority, and consequence—not one universal sequence.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. the selected physical architecture, subsystem decomposition, product hierarchy, build/make-buy-reuse strategy, and exact configurations;
2. internal and external interfaces with endpoints, planes, assumptions, guarantees, modes, versions, prechecks, and change status;
3. logical behavior, end-to-end scenarios, initialization, state/mode transitions, fault response, recovery, and shutdown;
4. product acceptance and verification evidence, open anomalies, deviations, waivers, limitations, and required retest;
5. physical mating, access, alignment, handling, cleanliness, grounding, power, pressure, thermal, fluid, network, identity, time, data, calibration, and authority dependencies;
6. facilities, tools, fixtures, simulators, emulators, instrumentation, test data, networks, external systems, trained people, permits, logistics, and spares;
7. hazard controls, safe intermediate states, stop-work authority, emergency response, rollback, de-integration, and recovery;
8. basic directed graphs, cycles, partial orders, longest paths, schedule logic, uncertainty, and configuration control.

As a retrieval test, inspect “install software after hardware arrives.” Ask what hardware identity, firmware, boot chain, power, network, credentials, storage, clock, configuration service, loader, rollback image, license, test data, operator authority, and evidence must exist. Ask whether an emulator can retire protocol risk sooner, whether installation changes the verified baseline, and what happens after a failed load. A delivery event is not a sufficient technical dependency.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish integration items, steps, increments, states, dependencies, precedence, readiness conditions, and schedule links;
2. derive dependencies across physical, functional, data, energy, environmental, human, supplier, configuration, and evidence domains;
3. build and review a directed dependency graph and compute valid topological orders and elementary earliest times;
4. diagnose cycles and choose among correction, joint integration, bootstrapping assets, or bounded iteration;
5. select risk-driven progressive increments using test doubles with explicit fidelity limits;
6. specify step-level entry, procedure, observation, pass, hold, abort, rollback, evidence, and exit conditions;
7. plan safe activation and irreversible assembly while preserving access and diagnostic isolation;
8. coordinate parallel integration without violating shared-resource, configuration, facility, or evidence constraints;
9. replan sequence after delivery, design, anomaly, supplier, facility, or configuration change without losing traceability;
10. state what sequence analysis establishes and what still requires readiness review, execution evidence, verification, and validation.

## Core Exposition

**Declare the integration objective and level.** Name the parent product or operational capability being integrated, the lifecycle phase, decision, product layer, target configuration, environment, authority, and evidence objective. Component bench integration, subsystem integration, system assembly, external-system interoperability, operational rehearsal, replacement, and de-integration have different participants and success criteria.

**Represent an integration step as a controlled transformation.** Record stable step ID; purpose and risk addressed; starting integration state; items and versions introduced/removed; interfaces changed; preconditions; procedure and responsible roles; facilities/tools/data; hazards and controls; observations; expected results; pass, hold, abort, and rollback criteria; ending state; evidence; anomalies; and allowed successors. “Connect A to B” is not executable control.

**Separate product containment from precedence.** A product hierarchy says what contains what. It does not say that every child must integrate before any cross-child risk can be exercised, nor which sibling comes first. Build structure, dependency graph, deployment, verification hierarchy, work packages, organizations, suppliers, and calendars are related but different views. Link them through stable identities.

**Derive dependencies from causality and validity.** Ask why a predecessor is required. Categories include physical access and support; structural load path; alignment; cleanliness; energy source and isolation; thermal control; pressure/fluid containment; electrical reference/ground; network path; identity, key, and authorization; clock/time; schema/reference data; calibration; software/firmware compatibility; initialization/state; safety interlock; environmental qualification; trained operator; external approval; and evidence needed to grant credit.

**Classify dependency semantics.** Common schedule relations—finish-to-start, start-to-start, finish-to-finish, and bounded lag—can represent timing, but technical semantics must remain explicit. `A before B` may mean B would be impossible, unsafe, invalid, unobservable, unrepresentative, or merely less convenient without A. Label hard technical precedence, soft preference, shared-resource exclusion, information dependency, delivery forecast, and risk-reduction preference separately.

**Challenge every hard edge.** For edge ((u,v)), record the condition produced by (u), consumed by (v), observation proving it, applicability, and consequence of violation. Ask whether the condition could be supplied by a qualified double, checked independently, or combined into one joint step. False hard edges serialize work and hide options; missing edges create unsafe or invalid sequences.

**Review graph completeness.** Start from product and interface structures, then add enabling products, external systems, people, data/configuration, verification evidence, and safe-state activities. Inspect every integration step for unmodeled predecessors. Review fan-in steps carefully: an end-to-end demonstration may require not just products but compatible versions, representative data, synchronized clocks, populated credentials, facilities, approved procedures, and trained participants.

**Find cycles before scheduling.** A topological order exists only for an acyclic graph. A cycle such as `identity needs network`, `network admission needs identity`, and `identity configuration needs admitted network` is not solved by choosing an arbitrary first activity. Possible resolutions include an out-of-band bootstrap credential, factory provisioning, a restricted commissioning network, a jointly controlled activation step, or architecture change.

**Distinguish feedback from impossible precedence.** Engineering maturation is iterative: integrate, observe, correct, and reintegrate. Model each pass as a bounded activity with entry/exit criteria and configuration identity, not as a timeless directed cycle in a one-pass precedence graph. If convergence is uncertain, treat it as risk and forecast rework branches; do not pretend iteration has zero duration.

**Compute eligible orders, then engineer the choice.** A topological sort returns one permissible order, not the best order. When multiple vertices are eligible, compare interface risk, consequence, uncertainty, access, reversibility, diagnostic value, fidelity, availability, resource use, downstream leverage, and change cost. Preserve the rationale for priority decisions.

**Use risk-driven early integration.** Integrate novel, tightly coupled, high-consequence, supplier-controlled, timing-sensitive, or hard-to-change interfaces early enough that evidence can alter architecture. “Early” means early relative to the last responsible design decision, not necessarily with final articles. Use contract tests, models, breadboards, emulators, digital environments, samples, or human mockups as appropriate.

**Bound every test double.** Record what the double represents, version, interface plane, timing/value/error/failure fidelity, omitted behaviors, configuration, validation evidence, owner, and retirement/replacement plan. Passing against a fast in-memory mock does not prove behavior over a lossy network; a mass simulator does not prove structural dynamics; a role-play does not prove staffing under sustained operations.

**Progress along several dimensions.** An increment can increase participant count, interface count, physical realism, software/data fidelity, environmental range, load/stress, failure injection, duration, operational staffing, external connectivity, or control authority. State which dimensions change. Avoid jumping simultaneously from a benign bench setup to full authority, peak load, harsh environment, and external operations; attribution and safety suffer.

**Design for observability and fault isolation.** Instrument interface planes, clocks, energy/material flows, state transitions, command authority, errors, environment, human actions, and configuration. Establish time correlation and data custody. Introduce a small enough change set that evidence can distinguish likely causes. Diagnostic access and temporary test points are controlled interfaces with removal or operational-security plans.

**Protect physical access.** Sequence measurements, inspections, torque witnesses, leak checks, continuity, fiber inspection, alignment, calibration, photography, identification, and interface verification before later assembly makes them inaccessible. Confirm the evidence belongs to the exact installed item and state. Plan how rework reopens, retests, and recloses the configuration.

**Plan receipt and prechecks.** Verify identity, version, configuration, preservation, shipping/environmental history, damage, cleanliness, calibration, certificates, open anomalies, documentation, and acceptance limitations. Before mating, check dimensions, keying, polarity, voltage, pinout, protocol/version, units, pressure, cleanliness, clock, credentials, data schema, command authority, and safe state at each applicable interface plane.

**Plan safe activation.** Establish grounding/bonding, isolation, protective devices, pressure containment, thermal path, cooling/lubrication, emergency stop, limit enforcement, access exclusion, fire/chemical controls, cybersecurity boundaries, valid configuration, monitoring, and authorized roles before energy or authority is applied. Use staged energization, current/pressure limits, inhibited outputs, restricted privileges, and controlled test values where appropriate.

**Treat software, data, and trust as integration items.** Firmware, operating system, container/image, configuration, schema, migration, seed data, models, certificates, keys, policies, identities, feature flags, time sources, and observability agents have versions and dependencies. Loading software changes the integrated configuration. Plan install, compatibility, backup, rollback, data reconciliation, key recovery, and audit evidence.

**Integrate humans and operations.** Operators, maintainers, administrators, safety personnel, incident responders, logistics, and external partners interact through information, authority, procedures, tools, workload, space, environment, training, and shift/handoff. Integrate representative work before final validation. A technically functional increment can remain operationally unusable or unsafe.

**Include external systems and natural/induced environments.** Networks, facilities, vehicles, regulators, partner services, suppliers, users, weather, loads, vibration, thermal, electromagnetic, contamination, and operational tempo may dominate behavior. Use bounded simulations early, then increase representativeness. Define responsibility and evidence at the external boundary.

**Distinguish acceptance, readiness, integration checks, verification, and validation.** A received child may be accepted against its specification but unready because its version, interface, anomaly status, handling, or evidence is incompatible with the planned step. Post-mating functional checks show the assembly is ready for further work; they do not automatically constitute formal verification or stakeholder validation. Map any intended evidence credit explicitly.

**Define readiness per step.** Confirm the required items and doubles; exact configuration; interface prechecks; environment/facility; tools/instrumentation calibration; data and cyber controls; procedure maturity; trained and authorized people; hazards/permits/emergency response; prior evidence; anomaly dispositions; rollback assets; logistics; and downstream capacity. SYSENG-038 deepens this assessment.

**Plan parallel work honestly.** Two graph-eligible activities may still compete for the same article, facility, bench, network, license, specialist, safety observer, test data, or configuration. They may produce incompatible changes or contaminate evidence. Model resource and configuration exclusions separately from causal precedence; otherwise temporary constraints become permanent architecture lore.

**Relate the dependency graph to schedule logic.** Assign credible durations, calendars, availability, and resources only after technical activities and edges are sound. Compute earliest/latest dates, float, critical and near-critical paths, and uncertainty using appropriate program methods. A longest path in an incomplete or date-constrained network is not reliable. Technical risk can warrant attention even off the modeled critical path.

**Manage integration states, not just completed activities.** After every step, record installed/active items, serials/builds/versions, connections, settings, calibrations, data, environmental exposure, test equipment, procedure revision, results, anomalies, repairs, waivers, evidence, and custody. Define whether the state is safe to hold, ship, store, test, modify, operate, or de-integrate.

**Control anomalies and re-entry.** Stop or hold at declared criteria. Preserve evidence before disturbing the state. Bound affected items and prior evidence; investigate without uncontrolled configuration changes; authorize repair/workaround/deviation; identify required regression and interface retest; and define the exact re-entry point. “Continue and fix later” lets uncertainty propagate.

**Plan rollback and de-integration.** For software, preserve backups, compatible schemas, credentials, and reconciliation paths. For hardware, preserve access, lifting/handling, plugs/covers, safe discharge, contamination controls, replaceable consumables, and inspection requirements. For operational changes, preserve fallback roles, communications, authority, and data custody. Some transitions are irreversible; make that constraint explicit before execution.

**Replan from changed facts.** Late delivery, design change, failed test, unavailable facility, expired calibration, supplier replacement, security advisory, anomaly, or altered external system can invalidate edges, readiness, doubles, durations, and evidence credit. Update the dependency model, configurations, interfaces, hazards, resources, and downstream procedures together. Do not simply drag a schedule bar.

**State evidence limits.** A complete acyclic graph proves only that the declared precedence relations permit a linear order. A computed critical path is conditional on network logic and estimates. A successful increment supports only its articles, versions, conditions, procedures, observations, and criteria. Neither graph nor demonstration alone proves final system verification, validation, production, operational readiness, or lifecycle fitness.

The following checker evaluates a small declared precedence model. It does not establish readiness, safety, resource availability, evidence quality, or optimality.

<!-- bijux-verify: {"id":"integration-precedence-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"activities_total=7\ntopological_order=receive,power,time,control,actuator,end_to_end,external\ncritical_finish_days=18\ncycle_detected=0\nundeclared_prerequisites=external:ops_ready\nevidence=declared_precedence_only\n","stderr":""}} -->
```python
activities = {
    "receive": {"duration": 2, "requires": []},
    "power": {"duration": 3, "requires": ["receive"]},
    "time": {"duration": 2, "requires": ["power"]},
    "control": {"duration": 4, "requires": ["power", "time"]},
    "actuator": {"duration": 5, "requires": ["receive"]},
    "end_to_end": {"duration": 3, "requires": ["control", "actuator"]},
    "external": {"duration": 4, "requires": ["end_to_end", "ops_ready"]},
}
order = ["receive", "power", "time", "control", "actuator", "end_to_end", "external"]
position = {name: index for index, name in enumerate(order)}
declared_edges = [
    (dependency, name)
    for name, item in activities.items()
    for dependency in item["requires"]
    if dependency in activities
]
cycle = any(position[dependency] >= position[name] for dependency, name in declared_edges)
earliest_finish = {}
for name in order:
    known = [dependency for dependency in activities[name]["requires"] if dependency in activities]
    earliest_start = max((earliest_finish[dependency] for dependency in known), default=0)
    earliest_finish[name] = earliest_start + activities[name]["duration"]
undeclared = sorted(
    f"{name}:{dependency}"
    for name, item in activities.items()
    for dependency in item["requires"]
    if dependency not in activities
)
print(f"activities_total={len(activities)}")
print("topological_order=" + ",".join(order))
print(f"critical_finish_days={earliest_finish['external']}")
print(f"cycle_detected={int(cycle)}")
print("undeclared_prerequisites=" + ",".join(undeclared))
print("evidence=declared_precedence_only")
```

The calculated 18 days ignore the missing `ops_ready` activity. The checker exposes rather than repairs that incompleteness; it also assumes the proposed order, durations, calendars, resources, and every other declared edge are correct.

## Definitions and Notation

Let activities be (V), declared directed dependencies (E\subseteq V\times V), configuration set (K), environments (H), integration items (P), and evidence records (D). For activity (v):

$$
Pred(v)=\{u\in V:(u,v)\in E\},\qquad Succ(v)=\{w\in V:(v,w)\in E\}.
$$

A sequence (\pi:V\rightarrow\{1,\ldots,|V|\}) is topologically valid when:

$$
\forall(u,v)\in E:\ \pi(u)<\pi(v).
$$

The eligible frontier after completed set (X\subseteq V) is:

$$
Eligible(X)=\{v\in V\setminus X:Pred(v)\subseteq X\}.
$$

Eligibility is graph-theoretic; executability additionally requires (Ready(v,k,h,t)).

For deterministic activity durations on an acyclic network:

$$
ES(v)=\max_{u\in Pred(v)}EF(u),\quad EF(v)=ES(v)+d(v).
$$

The modeled completion time is (\max_v EF(v)). A path attaining it is a longest path under the declared durations. Resource constraints, calendars, uncertainty, rework, and omitted logic can change the actual result.

Define the starting state (S^-_v) and ending state (S^+_v) of step (v). The procedure is a controlled transition:

$$
T_v:S^-_v\times Inputs_v\rightarrow S^+_v\times Evidence_v\times Outcome_v,
$$

where (Outcome_v\in\{pass,hold,abort\}) and rollback/de-integration rules constrain safe successor states. This notation is descriptive; execution remains a physical, computational, and human process.

Dependency records should include `edge_id`, predecessor, successor, condition produced/consumed, type, rationale, interface/state/resource, applicability, evidence, owner, criticality, workaround/double, and change authority. Activity records should include the step fields defined in the exposition.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—dependency elicitation.** Walk the product hierarchy, every registered interface, end-to-end scenario, state transition, budget, hazard control, verification objective, external system, enabling product, and lifecycle condition. For each intended step, ask what must already be true and how that truth is observed. This produces candidate edges and readiness conditions.

**Mechanism 2—semantic normalization.** Separate technical precedence from scheduling preference, resource exclusion, information need, delivery expectation, and iterative feedback. Remove duplicated transitive links only when doing so does not erase rationale or governance; a transitive reduction useful for visualization is not necessarily the authoritative dependency record.

**Mechanism 3—cycle analysis.** Run a cycle-detection or topological-sort check. For every strongly coupled cycle, examine whether an edge is false, whether members form one joint integration action, whether a bootstrap/double supplies the first valid state, or whether the cycle represents repeatable maturation. Record convergence/exit and maximum tolerated rework where iteration remains.

**Mechanism 4—increment design.** Choose a target behavior/interface/risk, minimal controlled participants, representative enough doubles, observation points, starting/ending configurations, and evidence criterion. Increase realism and consequence deliberately. Preserve a working reference increment when possible so new items can be compared against a known state.

**Mechanism 5—safe and diagnosable execution.** Gate entry, perform prechecks, capture baseline state, execute a versioned procedure, observe expected and adverse behavior, apply pass/hold/abort criteria, record anomalies without destroying evidence, and authorize the ending state. Control temporary patches and test configurations.

**Mechanism 6—evidence-aware progression.** Map each result to the claim it supports and its limitations. Decide whether the result grants integration check, verification credit, risk retirement, or only diagnostic information. Do not propagate credit across changed items, conditions, or procedures without rationale.

**Mechanism 7—continuous replanning.** Update edge conditions, readiness, item configurations, resource availability, risk priorities, and schedule logic as evidence arrives. Compare the new critical and near-critical paths, but also inspect high-consequence technical dependencies off those paths.

The core proof obligation for a proposed order is limited:

1. every declared hard predecessor occurs earlier;
2. the graph has no unresolved hard-dependency cycle;
3. every executed step satisfies its non-graph readiness predicates;
4. every state transition preserves declared safety, configuration, and evidence invariants;
5. each claimed integration/verification conclusion follows only within the evidence domain.

Items 3–5 cannot be proved by a topological sort. They require review and execution evidence.

## Alternatives and Trade-Offs

**Bottom-up product integration** fits hierarchical assembly and local verification, but can defer cross-branch behavior. **Thread-first integration** exercises an end-to-end mission or user thread early, but may depend heavily on doubles and cover only one scenario. Most systems combine them.

**Big-bang integration** reduces intermediate-environment construction but creates poor fault isolation, late discovery, and large rollback scope. **Incremental integration** improves learning and attribution but costs fixtures, doubles, automation, configuration control, and repeated regression.

**Hardware-first** can retire fit, power, thermal, and physical-interface risk. **Software/data-first virtual integration** can retire protocol, schema, behavior, and automation risk sooner. Neither proves the other domain; hybrid benches often provide better cross-domain learning.

**Risk-first ordering** attacks uncertainty and consequence early. **Availability-first ordering** keeps resources busy. Availability may be sensible when it produces reusable evidence, but it must not silently become architecture or force unsafe final sequence.

**Real article integration** provides higher representativeness but risks damage, scarcity, and schedule. **Test doubles** enable earlier, safer work but can conceal behavior outside their fidelity envelope. Plan staged replacement and regression.

**Strict serial integration** simplifies state attribution and scarce-article control. **Parallel integration** shortens elapsed time when branches and resources are genuinely independent, but increases configuration reconciliation and shared-environment risk.

**Permanent integration facilities** support repeatable regression and operations rehearsal. **Temporary project facilities** may cost less initially but can make later anomalies, updates, and sustainment hard to reproduce. Consider lifecycle ownership.

**Automated procedures** improve repeatability, capture, and scale. **Manual procedures** can handle novel physical work and judgment. Automation itself needs versioning, validation, authorization, safe failure, and human recovery.

## Failure Modes and Misconceptions

**“The product tree gives the order.”** Containment suggests assembly layers but misses sibling, cross-level, external, enabling, data, human, and environmental dependencies.

**“Delivered first means integrated first.”** Delivery order is an availability fact. The item may be technically unready or low-value to integrate; a double may better address the next risk.

**“A DAG is an integration plan.”** It omits procedure, configuration, readiness, safety, facilities, people, observation, evidence, anomalies, rollback, and authority.

**“Any topological order is equally good.”** Valid orders differ in risk discovery, access, reversibility, diagnostic power, resource use, fidelity, and cost of change.

**“A cycle means the project is iterative.”** It may mean contradictory prerequisites. Genuine iteration needs an initial state, controlled repetitions, convergence measure, and exit condition.

**“Standalone verification makes an item ready.”** Interface compatibility, exact version, anomaly status, handling, installation, environment, and planned evidence can still be inadequate.

**“Mocks remove dependencies.”** They defer or transform them. The double introduces fidelity, version, ownership, validation, and replacement dependencies.

**“Parallel graph nodes can run in parallel.”** Shared articles, facilities, people, networks, configurations, hazards, or evidence can prohibit it.

**“The critical path identifies all important integration work.”** It is conditional on schedule logic and estimates; a noncritical high-consequence interface can still deserve urgent evidence.

**“Functional checkout is formal verification.”** It may only establish readiness for the next step. Evidence credit depends on controlled requirements, article, method, environment, procedure, criterion, and record.

**“Software integration is reversible.”** Schema changes, data side effects, key rotation, external messages, firmware, and mixed-version operation can make rollback incomplete or dangerous.

**“Anomaly work can happen in place.”** Uncontrolled troubleshooting changes configuration and destroys causal evidence. Hold, record, authorize, and define re-entry.

**“Final operational integration is the first real test.”** It is the least affordable place to discover basic contract and initialization defects. Earlier bounded environments should retire those risks while preserving a final representative evaluation.

## Worked Examples

### Example 1

**Topological order is valid but not unique.** Activities are receipt inspection (R), power precheck (P), actuator precheck (A), controller/time integration (C), closed-loop integration (L), and external demonstration (X). Edges are (R\to P), (R\to A), (P\to C), (A\to L), (C\to L), and (L\to X).

`R,P,C,A,L,X` and `R,A,P,C,L,X` are both valid. `R,P,C,L,A,X` is invalid because (A) must precede (L). Choosing between the valid sequences depends on facility availability, actuator risk, controller emulator fidelity, diagnostic access, and the value of early timing evidence. The graph constrains; engineering selects.

### Example 2

**Bootstrap cycle.** A device needs network access to fetch identity configuration; network admission requires device identity; identity issuance requires an attested device state reported over the admitted network. The declared graph cycles.

The team defines a factory-installed bootstrap identity and a restricted commissioning network that permits only attestation and identity issuance. Successful enrollment replaces the bootstrap credential, records the device/configuration, and transitions to normal admission. Abort revokes partial credentials and returns the device to a controlled state. The cycle was resolved by architecture and procedure, not by ignoring an edge.

### Example 3

**Early API integration with a bounded emulator.** A supplier service is late, but its versioned API contract is high risk. An emulator implements request/response schemas, authentication errors, idempotency, rate limits, 50–300 ms latency, selected timeouts, and replayable faults. It omits supplier regional failover and undocumented throttling interactions.

Client contract tests and end-to-end transaction traces retire local serialization, retry, and duplicate-side-effect defects. They do not prove production availability or failover. When the supplier sandbox and then production-like environment arrive, the same tests run with representative network, credentials, quotas, observability, and failure conditions. Evidence stays partitioned by environment.

### Example 4

**Seal only after inaccessible evidence.** A sensor harness and fluid line will be hidden after an enclosure panel is bonded. Required predecessors include identity/configuration capture, connector inspection, pin-to-pin continuity and insulation checks, pressure/leak test, cleanliness check, routing/strain/clearance inspection, calibration, photographs, anomaly closure, and independent witness where required.

Only then may bonding proceed. A later failed end-to-end check triggers a controlled decision: diagnose through accessible planes, or de-bond using an approved repair process and repeat every invalidated check. Calendar pressure cannot convert inaccessible unknowns into acceptable evidence.

### Example 5

**Safe staged activation.** A motion system requires protective earth/bonding, supply polarity and limits, mechanical restraint, travel limits, emergency stop, inhibited command output, current monitoring, cleared exclusion area, approved procedure, and authorized operators before power.

Activation proceeds with low current limit and outputs inhibited; verifies rails and communications; checks sensor direction and limits using nonhazardous stimulus; enables low-speed motion; verifies emergency stop and safe state; then increases authority and load. Each stage has abort thresholds. “Power before software” versus “software before power” is too crude: safe power, boot, control, and authority states interleave.

### Example 6

**Late actuator delivery and an emulator.** The actuator is eight weeks late. A force/motion emulator lets the controller, command path, timing, fault handling, operator interface, logging, and integration automation mature. A mass/inertia fixture separately exercises mounting and handling. Neither represents actuator thermal behavior, backlash, saturation, electromagnetic effects, or real failure modes.

The plan records which tests receive provisional credit and which must repeat with the production-representative actuator. Emulator use changes the near-term order without erasing the real actuator dependency.

### Example 7

**Database migration is an integration sequence.** A service schema change affects old/new applications, data writers/readers, replication, analytics, backup/restore, and rollback. The team first deploys backward-compatible schema support, then new dual-capable code, observes mixed-version behavior, backfills with reconciliation, switches reads, stops old writes, and removes compatibility only after rollback and retention conditions expire.

Each step records schema/application versions, data counts/hashes, lag, errors, backups, feature flags, authority, and rollback boundary. A destructive migration first would make software rollback nominally available but data rollback false.

### Example 8

**Shared time is a hidden fan-in dependency.** Four subsystems pass pairwise tests using one laboratory time source. The operational design uses two time sources with switchover, holdover, certificates, network distribution, monitoring, and operator recovery. End-to-end ordering, timeout, and audit behavior depends on the full service.

The plan adds time-degraded and switchover increments before final operations, measures uncertainty at every consumer plane, and injects stale, stepped, lost, and conflicting time. Pairwise success did not cover the shared operational dependency or common cause.

### Example 9

**Operations work enters the integration graph.** A facility equipment increment is technically assembled, but hazardous-energy isolation requires trained operator and maintainer roles, permits, locks/tags, communication, shift handoff, access control, protective equipment, emergency response, and management authority.

Procedure walkthroughs precede controlled equipment rehearsal; representative staffing and off-nominal scenarios precede operational validation. The graph includes training qualification, facility readiness, emergency-team availability, and procedure baseline. People are not scheduled decoration around a machine-only graph.

### Example 10

**A change invalidates order and evidence.** A network gateway replacement changes power draw, connector, firmware, certificates, timing, management API, logging, and supplier support. It has passed supplier acceptance.

Impact analysis revisits power/thermal activation, harness mating, identity bootstrap, configuration tooling, observability, security accreditation, end-to-end timing, failure injection, rollback, spares, training, and external interoperability. Prior tests retain credit only where their claim does not depend on changed behavior. The dependency graph, readiness records, procedures, schedule, and configuration baseline are revised together.

## Cross-Program Connections

**Platform engineering.** Platform integration orders control/data planes, compute, network, storage, identity, observability, policy, deployment, regions, and operator workflows; emulated infrastructure and progressive authority are central.

**API and service engineering.** Consumer/provider contract tests, sandboxes, schema compatibility, identity, quotas, retries, failure injection, and mixed-version rollouts form a service integration graph distinct from team delivery dates.

**Data engineering.** Schema evolution, backfill, replay, dual write/read, lineage, quality, reconciliation, retention, and rollback require explicit precedence and state evidence to avoid irreversible corruption.

**Object-oriented programming.** Build dependencies and object construction order resemble precedence, but runtime services, physical assets, data migrations, people, and lifecycle evidence extend beyond package graphs.

**Functional programming.** Pure transformation pipelines make some data dependencies explicit; effects, resources, external state, failure, deployment, and human authority still require controlled integration sequencing.

**Project scheduling.** Technical dependency supplies schedule logic; calendars, resources, uncertainty, cost, and delivery forecasts add program constraints. Neither view should overwrite the other.

**Safety and security.** Safe activation, privilege progression, bootstrap trust, fault containment, emergency response, and negative testing govern permissible intermediate states.

**Verification and validation.** Integration creates articles and states on which verification/validation operate. Evidence credit must be mapped explicitly rather than inferred from activity completion.

## References

1. NASA, *Systems Engineering Handbook, Section 5.2: Product Integration*, current web edition. <https://www.nasa.gov/reference/5-2-product-integration/>
2. NASA, *Systems Engineering Handbook, Appendix H: Integration Plan Outline*, current web edition. <https://www.nasa.gov/reference/appendix-h-integration-plan-outline/>
3. NASA, *Systems Engineering Handbook, Section 6.1: Technical Planning*, current web edition. <https://www.nasa.gov/reference/6-1-technical-planning/>
4. NASA, *Systems Engineering Handbook, Section 6.3: Interface Management*, current web edition. <https://www.nasa.gov/reference/6-3-interface-management/>
5. NASA, *Systems Engineering Handbook, Section 6.5: Configuration Management*, current web edition. <https://www.nasa.gov/reference/6-5-configuration-management/>
6. NASA, *Systems Engineering Handbook, Section 5.3: Product Verification*, current web edition. <https://www.nasa.gov/reference/5-3-product-verification/>
7. NASA, *NPR 7123.1B: NASA Systems Engineering Processes and Requirements*, Change 4. <https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL>
8. Paul E. Black, NIST, *Dictionary of Algorithms and Data Structures: topological sort*, updated 2022. <https://xlinux.nist.gov/dads/HTML/topologicalSort.html>
9. U.S. Government Accountability Office, *Schedule Assessment Guide: Best Practices for Project Schedules*, GAO-16-89G. <https://www.gao.gov/products/gao-16-89g>
10. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>

## Exercises

### Exercise 1

Activities and durations in days are: `R=2`, `P=3`, `D=4`, `C=5`, `E=2`, `X=3`. Edges are (R\to P), (R\to D), (P\to C), (D\to C), (C\to E), and (E\to X). Compute earliest start/finish for every activity and modeled completion time. Give two consequences of an omitted external-operations predecessor for (X).

### Exercise 2

A proposed graph says: credentials require identity service; identity service requires the database; database startup requires storage keys; storage-key release requires authenticated credentials. Diagnose the cycle. Give at least three valid resolution patterns and the evidence needed before normal operation.

### Exercise 3

Review this order for a high-energy actuator: mount; connect power; energize; load controller; test emergency stop; configure travel limits; clear personnel; run motion. Identify at least ten missing or misordered conditions and propose a safer staged order with hold/abort evidence.

### Exercise 4

A payment client passed 200 tests against a mock. The mock has zero network latency, never throttles, returns ordered responses, implements only success and one timeout, shares the client clock, and does not persist idempotency keys. What conclusions are supported? Design the next three increments and state the remaining limitations after each.

### Exercise 5

A hospital medication-delivery platform integrates pump hardware, embedded software, drug library, patient identity, clinical orders, network/time/identity services, alarms, nurses, biomedical maintenance, pharmacy, and record system. Sketch a risk-driven integration dependency plan including configuration, test doubles, safe states, human work, external systems, anomalies, rollback, and evidence limits.

## Answers to the Exercises

### Answer 1

For source (R):

$$
ES_R=0,\quad EF_R=2.
$$

Then (P) and (D) can proceed:

$$
ES_P=2,\ EF_P=5;\qquad ES_D=2,\ EF_D=6.
$$

(C) waits for both:

$$
ES_C=\max(5,6)=6,\quad EF_C=11.
$$

Then:

$$
ES_E=11,\ EF_E=13;\qquad ES_X=13,\ EF_X=16.
$$

Modeled completion is 16 days, with (R\to D\to C\to E\to X) as the duration-determining path under these assumptions. If external-operations readiness is omitted, (X) may appear eligible before the external environment, accounts, data, approvals, staff, or procedures exist; the 16-day forecast and computed float are then false. Execution could also produce invalid evidence or unsafe effects because the intended operational boundary was absent. Add the activity/condition, credible duration/resources/calendar, and evidence rather than inserting a date constraint.

### Answer 2

The four activities form a hard directed cycle, so no one-pass topological order exists. Choosing one arbitrarily violates a declared prerequisite. Resolution patterns include:

1. provision a bounded bootstrap credential at manufacture or controlled enrollment, then replace/revoke it after identity-service activation;
2. release storage keys through an independent hardware/root-of-trust or authorized offline ceremony, with normal credentials used afterward;
3. use a restricted commissioning environment in which only database/identity bootstrap actions are allowed;
4. combine database, identity, and credential activation into one jointly controlled step with internal subprocedure and abort behavior;
5. change the architecture so the database can start encrypted with a separately governed recovery/unseal mechanism.

Evidence includes exact hardware/software/key/policy configuration; custody and authorization; attestation; restricted-path enforcement; audit; database integrity; identity issuance; credential replacement/revocation; restart, partial-failure, rollback, recovery, and attack tests; and proof that bootstrap privileges cannot persist or reach normal functions. A successful nominal boot alone does not establish security or operational recovery.

### Answer 3

Problems include missing identity/configuration receipt; damage/cleanliness inspection; mounting integrity/alignment; grounding/bonding; supply polarity/voltage/current limits; connector/pinout check; mechanical restraint; travel envelope; cooling/lubrication; inhibited outputs; controller/firmware compatibility; sensor direction/calibration; emergency-stop wiring and independent check; protective devices; exclusion area; hazard analysis/permit; trained authorized staff; instrumentation; approved procedure; communications/command authority; safe-state definition; rollback; and abort thresholds. Emergency stop, limits, and personnel clearing occur too late.

A safer order is: inspect and identify; establish configuration; mount/restraint/alignment; connect protective earth and verify bonding; verify power/interface de-energized; check polarity/limits/connectors; install and verify travel limits and emergency stop through non-energy checks; establish cooling/lubrication and monitoring; load/verify controller with outputs inhibited; clear/guard the area and brief authorized staff; energize at restricted current with outputs inhibited; verify rails, state, communication, sensors, and no unintended motion; test safe-state paths with bounded stimulus; enable low authority/speed through controlled motion; verify direction, limits, stop, and fault response; then increase range/load progressively.

Hold on any configuration, interface, protection, staffing, or observation gap. Abort on unexpected energy, motion, current, temperature, pressure, state, communication loss, protection failure, or boundary violation. Record exact configuration, measured checks, procedure revision, people, environment, traces, anomalies, and post-step state. Domain specialists must set actual thresholds.

### Answer 4

The 200 passes support client behavior only for the mock's implemented request/response cases, client build, test data, and local environment. They may reveal deterministic serialization or handling defects. They do not support real latency, throttling, reordering, duplicate delivery, idempotency persistence, independent clocks, authentication, availability, regional failover, or production correctness. Test count is not coverage proof.

Next increments could be:

1. **Adversarial emulator:** add latency/jitter, loss, reordering, throttling, duplicate/late responses, independent clock skew, authentication failures, persistent idempotency state, restart, and bounded fault scripts. This supports specified client behavior against the emulator, but fidelity to the provider remains unproven.
2. **Provider sandbox/contract environment:** run the same versioned suite with real credentials, network, quotas, schema, idempotency, observability, and provider-documented faults. This supports sandbox compatibility, not production scale, regional behavior, or full failure envelope.
3. **Production-like then controlled operational increment:** use representative topology/load/data/security/monitoring, canary authority, reconciliation, stop limits, and rollback; inject only authorized failures. This increases operational representativeness, but observation duration, rare failures, provider changes, peak events, and external dependencies still bound the conclusion.

Preserve which tests passed in which environment; do not collapse all 200+ results into one compatibility claim.

### Answer 5

Begin with the parent clinical outcome and hazards: correct patient/drug/dose/rate/order, authorized changes, timely alarms, safe interruption/recovery, privacy/audit, and usable clinical work. Pin pump/firmware/software/drug-library/schema/network/identity/time/order-record versions, disposables, test fluids, calibration, roles, procedures, facility, and evidence.

A risk-driven plan might:

1. verify received pump identity, configuration, calibration, power/battery, fluid-path integrity, sensors, actuator limits, safe state, alarm outputs, service interfaces, and anomalies;
2. integrate embedded control with pump/sensor simulators and safe fluid fixtures; exercise startup, occlusion, air, free-flow controls, battery loss, restart, watchdog, update/rollback, and evidence capture before patient authority;
3. integrate versioned drug library and order/patient schemas using synthetic data, contract tests, boundary values, stale/conflicting versions, signature/authorization, provenance, and rollback;
4. integrate network, independent time, identity, certificates, audit, and record/order service doubles with latency, loss, clock faults, denial, duplicate messages, disconnection, reconciliation, and least privilege;
5. replace doubles progressively with pharmacy, clinical-order, record, identity, time, and network test environments, preserving compatibility and data-cleanup boundaries;
6. integrate display, controls, alarms, nurse and biomedical workflows using representative rooms, noise, lighting, protective equipment, interruptions, staffing, shift handoff, maintenance tools, labeling, consumables, and emergency response;
7. conduct end-to-end nominal and off-nominal increments with safe fluids/simulated patients, independent observers, exact expected events, stop authority, no uncontrolled clinical data, and clinical/biomedical/pharmacy/security participation;
8. progress to tightly controlled operational evaluation only under applicable regulatory, clinical, safety, cybersecurity, privacy, and institutional authority.

Dependencies include protective power/fluid safety before actuation; verified library/order/patient compatibility before dose authority; identity/time/audit before accountable network actions; alarm routing and trained response before unattended operation; backup/rollback and reconciliation before migration; and representative external services before operational evidence claims.

Every step has entry, exact starting state, procedure, observations, pass/hold/abort, ending state, anomaly disposition, regression, and rollback/de-integration. Preserve a known-safe configuration. A failed step holds patient authority and clinical deployment. Successful simulated or test-environment integration does not prove clinical validity, production reliability, cybersecurity, usability across populations, regulatory conformity, or safe operation; those require the applicable independent reviews and controlled evidence.
