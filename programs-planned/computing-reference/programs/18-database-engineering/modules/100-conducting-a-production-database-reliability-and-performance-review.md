---
module_id: DBE-100
program: Database Engineering
level: 2
module_number: 100
title: Conducting a Production Database Reliability and Performance Review
status: complete
last_verified: 2026-09-05
---

# Conducting a Production Database Reliability and Performance Review

## One-Page Review

### Governing question

How should an independent reviewer decide whether a production database is correct, durable, secure, performant, recoverable, operable, and adequately provisioned for its declared workload and failure model—without confusing a checklist, dashboard, or successful demonstration with proof?

### Essential definitions

- A **review charter** names the decision, system boundary, service contract, workload, threat and failure models, evidence period, stakeholders, and exclusions.
- A **claim** is a testable statement such as “acknowledged writes survive one-zone loss”; an **acceptance criterion** states the evidence required to accept it.
- An **evidence item** has provenance: source, time, environment, version, population, method, result, limitations, and owner.
- A **finding** is a gap between a required claim and evidence or behavior; an observation is not automatically a defect.
- A **risk** combines a scenario, precondition, consequence, likelihood or frequency evidence, exposure, controls, uncertainty, and owner.
- A **blocker** is a failed or unverified condition whose consequence exceeds the review's acceptance policy.
- **residual risk** remains after credited controls; accepting it is an accountable business and engineering decision, not a reviewer euphemism.
- A **performance envelope** is the measured workload and system-state region in which correctness and service objectives hold.

### Central model, mechanism, or theorem

Build a traceable argument:

$$
\text{requirement} \rightarrow \text{claim} \rightarrow \text{acceptance criterion} \rightarrow \text{evidence} \rightarrow \text{finding} \rightarrow \text{action or accepted residual risk}.
$$

Test the database as a stateful service across steady load, overload, maintenance, change, dependency loss, failover, restore, and recovery. A claim is accepted only within the versions, topology, workload, time, and failure scope actually supported by evidence. Unknown is a result, not a pass.

### Critical invariants

- the review's decision and scope are fixed before evidence selection, and exclusions remain visible;
- user-visible correctness, durability, freshness, availability, latency, and recovery claims have explicit populations and clocks;
- acknowledged operations reconcile with committed state across retry, timeout, failover, and restore;
- performance comparisons hold workload, data, cache, topology, configuration, and measurement boundaries sufficiently constant;
- capacity includes skew, maintenance, growth, repair, rebuild, backup, and the declared failure state;
- security evidence covers identity, least privilege, secrets, network path, encryption, patching, audit, and privileged operations;
- every finding cites reproducible evidence, a violated criterion, consequence, owner, deadline, and verification method;
- waivers identify accountable acceptors, expiry, compensating controls, and residual risk.

### Common failures

- reviewing “the database” without application, client, replication, backup, and operator boundaries;
- letting available dashboards determine the questions instead of starting from claims;
- sampling a quiet hour and generalizing to peak, skew, maintenance, or failure;
- declaring availability from process uptime while requests are wrong, stale, rejected, or timed out;
- benchmarking queries without correctness checks, production data shape, or offered-load accounting;
- treating backup success, replica presence, or failover automation as restore evidence;
- multiplying ordinal severity labels into a pseudo-precise risk score;
- burying unknowns and assumptions in prose or converting missing evidence into “low risk”;
- producing a long issue list without decision gates, ownership, sequencing, or retest criteria;
- allowing the reviewed team to alter evidence after the fact without preserving provenance.

### Compact example

A service promises 99.95% monthly successful writes and zero loss of acknowledged writes after one-zone failure. Thirty days contain 43,200 minutes, so the availability budget is $0.0005\times43{,}200=21.6$ minutes. Monitoring shows 18 minutes of failed writes, leaving 3.6 minutes, but the latest failover test cannot reconcile 37 timed-out operations and the restore drill used an unverified backup. Availability is within budget; durability and recoverability are not demonstrated. The decision is not “green average”: failover/restore are blockers until histories reconcile and a representative restore passes.

### Connections

This review integrates the whole program: [ACID and Transaction Boundaries](041-acid-and-transaction-boundaries.md), [Failure Models](071-failure-models.md), [Point-in-Time Recovery and Restore Verification](080-point-in-time-recovery-and-restore-verification.md), [Evaluating Consistency, Latency, and Availability Trade-Offs](090-evaluating-consistency-latency-and-availability-trade-offs.md), [Database Observability and Capacity](098-database-observability-and-capacity.md), and [Online Schema and Version Upgrades](099-online-schema-and-version-upgrades.md). It is the program terminus; successor work is repeated review after material change and remediation.

## Governing Question

A database can answer test queries, show healthy CPU, maintain replicas, and complete scheduled backups while still being unsafe. The application may acknowledge before the declared durability point. A failover may lose a committed prefix. A restore may exceed its objective or omit keys. One tenant may dominate p99 while fleet averages look good. An administrator role may bypass application controls. A schema migration may consume the capacity reserved for repair.

The reviewer must make a bounded decision from incomplete evidence. That requires more than technical breadth: it requires disciplined claim construction, reproducible sampling, adversarial testing, explicit uncertainty, fair prioritization, and ownership. The output is an argument that another qualified person can challenge and reproduce—not a certificate of universal correctness.

## Why This Matters

Production databases concentrate persistent business state behind concurrency, caches, logs, indexes, replicas, queues, automation, and human procedures. A defect can be latent for months and become visible only during overload, operator error, corruption, restore, topology change, or a rare transaction interleaving. Performance and reliability are coupled: saturation causes timeouts and retries; retries amplify load; maintenance debt threatens recovery; aggressive tuning can weaken durability.

A strong review changes decisions. It can block an unsafe launch, bound a risky migration, direct scarce capacity, expose a false recovery assumption, or retire a recurring incident mechanism. A weak review merely creates compliance theater. Checklist completion is useful for coverage, but only evidence tied to concrete claims supports acceptance.

The review also protects epistemic integrity. It separates “observed in this test,” “inferred under named assumptions,” “documented by a product,” and “unknown.” This prevents local success from becoming an unearned global guarantee.

## Prerequisites and Retrieval

Retrieve database transaction semantics, isolation and anomaly models, write-ahead logging, checkpoints, crash recovery, backup and point-in-time recovery, physical and logical replication, quorum or synchronous acknowledgement, failover, sharding, query plans, cardinality estimates, indexing, locks, MVCC maintenance, compaction, schema change, and capacity envelopes.

Retrieve service-level indicators and objectives, error budgets, percentiles, offered versus completed load, open- and closed-loop generation, coordinated omission, Little's law, failure injection, canaries, incident command, and blameless postmortems. Retrieve threat modeling, least privilege, secret rotation, audit logging, encryption boundaries, supply-chain/version inventory, and vulnerability remediation.

Before the review, request architecture and data-flow diagrams; ownership and escalation; data classification; service and durability contracts; workload traces; schema and index inventory; configuration and version history; topology and failure domains; dependency map; SLO reports; incident/postmortem history; capacity forecasts; query and wait evidence; backup catalog and restore records; change history; access grants; runbooks; and unresolved risk acceptances. Missing evidence becomes an explicit finding or limitation.

## Learning Objectives

After completing this module, you should be able to:

1. write a review charter that fixes decision, boundary, claims, evidence period, and exclusions;
2. translate reliability, correctness, security, performance, capacity, and recovery requirements into testable acceptance criteria;
3. construct an evidence inventory with provenance, scope, confidence, and limitations;
4. design representative measurements and adversarial experiments without harming production;
5. reconcile client histories with database, replication, failover, and restore state;
6. distinguish causal findings from correlations and missing evidence;
7. prioritize risk without false numerical precision and identify non-negotiable blockers;
8. produce an actionable decision record with owners, deadlines, retest methods, waivers, and follow-up cadence.

## Core Exposition

**Charter the decision.** Begin with the exact decision: launch, ownership transfer, capacity approval, migration, version upgrade, incident follow-up, periodic assurance, or remediation closure. Name the accountable decision maker and reviewers. A review for a low-criticality internal cache cannot silently inherit the same requirements as a ledger, nor can a ledger lower requirements because evidence is inconvenient.

Define the system boundary from client intent to durable state and back: application libraries, connection pools, proxies, primary/leader, replicas, consensus or log transport, storage, key management, backup repository, restore environment, observability, automation, and operators. Name shared services and control planes. Draw trust and failure boundaries, not merely boxes.

Fix the review interval and versions. Configuration, schema, code, statistics, data distribution, topology, and workload change. Evidence from a previous major version or a pre-sharding topology may be historical context but cannot directly prove the current claim.

**Write the service contract before inspecting dashboards.** Define eligible operations and what success means: correct result, allowed staleness, transaction outcome, durability point, deadline, and acknowledgement semantics. State consistency per operation rather than calling the database “strong” or “eventual.” State RPO and RTO per incident class, not one slogan for all failures.

Use a claim matrix. Each row contains requirement, claim, scope, acceptance criterion, evidence method, evidence owner, status, limitation, and linked finding. Example: “For valid writes acknowledged success, loss is zero after failure of any one declared zone; verify by tagged client history, forced loss of the active zone, convergence, and exact post-failover reconciliation in the production-equivalent topology.”

**Classify evidence.** Direct reproduced evidence is usually stronger than an undocumented assertion, but method determines strength. Useful classes are current controlled experiment, production observation, artifact inspection, configuration proof, code/design review, vendor or standards documentation, historical incident, and expert judgment. Record who collected it, when, exact commands or queries, environment, sampling, raw artifact, transformation, result, and limitations.

Evidence can be valid yet insufficient. A successful restore proves that one backup restored in one environment at one time. It does not prove every backup, current retention, all encryption keys, target RTO, application semantics, or disaster access. Preserve negative and inconclusive results; do not rerun until passing and discard failures.

**Sample by risk, not convenience.** Include peak and quiet intervals, hot and ordinary tenants, large and small tables, common and expensive query families, read/write transactions, early and late retention, primary and replicas, each failure domain, maintenance, deployment, backup, restore, and overload. Use random or systematic sampling where population inference is intended, and targeted adversarial cases where rare high-consequence mechanisms matter.

A risk-based sample cannot establish absence of all defects. Report the exact population, selection method, coverage, and blind spots. Expand the sample when one failure suggests a class: one stale replica result should trigger investigation of lag, routing, session guarantees, and other replicas, not a local exception.

**Review data correctness first.** Inventory domain invariants, keys, constraints, null/default semantics, units, time zones, collation, encoding, lifecycle/retention, derived data, and reconciliation totals. Determine which invariants the database enforces, which applications enforce, and which no component owns. Inspect constraint validity, disabled checks, orphaned rows, duplicate identities, impossible state transitions, and silent truncation/coercion.

For transactional claims, use histories containing invocation, response, operation identity, arguments, result, client/session, and time bounds. Unknown outcomes after timeout are not failures safe to retry unless idempotency or conditional semantics establish it. Compare accepted acknowledgements with primary, replica, failover, and restored states. A row-count match can coexist with wrong values or missing relationships.

**Review durability and recovery as mechanisms.** Trace a write from application acknowledgement through transaction commit, log append/flush, replication acknowledgement, storage guarantees, and backup inclusion. Confirm exact sync modes, quorum membership, failure correlations, write-cache behavior, and unsafe overrides. Product documentation explains mechanisms; current configuration and experiments establish deployment evidence.

Inventory backups by type, base, incrementals/log segments, checksums, encryption key, retention, immutability/access, region/failure domain, catalog, and restoration dependency. Perform restore drills into an isolated environment, verify chain completeness and target selection, then run logical checks, application reads, permissions, jobs, and performance smoke tests. Measure RPO from recoverable state, and RTO from declared incident start through usable service—not only file copy.

**Review replication and failover.** Map source and apply positions, acknowledgement quorum, lag coordinates, conflict behavior, replication slots/log retention, fencing, leader election, routing, and read policies. Test process, node, storage, network, zone, and control-plane failures that are within scope. Ensure a stale primary cannot resume writes after a new authority is elected.

Failover success means more than role transition. Reconcile acknowledged and unknown client operations, verify uniqueness and monotonic/domain invariants, observe recovery debt and performance, exercise failback or document its absence, and ensure operators can diagnose split authority. Repeat with a degraded or rebuilding member if the contract promises that state.

**Review performance from user outcome to mechanism.** Establish baseline workload dimensions: offered rate by class, concurrency, transaction size, key/tenant skew, parameter/selectivity classes, rows/bytes, data and working-set size, read/write mix, result size, cache state, maintenance, topology, and dependency behavior. Measure correct completions, rejections, retries, timeouts, aborts, unknowns, latency distributions, queueing, and recovery after overload.

Compare like with like. A faster query returning fewer rows or weaker consistency is not an improvement. Fleet p99 is not the average of host p99 values. A closed-loop generator can under-report a stall because it stops offering work. Preserve raw distributions and client perspective; correlate with server waits and resource saturation.

Inspect normalized query families by total time, frequency, tail latency, errors, rows, buffers/I/O, temporary spill, WAL/log bytes, locks, and plan variants. Use execution plans with exact product semantics: some analysis commands execute statements and can mutate data. Compare estimates to actuals, bind classes, statistics, indexes, cache, memory, parallelism, version, and configuration. A plan is a hypothesis about mechanism, not the whole diagnosis.

**Review capacity as a failure-aware envelope.** Inventory CPU/core, memory and concurrency multiplication, local and remote storage, IOPS/bandwidth/latency, network, connections/threads, locks, log/WAL retention, replicas, backup, compaction/vacuum, repair, rebuild, schema/index migration, and observability overhead. Model skew and placement, not fleet average.

For a stable boundary, Little's law $L=\lambda W$ can check concurrency accounting. For $n$ equal nodes serving total load $X$, normal mean is $X/n$; after losing one, ideal mean is $X/(n-1)$ before skew and recovery overhead. This is a lower-bound planning calculation, not proof of N+1 capacity. Test the degraded topology until correctness, SLO, debt-drain, and free-space criteria hold.

Forecast using mechanisms—customers, events, bytes, retention, replicas, indexes, amplification—and uncertainty ranges. Include intervention lead time. A forecast that crosses a threshold in 60 days is already late if procurement, migration, and verification require 90.

**Review security and privacy as database behavior.** Map identities from human, workload, automation, replica, backup, monitoring, and break-glass access to exact grants and trust paths. Verify least privilege, separation of duties, credential storage/rotation/revocation, network restrictions, TLS and certificate validation, encryption/key access, patch/version posture, audit coverage, and sensitive telemetry handling.

Test representative denials as well as allowed paths. Confirm an application cannot create roles, bypass tenant filters, read system secrets, or alter audit policy unless explicitly required. Review stored procedures, extensions/plugins, user-defined code, database links, imports/exports, file access, and backup readers. Audit trails need protected time, identity, retention, access, and alerting; presence of log files is not accountability.

**Review operations and change.** Inspect on-call ownership, escalation, dependency contacts, dashboards, SLO alerts, runbooks, access under emergency, safe automation, maintenance schedules, deployment/schema protocol, feature gates, rollback limits, incident roles, and postmortem actions. Run a tabletop and at least one bounded technical exercise for high-consequence procedures.

Automation should be idempotent where possible, bounded, observable, cancellable, and protected by preconditions. Review commands for blast radius and unsafe defaults. A runbook that assumes the primary is reachable, credentials are available, or the backup catalog is intact may fail in the incident it claims to address.

Inspect incidents and near misses for recurring mechanisms, detection gaps, time to mitigate, confusing ownership, risky interventions, and overdue actions. Use blameless analysis to improve system and decision conditions. “Human error” ends inquiry too early; ask how permissions, interfaces, reviews, automation, feedback, and recovery shaped the action.

**Construct findings from criteria.** A defensible finding states: required claim; observed evidence; gap; scenario and consequence; affected population; likelihood/frequency evidence; existing and compensating controls; uncertainty; recommended action; owner; deadline; verification; and dependencies. Attach immutable or digest-bound evidence where possible.

Separate defect, risk, missing evidence, improvement, and accepted design trade-off. Do not label a product-specific difference a defect when the contract permits it. Conversely, do not downgrade missing recovery evidence because no outage has yet occurred.

**Prioritize without numerology.** Use explicit consequence categories and likelihood/frequency evidence with definitions. Quantitative expected loss $E=\sum_i p_iL_i$ is meaningful only when $p_i$ is a calibrated probability over a named interval and $L_i$ uses comparable consequence units; correlated scenarios cannot be summed as independent. Multiplying labels such as “3 × 4” creates an ordering convention, not quantitative risk.

Safety, legal, data-loss, or existential constraints may override expected-value ranking. Preserve confidence and urgency separately. A catastrophic unknown with no recovery evidence can be a blocker even if observed frequency is zero. The finite fixture below tests deterministic review triage; its ranks are policy orderings, not measured risk magnitudes.

<!-- bijux-verify: {"id":"finite-review-triage","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"decision=not_ready\nordered=R1,R2,R3,R4\nblockers=R1\nunknowns=R3\nall_owned=true\nall_have_retest=true\nevidence=finite_review_triage\n","stderr":""}} -->
```python
impact_rank = {"low": 1, "moderate": 2, "major": 3, "catastrophic": 4}
findings = [
    {"id": "R3", "impact": "major", "evidence": "unknown", "blocker": False,
     "owner": "capacity", "retest": "degraded load test"},
    {"id": "R1", "impact": "catastrophic", "evidence": "failed", "blocker": True,
     "owner": "recovery", "retest": "restore and reconcile"},
    {"id": "R4", "impact": "low", "evidence": "observed", "blocker": False,
     "owner": "observability", "retest": "audit query"},
    {"id": "R2", "impact": "major", "evidence": "failed", "blocker": False,
     "owner": "performance", "retest": "production-shaped benchmark"},
]

ordered = sorted(findings, key=lambda finding: (
    not finding["blocker"],
    -impact_rank[finding["impact"]],
    finding["id"],
))
blockers = [finding["id"] for finding in findings if finding["blocker"]]
unknowns = [finding["id"] for finding in findings if finding["evidence"] == "unknown"]
print(f"decision={'not_ready' if blockers else 'ready_with_constraints'}")
print("ordered=" + ",".join(finding["id"] for finding in ordered))
print("blockers=" + ",".join(sorted(blockers)))
print("unknowns=" + ",".join(sorted(unknowns)))
print(f"all_owned={str(all(f['owner'] for f in findings)).lower()}")
print(f"all_have_retest={str(all(f['retest'] for f in findings)).lower()}")
print("evidence=finite_review_triage")
```

**Make the decision explicit.** Useful dispositions are ready within scope, ready with binding constraints, or not ready. “Ready with constraints” names load, topology, feature, tenant, duration, and monitoring limits plus automatic or human enforcement. It is not a place to hide blockers.

For every blocker, specify the smallest sufficient closure evidence. For non-blocking findings, specify risk owner and due date. A waiver records reason, residual consequence, compensating control, accountable accepter, expiry, and triggers for immediate re-review. Reviewers advise; accountable owners accept business risk.

**Retest and maintain the argument.** Verify remediation against the original criterion and check regression elsewhere. Preserve before/after evidence. Reopen after material workload, data, schema, engine, topology, durability, security, backup, or ownership change. Periodic reviews should focus on changed claims and expiring evidence while retaining full traceability.

The final report includes executive decision, scope and exclusions, architecture/failure boundaries, claim matrix, methods and exact samples, evidence inventory, findings/risk register, blockers, remediation plan, waivers, retest results, and limitations. It names every claim that remains unknown and never claims external assurance that did not occur.

## Definitions and Notation

Let $O$ be the set of eligible offered operations during review interval $T$. Partition their observed outcomes into correct-within-deadline $C$, explicit failure $F$, rejected $J$, timed out or unknown $U$, and still in flight $I$, using one declared accounting boundary. Reconciliation requires $O=C\cup F\cup J\cup U\cup I$ with disjoint categories at the measurement instant.

Let $A=|C|/|O|$ be one possible availability SLI when the contract defines those sets that way. This formula is not universal: eligibility, invalid requests, canceled work, retry attempts, staleness, and deadline semantics must be declared. An objective $A_{slo}$ over window length $W$ permits unavailable-time equivalent $(1-A_{slo})W$ only under the chosen time-based interpretation.

For recovery event $e$, let $t_f$ be the declared failure time, $t_r$ the time usable verified service resumes, $s_f$ the last required state before failure, and $s_r$ the newest verified recovered state. $RTO_e=t_r-t_f$. RPO is an application-state distance between $s_f$ and $s_r$; expressing it as wall-clock duration is valid only when state time and clocks make that mapping meaningful.

Let workload vector $w=(\lambda, k, d, q, z, m)$ represent offered rate, concurrency, data/working-set shape, query/transaction mix, skew, and maintenance/failure state. The accepted performance envelope $P$ is the measured set of $w$ for which correctness and SLO predicates both hold. One maximum throughput is not $P$.

For finding $i$, $p_i$ is a calibrated probability over a named interval, $L_i$ is consequence in a comparable unit, and $p_iL_i$ is expected loss only under that model. Ordinal likelihood and impact categories remain categories. Let $Q_i\in\{\text{observed},\text{reproduced},\text{inferred},\text{unknown}\}$ record evidence state separately from consequence.

## Mechanisms, Invariants, or Proof Structure

**Argument structure.** For each requirement $R_j$, define a falsifiable claim $C_j$, acceptance predicate $K_j(E_j)$ over evidence $E_j$, and scope $S_j$. Acceptance is justified only if evidence provenance is valid, $K_j$ holds, and no counterevidence within $S_j$ remains unresolved. This is an assurance argument, not a mathematical proof that untested executions are safe.

**Completeness invariant.** Every in-scope requirement maps to at least one claim; every claim maps to criteria and evidence; every failed or unknown criterion maps to a finding or visible limitation; every finding maps to an owner and disposition. Traceability prevents attractive measurements from crowding out unmeasured obligations.

**Outcome-reconciliation invariant.** Client intent and responses are joined to database commit identities, replication positions, and recovered state. Duplicate retries are distinguished from logical operations. A timeout remains unknown until a read, idempotency key, transaction identifier, or other valid mechanism resolves it.

**Comparability invariant.** A performance delta is attributed only after checking versions, configuration, schema/statistics, dataset/distribution, workload generator, arrival process, cache, topology, maintenance, dependencies, and measurement pipeline. Remaining differences are named as confounders. Correlation can motivate a controlled intervention but does not by itself establish cause.

**Failure-closure invariant.** A failure experiment ends only after authority is unique, required state reconciles, service meets the degraded objective, repair/rebuild debt converges, alerts/runbooks work, and the system returns to a supported state. Stopping when a health check turns green hides recovery risk.

**Recovery proof obligation.** Backup creation plus checksums supports existence and transport integrity. Restore execution supports readability. Application and history reconciliation support semantic recovery. Timed end-to-end exercise supports RTO. Only their conjunction under the declared scenario supports the recovery claim.

**Finding-closure invariant.** Closure evidence addresses the original violated criterion in the relevant scope, not merely the implementation ticket. If an index is added for a latency finding, closure requires representative correct-query performance and regression checks, not existence of the index.

## Alternatives and Trade-Offs

**Comprehensive review versus targeted review.** A comprehensive review provides broad coverage but costs time and can dilute attention. A targeted review around migration, recovery, or performance goes deeper but must not imply assurance outside its charter. Use periodic broad review plus event-triggered targeted reviews for critical systems.

**Checklist versus claim-based argument.** Checklists improve recall and consistency. They become theater when every item has equal weight or “present” substitutes for “works.” Use a checklist to seed claims, then demand system-specific criteria and evidence.

**Production observation versus controlled test.** Production contains authentic scale and interactions but weak control and safety limits. Staging permits faults and repeatability but may not reproduce data, load, topology, or dependencies. Combine bounded production canaries and observations with production-equivalent experiments, and state the gap.

**Black-box versus white-box evidence.** Client histories measure the contract; database internals expose mechanism. Black-box evidence can show a violation without its cause. White-box health can look perfect while clients fail. Require both for important claims.

**Quantitative versus categorical prioritization.** Calibrated frequencies, money, time, and data-loss counts enable expected-value comparisons. Sparse catastrophic events and incomparable harms resist precise estimates. Use ranges and sensitivity analysis where data permits; otherwise use defined categories, confidence, and policy overrides without pretending arithmetic precision.

**Reviewer independence versus embedded expertise.** Independent reviewers challenge assumptions and incentives; embedded operators know hidden context. Pair them, require evidence provenance, record disagreements, and keep risk acceptance with the accountable owner rather than either reviewer alone.

**One-time certification versus continuous assurance.** A point review creates a clear gate but decays immediately as the system changes. Automated controls and recurring evidence improve currency but can institutionalize bad criteria. Maintain traceability, expiry, periodic adversarial review, and change-triggered reopening.

## Failure Modes and Misconceptions

**“The managed service owns reliability.”** A provider may own hardware, replication, or control-plane mechanisms. The customer still owns schema, workload, query behavior, access, application retry semantics, recovery requirements, configuration, and many failure interactions. Map responsibility explicitly.

**“Three replicas mean no data loss.”** Replica count says nothing about acknowledgement quorum, synchronization, placement correlation, lag, corruption propagation, fencing, or backup. Trace and test the write path.

**“Backups are green.”** A scheduled job can succeed while capturing the wrong database, omitting logs, using expired keys, exceeding RPO, or producing a restore too slow for RTO. Only representative restore and semantic validation support recovery.

**“CPU is low, so capacity is safe.”** One hot shard, serialized lock, storage tail, connection queue, log retention, memory multiplier, or rebuild can fail at low fleet average. Capacity is a multidimensional degraded-state envelope.

**“The p99 improved.”** Population, aggregation, timeout censoring, query mix, and correctness may have changed. Compare raw compatible distributions and outcomes by meaningful class.

**“No incidents means low risk.”** Detection may be absent, exposure may be recent, and catastrophic scenarios may be rare. Incident absence is evidence about an observed interval, not proof of safety.

**“A high risk score proves priority.”** Ordinal multiplication embeds arbitrary spacing and can hide catastrophic blockers. Show scenario, consequence, evidence, uncertainty, controls, and policy decision.

**“Unknown is neutral.”** Unknown recovery, durability, or authorization behavior can itself violate readiness criteria. Missing evidence must stay visible and may block by policy.

**“The reviewer owns remediation risk.”** Reviewers own method and honest reporting. System and business owners own implementation and residual-risk acceptance, with named accountability.

**“Passing once closes the matter.”** Evidence expires with material change and with time. Retest after remediation and reopen when workload, data, topology, version, schema, dependencies, or operators change.

## Worked Examples

### Example 1

**Situation.** A team asks for a “database health review” before launch but supplies no service contract.

The reviewer converts the request into a decision charter: launch at 5,000 offered writes/s and 20,000 reads/s; correctness includes unique order IDs and monotonic order states; acknowledged writes have zero-loss requirement for one-zone failure; reads allow five seconds of staleness; write p99 is 150 ms; RTO is 20 minutes; 90-day growth and N+1 repair are in scope. Client, proxy, database, replicas, backups, keys, and on-call are inside the boundary. Cross-region catastrophe is explicitly excluded and recorded as residual risk.

**Conclusion.** Scope and claims make “healthy” falsifiable and keep exclusions visible.

### Example 2

**Situation.** A 30-day service has a 99.95% time-based availability objective and used 18 minutes of equivalent unavailability.

The window is $30\times24\times60=43{,}200$ minutes. Budget is $(1-0.9995)\times43{,}200=21.6$ minutes. Remaining budget is $21.6-18=3.6$ minutes, or one sixth of the original. This arithmetic assumes the organization's time-equivalent SLI; request-based availability needs eligible-request counts instead. It says nothing about durability or correctness.

**Conclusion.** The service is within this availability budget but has little margin; other claims require separate evidence.

### Example 3

**Situation.** Backups report 100% success. The contract requires RPO 5 minutes and RTO 60 minutes after accidental deletion.

Select a backup chain and target point without privileging the newest known-good copy. Restore into isolated infrastructure using disaster credentials, logs, keys, and catalog. Start the timer at incident declaration; replay to a point before deletion; run schema, constraints, checksums, business totals, sampled records, permissions, and application probes. The drill reaches usable verified service in 74 minutes and newest recovered state is 3 minutes before deletion.

**Conclusion.** RPO passes, RTO fails; green backup jobs do not override the measured recovery finding.

### Example 4

**Situation.** An engine upgrade improves fleet mean latency 12%, but checkout p99 doubles.

Stratify by operation and bind/selectivity class. The checkout query changed from an indexed lookup to a scan for large merchants because statistics and a generic cached plan misestimate cardinality. Compare correct results, plan variants, estimates/actual rows, buffers, cache state, and waits under the same workload. A representative canary with refreshed statistics and controlled plan policy restores p99 without changing semantics.

**Conclusion.** Aggregate improvement cannot accept a critical-class regression; evidence identifies a reversible mechanism and retest.

### Example 5

**Situation.** Four nodes serve 6,000 requests/s. Each is tested to 1,850 requests/s under normal conditions, and the team claims N+1 capacity.

Normal ideal mean is $6{,}000/4=1{,}500$ requests/s. After one loss it is $6{,}000/3=2{,}000$ before leader skew, cold cache, repair, and control-plane overhead. The tested 1,850 is already short by 150 per remaining node. The review also requires debt-drain and correctness under failure.

**Conclusion.** Normal 81% of tested throughput is not N+1 headroom; degraded capacity is a blocker at this load.

### Example 6

**Situation.** The application role has `SELECT`, `INSERT`, `UPDATE`, and `DELETE` on its schema plus role creation “for deployment convenience.”

Trace actual deployment and runtime operations. Migrations use a separate short-lived identity; runtime never creates roles. Remove role administration, restrict network origin, rotate credentials, test allowed statements, and verify denial of role creation, cross-tenant reads, audit-policy changes, file export, and access to system secrets. Record emergency elevation separately with approval and audit.

**Conclusion.** Least privilege is demonstrated by required successes and forbidden failures, not a grant list alone.

### Example 7

**Situation.** A zone-failover drill reports success, but 37 client writes timed out around election.

Join idempotency keys and transaction identifiers to old leader log, quorum commit positions, new leader state, and client responses. Classify each timeout as committed once, not committed, or unresolved; replay only under idempotent/conditional semantics. Fence the old leader and verify acknowledged writes, uniqueness, balances, and sequence invariants after convergence. If any acknowledged write is absent or a timeout remains unresolved under a zero-ambiguity criterion, the durability claim fails.

**Conclusion.** A promoted replica is not sufficient evidence; client-history reconciliation closes the claim.

### Example 8

**Situation.** An online schema migration passed row-count comparison and is ready to drop the old column.

Review old/new readers and writers, backfill source-version predicates, null/default/type semantics, change-capture frontier, invalid rows, index/constraint validity, replica lag, backups, rollback, capacity, and stale connection pools. A retired batch writer still writes only the old column, so row counts match while new values can be null.

**Conclusion.** Contraction is blocked until the hidden writer is migrated, semantic reconciliation passes, and rollback no longer needs old state.

### Example 9

**Situation.** Three incidents were attributed to “operator error”: a destructive query, a failed failover, and deletion of a replication slot.

Review decision conditions. The same broad administrator role, ambiguous target naming, missing preview, no peer confirmation, and weak recovery rehearsal contributed to all three. Replace blame with controls: scoped roles, environment identity in prompts, dry-run/impact estimates, guarded destructive operations, two-person approval for high blast radius, tested rollback, and clearer alerts. Assign owners and simulate each scenario.

**Conclusion.** Incident review reveals a systemic control family, not three unrelated people problems.

### Example 10

**Situation.** The review has four findings: failed catastrophic restore evidence (blocker), failed major checkout performance, unknown major degraded capacity, and an observed low-impact audit-label gap.

Keep impact, evidence state, and blocker policy separate. Order the blocker first; require restore and semantic reconciliation before acceptance. Give performance and capacity named owners, deadlines, and representative retests; capacity remains unknown rather than passing. Ticket the audit gap with bounded urgency. The fixture's deterministic order is governance, not a quantitative risk calculation.

**Conclusion.** A useful risk register drives decision and verification without manufacturing precision.

## Cross-Program Connections

[Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) contributes SLOs, incident response, change safety, canaries, error budgets, and production readiness. This module specializes those practices for durable state and database internals.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes stakeholder needs, requirements traceability, hazard analysis, assurance cases, verification, validation, and lifecycle governance. The claim matrix is a database assurance argument.

[Security Engineering](../../25-security-engineering/ROADMAP.md) contributes threat models, identity, least privilege, secrets, cryptography boundaries, audit, vulnerability management, and incident evidence.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) contributes histories, failure models, replication, consensus, fencing, partial synchrony, and consistency semantics required to review failover honestly.

[API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) contributes client contracts, deadlines, retries, idempotency, compatibility, quotas, and observability at the service boundary.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) contributes fleet inventory, policy gates, safe automation, paved paths, access workflows, and standardized evidence collection. Standardization improves coverage but does not replace system-specific judgment.

## References

- Google SRE authors, [The Evolving SRE Engagement Model](https://sre.google/sre-book/evolving-sre-engagement-model/), in *Site Reliability Engineering*, checked 2026-09-05. Production-readiness scope, review objectives, architecture, monitoring, emergency response, capacity, change, and performance.
- Google SRE authors, [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/), in *Site Reliability Engineering*, checked 2026-09-05. User-facing and internal evidence, latency, traffic, errors, saturation, and actionable monitoring.
- Google SRE authors, [Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/), in *Site Reliability Engineering*, checked 2026-09-05. Hypothesis-driven diagnosis, evidence, and avoiding premature causal conclusions.
- Google SRE authors, [Testing for Reliability](https://sre.google/sre-book/testing-reliability/), in *Site Reliability Engineering*, checked 2026-09-05. Failure testing, system tests, and reliability evidence limits.
- Google SRE authors, [Postmortem Culture: Learning from Failure](https://sre.google/sre-book/postmortem-culture/), in *Site Reliability Engineering*, checked 2026-09-05. Blameless causal learning, review, and actionable follow-up.
- PostgreSQL Global Development Group, [Monitoring Database Activity](https://www.postgresql.org/docs/current/monitoring.html), PostgreSQL 18 current documentation checked 2026-09-05. Statistics, sessions, replication, WAL, I/O, locks, progress, and disk evidence.
- PostgreSQL Global Development Group, [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), PostgreSQL 18 current documentation checked 2026-09-05. Plan interpretation, execution caveats, sampled statistics, and platform-dependent costs.
- PostgreSQL Global Development Group, [Continuous Archiving and Point-in-Time Recovery](https://www.postgresql.org/docs/current/continuous-archiving.html), PostgreSQL 18 current documentation checked 2026-09-05. WAL archives, base backups, recovery targets, timelines, and recovery limitations.
- NIST, [SP 800-30 Rev. 1: Guide for Conducting Risk Assessments](https://csrc.nist.gov/pubs/sp/800/30/r1/final), September 2012, current publication record checked 2026-09-05. Risk assessment framing, uncertainty, threats, vulnerabilities, impacts, and communication.
- OWASP Foundation, [Database Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html), current guidance checked 2026-09-05. Least privilege, credential handling, network exposure, hardening, patching, and protected backups.

## Exercises

### Exercise 1

Define review charter, claim, acceptance criterion, evidence item, finding, blocker, residual risk, performance envelope, and waiver. Explain the difference between a review decision and universal certification.

### Exercise 2

A 28-day window has a 99.9% time-based availability objective and 31 minutes of equivalent unavailability. Compute the budget and overspend. Three equal nodes carry 4,800 requests/s and each sustains 2,150 requests/s under the tested degraded workload. Compute ideal normal and one-node-loss load per node, then state what the arithmetic does and does not prove.

### Exercise 3

A failover drill promotes a replica in 90 seconds. Five acknowledged writes are missing, 22 timed-out writes have unknown outcome, the old primary can still accept traffic from one proxy, and all health checks are green. Diagnose the failed claims and design the minimum closure evidence.

### Exercise 4

Design a production database review for a multi-tenant payment service before a major engine upgrade. Include scope, claims, sampling, experiments, security, performance, capacity, recovery, findings, and decision gates.

### Exercise 5

A team has no recent restore drill, no incident in two years, a vendor durability statement, 40% average CPU, one hot tenant at 88% shard capacity, an expiring encryption key, and a launch deadline tomorrow. Produce a defensible disposition, prioritized actions, residual-risk treatment, and retest plan.

## Answers to the Exercises

### Answer 1

A **review charter** fixes decision, boundary, contract, workload, failure/threat models, evidence period, owners, and exclusions. A **claim** is a testable system statement; its **acceptance criterion** says what evidence constitutes a pass. An **evidence item** records provenance, method, scope, result, and limitation. A **finding** links evidence or its absence to a criterion gap and consequence. A **blocker** violates policy for acceptance. **Residual risk** remains after credited controls. A **performance envelope** is the measured workload/state region where correctness and SLOs hold. A **waiver** records accountable acceptance, reason, controls, expiry, and triggers. The decision applies only to the declared scope and evidence; it cannot certify every execution, future version, workload, topology, threat, or failure.

### Answer 2

The window has $28\times24\times60=40{,}320$ minutes. At 99.9%, the time-equivalent budget is $0.001\times40{,}320=40.32$ minutes. With 31 minutes used, 9.32 remain; there is no overspend (overspend is 0), though about 76.9% of budget is consumed. Normal ideal node load is $4{,}800/3=1{,}600$ requests/s. After one node loss it is $4{,}800/2=2{,}400$ requests/s, exceeding tested sustainable load by 250 per remaining node. This refutes N+1 capacity at 4,800 under ideal balance. It does not prove behavior under skew, cold cache, repair, dependencies, correctness, or debt drain, and the availability arithmetic depends on the declared time-based SLI.

### Answer 3

Role promotion/RTO may have passed a narrow 90-second health criterion, but zero-loss durability fails because five acknowledged writes are absent. Twenty-two timeout outcomes violate outcome reconciliation, and the reachable old primary violates unique authority/fencing, creating split-brain risk. Stop or fence conflicting writes under the incident procedure, preserve histories/logs, join idempotency and transaction IDs to both authorities and quorum positions, reconcile every acknowledged and unknown operation, and repair only with idempotent/conditional rules. Closure requires no missing acknowledged writes under the contract, resolved unknowns or an explicitly accepted unknown policy, one fenced writer authority, invariant checks, representative correct requests, alert/runbook evidence, and recovery/debt convergence. Green health checks are supporting evidence only.

### Answer 4

Charter the decision as upgrade readiness for exact versions, regions, tenant classes, data stores, clients/proxies, replicas, backups/keys, and operators. Claims cover payment uniqueness/balance/state transitions; acknowledgement/durability; read freshness; p99/availability; one-zone failover; RPO/RTO; tenant isolation; audit; and 90-day N+1 capacity during upgrade/backup. Sample peak/quiet periods, hot/ordinary tenants, query/bind classes, large tables, replicas, maintenance, and incidents. Reconcile tagged transaction histories; restore a selected chain; test mixed-version replication, failover/fencing, backup compatibility, rollback boundary, and plan/result changes; run production-shaped open-load tests with correctness and debt drain. Inspect privileges, secrets, TLS, key rollover, audit, patches, extensions, and disaster access. Record evidence provenance and gaps. Block on correctness/durability, failed restore, incompatible rollback/failover, isolation, or unbounded degraded capacity; assign other findings with owners, deadlines, retests, and explicit waivers. Decide only for the tested envelope and reopen on material change.

### Answer 5

Disposition: not ready for tomorrow's unrestricted launch. Absence of incidents is weak historical evidence; the vendor statement describes a mechanism, not this configuration or recovery path. Missing restore evidence is a blocker when recoverability is required. The expiring key threatens database/backup availability and must be renewed or safely rotated with verified access before expiry. The hot tenant, not 40% fleet CPU, governs capacity; freeze or cap that tenant/load until degraded capacity is tested. Priority is: protect/rotate key with rollback and backup decryption test; perform isolated restore and semantic/RPO/RTO verification; measure and mitigate hot-shard normal and N+1 capacity; then document broader performance evidence. If the accountable owner accepts a limited launch, constraints must be enforceable—load/tenant cap, supported topology, heightened monitoring, on-call coverage, expiry within hours—and cannot waive a policy-defined data-loss or unrecoverable-key blocker. Retest each original criterion and remove constraints only after evidence passes.
