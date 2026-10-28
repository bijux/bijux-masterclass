---
module_id: SARCH-016
program: Software Engineering: Software Architecture
level: 1
module_number: 16
title: Testability Tactics
status: complete
last_verified: 2026-09-05
---

# Testability Tactics

## One-Page Review

### Governing question

How should architecture make relevant states controllable, outcomes observable, dependencies substitutable, and failures reproducible so claims can be tested without creating unsafe production bypasses?

### Essential definitions

- **testability** is the degree to which a system supports establishing test preconditions, applying stimuli, observing relevant outcomes, and diagnosing deviations under stated cost and confidence constraints.
- **controllability** is the ability to place the system and its environment into states required by a test.
- **observability** is the ability to distinguish relevant states and transitions through trustworthy outputs or evidence.
- A **test oracle** determines whether an observed outcome satisfies the expected property.
- A **test seam** is a boundary at which behavior or a dependency can be controlled or observed without editing the tested logic.
- **isolation** constrains interference among tests, tenants, resources, and external systems.
- **determinism** means that declared inputs and state determine the relevant outcome; reproducibility permits controlled replay even when the production system is intentionally nondeterministic.
- **fault injection** introduces a declared fault or adverse condition to observe bounded behavior.
- **test debt** is the accumulating cost and risk caused by weak, slow, flaky, inaccessible, or misleading verification mechanisms.

### Central model, mechanism, or theorem

Represent a tested transition system as $(S,I,O,\delta,\lambda)$ with states $S$, controllable inputs $I$, observable outputs $O$, transition function or relation $\delta$, and observation function $\lambda$. A required state $s_t$ is controllable from allowed setup state $s_0$ when some finite permitted input sequence reaches it. Two states are observationally distinguishable for a claim when some permitted experiment produces different relevant observations.

Architecture improves testability by exposing stable domain commands and observations, controlling time and nondeterminism, isolating state and dependencies, making setup and cleanup reliable, and preserving traceable evidence. It does not expose raw internals merely to raise a coverage number.

### Critical invariants

- derive tests and oracles from requirements, risks, invariants, contracts, and failure models;
- control relevant time, randomness, identity, configuration, state, dependencies, and fault conditions;
- observe outcomes at the boundary that owns the claim, including negative and delayed effects;
- isolate tests from each other and from unauthorized external or production writes;
- keep test seams semantically faithful to production contracts and failure behavior;
- make setup, reset, cleanup, and replay explicit, bounded, and auditable;
- prevent debug, bypass, fault, and synthetic identities from expanding production authority;
- record version, topology, data, stimulus, actual observation, oracle, and limitation;
- treat flaky or non-reproducible outcomes as evidence defects rather than acceptable noise;
- combine test evidence with review and production observation without claiming universal correctness.

### Common failures

Common failures include hidden wall clocks and randomness; singleton state; shared test tenants; unbounded asynchronous waiting; mocks that reproduce implementation calls but not provider semantics; test-only bypass endpoints deployed to production; logs without correlation or outcome meaning; destructive cleanup; fault injection without blast-radius control; snapshots that approve unintended change; coverage targets without meaningful oracles; and passing tests whose data, configuration, schema, or dependencies differ materially from production.

### Compact example

An expiry rule calls the wall clock directly, so a midnight test sometimes fails and waiting months is impractical. Make a clock capability an explicit dependency of the policy. Production supplies a monotonic or civil-time implementation appropriate to the rule; tests supply named instants, time zones, clock jumps, and boundary transitions. The seam controls relevant time without exposing a privileged endpoint or rewriting domain logic.

### Connections

[SARCH-004](004-quality-attributes-as-architectural-drivers.md) supplies measurable scenarios; [SARCH-006](006-architecturally-significant-requirements.md) supplies test-worthy requirements; [SARCH-011](011-availability-and-recovery-tactics.md) supplies fault and recovery scenarios; [SARCH-014](014-security-and-privacy-tactics.md) constrains test authority and data; and [SARCH-015](015-modifiability-and-evolvability-tactics.md) supplies seams and replaceable contracts. The Testing & Quality Engineering program owns testing theory and technique in depth; this module owns architectural affordances that make those techniques possible.

## Governing Question

A component can have high statement coverage while the system's failover, authorization, migration, and recovery behavior remains untestable. A production-like test can be misleading if state cannot be reset, asynchronous outcomes cannot be correlated, or an external simulator behaves unlike the real provider. What architecture decisions let evidence address the real claim?

The governing question is how a test obtains legitimate control, stimulates the correct boundary, observes every relevant outcome, applies a sound oracle, and leaves trustworthy evidence. Testability is not the number of test hooks; it is the system's capacity to support discriminating experiments safely and economically.

## Why This Matters

Untestable architecture makes uncertainty expensive. Teams avoid changes, rely on manual folklore, discover failure behavior in production, or accept flaky suites that no longer constrain design. Slow setup and diagnosis lengthen feedback and encourage broader, riskier batches.

Test mechanisms can themselves create risk. A bypass identity, reset endpoint, unrestricted fault injector, copied production dataset, or mutable shared environment can violate security, privacy, availability, and evidence integrity. Architectural testability must preserve the same control boundaries it helps verify.

Distributed and asynchronous behavior increases the challenge. One command can produce delayed messages, retries, state changes, notifications, and external effects. A synchronous response is not the whole outcome. Stable operation identity, traceable causality, virtual time, controlled dependencies, and reconciliation evidence become design concerns.

## Prerequisites and Retrieval

Retrieve requirement, invariant, risk, state, transition, input, output, precondition, oracle, test double, contract, dependency, seam, isolation, determinism, idempotency, timeout, trace, fault model, cleanup, replay, and evidence limitation.

From earlier modules, retrieve system boundaries, quality scenarios, ASRs, assumptions, decision records, availability and recovery, security trust boundaries, compatibility transitions, and deployment environments. You should be able to distinguish observed behavior from a correctness proof and internal instrumentation from a stakeholder outcome.

## Learning Objectives

After completing this module, you should be able to:

1. define testability scenarios with control, observation, oracle, cost, and evidence measures;
2. identify uncontrollable states and unobservable outcomes;
3. create stable seams for time, randomness, identity, state, and external dependencies;
4. design faithful fakes, simulators, contract checks, and integration boundaries;
5. isolate test state and make setup and reset reproducible;
6. support asynchronous causality, virtual time, and eventual-outcome observation;
7. add fault injection with scope, authority, stop conditions, and recovery;
8. prevent test facilities and data from becoming production vulnerabilities;
9. design layered evidence across unit, component, integration, system, and operation;
10. evaluate flakiness, diagnostic cost, and evidence limitations honestly.

## Core Exposition

**Frame a testability scenario.** Name the claim, source of test request, system state, stimulus, environment, required control, required observation, oracle, and measures. Measures may include setup time, execution time, observation delay, diagnosis time, reproducibility, isolation, fault coverage, and false-result rate.

Start with risky outcomes: authorization, money, state transition, migration, concurrency, recovery, safety, privacy, and supplier behavior. Do not optimize for tests that are easy while critical claims remain inaccessible.

**Design controllability.** A test must establish valid initial state and trigger relevant events. Make clocks, random sources, identity contexts, configuration, queues, schedulers, storage, and external effects controllable through ordinary owned interfaces or constrained seams. Prefer domain commands and builders over direct mutation of private representation.

Control is bounded. Tests should not manufacture impossible states unless the claim explicitly concerns corruption or defense. When direct state injection is necessary, label it and retain separate evidence that production transitions can reach valid states.

**Design observability for claims.** Observe externally meaningful results first: response, persisted state, emitted event, external call, audit decision, resource state, and delayed reconciliation. Internal counters and logs aid diagnosis but do not replace boundary outcomes.

Provide stable operation and causation identities across synchronous and asynchronous work. Structured events should expose semantic state and reason without leaking secrets or personal data. Define when an outcome is final, pending, compensated, or unknown.

**Construct sound oracles.** An oracle may compare exact outputs, validate invariants, check metamorphic relations, compare independent implementations, consult a model, or require qualified human judgment. Every oracle has scope. A snapshot detects change but does not decide whether the new value is correct.

Avoid duplicating the implementation in the test because the same defect can appear twice. Express expectations in domain terms and derive boundary cases from requirements and invariants. For approximate, concurrent, or nondeterministic systems, define acceptable sets and statistical or temporal bounds honestly.

**Create seams around volatility and nondeterminism.** Dependency injection is one mechanism, not the goal. A good seam exposes the smallest stable capability required by the policy and supports production and test implementations under one semantic contract.

Control civil time, monotonic duration, randomness, identifiers, ordering, retries, and scheduling separately when their meanings differ. A single global “test mode” hides which property changed and can permit impossible combinations.

**Use test doubles by fidelity need.** A stub returns programmed results; a fake implements simplified but working semantics; a simulator models selected behavior; a mock verifies expected interactions. Choose according to the claim. A mock can verify that code sent one call but cannot prove a supplier accepted, deduplicated, or settled it.

Contract verification checks shared examples or schemas at a boundary. It catches some drift but cannot prove implementation equivalence, operational limits, or every semantic edge. Retain selected real integration and end-to-end tests for the risks doubles cannot represent.

**Control state lifecycle.** Tests need isolated namespaces, deterministic fixtures, schema versions, ownership, retention, and cleanup. Prefer unique test identities and idempotent teardown over deleting broad shared state. Make reset APIs unavailable to unauthorized environments.

Database rollback can isolate one process but may not undo messages, caches, files, external calls, or background work. Track every side effect and wait for or cancel owned work before cleanup. Test recovery from interrupted cleanup.

**Handle asynchronous behavior.** Do not use arbitrary sleeps as synchronization. Observe a condition through a stable API or event, with a bounded deadline and diagnostic state. Virtual time can advance timers deterministically only if every relevant clock and scheduler participates.

Record causal identity, attempts, offsets, versions, and terminal states. Test duplicate, missing, reordered, delayed, and replayed events. Preserve idempotency and reconciliation rather than forcing synchronous behavior solely for tests.

**Support deterministic replay carefully.** Capture inputs, versions, configuration, seeds, ordering, clock events, and relevant dependency results. Replay cannot reproduce undeclared shared state, hardware timing, races, or external actors. Label the boundary of determinism.

For concurrency, deterministic schedulers can explore selected interleavings; stress tests can expose but not enumerate races. Combine invariants, model checks where appropriate, targeted schedules, long-running stress, and production diagnostics.

**Inject faults safely.** Expose fault controls at the resource or boundary whose behavior is under test: delay, loss, duplication, exception, capacity exhaustion, corrupt input, dependency outage, or process loss. Define authorized environment, target, magnitude, duration, blast radius, stop condition, cleanup, and observer.

Production fault injection requires strong authorization, peer or automated safeguards as consequence warrants, monitoring, rollback, and incident coordination. A test result supports only the injected fault, topology, load, version, and observation period.

**Make diagnostics actionable.** When a test fails, preserve expected and actual values, relevant state transitions, correlation identifiers, dependency observations, seed, timing, topology, version, and logs with privacy controls. Diagnostic information should identify the violated property before exposing implementation trivia.

Feedback time can be modeled as setup plus execution plus observation plus diagnosis. Parallel execution helps only if tests and resources are isolated. Sharding a flaky suite can increase nondeterministic interference and reduce trust.

**Protect production boundaries.** Do not ship unauthenticated debug, bypass, reset, clock-control, or fault endpoints. Where production diagnostics or controlled experiments are legitimate, treat them as real privileged capabilities with identity, authorization, scope, audit, expiry, rate bounds, and safe failure.

Use synthetic identities and data that cannot access real users. If representative personal or regulated data is necessary, obtain legitimate authority, minimize it, isolate it, protect it, retain it only as required, and audit use. Masking alone may not eliminate re-identification risk.

**Layer evidence.** Fast focused tests localize logic. Component tests verify owned contracts and state. Integration tests exercise real boundaries. System tests verify user-visible workflows. Performance, fault, migration, security, accessibility, and operational exercises address specialized claims. Review and static analysis examine properties execution may miss.

No pyramid shape or test count is universally correct. Allocate evidence by risk, feedback cost, fidelity, and diagnosability. Remove redundant tests only when another layer preserves the claim.

**Govern flakiness.** A flaky result cannot reliably distinguish product behavior from test and environment behavior. Quarantine may preserve pipeline availability briefly, but it must retain owner, impact, diagnosis, expiry, and repair. Re-running until green destroys negative evidence.

Classify nondeterminism: product race, uncontrolled dependency, shared state, resource exhaustion, clock, ordering, environment drift, or weak oracle. Fix the cause or narrow the claim. Track false-pass as well as false-fail risk.

**Record reproducible evidence.** Store module or requirement identity, test identity, environment, versions, dependencies, data class, exact stimulus, seed, command, timestamps, actual output, oracle, result, and limitations. Protect evidence integrity and access.

Passing tests prove only observed conformance for tested cases and conditions. Current catalogs such as the [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) can guide security verification coverage, while standards such as [ISO/IEC/IEEE 29119-2](https://www.iso.org/standard/79428.html) describe test processes; neither substitutes for system-specific risks and oracles.

## Definitions and Notation

Let the transition system be $(S,I,O,\delta,\lambda)$, where $\delta:S\times I\rightarrow S$ is deterministic for the simplified model and $\lambda:S\rightarrow O$ exposes relevant observation. Extend $\delta$ to finite input sequences $I^*$ as $\delta^*$.

State $s_t$ is controllable from $s_0$ under permitted tests when

$$
\exists \sigma\in I^*: \delta^*(s_0,\sigma)=s_t.
$$

States $s_1$ and $s_2$ are immediately observationally distinguishable when $\lambda(s_1)\ne\lambda(s_2)$. More generally, they may be distinguished by some permitted future input sequence whose observations differ. These properties are relative to the modeled state, input, output, and permissions.

For one feedback cycle, define

$$
T_f=T_{setup}+T_{execute}+T_{observe}+T_{diagnose}.
$$

For a defect independently detected by one run with probability $p$, the probability of at least one detection in $n$ runs is $1-(1-p)^n$. Independence and stable $p$ rarely hold for repeated identical tests; use this formula to expose assumptions, not justify rerun-until-green.

## Mechanisms, Invariants, or Proof Structure

Use this testability mechanism.

1. **Name claims:** derive risky properties, scenarios, invariants, contracts, and failure behavior.
2. **Map experiments:** identify initial states, stimuli, dependencies, outcomes, oracles, and evidence boundaries.
3. **Create control:** expose domain-safe seams for state, time, randomness, identity, configuration, scheduling, and faults.
4. **Create observation:** expose boundary outcomes, causal identities, state transitions, and privacy-safe diagnostics.
5. **Isolate:** separate data, resources, tenants, clocks, dependencies, and cleanup ownership.
6. **Select fidelity:** choose models, doubles, real integrations, environments, and human review according to the claim.
7. **Exercise adversity:** test invalid, delayed, duplicate, missing, reordered, overloaded, failed, recovery, and migration behavior.
8. **Protect controls:** authorize and constrain debug, reset, fault, synthetic, and production experiment capabilities.
9. **Record evidence:** preserve exact setup, versions, stimuli, observations, oracle, result, and limitations.
10. **Improve feedback:** diagnose flakiness and cost, remove accidental coupling, and reassess untestable claims.

The governing invariants are requirement-derived claims, permitted control, boundary observation, sound oracle, isolated state, faithful seams, bounded nondeterminism, protected test authority, reproducible evidence, and no overclaim beyond tested conditions.

## Alternatives and Trade-Offs

**Real dependency or double.** A real dependency improves selected fidelity but adds availability, state, cost, speed, and diagnosis concerns. A double improves control and edge coverage but can drift semantically. Contract and selected real integration tests connect them.

**Black-box or structural observation.** Boundary tests protect behavior and replacement. Internal observation localizes failures and checks mechanisms. Excess structural coupling makes harmless refactoring break tests; too little internal evidence can hide violated invariants.

**Shared or isolated environment.** Sharing reduces infrastructure cost and may expose interference. Isolation improves reproducibility and safety but costs provisioning time and can differ from integrated reality. Use isolated tests plus governed shared-system evidence.

**Virtual or real time.** Virtual time makes timers fast and deterministic but covers only participating clocks and schedulers. Real-time tests cover integration and clock behavior but are slow and variable. Both are needed for different claims.

**Fault injection in test or production.** Test environments permit broader control with lower consequence but may miss real topology and load. Production experiments offer fidelity but require strict scope, authority, monitoring, stop, and recovery.

## Failure Modes and Misconceptions

- **“High coverage means testable.”** Execution without a discriminating oracle may prove little.
- **“Private methods should be exposed for tests.”** Prefer controlling inputs and observing owned behavior.
- **“Mocks prove integration.”** They prove expectations about the mock interaction model.
- **“A staging environment is production-like.”** Versions, data, scale, identity, and failures may differ materially.
- **“Sleep makes async tests reliable.”** It creates timing races and slow feedback.
- **“Rollback cleans the test.”** Messages, caches, files, and external effects may remain.
- **“A fixed seed proves determinism.”** Undeclared concurrency and environment state can still vary.
- **“Fault injection proves resilience.”** It supports only selected faults and conditions.
- **“Test endpoints are harmless when undocumented.”** Attackers do not depend on documentation.
- **“Re-run until green handles flakiness.”** It discards evidence and hides false passes.
- **“More end-to-end tests are always safer.”** Slow, broad, weakly diagnosed tests can reduce feedback trust.
- **“Passing tests prove correctness.”** They prove observed results for tested cases and oracles.

## Worked Examples

### Example 1

**Question:** An expiry policy reads the wall clock directly. How should architecture make boundary dates testable?

**Reasoning:** Depend on a clock capability whose contract distinguishes civil instants and elapsed duration as required. Production supplies the governed clock; tests supply dates, zones, daylight changes, leap-related boundaries, and backward wall-clock adjustment. Keep the seam inside dependency construction, not an unauthenticated runtime endpoint.

**Conclusion:** Explicit time control makes edge states reachable without weakening production authority.

### Example 2

**Question:** Two internal states emit the same status, but one will charge a card on the next `confirm` and the other will not. Are they observable for that claim?

**Reasoning:** They are not immediately distinguishable through the status output. Apply the permitted `confirm` sequence in an isolated environment and observe the authoritative payment command or resulting state. If no safe observation exists, add semantic state or causal evidence rather than exposing arbitrary internals.

**Conclusion:** Observability is relative to the claim and may require an experiment sequence.

### Example 3

**Question:** Can a payment mock prove idempotency with a real provider?

**Reasoning:** It can verify client behavior against the modeled contract, including repeated identities and unknown outcomes. It cannot prove provider key scope, retention, settlement, webhook ordering, or failure semantics. Add provider contract examples, sandbox checks where representative, selected authorized integration, and reconciliation monitoring.

**Conclusion:** Double fidelity must be matched to the specific claim.

### Example 4

**Question:** A database transaction is rolled back after each test, but messages are published before rollback. Are tests isolated?

**Reasoning:** No. Consumers can process messages whose originating state disappeared, and later tests observe side effects. Use a transactional outbox or controlled publisher, unique namespaces, consumer reset, causal completion, and bounded cleanup. Verify interrupted cleanup and duplicate delivery.

**Conclusion:** Isolation must cover every side-effect boundary, not one database connection.

### Example 5

**Question:** How should a dependency-timeout fault be injected?

**Reasoning:** Target the owned client or controlled proxy; specify affected operation, delay distribution, duration, load, environment, authorization, blast radius, stop condition, observation, and cleanup. Verify deadline propagation, retry bounds, idempotency, degradation, recovery, and evidence. Do not silently slow a shared production path.

**Conclusion:** Fault injection is a governed experiment with a bounded claim.

### Example 6

**Question:** A suite sleeps five seconds before checking an asynchronous export. What is a better design?

**Reasoning:** Submit with a stable operation identity, observe pending and terminal state through an owned interface or event, wait until a bounded deadline, and emit diagnostic progress on failure. With virtual time, advance only after every relevant timer is registered. Test late, duplicate, missing, and canceled work.

**Conclusion:** Condition-based observation replaces arbitrary delay and improves diagnosis.

### Example 7

**Question:** A configuration has two databases, three cache modes, and four identity modes. How many full combinations exist?

**Reasoning:** $2\times3\times4=24$. Pairwise selection may reduce cases and find many interaction defects, but it does not prove higher-order interactions safe. Use risk, constraints, production frequency, and failure consequences to select additional combinations.

**Conclusion:** Combinatorial techniques manage evidence cost; they do not erase untested interactions.

### Example 8

**Question:** One run independently detects an intermittent defect with probability 0.1. What is the modeled chance of at least one detection in 20 runs?

**Reasoning:** $1-(1-0.1)^{20}=1-0.9^{20}\approx0.8784$, or 87.84%. Repeated identical runs often share schedule and environment, so independence is doubtful. Fix controllability and capture schedules rather than normalizing reruns.

**Conclusion:** Probability arithmetic exposes the weakness of flaky evidence rather than legitimizing it.

### Example 9

**Question:** Should an administrative `reset-all` endpoint exist so system tests can clean state?

**Reasoning:** Not as an ordinary deployed capability. Prefer isolated ephemeral environments or scoped deletion by test namespace. If governed reset is genuinely required, restrict environment, identity, objects, rate, approval, audit, confirmation, and fail-safe behavior, and verify it cannot address production.

**Conclusion:** Test control must not become destructive ambient authority.

### Example 10

**Question:** How should testability be designed for an infusion-pump control system?

**Reasoning:** Expose verified simulation and hardware-in-the-loop boundaries for commands, sensors, alarms, timing, power, network, occlusion, and recovery. Preserve production safety interlocks, authenticate test modes, make mode conspicuous, and prevent clinical deployment with unsafe controls. No external clinical, medical-device, safety, regulatory, cybersecurity, hardware, human-factors, statistical, or practitioner review is claimed; named qualified authorities must own hazards, oracles, physical evidence, release, and residual risk.

**Conclusion:** High-consequence testability enables realistic evidence without creating a path around safety.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) owns code-level seams, responsibility design, and refactoring.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns testing theory, techniques, automation, statistics, and quality governance.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns pipelines, environments, release evidence, incidents, and production experiments.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) owns clocks, scheduling, isolation, processes, and resource mechanisms.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns authorized adversarial testing and control assurance.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns nondeterminism, partial failure, ordering, replication, and distributed testing mechanisms.

## References

1. Robert V. Binder. *Testing Object-Oriented Systems: Models, Patterns, and Tools*. Addison-Wesley, 1999. Controllability, observability, test design, and architecture for testing.
2. Gerard Meszaros. *xUnit Test Patterns: Refactoring Test Code*. Addison-Wesley, 2007. Test doubles, fixtures, isolation, setup, teardown, and test smells.
3. Michael Feathers. *Working Effectively with Legacy Code*. Prentice Hall, 2004. Seams, dependency control, characterization, and safe change.
4. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. Testability scenarios, control and observation tactics, and architectural trade-offs.
5. Martin Fowler. [“Mocks Aren't Stubs.”](https://martinfowler.com/articles/mocksArentStubs.html), January 2007. Test-double terminology and classical versus mockist styles; consulted 2026-09-05.
6. OWASP Foundation. [Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/), version 5.0.0, May 2025. Security-verification requirements and coverage; consulted 2026-09-05.
7. ISO/IEC/IEEE. [ISO/IEC/IEEE 29119-2:2021, Software and systems engineering—Software testing—Part 2: Test processes](https://www.iso.org/standard/79428.html), edition 2, December 2021. Organizational and project test processes; consulted 2026-09-05.
8. Jez Humble and David Farley. *Continuous Delivery*. Addison-Wesley, 2010. Deployment pipelines, environments, test automation, release, and feedback.

## Exercises

### Exercise 1

Define a testability scenario for verifying order cancellation after a payment timeout and delayed provider callback.

### Exercise 2

For feedback components 12 s setup, 8 s execution, 15 s observation, and 25 s diagnosis, compute total feedback time and identify which architectural evidence could reduce the largest term.

### Exercise 3

Diagnose a suite with a shared tenant, direct wall-clock use, random IDs without saved seeds, provider mocks only, ten-second sleeps, broad reset credentials, rerun-until-green policy, and full customer data in logs.

### Exercise 4

Compare a stub, semantic fake, provider sandbox, and controlled production observation for verifying a messaging provider. Address control, fidelity, isolation, cost, risk, and oracle limits.

### Exercise 5

Design testability assurance for an unfamiliar municipal floodgate-control network. Separate automated checks, simulation, physical and operational exercises, qualified authority, and blockers.

## Answers to the Exercises

### Answer 1

From a valid authorized order with stable operation identity, cause the payment request to time out while the provider later reports success. Control provider timing and callback identity through a faithful simulator or authorized test boundary. Observe order, payment, cancellation, inventory, refund or compensation, notification, audit, and reconciliation outcomes through owned interfaces. The oracle requires no double charge or refund, one authoritative terminal disposition, preserved financial trace, bounded pending time, and correct user communication.

Record versions, policy, initial state, exact schedule, callback, retries, events, final state, and limitations. Exercise provider success, failure, unknown, duplicate, reordered, late-after-cancel, and callback-loss paths. A mock interaction alone is insufficient; selected provider contract and reconciliation evidence must support external semantics.

### Answer 2

$$
T_f=12+8+15+25=60\text{ seconds}.
$$

Diagnosis is the largest term at 25 seconds. Stable operation and causation identities, semantic state transitions, expected-versus-actual oracle output, dependency observations, saved seed and schedule, version and configuration, and privacy-safe structured diagnostics can reduce it. Observation at 15 seconds may also shrink through condition-based terminal-state signals rather than polling or sleeps. Optimize based on repeated evidence; adding verbose uncorrelated logs may increase diagnosis time and privacy risk.

### Answer 3

The shared tenant permits interference. Hidden time prevents boundary control. Unsaved seeds prevent replay. Provider mocks can drift from real semantics. Sleeps create races and slow feedback. Broad reset authority is destructive and may reach the wrong environment. Rerun-until-green discards failures and hides false passes. Customer logs create an unauthorized sensitive-data copy.

Use isolated namespaces or environments, explicit clocks, recorded seeds and schedules, semantic fakes plus contract and selected integration evidence, condition-based observation, scoped idempotent cleanup, and strict environment and identity boundaries. Quarantine only with owner and expiry while diagnosing each flaky class. Generate synthetic minimal data, redact before emission, constrain access and retention, and test that test controls cannot address production.

### Answer 4

A stub cheaply produces selected responses and errors but models little state. A semantic fake can exercise deduplication, ordering, callback, and state transitions deterministically, but its implementation may disagree with the provider. A provider sandbox covers actual protocol and some behavior, but may differ in scale, policy, timing, failure, and settlement and creates external state and availability. Controlled production observation offers strongest environmental fidelity for real traffic but lowest control and highest privacy, safety, and operational consequence.

Layer them by claim: stubs for caller branches, a fake for property and adverse schedules, shared contract cases and sandbox for integration, and privacy-safe production indicators for observed outcomes. Define oracle, identities, data, external-write authority, cleanup, quotas, cost, failure, evidence retention, and limitations at every layer. Never inject unapproved production messages merely for fidelity.

### Answer 5

Define commands, sensor inputs, water levels, gate positions, timing, authority, power, communication, local safe states, manual control, alarms, and recovery. Create bounded seams for simulated sensors, clocks, networks, power, and actuator feedback while preserving authentication and safety interlocks. Expose semantic state and causal evidence without allowing remote test mode to bypass physical authority.

Automation can verify protocol, units, state machines, authorization, configuration, command identity, timing bounds, duplicate and stale rejection, alarms, logs, and evidence freshness. Simulation can explore rainfall, sensor fault, network partition, delayed command, power loss, and recovery. Hardware-in-the-loop and controlled field exercises must validate actuator behavior, hydraulics, communication, manual procedures, safe stop, restoration, and cleanup under qualified supervision.

No external hydrology, civil, environmental, emergency-management, safety, regulatory, cybersecurity, hardware, human-factors, statistical, or practitioner review is claimed. Named qualified authorities must own hazard analysis, physical models, oracles, test authorization, release, and residual risk. Unauthenticated test control, unverified safe-state behavior, missing physical evidence, ambiguous manual authority, failed cleanup or recovery, or unresolved high-severity hazard blocks readiness.
