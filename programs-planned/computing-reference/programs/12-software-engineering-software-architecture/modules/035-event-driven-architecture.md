---
module_id: SARCH-035
program: Software Engineering: Software Architecture
level: 1
module_number: 35
title: Event-Driven Architecture
status: complete
last_verified: 2026-09-06
---

# Event-Driven Architecture

## One-Page Review

### Governing question

When should components coordinate by publishing and reacting to events, and how can architects preserve authority, causality, compatibility, delivery, failure, and operability without turning asynchronous flow into invisible coupling?

### Essential definitions

- An **event** is an immutable record that a fact of architectural interest occurred, with identity, type, subject, occurrence time, producer authority, and schema.
- A **command** asks an identified authority to attempt an action; an event reports an occurrence. A message's grammar does not determine which it is.
- An **event producer** is authoritative for asserting an event type under stated conditions; a **consumer** interprets and reacts to it.
- An **event channel** carries events under declared delivery, ordering, retention, replay, capacity, and access semantics.
- An **event broker** mediates publication and consumption; it does not define business meaning or end-to-end correctness.
- **notification** announces that something changed; **event-carried state transfer** includes enough state for consumers to update local views without a synchronous callback.
- **choreography** distributes workflow decisions among reactions; **orchestration** gives an explicit coordinator authority over workflow state and commands.
- **idempotent effect** reaches the same relevant state after repeated application of the same identified request or event.
- **eventual consistency** permits related views to differ temporarily under a convergence protocol; it does not mean “probably consistent later.”
- **event sourcing** derives current aggregate state from an authoritative event history; it is distinct from using events for integration.

### Central model, mechanism, or theorem

Represent an event as $e=(id,type,subject,source,t_o,t_r,schema,payload,context)$, separating occurrence time $t_o$ from record or receive time $t_r$. Let $pub(p,e)$ assert producer $p$ is authorized to publish $e$, and let $C(type)$ be its consumers.

At-least-once delivery permits repeated delivery, so a consumer claiming duplicate-safe processing for event $e$ needs a deduplication or idempotency property such as

$$
apply(apply(S,e),e)=apply(S,e)
$$

for the relevant state and effect boundary. Broker acknowledgment alone cannot establish this property for external effects.

### Critical invariants

- distinguish event, command, request, notification, state transfer, log record, and audit record;
- give every event stable identity, semantic type, subject, source authority, occurrence time, schema/version, and trace context;
- publish facts only after their authoritative state transition, or use an atomic outbox or equivalent protocol;
- define delivery, duplicate, ordering, retention, replay, capacity, and acknowledgment semantics per channel;
- make consumer idempotency, deduplication scope, retry, quarantine, and reconciliation explicit;
- preserve per-subject causality or expose versions when consumers depend on order;
- own workflow state explicitly; choreography must not hide circular or conflicting authority;
- evolve schemas and semantics compatibly across independently changing producers and consumers;
- apply backpressure and overload policy across producers, brokers, and consumers;
- minimize sensitive payloads and govern access, retention, deletion, and replay;
- observe causal chains, lag, failure, duplicate, poison, and terminal business outcomes;
- never equate accepted publication, broker durability, consumer acknowledgment, and completed business effect.

### Common failures

Common failures include naming commands in past tense; treating database change records as domain events; dual-writing state and events; assuming exactly-once effects from broker settings; using timestamps as total order; retrying non-idempotent consumers; broadcasting sensitive state; adding consumers with no ownership; circular choreography; infinite retention; silent schema reinterpretation; poison events blocking partitions; synchronous callbacks disguised as events; and tracing technical delivery without reconciling business outcomes.

### Compact example

Orders commits order state and an `OrderPlaced` outbox record in one local transaction. A relay publishes event identity `o-17:v3`; Inventory records that identity before reserving stock. If delivery repeats after a lost acknowledgment, Inventory recognizes the same event and does not reserve twice. Payment remains a separate effect with its own idempotency key and unknown-outcome reconciliation.

### Connections

[SARCH-034](034-pipe-and-filter-systems.md) develops staged flow, queues, backpressure, and end-to-end outcomes. [SARCH-036](../ROADMAP.md) next examines client-server architecture. Distributed Systems owns consensus, replication, delivery, and workflow algorithms; Data Engineering owns large-scale event-time processing; API Engineering owns message contract detail.

## Governing Question

Event-driven systems replace some direct requests with statements of fact and reactions. Producers can avoid knowing every consumer, consumers can build independent views, and work can proceed asynchronously. This supports extensibility, temporal decoupling, audit, and scale.

The apparent decoupling is incomplete. Consumers still depend on event meaning, identity, timing, authority, delivery, and retention. A workflow spread among reactions can become harder to understand than a direct call chain. The governing question is which coordination should be event-driven and how to make the remaining coupling explicit and operable.

## Why This Matters

Events fit systems where facts have several legitimate consumers, immediate synchronous completion is unnecessary, disconnected work must resume, or local authorities maintain independent state. They can protect producers from consumer-specific integration and enable replayable projections.

They also create stale views, duplicate delivery, order ambiguity, poison messages, hidden workflows, privacy copies, and operational backlog. A single user action can trigger effects minutes later across several owners. Without stable identity and outcome reconciliation, “message delivered” becomes a false substitute for business correctness.

Architecture must therefore describe semantic, transactional, temporal, operational, and governance contracts—not merely select a broker.

## Prerequisites and Retrieval

Retrieve event, command, fact, authority, message, channel, broker, publish, subscribe, schema, identity, occurrence time, receive time, causal order, duplicate, idempotency, retry, acknowledgment, transaction, outbox, inbox, replay, retention, backpressure, choreography, orchestration, state machine, eventual consistency, and reconciliation.

From SARCH-024 retrieve send/receive events, happens-before, correlation, and timeout ambiguity. From SARCH-026 retrieve data meaning, lineage, authority, and lifecycle. From SARCH-032 retrieve module events and data ownership. From SARCH-034 retrieve pipes, capacity, ordering, poison items, side effects, and end-to-end invariants.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish events from commands, notifications, state transfers, logs, and audit records;
2. define event identity, authority, time, schema, and semantic contracts;
3. choose event-driven collaboration from architectural forces rather than broker fashion;
4. reason about atomic publication, acknowledgment, duplicates, ordering, and replay;
5. design idempotent consumers and reconcile unknown external effects;
6. compare choreography and orchestration for multi-step workflows;
7. evolve event schemas and meaning across independent lifecycles;
8. control backpressure, poison events, retention, privacy, and security;
9. observe causal chains and terminal business outcomes;
10. evaluate event-driven claims using bounded structural, executable, and operational evidence.

## Core Exposition

**Start with facts and authority.** An event says something occurred: `OrderPlaced`, `PaymentAuthorized`, or `TemperatureThresholdExceeded`. The producer must have authority or evidence to assert that fact. A message called `AuthorizePayment` asks an authority to act and is a command even if sent through a topic.

Past-tense naming helps but is not proof. `CustomerDeleted` can be an event, a disguised instruction telling every consumer to erase data, or an ambiguous lifecycle claim. Define subject, scope, authority, preconditions, and meaning.

**Separate event from transport envelope.** An event has domain or system semantics. Its envelope may contain channel identifiers, partition key, delivery attempt, signature, trace context, content type, and schema reference. Keep transport metadata from silently redefining the fact.

The CloudEvents 1.0.2 specification provides a common event envelope with attributes including identifier, source, specification version, type, optional subject and time, and data content metadata [1]. Using that envelope supports interoperability but does not define business authority, delivery, order, or payload semantics.

**Choose event-driven collaboration for a reason.** Good forces include multiple unknown consumers, asynchronous work, disconnected operation, independent read views, audit-worthy state transitions, burst absorption, and distinct authority boundaries. Direct request-response is often clearer when a caller needs an immediate result from one known authority.

Do not publish every setter invocation. Choose facts stable enough for consumers to rely on and significant enough to govern. Excessively fine events expose implementation sequence; excessively broad events force consumers to retrieve missing state or parse unrelated data.

**Classify event shapes.** A notification says a subject changed and may require a callback. It minimizes payload duplication but creates temporal coupling to the source and can cause a read surge. Event-carried state transfer includes consumer-relevant facts, enabling local views but increasing payload, privacy, and compatibility responsibility.

A delta says what changed; a snapshot says current state. Deltas are compact but require order and starting state. Snapshots tolerate missed intermediate changes but cost more and can overwrite newer consumer state. Choose by consumer need and source authority.

**Define identity.** Event identity distinguishes one fact record from retries. Subject identity locates the entity or stream to which it applies. Command identity distinguishes one requested operation. Effect identity protects a downstream side effect.

Do not generate a new event identity on every delivery retry; that defeats deduplication. If a correction supersedes an earlier fact, issue a new identity with explicit relation rather than mutate the historical event silently.

**Separate time domains.** Occurrence time is when the fact happened under the producer's model. Record time is when it was persisted. Publish time is when the broker accepted it. Receive and process times belong to consumers. These can differ and clocks can be wrong.

Do not sort unrelated events by wall-clock timestamp and call the result causal. Preserve per-subject versions, producer sequence, or explicit causation where order matters. Cross-source order requires a stronger protocol than timestamp comparison.

**Define delivery semantics end to end.** A channel may lose, duplicate, reorder, delay, retain, or redeliver events according to its contract. “At most once,” “at least once,” and “exactly once” require a named boundary. A broker can deduplicate its records while an external payment effect duplicates.

Map milestones: source transaction committed; outbox record durable; broker accepted; consumer received; consumer state committed; external effect resolved; business workflow terminal. Acknowledgment must name one milestone. Monitoring the wrong one creates false health.

**Prevent dual-write gaps.** Updating authoritative state and publishing separately can create state without an event or an event without state. When both use one local database, store state and an outbox record atomically. A relay publishes pending records and marks progress.

The relay can publish twice around a crash, so consumers still need duplicate safety. Change-data capture can transport committed changes but raw row mutations are not automatically stable domain events. Translate source internals into governed event meaning.

**Design idempotent consumers.** If applying the same identified event twice should have one effect, record processed identity in the same transaction as local state when possible, or design a naturally idempotent assignment such as “set projection version to 7 if older.”

Deduplication has scope and retention. If identities expire before late replay, duplicates can return. A check separate from an external effect has its own crash gap. Payment, email, and device effects need provider idempotency, outcome queries, or reconciliation—not only an inbox table.

**Define ordering scope.** Global total order is expensive and rarely necessary. Per-subject or per-partition order often matches invariants. The partition key must remain stable and sufficiently distributed. Hot subjects limit throughput.

Even an ordered channel may redeliver old events. Consumers should use subject version, expected predecessor, or monotonic transition checks. Concurrent producers for one subject require an authority or concurrency protocol; a shared key alone does not resolve conflicting facts.

**Make eventual consistency a protocol.** Identify authoritative state, derived views, update mechanism, expected delay, conflict policy, repair, and user-visible behavior. State what “converged” means. Bound staleness where the decision requires it.

A user who submits an order and immediately queries a lagging view may see absence. Provide read-your-write routing, a pending state, monotonic version, or clear status. Do not tell users merely to refresh later when the architecture can express progress.

**Compare choreography and orchestration.** In choreography, components react to facts without one central workflow controller. It supports local autonomy and easy addition of reactions. Long flows can become implicit, circular, and difficult to cancel or explain.

In orchestration, a coordinator owns workflow state, issues commands, observes outcomes, handles timeout, and decides compensation. This makes progress and authority visible but centralizes process knowledge. A hybrid can publish domain facts while an explicit process manager owns one cross-authority workflow.

Choose based on workflow invariants, human review, deadline, cancellation, audit, and change. Do not call an undocumented chain “choreography” to avoid naming an owner.

**Handle failure as state.** Consumer failure can be transient, deterministic, permission-related, schema-related, or an exhausted dependency. Classify errors. Retry only safe transient cases with bounded attempts, delay, jitter, and budgets.

Quarantine poison events with original bytes, schema, source, identity, cause, processing history, and access control. Decide whether the partition may advance. Assign an owner and correction/replay process. A dead-letter queue is a backlog of unresolved outcomes.

**Apply backpressure across the system.** Brokers decouple short bursts but not sustained overload. Monitor consumer lag and age, partition skew, retry amplification, storage, and recovery time. Limit producers or admission when downstream capacity is exhausted.

Prioritize or isolate critical event classes. Reserve control capacity so pause, recovery, or cancellation is not blocked by data backlog. Retention expiry under lag is data loss and must trigger a governed response.

**Evolve schemas compatibly.** Producers and consumers deploy independently only if event contracts tolerate overlap. Define required and optional fields, defaults, unknown fields, enum extension, numeric units, precision, and semantic versioning policy.

Structural compatibility is insufficient. Changing `amount` from minor currency units to decimal major units can parse successfully and be catastrophically wrong. Add explicit units or a new field/type, support overlap, test mixed versions, and preserve event schema identity.

**Evolve meaning conservatively.** An event is part of consumers' history. Reinterpreting an existing type silently changes replay results. Publish a new type or version when meaning changes materially, provide migration, and document whether old history is transformed, upcast, or interpreted by historical rules.

Consumer-driven contract tests can reveal known incompatibility but not unknown consumers. Maintain registration, ownership, deprecation windows, telemetry, and communication. Public event channels require even stronger governance.

**Distinguish integration events from event sourcing.** Integration events communicate facts between boundaries. Event sourcing stores an aggregate's authoritative state transitions as events and reconstructs state by replay. A system can use either, both, or neither.

Publishing integration events does not make a service event-sourced. A broker log is not necessarily the domain's authoritative history. Event sourcing adds aggregate versioning, deterministic evolution, snapshot, upcasting, correction, privacy, and projection obligations.

**Control coupling honestly.** Events reduce location and direct consumer knowledge, and asynchronous delivery reduces simultaneous availability needs. They retain semantic, schema, temporal, capacity, and workflow coupling. Consumers may depend on undocumented event order or producer internals.

Map producers, consumers, event types, data ownership, channels, partitions, workflows, and teams. Review fan-out, fan-in, cycles, and orphan consumers. A producer may need to know no consumer names while still carrying their combined compatibility burden.

**Design security and privacy.** Authenticate publishers where threat assumptions require it, authorize event types and subjects, validate schemas and sizes, protect channel integrity and confidentiality, and isolate tenants. Do not trust a message merely because it arrived through an internal broker.

Minimize personal and secret data. Events, replicas, retries, logs, quarantines, backups, and replay multiply copies. Define purpose, retention, deletion or cryptographic erasure, subject access, and restricted fields. An immutable business history cannot override applicable privacy obligations by architectural preference.

**Observe causal and business outcomes.** Propagate correlation and causation identifiers, but do not expose sensitive or high-cardinality payloads as metric dimensions. Measure publication delay, consumer lag and age, throughput, error, retry, duplicate, quarantine, and partition skew.

Trace from initiating command through authoritative fact to required terminal outcomes. Reconcile by identity and reason. A broker with zero lag can still deliver semantically rejected events or fail to complete a payment.

**Test contracts and failure.** Validate event examples against schemas, then test semantic boundaries, unknown fields, mixed versions, duplicates, reorder, gaps, replay, stale events, poison input, oversize payloads, unauthorized publishers, lag, retention, and consumer restart.

Fault-inject around source commit, outbox relay, broker acknowledgment, consumer state, external effect, and consumer acknowledgment. Test choreography timeout, cancellation, compensation, and reconciliation. A local happy-path broker test is weak evidence for production recovery.

**Govern topology.** Catalogue event types, owners, source authority, schemas, channels, consumers, sensitive fields, retention, ordering, and service objectives. Review new consumers and payload expansion. Delete abandoned subscriptions and quarantines.

Version diagrams and generated topology with observation windows. Runtime discovery misses dormant consumers and proposed flows. Compare intended contracts with configuration, schemas, code, broker metadata, traces, incidents, and owners.

**Know when not to use events.** Direct calls fit immediate validation and a single known authority. Local transactions fit tightly coupled invariants. A modular monolith may use direct module contracts more clearly than an in-process event bus.

Do not add asynchronous failure merely for fashion. Use events where the fact and its independent reactions are first-class; keep commands and queries explicit where intent and response matter.

## Definitions and Notation

Let an event be $e=(id,type,subject,source,t_o,t_r,v,p,c)$, where $v$ is schema/semantic version, $p$ payload, and $c$ context including causation and correlation. Let $P$ be producers, $C$ consumers, and $T$ event types.

Authority relation $Auth\subseteq P\times T$ declares which producer may assert each type. Subscription relation $Sub\subseteq C\times T$ declares intended consumption. These relations do not establish runtime delivery or authorization enforcement by themselves.

For consumer state $S$, duplicate-safe application for event $e$ requires $apply(apply(S,e),e)=apply(S,e)$ over the relevant state and effect boundary. If external effect $g$ is outside that boundary, a separate stable key and reconciliation protocol are required.

Let $v_s(e)$ be a per-subject version. A consumer requiring sequential state can accept $e$ only when $v_s(e)=current(subject)+1$, treat older versions as duplicate/stale, and hold or recover gaps according to policy.

## Mechanisms, Invariants, or Proof Structure

**Fact-authority invariant.** Each event type has an authoritative producer condition. Consumers do not infer authority from channel location alone.

**Atomic-publication invariant.** The authoritative state transition and durable publication intent cannot diverge silently. Outbox or an equivalent transaction protocol closes the local dual-write gap; relay duplicates remain possible.

**Identity invariant.** Redelivery preserves event identity. Corrections and new facts receive new identities with explicit causation or supersession.

**Duplicate-safety limitation.** State idempotency does not imply external-effect idempotency when the effect occurs outside the atomic deduplication boundary. The equation's state $S$ must include every claimed effect or the claim must be narrowed.

**Order invariant.** Consumers depend only on the declared order scope and detect stale versions or gaps when those affect correctness. Wall-clock timestamps are never treated as universal total order.

**Workflow-authority invariant.** Every multi-step business outcome has an owner or explicit distributed rule for progress, timeout, cancellation, compensation, and terminal state.

**Compatibility invariant.** An accepted event remains interpretable under its published semantic contract for the governed retention and replay horizon, or a migration/upcast rule is supplied.

**Outcome invariant.** Each accepted initiating identity reaches an authorized terminal business state or remains visibly pending with owner and deadline. Delivery counters alone do not discharge this invariant.

## Alternatives and Trade-Offs

**Event versus request.** Events support independent reactions and temporal decoupling. Requests make intent, authority, and immediate outcome explicit. Many workflows need commands into authorities and events out.

**Notification versus state transfer.** Notifications minimize payload and preserve source authority but trigger callbacks and source load. State transfer supports local reads and disconnection but multiplies data and semantic responsibility.

**Choreography versus orchestration.** Choreography distributes change and avoids a central controller but hides long-flow state. Orchestration makes progress and recovery explicit but centralizes workflow policy.

**At-most-once versus at-least-once.** At-most-once avoids redelivery but can lose work. At-least-once supports recovery but requires duplicate-safe state and effects. Boundary-specific deduplication can offer stronger records without universal exactly-once claims.

**One shared channel versus typed channels.** Shared infrastructure simplifies operation and discovery but increases blast radius and access complexity. Separate channels isolate capacity, security, order, and retention at operational cost.

**Short versus long retention.** Short retention reduces cost and sensitive-data exposure but limits recovery and new projections. Long retention enables replay but creates schema, privacy, deletion, and operational obligations.

**Broker integration versus database outbox.** Direct broker publication is simple but risks dual-write divergence. Outbox aligns local state and intent but adds relay, duplicate, cleanup, and lag operations.

## Failure Modes and Misconceptions

1. **“Past tense makes a message an event.”** Authority and semantics determine fact versus disguised command.
2. **“Events eliminate coupling.”** Semantic, schema, temporal, capacity, and workflow coupling remain.
3. **“The broker owns business meaning.”** It transports records; domain authorities own facts.
4. **“A database change is a domain event.”** Row mutations expose storage decisions unless translated.
5. **“Publish after commit is safe.”** A crash between state and publication creates divergence.
6. **“Exactly once delivery means exactly once effect.”** External effects and crash boundaries remain.
7. **“Timestamps order events.”** Unsynchronized clocks cannot establish all causality.
8. **“Retries are harmless.”** Non-idempotent or unknown effects can duplicate harm.
9. **“Eventual consistency needs no bound.”** Users and decisions require progress and convergence policy.
10. **“Choreography has no owner.”** Outcomes, timeouts, and compensation still require authority.
11. **“A dead-letter queue solves poison events.”** It defers them and creates ownership and retention work.
12. **“Schema compatibility preserves meaning.”** Units, defaults, and interpretations can change.
13. **“Event-driven means event-sourced.”** Integration and authoritative state reconstruction are distinct.
14. **“Zero lag means healthy.”** Consumers can process incorrectly or fail external outcomes.
15. **“More events mean more flexibility.”** Fine-grained internals and uncontrolled fan-out increase coupling.

## Worked Examples

### Example 1

**Situation.** A message called `PaymentAuthorized` asks a payment component to attempt authorization.

**Reasoning.** The message describes an intent, not an occurred fact. Rename it `AuthorizePayment` and route it to the payment authority. On successful provider resolution, Payment publishes `PaymentAuthorized`; on refusal, it publishes or returns a distinct outcome under the workflow contract.

**Conclusion.** Commands request decisions; events record authoritative outcomes.

### Example 2

**Situation.** Orders commits state, then the process crashes before publishing `OrderPlaced`.

**Reasoning.** The separate writes created a lost event. Commit an outbox record in the order transaction. A relay later publishes the stable identity. Monitor outbox age and retry. Consumers remain duplicate-safe because the relay can crash after publish but before marking progress.

**Conclusion.** Atomic publication intent closes the local loss gap but does not remove duplicates.

### Example 3

**Situation.** Inventory receives event version 12 before version 11 for one product.

**Reasoning.** If inventory projection requires sequential deltas, hold 12, request or await the gap, and alert after a bound. A snapshot event could supersede both if its version and semantics permit. If operations commute, document that proof rather than imposing sequence.

**Conclusion.** Ordering response follows the consumer invariant, not a universal FIFO assumption.

### Example 4

**Situation.** An email consumer sends a receipt, crashes, and receives the event again.

**Reasoning.** Recording the event after send leaves an unknown outcome. Use a stable message key supported by the provider, query delivery outcome where possible, or record durable send intent and reconcile. An inbox alone cannot atomically cover a remote provider.

**Conclusion.** Duplicate-safe local state does not automatically protect external effects.

### Example 5

**Situation.** Five choreographed services react in a cycle, and no one can tell whether a refund is complete.

**Reasoning.** Model states, commands, events, timeouts, and compensation. Assign a process manager ownership of refund progress while services retain domain authority. Publish terminal facts and expose pending/failed state. Remove reactions that duplicate decisions.

**Conclusion.** Explicit orchestration can recover visibility when choreography hides workflow authority.

### Example 6

**Situation.** A consumer has processed no events for two minutes, but broker queue length is zero.

**Reasoning.** Check publication, partition assignment, retention, source outbox, schema rejection, and consumer offsets. Zero visible queue can mean producers stopped, events expired, or the metric excludes assigned partitions. Reconcile initiating identities to terminal outcomes.

**Conclusion.** Broker-local metrics need source and business context.

### Example 7

**Situation.** Version 2 changes temperature values from Celsius to Fahrenheit without changing the numeric field.

**Reasoning.** Parsing succeeds while meaning breaks. Add an explicit unit and new semantic version or event type, deploy consumers that handle both, test boundary values, and retain original version for replay. Never infer units from deployment date alone.

**Conclusion.** Semantic compatibility is stricter than structural schema compatibility.

### Example 8

**Situation.** A poison event retries 100 times per second and blocks a customer partition.

**Reasoning.** Classify the deterministic schema or data failure, bound attempts, quarantine with provenance and access control, and decide whether subject order permits later items. Alert the owning producer and consumer. Provide correction and replay while preventing retry amplification.

**Conclusion.** Poison handling requires order, ownership, and remediation policy.

### Example 9

**Situation.** A customer event broadcasts full address and birth date to twenty consumers, most of which need only customer region.

**Reasoning.** Minimize the integration event or publish access-controlled projections by purpose. Catalogue consumers and retention, encrypt, audit, and remove unused subscriptions. Govern deletion and replay copies. Do not use convenience to create uncontrolled personal-data replicas.

**Conclusion.** Event fan-out multiplies privacy and governance obligations.

### Example 10

**Situation.** A rail network publishes track occupancy, route setting, train position, and signal aspects across operational regions.

**Reasoning.** Define authoritative producers, subject versions, occurrence and receive time, safety modes, ordering, stale thresholds, and regional partition behavior. Commands to set routes remain distinct from observed facts. Safety interlocks do not rely solely on asynchronous integration events. Test duplicates, gaps, reordering, clock faults, partitions, replay, overload, unauthorized publishers, operator interpretation, and recovery.

**Conclusion.** Safety-related event integration needs explicit authority and independent safeguards beyond broker delivery.

## Cross-Program Connections

- **Distributed Systems:** ordering, delivery, consensus, replication, sagas, idempotency, clocks, and partitions deepen event mechanisms.
- **Data Engineering:** logs, windows, watermarks, joins, checkpoints, replay, lineage, and stream processing deepen event-time computation.
- **API and Service Engineering:** schemas, compatibility, errors, idempotency, and contract governance apply to asynchronous APIs.
- **Database Engineering:** transactions, logs, change capture, outboxes, isolation, and projections connect state and publication.
- **Security Engineering:** publisher identity, authorization, payload validation, tenant isolation, confidentiality, and audit govern channels.
- **Software Delivery and Reliability Engineering:** lag objectives, capacity, incidents, retry storms, quarantine, recovery, and reconciliation govern operations.
- **Testing and Quality Engineering:** contract, compatibility, property, load, fault, replay, and end-to-end outcome tests provide complementary evidence.
- **Software Design and Domain Modeling:** domain events, aggregates, bounded contexts, process managers, and authority determine event meaning.

## References

1. Cloud Native Computing Foundation, *CloudEvents — Version 1.0.2*, 3 February 2022. Official specification; current stable core version checked 2026-09-06. https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md
2. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns*, Addison-Wesley, 2003.
3. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
4. Chris Richardson, *Microservices Patterns*, Manning, 2018.
5. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003.
6. Vaughn Vernon, *Implementing Domain-Driven Design*, Addison-Wesley, 2013.
7. Pat Helland, “Life beyond Distributed Transactions: An Apostate's Opinion,” in *CIDR 2007*, 2007. http://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf
8. Tyler Akidau et al., “The Dataflow Model,” *Proceedings of the VLDB Endowment*, vol. 8, no. 12, 2015. https://doi.org/10.14778/2824032.2824076

## Exercises

### Exercise 1

Precisely distinguish event, command, notification, event-carried state transfer, integration event, event sourcing, producer authority, channel acknowledgment, choreography, orchestration, and eventual consistency.

### Exercise 2

A consumer receives subject versions 4, 5, 5, 7, and 6 in that order. Define its behavior when it requires sequential deltas and has durable deduplication. Explain what changes if events are complete snapshots.

### Exercise 3

Diagnose a system that updates a database then publishes directly, creates new identities on retry, acknowledges before an external effect, retries poison events forever, and stores full personal records in a long-retention dead-letter queue. Produce a repair.

### Exercise 4

Compare notification, event-carried state transfer, synchronous query, and a consumer-owned projection for customer risk status. Address authority, freshness, privacy, failure, load, compatibility, and user-visible consistency.

### Exercise 5

Transfer event-driven architecture to a regional emergency-water system involving sensors, treatment plants, pumps, laboratories, operators, public warnings, intermittent sites, safety interlocks, and regulatory evidence. Define events, commands, workflows, and assurance.

## Answers to the Exercises

### Answer 1

An **event** records an occurred fact; a **command** asks an authority to attempt action. A **notification** says something changed and may require a callback; **event-carried state transfer** includes consumer-relevant state. An **integration event** communicates a fact across a boundary; **event sourcing** reconstructs authoritative aggregate state from event history.

**Producer authority** is permission and semantic responsibility to assert an event type. A **channel acknowledgment** names a transport milestone, not necessarily a business effect. **Choreography** distributes workflow through reactions; **orchestration** gives a coordinator explicit workflow state and command authority. **Eventual consistency** is a defined convergence protocol allowing temporary divergence, not an unspecified delay.

### Answer 2

Starting at current version 3, accept and apply 4, then 5. Recognize the second 5 by identity or subject version as duplicate and do not repeat its effect. Hold 7 because 6 is missing. When 6 arrives, apply 6 then 7, assuming schemas and predecessor rules pass. Bound gap waiting, recover missing input or alert, and preserve ordering during restart.

For complete snapshots, version 7 may supersede missing version 6 if the contract says each snapshot fully represents required state and no intermediate effect is required. Apply only if 7 is newer than current. Still deduplicate external effects and retain audit or causation rules. A snapshot cannot skip an event whose independent business effect must occur merely because state fields are current.

### Answer 3

Store authoritative state and an outbox record atomically. Relay using the same event identity on retry and monitor outbox age. Define consumer acknowledgment after its declared local durable milestone. Protect the external effect with a stable effect key, provider idempotency or outcome query, durable intent, and reconciliation.

Classify failures and bound retry with backoff and budgets. Quarantine deterministic poison events with original provenance, schema, cause, and owner; decide partition progress and provide correction/replay. Minimize personal payloads before publication. Encrypt and restrict quarantine, set a purpose-bound retention and deletion process, audit access, and avoid copying full records when identifiers or controlled lookup suffice.

Finally test crashes around commit, relay, broker, consumer state, external effect, and acknowledgment; test duplicate, replay, poison, retention, access, and reconciliation. Broker delivery alone is not the success criterion.

### Answer 4

A notification preserves risk authority and minimizes copied data, but consumers must query and can create load or fail when the authority is unavailable. It can also collapse several changes. Event-carried state transfer supports local decisions and disconnection but copies sensitive risk data, needs semantic compatibility, and can become stale.

A synchronous query offers current authoritative evaluation under the service's availability and latency, with direct errors and access control. It creates temporal coupling and load. A consumer-owned projection supports fast local reads and independent operation but needs event identity, order, correction, lag objectives, reconciliation, privacy, and a visible pending/stale state.

Choose by decision tolerance. A high-stakes approval may synchronously confirm authority even if a projection guides the interface. A low-risk display may use a projection with version and age. Minimize fields and purpose, define failure and stale behavior, and avoid showing a lagging value as current. Test mixed schema versions, access, source outage, replay, correction, lag, and user comprehension.

### Answer 5

Authoritative events can include `SampleValidated`, `ContaminationConfirmed`, `PumpStateChanged`, `TreatmentModeEntered`, and `WarningIssued`, each with site, subject version, occurrence/receive time, units, confidence, source, schema, and causation. Commands such as `StopPump`, `CollectSample`, and `IssueWarning` go to named authorities with identity, authorization, deadline, and result. Raw sensor messages remain observations, not confirmed safety facts.

An explicit incident orchestrator can own investigation and warning progress while plants retain process-control authority and laboratories retain result authority. Publish facts through atomic local intent where possible; disconnected sites retain bounded signed records and reconcile on return. Consumers handle duplicates, gaps, stale events, corrections, and replay. Physical and local safety interlocks remain independent of broker availability.

Separate critical control capacity from analytics and public reporting. Define partition, overload, poison, retention, privacy, and regulatory evidence. Minimize personal/operator data, authenticate publishers, authorize subjects and commands, and protect quarantines. Public views state data age and warning authority.

Test sensor boundaries, calibration error, contradictory samples, duplicates, reorder, clock faults, link partitions, prolonged backlog, broker and site restart, schema rollout, unauthorized publication, command replay, operator override, warning delivery, reconciliation, and audit provenance. Trace each accepted critical identity to a terminal explained state. Drills and simulations remain bounded evidence; applicable human, safety, regulatory, and physical review is still required.
