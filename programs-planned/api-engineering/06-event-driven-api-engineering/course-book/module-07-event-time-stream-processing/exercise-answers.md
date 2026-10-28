# Worked Answers — Module 07: Event-Time Stream Processing, Windows, Watermarks, and Corrections

Use these solutions to audit your reasoning for **Event-Time Stream Processing, Windows, Watermarks, and Corrections**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Name four clocks

Event time is the authoritative completion instant in the fact; ingestion time is when the recovered broker accepts it; processing time is when analytics handles it; observation time is when a metric/log records that handling. The outage can make the latter three hours later while event time remains unchanged.

The chapter’s decisive distinction is this: Event time answers when the fact became true in the domain. Ingestion time answers when the event backbone accepted the record. Processing time answers when one consumer handled it. Observation time answers when an operator or monitoring system recorded a measurement.

## 2. Choose a window

Use tumbling five-minute windows for non-overlapping totals, sliding 30-minute windows for a continuously updated failure rate, and session windows keyed by user/tenant with an inactivity gap for upload sessions. Each needs explicit boundary and late-data policy.

In the cumulative capstone, the rule becomes concrete: A tumbling window divides time into non-overlapping intervals and answers questions such as “how many runs completed in each five-minute period?” A sliding window overlaps intervals and supports rolling rates. A session window groups activity separated by inactivity and requires key-specific state.

## 3. Define a watermark

A conservative source watermark can be the minimum partition watermark, where each partition uses maximum observed event time minus delay. An idle partition can stall it, so use an explicit idle-partition policy only after proving no pending source data or using broker progress. Never advance solely because wall time passed.

A useful way to reason about the boundary is: A watermark states that the processor does not expect events earlier than a threshold under normal conditions. It may be derived from maximum observed event time minus a delay allowance, partition progress, or an upstream source watermark.

## 4. Handle late-but-accepted data

Use stable window identity `(projectionVersion, key, start, end)` and increment monotonic revision. Recompute the aggregate with the event applied once and publish/upsert revision 2 with reason `late-arrival`. Downstream ignores older revisions.

The implementation consequence is: A window may emit an initial result when the watermark passes its end, then accept corrections for an allowed-lateness period. Each accepted late event updates the aggregate and increments a revision. A downstream consumer can upsert by (window start, window end, key, revision) or by stable window ID with monotonic revision.

## 5. Handle too-late data

Store event ID/type/subject, source position, window identity, lateness amount, classification, policy version, safe reason, and received time. Do not mutate the window automatically. The runbook decides targeted correction, isolated rebuild, or accepted loss with owner approval.

The important nuance is: A unique completed event with event time 10:04:40 arrives at processing time 10:07, within ten minutes of allowed lateness. The window increments completion/duration and emits revision 2. A duplicate of the first event is ignored. An event from 09:30 is beyond policy and enters the late-event store for correction review.

## 6. Separate duplicate and late

An immediate redelivery of the same event ID is on time but duplicate and applies zero effect. A first delivery of a unique event from four minutes ago may be late but within policy and applies one revision. Lateness and identity are orthogonal.

Under concurrency or failure, the distinction becomes: A duplicate may arrive immediately or months later. A late event may be unique. Deduplicate by stable event/effect identity before updating the window. Do not deduplicate by timestamp, payload equality, or broker offset.

## 7. Plan a checkpoint

Persist aggregate state, seen-event identity, watermark/source positions, policy/effect version, output revision, and output outbox intent in one transaction or recoverable protocol. Otherwise restart can lose or duplicate output.

The design remains honest only if: A serious stream processor checkpoints window aggregates, deduplication identity, watermark, source positions, policy version, and output revision atomically or under a recoverable protocol. A crash after output but before checkpoint can duplicate output; a crash after checkpoint but before output can lose it. An output outbox or transactional stream platform closes that boundary.

## 8. Prevent output duplication

Write revision state and an output outbox row atomically, then let a relay publish. A crash after publish may duplicate the same output event ID/revision, which downstream dedupes. Do not mark checkpoint complete before durable output intent.

The consumer-facing consequence is: A serious stream processor checkpoints window aggregates, deduplication identity, watermark, source positions, policy version, and output revision atomically or under a recoverable protocol. A crash after output but before checkpoint can duplicate output; a crash after checkpoint but before output can lose it. An output outbox or transactional stream platform closes that boundary.

## 9. Correct an algorithm

Create projection algorithm v2 and rebuild into an isolated target. Publish correction/replacement outputs with new effect version and revision/provenance, compare with v1, then switch readers. Preserve v1 outputs and defect report; do not mutate them silently.

The operational consequence is: A too-late event, corrected source event, or discovered processing defect may require recomputation. Corrections are versioned outputs with reason and source evidence. Rewriting a previously published aggregate without revision makes downstream state impossible to audit.

## 10. Bound state

Dimensions include active windows, tenant/key cardinality, allowed lateness, dedupe horizon, event rate, and projection versions. Bound with allowed keys, aggregation hierarchy, retention/expiry, partitioning, snapshots, and explicit rejection/overflow policy.

The strongest engineering interpretation is: During replay into a new projection version, the inbox/effect namespace changes intentionally so every historical event can apply once to the new state. Within that replay, duplicate event IDs still apply once.

**Evidence.** Exercise source authorization, canonical bytes, correlation/causation identity, consumer-group independence, and failure recovery in both tracks.

## 11. Protect replay determinism

Replace current time with event time, random IDs with derived stable IDs, unordered iteration with canonical order, mutable remote lookups with versioned immutable reference data, and environment-dependent configuration with a recorded policy version. Also avoid floating-point nondeterminism where exact totals matter.

The defect-oriented view is: A month of completion events is replayed today and all counts appear in today’s windows. Use the declared event-time field. Processing time may still measure replay throughput, but not business completion time.

## 12. Separate business and telemetry

The event projection derives from durable run facts and can rebuild/correct business completion history. OpenTelemetry request count measures observed HTTP/consumer operations and may be sampled or lost. It diagnoses throughput but cannot prove how many runs completed.

Across the Python and TypeScript tracks, the invariant is: Completion rate computed from business events is a durable product/operational projection with replay and correction semantics. Request latency from instrumentation is an observability metric with bounded labels and sampling/aggregation behavior. Both may appear on a dashboard, but their sources and truth claims differ.
