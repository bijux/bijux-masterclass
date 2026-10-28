# Reference Answers — Module 03: Worked answers — Module 03 — Delivery Semantics, Ordering, Partitioning, and Acknowledgement

Read after attempting all twelve Delivery Semantics, Ordering, Partitioning, and Acknowledgement exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Name six states

The domain transaction establishes authoritative truth; the outbox row records publication intent; the broker record establishes transport durability; the delivery attempt is temporary ownership; the consumer effect is the durable downstream result; acknowledgement advances the group. Crashes before outbox risk missing publication unless atomic, after broker acceptance risk duplicate relay, after effect before ack risk duplicate handling, and after ack should not redeliver. Each boundary needs a durable oracle.

## 2. Compare delivery modes

Disposable high-frequency progress may accept at-most-once if loss is explicitly tolerable and no authoritative state depends on it. Artifact publication requires at-least-once delivery because losing the fact can prevent consumers from discovering a durable artifact. Duplicates are handled with inbox/effect identity. The choice follows consequence, not prestige.

## 3. Choose a partition key

Run lifecycle uses run ID. Tenant billing totals may use tenant ID if updates must be serialized per tenant, though that risks hot tenants and may require sharding. Artifact chunks use artifact ID plus an ordered chunk strategy if chunk order matters; otherwise chunks may be independently addressed. The key is the smallest identity whose effects require sequence.

## 4. Reject global order

Partition offsets are only comparable inside one partition. Wall-clock timestamps can skew and arrival order can differ. A single global partition could impose sequence but limits throughput and still does not represent causal order across independent facts. The consumer should define per-subject order or use event-time window semantics.

## 5. Design group identities

Use stable logical groups such as `notification-v1`, `analytics-v1`, and `audit-v1`. Two notification replicas share `notification-v1` and divide partitions; analytics replicas share `analytics-v1`; audit replicas share `audit-v1`. No group is shared across different effects.

## 6. Set acknowledgement timing

Acknowledge only after the projection effect and any durable intent for the email command are committed. Publishing the email directly after the projection creates a second dual write. Write an outbox row in the same transaction as the projection, then let a relay publish it. Acknowledgement follows that transaction.

## 7. Handle a timeout

Prefer splitting long work into acceptance plus separately tracked completion when the handler effect is inherently long. Lease renewal is appropriate when the broker supports progress/renewal and stale ownership is fenced. Increasing the timeout is acceptable only with measured bounds and slower recovery consequences. An unbounded timeout hides dead consumers.

## 8. Classify failures

Malformed schema and unauthorized producer are terminal for that record under the current contract. A database outage is transient and should be retried with bounded backoff. A deterministic business conflict is usually terminal or idempotently recorded; retrying the same unchanged event will not alter the result. Classification must be explicit.

## 9. Calculate lag meaning

Group A is immediately concerning because age violates timeliness even with low count, likely indicating a stuck partition or poison event. Group B may be a normal burst if drain rate exceeds arrival rate and age remains bounded. Compare throughput, partition distribution, and projected drain time before deciding.

## 10. Explain redelivery identity

Channel, partition, offset, key, event ID, payload, and publication time remain the same because it is one broker record. Delivery token, deadline, and attempt count change. Handler invocation and trace span are new attempts. Deduplication keys on stable event/effect identity, not delivery token.

## 11. Review retention

The projection cannot be rebuilt from a stream that has already expired. Increase retention to cover the recovery objective, maintain an immutable archive/object store, or create periodic projection snapshots plus retained deltas. The chosen remedy must preserve schema interpretation and privacy policy.

## 12. Write a failure-window table

Before effect: no committed effect, no ack, redelivery expected, no duplicate effect. After effect before ack: redelivery expected, duplicate effect unless inbox/effect transaction detects it. After ack: no redelivery under normal broker operation. During nack: the token settles into delayed eligibility; a crash before the broker accepts nack behaves like ack expiry.
