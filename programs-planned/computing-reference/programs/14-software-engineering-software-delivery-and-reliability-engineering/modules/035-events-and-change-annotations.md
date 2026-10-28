---
module_id: SDRE-035
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 35
title: Events and Change Annotations
status: complete
last_verified: 2026-09-06
---

# Events and Change Annotations

## One-Page Review

### Governing question

How can operators record meaningful system changes so that telemetry can be aligned with what changed, where, when, by whom or what mechanism, and with what verified outcome—without claiming that temporal proximity proves causation?

### Essential definitions

- an **operational event** is a named point-in-time occurrence relevant to system behavior;
- a **change event** records an attempted or completed mutation to code, configuration, data shape, traffic, capacity, policy, dependency, or operating state;
- an **annotation** projects an event onto a chart or timeline;
- **event time** is when the occurrence happened; **observed time** is when telemetry received it;
- a **change window** is the interval during which a multi-step change can affect targets;
- a **target set** identifies the resources, services, tenants, regions, or cohorts exposed;
- a **change identity** is a stable identifier joining intent, execution, rollout, rollback, and audit evidence;
- **provenance** identifies the source record and mechanism that produced an event;
- **correlation** is an observed association; **causation** requires stronger design and evidence;
- **clock uncertainty** bounds the possible real time around a timestamp;
- a **baseline** is the comparison population or period chosen before inspecting the outcome;
- **change collision** occurs when multiple plausible changes overlap one symptom.

### Central model, mechanism, or theorem

Model change $c$ as

$$
c=(i,k,T,a,v,[s,e),o,p),
$$

where $i$ is identity, $k$ kind, $T$ target set, $a$ actor or automation identity, $v$ desired version, $[s,e)$ the effect window, $o$ outcome, and $p$ provenance. For anomaly interval $A$, temporal overlap is

$$
R(c,A)=\frac{\mu([s,e)\cap A)}{\mu(A)}
$$

when $\mu(A)>0$. A positive $R$ makes $c$ a candidate; it does not prove cause. Scope intersection, mechanism plausibility, comparative populations, rollback response, and confounders must also be examined.

With timestamp estimate $t$ and error bound $\epsilon$, real time lies in $[t-\epsilon,t+\epsilon]$. Change definitely preceded symptom only if $t_c+\epsilon_c<t_a-\epsilon_a$.

### Critical invariants

- event names identify stable schemas and never embed dynamic values;
- change identity, kind, targets, desired and previous versions, actor, source, and outcome are explicit;
- requested, started, applied, verified, failed, rolled back, and superseded are distinct states;
- event time and observed time are retained with clock and ingestion uncertainty;
- target scope uses the same resource, release, region, and cohort vocabulary as metrics and traces;
- retries and duplicate delivery do not manufacture new logical changes;
- partial rollout records actual exposure rather than intended exposure;
- annotation rendering remains traceable to the canonical event;
- missing, late, duplicated, reordered, and rejected events are measured;
- an annotation suggests hypotheses but never constitutes causal proof.

### Common failures

Failures include annotating only deployment start, replacing stable IDs with human text, recording intention as application, using one timestamp for a rolling change, omitting previous version and target scope, treating feature evaluation as feature configuration, losing rollback linkage, trusting controller success without outcome verification, overwriting corrections, rendering delayed events at ingestion time, ignoring simultaneous changes, and declaring “the deploy caused it” because two lines appear near each other.

### Compact example

A rollout controller emits `deployment.started`, one `deployment.target_applied` per bounded region, `deployment.verified`, and, if needed, `deployment.rollback_started` and `deployment.rolled_back`. Every record carries one change ID, artifact digest, previous version, desired version, region, actor, pipeline run, event time, observed time, and outcome. A latency chart renders the actual region application windows. Investigators compare candidate and unchanged regions, inspect trace and log mechanisms, and treat recovery after rollback as supporting—not conclusive—evidence.

### Connections

[SDRE-032](032-structured-logging.md) defines event records, [SDRE-033](033-metrics-and-dimensionality.md) defines comparable populations, and [SDRE-034](034-distributed-tracing.md) locates changes within operations. [SDRE-036](../ROADMAP.md) next governs correlation context.

## Governing Question

Production behavior changes because something changed: a binary, dependency, flag, configuration value, schema, route, certificate, quota, autoscaler target, operator action, or external service. Yet telemetry often records symptoms precisely while recording the intervention as a vague chat message or a vertical line labeled “deploy.” That imbalance turns diagnosis into memory and guesswork.

A useful change record must answer what state transition was attempted, which targets were actually exposed, when effects could begin and end, which mechanism acted, which versions bracketed the transition, and how outcome was verified. The record must survive retries, partial failure, delayed delivery, and later correction. It must also remain safe: actor and tenant identifiers may be sensitive, and arbitrary descriptions can leak secrets.

The governing question is evidential. Change events should reduce the candidate set and support comparisons, not predetermine blame. Temporal alignment is necessary for many causal hypotheses, but shared traffic, dependency incidents, and concurrent changes can explain the same association.

## Why This Matters

During an incident, “what changed?” is often the fastest useful question. A precise answer can separate one region from the fleet, one release from its control, or a configuration wave from a dependency failure. Change evidence also supports release verification, audit, capacity analysis, and learning after recovery.

OpenTelemetry's stable Logs Data Model represents timestamp, observed timestamp, trace context, severity, body, resource, scope, attributes, and event name [1]. Its current event semantic conventions define events as named occurrences and require stable names rather than dynamic values, but that guidance is explicitly Development as of retrieval [2]. A production schema should therefore pin its own version and migration policy rather than imply that every convention is stable.

CloudEvents 1.0.2 defines a portable event envelope with identity, source, type, subject, time, data schema, and content metadata [4]. It is useful transport calibration, not a complete operational-change ontology. Telemetry schemas can describe supported transformations as conventions evolve, but current OpenTelemetry guidance also describes limits and work in progress [3].

Google SRE's canarying guidance connects release changes to monitored comparison and notes that feature-flag principles apply beyond software releases [5]. Its monitoring guidance emphasizes symptoms and causes as distinct signal classes [6]. These sources support the workflow: record change evidence, align it with symptoms, then investigate mechanism. They do not license correlation as causation.

RFC 3339 supplies an interoperable Internet timestamp profile while warning that local time and leap-second behavior require care [7]. NIST SP 800-128 supplies security-focused configuration-management guidance and explicit change-control records [8]. Compliance records and observability events may share provenance, but an annotation view is not automatically an immutable audit trail.

## Prerequisites and Retrieval

Retrieve event, state transition, identifier, timestamp, interval, set intersection, deployment, release, configuration, feature flag, traffic split, rollback, provenance, idempotency, schema version, baseline, cohort, confounder, correlation, causation, clock offset, ingestion delay, and audit log.

From SDRE-032 retrieve structured naming, event versus observed time, duplicate delivery, transformation provenance, and audit separation. From SDRE-033 retrieve release and cohort dimensions, ratios, gaps, and aggregation. From SDRE-034 retrieve trace and span correlation plus clock uncertainty. From Modules 025–030 retrieve rollout and rollback mechanisms.

## Learning Objectives

After completing this module, you should be able to:

1. define a versioned operational-change event family;
2. distinguish intent, start, target application, verification, failure, rollback, and supersession;
3. model point changes and effect windows;
4. align event targets with metric, log, trace, and resource identities;
5. calculate overlap while refusing causal overclaim;
6. reason about timestamp uncertainty, delay, reordering, and correction;
7. deduplicate retried delivery without losing distinct attempts;
8. design annotations for deployment, configuration, flags, traffic, and operator action;
9. test controlled change histories against rendered timelines;
10. govern retention, access, provenance, and audit boundaries.

## Core Exposition

**Record a state transition, not a message.** “Deployed checkout” lacks identity, old and new state, scope, timing, mechanism, and outcome. Define an event family around lifecycle transitions: requested, authorized, started, applied to a target, verified, failed, rollback started, rolled back, and superseded. Each name identifies one stable schema.

Use stable names such as `deployment.target_applied` and attributes such as `change.id`, `service.name`, `deployment.environment`, `region`, `from.version`, `to.version`, and `outcome`. Do not create `deployed.checkout.v43.eu`. Dynamic values belong in typed fields. Descriptions help humans but cannot be the only machine-readable evidence.

Identity separates logical change from delivery attempts. An event ID deduplicates one occurrence; a change ID joins the lifecycle; a pipeline or controller attempt ID distinguishes retries. Re-emitting after timeout with the same event ID is duplicate delivery. Starting a new rollback attempt is a new event under the same change.

**Separate intent, mechanism, and observed state.** A merge, approval, or rollout request expresses intent. Controller acceptance says a mechanism began. Desired state written to a control plane is not proof that targets applied it. Target acknowledgement is not proof that health is acceptable. Verification is a separate state with named checks and evidence.

For rolling change, one point timestamp is insufficient. Record overall start and completion plus actual per-target or per-cohort application intervals at an appropriate bounded granularity. A region that never received the candidate belongs in the control group; a region that applied and rolled back needs both exposures.

Feature flags have at least configuration-change and evaluation semantics. `flag.updated` records rule state; per-request `flag.evaluated` may belong in a trace event or bounded attribute, not a global change timeline. Percentage rollout requires actual allocation policy, eligible population, salt/generation, and effective time. “10%” does not identify which users or whether assignment was stable.

Configuration changes include values, references, policy, secrets, certificates, quotas, and runtime tuning. Do not record secret material. Record an opaque version or digest, changed field classification, target, source system, and verification outcome. A digest proves equality of bytes only under the declared algorithm and canonicalization; it does not prove safe meaning.

Traffic changes—routing weights, failover, evacuation, load-balancer policy, DNS, and admission rules—can change populations without changing code. Capacity events—scale-out, instance replacement, limit change—may be automated and frequent. Apply aggregation policy: retain every materially distinct transition, but summarize noisy reconciler observations rather than flooding the event store.

**Preserve two times and an interval.** Event time belongs to the source occurrence. Observed time belongs to reception. Their difference measures pipeline delay only if clocks are compatible. A rollout effect window begins when a target can serve the new state and ends when exposure stops, not when a button was clicked.

Represent timestamp uncertainty. If a change time is $100\pm5$ seconds and symptom time is $108\pm5$, possible intervals overlap; definite order is unknown. If symptom time is $120\pm2$, then change latest 105 precedes symptom earliest 118. Precision printed to nanoseconds cannot overcome an unsynchronized source clock.

Late events should render at event time with a visible late-data indicator, not at observed time as though the change happened on ingestion. Corrections append a new revision or supersession link. Mutating history invisibly destroys reproducibility of past investigations.

**Align scope before time.** A database change in region A is not a plausible direct cause of a symptom isolated to untouched region B without an additional mechanism. Intersect target sets, tenants, routes, releases, resources, and time. Normalize identity through the same resource vocabulary used by metrics and traces.

Temporal overlap $R$ is a screening measure. An overlap of one says the change window covers the anomaly, not that it caused it. Zero overlap may reject a direct immediate-effect hypothesis but not delayed queues, cache expiry, resource leaks, or irreversible data mutation. Mechanism determines the relevant lag.

Build a candidate table containing change, overlap, scope intersection, plausible lag, mechanism evidence, unchanged comparison, rollback or roll-forward response, and confounders. Keep simultaneous changes visible. Choosing the most convenient annotation after observing the incident creates confirmation bias.

**Use comparisons carefully.** Before a rollout, define primary signals, guardrails, window, minimum traffic, and candidate/control allocation. Compare like populations and account for seasonality and shared dependencies. A before/after difference

$$
\Delta=\bar y_{after}-\bar y_{before}
$$

mixes the change with every other time-varying factor. A candidate-control difference can reduce common effects, but routing bias, interference, low counts, and concurrent changes remain.

Recovery after rollback strengthens a causal hypothesis when scope, timing, and mechanism agree. It is not conclusive: traffic may have fallen, a dependency may have recovered, caches may have warmed, or operators may have changed several controls. Record all interventions so the evidence can be evaluated.

The following deterministic model screens change windows and checks definite precedence under bounded clock error. It does not perform causal inference.

<!-- bijux-verify: {"id":"change-window-screen","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"overlap: 60 s\noverlap ratio: 75.00%\ndefinite precedence: True\nrecovery after rollback: 20 s\n","stderr":""}} -->
```python
change = (100, 180)
anomaly = (120, 200)
overlap = max(0, min(change[1], anomaly[1]) - max(change[0], anomaly[0]))
ratio = overlap / (anomaly[1] - anomaly[0])

change_time, change_error = 100, 5
symptom_time, symptom_error = 120, 2
definitely_before = change_time + change_error < symptom_time - symptom_error

rollback_time = 180
recovery_time = 200
print("overlap:", overlap, "s")
print(f"overlap ratio: {ratio:.2%}")
print("definite precedence:", definitely_before)
print("recovery after rollback:", recovery_time - rollback_time, "s")
```

**Design delivery and storage.** Emit from the authoritative mechanism whenever possible: deployment controller, configuration store, flag service, traffic control, database migrator, or privileged operations gateway. Chat and ticket systems may add context but should not invent canonical application state.

Use an outbox, durable controller history, or equivalent coupling when losing a change event would be dangerous. Specify at-least-once delivery and deduplication rather than claiming exactly once. Monitor production-to-event delay, duplicates, rejects, schema errors, clock quality, missing lifecycle transitions, and orphaned changes.

Project canonical events into annotations. A chart marker should link back to the immutable event identity and expose kind, scope, state, version, and uncertainty. Different charts may filter the same event stream. Do not copy manually edited labels into each dashboard as independent truth.

Retain a bounded searchable view for diagnosis and a separately governed audit record where required. Audit needs may demand authorization evidence, tamper resistance, longer retention, and restricted access. An observability pipeline optimized for sampling and transformation cannot silently claim those guarantees.

**Test the history.** Drive a controlled rollout through success, partial failure, retry, rollback, delayed event delivery, duplicate delivery, and correction. Assert lifecycle transitions, identities, actual target sets, ordering constraints, timestamps, schema versions, and annotation rendering. Join known metrics and traces by target and release, then confirm that the tool shows ambiguity when two changes collide.

## Definitions and Notation

Let change $c=(i,k,T,a,v_0,v_1,[s,e),o,p)$ have identity $i$, kind $k$, target set $T$, actor or automation $a$, prior and desired versions $v_0,v_1$, effect interval $[s,e)$, outcome $o$, and provenance $p$. Let anomaly $A=[u,w)$ with $w>u$.

Overlap length is $L=\max(0,\min(e,w)-\max(s,u))$ and anomaly overlap ratio is $R=L/(w-u)$. Let symptom scope be $S$; direct scope relevance requires $T\cap S\ne\varnothing$, subject to indirect mechanisms.

A timestamp estimate is $(t,\epsilon)$ with possible real interval $[t-\epsilon,t+\epsilon]$. Change definitely precedes anomaly onset only when $t_c+\epsilon_c<t_a-\epsilon_a$. Otherwise precedence may still be true but is not established by these timestamps.

For controlled expected event identities $E$ and observed identities $O$, completeness is $|E\cap O|/|E|$ for nonempty $E$. Production expected sets are rarely known; lifecycle invariants and source reconciliation provide bounded evidence.

## Mechanisms, Invariants, or Proof Structure

**Overlap derivation.** Two half-open intervals intersect from the later start to the earlier end. If that end does not exceed the start, length is zero; otherwise subtraction gives $L$. Dividing by anomaly duration normalizes screening across incidents.

**Non-causation argument.** Positive overlap and intersecting scope are compatible with cause, common cause, coincidence, reverse response, or a second simultaneous change. Since multiple models yield the same observation, overlap alone cannot identify cause.

**Uncertainty argument.** If the latest possible change time is earlier than the earliest possible symptom time, precedence holds for every admissible realization. If uncertainty intervals overlap, some realizations reverse the printed order; definite precedence is unavailable.

**Lifecycle invariant.** `verified` requires an earlier applied state for the relevant target and named evidence. `rolled_back` requires a rollback transition and a restored or replacement version. A controller retry may duplicate delivery but must not create a second logical application.

**Correction invariant.** Append-only correction with `supersedes` preserves what investigators previously saw and which value is current. In-place overwrite cannot prove either history from the resulting record alone.

**Comparison limitation.** Before/after difference identifies a temporal association under the chosen windows. Causal interpretation additionally needs exchangeable comparison, controlled assignment, or defensible assumptions about confounding and interference.

## Alternatives and Trade-Offs

1. **Point marker versus effect window.** A point is compact; a window represents rolling exposure but demands target-level state.
2. **Central emission versus source emission.** Central gateways standardize schemas; authoritative sources better know actual application. Reconcile both through provenance.
3. **Fine target events versus aggregation.** Per-instance detail diagnoses partial rollout; it may overwhelm storage. Region or cohort summaries need completeness counters.
4. **Generic envelope versus domain schema.** A portable envelope eases transport; domain fields define change meaning. Use both layers.
5. **Mutable record versus superseding event.** Mutation simplifies current queries; append-only supersession preserves investigation history.
6. **Automatic annotation versus manual note.** Automation is complete and structured; human notes capture context. Manual text cannot replace state evidence.
7. **Before/after versus concurrent control.** Before/after is easy but confounded by time. Controls reduce some confounding but can suffer selection and interference.
8. **Observability retention versus audit retention.** Short searchable retention controls cost; regulated evidence may require separate durable controls.
9. **One universal schema versus versioned families.** Universality simplifies joins but erases mechanism. Versioned families preserve semantics with migration cost.

## Failure Modes and Misconceptions

1. **“A deploy is one instant.”** Rolling exposure spans targets and time.
2. **“Requested means applied.”** Intent, mechanism, and observed state differ.
3. **“Controller success proves service health.”** Verification requires independent evidence.
4. **“Nearby annotations prove cause.”** Proximity only creates a candidate.
5. **“No annotation means no change.”** The event path may be incomplete.
6. **“Observed time is event time.”** Ingestion can be delayed and reordered.
7. **“Nanosecond text means nanosecond accuracy.”** Clock uncertainty dominates formatting.
8. **“Rollback recovery proves the release caused it.”** other interventions and time effects may explain recovery.
9. **“Feature enabled describes exposure.”** Eligibility, assignment, evaluation, and delivery can differ.
10. **“Every reconciler loop deserves an event.”** Noisy observations need governed aggregation.
11. **“Same event twice means two changes.”** At-least-once delivery creates duplicates.
12. **“Overwrite fixes a bad record.”** It erases investigation history.
13. **“An annotation is an audit log.”** Integrity, authorization, and retention guarantees differ.
14. **“Free text is enough.”** It cannot reliably join scope, identity, version, and state.
15. **“Record the full configuration for convenience.”** It can expose secrets and sensitive policy.
16. **“One global timeline has one clock.”** Sources have offset, drift, and ingestion delay.

## Worked Examples

### Example 1

**Point versus window.** A deployment starts at 10:00, reaches region A at 10:03, region B at 10:08, and completes at 10:12. One 10:00 marker falsely implies simultaneous exposure. Record the overall lifecycle and actual regional windows. **Conclusion:** diagnosis uses real exposure, not button-click time.

### Example 2

**Overlap calculation.** Change window $[100,180)$ and anomaly $[120,200)$ intersect for 60 seconds. Anomaly duration is 80, so $R=60/80=75\%$. **Conclusion:** the change is temporally plausible for much of the anomaly, not proven causal.

### Example 3

**Clock uncertainty.** Change $100\pm5$ and symptom $108\pm5$ yield intervals $[95,105]$ and $[103,113]$, which overlap. Printed order is not definite. **Conclusion:** retain uncertainty instead of manufacturing precedence.

### Example 4

**Definite precedence.** Change $100\pm5$ and symptom $120\pm2$ give latest change 105 and earliest symptom 118. Since $105<118$, precedence holds under the bounds. **Conclusion:** precedence is established, while causation remains open.

### Example 5

**Duplicate delivery.** A controller times out after emitting event `e7` and retries the same payload with `e7`. The receiver upserts by event ID but increments a duplicate counter. **Conclusion:** delivery retry does not create a new logical change.

### Example 6

**Partial rollout.** Desired version reaches 70 of 100 instances before health failure. Recording `deployment.failed` alone loses exposure. Target summaries record 70 candidate, 30 control, rollback start, and eventual restored counts. **Conclusion:** actual target state supports comparison and remediation.

### Example 7

**Change collision.** Latency rises while a release reaches region A, traffic weight doubles, and a dependency announces degradation. Candidate analysis retains all three, compares untouched region B, checks dependency spans, and tests rollback response. **Conclusion:** a timeline must show ambiguity rather than select one story.

### Example 8

**Feature configuration versus evaluation.** A flag becomes 10% enabled at noon, but cached clients refresh over 30 minutes. The configuration event marks rule change; trace attributes record evaluated generation and result. **Conclusion:** configured percentage and actual exposure are different evidence.

### Example 9

**Late annotation.** A regional failover occurs at 14:00 but its event arrives at 14:07. The chart renders the marker at event time, indicates seven-minute delivery lag, and preserves observed time. **Conclusion:** late evidence must not rewrite occurrence time.

### Example 10

**Sensitive configuration.** A certificate rotation event is useful, but private key bytes and operator email are not. Record certificate version or approved fingerprint, target, automation identity, result, and secure provenance reference. **Conclusion:** diagnostic utility does not justify secret disclosure.

## Cross-Program Connections

1. SDRE release modules define the mechanisms whose state transitions become change events.
2. [SDRE-032](032-structured-logging.md) owns the generic structured record and audit separation.
3. [SDRE-033](033-metrics-and-dimensionality.md) supplies release, region, and cohort comparison dimensions.
4. [SDRE-034](034-distributed-tracing.md) links a request to the configuration or release it actually observed.
5. Software Architecture owns boundaries used as change targets.
6. Database Engineering owns schema and migration state; this module records operational application evidence.
7. Data Engineering owns event transport and transformation at scale.
8. Security Engineering owns authorization, tamper evidence, secret handling, and audit requirements.
9. Platform Engineering owns shared deployment, configuration, and annotation products.
10. Distributed Systems Engineering owns clocks and causality; this module applies bounded uncertainty to operational timelines.

## References

1. OpenTelemetry, “Logs Data Model,” OpenTelemetry Specification 1.60.0, Stable, retrieved 2026-09-06. https://opentelemetry.io/docs/specs/otel/logs/data-model/
2. OpenTelemetry, “Semantic conventions for events,” Development status, retrieved 2026-09-06. https://opentelemetry.io/docs/specs/semconv/general/events/
3. OpenTelemetry, “Telemetry Schemas,” current specification with stated scope and work-in-progress limitations, retrieved 2026-09-06. https://opentelemetry.io/docs/specs/otel/schemas/
4. Cloud Native Computing Foundation, *CloudEvents Specification*, version 1.0.2, 2022. https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md
5. Google, “Release Engineering and Canarying,” *Site Reliability Engineering Workbook*, retrieved 2026-09-06. https://sre.google/workbook/canarying-releases/
6. Google, “Monitoring Distributed Systems,” *Site Reliability Engineering*, retrieved 2026-09-06. https://sre.google/sre-book/monitoring-distributed-systems/
7. IETF, RFC 3339, “Date and Time on the Internet: Timestamps,” July 2002. https://www.rfc-editor.org/rfc/rfc3339
8. NIST, SP 800-128, *Guide for Security-Focused Configuration Management of Information Systems*, updated 2019, retrieved 2026-09-06. https://csrc.nist.gov/pubs/sp/800/128/upd1/final

## Exercises

### Exercise 1

Define event ID, change ID, attempt ID, event time, observed time, target set, and provenance. Explain why none alone proves application success.

### Exercise 2

Change window is $[40,100)$ and anomaly is $[70,130)$. Compute overlap length and anomaly overlap ratio. If the change timestamp is $40\pm4$ and anomaly onset $47\pm3$, is precedence definite?

### Exercise 3

A dashboard shows deploy start but not target application, duplicates rollback markers, and places delayed events at ingestion time. Diagnose the schema and pipeline faults and propose focused tests.

### Exercise 4

Design events for a progressive flag rollout with 1%, 10%, 50%, and 100% stages, cached evaluation, rollback, and candidate/control comparison. Separate global events from request evidence.

### Exercise 5

A self-healing platform changes replicas, routes traffic, restarts instances, and modifies circuit-breaker thresholds during an outage. Design a bounded event history that supports causal investigation without emitting every controller reconciliation.

## Answers to the Exercises

### Answer 1

Event ID identifies one occurrence for deduplication. Change ID joins the intended lifecycle. Attempt ID distinguishes mechanism retries. Event time estimates occurrence; observed time records reception. Target set declares exposed scope. Provenance identifies the authoritative source record and mechanism. Success additionally requires a valid transition, actual application to intended targets, and named verification evidence; none of the individual fields establishes all of those facts.

### Answer 2

Intersection is $[70,100)$, length 30. Anomaly duration is 60, so overlap ratio is $30/60=50\%$. Change time lies in $[36,44]$ and anomaly onset in $[44,50]$. Definite strict precedence requires latest change $44$ to be less than earliest onset $44$; it is not. The bounds touch, so the timestamps do not establish strict precedence, although the change remains a candidate.

### Answer 3

The schema confuses intent/start with actual exposure, lacks stable event IDs or receiver deduplication, and maps observed time into event time. Add lifecycle names, change/event/attempt IDs, target application windows, event and observed timestamps, rollback linkage, and provenance. Test a controlled regional rollout, duplicate replay, delayed delivery, reordering, and correction. Assert one logical annotation per event ID, rendering at event time with lag visible, and target-level exposure independent of overall controller state.

### Answer 4

Emit stable `flag.rollout_stage_started`, `flag.rule_applied`, `flag.stage_verified`, and rollback events under one change ID, with rule generation, prior generation, eligible population definition, allocation salt/version, intended percentage, actual effective interval, target scope, and guardrail result. Do not emit one global event per request. Attach bounded evaluated generation and variant to sampled traces or governed logs, and aggregate exposure/outcome with metrics. Candidate/control comparisons use stable assignment and comparable populations. Cached clients require distribution-lag evidence before a stage is called fully applied.

### Answer 5

Create one incident/intervention correlation identity without pretending it is one atomic change. Emit material transitions: replica target changed and reached, traffic policy version applied, instance replacement summary by failure domain, circuit-breaker policy version applied, and each rollback or supersession. Aggregate repetitive reconciliation into interval summaries with attempted count, successful count, remaining divergence, first/last time, and affected target set; retain detailed controller logs separately for bounded time. Record automation identity, reason code, old/new state, source revision, clock uncertainty, and verification. A candidate table then evaluates overlapping interventions and mechanisms. A strong answer preserves distinct controllers and state transitions, exposes concurrency, bounds volume, and does not infer cause from the shared incident ID.
