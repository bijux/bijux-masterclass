---
module_id: API-061
program: API & Service Engineering
level: 2
module_number: 61
title: Commands, Events, and Messages
status: complete
last_verified: 2026-09-02
---

# Commands, Events, and Messages

## One-Page Review

### Governing question

How should a message-driven API distinguish commands, events, requests, replies, documents, and notifications so ownership, authority, acknowledgement, effects, ordering, retry, evolution, security, and failure recovery remain explicit across asynchronous boundaries?

### Essential definitions

- A **message** is a transportable envelope plus application content exchanged through a channel; it is the carrier, not the business meaning.
- A **command** requests that one logical authority attempt an action. It is imperative, directed, rejectable, and identified independently of delivery attempts.
- An **event** records an immutable fact that an authoritative producer says occurred. It is past tense and may have zero, one, or many consumers.
- A **request** asks for a reply under a correlation and lifetime contract; it may be a query or command.
- A **reply/outcome** reports acceptance, rejection, progress, result, or failure for a request/command. Broker settlement alone is not this outcome.
- A **document message** transfers state or a dataset for replacement, merge, synchronization, or processing under an explicit version/snapshot contract.
- A **notification** is a prompt that something may deserve attention; it may carry only a hint and require an authoritative read.
- **causation ID** identifies the message/decision that caused another message; **correlation ID** groups a wider conversation; **trace context** supports diagnostic propagation and is not business identity.
- A **delivery attempt** is one transport action for a stable logical message. Retry changes attempt metadata, not command/event identity.

### Central model, mechanism, or theorem

For command $c=(id,target,action,expectedVersion,payload)$ against authoritative state $x_v$, one logical handler decides:

$$
handle(c,x_v)\rightarrow(outcome,x_{v'},E),
$$

where $E$ is zero or more facts committed with the new state. If command ID $id$ was already decided, the handler returns the recorded outcome without repeating effects. Events can build a projection by a deterministic fold:

$$
p_n=fold(apply,p_0,[e_1,\ldots,e_n]).
$$

This supports replay only when event meaning/order, compatibility, side-effect isolation, and retained history are sufficient. A transport message can carry a command or event, but changing its noun does not change these semantic obligations.

### Critical invariants

Every message declares kind and schema/version; stable message/command/event ID; producer/source; subject/target; tenant/audience and data classification; produced time and, for facts, occurred time; content type; correlation/causation; partition/order key where relevant; and bounded payload. Commands name an authorized action and one logical owner, have deadline/expiry, idempotency/concurrency, and queryable outcomes. Events are immutable past-tense facts emitted only after the authoritative commit, with producer-owned meaning and no consumer-specific imperative hidden inside. Replies state which boundary they prove. Documents state snapshot/version/merge behavior. Notifications never masquerade as complete truth.

Publication is atomic with source state through an outbox/log or equivalent evidence. Consumers use idempotent effects/inboxes where redelivery is possible. Ordering is scoped, not global by assumption. Retry, backoff, poison handling, dead-letter/redrive, retention/replay, cancellation, backpressure, authorization, privacy, schema compatibility, observability, and reconciliation have explicit owners. Message content is minimized; credentials and unrestricted personal data do not leak into durable payloads or logs.

### Common failures

Naming commands in past tense; naming events as instructions; broadcasting a command with multiple competing authorities; treating `MessageReceived` as a domain fact; publishing before database commit; dual-writing database and broker; generating a new ID per retry; using correlation ID for deduplication; treating broker acknowledgement as business completion; infinite request/reply waits; late commands executing after caller intent expired; replying on an unbounded/user-controlled address; putting routing secrets or mutable state in headers; assuming partitions give global or causal order; replaying events through external side effects; using events as current-state dumps; breaking consumers by changing meaning while preserving type/version; routing every unknown message to a dead-letter graveyard; tracing IDs as authorization; and placing sensitive data into indefinitely retained logs.

### Compact example

`ReserveInventory` is a command directed to the inventory authority with command ID, item, quantity, expected version, actor scope, and deadline. One transaction records either rejection or reservation plus outbox event `InventoryReserved`. A lost outcome causes the caller to query/retry the same command ID; effects are not repeated. Billing and fulfillment independently consume the immutable event using inboxes. A UI notification contains event/resource ID and fetches the authorized current representation rather than trusting a stale payload. **Conclusion:** command, outcome, event, delivery, and notification identities and responsibilities remain separate even when one broker transports them all.

### Connections

[Idempotency Keys](037-idempotency-keys.md), [Choosing an Interface Style from Interaction Semantics](060-choosing-an-interface-style-from-interaction-semantics.md), and [Webhooks, Server-Sent Events, and WebSockets](059-webhooks-server-sent-events-and-websockets.md) establish retry and transport boundaries. The next modules turn these semantics into event schemas, AsyncAPI contracts, delivery guarantees, and ordering/replay designs.

## Governing Question

What does each message assert or request, who has authority to send and act on it, what acknowledgement/outcome is observable, and how do stable identity, atomicity, ordering, retry, replay, evolution, and recovery preserve that meaning under partial failure?

## Why This Matters

Messaging infrastructure moves bytes reliably according to a configured contract. It cannot decide whether the bytes are a request, an instruction, an observed fact, a state snapshot, a progress update, or a mere hint. That semantic distinction controls routing, authorization, idempotency, retention, replay, fan-out, monitoring, and incident recovery.

A command carries intent toward an authority. An event carries a producer's claim about the past. Treating them as interchangeable creates distributed ownership. If `ApproveLoan` is broadcast to many consumers, which one may decide? If `LoanApproved` is sent before the authoritative commit, what fact does it represent? If a consumer fails, should the producer retract the fact? The message broker cannot answer.

Asynchrony introduces time between intent and action. Permissions, state versions, deadlines, policy, and business relevance can change while a command waits. Events can arrive duplicated, delayed, or reordered. Consumers can be rebuilt from old data only if schemas and meaning remain compatible and external effects are isolated. Durable message systems amplify both correct and incorrect contracts over long retention and many consumers.

Clear taxonomy is therefore a safety mechanism. It lets teams state authority and observable boundaries, design targeted schemas and tests, and diagnose whether a failure belongs to transport, handling, workflow, projection, or domain policy.

## Prerequisites and Retrieval

Retrieve [Idempotency Keys](037-idempotency-keys.md), [API Threat Modeling](041-api-threat-modeling.md), [Deadlines, Cancellation, and Metadata](054-deadlines-cancellation-and-metadata.md), [Webhooks, Server-Sent Events, and WebSockets](059-webhooks-server-sent-events-and-websockets.md), and [Choosing an Interface Style from Interaction Semantics](060-choosing-an-interface-style-from-interaction-semantics.md). Be able to distinguish transport receipt, durable broker acceptance, consumer delivery, application acceptance, domain commit, workflow completion, retry, replay, and reconciliation.

Retrieve the exact message protocol/broker, AsyncAPI, event-envelope, trace-context, and schema specifications used by the implementation. Description formats and envelope standards document surfaces; they do not choose business semantics or guarantees.

## Learning Objectives

After completing this module, you can:

1. distinguish commands, events, requests/replies, documents, and notifications by meaning rather than transport;
2. design stable message envelopes without conflating business, diagnostic, and delivery identities;
3. assign authority for producing, routing, handling, acknowledging, and recovering each message kind;
4. define command idempotency, concurrency, expiry, cancellation, and outcome lookup;
5. publish facts atomically with authoritative state and consume them idempotently;
6. scope ordering and replay requirements by subject/partition and side-effect safety;
7. design request/reply over messaging without hiding asynchronous failure;
8. authorize and minimize durable messages across tenant and trust boundaries;
9. evolve schemas and semantics without silently reinterpreting retained history; and
10. verify message APIs with contract, model, fault, adversarial, replay, and operational tests.

## Core Exposition

### Separate carrier from meaning

AsyncAPI 3.0.0 defines a message as information exchanged through a channel and notes that messages can support event, command, request, or response patterns. This is the crucial separation: queue/topic/channel/protocol is carriage; application kind supplies meaning.

The same JSON object sent through Kafka, AMQP, HTTP webhook, or WebSocket does not acquire event semantics from the medium. Conversely, one broker can legitimately carry commands, events, replies, and documents if destinations, permissions, retention, and operational policies fit each kind. Put an explicit kind/type in the contract and use names/descriptions that reveal tense and authority.

Do not classify solely from whether a reply exists. Commands may be fire-and-observe-later or have outcomes. Events may trigger derived events. Requests can ask queries or commands. A document may be sent in response to a request. Classification asks what the sender means and what the receiver is authorized to do.

### Model commands as directed intent

A command requests an effect from one logical authority: `ReserveInventory`, `CloseAccount`, `GenerateStatement`. It is imperative and can be rejected because policy, validation, preconditions, capacity, deadline, or current state do not permit the action. Multiple physical workers may compete for scalability, but they represent one logical handler/decision boundary.

Include command ID, type/version, target aggregate/resource/tenant, requested action data, actor/delegation context or a safe reference, expected state version/precondition, issued time, deadline/expiry, correlation/causation, and reply/outcome contract. A queued command needs an expiry because eventual execution may violate user intent. Reauthorize at handling time; a credential snapshot or trace header is not permanent permission.

Idempotency attaches to the command identity and semantic scope. Atomically claim/record command ID with its canonical fingerprint and outcome/effect. Same ID plus different intent is a conflict, not a second command. Duplicate delivery returns/re-emits the recorded decision. Retention must cover retry/replay/reconciliation horizons; after expiry, behavior is explicit.

Optimistic concurrency belongs in the command when action depends on observed state. `expectedVersion=17` lets the authority reject a stale request instead of applying it to version 21. The caller may refetch/replan, not blindly change the version on retry. Commands can also carry business effective time, but worker clock or queue position must not silently redefine it.

Cancellation is another command or governed state transition, not message deletion magic. If the original has already committed, removing a queued copy does not undo it. Define cancel-before-accept, cancel-after-accept, compensating action, and terminal outcome semantics.

### Model events as immutable facts

An event states a fact under producer authority: `InventoryReserved`, `AccountClosed`, `StatementGenerated`. Use past tense and define the source-of-truth transition that makes it true. It may be interesting to zero, one, or many consumers. A producer owns the fact's meaning; consumers own their reactions.

Include stable event ID, type/spec version, source, subject, occurred time, produced/published time, tenant/audience/classification, schema/content type, correlation/causation, and partition/order key. CloudEvents 1.0.2 defines interoperable context attributes such as id, source, specversion, type, subject, time, data schema/content type, and data. It provides a useful envelope, not domain truth, authorization, ordering, or delivery guarantees.

Events are immutable. Correction is another fact, such as `ShippingAddressCorrected`, linked by subject/causation; do not edit retained history invisibly. Event payload may be a thin fact with identifiers or a richer state-at-time representation. Choose from consumer autonomy, privacy, schema coupling, fetch availability, and replay needs. Never claim that a snapshot-shaped event is current forever.

Events should not instruct one consumer: `SendEmailEvent` is usually a command disguised as a fact. A domain fact `OrderConfirmed` may lead a notification policy to decide a `SendConfirmationEmail` command. This separation lets new consumers react without pretending the producer owns their actions.

### Distinguish notifications and documents

A notification says “something may need attention” and can be lossy/coalesced if the contract permits. It often carries subject, change hint, version, and fetch link/reference. Consumers retrieve authorized current state. This reduces sensitive durable payload and avoids applying stale intermediate state, but increases read dependency and may miss transitions important to audit.

A document message transfers a stateful artifact: customer snapshot, catalog segment, settlement file, model, or batch. Define snapshot identity/version, coverage interval, authority, complete versus delta, replace/merge/upsert/delete semantics, checksum/count, schema, compression/encryption, ordering between snapshots/deltas, atomic application, and restart. A document is not automatically an event merely because it arrives asynchronously.

Use facts when transitions/history matter, notifications when prompt-to-read is enough, and documents when coherent state transfer is the interaction. Mixing them forces consumers to infer whether payload should be applied, fetched, merged, or audited.

### Design request/reply explicitly

Messaging can carry request/reply, but the exchange remains distributed and asynchronous. A request needs request ID, correlation ID, reply channel/address governed by policy, deadline/TTL, accepted response types, and authorization. A reply needs its own message ID, correlation to request, responder identity, outcome type/version, and terminal/progress semantics.

Do not let arbitrary clients inject reply destinations that escape tenancy or create SSRF/routing abuse. Prefer provisioned reply channels, scoped temporary destinations, or correlation on a controlled shared channel. Bound outstanding requests, reply size/count, and cleanup. Late replies after deadline are discarded or recorded according to policy, never attached to a reused correlation.

One reply may mean accepted, while completion arrives later. Define states such as rejected, durably accepted, in progress, completed, failed, cancelled, expired, or unknown. Do not map broker publish success to completed business action. When reply is lost, stable request/command ID plus outcome query/replay resolves ambiguity.

For low-latency request/response where participants must be online, ordinary HTTP/RPC may be simpler. Messaging request/reply is justified when broker routing, buffering, workload isolation, or uniform message infrastructure materially helps; it should not disguise a synchronous dependency behind a queue.

### Separate four identities

At minimum distinguish:

1. **Logical message ID** identifies one immutable message/fact.
2. **Command/request ID** identifies one requested decision and deduplication scope; it may equal the command message ID only by explicit convention.
3. **Correlation/causation IDs** group a conversation and link causal steps. Many messages can share correlation; therefore it is unsafe as a deduplication key.
4. **Trace/span IDs** are diagnostic context following W3C Trace Context or a chosen standard. Sampling, trust-boundary regeneration, and multiple traces mean they are not domain identity, authorization, or audit proof.

Delivery attempt ID/number is a fifth operational identity. A retry keeps logical ID and changes attempt metadata. Broker offset/delivery tag identifies a position/settlement action, not necessarily business identity. Resource/aggregate ID identifies the subject, not the particular command/event.

Validate ID format, length, tenant/scope, generation authority, collision policy, and retention. Opaque uniqueness does not grant permission. Do not place credentials or sensitive business meaning in routing IDs.

### Make acknowledgement boundaries observable

An acknowledgement can mean bytes accepted by a client library, broker durably accepted under configured replication, message delivered to a consumer process, consumer checkpoint advanced, application inbox committed, domain effect committed, or workflow completed. Name the boundary in contracts and telemetry.

AMQP 1.0, for example, defines delivery state and settlement mechanics at the messaging layer. Those mechanics are valuable but cannot define whether `ReserveInventory` succeeded in the domain. AsyncAPI can describe reply messages and operations, but implementation and business state still determine outcome.

Consumers should acknowledge/advance offsets only at their documented safe boundary. If ack precedes durable application acceptance, a crash can lose work. If ack follows slow external effects, redelivery may repeat them unless an inbox/outbox/idempotency protocol exists. Some consumers can acknowledge after durable inbox and process later; others atomically update local state plus checkpoint. State which.

### Commit facts atomically

Publishing an event before state commit creates a false fact if the transaction rolls back. Committing state then separately publishing creates a missing fact if the process dies. Use a transactional outbox, database log/change capture with defined semantics, event store as source of truth, or broker/database atomic mechanism that has evidence for the boundary.

In an outbox pattern, the command transaction writes domain state, command outcome, and immutable outbox record atomically. A publisher leases and emits outbox records, then marks attempts/success; duplicates are allowed because crash can occur after broker acceptance before mark. Event ID remains stable. Consumers deduplicate or make their state transition idempotent.

Do not claim exactly-once business effects from a broker feature alone. Broker transactions/idempotent producers can narrow duplication within their scope; external databases, emails, payments, and APIs remain separate boundaries. Design end-to-end identities, atomic local transitions, and reconciliation.

### Scope order and causality

Total global order is expensive and rarely necessary. State the domain key whose transitions require order: order ID, account ID, device ID, tenant, or workflow. Route that key consistently to a partition/serial authority where supported. Sequence/version within the subject detects duplicate, stale, or gap.

Transport order is conditional on producer/session/partition, retries, failover, and consumer concurrency. Two producers can observe/emit causal steps differently. Cross-partition order is not implied. If event B semantically requires A, encode version/causation/precondition and define buffer, fetch, retry, or reconciliation when A is absent.

Commutative/idempotent operations can tolerate reorder; state replacement needs version comparison; noncommutative transitions require serialization or explicit conflict rules. Do not block an entire partition indefinitely for one missing/poison record without a governed strategy.

### Design replay as a separate operating mode

Replay re-presents retained messages to rebuild, repair, audit, or create a consumer. It is not ordinary retry. Define source range, point-in-time schema/meaning, target consumer/version, ordering, rate/backpressure, isolation from live traffic, checkpoint, side-effect suppression, validation, and cutover.

A projection fold should be deterministic for the governed event stream. External emails, payments, webhooks, and tickets are not replay-safe just because local state updates are. Separate projection logic from effect dispatch; use recorded effect IDs/outcomes or an explicit no-effects replay mode. Test historic schemas and upcasters without rewriting the original event's meaning.

Retention and erasure complicate replay. Data minimization, tokenization, encryption-key lifecycle, legal holds, subject erasure, and derived stores must be designed together. “We can rebuild from the log” is false if required history expires, schemas/code vanish, events were corrections without bases, or secrets are destroyed by policy.

### Govern schemas and meaning

Schema compatibility is necessary but insufficient. Adding an optional field can still change authorization, defaulting, routing, cost, or consumer interpretation. Define message kind, type naming, semantic owner, schema owner, compatibility mode, defaults, enum evolution, numeric units, timestamps/time zones, identifiers, null/absence, payload bounds, privacy class, retention, examples, and deprecation.

Never change the meaning of an existing type/version while old messages remain replayable. Use a new event type/version for incompatible semantics and supply migration/upcasting rules where legitimate. Producers should publish facts they own, not consumer-specific denormalized jargon. Consumers should use anti-corruption mapping into their domain rather than importing transport schemas everywhere.

AsyncAPI can describe applications, servers, channels, operations, messages, replies, correlation IDs, schemas, security, and protocol bindings. Keep it synchronized with actual broker policy, schemas, and deployment. The next modules develop these contract/evolution mechanisms in detail.

### Secure and operate the message path

Authorize at multiple planes: connection to server, send/receive operation on channel, message type, tenant/subject, and domain action at handling time. Least privilege separates producers, consumers, replay operators, schema publishers, and redrive tools. Do not trust tenant, actor, trace, or source fields merely because a broker delivered them; bind trusted identity at ingress and validate cross-service claims.

Minimize payloads and headers. Durable logs, replicas, dead-letter stores, traces, and development copies widen exposure. Encrypt transport and storage; govern keys, field protection/tokenization, retention, erasure, backups, and operator access. Validate type/content/schema/size/decompression/structure before expensive work. Protect against floods, hot keys, high-cardinality routes, reply amplification, poison loops, and tenant starvation.

Observe logical message/command/event ID, safe type/version, source/destination, tenant-safe subject, partition/offset, attempt, age, queue/lag, processing/commit/ack latency, outcome class, retry/dead-letter/redrive, schema rejection, and trace correlation—without recording credentials or full sensitive payload. Alert on age/lag, stuck partitions, repeated poison, outcome unknowns, outbox backlog, dedup conflicts, reply timeout, and reconciliation drift.

Dead-letter is quarantine, not completion. Classify transient, permanent-message, permanent-policy, dependency, and operator-hold failures. Record bounded diagnostics and original identity safely. Redrive revalidates authorization/schema/deadline/idempotency, rate limits re-entry, and is auditable. A malformed or expired command may require terminal rejection rather than blind replay.

## Definitions and Notation

Let command $c=(id_c,type,target,actor,precondition,deadline,payload)$ and authoritative state $x_v$. Let event $e=(id_e,type,source,subject,occurred,version,data)$, outcome $o=(id_o,command,status,result)$, and general envelope $m=(id_m,kind,schema,source,destination,tenant,correlation,causation,trace,content)$.

Let delivery attempts $a_1,\ldots,a_k$ carry the same logical $m$; attempt metadata is not part of immutable content unless the contract explicitly signs/binds it separately. Let consumer inbox $I$ retain processed message IDs/fingerprints and outbox $O$ retain facts awaiting publication. Let subject sequence $seq_s(e)$ and projection $p_n$ model scoped order/replay.

Command safety requires one decision per $(scope,id_c,fingerprint)$; event truth requires authoritative commit before publish eligibility. Delivery may be at-most-once, at-least-once, or broker-specific within a declared boundary, while business effect semantics derive from handler atomicity and idempotency.

## Mechanisms, Invariants, or Proof Structure

1. Classify the message by meaning: command, fact, query/request, reply/outcome, document, or notification.
2. Name sender authority, logical target/audience, source of truth, handler owner, and trust boundary.
3. Define stable identities separately for logical message, command/request, event, subject, correlation/causation, trace, and delivery attempt.
4. Specify acknowledgement layers and queryable terminal/uncertain outcomes.
5. Make command claim/outcome/effect atomic; make event publication eligible atomically with source state.
6. Define duplicate, loss, retry, expiry, cancellation, poison, dead-letter/redrive, and reconciliation behavior.
7. Scope order by domain key; add sequence/version/gap rules where needed.
8. Govern schemas and semantics over retained history, including privacy/erasure.
9. Enforce connection/channel/message/domain authorization plus payload/rate/queue/replay bounds.
10. Verify normal, fault, adversarial, replay, recovery, and operational paths.

Proof sketch for duplicate safety: if claiming unseen command ID, writing its outcome/effects, and recording the ID are one atomic transition, at most one transition can own that ID under the store's uniqueness/serialization guarantee. Later deliveries observe the record and return its outcome. This does not guarantee external effects unless they share the atomic boundary or have their own stable effect IDs/idempotency.

Proof sketch for outbox completeness: if domain change and outbox insertion commit atomically, no committed change lacks its corresponding outbox record and no rolled-back change exposes a committed record. Publisher crash can duplicate emission but stable event ID plus consumer idempotency contains effects. The proof depends on transaction boundary and durable publisher recovery.

## Alternatives and Trade-Offs

**Command versus event.** Command preserves a single decision authority and explicit rejection/outcome; event enables independent reactions to a fact. A workflow commonly uses command then event rather than choosing one label for both.

**Thin event versus event-carried state.** Thin facts minimize duplication/privacy and encourage authorized reads but couple consumers to source availability/current state. Rich events support autonomy/replay but increase schema, retention, staleness, and disclosure cost.

**Notification versus full event.** Notification can be coalesced and prompts a current read; full event preserves transition history. Choose from audit/rebuild need, latency, source availability, and sensitivity.

**Queue versus log/topic.** Competing-consumer queues suit one logical handling group; logs/topics suit fan-out, retention, replay, and independent offsets. Products blend these concepts differently, so specify behavior instead of relying on nouns.

**Choreography versus orchestration.** Choreography lets services react independently but can obscure end-to-end state and create accidental cycles. Orchestration centralizes workflow decisions/outcomes but introduces an owner and potential bottleneck. Domain facts can coexist with explicit orchestration commands.

**Request/reply messaging versus HTTP/RPC.** Brokered reply can buffer/isolate and reuse messaging policy, but outstanding state, late replies, routing, cleanup, and hidden synchronous coupling add cost. Use the simplest boundary meeting availability/timing semantics.

**Event sourcing versus state plus integration events.** Event sourcing makes event history authoritative and supports temporal reconstruction under strict modeling; it imposes aggregate/event evolution, replay, snapshot, privacy, and tooling obligations. An outbox from ordinary state is often sufficient for integration facts.

## Failure Modes and Misconceptions

1. “Everything on a topic is an event.” Transport location does not determine meaning.
2. A command is broadcast to multiple autonomous decision-makers, creating conflicting authority.
3. An event is phrased as `DoThing`, hiding a consumer-specific instruction.
4. A notification/state snapshot is treated as complete transition history.
5. Producer emits before commit or dual-writes state and broker without recovery.
6. Retry creates a fresh logical ID, defeating deduplication.
7. Correlation/trace/offset is reused as business identity or authorization.
8. Broker/client acknowledgement is reported as domain completion.
9. Queued commands omit deadline, current authorization, precondition, and cancellation outcome.
10. Global order is inferred from one partitioned transport or wall-clock timestamp.
11. Replay invokes emails/payments/webhooks again or overwhelms live consumers.
12. Schema-compatible changes silently alter units, defaults, privacy, or semantic meaning.
13. Consumer-specific payloads leak into producer-owned domain facts.
14. Dead-letter becomes an unowned graveyard or redrive bypasses current validation/policy.
15. Durable payloads contain credentials, unrestricted personal data, or high-risk fields without lifecycle controls.

## Worked Examples

### Example 1

`ApproveExpense` is a command to the expense authority, not an event. It includes command ID, expense ID, approver identity/scope, expected version, issued time, deadline, and decision note. The handler reauthorizes and records accepted/rejected outcome atomically. Only a successful transition emits `ExpenseApproved`.

### Example 2

An order transaction writes state and `OrderConfirmed` outbox record together. Publisher sends the same event ID, crashes before marking success, and sends again. Fulfillment inbox sees the duplicate and does not allocate twice. Broker redelivery is visible, while the domain effect remains idempotent.

### Example 3

A UI badge only needs current unread count. A coalescible `UnreadCountChanged` notification contains account/version and prompts conditional authorized GET. It is not used to reconstruct every read/unread transition; an audit requirement would need durable facts instead.

### Example 4

A nightly customer master snapshot carries snapshot ID, `asOf`, schema, coverage, row count, checksum, complete-replace semantics, encryption metadata, and object reference. Receiver stages, verifies, atomically swaps, and records checkpoint. Calling it `CustomerUpdated` would hide its document semantics.

### Example 5

`GenerateReport` travels through a broker with controlled reply channel. First reply is `ReportAccepted`; later `ReportCompleted` references the command and object. A lost completion reply is recovered through `GetReportCommandOutcome`. Client publish acknowledgement never means report completion.

### Example 6

Two account events share partition key account ID and monotonic version 18/19. A consumer receives 19 after 17, records a gap, pauses that account, and retrieves/replays 18 or current snapshot per contract. It does not block unrelated accounts or sort globally by timestamps.

### Example 7

Projection rebuild reads retained `InventoryAdjusted` events into a fresh store with external notifications disabled. It checks historic schema adapters and compares totals/versions to authoritative snapshots before cutover. Replaying live notification handlers would resend emails and is forbidden.

### Example 8

An email policy consumes `OrderConfirmed` and decides `SendOrderConfirmation` command to one notification authority. `OrderConfirmed` remains consumer-neutral; the command has template/locale, recipient reference, policy version, expiry, and idempotent effect ID. Adding SMS later requires a new policy reaction, not changing the fact.

### Example 9

A tenant attempts to send a valid-schema command to another tenant's target and supplies a forged `traceparent` plus reply address. Broker ACL blocks unauthorized channel use; handler binds trusted connection identity, rejects cross-tenant target, validates reply routing, and treats trace context only as diagnostics. Schema validity never grants authority.

### Example 10

A poison event fails because an enum meaning was changed without a new version. Blind retries exhaust a partition. Operations quarantine by stable ID, preserve bounded error evidence, deploy a reviewed upcaster to the consumer, test it on retained samples, and rate-limited redrive while reconciling projection versions. The original event is not edited.

## Cross-Program Connections

[Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) supplies command, event, mediator, adapter, and workflow patterns. [Data Engineering](../../19-data-engineering/ROADMAP.md) consumes event logs, schemas, lineage, replay, and batch documents. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, order, clocks, logs, transactions, and delivery reasoning.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies producer/consumer trust, least privilege, data protection, replay defense, and audit. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies interface ownership and verification. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies brokers, schemas, paved roads, quotas, observability, redrive, and disaster recovery.

## References

1. AsyncAPI Initiative. “AsyncAPI Specification 3.0.0.” <https://www.asyncapi.com/docs/reference/specification/v3.0.0>
2. Cloud Native Computing Foundation. “CloudEvents Specification 1.0.2.” <https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md>
3. OASIS. “Advanced Message Queuing Protocol (AMQP) Version 1.0.” 29 October 2012. <https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-complete-v1.0-os.html>
4. W3C. “Trace Context, W3C Recommendation.” 23 November 2021. <https://www.w3.org/TR/trace-context/>
5. Apache Software Foundation. “Apache Kafka Documentation: Design.” Retrieved 2026-09-02. <https://kafka.apache.org/documentation/#design>
6. IETF. “RFC 9110: HTTP Semantics.” June 2022. <https://www.rfc-editor.org/rfc/rfc9110.html>
7. gRPC Authors. “Core concepts, architecture and lifecycle.” Retrieved 2026-09-02. <https://grpc.io/docs/what-is-grpc/core-concepts/>

## Exercises

### Exercise 1

Classify `RecalculateInvoice`, `InvoiceRecalculated`, `InvoiceChanged`, `InvoiceSnapshot`, and `InvoiceNeedsAttention` as command, event, ambiguous event/notification, document, or notification. Rewrite ambiguous names and state authority, expected consumer behavior, and acknowledgement for each.

### Exercise 2

Design the envelope and state machine for an expiring `TransferFunds` command delivered at least once. Include identities, fingerprint, actor/tenant authorization, precondition, deadline, duplicate conflict, atomic outcome/effects, lost reply, cancellation, and emitted facts.

### Exercise 3

An event stream for one device contains versions 40, 41, 42. A consumer checkpoint is 40; it receives 42 twice and then 41. Describe correct behavior for (a) replace-by-version device state and (b) noncommutative transition events. Explain why wall-clock sorting and broker acknowledgement are insufficient.

### Exercise 4

Design a safe replay of three years of order events into a new analytics projection while live traffic continues. Include schemas/meaning, range/order, side effects, privacy, backpressure, checkpoint/cutover, validation, failure recovery, and operator evidence.

### Exercise 5

Design commands, events, messages, documents, and notifications for a multi-tenant emergency-response workflow: dispatch a unit, accept/reject the command, track unit/incident state, notify browser operators and partner agencies, publish analytics facts, and export an audit package. Include atomicity, identity, authorization, ordering, replay, schema evolution, redrive, observability, and reconciliation.

## Answers to the Exercises

### Answer 1

`RecalculateInvoice` is an imperative command directed to the billing authority. It can be rejected/expired, needs command ID/precondition/actor policy/idempotency, and an application outcome distinct from broker ack. `InvoiceRecalculated` is a past-tense event emitted after authoritative commit; consumers acknowledge their own durable processing boundary, not the truth of the producer's fact.

`InvoiceChanged` is ambiguous: if it represents a committed transition, name the owned fact precisely (`InvoiceAmountCorrected`, `InvoiceTaxRecomputed`) with occurred time/version; if it merely prompts refresh, call it `InvoiceRefreshAvailable` and document coalescing/fetch. `InvoiceSnapshot` is a document with snapshot/version/as-of/coverage/checksum and replace/merge semantics. `InvoiceNeedsAttention` is a notification only if it prompts an authorized read/human workflow and can be coalesced; if “attention required” is an authoritative domain transition, rename it to the exact fact such as `InvoiceReviewRequired` and define the policy transition.

Authority follows kind: billing handler decides command/outcome and owns facts/snapshot; notification policy owns delivery prompts. Transport/broker ack proves only its configured boundary. Domain command outcome proves rejected/accepted/completed; consumer checkpoint proves that consumer's durable application boundary; snapshot ack proves validated/committed import as documented.

### Answer 2

Envelope includes immutable logical message/command ID, type/schema version, source, target account/authority, tenant, actor/delegation reference, transfer ID, from/to account IDs, amount/currency in exact units, expected source-account version, issued time, absolute deadline, correlation/causation, content type, and reply/outcome route governed by policy. Store a canonical semantic fingerprint over target/action inputs and scope; delivery attempt/offset/trace are separate.

On receive, authenticate trusted producer context, authorize tenant/actor/action/accounts, validate schema/size/amount/currency, and check deadline before work. Atomically claim `(tenant,command_id)` with fingerprint. Same ID/different fingerprint is conflict. Existing terminal outcome is returned; existing in-progress state is queried/waited according to protocol. For a new command, lock/serialize accounts or validate expected version, enforce funds/limits/policy, then atomically record debit/credit ledger entries, command outcome, and outbox facts `FundsTransferCompleted` or durable rejection as policy requires. Stable event/effect IDs derive from recorded records, not delivery attempts.

If reply is lost, caller retries same ID or queries outcome; no second transfer occurs. Expired-before-claim becomes terminal expired/rejected. Cancellation is a separate authorized command: before acceptance it may mark cancelled; after commit it cannot erase transfer and may initiate governed reversal/compensation with new identity. Emit immutable facts only after/with authoritative commit eligibility. Reconcile command/outcome, ledger, outbox, published events, and downstream inboxes; protect sensitive account data and audit every redrive.

### Answer 3

For replace-by-version state, checkpoint 40 plus first 42 reveals gap 41. If contract permits newer complete state to supersede older versions, consumer can validate 42, apply only if version exceeds stored, checkpoint 42, ignore duplicate 42 and late 41, while recording gap/reconciliation evidence. If every transition matters for audit, it must fetch/replay 41 before accepting 42 even if state replacement is possible.

For noncommutative transitions, do not apply 42 before 41. Buffer 42 within bounds, retrieve/retry missing 41, or pause/quarantine that device and reconcile from authoritative history/snapshot according to contract. Once 41 applies, apply one copy of 42 and advance checkpoint atomically with local state/inbox. If gap cannot be recovered, use documented reset/manual recovery rather than guessing.

Wall-clock timestamps can collide, skew, or reflect production rather than authoritative subject order. Broker order may only hold per producer/partition and can be disturbed by retry/failover/concurrent consumers. Broker ack says nothing about missing semantic predecessor or local atomic state. Subject version/sequence plus explicit gap and idempotency rules carries the required meaning.

### Answer 4

Pin source topic/log, partitions, start/end offsets or event-time plus offsets, retention availability, event type/version catalog, historic semantics/code/upcasters, ordering keys, and target projection version. Inventory erasure/tombstone/encryption-key policy and exclude/quarantine data the new projection is not authorized to retain. Make the projection fold deterministic and disable all external effects; use a dedicated replay consumer group and isolated capacity so replay cannot starve live traffic.

Load a consistent base if needed, then process each partition in order with stable event-ID inbox and atomic projection/checkpoint. Bound fetch batch, bytes, concurrency, queues, and database writes; monitor lag, age, throughput, schema/upcast rejection, poison records, duplicates, gaps, and resource saturation. Pause rather than skip silently. Record replay run ID, code/schema versions, source ranges, checksums/counts by type/tenant/time, quarantines, retries, and operator actions under protected audit.

While replay catches up, live events remain in the same retained source; advance to a declared high-water mark, then enter catch-up/dual-read comparison. Compare counts, aggregates, subject versions, sampled records, invariants, and authoritative snapshots. Cut reads over only after acceptance thresholds; preserve old projection/rollback and exact checkpoint. Restart resumes from durable checkpoint without repeating external effects. After cutover continue drift reconciliation, then retire old projection according to retention and rollback policy.

### Answer 5

`DispatchUnit` is a command to one dispatch authority with command ID, incident/unit/tenant, dispatcher authorization, expected unit/incident versions, priority, issued/deadline, correlation, and safe location reference. Handler reauthorizes, serializes by unit/incident as required, and atomically records accepted/rejected/completed outcome, state changes, and outbox facts. Lost reply is resolved by same-ID retry/outcome query; expiry and cancellation/redispatch are explicit transitions, not queue deletion assumptions.

Facts include `UnitDispatchAccepted`, `UnitAssigned`, `UnitEnRoute`, `UnitArrived`, `IncidentStatusChanged`, and terminal/release facts, each stable ID/type/version/source/subject/tenant/classification/occurred time/causation and subject sequence. Partition/order by unit and/or incident according to invariant; cross-key causal links use versions/causation and reconciliation. Consumers use inboxes and current policy. Analytics receives minimized durable facts with governed schema, retention, lineage, replay, lag, poison/redrive, and erasure controls.

Browser operators receive authorized SSE notifications/projections, not the raw unrestricted log: tenant/incident sequence, retention, snapshot reset, queue/connection/replay bounds, revocation, and polling fallback. Partner agencies receive minimized signed webhooks or provisioned broker feeds depending boundary: stable event ID, partner audience, receiver inbox, producer retries/redrive, endpoint/SSRF/signature controls, and explicit durable-acceptance ack. No partner chooses dispatch outcome unless delegated as the logical authority.

Audit package is a document produced by `GenerateIncidentAuditPackage` command: job outcome/status plus immutable encrypted object, manifest, schema, coverage interval, ordered event/version references, counts/checksums, redaction/classification, access expiry, and reproducibility evidence. Package completion emits a fact/notification; object verification and import have separate acknowledgement.

Transactional outbox connects authoritative state to events. Shared envelope distinguishes message, command, event, correlation, causation, trace, subject, and attempt identities. Channel and domain authorization, schema/size/decompression/rate/tenant quotas, broker lag/backpressure, dead-letter ownership, audited policy-aware redrive, trace-safe telemetry, and reconciliation across command ledger/state/outbox/broker/inboxes/projections/packages are required. Evolve additively where semantics remain; use new types/versions/upcasters for incompatible retained meaning. Test duplicate/loss/reorder/gap, stale command, revocation, cross-tenant forgery, process/broker/region failure, slow consumers, poison/schema skew, replay, mass incident surge, and disaster recovery.
