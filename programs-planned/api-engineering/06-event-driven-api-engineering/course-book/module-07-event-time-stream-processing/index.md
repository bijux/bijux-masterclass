# Module 07 — Event-Time Stream Processing, Windows, Watermarks, and Corrections

> **Program stage:** Course 6 of 10 — Extend the promise across asynchronous time.

> **Central question:** How do event time, processing time, windows, watermarks, lateness, and corrections affect derived results?

## Where this module fits

Module 06 produced **Build notification, analytics, audit, and orchestration consumers with stable derived-command identities and explicit state**. This module extends that result by asking: **How do event time, processing time, windows, watermarks, lateness, and corrections affect derived results?**

The new capstone increment is **Implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine**. It becomes the prerequisite for **Event Security, Multi-Tenancy, Privacy, and Trust**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Distinguish event time, ingestion time, processing time, and observation time.
- Choose tumbling, sliding, or session windows from the business question.
- Define a watermark as a completeness heuristic rather than a fact that no earlier event exists.
- Handle allowed lateness with revisioned outputs.
- Record beyond-lateness events instead of silently discarding them.
- Deduplicate event-time aggregates by stable event identity.
- Make window state and checkpoints replayable and versioned.
- Explain the difference between operational metrics and business stream projections.

## Capstone increment

Implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine.

## Core event model

### 1. Time fields answer different questions

Event time answers when the fact became true in the domain. Ingestion time answers when the event
backbone accepted the record. Processing time answers when one consumer handled it. Observation time
answers when an operator or monitoring system recorded a measurement.

A broker outage can leave event time unchanged while ingestion and processing happen hours later. A
replay makes processing time current for old facts. These times should not be substituted silently.

The completed-run event carries a domain completion timestamp in its payload and a CloudEvents `time`
for the integration fact. The window policy states which one is authoritative for the aggregate.

### 2. Windows encode a business question

A tumbling window divides time into non-overlapping intervals and answers questions such as “how many
runs completed in each five-minute period?” A sliding window overlaps intervals and supports rolling
rates. A session window groups activity separated by inactivity and requires key-specific state.

The course implements tumbling windows because they expose event-time and lateness semantics without
introducing every stream-processing feature. Choosing a window because a library defaults to it is not
a design argument.

Window width, timezone, boundary inclusion, event types, tenant grouping, and aggregation formula are
versioned policy.

### 3. A watermark is an estimate of completeness

A watermark states that the processor does not expect events earlier than a threshold under normal
conditions. It may be derived from maximum observed event time minus a delay allowance, partition
progress, or an upstream source watermark.

It does not prove no older event will ever arrive. Networks recover, offline producers reconnect, and
operators replay history. The late-data policy decides whether an arrival before the watermark can
revise a result, be routed to correction, or be rejected.

Advancing the watermark too aggressively creates false completeness; too slowly delays final results
and retains more state.

### 4. Allowed lateness creates revisioned outputs

A window may emit an initial result when the watermark passes its end, then accept corrections for an
allowed-lateness period. Each accepted late event updates the aggregate and increments a revision. A
downstream consumer can upsert by `(window_start, window_end, key, revision)` or by stable window ID with
monotonic revision.

Emitting a second indistinguishable “final” result can double-count downstream. Revision is part of the
output contract.

Beyond the allowed period, the event is recorded as too late with safe metadata and enters a correction
workflow. Silent drop hides data quality loss.

### 5. Duplicates and late events are independent dimensions

A duplicate may arrive immediately or months later. A late event may be unique. Deduplicate by stable
event/effect identity before updating the window. Do not deduplicate by timestamp, payload equality, or
broker offset.

During replay into a new projection version, the inbox/effect namespace changes intentionally so every
historical event can apply once to the new state. Within that replay, duplicate event IDs still apply
once.

Deduplication state must be retained at least as long as the replay/duplicate horizon or reconstructed
from checkpointed state.

### 6. Window state is durable application state

A serious stream processor checkpoints window aggregates, deduplication identity, watermark, source
positions, policy version, and output revision atomically or under a recoverable protocol. A crash after
output but before checkpoint can duplicate output; a crash after checkpoint but before output can lose
it. An output outbox or transactional stream platform closes that boundary.

The dependency-light model keeps state in memory to teach semantics. The course labels it non-durable.
The database/broker design exercise specifies how to store checkpoints and output intents.

State growth is bounded by active windows, keys, lateness, and retention. Unbounded distinct keys can
exhaust memory even with small event volume.

### 7. Corrections preserve transparency

A too-late event, corrected source event, or discovered processing defect may require recomputation.
Corrections are versioned outputs with reason and source evidence. Rewriting a previously published
aggregate without revision makes downstream state impossible to audit.

For a large correction, rebuild an isolated projection from a bounded event range and compare before
cutover. For one event, a targeted correction may update one window.

The policy distinguishes source correction, late arrival, and algorithm-version correction because they
imply different ownership and release decisions.

### 8. Business projections are not observability metrics

Completion rate computed from business events is a durable product/operational projection with replay
and correction semantics. Request latency from instrumentation is an observability metric with bounded
labels and sampling/aggregation behavior. Both may appear on a dashboard, but their sources and truth
claims differ.

Telemetry loss should not rewrite business completion counts. Conversely, an event projection should not
be used to infer HTTP latency or dependency saturation.

Course 4’s rule remains: telemetry helps diagnose; durable state and event facts prove business outcomes.

## Engineering requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Time source declared | Every aggregate names its event-time field and timezone. | Replay or delay moves facts into wrong periods. | Window policy |
| Window semantics versioned | Width, boundaries, key, types, and formula are explicit. | Consumers calculate incompatible totals. | Policy and fixture results |
| Watermark bounded | Watermark algorithm and delay are documented per source/partition. | Results finalize too early or state never closes. | Watermark vectors |
| Late-data policy | Accepted lateness revises output; excessive lateness is recorded. | Data disappears silently or endlessly mutates history. | Late-event store and revision test |
| Stable dedupe | Each event applies once per stream effect version. | Redelivery inflates aggregates. | Seen-event state |
| Durable checkpoint design | State, source position, and output intent have a recoverable boundary. | Crash loses or duplicates window output. | Checkpoint failure table |
| Business/telemetry separation | Projection claims and monitoring metrics name distinct sources. | Missing telemetry becomes missing business truth. | Source map and dashboard review |

## Worked failures

### Case 1 — processing-time windows during replay

A month of completion events is replayed today and all counts appear in today’s windows. Use the declared
event-time field. Processing time may still measure replay throughput, but not business completion time.

### Case 2 — watermark treated as certainty

The processor drops an event one second behind the watermark even though the allowed-lateness policy is
ten minutes. A watermark triggers initial completeness; allowed lateness determines revision eligibility.

### Case 3 — duplicate inflated duration

A redelivered completion increments count and total duration again. Apply effect-scoped event-ID dedupe
before aggregation, then acknowledge duplicate as already applied.

### Case 4 — correction overwrote output silently

A late event changes a published total with no revision or reason. Downstream consumers cannot tell
whether they saw old or new truth. Emit/upsert a higher revision and retain correction provenance.

## Python implementation

`EventTimeWindows` receives completed and failed events, derives a UTC tumbling-window start, checks
deduplication, compares event time with the watermark/allowed-lateness policy, and updates revisioned state.

```text
capstone/tracks/python-fastapi/src/event_engineering/stream.py
capstone/tracks/python-fastapi/tests_event/test_stream_security.py
```

The clock and watermark are explicit inputs. Tests use fixed timestamps at boundaries, late-but-accepted
cases, too-late cases, and duplicates. Avoid `datetime.now()` inside aggregation.

The returned `WindowResult` is a projection record, not a telemetry sample.

## TypeScript implementation

The TypeScript implementation parses timestamps into integer milliseconds only after validating range and
timezone. It computes boundaries with integer arithmetic and rejects unsafe values.

```text
capstone/tracks/typescript-fastify/src/event-engineering/stream.ts
capstone/tracks/typescript-fastify/test-event-core/evolution-stream.test.mjs
```

Do not rely on local timezone defaults in `Date`. Every fixture uses `Z` or an explicit offset and normalizes
to UTC. Revision and count serialization preserve integer safety.

## Cross-language invariant

For the same ordered or shuffled fixture events, both tracks produce identical windows, counts, total
duration, revisions, duplicate decisions, and late-event classifications. Processing order may differ; final
effect for the declared policy must match.

Shared vectors include boundary timestamps, duplicates, late accepted events, and beyond-lateness records.

## Design review

Review a stream projection by writing the mathematical function first: key, event-time extractor, window
assignment, aggregation, watermark, lateness, correction, and output identity. Then inspect state size,
checkpoint boundary, replay mode, and external outputs.

If the team cannot explain how one late event changes one previously emitted result, the stream contract is
not complete.

## End-to-end worked example

Completed events for 10:00:10 and 10:04:55 enter the 10:00–10:05 window. A failed event at 10:02 increments
failure count. The watermark advances to 10:05:30 and an initial revision is published.

A unique completed event with event time 10:04:40 arrives at processing time 10:07, within ten minutes of
allowed lateness. The window increments completion/duration and emits revision 2. A duplicate of the first
event is ignored. An event from 09:30 is beyond policy and enters the late-event store for correction review.

Replaying the same fixture into analytics v2 yields the same final revisioned aggregate because the function
depends on event facts and versioned policy, not wall clock.

## Failure patterns

- **Processing-time default.** Delayed or replayed facts enter the wrong business period.
- **Watermark certainty.** Events behind a heuristic threshold are silently discarded.
- **No revision.** Late corrections are indistinguishable duplicates or overwrite history.
- **Timestamp dedupe.** Distinct facts at one time are suppressed while true duplicates still pass.
- **Unbounded keys.** Window state grows without a cardinality or retention budget.
- **In-memory checkpoint claim.** A semantic example is described as durable production processing.
- **Telemetry conflation.** Instrumentation metrics are treated as authoritative business aggregates.

## Module synthesis

You are ready to leave this module when you can **distinguish event time, ingestion time, processing time, and observation time, choose tumbling, sliding, or session windows from the business question, and define a watermark as a completeness heuristic rather than a fact that no earlier event exists** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Plant a processing-time implementation and show that replay moves historical events into the wrong window** and requiring the following oracle: **Both correct runs converge on the same final windows and revisions. The accepted late event changes exactly one window, the duplicate changes none, and the too-late event enters a durable late record. Planted processing-time and no-dedupe implementations fail their expected oracles.**

The cumulative platform now includes **Implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Event Security, Multi-Tenancy, Privacy, and Trust](../module-08-event-security-and-multitenancy/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
