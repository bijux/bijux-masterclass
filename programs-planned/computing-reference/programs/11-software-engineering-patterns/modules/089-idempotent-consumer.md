---
module_id: SEPAT-089
program: Software Engineering: Patterns
level: 2
module_number: 89
title: Idempotent Consumer
status: complete
last_verified: 2026-08-29
---

# Idempotent Consumer

## One-Page Review

### Governing question

How can a consumer safely receive the same logical message more than once—concurrently, after crashes, or during replay—while committing the intended business effect once per defined effect identity?

### Essential definitions

- An operation $f$ is **idempotent** over a stated domain when $f(f(x))=f(x)$; in messaging the required property is usually one logical durable effect, not one handler invocation.
- A **logical message/event identity** is stable across transport redeliveries and producer relay retries.
- An **effect identity** scopes deduplication to consumer/effect name, effect version and logical event/business identity.
- An **inbox** is durable consumer-side evidence that a named effect processed an identity with a specific input fingerprint and outcome.
- A **duplicate delivery** repeats one logical event, even if broker offset, delivery tag, attempt and trace differ.
- A **semantic duplicate** describes the same business intent under different message IDs; transport-ID deduplication alone cannot detect it.
- A **natural idempotent effect** converges under repetition by its own conditional/set/version semantics.
- An **atomic inbox/effect transaction** commits deduplication evidence and the local business mutation together.
- An **in-progress record/lease** coordinates long-running work but does not prove completion; stale attempts require recovery/fencing.
- **deduplication retention** is how long identity/effect evidence remains authoritative relative to redelivery/replay horizons.

### Central model, mechanism, or theorem

For consumer $c$, effect version $v$, logical event $e$, define

$$
k=(c,v,e).
$$

In one local serializable or adequately isolated transaction, attempt `insert inbox(k, fingerprint, outcome)` under a unique constraint and apply effect $E_k$. If the insert wins, commit both; if $k$ already exists with the same fingerprint, return the recorded outcome without reapplying; if the fingerprint differs, raise an integrity conflict. Therefore concurrent/redelivered attempts converge to one committed local effect per $k$, assuming all effect writes and inbox evidence share the transaction. Broker acknowledgement occurs afterward and may be repeated.

### Critical invariants

- Deduplication keys use stable logical identity, not delivery attempt, offset alone, or trace ID.
- The key is scoped so independent consumers/effect versions do not suppress each other.
- Duplicate identity with different canonical input is an integrity failure, not “already processed.”
- Inbox insert and every local business/projection mutation commit or roll back together.
- Broker settlement/offset acknowledgement happens only after local commit and may be retried safely.
- Concurrent duplicates are arbitrated by a unique constraint/conditional write, not a racy read-then-insert.
- `in_progress`, `completed`, `failed`, `expired` and outcome-unknown states are not conflated.
- External effects have their own stable downstream key or are emitted through an outbox in the inbox/effect transaction.
- Retention covers maximum producer retry, broker redelivery, backup restore and authorized replay horizon—or replay uses a new effect namespace.
- Replays declare effect version and side-effect policy; rebuilds cannot resend email, charge or device commands accidentally.

### Common failures

Common failures include acknowledging before commit; writing inbox then effect in separate transactions; applying effect then writing inbox; checking an in-memory set; read-before-insert races; keying only by broker offset; keying only by event ID across independent consumers; accepting conflicting content under one ID; deleting inbox records too early; treating set insertion as proof that every downstream call succeeded; calling a payment provider inside the local transaction; retrying with a new downstream key; caching permanent failures as success; batch-acknowledging uncommitted records; replaying side effects; resetting dedupe state during migration; and interpreting a broker's “exactly once” scope as proof about an external database.

### Compact example

`AccountDebited(evt-51, €7)` is delivered twice concurrently to `balance-projection:v3`. Both attempt to insert inbox key `(balance-projection,v3,evt-51)` and decrement the projection in the same database transaction. The unique constraint lets one commit; the other reads the same fingerprint/outcome and returns duplicate-success. The offset is acknowledged only after commit. If v4 intentionally rebuilds a different projection, it uses a new effect namespace and suppresses external notifications during replay.

### Connections

[SEPAT-088](088-transactional-outbox.md) provides stable producer event identity and at-least-once publication, [SEPAT-081](081-retry-with-bounded-backoff.md) constrains retries, [SEPAT-061](061-message-channel.md) establishes the delivery boundary, and [SEPAT-069](069-dead-letter-channel.md) retains poison-message evidence. The successor [Combining Resilience Patterns Without Failure Amplification](../ROADMAP.md) composes retry, deadlines, breakers, limits, outbox and idempotency without multiplying work.

## Governing Question

How should a message consumer distinguish delivery attempts from logical effects, bind duplicate evidence to local state atomically, handle concurrency and replay, and extend idempotency across external systems whose transactions it does not control?

At-least-once delivery is often the useful reliability choice: if a consumer crashes after its local commit but before acknowledging the broker, the broker redelivers. Avoiding redelivery by acknowledging first risks loss. The Idempotent Consumer pattern makes repetition an expected input and establishes a durable “already produced this effect” decision.

## Why This Matters

Duplicate delivery is not rare exceptional behavior. It arises from lost acknowledgements, consumer restart, lease/visibility timeout, partition rebalance, producer outbox retry, broker replication uncertainty, operator replay, backup restore and connector migration. Two consumers may receive the same logical record concurrently. A handler can finish its database transaction while the runtime reports failure.

Some repeated operations happen to converge: assigning `status=paid` with a monotonic version may be naturally idempotent. Others are not: `balance -= 7`, append history, increment counter, send email, issue refund or activate device will multiply effects. Even a naturally idempotent database update can surround non-idempotent notifications.

“Exactly once” is meaningful only when its boundary is named. A broker can atomically consume and produce within its own log yet cannot by itself make an arbitrary payment API or SQL database effect once. The consumer must couple its progress evidence to the effect system, or make the downstream operation idempotent under a stable key.

## Prerequisites and Retrieval

Learners should retrieve:

- functions, state transitions and algebraic idempotence;
- at-most-once, at-least-once and scoped exactly-once delivery;
- local database transactions, unique constraints and conditional writes;
- message/event, attempt, offset, consumer group and effect identities;
- broker acknowledgement, visibility locks, partition assignment and batching;
- Transactional Outbox, external idempotency keys and reconciliation;
- ordering, versioning, replay, retention and schema compatibility;
- authentication, tenant isolation, audit and privacy.

Before continuing, explain why processing a message, committing a database update, then crashing before broker acknowledgement must be safe to repeat.

## Learning Objectives

After this module, learners can:

1. distinguish handler invocation, delivery, logical event and committed effect;
2. choose a correctly scoped stable effect key and input fingerprint;
3. derive why inbox and local effect must share one transaction;
4. use uniqueness/conditional writes to arbitrate concurrent duplicates;
5. compare natural idempotence, inbox tables, embedded identity and offsets-with-output;
6. model in-progress, completed, retryable, permanent and ambiguous outcomes;
7. extend idempotency to external effects using downstream keys or outbox;
8. design batch, ordering, replay, effect-version and retention semantics;
9. observe and reconcile duplicate handling without leaking sensitive data;
10. verify crash/concurrency/security boundaries and state residual limitations.

## Core Exposition

### Define the effect, not merely the handler

The equation $f(f(x))=f(x)$ is useful but incomplete for distributed consumers. What is $x$? What counts as the same invocation? Which effects are observed? For a consumer, define:

- logical input identity and canonical fingerprint;
- consumer/effect name and version;
- local target entity/projection/version;
- all durable changes, including audit and outbound messages;
- returned/recorded outcome on duplicate;
- time horizon and replay namespace.

A function that sets one column idempotently but sends an email on every call is not idempotent over its actual effect surface. A handler that is safe for exact duplicate bytes may not be safe for two different event IDs representing the same order payment. Technical and semantic identity are separate design problems.

State a target such as: “For authenticated producer `billing`, event ID `evt-51`, consumer `balance-projection`, effect version 3, exactly one projection delta is committed; all exact duplicates return the recorded result; conflicting reuse of the ID is quarantined.” This is testable.

### Why acknowledgements create redelivery

If a consumer acknowledges before applying its effect, a crash between acknowledgement and effect loses work: at-most-once behavior. If it applies the effect before acknowledgement, a crash between them causes redelivery: at-least-once behavior. Unless broker progress and target effect share one transaction, no ordering eliminates both risks.

For required work, prefer effect-before-acknowledgement and make the effect duplicate-safe. Broker settlement is transport evidence, not business-effect truth. On redelivery, the consumer consults its target/inbox and acknowledges only after seeing or committing the correct durable outcome.

Batch consumers complicate the boundary. Acknowledging a whole batch when only a prefix committed can lose the suffix. Options include one transaction for the batch, per-record acknowledgement/partial failure, or storing exact per-record effects plus a progress position atomically. Choose based on broker API and target transaction limits; never infer per-record success from handler return alone.

### Select stable identity and scope

Do not use delivery tag, receipt handle, attempt UUID, process ID or trace ID: these usually change on redelivery. Broker topic/partition/offset can identify one immutable log record within one broker history, but may not survive republishing, migration, restore or producer outbox duplicates that occupy different offsets. Prefer the producer's stable event/message ID with authenticated producer/tenant namespace.

Deduplication scope includes the effect. A single event may legitimately drive inventory, billing projection and analytics. Global `event_id` uniqueness across all consumers would let the first suppress the others. A useful key is:

$$
(producer, tenant, consumer, effect\_version, event\_id).
$$

Sometimes business intent identity is required. Two producers might issue different event IDs for one payment authorization; a provider effect key derived from `merchant + order + authorization-purpose` prevents duplicate charge. Keep transport event ID for audit and detect the producer defect rather than hiding it.

Record a canonical input fingerprint. If the same key arrives with different amount, tenant, entity or type, silently returning the old result masks corruption or attack. Quarantine and alert. Canonicalization must be versioned and unambiguous; signatures/producer authentication bind identity to content.

### Couple inbox and local effect atomically

Suppose inbox insertion and balance update are separate:

- inbox first, crash, then duplicate skips an effect that never happened;
- effect first, crash, then duplicate repeats the effect.

The solution is one local transaction containing both. A typical flow is:

1. authenticate/validate envelope, type, schema, tenant and fingerprint;
2. begin target-store transaction;
3. insert inbox key under a unique constraint/conditional put;
4. if inserted, validate business preconditions and apply all local effects;
5. record stable outcome/result metadata;
6. commit;
7. acknowledge broker.

If the key already exists, compare fingerprint, effect version and recorded outcome. Completed success returns duplicate-success. A permanent rejected outcome may also be replayed if the contract defines rejection as processed; a transient/aborted attempt must not be mistaken for success.

Do not implement `SELECT then INSERT` without uniqueness. Concurrent deliveries can both observe absence and both mutate. Let the database arbitrate with a unique key or conditional write. Handle constraint conflict by reading the winning record. Required isolation depends on effect: uniqueness prevents duplicate inbox rows, but business invariants may require entity version/locks too.

### Inbox schema and lifecycle

A robust record can contain producer/tenant, consumer/effect version, event ID, canonical fingerprint, target entity/version, state, result/reference, first/last seen, completion time, delivery count, source coordinates, schema/type and safe error/repair metadata.

For short atomic database work, inserting only on successful commit is simpler: failed transactions leave no completed inbox record and the broker retries. Long-running work may need `in_progress`, ownership lease/generation and a durable workflow. Then define recovery:

- a live duplicate observes in-progress and waits/retries without duplicating work;
- expired lease permits takeover with a higher fencing generation;
- stale worker cannot commit an external/local conflicting effect;
- unknown downstream result enters reconciliation rather than new action;
- completion stores the response/evidence before acknowledgement.

A timeout is not safe evidence that the prior worker or provider did nothing. “Delete in-progress and retry” can duplicate an effect. Query by stable downstream identity or escalate.

### Natural idempotence and monotonic state

Prefer effects that converge intrinsically where domain semantics allow:

- upsert entity version 8 only if current version < 8;
- add event ID to a set with unique membership;
- set a fact to a canonical value under a generation;
- compute a projection row deterministically from an authoritative version;
- use max/union/commutative semilattice-like updates for monotonic facts.

Contrast `balance = event.current_balance` at monotonic account version with `balance -= event.amount`. The first can ignore stale/duplicate versions but relies on authoritative complete snapshots and per-account order/validation. The second requires event identity deduplication and correct order because each unique debit is a delta. “Use an upsert” is not enough if an audit append or notification repeats.

Natural idempotence reduces inbox pressure but may still need evidence for conflicting payload, audit, replay and external effects. An embedded `last_event_id` works only for a single ordered stream; multiple producers/out-of-order events require a set, sequence window or separate inbox.

### Deterministic duplicate-effect trace

The following pure model receives two logical events with repeated delivery. An in-memory set models the uniqueness decision and the balance delta is applied once per event identity.

<!-- bijux-verify: {"id":"sepat-089-idempotent-effect","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"deliveries=evt-1,evt-1,evt-2,evt-1\nresults=applied,duplicate,applied,duplicate\nbalance=96\ninbox=credit-v1:evt-2,debit-v1:evt-1\n","stderr":""}} -->
```python
deliveries = [
    ("evt-1", "debit-v1", -7),
    ("evt-1", "debit-v1", -7),
    ("evt-2", "credit-v1", 3),
    ("evt-1", "debit-v1", -7),
]
balance = 100
inbox = set()
results = []

for event_id, effect_version, delta in deliveries:
    key = effect_version + ":" + event_id
    if key in inbox:
        results.append("duplicate")
    else:
        inbox.add(key)
        balance += delta
        results.append("applied")

print("deliveries=" + ",".join(item[0] for item in deliveries))
print("results=" + ",".join(results))
print("balance=" + str(balance))
print("inbox=" + ",".join(sorted(inbox)))
```

This execution proves exact sequential set/delta/output behavior for fixed inputs only. The set is not durable and there is no transaction, broker, concurrency, crash, authentication, fingerprint conflict, ordering, external effect, retention, replay or recovery.

### External effects reopen the dual-write problem

A local transaction cannot atomically include arbitrary email, payment, cloud-control or device APIs. If the handler commits inbox then calls externally, a crash can suppress the call on duplicate. If it calls then commits inbox, a crash can repeat the call.

Preferred strategies:

- use a downstream API that accepts a stable idempotency/effect key and returns the original result for identical retries;
- in the inbox/effect transaction, insert an outbound command into a transactional outbox; a dispatcher then retries with stable downstream identity;
- redesign so the external provider owns a queryable operation resource/state machine;
- if none is possible, record `outcome_unknown`, reconcile provider evidence, and use owned human review.

The downstream key should represent business effect, not delivery attempt. Verify provider key scope, payload-conflict behavior and retention: if the provider forgets keys after 24 hours but retries/recovery last 30 days, the guarantee expires. A successful HTTP response may be lost; query/replay with the same key.

### Failure classification and poison messages

Distinguish:

- duplicate completed input: return recorded outcome/acknowledge;
- transient technical failure before commit: roll back and retry with bounds;
- permanent schema/auth/business rejection: record/quarantine according to contract and avoid hot retry;
- conflicting identity/fingerprint: integrity/security incident;
- dependency unavailable: retry under deadline/budget or defer;
- local commit outcome unknown: query target transaction/effect evidence;
- external effect unknown: reconcile by downstream key;
- invariant violation/corruption: stop affected scope and escalate.

Dead-lettering stores failed delivery evidence; it does not mean the business effect is resolved. Redrive uses original logical identity and explicit effect version. Fixing poison data in place can make audit/replay ambiguous; retain original and a signed repair/transformation record.

### Ordering and duplicates interact

Idempotency does not make order irrelevant. `OrderShipped(v9)` before `OrderPaid(v8)` may violate a state machine even if both are unique. Consumers should use aggregate version/sequence where required:

- equal event ID/version is duplicate;
- lower committed version may be stale duplicate;
- next version applies;
- higher version is a gap to buffer/query/quarantine under a bound;
- conflicting event at one version is corruption.

Parallel partitions, retries and batch partial failure can reorder. A consumer can atomically store last sequence and effect for a single ordered entity stream, but only if no legitimate branching/multiple events share a version. Otherwise use a richer inbox and transition model. Do not indefinitely block an entire partition for one poison key without explicit availability trade-offs.

### Replay and effect versioning

Replay is intentional redelivery, often after code/schema changes. Reusing the old effect key means every historic event is skipped; deleting the inbox may repeat irreversible effects. Name the purpose:

- recovering the same lost target should preserve effect identity if exactly the same effect is missing and evidence supports repair;
- building projection v4 uses `projection:v4` and an isolated table/namespace;
- notifications, charges and device commands are disabled unless replay explicitly authorizes a new business effect;
- cutover occurs only after validation/reconciliation.

Effect version is semantic, not application release number. A code refactor with unchanged effect stays v3. A changed projection algorithm needing historical recomputation becomes v4. Store lineage so reviewers know which source events and effect definition produced a target.

### Retention and restore horizons

Deduplication evidence must outlive all legitimate repeats: producer retry/outbox retention, broker redelivery/retention, dead-letter redrive, disaster recovery restore, offline client/device synchronization and authorized replay. TTL chosen only to control cost turns old duplicates into new effects.

If indefinite evidence is too expensive, use compact per-entity version/high-watermark only where ordering guarantees make it sufficient; archive identity digests; partition by time with a strict replay policy; or make downstream business constraints independently prevent duplicate harm. Document the residual after expiry.

Backup restore is subtle: restoring the effect database to yesterday while the broker resumes today's offsets can either lose or repeat effects. Recovery planning coordinates target snapshot, inbox, source/broker positions and producer evidence, then reconciles before reopening consumption.

### Observability, security and verification

Measure received/applied/duplicate/conflict/retry/permanent/unknown counts, commit latency, in-progress age, unique-conflict rate, inbox size/retention, sequence gaps, broker lag, dead-letter/redrive and downstream idempotency outcomes. Bound labels; do not expose full event IDs or tenant payloads in high-cardinality telemetry. Durable inbox/target/provider facts—not logs/traces—are recovery truth.

Authenticate producer and bind tenant, event ID, type/schema, effect target and fingerprint. Otherwise an attacker can pre-seed an inbox key to suppress a legitimate event, reuse an ID with altered amount, cross tenants, or force unbounded unique-key storage. Authorize the effect independently; replayed old authorization claims may be expired/revoked. Encrypt/minimize inbox result data and apply retention/legal policy.

Verification injects failure before/after inbox insert, effect mutation, local commit, broker acknowledgement and downstream call. Run concurrent duplicates, conflicting payload, duplicates after TTL boundary, partition rebalance, batch partial failure, out-of-order/gap events, poison redrive, backup restore and replay versions. Assert one local effect per key, no inbox-without-effect/effect-without-inbox, correct recorded result, no unintended replay side effects and explicit unresolved ownership. Integration tests must exercise actual database constraints/isolation and deployed broker/provider semantics.

## Definitions and Notation

Let logical event $e$ have authenticated producer/tenant $p,t$, canonical fingerprint $h(e)$, and zero or more transport deliveries $d_{e,1},d_{e,2},\ldots$. Let consumer/effect definition be $c,v$, giving key $k=(p,t,c,v,e)$. Let inbox state $I_k$, local target transition $E_k:x\to x'$, broker acknowledgement $A_d$, and downstream effect identity $u_k$.

Idempotence is claimed over the observable effect surface and retention horizon: repeated valid deliveries for $k$ with the same fingerprint yield the same committed local result without additional effect. This does not imply one invocation, one broker record, no errors, global ordering, or idempotence after evidence expires.

## Mechanisms, Invariants, or Proof Structure

**Atomic local effect.** Unique inbox insertion and target mutation in one local transaction permit only one committed winner for $k$; losers observe the winner. If either is outside the transaction, a crash counterexample creates suppression or repetition.

**Conflict safety.** Storing/checking $h(e)$ makes same-key/different-content visible. Without a fingerprint, identity collision or malicious reuse silently returns an unrelated result.

**Acknowledgement safety.** Acknowledge after committed outcome. Crash after commit/before acknowledgement creates a duplicate, which the inbox absorbs. Acknowledge before commit has an unrecoverable loss window.

**Concurrent arbitration.** A database unique constraint/conditional write linearizes competing inserts for $k$. A read-before-write check without such arbitration admits two winners.

**External composition.** Atomic inbox/effect/outbox plus a downstream stable idempotency key extends one logical effect across another boundary under downstream retention/query assumptions. The local inbox alone cannot prove the external effect.

**Ordered effect.** For a named entity stream, atomic sequence check plus mutation can reject duplicates/stale versions and identify gaps. Idempotency handles repetition; it does not commute distinct unique events.

**Liveness.** Transient failures retry; permanent/conflicting/ambiguous cases enter explicit terminal or reconciliation states. Infinite hot retry is not a liveness proof, and manual review is legitimate owned progress when automation cannot decide.

## Alternatives and Trade-Offs

| Alternative | Prefer when | Limitation or cost |
|---|---|---|
| naturally idempotent conditional update | target semantics truly converge under repetition | may omit audit/external effects and conflict evidence |
| separate inbox table | many effects/entities need uniform evidence | storage/index/retention and transaction contention |
| embed processed IDs in entity | duplicates are scoped to one entity and set is bounded | entity growth, multi-entity effects, query/update complexity |
| store last sequence/version | one complete ordered stream per entity | gaps, branches, migration/republish and out-of-order limits |
| store broker offset with output | one partition/output store can commit atomically | transport coupling; republish/migration and multi-source complexity |
| broker transactional consume-produce | input offsets and outputs remain in supported broker scope | external database/API effects outside transaction |
| downstream idempotency key | provider offers durable same-input/same-result semantics | scope/retention/conflict/query behavior may be limited |
| inbox plus outbound outbox | external call must survive crash asynchronously | more state, relay latency, duplicates and operations |
| at-most-once acknowledgement first | loss is preferable to repetition | unsuitable for required effects |

## Failure Modes and Misconceptions

- **Idempotent means handler executes once.** Invocations can repeat; the defined effect converges.
- **Every duplicate has the same broker offset.** Producer retries/republish can create new records.
- **Event ID alone is the key.** Independent consumers/effect versions need scope.
- **Same ID always means same input.** Fingerprint conflict must fail visibly.
- **Check then insert is safe.** Concurrent duplicates race without uniqueness/conditional write.
- **Inbox first is safe.** A crash can suppress an uncommitted effect.
- **Effect first is safe.** A crash can repeat it.
- **In-memory cache is evidence.** Restart, eviction and multiple instances defeat it.
- **Database idempotence covers email/payment.** External systems create another dual-write boundary.
- **Timeout means the provider did nothing.** Outcome can be ambiguous.
- **Idempotence fixes ordering.** Two different unique events may not commute.
- **TTL is harmless cleanup.** Later duplicate/redrive can become a new effect.
- **Replay means delete inbox.** That can repeat irreversible effects.
- **Exactly-once broker covers external storage.** Scope and atomic target cooperation matter.
- **Dead-letter means processed.** It preserves unresolved evidence only.

## Worked Examples

### Example 1

`AccountDebited(evt-1, 7)` is delivered three times. A delta update without inbox produces `100→93→86→79`. Inbox key `(balance,v1,evt-1)` plus the delta in one transaction yields `100→93`; later deliveries return recorded success. The conclusion is that non-idempotent deltas require identity-based effect arbitration.

### Example 2

Two workers concurrently query “evt-1 absent,” then both decrement before inserting. A procedural pre-check fails. A unique inbox constraint inside the target transaction lets one insert/mutate; the other transaction conflicts and reads the winner. Concurrency safety comes from atomic arbitration, not timing.

### Example 3

The consumer inserts inbox success, crashes, and never updates the projection because the operations used separate transactions. Redelivery sees the key and skips forever. Combining inbox and projection in one transaction removes the inbox-without-effect state; rollback leaves both absent.

### Example 4

Event ID `evt-9` first says tenant A amount 10, then a forged delivery says tenant A amount 1,000. A consumer that checks only ID hides the attack. It verifies producer signature/tenant and compares canonical fingerprint; the conflict is quarantined and alerts without mutating or acknowledging as ordinary duplicate.

### Example 5

Projection v3 has processed all history. A new algorithm needs v4. Deleting v3 inbox rows risks emails embedded in old code; reusing v3 keys skips rebuild. The team creates isolated `projection:v4` effect identity/target, disables external side effects, replays, reconciles, then switches reads. Effect version represents semantic output.

### Example 6

A handler records inbox then calls a payment API. It crashes before the call; duplicate skips it. Reversing calls payment twice after a lost response. The corrected local transaction records inbox state plus an outbound payment command; dispatcher uses stable provider idempotency key and reconciles ambiguous results.

### Example 7

A batch of ten records commits effects for six, fails on seven, yet acknowledges all ten. Records seven through ten are lost. The consumer uses per-record partial acknowledgement or stores exact per-record results/offset progress with output atomically, then retries only uncommitted identities. Batch success must reflect durable granularity.

### Example 8

`OrderShipped(v9)` arrives before missing `OrderPaid(v8)`. Both IDs are unique, so pure dedupe would apply both in wrong order. The consumer stores per-order version, detects gap 8, defers/queries under a bound, then applies 8 and 9. Idempotency and ordering are orthogonal.

### Example 9

Inbox TTL is seven days, but dead-letter redrive occurs after thirty. The same refund event becomes “new” and refunds twice. Retention is extended to the full replay/restore horizon, or a permanent business uniqueness constraint/provider key prevents duplicate refund; policy documents any residual beyond retention.

### Example 10

A device activation acknowledgement is lost. The message redelivers after the local inbox says “command dispatched,” but physical result is unknown. The consumer queries signed device generation/state using the same command ID, fences stale commands and escalates disagreement. Named safety/device/operations reviewers define whether retry, deactivation or inspection is acceptable; an inbox row alone cannot prove physical state.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md): business identity, aggregate invariants and effect semantics define idempotency scope.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): effect boundaries, asynchronous coupling and external ownership.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): concurrency, crash, replay, restore and metamorphic duplicate tests.
- [Database Engineering](../../18-database-engineering/ROADMAP.md): unique constraints, isolation, conditional writes, atomic inbox/effect and retention.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): authenticated identity, conflict/replay attacks, tenant isolation and durable-data privacy.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): delivery semantics, acknowledgement ambiguity, ordering, fencing and end-to-end scope.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): consumer runtimes, broker settlement, lag/dead-letter operations and recovery tooling.

## References

1. Richardson, Chris. “Pattern: Idempotent Consumer.” *Microservices.io*. <https://microservices.io/patterns/communication-style/idempotent-consumer.html>
2. Richardson, Chris. *Microservices Patterns*, 2nd ed. Manning, 2025.
3. Apache Kafka Authors. “Design: Message Delivery Semantics and Transactions.” <https://kafka.apache.org/design/>
4. Apache Kafka Authors. “KafkaConsumer: Storing Offsets Outside Kafka.” <https://kafka.apache.org/documentation/#consumerapi>
5. Amazon Web Services. “Designing Lambda Applications: Implement Idempotency.” <https://docs.aws.amazon.com/lambda/latest/dg/concepts-application-design.html>
6. Amazon Web Services. “Understanding Retry Behavior in Lambda.” <https://docs.aws.amazon.com/lambda/latest/dg/invocation-retries.html>
7. Microsoft. “Prevent Message Loss and Duplicate Processing in Azure Service Bus.” <https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-message-loss-and-duplicates>
8. Helland, Pat. “Idempotence Is Not a Medical Condition.” *ACM Queue* 10(4), 2012. <https://queue.acm.org/detail.cfm?id=2187821>
9. Hohpe, Gregor, and Bobby Woolf. *Enterprise Integration Patterns*. Addison-Wesley, 2003.
10. Kleppmann, Martin. *Designing Data-Intensive Applications*. O'Reilly, 2017.
11. Gray, Jim, and Andreas Reuter. *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann, 1992.
12. Bailis, Peter, et al. “Highly Available Transactions: Virtues and Limitations.” *Proceedings of the VLDB Endowment* 7(3), 2013. <https://www.vldb.org/pvldb/vol7/p181-bailis.pdf>

Official Kafka, AWS and Azure delivery/idempotency guidance was checked on 2026-08-29. Exact offset transactions, duplicate-detection windows, visibility locks, batch settlement and provider idempotency behavior are version/service/configuration specific and must be verified against the deployed systems.

## Exercises

### Exercise 1

Define an effect key and atomic processing transaction for a balance projection consuming `AccountDebited`, and state how exact duplicate and conflicting duplicate deliveries behave.

### Exercise 2

Trace crashes for (a) acknowledge then effect, (b) effect then acknowledge without inbox, and (c) atomic inbox/effect then acknowledge. Classify loss and repetition risk.

### Exercise 3

Diagnose a consumer that uses an in-memory event-ID set, read-before-insert, seven-day TTL, global event-ID scope, and a payment call after inbox commit. Redesign and specify decisive tests.

### Exercise 4

Design a safe replay from projection v2 to v3 while the live consumer continues, including identity, target isolation, ordering/gaps, external side effects, validation and cutover.

### Exercise 5

Design idempotent consumption for high-stakes remote device configuration with concurrent redelivery, command expiry, ambiguous acknowledgement, restore and manual intervention.

## Answers to the Exercises

### Answer 1

Use authenticated `(producer, tenant, balance-projection, effect-v1, event-id)` plus a canonical fingerprint covering account, debit amount/currency, source account version and event type/schema. In one projection-database transaction insert the inbox key under a unique constraint, check expected account sequence/business invariants, apply one balance delta/audit entry and store result projection version. Commit, then acknowledge.

An exact duplicate with the same fingerprint reads the completed outcome and acknowledges without another delta. A concurrent duplicate loses the unique-key race and reads the winner. Same key with different account/amount/version/fingerprint is quarantined as integrity/security conflict, not acknowledged as ordinary duplicate. Gaps/out-of-order unique events follow a separate sequence policy.

### Answer 2

(a) Acknowledge then effect: crash after acknowledgement prevents redelivery, so the effect is lost—at-most-once risk. (b) Effect then acknowledge without inbox: crash after effect/before acknowledgement redelivers and repeats a non-idempotent effect—at-least-once delivery with unsafe duplicate effect.

(c) Atomic inbox/effect then acknowledge: crash before commit leaves neither and retry applies; crash after commit/before acknowledgement redelivers but finds the same inbox fingerprint/result and skips mutation; crash after acknowledgement is already complete. Thus one local effect per key holds under uniqueness/transaction assumptions, though external effects, retention expiry and conflicting IDs remain separate.

### Answer 3

In-memory evidence disappears/repeats across restart and is inconsistent across instances. Use a durable target-store inbox. Read-before-insert races; insert under a unique constraint/conditional transaction. Global event-ID scope suppresses independent consumers, so include producer/tenant/consumer/effect version. Compare fingerprint. Set retention from maximum producer/broker/DLQ/replay/restore horizon; seven days is safe only if all repeats are impossible after it or another business constraint remains.

The payment call after inbox commit has a lost-call window. Commit an outbound payment command with the inbox/local effect using Transactional Outbox, then dispatch using a stable provider business-effect key and reconcile ambiguous responses. Tests cover restart/multiple instances, simultaneous duplicates, conflicting payload, crash before/after local commit/ack/outbox dispatch/provider acceptance, TTL boundary/redrive, provider key expiry and backup restore. Assert one local and provider effect, stable result and explicit unknown/escalation.

### Answer 4

Keep v2 live and immutable. Create effect identity `projection:v3`, isolated v3 target and separate inbox/sequence evidence. Replay authenticated immutable history in per-aggregate order; detect duplicates, conflicts and gaps. Suppress email, payment, webhooks and device commands by an enforced replay mode—not a convention. If v3 needs new derived events, write to a quarantined validation outbox until approved.

Capture a source high-watermark, consume historical data to it, then tail live events using the same v3 identity. Reconcile entity counts, versions, invariants, sampled/full computed values and source-event coverage. Test duplicate/reorder/gap, code restart and schema evolution. Cut reads gradually after validation; preserve v2 rollback until acceptance. A code refactor alone does not require v3, while changed output semantics do. Never delete v2 dedupe evidence merely to force replay.

### Answer 5

Key the effect by authenticated tenant/device, command purpose, device generation/configuration version and stable command ID; store canonical signed fingerprint. A durable state machine distinguishes received, validated, dispatch-pending, issued, outcome-unknown, observed-applied, rejected, expired and manual-review. Local inbox/state/outbound command commit atomically. Concurrent consumers arbitrate by unique key and fencing generation; device rejects stale generation/replay.

Expiry prevents not-yet-issued unsafe work but cannot prove an issued command did not apply. Dispatcher retries with the same command ID; lost acknowledgement triggers signed device read-back/telemetry reconciliation. Conflicting evidence or unreachable device enters owned field/manual review rather than a new ID. Recovery aligns restored inbox/state with broker positions and observed device generation before reopening.

Tests inject concurrent duplicates, crash at every local/outbox/device boundary, delayed command beyond expiry, stale worker, signature/tenant conflict, acknowledgement loss, device reboot, key rotation, broker/database restore and operator replay. Named controls/device, functional-safety, security, reliability/operations and field-service reviewers define safe retry, read-back authority, fail-safe state and intervention. One inbox record does not establish physical correctness.
