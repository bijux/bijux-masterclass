---
module_id: API-066
program: API & Service Engineering
level: 2
module_number: 66
title: Delivery and Acknowledgment
status: complete
last_verified: 2026-09-02
---

# Delivery and Acknowledgment

## One-Page Review

### Governing question

What does each send, broker confirmation, delivery, lease, acknowledgement, offset commit, application record, and business outcome prove—and how should failures between those boundaries be handled without overstating at-most-once, at-least-once, or exactly-once guarantees?

### Essential definitions

- **producer acceptance** is the point at which a sending client or broker reports a publication outcome under a configured durability scope.
- **delivery** is an attempt to make a message available to a consumer; it does not prove application processing.
- An **acknowledgement** is a protocol/broker signal that advances delivery state under a precisely documented boundary.
- A **negative acknowledgement/reject** asks the delivery system to apply a specified retry, release, discard, or dead-letter policy.
- A **lease/visibility/ack deadline** temporarily assigns a message to a consumer; expiry can cause redelivery.
- A **checkpoint/offset commit** records consumer position for a stream/partition/subscription; it need not be atomic with application state.
- **at-most-once delivery** allows loss but prevents redelivery within a stated scope; **at-least-once delivery** allows duplicates but seeks no loss within a stated scope and limits.
- **exactly-once delivery/processing** is meaningful only with a named system boundary, failure model, configuration, and external-effect assumptions.
- **durable application acceptance** is an application-owned inbox/work record committed so processing can resume independently of broker delivery.

### Central model, mechanism, or theorem

For one logical message, consider boundaries

$$
P\rightarrow B\rightarrow D\rightarrow I\rightarrow E\rightarrow C,
$$

where $P$ is producer send, $B$ broker durable acceptance, $D$ consumer delivery, $I$ durable inbox/application acceptance, $E$ domain/external effect, and $C$ broker acknowledgement/checkpoint. A crash can occur between any adjacent boundaries. If $C$ precedes durable $I/E$, loss is possible. If $E$ precedes $C$, redelivery can repeat $E$. Safe at-least-once effects therefore require atomic $I/E/C$ where supported or stable identities plus idempotent/recoverable transitions across the split.

### Critical invariants

Every guarantee names producer, broker, destination/subscription, region, consumer, store, and external-effect scope; exact protocol/client/broker settings; durability/replication/retention; retry/lease/expiry; acknowledgement boundary; and failure assumptions. Logical message identity stays stable across attempts. Producer uncertainty after timeout is resolved by idempotent publication/outbox/state query, not a fresh fact. Consumers acknowledge only after their documented safe boundary, align batch/partition checkpoints with all prior required effects, and use inbox/effect IDs where redelivery is possible.

Leases are extended only while owned, bounded, cancellable work progresses; stale owners are fenced. Negative acknowledgement and retry classify transient/permanent/deadline/policy errors with backoff, attempt/age limits, order consequences, and dead-letter ownership. Broker “exactly once” never implies exactly-once email, payment, database, or workflow unless those effects participate in the same atomic/idempotent protocol. Monitoring distinguishes delivery attempts, duplicates, ack/nack/lease, processing outcomes, checkpoint, lag/age, unknown completion, and reconciliation.

### Common failures

Calling client enqueue a publish success; using broker ack without declaring replication/durability; assuming delivery means processing; auto-ack before handler; checkpointing a batch past failed records; acknowledging after non-idempotent external effect without effect ledger; letting lease expire while work continues; old consumer acknowledges after reassignment; repeated nack creates tight poison loop; infinite lease hides stuck work; retry after deadline executes stale command; new message ID on producer retry; treating MQTT QoS 2 or provider exactly-once feature as exactly-once business effect; transactional broker output combined with uncoordinated database write; swallowing ack failure; and reporting consumer lag alone while application inbox/effect backlog grows.

### Compact example

A payment event is delivered twice because the consumer commits the charge effect, crashes, and never acknowledges the first attempt. The second attempt carries the same event/effect ID. The consumer's effect ledger finds the completed processor charge and records its projection/checkpoint without charging again. Broker acknowledgement then means this subscription no longer needs delivery; it never means the whole order workflow finished. **Conclusion:** duplicate delivery is expected, while stable effect identity and recovery make the business outcome safe.

### Connections

[Idempotency Keys](037-idempotency-keys.md), [Commands, Events, and Messages](061-commands-events-and-messages.md), [Topic and Channel Design](064-topic-and-channel-design.md), and [Ordering and Partition Keys](065-ordering-and-partition-keys.md) define identities and topology. The next module develops idempotent consumers; dead-letter and replay modules handle terminal/recovery paths.

## Governing Question

Across producer, broker, consumer, application store, external dependencies, and workflow, what exact state transition does each acknowledgement certify, which crash windows remain, and what mechanism contains loss, duplication, stale work, and uncertain completion?

## Why This Matters

Messaging terminology compresses many boundaries into one word. A producer library can accept bytes into memory; a broker can replicate a record; a consumer can receive it; a handler can validate it; an inbox can persist it; a database can commit; an external payment can succeed; a workflow can complete. “Acked” at one boundary proves nothing automatically about the next.

Partial failure makes ambiguity unavoidable. The broker commits a publication but its response is lost, so the producer does not know whether to retry. A consumer performs an effect then crashes before acknowledgement, so the broker redelivers. A lease expires during a slow operation and two consumers act concurrently. A batch checkpoint moves beyond a poison message. Designs must make each window explicit.

Products expose different mechanisms and scopes. Kafka describes producer, partition log, offsets, transactions, and consumer delivery semantics. AMQP defines delivery states and settlement. MQTT 5.0 defines QoS handshakes, packet/session/message expiry, and acknowledgements. Pulsar exposes individual/cumulative acknowledgement, subscriptions, redelivery, and transactions/features. Google Pub/Sub documents acknowledgement deadlines/leases and a scoped exactly-once delivery feature. These mechanisms are useful but not interchangeable.

Correct systems choose a guarantee that matches business risk. At-most-once can fit replaceable telemetry. At-least-once plus idempotent effect fits many domain events. Broker transaction can atomically consume and produce within its ecosystem. A payment, email, or third-party API still needs its own stable effect protocol. Honest scoping is more valuable than a stronger marketing label.

## Prerequisites and Retrieval

Retrieve [Idempotency Keys](037-idempotency-keys.md), [Deadlines, Cancellation, and Metadata](054-deadlines-cancellation-and-metadata.md), [Commands, Events, and Messages](061-commands-events-and-messages.md), [Topic and Channel Design](064-topic-and-channel-design.md), and [Ordering and Partition Keys](065-ordering-and-partition-keys.md). Be able to enumerate crash windows around send, broker commit, delivery, effect, and acknowledgement.

Retrieve exact producer acknowledgements, replication/durability, retries/idempotence/transactions, subscription/consumer assignment, ack/nack/cumulative/batch behavior, lease/visibility extension, retention/expiry, dead-letter, and region/failover semantics for the selected provider/client versions.

## Learning Objectives

After completing this module, you can:

1. label every producer, broker, delivery, application, effect, and workflow acknowledgement boundary;
2. compare at-most-once, at-least-once, and exactly-once claims within explicit scopes;
3. design producer publication recovery for lost responses and duplicate attempts;
4. choose consumer acknowledgement timing based on durable state and effects;
5. align offset/checkpoint, batch, cumulative ack, and per-key ordering safely;
6. operate lease/visibility deadlines with progress, bounds, cancellation, and fencing;
7. classify nack/retry/expiry/dead-letter behavior without loops or stale commands;
8. integrate database and external effects using inbox/outbox/effect ledgers and reconciliation;
9. test all crash windows, failover, rebalances, late acks, and provider feature limits; and
10. observe delivery separately from application and business outcomes.

## Core Exposition

### Draw the acknowledgement ladder

For every message flow, draw states and evidence:

1. producer application commits source/outbox intent;
2. producer client accepts/enqueues record;
3. network/broker leader receives;
4. broker meets configured durability/replication and acknowledges;
5. consumer subscription makes a delivery/record available;
6. consumer validates/authenticates/schema-checks;
7. durable inbox/work record commits;
8. local domain/projection transaction commits;
9. external effects complete or are durably scheduled;
10. consumer acknowledges/commits checkpoint;
11. downstream workflow reaches terminal outcome.

Name which rung an API response, callback, metric, and alert refers to. “Published” should not mean client buffer on one dashboard and replicated broker record on another. “Processed” should distinguish validated, accepted, local state committed, external effect completed, and workflow complete.

Some rungs combine. A Kafka transaction can atomically commit consumed offsets and produced records within a supported Kafka scope. A database transaction can atomically commit inbox, projection, and outbox. A managed queue ack cannot generally join an arbitrary database transaction. Identify actual atomic boundaries rather than draw one distributed transaction in prose.

### Specify producer acceptance

Producer starts from one logical message/event ID and immutable content. If source state and publication must agree, write a transactional outbox/log entry with source transaction. Publisher retries the same record identity until broker acceptance is known or reconciliation resolves uncertainty.

Producer client enqueue only proves local library accepted work. Asynchronous send callback/future and flush/shutdown policy determine when failures surface. Process crash can lose buffered records unless source outbox resumes. Bound producer buffer, delivery timeout, retries, backoff, in-flight work, message age, and shutdown drain.

Broker acknowledgement strength depends on leader/replica/quorum, persistence, min in-sync replicas, transaction, region, and failure configuration. A returned success under weak replication may not survive a correlated failure. State the selected settings/SLO and test failover; do not cite product defaults as durable guarantee.

If broker accepts but response is lost, producer retry may duplicate. Provider idempotent producer/session sequencing can suppress duplicates within its scope, but application event ID remains stable across restart, failover, outbox replay, bridge, and migration. Never generate a new event fact simply because an attempt timed out.

### Define at-most-once delivery honestly

At-most-once usually acknowledges/advances before effect or does not retry after uncertain delivery. It can lose messages on consumer crash/network ambiguity. It fits sampling, high-frequency replaceable telemetry, cache hints, or notifications where newer state supersedes and loss budget is explicit.

“At most once” does not mean effect occurs once; a handler bug/client retry outside the scoped transport can still duplicate. Nor does it mean zero duplicates across migrations/replay. State failure model and identity scope.

If loss is acceptable, design detection/statistics and fallback: sequence gaps, periodic snapshots, polling current state, or reconciliation. Do not silently select auto-ack for financial/workflow events because it is convenient.

### Define at-least-once delivery honestly

At-least-once retains/retries/redelivers until acknowledgement or configured expiry/attempt/dead-letter boundary. It allows duplicates when handler/effect succeeds but acknowledgement is lost, lease expires, consumer crashes, or broker fails over. “At least once” is never infinite: retention, TTL, max delivery attempts, dead-letter, data loss disaster, and authorization may terminate delivery.

The consumer must be idempotent or route work through stable inbox/effect identities. A duplicate should be cheap and observable. The next module develops patterns; here the key is acknowledgement timing: do not ack before the durable boundary needed to recover, and expect redelivery after it.

At-least-once delivery plus idempotent local state can give effectively once-per-event local transition within dedup retention. External effects require their own idempotency/query/reconciliation. Avoid unqualified “exactly once.”

### Scope exactly-once claims

Exactly-once can refer to broker delivery to one subscription in one region, transactional consume-transform-produce, or one local state transition keyed by message ID. Each is valuable. Name the boundary, feature/config, client versions, retry/lease constraints, and excluded effects.

Google Pub/Sub's exactly-once delivery feature, for example, is tied to pull subscriptions and documented regional/acknowledgement behavior and does not automatically make arbitrary subscriber side effects exactly once. MQTT QoS 2 describes protocol packet/message delivery between client/server under session semantics, not a global business charge. Kafka transactions can atomically commit Kafka offsets/output records for configured consumers but do not atomically commit an unrelated database/email by default.

An exactly-once outcome across an external API is achievable only if that API participates via idempotency/effect ID, transactional resource, reservation/commit, or queryable outcome that resolves ambiguity. Otherwise the two generals-style uncertainty remains around response loss.

Prefer claim language such as “each event ID changes this projection at most once while inbox retention covers replay” or “consume offsets and produced records commit atomically within this Kafka cluster/transactional pipeline.”

### Choose consumer acknowledgement boundary

Options:

- **before processing:** lowest broker hold time, at-most-once/loss on crash;
- **after validation only:** malformed rejected but valid work can be lost unless durably staged;
- **after durable inbox:** broker can forget delivery; application owns later processing/retry;
- **after local effect transaction:** straightforward at-least-once with inbox/idempotency;
- **after external effect:** duplicate external calls possible if ack lost; needs effect ID/ledger;
- **after whole workflow:** often too slow/coupled; prefer durable acceptance plus outcome events/state.

The best boundary is the earliest durable state from which required work can recover without broker redelivery. Durable inbox decouples long workflows and acknowledges quickly, but transfers backlog/retry/monitoring/retention responsibility to the application. If no inbox, acknowledge after atomic local commit.

Validation/policy failures may be terminal reject/dead-letter, not ack as success. Record safe reason. Authorization can change between inbox and later work; decide whether acceptance snapshots delegated authority or execution reauthorizes.

### Align offsets, cumulative acknowledgements, and batches

Stream offsets/checkpoints often represent “all records before position are complete.” If processing concurrent records, commit only the highest contiguous completed offset; a hole at 100 prevents committing 101+ unless work at 100 is durably owned elsewhere and semantics permit. Committing maximum observed offset loses holes on restart.

Cumulative acknowledgement similarly acknowledges a range; use only when every prior delivery satisfies safe boundary. Individual ack improves isolation but may cost/state more. Exact provider behavior differs.

Batch fetch is not batch business atomicity. Validate each record, track result, and define partial failure. If one poison record blocks a partition, use bounded quarantine/reset policy; do not ack the batch wholesale. If applying a batch transaction, ensure all effects and checkpoint join it or each record has inbox/effect identity.

For per-key order, a failed earlier key version can block later same-key commit even if partition checkpoint handling lets other keys proceed. Durable inbox can accept a whole batch then process keyed lanes later; checkpoint means inbox acceptance, not effect completion, and telemetry must show both backlogs.

### Operate leases and visibility timeouts

Queue/pull systems lease a message for an acknowledgement deadline/visibility timeout. Set initial lease above normal setup but below unacceptable recovery delay. Extend based on measured progress, not blindly forever. Bound total processing/lease lifetime, extension increments, concurrent leases, in-flight bytes, and renew failures.

If work exceeds lease, either durably stage/inbox then ack, split into bounded job, or extend while fenced ownership remains. Network pause can lose lease while handler continues; use delivery/lease token or application ownership epoch so late owner cannot commit/ack after reassignment.

Ack IDs/tokens can expire or become invalid after redelivery. Treat ack response/error as evidence and reconcile; do not assume local call success without provider confirmation where feature requires it. A late ack must not acknowledge a newer delivery accidentally.

Visibility extension is not cancellation or progress truth. When deadline/cancellation occurs, stop downstream work cooperatively, release/nack/let expire according to policy, and record durable outcome. Effects already committed are not rolled back.

### Design nack, release, retry, and expiry

Classify errors:

- transient dependency/capacity: delayed retry with exponential jitter/Retry-After equivalent;
- malformed/incompatible: quarantine/dead-letter after validation evidence;
- unauthorized/forbidden: terminal reject or policy-hold, not endless retry;
- expired/stale command: terminal expired outcome;
- conflict/precondition: domain rejection or replan, not generic transport retry;
- unknown failure: bounded retry then quarantine/incident.

Immediate nack/redelivery loops can consume all capacity. Use delay/backoff, attempt/age budgets, per-key/tenant bulkheads, circuit breakers, and poison isolation. Provider dead-letter max attempts may be approximate/feature-scoped; application still records attempts/identity.

Message expiry/retention can race lease/retry. State whether expired in-flight work may finish and how producer/caller learns terminal outcome. Facts usually remain true after TTL; TTL controls delivery relevance, not truth. Commands can become unsafe after deadline.

Retry paths can reorder; preserve original ID/key/sequence and apply preceding module's gap rules. Redrive revalidates current schema/auth/deadline/idempotency and is auditable/rate-limited.

### Integrate local database effects

Best local pattern: atomically insert inbox keyed by consumer/message ID/fingerprint, apply projection/domain change, enqueue any outgoing outbox facts, and advance local checkpoint within one database transaction where possible. Duplicate unique conflict loads prior result and acknowledges safely.

If broker supports transaction connecting consumed offsets and produced broker records, use it for that pipeline with stable transactional identity/fencing and read-committed consumers as required. If application database is outside transaction, do not assume it joins. Use inbox/outbox and reconciliation.

If effect transaction commits then process crashes before ack, duplicate finds inbox. If ack commits then database rolls back, design is wrong unless work was durably staged elsewhere. Test both fault injections.

Dedup retention must cover maximum broker retention/replay/redrive/disaster horizon. If inbox entries expire sooner, old replay can repeat effects; versioned projections or permanent business effect IDs may still protect.

### Integrate external effects

For payment/email/webhook/vendor call, derive stable effect ID from logical event plus effect kind/recipient/scope. Record intent durably, call external system with its idempotency key where supported, record outcome. On timeout query by key before retry. If provider lacks idempotency/query, duplicates or loss remain; use reservation/manual reconciliation or accept documented risk.

Do not hold broker lease/transaction open for an unbounded external workflow. Durable inbox/effect ledger then acknowledge, and run effect state machine separately. Publish outcome fact after recorded result via outbox. This makes application backlog visible and recoverable.

Email providers may accept then later bounce; “accepted” differs from delivered. Payment authorized differs from captured/settled. Webhook 2xx differs from downstream business completion. Preserve domain-specific outcome states.

Compensation is a new authorized effect, not an acknowledgement rollback. It has its own ID/outcome and may fail.

### Bound throughput and backpressure

Prefetch/receive maximum/in-flight concurrency trades throughput against lease expiry, memory, duplicate work, and rebalance drain. Set per-instance/partition/key/tenant message/byte/concurrency bounds. Pull consumers fetch according to capacity; push consumers apply flow control/pause/nack without loops.

Let arrival rate $\lambda$, effective service rate $\mu$, and average processing time $W$. Stable backlog requires sustainable $\mu>\lambda$ with failure headroom; Little's Law approximates in-flight $L=\lambda W$ under stable conditions. Acknowledging into an inbox moves, not removes, backlog; monitor inbox age/size and workers.

Autoscaling on broker lag alone can over-scale a downstream-limited dependency and amplify failure. Include processing latency, error/retry, lease expiry, external capacity, key skew, and quota. Apply admission/circuit breaking and recovery budgets.

### Secure acknowledgement and control planes

Only authorized consumer identity/group/subscription may acknowledge. Bind ack token/delivery to subscription, tenant, lease, and attempt per provider. Do not expose arbitrary ack/nack/replay/redrive endpoints without authentication, authorization, CSRF/replay protection, rate limits, and audit.

A forged message cannot gain authority because broker delivered it. Validate producer/source/tenant/type/schema and domain authorization before acceptance/effect. A poison actor can intentionally cause long leases/retries; enforce size/complexity/time and per-tenant limits.

Dead-letter payloads, inboxes, effect ledgers, ack diagnostics, and traces contain sensitive data/identifiers. Minimize/encrypt/retain/erase/access-control them. Do not log credentials, full payload, or ack tokens.

### Observe and verify every boundary

Producer metrics: outbox backlog/age, attempts, client buffer, broker ack latency/result, unknown/timeouts, duplicate suppression, publish reconciliation. Broker: partitions/replicas, ingress, retention, delivery attempts, leases, ack/nack, expiries, redelivery/dead-letter, subscription lag/age.

Consumer: received/validated/rejected, inbox new/duplicate/conflict, processing started/completed/failed, local/external effect outcomes, ack result/latency, lease extensions/loss, contiguous checkpoint, retry/quarantine/redrive, stale owner, and backlog age at broker/inbox/effect/workflow.

Trace stable logical IDs and attempt IDs separately with safe cardinality. SLOs should name boundary: “99% of accepted events reach durable consumer inbox within X,” “effects complete within Y,” and “unknown outcomes reconciled within Z.”

Fault matrix injects crash before/after every boundary, response loss, broker leader/region failover, producer restart, duplicate, consumer process pause, lease expiry, late ack, rebalance, database rollback/commit race, external timeout-after-success, ack service outage, poison flood, retry exhaustion, dead-letter/redrive, retention expiry, and disaster replay. Assert business invariants and no silent loss, not merely client success codes.

## Definitions and Notation

Let logical message $m$ have attempts $a_1,\ldots,a_n$. Boundaries are producer/source $P$, broker durable acceptance $B$, delivery $D$, durable inbox $I$, local/external effect $E$, consumer acknowledgement/checkpoint $C$, and workflow outcome $W_f$.

Let $Ack_X$ mean acknowledgement of boundary $X$ only. Implication $Ack_B\nRightarrow E$ and $Ack_C\nRightarrow W_f$ generally. Let inbox/effect state $J(id_m)$ be unique by scope and canonical fingerprint. Duplicate delivery is safe if state transition/effect is idempotent or returns recorded result.

Let arrival/service rates $\lambda,\mu$, mean time $W$, in-flight $L\approx\lambda W$ under stable Little's Law assumptions, lease expiry $t_l$, command deadline $t_d$, and retry age $t_a$. Retry/extension must respect applicable bounds; $t_l$ is not proof of business deadline.

## Mechanisms, Invariants, or Proof Structure

1. Draw producer→broker→delivery→inbox→effect→ack→workflow states and name evidence.
2. Pin provider/client configuration, durability, retention, retry, lease, ack, failover, and exactly-once scope.
3. Keep logical ID/content stable across producer and consumer attempts; recover unknown publication.
4. Choose earliest durable consumer boundary that can resume all required work.
5. Atomically align inbox/local state/outbox/checkpoint where possible; otherwise use stable effect protocol and reconciliation.
6. Preserve contiguous batch/partition/key completion and fence stale lease/rebalance owners.
7. Classify nack/retry/expiry/poison with backoff, attempts/age/dead-letter/redrive and order policy.
8. Bound prefetch/in-flight/leases/backlogs/rates and monitor broker plus application queues.
9. Secure message, acknowledgement, replay, and redrive control planes and stored evidence.
10. Inject failure between every boundary and verify business invariants/recovery.

Proof sketch for the classic trade-off: if acknowledgement $C$ occurs before the only durable effect/acceptance $E$, crash after $C$ before $E$ loses work. If $E$ occurs before $C$, crash after $E$ before $C$ causes redelivery and can duplicate effect. Eliminating both requires an atomic boundary containing $E$ and $C$, or making repeated $E$ observationally idempotent/recoverable via stable identity.

## Alternatives and Trade-Offs

**At-most-once versus at-least-once.** At-most-once avoids redelivery but permits loss; at-least-once avoids loss within scope but requires duplicate safety and retention/retry operations.

**Ack after effect versus durable inbox.** Ack-after-effect uses broker as work queue but holds leases and duplicates effects on lost ack. Inbox acknowledges earlier and handles long work safely but creates an application queue to operate.

**Individual versus cumulative/batch ack.** Individual isolates failures at metadata/throughput cost. Cumulative/batch is efficient but cannot skip unresolved predecessors safely.

**Short lease versus long/extended lease.** Short recovers crashed work quickly but duplicates slow work; long reduces duplicates but delays recovery. Progress-based bounded extension plus fencing is robust.

**Broker transaction versus inbox/outbox.** Broker transactions compose broker records/offsets elegantly; inbox/outbox spans application database but permits duplicate publication. External effects still need identities/reconciliation.

**Automatic retry versus explicit workflow state.** Automatic retry fits short transient failures. Long/business work needs queryable application state, deadlines, operator controls, and outcomes.

**Strong exactly-once feature versus portable idempotency.** Provider feature can reduce duplicates/complexity within its scope; portable stable IDs protect across brokers, bridges, replay, migrations, and external systems but require application storage.

## Failure Modes and Misconceptions

1. Producer client buffer acceptance is called durable publication.
2. Broker ack omits replication/quorum/region/failure assumptions.
3. Delivery/handler entry is treated as successful processing.
4. Auto-ack or checkpoint occurs before recoverable application acceptance.
5. Ack-after-external-effect has no stable effect ID/outcome query.
6. Batch/cumulative ack advances past a hole or poison record.
7. Lease expires while stale handler continues and both owners commit.
8. Infinite lease extension hides deadlock and delays recovery.
9. Immediate nack creates hot redelivery loop and starvation.
10. Expired command is retried as if still authorized/relevant.
11. Broker exactly-once/QoS scope is marketed as exactly-once business workflow.
12. Broker transaction is assumed to include unrelated database/external effect.
13. Dedup/inbox retention is shorter than replay/redrive horizon.
14. Ack errors/results are ignored; control tokens leak into logs or APIs.
15. Broker lag is green while inbox/effect/workflow backlog is failing.

## Worked Examples

### Example 1

Producer outbox sends event, broker commits, response is lost. Publisher retries same event ID/content. Broker/client idempotence may suppress duplicate; if not, consumer inbox does. New event ID would create a second fact and is forbidden.

### Example 2

Telemetry cache hint auto-acks before processing under explicit at-most-once loss budget. Sequence gaps are acceptable because periodic full snapshot refreshes state. This boundary would be invalid for ledger transitions.

### Example 3

Projection consumer transaction inserts inbox, updates row, writes derived outbox, and stores checkpoint. Crash after commit before broker ack redelivers; unique inbox returns prior result and ack succeeds without duplicate projection/output fact.

### Example 4

Email consumer durably records `send-email:{event,recipient,template}` effect, acknowledges event, then worker calls provider with same idempotency key. Timeout queries outcome. Provider acceptance/bounce states remain distinct from broker ack.

### Example 5

Batch offsets 100–109 process concurrently; 104 fails. Commit tracker advances only through 103 unless 104 is durably inbox-owned and the contract defines checkpoint as inbox acceptance. Committing 109 directly would lose 104 on restart.

### Example 6

A 30-second lease covers normal 5-second handler. Slow job is staged to durable application queue and acked rather than extending for an hour. If extension is used, total lease and progress are bounded and ownership epoch fences stale workers.

### Example 7

Malformed payload is schema-invalid. Immediate nack caused 10,000 deliveries/minute. Policy changes to one validation record, terminal protected quarantine, rate-limited operator redrive after schema/upcaster fix, preserving identity and attempt history.

### Example 8

Kafka consume-transform-produce pipeline commits offsets and output records transactionally under its configured scope. A parallel database audit write is outside that transaction, so it uses inbox/outbox/reconciliation instead of being called exactly once.

### Example 9

Payment capture succeeds at processor; response and consumer ack are lost. Redelivery uses stable capture key and queries processor, records prior success, then acknowledges. Without provider idempotency/query, duplicate-charge risk remains and requires manual/reservation design.

### Example 10

Dashboard shows broker lag zero because handlers ack into inbox quickly, but effect queue is six hours old. End-to-end SLO/alerts include inbox/effect age and unknown outcomes, revealing the incident that transport-only metrics hid.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, transactions, logs, leases, and impossibility/ambiguity reasoning. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies atomicity, unique constraints, inbox/outbox, checkpoints, and effect ledgers. [Security Engineering](../../25-security-engineering/ROADMAP.md) governs message/control-plane authorization, replay, and sensitive operational state.

[Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) contributes SLOs, retries, backpressure, fault injection, and incident recovery. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns broker/client defaults, consumer frameworks, transactions, DLQ/redrive, telemetry, and paved roads. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes boundary definition, hazard analysis, verification, and assurance claims.

## References

1. Apache Software Foundation. “Apache Kafka 4.2 Design: Message Delivery Semantics.” <https://kafka.apache.org/42/design/design/#message-delivery-semantics>
2. OASIS. “Advanced Message Queuing Protocol (AMQP) Version 1.0.” 29 October 2012. <https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-complete-v1.0-os.html>
3. OASIS. “MQTT Version 5.0.” 7 March 2019. <https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html>
4. Apache Software Foundation. “Apache Pulsar: Messaging Concepts.” Retrieved 2026-09-02. <https://pulsar.apache.org/docs/next/concepts-messaging/>
5. Google Cloud. “Exactly-Once Delivery in Pub/Sub.” Retrieved 2026-09-02. <https://docs.cloud.google.com/pubsub/docs/exactly-once-delivery>
6. Google Cloud. “Lease Management in Pub/Sub.” Retrieved 2026-09-02. <https://docs.cloud.google.com/pubsub/docs/lease-management>

## Exercises

### Exercise 1

For a message-driven invoice workflow, list at least nine acknowledgement/outcome boundaries from source transaction through final customer delivery. State what each proves and what it does not.

### Exercise 2

A consumer receives 2,000 messages/s and mean handler time is 0.4 s. Estimate in-flight work by Little's Law. With safe maximum 500 concurrent messages, assess stability/capacity and propose backpressure. Explain why acknowledging to a durable inbox changes which queue is measured, not total work.

### Exercise 3

Design acknowledgement for a batch stream consumer that updates a database and emits derived events while preserving partition order. Include inbox/outbox, contiguous checkpoints, batch partial failure, crash windows, duplicate, poison, rebalance, and verification.

### Exercise 4

Design lease/visibility and effect handling for a queue-triggered video-transcoding job that can take 30 minutes and writes to object storage. Include staging, idempotency, progress, cancellation, lease loss, stale-owner fencing, retries, output commit, ack, and observability.

### Exercise 5

Evaluate an “exactly-once payment notifications” claim using a broker transaction, relational database, payment provider, email provider, and webhook partner. Rewrite the claim into precise scoped guarantees and design mechanisms/reconciliation for every boundary.

## Answers to the Exercises

### Answer 1

Boundaries: invoice state/outbox transaction committed; publisher client enqueued; broker durably accepted under replication policy; target subscription delivery created; consumer received; schema/auth validated; durable inbox/work accepted; invoice projection/local state committed; customer communication effect scheduled; provider accepted email/webhook; provider delivered/bounced or partner durably accepted; overall invoice workflow terminal.

Each proves only its state. Source/outbox proves publication obligation exists, not broker receipt. Client enqueue proves local buffering, not durability. Broker ack proves configured broker boundary, not consumer delivery. Delivery proves attempt, not validation/effect. Validation proves shape/policy at that moment, not durable recovery. Inbox proves application owns work, not completion. Local commit proves local effect, not external delivery. Provider acceptance proves provider boundary, not inbox visibility/customer reading/business completion. Workflow outcome composes explicitly required sub-outcomes but not unrelated consumers.

For each, record identity, timestamp/result, owner, retry/query, and failure. Public API/status uses terms such as queued, durably accepted, processing, sent-to-provider, delivered/bounced where evidenced, and complete/partial—not a single “processed.”

### Answer 2

Little's Law estimate is $L=\lambda W=2{,}000\times0.4=800$ in-flight messages under stable average assumptions. A safe cap of 500 cannot sustain 2,000/s at 0.4 s: maximum ideal service is $500/0.4=1{,}250$/s before headroom/failures, so backlog grows about 750/s. Reduce arrival/admit rate, increase safe workers/resources/downstream capacity, lower handler time, or partition/scale while respecting key/order and dependency quotas.

Use pull/prefetch/receive maximum 500 or lower headroom, bound bytes and per-tenant/key lanes, pause fetch/extend only progressing leases, and expose overload rather than buffering unboundedly. Autoscale only if downstream/store/provider capacity grows; otherwise rate-limit/circuit-break and retain broker backlog within age SLO.

If handler durably writes inbox quickly and acknowledges, broker in-flight/lag falls, but 800-equivalent work moves to inbox/effect queue. Measure inbox arrival/service/backlog age, storage, retries, and worker capacity. End-to-end completion remains limited by 1,250/s unless processing changes. Ack changes failure ownership and lease pressure, not conservation of work.

### Answer 3

For each record use stable consumer-scope inbox key/fingerprint. Within one database transaction insert inbox, apply projection/domain transition, insert derived outbox record with stable ID, and mark record complete; or durably inbox entire batch then process keyed/ordered later. Never publish derived event directly beside database commit.

Track completion per partition/offset. Advance broker checkpoint only to highest contiguous offset whose documented safe boundary is complete. If offset 104 fails while 105–109 finish, do not commit beyond 103 unless all later records plus 104 are durably application-owned and checkpoint semantics explicitly mean inbox acceptance. Preserve per-key subject sequence regardless.

Duplicate unique conflict returns recorded state/derived ID. Transient failure retries with jitter/bounds; poison quarantines original ID/key/schema/offset after terminal decision and requires explicit gap/reset policy before checkpoint crosses. Batch success is not all-or-nothing unless one bounded transaction actually covers it. Rebalance stops fetch, drains/cancels bounded work, commits contiguous state, and fences old owner; new owner resumes from checkpoint/inbox.

Crash tests: before inbox, during rolled-back transaction, after database/outbox commit before checkpoint, after publisher sends before outbox mark, after checkpoint, and during rebalance. Verify no lost projection, stable duplicate derived event, contiguous versions, recoverable poison, and eventual outbox publication. Observe broker lag, inbox backlog, offset holes, transaction latency, duplicates/conflicts, outbox age, retry/quarantine, and fence failures.

### Answer 4

Queue handler validates/authenticates job then atomically records durable transcode job/effect ID derived from source object/version/profile and initial state. Once staged, acknowledge queue promptly; application job queue, not a 30-minute broker lease, owns recovery. Worker leases job in short renewable epochs, records progress/checkpoints/output temporary object, and renews only while measurable progress occurs, with maximum attempt/lifetime and cancellation checks.

Every write is under job ID/attempt epoch. Output goes to attempt-scoped temporary location; final publish is conditional/atomic manifest or rename/object pointer guarded by current ownership and expected input checksum. Stale worker after lease loss cannot mark job complete or replace final pointer because epoch fence fails; it stops/cancels and cleans temporary output. Duplicate message finds existing job/outcome.

Cancellation marks desired state; workers stop cooperatively. Already published output is retained/deleted under explicit policy, not magically rolled back. Transient compute/storage retry resumes from checkpoint; corrupt input/unsupported codec/authorization becomes terminal protected quarantine/outcome. Unknown upload completion queries object/checksum before repeating.

Publish `TranscodeCompleted/Failed/Cancelled` via outbox after job terminal commit. Observe queue accept, application backlog age, lease epoch/renew/loss, progress age, attempts, resource use, temp/final objects, output checksum, cancellation latency, outcome publication, and orphan cleanup. Test worker/process/network pause beyond lease, two workers, storage response loss, partial output, source mutation, cancellation races, region failover, and disaster recovery.

### Answer 5

Rewrite claim: “Within configured broker transaction scope, each consumed input offset and resulting broker output record commit atomically and are read with the required isolation. Within the relational database, each message ID changes notification/effect state at most once for the retained replay horizon. Payment/email/webhook effects use stable provider-facing effect IDs and query/reconciliation; no unqualified exactly-once end-to-end delivery or human receipt is claimed.”

Broker transaction consumes facts and produces work/outcome records only within supported cluster/region/client settings, with stable transactional identity/fencing and fault tests. Database consumer uses inbox+effect ledger+outbox transaction because database is not assumed to join broker transaction. Crash after DB commit before offset/ack redelivers and inbox returns prior state.

Payment effect uses stable capture/refund ID, provider idempotency and outcome query; timeout never generates new key. Reconcile ledger/provider amounts/status and handle authorization/capture/settlement separately. Email effect uses recipient/template/version ID and provider idempotency if offered; provider accepted, delivered, bounced are separate, and human reading is not guaranteed. Webhook uses stable event ID, signed immutable payload, receiver inbox contract, retries/dead-letter/redrive; 2xx means receiver's documented acceptance, not downstream workflow completion.

For providers without idempotency/query, state duplicate/loss risk and add reservation/manual reconciliation or redesign. Publish effect outcomes through outbox; overall workflow aggregates required terminal states and exposes partial/unknown. Monitor every boundary/backlog and reconcile broker IDs, database ledger, provider reports, email events, webhook attempts/partner receipts. Inject response loss after every commit, duplicate, provider timeout, broker/DB outage, region failover, stale worker, replay, and compensation failure. Exactly-once labels remain scoped to proven atomic boundaries.
