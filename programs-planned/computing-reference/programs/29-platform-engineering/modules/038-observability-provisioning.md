---
module_id: PLAT-038
program: Platform Engineering
level: 1
module_number: 38
title: Observability Provisioning
status: complete
last_verified: 2026-09-02
---

# Observability Provisioning

## One-Page Review

### Governing question

How should a platform provision instrumentation, collection, transformation, storage, querying, correlation, alerting, access, retention, and cost controls so teams can answer operational questions without leaking data, overwhelming systems, or mistaking available telemetry for truthful evidence?

### Essential definitions

- **observability** is the capability to investigate relevant internal behavior from deliberately produced evidence; it is not a synonym for collecting many signals.
- **telemetry** is machine-produced measurements and events describing an observed entity or operation.
- A **signal** is a telemetry category with distinct semantics, such as metrics, logs/events, traces, or profiles.
- A **resource** identifies the entity described by telemetry, which may differ from the agent that emitted it.
- A **semantic convention** defines stable names, attributes, units, and meanings for common telemetry concepts.
- A **telemetry contract** defines questions, signals, schema, identity, cardinality, sensitivity, sampling, retention, owners, and consumers.
- A **pipeline** is an ordered receiver, processor, exporter, queue, transport, and backend path with explicit transformation and loss behavior.
- **cardinality** is the number of distinct attribute/label combinations; every Prometheus label combination creates a separate time series.
- **sampling** deliberately retains only part of a population under a known decision rule; it changes what can be inferred.
- An **SLO** is a target for a service-level indicator over a period; an alert is useful only when it drives an owned action.

### Central model, mechanism, or theorem

For observed entity $r$, operation $o$, and source time $t_s$, instrumentation emits record $x=(q,r,o,t_s,a,v)$: signal kind $q$, resource identity $r$, operation/event $o$, timestamp, attributes $a$, and schema revision $v$. Pipeline $P_w$ validates, enriches, filters/samples, batches, transports, and stores representation $y$. Query $Q(y)$ supports a decision only if identity/semantics remain compatible, relevant population and loss/sampling are known, timestamps are interpretable, access is authorized, and freshness/completeness meet the question. A dashboard result is evidence under these assumptions, not direct ground truth.

### Critical invariants

- Every telemetry product begins with owned operational/user questions and decisions, not vendor signal volume.
- Resource identity, service/operation naming, environment, artifact/configuration revision, and schema URL/revision correlate across signals.
- Metric names have one quantity and base unit; attributes are bounded and reviewed before creating new time series.
- Logs/events are structured, typed, timestamped, and redacted before emission; secrets, credentials, raw personal data, and unbounded payloads are excluded.
- Trace context is validated and propagated only across intended trust boundaries; baggage and trace state carry no secret or personal payload.
- Sampling policy, probability/selection bias, decision point, and unsampled fallback evidence are recorded; missing spans are not interpreted as success.
- Pipelines expose received, accepted, dropped, queued, retried, exported, rejected, and lag evidence per signal/tenant without recursive dependence on themselves alone.
- Telemetry failure never consumes unbounded application memory/CPU/disk or blocks critical request paths beyond declared budgets.
- Tenant access, encryption, residency, retention, deletion, legal holds, and break-glass querying apply from collection through backups and derived materializations.
- Alerts bind symptom, scope, threshold/model, data freshness, runbook, owner, severity, deduplication, and validation; dashboards do not substitute for response design.

### Common failures

Instrumenting without questions; calling a monitoring stack “observability”; treating telemetry as ground truth; changing attribute meaning silently; using Pod name as service identity; labeling metrics by user, request, URL, exception message, or trace ID; averaging percentiles; resetting counters without handling process restart; logging credentials or request bodies; parsing free-text logs into unstable schemas; generating one trace per health probe while missing rare failures; assuming the W3C sampled bit proves backend storage; placing personal data in baggage; sampling before error/status attributes exist; running one unbounded collector queue; retrying permanent backend rejection; dropping data without counters; alerting on stale or absent data as healthy; and giving every tenant global query access.

### Compact example

A platform provisions `checkout` with a versioned OpenTelemetry SDK distribution, resource attributes for service, environment, deployment artifact/configuration, and zone, plus a local collector endpoint. HTTP request duration is a histogram in seconds labeled only by normalized route, method, status class, and bounded error type; raw paths and account IDs are excluded. Structured events carry event name, source/observed timestamps, severity, trace/span correlation, and allowlisted fields. Parent-consistent trace sampling keeps 5% baseline while error and high-latency tail policies operate in a gateway collector; estimates record sampling assumptions. Collectors have bounded memory, batches, queues, retries, persistent buffering only where justified, tenant authorization, and self-telemetry. An SLO burn alert checks data freshness, links artifact/configuration changes, and routes to an owned runbook.

### Connections

This capability observes environment, artifact, deployment, configuration, secret-reference, and service-connectivity revisions from [PLAT-033](033-environment-provisioning.md) through [PLAT-037](037-service-connectivity.md). It builds on Kubernetes runtime/resource concepts and supplies evidence for later data-service access, reliability, SLO, incident, security, and cost capabilities.

## Governing Question

What platform product lets teams obtain trustworthy, timely, affordable, privacy-preserving operational evidence while keeping instrumentation and pipeline failure from harming the systems being observed?

Observability is an inference capability. Operators cannot see an internal queue, retry decision, configuration branch, or user outcome directly; they ask questions through measurements and events created by software and collection systems. Those systems select, transform, aggregate, sample, delay, and sometimes lose evidence.

The platform should provision consistent SDKs, resource identity, semantic conventions, collection, storage integrations, query/access, starter views, SLO/alert workflows, and lifecycle management. Application teams remain responsible for domain events, meaningful operation names, error classification, user outcomes, and response actions.

## Why This Matters

Production failures cross layers. A deployment may be healthy at Kubernetes level while users see checkout failures. A service may return fast errors and appear low-latency. A dependency may be saturated while caller queues hide it. Correlated metrics, events, traces, profiles, and change identity make these interactions investigable.

Telemetry can destabilize production. High-cardinality labels create millions of series, debug logs fill disks, synchronous exporters block requests, trace payloads exhaust collector memory, and backend outages trigger retry storms. The observation system needs resource and failure budgets.

Telemetry is sensitive data. URLs, headers, SQL, stack traces, baggage, log bodies, and resource metadata may expose credentials, personal data, tenant relationships, vulnerabilities, or business volumes. Broad query access can be as consequential as database access.

The capability also has economics. Recording everything forever is neither possible nor useful. Signal choice, aggregation, sampling, tiering, retention, and deletion must follow decision value and risk rather than default vendor settings.

## Prerequisites and Retrieval

Retrieve measurement scales and units, counters/gauges/histograms, quantiles and probability sampling, structured events, clocks and time synchronization, distributed tracing/span graphs/context propagation, HTTP/RPC semantics, queues/backpressure, batching, retry, compression, Kubernetes resources, workload identity, encryption, RBAC/ABAC, schemas/versioning, SLOs/error budgets, incident response, privacy/data classification, retention/deletion, and cost allocation.

You should distinguish observability from monitoring; telemetry from truth; observed resource from emitting agent; event time from observed/ingest time; metric instrument from exported aggregation; histogram from percentile; trace ID from security identity; context from baggage; head from tail sampling; drop from rejection from absence; query availability from data freshness; alert symptom from root cause; and retention from guaranteed erasure.

## Learning Objectives

After completing this module, you should be able to:

1. derive telemetry contracts from operational and user questions;
2. define cross-signal resource identity, semantic conventions, schema evolution, and change correlation;
3. design bounded metrics, structured events/logs, traces, profiles, and exemplars;
4. choose instrumentation, agents, gateways, collectors, processors, queues, and backends from failure and tenancy needs;
5. govern propagation, sampling, redaction, access, retention, deletion, and cost;
6. design SLOs, dashboards, alerts, and runbooks as decision systems;
7. observe pipeline health, loss, lag, and semantic drift without circular assumptions;
8. test observability through synthetic fixtures, failure injection, query assertions, and incident exercises; and
9. migrate and retire signals, schemas, views, alerts, storage, and vendor integrations safely.

## Core Exposition

### Begin with questions and decisions

List decisions the team must make: Is a user journey succeeding? Which revision changed it? Is latency in queue, service, network, or dependency? Which tenants/regions are affected? Is capacity or policy blocking work? Can a rollout progress? Has recovery restored outcomes?

For each question define subject, population, time range, signal, expected dimensions, freshness, accuracy, sampling, acceptable gaps, sensitivity, retention, query/view, owner, and action. A signal without a decision may still serve exploration, but its cost and lifecycle need an owner.

Separate debugging from alerting, compliance evidence, product analytics, billing, security detection, and scientific experimentation. One event can feed several purposes only when semantics, consent, access, retention, and accuracy satisfy each purpose.

Prioritize user outcomes, critical operations, dependency boundaries, saturation, and change identity. Host CPU alone rarely answers whether users succeeded.

### Write a telemetry contract

Define signal and stable name; observed entity/resource; operation or event semantics; instrument type; unit; temporality/aggregation; attributes and bounded values; source and observed timestamps; schema/semantic-convention revision; sensitivity; redaction; sampling; expected volume/cardinality; collection path; retention; access; consumers; SLO/alert use; owner; and deprecation.

State non-guarantees. A counter can reset; a gauge is sampled state; a log may arrive late or twice; a span may be unsampled or orphaned; a collector acknowledgement may precede backend persistence; a query can be partial; retention expiry may not instantly erase backups.

Treat telemetry schemas as APIs between instrumentation, collectors, queries, dashboards, alerts, exports, and humans. Test compatibility and version transforms.

Keep contracts in reviewable, machine-checkable catalogs where possible. Inventory signal age, owners, consumers, cost, access, and deletion state.

### Establish cross-signal resource identity

OpenTelemetry Resource describes the observed entity, not necessarily the instrumentation agent. Use consistent attributes across metrics, logs, traces, and profiles: service name/namespace/instance where appropriate, environment, cluster/namespace/workload, region/zone, and artifact/configuration/capability revisions.

Distinguish durable logical identity from ephemeral instance. `service.name=checkout` supports aggregation; instance/Pod identifies one runtime. Do not use a Pod name alone as service identity or aggregate unrelated services under one generic name.

Record deployment identity that answers “what changed”: artifact digest/release, configuration digest, platform capability revision, schema migration, feature variant where safe, and change time. Keep values bounded and avoid secrets.

Use schema URLs/revisions when semantic conventions evolve. A renamed attribute or changed unit can silently break queries if sources and consumers do not coordinate.

### Standardize semantic conventions

Adopt current stable conventions for common protocols, services, errors, resources, and operations, with an explicit stability policy. Generate constants where supported rather than copying string keys throughout code.

Create organization/domain conventions only for concepts not already represented. Define meaning, type, unit, allowed values, sensitivity, examples, owner, version, and compatibility. Avoid vendor-specific names at the instrumentation boundary when a neutral convention exists.

Normalize route templates, RPC method names, status classes, and bounded error types. Raw URL paths, SQL text, exception messages, user IDs, and arbitrary headers are not safe metric dimensions.

Version dashboards and alerts with their expected schemas. During migration, dual-write or transform only for a bounded window and compare results before removing old fields.

### Design metrics as aggregatable measurements

Use counters/sums for monotonically accumulated events such as requests and bytes, gauges for current sampled state such as queue depth, and histograms for distributions such as duration or size. Choose instrument and aggregation semantics before naming.

Metric names describe one quantity in one base unit. Prometheus guidance favors suffixes such as `_seconds`, `_bytes`, and `_total`; do not mix milliseconds and seconds or success count and latency in one family.

Dimensions should answer anticipated grouping questions and have bounded vocabularies. Estimate series count as the product of simultaneously varying label cardinalities, targets, and metric families. Correlations and sparsity can lower actual count; unconstrained input can raise it unexpectedly.

Do not average percentiles across instances. Aggregate histogram bucket counts/sums under compatible bucket schemas, then estimate quantiles for the combined population. Keep SLO boundary buckets or native-histogram compatibility where required.

Counters reset on restart and can decrease through target replacement or query composition. Use rate/increase functions that handle resets under backend semantics and preserve deployment/instance context for diagnosis.

### Control cardinality before ingestion

Every unique Prometheus label set is a time series. A `user_id` or raw path label can turn one metric into millions of series and expose personal data. Reject or rewrite unbounded attributes at SDK/view and collector policy boundaries.

Set per-instrument and per-tenant cardinality budgets, allowed label keys/value patterns, overflow behavior, and alerts. Prefer normalized route, status class, bounded error type, operation, region, and revision.

Move high-dimensional exploration to sampled traces, structured event stores, or analytics systems designed for it, with appropriate access and retention. Do not hide unbounded values in generated metric names.

Observe cardinality itself: active/new series, rejected points, attribute value count, memory/storage/query cost, and top contributors. Cardinality enforcement can alter queries, so surface overflow/drop metadata.

### Emit structured logs and events

Prefer typed structured events over free-text parsing. Define event name/class, source timestamp, observed timestamp, severity, resource, instrumentation scope, trace/span correlation where applicable, stable attributes, and body.

Use event names for durable schema identity; keep varying values in typed allowlisted fields. Human-readable text may accompany structure but should not be the only machine interface.

Classify fields before emission. Do not log passwords, tokens, private keys, session cookies, authorization headers, full connection strings, raw bodies, or unnecessary personal data. Redact/allowlist in the application before formatting because downstream regexes cannot recognize every encoding or derivative.

Manage debug levels as time-bounded, scoped configuration with volume/privacy budgets and audit. A global debug switch during an incident can create a second outage or leak.

### Instrument traces as causal evidence

A trace represents causally related operations as spans with trace/span context, timing, kind, status, events, links, and attributes. Name spans by stable operation/route, never individual URL or customer.

Create spans at meaningful boundaries: inbound request, outbound dependency, queue publish/consume, batch/job stage, datastore operation, and major domain step. Avoid a span for every loop iteration or trivial function.

Set error status according to signal semantics; an HTTP 404 may be expected or erroneous depending on operation. Record bounded error type and events without copying sensitive messages indiscriminately.

Asynchronous messaging may use parent/child or links depending on causality and fan-out. Propagate context in governed headers/metadata and handle retries/duplicate consumption deliberately.

### Govern trace context and baggage

W3C `traceparent` carries portable trace/parent identifiers and flags; `tracestate` carries vendor-specific correlation state. The sampled flag indicates upstream recording/export intent, not proof that a backend stored a complete trace.

Validate input format and size, create a new parent span as specified, and decide where to restart or strip context at trust boundaries. Malicious clients can force correlation, storage, or misleading parentage if context is trusted blindly.

Never put personal data, credentials, authorization, or domain payload in `traceparent`, `tracestate`, or baggage. Baggage can propagate broadly and be copied into telemetry; maintain an allowlist, size limits, and boundary policy.

Trace IDs are correlation identifiers, not authentication or authorization principals. Access checks use verified workload/user identity from the application/security layer.

### Choose sampling from inference needs

Head sampling decides early from available context and controls source overhead consistently, but cannot know a later error or latency tail. Tail sampling buffers completed or partial traces and can retain rare outcomes, but requires state, routing consistency, wait limits, and capacity.

Probability sampling supports estimates only when selection probability and consistency assumptions are known. Parent-consistent decisions preserve traces; independent per-span sampling creates gaps. Record policy/revision and any adjusted count or weighting semantics.

Always retaining errors can bias comparisons if success traces are sampled differently. Query systems and users must know denominators and policies. Keep unsampled aggregate metrics/events for broad rates and SLOs.

Bound trace size: attributes, events, links, span count, payload lengths, and duration. A single pathological trace should not exhaust SDK/collector/backend memory.

### Select instrumentation methods

Manual instrumentation best captures domain semantics and outcomes but requires code ownership. Library/framework instrumentation provides consistent protocol boundaries. Auto-instrumentation accelerates coverage but can emit unstable names, sensitive attributes, and extra overhead; review and pin its versions/configuration.

Platform distributions can package APIs, SDKs, exporters/OTLP defaults, semantic-convention version, resource detection, propagation, redaction, sampling, and self-telemetry. Libraries should depend on stable instrumentation APIs rather than application SDK implementations.

Agents/eBPF/network proxies observe without application changes but may describe a different resource and lack domain context. Combine them with application signals rather than claiming equivalence.

Measure instrumentation overhead under realistic throughput, concurrency, payloads, sampling, failures, and disabled-export paths.

### Build collection as explicit pipelines

A common topology is SDK/agent to node or local collector, then gateway collectors, then one or more backends. Local collection reduces application coupling and enriches runtime identity; gateways centralize tenancy, tail sampling, transforms, and exports.

Each signal pipeline declares receivers, processors in order, exporters, authentication, schemas, filters, redaction, batching, queues, retries, timeouts, routing, and failure behavior. Unreferenced configured components are not active.

Order matters. Redact before exporting; establish resource identity before routing; ensure attributes needed for sampling exist before sampling; batch after transformations when semantics allow.

Do not create circular dependencies where the only evidence for collector/backend health must traverse the failed path. Expose local health/self-metrics and an independent minimal alert path.

### Engineer backpressure, buffering, and loss

Telemetry is usually lower priority than the user request. SDK exporters use bounded queues and non-blocking or tightly bounded behavior. When full, apply declared drop/sample/backpressure policy and increment safe self-metrics.

Collector sending queues, batching, retries, and timeouts have finite capacity. Data rejected before a queue does not reach exporter retries; a full queue can drop or block according to configuration. Permanent errors should not retry forever.

Persistent queues survive selected process failures but add disk, I/O, encryption, corruption, identity, retention, and shutdown semantics. They are not a universal exactly-once guarantee; duplicates and final loss remain possible.

Size buffers from input rate $\lambda$, tolerable outage $d$, average encoded record size $b$, burst and compression uncertainty. A necessary raw-capacity estimate is $C\ge\lambda d b$ before metadata, batching, index, replication, and headroom.

### Design multi-tenant isolation

Authenticate sources and bind tenant/environment from trusted identity or collector context, not a spoofable attribute supplied by arbitrary clients. Authorize ingest signal, rate, size, and schema separately from query access.

Partition or quota receiver load, processor CPU, queues, export concurrency, storage, query concurrency, cardinality, retention, and alert evaluation. One noisy tenant must not exhaust shared telemetry for others.

Prevent cross-tenant joins and trace correlation unless explicitly authorized. Tenant ID can be sensitive and high-cardinality; enforce it at storage/access partitions rather than indiscriminately adding it to every metric.

Administrative support and break-glass query access are time-bounded, strongly authenticated, recorded, reviewed, and redacted in downstream exports.

### Protect privacy and security

Create a data-flow/threat model from instrumentation through SDK memory, local socket, collector, queues/disks, network, backend indexes, query caches, dashboards, alerts, exports, backups, and support tools.

Encrypt transport and storage; use workload identity and least privilege for ingest/query/admin. Separate tenants and environments. Harden collector receivers against untrusted sizes, attributes, decompression, parsing, and resource exhaustion.

Apply allowlist/minimization before emission, then defense-in-depth processors. Tokenization or keyed correlation can support investigation, but derived values remain sensitive and require key/lifecycle governance.

Support legal/contractual residency, consent, subject access/deletion where applicable, retention, legal hold, and export controls. Document backend/cache/backup deletion limitations.

### Make time semantics explicit

Record source event time and observed/ingest time where available. Clock skew can create negative durations, reordered events, false causal graphs, and wrong windows. Monitor synchronization and reject/mark implausible timestamps.

Use monotonic clocks for in-process duration when supported, wall clocks for cross-system correlation, and propagate explicit time zones only for human presentation. Store canonical timestamps.

Late and out-of-order data affect alert and SLO windows. Define lateness allowance, evaluation delay, correction/replay behavior, and whether a dashboard includes partial current intervals.

Collector/backend lag is part of freshness. A green value from an hour-old window is not current health.

### Correlate telemetry with change

Every deployment and dynamic configuration activation records exact artifact, configuration, environment, platform capability, route, and relevant flag revision. Emit bounded change events and resource attributes so queries compare before/after and stable/candidate populations.

Do not add commit SHA, image digest, Pod UID, and every flag to every metric blindly. Select bounded rollout/release dimensions or use exemplars/events/traces for high-detail linkage.

Observe loaded rather than merely desired revision where possible. Control-plane state can differ from process state during propagation or failed reload.

Change correlation supports diagnosis, not causation proof. Shared traffic, dependencies, seasonality, and multiple simultaneous changes can confound comparisons.

### Design SLOs and alerts as decisions

Define service-level indicators from user-visible success, latency, freshness, correctness, durability, or availability. Specify population, good/valid events, exclusions, source, schema, aggregation, window, and missing-data behavior.

Error-budget burn alerts combine magnitude and duration to detect fast and slow consumption. Validate queries against synthetic fixtures and known incidents. Check freshness/completeness before evaluating; absence is unknown unless a separately reliable heartbeat establishes meaning.

Every page has owner, severity, impact statement, scope, evidence links, runbook, safe first action, deduplication/grouping, silence/maintenance policy, and escalation. Notifications without action become ignored noise.

Use alerts for symptoms requiring timely response, tickets for capacity/debt, and dashboards for exploration. Do not page on every infrastructure cause independently of user impact unless immediate action is required.

### Build views for investigation

Provide starter views for service overview, user journeys, dependencies, deployments, saturation, queues, errors, latency distributions, SLOs, and telemetry health. Templates require owners and versioned queries.

Support pivots among metric exemplar, trace, structured event, deployment record, and resource inventory through shared safe identity. Correlation IDs do not guarantee causality, so preserve timestamps and links.

Dashboards state units, aggregation, population, time zone/window, sampling, freshness, source, and known gaps. Avoid panels whose green default masks no data.

Test views after schema/backend/query changes and against empty, partial, reset, delayed, and multi-region data.

### Govern retention, tiering, and cost

Retention follows diagnostic/SLO/audit value, sensitivity, legal needs, resolution, and cost. Raw high-resolution metrics, sampled traces, debug logs, aggregates, and compliance events need different periods and access.

Tier hot searchable, warm compacted, and cold archive only when restoration/query objectives justify complexity. Downsample metrics with declared aggregation and preserve SLO boundaries; downsampling cannot reconstruct lost labels or tails.

Allocate cost by tenant/service/signal/source where safe: ingest bytes, active series, samples, spans, events, storage, queries, egress, and alert evaluation. Give teams actionable budgets and top contributors, not surprise chargeback.

Retirement deletes unused instruments, dashboards, alerts, exports, indexes, schemas, access, and storage after consumer evidence and retention obligations. Stopping ingestion is not deletion.

### Observe the observation system

At each hop expose received, decoded, accepted, filtered/sample-dropped, processor-dropped, queue size/capacity, enqueue failure, retry, export success/failure/rejection, batch size, latency, memory/CPU/disk, and backend ingest/query/freshness.

Reconcile counts under known batching/duplication semantics and identify where exact equality is impossible. Canary telemetry with known IDs/values can test end-to-end arrival and queryability without containing production data.

Monitor schema rejection, unknown attributes, cardinality overflow, invalid timestamps, redaction matches, auth failures, tenant mismatch, and sampling-policy skew.

Use an independent minimal path for critical telemetry-pipeline alerts and test the case where the primary backend is unavailable.

### Test and release the capability

Use golden telemetry fixtures to assert resource identity, names, units, attributes, redaction, propagation, sampling metadata, and backend query results. Contract tests span SDK versions, collectors, transforms, and backend adapters.

Load-test realistic cardinality, event sizes, span fan-out, bursts, compression, queries, and backend throttling. Inject network loss, 429/5xx/permanent rejection, queue full, disk full, collector restart, bad schema, clock skew, certificate expiry, and tenant abuse.

Canary instrumentation and pipeline changes by service/cell, compare accepted/exported/loss/cost and query semantics, then progress. Preserve compatible rollback and versioned configurations.

Incident exercises should answer real questions using the provided evidence and reveal whether access, dashboards, runbooks, and correlation work under pressure.

### Operate the capability

Measure onboarding time, instrument/schema conformance, resource identity gaps, signal coverage for critical journeys, propagation breaks, accepted/exported/drop/reject/lag, series/cardinality, ingest/storage/query cost, query latency/failure, SLO freshness, alert precision/actionability, access violations, redaction findings, and retirement rate.

Capacity includes SDK overhead, network, collector CPU/memory/disk/file descriptors, queues, processors, tail-sampling state, backend ingest/index/storage, active series, query concurrency, dashboards, rules, notifications, and failover surge.

The following synthetic inventory demonstrates observability-provisioning coverage.

<!-- bijux-verify: {"id":"observability-provisioning-control-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"services=10\ntelemetry_contract=9\ncross_signal_identity=9\ncardinality_bounded=8\nredaction_tested=8\nsampling_declared=7\npipeline_loss_observed=8\nslo_action_owned=7\nretention_access_owned=9\n","stderr":""}} -->
```python
services = [
    {"name":"checkout",       "telemetry_contract":True,  "cross_signal_identity":True,  "cardinality_bounded":True,  "redaction_tested":True,  "sampling_declared":True,  "pipeline_loss_observed":True,  "slo_action_owned":True,  "retention_access_owned":True},
    {"name":"payments",       "telemetry_contract":True,  "cross_signal_identity":True,  "cardinality_bounded":True,  "redaction_tested":True,  "sampling_declared":True,  "pipeline_loss_observed":True,  "slo_action_owned":True,  "retention_access_owned":True},
    {"name":"inventory",      "telemetry_contract":True,  "cross_signal_identity":True,  "cardinality_bounded":True,  "redaction_tested":True,  "sampling_declared":True,  "pipeline_loss_observed":True,  "slo_action_owned":True,  "retention_access_owned":True},
    {"name":"catalog",        "telemetry_contract":True,  "cross_signal_identity":True,  "cardinality_bounded":True,  "redaction_tested":True,  "sampling_declared":True,  "pipeline_loss_observed":True,  "slo_action_owned":True,  "retention_access_owned":True},
    {"name":"shipping",       "telemetry_contract":True,  "cross_signal_identity":True,  "cardinality_bounded":True,  "redaction_tested":True,  "sampling_declared":True,  "pipeline_loss_observed":True,  "slo_action_owned":True,  "retention_access_owned":True},
    {"name":"search",         "telemetry_contract":True,  "cross_signal_identity":True,  "cardinality_bounded":True,  "redaction_tested":True,  "sampling_declared":True,  "pipeline_loss_observed":True,  "slo_action_owned":True,  "retention_access_owned":True},
    {"name":"recommendations", "telemetry_contract":True, "cross_signal_identity":True,  "cardinality_bounded":True,  "redaction_tested":True,  "sampling_declared":True,  "pipeline_loss_observed":True,  "slo_action_owned":True,  "retention_access_owned":True},
    {"name":"notifications",  "telemetry_contract":True,  "cross_signal_identity":True,  "cardinality_bounded":True,  "redaction_tested":True,  "sampling_declared":False, "pipeline_loss_observed":True,  "slo_action_owned":False, "retention_access_owned":True},
    {"name":"legacy-erp",     "telemetry_contract":True,  "cross_signal_identity":True,  "cardinality_bounded":False, "redaction_tested":False, "sampling_declared":False, "pipeline_loss_observed":False, "slo_action_owned":False, "retention_access_owned":True},
    {"name":"shared-legacy",  "telemetry_contract":False, "cross_signal_identity":False, "cardinality_bounded":False, "redaction_tested":False, "sampling_declared":False, "pipeline_loss_observed":False, "slo_action_owned":False, "retention_access_owned":False},
]

print(f"services={len(services)}")
for field in ("telemetry_contract", "cross_signal_identity", "cardinality_bounded", "redaction_tested", "sampling_declared", "pipeline_loss_observed", "slo_action_owned", "retention_access_owned"):
    print(f"{field}={sum(service[field] for service in services)}")
```

The counts reveal governance gaps; they do not prove telemetry truth, completeness, privacy, statistical validity, pipeline durability, alert quality, or successful deletion.

## Definitions and Notation

Let instrumentation emit record $x=(q,r,o,t_s,a,v)$ for signal $q$, observed resource $r$, operation/event $o$, source time $t_s$, attribute map $a$, and schema/semantic-convention revision $v$.

Pipeline $P_w$ under configuration revision $w$ performs ordered validation, resource detection/enrichment, redaction, filtering/sampling, aggregation/batching, queueing, transport, and backend storage, producing representation $y$ or an explicit drop/rejection/loss observation.

Let $t_o$ be observed/ingest time. Lag $L=t_o-t_s$ is meaningful only under clock and timestamp-source assumptions; negative or extreme values require classification.

For metric family with label domains of cardinalities $c_1,\ldots,c_n$ over $m$ targets, an upper combinatorial bound is $m\prod_i c_i$ series before accounting for sparse combinations, churn, and backend-generated series.

For input rate $\lambda$, outage tolerance $d$, and average encoded size $b$, raw buffer capacity must satisfy $C\ge\lambda d b$ before metadata, indexes, replication, compression uncertainty, and safety headroom. This is sizing evidence, not durability proof.

## Mechanisms, Invariants, or Proof Structure

The observability-provisioning assurance chain is:

1. define owned questions, populations, decisions, freshness, sensitivity, and actions;
2. specify signal schemas, resource identity, semantic conventions, units, attributes, and cardinality;
3. instrument domain and protocol boundaries with bounded overhead and redaction before emission;
4. propagate safe context and apply explicit sampling/inference policy;
5. collect through ordered authenticated multi-tenant pipelines with bounded queues, retries, and loss;
6. store/index under access, encryption, residency, retention, deletion, and cost policy;
7. correlate signals and exact change/runtime identity through compatible schemas;
8. query and visualize with population, sampling, freshness, aggregation, and gap semantics;
9. alert through validated SLO/symptom evidence linked to owner, runbook, and response; and
10. test, self-observe, migrate, and retire instrumentation, pipelines, views, rules, and data.

This is not proof that telemetry is true or complete. Instrumentation, clocks, propagation, sampling, collectors, schemas, storage, queries, humans, and the observed system can fail or bias evidence. The chain makes those assumptions and failure points explicit.

The invariants are decision-first design, cross-signal resource/change identity, bounded metric semantics, structured pre-redacted events, safe context, declared sampling, self-observed finite pipelines, bounded application impact, end-to-end data governance, and actionable alert ownership.

## Alternatives and Trade-Offs

**Direct-to-backend versus collectors:** direct export minimizes components but couples applications to vendor availability/configuration. Collectors centralize identity, transforms, sampling, queues, and routing while adding infrastructure and loss modes.

**Local agents versus gateway collectors:** local agents enrich runtime identity and isolate applications. Gateways centralize tenancy and tail decisions. Combined tiers improve control but add hops, lag, capacity, and debugging complexity.

**Metrics versus events/traces:** metrics aggregate cheaply for rates/SLOs but discard detail. Events/traces preserve high-dimensional context at higher volume, sampling, privacy, and query cost.

**Head versus tail sampling:** head sampling bounds source cost and preserves early consistency but misses later outcomes. Tail sampling selects by completed behavior but buffers state and needs trace routing/capacity.

**Pre-aggregation versus raw retention:** aggregation reduces cost/cardinality and protects privacy, but irreversible detail loss limits new questions. Raw data supports exploration but increases access, storage, and deletion risk.

**Shared versus tenant-dedicated pipelines:** shared systems improve utilization and standards; dedicated systems strengthen isolation and customization at operational/cost overhead.

**Push versus pull metrics:** pull exposes targets and scrape health naturally but requires reachability/discovery. Push fits jobs/remote edges but needs identity, backpressure, lifecycle, and stale-series semantics.

**Open conventions versus vendor-native fields:** neutral conventions improve portability/correlation; vendor features may be richer. Translate at controlled boundaries with tested semantic mappings.

## Failure Modes and Misconceptions

- **“More telemetry means more observability.”** unowned noise obscures questions and consumes budgets.
- **“Telemetry is ground truth.”** it is selected, transformed, delayed, sampled, and fallible evidence.
- **“Resource is the collector.”** it describes the observed entity, which may differ from the emitter.
- **“Labels are free metadata.”** each unique label combination creates storage/query work and may leak data.
- **“Percentiles can be averaged.”** instance quantiles do not generally aggregate into a fleet quantile.
- **“Trace ID is identity.”** it correlates operations and grants no authorization.
- **“Sampled means stored.”** the flag expresses a decision/intention; export/backend can fail.
- **“Tail sampling captures every error.”** overload, incomplete traces, wait limits, and routing can still drop them.
- **“Redaction downstream is sufficient.”** raw values already crossed process, transport, queue, and access boundaries.
- **“Persistent queue means exactly once.”** duplicates, rejection, corruption, full disk, expiry, and final loss remain.
- **“No data means healthy.”** it may mean no traffic, broken instrumentation, pipeline loss, stale query, or outage.
- **“Alert threshold is an SLO.”** an SLO defines user-oriented population and objective; alerting is response policy.
- **“A dashboard is a runbook.”** pictures do not define decisions, ownership, or safe actions.
- **“Retention expiry guarantees deletion.”** replicas, caches, exports, backups, and legal holds need separate lifecycle.
- **“Vendor migration is a collector config change.”** schemas, queries, alerts, access, sampling, cost, and history must migrate.

## Worked Examples

### Example 1

`http_requests_total` labels raw URL including account ID. Series and personal data grow without bound. Instrumentation replaces it with normalized route and bounded status/error attributes; account investigation uses protected sampled events. Conclusion: metric dimensions require bounded semantic design.

### Example 2

Each Pod reports a 99th percentile, and a dashboard averages them. The result is not the fleet p99. Compatible histogram buckets are summed and the quantile estimated from the combined distribution. Conclusion: aggregate distributions, not percentiles.

### Example 3

Auto-instrumentation emits `service.name=unknown_service` while logs use `checkout`. Cross-signal navigation fails. A platform resource contract supplies consistent logical service, instance, environment, and deployment revisions. Conclusion: resource identity is a provisioned contract.

### Example 4

An authorization header reaches logs, collector disk queue, and backend before a regex masks a dashboard field. Allowlisting at emission and processor defense in depth prevent the payload from entering the pipeline. Conclusion: display masking is not redaction.

### Example 5

One-percent head sampling misses a rare error cohort that appears after request start. Tail policy retains error traces while unsampled aggregate counters preserve the denominator; analyses disclose different selection probabilities. Conclusion: sampling follows inference needs and must remain visible.

### Example 6

The telemetry backend returns 429. An unbounded collector retry queue consumes memory and is killed, losing all buffered data. Bounded queue, retry/backoff/timeout, persistent storage only for priority signals, drop counters, and independent alerts contain failure. Conclusion: telemetry needs its own overload policy.

### Example 7

A global collector trusts client-supplied tenant attributes, enabling cross-tenant writes. The gateway derives tenant from authenticated workload identity and enforces per-tenant pipeline/storage/query policy. Conclusion: telemetry attributes are not an authorization source.

### Example 8

An alert evaluates a green rate over data last ingested 40 minutes ago. A freshness guard makes the result unknown and pages the telemetry path separately. Conclusion: values require completeness and freshness evidence.

### Example 9

A rollout changes artifact and configuration together, but metrics contain neither revision. Diagnosis takes hours. Bounded release identity plus deployment events and trace exemplars enable before/after comparison. Conclusion: change correlation must identify actual runtime state.

### Example 10

A deprecated attribute is removed after code migration, but three alerts still query it and silently return empty vectors. Consumer inventory, dual-write comparison, query contract tests, warnings, and staged removal prevent the gap. Conclusion: telemetry schemas are multi-consumer APIs.

## Cross-Program Connections

- **Statistics:** sampling, bias, uncertainty, distributions, quantiles, estimation, and missing data govern inference.
- **Data Engineering:** schemas, lineage, event time, late data, pipelines, storage tiers, retention, and deletion shape telemetry systems.
- **Distributed Systems:** context propagation, clocks, partial failure, retries, queues, causality, and convergence constrain evidence.
- **Computer Security:** identities, least privilege, multi-tenancy, secrets, metadata, privacy, and audit govern access and collection.
- **Software Engineering:** instrumentation APIs, semantic versioning, contract tests, dependency boundaries, and domain events create useful signals.
- **Reliability Engineering:** SLOs, error budgets, saturation, burn alerts, incident response, and graceful degradation turn evidence into action.
- **Human-Computer Interaction:** dashboard cognition, naming, alert fatigue, search, and information scent affect operational decisions.
- **Economics and Governance:** budgets, chargeback, residency, legal hold, retention, and review allocate finite observability capacity.

## References

1. OpenTelemetry, “Specification Overview,” current specification, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/otel/overview/
2. OpenTelemetry, “Resource,” current specification, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/otel/resource/
3. OpenTelemetry, “Semantic Conventions,” current specification, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/otel/semantic-conventions/
4. OpenTelemetry, “Telemetry Schemas,” current specification, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/otel/schemas/
5. OpenTelemetry, “Tracing SDK: Sampling,” current specification, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling
6. OpenTelemetry, “Logs Data Model,” current specification, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/otel/logs/data-model/
7. OpenTelemetry Collector, “Exporter Helper,” project documentation, retrieved 2026-09-02. https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/exporterhelper/README.md
8. OpenTelemetry, “Collector Troubleshooting,” project documentation, retrieved 2026-09-02. https://opentelemetry.io/docs/collector/troubleshooting/
9. Prometheus, “Metric and Label Naming,” official documentation, retrieved 2026-09-02. https://prometheus.io/docs/practices/naming/
10. Prometheus, “Instrumentation,” official documentation, retrieved 2026-09-02. https://prometheus.io/docs/practices/instrumentation/
11. W3C, “Trace Context,” Recommendation, 2021-11-23. https://www.w3.org/TR/trace-context/
12. Kubernetes, “Metrics for Kubernetes System Components,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/instrumentation/metrics/
13. OpenMetrics, “OpenMetrics Specification,” version 1.0.0, retrieved 2026-09-02. https://github.com/prometheus/OpenMetrics/blob/main/specification/OpenMetrics.md

## Exercises

### Exercise 1

Define observability, telemetry, signal, resource, semantic convention, telemetry contract, cardinality, pipeline, sampling, SLO, and exemplar. State one non-guarantee for each.

### Exercise 2

Trace one HTTP request's evidence from instrumentation through resource/context, metrics/events/spans, redaction, sampling, local and gateway collectors, queues/retries, backend storage, cross-signal query, SLO evaluation, alert, incident action, retention, and deletion.

### Exercise 3

A platform labels metrics with user IDs/raw URLs, averages per-Pod p99s, emits credentials in JSON logs, trusts trace IDs as authentication, tail-samples in an undersized single collector, has an unbounded memory queue, gives every tenant global query access, pages on stale dashboards, and removes attributes without consumer inventory. Diagnose at least fifteen failures and correct them.

### Exercise 4

Design observability provisioning for a multi-region payments platform with strict personal-data constraints, 99.99% authorization SLO, rare fraud failures, intermittent regional links, thirty-day investigation needs, two-year audit events, and a fixed monthly telemetry budget. Include signals, identity, sampling, pipelines, access, loss, alerting, retention, and testing.

### Exercise 5

A company must migrate telemetry backends and semantic-convention versions without losing alert coverage or cross-signal correlation. Design dual export/translation, schema compatibility, sampling, query/view validation, cost control, rollback, history/access migration, and proof for retiring the old path.

## Answers to the Exercises

### Answer 1

Observability is an inference capability but cannot guarantee every internal state is identifiable. Telemetry is machine-produced evidence but can be wrong or missing. A signal is a semantic category but no signal alone answers every question. A resource identifies the observed entity but depends on correct detection/configuration. A semantic convention standardizes meaning but evolves and may be misapplied. A telemetry contract specifies production/consumption but cannot prove implementation. Cardinality counts distinct dimension combinations but estimates may miss churn or sparse correlations. A pipeline transforms/transports records but can delay, duplicate, or lose them. Sampling selects a subset but cannot recover discarded detail. An SLO defines a target/population but does not itself create reliability. An exemplar links an aggregate observation to detailed context but may be sampled or unavailable.

### Answer 2

The request starts with trusted resource identity, exact release/configuration, W3C trace context, and a total operation name. Instrumentation increments bounded request metrics, creates a span, and emits structured domain/error events with source time and trace/span IDs. Allowlisting removes sensitive fields before serialization. Head sampling establishes parent consistency; an optional gateway tail policy uses status/latency under declared probabilities while aggregate metrics preserve denominator. A local collector enriches runtime identity and batches; a tenant-authenticated gateway validates schema, redacts again, applies routing/sampling, then enqueues and exports with bounded retry. Self-metrics show accepted, dropped, queued, retried, rejected, and lag. The backend stores under tenant access/retention. Queries join shared resource/release identity and state population/sampling/freshness. The SLO evaluates valid authorization events; burn alert checks freshness and routes to an owned runbook. Incident action is recorded. Hot detail expires at its policy, aggregates/audit follow separate retention, and deletion covers indexes, caches, exports, and governed backups with documented limits.

### Answer 3

User IDs/raw URLs create unbounded series and expose personal data; use normalized routes/bounded dimensions and protected events. Per-Pod p99 averages are mathematically invalid; aggregate compatible histogram buckets then estimate fleet quantile. Credentials must be excluded/redacted before emission, not only at display. Trace IDs are correlation values, not principals; use authenticated user/workload identity. One undersized tail sampler loses traces and creates a failure domain; shard consistently by trace, size wait/state, cap trace size, and retain aggregate fallback evidence. Unbounded memory queues can kill collectors; set capacity, backpressure/drop priority, retries/timeouts, persistent storage where justified, and self-alerts. Global query access violates tenancy; authenticate, authorize, partition, audit, and use bounded break glass. Stale dashboards are unknown, not healthy; freshness/completeness guards and an independent pipeline alert are required. Attribute removal breaks alerts/queries; inventory consumers, dual-write/transform, contract-test, warn, compare, then remove. Further corrections include resource identity, schema revisions, sampling disclosure, cardinality budgets, event/observed time, SLO population, runbooks, cost/retention, and deletion.

### Answer 4

Define user-visible authorization success/latency and critical fraud/audit questions. All signals use service/environment/region and exact release/configuration identity, never account/card values. Metrics count valid authorization outcomes and histogram latency with bounded route/status/error/region dimensions; no personal labels. Structured security/audit events use tokenized governed subject reference, event schema, source/observed time, immutable access, and two-year restricted retention. Traces use allowlisted protocol/domain attributes, 1% consistent baseline plus capacity-sized tail retention of errors/high latency and fraud signals; aggregate counters preserve denominators. Regional local collectors have bounded encrypted persistent queues sized for an agreed link outage, priority routing, explicit drop counters, and tenant identity; gateway/backend tiers are multi-region without uncontrolled cross-residency export. Thirty-day investigation keeps sampled traces/events and appropriate metric resolution; hot/high-volume data tiers down under tested aggregation. SLO burn alerts verify freshness and use independent regional notification, owner, and runbook. Monthly budgets cap series, ingest, trace size/rate, query, and retention with priority for SLO/audit. Tests cover redaction, synthetic SLO math, sampling estimates, partition/queue full, collector restart, backend rejection, clock skew, access, deletion, and incident investigation.

### Answer 5

Inventory every source schema/version, collector transform, metric/event/span, dashboard, alert, SLO, export, access role, retention, and external consumer. Add versioned translation/dual export at a controlled collector boundary while instrumentation emits one canonical semantic contract; avoid two independent samplers that produce incomparable traces. Preserve resource and trace IDs, schema URL, timestamps, temporality, histogram boundaries, and sampling metadata. Replay golden fixtures and synthetic canaries into both backends, asserting series/event/span fields, cross-signal pivots, SLO/alert query results, freshness, missing/reset/late behavior, access, and redaction. Progress services/tenants while comparing accepted/exported/loss/cardinality/cost and user-facing alerts. Rollback keeps the old export and queries without reversing source schema. Migrate required history with checksums/counts and documented transformations, reapply tenant access/retention/legal holds, and avoid indefinite full-cost dual storage. Retirement requires all sources/queries/alerts/users switched, no old-path reads/writes for the evidence window, equivalent critical alerts exercised, old retention/legal obligations met, exports and credentials revoked, queues drained, storage deleted under documented backup limits, and compatibility transforms removed last.
