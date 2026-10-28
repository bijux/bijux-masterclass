---
module_id: PLAT-093
program: Platform Engineering
level: 2
module_number: 93
title: Migration to the Platform
status: complete
last_verified: 2026-09-02
---

# Migration to the Platform

## One-Page Review

### Governing question

How should an organization move service outcomes, data, traffic, identities, operational responsibility, and developer workflows onto an internal platform while preserving continuity, autonomy, evidence, reversibility, and the option not to migrate when platform fit is poor?

### Essential definitions

- A **migration** transfers an owned service capability and its operational responsibility from a source operating model to a target platform contract; moving compute alone is relocation.
- A **migration unit** is the smallest dependency-coherent set of service, data, traffic, identity, jobs, integrations, controls and owners that can safely change together.
- A **target contract** states platform capabilities, interfaces, constraints, ownership, SLOs, support, evidence, cost, extension and exit behavior required after migration.
- **readiness** is verified ability of the workload, platform and people to enter a migration step under declared gates.
- A **wave** is a bounded group of compatible migration units scheduled together because dependency, risk, learning and support capacity justify shared execution.
- **coexistence** is the governed period during which source and target both participate, with explicit authority, synchronization, observability and cost rules.
- A **cutover** transfers traffic, writes, scheduled work, integrations or operational authority to the target under a state machine.
- A **fallback** returns defined authority to a still-valid source; **roll-forward** repairs the target while preserving its authority; neither is a vague promise to “roll back.”
- **stabilization** is the post-cutover interval in which target outcomes, operations, cost and support are observed before source retirement.
- **decommissioning** removes source traffic, writes, credentials, data, routes, jobs, alerts, contracts and resources after retention and recovery obligations are satisfied.

### Central model, mechanism, or theorem

For migration unit $u$ and gate $g$, readiness is conjunctive:

$$
Ready(u,g)=Fit_u\land Inventory_u\land Dependency_u\land Target_u\land Data_u
\land Security_u\land Operability_u\land People_u\land Capacity_g\land Evidence_u.
$$

A unit enters a wave only when every mandatory predicate is true or a named exception has owner, expiry and compensating control. During coexistence, each mutable resource has exactly one authoritative writer or a proven conflict protocol. Cutover advances only when entry conditions, outcome checks, data bounds and support capacity pass; fallback remains possible only while source validity and reverse synchronization are preserved.

### Critical invariants

- Migration is justified by named user and organizational outcomes; a deadline, license event or mandate may constrain timing but cannot substitute for fit and risk evidence.
- Inventory covers runtime, data, traffic, identity, trust, delivery, observability, schedules, integrations, cost, people and recovery dependencies with current owners.
- Every mutable datum, request route, job and control action has one declared authority at each coexistence state; dual write requires explicit idempotency and conflict semantics.
- Wave membership respects dependency closure, platform and support capacity, correlated risk, representative learning and bounded blast radius.
- Cutover and fallback are fenced, observable, rehearsed state machines with quantitative stop conditions; emergency improvisation is not the primary recovery design.
- Source retirement occurs only after stabilization, business/technical approval, recovery and retention evidence, dependency removal, credential revocation and residual-cost reconciliation.

### Common failures

Migrating because the platform exists; counting servers instead of service outcomes; stale CMDB inventory; missing batch, DNS, certificates, webhooks or incident access; putting tightly coupled units in different waves; early waves chosen only because they are trivial; forced modernization during cutover; platform capacity sized for steady state but not coexistence; unversioned target contracts; dual writes without conflict rules; DNS change called a rollback plan; irreversible schema migration before confidence; teams losing source expertise too early; platform support overloaded by simultaneous waves; success declared at traffic switch; and source systems left running indefinitely with live credentials and cost.

### Compact example

A payments service will move from team-managed clusters to a regional platform. Discovery identifies the API, database, settlement job, webhook callbacks, KMS keys, certificates, audit export, fraud dependency, DNS, dashboards, on-call access and recovery runbooks as one migration unit. Fit analysis chooses replatforming rather than rewriting business logic. The target contract is tested with a production-like shadow, immutable artifacts, workload identity, quota, SLOs, restore and exit. Data replicates source-to-target under measured lag; writes remain source-authoritative. A small read cohort moves first, then a fenced maintenance window drains requests, stops jobs, verifies zero lag, promotes target writer authority and gradually shifts traffic. Stop thresholds cover correctness, payment duplication, latency, error budget, backlog and support load. The source remains intact but read-only during stabilization. Only after two settlement cycles, restore evidence, owner approval and dependency scans does the team revoke credentials, archive required data, remove routes and alerts, cancel capacity and close residual costs.

### Connections

Migration consumes SLOs, inventories, dependency maps, upgrades, restore evidence, incident response, regional design, costs, blast-radius review, discovery and adoption cohorts from PLAT-081–092. It creates operating evidence for support, roadmaps, capability retirement, outcome measurement, strategy defense, autonomy and anti-monopoly governance in PLAT-094–100.

## Governing Question

Which services should move to the platform, in what dependency-coherent sequence, through which reversible authority transitions, and what evidence proves both the target outcome and safe retirement of the source?

Migration is a sociotechnical change. Interfaces, infrastructure and data move, but so do decisions, expertise, budgets, incident roles, risk ownership and daily habits. Ignoring any of these creates an apparently finished technical move with hidden operational dependence.

The platform is not automatically the correct target. Some workloads need capabilities, isolation, latency, hardware, jurisdiction or lifecycle economics outside its contract. A durable program makes retain, retire, replace and exception decisions explicit.

## Why This Matters

Internal platform value is realized only when real services can adopt safely. Greenfield demonstrations do not prove that stateful, regulated, interconnected or high-traffic systems can transfer responsibility.

Migration concentrates risk at transitions. Source and target may both exist, but data authority, queues, caches, DNS, credentials and operators can disagree. Redundancy without a control model creates duplication or loss.

Portfolio pressure can overwhelm the target. Many individually safe waves can exhaust quotas, platform on-call, enabling teams, network capacity, registry throughput or change windows when combined.

Finishing matters. Permanent coexistence doubles cost and attack surface, while premature decommissioning destroys fallback, evidence or legally required data. Stabilization and retirement need separate gates.

## Prerequisites and Retrieval

Retrieve platform strategy and target contract; application/service catalog; business owners and critical journeys; SLOs and error budgets; runtime, network, data, identity, trust, delivery, schedule and integration inventories; dependency graph; traffic and capacity profiles; data classification, retention and legal hold; security/threat assessment; backups and restore results; incident history; cost and licensing; team skills and operating model; adoption research; exceptions; target quotas; support capacity; maintenance calendar; and source decommission policy.

Distinguish application from service outcome; asset from dependency; workload from migration unit; eligibility from readiness; rehost from replatform and refactor; modernization from migration; wave from arbitrary batch; shadow from authoritative production; replication from validated consistency; dual run from dual write; traffic shift from authority transfer; rollback from fallback; fallback from disaster recovery; cutover success from stabilization; source shutdown from complete decommissioning; adoption mandate from product fit; and migrated count from realized value.

## Learning Objectives

After completing this module, you should be able to:

1. derive migration goals, exclusions and success measures from platform and service outcomes;
2. discover migration units and dependency closure across technical, operational and organizational systems;
3. choose retain, retire, replace, rehost, replatform, refactor or rebuild strategies by evidence;
4. define and test a versioned target platform contract before production transfer;
5. score readiness without hiding mandatory blockers inside an average;
6. plan waves using dependency, risk, representativeness, target capacity and support constraints;
7. design data, traffic, identity, job and control coexistence with unambiguous authority;
8. execute canary, cutover, fallback and roll-forward through fenced state machines;
9. validate user, service, security, operational, cost and developer outcomes through stabilization; and
10. decommission source systems with approval, retention, recovery, dependency and residual-cost evidence.

## Core Exposition

### Establish outcomes and authority

State why migration is being considered: improved delivery, security, reliability, developer independence, compliance, supportability, cost or source end-of-life. Define baselines and target outcomes.

Name decision authority for product, service risk, data, security, platform readiness, cutover and decommissioning. No single migration office should silently accept every domain’s residual risk.

Declare non-goals. Modernizing business architecture, changing databases and redesigning APIs during one cutover may exceed the safe change budget.

### Discover the real estate

Combine automated discovery with owner workshops, runtime traces, DNS, certificates, identity/audit, database connections, queues, scheduled jobs, billing, repositories and incident records.

Record confidence and observation date. An inventory item with no owner or telemetry is a migration risk, not evidence of absence.

Include cold paths: restore, failover, certificate rotation, month-end, key renewal, legal export, emergency access and vendor support.

### Form dependency-coherent units

Create a typed graph of runtime, data, traffic, identity, trust, delivery, operational, organizational and recovery dependencies. Identify strongly coupled components and shared cut sets.

A migration unit should transfer without leaving unsafe synchronous or authority edges across the boundary. It can contain several services or one partition of a larger service.

Record dependencies that will remain cross-boundary during coexistence, their latency, failure behavior, version contract, ownership and retirement condition.

### Decide whether and how to migrate

Evaluate retain, retire, replace, rehost, replatform, refactor and rebuild. Use business value, platform fit, source risk, change tolerance, time, skills, reversibility and total lifecycle cost.

Rehost can meet an urgent exit but may preserve toil. Replatform changes integration while limiting business-code change. Refactoring can unlock platform value but increases verification scope.

Do not force poor-fit services into a golden path. A governed exception with explicit owner and revisit date is more honest than an unsupported target deployment.

### Define the target contract

Specify identity, network, compute, storage, data, deployment, policy, observability, backup, recovery, SLO, quota, cost, support, extension and exit behavior.

Map source assumptions to target semantics. Local disk, static IP, privileged runtime, mutable hosts, long transactions, implicit trust and manual approvals need explicit treatment.

Version the contract and freeze material target changes during a wave unless emergency procedure and revalidation apply.

### Build the target foundation

Provision tenant/cell identity, network routes, DNS, certificates, keys, policy, quotas, artifact access, logs, metrics, traces, audit, backup and incident access through governed automation.

Verify platform capacity for source replication, shadow traffic, caches, cutover peaks, failback and concurrent waves—not only target steady state.

Test target isolation and blast radius. Migration must not merge risk domains merely to simplify onboarding.

### Assess readiness conjunctively

Use gates rather than one average score. Mandatory data-integrity, security, rollback or owner readiness cannot be offset by excellent documentation.

For each failed predicate, record remediation, owner, due date, evidence and consequence. Time-bound exceptions need compensating controls and expiry.

Assess the platform and migration organization as well as the workload. A ready application cannot migrate into an exhausted or unsupported platform.

### Design representative early moves

Begin with bounded units that teach real lessons: some state, integration, compliance and operational need, while keeping consequence recoverable.

Migrating only disposable stateless demos optimizes reported success but leaves the hardest assumptions untested. Migrating the most critical service first creates excessive risk.

Choose control units that remain on the source so outcome comparisons can identify target-specific regressions.

### Plan waves

Group by dependency closure, business calendar, risk, target pattern, data method, geography and owner availability. Limit correlated consequence and concurrent support demand.

Publish entry, exit, stop and learning criteria. Later waves should incorporate evidence; cloning a flawed runbook scales defects.

Maintain a rolling plan rather than assigning precise dates to unknown distant work. Protect capacity for remediation and support.

### Prepare people and operations

Define who builds, approves, observes, responds, owns and supports before, during and after cutover. Update escalation and incident roles.

Use pairing and rehearsal to transfer knowledge. Documentation handoff alone does not create operational competence.

Plan heightened support and a clear end to it. Permanent migration specialists can hide a platform that never becomes self-service.

### Establish coexistence states

Define states such as source-only, target-shadow, target-read, synchronized, cutover-ready, target-authoritative, fallback-eligible, stabilized and source-retired.

For each state, declare writers, readers, job scheduler, event producer, traffic owner, data sync direction, credential scope and allowed transitions.

Fence obsolete actors with epochs, leases or revoked credentials. A diagram arrow does not stop a source job from issuing duplicate effects.

### Migrate data safely

Inventory tables, objects, streams, caches, indexes, history, keys, retention and downstream consumers. Select bulk copy, change capture, logical replication, export/import or application-mediated migration.

Validate counts, checksums, constraints, sampled semantics, ordering, lag and business invariants. Equal row counts do not prove equivalent meaning.

Define writes during cutover. Pause, single-write with replication, dual-write with idempotency/conflict resolution, or partitioned authority have different proof obligations.

### Validate shadow and preproduction behavior

Replay sanitized representative traffic or mirror reads without causing external effects. Compare correctness, performance, security decisions and resource behavior.

Test peak, failure, dependency loss, restore, rotation, scaling and incident access. Happy-path conformance is insufficient.

Account for shadow cost and privacy. Mirrored personal data or duplicate webhook effects can create harm.

### Rehearse cutover and fallback

Run the exact state machine in a representative environment, including operator access, stop thresholds, fallback and cleanup. Time every step.

Precompute target sets and commands; use peer verification for irreversible actions. Confirm communications, ownership and vendor availability.

Prove fallback feasibility under current schema and data direction. If reverse sync is unavailable after promotion, define the roll-forward boundary explicitly.

### Execute progressively

Freeze conflicting changes for the shortest justified interval. Verify inventories, replication, capacity, backups, clocks, credentials and owners immediately before entry.

Move a canary cohort or read traffic where semantics permit. Compare target with control on user journey, correctness, latency, errors, saturation and security.

Advance only through declared gates. Time pressure does not convert a failed data or safety predicate into success.

### Transfer authority

Drain or fence source writers, reach the declared replication point, verify invariants, promote target authority and then shift dependent jobs and traffic in a controlled order.

DNS is one routing layer, not proof of convergence. Account for caches, long connections, queues, webhooks, batch jobs and clients with pinned endpoints.

Keep the transition idempotent and auditable. Re-running a step must not duplicate payment, notification or data mutation.

### Decide fallback or roll-forward

Use quantitative thresholds for correctness, loss, latency, saturation, backlog, security, data lag and recovery time. Include qualitative business-owner gates for critical semantics.

Fallback only if source validity, data reconciliation and external-effect handling remain proven. Otherwise stop new work, contain impact and roll forward under incident command.

Record the decision and authority epoch; do not let separate teams independently reverse traffic and data.

### Stabilize outcomes

Observe at least representative traffic cycles, scheduled jobs, backup, restore sampling, rotations, deployment, incident drills, cost close and support behavior.

Measure against baselines and target claims: user outcomes, SLOs, security, delivery, developer independence, support, toil and unit cost.

Close migration defects or assign durable product ownership. A temporary bridge without removal criteria becomes architecture.

### Decommission completely

Obtain business, technical, data, security and operations approval. Preserve archives, legal holds and recovery artifacts under named retention.

Remove source routes, writes, jobs, replication, credentials, keys, firewall rules, agents, monitors, backups, licenses, contracts and resources in recoverable order.

Scan for residual traffic, cost and dependencies; update catalogs, diagrams, runbooks, ownership and audits. Verify deletion or archive retrieval as required.

### Learn across the portfolio

After each wave, compare plan with actual effort, defects, support, target gaps, cutover time, fallback readiness and outcomes. Update patterns and estimates.

Keep workload-specific facts separate from reusable platform improvements. One service’s exception should not silently become the default abstraction.

Stop or redirect the program when evidence shows poor fit or transferred harm. Migration count is not the final outcome.

## Definitions and Notation

Let $U$ be migration units, $D$ typed dependencies, $G$ readiness gates, $W$ waves, and $Q$ platform/support capacity dimensions. For unit $u$, mandatory readiness is

$$
R(u)=\bigwedge_{g\in G_u} pass(u,g).
$$

An average readiness score may aid triage but cannot replace $R(u)$. A wave $w\subseteq U$ is admissible only if required dependency closure is satisfied and

$$
\sum_{u\in w} demand(u,q)\le capacity(w,q)\quad\forall q\in Q.
$$

Let migration state $z\in\{source,shadow,synchronized,target,fallback,stable,retired\}$. For mutable resource $r$, $Authority(r,z)$ names exactly one writer unless a documented conflict protocol $P_r$ is active.

Let $B_o$ and $T_o$ be baseline and target measurements for outcome $o$, with guardrail set $H$. Completion requires target evidence under representative operation, all $h\in H$ within bounds, and retirement predicates satisfied. “Moved” is not a mathematical synonym for “improved.”

## Mechanisms, Invariants, or Proof Structure

### Twelve-step migration mechanism

1. Define outcomes, authority, non-goals, baselines and platform-fit decision.
2. Discover assets, dependencies, owners, data, operations, costs and cold paths.
3. Form dependency-coherent migration units and choose a strategy for each.
4. Define, version and test the target platform contract and exit path.
5. Gate workload, platform, people, capacity, security and recovery readiness.
6. Plan representative, dependency-aware waves with bounded support and blast radius.
7. Establish coexistence states, authority, synchronization and fencing.
8. Rehearse data movement, traffic, jobs, cutover, stop and fallback end to end.
9. Execute a canary and advance only on user, system, data and security evidence.
10. Transfer authority atomically enough for the business semantics and stabilize.
11. Decommission source dependencies, credentials, data and cost after approval.
12. Reconcile outcomes and learning into the platform, portfolio and remaining waves.

### Outcome and fit invariant

Every unit has a justified target outcome, supported platform contract and permitted retain/exception alternative; migration volume cannot substitute for value.

### Inventory and dependency invariant

Runtime, data, traffic, identity, delivery, observation, schedule, organization and recovery edges have owners and freshness; unknown edges remain explicit risk.

### Readiness and capacity invariant

Mandatory gates are conjunctive, exceptions expire, and combined wave demand stays within target, enabling and support capacity under migration and failure load.

### Authority invariant

Every mutable resource, route, job and external effect has declared authority in each coexistence state, with fencing and conflict behavior verified.

### Transition invariant

Cutover, fallback and roll-forward have authenticated state, entry/exit conditions, stop thresholds, idempotency, audit and one incident decision authority.

### Completion invariant

Completion requires representative stabilization outcomes plus approved, retention-safe removal of source dependencies, authority, credentials and residual cost.

### Proof sketch: asset relocation cannot prove migration completion

Construct two services whose compute and traffic both run on the target platform. Service A also transfers data authority, scheduled jobs, identity, observability, incident ownership and recovery, then retires the source. Service B retains its writer, settlement job, administrator credentials and restore path on the source. Target asset counts are identical, but B cannot operate or recover independently and still carries source risk. Therefore target asset presence alone cannot prove migration completion.

### Executable readiness and wave audit

The synthetic audit applies conjunctive gates to six candidate services, then checks a three-unit wave against platform and support capacity. It demonstrates gate arithmetic; it does not validate a real migration.

<!-- bijux-verify: {"id":"migration-readiness-wave-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"services=6\nready=3\nconditional=2\nblocked=1\nselected=3\nplatform_units=9/10\nsupport_units=6/7\nwave_gate=pass\n"}} -->
```python
services = {
    "alpha": ("ready", 3, 2),
    "beta": ("ready", 4, 2),
    "gamma": ("ready", 2, 2),
    "delta": ("conditional", 2, 1),
    "epsilon": ("conditional", 3, 3),
    "zeta": ("blocked", 5, 4),
}
selected = ["alpha", "beta", "gamma"]
platform = sum(services[name][1] for name in selected)
support = sum(services[name][2] for name in selected)
states = [value[0] for value in services.values()]

print(f"services={len(services)}")
for state in ("ready", "conditional", "blocked"):
    print(f"{state}={states.count(state)}")
print(f"selected={len(selected)}")
print(f"platform_units={platform}/10")
print(f"support_units={support}/7")
gate = all(services[name][0] == "ready" for name in selected) and platform <= 10 and support <= 7
print(f"wave_gate={'pass' if gate else 'fail'}")
```

### Verification strategy

Reconcile discovery with runtime, network, identity, billing and owner evidence; test target contracts; trace dependency closure; recompute readiness predicates and wave capacity; verify backups and target restore; compare replicated data by structural and business invariants; rehearse cutover/fallback; run canary controls; audit authority epochs; observe stabilization cycles; scan residual traffic and cost; verify credential revocation and archive retrieval; and compare outcomes with baselines.

## Alternatives and Trade-Offs

1. Rehosting exits the source quickly but preserves operational assumptions and toil.
2. Replatforming captures shared capabilities with moderate change but exposes semantic mismatches.
3. Refactoring improves target fit but expands code, data and verification risk.
4. Rebuilding removes legacy constraints but delays value and risks lost behavior.
5. Replacing with a managed product reduces ownership but adds vendor and data-exit dependence.
6. Retaining avoids unjustified change but continues source risk and cost.
7. Large migration units reduce cross-boundary dependencies but increase cutover consequence.
8. Small units bound change but create more coexistence edges and sequencing.
9. Homogeneous waves improve repeatability but can repeat the same hidden defect.
10. Representative waves learn more but require stronger containment and support.
11. Offline migration simplifies authority but imposes downtime.
12. Online replication reduces downtime but adds lag, fencing and reconciliation complexity.
13. Dual write enables gradual transfer but requires idempotency and conflict semantics.
14. Source-authoritative coexistence is clear but limits target-only testing.
15. Automated cutover is repeatable but can propagate a bad state quickly.
16. Manual gates add judgment but introduce delay and operator variance.
17. Long stabilization improves confidence but prolongs duplicate cost and attack surface.
18. Rapid decommission saves cost but shortens fallback and evidence windows.

## Failure Modes and Misconceptions

1. “Everything should migrate” ignores fit, retirement and governed exceptions.
2. “A hard deadline is a readiness gate” confuses constraint with evidence.
3. “CMDB completeness is sufficient” ignores runtime and cold-path discovery.
4. “One application is one migration unit” ignores shared data and integrations.
5. “Few dependencies means low risk” ignores criticality and unknown edges.
6. “A readiness average can offset security failure” violates conjunctive gates.
7. “The workload is ready, so migration is ready” omits platform and people capacity.
8. “Trivial first waves prove the factory” test little representative behavior.
9. “Migrate the hardest first” spends learning budget at maximum consequence.
10. “Modernize everything during movement” expands simultaneous change unnecessarily.
11. “The target contract is whatever exists” removes explicit fitness and ownership.
12. “Steady-state capacity covers migration” ignores replication, shadow and recovery load.
13. “Dual run means safe fallback” ignores data divergence and external effects.
14. “Dual write is redundancy” ignores ordering, duplication and conflict.
15. “Equal row counts prove data integrity” ignores meaning and constraints.
16. “Shadow traffic is harmless” can leak data or duplicate side effects.
17. “DNS cutover is instantaneous” ignores caching and long-lived connections.
18. “Traffic shift transfers write authority” confuses routing with data control.
19. “Rollback is always possible” fails after incompatible schema or target-only writes.
20. “A runbook proves rehearsal” substitutes prose for observed execution.
21. “Canary success proves full-scale capacity” ignores scale and tenant diversity.
22. “Time pressure justifies bypassing stop gates” converts schedule risk into outage risk.
23. “Platform on-call can absorb every wave” ignores portfolio support concurrency.
24. “Training documents transfer expertise” omits practice and incident access.
25. “Cutover means completion” omits stabilization and source retirement.
26. “Keeping source forever is safer” accumulates cost, ambiguity and attack surface.
27. “Turning off compute decommissions the source” leaves data, credentials and routes.
28. “No source traffic means no dependencies” ignores recovery and scheduled paths.
29. “Migration count measures value” rewards motion rather than outcomes.
30. “A successful pattern fits every service” turns one wave’s learning into dogma.

## Worked Examples

### Example 1

Discovery finds a nightly settlement job absent from the service catalog. The API and job become one migration unit because separate authority would duplicate payments.

### Example 2

A legacy service cannot use workload identity before a vendor upgrade. The unit remains conditional with an expiring exception proposal rather than passing on an average score.

### Example 3

Three ready services individually fit platform capacity, but their combined shadow and support demand exceeds the wave limit. One moves to the next wave.

### Example 4

A team rehosts before a data-center exit, stabilizes, then schedules replatforming separately. The program avoids combining urgent relocation with architectural redesign.

### Example 5

Mirrored requests would send duplicate emails. The shadow adapter suppresses external effects and compares generated intent instead.

### Example 6

Replication shows zero lag but a business invariant detects missing closed accounts. Cutover stops because transport health does not prove semantic completeness.

### Example 7

A canary cohort passes median latency but fails the regulated tenant audit export. Segment-specific gates prevent rollout.

### Example 8

After target promotion, reverse replication is unavailable. The state machine marks fallback closed and shifts incident strategy to contain-and-roll-forward.

### Example 9

Thirty days after cutover, source DNS receives certificate-renewal traffic from an old agent. Decommissioning pauses until the hidden dependency is removed.

### Example 10

Migration improves deployment time but triples platform support effort. The outcome review funds missing self-service diagnostics before the next wave.

## Cross-Program Connections

- Systems Engineering contributes boundary, lifecycle, hazard, transition and verification reasoning.
- Software Architecture contributes dependency decomposition, strangling, compatibility and target contracts.
- Distributed Systems contributes replication, authority, fencing, idempotency and partial failure.
- Data Engineering contributes discovery, change capture, validation, reconciliation and retention.
- Cloud Engineering contributes landing zones, quotas, wave patterns, networking and cost.
- Security Engineering contributes identity migration, threat boundaries, key custody and revocation.
- Site Reliability Engineering contributes SLOs, canaries, incident command, recovery and stabilization.
- API and Service Engineering contributes compatibility, traffic transition, clients and external effects.
- Engineering Management contributes portfolio sequencing, ownership, skills, communication and risk acceptance.
- Finance and Governance contribute contracts, licenses, residual cost, legal hold and retirement approval.

## References

1. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/). Retrieved 2026-09-02.
2. DORA. [Platform Engineering](https://dora.dev/capabilities/platform-engineering/). Retrieved 2026-09-02.
3. Google Cloud. [What Is an Internal Developer Platform?](https://cloud.google.com/discover/what-is-an-internal-developer-platform). Retrieved 2026-09-02.
4. Google Cloud. [Migrate to Google Cloud: Get Started](https://cloud.google.com/architecture/migration-to-gcp-getting-started). Retrieved 2026-09-02.
5. Google Cloud. [Assess and Discover Your Workloads](https://cloud.google.com/architecture/migration-to-gcp-assessing-and-discovering-your-workloads). Retrieved 2026-09-02.
6. Google Cloud. [Plan and Build Your Foundation](https://cloud.google.com/architecture/migration-to-google-cloud-building-your-foundation). Retrieved 2026-09-02.
7. Google Cloud Migration Center. [Migration Planning Overview](https://cloud.google.com/migration-center/docs/migration-planning-overview). Retrieved 2026-09-02.
8. AWS Prescriptive Guidance. [Wave Planning](https://docs.aws.amazon.com/prescriptive-guidance/latest/application-portfolio-assessment-guide/wave-planning.html). Retrieved 2026-09-02.
9. AWS Prescriptive Guidance. [Migration Strategies](https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html). Retrieved 2026-09-02.
10. AWS Prescriptive Guidance. [Best Practices for Migration Cutover](https://docs.aws.amazon.com/prescriptive-guidance/latest/best-practices-migration-cutover/introduction.html). Retrieved 2026-09-02.
11. Microsoft. [Migration Wave Planning](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/migrate/migration-wave-planning). Retrieved 2026-09-02.
12. Microsoft. [Execute Migration to Cloud](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/migrate/execute-migration). Retrieved 2026-09-02.
13. Microsoft. [Decommission Source Workloads](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/migrate/decommission-source-workload). Retrieved 2026-09-02.
14. Google SRE. [Canarying Releases](https://sre.google/workbook/canarying-releases/). Retrieved 2026-09-02.
15. Google SRE. [Reliable Product Launches at Scale](https://sre.google/sre-book/reliable-product-launches/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

A portfolio has fifty services but incomplete ownership and dependency records. Design discovery evidence and criteria for forming migration units without claiming completeness prematurely.

### Exercise 2

A service passes eight of ten readiness gates but fails restore and target incident-access tests. Explain why a weighted 80% score is unsafe and define remediation evidence.

### Exercise 3

Design coexistence and cutover states for a service with a database, queue consumer, daily billing job and webhook side effects. Make authority explicit.

### Exercise 4

Three migration units demand platform/support capacity of $(4,2)$, $(3,3)$ and $(5,2)$ while a wave has limits $(10,6)$. Determine admissible combinations and discuss why capacity arithmetic is insufficient.

### Exercise 5

Traffic has run on the target for 30 days with good SLOs, but source backups, credentials, DNS records and a monthly job remain. Write the completion decision.

## Answers to the Exercises

### Answer 1

Combine catalog/CMDB data with runtime traces, network flows, DNS, certificates, identity/audit, repository/deployment, database, queue, scheduler, billing and incident evidence. Record owner, source, observation time and confidence for every node and edge. Run owner workshops and exercise cold paths such as restore and rotation.

Group strongly coupled data, synchronous, job and external-effect components whose authority must move together. Keep unknown-owner and unobserved regions as explicit risks; select only bounded early units whose missing-edge consequence is tolerable and verify discovery during rehearsal.

### Answer 2

Restore and incident access are mandatory survival properties. Averaging lets documentation or low-consequence checks numerically cancel an inability to recover or operate, which is not a valid implication.

Keep the unit blocked. Produce a successful isolated target restore with data/business invariant checks and measured RTO/RPO, plus an incident exercise proving independent identity, telemetry, permissions and escalation. Record artifacts, dates and owners; reassess platform capacity and invalidate the evidence when recovery dependencies change.

### Answer 3

Use source-only; target-shadow with no side effects; synchronized with source as sole database writer, source billing scheduler and source queue consumer; cutover-ready after drain and zero bounded lag; target-authoritative after writer epoch promotion; fallback-eligible while reverse reconciliation remains valid; stable; then retired.

Fence the old database writer, scheduler and queue consumer before enabling target counterparts. Give webhooks idempotency keys and an outbox tied to the authoritative epoch. Move queue ownership and job checkpoints explicitly; traffic routing alone cannot transfer them. Audit every transition and close fallback when target-only writes cannot safely return.

### Answer 4

Pairs one-plus-two demand $(7,5)$ and one-plus-three $(9,4)$ and pass. Two-plus-three demand $(8,5)$ and pass. All three demand $(12,7)$ and fail both limits. Each singleton passes.

Arithmetic is necessary but insufficient: dependency closure, correlated risk, timing, tenant consequence, platform quotas, data method, operator availability, business calendar and failure/recovery load can reject an otherwise admissible combination. Capacity estimates also require confidence and headroom.

### Answer 5

Do not declare completion. The target has passed one stabilization dimension, but the source still owns recovery artifacts, active credentials, routing and scheduled behavior. The monthly job has not completed a representative cycle.

Keep the source in controlled stabilization: identify and migrate or retire the job, test target backup/restore, satisfy retention/legal hold, remove stale DNS, revoke credentials, scan dependencies and residual traffic, obtain business/data/security/operations approval, then remove resources and reconcile licenses/cost. Record the target outcomes and final archive/deletion evidence before marking the unit complete.
