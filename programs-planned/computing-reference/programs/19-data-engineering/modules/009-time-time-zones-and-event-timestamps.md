---
module_id: DE-009
program: Data Engineering
level: 1
module_number: 9
title: Time, Time Zones, and Event Timestamps
status: complete
last_verified: 2026-09-02
---

# Time, Time Zones, and Event Timestamps

## One-Page Review

### Governing question

How should a data engineer model, capture, transport, compare and evolve temporal data so that instants, civil times, zones, precision, uncertainty and event semantics remain correct across systems?

### Essential definitions

- An **instant** identifies one point on a timeline under a declared time scale.
- A **local date-time** is a calendar date and wall-clock reading without enough information to identify an instant.
- A **UTC offset** is the numeric difference `local − UTC` at a particular instant; it is not a time-zone rule set.
- A **time-zone identifier** selects a rule history, commonly from the IANA Time Zone Database. Rules and future predictions can change by database release.
- A **zoned date-time** combines a local date-time, zone rules and a resolved offset; an overlap may require an explicit earlier/later choice.
- A **gap** is a range of local readings that does not occur when a civil clock moves forward. A **fold** or overlap is a range that occurs twice when it moves backward.
- **Event time** is when the modeled domain event occurred. **Ingestion time** is when a platform accepted it. **Processing time** is when an operator handled it. These timestamps answer different questions.
- **Resolution** is the smallest representable step. **Precision** describes meaningful or reported granularity. **Accuracy** describes closeness to the intended reference. They are independent.
- A **duration** is elapsed time on a timeline; a **calendar period** changes calendar fields. One day of civil time need not equal 86,400 elapsed seconds across a clock transition.
- A **half-open interval** `[a,b)` includes its start and excludes its end, allowing adjacent windows without double counting.
- A **wall clock** represents civil/system time and can be corrected. A **monotonic clock** is suitable for measuring elapsed time within a running system and does not identify a portable civil instant.

### Central model, mechanism, or theorem

Represent a temporal observation as

$$
T=(kind,value,scale,unit,precision,zone,offset,rules,uncertainty,source).
$$

`kind` identifies event, ingestion, processing, effective or other domain semantics. `value` is an instant or civil fields; `scale`, `unit` and `precision` define representation; `zone`, `offset` and `rules` define civil resolution; uncertainty and source state what the timestamp can prove.

For a local date-time $l$ and zone rules $Z$, resolution is set-valued:

$$
R_Z(l)=\{i\mid local_Z(i)=l\}.
$$

Its cardinality can be zero in a gap, one normally or two in a fold. Therefore a local date-time and zone name do not always select exactly one instant. A policy must reject, shift or explicitly choose for gaps and folds.

### Critical invariants

- Every timestamp field names its domain event and capture point; generic `timestamp` is insufficient.
- Instant, local date-time, date, time-of-day, duration and calendar period use distinct types.
- Epoch, time scale, unit, signed range and subsecond precision are explicit at every numeric boundary.
- Numeric offsets retain the original instant but do not replace a named zone for future or recurring civil intent.
- Gap/fold behavior is explicit and tested with actual transition fixtures; implicit library defaults are not the contract.
- Original zone, entered local fields, resolved offset, ruleset version and resolution decision are retained when audit or future reinterpretation requires them.
- Precision loss is detected before conversion; truncation or rounding follows a declared rule.
- Event, ingestion and processing timestamps are stored separately, and negative or large lateness is explainable rather than silently reordered.
- Adjacent windows use consistent boundaries, usually `[start,end)`, and state which timestamp drives membership.
- Wall-clock adjustments cannot corrupt elapsed-time measurement; monotonic values are never serialized as globally comparable instants.
- Leap-second and smear behavior is documented for systems requiring subsecond UTC traceability.
- Time-zone data and runtime upgrades are treated as data/semantic changes and validated against stored fixtures.

### Common failures

Storing every temporal concept as an epoch integer; omitting the epoch or unit; guessing seconds versus milliseconds from magnitude; labeling local civil fields “UTC”; treating an offset as a zone; relying on `EST` or another ambiguous abbreviation; silently resolving a daylight-saving gap or fold; converting a future appointment to an instant too early and discarding its zone; assuming all days contain exactly 86,400 elapsed seconds; using wall time for latency; assuming clock synchronization makes timestamps exact; sorting by ingestion time when the question concerns occurrence; assigning windows without naming the time axis; truncating nanoseconds into milliseconds; parsing permissive date formats; losing RFC 3339 `-00:00` semantics; assuming database `timestamp with time zone` preserves the supplied zone name; and upgrading TZDB without checking historical or future reinterpretation.

### Compact example

Four records arrive in ingestion order `a,b,c,d`, but their event-time order is `b,a,d,c`. Event `b` is two seconds late relative to its ingestion time. With 60-second half-open windows, event time `179999 ms` belongs to `[120000,180000)`, while `180000 ms` belongs to the next window. Converting `1700000000123456789 ns` to milliseconds discards `456789 ns`, so an exact conversion must reject or preserve the remainder rather than claim a millisecond value is identical.

### Connections

[DE-008](008-schemas-nullability-and-type-fidelity.md) supplies the type-fidelity model; [DE-002](002-rows-columns-records-and-events.md) distinguishes event records; [DE-004](004-avro-protocol-buffers-and-schema-aware-serialization.md), [DE-005](005-arrow-and-in-memory-columnar-representation.md) and [DE-006](006-parquet-and-columnar-files.md) carry temporal types through serialization, memory and files. Clock behavior connects to [Operating Systems](../../22-operating-systems/ROADMAP.md), distributed ordering to [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and temporal API contracts to [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md).

## Governing Question

What temporal fact does each value claim, and which representation preserves that fact through every boundary?

“Timestamp” is dangerously underspecified. `2026-11-01 01:30` might be a local appointment, one of two instants in a daylight-saving overlap, a wall-clock display derived from an instant or an invalidly stripped offset. `1700000000` might mean seconds, milliseconds or another epoch; even if the unit is guessed correctly, its time scale and leap-second behavior may differ.

Start from domain meaning. A payment can have `authorized_at`, `captured_at`, `received_at` and `recorded_at`; none substitutes for another. A daily store opening is civil intent in a named zone. A distributed trace span has wall timestamps for correlation and monotonic duration for elapsed measurement. A streaming event has event time plus ingestion/processing evidence.

[RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html) defines a constrained Internet timestamp profile with numeric offsets, fractional seconds and leap-second provisions. [RFC 9557](https://www.rfc-editor.org/rfc/rfc9557.html) extends that representation with additional information including time-zone identifiers. These strings are useful interchange contracts, but a field still needs domain semantics, precision and failure policy.

Named zones matter because civil rules are political and versioned. The [IANA TZDB theory](https://www.iana.org/time-zones/theory) explains that rules can change, future entries are predictions and pre-1970 history has limitations. A database release is therefore part of the interpretation context, not merely a software patch.

## Why This Matters

Temporal defects can remain dormant until a boundary: a daylight-saving transition, a rules update, a leap event, an epoch overflow, an out-of-order message or a precision-changing export. Happy-path tests in UTC during ordinary weeks do not exercise those boundaries.

Civil scheduling and instant recording have opposite needs. For an event that already happened, an instant supports global comparison, while original zone and offset may be audit evidence. For a future 09:00 appointment in `Europe/Dublin`, the local fields and zone express intent; calculating an instant today may become stale if civil rules change before the appointment. Retaining only the instant can make the meeting occur at the wrong local time.

Event pipelines use several clocks. Event time supports domain order, windows and lateness. Ingestion time measures source-to-platform delay. Processing time measures platform behavior. A retry can arrive later without changing when the event happened. Collapsing the three hides data freshness and can place records in the wrong window.

Precision errors are plausible. A nanosecond value truncated to milliseconds retains the same second and often prints similarly, yet distinct trades or sensor readings can become equal. Multiplying seconds as if they were milliseconds can place a date near 1970; interpreting milliseconds as seconds can overflow or produce a far-future date. Magnitude heuristics eventually fail and conceal contract violations.

Clock synchronization is estimation. [NTPv4](https://www.rfc-editor.org/rfc/rfc5905.html) models offset, delay, dispersion and jitter; synchronized hosts do not obtain perfect truth. Security, network asymmetry, oscillator drift and correction policy affect timestamps. Order-sensitive systems need uncertainty, sequence numbers, causality or transactional positions rather than relying solely on close wall times.

## Prerequisites and Retrieval

Retrieve domain definitions for each temporal field; authoritative event source; capture location; source clock and synchronization policy; event, ingestion and processing values; local date/time fields; calendar system; named time-zone identifiers; numeric offsets; TZDB release; gap/fold resolution policy; original timestamp text; epoch and time scale; integer signedness and width; unit and subsecond digits; declared precision, resolution, accuracy and uncertainty; leap-second and smear policy; operating-system clock APIs; database column types and session zone; language/runtime temporal types; serializer logical annotations; parsing strictness; acceptable ranges; sentinel values; null/default behavior; ordering and deduplication rules; interval boundary convention; window definitions; watermark/lateness policy; retention and replay horizon; historical and future schedules; TZDB/runtime deployment versions; validation telemetry; rejected values; and rollback/recomputation procedures.

Distinguish instant from local date-time; local date-time from date; date from business day; time-of-day from elapsed duration; duration from calendar period; UTC offset from zone rules; `Z` from unknown local offset `-00:00`; UTC from POSIX time; leap insertion from leap smear; source precision from storage resolution; resolution from accuracy; clock reading from observation uncertainty; wall clock from monotonic clock; event time from effective time; event time from ingestion time; ingestion from processing; ordering from simultaneity; half-open from closed intervals; late event from duplicate; timezone conversion from merely attaching a zone; rule upgrade from data correction; and stored instant from future civil intent.

Build a boundary inventory showing every representation. A source may produce RFC 3339 text, an API binding may convert to a language instant, a queue may use integer milliseconds, Arrow may use microseconds with a zone parameter, Parquet may use an `INT64` timestamp logical type, and a database may render in a session zone. The weakest hop determines fidelity.

## Learning Objectives

After completing this module, you should be able to:

1. choose distinct types for instants, civil values, durations, periods and intervals;
2. explain why an offset is not a time zone and why a local time can map to zero, one or two instants;
3. preserve epoch, scale, unit, range and precision across numeric timestamp conversions;
4. parse and emit constrained interchange timestamps with explicit offset semantics;
5. design gap, fold, leap-second and time-zone-rules policies;
6. separate event, ingestion, processing, effective and recorded timestamps;
7. define half-open windows, lateness and ordering on the correct time axis;
8. select wall and monotonic clocks for their appropriate roles;
9. construct temporal boundary, round-trip and version-upgrade fixtures; and
10. operate temporal schemas with telemetry, replay and rollback.

## Core Exposition

### Begin with the temporal kind

Use types that state what a value is. An instant supports comparison on a timeline. A local date-time supports civil intent but not global ordering. A date supports calendar classification. A time-of-day generally needs a date and zone before becoming an instant. A duration measures elapsed amount. A calendar period changes fields such as month or day under calendar rules.

Names should expose the domain event: `order_placed_at`, `valid_from`, `price_observed_at`, `source_received_at`. A generic `created_at` often becomes ambiguous when a record is imported, retried or rebuilt.

Document capture semantics. Does `occurred_at` come from a sensor clock, user entry, server receipt or reconstruction? Which component can correct it? What uncertainty applies?

### Model an instant explicitly

An instant needs a time scale or operational convention, an epoch if numeric, a unit, signed range and precision. “Unix timestamp” alone is insufficient because implementations differ around leap seconds and units.

For common POSIX-style epoch values, state seconds, milliseconds, microseconds or nanoseconds since `1970-01-01T00:00:00Z` under the system's leap-second convention. Use field names such as `event_time_ms` only as reinforcement; the schema metadata remains authoritative.

Check arithmetic before scaling. Multiplying signed 64-bit seconds by one billion can overflow even when the seconds value itself fits. Converting nanoseconds to milliseconds is exact only when the value is divisible by one million.

### Model civil time explicitly

A local date-time stores calendar fields without an offset or zone. It is appropriate for values such as “every day at 09:00” or a birthday when no instant is intended.

Do not silently attach the machine's default zone. Defaults vary by host, container, session and deployment. Require the relevant zone at the domain boundary or preserve the value as unresolved civil time.

For future appointments, retain local fields and zone ID. Also retain a previously resolved instant and ruleset version when useful, but be prepared to recompute and notify if rules change.

### Distinguish offset and zone

An offset such as `-04:00` provides a numeric relationship to UTC for one timestamp. A zone such as `America/New_York` selects a history and predicted future of offsets and transitions. Many zones share an offset at one instant and diverge later.

RFC 3339 numeric offsets make an instant derivable. They do not preserve the civil rules used or support future recurrence. RFC 9557 time-zone annotations can carry more context, but applications must specify consistency checks when offset and zone disagree.

Avoid abbreviations such as `CST`; they can be ambiguous across regions and history. Use IANA identifiers or a deliberately fixed offset.

### Resolve gaps and folds deliberately

When a clock moves forward, some local readings never occur. When it moves backward, some occur twice. These changes are not always one hour and are not limited to stereotypical seasonal transitions.

For a gap, choose among rejection, explicit shift forward/backward, or a domain-specific reschedule. For a fold, require an offset, earlier/later selection or additional evidence. Store the decision.

Language defaults differ. [PEP 495](https://peps.python.org/pep-0495/) defines Python's `fold` marker to distinguish the earlier and later readings in an overlap. A library feature is useful, but the domain contract must say which choice is valid.

### Version time-zone rules

TZDB identifiers are stable interfaces, but their rules can be corrected and future predictions can change. Record the rules release for regulated calculations, future schedules or reproducible historical reconstruction.

Test upgrades with a corpus of zones, transition edges, historical values and future appointments. Compare old and new resolved instants and offsets. Classify differences as corrected history, changed future prediction or unintended runtime behavior.

Do not blindly freeze old rules forever. Current civil operations often need updated rules, while audits may need the interpretation used originally. Retain both data and provenance so the use case decides.

### Use RFC 3339 precisely

RFC 3339 uses a full date, `T`, time, and `Z` or numeric offset, with optional fractional seconds. Numeric offset is local time minus UTC. Parse the full grammar, validate calendar dates and preserve needed fractional precision.

The offset `-00:00` indicates that UTC time is known while the local offset is unknown; it is not semantically identical to an ordinary known zero offset. Preserve this state if the domain needs provenance.

Be explicit about acceptance. Permissive parsers may accept spaces, missing offsets, impossible dates, excessive fractions or nonstandard tokens. Normalize only after validation and retain original text where audit requires it.

### Preserve added zone information

RFC 9557 supports additional timestamp information, including a time-zone identifier. This can represent both the instant via offset and the civil rule context via zone.

Define how to handle inconsistent data: reject, trust the offset for the instant and flag the zone, or apply a documented critical/noncritical annotation rule. Never silently rewrite one component based on the other without evidence.

For future civil intent, an offset is only the resolution under current rules. Store the local fields and zone as authoritative, not merely an already-computed instant.

### Separate precision, resolution and accuracy

Nanosecond storage does not imply nanosecond observation accuracy. A source clock may report nine fractional digits derived from a millisecond sensor. Record meaningful precision and uncertainty separately from storage resolution.

When reducing precision, specify truncation or rounding, behavior for negative epoch values and collision consequences. Exact conversion rejects a nonzero remainder. Lossy conversion retains source precision or a flag so consumers do not infer false accuracy.

Do not pad fractions with zeros and then claim higher measurement precision. Formatting width is not evidence about the clock.

### Choose a leap-second policy

UTC can include leap seconds, while POSIX time conventionally excludes them. RFC 3339 permits a seconds value of `60` at an inserted leap second under its rules. Many libraries cannot construct or preserve it.

[RFC 8633](https://www.rfc-editor.org/rfc/rfc8633.html) explains leap smearing and warns that smeared time sacrifices UTC fidelity during the smear interval and should remain within a controlled environment. Mixing smeared and nonsmeared sources can create disagreement.

Most business systems can document POSIX-style handling and accept bounded ambiguity. Systems with legal, astronomical or high-precision requirements need a declared scale, traceability, current leap data and conversion tests. Never infer the policy from an epoch integer alone.

### Use wall and monotonic clocks correctly

Wall-clock time can jump or slew when synchronized, corrected manually or changed at virtualization boundaries. It is suitable for civil timestamps and cross-system correlation with uncertainty.

A monotonic clock measures elapsed time within its defined runtime. POSIX [clock functions](https://pubs.opengroup.org/onlinepubs/9799919799/functions/clock_getres.html) distinguish realtime and monotonic clocks. Use monotonic readings for timeouts, duration and performance measurement where available.

Do not serialize a monotonic reading for comparison across machines or restarts: its origin is unspecified. For a trace span, store wall start/end for correlation and monotonic duration for reliable elapsed measurement.

### Treat clock synchronization as evidence

NTP estimates clock offset and network delay; dispersion and jitter quantify aspects of uncertainty. A “synchronized” flag does not guarantee exact timestamp order across hosts.

Capture synchronization health where ordering matters. Reject or mark events from grossly skewed clocks, retain source sequence numbers, and use broker offsets, transaction order or causal metadata for stronger ordering claims.

Security matters because manipulated time can affect certificates, logs, markets and distributed leases. Monitor independent sources and protect synchronization channels according to the threat model.

### Separate event-time roles

Define one field per role:

- `occurred_at`: domain occurrence according to the source;
- `observed_at`: when a measuring device observed it;
- `ingested_at`: when the platform durably accepted it;
- `processed_at`: when an operator handled it;
- `effective_from`: when a business fact begins to apply;
- `recorded_at`: when the database recorded the row.

Their order is not universally fixed. A user can report a past event; a corrected effective date can precede ingestion; clock skew can make calculated lateness negative. Validate plausible bounds, but preserve evidence instead of forcibly sorting timestamps.

### Define lateness and out-of-order behavior

For event time $e$ and ingestion time $a$, observed lateness is

$$
L=a-e.
$$

Positive $L$ indicates arrival after the declared event instant under aligned clocks; negative $L$ may indicate future-dated events, skew, prediction or semantic mismatch. It is not automatically invalid.

A watermark is a processing claim about how far event time is believed complete, not a physical law. Document its derivation, allowed lateness, updates, idleness behavior and correction path. Preserve records that miss a window through a late-data policy rather than dropping them silently.

### Use half-open intervals

Represent adjacent windows as `[start,end)`. An event exactly at the boundary belongs to the later window, preventing double counting. Store or derive boundaries in a declared time axis and precision.

Calendar windows require zone rules. A “local day” can span other than 24 elapsed hours across transitions. Build the start and end from civil midnights in the named zone, then resolve to instants; do not add a fixed 86,400 seconds to the first instant.

For intervals with uncertain or coarse timestamps, define whether membership uses point estimates, containment or overlap. False precision can create brittle boundaries.

### Distinguish duration from calendar period

An elapsed duration of 24 hours is fixed on the chosen timeline. Adding one calendar day retains local clock fields under calendar/zone rules and may produce 23 or 25 elapsed hours near transitions.

Months have variable lengths. Define end-of-month behavior: clamp, reject or carry. “One month after January 31” is a domain policy, not integer arithmetic.

Store units and semantics. Avoid encoding every period as seconds or every duration as a calendar object.

### Map Arrow and Parquet carefully

Apache Arrow timestamps have a unit and optional timezone parameter. Inspect the precise binding behavior; a timezone attribute need not preserve the original offset text or all civil intent.

Parquet's [logical types](https://parquet.apache.org/docs/file-format/types/logicaltypes/) distinguish UTC-adjusted instant semantics from local timestamp semantics and define millisecond, microsecond and nanosecond units. Treat `isAdjustedToUTC=false` as local fields encoded by a defined convention, not as an instant secretly stored in UTC.

When moving between Arrow, Parquet and a query engine, test unit, timezone metadata, negative epochs, precision, nulls and session-zone rendering. Inspect the file schema rather than trusting dataframe display.

### Understand database semantics

Database type names can mislead. PostgreSQL documents that `timestamp with time zone` values are stored internally in UTC and rendered in the session zone; the original input zone is not thereby retained. Preserve a zone ID in another column when it is domain evidence.

For `timestamp without time zone`, an input zone may be ignored by some operations. Configure strict adapters and query behavior. Never let a connection's session zone silently determine interpretation of unresolved local values.

Test drivers, migrations, bulk loaders, replicas and exports because each may choose different native types or session settings.

### Validate temporal inputs

Reject impossible dates, out-of-contract years, missing required offsets, invalid zone IDs, inconsistent offset/zone pairs, unexpected precision and integer overflow. Quarantine values with source and reason.

Avoid magic sentinels such as epoch zero, maximum date or year 9999 for missing. They collide with valid ranges, distort min/max statistics and can overflow arithmetic. Use explicit null or state tags.

Use strict canonical output and deliberately bounded input variants. Locale-dependent numeric dates such as `01/02/03` are unsuitable for portable contracts.

### Test temporal round trips

Cover ordinary instants plus both sides of zone transitions, gap locals, both fold choices, leap-relevant strings, negative epochs, epoch zero, range extremes, excessive fractional precision, offset extremes, unknown offsets, mismatched annotations and TZDB-version changes.

Traverse every production hop. Check both semantic equality and retained metadata. A value can identify the same instant while losing original local time, zone or precision; whether that is faithful depends on the field.

Freeze clock dependencies in deterministic tests. Separately run compatibility tests against current rules and report changes rather than updating expected outputs blindly.

### Operate temporal data as a governed contract

Monitor parse failures, gap/fold decisions, unknown zones, offset mismatches, precision truncation, future/past outliers, clock skew, negative lateness, lateness percentiles, TZDB/runtime versions and differences after upgrades.

Record producer and schema versions. A sudden cluster at epoch zero or whole-second boundaries may indicate defaulting or lost precision. A shift in lateness may indicate source clocks, networks or backfills rather than processing regression.

For a rules update, canary conversions, compare affected values, retain the old runtime for rollback and decide whether stored derived instants need recomputation. Never rewrite event-time evidence merely to make charts orderly.

## Definitions and Notation

Let an instant domain be $I$ and a local date-time domain be $L$. For zone-rules version $Z$, define `local_Z:I→L`. The inverse relation is set-valued:

$$
R_Z(l)=\{i\in I\mid local_Z(i)=l\}.
$$

For ordinary local values, $|R_Z(l)|=1$; in a gap it is zero; in a fold it is typically two. A resolver $\rho(l,Z,p)$ needs policy or evidence $p$ and may return an instant or an explicit error.

For integer timestamp $n$, epoch instant $E$ and unit size $u$, an idealized instant is

$$
i=E+n\cdot u,
$$

subject to the declared time scale, leap policy, integer range and library calendar. Conversion from fine unit $u_f$ to coarse $u_c=k u_f$ is exact only when $n\bmod k=0$.

Let $e$ be event time, $a$ ingestion time and $p$ processing time. Observed source lateness is $L_a=a-e$; platform wait is $L_p=p-a$. Interpret both with clock uncertainty and semantic definitions.

Let a half-open window be $W_j=[s_j,s_{j+1})$. Membership is `s_j <= t < s_{j+1}`. Adjacent windows share a boundary but never share a point.

Represent timestamp uncertainty as an interval $[\hat{t}-\epsilon_-,\hat{t}+\epsilon_+]$ or another calibrated model. Printed fractional digits alone do not determine $\epsilon$.

## Mechanisms, Invariants, or Proof Structure

Use this mechanism for each temporal field and pipeline:

1. Name the domain event, actor, capture point and owner.
2. Classify it as instant, local date-time, date, time-of-day, duration, period or interval.
3. Inventory source clock, synchronization, accuracy and uncertainty.
4. Declare epoch, scale, unit, range, precision and leap behavior.
5. Declare zone ID, offset, TZDB version and civil intent where applicable.
6. Specify gap/fold resolution, mismatch and invalid-input policies.
7. Separate event, ingestion, processing, effective and recorded fields.
8. Map every serializer, in-memory type, file type, database type and API string.
9. Prove exact conversions or name rounding/truncation and retained provenance.
10. Define interval boundaries, time axis, window membership and late-data handling.
11. Create ordinary, transition, leap, range, precision and malformed fixtures.
12. Execute round trips through real libraries, drivers, session settings and files.
13. Test old/new runtimes and TZDB versions against historical and future cases.
14. Deploy readers and observability before emitting new representation variants.
15. Canary, compare, retain rollback and reconcile derived values deliberately.
16. Audit clock health, temporal drift and rule-version distribution continuously.

The following executable model distinguishes event order from ingestion order, applies half-open event-time windows and detects precision loss. The integers are synthetic fixtures, not synchronized-clock or streaming-engine measurements.

<!-- bijux-verify: {"id":"event-time-boundary-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ingestion_order=('a', 'b', 'c', 'd')\nevent_order=('b', 'a', 'd', 'c')\nlateness_ms=(500, 2000, 100, 201)\nwindow_members=('a', 'd')\nboundary_in_next_window=True\nprecision_loss_ns=456789\nexact_millisecond_conversion=False\n","stderr":""}} -->
```python
events = (
    {"id": "a", "event_ms": 120000, "ingest_ms": 120500},
    {"id": "b", "event_ms": 119000, "ingest_ms": 121000},
    {"id": "c", "event_ms": 180000, "ingest_ms": 180100},
    {"id": "d", "event_ms": 179999, "ingest_ms": 180200},
)

ingestion_order = tuple(row["id"] for row in events)
event_order = tuple(
    row["id"] for row in sorted(events, key=lambda row: (row["event_ms"], row["id"]))
)
lateness_ms = tuple(row["ingest_ms"] - row["event_ms"] for row in events)

window_start = 120000
window_end = 180000
window_members = tuple(
    row["id"]
    for row in events
    if window_start <= row["event_ms"] < window_end
)

timestamp_ns = 1700000000123456789
timestamp_ms = timestamp_ns // 1000000
precision_loss_ns = timestamp_ns - timestamp_ms * 1000000

print("ingestion_order=" + str(ingestion_order))
print("event_order=" + str(event_order))
print("lateness_ms=" + str(lateness_ms))
print("window_members=" + str(window_members))
print("boundary_in_next_window=" + str(events[2]["event_ms"] == window_end))
print("precision_loss_ns=" + str(precision_loss_ns))
print("exact_millisecond_conversion=" + str(precision_loss_ns == 0))
```

Critical invariants are:

- **Meaning:** each field names the domain event and capture semantics.
- **Representation:** epoch, scale, unit, range and precision are explicit.
- **Civil resolution:** zone, offset, rules version and gap/fold decision are sufficient for the required reconstruction.
- **Exactness:** narrowing detects remainders and overflow before conversion.
- **Clock:** elapsed measurement uses monotonic time; wall readings carry uncertainty appropriate to their claim.
- **Axes:** event, ingestion and processing times remain distinct.
- **Boundaries:** every interval uses one declared inclusion convention and time axis.
- **Evolution:** runtime, schema and TZDB changes are compared using retained fixtures.
- **Provenance:** normalization and recomputation never erase original temporal evidence.

**Proof sketch — local date-time plus zone need not identify an instant.** During a backward transition, choose two distinct instants $i_1<i_2$ whose displayed local fields are equal under zone rules $Z$. Then `local_Z(i_1)=local_Z(i_2)=l`, so both $i_1$ and $i_2$ belong to $R_Z(l)$ and $|R_Z(l)|\geq2$. A function using only $(l,Z)$ cannot choose the intended instant without an additional rule or fact. During a forward gap, a local value $g$ has no preimage, so $R_Z(g)=\varnothing$. Thus unconditional conversion from local fields and a zone to exactly one instant is not a total, single-valued inverse.

## Alternatives and Trade-Offs

**Instant versus local civil storage.** Instants support global ordering and elapsed arithmetic. Local fields plus zone preserve future civil intent. Historical events may store both; future schedules should usually treat civil intent as authoritative and the current instant as derived.

**Offset versus named zone.** An offset is compact, unambiguous for one instant and independent of rule databases. It cannot describe transitions or recurrence. A zone supports civil behavior but depends on versioned rules. Carry both when audit or consistency checks justify it.

**Text versus integer timestamp.** RFC-style text is self-describing about calendar and offset and easier to inspect, but larger and still needs semantic/precision rules. Integers are compact and sortable when contracts agree, but unit and epoch errors are severe. Schema-aware systems can use either safely with complete metadata.

**UTC normalization versus original context.** Normalizing an occurred event to an instant simplifies joins. Discarding zone, offset and original text can lose audit evidence or civil intent. Preserve only what the domain needs, but make the loss deliberate.

**Strict transition rejection versus convenience resolution.** Rejecting ambiguous/nonexistent local values forces users or producers to decide correctly. Automatic shift/earlier/later policies improve continuity for low-risk schedules. The chosen policy must be domain-specific, visible and reproducible.

**Current versus pinned TZDB.** Current rules best support present civil operations. Pinned rules reproduce old decisions. Store version provenance and offer both modes where legal/audit requirements differ from current display.

**Nanosecond versus coarser storage.** Fine resolution preserves possible source distinctions but increases range and interoperability constraints and can imply false accuracy. Choose the coarsest resolution that preserves required evidence; retain remainder or original value when narrowing.

**Wall versus monotonic duration.** Wall endpoints support cross-system correlation but can jump. Monotonic elapsed time is robust locally but not portable across restarts/hosts. Critical telemetry often records both.

**Processing-time versus event-time windows.** Processing time is operationally simple and low latency. Event time reflects domain occurrence but requires watermarks, late updates and state. Choose based on the question, not engine convenience.

**Drop versus revise late data.** Dropping bounds cost but loses truth. Revising windows improves completeness but requires update-capable sinks and communicated finality. Side outputs preserve evidence for reconciliation. Establish service-level expectations and idempotence.

**Fixed duration versus calendar period.** Fixed durations are predictable on the timeline. Calendar periods match human schedules but depend on calendar, zone and end-of-month rules. Type them separately to prevent accidental substitution.

**Store uncertainty versus point only.** A point is simpler for joins and indexes. An uncertainty interval better represents sensor/clock evidence but complicates comparisons. High-consequence ordering should retain calibrated uncertainty or another stronger sequence source.

## Failure Modes and Misconceptions

- **“Everything should be UTC.”** Instants often should be normalized, but future civil schedules and dates have different semantics.
- **“UTC is a timezone string.”** UTC is a time standard; named regional zones contain changeable civil rules.
- **“Offset and zone are interchangeable.”** An offset describes one relationship; a zone describes rules across time.
- **“Local plus zone always resolves.”** Gaps yield no instant and folds yield multiple candidates.
- **“DST transitions are always one hour.”** Historical and current transitions can differ in size and cause.
- **“The server default zone is harmless.”** It is implicit mutable configuration and changes interpretation.
- **“Unix time fully defines the value.”** Unit, epoch, scale, signed range and leap policy are still required.
- **“Magnitude reveals seconds versus milliseconds.”** Heuristics fail across ranges and legitimize malformed contracts.
- **“More fractional digits mean a more accurate clock.”** Formatting and storage resolution do not establish observation accuracy.
- **“Dropping nanoseconds only changes display.”** It can collapse distinct events, order and deduplication keys.
- **“RFC 3339 accepts any ISO-like date.”** It is a constrained grammar; strict validation still matters.
- **“`-00:00` is just another spelling of UTC.”** RFC 3339 uses it to express unknown local offset with known UTC time.
- **“Leap seconds do not matter because we use epoch time.”** Epoch conventions differ; the boundary still needs a policy.
- **“Leap smear is UTC.”** It intentionally differs during the smear window and lacks a universal detection mechanism.
- **“NTP makes clocks identical.”** Synchronization estimates have delay, dispersion, jitter and failure modes.
- **“Wall-clock subtraction measures latency.”** Clock corrections can produce wrong or negative durations.
- **“Monotonic timestamps can be compared across hosts.”** Their origins are local and unspecified.
- **“Arrival order is event order.”** Retries, buffering, networks and partitions reorder records.
- **“Negative lateness is impossible.”** Clock skew, prediction and semantic mismatch can produce it.
- **“A watermark proves no earlier event exists.”** It is an operational completeness estimate with a late-data policy.
- **“Daily windows are 86,400 seconds.”** Civil days can differ across zone transitions.
- **“Closed intervals are easier.”** Adjacent closed intervals double-count shared boundaries.
- **“Adding one day equals adding 24 hours.”** Calendar and elapsed arithmetic answer different questions.
- **“Timestamp with time zone stores my zone.”** Some databases normalize to an instant and render through a session zone.
- **“TZDB upgrades are presentation-only.”** They can change derived instants, offsets and historical interpretations.

## Worked Examples

### Example 1

An API receives `2026-04-10T15:30:00-04:00`. The numeric offset makes the instant derivable: subtracting `-04:00` yields `19:30:00Z`. The value does not say which regional rules produced `-04:00`.

For a completed payment, the service stores the instant and preserves the original text for audit. For a future recurring appointment, it additionally requires an IANA zone and treats the local time plus zone as civil intent. The two fields use different contracts despite similar input strings.

### Example 2

A scheduler receives `2026-11-01 01:30 America/New_York` during a backward transition. The local reading occurs twice with different offsets. Choosing the runtime's default earlier offset can schedule the wrong medication reminder.

The boundary returns an ambiguity response listing the two offset-qualified candidates. The user or upstream rule selects one, and the record stores local fields, zone, selected offset, resolved instant, TZDB version and choice provenance. Replay produces the original decision even after a rules upgrade.

### Example 3

A maintenance job requests `02:30` on a date when the local clock jumps from `01:59:59` to `03:00:00`. No instant has those local fields. Silently shifting to `03:30` may be suitable for a low-risk batch but not a transport departure.

The scheduler declares `gap_policy=reject` for departures and `gap_policy=shift_forward_by_gap` for housekeeping. Metrics count each policy application. Tests verify the actual transition and do not assume every gap lasts one hour.

### Example 4

A source emits `1700000000123456789` nanoseconds since the POSIX epoch. A warehouse column supports milliseconds. Integer division gives `1700000000123` with a remainder of `456789 ns`.

An exact boundary rejects the conversion. A governed lossy export truncates and carries `source_precision=ns` plus a loss counter. It tests negative timestamps separately because division/rounding semantics can differ. The source value remains available for ordering and reconciliation.

### Example 5

A retailer schedules a promotion for 09:00 local time six months ahead in `Europe/Dublin`. Current rules produce a derived UTC instant. Before the date, a rules release changes the future offset.

The system retains local date-time and zone as authoritative, records the original rules release and calculated instant, and recomputes after upgrades. It reports the difference to the business owner before changing notifications. Storing only the first instant would have lost the intended wall time.

### Example 6

A trace records wall start `10:00:00.500` and wall end `10:00:00.200` because the system clock was corrected backward. Wall subtraction suggests negative latency. A monotonic clock measured `85 ms`.

The span stores wall start/end for correlation, monotonic duration for performance and clock-synchronization metadata. The monotonic readings themselves are not exported as global instants. An alert on wall/monotonic disagreement identifies clock behavior without corrupting latency statistics.

### Example 7

Four events arrive as `a,b,c,d`, but event-time sorting gives `b,a,d,c`. A one-minute window `[120000,180000)` includes `a` at the start and `d` one millisecond before the end. Event `c` at exactly `180000` belongs to the next window.

The pipeline assigns by `occurred_at`, tracks `ingested_at-occurred_at`, and accepts revisions until its watermark/allowed-lateness policy closes the result. A processing-time dashboard separately groups by ingestion to measure workload.

### Example 8

A source sends `2016-12-31T23:59:60Z`. The parser's ordinary date-time type rejects second 60 even though RFC 3339 permits it at a declared leap second. Replacing `60` with `59` would fabricate an instant.

The system's documented POSIX boundary rejects leap-second lexical input into that field and routes it to a specialized converter when required. A precision service instead uses current leap data and a declared scale. Neither path silently claims ordinary POSIX seconds preserve UTC exactly across the event.

### Example 9

A database column named `appointment_at` uses `timestamp with time zone`. Input includes `2026-06-01 09:00 America/Phoenix`. The database normalizes the instant and later renders it using the connection's `America/New_York` session zone. The original zone is gone.

The corrected schema stores `appointment_local`, `appointment_zone`, resolved `appointment_instant` and `rules_version`. Queries set session zones explicitly. Round-trip tests cover drivers and exports rather than relying on the column type's name.

### Example 10

A dataset has `created_at=0` for both genuinely epoch-time test records and missing legacy timestamps. Min/max statistics and retention jobs cannot distinguish them. Reinterpreting all zero values as null would erase valid evidence.

The migration adds a state field. Records with independent lineage proof become `missing`; verified test events remain `present`. Unresolved values become `legacy_unknown`. New writes forbid sentinels, and metrics track remaining ambiguous history without inventing a timestamp.

## Cross-Program Connections

**Operating Systems.** Realtime and monotonic clocks, clock correction, timer behavior and process lifetime determine which readings can measure elapsed time. A data contract must respect those kernel-level semantics.

**Distributed Systems.** Wall-clock order is weaker than causal or consensus order. Hybrid/logical clocks, sequence numbers, broker offsets and transaction positions complement physical timestamps when coordination needs stronger claims.

**Network Engineering.** Synchronization quality depends on delay, asymmetry, source diversity and security. Network partitions and retries also create event-time lateness and reorder arrival.

**API and Service Engineering.** Timestamp strings, patch semantics, fractional precision and offset/zone annotations are versioned API contracts. Generated clients must preserve rather than silently reinterpret them.

**Database Engineering.** Column types, session zones, indexes, interval arithmetic and range predicates determine temporal query correctness. Half-open validity ranges align with exclusion constraints and point-in-time queries.

**Security Engineering.** Trusted time affects certificates, signatures, leases, audit logs and retention. Time synchronization and user-supplied timestamps require threat modeling and provenance.

**Machine Learning Engineering.** Point-in-time joins, feature freshness and label leakage depend on separating event/effective/ingestion times. Coarse or corrected timestamps can change training examples.

**Systems Engineering.** Temporal accuracy is an interface property with explicit uncertainty, failure modes and verification evidence. High-consequence systems must say what a timestamp proves rather than equate digits with truth.

## References

1. IETF, [RFC 3339: Date and Time on the Internet — Timestamps](https://www.rfc-editor.org/rfc/rfc3339.html), retrieved 2026-09-02.
2. IETF, [RFC 9557: Date and Time on the Internet — Timestamps with Additional Information](https://www.rfc-editor.org/rfc/rfc9557.html), retrieved 2026-09-02.
3. IANA, [Theory and Pragmatics of the TZ Code and Data](https://www.iana.org/time-zones/theory), retrieved 2026-09-02.
4. IETF, [RFC 5905: Network Time Protocol Version 4](https://www.rfc-editor.org/rfc/rfc5905.html), retrieved 2026-09-02.
5. IETF, [RFC 8633: Network Time Protocol Best Current Practices](https://www.rfc-editor.org/rfc/rfc8633.html), retrieved 2026-09-02.
6. The Open Group, [POSIX clock_getres, clock_gettime and clock_settime](https://pubs.opengroup.org/onlinepubs/9799919799/functions/clock_getres.html), retrieved 2026-09-02.
7. Python Enhancement Proposals, [PEP 495: Local Time Disambiguation](https://peps.python.org/pep-0495/), retrieved 2026-09-02.
8. Apache Arrow, [Columnar Format](https://arrow.apache.org/docs/format/Columnar.html), retrieved 2026-09-02.
9. Apache Parquet, [Logical Type Definitions](https://parquet.apache.org/docs/file-format/types/logicaltypes/), retrieved 2026-09-02.
10. PostgreSQL Global Development Group, [Date/Time Types](https://www.postgresql.org/docs/current/datatype-datetime.html), retrieved 2026-09-02.

## Exercises

### Exercise 1

Design fields for a telehealth appointment booked as `2026-11-01 01:30` in `America/New_York`. The local time is in a fold, rules may change before the appointment and audit must reproduce what the user selected. Specify authoritative and derived fields, resolution flow, versioning, update behavior and at least eight fixtures.

### Exercise 2

A producer emits signed 64-bit nanoseconds since the POSIX epoch, while an API supports RFC 3339 with six fractional digits and a warehouse stores signed 64-bit milliseconds. Define exact and lossy mapping policies. Recompute the warehouse value and remainder for `1700000000123456789 ns`, and cover negative values, overflow, rounding and provenance.

### Exercise 3

An event system stores `occurred_at`, `ingested_at` and `processed_at`. Define lateness metrics, a 15-minute half-open event-time window, allowed-lateness behavior and treatment of negative lateness. Explain why ingestion-order sorting and wall-clock timestamps alone cannot prove event order across devices.

### Exercise 4

Plan a TZDB/runtime upgrade for a scheduling platform operating in 50 zones with historical records and future appointments. Include corpus selection, old/new comparisons, classification, consumer deployment, canary, user communication, recomputation, rollback, telemetry and evidence required before completion.

### Exercise 5

A financial audit pipeline mixes UTC, POSIX timestamps, a leap-smearing clock source and a nonsmearing source at microsecond precision. Design a safe temporal contract and reconciliation process. State which claims cannot be made from the existing values alone and which additional evidence is required.

## Answers to the Exercises

### Answer 1

Store authoritative `appointment_local=2026-11-01T01:30:00`, `zone_id=America/New_York` and an explicit overlap choice or selected offset. Store derived instant, resolved offset, TZDB release, resolution policy/version and selection actor/time. On entry, calculate all candidates; because there are two, require a user/domain choice rather than applying a hidden default.

Fixtures include ordinary winter/summer locals, gap local, both fold candidates, invalid zone, offset/zone mismatch, future rule change, fractional precision and cancellation/reschedule. After a rules upgrade, recompute future derived instants from authoritative civil intent, compare, notify before material changes and retain prior derivation for audit. Historical decisions remain reproducible using stored offset/rules provenance.

### Answer 2

For `1700000000123456789 ns`, truncating toward the defined coarse boundary gives `1700000000123 ms` with `456789 ns` remainder. An exact warehouse mapping rejects because the remainder is nonzero. A governed lossy mapping specifies truncation or rounding, handles negative division explicitly, reports loss and retains the original or remainder plus source precision.

The API can emit at most microsecond resolution, so it also needs divisibility by 1,000 for exact conversion. Test zero, `±1 ns`, values on exact millisecond boundaries, negative remainders, signed 64-bit endpoints, scaling overflow and RFC range limits. Never pad/truncate without provenance, and do not claim the exported digits retain nanosecond ordering.

### Answer 3

Define source lateness `ingested_at-occurred_at` and platform delay `processed_at-ingested_at`, qualified by clock uncertainty. A 15-minute event window is `[floor(event/15m)*15m, next_boundary)`. An event exactly at the end belongs to the next window. A watermark plus allowed lateness decides whether to revise, side-output or reject; the sink must support idempotent corrections.

Negative lateness is classified as skew, future scheduling or semantic error using bounds and source metadata, not silently clamped. Arrival order reflects networks, buffering and retries. Device wall clocks have offset and uncertainty, so close readings cannot prove causal order. Use device sequence, transaction/broker position or causal metadata where stronger ordering is required.

### Answer 4

Build a corpus covering every zone, all nearby transitions, historically important dates, future appointments, aliases and out-of-range inputs. Resolve it under the old and candidate runtime/TZDB versions. Classify each difference as historical correction, future prediction change, alias change, expected runtime difference or defect; obtain domain approval for affected schedules.

Deploy readers/observability first, canary resolution, notify owners/users of future appointment shifts and recompute only derived instants from retained civil intent. Preserve old values and rules provenance. Rollback pins the prior runtime/data and stops new derivations; it does not erase already communicated changes. Completion evidence includes corpus results, reviewed difference inventory, successful canary, version telemetry, consumer compatibility and a tested rollback.

### Answer 5

Declare for each input its time scale/convention, epoch, unit, precision, source clock, smear profile/window, synchronization state and uncertainty. Do not mix smeared and nonsmeared readings as if both were UTC during the affected interval. Preserve original values and source identity, convert through a controlled service with current leap data where a mapping is defined, and represent uncertainty or ambiguity explicitly.

Existing unlabeled epoch values cannot prove UTC traceability, leap handling, ordering within the smear window or true microsecond accuracy. Retrieve source configuration, smear function/version, NTP peer/health logs, leap-second data, oscillator/accuracy evidence and event sequence/transaction positions. Reconcile outside ambiguous intervals where possible; flag unresolved records rather than inventing a total order.
