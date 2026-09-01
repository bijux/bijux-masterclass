---
module_id: SYSENG-096
program: Systems Engineering
level: 2
module_number: 96
title: Human Factors and Cognitive Work
status: complete
last_verified: 2026-09-01
---

# Human Factors and Cognitive Work

## One-Page Review

### Governing question

How should engineers design a software-intensive capability so that people and automation can jointly perceive, decide, coordinate, act, and recover under realistic goals, time pressure, uncertainty, workload, and organizational constraints?

### Essential definitions

- **Human factors** applies knowledge about human capabilities, limitations, variability, and interaction to the design and evaluation of systems, work, environments, and organizations.
- **Cognitive work** is the activity of finding meaning, maintaining context, forming and revising plans, managing attention, coordinating, resolving uncertainty, and adapting action—not merely processing information.
- **Work as imagined** is how designers, managers, procedures, or models expect work to occur; **work as done** is how people actually reconcile goals, resources, constraints, surprises, and local conditions.
- A **joint cognitive system** is a coupled human–technology arrangement whose effective cognitive functions are distributed across people, representations, automation, procedures, and environment.
- **Situation awareness** is a model of how relevant elements are perceived, comprehended, and projected; it is not a quantity stored entirely inside one operator or proven by display exposure.
- **Mental workload** is the relation between task demands, available human resources, strategies, state, and context; it is not interchangeable with task count or one physiological signal.
- A **mode** is a distinct configuration of behavior, authority, control law, interface, or operating rule that changes what actions mean or what feedback is available.
- **Automation surprise** occurs when automation behavior or mode differs materially from a person's current process model, especially when state, intent, or transitions are poorly visible.
- **Resilience** is the capacity to sustain or recover required performance under varying conditions through anticipation, monitoring, response, and learning.
- A **human-performance envelope** bounds the population, roles, staffing, training, tools, environment, scenarios, duration, workload, and evidence for a human-factors claim.

### Central model, mechanism, or theorem

Represent one cognitive-work situation as

$$
\mathcal{W}=\langle G,A,I,M,C,E,T\rangle,
$$

where $G$ is the set of goals and constraints, $A$ available actions and authority, $I$ information and feedback, $M$ the participants' revisable process models, $C$ coordination structure, $E$ environment and resources, and $T$ temporal demands. Performance emerges from their interaction. A nominally correct procedure or interface cannot establish acceptable work if authority, feedback, coordination, time, or recovery is missing.

For a bounded interval $h$, a simple attention-capacity screen may use

$$
\rho_h=\frac{D_h}{C_h},
$$

where $D_h$ is declared attention demand and $C_h$ declared capacity. If $\rho_h>1$, the assumptions are infeasible. If $\rho_h\leq1$, human adequacy is not proved: sequencing, interruption, expertise, fatigue, uncertainty, multi-channel interference, and consequence still require evidence.

### Critical invariants

- Treat people as adaptive system participants with goals, expertise, limits, and authority—not as failure-rate components or unbounded exception handlers.
- Analyze work as done in representative contexts, including nominal, degraded, emergency, maintenance, recovery, transition, and adversarial conditions.
- Allocate goals, information, decisions, actions, authority, and recovery across the joint system; do not allocate only nominal functions.
- Make system state, automation mode, intent, uncertainty, constraints, and action effects observable at the time and place of decision.
- Bound claims by representative populations, accessibility needs, roles, training, staffing, shift, environment, duration, configuration, and scenario.
- Design for attention limits, interruptions, time pressure, memory decay, fatigue, stress, skill degradation, and competing goals without reducing them to one score.
- Preserve direct control, veto, confirmation, graceful degradation, safe stop, and recovery where consequence requires them.
- Engineer team cognition: shared artifacts, communication, handoffs, cross-checks, escalation, authority, and common-ground repair.
- Validate with complementary qualitative and quantitative evidence; usability, workload, safety, performance, trust, and operational fit are distinct claims.
- Investigate error as an outcome to explain through conditions, goals, representations, controls, and adaptation—not a terminal cause label.
- Monitor leading conditions such as workload margin, alarm burden, stale models, handoff gaps, workaround growth, override patterns, and recovery-test results.
- Reassess after changes in automation, interface, policy, staffing, training, workload, environment, organization, threats, or user population.

### Common failures

Common failures include designing for an average user; interviewing only managers; treating procedure compliance as proof of safe work; adding automation without mode and authority analysis; measuring clicks instead of outcome; equating workload with task count; blaming attention after hiding state; alarming every anomaly; requiring a human confirmation too quickly to evaluate; assigning rare recovery to operators whose skill has decayed; testing only rested experts in nominal scenarios; ignoring maintenance and support work; optimizing local efficiency while removing system margin; treating adaptation as misconduct; and claiming that one survey, simulator session, or incident-free period validates the human–system design.

### Compact example

A synthetic sixty-second incident assigns one operator three individually feasible actions requiring 20, 25, and 45 seconds of exclusive attention. Earliest-deadline-first scheduling completes the first two but finishes the last at 90 seconds against a 60-second deadline. The declared demand/capacity ratio is $90/60=1.5$. This proves only that the fixture's single-channel assumptions are infeasible; it does not measure cognition or prove how real operators will adapt.

### Connections

This module builds on function allocation, interfaces, safety, risk, verification, operations, resilience, systems of systems, interoperability, and emergent risk. It prepares organizational control, policy and ethics, adaptive systems, and whole-system review, and it connects directly to platform experience, API operability, security operations, data quality, and distributed-system incident response.

## Governing Question

What arrangement of people, automation, information, authority, coordination, environment, and evidence lets a capability achieve its goals without depending on impossible attention, hidden state, brittle procedure compliance, or heroic recovery?

Human performance is not an external input supplied after technical design. Architecture creates cognitive work whenever it chooses what is automated, where state lives, how failures surface, who may decide, which goals conflict, and what recovery remains. Human factors therefore belongs in system framing, requirements, architecture, verification, operations, and evolution—not only in interface styling.

## Why This Matters

Software-intensive systems increasingly mediate high-consequence work: clinical decisions, transportation, energy control, financial operations, emergency coordination, cyber defense, and infrastructure recovery. Their behavior changes faster than procedures and training. Operators often see only abstractions produced by sensors, aggregation, models, and alerts, while automation acts at machine speed. A design can be locally usable and still create poor system control through stale data, ambiguous authority, hidden modes, alert coupling, or unmanageable recovery.

Human variability is not simply noise around a correct procedure. People detect weak signals, reconcile incomplete information, improvise around resource shortages, coordinate tacitly, and protect goals that designers did not encode. The same adaptations can also consume margin or become unsafe when conditions change. Engineering must learn how success is produced as well as how failure occurred.

NASA's Human Systems Integration guidance treats human considerations as integrated across lifecycle domains rather than a late cockpit or interface concern. The U.S. Nuclear Regulatory Commission's human-factors engineering review model connects operating experience, function allocation, task analysis, staffing, human-system interfaces, procedures, training, verification, and implementation. These are useful structures, not universal certification substitutes. The applicable domain authority, population, environment, and consequences determine the evidence required.

## Prerequisites and Retrieval

Before making a human-factors claim, retrieve:

1. stakeholder outcomes, mission goals, unacceptable losses, hazards, security/privacy obligations, performance constraints, and authority boundaries;
2. participant populations, roles, expertise, language, culture, age range, sensory/motor/cognitive variation, accessibility needs, and exclusion risks;
3. work settings including noise, lighting, vibration, temperature, mobility, protective equipment, remote work, interruption, isolation, and adversarial pressure;
4. work as imagined: requirements, procedures, staffing plans, training, schedules, responsibility matrices, interface specifications, escalation paths, and performance targets;
5. work as done: field observation, contextual inquiry, logs, incident and near-miss narratives, workarounds, shadow systems, informal coordination, overrides, and successful adaptations;
6. operational scenarios across startup, nominal, peak, degraded, maintenance, emergency, recovery, handoff, software update, and mixed-version conditions;
7. goals and conflicts: safety, production, legality, service, cost, fairness, security, privacy, schedule, and personal or organizational incentives;
8. function and authority allocation for sensing, interpretation, planning, decision, action, confirmation, monitoring, exception handling, override, rollback, and learning;
9. information flows, representations, alarm logic, model confidence, provenance, freshness, latency, uncertainty, missingness, and correction mechanisms;
10. temporal structure: deadlines, dwell times, concurrency, interruption, task switching, recovery time, shift length, circadian exposure, and surge duration;
11. team and organizational structure: communication channels, common artifacts, handoffs, supervision, cross-checks, incident command, psychological safety, and escalation;
12. evidence: task analyses, prototypes, usability studies, simulations, workload measures, field trials, accessibility evaluations, training results, operational monitoring, limitations, and open findings.

Create at least one **cognitive-work trace**. Follow a representative participant from cue to interpretation, decision, action, feedback, coordination, recovery, and learning. Record what was known, assumed, hidden, delayed, contested, or reconstructed at each point. Repeat for a degraded or surprising condition and for another role that depends on the first participant's action.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish human factors, usability, cognitive work, human reliability, and organizational performance;
2. analyze the gap between work as imagined and work as done without romanticizing either;
3. model a joint cognitive system in terms of goals, actions, information, process models, coordination, environment, and time;
4. perform function and authority allocation for nominal and recovery work;
5. reason about workload, attention, interruption, fatigue, modes, automation surprise, trust, and skill decay;
6. analyze team cognition, handoffs, common ground, and distributed decision making;
7. translate field evidence into requirements, architecture, interface, staffing, training, and operational controls;
8. design representative human-in-the-loop scenarios and complementary measures;
9. investigate error and adaptation through system conditions rather than blame labels;
10. state human-performance conclusions within an explicit evidence envelope.

## Core Exposition

**Start with work and outcomes.** A screen is never the whole human–system interface. The interface includes procedures, alarms, communications, workspace, tools, automation behavior, organizational rules, staffing, and consequences. Begin with what participants must achieve and avoid, then trace how the system supports or obstructs that work. A visually polished display can still deny authority, conceal data age, or make recovery impossible.

**Study work as done.** Procedures describe an intended path under assumed conditions. Field work includes missing data, unavailable services, timing conflicts, local knowledge, interruptions, resource constraints, and multiple goals. Observe representative settings and ask participants to reconstruct decisions around actual cases. Treat workarounds as evidence: some expose design defects, some protect performance, and some introduce new risk. Do not assume that either compliance or deviation is inherently safe.

**Use cognitive task analysis where cognition matters.** Conventional task decomposition records observable steps; cognitive task analysis also elicits cues, judgments, strategies, difficult discriminations, uncertainty, expertise, and recovery. Compare novice and expert strategies without making undocumented expertise a system requirement. Critical-decision interviews, think-aloud work on suitable non-emergency tasks, artifact walkthroughs, and simulation debriefs reveal different evidence and biases.

**Model the joint system.** Cognition may be distributed across people, checklists, maps, dashboards, automation, communication channels, and the physical world. Ask which part remembers state, detects mismatch, predicts change, holds authority, and verifies effect. Moving a reminder into software can improve persistence but create stale-state or common-mode risk. Automating a calculation can reduce arithmetic burden while weakening visibility into assumptions.

**Allocate goals and authority, not just functions.** Function-allocation slogans about what humans or machines do best are too coarse. Machines can repeat operations quickly but may be brittle outside modeled conditions; people can reinterpret novel context but have attention, time, and memory limits. Allocate sensing, interpretation, decision, action, monitoring, exception handling, and recovery together. State who can veto, override, degrade, stop, and re-enter, and what evidence they receive.

**Design automation as a teammate with inspectable behavior.** People need to know what automation is doing, why, with what data and confidence, under which constraints, and what it will do next. This does not require exposing every implementation detail. It requires decision-relevant state, intent, limits, and feedback. Prevent silent mode changes, ambiguous labels, inconsistent mappings, and controls whose effect depends on hidden context.

**Calibrate reliance rather than maximizing trust.** Appropriate reliance varies with capability, context, consequence, evidence, and fallback. Overreliance can persist after automation leaves its competence envelope; underreliance can discard genuine benefit. Support calibration with observable performance, uncertainty, boundary conditions, failure cues, meaningful explanations, reversible trials, and practiced alternatives. A self-reported trust score is not proof of correct reliance.

**Treat situation awareness as relational.** The familiar perception–comprehension–projection model is useful for asking whether participants can detect relevant elements, understand their meaning, and anticipate near-future state. But poor performance should not be explained by saying awareness was lost and stopping there. Trace sensor coverage, aggregation, display salience, data age, team communication, goals, interruptions, expectations, and automation behavior that shaped what could be known.

**Analyze workload as a dynamic relation.** Workload depends on demand, skill, strategy, interface, time, state, environment, and consequence. Low workload can produce vigilance loss; high workload can cause deferral, tunneling, shortcut, and coordination breakdown. Peaks, concurrency, and recovery matter more than average task counts. Use multiple measures—performance, errors, timing, subjective ratings, observation, communication, and physiological signals where justified—and interpret disagreements rather than averaging them away.

**Engineer interruption and resumption.** An interruption imposes orientation, suspension, memory, switching, and resumption costs. Preserve place, rationale, pending commitments, data versions, and safe restart points. Prioritize interruptions by consequence and time. Batch low-value notifications; allow deferral where safe. Test nested interruptions during diagnosis and recovery, not only clean task completion.

**Design alarms as control information.** An alarm should identify a condition that matters, support diagnosis and prioritized action, and have a defined lifecycle. Measure alarm rate, concurrence, persistence, acknowledgement, suppression, shelving, false and missed conditions, and response outcome. Alarm floods are often architecture or policy failures. Adding a louder signal does not create capacity or resolve competing actions.

**Account for fatigue and circadian conditions.** Shift duration, time of day, sleep opportunity, callouts, monotonous monitoring, sustained emergency work, and commuting can affect performance. Do not compensate for unsafe staffing with interface claims. Design rotations, rest, cross-checks, automation support, escalation, and recovery around the actual duty pattern. Collect data with privacy and labor safeguards; monitoring people is itself a socio-technical intervention.

**Support skill acquisition and retention.** Training must match roles, configurations, scenarios, decisions, and recovery responsibilities. Rare emergencies need simulation, rehearsal, job aids, and accessible expertise. Automation can remove practice opportunities; if manual fallback remains a safety claim, measure whether people can detect the need, take control in time, reconstruct state, and perform after realistic skill decay.

**Engineer handoffs and team cognition.** Teams need common ground about goals, state, plans, uncertainties, ownership, and expected next actions. Structure handoffs around risks and pending commitments rather than raw data transfer. Provide read-back or closed-loop communication when consequence requires it. Analyze distributed teams, language differences, asynchronous channels, hierarchy, and the possibility that a junior participant cannot challenge a mistaken plan.

**Design for population variation.** Accessibility is not an edge case. Visual, auditory, motor, cognitive, linguistic, and technological variation changes whether a person can perceive, understand, and act. Include representative participants early; support multiple modalities without assuming they are equivalent; test assistive technology, zoom, contrast, keyboard paths, captions, timing, plain language, and physical reach where applicable. Record who remains excluded and why.

**Investigate error as a system signal.** Describe the action and context precisely: what was selected, omitted, delayed, misunderstood, or coordinated poorly. Reconstruct goals, cues, process model, interface, workload, training, procedures, incentives, and prior success. A label such as “operator error” restates where the outcome appeared. Corrective action should strengthen the control system rather than merely demand more vigilance.

**Preserve beneficial adaptation.** People often trade precision, timeliness, completeness, and effort to keep a system functioning. Map these adjustments and the margins they consume. Standardization can improve coordination but can also remove safe local flexibility. Define protected constraints and authorized adaptation space, then make deviations visible enough to learn without punishing honest reporting.

**Use representative human-in-the-loop evidence.** Recruit participants matching roles and relevant variation. Reproduce tools, data, latency, interruptions, staffing, communication, environment, and stakes as far as ethical and practical. Include surprise carefully without deception that invalidates consent or learning. Predefine outcomes and observation plans, retain qualitative explanations, and distinguish formative discovery from summative acceptance.

**Triangulate measures.** Completion time can improve while comprehension declines; fewer clicks can hide greater memory burden; a workload scale can remain moderate while a rare catastrophic error emerges. Combine outcome quality, constraint violations, timing, recovery, coordination, error patterns, subjective experience, observation, and operational data. Tie each metric to a decision and acknowledge reactivity, small samples, learning, and simulator fidelity.

**Bind evidence to an envelope.** A successful study with eight expert day-shift operators does not establish performance for novices, night shifts, another language, new automation, or an emergency lasting six hours. Record participants, roles, training, scenarios, configurations, environment, duration, measures, learning order, exclusions, uncertainty, and anomalies. Define what changes require renewed analysis or test.

The following fixture screens a declared single-channel incident schedule. It does not model human cognition.

<!-- bijux-verify: {"id":"cognitive-work-attention-screen","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"horizon_seconds=60\ndeclared_attention_seconds=90\ndeclared_capacity_ratio=1.50\nauthenticate_alert:finish=20:deadline=30:late=0\ncoordinate_dependency:finish=45:deadline=55:late=0\ncontain_release:finish=90:deadline=60:late=30\nmissed_deadlines=1\nstatus=declared_single_channel_schedule_infeasible\nevidence=synthetic_scheduling_screen_only\n","stderr":""}} -->
```python
actions = [
    {"name": "authenticate_alert", "duration": 20, "deadline": 30},
    {"name": "coordinate_dependency", "duration": 25, "deadline": 55},
    {"name": "contain_release", "duration": 45, "deadline": 60},
]
horizon = 60
print(f"horizon_seconds={horizon}")
print(f"declared_attention_seconds={sum(item['duration'] for item in actions)}")
print(f"declared_capacity_ratio={sum(item['duration'] for item in actions) / horizon:.2f}")
elapsed = 0
missed = 0
for item in sorted(actions, key=lambda value: value["deadline"]):
    elapsed += item["duration"]
    late = max(0, elapsed - item["deadline"])
    missed += late > 0
    print(f"{item['name']}:finish={elapsed}:deadline={item['deadline']}:late={late}")
print(f"missed_deadlines={missed}")
print("status=declared_single_channel_schedule_infeasible")
print("evidence=synthetic_scheduling_screen_only")
```

## Definitions and Notation

Let participants be $P$, goals and protected constraints $G$, available actions $A$, observations $I$, process models $M$, coordination relations $C$, environment and resources $E$, and temporal conditions $T$. These sets change with mode and configuration. A participant's process model is an analytical construct inferred from behavior and evidence, not a directly observable database inside the person.

For scenario $s$, configuration $k$, and population $p$, define a human-performance claim envelope

$$
\Omega_H=\langle p,roles,training,k,s,environment,staffing,duration,measures,assumptions\rangle.
$$

Let protected constraint $g$ require that a consequential action be authorized, informed, timely, observable, and recoverable. A review may use the necessary gate

$$
eligible(a,g)\Rightarrow authority(a)\land information(a)\land time(a)\land feedback(a)\land recovery(a).
$$

The gate does not prove that each predicate is true, that all constraints were discovered, or that actual participants will succeed. It prevents a review from accepting an action path while a declared noncompensable support condition is absent.

The ratio $\rho_h=D_h/C_h$ is only a declared capacity screen. $D_h$ should name what is counted and whether demands interfere; $C_h$ should state staffing, exclusivity, duty period, and uncertainty. Real cognitive work is neither perfectly divisible nor necessarily additive.

## Mechanisms, Invariants, or Proof Structure

1. **Frame work and loss.** Name stakeholders, goals, protected constraints, environments, modes, unacceptable outcomes, and decision authority.
2. **Identify participants.** Describe representative roles, populations, expertise, variation, accessibility, staffing, and organizational position.
3. **Observe work as done.** Compare requirements and procedures with field activity, adaptations, artifacts, interruptions, and successful recovery.
4. **Model the joint system.** Trace goals, actions, information, process models, automation, coordination, environment, and time.
5. **Allocate function and authority.** Cover sensing through recovery, including veto, override, degradation, stop, and re-entry.
6. **Analyze cognitive demands.** Examine uncertainty, workload, interruption, attention, memory, modes, fatigue, skill, trust, and temporal coupling.
7. **Analyze team and organization.** Check common ground, handoffs, cross-checks, hierarchy, escalation, incentives, and resource control.
8. **Design support and controls.** Improve observability, action mapping, pacing, prioritization, feedback, resilience, accessibility, and learning.
9. **Validate representatively.** Combine inspection, analysis, participant study, simulation, accessibility evaluation, operational evidence, and recovery tests.
10. **Operate and evolve.** Monitor leading conditions, protect reporting, investigate mechanisms, preserve safe adaptation, and reassess changes.

Core invariants are: no human role receives responsibility without information, time, authority, tools, and recovery; no automation claim omits mode, boundary, feedback, and fallback; no workload average hides consequential peaks; no manual fallback is credited without detection, takeover, and retained-skill evidence; no participant study escapes its envelope; no error label ends causal analysis; and no design change inherits human-performance evidence without an applicability review.

There is no formal proof that a finite study covers all human behavior. Populations, strategies, teams, organizations, environments, and technology evolve. The engineering argument is a bounded case that the joint system supports representative work, protects constraints, exposes uncertainty, and can learn and recover.

## Alternatives and Trade-Offs

**Standardization versus local adaptation.** Standard procedures improve coordination, training, and auditability. Local adaptation handles context the standard did not encode. Protect hard constraints while defining when adaptation is authorized, recorded, escalated, and learned from.

**Automation versus direct human control.** Automation can improve speed, consistency, and reach, especially for high-rate computation. Direct control can preserve contextual judgment and recovery skill. Choose by consequence, observability, validated envelope, timing, reversibility, and fallback—not by a general preference for more or less automation.

**Dense information versus progressive disclosure.** Dense displays support expert scanning and relationships but can overwhelm novices or small screens. Progressive disclosure reduces initial burden but can hide dependencies and slow emergency access. Test representative tasks, experience levels, devices, and degraded data.

**Centralized coordination versus distributed teams.** Central coordination can maintain a global view and priority, but may become overloaded or distant from local conditions. Distributed authority can respond quickly but needs common ground, conflict resolution, and shared constraints. Hybrid command requires explicit triggers and precedence.

**Realism versus experimental control.** Controlled studies isolate mechanisms and support repeatability but omit operational context. Field studies reveal real adaptation but contain confounds and ethical limits. Simulation enables rare conditions but depends on fidelity. Triangulate rather than declaring one method inherently decisive.

**Efficiency versus resilience.** Removing apparent redundancy and idle time can improve nominal throughput while eliminating cross-checks, learning, and surge capacity. Justify staffing and slack against variability, recovery, and consequence; do not treat protected margin as waste merely because average utilization is low.

## Failure Modes and Misconceptions

- **“People are the weakest link.”** This hides how people create resilience and how design and organization shape action.
- **“Human error is the root cause.”** It identifies a location in the event chain, not the conditions that made the action reasonable or consequential.
- **“Usability proves safety.”** Ease of use, task success, hazard control, security, accessibility, and operational resilience are different claims.
- **“One average user represents the population.”** Variation in ability, expertise, language, context, and assistive technology can change outcomes.
- **“Workload equals task count.”** Timing, uncertainty, interruption, strategy, interference, fatigue, and consequence change demand.
- **“More information improves awareness.”** Volume and poor organization can obscure relevant state and relationships.
- **“An alarm transfers responsibility.”** A person needs time, meaning, authority, and feasible action; acknowledgement is not hazard control.
- **“A human in the loop guarantees oversight.”** The loop may be too fast, opaque, or overloaded for meaningful intervention.
- **“Training repairs a bad design.”** Training cannot create missing feedback, authority, capacity, or recoverability.
- **“Automation removes workload.”** It often moves work into monitoring, exception handling, coordination, and rare recovery.
- **“No complaints means acceptance.”** Reporting cost, hierarchy, exclusion, and learned workarounds can suppress evidence.
- **“Field observation is objective truth.”** Observation changes behavior and samples only selected settings and times.
- **“A simulator proves operations.”** Fidelity, participants, incentives, duration, surprise, and organizational context bound results.
- **“Adaptation is noncompliance.”** Some adaptation maintains constraints; some migrates risk. Analyze its mechanism and boundary.
- **“Human performance is stable after release.”** Staffing, expertise, procedures, automation, workload, and organizations continue to change.

## Worked Examples

### Example 1

**Situation:** A deployment dashboard uses green when individual services pass checks. **Reasoning:** Operators infer system readiness, but shared identity and queue capacity are not represented. Add an explicit end-to-end gate, dependency state, evidence age, and explanation of blocked promotion. **Conclusion:** Clear component displays can still support a false system model.

### Example 2

**Situation:** A fraud system asks an analyst to approve an automated denial within eight seconds. **Reasoning:** The interface shows a confidence score but not evidence provenance, alternatives, policy basis, or affected-user context. The nominal human approval is too fast to be meaningful. **Conclusion:** A human in the loop without decision time and information is ceremonial authority.

### Example 3

**Situation:** A network center receives 900 alarms after a power event. **Reasoning:** Each device correctly reports a local symptom, but alarm multiplication exceeds attention and hides the common cause. Correlate cautiously, preserve raw evidence, prioritize by protected outcome, and present dependency context. **Conclusion:** Alarm floods are system-design failures, not proof that operators ignored warnings.

### Example 4

**Situation:** Automation controls a vehicle for hours, then requests takeover in six seconds at its boundary. **Reasoning:** The driver must reorient, determine mode, reconstruct environment, and choose an action after vigilance and skill decay. The fallback claim needs detection, transition, time, interface, and training evidence. **Conclusion:** Retaining a manual control does not establish recoverable human authority.

### Example 5

**Situation:** Nurses bypass repeated barcode scans during an emergency. **Reasoning:** The procedure assumes network availability, sufficient devices, and normal urgency; the workaround restores timeliness but weakens identity control. Design a bounded degraded mode with visible reconciliation and clinical authority. **Conclusion:** Workarounds can reveal conflicting system constraints and missing recovery design.

### Example 6

**Situation:** A global incident handoff copies hundreds of log lines into chat. **Reasoning:** The receiving team lacks hypothesis, affected scope, rejected explanations, ownership, pending actions, and evidence age. A structured state-and-commitment handoff plus read-back repairs common ground. **Conclusion:** More transferred data does not guarantee team cognition.

### Example 7

**Situation:** A status page uses color alone and imposes a ten-second confirmation timeout. **Reasoning:** Some users cannot distinguish states, keyboard navigation takes longer, and screen readers receive unlabeled changes. Add text and shape, semantic announcements, focus control, adjustable timing, and assistive-technology tests. **Conclusion:** Accessibility changes whether system control is available, not merely whether presentation is pleasant.

### Example 8

**Situation:** A security operations team shows good mean response time. **Reasoning:** Night-shift and simultaneous critical alerts have long tails, and analysts create private filters to cope. Segment by shift, alert class, concurrency, staffing, experience, and outcome; study filters as adaptations. **Conclusion:** Averages can conceal workload peaks and unequal operating conditions.

### Example 9

**Situation:** A predictive-maintenance model reduces routine inspections. **Reasoning:** Maintainers lose exposure to early physical cues and become dependent on model classifications. Preserve diagnostic opportunities, uncertainty, manual sampling, feedback from repair, and fallback practice. **Conclusion:** Automation can reduce nominal effort while eroding the expertise needed outside its envelope.

### Example 10

**Situation:** A simulator study with twelve expert operators finds no missed shutdowns. **Reasoning:** Participants were rested, knew the scenario family, used one software version, and worked individually for twenty minutes. The result supports that configuration and sample only. **Conclusion:** Human-in-the-loop evidence must remain bounded by participant, scenario, duration, and fidelity.

## Cross-Program Connections

- **Platform Engineering:** paved paths, observability, deployment controls, and recovery interfaces shape developer cognitive load and incident work.
- **API and Service Engineering:** error semantics, idempotency, asynchronous status, and versioning determine whether operators and consumers can form correct process models.
- **Data Engineering:** freshness, lineage, quality, correction, and uncertainty affect decision support and trust calibration.
- **Distributed Systems:** partial failure, retry, time, consistency, and failover create hidden modes and difficult recovery work.
- **Security Engineering:** alert triage, authorization, usable security, insider risk, and incident command require joint technical and human control.
- **Software Design:** boundaries and representations can localize reasoning or force people to reconstruct state across many tools.
- **Machine Learning:** distribution shift, confidence, explanation, feedback loops, appeal, monitoring, and rollback govern appropriate reliance.
- **Accessibility Engineering:** inclusive interaction is a system capability and an evidence obligation, not a final visual inspection.
- **Organizational Engineering:** incentives, hierarchy, staffing, reporting, funding, and decision rights shape cognitive work.
- **Ethics and Governance:** surveillance, autonomy, fairness, accountability, consent, and redress constrain human-performance interventions.

## References

1. NASA, [Human Systems Integration Handbook](https://ntrs.nasa.gov/citations/20210010952), NASA/SP-20210010952, 2021.
2. U.S. Nuclear Regulatory Commission, [Human Factors Engineering Program Review Model](https://www.nrc.gov/reading-rm/doc-collections/nuregs/staff/sr0711/r3/index.html), NUREG-0711 Revision 3, 2012.
3. Federal Aviation Administration, [Human Factors Design Standard](https://hf.tc.faa.gov/publications/2016-12-human-factors-design-standard/), HF-STD-001B, 2016.
4. ISO, [ISO 9241-210:2019 Ergonomics of human-system interaction—Human-centred design for interactive systems](https://www.iso.org/standard/77520.html), 2019.
5. Jens Rasmussen, [Skills, Rules, and Knowledge; Signals, Signs, and Symbols, and Other Distinctions in Human Performance Models](https://doi.org/10.1109/TSMC.1983.6313160), IEEE Transactions on Systems, Man, and Cybernetics, 1983.
6. Mica R. Endsley, [Toward a Theory of Situation Awareness in Dynamic Systems](https://doi.org/10.1518/001872095779049543), Human Factors, 1995.
7. Raja Parasuraman, Thomas B. Sheridan, and Christopher D. Wickens, [A Model for Types and Levels of Human Interaction with Automation](https://doi.org/10.1109/3468.844354), IEEE Transactions on Systems, Man, and Cybernetics Part A, 2000.
8. Erik Hollnagel and David D. Woods, [Joint Cognitive Systems: Foundations of Cognitive Systems Engineering](https://www.routledge.com/Joint-Cognitive-Systems-Foundations-of-Cognitive-Systems-Engineering/Hollnagel-Woods/p/book/9780367864200), CRC Press, 2005.

## Exercises

### Exercise 1

Analyze the difference between work as imagined and work as done for an on-call engineer responding to a database failover.

### Exercise 2

Three incident actions require 18, 24, and 30 seconds of exclusive attention within a 60-second horizon. Compute the declared capacity ratio, then explain why the result is neither a workload measurement nor a safety proof.

### Exercise 3

Design a human–automation allocation for an AI-assisted medication-order review, including authority, uncertainty, override, degraded mode, recovery, and evidence.

### Exercise 4

Construct a representative evaluation plan for a control-room alarm redesign serving expert and novice operators across day and night shifts.

### Exercise 5

Transfer cognitive-work reasoning to a platform team designing a self-service production-deployment path.

## Answers to the Exercises

### Answer 1

Work as imagined may say: receive an alert, inspect replica health, confirm the primary is unavailable, promote the designated replica, redirect traffic, verify integrity and latency, notify stakeholders, and open a post-incident record. It may assume current dashboards, one incident, known ownership, working identity, complete runbooks, and authority to act.

Work as done may involve correlated alerts, stale replication metrics, an ambiguous cloud event, a recent topology change absent from the runbook, a second team running maintenance, expired credentials, business pressure to restore quickly, and uncertainty about whether the old primary can return. The engineer may open several tools, ask a colleague to reconstruct change history, delay promotion to protect consistency, or use an undocumented read-only mode.

Model both without declaring procedure or adaptation automatically correct. Strengthen configuration visibility, data age and provenance, split-brain interlocks, authority, communication, bounded degraded service, credential recovery, checklists around irreversible actions, and post-action feedback. Exercise the real topology with representative interruptions and handoffs. Preserve the engineer's useful diagnostic strategies while removing reliance on private memory and heroic access.

### Answer 2

Declared demand is $18+24+30=72$ seconds. With declared capacity 60 seconds,

$$
\rho_h=\frac{72}{60}=1.2.
$$

Under the assumption that one participant must give each action exclusive, indivisible attention within the same horizon, the assignment is infeasible by at least 12 seconds before considering switching or interruption cost. The screen supports redesign: remove or defer work, automate a safely bounded part, provide another qualified participant, change deadlines if consequences permit, or reduce the event coupling.

It is not a workload measurement because durations are declared, cognitive interference is simplified, expertise and strategy are absent, and real work may overlap or take longer. It is not a safety proof when the ratio is below one either: sequence, deadlines, information, authority, fatigue, uncertainty, coordination, and errors remain. Validate revised work with representative participants and scenarios.

### Answer 3

Protected outcomes include avoiding contraindicated medication, unjustified delay, privacy breach, automation bias, and loss of clinical accountability. The assistant may retrieve current medications, allergies, laboratory values, guidelines, provenance, and known interactions; compute candidates; and present uncertainty and missing data. A licensed clinician retains authority to approve, modify, reject, request evidence, or enter a documented emergency exception. High-consequence conflicts cannot be cleared by an unexplained score.

Make patient identity, units, freshness, source, model/version, rationale, conflicting evidence, and policy visible. Bound automation by validated population, medication classes, data completeness, and clinical context. In degraded mode, show unavailable capabilities explicitly and route to a safe manual procedure with feasible workload. Preserve original orders and model output, support reversal and reconciliation, and prevent a silent model or policy change during an active decision.

Evidence combines clinical and human-factors review, representative cases including rare and conflicting signals, accessibility, novice/expert comparison, time pressure, interruption, missing/stale data, adversarial input, false positive/negative consequences, override reasoning, team handoff, and recovery. Monitor outcome disparity, alert burden, reliance patterns, exceptions, appeals, drift, and near misses. The clinician's click is not proof that the decision was meaningfully reviewed.

### Answer 4

Define alarm-related losses and tasks before changing presentation. Retrieve alarm history by condition, shift, concurrence, device, acknowledgement, suppression, response, and outcome; observe how operators diagnose, coordinate, and adapt. Recruit expert and novice participants representative of language and accessibility needs from day and night operations, while avoiding unsafe fatigue induction. Include supervisors and maintainers because configuration and shelving work affect alarms.

Test nominal detection, common-cause floods, stale sensors, conflicting alarms, hidden dependencies, interruption during diagnosis, handoff, degraded displays, and recovery. Compare the current and candidate designs with counterbalanced order where feasible. Measure constraint violations, correct diagnosis, time to effective action, missed/false actions, resumption, communication, workload ratings, usability, and qualitative strategy. Retain raw event sequences and debrief surprises.

State the envelope: participant characteristics, training, shift context, simulator fidelity, scenarios, duration, configurations, and uncertainty. A laboratory result does not close field effectiveness. Stage deployment with rollback, observe alarm volume and outcomes, protect reporting, and define thresholds and owners for renewed review.

### Answer 5

The platform's goal is not merely fewer deployment steps. It is a comprehensible, authorized, recoverable change that preserves service, security, and evidence. Study how teams currently prepare, approve, deploy, observe, stop, roll back, and coordinate incidents. Identify private scripts, repeated interpretation, missing ownership, ticket delays, and adaptations that supply context the official path lacks.

The paved path should expose prerequisites, policy decisions, artifact identity, environment differences, expected effects, health evidence, uncertainty, progressive-delivery state, ownership, and rollback readiness. Automate repeatable checks and safe orchestration while retaining meaningful veto and override with reason and audit. Do not require developers to understand every platform mechanism, but make decision-relevant state and failure recovery visible.

Evaluate new and experienced teams on routine, high-risk, denied, partial-failure, stale-observability, dependency-failure, and rollback scenarios. Measure successful outcomes, time, policy violations, diagnosis, recovery, cross-team coordination, accessibility, support demand, and strategy—not clicks alone. Monitor abandonment, manual bypass, override, failed rollback, alert burden, and unequal team outcomes. A fast happy path that turns every exception into an expert platform ticket has moved rather than reduced cognitive work.
