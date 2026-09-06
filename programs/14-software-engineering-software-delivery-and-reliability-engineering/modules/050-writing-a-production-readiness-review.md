---
module_id: SDRE-050
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 50
title: Writing a Production-Readiness Review
status: complete
last_verified: 2026-09-06
---

# Writing a Production-Readiness Review

## One-Page Review

### Governing question

How can a team turn evidence about a service, its operators, and a proposed launch into an accountable readiness decision without reducing judgment to checkbox theater or claiming that one review proves future reliability?

### Essential definitions

- a **production-readiness review (PRR)** is a structured, evidence-based examination of whether a defined workload and operating organization are prepared for a defined production change;
- **review scope** identifies the service boundary, change, environments, traffic, tenants, dependencies, regions, data, and time horizon covered;
- a **control objective** states the property that must hold, while a **control mechanism** is how the system attempts to establish it;
- **evidence** is a reproducible observation supporting or contradicting a readiness claim, with provenance, environment, owner, and date;
- a **finding** is a specific gap, uncertainty, or risk discovered by the review;
- a **blocker** is an unresolved finding whose declared acceptance rule forbids launch;
- a **condition** is bounded follow-up that may remain open under named ownership and explicit risk acceptance;
- **residual risk** remains after implemented controls and mitigations;
- a **readiness decision** is `ready`, `conditional`, or `not ready` for the stated scope and decision time;
- **expiry** marks when evidence or a decision must be revisited because the workload, environment, assumptions, or risk has changed.

### Central model, mechanism, or theorem

Let $C$ be mandatory control objectives, $s_c\in\{0,1\}$ indicate whether current evidence satisfies objective $c$, and $B$ be unresolved blocking findings. A necessary readiness predicate is

$$
R=\left(\bigwedge_{c\in C}s_c=1\right)\land(|B|=0).
$$

This predicate prevents a high aggregate score from hiding a missing mandatory property. It is not sufficient by itself: reviewers must establish scope, evidence quality, risk ownership, launch controls, and the limits of the conclusion. A conditional decision is legitimate only when no blocker is open and every remaining condition has an owner, deadline, verification method, bounded exposure, and authorized risk acceptance.

### Critical invariants

- identify the exact launch or production change before asking whether it is ready;
- review the workload, operating system, people, procedures, and dependencies together;
- phrase questions as control objectives and require evidence, not confident assertions;
- derive service-specific questions from architecture, user harm, incidents, and local standards;
- keep mandatory gates separate from prioritization scores;
- record every finding with severity, owner, due date, disposition, and verification method;
- require capacity, failure, recovery, rollback, and on-call evidence under declared conditions;
- make the decision authority and risk-acceptance authority explicit;
- bound rollout with progressive exposure, stop signals, rollback triggers, and emergency controls;
- expire or reopen the review when material assumptions change.

### Common failures

Failures include copying a generic checklist, reviewing an undefined boundary, accepting links without inspecting evidence, scoring away a blocker, trusting nominal capacity, omitting third-party dependencies, treating a runbook as proof of recovery, assigning findings to teams rather than accountable people, launching with no stop authority, allowing waivers without expiry, reviewing only software while ignoring staffing, using historical launch evidence after major change, and calling a self-review certification or external approval.

### Compact example

A payments API has passing functional tests and 40% normal CPU utilization. The PRR finds that loss of one zone leaves only 90 requests/second of measured safe capacity against a 110 requests/second launch requirement. The capacity objective is mandatory, so polished dashboards and a high checklist score cannot make the service ready. The team either reduces launch exposure below the tested survivor limit, adds and verifies capacity, or records `not ready`. The finding names an owner, evidence needed for closure, and a decision date.

### Connections

[SDRE-047](047-failure-domains.md), [SDRE-048](048-redundancy-and-diversity.md), and [SDRE-049](049-graceful-degradation.md) supply core readiness evidence about correlated loss, survivor behavior, and bounded reduced service. [SDRE-051](../ROADMAP.md) next develops incident severity and classification, which a PRR must connect to paging, authority, and launch-stop rules.

## Governing Question

A production launch changes who can be harmed, how quickly faults propagate, and who must respond. Unit tests may establish local behavior, but they do not show that capacity survives a domain loss, alerts reach an empowered operator, data can be restored, a rollback remains compatible, or dependencies can absorb launch traffic. A review is needed because the important evidence is distributed across architecture, delivery, reliability, security, data, product, support, and operations.

The review can still fail even when every question has an answer. Vague scope makes answers nonbinding. Binary checkboxes conceal evidence quality. An average score permits ten easy controls to outweigh one absent safety property. A waiver without an owner becomes permanent. A document frozen at approval decays while the system changes.

The governing question is therefore how to write a PRR that produces a defensible, time-bounded decision. The artifact must tell a later reader what was reviewed, which claims were tested, what remains uncertain, who owns each risk, why exposure is acceptable, and which event invalidates the decision.

## Why This Matters

Google's SRE account describes a PRR as a process for identifying a service's reliability needs from its specific details and, in its described operating model, as a prerequisite before an SRE team accepts production responsibility [1]. The durable lesson is not that every organization needs Google's ownership structure. It is that operational responsibility should follow explicit analysis, improvements, training, and transfer rather than an informal handoff.

Google's discussion of reliable product launches says launch checklists must be tailored to local infrastructure and cover themes such as architecture, dependencies, capacity, failure, monitoring, security, automation, and rollout [2]. Its published historical checklist, identified as circa 2005, is useful evidence of enduring categories but not a current universal template [3]. Current protocols, controls, risks, and organizational obligations must be verified locally.

AWS's current operational-readiness material treats the review as both a process and a checklist, recommends deriving questions from incidents and organizational requirements, and tracks residual risk and action items [4], [5]. This is source-specific guidance, not proof that completing a vendor questionnaire makes any workload safe. A useful PRR converts relevant guidance into local claims and verifies them against the actual workload.

Current Microsoft testing guidance recommends combining test types and selecting them by workload risk, including end-to-end, integration, load, stress, resilience, and security testing [6]. The durable implication is that no single green test category proves production readiness. These current vendor claims and canonical URLs were checked on 2026-09-06.

## Prerequisites and Retrieval

Retrieve service boundary, user journey, criticality, owner, dependency, failure domain, SLI, SLO, error budget, capacity, saturation, redundancy, degradation, recovery-time objective, recovery-point objective, alert, runbook, rollback, change window, threat, data classification, risk, mitigation, and residual risk.

From SDRE-041 through SDRE-045 retrieve reliability properties, measurement, objectives, agreements, and policy. From SDRE-046 retrieve automation ownership and reconciliation. From SDRE-047 retrieve transitive failure-domain analysis. From SDRE-048 retrieve survivor capacity, state, and failover requirements. From SDRE-049 retrieve honest degraded contracts, resource stability, and failback. The PRR does not replace those analyses; it asks whether their claims are current, coherent, and supported for the proposed exposure.

## Learning Objectives

After completing this module, you should be able to:

1. define a bounded PRR purpose, scope, decision, and expiry;
2. distinguish control objectives, mechanisms, claims, evidence, findings, and decisions;
3. tailor a review from architecture, user consequences, incidents, and organizational requirements;
4. evaluate evidence for relevance, provenance, representativeness, freshness, and reproducibility;
5. prevent aggregate scores from hiding mandatory-control failures;
6. write actionable findings with explicit closure and acceptance rules;
7. review architecture, capacity, observability, release, recovery, security, data, and operations coherently;
8. specify a progressive launch plan with stop, rollback, and emergency authority;
9. distinguish ready, conditional, and not-ready outcomes without overstating assurance;
10. keep readiness current through expiry, triggers, automation, and incident learning.

## Core Exposition

**Begin with the decision, not the questionnaire.** State the proposed change: for example, “open version 3 of the document API to 10% of European tenants, with writes enabled, on 2026-10-01.” Name the decision maker, reviewers, required approvers, review date, and latest valid decision date. Define what `ready`, `conditional`, and `not ready` mean before evidence is collected.

Scope the workload boundary. List serving components, control planes, data stores, queues, identity paths, deployment systems, observability, human escalation, and external providers. State regions, tenants, traffic classes, data classifications, planned load, launch spike, growth horizon, and excluded paths. An exclusion is not harmless: name its owner and explain why it cannot invalidate the decision.

Record assumptions explicitly. Examples include available staffing, a dependency quota, a maximum request mix, a recovery region, a schema version, and a traffic forecast. Give each material assumption an evidence link or named validator. If changing an assumption would reverse the decision, make it a reopening trigger.

**Write service-specific control objectives.** A checklist question such as “Is monitoring configured?” invites ceremonial compliance. A control objective such as “within two minutes, the on-call engineer can detect and localize any launch-caused breach of the checkout availability SLO by region and version” states a property. The team can then show signal definitions, alert routing, a test event, timing evidence, and limitations.

Organize objectives by risk, not document ownership. A practical review normally covers user journeys and service levels; architecture and dependencies; failure domains and degraded behavior; capacity and performance; observability and diagnosis; paging and incident command; build, deployment, rollback, and configuration; data integrity, backup, and restoration; security, privacy, and abuse; continuity and disaster recovery; support and communication; and launch governance. Include accessibility, legal, financial, or physical-safety properties when applicable.

Tailor questions from four inputs. First, trace critical user journeys and ask what could make their outcomes wrong, unavailable, slow, unsafe, or misleading. Second, inspect the architecture and dependency graph for state, authority, limits, and shared domains. Third, turn relevant incident causes and near misses into prevention or detection objectives. Fourth, incorporate organizational and regulatory requirements with traceable ownership. A generic baseline may seed the work, but local consequence determines mandatory status.

Keep one objective atomic enough to decide. “Reliability is good” is not reviewable. “The write path rejects rather than acknowledges when durable quorum is unavailable” and “the read path labels results older than five minutes” are separately testable. Avoid forcing several independent properties into one yes/no item.

**Demand evidence that matches the claim.** A claim is what the team believes. A design document explains intent. A configuration or code inspection shows an implemented mechanism. A controlled test observes behavior in a declared environment. A production observation demonstrates behavior under a particular exposure. These evidence forms answer different questions; none is automatically strongest for every claim.

Evaluate evidence along five dimensions. **Relevance** asks whether it addresses the objective. **Provenance** identifies who or what produced it and from which version. **Representativeness** compares test conditions with expected production conditions. **Freshness** checks whether later changes invalidated it. **Reproducibility** records commands, fixtures, environment, outputs, and limitations. A screenshot without query, time range, version, and population is weak evidence even if its graph is green.

Record negative and boundary evidence. Capacity evidence should include saturation and failure-mode behavior, not just a successful average load. Recovery evidence should include an actual restore and integrity check, not only a backup configuration. Rollback evidence should cover schema and state compatibility. Alert evidence should test notification delivery, deduplication, silence behavior, and human action. Security evidence should exercise denied and adversarial paths, not only successful authentication.

Do not confuse environmental observation with a universal guarantee. A 30-minute test at 1,000 requests/second on version `abc123` establishes only that observed behavior under that workload and environment. The review should state which request mix, data volume, cache state, dependency behavior, and failure injection were absent.

**Make mandatory gates explicit.** Some objectives protect properties that cannot be traded against convenience or schedule. Represent them as predicates rather than points. Examples may include authorization enforcement, durable acknowledgement, survivor capacity, recoverable critical data, reachable on-call ownership, and a viable stop or rollback path. The actual list depends on consequence and authority.

Scoring can help order improvements, but it must not decide readiness by averaging unlike risks. A 96% score says little if the missing 4% is restore capability. If the organization uses a maturity or risk score, show its scale, assumptions, and intended use. Apply mandatory gates first; use scores only among otherwise feasible choices.

For a quantitative risk model, let finding $i$ have estimated probability $p_i$ over a declared window and impact $I_i$ in a declared unit. Expected exposure $E_i=p_iI_i$ may support comparison. It does not capture fat tails, correlated failures, ethical constraints, uncertainty, or mandatory duties. Use ranges and sensitivity when estimates are weak, and never let a small guessed probability erase a catastrophic or prohibited outcome.

**Review architecture and dependencies as operated.** Include a current context diagram, request and data flows, trust boundaries, authority, and ownership. For each dependency record function, criticality, contract, timeout, retry, quota, load contribution, failure behavior, observability, and escalation. Trace transitive shared domains rather than treating vendor or service names as independence.

Ask what happens under machine, zone, region, network, control-plane, identity, and operator loss as applicable. Verify survivor capacity, state freshness, quorum placement, fencing, routing convergence, and failback. A redundant diagram is not evidence that the system continues to provide the declared user property.

Review degraded modes end to end. Name what clients receive, what work is omitted, which invariants remain, how modes enter and exit, how retry behavior changes, how debt accumulates, and how users are informed. Confirm that a frontend omission actually suppresses backend work and that stale or partial data retains provenance.

**Review capacity and performance from forecasts to failure.** Define workload units that predict resource use: requests by operation, messages, records, bytes, concurrent sessions, tenant skew, or another causal measure. Record forecast source, launch spike, growth horizon, uncertainty, and dependency amplification. Convert demand into every limiting resource rather than relying on CPU alone.

Let measured usable capacity be $C$ and declared launch load be $L$. Headroom fraction is

$$
H=\frac{C-L}{C}, \qquad C>0.
$$

The arithmetic is descriptive, not a universal acceptable threshold. `C` must be measured for the relevant request mix, latency objective, error criterion, data scale, and failure mode. If one-zone-loss capacity is 900 requests/second and launch load is 850, the nominal 5.56% headroom may be too small for forecast error or cache warming even though $L<C$.

Check queues, backlogs, storage growth, quotas, network, locks, pools, caches, and downstream limits. Review overload control, admission, retry budgets, backpressure, priority, and graceful degradation. Define growth alerts and capacity lead time. A plan to add capacity after saturation is only credible if its control-plane, quota, provisioning, and warmup path fit inside the available time.

**Review observability and response as a closed loop.** Map critical user outcomes to SLIs and objectives. Confirm that dashboards retain population, units, time, version, region, and degraded-mode context. Alerts should identify urgent user harm or an imminent loss of the ability to protect users; every page needs an owned action and a reachable escalation route.

Walk through detection, triage, mitigation, recovery, verification, and communication. Test that the paging system reaches the actual rotation, not merely that a rule exists. Check staffing, time zones, access, training, incident roles, dependency contacts, support scripts, status communication, and decision authority. A runbook is useful only if a qualified responder can execute it with available credentials and current interfaces.

Classify plausible incidents and connect severity to response time, leadership, communication, and launch-stop policy. Define who may reduce traffic, disable a feature, roll back, fail over, or accept degraded operation. Emergency access needs authentication, audit, expiry, and a path independent enough to survive the target incident.

**Review change and rollback as state transitions.** Record artifact identity, provenance, tests, configuration, migration order, compatibility window, and deployment segmentation. A progressive rollout limits simultaneous exposure only when cohorts are independent enough, telemetry distinguishes them, and automation can stop before the next increment.

Define rollout stages by measurable exposure, not adjectives such as “small.” For each stage specify duration or minimum sample, success criteria, stop signals, decision owner, and next action. Include quiet-period and peak-period behavior when they differ. Protect against an automatic rollout advancing on missing or aggregated telemetry.

Rollback is not simply redeployment of an older binary. Check data migration reversibility, protocol compatibility, queued messages, cache format, configuration, feature flags, and external side effects. When rollback is unsafe, define roll-forward or traffic isolation and test it. Record the latest point at which each recovery action remains valid.

**Review data, recovery, and security by property.** Classify data and define correctness, durability, confidentiality, integrity, retention, deletion, locality, and audit requirements. Map acknowledgement rules and replication. Verify backups through restoration, reconciliation, and application-level integrity checks. Compare measured recovery time and recoverable point with declared objectives, including access and dependency delays.

Identify trust boundaries, identities, privileges, secrets, supply-chain inputs, abuse paths, and tenant isolation. Include threat modeling and applicable security review without claiming that a PRR substitutes for specialist approval. Verify denied operations, revoked access, rotation, audit capture, and emergency access. Record unresolved security findings under the authority that can accept them.

**Turn gaps into controlled decisions.** Every finding should contain: identifier; violated or uncertain objective; observation and evidence; scenario; user or business consequence; severity rationale; blocking status; owner; mitigation; due date; verification method; disposition; residual risk; and acceptance authority. “Team to investigate” is not actionable ownership.

Use `ready` only when mandatory objectives have current supporting evidence and no blocker is open. Use `conditional` when the launch can proceed within explicitly bounded exposure while nonblocking work remains. Each condition needs an owner, deadline, verification, monitoring, rollback or containment, and authority. Use `not ready` when a blocker remains, essential evidence is unavailable, or decision authority cannot accept the exposure.

The following executable model illustrates gate-based classification. It deliberately does not calculate an average score.

<!-- bijux-verify: {"id":"classify-readiness-decision","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"decision=conditional\nopen_blockers=0\nopen_conditions=1\n","stderr":""}} -->
```python
findings = [
    {"id": "CAP-1", "blocking": True, "status": "closed"},
    {"id": "REC-1", "blocking": False, "status": "open"},
    {"id": "DOC-1", "blocking": False, "status": "accepted"},
]

unresolved = [item for item in findings if item["status"] == "open"]
blockers = [item for item in unresolved if item["blocking"]]
conditions = [item for item in unresolved if not item["blocking"]]

if blockers:
    decision = "not_ready"
elif conditions:
    decision = "conditional"
else:
    decision = "ready"

print(f"decision={decision}")
print(f"open_blockers={len(blockers)}")
print(f"open_conditions={len(conditions)}")
```

The observed output establishes this small program's behavior under CPython 3.14.4, not the correctness of any organization's readiness policy. A real decision must also validate mandatory controls, finding metadata, evidence freshness, authorized acceptance, and scope.

**Write the launch and follow-through plan.** The PRR should end with the decision, rationale, scope, conditions, blockers, evidence index, launch stages, success criteria, stop and rollback signals, communication, observation window, and next review. Make the artifact searchable and immutable enough to reconstruct the decision while linking to versioned evidence.

Specify post-launch verification. Compare real request mix, capacity, SLI behavior, dependency load, degraded operation, support contacts, and incident signals with assumptions. Close findings only with their declared evidence. Capture surprises and incidents as changes to control objectives, tooling, architecture, or training rather than endlessly appending checklist items.

Set expiry and reopening triggers. Material architecture or dependency changes, new data classes, traffic beyond reviewed bounds, ownership changes, expired recovery evidence, severe incidents, and long elapsed time can invalidate readiness. Automate stable facts such as configuration, policy, backup age, and ownership checks, but retain human judgment for consequence, ambiguity, and trade-offs.

## Definitions and Notation

Let $S$ be the declared review scope and $A=(a_1,\ldots,a_n)$ its material assumptions. Let $C$ be mandatory control objectives. For each $c\in C$, $s_c=1$ only when evidence relevant to scope $S$ is current and meets the objective's acceptance rule; otherwise $s_c=0$.

Let $F$ be findings, partitioned into resolved findings, accepted nonblocking conditions, open nonblocking conditions, and open blockers $B$. The gate predicate is

$$
R=\left(\bigwedge_{c\in C}s_c=1\right)\land(|B|=0).
$$

`Ready` requires $R$ and no open conditions. `Conditional` requires $R$, plus controlled open conditions with authorized acceptance. `Not ready` follows when $R$ is false, a blocker is open, or indispensable evidence is unavailable. These definitions are a review policy model, not a theorem that guarantees reliability.

For evidence item $e$, record production time $t_e$, applicable artifact or system version $v_e$, environment $q_e$, producer $o_e$, and limitations $l_e$. At decision time $t_d$, evidence age is $a_e=t_d-t_e$. An age bound is meaningful only with change and risk context; some evidence becomes invalid on a version change even when chronologically recent.

For a capacity test with measured acceptable throughput $C>0$ and scoped demand $L$, nominal headroom is $H=(C-L)/C$. For finding $i$, optional expected-exposure analysis may use $E_i=p_iI_i$ over a stated window. Both calculations require units and assumptions and remain subordinate to mandatory constraints and uncertainty.

## Mechanisms, Invariants, or Proof Structure

**Scope-binding argument.** Evidence establishes an observation only for its artifact, environment, workload, and time. If the launch differs materially from those conditions, the evidence does not directly satisfy the claim. Therefore every accepted evidence item must be bound to scope or accompanied by a justified transfer argument.

**Gate-before-score argument.** Suppose mandatory objective $c^*$ is unsatisfied. Any weighted average can be increased by adding or heavily weighting unrelated satisfied items while $c^*$ remains false. Therefore an average cannot enforce mandatory readiness. Evaluate the conjunction of mandatory predicates before any score-based prioritization.

**Operational-loop invariant.** For each critical failure, the review traces detectable user consequence to an owned signal, reachable responder, executable mitigation, recovery verification, and communication. A break in any link means documentation alone does not establish operability.

**Survivor-capacity condition.** If scoped load $L$ exceeds measured usable capacity $C_d$ after failure of tolerated domain $d$, queues, rejection, or objective breaches must occur unless admission or work changes. Therefore $C_d\ge L$ is a necessary capacity condition under the model, with additional margin needed for uncertainty and transition effects.

**Finding-closure invariant.** A finding is closed only when its predefined verification method produces acceptable evidence for the same objective and scope. Completing a ticket, changing prose, or accepting risk does not establish control effectiveness. Accepted risk remains a separate disposition with authority and expiry.

**Decision-expiry argument.** Readiness depends on $S$, $A$, control state, evidence, and findings at decision time. A material change to any of these premises can make the prior conclusion inapplicable. An expiry or reopening mechanism is therefore part of the decision, not administrative decoration.

**Assurance boundary.** Passing a PRR means the declared process found sufficient bounded evidence under its policy. It cannot prove the absence of unknown faults, future operator error, adversarial behavior, correlated failure, or environmental change. Honest wording preserves the distinction between reviewed readiness and guaranteed reliability.

## Alternatives and Trade-Offs

**Central review board versus embedded peer review.** A central group can preserve consistency, independence, and cross-service learning, but can bottleneck launches and miss local detail. Embedded reviewers understand the system and can engage early, but may normalize local risk. A hybrid can define central mandatory objectives while requiring independent peers for high-consequence decisions.

**One-time launch gate versus continuous readiness.** A formal gate creates a clear accountability point. It can also encourage last-minute evidence gathering and decay after launch. Continuous automated controls and periodic review detect drift, but without a decision point unclear ownership may persist. Use both: build readiness during design and delivery, then make an explicit scoped decision.

**Generic baseline versus tailored questions.** A baseline reduces omission and review cost. Excessive uniformity produces irrelevant answers and misses workload-specific harm. Maintain a small curated baseline, then add questions from the actual architecture, user journeys, incidents, and obligations. Retire questions whose objective is enforced elsewhere.

**Self-review versus independent review.** Self-review scales and teaches the owning team. Independence reduces motivated reasoning and supplies unfamiliar failure experience. Match review independence to consequence, novelty, and uncertainty; record who authored, challenged, and accepted each conclusion.

**Evidence depth versus delivery speed.** High-fidelity tests can be expensive or risky. Weak evidence can externalize cost to users and responders. Scale depth to potential harm, uncertainty, reversibility, and exposure. Reduce initial exposure when evidence is necessarily limited, but never use a small cohort to excuse a violation that harms each affected user severely.

**Blocking versus conditional launch.** Blocking creates a clear incentive to fix essential gaps, but overclassification drives concealment and review avoidance. Conditional launch preserves learning and schedule when exposure is bounded. Define blocking criteria before schedule pressure and require real containment, expiry, and acceptance for every condition.

**Documents versus executable policy.** Narrative captures rationale and ambiguity. Automation catches drift consistently. Automated checks can encode obsolete rules or mistake configuration for behavior. Link machine-enforced facts to human-readable objectives, version both, and inspect false positives and false negatives.

**Risk matrix versus quantitative model.** Ordinal matrices are accessible but often hide nonlinear scales and arbitrary cell boundaries. Quantitative estimates expose assumptions but can imply unjustified precision. Use either for prioritization with uncertainty, never as a substitute for mandatory properties or accountable judgment.

## Failure Modes and Misconceptions

1. **“A PRR is a universal checklist.”** A baseline helps, but meaningful questions arise from the reviewed service, change, users, dependencies, incidents, and obligations.
2. **“Every checked box is equivalent evidence.”** A verbal claim, stale document, configuration inspection, controlled test, and production observation establish different things.
3. **“A high score means ready.”** Aggregate scores can hide an absent mandatory control such as authorization, restoration, or survivor capacity.
4. **“No known blocker means ready.”** Missing evidence, undefined scope, or unknown ownership is itself a reason not to assert readiness.
5. **“The review belongs to operations.”** Product, development, data, security, support, and dependency owners contribute properties and evidence; one group cannot manufacture their authority.
6. **“A backup policy proves recoverability.”** Only representative restoration and integrity evidence supports recovery claims.
7. **“A rollback button makes changes reversible.”** Schemas, messages, state, caches, configurations, and external effects may prevent safe rollback.
8. **“Current CPU headroom proves capacity.”** Request mix, latency, memory, queues, downstream quotas, data scale, and failure transitions can be limiting.
9. **“A runbook proves operability.”** A real responder also needs paging, access, training, current commands, dependencies, authority, and recovery verification.
10. **“Redundant components prove resilience.”** Placement, common modes, state, control planes, survivor load, and failback determine the protected property.
11. **“A waiver closes the finding.”** Risk acceptance changes disposition; it does not establish the missing control. Keep residual risk, authority, expiry, and containment visible.
12. **“A small canary makes every risk acceptable.”** Some data loss, privilege failure, safety harm, or irreversible external effect is unacceptable even for one user.
13. **“The decision lasts until the next scheduled review.”** Material changes or invalidated assumptions can reopen it immediately.
14. **“Vendor assessment completion certifies our service.”** External guidance can prompt analysis, but local evidence and authority determine the bounded decision.
15. **“Passing means the service will not fail.”** A PRR reduces known and discoverable risk; it does not guarantee future behavior or eliminate unknown failure modes.

## Worked Examples

### Example 1

**Situation.** A team asks for a PRR of “the new search service.” Reviewers receive a diagram but no launch description.

**Reasoning.** “Search service” could mean shadow traffic, employee-only reads, 5% public traffic, or complete replacement. It could include indexing, autocomplete, ranking, and personalized history or only query serving. Evidence for 500 requests/second in one region cannot decide a global 5,000-request/second launch. The reviewer writes scope as public query serving for anonymous users, one region, 5% traffic, no personalized history, version `7c21`, maximum 600 requests/second, and a seven-day observation window. Indexer replacement and global failover are excluded, with owners and separate decisions.

**Conclusion.** The review becomes decidable only after workload, exposure, version, exclusions, and time are explicit. A favorable decision cannot be generalized beyond them.

### Example 2

**Situation.** A checklist has 49 satisfied items and one failed item: no tested restore for the only copy of customer encryption-key metadata. The scoring rule reports 98%.

**Reasoning.** Loss of this metadata can make otherwise intact customer data unrecoverable. It is a mandatory durability objective, not one interchangeable point. Let its satisfaction value be $s_{restore}=0$. Then the conjunction over mandatory controls is false regardless of the 49 other values. Reviewers create a blocking finding requiring a representative backup, isolated restore, integrity verification, and measured recovery time. Schedule pressure does not change the predicate.

**Conclusion.** The outcome is `not ready`; an average score cannot compensate for a failed mandatory recovery control.

### Example 3

**Situation.** A load test reports acceptable service at 1,250 requests/second. The proposed launch is 1,000 requests/second. The team claims 20% headroom.

**Reasoning.** Arithmetic gives $H=(1250-1000)/1250=0.20$. Inspection shows the test used read-only warm-cache traffic, while launch estimates include 30% writes and cold starts after deployment. It also ran with all zones healthy, but the readiness objective requires one-zone-loss operation. The number is correct for its experiment but not representative of the claim. The PRR asks for the launch request mix, cache transition, dependency quotas, latency criterion, and zone-loss scenario.

**Conclusion.** The existing evidence does not satisfy the capacity objective. Correct arithmetic cannot repair scope mismatch.

### Example 4

**Situation.** A deployment is progressive: 1%, 10%, 50%, then 100%. Automation advances after ten minutes if global error rate is below 1%.

**Reasoning.** At 1%, severe canary errors may be diluted by healthy baseline traffic, and ten quiet minutes may contain too few rare writes. The PRR requires version-labeled SLIs, minimum sample sizes by critical operation, latency and correctness criteria, a maximum observation time, missing-telemetry fail-stop behavior, and an empowered owner. It adds rollback compatibility evidence and prevents advance while the canary population or telemetry is incomplete.

**Conclusion.** Percentage stages alone do not bound risk. Cohort-specific evidence, observation rules, and stop authority make progressive exposure meaningful.

### Example 5

**Situation.** A service lists six replicas across three zones and marks “zone resilience” complete.

**Reasoning.** The dependency graph shows all replicas obtain credentials from one in-zone control endpoint and send writes to a three-voter database whose voters all occupy one zone. Losing that zone removes database quorum and credential refresh. Replica count does not preserve the write property. Reviewers map transitive domains, measure credential lifetime, relocate quorum voters, and require a failure test that includes state correctness, survivor capacity, routing, and failback.

**Conclusion.** Architecture inventory is not resilience evidence. The review follows authority and shared dependencies to the user-visible property.

### Example 6

**Situation.** A backup job reports green every night. The recovery-time objective is four hours and the recovery-point objective is one hour.

**Reasoning.** Job success shows that a process emitted an expected status, not that application state is recoverable. A representative restore takes 3 hours 20 minutes for data transfer, 55 minutes for index rebuilding, and 25 minutes for integrity verification: 4 hours 40 minutes, already beyond the objective. The restored snapshot is 38 minutes old, satisfying the recovery-point objective in this run. The PRR records the time components, environment, data volume, integrity queries, access path, and missing dependency-failure scenarios.

**Conclusion.** RPO evidence passes for the tested run, but measured RTO fails; the green backup status cannot close the recovery objective.

### Example 7

**Situation.** One nonblocking finding remains: support documentation for a new error message is incomplete. The launch affects 2% of internal users for 24 hours.

**Reasoning.** No mandatory control is missing. The condition names an owner, a deadline before external exposure, the exact document and approval needed, user-facing monitoring, an internal help contact, and automatic expiry after 24 hours. The support lead and launch decision maker accept residual confusion risk for this bounded cohort. If exposure expands or the deadline passes, the decision reopens.

**Conclusion.** `Conditional` is defensible because exposure, ownership, verification, acceptance, and expiry are explicit; it is not a polite synonym for unresolved blockers.

### Example 8

**Situation.** A rollback test successfully redeploys the old application binary, so the release objective is marked satisfied.

**Reasoning.** The new version writes a non-null column and emits messages the old consumer cannot parse. After rollback, reads fail on the new rows and queued messages retry indefinitely. Reviewers separate binary rollback from state compatibility. They require expand-contract schema order, dual-readable messages, a tested queue-drain or isolation procedure, configuration rollback, and application-level verification after reversal.

**Conclusion.** A deployment tool's success is insufficient. Rollback evidence must cover persistent state and external effects across the whole transition.

### Example 9

**Situation.** A risk workshop estimates a 2% chance of a dependency outage during the launch window with $300{,}000 estimated impact, and a 20% chance of a documentation defect with $5{,}000 impact.

**Reasoning.** Simple expected exposures are $0.02\times300{,}000=6{,}000$ and $0.20\times5{,}000=1{,}000$. This can prioritize investigation, but the inputs are uncertain and the outage may have a fat-tailed distribution. If the dependency controls authorization, a mandatory security rule may apply regardless of expectation. Reviewers record ranges, correlated causes, containment, and acceptance authority rather than presenting the estimates as precise truth.

**Conclusion.** Quantification exposes assumptions and supports comparison; it does not override hard constraints or eliminate uncertainty.

### Example 10

**Situation.** Three months after approval, traffic doubles, the primary database changes, the on-call team reorganizes, and a severe incident reveals retry amplification. The annual review date has not arrived.

**Reasoning.** Four decision premises changed: load, dependency behavior, operational ownership, and failure knowledge. The prior evidence was bound to the old system. Reopening triggers require immediate reassessment of capacity, failure domains, retry control, paging, runbooks, and launch or steady-state containment. Automated ownership and traffic checks could have surfaced two changes earlier; the incident should create or revise control objectives rather than merely add narrative.

**Conclusion.** Readiness is a time-bounded conclusion. Material change and incident evidence invalidate it before calendar expiry.

## Cross-Program Connections

- [SARCH-009](../../12-software-engineering-software-architecture/modules/009-architecture-decision-records.md) supports durable decision rationale; a PRR adds operational evidence, findings, and launch authority.
- [STQE-010](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) connects quality risks to a portfolio of test evidence rather than one green suite.
- [SEC-050](../../25-security-engineering/ROADMAP.md) develops a hardened service baseline; the PRR records applicable security outcomes without impersonating specialist review.
- [SYSENG-072](../../26-systems-engineering/modules/072-verification-planning.md) connects requirements and verification across the system boundary.
- [API-100](../../28-api-and-service-engineering/modules/100-conducting-a-production-api-and-service-readiness-review.md) applies readiness judgment to API contracts, clients, traffic, dependencies, and operations.
- [PLAT-050](../../29-platform-engineering/modules/050-designing-a-golden-path-that-remains-optional-but-attractive.md) addresses platform-owned defaults and adoption; a service PRR still owns workload-specific evidence and risk.

## References

1. Niall Richard Murphy and Todd Underwood, “The Evolving SRE Engagement Model,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/evolving-sre-engagement-model/). Accessed 2026-09-06.
2. Jennifer Petoff, Niall Richard Murphy, Betsy Beyer, and Chris Jones, “Reliable Product Launches at Scale,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/reliable-product-launches/). Accessed 2026-09-06.
3. Google, “Launch Coordination Checklist,” Appendix E in *Site Reliability Engineering: How Google Runs Production Systems*, identified by the publisher as Google's circa-2005 checklist, published online 2017. [Official online edition](https://sre.google/sre-book/launch-checklist/). Accessed 2026-09-06.
4. Amazon Web Services, “The ORR Tool,” *Operational Readiness Reviews*, AWS Well-Architected Framework, current online edition. [Official documentation](https://docs.aws.amazon.com/wellarchitected/latest/operational-readiness-reviews/the-orr-tool.html). Accessed 2026-09-06.
5. Amazon Web Services, “OPS 7: How Do You Know That You Are Ready to Support a Workload?” *AWS Well-Architected Framework*, current online edition. [Official documentation](https://docs.aws.amazon.com/wellarchitected/latest/framework/ops-07.html). Accessed 2026-09-06.
6. Microsoft, “Architecture Strategies for Testing,” *Azure Well-Architected Framework: Operational Excellence*, current online edition. [Official documentation](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/testing). Accessed 2026-09-06.

Current vendor claims are source-specific and were checked on 2026-09-06. The review model, thresholds, risk values, capacity figures, and decisions in this chapter are educational examples, not universal gates, certification criteria, or production guarantees.

## Exercises

### Exercise 1

Distinguish a control objective, control mechanism, claim, evidence item, finding, blocker, condition, and readiness decision for a service that must restore customer records after data loss.

### Exercise 2

A service has measured healthy capacity of 2,400 requests/second and one-zone-loss capacity of 1,500 requests/second. Declared launch load is 1,200 requests/second, with a possible 25% launch spike. Compute nominal headroom in both states before and during the spike. State why the arithmetic cannot alone approve launch.

### Exercise 3

Review this evidence statement: “Rollback tested successfully last quarter; see dashboard screenshot.” Diagnose its evidence defects and rewrite it with sufficient identity, environment, procedure, behavior, provenance, freshness, and limitations.

### Exercise 4

Design a PRR outcome for a launch with two findings: an untested restore for regulated records and missing support documentation. Define classification, ownership, closure evidence, decision, rollout containment, and reopening rules.

### Exercise 5

A service approved six months ago has unchanged application code but a new identity provider, twice the reviewed traffic, a different on-call vendor, and a newly discovered dependency retry storm. Decide which evidence can remain, which objectives must reopen, and how to construct a proportionate re-review.

## Answers to the Exercises

### Answer 1

The control objective is “customer records can be restored within declared recovery-time and recovery-point limits with application-level integrity.” Mechanisms include versioned backups, independent storage, access paths, restore automation, and integrity queries. The claim is that those mechanisms meet the objective for the scoped data volume and failure. Evidence is a dated restore of named artifact and data versions in a representative isolated environment, with commands, duration, recovered point, integrity results, owner, and limitations. A failed integrity query creates a finding. It is a blocker when policy forbids launch without recoverability. It could be a condition only if authoritative policy permits bounded exposure and all containment, ownership, expiry, and acceptance requirements hold. The readiness decision integrates this result with every other mandatory objective; it never follows merely from the existence of backup configuration.

### Answer 2

Normal headroom is $(2400-1200)/2400=0.50$, or 50%. One-zone-loss headroom is $(1500-1200)/1500=0.20$, or 20%. A 25% spike raises load to $1200\times1.25=1500$ requests/second. Healthy headroom then is $(2400-1500)/2400=0.375$, or 37.5%; one-zone-loss headroom is zero. The calculation assumes the measured request mix, latency and error criteria, data scale, cache state, dependency limits, routing, and capacity remain representative. Zero survivor margin leaves no modeled room for forecast error or transition overhead. Reviewers need failure-mode load evidence, downstream capacity, overload behavior, and a bounded rollout decision rather than arithmetic alone.

### Answer 3

The statement lacks artifact and configuration identity, test date, environment, procedure, data and schema state, operator, expected criteria, actual outputs, and limitations; “last quarter” is ambiguous and a screenshot is not reproducible. A stronger statement is: “On 2026-08-28, engineer A rolled deployment `service@abc123` back to `service@def456` in staging clone `stg-restore-17` using runbook revision 8 after applying schema migration 42. The command log and deployment events show completion in 6m12s; contract queries Q1–Q18 and message compatibility fixtures all passed. The test used 12% of production data volume, warm caches, and no third-party timeout, so it does not establish production-scale duration or behavior during provider failure.” The PRR then judges whether those limits fit the scoped claim.

### Answer 4

Untested restoration of regulated records is a blocking finding because a mandatory recovery and compliance objective lacks evidence. Name the data-system owner, require an isolated representative restore, application-level integrity checks, measured RTO/RPO, and compliance-owner review before closure. Missing support documentation can be a nonblocking condition only if exposure is otherwise safe: name the support owner, exact document, approval, due date, user-contact fallback, and expiry. The decision remains `not ready` while the restore blocker is open; a small rollout does not erase per-user data risk. After verified closure, the decision may become `conditional` for a bounded internal cohort until support evidence closes. Any expansion, missed deadline, recovery-system change, or failed post-launch criterion reopens the decision.

### Answer 5

Unchanged application-unit behavior may remain supporting evidence if artifact, configuration, and dependency assumptions still match, but it must be reviewed for transfer rather than accepted automatically. Identity, authorization, secret rotation, outage posture, and audit evidence must reopen because the authority dependency changed. Capacity, overload, queue, latency, SLO, and dependency-quota evidence must reopen at twice the traffic. Paging delivery, access, staffing, training, escalation, incident command, and runbook execution must reopen for the new vendor. Retry, timeout, backpressure, degradation, and dependency-protection objectives must reopen because the newly observed storm contradicts prior assumptions. Use the old PRR as an indexed baseline, mark unaffected evidence with a transfer rationale, focus new tests on changed boundaries and interactions, rerun mandatory gates, and issue a new scoped decision with expiry. Do not rewrite every document merely to make the review look new.
