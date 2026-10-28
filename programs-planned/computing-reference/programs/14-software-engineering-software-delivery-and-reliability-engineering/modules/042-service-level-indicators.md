---
module_id: SDRE-042
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 42
title: Service-Level Indicators
status: complete
last_verified: 2026-09-06
---

# Service-Level Indicators

## One-Page Review

### Governing question

How can engineers turn a user-valued service property into a quantitative indicator whose population, observation point, classification rule, units, window, and uncertainty are precise enough to support operational decisions?

### Essential definitions

- a **service-level indicator (SLI)** is a carefully defined quantitative measure of an aspect of delivered service;
- an **eligible event** belongs to the population the indicator claims to describe;
- a **good event** is an eligible event satisfying the declared outcome predicate;
- a **request-based SLI** is usually $|G|/|V|$, good events divided by valid eligible events;
- a **time-based SLI** classifies bounded time intervals rather than requests;
- a **distribution-based SLI** preserves observations such as latency in buckets before applying a good threshold;
- the **measurement point** is where and when the observation is made;
- a **measurement window** is the interval over which observations are selected and aggregated;
- a **proxy SLI** measures an observable correlated with, but not identical to, the user-valued property;
- **coverage** is the fraction of the intended population represented by evaluable observations;
- **missingness** is absence of required evidence and is not automatically good, bad, or ineligible;
- an **unknown classification** preserves events that cannot be judged honestly;
- an **SLI specification** records the population, predicate, point, source, units, window, partitions, exclusions, missing-data policy, and validation method.

### Central model, mechanism, or theorem

For intended event population $U$, eligibility predicate $E(e)$, observed-and-evaluable predicate $O(e)$, and good predicate $Q(e)$, define

$$
V=\{e\in U:E(e)\land O(e)\},\qquad
G=\{e\in V:Q(e)\}.
$$

When $|V|>0$, the observed SLI is $S=|G|/|V|$. Its coverage is $C=|V|/|\{e\in U:E(e)\}|$ when the intended eligible count is knowable. $S$ without $C$, exclusion counts, or missingness can look excellent while representing little of the intended service.

### Critical invariants

- begin with a user-valued behavior, not a convenient metric name;
- define one intended population and one observation boundary per indicator;
- make eligibility and goodness separate predicates;
- count all outcomes of an attempt or logical operation consistently;
- keep numerator and denominator from the same source, scope, and window where possible;
- treat zero denominators explicitly;
- preserve missing, late, duplicated, reset, and schema-incompatible observations;
- report counts and coverage with the ratio;
- partition cohorts only with bounded, decision-relevant dimensions;
- validate the indicator against controlled cases and a more direct reference measurement.

### Common failures

Failures include calling every metric an SLI, treating every HTTP 2xx as user success, excluding slow failures from latency, counting retries inconsistently, mixing client and server populations, averaging percentages without weights, using means that hide tails, computing quantiles after incompatible aggregation, interpreting no traffic as 100%, treating missing telemetry as zero errors, allowing exclusions to drift, changing thresholds without versioning, and reporting many nines from a tiny or biased sample.

### Compact example

During one hour, a checkout edge records 10,000 eligible final logical operations. Of these, 9,850 return a correct confirmation within 800 ms, 100 return a correct but slow confirmation, 30 fail, and 20 lack a trustworthy outcome because telemetry was rejected. The strict success-and-latency SLI is $9{,}850/(9{,}850+100+30)=98.70\%$ over 9,980 evaluable operations; coverage is $9{,}980/10{,}000=99.80\%$. The 20 unknowns are reported separately. Classifying them all as good would yield 98.70% only coincidentally after a changed denominator; classifying them all as bad gives a conservative lower bound of 98.50%.

### Connections

[SDRE-041](041-reliability-availability-and-durability.md) defines the properties being observed. [SDRE-043](../ROADMAP.md) next turns selected indicators into explicit objectives; later modules distinguish agreements and error-budget policy.

## Governing Question

“Availability is 99.9%” sounds precise, but the number is uninterpretable until its measurement contract is known. Was it time or requests? Which requests? Measured at the browser, edge, server, queue, or database? Did a syntactically successful response contain the correct result? Were retries counted as attempts or as one user operation? What happened to missing observations?

An SLI is not merely a stored time series or dashboard expression. It is a claim that a defined observation represents a defined aspect of service for a defined population. The governing question asks how to make that claim inspectable, reproducible, and honest about the distance between what users value and what instrumentation can see.

## Why This Matters

Google's SRE text defines an SLI as a carefully defined quantitative measure and emphasizes that client-side and server-side measurements can describe different experiences [1]. Its practical guidance recommends starting from what users care about, selecting only a small representative set, and standardizing measurement definitions [1]. The SRE Workbook commonly expresses an indicator as good events divided by total valid events because the ratio is interpretable and can later support objectives and budgets [2].

The ratio is only as trustworthy as its event model. A response counter can omit connections that never reached the server. A browser metric can exclude users who abandoned before instrumentation initialized. A latency histogram can preserve thresholds across instances, whereas an average or precomputed client-side quantile may not aggregate into the population the reader assumes [3]. Current OpenTelemetry metrics specifications distinguish event, metric-stream, and timeseries models and identify stream semantics with type, unit, temporality, timestamps, and attributes [4, 5]. Those details affect whether numerator and denominator can be combined.

Protocol status is evidence, not the complete product contract. RFC 9110 defines HTTP response classes and says 2xx means the request was successfully received, understood, and accepted [6]. A 200 response with the wrong account balance or an asynchronous acceptance whose job later fails can still violate the user's intended outcome. Indicator design therefore joins protocol evidence with domain semantics at the boundary where the result becomes knowable.

## Prerequisites and Retrieval

Retrieve service contract, user journey, event, operation, attempt, outcome, correctness, latency, availability, durability, population, sample, predicate, counter, gauge, histogram, percentile, dimension, timestamp, window, reset, missingness, bias, and uncertainty.

From SDRE-033 retrieve counter and histogram behavior. From SDRE-038 retrieve actionability. From SDRE-039 retrieve sampling and cost. From SDRE-040 retrieve measurement points and evidence quality. From SDRE-041 retrieve the distinction among mission reliability, demand availability, and state durability.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish an SLI specification from a raw metric and from an objective;
2. derive indicators from user journeys and service contracts;
3. define intended, eligible, evaluable, good, bad, and unknown populations;
4. construct request-, time-, and distribution-based indicators;
5. choose a measurement boundary and state its proxy gap;
6. handle retries, asynchronous completion, cancellations, and partial success;
7. preserve units, temporality, windows, resets, and aggregation meaning;
8. compute weighted aggregate and cohort-specific ratios correctly;
9. expose missingness, coverage, exclusions, and zero-denominator cases;
10. validate an SLI against controlled outcomes and direct user evidence.

## Core Exposition

**Begin with the user-valued behavior.** Write a concrete sentence before opening a metrics catalog: “an authorized buyer can place an order and receive a correct confirmation,” “a subscriber receives each urgent notification before its deadline,” or “an acknowledged object remains retrievable with identical content.” Identify the actor, operation, acceptable result, timing boundary, and population.

Now ask what can be observed. The ideal property may require knowledge unavailable at one component. A server sees handler completion; an edge sees network delivery; a client sees rendering; a synthetic probe sees one scripted path; a business reconciliation process can see semantic correctness later. Choose the closest feasible measurement and state what it misses.

**Separate the indicator from its target.** An indicator answers “what was measured?” An objective later answers “what range should be achieved?” Writing `99.9%` into the SLI definition prematurely mixes mechanism with policy. A latency threshold can appear inside a good-event predicate—“completed under 400 ms”—without asserting the percentage that must meet it. SDRE-043 governs that percentage and its evaluation window.

**Define the intended unit of analysis.** A user journey may contain client attempts, gateway attempts, server requests, dependency calls, queue deliveries, and one final logical outcome. These are different event populations. A retry can improve the logical-operation result while increasing attempt-level failures and latency. Neither view is false, but each answers a different question.

For a user-facing availability indicator, the logical operation is often primary. Retain attempt-level indicators for mechanism diagnosis. Declare how deduplication works, how long a logical operation remains open, and what happens when the client disappears before observing a result.

**Specify eligibility independently from goodness.** Eligibility decides whether an event belongs to the claim. Goodness judges eligible service. Authentication attacks, unsupported methods, malformed input, load-test traffic, administrative probes, and user cancellations may need distinct treatment. Do not exclude an event merely because the service failed it.

A client error is not automatically ineligible. A rejected payment with insufficient funds may be a correct service outcome; an authorization rejection caused by a stale policy cache may be a bad service outcome. HTTP status classes provide protocol semantics [6], while the product contract supplies the domain judgment.

**Preserve unknown.** An eligible event can be observed but not evaluable: its result record is corrupt, its join key is absent, clocks make the deadline undecidable, or measurement stops during a collector outage. Unknown is a property of evidence. It should not silently change the service's success predicate.

For a report, publish at least good, bad, unknown, excluded-by-reason, and intended counts. If the intended count is unknowable because the measurement point missed arrivals, say so. Where useful, bound the result: treating every unknown as bad gives a lower bound, and treating every unknown as good gives an upper bound, provided unknown events are otherwise eligible and counted once.

**Use a request-based ratio for discrete events.** Let valid evaluable events be $V$ and good events $G\subseteq V$. Then $S=|G|/|V|$. The ratio is naturally weighted by events. Aggregate cohorts by summing numerators and denominators, not by averaging their percentages unless equal cohort weight is the stated estimand.

Counts should normally originate from compatible monotonic counters with the same labels, source semantics, and interval. Counter resets, late data, duplicate ingestion, and inconsistent filters can make the derived ratio negative, greater than one, or biased. Test those cases instead of clamping the result and hiding the defect.

**Use time-based classification when time is the unit.** Divide an evaluation interval into fixed, non-overlapping slices, such as one minute, and classify each slice by a declared rule. A “good minute” might require at least one eligible probe and a request success ratio above a threshold. Time-weighted availability can also be computed from acceptable duration divided by eligible duration.

Time-based indicators weight quiet and busy periods by time; request-based indicators weight them by demand. A one-minute outage at peak load and at midnight have equal time weight but very different request weight. Choose based on the service question and report the alternate view when it materially changes interpretation.

**Use distributions before collapsing latency.** Latency is an observation for each event. A good-event latency SLI classifies an eligible event as good when its declared duration is at or below a threshold. A histogram stores counts across configured boundaries so threshold counts can be aggregated. Prometheus documents that histograms expose bucketed counts and calculate quantiles server-side, while summaries calculate streaming quantiles in the instrumented process [3]. This difference matters across replicas.

Do not discard failed or timed-out requests before defining the latency population. A fast error is not a good successful request; a timeout capped at ten seconds is still evidence of user delay. Often teams maintain separate availability and successful-request latency indicators, plus a combined “correct and within deadline” indicator for the user journey.

**Define measurement time and event time.** Specify start and end boundaries: client invocation to usable response, edge receipt to last byte, queue availability to processing completion, or data source event time to published result. Use monotonic clocks for durations within a process. Cross-process timestamps require clock-quality assumptions.

Select events by a declared timestamp. Completion-time windows include operations that finish in the interval; start-time windows include operations begun then. Long-running operations straddling a boundary can therefore move between reports. Pick one convention, retain enough fields to audit it, and avoid silently changing it.

**Make freshness and correctness first-class.** For a pipeline, freshness might be the proportion of eligible records visible within fifteen minutes of source event time. For search, quality could mean results computed from the entire authorized corpus. For a storage read, correctness could require identity, version, checksum, and semantic invariants. A status code or nonempty response is insufficient.

Some correctness is known only after reconciliation. Use a delayed indicator with an explicit maturity horizon rather than pretending immediate evidence is final. Separate preliminary and mature series so late corrections do not rewrite operational history without notice.

**Partition by decision-relevant cohorts.** Region, operation class, client version, service tier, and bounded payload class may expose concentrated harm. High-cardinality identity does not belong in metric dimensions. Publish global event-weighted results together with important cohort results and counts. A global ratio can meet an eventual objective while a small cohort receives no service.

**Version the specification.** Give each SLI a stable identifier and version. Record owner, user behavior, event unit, intended population, eligibility, goodness, observation point, source, query, units, temporality, timestamp selection, window, cohort dimensions, exclusions, missing-data handling, expected range, validation, and change history. A query text alone is not the specification because instrumentation and schemas can change beneath it.

The following executable model keeps evidence classes separate and computes an observed ratio plus bounds. It is a controlled event classifier, not a production monitoring implementation.

<!-- bijux-verify: {"id":"classify-sli-events","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"good=3 bad=2 unknown=1 excluded=1\nobserved=60.00% coverage=83.33%\nbounds=50.00%..66.67%\n","stderr":""}} -->
```python
events = [
    {"eligible": True, "outcome": "good"},
    {"eligible": True, "outcome": "good"},
    {"eligible": True, "outcome": "bad"},
    {"eligible": False, "outcome": "bad"},
    {"eligible": True, "outcome": "unknown"},
    {"eligible": True, "outcome": "good"},
    {"eligible": True, "outcome": "bad"},
]
eligible = [event for event in events if event["eligible"]]
good = sum(event["outcome"] == "good" for event in eligible)
bad = sum(event["outcome"] == "bad" for event in eligible)
unknown = sum(event["outcome"] == "unknown" for event in eligible)
excluded = len(events) - len(eligible)
evaluable = good + bad
observed = good / evaluable
coverage = evaluable / len(eligible)
lower = good / len(eligible)
upper = (good + unknown) / len(eligible)
print(f"good={good} bad={bad} unknown={unknown} excluded={excluded}")
print(f"observed={observed:.2%} coverage={coverage:.2%}")
print(f"bounds={lower:.2%}..{upper:.2%}")
```

**Validate the indicator as a measurement system.** Create fixtures containing success, semantic failure, fast failure, timeout, cancellation, retry, duplicate, late completion, clock skew, reset, missing observation, and schema change. Verify the classifications and queries. Compare server indicators with client or synthetic observations over matched operations. Investigate disagreement instead of selecting the more flattering source.

Review sampling. Event-count SLIs usually require exhaustive or demonstrably representative counting; trace sampling is not an automatic substitute. Review collection loss, timestamp delay, cardinality overflow, exporter rejection, and query freshness. Evidence health must remain separate from service health.

Finally, review decision usefulness. An SLI should change when the user-valued behavior changes, remain stable when irrelevant internals change, identify an owner, and support a plausible response. Retire indicators that no longer represent a valued contract, but retain versioned historical meaning for past reports.

## Definitions and Notation

Let $U_W$ be the intended population associated with measurement window $W$. Let $E(e)$ be the eligibility predicate, $O(e)$ the observed-and-evaluable predicate, and $Q(e)$ the good predicate. Define intended eligible, evaluable, good, bad, and unknown sets:

$$
I=\{e\in U_W:E(e)\},\quad
V=\{e\in I:O(e)\},\quad
G=\{e\in V:Q(e)\},
$$

$$
B=V\setminus G,\qquad X=I\setminus V.
$$

For $|V|>0$, observed service level is $S=|G|/|V|$. If $|I|>0$, coverage is $C=|V|/|I|$. If every intended eligible event appears exactly once and unknown means only unclassifiable outcome, bounds are

$$
\frac{|G|}{|I|}\le S_{\text{true}}\le\frac{|G|+|X|}{|I|}.
$$

For cohort $k$, let good and valid counts be $g_k$ and $v_k$. The event-weighted aggregate is

$$
S_{\text{event}}=\frac{\sum_k g_k}{\sum_k v_k}
=\sum_k\frac{v_k}{\sum_j v_j}\frac{g_k}{v_k},
$$

for cohorts with positive denominators. An equal-cohort mean assigns different weights and answers a different question.

For time slices $t\in T$, with weight $w_t>0$ and good classification $q_t\in\{0,1\}$, a weighted time indicator is $S_T=\sum_t w_tq_t/\sum_t w_t$. Equal fixed slices set every $w_t=1$.

For latency $L(e)$ and threshold $\tau$, a combined good predicate may be $Q(e)=\text{correct}(e)\land L(e)\le\tau$. The units and inclusion boundary—less than versus less than or equal—are part of the specification.

## Mechanisms, Invariants, or Proof Structure

**Subset invariant.** Because goodness is judged only for evaluable eligible events, $G\subseteq V\subseteq I\subseteq U_W$. Therefore $0\le |G|/|V|\le1$ when $|V|>0$. A computed ratio outside this range proves inconsistent counts, duplication, resets, or filters.

**Weighted-aggregation derivation.** Replace each cohort ratio $g_k/v_k$ with weight $v_k/\sum_jv_j$. The product is $g_k/\sum_jv_j$; summing yields $\sum_kg_k/\sum_jv_j$. An unweighted average is equivalent only when cohort denominators are equal or equal cohort importance is intentional.

**Unknown-bound argument.** Under one-to-one coverage, the worst case assigns all unknowns to bad and the best case assigns all to good. Any true count of good unknowns lies from zero to $|X|$, producing the stated interval. The bound is invalid if intended events are themselves missing or duplicated.

**Proxy-gap argument.** If server completion is observed before client usability, a server-side good event does not logically imply a good client event. The implication requires extra assumptions about network, intermediary, client, and rendering behavior. Those assumptions define the proxy gap and must be tested.

**Time-versus-demand argument.** Time weighting samples moments; request weighting samples demand. They coincide only under restrictive conditions, such as constant demand independent of service state and compatible classification. Otherwise neither can be substituted for the other.

**Threshold aggregation argument.** Counts in compatible histogram buckets are additive across instances and time intervals. Precomputed quantile values are not generally additive: the quantile of combined observations cannot be recovered by averaging per-instance quantiles. Preserve distributions or raw events when cross-scope quantiles are required.

## Alternatives and Trade-Offs

**Client versus server measurement.** Client measurement is closer to perceived completion but can be incomplete, privacy-sensitive, or unavailable before initialization. Server measurement is controlled and comprehensive for arrivals it sees but misses upstream failure and client rendering. Use both for critical journeys and quantify their gap.

**Request versus time weighting.** Request ratios represent demanded operations and emphasize busy periods. Time ratios include quiet periods and suit continuously required service. Report which population matters rather than selecting the higher number.

**Attempt versus logical-operation units.** Attempts expose retries and dependency instability. Logical outcomes represent whether the user eventually succeeded. Keep both with an explicit join and terminal-outcome rule.

**Separate versus combined predicates.** Separate availability, latency, freshness, and correctness indicators localize failure. A combined predicate represents complete user success. A small set can include both without multiplying redundant objectives.

**Threshold ratio versus percentile.** Threshold ratios answer what fraction met a specific deadline and compose naturally with event counting. Percentiles describe a distribution location but are sensitive to aggregation method. Choose according to the decision and retain distributions for investigation.

**Synthetic versus organic traffic.** Synthetic probes provide consistent coverage and can test from outside. They exercise a narrow scripted workload and may miss authentication, data, geography, and client diversity. Organic measurement is representative only if instrumentation coverage is known.

**Exclude versus classify bad.** Exclusion can remove traffic outside the contract; classifying bad preserves service-caused harm. Govern exclusions by named reason and monitor their rate so failures cannot migrate out of the denominator.

**Immediate versus mature correctness.** Immediate proxies support fast operations; delayed reconciliation sees semantic truth. Publish preliminary and mature variants with their lag rather than rewriting one unlabeled series.

## Failure Modes and Misconceptions

1. **“Every metric is an SLI.”** Resource utilization may explain behavior without measuring a delivered service property.
2. **“An SLI includes the desired percentage.”** The percentage target belongs to an SLO; the SLI defines measurement.
3. **“All 2xx responses are good.”** Protocol acceptance can coexist with incorrect content or failed downstream completion.
4. **“All 4xx responses are user-caused and excluded.”** Some are correct outcomes; others result from service defects or stale authorization state.
5. **“Server latency is user latency.”** Queuing before ingress, transport, client work, and rendering can dominate experience.
6. **“Retries disappear after success.”** Hiding attempts conceals instability, resource amplification, and extra latency.
7. **“No traffic means 100%.”** A zero denominator yields undefined or no-data, not success.
8. **“Missing telemetry means no errors.”** Missingness is evidence failure and needs its own classification.
9. **“Average latency represents most users.”** Skew and long tails can produce a benign mean while many users exceed a deadline.
10. **“Average of regional percentages is global availability.”** The unweighted mean gives regions equal weight, not requests.
11. **“Average of p99s is the global p99.”** Quantiles do not aggregate by arithmetic mean.
12. **“Histogram buckets can change freely.”** Boundary changes can make streams incompatible and historical comparisons false.
13. **“More exclusions make the SLI accurate.”** Uncontrolled exclusions can remove exactly the failures the contract should expose.
14. **“A synthetic probe represents all users.”** It represents its location, data, credentials, path, and schedule.
15. **“Five nines from 1,000 events is precise.”** Sample size, coverage, dependence, and bias bound defensible precision.
16. **“Clamping a ratio repairs it.”** Values outside $[0,1]$ reveal measurement inconsistency that must be diagnosed.
17. **“One global SLI protects every cohort.”** Large healthy cohorts can mask total failure for a small one.
18. **“Changing a query is harmless.”** It changes historical meaning unless versioned, backfilled, and reviewed.

## Worked Examples

### Example 1

**Situation.** A team calls CPU utilization its availability SLI. CPU remains at 30% while users receive authentication failures.

**Reasoning.** CPU is an internal resource signal. It may explain capacity failure but does not classify whether eligible authentication operations succeeded. Define the user event as one authorized login attempt, observe its terminal client-visible outcome, and use CPU only as diagnostic evidence.

**Conclusion.** A useful metric is not necessarily an SLI; the indicator must measure delivered service.

### Example 2

**Situation.** An API records 9,700 correct responses under 500 ms, 100 correct responses over 500 ms, 150 service failures, and 50 malformed unsupported requests.

**Reasoning.** If malformed unsupported requests are governed exclusions, eligible events total $9{,}950$. Availability by correct result is $(9{,}700+100)/9{,}950=98.492\%$. The combined correct-and-fast indicator is $9{,}700/9{,}950=97.487\%$. Excluded traffic is reported as $50/10{,}000=0.5\%$ of arrivals.

**Conclusion.** Eligibility and goodness produce two distinct, reproducible indicators from the same observations.

### Example 3

**Situation.** A client retries twice: the first attempt times out, the second receives 503, and the third succeeds after a total of 1.8 seconds.

**Reasoning.** Attempt availability is $1/3=33.33\%$. Logical-operation availability is $1/1=100\%$ if eventual success is the contract. If the user deadline is one second, combined logical success-and-latency is $0/1=0\%$. All three are valid only with their named event unit and predicate.

**Conclusion.** Retry aggregation can turn one trace into radically different but non-interchangeable SLIs.

### Example 4

**Situation.** Region A has 990 good of 1,000 valid events; region B has 45 of 50; region C has 1 of 10.

**Reasoning.** Event-weighted aggregate is $(990+45+1)/(1{,}000+50+10)=1{,}036/1{,}060=97.736\%$. Equal-region mean is $(99\%+90\%+10\%)/3=66.333\%$. The first describes a random valid event; the second assigns regions equal importance and exposes C's severe harm.

**Conclusion.** Publish counts and cohort values; choose weights from the question, not convenience.

### Example 5

**Situation.** Six intended eligible events contain three good, two bad, and one unknown outcome.

**Reasoning.** The observed ratio among evaluable events is $3/5=60\%$ and coverage is $5/6=83.33\%$. If the unknown is otherwise represented exactly once, the true ratio lies between $3/6=50\%$ and $4/6=66.67\%$.

**Conclusion.** A point estimate without coverage hides important evidence uncertainty.

### Example 6

**Situation.** A service is good for 59 of 60 minutes. The bad minute occurs at peak and contains 2,000 failed requests; each other minute has 10 good requests.

**Reasoning.** Equal-minute time SLI is $59/60=98.33\%$. Request SLI is $590/(590+2{,}000)=22.78\%$ if all peak-minute requests are bad. Time weighting says failure was brief; demand weighting says most observed requests failed.

**Conclusion.** Time and request indicators represent different populations and can legitimately diverge.

### Example 7

**Situation.** Two replicas report p99 latency of 100 ms and 1,000 ms. The first served 99,000 requests; the second served 1,000.

**Reasoning.** Averaging p99s gives 550 ms, but it does not determine the combined p99. The combined rank depends on each full distribution: the slow replica's observations may occupy exactly the worst 1%, or its distribution may overlap the first. Compatible histogram counts or raw observations are needed.

**Conclusion.** Quantiles are not additive statistics; retain an aggregatable distribution.

### Example 8

**Situation.** A server reports 99.99% successful completions, while a matched client cohort reports 99.5% usable responses.

**Reasoning.** Joining operation IDs reveals 0.3% fail before reaching the server and 0.19% complete server-side but fail during transport or rendering. The residual 0.00% is rounding. The server indicator remains useful for its boundary but overstates the end-to-end journey by about 0.49 percentage points.

**Conclusion.** Measure the proxy gap instead of arguing that one boundary is universally correct.

### Example 9

**Situation.** A data pipeline publishes 900 of 1,000 records within ten minutes, 50 between ten and thirty minutes, 20 after thirty minutes, and loses 30.

**Reasoning.** With all ingested records eligible, the ten-minute freshness SLI is $900/1{,}000=90\%$. A thirty-minute indicator is $950/1{,}000=95\%$. Excluding lost records as “no completion timestamp” would inflate these to $900/970=92.78\%$ and $950/970=97.94\%$.

**Conclusion.** Select the denominator at ingestion so missing completions remain service failures rather than disappearing.

### Example 10

**Situation.** A counter reset causes a query to derive 1,020 good events from 1,000 valid events during a deployment.

**Reasoning.** The ratio 102% violates $G\subseteq V$. Clamping it to 100% conceals incompatible reset handling or filters. Recompute increases with reset-aware counter semantics, verify that numerator and denominator share instance and window coverage, and compare raw points around deployment.

**Conclusion.** An impossible ratio is a failed measurement invariant, not extraordinary service.

## Cross-Program Connections

1. [STQE-001](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) connects oracle design and controlled fixtures to indicator validation.
2. [SARCH-001](../../12-software-engineering-software-architecture/ROADMAP.md) connects user journeys and observation boundaries to service architecture.
3. [API-001](../../28-api-and-service-engineering/ROADMAP.md) connects protocol outcomes, logical operations, retries, and API contracts.
4. [DE-001](../../19-data-engineering/ROADMAP.md) connects event time, freshness, completeness, and delayed reconciliation to pipelines.
5. [DBE-001](../../18-database-engineering/ROADMAP.md) connects correctness predicates and durable acknowledgment to database behavior.
6. [DARCH-001](../../20-data-architecture-engineering/ROADMAP.md) connects semantic ownership and quality dimensions to governed indicators.
7. [PLAT-001](../../29-platform-engineering/ROADMAP.md) connects reusable SLI templates and telemetry schemas to platform products.
8. [SEC-001](../../25-security-engineering/ROADMAP.md) connects abuse classification, authorization outcomes, privacy, and adversarial denominator manipulation.
9. [SYSENG-001](../../26-systems-engineering/ROADMAP.md) connects measurement error, coverage, and proxy models to systems evidence.
10. [DSE-001](../../17-data-structures-engineering/ROADMAP.md) connects streaming counters, histograms, and mergeable summaries to data structures.

## References

1. Jones, C., Wilkes, J., Murphy, N. R., and Smith, C. “Service Level Objectives.” *Site Reliability Engineering*. O'Reilly/Google, 2016. <https://sre.google/sre-book/service-level-objectives/>. Retrieved 2026-09-06.
2. Sloss, B. T., and others. “Implementing SLOs.” *The Site Reliability Workbook*. O'Reilly/Google, 2018. <https://sre.google/workbook/implementing-slos/>. Retrieved 2026-09-06.
3. Prometheus Authors. “Histograms and Summaries.” Prometheus documentation. <https://prometheus.io/docs/practices/histograms/>. Retrieved 2026-09-06.
4. OpenTelemetry Authors. “Metrics Data Model.” OpenTelemetry Specification 1.60.0, current specification. <https://opentelemetry.io/docs/specs/otel/metrics/data-model/>. Retrieved 2026-09-06.
5. OpenTelemetry Authors. “Metrics API.” OpenTelemetry Specification 1.60.0, current specification. <https://opentelemetry.io/docs/specs/otel/metrics/api/>. Retrieved 2026-09-06.
6. Fielding, R., Nottingham, M., and Reschke, J., eds. *HTTP Semantics*. RFC 9110, STD 97, June 2022. <https://www.rfc-editor.org/rfc/rfc9110.html>. Retrieved 2026-09-06.
7. Google. “Monitoring Distributed Systems.” *Site Reliability Engineering*. O'Reilly/Google, 2016. <https://sre.google/sre-book/monitoring-distributed-systems/>. Retrieved 2026-09-06.
8. Prometheus Authors. “The Zen of Prometheus.” Prometheus documentation. <https://prometheus.io/docs/practices/the_zen/>. Retrieved 2026-09-06.

## Exercises

### Exercise 1

Define SLI, intended population, eligibility, evaluability, goodness, measurement point, window, coverage, proxy, and unknown. Explain why an objective is not part of the SLI definition.

### Exercise 2

A service observes 4,800 good, 120 bad, 60 unknown, and 20 governed exclusions among 5,000 arrivals. Compute the observed ratio, coverage among intended eligible events, lower and upper bounds, and exclusion rate. State the assumptions behind the bounds.

### Exercise 3

A mobile operation may retry twice. Design separate attempt-level and logical-operation availability and latency indicators. Include deduplication, terminal outcome, cancellation, deadline, missingness, and client/server measurement.

### Exercise 4

Compare request-based and five-minute time-slice indicators for a ticketing service with sharp on-sale peaks. Choose a primary indicator, an important companion, and partitions. Explain how each can mislead.

### Exercise 5

Transfer the measurement model to a wildfire-warning pipeline that ingests sensors, validates readings, computes risk, and sends alerts. Specify two SLIs, their populations, predicates, boundaries, unknown handling, and validation without claiming public-safety certification.

## Answers to the Exercises

### Answer 1

An SLI is a carefully specified quantitative measure of delivered service. The intended population is everything the claim aims to cover; eligibility selects contract-relevant units; evaluability means required evidence exists; goodness is the acceptable-outcome predicate. The measurement point says where and when observation occurs, and the window selects aggregation time. Coverage is evaluable eligible units divided by intended eligible units. A proxy measures a correlated observable rather than the valued property itself. Unknown preserves an eligible unit that cannot be judged. An SLO supplies a target for an SLI; putting the target into the indicator would couple measurement mechanism to reliability policy and obscure changes to either.

### Answer 2

Intended eligible events are $5{,}000-20=4{,}980$. Evaluable events are $4{,}800+120=4{,}920$. The observed ratio is $4{,}800/4{,}920=97.561\%$. Coverage is $4{,}920/4{,}980=98.795\%$. The lower bound is $4{,}800/4{,}980=96.386\%$ and the upper bound $(4{,}800+60)/4{,}980=97.590\%$. Exclusions are $20/5{,}000=0.4\%$ of arrivals. Bounds assume every intended eligible event is represented exactly once, the 60 unknowns are the only unclassified eligible outcomes, and each must ultimately be good or bad under the same predicate.

### Answer 3

Attempt availability uses every transmitted attempt as denominator and classifies protocol plus domain outcome at the client; attempt latency runs from send to usable attempt result or deadline. Logical availability deduplicates by a stable operation ID and waits for one terminal state: correct eventual success, exhausted failure, explicit user cancellation classified by governed policy, or unknown after the observation horizon. Logical latency runs from first user action through terminal usable result, including retry backoff. Preserve attempt count and join it to the logical operation. Compare client and server records; server absence remains an observed client-side failure or unknown according to evidence, not an exclusion. Track missing joins and coverage separately.

### Answer 4

For ticket purchase, make request-based correct-and-before-deadline completion primary because peak demand represents most user attempts. Use a five-minute good-slice indicator as a companion to expose duration and recovery; require a minimum probe or request count and classify no-data explicitly. Partition by on-sale event, region, client class, and bounded operation while retaining global counts. Request weighting can make quiet continuous failures look small and can be distorted by retries. Time weighting gives a quiet interval the same weight as a peak and can hide massive brief harm. Neither percentage should replace cohort counts or coverage.

### Answer 5

First, a freshness-and-validity SLI uses each authenticated sensor reading accepted at ingress as the intended event. It is good when identity, range, sequence, and required quality checks pass and the reading becomes available to the risk computation within its hazard-specific deadline. Missing completion is bad after the deadline; corrupt joins are unknown and bounded separately. Measure ingress event time to durable risk-input availability. Second, an alert-delivery SLI uses each validated risk decision requiring notification. It is good when the correct alert reaches every required channel or acknowledged recipient class before its deadline; partial delivery is classified by a predefined predicate, and absent delivery evidence is unknown or conservatively bad by policy. Validate with controlled sensor fixtures, clock-skew cases, duplicates, channel failures, end-to-end drills, and reconciliation against authoritative logs. This is a measurement design, not proof of safety, effectiveness, regulatory compliance, or certification.
