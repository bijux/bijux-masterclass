---
module_id: SDRE-031
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 31
title: Observability Versus Monitoring
status: complete
last_verified: 2026-09-06
---

# Observability Versus Monitoring

## One-Page Review

### Governing question

How should engineers distinguish monitoring from observability so that a service both detects important conditions and supports disciplined investigation of states and failures that were not encoded in advance?

### Essential definitions

- **system state** is the set of internal facts relevant to a question at a time or over an interval;
- an **output** is externally available evidence produced by or about the system;
- **telemetry** is machine-produced data about behavior, such as metrics, logs, traces, events, and profiles;
- **instrumentation** is code or configuration that creates, enriches, and exports telemetry;
- **monitoring** collects, processes, aggregates, displays, and evaluates selected observations for known operational purposes;
- **observability**, in control theory, is a model-relative property: distinct relevant states can be distinguished from outputs over time;
- **operational observability** is the bounded capability to ask useful questions of a running system and distinguish plausible hypotheses with available evidence;
- a **monitor** is a predeclared evaluation that maps observations to a state, notification, or automated action;
- a **symptom** is user-visible deviation; a **cause** is a condition that contributes to it;
- **black-box evidence** observes externally visible behavior; **white-box evidence** exposes internals;
- **semantic context** gives a value meaning: identity, operation, version, unit, time, and relevant dimensions;
- **telemetry completeness** states whether expected evidence arrived with usable scope and timing.

### Central model, mechanism, or theorem

For a finite hypothesis set $H$ and question $q$, let observation function $g_q(h)$ return the evidence that would be visible under hypothesis $h$. Two hypotheses are indistinguishable when $g_q(h_i)=g_q(h_j)$. Evidence supports the question only if important competing hypotheses fall into different equivalence classes.

For a linear time-invariant model

$$
x_{t+1}=Ax_t,\qquad y_t=Cx_t,
$$

the $n$-state system is observable over $n$ samples exactly when the observability matrix

$$
\mathcal{O}=\begin{bmatrix}C\\CA\\\vdots\\CA^{n-1}\end{bmatrix}
$$

has rank $n$. This theorem is a calibration, not a claim that production software is a known linear system.

### Critical invariants

- monitoring and observability overlap; they are not rival products or disjoint telemetry stacks;
- every claim names its question, system boundary, state, outputs, interval, and assumptions;
- detecting a symptom does not identify its cause;
- more data cannot repair missing semantics, biased sampling, corrupted clocks, or inaccessible evidence;
- healthy monitors establish only their encoded predicates over received data;
- missing telemetry is an operational state, never silently equivalent to zero or health;
- black-box outcomes and white-box mechanisms complement rather than substitute for one another;
- telemetry identity and schema must survive collection, transformation, storage, and query;
- investigation preserves uncertainty and distinguishes correlation from causation;
- observability is tested against real diagnostic questions, cost, latency, privacy, and failure conditions.

### Common failures

Failures include renaming dashboards as observability, collecting three signal types without useful semantics, equating green alerts with correctness, alerting on causes while missing user symptoms, logging every field without privacy limits, using averages that hide tails, dropping rare failures through sampling, exploding metric cardinality, losing version and tenant context, treating absent data as zero, assuming a trace proves causation, instrumenting only the application while the telemetry pipeline fails, and promising that unknown failures can always be explained.

### Compact example

A checkout monitor sees normal aggregate error rate, yet some premium tenants time out. A black-box probe reproduces the symptom only for one region and feature generation. Version-tagged traces show requests waiting at a dependency; structured logs distinguish deadline cancellation from application rejection; queue-age and worker-state metrics show a stuck consumer cohort. These observations separate several hypotheses, but they do not by themselves prove why the dependency slowed. Monitoring detected and bounded the condition; operational observability made targeted investigation possible.

### Connections

[SDRE-030](030-designing-a-safe-release-pipeline.md) requires telemetry-complete release gates. [SDRE-032](../ROADMAP.md) next develops structured logging. Distributed Systems owns propagation and partial-failure models; Security Engineering owns telemetry confidentiality and integrity.

## Governing Question

The slogan “monitoring tells you when; observability tells you why” is memorable but technically weak. Monitoring can help explain mechanisms, and telemetry cannot mechanically deliver a unique why. A failure may have several contributing causes, multiple internal states may produce the same outputs, and a plausible correlation may not be causal.

A better distinction begins with questions. Monitoring evaluates selected known questions continuously: is the user-visible error budget burning, is a queue approaching its limit, did a certificate expire, did expected telemetry stop? Operational observability asks whether available outputs let an investigator distinguish the important states and hypotheses behind both expected and novel questions. Monitoring is an activity and decision system. Observability is a property or capability relative to a boundary and question. Instrumentation and telemetry support both.

The governing question is therefore not “Which tool category should we buy?” It is “Which operational decisions and investigations must this service support, which states must be distinguished, what evidence exposes them, and how will we know when that evidence is misleading or absent?”

## Why This Matters

Production systems fail outside their designers' exact predictions. A monitor can encode every known bad threshold and still miss a correctness defect, a regional cohort failure, a retry storm masked by successful responses, or an authorization leak that returns HTTP 200. Conversely, an enormous telemetry lake can fail to page anyone when users are harmed. Reliable operation needs both predeclared decisions and exploratory evidence.

Google's SRE text defines monitoring as collecting, processing, aggregating, and displaying real-time quantitative system data. It distinguishes black-box symptom evidence from white-box internal evidence and recommends latency, traffic, errors, and saturation as a compact starting set for user-facing services [1]. The same chapter says vocabulary varies. Its definitions are practical guidance, not universal law.

The OpenTelemetry observability primer currently describes observability as asking questions from outside and handling novel problems through emitted signals [2]. Its current signal documentation lists traces, metrics, logs, and baggage as supported categories; it describes events and profiles as under development or at the proposal stage on the retrieved page [3]. Those product-neutral signal categories are useful, but possessing one of each does not establish diagnostic capability. Meaning, coverage, correlation, collection reliability, retention, and query access matter more than a checklist.

The word observability also has a precise control-theory history. Kalman's state-space work relates internal state to input/output behavior and supplies rank criteria for linear models [4]. Software operations borrowed the word by analogy. The analogy teaches an essential constraint—different hidden states may be indistinguishable from chosen outputs—but production services are rarely known, deterministic, linear systems. This chapter keeps the formal and operational meanings explicit rather than borrowing a theorem's authority for an informal claim.

## Prerequisites and Retrieval

Retrieve system boundary, state, input, output, hypothesis, invariant, metric, time series, log, trace, span, event, profile, instrumentation, schema, dimension, cardinality, sampling, timestamp, clock, SLI, SLO, alert, incident, deployment generation, correlation, and causation.

From SDRE-021 through SDRE-030 retrieve production identity, environment, immutable release subjects, progressive exposure, guardrails, rollback eligibility, and completion verification. Observability evidence is meaningful only when it can be tied to the version, configuration, target, cohort, and time actually under investigation.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish formal observability, operational observability, monitoring, telemetry, and instrumentation;
2. state an observability claim relative to a question, boundary, model, outputs, interval, and assumptions;
3. use indistinguishability and the linear rank criterion as rigorous reasoning tools;
4. design monitors for user symptoms, capacity risks, evidence loss, and known invariants;
5. combine black-box and white-box evidence without confusing symptoms and causes;
6. evaluate telemetry by semantics, coverage, correlation, freshness, completeness, and queryability;
7. recognize sampling, aggregation, cardinality, clock, privacy, and pipeline failure modes;
8. conduct hypothesis-driven investigation without turning correlation into causation;
9. test whether a service supports representative diagnostic questions under stress;
10. define ownership and evidence for improving observability as a product capability.

## Core Exposition

**Begin with a boundary.** “The system is observable” is incomplete. A checkout service might be observable to its application team for request failures yet opaque to a payment provider's internals. Define the components, dependencies, users, control planes, telemetry path, and time interval inside the claim. Boundaries can nest: a database timeout is a symptom at the database boundary and a candidate cause at the checkout boundary.

**Name relevant state.** Complete physical state is neither available nor useful. Operational questions concern selected facts: running release digest, effective feature generation, request path, tenant class, queue age, dependency deadline, retry count, admission decision, database role, or saturation. Privacy and security rules may prohibit observing some facts directly. The design goal is sufficient distinction for legitimate decisions, not omniscience.

**Separate outputs from interpretations.** A log record, counter, trace span, probe result, and profile sample are outputs. “The database caused the outage” is an interpretation. Preserve raw-enough evidence, transformation lineage, units, timestamps, and uncertainty so investigators can challenge interpretations. Dashboards and alerts are queries over observations, not the observations themselves.

**Define monitoring as a decision loop.** A useful monitor has a target question, data contract, evaluation window, condition, uncertainty policy, action, owner, and validation method. It may page, create a ticket, block a rollout, invoke automation, or inform capacity planning. Collection with no consumer is telemetry accumulation; a chart with no question is decoration.

Monitors excel at known conditions requiring repeatable action. Examples include SLO burn, exhausted capacity, certificate lifetime, replication lag, invariant violation, release regression, and missing heartbeats. Encode the closest user-visible symptom practical, then retain diagnostic evidence for investigation. Alerting on every internal cause creates noise and assumes a fixed causal model.

Healthy monitor results are bounded. A five-minute error-rate rule says its query over received events did not cross its threshold. It says nothing about omitted tenants, silent telemetry loss, correctness errors classified as success, or failures shorter than aggregation resolution. State that bound in runbooks and automation.

**Define operational observability through distinction.** Let $H$ be plausible hypotheses for a question. Outputs partition $H$ into equivalence classes: hypotheses with identical observable evidence cannot be distinguished. Add evidence when an important class remains too broad. The goal is not a unique root cause for every future event; it is efficient narrowing among consequential alternatives with known limits.

Questions should traverse identity, topology, time, and causality candidates. “Why is checkout slow?” becomes: which users and regions; which release and configuration; which operations; where was time spent; which dependency and retry path; what resource was saturated; what changed; what evidence is absent? Each refinement implies semantic requirements.

An operational system is more observable when engineers can formulate these queries after an event without redeploying solely to add basic identity or correlation. Dynamic diagnostics may still be necessary. Safe runtime verbosity changes, targeted sampling, debug endpoints, and profiles extend evidence under control; claiming instrumentation will never need change is unrealistic.

**Use formal observability carefully.** In a linear time-invariant model, outputs across successive steps are $y_0=Cx_0$, $y_1=CAx_0$, and so on. Stacking them gives $Y=\mathcal{O}x_0$. If $\mathcal{O}$ has full column rank, distinct initial states produce distinct stacked outputs, so $x_0$ can in principle be recovered under the model. Rank deficiency leaves a nonzero state difference in the null space, making at least two states observationally identical.

Noise, unknown inputs, nonlinear dynamics, time variation, model error, and finite precision complicate estimation. Even full rank may be poorly conditioned: theoretically distinct states can require unrealistically precise measurement. Operational telemetry has analogous problems—rare signals, biased samples, delayed exports, and overloaded backends can make nominally present evidence practically useless.

**Combine black-box and white-box evidence.** Black-box probes exercise externally visible contracts: reachability, latency, correctness, authentication, and user workflow. They detect symptoms even when application instrumentation is broken. They may miss rare cohorts or internal precursors.

White-box telemetry exposes mechanisms: queue depth, pool wait, retry count, cache behavior, garbage collection, dependency latency, and configuration. It helps distinguish hypotheses and detect imminent problems, but internal health can be green while user outcomes fail. Place both around critical journeys. Avoid deriving the black-box result from the same internal metric, because correlated instrumentation failure defeats independence.

**Treat signal types as complementary encodings.** Metrics efficiently summarize numeric behavior across time and dimensions; they support monitors and comparisons but discard individual detail. Logs record discrete events and state transitions; structure and stable fields make them queryable. Traces connect units of work across components; sampling and broken propagation limit coverage. Profiles attribute resource consumption to code paths over samples. Events and change annotations establish temporal context. No fixed trio guarantees the answer to a question.

Choose representation from the query. Rate and distribution questions favor metrics. Exact state transitions and audit facts favor structured events. Path and latency decomposition favor traces. CPU or allocation attribution favors profiles. Correlate using stable resource, service, operation, release, region, tenant-class, and trace identities where permitted. Do not copy sensitive or unbounded values into every signal.

**Make semantics durable.** A value `37` needs a name, unit, type, temporality, aggregation, resource identity, operation, version, and collection time. Semantic conventions reduce incompatible naming, while schema versions let producers and consumers coordinate evolution. The current OpenTelemetry specification separates signal APIs, SDKs, semantic conventions, context propagation, and collection [5]. That architecture is a mechanism; teams still own domain semantics and migration.

Treat telemetry schemas like production interfaces. Review field removal, unit change, aggregation change, label normalization, and event renaming. Test queries and alerts against candidate telemetry. During migrations, dual-read or transform explicitly and measure both paths. A silently changed denominator can preserve a plausible chart while reversing its meaning.

**Preserve identity and time.** Bind every observation to the emitting resource and effective software, configuration, feature, and infrastructure generation when relevant. Capture event time and receive time separately. Record clock quality. Distributed clocks need not agree perfectly; causal context, monotonic durations, and bounded skew prevent false ordering claims.

Correlation identifiers connect evidence across services and asynchronous work. Propagate them through queues and retries without using sensitive business identifiers as universal keys. Record attempt identity separately from logical operation identity so duplicates and retries remain visible.

**Engineer the telemetry path.** Instrumentation can block, allocate, recurse, expose secrets, or amplify failure. Use bounded buffers, explicit backpressure or drop policy, batching, timeouts, and tested shutdown. Define whether critical audit evidence has stronger durability than diagnostic debug data. The service should not fail catastrophically merely because an optional exporter is unavailable.

Observe the observers. Measure instrumentation errors, queue occupancy, dropped records, export latency, collector health, schema rejection, sampling decisions, storage lag, query errors, and retention. Send an independent heartbeat or synthetic signal through the entire path. Missing telemetry must be distinguishable from a genuine zero.

**Control volume and cardinality.** Metric series scale approximately with the product of label value counts, not with the number of label names. A label set with $100$ endpoints, $20$ regions, $50$ status details, and $10{,}000$ customer IDs can imply up to one billion combinations before time samples. Actual sparsity helps, but unbounded identifiers remain unsafe metric dimensions.

Aggregate intentionally. Keep bounded dimensions for continuous monitoring, exemplars or links to sampled detail, and targeted logs or traces for investigation. Sampling policies must preserve rare errors, high latency, security events, and important cohorts. Record inclusion probability when statistical estimation uses samples. Tail sampling can retain completed anomalous traces but requires buffering and still depends on correct context.

**Protect people and systems.** Telemetry can contain credentials, tokens, payloads, personal data, source paths, query text, and internal topology. Minimize collection, classify fields, redact at the earliest reliable point, restrict access, encrypt transport and storage, audit queries, set retention, and test deletion. High diagnostic value does not erase legal, contractual, or ethical limits.

Integrity matters too. An attacker or broken service can suppress, forge, or flood telemetry. Separate security audit channels where justified, authenticate producers, rate-limit untrusted attributes, and preserve tamper-evident records for critical decisions. NIST SP 800-137 frames information-security continuous monitoring as a strategy for visibility, risk awareness, and timely response; it does not make generic application telemetry a compliance program [7]. Observability access is production access.

**Investigate scientifically.** Start from impact and timeline. List hypotheses and predictions: if workers are dead, queue age should rise while dequeue rate falls; if the database is slow, both client and server views should show increased service time; if the network is at fault, the views may diverge. Query evidence that discriminates, then update confidence. Google's troubleshooting chapter similarly recommends a methodical account of what is known, unknown, and needed while warning that correlation is not causation [6].

Correlation proposes hypotheses. It does not prove causation. A deployment and latency increase may share traffic growth as a cause. A slow downstream span may include client queueing. A retry counter may rise because of, rather than cause, saturation. Interventions, controlled comparisons, causal mechanism, and eliminated alternatives strengthen conclusions.

**Test the capability.** Build an observability question inventory from architecture and failure modes. For each question, record required identities, signals, queries, freshness, retention, privacy, expected cost, and fallback. During game days and real incidents, measure time to detect, time to orient, hypotheses eliminated, missing evidence, misleading evidence, and query accessibility.

An observability acceptance test injects or simulates a bounded condition and asks an engineer unfamiliar with the implementation to identify affected users, version, path, failure state, and safe next action using documented access. The score is not “three dashboards exist.” It is whether evidence supports the decision within the operational time budget without unsafe access.

## Definitions and Notation

Let $B$ be a declared system boundary, $S_B$ its relevant internal states, $U$ known inputs, and $Y$ available outputs during interval $T$. An observability claim is relative to $(B,S_B,U,Y,T,M)$, where $M$ is the assumed model. Changing the boundary, desired state detail, outputs, interval, or model can change the result.

For a finite diagnostic question $q$ with plausible hypotheses $H_q$, define observation function $g_q:H_q\rightarrow Y_q$. Relation

$$
h_i\sim_q h_j \iff g_q(h_i)=g_q(h_j)
$$

partitions hypotheses into observational equivalence classes. A decision-relevant pair is distinguishable only when its observations differ beyond stated noise and uncertainty.

For finite $|H_q|\ge2$, a useful local coverage measure is

$$
D_q=\frac{\left|\left\{\{h_i,h_j\}:g_q(h_i)\ne g_q(h_j)\right\}\right|}{\binom{|H_q|}{2}}.
$$

$D_q$ is a bounded design heuristic for an enumerated question, not a universal observability score. It ignores hypothesis probability, consequence, query cost, measurement noise, and human interpretation.

For an $n$-dimensional linear time-invariant system $x_{t+1}=Ax_t$, $y_t=Cx_t$, the observability matrix is $\mathcal{O}=[C^T,(CA)^T,\ldots,(CA^{n-1})^T]^T$. Full column rank $n$ implies unique reconstruction of the initial state in the ideal model.

## Mechanisms, Invariants, or Proof Structure

**Indistinguishability argument.** If two relevant hypotheses produce identical available outputs, no algorithm restricted to those outputs can always choose correctly between them. Better visualization of the same evidence cannot add the missing distinction. The remedy requires another output, input knowledge, a stronger model, or an explicitly uncertain decision.

**Linear rank argument.** Stacking $n$ outputs produces $Y=\mathcal{O}x_0$. If $\mathcal{O}$ has rank $n$, its null space contains only zero, so $\mathcal{O}x_a=\mathcal{O}x_b$ implies $x_a=x_b$. If rank is less than $n$, a nonzero $v$ exists with $\mathcal{O}v=0$; states $x$ and $x+v$ therefore produce the same stacked outputs.

**Monitoring bound.** A monitor computes predicate $P(Q(Y_T))$ from query $Q$ over received observations in interval $T$. A green result proves only that the computation did not trigger under its data and semantics. If collection is incomplete, the query is biased, or the predicate omits a failure, green cannot establish service correctness.

**Telemetry multiplicity argument.** Adding another signal type does not necessarily refine hypothesis classes. If a new log and an existing metric are derived from the same faulty counter, both fail together and provide no independent distinction. Diversity is valuable when semantics, vantage points, and failure modes differ.

**Causal restraint.** Observations can falsify predictions and alter relative confidence. They rarely prove a unique causal graph from passive data alone. Record confirmed facts, inferred mechanisms, alternatives, and unknowns separately.

The following deterministic model makes equivalence classes explicit. It is not a monitoring backend or proof about real incidents.

<!-- bijux-verify: {"id":"hypothesis-distinction","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"monitor classes: [['dead-workers', 'healthy', 'slow-dependency']]\ndiagnostic classes: [['dead-workers'], ['healthy'], ['slow-dependency']]\nmonitor distinguishing pairs: 0/3\ndiagnostic distinguishing pairs: 3/3\n","stderr":""}} -->
```python
from itertools import combinations

states = {
    "healthy": {"error_rate": 0.001, "queue_age": 1, "workers": 4, "dependency_p99": 30},
    "dead-workers": {"error_rate": 0.001, "queue_age": 120, "workers": 0, "dependency_p99": 30},
    "slow-dependency": {"error_rate": 0.001, "queue_age": 120, "workers": 4, "dependency_p99": 800},
}

def partition(fields):
    classes = {}
    for name, state in states.items():
        signature = tuple(state[field] for field in fields)
        classes.setdefault(signature, []).append(name)
    return sorted(sorted(group) for group in classes.values())

def distinguishable(fields):
    pairs = list(combinations(sorted(states), 2))
    count = sum(
        tuple(states[a][field] for field in fields)
        != tuple(states[b][field] for field in fields)
        for a, b in pairs
    )
    return count, len(pairs)

monitor = ("error_rate",)
diagnostic = ("error_rate", "queue_age", "workers", "dependency_p99")
print("monitor classes:", partition(monitor))
print("diagnostic classes:", partition(diagnostic))
print("monitor distinguishing pairs: %d/%d" % distinguishable(monitor))
print("diagnostic distinguishing pairs: %d/%d" % distinguishable(diagnostic))
```

## Alternatives and Trade-Offs

**Known-condition monitoring versus exploratory query.** Precomputed monitors are fast, cheap, repeatable, and actionable for known risks. Exploratory systems preserve richer evidence for unanticipated questions but cost more and require skill. Use both; do not page on arbitrary exploratory queries.

**Black-box versus white-box evidence.** Black-box probes align with user contracts and survive some instrumentation failures. White-box evidence narrows mechanisms and reveals precursors. Independent vantage points cost more but reduce common-mode blind spots.

**Pre-aggregation versus raw detail.** Aggregation makes continuous evaluation affordable and protects privacy when dimensions are controlled. It erases individual paths and distribution structure. Preserve bounded drill-down routes rather than retaining every raw event indefinitely.

**Head versus tail sampling.** Head sampling decides early and uses bounded resources but may discard later failures. Tail sampling can retain anomalous completed traces but buffers state, adds latency, and can fail under overload. Hybrid policies reserve errors, slow work, important cohorts, and a known-probability baseline sample.

**Push versus pull collection.** Pull makes target discovery and scrape failure explicit and centralizes cadence. Push supports short-lived or disconnected producers. Either requires identity, backpressure, loss accounting, and independent health checks; transport choice does not settle semantics.

**Automatic versus manual instrumentation.** Automatic instrumentation gives broad, consistent library coverage quickly. Manual domain events express business invariants and state transitions. Automatic spans cannot infer every domain meaning; manual code can drift or leak data. Layer them with reviewed conventions.

**Centralized versus federated ownership.** A platform can own transport, storage, access control, and common schemas. Service teams know domain questions. Central-only design becomes generic and shallow; service-only design duplicates infrastructure and fragments meaning. Publish explicit shared and local responsibilities.

**Always-on versus dynamically enabled detail.** Always-on evidence supports post-event investigation but consumes resources and expands privacy risk. Dynamic detail reduces steady cost but cannot recover past facts and may worsen an incident. Keep minimum viable diagnostic identity always on and gate targeted expansion safely.

**Vendor-specific versus portable semantics.** Vendor features can accelerate queries and correlation. Stable domain fields, open protocols, and export tests reduce lock-in and disaster risk. Portability has engineering cost and does not imply lowest-common-denominator instrumentation.

## Failure Modes and Misconceptions

1. **“Monitoring is legacy; observability replaces it.”** Known-condition monitoring and alerting remain necessary operational decision mechanisms.
2. **“Metrics, logs, and traces equal observability.”** Signal categories do not prove semantic coverage or diagnostic distinction.
3. **“Green means healthy.”** It means selected predicates did not fire over selected received evidence.
4. **“More telemetry is always better.”** Volume can add cost, noise, privacy exposure, overload, and slower investigation.
5. **“Every event should carry customer ID as a metric label.”** Unbounded cardinality can exhaust the monitoring system and expose data.
6. **“A trace shows the root cause.”** It records an observed path under sampling and propagation; causal interpretation remains work.
7. **“Logs are ground truth.”** Logs are produced by code, clocks, buffers, sampling, and schemas that can be wrong.
8. **“No data means zero.”** It may mean exporter failure, filter rejection, lag, outage, or absence of traffic.
9. **“White-box health replaces user probes.”** Internals can be green while routing, policy, content, or an external dependency harms users.
10. **“Black-box probes explain mechanisms.”** They establish contract outcomes and require internal evidence for discrimination.
11. **“Averages summarize latency.”** They can hide severe tails and cohort-specific failures.
12. **“Correlation IDs create causality.”** They connect records; they do not prove why events occurred.
13. **“Instrumentation is free.”** It consumes CPU, memory, network, storage, and operator attention and can affect the measured system.
14. **“The telemetry backend is outside the system.”** Its loss, lag, schema, and access are part of operational evidence quality.
15. **“Formal observability proves software debuggability.”** The rank theorem assumes a declared linear model and outputs; software usage is an analogy unless those assumptions hold.
16. **“Unknown unknowns will always be answerable.”** Novel queries are bounded by retained evidence, semantics, access, and physical indistinguishability.

## Worked Examples

### Example 1

**Situation.** A probe checks that `POST /checkout` returns HTTP 200. A release returns 200 but silently applies the wrong tax rate to one jurisdiction.

**Reasoning.** The monitor observes reachability and status, not the business invariant. Its green result is valid only for that predicate. Add a bounded synthetic correctness probe and a domain event containing tax-rule generation and jurisdiction class without personal data. Compare computed totals with an independently specified oracle.

**Conclusion.** Availability monitoring does not establish semantic correctness; the monitored contract must include consequential outcomes.

### Example 2

**Situation.** Let $A=\begin{bmatrix}1&1\\0&1\end{bmatrix}$ and $C=\begin{bmatrix}1&0\end{bmatrix}$ for state $x=[position,velocity]^T$.

**Reasoning.** The two-sample matrix is

$$
\mathcal{O}=\begin{bmatrix}C\\CA\end{bmatrix}=\begin{bmatrix}1&0\\1&1\end{bmatrix}.
$$

Its determinant is $1$, so rank is $2$. From $y_0=position$ and $y_1=position+velocity$, infer $velocity=y_1-y_0$. If instead $A=I$ with the same $C$, both rows would be $[1,0]$ and velocity would be unobservable.

**Conclusion.** Observability depends on both dynamics and outputs; measuring one component can reveal another only through an applicable model.

### Example 3

**Situation.** The executable model shows identical current error rate for healthy, dead-worker, and slow-dependency states.

**Reasoning.** The error-rate monitor places all three hypotheses in one equivalence class, so $D_q=0/3=0$. Queue age separates health from both failures; worker count and dependency latency separate the two failure mechanisms. With all four observations, $D_q=3/3=1$ for this enumerated set.

**Conclusion.** A monitor may be correct yet insufficient for diagnosis; add question-specific distinctions rather than arbitrary volume.

### Example 4

**Situation.** Error count falls to zero exactly when collector queue occupancy reaches its limit.

**Reasoning.** Two hypotheses fit: the service stopped failing, or error records were dropped. Export-success count, dropped-record count, end-to-end heartbeat, and independent black-box probe distinguish them. A rule that divides errors by received requests without completeness checks can report perfect success on no data.

**Conclusion.** Monitor telemetry completeness independently and make missing denominators an unavailable state.

### Example 5

**Situation.** A proposed request metric labels endpoint (100 values), region (20), detailed status (50), and customer ID (10,000).

**Reasoning.** The Cartesian upper bound is $100\times20\times50\times10{,}000=1{,}000{,}000{,}000$ series. Sparse traffic reduces active combinations but does not bound customer growth. Keep endpoint, region, and a small status class in metrics. Put authorized customer detail in sampled structured events or traces with access controls.

**Conclusion.** Preserve bounded dimensions for continuous monitoring and route high-cardinality detail through controlled diagnostic stores.

### Example 6

**Situation.** A latency field changes from milliseconds to seconds while its name remains `request_latency`.

**Reasoning.** Existing dashboards still render numbers, but thresholds and historical comparisons become wrong by a factor of $1{,}000$. Version the schema, introduce the new unit explicitly, test transformations, dual-read during transition, and annotate the cutover. Unit metadata must travel with the value.

**Conclusion.** Syntactically valid telemetry can be semantically false; schema compatibility is an operational correctness concern.

### Example 7

**Situation.** Uniform head sampling retains 1% of traces. A premium route contributes only 40 requests during an incident and fails 25% of them.

**Reasoning.** Expected retained traces from the route are $40\times0.01=0.4$; seeing none is unsurprising. Preserve all errors where feasible, define cohort-aware minimum samples, keep aggregate SLI counts unsampled, and record sampling probability. Tail selection can help if completion and buffers survive the incident.

**Conclusion.** Sampling policy is part of the evidence claim; rare high-impact behavior needs explicit protection.

### Example 8

**Situation.** Application metrics report low latency, but an external probe reports a slow checkout.

**Reasoning.** The application timer starts after gateway admission, excluding queueing, DNS, TLS, and gateway policy. Compare timestamps and scopes, then add gateway and client-path evidence. The discrepancy is useful: it narrows hidden time to the unmeasured path rather than showing that one source must be false.

**Conclusion.** Different vantage points require aligned boundaries before comparison and can expose measurement gaps.

### Example 9

**Situation.** Database latency and application retries rise together after a deployment.

**Reasoning.** Candidate hypotheses include a slow database causing retries, aggressive retries saturating the database, and shared traffic growth causing both. Check request volume, retry policy by release, database service time versus queue time, control cohorts, and a bounded retry intervention. A timestamp-aligned chart alone cannot select the causal direction.

**Conclusion.** Telemetry supports competing predictions; causal conclusions require mechanism and discriminating evidence.

### Example 10

**Situation.** A team adds asynchronous fulfillment and claims it is observable because a queue-depth dashboard exists.

**Reasoning.** Test bounded scenarios: stuck workers, poison messages, duplicated delivery, delayed dependency, and telemetry exporter failure. Ask an engineer to identify affected order class, logical message and attempt, producer release, consumer release, queue age distribution, retry/dead-letter state, and safe containment. Measure time and missing evidence. Protect order identity and payload privacy.

**Conclusion.** Acceptance is demonstrated question coverage under failure, not the existence of a dashboard.

## Cross-Program Connections

1. **Distributed Systems (DIST):** supplies partial failure, causal ordering, retry, and propagation models that bound telemetry interpretation.
2. **Systems Engineering (SYSENG):** supplies state estimation, feedback, sensor coverage, and boundary reasoning.
3. **Operating Systems (OS):** supplies scheduler, memory, I/O, clock, and profiling mechanisms behind host evidence.
4. **Networking (NET):** supplies path, loss, latency, naming, and transport behavior that application-only evidence can hide.
5. **Database Engineering (DBE):** supplies query, lock, log, replication, and transaction state needed to distinguish data-path failures.
6. **Data Engineering (DE):** supplies collection pipelines, schemas, late data, quality, and retention mechanisms for telemetry.
7. **Security Engineering (SEC):** owns sensitive-data minimization, access, producer authenticity, integrity, and abuse detection.
8. **Platform Engineering (PLAT):** owns common instrumentation, collection, storage, query, and service onboarding mechanisms.
9. **API and Service Engineering (API):** defines external contracts and identity propagation across service boundaries.
10. **Software Testing and Quality Engineering (STQE):** supplies oracles, fault injection, coverage, and acceptance methods for observability tests.

## References

1. Rob Ewaschuk, “Monitoring Distributed Systems,” in *Site Reliability Engineering*, O'Reilly Media, 2016. <https://sre.google/sre-book/monitoring-distributed-systems/>. Accessed 2026-09-06.
2. OpenTelemetry Authors, “Observability Primer,” last modified 2026-04-23 on the retrieved page. <https://opentelemetry.io/docs/concepts/observability-primer/>. Accessed 2026-09-06.
3. OpenTelemetry Authors, “Signals,” last modified 2026-03-10 on the retrieved page. <https://opentelemetry.io/docs/concepts/signals/>. Accessed 2026-09-06.
4. R. E. Kalman, “Mathematical Description of Linear Dynamical Systems,” *Journal of the Society for Industrial and Applied Mathematics, Series A: Control*, vol. 1, no. 2, pp. 152–192, 1963, DOI 10.1137/0301010. <https://epubs.siam.org/doi/10.1137/0301010>.
5. OpenTelemetry Authors, “OpenTelemetry Specification 1.60.0,” current version retrieved 2026-09-06. <https://opentelemetry.io/docs/specs/otel/>.
6. Betsy Beyer et al., eds., “Effective Troubleshooting,” in *Site Reliability Engineering*, O'Reilly Media, 2016. <https://sre.google/sre-book/effective-troubleshooting/>. Accessed 2026-09-06.
7. Kelley Dempsey et al., *Information Security Continuous Monitoring (ISCM) for Federal Information Systems and Organizations*, NIST SP 800-137, September 2011. <https://doi.org/10.6028/NIST.SP.800-137>.

## Exercises

### Exercise 1

Define monitoring, telemetry, instrumentation, formal observability, and operational observability. Explain why none is a synonym for a telemetry product.

### Exercise 2

For $A=\begin{bmatrix}1&0\\1&1\end{bmatrix}$, compare $C_1=\begin{bmatrix}1&0\end{bmatrix}$ with $C_2=\begin{bmatrix}0&1\end{bmatrix}$. Construct each two-sample observability matrix, compute its rank, and state which output can reconstruct both initial state components under the ideal model.

### Exercise 3

A service's aggregate success rate and average latency are green, but users with one feature generation in one region report missing results. Design a bounded investigation. Name the identities, black-box and white-box evidence, completeness checks, and at least three competing hypotheses.

### Exercise 4

A team wants to put raw account ID, SQL text, URL, region, release, and error message into every metric label. Design a safer representation across metrics, logs, traces, and audit events. State trade-offs and access controls.

### Exercise 5

A fleet monitor reports battery, position, and command success, yet some robots take unsafe routes. Define a system boundary and an observability question, identify indistinguishable hypotheses under current outputs, propose new evidence, and explain what still cannot be inferred causally.

## Answers to the Exercises

### Answer 1

Instrumentation creates or enriches evidence in code or configuration. Telemetry is the emitted machine data. Monitoring continuously evaluates selected observations for known operational decisions. Formal observability is a model-relative property that relevant internal state can be reconstructed or distinguished from outputs over time. Operational observability is a bounded ability to ask useful questions and distinguish important hypotheses using available evidence. A product may implement transport, storage, query, and visualization for any of these activities, but installing it does not establish semantic coverage, correct monitors, or state distinguishability.

### Answer 2

For $C_1$, $C_1A=[1,0]$, so

$$
\mathcal{O}_1=\begin{bmatrix}1&0\\1&0\end{bmatrix}
$$

has rank $1$ and cannot distinguish the second initial component. For $C_2$, $C_2A=[1,1]$, so

$$
\mathcal{O}_2=\begin{bmatrix}0&1\\1&1\end{bmatrix}
$$

has determinant $-1$ and rank $2$. Under the exact linear, noiseless, known-input assumptions, $C_2$ can reconstruct both components from two outputs. The result does not transfer automatically to a nonlinear or incorrectly modeled production service.

### Answer 3

Bind observations to region, feature generation, release digest, configuration, operation, dependency, and time. Use a black-box correctness probe with affected and control feature generations. Query per-cohort success and latency distributions rather than aggregate average; inspect traces for paths and deadlines; inspect structured events for result counts and decision branches; inspect dependency and data-store state. Verify denominators, dropped records, sampling, collector lag, clock bounds, and propagation. Competing hypotheses include a feature-specific application branch, stale regional configuration, missing regional data, dependency response differences, and telemetry classification error. Compare predictions and controls, preserve uncertainty, and contain the affected cohort before claiming root cause.

### Answer 4

Metrics should use bounded dimensions such as normalized operation, region, release, outcome class, and perhaps approved route template—not raw URL, account, SQL, or arbitrary errors. Structured logs or traces may retain normalized query identity, trace identity, controlled error code, and authorized pseudonymous account reference when investigation requires it; redact literals and credentials. Security audit events use a separate durable schema and restricted store. Apply sampling appropriate to signal purpose, encrypt transport and storage, audit access, limit retention, test deletion, and prevent untrusted strings from creating label series. The design sacrifices effortless per-account metric queries to bound cost and privacy risk while preserving controlled drill-down.

### Answer 5

Choose the boundary as robot planner, local sensors and controller, command link, and map/configuration service during one route. Ask why a robot selected a path that violated a geofenced safety constraint. Current outputs cannot distinguish a stale map, wrong geofence generation, planner defect, corrupted localization, delayed command, or obstacle-sensor blind spot when all report command success and final position. Add signed map and policy generation, planned path, localization confidence, sensor-health and freshness, command event/receive times, controller mode, and bounded decision trace. These outputs can eliminate hypotheses, but temporal correlation between a map update and unsafe route does not prove the update caused it; controlled replay, model checking, or a safe intervention may be required. Evidence must also avoid exposing sensitive location beyond authorized retention.
