---
module_id: LSDS-044
program: Large-Scale Data Systems Engineering
level: 1
module_number: 44
title: Event-Time Processing
status: complete
last_verified: 2026-09-04
---

# Event-Time Processing

## One-Page Review

### Governing question

How can a large-scale data system compute according to when events occurred while records arrive late, early, duplicated, corrected, backfilled, and stamped by clocks with different meanings, precision, trust, and uncertainty?

### Essential definitions

- **event time** is the application-defined time at which a represented occurrence happened or became effective; it is a field with provenance, not an engine clock.
- **capture time** records when a source observed or serialized the occurrence. It can differ from the occurrence itself.
- **ingestion time** records when an intermediary such as a broker accepted or appended the record.
- **processing time** is the runtime clock when an operator handles a record. It is operationally useful but replay-dependent.
- **publication time** records when a durable result became visible to its consumer.
- **clock domain** identifies the clock and semantics that produced a timestamp, including unit, epoch, precision, offset/zone, synchronization, and uncertainty.
- **arrival lateness** for record $i$ is $\ell_i=a_i-e_i$, where $a_i$ is comparable arrival time and $e_i$ is normalized event time. It may be negative because of clock skew, bad data, or a future-effective event.
- **out-of-order arrival** means arrival order differs from the event-time order required by a computation; it does not by itself identify which timestamp is wrong.
- A **watermark** is a system's claim about event-time progress, not the maximum timestamp observed. LSDS-045 develops that claim and its uncertainty.
- A **temporal correction** changes a previously recorded event time or effect interval while preserving lineage to the superseded assertion.

### Central model, mechanism, or theorem

Represent each record $r_i$ with immutable identity and a timestamp envelope:

$$E_i=(x_i,u_i,z_i,q_i,o_i,\epsilon_i,v_i),$$

where $x_i$ is the raw value, $u_i$ its unit/epoch, $z_i$ offset or civil-time zone context, $q_i$ precision, $o_i$ origin and clock domain, $\epsilon_i$ stated uncertainty, and $v_i$ the normalization-rule version. A deterministic normalizer either rejects/quarantines the envelope or produces a UTC instant or bounded interval $[e_i^-,e_i^+]$ without discarding the raw evidence.

For capture $c_i$, broker arrival $a_i$, first processing $p_i$, and durable publication $d_i$, useful comparable-clock measures include transport delay $a_i-c_i$, queue delay $p_i-a_i$, and freshness $d_i-e_i$. They are not universally nonnegative or comparable. The system must declare which clocks are trusted and which differences are meaningful.

Event-time computation is replayable when window/key assignment and state transitions are deterministic functions of recorded inputs, stable tie-break identity, captured reference data, and versioned rules—not the current wall clock. Completeness cannot be inferred from one event timestamp; it needs an explicit progress mechanism, lateness policy, or bounded input.

### Critical invariants

- Every timestamp carries semantic name, source, unit, epoch, precision, offset/zone treatment, uncertainty, validation state, and rule version.
- Raw timestamp evidence is retained when normalization can be corrected or audited; normalized values never erase provenance.
- Event time is distinct from capture, ingestion, processing, checkpoint, and publication time.
- Event-time order is distinct from source offset order, record identity, transaction order, and causality.
- Replay uses recorded temporal facts and pinned rules; `now`, host zone, locale, and mutable lookup data do not silently change results.
- Invalid, ambiguous, implausibly old, and future timestamps follow explicit reject, quarantine, correction, or bounded-clamp policy.
- Late-data acceptance, update, retraction, side-output, quarantine, and drop behavior is part of the result contract and is observable.
- Backfills and retries preserve original event time and identity while recording new attempt/arrival time.
- Multi-input operations define comparable time domains, skew bounds, idle-input behavior, and deterministic tie-breaking.
- Time-based authorization, retention, billing, and deletion never trust an unauthenticated producer timestamp alone.

### Common failures

Common failures include naming every timestamp `timestamp`; treating broker append time as occurrence time; parsing local civil time without a zone or ambiguity policy; silently converting seconds as milliseconds; inventing precision; assuming synchronized clocks; sorting solely by event time; treating the maximum observed timestamp as complete progress; using processing time during replay; overwriting the raw value after normalization; clamping bad timestamps without audit; dropping late data without a count and reason; extending a retry's event time to “now”; using a producer timestamp for authorization or retention; assigning an uncertain event to one boundary window without policy; computing averages that hide long lateness tails; and joining streams whose clocks are not comparable.

### Compact example

Four records have `(event, arrival)` seconds `(100,112)`, `(115,113)`, `(90,140)`, and `(125,130)`. Their arrival lateness values are `12`, `-2`, `50`, and `5`. With a 15-second operational threshold, the first and fourth are within threshold, the second is future-skewed, and the third is late. The sorted distribution `(-2,5,12,50)` has median `8.5`, but that median does not authorize dropping the 50-second tail. Sixty-second event-time windows start at 60, 60, 60, and 120 regardless of arrival order; whether the late update may revise the first window is a separate result policy.

### Connections

[LSDS-041](041-logs-as-distributed-input.md) and [LSDS-042](042-partitioned-consumption.md) establish input identity and progress; [LSDS-043](043-stateful-operators.md) establishes retained state and timers. [LSDS-045](../ROADMAP.md) turns timestamp evidence into watermark progress, [LSDS-046](../ROADMAP.md) defines windows and triggers, and [LSDS-047](../ROADMAP.md) through [LSDS-050](../ROADMAP.md) connect temporal computation to recovery and effects.

## Governing Question

Business questions are usually about the world, not the worker. How many orders were placed during a promotion? Which sensor readings preceded a fault? What was an account's exposure at market close? The record representing an occurrence may reach the system seconds, days, or months later. Mobile devices disconnect, brokers buffer, partitions retry, historical files are backfilled, and facts are corrected.

Processing-time systems answer a different question: what did this machine see during this execution interval? That answer can be useful for operational rate limiting or resource cleanup, but it changes when the same input is replayed at a different speed. Event-time processing instead assigns records and state transitions according to an application time recorded with the data.

The difficult part is not extracting a date field. A timestamp has meaning only with provenance, units, clock assumptions, precision, and correction rules. Two sources can both emit ISO-looking values while one means device observation and the other means broker receipt. A local time can occur twice during a daylight-saving transition or never occur during a spring gap. Producer clocks can drift or be maliciously set into the future.

The governing question is how to preserve trustworthy temporal evidence, normalize it deterministically, reason about order and lateness without pretending certainty, and expose policies that remain correct through retries, backfills, late arrivals, multi-stream joins, replay, and lifecycle decisions.

## Why This Matters

Event time makes historical and continuous computation comparable. A daily revenue aggregate can place a sale in the same business interval whether it arrives immediately or after an outage. A replay can reproduce the original classification. A temporal join can correlate observations according to when they occurred rather than whichever worker happened to run first.

Bad time semantics produce quiet corruption. Unit confusion can send records to 1970 or millennia ahead. A device clock five minutes fast can advance apparent progress and cause valid records from healthy devices to look late. A timestamp overwritten during a retry moves the event into a different window and prevents deterministic reconciliation. A join can miss matches because one stream uses occurrence time while another uses capture time.

Time also controls state and effects. Windows, timers, deduplication horizons, retention, service-level freshness, pricing intervals, access validity, and deletion policies all depend on clocks. A decision that is harmless for a dashboard may be unacceptable for invoices or regulatory records. “Ignore events older than 24 hours” is unsafe until the system declares older according to which clock, measured where, with what uncertainty, and with what appeal/correction path.

At scale, temporal distributions shape cost. The tail of lateness determines how long joins and windows retain state. Slow or idle partitions can hold back progress. Permitting corrections increases downstream update traffic. Conservatively waiting improves completeness but raises latency and state. Event time therefore couples product semantics, distributed-systems correctness, capacity, security, and user-visible trust.

## Prerequisites and Retrieval

Retrieve stable identity, partitioning, serialization, integrity, and scale reasoning from [LSDS-002](002-horizontal-partitioning.md) through [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md). Review input/log identity in [LSDS-041](041-logs-as-distributed-input.md), partition ownership and offsets in [LSDS-042](042-partitioned-consumption.md), and managed state/timers in [LSDS-043](043-stateful-operators.md).

You should understand UTC instants, local civil time, offsets, time zones, epoch units, monotonic versus wall clocks, quantiles, deterministic replay, stable record identity, state retention, and at-least-once delivery. Watermarks, windows, triggers, and consistent snapshots are introduced only enough to expose their dependency on the timestamp contract; later modules develop their mechanisms.

## Learning Objectives

After this module, you should be able to:

1. distinguish event, capture, ingestion, processing, checkpoint, and publication time;
2. design a timestamp envelope that preserves raw value, units, zone context, precision, origin, uncertainty, validation, and rule version;
3. normalize instants and bounded intervals deterministically without inventing unavailable precision;
4. separate event-time order from arrival order, source offsets, identity, transaction order, and causality;
5. calculate and interpret transport, queue, freshness, and arrival-lateness distributions with clock caveats;
6. specify policies for invalid, future, old, ambiguous, corrected, duplicate, retried, and backfilled timestamps;
7. make replay independent of wall clock, host locale, mutable time-zone data, and uncaptured reference state;
8. define late-data outcomes and correction/retraction semantics before selecting a watermark/window mechanism;
9. align multiple streams only when their timestamp domains and uncertainties are compatible; and
10. observe, test, secure, retain, and govern temporal evidence across the full data lifecycle.

## Core Exposition

### Name every temporal fact

Do not begin with one generic `timestamp` column. Name the business occurrence or effective time, source capture time, connector read time, broker append time, operator processing time, checkpoint completion time, result commit time, and consumer observation time when each exists. A record may carry only some of them, but absence is better than false equivalence.

Event time is defined by the application. For a purchase it might be authorization, checkout, settlement, or effective accounting date. For a sensor it might be physical sampling or device serialization. Write the governing question and choose the fact that answers it. If different consumers need different meanings, retain multiple named fields rather than repeatedly overwriting one canonical column.

Processing time comes from the executing runtime and changes with scheduling and replay. Ingestion time comes from an infrastructure boundary and can be a useful trustworthy fallback, but it answers when infrastructure accepted data. Neither substitutes invisibly for missing event time.

### Capture provenance before normalization

A timestamp envelope should preserve raw value, declared unit and epoch, input representation, source field/schema, producer and clock domain, offset or zone identifier, precision, uncertainty, and parsing/normalization version. Record whether the time was producer-declared, gateway-stamped, broker-stamped, or inferred.

For example, integer `1710000000` is uninterpretable without seconds versus milliseconds and an epoch. `2026-10-25 02:30` is ambiguous in zones that repeat that civil interval. `2026-03-29 02:30` may be nonexistent in a zone that jumps forward. An offset such as `+02:00` fixes an instant but does not preserve the named civil zone and its historical/future rules.

Keep raw evidence when later rules may improve interpretation. Normalization is derived data. A corrected rule can produce a new normalized version and lineage rather than silently mutating history.

### Normalize without inventing certainty

Normalize comparable instants to a documented UTC representation with explicit resolution. Do not attach `.000` microseconds to second-resolution data and then imply microsecond accuracy. Preserve the original precision and uncertainty separately from storage resolution.

RFC 3339 describes a constrained Internet timestamp representation with numeric offsets and an explicit unknown-local-offset convention. RFC 9557 extends Internet timestamps with bracketed time-zone information and critical annotations. A parser contract still must say which forms, leap-second values, offset/zone inconsistencies, and unknown offsets it accepts.

Some sources justify an instant only within interval $[e_i^-,e_i^+]$. Clock synchronization error, batch sampling, rounded dates, or business-effective intervals create genuine uncertainty. Store the interval or quality class. If it crosses a window boundary, policy may assign conservatively, duplicate into candidate intervals with reconciliation, or quarantine; choosing its midpoint silently creates false precision.

### Treat event time as evidence, not truth

Producer timestamps can be wrong through drift, reset, stale firmware, parsing errors, manual entry, or adversarial manipulation. Validate against source capabilities and independent infrastructure time. Useful checks include parseability, expected range, maximum future skew, historical retention horizon, monotonicity where promised, precision, offset/zone consistency, and disagreement with gateway or broker time.

A check detects inconsistency; it does not automatically identify the correct clock. If a mobile device reports an event ten minutes ahead of broker time, the device may be fast, the gateway may be delayed, or the event may intentionally be future-effective. Policy should classify the evidence and preserve both values.

Fallback from missing event time to ingestion time can keep a pipeline flowing, but it changes semantics. Mark the fallback, measure it, and decide whether consumers may combine inferred and native event time.

### Separate time, order, identity, and causality

Equal or increasing event timestamps do not provide a total order. Clock precision can collapse many events to one value. Independent producers can stamp the same instant. A clock can move backward. A later correction can describe an earlier occurrence.

Use stable source identity and offset/sequence for deterministic tie-breaking where available. A source partition offset orders log records in that partition, not occurrences across partitions. A database transaction commit order is not necessarily the order business facts occurred. Record identity decides duplication; event time alone cannot.

Causality requires domain evidence such as a parent identifier, transaction dependency, or logical/vector clock. If event A has an earlier physical timestamp than B, that does not prove A caused B. Never use timestamp sorting alone as a causal proof.

### Measure out-of-order arrival explicitly

Let $e_i$ be a normalized event instant and $a_i$ a comparable ingestion instant. Define arrival lateness $\ell_i=a_i-e_i$. Positive values mean the system received the record after its stated event time; negative values signal future-effective data, skew, or error. Do not coerce negatives to zero before investigating them.

Capture time $c_i$, first processing time $p_i$, and publication time $d_i$ permit further decomposition where clocks are comparable:

$$\text{transport}_i=a_i-c_i,\qquad \text{queue}_i=p_i-a_i,\qquad \text{freshness}_i=d_i-e_i.$$

These differences may include clock error and semantics, not only system delay. An old backfill has huge arrival lateness even when current transport and queue delays are tiny. A retry keeps original $e_i$ but receives a new attempt/arrival time.

### Use distributions and cohorts

Report lateness and freshness as distributions by source, partition, schema, tenant, geography, event type, connection mode, and time. Median behavior can look excellent while a small tail dominates state and correctness. Track high quantiles, maximum under a defined interval, negative counts, invalid counts, missing/fallback counts, and histogram overflow.

Quantile method, observation interval, sample weighting, and censoring matter. Per-record aggregation lets one noisy producer dominate. Per-partition maxima expose a stalled shard. Bucket boundaries should cover backfills without destroying resolution for normal traffic.

Correlate lateness with broker lag, retries, outages, deployment, clock-quality metadata, and watermark delay. Cardinality-safe labels and protected identifiers prevent telemetry from leaking raw customer or device data.

### Validate range, precision, and uncertainty

Range checks require semantics. An event older than product launch might be impossible for live input but valid in a migration. A future timestamp might be invalid for a physical sensor yet valid for a scheduled price. Separate live, correction, simulation, and backfill channels or carry an authorized mode.

Define strict boundaries: whether exactly the maximum future skew is accepted, how leap seconds are handled, whether offset-zone disagreement rejects, and whether rounding happens before or after range comparison. Test minimum/maximum representable values and integer overflow when converting seconds to nanoseconds.

If uncertainty is represented by an interval, comparisons can be definitely before, definitely after, or overlapping. A binary comparator that ignores overlap breaks transitivity or invents order. Keep deterministic storage order separate from semantic temporal comparison.

### Make replay time-invariant

Given the same qualified record sequence, initial state, code/rule versions, and captured reference inputs, event-time assignment should reproduce. Do not call the current wall clock to repair missing event time, select a window, or decide whether an event is late during replay.

Pin or record the time-zone database and normalization version when civil-time rules affect results. Governments revise zone rules; reprocessing with a new database may legitimately produce a different instant. Treat that as an explicit migration with a diff, not accidental drift.

Capture nondeterministic lookup results such as a tenant's historical time zone or business calendar version. Sorting ties needs a stable identifier rather than runtime arrival order when order affects state. Record mode and cutoff distinguish a bounded historical replay from live processing.

### Preserve backfill and retry semantics

A backfilled 2020 event processed in 2026 still has event time in 2020. Record the backfill job, import time, source snapshot, and lineage separately. Replacing event time with import time makes historical aggregates irreconcilable.

A retry preserves event identity and occurrence time while acquiring a new attempt, transport, and arrival history. Deduplication uses stable identity and a horizon consistent with retries/backfills. If a correction is a new assertion rather than a duplicate, give it its own identity plus a reference to the superseded record.

Backfills may overwhelm live state or reopen closed results. Admission should declare rate limits, allowable historical range, result-update mode, downstream compatibility, and whether progress signals exclude a dedicated backfill stream.

### Define late-data outcomes before mechanisms

“Late” is relative to a declared decision frontier, not merely positive $\ell_i$. A record can arrive after event time but before a result is finalized. Another can arrive milliseconds late relative to a speculative watermark. Policy may accept into open state, update an emitted result, retract and replace, emit a correction ledger, route to review, or drop with reason.

Each choice affects consumers. Upserts require stable result keys and version/conflict rules. Retractions require downstream support and lineage. Append-only sinks may need compensating records. Side outputs need ownership and replay, not an unmonitored dead end. A drop is a data-loss decision requiring metrics, sample-safe diagnostics, and policy authority.

Allowed lateness is not proof that all accepted records are correct or that later records cannot exist. It is an economic/semantic boundary based on observed tails, outage and retry horizons, correction obligations, latency SLOs, state capacity, and downstream contracts.

### Introduce progress cautiously

Seeing an event at time 12:00 does not prove no 11:59 event remains in a delayed partition. Maximum observed event time therefore cannot by itself close work safely. A watermark combines source knowledge or heuristics into a claim about future arrivals, with explicit idleness and partition-merge behavior.

Per-partition progress matters because a single active partition can race ahead while another is delayed. Marking a partition idle can unblock results but creates a contract for its return. Watermark alignment can throttle fast inputs to limit state when streams drift. LSDS-045 develops these mechanisms and their failure boundaries.

Keep timestamp quality separate from progress. Perfectly parsed event times do not establish completeness; a strong source frontier cannot repair a mis-stamped record.

### Align multiple streams deliberately

Temporal joins require both streams to name compatible facts. Joining order placement time to payment settlement time may be correct only with an intentional interval relationship. Joining device occurrence time to server receipt time because both columns say `timestamp` is accidental.

Document each stream's clock domain, precision, skew/uncertainty, correction behavior, and progress. Define inclusive/exclusive interval bounds and stable tie-breaking. One stream's uncertainty may require a wider join range, which increases false candidates and retained state.

For multiple inputs, the effective safe frontier is often constrained by the slowest relevant input. Some runtimes offer minimum or maximum watermark policies; a faster policy can produce earlier output but can also discard matches from a slower stream. Engine defaults are product behavior, not universal semantics.

### Connect event time to state and timers

Event-time windows retain state until progress plus allowed lateness permits cleanup. Event-time timers fire when the runtime's progress mechanism passes their timestamps; they are not precise wall-clock alarms. Recovery may cause overdue timers to fire together. Callbacks and emitted effects therefore need stable identity and idempotency.

State retention must cover normal disorder, outage, retry, backfill/correction, and safety margin. Longer retention improves correction opportunity but costs storage, checkpoints, restore, and privacy exposure. Processing-time TTL can delete event-time state during a pause or replay; event-time cleanup can stall when progress stalls.

Do not confuse event-time completeness with consistent checkpoint recovery. A watermark describes temporal progress; a checkpoint records recoverable computation/input state. Both are required for robust streaming but prove different properties.

### Design corrections and bitemporal history

Some facts have a valid/effective time and a separate system-recorded time. Bitemporal data preserves when a fact was true in the modeled domain and when the system learned or asserted it. This enables “what did we believe then?” as well as corrected historical views.

A correction should retain original identity, corrected value/time, reason, authority, assertion time, and supersession lineage. Decide whether correction order uses system assertion version, source transaction order, or another domain rule. Last-write-by-event-time is often wrong because a correction commonly carries an older valid time.

Materialized outputs need a propagation contract. Versioned upsert, retraction-plus-replacement, or immutable adjustment entries can work; silent in-place changes without provenance make audits impossible.

### Secure time-based behavior

Treat producer time as untrusted input at trust boundaries. An attacker may stamp far-future events to advance naive progress, force long-lived state, bypass “recent event” checks, evade retention, or poison sorted indexes. Far-past timestamps can trigger archival paths or expensive backfills.

Authorization token validity, replay protection, billing cutoff, retention eligibility, and legal deletion should rely on authenticated server time or governed evidence, not a client field alone. Where client occurrence time matters, combine it with server receipt time, bounded skew, identity, nonce/sequence, signature, and review policy.

Protect raw timestamps when they reveal behavior, location, or schedules. Minimize precision where the product does not need it, but preserve evidence required for correctness/audit under appropriate access control. Encryption, retention, deletion, backups, and legal hold apply to raw and derived temporal fields.

### Observe the temporal contract

Emit parse/validation outcomes, timestamp-source/fallback rates, future-skew and lateness distributions, per-partition event-time maxima, progress delay, late acceptance/drop/correction counts, state age, and result freshness. Monitor normalization-rule and time-zone database versions.

Trace a sampled record across capture, ingestion, processing, state update, checkpoint, publication, and observation with stable identifiers. Do not infer end-to-end delay from unrelated host clocks without synchronization metadata. Use monotonic duration clocks for local elapsed time where possible.

Alert on changes in distributions and cohorts rather than one universal threshold. A new producer firmware, zone rule, connector setting, or seconds/milliseconds schema error often appears as a sudden mode shift.

### Validate adversarial temporal behavior

Tests should include equal timestamps, reversed order, negative lateness, exact threshold boundaries, missing offsets, repeated/nonexistent civil times, leap-day and accepted leap-second forms, minimum/maximum instants, unit overflow, precision loss, clock reset, partition pause, idle/resume, retry, duplicate, correction, outage, and historical backfill.

Replay the same captured input at different speeds, host zones, and wall-clock dates; outputs should match under pinned rules. Rehearse time-zone database upgrades and quantify affected records. Inject one partition with a future spike and another with long delay. Verify state bounds, progress, corrections, side outputs, and downstream convergence.

Production readiness requires semantic fixtures from real source formats, observed tail distributions, failure drills, security abuse cases, rollback, and reconciliation against authoritative records. A parser unit test is necessary but far from sufficient.

## Definitions and Notation

For record $r_i$, let:

- $e_i$ be its normalized event instant, or $[e_i^-,e_i^+]$ when uncertainty is explicit;
- $c_i$ be source capture time;
- $a_i$ be trusted infrastructure ingestion/append time;
- $p_i$ be first operator processing time;
- $d_i$ be durable result publication time;
- $s_i$ be stable record/source identity and tie-break evidence;
- $v_i$ be normalization/schema/rule version; and
- $\ell_i=a_i-e_i$ be arrival lateness when both instants are comparable.

An event-time key can be written $K_i=(e_i,s_i)$ for deterministic total storage order; this does not claim causality. A timestamp envelope is $E_i=(x_i,u_i,z_i,q_i,o_i,\epsilon_i,v_i)$: raw value, unit/epoch, zone/offset context, precision, origin/clock domain, uncertainty, and rule version.

For a half-open event-time interval $W=[b,b+\Delta)$, exact event $i$ belongs when $b\le e_i<b+\Delta$. If only $[e_i^-,e_i^+]$ is known, membership is definite only when the full uncertainty interval lies inside under the chosen endpoint convention. Overlap with a boundary requires declared policy.

Let $F$ be a decision frontier such as a watermark. A record is late relative to $F$ when its relevant event-time point or interval is behind the frontier according to the system's comparison rule. This is different from $\ell_i>0$. Let $L$ be allowed lateness after a result frontier; cleanup or finality may require a condition such as $F>b+\Delta+L$, with equality behavior stated explicitly.

## Mechanisms, Invariants, or Proof Structure

Use this review structure for an event-time pipeline:

1. **Question:** identify the business occurrence/effective fact the computation answers.
2. **Envelope:** record raw timestamp, unit, representation, zone/offset, precision, origin, uncertainty, source identity, and version.
3. **Normalization:** deterministically map to an instant/interval or a classified rejection without losing raw evidence.
4. **Validation:** enforce source-specific range, skew, ambiguity, precision, and authorization rules with exact boundaries.
5. **Identity and order:** keep dedup identity, source order, event-time order, assertion order, and causal evidence separate.
6. **Replay:** pin code, schema, time-zone/business-calendar data, tie-breaking, reference inputs, and processing mode.
7. **Progress:** define per-source/partition progress, merge, idleness, restart, and uncertainty independently from timestamp parsing.
8. **Late result policy:** specify accept/update/retract/compensate/quarantine/drop behavior, stable output identity, and consumer support.
9. **State lifecycle:** size retention from disorder/outage/retry/correction evidence and prove cleanup, checkpoint, restore, and privacy behavior.
10. **Evidence:** test boundary/adversarial cases; monitor distributions, cohorts, versions, correction convergence, and protected lineage.

The central replay invariant is functional: with the same qualified records, identities/order, initial state, captured reference values, and rule versions, the event-time computation yields semantically equivalent outputs. Processing speed and wall-clock date are excluded inputs unless explicitly recorded.

The temporal evidence invariant is non-destructive: every normalized instant or interval is traceable to raw value, source, interpretation, and validation version. Corrections add a new assertion with lineage rather than erasing why the old output existed.

The progress invariant is scoped: a frontier is a claim only for named inputs, partitions, versions, and failure/idleness assumptions. It is never inferred merely from the largest event timestamp, and it does not guarantee producer timestamp truth.

The lifecycle invariant is end-to-end: late handling, state cleanup, downstream mutation support, retention, deletion, and audit agree. A runtime that can retract is insufficient if an append-only sink cannot represent the correction.

## Alternatives and Trade-Offs

**Event time** gives replay-stable business placement but needs timestamp quality, progress, state, and corrections. **Processing time** gives simple low-latency execution semantics but replay changes interval placement. **Ingestion time** is infrastructure-controlled and often trustworthy while measuring receipt rather than occurrence.

**One canonical timestamp** simplifies consumers but risks hiding meaning. **Multiple named temporal facts** preserve semantics and diagnostic power at schema/storage/query cost. A semantic view can expose one governed choice without deleting the rest.

**Reject invalid timestamps** protects downstream invariants but may lose availability. **Quarantine** preserves evidence and review at operational cost. **Fallback to ingestion time** keeps flow but mixes semantics unless marked. **Clamping** bounds resource abuse but corrupts placement if treated as truth.

**Strict early finality** lowers latency/state but increases missed late facts. **Long allowed lateness** improves correction coverage but raises state, checkpoint, restore, downstream update, and privacy cost. **Never-final mutable results** preserve openness while complicating consumers and audit.

**Upserts** compact current views but require stable keys/version conflict rules. **Retractions** preserve differential semantics but demand downstream support. **Immutable adjustments** suit ledgers and audit while consumers must compute net state.

**UTC instant only** supports unambiguous comparison. **Instant plus named zone/civil representation** also preserves human/legal context and future scheduling intent. Future local schedules may need re-resolution when zone rules change rather than premature conversion alone.

**Exact timestamps** simplify boundaries when justified. **Uncertainty intervals** are honest and safer but require three-valued comparisons and boundary policy. Inventing precision is simpler only superficially.

**Shared live/backfill input** reuses topology but lets history distort progress and capacity. **Dedicated backfill lanes** isolate controls and rate but require deterministic merge/reconciliation with live results.

## Failure Modes and Misconceptions

1. **“Timestamp means event time.”** The field might be capture, append, processing, or update time.
2. **“ISO format makes time unambiguous.”** A local civil value without offset/zone can repeat or not exist.
3. **“UTC removes clock error.”** UTC representation does not validate the producer clock.
4. **“Storage precision equals measurement accuracy.”** Nanosecond fields can hold second-precision evidence.
5. **“Offsets and zones are interchangeable.”** An offset fixes one instant; a zone carries civil-time rules.
6. **“Event time totally orders events.”** Ties, skew, corrections, and independent clocks require identity/tie-break rules.
7. **“Earlier timestamp proves causality.”** Physical time order is not a causal relation.
8. **“Negative lateness is impossible.”** Future-effective events, skew, and bad data produce it.
9. **“Average lateness sizes state.”** High tails, outages, and partition cohorts dominate.
10. **“Maximum observed time is a watermark.”** It says nothing about delayed partitions or unseen records.
11. **“Allowed lateness guarantees completeness.”** It is a policy boundary, not proof no later record exists.
12. **“Late means drop.”** Updates, retractions, adjustments, quarantine, and review are possible contracts.
13. **“Retry time should replace event time.”** That moves the business fact and breaks replay.
14. **“A backfill is live data arriving now.”** Its arrival is current; its occurrence remains historical.
15. **“Replay can call `now` for missing time.”** Results then depend on execution date.
16. **“Time-zone rules never change.”** Reprocessing can change without a pinned or migrated rule version.
17. **“Processing-time TTL safely cleans event-time state.”** Pauses/replays can expire still-valid temporal state.
18. **“Client time can control security and retention.”** Untrusted timestamps enable replay, bypass, and resource attacks.
19. **“A correction is a duplicate.”** It is a new assertion linked to the superseded fact.
20. **“Runtime retractions solve correction.”** Every downstream store and consumer must represent/converge them.

## Worked Examples

### Example 1

An order record contains `created_at`, `authorized_at`, `broker_append_at`, and `processed_at`. Revenue by purchase intent chooses `authorized_at`; pipeline freshness uses `processed_at-authorized_at`; broker diagnosis uses `processed_at-broker_append_at`. Calling any one field simply `timestamp` destroys these distinctions.

### Example 2

Raw value `1710000000` interpreted as Unix seconds is a 2024 instant; interpreted as milliseconds is in January 1970. A schema contract, magnitude/range validation, and unit-preserving envelope prevent a silent thousandfold error.

### Example 3

A device emits local `2026-10-25 02:30` with zone `Europe/Stockholm`. That civil value occurs twice around the fall-back transition. Without an offset, fold indicator, sequence, or source policy, normalization is ambiguous; selecting the first occurrence silently is not evidence.

### Example 4

For event/capture/arrival/process/publication seconds `(100,108,112,119,130)`, arrival lateness is 12, transport delay is 4, queue delay is 7, and freshness is 30. If event and capture use an unsynchronized device clock while later times use server clocks, only queue delay is directly trustworthy.

### Example 5

An event interval is `[119.8,120.3]` seconds and windows are `[60,120)` and `[120,180)`. The evidence overlaps the boundary, so exact membership is unknown. Policy may quarantine, model both candidates, or use a documented conservative assignment; midpoint placement invents certainty.

### Example 6

A mobile event occurs Monday, is captured offline, and arrives Friday after reconnection. It has large arrival lateness but small device capture delay. A Friday retry retains Monday event time and record identity while recording a new attempt and arrival; deduplication must cover that retry horizon.

### Example 7

One partition reports event time 18:00 while another has delivered only through 17:40. Closing all 17:59 windows from the maximum observation can lose the slow partition's events. Per-partition progress combined under declared idleness is needed before finality.

### Example 8

A result for account/day was emitted as 90. A late correction changes it to 95. A versioned upsert can set 95; a differential stream can emit `-90,+95`; an immutable ledger can emit adjustment `+5`. All need stable identity and consumers that converge on 95.

### Example 9

A client timestamps a request 30 days ahead. A naive maximum-timestamp watermark closes current state, and a timestamp-based retention rule keeps attacker data for 30 extra days. Future-skew validation, bounded progress contribution, server receipt time, and authorization prevent both correctness and resource attacks.

### Example 10

This fixture classifies arrival lateness and assigns deterministic 60-second event-time windows from recorded values.

<!-- bijux-verify: {"id":"event-time-classification","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"on_time=('a', 'd') future=('b',) late=('c',)\nlateness=(-2, 5, 12, 50) median=8.5 maximum=50\nwindows={'a': 60, 'b': 60, 'c': 60, 'd': 120}\n","stderr":""}} -->
```python
from statistics import median

records = (
    ("a", 100, 112),
    ("b", 115, 113),
    ("c", 90, 140),
    ("d", 125, 130),
)
threshold = 15
groups = {"on_time": [], "future": [], "late": []}
lateness = []
windows = {}

for record_id, event_time, arrival_time in records:
    delay = arrival_time - event_time
    lateness.append(delay)
    if delay < 0:
        groups["future"].append(record_id)
    elif delay <= threshold:
        groups["on_time"].append(record_id)
    else:
        groups["late"].append(record_id)
    windows[record_id] = (event_time // 60) * 60

ordered = tuple(sorted(lateness))
print(
    f"on_time={tuple(groups['on_time'])} "
    f"future={tuple(groups['future'])} late={tuple(groups['late'])}"
)
print(
    f"lateness={ordered} median={median(ordered)} "
    f"maximum={max(ordered)}"
)
print(f"windows={windows}")
```

The fixture proves only deterministic arithmetic for exact integer instants and one threshold convention. It does not implement parsing, clock validation, uncertainty, watermarks, distributed state, recovery, time zones, correction propagation, or production quantiles.

## Cross-Program Connections

- **Distributed Systems:** logical/physical clocks, partial order, message delay, partitions, replay, consensus timestamps, and consistent cuts constrain temporal claims.
- **Data Engineering:** CDC, schemas, source timestamps, backfills, deduplication, temporal joins, slowly changing facts, and reconciliation depend on lineage.
- **Database Systems:** valid time, transaction time, bitemporal tables, MVCC, interval queries, correction ledgers, and temporal constraints formalize history.
- **API and Service Engineering:** request deadlines, token validity, idempotency, client/server skew, scheduling, and webhook retries require distinct clocks.
- **Security Engineering:** signed evidence, anti-replay sequence, trusted server time, range validation, retention, minimization, and audit resist timestamp abuse.
- **Reliability Engineering:** freshness SLOs, lag, clock monitoring, stalled partitions, failure injection, recovery, and tail distributions make event time operable.
- **Platform Engineering:** schema registries, time-zone database rollout, runtime watermark APIs, telemetry, tenant controls, and backfill lanes provide shared guardrails.
- **Systems Engineering:** correctness, latency, state, cost, security, policy, human civil time, and downstream mutability form a coupled temporal system.

## References

1. Akidau, T., et al. [“The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing.”](https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/) PVLDB, 2015. Foundational separation of event time and processing time, windowing, triggers, watermarks, and refinement.
2. Apache Beam. [Programming Guide.](https://beam.apache.org/documentation/programming-guide/) Current timestamp, windowing, watermark, trigger, state/timer, and late-data programming contracts.
3. Apache Beam. [Beam Programming Model Basics.](https://beam.apache.org/documentation/basics/) Current conceptual treatment of event time, processing time, windows, watermarks, triggers, and unbounded data.
4. Apache Flink. [Generating Watermarks.](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/) Current timestamp assignment, per-partition watermarks, idleness, alignment, and source integration documentation.
5. Apache Flink. [Built-in Watermark Generators.](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/built_in/) Current monotonous and bounded-out-of-orderness strategy contracts.
6. Apache Flink. [Event Time API Package.](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/api/common/eventtime/package-summary.html) Current interfaces for timestamps, watermark generation, idleness, and alignment.
7. Apache Spark. [Structured Streaming Programming Guide: Event-Time Operations and Watermarks.](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html) Current window, late-data, watermark, state cleanup, and multiple-watermark policy behavior.
8. Apache Spark. [TimerValues API.](https://spark.apache.org/docs/latest/api/java/org/apache/spark/sql/streaming/TimerValues.html) Current distinction between processing-time and event-time timer values.
9. Apache Kafka. [ConsumerRecord API.](https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/consumer/ConsumerRecord.html) Current consumer record timestamp, timestamp type, partition, offset, headers, and identity-adjacent metadata.
10. Apache Kafka. [TimestampType API.](https://kafka.apache.org/43/javadoc/org/apache/kafka/common/record/TimestampType.html) Current create-time, log-append-time, and unavailable timestamp categories.
11. Internet Engineering Task Force. [RFC 3339: Date and Time on the Internet: Timestamps.](https://www.rfc-editor.org/rfc/rfc3339.html) Internet timestamp profile, offsets, unknown local offset, fractional seconds, and leap-second syntax.
12. Internet Engineering Task Force. [RFC 9557: Date and Time on the Internet: Timestamps with Additional Information.](https://www.rfc-editor.org/rfc/rfc9557.html) Named time-zone and other bracketed annotation syntax, consistency, and criticality.
13. Mills, D., et al. [RFC 5905: Network Time Protocol Version 4.](https://www.rfc-editor.org/rfc/rfc5905.html) Clock offset, delay, dispersion, synchronization, and error-bound concepts for networked clocks.

## Exercises

### Exercise 1

Records have `(event,arrival)` seconds `(40,45)`, `(52,49)`, `(30,80)`, `(70,82)`, and `(90,105)`. Compute sorted arrival lateness, median, and classifications under: future if negative, within threshold if `0<=lateness<=12`, late otherwise. Explain why the median cannot authorize cleanup.

### Exercise 2

A source emits Unix integer `1_710_000_000` but its schema omits units. Design a safe normalization/validation policy. State why magnitude guessing alone is insufficient and which evidence the normalized record retains.

### Exercise 3

An uncertain event occupies `[299.7,300.2]` seconds. Tumbling windows are half-open and 60 seconds wide. Determine definite or possible membership around the 300 boundary and propose two honest policies with trade-offs.

### Exercise 4

A live pipeline sees normal p99 lateness 8 minutes, a maximum supported disconnection of 6 hours, a 2-hour catch-up allowance, and 25% margin. Compute an additive planning horizon. Then explain why state retention and allowed lateness need not be identical.

### Exercise 5

Design an event-time readiness review for two joined streams: mobile orders use device local time plus named zone; payments use server UTC receipt time. Include semantics, normalization, uncertainty, identity/order, progress, replay, correction, security, capacity, and verification evidence.

## Answers to the Exercises

### Answer 1

Lateness values are `5`, `-3`, `50`, `12`, and `15`; sorted they are `(-3,5,12,15,50)` and the median is 12 seconds. The future group contains the second record, within-threshold contains the first and fourth, and late contains the third and fifth. The median hides the 50-second tail and says nothing about unseen records, stalled partitions, outage horizons, or a progress frontier, so it cannot justify cleanup.

### Answer 2

Quarantine or require schema/source metadata rather than silently guessing seconds. If a governed source contract establishes Unix seconds, parse with overflow/range checks into a UTC instant while retaining raw integer, seconds/epoch declaration, schema/source and clock origin, precision, uncertainty/quality, validation result, and rule version. Magnitude heuristics overlap across valid ranges and can change as dates or source behaviors evolve; a heuristic fallback must be explicitly marked and reversible.

### Answer 3

The interval overlaps `[240,300)` and `[300,360)`, so neither single-window membership is definite; each is possible. One policy quarantines/requests better evidence, maximizing semantic honesty but delaying or losing aggregation. Another contributes a provisional candidate to both windows and later reconciles or weights it, preserving recall at additional state, double-count protection, and downstream complexity. Assigning to the midpoint's window is acceptable only as an explicit approximation with error semantics.

### Answer 4

The additive base is $8$ minutes $+6$ hours $+2$ hours = 488 minutes. With 25% margin it is $488\times1.25=610$ minutes, or 10 hours 10 minutes. The inputs might overlap rather than add, so production evidence should refine the bound. Allowed lateness controls result mutation/finality, while state retention may also cover dedup retries, corrections, restore, downstream acknowledgment, privacy, or compact tombstones; different state types can therefore need different lifetimes.

### Answer 5

First define whether the join means order occurrence versus payment receipt and the allowed relationship; these are not naturally the same clock fact. Orders retain raw local value, named zone, offset/fold evidence, device identity/clock quality, gateway receipt, precision, uncertainty, and normalization/time-zone-database version. Payments retain server receipt plus transaction identity/order. Specify ambiguous/nonexistent local-time policy, skew/range validation, stable dedup/tie-break identity, per-input progress/idleness, join interval endpoints, uncertainty widening, and late correction/upsert/retraction behavior. Replay pins zone/rules/reference data and never uses current time. Security prevents device time from authorizing payment or advancing progress unchecked. Capacity estimates unmatched-state tails under outage/backfill. Evidence includes civil-time boundaries, skew/future attacks, duplicates/corrections, partition pause/resume, replay across host zones/dates, zone-database migration diffs, state/latency measurements, and authoritative reconciliation.
