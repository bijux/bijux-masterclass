---
module_id: SARCH-028
program: Software Engineering: Software Architecture
level: 1
module_number: 28
title: Operational Views
status: complete
last_verified: 2026-09-06
---

# Operational Views

## One-Page Review

### Governing question

How can an architecture description expose the states, signals, authorities, procedures, controls, dependencies, and evidence by which a system is operated safely through normal service, maintenance, degradation, incident, recovery, and retirement?

### Essential definitions

- An **operational state** is a declared mode with permitted capabilities, constraints, risks, entry conditions, and exit conditions.
- A **control action** intentionally changes system or operational state, such as deploy, drain, fail over, rotate, isolate, restore, or revoke.
- **telemetry** is emitted evidence about behavior, including metrics, logs, traces, events, profiles, and health observations.
- A **service-level indicator (SLI)** is a defined measurement of behavior for a population and window; a **service-level objective (SLO)** is a target for that indicator.
- An **alert** is a routed notification that evidence meets a declared condition requiring attention.
- A **runbook** is a versioned, executable or human procedure with prerequisites, authority, steps, checks, stop conditions, rollback, and escalation.
- An **incident** is an event or condition requiring coordinated response to limit harm and restore acceptable operation.
- A **recovery point** bounds acceptable state loss; a **recovery time** bounds the targeted interval to restore a declared capability.
- **toil** is recurring operational work that is manual, repetitive, automatable, tactical, and of limited enduring value.
- **operational conformance** is evidence that observed state and practice satisfy declared constraints at a recorded time and scope.

### Central model, mechanism, or theorem

Represent operations as

$$
O=(S,E,T,R,A,C,V),
$$

where $S$ is operational states, $E$ observed or commanded events, $T\subseteq S\times E\times S$ transitions, $R$ roles, $A$ authority assignments, $C$ constraints and controls, and $V$ evidence.

A permitted transition $(s,e,s')$ requires authorized actor, satisfied preconditions, protected execution, observable progress, verified postconditions, and a defined failure path. A successful command exit status is not itself proof that the operational objective holds.

### Critical invariants

- define service, users, capabilities, environments, states, and operating assumptions;
- distinguish desired state, observed state, health, readiness, serving, and user outcome;
- assign decision, execution, approval, communication, security, data, and recovery authority;
- connect SLIs and alerts to user or system consequences with explicit populations and windows;
- preserve telemetry identity, time, integrity, retention, privacy, and failure visibility;
- make control-plane and observability dependencies visible;
- give runbooks prerequisites, bounded actions, verification, rollback, stop, and escalation;
- model maintenance, overload, dependency loss, security containment, recovery, and retirement;
- protect administrative access, secrets, break-glass paths, and automation against misuse;
- exercise backups, failover, restoration, and incident coordination in recorded environments;
- reconcile operations with runtime, deployment, data, security, delivery, and support views;
- bound every operational claim to evidence, environment, time, and exclusions.

### Common failures

Common failures include equating a running process with a healthy service; monitoring only internal resource use; alerting on every anomaly; paging without an actionable owner; using averages that hide harmful tails; treating missing telemetry as healthy; granting runbooks unbounded privilege; automating destructive action without preconditions or stop rules; declaring recovery from backup existence rather than restore evidence; rotating credentials without consumers; hiding control-plane dependencies; merging incident command with every technical task; and claiming one drill proves readiness for every failure.

### Compact example

An API process is running and its local health endpoint returns 200, but all requests fail authorization because the identity provider is unavailable. The operational view distinguishes process-liveness, dependency-readiness, serving state, and user-success SLI. It defines degraded behavior, alert ownership, dependency evidence, and recovery rather than reporting “up.”

### Connections

[SARCH-018](018-observability-and-operability-tactics.md) supplies tactics; [SARCH-024](024-runtime-interaction-views.md) supplies failure sequences; [SARCH-025](025-deployment-views.md) supplies deployed resources; [SARCH-027](027-development-and-build-views.md) supplies change and artifact evidence. [SARCH-029](../ROADMAP.md) next develops security views. Reliability, Platform, Cloud, Security, Systems, and Testing programs deepen operational mechanisms.

## Governing Question

Architecture that explains only construction is incomplete. Systems spend most of their life being observed, changed, repaired, secured, scaled, backed up, restored, and eventually retired. These activities use powerful control paths and occur precisely when information is uncertain and risk is high.

The governing problem is to show how operators and automation recognize state, decide, act, verify, communicate, recover, and learn. The view must include both normal and exceptional operation without turning into a product-specific dashboard inventory or an unbounded collection of procedures.

## Why This Matters

Operational qualities emerge from socio-technical interaction. Detection depends on telemetry and user reports. Diagnosis depends on context and preserved evidence. Recovery depends on artifacts, state, capacity, credentials, procedures, and authority. Poor coordination can make a correct technical action harmful; excessive privileges can turn convenience automation into a large failure domain.

Maintenance and change are normal sources of risk. Draining traffic, migrating data, rotating keys, scaling capacity, failing over, and retiring systems temporarily alter assumptions. If these states are absent from architecture, runbooks improvise them under pressure.

An operational view makes control and evidence first-class. It enables readiness reviews, incident exercises, support handoffs, access review, recovery planning, capacity decisions, and post-incident learning while preserving the limits of measured evidence.

## Prerequisites and Retrieval

Retrieve service, capability, state, transition, desired state, observed state, health, liveness, readiness, telemetry, metric, log, trace, event, SLI, SLO, error budget, alert, page, dashboard, runbook, playbook, on-call, incident, severity, command, containment, mitigation, recovery, backup, restore, failover, recovery point, recovery time, maintenance, toil, break-glass, audit, and conformance.

From prior modules, retrieve quality scenarios, availability, performance, security, testability, observability, context, runtime interaction, deployment, data, and build views. Distinguish data-plane behavior, control-plane action, management access, evidence collection, and human authority.

## Learning Objectives

After completing this module, you should be able to:

1. define operational states, events, transitions, roles, authorities, controls, and evidence;
2. distinguish liveness, readiness, serving, health, and user-visible outcome;
3. define SLIs, SLOs, alerts, and error budgets with populations and windows;
4. design telemetry and expose failure of the observability path itself;
5. write reviewable runbook contracts with safe automation boundaries;
6. model maintenance, degradation, overload, security containment, recovery, and retirement;
7. assign incident command, technical, communication, and business decision authority;
8. evaluate backup, restoration, failover, credential, and control-plane dependencies;
9. distinguish desired configuration from observed operational conformance;
10. connect operational evidence and learning back to architecture decisions.

## Core Exposition

**Frame the service and operating context.** Name users, critical capabilities, environments, dependencies, hours, support boundaries, regulatory or safety conditions, and the decision the view supports. Define whether it describes production, disaster recovery, factory devices, developer infrastructure, or another environment. State lifecycle version and evidence date.

ISO/IEC/IEEE 42010:2022 remains the current published architecture-description edition as checked on 2026-09-06 [1]. Concern-governed operational projections may include state models, responsibility maps, signal flows, control paths, runbook inventories, recovery paths, and incident structures. Correspondences keep them coherent.

**Define operational states.** Avoid one binary `up/down` flag. Useful states may include provisioning, starting, warming, ready, serving, degraded, overloaded, draining, maintenance, isolated, recovering, failed-safe, and retired. Define capabilities, allowed actions, data risk, security posture, entry evidence, and exit evidence for each.

State is concern-relative. A database can be process-live but not accepting writes; a replica can be serving stale reads but not in quorum; an edge device can be locally autonomous but disconnected from central management. Publish state at the resolution users and responders need.

**Model transitions as controlled actions.** For deploy, drain, failover, restore, rotate, isolate, or retire, record initiating event, authorized actor, prerequisites, change identity, target scope, concurrency, timeout, progress, postconditions, failure state, rollback or forward recovery, and escalation.

Control action success is not business success. A failover command can return zero while routing still points to the old site. A restore can complete while the database is inconsistent with external effects. Verify the declared objective through independent and user-relevant evidence.

**Assign operational authority.** Distinguish incident command, technical execution, security containment, data correction, business degradation, safety shutdown, communication, and external notification. One person may hold several roles in a small system, but the decisions remain distinct.

Define authentication, authorization, separation of duties, delegation, expiry, revocation, and audit. Break-glass access needs a narrow trigger, strong identity, time bound, recording, review, and recovery. It is not a permanent bypass with an alarming name.

**Measure user-relevant behavior.** An SLI needs event definition, eligible population, success predicate, observation point, window, aggregation, missing-data policy, and quality. Examples include successful checkout fraction, latency below a threshold, freshness of published data, or valid control actions completed before a deadline.

An SLO sets a target for the defined SLI. For target $p$ over window with $N$ eligible events, a simple allowed-failure count is $(1-p)N$, subject to rounding and policy. For a continuously measured 30-day window, 99.9% nominal availability allows $0.001\times30\times24\times60=43.2$ minutes outside the objective. This arithmetic does not define which events count or excuse harmful concentration.

Error budgets support risk decisions only when indicator and objective represent user value. A monthly budget exhausted in one critical hour can cause unacceptable harm. Segment by capability, user, region, or risk when aggregation hides consequences.

**Design alerts for action.** Alerts should identify a consequential condition, responsible role, urgency, evidence, and initial action. Page when timely human intervention is needed. Use lower-urgency routes for conditions that can wait. Deduplicate correlated symptoms without hiding distinct failures.

Symptom-based alerts often align better with user harm; cause-based signals aid diagnosis and early prevention. Use both where justified. Static thresholds, rates, burn rates, change points, and composite conditions have different sensitivity. Validate against historical events and induced failures without assuming the past covers new modes.

**Treat telemetry as a production subsystem.** Define sources, instrumentation, identities, clocks, collection, buffering, sampling, aggregation, storage, retention, access, cost, and failure. Separate application behavior from telemetry pipeline behavior. Missing data must yield `unknown` or an explicit inference, not silently healthy.

OpenTelemetry documentation retrieved 2026-09-06 describes telemetry signals including traces, metrics, and logs and explains observability as using emitted signals to understand system behavior [3]. This supplies interoperable mechanisms, but instrumentation completeness, semantic correctness, sampling, cardinality, clock error, and export reliability remain architecture concerns.

Protect telemetry: it can contain credentials, identifiers, payloads, topology, and security events. Apply minimization, redaction, access, integrity, retention, and incident preservation. Attackers may disable or flood it. Keep critical audit evidence under an authority not fully controlled by the observed workload.

**Design dashboards for decisions.** A dashboard should answer a question: Are users succeeding? Is harm growing? Which scope is affected? What changed? Is mitigation working? Combine user outcomes, traffic, errors, latency distributions, saturation, dependency health, change markers, and data freshness as relevant.

Averages can hide tails and subgroups. Percentiles require populations and windows. High-cardinality labels can overload monitoring or expose sensitive values. Every panel needs unit, source, aggregation, missing-data behavior, and ownership. A dashboard without an associated decision can become decorative inventory.

**Make runbooks bounded and verifiable.** A runbook names purpose, symptoms, prerequisites, required role, risk, inputs, commands or actions, expected observations, branching conditions, timeouts, stop conditions, rollback or recovery, escalation, communication, and evidence capture. Version it with the architecture and test applicable steps.

Automation should be idempotent or explicitly protect non-repeatable effects. Use dry-run or preview where it represents reality, narrow scope, confirmation for high-impact actions, rate limits, locks, and independent postcondition checks. Do not automate uncertainty into faster damage.

**Plan overload and dependency loss.** Define admission, queue bounds, load shedding, prioritization, backpressure, retry budgets, degraded responses, and recovery. Identify which users or work may be delayed or rejected. Preserve fairness, safety, and business authority rather than letting resource exhaustion decide policy accidentally.

Dependencies include identity, DNS, certificates, time, configuration, storage, telemetry, control planes, people, vendors, and facilities. Model which capabilities continue during loss and for how long. A service that serves cached reads while authorization data is stale may be technically available but unsafe.

**Operate maintenance and change states.** Draining stops new work while completing, transferring, or safely abandoning existing work. Maintenance may reduce redundancy. Key rotation creates overlapping trust. Schema migration creates mixed readers and writers. Capacity changes can redistribute load and expose cold paths.

State the safe order, compatibility interval, monitoring, abort thresholds, and rollback limits. Suppressing alerts during maintenance must be scoped and expiring; otherwise real harm disappears. Announce user impact and maintain an authoritative change record.

**Prepare incident response.** Define intake, triage, severity, command, investigation, containment, mitigation, recovery, communication, evidence preservation, and learning. NIST SP 800-61 Revision 3, published April 2025 and checked on 2026-09-06, integrates incident response across cybersecurity risk management and emphasizes preparation, detection, response, recovery, and improvement [2].

Incident command maintains objectives, roles, decisions, and shared state; it need not be the deepest technical expert. Preserve a timestamped decision and action log. Separate hypotheses from observations. Stabilize harm before optimizing diagnosis when policy permits. Security evidence and safety events may require specialized custody and notification.

**Design recovery from outcomes backward.** Define restored capability, acceptable data point, dependencies, environment, authority, and evidence. Backup is a potential input to recovery, not proof. Restoration includes locating artifacts and keys, provisioning, validating integrity, replaying changes, reconciling external effects, warming, shifting traffic, and monitoring.

Recovery time objective and recovery point objective are targets under stated scenarios, not guarantees. Test restoration at realistic scale and isolation. Record achieved times, data loss, manual steps, excluded dependencies, and defects. A successful tabletop tests coordination; it does not prove storage restoration.

**Control toil and learning.** Track recurring manual work by frequency, time, risk, cognitive load, and automation potential. Remove root causes, improve interfaces, automate bounded actions, and retain human judgment for policy and novel failure. Automation maintenance itself is operational work.

After incidents and drills, identify contributing conditions across design, code, deployment, operations, organization, and incentives. Actions should have owner, rationale, expected risk reduction, evidence, and completion criteria. Avoid attributing complex failure to one operator action while ignoring the system that made it hazardous.

**Retire safely.** Retirement removes traffic, dependencies, data, identities, secrets, certificates, backups, alerts, dashboards, DNS, contracts, and support obligations according to policy. Preserve required records and prove consumers migrated. A silent service with live credentials and sensitive data remains an attack and cost surface.

**Gather bounded conformance evidence.** Desired configuration and runbooks express intent. Runtime APIs, black-box probes, telemetry, audit logs, inventories, exercises, restore results, and user reports provide observations. Each can be stale, incomplete, or compromised. Compare explicit constraints at a recorded time and retain uncertainty.

Google's SRE monitoring chapter distinguishes black-box and white-box monitoring and emphasizes signals useful for paging and diagnosis [4]. Use this as practice calibration, not universal policy. The architecture must derive indicators, urgency, and ownership from its users and risks.

## Definitions and Notation

Define an operational model

$$
O=(S,E,T,R,A,C,V),
$$

where $S$ is operational states; $E$ observed and commanded events; $T\subseteq S\times E\times S$ transitions; $R$ roles; $A\subseteq R\times T$ authority; $C$ constraints and controls; and $V$ versioned evidence.

Let an SLI over eligible population $U_W$ in window $W$ be

$$
SLI(W)=\frac{|\{x\in U_W:good(x)\}|}{|U_W|},
$$

when $|U_W|>0$. Report unknown or missing classifications separately. For target $p$, the simple event error budget is $(1-p)|U_W|$; consumption patterns and consequence still matter.

For transition $\tau=(s,e,s')$, define $Permitted(\tau,r,c)$ to require $(r,\tau)\in A$, satisfied preconditions in context $c$, protected execution, and declared postcondition evidence. Permission does not imply success. Evidence after execution determines whether $s'$ was reached or an intermediate/failure state applies.

## Mechanisms, Invariants, or Proof Structure

Use this operational-view mechanism.

1. **Frame:** name service, users, capabilities, environment, time, dependencies, support, and risk.
2. **Define states:** specify permitted capabilities, constraints, entry, exit, health, and evidence.
3. **Map transitions:** record triggers, preconditions, authority, actions, timeouts, postconditions, rollback, and failure states.
4. **Assign roles:** distinguish command, execution, security, data, business, safety, communication, and escalation.
5. **Instrument:** define user-relevant signals, telemetry paths, clocks, identity, privacy, integrity, and missing-data behavior.
6. **Set objectives and alerts:** define populations, windows, thresholds, consequences, owners, urgency, and first actions.
7. **Operationalize:** govern runbooks, automation, access, changes, maintenance, overload, and dependency loss.
8. **Prepare and recover:** exercise incidents, containment, backups, restoration, failover, reconciliation, and communication.
9. **Learn and retire:** reduce toil, govern corrective actions, remove obsolete assets and authority, and retain required evidence.
10. **Reconcile and verify:** map runtime, deployment, data, security, delivery, support, and observed conformance.

The governing invariants are explicit operational state, user-relevant evidence, bounded control authority, safe and verified transitions, actionable alerts, observable telemetry failure, tested recovery, protected incident evidence, governed learning, complete retirement, cross-view correspondence, and bounded claims.

If an event population is partitioned into good, bad, and unknown sets, then $|U|=|G|+|B|+|X|$. Reporting only $|G|/(|G|+|B|)$ omits unknowns and can overstate observed success. This counting result does not determine how unknowns should affect policy; that is a declared risk decision.

## Alternatives and Trade-Offs

**Black-box versus white-box observation.** Black-box probes approximate user outcomes and catch unknown internal causes. White-box telemetry supports diagnosis and prediction but can report healthy internals while users fail. Use complementary observations and expose their shared dependencies.

**Manual versus automated control.** Humans handle novel judgment and policy but are slower and error-prone under pressure. Automation is fast and consistent but can amplify flawed assumptions. Automate bounded, observable actions and retain explicit authority for consequential decisions.

**Centralized versus federated operations.** Centralization standardizes response and tooling but can distance responders from domain context and create common control failure. Federation preserves ownership but needs interoperable severity, escalation, evidence, and communication.

**Fail-open versus fail-closed.** Failing closed protects some security or safety invariants but can deny critical service. Failing open preserves access but may authorize harmful action. Decide per capability, threat, duration, user, and compensating control.

**Immediate rollback versus forward recovery.** Rollback can restore known code quickly when data and dependencies remain compatible. Forward recovery may be necessary after irreversible schema, external, or physical effects. Model both boundaries before change.

**Detailed telemetry versus cost and exposure.** More telemetry aids diagnosis but consumes resources and may leak sensitive data. Select signals by operational questions, sample consciously, protect access, and retain critical evidence.

**High availability versus operational simplicity.** Redundancy and automated failover can reduce some outages but add modes, dependencies, and testing burden. A simpler degraded service may be safer than complex unverified failover.

## Failure Modes and Misconceptions

- **Process live means service healthy.** Dependencies, routing, data, and user outcomes may fail.
- **No alert means no incident.** Telemetry or alert routing may be broken.
- **Every anomaly should page.** Pages require timely, actionable human response.
- **Average latency represents users.** Tails and subgroups can contain concentrated harm.
- **A dashboard is an operational view.** Panels need decisions, semantics, ownership, and action.
- **A runbook command succeeding proves recovery.** Verify independent postconditions and user capability.
- **Automation removes risk.** It changes speed, scale, authority, and failure modes.
- **Backup means recoverable.** Restore, compatibility, keys, dependencies, and reconciliation need evidence.
- **Failover is one action.** Detection, data, routing, capacity, identity, validation, and failback interact.
- **Break-glass access may stay broad.** Emergency authority needs narrow scope, expiry, audit, and review.
- **Incident command should do all technical work.** Coordination and technical execution are distinct roles.
- **One drill proves readiness.** Evidence is scenario-, environment-, scale-, and time-bounded.
- **Retired means no traffic.** Data, credentials, dependencies, contracts, and costs may remain.

## Worked Examples

### Example 1

**Situation.** An API process is live, but its identity provider is unreachable and users receive 401 responses.

**Reasoning.** Process-liveness passes; dependency-readiness and user-success fail. Model `serving-degraded` or `unavailable-for-authenticated-use`, alert on user failures, and define whether any bounded cached authorization is safe. Recovery verifies authenticated user journeys, not just process status.

**Conclusion.** Operational health is capability- and observer-specific.

### Example 2

**Situation.** CPU reaches 95% but requests meet their SLO; later request errors spike while CPU is 30%.

**Reasoning.** CPU is a cause or saturation signal, not direct user harm. Page on sustained user-impact burn or an imminent capacity condition with action. Retain CPU for diagnosis. The low-CPU error spike may come from dependency rejection and deserves symptom-based alerting.

**Conclusion.** Combine user symptoms with causal signals instead of treating resource thresholds as service truth.

### Example 3

**Situation.** A continuously assessed service has a 99.9% objective over 30 days.

**Reasoning.** Thirty days contain $30\times24\times60=43{,}200$ minutes. The nominal outside-objective allowance is $0.001\times43{,}200=43.2$ minutes. An outage affecting only critical transactions may violate policy before this aggregate budget is exhausted.

**Conclusion.** Error-budget arithmetic is useful only with a valid indicator and consequence model.

### Example 4

**Situation.** A runbook says “restart all workers if queues stall.”

**Reasoning.** Add queue identity, stall definition, consumer ownership, in-flight semantics, prerequisite evidence, one-worker canary, concurrency limit, timeout, backlog and error observations, stop threshold, rollback or escalation, and incident log. Restarting all workers could duplicate effects or remove diagnostic evidence.

**Conclusion.** Safe runbooks bound authority and verify outcomes instead of listing commands alone.

### Example 5

**Situation.** A stateful node needs maintenance while two replicas remain.

**Reasoning.** Check quorum, replica freshness, failover capacity, backup status, active change, and zone risk. Drain clients, transfer leadership, verify remaining service, perform maintenance, rejoin, resynchronize, and verify before restoring redundancy. Abort if lag or error thresholds cross bounds.

**Conclusion.** Maintenance is an operational state transition with temporarily altered risk.

### Example 6

**Situation.** Nightly backups report success, but a quarterly restore cannot decrypt them.

**Reasoning.** The backup job proved bytes were written, not recoverability. Restore testing needs retained and accessible keys, artifact and schema compatibility, sufficient capacity, integrity checks, replay, and user-level validation. Record the failed dependency and update recovery evidence.

**Conclusion.** Recovery is demonstrated by bounded restoration outcomes, not backup existence.

### Example 7

**Situation.** A database password rotates, but one batch worker runs monthly and still holds the old credential.

**Reasoning.** Inventory consumers, introduce overlapping validity if risk allows, distribute the new secret, verify active and dormant paths, observe old use, then revoke. The monthly path needs simulation or explicit activation before overlap expires. Logs and caches must not expose either secret.

**Conclusion.** Credential rotation is a multi-consumer transition, not one value replacement.

### Example 8

**Situation.** During a regional incident, three teams independently change routing.

**Reasoning.** Conflicting mitigations obscure causality and may oscillate traffic. Incident command declares objective, assigns routing owner, freezes unrelated change, records hypotheses and actions, schedules updates, and delegates investigation. Technical owners still decide within their domains under the shared plan.

**Conclusion.** Incident command coordinates authority and information rather than replacing expertise.

### Example 9

**Situation.** Metrics disappear from half the fleet while user probes still pass.

**Reasoning.** Treat telemetry state as unknown, alert its owner at appropriate urgency, compare collector, network, quota, and agent evidence, and avoid interpreting absent error series as zero. Preserve black-box probes while repairing the signal path. If audit evidence is affected, apply stronger containment.

**Conclusion.** Observability failure is an operational condition with its own response.

### Example 10

**Situation.** A chemical plant control service loses central connectivity during a process excursion.

**Reasoning.** Local controllers retain bounded safety authority, validated setpoints, independent sensors, alarms, and fail-safe transitions. Central commands carry identity and validity and cannot override expired local limits. Operators have physical shutdown, communication, and incident roles. Logs preserve local time uncertainty and reconcile later. Formal hazard analysis and regulatory assurance remain separate requirements.

**Conclusion.** High-consequence operations require local authority, independent evidence, safe states, and human coordination.

## Cross-Program Connections

- **Software Delivery and Reliability Engineering:** SLOs, alerts, on-call, change, incidents, recovery, and learning deepen operations.
- **Platform Engineering:** control planes, automation, policy, telemetry, self-service, and fleet management implement operational controls.
- **Cloud Engineering:** managed services, regional failures, elasticity, quotas, and shared responsibility specialize operation.
- **Security:** detection, containment, identity, break-glass access, audit, evidence, and notification govern cyber incidents.
- **Systems Engineering:** hazards, physical controls, operators, facilities, maintenance, and assurance connect software to the whole system.
- **Operating Systems and Networks:** resource saturation, process state, clocks, routing, loss, and control paths explain symptoms.
- **Database and Data Engineering:** backup, restore, replay, reconciliation, migrations, freshness, and data quality govern state recovery.
- **Software Testing and Quality Engineering:** fault injection, drills, restore tests, canaries, and oracles produce bounded readiness evidence.

## References

1. ISO/IEC/IEEE, *ISO/IEC/IEEE 42010:2022 Software, systems and enterprise — Architecture description*, 2nd ed., November 2022. Official catalogue; current edition checked 2026-09-06. https://www.iso.org/standard/74393.html
2. Alexander Nelson, Sanjay Rekhi, Karen Scarfone, and Murugiah Souppaya, *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile*, NIST SP 800-61 Rev. 3, April 2025. Current revision checked 2026-09-06. https://doi.org/10.6028/NIST.SP.800-61r3
3. OpenTelemetry Authors, “Observability Primer,” current official documentation. Retrieved 2026-09-06. https://opentelemetry.io/docs/concepts/observability-primer/
4. Rob Ewaschuk, “Monitoring Distributed Systems,” in Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds., *Site Reliability Engineering*, O’Reilly Media, 2016. https://sre.google/sre-book/monitoring-distributed-systems/
5. Betsy Beyer, Niall Richard Murphy, David K. Rensin, Kent Kawahara, and Stephen Thorne, eds., *The Site Reliability Workbook*, O’Reilly Media, 2018.
6. Paul Clements et al., *Documenting Software Architectures: Views and Beyond*, 2nd ed., Addison-Wesley, 2010.
7. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.

## Exercises

### Exercise 1

Precisely distinguish desired state, observed state, liveness, readiness, serving state, health, SLI, SLO, alert, incident, mitigation, and recovery.

### Exercise 2

In a window of 2,000,000 eligible requests, 1,996,800 are good, 2,200 are bad, and 1,000 have unknown outcome because telemetry was lost. Compute success (a) over all eligible requests with unknowns not good and (b) among classified requests. Compare with a 99.9% target.

### Exercise 3

Redesign a runbook that says “on high latency, fail over immediately.” Include evidence, authority, state, data, capacity, security, execution, postconditions, stop, rollback or forward recovery, and communication.

### Exercise 4

Compare centralized and federated operations for a platform serving twenty product teams. Address service ownership, incident command, access, common tooling, telemetry, escalation, change, learning, and common failure.

### Exercise 5

Transfer the method to a metropolitan rail-signaling system. Design operational views for normal service, degraded sensors, maintenance possession, communication loss, safety stop, software update, incident command, passenger communication, evidence, recovery, and return to service.

## Answers to the Exercises

### Answer 1

**Desired state** is authorized intent; **observed state** is time-bounded evidence. **Liveness** says a process or mechanism progresses or responds. **Readiness** says it can accept selected work. **Serving state** says routing and admission expose it to users. **Health** is a concern-specific judgment about capability and risk. An **SLI** measures defined behavior; an **SLO** sets its target. An **alert** routes a condition for action. An **incident** requires coordinated response. A **mitigation** limits current harm; **recovery** restores a declared acceptable capability and state.

These can disagree. A live process can be unready; a ready instance can receive no traffic; a serving service can fail users; a mitigation can improve impact without removing cause; and desired recovery can differ from observed results.

### Answer 2

The counts sum to 2,000,000. Treating unknowns as not good, success over all eligible requests is $1{,}996{,}800/2{,}000{,}000=0.9984$, or 99.84%, below 99.9%. Among classified requests, the denominator is $1{,}996{,}800+2{,}200=1{,}999{,}000$, so success is about 99.8899%, also below 99.9%.

Both labels matter. The first conservatively represents the eligible population; the second isolates measured outcomes but must not hide the 1,000 unknowns. Report good, bad, unknown, collection failure scope, user concentration, and window. Policy may classify unknowns differently only through an explicit risk decision.

### Answer 3

Define high latency by user-relevant SLI, scope, burn, and duration; confirm telemetry health and recent changes. Incident command or delegated service authority approves failover. Preconditions include target-region artifact and configuration, data freshness and quorum, capacity, routing, identity, secrets, compliance, and no conflicting change.

Canary a bounded traffic fraction, observe user success, error, latency, saturation, data conflict, and security signals, then increase under a rate limit. Preserve action identity and decision log. Stop if target errors, lag, saturation, or data risk cross bounds. If source remains safe, shift back; if state diverged, use forward reconciliation rather than blind rollback. Verify user journeys and authoritative state independently of command success. Communicate scope, expected impact, updates, and recovery; escalate data or security uncertainty to its authority.

### Answer 4

Central operations can standardize on-call intake, severity, incident command, access controls, telemetry, and cross-platform response. It also concentrates privilege and failure and may lack product meaning. Federated teams retain service expertise and change autonomy but can produce inconsistent paging, weak coverage, and slow cross-team coordination.

A balanced design assigns each product a service owner, SLOs, runbooks, and technical on-call while a platform group owns common control planes and telemetry. A trained incident commander coordinates broad events. Use shared identity, severity, evidence, communication, escalation, and audit contracts; keep product-specific decisions with domain owners. Review privileged access, prevent platform tooling from becoming an unexamined common cause, and publish control-plane degraded procedures. Learning actions have local owners and cross-cutting governance without one group silently assuming all operational risk.

### Answer 5

Define operational states such as normal automatic service, reduced-speed degraded service, manual authority, maintenance possession, communication-isolated safe state, emergency stop, recovery validation, and return to service. Each state names permitted train movements, speed, route authority, sensor requirements, human roles, entry and exit evidence, and fail-safe behavior.

Sensor disagreement or loss triggers bounded movement policy and operator alert; communication loss prevents unsafe new authority while preserving local protective controls. Maintenance possession requires authenticated geographic scope, track occupancy confirmation, interlocks, expiry, and independent release. Software update drains or isolates equipment, verifies signed compatible artifacts, tests local control, and rolls back only before declared state boundaries.

Incident command coordinates traffic control, field engineering, safety authority, security, emergency services, and passenger communication. Evidence includes independent train detection, controller state, commands, acknowledgments, clocks with uncertainty, configuration digests, operator decisions, and physical inspection. Recovery reconciles field and central state, validates routes and interlocks, runs controlled test movements, removes temporary authority, and obtains safety approval before gradual return. The architecture view supports but does not replace formal railway hazard analysis, certification, and regulated operating rules.
