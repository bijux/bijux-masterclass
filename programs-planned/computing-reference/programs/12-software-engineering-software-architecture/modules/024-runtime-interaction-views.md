---
module_id: SARCH-024
program: Software Engineering: Software Architecture
level: 1
module_number: 24
title: Runtime Interaction Views
status: complete
last_verified: 2026-09-06
---

# Runtime Interaction Views

## One-Page Review

### Governing question

How can an architecture description show the causally significant events of a runtime scenario so that stakeholders can reason about ordering, concurrency, latency, ambiguity, failure, state change, authority, and recovery without mistaking one trace for all possible behavior?

### Essential definitions

- An **interaction** is a scenario-bounded exchange of events among runtime participants.
- A **participant** is a runtime role or instance that sends, receives, computes, stores, decides, or observes.
- An **event** is a relevant occurrence: a send, receive, state transition, timeout, cancellation, or external effect.
- A **message** relates a send event to a receive event and carries declared meaning, identity, data, and protocol obligations.
- A **trace** is one ordering of events admitted by the model; it is not automatically the only possible execution.
- **happens-before**, written $\rightarrow$, is a causal partial order induced by local participant order, message send-before-receive, and transitivity.
- Two events are **concurrent** when neither happens before the other in the modeled relation.
- An **alternative** is a guarded set of permitted event paths, including timeout, rejection, cancellation, duplicate, and recovery paths.
- A **linearization** is a total ordering of events that preserves every happens-before constraint.
- A **correlation identity** joins observations belonging to one logical operation across messages, retries, asynchronous stages, and telemetry.

### Central model, mechanism, or theorem

Model a runtime scenario as

$$
I=(P,E,M,\prec_P,G,Q),
$$

where $P$ is the participant set, $E$ the event set, $M\subseteq E\times E$ the send-receive relation, $\prec_P$ local participant order, $G$ guarded alternatives, and $Q$ scenario obligations. The causal relation $\rightarrow$ is the transitive closure of $\prec_P\cup M$.

A displayed sequence is valid only if it is a linear extension of $\rightarrow$ and satisfies the selected guards and obligations. If neither $e\rightarrow f$ nor $f\rightarrow e$, the model must not invent a causal order merely because the events occupy different vertical positions.

### Critical invariants

- name scenario, scope, lifecycle state, abstraction, participants, and success criterion;
- distinguish participant roles, types, and runtime instances;
- distinguish send, receive, acceptance, processing, commit, reply, observation, and external effect;
- preserve local order and send-before-receive while exposing genuinely concurrent events;
- state guards, preconditions, postconditions, invariants, timeouts, deadlines, loops, and termination;
- treat timeout as local uncertainty rather than proof of remote non-execution;
- carry stable operation, message, causation, and correlation identity through retries and asynchronous work;
- locate authoritative state transitions and irreversible external effects;
- model rejection, partial failure, cancellation, duplicate, reordering, overload, and recovery paths;
- reconcile interaction claims with component-and-connector, deployment, data, security, and operational views;
- bind conformance claims to versioned models, tests, traces, logs, and known evidence limits.

### Common failures

Common failures include drawing only the happy path; presenting vertical placement as measured time; assuming clocks on different hosts are comparable; merging send and receive into one event; confusing message acceptance with business completion; omitting guards, loops, timeouts, cancellation, and retries; treating timeout as non-execution; assigning a total order to concurrent events; hiding shared state and external side effects; and claiming one observed trace proves all permitted behavior.

### Compact example

Checkout sends `authorize(op-71)` to a payment provider. The provider may commit the charge before checkout's 800 ms deadline, yet the response may arrive late. The timeout orders checkout's local fallback after its deadline; it does not prove the provider made no charge. The view must carry `op-71`, prohibit blind creation of a second payment identity, and show later status reconciliation.

### Connections

[SARCH-018](018-observability-and-operability-tactics.md) supplies causal observability; [SARCH-021](021-context-views.md) supplies external crossings; [SARCH-023](023-component-and-connector-views.md) supplies runtime topology and connector semantics. [SARCH-025](../ROADMAP.md) next develops deployment views, while Distributed Systems later deepens logical time and distributed protocols.

## Governing Question

A component-and-connector view answers “what can interact?” A runtime interaction view asks “what may happen, in what causal order, under which conditions, and with what outcome?” That change of emphasis exposes facts hidden by topology: a response can race a timeout, two updates can be concurrent, a queue acknowledgment can precede business completion, and an operation can take effect even when its caller observes failure.

The governing problem is to represent enough temporal and causal structure for architectural reasoning without pretending to specify every instruction or predict one universal execution. The view must make success, alternatives, failure, authority, and uncertainty explicit at a resolution appropriate to its stakeholders.

## Why This Matters

Ordering is often part of correctness. Debit must not become spendable before authorization; a configuration generation must not be activated before validation; a rail movement authority must not be issued from stale occupancy; cancellation must not silently erase an irreversible external action. Latency, availability, security, auditability, and consistency arise from paths through time, not static boxes alone.

Distributed and concurrent systems make intuition unreliable. Network transmission separates send from receive. Schedulers interleave work. Buffers delay delivery. Retries repeat requests. Clocks drift. A participant can fail after committing but before replying. A trace collected in production is an observation with missing and sampled data, not a complete specification.

A disciplined interaction view supplies reviewable causal constraints and alternatives. It enables architects to find ambiguous outcomes, races, lock cycles, unauthorized delegation, missing deadlines, retry amplification, orphan work, unsafe compensation, and telemetry gaps before these become incidents.

## Prerequisites and Retrieval

Retrieve participant, component, connector, message, event, state, invariant, precondition, postcondition, guard, sequence, concurrency, partial order, total order, send, receive, request, response, acknowledgment, retry, timeout, deadline, cancellation, idempotency, operation identity, correlation, authority, trace, span, clock skew, conformance, and evidence.

From prior modules, retrieve quality-attribute scenarios, availability and performance tactics, security and interoperability tactics, observability and operability, context views, module/code views, and component-and-connector configurations. Distinguish logical interaction, physical deployment, source dependency, and observed telemetry.

## Learning Objectives

After completing this module, you should be able to:

1. define participants, events, messages, traces, guards, and causal order;
2. distinguish local order, message order, wall-clock order, and arbitrary diagram order;
3. model synchronous, asynchronous, streaming, callback, and shared-state interactions;
4. expose concurrency, races, loops, timeouts, retries, cancellation, and partial failure;
5. specify preconditions, postconditions, state authority, and externally visible effects;
6. preserve operation and correlation identity across ambiguous outcomes;
7. use partial orders and linearizations to review valid and invalid traces;
8. connect latency budgets to event boundaries without inventing precision;
9. compare prescribed interaction models with tests and runtime telemetry;
10. reconcile interaction views with topology, deployment, data, security, and operations.

## Core Exposition

**Frame one scenario.** Start with stakeholder, stimulus, operating condition, initiating event, intended response, measurable response condition, and failure or recovery concerns. State whether the view is logical, design-time, deployment-specific, or reconstructed from observation. Name included and omitted participants, lifecycle state, version, and abstraction.

“Place an order during normal operation” and “recover an uncertain payment after provider isolation” deserve separate projections even when they share participants. Combining every alternative into one diagram produces a dense graph that nobody can validate.

ISO/IEC/IEEE 42010:2022 remains the current published architecture-description edition as checked on 2026-09-06; it organizes descriptions around stakeholder concerns, viewpoints, model kinds, and correspondences rather than mandating one universal notation [1]. UML 2.5.1 remains the current formal UML version in the OMG catalogue as checked on the same date. Its Interaction package defines traces and partial-order constraints and offers sequence, communication, interaction-overview, and timing diagram variants [2]. The architectural obligation is semantic clarity, not decorative compliance.

**Choose participants deliberately.** A participant may be a user role, service instance, worker, broker, database authority, device, external provider, scheduler, control plane, or security decision point. Show the runtime role needed for the scenario, not every class.

Distinguish role from instance. `payment-provider` may be a role; `provider replica p7` is an instance. Multiplicity matters when concurrent requests reach different instances or one consumer owns a partition. State whether a lifeline represents one instance, any instance of a type, or a collective.

**Separate events.** Sending, transport acceptance, receiving, beginning work, committing state, publishing an event, acknowledging delivery, replying, and observing a reply are distinct occurrences. Collapsing them into one arrow hides delay and failure intervals. If architecture depends on “durably accepted” or “externally visible,” name the exact event and authority.

A synchronous call blocks a caller according to a local programming model; it does not make network execution instantaneous or atomic. A broker acknowledgment may establish durability under a declared failure model but does not prove a consumer applied the business transition.

**Model causal order, not page order.** Lamport formalized happens-before as a partial ordering built from order within a process, message send before corresponding receive, and transitivity [3]. Assert only causal constraints justified by participant behavior or communication. If two events have no causal path, treat them as concurrent even if one is drawn higher.

Let $e\prec_p f$ mean participant $p$ performs $e$ before $f$. Let $(s,r)\in M$ pair a message send with its receive. Then $\rightarrow=(\prec_P\cup M)^+$, the transitive closure. A concrete execution may select one linearization, but a design view should preserve the relevant set of allowed linearizations.

Physical timestamps are evidence, not causality by themselves. On one monotonic clock, $t(f)-t(e)$ can estimate elapsed time subject to measurement error. Across hosts, the difference includes clock offset and synchronization error. An observed negative duration can result from skew rather than reverse causation.

**Show messages as contracts.** Give each consequential message a semantic name, direction, identity, required data, authority, confidentiality, integrity, expected response, deadline, ordering scope, delivery behavior, and version assumptions. Distinguish command, event, query, response, acknowledgment, cancellation, and control message.

`authorize(operation_id, amount, currency, account)` supports review only if the view also identifies who may authorize, when the identity is unique, whether duplicates are safe, and what accepted, declined, unavailable, or indeterminate means.

**Use guards and alternatives.** A scenario has preconditions, invariants, and postconditions. Guards select alternatives such as `[authorized]`, `[declined]`, `[deadline expired]`, `[duplicate identity]`, or `[version unsupported]`. State whether guards are exhaustive and whether simultaneous guards are possible.

Loops require entry, continuation, exit, and a bound or resource policy. A retry loop without deadline, attempt limit, backoff, jitter, and operation identity can amplify failure indefinitely. A stream needs flow control and completion semantics, not an arrow repeated forever.

**Treat timeout as local knowledge.** A timeout says the waiting participant did not observe a qualifying response by its local deadline. It does not establish whether the request was sent, received, rejected, committed, or replied to. Classify the outcome as safely retryable, terminal, or indeterminate. Indeterminate outcomes need stable identity, status lookup, reconciliation, or compensation appropriate to the effect.

Cancellation is also a protocol. State whether it is advisory, acknowledged, effective only before a named commit point, or guaranteed for a bounded local operation. Distinguish stopping computation from undoing an external effect.

**Locate state and authority.** Mark state reads, validations, tentative changes, commits, publications, and external effects. Identify the authoritative participant and version or token used for conditional transitions. Otherwise a plausible message order can hide a lost update or double effect.

When several participants change state, do not label a long sequence “transaction.” State the atomicity boundary. Outside it, describe durable records, retries, compensation, reconciliation, and failure ownership. Compensation is a new semantic action and may itself fail; it is not time reversal.

**Expose concurrency and reentrancy.** Parallel fragments or explicit partial-order annotations should show independent work. Challenge shared state, lock acquisition, capacity, ordering, and callbacks. A callback may reenter a participant while it holds a lock or is midway through an invariant-preserving transition.

For locks $L_1$ and $L_2$, if one path acquires $L_1$ then waits for $L_2$ while another holds $L_2$ and waits for $L_1$, the wait-for cycle exposes a deadlock possibility. Show acquisition and callback boundaries when this is an architectural risk, not every mutex instruction.

**Budget time at defined boundaries.** Attach deadlines to an observer and response condition. If a serial path contains compatible durations $d_1,\dots,d_n$, a simple budget requires $\sum_i d_i\le D$ after uncertainty and recovery margin. Parallel required branches often contribute their maximum, but queueing, contention, retries, and join policy change the result.

This arithmetic allocates a budget; it does not predict production latency. Record whether time is processing, waiting, transfer, queueing, backoff, or observation. Do not add independently reported percentiles as though they were aligned samples.

**Trace identity and authority.** Carry operation identity across retries, message identity across delivery, causation identity across derived work, and correlation identity across observations. These can coincide in simple designs but serve different purposes. Security identity and delegated authority are separate: a trace identifier is not an authorization credential.

**Connect prescription and observation carefully.** A prescribed model says what behavior is permitted or required. A model-based test explores selected paths. A runtime trace records events produced by instrumentation. A log records a local statement. These artifacts answer different questions.

OpenTelemetry's current concepts documentation, retrieved 2026-09-06, describes traces as request paths and spans as units of work carrying identifiers, timestamps, events, links, attributes, and status [4]. Its tracing specification relates root and child spans through context [5]. Sampling, missing instrumentation, buffering, export failure, clock skew, and broken propagation can still produce incomplete or misleading traces.

Conformance needs a mapping from model event to evidence event, versions, environment, expected alternatives, and tolerances. A trace matching one linearization establishes one observed instance under recorded conditions. It does not show that every permitted path is implemented or every forbidden path impossible.

**Reconcile adjacent views.** Every participant should map to a runtime component or external party. Every message should map to a connector or shared-state mechanism. Deployment views locate instances. Data views identify authoritative state. Security views identify trust and privilege. Operational views define telemetry, timeout ownership, recovery, and escalation.

A message with no connector, a participant with no deployed instance, a commit with no data authority, or a timeout with no owner indicates missing design or correspondence—not merely a drawing defect.

## Definitions and Notation

Define an interaction model $I=(P,E,M,\prec_P,G,Q)$ where $P$ is a finite participant set; $E$ is a finite event set; $M\subseteq E\times E$ pairs sends and receives; $\prec_P=\bigcup_{p\in P}\prec_p$ is strict local event order; $G$ contains guards; and $Q$ contains state, time, authority, and outcome obligations.

Define causal order as $\rightarrow=(\prec_P\cup M)^+$. The model is causally well formed only if $\rightarrow$ is irreflexive. A cycle $e\rightarrow e$ means contradictory ordering constraints. Events are concurrent, $e\parallel f$, when neither $e\rightarrow f$ nor $f\rightarrow e$.

A trace $\tau=(e_1,\ldots,e_n)$ is a valid linearization when it contains each selected event once and

$$
e_i\rightarrow e_j \implies i<j,
$$

while satisfying active guards and $Q$. Multiple linearizations can represent the same partial-order scenario.

If endpoint clocks may each differ from true time by at most $\epsilon$, an observed cross-host difference $\widehat{\Delta}=t_r-t_s$ gives the illustrative uncertainty band $[\widehat{\Delta}-2\epsilon,\widehat{\Delta}+2\epsilon]$. State the synchronization model; do not use this bound when its premises are absent.

Let $Commit(o)$ be the authoritative effect for operation identity $o$. A duplicate-safety invariant is

$$
\#\{c\mid c=Commit(o)\}\le 1
$$

within a declared authority and retention horizon. This permits multiple deliveries, attempts, spans, or responses while constraining the authoritative effect.

## Mechanisms, Invariants, or Proof Structure

Use this review mechanism.

1. **Frame:** name concern, stimulus, condition, response, measure, scope, abstraction, and lifecycle state.
2. **Select participants:** distinguish roles, types, instances, collectives, external parties, and authorities.
3. **Identify events:** separate send, receive, accept, process, commit, publish, reply, observe, timeout, cancel, and recover.
4. **Order causally:** add local and send-receive edges; preserve concurrency; reject cycles and invented order.
5. **Specify messages:** record semantics, identity, data, authority, version, delivery, ordering, timing, and failure.
6. **Add alternatives:** state guards, preconditions, invariants, postconditions, loops, bounds, and terminal outcomes.
7. **Challenge:** trace duplicate, delay, reordering, timeout, cancellation, crash, overload, stale state, attack, and recovery.
8. **Budget:** attach deadlines and capacities to exact observers and event boundaries with uncertainty.
9. **Correlate:** preserve operation, message, causation, security, and telemetry identity without conflating them.
10. **Reconcile and verify:** map to topology, deployment, data, security, tests, traces, operations, and evidence limits.

The governing invariants are causal consistency, explicit concurrency, stable identity, authoritative effects, bounded alternatives, local interpretation of timeout, declared security authority, cross-view correspondence, and evidence-bounded conformance.

If $\rightarrow$ is finite and acyclic, at least one linear extension exists. Repeatedly select an event with no unprocessed predecessor, append it, and remove it. A finite acyclic graph always has such a minimal event; otherwise following predecessors would eventually repeat a node and form a cycle. This proves existence of an admissible total order for the stated constraints, not that an implementation realizes every such order or meets $Q$.

## Alternatives and Trade-Offs

**Sequence versus communication views.** A sequence view foregrounds order along lifelines. A communication view foregrounds relationships and numbered messages. Use the form that answers the concern while preserving one semantic event model.

**Partial order versus one concrete trace.** Partial order preserves concurrency and legal interleavings. One trace is easier to read for an incident or exemplar. Label it as one permitted or observed linearization and state omitted alternatives.

**Logical versus instance-specific participants.** Logical roles remain stable. Instance views reveal routing, replicas, zones, and failure boundaries but age faster. Link both when deployment changes behavior.

**Synchronous versus asynchronous interaction.** Synchronous invocation simplifies immediate control flow but couples caller progress to callee latency. Asynchrony decouples time but creates acceptance/completion distinctions, delayed authorization, duplicates, backlog, and reconciliation.

**Orchestration versus choreography.** An orchestrator makes sequence and recovery ownership visible but becomes a coordination dependency. Choreography supports autonomy but makes causal paths and global invariants harder to diagnose.

**Prescriptive model versus observed trace.** A model defines allowed or required behavior. Traces reveal encountered behavior in a recorded environment. Compare them only with known mappings, instrumentation, versions, sampling, and uncertainty.

**Compact view versus exhaustive state model.** A concise view supports review. A protocol state machine or model checker supports systematic path exploration. Link them instead of forcing exhaustive behavior into an unreadable diagram.

## Failure Modes and Misconceptions

- **The arrow is instantaneous.** Send and receive are separate events with failure between them.
- **Higher means earlier everywhere.** Vertical placement is notation; causality needs explicit constraints.
- **A timeout means nothing happened.** It means one observer lacked a qualifying response by a local deadline.
- **Acknowledged means completed.** Acknowledgment may mean receipt, enqueue, processing, or commit.
- **The trace is the specification.** It is one possibly incomplete execution.
- **Timestamps prove causality.** Cross-host values require synchronization assumptions.
- **Retries repeat the same outcome.** They can duplicate effects without stable identity and authoritative deduplication.
- **Cancellation undoes work.** It may only request that future work stop.
- **Parallel branches are independent.** They may share state, locks, quotas, or downstream capacity.
- **Compensation is rollback.** It is a new, fallible domain action.
- **One lifeline means one process.** It can mean role, type, instance, or collective.
- **Correlation equals authorization.** Context identifiers do not confer permission.
- **A matching happy path proves conformance.** It establishes at most one observed path.

## Worked Examples

### Example 1

**Situation.** A client calls inventory to reserve item `A` and receives `reserved`.

**Reasoning.** Let $s_1$ be the send of `reserve(op-1,A)`, $r_1$ its receipt, $c_1$ the authoritative commit, $s_2$ the response send, and $r_2$ the response receipt. Then $s_1\rightarrow r_1\rightarrow c_1\rightarrow s_2\rightarrow r_2$. Collapsing these into one arrow hides failures between commit and observation.

**Conclusion.** A synchronous-looking call contains several causal events and an interval of outcome ambiguity.

### Example 2

**Situation.** Checkout sends `authorize(op-71)` and times out at 800 ms; the provider commits at 760 ms but its response arrives at 920 ms.

**Reasoning.** The timeout follows checkout's send and local deadline. Provider commit follows provider receive. Timeout does not imply non-commit. A retry with a new identity could double charge; retrying or querying with `op-71` supports reconciliation against the provider's authority.

**Conclusion.** Timeout creates local uncertainty; stable operation identity protects the authoritative effect.

### Example 3

**Situation.** An API returns `202 Accepted` after enqueueing a report request.

**Reasoning.** Separate submit, receive, durable queue commit, acceptance reply, worker receive, report commit, completion publication, and client observation. The `202` may mean durable acceptance when the queue commit precedes it. It cannot mean completion, which occurs later. Poison input and expiration need terminal outcomes.

**Conclusion.** Name the milestone an acknowledgment establishes; acceptance and completion differ.

### Example 4

**Situation.** After $a$, two participants independently perform $b$ and $c$, and join $d$ waits for both.

**Reasoning.** Constraints are $a\rightarrow b\rightarrow d$ and $a\rightarrow c\rightarrow d$, with $b\parallel c$. The valid linearizations are $(a,b,c,d)$ and $(a,c,b,d)$. Requiring $b$ before $c$ needs another causal mechanism.

**Conclusion.** Partial order exposes concurrency; two drawings can express one causal model.

### Example 5

**Situation.** A consumer writes an invoice, crashes before acknowledging, then receives the same message again.

**Reasoning.** At-least-once delivery permits two attempts. Fresh invoice keys create duplicates. Carry `bill-204`, enforce one invoice transition for that identity, and acknowledge after durable commit. The deduplication horizon must cover redelivery and replay.

**Conclusion.** Delivery can repeat while the authoritative effect remains singular only under an explicit invariant.

### Example 6

**Situation.** Two workers read account version 8 with balance 100 and subtract 30 and 50.

**Reasoning.** The reads are concurrent. Unconditional stores of 70 and 50 lose one debit. With `expected_version=8`, one commit succeeds and advances the version; the other is rejected and must re-read or follow conflict policy.

**Conclusion.** The authoritative transition, not message order alone, needs a concurrency invariant.

### Example 7

**Situation.** A holds $L_1$, calls B, and waits. B holds $L_2$ and calls back into A, whose callback needs $L_1$.

**Reasoning.** A waits for B while holding $L_1$; B waits for A while holding $L_2$. The wait-for cycle permits deadlock. Release locks before calls, prohibit synchronous callbacks, enforce lock order, or queue the callback; each alternative changes semantics.

**Conclusion.** Interaction and lock boundaries reveal reentrancy risks hidden by topology.

### Example 8

**Situation.** Travel orchestration reserves flight and hotel, then fails to reserve a car.

**Reasoning.** Independent providers cannot be atomically rolled back. Hotel cancellation succeeds; flight cancellation is rejected as nonrefundable. The terminal state is partial, requiring user communication and business policy. Compensation commands carry original identities and can fail.

**Conclusion.** Compensation is a fallible forward interaction, not time reversal.

### Example 9

**Situation.** A trace has gateway, order, and database spans but no required payment span.

**Reasoning.** Payment might have been skipped, uninstrumented, sampled out, disconnected from context, or lost during export; the model might not apply to this request. Check guards, operation identity, instrumentation version, sampling, logs, and provider records.

**Conclusion.** A missing span is bounded evidence, not proof of omission or success.

### Example 10

**Situation.** An infusion pump receives a dosage plan while intermittently disconnected.

**Reasoning.** Model signed plan receipt, patient/device and version validation, local safety limits, activation, physical delivery, immutable local record, delayed upload, duplicate upload, revocation, and safe mode. A supervisory timeout cannot imply no dose. Offline authority and reconciliation need explicit bounds. Hazard analysis and regulated verification remain separate activities.

**Conclusion.** High-consequence views must expose local authority, physical effect, stale commands, and reconciliation without claiming certification.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** happens-before, races, locks, reentrancy, and memory models deepen local concurrency.
- **Distributed Systems:** logical clocks, partial failure, replication, delivery, and causality deepen cross-node ordering.
- **Operating Systems:** scheduling, IPC, timers, blocking, and monotonic clocks explain runtime mechanisms.
- **API and Service Engineering:** protocol operations, status semantics, deadlines, idempotency, and versioning specialize messages.
- **Database Engineering:** transactions, isolation, conditional writes, and logs determine when state becomes authoritative.
- **Software Delivery and Reliability Engineering:** tracing, incident reconstruction, service objectives, and recovery turn models into evidence.
- **Security:** authentication, delegation, replay resistance, revocation, and audit constrain who may cause events.
- **Systems Engineering:** hazardous control sequences, timing, physical effects, and assurance connect software to the whole system.

## References

1. ISO/IEC/IEEE, *ISO/IEC/IEEE 42010:2022 Software, systems and enterprise — Architecture description*, 2nd ed., November 2022. Official catalogue; current edition checked 2026-09-06. https://www.iso.org/standard/74393.html
2. Object Management Group, *OMG Unified Modeling Language (OMG UML), Version 2.5.1*, formal/2017-12-05, December 2017, Clause 17. Official specification and current formal version checked 2026-09-06. https://www.omg.org/spec/UML/2.5.1/PDF
3. Leslie Lamport, “Time, Clocks, and the Ordering of Events in a Distributed System,” *Communications of the ACM* 21(7), 558–565, 1978. https://doi.org/10.1145/359545.359563
4. OpenTelemetry Authors, “Signals,” current concepts documentation. Retrieved 2026-09-06. https://opentelemetry.io/docs/concepts/signals/
5. OpenTelemetry Authors, “Tracing API,” current specification documentation. Retrieved 2026-09-06. https://opentelemetry.io/docs/specs/otel/trace/api/
6. Paul Clements et al., *Documenting Software Architectures: Views and Beyond*, 2nd ed., Addison-Wesley, 2010.
7. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
8. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly Media, 2017, Chapters 8–9.

## Exercises

### Exercise 1

Distinguish send, receive, business commit, acknowledgment, timeout, and trace span. Which relationships are causal by definition, and which require a protocol?

### Exercise 2

Events $a,b,c,d,e$ satisfy $a\rightarrow b$, $a\rightarrow c$, $b\rightarrow d$, $c\rightarrow d$, and $d\rightarrow e$. Identify concurrent pairs and enumerate all valid linearizations.

### Exercise 3

Host X records send at 12.000 s; host Y records receive at 11.994 s. Each clock may differ from true time by at most 5 ms. Diagnose the observation and compute the illustrative $\widehat{\Delta}\pm2\epsilon$ interval.

### Exercise 4

Design shipment creation through an external carrier when responses can be lost. Compare blind retry, status-before-retry, and stable-operation-identity approaches. Include authority, timeout, cancellation, and reconciliation.

### Exercise 5

Transfer the method to an offline-capable irrigation controller. Design interactions for plan receipt, sensor and safety checks, valve control, ineffective-flow detection, delayed stop, physical-effect recording, and later reconciliation.

## Answers to the Exercises

### Answer 1

A **send** is the sender's local emission; a **receive** is the receiver's local acceptance of that message, so send precedes receive. A **business commit** is the authoritative state transition. An **acknowledgment** reports a protocol-defined milestone: receipt, enqueue, processing, or commit. A **timeout** is a local event saying no qualifying response was observed by a deadline. A **trace span** is an instrumentation record that may approximate several events.

Local program order and send-before-receive are causal in this model. Whether receive precedes commit, commit precedes acknowledgment, or timeout permits retry depends on protocol. Span parentage supports reconstruction only when instrumentation and context propagation are sound.

### Answer 2

Transitivity makes $a$ precede every other event, both $b$ and $c$ precede $d$, and $d$ precedes $e$. The only concurrent pair is $b\parallel c$. There are exactly two valid linearizations: $(a,b,c,d,e)$ and $(a,c,b,d,e)$. Any order placing $d$ before $b$ or $c$, $e$ before $d$, or anything before $a$ is invalid.

### Answer 3

$\widehat{\Delta}=11.994-12.000=-0.006$ s, or $-6$ ms. With $\epsilon=5$ ms at each endpoint, the illustrative band is

$$
[-6-10,-6+10]\text{ ms}=[-16,4]\text{ ms}.
$$

The timestamps do not establish negative transmission time or reverse causality; offsets can explain them. Send-before-receive still follows from the message relation. The numeric band requires the stated error model, correct event timestamps, and no additional uncertainty; without those premises it is unjustified.

### Answer 4

The carrier owns carrier shipment creation; the local system owns its request and reconciliation record. Allocate a stable operation identity before the first request and bind it to the carrier idempotency key when supported. Record attempts, responses, carrier identity, and terminal state.

Blind retry with a fresh identity can duplicate shipments. Status-before-retry reduces duplication when authoritative lookup exists, but lookup can be unavailable or delayed. Same-identity retry works only within the carrier's deduplication scope and retention. On timeout, mark the result indeterminate, query by identity, retry only within contract and deadline, and escalate unresolved cases. Cancellation is separate and effective only if confirmed before the irreversible handoff boundary. Reconciliation compares local intent, carrier authority, billing, and physical handoff.

### Answer 5

Use controller instance, signed-plan authority, sensors, safety policy, valve actuator, local journal, and supervisor as participants. The controller authenticates a plan with plan, site, zone, version, validity, and correlation identities; rejects stale or wrong-site plans; persists accepted intent; reads sensors; and evaluates moisture, reservoir, maintenance, and maximum-flow guards.

If locally authorized, it issues an identified valve-open command and records acknowledgment separately from physical flow evidence. Absent expected flow, it closes the valve, records the fault, and enters a safe state. It records duration, measured flow, closure command, closure evidence, and uncertainty. A delayed stop for the same operation still closes the valve, but prior water flow remains recorded rather than rewritten as canceled.

Offline policy states maximum autonomous duration, plan expiry, safety limits, replay protection, and behavior when sensors disagree. On reconnection, the controller uploads operation identities and immutable records; the supervisor deduplicates, compares planned and observed effects, applies newer policy prospectively, and raises discrepancies. Alternatives pass only if they preserve explicit authority, safe bounds, stale-command handling, physical evidence, and recovery ownership.
