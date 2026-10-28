# Worked Answers — Module 03: Delivery Semantics, Ordering, Partitioning, and Acknowledgement

Use these solutions to audit your reasoning for **Delivery Semantics, Ordering, Partitioning, and Acknowledgement**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Name six states

The domain transaction establishes authoritative truth; the outbox row records publication intent; the broker record establishes transport durability; the delivery attempt is temporary ownership; the consumer effect is the durable downstream result; acknowledgement advances the group. Crashes before outbox risk missing publication unless atomic, after broker acceptance risk duplicate relay, after effect before ack risk duplicate handling, and after ack should not redeliver. Each boundary needs a durable oracle.

The chapter’s decisive distinction is this: The producer first changes domain state. It then records or publishes a message. The broker accepts and persists a record. A consumer receives a delivery. The handler may commit a database effect. Finally, the consumer acknowledges the delivery and the group advances.

## 2. Compare delivery modes

Disposable high-frequency progress may accept at-most-once if loss is explicitly tolerable and no authoritative state depends on it. Artifact publication requires at-least-once delivery because losing the fact can prevent consumers from discovering a durable artifact. Duplicates are handled with inbox/effect identity. The choice follows consequence, not prestige.

In the cumulative capstone, the rule becomes concrete: At-most-once processing can be implemented by advancing or acknowledging before work. It avoids redelivery but loses work when the handler crashes afterward. This may be acceptable for disposable telemetry, not for authoritative artifact publication.

## 3. Choose a partition key

Run lifecycle uses run ID. Tenant billing totals may use tenant ID if updates must be serialized per tenant, though that risks hot tenants and may require sharding. Artifact chunks use artifact ID plus an ordered chunk strategy if chunk order matters; otherwise chunks may be independently addressed. The key is the smallest identity whose effects require sequence.

A useful way to reason about the boundary is: The partition key should be the smallest identity whose events require order. Run lifecycle events use run ID because requested → started → completed must be ordered for one run. Partitioning by tenant would serialize unrelated runs and create hot tenants. Partitioning by random event ID would destroy run order.

## 4. Reject global order

Partition offsets are only comparable inside one partition. Wall-clock timestamps can skew and arrival order can differ. A single global partition could impose sequence but limits throughput and still does not represent causal order across independent facts. The consumer should define per-subject order or use event-time window semantics.

The implementation consequence is: Two runs use different partition keys. run-B completed is observed before run-A started, and a dashboard labels the stream corrupt. There was no cross-run ordering promise. The projection must order within each subject or use event time and explicit aggregation semantics.

## 5. Design group identities

Use stable logical groups such as `notification-v1`, `analytics-v1`, and `audit-v1`. Two notification replicas share `notification-v1` and divide partitions; analytics replicas share `analytics-v1`; audit replicas share `audit-v1`. No group is shared across different effects.

The important nuance is: Audit and notification instances both join analysis-consumers. Each receives only some completion events, so neither effect is complete. Give each logical effect its own group; replicas of the same effect share a group.

## 6. Set acknowledgement timing

Acknowledge only after the projection effect and any durable intent for the email command are committed. Publishing the email directly after the projection creates a second dual write. Write an outbox row in the same transaction as the projection, then let a relay publish it. Acknowledgement follows that transaction.

Under concurrency or failure, the distinction becomes: The notification consumer acknowledges, then writes its delivery record. A process crash between those steps permanently loses the notification. Move acknowledgement after the durable effect or use a transactionally coupled inbox/effect boundary.

## 7. Handle a timeout

Prefer splitting long work into acceptance plus separately tracked completion when the handler effect is inherently long. Lease renewal is appropriate when the broker supports progress/renewal and stale ownership is fenced. Increasing the timeout is acceptable only with measured bounds and slower recovery consequences. An unbounded timeout hides dead consumers.

The design remains honest only if: The acknowledgement deadline must exceed expected handler time but remain short enough for useful recovery. Long-running work should renew a lease or split acceptance from completion rather than set an unbounded deadline.

## 8. Classify failures

Malformed schema and unauthorized producer are terminal for that record under the current contract. A database outage is transient and should be retried with bounded backoff. A deterministic business conflict is usually terminal or idempotently recorded; retrying the same unchanged event will not alter the result. Classification must be explicit.

The consumer-facing consequence is: A schema-invalid record is negatively acknowledged immediately forever. It monopolizes the head of the ordered partition. Validate before handler dispatch, classify the failure as permanent after bounded attempts, record a dead letter, and advance under an approved runbook.

## 9. Calculate lag meaning

Group A is immediately concerning because age violates timeliness even with low count, likely indicating a stuck partition or poison event. Group B may be a normal burst if drain rate exceeds arrival rate and age remains bounded. Compare throughput, partition distribution, and projected drain time before deciding.

The operational consequence is: Lag count is the number of records not yet acknowledged by a group. Oldest-message age measures how long the oldest pending fact has waited. A low count can still be critical if one event has been stuck for hours. A high count may be acceptable during a brief known burst if age remains within the service objective and drain capacity is sufficient.

## 10. Explain redelivery identity

Channel, partition, offset, key, event ID, payload, and publication time remain the same because it is one broker record. Delivery token, deadline, and attempt count change. Handler invocation and trace span are new attempts. Deduplication keys on stable event/effect identity, not delivery token.

The strongest engineering interpretation is: Attempt counts must be scoped to a group and record position. A new delivery token does not reset the attempt history. When the maximum is reached, the consumer records a dead letter with safe failure metadata and terminates or parks the record under policy.

## 11. Review retention

The projection cannot be rebuilt from a stream that has already expired. Increase retention to cover the recovery objective, maintain an immutable archive/object store, or create periodic projection snapshots plus retained deltas. The chosen remedy must preserve schema interpretation and privacy policy.

The defect-oriented view is: A short retention period can make recovery impossible even if consumers use explicit acknowledgement. Infinite retention creates privacy, storage, and schema-understanding obligations. Each channel needs a retention rationale connected to replay and audit requirements.

## 12. Write a failure-window table

Before effect: no committed effect, no ack, redelivery expected, no duplicate effect. After effect before ack: redelivery expected, duplicate effect unless inbox/effect transaction detects it. After ack: no redelivery under normal broker operation. During nack: the token settles into delayed eligibility; a crash before the broker accepts nack behaves like ack expiry.

Across the Python and TypeScript tracks, the invariant is: A crash after receive but before effect should redeliver. A crash after effect but before acknowledgement also redelivers, even though the business work already happened. Acknowledging before the effect avoids duplication but permits loss. No acknowledgement order eliminates both hazards without a transactional relationship between the effect store and delivery position.
