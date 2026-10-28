---
module_id: SARCH-018
program: Software Engineering: Software Architecture
level: 1
module_number: 18
title: Observability and Operability Tactics
status: complete
last_verified: 2026-09-05
---

# Observability and Operability Tactics

## One-Page Review

### Governing question

How should architecture expose enough trustworthy system state and provide enough bounded control for people and automation to detect, diagnose, mitigate, recover, and learn safely?

### Essential definitions

- **observability** is the ability to infer relevant internal state and behavior from available outputs under a declared model and set of questions.
- **operability** is the degree to which authorized people and automation can understand, control, maintain, restore, and evolve a system safely and effectively.
- **telemetry** is machine-produced evidence about execution, state, and environment, including metrics, events, logs, traces, and profiles.
- A **metric** is a numeric measurement over declared dimensions and time; a **log** is a timestamped event record; a **trace** represents causally related work across boundaries.
- **cardinality** is the number of distinct values or combinations represented by dimensions.
- **correlation** links observations belonging to the same logical operation, change, resource, or causal chain.
- A **health signal** supports a declared decision about service, readiness, dependency, or component state; it is not a universal Boolean truth.
- A **runbook** is a governed operational procedure with preconditions, authority, steps, observations, stop conditions, recovery, and ownership.
- **toil** is repetitive, manual, automatable operational work that scales with service demand and carries little enduring value.

### Central model, mechanism, or theorem

Let system state be $x\in X$, permitted diagnostic experiment $u\in U$, and observation $y=h(x,u)$. States $x_1$ and $x_2$ are indistinguishable for available diagnostics when

$$
x_1\sim_U x_2 \iff \forall u\in U:\ h(x_1,u)=h(x_2,u).
$$

Architecture improves practical observability by designing semantic state, causal identity, trustworthy signals, bounded diagnostic experiments, and retention so states relevant to operational decisions are distinguishable. It improves operability by supplying authorized, reversible, observable controls with safe defaults, capacity, procedures, and learning loops. Telemetry volume alone changes neither property.

### Critical invariants

- begin with operational questions, decisions, failure models, and stakeholder outcomes;
- measure at the boundary that owns the claim and correlate across internal boundaries;
- preserve semantic identity for service, operation, tenant, resource, version, change, and attempt;
- define units, aggregation, time, population, missing data, sampling, and freshness;
- bound label cardinality, telemetry volume, retention, query cost, and failure amplification;
- protect secrets, personal data, customer content, and security-relevant evidence;
- keep telemetry failure from exhausting or blocking the primary service unless policy explicitly requires it;
- make operational controls authenticated, authorized, scoped, auditable, reversible where possible, and safe under concurrency;
- exercise detection, diagnosis, mitigation, recovery, failback, and manual procedures;
- bind conclusions to versions, topology, workload, sampling, retention, and observation limits.

### Common failures

Common failures include collecting every event without operational questions; averages that hide tenants or tails; unbounded user IDs in metric labels; logs without stable operation identity; traces sampled away during rare failures; health checks that cause cascading ejection; dashboards with no decision owner; alerts on resource symptoms without user impact; runbooks that require the failed identity system; debug endpoints with broad production authority; telemetry backpressure that blocks requests; and calling a green dashboard proof of correctness.

### Compact example

A checkout request returns a timeout after payment authorization. A request ID generated independently at every hop cannot connect the user attempt, payment command, callback, order state, and reconciliation. Use one stable logical operation identity plus per-attempt and trace identities. Record semantic transitions and authoritative outcomes, not card data or credentials. Operators can then distinguish “payment rejected,” “payment accepted but response lost,” and “provider unknown,” each of which requires a different action.

### Connections

[SARCH-004](004-quality-attributes-as-architectural-drivers.md) supplies measurable outcomes; [SARCH-011](011-availability-and-recovery-tactics.md) supplies detection and recovery; [SARCH-012](012-performance-and-latency-tactics.md) supplies distributions and correlation; [SARCH-014](014-security-and-privacy-tactics.md) constrains privileged controls and telemetry data; [SARCH-016](016-testability-tactics.md) supplies controlled experiments and evidence; and [SARCH-017](017-interoperability-tactics.md) supplies cross-system semantic identity.

## Governing Question

A system can emit terabytes of logs yet leave operators unable to tell whether users received correct results. It can have polished dashboards but no safe way to stop a retry storm, revoke a bad configuration, or restore authoritative state. What architecture makes important states visible and legitimate action possible?

The governing question is how operational decisions map to signals, diagnostic paths, controls, authority, and evidence across normal behavior, change, overload, partial failure, incident, and recovery. Observability without operability produces knowledge without control; operability without observability produces dangerous action without feedback.

## Why This Matters

Production behavior is an architectural outcome. Dependencies fail partially, workloads shift, clocks disagree, state diverges, versions coexist, and humans act under pressure. If the architecture loses causal identity or hides authoritative transitions, no dashboard configuration can reconstruct them reliably.

Operational mechanisms are also attack and failure surfaces. A powerful console, reset command, trace store, deployment controller, or feature switch can disclose data or change service globally. They need stronger design than informal “admin tools,” not weaker design because few people use them.

Telemetry consumes CPU, memory, network, storage, money, and human attention. High-cardinality dimensions can exhaust collection and query systems precisely during incidents. Sampling and aggregation reduce cost but can erase rare evidence. Architecture must align evidence fidelity with consequence.

## Prerequisites and Retrieval

Retrieve system state, output, metric, log, event, trace, span, profile, correlation, identity, unit, aggregation, distribution, percentile, cardinality, sampling, health, alert, incident, control plane, runbook, rollback, recovery, audit, privacy, and evidence limitation.

From earlier modules, retrieve stakeholder-visible outcomes, quality scenarios, fault models, SLOs, latency distributions, workload dimensions, security boundaries, test oracles, stable operation identity, version coexistence, and residual risk. You should be able to distinguish a symptom from a cause and an observation from proof.

## Learning Objectives

After completing this module, you should be able to:

1. frame observability and operability scenarios around decisions and outcomes;
2. distinguish metrics, logs, traces, events, profiles, audits, and health signals;
3. design semantic identity and causal correlation across boundaries;
4. specify units, dimensions, aggregation, missingness, sampling, and retention;
5. control cardinality, telemetry cost, and failure amplification;
6. design health, alert, and diagnostic signals for explicit actions;
7. build bounded operational controls, runbooks, and recovery paths;
8. protect telemetry and administrative capabilities by security and privacy policy;
9. exercise detection, diagnosis, mitigation, recovery, and learning;
10. state what production evidence does and does not establish.

## Core Exposition

**Begin with questions and decisions.** Ask whether users can complete a capability correctly, which population is affected, when behavior changed, which dependency or version participates, what state is authoritative, and what safe action exists. Each signal should support a named decision, investigation, obligation, or learning need.

Inventory operators: service teams, incident commanders, support, security, privacy, compliance, suppliers, and automated controllers. Give each the least observation and control needed. “Everyone can see everything” is neither operable nor privacy preserving.

**Observe outcomes first.** Measure correct completion, latency, availability, freshness, durability, rejection, and safety at the boundary that owns the stakeholder promise. Internal CPU and queue measurements explain mechanisms but cannot substitute for user outcomes.

Segment by operation, region, tenant class, version, dependency, or other dimensions only when the distinction supports action and is safe to retain. Aggregate views can hide minority or high-consequence failures; unrestricted segmentation can disclose people or explode cardinality.

**Design semantic events.** Record meaningful transitions such as `OrderAccepted`, `PaymentOutcomeUnknown`, or `InventoryReservationExpired`, with stable identity, version, time semantics, actor or authority reference, provenance, and outcome. Avoid reconstructing domain truth from free-form text written for one debugging episode.

Events do not automatically equal authoritative state. Delivery can be delayed, duplicated, reordered, or lost; producers can be compromised. Identify the source of truth and reconciliation path. Preserve schema and semantic version so later analysis interprets old evidence correctly.

**Use metrics for bounded numeric questions.** Define name, unit, population, dimensions, aggregation, window, clock, reset behavior, missingness, and owner. Counters count events; gauges represent sampled state; histograms retain distributions under configured buckets or sketches. An average of averages is generally wrong unless weighted by populations.

Metric labels form a product of distinct values. A label set with 20 services, 50 routes, 10 status classes, and 100 regions permits up to $20\times50\times10\times100=1{,}000{,}000$ series before replicas or tenants. Never place unbounded request, user, email, or object identifiers in metric dimensions.

**Use logs as governed event records.** Structured logs support filtering and machine interpretation when field semantics are stable. Include relevant operation, attempt, component, version, result, and reason. Keep secrets, tokens, credentials, raw personal data, and unnecessary payloads out before emission.

Log levels are policy, not truth. A critical security event can be low volume; repetitive expected errors can overwhelm storage. Define rate limiting and loss indicators so suppression does not pretend nothing occurred.

**Use traces for causal paths.** A trace relates spans representing work across synchronous and asynchronous boundaries. Propagate context while separating logical operation identity from network attempt and trace. Retries, queues, callbacks, and long-running workflows may cross trace lifetimes and need durable causal links.

Tracing systems such as those described by the Dapper paper make distributed latency and dependency paths inspectable, but sampling and instrumentation determine what is visible [1]. A trace is an observation from participating components, not an authoritative proof of every effect.

**Sample deliberately.** Head sampling decides before the outcome is known and can miss rare failures. Tail sampling uses later information but requires buffering and a definition of interesting outcomes. Adaptive sampling can preserve anomalies while complicating statistical interpretation.

Record sampling policy and effective probability. Preserve unsampled aggregate outcome metrics and security or audit evidence required by policy. If each of $n$ independent rare incidents has sampling probability $p$, probability of observing at least one is $1-(1-p)^n$; independence and stable $p$ must not be assumed silently.

**Control telemetry cost and failure.** Estimate bytes, events, series, retention, replication, query load, and egress. At 20,000 events/s and 500 bytes/event, raw volume is $10$ MB/s or 864 GB/day in decimal units before indexes, replication, and compression. Volume is an architecture input.

Buffer within bounded memory or disk, shed low-priority telemetry, aggregate, sample, and expose loss. Decide whether audit or safety evidence must block an operation if it cannot be recorded; ordinary debug export should usually fail independently rather than exhaust the primary path.

**Design health by consumer.** Liveness asks whether restart may help. Readiness asks whether an instance should receive a class of work. Dependency health describes a relationship. Service health describes stakeholder outcomes. One Boolean cannot answer them all.

Use representative checks without making them destructive or expensive. Avoid ejecting every slow instance during overload and causing a cascade. Apply hysteresis, minimum capacity, multiple signals, and clear ownership of automated actions.

**Alert for action.** An alert should identify an urgent condition, affected outcome, evidence, uncertainty, owner, and first safe action. Prefer symptoms tied to user impact or imminent invariant breach over every resource threshold. Resource signals remain useful for diagnosis and forecast.

Define grouping, deduplication, inhibition, escalation, maintenance, and recovery notification. Measure detection delay, acknowledgment, mitigation, restoration, false positives, false negatives, and human load. A silent alert caused by a broken notification path is an observability failure.

**Create diagnostic paths.** Operators need dependency maps, version and change correlation, state and queue inspection, configuration provenance, recent events, and safe comparison across healthy and affected populations. Query interfaces should reveal semantics without requiring shell access to every host.

Bound diagnostic cost and authority. An unrestricted heap dump, database query, packet capture, or customer replay can expose secrets and disrupt service. Require legitimate purpose, scoped access, audit, retention, and safe cancellation.

**Design operational controls.** Provide explicit commands for drain, pause, resume, shed, reroute, revoke, rotate, reconcile, replay, rollback, restore, and failover as the domain requires. Each command needs preconditions, identity, authorization, idempotency, concurrency, scope, expected observations, timeout, stop, rollback or forward repair, and audit.

Prefer declarative desired state where controllers can converge safely. Imperative commands remain appropriate for discrete domain actions. Automation must expose its decision and permit safe intervention; hidden controllers can fight operators or one another.

**Separate control and data planes.** A control plane configures or directs data-plane work. Separation can protect service from management churn, but each plane needs identity, availability, capacity, compatibility, and recovery. Cached last-known configuration may preserve service, yet revocation and unsafe stale policy require explicit bounds.

Recovery must not depend entirely on the failed plane. Maintain tested break-glass access, offline procedures, credentials, and evidence according to consequence. Prevent the recovery path from becoming unmonitored permanent bypass.

**Write executable runbooks.** State trigger, scope, prerequisites, authority, hazards, steps, expected observation after each step, stop conditions, escalation, communication, recovery, cleanup, and evidence. Link commands to stable tooling rather than fragile screenshots.

Exercise runbooks under representative failure, load, unavailable people, and lost dependencies. Update them after system change and incidents. A procedure is not evidence until executed and observed in the relevant environment.

**Reduce toil without hiding judgment.** Automate repetitive, deterministic, well-understood work. Preserve human authority for novel, ambiguous, high-consequence decisions. Automation needs rate bounds, dry-run or preview where meaningful, rollback, observability, and ownership.

Track operational load by source and change the architecture that creates it. Faster manual repetition is not sustainable operability. Remove noisy alerts, fragile dependencies, inconsistent configuration, and recurring reconciliation at their source.

**Protect telemetry and controls.** Classify observations, minimize sensitive fields, control access, encrypt appropriately, retain by purpose, support deletion obligations, and audit use. Multi-tenant telemetry needs tenant isolation. Correlation identifiers should not encode secrets or stable personal data.

Administrative systems need phishing-resistant identity where justified, least privilege, separation of duties, just-in-time access, session recording where lawful, and rapid revocation. Security audit evidence and debugging telemetry may have different access and retention policies.

**Learn from operations.** Correlate incidents and near misses with architecture decisions, assumptions, deployments, configurations, workload, and dependency changes. Update failure models, SLOs, runbooks, tests, capacity, controls, and ADRs. Preserve blameless causal analysis without erasing accountability for systems and decisions.

Production observation shows what occurred for observed populations and conditions. Absence of an alert does not prove absence of failure. Missing telemetry, sampling, broken clocks, compromised producers, and unknown unknowns bound every conclusion.

## Definitions and Notation

Let state $x\in X$, permitted diagnostic experiment $u\in U$, and observation $h(x,u)\in Y$. Define operational indistinguishability

$$
x_1\sim_Ux_2 \iff \forall u\in U:h(x_1,u)=h(x_2,u).
$$

This is relative to modeled states, available experiments, permissions, retention, sampling, and observation fidelity. Practical observability for a decision requires that states demanding different actions not remain in the same relevant equivalence class.

For eligible events $E$ and failures $F\subseteq E$, observed failure ratio is $r=|F|/|E|$ when $|E|>0$. Report no observations rather than zero failure when $E$ is empty. For impact time $t_i$, alert time $t_a$, mitigation $t_m$, and restored outcome $t_r$, define detection delay $t_a-t_i$, mitigation delay $t_m-t_i$, and restoration delay $t_r-t_i$ only when clocks and event definitions are valid.

If independent incidents are each retained with probability $p$, $P(observe\ at\ least\ one)=1-(1-p)^n$. Correlated sampling, head decisions, missing context, and changing policies invalidate naive inference.

## Mechanisms, Invariants, or Proof Structure

Use this observability and operability mechanism.

1. **Name decisions:** identify user outcomes, invariants, threats, operational questions, actors, and safe actions.
2. **Model state:** locate authority, transitions, dependencies, versions, changes, and ambiguity that operations must distinguish.
3. **Design identity:** preserve service, operation, attempt, resource, tenant, version, change, and causal references.
4. **Emit evidence:** choose semantic events, distributions, logs, traces, profiles, health, and audit by claim.
5. **Bound telemetry:** control dimensions, sampling, volume, retention, cost, privacy, integrity, and failure effects.
6. **Detect and diagnose:** connect outcome alerts to component evidence, uncertainty, owner, and first safe action.
7. **Control safely:** expose authenticated, authorized, scoped, idempotent, observable, and recoverable operational actions.
8. **Prepare recovery:** maintain independent control paths, executable runbooks, communications, and practiced authority.
9. **Exercise:** test instrumentation loss, overload, partial failure, bad change, control concurrency, mitigation, and failback.
10. **Learn:** update models, objectives, tests, controls, procedures, and decisions from observed outcomes.

The governing invariants are decision-oriented evidence, semantic identity, outcome-first measurement, explicit aggregation and sampling, bounded telemetry, protected data, independent service failure, authorized control, practiced recovery, and claims limited to observation.

## Alternatives and Trade-Offs

**Metrics or events and traces.** Metrics summarize populations efficiently but lose individual causality. Events and traces retain context but cost more and require sampling, indexing, and privacy control. Use complementary signals by question.

**Head or tail sampling.** Head sampling is cheap and immediate but cannot see final outcome. Tail sampling preserves selected results but buffers data and delays decisions. Keep policy and statistical limits explicit.

**Centralized or federated telemetry.** Centralization supports correlation and shared operation but concentrates cost, data, and failure. Federation preserves ownership and isolation but complicates cross-system queries and semantics.

**Automatic or manual control.** Automation reacts quickly and consistently to modeled states but can amplify a wrong diagnosis. Human action handles novelty but is slower and capacity-limited. Combine bounded automation with visible state, stop conditions, and authority.

**Fail-open or fail-closed evidence paths.** Debug telemetry should normally fail without blocking useful work. Legally required audit or safety evidence may require refusal when recording fails. Decide explicitly per event class.

## Failure Modes and Misconceptions

- **“More logs mean more observability.”** Meaning, identity, questions, and trustworthy retention matter.
- **“A dashboard is operability.”** Safe authority and recovery actions are also required.
- **“Average health is green.”** Minority, tenant, region, and tail failures can disappear in aggregation.
- **“Every identifier should be a metric label.”** Unbounded dimensions exhaust telemetry systems.
- **“A trace proves causality.”** It records participating instrumentation and propagated context.
- **“No alert means no incident.”** Signals, sampling, routing, or thresholds may have failed.
- **“Health checks are harmless.”** Aggressive ejection can cause cascading overload.
- **“Admin tools are internal.”** Network location does not supply identity or authorization.
- **“Automation eliminates operators.”** Novel judgment, authority, and exception handling remain.
- **“Runbooks are executable evidence.”** They require current, observed exercises.
- **“Telemetry may contain everything.”** It is a sensitive, expensive production data system.
- **“Observed success proves reliability.”** It supports only the observed population and conditions.

## Worked Examples

### Example 1

**Question:** How should a timed-out checkout be observable across payment and order systems?

**Reasoning:** Preserve one logical operation identity, separate attempt and trace identities, and record order and payment semantic transitions, provider reference, version, deadline, and authoritative outcome. Correlate callback and reconciliation without logging card data or tokens. Distinguish rejected, accepted-response-lost, and unknown states.

**Conclusion:** Causal semantic identity makes different recovery decisions distinguishable.

### Example 2

**Question:** Labels have 20 services, 50 routes, 10 status classes, and 100 regions. What maximum series combinations result?

**Reasoning:** $20\times50\times10\times100=1{,}000{,}000$ combinations before instances, environments, tenants, or histograms. Remove dimensions that do not support aggregate action and move high-cardinality identity to controlled event or trace stores.

**Conclusion:** Cardinality is a multiplicative architecture constraint.

### Example 3

**Question:** What raw daily volume follows from 20,000 events/s at 500 bytes each?

**Reasoning:** The rate is 10,000,000 bytes/s. Over 86,400 seconds, volume is 864,000,000,000 bytes, or 864 GB/day in decimal units, before indexes, replication, metadata, and compression.

**Conclusion:** Telemetry fidelity, cost, and failure behavior require explicit capacity design.

### Example 4

**Question:** A service has 1,000 eligible events and 25 failures. What is the observed failure ratio?

**Reasoning:** $r=25/1000=0.025$, or 2.5%. The result needs window, population, correctness, sampling, and missing-event definitions. With zero eligible events, report no observations rather than 0% failures.

**Conclusion:** Even simple ratios need a declared observation boundary.

### Example 5

**Question:** Ten independent rare incidents each have 5% probability of trace retention. What is the modeled chance of observing at least one?

**Reasoning:** $1-0.95^{10}\approx0.4013$, or 40.13%. Head sampling may correlate retention with traffic rather than outcome, so the independence model can be wrong. Preserve error metrics and consider tail or rule-based sampling.

**Conclusion:** Low sampling can erase rare evidence, and naive probabilities need explicit assumptions.

### Example 6

**Question:** Should a readiness check call every dependency for every probe?

**Reasoning:** It can amplify load and eject healthy instances when one optional dependency slows. Define which work classes require which dependencies, use bounded representative signals, separate liveness and readiness, add hysteresis and minimum capacity, and observe user outcomes.

**Conclusion:** Health is a consumer-specific decision signal, not a universal dependency conjunction.

### Example 7

**Question:** An alert fires whenever CPU exceeds 80%. Is it actionable?

**Reasoning:** Not yet. Identify affected user outcome, duration, saturation evidence, workload, owner, and safe action. High CPU can be efficient and harmless; a queue or latency objective may fail at lower average CPU. Use resource thresholds for diagnosis or imminent risk with validated relationships.

**Conclusion:** Alerts should connect evidence to consequence and action.

### Example 8

**Question:** What must a production `pause-consumer` control specify?

**Reasoning:** Define identity and authorization, queue and partition scope, concurrent commands, idempotency, accepted in-flight work, lease behavior, expected signal, timeout, backlog risk, restart, audit, and automatic expiry if appropriate. Test control-plane loss and accidental broad scope.

**Conclusion:** Operational commands are real domain capabilities with contracts and hazards.

### Example 9

**Question:** A runbook says “restart until healthy.” Why is it unsafe?

**Reasoning:** It lacks diagnosis, authority, bounds, state effects, maximum attempts, expected observations, stop, escalation, and recovery. Restart may destroy evidence, repeat corruption, or overload survivors. Replace it with fault-specific preconditions, one bounded action, outcome checks, and escalation.

**Conclusion:** A runbook must govern decisions and evidence, not encode ritual.

### Example 10

**Question:** How should observability and operability be designed for a municipal water-treatment controller?

**Reasoning:** Expose physical state, sensor quality, commands, authority, timing, alarms, control mode, software and configuration version, communication, and safe-state transitions. Separate operational, safety, security, and privacy evidence; provide authenticated local and recovery control; exercise loss, false sensor, bad change, failover, and manual operation. No external water-treatment, chemical, safety, environmental, regulatory, cybersecurity, hardware, human-factors, or practitioner review is claimed; named qualified authorities must validate signals, controls, exercises, release, and residual risk.

**Conclusion:** High-consequence operations require trustworthy physical outcomes and bounded authority, not just software dashboards.

## Cross-Program Connections

- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns oracle design, instrumentation tests, fault injection, and evidence quality.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns SLO operation, telemetry pipelines, alerting, incidents, runbooks, and toil reduction.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns security monitoring, audit, privileged access, detection, and response mechanisms.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects observations and controls to physical state, hazards, operators, and lifecycle assurance.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns causal ordering, partial failure, distributed tracing limits, and control convergence.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns shared telemetry, operational interfaces, control planes, and developer-facing diagnostics.

## References

1. Benjamin H. Sigelman et al. [“Dapper, a Large-Scale Distributed Systems Tracing Infrastructure.”](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/) Google Research, 2010. Distributed trace context, sampling, collection, and production use; consulted 2026-09-05.
2. Betsy Beyer et al., editors. [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/), O'Reilly, 2016. Monitoring, distributed systems, alerting, automation, incident response, and operational practice; consulted 2026-09-05.
3. Betsy Beyer et al., editors. [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/), O'Reilly, 2018. Implementing SLOs, monitoring, alerting, incident response, and operational controls; consulted 2026-09-05.
4. Charity Majors, Liz Fong-Jones, and George Miranda. *Observability Engineering*. O'Reilly, 2022. High-cardinality events, distributed systems, debugging, sampling, and organizational practice.
5. Cindy Sridharan. *Distributed Systems Observability*. O'Reilly, 2018. Metrics, logs, traces, monitoring, and distributed-system diagnosis.
6. OpenTelemetry Authors. [OpenTelemetry Specification](https://opentelemetry.io/docs/specs/), current specification index. Telemetry data, context, resources, traces, metrics, logs, and profiles; consulted 2026-09-05.
7. Michael Nygard. *Release It! Design and Deploy Production-Ready Software*, second edition, Pragmatic Bookshelf, 2018. Stability, control, production diagnostics, failure, and recovery.
8. NIST. [SP 800-61 Rev. 3, Incident Response Recommendations and Considerations for Cybersecurity Risk Management](https://csrc.nist.gov/pubs/sp/800/61/r3/final), April 2025. Incident preparation, detection, response, recovery, and improvement; consulted 2026-09-05.

## Exercises

### Exercise 1

Define an observability and operability scenario for diagnosing delayed order fulfillment without assuming that logs alone suffice.

### Exercise 2

A metric has 12 services, 40 routes, 8 result classes, 6 regions, and 3 environments. Compute maximum label combinations and explain two controls.

### Exercise 3

Diagnose a system with request IDs regenerated at every hop, customer IDs in metric labels, full payload logs, 1% head sampling, dependency-conjunctive health, CPU-only alerts, unaudited admin scripts, and a runbook stored behind failed identity.

### Exercise 4

Compare metrics, structured events, traces, and audits for investigating authorization failures. Address semantics, causality, aggregation, cost, privacy, integrity, and retention.

### Exercise 5

Design observability and operability assurance for an unfamiliar regional avalanche-warning network. Separate automated checks, operational exercises, qualified authority, and blockers.

## Answers to the Exercises

### Answer 1

For a correctly accepted order not fulfilled within its declared window, an operator must identify the affected customer-safe order reference, current authoritative state, last valid transition, inventory, payment, warehouse, carrier, retry, queue, version, configuration, and dependency evidence within a measured diagnosis time. Preserve one logical operation identity with attempt, message, shipment, and trace references. Observe correct terminal outcomes and pending age at the order boundary, then correlate component queues, errors, and changes.

Provide scoped controls to pause unsafe retry, reconcile one order, reroute eligible work, or escalate supplier action, each with authorization, idempotency, expected observations, stop, and audit. Protect customer and payment data. Test delayed, duplicate, missing, reordered, supplier-outage, and reconciliation paths. Logs assist diagnosis but do not replace authoritative state, user outcome metrics, traces, or operational control.

### Answer 2

Maximum combinations are

$$
12\times40\times8\times6\times3=69{,}120.
$$

This excludes instances and histogram buckets. First, retain only dimensions tied to aggregate action: combine or remove route and result categories whose distinction has no operational decision. Second, move high-cardinality request, tenant, or object identity to access-controlled structured events or traces and use bounded exemplars if supported. Also budget series, enforce schema, observe dropped series, and set retention by purpose.

### Answer 3

Regenerated IDs break causality. Customer labels expose data and create unbounded cardinality. Payload logs create a sensitive store. One-percent head sampling can miss rare failures. Conjunctive dependency health can eject every instance during optional dependency failure. CPU-only alerts lack user outcome and action. Scripts have unbounded authority and weak evidence. The unavailable identity path makes the runbook inaccessible during the event it addresses.

Preserve logical and causal identity across boundaries; minimize and protect semantic events; bound metric dimensions; retain aggregate outcomes and adopt consequence-aware sampling; separate liveness, readiness, dependency, and service health; alert on outcome or imminent invariant breach; replace scripts with scoped, authorized, idempotent, audited controls; and maintain exercised independent recovery access and procedures. Verify telemetry loss, overload, partial dependencies, bad changes, response, restoration, and failback.

### Answer 4

Metrics efficiently show rates and distributions by bounded service, decision, reason class, version, and region, but not individual causality. Structured events capture subject reference, action, object class, policy version, decision, and reason under privacy constraints. Traces connect authorization calls to request paths and dependencies but depend on propagation and sampling. Audits preserve higher-integrity evidence for governed attribution and investigation, with stricter access and retention.

Use all by purpose: outcome metrics for detection, events and traces for diagnosis, and protected audits for accountability. Keep credentials, raw personal content, and sensitive policy detail out unless specifically authorized. Define clocks, correlation, missing data, sampling, producer trust, tamper resistance, query access, retention, and deletion. No signal alone proves whether the policy itself is legitimate or complete.

### Answer 5

Define snowpack and weather observations, sensor quality, geographic model, forecast version, hazard level, issue and expiry times, alert authority, communication channels, acknowledgment, public accessibility, field teams, power, network, and manual operation. Preserve provenance, units, clock semantics, versions, uncertainty, changes, and authoritative transitions. Expose user-visible delivery outcomes plus sensor, model, queue, dependency, and control evidence.

Automation can verify schemas, units, sensor freshness, model and configuration provenance, identity, authorization, alert transitions, timing, cardinality budgets, telemetry loss, communication outcomes, and evidence freshness. Exercises can test sensor fault, regional network loss, surge, conflicting data, false positive, missed alert, bad configuration, manual issuance, revocation, recovery, and public correction. Controls require narrow geographic scope, concurrency rules, expected observations, stop, rollback or correction, and audit.

No external avalanche, meteorological, geospatial, emergency-management, safety, accessibility, telecommunications, regulatory, cybersecurity, human-factors, statistical, or practitioner review is claimed. Named qualified authorities must own hazard models, alert thresholds, public policy, exercises, validation, release, and residual risk. Unknown sensor provenance, ambiguous alert authority, inaccessible warning, unaudited broad control, failed offline operation, missing delivery evidence, or unresolved high-severity hazard blocks readiness.
