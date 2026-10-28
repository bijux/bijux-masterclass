---
module_id: API-097
program: API & Service Engineering
level: 2
module_number: 97
title: API Metrics, Logs, and Traces
status: complete
last_verified: 2026-09-02
---

# API Metrics, Logs, and Traces

## One-Page Review

### Governing question

How should an API expose metrics, logs, and traces that preserve protocol and product meaning across clients, gateways, meshes, services, and dependencies—without creating unbounded cost, leaking sensitive data, or mistaking telemetry for truth?

### Essential definitions

- A **metric** is an aggregated time series/distribution suited to rates, ratios, saturation, concurrency, and latency distributions.
- A **log** is a timestamped event record with structured attributes suited to discrete decisions, errors, audit-relevant facts, and diagnosis.
- A **trace** is a graph of spans representing causal work for a logical operation across process/service boundaries.
- A **span** records one bounded operation, its parent/links, timing, status, events, and low-cardinality attributes.
- A **resource** identifies the entity producing telemetry: service, version, instance, environment, region, and similar stable dimensions.
- **cardinality** is the number of distinct time series or attribute values; unbounded user/request/object identifiers do not belong in metric labels.
- **correlation context** joins telemetry safely using trace/span/request/operation identifiers; it is not authentication or authorization context.
- **sampling** selects telemetry records; head sampling decides early, tail sampling later with more outcome context.
- **telemetry health** measures instrumentation, buffering, export, processing, storage, query, and alert delivery itself.

### Central model, mechanism, or theorem

For requests classified by route template $r$, method $m$, outcome $o$, version $v$, and bounded tenant tier $t$, potential metric series scale approximately as

$$
S\le |R||M||O||V||T|\times B,
$$

where $B$ accounts for histogram buckets and auxiliary series. A raw path/user/order/request label can make a bounded product unbounded. Metrics locate population symptoms, traces explain sampled causal paths, logs record discrete evidence, and application/domain state remains authoritative. Their intersection supports diagnosis; no signal alone proves correctness or absence.

### Critical invariants

Telemetry starts from user/API outcomes and distinguishes logical operations from attempts/hops. Route labels use templates, status/error taxonomies are stable, units and histogram boundaries match SLOs, and metrics can aggregate across instances. Logs are structured, schema/versioned, severity-consistent, correlated, redacted and bounded. Traces propagate valid context across trusted boundaries, create correct client/server/producer/consumer spans, model retries/fan-out/queues/links, and avoid duplicate instrumentation.

Identity, token, body, query, headers, personal/payment/secret data are deny-by-default with approved allowlists, hashing/tokenization rules and retention/access controls. Incoming trace context is untrusted metadata: validate/regenerate as required and never authorize from it. Telemetry backpressure cannot take down the API. Export loss, sampling, clock skew and instrumentation gaps are visible. SLO, alert, dashboard and incident queries are tested against synthetic known outcomes.

### Common failures

Raw URL/user/order/request IDs as metric labels; averages hiding tails; averaging per-instance quantiles; buckets unrelated to SLO; counters used as gauges; status `500` as only error dimension; logical calls mixed with retry attempts; gateway/service double counting; one span per trivial function; broken parentage across queues; treating `200` span status as business success; recording bodies/tokens; trusting `traceparent`; baggage explosion; logs as prose; unbounded stack traces; audit/diagnostic conflation; unsynchronized clocks; sampling away rare errors; telemetry exporter blocking requests; missing drop metrics; dashboards without deploy/config dimensions; and assuming no telemetry means no event.

### Compact example

Checkout p99 rises while mean and error rate look normal. Route-template histogram shows `/checkout` tail only in version p12. Exemplars link slow buckets to sampled traces: each logical request has three payment attempts after a mesh retry change. Structured attempt logs show deadline exhausted, while order state proves no duplicate charges. **Conclusion:** metric distribution locates, trace explains causal amplification, logs expose retry decisions, and domain state confirms effect safety.

### Connections

[Error Translation](035-error-translation.md), [Rate Limits](039-rate-limits-and-quotas.md), [GraphQL Cost Control](058-graphql-authorization-and-cost-control.md), [Retries](072-retries-and-backoff.md), [Tail Latency](077-fan-out-and-tail-latency.md), [Partial Results](078-partial-results-and-graceful-degradation.md), [Gateway Responsibilities](091-api-gateways-and-edge-responsibilities.md), [Service Mesh](093-service-mesh-relationships.md), and [Integration Testing](095-integration-and-end-to-end-api-testing.md) define observable events. Later capacity/readiness modules consume the evidence.

## Governing Question

How should teams define telemetry questions and schemas, instrument API lifecycle and distributed attempts, control dimensions/privacy/cost, verify the pipeline, and turn signals into trustworthy SLO, debugging, security, product, and capacity decisions?

## Why This Matters

An API can be syntactically healthy while consumers fail: wrong authorization, stale reads, partial results, retry amplification, degraded dependency, incompatible version, or successful response with failed business outcome. Infrastructure CPU alone cannot describe this.

Metrics provide affordable population views but discard individual context. Logs preserve detail but are costly and difficult to aggregate consistently. Traces reconstruct sampled causality but depend on propagation, instrumentation, sampling and clocks. Combining them deliberately shortens detection and diagnosis.

Telemetry is also a distributed production subsystem. Every attribute multiplies storage; every body can leak data; every exporter consumes CPU/memory/network; every schema migration can break dashboards; every sampling policy biases visibility. Instrumentation can itself alter latency or fail requests.

The goal is not “collect everything.” It is to answer owned questions with bounded, semantically stable, privacy-safe evidence and explicit uncertainty.

## Prerequisites and Retrieval

Retrieve [Headers and Metadata](004-headers-and-metadata.md), [Tracing a Request](010-tracing-a-request-through-client-proxy-and-service.md), [Authentication Context](033-authentication-context-propagation.md), [Error Translation](035-error-translation.md), [Data Exposure](048-enumeration-and-data-exposure.md), [AsyncAPI Contracts](063-asyncapi-contracts.md), [Delivery and Acknowledgment](066-delivery-and-acknowledgment.md), [Timeouts](071-timeout-and-deadline-budgets.md), [Retries](072-retries-and-backoff.md), [Tail Latency](077-fan-out-and-tail-latency.md), [Product Ownership](089-api-product-ownership.md), [Gateways](091-api-gateways-and-edge-responsibilities.md), [Mesh](093-service-mesh-relationships.md), and [Integration Testing](095-integration-and-end-to-end-api-testing.md).

Retrieve user journeys and API/domain outcomes; SLOs/error budgets; route templates/versions/deprecations; gateway/mesh/service/dependency topology; retry/fan-out/async paths; error/problem taxonomy; current metric/log/trace schemas and semantic-convention versions; cardinality/volume/cost/retention; sampling; privacy/data classifications; pipeline/drop/queue health; dashboards/alerts/runbooks; deploy/config/feature events; incident queries; and known instrumentation gaps.

## Learning Objectives

After completing this module, you can:

1. assign questions to metrics, logs, traces, domain state, audit records and profiles;
2. define logical operation, attempt, hop, dependency and business-outcome telemetry;
3. choose counter, gauge and histogram instruments with aggregatable dimensions and SLO-aligned boundaries;
4. estimate and govern cardinality, volume, retention, sampling and cost;
5. design structured log schemas, stable error taxonomies, correlation and redaction;
6. propagate trace context safely and model retries, fan-out, async queues, links and long-running operations;
7. apply current semantic conventions with explicit version/migration control;
8. verify telemetry correctness, completeness, pipeline health, privacy and failure isolation;
9. build SLOs, alerts, dashboards, exemplars and incident workflows from tested queries; and
10. state uncertainty introduced by aggregation, sampling, loss, clocks, drift and missing instrumentation.

## Core Exposition

### Begin with decisions and questions

For each journey ask: Is traffic reaching the API? Are consumers succeeding? Which route/version/tenant tier is affected? Is failure protocol, auth, quota, domain, dependency or overload? Is latency queue, gateway, app, database or downstream? Are retries multiplying? Did an effect occur? What changed?

Name who acts on the answer and within what time. Alerts need low-cost aggregatable signals; diagnosis needs correlated detail; audit requires controlled durable evidence; product analytics needs consent/governance and should not be smuggled into operational telemetry.

Define a telemetry contract: signal/name/type/unit/attributes, exact event semantics, producer, source clock, aggregation/temporality, stability, privacy class, retention, sampling, owner and consumers. Version material changes.

### Model the API lifecycle

Separate one logical consumer operation from transport attempts and infrastructure hops. One order submission may create two client attempts, two gateway spans, four service attempts and six dependency calls. Counting all server observations as orders inflates demand and success.

Use distinct counters/events: logical operations where a stable idempotency/correlation boundary exists; received attempts at every boundary; accepted/rejected/overload; completed protocol outcome; domain outcome; deduplication; effects; dependency attempts. Attach attempt number and retry reason to spans/logs, not unbounded metric labels.

For async flows, distinguish published, broker accepted, delivered, processed, acknowledged, retried, dead-lettered and domain effect. Queue time and processing time are different distributions. For long-running operations, distinguish creation/acceptance, execution state transitions, polling and terminal outcome.

### Design metrics for aggregation

Counters monotonically accumulate events until reset; query rates/increases. Gauges rise/fall for current concurrency, queue depth or connection count. Histograms retain distributions of latency, size or work and can aggregate across instances when bucket/resolution semantics align. Prometheus documents counters, gauges, classic/native histograms and summaries; precomputed per-instance summary quantiles generally cannot be meaningfully averaged.

At minimum measure request/operation rate, errors by stable class, duration distribution and saturation/admission. Add dependency attempts/duration/errors, retries, timeouts/cancellations, rejected/overload, inflight, request/response size, cache, queue lag and domain success only when an action follows.

Use route templates such as `/orders/{id}`, not raw paths. Dimensions should be finite, owned and query-relevant: method, route, status class/error code, API/provider version, environment, region, bounded tenant/service tier and perhaps protocol. Never user/email/token/request/object/trace ID.

Compute dimension budget before shipping. If 100 routes × 8 methods × 8 outcomes × 4 versions × 3 tiers × 15 classic histogram series, potential $S=1,152,000$ series before instances/regions. Reduce dimensions or use logs/traces for detail.

Choose histogram boundaries around SLO and diagnostic regimes; include count/sum and overflow. Quantiles require adequate data and known approximation. Mean $\bar{x}=\sum x_i/n$ cannot reveal a bimodal tail. Never average p99s across instances; aggregate histogram distributions.

### Define errors and outcomes semantically

HTTP status is necessary but insufficient. Classify client-invalid, unauthenticated, unauthorized, quota, conflict, not-found, dependency, timeout, overload, internal and domain decline. Keep stable bounded codes separate from localized free text.

RFC 9457 defines HTTP Problem Details and identifies problem type with a URI; it warns that problem details are not an implementation debugging format. Map stable problem/domain outcome to metric dimension and structured log/trace event without copying sensitive detail.

A span's error/status represents that operation according to convention, not business truth. A `200` search with partial/degraded results may need success plus degradation attributes/counter. A payment decline can be a valid API response and unsuccessful business outcome. Record both.

### Build structured logs

Use typed fields: timestamp, severity, event name/schema version, service/version/environment, trace/span/request/operation ID, route/method/outcome/error code, attempt, actor category/tenant tier, dependency, duration and safe diagnostics. Avoid concatenated prose as the only structure.

Log once at the layer with decision context; downstream layers add their own bounded events. Do not repeat the same exception with stack at every hop. Preserve exception chain where needed and cap/redact stack/field sizes.

Apply allowlist collection. Tokens, credentials, cookies, authorization headers, signatures, raw bodies/queries, payment/personal data and tenant/user/object identifiers are excluded unless an explicit controlled purpose permits transformed values. Hashing low-entropy identifiers is reversible by guessing; encryption does not remove access/retention obligations.

Audit events have stronger completeness, integrity, access and retention requirements than diagnostic logs. Keep schemas/pipelines distinct while correlating through approved identifiers.

### Trace causal work correctly

Create server span for received request after extracting/validating context; client span for outbound dependency; producer/consumer spans for message lifecycle; internal spans only for meaningful latency/failure boundaries. Avoid span-per-function noise.

W3C Trace Context standardizes `traceparent` and optional vendor `tracestate` propagation. Treat inbound values as untrusted: validate lengths/format, bound headers, prevent response/log injection, and regenerate/ignore according to trust policy. Trace IDs never grant identity or authorization.

Retries are sibling/child attempts under logical operation; preserve reason/number/deadline. Fan-out shows parallel children. Async receive may use parent when causal semantics and lifetime fit, or a link when work relates to a produced context without direct parent ownership. Record queue wait separately.

Streaming spans must not remain indefinitely unbounded without useful events/metrics; define stream lifetime/message aggregation/error/cancel semantics. Long-running operation creation and execution may be linked across time rather than one enormous span.

Beware duplicate auto+manual instrumentation, client+proxy ambiguity and clock skew. Span timing across hosts is evidence with clock uncertainty; per-process duration is generally safer than subtracting unrelated wall clocks.

### Correlate without cardinality explosion

Put trace/request/operation IDs in logs and trace records, not metric labels. Exemplars can attach a sampled trace reference to a histogram observation without making a series per trace. From an alerting metric, select exemplar/trace, then correlated logs/state.

Propagate only bounded correlation fields. Baggage travels across services and can leak or amplify; allowlist key/value size/count, strip at trust boundaries and never put secrets or authorization decisions in it.

Domain identifiers can appear in tightly controlled logs only if needed and classified; prefer opaque operation ID/tokenization with lookup under audited access. Correlation convenience does not override minimization.

### Sample deliberately

Metrics are typically aggregated without per-request sampling, though collection can still lose data. Logs use severity/event/rate-aware sampling; never sample required audit or rare critical safety outcomes without policy. Traces may use head sampling for cost/latency or tail sampling to retain errors/slow/rare routes after completion.

Sampling biases estimates and may lose parent/child portions. Record decision/ratio and propagate consistently. Ensure rare errors, security denies, high latency and new versions have appropriate retention, while controlling an attacker who generates “interesting” expensive telemetry.

Use dynamic policies carefully: an incident sampling increase can overload exporters/storage and expose more data. Budget CPU/memory/network/storage and include emergency controls.

### Instrument the telemetry pipeline

Measure SDK/exporter queue depth, dropped records/bytes, batch size, export latency/errors/retries, collector receiver/processor/exporter health, storage ingestion/lag/rejection, query latency, alert evaluation/delivery and schema/cardinality rejection.

Telemetry must degrade safely. Non-audit diagnostic export generally buffers within bounds then drops with counters; it must not block API indefinitely or exhaust memory. Required audit needs its own explicit availability/backpressure policy rather than pretending best-effort logs are complete.

Watch cardinality and volume per service/version/signal/attribute. Enforce attribute length/count, series budgets and drop/redaction policies close to source, with visibility into dropped data.

### Verify telemetry as product behavior

Automated tests send known success, error, retry, timeout, cancel, partial, async and auth scenarios, then assert expected metrics deltas, log fields/redaction, trace topology/status/attributes and domain outcome. Tolerate timing/export latency but not semantic ambiguity.

Test route templating, status/error mapping, histogram unit/bounds, counter resets, duplicate instrumentation, trace propagation/malformed context, sampling, clock skew, exporter outage/backpressure, collector restart, cardinality attacks and PII/secret scanners.

Use synthetic expected counts to validate dashboards/SLO/alerts and alert delivery. A beautiful dashboard with a wrong query is a production defect. Version semantic conventions and dual-emit/migrate queries when current OpenTelemetry conventions change stability/names.

### Turn signals into operations

SLOs use user-visible success and latency distributions at the owned boundary, not merely pod health. Separate availability, correctness/degraded and freshness where meaningful. Measure numerator/denominator with aligned events and exclude only documented traffic.

Alerts should express actionable symptoms/burn, then link dashboards/runbooks with route/version/region/error/dependency breakdown and recent deploy/config events. Avoid alerting on raw log strings or a single instance percentile.

During incident, test telemetry health first, compare client/gateway/service/dependency counts, distinguish logical calls/attempts/effects, use traces for hypotheses, logs for decisions, and authoritative state for outcome. Record uncertainty and gaps.

## Definitions and Notation

Let $R,M,O,V,T$ be bounded route-template, method, outcome, version and tenant-tier value sets; $B$ is histogram/auxiliary series multiplier and $S$ potential series. Let $N$ be request observations, $x_i$ durations, $H(b)$ cumulative bucket counts, and $q_\phi$ a quantile estimate. Let $L$ denote logical operations, $A$ attempts and $E$ domain effects.

A **semantic convention** assigns shared meaning/names/types/units to telemetry. An **exemplar** links an aggregate observation to detailed context. **tail sampling** decides after more trace data exists. **telemetry debt** is a known gap, ambiguity, cardinality/privacy risk or broken consumer with owner and remediation.

## Mechanisms, Invariants, or Proof Structure

**Cardinality product.** Each independent metric-label value combination may form a distinct series, so the Cartesian-product upper bound multiplies. Adding unbounded raw path/user IDs removes the finite bound.

**Average counterexample.** Nine requests at 10 ms and one at 910 ms have mean 100 ms, while p90 boundary/tail is dramatically different. A mean cannot reconstruct the distribution; histogram/tail evidence is necessary.

**Signal-complement argument.** Metrics aggregate and lose individual causality; traces sample causal structure and can miss records; logs preserve selected events but may lack population context; state owns effects. Therefore no one signal entails end-to-end correctness.

**Attempt-accounting argument.** If one logical operation creates k attempts, request counters observe k while demand/effect may be one. Without distinct L/A/E instruments, retry changes can masquerade as user growth or duplicate success.

## Alternatives and Trade-Offs

Vendor-neutral semantic conventions improve portability/correlation but evolve and may not express local domain outcomes; extend under owned namespaces. Auto-instrumentation is broad/cheap but lacks domain context and can duplicate manual spans. Manual instrumentation is precise but inconsistent without libraries/review.

Histograms aggregate and support later quantiles but cost buckets/resolution and approximate values. Summaries compute client-side quantiles accurately for configured windows but usually cannot aggregate across replicas. Logs provide flexible detail at high cost. Traces offer causality at sampling/storage cost.

Head sampling is simple/cheap but cannot know final error/latency. Tail sampling retains outcomes but requires buffering/distributed decisions and can drop under pressure. Full capture may be justified briefly in small controlled environments, not assumed safe.

Central collectors standardize/enrich/redact but add shared failure/blast radius. Direct export is simpler but duplicates configuration and credentials. Layered agents/gateways trade isolation for operational complexity.

## Failure Modes and Misconceptions

- “More telemetry is always better” ignores cost, privacy and operator attention.
- “No errors recorded means healthy” ignores loss/sampling/gaps.
- “Trace ID is identity” enables spoofing/authorization failure.
- “Status 200 is success” ignores partial/degraded/domain outcomes.
- “Request count is demand” ignores retries/hops/polling.
- “Average latency describes users” hides tails/distributions.
- “Average p99s” is statistically invalid for aggregate latency.
- “Raw path is a useful label” creates unbounded cardinality.
- “Hashing makes PII anonymous” can remain linkable/guessable.
- “Log every body during incident” expands exposure exactly under stress.
- “Auto-instrument everything” creates duplicate/noisy spans.
- “Sampling only affects detail” can bias rare/error analysis.
- “Collector is observability” ignores exporter/query/alert health.
- “Dashboard rendered” does not prove the query means what its title claims.

## Worked Examples

### Example 1

Raw `/orders/8472` labels create a series per order. Replace with `/orders/{id}` and put approved correlation in trace/log. **Conclusion:** metrics aggregate; detail lives elsewhere.

### Example 2

The dimension example yields $100\cdot8\cdot8\cdot4\cdot3\cdot15=1,152,000$ potential series. Remove method where route implies it and tenant tier from latency histogram. **Conclusion:** budget before emitting.

### Example 3

Nine 10 ms plus one 910 ms request average 100 ms. Histogram exposes a 10% severe tail. **Conclusion:** means conceal distributions.

### Example 4

Client retries once; gateway and service each record two attempts. One idempotent effect occurs. Separate L=1, A=2 per boundary, E=1. **Conclusion:** attempts are not demand/effects.

### Example 5

`200` response contains `degraded=true` and omits recommendations. Protocol succeeds, degradation counter/log/span attribute records product impairment. **Conclusion:** model multiple outcome axes.

### Example 6

Attacker supplies forged valid-looking `traceparent`. Service propagates correlation but authorizes only verified token/context. **Conclusion:** trace context is untrusted metadata.

### Example 7

Queue consumer creates a new root and loses producer causality. Add message creation context link and queue-time metric. **Conclusion:** async causality needs explicit modeling.

### Example 8

Exporter blocks on outage and consumes request threads. Bound queue/export deadline and drop diagnostic spans with visible counter. **Conclusion:** telemetry must not amplify failure.

### Example 9

Tail sampler keeps errors but attacker generates cheap 4xx floods. Rate/budget policies plus security counters preserve signal without storage denial. **Conclusion:** sampling is an admission surface.

### Example 10

SLO dashboard counts gateway attempts as users and reports 99.9%; synthetic known outcomes reveal denominator inflation. Fix query and add regression. **Conclusion:** telemetry consumers require tests.

## Cross-Program Connections

[Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies SLOs, error budgets, alerts, incident response, progressive delivery and operational evidence.

[Statistics and testing material](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies distributions, sampling bias, test oracles and verification.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies data classification, threat modeling, identity/trust boundaries, audit, retention and access controls.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies causality, clocks, partial failure, messaging, retries, sampling and uncertainty.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies telemetry pipelines, schemas, collectors, storage, cost, self-service dashboards and governance.

## References

1. OpenTelemetry, [Semantic Conventions 1.44.0](https://opentelemetry.io/docs/specs/semconv/).
2. OpenTelemetry, [HTTP Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/http/).
3. W3C, [Trace Context Recommendation](https://www.w3.org/TR/trace-context/), 23 November 2021.
4. IETF, [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html), July 2023.
5. Prometheus, [Metric Types](https://prometheus.io/docs/concepts/metric_types/).
6. Prometheus, [Histograms and Summaries](https://prometheus.io/docs/practices/histograms/).
7. Prometheus, [Metric and Label Naming](https://prometheus.io/docs/practices/naming/).

## Exercises

### Exercise 1

Design the metric/log/trace/domain-state evidence for create order with auth, idempotency, payment retry, async fulfillment and partial response.

### Exercise 2

Estimate potential series for 80 routes, 6 methods, 10 outcomes, 5 versions, 4 regions and a 12-series histogram. Redesign within a 100,000-series service budget.

### Exercise 3

Trace one logical request with two client attempts, gateway, three parallel dependencies and an async message. Define parent/link, attributes, outcomes and correlation.

### Exercise 4

Create a privacy/cardinality/sampling policy for a multi-tenant financial API during a high-severity incident.

### Exercise 5

Diagnose disagreement: clients report failures, gateway metrics are healthy, service logs are sparse, traces show gaps, domain state has successful effects and alert did not fire.

## Answers to the Exercises

### Answer 1

Metrics: logical accepted/completed/domain outcome/deduped effect; received attempts/status/problem class; route-template latency/size; auth denies; payment attempts/errors/duration; event publish/delivery/process/ack/lag; partial/degraded; inflight/saturation. Logs at decisions: safe operation/trace IDs, tenant tier, route/version, idempotency result, auth category, payment attempt/reason/deadline, event key token, fulfillment transition, problem/degradation—no token/body/card data. Trace server/client spans through gateway/order/payment, sibling retry attempts, producer and linked consumer with queue time; mark protocol and business outcomes separately. Authoritative state asserts one order/payment intent and fulfillment state. Correlate via opaque operation/trace ID; never metric label. Test response loss, retry and partial response.

### Answer 2

Raw upper bound is $80\cdot6\cdot10\cdot5\cdot4\cdot12=11,520,000$ series, far beyond 100,000 and before instances. Route tables usually bind method, so combine operation template rather than route×method; collapse outcome to bounded status/error classes, remove version/region from the high-resolution histogram if separate deployment/resource metrics and targeted logs/traces can diagnose them, or record coarser SLO buckets. For example 480 operation templates × 5 outcomes × 12 = 28,800 series. Add lower-cost request counter dimensions selectively and enforce per-instrument/attribute budgets. Validate actual active combinations; an upper bound is planning, not observed cardinality.

### Answer 3

Use a logical operation span/context at client if owned; two client-attempt spans are siblings with attempt number/reason/remaining deadline. Each gateway/server hop continues validated context with server spans, avoiding duplicate proxy/manual spans. Three dependency client spans are parallel children of the service attempt and identify bounded dependency/operation/outcome. Producer span injects message context/correlation. Consumer processing uses extracted parent when representing direct causal continuation, or link when delayed/batched/multi-source; record queue time and delivery attempt separately. Logs carry trace/span/opaque operation IDs. Metrics count L=1, client attempts=2, each boundary attempts, dependency attempts=3 per service attempt, messages/deliveries and final effect independently. No user/token/body in propagation.

### Answer 4

Deny tokens/cookies/auth headers/signatures, account/card/body/query and raw user/object IDs across all signals. Allow stable service/version/environment/region/route template/problem code/tenant tier; use audited tokenization for an operation/account lookup only in restricted short-retention incident logs. Bound attribute names/count/length and metric values; never tenant ID in labels. Validate/regenerate trace context at edge and strip unapproved baggage. Keep audit stream unsampled with separate integrity/access/retention; tail-sample errors/slow/new version within quotas, plus low-rate unbiased baseline. Cap attacker-triggerable 4xx/security traces and retain aggregate denies. Incident elevation needs approver/scope/expiry/budget, secret/PII scanning and automatic rollback; telemetry pipeline drop/queue/storage/access is monitored.

### Answer 5

First verify signal definitions and pipeline health: client endpoint/version, gateway success criteria and route, exporter/collector drops/lag, sampling, log severity/rate limits, trace propagation/instrumentation, query/alert evaluation/delivery. Reconcile counts by logical operation versus attempts and time windows. Domain success plus client failure suggests response-path ambiguity, timeout after commit, incompatible response, partial/degraded outcome or wrong client population; it does not prove client success. Reproduce with synthetic correlated request and capture gateway/service/dependency phases plus client deadline. Inspect problem/status/body compatibility and canary/version/config. Fix sparse logs/trace gaps and alert query/denominator, but use authoritative state to protect retry/idempotency effects. Record uncertainty and test the repaired dashboard/alert with known failures.
