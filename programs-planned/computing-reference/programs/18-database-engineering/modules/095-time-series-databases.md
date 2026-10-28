---
module_id: DBE-095
program: Database Engineering
level: 2
module_number: 95
title: Time-Series Databases
status: complete
last_verified: 2026-09-05
---

# Time-Series Databases

## One-Page Review

### Governing question

How should a database ingest, order, compress, query, retain, and repair timestamped observations when clocks, late data, duplicate points, high-cardinality identities, counter resets, and distributed failure make “time plus value” ambiguous?

### Essential definitions

- A **time series** is an ordered collection of observations for one stable series identity, not merely any table containing a timestamp.
- **Event time** is when the measured event is said to occur; **ingestion time** is when the database accepts it; **processing time** is when computation observes it.
- A **series key** is the canonical identity formed from measurement and indexed dimensions/labels. A field/value is generally not part of identity.
- **Cardinality** is the number of distinct series keys; **churn** is the rate at which series appear and disappear.
- A **sample** contains series identity, event timestamp, value, and often quality, source sequence, or provenance.
- **Out-of-order data** arrives behind the current event-time frontier; **lateness** is its distance from a chosen frontier or watermark.
- A **chunk**, **block**, or **segment** is a bounded physical grouping, commonly by time and series/range.
- **Downsampling** derives lower-resolution aggregates; a **rollup** stores those aggregates under an explicit window and correction contract.
- A **counter** accumulates and may reset; a **gauge** measures a level. Rate calculations require different semantics.
- **Retention** controls logical availability; physical reclamation may occur later through compaction or deletion.

### Central model, mechanism, or theorem

Represent a sample as $(s,t,q,x,m)$: stable series key $s$, event time $t$, source sequence or tie-breaker $q$, value $x$, and metadata $m$. The database must define whether equal $(s,t)$ points reject, replace, merge, coexist, or resolve by $q$. Sorting and compression are physical mechanisms; they do not choose this logical rule.

For fixed-rate sampling frequency $f$, series count $C$, and retention $H$ seconds, the ideal point count is $P=CfH$. Physical capacity adds identity/index metadata, timestamp and value encoding, WAL, replication, compaction, rollups, late-data buffers, and headroom. High series cardinality can dominate even when $P$ is modest.

### Critical invariants

- series identity is canonical, bounded, authorized, and stable across writers and query paths;
- timestamp units, time zone, precision, leap/clock behavior, and tie-breaking are explicit;
- accepted duplicate and out-of-order samples follow one deterministic version/correction rule;
- range queries return the correct ordered snapshot without silently omitting late or repaired data;
- counter rates distinguish resets, wraparound, gaps, and interpolation assumptions;
- rollups preserve window definition, coverage, aggregation state, provenance, and correction status;
- retention never deletes raw data before every promised correction, audit, rollup, and restore obligation permits it;
- backup and restore preserve samples, identity dictionary/indexes or rebuild rules, retention state, and replay coordinate coherently.

### Common failures

- placing request IDs, user IDs, URLs, or random values in indexed labels and creating cardinality explosions;
- trusting client clocks as a total order;
- collapsing duplicate timestamps without a documented rule;
- computing rate across a counter reset as a negative event;
- treating absent samples as zero;
- averaging precomputed averages without weighting by count or duration;
- expiring raw data before late corrections have reached rollups;
- designing one partition per series forever or one current-time range for all series;
- benchmarking sequential ingest without churn, queries, compaction, rollups, and failure;
- calling an interpolated or downsampled value an observation.

### Compact example

A counter has `(t,value)` samples `(0,100)`, `(10,130)`, `(20,5)`, `(30,25)`. The value at 20 indicates a reset. Valid positive deltas are 30 over 10 seconds and 20 over 10 seconds. Across observed intervals, total increase is 50 over 30 seconds, or about 1.667 units/s if the reset contributes no unknown increase. Treating `25-100` over 30 seconds as the rate gives a false negative result.

### Connections

The previous module, [Wide-Column Databases](094-wide-column-databases.md), supplies partition and clustering reasoning often used for time buckets. The roadmap's next module, [Graph Databases](../ROADMAP.md), changes the dominant access primitive from time range to relationship traversal. Prerequisites include [Window Functions](015-window-functions.md), [Sharding and Data Placement](086-sharding-and-data-placement.md), [Evaluating Consistency, Latency, and Availability Trade-Offs](090-evaluating-consistency-latency-and-availability-trade-offs.md), and [Columnar Analytical Databases](091-columnar-analytical-databases.md).

## Governing Question

A monitoring system receives metrics from millions of sources. An industrial historian receives corrections days late. A financial feed carries exchange timestamps and arrival sequences. A product analytics service needs recent dashboards, long-range aggregates, retention, and deletion. All contain times and values, yet they require different identity, ordering, precision, aggregation, and consistency.

What must a database guarantee so that a “latest value,” range, rate, percentile, or rollup remains meaningful under late data, duplicate timestamps, clock failure, retries, compaction, retention, and restore? The answer begins with measurement semantics and ends with operational evidence.

## Why This Matters

Time-series databases exploit a valuable workload shape: many appends, queries bounded by time and identity, age-based retention, and compressible local timestamp/value patterns. Specialized layouts can sustain high ingest, scan contiguous time ranges, and reduce storage substantially.

Specialization also creates sharp failure modes. An unbounded label dimension turns one metric family into millions of tiny series. A current-time partition becomes a write hotspot. A long-range query fans out across thousands of chunks. Late corrections leave rollups inconsistent. Counter resets appear as outages or negative traffic. Clock skew reorders causality. Deleting raw data removes the only way to recompute a faulty aggregate.

The database can faithfully store bytes while the measurement is still wrong. Therefore distinguish observed value, derived estimate, ingestion artifact, and business claim. A successful query proves neither sensor calibration nor causal interpretation.

## Prerequisites and Retrieval

Retrieve partitioning, ordered indexes, columnar compression, WAL and recovery, MVCC snapshots, replication, materialized views, window aggregation, probability summaries, and queue stability. Be able to distinguish a monotonic clock from wall time and a counter from a gauge.

Retrieve RFC 3339's Internet timestamp profile and its limits. A textual timestamp needs an offset or UTC marker, precision, and parser rules. Civil time zones and daylight-saving policy are separate from an instant. Leap seconds, clock steps, uncertainty, and source clock quality must be handled by the application/system contract.

For an engine, record exact version; sample type model; timestamp precision/range; duplicate semantics; label/field indexing; WAL and durability; block/chunk duration; compression; out-of-order window; retention and deletion; rollup/continuous aggregate behavior; compaction; replication; query consistency; backup/restore; and limits. Current behavior comes from official documentation for that version.

## Learning Objectives

After completing this module, you should be able to:

1. specify series identity, sample types, timestamp sources, duplicate rules, and time semantics;
2. calculate first-order cardinality, point volume, partition size, and query fan-out under stated assumptions;
3. design ingestion for retry, out-of-order data, gaps, corrections, and durable acknowledgement;
4. explain timestamp/value compression and where disorder or churn defeats it;
5. compute rates and rollups while handling resets, coverage, weighting, and late correction;
6. choose time/identity partitioning and diagnose hotspots, cardinality explosions, and small-series overhead;
7. design retention, downsampling, backup, and restore as one recoverable lifecycle;
8. validate semantics and performance under representative faults and workload maturity.

## Core Exposition

**Define the observation.** A sample is not just `(timestamp,value)`. Identify measurement name, subject dimensions, unit, value type, event time, source identity, source sequence, quality/calibration flags, and ingestion provenance. State whether it is a direct observation, counter, state transition, estimate, histogram, summary, or derived aggregate.

A temperature of 20 without Celsius/Kelvin, sensor calibration, location, and timestamp source is incomplete. A latency percentile without population/window and aggregation method is not safely mergeable. A “request count” that resets on restart is a cumulative counter with epochs, not an eternal total.

**Canonicalize series identity.** A series key commonly combines metric/measurement name with indexed label or tag pairs in canonical name/value order. The same logical labels in different serialization order must map to one identity. Normalize only when domain semantics allow it; lowercasing case-sensitive tenant IDs merges distinct series.

Classify attributes. Bounded dimensions such as region, status, method, and service may be suitable labels. Unbounded values such as trace ID, request ID, raw URL, timestamp, random hash, or user-generated text usually belong in non-indexed fields, exemplars, logs, or another store. “Usually” is workload guidance; prove actual bounds and query needs.

**Model cardinality and churn.** If label dimensions have possible counts $a_1,\ldots,a_n$, the theoretical cross product is $C_{max}=\prod_i a_i$, though correlations may reduce realized series. Adding `user_id` with ten million values can multiply identity metadata even when each user emits one sample.

Cardinality consumes dictionaries, postings/indexes, per-series state, cache, compaction metadata, and query planning memory. Churn can be worse than stable high cardinality because caches and index structures continually allocate cold identities. Track active, created, retired, and never-reused series over time.

**Separate clocks.** Event time may come from device, exchange, application, database coordinator, or gateway. Ingestion time comes from the accepting system; processing time belongs to a query/job. Store both when delay and clock quality matter. Never silently replace an invalid event timestamp with ingestion time; record the substitution and quality.

Wall-clock timestamps do not establish causality or uniqueness. Multiple samples can share a timestamp at finite precision, clocks can move backward, and offline devices can upload old data. Add source sequence or stable event ID when exact ordering/deduplication matters. A hybrid/logical timestamp may order writes but still differs from measured event time.

**Define duplicate semantics.** For equal series and event timestamp, an engine might reject, overwrite, choose last arrival, choose greatest sequence, merge, or retain multiple points. Each suits different domains. Sensor corrections may use greatest source revision. Trade ticks may require all events distinguished by venue sequence. Metrics scrapes may legitimately replace a retry of the same scrape identity.

Use a stable ingestion idempotency key to distinguish retry from a new observation. “Last write wins” based on arrival can make replay order change history. If replacement is allowed, preserve correction provenance or audit as required.

**Bound out-of-order acceptance.** Let frontier $F_s$ be the greatest accepted event time for series or partition and sample time be $t$. Lateness can be $\ell=F_s-t$ when $t<F_s$. An out-of-order window $W$ accepts or optimizes samples with $\ell\le W$; data beyond it may reject, enter a repair path, or create expensive old-chunk rewrites.

The choice of frontier scope matters. A global frontier lets one future-skewed source make every normal sample “late.” Per-series frontiers cost state but localize skew. Watermarks are claims about future arrival, not measurements of current wall time; define how they advance and recover after idle sources.

**Write durably before buffering claims.** Ingestion may batch samples into WAL segments and mutable head blocks, then seal immutable chunks. Acknowledgement must name persistence, replication, and duplicate behavior. Group commit trades sync amortization for queue delay. Backpressure protects bounded memory and compaction queues.

A batch may contain several series and timestamps. State whether it is all-or-nothing, partially accepted with per-sample results, or retryable by identity. Unknown outcomes require status lookup or idempotent replay.

**Partition by time and identity.** Pure time partitioning groups all current writes and can hotspot one range or chunk. Pure series partitioning spreads identities but lets one series grow forever and makes retention/old repair granular. A composite maps series hash/range plus time bucket, bounding chunks while distributing current writes.

Bucket duration trades metadata and query fan-out against partition size and rewrite. For rate $f$, duration $w$, and average encoded live sample bytes $b$, one series bucket has approximately $fw$ points and $fwb$ bytes. Multiple series per shard and burst/skew must be added. Choose from peak, not mean, and include out-of-order reopening.

**Store by query order.** Samples for one series and time interval benefit from timestamp order. Blocks can encode a base timestamp plus deltas; regular intervals make deltas repetitive. Values may use integer delta, run-length, dictionary, bit packing, floating-point XOR, or domain-specific codecs. Indexes route series and time ranges to blocks.

Facebook's Gorilla paper describes delta-of-delta timestamp compression and XOR-based floating-value compression for a monitoring workload. It is a concrete design, not a universal bound. Irregular timestamps, noisy floating bits, disorder, and mixed types reduce compression. Measure decoded CPU and query selectivity as well as bytes.

**Make block metadata safe.** Time bounds, series bounds, counts, null/quality flags, min/max, checksums, compression type, and format version guide pruning and decoding. Pruning may create false-positive reads but must not omit matching samples. A corrupted bound cannot be trusted as an optimization; fail, repair, or fall back according to the integrity contract.

**Distinguish raw and rollup truth.** A rollup over window $I$ should carry at least window boundaries, function, count, sum or mergeable state, min/max as applicable, quality/coverage, source frontier, version, and correction status. Store `sum` and `count` to combine averages: global mean is $\sum_j sum_j/\sum_j count_j$, not the unweighted mean of window means.

Percentiles are not composable from percentile values. Merge a defined sketch/histogram with known error/scale semantics or recompute from raw data. Minimum and maximum compose but do not reveal missing coverage. Distinct counts need set or mergeable estimator semantics.

**Define window boundaries.** State time basis, interval closure, alignment origin, time zone, and daylight-saving behavior. UTC fixed-duration windows avoid variable civil-hour length; business-day windows require zone/version policy. A sample on the boundary must enter exactly one tumbling window.

Sliding windows overlap, so one sample may contribute to several outputs. Session windows depend on gap rules and can change when late data bridges sessions. Rollups must version these definitions.

**Handle late correction through the lifecycle.** If raw sample changes after its rollup was emitted, either update/retract the rollup, mark it provisional until a watermark, or refuse changes beyond a documented horizon. Downstream consumers need stable rollup identity and version so replay does not double count.

Do not delete raw data until every promised rollup is complete and verified, the correction horizon closes, audits permit it, backups meet policy, and rollback is no longer needed. If raw data is intentionally gone, document which aggregate errors can no longer be repaired.

**Interpret gauges and counters separately.** A gauge can rise or fall; interpolation may be linear, step, last-known, or forbidden. A cumulative counter should generally be nondecreasing within an epoch but resets or wraps. Rate uses positive increments over elapsed time, excluding or specially treating resets according to semantics.

For samples $(t_i,x_i)$, a simplified counter increase is $\Delta_i=x_i-x_{i-1}$ when nonnegative; if negative, mark reset and use $x_i$ as post-reset increase only when the reset model justifies it. Divide an explicitly accumulated increase by an explicitly chosen elapsed/observed duration. Gaps and resets introduce uncertainty that must be surfaced.

**Do not turn missing into zero.** Absence can mean no event, failed scrape, offline sensor, lost transport, retention, query gap, or true zero not emitted. Carry presence and quality. Interpolation creates estimates, so mark method and maximum gap. Alerting should distinguish “zero traffic” from “no observations.”

**Design query execution.** Exact series plus bounded time range should route to a small block set. Label predicates use postings or metadata indexes to select series, then time bounds select blocks. Grouping across millions of series can exhaust memory even if each range is short. Push predicates and partial aggregation while preserving exact semantics.

Long queries compete with ingest, compaction, rollups, and caches. Apply range/cardinality/result limits, admission control, cancellation, spill, and tenant quotas. Record examined series/blocks/points versus returned values; a fast cache hit and a cold month scan are different workloads.

**Control high-cardinality queries.** Regex or negative label matchers can enumerate most series. Group-by on user or path can materialize huge state. Predeclare safe dimensions, use query cost estimation, and require narrower time/tenant bounds. Do not rely only on response-size limits because aggregation can consume resources before output.

**Use retention as state transition.** Logical expiry may hide data before physical files are removed. Dropping whole time chunks is efficient when all contents share retention and no late corrections or legal holds remain. Mixed-retention data in one block requires filtering or rewrite. Retention policy changes can expose or remove data unexpectedly if not versioned.

Legal hold, tenant deletion, and privacy erasure may conflict with shared compressed blocks and backups. State logical visibility, physical reclamation, cryptographic erasure, and backup expiry separately. Indexes, rollups, caches, replicas, and exports join the deletion surface.

**Separate database consistency from measurement truth.** A linearizable latest read can return the most recently committed faulty sensor value. An eventually consistent replica can lag a correct value. Record consistency, freshness, source quality, and correction status independently.

Distributed stores partition series/time, replicate blocks, and route aggregations. Define read snapshot across shards, partial-response behavior, deduplication during replica overlap, and leader/follower lag. A global query may mix shard times unless a snapshot/barrier protocol says otherwise.

**Manage compaction and mutable windows.** Immutable blocks improve compression and scans. Late samples, deletes, and corrections create overlays or require rewrites. Compact by time/series while preserving duplicate/version rules. Too aggressive sealing magnifies tiny-block overhead; too-long mutable heads increase memory and recovery.

Observe head-block age/bytes, WAL, sealed block count/size, overlap, late overlays, compaction debt, reopened windows, and free space. A policy that performs well for in-order metrics may fail for intermittently connected devices.

**Plan disaster recovery.** A coherent backup includes raw blocks, mutable/WAL state at a declared boundary, series dictionaries and indexes or rebuild rules, schema/metric metadata, rollup definitions/state, retention/legal holds, tenancy/security, encryption keys, and replay coordinates. Restore exact timestamp precision and identity canonicalization.

Verify raw keyed samples, duplicates/corrections, block checksums, label queries, rates, rollups, retention, and change continuity. Restore a point before a late correction and prove replay updates both raw and derived state idempotently.

**Observe what drives cost.** Collect samples and bytes accepted/rejected/deduplicated; event-to-ingest delay; out-of-order distribution; active/new/retired series; label-value cardinality; points/bytes per block; WAL/sync; compression ratio and decode CPU; index/postings memory; query series/blocks/points examined; cache; rollup lag/corrections; retention backlog; compaction; replication; and backup/restore results.

Slice by tenant, measurement, label key, shard, time bucket, source version, and query class. Avoid exporting raw high-cardinality labels into the monitoring system that is already failing from high cardinality.

**Benchmark mature mixed load.** Generate realistic cardinality, churn, skew, timestamp jitter, duplicate retry, out-of-order distribution, value compressibility, label predicates, ranges, group-bys, rollups, retention, and corrections. Run through cache turnover, block sealing, compaction, retention, and repair—not only the initial empty-store ingest phase.

Inject clock jumps/future timestamps, node loss, delayed replicas, WAL truncation, corrupt blocks, full disk, query storms, rollup restart, backup interruption, and restore. Use a finite reference model to compare ordered samples and derived aggregates. Passed runs are bounded evidence.

The executable fixture below computes a finite observed-positive-increase rate with one reset. It treats increase during the reset interval as unknown, excludes the first post-reset value, and uses the entire 30-second wall interval as its declared denominator. It is not a clock validator, query engine, gap estimator, storage codec, or production rate function.

<!-- bijux-verify: {"id":"finite-counter-rate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"positive_increase=50\nresets=1\nelapsed_seconds=30\nrate_per_second=1.667\nnaive_delta=-75\nnaive_rate_invalid=true\nevidence=finite_counter_rate\n","stderr":""}} -->
```python
samples = [(0, 100), (10, 130), (20, 5), (30, 25)]
increase = 0
resets = 0
for (_, previous), (_, current) in zip(samples, samples[1:]):
    delta = current - previous
    if delta >= 0:
        increase += delta
    else:
        resets += 1

elapsed = samples[-1][0] - samples[0][0]
naive_delta = samples[-1][1] - samples[0][1]
print(f"positive_increase={increase}")
print(f"resets={resets}")
print(f"elapsed_seconds={elapsed}")
print(f"rate_per_second={increase / elapsed:.3f}")
print(f"naive_delta={naive_delta}")
print(f"naive_rate_invalid={str(resets > 0).lower()}")
print("evidence=finite_counter_rate")
```

## Definitions and Notation

- $s$ is a canonical series key; $t$ is event time; $q$ is a source sequence/revision; $x$ is a value; $m$ is quality/provenance metadata.
- **Event time**, **ingestion time**, and **processing time** identify different clocks and stages.
- **Cardinality** $C$ is distinct series count; **churn** is identity creation/retirement rate.
- $f$ is samples per second per series, $H$ retention seconds, and $P=CfH$ an idealized point count.
- $F_s$ is a series/partition event-time frontier; $\ell=F_s-t$ is lateness for a behind-frontier sample; $W$ is an acceptance/optimization window.
- $w$ is time-bucket duration and $b$ is average encoded live bytes per sample in a simplified capacity model.
- A **duplicate** shares the database's identity coordinate; a **retry** repeats one intended ingestion; a **correction** intentionally changes an earlier observation.
- A **watermark** is a protocol claim about future event-time arrivals, not current wall time.
- A **chunk/block/segment** is a bounded physical group of samples and metadata.
- A **rollup** is a materialized time-window aggregate with coverage, provenance, and version.
- A **gauge** measures a level; a **counter** accumulates within reset epochs.
- **Coverage** records which expected interval/population contributes to a derived result.
- **Retention** governs availability; **reclamation** removes physical representations after safety conditions.
- **Series fan-out** is the number of identities selected; **chunk fan-out** is the number of time/storage units touched.

## Mechanisms, Invariants, or Proof Structure

**Identity invariant.** Canonicalization maps equivalent allowed label sets to one series key and distinct domain identities to different keys. Writers, indexes, queries, replay, and restore use the same versioned rule. Unbounded label values are rejected or routed outside indexed identity before allocation.

**Ordered visibility.** For sample coordinate $(s,t)$, duplicate/correction policy selects a deterministic version using $q$ or declared rule. A snapshot range merges mutable, immutable, late-overlay, and replica candidates, deduplicates by coordinate/version, and sorts by event-time/tie-breaker. Pruning bounds have no false negatives. Omitting any component can silently lose late data.

**Point-count derivation.** Under $C$ stable series, constant frequency $f$, complete emission, and retention $H$, each series emits $fH$ points and total $P=CfH$. Real capacity must model churn, gaps, bursts, encoding, index, WAL, replication, compaction, rollups, and retention lag. The expression is a baseline, not a bound without peak assumptions.

**Weighted-rollup invariant.** If disjoint windows carry exact sums $S_j$ and counts $N_j$, their combined mean is $\sum_jS_j/\sum_jN_j$ when total count is positive. Averaging means $S_j/N_j$ is correct only under equal effective counts or explicit weighting. Coverage and units must also agree.

**Counter-rate premise.** Within one non-wrapping epoch, counter difference equals accumulated events represented between samples. Negative difference signals reset/wrap/correction unless the type permits decline. Combining epochs requires a declared reset contribution and time denominator; otherwise report unknown rather than inventing rate.

**Rollup convergence.** Raw mutation carries stable identity/version. Rollup recomputation or reversible delta applies idempotently, and downstream output carries rollup version. Complete late/correction replay plus reconciliation converges after the correction horizon. Deleting raw inputs before verification removes the recovery proof.

**Retention safety.** Raw data can be reclaimed only when no supported query, late correction, rollup rebuild, audit, legal hold, backup/restore, or rollback requires it. Hiding it from ordinary reads is not this proof. Every derivative and replica participates in the deletion claim.

## Alternatives and Trade-Offs

**Specialized time-series versus general database.** Specialized engines can optimize append, time pruning, compression, and retention. Relational, columnar, wide-column, or object-table systems may better support joins, transactions, or shared governance. Compare exact workload and lifecycle.

**Labels versus fields.** Labels accelerate identity filtering and grouping at cardinality cost. Fields hold rich values but may require scans or secondary indexes. Promote only bounded, frequently queried dimensions and measure churn.

**Long versus short chunks.** Long chunks improve sequential compression and reduce metadata but increase rewrite, hotspot, and long-range contention. Short chunks isolate late updates and retention but amplify metadata and fan-out. Hybrid sizing can adapt by workload.

**Raw versus rollup retention.** Raw supports correction and new analyses at storage cost. Rollup reduces cost but freezes aggregation choices and error. Tiering raw to colder storage can preserve repair with higher latency and operational complexity.

**Overwrite versus multi-version duplicates.** Overwrite simplifies latest state but loses audit and makes replay order important. Multi-version retains truth but expands query/deduplication. Stable source revisions enable deterministic compaction.

**Exact versus approximate aggregate.** Exact results require raw or exact mergeable state and more resources. Sketches bound memory and merge cost but introduce defined error and compatibility requirements. Never relabel an estimate as exact.

**Ingestion-time versus event-time windows.** Ingestion time is operationally available and ordered by acceptance but misplaces delayed events. Event time matches domain occurrence but requires disorder/correction policy. Store both when either question matters.

**Synchronous versus asynchronous rollup.** Synchronous maintenance improves immediate consistency but increases ingest latency and coupling. Asynchronous rollup allows scale and replay but exposes staleness. Version, watermark, and correction state make either honest.

## Failure Modes and Misconceptions

- **“A timestamp makes data time series.”** Identity, order, value type, window, retention, and workload define the model.
- **“Labels are just metadata.”** Indexed label combinations allocate series and can dominate cost.
- **“One million samples is one series.”** Cardinality and point count are independent dimensions.
- **“Client time orders events.”** Clocks collide, skew, pause, and move backward.
- **“Duplicate timestamp means retry.”** It may be collision, correction, or distinct event lacking a tie-breaker.
- **“Missing means zero.”** It can mean loss, outage, silence, expiry, or unknown.
- **“Counter difference always gives rate.”** Resets, wrap, gaps, correction, and denominator matter.
- **“Averages can be averaged.”** Only with correct weighting and compatible windows/populations.
- **“Percentiles are mergeable numbers.”** Percentile values alone do not contain distribution state.
- **“Compression ratio predicts query latency.”** Decode CPU, pruning, cache, fan-out, and aggregation dominate differently.
- **“TTL removes bytes immediately.”** Logical expiry precedes compaction/reclamation.
- **“Downsampling preserves the data.”** It preserves only declared aggregate state and coverage.
- **“Late data is only an ingestion issue.”** It affects chunks, rollups, alerts, retention, and downstream consumers.
- **“Current-time partitioning distributes writes.”** It may concentrate every producer in one range.
- **“Successful restore proves correct metrics.”** Identity, duplicates, rates, rollups, and replay continuity need semantic checks.

## Worked Examples

### Example 1

**Situation.** Metric `http_requests` has 8 services, 5 regions, 6 methods, 12 statuses, and an added `user_id` dimension with 2 million values.

The unconstrained cross product without user is $8\times5\times6\times12=2{,}880$ potential series. Adding user makes 5.76 billion potential combinations. Correlation reduces realized count, but even one series per active user-service pair can overwhelm identity metadata. Keep user in logs/traces or a separately bounded analytics model.

**Conclusion.** One unbounded label can dominate every bounded dimension.

### Example 2

**Situation.** 250,000 stable series emit every 15 seconds and retain 30 days. Estimate ideal points.

$f=1/15$, $H=30\times86{,}400=2{,}592{,}000$ seconds. Each series emits 172,800 points, so $P=43.2$ billion points. Physical bytes require measured encoding, labels/index, WAL, replication, compaction, rollups, and headroom.

**Conclusion.** First-order point count is necessary but far from physical capacity.

### Example 3

**Situation.** Device A's frontier is 12:10. It uploads points at 12:09, 12:03, and a clock-skewed 18:00. The allowed lateness is ten minutes.

The first is one minute late and the second seven minutes late, both within the current window. Accepting the future-skewed point as the new frontier would make subsequent normal data hours late. Validate plausible future skew or quarantine it; use a per-device frontier and quality flag.

**Conclusion.** Frontier scope and future-timestamp validation are part of disorder correctness.

### Example 4

**Situation.** Two trade events share millisecond timestamp 1000 but have venue sequences 81 and 82.

If identity is only `(symbol,time)`, one may overwrite. Use `(symbol,time,venue_sequence)` or stable event ID, preserving both and deterministic order. A retry repeats the same event identity; a correction carries a revision linked to that identity.

**Conclusion.** Timestamp precision rarely supplies unique event identity.

### Example 5

**Situation.** Window A has mean 10 from 100 samples; window B has mean 30 from 10 samples.

Unweighted mean is 20 and is wrong for all samples. Recover sums: 1,000 and 300. Combined mean is $1{,}300/110\approx11.818$. Coverage and units must still agree.

**Conclusion.** Rollups need mergeable state, not display statistics alone.

### Example 6

**Situation.** Counter samples are 100, 130, 5, and 25 at ten-second intervals.

Known nonnegative increments are 30 before reset and 20 afterward, totaling 50. Treating the first post-reset value 5 as events since reset would yield 55, but the reset time within the interval is unknown. The executable fixture excludes it and reports an observed-positive-increase rate of $50/30\approx1.667$/s over wall time, with one reset flagged. A different policy must label its assumption.

**Conclusion.** Reset handling changes the numerator and must be declared rather than hidden.

### Example 7

**Situation.** A dashboard has no sample for one host during five minutes. Filling zero triggers a “service idle” conclusion.

The absence could be scraper failure or network partition. Carry a presence/quality series and evaluate staleness. A step-held estimate may be acceptable for configuration state but not necessarily resource use. Alert separately on missing observations.

**Conclusion.** Imputation is a model with uncertainty, not recovered observation.

### Example 8

**Situation.** Raw data retains seven days; a daily rollup is considered final after ten days because devices may reconnect late.

The database deletes the raw point three days before the correction horizon closes. A day-eight correction cannot rebuild the daily aggregate. Increase raw/cold retention beyond finalization and verification, or shorten the accepted correction promise explicitly. Mark rollups provisional until closure.

**Conclusion.** Raw retention must dominate promised correction and rollup recovery horizons.

### Example 9

**Situation.** A query selects 500,000 series for one hour, returning one aggregate each. Response size is modest.

The engine may still open postings, touch blocks, decode points, and hold 500,000 group states. Bound series fan-out and examined points, estimate before execution, push partial aggregation, spill safely, and apply tenant admission control. Output rows alone are not cost.

**Conclusion.** Time-series query cost has identity and block fan-out dimensions hidden by compact results.

### Example 10

**Situation.** A restored store has equal total sample count but a different canonical label ordering and rollup frontier.

Equivalent labels may split into duplicate series, while replay can skip or double-apply aggregates. Compare canonical series identities, keyed sample coordinates and revisions, duplicate policy, raw hashes, rollup sums/counts/coverage/version, retention state, and exact replay coordinate before serving.

**Conclusion.** Count equality cannot prove a semantically coherent time-series restore.

## Cross-Program Connections

[Data Engineering](../../19-data-engineering/ROADMAP.md) connects event time, watermarks, late data, windows, replay, and materialized state. A database must expose enough version and correction semantics for those pipelines.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) contributes clocks, causality, replication, partial failure, partitioning, and snapshot reasoning. Timestamp storage alone does not solve distributed time.

[Algorithms Engineering](../../16-algorithm-engineering/ROADMAP.md) connects compression, sketches, selection, merge, range search, and cost analysis. Time-series codecs and approximate rollups depend on their premises.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects telemetry validity, queues, overload, fault injection, capacity, and recovery. The monitoring database itself must remain observable without recursively exploding cardinality.

[Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) connects authoritative observations, semantic units, retention, tiering, governance, and serving models. Raw and rollup layers have distinct ownership.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects tenant labels, sensitive telemetry, query isolation, encryption, audit, deletion, and backup. Metadata may reveal identities even when values are encrypted.

## References

- Tuomas Pelkonen et al., [Gorilla: A Fast, Scalable, In-Memory Time Series Database](https://www.vldb.org/pvldb/vol8/p1816-teller.pdf), PVLDB 8(12), 2015. Primary source for a monitoring workload, sharding, delta-of-delta timestamps, and XOR value compression.
- Michael P. Andersen and David E. Culler, [BTrDB: Optimizing Storage System Design for Timeseries Processing](https://www.usenix.org/conference/fast16/technical-sessions/presentation/andersen), FAST 2016. Primary source for versioned time-series storage and tree-based aggregation.
- Graham Klyne and Chris Newman, [RFC 3339: Date and Time on the Internet: Timestamps](https://www.rfc-editor.org/rfc/rfc3339), July 2002. Timestamp representation, offset, precision, and interoperability constraints.
- Prometheus Authors, [Storage](https://prometheus.io/docs/prometheus/latest/storage/), current Prometheus documentation checked 2026-09-05. Concrete WAL, block, retention, and local-storage behavior.
- Prometheus Authors, [Metric types](https://prometheus.io/docs/concepts/metric_types/), current documentation checked 2026-09-05. Counter, gauge, histogram, and summary semantics in a prominent monitoring model.
- InfluxData, [Schema design](https://docs.influxdata.com/influxdb3/core/write-data/best-practices/schema-design/), current InfluxDB 3 Core documentation checked 2026-09-05. Concrete tag/field, schema, and high-cardinality guidance.
- Tiger Data, [Understand hypertables and chunks](https://docs.timescale.com/use-timescale/latest/hypertables/), current documentation checked 2026-09-05. Concrete time partitioning and chunk concepts in TimescaleDB.
- OpenTelemetry Authors, [Metrics Data Model](https://opentelemetry.io/docs/specs/otel/metrics/data-model/), current specification checked 2026-09-05. Metric streams, temporality, aggregation, identity, and data-point model.
- Colin Adams et al., [Monarch: Google's Planet-Scale In-Memory Time Series Database](https://research.google/pubs/monarch-googles-planet-scale-in-memory-time-series-database/), PVLDB 13(12), 2020. Primary source for a large distributed monitoring architecture and query system.
- Prometheus Authors, [Querying basics](https://prometheus.io/docs/prometheus/latest/querying/basics/), current Prometheus documentation checked 2026-09-05. Concrete selectors, range vectors, timestamps, lookback, and staleness behavior in a monitoring query model.

## Exercises

### Exercise 1

Define series key, cardinality, churn, event time, ingestion time, duplicate, correction, watermark, rollup, counter, and gauge. Explain why sample count alone cannot size a system.

### Exercise 2

There are 800,000 stable series sampled every 30 seconds for 180 days. Derive ideal point count. If compressed point payload averages 2.5 bytes, compute payload bytes, then name at least eight excluded costs.

### Exercise 3

A counter has samples `(0,900)`, `(20,960)`, `(50,40)`, `(80,100)` and a known reset between 20 and 50. Compute a rate under two explicit reset assumptions, state uncertainty, and design the stored metadata needed for a stronger answer.

### Exercise 4

Design raw and rollup storage for ten million intermittently connected meters: five-minute normal sampling, seven-day late arrivals, monthly billing, regulatory raw retention for one year, and interactive five-year trend queries. Address identity, partitioning, correction, cardinality, rollup, and restore.

### Exercise 5

A telemetry platform is failing from label cardinality and query storms while its own monitoring exports tenant IDs and query strings as labels. Design a safe migration that preserves diagnostic value, prevents ingestion/replay loss, and validates cost and semantic correctness.

## Answers to the Exercises

### Answer 1

A **series key** is canonical measurement plus identity dimensions. **Cardinality** is distinct keys; **churn** is key creation/retirement rate. **Event time** describes occurrence; **ingestion time** describes acceptance. A **duplicate** shares the model's sample coordinate; a **correction** deliberately revises an earlier observation. A **watermark** claims a bound on future late arrivals. A **rollup** is versioned window aggregate state. A **counter** accumulates within reset epochs; a **gauge** measures a level. Equal sample count can have radically different identity metadata, churn, labels, compression, timestamp disorder, indexes, WAL, replication, compaction, rollups, retention lag, query fan-out, and recovery cost.

### Answer 2

Retention is $180\times86{,}400=15{,}552{,}000$ seconds. At one sample per 30 seconds, each series has 518,400 points. Across 800,000 series, $P=414{,}720{,}000{,}000$ points. At 2.5 payload bytes, that is 1,036,800,000,000 bytes, about 1.037 TB decimal. Excluded costs include series/label dictionaries, timestamps if not included, block headers/checksums, postings/indexes, WAL, replication, compaction overlap, mutable heads, caches, tombstones, late overlays, rollups, backup, filesystem allocation, encryption, and operational free-space headroom.

### Answer 3

Before reset, increase is 60. After reset, from 40 to 100 adds 60. If the first post-reset value 40 represents events accumulated since reset and is included, total known/assumed increase is 160 over 80 seconds, or 2.0/s. If events between last pre-reset sample and the first post-reset sample are unknown and the 40 is excluded, observed within-epoch increase is 120 over 80 wall seconds, or 1.5/s, but coverage is incomplete. A stronger record stores counter epoch/boot ID, source monotonic sequence, exact reset event/time or bounds, sample quality, ingestion time, expected cadence, and gap markers. The result should carry numerator, denominator, coverage, reset count, and assumption.

### Answer 4

Use stable meter identity with bounded model/region dimensions; keep customer or request IDs out of unbounded labels unless required and governed. Partition raw by hash(meter) plus bounded time chunk sized from peak uploads, including seven-day reopening. Store event and ingestion time, source sequence, quality, and correction revision. Monthly billing consumes versioned raw data only after the late horizon and reconciliation; preserve exact sum/count and source frontier, with correction/rebill workflow. Retain raw one year in queryable or cold verifiable form, including legal holds and backups. Build daily/monthly mergeable rollups with coverage for five-year trends, never unweighted averages. Restore must recover raw/chunks, identities, rollup definitions/state, billing versions, retention, and replay coordinates; replay corrections idempotently and compare billed/rollup outputs before service.

### Answer 5

First cap new damage with tenant quotas, query admission/cancellation, label allowlists, and rejection metrics that do not repeat raw labels. Replace tenant-ID labels in platform self-metrics with bounded tier/region plus a pseudonymous heavy-hitter channel or sampled secured logs; normalize query text to bounded query fingerprints/templates. Deploy dual observation temporarily, quantify active/new series, index memory, ingestion bytes, query fan-out, cache, and diagnostic tasks served. Update alerts/dashboards and preserve a mapping under restricted retention where investigations require it. Backfill/replay only if identity semantics and retention justify it; otherwise begin a new metric version and keep old data read-only until expiry. Validate counts/rates/alerts under a fixed interval, induce query storms, verify no ingestion gaps, and ensure the replacement monitoring path remains available during failure. Remove old labels after consumers and rollback checks pass.
