---
module_id: SARCH-011
program: Software Engineering: Software Architecture
level: 1
module_number: 11
title: Availability and Recovery Tactics
status: complete
last_verified: 2026-09-05
---

# Availability and Recovery Tactics

## One-Page Review

### Governing question

How should architecture detect, contain, recover from, and learn about failures so a defined capability remains acceptably usable and accepted work remains correct?

### Essential definitions

- **availability** is the degree to which a capability is usable when required under stated conditions; it is not merely process uptime.
- A **failure** is externally observable deviation from required service; a **fault** is a hypothesized or observed cause capable of producing failure.
- **fault tolerance** is the ability to continue acceptable service despite specified faults.
- **resilience** is the ability to prepare for, absorb, recover from, and adapt to disruption within defined objectives.
- **recovery time objective** (RTO) is the targeted maximum time to restore a defined capability after a declared disruption.
- **recovery point objective** (RPO) is the targeted maximum age of recoverable state, expressed relative to a defined point and data class.
- **graceful degradation** preserves a reduced but explicitly acceptable service when full service is unavailable.
- **error budget** is the tolerated amount of unsuccessful service under a defined indicator, objective, population, and window.

### Central model, mechanism, or theorem

Define availability from stakeholder-visible eligible outcomes:

$$
A=\frac{successful\ eligible\ service\ events}{all\ eligible\ service\ events}
$$

over a declared window and environment. Architecture then applies tactics in a control loop: prevent selected faults, detect symptoms, contain propagation, preserve or reconstruct state, restore capacity and authority, reconcile uncertain outcomes, and learn through evidence. Every tactic is conditional on a fault model and can introduce new dependencies or common causes.

### Critical invariants

- define the capability, eligible population, success semantics, window, and observation point;
- distinguish availability, durability, correctness, latency, disaster recovery, and business continuity;
- specify fault and dependency assumptions, including common causes;
- preserve accepted-work identity and authoritative state across retry and failover;
- make failure detection, containment, recovery, and reconciliation ownership explicit;
- define degraded service and unsafe operations, not only binary up/down;
- separate RTO, RPO, detection time, failover time, and full restoration;
- test recovery paths and human authority, not just redundant components;
- prevent nominal control planes from being the only recovery path;
- bound evidence to the tested environment, faults, workload, and version.

### Common failures

Common failures include equating health checks with correctness; copying supplier uptime into an end-to-end objective; adding replicas inside one failure domain; retrying non-idempotent work; failing over to stale or corrupt state; assuming backups are recoverable; measuring restoration from engineer response instead of user failure; hiding planned downtime; declaring every request eligible after filtering failures; confusing RPO with backup frequency; ignoring control-plane, identity, DNS, and human dependencies; and never exercising failback or reconciliation.

### Compact example

An order service times out after sending a payment authorization. Retrying blindly can charge twice; failing the order can contradict a successful authorization. The architecture assigns a stable operation identity, persists pending state, queries or receives authoritative outcome, reconciles late results, and exposes a bounded pending response. Availability includes correct terminal or explicitly pending outcomes—not merely an HTTP response from a live process.

### Connections

[SARCH-003](003-functional-scope-and-system-context.md) supplies dependency and failure boundaries; [SARCH-004](004-quality-attributes-as-architectural-drivers.md) supplies measurable scenarios; [SARCH-005](005-constraints-assumptions-and-risks.md) supplies fault assumptions and residual risk; and [SARCH-010](010-framing-an-architecture-problem-before-choosing-technology.md) prevents premature redundancy choices. [SARCH-012](../ROADMAP.md) addresses latency, which interacts with detection, retry, and recovery.

## Governing Question

A service can have running processes, green health checks, and redundant servers while users cannot complete correct work. Conversely, a failed component may be invisible because another path preserves the outcome. What must architecture measure and control so availability reflects the capability rather than machinery?

The governing question is how to select tactics for an explicit failure model and recovery objective, then verify that normal, degraded, failover, reconciliation, and restoration behavior preserve stakeholder outcomes. There is no universally “highly available” topology.

## Why This Matters

Failures cross boundaries. A healthy application can depend on unavailable identity, DNS, certificates, networks, data, operators, or suppliers. Local redundancy may increase system complexity and create new common causes. Architecture must reason end to end and preserve authority during ambiguous outcomes.

Recovery is also a correctness problem. Restoring an old snapshot can violate accepted transactions. Promoting two writers can split authority. Retrying can duplicate effects. A fast restart that loses state may be worse than a slower, reconciled recovery.

Availability decisions affect cost, latency, consistency, security, operability, and change. Redundancy, timeouts, failover, queues, backups, and degraded modes all have assumptions and consequences. Explicit scenarios prevent “more replicas” from replacing analysis.

## Prerequisites and Retrieval

Retrieve capability, stakeholder, quality-attribute scenario, service-level indicator, service-level objective, eligible event, fault, error, failure, dependency, failure domain, common cause, state authority, idempotency, timeout, retry, recovery, reconciliation, invariant, RTO, RPO, backup, restore, failover, failback, and residual risk.

From earlier modules, retrieve typed context crossings, end-to-end measures, known-inventory limits, constraints and assumptions, ASR allocation, trade-off sensitivity, and decision records. You should be able to distinguish an external dependency’s service claim from the integrated capability outcome.

## Learning Objectives

After completing this module, you should be able to:

1. define availability from eligible stakeholder-visible outcomes;
2. distinguish faults, errors, failures, durability, correctness, and recovery;
3. construct availability and recovery scenarios with explicit fault models;
4. reason about serial dependencies and common causes;
5. select prevention, detection, containment, redundancy, and recovery tactics;
6. preserve authority and identity through retry, failover, and reconciliation;
7. define RTO and RPO without confusing them with implementation metrics;
8. design graceful degradation and manual operation safely;
9. plan claim-specific fault, backup, restore, and recovery evidence;
10. evaluate residual risk and reopen assumptions after incidents.

## Core Exposition

**Define the capability and success.** Start at the user or consuming system. Identify eligible operations, required correctness, response states, observation points, and time window. A request can return 200 while serving stale unauthorized data; it is not successful. An explicitly bounded pending response may be acceptable if the scenario permits it.

Time-based availability measures duration of unusability. Event-based availability measures the proportion of eligible service events that succeed. Event-based measures often represent partial service and variable demand better, but require careful eligibility and outcome definitions. Publish exclusions, maintenance treatment, client cancellations, overload rejection, and dependency failures.

**Define fault models.** Name component crash, process pause, network loss, delay, duplication, reordering, disk loss, corrupt data, configuration error, credential expiry, malicious action, supplier outage, zone loss, region loss, and operator error as applicable. State which faults can occur together. Availability claims outside this set remain unverified.

Failure domains are not labels. Two replicas on different machines can share power, network, deployment, identity, storage, software defect, configuration, or account authority. Common-cause analysis asks which single event can defeat supposedly independent paths.

**Prevent selected faults.** Simplicity, least privilege, safe defaults, resource quotas, validation, isolation, gradual rollout, compatibility rules, capacity margin, and controlled change can reduce failure likelihood. Prevention is never complete. It must be paired with detection and recovery for residual faults.

**Detect meaningful symptoms.** Heartbeats detect some loss of liveness, not correctness. Synthetic transactions can exercise a path but cover selected inputs. Invariants and reconciliation detect state divergence. User-edge telemetry observes outcomes but may arrive late. Use multiple signals and define detection latency, false positives, and false negatives.

Failure detectors under delay are uncertain. An aggressive timeout speeds failover but can eject healthy slow instances or create duplicate work. A conservative timeout preserves stability but extends unavailability. Treat thresholds as sensitivity points and test tail conditions.

**Contain propagation.** Partition failure domains, bound queues, isolate resources, shed load, limit concurrency, use bulkheads, and stop retry storms. Circuit breaking can prevent repeated calls to a failing dependency, but it needs open, half-open, and recovery semantics and can deny a recovered service if probes are wrong.

Containment also applies to change: staged deployment, blast-radius limits, feature controls, and rollback can stop a bad release from affecting all users. If configuration, schema, or data change is irreversible, binary rollback may not exist.

**Use redundancy with explicit independence.** Active-active capacity can reduce failover delay but complicates state authority and conflict. Active-passive can preserve one writer but requires promotion, readiness, data freshness, and tested failover. Spare components help only if they are compatible, provisioned, observable, and outside the relevant failure domain.

For a serial workflow that needs all independent components, availability multiplies. Parallel alternatives can improve availability only if routing, state, and shared dependencies permit either path to serve correctly. Independence assumptions usually dominate arithmetic.

**Preserve state and authority.** Stateless restart is simple only when durable authoritative state exists elsewhere. Replication reduces loss under selected failures but can copy corruption. Quorums or leaders manage authority under particular network and timing assumptions. Failover must prevent simultaneous writers or define conflict semantics.

Stable operation identities make retry and reconciliation possible. Idempotency is an end-to-end property of the effect and key scope, not an HTTP method label. Record pending and unknown outcomes rather than inventing success or failure.

**Separate backup, restore, and continuity.** A backup is a copy under a policy. Recoverability requires readable data, keys, schemas, software, dependencies, procedures, authority, capacity, and verified restoration. Backup frequency does not equal RPO if replication lag, incomplete snapshots, corruption, or unprotected logs change the recoverable point.

RTO begins at a defined event—fault occurrence, detection, incident declaration, or user impact—and ends at a defined service state. State whether it includes diagnosis, authorization, infrastructure, data restore, validation, traffic shift, and backlog recovery. Full business recovery may take longer than minimum service restoration.

**Design degraded behavior.** Decide which capabilities remain safe and valuable. A store may allow browsing but disable checkout when payment is unknown. A clinical system may display last-known data with age and authority while preventing unsafe writes. Degradation must not bypass authorization, hide staleness, or produce irreversible incorrect outcomes.

Manual fallback creates human capacity, training, accessibility, audit, timing, and reconciliation dependencies. Exercise it with realistic volumes and unavailable primary tools. A PDF runbook reachable only through the failed identity system is not a recovery path.

**Plan recovery and failback.** Recovery includes detection, incident authority, containment, promotion or rebuild, data validation, traffic restoration, capacity, backlog, reconciliation, and communication. Failback can be as risky as failover because authority and state move again. Define when recovered components are trustworthy and who decides.

Automate deterministic, well-bounded actions while preserving safe stop conditions and operator visibility. Automation can amplify a bad diagnosis. High-consequence recovery may require independent confirmation or two-person authority.

**Test claims, not rituals.** Verify backups by restoring them. Exercise loss of the primary control plane, credentials, people, region, and supplier where relevant. Test partial failures, corrupt data, slow responses, duplicate messages, and capacity during recovery. Record toolchain, topology, version, workload, injected fault, actual output, and limitation.

A game day supports behavior under selected conditions; it does not prove every fault is tolerated. Production indicators show observed outcomes for a period. Incidents and near misses update fault models, assumptions, tactics, and ADRs.

## Definitions and Notation

Let $E_w$ be eligible service events in window $w$, and $S_w\subseteq E_w$ those meeting correctness and response criteria. Event availability is

$$
A_w=\frac{|S_w|}{|E_w|},\qquad |E_w|>0.
$$

If $|E_w|=0$, report no observations rather than 100% availability. Time availability over observed interval $T$ with unusable duration $D$ is

$$
A_T=1-\frac{D}{T}.
$$

For independent serial dependencies required for success,

$$
A_{series}=\prod_{i=1}^{n}a_i.
$$

For two independent parallel alternatives where either suffices,

$$
A_{parallel}=1-(1-a_1)(1-a_2).
$$

These models require binary success, correct routing, compatible state, and independence. Shared causes, overload, degraded outcomes, repair dynamics, and correlated maintenance require richer models.

Define $t_d$ detection time, $t_c$ containment time, $t_r$ minimum service restoration, and $t_f$ full restoration including backlog and reconciliation. They need not occur in a simple sum or start at the same reference event. Define RPO for data class $x$ as a maximum acceptable interval between the failure reference point and latest correctly recoverable state for $x$.

## Mechanisms, Invariants, or Proof Structure

Use this availability and recovery mechanism.

1. **Frame the service:** define capability, users, eligible outcomes, correctness, window, and observation.
2. **Build the fault model:** identify faults, dependencies, common causes, detection limits, and residual scope.
3. **Set objectives:** define availability, degradation, RTO, RPO, backlog, and communication scenarios.
4. **Prevent:** reduce fault likelihood through simplicity, isolation, validation, capacity, and safe change.
5. **Detect:** combine liveness, correctness, invariant, synthetic, user-edge, and operational signals.
6. **Contain:** bound propagation, load, queues, retries, resources, releases, and authority.
7. **Recover:** restore capacity and state, establish one authority, reconcile, and fail back safely.
8. **Degrade:** preserve explicitly safe capabilities and manual procedures.
9. **Verify:** test faults, restore, traffic shift, capacity, control paths, humans, and evidence limitations.
10. **Learn:** update fault models, assumptions, decisions, runbooks, and residual risk after observation.

The governing invariants are outcome-based measurement, explicit eligibility, bounded fault model, visible common causes, stable accepted-work identity, single or reconciled authority, honest degradation, distinct RTO/RPO, executable recovery, claim-specific evidence, and lifecycle learning.

Arithmetic availability models prove only results under stated independence and composition assumptions. Passing exercises proves observed recovery in the tested environment, not universal resilience.

## Alternatives and Trade-Offs

**Active-active** reduces failover delay and can share load, but increases coordination, consistency, conflict, and operational complexity. **Active-passive** simplifies authority but depends on promotion, standby readiness, data freshness, and failover capacity.

**Fast detection** reduces user impact but increases false failover under delay or load. **Slow detection** avoids churn but extends outages. Use differentiated thresholds, multiple signals, hysteresis, and scenario evidence.

**Retries** mask transient failure but amplify load and duplicate effects. **Fail-fast behavior** protects capacity but exposes more immediate failure. Bound attempts, use budgets and jitter, preserve operation identity, and coordinate across layers.

**Strong consistency** can preserve one authoritative state but may reject or delay operations during partition. **Available degraded operation** preserves access but needs safe subsets, staleness, conflict, and reconciliation semantics.

**Automated recovery** is fast and repeatable for modeled faults but can amplify incorrect diagnosis. **Manual recovery** supports judgment for novel conditions but is slower, capacity-limited, and vulnerable to access or training gaps. Combine automation with observability, stop conditions, and practiced authority.

## Failure Modes and Misconceptions

- **“The process is up, so the service is available.”** Measure correct stakeholder-visible outcomes.
- **“Five nines is a design.”** It is incomplete without service, population, window, exclusions, and consequence.
- **“Replicas are independent.”** Deployment, data, identity, configuration, and operators can be common causes.
- **“Retry improves reliability.”** Unbounded or non-idempotent retry can cause overload and duplicate effects.
- **“Timeout means failure.”** It means the observer lacks a timely result; the effect may have occurred.
- **“Backup means recoverable.”** Keys, software, schema, authority, capacity, and restore evidence are required.
- **“RPO equals backup interval.”** Recoverable state depends on capture, completeness, integrity, and restoration.
- **“RTO starts when on-call responds.”** Define the stakeholder-relevant reference and end state.
- **“Failover completes recovery.”** Reconciliation, capacity, backlog, communication, and failback remain.
- **“Planned downtime does not count.”** Eligibility and exclusions require stakeholder authority, not convenience.
- **“A degraded response is always better.”** Unsafe, stale, or unauthorized behavior can be worse than refusal.
- **“Supplier SLA composes.”** End-to-end service includes every dependency and integration behavior.
- **“A game day proves resilience.”** It supports only selected faults, conditions, versions, and observations.
- **“Automation removes human dependency.”** Authority, diagnosis, access, and stop decisions often remain human.

## Worked Examples

### Example 1

**Question:** A service handled 99,700 of 100,000 eligible requests correctly. What is event availability?

**Reasoning:** $A=99{,}700/100{,}000=0.997$, or 99.7%. Confirm that failures, timeouts, incorrect responses, retries, and partial results were classified consistently. The result describes this population and window only.

**Conclusion:** Availability arithmetic is meaningful only after eligibility and success semantics are defined.

### Example 2

**Question:** How much unavailability does 99.9% allow in a 30-day window?

**Reasoning:** The window contains $30\times24\times60=43{,}200$ minutes. The unavailable fraction is $0.001$, so allowed unavailability is $43.2$ minutes. A 40-minute outage during payroll cutoff can still violate a business scenario.

**Conclusion:** Aggregate percentages must be paired with critical-window and consequence scenarios.

### Example 3

**Question:** Three independent serial dependencies each have 99.9% availability. What is the simplified workflow availability?

**Reasoning:** $0.999^3=0.997002999$, about 99.7003%. The result assumes independent binary success and all three are required. Shared dependencies can worsen it; degraded alternatives can change the model.

**Conclusion:** Assigning the end-to-end target to each dependency does not preserve the target.

### Example 4

**Question:** Two independent paths each have 99% availability and either suffices. What is simplified parallel availability?

**Reasoning:** Both fail with probability $0.01\times0.01=0.0001$, so availability is $1-0.0001=0.9999$, or 99.99%. Shared routing, data, deployment, or identity can destroy independence.

**Conclusion:** Redundancy helps only when paths are correctly substitutable and independent for the modeled fault.

### Example 5

**Question:** Should a payment request be retried after timeout?

**Reasoning:** A timeout is an unknown observation. Reuse a stable idempotency identity, persist pending state, query or accept authoritative callback, and reconcile late results. Blind retry can double charge; immediate failure can contradict an accepted payment.

**Conclusion:** Availability tactics must preserve effect identity and correct uncertainty semantics.

### Example 6

**Question:** Does a daily backup provide a 24-hour RPO?

**Reasoning:** Not necessarily. The snapshot may be incomplete, corrupt, unencrypted without usable keys, missing logs, or unrecoverable with current schema and software. Define data class and failure point, then restore and validate state. Continuous replication can also copy corruption.

**Conclusion:** RPO is a recoverable-state objective, not a schedule label.

### Example 7

**Question:** Why can a health check cause an outage?

**Reasoning:** Under overload, slow but correct instances may miss aggressive probes. Removing them raises load on survivors, causing cascading ejection. Use representative health semantics, concurrency limits, load shedding, hysteresis, and separate readiness from liveness.

**Conclusion:** Detection thresholds are sensitivity points that interact with capacity and containment.

### Example 8

**Question:** What is required for safe read-only degradation?

**Reasoning:** Identify authoritative snapshot, freshness age, authorization, allowed data, unsafe writes, user communication, cache integrity, expiry, and recovery. A medical viewer may show last-known allergies with timestamp while blocking medication updates; stale identity must not grant access.

**Conclusion:** Degraded mode is a specified capability with invariants, not an improvised bypass.

### Example 9

**Question:** Why test failback after successful failover?

**Reasoning:** The former primary may contain stale or divergent state. Returning traffic can reintroduce split authority, overload, schema mismatch, or old configuration. Validate synchronization, fence obsolete writers, stage traffic, observe outcomes, and retain rollback.

**Conclusion:** Authority and state move twice; recovery evidence must cover both transitions.

### Example 10

**Question:** How should availability be designed for an emergency ventilation controller?

**Reasoning:** Define safe physical states, sensor faults, power, networks, local control, operator authority, timing, degraded operation, cybersecurity, and recovery. Redundancy cannot replace hazard analysis or physical evidence. No external safety, industrial-control, regulatory, human-factors, cybersecurity, or practitioner review is claimed; named qualified authorities must validate hazards, objectives, independence, tests, release, and residual risk.

**Conclusion:** High-consequence availability is safe service under defined faults, not maximum software uptime.

## Cross-Program Connections

- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies fault injection, recovery verification, statistical evidence, and oracle design.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) operates SLIs, SLOs, error budgets, incidents, rollouts, and recovery exercises.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) develops transactions, replication, backup, restore, and recovery correctness.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) explains process, storage, scheduling, resource, and failure mechanisms.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies delay, partition, routing, redundancy, and reachability behavior.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects continuity, hazards, human operation, and lifecycle recovery.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) formalizes partial failure, failure detection, replication, consensus, and consistency.

## References

1. Betsy Beyer et al., editors. [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/), O'Reilly, 2016. Service indicators, objectives, error budgets, monitoring, distributed-system reliability, and incident response; consulted 2026-09-05.
2. Google. [Availability Table](https://sre.google/sre-book/availability-table/), *Site Reliability Engineering*. Time-based and aggregate availability calculations and allowed unavailability; consulted 2026-09-05.
3. Marianne Swanson et al. [NIST SP 800-34 Rev. 1, Contingency Planning Guide for Federal Information Systems](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final), May 2010, updated November 2010. Contingency planning, business impact, recovery strategies, testing, maintenance, and lifecycle integration; consulted 2026-09-05.
4. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. Availability scenarios, fault detection, recovery, prevention tactics, and trade-offs.
5. Michael Nygard. *Release It! Design and Deploy Production-Ready Software*, second edition, Pragmatic Bookshelf, 2018. Stability patterns, cascading failure, timeouts, circuit breakers, bulkheads, and production learning.
6. Martin Kleppmann. *Designing Data-Intensive Applications*, O'Reilly, 2017. Faults, partial failure, replication, consistency, transactions, and distributed data recovery.
7. ISO. [ISO 22301:2019, Security and resilience—Business continuity management systems—Requirements](https://www.iso.org/standard/75106.html), edition 2, October 2019. Business continuity management, disruption response, recovery, and improvement; consulted 2026-09-05.
8. David D. Clark. “The Design Philosophy of the DARPA Internet Protocols.” *ACM SIGCOMM Computer Communication Review* 18(4), 1988. Survivability, fate sharing, end-to-end state, and failure-oriented design principles.

## Exercises

### Exercise 1

Define an availability indicator for course registration that avoids counting incorrect confirmations, invalid requests, and hidden retry attempts misleadingly.

### Exercise 2

Compute simplified availability for four independent serial dependencies at 99.95% each, then explain why the result is not a production guarantee.

### Exercise 3

Diagnose a design with three replicas in one region, one global identity tenant, automatic retries at every layer, daily untested backups, and a 99.99% user promise.

### Exercise 4

Compare active-active and active-passive recovery for an order authority. Address failure model, state, fencing, latency, cost, operations, failover, failback, and evidence.

### Exercise 5

Design availability and recovery assurance for an unfamiliar regional blood-bank inventory network. Separate automation, exercises, clinical and operational authority, and blockers.

## Answers to the Exercises

### Answer 1

Define eligible events as syntactically valid, authorized registration attempts received at the user edge during declared enrollment windows, with stable operation identity so client retries count as one logical attempt. Success means the system returns a correct confirmed registration, correct rule-based rejection, or explicitly allowed bounded pending state while preserving prerequisite, capacity, and duplicate invariants. Timeouts, incorrect confirmations, unresolved pending beyond the bound, and accepted work later lost are failures.

Publish window, population, observation points, excluded maintenance under stakeholder policy, identity outages, downstream dependencies, partial results, and reconciliation. Measure logical outcomes rather than raw HTTP responses. Segment peak, normal, cohort, and degraded conditions so aggregate success cannot hide the critical opening period.

### Answer 2

Each dependency has $a=0.9995$. Under independent binary success with all four required,

$$
A=0.9995^4=0.9980014995000625,
$$

or about 99.80015%. The result does not cover common identity, network, deployment, configuration, data, or operator causes; variable demand; repair; degraded behavior; correctness; dependency definitions; or measurement differences. Production evidence must validate the end-to-end outcome under declared conditions. The arithmetic demonstrates only that copying an end target to serial components is inadequate under the simplified model.

### Answer 3

The replicas share regional infrastructure and likely deployment, configuration, and data causes. Global identity remains a single failure path. Layered retries multiply attempts, amplify overload, and can duplicate effects. Backup schedule does not prove recoverability, keys, completeness, or RPO. The user promise lacks eligible outcomes, window, exclusions, correctness, workload, degradation, and end-to-end composition.

Build fault and dependency models; define service indicators and business scenarios; isolate relevant failure domains; coordinate retry budgets and stable operation identities; provide overload containment; separate recovery credentials and control paths; test restore, state authority, failover, capacity, reconciliation, and failback; and record residual common causes. Reframe 99.99% through stakeholder consequence and evidence rather than topology count.

### Answer 4

Active-active can serve regional loss quickly and reduce distance, but order authority requires partitioning, consensus, or explicit conflict semantics; payment and inventory unknown outcomes still need reconciliation. It increases routing, security, deployment, observability, and operational complexity. Active-passive preserves a simpler writer model but requires current standby state, promotion authority, fencing, capacity, routing, and a longer tested recovery path.

For both, define region, network, data-corruption, configuration, identity, supplier, and operator faults; RTO/RPO; accepted-work behavior; backlog; and degraded service. Test partitions, stale state, duplicate commands, promotion, fencing, full load, control-plane loss, recovery, and failback with versioned evidence. Select using consequence, team capability, cost, latency, consistency, and residual risk; no topology guarantees availability by name.

### Answer 5

Define authoritative inventory by blood product, location, compatibility, expiry, reservation, transport, and reconciliation. Model hospital, donation center, laboratory, transport, identity, network, power, operator, and emergency authority dependencies. Scenarios include network partition, stale stock, duplicate reservation, refrigeration failure, disaster demand, identity outage, manual allocation, recovery, and data reconciliation. Degraded operation must expose age and uncertainty and prevent unsafe double allocation.

Automation can check state-machine and unit invariants, stable identities, schema/configuration, replication lag, expiry, alerts, trace links, and evidence freshness. Exercises can test partition, manual procedures, restore, failover, reconciliation, logistics, and full-load recovery. These do not establish clinical compatibility, emergency allocation policy, human capacity, or acceptable risk. No external blood-bank, clinical, logistics, safety, regulatory, cybersecurity, human-factors, or practitioner review is claimed. Named qualified authorities must own clinical rules, operational allocation, hazards, validation, release, and residual risk. Ambiguous inventory authority, stale compatibility data, unsafe duplicate allocation, unavailable manual procedure, failed restore, or unresolved high-severity hazard blocks the corresponding readiness claim.
