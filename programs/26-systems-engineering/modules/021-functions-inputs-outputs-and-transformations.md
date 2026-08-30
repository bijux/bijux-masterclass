---
module_id: SYSENG-021
program: Systems Engineering
level: 1
module_number: 21
title: Functions, Inputs, Outputs, and Transformations
status: complete
last_verified: 2026-08-31
---

# Functions, Inputs, Outputs, and Transformations

## One-Page Review

### Governing question

How can a team describe what a system must do as a coherent network of purposeful transformations—with explicit inputs, outputs, controls, resources, states, timing, quality, and failures—so that stakeholder outcomes can be traced and verified without prematurely freezing the physical solution?

### Essential definitions

- A **function** is a purposeful action or transformation the system performs to contribute to an outcome.
- An **input** is matter, energy, data, information, or a triggering/control condition consumed, modified, referenced, or acted upon by a function.
- An **output** is matter, energy, data, information, state change, service, or effect produced by a function.
- A **transformation** maps admissible input and pre-state conditions to output and post-state behavior under stated controls, resources, and environment.
- A **control** constrains when or how a function executes without necessarily being consumed; a **resource/mechanism** enables execution.
- A **functional interface** is a governed exchange or dependency between functions or across the system boundary, including semantics, direction, quality, timing, modes, and failure behavior.
- A **functional architecture** is the organized set of functions and their flows, dependencies, behavior, and contribution to outcomes; it is not the physical product breakdown.
- A **black-box model** describes externally observable transformations at a boundary; a **white-box model** exposes internal functional structure while preserving that boundary contract.
- A **conservation/balance relation** accounts for relevant matter, energy, data, or resource across a transformation and storage; it applies only where the modeled quantity and boundary justify it.
- **Functional completeness** is a scoped assurance claim that required outcomes, conditions, modes, interfaces, failures, and lifecycle functions have adequate functional coverage and trace—not a count of diagram boxes.

### Central model, mechanism, or theorem

Represent a function as a contract:

\[
f:\langle I,S,C,R,E\rangle\rightarrow\langle O,S',D\rangle,
\]

where \(I\) is typed input, \(S\) pre-state, \(C\) control, \(R\) enabling resources, \(E\) environment, \(O\) output, \(S'\) post-state, and \(D\) diagnostics/evidence. A valid execution claim requires a defined domain and behavior:

\[
Pre_f(I,S,C,R,E)\Rightarrow Post_f(O,S',D)
\]

within stated performance, quality, and uncertainty bounds.

For a connection from function \(f_i\) to \(f_j\), compatibility requires more than matching labels:

\[
Compatible(O_i,I_j) = Type\land Unit\land Semantics\land
Range\land Timing\land Quality\land Mode\land Authority.
\]

If any conjunct is unknown, the interface is unresolved rather than proven compatible.

### Critical invariants

- Every function traces to an authorized outcome, requirement, hazard control, interface obligation, lifecycle need, or explicit derived rationale.
- Function names use stable action-object intent and avoid embedding a chosen component unless that choice is already constrained.
- Inputs and outputs are typed by meaning, unit, range, quality, timing, provenance, and applicability—not merely by names or arrows.
- System boundary, environment, actors, external systems, and ownership are explicit.
- Preconditions, triggers, states, modes, controls, resources, postconditions, and exceptions accompany nominal transformations where relevant.
- Every output is consumed, exported, stored, intentionally discarded, or identified as an unintended effect; every required input has a legitimate source.
- Fan-in, fan-out, feedback, concurrency, delay, storage, initialization, shutdown, degraded operation, and recovery are modeled deliberately.
- Functional and physical architectures remain distinguishable; allocation is a later many-to-many decision, not hidden inside functional naming.
- Conservation equations state boundary, interval, storage, losses, sources, sinks, and uncertainty.
- Verification evidence tests observable contracts at appropriate boundaries; simulations and executable checks remain bounded by their models.

### Common failures

Failures include naming components instead of functions; using vague verbs such as “manage” without transformed object or outcome; drawing untyped arrows; confusing a command with energy or material flow; omitting state and modes; assuming output names imply consumer compatibility; losing storage and delay; modeling only the happy path; treating feedback as a cycle error; forgetting humans, operations, maintenance, security, and disposal; forcing a functional tree when behavior is a graph; allocating before alternatives exist; claiming completeness because every requirement has a box; and applying conservation to information as if copying data consumed the source.

### Compact example

For a cold-chain container, “maintain payload temperature” is refined into sense thermal state, estimate payload condition, determine control action, move heat, distribute conditioned air, record evidence, alert operators, and enter safe degraded operation. Temperature samples carry unit, uncertainty, timestamp, location, and calibration provenance. A controller command is not cooling energy; electrical power, refrigerant/air heat flow, and control information are distinct. A thermal balance names container boundary, heat leakage, payload storage, active heat removal, interval, and uncertainty. The functional model leaves compressor, thermoelectric, or passive-store implementation open until trade studies, while its input/output and performance contracts make alternatives comparable.

### Connections

Retrieve stakeholder outcomes, operational scenarios, functional/performance requirements, decomposition, allocation, traceability, and change control from SYSENG-001–020. Continue with functional decomposition, functional flow, state/mode analysis, interfaces, logical architecture, physical allocation, verification, human systems integration, safety, security, and operations.

## Governing Question

Requirements state obligations, but they do not automatically reveal the coordinated behavior needed to satisfy them. A response-time requirement may require sensing, interpretation, decision, actuation, feedback, logging, and recovery. A system boundary receives and emits matter, energy, information, and effects. Functional analysis makes these transformations and dependencies reviewable before a team commits to hardware, software, personnel, or organizational structure.

The goal is not to create the largest functional diagram. It is to build a coherent explanatory and verification model: what enters, what changes, what leaves, under which conditions, with what performance, and what happens when assumptions fail. The model must remain solution-neutral enough to preserve alternatives while specific enough to expose interfaces, derive requirements, and support evidence.

## Why This Matters

A list of functions can look complete while behavior remains impossible. “Sense,” “decide,” and “act” do not say which state is sensed, who owns the data, whether timestamps align, how decisions handle uncertainty, what energy performs the action, or which feedback confirms the result. Hidden assumptions surface late as incompatible interfaces, unsafe transitions, missing maintenance behavior, or tests that observe the wrong boundary.

NASA’s current Logical Decomposition guidance describes functional analysis as identifying, describing, and relating functions; it calls for each function to be described by inputs, outputs, failure modes, consequences, and interface requirements, arranged so operational use can be traced end to end. ISO/IEC/IEEE 15288:2023 supplies the current system-lifecycle context without prescribing one model or methodology. SEBoK 2.14’s current Functional Architecture article emphasizes input-output transformations and purposeful tasks while noting that “function” has broader uses elsewhere. These sources support a method, not a universal notation.

Functional reasoning also protects design freedom. If “compress refrigerant” appears where the actual obligation is “remove heat from payload,” a solution has been embedded before comparison with phase-change storage or another mechanism. Conversely, endless abstraction such as “provide service” cannot drive interfaces or verification. Good models identify observable transformations and constraints at the decision-relevant level.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. stakeholder needs and ConOps define outcomes, actors, scenarios, environment, modes, and lifecycle context;
2. functional requirements state behavior, while performance requirements bound how well it occurs;
3. decomposition preserves parent intent through contribution and coverage arguments rather than word splitting;
4. allocation links requirements to subsystems but does not by itself define behavior or prove system composition;
5. trace links require semantic rationale and exact configuration;
6. changed requirements can invalidate functions, interfaces, state behavior, and evidence;
7. verification observes specified properties; validation evaluates usefulness in representative operation;
8. models are abstractions whose omissions and assumptions limit conclusions.

As a retrieval test, consider “the camera sends an image to the AI.” Identify at least four hidden ambiguities: image encoding and dimensions, timestamp/provenance, transport and latency, missing/corrupt behavior, calibration, privacy authority, model input normalization, or whether “AI” is a function or a selected component. If an arrow does not answer decision-relevant questions, it is only a sketch.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish stakeholder outcome, capability, function, activity, process, physical component, and implementation mechanism;
2. define a system boundary and identify external actors, systems, environments, flows, and effects;
3. express functions as action-object transformations with typed contracts;
4. classify matter, energy, data, information, control, resource, state, and diagnostic flows;
5. specify preconditions, triggers, postconditions, modes, timing, quality, uncertainty, and failure semantics;
6. connect functions through semantically compatible interfaces and detect orphan inputs or unused outputs;
7. use black-box and white-box views without breaking boundary contracts;
8. apply balance and conservation reasoning with explicit storage, loss, source, sink, interval, and evidence limits;
9. evaluate alternative functional structures before physical allocation;
10. construct bounded completeness and verification arguments for high-consequence functional behavior.

## Core Exposition

**Start with outcomes and scenarios.** Extract what stakeholders need to accomplish, not what the proposed product contains. Walk nominal, alternate, degraded, emergency, maintenance, startup, shutdown, update, and disposal scenarios. Identify actors and external systems. Each step suggests transformations, exchanged flows, triggers, and observable outcomes. Scenario coverage is evidence for discovery, not proof that every future use is known.

**Declare the system of interest and boundary.** Name what is inside, outside, and shared. A human may be inside a sociotechnical system boundary but external to a device boundary. A cloud service can be an external dependency in one model and an internal element in another. Record viewpoint, lifecycle stage, configuration, and boundary rationale so diagrams do not silently disagree.

**Build a context transformation.** Treat the system initially as one black box. List incoming matter, energy, data, information, commands, disturbances, and services; outgoing products, signals, waste, heat, emissions, actions, and stakeholder effects. Identify controls and enabling resources. This prevents internal detail from hiding missing external obligations.

**Name functions by stable intent.** Prefer action-object phrases: `estimate vehicle pose`, `limit delivered torque`, `authenticate maintenance request`, `remove payload heat`. Avoid nouns (`database`), organizations (`operator team`), or mechanism-bound names (`run PostgreSQL query`) unless the architecture has legitimately fixed them. “Manage data” is too vague until the transformation and outcome are explicit.

**Distinguish levels of abstraction.** A capability is an ability to achieve an outcome in context; a function is purposeful behavior contributing to it; a subfunction refines how the parent transformation is accomplished; an activity may describe an operational step by an actor; a process can mean ordered activities or an organizational lifecycle practice. Define local semantics and do not connect unlike levels as peers without rationale.

**Specify input contracts.** For each input, record semantic type, structure, unit, reference frame, range, resolution, accuracy/uncertainty, rate, latency, freshness, ordering, provenance, integrity, confidentiality, authority, optionality, invalid/missing representation, and applicable modes. Not every attribute applies, but omission should be deliberate. “Temperature” without Celsius/Kelvin, location, timestamp, and uncertainty is not a reliable interface.

**Specify output contracts.** Define the same attributes plus consumer obligations, acceptance criteria, persistence, side effects, and allowable degradation. An output can be a changed physical state or effect, not only a message. Identify whether it is consumed by another function, crosses the system boundary, enters storage, or is intentionally discarded. Unaccounted output may be waste, leakage, privacy exposure, or a missing consumer.

**Separate flows by ontology.** Matter and energy are usually conserved across a suitable boundary subject to storage and sources/sinks. Data can be copied; information quality can increase or decrease through interpretation; a control signal constrains behavior; a resource enables action; a trigger initiates it. A message saying “open valve” is not the mechanical energy that moves the valve. Mixing flow types hides necessary enabling functions.

**Describe transformation semantics.** State the relation between admissible inputs/pre-state and outputs/post-state. It may be deterministic, nondeterministic, stochastic, continuous, discrete, or human-mediated. Specify invariants, tolerances, timing, priority, and acceptable uncertainty. If behavior is intentionally unconstrained, say what bounds remain and how verification will observe them.

**Add preconditions, triggers, and postconditions.** A precondition describes what must hold for valid execution; a trigger starts or enables it; a postcondition describes the required result. Do not confuse a required input with a precondition. A payment amount is input; authenticated session may be a precondition; user confirmation a trigger; recorded authorization and balance state are postconditions.

**Model state and memory.** Stateless notation is insufficient when output depends on history. Identify state variables, ownership, initialization, persistence, transition guards, timeouts, reset, recovery, and consistency. Storage is a functionally significant behavior: write, retain, retrieve, expire, reconcile, back up, and destroy may be necessary transformations.

**Model modes and applicability.** Functions can be active, inhibited, modified, or unavailable in startup, nominal, degraded, emergency, maintenance, update, transport, or shutdown modes. State which input/output contracts change and which invariants never relax. Avoid drawing separate mode diagrams whose common flows silently diverge; maintain governed relationships among views.

**Represent sequence, concurrency, and time.** Data-flow adjacency does not necessarily imply temporal order. Model precedence, concurrency, synchronization, deadlines, periods, jitter, latency budgets, queuing, timeout, and race resolution where relevant. End-to-end response is composed from sensing, transport, computation, decision, actuation, and physical response, including waiting and uncertainty.

**Represent fan-in and fan-out.** Multiple inputs may need correlation, fusion, arbitration, or synchronization. One output feeding several consumers creates coupled semantics and capacity. Define partial availability, contradictory sources, priority, backpressure, and consumer-specific transformations. A junction symbol is not a fusion rule.

**Represent feedback deliberately.** Closed-loop behavior uses observed output/state to adjust action. Define controlled variable, reference, sensor, estimator, controller, actuator, plant/environment, sampling, delay, saturation, stability evidence, and safe behavior on lost feedback. Functional feedback is often necessary; it should not be rejected merely because trace justification cycles are suspicious.

**Represent disturbances and unintended effects.** Environment inputs include noise, heat, vibration, adversarial traffic, human interruption, supply variation, and failure propagation. Outputs include waste heat, emissions, electromagnetic interference, misleading alerts, and data exposure. Naming these enables constraints, mitigations, and verification rather than treating them as surprises.

**Model failure semantics.** For each critical function ask: omission, commission, incorrect value, wrong destination, early/late, duplicate, stale, inconsistent, partial, unauthorized, and unavailable resource. Describe detection, containment, degraded output, recovery, evidence, and consequence. Failure analysis and functional architecture should inform each other without claiming one method finds all failures.

**Include enabling and lifecycle functions.** Systems need deployment, configuration, calibration, authentication, monitoring, diagnosis, maintenance, update, backup, recovery, training, support, decommissioning, data retention, and disposal. These may not deliver the headline mission output, but omission can make the system unsafe, insecure, unmaintainable, or noncompliant.

**Include human functions honestly.** Identify perception, decision, physical action, communication, workload, authority, training, error opportunity, accessibility, and environmental constraints. Do not allocate a function to “the operator” merely because automation is difficult. Human performance varies; the interface and organization are part of the functional contract.

**Preserve logical-physical separation.** A functional architecture organizes transformations and flows; a physical architecture organizes implemented elements and connections. Allocation later maps functions to hardware, software, people, facilities, or external services, often many-to-many. Early feasibility constraints may inform functional models, but selected mechanisms should be labeled, not smuggled in.

**Refine black boxes into white boxes.** When opening a parent function, child functions collectively preserve the parent boundary contract. Internal flows should explain transformation, timing, failure, and evidence. Every parent input is consumed or forwarded; every parent output is produced; parent state and invariants are preserved or explicitly derived. Decomposition is developed fully in SYSENG-022.

**Check interface compatibility.** Compare producer output with consumer input for semantic type, schema, unit, reference, range, precision, rate, latency, ordering, quality, security, failure representation, authority, mode, and version. Adaptation may require a new function—convert unit, validate provenance, buffer rate, transform schema—not a renamed arrow.

**Check graph integrity.** Query required inputs without sources, outputs without consumers or boundary destinations, functions without source rationale, disconnected subgraphs, unintended cycles, dead ends, and paths that bypass required control. Graph checks establish declared structure only. Reviewers must still inspect semantics and missing functions.

**Use balance equations carefully.** For an extensive quantity \(q\) within boundary \(\Omega\) over \([t_0,t_1]\):

\[
q(t_1)-q(t_0)=\int_{t_0}^{t_1}(in-out+generation-consumption)\,dt.
\]

Define sign convention, boundary, storage, loss, measurement location, interval, and uncertainty. Energy, mass, charge, and financial value may support balances under appropriate models. Information is not generally conserved: copying produces another representation without removing the source, and semantic value is context-dependent.

**Derive functional performance requirements.** From transformation paths derive latency, throughput, capacity, accuracy, availability, integrity, and resource constraints at observable boundaries. Allocate budgets only after composition relations are understood. Child performance does not automatically establish system performance when queues, interfaces, shared resources, or physical dynamics intervene.

**Compare alternative functional architectures.** Alternative ordering, centralization, distribution, feedback, buffering, autonomy, and human participation can achieve the same outcome. Compare robustness, complexity, observability, coupling, safety, security, resource use, adaptability, verification, and lifecycle burden before physical selection. Keep rejected alternatives and assumptions as decision evidence.

**Trace end to end.** Each function traces upward to outcomes, requirements, hazards, interfaces, or derived rationale and downward to later allocation and evidence. Each critical scenario has an end-to-end path across modes and failure responses. Trace rationale states contribution; link presence alone does not demonstrate coverage or sufficiency.

**Plan verification at functional boundaries.** Define stimuli, pre-state, controls, environment, expected outputs/post-state, timing, uncertainty, oracle, configuration, and negative cases. Observe internal boundaries when they diagnose composition, but retain system-boundary tests. Simulation can explore behavior; it cannot validate unmodeled environment or implementation effects.

**Review completeness through questions.** Can every required outcome be reached? Are all scenario steps, modes, lifecycle stages, interfaces, resources, disturbances, failures, controls, and recovery behaviors represented? Are every input and output accounted for? Do high-consequence paths have independent challenge? A “yes” is a scoped review judgment with evidence and limitations, not mathematical completeness.

**Govern model consistency.** Assign ownership, versioning, naming vocabulary, type definitions, view-generation rules, change control, and review. Prevent diagrams, requirements, interface definitions, and test models from becoming inconsistent copies. Where a model generates views, verify transformation fidelity and preserve human-readable rationale.

The following executable check detects selected declared interface mismatches. It cannot interpret engineering meaning or discover missing flows.

<!-- bijux-verify: {"id":"functional-flow-contract-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"connections_total=5\ncompatible_declared=1\ntype_mismatch=F-002\nunit_mismatch=F-003\nmode_mismatch=F-004\nquality_missing=F-005\nunresolved=F-002,F-003,F-004,F-005\nevidence=declared_contracts_only\n","stderr":""}} -->
```python
connections = [
    {"id": "F-001", "out_type": "temperature", "in_type": "temperature",
     "out_unit": "degC", "in_unit": "degC", "out_modes": {"nominal", "degraded"},
     "in_modes": {"nominal", "degraded"}, "quality": "u<=0.2 degC"},
    {"id": "F-002", "out_type": "position", "in_type": "velocity",
     "out_unit": "m", "in_unit": "m", "out_modes": {"nominal"},
     "in_modes": {"nominal"}, "quality": "timestamped"},
    {"id": "F-003", "out_type": "pressure", "in_type": "pressure",
     "out_unit": "kPa", "in_unit": "Pa", "out_modes": {"nominal"},
     "in_modes": {"nominal"}, "quality": "calibrated"},
    {"id": "F-004", "out_type": "command", "in_type": "command",
     "out_unit": "enum", "in_unit": "enum", "out_modes": {"nominal"},
     "in_modes": {"nominal", "emergency"}, "quality": "authenticated"},
    {"id": "F-005", "out_type": "image", "in_type": "image",
     "out_unit": "pixels", "in_unit": "pixels", "out_modes": {"nominal"},
     "in_modes": {"nominal"}, "quality": ""},
]

def compatible(item):
    return (
        item["out_type"] == item["in_type"]
        and item["out_unit"] == item["in_unit"]
        and item["in_modes"] <= item["out_modes"]
        and bool(item["quality"])
    )

valid = [item for item in connections if compatible(item)]
print(f"connections_total={len(connections)}")
print(f"compatible_declared={len(valid)}")
print("type_mismatch=" + ",".join(item["id"] for item in connections if item["out_type"] != item["in_type"]))
print("unit_mismatch=" + ",".join(item["id"] for item in connections if item["out_unit"] != item["in_unit"]))
print("mode_mismatch=" + ",".join(item["id"] for item in connections if not item["in_modes"] <= item["out_modes"]))
print("quality_missing=" + ",".join(item["id"] for item in connections if not item["quality"]))
print("unresolved=" + ",".join(item["id"] for item in connections if item not in valid))
print("evidence=declared_contracts_only")
```

The result checks equality and set inclusion in five in-memory records. It does not show that `temperature`, `command`, modes, or quality statements have correct semantics; even F-001 needs domain review.

## Definitions and Notation

Let the functional graph be \(G_F=(F,L)\), where \(F\) is the set of versioned function contracts and \(L\) typed flow relations. A contract is:

\[
F_k=\langle id,purpose,I,O,S,C,R,E,P,Q,M,X,A\rangle,
\]

where \(P\) contains pre/postconditions, \(Q\) performance/quality, \(M\) modes, \(X\) exceptions/failure behavior, and \(A\) authority and trace rationale. A flow \(l_{ij}\) includes producer/consumer ports, semantic type, unit/reference, range, timing, quality, security, version, mode, and ownership.

For a path \(p=(f_1,\ldots,f_n)\), end-to-end latency is not always a simple sum. Under a sequential, no-overlap assumption:

\[
T_p=\sum_{k=1}^{n}T_{f_k}+\sum_{l\in p}T_l+T_{queue}.
\]

Concurrency, pipelining, contention, retry, and physical settling require another composition model. State the assumption before using the equation.

Define structural defects relative to declared policy: `source(l)` and `target(l)` exist; each required input port has an admissible source; each output has a consumer, boundary sink, store, or approved discard; every function has source rationale; required scenario paths exist. These predicates support triage but do not establish semantic functional completeness.

## Mechanisms, Invariants, or Proof Structure

Use an iterative functional-analysis loop:

1. **Frame:** identify system of interest, viewpoint, boundary, configurations, external context, outcomes, and representative scenarios.
2. **Transform:** define the black-box input/output transformation and its controls, resources, environment, states, quality, and failures.
3. **Refine:** expose internal functions and flows while preserving the parent boundary contract; explore alternatives before allocation.
4. **Connect:** type functional interfaces and check semantics, units, timing, quality, modes, authority, storage, and feedback.
5. **Challenge:** run balance, path, failure, concurrency, lifecycle, human, security, and adversarial reviews; search for missing behavior beyond the model.
6. **Trace and verify:** connect functions to source intent, derived requirements, later allocation, and observable evidence.
7. **Baseline and change:** record assumptions, rationale, alternatives, versions, and review; reanalyze affected paths after change.

The preservation obligation for white-box refinement is conditional:

\[
Behavior(children,internal\ flows)\upharpoonright Boundary(parent)
\subseteq AllowedBehavior(parent),
\]

and required parent outcomes must remain reachable under specified conditions. The subset expression is an assurance target, not automatically a formal proof. Models may omit timing, continuous physics, human behavior, faults, or environment; evidence must match the consequence and model fidelity.

## Alternatives and Trade-Offs

**Narrative scenarios** communicate context and human intent well but make complex concurrency and flow consistency difficult to inspect. **Functional flow diagrams** expose sequence and dependency but can hide state and data semantics. **State machines** clarify modes and transitions but can become unwieldy for continuous or distributed behavior. **Data-flow and activity models** expose transformation and exchange but require explicit timing/failure extensions. Use coordinated views with one governed semantic model where practical.

**Top-down discovery** preserves source intent and boundary outcomes but may miss technology constraints and operational knowledge. **Bottom-up discovery** surfaces existing capabilities, interfaces, and failure behavior but can legitimize accidental design. Iterate between them while labeling source and rationale.

**Pure implementation independence** preserves choice but can become too abstract to test. **Technology-aware functional modeling** improves feasibility but risks premature selection. Include constraints that are authoritative; express candidate mechanisms as alternatives rather than function identity.

**Centralized transformations** can simplify consistency and authority but create bottlenecks and single points of failure. **Distributed functions** improve locality, autonomy, or resilience but add synchronization, emergent behavior, and interface burden. Compare at the functional level before assigning components.

**Strict synchronous contracts** simplify reasoning but amplify latency and availability coupling. **Asynchronous flows** support decoupling and buffering but add ordering, staleness, duplication, backpressure, and reconciliation functions. The correct choice depends on outcome and failure semantics.

**Formal executable models** can explore state space and catch declared inconsistencies; they demand precise abstractions and may omit physical, social, or security reality. **Review-oriented models** are accessible to stakeholders but depend more on disciplined reasoning. Combine when risk warrants.

## Failure Modes and Misconceptions

- **“A function is a component.”** A function describes purposeful behavior; allocation decides which component or human performs it.
- **“Every arrow is data.”** Systems exchange matter, energy, control, resources, state effects, and information with different semantics.
- **“Matching names mean compatible ports.”** Compatibility requires unit, reference, range, timing, quality, mode, version, and authority.
- **“The diagram shows order.”** Unless notation defines temporal semantics, adjacency can mean dependency rather than sequence.
- **“Feedback is a bad cycle.”** Feedback can be essential control behavior; analyze delay, stability, saturation, and failure.
- **“Mass in equals mass out.”** Storage, reaction, accumulation, leakage, sources, sinks, interval, and measurement uncertainty matter.
- **“Information is conserved.”** It can be copied, compressed, inferred, corrupted, or destroyed; conservation analogies need care.
- **“Nominal path coverage is completeness.”** Degraded, emergency, maintenance, update, startup, shutdown, and recovery behavior matter.
- **“A solver/model verified the architecture.”** It verified encoded properties under model assumptions, not omitted environment or realization.
- **“More boxes mean more rigor.”** Decision-relevant semantics and trace matter more than diagram density.

## Worked Examples

### Example 1

**Cold-chain temperature control.** Inputs include payload thermal state, ambient heat, door state, setpoint, electrical energy, and calibration evidence; outputs include conditioned payload state, waste heat, alarms, and records. Reasoning separates temperature information from heat flow and controller command from actuator energy. A balance includes stored payload energy and leakage. Evidence limits: chamber tests bound named loads and sensors, not every packing pattern. Conclusion: the contract supports comparing active and passive mechanisms without selecting one.

### Example 2

**Water treatment.** `produce potable water` refines into receive source water, characterize quality, remove solids, inactivate pathogens, control chemistry, verify quality, route product, and handle residuals. Matter flows, chemical energy, sensor data, permits, and operator controls are distinct. An unused residual output exposes a disposal function. Online turbidity cannot alone prove pathogen removal; verification and regulatory evidence retain their separate scope.

### Example 3

**Emergency dispatch.** A call becomes a validated incident, prioritized response, assigned resource, operator guidance, and recorded outcome. State and provenance are essential when calls duplicate or locations conflict. Human judgment is a function with workload and authority, not an unspecified box. Simulation bounds queue performance under modeled arrival rates; it cannot validate caller behavior or every regional emergency.

### Example 4

**Warehouse robot feedback.** Desired pose, estimated pose, map, constraints, and energy enable plan motion, command actuators, move, sense, and correct. The estimator output and planner input both say “pose,” but compatibility also needs frame, timestamp, covariance, and map version. Lost localization triggers safe degraded behavior. Track tests support specified floors and speeds, not arbitrary obstacles.

### Example 5

**Medication infusion.** Functions interpret prescription, authenticate context, calculate delivery, constrain rate, actuate flow, measure delivery, detect occlusion, alarm, and record evidence. A software command is neither fluid flow nor proof of delivered dose. Assumptions cover tubing and calibration. High-consequence conclusions require clinical, human-factors, safety, cybersecurity, and regulatory evidence beyond the model.

### Example 6

**Satellite power management.** Solar energy is converted, stored, distributed, limited, measured, and shed across modes. Conservation includes battery state and losses; information flows carry estimates and commands. An eclipse scenario reveals initialization and load-shedding functions. The budget model supports stated orbit, degradation, and uncertainty; it does not prove flight hardware efficiency.

### Example 7

**Privacy-preserving analytics.** Raw events enter validation, minimization, authorization, aggregation, analysis, retention, and deletion functions. Data can be copied, so a mass-flow analogy fails. Outputs include metrics, access logs, residual disclosures, and deletion evidence. A schema checker confirms fields, not whether re-identification risk is acceptable. Privacy authority and threat analysis constrain the functional contract.

### Example 8

**Accessible ticket kiosk.** Functions present choices, receive multimodal input, maintain session state, calculate fare, authorize payment, issue entitlement, assist recovery, and protect privacy. Human abilities and environmental noise are inputs/constraints. Timeout and error behavior affect users differently. Representative testing bounds the included populations and contexts; it cannot claim universal accessibility.

### Example 9

**Fire suppression.** Detect fire indicators, corroborate hazard, isolate energy, warn occupants, release suppressant, verify effect, ventilate, and support responders. Control information, suppressant mass, electrical energy, and hazardous byproducts require separate flows. False activation and failed release are modeled. A functional path does not establish safe chemical selection or coverage geometry.

### Example 10

**Machine-learning perception.** Sensor signals are calibrated, synchronized, transformed, inferred, quality-assessed, fused, and converted into bounded scene information. Model weights and configuration are resources/state; confidence is an output requiring semantics. Distribution shift and adversarial input are environment/failure conditions. Dataset results support named populations and metrics, not all operational scenes or downstream driving safety.

## Cross-Program Connections

- **Platform Engineering:** platform capabilities transform developer inputs into deployable, observable services; contracts must include policy, provenance, failure, and human workflow.
- **API and Service Engineering:** service interfaces operationalize typed functional flows, including semantic versioning, idempotency, latency, errors, authorization, and backpressure.
- **Data Engineering:** pipelines are transformation graphs whose schemas, lineage, quality, state, late data, and replay semantics mirror functional contracts.
- **Object-Oriented Programming:** methods and collaborators realize allocated functions, while class names must not replace system-level behavior and boundary reasoning.
- **Functional Programming:** pure functions make input-output relations explicit, but real systems still require modeled state, time, resources, effects, and failure.
- **Safety and security:** functional failure and misuse analysis connects transformations to hazards, threats, controls, diagnostics, and assurance evidence.

## References

1. ISO, “ISO/IEC/IEEE 15288:2023 — Systems and software engineering — System life cycle processes,” second edition, published 2023-05. https://www.iso.org/standard/81702.html
2. NASA, “4.3 Logical Decomposition,” NASA Systems Engineering Handbook. https://www.nasa.gov/reference/4-3-logical-decomposition/
3. NASA, “4.0 System Design Processes,” NASA Systems Engineering Handbook. https://www.nasa.gov/reference/4-0-system-design-processes/
4. NASA, “System Engineering Handbook: Appendix,” definitions of functional analysis, functional decomposition, functional baseline, and functional flow block diagram. https://www.nasa.gov/reference/system-engineering-handbook-appendix/
5. NASA, “2.0 Fundamentals of Systems Engineering,” NASA Systems Engineering Handbook. https://www.nasa.gov/reference/2-0-fundamentals-of-systems-engineering/
6. NASA, “5.2 Product Integration,” NASA Systems Engineering Handbook. https://www.nasa.gov/reference/5-2-product-integration/
7. SEBoK Editorial Board, “Functional Architecture,” *Guide to the Systems Engineering Body of Knowledge*, version 2.14. https://sebokwiki.org/wiki/Functional_Architecture
8. SEBoK Editorial Board, “Function (glossary),” *Guide to the Systems Engineering Body of Knowledge*, version 2.14. https://sebokwiki.org/wiki/Function_%28glossary%29

## Exercises

### Exercise 1

Create a black-box functional contract for a home smoke-alarm system. Classify inputs, outputs, controls, resources, state, environment, timing, quality, and failure behavior without choosing sensor or network technology.

### Exercise 2

A producer outputs `speed` in km/h every 200 ms with ±2 km/h uncertainty and local monotonic timestamps. A consumer expects m/s every 100 ms with ±0.3 m/s uncertainty and UTC timestamps. Determine compatibility and specify required transformations or evidence.

### Exercise 3

A reservoir receives 12.0 ± 0.3 L/min, releases 9.5 ± 0.2 L/min, and loses an estimated 0.8 ± 0.2 L/min over 30 minutes. Compute nominal storage change and a conservative additive uncertainty bound. State evidence limits.

### Exercise 4

Refine `deliver authenticated emergency message` into a white-box functional network. Demonstrate how the children preserve the parent boundary contract across nominal, delayed, duplicate, and unavailable-network conditions.

### Exercise 5

Review a proposed autonomous clinical robot model containing only `sense patient`, `AI decision`, and `actuate treatment`. Produce an adversarial gap analysis and a bounded verification strategy.

## Answers to the Exercises

### Answer 1

Boundary: the alarm system includes detection, local reasoning, notification, self-check, power management, and user interaction; occupants, dwelling environment, emergency services, and optional external services are outside. Inputs include smoke/combustion indicators, ambient disturbances, user test/silence commands, configuration, time, and power. Controls include authorized sensitivity/mode policy and silence limits. Resources include stored/electrical energy, calibration state, sound/light capability, and communication availability. State includes initialization, nominal, alarm, silenced, fault, low-power, maintenance, and end-of-life.

Outputs include local warning effects, status/fault indications, optional authenticated event information, diagnostic records, waste heat, and end-of-life indication. Contracts specify detection and warning timing, measurable sound/light properties, false/missed behavior, uncertainty, priority, persistence, accessibility, and privacy. Failures include missing/stale/contradictory observations, depleted power, impaired annunciation, unauthorized silence, and communication loss; local warning cannot depend solely on remote service. This contract remains technology-neutral. It supports analysis but does not establish regulatory conformity or household safety without applicable standards, implementation, and representative evidence.

### Answer 2

The connection is not directly compatible. Units differ: \(v_{m/s}=v_{km/h}/3.6\), and the uncertainty converts to approximately ±0.556 m/s, which is worse than the consumer’s ±0.3 m/s requirement. Rates differ: a 5 Hz producer cannot supply new observations to a 10 Hz consumer; interpolation would create estimates and needs a dynamics/error model. Timestamp reference differs: local monotonic time supports interval ordering but not UTC without a synchronized mapping and uncertainty.

Required functions may convert units, map time bases with synchronization provenance, buffer/order samples, and estimate intermediate values with declared age and covariance. Yet conversion cannot improve source accuracy by itself. The source, consumer requirement, or estimation architecture must change, or the consumer must accept degraded quality explicitly. Verification uses known-speed inputs, clock disturbance, dropout, boundary values, and end-to-end timestamps on named configurations. Passing record-shape checks would not establish physical accuracy.

### Answer 3

Using inflow-positive convention, nominal rate of storage change is

\[
12.0-9.5-0.8=1.7\ \text{L/min}.
\]

Across 30 minutes, nominal accumulation is \(1.7\times30=51\) L. With a conservative additive bound and treating duration as exact, rate uncertainty is \(0.3+0.2+0.2=0.7\) L/min, giving ±21 L over the interval. Thus the bounded arithmetic result is 51 ± 21 L, or [30, 72] L under those assumptions.

This is not a statistical confidence interval. It assumes constant rates, independent meaning of the provided bounds is not used, the loss estimate belongs inside the chosen boundary, no other sources/sinks or overflow exist, storage geometry does not alter flows, and measurement biases are already covered. Evidence should check sensor calibration, temporal variation, boundary definition, initial/final direct level measurements, and whether uncertainty combination should be probabilistic or correlated.

### Answer 4

One network is: receive request; authenticate origin and authorization; validate content/schema; assign immutable message ID and priority; determine destinations; protect confidentiality/integrity; enqueue durably; select available route; transmit; receive/validate acknowledgement; reconcile duplicates; escalate on deadline; present to authorized recipient; record outcome; and expire protected data according to policy. Inputs/outputs carry identity, provenance, timestamp, version, priority, confidentiality, integrity status, and expiry. Resources include keys, clock, directory, queue, networks, endpoint capability, and operators.

Nominal behavior yields one accepted, intelligible presentation and auditable acknowledgement within the parent deadline. Delay triggers retry/escalation while preserving age. Duplicate reception uses idempotent identity and records repeated attempts rather than causing repeated harmful action. Network unavailability retains a bounded queue, selects alternate routes, alerts operators, and eventually declares failure instead of fabricating delivery. Child latency budgets, security properties, and failure paths must compose to the parent contract. Tests cover modeled networks, faults, keys, endpoints, and timing; validation with responders examines intelligibility and workflow. Neither successful transmission nor a cryptographic acknowledgement alone proves the emergency outcome.

### Answer 5

The three boxes omit boundary, clinical source authority, patient identity and consent, sensor calibration/provenance, data quality and timing, preprocessing, state/history, contraindications, uncertainty, model/version control, explainability needed for action, human authorization, treatment constraints, dose/force limits, actuator energy, independent interlocks, feedback confirming delivery and effect, alarms, abort, degraded mode, recovery, logging, privacy/security, cleaning, maintenance, update, and disposal. “AI decision” also conflates inference, quality assessment, policy, clinical judgment, and authority.

Adversarial analysis covers wrong patient, stale/shifted/corrupt or malicious input, unavailable sensor, confident wrong inference, conflicting observations, model rollback, network loss, actuator mismatch, occlusion, human interruption, and unsafe feedback delay. Build typed contracts and state/mode models, trace each high-consequence function to clinical and hazard sources, and independently review allocation. Verification combines schema/property checks, calibrated physical tests, fault injection, timing/resource bounds, cybersecurity assessment, interlock tests, integrated treatment-delivery measurement, and configuration audit. Representative clinical simulation and governed study address usability and outcome validity. Conclusions remain bounded to studied patients, contexts, configurations, failure sets, and regulatory authorization; no model or test suite establishes universal clinical safety.
