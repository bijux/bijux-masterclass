---
module_id: SYSENG-069
program: Systems Engineering
level: 2
module_number: 69
title: Resilience and Graceful Degradation
status: complete
last_verified: 2026-08-31
---

# Resilience and Graceful Degradation

## One-Page Review

### Governing question

When adverse conditions exceed prevention or nominal design assumptions, which essential outcomes must continue, how will performance degrade without violating safety or integrity constraints, how will the system recover and adapt, and what scenario-based evidence bounds those claims?

### Essential definitions

- **Resilience** is the engineered capability to anticipate, withstand, recover from, and adapt to adverse conditions, stresses, attacks, failures, or change while preserving prioritized mission/business outcomes within stated limits.
- **Robustness** is insensitivity or acceptable performance under a bounded set of variations without structural change. **Reliability** concerns continued required performance over time. **Fault tolerance** concerns specified faults. Each contributes to resilience but is not equivalent to it.
- **Graceful degradation** is controlled transition to explicitly defined lower service rather than abrupt, uncontrolled, misleading, or unsafe loss. A slower collapse is not graceful if critical outcomes or safety constraints fail.
- An **essential function/service** is prioritized for preservation because its loss produces unacceptable safety, mission, legal, or stakeholder consequences. Priority is scenario- and time-dependent.
- A **service floor** is the minimum acceptable performance, quality, integrity, and safety level for a service during a declared disturbance and interval.
- A **disturbance** is an event, condition, stress, attack, failure, demand surge, environmental change, or combination that challenges system performance. A **disturbance profile** includes magnitude, duration, onset, spatial/functional extent, correlation, and uncertainty.
- **Absorptive capacity** limits immediate loss; **adaptive capacity** reconfigures resources/behavior during change; **restorative capacity** recovers service; **transformative learning** changes the system when the old configuration or operating concept is inadequate.
- **Recovery time objective (RTO)** is a target duration for restoring a specified service level. **Recovery point objective (RPO)** bounds acceptable data/state loss. Neither establishes achieved recovery without scenario evidence.
- A **degraded mode** is a controlled configuration with named capabilities, limits, entry/exit criteria, authority, observability, duration, and verification. It is not an informal label for “something still works.”
- **Resilience debt** is accumulated fragility from deferred restoration, temporary workarounds, reduced margins, exhausted spares, staff fatigue, or unclosed anomalies after apparent service recovery.

### Central model, mechanism, or theorem

Let normalized stakeholder utility $u(t)\in[0,1]$ represent the weighted, constraint-qualified service delivered after a disturbance begins at $t_0$. Define a minimum acceptable floor $u_{min}(t)$ and an assessment horizon $T$. A simple lost-service measure is

\[
L=\int_{t_0}^{T}\max(0,1-u(t))\,dt,
\]

while floor violation is

\[
V=\int_{t_0}^{T}\mathbf{1}[u(t)<u_{min}(t)]\,dt.
\]

Two systems can have the same lost-service area but different safety consequences, minimum depth, recovery trajectory, or stakeholder distribution. Therefore report the trajectory and constraints—not one “resilience score.” A useful claim binds disturbance class, essential services, floor, degradation/recovery metrics, resource assumptions, and evidence.

### Critical invariants

- Resilience requirements name essential outcomes and stakeholders, not merely infrastructure uptime or component availability.
- Disturbance profiles state magnitude, duration, correlation, sequence, environment, demand, and uncertainty; single-component faults do not cover system shock.
- Safety, security, privacy, data integrity, legal, and physical constraints remain binding in degraded operation unless an authorized, explicit rule states otherwise.
- Service priorities, shedding order, quality indicators, error bounds, and user-visible state are defined before disruption.
- Entry, behavior, authority, duration, exit, rollback, and verification are specified for every credited degraded mode.
- Detection, sensemaking, decision, reconfiguration, containment, recovery, validation, and learning are distinct evidence-bearing stages.
- Redundancy and diversity claims include common causes, shared resources, coverage, load after failure, and depleted capacity.
- Recovery restores coherent end-to-end service and trustworthy state; restarting processes or clearing alarms is not sufficient.
- Human workload, staffing, communication, access, competence, fatigue, and organizational authority are part of the resilient system.
- Temporary workarounds, consumed inventory, bypassed controls, deferred maintenance, and unresolved anomalies remain visible as resilience debt.
- Exercises include correlated, prolonged, ambiguous, compound, and recovery-phase challenges with predeclared success/oracles.
- Operational evidence, near misses, changed threats, configuration, suppliers, environment, and demand update scenarios and decisions.

### Common failures

Common failures include calling ordinary high availability “resilience”; measuring only mean recovery time; maximizing aggregate throughput while critical users lose service; hiding integrity errors behind uptime; allowing a degraded mode to disable safety constraints; assuming backups share no cause; keeping automatic retry active during overload; shedding load without stakeholder priorities; failing over to stale or corrupt state; entering a safe mode that operators cannot sustain; restoring dashboards before end-to-end outcomes; practicing only announced daytime drills; crediting heroic staff as designed capacity; leaving temporary bypasses indefinitely; adapting online without bounded authority; and declaring recovery complete while spares, margins, staffing, or data remain depleted.

### Compact example

A synthetic 12-hour utility trajectory is sampled hourly: $1.00,0.82,0.65,0.55,0.62,0.70,0.78,0.86,0.92,0.96,0.99,1.00,1.00$. A trapezoidal calculation gives 2.15 normalized service-hours lost. Minimum utility is 0.55; a declared critical floor of 0.60 is violated for one sampled hour; utility first returns to at least 0.90 at hour 8 and to 1.00 at hour 11. This checks synthetic arithmetic only, not real resilience, continuous extrema, safety, data integrity, or stakeholder equity.

### Connections

Reliability and availability characterize failure/restoration distributions; redundancy and CCF analysis show how capacity survives; hazards and safety cases constrain degraded behavior. Verification, validation, operations, cybersecurity, platforms, APIs, data engineering, human factors, logistics, and governance provide the mechanisms and evidence for response, recovery, and adaptation.

## Governing Question

Can the configured socio-technical system preserve explicitly prioritized outcomes above required floors during credible adverse conditions, transition through observable and authorized degraded states without unsafe or corrupt behavior, restore verified service within bounded time/data loss, and learn without introducing uncontrolled change?

Resilience is conditional. “The platform is resilient” is not reviewable until disturbance, outcome, service floor, time, resources, dependencies, and evidence are stated. Resilience to a short regional network outage says little about a month-long supplier loss, a corrupt update, wildfire plus staffing disruption, or a deliberate attacker who adapts to recovery actions.

## Why This Matters

Prevention cannot cover every future combination of failure, attack, environmental stress, demand, human action, and dependency outage. Highly reliable systems can encounter conditions outside their estimated distributions; robust designs can exhaust their bounded margins. Resilience engineering addresses what happens next without using “unknown unknowns” to excuse vague requirements.

NIST SP 800-160 Volume 2 Revision 1 organizes cyber-resiliency around anticipating, withstanding, recovering from, and adapting to adverse conditions and connects goals, objectives, techniques, approaches, and design principles to lifecycle systems engineering. NASA work distinguishes reliability, robustness, and resilience and identifies simplification, margin, diversity, monitoring, reorganization, graceful degradation, human participation, and learning as useful—but context-dependent—heuristics. NASA's graceful-degradation research in air traffic control also emphasizes interacting technological, environmental, and human causes.

DHS resilient positioning/navigation/timing guidance treats prevention, response, and recovery as related layers and uses observable, outcome-based performance. FEMA's community-lifeline construct reminds engineers that service value is interdependent: power, communications, transportation, water, health, safety, and supply chains can determine one another's recovery. The scale differs, but the systems principle transfers: restoring a component is not the same as restoring a stakeholder outcome.

Resilience can conflict with safety or integrity. Continuing service at any cost may be worse than controlled shutdown. A resilient design therefore preserves critical constraints, communicates uncertainty and degraded capability, and makes authorized trade-offs visible.

## Prerequisites and Retrieval

Before accepting a resilience or graceful-degradation claim, retrieve:

1. mission/business objectives, critical services, stakeholders, consequence categories, safety/security/privacy/legal constraints, service priorities, and authorized trade-off decisions;
2. service-level indicators, quality/integrity/error limits, floors, RTO/RPO, maximum outage/degraded duration, recovery sequencing, and acceptance criteria;
3. system boundary, architecture, dependencies, external services, supply/logistics, facilities, geography, people, organizations, data/state, control authority, and neighboring lifelines;
4. disturbance catalog and profiles: faults, attacks, overload, environmental hazards, resource/supplier loss, human/organizational disruption, misinformation, compound/sequential events, duration, correlation, and uncertainty;
5. operational modes and state machines, mode annunciation, entry/exit/rollback, service shedding, prioritization, capacity reservation, safe state, manual operation, and emergency procedures;
6. monitoring, observability, health estimation, anomaly detection, diagnostic uncertainty, communications, decision support, escalation, incident command, and authority delegation;
7. redundancy/diversity, margins, isolation/segmentation, modularity, substitution, reconfiguration, rate limiting, backpressure, circuit breaking, queues, caches, replicas, backups, and alternate suppliers/sites;
8. recovery plans, dependency order, clean-room/rebuild capability, immutable/offline assets, data reconciliation, configuration restoration, validation, security re-establishment, and return-to-service authority;
9. experiments, fault injection, chaos tests, simulations, table-top exercises, drills, historical incidents, near misses, field telemetry, workload studies, recovery timings, and unplanned interventions;
10. current spares, inventory, capacity/margin, technical debt, temporary controls, waived requirements, staff readiness/fatigue, open anomalies, changed threats/demand, lessons, and revalidation triggers.

Use an outcome-thread challenge: select one essential stakeholder outcome and follow it through a compound disturbance, including detection uncertainty, initial absorption, every dependency, degraded decision, resource depletion, human work, recovery order, state reconciliation, verification, and renewed operation. Any hidden manual intervention or untracked external service is an assumption requiring ownership and evidence.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish resilience from reliability, availability, robustness, fault tolerance, survivability, continuity, and disaster recovery;
2. formulate disturbance- and outcome-bounded resilience requirements;
3. define essential services, stakeholder priorities, service floors, degraded modes, RTO, and RPO;
4. analyze performance-loss trajectories without collapsing them into a misleading score;
5. design anticipation, absorption, containment, reconfiguration, recovery, and adaptation mechanisms;
6. preserve safety, integrity, observability, and authority during graceful degradation;
7. integrate technical, human, organizational, supplier, and infrastructure dependencies;
8. construct compound/adversarial resilience tests with valid oracles and evidence limits;
9. manage recovery validation, resilience debt, learning, and configuration change;
10. communicate bounded claims and trade-offs without promising universal survival.

## Core Exposition

**Define outcomes, not assets.** Start with what stakeholders must still accomplish: safe evacuation, medication delivery, command authority, minimum environmental control, settlement integrity, or emergency communication. A server or pump matters through an outcome chain. Asset uptime can be high while the outcome fails at an interface.

**Prioritize explicitly.** Define essential, important, deferrable, and prohibited services for each scenario. Record stakeholder conflicts and decision authority. First-come-first-served or highest-revenue scheduling may violate safety or public obligations during scarcity.

**Specify floors and quality.** Availability alone treats wrong, stale, insecure, or dangerously delayed output as service. Bind capacity, latency, accuracy, freshness, consistency, safety, security, and duration. Define how users learn the current mode and limitations.

**Characterize disturbance profiles.** Include onset, magnitude, duration, geographic/functional extent, correlation, progression, observability, and recovery interference. A brief independent component fault and a prolonged regional event need different architecture, inventories, staffing, and evidence.

**Model the trajectory.** Mark pre-disturbance baseline, detection time, minimum service, degradation slope, floor violation, stabilization, partial restoration, full functional recovery, and replenishment. Keep multiple service dimensions when weights would hide critical harm. State sampling and continuous-time uncertainty.

**Design anticipation.** Use horizon scanning, threat/hazard intelligence, dependency monitoring, capacity forecasts, precursor detection, drift indicators, inventories, exercises, and decision triggers. Prediction can be wrong; anticipation also prepares options, authority, and reserves.

**Absorb with margin and containment.** Capacity reserve, physical margin, buffers, isolation, redundancy, diversity, passive protection, rate limits, and local autonomy can reduce immediate loss. Margins require governing units, conditions, aging, demand, and consumption visibility.

**Control overload.** Unbounded retry, synchronized reconnect, queue growth, and failover can amplify disturbance. Use admission control, backpressure, jitter, bounded queues, circuit breakers, load shedding, and recovery ramp limits. Verify that control traffic and emergency users retain resources.

**Engineer degraded modes.** Each mode has an owner, entry trigger, allowed/prohibited functions, resource budget, human roles, interface behavior, data guarantees, safety constraints, duration, monitoring, exit criteria, and recovery path. Avoid mode ambiguity between system and operator.

**Degrade function before integrity.** Prefer lower rate, resolution, geographic coverage, convenience, or nonessential features over silent corruption or unsafe approximation. If trustworthy service cannot be maintained, fail visibly and safely rather than return plausible wrong output.

**Use substitutability carefully.** Alternate components, sites, suppliers, communications, algorithms, or manual processes can preserve outcome. Validate interface semantics, capacity, competence, credentials, data, environmental fit, and common causes. A backup contract is not delivered capacity.

**Localize authority.** Central control optimizes globally but can be unreachable. Bounded local autonomy can preserve response; it needs policy, conflict resolution, synchronization, safe limits, revocation, and reconciliation. Split-brain availability without state integrity may cause irreversible harm.

**Design observability under distress.** Monitoring shares the disturbed system unless isolated. Preserve trustworthy time, provenance, health, mode, capacity, control status, dependency state, and uncertainty. Missing telemetry must not appear healthy. Provide out-of-band paths proportionate to consequence.

**Support human sensemaking.** Operators need prioritized cues, current modes, implications, available options, predictions with uncertainty, and coordination support. Avoid floods of secondary alarms. Plan staffing, handover, fatigue, protective equipment, remote/local authority, and degraded communications.

**Contain cyber compromise.** Segmentation, least privilege, diversity, dynamic reconfiguration, deception, non-persistence, protected backup, alternate communications, and clean rebuild can limit adversary freedom. Safety and security coordinate consequences while retaining different threat likelihood reasoning.

**Recover in dependency order.** Restore prerequisites before consumers: power, identity, time, network, data, control, application, and user workflow as applicable. Maintain a dependency graph and alternative paths. Starting everything simultaneously can cause overload or inconsistent state.

**Reconcile state.** Determine authoritative source, RPO, missing/duplicate/conflicting operations, ordering, schema/version compatibility, and integrity proof. Decide whether to replay, merge, compensate, rebuild, or discard. A process restart does not restore trustworthy business or physical state.

**Validate before declaring recovery.** Test end-to-end outcomes, constraints, configuration, data integrity, security posture, control effectiveness, monitoring, performance, and absence of induced failures. Separate service restoration from full replenishment of spares, capacity, staffing, and margin.

**Track resilience debt.** Temporary routing, disabled protection, emergency patches, deferred maintenance, exhausted consumables, borrowed staff, and manual records may sustain service. Record owners, risk, monitoring, expiry, removal, and verification. “Recovered” systems can be fragile to the next disturbance.

**Learn without normalizing deviance.** Compare observed trajectory and decisions with assumptions. Preserve surprises, workarounds, near misses, and successful adaptations. Convert learning into requirements, design, procedures, training, inventories, supplier agreements, scenarios, and evidence; do not praise heroics while leaving the design dependent on them.

**Govern adaptation.** Runtime learning or reconfiguration can improve response but may cross validated boundaries. Define allowable adaptation space, safety envelopes, authority, monitoring, rollback, audit, and post-event review. Novel behavior outside the assurance basis needs escalation.

**Test compound scenarios.** Combine dependency loss with demand surge, sensor ambiguity, staff shortage, malicious activity, bad weather, and incomplete recovery. Vary timing and duration. Include disturbance during recovery and a second event before replenishment.

**Use progressive exercises.** Begin with analysis and simulation, then component fault injection, integrated controlled tests, table-top coordination, production-like drills, and bounded operational experiments. Announced drills test plans; surprise and adversarial variants test sensemaking, while safety controls constrain experimentation.

**Define truthful oracles.** A service can appear responsive while returning stale data or violating physical constraints. Measure stakeholder outcome, state integrity, safety, prioritization, resource use, operator workload, and recovery validity. Retain aborted tests and unexpected interventions.

**Measure distributions and tails.** Report minimum service, time below floor, time to stable degraded service, RTO/RPO performance, lost-service area, recovery variance, staff effort, consumed reserves, and uncertainty by scenario. Means conceal rare long recoveries and unequal stakeholders.

**Avoid resilience score theater.** Composite indices can compare alternatives only when normalization, weights, constraints, uncertainty, and decision meaning are explicit. Never allow strong noncritical performance to compensate mathematically for a violated safety floor.

**Reassess lifecycle change.** New demand, climate/environment, suppliers, infrastructure, staff, software, threat behavior, obsolescence, and technical debt change the disturbance envelope and capacity. Update cases after incidents and before major configuration or operating changes.

The following synthetic fixture recomputes selected trajectory summaries with trapezoidal integration.

<!-- bijux-verify: {"id":"resilience-trajectory-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"samples=13\nhorizon_hours=12\nminimum_utility=0.55\nminimum_hour=3\nlost_service_hours=2.150\nsampled_hours_below_floor=1\nfirst_hour_at_or_above_0.90=8\nfirst_hour_fully_restored=11\nstatus=declared_resilience_trajectory_consistent\nevidence=synthetic_hourly_samples_only\n","stderr":""}} -->
```python
utility = [1.00, 0.82, 0.65, 0.55, 0.62, 0.70, 0.78,
           0.86, 0.92, 0.96, 0.99, 1.00, 1.00]
floor = 0.60
loss = sum(((1 - utility[i]) + (1 - utility[i + 1])) / 2
           for i in range(len(utility) - 1))
minimum = min(utility)
print(f"samples={len(utility)}")
print(f"horizon_hours={len(utility) - 1}")
print(f"minimum_utility={minimum:.2f}")
print(f"minimum_hour={utility.index(minimum)}")
print(f"lost_service_hours={loss:.3f}")
print(f"sampled_hours_below_floor={sum(value < floor for value in utility)}")
print(f"first_hour_at_or_above_0.90={next(i for i, value in enumerate(utility) if i > 0 and value >= 0.90)}")
print(f"first_hour_fully_restored={next(i for i, value in enumerate(utility) if i > 0 and value == 1.00)}")
print("status=declared_resilience_trajectory_consistent")
print("evidence=synthetic_hourly_samples_only")
```

Linear interpolation is implicit in the trapezoidal area, but the sampled floor count does not establish continuous time below the floor. The utility weights are undeclared synthetic aggregates. No safety, integrity, equity, probability, or operational resilience claim follows.

## Definitions and Notation

Let services $s\in S$ have performance vectors $y_s(t)$ and stakeholder-defined utility mappings $U_s(y_s,t,c)$ under context $c$. If aggregation is justified, $u(t)=\sum_s w_sU_s$ with declared weights $w_s$; hard constraints $g_j(y,t,c)\le0$ remain outside compensation.

For disturbance profile $d$, define response trajectory $u_d(t)$, minimum $u_d^{min}$, time below service floor $T_{below}$, stabilization time $T_s$, partial/full recovery times, and lost-service area $L_d$. RTO and RPO are requirements; observed $T_R$ and state loss $D_R$ are evidence.

A degraded mode $m$ is a controlled state tuple

\[
m=(services,limits,constraints,resources,authority,entry,exit,monitoring).
\]

Leaving any element implicit creates operational ambiguity. Let resilience debt $B$ be a structured inventory rather than one number: depleted resources, bypassed controls, temporary changes, unresolved anomalies, and human/organizational load have different consequences.

## Mechanisms, Invariants, or Proof Structure

A defensible resilience claim follows this chain:

1. **Outcome validity:** essential stakeholder outcomes, priorities, constraints, floors, and time horizons are explicit.
2. **Disturbance validity:** scenario profiles cover relevant faults, attacks, environment, demand, duration, correlation, ambiguity, and compounds with uncertainty.
3. **Architecture validity:** margins, containment, independence, substitution, observability, authority, and resource dependencies support the claimed response.
4. **Degradation validity:** state transitions, shedding, quality/integrity, safety, user communication, human work, and duration are controlled.
5. **Recovery validity:** dependency order, clean state, RPO, configuration, security, end-to-end validation, and replenishment are evidenced.
6. **Measurement validity:** metrics/oracles capture outcome trajectories, floors, tails, integrity, stakeholders, resources, and interventions without compensating away harm.
7. **Exercise validity:** representative and adversarial scenarios, timing, people, environments, success rules, aborts, surprises, and evidence limits are preserved.
8. **Adaptation validity:** learning changes requirements/design/operations within authority, safety envelopes, configuration control, and revalidation.
9. **Lifecycle validity:** field evidence, dependencies, demand, threats, debt, staffing, suppliers, and environment continually update the claim.

## Alternatives and Trade-Offs

**Absorb versus recover.** More margin reduces immediate loss but costs resources and can mask drift. Faster recovery can use lighter architecture but depends on detection, access, clean state, and supply. Balance by consequence and disturbance duration.

**Centralized versus local autonomy.** Central control optimizes global priorities; local autonomy survives disconnection. Local decisions can conflict or diverge. Use bounded authority and reconciliation.

**Hot redundancy versus rebuild.** Hot capacity gives fast failover but shares exposure and cost. Clean rebuild may defeat persistence but lengthens outage. Combine protected minimum service with trustworthy restoration when needed.

**Automatic versus human-directed degradation.** Automation meets tight timing; people handle novelty and ethical/mission trade-offs. Design clear envelopes, explanations, override, workload, and safe defaults.

**Uniform versus prioritized service.** Uniform degradation appears fair but can sacrifice essential outcomes. Priority protects consequence-critical services but needs legitimate governance and communication.

**Restore old state versus transform.** Restoration returns known capability quickly; transformation addresses revealed systemic weakness but introduces change risk. Stabilize safely, preserve evidence, then govern redesign.

## Failure Modes and Misconceptions

- **“Five nines means resilient.”** Availability summarizes service time; resilience explains bounded behavior through adverse trajectories and adaptation.
- **“Any continued output is graceful.”** Wrong, stale, unsafe, or misleading output can be worse than visible loss.
- **“RTO is recovery evidence.”** It is a target until representative end-to-end recovery demonstrates it.
- **“Backup equals recoverability.”** Restore tools, credentials, state integrity, compatibility, people, and dependency order matter.
- **“Safe mode is automatically sustainable.”** Resource, human, environmental, and duration limits must be verified.
- **“Automation removes human dependence.”** It changes human roles to supervision, exception handling, authorization, and recovery.
- **“Unknown threats cannot be engineered.”** Specific unknowns cannot be tested, but margins, diversity, observability, option capacity, learning, and broad stress classes can be designed.
- **“One resilience score compares designs.”** Aggregation can hide floors, stakeholders, integrity, tail risk, and uncertainty.
- **“Recovery ends when traffic returns.”** State, controls, security, spares, margins, staffing, and debt may remain impaired.
- **“Adaptation is always beneficial.”** Unbounded change can violate the assurance basis or amplify disturbance.
- **“A successful drill proves resilience.”** Scenario selection, notice, scripted response, exposure, and oracles bound evidence.
- **“Heroic response is capacity.”** Repeated heroics reveal design or organizational debt unless explicitly sustainable.

## Worked Examples

### Example 1

A hospital loses utility power. Generator start preserves outlets, but fuel endurance, cooling, oxygen, staffing, pharmacy refrigeration, elevators, and communications determine patient outcomes. The resilience requirement prioritizes life-support and emergency services, defines shedding, fuel resupply assumptions, manual contingencies, and repeated-start tests. Generator availability alone was an asset metric, not the outcome case.

### Example 2

An API cluster receives ten times normal demand. Automatic retries multiply traffic and exhaust connection pools. Admission control reserves emergency clients, rejects nonessential work visibly, adds retry jitter/backpressure, and sheds expensive features before core transactions. The degraded mode preserves correctness and priority with lower throughput; latency dashboards alone would miss rejected critical users.

### Example 3

A navigation receiver detects interference and switches to inertial estimation. Accuracy uncertainty grows with time. Graceful degradation includes an integrity bound, visible mode, restricted speed/route, cross-checks, and a maximum duration before controlled stop. Continuing to emit precise-looking positions without uncertainty would be graceful only cosmetically.

### Example 4

A replicated database survives a network partition by accepting writes in both regions. Availability remains high, but conflicting medication orders cannot be safely merged. The design chooses single-writer authority for safety-critical records, read-only local access, queued noncritical work, and explicit reconciliation. Integrity is a hard constraint, not a weighted service dimension.

### Example 5

A wildfire closes a data center and roads simultaneously. Remote failover succeeds, but the same event prevents staff and replacement hardware from reaching the alternate site. The scenario combines geographic, human, logistics, and communications dependencies; remote operation, spares, staffing rotations, and access agreements become evidence-bearing controls.

### Example 6

An autonomous vehicle loses two sensors in rain. The degraded controller reduces speed but increases following uncertainty and operator workload. Validation measures safe envelope, mode awareness, takeover time, road geometry, visibility, and fallback destination. “Reduced speed” is not automatically safe or sustainable.

### Example 7

Ransomware reaches the primary environment and online replicas. Offline immutable artifacts exist, but restore credentials and infrastructure definitions share the compromised identity service. Recovery design adds separately protected authority, clean-room tooling, provenance, staged rebuild, data validation, and business reconciliation. Backup success is tested as an end-to-end outcome.

### Example 8

A spacecraft loses a thermal-control loop. Load shedding preserves avionics and communication while pausing instruments, but battery and thermal margins shrink. The mode specifies priorities, sun attitude, duty cycle, telemetry, ground authority, time limit, and recovery. Operators see both service and remaining option capacity.

### Example 9

A drill restores customer traffic in 45 minutes, meeting RTO, but uses unrehearsed expert commands, loses six hours of records beyond RPO, and leaves protections disabled. The case records failure despite headline recovery time. Procedures, automation, validation, and protection restoration are corrected before another representative exercise.

### Example 10

After a supplier failure, a team qualifies an alternate part under emergency authority. Service resumes, but inspection inventory, test margin, documentation, spares, and maintainer training remain incomplete. These are tracked as resilience debt with expiry, controls, and closure evidence; the temporary configuration does not silently become normal.

## Cross-Program Connections

**Reliability and availability.** Failure and repair distributions inform expected trajectories; resilience includes correlated shock, bounded degraded operation, resources, adaptation, and outcome priorities beyond averages.

**Safety and assurance.** Hazard constraints determine when continuing is unacceptable. Safety cases justify degraded modes, recovery evidence, assumptions, debt, monitoring, and bounded authorization.

**Platform and API engineering.** Rate limits, queues, retries, circuit breakers, bulkheads, failover, rollout, rollback, identity, and observability implement resilience but can also amplify failure.

**Data engineering.** Replication, consistency, lineage, freshness, backup, replay, schema evolution, and reconciliation determine whether recovered service is trustworthy.

**Cybersecurity.** Anticipation, segmentation, non-persistence, diversity, protected recovery, deception, and adaptive response address capable adversaries. Safety consequences and security paths remain coordinated but distinct.

**Human and organizational systems.** Incident command, staffing, workload, communication, improvisation, supplier relationships, legitimacy of priorities, and learning are part of system behavior.

## References

1. NIST, [SP 800-160 Volume 2 Revision 1: Developing Cyber-Resilient Systems—official publication record](https://csrc.nist.gov/pubs/sp/800/160/v2/r1/final), 2021.
2. NIST, [SP 800-160 Volume 2 Revision 1: Developing Cyber-Resilient Systems](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-160v2r1.pdf), 2021.
3. NIST, [SP 800-160 Volume 1 Revision 1: Engineering Trustworthy Secure Systems](https://www.nist.gov/publications/engineering-trustworthy-secure-systems), 2022.
4. NASA, [Designing Graceful Degradation into Complex Systems](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20190025127.pdf), 2018.
5. NASA, [Reliability, Robustness, and Resilience](https://ntrs.nasa.gov/api/citations/20210019589/downloads/ICES-2021-140.pdf), 2021.
6. NASA, [NASA-HDBK-1002 Draft 2: Fault Management Handbook](https://www.nasa.gov/wp-content/uploads/2015/04/636372main_NASA-HDBK-1002_Draft.pdf), 2012; cited explicitly as draft guidance.
7. NASA, [NASA Systems Engineering Handbook, NASA/SP-2016-6105 Rev. 2](https://science.nasa.gov/wp-content/uploads/2023/04/nasa_systems_engineering_handbook_0.pdf), 2016.
8. U.S. Department of Homeland Security, [Resilient PNT Conformance Framework](https://www.dhs.gov/sites/default/files/publications/2020_12_resilient_pnt_conformance_framework.pdf), 2020.
9. U.S. Department of Homeland Security, [Resilient PNT Reference Architecture](https://www.dhs.gov/sites/default/files/2022-06/22_0609_st_resilient_pnt_ra.pdf), 2022.
10. FEMA, [Community Lifelines](https://www.fema.gov/af/emergency-managers/practitioners/lifelines), accessed 2026-08-31.

## Exercises

### Exercise 1

Define resilience requirements for a regional emergency-dispatch service facing network loss, demand surge, and reduced staffing. Specify outcomes, floors, priorities, modes, RTO/RPO, constraints, resources, metrics, and evidence limits.

### Exercise 2

Given hourly utilities $1.0,0.7,0.5,0.6,0.8,0.9,1.0$ and floor 0.6, compute trapezoidal lost-service area, minimum/depth, sampled floor violations, and first full recovery. Critique the metric.

### Exercise 3

Design graceful degradation for a data pipeline whose results drive physical dosing. Address freshness, accuracy, backlog, priority, admission, observability, safe shutdown, state reconciliation, and human authority.

### Exercise 4

Construct a compound exercise for a cyber compromise during recovery from an environmental outage. Define injected events, protected functions, staffing, evidence/oracles, abort criteria, negative evidence, and bounded conclusions.

### Exercise 5

A service has nominal traffic restored but uses manual routing, borrowed staff, emergency credentials, unverified data reconciliation, depleted spares, and disabled monitoring. Build a resilience-debt closure and re-acceptance plan.

## Answers to the Exercises

### Answer 1

Essential outcomes are receiving distress requests, locating callers within declared uncertainty, prioritizing life threats, dispatching available units, and preserving an auditable record. Define a floor such as continuous intake for priority calls, bounded queue/wait, visible location confidence, authenticated dispatch, and no silent record loss. Shed analytics, recordings beyond legal minimum, and administrative reporting before intake/dispatch. Modes cover partial network, local autonomy, manual radio, and reduced staffing with entry/exit, authority, duration, and user notices.

RTO applies separately to intake, dispatch, and full records; RPO for safety-critical events may be zero or explicitly bounded through local durable queues. Constraints include access control, privacy, responder safety, and priority governance. Resources include alternate carriers/radio, local power, maps, staff rotation, mutual aid, paper/offline procedures, credentials, and reconciliation. Exercises combine carrier outage, surge, ambiguous location, and staff loss. Measure outcome tails, floor time, integrity, workload, interventions, and replenishment. Results support only the tested geography, demand, duration, configurations, and staffing.

### Answer 2

Trapezoidal losses across six intervals are $(0+0.3)/2=0.15$, $(0.3+0.5)/2=0.40$, $(0.5+0.4)/2=0.45$, $(0.4+0.2)/2=0.30$, $(0.2+0.1)/2=0.15$, and $(0.1+0)/2=0.05$, totaling 1.50 utility-hours. Minimum utility is 0.5 at hour 2, a depth of 0.5 below nominal and 0.1 below the floor. Exactly one sampled point is below 0.6 because equality is not below. Full recovery first occurs at hour 6.

The aggregate hides service dimensions, stakeholder weights, safety/integrity, continuous behavior between samples, recovery resource cost, and uncertainty. Linear interpolation is assumed for area. A brief deep unsafe loss could have the same area as a long mild reduction. Report trajectory, floors, constraints, tails, and disaggregated outcomes.

### Answer 3

Define dosing decisions as essential and safety/integrity constraints as noncompensable. Each result carries source, event time, processing time, version, quality/confidence, and maximum valid age. Admission prioritizes safety-critical patients; backpressure prevents hidden unbounded lag; noncritical analytics shed first. If freshness/accuracy bounds fail, the pipeline reports unavailable/degraded rather than plausible stale values, inhibits unsafe automatic dosing, and transfers authority through a validated clinical procedure.

Observability distinguishes input absence, backlog, compute failure, stale output, and downstream acknowledgment. Local safe limits and diverse checks bound dose. Recovery identifies authoritative state, duplicates, gaps, order, schema/model compatibility, and compensating actions before replay. Human displays show mode, age, uncertainty, and required action. Tests cover clock skew, burst, duplicate/reordered data, corrupted model/configuration, partial replay, network partition, alarm workload, and recovery. Passing synthetic loads does not prove clinical effectiveness or every patient condition.

### Answer 4

Scenario: wildfire removes the primary site and staff access; failover begins; an attacker uses previously stolen recovery credentials to corrupt infrastructure definitions and backup metadata. Protect minimum command, safety monitoring, identity, trustworthy time/logging, and communication. Inject ambiguous telemetry, delayed supplier response, one unavailable expert, network congestion, and a second compromise indicator during staged restoration.

Use representative on-call staffing and declared out-of-band authority. Oracles cover safe service floors, data/config provenance, privilege, containment, workload, decision logs, RTO/RPO, recovery order, and absence of lateral movement—not merely endpoint uptime. Abort if physical safety, irreversible production data, or experiment containment is threatened. Preserve missed detections, false hypotheses, unsafe commands, undocumented workarounds, and facilitator interventions as evidence. The exercise supports preparedness for this bounded profile; capable adversaries, longer duration, other staff, and untested dependencies remain limitations.

### Answer 5

Do not declare full recovery. Create owned debt records for manual routing capacity/error and duration; borrowed-staff competence/fatigue and return date; emergency-credential scope, monitoring, rotation, and revocation; reconciliation gaps and affected decisions; spare replenishment lead time and reduced redundancy; and monitoring blind spots. Link each to hazards, service floors, temporary authorization, stop criteria, and expiry.

Sequence closure by risk: restore trustworthy monitoring and privileged identity, validate/reconcile critical state, establish sustainable routing, replenish safety-critical spares, return staffing with safe handover, then remove temporary mechanisms. Independently verify end-to-end outcome, configuration, data integrity, security, performance, and controls. Monitor anomalies and second-event capacity throughout. The authorized role reviews residual risk and re-accepts the normal configuration only after closure evidence; unresolved items require explicit restricted operation, not silent normalization.
