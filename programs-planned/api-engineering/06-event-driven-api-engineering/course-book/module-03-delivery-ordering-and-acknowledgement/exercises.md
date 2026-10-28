# Exercises — Module 03 — Delivery Semantics, Ordering, Partitioning, and Acknowledgement

Model concrete crash windows and state transitions. Avoid vendor slogans.

## 1. Name six states

For one completion fact, identify domain commit, outbox record, broker record, delivery attempt, consumer effect, and acknowledgement. Place a crash between each adjacent pair.

## 2. Compare delivery modes

Choose at-most-once or at-least-once for disposable progress telemetry and for artifact publication. Defend both choices.

## 3. Choose a partition key

Select a partition key for run lifecycle events, tenant billing totals, and artifact chunks. Explain the ordering domain for each.

## 4. Reject global order

A consumer expects all events across tenants in timestamp order. Explain why broker offsets cannot supply that promise without a global bottleneck.

## 5. Design group identities

Define group names for notification, analytics, and audit, each with two replicas. Explain which instances share progress.

## 6. Set acknowledgement timing

A handler writes a projection and publishes an email command. Decide when it may acknowledge and identify the remaining dual-write issue.

## 7. Handle a timeout

A handler runs longer than `ack_wait` but is still healthy. Compare extending/renewing a lease, splitting work, and increasing the timeout.

## 8. Classify failures

Classify malformed schema, temporary database outage, unauthorized producer, and deterministic business conflict as retryable or terminal.

## 9. Calculate lag meaning

Group A has lag 10 and oldest age 2 hours; Group B has lag 10,000 and oldest age 8 seconds. Which is more urgent and what additional capacity evidence is needed?

## 10. Explain redelivery identity

Which fields remain the same and which change when the same record is delivered at attempt 3?

## 11. Review retention

A completion stream is retained for seven days, but a projection may need rebuilding after 30 days. Identify the contradiction and two remedies.

## 12. Write a failure-window table

Create rows for crash before effect, after effect before ack, after ack, and during nack. State expected redelivery and duplicate-effect risk.

## Submission format

Submit Module 03 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
