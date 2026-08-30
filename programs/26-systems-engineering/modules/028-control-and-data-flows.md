---
module_id: SYSENG-028
program: Systems Engineering
level: 1
module_number: 28
title: Control and Data Flows
status: complete
last_verified: 2026-08-31
---

# Control and Data Flows

## One-Page Review

### Governing question

How can a team specify control and data flows among logical elements so that causality, authority, meaning, time, ordering, quality, and failure behavior are analyzable—without treating a labeled arrow, matching schema, or successful nominal message exchange as proof of correct end-to-end behavior?

### Essential definitions

- A **flow** is a directed transfer or availability relationship for a typed item, event, signal, command, observation, state, or other interaction under stated conditions.
- A **data flow** conveys information consumed as an input, evidence, state representation, query/result, event fact, or recorded outcome.
- A **control flow** enables, inhibits, selects, synchronizes, authorizes, prioritizes, interrupts, or changes the execution or mode of behavior.
- A **trigger** is a control occurrence whose satisfaction can initiate or advance behavior; it is not necessarily a command.
- A **command** is an intentional request from an authorized source to produce an effect, subject to acceptance and execution semantics.
- An **event** represents an occurrence of interest; an event notice is data about that occurrence and may arrive late, duplicated, reordered, or not at all.
- A **flow item** is the typed thing transferred, including payload, identity, units, classification, version, provenance, and quality metadata.
- A **flow contract** defines producer, consumer, direction, semantics, applicability, timing, ordering, cardinality, quality, authority, security, failure, and evidence.
- **Freshness** bounds the acceptable age of information relative to its observation or validity time, not merely its receipt time.
- **Provenance** records origin, transformations, configuration, time basis, and custody needed to interpret and trust an item.
- **backpressure** is the mechanism by which a downstream capacity limit constrains upstream production or admission.
- **flow closure** means every required input/control is supplied, every output is consumed or intentionally external, and paths compose into required scenario outcomes without unexplained sources, sinks, or cycles.

### Central model, mechanism, or theorem

Represent the logical flow architecture as a typed directed multigraph:

\[
G_F=(L,E),\qquad
e=\langle id,s,t,k,x,g,m,\tau,o,q,a,f,v\rangle,
\]

where (L) is logical elements; source (s) and target (t); kind (k\in\{data,control,command,event,query,response\}); item contract (x); guard/trigger (g); mode/configuration (m); timing (\tau); ordering/cardinality (o); quality/provenance (q); authority/security (a); failure/backpressure (f); and version/evidence (v).

For an input or control port (p), compatibility requires more than type:

\[
Compatible(e,p)=Direction\land Meaning\land Type\land Unit\land Range\land
TimeBasis\land Freshness\land Ordering\land Cardinality\land Quality\land
Authority\land Security\land Mode\land Version\land FailureSemantics.
\]

A flow architecture is acceptable only conditionally when graph well-formedness, semantic compatibility, behavioral closure, temporal/resource feasibility, failure containment, and empirical evidence all hold for the named configurations and scenarios.

### Critical invariants

- Every flow has stable identity, source, target, direction, kind, item semantics, mode/configuration, rationale, owner, and version.
- Control and data roles remain explicit even when one physical message carries both; payload presence does not imply authority to act.
- Every required function input and enabling condition has a justified source; every output has an intended consumer, store, effect, or external sink.
- Producer and consumer agree on meaning, units, ranges, reference frames, time bases, quality, classification, version, and failure behavior.
- Commands identify authority, acceptance, rejection, acknowledgement, execution, completion, cancellation, idempotency, and safe timeout semantics.
- Events identify occurrence identity, event time, detection time, publication time, ordering scope, duplication, loss, replay, and correction semantics.
- State synchronization identifies authority, snapshot/delta rules, consistency, conflict resolution, reconciliation, deletion, and recovery.
- Timing analysis includes sampling, detection, computation, queues, transport, scheduling, actuation, retries, and clock uncertainty.
- Capacity analysis includes rates, burst, size, fan-out, buffering, priority, backpressure, overload policy, and recovery.
- Feedback loops state sign, delay, sampling, stability assumptions, saturation, initialization, and degraded behavior.
- Security/privacy controls protect semantics and authority across trust boundaries without destroying required availability or observability.
- Static and executable model checks remain bounded by encoded assumptions; integrated realization and operational evidence remain necessary.

### Common failures

Failures include drawing bidirectional arrows without separate contracts; naming a flow `data`; confusing an event occurrence with its notification; treating a flag as both observation and authorization; relying on receipt time as event time; omitting units, frames, or uncertainty; assuming exactly-once delivery; using acknowledgements without defining what they acknowledge; allowing retries to repeat non-idempotent effects; broadcasting commands without authority; sharing state through snapshots with no owner; ignoring queue saturation; dropping safety traffic with ordinary telemetry; creating unbounded fan-out; closing feedback loops without delay analysis; using sequence numbers with no reset/epoch rule; accepting stale but authentic commands; encrypting without key/recovery lifecycle; and claiming a diagram is complete because all ports are connected.

### Compact example

A cold-storage controller receives temperature observations and a door-state event, issues compressor commands, and publishes health evidence. Each observation carries sensor identity, °C unit, calibration version, observation time, uncertainty, validity interval, and quality flags. `Door open` is data about an occurrence; it changes control behavior only through a governed policy. A compressor command identifies authorized issuer, target, setpoint/range, command ID, expiry, preconditions, acknowledgement meaning, cancellation, and safe failure. The control loop budget includes sampling, sensing, transport, decision, queue, actuation, and thermal response. Duplicate observations may be harmless; duplicate `start compressor` commands require idempotency. Loss of network triggers a bounded local control mode. A diagram can document these flows, but chamber tests and fault injection are still needed to establish behavior of the realized system.

### Connections

SYSENG-021–025 define transformations, functional flow, state/mode, and scenarios. SYSENG-026 defines logical elements, and SYSENG-027 allocates functional contributions to them. This module specifies the interactions created by those allocations. SYSENG-029 compares architecture alternatives; SYSENG-030 checks logical-architecture completeness and consistency. Later interface, physical architecture, performance, safety, security, verification, operations, and configuration modules refine and test these contracts. API, platform, data, object-oriented, and functional programs encounter the same semantics in requests, events, streams, state, effects, and feedback.

## Governing Question

How should control and data flows be modeled and governed so that a reviewer can determine what may cause what, which information is valid for which decision, who has authority, whether timing/capacity close, and how the system behaves when transfers are late, duplicated, reordered, corrupted, absent, or malicious?

The answer is a portfolio of typed contracts and scenario evidence, not a prettier arrow diagram. Define exact items and causal roles, preserve producer/consumer meaning, qualify by mode and configuration, allocate time and capacity, expose state and feedback, state abnormal behavior, and verify the selected realization under representative conditions.

## Why This Matters

Logical elements collaborate through flows. If those flows are ambiguous, the architecture cannot preserve function allocation. A consumer may interpret Celsius as Fahrenheit, receipt time as observation time, an untrusted event as a command, an acknowledgement as completion, or a snapshot as authoritative state. Each error can exist while types match and messages arrive successfully.

SEBoK 2.14 distinguishes function input/output flows from control flows and describes behavioral architecture in terms of sequencing, conditions, data/control flow, modes, and temporal properties. NASA’s current Logical Decomposition guidance asks teams to describe function inputs, outputs, failures, consequences, and interfaces and to trace end-to-end paths. NASA’s interface outline calls for responsibility, units, tolerances, software/data, signal, power, material, and other interface detail. OMG SysML 2.0 supplies formal modeling constructs for ports, directed features, connections, and transfers. ISO/IEC/IEEE 42010:2022 frames architecture descriptions around stakeholder concerns and viewpoints. These sources enable precise modeling but do not make a notation, connector, or tool execution sufficient assurance.

Flow design determines emergent system qualities. A new boundary introduces latency and failure. A fan-out multiplies load and disclosure. A shared event stream couples retention and schema evolution. A command path establishes authority and hazard exposure. A feedback loop can oscillate. A retry can duplicate a physical effect. Consequently, every arrow is an engineering claim about semantics and behavior.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. a function transforms typed inputs into outputs subject to controls, preconditions, modes, timing, and failures;
2. FFBDs express precedence and control logic but do not fully specify interface semantics;
3. state and mode models define legal behavior and transitions;
4. scenarios supply end-to-end nominal, alternate, degraded, recovery, and misuse paths;
5. logical components own responsibilities, state/policy, and provided/required interactions;
6. function allocation creates boundary crossings that require interface contracts;
7. end-to-end timing, reliability, safety, security, and privacy arise from composition;
8. models and tests support claims only within their encoded and observed conditions.

As a retrieval test, inspect an arrow `Sensor -> Controller: pressure`. Ask whether it is a sampled value, threshold event, stream, query result, or shared state; absolute or differential pressure; unit and reference; observation time; uncertainty and calibration; rate and burst; loss/duplicate behavior; validity duration; quality flags; security classification; and degraded-mode use. Until answered, the arrow is a prompt, not a contract.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish data, control, command, event, query/response, state-synchronization, material, energy, and resource interactions;
2. specify a typed logical flow contract independent of physical transport;
3. separate occurrence, observation, notification, decision, authorization, command, execution, acknowledgement, and outcome;
4. define semantic compatibility using units, frames, time, quality, provenance, authority, modes, and versions;
5. analyze ordering, cardinality, idempotency, cancellation, replay, and state consistency;
6. allocate latency, capacity, buffers, priorities, and backpressure across end-to-end paths;
7. reason about feedback loops, sampling, delay, saturation, and degraded control;
8. allocate security, privacy, safety, and evidence obligations to flow endpoints and boundaries;
9. challenge flow architectures with fault, overload, timing, trust, and lifecycle scenarios;
10. combine bounded static checks, simulation, testing, and operational measurements into a defensible assurance argument.

## Core Exposition

**Frame the flow viewpoint.** Identify system and architecture level, stakeholder concerns, decisions, modes, configurations, scenarios, logical elements, allocated functions, physical assumptions deliberately excluded, modeling semantics, and evidence threshold. A timing viewpoint and an information-authority viewpoint can show the same flows differently; stable identifiers connect them.

**Start from behavior, not connections.** Walk each controlled scenario and allocation. For every function contribution, list required inputs, enabling/inhibiting controls, produced outputs, state reads/writes, resource use, commands, events, and evidence. Then identify which items cross logical boundaries. Drawing connections first tends to preserve current technology and omit abnormal behavior.

**Distinguish flow roles.** Data supplies information. A control enables, inhibits, selects, synchronizes, interrupts, or changes mode. A command is an authorized request for effect. An event reports an occurrence. A query asks for information; its result does not inherently authorize action. A state update claims a change to governed state. The same encoded message may contain several roles, but the contract names each so consumers do not infer authority from format.

**Separate occurrence from report.** A door physically opens at event time. A sensor detects it later; a component publishes a notice later still; a consumer receives and processes it after further delay. Record occurrence identity and these time points where relevant. “Latest message” can be older than current reality after partitions, retries, or clock errors.

**Define the item semantically.** Give stable identity, domain meaning, schema/type, fields, units, range, reference frame, precision, resolution, uncertainty, encoding, classification, optionality, invariants, invalid/unknown states, and version. A numerical field named `heading` is ambiguous without true/magnetic reference, degrees/radians, wrapping, coordinate convention, and validity.

**Record provenance and quality.** State original source, transformations, calibration/configuration, observation time, custody, quality indicators, uncertainty, and integrity evidence. Consumers define which quality conditions permit which uses. A low-confidence estimate might support display but not autonomous actuation. Provenance is an interpreted chain, not a decorative source string.

**Define source, target, and direction.** Use distinct flows for opposite directions unless their contracts genuinely match. Identify producer responsibility for valid publication and consumer responsibility for validation/use. Multicast names each intended audience or an eligibility rule. External actors and environments remain explicit boundary endpoints.

**Qualify applicability.** State mode, state, configuration, variant, jurisdiction, mission interval, and guard. A maintenance command may be illegal during operation; a degraded estimate may be valid only below a rate limit. Verify that transitions enable and disable flows coherently and clear or revalidate queued items.

**Specify triggers and guards.** A trigger identifies the occurrence or condition that makes behavior eligible. A guard is evaluated from authoritative, sufficiently fresh state. Define edge/level behavior, debounce, hysteresis, simultaneity, priority, re-entry, and missed-trigger handling. A Boolean `start=true` without epoch or transition semantics can retrigger indefinitely.

**Specify command lifecycle.** Define issuer authority, target, command identity, parameters, preconditions, validity/expiry, admission, rejection reasons, queueing, execution, completion, cancellation, compensation, acknowledgement, audit, and retry. Distinguish accepted, started, physically effected, completed, and outcome verified. An HTTP success or bus acknowledgement may prove only receipt.

**Specify event semantics.** Define occurrence identity, aggregate or entity scope, event time, publisher time, ordering domain, partition key, duplication, loss, replay, late arrival, correction/retraction, retention, and consumer checkpoint. “Exactly once” is usually an end-to-end effect claim requiring producer, transport, consumer, and state semantics—not a transport label.

**Specify query/response semantics.** State snapshot time, consistency, filters, pagination, authorization, partial results, timeout, cache/staleness, and error distinctions. A retry may observe a different state. If a response drives a critical decision, record its validity horizon and provenance rather than assuming synchronous freshness.

**Specify state synchronization.** Identify the semantic owner and whether transfers are snapshots, deltas, logs, commands, or derived views. Define version/epoch, causality, consistency, conflict detection/resolution, tombstones/deletion, compaction, bootstrap, partition, reconciliation, and recovery. Bidirectional replication without authority rules creates conflicting truth.

**Model ordering and concurrency.** State whether order is total, per source, per entity, causal, priority-based, or unconstrained. Define simultaneous/conflicting commands, races, and join conditions. Sequence numbers need scope, width, wrap, restart epoch, persistence, and comparison rules. Timestamps alone do not establish causality under uncertain clocks.

**Model cardinality and idempotency.** Define zero/one/many occurrences, duplication tolerance, deduplication identity/window/store, and repeated-effect semantics. An idempotency key prevents duplicate effect only within its governed scope and retention. Physical operations may require feedback to establish whether a timed-out command already acted.

**Model cancellation and compensation.** Cancellation may race with start or completion. State when it is accepted, what can still happen, how consumers learn the terminal outcome, and how partial effects are made safe. Compensation is a new domain action with its own failures, not a time reversal.

**Allocate latency.** Define end-to-end deadline and measurement points. Include sampling, sensing, batching, detection, computation, queueing, serialization, transport, scheduling, consumer processing, actuation, physical response, retry, and clock uncertainty. Use sums for serial paths, maxima for parallel joins, and conditional distributions or response-time analysis when bounds are not simple.

**Allocate throughput and capacity.** Record mean and peak rate, burst envelope, item size, fan-out, concurrency, service rate, buffer, priority, admission, backpressure, shedding, persistence, and recovery drain. Stable average rate does not prevent burst overflow. A finite buffer delays loss; it does not remove a sustained capacity deficit.

**Define backpressure and overload policy.** Decide whether producers slow, block, buffer, aggregate, sample, reject, shed, or degrade. Prioritize by stakeholder consequence, not implementation convenience. Preserve critical control and evidence where required, while bounding memory, stale work, retry storms, and starvation.

**Analyze feedback.** Identify controlled variable, observation, error, controller, command, actuator, plant/environment, disturbances, sampling, delays, sign, gains or policy, saturation, anti-windup, stability basis, safe state, and monitoring. Logical flow review cannot prove physical stability, but it must expose the loop and its assumptions for analysis and test.

**Treat time as data and infrastructure.** Define clock source, synchronization, accuracy, precision, monotonic versus civil time, leap/discontinuity behavior, timestamp origin, and uncertainty. Compare times only when their bases and error permit. Safety deadlines may need local monotonic measurement even when audit requires civil time.

**Handle unknown, invalid, and absent values.** Absence can mean no event, lost message, unavailable source, filtered data, or not-yet-initialized state. Model these separately. Avoid magic numbers. Define validation, quarantine, substitution, degraded use, alarm, and recovery for out-of-range, inconsistent, stale, or unauthenticated items.

**Allocate safety obligations.** Identify hazardous commands, permissives, inhibits, interlocks, safe-state signals, independent observations, and response evidence. Validate control authority at the effect boundary. Analyze stale/replayed commands, conflicting sources, common-cause data, missed events, and failure of the monitoring path.

**Allocate security and privacy.** Define identities, authentication, authorization, integrity, confidentiality, anti-replay, freshness, least privilege, classification, minimization, retention, deletion, audit, key/policy lifecycle, and incident response. Authentic data can still be stale, semantically invalid, overprivileged, or unsafe. Encryption can increase latency and complicate recovery; budget it.

**Protect semantic availability.** Availability is not merely bytes arriving. A consumer needs sufficiently fresh, interpretable, authorized, quality-bounded information. Define degraded semantics, cached validity, alternate sources, local autonomy, and recovery reconciliation. Do not convert a communication outage into silent use of indefinite stale state.

**Define observability without circular proof.** Allocate records for input acceptance, transformations, decisions, commands, effects, rejection, timing, configuration, and faults with provenance and integrity. A component’s self-report is useful but may not independently establish its effect. Correlate boundary evidence and physical observations where consequence requires.

**Manage schema and semantic evolution.** Version meaning, not only serialization. State compatibility direction, defaults, unknown fields, enum extension, unit changes, deprecation, coexistence, migration, rollback, and evidence applicability. A consumer that parses a message may still misinterpret a changed field.

**Preserve logical/physical separation.** Logical contracts say what must be exchanged and under what qualities. Later realization selects shared memory, human communication, network protocol, electrical signal, fluid line, or mechanism. Genuine constraints such as propagation delay or regulatory protocol may enter early, but label them as constraints and preserve the logical intent.

**Review paths, cuts, and cycles.** Trace end-to-end sources to sinks, controls to effects, and evidence back to outcomes. Find missing sources, orphan sinks, unintended fan-out, single points of failure, trust crossings, cycles, and bypasses. Graph reachability is necessary but does not validate semantics.

**Verify progressively.** Use metamodel constraints and static checks for identity, direction, type, port, mode, ownership, and budget declarations. Execute models for ordering and state behavior. Simulate timing, capacity, and control. Test interfaces with valid, boundary, invalid, stale, duplicate, reordered, lost, and malicious items. Perform load, fault, security, human, hardware-in-loop, and integrated system tests as appropriate. Monitor operational distributions and revise assumptions.

**Govern the baseline.** Control flow/item/interface versions, sources/targets, scenarios, modes, budgets, authorities, rationale, assumptions, tests, and waivers. A change to producer meaning, clock, rate, retention, authority, or physical path can invalidate consumers and evidence. Traverse impact before approval and retain rollback/reconciliation plans.

The following checker finds selected declaration defects in five flow records. It cannot establish semantic or physical correctness.

<!-- bijux-verify: {"id":"flow-contract-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"flows_total=5\nwell_formed_declared=1\nmissing_kind=FL-002\nmissing_item=FL-003\nmissing_timing=FL-004\nmissing_failure=FL-005\nunresolved=FL-002,FL-003,FL-004,FL-005\nevidence=declared_fields_only\n","stderr":""}} -->
```python
flows = [
    {"id": "FL-001", "kind": "observation", "item": "temperature estimate °C",
     "timing": "age <= 2 s", "failure": "enter bounded local mode"},
    {"id": "FL-002", "kind": "", "item": "door occurrence",
     "timing": "publish <= 100 ms", "failure": "infer from independent contact"},
    {"id": "FL-003", "kind": "command", "item": "",
     "timing": "expires after 1 s", "failure": "reject stale command"},
    {"id": "FL-004", "kind": "event", "item": "compressor disposition",
     "timing": "", "failure": "retain pending outcome"},
    {"id": "FL-005", "kind": "evidence", "item": "decision record",
     "timing": "retain 30 days", "failure": ""},
]
required = ("kind", "item", "timing", "failure")
valid = [flow for flow in flows if all(flow[field] for field in required)]
print(f"flows_total={len(flows)}")
print(f"well_formed_declared={len(valid)}")
for field in required:
    print(f"missing_{field}=" + ",".join(flow["id"] for flow in flows if not flow[field]))
print("unresolved=" + ",".join(flow["id"] for flow in flows if flow not in valid))
print("evidence=declared_fields_only")
```

FL-001 can still be wrong: the record does not prove correct sensor provenance, uncertainty, sampling, authority, capacity, controller behavior, or chamber performance.

## Definitions and Notation

Let (L) be logical elements, (P) ports, (E) flow edges, (X) flow-item types, (M) modes/configurations, and (S) scenarios. A connection relation (C\subseteq P\times P) states potential interaction; an item-flow relation (E\subseteq P\times P\times X\times M) states what is intended to flow in a usage context. Connection does not imply occurrence, delivery, acceptance, or correct effect.

For an item occurrence (x_i), distinguish:

\[
t_o\leq t_d\leq t_p\leq t_r\leq t_c,
\]

where (t_o) is occurrence/observation time, (t_d) detection, (t_p) publication, (t_r) receipt, and (t_c) consumption. Freshness at consumption is (A=t_c-t_o), with combined clock uncertainty included. Transport latency (t_r-t_p) alone cannot establish freshness.

For a serial path with stage bounds (b_i), boundary/queue bounds (d_j), clock allowance (u), and reserve (r):

\[
T=\sum_i b_i+\sum_j d_j+u+r\leq D.
\]

For a finite buffer of (B) items, arrival rate (\lambda), and service rate (\mu), sustained (\lambda>\mu) is infeasible: under a deterministic approximation, overflow occurs no later than (B/(\lambda-\mu)) after the overload begins. Real burst and service distributions require stronger queueing or simulation evidence.

For duplicate-tolerant effects, define deduplication key (k), scope (s), retention window (w), and atomic relation between effect and recorded key. “Idempotent” without those semantics is incomplete.

## Mechanisms, Invariants, or Proof Structure

Use a flow-assurance loop:

1. **Frame:** control system/viewpoint, scenarios, modes, allocations, logical boundaries, concerns, constraints, notation, and evidence threshold.
2. **Inventory:** enumerate inputs, controls, outputs, state, commands, events, queries, evidence, material/energy/resource flows, and cross-boundary interactions.
3. **Contract:** define meaning, source/target, direction, item, time, quality, order, cardinality, authority, security/privacy, failure, version, and ownership.
4. **Compose:** trace causal paths and feedback; analyze modes, state, timing, capacity, backpressure, common cause, and end-to-end outcomes.
5. **Challenge:** inject absence, delay, duplication, reordering, corruption, stale/replayed/malicious input, overload, clock faults, partial recovery, and concurrent authority.
6. **Verify:** apply static checks, execution, simulation, interface/load/fault/security/human/integration tests, and operational measurement proportional to consequence.
7. **Govern:** baseline exact endpoints/contracts/evidence, traverse changes, manage coexistence and rollback, and revalidate affected scenarios.

The assurance argument links requirement and scenario sources to allocated functions; functions to ports and flow contracts; flow contracts to timing/capacity/fault/security analyses; and those claims to configuration-specific evidence. Its conclusion is bounded: the architecture is consistent and feasible for named conditions—not that connected arrows guarantee system behavior.

## Alternatives and Trade-Offs

**Synchronous request/response versus asynchronous event.** Synchronous interaction can simplify immediate error handling but couples availability and latency. Events decouple time and support fan-out, but introduce ordering, duplication, retention, eventual-state, and outcome-ownership obligations.

**Command versus desired-state flow.** Commands request transitions and require lifecycle semantics. Desired state can simplify convergence and retry but needs authoritative versions, reconciliation, and conflict rules. Neither eliminates acknowledgement and observation of actual effect.

**Push versus pull.** Push can reduce detection delay and support streaming; it can overload consumers. Pull gives consumers rate control but may increase staleness and synchronized polling. Hybrid notification-plus-query adds consistency and race questions.

**Central bus versus explicit peer flows.** A bus can standardize transport and observability, but logical producers, consumers, authorities, and semantics must remain visible. Peer contracts can clarify ownership but multiply integration surfaces. Topic names do not replace interface definitions.

**Snapshot versus delta/log.** Snapshots ease bootstrap but can be large and lose causality. Deltas/logs preserve change history but need ordering, retention, compaction, missing-entry recovery, and snapshot reconciliation.

**Lossless buffering versus bounded shedding.** Persistence protects work but increases delay and stale backlog. Shedding bounds resources but requires consequence-aware priority and disclosure. Critical control may need separate capacity and failure behavior.

**Central versus local control.** Central control can coordinate globally but depends on communication and central availability. Local control improves response and degraded autonomy but needs policy synchronization, authority boundaries, and stable rejoin.

## Failure Modes and Misconceptions

- **Arrow-as-contract:** a line shows association but not semantics. Add the governed flow record.
- **Type-only compatibility:** matching schemas hide unit, frame, time, quality, authority, and version mismatch.
- **Control/data conflation:** a status field silently triggers effect. Separate observation, decision, authorization, and command.
- **Notification-as-occurrence:** receipt time substitutes for event time. Preserve occurrence identity and time basis.
- **Acknowledgement ambiguity:** `ACK` could mean bytes, validation, admission, execution, or outcome. Name the state.
- **Exactly-once slogan:** transport delivery is confused with end-to-end effect. Define identity, transaction boundaries, retention, and recovery.
- **Timestamp causality:** wall-clock order is treated as causal order. Define ordering domain and clock uncertainty.
- **Unbounded retry:** failure amplification overloads dependencies or repeats effects. Bound retries and use idempotency/compensation.
- **Buffer-as-capacity:** finite storage hides sustained rate deficit until later. Analyze arrival/service rates and drain time.
- **Broadcast authority:** any subscriber can act on a message. Enforce target, identity, authorization, and purpose.
- **Snapshot truth:** replicated data is treated as authoritative indefinitely. Define owner, age, version, and reconciliation.
- **Feedback blindness:** a cycle is drawn without sign, delay, saturation, or stability reasoning.
- **Unknown-as-zero:** absence or invalidity becomes a plausible value. Model validity states explicitly.
- **Security-is-encryption:** confidentiality is added while authorization, replay, availability, provenance, and key lifecycle remain open.
- **Observability proof:** self-reported success is accepted as physical outcome. Correlate independent boundary/effect evidence.
- **Protocol-first architecture:** a transport technology drives semantics. Specify logical obligations and then select a fitting realization.

## Worked Examples

### Example 1

A freezer controller receives `temperature_estimate`. The contract adds sensor ID, °C, calibration version, observation time, uncertainty, validity of two seconds, and invalid/stale states. The controller accepts fresh estimates for automatic control, displays lower-quality estimates with warning, and enters bounded local safe behavior when no valid estimate exists. Receipt of a syntactically valid payload is not evidence of accurate temperature.

### Example 2

An actuator API returns `accepted`. Operations had interpreted it as “valve closed.” The flow model separates command received, validated, admitted, execution started, position observed, and terminal outcome. Each carries command ID and time. A timeout after admission queries disposition before retrying. This prevents duplicate physical effects and makes the evidence claim precise.

### Example 3

A flood-warning event arrives after a newer correction because two publishers use different routes. Per-region causal version and correction semantics let the consumer reject the stale warning state while retaining audit history. A wall-clock comparison alone was rejected because clock uncertainty exceeded the publication interval. Public cancellation remains a distinct authorized command and event.

### Example 4

A processing path has 40 ms sampling, 25 ms sensing, 35 ms transport, 55 ms decision, 30 ms queue, 45 ms actuation, 20 ms clock/measurement allowance, and 50 ms reserve. Total allocation is (300) ms. It exactly meets a 300 ms deadline but has no unallocated headroom; representative tail and fault measurements are required before acceptance.

### Example 5

A stream receives 140 items/s during a burst and processes 100 items/s with a 2,000-item buffer. Under the bounded deterministic approximation, net growth is 40 items/s and overflow begins within (2000/40=50) seconds if overload persists. The team adds admission, priority shedding, producer backpressure, alerting, and recovery-drain analysis rather than calling the buffer “lossless.”

### Example 6

Two door controllers exchange desired state. During a partition, one accepts `locked` and the other `maintenance-open`. On reconnection, last-write-wins would hide authority. The corrected contract gives safety lock precedence except under a locally authenticated maintenance interlock, uses an epoch/version, records reason and issuer, and defines reconciliation and physical-state verification.

### Example 7

A dosage recommendation event is authentic and schema-valid but six hours old. The consumer had checked signature but not clinical validity time, patient-context version, or supersession. The contract adds subject, observation and model versions, freshness, confidence, intended-use restriction, supersession, and mandatory clinician authority. No software test establishes clinical safety for all populations.

### Example 8

A fan-out telemetry topic adds 80 consumers. Producer output is 5 MB/s, so naive broker egress becomes 400 MB/s before replication and protocol overhead. The logical view records audience classes, aggregation, sampling, privacy purpose, retention, and priority. Architecture alternatives compare shared derived products with indiscriminate broadcast.

### Example 9

A water-level feedback loop samples every second, but variable network delay reaches four seconds and commands can queue. The logical model exposes delayed observation and stale command paths. Control analysis selects a local loop for fast safety response and a slower supervisory flow with expiry and bounded setpoints. Simulation and plant testing remain necessary for stability evidence.

### Example 10

An audit pipeline records that a policy engine “allowed” a request, yet cannot reconstruct the policy version, input provenance, clock, or downstream effect. The revised evidence flow binds decision ID, subject, inputs/digests, policy/model/configuration versions, authority, decision time, command ID, and effect disposition with privacy-aware retention. The record supports trace, but independent review is still required for consequential decisions.

## Cross-Program Connections

- **API and service engineering:** request/response, events, idempotency, retries, pagination, versioning, and error contracts instantiate logical flow concerns.
- **Platform engineering:** control planes distribute desired state, policy, credentials, and reconciliation; data planes need bounded fast-path semantics and telemetry.
- **Data engineering:** provenance, event time, watermarking, quality, schemas, lineage, retention, and correction are flow-contract properties.
- **Object-oriented programming:** method calls and messages carry control/data semantics, but runtime call structure must not be mistaken for the logical architecture.
- **Functional programming:** pure transformations clarify data dependencies; effects, time, state, streams, and external authority still require governed boundaries.
- **Security:** identity, authorization, integrity, confidentiality, anti-replay, availability, classification, and key lifecycle are endpoint and path obligations.
- **Control engineering:** sampling, delay, feedback, saturation, stability, and physical response constrain logical flow feasibility.
- **Verification:** interface conformance, scenario traces, load/fault tests, hardware-in-loop trials, and operational monitoring support different bounded claims.

## References

1. NASA, *Systems Engineering Handbook, Section 4.3: Logical Decomposition*, current web edition, updated 2023. <https://www.nasa.gov/reference/4-3-logical-decomposition/>
2. NASA, *Systems Engineering Handbook, Section 4.0: System Design Processes*, current web edition, updated 2023. <https://www.nasa.gov/reference/4-0-system-design-processes/>
3. NASA, *Systems Engineering Handbook Appendix L: Interface Requirements Document Outline*, current web edition, updated 2023. <https://www.nasa.gov/reference/system-engineering-handbook-appendix/>
4. Systems Engineering Body of Knowledge, *Logical Architecture*, SEBoK version 2.14, 2026. <https://sebokwiki.org/wiki/Logical_Architecture>
5. Object Management Group, *Systems Modeling Language Version 2.0*, formal specification, 2026. <https://www.omg.org/spec/SysML/2.0>
6. Object Management Group, *Systems Modeling Language Version 2.0, Part 1: Language Specification*, 2026. <https://www.omg.org/spec/SysML/2.0/Language/PDF>
7. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2022. <https://www.iso.org/standard/74393.html>
8. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>

## Exercises

### Exercise 1

Specify the logical flows for a remotely commanded pump: observation, control decision, command, acknowledgement, physical-effect evidence, alarm, and maintenance override. Include time, authority, duplication, cancellation, failure, and evidence limits.

### Exercise 2

A serial protection path has sampling 20 ms, sensing 35 ms, validation 25 ms, queue 40 ms, decision 55 ms, transport 30 ms, actuation 70 ms, clock allowance 15 ms, and required reserve 60 ms against a 350 ms deadline. Does the allocation close? What evidence is still required?

### Exercise 3

A consumer processes entity events using a global timestamp, retries indefinitely after timeout, and writes a non-idempotent charge before saving its checkpoint. Identify at least eight defects and propose corrected flow semantics.

### Exercise 4

An incoming stream bursts at 260 items/s for 90 seconds. Service is 200 items/s, existing backlog is 600 items, and buffer capacity is 5,000 items. Determine whether overflow occurs under a deterministic approximation, the time/capacity result, and why this is not a complete capacity proof.

### Exercise 5

Design an assurance review for moving a centralized safety-control flow to local autonomous controllers with supervisory updates. Include invariants, modes, time, feedback, authority, security, common cause, reconciliation, tests, and bounded conclusion.

## Answers to the Exercises

### Answer 1

Define a sensor observation carrying pump/line identity, measured quantity and unit, observation time, uncertainty, calibration/configuration, quality, freshness, and invalid states. A Control Decision consumes authorized fresh observations and emits a reason-coded desired action under a named policy version; it is not itself the actuator command. The command carries issuer/target identity, authority, command ID, action/parameters, preconditions, expiry, mode, and cancellation semantics. The pump returns separate received, validated/admitted, started, and terminal disposition events. Physical-effect evidence comes from governed position/flow/pressure observations, preferably with independence appropriate to consequence.

Maintenance override requires local/remote authority rules, interlocks, indication, expiry, audit, and return-to-service checks. Define duplicate command handling by ID and retention window; on ambiguous timeout, query disposition before retry. Define communication loss, stale observation, conflicting authority, actuator fault, alarm priority, and bounded local safe behavior. Model tests can check sequences and contracts; hardware/plant tests, security assessment, representative communications, operator trials, and authorized safety review remain necessary.

### Answer 2

Operational stages sum to (20+35+25+40+55+30+70=275) ms. Adding 15 ms clock allowance and 60 ms reserve gives:

\[
T=275+15+60=350\text{ ms}.
\]

The declared allocation exactly closes the deadline with no extra headroom beyond the required reserve. Acceptance still needs evidence for measurement-point consistency, worst-case sampling alignment, queue and scheduling bounds, clock uncertainty, transport behavior, actuation and physical response, concurrent load, retries, degraded modes, failure detection, and representative tail distributions or deterministic worst-case assumptions. Integrated fault tests must show the required protective outcome, not just message timing.

### Answer 3

Defects include global timestamp order without clock/causal guarantees; no per-entity ordering key; no event identity; no duplicate policy; indefinite retries; retry amplification; non-idempotent effect; checkpoint after effect without atomicity; ambiguous timeout; no expiry; no poison-event policy; no correction/retraction; and no bounded backlog or recovery semantics.

Use stable event and entity IDs, source epoch/version, event time plus uncertainty, per-entity or causal ordering, and explicit late/correction rules. Make charging idempotent under a governed key/window or atomically couple effect and processed-event record. On ambiguity, query disposition before retry. Bound retries with backoff/jitter and terminal handling; define expiry, authorization, validation, quarantine, checkpoint durability, replay/bootstrap, backpressure, observability, and reconciliation. Test crashes at every boundary and verify ledger outcomes independently.

### Answer 4

The net burst accumulation is (260-200=60) items/s. Over 90 seconds it adds (60(90)=5{,}400) items. With an existing 600 items, demand reaches 6,000 items, exceeding the 5,000-item capacity. Available space is (5000-600=4400) items, so deterministic overflow starts after:

\[
t=4400/60\approx73.33\text{ s}.
\]

At least 1,000 additional slots would avoid overflow for exactly this bounded burst, but that is not a full design. Item sizes, variable arrivals/service, fan-out, persistence bandwidth, priorities, concurrent recovery, failures, buffer implementation, stale-work value, backpressure latency, drain time, and future bursts require analysis or simulation. A safer design may admit, aggregate, prioritize, or shed rather than only add memory.

### Answer 5

Preserve invariants for safe limits, authorized control, bounded response, valid/fresh observations, deterministic conflict handling, auditable decisions/effects, and safe behavior under communication loss. Baseline centralized flows, physical plant assumptions, hazards, modes, timing, clocks, policies, configurations, and evidence. In the candidate, local controllers own fast loops and bounded actuation; supervisory flows distribute signed/versioned constraints and desired objectives, not unconstrained commands. Define update expiry, local validation, partition duration, policy rollback, rejoin, state reconciliation, and override authority.

Analyze sampling/delay/stability, saturation, concurrent controllers, shared sensors/power/clocks, common software/policy faults, malicious/replayed updates, overload, degraded/maintenance/startup/recovery modes, and operator workload. Use static model checks, control analysis, simulation, fault/threat analysis, hardware-in-loop, representative plant tests, partition/rejoin drills, security tests, and independent outcome observations. Reject hard safety or authority violations before trade scoring. Conclude only for the tested controller, plant, network, policy, configuration, environmental, and operational bounds; local autonomy is not inherently safer or more available.
