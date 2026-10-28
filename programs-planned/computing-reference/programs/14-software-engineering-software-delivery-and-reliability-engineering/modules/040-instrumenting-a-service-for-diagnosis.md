---
module_id: SDRE-040
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 40
title: Instrumenting a Service for Diagnosis
status: complete
last_verified: 2026-09-06
---

# Instrumenting a Service for Diagnosis

## One-Page Review

### Governing question

How can a team instrument a service so an operator can detect user harm, bound its scope, connect it to changes, follow one operation across boundaries, test likely mechanisms, and recognize missing evidence without turning production into an unsafe data collector?

### Essential definitions

- an **instrumentation contract** maps operational questions to signals, fields, measurement points, owners, limits, and validation;
- a **user journey** is an externally meaningful sequence whose outcome can be observed at a declared boundary;
- a **measurement point** is the precise location and time at which a value or event is observed;
- a **resource** identifies the entity producing telemetry; an **instrumentation scope** identifies the library or component that produced it;
- **black-box evidence** observes externally visible behavior; **white-box evidence** observes internals;
- a **metric** aggregates measurements; a **log record** describes an event; a **span** describes an operation interval; a **change event** describes an intervention;
- **correlation context** links records that belong to one operation without making them causally equivalent;
- **semantic convention** is a governed naming and meaning agreement across producers;
- **cardinality budget** bounds distinct attribute combinations;
- **telemetry self-observation** measures production, acceptance, rejection, delay, loss, and export health;
- **diagnostic closure** exists when evidence can answer what failed, for whom, when, where, after what change, and which next test distinguishes leading hypotheses.

### Central model, mechanism, or theorem

For operational questions $Q$ and telemetry records $R$, instrumentation is sufficient only relative to a declared diagnostic relation $D(Q,R)$. More records do not imply more diagnosis. A useful design creates a chain:

$$
\text{journey outcome}\rightarrow\text{bounded population}\rightarrow
\text{operation context}\rightarrow\text{internal mechanism}\rightarrow
\text{change evidence}.
$$

If any arrow depends on an absent, stale, untrusted, or sampled field, the conclusion must expose that uncertainty.

### Critical invariants

- instrument user outcomes at the boundary where they become observable;
- pair black-box symptoms with white-box mechanisms;
- use one stable service identity and versioned semantic meanings across signals;
- keep metric dimensions bounded; put high-cardinality detail in controlled logs or traces;
- propagate operation context across every supported transport and clear it between unrelated work;
- record start/end semantics, status, retry attempts, queue time, and dependency boundaries deliberately;
- correlate change events by stable release and deployment identity;
- never record secrets or unrestricted personal data as diagnostic convenience;
- preserve missing, sampled, rejected, and delayed evidence as visible states;
- test telemetry semantics, cost, failure behavior, and downstream queries before relying on it.

### Common failures

Failures include instrumenting only success paths, timing only handler code while excluding queueing, treating a retry as one opaque request, labeling metrics with request or user IDs, using different service names in logs and traces, creating spans around trivial functions, omitting asynchronous context extraction, logging raw credentials, deriving status from exceptions alone, recording deployment time manually, sampling without policy provenance, relying on the same failed network for probes and export, testing emission but not queries, and allowing telemetry failure to crash the service.

### Compact example

A checkout service defines `place_order` at the API boundary. A counter and latency histogram use bounded labels: operation, outcome, region, and release. The server span carries the same operation and release, then child spans cover payment and inventory calls. A structured failure log contains timestamp, error class, safe order class, trace ID, and release—not payment data. Deployment events name the release and exposure window. An external probe measures the journey from outside. Dashboards preserve scope; alerts use user symptoms. Export accepted/dropped counts and evidence age expose blind spots. Fixture requests verify success, validation failure, dependency timeout, retry, cancellation, context loss, and exporter rejection.

### Connections

[SDRE-031](031-observability-versus-monitoring.md) supplies diagnostic questions; [SDRE-032](032-structured-logging.md) through [SDRE-039](039-telemetry-sampling-and-cost.md) supply the individual mechanisms. [SDRE-041](../ROADMAP.md) next defines the reliability properties this evidence will measure.

## Governing Question

Instrumentation is often added record by record: a log for one defect, a metric for one dashboard, and spans because a framework offers them. The result can be expensive yet diagnostically empty. Names drift, identifiers do not join, retries disappear, and telemetry fails exactly when the service does.

A diagnosable service begins with decisions. During a failed operation, an operator needs to establish user impact, population, time, release, dependency path, and plausible mechanism. Each piece of evidence has a distinct job. Metrics reveal aggregate change, traces preserve an operation path, logs capture discrete detail, changes identify interventions, and probes observe from outside.

The governing question asks for the smallest safe, governed evidence system that closes important diagnostic questions while admitting its blind spots.

## Why This Matters

Google SRE distinguishes black-box symptom evidence from white-box internal evidence and recommends using both to answer what is broken and why [1]. OpenTelemetry currently describes traces, metrics, logs, and baggage as related but distinct signals [2]. Its code-based guidance separates library API use from service SDK and exporter configuration [3], while library guidance stresses semantic conventions, context extraction/injection, performance, error handling, and testing [4].

Current OpenTelemetry documentation identifies instrumentation scope by name, version, schema URL, and optional attributes [5]. General and trace semantic conventions provide shared meanings across languages and protocols [6, 7]. The service entity registry requires a logical service name shared by horizontally scaled instances and distinguishes that identity from an instance [8]. These are current conventions, not a guarantee that any backend interprets every field identically.

## Prerequisites and Retrieval

Retrieve user journey, operation, request, message, job, outcome, latency, counter, histogram, log event, span, trace, parent, link, resource, context, sampling, cardinality, schema, release, deployment, freshness, missingness, alert, dashboard, probe, retry, timeout, cancellation, queue, privacy, and runbook.

From SDRE-032 retrieve structured event design and redaction. From SDRE-033 retrieve aggregation and dimensions. From SDRE-034 retrieve trace boundaries. From SDRE-035 and SDRE-036 retrieve change and correlation identity. From SDRE-037 through SDRE-039 retrieve presentation, actionability, selection, and loss.

## Learning Objectives

After completing this module, you should be able to:

1. derive an instrumentation contract from operational questions;
2. select black-box and white-box measurement points;
3. assign complementary roles to metrics, logs, traces, and change events;
4. define stable resource, operation, release, and scope identity;
5. instrument retries, queues, asynchronous work, and dependencies;
6. preserve useful correlation without leaking unsafe data;
7. bound cardinality, volume, overhead, and sampling loss;
8. expose telemetry pipeline health independently from service health;
9. validate semantic outputs and downstream diagnostic queries;
10. review instrumentation through incident, release, and schema change.

## Core Exposition

**Write questions and decisions first.** Begin with representative failures: users cannot authenticate, checkout is slow only in one region, a release increases timeouts, a queue backlog delays work, or a dependency returns invalid data. For each, ask what outcome establishes harm, what population bounds it, which mechanisms could explain it, and what next observation separates those hypotheses.

Turn those questions into an instrumentation table with journey, operation, measurement point, signal, fields, units, labels, correlation key, sampling policy, privacy class, owner, freshness, expected query, and test. Remove any record with no supported decision unless an explicit exploratory or audit purpose justifies it.

**Draw the service boundary and journey.** Name ingress types—HTTP, RPC, message, schedule, stream—and egress dependencies. Include queues, caches, storage, identity, and background work. Mark where a user outcome becomes knowable. A server that accepted a command may not know whether asynchronous fulfillment succeeded; those are separate operations and outcome measurements.

Define operation names from stable behavior, not raw URLs or user input. `/orders/{id}` is bounded; `/orders/927461` creates unbounded names. Distinguish attempt, logical operation, and user journey. Retries create multiple attempts for one logical operation, while duplicate delivery may create repeated processing of one message.

**Establish identity once.** A logical service name should be stable across replicas; instance identity distinguishes processes or tasks [8]. Add environment, region, version, and deployment identity as resource attributes where applicable. Do not encode ephemeral instance IDs into the logical service name.

Instrumentation scope identifies which library or application component emitted a record and which schema it used [5]. Version conventions and producers. When migrating meanings, dual-publish only for a bounded interval, mark both schemas, validate consumers, then retire the old field.

**Use metrics for aggregate questions.** For each critical operation, count eligible attempts and outcomes and record a latency distribution with declared boundaries. Add traffic and saturation relevant to capacity. Labels should support an action: operation, outcome class, region, release, and bounded tier may be useful. Request, trace, user, session, raw URL, and error-message labels usually explode cardinality.

Place timers deliberately. End-to-end server latency starts when the server accepts the operation and ends when its declared responsibility completes. Record queue wait separately from execution. Client and server durations answer different questions. Retries need attempt counts and final logical outcome so a successful retry does not erase dependency instability.

**Use spans for operation structure.** Create spans around meaningful remote calls, queues, durable work, and major internal boundaries that explain latency or failure. Extract upstream context before starting a server/consumer span and inject current context into supported outbound transports [4]. For batch work, links may represent multiple causal predecessors better than pretending one parent.

Record status from the operation's contract, not simply “exception occurred.” A handled validation rejection may be an expected outcome; a swallowed timeout may be an error even without an exception. Avoid a span for every function: overhead and visual depth can hide the causal path.

**Use logs for discrete detail.** Emit structured events for state transitions, rejected inputs by safe class, dependency errors, retry exhaustion, configuration loading, and security-relevant actions. Include event time, observed time when available, severity semantics, event name, service/release identity, operation, safe error class, and trace/span context.

Do not log complete request bodies, tokens, credentials, personal identifiers, or unbounded stack data by default. Apply allowlists and test redaction. A hash may remain personal or reversible through guessing; it is not automatic anonymization.

**Record changes as first-class evidence.** Emit deployment, configuration, flag, schema, dependency, and rollback events from the authoritative controller. Include stable change ID, artifact digest, version, environment, scope, actor class, start/end exposure, and result. Application startup logs are useful but do not alone establish exposure.

**Correlate without overclaiming.** Use trace context for one distributed operation and stable release/change IDs for interventions. Preserve identifiers across logs and spans, but avoid metric labels with trace IDs. Correlation makes records joinable; it does not prove one caused another.

The executable model below demonstrates complementary signal shapes for three controlled attempts. Metrics use bounded dimensions, failure logs retain trace detail, and trace records preserve per-attempt duration. It is not an OpenTelemetry SDK or production exporter.

<!-- bijux-verify: {"id":"diagnostic-signal-shapes","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"metric groups: 3\nfailed traces: ['t2', 't3']\nslowest trace: t3 900ms\nmetric has trace id: False\n","stderr":""}} -->
```python
attempts = [
    {"trace": "t1", "region": "se", "release": "r7", "outcome": "ok", "ms": 80},
    {"trace": "t2", "region": "se", "release": "r7", "outcome": "timeout", "ms": 500},
    {"trace": "t3", "region": "us", "release": "r7", "outcome": "timeout", "ms": 900},
]
metrics = {}
logs = []
metric_label_names = {"region", "release", "outcome"}
for attempt in attempts:
    key = (attempt["region"], attempt["release"], attempt["outcome"])
    metrics[key] = metrics.get(key, 0) + 1
    if attempt["outcome"] != "ok":
        logs.append({"trace": attempt["trace"], "error_class": attempt["outcome"]})

slowest = max(attempts, key=lambda attempt: attempt["ms"])
print("metric groups:", len(metrics))
print("failed traces:", [record["trace"] for record in logs])
print("slowest trace:", slowest["trace"], f'{slowest["ms"]}ms')
print("metric has trace id:", "trace" in metric_label_names)
```

The final check is intentionally limited to this controlled key set; a real schema validator must inspect attribute names and values directly. The shapes illustrate an invariant: aggregate dimensions support population comparison while high-cardinality trace identity remains in event-level evidence.

**Instrument asynchronous work explicitly.** A producer operation ends when its declared responsibility—often durable enqueue—completes. Consumer queue delay begins at message availability and execution begins at receipt. Preserve message or causation identity safely, represent redelivery and attempt number, and distinguish success from acknowledgment if those differ.

Thread-local context does not automatically cross task pools, callbacks, or durable queues. Test extraction, injection, cancellation, timeout, and context cleanup. Leaked context can attach one user's telemetry to another operation.

**Expose evidence quality.** Export counts for attempted, accepted, rejected, sampled, dropped, retried, queued, and successfully exported telemetry. Record queue age and capacity, last successful export, schema rejection, cardinality overflow, and collector reachability. These values measure evidence health, not user health.

Use an independent black-box probe for critical journeys [1]. If service and telemetry exporter share DNS, network, credentials, or region, one failure can erase both. Document remaining common dependencies; perfect independence is rarely achievable.

**Budget overhead and loss.** Measure allocation, CPU, latency, export bytes, queue memory, collector load, storage, and query cost. Disable expensive attribute construction when a span is not recording where the API permits. Batch within bounded delay and memory. Apply the SDRE-039 sampling contract and retain policy version.

Never let normal telemetry failure crash business logic [3, 4]. This preference is not absolute for mandatory audit evidence: if an operation legally requires a durable audit record, the product contract may need fail-closed behavior. State that boundary explicitly rather than letting a generic library decide.

**Connect evidence to operational surfaces.** Dashboards use aggregate symptoms, population, release, evidence freshness, and drill-down. Alerts use actionable user harm. A drill-down preserves absolute time, region, release, operation, and trace context. Runbooks name queries and expected evidence gaps.

Build at least one “golden path” from external symptom to metric cohort, trace, failure log, dependency evidence, and recent change. Also build a missing-evidence path: probe fails, application telemetry absent, collector queue saturated, or permissions denied. Unknown must remain visible.

**Test semantics, not only emission.** Unit tests assert names, units, label sets, status mapping, timer boundaries, redaction, and context cleanup. Integration tests cover real framework instrumentation, nested spans, retry attempts, messages, and exporter failure. Query tests use fixtures for reset, no traffic, high cardinality, partial propagation, sampling, delayed events, and schema migration.

Run controlled fault scenarios: dependency timeout, invalid response, queue backlog, cancellation, disk full, clock skew, dropped export, and deployment rollback. Verify that the intended dashboard and alert reach the correct conclusion. A record visible in a backend is necessary evidence, not proof of diagnostic closure.

Review instrumentation after incidents and architecture changes. Remove unused high-cost fields, but preserve rare obligations through explicit risk review. Every signal needs an owner, schema, version, cost budget, privacy classification, test, and retirement path.

## Definitions and Notation

Let $Q=\{q_1,\ldots,q_m\}$ be declared operational questions and $R$ the records available during a bounded interval. Let $D(q,R)$ be a diagnostic procedure returning an answer plus limitations. Instrumentation is sufficient for $q$ only if $D$ can produce the required decision under declared failure and freshness assumptions.

For operation class $o$, let $A_o$ be eligible attempts and $Y(a)$ the declared outcome of attempt $a$. An outcome count is $N_{o,y}=|\{a\in A_o:Y(a)=y\}|$. The labels defining $o$ and $y$ are part of the measurement contract.

For a span with start $s$ and end $e$ on a suitable monotonic clock, duration is $d=e-s\ge0$. Queue wait, execution, client time, and server time use different $s$ and $e$ and cannot be substituted silently.

Let $K_M$ be permitted metric dimensions and $K_E$ permitted event-level fields. Trace identity belongs in $K_E$ but ordinarily not $K_M$. A cardinality budget bounds the distinct value combinations of $K_M$ per instrument and collection scope.

## Mechanisms, Invariants, or Proof Structure

**Question-coverage argument.** If no record in $R$ observes a required variable for $q$, no downstream dashboard can derive it without an additional assumption. Therefore instrumentation review begins with required variables, not visualizations.

**Boundary argument.** A measurement before an operation's responsibility ends cannot establish its final outcome. Enqueue success cannot prove fulfillment success. Each outcome must be observed at the boundary where it becomes knowable.

**Aggregation argument.** Removing high-cardinality identity from metric labels preserves bounded grouping but prevents per-request metric lookup. Retaining trace identity in logs or spans supplies drill-down without multiplying metric series. The two signal shapes are complementary.

**Correlation argument.** Equal trace or change identifiers establish declared membership, not causation. Causal claims require temporal order, mechanism, alternative testing, and evidence quality beyond identifier equality.

**Missingness argument.** If exporter failure and healthy zero both produce no stored record, they are observationally equivalent downstream. Independent accepted/dropped/freshness evidence is required to distinguish them.

**Overhead argument.** Instrumentation shares finite CPU, memory, network, and storage. Unbounded work can reduce service reliability and corrupt observations. Therefore every instrumentation path needs bounded attributes, buffering, and failure behavior.

## Alternatives and Trade-Offs

**Automatic versus manual instrumentation.** Automatic coverage is fast and consistent for supported libraries; manual instrumentation captures domain outcomes. Combine them while testing duplicate spans and semantic conflicts.

**Black-box versus white-box.** External probes observe user symptoms and miss internal detail. Internal signals explain mechanisms and can disappear with the service. Critical paths need both.

**Wide events versus multiple signals.** Rich event records simplify per-operation joins but cost more and do not replace aggregate metrics. Separate signals optimize different questions but require consistent identity and semantics.

**Coarse versus fine spans.** Coarse spans reduce overhead but hide internal waits. Fine spans localize work but create noise and cost. Instrument boundaries that distinguish hypotheses.

**Central versus library-owned conventions.** Central governance improves consistency; library ownership stays close to meaning. Use shared conventions with named domain owners and versioned extension points.

**Synchronous versus asynchronous export.** Synchronous export provides immediate handoff and adds request latency and failure coupling. Bounded asynchronous export protects the request path but can lose buffered data at crash.

**Fail-open versus fail-closed audit emission.** Fail-open protects availability; fail-closed protects mandatory evidence. Choose from the product and regulatory contract, not the telemetry library default.

**More context versus privacy and cardinality.** Detailed context accelerates diagnosis and increases exposure and cost. Allowlists, redaction, event-level placement, retention, and access control must precede collection.

**Stable schemas versus rapid evolution.** Stable meanings protect queries; evolution fixes gaps. Version, dual-publish briefly, validate, and retire rather than mutate silently.

## Failure Modes and Misconceptions

1. **“More telemetry means more observability.”** More redundant or incoherent records can increase search cost without answering a question.
2. **“Framework defaults understand the business outcome.”** They observe protocol mechanisms, not necessarily fulfillment or user success.
3. **“A 200 response is success.”** The body or later asynchronous work may represent failure.
4. **“Exceptions define errors.”** Expected exceptions and silent error returns both defeat that shortcut.
5. **“One timer is end-to-end latency.”** Queue, client, server, dependency, and fulfillment intervals have different boundaries.
6. **“Request IDs are useful metric labels.”** They destroy bounded aggregation.
7. **“Trace context proves causality.”** It provides membership and ordering evidence only.
8. **“Every function needs a span.”** Excess detail raises overhead and obscures meaningful structure.
9. **“Hashing personal data makes it safe.”** Guessing, linkage, and policy obligations may remain.
10. **“Startup logs prove deployment exposure.”** They omit traffic assignment and controller state.
11. **“No stored telemetry means no event.”** Export, sampling, filtering, or permissions may explain absence.
12. **“The exporter may crash the request.”** Normal diagnostic telemetry should usually degrade independently.
13. **“Probe and service telemetry are independent.”** Shared network, identity, region, or backend can couple them.
14. **“A passing emission test proves dashboards.”** Query, aggregation, links, and rendering need separate validation.
15. **“Semantic conventions never change.”** Stability and migration status vary; version and review current sources.
16. **“Unused fields can always be deleted.”** Rare incident, audit, and safety uses require explicit review.

## Worked Examples

### Example 1

**Derive signals from a question.** “Did release r7 harm checkout in Sweden?” requires eligible attempt counts, outcome classes, latency distribution, region and release labels, exposure change events, and drill-down trace identity. CPU alone cannot answer it. **Conclusion:** the question determines measurement points and join keys.

### Example 2

**Separate enqueue from fulfillment.** An API returns 202 after durable enqueue in 40 ms; a worker fails payment 20 seconds later. API acceptance is successful under its contract, while journey fulfillment fails. Record distinct producer and consumer operations linked by message context. **Conclusion:** one early success must not erase a later outcome.

### Example 3

**Bound metric cardinality.** With 5 regions, 4 releases, 12 operations, and 6 outcome classes, the theoretical product is $5\times4\times12\times6=1{,}440$ combinations before sparsity. Adding one million user IDs multiplies the bound catastrophically. Keep user identity out of metrics. **Conclusion:** dimension products are reviewed before deployment.

### Example 4

**Instrument a retry.** A dependency times out twice and succeeds on the third attempt. Record three child attempts with durations and outcomes, one logical dependency operation with final success, and a retry counter. The user outcome can be successful but latency and dependency instability remain visible. **Conclusion:** attempts and logical outcomes answer different questions.

### Example 5

**Diagnose missing data.** An external probe fails, application metrics vanish, and collector accepted-count remains flat while export failures rise. Absence cannot be read as zero traffic. The evidence points to a telemetry path problem plus possible service harm, requiring independent checks. **Conclusion:** self-observation converts silence into bounded uncertainty.

### Example 6

**Correlate a change safely.** Error ratio rises after release r8 exposure begins. Metrics partition r7/r8, traces show r8 failures in a new parser, and rollback reduces errors. This supports a causal hypothesis more strongly than timestamp proximity alone, but shared traffic changes remain alternatives. **Conclusion:** identifiers organize evidence; mechanism and intervention tests support causality.

### Example 7

**Prevent context leakage.** A worker pool reuses a thread whose previous task had trace `a`. The next unrelated task has no extracted parent but inherits `a` from thread-local state. A test asserts context cleanup after each task and starts a new root when no valid parent exists. **Conclusion:** context lifecycle is part of data correctness and privacy.

### Example 8

**Choose log detail.** A payment decline log needs safe reason class, provider operation, release, region, and trace ID. It excludes card number, token, customer email, raw payload, and provider secret. Restricted audit evidence follows a separate contract. **Conclusion:** diagnostic sufficiency is compatible with data minimization.

### Example 9

**Validate a timer.** A message is available at 10.000 s, consumed at 10.450 s, processing begins at 10.500 s, and ends at 10.900 s. Queue wait is 450 ms, dispatch overhead 50 ms, execution 400 ms, and availability-to-completion 900 ms. **Conclusion:** named boundaries prevent one latency value from hiding the mechanism.

### Example 10

**Close a diagnostic path.** A page identifies failed document writes in region A. The dashboard shows release scope and fresh evidence; a trace locates storage timeout; a log supplies safe error class; a deployment event identifies a connection-pool change; rollback restores a black-box probe; export counters show no loss. **Conclusion:** closure is a tested chain of complementary evidence, not one giant record.

## Cross-Program Connections

1. [API-001](../../28-api-and-service-engineering/ROADMAP.md) connects operation and outcome contracts to service boundaries.
2. [DIST-001](../../27-distributed-systems-engineering/ROADMAP.md) connects propagation, retries, queues, partial failure, and causality limits.
3. [DE-001](../../19-data-engineering/ROADMAP.md) connects telemetry schemas, timestamps, lineage, and late data to pipelines.
4. [DARCH-001](../../20-data-architecture-engineering/ROADMAP.md) connects retention, privacy, governance, and analytical fitness.
5. [NET-001](../../24-network-engineering/ROADMAP.md) connects probes, transport loss, and dependency timing to network mechanisms.
6. [SEC-001](../../25-security-engineering/ROADMAP.md) connects redaction, identity trust, audit evidence, and adversarial input.
7. [OS-001](../../22-operating-systems/ROADMAP.md) connects resource saturation and monotonic clocks to runtime evidence.
8. [SARCH-001](../../12-software-engineering-software-architecture/ROADMAP.md) connects measurement boundaries to components and ownership.
9. [STQE-001](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) connects semantic fixtures and fault scenarios to quality engineering.
10. [PLAT-001](../../29-platform-engineering/ROADMAP.md) connects conventions, SDK defaults, and telemetry guardrails to platform products.

## References

1. Ewaschuk, R. “Monitoring Distributed Systems.” *Site Reliability Engineering*. O'Reilly/Google, 2016. <https://sre.google/sre-book/monitoring-distributed-systems/>. Retrieved 2026-09-06.
2. OpenTelemetry Authors. “Signals.” Current OpenTelemetry documentation, last modified March 10, 2026. <https://opentelemetry.io/docs/concepts/signals/>. Retrieved 2026-09-06.
3. OpenTelemetry Authors. “Code-Based Instrumentation.” Current OpenTelemetry documentation. <https://opentelemetry.io/docs/concepts/instrumentation/code-based/>. Retrieved 2026-09-06.
4. OpenTelemetry Authors. “Libraries.” Current OpenTelemetry documentation. <https://opentelemetry.io/docs/concepts/instrumentation/libraries/>. Retrieved 2026-09-06.
5. OpenTelemetry Authors. “Instrumentation Scope.” Current OpenTelemetry documentation, last modified June 19, 2026. <https://opentelemetry.io/docs/concepts/instrumentation-scope/>. Retrieved 2026-09-06.
6. OpenTelemetry Authors. “General Semantic Conventions.” OpenTelemetry Semantic Conventions. <https://opentelemetry.io/docs/specs/semconv/general/>. Retrieved 2026-09-06.
7. OpenTelemetry Authors. “Trace Semantic Conventions.” OpenTelemetry Semantic Conventions. <https://opentelemetry.io/docs/specs/semconv/general/trace/>. Retrieved 2026-09-06.
8. OpenTelemetry Authors. “Service Entity.” OpenTelemetry Semantic Conventions Registry. <https://opentelemetry.io/docs/specs/semconv/registry/entities/service/>. Retrieved 2026-09-06.

## Exercises

### Exercise 1

Define instrumentation contract, measurement point, resource, instrumentation scope, black-box evidence, white-box evidence, semantic convention, and diagnostic closure.

### Exercise 2

A service has 3 regions, 5 releases retained during rollout, 20 operations, 4 outcome classes, and 6 bounded customer tiers. Compute the maximum label-product combinations before sparsity. Explain why adding 500,000 user IDs is unacceptable.

### Exercise 3

An asynchronous image service records only API 202 responses and worker CPU. Diagnose the evidence gaps for “Did the user's image become available within 30 seconds?” Design the missing metrics, spans, logs, and context.

### Exercise 4

Design an instrumentation contract for password reset across API, email queue, provider, link click, and credential update. Include privacy, retry, outcome, probes, changes, dashboards, alerts, and loss evidence.

### Exercise 5

Transfer the design to an automated greenhouse where sensors, irrigation controllers, and a cloud scheduler communicate intermittently. Operators must diagnose plant-risk events without collecting unnecessary worker data. Define boundaries, signals, correlation, independent checks, and tests.

## Answers to the Exercises

### Answer 1

An instrumentation contract maps questions to signals, fields, measurement points, owners, limits, and tests. A measurement point is where and when evidence is observed. A resource identifies the producing entity; instrumentation scope identifies the producing library or component and schema context. Black-box evidence observes external behavior; white-box evidence observes internals. A semantic convention governs shared names and meanings. Diagnostic closure means the evidence chain can establish what failed, for whom, when, where, after which change, and which next test distinguishes likely mechanisms, while disclosing uncertainty.

### Answer 2

The product bound is $3\times5\times20\times4\times6=7{,}200$ possible combinations per instrument before absent combinations and other attributes. Adding 500,000 user IDs raises the theoretical product to 3.6 billion, threatening producer memory, transport, backend indexing, and query usability. Keep bounded tier in metrics; retain authorized user-level detail only in controlled event evidence when necessary. A strong answer also monitors actual cardinality and overflow rather than treating the product as a predicted observed count.

### Answer 3

API acceptance does not observe fulfillment; CPU neither identifies the journey nor its outcome. Create a logical job identity linked safely from API span to producer enqueue and consumer processing. Count accepted jobs, eligible completions, failure classes, and completion-latency histograms from acceptance to availability. Trace queue wait, processing, storage, and publication; log safe state transitions and terminal errors with trace/job context; record retry attempts, redelivery, cancellation, and expiry. Add an external availability probe, deployment events, and exporter accepted/dropped/freshness signals. Test successful completion, provider timeout, duplicate delivery, context loss, delayed job, invalid input, exporter failure, and no traffic.

### Answer 4

Define separate outcomes: reset request accepted without revealing account existence, email durably queued, provider accepted, link validated, and credential changed. Metrics use bounded operation, outcome, region, provider class, and release—never email or token. Spans link API, queue, provider, click, and update where trust permits; durable messages extract/inject context and distinguish attempts. Logs contain safe reason classes and restricted audit identifiers under a separate access/retention contract. Redact tokens, addresses, bodies, and credentials. External probes use controlled accounts and avoid triggering abuse. Change events cover templates, provider routing, token policy, and deployments. Dashboards show user-safe success, latency, provider, release, and evidence health; pages require actionable widespread harm or security risk. Export loss, sampling, queue age, and schema rejection remain visible. Tests include enumeration resistance, expiry, replay, retries, delayed mail, provider failure, context cleanup, redaction, and rollback.

### Answer 5

Measure the plant-risk journey at greenhouse boundaries: sensed moisture/temperature, scheduler decision, command delivery, valve actuation, water flow, and postcondition. Metrics aggregate bounded greenhouse, zone, device class, outcome, and software release. Event records capture safe device state transitions and calibration class; traces or causation IDs link scheduler commands to controller acknowledgments without worker identity. Record firmware and configuration changes authoritatively. Independent local alarms and physical flow sensors reduce dependence on the cloud path. Missing gateways, stale sensors, disagreement, clock drift, duplicate commands, manual override, and export loss are explicit states. Minimize worker data to authorized role/action audit where safety requires it. Test disconnection, stuck valve, false sensor, retry, context reuse, local fallback, telemetry saturation, and recovery. Evaluation rewards plant-risk boundaries, data minimization, independent verification, and honest missingness rather than a particular vendor stack.
