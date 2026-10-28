---
module_id: SDRE-039
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 39
title: Telemetry Sampling and Cost
status: complete
last_verified: 2026-09-06
---

# Telemetry Sampling and Cost

## One-Page Review

### Governing question

How can a team reduce telemetry production, transport, processing, and storage cost while preserving enough known evidence—and enough information about what was lost—to support valid operational decisions?

### Essential definitions

- **telemetry unit** is the object considered for selection: measurement, log record, span, whole trace, exemplar, profile sample, or another declared unit;
- **sampling frame** is the population of eligible units from which selection occurs;
- **inclusion probability** $\pi_i$ is the probability that eligible unit $i$ is retained under the design;
- **weight** $w_i=1/\pi_i$ represents how many population units a retained unit stands for when design-based estimation applies;
- **uniform probability sampling** gives eligible units the same inclusion probability $p$;
- **stratified sampling** partitions the frame and selects under a declared probability within each stratum;
- **head sampling** decides before the complete trace outcome is known;
- **tail sampling** delays the trace decision until enough spans or time have arrived;
- **targeted retention** keeps units because of content, such as errors or high latency, and is not a representative sample unless probabilities and weights are known;
- **filtering** deterministically removes declared classes; **aggregation** combines measurements into summaries;
- **rate limiting** caps accepted volume based on time or capacity and can create load-dependent loss;
- **exemplar** is a selected measurement-linked record that connects an aggregate to detailed context;
- **selection provenance** records unit, frame, policy version, probability, decision point, and known loss;
- **logical volume** is encoded telemetry before compression and replication; **physical retained volume** includes storage duration, compression, indexes, and copies.

### Central model, mechanism, or theorem

For eligible units $i=1,\ldots,N$ with known inclusion probabilities $0<\pi_i\le1$, the expected retained count is

$$
E[n_s]=\sum_{i=1}^{N}\pi_i.
$$

For a population total $T=\sum_i y_i$, the Horvitz–Thompson estimator

$$
\widehat T=\sum_{i\in S}\frac{y_i}{\pi_i}
$$

is design-unbiased when selection follows the declared probabilities: $E[\widehat T]=T$. A naive aggregate over a content-biased sample generally does not estimate the population aggregate.

An initial physical storage estimate is

$$
C_v=qbs\,Rcr,
$$

where $q$ is units per second, $b$ logical bytes per unit, $s$ seconds per day, $R$ retention days, $c$ stored-to-logical compression/index factor, and $r$ physical copy factor. Every variable needs measurement rather than wishful defaults.

### Critical invariants

- name the sampling unit, eligible population, decision point, and policy version;
- preserve a whole-trace decision across services when whole traces are the analysis unit;
- never interpret a targeted sample as representative without a valid weighting design;
- keep inclusion probability or equivalent threshold with retained data when estimating populations;
- distinguish absent because nonexistent from absent because filtered, sampled, rejected, or dropped;
- protect rare critical classes only with bounded cardinality and capacity assumptions;
- treat metric aggregation and dimension control as semantics, not random event deletion;
- monitor the telemetry pipeline's accepted, sampled, rejected, dropped, delayed, and overflowed volume;
- include collection and query cost, not storage price alone;
- version policy changes so comparisons do not silently cross selection regimes.

### Common failures

Failures include sampling spans independently and producing broken traces, sampling after discarding the probability, keeping every error until an error storm overloads the pipeline, deriving an error rate naively from error-biased traces, dropping low-severity logs before security or incident requirements are known, attaching unbounded tenant or request identifiers to metrics, calling deterministic filtering “random sampling,” assuming compression and indexes are free, scaling collectors without scaling the saturated backend, routing one trace across several tail samplers, adapting rates without recording the rate, and treating a retained example as proof that a behavior is common.

### Compact example

A service emits 20,000 trace records per second at 500 logical bytes each. Uniform 10% selection yields an expected 86.4 GB of logical data per day. Seven days of retention at a measured stored-to-logical factor of 0.4 and two physical copies yields $86.4\times7\times0.4\times2=483.84$ GB. The policy keeps a deterministic, consistent subset by trace identity, records $p=0.1$, monitors pre- and post-selection counts, and separately reserves bounded capacity for rare error traces. Estimates use weights; diagnostic searches disclose targeted retention and possible missing traces.

### Connections

[SDRE-033](033-metrics-and-dimensionality.md) supplies metric aggregation, [SDRE-034](034-distributed-tracing.md) supplies trace structure, [SDRE-036](036-correlation-and-context-propagation.md) supplies propagated decisions, and [SDRE-038](038-alerting-and-actionability.md) supplies consequence-led monitoring. [SDRE-040](../ROADMAP.md) next integrates a coherent diagnostic instrumentation design.

## Governing Question

Full-fidelity telemetry is attractive because future questions are unknown. It is also finite systems work: applications allocate records, networks carry them, collectors parse and queue them, processors transform them, indexes amplify them, storage retains copies, and people search them. Under burst load, an unbounded telemetry path can compete with the service it is meant to observe.

Reducing volume is therefore necessary in many systems, but every reduction changes evidence. Random selection can support population estimates when its design is known. Content-based retention is useful for diagnosis but distorts prevalence. Aggregation preserves declared summaries while removing individual events. Filtering can remove known noise but makes discarded questions impossible. Rate limiting protects capacity while losing evidence exactly when load is high.

The governing question joins statistical validity and systems safety: which unit and population matter, which future decisions must remain possible, what loss can be tolerated, where should the decision occur, what will it cost, and how will investigators know what they cannot see?

## Why This Matters

OpenTelemetry describes sampling as a control on tracing noise and overhead and distinguishes early head decisions from later tail decisions based on more complete trace information [1]. Its Trace SDK specifies recording and sampled state, built-in sampling behavior, and the propagation implications of a sampled flag [2]. The current probability-sampling specification adds threshold and randomness information intended to make probabilities composable and interpretable [3].

The W3C Trace Context Level 2 candidate recommendation defines interoperable sampled and random trace flags while warning that inconsistent component decisions can fragment traces [4]. These flags communicate context; they do not promise that every downstream system stored every span.

Tail sampling buys richer decisions by buffering and correlating spans. Current OpenTelemetry Collector scaling guidance notes that stateful processors need trace-consistent routing; distributing one trace across independent tail samplers can produce inconsistent decisions and missing spans [5]. Collector capacity and backend capacity remain separate constraints.

Metrics need a different model. Current OpenTelemetry Metrics SDK guidance defines cardinality limits and an overflow aggregation so measurements are represented without pretending every attribute set remains independently queryable [6]. Logs have record bodies, timestamps, severity, trace context, resources, and attributes whose meaning should survive any declared filter [7]. The Dapper paper remains a useful primary account of sampling as part of a low-overhead, ubiquitous production tracing design [8].

## Prerequisites and Retrieval

Retrieve event, log record, metric measurement, metric stream, span, trace, trace context, attribute, cardinality, histogram, aggregation, population, sample, probability, expectation, bias, variance, estimator, throughput, latency, queue, backpressure, compression, index, replication, retention, confidentiality, incident, and service-level indicator.

From SDRE-033 retrieve why metric identity and aggregation control query meaning. From SDRE-034 retrieve trace completeness, parent-child structure, clocks, and critical-path limits. From SDRE-036 retrieve propagation boundaries and trust. From SDRE-038 retrieve missing-evidence behavior and telemetry-pipeline alerts.

## Learning Objectives

After completing this module, you should be able to:

1. declare a sampling unit, frame, decision point, and inclusion policy;
2. distinguish sampling, filtering, aggregation, rate limiting, and retention;
3. explain head, parent-consistent, and tail trace sampling;
4. compute expected retained volume and a first-order storage estimate;
5. use inclusion weights for a population total under a valid design;
6. identify bias from targeted error, latency, tenant, or release retention;
7. design bounded protection for rare diagnostic evidence;
8. reason about logs, metrics, traces, and exemplars differently;
9. test selection determinism, capacity, policy change, and failure behavior;
10. govern telemetry value, cost, privacy, and loss as one lifecycle.

## Core Exposition

**Start from decisions, not a universal percentage.** List the operational questions telemetry must support: alert evaluation, release comparison, incident reconstruction, performance distribution, dependency diagnosis, security investigation, capacity planning, and compliance. Each question implies a unit, required fields, time horizon, latency, and acceptable error.

An SLI computed from a metric counter may require complete aggregation but not every request record. A rare protocol failure may require full trace structure. Debug logs may be valuable for minutes and useless after a release stabilizes. Security records may have stricter retention and access rules. One sampling policy cannot preserve all these uses.

Define the **frame** before selection. “Sample 5%” is incomplete: 5% of incoming root traces, spans at each service, accepted collector batches, stored log records, or metric measurements? State environment, services, operations, tenants, time, and exclusion rules. Units omitted before the frame is observed have inclusion probability zero and cannot be recovered by later weighting.

**Distinguish reduction mechanisms.** Probability sampling selects units according to a known randomized or deterministic-probability design. Deterministic consistent selection can use a sufficiently random trace identifier and a threshold so the same trace decision is honored across components [2–4]. Repeatability is useful, but a deterministic rule is representative only if its input randomness assumptions hold.

Filtering removes a declared class: health-check success logs, for example. It is appropriate when the class is known to have no retained use, but it gives those records $\pi=0$ for later questions. Aggregation maps many measurements to a sum, count, histogram, maximum, or other declared summary. It preserves only properties supported by that aggregation. Rate limiting accepts at most a capacity over time; selection then depends on arrival order and load and is rarely a uniform sample.

Retention limits how long already accepted data remains. Compression changes physical bytes, not logical evidence. Attribute truncation changes detail. Redaction changes sensitive content. These controls can coexist, but record their order because filter-then-sample and sample-then-filter produce different counts, costs, and probabilities.

**Model cost by pipeline stage.** Measure produced units and bytes, application CPU and allocation, export bytes, collector receive and send volume, queue occupancy, processing CPU and memory, rejected and dropped units, backend ingest, index amplification, retained physical bytes, query scans, cache, and egress. A low storage bill can hide high application or query cost.

For rate $q$, average logical size $b$, seconds per day $s=86{,}400$, selection fraction $p$, retention $R$, stored-to-logical factor $c$, and physical copies $r$, an initial estimate is $qbp sRcr$. Here $c$ may be below one with compression or above one after indexes and metadata. Measure it for each signal and backend. Replication, erasure coding, backup, and hot/cold tiers need separate accounting if one factor hides important choices.

Work from percentiles and bursts, not just mean rate. A deployment, retry storm, or incident can increase event size and volume together. Budget ingress, queue memory, CPU, and storage under credible bursts. If telemetry backpressure reaches the application, decide whether to drop telemetry, shed diagnostic detail, spool locally, or risk service latency; document the safety priority.

The executable model below uses a 32-bit suffix only as controlled input to illustrate a threshold decision. Production trace identifiers must satisfy the randomness and consistency assumptions of the applicable specification [3, 4]. Decimal GB means $10^9$ bytes.

<!-- bijux-verify: {"id":"sampling-volume-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"kept: ['10000000']\nsampled raw per day: 86.40 GB\nretained physical: 483.84 GB\n","stderr":""}} -->
```python
trace_ids = ["10000000", "50000000", "90000000", "d0000000"]
probability = 0.25
threshold = int(probability * 2**32)
kept = [trace_id for trace_id in trace_ids if int(trace_id, 16) < threshold]

rate_per_second = 20_000
bytes_per_record = 500
pipeline_fraction = 0.10
days = 7
stored_to_logical = 0.40
copies = 2

daily = rate_per_second * bytes_per_record * 86_400 * pipeline_fraction
physical = daily * days * stored_to_logical * copies
print("kept:", kept)
print(f"sampled raw per day: {daily / 1e9:.2f} GB")
print(f"retained physical: {physical / 1e9:.2f} GB")
```

Exactly one of four evenly placed controlled identifiers falls below the 25% threshold. That tiny fixture tests boundary logic, not statistical representativeness. The separate volume policy retains 10% and estimates 86.4 GB logical per day, then 483.84 GB physical over seven days under the measured factors.

**Use design information for estimation.** Let indicator $I_i=1$ if unit $i$ is included and zero otherwise. Since $E[I_i]=\pi_i$,

$$
E\left[\sum_i \frac{I_i y_i}{\pi_i}\right]
=\sum_i \frac{E[I_i]y_i}{\pi_i}
=\sum_i y_i=T.
$$

This proves design unbiasedness of the total estimator under known positive inclusion probabilities. It does not guarantee a small error in one realized sample, independence, correct frame coverage, or absence of measurement error. Uncertainty depends on the design and joint inclusion probabilities.

Uniform sampling with probability $p$ gives weight $1/p$. Stratified sampling may keep 100% of rare critical operations and 1% of routine operations; estimates then use each unit's stratum probability. Store policy version, stratum, and effective probability or threshold with the data. If adaptive logic changes probabilities under load without recording them, later estimation becomes unreliable.

Targeted retention answers “show me valuable examples,” not “how common is this?” Keeping all errors and 1% of successes makes errors dominant in the retained set. Weighting can estimate a rate only if the eligibility, classification timing, and probabilities are known. Tail rules based on final latency or error are content-dependent strata, not magic immunity from bias.

**Choose the trace decision point.** Head sampling decides at or near trace start. It is cheap, limits recording and export early, and can propagate a consistent parent decision. It cannot know downstream error, final duration, or later attributes [1, 2]. Root decisions should remain coherent across service boundaries unless a documented policy deliberately changes them.

Tail sampling waits for most or all spans and can prioritize errors, latency, release, or rare attributes [1]. It must buffer spans, decide when a trace is complete despite late or missing data, and keep all spans for a trace at a compatible decision point. Memory is roughly arrival rate times decision wait times bytes held per trace, before runtime and indexing overhead.

At 50,000 traces/s, an 8-second decision wait, 12 spans/trace, and 500 encoded bytes/span requires $50{,}000\times8\times12\times500=2.4$ GB of span payload in flight. Skew, late spans, queues, object overhead, and copies raise the requirement. Trace-aware routing is essential when scaling stateful collectors [5].

Hybrid policies may head-sample routine traffic to protect ingress and then tail-select among what remains. Tail sampling cannot recover traces already dropped at the head. A policy that says “tail keeps every error” is false if head selection removed errors before their outcomes were known.

**Handle partial traces honestly.** The propagated sampled flag indicates a recording decision, not confirmed backend completeness [2, 4]. Components can be uninstrumented, propagation can fail, exporters can reject, queues can overflow, and tail windows can close before late spans. Record dropped counts, export failures, accepted spans, incomplete-trace indicators, and policy versions. A trace UI should disclose gaps rather than draw invented edges.

Do not sample spans independently when queries assume a whole request. Independent 10% span selection across ten required spans retains a complete trace with probability $0.1^{10}=10^{-10}$ under independence. Span-level selection can be valid for a span population question, but not for full-path diagnosis.

**Treat logs by event value and obligations.** Begin with structured severity, event kind, service, environment, operation, privacy class, and trace context [7]. Remove duplicates and known high-volume noise at the source when safe. Rate-limit repeated messages with suppressed-count summaries so investigators know loss occurred. Never discard audit or security records merely because their severity label is low; use the governing retention and access policy.

Probability-sampled logs can estimate counts if the frame and probability are recorded. Content-based filters are often more useful operationally but must be disclosed. Burst rate limits protect pipelines yet preferentially lose incident-time evidence. Reserve bounded capacity for critical classes, emit drop counters outside the congested path, and test adversarial high-cardinality messages.

**Treat metrics as aggregates.** Metrics already summarize measurements by instrument, attributes, temporality, and aggregation. Randomly dropping counter updates changes totals unless weighting or aggregation semantics explicitly compensate. Prefer controlling attributes, views, histogram buckets, collection interval, and aggregation rather than sampling metric points blindly.

Cardinality is the number of distinct attribute combinations. A limit protects memory but merges or omits detail according to the implementation. Current OpenTelemetry Metrics SDK guidance uses an overflow attribute set so measurements beyond the limit remain in one aggregate while per-attribute queries lose detail [6]. Monitor overflow and never interpret missing series as zero.

Exemplars link selected measurements to detailed trace or context. They are examples from an aggregate, not the distribution itself. A slow exemplar proves at least one slow operation existed; it does not estimate the slow-operation rate without a sampling design.

**Protect rare value without unbounded promises.** “Keep all errors” can overload the pipeline during the very failure being diagnosed. Use capacity reservations, per-class budgets, priority queues, bounded buffers, and explicit degradation. For example: reserve a fixed error-trace budget, sample above it with a recorded probability, retain aggregate error counts independently, and surface dropped-error counts.

Stratify by stable, bounded characteristics that exist at the decision point. Per-tenant guarantees can explode state with adversarial tenant identifiers. Hash-bucket large populations, cap strata, aggregate overflow, and give genuinely critical classes explicit ownership. Fairness is a policy: equal samples per tenant, proportional samples, and minimum guarantees answer different questions.

**Govern policy change and evidence lineage.** Store a stable policy identifier and effective interval. Record selectors, probabilities, thresholds, priority rules, caps, decision location, software version, and fallback behavior. A dashboard spanning a rate change must either weight intervals correctly or partition the comparison.

Review telemetry using value and cost: which alerts, diagnoses, audits, or decisions used it; which fields were queried; which classes were dropped; what blind spots appeared; and what application, pipeline, backend, and human costs resulted. Absence of queries is evidence, not automatic permission to delete rare emergency data.

Test deterministic decisions against fixed identifiers and threshold boundaries. Test statistical selection over seeded controlled populations without treating one run as proof. Test probability metadata, parent consistency, late spans, incomplete traces, collector redistribution, queue overflow, backend rejection, policy rollback, clock error, cardinality attack, privacy redaction, and dual-policy intervals. Verify that cost controls do not disable the counters needed to observe their own loss.

## Definitions and Notation

Let $U=\{1,\ldots,N\}$ be the finite eligible telemetry population for a declared interval and $S\subseteq U$ the retained sample. Unit $i$ has measured value $y_i$, inclusion indicator $I_i$, and first-order inclusion probability $\pi_i=P(I_i=1)$. Design-based weighting requires $0<\pi_i\le1$ for every unit represented by the estimate.

The population total is $T=\sum_{i\in U}y_i$ and the Horvitz–Thompson estimate is $\widehat T=\sum_{i\in S}y_i/\pi_i$. For uniform Bernoulli sampling, $\pi_i=p$ and $E[|S|]=Np$. A selected diagnostic subset with unknown probabilities is denoted $D$ rather than falsely calling it a representative sample.

For volume, let $q$ be eligible units/s, $b$ mean logical bytes/unit, $p$ retained fraction, $s=86{,}400$ s/day, $R$ days, $c$ physical stored bytes per retained logical byte, and $r$ copy factor. The estimate $qbp sRcr$ assumes stationary averages and omits fixed and query-dependent costs.

For tail buffering, let $\lambda$ be traces/s, $w$ decision wait, $m$ mean spans/trace, and $b_s$ mean bytes/span. Payload in flight is approximately $B=\lambda w m b_s$ under stable arrival and bounded means.

## Mechanisms, Invariants, or Proof Structure

**Estimator proof.** Write $\widehat T=\sum_i I_i y_i/\pi_i$. Linearity of expectation and $E[I_i]=\pi_i$ yield $E[\widehat T]=\sum_i y_i=T$. Independence is unnecessary for unbiasedness of the total, but variance calculation needs the selection design and joint probabilities.

**Zero-probability boundary.** If a represented unit has $\pi_i=0$, $y_i/\pi_i$ is undefined and the unit can never contribute. Therefore no weighting scheme reconstructs a class excluded from the frame. Claims must be restricted to positive-probability units.

**Whole-trace invariant.** If the analysis unit requires every one of $k$ spans and spans are retained independently with probability $p$, complete retention probability is $p^k$. For $0<p<1$ and $k>1$, $p^k<p$. A trace-consistent decision retains complete eligible traces with probability near $p$, subject to propagation and pipeline loss.

**Tail-state lower bound.** A tail decision cannot use an outcome attribute before that attribute arrives. It must hold earlier spans or external state until a decision deadline. Thus later information necessarily trades earlier resource release for richer selection.

**Cost monotonicity.** In the simple positive-factor model, increasing $q,b,p,R,c,$ or $r$ while holding others fixed cannot reduce estimated physical volume. This does not imply reducing any one factor is semantically safe.

**Biased-subset argument.** When inclusion probability depends on $y_i$, the unweighted sample mean is generally centered on the selected distribution rather than the population. Targeted retention must be treated as diagnostic evidence or corrected with a valid design and weights.

## Alternatives and Trade-Offs

**Full capture versus reduction.** Full capture preserves the most potential detail and can threaten service and telemetry capacity. Reduction bounds cost and creates known or unknown blind spots. Use full capture for bounded critical populations, not as an unmeasured default.

**Head versus tail trace sampling.** Head decisions are early, cheap, and propagation-friendly; they cannot see final outcomes. Tail decisions use richer evidence but require state, trace-aware routing, completion heuristics, and fallback behavior.

**Uniform versus stratified probability.** Uniform selection is simple and supports broad estimates. Stratification protects rare classes and can improve precision, but it needs stable strata, probability metadata, and weighted queries.

**Probability sampling versus targeted retention.** Probability designs support estimation. Targeting keeps diagnostically valuable cases. A dual stream can provide a representative baseline plus a clearly marked diagnostic subset.

**Source versus collector versus backend reduction.** Early reduction saves downstream cost but cannot use later context and makes loss irreversible. Later reduction has richer information but pays earlier production and transport cost.

**Drop versus aggregate.** Dropping removes evidence. Aggregation preserves selected summaries but removes individual structure. Choose from future query requirements, not implementation convenience.

**Fixed versus adaptive rates.** Fixed rates are explainable and comparable but may fail under bursts. Adaptive rates protect capacity but create time- and load-dependent probabilities that must be exported and used.

**Long versus short retention.** Long retention supports seasonal, security, and regression analysis at higher cost and exposure. Tiering, aggregation, and selective retention can preserve specific uses without keeping all detail hot.

**Central versus per-tenant budgets.** Central budgets maximize pooled utilization but noisy tenants can dominate. Per-tenant guarantees improve isolation and add state, fairness choices, and cardinality risk.

## Failure Modes and Misconceptions

1. **“Five percent means representative.”** Representation depends on the frame, randomness assumptions, loss, and known inclusion probabilities.
2. **“Deterministic means biased.”** A threshold over sufficiently random identifiers can implement probability sampling; deterministic selection over correlated IDs can be biased.
3. **“Tail sampling sees every error.”** It cannot recover head-dropped traces or spans lost before the decision.
4. **“The sampled flag proves complete storage.”** It communicates a decision, not successful end-to-end retention.
5. **“Sampling spans is equivalent to sampling traces.”** Independent span decisions fragment whole-trace evidence.
6. **“Keep all errors is safely bounded.”** Error storms can turn the exceptional class into the dominant load.
7. **“A sampled error ratio is the service error ratio.”** Targeted selection changes the denominator unless valid weights restore it.
8. **“Rate limiting is random sampling.”** It usually favors earlier arrivals and loses more during bursts.
9. **“Metrics should be sampled like logs.”** Metric updates participate in aggregations and temporality; blind deletion changes semantics.
10. **“Overflow preserves every grouped query.”** It preserves an aggregate while losing independent attribute-set detail.
11. **“Compression removes cost proportionally everywhere.”** It does not remove application CPU, network ingress, indexing, or query scans.
12. **“Average event size is enough.”** Size and rate may rise together during incidents; tails and bursts determine capacity.
13. **“More collectors solve telemetry overload.”** A saturated network or backend can be harmed by more senders [5].
14. **“Adaptive sampling needs no lineage.”** Unrecorded rate changes invalidate comparisons and weights.
15. **“An exemplar establishes prevalence.”** It demonstrates one selected case, not its population frequency.
16. **“Unused telemetry has no value.”** Rare incident, audit, or security value requires risk-based review, not query counts alone.

## Worked Examples

### Example 1

**Estimate retained storage.** A pipeline receives 20,000 records/s at 500 logical bytes, retains 10%, keeps seven days, stores 0.4 physical bytes per logical byte after compression and indexes, and maintains two copies. Daily selected volume is $20{,}000\times500\times86{,}400\times0.1=86.4$ GB. Physical retained volume is $86.4\times7\times0.4\times2=483.84$ GB. **Conclusion:** declared factors make the estimate reviewable, but measured bursts and fixed/query cost remain outside it.

### Example 2

**Check a threshold boundary.** With 32-bit values and $p=0.25$, threshold is $0.25\times2^{32}=1{,}073{,}741{,}824=0x40000000$. Values strictly below it are retained; the value equal to it is not under the stated comparison. **Conclusion:** deterministic sampling needs an exact bit width, comparison, and boundary test.

### Example 3

**Estimate a population total.** A 10% uniform sample contains request byte values 200, 400, and 500. The weighted total estimate is $(200+400+500)/0.1=11{,}000$ bytes for the frame. This is unbiased over repeated designs, not guaranteed equal to the realized population total. **Conclusion:** weights support a bounded statistical claim, not certainty from one sample.

### Example 4

**Correct targeted error retention.** A population has 100 errors and 9,900 successes. Policy retains all errors and 1% of successes; suppose it retains 99 successes. The naive sample ratio is $100/199=50.3\%$. Weighted counts are $100/1=100$ errors and $99/0.01=9{,}900$ successes, so the estimate is $100/10{,}000=1\%$. **Conclusion:** content-biased samples require known stratum probabilities and weighted queries.

### Example 5

**Expose a zero-probability class.** A source filter deletes every successful health-check log before the sampling frame. Later, an investigator asks whether health checks preceded a failure. Those records have inclusion probability zero and cannot be reconstructed or weighted. **Conclusion:** filtering is an irreversible scope decision, not cheap random sampling.

### Example 6

**Size a tail buffer.** At 50,000 traces/s, eight seconds of wait, 12 spans/trace, and 500 bytes/span, payload is $50{,}000\times8\times12\times500=2.4$ GB. If runtime objects double payload and two copies coexist during batching, a rough working amount becomes 9.6 GB before skew. **Conclusion:** tail policy is also stateful capacity engineering.

### Example 7

**Quantify trace fragmentation.** Ten required spans are independently kept at 10%. Under independence, complete-trace probability is $0.1^{10}=10^{-10}$, or one in ten billion. A consistent whole-trace 10% decision aims to retain all instrumented spans for about one in ten traces. **Conclusion:** choose the selection unit from the query unit.

### Example 8

**Respond to metric cardinality overflow.** A request ID is accidentally attached to a counter. The SDK limit aggregates excess attribute sets into an overflow series. The overall sum can remain represented, while a query grouped by route and tenant can undercount or lose attribution. Remove request ID, retain bounded route and tier, and alert on overflow. **Conclusion:** aggregation safety does not preserve every dimension.

### Example 9

**Compare across a policy change.** Week A retains routine traces at 10%; Week B retains them at 2%. The dashboard shows 10,000 versus 3,000 stored traces and claims traffic fell 70%. Weighted estimates are 100,000 and 150,000 eligible traces, implying a 50% rise under the declared design. **Conclusion:** stored counts across policy versions are not directly comparable.

### Example 10

**Degrade during an error storm.** A policy promises all errors, but errors rise from 100/s to 200,000/s and exceed ingress. Reserve capacity for 5,000 error traces/s, then probability-sample overflow with an exported effective rate; retain independent metric counts; emit rejected and dropped counters through a protected path; and preserve a small representative success stream. **Conclusion:** bounded, visible degradation is more honest than an impossible completeness promise.

## Cross-Program Connections

1. [ALGE-001](../../16-algorithm-engineering/ROADMAP.md) connects reservoir, hashing, and streaming selection to algorithmic cost.
2. [DSE-001](../../17-data-structures-engineering/ROADMAP.md) connects bounded buffers, sketches, and indexes to retained evidence.
3. [DE-001](../../19-data-engineering/ROADMAP.md) connects sampling lineage, schema, partitioning, and late data to pipelines.
4. [DARCH-001](../../20-data-architecture-engineering/ROADMAP.md) connects hot/cold tiers, retention, governance, and analytical fitness.
5. [LSDS-001](../../21-large-scale-data-systems-engineering/ROADMAP.md) connects distributed ingestion, backpressure, compaction, and query cost.
6. [DIST-001](../../27-distributed-systems-engineering/ROADMAP.md) connects trace routing, partial failure, duplication, and missing spans to distributed semantics.
7. [SEME-001](../../10-software-engineering-methods-and-evolution/ROADMAP.md) connects policy change, cost evidence, and feedback to engineering evolution.
8. [SEC-001](../../25-security-engineering/ROADMAP.md) connects audit retention, sensitive attributes, adversarial volume, and access control.
9. [PLAT-001](../../29-platform-engineering/ROADMAP.md) connects telemetry budgets and default policies to platform guardrails.
10. [CLOUD-001](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) connects storage tiers, egress, replication, and resource capacity to cloud cost.

## References

1. OpenTelemetry Authors. “Sampling.” Current OpenTelemetry documentation, last modified October 16, 2025. <https://opentelemetry.io/docs/concepts/sampling/>. Retrieved 2026-09-06.
2. OpenTelemetry Authors. “Tracing SDK—Sampling.” OpenTelemetry Specification. <https://opentelemetry.io/docs/specs/otel/trace/sdk/>. Retrieved 2026-09-06.
3. OpenTelemetry Authors. “TraceState: Probability Sampling.” OpenTelemetry Specification. <https://opentelemetry.io/docs/specs/otel/trace/tracestate-probability-sampling/>. Retrieved 2026-09-06.
4. W3C Distributed Tracing Working Group. *Trace Context Level 2*. Candidate Recommendation Draft, March 28, 2024. <https://www.w3.org/TR/trace-context-2/>. Retrieved 2026-09-06.
5. OpenTelemetry Authors. “Scaling the Collector.” Current OpenTelemetry documentation, last modified July 17, 2026. <https://opentelemetry.io/docs/collector/scaling/>. Retrieved 2026-09-06.
6. OpenTelemetry Authors. “Metrics SDK—Cardinality Limits.” OpenTelemetry Specification. <https://opentelemetry.io/docs/specs/otel/metrics/sdk/>. Retrieved 2026-09-06.
7. OpenTelemetry Authors. “Logs Data Model.” OpenTelemetry Specification, stable. <https://opentelemetry.io/docs/specs/otel/logs/data-model/>. Retrieved 2026-09-06.
8. Sigelman, B. H., Barroso, L. A., Burrows, M., Stephenson, P., Plakal, M., Beaver, D., Jaspan, S., and Shanbhag, C. “Dapper, a Large-Scale Distributed Systems Tracing Infrastructure.” Google Research technical report, 2010. <https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/>. Retrieved 2026-09-06.

## Exercises

### Exercise 1

Define sampling unit, frame, inclusion probability, targeted retention, head sampling, tail sampling, aggregation, rate limiting, and selection provenance. Explain why “retain 5%” is incomplete.

### Exercise 2

A log pipeline receives 12,500 records/s at 800 logical bytes each, retains 4%, keeps 14 days, has a stored-to-logical factor of 0.55, and maintains three copies. Estimate daily selected logical GB and physical retained GB using decimal units.

### Exercise 3

A sample keeps all 40 failed operations and 2% of 4,000 successful operations; exactly 80 successes are retained. Compute the naive retained error ratio and the weighted population error-ratio estimate. State the assumptions.

### Exercise 4

Design a telemetry reduction policy for a payment service that needs user-impact metrics, representative performance trends, full evidence for a bounded fraud-review class, and detailed diagnosis for rare failures. Include overload degradation and policy lineage.

### Exercise 5

Transfer the model to wildlife acoustic sensors with intermittent satellite links. Researchers need species prevalence estimates and rare-call examples while battery, bandwidth, and storage are limited. Design the frame, selection, weighting, rare-event policy, loss evidence, and validation.

## Answers to the Exercises

### Answer 1

The sampling unit is the object selected; the frame is the declared eligible population. Inclusion probability is a unit's chance of retention. Targeted retention selects by content and is not automatically representative. Head trace sampling decides before the full outcome; tail sampling waits for later trace evidence. Aggregation maps many measurements to declared summaries. Rate limiting caps volume and usually creates arrival- and load-dependent loss. Selection provenance records unit, frame, policy, decision point, probability, and known loss. “Retain 5%” omits all of these semantics and cannot support a valid completeness, cost, or estimation claim.

### Answer 2

Selected bytes/day are $12{,}500\times800\times86{,}400\times0.04=34{,}560{,}000{,}000$ bytes, or **34.56 GB/day**. Physical retained volume is $34.56\times14\times0.55\times3=798.336$ GB, or **798.34 GB** rounded to two decimals. This stationary first-order estimate excludes bursts, application/export cost, fixed metadata, query scans, backup outside the copy factor, and variation in compression.

### Answer 3

The retained set contains 40 failures and 80 successes, so the naive ratio is $40/120=33.3\%$. Failure weight is $1/1=1$ and success weight is $1/0.02=50$. Weighted counts are 40 failures and $80\times50=4{,}000$ successes; the estimated ratio is $40/4{,}040=0.990\%$. This requires a complete frame, correct classification, all failures having probability 1, each success having probability 0.02 under the declared design, and no additional pipeline loss. Here the given population confirms the estimate exactly, but that is not guaranteed in general.

### Answer 4

Compute user-impact counters and histograms with bounded dimensions before detail reduction; do not sample away SLI semantics. Maintain a uniform trace stream with recorded probabilities for performance trends. Define a bounded, access-controlled fraud-review frame retained fully only while its explicit legal and capacity policy permits. Tail-select rare failures after a trace-consistent routing layer, while retaining a small representative baseline. Under overload, reserve class budgets, sample overflow with exported effective probability, keep aggregate accepted/dropped counts through an independent path, and fail without slowing payments. Store policy ID, interval, frame, strata, thresholds, software version, decision location, and fallback. Test errors, bursts, missing spans, rate change, privacy redaction, and backend rejection. Acceptable variants must preserve metrics, bounded critical retention, representative and diagnostic distinction, and visible loss.

### Answer 5

Define the frame as all analysable time windows at registered sensors during declared active periods, including a heartbeat inventory so silent sensors are not omitted. Use locally deterministic probability selection for ordinary clips and retain the probability, sensor, time, firmware, and selection policy. Weight ordinary selected windows by inverse inclusion probability when estimating prevalence, with stratification by habitat or season if declared in advance. A rare-call detector may retain higher-probability diagnostic examples, but those clips form a targeted stream and do not directly estimate prevalence. Cap rare-event storage and sample overflow visibly. Preserve compact counts for produced, classified, selected, queued, transmitted, expired, and dropped windows; distinguish no call from no sensor or no link. Validate with labeled controlled audio, seeded selection, threshold boundaries, disconnected operation, backlog expiry, clock drift, battery exhaustion, false rare detections, and independent field surveys. Evaluation rewards frame coverage, weighting, bounded rare-event protection, and honest missingness rather than a particular sampling rate.
