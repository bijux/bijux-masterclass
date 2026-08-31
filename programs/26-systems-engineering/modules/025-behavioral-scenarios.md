---
module_id: SYSENG-025
program: Systems Engineering
level: 1
module_number: 25
title: Behavioral Scenarios
status: complete
last_verified: 2026-08-31
---

# Behavioral Scenarios

## One-Page Review

### Governing question

How can a team construct and govern a portfolio of behavioral scenarios that exposes how people, systems, environments, functions, interfaces, states, timing, resources, and failures interact across the lifecycle—so requirements and architecture can be challenged in context without mistaking a compelling story, sampled trace, or test script for complete behavior?

### Essential definitions

- A **behavioral scenario** is a controlled description/model of a credible sequence or partial order of events and interactions from a defined initial context toward outcomes.
- An **operational scenario** emphasizes system use with actors and environment; a **design reference mission/scenario** provides a selected reference case for analysis and comparison.
- A **use case** describes goal-oriented interaction and may contain many scenarios; a scenario is one path or family of paths through it.
- A **main/nominal flow** represents expected successful behavior under stated conditions; **alternate**, **off-nominal**, **exception**, **degraded**, and **emergency** flows vary conditions or outcomes.
- A **precondition** must hold before the scenario begins; a **trigger** initiates it; a **postcondition/outcome** describes the ending evidence and system/stakeholder state.
- An **actor** is a person, organization, external system, environment, or other role interacting at the modeled boundary; a role is not automatically an implementation element.
- A **scenario parameter** varies population, environment, timing, load, configuration, failure, threat, or behavior while preserving the scenario’s identity/rationale.
- A **scenario portfolio** is a governed set selected to cover decision-relevant lifecycle, stakeholder, mode, interface, performance, hazard, threat, and uncertainty dimensions.
- A **witness trace** demonstrates one admissible execution; it neither proves all required behavior nor excludes prohibited behavior.
- **Scenario coverage** is a scoped mapping from declared obligations/risk dimensions to scenarios and evidence; raw scenario count is not completeness.
- A **scenario oracle** defines expected observations and acceptable bounds; narrative plausibility is not an oracle.
- An **assumption** constrains applicability and must be traceable, testable/reviewable where possible, monitored, and revisited after change.

### Central model, mechanism, or theorem

Represent a scenario as:

$$
\Gamma=\langle id,B,A,E,C,S_0,tr,F,O,Q,H,U,V\rangle,
$$

where $B$ is boundary/configuration, $A$ actors/authority, $E$ environment, $C$ constraints/resources, $S_0$ initial state/mode, $tr$ trigger, $F$ ordered/partially ordered flow with branches, $O$ outcomes/postconditions, $Q$ quality/timing/oracles, $H$ assumptions, $U$ uncertainties, and $V$ trace/evidence.

For declared coverage obligations $D$ and portfolio $P$:

$$
Coverage(P,D)=\frac{|\{d\in D:\exists\Gamma\in P,\ AdequatelyCovers(\Gamma,d)\}|}{|D|}.
$$

This ratio is interpretable only with the exact denominator, adequacy criteria, versions, exclusions, and semantic review. Even 100% does not prove that $D$ itself is complete.

### Critical invariants

- Every scenario has stable identity, version, owner, purpose, decision use, boundary, configuration, and source rationale.
- Actors are roles with goals, capabilities, constraints, information, authority, workload, and failure/error possibilities.
- Initial physical/estimated/control states, modes, environment, resources, data, and assumptions are explicit.
- Events and interactions identify producer, consumer, object/effect, timing/order, state change, uncertainty, and failure semantics as relevant.
- Main, alternate, off-nominal, degraded, emergency, recovery, and termination paths preserve trace to requirements and hazards/threats.
- Outcomes distinguish command from physical effect, activity from stakeholder value, and planned evidence from observed result.
- Scenario narratives remain consistent with function, FFBD, state/mode, interface, timing, resource, and physical models.
- Portfolio selection considers lifecycle stages from concept, integration, test, deployment, operation, sustainment, update, and disposal.
- Boundary values, rare/high-consequence cases, human error, adversarial action, common cause, and interacting changes are not averaged away.
- Scenarios remain implementation-neutral until authoritative constraints or a deliberate architecture decision justify detail.
- Generated, simulated, replayed, or tested traces record model/configuration/population/environment and evidence limits.
- Scenario sufficiency and acceptance use affected stakeholders and competent domain/assurance authorities proportional to consequence.

### Common failures

Failures include writing only a happy path; treating personas as representative evidence; omitting initial mode/configuration; using “system” as one opaque actor; specifying UI/component choices before architecture selection; leaving timing and resources implicit; turning a scenario directly into normative requirement text without analysis; ignoring alternate exits and recovery; duplicating inconsistent flows across documents; using one reference mission as a maximum envelope; counting scenarios instead of mapping coverage; confusing simulation output with field behavior; validating only average users and environments; and claiming that a test passing one scripted trace validates the use case or stakeholder outcome.

### Compact example

An emergency-message scenario begins with a responder in a network-degraded location, current authorization, a time-critical message, limited device energy, and uncertain recipient availability. The responder requests delivery; the system validates identity/content, selects routes, protects and queues the message, reports provisional state, attempts channels, reconciles duplicate acknowledgements, and escalates before the deadline. Alternate flows cover invalid authority, stale location, no channel, delayed acknowledgement, cancellation, recipient handoff, and recovery after partition. Outcomes distinguish `transmitted`, `authenticated acknowledgement received`, `recipient understood`, and `operational response achieved`; each needs different evidence.

### Connections

Behavioral scenarios synthesize stakeholder/ConOps work with functions, decomposition, FFBDs, and state/mode models. They drive logical components, allocation, control/data flows, alternatives, interfaces, human systems integration, timing/resources, risk, verification, validation, operations, digital twins, and configuration/change analysis.

## Governing Question

Models divide behavior into functions, states, interfaces, and requirements. Stakeholders experience none of these in isolation; they experience an unfolding situation. Scenarios recombine views into credible threads: who knows what, what happens next, which resources and environment matter, how modes change, and whether outcomes remain valuable after faults or uncertainty.

Stories are powerful precisely because they can conceal gaps. A fluent narrative may assume perfect data, instantaneous response, unlimited staffing, cooperative users, and successful recovery. The governing question asks how to retain the accessibility of narrative while giving scenarios controlled identities, explicit assumptions, analytical semantics, traceability, and bounded evidence.

## Why This Matters

Many system failures occur in interactions rather than components: a correct alarm arrives during a high-workload handoff; a retry duplicates a dose; a locally safe fallback blocks evacuation; a maintenance procedure changes a shared configuration; individually valid services disagree about time. Scenario analysis exposes these cross-view conditions before integration and operation.

NASA’s current Stakeholder Expectations guidance describes operational scenarios as a dynamic view across modes, transitions, external interfaces, anticipated hazards/faults, and failure mitigation. Its current ConOps outline calls for labeled nominal and off-nominal scenarios covering expected functions and capabilities across the lifecycle. NASA technical-risk guidance defines a scenario as a credible event sequence evolving a system/process from one state to a future state. SEBoK 2.14 identifies scenarios of functions as behavior chains and notes their use in evaluating requirements/design and supporting verification/validation. OMG’s current SysML overview distinguishes use case, activity, sequence, and state-machine behavior views, reinforcing that one notation does not answer every scenario question.

Scenarios also support discovery rather than only documentation. Walking an off-nominal thread can derive a missing function, state, interface, requirement, hazard control, staffing constraint, or verification environment. Those discoveries must enter their authoritative artifacts with rationale; the scenario should not become a shadow specification.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. ConOps establishes actors, outcomes, boundaries, environment, modes, support, and lifecycle context;
2. functions and decomposition express transformations and contribution;
3. FFBDs express execution logic and alternative paths;
4. state/mode models express history, guards, transitions, and concurrent regimes;
5. interface contracts govern exchanged matter, energy, data, information, controls, and effects;
6. traceability links source intent through architecture and evidence;
7. verification checks specified properties while validation examines intended use/outcomes;
8. model/simulation/test results are conditional on configurations, inputs, assumptions, and observed cases.

As a retrieval test, assess “User logs in and completes payment.” Missing context includes user capability/authority, device/network state, identity evidence, amount/currency, merchant state, timeout, duplicate submission, declined/uncertain authorization, accessibility, fraud, privacy, receipt, settlement, cancellation, and recovery. Two steps are not a behavioral scenario fit for engineering decisions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish scenario, use case, design reference mission, requirement, workflow, test case, simulation run, and operational procedure;
2. create a controlled scenario frame with actors, boundary, configuration, initial state, environment, assumptions, trigger, and outcomes;
3. write nominal, alternate, degraded, exception, emergency, recovery, and termination flows;
4. express ordered and concurrent interactions with state, timing, resource, authority, and uncertainty semantics;
5. use parameterization and equivalence arguments without hiding critical variation;
6. construct a risk- and decision-based scenario portfolio and coverage matrix;
7. derive candidate requirements/functions/interfaces while preserving source authority;
8. transform scenarios into verification/validation designs without equating them;
9. use simulation, replay, synthetic data, and field evidence with correct labels and limits;
10. review high-consequence scenarios for representativeness, adversarial gaps, and bounded conclusions.

## Core Exposition

**Define the decision purpose.** State whether a scenario supports stakeholder agreement, requirement discovery, architecture comparison, interface review, hazard/threat analysis, staffing, verification design, validation, training, or change impact. One scenario can serve several purposes, but adequacy criteria differ. Avoid generic stories with no review question.

**Identify the system and scenario boundary.** Name system of interest, included humans/organizations/enabling systems, external entities, geography, temporal horizon, lifecycle stage, and excluded behavior. A person may be inside a sociotechnical boundary and external to a device boundary. Record viewpoint to prevent contradictory actor roles.

**Assign stable identity and governance.** Give scenario ID, title, version, owner, status, source, applicable configurations, review authority, and change history. Use durable domain names, not delivery sequence. References from requirements, models, tests, and decisions must resolve to exact scenario versions.

**Define actor roles.** For each actor, state goal, authority, capabilities, information, limitations, workload, incentives, accessibility, training, and plausible error/misuse. Avoid assuming “operator” can detect or correct anything. External systems have availability, trust, version, and ownership constraints.

**Set initial conditions.** Record physical state, estimated/known state and uncertainty, controller state, operational mode, configuration/baseline, data version, resources, environment, current activities, and unresolved faults. A scenario without initial state cannot support deterministic interpretation or reproducible evidence.

**State trigger and preconditions.** Preconditions are facts required before entry; the trigger is the event/decision that begins the thread. Do not hide actions in preconditions. If a precondition may fail, decide whether it creates another scenario/branch. Define trigger source, timestamp, authentication, duplication, and delay when relevant.

**Write outcomes before steps.** Identify stakeholder outcome, system postconditions, residual state, evidence, and unacceptable outcomes. Distinguish process completion from value: `message sent` differs from `recipient acted`; `model returned score` differs from `patient received appropriate care`. This prevents activity from becoming success by definition.

**Make the scenario falsifiable for its purpose.** State which observation, contradiction, or outcome would show that an assumption, requirement interpretation, architecture claim, or operational concept does not hold. An oracle may include ranges, temporal ordering, prohibited effects, uncertainty, and competent disposition rather than one expected value. Preserve inconclusive results when observability is inadequate. A story that can reinterpret every outcome as success cannot challenge design; it is advocacy. Falsifiability remains scoped: failure of one scenario execution can expose a problem, while success cannot prove all executions or stakeholder contexts acceptable.

**Write the nominal flow.** Describe actor-system-environment interactions at consistent abstraction. Each step names initiator, action/event, object/effect, receiving role/function, state/mode change, and necessary timing. Maintain implementation independence unless a controlled decision fixes a mechanism. A nominal flow is a baseline for challenge, not “the real scenario.”

**Add alternate successful flows.** Capture other legitimate paths: different actor, route, mode, ordering, resource, or optional behavior that achieves an acceptable outcome. Explain choice conditions and equivalent/non-equivalent evidence. Do not multiply scenarios for cosmetic differences; parameterize only when semantics truly remain stable.

**Add off-nominal and exception flows.** Consider missing/invalid/stale/contradictory inputs; delays; resource exhaustion; partial completion; actor error; interface failure; environmental extremes; degraded dependencies; duplicate/out-of-order events; and recovery failure. Each branch has detection, response, escalation, outcome, and residual state.

**Add hazard and adversarial flows.** Use hazard analysis, incident history, threat models, and domain expertise. Include common cause, simultaneous faults, malicious actors, privilege misuse, spoofing, unsafe workaround, and organizational pressure where credible. Avoid sensational cases without decision relevance, but do not exclude rare high-consequence events because averages are favorable.

**Use counterfactual challenge.** Ask what changes if an actor does not cooperate, an external authority rejects the request, a “reliable” dependency is unavailable, an observation is plausible but wrong, the environment crosses a boundary, or two accepted changes coexist. Reverse assumptions one at a time and in causally credible combinations. Counterfactuals reveal hidden dependencies and fragile success conditions, but arbitrary combinations can waste effort; prioritize sensitivity, incident evidence, hazards, threats, novelty, and consequence. Record whether the architecture tolerates, detects, degrades under, or explicitly excludes each challenged condition and who accepts the exclusion.

**Represent order and concurrency.** Narrative words such as “then” and “meanwhile” are often insufficient. Link to FFBD/activity/sequence models for precedence, parallelism, synchronization, timeout, retry, and cancellation. Identify shared resources and races. A sequence diagram message is not necessarily physical effect or completed transaction.

**Represent state and mode changes.** Name initial and terminal states, guards, transitions, and uncertain state knowledge. Cross-check state machines. If a scenario relies on an impossible or forbidden transition, revise it; if it reveals a missing legitimate transition, govern the derived change.

**Represent interfaces and objects.** Specify exchanged semantics, type/schema, unit/reference, range, timing, quality, provenance, security/privacy, version, missing/invalid values, and ownership through authoritative interface links. Narrative labels such as “data” or “approval” do not establish compatibility.

**Represent time.** Establish scenario clock, relative/absolute events, deadlines, dwell, frequency, load pattern, queueing, synchronization, and uncertainty. Avoid false precision. Critical paths need timing budgets and resource-aware models; storyboard spacing has no quantitative meaning.

**Represent resources.** Identify energy, capacity, bandwidth, storage, personnel, attention, facilities, consumables, spares, and authority. State availability and contention. A scenario can be logically coherent yet infeasible when two concurrent actors need the same operator or equipment.

**Represent assumptions and uncertainty.** Classify assumption source, owner, confidence, sensitivity, validation plan, monitoring trigger, and expiration. Distinguish aleatory variation, epistemic uncertainty, and ignorance where useful. If the outcome reverses under plausible assumption values, scenario conclusions are not robust.

**Parameterize responsibly.** Define allowed parameter domains and correlations for weather, users, loads, failures, configurations, and timing. One parameterized family can reduce duplication, but critical discrete semantics may require separate scenarios. “All users” is not a parameter range unless population characteristics and exclusions are explicit.

**Build a scenario portfolio.** Create coverage dimensions: stakeholder/actor, goal, lifecycle stage, operational mode, configuration/variant, environment, interface, performance boundary, human workload/accessibility, failure/hazard, threat, recovery, sustainment, and disposal. Select scenarios using risk, novelty, coupling, consequence, uncertainty, and decision value—not equal quotas.

**Use coverage matrices carefully.** Map each obligation/risk dimension to scenario versions and adequacy rationale. Separate covered, partially covered, planned, excluded, and unknown. A cell means a reviewed relationship, not evidence that the scenario passed. Report critical uncovered dimensions individually rather than average them away.

**Use combinatorial methods selectively.** Pairwise or covering arrays can sample interacting parameters, boundary-value analysis targets thresholds, and Monte Carlo explores distributions. Rare/high-consequence and causally coupled combinations need deliberate inclusion. Statistical sampling cannot compensate for a wrong model or excluded population.

**Synthesize across scenarios.** Identify recurring functions, interfaces, states, rules, and resources; consolidate them into architecture. Resolve contradictions and distinguish genuine mode variation from inconsistent assumptions. Scenarios are analysis inputs/views; governed requirements and models become durable definitions.

**Derive candidate requirements.** A scenario may reveal needs for timeout, degraded operation, acknowledgement, staffing, training, compatibility, logging, recovery, or disposal. Record candidate source scenario and rationale, then validate quality, necessity, feasibility, priority, and authority. Do not automatically turn every narrative step into a “shall.”

**Compare architecture alternatives.** Run the same controlled scenario portfolio against alternatives. Compare outcome, timing, resources, resilience, human burden, safety/security, operability, observability, and lifecycle cost. If an alternative requires different scenario assumptions, expose that rather than claiming direct equivalence.

**Design verification from scenarios.** Convert relevant paths into controlled test/analysis cases with exact configuration, initial state, stimuli, environment, timing, expected observations/oracle, uncertainty, negative cases, and acceptance authority. A scenario is broader than a test script; one path may require several evidence methods.

**Design validation with stakeholders.** Use representative tasks, actors, environments, goals, and measures. Observe workarounds, workload, accessibility, comprehension, trust, and unintended effects. Stakeholder participation must represent affected diversity and power, not only available project staff. Results remain bounded by sample/context.

**Use simulation and replay transparently.** Record model, data, seed, distributions, scenario version, configuration, execution engine, and deviations. Simulation supports what-if analysis; replay supports behavior on recorded inputs; synthetic data supports declared properties. None alone establishes future operational outcomes.

**Capture evidence and anomalies.** Link each execution/result, deviation, anomaly, waiver, and stakeholder observation. Preserve failed and inconclusive outcomes. Do not rewrite the scenario after a failure to make the result pass without controlled change and impact analysis.

**Maintain operational feedback.** Field incidents, telemetry, support records, and observed adaptations can create new scenarios or alter parameters. Protect privacy/security and recognize reporting bias. Update trace, architecture, tests, training, and procedures through change control.

**Review scenario quality.** Ask whether the scenario is credible, relevant, internally consistent, traceable, implementation-appropriate, observable, reproducible enough for purpose, and explicit about assumptions/uncertainty. Challenge who or what is absent, whose authority is assumed, and which outcome evidence could falsify the story.

The following checker detects selected missing fields in five scenario records. It does not assess credibility or behavioral completeness.

<!-- bijux-verify: {"id":"behavioral-scenario-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"scenarios_total=5\nwell_formed_declared=1\nmissing_initial_state=S-002\nmissing_trigger=S-003\nmissing_alternates=S-004\nmissing_outcome=S-005\nunresolved=S-002,S-003,S-004,S-005\nevidence=declared_fields_only\n","stderr":""}} -->
```python
scenarios = [
    {"id": "S-001", "actors": ["operator", "service"], "initial_state": "degraded-network",
     "trigger": "emergency request", "flow": ["validate", "route", "acknowledge"],
     "alternates": ["no route -> escalate"], "outcome": "disposition recorded"},
    {"id": "S-002", "actors": ["operator"], "initial_state": "",
     "trigger": "request", "flow": ["validate"], "alternates": ["reject"], "outcome": "known"},
    {"id": "S-003", "actors": ["service"], "initial_state": "idle",
     "trigger": "", "flow": ["process"], "alternates": ["timeout"], "outcome": "recorded"},
    {"id": "S-004", "actors": ["operator", "service"], "initial_state": "ready",
     "trigger": "request", "flow": ["process"], "alternates": [], "outcome": "completed"},
    {"id": "S-005", "actors": ["service"], "initial_state": "ready",
     "trigger": "request", "flow": ["process"], "alternates": ["failure"], "outcome": ""},
]
required = ("actors", "initial_state", "trigger", "flow", "alternates", "outcome")
valid = [item for item in scenarios if all(item[field] for field in required)]
print(f"scenarios_total={len(scenarios)}")
print(f"well_formed_declared={len(valid)}")
for field in ("initial_state", "trigger", "alternates", "outcome"):
    print(f"missing_{field}=" + ",".join(item["id"] for item in scenarios if not item[field]))
print("unresolved=" + ",".join(item["id"] for item in scenarios if item not in valid))
print("evidence=declared_fields_only")
```

Even S-001 may be implausible, unsafe, unrepresentative, or semantically incomplete. The checker evaluates only nonempty declared fields.

## Definitions and Notation

Let $Events(\Gamma)=\{e_1,\ldots,e_n\}$ and $\prec_\Gamma$ be a partial order rather than forcing total sequence. Let $State(e_i^-)$ and $State(e_i^+)$ denote modeled state before/after an event, and let $Obs(e_i)$ be expected observable evidence with tolerance and authority.

A scenario consistency obligation is:

$$
\forall e_i\prec_\Gamma e_j:\ FeasibleOrder(e_i,e_j,S,E,R,T)
$$

with state $S$, environment $E$, resources $R$, and timing $T$. This does not prove real feasibility; it identifies the dimensions the scenario/model must justify.

For scenario parameter vector $\theta\in\Theta$, outcomes $O(\Gamma,\theta)$ can be explored. A sample $\Theta_s\subset\Theta$ supports conclusions only for its sampling design/model and cannot establish behavior outside $\Theta_s$ without a justified generalization or bound.

## Mechanisms, Invariants, or Proof Structure

Use a scenario assurance loop:

1. **Frame:** state decision purpose, source, boundary, actors, lifecycle, configuration, initial state/mode, environment, trigger, and outcomes.
2. **Thread behavior:** write nominal interactions at stable abstraction, then add alternatives, exceptions, degradation, hazards/threats, recovery, and termination.
3. **Enrich:** attach state, functions, interfaces/objects, timing, resources, authority, assumptions, uncertainty, and observables.
4. **Portfolio:** map coverage dimensions, prioritize risk/novelty/coupling/consequence, parameterize carefully, and expose gaps/exclusions.
5. **Synthesize:** reconcile recurring behavior into requirements/architecture and evaluate alternatives without creating a shadow specification.
6. **Evidence:** design verification/validation, simulation, replay, and monitoring with exact configurations/oracles and bounded claims.
7. **Govern:** review with affected stakeholders/domain authorities, baseline, trace, manage anomalies, and change after new evidence.

The result is a structured argument that important behavioral contexts have been examined. It is not proof that all situations, users, failures, attacks, or future adaptations have been imagined.

## Alternatives and Trade-Offs

**Narrative scenarios** are accessible and preserve context but can be ambiguous. **Structured tables** improve completeness and comparison but can feel mechanical. **Use case/activity/sequence/state models** add precise viewpoints but require semantic governance. Use coordinated forms rather than force every concern into one notation.

**Few deep reference scenarios** support rich end-to-end analysis. **Many shallow scenarios** broaden coverage but create maintenance and superficial review. Maintain a risk-based portfolio with reusable parameter families and dedicated critical cases.

**Implementation-neutral scenarios** preserve trade space. **Implementation-specific operational scenarios** are necessary after allocation for integration, deployment, and procedures. Label maturity and do not let candidate design leak backward as need.

**Deterministic reference cases** support comparison/reproducibility. **Stochastic ensembles** explore variability but depend on distributions/correlations. Use both when uncertainty matters, retaining rare high-consequence cases explicitly.

**Synthetic/simulated actors** scale exploration. **Human-in-the-loop and field observation** reveal adaptation, workload, and context but cost more and raise ethics/privacy issues. Match evidence to risk and intended claim.

## Failure Modes and Misconceptions

- **“A use case is one scenario.”** A use case typically admits multiple scenario paths.
- **“Nominal means likely.”** It means selected expected operation under stated conditions; frequency requires evidence.
- **“Reference means worst case.”** A reference case is not an envelope unless defined and justified as one.
- **“Every scenario step becomes a requirement.”** Steps are analysis evidence; normative obligations need necessity and authority.
- **“More scenarios mean more coverage.”** Coverage depends on mapped dimensions and semantic adequacy.
- **“Parameterization covers everyone.”** Only if domains, correlations, exclusions, and outcome semantics are justified.
- **“Simulation success validates operation.”** It validates model behavior under selected inputs.
- **“A passed test validates the scenario.”** One script/configuration does not establish the whole behavior or stakeholder outcome.
- **“Off-nominal means one failure at a time.”** Common cause, sequences, human response, and adversarial combinations can dominate.
- **“The story is implementation-free.”** Component/UI/protocol names may already freeze design; inspect each detail’s authority.

## Worked Examples

### Example 1

**Cold-chain delivery.** Initial conditions include packed payload, calibration, route, ambient envelope, battery estimate, and responsible courier. Nominal delivery, prolonged door opening, sensor disagreement, route delay, grid outage, and handoff are separate/branched threads. Outcome is payload evidence and disposition, not merely controller uptime. Field trials remain bounded by routes, loads, weather, and users.

### Example 2

**Flood warning.** Actors include observers, forecast service, authority, channels, responders, and public populations. Scenarios cover normal monitoring, uncertain threshold, sensor loss, conflicting data, warning issuance/correction, channel outage, and evacuation accessibility. Historical replay cannot establish unprecedented weather or representative comprehension.

### Example 3

**Aircraft turnaround.** Maintenance, fueling, loading, crew, dispatch, and weather activities partially order and share resources. A late defect changes readiness and human workload. The scenario exposes an unsafe assumption that schedule pressure cannot affect authority. Simulation supports modeled durations/resources, not organizational behavior by itself.

### Example 4

**Account recovery.** Credible threads cover legitimate loss, stale contact data, stolen device, attacker social engineering, accessibility, delayed notification, dispute, and revocation. `Code sent` differs from identity restored safely. Security tests cover modeled attacks/configurations, not universal identity assurance.

### Example 5

**Water contamination.** A batch passes online monitoring, later laboratory evidence conflicts, and distributed product must be traced, isolated, communicated, and remediated. The scenario derives recall and evidence-retention needs. Regulatory/domain authority determines acceptable response; a narrative cannot authorize release.

### Example 6

**Warehouse peak load.** Concurrent orders, partial inventory, robot congestion, worker intervention, substitution, and carrier cutoff expose shared resources and state races. Parameterized demand plus targeted worst interactions is superior to average load alone. Load tests remain bounded to modeled layouts/staffing.

### Example 7

**Satellite safe-mode recovery.** Initial fault knowledge is uncertain; energy, attitude, thermal, communication, ground availability, and authority interact. Alternate threads cover no contact and failed recovery. Simulation depends on modeled faults/orbit; operational readiness requires hardware, procedures, people, and configuration evidence.

### Example 8

**Clinical alert.** A high-risk result arrives during shift handoff with incomplete history and alert fatigue. Threads cover acknowledgement without action, escalation, wrong-patient risk, contradictory data, downtime, and patient-specific contraindication. Retrospective accuracy cannot validate clinical workflow or outcomes across populations.

### Example 9

**Regional service migration.** Scenarios combine canary deployment, schema dual-write, region loss, rollback, stale clients, and reconciliation. Individually safe changes interact. Chaos tests support injected failures and topology, not all common-cause cloud or organizational failures.

### Example 10

**Autonomous shuttle boarding.** Actors include diverse riders, attendant, remote operator, traffic system, door, and environment. Scenarios cover mobility devices, crowding, obstruction, sensor disagreement, emergency egress, network loss, and schedule pressure. Fixture and representative human evidence remain bounded; accessibility and safety authorities must review conclusions.

## Cross-Program Connections

- **Platform Engineering:** golden paths, incident drills, deployment/recovery, and developer journeys are scenario portfolios with real human and dependency contexts.
- **API and Service Engineering:** consumer-provider interactions, retries, partial failure, version negotiation, and sagas require alternate behavioral threads.
- **Data Engineering:** ingestion, late/corrected data, schema evolution, backfill, deletion, and lineage incidents unfold as stateful scenarios.
- **Object-Oriented Programming:** use cases inform collaborations, but object-level sequence diagrams should not replace system boundary/outcome analysis.
- **Functional Programming:** executable scenario generators and property-based tests sample behavior; their generators/oracles define claim limits.
- **Safety/security:** accident and attack scenarios identify hazardous paths and controls while assurance requires broader causal and evidence analysis.

## References

1. ISO, “ISO/IEC/IEEE 15288:2023 — Systems and software engineering — System life cycle processes,” second edition, published 2023-05. https://www.iso.org/standard/81702.html
2. NASA, “4.1 Stakeholder Expectations Definition,” especially ConOps and operational scenarios. https://www.nasa.gov/reference/4-1-stakeholder-expectations-definition/
3. NASA, “Appendix S: Concept of Operations Annotated Outline,” especially operational scenarios/use cases/design reference missions. https://www.nasa.gov/reference/appendix-s-concept-of-operations-annotated-outline/
4. NASA, “6.4 Technical Risk Management,” scenario definition and uncertainty context. https://www.nasa.gov/reference/6-4-technical-risk-management/
5. NASA, “5.2 Product Integration,” lifecycle hardware/software/human/environment interactions. https://www.nasa.gov/reference/5-2-product-integration/
6. NASA, “3.0 Systems Engineering Processes,” human error analysis and nominal/contingency/emergency task scenarios. https://www.nasa.gov/reference/3-0-systems-engineering-processes-vol-2/
7. SEBoK Editorial Board, “Operational Scenario (glossary),” *Guide to the Systems Engineering Body of Knowledge*, version 2.14. https://sebokwiki.org/wiki/Operational_Scenario_%28glossary%29
8. SEBoK Editorial Board, “Logical Architecture,” scenario of functions and behavioral architecture, version 2.14. https://sebokwiki.org/wiki/Logical_Architecture
9. Object Management Group, “SysML v1 Specification” behavior-diagram overview. https://www.omg.org/sysml/sysmlv1/

## Exercises

### Exercise 1

Rewrite “A commuter buys a ticket” as a controlled behavioral scenario with boundary, actors, initial state, trigger, nominal/alternate/off-nominal flows, timing/resources, outcomes, assumptions, and evidence limits.

### Exercise 2

Design a scenario portfolio for a battery-backed vaccine refrigerator. Create coverage dimensions and select a small but defensible set without claiming exhaustive combinations.

### Exercise 3

A simulated evacuation succeeds in 7:40 against an 8-minute objective for 1,000 synthetic occupants. Identify the missing evidence needed before making an operational or safety claim.

### Exercise 4

Convert a regional-service failure scenario into verification and validation work. Distinguish model checks, injected-failure tests, operator exercises, and field monitoring.

### Exercise 5

Construct an adversarial clinical scenario in which a decision-support alert is technically delivered but the stakeholder outcome fails. Produce a bounded assurance response.

## Answers to the Exercises

### Answer 1

Scope a station ticketing service including commuter interaction and external payment/entitlement services, not transport operation. Actors include commuter with declared accessibility/language/payment context, kiosk/app role, payment provider, fare authority, support, and network. Initial state records fare table/version, device/session, connectivity, clock, accessibility configuration, payment status, and no existing entitlement. Trigger is commuter request for a named journey.

Nominal flow: present applicable journeys/fares; receive accessible selection; show total/terms; obtain confirmation; authorize payment; issue cryptographically/verifiably bound entitlement; present/retain receipt; end session and protect data. Alternatives include another fare/payment/interface and assisted purchase. Off-nominal paths include stale fare, duplicate submission, uncertain payment, network loss, timeout, printer failure, accessibility barrier, cancellation, refund/dispute, and wrong entitlement. Outcomes distinguish payment authorization, entitlement issued/usable, receipt, and privacy/session closure. Evidence combines interface, timing, payment, accessibility/usability, fault, security, and representative validation bounded by configurations, users, stations, providers, and applicable authority.

### Answer 2

Dimensions include lifecycle (transport/install/operation/maintenance/update/disposal), power (grid/battery/transition/exhaustion), thermal load/ambient, door behavior, payload/packing, sensor health/disagreement, controller/actuator failure, connectivity, alarm recipients, operator handoff/error, configuration/version, recovery, and high-consequence exposure duration. Select reference cases: nominal hottest credible operating day; prolonged door-open during loading; grid loss with high thermal load; sensor disagreement during outage; cooling degradation with delayed responder; battery near end-of-life; maintenance/calibration misconfiguration; update/restart with retained state; alarm-channel failure/handoff; and recovery/disposition after temperature excursion.

Parameterize within justified ranges but keep sensor disagreement plus power loss as a dedicated interacting case. Map every requirement, hazard, actor, mode, interface, and lifecycle obligation to reviewed scenarios, exposing partial/unknown cells. Chamber, battery, fault, alarm, procedure, usability, field, and configuration evidence supports named conditions. The portfolio is defensible by risk and coverage rationale, not exhaustive; field monitoring and change control add scenarios after incidents/new environments.

### Answer 3

The 20-second nominal margin is not enough. Establish model geometry, exits, route/blockage behavior, movement/disability distributions, decision/pre-movement time, group behavior, staff actions, smoke/fire/toxic conditions, visibility, alarm comprehension, counterflow, congestion, door capacity/failure, and correlations. Verify the 8-minute objective’s start/end definitions and whether it applies to worst case, percentile, or all occupants. Report run distribution, random seeds, sensitivity, numerical/model validation, and uncertainty rather than one run.

Validate assumptions with measured facility data, drills or ethically appropriate human studies, accessibility and human-factors review, fire/hazard engineering, and independent code/regulatory authority. Analyze unavailable exits, delayed alarm, mobility aids, children, language, panic myths versus evidence, responder access, and tenability time—not egress time alone. The simulation result shows one encoded population/run met one timing comparison. It does not establish safe evacuation or representative real behavior.

### Answer 4

Formal/static work checks state-transition legality, retry/timeout bounds, invariants such as no dual writer, and trace/configuration consistency. Simulation evaluates topology, demand, correlated timing, data loss, and recovery assumptions across parameter sets. Injected-failure tests disable named region/network/storage/control-plane dependencies on production-like configurations and measure detection, routing, service level, data integrity, reconciliation, and rollback. Each has exact fault scope and oracle.

Operator exercises test alerts, authority, diagnosis, communication, manual controls, workload, handoff, and procedures, including misleading signals and unavailable experts. Staged deployment/canary evidence checks compatibility and rollback prerequisites. Field monitoring tracks outcomes, near misses, false failover, recovery time, data divergence, and user impact with privacy/security controls. Passing model/tests supports encoded/injected cases; operator exercises support sampled teams; monitoring supports observed deployments. None proves all regional/common-cause failures. Anomalies update scenarios, architecture, procedures, and evidence through change control.

### Answer 5

Scenario: a high-severity allergy interaction is correctly computed and delivered during shift handoff, but the alert is visually indistinguishable from frequent low-value alerts; the receiving clinician acknowledges to clear the queue without reading details; responsibility is ambiguous; the order proceeds; the patient is harmed. Alternate contributors include stale allergy provenance, accessibility, workload, language, downtime recovery, duplicate alerts, escalation failure, and automation bias. Technical delivery and acknowledgement are not the clinical outcome.

Trace the scenario to clinical need, hazard, workflow, data provenance, prioritization, presentation, acknowledgement semantics, responsibility, escalation, audit, and monitoring. Analyze alert tiers, independent hard stops where justified, context-sensitive suppression, handoff ownership, escalation, and safe downtime without assuming more alerts improve safety. Evidence includes data-quality tests, interface/timing checks, human-factors evaluation, representative simulation, prospective monitored clinical validation, adverse-event/near-miss review, security/privacy assessment, and independent clinical/safety/regulatory authority. Conclusions remain bounded by populations, sites, workflows, model/version, alert classes, and observation interval; delivered-message metrics cannot establish safe care.
