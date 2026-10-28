---
module_id: DE-057
program: Data Engineering
level: 2
module_number: 57
title: Event Time and Processing Time
status: complete
last_verified: 2026-09-03
---

# Event Time and Processing Time

## One-Page Review

### Governing question

Which clock and timestamp should govern each streaming decision, what does that timestamp actually mean, and how can engineers reason about latency, order, deadlines, replay, clock error, civil time, and temporal change without treating a machine clock as business truth?

### Essential definitions

- **Event time** is the time attributed to the domain occurrence represented by a record, according to a named authority and semantic rule.
- **Capture time** is when a producer or source adapter observed or encoded the occurrence; it may differ from the occurrence itself.
- **Commit/source time** is when an authoritative source, such as a database, committed or recorded the change.
- **Append time** is when a broker/log accepted a record under its timestamp policy.
- **Ingestion time** is when a pipeline boundary first admitted or observed the record.
- **Processing time** is the runtime clock time when a particular stage processes the record. It is stage- and attempt-specific.
- **Observation/publication time** is when a result becomes visible to a named downstream reader or user.
- A **clock domain** is a set of timestamps produced from one time source, scale, synchronization, and error model.
- **Clock offset** is the estimated difference between a clock and its reference; **uncertainty** bounds how wrong the timestamp may be.
- **Skew** is a difference between clocks or their rates/offsets; **drift** is change in clock error over time.
- A **wall clock** maps readings to civil/UTC-like instants and may be corrected; a **monotonic clock** is suitable for elapsed durations because it does not move backward within its documented process/system scope.
- A **timezone offset** maps a local representation to UTC at an instant; a **time-zone identifier** selects a changing civil-time ruleset.
- **Latency decomposition** separates source/capture, transport, queue, processing, output, and visibility intervals rather than subtracting unrelated clocks blindly.
- **Temporal provenance** records the timestamp field, authority, clock, precision, timezone/scale, capture rule, uncertainty, and transformation history.
- A **time contract** defines these semantics plus invalid/future/old timestamp policy, order relation, replay behavior, and compatibility version.

### Central model, mechanism, or theorem

For one record $x$, let $t_e$ be its event timestamp, $t_i$ its ingestion observation, $t_p$ processing start, $t_o$ output acceptance, and $t_v$ visibility. When readings are comparable and corrected to one scale, observed intervals are

$$
L_{source}=t_i-t_e,
\quad L_{queue}=t_p-t_i,
\quad L_{compute}=t_o-t_p,
\quad L_{publish}=t_v-t_o,
$$

and

$$
L_{end}=L_{source}+L_{queue}+L_{compute}+L_{publish}=t_v-t_e.
$$

If timestamp $t_j$ has bounded error $\epsilon_j$, a difference $d=t_b-t_a$ has conservative uncertainty interval

$$
d_{true}\in[d-(\epsilon_a+\epsilon_b),\ d+(\epsilon_a+\epsilon_b)].
$$

Therefore $t_a<t_b$ proves real-time order only when the uncertainty intervals do not overlap, for example $t_a+\epsilon_a<t_b-\epsilon_b$. Negative observed latency is evidence of incomparable semantics, bad units, or clock error—not time travel.

### Critical invariants

- Every timestamp field has one durable name, semantic authority, clock domain, scale/epoch, unit/precision, timezone/offset rule, uncertainty, and schema version.
- Domain occurrence, producer capture, source commit, broker append, ingestion, processing, output, and visibility times remain distinct fields.
- Event time is chosen from the business question; a producer clock is not called event time merely because it is embedded in the event.
- Processing time is attempt- and stage-specific and is not stable under backlog, replay, scaling, pause, or failure.
- Durations and deadlines within one runtime use a monotonic clock; wall-clock timestamps are retained for cross-system correlation with explicit uncertainty.
- Latency subtraction occurs only across comparable clock domains, or the result carries an error interval and invalid/negative handling.
- Timestamp order never substitutes for causal relations, source sequence, broker offset, business version, or transaction order when those are required.
- Original timestamp and provenance survive transformation; correction adds a versioned derived field rather than silently overwriting evidence.
- Event-time validation bounds implausible future/past values without discarding valid offline, delayed, or corrected data indiscriminately.
- Local civil time includes a zone identifier and disambiguation policy when converted to an instant; abbreviations and bare local strings are insufficient.
- Replay states whether historical processing time is reproduced, recomputed, or replaced by a recorded observation; results do not accidentally depend on wall-clock “now.”
- Clock synchronization, offset, jitter, dispersion, step/slew events, leap handling, and timezone-database versions are observable dependencies.
- SLOs name their endpoints and statistic: occurrence-to-visible freshness differs from append-to-process lag and handler duration.
- Temporal migration dual-records old/new semantics, compares results over finite cuts, and preserves rollback and reprocessing evidence.

### Common failures

Common failures include using one field named `timestamp` for several meanings; equating producer send time with domain occurrence; using broker append time for user-behavior windows; subtracting clocks without uncertainty; sorting independent producers by wall time; measuring elapsed duration with a clock that can jump; storing a bare local time or timezone abbreviation; treating milliseconds as seconds; inferring precision from decimal digits; overwriting original timestamps during correction; dropping “future” offline events during clock skew; calculating freshness from processing time; assuming replay reproduces processing-time results; using current timezone rules for past/future intent without version awareness; and treating a watermark as a perfect clock.

### Compact example

Records arrive in append order `a,b,c,d`, but their event timestamps sort as `c,a,b,d`. For `a`, event/ingest/process readings of 1000/1120/1250 ms yield observed source delay 120 ms, queue delay 130 ms, and event-to-process delay 250 ms. Record `d` has 1600/1400/1450 ms, producing a negative source and end-to-process delay because its producer clock is ahead or its timestamp has different semantics. With combined endpoint uncertainty 300 ms, the observed -150 ms end-to-process value means a possible true interval `[-450,150]`, not a reliable negative latency.

### Connections

[DE-051](051-streams-logs-and-unbounded-data.md) separated logical identity from mutable observation. [DE-052](052-topics-partitions-and-offsets.md) supplied deterministic log coordinates; [DE-053](053-producer-keys-and-ordering.md) separated append, causal, event-time, and business-version order; [DE-055](055-delivery-semantics-in-streaming-pipelines.md) and [DE-056](056-exactly-once-effects.md) made processing attempts replayable. DE-058 will turn event-time progress into window/watermark policy, DE-059 will manage state, and DE-060 will handle late, duplicate, and out-of-order records.

## Governing Question

Time appears in nearly every streaming requirement: events from the last five minutes, alerts within thirty seconds, sessions ending after inactivity, daily revenue in a customer's locale, a database change applied before its deadline, or the newest device reading. These phrases name different clocks and order relations. Implementing them with a generic `timestamp` field creates silent semantic errors.

Event time answers a domain question: when did the represented occurrence happen according to a specified authority? Processing time answers an operational question: when did this stage execute this attempt? Append and ingestion time describe system observation. Source commit time may provide authoritative database order. Visibility time closes a user-facing freshness objective. None can be substituted without changing the question.

Clocks are measurements, not omniscient order oracles. Producer devices may be offline, misconfigured, drifting, malicious, or corrected. NTP estimates offset and dispersion; it does not make all readings identical. Network delay is variable and generally asymmetric. A timestamp with millisecond units may have only second-level resolution or much larger uncertainty.

The governing task is to create a time contract. It identifies each timestamp's provenance, scale, precision, uncertainty, and compatibility; specifies which time controls each operation; separates causal/business order from clock order; and makes replay, validation, civil-time conversion, and migration explicit.

## Why This Matters

Using processing time for domain aggregation makes results depend on backlog and infrastructure. A purchase that occurred at 23:59 can enter the next day's total because a broker outage delayed it past midnight. A replay next month assigns all historical events to the replay day. Capacity changes alter queue delay and therefore business results.

Using event time everywhere is also wrong. Retry deadlines, cache expiry, circuit breakers, and handler timeouts need elapsed processing/runtime time. Waiting for a device-reported future timestamp can block progress. Operational admission and autoscaling respond to current backlog, not the domain time embedded in records.

Latency metrics fail when endpoints are vague. “Pipeline latency” might mean source commit to connector capture, broker append to consumer fetch, fetch to effect, or domain occurrence to customer-visible result. Each diagnoses a different subsystem. A single total hides where the budget was spent and may subtract unrelated clocks.

Temporal bugs have governance impact. Billing dates, filing deadlines, trading cutoffs, medication events, retention, and data-residency actions depend on legal/business definitions. Civil time changes with governments and daylight-saving rules. A local time can be nonexistent in a spring-forward gap or occur twice during a fall-back overlap.

Replay is a temporal test. Event-time-deterministic logic should reproduce the same result from the same cut and reference data. Processing-time-dependent logic commonly changes unless its clock decisions were persisted. Exactly-once effects do not guarantee temporally equivalent results when “now” is re-evaluated.

## Prerequisites and Retrieval

Retrieve the business question: occurrence being timed; authority that determines it; whether users supplied a local civil time or an instant; legal cutoff; correction policy; accepted delay; order/causality; required precision; uncertainty tolerance; and responsible domain owner.

Retrieve every timestamp field: schema path/name; sample values; unit/epoch/scale; precision/resolution; nullable/default behavior; producer/source; creation/capture rule; clock library; timezone/offset; uncertainty; validation; transformations; and version history.

Retrieve clock evidence: host/device clock source; synchronization service/version; last update; offset estimate; jitter/dispersion/error bound; stratum/reference; step versus slew behavior; suspend/resume; leap-second handling; monotonic clock scope; virtualization; and alert thresholds.

Retrieve platform times: database transaction begin/commit/CDC timestamps; broker create/append timestamp policy; topic override; connector processing timestamp; ingestion edge; consumer fetch; handler start/end; output acceptance; storage commit; cache/materialization refresh; API response; and user-visible publication.

Retrieve ordering evidence: source sequence/LSN; topic generation/partition/offset; producer epoch/sequence; business entity/version; command/causation ID; transaction ID; event timestamp; and conflict-resolution rule. Do not infer one from another.

Retrieve temporal processing: timestamp extractor/assigner; invalid/future/past bounds; unit conversion; timezone database; event-time timers; processing-time timers; scheduling; windows/watermarks/triggers (inventory only here); allowed lateness; state TTL; replay clock; and test clock.

Retrieve SLO evidence: exact start/end milestone; population and exclusions; percentile/window; clock domains; correction and uncertainty; queue/compute/output components; oldest obligation; late/future rates; timestamp missing/invalid rate; and business-visible reconciliation.

Retrieve failure/change cases: clock step backward/forward; drift; NTP loss; device reset; suspend; daylight transition; timezone-rule update; leap second; unit/schema change; null/default; future malicious timestamp; offline upload; backlog; retry; replay; region change; connector upgrade; topic timestamp-policy change; and historical correction.

Distinguish instant from local date/time; timezone ID from UTC offset; scale from format; unit from precision; precision from accuracy; timestamp from duration; wall from monotonic clock; event from capture time; producer create from domain occurrence; source commit from connector processing; append from ingestion; processing start from output/visibility; timestamp order from causal/business/log order; lateness from latency; and current-rule conversion from stored historical intent.

Create a time contract:

| Concern | Required decision and evidence |
|---|---|
| Meaning | Field, domain event, authority, capture rule, fallback and corrections |
| Representation | Epoch/scale, unit, precision, timezone/offset, nullable/default, range |
| Provenance | Device/source/producer, clock domain, software/schema/config version |
| Error | Offset, resolution, synchronization, uncertainty bound, invalid/future policy |
| Order | Event/causal/business/source/log relation and tie/conflict handling |
| Processing | Which time governs grouping, deadlines, timers, expiry, replay and UI |
| Latency | Named endpoints, comparable clocks, components, statistic and error interval |
| Civil time | IANA zone, tzdb version, overlap/gap/future-rule disambiguation and intent |
| Change | Dual fields, backfill/correction, compatibility, cutover, rollback, lineage |
| Evidence | Golden timestamps, clock fault tests, replay comparison, metrics and audit |

Write a falsifiable claim: “For schema `event-time-v3`, `occurred_at` is an RFC 3339 instant produced from the order service's committed domain clock with declared ±250 ms bound; database LSN remains authoritative for source order; broker append and stage processing times are separate observations; occurrence-to-visible latency carries combined endpoint uncertainty; durations use monotonic clocks; invalid/future records enter governed review; and replay uses stored event time rather than wall-clock now.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish event, capture, source commit, append, ingestion, processing, output, and visibility time;
2. specify timestamp authority, scale, unit, precision, timezone, uncertainty, and provenance;
3. decide which clock governs business grouping, operational deadlines, duration, replay, and SLOs;
4. decompose latency and propagate clock-error bounds;
5. reject timestamp order when causal, business-version, transaction, or log order is required;
6. use monotonic clocks for elapsed time and wall clocks for interoperable instants with caveats;
7. model civil-time overlap, gaps, future rule changes, and timezone-database versions;
8. validate delayed, future, missing, corrected, and adversarial timestamps without silent loss;
9. migrate time semantics with dual recording and deterministic replay; and
10. test clock faults and reconcile temporal outputs with authoritative cuts.

## Core Exposition

### Start with the domain occurrence

Ask what happened and who can say when. A card terminal may record when a customer tapped, a payment processor when authorization completed, and a ledger when posting committed. These are different occurrences. Calling all three `transaction_time` does not resolve which drives settlement or customer reporting.

The event-time authority might be the service that commits the domain transition, a trusted sensor, a user-declared scheduled time, or an exchange sequence with an associated timestamp. State whether the time is asserted, measured, derived, or corrected. Record the original assertion even when a later trusted process produces a corrected field.

If no reliable occurrence timestamp exists, do not invent precision. Source commit or ingestion time may be the honest proxy. Name it as such and document the bias it introduces.

### Separate the timeline fields

Create distinct fields such as `occurred_at`, `captured_at`, `source_committed_at`, `broker_appended_at`, `ingested_at`, `processing_started_at`, `output_accepted_at`, and `visible_at`. A record need not carry them all, but telemetry and lineage should connect them.

Each stage can have many processing times because replay and retry repeat execution. Append time can change when a connector republishes. Event time should remain stable for one occurrence unless a versioned correction is issued. Source commit time may apply to an entire transaction, not every row independently.

Use field names that encode meaning, not storage type. `event_timestamp_ms` says unit but not authority. A schema description should answer both.

### Define clock domains and uncertainty

Two timestamps are directly subtractable only when they refer to comparable instants on compatible scales and their error is acceptable. Record clock source and synchronization health at the point of observation. A timestamp's decimal precision is not its accuracy.

NTP's model includes offset, round-trip delay, dispersion, and jitter; accumulated synchronization distance provides an error-related bound. A green “NTP running” flag is weaker evidence than measured offset and dispersion at the relevant time.

Represent a reading as an interval $[t-\epsilon,t+\epsilon]$ when a bound is available. If intervals overlap, wall-clock order is indeterminate. Use source sequences, transactions, business versions, or causality rather than breaking ties with hostnames.

### Use monotonic clocks for elapsed duration

Wall clocks can step backward or forward because of synchronization, administrator action, virtual-machine behavior, or platform policy. Subtracting two wall-clock reads inside a process can yield negative or inflated durations.

Use a documented monotonic clock for elapsed deadlines, retry backoff, handler duration, and timeout budgets. Python's current `time.monotonic()` documentation states the clock cannot go backward, is unaffected by system-clock updates, and has an undefined reference point so only differences are valid.

Monotonic readings generally cannot be compared across processes or persisted as global instants without platform-specific guarantees. Record wall-clock endpoints for distributed correlation and monotonic duration for local measurement; do not convert an arbitrary monotonic origin to UTC.

### Decompose latency by ownership

Occurrence-to-visible freshness can be decomposed into source/capture, transport/append, queue, compute, output, and publication intervals. Name each owner and measure percentiles, not just averages. Include retry and replay attempts without double-counting one occurrence.

If event and visibility clocks have uncertainties $\epsilon_e$ and $\epsilon_v$, total latency has at least their combined endpoint uncertainty. Intermediate component sums may not equal the endpoint subtraction exactly because observations use different clocks, buffering, sampling, and instrumentation.

Negative latency should trigger validation: wrong units/epoch, future producer clock, reversed endpoints, parsing/timezone error, reused field, or error wider than the observed difference. Clamping to zero hides evidence and biases distributions.

### Choose event time for domain grouping

Use event time when the output asks about when domain occurrences happened: revenue by purchase day, trips by departure hour, sensor readings by measurement minute, or sessions by user activity. This makes results resilient to variable transport, backlog, scale, and replay.

Event time does not guarantee timely arrival. Offline devices and outages can deliver old events. Policies for waiting, provisional results, correction, and late data are needed; DE-058 develops windows and watermarks.

If the producer time actually means “serialization time,” it may be a reasonable capture proxy but should not be relabeled. A source-specific timestamp extractor can choose a deeper authoritative field while preserving broker metadata.

### Choose processing time for operational control

Processing time is appropriate for “retry in 30 seconds,” “flush this buffer after 100 ms,” “alert if no progress for five minutes,” and “expire a local cache after one hour.” These decisions concern the running system now.

Processing-time aggregation is appropriate when the question itself is arrival-oriented, such as requests admitted per service minute or work processed per billing interval. It is not a substitute for event time because it is easier.

Record which stage's processing time is used. Source operator receipt, transformation execution, sink write, and query refresh can differ substantially. Retry creates new processing-time observations for the same event.

### Understand ingestion and broker timestamp policies

Ingestion or append time is useful when producers are untrusted, event timestamps are absent, or operators need a consistent platform observation. It narrows producer clock error but includes upstream delay and cannot reconstruct the occurrence.

Kafka's current topic configuration can use `CreateTime` or `LogAppendTime`; the default is `CreateTime`. Kafka Streams' default timestamp extractor interprets these as producer/event-time-like or broker ingestion-time semantics according to server/topic configuration. Therefore the meaning can change without payload schema changes if topic policy changes.

Inventory effective broker and topic configuration, producer timestamp behavior, connector republishing, and migration history. Preserve the record timestamp type or equivalent provenance where APIs expose it.

### Keep source commit and CDC processing time distinct

Change-data-capture events often contain both when the database change occurred/committed and when the connector processed the event. Debezium's SQL Server documentation, for example, distinguishes `source.ts_ms` for the database change from envelope `ts_ms` for connector processing, and uses their difference as a lag indicator.

The precise source field varies by connector and database. Some databases expose transaction commit time imperfectly or not at all; log sequence number is often stronger ordering evidence. Preserve transaction and log coordinates alongside time.

Connector processing time can diagnose capture lag. It should not replace source commit time in business history simply because it is populated consistently.

### Separate timestamp order from causal order

If command A causes event B, record causation or business version. Wall-clock timestamps can invert under skew or network delay. If two independent events are concurrent, sorting by time imposes a presentation order but does not discover causality.

For one partition, offset order is deterministic log order even when timestamps decrease. For one database, LSN/transaction order may govern change application. For one aggregate, expected versions may govern legal state. Event time can still drive temporal analysis, but conflict resolution should use the declared authority.

Never use “latest timestamp wins” unless the source, clock error, concurrency, and correction semantics make it a legitimate domain rule. Otherwise a far-future clock can suppress valid updates indefinitely.

### Validate timestamps without destroying delayed data

Validate type, unit, epoch, range, timezone, precision, field presence, and semantic bounds. Compare event time with trusted ingestion time using an uncertainty-aware future threshold and a domain-specific oldest plausible time.

Do not silently replace invalid event time with ingestion time; that changes grouping while concealing quality problems. Preserve the original, attach validation status/reason, and route according to policy: quarantine, degraded proxy field, source repair, or explicit unknown-time bucket.

Offline and batch sources legitimately arrive late. Apply source-class policies rather than one global threshold. A device clock reset may need sequence-based reconstruction; a malicious far-future timestamp needs isolation so it cannot advance event-time progress.

### Represent instants and civil time separately

RFC 3339 provides an interoperable timestamp representation with a numeric UTC offset and optional fractional seconds. Normalize instants for comparison, but preserve the original representation where legal/audit intent matters.

A UTC offset is not a time zone. `-05:00` does not encode daylight-saving changes or future government decisions. For civil schedules and grouping, store the local date/time, an IANA zone identifier such as `America/New_York`, the disambiguation choice for overlaps/gaps, and the rules/version used for materialization.

During fall-back, one local time can map to two instants; during spring-forward, a local time may not exist. Define reject, choose-earlier/later, or shift policy. Future civil appointments may need re-resolution when timezone rules change; historical facts often retain the resolved instant and rule provenance.

### Handle units, precision, and range

Epoch seconds, milliseconds, microseconds, and nanoseconds can all fit common integer types for some dates. A value in the wrong unit may parse into 1970 or a far future year. Put units in schema types/metadata and use range checks plus golden vectors.

Precision is representational granularity; resolution is how often a clock value changes; accuracy is closeness to truth; uncertainty is the bound/estimate. Nine fractional digits do not prove nanosecond accuracy. Rounding can change bucket boundaries and equality.

Use integer or well-specified decimal representations when binary floating point could lose exact large-epoch subsecond values. Define overflow, negative epochs, leap handling, and serialization across languages.

### Treat leap seconds and time scales explicitly

UTC, TAI, GPS-like scales, POSIX/Unix time, and application-smear conventions are not identical around leap adjustments. RFC 3339 syntax permits leap-second notation, while many libraries and Unix-like clocks do not represent it directly. NIST documents UTC leap-second information; platforms may step, repeat, or smear according to implementation.

Most business pipelines can adopt a documented Unix/UTC-like convention and accept bounded behavior near a leap event. Precision systems must record the scale and conversion tables. Never mix TAI, GPS, and Unix epoch counts as if labels alone aligned them.

Test parsing and duration around leap boundaries according to the actual platform. A monotonic duration clock avoids wall-clock discontinuity for elapsed work but does not answer civil-time labeling.

### Design replay semantics

On replay, stored event, source commit, and original append metadata can remain stable. Processing time becomes the replay attempt time unless the historical observation was recorded and deliberately reused. Any transformation calling wall-clock `now()` can produce different output.

Make temporal dependencies explicit inputs: reference-data version, timezone database, holiday calendar, effective policy, and evaluation instant. Deterministic replay may use a logical/test clock derived from the input cut or preserved original decision time.

If the business policy intentionally applies current rules to historical facts, label the result as a new materialization version rather than pretending to reproduce the old output. Compare old/new cuts and publish corrections with lineage.

### Build temporal SLOs correctly

Define freshness as an endpoint pair: domain occurrence to visible result, source commit to target commit, or broker append to consumer effect. State population, percentile, time window, exclusions, and uncertainty. Separate availability from freshness and completeness.

Measure component percentiles and oldest obligations. Percentiles do not add algebraically across dependent distributions, so use trace-linked endpoint observations for end-to-end SLOs and components for diagnosis.

Backlog age based on event time can be distorted by bad/future/ancient timestamps. Pair it with append/ingest age, source position lag, and validation status. Use monotonic timers for in-process deadlines and wall-clock instants for cross-service timestamping.

### Change time semantics safely

A switch from broker append time to payload occurrence time can reassign records to days/windows, change state keys, mark historical data late, and alter retention. Treat it as a data-model migration, not a config toggle.

Introduce a new versioned timestamp field/semantic. Dual-compute outputs over exact cuts, quantify boundary movement, missing/invalid/future rates, correction volume, state growth, freshness, and domain agreement. Preserve old field and timestamp type, and isolate new state/output generation.

Cut over with compatible consumers, explicit checkpoint/state mapping, rollback horizon, and replayable source history. Document how future records, old schemas, corrections, and backfills behave during mixed operation.

### Observe and test clock behavior

Monitor timestamp missing/invalid/unit/range rates; event-minus-ingest distribution; negative/future counts; per-source offset and dispersion; NTP reachability; clock steps/slews; monotonic timer anomalies; event/append/process/visible latency; timezone/tzdb version; and replay result drift.

Test clocks ahead/behind, backward/forward wall steps, drift, synchronization loss, suspend/resume, DST overlap/gap, leap representation, seconds/milliseconds confusion, maximum range, null/default, malicious future, ancient offline, out-of-order arrival, replay at a different time, and timezone-rule update.

Use injected clocks rather than waiting for real time. Golden cases carry original strings, parsed instant, zone, offsets, uncertainty, expected order, and expected validation. Reconcile temporal aggregates against authoritative finite cuts.

### Review the complete time argument

A defensible design connects fourteen claims: domain question and authority are named; timeline fields are separate; representation and scale are specified; clocks have provenance/error; durations use monotonic time; latency endpoints are comparable; causal/business/log order does not rely on wall time; invalid/delayed data has policy; civil time retains zone/rule intent; replay controls `now`; platform timestamp settings are inventoried; SLOs name endpoints; migrations dual-run; and clock fault/reconciliation evidence covers the contract.

If any link is missing, narrow the claim. A timestamp can be precise but inaccurate, standardized but semantically wrong, correctly parsed but from the wrong clock, or chronologically sorted but causally invalid. Time engineering is provenance plus uncertainty plus policy.

## Definitions and Notation

For occurrence $x$, define timestamp observations after conversion to one stated time scale:

- $t_e(x)$: domain event time.
- $t_c(x)$: capture/producer observation time.
- $t_s(x)$: authoritative source commit time when available.
- $t_a(x)$: broker/log append time.
- $t_i(x)$: pipeline ingestion time.
- $t_p^{(j,k)}(x)$: processing time at stage $j$ and attempt $k$.
- $t_o(x)$: accepted output/effect time at the named boundary.
- $t_v(x)$: consumer-visible publication time.
- $\epsilon_j(x)$: uncertainty bound for timestamp $j$.
- $q(x)$: source/log/business sequence or version independent of wall time.
- $z(x)$: civil-time zone identifier and rules version.

Observed event-to-processing delay at stage $j$, attempt $k$ is

$$
\widehat L_{e\to p}^{(j,k)}(x)=t_p^{(j,k)}(x)-t_e(x).
$$

If endpoint errors are bounded,

$$
L_{e\to p}^{(j,k)}(x)\in
[\widehat L-(\epsilon_e+\epsilon_p),\widehat L+(\epsilon_e+\epsilon_p)].
$$

For two events $x,y$, clock evidence proves $x$ occurred before $y$ only if

$$
t_e(x)+\epsilon_e(x)<t_e(y)-\epsilon_e(y).
$$

Otherwise the intervals overlap and timestamp order is uncertain. A source sequence $q(x)<q(y)$ may still prove source order, but not necessarily physical occurrence order.

Latency decomposition for comparable endpoints is

$$
L_{end}=(t_i-t_e)+(t_p-t_i)+(t_o-t_p)+(t_v-t_o).
$$

The identity is algebraic; measured components from different instrumentation may not sum exactly. Do not mix attempts or percentiles.

Let wall-clock readings be $w_1,w_2$ and monotonic readings $m_1,m_2$. For local elapsed duration prefer

$$
\Delta=m_2-m_1,
$$

because a wall correction can make $w_2-w_1$ discontinuous. The monotonic origin is arbitrary and not an interoperable instant.

For a civil tuple $c=(date,time,zone,fold/policy,ruleset)$, conversion to an instant is a versioned partial function $I_z(c)$. It may yield zero instants in a gap, two candidates in an overlap without disambiguation, or change for a future date when rules change.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. **Name the question.** Identify whether the decision concerns domain occurrence, source commit, platform arrival, runtime duration, or visibility.
2. **Inventory fields.** Separate event, capture, commit, append, ingestion, processing, output, and visibility observations.
3. **Specify representation.** Record scale/epoch, unit, precision, range, offset/zone, null/default, and schema version.
4. **Bind provenance.** Name authority, clock domain, capture rule, synchronization, and transformations.
5. **Quantify error.** Carry offset/dispersion/uncertainty and reject unsupported timestamp ordering.
6. **Choose order evidence.** Use source sequence, transaction, partition offset, causal link, or business version where required.
7. **Assign clocks.** Use event time for domain grouping, processing/monotonic time for runtime control, and explicit endpoints for SLOs.
8. **Govern anomalies.** Handle missing, invalid, future, old, corrected, and civil-time-ambiguous inputs without silent overwrite/loss.
9. **Control replay.** Make `now`, reference data, timezone rules, and logical clocks explicit and versioned.
10. **Test and migrate.** Inject clock faults, dual-run semantic changes, compare finite cuts, and preserve rollback evidence.

The core semantic invariant is:

> Every time-dependent decision names the timestamp meaning and authority it uses; no conversion, fallback, correction, or replay silently changes that meaning.

The ordering invariant is:

> Wall-clock order is used as authoritative order only when clock intervals establish it and the domain contract permits it; otherwise a causal, transactional, source, log, or business-version relation decides.

The operational invariant is:

> Elapsed-time control uses a monotonic clock, while cross-system instant observations carry wall-clock provenance and uncertainty.

This executable calculates observed latency components and endpoint-error intervals for four records. It illustrates arithmetic over given readings; it does not establish actual event truth, synchronized clocks, NTP bounds, or platform timestamp semantics.

<!-- bijux-verify: {"id":"time-domain-latency","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"arrival_order=('a', 'b', 'c', 'd')\nevent_time_order=('c', 'a', 'b', 'd')\nprocessing_order=('a', 'c', 'd', 'b')\nsource_delays_ms=(('a', 120), ('b', 80), ('c', 310), ('d', -200))\nqueue_delays_ms=(('a', 130), ('b', 320), ('c', 90), ('d', 50))\nevent_to_process_ms=(('a', 250), ('b', 400), ('c', 400), ('d', -150))\nfuture_clock_records=('d',)\nlatency_bounds_ms=(('a', (-50, 550)), ('b', (100, 700)), ('c', (100, 700)), ('d', (-450, 150)))\nmax_nonnegative_observed_ms=400\n","stderr":""}} -->
```python
records = (
    {"id": "a", "event_ms": 1000, "ingest_ms": 1120, "process_ms": 1250},
    {"id": "b", "event_ms": 1100, "ingest_ms": 1180, "process_ms": 1500},
    {"id": "c", "event_ms": 900, "ingest_ms": 1210, "process_ms": 1300},
    {"id": "d", "event_ms": 1600, "ingest_ms": 1400, "process_ms": 1450},
)
event_error_ms = 250
processing_error_ms = 50
combined_error_ms = event_error_ms + processing_error_ms

arrival_order = tuple(item["id"] for item in sorted(records, key=lambda x: x["ingest_ms"]))
event_order = tuple(item["id"] for item in sorted(records, key=lambda x: x["event_ms"]))
processing_order = tuple(item["id"] for item in sorted(records, key=lambda x: x["process_ms"]))
source_delays = tuple((item["id"], item["ingest_ms"] - item["event_ms"]) for item in records)
queue_delays = tuple((item["id"], item["process_ms"] - item["ingest_ms"]) for item in records)
end_delays = tuple((item["id"], item["process_ms"] - item["event_ms"]) for item in records)
future_clock_records = tuple(item["id"] for item in records if item["event_ms"] > item["ingest_ms"])
bounds = tuple(
    (identifier, (delay - combined_error_ms, delay + combined_error_ms))
    for identifier, delay in end_delays
)

print(f"arrival_order={arrival_order}")
print(f"event_time_order={event_order}")
print(f"processing_order={processing_order}")
print(f"source_delays_ms={source_delays}")
print(f"queue_delays_ms={queue_delays}")
print(f"event_to_process_ms={end_delays}")
print(f"future_clock_records={future_clock_records}")
print(f"latency_bounds_ms={bounds}")
print(f"max_nonnegative_observed_ms={max(delay for _, delay in end_delays if delay >= 0)}")
```

The ±250/±50 ms bounds are supplied assumptions, not measurements. A production system must derive and retain defensible clock evidence.

## Alternatives and Trade-Offs

**Event time versus processing time.** Event time answers domain occurrence questions and supports stable replay but requires trustworthy timestamps and late-data policy. Processing time is simple/current for operations but makes domain results depend on arrival and replay.

**Producer time versus broker append time.** Producer time is closer to origin but inherits device clocks and ambiguity. Append time is platform-controlled but includes upstream delay and can change semantics through broker configuration.

**Source commit time versus row/application time.** Commit time aligns database visibility/transactions; application occurrence can precede it and may be user/domain authoritative. Preserve both with source sequence.

**Wall versus monotonic clock.** Wall time supports cross-system instants and civil correlation but can jump. Monotonic time measures local duration reliably but has an arbitrary, usually nonportable origin.

**Exact reading versus uncertainty interval.** A scalar is easy to store/query but encourages false order/latency precision. An interval or quality metadata is more honest at storage and analytical cost.

**Reject versus quarantine versus proxy invalid time.** Reject protects semantics but can lose obligations. Quarantine preserves evidence but needs repair. A proxy such as ingestion time keeps flow but changes meaning and must be labeled.

**UTC instant versus local civil representation.** UTC is unambiguous for elapsed/order comparisons; civil time preserves user/legal intent. Many applications need both instant and zone/local/rules provenance.

**Fixed offset versus IANA time zone.** Fixed offsets are stable for one instant but cannot express changing civil rules. Zone IDs support history/future policy but depend on an evolving database.

**Original versus corrected event time.** Original values preserve audit/source evidence. Corrected values improve analysis. Store both with correction authority/version rather than destructive overwrite.

**Timestamp order versus sequence/version.** Timestamp order supports temporal analysis across domains but may be uncertain. Source/log/business sequence gives a stronger local order while saying less about physical time.

**Current-time replay versus logical historical clock.** Current time applies today's policy and is easy, but results drift. A recorded/logical clock supports reproduction at the cost of more inputs and versioning.

**Strict future bound versus source-specific tolerance.** Strict bounds resist malicious/broken clocks but reject offline or pre-scheduled facts. Source classification and uncertainty-aware policy are safer than one global number.

## Failure Modes and Misconceptions

**“Timestamp means event time.”** The field may be producer send, database commit, broker append, connector process, or ingestion time. Inspect provenance.

**“Producer create time is when the business event happened.”** It can be serialization time after delay or a host default, not domain authority.

**“Broker time is objective truth.”** It is one platform observation and includes upstream delay; cluster clocks also have error.

**“More decimal digits mean more accuracy.”** Representation precision does not establish clock resolution or correctness.

**“NTP makes clocks identical.”** Synchronization estimates and disciplines clocks with offset, delay, jitter, and dispersion; residual uncertainty remains.

**“Sort by timestamp to recover causality.”** Concurrent sources and skew can invert causal/business order. Use explicit relations/versions.

**“Negative latency should be clamped to zero.”** It signals clock, unit, semantic, or instrumentation defects and must remain visible.

**“Use `time.time()` for retry deadlines.”** Wall-clock adjustments can distort duration. Use the platform's monotonic clock.

**“Monotonic timestamp can be sent to another host.”** Its origin is typically arbitrary and only differences in its documented scope are meaningful.

**“UTC solves time zones.”** It identifies an instant but can lose future/local civil intent such as “09:00 Europe/Dublin.”

**“`EST` is a sufficient zone.”** Abbreviations are ambiguous and do not encode a location's rule history/future.

**“An offset is a timezone.”** `-05:00` does not say whether or when daylight rules apply.

**“Every local time maps to one instant.”** DST/political transitions can create gaps or overlaps.

**“Unix time is exactly UTC everywhere.”** Leap handling and platform conventions differ; state the scale/convention.

**“Milliseconds fit means units are correct.”** Seconds/microseconds can parse as plausible integers. Validate expected range and vectors.

**“Latest timestamp wins.”** A future/bad clock can suppress later valid business versions. Timestamp may not be conflict authority.

**“Processing time is stable on replay.”** Replay occurs at a new time and under a different backlog/capacity schedule.

**“Exactly-once effects make time deterministic.”** The once-only effect can still use a different `now()` or timezone rules during replay.

**“One latency metric diagnoses the pipeline.”** Named components and endpoint scope are needed to identify owner and budget.

**“Changing timestamp extractor is operational only.”** It can reassign windows/state, change lateness, and rewrite business aggregates.

## Worked Examples

### Example 1

A mobile device records a photo at 09:00 while offline and uploads at 15:00. Event time is capture occurrence; ingestion time is 15:00. A user gallery groups by capture day, while operational upload SLO measures request admission to visible object. Replacing the former with ingestion time changes product history.

### Example 2

Two services timestamp commands at 10:00:00.120±80 ms and 10:00:00.200±80 ms. Their intervals overlap, so the 80 ms scalar difference does not prove real order. A causation ID and aggregate version decide the legal transition.

### Example 3

A Kafka topic changes from `CreateTime` to `LogAppendTime` during a migration. The payload field remains unchanged, but an application using the record timestamp moves from producer-time-like to broker-ingestion semantics. Dual extraction and output comparison are required.

### Example 4

A CDC event has database source time 12:00:00.000, connector time 12:00:03.200, broker append 12:00:03.350, and target commit 12:00:04.100. Capture lag is observed as 3.2 s, broker leg 0.15 s, and target leg 0.75 s, subject to clock bounds. LSN remains the source-order authority.

### Example 5

A host's wall clock steps backward two seconds during a 500 ms request. Wall subtraction reports a negative duration. The monotonic interval remains 500 ms. Telemetry retains both the wall endpoints and monotonic duration plus a clock-step event.

### Example 6

`2026-11-01 01:30 America/New_York` occurs twice during the fall overlap. An appointment record stores local date/time, zone, and fold/later-offset choice, plus resolved instant and tzdb version. A bare `01:30 EST` would not preserve the intended candidate reliably.

### Example 7

A sensor's seconds-since-epoch value is decoded as milliseconds, landing in January 1970. Range and source-frequency checks quarantine the record with original bytes. The pipeline does not silently replace it with ingestion time.

### Example 8

A replay in September recomputes a July promotion whose code calls current wall time. Results differ despite exactly-once state recovery. The corrected transform reads an explicit evaluation instant and promotion-calendar version stored with the materialization.

### Example 9

A device clock runs ten minutes ahead. Its event appears future-dated and would advance naive event progress. Source-class validation isolates it, retains sequence and ingestion time, estimates correction from synchronization evidence, and publishes a versioned corrected timestamp after review.

### Example 10

An SLO says 99% of source commits become query-visible within 60 seconds. Traces connect source transaction/LSN to materialized version and carry endpoint clock error. Broker lag and handler duration remain diagnostic SLIs; they are not substituted for the visibility endpoint.

## Cross-Program Connections

Distributed systems contributes partial order, logical clocks, causal metadata, clock synchronization, uncertainty intervals, leases, and impossibility of deriving total causality from imperfect physical clocks.

Operating systems contributes realtime and monotonic clocks, timer resolution, suspend behavior, scheduling, virtualization, clock adjustment, and process-local origins.

Networking contributes variable/asymmetric delay, NTP/PTP transport, jitter, partitions, and timestamping locations. Network latency and clock offset are not independently observable from one one-way sample.

Database systems contributes transaction/commit time, log sequence numbers, temporal tables, system/application time, MVCC visibility, CDC, and bitemporal modeling.

Programming languages contributes datetime types, integer ranges, parsing, timezone libraries, floating-point precision, injected clocks, and serialization compatibility.

Formal methods contributes happened-before, interval order, temporal logic, model checking, and explicit assumptions about clock bounds and failure.

Statistics contributes percentile estimation, censored/biased latency samples, uncertainty propagation, clock-error distributions, and non-additivity of component percentiles.

Site reliability engineering contributes freshness SLOs, tracing, clock-health monitoring, backlog age, fault injection, change comparison, and replay drills.

Security engineering contributes trusted timestamp authority, tamper resistance, replay attacks, malicious future values, audit, and privacy of time/location metadata.

Data governance contributes retention/effective dates, legal time, timezone provenance, correction lineage, reproducibility, and accountable data-quality rules.

Human-computer interaction contributes local display, user intent, ambiguous/nonexistent civil input, locale, and explanations for provisional/corrected results.

Scientific computing contributes time scales, leap seconds, calibration, error bounds, measurement precision, and reproducible observation.

## References

1. Apache Flink. [Generating Watermarks](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/). Accessed 2026-09-03. Primary documentation for assigning event timestamps, event-time progress, periodic/punctuated generation, idle sources, and clock-dependent strategies.
2. Apache Beam. [Basics of the Beam Model](https://beam.apache.org/documentation/basics/). Accessed 2026-09-03. Primary documentation distinguishing event time from processing time and describing watermark estimates, late data, and trigger motivations.
3. Apache Kafka. [Topic Configurations, Apache Kafka 4.3](https://kafka.apache.org/43/configuration/topic-configs/). Accessed 2026-09-03. Primary configuration reference for `CreateTime`, `LogAppendTime`, and broker validation of producer timestamps.
4. Apache Kafka. [Configuring a Streams Application, Apache Kafka 4.3](https://kafka.apache.org/43/streams/developer-guide/config-streams/). Accessed 2026-09-03. Primary documentation for timestamp extraction and producer-time versus broker-ingestion semantics.
5. Apache Kafka. [TimestampType API, Apache Kafka 4.3](https://kafka.apache.org/43/javadoc/org/apache/kafka/common/record/TimestampType.html). Accessed 2026-09-03. Primary API definition of create-time, log-append-time, and absent timestamp types.
6. Debezium. [Debezium Connector for SQL Server](https://debezium.io/documentation/reference/stable/connectors/sqlserver.html). Accessed 2026-09-03. Primary connector documentation distinguishing source database time from connector processing time and deriving capture lag.
7. RFC Editor. [RFC 3339: Date and Time on the Internet: Timestamps](https://www.rfc-editor.org/info/rfc3339/). Accessed 2026-09-03. Primary Internet standard for interoperable instant representation, numeric offsets, fractional seconds, and leap-second syntax.
8. RFC Editor. [RFC 5905: Network Time Protocol Version 4](https://www.rfc-editor.org/info/rfc5905/). Accessed 2026-09-03. Primary protocol specification for clock offset, round-trip delay, dispersion, jitter, and synchronization distance.
9. Python Software Foundation. [Python `time` Module](https://docs.python.org/3/library/time.html). Accessed 2026-09-03. Primary runtime documentation for wall-clock behavior, monotonic clocks, arbitrary origins, resolution, and platform leap handling.
10. Internet Assigned Numbers Authority. [Theory and Pragmatics of the Time Zone Database](https://data.iana.org/time-zones/theory.html). Accessed 2026-09-03. Primary tzdb documentation for geographic zones, civil-time changes, historical/future limitations, transitions, and leap treatment.
11. National Institute of Standards and Technology. [Leap Second and UT1-UTC Information](https://www.nist.gov/pml/time-and-frequency-division/time-realization/leap-seconds). Accessed 2026-09-03. Primary time-service reference for UTC(NIST), leap-second history, and current UT1-UTC information.

## Exercises

### Exercise 1

For records `a:(event=1000, ingest=1120, process=1250)`, `b:(1100,1180,1500)`, `c:(900,1210,1300)`, and `d:(1600,1400,1450)` milliseconds, compute arrival, event-time, and processing order; source, queue, and event-to-process delays; and future-clock flags. With event uncertainty ±250 ms and processing uncertainty ±50 ms, compute each end-delay interval.

### Exercise 2

Event A is stamped 1000±30 ms, B is 1040±20 ms, and C is 1100±20 ms on comparable scales. Determine which pairwise real-time orders are proven by non-overlapping intervals. Explain what additional sequence/causal evidence is required when intervals overlap.

### Exercise 3

Design storage and input validation for a user appointment entered as `2026-11-01 01:30` in `America/New_York`. Address overlap/gap policy, resolved instant, original civil intent, zone/tzdb version, future rule changes, display, audit, and replay.

### Exercise 4

A source commit-to-visible SLO is 60 seconds. One trace reports source-to-ingest 12 s, queue 18 s, compute 7 s, output 5 s, and publication 9 s. Compute the total and remaining budget. Endpoint uncertainties are ±400 ms and ±600 ms; report the total latency interval and explain why adding p99 component values does not establish end-to-end p99.

### Exercise 5

Plan a migration from Kafka record `LogAppendTime` processing to a payload `occurred_at` field for daily domain aggregates. Include authority/schema, timestamp validation, dual extraction, state/output isolation, late/future data, timezone policy, exact-cut comparison, replay, checkpoint/state cutover, rollback, monitoring, and domain sign-off.

## Answers to the Exercises

### Answer 1

Arrival/ingestion order is `a,b,c,d`; event-time order is `c,a,b,d`; processing order is `a,c,d,b`. Source delays are a 120 ms, b 80 ms, c 310 ms, and d -200 ms. Queue delays are a 130 ms, b 320 ms, c 90 ms, and d 50 ms. Event-to-process delays are a 250 ms, b 400 ms, c 400 ms, and d -150 ms; d is future-clock flagged because event exceeds ingestion. Combined endpoint uncertainty is 300 ms, giving a `[-50,550]`, b `[100,700]`, c `[100,700]`, and d `[-450,150]` ms. The values are observational intervals, not proof of actual transit; d suggests clock/semantic/unit investigation.

### Answer 2

A's interval is `[970,1030]`, B's `[1020,1060]`, and C's `[1080,1120]`. A and B overlap from 1020 to 1030, so neither A-before-B nor B-before-A is proved. B's latest possible time 1060 is earlier than C's earliest 1080, so B before C is proved under the stated bounds. A's latest 1030 is also before C's earliest 1080, so A before C is proved. For A/B use an authoritative source sequence, transaction order, partition offset where applicable, business version, or explicit causation; do not invent order from midpoint timestamps.

### Answer 3

Store the original local date/time, IANA zone `America/New_York`, user/tenant intent, and explicit overlap selection such as earlier/later offset (or reject and ask). Resolve to a UTC-like instant using a recorded tzdb version and store the resulting numeric offset. The fall overlap can yield two candidates, so silent defaulting is unsafe; spring gaps require reject/shift policy too. Display should convert the stored instant in the intended/current policy while surfacing offset where ambiguity matters. Because future government rules may change, retain civil fields and re-resolve before execution under a versioned policy, recording any change and notification. Replay chooses either original resolved instant/rules or current-policy rematerialization explicitly; audit keeps both.

### Answer 4

The component total is $12+18+7+5+9=51$ seconds, leaving 9 seconds of the 60-second budget for this trace. Combined endpoint uncertainty is 1.0 second, so a 51-second observed endpoint latency corresponds conservatively to `[50,52]` seconds. This does not change the component ownership arithmetic but qualifies the observed total. Adding component p99 values mixes potentially different records and dependence structures; it can over- or under-characterize end-to-end p99. Measure linked source/visible endpoints for each occurrence, then compute the end-to-end distribution; use component percentiles for diagnosis.

### Answer 5

Define `occurred_at` authority, RFC/epoch/unit/precision, timezone/offset, uncertainty, version, correction, and source-specific missing/future/old policy. Inventory current effective topic `LogAppendTime`, extractor, states, windows, outputs, and retained cuts. Add a new extractor and dual-record both broker append and payload event time without overwriting either. Run a separate state/output generation over exact source cuts; quantify day/window reassignment, late/future/invalid rates, correction volume, state growth, freshness, and business totals, with IANA zone/rules for civil-day grouping. Replays use stored event time and versioned reference/tzdb policy, not current wall time. Validate domain samples and delayed/offline/adversarial cases. Cut over at a named checkpoint with compatible code/state mapping or rebuild from a finite cut, preserve source/state for rollback, and prevent mixed semantics in one materialization. Monitor both timestamp distributions, clock quality, output deltas, watermark behavior (developed in DE-058), and user-visible reconciliation; require domain-owner sign-off on changed totals and correction policy.
