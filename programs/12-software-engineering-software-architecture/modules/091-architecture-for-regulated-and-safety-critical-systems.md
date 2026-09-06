---
module_id: SARCH-091
program: Software Engineering: Software Architecture
level: 2
module_number: 91
title: Architecture for Regulated and Safety-Critical Systems
status: complete
last_verified: 2026-09-06
---

# Architecture for Regulated and Safety-Critical Systems

## One-Page Review

### Governing question

How should architects shape a software-intensive system when legitimate authorities require evidence of conformance and system behavior can contribute to injury, environmental damage, loss of essential service, or other unacceptable harm?

### Essential definitions

- a **regulated system** is subject to applicable law, regulation, authorization, or recognized conformity obligations; it is not necessarily safety-critical;
- a **safety-critical function** can cause, contribute to, control, detect, mitigate, or recover from a hazardous system condition;
- a **hazard** is a system state or set of conditions that, with a worst-case environment, can lead to harm;
- **risk** combines uncertainty about hazardous events and consequences under declared criteria;
- a **safety constraint** states behavior that must hold to prevent or control a hazard;
- **functional safety** is the part of overall safety that depends on a system responding correctly to inputs;
- **development assurance** uses disciplined lifecycle evidence to justify confidence appropriate to consequence;
- an **assurance case** is a structured claim, argument, and evidence package with context, assumptions, and defeaters;
- **independence** is freedom from a specified common cause, influence, resource, or verification conflict—not mere duplication;
- a **safe state** has acceptable risk for a defined condition and duration; it is context-specific;
- **fail-safe** moves toward a safe state on failure; **fail-operational** preserves required service through declared faults;
- a **degraded mode** delivers explicitly reduced capability under altered constraints and authority;
- **traceability** connects hazards, requirements, architecture, implementation, verification, configuration, and decisions bidirectionally;
- **configuration baseline** identifies the exact hardware, software, data, tools, parameters, and evidence to which a claim applies.

### Central model, mechanism, or theorem

Represent a safety-relevant architecture argument as

$$
A=(C,H,K,M,I,V,O,\Gamma,L),
$$

where $C$ is context and applicable authority, $H$ hazards and harms, $K$ safety constraints, $M$ mechanisms and system boundaries, $I$ independence and fault assumptions, $V$ verification and assurance evidence, $O$ operational authority and degraded behavior, $\Gamma$ the exact configuration baseline, and $L$ lifecycle change, incident, and retirement. Architecture is acceptable only when every material safety claim has justified evidence for the actual configured system and unresolved defeaters are visible to the authorized decision maker.

### Critical invariants

- applicability, classification, criticality, and acceptance authority come from the governing domain, not an architect's preference;
- conformance evidence and safety evidence overlap but neither implies the other;
- hazards are analyzed at the socio-technical system boundary, including people, environment, suppliers, data, and operation;
- every safety constraint traces to mechanisms, owners, verification, and operational response;
- critical functions declare timing, units, validity, authority, state, failure, and recovery semantics;
- redundancy claims identify independence and common-cause assumptions;
- fail-safe and fail-operational choices state the condition, horizon, and remaining capability;
- safety mechanisms remain effective during startup, update, rollback, maintenance, partial failure, and degraded operation;
- security, safety, privacy, accessibility, and operational constraints are reconciled rather than ranked silently;
- tools, generated artifacts, models, data, configuration, and third-party components are inside the assurance boundary when claims depend on them;
- change impact reaches hazards, assumptions, evidence, deployed configuration, training, and authorization;
- no checklist, test suite, standard citation, or assurance-case diagram proves universal safety.

### Common failures

Common failures include calling every important system safety-critical; treating regulated and safety-critical as synonyms; beginning from a standard checklist instead of hazards and authority; assigning software a criticality disconnected from system analysis; using redundancy with one power, clock, network, compiler, operator, or design fault; assuming shutdown is always safe; averaging away a catastrophic case; treating security controls as safety controls without interaction analysis; verifying nominal paths only; omitting maintenance and update states; using test coverage as proof; accepting supplier claims without integration evidence; allowing safety monitors to share the failing path; and declaring a safety case complete while assumptions or configuration are unknown.

### Compact example

An infusion system receives a prescribed rate, drives a pump, observes flow, alarms, and permits clinical override. System hazard analysis identifies overdose, underdose, delayed therapy, and unavailable alarm. The architecture separates prescription authority, dose-limit policy, command generation, independent flow observation, actuator control, alarm, audit, and human interface; every value carries units, patient/session identity, provenance, validity, and configuration. A stale or wrong-epoch command is inhibited. Network loss enters a bounded clinical mode rather than inventing a universal “safe shutdown.” Independent verification challenges shared sensors, power, compiler, and requirements. Named clinical, regulatory, safety, security, and product authorities decide fitness; the software chapter does not.

### Connections

[SARCH-070](070-running-an-evidence-based-architecture-review.md) supplies review mechanics. [SARCH-089](089-managing-exceptions-and-technical-risk.md) supplies bounded technical-risk decisions. [SARCH-092](../ROADMAP.md) next examines high-change domains, where change speed must still respect consequence and evidence.

## Governing Question

Regulation establishes legitimate obligations and decision authorities. Safety engineering controls hazards that can produce harm. A system may be regulated for privacy, financial integrity, spectrum use, or market conduct without controlling physical danger. A safety-critical function may exist in a sector with no product-specific software regulation. Architecture must discover the actual combination rather than borrow a label.

The hard work is maintaining a justified connection from hazardous system behavior to architectural constraint, implementation, exact configuration, operation, and change. Software acts through hardware, networks, operators, procedures, data, and organizations. A locally correct function can participate in unsafe control; a compliant development record can describe a system with an omitted hazard; a safe design can become unsafe after configuration drift.

## Why This Matters

IEC 61508 is a basic functional-safety standard for electrical, electronic, and programmable-electronic safety-related systems. The official record for IEC 61508-2:2010 identifies edition 2 and a 2027 stability date; software-specific requirements sit in IEC 61508-3 [1]. ISO 26262:2018 adapts functional-safety lifecycle concepts for production road vehicles [2]. These standards are domain-scoped. Their integrity levels, terminology, and lifecycle rules must not be mixed casually.

FAA Advisory Circular 20-115D remains active and recognizes DO-178C/ED-12C and supplements as an acceptable—but not the only—means of showing compliance with applicable airworthiness regulations for airborne software [3]. FDA's current recognized-consensus-standard record includes IEC 62304 edition 1.1 for medical-device software lifecycle processes and notes that it does not cover validation and final release of the complete device [4]. These examples demonstrate why a software process standard is part of a larger product authorization.

ISO/IEC/IEEE 15026-2:2022 specifies assurance-case structure and terminology [5]. A structured argument makes reasoning reviewable, but confidence depends on sound claims, valid evidence, true assumptions, representative configuration, and competent challenge. Architecture supplies the system mechanisms and trace links on which such arguments depend.

## Prerequisites and Retrieval

Retrieve harm, hazard, hazardous event, risk, safety, security, functional safety, criticality, integrity level, severity, exposure, controllability, safety constraint, fault, error, failure, common cause, independence, defense in depth, diversity, safe state, fail-safe, fail-operational, degraded mode, watchdog, interlock, authority, assurance, verification, validation, traceability, baseline, tool qualification, configuration, supplier, incident, and residual risk.

SARCH-018 through SARCH-020 supply safety-related quality scenarios, security interaction, usability, and accessibility. SARCH-022 through SARCH-030 supply architectural views and stakeholder-specific descriptions. SARCH-061 through SARCH-070 supply trade-off and evidence methods. This module integrates those ideas for regulated and safety-critical architecture. Systems Engineering owns broader hazard and lifecycle methods; domain-qualified authorities own classification, acceptance, and authorization.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish regulation, conformance, functional safety, system safety, and criticality;
2. derive architectural safety constraints from system hazards;
3. define critical interface semantics for identity, units, time, validity, authority, and failure;
4. design containment, monitoring, independence, diversity, and degraded modes;
5. distinguish fail-safe from fail-operational requirements;
6. evaluate redundancy under common-cause and correlation assumptions;
7. organize a claim-argument-evidence structure with visible defeaters;
8. include tools, suppliers, data, configuration, people, and operation in the assurance boundary;
9. perform architecture-level change impact and configuration reconciliation; and
10. state evidence limitations without claiming certification or safety.

## Core Exposition

**Establish applicable authority and context.** Identify product, use, users, jurisdictions, environments, operators, owners, suppliers, regulators, conformity routes, recognized standards, and authorization decisions. Record exact versions and interpretations. A standard may be mandatory, an accepted means, contractual, voluntary, or irrelevant depending on context. Architects provide evidence; they do not self-designate legal applicability.

**Define the socio-technical system boundary.** Include controlled process, hardware, software, communication, energy, sensors, actuators, operators, maintainers, users, data, environment, external services, suppliers, and emergency response. Model intended and reasonably foreseeable use and misuse. Moving a function outside one software process does not remove it from the hazard path.

**Classify from hazards, not importance.** Use the domain's legitimate method to identify whether software causes, controls, detects, mitigates, or responds to hazardous conditions. NASA guidance, for example, links safety-critical determination to system hazard analysis and several roles software can play [7]. Criticality affects rigor, independence, change, and evidence; it must not be assigned simply because a feature is commercially important.

**Derive safety constraints.** Express constraints on unsafe control, timing, sequence, values, states, transitions, authority, availability, and recovery. “The software shall be safe” is not verifiable. “No infusion command lacking the current patient-session identity, authorized prescription epoch, unit, and validity interval may reach the actuator” constrains an identifiable path.

**Allocate constraints to architecture.** Assign prevention, detection, containment, mitigation, recovery, and human action across independent elements. Avoid placing the constraint and sole monitor in one failure domain without justification. Trace each allocation to interfaces, deployment, data, state, timing, configuration, ownership, and verification.

**Make critical interfaces semantic.** Specify identity, units, range, precision, timestamp source, validity, freshness, sequence, authority, state preconditions, error, timeout, duplicate, loss, conflict, and recovery. Type compatibility is insufficient. A value of 5 can mean milligrams, milliliters per hour, stale sensor output, a test fixture, or the wrong patient.

**Control state and authority.** Safety-relevant commands need a single current authority or an explicit arbitration protocol. Use epochs, leases, fencing, state machines, interlocks, or physical separation as appropriate. Define behavior during startup, handover, partition, failover, restart, update, rollback, maintenance, and emergency override. Prevent a recovered stale controller from silently regaining command.

**Choose fail-safe or fail-operational from the hazard.** Stopping a factory robot may be safe in one state; stopping life support or rail signaling indiscriminately may create harm. Define the state considered safe, time available, environmental assumptions, operator action, and required continued capability. A system may fail-operational briefly and then transition to a different safe condition.

**Design containment and independence.** Partition critical from noncritical functions by resource, privilege, timing, state, deployment, and change. Bound queues, memory, CPU, network, storage, and retries. Independence claims name what is independent: requirements, design, implementation, power, clock, sensor, network, processor, compiler, verification, organization, or operation. Logical duplication on one host offers no power independence.

**Analyze common cause and correlation.** If two channels fail independently with probability $p$, simultaneous failure may be modeled as $p^2$ for the declared interval. If a common-cause event occurs with probability $q$, a simple illustrative model is

$$
P_{\mathrm{both}}=q+(1-q)p^2.
$$

With $p=0.01$ and $q=0.001$, this is $0.001+0.999(0.0001)=0.0010999$, nearly eleven times $0.0001$. The figures are hypothetical; the point is that an unjustified independence assumption can dominate the result.

**Use diversity carefully.** Different algorithms, languages, teams, or hardware can reduce selected common causes, but shared requirements, training data, sensors, compilers, libraries, infrastructure, and misunderstandings remain. Diversity also adds reconciliation, testing, and maintenance complexity. Identify the fault class it addresses and evidence it actually changes exposure.

**Reconcile security and safety.** Authentication can prevent unsafe commands; key rotation can also make a controller unavailable. Network isolation can contain attack; it can block remote monitoring. Logging can support investigation; it can leak sensitive data or consume critical resources. Jointly analyze malicious and accidental causes, privilege, update, recovery, emergency access, and degraded operation.

**Design human authority and observability.** Operators need actionable, timely, prioritized, accessible information and safe controls. Avoid alarm floods and opaque automation. Define acknowledgment, override, two-person action, handover, training, workload, and fallback according to context. Automation changes human work; it does not remove people from the system.

**Build an assurance case.** State top claims for the exact system and intended use. Decompose through hazards, constraints, architecture, implementation, verification, operation, and lifecycle. Attach evidence with provenance and validity. Record context, assumptions, confidence, counterevidence, unresolved hazards, and defeaters. Independent challenge should test the argument, not merely formatting.

**Match verification to claims.** Combine reviews, static analysis, formal reasoning, unit and integration tests, fault injection, timing analysis, simulation, hardware-in-the-loop, usability studies, penetration work, operational exercises, physical tests, and field evidence as applicable. Test boundaries, invalid input, overload, concurrency, restart, maintenance, update, rollback, partial failure, and long duration. Coverage measures executed structure; it does not prove the requirements complete or the oracle correct.

**Control tools and generated artifacts.** If a compiler, model transformer, code generator, test oracle, configuration tool, dataset, or deployment pipeline can introduce an undetected safety-relevant error, include it in tool strategy and assurance. Qualification or additional verification follows the governing scheme. Record exact versions, options, inputs, outputs, and reproducibility limits.

**Govern suppliers and reused components.** Obtain requirements, assumptions, failure behavior, evidence, configuration, vulnerability, lifecycle, and change information appropriate to the claim. Treat opaque software, hardware, cloud services, and models as uncertain boundaries. Wrap, monitor, restrict, diversify, replace, or add independent mitigation where evidence is insufficient. Supplier certification does not automatically establish safe integration.

**Baseline the deployed system.** Link source, generated code, binary, hardware revision, programmable logic, model, dataset, parameters, configuration, dependencies, tools, deployment, procedures, training, and evidence. Reconcile declared and observed configuration. A valid test against version A does not justify version B because filenames match.

**Perform change impact before and after release.** Trace a proposed change to hazards, constraints, interfaces, assumptions, evidence, tools, suppliers, operations, training, cybersecurity, and authorization. Preserve safety during migration and rollback. After deployment, monitor leading conditions, incidents, near misses, anomalies, workaround, and drift. Feed evidence into hazard analysis and the assurance case.

## Definitions and Notation

Let $A=(C,H,K,M,I,V,O,\Gamma,L)$. $C$ contains intended use, environment, stakeholders, authority, and applicability. $H$ contains hazards, hazardous scenarios, harms, and risk criteria. $K$ contains derived safety constraints. $M$ maps constraints to architecture and implementation mechanisms. $I$ records fault models, independence, diversity, and common causes. $V$ holds arguments and evidence. $O$ defines operational modes, human authority, monitoring, and emergency behavior. $\Gamma$ is the exact configuration baseline. $L$ controls change, incident, maintenance, and retirement.

A **fault** is an hypothesized or observed cause; an **error** is an incorrect internal state; a **failure** is externally visible deviation from required service. One fault can remain latent, propagate into error, and eventually cause failure. A hazard is not identical to a component failure: unsafe interaction among correctly operating components can be hazardous.

An assurance claim has form $(g,c,a,e,d)$: goal $g$, context and assumptions $c$, argument $a$, evidence $e$, and defeaters or doubts $d$. Evidence strength depends on claim fit, provenance, configuration, independence, coverage, and currency.

## Mechanisms, Invariants, or Proof Structure

### Hazard-to-mechanism trace invariant

Every material hazard traces through a safety constraint to allocated mechanisms, interfaces, owners, verification, operational response, and residual-risk authority. Every claimed safety mechanism traces back to at least one justified constraint. Missing links remain visible gaps.

### Configuration-identity invariant

An assurance claim applies only to configurations covered by its evidence and assumptions. Substituting hardware, binary, data, parameter, tool, network, procedure, or environment requires demonstrated equivalence or renewed analysis.

### Independence invariant

No independence credit is taken without naming the fault or influence being separated and evidence for that separation. Redundant components sharing a cause remain one failure domain for that cause.

### Lifecycle-safety invariant

Safety constraints apply in every reachable lifecycle state, including installation, startup, normal use, degraded operation, maintenance, update, rollback, recovery, and retirement. A safe destination cannot justify an unsafe transition.

### Executable command-admission illustration

<!-- bijux-verify: {"id":"safety-command-admission","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"current command: permit\nstale epoch: inhibit-epoch\nexpired command: inhibit-stale\ninvalid sensor: inhibit-input\nmaintenance state: require-authorized-manual\n","stderr":""}} -->
```python
def admit(*, epoch, current_epoch, age_ms, max_age_ms,
          inputs_valid, mode):
    if epoch != current_epoch:
        return "inhibit-epoch"
    if age_ms > max_age_ms:
        return "inhibit-stale"
    if not inputs_valid:
        return "inhibit-input"
    if mode != "automatic":
        return "require-authorized-manual"
    return "permit"

cases = {
    "current command": (8, 8, 40, 100, True, "automatic"),
    "stale epoch": (7, 8, 20, 100, True, "automatic"),
    "expired command": (8, 8, 140, 100, True, "automatic"),
    "invalid sensor": (8, 8, 30, 100, False, "automatic"),
    "maintenance state": (8, 8, 30, 100, True, "maintenance"),
}
for name, facts in cases.items():
    print(f"{name}: {admit(epoch=facts[0], current_epoch=facts[1], age_ms=facts[2], max_age_ms=facts[3], inputs_valid=facts[4], mode=facts[5])}")
```

This fictional predicate demonstrates explicit epoch, freshness, validity, and mode. It defines no clinically or physically safe threshold, cannot validate sensors, and is not a safety function.

### Proposition: conformance does not imply safety

Suppose a system satisfies every requirement in an applicable software-process standard, but hazard analysis omitted a harmful interaction with a manual maintenance mode. Process conformance and the omitted hazard can coexist. Therefore conformance alone cannot imply system safety.

### Proposition: duplication does not imply independence

Suppose two controllers run identical binaries on one processor and share power and input. One processor, power, sensor, requirement, or software fault can defeat both. Thus component count two can coexist with a single failure domain; duplication alone does not imply independence.

## Alternatives and Trade-Offs

**Fail-safe versus fail-operational.** Fail-safe limits exposure by stopping or moving to a known condition. Fail-operational preserves essential service through faults. Choose from hazard, time, environment, fallback, and recovery—not a universal reliability preference.

**Partition versus integration.** Strong partition reduces propagation and assurance scope but adds boundary, synchronization, and resource-allocation complexity. Integration reduces interfaces but expands critical scope. Justify the containment mechanism and shared dependencies.

**Homogeneous redundancy versus diversity.** Homogeneous channels simplify behavior and maintenance but share systematic faults. Diversity targets selected common causes but creates divergence and reconciliation risk. Neither creates independence automatically.

**Formal verification versus testing.** Formal methods can prove properties of a model under assumptions. Testing observes selected executions of an implementation. Both can miss wrong requirements, environment models, tool faults, and unexamined integration; combine them according to claims.

**Automation versus human control.** Automation offers consistent timely response; humans handle unmodeled context and legitimate authority. Humans can be overloaded or slow, and automation can be opaque or brittle. Design allocation, information, rehearsal, and graceful handover together.

## Failure Modes and Misconceptions

1. **“Regulated means safety-critical.”** Regulation may concern other protected outcomes.
2. **“Safety-critical means certified.”** Criticality and authorization are separate.
3. **“A standard defines every hazard.”** Local system analysis remains necessary.
4. **“Software cannot cause harm.”** It participates through controlled systems and decisions.
5. **“Component reliability proves system safety.”** Interaction can be unsafe without component failure.
6. **“Shutdown is always safe.”** Essential service may require bounded continued operation.
7. **“Redundant means independent.”** Common causes can defeat every channel.
8. **“Different code guarantees diversity.”** Requirements and infrastructure may remain shared.
9. **“The monitor is independent.”** It may share sensor, clock, power, compiler, or state.
10. **“Security and safety always align.”** Controls can create conflicting failure behavior.
11. **“Coverage proves correctness.”** It says nothing alone about complete requirements or valid oracles.
12. **“Formal proof proves the product safe.”** Proof scope and assumptions bound the claim.
13. **“A supplier certificate transfers assurance.”** Integration and configuration require evidence.
14. **“The binary name identifies the baseline.”** Exact provenance and configuration matter.
15. **“Rollback restores safety.”** State, data, hardware, and procedure may be incompatible.
16. **“Operators are a fallback.”** They need authority, information, time, training, and workable load.
17. **“An assurance case is a diagram.”** It is an evolving argument with evidence and defeaters.
18. **“No incidents proves safety.”** Exposure, detection, duration, and chance limit inference.

## Worked Examples

### Example 1

**Situation.** A payment service is heavily regulated but cannot physically injure a user through its direct operation.

**Reasoning.** Map financial, privacy, market, availability, and consumer obligations without applying an automotive safety integrity level. It may be mission-critical and highly consequential while not functionally safety-critical. Use domain-appropriate controls and authorization.

**Conclusion.** Consequence and applicable authority determine the assurance scheme, not rhetorical importance.

### Example 2

**Situation.** An infusion command carries value 5 without unit or patient-session identity.

**Reasoning.** Type checking succeeds while milligrams and milliliters per hour differ, and a valid command may target the wrong patient. Add unit, range, prescription provenance, patient/session identity, epoch, validity, state precondition, acknowledgment, and independent observation.

**Conclusion.** Safety-relevant interfaces require domain semantics beyond wire compatibility.

### Example 3

**Situation.** A rail door controller loses communication while a train is moving.

**Reasoning.** “Fail open” and “fail closed” are both incomplete. Use train state, platform detection, speed, local interlocks, validated timeout, operator authority, and bounded degraded procedures. Prevent stale central commands from overriding newer local state.

**Conclusion.** Safe state depends on context, time, and physical process.

### Example 4

**Situation.** Two safety channels run on one processor with one power supply.

**Reasoning.** Duplication may detect selected logic disagreements, but processor, power, clock, compiler, requirement, and input faults remain common. Claim only demonstrated coverage. Add physical separation or independent mitigation where the hazard requires it.

**Conclusion.** Redundancy is a mechanism; independence is a claim requiring a named fault model.

### Example 5

**Situation.** A manufacturer replaces a sensor with a pin-compatible model.

**Reasoning.** Evaluate range, precision, latency, failure behavior, calibration, diagnostics, environmental limits, electromagnetic behavior, supplier process, driver, configuration, hazard links, tests, procedures, and authorization. Connector compatibility establishes almost none of these.

**Conclusion.** Configuration change requires claim-level impact, not only interface fit.

### Example 6

**Situation.** A formal proof shows a controller never commands pressure above limit $P$.

**Reasoning.** Inspect whether the model includes unit conversion, numeric overflow, actual compiler, configuration, sensor error, actuator dynamics, concurrency, maintenance mode, and the correct value of $P$. Retain the proof as strong evidence for its precise property and assumptions.

**Conclusion.** Formal evidence can be powerful without becoming a universal product-safety claim.

### Example 7

**Situation.** A security update invalidates certificates during emergency operation.

**Reasoning.** Jointly analyze compromise, unavailable command, key custody, time, offline nodes, rollback, and emergency authority. Stage dual trust inside a bounded interval, protect downgrade, verify revocation, rehearse disconnected recovery, and remove old trust with configuration evidence.

**Conclusion.** Security change must preserve safety-relevant availability and authority through transition.

### Example 8

**Situation.** A medical-device supplier provides a component certificate but withholds failure details.

**Reasoning.** Identify claims the component supports, exact version and configuration, integration assumptions, and missing evidence. Restrict privileges and function, wrap inputs and outputs, monitor independently, test faults, obtain contractual change notice, or replace it. Escalate unresolved residual risk to legitimate product authorities.

**Conclusion.** Supplier evidence informs but does not certify system integration.

### Example 9

**Situation.** A software update passes all nominal tests but changes recovery timing.

**Reasoning.** Trace the timing assumption to hazards, degraded mode, watchdog, operator procedure, capacity, and recovery test. Exercise overload, restart, partial network, old/new coexistence, rollback, and long-duration behavior on the actual baseline. Update training and assurance evidence.

**Conclusion.** Safety-relevant change includes transitions and operation, not only functional output.

### Example 10

**Situation.** A floodgate system combines water sensors, weather data, automated actuation, remote control, and local operators.

**Reasoning.** Model upstream and downstream harm, false and missed readings, power and link loss, malicious command, gate jam, conflicting authorities, evacuation, accessibility, environment, and manual action. Separate sensing, plausibility, forecast advice, command policy, actuation interlocks, position observation, alarms, and audit. Preserve local safe authority during isolation, validate physical limits, rehearse emergency modes, and involve water, environmental, safety, security, accessibility, municipal, and affected-community authorities.

**Conclusion.** Whole-system authority and physical evidence bound what software architecture can claim.

## Cross-Program Connections

- [Testing and Software Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns verification strategy, coverage, oracle, independence, and fault-injection methods.
- [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns safe delivery, recovery, incident, and operational evidence.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) owns scheduling, memory, isolation, timing, and kernel mechanisms behind containment claims.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns threats, authorization, secure update, keys, and security assurance.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns system hazards, requirements, lifecycle, physical integration, human factors, and assurance in depth.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns qualified or governed delivery capabilities where a platform forms part of the evidence chain.

## References

1. IEC, [IEC 61508-2:2010, *Functional safety of electrical/electronic/programmable electronic safety-related systems — Part 2*](https://webstore.iec.ch/en/publication/5516), edition 2.0, April 2010; official record and 2027 stability date checked 2026-09-06. IEC 61508-3 contains software requirements.
2. ISO, [*ISO 26262 Road Vehicles — Functional Safety*](https://www.iso.org/publication/PUB200262.html), second-edition multipart series, 2018; official collection record checked 2026-09-06.
3. FAA, [Advisory Circular 20-115D, *Airborne Software Development Assurance Using EUROCAE ED-12( ) and RTCA DO-178( )*](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf), July 2017; active status and recognized documents checked 2026-09-06.
4. U.S. FDA, [Recognized Consensus Standard 13-79: IEC 62304 Edition 1.1](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/detail.cfm?standard__identification_no=38829), medical-device software lifecycle processes; current recognition record checked 2026-09-06.
5. ISO/IEC/IEEE, [ISO/IEC/IEEE 15026-2:2022, *Systems and software engineering — Systems and software assurance — Part 2: Assurance case*](https://www.iso.org/standard/80625.html), 2nd ed., November 2022; published status checked 2026-09-06.
6. Nancy G. Leveson, *Engineering a Safer World: Systems Thinking Applied to Safety*, MIT Press, 2011, [open-access book record](https://mitpress.mit.edu/9780262533690/engineering-a-safer-world/). System hazards, unsafe control, and socio-technical safety.
7. NASA, [Software Engineering and Software Assurance Handbook](https://swehb.nasa.gov/), implementing guidance for NPR 7150.2 and NASA-STD-8739.8; current official resource and safety-critical determination guidance checked 2026-09-06.
8. NASA, [NASA-STD-8739.8, *Software Assurance and Software Safety Standard*](https://standards.nasa.gov/standard/NASA/NASA-STD-87398), official standard resource checked 2026-09-06.
9. John C. Knight, “Safety Critical Systems: Challenges and Directions,” *Proceedings of the 24th International Conference on Software Engineering*, pp. 547–550, 2002, [DOI 10.1145/581339.581406](https://doi.org/10.1145/581339.581406).
10. Tim Kelly and Rob Weaver, “The Goal Structuring Notation — A Safety Argument Notation,” Proceedings of the Dependable Systems and Networks Workshop on Assurance Cases, 2004. Structured safety-argument context.
11. ISO, [ISO 14971:2019, *Medical devices — Application of risk management to medical devices*](https://www.iso.org/standard/72704.html), 3rd ed., December 2019. Domain-specific medical-device risk-management context.
12. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021. Quality scenarios, architecture tactics, trade-offs, and evidence.

## Exercises

### Exercise 1

Distinguish regulated, mission-critical, safety-critical, conforming, and safe. Explain why none is a synonym for another.

### Exercise 2

Two independent channels each have hypothetical failure probability $p=0.02$ per mission. Compute the simultaneous-failure estimate under independence. Recompute with common-cause probability $q=0.003$ using $q+(1-q)p^2$. State why neither number proves safety.

### Exercise 3

Diagnose this claim: “The controller is safe because it has two replicas, 100% statement coverage, and a certified supplier library.” Identify at least ten missing questions.

### Exercise 4

Create an architecture-level assurance outline for an automated warehouse vehicle. Include hazards, constraints, boundaries, independence, human authority, evidence, configuration, and change.

### Exercise 5

Design the architecture and assurance approach for a remote wildfire lookout system with cameras, smoke sensors, machine-learning advice, intermittent networks, public warnings, local responders, changing models, privacy-sensitive imagery, and harsh weather.

## Answers to the Exercises

### Answer 1

Regulated means subject to applicable legal, regulatory, authorization, or conformity obligations. Mission-critical means failure materially harms a mission. Safety-critical means a function can cause, control, detect, mitigate, or recover from hazardous conditions under the domain's analysis. Conforming means specified applicable requirements are satisfied. Safe means risk is judged acceptable by legitimate authority for defined use and context. A regulated tax system may not be safety-critical; an experimental machine may be safety-critical before formal certification; a conforming process can omit a local hazard; and a safe state in one environment can be hazardous in another. Classification, evidence, and decision authority must remain explicit.

### Answer 2

Under the stated independence assumption, $p^2=0.02^2=0.0004$. With the illustrative common-cause model, $0.003+(1-0.003)(0.0004)=0.003+0.997(0.0004)=0.0033988$. The common cause dominates. Neither result proves safety because probabilities may be uncalibrated; missions may differ; channels may not be independent; loss severity, exposure, detection, repair, and demand rate are absent; systematic design and requirement faults are omitted; common causes are incomplete; and acceptable risk is a legitimate domain decision. A correct calculation retains assumptions and units.

### Answer 3

Ask: what hazards and harms exist; what safety constraints follow; which functions can contribute; what fault and demand models apply; independent with respect to what; what power, clock, processor, sensor, network, requirement, compiler, library, and operator are shared; how replicas arbitrate disagreement; whether failure is detectable; which states and timing matter; whether the oracle and requirements are valid; what statement coverage omits; which library version, scope, configuration, and claims were certified; how integration assumptions are met; what happens during startup, overload, maintenance, update, rollback, partition, and emergency; what human authority and fallback exist; what exact baseline was tested; and who accepts residual risk. The original facts are evidence fragments, not a safety argument.

### Answer 4

Identify collision, crushing, dropped load, blocked egress, fire, unsafe speed, lost localization, and unavailable stop. Derive constraints for bounded speed and separation, valid route authority, obstacle response, load state, emergency stop, energy, and degraded operation. Separate mission planning, safety-rated motion control, localization diversity, obstacle detection, actuator interlock, independent stop, fleet coordination, operator interface, and audit; bound shared compute and networks. State common causes and human handover. Evidence includes hazard analysis, timing and braking calculations, simulation, fault injection, hardware-in-the-loop, physical boundary tests, usability and accessibility work, security analysis, maintenance procedures, and drills. Baseline hardware, firmware, maps, configuration, tools, and procedures. Reassess hazards and evidence for vehicle, layout, load, model, software, or operational change. Qualified warehouse-safety and regulatory authorities decide acceptance.

### Answer 5

Treat detection and public warning as different authorities. Hazards include missed or false fire indication, stale imagery, privacy exposure, wrong location, inaccessible warning, network loss, compromised sensor, model drift, alert overload, responder misdirection, and unsafe field maintenance. Carry source identity, geography, time, uncertainty, provenance, model version, and expiry. Separate acquisition, sensor plausibility, evidence storage, model advice, human assessment, warning authorization, geographic targeting, accessible message generation, channel delivery, correction, and audit. The model advises unless legitimate policy grants bounded automation; it cannot silently issue public warnings.

Local lookouts retain offline observation and responder contact; warning channels expose freshness and support authenticated correction. Use diverse sensors where they address known causes, protected local power, bounded queues, store-and-forward, independent communication, and explicit degraded modes. Verify harsh weather, smoke and non-fire confounders, darkness, obstruction, clock error, loss, overload, compromise, old/new model coexistence, rollback, and prolonged isolation. Baseline cameras, calibration, models, training data provenance, software, hardware, configuration, geography, and procedures. Monitor drift and near misses, protect imagery and affected communities, and require wildfire-science, emergency-management, accessibility, privacy, security, telecommunications, responder, public-authority, and community review. No software test alone authorizes a warning or proves public safety.
