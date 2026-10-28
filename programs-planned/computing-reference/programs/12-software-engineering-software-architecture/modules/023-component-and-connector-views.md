---
module_id: SARCH-023
program: Software Engineering: Software Architecture
level: 1
module_number: 23
title: Component-and-Connector Views
status: complete
last_verified: 2026-09-06
---

# Component-and-Connector Views

## One-Page Review

### Governing question

How can an architecture description expose runtime computational elements and their interaction mechanisms so that stakeholders can reason about behavior, protocols, concurrency, failure, security, performance, and operational responsibility?

### Essential definitions

- A **runtime component** is an executing or active computational element with behavior, state, responsibilities, and interaction points.
- A **connector** is an explicit interaction mechanism with semantics such as invocation, messaging, streaming, shared data, event publication, coordination, or synchronization.
- A **port** is a component interaction point that provides or requires a protocol, data shape, quality, or authority.
- A **role** is a participant position in a connector, such as caller, callee, publisher, subscriber, producer, consumer, reader, or writer.
- An **attachment** binds a component port to a compatible connector role.
- A **configuration** is a set of component and connector instances and their attachments under declared constraints.
- A **protocol** constrains permitted sequences and meanings of interaction events.
- **architectural mismatch** occurs when participant assumptions about interaction, control, data, quality, or environment are incompatible.
- A **topology** describes arrangement and multiplicity; it does not by itself establish deployment location.

### Central model, mechanism, or theorem

Represent a component-and-connector configuration as

$$
\Gamma=(C,K,P,R,A),
$$

where $C$ and $K$ are component and connector instances, $P(c)$ gives component ports, $R(k)$ gives connector roles, and $A\subseteq P\times R$ gives attachments. An attachment $(p,r)$ is admissible only when the port and role agree on direction, operation or event semantics, schema, protocol, identity and authority, timing, delivery, ordering, capacity, failure, and lifecycle conditions relevant to the concern.

Type compatibility is necessary but insufficient: two endpoints can share a schema and still disagree about retries, duplicate effects, ordering, cancellation, authorization, or ambiguous outcomes.

### Critical invariants

- state scope, scenario, lifecycle state, abstraction, instance/type meaning, and notation;
- model runtime responsibilities as components rather than copying source modules;
- model consequential interaction semantics explicitly rather than using generic lines;
- name ports, roles, direction, initiation, protocol, authority, and failure behavior;
- distinguish synchronous calls, queues, streams, events, shared data, and control connectors;
- expose cardinality, concurrency, buffering, backpressure, ordering, retry, and cancellation assumptions;
- preserve operation and message identity across timeout, duplicate, replay, and recovery;
- show trust, privilege, sensitive data, and administrative control across attachments;
- reconcile configuration with context, module, runtime sequence, deployment, data, and operational views;
- bind claims to contracts, models, tests, traces, configuration, and known evidence limits.

### Common failures

Common failures include relabeling a class diagram as runtime architecture; treating every line as an API; hiding queues, brokers, proxies, databases, callbacks, and service meshes; showing component types when reasoning depends on instances; omitting multiplicity and shared dependencies; assuming schema compatibility proves protocol compatibility; drawing request arrows without timeout or response ambiguity; modeling publish-subscribe as direct publisher-to-subscriber calls; ignoring backpressure and queue capacity; treating a load balancer as behaviorless; confusing logical topology with deployment; and claiming the diagram proves production behavior.

### Compact example

Checkout attaches its `authorize-payment` port to the caller role of a request-response connector; a payment provider fills the callee role. The connector contract includes operation identity, deadline, authentication, response meanings, retry conditions, and later status reconciliation. A timeout means checkout lacks a timely response—it does not prove the provider made no charge.

### Connections

[SARCH-017](017-interoperability-tactics.md) supplies semantic and protocol contracts; [SARCH-018](018-observability-and-operability-tactics.md) supplies causal identity and operational evidence; [SARCH-021](021-context-views.md) supplies external crossings; [SARCH-022](022-module-and-code-views.md) supplies static implementation structure. [SARCH-024](../ROADMAP.md) next develops time-ordered runtime interaction views.

## Governing Question

A module view can show which code depends on which code while saying little about what runs. One module may create hundreds of concurrent component instances; several modules may execute within one process; a connector may be implemented by libraries, proxies, brokers, networks, storage, and operations together.

The governing problem is how to represent the runtime architecture at a useful abstraction: the active responsibilities, the mechanisms that coordinate them, the assumptions at each attachment, and the configurations under which quality claims are supposed to hold.

## Why This Matters

Quality attributes emerge from interaction. A request path's latency depends on connectors, queues, contention, retries, and fan-out. Availability depends on shared connectors, failure detection, routing, and recovery. Security depends on identity propagation and authorization at crossings. Data correctness depends on ordering, duplicates, ownership, transactions, and reconciliation.

If connectors are reduced to unlabeled arrows, the most consequential decisions disappear. Teams then discover in production that a “call” blocks indefinitely, an “event” can be duplicated, a “stream” has no backpressure, a “database” is a shared synchronization point, or a callback executes user code inside a lock.

A good component-and-connector view does not reproduce every socket or function call. It selects runtime elements and connector semantics needed by scenarios, then links to detailed protocols, sequences, deployment, and evidence. Several projections may be necessary for normal, peak, failure, recovery, and adversarial conditions.

## Prerequisites and Retrieval

Retrieve runtime, component, connector, port, role, attachment, configuration, instance, type, protocol, request, response, message, event, stream, queue, buffer, backpressure, ordering, delivery, duplicate, retry, deadline, cancellation, idempotency, authority, trust, shared state, topology, trace, and conformance.

From prior modules, retrieve system context, quality scenarios, availability, performance, scalability, security, testability, interoperability, observability, conflict resolution, and module/code views. You should be able to distinguish source dependency, runtime interaction, deployment communication, and data authority.

## Learning Objectives

After completing this module, you should be able to:

1. define runtime components, connectors, ports, roles, attachments, and configurations;
2. select an abstraction and distinguish component types from instances;
3. model invocation, messaging, event, streaming, shared-data, and control connectors;
4. specify attachment compatibility beyond schemas and signatures;
5. expose concurrency, multiplicity, buffering, backpressure, ordering, and failure;
6. trace identity, authority, sensitive data, cancellation, retry, and reconciliation;
7. detect architectural mismatch between interacting participants;
8. compare alternative runtime configurations against quality scenarios;
9. reconcile component-and-connector views with static, sequence, deployment, data, and operational views;
10. evaluate conformance using bounded models, tests, traces, and configuration evidence.

## Core Exposition

**Define the view's concern and resolution.** State stakeholders, scenarios, lifecycle state, element types, connector types, instance/type notation, and omissions. A product owner may need a capability flow; performance engineers need queue and fan-out topology; security reviewers need identity and trust; operators need control and failure paths.

ISO/IEC/IEEE 42010:2022 remains the current published architecture-description edition as checked on 2026-09-06 and requires governed viewpoints and model kinds rather than prescribing one universal diagram [1]. A component-and-connector view is one concern-oriented model, not the entire architecture.

**Model runtime components.** A component is active at runtime: a process, service instance, worker, filter, repository abstraction with live behavior, rules engine, controller, scheduler, or client. Choose components according to behavior and quality reasoning rather than source packaging. Record responsibilities, state ownership, concurrency model, lifecycle, provided and required ports, resource bounds, and failure unit.

Do not assume one component equals one process, container, service, class, module, or team. A process can host several runtime components; one logical component can have many instances; a static module can participate in multiple components. Correspondence belongs in linked views.

**Make connectors first-class.** Allen and Garlan's foundational work treated connectors as explicit semantic entities with participant roles and interaction protocols rather than mere definition-use links [2]. This matters because invocation, publish-subscribe, queueing, streaming, transactions, and shared data impose different behavior.

A connector may be implemented by code in participants plus infrastructure between them. An HTTP request-response connector includes client library, name resolution, connection management, intermediaries, server, deadline, and response semantics as relevant. A brokered queue includes publishing, storage, delivery, acknowledgment, redelivery, retention, and administration. Model the architectural behavior, not a product logo.

**Name ports and roles.** A component port declares an interaction capability or requirement. A connector role declares participant obligations. For request-response, caller and callee roles differ. For publish-subscribe, publisher, broker, subscription, and subscriber roles differ. For shared storage, reader, writer, transaction coordinator, and schema authority may differ.

Attachment compatibility requires more than matching names. Check semantic operation, units, schema evolution, sequence, initiation, authentication, authorization, confidentiality, integrity, deadlines, delivery, ordering, capacity, retry, cancellation, error, lifecycle, and evidence. A JSON document accepted by both endpoints can still carry contradictory meanings.

**Distinguish connector families.** Synchronous invocation couples caller progress to response or timeout. It makes immediate results convenient but propagates latency and availability dependency. Define deadline, cancellation, connection failure, partial work, response authority, and retry safety.

Asynchronous queues decouple submission time from processing time and can level load. They introduce durable acceptance meaning, delay, capacity, ordering scope, duplication, poison messages, acknowledgments, replay, and backlog recovery. “Sent” can mean accepted locally, persisted by a broker, delivered, processed, or committed; name the event.

Publish-subscribe lets publishers avoid knowing subscribers. It introduces subscription lifecycle, filtering, delivery isolation, schema compatibility, replay, and fan-out. A slow subscriber should not silently stall unrelated subscribers unless that coupling is intentional.

Streams model sequences with flow control, framing, ordering, restart, and termination. Bounded buffers require backpressure, shedding, spill, or admission policy. Unlimited buffering merely transfers overload into memory, storage, or delayed failure.

Shared-data connectors coordinate through a database, filesystem, cache, memory region, or distributed store. They can create implicit communication, contention, schema coupling, transaction boundaries, polling, and ambiguous ownership. Draw the shared connector when it is architecturally significant instead of showing independent components that secretly coordinate through it.

**Model component and connector types separately from instances.** A type describes common behavior and constraints; an instance participates in one configuration. If failure or capacity reasoning depends on three replicas, two queues, or one shared broker, show instances or multiplicities. “Order service” as a type cannot reveal whether all replicas depend on one database.

Configuration can vary by environment and mode. Healthy operation may use all replicas; degraded mode may isolate a region; maintenance may drain a queue; recovery may enable replay. Use separate projections or state annotations rather than merging incompatible configurations.

**Expose concurrency and capacity.** Record whether a component is single-threaded, replicated, partitioned, reentrant, event-loop based, actor-like, or worker-pooled where relevant. State queue and connection bounds, admission, scheduling, batch size, and resource ownership. Multiplicity without routing semantics is incomplete.

For arrival rate $\lambda$ and sustainable service rate $\mu$, a persistent $\lambda>\mu$ means backlog grows in the simplified fluid model. Temporary bursts can be absorbed only within capacity and recovery margin. This inequality is a diagnostic model, not a full queueing theorem or production guarantee.

**Treat time and failure as protocol.** Define timeout as an observation at one participant, not proof of remote non-execution. Carry stable operation or message identity through retry and reconciliation. State whether cancellation is advisory, accepted, or terminal. Separate local task outcome from external side effect.

Model failure boundaries and common causes. A load balancer, broker, database, identity provider, service mesh, certificate authority, DNS, or control plane can be a shared connector dependency. Replicated boxes do not provide independence when they share one failure authority.

**Model ordering and delivery scope.** Global ordering, per-key ordering, per-connection ordering, and no ordering are different contracts. At-most-once delivery may lose work; at-least-once delivery may duplicate it; “exactly once” requires a precisely bounded state transition and failure model, not a marketing label. Define the authoritative effect and deduplication horizon.

Retries belong to a budget with deadline, backoff, jitter, capacity, and idempotency. A retry connector can amplify overload. Circuit breaking and load shedding change responses and must be visible in failure views. SARCH-024 will trace event order and concurrency in detail.

**Expose authority and trust.** For each attachment, identify authenticated identity, delegated authority, authorization decision, sensitive data, integrity protection, replay protection, audit, and administrative control. A gateway authenticating a caller does not automatically authorize downstream actions. Preserve user and workload identity only as far as justified.

Control connectors deserve special treatment. Configuration, deployment, feature flags, secrets, schema management, and administrative commands can change data-plane behavior. Model control-plane unavailability, stale state, privilege, rollback, and break-glass operation.

**Find architectural mismatch.** Mismatch occurs when one participant assumes synchronous completion and another promises eventual processing; one retries and another performs non-idempotent effects; one emits local time and another assumes UTC; one blocks on callbacks and another calls back under a held lock; or one expects unbounded input while another has finite buffers.

Build an assumption ledger for each attachment. Test protocol state machines, error mappings, cancellation, version skew, backpressure, security, and recovery. Adapters can translate compatible differences, but they cannot manufacture missing authority, durability, or semantic agreement.

**Compare configurations using scenarios.** For a quality scenario, trace stimulus through components and connectors to response. Assign latency and capacity budgets, failure and trust boundaries, state authority, and evidence. Compare alternative topology under normal, peak, failure, recovery, adversarial, and change conditions.

Avoid summing local guarantees without composition assumptions. Parallel fan-out latency depends on the slowest required branch and correlation. Serial calls add processing and waiting, but timeouts and retries change populations. Availability values do not multiply honestly without independence and response definitions.

**Reconcile other views.** Map context crossings to boundary ports and connectors. Map runtime components to implementing modules. Map connector implementations to protocols, libraries, infrastructure, and configuration. Map instances to deployment nodes. Map shared-data connectors to data authority and consistency. Map failure and control paths to operational views.

Mismatch between views is a review finding. A runtime component with no code owner, a connector with no deployable implementation, or a deployment link with no logical interaction needs resolution.

**Gather bounded conformance evidence.** Static configuration can show declared attachments. Contract tests can exercise selected protocols. Model checking can explore finite state abstractions. Integration tests can observe failures and version combinations. Traces can show encountered runtime paths; broker and service configuration can show current topology.

None proves universal production behavior. Traces miss dormant paths; tests sample inputs and conditions; models abstract; configuration can drift. Record environment, versions, scenarios, results, exclusions, and evidence age. Review after new connector, topology, workload, dependency, threat, incident, or operating mode.

## Definitions and Notation

Define a configuration

$$
\Gamma=(C,K,P,R,A),
$$

where $C$ is component instances, $K$ connector instances, $P=\bigcup_{c\in C}P(c)$ ports, $R=\bigcup_{k\in K}R(k)$ roles, and $A\subseteq P\times R$ attachments.

Let $contract(x)$ contain the relevant semantic, protocol, quality, and authority obligations for port or role $x$. Define an admissibility predicate

$$
Compatible(p,r,Q)\iff obligations(p,Q)\text{ and }obligations(r,Q)\text{ are jointly satisfiable},
$$

for concern set $Q$. Structural attachment conformance is

$$
AttachOK(\Gamma,Q)\iff \forall(p,r)\in A,\ Compatible(p,r,Q).
$$

This definition moves the hard work into explicit obligations; name equality or schema validation alone cannot establish compatibility.

For simplified backlog $B(t)$ over interval $\Delta t$ with constant arrival and service rates,

$$
B(t+\Delta t)=\max(0,B(t)+(\lambda-\mu)\Delta t).
$$

The model assumes homogeneous work, available service, and no admission or loss. Use it to expose overload direction, not predict a real queue without calibration.

Let $Prov(e)$ be the authoritative state transition for operation identity $e$. An idempotency invariant is that repeated accepted presentations of the same identity do not create more than one authoritative effect. Storage horizon, scope, conflicts, and downstream effects must be specified.

## Mechanisms, Invariants, or Proof Structure

Use this component-and-connector mechanism.

1. **Frame:** name concerns, scenarios, scope, state, abstraction, instance/type semantics, and notation.
2. **Identify components:** assign runtime responsibility, state, lifecycle, concurrency, resources, and failure boundary.
3. **Identify connectors:** choose explicit invocation, queue, event, stream, shared-data, synchronization, or control semantics.
4. **Specify ports and roles:** define direction, initiation, operations, events, protocol, authority, and quality obligations.
5. **Attach:** check schema, semantics, ordering, delivery, timing, capacity, failure, security, and lifecycle compatibility.
6. **Configure:** show instances, multiplicity, routing, partitioning, shared dependencies, modes, and transitions.
7. **Challenge:** trace timeout, duplicate, overload, backpressure, cancellation, version skew, attack, and recovery.
8. **Budget:** allocate latency, capacity, availability, trust, data, and operational responsibility without false composition.
9. **Reconcile:** map context, module, sequence, deployment, data, and operational views.
10. **Verify and govern:** use models, tests, traces, configuration, and incidents with explicit limits and triggers.

The governing invariants are explicit runtime responsibility, first-class connector semantics, compatible attachments, bounded concurrency and capacity, stable causal identity, declared ordering and failure, preserved authority, visible common dependencies, cross-view correspondence, and evidence-bounded conformance.

If every attachment satisfies $Compatible(p,r,Q)$, then the configuration has no declared attachment incompatibility for $Q$. This follows by universal quantification over $A$. It does not prove the obligation sets are complete, implementations conform, or the combined system meets end-to-end qualities.

## Alternatives and Trade-Offs

**Direct invocation** is simple and gives immediate responses but couples latency and availability. **Queued interaction** absorbs bursts and decouples time but introduces backlog, duplication, and delayed outcomes.

**Implicit library or framework connectors** reduce visible infrastructure but can hide threading, retries, serialization, and failure. **Explicit connector components** improve governance and observation but add configuration and operational surface.

**Type-level views** stay compact and durable. **Instance-level views** reveal shared dependencies, cardinality, routing, and failures but change more often. Use type views for common contracts and instance projections for concrete scenarios.

**One comprehensive configuration** centralizes information but quickly becomes unreadable. **Scenario projections** focus reasoning but can omit shared dependencies or drift. Preserve stable identities and a reconciled base model.

**Formal protocol models** can expose deadlock and incompatible sequences within an abstraction. **Tests and traces** connect to implementations but sample behavior. Use formalization where protocol consequence warrants it and empirical evidence for the deployed realization.

## Failure Modes and Misconceptions

- **“Components are classes.”** Runtime components are active architectural responsibilities, often implemented by many classes or modules.
- **“Connectors are arrows.”** They carry protocol, quality, failure, security, and operational semantics.
- **“Matching schemas means compatibility.”** Sequence, authority, units, retries, ordering, and errors can still conflict.
- **“A type diagram shows redundancy.”** Failure analysis often needs instances and shared dependencies.
- **“Async means decoupled.”** Schema, capacity, timing, replay, and authority still couple participants.
- **“A timeout means nothing happened.”** It means the observer lacks a timely result.
- **“Exactly once is a transport property.”** Authoritative effects require scoped identity and state transitions.
- **“Buffers solve overload.”** Finite capacity only delays a persistent rate imbalance.
- **“The broker guarantees ordering.”** Ordering has a key, partition, session, and failure scope.
- **“A gateway owns all security.”** Downstream authorization and data handling remain.
- **“Replicas imply independent failure.”** They may share data, network, identity, control, or operator failure.
- **“The runtime diagram is the deployment.”** Logical interaction and physical placement are distinct views.
- **“Traces reveal the architecture.”** They show encountered paths under specific instrumentation and conditions.

## Worked Examples

### Example 1

**Question:** Checkout times out calling payment. May it retry with a new identifier?

**Reasoning:** No, not safely for a charge operation. Preserve one operation identity, query or reconcile the authoritative result, and retry only under the provider's contract. Define deadline, authentication, idempotency horizon, response meanings, later settlement, reversal, and dispute. Timeout is local uncertainty.

**Conclusion:** Request-response compatibility includes ambiguous outcome and stable identity.

### Example 2

**Question:** A queue begins with 200 jobs, receives 50 jobs/s, and processes 40 jobs/s for 30 seconds. What does the simplified model predict?

**Reasoning:** Net growth is $(50-40)30=300$, so backlog becomes $200+300=500$ jobs, assuming no admission, loss, scaling, or rate variation. Continued overload grows without bound in this model; a larger finite queue changes time to exhaustion, not sustainability.

**Conclusion:** Capacity and recovery rate belong in the connector view.

### Example 3

**Question:** One publisher has three subscribers, and one subscriber is slow. What must the connector specify?

**Reasoning:** Define whether subscriptions have independent buffers, acknowledgments, retry, retention, and delivery state. If one shared cursor gates publication, the slow subscriber can couple all others. Isolate subscriptions or declare the coupling; bound backlog and poison-event handling.

**Conclusion:** Publish-subscribe topology alone does not guarantee subscriber isolation.

### Example 4

**Question:** A producer stream emits 1,000 items/s while a consumer sustains 700. What choices exist?

**Reasoning:** Persistent excess is 300 items/s. Use backpressure to slow the producer, admission or load shedding, partitioned consumers if work permits, bounded spill with recovery, aggregation, or a changed requirement. Unlimited memory buffering hides the conflict until failure.

**Conclusion:** A stream connector needs an explicit overload policy.

### Example 5

**Question:** Two components have no direct connector but update the same order table. Are they independent?

**Reasoning:** No. The database is a shared-data connector. Record schema and transaction authority, isolation, locking, polling, change notification, migration, failure, and ownership. Conflicting interpretations or writes can couple releases even without network calls.

**Conclusion:** Shared storage is interaction and must be visible when consequential.

### Example 6

**Question:** A component invokes a callback while holding a lock; the callback re-enters it. What mismatch exists?

**Reasoning:** The component assumes callback behavior will not require its locked state, while the callback assumes reentrancy. This can deadlock or violate invariants. Specify callback protocol, release internal locks before foreign behavior, serialize through a queue, or explicitly support reentrancy with a proven synchronization design.

**Conclusion:** Connector protocol includes control and synchronization assumptions.

### Example 7

**Question:** An API gateway authenticates a user, and downstream services trust an unsigned user header. Is the attachment secure?

**Reasoning:** Any caller reaching downstream may forge the header. Define authenticated workload and user identity propagation, integrity protection, audience, expiry, authorization at the resource owner, network paths, and audit. The gateway's role does not replace downstream authority.

**Conclusion:** Identity and authorization obligations cross every relevant attachment.

### Example 8

**Question:** Four service replicas use one database. How should availability be drawn?

**Reasoning:** Show four component instances, routing connector, and one shared-data instance plus its real redundancy. The service replicas tolerate one instance loss but not necessarily database, identity, DNS, or control-plane loss. Test the scoped failure configurations.

**Conclusion:** Instance views expose common dependencies hidden by type-level redundancy.

### Example 9

**Question:** A consumer accepts schema version 2 fields but interprets timestamps as local time while the producer emits UTC. Are they compatible?

**Reasoning:** Schema validation can pass while semantic interpretation shifts deadlines. Specify timezone and instant representation, version meaning, unknown fields, clock source, conversion, boundary cases, and compatibility tests. Adapt explicitly if historical data used different rules.

**Conclusion:** Semantic and temporal compatibility exceed structural schema compatibility.

### Example 10

**Question:** How should a remote patient-monitoring runtime view represent alarms?

**Reasoning:** Show sensor, validation, patient device, transmission, ingestion, rule evaluation, clinician queue, notification channels, acknowledgment, escalation, audit, and support components and connectors. Specify units, sample time, identity, loss, duplication, delay, offline buffering, priority, alarm authority, accessibility, and manual recovery. No external medical, clinical, device, telecommunications, accessibility, privacy, safety, regulatory, security, human-factors, or practitioner review is claimed; qualified authorities must validate thresholds, protocols, evidence, release, and residual risk.

**Conclusion:** High-consequence connectors require end-to-end protocol and authority assurance.

## Cross-Program Connections

- [Software Engineering: Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) owns detailed object and functional collaboration inside architectural components.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns protocol, contract, integration, concurrency, and fault-test methods.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns transaction, isolation, storage, and query mechanisms behind shared-data connectors.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) owns transport behavior, routing, congestion, and network failure beneath logical connectors.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns threat, identity, authorization, protocol protection, and security verification.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns ordering, delivery, replication, consensus, and partial-failure algorithms used by connectors.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 42010:2022, Software, systems and enterprise—Architecture description](https://www.iso.org/standard/74393.html), edition 2, November 2022. Architecture descriptions, viewpoints, views, model kinds, and correspondence; consulted 2026-09-06.
2. Robert Allen and David Garlan. [Formalizing Architectural Connection](https://doi.org/10.1109/ICSE.1994.296767), *Proceedings of the 16th International Conference on Software Engineering*, 71–80, May 1994. Primary work treating connectors as protocol-bearing architectural entities; consulted 2026-09-06.
3. Paul Clements, Felix Bachmann, Len Bass, David Garlan, James Ivers, Reed Little, Paulo Merson, Robert Nord, and Judith Stafford. *Documenting Software Architectures: Views and Beyond*, 2nd edition. Addison-Wesley, 2010. Component-and-connector structures, ports, roles, attachments, styles, and documentation.
4. James Ivers, Paul Clements, David Garlan, Robert Nord, Bradley Schmerl, and Oviedo Silva. [Documenting Component and Connector Views with UML 2.0](https://www.sei.cmu.edu/library/documenting-component-and-connector-views-with-uml-20/), CMU/SEI-2004-TR-008, April 2004. Component-and-connector semantics and notation mapping; consulted 2026-09-06.
5. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, 4th edition. Addison-Wesley, 2021. Runtime structures, quality-attribute tactics, scenarios, and evaluation.
6. Mary Shaw and David Garlan. *Software Architecture: Perspectives on an Emerging Discipline*. Prentice Hall, 1996. Components, connectors, configurations, and architectural styles.
7. George T. Heineman and William T. Councill, editors. *Component-Based Software Engineering: Putting the Pieces Together*. Addison-Wesley, 2001. Component contracts, composition, and mismatch.

## Exercises

### Exercise 1

Define runtime component, connector, port, role, attachment, configuration, protocol, and architectural mismatch for an order-fulfillment capability.

### Exercise 2

A queue starts with 1,000 jobs, receives 120 jobs/s, and processes 150 jobs/s. Under the simplified model, compute backlog after 20 seconds, time to empty if rates remain constant, and the result if processing falls to 100 jobs/s.

### Exercise 3

Diagnose a diagram showing replicated services joined by generic arrows while omitting queues, shared database, identity, DNS, control plane, deadlines, retries, ordering, backpressure, and reconciliation.

### Exercise 4

Compare synchronous invocation, a durable queue, and publish-subscribe for accepting and distributing warehouse allocation work. Address authority, latency, capacity, delivery, ordering, duplicates, failure, security, and operation.

### Exercise 5

Design and assure component-and-connector views for an unfamiliar autonomous irrigation network. Separate logical interaction claims from physical, safety, deployment, and empirical evidence.

## Answers to the Exercises

### Answer 1

An order coordinator is a runtime component with active fulfillment behavior and state. Its `request-allocation` port requires an allocation protocol. A durable queue is a connector with producer, storage, delivery, acknowledgment, and consumer roles. Attaching the coordinator's producer port and warehouse worker's consumer port creates part of a configuration.

The protocol defines acceptance, identity, schema, ordering, retry, deadline, cancellation, outcome, and recovery. Architectural mismatch occurs if the coordinator treats broker acceptance as completed allocation while the worker promises only eventual attempt, or if the coordinator retries non-idempotently while the worker lacks deduplication. The configuration includes actual component and connector instances and attachments under declared routing and capacity.

### Answer 2

Net drain is $150-120=30$ jobs/s. After 20 seconds, backlog is $\max(0,1000-30(20))=400$ jobs. At constant rates, time from the initial state to empty is $1000/30\approx33.33$ seconds; from the 20-second point it is another $400/30\approx13.33$ seconds.

If service falls to 100 jobs/s while arrival remains 120, backlog grows by 20 jobs/s. After 20 seconds it would be $1000+20(20)=1400$ jobs. These values assume homogeneous work, constant rates, available service, and no admission, loss, priority, scaling, or batch effect; a real queue requires measured distributions and capacity limits.

### Answer 3

The diagram shows types or replicas without the connector mechanisms and common dependencies needed for quality reasoning. Define component instances or multiplicities and routing. Replace generic arrows with request-response, queue, event, shared-data, identity, resolution, and control connectors as applicable. Add ports, roles, authority, schemas, deadlines, cancellation, retry budget, idempotency, ordering, capacity, backpressure, error, and reconciliation.

Show database, DNS, identity, certificates, network, and control-plane sharing where they form common failures. Create normal, overload, dependency-loss, control-plane-loss, recovery, and adversarial projections. Reconcile code, deployment, data authority, operational controls, and observed configuration. Do not infer behavior merely from replica count.

### Answer 4

Synchronous invocation can return immediate accepted or rejected allocation but couples the requester to allocator latency and availability. It needs deadline, cancellation, ambiguous-outcome reconciliation, and safe retry. A durable queue can accept work during bursts or allocator outage, but broker acceptance is not allocation; it needs bounded capacity, operation identity, ordering scope, redelivery, poison handling, backlog objectives, result publication, and reconciliation.

Publish-subscribe fits distribution of an already authoritative allocation fact to several independent consumers, not competitive ownership of one command unless the protocol defines it. It needs subscription lifecycle, replay, per-subscriber isolation, schema evolution, and outcome observation. For allocation commands, a partitioned durable queue with one authoritative consumer per allocation key may fit; publish allocation decisions afterward. Protect identity and warehouse authority, preserve inventory consistency, measure peak and recovery rates, and assign broker and on-call ownership. Select from actual scenarios rather than fashion.

### Answer 5

Show field sensors, local controller, weather-input adapter, policy evaluator, valve-command coordinator, actuator, operator console, alerting, audit, configuration, and update control as components. Connect them through sampled telemetry, validated state, command, observed actuation, acknowledgment, alarm, manual override, and configuration protocols. State units, time validity, identity, authorization, ordering, loss, duplication, offline buffering, capacity, safe state, and reconciliation.

Logical attachment evidence can include contract review, finite protocol models, schema and unit checks, integration tests, selected fault injection, traces, and configuration comparison. It cannot establish sensor calibration, hydraulic behavior, radio coverage, actuator safety, environmental impact, human response, power continuity, or field readiness. Link physical, deployment, security, hazard, accessibility, and operational views.

No external agronomy, hydrology, environmental, radio, controls, electrical, accessibility, safety, regulatory, security, human-factors, or practitioner review is claimed. Named qualified authorities, operators, and affected communities must approve limits, authority, protocols, tests, release, and residual risk. Unknown safe water bounds, unverified actuation, ambiguous override, inaccessible alarms, failed offline behavior, or unresolved shared control failure blocks readiness.
