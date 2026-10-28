---
module_id: API-067
program: API & Service Engineering
level: 2
module_number: 67
title: Idempotent Consumers
status: complete
last_verified: 2026-09-02
---

# Idempotent Consumers

## One-Page Review

### Governing question

How can a consumer accept duplicates, retries, replays, concurrent deliveries, and uncertain external outcomes while making each logical message produce no additional unintended effect after its first accepted execution?

### Essential definitions

- An operation is **idempotent** when applying it repeatedly has the same intended state effect as applying it once.
- A **logical message identity** names the fact or command across all delivery attempts; a delivery or invocation ID names only one attempt.
- A **consumer scope** distinguishes independent handlers, projections, tenants, and semantic versions that may each legitimately process the same message.
- An **inbox** is durable consumer-owned state recording acceptance, processing state, fingerprint, and outcome for a scoped message identity.
- A **fingerprint** is a canonical digest of immutable semantic inputs used to detect reuse of one identity for different content.
- An **effect identity** names one downstream side effect, such as a charge or notification, independently of transport attempts.
- The **deduplication horizon** is the period and replay domain for which prior identities and outcomes remain available.
- **Natural idempotency** comes from the state transition itself; **constructed idempotency** adds uniqueness, versions, ledgers, or outcome recovery.

### Central model, mechanism, or theorem

For consumer scope $c$, logical message $m$, immutable fingerprint $f$, and intended state/effects $S$, require

$$
Apply(c,m,f,Apply(c,m,f,S))=Apply(c,m,f,S).
$$

An atomic unique claim on $(c,m)$ chooses one owner/outcome. A later attempt with the same $f$ returns or resumes that outcome; a different $f$ is an identity conflict, never a harmless duplicate. Local state, inbox status, and outgoing outbox records commit together. External effects use separately stable effect IDs and queryable outcome state.

### Critical invariants

Message IDs remain stable across retry, broker redelivery, replay, bridge, and region recovery. Deduplication keys include the correct consumer/tenant/operation scope. The first durable claim is enforced by an authoritative conditional write or unique constraint, not a check-then-insert race or cache. Same key plus different fingerprint is quarantined. Inbox claim, domain mutation, stored outcome, and derived outbox records are atomic where they share a store.

Processing state distinguishes absent, in progress with fenced owner/lease, succeeded, terminally rejected, and uncertain external outcome. Duplicate attempts never silently acknowledge an unfinished abandoned claim. External calls receive stable effect IDs; timeout-after-success is resolved by provider lookup/replay, not a new key. Deduplication/effect retention covers the maximum broker retention, redrive, disaster replay, and audit horizon—or replay has an explicit reset/version policy.

### Common failures

Deduplicating by delivery attempt ID; omitting consumer or tenant scope; trusting producer timestamps; `SELECT` then `INSERT` without uniqueness; writing a “processed” row before the business transaction; marking success before an external call; reusing a key with changed payload; deleting inbox rows before replay expires; using a volatile cache as sole authority; treating an increment as naturally idempotent; ignoring concurrent duplicates; acknowledging a duplicate whose original is still in progress; one global dedup table becoming a hot partition; cross-region claims without one authority; and calling broker exactly-once delivery an exactly-once payment.

### Compact example

Two workers concurrently receive event `order-81:confirmed:7` for the same billing projection. Both attempt to insert `(billing-v3, tenant-4, event-id)` with the same fingerprint. One unique insert wins and atomically creates the invoice projection plus an outbox record; the other observes the committed outcome and acknowledges without repeating it. If its fingerprint differs, the consumer quarantines an identity collision. **Conclusion:** concurrency is resolved by authoritative uniqueness and transactional effects, not by timing.

### Connections

[Idempotency Keys](037-idempotency-keys.md), [Commands, Events, and Messages](061-commands-events-and-messages.md), [Ordering and Partition Keys](065-ordering-and-partition-keys.md), and [Delivery and Acknowledgment](066-delivery-and-acknowledgment.md) establish identity, semantics, order, and redelivery. The next modules apply these guarantees to dead letters, versioning, replay, and event-driven workflows.

## Governing Question

What durable identity, atomic boundary, concurrency control, outcome state, external-effect protocol, retention policy, and verification evidence make repeated delivery observationally equivalent to one accepted execution within a precisely stated consumer scope?

## Why This Matters

At-least-once delivery makes duplicates normal. A consumer can commit its database update and crash before acknowledgement; a broker can redeliver after lease expiry; a producer can publish twice after a lost response; an operator can replay retained history; a region can recover from an older checkpoint. Even an exactly-once broker feature may not cover publish-side duplicates, another database, a payment provider, or a later disaster replay.

Duplicate resistance is a business correctness property. A second projection assignment may be harmless, while a second balance increment, shipment, email, entitlement grant, or payment is not. The syntax of the handler does not prove the outcome. The design must identify every stateful effect and establish how the effect recognizes a repeated logical intent.

Concurrency makes naive deduplication fail. Two workers can both read “not processed,” both mutate state, and only then try to record completion. A cache can evict or split. A key can be reused with different content. An in-progress row can outlive a crashed worker. A replay can outlive the table's time-to-live. Durable uniqueness, transactions, fencing, fingerprints, and explicit recovery states turn these races into inspectable outcomes.

Idempotency also improves operations. It permits safe retries, redrive, backfill, reconciliation, failover, and client recovery. It does not remove capacity, ordering, authorization, or retention obligations. Duplicate storms still consume reads, locks, network, and acknowledgements; old commands may be unsafe even if repeated effects are suppressed.

## Prerequisites and Retrieval

Retrieve [Idempotency Keys](037-idempotency-keys.md), [Commands, Events, and Messages](061-commands-events-and-messages.md), [Event Schema Design](062-event-schema-design.md), [Ordering and Partition Keys](065-ordering-and-partition-keys.md), and [Delivery and Acknowledgment](066-delivery-and-acknowledgment.md). Be able to draw the crash windows between receive, inbox claim, domain commit, external effect, outbox publication, and broker acknowledgement.

Retrieve the selected broker's message-ID, redelivery, ordering, offset/ack, replay, retention, and regional semantics. Retrieve the authoritative store's unique/conditional-write, transaction isolation, retry, TTL, replication, failover, and backup-restore behavior. For each external provider, retrieve idempotency-key scope, parameter comparison, result caching, retention, concurrent-request, timeout, lookup, and reconciliation semantics.

## Learning Objectives

After completing this module, you can:

1. define idempotency as an observable domain outcome within an explicit consumer scope;
2. distinguish natural idempotency from constructed inbox, version, and effect-ledger mechanisms;
3. design stable message, fingerprint, consumer, tenant, and effect identities;
4. use authoritative uniqueness/conditional writes without check-then-act races;
5. atomically combine inbox state, domain mutation, outcome, and derived outbox records;
6. recover safely from concurrent, abandoned, failed, and uncertain processing states;
7. protect external effects with stable provider keys, lookup, ledgers, and reconciliation;
8. size retention and storage for replay, redrive, failover, and legal/audit horizons;
9. handle ordering, batches, multi-region authority, security, and duplicate storms; and
10. verify idempotency using concurrency, crash-window, replay, and adversarial tests.

## Core Exposition

### Define the observed effect and scope

Idempotency is not “the handler returned 200 twice.” Name the observer and invariant: one invoice per order version, one balance transition per ledger entry, one email per notification intent, or one projection value per subject version. Responses may differ while intended state is unchanged; a repeated request can return cached success, current outcome, or conflict.

Scope the claim by consumer purpose and semantic version. The same event may legitimately update billing, search, fraud, and analytics once each. Use a key such as `(tenant, consumer_name, consumer_semantic_version, message_id)`. Do not use deployment instance or ephemeral consumer-group generation as the durable consumer identity.

Decide whether a new consumer semantic version should reuse prior results, migrate them, or process history anew into distinct state. Changing code without changing scope can suppress a required recomputation; changing scope casually can repeat business effects. Version policy is part of rollout and replay design.

List every observable write: primary database, secondary index, outgoing event, cache, blob, search engine, payment, email, webhook, audit record, and metric with billing consequences. One idempotent projection does not make sibling effects idempotent.

### Choose a stable logical message identity

Use a source-assigned event/command ID that represents one immutable fact or intent. Preserve it through retry, redelivery, republish, retry topic, dead letter, bridge, mirror, and replay. Broker delivery tag, ack token, offset alone, trace ID, timestamp, or random ID generated by the consumer identifies the wrong scope.

If a provider message ID can change on duplicate publication, carry an application event ID in the envelope. If legacy messages lack IDs, a canonical semantic key can be derived only when the domain proves uniqueness, for example `(tenant, ledger_entry_id, projection_name)`. Hashing an entire mutable payload is a weak substitute because serialization, metadata, and schema representation can change.

Include tenant/account boundary in identity or prove global uniqueness. Normalize bytes, case, Unicode, and type before storage. Do not expose sensitive fields in keys, logs, metrics, or partition names. Enforce maximum length and allowed forms to prevent storage amplification and hot-key abuse.

### Bind identity to immutable content

Store a fingerprint of canonical semantic input with the identity. A later occurrence with the same identity and fingerprint is a duplicate. The same identity with a different fingerprint indicates producer corruption, collision, replay transformation, or attack; quarantine and alert rather than returning an unrelated prior success.

Canonicalization includes schema/type/version, tenant, subject, operation, and immutable effect-relevant fields. Exclude transport attempt metadata and fields explicitly allowed to vary. Version the canonicalization algorithm so upgrades do not turn old duplicates into false conflicts.

A cryptographic digest is compact but does not replace authorization or schema validation. Retain enough protected evidence to diagnose conflicts under privacy rules. Never log full payment or personal payload merely to prove equality.

### Prefer natural idempotency when it is true

Assignment of complete state with a monotonic source version can be naturally idempotent: setting order status for version 12 to `shipped` twice leaves the same state. Conditional `apply if incoming_version > stored_version` also rejects stale duplicates for complete-state projections.

Increment, append, allocate, send, charge, and “create with generated ID” are not naturally idempotent. Converting `balance += amount` to `balance = supplied_total` is safe only if the producer owns an authoritative complete balance/version. Absolute overwrite without version can let a stale duplicate regress state.

Algebraic operations may commute yet not be idempotent. Set union and maximum are both; addition is commutative but repeated addition changes the outcome. A conflict-free data type needs its own operation identity/counter component rules. State the proof instead of labeling all upserts idempotent.

Natural idempotency can reduce inbox retention pressure, but an inbox still provides conflict detection, outcome replay, operational evidence, and control of derived non-idempotent effects.

### Claim work with authoritative uniqueness

The canonical insert-first pattern attempts one atomic insert under a unique constraint/conditional put for the full scoped key. Exactly one concurrent transaction claims an absent identity. Losers inspect the authoritative row and choose among same-result return, wait/retry for in-progress work, terminal result, or conflict.

Do not perform `SELECT absent` followed by an unconstrained insert. Both workers can observe absence. An application mutex protects one process only. A cache `SETNX` may help throttle but is not authoritative if eviction, failover, or split-brain can lose the claim. Database uniqueness or an equivalently specified strongly consistent conditional write decides.

PostgreSQL documents composite unique constraints and `INSERT ... ON CONFLICT`; unique indexes can block concurrent conflicting inserts. Exact behavior, isolation, deadlock, and retry rules are store specific. Treat unique/serialization/deadlock errors as classified transactional outcomes, retry the whole transaction where required, and never continue with partially stale reads.

Partition/index the inbox for the scoped access pattern and lifecycle. Avoid one monotonically increasing hot partition. Bound connections, transaction time, lock waits, duplicate reads, and retry rate.

### Commit local state and outcome atomically

When inbox and business state share a transactional store, one transaction should:

1. claim or verify the scoped identity and fingerprint;
2. validate current domain preconditions and source version;
3. apply the business transition;
4. store the stable result/terminal state;
5. write derived events or work to an outbox; and
6. mark the inbox succeeded before commit.

If the transaction aborts, none of these becomes visible. If it commits and the process crashes before broker acknowledgement, redelivery finds the committed outcome. This closes the local effect/ack crash window without a distributed transaction with the broker.

Do not insert `processed=true`, commit, then update domain state. A crash loses the effect forever because duplicates are suppressed. Do not update domain state first and record inbox in another transaction; a crash repeats the mutation. An outbox in the same transaction prevents “state changed but derived event missing,” though the publisher and downstream consumers still need stable IDs.

Store enough outcome to answer a duplicate correctly. A projection event may need only succeeded/fingerprint; a command may require resource ID, status, or rejection code. Encrypt or minimize retained response data.

### Model processing states and recovery

A useful state machine is absent, in progress, succeeded, terminally rejected, and uncertain. `In progress` records owner/epoch, start/heartbeat, lease deadline, attempt count, and resumable work reference. A duplicate must not assume in progress means success.

Prefer short local transactions that complete claim and local effect together. For long work, atomically create durable work/inbox, then broker-acknowledge once ownership has transferred. Workers acquire a bounded renewable lease with fencing epoch. Completion is conditional on the current epoch so a timed-out old worker cannot overwrite a replacement.

When an owner disappears, another attempt can take over after verified expiry. Resume from durable checkpoints or restart only idempotent steps. A permanent validation/domain rejection can be stored as a terminal outcome so duplicate invalid commands receive consistent treatment. Transient failures remain retryable; do not cache them as success.

An `uncertain` state is essential when an external request may have succeeded but its response was lost. Recovery queries the provider by stable effect identity. Operators need explicit resolution paths; changing the ID to escape uncertainty risks a duplicate.

### Protect external effects separately

Derive an effect ID from stable logical message identity plus effect kind, recipient/resource, and semantic version. Persist effect intent before calling the provider. Send the same provider idempotency key on every retry and record request fingerprint, provider request/object ID, attempts, and observed outcome.

Provider guarantees are scoped. Stripe's API documentation, for example, describes saved outcomes, parameter comparison, and key pruning after a documented period for its API version. A consumer cannot assume every provider behaves this way or retain deduplication forever. Pin the provider contract and align retry horizon with its retention.

After timeout, query outcome by key/object ID when supported. If lookup proves completed, record it; if absent and retry is safe, retry same ID; if unknowable, escalate to reconciliation rather than invent another key. Payment authorized, captured, settled, and refunded are distinct outcomes. Email accepted is not delivered.

Do not hold a database transaction or broker lease across an unbounded provider call. Use a durable effect state machine and outbox/inbox boundary. When the provider lacks idempotency and lookup, exactly-once external effect is impossible under response loss; use reservation/compensation/manual review or accept named risk.

### Preserve order and batch correctness

Deduplication does not repair out-of-order state. For ordered subject transitions, store message ID plus expected subject version and atomically advance the subject's last version. A duplicate ID returns prior outcome; a different old ID is stale; a future version is a gap. One global `processed_ids` table without version checks can apply version 12 before 11.

Batch delivery is not one identity. Claim/process each logical message or make the batch an explicitly atomic domain unit with its own stable ID. Track partial outcomes and advance stream checkpoints only past the highest contiguous safely accepted record. If a whole batch retries, completed records should be cheap duplicates while unresolved records proceed.

Derived events retain causation/message identity and receive their own stable event IDs in the outbox. A retry topic, dead-letter redrive, or replay must not generate new logical IDs. Any transformation that intentionally creates a new fact documents lineage and new identity.

### Size retention and replay policy

For arrival rate $\lambda$, average retained bytes per inbox record $b$, and deduplication horizon $T$, first-order storage is

$$
Storage\approx \lambda bT,
$$

before indexes, replicas, versions, backups, and headroom. Partition/compact/archive by a governed lifecycle and measure actual cardinality and bytes.

Set $T$ at least as large as the maximum relevant broker retention, retry/dead-letter delay, operator redrive, replay/backfill, region recovery, backup restore, and external-provider retry horizon for the claimed guarantee. If business effect IDs must never repeat, retain a compact permanent ledger or make source state/version itself reject repeats.

Deleting inbox data makes an old identity eligible again. TTL is therefore a semantic boundary, not mere housekeeping. Replay older than $T$ needs a new isolated consumer scope/state, a snapshot/version gate, a preloaded dedup set, or explicit acceptance that effects may repeat. Test backup restoration: restoring business state without corresponding inbox/effect ledger can reopen duplicates.

Retention must also satisfy privacy and deletion rules. Prefer opaque IDs, minimized fingerprints/results, encryption, tenant deletion workflows, and separately protected audit evidence.

### Design multi-region authority

Active-passive consumers should have one authoritative claim store/region epoch and fence stale regions. On failover, restore business state, inbox, effect ledger, and outbox to a consistent recovery point. Broker offsets alone do not prove effect state.

Active-active processing requires globally consistent uniqueness for noncommutative effects or a domain partition/home region per identity. Eventual replication can let two regions both observe absence and commit. Later deduplication detects but cannot undo two payments.

If effects are naturally mergeable, region-local claims plus a proven merge may work. Otherwise route by stable home, use consensus/conditional authority, or accept availability loss during partition. Preserve identity/fingerprint across mirrors even when provider message IDs or offsets change.

### Secure and operate the mechanism

Authenticate message source and authorize action at the correct time. A known message ID does not authorize replay or reveal its prior result. Bind tenant and principal/delegation context into the durable record where semantics require it; decide whether delayed work executes under accepted authority or reauthorization.

Protect inbox/effect tables from arbitrary reads and mutation. Limit key length, request size, duplicate rate, per-tenant concurrency, and lookup amplification. Attackers can replay one valid ID to create lock/cache pressure or probe whether another tenant's operation exists. Return non-enumerating errors across tenant boundaries.

Observe original versus duplicate attempts, same-ID conflicts, claim latency/conflict rate, in-progress age, lease takeovers/fence failures, transaction retries, terminal/transient outcomes, external uncertain age, dedup hit rate, inbox cardinality/bytes, expiry, replay age, checkpoint lag, and reconciliation drift. Use safe hashes/high-cardinality trace links rather than raw sensitive IDs as metric labels.

Duplicate ratio is not automatically a broker defect; it can reflect expected recovery. Alert on changes, storms, conflicts, abandoned claims, horizon violations, and repeated external uncertainty. Capacity-test duplicate-heavy traffic because suppressed work still consumes resources.

### Verify the idempotency claim

Unit/property tests apply the same semantic message $n\ge2$ times and compare full intended state/effect set with one application. Vary delivery metadata while identity/content stays stable; mutate content under the same ID and require conflict.

Concurrency tests start many attempts simultaneously and assert one committed local transition/outbox/effect intent. Integration fault tests crash before claim, after claim, after mutation before commit, after commit before ack, during acknowledgement, before/after external send, after provider success before local record, during lease takeover, and during region failover.

Replay tests exceed normal batch size and exercise retention boundaries: just before TTL, exactly at expiry, after expiry, restored backup, new consumer version, and dead-letter redrive. Ordering tests combine duplicates with stale/gap records. Security tests cross tenants, forge IDs/fingerprints, flood one key, and attempt outcome enumeration.

Reconciliation compares source facts to inbox, domain state, outbox publication, external provider objects, and broker/checkpoint ranges. The evidence for idempotency is invariant preservation across repeated and failed execution—not merely a deduplication log line.

## Definitions and Notation

Let $m$ be a stable logical message ID, $a_i$ its delivery attempts, $c$ a durable consumer scope, $t$ a tenant/security scope, $f(m)$ its canonical fingerprint, and $e_k(m)$ a stable ID for effect kind $k$. Let inbox state $I(c,t,m)$ be absent, in progress with fencing epoch $q$, succeeded with outcome $o$, terminally rejected, or uncertain.

Idempotency for observable state transition $F_{c,m}$ requires $F_{c,m}(F_{c,m}(S))=F_{c,m}(S)$ within stated horizon and failure model. Equality is semantic: timestamps, attempt counters, and telemetry may change while protected business state/effect cardinality does not.

Let arrival rate be $\lambda$, duplicate fraction $d$, average retained bytes $b$, horizon $T$, and service capacity $\mu$. New unique claim rate is approximately $(1-d)\lambda$, but total lookup/admission load remains $\lambda$; stability still requires offered work below sustainable capacity with headroom.

## Mechanisms, Invariants, or Proof Structure

1. Define the exact observable outcome and consumer/tenant/version scope.
2. Preserve one logical message ID and canonical immutable fingerprint across every path.
3. Enumerate all local, derived, and external effects and assign stable effect IDs.
4. Use authoritative uniqueness/conditional write to serialize concurrent claims.
5. Atomically commit inbox, local domain transition, stored outcome, and outbox.
6. Model in-progress, terminal, and uncertain states with bounded leases and fencing.
7. Resolve external ambiguity by same-key retry/query/reconciliation, never a fresh effect ID.
8. Combine deduplication with subject versions, contiguous checkpoints, and batch partial outcomes.
9. Retain identity/outcome evidence through every retry, replay, redrive, failover, and restore horizon.
10. Verify with duplicate, concurrency, crash-window, expiry, region, and adversarial tests.

Proof sketch: assume a unique constraint admits at most one row for $(c,t,m)$, the same transaction conditionally inserts that row and commits local state/outbox, and all duplicates have the same fingerprint. Concurrent attempts serialize at the constraint; at most one can commit the transition. A crash before commit leaves neither claim nor effect, so retry may execute; a crash after commit leaves both, so retry returns the stored outcome. Thus the local transition occurs at most once. External effects require an additional stable $e_k(m)$ and provider/ledger protocol; without it, this proof does not cross the network boundary.

## Alternatives and Trade-Offs

**Natural transition versus inbox.** Versioned assignment/max/set operations reduce coordination and storage, but only when algebraically/domain idempotent. Inbox supports arbitrary mutations, conflicts, outcomes, and audit at storage cost.

**Insert-first versus effect-first.** Insert-first in one transaction safely claims local work. Effect-first can duplicate after crash; a separately committed claim before effect can strand work unless it has recoverable state/lease.

**Store full result versus compact marker.** Full result makes duplicates consistent and supports command recovery but increases privacy/storage/versioning burden. Marker is smaller but caller may need current-state query and cannot reproduce an old response.

**Database uniqueness versus distributed cache.** Database/strong conditional store is authoritative and durable but adds latency/contention. Cache can shed duplicate load but must remain an optimization in front of authority.

**Per-message inbox versus per-subject high-water mark.** Inbox handles out-of-order IDs and exact conflicts. High-water version is compact and powerful for contiguous/complete-state streams but cannot identify arbitrary duplicate IDs, gaps, or independent branches alone.

**Permanent ledger versus TTL.** Permanent compact business IDs protect lifelong effects but grow and complicate deletion. TTL controls cost but bounds the guarantee and requires replay procedures.

**Global claim store versus home-region partitioning.** Global consistency simplifies one-effect guarantees at latency/availability cost. Home-region routing scales locality but needs stable ownership/failover fencing. Eventual active-active is unsafe for noncommutative effects without merge/compensation.

**Broker transactions versus application inbox.** Broker transactions can atomically consume/produce in supported scope. Inbox joins application database state and remains useful for replay/external effects; neither silently includes the other system.

## Failure Modes and Misconceptions

1. “At-least-once plus retry” is treated as safe without idempotent effects.
2. Delivery attempt ID, offset, trace ID, or timestamp is used as logical identity.
3. Consumer, tenant, effect kind, or semantic version is omitted from key scope.
4. Same identity with changed payload returns the old outcome instead of conflict.
5. Check-then-insert races because no authoritative uniqueness exists.
6. Volatile cache/lock is the only deduplication record.
7. Inbox commits before domain state, suppressing recovery after crash.
8. Domain mutation commits before inbox, repeating after crash.
9. “Upsert” hides a non-idempotent increment or stale overwrite.
10. An in-progress duplicate is acknowledged although the owner died before effect.
11. External effect receives a new idempotency key on retry or timeout.
12. Provider key retention is shorter than application retry/reconciliation horizon.
13. Inbox TTL is shorter than broker retention, DLQ age, replay, or backup restore.
14. Deduplication suppresses a later required event because producer reused an ID.
15. Subject versions/order are ignored, so a unique but stale event regresses state.
16. Batch checkpoint passes an unresolved record because other items were duplicates.
17. Two regions each claim the same noncommutative effect under eventual replication.
18. Duplicate storms exhaust lookup/lock capacity even though effects are suppressed.

## Worked Examples

### Example 1

A customer projection receives `CustomerAddressChanged` twice. It conditionally assigns the complete address only when `customerVersion` exceeds stored version. The second version-19 event is naturally suppressed; inbox fingerprint still detects corrupted reuse.

### Example 2

An inventory event says “decrement 3.” Repeating it is unsafe. The consumer transaction inserts `(inventory-v2,event-id)`, applies the decrement, stores resulting stock, and writes an outbox record. Concurrent duplicate insert loses uniqueness and returns the stored outcome.

### Example 3

Two messages carry ID `evt-91`; one says amount 20 and one amount 200. Their canonical fingerprints differ. The consumer quarantines both relationship evidence and alerts rather than treating the second as a duplicate or applying it under a new ID.

### Example 4

A worker claims long image processing then crashes. The inbox remains `in_progress` with expired owner epoch 4. A replacement acquires epoch 5 and resumes from durable blob/checkpoint; epoch 4's late completion fails conditional fencing.

### Example 5

A charge request times out after the provider may have accepted it. The effect ledger remains uncertain and retains the same charge key. Recovery queries/retries that key and records the provider object; it never generates a new payment intent merely to clear the timeout.

### Example 6

A batch contains offsets 70–74; 70, 71, and 73 are committed duplicates, 72 is new but fails transiently, and 74 succeeds into the inbox. The consumer does not checkpoint past 71 unless 72–74 are durably owned under documented semantics.

### Example 7

An inbox TTL is seven days while a dead-letter queue retains messages for thirty. A day-20 redrive can repeat effects. The team extends the compact effect ledger beyond thirty days and makes redrive reject entries outside verified dedup coverage.

### Example 8

Billing and search both consume one order event. Keys include distinct consumer scopes, so each processes it once. A deployment restart does not change scope; a deliberate search-v2 rebuild uses isolated projection state and cannot repeat billing.

### Example 9

Regions A and B lose contact. Routing keeps account 42 homed in A; B cannot claim its payment effect without a higher authority epoch. Availability for that account pauses rather than allowing two charges under eventually replicated inbox rows.

### Example 10

At 10,000 deliveries/s with 35% duplicates, unique business transitions arrive at 6,500/s, but the authority still serves 10,000 claim/lookups/s. Capacity planning accounts for duplicate admission, conflicts, indexes, acknowledgements, and storm headroom—not just effect rate.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies unique constraints, transactions, isolation, conditional updates, indexes, TTL, backup, and recovery. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, retries, leases, fencing, consensus, replication, and impossibility boundaries.

[Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) contributes unit of work, repository, transactional outbox, state machine, and saga patterns. [Security Engineering](../../25-security-engineering/ROADMAP.md) contributes tenant isolation, authentication, replay resistance, privacy, and abuse controls.

[Data Engineering](../../19-data-engineering/ROADMAP.md) uses idempotent sinks, checkpoints, replay, backfill, watermarks, and versioned projections. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns broker/runtime defaults, claim stores, metrics, scaling, disaster recovery, and redrive tooling. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes boundary allocation, invariants, failure analysis, verification evidence, and lifecycle control.

## References

1. Microsoft. “Idempotent Consumer Pattern.” Retrieved 2026-09-02. <https://learn.microsoft.com/en-us/azure/architecture/patterns/idempotent-consumer>
2. Apache Software Foundation. “Apache Kafka 4.2 Design.” <https://kafka.apache.org/42/design/design/>
3. PostgreSQL Global Development Group. “PostgreSQL 18: INSERT.” Retrieved 2026-09-02. <https://www.postgresql.org/docs/current/sql-insert.html>
4. PostgreSQL Global Development Group. “PostgreSQL 18: Constraints.” Retrieved 2026-09-02. <https://www.postgresql.org/docs/current/ddl-constraints.html>
5. PostgreSQL Global Development Group. “PostgreSQL 18: Transaction Isolation.” Retrieved 2026-09-02. <https://www.postgresql.org/docs/18/transaction-iso.html>
6. Google Cloud. “Exactly-Once Delivery in Pub/Sub.” Retrieved 2026-09-02. <https://docs.cloud.google.com/pubsub/docs/exactly-once-delivery>
7. Stripe. “Idempotent Requests.” Retrieved 2026-09-02. <https://docs.stripe.com/api/idempotent_requests>

## Exercises

### Exercise 1

Classify these operations as naturally idempotent, idempotent only with version/identity, or non-idempotent: set profile to complete value, increment loyalty points, insert set member, append audit line, send email, and apply maximum observed temperature. State required assumptions and the exact observer.

### Exercise 2

Design an inbox schema and transaction for an order-invoicing consumer. Include consumer/tenant/message scope, fingerprint, processing state, domain mutation, outcome, outbox, uniqueness, concurrent duplicate behavior, same-ID conflict, transaction retry, and acknowledgement boundary.

### Exercise 3

A system receives 12,000 deliveries/s, 25% duplicates, retains 420 bytes of inbox data per unique message for 21 days, and uses three replicas. Estimate unique claim rate, logical retained data, and replicated retained data before indexes/headroom. Explain which load rate governs claim-store admission capacity.

### Exercise 4

Design a consumer that charges a payment provider and emits `PaymentCaptured`. Include message/effect identity, fingerprints, local states, provider key/lookup, timeout-after-success, outbox, acknowledgement, retention, reconciliation, authorization, and fault tests.

### Exercise 5

Plan a multi-region replay of forty-five days of order events when the normal inbox TTL is thirty days. Preserve billing effects and ordering while rebuilding a new search projection. Include scope/versioning, effect isolation, historical identity, dedup gap, region authority, checkpoints, capacity, security, parity, and rollback.

## Answers to the Exercises

### Answer 1

Setting a complete profile value is naturally idempotent for the same immutable value, but needs a source version/conditional update to prevent a stale duplicate from overwriting newer state. Set insertion is naturally idempotent under set semantics and a canonical member identity. Maximum observed temperature is algebraically idempotent and commutative for the maximum observer, though event-time/window attribution may need identity and watermark policy.

Incrementing loyalty points is not idempotent: repeat adds again. Bind one award/ledger-entry ID and insert it uniquely with balance update in one transaction. Appending an audit line is not idempotent unless the log rejects a stable audit-event ID or represents a set/indexed fact. Sending email is an external non-idempotent effect; use stable notification ID, effect ledger, provider idempotency where available, and outcome/reconciliation. “Same final database row” is insufficient if billing, audit, or notification observers differ.

### Answer 2

Use a composite unique key `(tenant_id, 'invoice-v1', message_id)` with non-null canonical fingerprint, message/schema version, subject/order ID/version, status, owner epoch/lease where needed, stable invoice/outcome reference, attempt timestamps/count, and protected diagnostic fields. The invoice table has a unique business key such as `(tenant_id, order_id, invoice_revision)`; outbox has a stable derived event ID/causation.

For short work, begin one database transaction and attempt the inbox insert. On an existing row, compare fingerprint: different means quarantine/conflict; succeeded or terminal means return recorded outcome; live in-progress means bounded retry; expired ownership follows fenced recovery. On a new row, validate expected order version and authorization, create invoice, store result, create outbox `InvoiceIssued`, mark succeeded, and commit. Then acknowledge the broker. Crash before commit leaves no effect; crash after commit/before ack makes redelivery retrieve the result.

Use the database's unique constraint/`ON CONFLICT` behavior and retry the whole transaction on serialization/deadlock outcomes. Never commit “processed” before invoice or publish directly outside the outbox. Metrics distinguish winner, same-result duplicate, conflict, retry, and abandoned claim without leaking tenant data.

### Answer 3

Unique fraction is $1-0.25=0.75$, so unique claim rate is $12{,}000\times0.75=9{,}000$ records/s. Twenty-one days contain $21\times86{,}400=1{,}814{,}400$ seconds. Logical retained bytes are

$$
9{,}000\times420\times1{,}814{,}400=6{,}858{,}432{,}000{,}000\text{ bytes},
$$

about 6.86 TB decimal before indexes/metadata. Three replicas require about 20.58 TB decimal of record bytes before indexes, backups, compaction overhead, and headroom.

Admission capacity is governed by all 12,000 deliveries/s because duplicates still perform validation and authoritative lookup/conflict work. Unique inserts/business transitions are 9,000/s. Benchmark both paths, bursts, one-key contention, retention cleanup, replication, and failure/retry amplification; partition and provision connections/IOPS with SLO headroom.

### Answer 4

Use consumer key `(tenant,payment-capture-v1,message_id)` and immutable fingerprint over payment/order/amount/currency/payment-method reference and command version. Derive effect ID from `(tenant,message_id,capture,provider-account)`; never use broker attempt ID. In one local transaction claim inbox, validate authorization/order version, create effect intent `pending`, and commit durable work. The broker may then be acknowledged because the application owns recovery; alternatively keep bounded delivery until durable acceptance is confirmed.

Effect worker leases the intent with fencing epoch and calls the pinned provider using the same idempotency key every time. Record provider request/object ID. Response success moves effect to captured; terminal decline records terminal result; transport timeout moves to uncertain. Recovery queries/retries the same key/object according to provider semantics. It never creates a new key. An outbox transaction records `PaymentCaptured` only from confirmed captured state with stable event ID; publisher retry and downstream consumers deduplicate.

Retain compact effect/business identity at least through provider-key retention, chargeback/reconciliation, broker/DLQ/replay, disaster restore, and business duplicate horizon. If provider retention is shorter, local ledger plus provider object lookup/manual reconciliation governs late uncertainty. Reauthorize delayed execution or persist accepted delegation according to contract; isolate provider accounts/tenants and protect results.

Inject crashes before/after intent commit, before provider call, timeout after provider success, after response before local commit, after captured commit before outbox publish, after publish before mark/ack, lease takeover, duplicate concurrency, same-ID changed amount, key expiry, and region failover. Reconcile source order, inbox, effect ledger, provider object, outbox, broker, and accounting ledger.

### Answer 5

Billing must not reuse a scope whose evidence expired. First inventory source retention, event IDs/fingerprints/versions, order sequence, billing inbox/effect-ledger permanence, provider horizon, old/new search schemas, mirrors, checkpoints, and restore points. Forty-five-day replay exceeds the thirty-day normal inbox guarantee; do not feed it blindly into effecting consumers.

Create isolated `search-rebuild-<semantic-version>` projection state and durable consumer scope, preserving original event IDs, fingerprints, subject versions, and causation. This new scope may process each historical event once into new search state but has no credentials/routes for billing, payment, email, or other business effects. Existing billing subscriptions remain disconnected from the replay; if billing verification is required, run read-only reconciliation against its compact permanent ledger/source snapshots rather than execute commands.

Replay per order in authoritative version order, detect duplicates/stale/gaps, checkpoint contiguous durable acceptance, and throttle by region/tenant/partition so live traffic retains capacity. Choose one replay coordinator/home epoch; fence a failed region before takeover and restore projection plus inbox/checkpoint consistently. Encrypt data, reapply current access/deletion policy, limit operator authorization, and audit replay ranges without exposing payloads.

Shadow-query old and new search, comparing per-order last version, counts, checksums, representative queries, deletions, and gap/conflict reports at recorded high-water marks. Fault-test duplicate source records, region loss, expired normal inbox entries, missing versions, schema variants, and restart from checkpoint. Cut reads at an explicit parity/high-water gate while retaining old projection for rollback. Rollback changes read routing only; it never replays billing effects or changes historical logical identities.
