---
module_id: SARCH-060
program: Software Engineering: Software Architecture
level: 2
module_number: 60
title: Evaluating a Distributed Architecture Under Failure
status: complete
last_verified: 2026-09-06
---

# Evaluating a Distributed Architecture Under Failure

## One-Page Review

### Governing question

How can an architecture team obtain bounded, reproducible evidence that a distributed system preserves named business, safety, security, and recovery properties under relevant faults, rather than merely demonstrating that processes restart?

### Essential definitions

- A **fault** is a hypothesized cause of an incorrect state; an **error** is an incorrect internal state; a **failure** is an externally visible deviation from the promised service [1].
- A **failure model** declares the faults, timing, scope, combinations, and adversarial powers covered by an analysis or experiment.
- A **steady-state hypothesis** states which measured properties should remain within bounds during an experiment.
- A **failure scenario** names trigger, injection point, scope, timing, duration, workload, expected response, recovery condition, and evidence.
- A **safety property** says that a forbidden outcome never occurs; a **liveness property** says that a desired outcome eventually occurs under stated fairness and recovery assumptions.
- **Fault injection** deliberately creates or simulates a fault at a controlled boundary. **Chaos engineering** uses experiments on a system to build evidence about behavior under turbulent conditions [2, 3].
- An **oracle** decides whether an observed history satisfies a specified property. A health endpoint is an observation, not an end-to-end oracle.
- **Blast radius** is the people, tenants, data, resources, regions, or physical processes exposed to an experiment or real fault.
- **Containment** prevents a local fault or exhausted resource from propagating beyond a declared boundary.
- **Reconciliation** compares durable technical and business facts after recovery and resolves unknown, duplicate, missing, or conflicting outcomes.

### Central model, mechanism, or theorem

Evaluation joins a claim to a failure model and evidence:

$$
J=(C,A,F,W,O,E,L),
$$

where $C$ is the claim, $A$ its assumptions, $F$ the injected or analyzed failure scenario, $W$ the workload and system configuration, $O$ the oracle, $E$ the retained evidence, and $L$ the limitations. A passing result supports only this tuple. It does not prove universal resilience.

For a recovery objective $T_{obj}$, measure from business-impact start $t_b$ to verified useful recovery $t_v$:

$$
T_{rec}=t_v-t_b.
$$

Routing completion, process restart, or queue drain is not necessarily $t_v$. The endpoint must include the declared service, data, authority, security, and reconciliation conditions.

### Critical invariants

- every claim names service, users, workload, configuration, property, threshold, interval, and failure scope;
- every injected fault has authorization, bounded blast radius, stop conditions, cleanup, and an independent abort path;
- control and observation are independent enough that the experiment cannot hide its own harm;
- safety and security invariants remain mandatory in degraded mode unless an accountable exception is explicitly authorized;
- retries preserve business identity and remain within one end-to-end time and work budget;
- only current fenced authority may accept writes or issue commands after reconfiguration;
- backups, replicas, caches, and queues count as recovery mechanisms only when their required restore paths and dependencies are exercised;
- recovery is not complete until ambiguous business effects and integrity violations are reconciled;
- negative and anomalous observations are retained with exact system and experiment versions;
- a successful campaign is evidence for tested conditions, never proof that untested faults cannot fail.

### Common failures

Common failures include injecting only process kills; choosing faults after seeing telemetry; testing an idle toy system; using the same control plane to inject, observe, and abort; declaring success when health checks turn green; omitting common-mode dependencies; assuming redundant providers are independent; masking data loss with stale caches; retrying non-idempotent operations; failing over without fencing; measuring recovery from alert time rather than impact start; stopping the clock before reconciliation; running production experiments without explicit authority; turning a game day into an improvised outage; and treating zero observed failures as a zero failure probability.

### Compact example

A checkout service promises that under loss of one application zone at 600 orders/s, at least 95% of admitted orders reach a durable terminal state within 30 seconds, no payment is captured twice, and no order is reported declined while payment outcome is unknown. The experiment records one order and payment identity per intent, removes the zone, checks histories against the three oracles, caps exposure at 5% of tenants, and aborts independently on duplicate capture or backlog age above 20 seconds. Recovery ends only after unknown provider outcomes reconcile. A green load balancer alone cannot pass the claim.

### Connections

[SARCH-051](051-partial-failure-as-an-architectural-constraint.md) defines partial failure; [SARCH-052](052-consistency-and-availability-trade-offs.md) through [SARCH-059](059-edge-and-hybrid-architectures.md) supply the architectures being evaluated. [SARCH-061](../ROADMAP.md) next introduces the Architecture Tradeoff Analysis Method. Reliability Engineering owns production reliability practice; this module owns architectural judgment from failure evidence.

## Governing Question

A diagram can show redundancy, queues, regions, and control planes without showing whether they preserve an outcome when timeouts, partitions, overload, stale authority, corrupt state, or operator error interact. Architecture evaluation must turn vague confidence into explicit, falsifiable claims and evidence.

The task is not to ask whether “the system survives failure.” It is to identify which properties must hold, under which faults and workloads, for how long, with which degraded contract, and how observers decide. The answer combines analysis, deterministic testing, simulation, controlled injection, recovery exercises, production evidence, and disciplined limits.

## Why This Matters

Distributed failures are usually selective. A request can time out after its payment completed; one region can accept writes while another believes it is primary; a queue can protect the producer while exhausting consumers; a cache can keep pages green while authoritative data is unavailable. Component recovery can therefore coexist with business loss, security exposure, and permanent divergence.

Evaluation affects architecture before incidents. It exposes hidden shared dependencies, unsafe authority transfers, unbounded retry amplification, missing observability, and recovery paths that require the failed control plane. It also prevents overclaiming: one successful experiment establishes observed behavior for a recorded configuration, not a universal probability or guarantee.

## Prerequisites and Retrieval

Retrieve fault, error, failure, partial failure, failure domain, common cause, timeout, deadline, retry, idempotency, backpressure, queue, overload, circuit breaker, bulkhead, partition, quorum, consistency, epoch, lease, fencing, failover, recovery point, recovery time, degraded mode, observability, trace, audit, hypothesis, invariant, safety, liveness, workload, oracle, blast radius, canary, rollback, reconciliation, and residual risk.

From SARCH-051 retrieve explicit failure models and ambiguous outcomes. SARCH-052 through SARCH-054 supply consistency, placement, and regional authority. SARCH-055 through SARCH-059 supply control planes, cells, queues, event-native execution, and edge operation. Testing Engineering supplies test-design depth; Distributed Systems supplies formal protocol properties; Reliability Engineering supplies SLO and incident practice.

## Learning Objectives

After completing this module, you should be able to:

1. translate architectural promises into scoped, falsifiable failure claims;
2. construct fault, dependency, workload, state, and recovery coverage models;
3. distinguish safety, liveness, availability, integrity, security, and business-outcome oracles;
4. select analysis, model checking, simulation, test environments, and production experiments by claim;
5. design safe fault injection with progressive exposure and independent controls;
6. evaluate quorum, failover, queue, retry, cache, and degraded-mode behavior;
7. measure recovery from impact through business reconciliation;
8. recognize common cause, correlated faults, observer failure, and experiment confounding;
9. interpret repeated experiments without false statistical certainty;
10. write an evidence-bounded architectural verdict with residual risks and required changes.

## Core Exposition

**Start from consequences, not fault tools.** Name the externally valuable service and the unacceptable outcomes. “Pods restart” is a mechanism claim. “No acknowledged order is lost” is a business integrity claim. “No stale controller can actuate a gate” is an authority and safety claim. Only the latter claims tell the evaluator what must be observed end to end.

State the population, workload, topology, versions, data state, threat assumptions, and interval. A claim about one-zone loss at ordinary load says nothing about a regional control-plane failure during a traffic peak. Avizienis and colleagues distinguish faults, errors, and failures precisely because injecting a fault does not tell us which errors it activates or which service failures emerge [1].

**Write a failure model.** Cover crash-stop, crash-recovery, omission, delay, reordering, duplication, partition, corruption, exhaustion, timing, stale configuration, bad deployment, credential failure, malicious input, and operator action where relevant. Specify scope: one process, host, rack, zone, region, identity authority, network path, tenant, or common dependency.

Single faults are a starting point. Distributed incidents often combine latent state with a trigger: a full retry budget meets slow storage; an expired certificate meets control-plane loss; a failover meets an old writer; a restore meets an incompatible schema. Pairwise or sequence-based campaigns reveal interactions, but combinatorial explosion requires risk-based selection.

**Map dependencies and common causes.** Draw request, state, control, identity, time, telemetry, deployment, and recovery dependencies. Include DNS, keys, certificate validation, quotas, build artifacts, operators, and physical facilities. Two services in different zones are not independent when they share a database, route controller, credential issuer, or deployment pipeline.

Use cut sets qualitatively: which smallest combinations remove the required outcome? Quantitative reliability models help only when event definitions, time basis, dependence, repair, and data justify them. Do not square a guessed failure probability to make redundancy look safe.

**Define oracles before injection.** A process oracle checks liveness; a protocol oracle checks histories; a data oracle checks acknowledged state, invariants, and durable effects; a business oracle checks orders, payments, notifications, or physical outcomes; a security oracle checks authority and confidentiality; a recovery oracle checks reconciled terminal state. One experiment may need all of them.

Linearizability, for example, is a safety property over operation histories: each completed operation must appear to take effect at one point between invocation and response while respecting real-time order [4]. A successful health probe cannot establish it. Use a history checker with unique operations and uncertain outcomes, plus implementation evidence appropriate to the claim.

**Separate safety from liveness.** During a partition, refusing writes may preserve one-copy authority but reduce progress. Accepting writes in both partitions may preserve local availability while violating a global invariant. State which choice the architecture promises and test the exact boundary.

Safety failures usually require immediate abort and preservation of evidence. Liveness results require a declared time bound, fairness assumptions, workload, and eventually restored resources. “Eventually recovers” without a bound or resource premise cannot guide operations.

**Build a coverage model.** Create a matrix across fault class, injection point, scope, workload, system state, duration, recovery path, and property. Add peak, burst, skew, large tenant, cold cache, backlog, schema transition, credential rotation, and deployment states. Include early injection, midpoint failure, post-effect response loss, restart during recovery, and a second fault during degraded operation.

A weighted coverage score can prioritize work but is not a reliability probability. If scenario weights $w_i$ represent reviewed importance and $x_i$ is 1 only when a scenario has current passing evidence, then $K=\sum w_ix_i/\sum w_i$ reports plan coverage. Its meaning depends entirely on the scenario set and weights; unmodeled hazards remain outside the denominator.

**Choose evidence by the claim.** Static architecture review reveals missing boundaries. Fault trees and dependency analysis reveal combinations. Formal specification and model checking explore protocol states under abstractions. Deterministic simulation explores many event schedules with reproducible seeds. Component injection isolates mechanisms. Integrated environments expose real dependencies. Production experiments provide operational realism but require much stronger safeguards.

No method dominates. A model checker cannot validate kernel, cloud, or human behavior omitted from its model. A staging exercise may differ in data volume, topology, and operator access. A production experiment observes only executed conditions and may be unsafe for irreversible consequences. FoundationDB’s published architecture describes deterministic simulation as a major testing mechanism, but its evidence is tied to that system’s design for simulation [5].

**Make the experiment reproducible.** Record hypothesis, architecture revision, build and configuration digests, dependency versions, topology, data fixture, workload generator, clock basis, random seed, injected fault, timing, commands, observers, traces, metrics, logs, outcomes, anomalies, cleanup, and reviewer. Preserve failed runs; they often carry the most valuable evidence.

Determinism supports replay but does not guarantee realism. Nondeterministic experiments need synchronized timestamps, causation and request identities, enough repetitions, and explicit variance. Changes between runs invalidate simple comparisons unless treated as experiment factors.

**Control blast radius.** Begin with review, model, or simulation; then isolated component tests; then integrated non-production environments; then canary or production experiments only when the risk warrants and authority exists. Progressive exposure should vary tenants, requests, instances, zones, duration, or capabilities independently.

Define preconditions and abort conditions before execution. The abort path must not rely solely on the component being failed. Protect emergency access, safety interlocks, data backups, customer communications, and incident command. Chaos Engineering literature emphasizes empirical experiments and minimizing blast radius, but the practice does not waive change, safety, privacy, or security governance [2, 3].

**Test observers and controls.** An injection controller can report success even when it did not affect the intended target. Confirm the fault through an independent signal. Similarly, an observability pipeline may fail with the service, clocks may skew, sampling may omit affected tenants, and dashboards may aggregate away a minority failure.

Use at least one observer outside the injected boundary. Record missing telemetry as evidence, not as zero errors. Test whether responders can distinguish injection, real incident, observer failure, and recovery. If the same identity system authorizes injection and emergency stop, its failure can remove both.

**Exercise retry and overload behavior.** Retry evaluation must trace one business identity through every layer and count total attempts, elapsed time, concurrency, queue depth, and downstream work. Inject delay and ambiguous completion, not only clean refusal. Confirm that retry budgets, admission, breakers, and bulkheads prevent a degraded dependency from consuming healthy capacity.

A fixed independent retry model may have expected attempts $1/(1-p)$ for per-attempt retry probability $p<1$, but real overload violates independence: attempts add load and change $p$. Use the expression only as a baseline, then load-test feedback, synchronized retries, and recovery surges.

**Evaluate queues by age and outcome.** A queue can turn a visible failure into delayed harm. Measure admitted rate, service rate, oldest age, bytes, tenant fairness, expiry, redrive, poison handling, and business validity. When service rate stays below arrival rate, recovery cannot complete without added capacity, shedding, prioritization, or a changed contract.

Inject consumer loss, partition, duplicate delivery, crash around external effects, expired work, schema incompatibility, and poison input. A drained queue is insufficient if effects duplicated, orders expired, or dead-letter work remained unowned.

**Evaluate caches and degraded modes.** Force origin loss, stale entries, revocation, deletion, partial invalidation, and cold restart. Confirm that responses identify freshness and do not elevate cached data into write authority. A fallback must have bounded age, scope, security behavior, capacity, exit criteria, and reconciliation.

Degraded service is a separate contract. List allowed and forbidden operations, users, duration, data sources, authority, visibility, and safe exit. Test entry and exit repeatedly; many systems enter degraded mode but cannot leave without a second outage.

**Evaluate failover as authority transfer.** Kill the current writer at awkward points: before commit, after commit before response, during replication, during lease renewal, and during promotion. Partition old and new leaders, skew clocks within and beyond assumptions, lose the control plane, and restart the old leader after promotion.

The oracle checks that only current authority accepts effects, stale authority is fenced, acknowledged durability matches the contract, capacity is adequate, and ambiguous operations reconcile. Traffic moving to a destination is routing evidence, not proof of safe failover.

**Test recovery dependencies.** Recovery may need identities, keys, DNS, artifacts, schemas, quotas, consoles, networks, backups, and people unavailable in the incident. Exercise cold bootstrap rather than only warm restart. Restore into an isolated environment, verify data and executable compatibility, and establish how clean state is selected if recent state may be corrupt or compromised.

Measure from impact start to useful recovered service. Track detection, decision, access, provisioning, restore, replay, validation, routing, backlog clearance, and reconciliation separately. This reveals which architectural dependency dominates recovery rather than hiding it behind one total.

**Reconcile business outcomes.** Timeouts create unknowns. After the technical path is healthy, query durable identities across orders, payments, inventory, messages, and external providers. Classify each as completed, confirmed absent, rejected, compensated, or unresolved. Preserve human repair and customer communication.

Exactly-once business effect is not established by one delivery metric. It needs stable intent identity, conditional state transitions, durable receipts, deduplication retention, and reconciliation across every side-effect boundary.

**Include security and adversarial faults.** Test expired or revoked credentials, unavailable identity services, stale authorization, key loss, malicious payload, compromised automation, replayed control commands, observer tampering, and break-glass access. Degraded availability must not silently expand privilege.

Production security experiments require tightly scoped authority and data protection. Some attack paths belong in isolated environments or independent assessments. Record which cases were not executed and why; absence of safe authorization is a limitation, not a passing result.

**Interpret repeated results carefully.** Zero failures in $n$ independent identical Bernoulli trials does not establish zero risk. A rough 95% upper confidence bound called the rule of three is $p<3/n$ when its assumptions hold. With 300 qualifying trials and zero failures, the bound is about 1%, not zero.

Distributed experiments rarely satisfy identical independent trials: state, traffic, versions, schedules, and recovery history differ. Report counts and contexts; use statistical models only with justified sampling and independence. Rare catastrophic, adversarial, systematic, and common-cause failures cannot be dismissed by routine trial frequency.

**Write a verdict, not a celebration.** For each claim, report passed, failed, inconclusive, unavailable, or not evaluated. Attach evidence and limitations. Separate observations from causal inference. List defects, architectural changes, temporary containment, residual risks, owners, and evidence-expiry conditions.

Evidence expires when topology, workload, dependency, version, schema, identity, recovery procedure, threat, or staff changes materially. Re-run the smallest campaign that restores the argument. A mature architecture keeps evaluation designs as durable assets, not one-time demonstrations.

## Definitions and Notation

Let:

- $C$ be a scoped architectural claim and $A$ its assumptions;
- $F=(g,p,s,t,d)$ describe fault trigger $g$, injection point $p$, scope $s$, timing $t$, and duration $d$;
- $W$ be recorded workload, topology, state, software, configuration, and dependency versions;
- $O$ be the set of property oracles and $E$ retained evidence;
- $t_b$ be business-impact start and $t_v$ verified useful recovery;
- $T_{rec}=t_v-t_b$ be measured recovery time for the declared outcome;
- $w_i>0$ be reviewed importance weight for scenario $i$ and $x_i\in\{0,1\}$ indicate current passing evidence;
- $K=\sum_iw_ix_i/\sum_iw_i$ be a planning coverage ratio, not a reliability probability;
- $n$ be qualifying repeated trials and $p$ an assumed identical independent per-trial failure probability;
- **confounder** mean an uncontrolled difference that offers another explanation for an observed change;
- **counterfactual** mean the unobserved outcome that would have occurred without the intervention;
- **evidence expiry** mean a defined change that invalidates transfer of an earlier result.

An evaluation result has the form $J=(C,A,F,W,O,E,L)$, with $L$ recording limits and exclusions. Two results are comparable only when relevant tuple differences are controlled or explicitly analyzed.

## Mechanisms, Invariants, or Proof Structure

### Failure-evaluation procedure

1. Identify stakeholders, valuable outcomes, unacceptable harm, authority, and decision owner.
2. Convert architectural promises into measurable safety, liveness, integrity, security, performance, and recovery claims.
3. Record assumptions, topology, state, workload, versions, and evidence-expiry conditions.
4. Map service, state, control, identity, time, deployment, observation, recovery, people, and physical dependencies.
5. Define faults, combinations, sequences, scopes, durations, and common causes.
6. Define independent technical, business, security, physical, and recovery oracles.
7. Build the coverage matrix and prioritize by consequence, uncertainty, novelty, incident history, and architectural sensitivity.
8. Select review, formal analysis, deterministic simulation, isolated injection, integrated exercise, or production experiment.
9. Establish preconditions, authorization, blast radius, abort, cleanup, incident ownership, and evidence capture.
10. Execute reproducibly, preserve all outcomes, reconcile effects, and issue a bounded verdict.

### Proof obligations

For each passing claim, reviewers must be able to answer:

- **Relevance:** Did the injected condition activate the intended architectural boundary under representative state and load?
- **Observability:** Could the oracles see every property named in the claim, including minority and missing-data outcomes?
- **Control:** Were confounders, experiment interference, and version changes recorded?
- **Containment:** Could the experiment itself exceed authority or harm bounds?
- **Recovery:** Did measurement include useful service, integrity, authority, security, backlog, and reconciliation?
- **Transfer:** Which production configurations and future changes can legitimately inherit the result?

### Invariants

- no success verdict without a falsifiable predeclared claim and oracle;
- no experiment without bounded authority, exposure, abort, cleanup, and retained evidence;
- no fault confirmation solely from the injector that attempted it;
- no availability result that hides incorrect, unauthorized, stale, or duplicate outcomes;
- no failover success while stale authority can still act;
- no recovery success before business and security reconciliation;
- no coverage ratio represented as incident probability;
- no repeated-trial statistic without sampling and independence assumptions;
- no evidence transfer across a material expiry condition without review;
- no unexecuted or unsafe scenario silently counted as passing.

## Alternatives and Trade-Offs

- **Architecture review versus experiment:** review is cheap and broad but may miss runtime interactions; experiments observe implementation behavior but cover only executed conditions.
- **Formal model versus deployed system:** formal methods exhaustively explore a bounded abstraction; deployed tests include real code and dependencies but cannot enumerate schedules or prove omitted properties.
- **Deterministic simulation versus physical realism:** simulation supports repeatable schedule exploration; real infrastructure adds kernels, networks, devices, providers, and humans that the simulator may omit.
- **Staging versus production:** staging permits stronger destructive faults; production supplies authentic scale and dependencies but raises customer, data, safety, and regulatory consequences.
- **Broad random injection versus targeted injection:** broad campaigns discover surprises; targeted campaigns attribute mechanisms and reproduce incidents more reliably.
- **Single-fault versus combined-fault coverage:** single faults isolate behavior; combinations expose latent interactions at rapidly increasing cost.
- **Steady workload versus adversarial workload:** steady load makes comparison easier; burst, skew, cold state, and large tenants expose capacity cliffs.
- **Automatic abort versus human incident command:** automation reacts quickly; humans interpret cross-domain harm. High-risk exercises generally need both with independent access.
- **Synthetic oracle versus business reconciliation:** synthetic checks are fast; durable business comparison catches ambiguous and cross-provider effects at higher cost and delay.
- **Frequent small experiments versus rare full exercises:** small tests limit exposure and regression time; full exercises reveal coordination, bootstrap, and capacity gaps.
- **Fail closed versus degraded service:** fail closed preserves some safety or security properties; bounded degraded service preserves availability but needs explicit authority, freshness, and reconciliation.
- **Statistical confidence versus consequence analysis:** repetition estimates rates under assumptions; hazard, adversarial, systematic, and common-cause reasoning addresses failures poorly represented by random samples.

## Failure Modes and Misconceptions

1. **“A process kill represents failure.”** It covers one crash shape, not delay, partition, corruption, exhaustion, stale authority, or common cause.
2. **“Chaos means random breakage.”** Useful experiments have hypotheses, controls, oracles, bounds, and learning goals.
3. **“Green health checks prove recovery.”** They may omit data, business, security, minority, and physical outcomes.
4. **“Staging passed, so production is safe.”** State, scale, topology, dependencies, access, and humans may differ.
5. **“Production testing is inherently stronger.”** Unsafe or poorly observable tests can produce harm and weak evidence.
6. **“Redundant regions are independent.”** They may share identity, deployment, DNS, software, operators, providers, or policy.
7. **“Traffic moved, so failover succeeded.”** Authority, data, capacity, unknown operations, and stale writers may still be wrong.
8. **“The queue protected us.”** It may have converted loss into lateness, expiry, unfairness, duplicates, or an unbounded recovery tail.
9. **“A cache kept availability.”** Stale or unauthorized answers can violate the useful-service contract.
10. **“No alerts means no impact.”** Telemetry may have failed, sampled away a cohort, or measured components rather than outcomes.
11. **“Zero failures means zero risk.”** Finite observations support only a bounded inference under explicit assumptions.
12. **“More fault cases always mean better coverage.”** Repeated low-consequence variants can leave critical boundaries untouched.
13. **“Rollback restores the past.”** Durable writes, external effects, schema changes, and compromised credentials may be irreversible.
14. **“Recovery time starts at detection.”** User harm can begin earlier; delayed detection belongs in the measurement.
15. **“Recovery ends when requests succeed.”** Backlog, ambiguity, security, data integrity, and customer repair may remain.
16. **“The injector’s success message confirms the fault.”** Independent observation must verify target and effect.
17. **“Game days replace incident readiness.”** Announced exercises may not test surprise, fatigue, access loss, or malicious action.
18. **“A passing experiment approves residual risk.”** Technical evidence informs the accountable decision; it does not own safety, legal, security, or business acceptance.

## Worked Examples

### Example 1

**Turn “highly available” into claims.**

**Situation.** A team says its document service remains highly available if a zone fails.

**Reasoning.** The phrase lacks user, operation, load, correctness, and time. The team replaces it with: at 4,000 reads/s and 400 writes/s, loss of any one application zone for 20 minutes allows at least 99% of admitted reads within 500 ms, rejects rather than acknowledges writes without current quorum, loses no acknowledged write, and restores normal routing within 10 minutes after the zone returns. Separate oracles check latency, acknowledgement history, quorum authority, durable state, and restoration.

**Conclusion.** A measurable claim can fail informatively; “highly available” cannot.

### Example 2

**Find a hidden common cause.**

**Situation.** Two regional stacks are presented as independent because their compute and databases are separate.

**Reasoning.** The dependency map shows both validate tokens through one global identity service, obtain routing from one control plane, consume artifacts from one registry, and receive simultaneous configuration from one pipeline. Loss or corruption of any shared dependency can disable both stacks. The campaign adds identity unavailability, stale cached keys, control-plane partition, registry loss during cold bootstrap, and a bad global configuration. It also separates rollout cohorts and provides scoped emergency credentials.

**Conclusion.** Geographic duplication did not establish failure independence; the control and identity graph determined the real cut sets.

### Example 3

**Evaluate quorum loss without corrupting authority.**

**Situation.** A five-member metadata service requires three votes. A partition leaves groups of three and two.

**Reasoning.** The campaign writes unique values before and during partition, verifies only the three-member side can commit, and confirms the two-member side rejects writes while it may serve explicitly bounded stale reads. It then partitions the old leader from a majority, promotes a new leader, and reconnects the old one. Epoch fencing must reject stale writes. History and replica state are checked after convergence.

**Conclusion.** Availability on the majority side is acceptable only with preserved single authority and explicit minority behavior.

### Example 4

**Expose multiplicative retries.**

**Situation.** A client, gateway, service, and database adapter each permit three attempts after a slow dependency.

**Reasoning.** One logical request can cause up to $3^4=81$ downstream attempts if layers multiply independently. Injecting delay rather than refusal keeps attempts in flight and consumes pools. The corrected design creates one request identity, propagates one deadline and attempt budget, assigns retry ownership to the layer with business context, uses jitter, and applies admission and bulkheads. The oracle counts attempts and business effects per identity.

**Conclusion.** Restart success is irrelevant if retry feedback exhausts the healthy system; the experiment must observe work amplification.

### Example 5

**Reject a false queue recovery.**

**Situation.** An ingestion queue receives 900 events/s. During consumer degradation it serves 300/s for 15 minutes; afterward capacity is 1,200/s while arrivals remain 900/s.

**Reasoning.** Backlog growth is $(900-300)\cdot900=540{,}000$ events. Net recovery is $1{,}200-900=300$ events/s, so ideal clearance takes $540{,}000/300=1{,}800$ seconds, or 30 minutes. The oracle also checks oldest age, expiry, duplicates, poison records, tenant fairness, and downstream outcomes. If a 20-minute freshness contract applies, added capacity or shedding is required; eventual drain does not pass.

**Conclusion.** Queue depth and service recovery must be evaluated against time and business validity, not eventual emptiness.

### Example 6

**Measure recovery from impact to reconciliation.**

**Situation.** A regional payment failover starts at 10:06, although customer timeouts began at 10:00. Routing succeeds at 10:10, ordinary requests meet latency at 10:14, and ambiguous captures reconcile at 10:42.

**Reasoning.** If the claim is useful payment service with reconciled outcomes, $t_b=10{:}00$ and $t_v=10{:}42$, so $T_{rec}=42$ minutes. Detection took 6 minutes, routing finished after 10, serving stabilized after 14, and reconciliation consumed the remaining 28. Reporting a four-minute failover from decision to route change hides most customer and integrity impact.

**Conclusion.** Recovery boundaries must follow the promised outcome, not the most flattering infrastructure milestone.

### Example 7

**Detect a broken observer.**

**Situation.** During a zone isolation experiment, dashboards show zero errors and the injector reports successful network rules.

**Reasoning.** Tenant probes outside the zone report timeouts, while tracing and metrics exporters inside the zone cannot reach their collector. Missing series were rendered as zero. An external traffic ledger shows 8% of requests had no terminal outcome. The evaluation fails both observability and service claims. The remedy distinguishes absent from zero, adds external probes and durable request accounting, and independently confirms network effects.

**Conclusion.** An experiment without an independent oracle can mistake observer failure for resilience.

### Example 8

**Interpret zero observed failures.**

**Situation.** A controlled failover passes 300 times with no lost acknowledged writes, and a report claims the loss probability is zero.

**Reasoning.** Under identical independent Bernoulli trials, the rough 95% rule-of-three upper bound is $3/300=0.01$, or 1%. Even that bound may not apply because trials reuse code, topology, operators, state distributions, and recovery mechanisms. Systematic bugs, common causes, and untested schedules are not sampled independently. Report 0 failures in 300 recorded cases and the case distribution, not zero probability.

**Conclusion.** Repetition strengthens bounded evidence but cannot justify certainty or erase model limitations.

### Example 9

**Bound a production experiment.**

**Situation.** A marketplace wants to test loss of its recommendation dependency during a sales event.

**Reasoning.** The architecture allows a stale, age-labeled fallback but checkout must remain independent. The experiment begins at 0.5% of sessions, excludes regulated and vulnerable cohorts, caps duration at five minutes, and stops on checkout error, latency, or fallback-age thresholds. A separate operations path can restore routing. Observers compare recommendations, checkout completion, resource saturation, and cohort impact. The exercise does not inject payment or identity faults during peak commerce.

**Conclusion.** Progressive exposure and explicit exclusions produce useful evidence without pretending every high-consequence fault belongs in production.

### Example 10

**Evaluate an edge safety architecture.**

**Situation.** A water-treatment site uses local interlocks, an edge controller, regional supervision, and a cloud optimizer. The team proposes disconnecting the site uplink.

**Reasoning.** The claim says local chemical and pressure invariants remain enforced for four isolated hours, cloud commands expire, operators retain authenticated bounded control, audit storage does not fill, and reconnection cannot replay stale actuation. The exercise first uses simulation and hardware-in-the-loop; physical injection requires safety authority. Oracles include independent sensors, controller epochs, command logs, buffer age, operator actions, and water-quality measurements. Recovery includes physical reconciliation, not only message drain.

**Conclusion.** Distributed failure evaluation must extend to physical state and accountable authority when software controls consequential processes.

## Cross-Program Connections

- **Software Delivery and Reliability Engineering:** owns SLOs, incident response, game days, recovery practice, and production experiment operations.
- **Software Testing and Quality Engineering:** owns test design, oracles, coverage, property testing, mutation, reproducibility, and defect analysis.
- **Distributed Systems Engineering:** owns formal failure models, consensus, replication, histories, safety, liveness, and model checking.
- **Systems Engineering:** owns hazards, FMEA, fault trees, physical consequences, assurance arguments, and accountable acceptance.
- **Security Engineering:** owns threat models, adversarial tests, privilege, credential failure, break-glass control, and compromise recovery.
- **Platform Engineering:** owns injection mechanisms, workload isolation, topology controls, telemetry substrate, and safe automation.
- **Database Engineering:** owns transaction, replication, backup, restore, corruption, durability, and history evidence.
- **API and Service Engineering:** owns deadline, retry, idempotency, pending-state, error, and client-visible contracts.
- **Network Engineering:** owns loss, delay, reorder, partition, congestion, routing, and network-fault measurement.
- **Data Architecture Engineering:** owns authority, lineage, retention, deletion, reconciliation, and cross-system data outcomes.

## References

1. Algirdas Avizienis, Jean-Claude Laprie, Brian Randell, and Carl Landwehr, “Basic Concepts and Taxonomy of Dependable and Secure Computing,” *IEEE Transactions on Dependable and Secure Computing* 1(1), 2004. <https://doi.org/10.1109/TDSC.2004.2>
2. Ali Basiri et al., “Chaos Engineering,” *IEEE Software* 33(3), 2016. <https://doi.org/10.1109/MS.2016.60>
3. Principles of Chaos Engineering, “Principles,” 2019 edition; retrieved 2026-09-06. <https://principlesofchaos.org/>
4. Maurice P. Herlihy and Jeannette M. Wing, “Linearizability: A Correctness Condition for Concurrent Objects,” *ACM Transactions on Programming Languages and Systems* 12(3), 1990. <https://doi.org/10.1145/78969.78972>
5. Jingyu Zhou et al., “FoundationDB: A Distributed Unbundled Transactional Key Value Store,” *Proceedings of SIGMOD 2021*. <https://doi.org/10.1145/3448016.3457559>
6. Peter Alvaro, Joshua Rosen, and Joseph M. Hellerstein, “Lineage-Driven Fault Injection,” *Proceedings of SIGMOD 2015*. <https://doi.org/10.1145/2723372.2723711>
7. Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds., *Site Reliability Engineering*, O'Reilly Media, 2016, especially “Testing for Reliability.” <https://sre.google/sre-book/testing-reliability/>
8. National Institute of Standards and Technology, *Developing Cyber-Resilient Systems: A Systems Security Engineering Approach*, NIST SP 800-160 Volume 2 Revision 1, December 2021. <https://doi.org/10.6028/NIST.SP.800-160v2r1>
9. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
10. Michael T. Nygard, *Release It!*, 2nd ed., Pragmatic Bookshelf, 2018.

## Exercises

### Exercise 1

Define fault, error, failure, failure model, steady-state hypothesis, failure scenario, safety property, liveness property, oracle, fault injection, chaos engineering, blast radius, containment, confounder, reconciliation, and evidence expiry.

### Exercise 2

A queue receives 1,500 requests/s. A dependency slowdown reduces service to 600/s for 12 minutes. After repair, sustainable service is 2,100/s while arrivals continue. Compute the ideal backlog and drain time. If the oldest-work objective is 15 minutes, explain why arithmetic alone cannot establish compliance.

### Exercise 3

Diagnose a “regional failover passed” report that starts its timer when operators click failover, observes only load-balancer health, uses new write identities on retry, shares one identity service between regions, stops when traffic moves, and discards failed-run logs. Design corrected claims, injection, oracles, authority, timing, and evidence.

### Exercise 4

Compare architecture review, formal modeling, deterministic simulation, isolated fault injection, staging game days, and bounded production experiments for a multi-region clinical records service. Allocate methods to consistency, security, capacity, recovery, and clinical workflow claims, and state the transfer limits.

### Exercise 5

Design a failure-evaluation campaign for an international emergency-notification platform using mobile networks, regional brokers, translation services, geospatial targeting, government authorities, and public alerts. Cover claims, common causes, combined faults, workloads, safety and liveness oracles, authority, retries, queues, degraded operation, security, progressive exposure, abort, recovery, reconciliation, evidence, and residual risk.

## Answers to the Exercises

### Answer 1

A **fault** is a hypothesized cause, an **error** an incorrect internal state, and a **failure** an externally visible service deviation. A **failure model** declares covered fault powers and conditions. A **steady-state hypothesis** names measured bounds expected during an experiment. A **failure scenario** specifies trigger, point, scope, timing, duration, workload, expected behavior, recovery, and evidence. A **safety property** forbids bad outcomes; a **liveness property** requires eventual good outcomes under assumptions. An **oracle** judges observations against a property. **Fault injection** deliberately creates or simulates a fault; **chaos engineering** uses controlled system experiments to build empirical failure evidence. **Blast radius** is exposed impact; **containment** limits propagation. A **confounder** offers another explanation for a result. **Reconciliation** resolves divergent or unknown durable outcomes. **Evidence expiry** is a material change that prevents unreviewed transfer of a result.

### Answer 2

Twelve minutes is 720 seconds. Backlog growth is $(1{,}500-600)\cdot720=648{,}000$ requests. After repair, net drain is $2{,}100-1{,}500=600$ requests/s, so ideal clearance takes $648{,}000/600=1{,}080$ seconds, or 18 minutes. The arithmetic assumes constant admitted rate, constant service, no retries, no priority classes, no poison work, no expiry, no downstream bottleneck, and no resource saturation. Oldest work already accrued delay during degradation, and new arrivals may affect scheduling. The campaign must measure age distribution and terminal business outcomes under the real policy; since ideal drain exceeds 15 minutes, unchanged capacity cannot justify the objective.

### Answer 3

Define claims from first customer impact: bounded correct reads, no lost acknowledged writes, one effect per business identity, current write authority only, explicit unknown outcomes, and reconciled service by a named deadline. Inject region isolation and shared-identity loss at recorded workload and state, including failure before commit, after commit before response, during promotion, and old-region restart. Preserve one request identity across retries.

Use external client probes, operation-history and durable-state checkers, authority epochs and fencing logs, identity-cache age, capacity and latency, unknown-effect records, and business reconciliation. Measure detection, decision, access, promotion, serving, backlog, and reconciliation from impact start. Test a separately scoped emergency identity path and reject privilege expansion. Retain successful, failed, aborted, and inconclusive runs with exact versions. Traffic movement is one observation; the verdict waits for integrity, authority, capacity, security, and reconciliation.

### Answer 4

Architecture review maps shared identity, key, DNS, deployment, state, operator, and recovery dependencies and finds missing containment. Formal modeling addresses record-version authority, quorum transitions, stale writers, and selected safety/liveness properties under an abstract failure model. Deterministic simulation explores message schedules, crashes, retries, and recovery using reproducible seeds if the implementation exposes controllable time and I/O. Isolated injection validates storage, identity, cache, and broker mechanisms without clinical exposure.

Staging game days exercise integrated topology, cold restore, access, runbooks, and staffing with synthetic governed data, but production scale and clinical workflow may differ. Bounded production experiments may validate safe read routing, capacity, and observer behavior for a small authorized cohort; they should not deliberately risk record corruption, confidentiality, or unsafe clinical decisions. Clinical workflow exercises need authorized representative staff and safety oversight. No method alone transfers across different schema, topology, population, threat, workload, or version; the evidence record names these expiry conditions.

### Answer 5

Claims include: authenticated current authorities can issue one alert intent; no unauthorized or superseded alert is sent; admitted urgent alerts reach a defined target proportion within jurisdiction-specific deadlines; inaccessible or untranslated cohorts are visible; retries do not duplicate public effects; and every unknown delivery reconciles to an accountable terminal state. Map common dependencies in identity, geospatial data, translation, DNS, time, carrier gateways, deployment, and emergency staffing. Scenarios combine regional broker loss with carrier congestion, translation delay with schema change, authority credential revocation with control-plane loss, and reconnect surges after mobile outage.

Use representative geography, language, accessibility needs, device age, peak emergency load, cold caches, and large jurisdictions. Safety oracles reject wrong geography, language, authority, epoch, content, and duplicate or stale alerts. Liveness oracles measure accepted-to-carrier and accepted-to-observed delivery under explicit carrier limits. One durable alert and recipient-batch identity spans retries; queues prioritize current life-safety alerts, bound age and bytes, expire superseded work, isolate poison translations, and expose non-delivery. Degraded mode permits locally authenticated pre-scoped authorities and approved templates, never anonymous privilege expansion.

Progress from review and simulation to provider sandboxes, isolated regional exercises, opt-in staff devices, and legally authorized public drills; do not experiment on real emergency messages without competent authority. Bound tenant, geography, recipient, duration, and send capability. Independent controls stop issuance and carriers suppress test namespaces. External probes, provider receipts, device observations, authority logs, content hashes, queue age, accessibility checks, operator actions, and public feedback form evidence. Recovery fences obsolete regions, reconciles batches and carrier receipts, cancels superseded alerts, communicates mistakes, and preserves audit. Residual risks include carrier black boxes, handset power, human interpretation, translation adequacy, compromised authorities, disasters affecting multiple providers, and populations absent from the sample; accountable public-safety, accessibility, privacy, security, carrier, and governmental owners must review them.
