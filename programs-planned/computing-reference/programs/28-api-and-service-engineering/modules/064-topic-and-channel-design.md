---
module_id: API-064
program: API & Service Engineering
level: 2
module_number: 64
title: Topic and Channel Design
status: complete
last_verified: 2026-09-02
---

# Topic and Channel Design

## One-Page Review

### Governing question

How should a message-driven API map commands, facts, notifications, and documents onto semantic channels and physical topics, queues, subscriptions, or routes so ownership, audience, tenancy, ordering, retention, security, capacity, and lifecycle remain explicit and evolvable?

### Essential definitions

- A **semantic channel** is a contract-level addressable stream or route with one coherent purpose, owner, message family, audience, and lifecycle.
- A **physical destination** is the broker/provider resource—topic, queue, exchange, subscription, stream, or similar—that realizes one or more semantic channels.
- A **topic** commonly supports publish/subscribe fan-out or retained logs; exact behavior is product/protocol-specific.
- A **queue/subscription** commonly owns competing-consumer delivery state for one logical consumer group; it is not the event itself.
- A **routing key/topic name** is protocol-facing addressing metadata used to select a destination or subscription.
- A **channel taxonomy** is the durable naming and ownership scheme for domains, message kinds, versions, regions/environments, and tenancy.
- **channel cardinality** is the number of destination instances created by parameter combinations such as tenant, device, customer, or reply ID.
- A **compatibility boundary** identifies which message schemas/types and consumers must evolve together on a channel.
- A **lifecycle channel** is an operational destination for retry, quarantine, dead-letter, replay, or audit; it still requires ownership and policy.

### Central model, mechanism, or theorem

Let logical channel $c$ have contract

$$
c=(owner,purpose,kinds,audience,order,retention,security,capacity,lifecycle).
$$

A mapping $g(c,e,t,r)\rightarrow d$ selects physical destination $d$ for environment $e$, tenant strategy $t$, and region $r$. It is valid only if the destination's configured properties satisfy every channel invariant. If one destination carries channels $c_1,\ldots,c_n$, its policy must satisfy the strongest compatible requirement; conflicting retention, ACL, ordering, throughput, or schema evolution is evidence to separate them.

### Critical invariants

Channel boundaries follow durable semantic ownership, consumer audience, trust/data class, delivery/order/retention needs, and capacity—not team names or temporary projects. Commands have one logical authority and isolated reply/outcome rules; facts support independent consumers without consumer-specific naming. A channel defines allowed message types/schema compatibility, partition/order key, producer/consumer authorization, tenant/region/environment mapping, retention/compaction/expiry, replay, size/rate/quota, acknowledgement, dead-letter/redrive, and owner/runbook.

Logical names remain stable while physical mappings may vary by environment/provider. Wildcards/parameters are bounded and authorization-safe. Tenant isolation is an explicit choice among shared, partitioned, namespaced, or dedicated resources, with cardinality and noisy-neighbor analysis. Retry/dead-letter channels retain original logical identity and safe diagnostics; they never become unowned dumping grounds. Provisioning and deletion use governed IaC, compatibility/migration, observation, drain, backup/replay, and rollback evidence.

### Common failures

One topic for everything; one topic per event without operational reason; destination named after producing service/team; commands broadcast like facts; consumer name embedded in producer-owned event topic; environment/region/tenant concatenated ad hoc; topic per customer/device causing unbounded metadata; shared tenant topic without payload/ACL isolation; wildcard subscription grants cross-tenant access; channel mixes public and restricted data; unrelated schemas share one compatibility subject; changing topic to “version” a field; relying on wall-clock/topic order; retention chosen from defaults; compaction treated as complete history; reply topic attacker-controlled; retry topic creates endless loops; dead-letter has no owner/redrive policy; migration dual-publishes different event IDs; auto-create bypasses policy; and deleting an “unused” channel while dormant/replay consumers still depend on it.

### Compact example

An order domain uses semantic channel `confirmedOrders` for immutable `OrderConfirmed` facts, mapped in production to region-specific retained topics through IaC. All events key by order ID, use one transitive schema boundary, and allow only the order outbox producer. Billing and fulfillment each own independent subscriptions/checkpoints. Restricted fraud facts use a separate channel/ACL/retention. A per-consumer quarantine retains original event ID and reason; redrive returns to the normal handler with current policy. **Conclusion:** one fact channel can serve many consumers, but incompatible security or lifecycle requirements require separation.

### Connections

[Commands, Events, and Messages](061-commands-events-and-messages.md), [Event Schema Design](062-event-schema-design.md), and [AsyncAPI Contracts](063-asyncapi-contracts.md) define meaning and description. The next module develops ordering and partition keys; later modules develop acknowledgement, replay, dead-letter, and asynchronous API operations.

## Governing Question

Which message families belong together under one semantic and compatibility boundary, how do those boundaries map to provider resources across tenants/regions/environments, and what policy keeps routing, security, capacity, retention, replay, and migration correct throughout the channel lifecycle?

## Why This Matters

Channel structure becomes architecture. It determines who can publish and consume, which messages share partitions and quotas, how schemas evolve, how long facts survive, where replay begins, how failures isolate, and what operators can observe. Poor structure couples unrelated domains or explodes broker metadata and cost.

Names are only the visible part. A topic called `orders` may be a retained event log, a competing command queue, a transient notification feed, or a mixture. Those alternatives require different authority, acknowledgement, order, retention, and consumer behavior. Without a contract, producers and consumers infer incompatible semantics from one string.

Provider vocabulary differs. Kafka topics are partitioned logs with consumer groups; MQTT topic names and filters support hierarchical publish/subscribe with QoS/session/retained-message behavior; AMQP distinguishes nodes, addresses, links, delivery/settlement; Pulsar exposes topics, subscriptions, partitions, retention/backlog and subscription types. Design semantic channels first, then bind them precisely to the chosen product.

Channel decisions are difficult to reverse because retained data, ACLs, offsets, dashboards, connectors, schemas, and external consumers accumulate. A migration must preserve identity and ordering enough for consumers to avoid gaps and duplicates. Durable boundaries and explicit lifecycle policy reduce that cost.

## Prerequisites and Retrieval

Retrieve [API Threat Modeling](041-api-threat-modeling.md), [Commands, Events, and Messages](061-commands-events-and-messages.md), [Event Schema Design](062-event-schema-design.md), and [AsyncAPI Contracts](063-asyncapi-contracts.md). Know the chosen broker/protocol's destination, partition, subscription, ordering, retention, compaction, expiry, wildcard, acknowledgement, quota, and authorization semantics.

Inventory producers, consumers—including dormant/replay/batch integrations—message types/schemas, tenant/data classification, regional/residency rules, volumes/bursts/sizes, replay horizons, delivery/order requirements, and operational ownership. Retrieve exact provider/version documentation rather than relying on generic queue/topic terminology.

## Learning Objectives

After completing this module, you can:

1. derive semantic channels from message meaning, authority, audience, trust, and lifecycle;
2. distinguish logical channels from physical topics, queues, subscriptions, and routes;
3. choose channel granularity and naming without service coupling or cardinality explosion;
4. separate commands, events, replies, notifications, and operational failure channels;
5. design tenant, environment, and regional mapping with ACL and residency controls;
6. align message schemas and compatibility boundaries with channel policy;
7. specify retention, compaction, expiry, replay, capacity, quotas, and observability;
8. design retry, quarantine, dead-letter, and redrive channels safely;
9. provision and reconcile channels through governed contracts and IaC; and
10. migrate, deprecate, and delete destinations without gaps, identity loss, or orphaned consumers.

## Core Exposition

### Start from semantic channel intent

For each interaction, state message kind, authority, sender set, logical audience, and outcome. Commands go to one logical authority even when many workers compete. Facts originate from one owning domain and can fan out to independent consumers. Notifications may be lossy/coalesced. Documents may need separate size/retention paths. Replies belong to a controlled request/outcome conversation.

Then state channel purpose in one sentence: “carries immutable order-confirmation facts produced by the order authority for authorized internal consumers.” If the sentence needs “and also,” test whether security, schema, retention, ordering, scale, or lifecycle conflicts justify separation.

Do not name a fact channel after today's producer service (`order-service-output`) or consumer (`billing-input`). Services reorganize; the domain fact and ownership endure. Consumer-specific queues/subscriptions can be named by consuming application because they own delivery state, but the producer-owned event stream remains consumer-neutral.

Commands should name target capability/domain (`inventory.reserve.commands`) rather than requesting service deployment. One logical handler group consumes. If multiple autonomous systems should react, publish a fact; do not broadcast one command and accept competing decisions accidentally.

### Separate logical and physical topology

AsyncAPI channel key/address split helps: the contract key can remain semantic while environment-specific address maps to provider resource. Maintain a channel catalog mapping application/operation/message to physical cluster/namespace/topic/queue/subscription, schema subject, ACL, retention, partitioning, quota, and owner.

The mapping can differ: staging may use shared cluster namespace; production uses regional clusters; an external partner receives webhooks rather than broker access; MQTT devices publish hierarchical topics that bridge into an internal log. Adapters preserve event identity/type/tenant/sequence and document acknowledgement changes.

Avoid pretending abstractions are identical. A Kafka consumer group offset, MQTT session/QoS flow, AMQP delivery settlement, and Pulsar subscription cursor differ. Bind exact behavior and test. “Topic” in the semantic model means an addressable publish/subscribe boundary, not a guarantee of retention or fan-out.

Physical resource identity is managed by IaC and stable identifiers/tags. Automatic topic/queue creation is disabled or constrained in production because defaults can violate partitions, replication, retention, encryption, schema, and ACL policy. The AsyncAPI contract and IaC reconcile through the semantic channel ID.

### Choose channel granularity

One channel may carry several event types when they share domain owner, subject/order key, audience/security, retention/replay, scale, and compatibility strategy. This supports related streams and atomic/causal consumption where the broker can preserve the required scoped order. Consumers discriminate by type.

Separate channels when facts have different classification or consumers, different retention/residency, incompatible ordering/partition key, extreme volume/size, independent lifecycle, protocol/binding, or schema compatibility ownership. Commands and events usually separate because authority and consumption differ. Large documents separate from small events to protect broker limits.

One topic per event type maximizes isolation but creates destination/ACL/monitoring/connector overhead and can destroy cross-type subject order. One topic for an entire enterprise minimizes resource count but creates broad ACLs, hot/noisy streams, schema unions, incompatible retention, and massive blast radius. Choose the coarsest boundary that preserves invariants, then validate provider capacity.

Estimate channel count before parameterization. If domains $D$, environments $E$, regions $R$, tenants $T$, and versions $V$ are multiplied naïvely, count can approach

$$
N=D\cdot E\cdot R\cdot T\cdot V.
$$

Not every dimension belongs in a physical destination. Environment/region often map to clusters/namespaces; tenant may be shared with keyed isolation; schema version often stays within one compatible channel. Quantify metadata, controllers, ACLs, monitoring, cost, and operational limits.

### Design durable names and taxonomy

Define lowercase/delimiter/character/length rules compatible with all target tools. Use stable hierarchy such as organization/domain/capability/kind/major only where each segment drives ownership/policy. Do not encode temporary team, sprint, deployment color, ticket, or date.

Environment and region may belong outside the logical name in cluster/account/namespace. If they appear physically, generate from one mapping, not producer string concatenation. Tenant IDs in names create cardinality and disclosure concerns; choose only after isolation analysis. Never include credentials or personal data in topic/queue/subscription names because names appear in logs/metrics/control planes.

Do not version a destination for every additive schema update. Schema registry/message type carries compatible evolution. Introduce a major channel/type when meaning, wire format, security, order, or lifecycle cannot coexist. State dual-publish and retirement plan.

Names alone are not discovery. Catalog each channel's description, owner/on-call, lifecycle, producers, allowed messages/schema subjects, consumers/subscriptions, data class, tenant strategy, partition key/order, retention/compaction, rate/size, DLQ/redrive, region, IaC resource, contract version, and runbooks.

### Separate producers, streams, and subscriptions

Producer authorization belongs to the semantic fact/command source. For facts, restrict write to authoritative outbox/publisher identities. For commands, restrict senders by business capability and receive to the authority. A broadly writable topic cannot establish source truth from a self-declared payload field.

Fan-out facts use one producer-owned stream plus consumer-owned subscriptions/groups/cursors. Each logical consumer has independent checkpoint, retry, lag SLO, replay, and deletion lifecycle. Multiple replicas of one consumer share a group/subscription for load distribution; different business consumers do not share one group accidentally or they split events.

Queue-per-consumer copies can isolate delivery/retry but multiply resources/storage/routing and make replay/history producer-specific. Log plus independent offsets can support replay/fan-out but requires consumers to manage lag/retention and partition concurrency. Broker choice and adapter should match requirements.

Subscription names are durable consumer application identities, not instance/pod IDs. Ephemeral debug subscriptions have TTL/quota/owner and cannot retain unbounded backlog. Dormant consumers are registered; automated “unused” cleanup considers replay/disaster consumers and declared lifecycle.

### Design tenant isolation deliberately

Shared channel with tenant in authenticated envelope/key is resource-efficient but demands strong producer binding, payload validation, consumer filters/ACL support, per-tenant quotas, encryption/classification, and proof consumers cannot receive other tenants. Client-side filtering after broad delivery is not isolation.

Namespace/topic per tenant improves ACL, retention, residency, and blast isolation but multiplies resources, schema subjects, connectors, metrics, and migrations. Dedicated cluster/account offers strongest isolation for regulated/large tenants at highest cost. Hybrid tiers dedicate heavy/sensitive tenants while sharing others under governed keys.

Do not let untrusted tenant strings form resource names or wildcard filters directly. Map authenticated tenant to normalized internal ID through policy, constrain length/character/cardinality, and provision via authorized control plane. MQTT wildcard subscriptions in particular require careful ACL intersection; `#` or `+` can widen audience beyond intent.

Cross-tenant aggregate analytics should consume through an explicitly privileged, audited projection path with minimization, not a wildcard granted to ordinary consumers. Tenant migration preserves event identity, checkpoints, order/gap detection, and residency, with dual-read/write controls and reconciliation.

### Align schema compatibility boundaries

List allowed message types per channel and exact discriminator/envelope. Each type has a schema subject/owner and compatibility policy. A channel carrying unrelated schemas under one registry subject/union can make one producer's change block or break others. Conversely, many compatible types can share a channel while retaining per-type schema identities.

Consumers decide whether unknown message types are ignored, quarantined, or rejected. Silent ack/drop can lose newly introduced facts; infinite retry can block a partition. Use operation-level message selection, type registry, and rollout ordering. Audit unexpected types.

Channel major versions are reserved for incompatible coexistence needs. During migration, old/new types/channels share a documented fact identity/causation mapping. Avoid converting one domain fact into two independently generated IDs, which defeats deduplication/parity.

Schema retention must outlive message retention/replay/support. Compacted topics still retain old encodings until compaction/segment lifecycle removes them. Dead-letter/retry archives may outlive primary retention; retain schemas and privacy policy accordingly.

### Specify ordering and partition interaction

The next module develops key design, but channel boundaries must state the ordering subject and compatible partition key. Mixing message families requiring order by different keys in one partitioned topic cannot satisfy both generally. Global single-partition order sacrifices scalability/availability and rarely matches domain need.

Routing, retry topics, priority channels, and region bridging can reorder. Encode subject version/sequence and gap policy. Consumer concurrency must preserve per-key processing where required. Do not infer domain order from timestamp, offset across partitions, or topic name.

Channel migration changes partitions/routing and can disrupt order. Define cutover boundary, high-water marks, duplicate/gap reconciliation, and stable event identity. Avoid resizing/rehashing without understanding provider key-to-partition consequences.

### Define retention, expiry, and compaction

Retention follows business recovery/replay/audit objectives, maximum consumer outage/lag, legal/privacy requirements, and storage/cost evidence. State time/size policies, minimum guaranteed window under load, replication/backup, and what happens after expiry. Default broker settings are not a requirement.

Command deadlines and message expiry may be shorter than destination retention. Expired commands become terminal expired/rejected and are not blindly executed. Event retention may support replay but not permanent audit; archive separately with integrity/access/erasure if required.

Log compaction keeps latest records per key according to broker behavior and tombstones/configuration; it is not a complete ordered history. It suits reconstructing latest keyed state when producer/consumer semantics, tombstones, key stability, and compaction lag are understood. Do not use it where every transition/audit is required unless a separate retained history exists.

MQTT retained messages provide a last known publication per topic under protocol rules, not an event log. Sessions/QoS/message expiry also differ from log retention. Bind precise semantics; never translate “retained” generically across brokers.

### Bound capacity and blast radius

Estimate average/peak messages and bytes per second, burst duration, key distribution, number of producers/consumers/subscriptions, fan-out, retention storage, replay/backfill rate, and regional replication. Include encoding, headers, replication, indexes, and dead-letter overhead. Validate against provider quotas and failure capacity.

Large shared topics can create noisy-neighbor lag and broad incident blast radius. Too many small topics burden metadata/controllers/connections/files/metrics. Hot keys cap one partition; random keys destroy subject order. Balance using measured distribution and future growth, then test rebalancing/failover.

Set per-producer/tenant/channel rate/byte/message-size quotas, consumer concurrency/prefetch/in-flight bounds, backlog/age limits, replay budgets, and admission/load shedding. Critical commands/facts can use isolated channels/capacity from bulk analytics. Priority should not permit starvation; document scheduling/fairness.

Monitor ingress/egress rate/bytes, partitions, replication health, producer errors, consumer group/subscription lag/age, backlog storage, hot keys/partitions, unknown types/schemas, auth denies, retries/DLQ, message expiry, and quota throttling. Avoid tenant/message IDs as unbounded metric labels.

### Design retry, quarantine, and dead-letter channels

Retry may occur in consumer memory with backoff, broker redelivery delay, scheduled retry destinations, or workflow state. Each option affects order, duplicate windows, resource occupancy, and failure isolation. Define transient/permanent classification, attempts/age/deadline, backoff/jitter, and original identity.

If staged retry topics are used, keep original logical event ID/type/source/subject/sequence/causation and record attempt metadata separately. Moving an event out of its ordered partition can let later events pass; consumers need per-key blocking, version/gap reconciliation, or explicit relaxed order.

Dead-letter/quarantine channel is per semantic/consumer boundary when failure depends on consumer/schema/policy. Store minimal original envelope/payload or secure reference, source location/schema ID, failure class, bounded diagnostics, first/last time, attempts, and owner. Apply encryption, classification, retention, access, erasure, and size limits; DLQ often contains the most sensitive malformed data.

Redrive revalidates schema, authorization, tenant, deadline, current policy, idempotency, and target mapping. It is rate-limited, previewable, auditable, cancellable, and reconciled. Never publish recursively back into DLQ or reset identity/attempt history.

### Provision and govern lifecycle

Create destinations/subscriptions through reviewed IaC/control plane with semantic channel ID, owner, tags, protocol/binding, partitions, replication, retention/compaction, encryption, quotas, ACLs, schema policy, DLQ, monitoring, backup, and deletion protection. AsyncAPI and IaC validate each other.

Changes are classified: compatible config expansion, capacity change, security/retention high risk, or semantic breaking migration. Validate provider constraints and staged rollout. A retention reduction can destroy recoverability; an ACL widening can disclose data; a partition change can alter order. Require backups/high-water evidence and rollback where possible.

For migration, inventory producers/consumers/connectors/schemas/offsets, create target, mirror/dual-publish from one authoritative event identity, validate counts/checksums/order/gaps/latency, move consumers with checkpoints, stop old writes, drain/observe, archive if required, then delete after deprecation. Do not dual-write independent business transactions.

Deletion checks declared and observed producers/consumers over meaningful windows, dormant/replay/legal dependencies, backlog, snapshots/archive, schema retention, incident rollback, and ACL/reference cleanup. Tombstone/catalog record preserves history without leaving active resources.

## Definitions and Notation

Let channel contract $c=(o,p,K,A,Q,H,X,L)$ contain owner $o$, purpose $p$, allowed message kinds/types $K$, audience $A$, order/partition rule $Q$, retention/history $H$, security/classification $X$, and lifecycle/capacity $L$.

Let mapping $g(c,e,t,r)=d$ produce physical destination $d$ for environment, tenant strategy, and region. Let configured properties $P(d)$ and required properties $R(c)$. Conformance requires $P(d)\models R(c)$ under the exact provider semantics.

Let dimensions $D,E,R,T,V$ estimate worst-case destination count $N=DERTV$ before consolidation. Let producer set $P_c$, consumer subscriptions $G_c$, allowed types $M_c$, and schema subjects $S_c$ support inventory/reconciliation. Counts alone do not decide granularity; incompatible invariants do.

## Mechanisms, Invariants, or Proof Structure

1. Classify messages and state semantic channel purpose, authority, audience, and owner.
2. Group only message families with compatible security, retention, order key, scale, schema, and lifecycle.
3. Define durable logical taxonomy, allowed types, compatibility subjects, and unknown-type behavior.
4. Choose tenant/environment/region mapping and calculate physical cardinality/cost/limits.
5. Bind logical channels to exact provider destinations, subscriptions, protocol semantics, and IaC.
6. Specify ACLs, producer truth, consumer groups, quotas, ordering/partition, retention/compaction/expiry, replay, and SLOs.
7. Design retry/quarantine/dead-letter/redrive without identity loss or order surprises.
8. Verify contracts, schemas, IaC, broker state, ACLs, producers/consumers, and telemetry.
9. Load/fault/security/replay test capacity, noisy neighbors, outages, wildcard abuse, and recovery.
10. Migrate/deprecate/delete with stable identities, checkpoints, reconciliation, observation, and rollback.

If two logical channels require mutually exclusive policy—such as broad public read and restricted health data—one physical ACL cannot satisfy both without overexposure or denial; they must be separated or protected by a mediation layer that enforces distinct authorized views. If tenant-per-topic count exceeds provider/control-plane/operational capacity, stronger isolation cannot be claimed sustainable without tiering or dedicated infrastructure evidence.

## Alternatives and Trade-Offs

**One broad topic versus many narrow topics.** Broad reduces resource overhead and can preserve cross-type key order but widens ACL/schema/retention/blast coupling. Narrow isolates policy/scale but increases metadata, connectors, and migrations.

**Shared stream plus consumer groups versus routed per-consumer queues.** Shared retained stream supports fan-out/replay; queues isolate delivery/retry and may fit work distribution. Provider semantics and storage/ownership decide.

**Shared tenant channel versus tenant destinations.** Shared scales operationally but needs strong message-level isolation/quotas. Dedicated improves blast/ACL/residency isolation at high cardinality/cost. Hybrid tiering often wins.

**Hierarchical/wildcard routing versus explicit destinations.** Wildcards enable flexible IoT/fan-out subscriptions but complicate least privilege and surprise matches. Explicit channels improve reviewability but proliferate resources/routes.

**Delete retention versus compaction versus archive.** Delete retention preserves transitions for a window; compaction preserves latest keyed records under broker rules; archive supports longer recovery/audit but adds access/lineage/erasure. They can compose.

**Retry in place versus retry channels.** In-place can preserve order but blocks resources; retry channels free the main flow but reorder and add topology. Choose per failure/ordering requirement.

**Semantic name stability versus physical provider optimization.** Stable contract names help consumers; provider resources may move/split. A governed mapping/adapter decouples them while adding operational ownership.

## Failure Modes and Misconceptions

1. Physical broker noun is assumed to define semantic delivery/retention behavior.
2. Channel boundary follows current service/team instead of domain fact/authority.
3. Commands and facts share one broad route and conflicting consumption semantics.
4. One topic per type explodes resources or destroys required cross-type key order.
5. One topic for everything forces broad ACL, retention, schema, and blast radius.
6. Tenant/region/environment strings form resource names without normalization/control.
7. Wildcard/client-side filtering is treated as tenant isolation.
8. Schema version is encoded into a new topic for every additive change.
9. Topic default retention/compaction is mistaken for business recovery/audit.
10. Global/domain order is inferred from topic, timestamp, or cross-partition offsets.
11. Consumer replicas and different business consumers accidentally share one group.
12. Retry topology violates order/deadline or creates loops with new identities.
13. Dead-letter has weak privacy, no owner, no replay validation, or infinite retention.
14. Auto-create bypasses partitions, encryption, ACL, schemas, quotas, and monitoring.
15. Migration/deletion ignores dormant consumers, offsets, retained schemas, gaps, and rollback.

## Worked Examples

### Example 1

`OrderConfirmed` and `OrderCancelled` share order owner, order key, internal audience, retention, and schema governance, so one `orderLifecycleFacts` channel is coherent. `PaymentCardRiskFlagged` is separated because classification and consumer ACL differ despite sharing order ID.

### Example 2

`ReserveInventory` commands use one authority-owned queue/group. Ten worker replicas compete within that group; a second business consumer cannot join and steal commands. Outcomes and resulting facts use separate channels.

### Example 3

An IoT MQTT hierarchy `org/{tenant}/device/{device}/telemetry` permits bounded device publications. ACL binds authenticated device to its exact prefix; analytics wildcard is a privileged audited role. Bridge preserves identity/QoS interpretation into an internal retained log.

### Example 4

Ten thousand small tenants share a keyed channel with broker-enforced producer identity, authorized server-side consumption, per-tenant quotas, and encrypted payloads. Three regulated tenants receive dedicated namespaces/clusters. The tiering decision avoids both weak isolation and unbounded topic count.

### Example 5

A compacted customer-state channel uses customer ID key and tombstones to rebuild latest projection. A separate immutable customer-audit channel retains transitions. Compaction is never described as complete audit history.

### Example 6

A consumer retries transient database errors in place briefly. Longer delay moves to a retry channel and records original ID/sequence; later subject events are buffered/reconciled by version. Permanent schema errors go to consumer-owned quarantine, not a shared global graveyard.

### Example 7

Per-customer reply topics for every request would create millions of resources. The design uses controlled shared reply channel partitioned by requester identity, required correlation, scoped ACL/filter enforced by broker/service, TTL, outstanding limits, and no user-supplied arbitrary address.

### Example 8

A new event schema is backward compatible, so it remains on the same channel/schema subject. A changed fact meaning and stricter restricted audience creates a new event type/channel major with dual publication from one source transaction and stable causation mapping.

### Example 9

Production region migration mirrors retained topics, captures per-partition high-water marks, preserves event IDs/keys, compares counts/checksums/subject versions, and moves consumer checkpoints. Consumers tolerate duplicates and detect gaps; old region drains before deletion.

### Example 10

Catalog says a subscription is unused, but disaster-recovery replay job has no recent traffic. Deletion review finds the declared owner and recovery dependency. The subscription becomes ephemeral-on-demand with tested checkpoint/snapshot procedure rather than silently deleted.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies logs, queues, partitions, order, replication, and failure reasoning. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies throughput, fan-out, connections, regional paths, and loss. [Security Engineering](../../25-security-engineering/ROADMAP.md) governs ACLs, tenancy, data classification, and trust boundaries.

[Data Engineering](../../19-data-engineering/ROADMAP.md) consumes topics for streaming, replay, lineage, and data quality. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns brokers, namespaces, IaC, quotas, catalogs, telemetry, and paved roads. [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) contributes managed-service quotas, residency, cost, replication, backup, and disaster recovery.

## References

1. AsyncAPI Initiative. “AsyncAPI Specification 3.1.0.” <https://www.asyncapi.com/docs/reference/specification/v3.1.0>
2. Apache Software Foundation. “Apache Kafka Documentation.” Retrieved 2026-09-02. <https://kafka.apache.org/documentation/>
3. OASIS. “MQTT Version 5.0.” 7 March 2019. <https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html>
4. OASIS. “Advanced Message Queuing Protocol (AMQP) Version 1.0.” 29 October 2012. <https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-complete-v1.0-os.html>
5. Apache Software Foundation. “Apache Pulsar: Messaging Concepts.” Retrieved 2026-09-02. <https://pulsar.apache.org/docs/next/concepts-messaging/>
6. AsyncAPI Initiative. “AsyncAPI Bindings Specifications.” Retrieved 2026-09-02. <https://github.com/asyncapi/bindings>

## Exercises

### Exercise 1

Given events `OrderCreated`, `OrderConfirmed`, `OrderCancelled`, `PaymentCaptured`, `FraudRiskFlagged`, and command `ReserveInventory`, propose semantic channel grouping. State owner, audience, security, order key, retention, schema boundary, and why particular types must separate.

### Exercise 2

Estimate worst-case destination count for 12 domains, 3 environments, 4 regions, 25,000 tenants, and 2 major versions if every dimension becomes a topic. Recompute if environment/region use cluster/namespace, tenant is shared with 100 dedicated exceptions, and only 3 domains need 2 concurrent majors. Explain why arithmetic is only one decision input.

### Exercise 3

Design MQTT topics and ACLs for multi-tenant building sensors plus an internal retained analytics log. Include topic hierarchy/filter safety, device/tenant identity, QoS/retained/expiry meaning, bridge mapping, cardinality, schema, order, privacy, quotas, and recovery.

### Exercise 4

Design retry, quarantine, and redrive for a per-account ordered event consumer. Include transient/permanent classification, attempts/age, original identity/sequence, ordering effect, schema/auth/deadline checks, security/retention, observability, and reconciliation.

### Exercise 5

Plan a zero-data-loss migration from a shared `commerce.events` topic to separate order and payment channels with different ACL/retention. Include inventory, target provisioning, schema/identity, dual publish or mirror, checkpoints/high-water marks, parity, consumers, rollback, drain, deprecation, and deletion.

## Answers to the Exercises

### Answer 1

`OrderCreated`, `OrderConfirmed`, and `OrderCancelled` can share an order-lifecycle fact channel if the order domain owns all, events key/sequence by order, audience is ordinary authorized commerce consumers, retention/replay and classification align, and each type retains its own transitive schema subject under one channel discriminator. Sharing can preserve cross-type per-order order.

`PaymentCaptured` belongs to payment-owned fact channel because authority, payment key/order, PCI-adjacent classification/minimization, retention, ACL, and consumers differ. `FraudRiskFlagged` separates further even if keyed by order/payment because restricted risk audience and retention cannot coexist with broad order ACL. A mediated minimized fact can be published for ordinary consumers if needed.

`ReserveInventory` is a command to one inventory authority and belongs on an authority-owned command queue/channel, keyed/scoped by inventory item/order as its concurrency contract requires, with deadline/idempotency/outcome semantics. Worker replicas share one group; other business consumers cannot compete. Resulting `InventoryReserved` fact would be a separate inventory fact channel. Each channel documents quotas, schemas, DLQ/redrive, and owner/runbook.

### Answer 2

Naïve count is $12\times3\times4\times25{,}000\times2=7{,}200{,}000$ topic instances before subscriptions, retry/DLQ, replicas, and monitoring. This is operationally implausible for most platforms.

If environment and region are cluster/namespace dimensions, not topic multipliers, base shared channels are 12. Add 100 dedicated tenant exceptions per domain: $12\times100=1{,}200$, plus 12 shared gives 1,212. If only three domains need one additional concurrent major, add three shared major channels and, if every dedicated exception in those domains also needs both majors, add $3\times100=300$; worst case becomes 1,515. A narrower migration could dual-version only affected tenants and be lower.

Arithmetic reveals cardinality/cost but not security, residency, order, throughput, schema, consumer, retention, provider quota, or blast-radius compatibility. Dedicated resources may still be required for regulated/heavy tenants; shared resources require server-side isolation and quotas. Measure metadata/ACL/monitoring/connector cost and provider limits before choosing.

### Answer 3

Use a bounded hierarchy such as `org/{tenantInternalId}/building/{buildingId}/device/{deviceId}/telemetry/{kind}`. An authenticated provisioned device may publish only its exact tenant/building/device prefix; it cannot choose arbitrary IDs. Tenant operators subscribe only their exact tenant subtree. Cross-tenant analytics wildcard is a distinct privileged audited bridge identity; ordinary clients never receive all data and filter locally. Normalize/allowlist identifiers and cap buildings/devices/topic length/cardinality.

Document MQTT 5.0 QoS per message kind as transport delivery scope, not business exactly-once. Decide session expiry, message expiry, retain flag, last-will, maximum packet/in-flight, shared subscription behavior, and duplicate handling. Retained telemetry is last-known publication, not history; do not mix command/reply topics or treat retained messages as replay log. Per-device sequence/occurred/received times detect gaps/order beyond connection behavior.

Bridge validates trusted device-to-tenant binding, schema/type/size/unit/time, rate quotas, and classification; preserves stable event ID/source/subject/sequence and records MQTT delivery metadata separately. It publishes to internal retained log keyed by device under governed schema and regional/residency mapping. Broker ACLs, TLS/device credentials/rotation, payload encryption/minimization, and cross-tenant denies are tested.

Use per-device/tenant rate and byte quotas, connection/in-flight limits, compression/size bounds, hot-tenant isolation, and monitored drops/QoS retries/session state. Recovery distinguishes MQTT live/last-known behavior from internal log replay; bridge has inbox/outbox/idempotency and reconciliation to device sequence. Provision topics logically through policy even if broker topic names are dynamic; inventory owners and lifecycle.

### Answer 4

On receive validate type/schema/size, tenant/authorization, event ID, account ID/version, and local inbox. Transient dependency errors retry briefly in place with exponential jitter while respecting attempt/age budget. Because account events are noncommutative, do not acknowledge and let later same-account versions apply. Bound partition blocking; isolate/account-pause and continue unrelated keys if architecture supports it.

Long delay may use retry channel, but preserve original event ID/type/source/account/version/causation/schema ID and add attempt metadata separately. Record that leaving primary partition allows later versions to arrive; consumer buffers/rejects them by account version or marks gap and fetches/replays authoritative history/snapshot. Permanent schema, unauthorized, impossible transition, or expired-retention cases enter consumer-owned quarantine with bounded reason/source location and no recursive retry.

Quarantine inherits payload classification/encryption/access/erasure, has finite retention and owner/on-call. Observe message age, attempts, account gap, partition lag, quarantine count/reason, redrive rate/outcome, and reconciliation drift without logging sensitive payload. Alert poison loops/hot accounts.

Redrive requires approved operator/workflow, preview, current schema/upcaster, tenant authorization, deadline/relevance, idempotency/inbox, destination mapping, and rate budget. It retains identity/history and is cancellable/audited. After processing, compare account projection version/invariants to authoritative state; skip only under explicit correction/reset procedure, never ack/drop silently.

### Answer 5

Inventory all producers/outboxes, message types/schema IDs, keys/partitions, consumer groups/connectors/offsets, replay/dormant consumers, ACLs, retention/compaction, regions, volumes, and owners. Define order facts and payment facts with distinct semantic owners, allowed schemas, keys, classification, retention, quotas, DLQs, and AsyncAPI operations. Provision target topics through IaC with replication/encryption/ACL/monitoring/schema policy and rollback capacity.

Prefer one authoritative routing publisher/outbox record that emits/mirrors each original event with the same event ID/type/source/subject/occurred time/key/sequence; mapping metadata identifies old/new positions. Do not create two domain events or dual-write business state. If broker mirroring is used, verify it preserves headers/keys/schemas and document offset differences. Capture per-partition start/high-water marks.

Backfill retained old history into targets within retention, then dual route live events. Compare per-type/key/time counts, unique IDs, checksums, subject sequences/gaps, schema rejection, latency, and ACL denies. New consumers start from mapped checkpoints/high-water, use inbox/idempotency, and compare shadow projections/outcomes. Move restricted payment consumers first only after ACL negative tests; ensure order consumers cannot read payment.

Rollback keeps old publication/consumers and can stop target reads without identity divergence. Once parity and SLO/replay/fault tests pass, move all declared consumers/connectors, stop old writes at recorded high-water, drain lag, reconcile final IDs/sequences, and observe through maximum dormant/rollback window. Publish deprecation/catalog updates and retain old schemas/offset maps/archive as required.

Deletion checks no active or dormant/replay/legal dependency, zero/accepted backlog, archive/restore, ACL/reference/dashboard cleanup, and disaster procedure. Delete through reviewed IaC with recoverability evidence; preserve tombstone catalog/migration record. Any discovered gap resumes from source archive/outbox using original IDs rather than inventing replacements.
