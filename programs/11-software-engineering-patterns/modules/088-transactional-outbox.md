---
module_id: SEPAT-088
program: Software Engineering: Patterns
level: 2
module_number: 88
title: Transactional Outbox
status: complete
last_verified: 2026-08-29
---

# Transactional Outbox

## One-Page Review

### Governing question

How can a committed change in one transactional store durably create an obligation to publish a message without a distributed transaction across that store and the broker—and without losing the obligation when processes crash?

### Essential definitions

- A **dual write** is one logical operation that independently writes two transactional systems, such as a database and broker.
- A **transactional outbox** atomically stores authoritative domain change and publication intent in the same local transaction.
- An **outbox record** is the durable publication intent, including stable event/message identity, destination/routing data, schema/type, payload or reconstructable immutable reference, ordering information and lifecycle metadata.
- A **relay** transfers committed outbox records to a broker or destination asynchronously.
- A **polling publisher** claims/query-scans outbox records; a **transaction-log tailer/CDC relay** derives committed outbox inserts from the database change log.
- The **commit–publish gap** is the unsafe interval between domain commit and a separate broker send.
- The **publish–mark ambiguity window** occurs when the broker accepts a record but the relay crashes before recording that fact.
- **at-least-once publication** means eligible committed intent is retried until acknowledged, so duplicates are possible.
- A **stable event identity** remains the same across relay attempts; an attempt/message transport identity may change.
- **ordering scope** names the key—often one aggregate/entity—within which consumers require an ordered sequence.

### Central model, mechanism, or theorem

Let local transaction \(T\) atomically commit domain state \(D'\) and outbox intent \(O_e\):

\[
T: (D,O) \rightarrow (D', O \cup \{O_e\}).
\]

Atomicity establishes the producer invariant

\[
D'\text{ commits} \iff O_e\text{ commits}
\]

for the change/event pair encoded by that transaction. A relay later attempts \(O_e\rightarrow B_e\). It cannot generally atomically combine broker acceptance and outbox acknowledgement; a crash can therefore publish \(B_e\) more than once. The pattern guarantees durable *publication intent* coupled to local commit, not exactly-once delivery or consumer effect. End-to-end correctness requires a stable event ID, safe relay retries, broker retention/acknowledgement, and an idempotent consumer boundary.

### Critical invariants

- Domain change and corresponding outbox record commit or roll back in one local transaction.
- The outbox payload/reference represents the committed fact, not mutable state re-read later without version binding.
- Each logical event has a stable immutable identity and compatible content across all relay attempts.
- Relay claims are bounded, recoverable and safe under concurrent workers; stale owners cannot corrupt lifecycle state.
- Mark-before-publish is forbidden; publish-before-mark accepts duplicates rather than loss.
- Ordering is claimed only for a defined producer/aggregate/partition scope with explicit sequence and routing.
- Backlog count, bytes, oldest age and storage/transaction cost are bounded by admission and retention policy.
- Cleanup cannot delete a record before required broker acknowledgement/reconciliation and replay obligations are satisfied.
- Relay credentials are narrower than producer authority; untrusted payload cannot choose arbitrary destinations or headers.
- Consumer idempotency and atomic effect/inbox recording remain separate requirements; outbox does not solve them.

### Common failures

Common failures include sending before commit and later rolling back; sending after commit and crashing first; marking sent before broker acceptance; generating a new event ID on retry; rebuilding event bytes from current mutable rows; assuming a timestamp gives a total commit order; parallel relays reordering one aggregate; unbounded broker-outage backlog; hot polling and long producer transactions; clearing old rows without broker/replay evidence; treating CDC offset commit as a consumer effect guarantee; publishing database schema as a public contract; routing from attacker-controlled fields; exposing secrets in durable payloads; replaying obsolete commands; and calling broker “exactly once” features an end-to-end proof.

### Compact example

In one database transaction, an order changes from `pending` to `paid` and inserts outbox event `evt-41`, aggregate `order-17`, sequence 8, type `OrderPaid`, immutable versioned payload. The relay publishes `evt-41`, the broker accepts it, and the relay crashes before marking the row. Recovery republishes the same ID and bytes. The consumer deduplicates `evt-41`; the relay eventually records acknowledgement. No event is lost, but duplicate delivery was expected rather than denied.

### Connections

[SEPAT-087](087-saga.md) creates durable workflow transitions that need reliable commands/events, [SEPAT-061](061-message-channel.md) and [SEPAT-066](066-publish-subscribe-channel.md) define delivery boundaries, while [SEPAT-069](069-dead-letter-channel.md) preserves failed delivery evidence. The successor [Idempotent Consumer](../ROADMAP.md) completes the receiving-side effect boundary that Transactional Outbox intentionally leaves open.

## Governing Question

How can a service make “this local business fact committed, therefore this message must eventually be offered for publication” one atomic statement, while accepting that the database and broker do not share a transaction?

The Transactional Outbox pattern changes the second write. Instead of treating broker publication as part of the request transaction, the producer stores a durable publication obligation beside the domain change. A relay performs external delivery later. The pattern removes the producer's lost-intent dual-write gap; it does not remove asynchronous delay, duplicates, ordering design, consumer failure or operational backlog.

## Why This Matters

Consider two obvious orders. Send to the broker first, then commit the database: if the database rolls back, consumers act on a fact that never became authoritative. Commit the database first, then send: if the process crashes in between, the fact exists but observers may never hear it. Retrying the whole request can duplicate domain work, and “we will reconcile logs later” is not a deterministic publication protocol.

Two-phase commit across the database and broker may be unavailable, operationally undesirable, or incompatible with independent systems. The outbox uses the database's existing atomicity to persist both source truth and an obligation. This is a precise narrowing: it solves atomic creation of intent inside one local transaction. The relay and consumers remain distributed.

This boundary supports domain events, saga commands, cache/projection invalidation, webhooks, audit feeds and integration messages. Failures are often silent: a green request latency graph can coexist with a growing outbox and stale downstream state. Publication lag and reconciliation therefore belong to correctness and service-level objectives, not only messaging operations.

## Prerequisites and Retrieval

Learners should retrieve:

- local ACID transaction commit/rollback and isolation;
- domain event versus command semantics and authoritative source ownership;
- message identity, acknowledgement, retry and at-least-once delivery;
- primary keys, unique constraints, versions and per-aggregate sequence numbers;
- database polling, row locks, leases, write-ahead/change logs and CDC;
- idempotent effects and consumer inbox/deduplication;
- queue/backlog capacity, deadlines, backpressure and observability;
- schema compatibility, security classification and data retention.

Before continuing, enumerate the four outcomes of independently attempting a database commit and broker publication, and identify which two make the systems disagree.

## Learning Objectives

After this module, learners can:

1. derive the producer dual-write failure matrix;
2. state exactly what local atomicity the outbox provides and what it does not;
3. design stable outbox identity, payload, routing, sequence and lifecycle fields;
4. compare polling publisher and transaction-log/CDC relays;
5. make relay claiming and acknowledgement safe under crash and concurrency;
6. define honest ordering scope across aggregates, instances and partitions;
7. bound backlog, retention, cleanup and recovery traffic;
8. separate publication, broker delivery and consumer-effect evidence;
9. secure event creation, routing, payload, replay and operator repair;
10. verify every commit, relay, broker acknowledgement and cleanup boundary.

## Core Exposition

### Derive the dual-write matrix

Let `DB` mean the domain transaction committed and `MSG` mean the broker accepted the intended message. Independent writes allow four states:

| DB | MSG | Interpretation |
|---|---|---|
| no | no | no business fact and no notification; ordinary failure |
| yes | no | committed fact is invisible downstream; lost publication |
| no | yes | consumers observe a fact that rolled back or never existed |
| yes | yes | desired outcome, subject to duplicate/order/consumer semantics |

Reordering only chooses which inconsistent row becomes possible. Broker-first permits `no/yes`; database-first permits `yes/no`. A process-level retry cannot know whether a timed-out broker operation committed, so naive compensation adds ambiguity.

The outbox makes the local choice `DB and O` versus `neither`. External `MSG` remains later. If the broker is down, `O` persists and can be retried. If the local transaction rolls back, no outbox record becomes visible. The application trades synchronous broker dependence for asynchronous backlog and eventual publication.

### Define the publication contract

Not every database change needs a public event. Before inserting a row, define:

- source fact and authoritative entity/version;
- event versus command semantics;
- event/message ID and creation transaction identity;
- aggregate/ordering key and monotonic sequence if required;
- stable type/name and schema version;
- destination selected from trusted policy;
- immutable payload bytes or immutable version-bound reference;
- tenant/security classification and allowed headers;
- creation time, not-before/expiry where semantically valid;
- delivery lifecycle and evidence required before cleanup.

An outbox row is an obligation, not a convenient copy of a mutable object. If the relay reconstructs `OrderPaid` by reading the current order after it was refunded, it can publish content that never matched the original commit. Prefer serializing canonical versioned event data in the transaction. A content-addressed immutable object/reference can work when atomic reference creation, availability and retention are proven. Binding only to an entity ID is insufficient.

Public events should express durable domain contracts rather than database table rows. Database columns evolve for local needs; leaking them couples consumers to private schema and may expose secrets. Validate event construction in producer tests and schema/compatibility governance.

### Model identities precisely

Separate the logical **event ID** from relay **attempt ID**, broker record/offset, trace ID, request ID and domain entity ID. All relay retries for one outbox record preserve event ID and content fingerprint. The broker may assign a new record/offset to a duplicate attempt; consumers deduplicate the logical event ID within the correct producer/tenant namespace.

Generate event identity before or inside the local transaction using a collision-resistant or database-assigned unique key. Enforce uniqueness. If a command retry legitimately reaches the producer twice, producer request idempotency may need to ensure it creates one domain transition and one outbox event; the outbox alone does not deduplicate incoming commands.

Ordering needs explicit identity too. A per-aggregate sequence generated atomically with the aggregate update can express `order-17` versions 7 then 8. A wall-clock timestamp is not a total commit order: clocks collide/skew and transaction creation order can differ from commit visibility. A global database sequence may have gaps and allocation order need not equal commit order. State the actual property and route all events for one ordering key through compatible serialization/partitioning.

### Commit domain state and outbox atomically

The producer transaction should:

1. validate command/idempotency and authorization;
2. read/check the authoritative entity version;
3. compute the domain transition and event from the same before/after facts;
4. write the domain mutation;
5. insert immutable outbox record(s);
6. commit once.

A unique constraint can bind one event type/effect to a domain transition. Transaction rollback removes both mutation and outbox insertion. Avoid network calls inside this transaction: a broker call lengthens locks and still cannot participate atomically without a supported distributed protocol. Keep payload construction deterministic and bounded; oversized records increase database, log, backup and relay costs.

If triggers generate outbox rows, they can prevent application omission and see committed row changes, but domain semantics in database triggers can become hidden and difficult to version/test. Application-level creation is explicit but every write path must use it. A repository/unit-of-work boundary, database constraint, invariant audit or code-generation framework can reduce omission. Choose ownership deliberately.

### Relay by polling

A polling publisher queries eligible committed rows, claims a bounded batch, publishes and records outcome. Multiple workers need a concurrency protocol such as short row locks with skip-locked selection, or leases plus owner/generation tokens. Do not hold a database transaction open while waiting on a remote broker if avoidable; claim durably, release, publish, then conditionally acknowledge the same owner/generation. A stale worker must not mark a row whose claim was superseded.

Poll interval trades latency for database load. Empty hot polling wastes resources; huge batches create long locks, unfairness and recovery bursts. Use indexes for eligibility/order, bounded batch bytes/count, adaptive wake-up where supported, and per-tenant/partition fairness. Retriable failures get bounded backoff/jitter; permanent contract/routing failures enter an owned quarantine state, not infinite hot retry.

Polling is portable and operationally direct. It can struggle with high volume, exact commit ordering, table bloat and query contention. Deleting or updating rows creates additional write amplification. Partitioning/archival and carefully designed lifecycle tables may be required.

### Relay by transaction-log tailing or CDC

Log tailing observes committed outbox inserts from the database replication/change log and transforms/routes them. It avoids repeated polling and can preserve database log order within documented scopes. Debezium's documented Outbox Event Router, for example, expects an outbox table and maps configured ID, aggregate, type, payload and routing fields; exact connector behavior is version-specific.

CDC adds infrastructure, permissions, log-retention and offset/recovery dependencies. A captured outbox insert still must reach the destination; connector offset commit can be ambiguous relative to broker publication. Schema changes, snapshots, connector reconfiguration, failover and log truncation require tests. Capturing arbitrary domain-table rows and trying to infer events is not equivalent to an explicit outbox: row changes may lack business meaning, before-state, tenant policy or canonical contract.

Choose polling or CDC from throughput, latency, ordering, operational ownership, database capabilities, portability and recovery evidence. Both implement a relay; neither changes the local atomic invariant.

### Accept duplicate publication

There is normally no atomic transaction spanning broker acceptance and `outbox.published=true`. Two unsafe choices remain:

- mark first, publish second: crash between them loses the event;
- publish first, mark second: crash between them duplicates the event.

Choose possible duplication over silent loss for required publication. Preserve the same event ID and content so broker-side producer idempotence (where configured) and consumer deduplication can help. Broker transactional/idempotent producer features can narrow duplicates within their documented session/topic conditions, but database-to-broker end-to-end atomicity still requires proof; do not generalize a product label.

Acknowledgement should identify destination, event/content, broker evidence if available, attempt, time and relay generation. A `published_at` timestamp is local evidence, not proof that every consumer received or applied the event. For webhooks, “HTTP 200” proves only the receiver's contractually defined acknowledgement; payload effect may need destination-specific idempotency and receipts.

### Deterministic crash-window trace

The following pure model commits domain state with one outbox record, simulates broker acceptance followed by relay crash, then retries with the same event ID. The final set models one consumer effect for duplicate records.

<!-- bijux-verify: {"id":"sepat-088-outbox-crash-window","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"commit=order-17:paid,outbox=evt-41:pending\nbroker=evt-41,evt-41\nconsumer-effects=evt-41\noutbox=evt-41:published\n","stderr":""}} -->
```python
domain = {}
outbox = {}
broker = []

domain["order-17"] = "paid"
outbox["evt-41"] = "pending"
print("commit=order-17:" + domain["order-17"] + ",outbox=evt-41:" + outbox["evt-41"])

broker.append("evt-41")
# The first relay attempt stops after broker acceptance, before acknowledgement.
broker.append("evt-41")
outbox["evt-41"] = "published"

consumer_effects = sorted(set(broker))
print("broker=" + ",".join(broker))
print("consumer-effects=" + ",".join(consumer_effects))
print("outbox=evt-41:" + outbox["evt-41"])
```

This execution proves exact deterministic container/output behavior for one repeated ID. It does not execute a transaction, broker, crash, relay concurrency, database isolation, network acknowledgement, durable deduplication, ordering, backpressure, security, CDC or recovery.

### Define ordering narrowly

“Messages are ordered” is incomplete. Name source, key, competing writers, commit order definition, relay lane, broker partition, consumer group and recovery behavior. Common useful guarantees are per aggregate/entity, not global.

To preserve per-aggregate order:

- atomically assign aggregate version/sequence with domain update;
- route a stable aggregate key to one ordered broker partition/lane;
- prevent parallel relay attempts from overtaking earlier sequence for that key, or let consumers buffer/reject gaps explicitly;
- treat retries without changing sequence;
- have consumers detect duplicate, stale and gap conditions.

Strict ordering can reduce throughput and availability. Independent aggregates may publish concurrently. Global order across shards/databases requires an explicit sequencer/consensus or a weaker causal contract. If consumers merely need monotonic entity versions, tolerate cross-entity reorder and document it.

### Bound backlog and recovery

During broker outage, local transactions can continue creating publication debt. Outbox count, bytes and oldest age then grow; database storage, indexes, logs, backups and query latency can threaten the source of truth. This is delayed coupling, not decoupling from capacity.

Define budgets and staged response:

- monitor pending count/bytes/age per destination/tenant/class;
- reserve storage and protect producer transaction latency;
- shed optional event-producing work or disable optional payloads first;
- degrade readiness or reject operations whose required notifications cannot meet contract;
- preserve critical reconciliation/control capacity;
- alert before log/storage exhaustion;
- pace recovery so a backlog does not flood broker/consumers or starve live traffic.

Priority can help but must not starve old required events or reorder a protected key. Weighted lanes and separate tables/partitions may isolate critical streams. Expired commands may be unsafe to execute, while historical facts usually should not be silently dropped; semantics decide.

### Retention, cleanup and replay

Cleanup is part of correctness. Define the condition: broker acknowledgement plus a safety delay, reconciled destination receipt, CDC offset beyond retained source, or archival that supports audit/replay. Never delete merely because a relay attempted publication. Broker retention does not automatically satisfy legal audit or rebuild horizons.

Deleting rows in large transactions can cause locks, log bursts and bloat. Use bounded batches/partitions and verify replicas/backups. Tombstones/partition drops must respect CDC readers. Retain stable event identity long enough for consumer deduplication/replay contracts; replayed facts should preserve original event ID and occurrence data while using a distinct replay/attempt context.

An outbox is not automatically an event store. It may be pruned after delivery and may lack full aggregate history. Event sourcing uses events as authoritative state; outbox records are publication obligations derived within another authoritative transaction. Conflating them creates false recovery assumptions.

### Consumer boundary remains separate

The relay's successful publish does not prove a consumer processed the record. Brokers may redeliver; consumer code may commit an effect then crash before acknowledgement; multiple consumer groups have independent progress. The next module develops Idempotent Consumer.

At minimum, consumers use the stable event ID, validate producer/type/schema/tenant, and atomically bind deduplication/inbox state to their own local effect. If the consumer then publishes another event, it creates its own outbox in that same local transaction. This forms a chain of locally atomic handoffs, not one global transaction.

End-to-end evidence distinguishes: source domain commit, outbox insertion, relay claim/attempt, broker acknowledgement/offset, consumer delivery, inbox/effect commit and consumer acknowledgement. A trace correlates these facts but cannot replace them.

### Security, privacy and governance

The producer transaction is the trusted creation boundary. Derive destination, type and security headers from server policy, not arbitrary user payload. Authorize the domain transition first. Bind tenant, aggregate and event ID; prevent cross-tenant topic/partition injection. Validate size and schema before commit.

Outbox tables replicate into backups and may be visible to CDC operators. Minimize secrets and personal data, encrypt/classify fields where needed, use references only with proven retention/authorization, and define erasure versus immutable-audit policy with legal review. Relays need read/claim and narrowly scoped destination publish rights—not domain mutation or wildcard administration.

Schema/type/destination changes are deployable contracts. Use compatibility tests, staged routing, versioned consumers and replay tests. An operator repair that inserts a missing outbox row must first establish the authoritative domain fact and canonical original event semantics, then use a stable repair identity and journal the action; fabricating notifications from partial tables can worsen an incident.

### Verification strategy

Test the transaction rollback and commit pair directly: fail before/after domain write and outbox insert, and prove only `(neither)` or `(both)` is visible. Test event bytes against the committed version. Exercise unique constraints and incoming-command retries.

For relays inject failure before claim, after claim, before broker request, after broker acceptance before local acknowledgement, and during acknowledgement/lease expiry. Run multiple workers, stale generations, partial batches, slow broker, permanent schema/routing rejection and restart. Assert no eligible row is silently lost; duplicates keep identity/content; lifecycle changes are conditional.

Test per-key ordering with concurrent producers/relays, equal timestamps, transaction reorder, retry and partition rebalance. Load-test polling/CDC overhead, transaction latency, index/bloat and backlog capacity. Simulate broker outage until staged admission, then recovery with pacing and live-traffic fairness. Test cleanup during relay/CDC lag, replay after retention, database failover and connector snapshot/schema evolution.

Security tests attempt destination/header/tenant injection, oversized payload, relay privilege abuse, secret leakage and malicious replay. Reconciliation compares authoritative domain transitions, expected outbox rows, broker evidence and consumer effects. No unit trace or broker marketing guarantee establishes universal end-to-end exactly once.

## Definitions and Notation

Let \(D_v\) be authoritative domain entity state at version \(v\), \(O_e\) an outbox intent with stable event ID \(e\), type \(\tau\), schema version \(s\), payload/fingerprint \(p\), ordering key \(k\) and sequence \(q\). Let relay attempts be \(a_1,a_2,\ldots\), broker records \(B_{e,a}\), and outbox lifecycle state \(l_e\). Let \(A\) be eligible pending backlog, \(|A|\) count, \(bytes(A)\) storage, and \(age_{max}(A)\) oldest eligible age.

The core local invariant is that the corresponding \(D_v\) and \(O_e\) are visible together after commit and absent together after rollback. It does not imply \(B_{e,a}\) is synchronous, unique, ordered globally, retained forever, delivered to every consumer, or applied exactly once.

## Mechanisms, Invariants, or Proof Structure

**Dual-write elimination.** Because domain mutation and outbox insert share one atomic local transaction, no crash exposes exactly one of that pair, assuming all producer write paths obey the boundary and storage atomicity holds.

**Event truth.** If payload/fingerprint is computed from the same committed transition and immutable across attempts, every duplicate relay attempt represents the same fact. Reconstruction from unversioned mutable state breaks this argument.

**At-least-once publication.** Publish-before-mark plus durable retry makes acceptance eventually repeat until acknowledgement under fair relay scheduling, available broker/database and retained intent. It deliberately permits duplicates in the publish–mark window.

**No-loss choice.** Mark-before-publish can permanently suppress an unpublished event after crash; publish-before-mark cannot silently suppress it but may duplicate it. Required publication therefore chooses duplicate-tolerant mechanics.

**Per-key order.** Atomic sequence assignment, no overtaking in the relay lane, stable broker partitioning and consumer gap/stale checks can preserve order for one key. Remove any premise and the ordering claim weakens.

**Bounded operation.** Admission thresholds, finite batches, indexed claims, retention and paced recovery can keep outbox debt within declared resources. The pattern alone provides no bound; an indefinitely unavailable broker with unconstrained producers grows debt indefinitely.

**End-to-end composition.** Producer outbox plus at-least-once transport plus atomic consumer inbox/effect yields one logical consumer effect per stable event ID under deduplication retention and local isolation assumptions. Outbox alone proves only the producer half.

## Alternatives and Trade-Offs

| Alternative | Prefer when | Limitation or cost |
|---|---|---|
| synchronous broker write in 2PC | database/broker support it and coupling/blocking are acceptable | availability, operational complexity, limited external participants |
| best-effort send after commit | notification is disposable and reconciliation is sufficient | silent loss for required messages |
| broker first | message can safely exist without domain commit | usually publishes false facts after rollback |
| polling publisher | portability and simple database ownership dominate | query load, latency, bloat and ordering complexity |
| transaction-log/CDC relay | high throughput/low polling load and CDC operations are mature | connector/log/offset/schema/failover complexity |
| database notifications as wake-up | notification can prompt polling while table remains truth | notification alone may be lossy or connection-scoped |
| event sourcing | events are authoritative aggregate state | larger modeling, evolution, projection and operational commitment |
| direct source-table CDC | row changes themselves are a sufficient governed contract | often lacks domain semantics and leaks schema |
| reconciliation scan | low-volume gaps can be derived unambiguously | detection delay and hard reconstruction; useful defense, not primary atomicity |

## Failure Modes and Misconceptions

- **The outbox sends atomically to the broker.** It atomically creates local publication intent.
- **No duplicate can occur.** Broker acceptance before relay acknowledgement creates a duplicate window.
- **Exactly-once broker means exactly-once business effect.** Consumer transaction/effect evidence is separate.
- **A new retry ID is harmless.** It defeats logical-event deduplication.
- **The latest row can rebuild the old event.** Current state may differ from committed event-time state.
- **Timestamps define order.** Clock/allocation order need not equal commit or causal order.
- **Ordering is global.** It normally needs a named key/partition and serialization.
- **Polling with many workers is automatically safe.** Claims, leases, generations and conditional acknowledgement matter.
- **CDC removes operational state.** Offsets, logs, snapshots, schema and connector recovery become critical.
- **Outbox backlog is cheap.** It consumes source database capacity and creates publication debt.
- **Published means consumed.** It proves only the configured broker/destination acknowledgement.
- **Dead-letter/quarantine resolves the event.** The domain obligation still needs owned repair.
- **Cleanup is housekeeping.** Premature deletion can destroy recovery/replay evidence.
- **An outbox is an event store.** Publication obligations need not be authoritative history.
- **Triggers always solve omission.** They may hide domain semantics and still need contract/version governance.

## Worked Examples

### Example 1

A service commits `invoice.status=issued` and crashes before direct broker send. The database-first dual write leaves `DB=yes, MSG=no`. With an outbox, the same transaction inserts `InvoiceIssued(evt-9)`; recovery relay later sends it. The conclusion is durable intent survives process failure independently of request handling.

### Example 2

A service sends `AccountOpened` before its database transaction fails a unique constraint. Consumers create welcome work for an account that does not exist. Moving broker-first to database-first merely changes the possible inconsistency. Atomically persisting domain state plus outbox eliminates both producer pair mismatches.

### Example 3

The relay publishes `evt-41`, broker accepts, then the host dies before `published_at`. Recovery republishes `evt-41` with identical bytes. Mark-first would risk loss, so the design accepts duplicates; consumer inbox/effect commits once. The event ID, not broker offset, names the logical fact.

### Example 4

An order is paid at version 8 and refunded at version 9 before relay publication. A relay that reconstructs payload from the current row emits `OrderPaid` containing `refunded`. Storing canonical version-8 bytes—or an immutable version-bound reference—in the outbox preserves event truth.

### Example 5

Transactions for order version 7 and 8 are created on different instances; timestamps collide and version 8's relay runs first. A per-order sequence, stable order key/partition, and relay no-overtake/gap policy preserve 7 then 8. Unrelated orders remain parallel; no global order is claimed.

### Example 6

Four polling workers select the same pending rows without claims and produce four duplicates per cycle. The table uses bounded skip-locked claim or leases with owner/generation, releases database locks before remote I/O, and conditionally acknowledges the current generation. Duplicates remain possible after broker accept, but concurrency no longer creates avoidable races.

### Example 7

The broker is unavailable for six hours. Outbox bytes approach the database reserve and producer latency rises. Policy sheds optional analytics-producing operations, rejects new operations whose required notification SLO cannot be met, preserves critical control/reconciliation capacity, and alerts. Recovery uses bounded weighted pacing so old backlog and live events progress without consumer collapse.

### Example 8

A CDC connector is redeployed with a new snapshot configuration and republishes retained outbox inserts. Stable event IDs and consumer deduplication make repetition safe; reconciliation verifies no log gap. The team tests connector offset, database failover and schema evolution rather than assuming CDC eliminates duplicates.

### Example 9

An attacker supplies `destination=admin.commands` and embeds credentials in event metadata. The producer ignores client routing, selects an allow-listed destination from authenticated domain policy, binds tenant/type, validates size/schema and stores no unnecessary secret. The relay has publish rights only to approved destinations.

### Example 10

An operations tool finds a completed regulated case without its required outbox event. It does not blindly synthesize from today's row. An authorized reviewer verifies the original transition/version and audit evidence; the tool inserts one canonical repair event under a stable repair key in a journaled transaction. Legal/domain reviewers define whether late notification is adequate; technical delivery evidence cannot decide regulatory sufficiency.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md): domain events, aggregates and authoritative transitions define what the outbox records.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): transactional boundaries, asynchronous coupling and failure ownership.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): crash-window, concurrency, compatibility, backlog and reconciliation tests.
- [Database Engineering](../../18-database-engineering/ROADMAP.md): atomic transactions, isolation, indexes, write-ahead logs, CDC, bloat and retention.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): tenant/routing authority, relay privileges, replay and durable payload privacy.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): partial failure, acknowledgement ambiguity, ordering, identity and at-least-once delivery.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): broker/CDC operations, lag objectives, repair tooling, capacity and recovery game days.

## References

1. Richardson, Chris. “Pattern: Transactional Outbox.” *Microservices.io*. <https://microservices.io/patterns/data/transactional-outbox.html>
2. Richardson, Chris. “Pattern: Polling Publisher.” *Microservices.io*. <https://microservices.io/patterns/data/polling-publisher.html>
3. Richardson, Chris. *Microservices Patterns*, 2nd ed. Manning, 2025.
4. Amazon Web Services. “Transactional Outbox Pattern.” AWS Prescriptive Guidance. <https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html>
5. Debezium Authors. “Outbox Event Router.” Debezium Reference Documentation. <https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html>
6. Helland, Pat. “Life Beyond Distributed Transactions: An Apostate's Opinion.” *CIDR*, 2007, pp. 132–141. <https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf>
7. Hohpe, Gregor, and Bobby Woolf. *Enterprise Integration Patterns*. Addison-Wesley, 2003.
8. Kleppmann, Martin. *Designing Data-Intensive Applications*. O'Reilly, 2017.
9. Gray, Jim, and Andreas Reuter. *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann, 1992.
10. Fowler, Martin. “What Do You Mean by ‘Event-Driven’?” 2017. <https://martinfowler.com/articles/201701-event-driven.html>
11. CloudEvents Authors. “CloudEvents Specification.” <https://github.com/cloudevents/spec>
12. PostgreSQL Global Development Group. “Explicit Locking” and “Logical Decoding Concepts.” <https://www.postgresql.org/docs/current/explicit-locking.html> and <https://www.postgresql.org/docs/current/logicaldecoding-explanation.html>

Official AWS, Debezium, CloudEvents and PostgreSQL sources were checked on 2026-08-29. Exact broker acknowledgement, idempotent-producer, partition ordering, CDC offset and database lock/log behavior are product/version/configuration specific and must be verified for the deployed stack.

## Exercises

### Exercise 1

Derive the dual-write failure matrix for a database and broker, then state precisely how a transactional outbox changes it.

### Exercise 2

Design an outbox record and per-order ordering protocol for `OrderPaid` and `OrderRefunded`, including identity, immutable content, relay attempts and consumer gap behavior.

### Exercise 3

Diagnose a relay that marks rows sent before publishing, hot-polls without an index, holds row locks during broker I/O, uses timestamps for global order, and deletes rows after any attempt. Redesign and specify decisive tests.

### Exercise 4

Compare polling and transaction-log/CDC relays for a service producing 20,000 events/s across many aggregate keys with a strict per-key order requirement and a mature database platform but a small messaging team.

### Exercise 5

Design transactional publication for high-stakes device commands during a 12-hour broker outage. Include admission/backlog, expiry, security, acknowledgement, repair, recovery pacing and named human review.

## Answers to the Exercises

### Answer 1

Independent writes permit `(DB no, MSG no)`, `(yes, no)`, `(no, yes)` and `(yes, yes)`. Database-first plus crash can produce a committed fact with no message; broker-first plus database rollback can publish a false fact. Changing order removes neither class collectively.

The outbox local transaction commits domain change and publication intent together: either both are visible or neither is. Broker publication happens later from durable intent. Thus a broker outage no longer loses the obligation and rollback emits no committed outbox row. The relay can still publish duplicates after broker acceptance/before local acknowledgement; delivery can be delayed, reordered outside its defined scope, or fail at consumers. Stable identity, retry, ordering mechanics, backlog policy and consumer idempotency remain required.

### Answer 2

Store event ID, producer/tenant, type/schema version, order aggregate key, atomically assigned order version/sequence, occurrence/commit metadata, trusted destination, immutable canonical payload/fingerprint, lifecycle, attempts/next eligibility and claim owner/generation. `OrderPaid` at sequence 8 and `OrderRefunded` at 9 preserve content from those transitions. All retries preserve event ID, sequence and bytes while creating new attempt/broker identities.

Route the stable order key to one ordered broker partition. The relay must not let sequence 9 overtake eligible 8 for the same key, or consumers must buffer/reject gaps under a bounded recovery policy. Consumers treat repeated sequence/ID as duplicate, lower version as stale, and higher-than-next as a gap requiring wait/query/reconciliation. Cross-order events may interleave; no global order is promised.

### Answer 3

Mark-before-publish loses records after a crash. Mark only after broker acknowledgement and accept duplicate attempts with stable event ID/content. Index pending/eligible time plus ordering/claim keys, poll adaptively in bounded batches, and monitor query cost. Claim using short skip-locked transactions or leases, release database locks before network I/O, then acknowledge conditionally by owner/generation so stale workers cannot corrupt state.

Replace global timestamp claims with a named order key and atomic per-key sequence routed through a compatible relay/broker lane. Delete only after specified acknowledgement/reconciliation/replay delay, in bounded cleanup batches. Tests inject crash at each claim/publish/ack boundary, concurrent/stale workers, equal/skewed timestamps, out-of-order transactions, broker delay/outage, cleanup races and restart. Oracles are no lost eligible intent, identical duplicate identity/content, preserved per-key sequence and bounded database/backlog impact.

### Answer 4

CDC/log tailing is attractive at 20,000/s because it avoids hot table scanning and can consume committed inserts efficiently. A mature database platform may already own replication slots/log retention/failover. Use an explicit outbox table so business event contracts are deliberate; configure key routing by aggregate and prove the connector/broker preserve per-key order. Stable IDs still cover duplicate snapshots/restarts.

The small messaging team is a serious operational cost: connector offsets, log retention, schema evolution, snapshots, failover and broker routing need ownership. A well-partitioned polling publisher may be simpler if measured database capacity and latency suffice, but requires indexes, claims, table lifecycle and no-overtake design. Run representative benchmarks and recovery drills for both. Choose CDC only with on-call/runbooks, lag budgets and reconciliation; choose polling if its measured cost is acceptable and ownership is clearer. Neither changes consumer idempotency or global-order limits.

### Answer 5

Commit authorized device-command intent and outbox record atomically with stable command ID, tenant/device/generation, signed canonical payload reference/bytes, safety classification, issue/not-before/expiry semantics and per-device sequence. Broker outage grows measured count/bytes/oldest age. Reserve database and critical-command/reconciliation capacity; reject new nonessential commands before the budget, and stop accepting commands whose safe delivery deadline cannot be met. Expiry prevents future execution but does not erase an already issued ambiguous effect.

Relay credentials are device/topic allow-listed; commands are signed, replay-protected and fenced by device generation. Publish-before-mark uses stable IDs; destination acknowledgement and signed device read-back are distinct evidence. Quarantine invalid/expired commands with owned review. Cleanup retains audit and deduplication horizons. Recovery prioritizes safety/reconciliation, preserves per-device order, and paces backlog so live control and devices are not flooded.

Tests cover transaction rollback, outage to capacity threshold, clock/expiry edges, duplicate/reordered commands, stale generation, relay crash after acceptance, credential/key rotation, device acknowledgement loss, repair and paced recovery. Named controls/device, functional-safety, security, reliability/operations, field-service and regulatory reviewers define fail-safe behavior, command expiry, acceptable late execution, repair authority and evidence. Automated publication success alone cannot establish physical safety.
