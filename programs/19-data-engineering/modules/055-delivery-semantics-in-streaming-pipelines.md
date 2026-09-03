---
module_id: DE-055
program: Data Engineering
level: 2
module_number: 55
title: Delivery Semantics in Streaming Pipelines
status: complete
last_verified: 2026-09-03
---

# Delivery Semantics in Streaming Pipelines

## One-Page Review

### Governing question

For each boundary in a streaming pipeline, when may the system declare an input complete, what can happen after every relevant crash or timeout, and how can operators prove whether records may be omitted, replayed, duplicated, delayed, or made visible more than once?

### Essential definitions

- A **delivery scope** names the source, subscription or group, destination, identity, interval, and failure model to which a guarantee applies.
- A **delivery attempt** is one presentation of a logical input to a consumer. Redelivery is another attempt for the same source identity; a producer duplicate may be a distinct source record.
- An **acknowledgement** tells a delivery service that an attempt or message may stop being offered under the service contract.
- A **checkpoint** is durable recovery progress, commonly the next source position to process or a snapshot containing source positions and state.
- The **processed frontier** is the largest contiguous source prefix whose application work has completed under the declared meaning of processed.
- The **effect frontier** is the largest contiguous prefix whose required destination effects are durably accepted.
- **At-most-once delivery** permits omission but prevents service-level redelivery within its scope, commonly by acknowledging before work.
- **At-least-once delivery** avoids omission while replay remains possible, commonly by acknowledging or checkpointing after work.
- **Exactly-once delivery** is a product-specific promise that a named source message is not delivered again after successful acknowledgement under documented constraints. It does not automatically make arbitrary external effects occur once.
- **Exactly-once state/effects** means each logical input changes a named state or effect boundary once despite retries; this is different from executing handler code once.
- A **crash window** is an interval between non-atomic milestones in which failure changes recovery behavior.
- A **replay set** contains inputs after the durable checkpoint that may be presented again. An **omission set** contains required inputs skipped because recovery progress advanced too early or history disappeared.
- A **poison record** repeatedly fails deterministically or violates policy; a **transient failure** may succeed on a bounded retry.
- A **dead-letter/quarantine path** is an explicit alternate outcome with identity, reason, evidence, authorization, retention, and replay policy—not proof that the primary result succeeded.
- An **uncertain acknowledgement** means the caller cannot determine whether the service accepted an ack, checkpoint, or output request. The retry protocol must tolerate either outcome.

### Central model, mechanism, or theorem

For a partition with ordered source positions, let $F$ be the fetched frontier, $P$ the largest contiguous processed frontier, $E$ the largest contiguous durably accepted effect frontier, and $C$ the durable checkpoint; all are expressed as the next position. A conservative after-effect checkpoint policy maintains

$$
C \le E \le P \le F.
$$

If failure occurs, potential replay is the half-open interval $[C,F)$ and potential duplicate effects are $[C,E)$. Advancing $C$ beyond $E$ creates the possible omission interval $[E,C)$. At-most-once commonly accepts that omission window; at-least-once keeps $C\le E$ and accepts replay. Removing both windows requires one atomic or equivalent recovery protocol across the effect and progress boundary, developed in DE-056.

For a pipeline of stages, a guarantee composes only if identities and recovery boundaries compose. Informally,

$$
G_{\mathrm{end}} \preceq \min(G_1,G_2,\ldots,G_n),
$$

where the ordering means “no stronger than,” but even the minimum is not valid when stages use incompatible identities, lose history, bypass acknowledgements, or expose effects outside the coordinated boundary.

### Critical invariants

- Every guarantee names its source generation, subscription/group, destination, message identity, interval, acknowledgement/checkpoint event, and included failures.
- Fetched, deserialized, validated, transformed, state-applied, output-accepted, published, and acknowledged are separate milestones.
- A checkpoint is the next input to process and advances only across a contiguous completed prefix; concurrent holes are never hidden by a later completion.
- At-least-once paths keep recoverable source history until accepted progress and tolerate re-execution from the durable checkpoint.
- At-most-once paths document which failures can omit work, why omission is acceptable, and how omissions are measured or reconciled.
- Unknown ack/commit/output results are treated as ambiguous, never silently converted to success or definite failure.
- Batch acknowledgement semantics cover every member and partial outcome; one successful item cannot advance progress over a failed earlier item.
- Redelivery identity survives retries; producer duplicates, republished records, split batches, and re-encoded events are not assumed identical without an explicit occurrence key.
- Retry classification, maximum attempts/time, backoff, deadline, retention margin, and terminal disposition are bounded and observable.
- Poison handling does not block a partition indefinitely or discard governed data silently; quarantine preserves lineage and controlled replay.
- Ownership generation and checkpoint authority prevent revoked or stale consumers from advancing progress.
- Snapshot/state recovery includes compatible source positions; restoring state and independently choosing offsets cannot create gaps or double application.
- Delivery promises are evaluated separately for source-to-client, client-to-handler, state, output log, external sink, and consumer-visible publication.
- Replay drills inject failures before and after each milestone and compare input identities, accepted effects, checkpoints, quarantine, and visible results.

### Common failures

Common failures include calling a system “exactly once” without naming the scope; acknowledging on fetch; committing the end of a batch while lower offsets still run; assuming a successful handler return means a database write is durable; treating an ack timeout as failure and a retry as harmless; mistaking producer duplicates for broker redelivery; deleting source history before the recovery margin; retrying permanent schema or authorization errors forever; dead-lettering without lineage or replay controls; restoring state from one checkpoint and offsets from another; letting a stale owner commit; considering zero lag proof of effects; summing per-stage guarantees without inspecting boundaries; and measuring attempts instead of logical outcomes.

### Compact example

A consumer starts at next offset 100 and fetches 100–104. If it commits 103 before applying record 102, then crashes, recovery starts at 103 and record 102 is omitted. If it applies 102 but the durable checkpoint remains 102, a crash causes 102 to be replayed and its non-idempotent effect may duplicate. If effect 102 and next offset 103 share one atomic recovery boundary, recovery sees both or neither. The arithmetic identifies crash windows; it does not prove that a particular database, broker, connector, or transaction protocol implements the atomic case.

### Connections

[DE-051](051-streams-logs-and-unbounded-data.md) established occurrence identity, replayable logs, and finite cuts. [DE-052](052-topics-partitions-and-offsets.md) defined next-position coordinates and retention. [DE-053](053-producer-keys-and-ordering.md) separated producer duplicates and partition order. [DE-054](054-consumer-groups.md) supplied epoch-scoped ownership and checkpoint handoff. DE-056 will design exactly-once effects, while DE-057 through DE-060 treat time, windows, state, and late/duplicate/out-of-order inputs.

## Governing Question

“Is this pipeline at least once?” is not yet an engineering question. At least once from which source identity to which observation? Does “delivered” mean returned by a client library, admitted to a handler, stored in application state, appended to an output topic, accepted by an external API, or visible to a user? Which crashes, network partitions, regional failures, retention losses, operator resets, and software defects are included?

Delivery semantics arise from the ordering and atomicity of milestones. A consumer fetches, decodes, validates, computes, changes state, writes outputs, records progress, and acknowledges. If these actions cross independently failing systems, every ordering leaves a crash window. Acknowledging first can skip unfinished work. Acknowledging last can repeat finished work. A product can narrow the window with transactions, idempotency, deduplication, snapshots, leases, or reconciliation, but a label cannot close it.

The governing task is therefore to draw the recovery protocol. Name every durable frontier, put failures between every pair of milestones, and calculate the result after restart. A useful guarantee is a testable statement about logical identities and observable outcomes over a bounded interval. It includes exclusions and recovery evidence.

This module concentrates on delivery, replay, omission, checkpoint timing, and guarantee composition. It deliberately does not claim that avoiding repeat delivery makes arbitrary business effects occur once. DE-056 develops the transaction, idempotency, ledger, outbox, and reconciliation mechanisms needed at effect boundaries.

## Why This Matters

Most streaming failures happen after some work succeeded and before related progress became durable. A payment notification is sent but its input offset is not committed. A checkpoint advances but an asynchronous object upload later fails. A state snapshot completes while a nontransactional side effect remains uncertain. The system recovers exactly as configured, yet the business sees a duplicate or omission.

The semantic choice affects availability, latency, throughput, storage, and operational complexity. Acknowledging before work reduces backlog and replay but accepts loss. Acknowledging after work preserves inputs but increases duplicates and retention demand. Coordinating progress with state or outputs can strengthen results, but adds protocol coupling, timeout interactions, fencing, and recovery paths.

Concurrency makes a scalar checkpoint deceptive. If offsets 10, 11, and 12 run in parallel and 12 finishes first, committing 13 claims the entire prefix through 12 is complete. A crash can permanently skip 10 and 11. Correct systems track holes, restrict concurrency within an order domain, or advance only the largest contiguous completion prefix.

Retries multiply load precisely when dependencies are degraded. A backlog plus short visibility timeout can make the same expensive record execute concurrently. Unbounded poison retries can hold an ordered partition forever. Aggressive dead-lettering can preserve throughput while silently violating completeness. Delivery design is capacity and governance design as much as message-client configuration.

Semantics also differ across products. Kafka consumers control stored next offsets and can couple them with application storage. Kinesis Client Library resumes from checkpoints and explicitly documents consumer-retry duplicates. Pub/Sub acknowledgement deadlines govern redelivery, while its exactly-once delivery option has pull and regional constraints. Pulsar Functions places acknowledgement at different nodes for its processing modes. Flink distinguishes replayed execution from exactly-once managed state and requires replayable sources plus transactional or idempotent sinks for end-to-end results. Preserve those scopes instead of translating every product term into one universal promise.

## Prerequisites and Retrieval

Retrieve the business obligation: required input set; allowed omissions, duplicates, delay, and reordering; effect identity; correction/reversal rules; consumer-visible completion; financial/safety/legal consequences; reconciliation source; and accountable owner.

Retrieve source facts: product/version; topic/stream/subscription generation; partition/shard/message coordinates; occurrence and producer-request identity; ordering contract; retention/expiry; replay/reset APIs; redelivery rules; maximum delivery attempts; acknowledgement deadline/lease; and cross-region behavior.

Retrieve consumer facts: group/subscription/application identity; member and ownership generation; client/framework/version; fetch/prefetch; batch size; concurrency; handler lifecycle; timeout/cancellation; acknowledgement mode; auto/manual commit; checkpoint representation; callback behavior; and shutdown/rebalance path.

Retrieve processing milestones: fetch; decode; schema validation; authorization; domain validation; state read/write; enrichment calls; transformation; output creation; sink request; durable acceptance; publication; checkpoint; ack; audit; and metric emission. For each, record whether it is durable, queryable, repeatable, reversible, and bound to input identity.

Retrieve state and checkpoint facts: next-position convention; per-partition or global vector; contiguous-prefix calculation; snapshot/checkpoint identifier; state schema/code/config version; storage durability; completion protocol; restore selection; retention; corruption detection; ownership fencing; and savepoint versus automatic recovery behavior.

Retrieve failure facts: process kill; host loss; pause; rebalance; stale owner; broker/coordinator outage; checkpoint-store outage; sink timeout; accepted-but-response-lost; partial batch; throttling; malformed data; schema outage; authorization expiry; dependency brownout; region loss; operator reset; deployment; and source retention expiry.

Retrieve retry policy: error classification; immediate or delayed retry; exponential backoff and jitter; per-attempt timeout; end-to-end deadline; maximum attempts/age; concurrent attempts; visibility/ack extension; circuit breaking; retry topic; quarantine; terminal disposition; and replay authorization.

Retrieve observable evidence: delivery attempts by occurrence ID; redelivery reason; fetched/processed/effect/checkpoint frontiers; uncommitted age; checkpoint duration/failure; restore position; duplicate/omission detector; poison age; retry amplification; quarantine counts; sink receipts; reconciliation differences; and user-visible publication.

Distinguish record from logical event; publish duplicate from redelivery; attempt from outcome; fetch from process; handler return from durable effect; ack request from accepted ack; offset from next offset; position from checkpoint; sparse completions from contiguous prefix; state snapshot from output commit; retry from replay; redelivery from reprocessing; dead letter from success; exactly-once delivery from exactly-once effect; framework-managed state from external state; ordering from delivery count; and low lag from correctness.

Create a delivery contract:

| Concern | Required decision and evidence |
|---|---|
| Scope | Source/subscription generation, interval, destination/observer, failures, exclusions |
| Identity | Source occurrence, producer request, delivery attempt, effect, batch, checkpoint |
| Milestones | Fetch, process, state, sink acceptance, publication, checkpoint, acknowledgement |
| Frontier | Next-position convention, contiguous completion, holes, multi-partition vector |
| Failure | Crash window outcome at every boundary, including unknown responses and stale owners |
| Retry | Classification, timeout, backoff/jitter, maximum attempts/age, concurrency and capacity |
| Poison | Quarantine schema, authorization, retention, replay, order/completeness consequence |
| Recovery | Source history, restore selection, state/offset compatibility, catch-up and replay margin |
| Composition | Guarantee and identity mapping across every connector, buffer, state store, and sink |
| Evidence | Fault matrix, attempt/outcome ledger, reconciliation, metrics, alerts and drill cadence |

Write a falsifiable claim: “For subscription generation `S` over cut `[a,b)`, after any tested single process/host/coordinator/sink-timeout failure while source history remains retained, every valid occurrence reaches the accepted output boundary at least once; checkpoint `C_p` for each partition is the next position after the largest contiguous accepted prefix; repeats preserve occurrence identity and are bounded/observable; invalid inputs enter governed quarantine; and no stronger claim is made for external effects outside that boundary.”

## Learning Objectives

After completing this module, you should be able to:

1. define delivery guarantees by identity, boundary, interval, and failure model;
2. distinguish at-most-once, at-least-once, exactly-once delivery, state, processing, and effects;
3. derive omission and replay windows from checkpoint/effect ordering;
4. compute safe contiguous checkpoints under batches and concurrent completion;
5. treat acknowledgement, commit, and output timeouts as ambiguous outcomes;
6. design bounded retries, leases, poison handling, quarantine, and replay controls;
7. align source positions with state snapshots and ownership generations;
8. assess whether guarantees compose across brokers, frameworks, connectors, and sinks;
9. instrument logical outcomes rather than trusting lag or attempt counts; and
10. construct fault-injection and reconciliation evidence for a delivery claim.

## Core Exposition

### Define the observation boundary

Start with the observer that matters. A broker can promise not to redeliver an acknowledged message, while the consumer may have called a payment API twice before that acknowledgement. A framework can restore managed state exactly once while a logging, email, or database side effect repeats. A connector can deliver to a database at least once while a downstream materialized view exposes only one current row because writes replace by key.

Draw a directed path from source occurrence to business observation. Label each buffer, ownership domain, transformation, state store, output log, connector, sink, and publication layer. For every edge, name the identity and durable acceptance evidence. Guarantees attach to those edges and nodes, not to the architecture diagram as a whole.

Use vocabulary such as “source-to-handler delivery,” “managed-state application,” “output-topic visibility,” and “customer-visible effect.” Avoid an unqualified “processing exactly once.” Handler code may execute repeatedly during deterministic replay even when restored state and transactional outputs reveal one result.

### Model milestones and crash windows

For one input, a typical path is fetch → decode → validate → compute → state update → sink request → sink acceptance → progress commit → acknowledgement. Some products merge ack and progress; others checkpoint a vector during a global snapshot. Some clients prefetch far ahead of handler completion.

Place a crash between every adjacent pair. Ask what survives, where recovery begins, and what the next owner can observe. If the checkpoint survives but a required effect does not, omission is possible. If the effect survives but the checkpoint does not, replay and duplicate effect are possible. If neither survives, replay is expected. If both are one committed recovery unit, recovery observes both or neither—subject to that unit's actual failure contract.

Also test uncertain responses. A timeout after a commit request is not evidence that the commit failed. Retrying may be harmless for a monotone same-value checkpoint, unsafe if an older asynchronous callback overwrites newer progress, or rejected after ownership changes. Record request identity and query authoritative state where supported.

### Understand at-most-once delivery

At-most-once puts the durable completion marker before work or declines replay after failure. It is appropriate only when missing an input is acceptable or another authoritative process repairs omissions. Telemetry sampling, replaceable cache warming, and high-frequency sensors whose next value supersedes the last may qualify; billing, inventory decrements, security alerts, and change-data capture usually do not without reconciliation.

The semantic does not mean every record is delivered once. It means zero or one delivery within the named scope. A crash after early acknowledgement and before processing yields zero. Source expiration, reset, authorization failure, or corrupted data can add other omission paths unless excluded or controlled.

Measure omission opportunities: acknowledgements ahead of effects, early-ack count, cancelled handlers after ack, expired source range, and comparison with an authoritative source. Document the product reason for preferring latency or duplicate avoidance over completeness.

### Understand at-least-once delivery

At-least-once delays progress until the declared work boundary completes and retains enough source history for recovery. A crash after work but before checkpoint replays a suffix. The same logical occurrence may execute multiple times, possibly concurrently if a lease expires while the old worker continues.

The guarantee requires more than retries. The source must still contain the record; the subscription must not expire; reset policy must not jump forward; poison handling must preserve a governed outcome; and retry exhaustion must not silently discard work. If a valid message can expire from the source before completion, “at least once” needs a bounded interval or a durable alternate store.

At-least-once delivery is often the honest transport baseline. Its operational cost is replay amplification. Capacity plans must include the number and expense of repeated records after the oldest recoverable checkpoint, plus live arrivals during catch-up.

### Treat product exactly-once delivery precisely

Some services provide a no-redelivery promise for a service-defined message identity after a successful acknowledgement. That materially reduces duplicate delivery, but the scope matters. Google Pub/Sub's current exactly-once delivery documentation limits the feature to pull/StreamingPull subscriptions within a cloud region, makes acknowledgement success observable through supported interfaces, and notes that separate publish-side duplicates can still exist.

This is stronger than ordinary at-least-once delivery between Pub/Sub and the subscriber. It is not automatically an atomic transaction with a database or external API. If the effect succeeds and the acknowledgement remains uncertain or occurs later, application progress is still needed to avoid repeating the effect. If a publisher creates two distinct messages, a subscriber-level delivery feature does not merge them.

Preserve vendor terminology in inventories. Record product/version, subscription type, region/endpoints, client capability, message-ID scope, acknowledgement response behavior, lease/deadline rules, quotas, latency effects, and excluded publisher or downstream boundaries.

### Advance only a contiguous checkpoint

For a partition, let $D$ be the set of next positions whose preceding records have completed the required boundary. The safe scalar checkpoint is the smallest unfinished position, equivalently one after the largest contiguous completed prefix. Completion of a higher offset cannot bridge a lower hole.

Suppose next offset is 20 and workers finish records 20, 22, and 23 while 21 is still running. The safe checkpoint is 21, not 24. If 21 later succeeds, the checkpoint may advance through 24. A tracker can maintain a base frontier plus a bounded set/bitmap of out-of-order completions. It must clear or version that structure on reassignment.

If strict partition order is a business invariant, do not parallelize records from that partition at all. If operations commute and concurrent completion is allowed, still preserve a contiguous recovery frontier or use a framework whose snapshot algorithm accounts for in-flight work.

### Make batch semantics explicit

Fetch batches, processing batches, sink batches, and checkpoint batches need not align. A client may return 500 records across several partitions; the application may create 50-item database writes; the checkpoint may be per partition; and a remote batch API may partially accept items.

For every batch API, define atomicity and item-level receipts. “Request succeeded” may mean all items, while “request failed” may conceal partial acceptance. Retry only failed items when authoritative results exist. Otherwise reuse stable effect identities and reconcile. Never commit a partition's batch end solely because a multi-partition call returned generally successful.

Kafka's consumer API documents committed offsets as the next message to consume. A manual consumer should commit each partition's next completed offset, not the last processed offset and not a global maximum. Automatic commits provide at-least-once only under the documented requirement that all records returned by a poll are consumed before a later poll or close; otherwise committed progress can get ahead and records can be missed.

### Align acknowledgement deadlines and work

Queue-style services often grant a time-bounded delivery lease. If processing exceeds the acknowledgement deadline, the message becomes eligible for redelivery. Clients may extend the deadline, but lease extension is a liveness mechanism, not proof that effects are safe or progress is occurring.

Choose initial deadline and extension policy from processing-time distributions, dependency timeouts, pause behavior, and failover objectives. Too short causes duplicate concurrent work. Too long delays retry after a dead worker. Bound total extension so poison or wedged work eventually moves to a controlled disposition.

Track current attempt, lease expiry, extensions, processing age, and ownership token. If an old acknowledgement ID or token expires, do not assume a late ack applies to the newest delivery. Product APIs may reject stale acknowledgement identities specifically to prevent that ambiguity.

### Classify retries and poison inputs

Transient failures include throttling, short dependency unavailability, and retryable transport errors. Permanent failures include schema incompatibility under current code, invalid business data, denied authority, and destinations that no longer exist. Misclassification either drops recoverable work or creates a retry storm.

Define a retry budget in attempts and wall-clock age. Use exponential backoff with jitter, but ensure the delay plus processing fits retention and freshness objectives. Apply admission and concurrency limits so retries do not starve new traffic or overwhelm a recovering dependency.

A poison path should preserve source identity, raw or protected payload reference, schema, code/config generation, first/last failure, attempt history, error class, owner, legal classification, and intended repair/replay action. Quarantine is a distinct accepted outcome only if the delivery contract says so. Otherwise moving a record there breaks the primary completeness claim.

### Separate producer duplicates from redelivery

A producer may time out after an accepted publish and send another record. The two source records can have distinct broker positions and even distinct broker message IDs. Consumer redelivery repeats one accepted source record. These need different evidence and often different deduplication keys.

Carry an occurrence or command identity assigned before the uncertain publish attempt. Preserve broker coordinates and delivery-attempt identity separately. Metrics should distinguish repeated delivery of one source coordinate, multiple source coordinates with one occurrence key, and legitimately repeated business events.

AWS documents both paths for Kinesis Data Streams: uncertain producer retries can create two records with unique sequence numbers, and consumer restart resumes after the last checkpoint, replaying records processed since it. Treating both as one “duplicate count” hides the responsible boundary.

### Coordinate state snapshots and source positions

Stateful frameworks often checkpoint operator state and source positions together. A consistent snapshot represents state after all inputs before its barriers and none after. Recovery restores that state and rewinds sources to matching positions. Independently selecting the newest state snapshot and newest source offsets can omit updates; selecting older state with newer offsets can also omit, while newer state with older offsets can double-apply.

Flink's current documentation explicitly distinguishes exactly-once managed-state updates from executing every event once. Recovery rewinds and replays source data. Its end-to-end statement requires replayable sources and transactional or idempotent sinks. Connector capabilities still determine the actual source and sink boundary.

Record checkpoint ID, source-position vector, state handles/digests, code/savepoint schema, completion status, external commit handles, and restore attempt. Only completed compatible checkpoints are eligible. Test loss during snapshot creation, storage finalization, coordinator acknowledgement, and restore.

### Respect ownership and stale consumers

DE-054 showed that a consumer can lose ownership without a graceful callback. A stale process may finish an old batch and attempt to commit after a new owner has advanced progress. Progress storage must enforce current assignment/generation where the platform provides it, or application storage must use conditional tokens.

On planned revocation, stop admission, drain bounded work, record per-partition contiguous frontiers, and commit only while authority remains. On loss, do not make an unsafe final progress claim. Candidate completions from the old generation require rejection or reconciliation.

An at-least-once contract must include concurrent-attempt behavior during lease transfer. Two executions do not necessarily violate at-least-once delivery, but they can violate external invariants unless DE-056's effect mechanisms fence or deduplicate them.

### Compose stage guarantees conservatively

Consider source → transformation → output topic → connector → database → materialized API. Each edge has its own acknowledgement, retention, identity, and failure behavior. An at-least-once first edge plus an at-most-once connector does not produce end-to-end at-least-once. An exactly-once state snapshot plus a non-idempotent external call does not produce exactly-once effects.

Composition also fails when identity changes. If a connector republishes without the original occurrence ID, downstream systems cannot recognize replay. If one event becomes many records, define child identities and completion: does the parent complete when all children are accepted, any child, or a durable manifest is published? If many inputs aggregate to one output, define the input cut covered by that output.

Build a guarantee matrix by stage. For each, list input identity, accepted output, ack/checkpoint, replay source, retry behavior, retention, ordering, state, and failure exclusions. The end-to-end claim is the strongest property proved across every row—not the strongest product setting present anywhere.

### Govern resets, replays, and backfills

Offset resets and seek operations redefine future delivery. A forward reset can omit obligations; a backward reset can repeat them. Treat both as production data changes with authorization, exact cut, reason, impact preview, output isolation, checkpoint/state compatibility, approval, audit, abort, and reconciliation.

Prefer an isolated recovery subscription/group and output generation for investigation or recomputation. It preserves live progress and makes comparison possible. Publishing repaired results requires a separate conditional procedure; merely replaying is not proof that missing or duplicate effects were corrected.

Retain source history, schemas, code/artifacts, state snapshots, keys, credentials, and dependencies for the promised recovery horizon. A 24-hour log is not a seven-day replay guarantee. Include worst incident detection, decision, repair, restore, and catch-up time plus variance.

### Observe logical outcomes

Monitor fetched, decoded, accepted, retried, quarantined, and acknowledged counts by stable source identity and reason. Track per-partition fetched, contiguous processed, effect, and checkpoint frontiers; checkpoint age/duration/failure; oldest uncommitted input; delivery attempts; lease extensions/expiry; retry amplification; poison age; source retention margin; and restore/catch-up.

Lag measures source position distance, not required effects. Zero lag can coexist with early checkpoints and missing outputs. High delivery-attempt count can be harmless if effects deduplicate; one attempt can still omit an effect if acknowledged early. Reconciliation compares authoritative input cuts with accepted business outcomes.

Alert on semantic risk: checkpoint ahead of effects, frontier regression, increasing holes, stale-generation commit attempts, expired history, acknowledgement failures, duplicate occurrence identities, retry-budget exhaustion, quarantine without owner, and unexplained source-to-output count/key differences.

### Test the recovery protocol

Construct a milestone fault matrix. Kill the process after fetch, after state mutation, during sink request, after sink acceptance, before checkpoint, during checkpoint, after checkpoint, during acknowledgement, after acknowledgement, and during revocation. Add response loss, partial batch acceptance, long pause, lease expiry, stale owner, checkpoint-store outage, retention expiry, schema error, authorization failure, and regional failover where claimed.

For each injection, capture input coordinate/occurrence, attempts, accepted state/effects, checkpoint before/after, restore start, quarantine, and visible result. Compare with the promised omission and duplication bounds. Repeat at boundary offsets, empty/nonempty batches, maximum batch size, multiple partitions, and concurrent completions.

A test harness that counts handler invocations cannot establish exactly-once state or effects. Query durable state and sink receipts, then reconcile the full finite input cut. Preserve artifacts so a later client, broker, framework, or configuration change can rerun the same proof obligations.

### Review the complete semantics argument

A defensible design connects fourteen claims: the business observation is named; source identities and retained cut are complete; milestones are explicit; acknowledgement/checkpoint convention is correct; only contiguous progress advances; crash windows yield documented replay or omission; ambiguous outcomes are tolerated; batches preserve item/partition results; retries are bounded; poison disposition is governed; state and positions restore together; ownership fences stale progress; stage identities/guarantees compose; and fault/reconciliation evidence covers the declared failure model.

Any missing link weakens the result. A product checkbox cannot repair an undefined effect identity. A durable checkpoint cannot recover expired source history. Idempotent output cannot fix a forward reset that skipped input. A passing happy-path test cannot cover the crash window it never enters.

## Definitions and Notation

For partition $p$, use monotonically ordered source positions. Let positions denote the next record, so interval $[a,b)$ contains records $a$ through $b-1$.

- $F_p$: fetched frontier, the next position after records returned to the application.
- $P_p$: largest contiguous processed frontier under the handler's declared completion rule.
- $E_p$: largest contiguous frontier with required effects durably accepted.
- $C_p$: durable checkpoint from which recovery resumes.
- $H_p$: earliest retained source position; positions below it are no longer replayable.
- $L_p$: current source end position for the chosen isolation/visibility rule.
- $D_p$: set of completed positions above the current contiguous frontier, representing holes.
- $g$: current consumer ownership generation or lease token.
- $x$: logical occurrence identity assigned independently of delivery attempt.
- $a_i(x)$: delivery attempt $i$ for occurrence $x$.
- $e(x)$: required effect identity or outcome for $x$.
- $t_{ack}$: time acknowledgement/progress becomes authoritatively durable.
- $t_{effect}$: time the named effect becomes authoritatively durable.
- $R_p=[C_p,F_p)$: conservative potential replay interval after a crash.
- $U_p=[E_p,C_p)$ when $C_p>E_p$: potential omission interval caused by early progress.
- $Q$: governed quarantine set.

For an after-effect checkpoint policy, a useful invariant is

$$
H_p \le C_p \le E_p \le P_p \le F_p \le L_p.
$$

The inequality is a modeling discipline, not a platform theorem. Some pipelines do not have a distinct effect frontier; some stateful frameworks capture $C$ and state together; some queue services track individual messages rather than a scalar prefix. Map the model to the product instead of forcing incompatible coordinates.

Potential replay records are

$$
N_{replay,p}=F_p-C_p,
$$

while records that may repeat an already accepted effect are

$$
N_{dup,p}=\max(0,E_p-C_p).
$$

If progress is early, potential omission is

$$
N_{omit,p}=\max(0,C_p-E_p).
$$

These are upper-bound counts for one known frontier snapshot. Actual recovery can fetch fewer records, and effects may be idempotent or transactional. The formulas do not count producer duplicates or prove outcomes.

Let checkpoint interval be $I$, input rate be $\lambda$, and replay processing cost per input be $w$. A rough steady-rate replay work estimate is $\lambda Iw$, but batch size, barrier duration, state restoration, skew, downtime, live traffic, and last-checkpoint failure add variance. Measure distributions rather than choosing $I$ from the mean.

For retry attempt timeout $d_i$, backoff $b_i$, and processing time $s_i$, a bounded retry age is

$$
T_{retry}=\sum_{i=1}^{n}(d_i+s_i)+\sum_{i=1}^{n-1}b_i.
$$

Require $T_{retry}$ plus detection, restore, and catch-up to fit source retention and business freshness, or define a durable alternate outcome.

Delivery guarantees can be described as allowed cardinalities of service presentations $A(x)$ for a source occurrence $x$ under a failure model:

$$
\text{at-most-once}: |A(x)|\in\{0,1\},\qquad
\text{at-least-once}: |A(x)|\ge1.
$$

Exactly one presentation would require $|A(x)|=1$, but vendor promises add scope, successful-ack, subscription, regional, and identity conditions. Neither formula constrains $|e(x)|$ unless the effect boundary is part of the protocol.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. **Name the obligation.** Define the finite input cut and business observation, including allowed quarantine or expiration.
2. **Bind identity.** Map occurrence, source coordinate, attempt, checkpoint, child output, effect, and ownership generation.
3. **Draw milestones.** Mark every durable and nondurable step from fetch through visibility.
4. **Enumerate failures.** Insert crash, timeout, response loss, partial success, reassignment, and operator action between milestones.
5. **Compute recovery.** For each failure, identify restored state, start position, replay, omission, uncertain effects, and authority.
6. **Protect the frontier.** Advance only the next position after a contiguous accepted prefix; reject stale generations and regression.
7. **Preserve replay.** Retain inputs and compatible state/code/config for the entire recovery and retry horizon.
8. **Bound retries.** Classify errors, limit attempts/age/concurrency, protect dependencies, and govern terminal disposition.
9. **Compose stages.** Verify identity and acceptance mapping across every output, connector, state store, and sink.
10. **Test and reconcile.** Inject each failure and compare the finite input cut with durable outcomes.

The core safety invariant for an at-least-once effect boundary is:

> No durable checkpoint advances beyond the largest contiguous prefix whose required effect boundary is authoritatively accepted under the current ownership generation.

The corresponding liveness condition is:

> Every valid uncheckpointed occurrence is eventually accepted at the required boundary or moved to an explicitly permitted, durable, owned terminal disposition while replay history remains available.

Safety without liveness retries forever. Liveness without safety can skip work. Both require operational assumptions: available source history, recoverable checkpoint storage, bounded poison handling, capacity, dependency recovery, authentic identities, and authorized ownership.

The following executable exposes three crash windows over the same finite input cut. It models integer frontiers and effect sets, not a broker, database, transaction coordinator, or distributed failure detector.

<!-- bijux-verify: {"id":"delivery-crash-windows","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input_cut=(100, 101, 102, 103, 104)\nat_most_checkpoint=103\nat_most_effects=(100, 101)\nat_most_omitted=(102,)\nat_least_checkpoint=102\nat_least_effects_before_crash=(100, 101, 102)\nat_least_replay=(102, 103, 104)\nat_least_duplicate_candidates=(102,)\natomic_checkpoint=103\natomic_effects=(100, 101, 102)\natomic_restart=(103, 104)\natomic_omitted=()\natomic_duplicate_candidates=()\nfrontier_invariant=True\n","stderr":""}} -->
```python
input_cut = tuple(range(100, 105))
crash_record = 102

# Early progress survives, but the effect for record 102 does not.
at_most_checkpoint = crash_record + 1
at_most_effects = tuple(range(100, crash_record))
at_most_omitted = tuple(
    offset
    for offset in input_cut
    if offset < at_most_checkpoint and offset not in at_most_effects
)

# The effect survives, but progress still points to record 102.
at_least_checkpoint = crash_record
at_least_effects = tuple(range(100, crash_record + 1))
at_least_replay = tuple(
    offset for offset in input_cut if offset >= at_least_checkpoint
)
at_least_duplicates = tuple(
    offset for offset in at_least_replay if offset in at_least_effects
)

# One recovery unit contains effect 102 and next position 103.
atomic_checkpoint = crash_record + 1
atomic_effects = tuple(range(100, crash_record + 1))
atomic_restart = tuple(
    offset for offset in input_cut if offset >= atomic_checkpoint
)
atomic_omitted = tuple(
    offset
    for offset in input_cut
    if offset < atomic_checkpoint and offset not in atomic_effects
)
atomic_duplicates = tuple(
    offset for offset in atomic_restart if offset in atomic_effects
)

print(f"input_cut={input_cut}")
print(f"at_most_checkpoint={at_most_checkpoint}")
print(f"at_most_effects={at_most_effects}")
print(f"at_most_omitted={at_most_omitted}")
print(f"at_least_checkpoint={at_least_checkpoint}")
print(f"at_least_effects_before_crash={at_least_effects}")
print(f"at_least_replay={at_least_replay}")
print(f"at_least_duplicate_candidates={at_least_duplicates}")
print(f"atomic_checkpoint={atomic_checkpoint}")
print(f"atomic_effects={atomic_effects}")
print(f"atomic_restart={atomic_restart}")
print(f"atomic_omitted={atomic_omitted}")
print(f"atomic_duplicate_candidates={atomic_duplicates}")
print(f"frontier_invariant={at_least_checkpoint <= len(at_least_effects) + 100}")
```

The atomic case is an assumption in this arithmetic. Its implementation and proof obligations depend on the state/output system and are the subject of DE-056.

## Alternatives and Trade-Offs

**Early versus late acknowledgement.** Early ack reduces redelivery and backlog but accepts omission between ack and work. Late ack protects completeness while repeating work after crash. Choose from business loss/duplicate costs and repair capability.

**Automatic versus manual progress.** Automatic commit is simple and can be safe when processing is synchronous within the client's documented poll contract. Manual progress can align more precisely with work, but off-by-one offsets, concurrent holes, async callback reordering, and stale ownership become application responsibilities.

**Per-record versus batched checkpoints.** Per-record progress narrows replay but increases coordination/storage cost. Batching improves throughput but enlarges replay and duplicate candidates. Size from recovery cost and retention/freshness, not throughput alone.

**Serial versus concurrent partition processing.** Serial handling naturally preserves a contiguous frontier and order but caps throughput. Concurrent handling can exploit commuting work, yet needs hole tracking, bounded memory, cancellation, and safe reassignment.

**Short versus long acknowledgement deadline.** Short deadlines detect dead workers quickly but cause redelivery during legitimate slow work. Long deadlines reduce duplicates but delay failover. Adaptive extension needs caps and progress monitoring.

**Inline retry versus retry topic/queue.** Inline retry preserves order but blocks following work and can cause partition starvation. Delayed retry isolates failures and schedules backoff, but changes order, identity mapping, retention, and completion semantics.

**Stop on poison versus quarantine.** Stop preserves strict prefix completeness and ordering but can halt a large domain. Quarantine restores flow but must be an authorized semantic outcome with repair and replay; otherwise it is disguised loss.

**Replay from source versus persist intermediate outputs.** Source replay simplifies lineage when transformation is deterministic and dependencies remain reproducible. Durable intermediate results reduce recomputation and nondeterminism but add storage, versioning, privacy, and consistency boundaries.

**Broker checkpoint versus external checkpoint.** Broker-managed progress integrates with group tooling and ownership. External progress can align atomically with application state/effects but needs its own fencing, backup, monitoring, and reset tooling. Two independent progress authorities invite divergence.

**Stateful framework versus bespoke consumer.** A framework can coordinate barriers, state, and source positions, reducing protocol code. Connector limits and external effects remain; operational complexity shifts to checkpoint storage, state compatibility, and restore performance.

**Product exactly-once delivery versus application deduplication.** A service feature can suppress redelivery in its documented scope and expose ack success. Application identity can span producer duplicates and downstream effects, but requires storage and lifecycle rules. They solve overlapping, not identical, problems.

**Long retention versus archival replay.** Long hot retention simplifies immediate recovery but costs storage. Archive lowers cost and supports long horizons, yet restore speed, coordinate mapping, schema/code availability, and ordering must be tested.

## Failure Modes and Misconceptions

**“At least once means the handler runs at least once.”** It applies only under named retention, terminal-disposition, and failure assumptions. Expiry or a forward reset can still omit work.

**“At most once means once.”** Zero deliveries are allowed. Early acknowledgement deliberately creates a loss window.

**“Exactly-once delivery means exactly-once payment.”** Delivery to a subscriber and an external business effect are different boundaries.

**“Processed means returned from poll.”** Fetch advances an in-memory position; application validation, state, outputs, and durable progress may not have happened.

**“Commit offset 42 after record 42.”** Kafka-style committed offsets denote the next record, so after 42 the value is 43. Product conventions must be explicit.

**“Commit the maximum finished offset.”** A lower in-flight hole can be skipped. Advance only through a contiguous accepted prefix.

**“A successful send response means the whole batch succeeded.”** Some APIs expose partial item results; timeouts may hide partial acceptance. Inspect authoritative per-item semantics.

**“A failed acknowledgement means it was not accepted.”** The response can be lost after acceptance. Treat it as uncertain unless the product proves otherwise.

**“Redelivery is the only duplicate source.”** Producer retries can create distinct source records for one logical occurrence; repair jobs and connectors can republish too.

**“The broker deduplicates my application retry.”** Deduplication scope may depend on producer session, sequence, time window, or message ID. A new publish identity may bypass it.

**“Retries guarantee completion.”** Unbounded retries can exceed retention, freshness, and capacity, while permanent failures never succeed.

**“Dead-letter means delivered.”** It is an alternate outcome. Whether it satisfies the obligation must be declared and governed.

**“A long ack deadline prevents duplicates.”** A process can outlive its lease or lose authority; publisher duplicates and operator replays remain.

**“Checkpoint every five seconds means five seconds of replay.”** Checkpoint duration/failure, rates, batches, state, downtime, and restore/catch-up expand the window.

**“Exactly-once managed state means code executes once.”** Replay may re-execute records while restored state reflects one application.

**“Every connector inherits the framework guarantee.”** Source and sink connectors have their own capabilities and configuration.

**“Zero lag proves no loss.”** An early checkpoint can create zero lag while required effects are missing.

**“Quarantine every error to protect throughput.”** Authorization or dependency outages can mass-quarantine valid data and destroy freshness/completeness.

**“Replay in production is reversible.”** Repeated external effects may be irreversible. Isolate, preview, fence, and reconcile.

**“One guarantee applies across regions forever.”** Regional endpoints, failover, subscription replication, and retention can narrow the claim.

## Worked Examples

### Example 1

A telemetry sampler acknowledges each reading before feature extraction. A host crash loses 37 acknowledged readings, but the next readings supersede them and the product contract permits bounded sampling loss. The team measures early-ack omissions and does not reuse this design for security alarms.

### Example 2

A Kafka consumer inserts offsets 700–799 into a warehouse, then crashes before committing next offset 800. Recovery begins at 700 and repeats the inserts. The transport path is at least once. Stable occurrence keys or a coupled effect/progress mechanism are needed if duplicate rows are unacceptable.

### Example 3

Offsets 50–53 execute concurrently. Results for 50, 52, and 53 are durable while 51 waits on a dependency. The completion tracker holds checkpoint 51 and records holes 52/53. When 51 succeeds it advances the next offset to 54. Committing 54 earlier would permit omission of 51.

### Example 4

A Pub/Sub pull subscriber processes for 90 seconds but its acknowledgement lease expires after 60. Another worker receives the same message. The old ack identity is no longer current under the documented exactly-once delivery behavior. Both workers' external requests still need an effect identity and fencing/deduplication beyond subscriber delivery.

### Example 5

A Kinesis processor writes records 10,001–20,000 to an object and fails before checkpoint. KCL resumes from the last successful checkpoint and repeats the range, matching AWS's documented consumer-retry pattern. A deterministic object name derived from shard and first sequence can make repeats converge, but that is a sink effect design.

### Example 6

A 100-item destination batch returns 97 successes, two retryable throttles, and one permanent validation error. The application records item receipts, retries only the two with stable identities, quarantines the invalid item under policy, and advances each partition only through its accepted contiguous prefix.

### Example 7

A Flink job restores checkpoint 812. Source positions and managed aggregation state return together; records after its barriers replay. The managed state remains exactly-once under the framework assumptions, while a custom HTTP call issued outside a coordinated sink can repeat. The runbook states both scopes.

### Example 8

A schema registry outage is misclassified as malformed input. Thousands of valid records enter quarantine, lag falls, and dashboards look healthy. Reconciliation finds missing outputs. The corrected classifier treats dependency unavailability as transient, rate-limits retries, and alerts on quarantine-rate shifts.

### Example 9

An operator resets a live group forward by one million offsets to clear lag. No application errors occur, but the skipped interval never affects the materialization. Reset tooling now requires an exact cut preview, protected approval, isolated repair output, and post-action source-to-effect reconciliation.

### Example 10

An ingestion path claims at least once from topic to database. Its first consumer is at least once, but an intermediate connector acknowledges output records before asynchronous database writes complete. Crash testing exposes omissions. The end-to-end claim is weakened until the connector boundary changes and the cut is reconciled.

## Cross-Program Connections

Distributed systems contributes failure models, partial synchrony, leases, fencing, atomic commit, consensus, and the two-generals-style uncertainty of lost responses. Delivery semantics are protocols under incomplete knowledge.

Database systems contributes transactions, write-ahead logging, atomic commit, MVCC, constraints, idempotent upsert, isolation, recovery, and reconciliation. Progress and effect boundaries often meet in a database.

Operating systems contributes process crashes, buffered I/O, `fsync`, signals, cancellation, scheduling pauses, thread pools, and graceful shutdown. “The handler returned” is not necessarily durable.

Networking contributes timeouts, retransmission, duplicated packets, partitions, backpressure, connection reset, and ambiguous request outcomes. Remote calls cannot infer acceptance solely from response absence.

Algorithms contributes prefix scans, interval arithmetic, sparse-hole tracking, exponential backoff, jitter, queueing, and amortized checkpoint cost.

Formal methods contributes safety/liveness separation, state-machine refinement, temporal properties, linearization points, counterexamples, and model checking around crash windows.

Site reliability engineering contributes failure injection, recovery objectives, retry budgets, capacity headroom, retention margin, observability, incident response, and reconciliation drills.

Security engineering contributes authentic message identity, authorization for ack/reset/replay, integrity of checkpoints/quarantine, tenant isolation, audit, and denial-of-service controls on poison/retry paths.

Platform engineering contributes deployment drains, disruption budgets, regional placement, client/version policy, managed checkpoint storage, secret rotation, and guarded self-service replay tools.

API and service engineering contributes idempotency keys, conditional requests, retryable error taxonomies, deadlines, request receipts, and pagination/cursor semantics at downstream effects.

Control theory contributes feedback delay and retry amplification. Backoff, circuit breaking, and autoscaling can stabilize or destabilize a recovering pipeline.

Software testing contributes deterministic fault points, finite-cut oracles, property tests, metamorphic replay checks, and durable evidence artifacts.

## References

1. Apache Kafka. [KafkaConsumer API, Apache Kafka 4.3](https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html). Accessed 2026-09-03. Primary client documentation for fetched versus committed position, automatic/manual commits, next-offset convention, at-least-once replay, and external offset storage.
2. Apache Kafka. [Consumer Configuration, Apache Kafka 4.3](https://kafka.apache.org/43/generated/consumer_config.html). Accessed 2026-09-03. Primary configuration reference for automatic commits, acknowledgement-related timing, offset reset, polling, and transactional read isolation.
3. Apache Kafka. [Distribution: Consumer Offset Tracking, Apache Kafka 4.3](https://kafka.apache.org/43/implementation/distribution/). Accessed 2026-09-03. Primary implementation documentation for group coordinators, durable offset commits, replication acknowledgement, retry, and offset lookup.
4. Apache Flink. [Fault Tolerance](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/). Accessed 2026-09-03. Primary documentation for source-position/state snapshots, replay, at-most/at-least/exactly-once managed state, and end-to-end prerequisites.
5. Apache Flink. [Fault Tolerance Guarantees of Data Sources and Sinks](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/guarantees/). Accessed 2026-09-03. Primary connector matrix distinguishing state guarantees from end-to-end source/sink capabilities.
6. Apache Pulsar. [Pulsar Functions Concepts](https://pulsar.apache.org/docs/4.2.x/functions-concepts/). Accessed 2026-09-03. Primary documentation for Functions acknowledgement timing and at-most-once, at-least-once, effectively-once, and manual modes.
7. Apache Pulsar. [Pulsar Connector Overview](https://pulsar.apache.org/docs/4.2.x/io-overview/). Accessed 2026-09-03. Primary connector documentation stating processing guarantees depend on external sink implementation and idempotent retry behavior.
8. Amazon Web Services. [Use Kinesis Client Library](https://docs.aws.amazon.com/streams/latest/dev/kcl.html). Accessed 2026-09-03. Primary documentation for KCL checkpointing, restart, fault tolerance, and at-least-once delivery.
9. Amazon Web Services. [Handle Duplicate Records in Kinesis Data Streams](https://docs.aws.amazon.com/streams/latest/dev/kinesis-record-processor-duplicates.html). Accessed 2026-09-03. Primary documentation distinguishing producer-retry duplicates from consumer-retry replay after the last checkpoint.
10. Google Cloud. [Pub/Sub Service Overview](https://cloud.google.com/pubsub/docs/pubsub-basics). Accessed 2026-09-03. Primary documentation for acknowledged/unacknowledged messages, acknowledgement deadlines, redelivery, retention, and subscription delivery patterns.
11. Google Cloud. [Exactly-Once Delivery for Pub/Sub](https://cloud.google.com/pubsub/docs/exactly-once-delivery). Accessed 2026-09-03. Primary documentation for acknowledgement results, redelivery versus duplicate terminology, pull-only and regional scope, lease extension, and publisher-duplicate exclusions.

## Exercises

### Exercise 1

A partition's next checkpoint is 400. The consumer fetches through 419 and has durably accepted effects through 411, expressed as next frontier 412. Compute the potential replay interval/count and duplicate-effect candidate interval/count after a crash. Then analyze an erroneous early checkpoint of 416.

### Exercise 2

Offsets 30–36 execute concurrently. Records 30, 31, 33, 34, and 36 complete; 32 and 35 remain in flight. Starting from checkpoint 30, compute the safe next checkpoint and hole set. Recompute after 32 completes, then after 35 completes. Explain the ownership data needed across rebalance.

### Exercise 3

A retry policy allows four attempts. Each attempt has a 12-second request timeout and 3 seconds of local work. Backoffs are 2, 4, and 8 seconds. Detection/restore takes 45 seconds and catch-up takes 70 seconds. Compute the retry age and total simple recovery horizon. Assess a 3-minute freshness objective and 5-minute source-retention margin.

### Exercise 4

Design delivery semantics for a 200-item multi-partition batch sent to a destination that can partially accept items but may time out before returning its per-item response. Include identities, authoritative receipts, contiguous frontiers, retry classification, poison handling, ownership loss, capacity, and reconciliation.

### Exercise 5

Audit the claim “exactly once from Pub/Sub through a Flink job into an external database.” Define every boundary and failure model, identify which current product guarantees are relevant, list missing evidence, and write a narrower falsifiable claim that can be tested without presuming exactly-once database effects.

## Answers to the Exercises

### Answer 1

With $C=400$, $F=420$, and $E=412$, potential replay is `[400,420)`, 20 records. Already accepted effects inside it are `[400,412)`, so up to 12 effect candidates may repeat; whether they produce duplicates depends on the sink protocol. If an early checkpoint advances to 416 while effects remain at 412, recovery starts at 416 and `[412,416)`—four records—may be omitted. The later checkpoint reduces replay to `[416,420)` but violates the conservative $C\le E$ invariant. These counts assume contiguous known frontiers and do not include producer duplicates.

### Answer 2

From 30, completion is contiguous through record 31, so the safe next checkpoint is 32. The completed-above-frontier hole set is `{33,34,36}` while unfinished records are 32 and 35. After 32 completes, the contiguous prefix extends through 34, so checkpoint becomes 35 and the remembered higher completion is `{36}`. After 35 completes, completion extends through 36 and checkpoint becomes 37 with no holes. Across rebalance, either drain before handoff or durably bind base frontier, hole evidence if the framework supports it, input/effect receipts, state/checkpoint ID, old/new ownership generation, and cancellation outcome. A stale owner must not commit its late completions; simplest recovery replays from the last durable contiguous frontier.

### Answer 3

Attempt work is $4(12+3)=60$ seconds. Backoff totals $2+4+8=14$, so $T_{retry}=74$ seconds. Adding 45 seconds of detection/restore and 70 of catch-up yields 189 seconds. That exceeds a 180-second freshness objective by 9 seconds. It remains inside a 300-second retention margin by 111 seconds under the simple deterministic calculation. The retention margin must also cover incident variance, live arrivals, checkpoint age, throttling, and restore failure, so measure percentiles and add headroom. Reduce per-attempt timeout where safe, classify errors earlier, parallelize only independent work, improve restore/catch-up, or increase retention; do not merely delete retries needed for completeness.

### Answer 4

Assign every source occurrence a stable ID before the destination call and each destination effect a stable item ID; retain source partition/offset, batch request ID, attempt ID, and ownership generation separately. Query or record authoritative per-item receipts because a timeout can hide partial acceptance. Retry only confirmed-unaccepted/retryable items when possible; otherwise resend with stable effect identities and reconcile. Track accepted items per partition and advance each checkpoint only through its contiguous accepted prefix, never the overall maximum or batch end. Classify validation/authorization versus throttling/transport failures; bound attempts, age, backoff, and concurrency. Quarantine permanent invalid items only under an explicit completeness policy with protected payload reference, error evidence, owner, and replay controls. On ownership loss, cancel work and reject late progress from the stale generation. Capacity includes duplicate attempts and receipt queries. Reconcile the finite input cut against destination receipts and quarantine before declaring the batch complete.

### Answer 5

Separate publisher→Pub/Sub accepted message, Pub/Sub subscription→subscriber delivery, source→Flink checkpointed state, Flink→database request, database durable effect, and database→user visibility. Pub/Sub exactly-once delivery is relevant only for a supported pull/StreamingPull subscription, documented message-ID and acknowledgement behavior, regional connection scope, and successful ack; distinct publisher duplicates remain possible. Flink can restore matching source positions and managed state, but its own documentation requires a replayable source and transactional or idempotent sink for end-to-end exactly-once results. Evidence is needed for connector versions/configuration, subscription endpoints, ack integration with checkpoints, occurrence identity, database transaction/idempotency semantics, partial/unknown writes, checkpoint commit protocol, state compatibility, ownership fencing, retention, failover, and reconciliation. A narrower claim is: “For subscription generation `S` and finite cut `[a,b)`, under tested worker/checkpoint failures within retained history, every source message accepted by the Flink source contributes at least once to a database request with stable occurrence identity; managed Flink state restores from matching source positions; repeats and uncertain writes are measured and reconciled; no exactly-once database-effect claim is made until its transaction/idempotency protocol is separately proved.”
