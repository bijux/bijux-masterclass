---
module_id: SYSENG-053
program: Systems Engineering
level: 2
module_number: 53
title: Behavior Models
status: complete
last_verified: 2026-08-31
---

# Behavior Models

## One-Page Review

### Governing question

How can engineers model what a system does across scenarios, functions, interactions, modes, states, concurrency, timing, faults and recovery with enough semantic precision to expose missing and unsafe behavior—without mistaking a well-formed diagram or verified abstraction for validated real-world behavior?

### Essential definitions

- A **behavior** is an occurrence or ordered/conditional set of occurrences that transforms state, exchanges items/energy/information, performs work or produces observable outcomes over time.
- A **behavior model** is a governed semantic representation of actions, events, inputs/outputs, control, state, time, resources, performers and constraints for declared system scope and intended use.
- A **scenario/use case** describes an actor-goal interaction through nominal, alternate and exception paths in a defined context; it supplies behavior examples, not exhaustive semantics by itself.
- An **activity/functional-flow model** represents actions/functions, control and object/resource flows, sequencing, branching, joining, concurrency and termination.
- An **interaction/sequence model** represents time-ordered exchanges among participants for a scenario; it does not alone define all participant states or every possible ordering.
- A **state** is an abstraction of relevant history for which future response is governed consistently; a **mode** is an operational configuration or policy regime and may be modeled separately from state.
- An **event** is an occurrence that can trigger behavior. A **guard** is a Boolean condition controlling whether a transition or succession is enabled.
- A **transition** maps a source state, triggering event/condition and input context to a target state plus outputs/effects.
- **Concurrency** permits partially ordered or overlapping occurrences. **Interleaving** is one linearization and must not be confused with true independence.
- **Timing semantics** define clocks/reference, durations, deadlines, latency, periodicity, jitter, timeout and ordering; diagram position is not a time specification.
- **Nondeterminism** means more than one behavior is permitted from the same modeled condition; it can be intentional abstraction or an unresolved conflict.
- **Deadlock** is a reachable state with no permitted progress when progress is required. **Livelock** permits internal activity without required external progress.
- A **safety property** excludes bad traces/states; a **liveness property** requires eventual progress under stated fairness/environment assumptions.
- **Model checking** explores a formalized transition model against properties. Its conclusion is bounded by modeled state, semantics, abstraction, assumptions and tool correctness.

### Central model, mechanism, or theorem

Represent a labeled transition system as

\[
\mathcal{B}=(S,S_0,E,I,O,T,Inv,Time),
\]

where $S$ is state, $S_0$ initial states, $E$ events, $I/O$ inputs and outputs, $T\subseteq S\times E\times Guard\times Effect\times S$ transitions, $Inv$ state invariants and $Time$ clock/timing semantics.

A concrete execution trace is

\[
\sigma=s_0\xrightarrow{e_1,g_1/o_1}s_1\xrightarrow{e_2,g_2/o_2}\cdots .
\]

Structural checks can establish that every declared state is reachable, no state/event pair is accidentally ambiguous, and required safe states have modeled paths. Formal verification can establish $\mathcal{B}\models\varphi$ for property $\varphi$. Neither establishes that $\mathcal{B}$ includes every relevant environmental, human, physical, adversarial or failure behavior, so validation and empirical evidence remain necessary.

### Critical invariants

- Every behavior model declares system boundary, purpose/intended use, abstraction, baseline/configuration, actors/performers, environment and authoritative semantics.
- Scenarios, activities, interactions, state machines, timing models and algorithms are linked complementary views; none silently substitutes for another.
- Actions identify inputs, outputs/effects, preconditions, postconditions, resources, performer/responsibility and failure/exception behavior where relevant.
- Events, guards, priorities and transition effects are explicit; overlapping guards and unhandled events are either intentional and governed or defects.
- Initial, final, safe/degraded/emergency and recovery states/modes are defined with entry/exit/invariants and permitted transitions.
- Concurrency exposes synchronization, shared resources, races, ordering, cancellation, backpressure and common-cause dependencies.
- Time uses declared clocks, reference events, units, bounds, uncertainty and composition; visual spacing carries no semantics.
- Human, software, hardware, organization and external-service behavior are modeled at the level needed for lifecycle decisions.
- Nominal, boundary, degraded, fault, misuse, abuse, interruption, recovery and shutdown/disposal behavior are considered proportionally.
- Requirements trace to observable behavior and properties; behavior can derive new requirements, interfaces, hazards and verification cases through governed rationale.
- Structural validation, simulation, model checking, test and operational observation retain distinct evidence claims and configured inputs.
- Abstraction mappings and assumptions connect formal/model state to real system observations; state-space reduction preserves named properties.
- Behavior changes undergo impact analysis across requirements, structure, interfaces, timing, safety/security, tests, procedures and decisions.
- A passed model property never overrides contradictory field/test evidence or legitimizes an incomplete model.

### Common failures

Common failures include drawing only the happy path; using an activity diagram as a flowchart without tokens/data/resources; using sequence diagrams as the complete protocol; calling every variable value a state; mixing mode and lifecycle phase; omitting initial or termination behavior; using prose inside guards; overlapping guards without priority; ignoring unhandled events; permitting impossible transitions; assuming the diagram's left-to-right distance means time; serializing concurrent work; hiding queues and backpressure; omitting cancellation and retries; treating timeout as a benign branch; missing human confirmation and workload; modeling components without environmental behavior; ignoring degraded/manual/maintenance states; declaring “safe state” without reachability or hazard evidence; checking only state coverage; confusing simulation traces with exhaustive proof; verifying a formal property on the wrong abstraction; and updating behavior without propagating requirements, interfaces or tests.

### Compact example

A pump controller has OFF, STARTING, RUNNING, DEGRADED and SAFE states. Eight transitions cover start/readiness, startup timeout, stop, minor/major fault, recovery and escalation. A checker confirms unique state-event pairs, all states reachable, no nonterminal dead ends, a reachable safe state and requirement IDs on every transition. It does not show that sensor faults, simultaneous events, timing, physical hydraulic response, operator actions or the chosen safe state are adequate; those require richer models and evidence.

### Connections

SYSENG-052 supplies behavioral requirements and SYSENG-054 allocates behavior to structure. SYSENG-055 supplies timing/resource constraints; SYSENG-056–058 integrate trace, consistency and simulations; SYSENG-059–060 address review and tool boundaries. Earlier ConOps, functions, interfaces, hazards, verification and human-work modules define the realities a behavior model must represent.

## Governing Question

For every material operational situation, can the team explain what triggers the system, what concurrently happens, which actors and resources participate, what information/energy/material crosses boundaries, how state and time change, how faults and interruptions are handled, and which observable evidence shows the required outcome?

If the answer depends on mentally combining inconsistent diagrams, the behavior is not sufficiently modeled. The goal is not one giant executable model; it is a coherent set of purpose-fit views with explicit semantic ownership and traceable evidence.

## Why This Matters

Static architecture can appear complete while dynamic behavior fails at transitions: initialization uses stale data, two components wait forever, retry storms exhaust capacity, an operator acts on outdated state, recovery violates an invariant, or a nominally safe shutdown removes a needed service. These defects cross hardware, software, people, procedures, networks and organizations.

NASA Logical Decomposition uses functional analysis to create detailed functional requirements and architecture from stakeholder expectations. The handbook identifies functional flow, timing and state analysis as systems-engineering techniques. NASA-HDBK-1009A integrates system modeling into NASA processes and provides behavior-model examples. SysML 2.0 defines actions as occurrences over time with input/output parameters, nested performances, successions, guards and control nodes, and also defines states and transitions.

NASA software guidance calls for behavior-based, scenario/use-case and state/mode analysis, especially for safety-critical requirements and safe-state behavior. NIST IR 8539 demonstrates how transition models and temporal properties can expose security-policy semantics and support model checking. These sources support analytic rigor while reinforcing a limit: property verification is only as relevant as the transition model and operational mapping.

## Prerequisites and Retrieval

Before modeling behavior, retrieve:

1. system boundary/configuration, lifecycle, ConOps, mission threads, use/misuse cases, actors, external systems, environments, modes/states and success/failure outcomes;
2. functional, performance, timing, interface, safety, security, privacy, human-factor, reliability, maintainability and recovery requirements with rationale;
3. functions/actions and decompositions, logical/physical architecture, performers, interfaces, item/data/energy flows, resources and budgets;
4. hazards/threats, faults, failures, incidents, controls, risk responses, safe/degraded behavior and emergency/contingency procedures;
5. existing use-case, activity/flow, sequence/interaction, state/mode, timing, algorithm, simulation, operator-task and business-process models;
6. clocks/reference events, latency/duration/period/deadline/jitter data, scheduling/priority, queues/capacity, concurrency and synchronization;
7. model language/profile/metamodel, execution semantics, abstraction/mapping, solver/simulator versions, assumptions and property specifications;
8. verification cases, tests/logs/telemetry, field observations, anomalies, model-checking/simulation results and configured baselines.

Use a retrieval test: “On fault the system enters safe mode.” Ask which system/configuration and fault set, how detected and distinguished, detection/transition deadline, concurrent work cancellation, data/energy effects, operator notification/authority, what “safe” means for each hazard and stakeholder, which recovery is allowed, and which evidence covers sensor/common-cause/adversarial faults. A state label is not a safety case.

## Learning Objectives

After completing this module, you should be able to:

1. select scenario, activity, interaction, state, timing and algorithm views for explicit questions;
2. define behavior semantics for events, actions, flows, guards, effects, states, modes, resources and time;
3. model nominal, alternate, boundary, failure, interruption, recovery and retirement paths;
4. represent concurrency, synchronization, queues, priorities, cancellation and backpressure;
5. detect unreachable states/actions, deadlock/livelock, missing events, guard overlap, invalid transitions and timing conflicts;
6. link behavior bidirectionally with requirements, structure, interfaces, hazards, humans and verification cases;
7. distinguish simulation, exploration, model checking, test and operational validation claims;
8. state safety/liveness properties and abstraction/environment/fairness assumptions;
9. govern behavior baselines, variants, changes, generated implementations and evidence;
10. review and communicate bounded conclusions without confusing model semantics with the real system.

## Core Exposition

**Start with an operational question.** Decide whether the model must clarify stakeholder interaction, functional allocation, interface ordering, controller states, timing margin, human work, failure recovery, security policy or verification coverage. Choose abstraction and notation only after purpose. One model rarely answers all questions well.

**Ground behavior in scenarios.** Identify actor goal, starting configuration, trigger, environment, assumptions, nominal steps, alternatives, exceptions, outcomes and postconditions. Include people affected but not actively operating the system. Scenarios sample the behavior space and drive discovery; do not claim completeness from a few stories.

**Define actions semantically.** For each action/function, state what transforms, inputs, outputs, controls, preconditions, postconditions/effects, performer, resources, duration and exceptions. Decompose only until responsibility, interfaces, requirements and verification are clear. Avoid algorithmic design detail when the intended model is solution-neutral.

**Model flows explicitly.** Distinguish control tokens, data/information, material, energy and authority. Name item type/schema/unit/classification, producer, consumer and transformation. Fork/join semantics must say whether all, any or selected branches synchronize. Hidden flows create missing interfaces and security/privacy problems.

**Use interaction models for contracts.** Show participants, messages/events, direction, order/partial order, correlation, response, timeout, retry, cancellation and alternative/error fragments. Link messages to interface definitions. A sequence trace is one permitted scenario unless the notation explicitly generalizes; it cannot alone rule out other sequences.

**Define state by relevant memory.** Two histories belong to the same state only if future modeled response is equivalent for the purpose. Separate orthogonal regions when possible. Define initial state, entry/exit behavior, invariants and final/terminal meaning. Avoid state explosion from irrelevant variables and avoid collapsing histories that change safety or response.

**Separate modes from states deliberately.** A mode may configure sets of functions, limits, interfaces and authority across several components, while a local state records progress. Define their relationship and prohibited combinations. Lifecycle phase, test configuration and operational mode are different axes unless the metamodel says otherwise.

**Specify transitions completely.** Record source, event, guard, priority, target, actions/effects, outputs, timing, consumed inputs and requirement/hazard links. Determine behavior for simultaneous events and guards. Decide whether absent transition means ignore, defer, reject, remain, error or unspecified; silence is dangerous.

**Handle nondeterminism honestly.** Multiple transitions may be intentionally allowed because environment or implementation chooses. Document resolution and properties that must hold for every choice. Accidental overlapping guards or unclear priority are defects. Do not force fake determinism when evidence cannot distinguish behavior.

**Model concurrency as partial order.** Identify independent and dependent actions, shared resources, locks/transactions, message delivery, queues, scheduling, priority inversion, races and synchronization barriers. Enumerate critical interleavings or use formal/simulation tools. A single sequence drawing hides concurrency risk.

**Make time first-class.** Define clock domains, synchronization, drift, reference events, durations, deadlines, periods, latency distributions/bounds, jitter, timeout and freshness. Trace end-to-end timing through actions, queues, interfaces and human response. State worst-case/statistical assumptions and correlation. Diagram spacing has no timing value.

**Represent resources and capacity.** Behavior consumes processors, power, bandwidth, memory, storage, fuel, operators, beds, vehicles or permissions. Model acquisition/release, contention, capacity and degraded availability. A behavior that is logically enabled but lacks a required resource is not operationally feasible.

**Model data and state effects.** State transitions may depend on data age, quality, classification and consistency. Record read/write ownership, atomicity, persistence, replication and rollback. Retries require idempotency or compensation semantics. Do not treat data flow as control flow.

**Include humans and organizations.** Model perception, information presentation, decision authority, workload, communication, handoffs, confirmation, training and recovery. Human variability is not a random delay placeholder. Include staffing, shifts and conflicting goals. Validate with representative participants and conditions.

**Develop failure behavior causally.** Start from fault/threat/event detection through isolation, containment, degraded service, notification, compensation, recovery and return. Include missed/false detection, common cause, simultaneous faults, repair failure and unsafe recovery. Link hazards and controls; a transition to SAFE needs a defensible invariant and reachability/timing evidence.

**Specify safety and liveness properties.** Examples: “a hazardous actuator is never energized when guard open” (safety) and “every accepted emergency request eventually receives service or an explicit failure” (liveness). State environment and fairness assumptions. Liveness can be false under permanent network failure unless fallback or bounded assumptions exist.

**Check structural integrity.** Detect missing initial/final states, unreachable states/actions, nonterminal dead ends, orphan flows, unmatched sends/receives, unhandled events, guard gaps/overlap, impossible joins, cycles without progress and invalid types/units. Structural success does not establish complete operational semantics.

**Explore and simulate.** Execute representative, boundary, random, adversarial and failure scenarios; capture seeds, inputs, configurations and coverage. Simulation can estimate distributions and reveal emergent timing/resource effects. Finite traces do not prove absence of unobserved behavior.

**Use formal verification selectively.** Translate a controlled abstraction and properties into a model checker/theorem/protocol tool. Check invariants, reachability, deadlock, temporal ordering and liveness. Record abstraction, state reduction, environment, fairness, tool/version and counterexamples. Confirm that reductions preserve the named property and map results back to system concepts.

**Validate the model.** Review scenarios and semantics with stakeholders, domain experts, operators, safety/security and implementers. Compare model predictions/traces to prototypes, tests, incidents and operational data under aligned configuration. Investigate discrepancy among model, implementation, measurement and environment; never declare the model right by authority.

**Trace but do not overclaim.** Link requirements to actions, states, transitions and properties; behavior to performers and interfaces; hazards to fault paths; verification cases to traces/coverage. A requirement connected to a transition is represented, not necessarily satisfied. Derive new requirements through explicit reasoning.

**Manage variants and refinement.** Preserve abstract behavior while refining into detailed behavior and allocation. Define conformance: trace inclusion, simulation relation, contract preservation or project rule. Check variant modes/features and environment assumptions. Similar diagrams do not prove refinement.

**Control change and generation.** Baseline model, libraries, semantics, property set and toolchain. Assess changes across requirements, structure, interfaces, timing/resources, hazards, code/configuration, procedures and tests. Generated code or test cases inherit model/tool defects and require review/verification. Preserve prior decision configurations.

The following executable teaching model checks a five-state transition table. It deliberately treats SAFE as an allowed terminal state. It cannot evaluate timing, guards, concurrency, hydraulics, sensor coverage, human behavior or whether SAFE is actually safe.

<!-- bijux-verify: {"id":"behavior-transition-integrity-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"states=5\ntransitions=8\nunique_state_event_pairs=1\nreachable_states=5\nunreachable_states=0\nguard_conflicts=0\ndead_end_nonterminal=0\nsafe_state_reachable=1\nrequirements_traced=8\nstatus=behavior_model_structurally_consistent\nevidence=declared_transition_table_only\n","stderr":""}} -->
```python
states = {"OFF", "STARTING", "RUNNING", "DEGRADED", "SAFE"}
initial = "OFF"
terminal = {"SAFE"}
transitions = [
    ("OFF", "start", "STARTING", "BR-01"),
    ("STARTING", "ready", "RUNNING", "BR-02"),
    ("STARTING", "timeout", "SAFE", "BR-03"),
    ("RUNNING", "stop", "OFF", "BR-04"),
    ("RUNNING", "minor-fault", "DEGRADED", "BR-05"),
    ("RUNNING", "major-fault", "SAFE", "BR-06"),
    ("DEGRADED", "recover", "RUNNING", "BR-07"),
    ("DEGRADED", "escalate", "SAFE", "BR-08"),
]
pairs = [(source, event) for source, event, _, _ in transitions]
adjacency = {state: set() for state in states}
for source, _, target, _ in transitions:
    adjacency[source].add(target)
reachable, frontier = {initial}, [initial]
while frontier:
    source = frontier.pop()
    for target in adjacency[source] - reachable:
        reachable.add(target)
        frontier.append(target)
dead_ends = [state for state in states - terminal if not adjacency[state]]

print(f"states={len(states)}")
print(f"transitions={len(transitions)}")
print(f"unique_state_event_pairs={int(len(pairs) == len(set(pairs)))}")
print(f"reachable_states={len(reachable)}")
print(f"unreachable_states={len(states - reachable)}")
print(f"guard_conflicts={len(pairs) - len(set(pairs))}")
print(f"dead_end_nonterminal={len(dead_ends)}")
print(f"safe_state_reachable={int('SAFE' in reachable)}")
print(f"requirements_traced={sum(bool(requirement) for *_, requirement in transitions)}")
consistent = states == reachable and len(pairs) == len(set(pairs)) and not dead_ends
print("status=" + ("behavior_model_structurally_consistent" if consistent else
                   "behavior_model_needs_work"))
print("evidence=declared_transition_table_only")
```

Unique state-event pairs are a simplified proxy because real guards may partition or overlap the same event. A complete review must examine guard satisfiability, event priority, invariants, effects, time and every relevant environment/fault combination.

## Definitions and Notation

Let enabled transitions in state $s$ for event $e$ and valuation $x$ be

\[
Enabled(s,e,x)=\{t\in T:t.source=s\land t.event=e\land t.guard(x)\}.
\]

Determinism for the modeled condition requires $|Enabled|\le 1$; completeness may require $|Enabled|=1$ for every admissible condition. Intentional nondeterminism relaxes uniqueness but properties must hold across permitted choices.

For actions $a\prec b$, $a$ must complete or reach a declared synchronization point before $b$. If neither $a\prec b$ nor $b\prec a$, concurrency is permitted but resource/data constraints can still impose runtime order.

End-to-end latency is not automatically additive under concurrency and queues. A generic composition is

\[
L=f(D,Q,C,N,H,U),
\]

with action durations $D$, queues $Q$, concurrency/scheduling $C$, network/interface delay $N$, human contribution $H$ and uncertainty $U$.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—scope and scenario.** Define intended question, boundary, actors, triggers, context, paths, outcomes and abstraction.

**Mechanism 2—semantic behavior.** Define actions/flows, interactions, states/modes, events/guards/effects, concurrency, time, resources and human/external behavior.

**Mechanism 3—off-nominal assurance.** Add faults, threats, degradation, interruption, safe behavior, recovery, shutdown and safety/liveness properties.

**Mechanism 4—analysis and evidence.** Run structural checks, scenario simulation, formal verification and configuration-aligned validation with bounded claims.

**Mechanism 5—integration and lifecycle.** Trace to requirements/structure/interfaces/hazards/tests, refine variants, control changes/generation and reconcile operational evidence.

A verified property is conditional on the transition semantics, abstraction and assumptions. Its system meaning requires a defensible mapping to real observations and relevant omitted phenomena.

## Alternatives and Trade-Offs

**Scenario narratives** communicate goals and exceptions but sample behavior. **State/activity formalisms** enable broader analysis but demand semantics and training. Link rather than substitute.

**One integrated executable model** improves consistency and automation but can become huge, brittle and inaccessible. **Federated purpose-fit models** scale disciplines but require identity, mapping and consistency governance.

**Deterministic models** ease implementation and testing. **Nondeterministic abstractions** preserve legitimate freedom and environment uncertainty. Make choice and resolution explicit.

**Synchronous semantics** simplify step reasoning. **Asynchronous semantics** reflect distributed reality but introduce queues, delay, reordering and failure. Do not analyze one while implementing the other.

**Detailed timing/resource models** improve feasibility evidence but cost data and maintenance. Add fidelity where decision sensitivity and consequence justify it.

**Formal model checking** explores abstract state systematically and produces counterexamples. **Simulation/test** handles richer physics and implementation but samples cases. Combine evidence without merging claims.

## Failure Modes and Misconceptions

**“Use cases are requirements.”** They reveal context and behavior; derive precise obligations separately.

**“Every path in a diagram is possible.”** Guards, resources, invariants and environment may make paths infeasible.

**“State coverage is behavior coverage.”** Transitions, conditions, sequences, timing, data and concurrency matter.

**“A safe state is a named box.”** Safety depends on hazard, time, environment, outputs, people and reachability.

**“Retries improve reliability.”** Without bounds, backoff, idempotency and capacity, retries can amplify failure.

**“Parallel branches run independently.”** They can share resources, data and common causes.

**“Model checking proves the system.”** It proves a property of a formalized model under assumptions.

**“Simulation found no failure.”** Finite scenarios are positive evidence within coverage, not absence proof.

**“Human behavior is a delay distribution.”** Perception, authority, workload, communication and adaptation need explicit treatment.

**“Generated implementation preserves intent.”** Generator and platform semantics, timing and environment require verification.

## Worked Examples

### Example 1

**Alternate clinical path.** A medication workflow models allergy-data unavailable, clinician override, second check, patient refusal and emergency exception; nominal order-entry sequence alone had hidden the authority and safety states.

### Example 2

**Guard overlap.** `temperature > 80` enters cooling while `sensor_invalid or temperature > 90` enters safe shutdown. At 95 with invalid sensor both enable; priority/semantics and hazard rationale must be explicit.

### Example 3

**Deadlock.** Two services each hold one resource and await the other. A pretty sequence never shows the interleaving; a resource/transition model produces a counterexample and drives ordering/timeout requirements.

### Example 4

**Retry storm.** Client, gateway and worker independently retry after timeouts. Queue and timing simulation exposes overload feedback. Bounded coordinated retry, idempotency and backpressure become architectural requirements.

### Example 5

**Mode/state confusion.** TRAINING and OPERATIONAL are system modes; READY and ACTIVE are controller states. Modeling orthogonal axes prevents an ACTIVE controller from using live outputs during TRAINING.

### Example 6

**Safe-state timing.** A major fault transition reaches SAFE logically, but valve closure takes longer than hazard tolerance under low temperature. Physical/timing evidence refutes an adequate-looking state machine.

### Example 7

**Human handoff.** Automation transfers control during degraded sensing. The behavior includes attention capture, situation summary, authority acknowledgment, response window and fallback; instantaneous “handoff” was unsafe.

### Example 8

**Security policy.** A transition model shows roles, grants, revocation and access. A temporal property forbids access after revocation; model checking finds a cached-token path. Real token/cache implementation still needs test evidence.

### Example 9

**Variant refinement.** A low-connectivity product refines synchronous cloud authorization into local cached authorization plus reconciliation. Trace inclusion and security/privacy properties are checked under explicit staleness assumptions.

### Example 10

**Operational discrepancy.** Telemetry shows repeated DEGRADED↔RUNNING oscillation absent from the model. Engineers align configuration and investigate hysteresis, sensor noise, implementation, model and environment before changing authority.

## Cross-Program Connections

**Platform engineering.** Reconciliation loops, deployment, autoscaling, policy, incident and recovery behavior require states, concurrency, backpressure and desired/observed-state semantics.

**API and service engineering.** Protocol sequences, retries, timeouts, idempotency, sagas and compatibility are behavior contracts, not just endpoint schemas.

**Data engineering.** Pipeline scheduling, event time, watermarks, replay, late data, transactions and recovery need explicit state and temporal behavior.

**Object-oriented programming.** Object protocols and state-dependent methods benefit from state models; class structure alone cannot express legal call sequences.

**Functional programming.** State transitions, algebraic effects, event streams and temporal properties can be expressed compositionally, but external effects and runtime schedules remain empirical concerns.

## References

1. NASA, *Systems Engineering Handbook, Section 4.3: Logical Decomposition*, current web edition. <https://www.nasa.gov/reference/4-3-logical-decomposition/>
2. NASA, *Systems Engineering Handbook, Section 4.0: System Design Processes*, current web edition. <https://www.nasa.gov/reference/4-0-system-design-processes/>
3. NASA, *Systems Engineering Handbook, Appendix F: Functional, Timing, and State Analysis*, current routing page. <https://www.nasa.gov/reference/appendix-f-functional-timing-and-state-analysis/>
4. NASA, *NASA Systems Modeling Handbook for Systems Engineering*, NASA-HDBK-1009A, active 2025. <https://standards.nasa.gov/standard/NASA/NASA-HDBK-1009>
5. Object Management Group, *Systems Modeling Language Specification Version 2.0*, 2025. <https://www.omg.org/spec/SysML/2.0>
6. NASA, *Systems Engineering Handbook, Section 4.1: Stakeholder Expectations Definition*, current web edition. <https://www.nasa.gov/reference/4-1-stakeholder-expectations-definition/>
7. NASA, *Systems Engineering Handbook, Section 4.2: Technical Requirements Definition*, current web edition. <https://www.nasa.gov/reference/4-2-technical-requirements-definition/>
8. NASA Software Engineering Handbook, *SWE-051: Software Requirements Analysis*, current Version D. <https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695426/SWE-051%2B-%2BSoftware%2BRequirements%2BAnalysis>
9. NIST, *IR 8539: Security Property Verification by Transition Model*, 2025. <https://csrc.nist.gov/pubs/ir/8539/final>
10. NASA, *Systems Engineering Handbook, Section 6.3: Interface Management*, current web edition. <https://www.nasa.gov/reference/6-3-interface-management/>

## Exercises

### Exercise 1

Design complementary behavior models for an automated rail-door system across boarding, departure, obstruction, manual override, sensor disagreement, power loss and evacuation.

### Exercise 2

Audit a state machine with 22 states, no declared initial state, three unreachable states, two nonterminal dead ends, overlapping guards, unhandled timeout, a “SAFE” state without invariant, and 95-percent state coverage.

### Exercise 3

Model and analyze a distributed payment workflow with retries, idempotency, duplicate/out-of-order messages, partial failure, compensation and reconciliation.

### Exercise 4

Explain what evidence is needed to claim that a formally checked access-control transition model supports the security of a deployed service.

### Exercise 5

Operational data show a recovery loop oscillating between DEGRADED and RUNNING, overloading operators. Plan diagnosis, correction, verification and controlled behavior-model change.

## Answers to the Exercises

### Answer 1

Start with actors and outcomes: passengers including mobility/sensory/cognitive subgroups, operator/driver, platform staff, maintenance, train control and emergency services. Define vehicle/platform configuration, station alignment, train stopped/moving, side selection, operating/manual/maintenance/evacuation modes, crowd/weather/lighting and power/network states. Build scenarios for arrival, enable, opening, boarding/alighting, warning, closing, lock/prove, departure; then obstruction, repeated obstruction, trapped item/person, sensor disagreement/failure, manual release, power loss and evacuation.

Use an activity/functional model for sensing, authorize-side, command, actuate, detect obstruction, warn, verify lock and release train; show data/power/control flows, performers and resources. Use interactions for train control–door controller–operator–platform messages, acknowledgments, timeout and manual authority. Use state machines for CLOSED_LOCKED, OPENING, OPEN, CLOSING, OBSTRUCTED, ISOLATED, MANUAL_RELEASED and FAULT/SAFE, with operational mode orthogonal where needed. Use timing models for warning, closure force/time, obstruction response, lock proof and departure inhibition.

Define guards, simultaneous events, priorities and effects. Model moving-train inhibition, wrong-side prevention, door interlock, degraded isolation, passenger alarm and emergency release. “Safe” differs by hazard: preventing departure with an unlocked door may conflict with evacuation; authority and context matter. Include human detection, display, acknowledgment, workload and fallback.

Trace requirements/hazards/interfaces to behavior and allocate across sensors, controller, actuator, train control, operator and procedures. Analyze reachability, deadlock, guard gaps/overlap, repeated obstruction, sensor common cause, power transients, queued commands and recovery. Simulate loads and faults; formally check critical invariants where semantics support it; test representative hardware, timing, environmental and human cases. Validate with affected passengers/operators, preserve anomalies and reopen on incident or configuration evidence.

### Answer 2

Freeze the audited baseline, language/profile/tool semantics and properties. Identify intended state-machine scope, environment, events and required progress. Add an authorized initial configuration only after deriving it from ConOps/reset behavior; do not choose the visually top state. Determine whether three unreachable states are obsolete, missing transitions/guards, variant-only or evidence of incomplete environment. Retain rationale and impact when removing or reconnecting them.

For two nonterminal dead ends, decide whether termination was omitted, an event/environment assumption is absent, or a real deadlock exists. Add neither self-loops nor catch-all transitions merely to satisfy lint. Enumerate overlapping guard valuations and priority; prove disjointness, define deterministic precedence or document intentional nondeterminism and check properties for all choices. Specify timeout source, clock, bound, event handling, target/effects and late-event behavior.

Define SAFE through hazard-specific invariants, outputs, energy/data state, service consequences, operator communication, entry deadline, persistence and recovery authority. Demonstrate reachability under relevant faults and that entry does not create a worse hazard. Inspect all unhandled events by state and simultaneous-event rules.

Replace the 95-percent claim with state, transition, guard-boundary, event-sequence, timing, requirement/hazard and scenario coverage. Run structural checks and generate counterexamples. Perform domain/safety/operator review, simulation/model checking as appropriate, and configuration-aligned tests. A fully reachable machine can still omit the real failure that matters.

### Answer 3

Define payment identity, parties, ledger/processor/service boundaries, amount/currency, authorization/capture/refund semantics, consistency, finality, timeout and legal/audit/security obligations. Give every client intent a stable idempotency key and every message/event a unique/correlated identity. Model durable states such as RECEIVED, VALIDATED, AUTHORIZING, AUTHORIZED, CAPTURING, SETTLED, DECLINED, COMPENSATING, RECONCILE and MANUAL_REVIEW, separating external provider state from local belief.

Model at-least-once/loss/delay/duplicate/reordering, crashes before/after persistence, ambiguous provider timeout, concurrent retry and replay. Define transition preconditions, atomic state/outbox/inbox writes, deduplication window, idempotent provider contract, retry budget/backoff/jitter, queue capacity/backpressure and poison handling. Never infer failure from timeout when outcome may be unknown.

For compensation, specify which actions are reversible, authority, financial effects, retry/reconciliation and user communication; compensation is a new transaction, not deletion. Reconciliation compares authoritative ledgers using stable identity, detects missing/duplicate/mismatched outcomes and routes bounded exceptions. Protect against replay and unauthorized state transitions.

Check no double capture/settlement, monetary conservation under declared fees/rounding, valid terminal states, eventual explicit outcome under bounded provider/fairness assumptions, and recoverability after each persistence/send point. Explore failure interleavings with deterministic simulation/property-based/model checking where suitable. Test sandbox and fault-injected integration, then reconcile production shadow evidence. Preserve model/tool/configuration and limits; external provider/legal behavior still requires empirical and contractual evidence.

### Answer 4

State exactly which security properties, service/configuration, identities/roles/resources/actions, policy version, threat/environment and intended decision the model covers. Preserve mapping from deployed policy constructs and code/configuration to model states, events, guards and effects. Document abstractions, omitted mechanisms, trust boundaries, attacker capabilities, concurrency, token/cache/session lifetime, clock and revocation semantics, and fairness/environment assumptions.

Verify model construction and translation: parser/generator/tool versions, property formulation, state reduction, initial states, environment constraints and counterexample interpretation. Independently review that the property expresses the security requirement and that abstraction preserves it. Record whether the result covers all reachable modeled traces or a bounded domain.

Then verify implementation correspondence through configuration review, generated-policy comparison if applicable, unit/contract tests, state-transition and negative tests, concurrency/race/replay/cache/revocation cases, penetration/adversarial testing and deployment inspection. Validate identity-provider, proxy, database, queue and operational-admin behavior across failure/recovery. Monitor logs/telemetry with provenance and investigate divergence.

Assess model and implementation supply chain, tool qualification proportional to consequence, access/change control and deployed baseline. Link residual threats and unmodeled properties to risk authority. The defensible claim is that a specific formal model satisfies named properties and configured implementation evidence supports correspondence within limits—not that the deployed service is secure in general.

### Answer 5

Protect operations first: define escalation, dwell limits, manual/degraded mode, staffing and workload relief under accountable authority. Preserve telemetry, alarms, commands, operator actions/communications, software/configuration, sensors/calibration, environment/load and the authoritative behavior baseline. Quantify oscillation frequency, dwell, trigger values, hysteresis, consequences and affected shifts/sites; do not smooth away transitions.

Align clocks, IDs, state definitions and configurations. Reconstruct traces around every DEGRADED↔RUNNING edge. Form hypotheses: overlapping guards, insufficient hysteresis/debounce, noisy/biasing sensor, delayed data, concurrent health evaluators, recovery before causal fault clears, timeout/retry interaction, implementation/model mismatch, resource pressure or operator intervention. Check common cause and safety impact.

Use targeted replay, instrumentation, boundary tests, fault injection, scheduling/concurrency analysis and model exploration to discriminate. Inspect guard satisfiability/priority, invariants, entry/exit actions, timers and cancellation. Model operator attention, acknowledgment, handoff and repeated workload, not just automatic state.

Evaluate alternatives such as hysteresis and minimum dwell, evidence-based recovery gate, single transition authority, filtered/qualified sensing, rate limiting, latch/manual review or deeper fault correction. Analyze delayed recovery and missed-fault risks. Update requirements, hazards, interfaces, timing/resource budgets, procedures/training, monitoring and tests through impact-aware decision/change control.

Baseline the corrected model and implementation together. Re-run reachability, guard, deadlock/liveness and safety properties; test nominal, boundary, noisy, delayed, simultaneous and common-cause cases with representative operators. Stage rollout with rollback. Validate reduced oscillation and workload without increased unsafe dwell or missed recovery. Preserve old/new records and reopen on recurrence, new environment/configuration or outcome thresholds.
