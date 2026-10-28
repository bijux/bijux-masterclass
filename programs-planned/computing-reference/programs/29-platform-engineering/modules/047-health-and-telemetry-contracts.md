---
module_id: PLAT-047
program: Platform Engineering
level: 1
module_number: 47
title: Health and Telemetry Contracts
status: complete
last_verified: 2026-09-02
---

# Health and Telemetry Contracts

## One-Page Review

### Governing question

How should a platform define health decisions and telemetry evidence so workload controllers take safe actions, teams detect user harm, operators diagnose causes, and signals remain trustworthy, affordable, private, versioned, and useful during the failures they are meant to explain?

### Essential definitions

- A **health contract** maps observed evidence to a bounded action such as continue startup, admit traffic/work, restart, pause rollout, alert, or declare a terminal outcome.
- A **startup check** asks whether initialization has completed sufficiently for readiness and liveness evaluation; it is not a promise of user success.
- **readiness** means an instance is currently eligible for a named class of new work or routing; it is distinct from process life and whole-service availability.
- **liveness** means restart is a justified local recovery action; dependency unavailability that restart cannot repair is not liveness failure.
- A **workload outcome** is the user/domain result the component exists to produce, such as a successful request, accepted event effect, complete batch result, or safe stateful read/write.
- **telemetry** is emitted evidence about system execution, commonly metrics, logs, traces, events, profiles, and crash artifacts.
- An **SLI** is a defined quantitative measure of service behavior; an **SLO** is a target range or proportion for that SLI over a window.
- An **error budget** is the allowed bad fraction or amount implied by an SLO; it is a policy tool, not permission to create avoidable harm.
- **cardinality** is the number of distinct attribute combinations generating separate series or aggregation identities.
- A **telemetry contract** versions signal names, types, units, attributes, aggregation/temporality, identity, privacy, retention, availability, and consumer expectations.

### Central model, mechanism, or theorem

For workload operation class $u$, health decision $H_u(e,t)\rightarrow(a,r)$ maps evidence $e$ at time $t$ to action $a$ and reason $r$. Evidence is valid only with known source, revision, freshness, scope, and uncertainty. For SLI window with valid events $V$, good events $G\subseteq V$, observed success $s=|G|/|V|$, and target $S$, error budget fraction is $1-S$. Burn rate $b=(1-s)/(1-S)$ compares observed bad fraction with allowed bad fraction when denominators and exclusions are defined. Probe state, telemetry delivery, and SLO health are separate layers and can disagree.

### Critical invariants

- Every health signal names its consumer and action; the same endpoint is not reused blindly for startup, routing, restart, rollout, and paging.
- Startup, readiness, liveness, availability, degradation, drain, progress, completion, and domain correctness remain distinct states.
- Liveness depends on locally recoverable failure; broad dependency checks do not trigger fleet restart storms.
- Readiness represents the operation being routed and fails before drain; it is cheap, bounded, and avoids fan-out that creates correlated outages.
- Batch, event, and stateful profiles expose progress/lease/quorum/result evidence rather than inheriting request-service probe semantics.
- SLI numerator, denominator, exclusions, population, scope, window, source, late-data behavior, and target are explicit and versioned.
- Metrics use stable names/types/units and bounded dimensions; unique user/request/event/error text does not become an unrestricted label.
- Logs, traces, metrics, profiles, and events share stable service/resource/revision correlation without confusing correlation with causation.
- Sensitive payloads, secrets, tokens, personal data, internal topology, and high-cardinality identifiers are minimized, redacted, access-controlled, retained, and deleted by policy.
- Telemetry export is bounded and cannot exhaust application resources or block shutdown indefinitely; loss/backpressure/drop state is itself observable.
- Sampling, aggregation, histogram buckets, temporality, clock behavior, and schema revisions are disclosed so consumers do not infer unsupported precision.
- Alerts prioritize actionable user symptoms and multi-window budget consumption, link ownership/runbooks/evidence, and are tested for missing/stale telemetry.

### Common failures

Using one `/health` for every controller action; reporting ready when only a socket listens; failing liveness because a database is down; making readiness call every dependency; hiding overload by staying ready until OOM; restarting a slow-starting process before initialization; considering green Pods a healthy batch result; measuring success only at the server while clients time out; excluding all hard failures from the denominator; averaging percentiles; choosing histogram buckets after incidents without versioning; putting user ID, URL, exception text, or trace ID in metric labels; logging request bodies or environment variables; assuming trace sampling preserves rare failures; blocking requests on telemetry export; paging on every cause metric; and deleting a service while telemetry credentials, collectors, dashboards, recordings, profiles, and retained personal data remain.

### Compact example

A request-service profile has a startup check for schema/config initialization, readiness for accepting bounded requests, and liveness only for a verified local event-loop deadlock. During database outage it may fail write readiness or return controlled errors, but it does not restart every replica. Request SLI measures valid client-visible operations at the gateway: good means correct response before deadline; explicit client cancellations and approved probes are classified separately. Metrics use route templates, method, outcome class, region, and revision—not raw URLs or user IDs. Traces link gateway and downstream work under tail-aware sampling, logs carry redacted correlation IDs, and the collector exposes queue/drop/export health. Fast and slow burn alerts page the accountable service owner; dependency saturation remains diagnostic context. Synthetic tests validate the path and missing-telemetry alarm.

### Connections

This module operationalizes workload-specific health from [PLAT-041](041-workload-archetypes.md), template acceptance from [PLAT-042](042-service-templates.md), outcome evidence from [PLAT-043](043-batch-and-scheduled-workload-templates.md) through [PLAT-045](045-stateful-workload-standards.md), and runtime behavior from [PLAT-046](046-runtime-and-language-baselines.md). It builds on observability, deployment, environment, and platform-operations capabilities from earlier modules and feeds security, lifecycle, and golden-path standards that follow.

## Governing Question

What versioned platform contract can turn health observations into safe controller/operator actions and turn execution data into trustworthy user-outcome, diagnostic, capacity, security, and lifecycle evidence?

“Healthy” has no useful meaning without a subject, operation, observer, time, and action. A process can be live but unable to serve writes. One replica can be unready while the service remains available. A batch Pod can exit zero while its result is incomplete. A database can answer TCP while lacking write quorum.

Telemetry also has no inherent truth. A metric can omit failed requests, a log can be dropped, a trace can be sampled away, a clock can skew, and a dashboard can query stale or high-cardinality data incorrectly. Evidence must carry semantics and limitations.

The platform supplies consistent mechanisms and defaults while product owners define domain-good outcomes. A generic library can count requests; only the service contract knows whether a late `200`, a stale response, or a duplicate payment is good.

## Why This Matters

Health checks control traffic and restarts. A false negative can remove all capacity or create restart amplification; a false positive routes users to corrupt or overloaded instances. Probe thresholds are control-loop parameters, not cosmetic YAML.

Observability enables detection and explanation under partial failure. Without common identity and context, operators manually join gateway, application, queue, database, and platform evidence precisely when time matters.

Telemetry can harm the system it observes. Unbounded labels explode series count, logging blocks IO, trace export consumes memory, profile collection exposes secrets, and collectors become shared bottlenecks. Cost and privacy are part of correctness.

SLOs align technical evidence with user experience. CPU, restarts, and queue depth are useful causes, but users care whether requests finish correctly, events take effect, data is fresh, and jobs meet deadlines. Cause-only alerts page teams without proving impact; symptom-only signals need diagnostics.

Evidence must survive change. New routes, semantic conventions, sampling policies, bucket boundaries, and service identities can break dashboards or make trend comparisons invalid. Telemetry is an API with consumers and migration obligations.

## Prerequisites and Retrieval

Retrieve processes and signals, startup/shutdown, load balancing, queues and leases, jobs and terminal results, stateful quorum, deadlines, cancellation, retries, overload/backpressure, control loops, probability and statistics, rates/counters/gauges/histograms, quantiles, time series, sampling, distributed tracing/context propagation, structured logging, profiles, clocks and temporality, SLOs/error budgets, incident response, security/privacy, data retention, Kubernetes probes/readiness, OpenTelemetry signals/data models, Prometheus naming/histograms, deployment canaries, and platform lifecycle.

You should distinguish observation from fact; health state from controller action; startup from readiness; readiness from service availability; liveness from dependency health; degradation from failure; process exit from batch result; event delivery from accepted effect; quorum from ready Pods; metric point from time series; counter from rate; histogram from summary; average from percentile; span parentage from causation; correlation ID from trace ID; sampling absence from event absence; telemetry ingestion from end-to-end queryability; and dashboard green from user outcome.

## Learning Objectives

After completing this module, you should be able to:

1. design action-specific startup, readiness, liveness, drain, progress, completion, and outcome contracts;
2. specialize health semantics for request, event, batch, scheduled, and stateful workload profiles;
3. define SLIs/SLOs/error budgets with explicit populations, windows, exclusions, sources, and uncertainty;
4. specify compatible metrics, logs, traces, events, profiles, and resource identity;
5. control cardinality, sampling, aggregation, temporality, clock, privacy, retention, and cost;
6. build a resilient collection pipeline with observable drops, queues, freshness, and query paths;
7. design actionable symptom and diagnostic alerts with burn-rate, ownership, and runbooks;
8. test failure, missing/stale evidence, rollouts, telemetry migrations, and incident workflows; and
9. maintain, deprecate, and retire health/telemetry contracts and every retained artifact.

## Core Exposition

### Begin with subject, operation, and action

For every health question, name the subject: process, container, instance, replica set, queue consumer, scheduled operation, stateful member, cluster, service journey, dependency, or telemetry pipeline. Then name the operation and observer.

Define the action. A failed startup check prevents later checks or triggers eventual restart. Failed readiness removes new work. Failed liveness restarts a container. Failed rollout health pauses promotion. Failed SLO alert pages a human or invokes controlled automation.

Evidence suitable for one action can be unsafe for another. Database reachability may be useful for write readiness, but using it for liveness restarts all frontends during a database incident. A synthetic checkout proves a journey but is too slow and externally coupled for per-second Pod probes.

Specify reason codes, thresholds, freshness, hysteresis, timeout, failure/success counts, ownership, and fallback when evidence is missing. “False” without a stable reason forces log archaeology.

State non-guarantees. Passing readiness does not prove every request succeeds; liveness success does not prove progress; collected telemetry does not prove completeness; a met SLO does not prove every user was served.

### Model health as a typed state machine

A useful component state model includes initializing, eligible, degraded, draining, locally failed/restartable, externally blocked, terminal success/failure, and unknown. Not every archetype uses every state.

Transitions have evidence and actions. Initializing becomes eligible after required local initialization and role acquisition. Eligible becomes draining before traffic/work acquisition stops. External dependency loss may become degraded or unready, not locally restartable.

Unknown is first-class. A timed-out probe, missing metric, broken collector, or stale status is not automatically healthy or failed. Choose conservative action by risk and preserve the distinction for diagnosis.

Aggregate state intentionally. A service can remain available with one failed instance. A stateful cluster can lose write quorum while individual members answer. A composite journey can fail although every component’s local readiness is green.

Expose observed revision/generation, last transition, last successful evidence, reason, and scope. Status without freshness can remain green long after its observer stops.

### Design startup checks

Startup asks whether initialization has reached a point where ordinary readiness/liveness evaluation is meaningful. Examples include loading configuration, verifying identity, applying safe local migrations, warming essential structures, restoring a checkpoint, or joining membership.

Size timeout/failure thresholds from the measured worst credible path plus capacity and failure behavior. A threshold shorter than cold image pull plus recovery produces restart loops; an unbounded threshold hides permanent deadlock.

Kubernetes startup probes suppress readiness and liveness until success. This protects slow starters but does not complete application bootstrap correctly. The application/operator must expose honest progress and terminal failure.

Do not perform destructive or repeated external initialization in a probe. Probe calls can repeat and overlap. Separate idempotent status observation from one-time lifecycle actions.

Observe startup stage/duration, blockers, resource pressure, revision, and termination. Alert when rollout capacity cannot become ready before the service objective, not merely when a Pod eventually exhausts retries.

### Design readiness for admission

Readiness answers whether this instance should receive a named class of new work. A request instance may be ready for reads but not writes; a consumer may be ready to acquire partitions; a stateful follower may serve bounded-staleness reads but not leadership writes.

Use operation-specific endpoints or internal state when routing supports it. A single Boolean may be the provider interface, but derive it from a documented conservative combination and keep richer reasons in status/telemetry.

Readiness is cheap, bounded, and primarily local. Checking every downstream on every probe creates fan-out load and correlated removal. Include a dependency only when the instance cannot safely accept the routed operation and no graceful degradation exists.

Fail readiness before shutdown drain, then wait for routing/lease withdrawal and finish bounded in-flight work. Passing readiness during termination routes new work into a shrinking grace period.

Overload policy matters. Readiness flapping can move overload across replicas and destabilize the fleet. Prefer bounded local queues/load shedding and scaling signals; use readiness only when removal is safer than controlled rejection.

### Reserve liveness for restartable local faults

Liveness means a restart is expected to improve this container’s condition. Examples include a proven deadlocked event loop, irrecoverable local corruption of disposable state, or a stuck process that no longer advances a local watchdog.

Do not fail liveness on shared database, broker, DNS, identity, configuration provider, network, or regional outage unless restart repairs local state and is rate-limited safely. Restart storms erase diagnostics, reload dependencies, and consume capacity.

Use startup gating, sufficient timeout, and failure thresholds to tolerate scheduling/CPU pressure and transient pauses. Probes themselves need resource budget and must not queue behind the exact worker pool they are testing without understanding that implication.

Record last successful progress, probe duration/result/reason, restart cause, previous exit, and local diagnostic snapshot. A liveness restart without evidence can turn a reproducible hang into an intermittent mystery.

Test positive recovery and false-positive scenarios. If restart never repairs the injected condition, it is not a justified liveness signal.

### Define degradation and dependency behavior

Services often provide partial outcomes: cached reads during database loss, one region during another’s outage, delayed events during broker throttling, or read-only state during quorum loss. Model this as explicit degradation rather than binary health.

Name affected operations, users/tenants, consistency/freshness, duration, fallback, and safety limit. A stale response can be good or bad depending on the contract.

Dependency health is diagnostic and an input to operation readiness/SLO; it is not the service’s entire health. Track dependency calls from the caller perspective: deadlines, errors, saturation, retries, circuit state, and version.

Avoid transitive probe fan-out. Service A readiness calling B, which calls C, can remove the whole graph during C failure. Each component should decide whether it can serve its own promised operation.

Expose degradation to users and operators where appropriate. Silent fallback can meet availability while violating correctness or freshness.

### Specialize by workload archetype

Request services use startup, per-operation readiness, liveness, drain, latency/error/saturation, and end-to-end request outcomes. Readiness should align with routing and overload behavior.

Event consumers use ability to acquire work, lease/partition ownership, progress/lag age, settlement/effect outcomes, poison/retry, and drain. A consumer can be process-live but stuck with no progress; liveness restart is justified only when local recovery helps.

Batch jobs use admission/startup, progress freshness, checkpoint, deadline feasibility, partition completion, result manifest, commit, and terminal status. Permanent readiness is usually meaningless. Exit zero is supporting evidence, not the domain result.

Scheduled jobs add intended period, materialization, lateness, overlap, last successful business period, catch-up, and stale outcome. Controller creation is not scheduled-business health.

Stateful services use member identity/role, membership, term/fence, quorum, replication/commit/apply lag, shard coverage, storage health, backup freshness, restore evidence, and operation-specific readiness. TCP response is insufficient.

### Define SLIs from user outcomes

Choose a service boundary and user operation. For request availability, valid events may be eligible client operations at the edge; good events complete correctly within deadline. For data freshness, good observations are below allowed age. For batch, good operations finish validated before deadline.

Define numerator, denominator, exclusions, scope, window, attribution, source, late/duplicate events, retries, cancellations, synthetic traffic, maintenance, and data correction. Exclusions require governance because they can make the SLI green by removing hard cases.

Prefer ratio-based event SLIs where possible because they weight actual use. Time-based availability can overemphasize quiet periods; event-based metrics can underrepresent users who stop trying during failure. Add synthetic or demand indicators where needed.

Measure at the closest reliable observer to the user outcome. Server-side success misses client timeouts and routing failures; client telemetry may be sampled or unavailable. Reconcile multiple perspectives and disclose limitations.

Version SLI definitions. A route classification, deadline, denominator, or observer change breaks comparability unless dual-computed and annotated.

### Set SLOs and error budgets deliberately

Set objectives from user needs, dependency realities, architecture, risk, and cost—not current performance rounded upward. Specify target $S$, window, measurement, and review.

For observed good fraction $s$, bad fraction is $1-s$. Relative budget burn is $b=(1-s)/(1-S)$. If $S=0.999$ and observed $s=0.997$, then $b=0.003/0.001=3$: budget is consumed three times the sustainable rate over that observation window.

Use multiple windows to combine fast detection of severe outages with slower detection of persistent moderate harm. Tune paging/ticket thresholds to available response and test them against historical/synthetic incidents.

An error budget informs release/risk decisions. It does not override safety, security, legal, or individual-user harm and does not require spending the budget.

Report uncertainty, low traffic, delayed ingestion, and incomplete coverage. A high percentage over three requests has different confidence and impact than over millions.

### Design metric contracts

Define metric name, purpose, instrument/type, monotonicity, unit, attributes and allowed values, aggregation, temporality, collection/export interval, owner, stability, retention, and SLI/alert consumers.

Counters represent cumulative monotonic occurrences and are converted to rates/deltas by consumers. Gauges represent sampled current values. Histograms record distributions in buckets/count/sum and can aggregate across instances when boundaries align.

Use base units and stable suffix/naming conventions. Include unit in metadata/name according to the chosen ecosystem and never silently change seconds to milliseconds or counter to gauge.

Prometheus naming guidance emphasizes application prefix, base units, and metrics representing the same logical thing across label dimensions. OpenTelemetry’s metrics data model defines streams, temporality, aggregation, and attributes; translation needs a tested contract.

Avoid duplicate instruments for one event unless reconciliation is defined. Client and server counts legitimately observe different boundaries and should have distinct names/semantics.

### Control cardinality before production

If label dimensions have cardinalities $c_1,\ldots,c_k$, the theoretical combination count can approach $C=\prod_i c_i$, multiplied by services, instances, revisions, regions, and retention blocks. Sparse use reduces actual count but does not remove burst risk.

Use bounded route templates, operation names, method, status/outcome class, region, environment, revision, and controlled tenant tier where justified. Never use raw URL, user/email, request/event/trace ID, stack trace, unbounded error text, timestamp, or arbitrary query as a metric label.

Put high-cardinality identity in scoped logs/traces/events or exemplars under sampling/access controls. Even those stores require budgets and privacy policy.

Enforce allowlists, length/value normalization, series budgets, per-owner quotas, drop/relabel rules, and preproduction cardinality tests. Surface dropped series rather than silently claiming complete telemetry.

Retiring a label value does not immediately remove historical cost. Account for retention and index compaction.

### Choose histograms and quantiles carefully

Latency is a distribution. Mean conceals tails; a percentile without population/window/method is ambiguous. Histograms enable aggregation when buckets align; client-side summaries may calculate quantiles that generally cannot be averaged across instances.

Choose bucket boundaries around user objectives and observed range, with enough resolution to estimate threshold proportions and diagnose shape without excessive cost. Version bucket changes and dual-publish when consumers require continuity.

For an objective “under $D$,” directly count observations at or below $D$ when possible rather than relying on an interpolated percentile. Histogram buckets can provide this ratio if a boundary matches $D$.

Do not average p99 across Pods or minutes. Aggregate underlying distributions or use a backend algorithm with documented approximation/error and consistent population.

Record overflow/underflow, count, sum where meaningful, negative-value semantics, exemplars, and missing-data behavior. A maximum above the highest bucket remains indistinguishable without suitable bounds.

### Build structured log contracts

Define timestamp/observed time, severity number/text, body, service/resource identity, revision, environment, event name, trace/span correlation, error type, outcome, and safe domain identifiers. Use machine-parseable structured output.

Logs are discrete records, not a metrics substitute. Repeated per-request success logs create cost and privacy risk; metrics/traces can summarize while logs capture decisions, state transitions, failures, and audit-relevant events.

Never emit secrets, tokens, credentials, private keys, full authorization headers, unrestricted request/response bodies, environment dumps, or personal data by default. Redact before export, not only at the backend.

Bound message/attribute size and rate. Multiline stack traces need stable parsing or structured exception fields. Error type is controlled; raw exception text is not a metric dimension.

OpenTelemetry’s log data model distinguishes event timestamp, observed timestamp, severity, body, attributes, resource, and trace context. Pin the schema/SDK mapping and test collectors/backends.

### Trace distributed work honestly

A trace represents one observed causal/correlation graph under instrumentation and sampling. Spans record named operations, timestamps, status, attributes, events, links, and resource/scope identity.

Propagate context across trusted boundaries with limits. Do not trust incoming trace sampling or baggage as authorization. Validate size/keys and prevent sensitive tenant/user data from propagating broadly.

Use span links for batch, fan-out, messaging, and other many-to-many relations where one parent is misleading. Parent-child shape is instrumentation convention, not proof of domain causality.

Record errors without marking every expected domain rejection as infrastructure failure. Status and attributes should align with the semantic convention and operation contract.

Sampling absence does not mean no event. Head sampling decides early and may miss rare failures; tail sampling observes more before decision but adds collector state, delay, privacy, and outage behavior. Preserve SLI metrics independently of trace sampling.

### Quantify sampling limitations

With independent per-event sampling probability $p$ and $n$ occurrences of a rare condition, probability of observing at least one is $1-(1-p)^n$. At $p=0.01$ and $n=10$, detection probability is about $1-0.99^{10}\approx0.0956$, under ten percent.

Independence and uniform probability often fail: tail policies, traffic bias, correlated bursts, collector drops, and trace fan-out change the result. Treat the formula as intuition, not completeness proof.

Use error/latency/tenant-aware sampling only with bounded attributes and fairness/privacy review. Keep aggregate counters for every eligible operation at lower cost.

Record sampling policy/revision and effective accepted/dropped counts. A query cannot interpret trace volume without the selection mechanism.

During incidents, temporary sampling increases need capacity, expiry, authorization, and rollback; otherwise diagnostics can create a second outage or privacy breach.

### Treat profiles and crash artifacts as sensitive evidence

CPU, allocation, heap, mutex, goroutine/thread, and continuous profiles reveal bottlenecks not obvious in traces. They can also expose code, object values, URLs, identifiers, and secrets.

Define which profiles are permitted, collection duration/rate, overhead budget, target authorization, storage/access, retention, redaction, and incident use. Test overhead on representative workloads.

Heap dumps and core dumps are highly sensitive, large artifacts. Disable broad automatic collection; use controlled capture, encryption, scoped access, deletion, and legal/security review.

Correlate profiles with service/revision/resource and time windows without labeling every sample by unbounded user context.

Profiles complement metrics/traces/logs. They do not prove user outcome or replace reproducible debugging.

### Standardize resource and service identity

Use stable catalog service/component identity plus environment, region/zone where useful, workload archetype, deployment revision/artifact digest reference, instance identity, runtime baseline, and telemetry schema revision.

Separate service name from instance/Pod, owner/team, namespace, and business system. Renaming teams should not rewrite durable service identity or fracture time series.

Validate identity at emission or collection. Untrusted applications must not impersonate another service/tenant through arbitrary resource attributes.

Keep high-cardinality instance IDs out of SLO aggregations unless required for diagnosis. Preserve them in scoped telemetry for per-instance investigation.

Define behavior for missing/unknown identity. Dropping, quarantining, or marking telemetry has trade-offs; silently merging it into a default service corrupts evidence.

### Engineer the collection pipeline

Map application SDK/agent, local stdout/scrape/receiver, node/sidecar/gateway collector, queue/buffer, processor, exporter, network, backend ingestion/index/query, and dashboard/alert consumers.

Choose pull, push, or hybrid per signal and environment. Scraping exposes target status and supports pull freshness; push suits short-lived jobs and traces/logs but needs buffering, identity, backpressure, and acknowledgement semantics.

Bound application SDK queues, batch sizes, retry, memory, disk spill, timeout, and shutdown flush. Telemetry export is not on the critical request path unless explicitly justified.

Collectors need resource limits, tenant isolation, rate/cardinality controls, queue/drop/retry/export metrics, health, scaling, disruption, upgrade, and disaster behavior. A shared collector outage must not crash every application.

End-to-end telemetry health includes emission, collection, export, ingestion, indexing, query, alert evaluation, notification, and operator access. A green collector process proves little about query freshness.

### Observe the observer

Measure emitted/accepted/dropped items and bytes, queue length/age, retry, export error, backpressure, sampling, processor rejection, backend ingestion lag, index/query latency, alert evaluation, notification delivery, and dashboard data freshness.

Use independent or reduced-dependency monitoring for critical telemetry components. If the only alarm path depends entirely on the failed pipeline, silence is ambiguous.

Heartbeats or canary telemetry with known cadence can test end-to-end freshness. They are synthetic evidence and need owner, cost, routing, and false-positive control.

Define behavior when telemetry is missing: deployment gates may pause, autoscaling may use safe fallback, liveness must not restart blindly, and alerts should distinguish service healthy from unknown.

Exercise backend/collector outage, network partition, credential expiry, quota, storage full, schema rejection, clock skew, and high-cardinality storm.

### Design actionable alerts

Page on urgent, actionable user harm or imminent exhaustion where a responder can change the outcome. Create tickets for slower budget burn/capacity/deprecation; dashboards support exploration; logs/traces support diagnosis.

Symptom alerts use SLI/budget/freshness. Cause alerts such as disk full, no quorum, or certificate expiry are appropriate when they are directly actionable and precede certain harm.

Every alert has owner/on-call, severity, service/scope, condition/window, current value, reason, runbook, dashboards/queries, recent change, dependency context, and safe mitigation/stop conditions.

Avoid one alert per instance for a service-wide incident. Group/deduplicate while preserving distinct tenants/regions when response differs. Test routing and escalation.

Review false positives, false negatives, time to detect, time to acknowledge/mitigate, and post-incident evidence gaps. Removing noisy alerts without replacing detection can merely create silence.

### Use synthetic and real-user evidence appropriately

Synthetic probes test known journeys from controlled locations and can detect zero-traffic failures, DNS/TLS/routing, and dependencies. They cover only scripted data, credentials, locations, and cadence.

Real-user/server event SLIs measure actual eligible operations but may miss users who cannot initiate requests or abandon during outage. Client-side signals add perspective with sampling/privacy/version limitations.

Combine boundary observations: edge/gateway, application, broker/job outcome, data freshness, and synthetic. Resolve disagreements explicitly rather than selecting the greenest source.

Synthetic actions must be idempotent, isolated or cleaned, marked for filtering, rate-limited, and authorized. They must not create production financial/email/destructive effects.

Monitor the synthetic system itself—credential expiry, scheduler, location availability, and result ingestion—so missing probes do not masquerade as success.

### Govern privacy, access, retention, and cost

Classify every signal/field and data flow. Minimize at source, tokenize/pseudonymize only when policy permits, redact before leaving the workload boundary, encrypt in transit/at rest, and authorize query/export/deletion.

Separate broad operational metrics from restricted logs/traces/profiles/audit. On-call convenience does not justify global access to payloads or personal data.

Define retention by purpose and environment: high-resolution metrics, downsampled aggregates, logs, traces, profiles, crash dumps, audit, and incident holds differ. Deletion must reach replicas, archives, exports, and caches.

Budget per service/profile for series, samples, log bytes, spans, profile CPU/storage, queries, and retention. Surface spend and dropped data by owner. Cost control should preserve SLO evidence before verbose diagnostics.

Rate limits and sampling must fail visibly. Silent backend throttling corrupts incident and compliance assumptions.

### Version telemetry as an API

Version metric names/types/units/labels, log event names/fields/severity, span names/kinds/attributes/status, resource identity, semantic conventions, sampling, buckets, temporality, and SLI queries.

OpenTelemetry semantic conventions can have different stability levels by domain/signal. Pin versions/opt-in behavior and inspect emitted data; do not upgrade every SDK/agent independently without migration.

For breaking changes, dual-emit or transform for a bounded window, update recording/alert/SLO/dashboard consumers, compare totals/distributions, then remove old streams after retention/rollback needs.

Avoid permanent aliases that double cost and hide migration. Inventory consumers, including ad hoc reports and compliance exports, before removal.

Record annotation/change events so trend shifts caused by instrumentation are not mistaken for product changes.

### Test health and telemetry contracts

Test startup success/slow/terminal failure, readiness per operation, overload/flap, dependency outage, liveness positive recovery and false positives, drain, forced termination, rollout, and missing/stale status.

Test every archetype: request routing/deadline, event lease/progress/effect, batch partition/result/deadline, schedule stale period, and stateful role/quorum/fence/storage/recovery.

Telemetry tests validate names, types, units, allowed dimensions, cardinality, histograms, timestamps, severity, trace propagation/links, sampling, redaction, resource identity, schema revision, and application overhead.

Pipeline tests inject queue saturation, collector/backend outage, credential expiry, retry/drop, clock skew, duplicate data, partial ingestion, query staleness, alert evaluation, notification failure, and recovery surge.

SLO/alert tests replay known good/bad/unknown fixtures, low traffic, late data, exclusions, rollout versions, fast/slow burns, and telemetry absence. Incident games verify access and runbooks.

### Maintain current conformance and lifecycle

Conformance evaluates current probe definitions/actions, profile outcome evidence, telemetry library/agent/collector revisions, emitted schemas, privacy/cardinality/cost, pipeline freshness, SLI/SLO/alerts, owners/runbooks, retention, and exceptions.

Generated defaults drift as applications add routes, dependencies, queues, schemas, and custom labels. Continuously inspect actual signals and deployed config; ancestry is not evidence.

Brownfield adoption can begin with stable service identity, request/outcome metrics, health correction, redaction, and alert ownership, then add traces/profiles. Do not require repository replacement.

Deprecation inventories emitters and every consumer, publishes replacement and compatibility, dual-runs with reconciliation, migrates alert/SLO history deliberately, and stops new use before removal.

Retirement removes probes/routing only with workload retirement, revokes telemetry credentials, stops collectors/agents, deletes recording/alert/dashboard/synthetic definitions, handles retained logs/traces/profiles/crash data, removes schemas/libraries, and preserves required audit/tombstone evidence.

### Operate health and telemetry as platform products

Catalog contracts, profiles, schemas, owners, consumers, SLOs, alerts, runbooks, pipelines, storage, costs, privacy classes, exceptions, revisions, and retirement.

Measure detection coverage and latency, false alerts/missed incidents, diagnostic time, telemetry freshness/drop, cardinality/cost, SLO correctness, migration uptake, privacy/security findings, user effort, and incident evidence quality.

Canary libraries, collectors, processors, schemas, buckets, sampling, and alert changes with representative workload profiles. Roll back only while emitted/query schemas and buffered data remain compatible.

The following executable inventory is synthetic review evidence. It counts declared controls and does not prove health-action safety, telemetry completeness, SLI validity, sampling coverage, alert usefulness, privacy compliance, pipeline availability, or production reliability.

<!-- bijux-verify: {"id":"health-telemetry-control-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"contracts 10\naction_specific_health 10\noutcome_sli 9\nmetric_cardinality 9\nlogs_traces_privacy 9\npipeline_observed 8\nalerts_owned 9\narchetype_specific 8\nschema_migratable 8\nretirement_owned 8\n","stderr":""}} -->
```python
contracts = [
    ("request-service", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("public-api", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("event-consumer", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("batch-job", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("scheduled-job", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("stateful-store", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("node-agent", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("legacy-service", 1, 1, 1, 1, 1, 1, 0, 1, 0),
    ("partner-worker", 1, 1, 1, 1, 0, 1, 1, 0, 1),
    ("experimental-runtime", 1, 0, 0, 0, 0, 0, 0, 0, 0),
]
fields = [
    "action_specific_health", "outcome_sli", "metric_cardinality",
    "logs_traces_privacy", "pipeline_observed", "alerts_owned",
    "archetype_specific", "schema_migratable", "retirement_owned",
]
print("contracts", len(contracts))
for index, field in enumerate(fields, start=1):
    print(field, sum(row[index] for row in contracts))
```

## Definitions and Notation

For operation class $u$, health decision $H_u(e,t)=(a,r)$ maps evidence vector $e$ at time $t$ to action $a$ and reason $r$. Evidence carries source, revision, scope, freshness, and uncertainty; equal Boolean outputs need not justify equal actions.

For valid SLI event set $V$ and good subset $G$, observed success $s=|G|/|V|$. Target $S$ implies allowed bad fraction $1-S$; burn rate $b=(1-s)/(1-S)$ when $S<1$ and denominator semantics are fixed.

For metric label dimensions with possible counts $c_i$, potential combination count is $C=\prod_i c_i$. Actual series also depends on sparse use, resources, revisions, churn, retention, and aggregation.

For independent sampling probability $p$ across $n$ occurrences, probability of at least one sampled observation is $P=1-(1-p)^n$. Independence and uniformity are explicit assumptions.

Let telemetry path $P_t=(E,C,Q,X,B,A,N)$ contain emission $E$, collection $C$, queue/processing $Q$, export $X$, backend $B$, alert/query evaluation $A$, and notification/access $N$. End-to-end evidence is available only when required stages are fresh and semantically compatible.

## Mechanisms, Invariants, or Proof Structure

The health-and-telemetry assurance chain is:

1. name subject, operation, observer, action, evidence freshness, reason, owner, and non-guarantees;
2. implement typed startup, readiness, liveness, degradation, drain, progress, terminal, and unknown states specialized by archetype;
3. define user-outcome SLIs with explicit populations, good/bad/unknown classification, windows, sources, exclusions, and version;
4. set objectives/error-budget policy from needs and risk, with multi-window actionable symptom and cause alerts;
5. specify metrics, logs, traces, events, profiles, identity, schemas, aggregation, temporality, sampling, and correlation;
6. enforce cardinality, privacy, access, retention, cost, and application-overhead bounds at emission and pipeline stages;
7. engineer collection/export/backend/query/notification for isolation, backpressure, observable drops, freshness, and independent checks;
8. test health actions, failure amplification, workload outcomes, signal semantics, missing/stale data, pipeline faults, alert routing, and incident access;
9. continuously validate deployed emitters, schemas, consumers, SLOs, alerts, costs, owners, and exceptions rather than template ancestry; and
10. dual-run and reconcile breaking telemetry changes, then remove emitters, consumers, authority, pipelines, retained sensitive data, and docs during retirement.

The burn-rate equation is arithmetic over a chosen SLI definition; it cannot validate the denominator or prove user fairness. The sampling equation quantifies one idealized observation probability; correlated failure and selection policies can invalidate its assumptions. Both require semantic review.

The invariants are action specificity, typed health, local restartability, operation readiness, archetype outcomes, explicit SLI population, bounded cardinality, common identity, privacy, non-blocking export, disclosed aggregation/sampling, actionable alerts, and complete lifecycle.

## Alternatives and Trade-Offs

**One health endpoint versus action-specific endpoints:** one endpoint is simple but conflates restart, routing, and diagnosis. Specific checks improve safety while adding contract/test surface.

**Local readiness versus dependency checks:** local checks avoid correlated removal and load. Dependency evidence better reflects ability to serve some operations but needs caching, bounds, and degradation semantics.

**Restart versus remain degraded:** restart repairs local deadlock quickly but amplifies shared failure and loses evidence. Degradation preserves capacity/context while requiring controlled error and recovery.

**Server-side versus edge/client SLI:** server telemetry is complete and owned but misses routing/client timeout. Edge/client evidence reflects experience but adds sampling, identity, version, and privacy limits.

**Event-based versus time-based availability:** event ratios weight demand but miss users who stop trying. Time/synthetic measures cover quiet periods but may overweight low demand and scripted paths.

**Histogram versus client summary:** histograms aggregate across instances with chosen buckets and approximation. Summaries can estimate local quantiles directly but generally cannot be meaningfully averaged.

**Head versus tail trace sampling:** head sampling is cheap/distributed but decides before outcome. Tail sampling keeps interesting completions but needs stateful collectors, delay, and capacity.

**Sidecar versus node/gateway collector:** sidecars isolate/configure per workload but multiply resources and lifecycle. Shared collectors are efficient but widen blast radius and tenant contention.

**Push versus scrape:** push suits traces/logs/short jobs and buffers locally. Scrape gives target discovery/freshness and simpler backpressure for metrics but needs reachable endpoints and short-lived handling.

**Rich diagnostics versus minimization:** payload-rich evidence speeds some investigations but increases cost, privacy, and security risk. Structured bounded fields plus controlled capture preserve safer escalation.

**Fast page versus multi-window confirmation:** fast alerts reduce detection time but page on transients. Slow windows reduce noise but delay severe response; combined burn windows balance them.

**Long retention versus downsampling/deletion:** history supports trends, audits, and rare incidents. It grows cost/privacy exposure and preserves obsolete schemas; tiered retention aligns purpose.

## Failure Modes and Misconceptions

- **“Health is one Boolean.”** subject, operation, observer, time, and action determine meaning.
- **“Running means ready.”** a process can run while warming, draining, overloaded, unfenced, or unable to serve.
- **“Readiness means the service is available.”** other replicas, routing, dependencies, and user outcomes determine service health.
- **“Liveness should test every dependency.”** restarting cannot repair most shared outages and can amplify them.
- **“More probe sensitivity is safer.”** short timeouts and low thresholds can create control-loop instability.
- **“Exit zero means batch success.”** result manifests and domain validation determine completion.
- **“TCP response proves stateful health.”** quorum, role, lag, fencing, storage, and data integrity remain.
- **“Collected metrics are complete.”** emission, scrape/export, processing, ingestion, and query can drop or delay.
- **“A green dashboard proves good users.”** SLI semantics and observer coverage may be wrong.
- **“A high SLO percentage is automatically better.”** cost, user needs, window, and measurement define usefulness.
- **“Exclusions remove noise.”** exclusions can remove real hard failures and need governance.
- **“A counter value is a rate.”** rates require time/temporality/reset handling.
- **“Average latency represents users.”** distributions and tails matter.
- **“Percentiles can be averaged.”** quantiles require aggregatable underlying distributions or defined algorithms.
- **“Labels are free context.”** cardinality multiplies storage/query cost and outage risk.
- **“Trace absence means no request.”** sampling and pipeline loss break that inference.
- **“Trace parent means domain cause.”** instrumentation graphs encode correlation conventions.
- **“Telemetry must never be lost.”** blocking/unbounded guarantees can take down the application; loss must be bounded/visible.
- **“Cause alerts are user impact.”** CPU or disk can be diagnostic without violating outcomes.
- **“Deleting dashboards retires telemetry.”** emitters, credentials, pipelines, recordings, retained data, and consumers remain.

## Worked Examples

### Example 1

A frontend liveness probe queries the database. Database outage makes all replicas fail liveness and restart, adding connection storms. Liveness becomes a local event-loop watchdog; write readiness and SLI reflect database impact, while dependency telemetry diagnoses it. Conclusion: restart signals must be locally repairable.

### Example 2

One endpoint returns `200` after opening a socket and is used for startup, readiness, and liveness. During warmup it receives traffic; during drain it stays routed; during dependency failure it restarts. Separate state/action checks correct each transition. Conclusion: equal HTTP status does not imply equal health semantics.

### Example 3

An SLO target is $S=99.9\%=0.999$ and a one-hour window observes $s=99.7\%=0.997$. Bad fraction is 0.003, budget fraction 0.001, so burn rate is 3. Conclusion: the window consumes budget at three times the sustainable rate, subject to valid SLI semantics.

### Example 4

Metrics label `service` (50), raw route (10,000), status (10), region (4), and revision (20), allowing up to 400 million combinations before instances. Replacing raw route with 80 templates and removing revision from the long-lived aggregation reduces the bound drastically. Conclusion: bounded semantics prevent cardinality explosions.

### Example 5

Five Pods each report p99 from a client summary: 20, 25, 30, 80, and 500 ms. Their average, 131 ms, is not fleet p99 because traffic counts/distributions differ. Aligned histogram buckets are aggregated before estimating the quantile. Conclusion: averages of percentiles are not percentiles.

### Example 6

Trace head sampling is 1%; a rare bug occurs ten times. Ideal detection probability is $1-0.99^{10}\approx9.56\%$. Error counters capture all failures, while a bounded tail policy retains failed traces when capacity permits. Conclusion: sampled traces diagnose but cannot be the sole failure counter.

### Example 7

A consumer process is live and ready but its oldest message age rises for an hour because effects time out. Health contract exposes progress/effect ambiguity, pauses acquisition when safe, and pages on outcome age; restarting alone would duplicate attempts. Conclusion: consumer health includes progress and settlement, not process response.

### Example 8

A batch Job exits zero after nine of ten partitions. Pod status and logs look green, but no committed result manifest exists. Terminal outcome remains failed/incomplete and schedule freshness alerts. Conclusion: controller/process telemetry is weaker than domain result evidence.

### Example 9

Collector queue fills during a backend outage. Unbounded retry uses application memory and causes OOM. Bounded SDK queues drop low-priority diagnostics with counters, collectors spill within quota, SLO metrics retain priority, and an independent canary alerts on query staleness. Conclusion: telemetry failure must be isolated and observable.

### Example 10

A service is retired, but traces with personal identifiers remain for 90 days, synthetic credentials still run, alert rules page an abandoned rotation, and a collector token can write. Retirement revokes, deletes/retains by policy, removes consumers, verifies exports/caches, and leaves a tombstone. Conclusion: telemetry has its own data and authority lifecycle.

## Cross-Program Connections

- **Reliability engineering:** SLIs, SLOs, error budgets, burn alerts, overload, incidents, and recovery connect evidence to user outcomes.
- **Distributed systems:** partial failure, clocks, causality, retries, queues, leases, quorum, and sampling explain disagreements among health observations.
- **Statistics:** populations, ratios, quantiles, histograms, sampling probability, confidence, bias, and late data bound inference.
- **Operating systems:** process state, signals, resource pressure, clocks, profiles, and crash artifacts ground probes and diagnostics.
- **API engineering:** operation identity, deadlines, status, versioning, compatibility, and error semantics define request and telemetry contracts.
- **Data engineering:** event-time/processing-time, schemas, pipelines, aggregation, retention, lineage, and quality apply directly to telemetry data.
- **Security engineering:** identity, integrity, redaction, privacy, access, encryption, audit, and deletion protect observation systems.
- **Human factors:** alert fatigue, actionable runbooks, dashboard cognition, ownership, and incident communication shape operational response.
- **Systems engineering:** typed states, control-loop actions, assurance evidence, failure modes, interfaces, and lifecycle prevent local signals from overclaiming.
- **Economics and governance:** telemetry cost, retention, SLO targets, error-budget policy, privacy, and exception ownership allocate scarce capacity and risk.

## References

1. Kubernetes Authors, “Liveness, Readiness, and Startup Probes,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/pods/probes/
2. OpenTelemetry Authors, “Signals,” current documentation, retrieved 2026-09-02. https://opentelemetry.io/docs/concepts/signals/
3. OpenTelemetry Authors, “Metrics Data Model,” current specification, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/otel/metrics/data-model/
4. OpenTelemetry Authors, “Tracing API,” current specification, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/otel/trace/api/
5. OpenTelemetry Authors, “Logs Data Model,” current specification, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/otel/logs/data-model/
6. OpenTelemetry Authors, “Semantic Conventions,” version 1.44.0, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/semconv/
7. Prometheus Authors, “Metric and Label Naming,” current documentation, retrieved 2026-09-02. https://prometheus.io/docs/practices/naming/
8. Prometheus Authors, “Histograms and Summaries,” current documentation, retrieved 2026-09-02. https://prometheus.io/docs/practices/histograms/
9. Betsy Beyer et al., “Service Level Objectives,” Site Reliability Engineering, Google, 2016. https://sre.google/sre-book/service-level-objectives/
10. Alex Hidalgo, “Implementing SLOs,” O’Reilly Media, 2020.
11. W3C, “Trace Context,” Recommendation, version 1.1, November 2021. https://www.w3.org/TR/trace-context/
12. IETF, “The Syslog Protocol,” RFC 5424, March 2009. https://www.rfc-editor.org/rfc/rfc5424
13. CNCF Platforms Working Group, “Platforms White Paper,” April 2023. https://tag-app-delivery.cncf.io/whitepapers/platforms/

## Exercises

### Exercise 1

Define health contract, startup, readiness, liveness, workload outcome, telemetry, SLI, SLO, error budget, cardinality, telemetry contract, and unknown health. State one adjacent concept each must not be confused with.

### Exercise 2

Design health states and actions for a request service, event consumer, scheduled reconciliation, and three-voter stateful store. Include startup, readiness/acquisition, liveness, drain, progress, terminal/domain evidence, unknown state, and dependency failure.

### Exercise 3

A platform uses one dependency-heavy probe for startup/readiness/liveness, labels metrics by user ID/raw URL/error text, averages Pod p99, samples traces at 0.1% as its only failure count, logs bodies/tokens, blocks requests on export, and pages on every CPU spike. Diagnose at least twenty defects and correct them.

### Exercise 4

Design a telemetry product for 500 services across request, event, batch, and stateful profiles. Define identity, signal contracts, SLI/SLO, cardinality/cost, collection topology, sampling, privacy, pipeline health, alerts, migrations, brownfield adoption, and retirement.

### Exercise 5

During a rollout, readiness flaps, the collector drops spans, metric units changed, an SLO denominator excludes timeouts, synthetic credentials expired, and logs contain regulated data. Produce a containment, evidence reconstruction, service decision, telemetry migration, privacy response, and prevention sequence.

## Answers to the Exercises

### Answer 1

A health contract maps evidence to an action and differs from a generic status label. Startup gates meaningful later checks and differs from user readiness. Readiness admits a named class of new work and differs from whole-service availability. Liveness justifies local restart and differs from dependency health. A workload outcome is the promised domain result and differs from process/controller success. Telemetry is emitted execution evidence and differs from guaranteed truth. An SLI defines a quantitative behavior measure and differs from a target. An SLO targets an SLI over a window and differs from a contractual SLA or current performance. Error budget is the allowed bad fraction implied by the objective and differs from permission for harm. Cardinality counts distinct attribute combinations and differs from event volume. A telemetry contract versions signal semantics/consumers and differs from an implementation library. Unknown health means evidence is missing/stale/ambiguous and differs from healthy or failed.

### Answer 2

The request service starts after config/identity/local initialization; readiness admits read/write operations only when the instance can meet their contract; liveness detects a local deadlock; drain removes readiness before bounded completion; outcomes are correct deadline-bound edge-observed responses. Database loss creates explicit write degradation/unreadiness without restart. The event consumer starts after config/broker identity, is acquisition-ready when leases and downstream effect capacity are available, uses local stuck-progress liveness only if restart helps, drains by stopping acquisition and settling/returning work, and measures oldest age plus accepted idempotent effect; ambiguous settlement is unknown/blocked. Scheduled reconciliation tracks intended business period, materialization/lateness, progress/checkpoint, validated result/commit, missed/overlap, and stale last success; exit zero alone is insufficient. The stateful store starts after identity/storage/member initialization, exposes role-specific read/write readiness from membership/quorum/fence/lag, uses liveness only for locally recoverable process faults, transfers leadership and drains before disruption, and reports quorum, committed/applied data, backup/restore evidence. Missing controller/telemetry status remains unknown with risk-specific conservative action rather than automatic healthy or restart.

### Answer 3

One probe conflates actions; dependencies create transitive fan-out/correlated removal; startup lacks realistic initialization bound; readiness does not name routed operation or drain; liveness restarts shared outages and may amplify them; timeouts/thresholds and reason/freshness are absent. Split typed checks: startup for local initialization, cheap operation readiness, local-restartable liveness, explicit degradation/drain, and SLO outcome evidence. User IDs, raw URLs, and error text are high-cardinality and potentially personal; use route templates and bounded outcome/error classes, keeping scoped IDs in protected sampled logs/traces. Pod p99 values cannot be averaged; aggregate aligned histograms or use a defined backend distribution. A 0.1% trace sample is biased/incomplete and cannot count failures; maintain unsampled aggregate SLI counters and record sampling/drop policy, with bounded tail retention for errors. Bodies/tokens violate minimization and secret/privacy controls; redact at source, restrict access, and apply retention/deletion. Synchronous blocking export puts telemetry on the request path; use bounded queues/timeouts/drop evidence and isolated collectors. CPU is a diagnostic cause, not necessarily user harm; page on urgent outcome/budget exhaustion or imminent actionable resource failure, route ownership/runbooks, and use CPU in diagnosis/capacity tickets. Further fixes include stable identity, units/types, cardinality budgets, histogram buckets, context trust limits, collector/backend health, missing-data alerts, synthetic journey, cost, version migration, conformance tests, and retirement.

### Answer 4

Establish stable catalog service identity plus environment, region, revision/digest reference, archetype, instance, runtime baseline, and telemetry-schema revision. Shared metric/log/trace/resource contracts define names, types, units, allowed bounded attributes, severity, context, aggregation/temporality, sampling, redaction, owner, retention, and consumers; profiles add request latency/outcome/drain, event lag/effect/lease, batch progress/result/deadline, and stateful membership/quorum/fence/storage/recovery. Each service defines user-boundary SLI populations/good events/exclusions and risk-based SLO/burn policy. Enforce series/log/span/profile budgets, route templates, quotas, and visible drops. Use workload SDKs/agents into node or gateway collectors with tenant isolation, bounded queues/spill/retry, backend ingestion/query, and independent canary freshness; sidecars are reserved for isolation/compatibility needs. Keep aggregate outcome metrics broadly available; sample traces and restrict logs/profiles by privacy. Multi-window symptom alerts page owners with runbooks; diagnostic and capacity alerts are action-specific. Version schemas/semantic conventions and dual-run/reconcile breaking changes. Brownfield starts with identity, safe health, redaction, outcomes, and alert owner, then expands. Retirement removes emitters, credentials, collectors, alerts/dashboards/synthetics, retained data/exports, and libraries with tombstone evidence.

### Answer 5

Pause rollout and automation that relies on flapping readiness or changed metrics; preserve stable capacity and compare old/new revisions. Determine whether readiness reflects real operation failure, overload, dependency coupling, probe-resource starvation, or instrumentation change; remove new traffic only when safer and avoid liveness restarts. Inventory emitted, queued, accepted, dropped, ingested, and queryable spans/metrics/logs by revision and time; use gateway/controller/application/domain records to reconstruct user outcomes, explicitly marking gaps. Restore or dual-compute the old metric unit and correct metadata/query/alerts before continuing; never splice incompatible values into one series. Rebuild the SLO denominator to include eligible timeouts and backfill/recompute where raw evidence permits, annotating incomparable windows. Treat expired synthetic credentials as synthetic unknown, rotate through scoped identity, and do not infer service health from missing tests. Contain regulated logs: stop/redact emission, restrict queries/exports, preserve incident evidence under authority, identify all backends/replicas/caches, notify privacy/security owners, and delete/retain by policy. Test fixed probe actions, units, denominator, sampling/drop, synthetic freshness, and redaction in canary; resume rollout only with user-outcome and pipeline evidence. Add schema compatibility gates, cardinality/privacy tests, collector capacity/drop alerts, SLI review, credential-expiry monitoring, and an incident record of evidence limitations.
