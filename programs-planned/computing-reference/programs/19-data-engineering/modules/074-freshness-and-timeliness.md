---
module_id: DE-074
program: Data Engineering
level: 2
module_number: 74
title: Freshness and Timeliness
status: complete
last_verified: 2026-09-03
---

# Freshness and Timeliness

## One-Page Review

### Governing question

How can a data team prove that every required cohort is current enough and available by its business deadline when event time, source commit time, ingestion time, processing time, publication time, quiet periods, late data, backfills, retries, and clock uncertainty tell different stories?

### Essential definitions

- **Freshness** is the age of the newest trustworthy business-effective data for a declared cohort at an observation time.
- **Timeliness** is conformance to a declared arrival, processing, validation, or publication deadline for a particular expected interval or event.
- **Event/effective time** says when a fact occurred or became true in the business domain.
- **Source commit time** says when the source durably recorded the fact; **ingestion time** says when the data platform accepted it.
- **Processing time** is the worker's clock while computation occurs; **publication time** is when a committed, validated version becomes visible to consumers.
- A **data interval** is the logical business interval a run is responsible for; it is not necessarily the run's wall-clock execution interval.
- A **freshness frontier** is the greatest event/effective time proven complete enough under a named late-data and coverage policy.
- A **watermark** is a progress assertion about event time under a source/engine policy; it is not proof that every expected event exists.
- **Schedule delay** is actual start minus eligible/scheduled start; **runtime** is finish minus start; **publication delay** is visible time minus interval deadline or end.
- **End-to-end latency** is consumer-visible time minus the selected origin time for the same fact/version.
- An **expected-arrival calendar** enumerates which cohorts/intervals should arrive and when, including timezones, holidays, closures, and no-data declarations.
- A **heartbeat** is an explicit progress record emitted even when no business events occur.
- A **freshness/timeliness SLO** defines subject, clock, population, percentile or fraction, threshold, window, exclusions, and error-budget policy.
- **Pending** means the applicable deadline or lateness window has not expired; **late/stale** means it has; **unknown** means measurement evidence is unavailable or incomplete.
- A **backfill** republishes historical intervals and must not make current-period freshness appear better merely because its load time is recent.

### Central model, mechanism, or theorem

For cohort $c$ observed at trusted time $t_o$, let $F_c(t_o)$ be its proven event-time frontier. Its age is

$$
A_c(t_o)=\max(0,t_o-F_c(t_o)).
$$

For expected interval $i$ with deadline $D_i$ and atomic consumer-visible publication time $P_i$, publication lateness is

$$
L_i=\max(0,P_i-D_i).
$$

For record $x$, decompose end-to-end latency:

$$
t_{visible}(x)-t_{event}(x)=
[t_{commit}-t_{event}]+[t_{ingest}-t_{commit}]+[t_{finish}-t_{ingest}]+[t_{visible}-t_{finish}].
$$

The terms expose source, transport, compute, and publication delay. They are meaningful only when the timestamps refer to the same identity/version and their clocks and uncertainty are documented. A recent maximum event timestamp does not imply completeness: the newest event may be present while an earlier required event or partition is missing.

### Critical invariants

- Every metric names the dataset/version, cohort, expected interval, business purpose, origin and observation clocks, timezone, threshold, window, and owner.
- Event/effective, source commit, ingestion, processing, validation, and publication times remain distinct fields.
- Freshness uses a proven frontier, not blindly `MAX(timestamp)`, filesystem modification time, task finish time, or load time.
- Expected-arrival calendars distinguish healthy quiet periods from missing feeds and account for weekends, holidays, daylight-saving transitions, and source closures.
- Measurements cover every required tenant, partition, region, source, and shard; a fresh fast cohort cannot hide a stale slow one.
- Empty expected intervals produce explicit no-data/progress evidence; absence is not automatically success or failure.
- Data and its publication marker/version commit atomically or through a recoverable protocol.
- Watermark, offset, source commit, target checkpoint, row counts, and quality results identify the same committed cut.
- Late and corrected events reopen affected windows under versioned finality policy rather than silently rewriting evidence.
- Backfills retain original event/effective time and interval identity; recent ingestion does not relabel old data as fresh.
- Clock source, synchronization, skew bound, timestamp precision, and monotonic versus wall-clock use are documented.
- Missing metrics, failed probes, partial scans, and stale monitoring paths yield unknown, never a synthetic zero-lag pass.
- SLOs specify per-event versus per-interval semantics, percentile/fraction aggregation, consecutive-breach rules, and error-budget math.
- Alerts include duration and cohort context, deduplicate symptoms, inhibit downstream noise, and link to bounded remediation.
- Historical observations are immutable and sufficient to recompute whether the contract passed at the time.

### Common failures

Common failures include equating a green scheduler with fresh data; measuring table update time after maintenance; using ingestion time for backfilled records; trusting global `MAX(event_time)` while one partition is stale; declaring quiet streams healthy without heartbeats; treating a watermark as completeness proof; comparing clocks with unknown skew; confusing logical date with actual start; alerting before a batch deadline; averaging lag across tenants; dropping late events to improve metrics; publishing a success marker before the table commit; resetting age to zero on an empty overwrite; measuring only successful runs; letting monitoring lag report zero; using one threshold for trading and monthly reporting; and paging on every transient breach without an error-budget policy.

### Compact example

A ten-minute interval expects events at minutes 0, 5, and 10. At minute 16, the target contains events for 0 and 10. The newest event is six minutes old and passes a ten-minute freshness threshold. Publication at minute 14 also beats a minute-15 deadline. Yet minute 5 is absent, so interval completeness fails and release readiness is false. After the missing event is incorporated into a new version, the combined freshness, deadline, and coverage gate passes. Recency and timeliness were necessary evidence, not sufficient evidence.

### Connections

[DE-023](023-file-arrival-and-manifest-processing.md) establishes expected arrivals, [DE-030](030-designing-replayable-raw-ingestion.md) preserves event and ingestion provenance, [DE-049](049-run-metadata-and-operational-state.md) identifies logical intervals and executions, [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) defines lateness and correction behavior, [DE-066](066-time-travel-and-reproducible-reads.md) pins published versions, [DE-071](071-completeness-validity-accuracy-and-consistency.md) defines coverage, and [DE-073](073-reconciliation-tests.md) aligns source and target cuts. DE-075 adds volume and distribution monitoring.

## Governing Question

“The pipeline succeeded at 06:05” says little by itself. The run may have processed yesterday's already-stale extract, skipped one tenant, published an unvalidated version, or finished before a source delivered its final partition. Conversely, an intentionally quiet source can be healthy even though its latest business event is old.

Freshness and timeliness therefore require an expectation model. The contract must say what data is expected, which time gives business meaning, when it should become available, how late corrections behave, and how absence is distinguished from silence. Measurement without that model produces attractive but misleading age gauges.

The time axis is plural. Event time locates a fact in the domain. Commit time locates durable source acceptance. Ingestion time locates platform acceptance. Processing and publication clocks describe internal delivery. Comparing adjacent timestamps diagnoses where latency accrued, while substituting one for another changes the question.

The governing requirement is cohort-complete, versioned temporal evidence tied to a consumer promise. A usable design can say not only “stale,” but which source, interval, partition, stage, and dependency caused the miss; whether the state is pending, late, or unknown; which consumers are affected; and which repair is safe.

## Why This Matters

Correct old data can be operationally wrong. Inventory, entitlements, fraud features, incident telemetry, prices, and regulatory positions lose fitness as decisions outrun their update cadence. The acceptable age depends on the use: milliseconds, minutes, daily close, or monthly certification can all be valid contracts.

Freshness defects often precede visible correctness defects. A stalled source, growing consumer lag, held watermark, or delayed partition can be detected before a consumer notices missing decisions. Stage-specific latency turns that early signal into diagnosis rather than a generic page.

Bad metrics create both false confidence and noise. A global maximum is dominated by the fastest producer. An average hides a stranded tenant. A job-finish timestamp says code ended, not data was complete or visible. Repeated false alarms teach responders to ignore the control when a real breach arrives.

Temporal evidence also governs release and incident decisions. Some products may serve a labeled last-known-good version; others must fail closed. Some late records can update prior windows; others require human certification. The policy belongs in the data product contract, not improvised during an outage.

Freshness observations can reveal business activity patterns, customer presence, or operational incidents. Store the minimum cohort detail needed, protect identifiers, and define retention just as for other quality evidence.

## Prerequisites and Retrieval

Retrieve business purpose: consumers, decisions, harm from delay, required cadence, deadline, service window, timezone, critical cohorts, maximum age, degradation mode, materiality, and owner.

Retrieve expected arrivals: source/calendar identity, intervals, partitions, tenants, weekdays, holidays, closures, cutoff rules, no-data declarations, heartbeat behavior, source backfills, and schema/control manifests.

Retrieve time semantics: event/effective time, source commit time, ingestion/landing time, processing start/finish, validation finish, publication/visibility time, consumer observation time, precision, timezone, clock source, skew, and monotonic-clock availability.

Retrieve source progress: database log position, broker partition offsets, object manifest, sequence, transaction boundary, extraction watermark, API cursor, source high-water mark, and evidence that a quiet interval is complete.

Retrieve pipeline progress: scheduler logical interval, eligibility and actual start, retries, task attempts, queue delay, dependency/sensor wait, runtime, checkpoint, watermark per input, idle-partition policy, state backlog, and resource saturation.

Retrieve target publication: dataset and table identity, committed version, atomic marker, validation status, cache/index/materialized-view refresh, serving replication, catalog state, consumer visibility probe, and rollback version.

Retrieve quality policy: frontier rule, threshold per cohort/use, allowed lateness, completeness dependency, percentile/fraction, rolling window, consecutive-breach requirement, maintenance exclusions, error budget, severity, gate, and escalation.

Retrieve monitoring system: query and code version, evaluator schedule, metric timestamp, scrape/transport delay, missing-series policy, cardinality, retention, alert grouping, inhibition, runbook, and monitor-of-monitor control.

Distinguish event time from arrival time; logical interval from wall-clock execution; newest observed event from proven frontier; quiet from missing; pending from late; late event from late publication; source lag from target lag; data version from task attempt; last-known-good from latest attempted; clock skew from negative latency; and measurement failure from zero delay.

Create a temporal contract:

| Concern | Required decision and evidence |
|---|---|
| Subject | Product/version, cohort grain, required intervals and consumers |
| Clocks | Meaning, source, timezone, precision, skew bound and timestamp identity |
| Expectation | Calendar, cutoff, manifests, heartbeats and no-data declarations |
| Frontier | Event-time completeness rule, watermark/offset and allowed lateness |
| Delivery | Eligible/start/finish/validate/publish/visible milestones and deadlines |
| Objective | Age/latency threshold, percentile/fraction, window and error budget |
| State | Pending, healthy, stale, late, unknown, excluded and recovering |
| Action | Gate, degrade, alert, escalate, replay, backfill and revalidate |
| Evidence | Pinned versions, per-cohort metrics, coverage, decisions and retention |

Write a falsifiable claim: “At 06:15 UTC, product P version V42 covers every expected tenant/day partition through business date 2026-09-02; each source manifest is complete, target checkpoint equals the committed source frontier, maximum per-tenant event age is under 25 hours, 99.5% of events in the trailing 30 days became consumer-visible within 20 minutes, the daily version was atomically published before its 06:10 deadline in 29 of 30 eligible intervals, and the remaining miss consumed one explicitly computed error-budget interval.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish freshness, timeliness, event time, commit time, ingestion time, processing time, and publication time;
2. define expected-arrival calendars, heartbeats, no-data declarations, and cohort-complete frontiers;
3. decompose end-to-end latency into source, transport, compute, validation, and serving stages;
4. use watermarks, offsets, manifests, and checkpoints without overstating what they prove;
5. design batch and streaming freshness checks that survive quiet inputs, late data, retries, and backfills;
6. specify SLO thresholds, percentiles, rolling windows, consecutive breaches, and error budgets;
7. account for timezone, daylight-saving, precision, clock skew, and monotonic duration measurement;
8. distinguish pending, late, stale, unknown, excluded, and recovering states;
9. create actionable alerts and safe degradation/recovery procedures; and
10. preserve versioned evidence sufficient for audit and historical recomputation.

## Core Exposition

### Define freshness from the consumer backward

Start with the decision, not the available timestamp column. Ask what fact must be current, for whom, and by when. A customer dashboard may require each tenant through its local business close; a fraud feature may require event-to-serving latency; a monthly report may require certified completeness by a filing deadline.

Choose cohort grain before aggregation. Measure per tenant, region, source, partition, instrument, or another failure domain. Summarize with maximum, quantiles, and breach fractions only after retaining cohort evidence. A global maximum timestamp is a claim about one row, not the population.

Define the frontier. `MAX(event_time)` is acceptable only when the newest record is itself sufficient under the contract. Usually the frontier needs a manifest, contiguous sequence/offset, expected key set, source close marker, watermark plus late-data policy, or reconciliation result. Call it “observed maximum” until completeness evidence qualifies it.

Separate record age from interval delivery. Record age answers how old the newest qualified fact is. Interval timeliness asks whether the complete version for logical interval $i$ was visible by $D_i$. A stream can have good median record latency but miss a required daily close; a batch can publish on time while containing old source data.

### Model every clock and milestone

Record timestamps at durable boundaries: event/effective, source commit, connector capture, platform ingress, processing start/finish, validation finish, target commit, publication marker, cache/serving visibility, and observation. Attach record/run/version identity so subtraction pairs the same work.

Use wall clocks for business deadlines and cross-system timestamps. Use monotonic clocks for duration inside one process because wall time can jump. Synchronize infrastructure clocks and retain an uncertainty bound. A negative stage latency usually signals mismatched identity, precision, timezone, or clock skew; do not clamp it silently before diagnosis.

Decompose delay. If source commit-to-ingest grows, inspect connector/log access/network. If ingest-to-finish grows, inspect queueing, backlog, skew, capacity, checkpoints, and retries. If finish-to-visible grows, inspect validation, transactions, catalogs, caches, replicas, and publication protocol.

Logical dates are labels for data intervals, not execution instants. A daily interval normally becomes eligible after its end. Retries and backfills share a logical interval but have distinct attempts and wall-clock milestones. Report both.

### Build expected-arrival and completion evidence

An arrival calendar is executable data. Enumerate expected interval/cohort keys, eligibility time, deadline, timezone/calendar version, dependencies, and no-data behavior. Generate observations by left joining expectations to actual committed arrivals so missing rows remain visible.

Calendar time is domain-specific. Daylight-saving transitions contain 23 or 25 local hours; market holidays and month ends vary; upstream maintenance may be planned. Version changes rather than editing history. Apply exclusions narrowly and record approval, interval, reason, and affected consumers.

Quiet inputs need explicit progress. A heartbeat may state “source alive through offset/time X with zero business events.” A file source can publish a zero-row manifest. A database can expose a committed log position. Without such evidence, silence is unknown even if silence is common.

Completion should be atomic with data or recoverable. A marker before data becomes visible yields a false-ready window. Data before a marker may be safe but appears late and must recover idempotently. Prefer one transaction/version pointer or a protocol whose states and repair are tested.

### Operate batch freshness

For each logical interval, track expected time $E_i$, deadline $D_i$, eligible time, dependency-ready time, queued/start time, finish, validation, target commit, and consumer-visible publication. Store delays and status per stage.

Test the payload, not only orchestration. Verify manifest/partition coverage, row counts or declared zero, event-time bounds, source cutoff, reconciliation, schema/quality status, and target version. A task can succeed with a stale input path or a partial dynamic partition list.

Retries preserve the interval identity. The first attempt may miss its deadline while a later attempt succeeds. Retain time-to-first-good-publication and attempt history; do not rewrite the SLO outcome to on-time merely because the final state is healthy.

Backfills use original business/effective timestamps and a backfill reason. Separate “historical interval successfully republished now” from current freshness. If the backfill changes derived current state, identify and republish affected present windows deliberately.

### Operate streaming freshness

Track source log/partition progress, consumer position, event-time frontier, processing-time observation, target committed checkpoint, and serving visibility. Offset lag is workload units, not elapsed time; time lag is not backlog size. Both help diagnose capacity and source idleness.

Watermarks encode a late-data assumption. A watermark near now can permit windows to close, but cannot prove an upstream event was never lost. Validate sequence continuity, expected source partitions, checkpoints, and periodic source-target reconciliation alongside it.

Multi-input operators typically progress at the slowest active input. An idle partition can freeze a minimum watermark; marking it idle can restore progress but risks misclassifying a merely delayed partition. Base idleness on source semantics and reactivation tests. Watermark alignment can bound fast/slow drift and state growth but may throttle throughput.

Measure late-arrival distributions relative to event and ingest time: count/fraction and quantiles by cohort, plus correction depth and windows reopened. Configure allowed lateness from risk and observed distributions, then monitor tail movement. Dropping late data makes the latency chart prettier by deleting evidence; route, correct, or explicitly reject it instead.

### Define objectives and gates

Choose a service-level indicator with a precise population. Per-event latency SLI might be

$$
SLI_{event}(W)=\frac{|\{x\in W:\ell(x)\le\tau\}|}{|\{x\in W:\ell(x)\text{ measured}\}|}.
$$

Its companion coverage reports measured eligible events divided by intended eligible events. Without coverage, disappearing slow events improve the SLI.

Per-interval timeliness is

$$
SLI_{interval}(W)=\frac{|\{i\in W:P_i\le D_i\land Complete_i\}|}{|Expected(W)|}.
$$

Store numerator, denominator, exclusions, unknowns, and distribution, not only a percentage. Define rolling or calendar window and whether consecutive failures page sooner than budget exhaustion.

If the objective permits fraction $p$ on $N$ expected intervals, the nominal failure allowance is $N(1-p)$; state rounding policy because intervals are indivisible. Track consumption and burn rate. Error budgets authorize product decisions but do not transform late data into on-time data.

Gate on combined evidence. A publishable version may require frontier age, interval completeness, quality/reconciliation success, committed checkpoint, target visibility, and monitor coverage. Critical unknowns hold the gate. A warning-only product can publish a clearly labeled last-known-good version under an agreed degradation policy.

### Monitor, alert, recover, and learn

Export per-stage latency, frontier age, observed-max age, schedule delay, runtime, publication delay, source/target offset positions, backlog, late fraction, correction depth, expected/arrived intervals, unknowns, last-good version, and SLO budget.

Keep cardinality controlled while preserving diagnosis. Aggregate low-risk cohort labels, store detailed evidence in governed tables, and link alert instances to run/version IDs. Monitor the evaluator's own last success and input coverage; a silent monitor is not a healthy product.

Alert after the contract says a cohort should exist, accounting for deadline and grace rather than arbitrary scheduler cadence. Require a suitable duration to avoid transient noise, but page immediately for hard deadlines. Group related downstream symptoms under the earliest common stale dependency and inhibit cascades.

Runbooks classify source-not-ready, capture lag, queue/capacity, compute failure, validation hold, publication inconsistency, serving cache/replica, monitor failure, and clock fault. Preserve evidence, protect last-known-good, communicate exact affected versions/cohorts, and choose replay/backfill/resync under idempotent semantics.

Recovery needs a new proven version. Verify expected coverage, temporal frontier, quality, reconciliation, publication visibility, and downstream refresh. Close the incident only after backlog and SLO burn stabilize. Review recurrence, detection delay, time to safe data, false alarms, and whether the expectation model itself was wrong.

## Definitions and Notation

Let:

- $t_o$ be observation time from the named monitoring clock;
- $t_e(x),t_c(x),t_i(x),t_f(x),t_p(x),t_v(x)$ be event, source-commit, ingest, processing-finish, publish, and consumer-visible times for fact $x$;
- $c$ be a required cohort and $F_c(t_o)$ its proven event-time frontier;
- $A_c(t_o)=\max(0,t_o-F_c(t_o))$ be frontier age;
- $i=[B_i,E_i)$ be a logical data interval with deadline $D_i$;
- $P_i$ be first complete, validated, consumer-visible publication time;
- $L_i=\max(0,P_i-D_i)$ be positive publication lateness;
- $X(W)$ be expected intervals/events in evaluation window $W$;
- $M(W)\subseteq X(W)$ be those whose latency was successfully measured;
- $Good_\tau(W)=\{x\in M(W):t_v(x)-t_e(x)\le\tau\}$; and
- $U(W)=X(W)\setminus M(W)$ be missing/unknown measurement coverage.

Then event-latency compliance and measurement coverage are

$$
Q_\tau(W)=\frac{|Good_\tau(W)|}{|M(W)|},\qquad C(W)=\frac{|M(W)|}{|X(W)|}.
$$

Both are required. If $|X(W)|=0$, apply the declared no-traffic semantics rather than dividing by zero. An interval is on-time only when

$$
OnTime(i)\iff Complete(i)\land Valid(i)\land P_i\le D_i.
$$

This prevents an early partial publication from satisfying the deadline. If clocks have uncertainty bounds $\epsilon_a$ and $\epsilon_b$, a cross-clock latency should carry at least the combined uncertainty rather than report spurious precision.

## Mechanisms, Invariants, or Proof Structure

Proof sketch that a recent maximum timestamp does not prove interval completeness:

1. Let interval $i$ require events with identities at minutes $0$, $5$, and $10$.
2. Let the target contain the minute-$0$ and minute-$10$ events but omit minute $5$.
3. Observe the target at minute $16$ with a maximum-age threshold of ten minutes.
4. Its maximum observed event time is minute $10$, so observed age is six minutes and the freshness check passes.
5. Yet the required identity at minute $5$ is absent, so interval completeness is false.
6. Therefore `MAX(event_time)` age below a threshold does not imply completeness of the expected interval.
7. A safe release gate conjoins temporal recency with expectation/manifest coverage and other required quality evidence.

The result does not make maximum timestamp useless. It is an efficient recency signal when its subject and coverage are explicit. The proof bounds the claim it can support.

The executable reproduces the counterexample, an on-time publication, the combined failed release gate, and a repaired complete interval. It is a deterministic teaching model, not a scheduler, watermark generator, clock-synchronization service, stream processor, or SLO platform.

<!-- bijux-verify: {"id":"freshness-with-coverage","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"freshness_age_minutes=6\nfreshness_pass=True\nmissing_expected_minutes=(5,)\ninterval_complete=False\npublication_delay_minutes=4\ndeadline_pass=True\nrelease_ready=False\nrepaired_release_ready=True\n","stderr":""}} -->
```python
expected_minutes = {0, 5, 10}
observed_minutes = {0, 10}
observation_minute = 16
freshness_threshold = 10
interval_end_minute = 10
publication_minute = 14
deadline_minute = 15

freshness_age = observation_minute - max(observed_minutes)
missing = tuple(sorted(expected_minutes - observed_minutes))
freshness_pass = freshness_age <= freshness_threshold
interval_complete = not missing
deadline_pass = publication_minute <= deadline_minute

print(f"freshness_age_minutes={freshness_age}")
print(f"freshness_pass={freshness_pass}")
print(f"missing_expected_minutes={missing}")
print(f"interval_complete={interval_complete}")
print(f"publication_delay_minutes={publication_minute - interval_end_minute}")
print(f"deadline_pass={deadline_pass}")
print(f"release_ready={freshness_pass and interval_complete and deadline_pass}")

repaired_minutes = observed_minutes | {5}
repaired_ready = (
    observation_minute - max(repaired_minutes) <= freshness_threshold
    and repaired_minutes == expected_minutes
    and deadline_pass
)
print(f"repaired_release_ready={repaired_ready}")
```

## Alternatives and Trade-Offs

1. **Observed maximum versus proven frontier:** maximum is cheap and responsive; a manifest/contiguous frontier is stronger but requires source cooperation.
2. **Event time versus ingestion time:** event time reflects business recency; ingestion time diagnoses platform arrival and is more controllable but mislabels backfills.
3. **Polling versus push/heartbeats:** polling independently observes state; push is faster and cheaper but can fail silently without liveness controls.
4. **Global versus cohort metrics:** global metrics are compact; cohort metrics expose isolated failures but increase storage and cardinality.
5. **Maximum versus quantiles:** maximum protects every cohort/event but is noisy; quantiles support high-volume objectives while allowing a declared tail.
6. **Hard deadline versus rolling SLO:** a hard close matches discrete business obligations; a rolling budget supports continuous services but can obscure a critical one-off miss.
7. **Strict watermark versus allowed lateness:** strict closure reduces latency/state; wider lateness improves completeness but delays finality and increases correction cost.
8. **Idle-input detection versus waiting:** idleness restores progress for quiet sources; a mistaken idle classification can close windows before delayed data.
9. **Fail closed versus last-known-good:** holding protects correctness; serving labeled older data may preserve availability when consumers can tolerate staleness.
10. **One atomic publish versus staged serving:** atomic pointers give clean visibility; multi-stage caches/replicas need end-user probes and more state tracking.
11. **Per-event instrumentation versus sampled latency:** exact timestamps support strong tails and diagnosis; sampling costs less but needs inclusion probabilities and coverage labels.
12. **Automatic backfill versus manual approval:** automation shortens recovery; bounded approval may be necessary when correction changes certified or externally consumed history.

Choose by business loss from stale or unavailable data, source semantics, correction frequency, traffic shape, scale, privacy, and ability to create trustworthy completion evidence. Preserve which alternative was selected and what it cannot prove.

## Failure Modes and Misconceptions

- **“The DAG succeeded, so the data is fresh.”** A successful attempt can read stale or partial input and may not prove consumer visibility.
- **“The latest row is recent, so the table is current.”** One new row can hide missing partitions, identities, or cohorts.
- **“No rows means no lag.”** Silence is unknown unless a calendar, heartbeat, or zero-row manifest proves expected quiet.
- **“Watermark means complete.”** It encodes progress/late-data policy, not universal upstream delivery correctness.
- **“Consumer offset lag is time lag.”** Offset counts depend on traffic; pair positions with timestamps and throughput.
- **“Average freshness represents users.”** Averages hide sparse severe cohort failures and long tails.
- **“Load time is the right timestamp.”** It makes historical backfills appear current.
- **“File modification time is source freshness.”** Copies, compaction, metadata repair, and rewrite change it without changing business facts.
- **“Logical date is start time.”** Scheduler logical dates generally label data intervals.
- **“Deadline equals schedule time.”** Eligibility, dependencies, interval end, and consumer promise are separate milestones.
- **“Retry success restores on-time status.”** It restores health but does not erase the original deadline miss.
- **“Clamp negative latency to zero.”** Diagnose clock skew, timezone, precision, and mismatched record identities first.
- **“UTC solves all calendar problems.”** Business intervals may follow local holidays and daylight-saving rules even when storage is UTC.
- **“Every local day is 24 hours.”** DST transitions invalidate that assumption.
- **“One threshold fits every dataset.”** Tolerance follows use and risk, not platform convenience.
- **“Missing monitoring means zero lag.”** Failed or delayed measurement is unknown and should be independently alerted.
- **“Partial scan can pass.”** Coverage must accompany the metric and critical unknowns must hold the gate.
- **“Drop late events to meet the SLO.”** That changes the population and conceals data loss unless rejection is an explicit contract.
- **“A newer target version is fresher.”** It may be a rewrite of old facts or a partial failed recovery.
- **“Publish marker and data will converge.”** Non-atomic visibility creates false-ready or false-late windows that need a protocol.
- **“The fastest partition defines stream progress.”** Required progress is constrained by the slowest applicable active input/cohort.
- **“Mark every quiet partition idle.”** A delayed partition can be mistaken for absent and cause premature finality.
- **“P99 alone is enough.”** Retain count, population, coverage, maximum/critical cohorts, and distribution semantics.
- **“Percentages average naturally.”** Combine numerators and denominators; do not average unequal cohort rates.
- **“Error budget excuses any miss.”** Critical deadlines and cohort-specific policies may override aggregate allowance.
- **“Maintenance exclusions can be permanent.”** Exclusions need scope, expiry, ownership, and historical visibility.
- **“Alert on every threshold crossing.”** Use deadline, duration, seasonality, grouping, and impact to control noise.
- **“Backfill closes the incident automatically.”** Revalidate completeness, current derived state, visibility, and downstream consumption.
- **“Freshness proves accuracy.”** Recent data can be invalid or wrong; temporal evidence is one dimension.
- **“Stale data must always be unavailable.”** Serving last-known-good can be correct if labeled and permitted by consumer policy.

## Worked Examples

### Example 1

A daily ledger closes at 23:59 New York time and must publish by 06:00 local time. The calendar converts each business-day boundary using the named timezone database version, includes holidays, and stores the source close marker. The gate requires complete accounts, reconciliation, certification, and consumer-visible version before the deadline; task success alone is insufficient.

### Example 2

A sensor stream normally emits every second. Per-device heartbeats advance liveness even during an explicit paused state. The platform reports event-time age per device, p99 end-to-end latency, expected-versus-active devices, late fraction, and monitor coverage. A new event from one device cannot hide a disconnected factory.

### Example 3

A CDC pipeline shows source latency at 20 seconds and target latency at 900 seconds while incoming positions continue. The evidence localizes most delay after capture, so responders inspect apply throughput, target indexes, locks, network, and transaction size rather than blaming source log access.

### Example 4

A source publishes hourly object manifests, including `row_count=0`. The arrival evaluator left joins 24 expected hour/source pairs to committed manifests. Hour 13 has no object and no zero manifest, so it is unknown after cutoff; hour 14's zero manifest is complete and timely.

### Example 5

A three-month backfill lands today. The table's storage modification and ingestion times are recent, but event dates remain historical and the product's current frontier does not move. Backfill timeliness is measured against its remediation deadline under a separate objective.

### Example 6

A streaming join receives a high-volume orders input and a quiet currency-rate input. The rate source emits versioned progress heartbeats. Idleness is allowed only outside rate publication windows; watermark alignment bounds excessive order buffering. A missing scheduled rate is late, not idle.

### Example 7

A daily feature table finishes at 04:00 but validation fails until 04:40; the consumer cache exposes the new committed version at 04:44. With a 04:30 deadline, runtime appears healthy but first-good-publication is fourteen minutes late. Stage decomposition attributes the delay to validation and serving.

### Example 8

A continuous product promises 99.9% of eligible events visible within five minutes over 30 days. It also requires 99.99% timestamp coverage and zero unknown critical partitions. Slow events cannot disappear from the latency denominator merely because their visibility probe failed.

### Example 9

During an outage, a dashboard serves last-known-good V51 with `as_of` and stale-state labels while V52 is quarantined. Consumers whose maximum age permits V51 continue; settlement fails closed. Recovery publishes V53 atomically and retains the missed-deadline evidence for V52.

### Example 10

A local-day model sees 23 hourly partitions on spring transition and 25 in autumn. The expectation generator derives UTC boundaries from the business timezone rather than requiring 24 rows. Repeated local hours carry offsets/fold semantics, preventing both false missing and accidental deduplication.

## Cross-Program Connections

- **Distributed Systems:** clocks, causal order, heartbeats, leases, watermarks, checkpoints, backpressure, partitions, and partial failure determine temporal evidence.
- **Reliability Engineering:** SLIs, SLOs, error budgets, burn rates, alert duration, graceful degradation, incident response, and postmortems make freshness operable.
- **Statistics:** quantiles, censored observations, sampling, seasonality, tail risk, confidence, and weighted aggregation bound latency claims.
- **Algorithms and Data Structures:** streaming quantiles, interval sets, heaps, histograms, calendars, and compact offset state control measurement cost.
- **Software Engineering:** monotonic clocks, idempotency, retries, versioning, tests, contracts, and atomic publication prevent temporal regressions.
- **Platform Engineering:** scheduler intervals, sensors, lineage, metric pipelines, catalogs, serving probes, quotas, and policy gates scale controls.
- **API and Service Engineering:** request timestamps, event delivery, pagination snapshots, cache age, retry semantics, and `as_of` metadata expose timeliness to consumers.
- **Systems Engineering:** end-to-end budgets, bottleneck decomposition, feedback delay, coupled queues, and degradation policy connect components to mission outcomes.
- **Security Engineering:** signed time/progress evidence, tamper resistance, least privilege, and monitor integrity protect high-stakes deadlines.
- **Privacy Engineering:** activity timing and cohort metrics can reveal sensitive behavior, requiring minimization, access controls, aggregation, and retention limits.

## References

1. Great Expectations. [Validate data freshness with GX](https://docs.greatexpectations.io/docs/reference/learn/data_quality_use_cases/freshness/). Accessed 2026-09-03. Primary documentation for timestamp-based freshness checks, recency thresholds, and freshness SLAs.
2. dbt Labs. [Source freshness](https://docs.getdbt.com/docs/deploy/source-freshness). Accessed 2026-09-03. Primary documentation for source loaded-at configuration, warning/error thresholds, filters, snapshots, and freshness execution.
3. Apache Airflow. [DAG runs and data intervals](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html). Accessed 2026-09-03. Primary documentation distinguishing logical data intervals, scheduling, actual runs, catchup, and backfill.
4. Apache Flink. [Generating watermarks](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/). Accessed 2026-09-03. Primary documentation for timestamp assignment, bounded out-of-orderness, idle inputs, watermark alignment, and propagation.
5. Apache Flink. [Metrics](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/metrics/). Accessed 2026-09-03. Primary documentation for current input/output watermarks, watermark drift, idleness, checkpoint, backpressure, and operator metrics.
6. Apache Beam. [Programming Guide: watermarks and late data](https://beam.apache.org/documentation/programming-guide/#watermarks-and-late-data). Accessed 2026-09-03. Primary documentation for event time, processing time, watermarks, triggers, allowed lateness, and late-data handling.
7. AWS. [Monitoring AWS DMS tasks](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Monitoring.html). Accessed 2026-09-03. Primary service documentation for source and target CDC latency, throughput, backlog, task, and table metrics.
8. OpenLineage. [Object model](https://openlineage.io/docs/spec/object-model/). Accessed 2026-09-03. Primary specification for run events, event time, nominal timing, datasets, versions, lineage, and extensible facets.
9. OpenLineage. [Facets and extensibility](https://openlineage.io/docs/spec/facets/). Accessed 2026-09-03. Primary specification documentation for attaching run, job, input, and output context to lineage events and safely extending their evidence model.
10. Prometheus. [Alerting rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/). Accessed 2026-09-03. Primary documentation for rule expressions, pending duration, keep-firing behavior, labels, annotations, and alert states.
11. Google. [Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/). Accessed 2026-09-03. Primary SRE book chapter for latency, traffic, errors, saturation, symptom-versus-cause monitoring, and actionable alerts.
12. Apache Kafka. [Monitoring](https://kafka.apache.org/documentation/#monitoring). Accessed 2026-09-03. Primary documentation for broker, producer, consumer, request, lag, and throughput metrics used to diagnose stream progress.
13. Debezium. [PostgreSQL connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html). Accessed 2026-09-03. Primary documentation for source timestamps, LSN offsets, snapshots, replication slots, recovery duplicates, and connector lag evidence.
14. UK Government Data Quality Hub. [The Government Data Quality Framework](https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework). Accessed 2026-09-03. Primary framework for timeliness, lifecycle controls, user needs, measurement, communication, and improvement.

## Exercises

### Exercise 1

Design a freshness and timeliness contract for a daily multi-region financial dataset. Include local calendars, expected cohorts, source close, logical interval, clocks, manifest/frontier, stage milestones, completeness, deadline, SLO, unknowns, publication, evidence, and ownership.

### Exercise 2

Specify temporal monitoring for a partitioned CDC pipeline. Include source and target positions, source/target time lag, event-time watermark, idle partitions, backlog, throughput, checkpoints, late events, correction depth, serving visibility, and diagnosis.

### Exercise 3

Create an SLO for 99.9% of events visible within five minutes and 99% of daily intervals published by 06:00. Define populations, coverage, quantiles/fractions, error-budget rounding, critical cohorts, exclusions, missing telemetry, and alert burn policy.

### Exercise 4

Design a safe monitor and gate for hourly files where legitimate zero-row intervals, delayed manifests, backfills, duplicate deliveries, DST, and source maintenance occur. State how every condition is classified and evidenced.

### Exercise 5

Write a stale-data incident and recovery runbook. Cover triage by latency stage, last-known-good policy, source communication, capacity/backpressure, replay/backfill, temporal and quality revalidation, atomic republish, downstream notification, SLO accounting, and recurrence.

## Answers to the Exercises

### Answer 1

Create region/business-day expectations from versioned timezone and holiday calendars, not a fixed UTC day. Each cohort records source-close marker and log/snapshot cut, zero/nonzero manifest, expected accounts/partitions, and deadline. Store event/effective, source commit, ingest, eligible, start, finish, validation, target commit, publication, consumer-visible, and observation times with named clocks/skew bounds. The frontier advances only when manifests, continuity, completeness, reconciliation, and committed checkpoint agree. Gate requires all critical regions, zero unknown execution, and atomic published version by the regional deadline. Measure per-region age and interval on-time rate, retain attempts/misses, protect detailed evidence, and assign source, pipeline, quality, publication, business, and incident owners.

### Answer 2

For every source partition retain committed source LSN/offset and timestamp, connector-read position, event-time watermark, last heartbeat, incoming rate, and idle decision. Pair these with sink-applied and atomically committed positions, oldest pending event time, backlog records/bytes, processing throughput, target commit, and serving probe. Source time lag high with similar target lag points upstream; low source lag with high target lag points to apply/target capacity. Offset lag without traffic rate is not duration. A minimum watermark stall is classified by partition; idleness is allowed only under source semantics and revoked on return. Track late fraction/quantiles, dropped/routed updates, reopened windows, checkpoint continuity, monitor coverage, and periodic reconciliation.

### Answer 3

Eligible events are source-committed events for named products/cohorts in the rolling 30-day window; visibility is first successful consumer read of their committed target version. Report count within five minutes divided by measured eligible count plus measurement coverage against intended/source counts; critical cohorts also have maximum bounds. Daily population is the calendar's expected complete intervals, and success requires validation plus visibility by 06:00. At 99% over 30 expected days, state whether zero misses are required or one is allowed by rounding; do not silently round 0.3. Exclusions are approved, scoped maintenance only. Missing telemetry is unknown and consumes/blocks under policy. Alert fast on critical cohorts or hard daily deadlines and on multi-window burn rates for the event SLO, with symptom grouping and monitor-liveness alerts.

### Answer 4

Generate `(source,hour)` expectations from timezone-aware half-open intervals; DST produces the correct 23/25 local-hour mapping with offsets. Require an atomically committed manifest containing interval, source cut, object identities/digests, row count, schema, and completion time. A signed zero-row manifest is complete; no file/manifest is pending until cutoff then late; manifest without all objects is inconsistent/unknown; objects without committed manifest are unready; duplicates follow stable delivery identity and are reconciled; backfills retain historical interval and separate remediation deadline. Planned maintenance is a versioned, expiring exclusion. Gate checks manifest, deduplicated coverage, event bounds, quality, target version, and consumer visibility; retain every classification.

### Answer 5

Identify affected products, versions, cohorts, business deadlines, frontier, last-good version, and monitor coverage. Decompose source event-to-commit, capture/transport, queue/start, compute, validation, publish, and serving delay; check clocks before accepting negative values. Preserve manifests, positions, attempts, metrics, and alerts. Follow product policy: fail closed or serve labeled last-known-good with `as_of` and affected-cohort notices. Coordinate source closure/heartbeats, remove bottlenecks without skipping evidence, and replay/backfill idempotently from pinned cuts. Publish a new validated version atomically after completeness, reconciliation, freshness, checkpoints, and end-user visibility pass. Notify consumers of versions and replay needs, retain the original miss in SLO accounting, monitor backlog/burn stabilization, and remediate expectation, capacity, protocol, or alert-design root causes.
