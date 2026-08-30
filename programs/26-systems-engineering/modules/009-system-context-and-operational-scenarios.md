---
module_id: SYSENG-009
program: Systems Engineering
level: 1
module_number: 9
title: System Context and Operational Scenarios
status: complete
last_verified: 2026-08-30
---

# System Context and Operational Scenarios

## One-Page Review

### Governing question

Who and what surrounds the system of interest, and how do people, systems, resources, environments, authorities, and lifecycle activities interact over time to produce intended and unintended outcomes?

### Essential definitions

- **System context** is the setting and circumstances of influences on the system of interest, including external entities, environments, interfaces, stakeholders, authorities, resources, and lifecycle conditions.
- A **context model** represents the system boundary and relevant relationships to external entities for a stated concern, viewpoint, time, and lifecycle scope.
- A **context diagram** is one view of context; it is not the context itself and does not establish completeness.
- An **operational concept** expresses an organization's intent and assumptions about operations from user/operator perspectives.
- A **concept of operations (ConOps)** explains at a high level how an envisioned system and its operational ecosystem will achieve objectives across lifecycle conditions without prematurely fixing design.
- An **operational scenario** is a time-ordered description of interactions among the system, users, other systems, and environment where the sequence has end-use significance.
- An **actor** is a role or external entity participating in a scenario; one person or system can enact multiple roles.
- A **precondition** must hold before a scenario begins; a **trigger** initiates it; a **postcondition/end state** describes the resulting state and unresolved obligations.
- An **alternate path** is a legitimate variation; an **exception/failure path** addresses violated expectations; **recovery** restores, degrades, compensates, or transitions safely.
- A **mode** is a distinct configuration or behavioral condition; a **mode transition** changes allowed functions, interfaces, responsibilities, or constraints.
- A **mission thread** traces an outcome end to end across multiple systems, organizations, and interfaces.

### Central model, mechanism, or theorem

Represent scenario (s) as:

\[
s=\langle objective,actors,context,preconditions,trigger,modes,steps,
alternates,failures,recovery,end\ state,measures,observations,trace,evidence\rangle.
\]

Represent context relation (r) as:

\[
r=(source,target,exchange,direction,interface,authority,condition,
quality,timing,failure,evidence).
\]

A scenario set is adequate for a decision only when it covers relevant objectives, stakeholders, functions, modes, interfaces, environments, lifecycle stages, hazards/failures, human decisions, and recovery obligations at the required depth. Coverage matrices reveal omissions; they do not prove that the axes or scenarios are complete.

### Critical invariants

- Every context model names the system of interest, boundary, concern, viewpoint, configuration, horizon, and lifecycle scope.
- External entities include people, organizations, natural conditions, authorities, suppliers, enabling systems, adversaries, and affected non-users where relevant.
- Every crossing states content/quantity, direction, semantics, timing, quality, authority, and failure behavior.
- Scenarios remain outcome- and interaction-focused until design choices are justified.
- Nominal success never substitutes for degraded, failure, misuse, emergency, maintenance, update, migration, and retirement coverage.
- Human workload, decision rights, accessibility, training, handoff, and recovery are part of system behavior.
- End states include records, resources, hazards, custody, notifications, and obligations—not only a success message.
- Scenario steps use causal and temporal ordering and expose concurrency, delay, interruption, and branching.
- Requirements, architecture, hazards, interfaces, verification, and validation trace bidirectionally to scenarios.
- High-consequence operational claims require applicable independent domain and stakeholder authority.

### Common failures

Failures include drawing only direct software integrations; treating operators as an icon labeled “user”; omitting non-users affected by outputs; mixing current and future context without notation; writing happy-path UI scripts as operational scenarios; encoding a preferred design before needs are understood; skipping initialization, authentication, handoff, cancellation, retry, degraded mode, recovery, and shutdown; assuming a supplier's context boundary matches yours; treating a coverage matrix as completeness proof; validating in a laboratory without representative workload; and ending a scenario before reconciliation, notification, or hazardous-state clearance.

### Compact example

A delivery-drone “deliver package” scenario is incomplete if it begins after launch and ends at drop-off. Operational context includes customer, bystanders, operator, airspace authority, weather, map and positioning services, communications, charging, maintenance, emergency responders, property, privacy, noise, wildlife, and disposal. Scenarios must cover mission planning, authorization, loading, launch, navigation, handoff, failed positioning, lost communications, severe weather, unsafe landing area, diversion, retrieval, incident evidence, maintenance, software update, and retirement. The broader context reveals requirements and hazards that a flight-control diagram cannot.

### Connections

Retrieve boundaries, stakeholders, emergence, feedback, openness, uncertainty, assumptions, constraints, and dependencies from Modules 001–008. Continue to problem framing and stakeholder needs. Later requirements, behavior models, interfaces, integration, verification, validation, human factors, lifecycle, and systems-of-systems modules turn scenarios into governed engineering evidence.

## Governing Question

A system never operates in an abstract blank space. It is started, supplied, commanded, observed, maintained, opposed, repaired, governed, and retired by a larger operational system. Static requirements often hide this temporal reality. “The device shall transmit an alert” says little about who recognizes the condition, which mode permits transmission, what network and identity state exist, who receives it, how urgency is interpreted, what happens if acknowledgement is absent, or how the incident closes.

The governing question asks teams to combine two views. Context identifies relevant external relationships and authority. Scenarios animate those relationships through time, modes, decisions, failures, and outcomes. Together they expose missing stakeholders, interfaces, capabilities, constraints, evidence, and responsibilities before architecture hardens.

## Why This Matters

Many system failures occur between well-built components: at handoffs, mode transitions, shared resources, incompatible assumptions, ambiguous authority, abnormal conditions, or recovery. A component test can show that an alert packet is emitted. An operational scenario can reveal that the receiver is unauthenticated during a shift change, two teams assume the other responds, and the local operator cannot tell whether recovery succeeded.

ISO/IEC/IEEE 29148 defines an operational scenario as an imagined sequence including interaction with environment and users and notes its use for requirements, design, verification, and validation. NASA's handbook describes ConOps and scenarios as time-sequenced operational views spanning modes, interfaces, hazards, failures, mitigation, human/system allocation, support, and disposal. ISO/IEC/IEEE 42010 connects architecture descriptions to stakeholders, concerns, environment, and purpose-specific views.

Context and scenarios also prevent premature solutioning. A need may be “restore safe drinking-water service after contamination,” not “build a mobile dashboard.” An implementation-neutral scenario reveals sampling, authority, laboratories, utilities, field crews, communities, vulnerable users, public communication, logistics, records, remediation, and restoration evidence. Only then can candidate technical and organizational solutions be evaluated against the actual operation.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. a boundary is selected for a concern and can change by lifecycle viewpoint;
2. stakeholders include affected parties, not only direct users and sponsors;
3. interface semantics and failure behavior matter as much as connectivity;
4. feedback and delay change future actions and observed outcomes;
5. open systems depend on enabling systems and external authority;
6. assumptions and constraints must be explicit and time-bounded;
7. uncertainty and complexity require alternate scenarios and adaptive observation.

As a retrieval test, draw a context diagram for an elevator. If it shows only passenger and power, ask about building control, fire alarm, doors, shaft, structural load, maintenance, inspection authority, emergency service, accessibility, communications, environmental conditions, cybersecurity administration, supply chain, cleaning, evacuation, and retirement. Then animate a power loss with a passenger inside. Missing entities become missing steps, requirements, or responsibilities.

## Learning Objectives

After completing this module, you should be able to:

1. define system context, operational concept, ConOps, scenario, actor, mode, and mission thread;
2. construct purpose-specific context models with typed exchanges and authority;
3. distinguish context diagrams from architectures, data-flow diagrams, and organization charts;
4. write implementation-responsible but solution-neutral operational scenarios;
5. specify preconditions, triggers, temporal steps, branches, recovery, and end states;
6. cover nominal, degraded, exceptional, emergency, maintenance, update, and retirement conditions;
7. model human roles, workload, handoffs, accessibility, and decision rights;
8. build and challenge scenario coverage/traceability matrices;
9. derive candidate needs, requirements, interfaces, hazards, and validation evidence from scenarios;
10. state evidence limits and required authority for consequential operations.

## Core Exposition

**Name the system of interest.** A context model is meaningless without the entity whose environment it describes. “Payment system” might mean checkout application, merchant service, acquiring enterprise, or whole payment ecosystem. Mark the chosen boundary and related systems explicitly. Maintain separate product, operational, support, legal, security, ecological, and lifecycle views when one line cannot answer every concern.

**Name purpose and viewpoint.** Context for latency differs from context for privacy, maintenance, public safety, or retirement. Record model owner, stakeholders/concerns addressed, configuration, time horizon, and exclusions. A purpose statement makes absence reviewable instead of accidental.

**Inventory external entities by role.** Include beneficiaries, users, operators, administrators, maintainers, trainers, suppliers, owners, regulators, auditors, responders, adversaries, and affected non-users. Add external systems, utilities, facilities, materials, data, natural environment, markets, policies, and enabling systems. Roles are more durable than named individuals or vendors.

**Type each relationship.** A line labeled “uses” is insufficient. State request/response, command, observation, material, energy, money, identity, authority, responsibility, hazard, custody, or waste. Add direction, unit/semantics, cadence/latency, quality, capacity, authentication/consent, ownership, allowable modes, and failure behavior. Relate each crossing to requirements and evidence.

**Separate current, transition, and target context.** Legacy and future systems may coexist during migration. Use distinct models or explicit temporal notation. Record dual-write, reconciliation, identity, authority, rollback, data custody, and decommissioning. A target-only picture can make the transition infeasible; a current-only picture can preserve obsolete constraints.

**Use context diagrams as indexes.** A readable diagram should prompt deeper interface, stakeholder, scenario, hazard, and dependency artifacts. Do not overload one view until semantics disappear. Maintain a context relation table as the authoritative detail and check diagram/table consistency.

**Distinguish operational concept and ConOps.** Terminology varies across organizations and standards. Define local usage. Both should explain intended operation from stakeholder perspectives, including mission/objectives, context, lifecycle, users/operators, modes, timelines, support, assumptions, constraints, and representative nominal/off-nominal scenarios. Keep the document useful for decisions rather than ceremonial.

**Write scenarios from outcomes.** Begin with stakeholder/mission objective and initial context. Use roles and observable interactions, not screen names or class methods unless implementation is already governed. “Responder obtains verified incident location within two minutes while the caller cannot speak” preserves design space. “User clicks blue location button” prematurely selects an interface.

**Specify preconditions and trigger.** Preconditions include mode, state, authority, resources, environment, data, staffing, and external-system readiness. They are not free: trace them to earlier scenarios or operating controls. The trigger is an event or decision that begins the sequence. If preconditions fail, define prevention, alternate entry, or recovery.

**Order interaction causally.** Number steps when order matters. Record actor, action/exchange, system response, information available, time/resource constraint, and resulting state. Show concurrency, asynchronous events, deadlines, feedback, and interruptibility. Avoid a narrative so smooth that it hides queues, decision latency, or contention.

**Branch honestly.** Alternate paths deliver the objective in another valid way. Exceptions violate an expectation. Failure paths cover absent, delayed, incorrect, unauthorized, overloaded, contradictory, or malicious input and internal failure. Recovery can retry, compensate, degrade, substitute, isolate, roll back, hand off, or reach a safe state. Each branch needs an end condition and authority.

**Model modes and transitions.** Define entry/exit guards, responsible actor, allowed/prohibited functions, interfaces, data/state continuity, observability, and failure of transition. Initialization, commissioning, nominal, peak, degraded, emergency, maintenance, calibration, update, migration, training, shutdown, and retirement may differ. Many hazards occur because both sides disagree about current mode.

**Model human work.** State what each role perceives, decides, communicates, and controls; workload, training, accessibility, fatigue, stress, environment, and handoff; and what automation assumes. Include workarounds and recovery, not an idealized procedure. A scenario cannot establish human performance without representative evaluation.

**Close the end state.** Success includes more than immediate function. Record resource consumption, data/records, custody, unresolved work, notifications, billing, audit, privacy, hazards, environmental effects, maintenance need, and readiness for the next scenario. Failed operations also need stable, observable, authorized end states.

**Cover lifecycle.** Development, production, integration, test, deployment, training, operation, sustainment, incident response, upgrade, migration, decommissioning, and disposal involve different actors and enabling systems. Operational design that ignores key provisioning, calibration, spare parts, data export, credential revocation, or hazardous disposal is incomplete.

**Build scenario families.** Start with a nominal spine, then vary actor capability, load, environment, timing, resource, interface, mode, failure, misuse, and recovery. Use hazard analysis, dependency map, assumption triggers, historical anomalies, and stakeholder walkthroughs to generate branches. Avoid combinatorial enumeration by prioritizing consequence, uncertainty, coupling, novelty, and validation need.

**Trace scenarios bidirectionally.** A scenario step can motivate a need, requirement, interface, function, mode, hazard control, measure, observation, or test. Every critical requirement should appear in relevant scenarios or have rationale for non-scenario verification. When architecture changes, rerun affected scenarios; when a scenario changes, perform impact analysis.

**Check coverage without claiming completeness.** Create matrix rows for scenarios and columns for objectives, roles, functions, interfaces, modes, environments, lifecycle stages, hazards/failures, requirements, and validation settings. Empty cells may be justified or reveal gaps. The matrix cannot show an omitted column, stakeholder, or unknown condition; independent challenge and operational learning remain necessary.

The executable checker illustrates this bounded role. It finds a maintenance scenario with no precondition, a network-loss scenario with no recovery, and a fire scenario with no requirement trace. It does not know whether the scenario content, actors, axes, or requirements are correct.

<!-- bijux-verify: {"id":"scenario-coverage-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"scenarios_total=4\nnominal_scenarios=1\noff_nominal_scenarios=3\nactors_covered=4\nrequirements_covered=5\nmissing_preconditions=S-maintenance\nmissing_recovery=S-network-loss\nmissing_trace=S-fire\ncoverage_complete=false\nevidence=declared_scenarios_only\n","stderr":""}} -->
```python
scenarios = [
    {
        "id": "S-nominal",
        "kind": "nominal",
        "actors": ["user", "operator"],
        "preconditions": ["service-ready"],
        "recovery": ["not-needed"],
        "requirements": ["R-1", "R-2"],
    },
    {
        "id": "S-network-loss",
        "kind": "degraded",
        "actors": ["user", "operator"],
        "preconditions": ["active-session"],
        "recovery": [],
        "requirements": ["R-3", "R-4"],
    },
    {
        "id": "S-maintenance",
        "kind": "maintenance",
        "actors": ["maintainer", "operator"],
        "preconditions": [],
        "recovery": ["return-to-service"],
        "requirements": ["R-5"],
    },
    {
        "id": "S-fire",
        "kind": "emergency",
        "actors": ["operator", "responder"],
        "preconditions": ["alarm-confirmed"],
        "recovery": ["safe-state"],
        "requirements": [],
    },
]

missing_preconditions = sorted(s["id"] for s in scenarios if not s["preconditions"])
missing_recovery = sorted(s["id"] for s in scenarios if not s["recovery"])
missing_trace = sorted(s["id"] for s in scenarios if not s["requirements"])
actors = {actor for scenario in scenarios for actor in scenario["actors"]}
requirements = {req for scenario in scenarios for req in scenario["requirements"]}
nominal = sum(scenario["kind"] == "nominal" for scenario in scenarios)

print(f"scenarios_total={len(scenarios)}")
print(f"nominal_scenarios={nominal}")
print(f"off_nominal_scenarios={len(scenarios) - nominal}")
print(f"actors_covered={len(actors)}")
print(f"requirements_covered={len(requirements)}")
print(f"missing_preconditions={','.join(missing_preconditions) or 'none'}")
print(f"missing_recovery={','.join(missing_recovery) or 'none'}")
print(f"missing_trace={','.join(missing_trace) or 'none'}")
complete = not (missing_preconditions or missing_recovery or missing_trace)
print(f"coverage_complete={str(complete).lower()}")
print("evidence=declared_scenarios_only")
```

**Turn scenarios into validation evidence.** Define representative actors, data, loads, environments, interfaces, faults, timing, and success/stop criteria. Use simulation, rehearsal, emulation, field trials, and operational observation according to consequence. Verification of scripted steps is not validation of stakeholder outcome. Preserve deviations and workarounds as evidence, not noise.

**Govern scenario changes.** Baseline scenario versions with context, requirements, architecture, hazards, tests, and operating procedures. Record rationale and authority. When incidents reveal unmodeled paths, update the scenario family and affected artifacts. Do not rewrite history so that past evidence appears to cover the new operation.

## Definitions and Notation

Let system of interest (S) have environment (E), boundary (B), and context entities (X=E\setminus S) relevant to concern (c). A context relation is (r\in R\subseteq(S\times X)\cup(X\times S)\cup(X\times X)) when external-external interaction affects the system outcome.

For scenario (s), let states (x_0,\ldots,x_n), events/actions (e_1,\ldots,e_n), modes (m_i), and actors (a_i) satisfy:

\[
x_i=Transition(x_{i-1},e_i,m_i,a_i,environment_i).
\]

The notation does not assert determinism; transitions can branch or carry uncertainty. A trace is acceptable only if preconditions hold and the end state meets authorized outcome and safety/obligation predicates.

Let coverage matrix (M_{ij}=1) when scenario (s_i) substantively exercises coverage item (q_j), otherwise 0 or a justified not-applicable mark. A column with no coverage is a gap candidate:

\[
Gap(q_j)\iff \sum_i M_{ij}=0.
\]

Nonzero coverage establishes presence, not adequacy, realism, independence, or correctness.

## Mechanisms, Invariants, or Proof Structure

Use this context-and-scenario procedure:

1. **Frame purpose.** Name system of interest, decision, concern, stakeholders, lifecycle scope, configuration, and horizon.
2. **Elicit external entities.** Include roles, organizations, systems, resources, environments, authorities, adversaries, and affected non-users.
3. **Type relationships.** Record exchange, direction, semantics, timing, quality, authority, modes, failure, and evidence.
4. **Separate temporal contexts.** Model current, transition, target, and retirement states explicitly.
5. **Select outcome threads.** Prioritize stakeholder value, risk, uncertainty, coupling, novelty, and validation need.
6. **Write scenario spine.** Define objective, preconditions, trigger, modes, causal steps, measures, observations, and end state.
7. **Add branches.** Vary actors, load, environment, timing, resource, interface, failure, misuse, emergency, and recovery.
8. **Trace artifacts.** Link requirements, functions, interfaces, assumptions, hazards, architecture, tests, and evidence.
9. **Challenge coverage.** Use matrices, walkthroughs, independent perspectives, counterexamples, and historical anomalies.
10. **Validate and evolve.** Exercise representative operations, retain deviations, and govern scenario/context change.

Five invariants guide review.

**Purpose invariant.** Context membership and scenario detail remain justified by a named decision or concern.

**Interaction invariant.** Every material boundary crossing has semantics, authority, conditions, and failure behavior.

**Temporal invariant.** Preconditions, triggers, modes, sequence, branches, recovery, and end obligations remain explicit.

**Stakeholder invariant.** Direct actors, affected non-users, support roles, and governing authorities are not collapsed into a generic user.

**Evidence invariant.** Scenario documents and automated coverage checks never claim representative operational validation by themselves.

## Alternatives and Trade-Offs

**One comprehensive context view versus multiple focused views.** One picture aids orientation but becomes unreadable and conflates concerns. Focused views preserve semantics but require consistency management. Use an overview plus governed relation tables/views.

**Narrative versus formal behavioral model.** Narrative is accessible to diverse stakeholders and captures lived context. State machines, sequence models, and executable simulations improve precision. Maintain semantic links and validate both with stakeholders.

**Broad scenario family versus prioritized threads.** Breadth finds gaps but grows combinatorially. Prioritization controls effort but can miss rare interactions. Use risk, uncertainty, novelty, coupling, and lifecycle coverage, then retain an explicit coverage debt.

**Solution-neutral versus design-specific scenarios.** Neutral scenarios protect problem understanding and alternatives. Design-specific scenarios support verification and operations. Keep both, label level, and trace design realization back to operational intent.

**Synthetic environment versus field realism.** Simulation and emulation are safe, repeatable, and fault-friendly. Field use reveals real interaction but introduces consequence and confounding. Progress through evidence stages with guardrails.

**Role abstraction versus named organization.** Roles survive reorganizations and clarify responsibility. Named entities capture actual contracts and authority. Model role first, then allocation/configuration.

**Happy-path clarity versus branch detail.** A simple spine communicates intent. Too little branching hides resilience needs; too much obscures the primary outcome. Separate linked scenario variants.

**Static baseline versus living operational model.** Baselines support traceability and acceptance. Operation changes context. Version changes, retain history, and trigger revalidation rather than editing silently.

## Failure Modes and Misconceptions

1. **The context diagram is the context.** It is a purpose-specific representation with omissions.
2. **External means irrelevant or uncontrolled.** External entities can dominate outcome and still require internal ownership.
3. **Users are the only stakeholders.** Maintainers, responders, non-users, regulators, suppliers, and communities may be affected.
4. **A user story is an operational scenario.** It can omit ecosystem, modes, failures, resources, and end obligations.
5. **A use case is a test case.** Operational intent, requirements, test procedure, and evidence are related but distinct.
6. **Nominal coverage establishes readiness.** Degraded, emergency, maintenance, transition, and retirement often drive architecture.
7. **More scenarios guarantee completeness.** Repeated happy paths can leave the same blind spots.
8. **A matrix proves adequate coverage.** It checks declared axes only.
9. **People follow the procedure deterministically.** Workload, perception, adaptation, incentives, and accessibility matter.
10. **Recovery ends when service restarts.** Reconciliation, notification, evidence, hazard clearance, and learning remain.
11. **Current context equals target context.** Migration and coexistence create unique interfaces and risks.
12. **Scenario success proves real-world value.** Representativeness and stakeholder outcome require validation evidence.

## Worked Examples

### Example 1

**Question:** What belongs in the context of a city water-contamination response?

**Assumptions:** The system of interest is the coordinated detection-to-restoration capability, not merely a laboratory or dashboard.

**Reasoning:** Include utilities, sensors, laboratories, field crews, public health, municipal authority, hospitals, schools, residents, vulnerable populations, media, suppliers, neighboring networks, weather/watershed, power/communications, regulators, and emergency logistics. Type sample custody, measurement, alert, authority, isolation command, bottled-water supply, public guidance, remediation, and evidence flows. Animate detection uncertainty, conflicting samples, network isolation, notification/accessibility, supply distribution, retesting, and authorized restoration.

**Evidence limit:** A context workshop cannot establish epidemiology, analytical validity, legal authority, equity, or operational readiness. Domain review and exercises are required.

**Conclusion:** Outcome-centered scope reveals socio-technical actors and obligations hidden by an application boundary.

### Example 2

**Question:** Why separate current, migration, and target context for a record system?

**Assumptions:** Legacy and target systems coexist while users and downstream partners migrate in cohorts.

**Reasoning:** Current context has one source of truth and interface set. Transition adds replication, translation, reconciliation, dual identity/access, routing, support, rollback, data-quality disputes, and change authority. Target context removes legacy interfaces but adds archive, retention, and decommissioning obligations. A target-only diagram cannot explain how writes remain consistent or who resolves divergence. Create three views and scenarios for cohort cutover, partial failure, rollback, late legacy record, and final custody transfer.

**Evidence limit:** Migration rehearsal covers its dataset, load, and partners. Production evidence needs representative scale, reconciliation, rollback, privacy, audit, and stakeholder acceptance.

**Conclusion:** Transition is its own operational system, not an arrow between architecture diagrams.

### Example 3

**Question:** How should an emergency elevator scenario be written?

**Assumptions:** Fire alarm occurs while passengers include a wheelchair user and a person who cannot hear the audible instruction; power and network may degrade.

**Reasoning:** State initial floor, direction, occupancy/load, mode, door state, alarm authority, power, communications, and accessibility resources. Trace alarm reception, validation, control transition, safe-floor selection, motion/door constraints, multimodal instruction, passenger action, responder control, loss-of-power branch, trapped-passenger communication, manual rescue, and return-to-service authority. Include conflicting sensor/alarm, smoke at target floor, and failed door. End state includes passenger accounting, hazard status, incident record, inspection, and mode reset.

**Evidence limit:** Script review does not establish timing, human comprehension, mechanical safety, fire strategy, accessibility, or regulatory compliance. Integrated drills and authorities are needed.

**Conclusion:** Modes, diverse actors, branches, and end obligations turn “recall elevator” into an operational scenario.

### Example 4

**Question:** Is “customer completes checkout” an adequate service scenario?

**Assumptions:** The checkout crosses inventory, price, promotion, tax, payment, fraud, identity, fulfillment, notification, and support boundaries.

**Reasoning:** Define cart/version, customer role/accessibility, market, currency, inventory reservation, deadlines, and consent. Trace totals and explanations, payment authorization, uncertain timeout, idempotent retry, inventory race, fraud challenge, cancellation, fulfillment commitment, confirmation, records, and customer recourse. Alternate paths include guest checkout and supported payment. Failure paths distinguish declined, unknown, duplicate, partial reservation, and downstream outage. End state reconciles money, inventory, order, notification, audit, and privacy.

**Evidence limit:** UI automation cannot validate provider semantics, financial reconciliation, accessibility, fraud fairness, legal duties, or fulfillment outcome.

**Conclusion:** Operational checkout is an end-to-end state transition, not a sequence of screen clicks.

### Example 5

**Question:** How can a context model expose a hidden shared dependency?

**Assumptions:** Primary and backup communication services appear as two external providers.

**Reasoning:** Expand each relationship to network carrier, DNS, identity, certificate authority, power, region, device radio/antenna, management plane, billing/account, operator, and software update. The two providers may share the same physical access, upstream carrier, credential, or device. Add an external-external edge where shared infrastructure affects both. Write a scenario for carrier loss during emergency, including detection, channel selection, user instruction, capacity, priority, acknowledgement, and recovery.

**Evidence limit:** Provider diversity by name is not independence. Architecture evidence, contracts, route/failure-domain analysis, and joint exercises bound the claim.

**Conclusion:** Context needs transitive and shared relationships whenever they change mission outcomes.

### Example 6

**Question:** What does a maintenance scenario add beyond an operational happy path?

**Assumptions:** A medical device requires calibration and software update while clinical service continues nearby.

**Reasoning:** Maintenance changes custody, access, enclosure, network, software, data, alarms, replacement capacity, cleanliness, and authority. Define removal-from-service, patient/work transfer, identity, tool/calibration provenance, backup/restore, update verification, fault branch, rollback, post-maintenance checks, records, release authority, and return to inventory. Include expired credentials, wrong configuration, unavailable replacement, contaminated equipment, and discovery of a safety issue affecting peers.

**Evidence limit:** Technician completion status does not establish clinical readiness. Calibration, configuration, cybersecurity, cleanliness, functional, human-workflow, and release evidence are distinct.

**Conclusion:** Maintenance is a mode with unique interfaces and hazards, not an implementation detail outside operation.

### Example 7

**Question:** How should a high-load public-service scenario include affected non-users?

**Assumptions:** An online benefits portal changes access to an essential service during a filing deadline.

**Reasoning:** Include applicants with varied language, disability, connectivity, identity documents, and digital skill; household members; caseworkers; call centers; advocates; identity/payment services; policy authority; fraud review; and people unable to access the portal. Trace normal and assisted application, save/resume, deadline, identity ambiguity, document failure, overload, duplicate submission, appeal, notification, and continuity through alternate channels. Measure completion distribution and harm from delay, not only server latency.

**Evidence limit:** Analytics exclude people who never connect or abandon before observation. Community/user research, accessibility, policy/legal, operational, and equity review are required.

**Conclusion:** Context includes those excluded or affected by the system, not only actors already visible in logs.

### Example 8

**Question:** What makes a scenario trace useful rather than ceremonial?

**Assumptions:** A lost-network scenario links requirements R-3 and R-4 to degraded behavior but has no explicit recovery.

**Reasoning:** Trace each step to requirement, interface, mode/state, assumption, hazard/control, function/allocation, observation, verification method, and validation setting. The missing recovery appears as an unclosed end state: buffered work, user status, authorization expiry, reconciliation, and return-to-normal behavior are undefined. Add recovery requirements and architecture, then tests for reorder, duplicate, conflict, capacity, notification, and audit. Bidirectional tracing also asks which requirements never appear in an operational thread.

**Evidence limit:** Links show intended relationships, not correctness or test success. Review semantics and representative execution.

**Conclusion:** Traceability is valuable when a scenario gap triggers concrete cross-artifact impact and closure.

### Example 9

**Question:** How should scenarios address concurrent incidents and operator workload?

**Assumptions:** A control center handles routine alarms well, but storm conditions create correlated faults, degraded sensors, calls, and shift handoff.

**Reasoning:** Model event arrival, queue/priority, shared displays, staffing, roles, communication, decision authority, fatigue, handoff, automation behavior, and field-resource contention. Run separate and combined threads: ambiguous sensor, escalating fault, public report, failed acknowledgement, and new emergency during mitigation. Observe missed cues, mode confusion, interruptions, workaround, and recovery debt. Provide triage, escalation, load shedding, additional staffing, and stable handoff artifacts.

**Evidence limit:** Average response time hides overload tails and cognitive failure. Representative simulation with trained personnel and human-factors observation is needed.

**Conclusion:** Concurrent scenarios reveal resource and coordination emergence that isolated use cases cannot.

### Example 10

**Question:** What must a retirement scenario cover for a cloud service?

**Assumptions:** The service stores customer data, issues credentials, uses suppliers, exposes APIs, and has legal/contractual retention duties.

**Reasoning:** Define decision/notice authority, customer communication/accessibility, export format and validation, migration support, write freeze, reconciliation, billing, records/holds, deletion and verification, backup/key/log treatment, credential/DNS/certificate revocation, supplier termination, monitoring, incident coverage, staff knowledge, asset disposition, and residual support. Branch for unreachable customer, disputed custody, failed export, active legal hold, security incident, and rollback before irreversible deletion. End only when obligations and residual risks have owners.

**Evidence limit:** Resource deletion messages do not establish customer receipt, complete erasure, legal compliance, or safe migration. No external legal, regulatory, academic, or practitioner review is claimed.

**Conclusion:** Retirement is an operational outcome with stakeholders and evidence, not a final infrastructure command.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) turns scenarios into domain behaviors, states, responsibilities, and invariants.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) uses scenarios to evaluate quality attributes and architectural decisions.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) contributes threat actors, trust boundaries, misuse, incident, and recovery scenarios.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) models concurrency, partial failure, time, recovery, and external coordination.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) specifies end-to-end contracts, failure semantics, and ecosystem journeys.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) models platform-consumer-team roles, workflows, constraints, and operational feedback.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, May 2023. Consulted 2026-08-30.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, November 2018. Consulted 2026-08-30.
3. ISO/IEC/IEEE. [ISO/IEC/IEEE 42010:2022 — Architecture description](https://www.iso.org/standard/74393.html), second edition, November 2022. Consulted 2026-08-30.
4. NASA. [*NASA Systems Engineering Handbook*, Rev. 2](https://www.nasa.gov/reference/systems-engineering-handbook/), NASA/SP-2016-6105 Rev2, 2016. Consulted 2026-08-30.
5. NASA. [Systems Engineering Handbook Appendix](https://www.nasa.gov/reference/system-engineering-handbook-appendix/), including the ConOps annotated outline. Consulted 2026-08-30.
6. SEBoK Editorial Board. [System Requirements](https://sebokwiki.org/wiki/System_Requirements), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-30.
7. SEBoK Editorial Board. [Stakeholder Needs Definition](https://sebokwiki.org/wiki/Stakeholder_Needs_Definition), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-30.
8. Ron Ross, Mark Winstead, and Michael McEvilley. [*Engineering Trustworthy Secure Systems*](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final), NIST SP 800-160 Vol. 1 Rev. 1, November 2022. Consulted 2026-08-30.

## Exercises

### Exercise 1

Create purpose-specific operational, security, support, and lifecycle context views for a public electric-vehicle charging station. Include typed relationships, authority, modes, failure behavior, and excluded concerns.

### Exercise 2

Write a scenario for “remote consultation during intermittent connectivity” with objective, roles, preconditions, trigger, modes, temporal steps, branches, recovery, end state, measures, observations, trace candidates, and evidence limits.

### Exercise 3

Build a scenario coverage matrix for a warehouse-robot capability across objectives, workers, maintainers, visitors, interfaces, modes, environments, lifecycle stages, hazards, requirements, and validation settings. Explain why the matrix does not prove completeness.

### Exercise 4

Diagnose and repair this scenario: “The customer taps Pay. The app calls `/charge`. The database saves success. A receipt appears.” Preserve operational intent and add missing actors, context, uncertainty, failure, recovery, and end obligations without committing prematurely to one design.

### Exercise 5

Design a high-consequence scenario family for automated railway-platform doors, including normal boarding, crowding, obstruction, sensor disagreement, train misalignment, power/network loss, fire/evacuation, manual control, maintenance, update, return to service, and retirement.

## Answers to the Exercises

### Answer 1

The operational view includes driver/passenger roles, vehicle, charging equipment, operator, grid/energy, payment/identity, tariff, parking/site, network, support, weather, and accessibility, with exchanges for authorization, power, status, money, consent, and assistance. Security adds credentials, certificates/time, administration, update, monitoring, physical access, adversary, privacy/data, and incident authority. Support adds maintainer, tools, spares, calibration, cleaning, towing, site safety, supplier, and outage communication. Lifecycle adds manufacture, installation/inspection, commissioning, migration, ownership transfer, decommissioning, recycling, data/key deletion, and environmental duties.

For every line record direction, semantics/unit, timing/capacity, identity/authority, allowed mode, failure, and evidence. Separate current/target/migration contexts. Explicit exclusions might include vehicle propulsion internals unless charge negotiation or safety depends on them. Context models remain concern-specific and must cross-reference shared entities and assumptions.

### Answer 2

Objective: clinician and patient complete a clinically adequate consultation or transition safely despite intermittent connectivity. Roles include patient, clinician, interpreter/caregiver where authorized, scheduling/support, emergency service, identity/consent, record/prescription systems, and network. Preconditions cover identity, consent/privacy, location/emergency information, device/accessibility, clinical suitability, records, contact alternatives, and current connectivity. Trigger is scheduled or urgent session start.

Trace connection and identity, shared understanding of limitations, clinical interaction, evidence/observation, a network-loss branch, bounded reconnect, alternate audio/text or reschedule, emergency escalation, documentation reconciliation, prescription/referral, notification, and closure. Handle partial audio/video, duplicate/conflicting records, lost consent context, interpreter loss, and inability to locate patient. Measures include clinical/communication adequacy, time, equity, safety escalation, and record completeness—not connection uptime alone. Simulation and workflow tests cannot establish clinical efficacy, privacy legality, or universal accessibility; applicable clinical, privacy, safety, accessibility, and regulatory review is required.

### Answer 3

Rows should include nominal pick/place, worker crossing, visitor entry, peak load, low battery, blocked route, dropped/damaged item, localization/sensor disagreement, network/control loss, emergency stop, fire/evacuation, manual recovery, cleaning, maintenance, software/map update, commissioning, return to service, and retirement. Columns mark objectives and affected roles; warehouse/order/identity/power/network interfaces; idle/navigating/carrying/degraded/emergency/maintenance modes; lighting/dust/noise/temperature/aisle conditions; lifecycle stages; collision, crush, fire, load, security, and ergonomic hazards; traced requirements; and analysis, simulation, lab, integrated, human-factors, and site validation.

A nonempty cell shows declared consideration, not adequate depth, realism, correctness, independence, or pass evidence. Missing stakeholders, axes, correlations, scenarios, or unknown conditions remain invisible. Challenge with workers/maintainers/safety/security, incident history, hazard/dependency analysis, counterexamples, and operational learning.

### Answer 4

Restate objective: an authorized customer and merchant reach one unambiguous, explainable purchase outcome with money, order, inventory, fulfillment, notification, records, privacy, and recourse reconciled. Define market/currency, cart/price/tax, customer role/accessibility, identity/consent, merchant, inventory, payment/fraud, fulfillment, network, and support. Trigger is customer authorization, not a UI gesture.

Trace quoted terms, authorization, uncertain payment result, inventory reservation, fraud/identity challenge, cancellation, retries/idempotency, fulfillment commitment, customer status, and reconciliation. Branch for decline, timeout/unknown, duplicate, price/inventory change, partial downstream failure, abandoned flow, refund, and dispute. Do not prescribe `/charge` or a database until architecture is selected. End states must distinguish success, failure with no transfer, pending/unknown, and compensated/recovered states, each observable and owned. Trace candidate needs, requirements, interfaces, hazards, measures, and validation evidence.

### Answer 5

Define roles and context: passengers with varied mobility/sensory/cognitive needs, staff, driver/control center, maintainers, responders, train control/position, platform/doors/sensors, power/network/time, alarms/signage, station environment, regulator, suppliers, and security administration. Scenarios cover aligned normal open/close/departure; crowd/peak pressure; person/object obstruction and repeated attempts; sensor or train-position disagreement; door/platform/train mismatch; power/network/control loss; fire/evacuation; manual isolation/release; rescue; maintenance/calibration/update; rollback; inspection/release; and decommissioning.

For each state preconditions, trigger, speed/position/mode, allowed motion, sensing uncertainty, human information/authority, interlocks, timing, degraded behavior, emergency priority, recovery, passenger accounting, records, hazard clearance, and return-to-service authority. Trace hazards and requirements to independent safety analysis, interface and timing verification, fault injection, environmental/integrated testing, accessibility/human-factors exercises, security assessment, maintenance validation, and operational readiness. No scenario document or local checker establishes acceptable safety, accessibility, regulatory compliance, emergency authority, or external review. Named railway safety, operations, accessibility/human-factors, engineering, cybersecurity, maintenance, regulatory, emergency, worker, and passenger authorities must review applicable claims.
