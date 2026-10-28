# Reference Answers — Module 07: Worked answers — Module 07 — Event-Time Stream Processing, Windows, Watermarks, and Corrections

Read after attempting all twelve Event-Time Stream Processing, Windows, Watermarks, and Corrections exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Name four clocks

Event time is the authoritative completion instant in the fact; ingestion time is when the recovered broker accepts it; processing time is when analytics handles it; observation time is when a metric/log records that handling. The outage can make the latter three hours later while event time remains unchanged.

## 2. Choose a window

Use tumbling five-minute windows for non-overlapping totals, sliding 30-minute windows for a continuously updated failure rate, and session windows keyed by user/tenant with an inactivity gap for upload sessions. Each needs explicit boundary and late-data policy.

## 3. Define a watermark

A conservative source watermark can be the minimum partition watermark, where each partition uses maximum observed event time minus delay. An idle partition can stall it, so use an explicit idle-partition policy only after proving no pending source data or using broker progress. Never advance solely because wall time passed.

## 4. Handle late-but-accepted data

Use stable window identity `(projectionVersion, key, start, end)` and increment monotonic revision. Recompute the aggregate with the event applied once and publish/upsert revision 2 with reason `late-arrival`. Downstream ignores older revisions.

## 5. Handle too-late data

Store event ID/type/subject, source position, window identity, lateness amount, classification, policy version, safe reason, and received time. Do not mutate the window automatically. The runbook decides targeted correction, isolated rebuild, or accepted loss with owner approval.

## 6. Separate duplicate and late

An immediate redelivery of the same event ID is on time but duplicate and applies zero effect. A first delivery of a unique event from four minutes ago may be late but within policy and applies one revision. Lateness and identity are orthogonal.

## 7. Plan a checkpoint

Persist aggregate state, seen-event identity, watermark/source positions, policy/effect version, output revision, and output outbox intent in one transaction or recoverable protocol. Otherwise restart can lose or duplicate output.

## 8. Prevent output duplication

Write revision state and an output outbox row atomically, then let a relay publish. A crash after publish may duplicate the same output event ID/revision, which downstream dedupes. Do not mark checkpoint complete before durable output intent.

## 9. Correct an algorithm

Create projection algorithm v2 and rebuild into an isolated target. Publish correction/replacement outputs with new effect version and revision/provenance, compare with v1, then switch readers. Preserve v1 outputs and defect report; do not mutate them silently.

## 10. Bound state

Dimensions include active windows, tenant/key cardinality, allowed lateness, dedupe horizon, event rate, and projection versions. Bound with allowed keys, aggregation hierarchy, retention/expiry, partitioning, snapshots, and explicit rejection/overflow policy.

## 11. Protect replay determinism

Replace current time with event time, random IDs with derived stable IDs, unordered iteration with canonical order, mutable remote lookups with versioned immutable reference data, and environment-dependent configuration with a recorded policy version. Also avoid floating-point nondeterminism where exact totals matter.

## 12. Separate business and telemetry

The event projection derives from durable run facts and can rebuild/correct business completion history. OpenTelemetry request count measures observed HTTP/consumer operations and may be sampled or lost. It diagnoses throughput but cannot prove how many runs completed.
