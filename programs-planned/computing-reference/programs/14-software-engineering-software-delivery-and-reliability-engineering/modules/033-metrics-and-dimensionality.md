---
module_id: SDRE-033
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 33
title: Metrics and Dimensionality
status: complete
last_verified: 2026-09-06
---

# Metrics and Dimensionality

## One-Page Review

### Governing question

How can engineers design metric streams whose numbers retain correct meaning across time, aggregation, restarts, dimensions, and scale while remaining affordable enough to monitor continuously?

### Essential definitions

- a **measurement** is a numeric observation made under a stated procedure;
- a **metric stream** is a sequence of points with one name, resource and scope identity, type, unit, temporality, and attribute set;
- a **dimension** or **label** is an attribute used to partition a metric into distinct streams;
- **cardinality** is the number of distinct attribute sets, and therefore streams, materialized for a metric under a given identity scope;
- a **counter** is a sum whose intended value is monotonic between resets;
- a **gauge** reports a current or most recently observed value without inherent additive semantics;
- a **histogram** compresses a population into count, sum, and bucket counts, optionally with minimum, maximum, and exemplars;
- **temporality** says whether a point covers an interval delta or accumulation since a start time;
- a **reset** begins a new cumulative sequence and is not a negative event count;
- **staleness** means the last point no longer represents current knowledge;
- an **exemplar** links an individual observation and context to an aggregate;
- **aggregation** combines streams or time intervals only when their units, meanings, and population weights permit it;
- a **quantile** is a population value at a rank; a histogram usually bounds rather than recovers it exactly;
- **ratio of sums** weights component ratios by their denominators; a mean of ratios weights components equally.

### Central model, mechanism, or theorem

Identify a stream by

$$
K=(\rho,\sigma,n,\tau,u,\theta,a),
$$

where $\rho$ is resource, $\sigma$ instrumentation scope, $n$ name, $\tau$ point type, $u$ unit, $\theta$ temporality/intrinsic properties, and $a$ the complete attribute set. Changing any identifying semantic creates a different stream even if a dashboard aliases it.

For bounded label domains $D_1,\ldots,D_k$, the Cartesian upper bound on streams is

$$
S_{max}=\prod_{i=1}^{k}|D_i|.
$$

Actual cardinality is the number of combinations that occur, but an unbounded domain such as user, request, or raw URL makes the upper bound operationally unsafe.

For component successes $s_i$ and totals $t_i>0$, aggregate success is

$$
R=\frac{\sum_i s_i}{\sum_i t_i},
$$

not generally the unweighted mean $\frac{1}{m}\sum_i s_i/t_i$.

### Critical invariants

- every stream has one stable name, type, unit, population, temporality, and attribute schema;
- counter rates account for start time, reset, gaps, and overlap before differencing;
- gauges are aggregated only with a domain rule such as sum, maximum, or weighted average;
- numerator and denominator share the same population and dimensions before division;
- histograms expose bucket error and merge only compatible boundaries and semantics;
- missing, stale, delayed, and explicitly zero values remain distinguishable;
- dimensions are bounded, necessary for a query, and safe for privacy and cost;
- aggregation order is justified; averages of averages require weights;
- resource and release identity remain available for diagnosis without uncontrolled fan-out;
- recording, export, storage, query, and alert costs are measured as part of instrumentation.

### Common failures

Failures include putting request or user IDs in labels, encoding dimensions in metric names, summing temperatures or queue ages without meaning, treating cumulative counters as gauges, interpreting reset as negative work, dividing mismatched populations, averaging percentages without weights, using mean latency for tail-sensitive service, choosing buckets after the incident, summing incompatible histograms, treating absent data as zero, keeping stale gauges forever, emitting overlapping writers for one stream, changing units in place, and optimizing storage by dropping the dimension needed to detect a harmed cohort.

### Compact example

A request metric uses stable name `checkout.requests`, monotonic cumulative sum semantics, unit `{request}`, and bounded attributes `operation`, `outcome`, `region`, and `release`. It excludes raw path, trace ID, account, and exception message. Start time identifies resets. A latency histogram uses seconds and policy-aligned boundaries, retaining count and sum plus exemplars to sampled traces. The dashboard calculates global success as ratio of summed success and total counts, shows per-region and per-release distributions, marks stale series unavailable, and measures active series, ingest bytes, dropped points, and query cost.

### Connections

[SDRE-032](032-structured-logging.md) preserves individual event detail and schema. [SDRE-034](../ROADMAP.md) next connects individual operations through distributed tracing. Data Engineering owns streaming transformations; Database Engineering owns time-series storage and query mechanisms.

## Governing Question

A metric is not just a number with a name. `latency=12` lacks unit, operation, population, aggregation, timestamp, and distribution. `requests=1000` might be a cumulative process counter, an interval delta, an estimate, or a stale last value. Adding labels may recover meaning but can create millions of time series and expose sensitive identifiers.

Metrics deliberately discard individual detail to make continuous reasoning affordable. Good design decides what may be aggregated, which distinctions must survive, how state changes over time, and what error the compression introduces. It also ensures that missing evidence, process resets, duplicated writers, and schema changes cannot masquerade as business behavior.

The governing question is therefore two-sided: which numeric model supports the decision, and can the system afford that model at fleet scale? Correctness without sustainable cost will be disabled during an incident; low cost without meaningful dimensions will confidently hide the incident.

## Why This Matters

Metrics drive pages, release gates, autoscaling, capacity plans, SLOs, billing checks, and executive reports. A semantic mistake can automate harm: an average can approve a release whose tail is broken, a reset can trigger a false negative rate, or a label explosion can overload the telemetry system precisely when failures create novel values.

The current OpenTelemetry metrics data model describes metric streams through resource, instrumentation scope, name, point type, unit, intrinsic properties, attributes, time, and temporality. Its stable model covers monotonic sums, gauges, explicit and exponential histograms, exemplars, resets, gaps, and semantics-preserving transformations [1]. Those mechanisms do not choose an application's population, useful labels, or acceptable error.

OpenMetrics 1.0 supplies a durable exposition model for metric families, label sets, counters, gauges, histograms, and related metadata [2]. Current Prometheus instrumentation and naming guidance recommends dimensions rather than proliferating names, while warning against high-cardinality or unbounded values such as user identifiers [3, 4]. Its numerical cardinality guidance is ecosystem practice, not a universal capacity law; actual limits depend on workload and implementation.

Google SRE's monitoring guidance proposes latency, traffic, errors, and saturation as a compact starting set for user-facing systems and explicitly separates successful and failed latency [5]. Dean and Barroso show why rare latency variability matters at large scale [6]. These sources motivate population and tail reasoning rather than prescribing one dashboard.

At storage scale, Monarch demonstrates a production design for a globally distributed in-memory time-series database and documents the indexing, query, availability, and scale concerns created by large metric workloads [7]. The architecture is evidence that dimensional telemetry is a data system, not a recommendation to copy one vendor's implementation.

Jain's performance-analysis text provides a durable calibration for choosing metrics, characterizing workloads, summarizing measurements, comparing systems, and avoiding ratio and presentation errors [8]. Tooling has changed since 1991; populations, measurement procedures, and valid aggregation remain foundational.

## Prerequisites and Retrieval

Retrieve measurement, unit, time series, attribute, set, Cartesian product, counter, gauge, histogram, bucket, distribution, mean, quantile, rate, derivative, reset, interval, cumulative, delta, sample, bias, SLI, SLO, staleness, resource, release, and exemplar.

From SDRE-031 retrieve operational questions, evidence completeness, black-box/white-box boundaries, and hypothesis distinction. From SDRE-032 retrieve typed schemas, resource identity, event versus observed time, loss, duplicates, and transformation provenance. Metrics compress events; compression must declare what it preserves.

## Learning Objectives

After completing this module, you should be able to:

1. identify a metric stream by its complete semantic key;
2. choose counters, gauges, histograms, or event logs from the question;
3. derive rates from cumulative or delta sums while handling resets and gaps;
4. distinguish point time, interval, start time, freshness, zero, and absence;
5. calculate cardinality bounds and reject unsafe label domains;
6. aggregate ratios, gauges, and distributions with valid weights and semantics;
7. choose histogram boundaries and state quantile error;
8. design resource, operation, outcome, region, release, and cohort dimensions;
9. test overlapping writers, schema drift, sampling, and telemetry overload;
10. govern metric cost, ownership, retirement, and diagnostic value.

## Core Exposition

**Start with a measurement procedure.** Define what occurrence or state changes the value, where it is observed, which clock applies, and what population it represents. A request counter at a client, gateway, application, and database measures different boundaries. The same name cannot erase those vantage points.

Specify name, description, unit, point type, monotonicity, temporality, resource, scope, attribute schema, owner, expected range, and consumer. A unit is part of meaning. Changing milliseconds to seconds under the same stream identity silently breaks thresholds by a factor of one thousand.

Use a stable domain noun and operation rather than embedding every dimension in names. `http.responses.500.us_east` creates schema through string parsing. A stable request metric with bounded status class and region attributes supports aggregation, validation, and migration. Not every possible distinction belongs in a metric.

**Understand stream identity.** A time series is determined by its identifying metadata and full label set. Adding `release=abc` does not add one field to an existing stream; it partitions observations into separate streams. Removing it later merges populations only if the values are aggregable and no query needs the distinction.

Resource attributes also multiply effective series. Ten instance streams with the same metric labels are ten streams before query aggregation. Instrumentation scope and unit conflicts can prevent safe merge. Inventory the whole stream key rather than counting label values inside application code alone.

The Cartesian product gives an upper bound, not a forecast. Five labels with 10 values each allow $10^5=100{,}000$ combinations. Correlations and sparse traffic may materialize fewer. A single unbounded label makes future risk open-ended and can create a new stream on every request.

Estimate active series, creation rate, churn, samples per second, bytes per sample, retention, index overhead, query fan-out, and alert evaluation. Cardinality churn can be harmful even when concurrent count seems bounded because indexes and caches see continual new identities.

**Use counters for occurrences and accumulated work.** A monotonic counter records a nonnegative increment for requests, bytes, retries, or failures. Its absolute cumulative value is usually less useful than change over a window. If $C(t_2)\ge C(t_1)$ within one unbroken sequence, average rate is $(C(t_2)-C(t_1))/(t_2-t_1)$.

A process restart resets its local counter. Start time or reset detection begins a new sequence; subtracting across the reset yields a false negative count. A missing scrape creates a longer rate interval, not necessarily zero activity. Overlapping writers for one declared stream can produce decreases, spikes, or double counts and violate single-writer reasoning.

Delta sums report change for explicit nonoverlapping intervals. They simplify some stateless aggregation and sampling designs but require reliable interval coverage. Cumulative sums make intermittent collection easier to reconcile but retain state proportional to stream cardinality. Translation must preserve start and end times.

Never decrement a monotonic total to represent cancellation. Record started and completed/cancelled outcomes separately or use a current-work gauge. Counters preserve events; gauges model present state.

**Use gauges with an aggregation rule.** A gauge reports a current or last-observed measurement: queue depth, temperature, memory use, concurrent work, or leader identity encoded numerically only when appropriate. It has no automatic sum semantic. Summing queue depth across shards may be useful; summing CPU temperature across hosts is usually not. Maximum, distribution, or per-resource view may answer the question.

Staleness is part of a gauge. A queue depth of zero at 10:00 is not current health at 10:20 if collection stopped. Store sample time, define freshness, and mark absent or stale values rather than carrying them forward indefinitely. An explicit observed zero and no point are different states.

When averaging gauges, weight by exposure. Mean per-instance CPU may weight instances equally; fleet utilization may require capacity weights; user latency must weight requests, not hosts. State which population the aggregate represents.

**Preserve distributions.** Mean latency hides variance, skew, multimodality, and tails. Samples $1,1,1,1,96$ have mean $20$ but four fast requests and one very slow request. Another population $20,20,20,20,20$ has the same mean and different operational consequences.

A histogram stores count, sum, and bucket populations. With cumulative upper-bound buckets, counts should be nondecreasing and the infinity bucket equals total count. Bucket boundaries must align with decisions: user deadline, SLO threshold, timeout, and diagnostic ranges. Boundaries chosen only around normal behavior can collapse every failure into the last bucket.

A quantile derived from fixed buckets is interval-censored. If the target rank falls after the count at bound $b_{k-1}$ and at or before the count at $b_k$, the value lies in $(b_{k-1},b_k]$ under that convention. Linear interpolation assumes a within-bucket distribution that telemetry did not observe. Report the bound or interpolation assumption.

Histograms merge across streams only when population, unit, temporality, and bucket semantics are compatible. Counts and sums add; corresponding bucket counts add. Precomputed client-side quantiles generally cannot be averaged to recover the combined quantile because ranks depend on the combined distribution.

Exponential histograms trade fixed policy boundaries for approximately constant relative resolution across a wide range [1]. They still compress and require scale compatibility rules. Explicit histograms remain useful when exact policy thresholds matter.

Exemplars retain selected individual observations and correlation context inside an aggregate. They connect a latency bucket to a trace without putting trace IDs in metric labels. Exemplars are examples, not an unbiased reconstruction unless their selection policy establishes that.

**Aggregate ratios from counts.** A success rate needs numerator and denominator over the same boundary, interval, and dimensions. If one region reports successes after gateway admission while another counts all client attempts, summing them produces no coherent global population.

Use ratio of sums when combining disjoint request populations. Suppose a large region has 999 successes of 1,000 and a small region has 90 of 100. Global success is $1{,}089/1{,}100=99.0\%$. The unweighted mean of $99.9\%$ and $90\%$ is $94.95\%$ and gives the small region half the weight. Both views can be useful, but they answer different questions.

Keep the regional view even when global weighting is correct. A global 99.0% can hide severe harm to the small region. Aggregate for the global SLO and retain bounded dimensions for fairness and diagnosis.

For ratios derived from sampled events, numerator and denominator need compatible sampling probabilities or weights. Sampling only successes or only errors biases the rate. Unsampled metric counters are often the authoritative aggregate while sampled traces explain examples.

**Choose dimensions from decisions.** Useful labels often include normalized operation, bounded outcome or error class, region, dependency, protocol, service tier, and release/configuration generation. Each must support a named query: locate a harmed cohort, compare candidate to control, route an owner, or aggregate an SLO.

Avoid user ID, request ID, trace ID, session, raw URL, SQL, exception message, file path, timestamp, and arbitrary payload as metric labels. Put individual identity in controlled logs or traces and link through exemplars. Normalize URL templates and error taxonomies before recording.

Dimensions can be bounded individually yet explosive together. Operation 20, method 3, status 5, region 4, and customer tier 10 allow 12,000 combinations per resource and metric. Adding 100 release identifiers retained concurrently yields 1.2 million. Lifecycle and churn matter as much as static domain size.

Attribute absence also has semantics. Missing `region` may represent legacy instrumentation, unknown location, global scope, or transformation loss. Choose an explicit bounded `unknown` only when those meanings may be combined; otherwise keep separate schema or quality signals.

**Respect time and temporality.** A point has an observation/end time and, for interval values, a start. Cumulative points cover from a stable start; delta points cover successive intervals. Converting delta to cumulative requires ordered, gap-aware state. Converting cumulative to delta requires reset and overlap detection.

Window alignment affects comparisons. A five-minute candidate rate and a five-minute control rate may cover different traffic if scrape delays or rollout stages differ. Record event-time interval, query evaluation time, and freshness. Do not compare a partial current bucket with a completed historical bucket without marking it.

Rates over too-short windows amplify scrape jitter and low counts; long windows delay detection and mix regimes. Choose the window from event frequency, decision latency, false-positive cost, and maximum tolerated harm. Report the actual count so a percentage based on two requests is not mistaken for certainty.

**Distinguish gaps, zero, and stale.** No recorded point can mean no target, failed discovery, scrape failure, exporter rejection, filter, unsupported metric, or expired series. Zero can mean the producer observed none. A stale marker or freshness predicate tells consumers not to reuse old state.

Monitor the metric path: collection success, samples accepted/rejected, duplicate or out-of-order points, exporter queue, dropped points, active series, churn, ingest latency, storage lag, query errors, and rule evaluation. Use independent black-box probes for critical user outcomes.

**Design transformations as semantic operations.** Spatial aggregation removes attributes by combining compatible streams. Temporal aggregation lowers resolution over compatible intervals. Lowering histogram resolution merges buckets and widens error. Each transformation records which distinctions and precision were lost.

Downsampling counters must preserve changes and reset boundaries. Downsampling gauges needs a declared summary such as last, min, max, or time-weighted mean. Downsampling histograms combines counts and sums under compatible buckets. “Average everything every hour” has no universal meaning.

Views and relabeling can reduce cost at collection, but dropping a label before policy queries run makes that distinction unrecoverable. Validate transformation against a query inventory and incidents. Retain raw detail for a bounded interval if a later expensive investigation requires it, subject to privacy and cost.

**Test instrumentation and economics.** Unit-test increments, types, units, boundaries, and label values. Test zero initialization and absence semantics. Restart producers, delay scrapes, duplicate writers, change clocks, drop intervals, overflow exporters, and introduce unknown labels. Compare derived queries with known event fixtures.

Load-test label combinations and churn. Set budgets for active series, new series per minute, samples, bytes, retention, query fan-out, and rule evaluation. Reject or aggregate unsafe attributes before storage rather than waiting for a telemetry outage.

Review metrics as APIs. Track owners and consumers, version semantic breaks, deprecate with overlap, and delete unused streams. Usage alone is insufficient—a rarely queried metric may be essential during incidents—so retirement includes scenario review.

The following deterministic model contrasts series bounds, weighted ratios, and histogram quantile bounds. It is not a telemetry SDK or statistical package.

<!-- bijux-verify: {"id":"metric-semantics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"upper-bound series: 120000\nweighted success: 99.000%\nmean-of-percentages: 94.950%\np50 bucket: (50, 100]\n","stderr":""}} -->
```python
dimensions = [20, 3, 5, 4, 100]
upper_bound = 1
for size in dimensions:
    upper_bound *= size

groups = [(999, 1000), (90, 100)]
weighted = sum(success for success, total in groups) / sum(total for success, total in groups)
mean_percent = sum(success / total for success, total in groups) / len(groups)

observations = [40, 60, 80, 100, 200]
bounds = [50, 100, 250]
target_rank = 3
lower = "-infinity"
upper = None
for bound in bounds:
    if sum(value <= bound for value in observations) >= target_rank:
        upper = bound
        break
    lower = str(bound)

print("upper-bound series:", upper_bound)
print(f"weighted success: {weighted:.3%}")
print(f"mean-of-percentages: {mean_percent:.3%}")
print(f"p50 bucket: ({lower}, {upper}]")
```

## Definitions and Notation

Let $K=(\rho,\sigma,n,\tau,u,\theta,a)$ identify a metric stream. Let $a$ be a finite map from attribute keys to values. For observed combinations $A\subseteq D_1\times\cdots\times D_k$, actual series cardinality is $S=|A|$ and $S\le\prod_i|D_i|$ when every domain is finite.

Let cumulative counter sequence have points $(t_i,C_i,s_i)$, where $s_i$ is the accumulation start. A simple adjacent rate is valid only within one unbroken sequence with $s_i=s_{i-1}$, compatible identity, $t_i>t_{i-1}$, and $C_i\ge C_{i-1}$:

$$
r_i=\frac{C_i-C_{i-1}}{t_i-t_{i-1}}.
$$

Let histogram boundaries be $b_1<\cdots<b_k<+\infty$, cumulative bucket counts $H_j=|\{x:x\le b_j\}|$, total count $N$, and sum $Q=\sum x$. Then $H_1\le\cdots\le H_k\le N$. Mean is $Q/N$ for $N>0$. A target rank first reached in bucket $j$ bounds the observation to $(b_{j-1},b_j]$, with the appropriate negative-infinity first bound.

For groups $i=1,\ldots,m$ with successes $s_i$ and totals $t_i>0$, ratio of sums is $R=\sum s_i/\sum t_i$. Mean of ratios is $M=m^{-1}\sum(s_i/t_i)$. $R=M$ only under special relationships such as equal denominators or compensating rates.

## Mechanisms, Invariants, or Proof Structure

**Cardinality bound.** Every realized label set is an element of the Cartesian product, so its count cannot exceed the product of finite domain sizes. The upper bound can be loose because combinations may be impossible. It becomes unusable when a domain is unbounded or unknown.

**Counter-rate argument.** Within one cumulative sequence, subtraction removes prior accumulated work and leaves events during the interval. Across a reset, the later value excludes earlier work, so subtraction is invalid. Start identity and monotonicity are necessary evidence for the simple rate.

**Weighted-ratio derivation.** Each group's rate is $r_i=s_i/t_i$. Global successes and attempts are additive over disjoint populations, giving $R=\sum t_ir_i/\sum t_i$. Thus $R$ is a denominator-weighted mean. Equal weighting answers a different question: performance of a uniformly selected group.

**Histogram bound.** Cumulative count $H_j$ tells how many observations are at or below $b_j$. When the target rank exceeds $H_{j-1}$ and is at most $H_j$, the ranked value must be inside that bucket. Its exact location is not identified without more information or an interpolation assumption.

**Mean counterexample.** Populations $1,1,1,1,96$ and $20,20,20,20,20$ both sum to 100 and count five, hence mean 20. Their p80/p100 behavior differs. Count and sum are insufficient to reconstruct tails.

**Dimension-loss argument.** Aggregation that removes an attribute maps several streams to one result. Once the source streams expire, no query over the aggregate can reconstruct how value was divided among the removed dimension without another model or evidence.

## Alternatives and Trade-Offs

**One metric versus labeled family.** Labels keep one semantic family and support aggregation; separate names can enforce truly different semantics. Use labels for bounded dimensions of one measurement, names for different populations or types.

**Counter versus gauge.** Counters preserve occurrence history across collection gaps when cumulative state survives. Gauges represent present state directly. Deriving current concurrency from started minus completed counters is resilient but requires compatible reset handling.

**Cumulative versus delta.** Cumulative streams reconcile intermittent collection and make gaps visible through later totals, at state cost proportional to cardinality. Delta moves state downstream and supports some sampling, but missing intervals lose their values.

**Explicit versus exponential histograms.** Explicit boundaries align exactly with policy thresholds and merge simply when identical. Exponential schemes cover wide ranges with relative resolution. Choose from decision error, interoperability, and cost.

**Histogram versus client-computed quantiles.** Histograms aggregate across instances and support multiple server-side ranks with bounded bucket error. Client quantiles can be more locally accurate or adaptive but are generally not mergeable. Preserve distributions needed at the aggregation boundary.

**Low versus high dimensionality.** More dimensions improve diagnosis and fairness checks; they increase memory, storage, churn, query fan-out, and privacy risk. Preserve bounded consequential cohorts and route individual identity to logs or traces.

**Pre-aggregation versus raw events.** Metrics make continuous decisions cheap. Raw events permit new questions and exact records at greater volume. Use metrics for authoritative aggregates and sampled/detail signals for explanation.

**Instance versus service aggregation.** Instance data finds hotspots and imbalance; service aggregates align with user outcomes. Retain instance detail for a bounded diagnostic window and alert primarily on service symptoms unless an instance requires action.

**Static versus adaptive dimensions.** Static schemas are predictable and queryable. Adaptive top-k or overflow buckets bound dynamic workloads but hide the long tail and change membership. Record approximation and use detail stores for follow-up.

## Failure Modes and Misconceptions

1. **“A metric is just name and value.”** Type, unit, identity, attributes, temporality, and time determine meaning.
2. **“Labels are free metadata.”** Every distinct label set creates a stream and index work.
3. **“Bounded labels cannot explode.”** Their Cartesian product and lifecycle can still be enormous.
4. **“Request IDs improve metric diagnosis.”** They turn aggregates into one series per request; use exemplars or traces.
5. **“Counters never decrease.”** Process or sequence resets occur; negative deltas need reset interpretation.
6. **“No sample means zero.”** Discovery, export, storage, or query may have failed.
7. **“The last gauge remains current.”** Freshness expires; carrying forward hides outage and change.
8. **“All gauges can be summed.”** Aggregation requires a domain meaning.
9. **“Average percentages gives the global rate.”** It weights groups rather than observations unless denominators match.
10. **“Mean latency represents users.”** Different distributions share a mean, and tails can dominate composed services.
11. **“A histogram gives exact quantiles.”** Fixed buckets provide interval information; interpolation adds assumptions.
12. **“Client quantiles can be averaged.”** Quantiles are not additive and usually cannot reconstruct the union.
13. **“Buckets can change in place.”** Boundary changes alter stream semantics and break aggregation/history.
14. **“Global health makes cohort dimensions unnecessary.”** Small regions or releases can be severely harmed under a green aggregate.
15. **“Downsampling is just storage compression.”** It chooses temporal and spatial semantics and can erase incidents.
16. **“Telemetry capacity is separate from reliability.”** Cardinality storms and expensive queries can blind monitoring during failures.

## Worked Examples

### Example 1

**Situation.** A cumulative request counter is 9,800 at 10:00 and 10,400 at 10:02 with the same start time.

**Reasoning.** The interval contains $10{,}400-9{,}800=600$ requests over 120 seconds. Average rate is $600/120=5$ requests/s. This does not reveal within-window bursts.

**Conclusion.** Counter difference yields an interval average only under unbroken identity and monotonicity.

### Example 2

**Situation.** The next sample is 80 because the process restarted.

**Reasoning.** Naive difference $80-10{,}400=-10{,}320$ is not negative traffic. A new accumulation start identifies a reset. Rate after restart needs a point from the new sequence or a model that accounts for the boundary.

**Conclusion.** Reset is telemetry lifecycle, not a negative business event.

### Example 3

**Situation.** A metric has dimensions 20 operations, 3 methods, 5 outcomes, 4 regions, and 100 customer classes.

**Reasoning.** The Cartesian upper bound is $20\times3\times5\times4\times100=120{,}000$ streams per remaining identity scope. If customer class is unnecessary or can be reduced to 10 bounded tiers, the bound falls to 12,000. Actual combinations must still be measured.

**Conclusion.** Dimension design is multiplicative; start from named queries and budgets.

### Example 4

**Situation.** Regions report 999/1,000 and 90/100 successes.

**Reasoning.** Global user-weighted success is $(999+90)/(1{,}000+100)=1{,}089/1{,}100=99.0\%$. Equal region mean is $(99.9\%+90\%)/2=94.95\%$. The first answers a random-request question; the second highlights a random-region experience.

**Conclusion.** Choose weights from the population and retain the harmed-region view.

### Example 5

**Situation.** Five latencies are 40, 60, 80, 100, and 200 ms with cumulative bounds 50, 100, and 250 ms.

**Reasoning.** Counts are 1, 4, and 5; total is 5 and sum 480, so mean is 96 ms. Median rank 3 first appears in the 100-ms bucket, so p50 lies in $(50,100]$ ms. Exact 80 ms is known only because raw samples were supplied, not from the histogram.

**Conclusion.** Histograms support aggregate count, mean, and bounded quantiles while discarding exact values.

### Example 6

**Situation.** Two instances export p99 latency 100 ms and 1,000 ms.

**Reasoning.** Their average 550 ms is not the combined p99. One instance may have ten requests and the other one million; the rank in the union depends on both full distributions. Merge compatible histogram counts or retain a mergeable sketch with stated error.

**Conclusion.** Quantiles are not additive statistics.

### Example 7

**Situation.** Queue depth is 20 on shard A and 30 on shard B; queue age is 5 and 100 seconds.

**Reasoning.** Total queue depth 50 represents total waiting items if shards are disjoint. Summed age 105 seconds has no useful interpretation. Maximum age 100 detects the oldest harm; a depth-weighted age requires per-item or representative weighting assumptions.

**Conclusion.** The same resources can support sum for one gauge and maximum for another.

### Example 8

**Situation.** A latency gauge last reported 12 ms twenty minutes ago while its exporter is down.

**Reasoning.** Reusing 12 as current hides uncertainty. Compare point time with freshness policy, mark the stream stale, alert on telemetry completeness where actionable, and use an independent user probe. Do not replace absence with zero.

**Conclusion.** Freshness is part of gauge truth.

### Example 9

**Situation.** Candidate and control releases share one fleet-wide error counter.

**Reasoning.** Aggregation removed the release dimension before comparison. Old healthy traffic can mask candidate failure, and the split cannot be reconstructed after source series expire. Add bounded release generation during rollout, budget concurrent generations, and retire it after the diagnostic window.

**Conclusion.** A dimension required by a decision must survive until that decision and investigation finish.

### Example 10

**Situation.** An incident introduces a unique raw error message per request, producing 50,000 new streams per minute.

**Reasoning.** The label violates bounded-domain policy and churns indexes. Reject or map it to a bounded error taxonomy, increment a dropped-attribute counter, retain sampled messages in structured logs, and protect the metrics backend with series-creation limits. Verify SLO counters remain available.

**Conclusion.** Cardinality controls must fail visibly while preserving critical aggregate signals.

## Cross-Program Connections

1. **Systems Engineering (SYSENG):** supplies measurement, state estimation, feedback, sensor coverage, and control-loop reasoning.
2. **Data Structures Engineering (DSE):** supplies sketches, histograms, indexes, and memory trade-offs.
3. **Data Engineering (DE):** supplies windowing, late data, stream aggregation, schemas, and quality.
4. **Database Engineering (DBE):** supplies time-series indexing, compression, retention, and query execution.
5. **Distributed Systems (DIST):** supplies clocks, partial failure, duplicate writers, ordering, and convergence.
6. **Operating Systems (OS):** supplies counters, gauges, schedulers, clocks, and resource accounting.
7. **Networking (NET):** supplies throughput, loss, latency, queue, and path measurement semantics.
8. **Security Engineering (SEC):** owns metric integrity, tenant isolation, sensitive dimensions, and telemetry abuse.
9. **Platform Engineering (PLAT):** owns shared metric SDKs, collectors, budgets, storage, and query service levels.
10. **API and Service Engineering (API):** defines normalized operations, outcomes, and user boundaries that metrics measure.

## References

1. OpenTelemetry Authors, “Metrics Data Model,” OpenTelemetry Specification 1.60.0, mixed document with stable overview and model sections. <https://opentelemetry.io/docs/specs/otel/metrics/data-model/>. Accessed 2026-09-06.
2. OpenMetrics Authors, “OpenMetrics Specification 1.0.” <https://prometheus.io/docs/specs/om/open_metrics_spec/>. Accessed 2026-09-06.
3. Prometheus Authors, “Instrumentation.” <https://prometheus.io/docs/practices/instrumentation/>. Accessed 2026-09-06.
4. Prometheus Authors, “Metric and Label Naming.” <https://prometheus.io/docs/practices/naming/>. Accessed 2026-09-06.
5. Rob Ewaschuk, “Monitoring Distributed Systems,” in *Site Reliability Engineering*, O'Reilly Media, 2016. <https://sre.google/sre-book/monitoring-distributed-systems/>. Accessed 2026-09-06.
6. Jeffrey Dean and Luiz André Barroso, “The Tail at Scale,” *Communications of the ACM*, vol. 56, no. 2, pp. 74–80, 2013, DOI 10.1145/2408776.2408794. <https://research.google/pubs/the-tail-at-scale/>.
7. Colin Adams et al., “Monarch: Google's Planet-Scale In-Memory Time Series Database,” *Proceedings of the VLDB Endowment*, vol. 13, no. 12, pp. 3181–3194, 2020. <https://www.vldb.org/pvldb/vol13/p3181-adams.pdf>.
8. Raj Jain, *The Art of Computer Systems Performance Analysis: Techniques for Experimental Design, Measurement, Simulation, and Modeling*, Wiley, 1991, ISBN 978-0-471-50336-1. <https://www.cs.wustl.edu/~jain/books/perfbook.htm>.

## Exercises

### Exercise 1

Define measurement, stream identity, counter, gauge, histogram, temporality, dimension, cardinality, reset, staleness, and exemplar. Explain why metric name alone is insufficient.

### Exercise 2

A counter has points $(10{:}00,1{,}000,s_1)$, $(10{:}02,1{,}600,s_1)$, $(10{:}04,200,s_2)$, and $(10{:}06,800,s_2)$. Compute every valid adjacent average rate and explain the invalid interval.

### Exercise 3

Design metrics for an asynchronous image service with upload, transform, and delivery stages. Include traffic, errors, latency, saturation, queue state, release comparison, freshness, and bounded dimensions. Reject at least four tempting labels.

### Exercise 4

Compare an explicit histogram with boundaries 100, 250, 500, and 1,000 ms against client-computed p50/p95/p99 for a service aggregated across 200 instances. State what can merge, what error is known, and which you choose.

### Exercise 5

A public transit system wants real-time reliability by route, stop, vehicle, trip, rider, ticket, region, software release, and error text. Produce a metric-and-detail architecture that supports fleet SLOs, small-route fairness, incident diagnosis, privacy, cost, late data, and telemetry failure.

## Answers to the Exercises

### Answer 1

A measurement is a numeric observation under a procedure. Stream identity combines resource, scope, name, type, unit, temporality/intrinsic properties, and full dimensions. A counter accumulates nonnegative occurrences between resets; a gauge reports current or last-observed state; a histogram compresses a population into count, sum, and buckets. Temporality defines interval delta versus accumulation. A dimension partitions streams; cardinality counts realized sets. A reset starts a new cumulative sequence; staleness invalidates an old point as current evidence. An exemplar links selected individual context to an aggregate. Name alone omits every other semantic and cannot tell consumers how to aggregate or compare the value.

### Answer 2

From 10:00 to 10:02, start identity is unchanged and rate is $(1{,}600-1{,}000)/120=5$ units/s. The 10:02-to-10:04 subtraction is invalid because start changes from $s_1$ to $s_2$; $200-1{,}600$ is a reset artifact. From 10:04 to 10:06, rate is $(800-200)/120=5$ units/s. One cannot infer the reset-crossing interval total without additional delta or event evidence.

### Answer 3

Use counters for accepted uploads and stage completions by normalized operation, bounded outcome/error class, region, service tier, and release during rollout. Use histograms for end-to-end and per-stage latency with deadline/SLO-aligned boundaries. Use gauges for queue depth and oldest age per bounded queue/region, worker capacity, and exporter health; define sum for depth and maximum for age. Measure active series, samples, drops, and freshness. Reject image ID, user ID, trace ID, raw URL, filename, and exception message as labels. Link exemplars to traces and retain individual details in protected structured logs. Keep candidate/control release long enough for rollout and investigation, then retire old values.

### Answer 4

Compatible explicit bucket counts, total, and sum add across 200 instances, so fleet distributions and bounded quantiles are computable. The target quantile lies within the first bucket whose cumulative count reaches its rank; worst interval width depends on boundaries, and interpolation adds an assumption. Client p50/p95/p99 generally cannot be merged or averaged because the union's ranks depend on each full distribution and request count. Choose the explicit histogram when fleet aggregation and policy thresholds matter, adding narrower boundaries around SLO and timeout values. A client sketch is acceptable only if it has specified merge and error properties supported end to end.

### Answer 5

Use unsampled counters for trips, expected/actual arrivals, cancellations, and bounded outcome classes by route class, bounded route ID where budget permits, region, time band, and release. Use histograms for arrival deviation and journey latency with passenger-impact thresholds; calculate fleet reliability as ratio of summed qualifying events while retaining small-route views. Vehicle or trip identity may be retained briefly in controlled logs/traces, not continuous metric labels; rider, ticket, and raw error text are excluded or pseudonymized only under authorized detail workflows. Stream late events by event-time windows with correction status, expose completeness and lag, and reconcile against the schedule authority. Budget series and churn, tier retention, protect access, and maintain independent telemetry-path monitors. This preserves fleet decisions and fairness while routing individual diagnosis to a higher-cardinality governed store.
