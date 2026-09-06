---
module_id: SARCH-044
program: Software Engineering: Software Architecture
level: 1
module_number: 44
title: Asynchronous Messaging Integration
status: complete
last_verified: 2026-09-06
---

# Asynchronous Messaging Integration

## One-Page Review

### Governing question

When should systems exchange durable messages instead of waiting for immediate business completion, and how should the architecture define authority, delivery, ordering, duplication, backlog, compatibility, security, and outcome evidence across time?

### Essential definitions

- **asynchronous messaging** lets a sender continue after an agreed acceptance point without waiting for the receiver's final business result;
- a **message** is an immutable communication envelope carrying identity, type, version, routing data, relevant context, and payload;
- a **command** asks a named owner to attempt an action, an **event** states an observed fact, and a **document message** transfers a representation for another purpose;
- a **channel** is a logical communication path; a broker, log, queue, or topic is one implementation mechanism;
- **delivery** moves an attempt to a receiver, while **processing** interprets it and may commit effects;
- **acknowledgment** confirms only the contractually named stage, such as broker persistence or consumer processing;
- **at-most-once** delivery may lose a message but avoids broker redelivery; **at-least-once** delivery may repeat it; any stronger claim must name its scope and failure assumptions;
- **idempotent consumption** makes repeat handling under one message or operation identity preserve the intended effect;
- **ordering** is always relative to a scope, such as one partition key, producer epoch, or aggregate—not an unqualified global property;
- **backlog** is accepted work not yet completed; **lag** measures progress behind an authoritative position or time;
- a **dead-letter destination** isolates messages that cannot progress under a declared retry policy; it is not a correctness solution or archive;
- **replay** deliberately processes retained messages again under an explicit code, schema, state, authorization, and side-effect policy.

### Central model, mechanism, or theorem

Model a message path as producer transaction $P$, publication boundary $B$, channel $C$, delivery attempt $D_i$, consumer transaction $K$, and observable business outcome $O$. Each transition has different evidence. “Sent,” “accepted,” “persisted,” “delivered,” “acknowledged,” and “business complete” are not synonyms.

For arrival rate $\lambda$, sustainable processing capacity $\mu$, and interval $t$, a simplified backlog change is

$$
\Delta Q=(\lambda-\mu)t.
$$

During a complete $t$-second consumer outage, backlog growth is $\lambda t$. Under stable long-run conditions, Little's Law $N=\lambda W$ relates average in-system work, completion rate, and average time; it does not prove recovery capacity during overload.

### Critical invariants

- name the sender acceptance point and the receiver business outcome separately;
- assign one authority for each command decision and event fact;
- persist business change and publication obligation atomically, or expose the gap honestly;
- assume duplicates wherever acknowledgment or visibility can be lost;
- bind deduplication to stable identity, principal, semantic fingerprint, and retention;
- define ordering scope, partition key, producer epochs, and late-message policy;
- bound message size, arrival rate, partitions, concurrency, attempts, delay, backlog, retention, and replay;
- use retry only for classified transient failure, with backoff, jitter, expiry, and admission;
- isolate poison messages without silently skipping required work;
- evolve envelopes, payloads, errors, and semantics across mixed producer and consumer versions;
- authenticate publishers and consumers, authorize channel and business action, minimize data, and protect retained history;
- observe accepted messages, attempts, consumer effects, lag, age, discards, duplicates, and business outcomes independently;
- test crash windows, duplicate and out-of-order delivery, partitions, poison data, overload, replay, rollback, and recovery.

### Common failures

Common failures include returning success when only a broker accepted work; publishing after a database commit without closing the crash gap; calling every message an event; allowing many producers to announce another owner's facts; assuming exactly-once business effects; using trace IDs as deduplication keys; requiring global order; choosing a mutable partition key; retrying poison data forever; treating a dead-letter queue as completion; acknowledging before durable effect; replaying emails or payments; retaining sensitive messages indefinitely; changing meaning without changing version; and sizing only normal throughput rather than outage recovery.

### Compact example

A billing service accepts 500 invoice commands per second. A 15-minute consumer outage creates $500\times900=450{,}000$ messages. At 2 KB per message, raw payload alone is about 900 MB before broker indexes, replication, envelopes, and compression. If restored capacity merely equals 500/s, lag never falls. Recovery needs measured excess capacity, bounded retention, admission, and a business rule for commands that expire while waiting.

### Connections

[SARCH-035](035-event-driven-architecture.md) introduces the architectural style; [SARCH-041](041-system-of-record-boundaries.md) locates fact authority; [SARCH-043](043-synchronous-request-response-integration.md) provides the temporal alternative. [SARCH-045](../ROADMAP.md) next examines batch and file exchange. API Engineering owns protocol and schema implementation depth; Distributed Systems owns failure, time, and consistency theory.

## Governing Question

Asynchronous messaging decouples the sender's immediate progress from the receiver's completion. That can absorb bursts, survive temporary receiver failure, support independent reactions, and preserve work across restarts. It also creates durable intermediate states: accepted but not delivered, delivered but not processed, processed but not acknowledged, retried, expired, quarantined, or completed without the sender yet knowing.

The architectural task is to decide what the message means, who owns it, what acceptance proves, which histories must be durable, how duplicates and reordering affect state, how backlog remains bounded, and how users learn the final outcome. Selecting a broker or topic is secondary.

## Why This Matters

A synchronous chain holds caller resources while work proceeds. Messaging can turn that temporal dependency into a durable handoff. Order fulfillment may respond with a pending order, then allocate stock, arrange delivery, and notify the buyer independently. Telemetry producers can continue while consumers scale or restart. One fact can support several independent reactions.

The trade is explicit complexity. Immediate exceptions become later state transitions. Debugging crosses time and retained history. Duplicate delivery is normal under many useful failure policies. Ordering is scoped. Producers and consumers run different versions. Backlog consumes storage and can conceal an outage behind successful publishing. A replay may repeat real-world effects.

Good messaging architecture makes these states visible and bounded. Bad messaging architecture replaces a clear synchronous failure with silent, delayed, and difficult-to-reconcile inconsistency.

## Prerequisites and Retrieval

Retrieve service boundary, system of record, command, event, transaction, commit, message, channel, queue, topic, partition, producer, consumer, broker, log, acknowledgment, retry, idempotency, ordering, concurrency, queueing, throughput, latency, availability, consistency, authentication, authorization, schema, compatibility, observability, and recovery.

From SARCH-018 retrieve architectural evidence; SARCH-024 supplies runtime interaction views; SARCH-035 supplies event-driven style; SARCH-041 supplies fact authority; SARCH-042 supplies local transaction placement; and SARCH-043 supplies operation identity, deadlines, retries, and ambiguous outcomes.

## Learning Objectives

After completing this module, you should be able to:

1. state exactly what asynchronous acceptance and acknowledgment prove;
2. distinguish commands, events, documents, notifications, and internal records;
3. assign command and fact authority without hidden shared ownership;
4. close or expose database-to-message publication gaps;
5. design idempotent consumers for duplicate and uncertain delivery;
6. define ordering scope, partitioning, concurrency, and late-message handling;
7. budget throughput, backlog, retention, and recovery headroom;
8. classify retryable, poison, expired, and irrecoverable messages;
9. evolve message contracts safely across mixed deployments and replay;
10. design security, privacy, observability, testing, and user-visible outcome inquiry.

## Core Exposition

**Define the waited-for outcome.** Asynchrony is relative to a business outcome. A producer may synchronously wait for broker acceptance but not for fulfillment. A consumer may call another service synchronously while handling the message. Name each boundary.

If an order endpoint returns `202 Accepted`, the response should identify the pending operation and how to query or receive its outcome. Acceptance must not be described as shipment, payment, or completion. A useful asynchronous contract exposes progress and terminal failure instead of making the client guess.

**Choose message intent deliberately.** A command expresses imperative intent toward an owner: `ReserveInventory`. One handler or coordinated owner decides whether it can occur. An event expresses an observed fact in past tense: `InventoryReserved`. Consumers may react independently. A document transfers a representation, such as a price catalog, for a named integration purpose.

A notification is often a lossy hint that something may have changed; the receiver can query authority. A domain event is stronger: it is retained evidence that the owning domain observed a fact. A broker envelope is not automatically a domain fact. Naming every payload `SomethingEvent` does not remove command coupling.

**Assign authority before routing.** The inventory owner decides whether stock is reserved and publishes the resulting fact. A storefront may request the reservation but must not publish `InventoryReserved` on inventory's behalf. Multiple authoritative publishers make contradiction inevitable.

Shared facts still need semantic ownership, versioning, correction, and provenance. Subscribers own their reactions and local derived state. They do not acquire authority over the original fact merely by retaining a copy.

**Separate the message lifecycle.** A producer creates intent, commits local state, hands data to a publication mechanism, and may receive an acceptance. The channel retains or routes the message. A consumer receives an attempt, validates it, performs local work, records an outcome, and acknowledges at some stage.

Write a state model for each boundary. Does producer success mean stored in one broker memory buffer, durably replicated, or committed in the producer's database? Does consumer acknowledgment mean parsed, stored in an inbox, committed with the business effect, or merely scheduled? Protocol words alone do not answer the business question.

**Close the dual-write gap.** Suppose order state commits, then the process crashes before publishing `OrderPlaced`. The order exists but subscribers never learn. If publication happens first, the event may be observed for an order that later rolls back. Two independent writes do not become atomic because they are adjacent in code.

A transactional outbox stores the domain change and publication record in one local transaction. A relay later publishes the outbox entry and records progress. Crash after publication but before relay progress creates a duplicate, so consumers still need idempotency. Change-data capture can relay committed records, but capture position, schema, filtering, replay, and ownership are part of the contract.

Another design makes the message log the authoritative write and derives state from it. That changes the storage and recovery model; it is not simply “adding events.” Distributed transactions can coordinate supported participants but add availability, operational, and ownership constraints. Select the mechanism from invariants and failure consequences.

**Assume duplicate delivery.** With at-least-once delivery, a broker redelivers when acknowledgment is absent. The consumer may have committed and crashed before acknowledging. Redelivery is therefore the correct recovery action, not a broker defect.

An idempotent consumer records message or operation identity with the business effect in one local transaction. It verifies principal and semantic fingerprint so a reused key with different payload is rejected. Retention must exceed the maximum retry, delay, and replay horizon. Merely checking a short-lived cache before a separate write leaves a crash race.

Natural idempotency can help: setting an account status to a specified version is safer than incrementing it blindly. Even then, audit entries, emails, and external effects may repeat. Evaluate the complete effect, not only one table row.

**Scope every delivery guarantee.** At-most-once mechanisms may discard after an uncertain attempt. At-least-once mechanisms favor eventual redelivery and duplicates. “Exactly once” can describe broker record placement, transactional consumption within one system, or deduplicated effects under a key and retention window. It does not automatically mean one real-world business effect across arbitrary services and time.

Ask: exactly one what, observed by whom, within which boundary, under which identities, for how long, and under which failures? Prefer explicit mechanisms and residual failure states to an unqualified guarantee label.

**Define ordering narrowly.** A broker cannot give useful total order across unlimited publishers, partitions, regions, retries, and histories without strong coordination and throughput cost. Most domains need order only for one entity or aggregate.

Choose a stable partition key such as account ID so related messages reach one ordered lane. Sequence numbers or source versions allow consumers to detect gaps, duplicates, and late arrivals. Producer epochs distinguish a restarted or fenced writer. A consumer still needs a policy: buffer, fetch missing state, apply commutatively, ignore stale versions, or stop and reconcile.

Order of publication is not necessarily order of business time. Late facts can be valid. Clocks from different systems do not create a trustworthy total order by timestamp. Lamport's happened-before relation demonstrates that causal order is partial; unrelated events need not be ordered [1].

**Partition from domain and capacity forces.** More partitions permit more parallel consumption but make per-key imbalance, movement, and coordination visible. A hot tenant or popular item can dominate one partition. Random keys spread load but destroy entity order. Mutable keys move one entity between histories.

Estimate key distribution and worst-case work, not only message count. A 1 KB notification and a 1 KB image-processing command may have radically different cost. Bound consumer concurrency by downstream capacity as well as broker throughput.

**Treat backlog as product state.** A queue buffers a difference between arrival and processing. If $\lambda>\mu$, simplified backlog grows at $(\lambda-\mu)t$. If capacity equals arrival after recovery, accumulated lag never shrinks. Plan excess capacity or controlled admission.

Backlog age often matters more than depth. Ten thousand messages may be seconds at high throughput or days at low throughput. Measure oldest useful message, per-key lag, bytes, work estimate, and deadline or expiry. Expired commands need a domain outcome, not silent deletion.

Storage planning includes envelope, index, replication, transactions, segment overhead, and headroom. Retention serves recovery, audit, replay, or consumer independence, but each purpose has different privacy and correctness constraints.

**Use backpressure and admission end to end.** A durable broker can absorb a burst but cannot create processing capacity. Unlimited acceptance converts overload into storage exhaustion and intolerable delay. Producers need quotas and rejection semantics; consumers need bounded prefetch, concurrency, memory, and downstream demand.

Priority can protect urgent work, but starvation and tenant fairness need policy. Separate workloads when their consequences, capacity, retention, or security differ. A single global queue creates hidden coupling between unrelated products.

**Classify failures before retry.** Transient infrastructure failures may justify bounded retry. Invalid schema, impossible domain state, revoked authority, or deterministic code defects do not become healthy with repetition. Apply capped attempts or elapsed time, backoff, jitter, and broker pushback without blocking all unrelated keys.

A poison message repeatedly crashes or rejects a consumer. Quarantine it with original identity, authenticated provenance, failure class, code and schema versions, attempt history, and controlled inspection. Continue only when skipping it preserves ordering and business invariants. A dead-letter record is unresolved work, not success.

Operational re-drive must be authorized, rate-limited, idempotent, and observable. Repairing data or deploying code before redrive may change the correct action. Never let a dashboard button resend millions of effects without preview, scope, and rollback planning.

**Design time semantics.** Messages can carry creation time, event time, acceptance time, processing time, expiry, and business-effective time. State which clock and authority produced each value. Time-to-live can prevent obsolete work but cannot substitute for a terminal business result.

Delayed delivery supports reminders and scheduled attempts, but schedule precision, duplicate wakeups, cancellation, clock correction, and long retention need contracts. For critical schedules, persist business schedule state and derive messages rather than trusting one transient timer.

**Separate choreography and orchestration.** In choreography, services react to facts without one process controller. This supports local autonomy, but the end-to-end process and failure policy can become implicit. In orchestration, a process owner issues commands, records progress, and decides compensation or escalation. This improves visibility but introduces an authority and availability boundary.

Neither pattern guarantees consistency. Define business invariants, state transitions, timeouts, compensation limits, and manual resolution. Compensation is a new action that may fail; it is not time reversal.

**Evolve contracts across retained history.** Producers and consumers deploy independently, and old messages may remain for months. Envelope and payload versions, defaults, enum growth, units, identifiers, nullability, and semantic meaning must coexist.

Consumers should tolerate additive data they do not need while rejecting meaning they cannot interpret safely. Producers should not assume every historical consumer upgraded. A schema registry can enforce syntactic compatibility, but it cannot prove semantic compatibility such as changed currency units or side effects.

Replay makes compatibility two-dimensional: new code reads old data, and restored old code may read newer retained data. Record transformation versions and preserve raw authoritative input when lawful and useful. Test rollback and replay explicitly.

**Treat replay as a governed operation.** Replay can rebuild projections, recover from consumer defects, or introduce a new subscriber. It can also resend emails, charges, alerts, or partner commands. Classify handlers as pure projection, idempotent effect, externally effectful, or replay-forbidden.

Use a distinct replay run identity while preserving original message and business identities. Define source range, ordering, code version, destination, side-effect mode, capacity budget, validation, cutover, and abort. Rebuild into an isolated destination and compare before switching when possible.

**Preserve security through the channel.** Authenticate publishers and consumers as workloads. Authorize publish, subscribe, administration, replay, and business action separately. A consumer should not trust a payload solely because it arrived from an internal broker.

Protect integrity and provenance across relays. Restrict topic wildcards, tenant mixing, and administrative credentials. Encrypt transport and storage as required, but remember brokers, operators, schema systems, archives, and dead-letter stores may see plaintext or metadata.

Minimize personal and secret data. Retention, replicas, backups, replay, and dead letters make deletion and purpose limitation harder. Prefer stable references when receivers can lawfully query authority, but do not create a new synchronous dependency without analyzing it.

**Observe business outcomes, not broker health alone.** Measure producer acceptance and rejection, publication delay, partition skew, delivery attempts, age and depth, consumer success, deduplication, quarantine, expiry, re-drive, and downstream saturation. Correlate with stable operation and message identity without logging secrets.

A broker can be healthy while a consumer has silently stopped applying business effects. A low queue can mean fast processing or data loss. Reconcile authoritative facts with expected derived outcomes and expose pending, failed, and manually resolved states to users and operators.

**Test the crash matrix.** Crash before local commit, after local commit before outbox relay, after publish before relay checkpoint, after delivery before consumer commit, after consumer commit before acknowledgment, and during external side effect. Verify duplicates, missing acknowledgments, and recovery.

Also test out-of-order delivery, gaps, hot partitions, malformed and oversized messages, revoked credentials, schema mismatch, broker partition, retention pressure, consumer slowdown, replay, rollback, and disaster recovery. Assertions must inspect business state and evidence, not only that a handler returned.

**Know when not to use messaging.** If a caller needs a bounded current authoritative answer before acting, synchronous integration may be clearer. If data naturally arrives as large periodic sets, batch or file exchange may fit. If the receiver cannot expose pending and failed outcomes, asynchronous acceptance may mislead users.

Messaging is strongest for durable handoff, burst absorption, independent reactions, long-running processes, and reconstructable derived state. It is not a default substitute for clear ownership or a mechanism for making inconsistency disappear.

## Definitions and Notation

Let message $m$ have immutable identity $id(m)$, semantic type $type(m)$, schema version $v(m)$, authority $auth(m)$, partition key $p(m)$, source sequence $s(m)$ where defined, creation time, expiry, payload, and integrity metadata.

Let $A(m)=\{a_1,\ldots,a_k\}$ be delivery attempts. Consumer business effect $E(m)$ is distinct from receipt, handler return, and acknowledgment. Deduplication relation $same(m_1,m_2)$ requires the contract's identity scope and compatible semantic fingerprint, not equal trace IDs.

For arrival rate $\lambda$ messages/s, sustainable completion capacity $\mu$ messages/s, and interval $t$, simplified backlog change is $\Delta Q=(\lambda-\mu)t$. A complete consumer outage gives $\mu=0$ and growth $\lambda t$. Drain time for existing backlog $Q$ under constant excess capacity is $Q/(\mu-\lambda)$ when $\mu>\lambda$.

Ordering relation $\prec_k$ is defined only within key or partition scope $k$. Source version $s$ can detect duplicate ($s$ equal), next ($s+1$), gap ($s'>s+1$), or stale ($s'<s$) observations under one authoritative sequence.

## Mechanisms, Invariants, or Proof Structure

**Acceptance invariant.** Every acknowledgment names exactly which durable or processing state it proves; no earlier stage is presented as a later business outcome.

**Authority invariant.** Commands target an owner, and events are published by or under the authority that observed the fact. Subscribers own only their reactions and derived state.

**Publication-gap argument.** If database commit and publication are independent, a crash can occur after either first action and before the second. Therefore application ordering alone cannot guarantee both-or-neither visibility. An atomic local record, coordinated transaction, or log-as-authority changes the mechanism.

**Duplicate-delivery argument.** If a consumer commits before acknowledgment and the acknowledgment is lost, redelivery and no-redelivery executions are indistinguishable to the broker. At-least-once recovery therefore requires duplicate-tolerant effects.

**Ordering invariant.** Required ordering names an authority, key, sequence, epoch, and late/gap policy. No wall-clock timestamp or topic name is treated as universal total order.

**Capacity invariant.** Arrival, completion, message size, backlog bytes, oldest age, partitions, concurrency, attempts, retention, replay rate, and downstream work are bounded and observed.

**Failure invariant.** Transient, permanent, poison, expired, unauthorized, and unknown outcomes have distinct policies. Quarantine and dead-letter state remain unresolved until an authorized terminal action.

**Compatibility invariant.** Supported envelope, payload, semantic, policy, and retained-data versions coexist under tested deploy, rollback, and replay paths.

**Security invariant.** Publisher, consumer, administrator, replay operator, principal, purpose, provenance, and tenant remain explicit; channel possession alone grants no business authority.

**Evidence invariant.** Broker acceptance, delivery, acknowledgment, consumer commit, external effect, and user outcome are recorded and reconciled as different observations.

## Alternatives and Trade-Offs

| Choice | Advantages | Costs and risks | Prefer when |
|---|---|---|---|
| Point-to-point queue | one competing-consumer work stream | hidden backlog and command ownership errors | one owner processes each unit |
| Publish-subscribe | independent reactions and extensibility | fan-out, privacy, version, and replay exposure | one fact legitimately serves several consumers |
| Partitioned log | retention, ordered key histories, replay | partition skew and operational state | derived views or event streams need history |
| Broker-routed topic | flexible routing and filtering | routing policy can become hidden domain logic | stable technical routing rules suffice |
| Transactional outbox | closes local state/publication gap | relay, duplicates, cleanup, lag | database state is authority and events follow commit |
| Log as authority | one append history can drive state | event-model, replay, and correction complexity | domain genuinely benefits from event-sourced state |
| Distributed transaction | coordinated supported participants | coupling, blocking, operations, limited reach | strict atomicity and infrastructure justify it |
| Choreography | autonomous reactions | implicit process and difficult global diagnosis | facts trigger genuinely independent behavior |
| Orchestration | explicit process state and recovery policy | central process authority and coupling | multi-step progress needs coordinated decisions |
| Dead-letter isolation | protects throughput from poison work | forgotten required work and sensitive copies | terminal handling and ownership are explicit |
| Synchronous call | immediate current outcome | temporal and failure coupling | caller cannot proceed without the result |
| Batch/file exchange | efficient large-set transfer | latency and reconciliation | periodic complete sets are natural |

## Failure Modes and Misconceptions

1. **“Accepted means completed.”** It proves only the named handoff stage.
2. **“A durable broker makes the workflow durable.”** Producer and consumer crash gaps still matter.
3. **“Every message is an event.”** Many payloads are commands, documents, or notifications.
4. **“Publish-subscribe removes coupling.”** Meaning, schema, volume, retention, and operation still couple participants.
5. **“Exactly once means one business effect.”** Scope and failure assumptions determine the claim.
6. **“Duplicates are exceptional.”** Lost acknowledgments make them a normal recovery case.
7. **“A trace ID is a message or operation ID.”** Identity scopes and retention differ.
8. **“Topics are systems of record.”** Authority depends on governed production and history semantics.
9. **“Timestamps give total order.”** Distributed clocks and concurrent events do not establish it.
10. **“More partitions always improve throughput.”** Hot keys and downstream capacity can dominate.
11. **“A queue solves overload.”** It delays overload unless arrival and recovery are bounded.
12. **“Retries fix bad messages.”** Deterministic poison data consumes capacity repeatedly.
13. **“Dead-letter means handled.”** It is unresolved work in another location.
14. **“Replay is just reading again.”** Consumers may repeat irreversible effects.
15. **“Schema compatibility proves semantic compatibility.”** Units, meaning, authority, and side effects may change.
16. **“Encryption solves message security.”** Authorization, provenance, retention, operators, and metadata remain.

## Worked Examples

### Example 1

**Situation.** Telemetry arrives at 1,200 messages/s, and consumers are unavailable for 20 minutes. Average raw payload is 1.5 KB.

**Reasoning.** With zero completion, backlog becomes $1{,}200\times1{,}200=1{,}440{,}000$ messages. Raw payload is about 2.16 GB using decimal units. Broker envelope, indexes, replication, transaction records, and safety margin increase storage. If restored capacity equals 1,200/s, the queue never drains; recovery requires measured excess capacity or controlled admission.

**Conclusion.** Outage duration and recovery headroom, not nominal throughput alone, determine safe buffering.

### Example 2

**Situation.** Eight consumers each sustain 75 messages/s against arrival of 500/s. Two consumers fail for ten minutes.

**Reasoning.** Normal capacity is $8\times75=600$/s, 100/s or 20% above arrival. With two consumers down, capacity is 450/s and backlog grows 50/s, creating 30,000 messages in 600 seconds. After recovery, 100/s excess drains that backlog in 300 seconds under the simplified constant-rate model. Downstream limits and work skew still need measurement.

**Conclusion.** Capacity plans must cover degraded operation and drain time, not just healthy equilibrium.

### Example 3

**Situation.** An order transaction commits, but the process crashes before publishing `OrderPlaced`.

**Reasoning.** A later retry may not know publication state, and subscribers miss fulfillment if nothing repairs the gap. Store order and outbox entry in one local transaction. A relay publishes the immutable entry. If it crashes after publish before checkpoint, it publishes again; consumers record message identity with their local effect atomically.

**Conclusion.** The outbox closes loss between local commit and publication but deliberately leaves duplicates to idempotent consumers.

### Example 4

**Situation.** A consumer debits loyalty points, commits, then loses its acknowledgment.

**Reasoning.** The broker redelivers. A blind decrement double-debits. The handler uses stable redemption operation ID, member principal, and request fingerprint; in one transaction it either returns the stored outcome or applies the debit once and records it. A reused ID with different points is rejected. Email confirmation uses the same operation outcome but its own idempotent send policy.

**Conclusion.** Duplicate-tolerant processing covers the whole business effect, not merely broker receipt.

### Example 5

**Situation.** Account balance messages use customer region as partition key, but customers can move regions.

**Reasoning.** After a move, one account has messages in two partition histories and concurrent consumers can reorder effects. Partition by stable account ID instead. Include authoritative account version and producer epoch. On a gap, the consumer pauses that key and fetches or reconstructs missing state; it may continue unrelated keys.

**Conclusion.** Ordering requires a stable domain key and a gap policy, not merely an ordered broker primitive.

### Example 6

**Situation.** One malformed message fails deserialization and blocks an ordered partition.

**Reasoning.** Immediate infinite retry prevents all later keys on that lane. After bounded attempts, quarantine the original bytes, provenance, schema ID, code version, and failure without exposing secrets. Whether the partition continues depends on invariant scope: an independent notification may be skipped; an account ledger gap must stop that account until repaired. Authorized redrive preserves identity and limits rate.

**Conclusion.** Poison-message isolation must preserve business ordering and ownership, not just restore throughput.

### Example 7

**Situation.** A team wants to replay six months of `InvoiceIssued` into a new projection, but the existing consumer also emails customers.

**Reasoning.** Separate pure projection from external notification. Replay original message identities under a new run identity into an isolated projection, pin code and transformation versions, rate-limit against source and database capacity, compare totals and sampled records, then switch reads. Disable externally effectful paths; historical emails are not resent.

**Conclusion.** Replay is a governed migration with side-effect classification, validation, and cutover.

### Example 8

**Situation.** A broker topic carries tenant billing events, and a wildcard consumer credential can read every tenant.

**Reasoning.** Transport encryption does not prevent authorized-but-overbroad consumption. Isolate tenant or trust domains where required, restrict subscriptions and administration, authenticate workloads, authorize business use, audit replay, minimize payloads, and protect dead-letter and archive copies. Rotate credentials while old and new consumers coexist.

**Conclusion.** Channel security includes least privilege, provenance, retained data, and operations—not only encryption.

### Example 9

**Situation.** Checkout publishes `PaymentRequested` and immediately shows “Paid.”

**Reasoning.** Publication proves neither authorization nor capture. The order enters `payment_pending` with a stable operation ID. Payment authority later publishes accepted, rejected, or unknown outcome. The client queries order status or receives a notification. Expiry triggers an explicit failure or manual path; timeout never becomes rejection or success.

**Conclusion.** Asynchronous UX must expose pending and terminal outcomes rather than relabeling acceptance as completion.

### Example 10

**Situation.** A hospital publishes medication-order messages during network partition and later reconnects with duplicates and late cancellations.

**Reasoning.** The prescriber authority signs an immutable order identity, patient identity, medication, dose, version, and validity interval. Administration requires a current local safety policy and records its effect idempotently. Cancellation carries a higher authoritative version but cannot undo an already administered dose; that conflict becomes an urgent clinical reconciliation. Per-patient ordering, offline authority, expiry, and human procedures are explicit.

**Conclusion.** Safety-critical messaging must represent irreversible effects and late knowledge honestly; ordering and replay cannot reverse reality.

## Cross-Program Connections

- **API and Service Engineering:** owns message schemas, protocol bindings, idempotency interfaces, compatibility testing, and client contracts in depth.
- **Distributed Systems Engineering:** owns delivery under failure, time, ordering, consensus, replication, and consistency theory.
- **Data Engineering:** owns high-volume streams, processing time and event time, checkpoints, stateful operators, and pipeline recovery.
- **Database Engineering:** owns local transactions, outbox and inbox tables, isolation, logs, and durable deduplication state.
- **Data Architecture Engineering:** owns authoritative data products, lineage, retention, privacy, and consumer contracts.
- **Security Engineering:** owns workload identity, channel authorization, provenance, integrity, secrets, and retained-data controls.
- **Software Delivery and Reliability Engineering:** owns capacity, SLOs, overload, incident response, rollout, reconciliation, and disaster recovery.
- **Platform Engineering:** provides governed brokers, schemas, identity, quotas, observability, replay tooling, and safe defaults without owning domain meaning.

## References

1. Leslie Lamport, “Time, Clocks, and the Ordering of Events in a Distributed System,” *Communications of the ACM* 21(7), 1978. <https://doi.org/10.1145/359545.359563>
2. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions*, Addison-Wesley, 2003. <https://www.enterpriseintegrationpatterns.com/>
3. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
4. OASIS, *Advanced Message Queuing Protocol (AMQP) Version 1.0*, October 2012. <https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-overview-v1.0-os.html>
5. Cloud Native Computing Foundation, *CloudEvents Specification, Version 1.0.2*, February 2022. <https://github.com/cloudevents/spec/tree/v1.0.2>
6. Philip A. Bernstein and Eric Newcomer, *Principles of Transaction Processing*, 2nd ed., Morgan Kaufmann, 2009.
7. Pat Helland, “Life beyond Distributed Transactions: An Apostate's Opinion,” *CIDR*, 2007. <https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf>
8. Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds., *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. <https://sre.google/sre-book/table-of-contents/>

## Exercises

### Exercise 1

Define asynchronous messaging, command, event, document message, channel, delivery attempt, acknowledgment, at-most-once, at-least-once, idempotent consumer, ordering scope, backlog, dead-letter destination, and replay. Explain why synchronously waiting for broker acceptance can still be asynchronous with respect to business completion.

### Exercise 2

A channel receives 900 messages/s. Consumers stop for 12 minutes, and raw messages average 2.5 KB. Compute outage backlog and raw bytes. Ten consumers later sustain 110 messages/s each. Compute healthy excess capacity and simplified drain time, then recompute the direction of backlog change if three consumers fail. State limitations.

### Exercise 3

Design crash-safe publication and consumption for `ShipmentBooked`. Cover producer transaction, outbox relay, duplicates, consumer transaction, external carrier calls, acknowledgment, unknown outcomes, and reconciliation.

### Exercise 4

Compare a point-to-point queue, publish-subscribe topic, partitioned retained log, synchronous call, and batch file for catalog prices, stock reservations, analytics facts, fraud decisions, and nightly partner settlement. Define authority, latency, order, retention, and failure.

### Exercise 5

Design asynchronous messaging for regional emergency shelters during intermittent connectivity. Cover commands and events, offline authority, stable identity, ordering, duplicate and late delivery, expiry, capacity, priority, security, privacy, replay, user-visible outcome, and manual reconciliation. Identify facts that delayed messages cannot reverse.

## Answers to the Exercises

### Answer 1

**Asynchronous messaging** lets the sender proceed after an agreed handoff without waiting for final receiver work. A **command** asks an owner to act; an **event** states an observed fact; a **document message** transfers a representation. A **channel** is the logical path. A **delivery attempt** is one try; an **acknowledgment** proves only its named stage. **At-most-once** may lose but avoids broker redelivery; **at-least-once** favors redelivery and permits duplicates. An **idempotent consumer** preserves the intended effect for repeats under a stable identity. **Ordering scope** names the key or partition within which order is promised. **Backlog** is accepted incomplete work. A **dead-letter destination** isolates unresolved failures. **Replay** deliberately reprocesses retained history under policy. Waiting for durable broker acceptance is synchronous for the handoff, but the business operation remains asynchronous if sender completion does not wait for the receiver's outcome.

### Answer 2

Twelve minutes is 720 seconds. Backlog is $900\times720=648{,}000$ messages. Raw payload is $648{,}000\times2.5$ KB $=1{,}620{,}000$ KB, about 1.62 GB in decimal units. Restored capacity is $10\times110=1{,}100$/s, giving 200/s excess. Simplified drain time is $648{,}000/200=3{,}240$ seconds, or 54 minutes, while new messages continue arriving. With three consumers down, capacity is $7\times110=770$/s, a deficit of 130/s, so backlog grows. The model omits envelope and replication bytes, skew, variable work, downstream limits, retries, pauses, expiry, and changing rates; measured recovery must validate it.

### Answer 3

Shipment authority commits booking intent and an outbox record in one local transaction under stable booking operation ID and fingerprint. A relay publishes the immutable record and checkpoints progress; publish-before-checkpoint can duplicate. The carrier call is a separate effect: its consumer records an inbox claim, invokes the carrier using a stable carrier idempotency key, and records accepted, rejected, or unknown status. It must not acknowledge after an uncertain timeout as though failure were terminal. If the carrier supports outcome query, reconciliation uses the same identity; otherwise manual resolution remains explicit. Consumer state change and inbox completion commit together where possible, then acknowledgment occurs. A later `ShipmentBooked` fact comes only from shipment authority once evidence exists. Monitoring reconciles outbox, broker, inbox, carrier, and business outcomes.

### Answer 4

Catalog prices suit a retained, versioned topic or document stream when consumers accept bounded propagation; pricing remains authority and messages carry product/version order. Stock reservation and fraud decisions need a current authoritative result before checkout acts, so a bounded synchronous call or pending command with explicit outcome is preferable; message acceptance alone is insufficient. Analytics facts suit publish-subscribe or a partitioned log because independent consumers need retention and replay, with source identity and event-time policy. Nightly partner settlement naturally suits a manifest-controlled batch file with totals, checksums, sequence, acknowledgment, and reconciliation. A point-to-point queue fits one owning worker group for each command. Choice follows required latency, authority, per-key order, history, consumer count, and failure semantics rather than one transport for every case.

### Answer 5

Regional coordination owns shelter activation and publishes versioned `ShelterActivated` or `ShelterClosed` facts; a delegated local commander may issue offline commands only within recorded jurisdiction and time. Each command has stable operation, shelter, principal, device, and semantic fingerprint identities plus validity and expiry. Per-shelter source versions detect duplicate, gap, and late delivery. A late closure cannot erase that people were already admitted, supplies consumed, or treatment given; those are new immutable facts requiring reconciliation. Devices store an encrypted bounded local outbox, prioritize life-safety work, shed informational updates first, and expose pending, accepted, rejected, expired, and unknown states. Reconnection rate is capped to protect regional capacity. Workload and human authority are authenticated; least privilege, integrity, tenant/jurisdiction isolation, data minimization, retention, and lost-device revocation apply. Replay rebuilds projections with external alerts disabled. Operators reconcile conflicts against signed local logs and current regional authority, while users see source and freshness. Full credit requires honest irreversible history, offline authority limits, and no inference of safety or capacity from missing messages.
