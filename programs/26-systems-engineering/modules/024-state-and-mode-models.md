---
module_id: SYSENG-024
program: Systems Engineering
level: 1
module_number: 24
title: State and Mode Models
status: complete
last_verified: 2026-08-31
---

# State and Mode Models

## One-Page Review

### Governing question

How can a team model what a system is, knows, permits, and does over time—through explicit states, modes, events, guards, transitions, invariants, concurrent regions, timing, uncertainty, and recovery—so that behavior is analyzable and verifiable without confusing a diagram label with physical reality or a declared “safe state” with demonstrated safety?

### Essential definitions

- **State** is the information about a system at an instant needed to determine relevant future behavior under future inputs; a **state variable** represents one dimension of that information.
- **Physical state** describes the system under control; **knowledge/estimated state** describes what the controller believes, with provenance and uncertainty; **control state** describes the controller’s own execution status.
- A **mode** is a named configuration or regime that enables, disables, or modifies functions, interfaces, limits, authorities, and transition rules for a purpose.
- A **state machine** is a behavioral model of states and transitions caused by events under guards, with entry, exit, transition, and ongoing activities according to a defined semantic profile.
- An **event** is an occurrence presented to the model; a **trigger** identifies the event/condition that may enable a transition.
- A **guard** is a side-effect-free predicate that must hold when evaluated for a transition to be eligible.
- A **transition effect/action** changes state or produces a governed external effect; it is distinct from the event that triggered it.
- An **invariant** is a property required to hold throughout a state/mode or across all modeled executions within a declared scope.
- A **composite state** contains substates; **orthogonal regions** model concurrent state dimensions with explicit synchronization/interaction semantics.
- A **terminal state** ends the modeled lifecycle or scenario; a **transient state** should be exited under stated progress/timing conditions.
- A **safe state** is a context- and hazard-specific condition with accepted residual risk; it may differ by environment, mission phase, occupant state, and remaining resources.
- **Reachability** and **determinism** are properties of the encoded model under its event and scheduling semantics, not proof of realized-system correctness.

### Central model, mechanism, or theorem

Represent a transition as:

\[
\tau=\langle s,e,g,a,s',t,p,q,r\rangle,
\]

where \(s\) is source state, \(e\) event/trigger, \(g\) guard, \(a\) effect, \(s'\) target, \(t\) timing/timeout semantics, \(p\) priority/conflict resolution, \(q\) authority and evidence, and \(r\) failure/rollback behavior.

A transition is eligible only if:

\[
Eligible(\tau,\hat{x},m,c)=In(s)\land Occurred(e)\land
Fresh(\hat{x})\land g(\hat{x},m,c),
\]

where \(\hat{x}\) is estimated state, \(m\) mode, and \(c\) configuration. Eligibility does not prove the effect succeeds physically.

For initial states \(S_0\), modeled runs \(Runs(M,S_0,H)\), and invariant \(I\):

\[
\forall\rho\in Runs(M,S_0,H):\Box I(\rho)
\]

is meaningful only within model assumptions \(H\), event bounds, environmental abstraction, and fairness/scheduling rules.

### Critical invariants

- The system of interest, controller/system-under-control boundary, viewpoint, state ownership, configuration, and time base are explicit.
- Physical, estimated, commanded, desired, and control-execution states remain distinct and traceably related.
- Every state/mode has purpose, entry conditions, allowed functions/interfaces, invariants, ongoing behavior, exits, and observability appropriate to scope.
- Every transition has stable identity, source, trigger, guard, effect, target, timing, priority, authority/rationale, and failure disposition as applicable.
- Missing, stale, uncertain, contradictory, delayed, duplicate, and out-of-order observations have modeled behavior.
- Guard overlap, gaps, event ordering, simultaneous events, and transition conflicts are resolved deliberately rather than by drawing order.
- Initialization establishes known state or explicit uncertainty before hazardous functions are enabled.
- Transient states and retries have progress, timeout, resource bounds, and escape; terminal states have deliberate outcomes.
- Composite and orthogonal state semantics preserve parent invariants and control cross-region interaction/state explosion.
- Mode changes update functions, interfaces, limits, resource budgets, authority, alerts, verification applicability, and operational procedures consistently.
- Safe/degraded/emergency states are justified against named hazards and context; transition paths into and out of them are analyzed.
- Simulation, model checking, code generation, and tests remain bounded by semantics, abstraction, configuration, and observed cases.

### Common failures

Failures include using state and mode as synonyms; naming activities such as “processing” without stable state meaning; treating a command as physical state; assuming a sensor value equals truth; omitting uncertainty and freshness; placing side effects in guards; leaving unhandled events; relying on implicit transition priority; making every combination a flat mode; ignoring concurrent-region races; entering operation before initialization; defining a safe state without hazard context; using reset as universal recovery; forgetting maintenance/update/disposal modes; generating code from an unverified model; and claiming safety because a model checker finds no counterexample within an incomplete state space.

### Compact example

An autonomous shuttle door has physical position/velocity/obstruction state, estimated state from sensors, commanded state, controller state, and vehicle mode. In `boarding`, a close request is eligible only when departure is authorized, observations are fresh, and no obstruction is conservatively indicated. Closing has a force/speed invariant and timeout. Obstruction causes stop/reverse; sensor disagreement enters `state-uncertain` and inhibits vehicle motion. `closed-confirmed` requires independent interlock evidence, not merely a close command. “Safe” differs for a moving vehicle, fire evacuation, and maintenance, so hazard authority defines context-specific degraded behavior.

### Connections

State/mode models complement function contracts, decomposition, and FFBD paths from SYSENG-021–023. They inform behavioral scenarios, logical components, allocation, control/data flows, interfaces, timing, resources, hazards/threats, verification, operations, configuration management, and autonomous-system assurance.

## Governing Question

The same input can require different behavior depending on history. A door-close request means one thing while stationary and boarding, another during emergency egress, and nothing useful when state knowledge is stale. Functional flow captures progression; state and mode models capture the memory, regimes, and conditions that make progression valid.

The engineering difficulty is that real state is not identical to its representation. A controller observes noisy, delayed evidence and sends commands whose physical effects may fail. Models must therefore distinguish the system under control from the controller and its knowledge. The governing question asks how to preserve that distinction while creating behavior precise enough to review, analyze, implement, and verify.

## Why This Matters

State defects produce dangerous emergent behavior: a restart reuses stale authority; two concurrent regions disagree about readiness; a timeout fires after an operation already completed; maintenance mode leaves a safety interlock bypassed; a vehicle believes a door is closed because it issued a close command. These failures exist between events, state knowledge, effects, and physical truth.

The current NASA handbook points projects to state analysis alongside functional and timing analysis. JPL’s current State Analysis overview emphasizes modeling the physical system, sensors/actuators, state knowledge, control objectives, and the separation between control system and system under control. ISO/IEC/IEEE 15288:2023 provides the lifecycle setting without prescribing one modeling method. OMG’s current SysML specification pages identify state machines as a systems-modeling capability; the ISO/IEC 19514:2017 SysML 1.x specification describes discrete behavior through states, transitions, entry/exit/do activities, events, guards, and concurrent composite states. SysML v2 is current as a separate OMG specification family, so a project must record the exact language/profile rather than say only “SysML.”

A disciplined state model supports requirements discovery, interface definition, fault response, timing analysis, test generation, code design, and operator procedures. It cannot replace physical models, clinical/safety reasoning, or empirical evidence. Its greatest value is making assumptions and missing behavior visible before implementation supplies accidental answers.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. functions transform typed inputs and state into outputs and new state;
2. functional decomposition preserves parent boundary behavior through child networks;
3. FFBDs express execution sequence/logic but do not alone encode complete state semantics;
4. modes arise from operational scenarios, constraints, hazards, maintenance, and lifecycle needs;
5. control flows differ from observations, commands, matter, energy, and physical effects;
6. traceability links state behavior to needs, requirements, hazards, interfaces, decisions, and evidence;
7. requirement changes can invalidate guards, transitions, modes, tests, and operational procedures;
8. formal and executable analysis establishes only properties of the encoded abstraction.

As a retrieval test, examine `OFF → ON` after event `power button`. Ask whether external power is available, startup self-test completes, output is safe during initialization, the button bounces, shutdown is in progress, a fault is latched, or maintenance authority is active. Two circles and an arrow do not define operational behavior.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish physical, estimated, commanded, desired, controller, lifecycle, and operational state;
2. define modes by enabled behavior and constraints rather than labels alone;
3. specify states, events, guards, effects, transitions, timeouts, priorities, and authority;
4. model initialization, stable/transient/terminal states, composite states, history, and orthogonal regions;
5. represent uncertainty, observation freshness, sensor disagreement, and state-estimation failure;
6. analyze reachability, deadlock/livelock, nondeterminism, guard gaps/overlap, and forbidden transitions;
7. integrate state machines with functions, FFBDs, interfaces, timing, resources, hazards, threats, and humans;
8. define context-specific degraded and safe-state behavior with recovery evidence;
9. use simulation/model checking/test generation without overclaiming model fidelity;
10. construct a bounded assurance argument for a high-consequence stateful system.

## Core Exposition

**Define the model frame.** Name system of interest, system-under-control/controller boundary, viewpoint, lifecycle phase, configuration, environment, state-machine language/profile/version, event semantics, scheduling/fairness assumptions, and intended decisions. A device, subsystem, mission, operator workflow, and organizational approval process require different state abstractions.

**Inventory state variables.** Identify quantities whose current value/history affects future behavior: physical configuration, energy, thermal condition, position, ownership, authorization, data version, task progress, faults, and resource availability. Record domain, unit/reference, dynamics, valid/unknown representation, owner, persistence, and reset behavior. Avoid duplicating the same state without consistency rules.

**Separate truth from knowledge.** Let \(x\) denote physical state and \(\hat{x}\) the estimated state. Measurements \(y\) relate through a model such as \(y=h(x)+v\), with noise/error \(v\). Commands target change but do not establish \(x\). Record estimator/model version, timestamp, uncertainty, provenance, and validity; state uncertainty is itself decision-relevant.

**Assess observability and diagnosability.** Ask whether the available observation history can distinguish state alternatives that require different action. Two physical states may produce the same sensor reading until a deliberate probe, additional sensor, elapsed time, or changed operating condition separates them. Define which states are directly measured, inferred, or fundamentally ambiguous; what excitation is safe; how quickly ambiguity must resolve; and what degraded behavior applies meanwhile. Diagnostics that merely echo controller variables do not independently observe the plant. Review common sensors, shared clocks, calibration, model bias, and common-cause loss before claiming independent confirmation. Observability in a mathematical model is conditional on that model and operating point; practical diagnosability also depends on noise, sampling, computation, and access. If hazardous state cannot be known reliably within the available time, redesign the sensing, control objective, or physical constraint rather than encoding optimistic guards.

**Define modes by consequences.** For each mode, list active/inhibited/modified functions, interfaces, limits, resources, authorities, alerts, evidence, and allowed transitions. `normal`, `degraded`, and `maintenance` are not sufficient definitions. Decide whether modes are exclusive, hierarchical, or orthogonal state dimensions.

**Choose state granularity.** States should distinguish behaviorally different futures. If two named states respond identically to all relevant events and have identical invariants, the distinction may be unnecessary. If one state hides different authority, hazard, timing, or recovery behavior, refine it. Granularity is viewpoint- and decision-dependent.

**Define entry, ongoing, and exit behavior.** Entry actions establish local conditions; ongoing/do behavior persists while in state; exit actions prepare transition. Clarify interruption semantics, completion, errors, and external effects. Do not place irreversible effects in entry/exit actions without idempotency and recovery reasoning.

**Specify events and queues.** Events can be signals, calls, state changes, time events, operator actions, or physical observations. Define source, identity, payload, timestamp, ordering, duplication, loss, priority, authentication, and persistence. State-machine tools differ on queueing and run-to-completion; document the exact semantics.

**Write guards as predicates.** Guards refer to valid/fresh state knowledge, mode, configuration, and authority. They should not modify state. Specify units, thresholds, boundary equality, uncertainty treatment, and missing values. Ensure choice guards are mutually exclusive when required or define priority/allowed nondeterminism.

**Define transition effects.** State which commands, outputs, state updates, logs, and interface events occur. Separate requested effect from confirmed physical outcome. If a command can fail, model acknowledgement, observation, timeout, rollback/compensation, and uncertain result rather than jumping directly to success state.

**Resolve simultaneous eligibility.** Multiple events/transitions can be eligible at once. Define priority, conflict, preemption, deferral, nondeterminism, or concurrency explicitly. Diagram placement should not determine safety. Where nondeterminism is intentional, every allowed result must satisfy invariants and verification obligations.

**Model initialization.** Establish initial pseudostate, retained state validity, configuration, clock, identity, calibration, resource status, and fault memory. After power loss or update, persisted state may be stale or incompatible. Keep hazardous outputs inhibited until state is known enough or enter a conservative degraded mode.

**Model transient and terminal states.** Transient states need completion event, progress measure, deadline, resource bound, and escape/failure transition. Terminal states represent deliberate end conditions such as disposed, aborted, or completed—not “diagram ends here.” Continuous operational states still need controlled shutdown and failure behavior.

**Use composite states.** Group shared behavior and transitions without duplicating them. Define initial substate, entry/exit across hierarchy, event handling, and history semantics. Shallow/deep history can restore unsafe or obsolete substate after maintenance or configuration change; use it only with compatibility checks.

**Use orthogonal regions cautiously.** Concurrent regions reduce flat-state explosion but introduce synchronization and interaction. Define shared variables/resources, event broadcast, completion, invariants across region combinations, and transition ordering. “Communications ready” and “mechanism ready” regions may jointly gate operation.

**Control state explosion.** Separate truly independent dimensions; abstract irrelevant values; use hierarchy, parameterization, and generated views; define constraints on legal combinations. Do not create a named mode for every product of state variables. Preserve the authoritative semantic model behind readable views.

**Model time explicitly.** Distinguish event time, processing time, wall/monotonic time, deadlines, dwell, periodic activity, timeout, and freshness. Define clock source, synchronization, drift, reset, and uncertainty. A timeout event racing with completion needs deterministic or safely nondeterministic resolution.

**Model failure and recovery.** Include detected, suspected, latent, intermittent, common-cause, and state-knowledge failures as relevant. Specify fault latching, containment, degraded functions, operator authority, recovery preconditions, verification, retry limits, and escalation. Reset clears controller state only if physical and retained state are reconciled.

**Define safe states contextually.** Start from hazard/threat analysis: which controlled variables, energy, motion, containment, communication, human egress, and time-to-harm matter? One hazard may prefer power off while another requires active cooling. A safe state can be unreachable after resource loss; define safer trajectories and residual-risk decisions rather than a magic node.

**Model humans and external authorities.** Operator awareness, workload, training, confirmation, override, handoff, and delayed response influence transitions. Authenticate authority and model disagreement or absence. A human should not be assigned “resolve unknown state” without observations, time, controls, and feasible action.

**Cross-check functions and FFBDs.** Each state/mode enables or inhibits functions; functions consume/produce state; FFBD transitions align with events/guards. Identify flows that bypass state invariants or state transitions with no realizing function. No single view is authoritative for every concern, but their semantics must be consistent.

**Cross-check interfaces.** State/mode changes can alter schema, allowed messages, frequency, quality, power, physical connections, or ownership. External systems need explicit mode/state negotiation and compatibility behavior. Never infer that peers change modes simultaneously; model handshake, partial transition, timeout, and rollback.

**Cross-check resources and timing.** A logically eligible transition can be infeasible without energy, bandwidth, operator attention, or actuator capacity. State invariants include resource bounds. Analyze worst-case dwell and transition latency, queues, scheduling, and physical settling under named loads/configurations.

**Analyze reachability.** Identify required unreachable states, forbidden reachable states, dead ends, trap states, and terminal states. Guard-aware reachability is stronger than graph traversal, but depends on encoded domains and events. Examine boundary values and configuration variants.

**Analyze determinism and completeness.** For each relevant state/event/input partition, determine eligible transitions. Flag guard gaps, overlap, contradictory priorities, and ignored events. Complete input partitioning can be impractical for continuous variables; define abstraction and safe default/unknown behavior.

**Analyze invariants and liveness.** Safety properties state what never happens; liveness states that required progress eventually occurs under assumptions. Deadlock violates progress; livelock performs transitions without outcome. Fairness, environment, resource, and timing assumptions must accompany liveness claims.

**Use simulation and model checking proportionally.** Simulate representative and adversarial traces; enumerate bounded state spaces; check invariants, reachability, deadlock, transition coverage, and temporal properties. Record model/tool/property versions and bounds. Counterexample absence means none was found in that model—not that implementation or environment is universally safe.

**Derive tests.** Cover every state and transition as risk warrants, plus guard boundaries, invalid events, event sequences, concurrent interleavings, timeouts, startup/restart, retained state, configuration change, sensor disagreement, actuator failure, degraded recovery, and forbidden transitions. Link expected physical observations, not only controller variables.

**Govern code generation and implementation.** Generated code inherits model and generator defects. Qualify/verify tooling as required, inspect semantic mapping, protect manual integration points, and test realized timing/concurrency. Configuration-control model, profile, generator, runtime, and deployment together.

**Control model change.** Trace changed state variables, guards, transitions, modes, functions, interfaces, hazards, tests, operator procedures, and deployed variants. Re-run analysis on the actual target baseline. Preserve decision rationale and historical execution semantics.

The following checker detects selected missing declarations in five transition records. It does not execute a state machine.

<!-- bijux-verify: {"id":"state-transition-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"transitions_total=5\nwell_formed_declared=1\nmissing_trigger=T-002\nmissing_guard=T-003\nmissing_effect=T-004\nmissing_authority=T-005\nunresolved=T-002,T-003,T-004,T-005\nevidence=declared_fields_only\n","stderr":""}} -->
```python
transitions = [
    {"id": "T-001", "source": "idle", "trigger": "start", "guard": "ready and fresh",
     "effect": "command motion", "target": "moving", "authority": "operations"},
    {"id": "T-002", "source": "moving", "trigger": "", "guard": "obstruction",
     "effect": "command stop", "target": "stopping", "authority": "safety"},
    {"id": "T-003", "source": "stopping", "trigger": "motion-stopped", "guard": "",
     "effect": "record stop", "target": "idle", "authority": "operations"},
    {"id": "T-004", "source": "moving", "trigger": "timeout", "guard": "deadline exceeded",
     "effect": "", "target": "fault", "authority": "safety"},
    {"id": "T-005", "source": "fault", "trigger": "reset", "guard": "physical state reconciled",
     "effect": "clear controller latch", "target": "idle", "authority": ""},
]
required = ("source", "trigger", "guard", "effect", "target", "authority")
valid = [item for item in transitions if all(item[field] for field in required)]
print(f"transitions_total={len(transitions)}")
print(f"well_formed_declared={len(valid)}")
for field in ("trigger", "guard", "effect", "authority"):
    print(f"missing_{field}=" + ",".join(item["id"] for item in transitions if not item[field]))
print("unresolved=" + ",".join(item["id"] for item in transitions if item not in valid))
print("evidence=declared_fields_only")
```

Even T-001 may be semantically unsafe. The checker cannot assess freshness, physical readiness, conflicting transitions, timing, state reachability, or authority competence.

## Definitions and Notation

Let a labeled transition system be \(M=(S,E,\rightarrow,S_0)\), with state space \(S\), events \(E\), transition relation \(\rightarrow\subseteq S\times E\times S\), and initial set \(S_0\). Guards/effects enrich the relation. Determinism relative to abstraction requires at most one resolved transition for a given modeled state and event/input valuation, unless intentional nondeterminism is declared.

Let physical state \(x_t\), observation \(y_t\), estimate \(\hat{x}_t\), desired state \(x_t^*\), and command \(u_t\) remain distinct:

\[
x_{t+1}=f(x_t,u_t,w_t),\quad y_t=h(x_t,v_t),\quad
\hat{x}_t=Est(y_{0:t},u_{0:t-1},Model).
\]

Disturbance \(w_t\) and measurement error \(v_t\) limit knowledge. These equations are generic structure, not an asserted estimator for every system.

For a transition-coverage metric, always name eligible population and configuration:

\[
Coverage=\frac{|T_{executed\ with\ accepted\ evidence}|}{|T_{required\ in\ scope}|}.
\]

One hundred percent does not prove missing transitions absent or state invariants valid.

## Mechanisms, Invariants, or Proof Structure

Use a state-model assurance loop:

1. **Frame:** identify system/controller boundary, viewpoint, state variables, modes, semantics, configuration, environment, and decisions.
2. **Define:** specify states/modes, invariants, observations/uncertainty, events, guards, effects, targets, time, priority, authority, and failure behavior.
3. **Compose:** add hierarchy and orthogonal regions while controlling shared state, synchronization, initialization, and legal combinations.
4. **Integrate:** reconcile functions, FFBD paths, interfaces, resources, timing, hazards/threats, humans, and physical dynamics.
5. **Analyze:** check reachability, forbidden states, gaps/overlap, nondeterminism, deadlock/livelock, invariants, liveness, timeouts, and change impact.
6. **Verify and validate:** exercise model and realization, observe physical effects, challenge abstraction, and assess representative operational use.
7. **Baseline and monitor:** control semantic profile/model/runtime configuration, deployment, anomalies, and reopening after new evidence.

The resulting argument is conditional. Formal analysis can establish properties over encoded runs; empirical evidence can observe selected real configurations. Neither proves the abstraction complete, sensors truthful in all conditions, actuators effective, humans predictable, or every hazard controlled.

## Alternatives and Trade-Offs

**Flat finite-state machines** are simple but explode with interacting dimensions. **Hierarchical state machines** factor shared behavior but complicate entry/exit/history semantics. **Orthogonal regions** represent concurrency but multiply combinations and races. Choose the smallest semantics that preserve decision-relevant behavior.

**Mode tables** clearly compare enabled functions/limits across modes but underrepresent transitions. **State diagrams** show transitions but can hide detailed invariants. **State-transition tables** support completeness review. **Temporal logic/formal models** support stronger analysis but require abstraction expertise. Coordinate views from governed semantics.

**Event-driven models** suit discrete control. **Continuous/hybrid models** are needed where physical dynamics and thresholds matter. Discretizing temperature or velocity into labels can miss boundary/chattering effects; hybrid analysis costs more but may be necessary.

**Centralized mode control** simplifies authority and consistency but creates a dependency. **Distributed state/mode coordination** improves autonomy/resilience but adds consensus, stale knowledge, partition, and recovery behavior. Explicitly model partial agreement.

**Fail-safe shutdown** may reduce some hazards while increasing others. **Fail-operational degradation** preserves service but needs resources, independence, and bounded authority. Select through hazard/context evidence rather than naming convention.

## Failure Modes and Misconceptions

- **“State is the latest sensor value.”** State can be hidden; observations have noise, delay, provenance, and uncertainty.
- **“Commanded means achieved.”** Physical outcome requires observation/evidence.
- **“Mode is just a label.”** It changes enabled functions, interfaces, limits, authority, and evidence applicability.
- **“Unspecified events are ignored safely.”** Ignoring may violate an invariant; define behavior.
- **“Transitions are evaluated top to bottom.”** Only if the semantic profile explicitly says so.
- **“Reset returns to a known state.”** Controller reset may leave physical and retained state unreconciled.
- **“Safe state is universal.”** Safety is hazard-, context-, time-, and resource-dependent.
- **“Every state/transition covered means correct.”** Missing states, bad guards, wrong oracles, and physical failures remain possible.
- **“No model-checker counterexample proves safety.”** It proves only the encoded property over explored/model-defined behavior.
- **“Generated code needs no design review.”** Generator, runtime, integration, scheduling, hardware, and model defects remain.

## Worked Examples

### Example 1

**Cold-chain controller.** Physical payload temperature, sensor estimate, controller mode, door state, and energy reserve are separate. Startup enters `state-uncertain` until calibration/freshness criteria hold. Degraded mode changes alert and cooling limits. Chamber results support named loads and sensors; they cannot prove every packing pattern or field disturbance.

### Example 2

**Water-treatment batch.** States include receiving, treating, sampling, awaiting-result, accepted, isolated, reprocessing, and disposed. A laboratory result must match batch identity/version; timeout does not imply failure or acceptance. Reprocess loops are bounded. Regulatory evidence, not a state label, authorizes release.

### Example 3

**Aircraft landing gear.** Commanded down, actuator running, estimated position, physical lock, and cockpit indication differ. Sensor disagreement enters uncertain/degraded behavior and inhibits false “down-and-locked.” Safe response depends on flight phase and remaining time. Certification requires physical, timing, fault, human, and independence evidence.

### Example 4

**Account session.** Unauthenticated, challenge-pending, authenticated, step-up-required, locked, recovery, and revoked modes govern operations. Duplicate/out-of-order authentication events and clock expiry are modeled. Formal transition checks cover encoded sessions, not all credential attacks or identity fraud.

### Example 5

**Warehouse robot.** Physical pose, estimated pose/covariance, task state, traffic mode, and safety-stop state are orthogonal but interacting. Lost localization inhibits motion; recovery reconciles map/version and physical location. Track tests support specified floors, loads, and obstacles, not all warehouses.

### Example 6

**Satellite operations.** Mission phase, attitude-control mode, power mode, communication state, and fault-protection state cannot be flattened practically. Orthogonal regions use cross-invariants such as prohibiting high-power payload while energy-critical. Simulation depends on modeled faults/orbit and does not establish flight assurance alone.

### Example 7

**Data pipeline.** Dataset state distinguishes received, validated, quarantined, transformed, published, superseded, and deleted; job execution state is separate. A successful job command does not prove data publication or quality. Replay and schema-version changes require idempotency and lineage evidence.

### Example 8

**Infusion system.** Prescription authorization, programmed dose, physical fluid delivery, estimated delivered volume, alarm state, and clinician workflow differ. Occlusion and sensor disagreement enter bounded degraded behavior. High-consequence conclusions require physical metrology, clinical, safety, cybersecurity, usability, and regulatory evidence.

### Example 9

**Regional service recovery.** Regions can be healthy, suspected, isolated, restoring, reconciling, or retired; global mode can be normal, partitioned, or recovery. Partial knowledge and split-brain authority are explicit. Chaos tests cover injected faults and configurations, not every correlated infrastructure failure.

### Example 10

**Autonomous shuttle door.** Boarding, closing, obstruction-reverse, closed-confirmed, state-uncertain, emergency-egress, and maintenance behavior is governed by vehicle mode. Motion enablement needs confirmed physical interlock, not command history. Fixture and representative user evidence remain bounded; independent safety/accessibility authority is required.

## Cross-Program Connections

- **Platform Engineering:** deployment, incident, reconciliation, and resource lifecycle controllers are stateful systems whose desired, observed, and actual states differ.
- **API and Service Engineering:** protocol state, idempotency, retries, leases, sagas, and version negotiation depend on explicit event and transition semantics.
- **Data Engineering:** dataset/job state, watermarks, late events, backfills, lineage, and retention require separation of execution and data truth.
- **Object-Oriented Programming:** State patterns can implement local state behavior, while system modes and physical truth cross object boundaries.
- **Functional Programming:** algebraic data types and reducers make state transitions explicit; effects, concurrency, time, and physics still require system models.
- **Safety/security:** hazards and threats constrain reachable states, transition authority, fail-safe/fail-operational behavior, and assurance evidence.

## References

1. ISO, “ISO/IEC/IEEE 15288:2023 — Systems and software engineering — System life cycle processes,” second edition, published 2023-05. https://www.iso.org/standard/81702.html
2. NASA, “Appendix F: Functional, Timing, and State Analysis,” current handbook routing page. https://www.nasa.gov/reference/appendix-f-functional-timing-and-state-analysis/
3. NASA JPL, “System Engineering — State Analysis.” https://www.jpl.nasa.gov/work-with-us/technology-system/mds/system-engineering/
4. NASA JPL, “Mission Data System.” https://www.jpl.nasa.gov/work-with-us/technology-system/mds/
5. Ingham, M., Rasmussen, R., and Bennett, M., “Engineering Complex Embedded Systems with State Analysis and the Mission Data System,” NASA NTRS 20070019287. https://ntrs.nasa.gov/citations/20070019287
6. Object Management Group, “OMG SysML Specifications,” including the current SysML v2 specification family and archived SysML v1 releases. https://www.omg.org/sysml/specifications.htm
7. ISO/IEC, *ISO/IEC 19514:2017 — Information technology — Object management group systems modeling language*, State Machines overview available from OMG. https://www.omg.org/spec/SysML/ISO/19514/PDF
8. Object Management Group, “SysML v1 Specification” overview. https://www.omg.org/sysml/sysmlv1/
9. NASA JPL, “Mission Data System State Database.” https://mds.jpl.nasa.gov/public/database/

## Exercises

### Exercise 1

Design a state/mode model for a battery-backed medical refrigerator. Separate physical, estimated, desired, command, controller, and operational states; cover startup, normal, door-open, power loss, sensor disagreement, degraded operation, alarm, recovery, maintenance, and shutdown.

### Exercise 2

In state `heating`, two transitions share event `sample`: guard A is \(T\ge80\), guard B is \(T\le85\). Diagnose the model and redesign it for exclusive, uncertainty-aware behavior with sensor failure.

### Exercise 3

A timeout is 500 ms. Completion may physically occur at 480 ms, its observation arrives at 520 ms, and the timeout event is processed at 505 ms. Analyze possible transitions and specify safe semantics without assuming perfect clocks or instantaneous observation.

### Exercise 4

Create orthogonal regions for a service with deployment state, traffic state, and data-migration state. Define cross-region invariants and analyze a rollback during partial migration.

### Exercise 5

Construct an assurance plan for an autonomous clinical robot’s `safe` and `degraded` modes. Explain why reachability, transition coverage, simulation, and generated code are insufficient by themselves.

## Answers to the Exercises

### Answer 1

Physical variables include chamber/payload temperature distribution, door position, grid/battery energy, cooling effect, and ambient heat. Estimated variables include timestamped temperatures with uncertainty/provenance, energy estimate, and door confidence. Desired state is permitted temperature range and reserve policy. Commands request cooling, isolation, alarm, or shutdown; they do not establish physical outcome. Controller states include initializing, controlling, diagnosing, and fault-latched. Operational modes include normal, grid-loss, energy-critical, sensor-disagreement, maintenance, recovery, and retired.

Startup inhibits acceptance until identity/configuration, sensors, clock, stored history, energy, and cooling response are checked. Door-open changes thermal model and timer. Grid loss transitions to battery policy; energy-critical prioritizes preservation/alarm. Sensor disagreement enters conservative estimate and service action. Recovery requires fresh consistent evidence and physical response, not reset alone. Maintenance has explicit authority and prevents unintentional normal operation. Evidence includes calibration, thermal/battery tests, fault injection, timing, alarms, operator procedures, and configuration audit, bounded to tested loads/environments and applicable medical/regulatory authority.

### Answer 2

The guards overlap for \(80\le T\le85\), creating two eligible transitions unless priority or nondeterminism is explicitly safe. They also assume \(T\) is true, current, scalar state. Define measurement \(y\), estimate \(\hat{T}\), uncertainty \(u\), timestamp/freshness, sensor agreement, and thresholds from authorized requirements.

One exclusive design: `sensor-invalid/stale/disagree` → state-uncertain and inhibit heat; `\hat{T}-u\ge85` → overtemperature response; `\hat{T}+u<80` → continue heating; otherwise → uncertainty band that stops or modulates heat and obtains additional evidence according to hazard policy. Equality semantics are explicit. If hysteresis is needed, encode different enter/exit thresholds and current state to prevent chatter. Verification covers boundaries, uncertainty, delay, stuck/noisy sensors, clock issues, and physical temperature—not merely transition-variable values.

### Answer 3

At 505 ms the controller may know only that no completion observation has arrived, although the physical action completed at 480 ms. Transitioning directly to “failed” and commanding a retry could duplicate a harmful effect. Define timeout as `completion not confirmed by deadline`, not proof of physical failure. Enter an `outcome-uncertain` state, inhibit non-idempotent retry, query independent state/acknowledgement, and apply a bounded reconciliation deadline. Commands and completion observations carry operation ID and monotonic timestamps with clock uncertainty.

If physical confirmation at 520 ms is valid for the same operation/configuration, reconcile to completed-late and disposition the timing violation. If evidence remains unavailable, move to hazard-specific degraded/safe behavior and human/authority escalation. Specify event ordering when timeout and completion are queued together; both allowed interleavings must preserve invariants if nondeterministic. Tests inject delayed/lost/duplicate events and clock drift, but physical instrumentation is needed to establish actual completion.

### Answer 4

Deployment region: stable-old, deploying-new, stable-new, rollback. Traffic region: old-only, shadow, canary, mixed, new-only, drained. Migration region: not-started, copying, dual-write, cutover, reconciling, complete, reversing. Cross-invariants include: new traffic requires schema compatibility; old-only must remain readable during copying; rollback is permitted only while reverse compatibility or a verified reverse transformation exists; a destructive cutover cannot coexist with unverified old-version writes; and deployment “stable” requires migration/traffic states allowed by the release policy.

During partial migration, rollback cannot merely redeploy old code. Freeze or route writes, identify data-version boundaries, reconcile dual writes, verify reverse transformation, restore old-compatible traffic, then roll back deployment. If reversal is unsafe, remain in bounded mixed/degraded mode and escalate rather than fabricate rollback success. Model checking can explore encoded region combinations; database tests, lineage, load/failure evidence, and operational authority are still required.

### Answer 5

Define hazards and contexts first: motion/force, dose/treatment, collision, infection, privacy, loss of support, human egress, and time-to-harm. `Safe` and `degraded` modes specify physical bounds, active/inhibited functions, independent interlocks, required observations/uncertainty, energy/resource needs, clinician authority, alarms, time limits, exit/recovery, and residual risk. Different clinical contexts may require stop, controlled continuation, or handoff; one universal safe node is invalid.

Reachability shows encoded paths exist, not that sensors/actuators make them physically achievable. Transition coverage observes listed transitions, not missing states or correct guards. Simulation depends on patient/environment/fault models. Generated code preserves model and generator errors and may behave differently under scheduling/hardware. Assurance combines formal invariant/deadlock analysis, physical metrology, fault injection, timing/concurrency tests, cybersecurity/privacy assessment, independent safety analysis, clinical/human-factors validation with representative populations/workflows, configuration control, monitored deployment, and competent regulatory/clinical acceptance. Conclusions remain bounded to authorized configurations, contexts, hazards, and evidence.
