---
module_id: SYSENG-040
program: Systems Engineering
level: 1
module_number: 40
title: Planning System Integration Around Interface Risk
status: complete
last_verified: 2026-08-31
---

# Planning System Integration Around Interface Risk

## One-Page Review

### Governing question

How should an integration strategy concentrate scarce articles, environments, people, schedule, and evidence on the interfaces whose uncertainty and consequences can still change the architecture, while preserving safe and reproducible progression to the complete system?

### Essential definitions

- **Interface risk** is uncertainty that interacting elements, people, environments, or organizations will fail to exchange required matter, energy, information, control, authority, or service with acceptable behavior and consequence.
- An **interface-risk statement** names a cause or uncertain condition, the interface/scenario, possible failure, and consequences—not merely “integration risk: high.”
- A **risk driver** is an attribute such as novelty, ambiguity, cross-domain conversion, tight timing, shared resource, common cause, supplier control, incompatible maturity, poor observability, irreversibility, or hazardous authority that raises concern.
- An **integration strategy** explains how increments, order, articles/doubles, environments, readiness gates, and evidence progressively address system and interface risk.
- An **integration plan** operationalizes the strategy into controlled steps, participants, configurations, locations, resources, procedures, schedules, verification links, anomaly handling, and decision points.
- A **risk-retirement objective** is a falsifiable claim and evidence threshold whose satisfaction reduces a named uncertainty or consequence; activity completion alone does not retire risk.
- A **risk-reduction experiment** is an analysis, model, inspection, prototype, contract test, simulation, bench, fault injection, human-in-the-loop, environmental, or operational exercise selected to inform a decision.
- **Test fidelity** is the degree to which an article, double, environment, load, timing, failure behavior, human context, and observation represent what matters to a claim.
- **Progressive integration** increases scope, realism, load, environment, authority, duration, and consequence in controlled increments.
- An **integration thread** traces one end-to-end outcome or hazard across functions, physical elements, interfaces, configurations, people, environments, and evidence.
- **Regression** re-establishes confidence in previously supported behavior after a change or new combination.
- **Residual interface risk** is uncertainty/consequence remaining after planned controls and evidence, owned and accepted at the appropriate authority.

### Central model, mechanism, or theorem

For interface-risk item (i), when defensible quantitative probability (p_i) and commensurate consequence measure (c_i) exist, a simplified exposure is:

\[
R_i=p_i c_i.
\]

For candidate evidence action (a), estimated reduction is:

\[
\Delta R_{i,a}=R_i^{before}-E[R_i^{after}\mid a].
\]

The ratio (\Delta R/cost) can inform—not decide—selection. Estimates may be sparse, dependent, multi-dimensional, or ethically non-compensatory. Safety, legal, security, or mission constraints may require work regardless of expected-value ranking.

For interface (j), scenario set (S_j), and evidence set (E_j), risk retirement requires more than declaration coverage:

\[
Retired(j)\Rightarrow
\forall s\in S_j^{critical}:Compatible(j,s)\land EvidenceSupports(E_j,j,s)
\land ResidualAccepted(j,s).
\]

A passed nominal test or complete interface list does not satisfy this implication for omitted modes, faults, environments, versions, humans, or common causes.

### Critical invariants

- The plan names system scope, architecture/configurations, lifecycle interval, integration objectives, authorities, assumptions, constraints, and evidence decisions.
- Every important internal/external interface has stable identity, endpoints/path, contract, owner(s), change status, scenarios, risk drivers, evidence, and residual-risk disposition.
- Risk statements separate cause/condition, interface event, failure, consequence, affected configuration, and evidence gap.
- Integration order respects hard dependencies and safe states while exposing high-consequence/high-uncertainty interactions before changes become unaffordable.
- Each increment has an exact starting/ending configuration, risk-retirement objective, articles/doubles, fidelity limits, environment, procedure, readiness, observation, criteria, anomaly, rollback, and evidence record.
- Cross-domain, shared-resource, external-system, supplier, human, organizational, degraded-mode, recovery, maintenance, and retirement interfaces are included.
- Risk scoring never lets many low-consequence items offset a mandatory safety/security/legal/mission constraint.
- Test doubles have controlled identity, validated fidelity for the claim, explicit omissions, and replacement/regression plans.
- Interface evidence covers both endpoint conformance and assembled/path behavior at appropriate planes, loads, environments, and faults.
- Configuration, interface, requirement, hazard, verification, risk, procedure, schedule, facility, and evidence records remain synchronized.
- Anomalies preserve state/evidence, trigger impact and regression analysis, and update the risk model rather than being counted only as test failures.
- Resources include facilities, long-lead articles, fixtures, simulators, instrumentation, data, networks, external systems, trained people, spares, consumables, and contingency.
- Progress is measured by evidence-supported risk reduction and usable integrated states, not by percent of planned events executed.
- Plan changes after design, delivery, anomaly, facility, supplier, or external-system changes are controlled and rationale is preserved.

### Common failures

Common failures include sequencing only by product hierarchy or delivery date; planning one final end-to-end event; ranking interfaces only by count or novelty; writing risks without causes and consequences; using arbitrary red/yellow/green arithmetic; treating a signed ICD as compatibility evidence; testing each endpoint but not the path; using ideal mocks that omit timing, load, state, and failure; deferring supplier/external/human interfaces; testing only nominal mode; omitting shared time, power, identity, data, environment, operator, and facility common causes; changing many things at once; claiming risk retired because a test occurred; consuming the only system article without rollback or fault isolation; underfunding data reduction and regression; letting schedule slips erase high-value tests; and failing to update risk after surprising success or failure.

### Compact example

A service controller depends on a supplier actuator through a gateway. The actuator arrives late, but the protocol, command authority, timing, and fault semantics are high risk. The plan first uses a validated emulator to test schemas, sequences, retries, stale commands, and bounded timing; a power/mass fixture tests physical support; supplier hardware later replaces the doubles for current transients, thermal behavior, backlash, limits, and real faults. Evidence is partitioned by fidelity, regression is planned, and hazardous motion waits for verified safe-state controls. Delivery delay changes the sequence but does not postpone every interface question.

### Connections

SYSENG-031–034 identify and contract interfaces. SYSENG-035–036 define the physical elements and child structure. SYSENG-037 supplies dependency/order logic, SYSENG-038 readiness gates, and SYSENG-039 configuration identity. This module integrates those into a risk-driven strategy. Later trade, risk, decision, verification, validation, supplier, specialty-engineering, operations, and lifecycle modules deepen the plan's governance and evidence.

## Governing Question

Which interactions can defeat the system, which evidence can most usefully change that uncertainty now, and how should integration increments be arranged so learning is early, safe, representative enough, reproducible, and convertible into controlled system evidence?

The purpose is not to produce the largest test matrix. It is to construct a credible route from independently realized elements to a system whose important interactions are understood and supported by bounded evidence. Planning combines architecture, interface management, risk, configuration, verification, facilities, suppliers, people, schedule, and operations.

## Why This Matters

Many system failures occur not because every element is individually poor, but because locally acceptable elements interact through mismatched assumptions, measurement planes, timing, resources, state, faults, authority, versions, environments, or organizations. Interfaces concentrate emergent behavior and ownership gaps. They are also where late discovery is particularly expensive: parts may be inaccessible, contracts fixed, certification evidence invalidated, and operational work already trained.

NASA's current Product Integration guidance treats integration as engineering subsystem/environment interactions throughout lifecycle, not merely final assembly. It calls for early planning, sequences/procedures, enabling products, facilities, simulators, recording devices, interface control, and capture of anomalies and rationale. NASA's Integration Plan outline connects strategy, every internal/external participant, support equipment, each step, verification activity, responsibilities, location, and schedule.

NASA Interface Management guidance requires controlling internal/external interfaces and evaluating them during integration. NASA Technical Risk Management guidance combines risk-informed decisions with continuous risk management. NASA Technical Planning and V&V-plan guidance connect integration to resources, workflows, external interfaces, and evidence. Together they support an integration plan that is driven by uncertainty and consequences while remaining executable.

Risk numbers can aid decisions only when their meaning and evidence are defensible. A probability estimated from relevant repeated operations differs from a subjective ordinal likelihood. Consequences across safety, mission, cost, schedule, privacy, environment, and reputation may not share a unit. The plan should expose assumptions, uncertainty, dependence, mandatory constraints, and sensitivity rather than manufacture precision.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. stakeholder outcomes, ConOps/scenarios, system boundary, environments, lifecycle, configurations, and decision/review milestones;
2. logical/physical architecture, subsystem decomposition, product structure, allocation, states/modes, end-to-end flows, and safe states;
3. interface register, contracts/ICDs, assumptions/guarantees, owners, external agreements, versions, changes, and discrepancy history;
4. hazards/threats, FMEA/FTA or other failure analysis, performance/resource budgets, common causes, human tasks, and operational recovery;
5. integration dependency/order, readiness criteria, configuration baselines, verification/validation matrices, evidence, anomalies, and residual risks;
6. suppliers, commercial/reused items, services, facilities, test articles/doubles, tooling, instrumentation, data, networks, people, logistics, and long-lead constraints;
7. risk statement, uncertainty, consequence, expected-value limits, test fidelity, experimental design, observability, regression, and evidence applicability;
8. schedule logic, resources, contingency, cost, change control, anomaly management, data reduction, and decision authority.

As a retrieval test, inspect “test all APIs in staging before production.” Ask which consumers/providers/gateways/versions/schemas, identity, quotas, state/data, concurrency, latency, retries, faults, regions, external dependencies, observability, production differences, rollback, and human incident actions apply. Ask which risk or requirement each test informs and what staging cannot represent. Environment names are not integration strategies.

## Learning Objectives

After completing this module, you should be able to:

1. formulate actionable interface-risk statements with cause, event, consequence, configuration, and evidence gap;
2. identify interface risk across physical, functional, data, control, energy, environmental, human, supplier, and organizational domains;
3. distinguish qualitative prioritization, expected exposure, uncertainty, constraints, and risk acceptance;
4. define falsifiable risk-retirement objectives and evidence thresholds;
5. design progressive integration increments around end-to-end threads and interface risk;
6. select and govern models, simulators, emulators, prototypes, real articles, and environments by fidelity and decision value;
7. integrate readiness, configuration, procedures, anomaly, rollback, regression, facilities, people, data, and schedule into the plan;
8. measure progress by supported claims and residual risk rather than event completion;
9. replan after changes and surprising evidence while preserving traceability and prior evidence limits;
10. critique big-bang, nominal-only, supplier-late, and score-driven integration strategies.

## Core Exposition

**Frame the integration decision space.** Declare system and integration level, lifecycle interval, target configurations, operating environments, objectives, review/decision dates, available articles, constraints, authorities, and evidence needed. Separate developmental learning, formal verification, validation, qualification, acceptance, interoperability, operational rehearsal, and deployment objectives.

**Build the interface universe.** Combine registered interfaces with architecture paths, shared resources, physical adjacency, common environments, people/procedures, suppliers, enabling systems, external organizations, and lifecycle transitions. Include unintended coupling: ground, heat, vibration, electromagnetic effects, shared libraries, identity, clocks, data sources, facilities, operators, and change processes.

**Write risk statements with mechanism.** Use a form: “Because [cause/uncertain condition], [interface/path] may [failure] during [configuration/scenario], leading to [technical/stakeholder consequences], with uncertainty in [evidence gap].” Avoid “API integration high risk” or “vendor may be late”; those do not identify what evidence or mitigation matters.

**Characterize risk drivers.** Inspect novelty, complexity, ambiguity, tight margins, cross-domain conversion, asynchronous state, rate/load, tolerance stack, long path, fan-in/fan-out, shared resource, common cause, hazardous energy/authority, security/privacy boundary, human handoff, supplier/external control, maturity mismatch, inaccessible mating, irreversible change, poor observability, and sparse evidence.

**Distinguish uncertainty from issue.** A risk concerns a possible future shortfall; an observed incompatibility is an issue/anomaly needing resolution, though it may create new risks. Keep both connected. Do not reduce a known failed interface's likelihood to `high` and continue as if nothing happened.

**Assess without false precision.** When relevant data and common units exist, quantify distributions, correlations, consequence, model uncertainty, and sensitivity. Otherwise use defined ordinal categories with rationale. Treat safety/legal/security constraints and single-point catastrophic failures through governing acceptance rules, not portfolio averaging.

**Map risk to decisions.** Ask which architecture, supplier, interface, budget, procedure, facility, or schedule decision changes with evidence; the latest date evidence remains actionable; and the consequence of waiting. A beautiful late demonstration has low decision value if the design can no longer change.

**Define a risk-retirement claim.** State the interface, configuration/modes, input/environment/failure envelope, observation plane, measure, threshold, article/double, method, sample/duration, analysis, uncertainty, and decision. “Run integration test” is an activity. “Under profile N4 at the consumer plane, 99.9th percentile command age remains below 180 ms during failover with no duplicate actuation” is a testable claim, subject to statistical design.

**Choose evidence by information value.** Consider analysis, interface review, executable contract checks, models, simulation, breadboard, mockup, supplier sample, software/hardware/human-in-the-loop, environmental test, fault injection, and operational pilot. Prefer the least costly safe evidence that can discriminate the decision, then increase fidelity for remaining uncertainties.

**Bound models and doubles.** Record represented interface plane, versions, values, timing, load, dynamics, state, failures, environment, human behavior, validation evidence, omissions, and retirement plan. A mock can retire client serialization risk but not provider availability; a structural mass dummy cannot retire dynamic coupling.

**Design progressive increments.** Increase one or a few dimensions deliberately: participant/interface count, physical realism, load/stress, environmental range, failure severity, duration, operational staffing, external connectivity, data sensitivity, or control authority. Preserve a known reference state and diagnostic observability. Avoid simultaneous jumps that make failures unsafe or uninterpretable.

**Use end-to-end threads.** Select mission, user, safety, security, maintenance, recovery, update, and retirement threads that cross child boundaries. Trace trigger, data/material/energy/control/authority, states, timing, shared resources, humans, external systems, success, failure, and evidence. Thread coverage complements bottom-up product assembly.

**Plan endpoint and path evidence.** Verify each provider/consumer at its declared plane, conversions and intermediaries, physical/media behavior, and assembled interaction. A producer and consumer can each meet their local specifications while gateway queuing, wiring loss, clock skew, unit conversion, human handoff, or environmental coupling violates the system contract.

**Target margins and boundaries.** Test nominal function, limits, just-inside/outside boundaries, tolerance combinations, startup/shutdown, transients, peak concurrent load, long duration, degraded/fault modes, recovery, mixed versions, and environmental extremes appropriate to the risk. Do not spend all evidence at the easy center of the envelope.

**Expose common cause.** Challenge nominal redundancy for shared power, clock, network, identity, software, data, location, cooling, operator, supplier, procedure, or maintenance. Include correlated failure and recovery. Pairwise tests may miss shared fan-in services.

**Integrate humans and organizations.** Plan representative staffing, roles, authority, workload, information, procedures, training, shift/handoff, communication, management escalation, supplier response, and external agreements. Exercise anomalies, not just rehearsed nominal steps. Organizational latency can be an interface property.

**Connect order and readiness.** Use SYSENG-037 hard dependencies and risk priority to select steps; use SYSENG-038 evidence gates to authorize exact execution. High-risk work should be early enough to inform decisions, but never bypass required safety, configuration, facility, or personnel readiness.

**Control configurations.** Use SYSENG-039 manifests for articles, builds, data, models, doubles, procedures, environments, instrumentation, and external states. Record which evidence belongs to which configuration. Plan regression when doubles are replaced or participants change.

**Define every integration step.** Record ID/purpose/risk; starting/ending configuration; items/interfaces; prerequisites/readiness; location/environment; double/fidelity; procedure; roles; hazards/controls; instrumentation/data; expected behavior; pass/hold/abort; anomaly/rollback; evidence/verification credit; residual risk; allowed successors; schedule/resources.

**Plan observability and data reduction.** Allocate test points, synchronized clocks, sensors/logs/traces, command/state/event correlation, calibration/uncertainty, storage, custody, analysis algorithms, personnel, turnaround, and report. Data not reduced before the next irreversible step cannot govern it.

**Plan anomaly learning.** Define stop/hold, preserve state, configuration capture, evidence custody, triage, ownership, reproduction, cause analysis, corrective action, regression, risk update, re-entry, and communication. A surprising pass can also change the model; investigate why expected stress did not appear.

**Plan regression strategically.** Maintain a mapping from changes/interfaces to previously supported claims. Define smoke, targeted, thread, safety/security, performance, and full regression sets by consequence and coupling. Automate stable checks, but preserve representative physical/human evidence where automation cannot substitute.

**Resource the enabling system.** Budget facilities, clean/secure space, utilities, fixtures, simulators, test equipment, instrumentation, data systems, licenses, networks, external windows, trained staff, safety/quality observers, spares, consumables, shipping/storage, calibration, maintenance, and contingency. Long-lead or single-use assets shape strategy.

**Integrate schedule with technical logic.** Link predecessor conditions, readiness, evidence reduction, decision dates, supplier/external availability, facility calendars, resource conflicts, rework/regression, and contingency. Protect high-information events from being deleted automatically after slips. A schedule critical path is not identical to technical risk priority.

**Measure progress honestly.** Track risk-retirement claims supported/limited, critical scenarios exercised, interfaces/configurations with representative evidence, residual risk trend, unresolved assumptions/anomalies, regression status, readiness, and usable integrated states. Event count or percent procedures run can rise while risk remains unchanged.

**Manage residual risk and evidence limitations.** State what remains untested/unmodeled, why, consequence, owner, controls/monitoring, downstream constraints, closure or operational response, and acceptance authority. Successful evidence reduces bounded uncertainty; it does not make risk zero.

**Replan continuously.** Update the plan after architecture/interface/configuration changes, supplier evidence, delivery movement, facility loss, readiness findings, anomalies, operational learning, or risk-model change. Preserve rationale and impact on prior evidence; do not drag dates without revisiting the strategy.

**State evidence limits.** Risk matrices, expected exposures, coverage counts, simulations, prototypes, and tests support scoped decisions. They do not prove interface completeness, independence, production quality, operational validity, or absence of unknown interactions.

The following checker finds selected governance gaps in six interface-risk records. It does not assess whether the risks or mitigations are correct.

<!-- bijux-verify: {"id":"interface-risk-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"risks_total=6\nwell_formed_declared=1\nmissing_contract=IR-002\nmissing_owner=IR-003\nmissing_scenarios=IR-004\nmissing_evidence=IR-005\nmissing_mitigation=IR-006\nunresolved=IR-002,IR-003,IR-004,IR-005,IR-006\nevidence=declared_fields_only\n","stderr":""}} -->
```python
risks = [
    {"id": "IR-001", "contract": "ICD-7D", "owner": "Interface Lead",
     "scenarios": ["startup", "failover"], "evidence": ["bench-18"], "mitigation": ["emulator", "fault test"]},
    {"id": "IR-002", "contract": "", "owner": "Power Lead",
     "scenarios": ["peak load"], "evidence": ["analysis-4"], "mitigation": ["current-limited test"]},
    {"id": "IR-003", "contract": "API-12", "owner": "",
     "scenarios": ["retry"], "evidence": ["contract-tests"], "mitigation": ["idempotency key"]},
    {"id": "IR-004", "contract": "HMI-3", "owner": "Operations Lead",
     "scenarios": [], "evidence": ["walkthrough-2"], "mitigation": ["role rehearsal"]},
    {"id": "IR-005", "contract": "TIME-2", "owner": "Timing Lead",
     "scenarios": ["source loss"], "evidence": [], "mitigation": ["holdover test"]},
    {"id": "IR-006", "contract": "MECH-9", "owner": "Structures Lead",
     "scenarios": ["transport", "installation"], "evidence": ["fit-check"], "mitigation": []},
]
fields = ("contract", "owner", "scenarios", "evidence", "mitigation")
valid = [risk for risk in risks if all(risk[field] for field in fields)]
print(f"risks_total={len(risks)}")
print(f"well_formed_declared={len(valid)}")
for field in fields:
    print(f"missing_{field}=" + ",".join(risk["id"] for risk in risks if not risk[field]))
print("unresolved=" + ",".join(risk["id"] for risk in risks if risk not in valid))
print("evidence=declared_fields_only")
```

`IR-001` may still omit the decisive failure, use an unrepresentative bench, or claim excessive retirement. Record completeness is only a first review.

## Definitions and Notation

Let interfaces be (I), scenarios (S), risk items (Q), evidence actions (A), configurations (K), consequences (C), and observations (E).

Risk relation:

\[
affects\subseteq Q\times I\times S\times K.
\]

Evidence support:

\[
supports\subseteq E\times Claim\times K\times S.
\]

For quantitative exposure when justified:

\[
R(q)=\sum_c P(c\mid q,k,s)\,L(c),
\]

where dependence, uncertainty, and incomparable consequence dimensions must be modeled or reported rather than hidden.

Interface-scenario declaration coverage:

\[
C_{decl}=
\frac{|\{(i,s):\exists e\ supports(e,claim(i,s),k,s)\}|}
{|\{(i,s):applicable(i,s,k)\}|}.
\]

This shows which declared cells have linked evidence, not evidence quality or interface completeness.

An integration step transition follows SYSENG-037, augmented with risk objective:

\[
T_a:(State^-,Q_{target})\rightarrow(State^+,E,Findings,Q_{residual}).
\]

The step has value when evidence changes a decision, control, or justified residual-risk assessment—not simply because (State^+) exists.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—risk discovery.** Traverse interface registers, architecture paths, scenarios/modes, hazards/threats, budgets, suppliers, common resources, people, environments, changes, anomalies, and lifecycle transitions. Use cross-domain reviewers and counterexample prompts.

**Mechanism 2—risk formulation and ownership.** Write causal statements, identify configurations and evidence gaps, assign technical and consequence owners, and distinguish risks from current issues/assumptions.

**Mechanism 3—decision-linked evidence design.** Define the decision, latest useful date, discriminating claim, method, fidelity, configuration, conditions, observations, thresholds, uncertainty, and limitations.

**Mechanism 4—increment synthesis.** Combine dependency-valid order with risk priority, safe/readiness constraints, available articles/doubles, diagnostic isolation, configuration control, and resource/schedule realities.

**Mechanism 5—execution and learning.** Gate readiness, execute controlled procedure, preserve data/configuration, evaluate criteria, investigate anomalies, update risk/architecture/interfaces, and map evidence to claims.

**Mechanism 6—regression and progression.** Reconfirm prior claims affected by each change, replace doubles progressively, increase representativeness, accept residual risk at authority, and proceed to system/external/operational states.

The assurance argument for a plan is:

1. important interface risks and scenarios are credibly identified;
2. selected steps can discriminate decisions before commitment;
3. hard dependencies, readiness, safety, configuration, and resources make steps executable;
4. observations/criteria support bounded claims and anomaly learning;
5. progression/regression reaches required integrated configurations;
6. residual risks and omitted evidence are explicit and accepted.

No finite plan proves unknown interactions absent.

## Alternatives and Trade-Offs

**Bottom-up integration** follows product hierarchy and local maturity. **Thread-first integration** exposes cross-boundary outcomes early. Combine them to preserve build logic and end-to-end learning.

**Risk-first scheduling** maximizes early learning. **Availability-first scheduling** uses delivered resources. Availability-first is defensible when it produces relevant evidence without crowding out decision-critical work.

**Real articles** provide realism but may be scarce, fragile, or late. **Doubles** enable early safe work but create fidelity risk. Stage replacement with explicit regression.

**Broad integrated events** expose emergence but have poor fault isolation. **Narrow experiments** discriminate mechanisms but may miss composition. Alternate focused and expanding increments.

**Formal verification** can cover large state spaces under a model. **Empirical integration** encounters physical/runtime/human reality. Each is bounded by assumptions; combine where consequence warrants.

**Quantitative risk models** support sensitivity and expected-value decisions when data/models exist. **Structured qualitative review** is more honest under sparse evidence. Never present ordinal multiplication as precise economics.

**Dedicated integration facilities** support repeatable regression. **Shared/temporary facilities** reduce fixed cost but add schedule/configuration uncertainty. Include lifecycle operations and update needs.

## Failure Modes and Misconceptions

**“All interfaces are in the ICD, so risk is controlled.”** Documents can be ambiguous, inconsistent, stale, locally conforming yet system-incompatible, or silent on faults and environment.

**“High risk means test first.”** First define a safe discriminating test and required prerequisites; some analysis or architecture change should precede exposure.

**“A passed test retires the risk.”** Only the supported claim for exact article/configuration/conditions is reduced. Fidelity gaps and other scenarios remain.

**“The risk score chooses the plan.”** Scores omit uncertainty, dependence, constraints, information value, timing, reversibility, and multiple consequence dimensions.

**“Mocks let us finish integration before hardware.”** They retire only represented behaviors and add replacement/regression obligations.

**“Nominal end-to-end success proves compatibility.”** Boundary, load, fault, recovery, environment, duration, and human behavior remain.

**“Each pair passed, so the system will pass.”** Shared resources, common cause, concurrency, fan-in, emergent qualities, and external context can fail in composition.

**“Test failures are schedule problems.”** They are evidence about product, contract, method, environment, or plan. Preserve state and update the model.

**“After final integration, risk is gone.”** Operations, updates, maintenance, suppliers, external changes, and retirement continue integration risk.

## Worked Examples

### Example 1

**Novel interface before final hardware.** A new optical link joins two mature subsystems. Risk drivers are alignment tolerance, contamination, thermal drift, protocol acquisition, and inaccessible final routing. Early work combines optical bench, representative connector samples, thermal model, acquisition emulator, and access mockup.

Claims/evidence are separated: bench supports loss/acquisition under stated alignment; mockup supports access; model supports bounded thermal sensitivity. Final installed thermal/vibration/routing and long-duration acquisition still require regression.

### Example 2

**Familiar protocol, unit mismatch.** A producer sends pressure in kPa as integer; consumer interprets Pa as floating point. Both use the same message schema field name and pass serialization tests.

Semantic contract tests at endpoints and gateway inject boundary values and verify units, scale, range, invalid values, timing, alarms, and operator display. Familiar transport lowered novelty but did not lower semantic consequence.

### Example 3

**Latency budget with bounded margin.** End-to-end requirement is 250 ms. Contributions are sensing 35, network 40, processing 85, actuation 30, with 40 ms jitter/uncertainty reserve:

\[
Margin=250-(35+40+85+30)-40=20\text{ ms}.
\]

The plan measures compatible start/end events and correlated tails under load/failover. Twenty milliseconds arithmetic margin does not prove a percentile or worst-case claim.

### Example 4

**Power transient exposes hidden integration load.** Capacity is 600 W with 100 W reserve. Children need 180, 220, and 90 W; conversion/cooling/control overhead is 30 W:

\[
Margin=600-100-(180+220+90)-30=-20\text{ W}.
\]

The plan tests staged activation/current limiting and captures source/consumer planes, inrush, voltage sag, timing, thermal response, and safe recovery. Local steady-state passes cannot close the system transient.

### Example 5

**Supplier sandbox fidelity.** A provider sandbox covers API schemas and authentication but has unlimited quotas, deterministic latency, no regional failover, synthetic idempotency, and weekly data reset.

Use it early for contract and client-state defects. Plan provider performance environment and controlled operational canary for quotas, tails, duplicate delivery, persistence, failover, observability, and support response. Record provider-controlled residual risk.

### Example 6

**Organizational interface dominates recovery.** Two technical systems interoperate, but incident recovery needs one organization to revoke credentials and another to restore service. Their escalation hours, evidence formats, authority, and clocks differ.

The plan includes joint tabletop, timed role rehearsal, unavailable-contact scenario, audit exchange, and after-hours authorization. Technical API success did not cover the human/organizational control loop.

### Example 7

**Shared time common cause.** Redundant controllers use separate compute/power but one time-distribution path. The plan tests source loss, corrupt/stepped time, certificate expiry, network partition, holdover, disagreement, alarm, operator response, and recovery at each consumer plane.

Evidence may force an independent source/path or revised safe-state logic. Pairwise controller tests would not reveal the dependency.

### Example 8

**Human handoff under load.** A command transfers from automated control to an operator during degradation. Risk lies in notice timing, state comprehension, authority, workload, procedure, and return-to-automation handshake.

Human-in-the-loop increments progress from walkthrough to simulator to representative workload and failure timing. Measures include detection, decision/action time, errors, workload, communication, and safe recovery. One trained expert demonstration is not population validation.

### Example 9

**Fault injection protects evidence.** A data pipeline claims exactly-once external effect during retry. The plan injects lost acknowledgments, delayed duplicates, process restart, network partition, clock skew, and partial downstream commit while correlating operation IDs and durable state.

The test distinguishes client retry, broker, consumer, database, and external side effect. Killing random processes without state observability would create activity but weak diagnosis.

### Example 10

**Replan after change.** A gateway supplier changes chipset, firmware, power, timing, certificates, management API, and support lifetime. Prior fit and nominal schema evidence may retain partial value; power/thermal, timing, identity, failure, configuration, tooling, spares, and operational evidence is affected.

The plan updates risk statements, configurations, dependencies, doubles, readiness, regression, schedule/resources, and residual-risk authority. It does not merely insert a replacement test date.

## Cross-Program Connections

**Platform engineering.** Platform integration risk clusters around control/data planes, identity, policy, network, storage, observability, multi-region failure, deployment, shared services, and on-call operations.

**API and service engineering.** Consumer-driven contracts, schema/version compatibility, quotas, idempotency, retries, timeouts, ordering, failure injection, sandboxes, canaries, and provider change are interface-risk evidence.

**Data engineering.** Schema, semantics, lineage, time, replay, backfill, duplicates, quality, retention, privacy, capacity, and downstream side effects require progressive integration and reconciliation.

**Object-oriented programming.** Unit/class contracts support local reasoning, while dependency injection, runtime wiring, concurrency, resources, deployment, state, and external systems determine integration risk.

**Functional programming.** Pure transformations aid contract and property tests; effect boundaries, streams, state stores, timing, retries, and operations concentrate interface risk.

**Risk and decision analysis.** Information value, uncertainty, consequence, sensitivity, alternatives, and acceptance determine which evidence matters when.

**Verification and validation.** Integration checks create configurations for formal evidence; verification/validation objectives shape fidelity, criteria, participants, and environments.

## References

1. NASA, *Systems Engineering Handbook, Section 5.2: Product Integration*, current web edition. <https://www.nasa.gov/reference/5-2-product-integration/>
2. NASA, *Systems Engineering Handbook, Appendix H: Integration Plan Outline*, current web edition. <https://www.nasa.gov/reference/appendix-h-integration-plan-outline/>
3. NASA, *Systems Engineering Handbook, Section 6.3: Interface Management*, current web edition. <https://www.nasa.gov/reference/6-3-interface-management/>
4. NASA, *Systems Engineering Handbook, Section 6.4: Technical Risk Management*, current web edition. <https://www.nasa.gov/reference/6-4-technical-risk-management/>
5. NASA, *Systems Engineering Handbook, Section 6.1: Technical Planning*, current web edition. <https://www.nasa.gov/reference/6-1-technical-planning/>
6. NASA, *Systems Engineering Handbook, Appendix I: Verification and Validation Plan Outline*, current web edition. <https://www.nasa.gov/reference/appendix-i-verification-and-validation-plan-outline/>
7. NASA, *NPR 7123.1B: NASA Systems Engineering Processes and Requirements*, Change 4. <https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL>
8. NASA, *NASA Risk Management Handbook*, NASA/SP-2011-3422. <https://ntrs.nasa.gov/citations/20120000033>
9. NIST, *SP 800-30 Revision 1: Guide for Conducting Risk Assessments*. <https://csrc.nist.gov/pubs/sp/800/30/r1/final>
10. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>

## Exercises

### Exercise 1

An interface register contains six risk records. Five name an owner, contract, critical scenarios, evidence gap, mitigation, and retirement criterion; the sixth says only `vendor interface—high`. Compute declaration coverage and explain how to disposition the sixth without inventing a score.

### Exercise 2

An end-to-end response requirement is 400 ms. Controlled reserve is 50 ms. Contributions are 80, 120, 95, and 70 ms. Compute margin. Design an integration experiment that can support a meaningful tail-latency claim rather than only the sum.

### Exercise 3

Risk A has a defensible probability 0.30 and consequence 100 cost units; an experiment costing 10 is expected to eliminate the exposure if successful. Risk B has probability 0.10 and consequence 300 cost units; an experiment costing 5 has the same simplifying assumption. Compute naive exposures and exposure-reduction-per-cost. Give at least six reasons this must not automatically select B.

### Exercise 4

Critique: “Integrate each subsystem when delivered, run its smoke test, then perform one full-system test in the operational environment. Any failure will be assigned to the subsystem that caused it.” Propose a risk-driven alternative.

### Exercise 5

Develop an interface-risk-driven integration plan for a hospital medication-delivery platform spanning pump hardware/control, disposables, drug library, patient/order/record data, network/time/identity, alarms, nurses, pharmacy, biomedical maintenance, facilities, suppliers, security/privacy, and clinical operations.

## Answers to the Exercises

### Answer 1

Declaration coverage is:

\[
C=5/6\approx0.8333=83.3\%.
\]

Do not call the register 83.3% risk-controlled. For the sixth, identify endpoints/path, exact supplier product/service/version, contract/interface plane, cause or uncertain condition, configuration/scenarios, possible failure, technical/stakeholder consequence, evidence gap, owner and consequence authority, current controls, candidate evidence/mitigation, decision/latest useful date, retirement threshold, residual-risk acceptance, and supplier/change constraints. It may become several risk items or a current issue. The five complete records also need substantive review; field completion does not prove risk discovery or control.

### Answer 2

\[
Margin=400-50-(80+120+95+70)=400-50-365=-15\text{ ms}.
\]

The declared allocation already fails. First reconcile measurement events/planes, simultaneity, overlap, overhead, and whether contributions add. The team must reduce demand, change architecture/capacity, or revise requirement/reserve only with authority/evidence.

An experiment pins exact endpoint/intermediary builds/configuration and instruments synchronized producer-trigger and consumer-visible completion events. Generate representative request/state/data mixes, concurrency, payloads, background load, retries, failures/failover, network conditions, warm/cold starts, resource contention, and duration. Predeclare percentile or worst-case claim, sample strategy, exclusions, uncertainty, outlier handling, clock-error bound, and acceptance. Capture per-segment traces plus end-to-end measurements to avoid assuming independent tails. Exercise boundary/degraded conditions and report anomalies. A sample percentile supports only the tested population/conditions; rare events and future load remain limitations.

### Answer 3

Naive exposures:

\[
R_A=0.30(100)=30,\qquad R_B=0.10(300)=30.
\]

If each experiment eliminated its exposure with certainty, naive reduction per cost is:

\[
30/10=3\quad\text{for A},\qquad30/5=6\quad\text{for B}.
\]

This arithmetic favors B, but automatic selection is invalid because: probabilities/consequences may have different evidence/uncertainty; `cost units` may omit safety, privacy, environment, mission, and schedule dimensions; the experiment may not eliminate exposure or may fail to discriminate; risks may be correlated/common-cause; evidence may arrive after different decision dates; A may be a mandatory precursor; B may be unsafe/unready to test; consequences may be non-compensatory; mitigations may affect other risks; resource/facility opportunities differ; and residual/tail consequences matter. Compare value of information, constraints, dependence, timing, reversibility, readiness, and authority with sensitivity analysis.

### Answer 4

The proposal confuses delivery with technical order; omits interface-risk discovery; defers cross-subsystem/external/human behavior; lacks doubles, representative progressive environments, configurations, readiness, criteria, observability, faults, data reduction, anomaly handling, regression, rollback, facilities/resources, and residual-risk authority. One full-system failure may have no unique subsystem cause: interface assumptions, shared resources, environment, configuration, timing, procedure, or common cause can dominate.

A better strategy builds the interface/risk universe and critical end-to-end threads; derives hard dependencies; prioritizes uncertain/high-consequence decisions; uses analyses, contract checks, benches, emulators, and prototypes early; validates fidelity; progressively replaces doubles and increases scope/load/environment/authority; instruments endpoints/paths/shared services; tests boundaries, faults, recovery, humans, and external organizations; gates exact configurations/readiness; preserves known-good increments; defines anomaly/re-entry and risk-based regression; and schedules facilities/people/data reduction/contingency. Each step has a falsifiable risk-retirement claim and bounded evidence. Final representative system evaluation remains necessary but is no longer the first discovery event.

### Answer 5

Start with clinical outcomes/hazards: right patient/drug/dose/rate/order, authorized change, safe fluid delivery, timely alarm/response, privacy/audit, downtime/recovery, cleaning/maintenance, and safe update. Build interface risks across medication/fluid path, sensing/actuation/control, power/battery, firmware/library, display/alarm, patient/order/record semantics, network/time/identity, nurse/pharmacy/biomedical roles, suppliers, facilities, and external clinical governance.

High-value increments include:

1. fluid/pump fixtures and embedded simulators for calibration, limits, occlusion/air/free-flow, battery/power, watchdog, restart, safe state, update/rollback, and data capture using safe fluids;
2. executable contracts and synthetic datasets for patient/order/drug/library identity, units, dose/rate rules, freshness, authorization, provenance, conflicting/stale versions, duplicate/replay, reconciliation, and privacy;
3. network/time/identity/record/order/alarm doubles with latency/loss/partition, clock faults, certificate/key expiry, denial, least privilege, audit, service restart, and external side effects;
4. progressive replacement with supplier/clinical test environments, exact versions/quotas/configurations, representative topology/load, and bounded canary authority;
5. human-in-the-loop setup/program/check/start/alarm/recovery/cleaning/maintenance/update scenarios with representative nurses, pharmacy, biomedical, IT/security, staffing, interruptions, workload, shift/handoff, room noise/light, consumables, communication, and emergency authority;
6. integrated safe-fluid nominal and off-nominal threads, independent clinical/safety/security observers, predeclared stop criteria, exact configuration/evidence, anomaly preservation, and rollback/de-integration;
7. only then, appropriately authorized clinical/operational validation under applicable institutional and regulatory controls.

For each risk, record cause/scenario/consequence, interface contract, owner and clinical consequence authority, evidence gap, double fidelity, configuration, threshold, mitigation, residual risk, and decision date. Plan facilities, fixtures, instrumentation/calibration/time correlation, synthetic-data custody, suppliers, trained people, spares/consumables, data reduction, regression, recovery, and schedule contingency. Preserve patient-disconnected safe state and prohibit uncontrolled production data/orders or patient authority in developmental increments.

Evidence from simulators, synthetic data, supplier sandboxes, and one representative team remains bounded. The plan cannot itself prove clinical safety, usability across populations, cybersecurity, production reliability, regulatory conformity, or correct patient outcomes; those require applicable independent review, formal verification/validation, and controlled operational evidence.
