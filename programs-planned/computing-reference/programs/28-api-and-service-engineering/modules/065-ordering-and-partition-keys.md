---
module_id: API-065
program: API & Service Engineering
level: 2
module_number: 65
title: Ordering and Partition Keys
status: complete
last_verified: 2026-09-02
---

# Ordering and Partition Keys

## One-Page Review

### Governing question

Which domain transitions truly require order, over what subject/scope, and how should partition keys, sequences, producer concurrency, consumer processing, retries, rebalances, and migrations preserve that order without creating global bottlenecks or hot-key failures?

### Essential definitions

- **domain order** is a required precedence relation among facts or commands because reversing them changes correctness.
- **transport order** is the order a broker/protocol exposes within its documented scope, often one partition, ordering key, producer session, or subscription.
- A **total order** compares every pair of events; a **partial order** compares only causally or domain-related pairs.
- A **partition key** is the value a routing function uses to place related records into an ordered shard/partition.
- An **ordering subject** is the stable domain entity or coordination scope whose transitions must serialize, such as account, order, device, or workflow.
- A **subject sequence/version** is an authoritative monotonic value used to detect duplicate, stale, or missing transitions within one subject.
- A **hot key** receives disproportionate traffic and caps throughput at one partition/consumer serialization path.
- **processing order** is the order effects commit in the consumer; it can diverge from fetch/delivery order through concurrency, retry, or asynchronous I/O.
- **fencing** prevents a stale producer/consumer owner from continuing after a lease/epoch/rebalance transfers authority.

### Central model, mechanism, or theorem

Let events for subject $s$ have authoritative sequence $v=1,2,\ldots$. Route by

$$
p=h(key(s))\bmod P
$$

for $P$ partitions under the provider's exact partitioner. Same stable key normally gives partition locality while $P$ and partitioner remain compatible; it does not create cross-key order. A consumer may commit event $e_{s,v}$ only when its subject state expects $v$ (or when the documented commutative/version-replacement rule permits otherwise). Gap detection is

$$
v>last(s)+1.
$$

This application sequence survives retries, bridges, and partition migrations better than relying only on broker offsets.

### Critical invariants

Order is required only where a domain proof needs it and is scoped by stable ordering subject. All messages in that scope use the same canonical key and compatible channel/path; the key is present, validated, immutable, non-sensitive, and authorized. One subject's authoritative sequence/version is assigned at the source commit and stable across attempts. Producer concurrency/retry configuration is tested; retries keep identity/key/sequence. Consumer fetch, dispatch, processing, effect commit, and checkpoint preserve per-key order or use an explicit commutative/versioned algorithm.

Offsets identify broker position, not domain version across partitions/topics/regions. Timestamps and trace IDs do not prove order. Rebalances/failover fence stale owners and atomically align state/checkpoint. Gaps, duplicates, late events, poison records, retry detours, key skew, and hot subjects have bounded policy. Partition-count/partitioner/key changes are migrations with dual-routing/high-water/reconciliation evidence, not transparent configuration edits. Global order is chosen only when its throughput/availability/latency cost is an explicit hard requirement.

### Common failures

Saying “the topic is ordered” without scope; using random/no key for state transitions; keying by event type instead of entity; inconsistent key serialization/case; mutable email/name as key; tenant omitted from a non-global ID; hashing sensitive identifiers without threat analysis; relying on timestamps; using correlation/trace ID as order; multiple producers assigning the same subject version without authority; assuming same key stays on same partition after partition-count/algorithm change; worker pool commits out of order; offset advances past failed earlier record; retry topic lets later records pass; one poison subject blocks an entire partition forever; global key makes one hot partition; splitting a hot entity without conflict model; and region migration creates two active writers.

### Compact example

Account facts key by `(tenantId, accountId)` and carry `accountVersion`. Versions 41 and 42 route to one partition. The consumer receives 42 while local version is 40 because 41 was diverted to retry; it detects a gap, pauses that account, and restores 41 before committing 42. Other accounts continue through keyed lanes. A rebalance increments ownership epoch so the old worker cannot commit. **Conclusion:** partition locality helps delivery, but subject sequence, keyed processing, fencing, and gap recovery establish end-to-end order.

### Connections

[Topic and Channel Design](064-topic-and-channel-design.md) defines the physical boundary; [Commands, Events, and Messages](061-commands-events-and-messages.md) defines identity/authority; [Event Schema Design](062-event-schema-design.md) defines subject sequence fields. The next module separates delivery and acknowledgement guarantees, followed by idempotent consumers and replay.

## Governing Question

What precedence relation must be preserved for correctness, which authority assigns it, how is the ordering subject routed and processed, and how does the system detect and recover from duplication, gaps, retries, skew, rebalances, failover, and topology change?

## Why This Matters

“Ordered messaging” is dangerously incomplete. Kafka documents totally ordered partitions; Google Pub/Sub offers ordering within an ordering key under configured conditions; Kinesis maps partition keys to shards; Pulsar exposes subscription/routing modes. None of these automatically defines the domain subject, source sequence, cross-topic causality, consumer effect order, or multi-region authority.

Ordering has a cost. Putting every record on one partition creates a total transport order but limits parallelism and expands blast radius. Hashing by entity scales across partitions but one popular entity remains hot. Random distribution maximizes throughput but forces downstream coordination for noncommutative transitions. The correct scope is the smallest domain boundary whose operations cannot commute safely.

Transport order can be lost after delivery. A consumer fetches records sequentially then submits them to a worker pool; record 12 completes before 11. A failed record moves to a retry topic while later versions proceed. A rebalance runs old and new owners briefly without fencing. A regional failover has two producers. End-to-end correctness therefore composes producer, broker, consumer, state store, and recovery.

Explicit subject versions also make failures observable. Broker offsets cannot tell whether an account jumped from version 40 to 42 when events passed through multiple topics or regions. A domain sequence detects gap and enables targeted replay/snapshot/reconciliation.

## Prerequisites and Retrieval

Retrieve [Idempotency Keys](037-idempotency-keys.md), [Commands, Events, and Messages](061-commands-events-and-messages.md), [Event Schema Design](062-event-schema-design.md), and [Topic and Channel Design](064-topic-and-channel-design.md). Be able to distinguish domain order, causality, wall-clock/event/ingest time, broker partition/offset, delivery attempt, subject version, and consumer checkpoint.

Retrieve exact producer partitioner and retry/idempotence settings, broker partition/order/failover semantics, consumer group/subscription/rebalance behavior, state/checkpoint transaction model, bridge/mirror behavior, and current partition/key distribution. Provider guarantees are version/configuration dependent.

## Learning Objectives

After completing this module, you can:

1. derive minimal ordering scope from domain invariants and commutativity;
2. distinguish total, partial, causal, transport, delivery, and processing order;
3. select canonical stable partition keys and subject sequences;
4. reason about producer batching, concurrency, retry, idempotence, and multi-writer authority;
5. preserve keyed order through consumer dispatch, async work, checkpoints, and rebalances;
6. detect and handle duplicates, stale records, gaps, late events, and poison subjects;
7. quantify partition skew, hot keys, parallelism, and global-order cost;
8. design multi-entity and cross-stream workflows without invented global order;
9. migrate keys, partition counts, topics, and regions with reconciliation; and
10. verify ordering under load, failure, replay, and adversarial inputs.

## Core Exposition

### Derive order from domain invariants

Write pairs of operations/events and ask whether swapping them changes a valid outcome. `AccountOpened` must precede `AccountClosed`; balance debits/credits may be noncommutative with overdraft decisions; `OrderConfirmed` precedes `OrderCancelled` under a state machine. Independent orders normally need no relative order.

Some operations commute. Incrementing a counter with stable operation IDs may converge regardless of order. Taking maximum observed version/timestamp under a trusted rule can tolerate reorder. Set union can commute; list append does not. If a consumer uses a commutative/idempotent merge, it can gain parallelism—but document the algebra and conflicts rather than casually claiming order is unnecessary.

Choose the smallest ordering subject that contains noncommutative transitions: account, order, device, reservation, workflow. Tenant-wide/global order is rarely required. If a rule spans two accounts, one account key cannot serialize it; use an authoritative transaction/coordinator, deterministic multi-key locking, saga with explicit compensations, or a ledger model—not wishful broker order.

Order of facts reflects the source state transition. The authoritative store/aggregate/ledger assigns a monotonic version within the same atomic commit that makes the event eligible. Publication timing may differ, but source version remains truth.

### Distinguish five orders

1. **Domain order:** required state-machine/causal precedence.
2. **Producer send order:** order one producer client submits batches/records.
3. **Broker order:** provider-defined order within partition/key/session/shard.
4. **Delivery/fetch order:** order records reach a consumer instance; retry/rebalance can repeat.
5. **Processing/commit order:** order consumer effects and checkpoints become durable.

These can diverge. A broker can preserve partition order while concurrent callbacks commit effects out of order. A producer can create domain versions 10/11 but publisher workers send 11 first unless outbox dispatch is keyed/ordered. A mirror can preserve per-partition order but repartition by another key. A retry channel deliberately detours one record.

State the required end-to-end chain and evidence at each hop. If only final replace-by-version state matters, consumer can ignore stale records. If every transition has an effect, gaps require recovery before later commit.

### Model total, partial, and causal order

A total order compares every event. One ordered partition/sequencer can provide it within a service boundary, but throughput, availability, latency, and failover depend on that serialization point. Many “global order” requests actually need deterministic audit display, not global execution. A stable tie-breaker can sort reports without forcing live total order.

A partial order relates only events for the same subject or explicit causality. It scales because independent subjects run concurrently. Represent relation $e_a\prec e_b$ through subject version, command/event causation, or workflow state. Do not infer it solely from wall clocks; clocks skew and equal timestamps occur.

Vector clocks/logical clocks can represent causality in specialized distributed systems, but they add metadata/state and do not resolve conflicting business decisions automatically. Most APIs benefit from authoritative per-aggregate sequence plus explicit cross-workflow causation/preconditions.

Trace context follows diagnostic execution and is neither authoritative causal history nor domain order. Sampling, async fan-out, trust-boundary regeneration, and batch processing make trace topology incomplete. Keep causation ID/version in business envelope.

### Choose a stable canonical key

The partition key should equal or deterministically derive from the ordering subject. Account facts use account ID plus tenant scope; device readings use device ID; order lifecycle facts use order ID. If identifiers are only tenant-unique, encode a canonical length-prefixed tuple or unambiguous structured bytes—not string concatenation that can collide.

Define type, encoding, Unicode/case normalization, null/empty handling, length, maximum cardinality, authority, and privacy. All producers/languages use shared conformance vectors. The broker hashes bytes; `ABC`, `abc`, different Unicode normalization, and integer text/binary forms can route differently.

Key must remain stable for the subject lifetime. Email, username, status, region, or owner are mutable and inappropriate. A random event ID distributes each transition separately and destroys subject locality. Event type key groups all instances of a type into one hot partition and does not serialize one entity meaningfully.

Avoid exposing direct personal identifiers in broker keys/logs/metrics/control plane. Use opaque stable scoped ID or keyed tokenization with governed collision/key-rotation semantics. Hashing low-entropy values alone does not anonymize them. Authorization validates key matches trusted payload subject and tenant.

### Understand partition mapping

Kafka allows semantic key partitioning and documents locality from same user ID key. Common hash-modulo mapping illustrates the principle, but actual partitioners/broker routing must be pinned. Some sticky/batching behavior applies when key absent. Google Pub/Sub ordering uses ordering keys; Kinesis maps partition keys to shards; Pulsar supports routing modes and keyed subscriptions. Do not port assumptions blindly.

Same key locality is conditional on same topic/stream, partitioner implementation/configuration, partition count/routing epoch, producer/client versions, and bridge behavior. Adding partitions under simple modulo changes many mappings. Old records stay in old partitions; new records may route elsewhere, so concurrent consumption no longer guarantees one partition for full subject history.

Explicit partition numbers couple producers to topology and make scaling/migration difficult. Prefer stable semantic keys and provider-supported routing unless specialized ownership justifies manual mapping. Record partitioner/version in contract and test deterministic vectors.

The broker offset is monotonic only within a partition. Offsets across partitions cannot be compared to determine event order. A topic offset may reset/change under migration/restore; it is not a portable domain version.

### Control producer order and authority

One source transaction assigns subject version and outbox record. Outbox publisher must preserve per-key order: partition/lease work by subject, query ordered by source sequence, or use a dispatcher that never has multiple unresolved sends for the same key when retry can reorder. Parallelize across keys.

Producer batching and in-flight requests improve throughput. Under failures, retry behavior and idempotent producer configuration can affect duplicate/order guarantees; pin exact client settings and test broker/client versions. Stable event ID/subject version still provide application detection even if transport promises hold.

Multiple legitimate producers for one ordering subject require one sequencing authority: shared transactional store, leader/lease/epoch, consensus log, or conflict-resolution model. Timestamps or locally incremented counters on two writers collide. Fencing tokens/epochs reject stale writer after leadership changes.

Regional active-active writes cannot maintain one simple per-subject sequence without coordination or a merge model. Options: home-region route, per-subject leader, globally consistent sequence/transaction, CRDT/commutative operations, or accept conflicts with explicit versions. State availability/latency trade-off.

### Preserve order in consumers

Broker assignment often gives one consumer instance a partition, but application worker pools can break order. Use one serial lane per partition/key, keyed executor/mailbox, partition-affine stateful processor, or concurrency controller that prevents later same-key commit before earlier terminal state. Bound lane queues and idle-key cleanup.

Parallel fetch and deserialize can remain safe if effect commit is resequenced. Tag records with partition/offset and subject sequence; release results in order only if side effects have not occurred prematurely. Async external calls are difficult to reorder safely—use idempotent effect IDs and wait/coordinate per key.

Checkpoint/offset must align with durable application state. Advancing partition offset past an unresolved earlier record can lose it even if later records succeeded. Atomic local state+inbox+checkpoint, broker transaction where scope fits, or durable inbox before ack establishes boundary. The next modules deepen acknowledgement/idempotency.

For replace-by-version state, consumer can apply if $v>last$, ignore $v\le last$, and detect but perhaps tolerate gaps if each event is a complete snapshot. For transition effects, require $v=last+1$ before apply. Document initialization, reset, tombstone, wrap, and correction.

### Handle duplicates, stale records, and gaps

Duplicate has same logical event ID/version; return prior result or ignore after inbox. Stale has lower/equal subject version but possibly different ID; investigate producer correction/replay and apply policy. Gap has version greater than expected. Do not collapse all into “out of order.”

On gap, buffer within per-key count/bytes/age, pause only affected key/partition where possible, fetch missing events from retained log/source, request authorized snapshot/reset, or quarantine/reconcile. Unbounded buffering is a memory attack. If missing event expired, reset from a coherent snapshot with version and audit lost transition effects.

Late event may be correct event-time data arriving after processing-time windows. Stream processing uses watermarks/allowed lateness/retractions separately from entity state version. A late measurement can have a new ingestion sequence but old observed time; define both.

Corrections are new facts with new subject version linking corrected event. Do not insert/rewrite an old version silently. Consumers update projections/aggregates under correction policy.

### Treat retry as an ordering decision

In-place retry blocks later records in a partition, preserving order but causing head-of-line blocking across unrelated keys sharing it. Keyed pause lets unrelated keys proceed if consumer framework/state supports it. A retry topic frees main partition but later same-key records can overtake.

For noncommutative transitions, either retain per-key block until success/terminal decision, route all later same-key records behind the retry state, or use sequence/gap to refuse later commit until predecessor recovered. For commutative/complete versioned state, allow later records and classify stale retry when it returns.

Poison records need bounded attempt/age and quarantine. One bad subject should not freeze an entire high-volume partition forever, but skipping must be an explicit reset/correction/reconciliation—not silent offset advance. Quarantine preserves original ID/key/version/schema/location and current authorization/privacy.

Retry preserves key and partition intent. If the physical retry channel has different partition count/partitioner, application subject sequence—not matching partition number—guides recovery.

### Manage rebalances, leases, and failover

Consumer group rebalance moves partition ownership. Stop fetch, quiesce/cancel/finish bounded in-flight work, commit state/checkpoint atomically, revoke, then new owner restores from durable checkpoint. Timeouts can overlap old/new processing; use partition/subject lease epoch or state-store fencing so stale owner cannot commit after revocation.

Static membership can reduce unnecessary reassignments but does not remove crash/fencing requirements. Cooperative rebalancing changes movement behavior but application still handles revocation safely. Pin exact client/broker semantics.

Broker leader failover may retry/duplicate. Provider configuration determines durability/order. Application event IDs and subject versions detect anomalies. Cross-cluster mirrors/DR restore need documented partition/key mapping, high-water marks, offsets translation, and single-writer/fencing.

Never let both regions resume writes for same subject after partition without conflict policy. Recovery drills must simulate network partition, stale lease, process pause, clock skew, and delayed old writer—not only clean shutdown.

### Quantify skew and hot keys

With total rate $\lambda$ and key fraction $q_s$, subject rate is $\lambda_s=q_s\lambda$. Since one subject serializes on one lane/partition for strict order, its service capacity $\mu_s$ must exceed peak $\lambda_s$ with headroom. Adding partitions does not split one key automatically.

Measure per-key/partition records and bytes, p95/p99/max share, lag/age, processing latency, queue depth, throttling, and rebalance load. Avoid exporting raw high-cardinality sensitive keys; use top-K secured diagnostics, hashed/bucketed metrics, and sampled traces.

Mitigations: remove unnecessary global order, optimize/batch per-key processing, increase single-lane capacity, isolate hot tenants/entities, use hierarchical key where operations commute within subkeys, pre-aggregate, or redesign state/coordination. Adding random suffix (“salting”) breaks order unless downstream merge has a mathematically valid rule.

A celebrity account or fleet gateway can dominate. Load tests use realistic skew, not uniform random keys. Tenant quotas prevent one key/tenant starving others, but throttling must respect command deadlines and fact retention.

### Coordinate multi-entity workflows

A transfer touches two accounts; an order workflow touches payment, inventory, fulfillment. No single event partition key gives total order across all without centralizing. Keep each aggregate's authoritative order and coordinate through command IDs, preconditions, workflow/saga state, transactional ledger, or multi-entity transaction where available.

Workflow event carries workflow sequence plus references to aggregate versions. Consumers never infer causal success from arrival order across topics. `PaymentCaptured` and `InventoryReserved` can arrive either way; orchestrator records both facts by IDs and advances when predicate holds. Compensation has new commands/events, not rewind.

For atomic double-entry ledger, one authority/transaction may order entries by transaction ID and accounts within a database; downstream events can project per account with shared transaction/causation ID. Do not make broker partitioning substitute for source atomicity.

### Migrate keys and partition topology

Key change is breaking for ordering/locality. Inventory history, producers, consumers, partitioners, joins/state stores, retry/DLQ, mirrors, and schema. Define old/new canonical key mapping and whether one event can route both without divergent identities.

Create new topic/channel or routing epoch when necessary. Dual publish/mirror same event ID/subject sequence/key versions from one source. Backfill history in subject order, capture high-water marks, start shadow consumers, compare counts/checksums/versions/gaps/state, then cut at explicit epoch. Consumers deduplicate across paths.

Increasing partitions in place may redistribute new keys; assess provider semantics and stateful consumer consequences. A new topic with stable partition count can give cleaner cutover. Never assume partition number equality across clusters/topics.

Region failover assigns one writer epoch/home and fences old region. Offset translation is operational; domain version is reconciliation truth. Retain rollback source until consumers, gaps, state, and SLOs pass the maximum observation window.

### Verify ordering under faults

Model/property tests generate subject state machines and permute independent keys while asserting required precedence. Verify commutative claims with algebraic/property tests. Golden partition vectors test key bytes/normalization/partitioner across languages and versions.

Integration tests cover multiple producers, batching, retries, broker failover, duplicate, reorder, missing record, retry detour, poison, slow/hot key, worker concurrency, crash between effect/checkpoint, rebalance during in-flight, stale owner fencing, partition resize, mirror/region failover, replay/backfill, and schema/key changes.

Observe event ID, safe subject hash/tenant, subject version, partition/offset, producer epoch, consumer ownership epoch, expected/actual version, gaps/stale/duplicates, keyed queue age, per-partition lag, hot-key share, retries/quarantine, and checkpoint commit. Do not log payload secrets or unbounded IDs.

Reconcile projection's per-subject last version/invariants against authoritative snapshots/log ranges. Ordering is not proven by “no broker errors”; it is proven by state and fault evidence.

## Definitions and Notation

Let event $e_{s,v}$ be subject $s$ at authoritative version $v$. Required partial order is $e_{s,v}\prec e_{s,v+1}$. Let canonical key $k(s)$ and partitioner $p=h(k(s))\bmod P$ illustrate routing for $P$ partitions; actual $h$ and mapping are provider/version specific.

Let consumer state $last(s)$ be highest committed contiguous subject version. Duplicate/stale satisfies $v\le last(s)$; next satisfies $v=last(s)+1$; gap satisfies $v>last(s)+1$. For complete-state last-write-by-version projections, apply may use $v>last(s)$ while separately recording gaps; transition consumers require contiguity.

Let total arrival rate $\lambda$, key share $q_s$, subject rate $\lambda_s=q_s\lambda$, and single-key service capacity $\mu_s$. Stable operation requires peak arrival below sustainable service with headroom; $\lambda_s\ge\mu_s$ causes unbounded backlog absent shedding/coalescing/redesign.

## Mechanisms, Invariants, or Proof Structure

1. Derive required precedence/commutativity from domain state transitions.
2. Choose smallest stable ordering subject and authoritative sequence assignment.
3. Specify canonical non-sensitive key bytes and provider partitioner/version.
4. Ensure every producer/path uses same key/sequence and fence multi-writer authority.
5. Preserve keyed order through batching/retry/broker/mirror and detect anomalies independently.
6. Serialize or correctly merge consumer effects; atomically align state/inbox/checkpoint.
7. Handle duplicate/stale/gap/late/correction with bounded explicit policy.
8. Design retry, poison, rebalance, lease, and failover behavior without silent skip or stale commit.
9. Measure skew/hot subjects and migrate topology with stable IDs/high-water/reconciliation.
10. Verify state-machine properties and inject concurrency/failure/replay/migration faults.

Proof sketch: if the source assigns unique contiguous $v$ atomically, all records for $s$ route through one ordered path, and consumer commits only expected $v=last+1$ atomically with advancing `last`, then the projection cannot commit $v+1$ before $v$. Each assumption is necessary; worker side effects before resequencing, two writers, key drift, or non-atomic checkpoint breaks the conclusion.

## Alternatives and Trade-Offs

**Global total order versus keyed partial order.** Global simplifies some audits/coordinators but serializes all traffic and enlarges failure domain. Keyed order scales independent subjects while cross-subject workflows need explicit coordination.

**Broker order alone versus subject sequence.** Broker partition order is efficient locally; subject sequence survives topology/bridge/retry and detects gaps. Use both when correctness matters.

**Strict serial processing versus commutative/versioned parallelism.** Serial is simpler for noncommutative transitions; algebraic merges improve throughput but demand proof, idempotency, and conflict semantics.

**In-place retry versus retry channel.** In-place preserves partition order but blocks unrelated keys. Retry channel isolates delay but permits overtaking. Keyed pause/sequence recovery can balance.

**Hash partitioning versus explicit routing/range.** Hash spreads stable keys but obscures placement/migration; explicit/range supports locality/control but risks skew and operational complexity.

**Home-region single writer versus active-active merge.** Home region simplifies sequence/order at availability/latency cost; active-active needs coordination or commutative conflict model and cannot promise simple global order for free.

**Stable partition count versus elastic reshard.** Stability preserves mapping/local state; reshard adds capacity but changes routes/state movement. Plan epochs/migration rather than treating it as invisible.

## Failure Modes and Misconceptions

1. “The topic is ordered” omits partition/key/producer/consumer scope.
2. Event ID, type, timestamp, correlation, or trace ID is used as partition key instead of ordering subject.
3. Canonical key bytes differ across languages, tenants, case, or Unicode forms.
4. Mutable/sensitive field becomes long-lived routing key.
5. Multiple writers assign local sequences without leader/transaction/conflict model.
6. Offset or timestamp is treated as portable domain version/global order.
7. Async worker pool commits effects/checkpoints out of order.
8. Offset advances past failed predecessor; later records make loss permanent.
9. Retry topic or DLQ silently violates per-key order.
10. Poison event blocks every key in a partition indefinitely.
11. Random salting “fixes” a hot key while destroying noncommutative order.
12. Adding partitions/partitioner upgrade is assumed to preserve key mapping/history.
13. Rebalance lets stale consumer commit after new owner without fencing.
14. Active-active region failover produces two authoritative sequences.
15. Uniform-key load tests miss production skew and single-key capacity.

## Worked Examples

### Example 1

Order lifecycle facts key by `(tenant,orderId)` and carry `orderVersion`. Independent orders process concurrently; versions within one order commit contiguously. No tenant-wide total order is claimed.

### Example 2

Telemetry measurements can be aggregated by commutative max/count with event-ID deduplication, so strict arrival order is unnecessary. Device configuration commands remain serial by device because later command assumes prior version.

### Example 3

Two producers emit account versions 17 independently after a split brain. Consumer detects conflicting IDs/fingerprints at same version and quarantines; timestamp sorting cannot repair authority. Fencing/home-region leadership prevents recurrence.

### Example 4

A consumer fetches offsets 100/101 for one account and starts async writes. 101 finishes first. The design replaces unrestricted pool with keyed lane and atomic state/checkpoint; only after 100 commits may 101 effect begin/commit.

### Example 5

Version 42 goes to delayed retry while 43 arrives. A transition consumer refuses 43, buffers within bounds, restores 42, then advances. A complete-state projection may apply 43 and classify 42 stale if the contract proves no transition effect is needed.

### Example 6

One celebrity tenant produces 35% of traffic. Adding partitions helps other keys but not its serial tenant-wide key. The system changes the unnecessary tenant key to order ID while moving the truly tenant-global quota decision to a separate coordinator.

### Example 7

A transfer touches accounts A and B. Events retain per-account versions and common transfer ID. One ledger transaction is authoritative; downstream arrival across account partitions is unordered. Consumers reconcile transfer predicate instead of comparing offsets.

### Example 8

Partition count grows from 8 to 16 under modulo hashing. Many keys remap while old history remains in prior partitions. The team creates a routing epoch/new topic, backfills per subject, dual publishes same IDs/versions, and cuts after parity rather than assuming transparent resize.

### Example 9

A rebalance occurs with one external call in flight. Ownership epoch changes; old worker's conditional state commit fails fencing. New owner reprocesses from durable checkpoint with same effect ID and obtains prior external outcome.

### Example 10

Region A loses connectivity and Region B takes home ownership epoch 9. Region A's paused process resumes with epoch 8 and is rejected at authoritative store/publisher. Mirrored offsets differ, but subject versions and event IDs reconcile without dual truth.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial orders, logical clocks, consensus, logs, leases, and fencing. [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) contributes hashing, load distribution, queues, and scheduling. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies versions, transactions, locks, ledgers, and checkpoints.

[Data Engineering](../../19-data-engineering/ROADMAP.md) uses partitions, event time, watermarks, replay, and stateful stream processing. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns broker partitioning, consumer runtimes, autoscaling, metrics, and migration tooling. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes invariant allocation, interface verification, failure analysis, and migration control.

## References

1. Apache Software Foundation. “Apache Kafka 4.2 Design.” <https://kafka.apache.org/42/design/design/>
2. Apache Software Foundation. “Apache Kafka 4.2 Producer Configurations.” <https://kafka.apache.org/42/configuration/producer-configs/>
3. Apache Software Foundation. “Apache Pulsar: Messaging Concepts.” Retrieved 2026-09-02. <https://pulsar.apache.org/docs/next/concepts-messaging/>
4. Google Cloud. “Order Messages in Pub/Sub.” Retrieved 2026-09-02. <https://docs.cloud.google.com/pubsub/docs/ordering>
5. Amazon Web Services. “Amazon Kinesis Data Streams Terminology and Concepts.” Retrieved 2026-09-02. <https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html>
6. W3C. “Trace Context, W3C Recommendation.” 23 November 2021. <https://www.w3.org/TR/trace-context/>

## Exercises

### Exercise 1

For account transactions, order lifecycle, IoT telemetry, notification delivery, and global audit display, identify required order subject, whether operations commute, candidate partition key/sequence, and whether total order is actually necessary.

### Exercise 2

A topic has 24 partitions and 40,000 records/s. One tenant/account key carries 18% of records; one serial consumer lane sustains 5,500 records/s at safe utilization. Compute the hot-key rate and assess stability. Explain why doubling partitions may not help and propose semantic/operational alternatives.

### Exercise 3

Design a consumer for per-device transition events that can process 10,000 devices concurrently while preserving device order. Include keyed lanes, bounds, duplicate/stale/gap policy, async effects, checkpoints, retry, poison, rebalance, fencing, and observability.

### Exercise 4

Plan a partition-key migration from customer ID to order ID while retained history and live traffic coexist. Include domain-order justification, schemas/routing epoch, backfill, dual publish, consumers/state, parity, high-water marks, hot-key tests, rollback, and retirement.

### Exercise 5

Design ordering for an active-passive multi-region payment workflow with accounts, transfers, and notifications. Define authority/epochs, per-entity versions, cross-entity causality, broker/mirror paths, failover, fencing, duplicates/gaps, reconciliation, and disaster tests without claiming global order.

## Answers to the Exercises

### Answer 1

Account transactions require order per `(tenant,accountId)` when balance/overdraft/state transitions are noncommutative; key by canonical scoped account ID and assign authoritative account/ledger version. Independent accounts have no required total order. Cross-account transfer needs ledger/transaction coordinator or workflow, not one account partition alone.

Order lifecycle requires order per scoped order ID and `orderVersion`; created/confirmed/cancelled do not commute under state machine. IoT raw measurements may tolerate reorder if each has device sequence/observed time and aggregation is commutative/window-correct; configuration transitions key by device and require config version. Notification delivery often deduplicates by notification/effect ID and can commute across recipients; per-recipient preference/version or conversation order may be scoped when UX demands it.

Global audit display usually needs deterministic reporting, not live global serialization. Store occurred/recorded times, source versions, causation, and stable tie-breaker; acknowledge partial order/concurrent facts. Use total sequencer only if a legal/domain invariant truly requires one adjudicated sequence and accept its capacity/availability cost.

### Answer 2

Hot-key rate is $0.18\times40{,}000=7{,}200$ records/s. Safe single-lane service is 5,500 records/s, so utilization demand is $7{,}200/5{,}500\approx1.309$ or 131%; backlog grows by at least 1,700 records/s before bursts/failures. The design is unstable.

Doubling partitions does not split one stable key; its records still route to one partition/lane. It helps other keys and may remap history, but hot subject remains serial. First question whether tenant-wide ordering is necessary. If order is really per account/order/device, use that stable subject key while moving tenant-wide quota/coordination to dedicated service. If one account truly must serialize, optimize/batch state transitions, increase single-lane/storage capacity, isolate the hot subject/tenant, apply admission/rate limits, or redesign with proven commutative operations/subkeys. Random salting is invalid without merge/conflict proof.

Load/fault test realistic 18%+ bursts, retry, failover, and rebalance; monitor top-key secured share, lane queue/age, processing latency, throttling, and subject gaps. Preserve stable identity/versions during any key migration.

### Answer 3

Use canonical `(tenant,deviceId)` key and authoritative contiguous `deviceVersion` assigned with source transition. Broker partitions distribute devices; each consumer owns assigned partitions and dispatches to bounded keyed mailboxes/executors, one active transition per device but many devices concurrently. Limit global/per-partition/per-key queued messages/bytes/age, idle-lane count, async calls, and rate; backpressure/pause before memory exhaustion.

Atomically store device projection, event inbox ID/fingerprint, last contiguous version, pending durable effect IDs/outcomes, and checkpoint/ack boundary. Same ID/version duplicate returns prior outcome; lower version is stale and audited; expected `last+1` applies; higher is gap. Buffer small gaps per device, retrieve retained missing range or authorized snapshot/reset, and never silently advance for transition events.

Async external effects use stable effect ID and remain within keyed state machine: later version cannot commit first. Short transient retry blocks device; longer retry uses durable per-device pending state and prevents later commit. Permanent poison quarantines original ID/key/version/schema with protected bounded diagnostics; operator reset/redrive revalidates current policy/idempotency and reconciles.

On rebalance stop new dispatch, drain/cancel bounded work, atomically commit, and increment/release ownership epoch. New owner restores; stale commits fail fencing. Test crash after effect/before checkpoint, lease pause, duplicate, gap, retry overtaking, hot device, broker failover, and replay. Observe safe device hash, expected/actual version, keyed queue age, partition lag, epoch/fence failures, retries/quarantine, checkpoint latency, and reconciliation drift.

### Answer 4

First prove customer-wide order is unnecessary and order-local transitions only require order ID. Inventory all event types, source versions, producers/partitioners, topics/partitions, consumer groups/state stores/joins, retry/DLQ, mirrors, schemas, and customer-key assumptions. Add explicit `orderingKeyVersion`/routing epoch and ensure order ID plus tenant is present/canonical on every relevant event; keep event ID and authoritative order version stable.

Prefer a new topic/routing epoch with fixed planned partitions. Backfill retained history grouped/sorted by order version, preserving IDs/schema/causation and recording source positions/high-water marks. One authoritative outbox router dual publishes live events under old customer key and new order key—no independent fact generation. Shadow consumers build new keyed state; inbox deduplicates and parity checks per-order counts/checksums/versions/gaps plus aggregate business invariants.

Test key conformance across languages, distribution/skew/hot orders, retry/rebalance/failover, joins formerly colocated by customer, and consumer capacity. Move consumers at explicit source/new high-water correspondence, maintaining old path for rollback. New processing uses order-key lanes; customer-wide calculations become explicit aggregation/coordinator, not implicit partition order.

After all active/dormant/replay consumers migrate, stop old publication, drain/reconcile final versions, observe through rollback/retention window, archive mapping/checkpoints/schemas, then delete via channel lifecycle policy. Rollback resumes old consumers while dual publication remains; stable IDs prevent duplicate effects. Any parity gap pauses cutover and replays original IDs.

### Answer 5

Choose one home/active region per authoritative payment account/ledger shard under lease/consensus epoch. Source store rejects writes/outbox publication with stale epoch. Accounts have contiguous account/ledger versions; transfer has stable transfer/command ID and transfer state version. One atomic ledger transaction or coordinator commits debit/credit and outbox facts; broker partitions cannot create atomicity across accounts.

Events key per account for account projections and carry common transfer ID/causation plus source transaction reference. Transfer orchestrator records both sides/status explicitly; it does not compare cross-partition/topic offsets or timestamps. Notifications are downstream effects with stable effect IDs and may arrive later/retry without changing payment truth. No global order is claimed across accounts/regions.

Primary broker paths preserve canonical keys/versions; mirror documents whether partitions/offsets change and preserves event IDs/headers. Consumer state/checkpoint is atomic/idempotent and detects duplicate/stale/gap. Region B continuously verifies replicated store/log high-water and mirror lag. Failover fences region A, establishes higher epoch in authoritative quorum, confirms recovery point, assigns B writers, resumes publication from durable outbox, and reconciles subject versions/IDs rather than offsets alone.

If A resumes partitioned, epoch rejects its writes/publishes. Lost responses resolve by command/transfer outcome ID. Gaps trigger retained range/snapshot reconciliation; duplicates dedupe; uncertain external payment effects query provider by stable effect ID. Failback is another epoch/migration, never simultaneous writers.

Test abrupt region/broker/store loss, network partition, delayed stale process, partial replication, clock skew, duplicate mirror, missing record, reordered notification, consumer rebalance, registry outage, and failback. Verify ledger balance/invariants, transfer terminal states, per-account contiguous versions, outbox-to-broker completeness, consumer checkpoints, notification effect ledger, RPO/RTO, and protected audit. Global chronology for reports uses times/causation/tie-breaks with concurrency disclosed.
