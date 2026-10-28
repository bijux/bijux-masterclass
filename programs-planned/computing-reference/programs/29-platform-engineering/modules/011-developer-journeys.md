---
module_id: PLAT-011
program: Platform Engineering
level: 1
module_number: 11
title: Developer Journeys
status: complete
last_verified: 2026-09-02
---

# Developer Journeys

## One-Page Review

### Governing question

How can a platform team understand, design, operate, and measure the developer’s complete path from a real trigger to a verified and sustainable outcome across interfaces, teams, providers, waits, failures, recovery, and lifecycle changes?

### Essential definitions

- A **developer journey** is the end-to-end experience and work through which a defined developer or service-owner segment makes progress from a trigger to a verified outcome in context.
- A **journey stage** is a meaningful phase such as discovery, qualification, declaration, fulfillment, validation, integration, operation, change, recovery, or retirement; it is not necessarily one screen or service.
- A **touchpoint** is an interaction with an interface, person, document, message, provider, or system during the journey.
- **Frontstage work** is visible to the consumer. **Backstage work** includes people, processes, systems, rules, and providers that enable or delay the visible experience.
- A **service blueprint** links consumer actions and evidence to frontstage interactions, backstage activities, support processes, ownership, and dependencies.
- A **moment of consequence** is a point where an action or decision materially affects safety, cost, data, availability, reversibility, or responsibility.
- A **journey break** is a state from which the consumer cannot reach the intended outcome through the supported path with understandable recovery.
- A **critical journey** is a high-value, frequent, consequential, strategically important, or foundational journey selected for sustained product ownership and evidence.

### Central model, mechanism, or theorem

Model journey $j$ as $J_j=(U,K,\tau,S,A,D,H,F,X,E,O,L)$: consumer segment $U$, context $K$, trigger $\tau$, states $S$, actions $A$, decisions $D$, handoffs $H$, feedback $F$, exceptions and recovery $X$, evidence $E$, verified outcome $O$, and lifecycle continuation $L$. Map both consumer experience and delivery system. Optimize the complete journey under explicit guardrails; a locally fast interface can coexist with a slow, unsafe, or broken end-to-end service.

### Critical invariants

- Journey scope begins at the consumer’s real trigger and ends only when the outcome is verified and responsibilities are understood.
- Current-state maps come from observed work, operational evidence, support, and diverse consumers—not platform assumptions.
- Active work, waiting, handoffs, uncertainty, failure, recovery, and abandonment remain visible.
- Portal, CLI, API, IDE, documentation, chat, tickets, and provider consoles are channels over journey contracts, not separate realities.
- Consumer, platform, provider, policy, and domain decisions retain named authority throughout the journey.
- Happy path, degraded path, exception, cancellation, retry, rollback, and retirement are first-class.
- Improvements are evaluated across task success, quality, safety, accessibility, cost, consumer effort, and operator burden.

### Common failures

Mapping only screens; beginning at login and ending at “request accepted”; drawing an imagined future path before observing current work; hiding tickets and personal messages; treating a linear happy path as reality; optimizing the platform’s processing time while consumers wait elsewhere; combining unlike segments; ignoring non-users and abandoned attempts; instrumenting clicks without outcome correlation; and publishing a journey map with no owner, backlog, operating evidence, or update cycle.

### Compact example

A “deploy service” journey begins when a team has a tested release candidate, not when it opens the portal. The team discovers the supported workload profile, confirms ownership and policy, declares release intent, previews changes, submits, observes build and rollout, diagnoses a failed health check, rolls back, repairs the application, retries, verifies telemetry and application behavior, communicates readiness, and later upgrades or retires the service. The blueprint also shows policy evaluation, artifact service, runtime provider, platform reconciliation, on-call, and support. A green deployment state is evidence, not the final domain outcome.

### Connections

Retrieve segments and jobs from [PLAT-002](002-platform-consumers-and-jobs-to-be-done.md), cognitive-load analysis from [PLAT-003](003-developer-cognitive-load.md), self-service states from [PLAT-005](005-self-service-and-guardrails.md), team interfaces from [PLAT-009](009-platform-team-boundaries.md), and value hypotheses from [PLAT-010](010-defining-a-platform-s-value-proposition.md). The next module narrows one milestone: [time to first successful deployment](../roadmap.md#block-02--developer-experience-and-platform-interfaces). Later modules own each interface, diagnostics, versioning, discoverability, and experience measurement in depth.

## Governing Question

What work must a developer actually complete—not merely what the platform UI displays—to achieve a useful, verified, recoverable outcome, and how can the platform improve that path without shifting burden or erasing authority?

Developers experience a system of people, interfaces, providers, rules, and delays. Organizational charts and component diagrams are not their journey. A platform can have excellent individual APIs while the complete task remains fragmented across access requests, documentation, identity setup, provider consoles, chat, tickets, approvals, and manual verification.

A journey perspective changes the unit of design from component usage to progress. It asks why the consumer started, what they must know and decide, where responsibility changes, how they learn what happened, what they do when reality diverges, and how the outcome survives later change.

## Why This Matters

Local optimization is seductive. A portal team can reduce form completion from five minutes to two while fulfillment still waits two days. An infrastructure API can return `202 Accepted` immediately while no durable status or recovery exists. A deployment can become green while the application is inaccessible, unobservable, or unsafe.

Current DORA platform guidance recommends mapping critical user journeys such as creating a service and debugging production, prioritizes clear task-outcome feedback, and measures task success alongside adoption, experience, and delivery performance. This supports an end-to-end unit of product work rather than a feature or component metric.

Current GOV.UK service guidance makes the analogous service-design principle explicit: solve a whole problem, join related services into a journey that makes sense to users, and do not make users understand organizational structures. Its journey-mapping guidance combines user experience with online/offline touchpoints, backstage processes, evidence, and the organizations involved. The transfer to internal platforms is direct: developers should not have to reconstruct the platform org chart to complete a routine job.

Service blueprinting provides a durable technique for connecting visible experience with employee actions, backstage processes, support, and physical or informational evidence. Human-centered design adds context of use and lifecycle evaluation. The SPACE framework warns against one-dimensional developer-productivity measurement and organizes satisfaction/well-being, performance, activity, communication/collaboration, and efficiency/flow.

Journey design also reveals product boundaries. If completion depends on an unowned identity queue or provider-specific recovery, the platform promise is incomplete. If a valid domain decision requires application expertise, the journey should request that decision rather than hide or centralize it. A map makes responsibility and coordination debt visible.

## Prerequisites and Retrieval

Retrieve from PLAT-001 the total-system boundary. Retrieve segments, jobs, contexts, and authorities from PLAT-002; cognitive-load drivers from PLAT-003; product lifecycle from PLAT-004; self-service and operation state from PLAT-005; route variation from PLAT-006; capability/provider separation from PLAT-007; external-provider responsibilities from PLAT-008; team interactions from PLAT-009; and value hypotheses from PLAT-010.

You should understand user research, process and state models, service ownership, APIs, identity, policy, observability, incident response, accessibility, qualitative and quantitative evidence, and lifecycle design. Journey mapping is a collaborative analytic practice, not a drawing exercise.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish developer journeys from workflows, interface flows, architecture diagrams, and delivery pipelines;
2. scope a journey from trigger through verified outcome and lifecycle continuation;
3. observe and model consumer actions, decisions, touchpoints, waits, handoffs, providers, exceptions, recovery, evidence, and emotions without substituting assumptions;
4. construct a service blueprint connecting frontstage experience to backstage operation and ownership;
5. select critical journeys using value, frequency, consequence, dependency, and learning evidence;
6. instrument end-to-end task and operation correlation while respecting privacy and bounded interpretation; and
7. redesign and validate journeys without optimizing one channel at the expense of safety, accessibility, recovery, or operator sustainability.

## Core Exposition

### Distinguish the journey from nearby artifacts

A **workflow** describes ordered work, often from the system or process perspective. An **interface flow** describes navigation through screens or commands. A **pipeline** executes automated stages. An **architecture diagram** shows components and relationships. A **journey** centers the consumer’s progress and includes all of these where relevant.

One journey may cross several workflows and interfaces. “Create a service” can include finding the platform, selecting a workload class, establishing a repository, declaring ownership and data context, obtaining access, building, deploying, observing, diagnosing, verifying, and receiving support. Conversely, one platform workflow may participate in several journeys.

Keep the unit tied to a job and outcome. “Use the developer portal” is not a journey because it has no external purpose. “Recover a failed production deployment” is a journey even when it uses a CLI, portal, telemetry product, chat, and human incident process.

### Scope trigger, outcome, and continuation

The trigger is the event or need that starts the consumer’s work: a new service decision, release candidate, expiring credential, incident, provider deprecation, audit request, or retirement decision. Starting at platform login hides discovery, eligibility, preparation, and access.

The outcome is not the last technical operation. It is a verified consumer-relevant state. An environment is useful when the authorized team can use it under the promised controls and observe its status. A deployment is successful when application behavior and required evidence meet the declared acceptance, not merely when a controller reports completion.

Continuation covers operation, change, recovery, and retirement. Some research maps one bounded episode at a time, but the product model must link episodes. A fast creation journey can cause a poor upgrade or deletion journey. Record the handoff and later obligations instead of pretending the experience ends.

### Model a complete journey

Represent journey $j$ as

$$
J_j=(U,K,\tau,S,A,D,H,F,X,E,O,L),
$$

where $U$ is consumer segment, $K$ context, $\tau$ trigger, $S$ observable consumer and system states, $A$ actions, $D$ decisions and authorities, $H$ handoffs, $F$ feedback, $X$ exceptions and recovery, $E$ evidence, $O$ verified outcome, and $L$ lifecycle continuation.

For each stage capture:

- consumer goal, action, decision, question, expectation, and available evidence;
- interface or human touchpoint, including offline and informal channels;
- frontstage response and backstage activity;
- owner, provider, policy authority, dependency, and support path;
- input, output, state, wait, error, retry, cancellation, and recovery;
- active time, elapsed time, coordination, and uncertainty;
- accessibility, security, privacy, cost, and consequence; and
- observed pain, successful workaround, abandoned path, and improvement opportunity.

Do not force the map into a single line. Journeys branch, loop, pause, resume, and terminate. Represent alternative outcomes and the information available at each decision.

### Research the current journey

Begin with actual work. Recruit across segment, experience, workload, location, access needs, outcome, and adoption status. Include consumers who needed support, abandoned, used alternatives, or never found the platform. Observe tasks when possible; recollection often omits routine workarounds and wait.

Combine interviews and contextual inquiry with operation logs, tickets, chat themes, documentation searches, provider events, incidents, cost data, and accessibility research. Ask consumers to show artifacts and transitions. Ask support and provider teams what invisible work occurs.

Separate observed evidence, participant report, analytics, and team inference on the map. Timestamp research and identify gaps. A journey assembled only by platform employees tends to mirror intended architecture rather than lived experience.

Protect participants. Journey instrumentation can expose source names, incidents, skill signals, schedules, or sensitive workload context. Collect the minimum necessary, define purpose and retention, restrict access, aggregate appropriately, and do not turn experience research into individual performance surveillance.

### Build a service blueprint

Use horizontal stages and vertical layers. A practical blueprint includes:

1. consumer actions and decisions;
2. visible evidence, interfaces, people, and messages;
3. frontstage platform responses;
4. backstage platform, provider, and policy work;
5. supporting systems, teams, rules, and data;
6. ownership, handoffs, service objectives, and failure boundaries; and
7. measures, pain points, hypotheses, and open questions.

Draw lines of interaction and visibility. The consumer need not see every provider detail, but the platform must know what makes the promise work. Mark moments of consequence and truth: access granted, irreversible deletion, cost commitment, traffic shift, credential exposure, recovery acceptance, or responsibility transfer.

The blueprint should link to authoritative contracts rather than duplicate fast-changing detail. It is a shared diagnostic model for consumers, product, design, engineering, providers, support, security, and operations.

### Quantify time, wait, and handoffs carefully

Elapsed time is the difference between trigger and verified outcome. Active time is human or system work; wait time includes queues, schedules, propagation, and unknown state. Coordination time may overlap active or wait, so define categories before summing.

The following synthetic stage list shows a 20-minute journey with eight active minutes, 12 waiting minutes, and four actor handoffs. It validates arithmetic only, not journey quality.

<!-- bijux-verify: {"id":"developer-journey-time","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"stages=6\nelapsed=20\nactive=8\nwait=12\nhandoffs=4\noutcome=verified\n","stderr":""}} -->
```python
stages = [
    ("discover", 2, "consumer", "active"),
    ("declare", 3, "consumer", "active"),
    ("policy-wait", 7, "policy", "wait"),
    ("provision", 1, "platform", "active"),
    ("provider-wait", 5, "provider", "wait"),
    ("verify", 2, "consumer", "active"),
]

elapsed = sum(duration for _, duration, _, _ in stages)
active = sum(duration for _, duration, _, kind in stages if kind == "active")
wait = sum(duration for _, duration, _, kind in stages if kind == "wait")
handoffs = sum(left[2] != right[2] for left, right in zip(stages, stages[1:]))
print(f"stages={len(stages)}")
print(f"elapsed={elapsed}")
print(f"active={active}")
print(f"wait={wait}")
print(f"handoffs={handoffs}")
print("outcome=verified")
```

The calculation does not say whether a policy wait is necessary, whether actors work concurrently, or whether verification is adequate. Real event logs need clock definitions, identifiers, missing-event handling, retries, parallelism, privacy controls, and an explicit outcome.

### Design feedback and recovery

At every material transition, consumers need to know what the system accepted, what it is doing, what state is authoritative, whether action is required, what the limits are, and where evidence lives. Feedback should use consumer language while preserving correlation to provider state.

Errors belong in context. State the failed operation, affected resource, retained state, responsible boundary, safe next actions, retry semantics, support correlation, and documentation. A message that exposes a provider code without platform meaning transfers diagnosis.

Map cancellation, timeout, duplicate submission, partial fulfillment, stale status, provider failure, policy denial, invalid consumer input, unsupported context, rollback, compensation, escalation, and resume. Recovery is not an edge case for journey design; it is where independence and trust become testable.

### Coordinate channels around one contract

Portal, CLI, API, IDE, documentation, notifications, and support can meet different contexts. They should expose one capability contract and durable operation identity. A request created in a CLI should be observable through an API or portal where authorized; support should use the same correlation.

Channel parity does not require identical presentation. A screen reader, shell automation, incident responder, and occasional user have different interaction needs. Preserve semantic states, authorization, evidence, and lifecycle while designing channel-appropriate affordances.

Informal chat can reveal and unblock problems, but it should not become an invisible production interface. Convert recurring answers into documentation, diagnostics, product changes, or an explicit support record. Preserve privacy and avoid mining private conversation without consent and governance.

### Select critical journeys

Not every journey can receive equal attention. Select using consumer and organizational value, frequency, consequence, breadth, current failure, foundational dependency, strategic importance, inequity, and learning value. Publish the evidence and excluded scope.

Common platform critical journeys include creating a service, obtaining an environment, deploying a change, debugging production, rotating a credential, recovering a failed change, onboarding an existing workload, responding to provider change, and retiring a service.

Do not select only creation. Mature users spend more time changing, diagnosing, recovering, migrating, and retiring. A platform optimized for demos can have an excellent first journey and a damaging lifetime experience.

### Instrument the journey end to end

Create stable identifiers for consumer intent, operation, resource, provider object, policy decision, support case, change, and incident. Correlate stages without treating a person as the unit of productivity. Record state transition, time, source, outcome, error class, recovery, and evidence freshness.

Define success and eligible attempt. Measure completion, abandonment, independent completion, elapsed and active time, waits, handoffs, retries, rework, error, recovery, support, satisfaction, perceived workload, accessibility, quality, safety, cost, and operator burden.

Use multiple dimensions in the spirit of SPACE rather than one activity count. Activity such as commands, commits, or clicks can help reconstruct work but is not productivity. Communication may be necessary collaboration or avoidable coordination. Efficiency without performance or well-being is incomplete.

### Redesign and validate the future journey

Identify root mechanisms rather than drawing fewer boxes. Remove duplicated declarations, encode deterministic rules, compose providers, externalize state, clarify decisions, design recovery, and move support evidence into the product. Retain meaningful domain choices and human judgment.

Prototype the riskiest stages and degraded paths with representative consumers. Test comprehension, accessibility, authority, operation, failure, support, and recovery. Compare with the current baseline and watch for burden transferred backstage.

Assign journey ownership and a cross-team improvement mechanism. Capability teams own their contracts; one product owner coordinates the end-to-end proposition and evidence. Review maps after incidents, provider changes, policy changes, research, and material releases. Archive obsolete maps with dates rather than presenting them as current truth.

## Definitions and Notation

$J_j=(U,K,\tau,S,A,D,H,F,X,E,O,L)$ models a journey through segment, context, trigger, states, actions, decisions, handoffs, feedback, exception/recovery, evidence, outcome, and lifecycle continuation.

For one non-overlapping sequential trace, elapsed time is $T_e=\sum_i t_i$. If each stage is classified active or waiting, $T_e=T_a+T_w$. Real journeys can have concurrency, missing events, rework, and human activity overlapping system wait; the equality applies only after the trace and classification rules are stated.

For adjacent stages with actors $q_i$, handoff count is

$$
H=\sum_{i=1}^{n-1}\mathbf{1}[q_i\ne q_{i+1}].
$$

A handoff is not automatically waste. It can preserve authority or expertise; repeated handoffs without useful state transfer are stronger redesign evidence.

## Mechanisms, Invariants, or Proof Structure

Use a repeating loop: select a bounded job; recruit representative participants; observe current work; assemble evidence; map experience and service landscape; blueprint frontstage/backstage delivery; identify breaks and consequence points; write improvement hypotheses; prototype; instrument; release gradually; compare outcomes; and update the map.

The scope invariant prevents a platform-centric start or end. The evidence invariant separates observation from inference. The authority invariant preserves consumer, platform, provider, and policy decisions. The lifecycle invariant connects creation to operation, change, recovery, and retirement. The system invariant prevents channel speed from masking backstage queues and operator toil.

Validate arithmetic only where the trace supports it. Parallel branches require interval union or a critical-path model, not naive summation. A missing event is not zero duration. An accepted request is not completion. A successful platform operation is not necessarily a verified domain outcome.

Adversarial review includes: new versus expert users; voluntary versus mandated use; successful versus abandoned attempts; ordinary versus degraded paths; synchronous versus asynchronous work; portal versus automation; supported versus escaped workloads; accessible versus inaccessible channels; platform health versus provider failure; and fast creation versus costly lifetime operation.

## Alternatives and Trade-Offs

**Journey map** emphasizes consumer experience, goals, pain, and evidence. It can hide delivery mechanics. Pair it with a service blueprint when backstage ownership matters.

**Service blueprint** exposes delivery layers and handoffs. It can become an architecture diagram that loses human context. Keep consumer actions and evidence as the reference line.

**Process map or BPMN** precisely models control flow and decisions. It can over-specify an imagined process and omit emotion, comprehension, informal work, and abandonment. Derive it from observed journey evidence where automation needs rigor.

**Event-log analysis** measures large-scale traces and variation. It sees only instrumented behavior and can threaten privacy or misclassify outcomes. Combine it with research and explicit governance.

**Embedded observation** reveals context and workarounds. It is time-intensive and can influence behavior. Sample deliberately and triangulate with longitudinal signals.

**One universal journey** offers simple governance but erases segment and workload differences. Use a common contract with distinct profiles or separate journeys when decisions and outcomes differ materially.

## Failure Modes and Misconceptions

- **“The journey is the portal flow.”** Developers cross channels, teams, providers, and offline work before and after the portal.
- **“Request accepted means success.”** Acceptance establishes receipt, not fulfillment, readiness, integration, or domain verification.
- **“Fewer steps means better.”** A preview or confirmation can reduce irreversible harm; count purpose and burden, not boxes.
- **“All handoffs are waste.”** Some preserve authority and specialization; unclear state and avoidable coordination are the target.
- **“Telemetry tells us the journey.”** Logs omit intent, comprehension, informal work, abandonment, and uninstrumented alternatives.
- **“The average developer journey improved.”** Averages can hide novices, experts, disabled users, specialist workloads, and severe tails.
- **“Happy-path usability is developer experience.”** Failure, recovery, support, upgrade, and retirement determine long-term independence.
- **“One channel should do everything.”** Different contexts need different affordances over consistent semantics.
- **“The map is the deliverable.”** Value comes from owned changes, operating evidence, and maintained shared understanding.
- **“More developer activity means productivity.”** Activity is one signal and can rise because the journey became more fragmented.

## Worked Examples

### Example 1

A new-service journey begins with architecture approval in a document, crosses repository creation, ownership registration, identity, build, deployment, telemetry, and support, and ends at verified service readiness. Mapping only the template made the platform miss three days of access waits. The redesign pre-qualifies access and makes decisions visible.

### Example 2

A credential-rotation API responds quickly, but consumers wait for propagation and cannot tell which workloads adopted the new version. The journey adds overlap state, consumer rollout evidence, expiry, revocation, and recovery. API latency remains useful but no longer stands in for completion.

### Example 3

Expert teams avoid a portal because it hides provider options needed for data residency. Their provider-direct path is mapped rather than labeled resistance. The platform creates an explicit specialist profile and preserves consequential provider exposure while sharing identity, audit, and support.

### Example 4

A policy denial message says only “forbidden.” The blueprint shows the platform has policy reason, authority, and remediation metadata backstage but drops it at the interface. The product exposes scoped explanation, retained state, safe correction, and an exception route without weakening authorization.

### Example 5

A deployment succeeds technically while application smoke tests and telemetry fail. The journey separates platform rollout completion from application readiness. The application team owns domain acceptance; the platform correlates evidence and offers rollback without claiming application truth.

### Example 6

A screen-reader user can submit an environment request but asynchronous status changes are not announced. Research across the full journey finds the user repeatedly refreshes and misses an expiry warning. The redesign adds semantic live status, notification preference, and accessible recovery—not merely form labels.

### Example 7

Chat analysis suggests frequent help with database deletion. Consent-governed research shows the real issue is uncertainty about backups and billing after deletion. The platform adds deletion phases, retention evidence, cost stop time, cancellation boundaries, and a durable support case rather than a chatbot answer.

### Example 8

During a provider control-plane outage, existing workloads serve but creates and deletes cannot be reconciled. The degraded journey exposes stale observation time, queues safe intent, blocks unsafe irreversible work, links incident status, and reconciles after recovery. A generic red banner would not guide action.

### Example 9

A platform measures a 12-minute median deployment but excludes failed attempts that never emit the final event. Reconstructing the eligible denominator reveals abandonment and a 90-minute tail caused by ownership metadata. The team repairs instrumentation and the early-stage dependency before claiming improvement.

### Example 10

A service-retirement journey spans consumer inventory, dependency notice, data export, traffic removal, access revocation, evidence retention, provider deletion, cost closure, and catalog history. Treating “delete runtime object” as the journey left credentials, invoices, and dependents behind.

## Cross-Program Connections

Human-computer interaction and service design contribute contextual research, accessibility, journey mapping, service blueprints, touchpoints, and evaluation. Product management connects journeys to segments, value hypotheses, priorities, and lifecycle. Process engineering contributes flow, queues, handoffs, work-in-progress, and control models.

API and distributed-systems engineering contribute durable operation identifiers, asynchronous state, idempotency, retries, partial failure, and observability. Reliability engineering contributes degraded paths, incident coordination, recovery, and objectives. Security and privacy engineering define identity, decision authority, data-minimizing instrumentation, and safe support.

Organizational design makes backstage ownership and incentives visible. Data engineering helps reconstruct traces and uncertainty without equating available data with truth. Ethics and accessibility review ensure that convenience for the modal consumer does not become exclusion, surveillance, or burden for others.

## References

- DORA, [*Platform Engineering*](https://dora.dev/capabilities/platform-engineering/), updated January 12, 2026. Current guidance on critical user journeys, clear task-outcome feedback, task success, developer experience, adoption, and delivery outcomes.
- DORA, [*2024 Accelerate State of DevOps Report*](https://dora.dev/research/2024/dora-report/), corrected edition v2024.3. Empirical platform, developer-independence, user-centeredness, productivity, throughput, and stability findings with survey limitations.
- UK Government Digital Service, [*Solve a Whole Problem for Users*](https://www.gov.uk/service-manual/service-standard/point-2-solve-a-whole-problem), updated January 29, 2026. Current end-to-end journey, cross-organizational responsibility, user-centered scope, alternatives, and incremental improvement guidance.
- UK Government Digital Service, [*Map and Understand a User's Whole Problem*](https://www.gov.uk/service-manual/design/map-a-users-whole-problem), current Service Manual retrieved 2026. Current service-landscape, touchpoint, backstage-process, evidence, stakeholder, experience-map, and cross-boundary change guidance.
- UK Government Digital Service, [*Designing Good Government Services: An Introduction*](https://www.gov.uk/service-manual/design/introduction-designing-government-services), current Service Manual retrieved 2026. Beginning-to-end design across digital, offline, supplier, support, exception, and unpredictable technical paths.
- Mary Jo Bitner, Amy L. Ostrom, and Felicia N. Morgan, [“Service Blueprinting: A Practical Technique for Service Innovation”](https://doi.org/10.2307/41166446), *California Management Review* 50(3), 2008. Peer-reviewed foundation for customer actions, visible contact, backstage employee actions, support processes, evidence, and service innovation.
- ISO, [ISO 9241-210:2019 — *Human-Centred Design for Interactive Systems*](https://www.iso.org/standard/77520.html), reviewed and confirmed 2025. Current human-centered lifecycle, context-of-use, multidisciplinary, and evaluation principles.
- Nicole Forsgren, Margaret-Anne Storey, Chandra Maddila, Thomas Zimmermann, Brian Houck, and Jenna Butler, [“The SPACE of Developer Productivity”](https://queue.acm.org/detail.cfm?id=3454124), *ACM Queue* 19(1), 2021. Satisfaction/well-being, performance, activity, communication/collaboration, and efficiency/flow framework with multi-level measurement guidance.
- Katherine N. Lemon and Peter C. Verhoef, [“Understanding Customer Experience Throughout the Customer Journey”](https://doi.org/10.1509/jm.15.0420), *Journal of Marketing* 80(6), 2016. Peer-reviewed synthesis of journey stages, touchpoints, channels, experience, and organizational research challenges.

## Exercises

### Exercise 1

Map the current journey for creating a development environment, beginning at the real trigger and ending at verified usefulness. Include stages, decisions, touchpoints, backstage work, waits, handoffs, failures, recovery, evidence, and lifecycle continuation.

### Exercise 2

A deployment portal reports a median completion time of eight minutes. Design an investigation that determines whether this measures the complete developer journey and whether the journey improved.

### Exercise 3

Create a service blueprint for rotating a workload credential. Allocate consumer, platform, identity-provider, security-authority, application, and support responsibilities across normal, failed, cancelled, and emergency paths.

### Exercise 4

Choose three critical journeys for a platform serving stateless services, data pipelines, and machine-learning workloads. Defend the selection using value, frequency, consequence, dependency, inequity, and learning evidence without inventing one universal journey.

### Exercise 5

Transfer the journey model to a regional hospital laboratory-result platform. Map trigger through verified clinical receipt and correction, preserving laboratory truth, clinical interpretation, privacy, accessibility, downtime, support, and patient recourse.

## Answers to the Exercises

### Answer 1

The trigger is an approved need for a bounded development task. Stages are discover and qualify; identify owner, project, workload, data class, region, expiry, and budget; establish access; preview derived identity/network/policy/cost; submit; observe validation and provisioning; receive locators and authorization; connect the workload; verify function, telemetry, isolation, and ownership; use and change; renew or expire; recover from failure; and delete with retained evidence. Touchpoints may include docs, CLI/API/portal, identity, policy, provider, notifications, catalog, telemetry, billing, and support. Backstage work includes authorization, account placement, quota, reconciliation, provider calls, evidence, and cleanup. Map access and approval waits, actor handoffs, invalid declarations, partial resources, stale status, provider outage, cancellation, duplicate requests, and deletion failure. The outcome is an authorized, usable, observable environment; continuation links to change, recovery, expiry, and verified deletion.

### Answer 2

First identify timer boundaries: portal submission to platform state may exclude discovery, access, preparation, queueing, application verification, failures without completion events, and later recovery. Define the eligible attempt denominator, real trigger, and verified application outcome. Correlate request, operation, provider resource, deployment, policy, telemetry, support, and application evidence. Include abandoned and retried attempts, tails, degraded periods, and users of other channels. Measure elapsed and active time, waits, handoffs, independent completion, errors, recovery, quality, accessibility, satisfaction, and operator load. Observe representative novices, experts, disabled users, and workload profiles; compare against a pre-change or staggered baseline while recording concurrent changes. The eight-minute metric remains a bounded platform-stage measure, not proof of journey improvement.

### Answer 3

The application owner decides timing and validates consumers; security defines credential policy and emergency authority; the platform exposes one rotation operation, validates context, coordinates state, and communicates; the identity provider issues and revokes versions; workloads adopt the new identity; support uses the same correlation. Normal states include requested, authorized, issued, overlap, rollout observed, old revoked, and complete. Failure records whether old and new credentials remain valid and who acts. Cancellation before issuance stops; after issuance it compensates by revoking the new version or reports incomplete cleanup. Emergency rotation uses predeclared authority, short bounds, notification, and later review. Evidence includes decision, issuer event, active versions, workload adoption, revocation, expiry, support, and audit. The platform cannot declare application recovery solely from provider issuance.

### Answer 4

Choose “deploy and recover a stateless service” for high frequency, shared dependencies, and direct delivery value; include recovery so creation does not dominate. Choose “diagnose and restore a failed data pipeline” for data correctness, lineage, and consequential operational learning; its states differ from request/response service recovery. Choose “obtain and retire a governed accelerator workspace” for costly, specialized, inequitable access and provider dependencies in ML. Share identity, evidence, cost, and support semantics, but keep separate decisions and outcomes. Use observed demand, incident severity, wait, abandonment, support, access barriers, and strategic commitments. Revisit selection if a rare journey is not platform-owned or another foundational failure affects more consumers.

### Answer 5

The trigger is a laboratory-validated result or correction ready for authorized routing. Stages include patient/context match; provenance and code validation; privacy and purpose check; route resolution; durable transmission; receiving-system acknowledgement; clinician-work-queue visibility; urgent escalation; clinical receipt; correction or supersession; records retention; and patient-facing access or recourse where applicable. The blueprint shows laboratory systems, identity, terminology, platform routing, clinical records, notifications, downtime queues, support, and audit. Laboratories own result truth and correction; clinicians own interpretation and treatment; privacy/records authorities own access and retention; the platform owns technical state and correlation. Map mismatch, duplicate, delay, inaccessible notification, provider outage, stale acknowledgement, correction race, emergency access, and reconciliation. Verified transport is not verified clinical interpretation; evidence must preserve both boundary and human recourse.
