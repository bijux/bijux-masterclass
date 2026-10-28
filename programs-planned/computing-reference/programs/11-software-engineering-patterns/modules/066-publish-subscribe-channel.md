---
module_id: SEPAT-066
program: Software Engineering: Patterns
level: 2
module_number: 66
title: Publish-Subscribe Channel
status: complete
last_verified: 2026-08-29
---

# Publish-Subscribe Channel

## One-Page Review

### Governing question

How can one publication become independently consumable by multiple interested subscriber groups while making subscription membership, durability, retention, filtering, delivery/effect semantics, ordering, lag, backpressure, schema evolution, security, cost, and terminal failure explicit?

### Essential definitions

- A **Publish-Subscribe Channel** accepts one message and makes a copy/logical delivery available to each interested subscriber.
- A **topic/subject** names the publication stream; a **subscription** is one independently governed interest and delivery state.
- A **consumer group** shares one subscription's work among competing consumers; it is not an additional logical subscriber.
- A **transient subscriber** receives only while attached under the product's live-broadcast semantics.
- A **durable subscriber** retains an obligation/checkpoint while disconnected, subject to retention and expiry.
- A **retained log** stores publications independently of subscriber processing so groups can replay from positions.
- **fan-out** is the number of matched subscriptions/targets per publication; each creates independent cost and effect risk.
- A **subscription filter** selects a subset for one subscriber; its version and unknown/error semantics are part of that subscription contract.
- **lag** measures a subscriber group's progress behind retained publication, while **oldest age** captures time-to-processing risk.
- A **terminal subscription outcome** is confirmed processing, intentional filtered/expired/cancelled result, or owned unresolved/dead-letter work.

### Central model, mechanism, or theorem

For publication $m$ at time $t$, let $S_t$ be the snapshot of subscriptions and $match(s,m)$ each subscription's filter. The intended obligation set is

$$
O(m,t)=\{(m,s)\mid s\in S_t\land match(s,m)=T\},
$$

subject to declared transient/durable/retention semantics. For each obligation, delivery attempts $D_{m,s}$ and committed effects $E_{m,s}$ are independent. A typical at-least-once design targets

$$
D_{m,s}\ge1,\qquad E_{m,s}=1,
$$

but effect uniqueness requires subscriber-specific idempotency; one topic publication or broker acknowledgment cannot establish all $E_{m,s}=1$.

Fan-out delivery work for $N$ publications is approximately

$$
W=\sum_{m=1}^{N}|O(m)|,
$$

before retries, filtering implementation, replication, bytes, and downstream effects. Subscriber growth therefore changes capacity/cost without changing producer call count.

### Critical invariants

- Message type is a fact/document appropriate for independent reactions; commands with one decision owner are not accidentally broadcast.
- Topic, publisher, subscription owners, consumer groups, filter, durability, start position, retention, replay, and deletion are registered/auditable.
- Producer state plus publication uses outbox/transactional protocol where omission would violate the business contract.
- Each matched durable subscription owns its delivery, checkpoint/ack, retry, idempotent effect, dead letter, lag SLO, and recovery.
- One subscription's success/failure does not erase or falsely satisfy another's obligation.
- Schema/type/version, identity, partition key, provenance, and security classification remain stable across fan-out.
- Ordering claims name partition/subscription scope and account for concurrent consumers, retries, rebalance, and filters.
- Slow/broken subscribers are isolated through independent queues/positions, quotas, rate limits, and retention—not unbounded shared blockage.
- Publish/subscribe/filter/admin permissions and field-level purpose/tenant rules prevent broad unintended disclosure.
- Subscription and schema lifecycle handles creation, backfill, pause, deletion, ownership transfer, replay, corrections, and retained history.

### Common failures

Common failures include calling competing consumers pub/sub, broadcasting commands, assuming every subscriber was present, transient subscribers expecting replay, durable subscriptions with no owner, one ack treated as global success, non-idempotent subscriber effects, retention shorter than outage, slow group hidden by topic health, global ordering assumptions, filter changes silently skipping history, new subscriber replay causing irreversible effects, schema changes ignoring old retained messages, sensitive superset topics, wildcard subscriptions, publisher depending on unknown consumers, fan-out cost explosion, shared dead-letter queue without subscription provenance, and deleting a subscription to make lag disappear.

### Compact example

An in-memory topic snapshots two durable subscriptions—billing and search—while an inactive transient email listener creates no obligation. Billing acknowledges once. Search fails before ack, redelivers, uses a subscription-local processed identity to avoid a second effect, then acknowledges. Final result is two logical effects, one per durable subscription, despite three total delivery attempts.

### Connections

[SEPAT-065](065-content-based-router.md) supplies explicit subscription filtering semantics; [SEPAT-067](../ROADMAP.md) scales one subscription through Competing Consumers. Pub/sub connects to [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md), [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), [Platform Engineering](../../29-platform-engineering/ROADMAP.md), and [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

What exactly does a publisher promise to which subscriber populations, and how can every subscriber progress or fail independently without turning fan-out into invisible data loss, duplicated effects, privacy expansion, or unbounded operational debt?

Publish-subscribe decouples a producer from the number and identity of consumers. It does not remove semantic coupling: every subscriber depends on event meaning, schema, identity, timing, retention, and source authority. Nor does it make all downstream work one transaction.

## Why This Matters

One business fact can drive billing, search, audit, notifications, analytics, and automation. Pub/sub permits independent deployment, scaling, buffering, and recovery. New consumers can be added without changing producer logic.

Each subscriber creates another obligation and effect boundary. A broken subscription may lag for days while others succeed; a later replay may duplicate email or payment; a broad topic may disclose fields to teams that never needed them. The architecture is production-grade only when these obligations are owned and observable.

## Prerequisites and Retrieval

You should understand Message Channel, Message Router, Content-Based Router, event versus command semantics, publisher confirms, acknowledgements, outbox/inbox, idempotency, partitions/order, retention/replay, schemas, authorization/privacy, and capacity. Retrieve these facts:

1. One publication can lead to zero, one, or many subscription deliveries depending on subscription/filter/time semantics.
2. Consumer group members compete for one logical subscription; separate groups each receive their own logical stream.
3. Broker acceptance does not prove processing by any subscriber, much less all subscribers.
4. Consumer effect can commit before ack; redelivery then requires subscription-specific deduplication.
5. Retention bounds how long disconnected/new groups can read history; it is not infinite recovery.
6. Per-partition order does not create global order or identical effect order across groups.
7. Adding a subscription changes data disclosure, cost, capacity, and operational ownership even if publisher code does not change.

## Learning Objectives

After completing this module, you should be able to:

- distinguish pub/sub from point-to-point, competing consumers, recipient lists, broadcast, and retained logs;
- choose transient, durable queue-per-subscription, or log/group semantics for a use case;
- model subscription snapshots, filters, delivery attempts, effects, lag, retention, and terminal outcomes;
- design producer outbox and subscriber inbox/idempotency boundaries end to end;
- define ordering, partition, rebalance, retry, dead-letter, replay, backfill, and correction semantics per group;
- isolate slow subscribers and bound fan-out, message bytes, downstream concurrency, cost, and retention;
- evolve schemas and subscription filters across active and retained versions;
- authorize publishers/subscribers/fields/tenants/purposes and prevent wildcard or confused-deputy disclosure;
- instrument publication and each subscription's age, lag, delivery, effect, error, and recovery;
- verify with protocol models, real broker/database fault tests, load/skew/replay, security, and high-stakes human review.

## Core Exposition

### Publish facts, not ambiguous ownership

Events in past tense—`InvoiceIssued`, `OrderCancelled`—can support independent reactions. A command such as `ChargeCard` should normally have one owner; broadcasting it risks several processors performing the same decision. If several recipients must act, define separate commands/workflow or an event whose reactions are independently owned.

Document authoritative source and event occurrence. A producer should not tailor the fact to one consumer or wait for every unknown future subscriber synchronously.

### Identify the logical subscription

Name subscription by durable business responsibility (`search-index-invoice`, not deployment pod). Record owner/on-call, purpose, filter, consumer group, start position, durability, SLO, retry/dead-letter, schema support, permissions, capacity, and deletion process.

Instances within a group are replaceable competing workers. Creating a new group creates a new logical fan-out obligation; scaling instances does not.

### Choose live broadcast versus durable delivery

Transient broadcast suits ephemeral telemetry/UI hints where absence while disconnected is acceptable. Durable subscription/queue retains undelivered work. A retained log stores history and lets groups track offsets/replay. Product terminology varies; state actual semantics.

Do not assume a subscriber created after publication receives history. Define earliest/latest start, retention, compaction, snapshot/bootstrap, and gaps.

### Snapshot membership semantics

Specify whether obligation set is determined at publish time, by retained log availability when a group later subscribes, or by an explicit backfill. Subscription deletion can cancel unresolved obligations only under reviewed policy and audit.

Dynamic filters/version changes need an effective offset/time. Re-evaluating old history under new filters is a new backfill/reclassification operation, not ordinary retry.

### Close the producer publication gap

Write authoritative business state and outbox event in one transaction; relay same event identity until broker confirms. Reconcile old outbox rows. If omission is tolerable, state it rather than implying reliable propagation.

Publisher confirm ends at broker responsibility under configured durability. It neither waits for nor enumerates subscriber effects.

### Give each subscription an effect boundary

Subscriber validates/authenticates message, claims `(subscription_id,message_id)` in inbox or uses a naturally idempotent/versioned transition, commits effect and outgoing outbox, then acknowledges/checkpoints. Redelivery after uncertain ack finds prior claim and does not repeat effect.

Remote effects need idempotency keys/workflow/reconciliation. The same message may legitimately cause one effect in billing and another in search; dedupe scope must include subscription/operation.

### Isolate acknowledgements and progress

Billing ack cannot advance search. Each queue/group holds its own ack/offset and failure policy. Shared checkpoints among unrelated responsibilities couple releases and let one processor skip another's work.

Track processed effect, broker checkpoint, and derived publication separately where transaction scope differs. “Offset committed” is not always “all external work complete.”

### Define delivery semantics per subscription

At-most-once may lose work; at-least-once expects duplicates; ecosystem-specific transactions may atomically connect input offsets and output records within limited scope. State the exact systems and effects covered.

Do not advertise one global exactly-once property for arbitrary email/payment/search/HTTP effects. Use stable identities, idempotency, and reconciliation.

### Design filters as subscription policy

Filters reduce delivery/cost but create semantics: inspected scope, missing/null/unknown/error, version, effective point, and evidence. Server-side/broker filtering may discard nonmatches before subscriber sees them; ensure that is intentional.

Precise filters and message types reduce accidental matches. A broad wildcard can match future types/fields and expand privacy/cost. Test old/new messages and filter policies as in Content-Based Router.

### Preserve ordering honestly

Partition by scoped entity/key when transitions require order. Within a group, one partition is processed by one active member at a time under common log semantics, but rebalances/retries/effect concurrency can complicate observed outcomes. Different groups progress at different speeds.

Consumers validate entity version/gaps/duplicates; do not assume billing and search effects occur simultaneously or in one relative order. Global order limits throughput and rarely matches business need.

### Handle slow subscribers independently

One slow group should accumulate its queue/lag without blocking healthy groups, subject to broker storage and publisher quotas. Set per-subscription rate/concurrency/prefetch, retention, backlog/age limits, downstream capacity, and alerting.

Autoscaling can overload the effect database. Oldest age and business completion SLO matter more than depth alone. Define overload choices: scale, throttle, pause, shed explicitly permitted work, extend retention, or degrade.

### Govern retry and dead letters per group

Classify transient, throttled, conflict, malformed, unsupported, unauthorized, expired, and permanent domain failures. Bound retry with backoff/jitter/deadline. Quarantine/dead-letter retains subscription ID, original identity, attempt/evidence, and access controls.

One shared dead-letter channel can work only if provenance/ownership/routing are preserved. Redrive uses same logical identity, current authorization/applicability checks, rate limits, and reconciliation; it does not republish to every subscriber unless explicitly intended.

### Design retention and replay

Retention covers maximum expected outage, recovery rate, compliance/privacy/cost, and schema support. Compaction may preserve latest key state but discard event history; deletion can create gaps. Backups/restores and region replication add separate guarantees.

Replay read-model events may be safe under idempotent rebuilding; replay emails/payments/commands can be harmful. Classify event consumers as replayable, rebuild-only, live-effect, or requires explicit simulation/approval.

### Bootstrap new subscribers

A new subscriber may start from current point, retained beginning, a snapshot plus subsequent offset, or a governed backfill. Bind snapshot version/watermark and avoid gap/double application. Capacity-test catch-up without harming live traffic.

Authorize historical access separately; a new current purpose may not permit reading years of personal data.

### Evolve message contracts for independent consumers

Producer cannot know every subscriber deployment. Use versioned stable semantics, compatibility matrices, retained fixtures, and schema registry checks. Additive optional fields are safe only when absence and old-reader ignorance preserve correctness.

Track group-supported versions. Unknown critical fields/types route to review/fail closed rather than silent ignore. Retain translators/schemas for historical replay until no obligation needs them.

### Secure fan-out

Authenticate publisher and subscriber workloads; authorize topic publish, subscription creation/filter/admin, consume by group, tenant/partition, field/purpose, region and replay. Prevent producers from publishing another tenant/source and consumers from wildcard subscribing.

Minimize payload for the audience. Split topics/messages by sensitivity/purpose/retention instead of one canonical superset. Encrypt, rotate credentials/keys, protect offsets/DLQs/snapshots, audit access/config, and redact telemetry.

### Bound fan-out and cost

Model matched subscription count, delivery bytes, retention replicas, egress, retry, storage, and downstream effects. Subscription admission reviews projected rate/size/filter/catch-up/cost and owner capacity. Quotas and budgets prevent a wildcard group from destabilizing the platform.

Publisher throughput can be stable while total work grows with subscriptions. Monitor publish-to-delivery amplification.

### Manage subscription lifecycle

Creation requires owner/purpose/contract/security/capacity/recovery evidence. Pause retains or drops according to policy. Ownership transfer updates on-call and credentials. Deletion drains/cancels outstanding work, preserves audit, revokes access, handles dead letters/snapshots, and reconciles effects.

Never delete/recreate a group solely to clear lag unless data loss is explicitly approved and recorded.

### Observe producer and every group

Producer metrics: outbox age, publish attempts/confirms/failures, type/version/rate/bytes. Broker/topic: availability, storage/retention, partitions/skew, fan-out. Per group: position/lag, oldest age, delivery/redelivery, processing/effect/ack time, dedupe, retry/DLQ, filter rate, unsupported version, downstream saturation, reconciliation.

Use bounded topic/group/outcome labels; traces carry sampled IDs. Logs/DLQ evidence redact payload. Business SLO measures source decision to each required reaction, not topic availability alone.

### Test end-to-end fan-out

Unit/property-test envelope, filter, subscription identity, idempotency, versions/order/gaps, retry/expiry, snapshot+offset. Contract-test each group against old/new/historical fixtures. Integration-test real broker/client/database for topic/subscriptions/groups, ack/offset, retention, rebalances, durability, ACL/filter, DLQ and schema registry.

Crash producer around state/outbox/publish/confirm; crash each consumer around inbox/effect/ack; disconnect beyond retention; add/remove/pause subscriptions; change filter; replay/backfill; restore snapshots; rotate credentials. Load-test subscription count, skew, slow group, catch-up, retry storm and downstream limits. Reconcile every intended subscription/effect.

### Review high-stakes fan-out as disclosure and action

Clinical, financial, safety and regulatory facts may trigger several critical reactions. Define which groups are mandatory, timing/escalation, authority, current-state checks, unknown/unavailable behavior, privacy/purpose, and operator visibility. An optional analytics subscriber is not equivalent to mandatory safety response.

Named domain, affected-user, privacy/legal/regulatory, security, accessibility/human-factors and operations owners review real events/subscriptions/recovery. Broker fan-out tests cannot establish substantive safety.

### Executable model: independent durable obligations

The finite bus snapshots two active durable groups and ignores one inactive transient listener. Billing acknowledges once; search is redelivered but applies one subscription-local effect. It is not a durable/concurrent broker model.

<!-- bijux-verify: {"id":"publish-subscribe-obligations","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"published=e-1 obligations=billing,search\nbilling=acked search=pending email=none\nsearch_attempts=2 search=acked effects=2\n","stderr":""}} -->
```python
class Topic:
    def __init__(self):
        self.subscriptions = {
            "billing": {"durable": True, "active": True, "queue": [], "attempts": {}},
            "search": {"durable": True, "active": True, "queue": [], "attempts": {}},
            "email": {"durable": False, "active": False, "queue": [], "attempts": {}},
        }

    def publish(self, message):
        obligations = []
        for name, subscription in self.subscriptions.items():
            if subscription["durable"] or subscription["active"]:
                subscription["queue"].append(message)
                obligations.append(name)
        return obligations

    def deliver(self, name):
        subscription = self.subscriptions[name]
        message = subscription["queue"][0]
        message_id = message["id"]
        subscription["attempts"][message_id] = subscription["attempts"].get(message_id, 0) + 1
        return message

    def acknowledge(self, name):
        self.subscriptions[name]["queue"].pop(0)


topic = Topic()
obligations = topic.publish({"id": "e-1", "type": "invoice-issued"})
print(f"published=e-1 obligations={','.join(obligations)}")
effects = set()
billing_message = topic.deliver("billing")
effects.add(("billing", billing_message["id"]))
topic.acknowledge("billing")
topic.deliver("search")
print("billing=acked search=pending email=none")
search_message = topic.deliver("search")
effects.add(("search", search_message["id"]))
topic.acknowledge("search")
attempts = topic.subscriptions["search"]["attempts"]["e-1"]
print(f"search_attempts={attempts} search=acked effects={len(effects)}")
```

### Finite invariant argument

At publish, billing/search are durable and therefore receive one queued reference; email is neither durable nor active and receives none. Billing delivery records attempt one, applies pair `(billing,e-1)`, and ack removes its queue entry. Search first delivery records attempt one but remains pending. Second delivery reads same head and records attempt two; set insertion creates only `(search,e-1)`, then ack removes it.

Final effect set has two distinct subscription-scoped pairs; search duplicate attempt did not add another. The argument assumes serialized failure-free in-memory operations and manually placed effect/ack order; a crash between effect and durable inbox would break the real guarantee. It proves no retention, broker durability, concurrency, filtering, authorization, or external effect behavior.

### Evidence classification

The snippet report is empirical evidence for two obligations, absent transient delivery, independent ack state, search redelivery and two subscription-scoped effects. The trace is independently recomputable. It provides no real broker, database transaction, network, replication, schema, security, load, replay or exactly-once evidence.

## Definitions and Notation

Topic publication $m=(id,type,version,key,source,time,payload)$. Subscription $s=(id,owner,filter,durability,start,retention,group,delivery,security,SLO)$. Membership snapshot $S_t$ and obligation set $O(m,t)$ require product-specific subscription timing semantics.

$D_{m,s}$ counts attempts and $E_{m,s}$ committed domain effects scoped to subscriber operation. Group instances $c_{s,1},\ldots$ share obligation stream/position for $s$. Lag $L_s$, oldest age $A_s$, arrival rate $\lambda_s$, sustainable completion $\mu_s$, and retention horizon $H$ govern recoverability.

Publication fan-out $f(m)=|O(m,t)|$, total attempts include retries $W'=\sum_{m,s}D_{m,s}$, and effect count is not inferred from $W'$.

## Mechanisms, Invariants, or Proof Structure

Mechanism: producer transaction stores state/outbox; relay confirms one topic publication; broker snapshots/routes/retains per subscriptions; each group independently validates, claims `(s,m)`, commits effect/outbox, then acks/checkpoints; retries/DLQ/replay remain group-specific; reconciliation joins source event, topic, group positions/inboxes and effects.

Safety invariants include stable source identity/meaning; authorized matched obligation set; independent progress; no ack before durable group effect/claim; at most one logical effect per `(subscription,operation,message)` under idempotency; scoped ordering; bounded fan-out/resources; schema/security compatibility; and terminal evidence for each mandatory obligation. Liveness requires retention, availability, capacity, valid policy/schema/credentials and owned recovery.

Finite models prove local attempt/effect traces. Broker tests establish configured routing/durability/offset behavior. Database/fault tests establish inbox/effect/ack recovery. Load tests establish bounded capacity for a scenario. Security/domain/human review validates disclosure and reaction policy. None alone proves end-to-end global completion.

## Alternatives and Trade-Offs

| Approach | Recipients | Strong fit | Main risk |
|---|---|---|---|
| Point-to-point queue | One competing group | One owned background task | Not independent fan-out |
| Transient broadcast | Currently attached listeners | Ephemeral hints/telemetry | Disconnected loss/no replay |
| Durable queue per subscription | Registered groups | Independent reliable work | Queue/ops growth |
| Partitioned retained log/groups | Groups with offsets | Replay, projections, ordered keys | Retention/rebalance/schema complexity |
| Recipient List router | Computed recipients per message | Explicit bounded fan-out | Partial publication/policy coupling |
| Direct callbacks/webhooks | Registered endpoints | External integrations | Availability/retry/security coupling |
| Shared database polling | Readers discover changes | Controlled legacy | Coupling/missed-change/load semantics |

Hybrid is common: one retained domain-event log, filtered durable queues for operational consumers, and transient UI notifications derived downstream.

## Failure Modes and Misconceptions

- **“Pub/sub means everyone gets it.”** Only matched subscriptions under timing/durability/retention semantics do.
- **“Consumer instances are subscribers.”** Instances in one group compete for one logical stream.
- **“Publisher confirm means all consumers processed.”** It ends at broker responsibility.
- **“One ack completes the event.”** Every subscription has independent progress/effect.
- **“Exactly once applies globally.”** Arbitrary downstream effects require subscriber idempotency/reconciliation.
- **“New subscribers automatically get history.”** Only retained/backfilled data and authorized start positions permit it.
- **“Retention guarantees recovery.”** Recovery must finish before data disappears and schemas/credentials must still work.
- **“Filters are only optimization.”** They define which obligations exist and can silently drop new/unknown messages.
- **“Order is identical across subscribers.”** Groups progress/retry independently.
- **“A slow group cannot affect publishers.”** Shared broker storage/quotas/cost can eventually couple them.
- **“Replay is harmless.”** Live-effect consumers can resend money/email/actions.
- **“Delete the group to clear lag.”** That discards obligation/history and hides failure.
- **“One broad topic maximizes reuse.”** It expands disclosure, schema coupling, bytes and wildcard risk.
- **“Adding a subscriber is free.”** It adds delivery/effect/capacity/security/on-call obligations.
- **“Green broker tests prove business fan-out.”** Domain effects and mandatory reaction policy need stronger evidence.

## Worked Examples

### Example 1

**Situation.** `InvoiceIssued` feeds ledger, search and email groups.

**Reasoning.** Each group has independent inbox/effect/ack, retries, lag and DLQ. Email failure does not roll back ledger; mandatory ledger SLO differs from optional email.

**Conclusion.** One fact creates separate obligations with separate criticality.

### Example 2

**Situation.** Two pods in `search-index` group both expect every message.

**Reasoning.** They compete for partitions/work; together they implement one subscription. Create distinct group IDs only for independent logical reactions.

**Conclusion.** Scaling and fan-out are different axes.

### Example 3

**Situation.** An inactive transient websocket listener expects yesterday's events after reconnect.

**Reasoning.** Live broadcast has no durable history. Use snapshot/current state plus resume token/retained stream if catch-up is required.

**Conclusion.** Subscriber lifetime must match channel durability.

### Example 4

**Situation.** Search commits index update, crashes before offset commit, then redelivers.

**Reasoning.** Use event/version as idempotent index transition or durable inbox; acknowledge after effect boundary. Redelivery becomes no-op/reconciliation, not duplicate document.

**Conclusion.** At-least-once delivery requires group-scoped idempotency.

### Example 5

**Situation.** Billing lag is zero, notification lag is 2 million.

**Reasoning.** Topic health cannot summarize group health. Alert notification oldest age/downstream saturation and isolate its retry/capacity without disturbing billing.

**Conclusion.** Observe every subscription independently.

### Example 6

**Situation.** New subscriber starts at beginning and sends every historical welcome email.

**Reasoning.** Live-effect consumer is not replay-safe. Bootstrap from current position or run an effect-disabled backfill/snapshot with new approved operation semantics.

**Conclusion.** Replay policy belongs to consumer contract.

### Example 7

**Situation.** Subscription filter changes from EU to all regions with no review.

**Reasoning.** Disclosure, volume and downstream capacity expand; effective offset determines whether history is reclassified. Version, shadow, authorize, canary and reconcile.

**Conclusion.** Filter changes are policy deployments.

### Example 8

**Situation.** A subscriber is offline longer than seven-day retention.

**Reasoning.** Log gap cannot be retried from broker. Restore from authoritative snapshot/backfill plus watermark, or declare irrecoverable loss under policy and reconcile.

**Conclusion.** Retention and recovery time form one contract.

### Example 9

**Situation.** A wildcard audit subscriber receives health and payment payloads.

**Reasoning.** Topic consume permission does not prove purpose/field authorization. Split/minimize contracts, restrict wildcard/subscription creation, encrypt/audit and validate tenant/purpose.

**Conclusion.** Fan-out is also a disclosure operation.

### Example 10

**Situation.** A clinical critical-result event has notification, escalation, audit and analytics groups.

**Reasoning.** Notification/escalation are mandatory timed workflows with current patient/order/authority checks and accessible human acknowledgement; analytics is delayed/minimized optional. Track each separately and reconcile safety outcomes.

**Conclusion.** Subscriber criticality and semantics cannot be flattened into “delivered.”

## Cross-Program Connections

- [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md) develops logs, delivery, ordering, consistency, replication, failure, lag and recovery.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies event contracts, idempotency, asynchronous operations and consumer compatibility.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) operates topics, subscriptions, quotas, retention, schema registry, telemetry and disaster recovery.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies workload identity, topic/group ACLs, tenant/purpose/field authorization, privacy and audit.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) grounds outbox/inbox, uniqueness, projections, snapshots and reconciliation.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) provides protocol, contract, fault, replay, load, security and recovery evidence.
- [SEPAT-065](065-content-based-router.md) develops filters; [SEPAT-067](../ROADMAP.md) scales one group with competing workers.

## References

1. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns*, Addison-Wesley, 2003. Publish-Subscribe Channel, Durable Subscriber, Message Channel and related patterns.
2. Enterprise Integration Patterns, [“Publish-Subscribe Channel”](https://www.enterpriseintegrationpatterns.com/patterns/messaging/PublishSubscribeChannel.html), accessed 2026-08-29. Pattern problem, solution and implementation considerations.
3. Apache Kafka, [“Documentation”](https://kafka.apache.org/documentation/), current documentation accessed 2026-08-29. Topics, partitions, consumer groups, offsets, retention and delivery.
4. RabbitMQ, [“Publish/Subscribe tutorial”](https://www.rabbitmq.com/tutorials/tutorial-three-python), current tutorial accessed 2026-08-29. Exchange-based broadcast and per-consumer queues.
5. RabbitMQ, [“Consumer Acknowledgements and Publisher Confirms”](https://www.rabbitmq.com/docs/confirms), current documentation accessed 2026-08-29. Independent publisher/broker and broker/consumer responsibility boundaries.
6. NATS, [“Documentation”](https://docs.nats.io/), current documentation accessed 2026-08-29. Core publish-subscribe and JetStream persistence/consumer concepts.
7. Amazon Web Services, [“Subscribe API”](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html), accessed 2026-08-29. Subscription protocols, filters, delivery and redrive policy.
8. Amazon Web Services, [“SNS message delivery retries”](https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html), accessed 2026-08-29. Protocol-specific retry/backoff and DLQ behavior.
9. Clemens Vasters et al., [“CloudEvents Specification”](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md), current specification accessed 2026-08-29. Event identity, source, type, subject and time context.
10. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Logs, streams, partitioning, delivery, derived data and distributed failure.

## Exercises

### Exercise 1

Model one publication with four subscriber groups, two filters, one transient listener and a later-created group. Define exact obligation set, delivery/effect identities and timing/retention assumptions.

### Exercise 2

Design a durable pub/sub event for invoices. Specify producer outbox, three groups, idempotency, partition/order, filters, schema evolution, lag SLOs, retry/DLQ, replay and reconciliation.

### Exercise 3

Design bootstrap for a new search projection from snapshot plus retained log. Prove absence of gap/double application under stated watermark/offset protocol and plan failure recovery.

### Exercise 4

Diagnose a platform with wildcard topics, 400 ownerless groups, unbounded retention, shared DLQ, replayed emails and a database overwhelmed by autoscaling. Produce incremental governance/technical correction and evidence gates.

### Exercise 5

Review a high-stakes clinical-result pub/sub flow. Cover authoritative event, mandatory/optional groups, timing/current-state/unknowns, idempotency, order/corrections, privacy/purpose, accessible escalation, operations, verification and named human review.

## Answers to the Exercises

### Answer 1

At publish time snapshot registered durable groups A/B/C/D; filters match A, C and D, so obligations are `(m,A),(m,C),(m,D)`. B has an explicit filtered terminal result if broker records it, or simply no obligation under contract—state which. Active transient listener T receives a best-effort live copy but no durable obligation; inactive transient listener receives none. Group E created later receives history only if retained-log start/backfill explicitly includes this offset within retention and authorized purpose; otherwise none.

Stable event ID remains `m`; each group effect claim keys `(subscription_id, operation, m)`, delivery attempt IDs are separate. Retention must outlast allowed outage/catch-up; subscription/filter version/effective offset and membership control-plane consistency are premises. Publisher confirm proves broker acceptance only. Each A/C/D group independently commits effect/inbox before ack, and its failure/DLQ/lag does not satisfy another.

### Answer 2

Invoice service transaction stores invoice/version plus `InvoiceIssued` outbox with stable ID, tenant/invoice key, exact money/currency, occurrence/provenance and schema version; relay confirms topic publication. Ledger group is mandatory, inbox/transactionally writes versioned entries/outbox and has tight age SLO. Search group idempotently upserts invoice version and can replay/rebuild. Notification group uses stable notification idempotency and current consent/contact/state; replay is effect-disabled/explicit only.

Partition by tenant/invoice; consumers reject duplicates/stale and detect gaps/corrections. Filters are versioned, tested for missing/unknown and authorized fields. Schema compatibility covers retained fixtures and critical-field rollout. Each group has bounded retries, typed errors, protected DLQ owner/redrive, rate/concurrency sized to downstream and oldest-age alerts. Reconcile source outbox/topic, group offsets/inboxes, ledger/search/notification outcomes and correction lineage; crash-test every commit/confirm/ack boundary and load-test skew/catch-up.

### Answer 3

Create database/search snapshot from authoritative source at logical watermark $w$ that corresponds to event log position(s) per partition. Snapshot records entity versions and watermark. New group is created/retained before or consistently with snapshot so events after $w$ cannot expire; bulk-load snapshot idempotently, then consume strictly after $w$. If snapshot scan includes changes beyond $w$, use MVCC snapshot at $w$ or entity/version merge rules so log events deterministically supersede.

Stable key/version makes reapplication at boundary harmless; choosing inclusive consumption deliberately with dedupe is safer than an unproven exclusive conversion. Verify every partition watermark, no missing partitions, snapshot counts/digests, event gaps, version monotonicity and final source/projection reconciliation. Checkpoint bootstrap stages durably; on crash resume snapshot chunks/offsets, not restart effects blindly. Retention/capacity covers snapshot duration plus catch-up; throttle to protect live traffic. Fault-test concurrent updates, partition rebalance, snapshot failure, expiry approach and restore.

### Answer 4

Inventory topics/groups/owners/purpose/ACL/filter/start/retention/rate/lag/downstream/replay/DLQ and effects; freeze new wildcard/group creation. Assign owners/SLOs or pause/delete through reviewed drain/reconciliation. Split sensitive domains/purposes, minimize schemas, replace wildcard ACLs/filters with allowlisted contracts and audit access. Set retention from recovery/privacy/cost requirements, not infinite default; preserve required backups/snapshots.

Partition DLQ logically by subscription or retain immutable subscription provenance and route to owned queues; add age/rate alerts, inspect/correct/cancel/redrive tools, privacy controls and reconciliation. Classify consumers replayable versus live-effect; fence email/payment from historical replay and require explicit simulation/backfill identity. Cap per-group concurrency/prefetch/rate to database capacity; autoscale using lag/age plus downstream saturation, with retry backoff/jitter and quotas.

Introduce subscription admission/deletion lifecycle, schema/version contracts, chargeback/budgets and dashboards. Gates include zero ownerless mandatory groups, least-privilege tests, retention/recovery proof, no unexplained lag/DLQ, stable database saturation under worst catch-up, duplicate/replay fault tests, source-to-group-effect reconciliation, credential rotation and disaster restore. Migrate incrementally; deleting lag is not success.

### Answer 5

Authoritative laboratory/result operation transaction stores patient/specimen/order/result version, typed value/unit/qualifier/reference/method, status/correction, occurrence/provenance, policy/privacy metadata, audit and outbox. Mandatory clinical record, responsible-care-team notification and critical escalation groups have explicit time SLOs/current patient-order-result-authority checks, idempotent inbox/effects, correction/version/gap handling, independent ack/DLQ/reconciliation. Optional analytics receives minimized/deidentified data and cannot satisfy safety obligations.

Partition by tenant/patient or result/order according to reviewed ordering; corrections supersede/link and consumers reject stale versions. Unknown/unavailable/conflicting critical evidence triggers approved time-bounded escalation, not ordinary default. Enforce patient/tenant/professional/purpose/consent/jurisdiction and field/channel authorization, encryption/key rotation, retention/deletion and redacted telemetry/DLQ. Replay live notifications only under explicit reviewed workflow.

Accessible work queues distinguish new, urgent, acknowledged, unavailable, corrected, overridden and unresolved using keyboard/screen-reader/color-independent cues; mitigate alert fatigue and record rationale. Test clinical vectors/units/qualifiers, duplicates/gaps/corrections, every source/outbox/broker/group effect/ack crash, outage beyond threshold, current authority change, privacy attacks, load/backlog/recovery, replay, accessibility and disaster reconciliation. Named laboratory specialists, treating clinicians/nurses/pharmacists as relevant, clinical safety/informatics, patients/representatives, privacy/legal/regulatory, security, accessibility/human-factors, data/messaging/SRE and incident-response owners review real semantics. Broker delivery evidence cannot establish patient safety.
