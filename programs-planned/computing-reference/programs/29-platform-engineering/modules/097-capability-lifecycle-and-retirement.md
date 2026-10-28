---
module_id: PLAT-097
program: Platform Engineering
level: 2
module_number: 97
title: Capability Lifecycle and Retirement
status: complete
last_verified: 2026-09-02
---

# Capability Lifecycle and Retirement

## One-Page Review

### Governing question

How should a platform introduce, mature, deprecate and retire capabilities so that users can depend on explicit contracts, experimentation does not become accidental permanence, migrations preserve outcomes, and residual data and infrastructure are closed safely?

### Essential definitions

- A **capability lifecycle** is the governed sequence of states, evidence gates, promises, ownership and transitions through which a platform offering moves from proposal to disposition.
- A **lifecycle state** communicates fitness and promise; useful states include proposed, experimental, preview, general availability, limited, deprecated, retired and archived.
- **experimental** means bounded learning with no production promise beyond stated safeguards; **preview** means an integrated candidate offered to named cohorts under explicit limits.
- **general availability** means the platform accepts the published production service, support, compatibility, security and lifecycle obligations; it does not mean complete or immutable.
- **deprecation** is a published warning that a supported contract is scheduled or eligible for removal, with reason, replacement or alternative, notice window and migration path.
- **retirement** ends supported use of a capability after an authorized gate; **disposition** completes the remaining treatment of data, infrastructure, identity, secrets, contracts, records and knowledge.
- A **consumer inventory** links actual and potential users, services, owners, versions, usage, data, dependency paths and migration state.
- A **compatibility window** is the declared period or release span during which old and new contracts coexist or interoperate.
- A **last responsible moment** is the latest decision point that preserves required transition, safety and compliance options without committing prematurely.
- A **retirement evidence pack** is the reproducible record proving communication, migration or exception, traffic cessation, data disposition, access revocation, dependency removal, financial closure and post-retirement routing.

### Central model, mechanism, or theorem

Model a capability as a state machine $L=(Q,T)$ with states $Q$ and authorized transitions $T$. For transition $q_a\rightarrow q_b$, gate $G_{a,b}$ is a conjunction of required evidence predicates rather than a date alone. A retirement gate can be expressed as

$$
G_{retire}=U\land M\land Z\land D\land A\land R\land C,
$$

where $U$ is complete consumer ownership, $M$ verified migration or approved exception, $Z$ absence of unsupported traffic, $D$ data disposition, $A$ access and secret closure, $R$ dependency and redirect readiness, and $C$ contract/cost closure. A calendar may trigger review, but cannot prove these predicates.

### Critical invariants

- Every lifecycle state has an owner, intended users, service/support/compatibility promise, allowed data and workloads, evidence gate, review date and exit path.
- A capability cannot advance because time elapsed or code shipped; users, operations, security, cost and recoverability evidence must satisfy the transition gate.
- Deprecation preserves the existing contract for its declared window, emits discoverable warnings, provides a fit replacement or explicit alternative, and accounts for consumer delivery capacity.
- Retirement requires consumer-by-consumer migration or accepted exception, observed legacy use, rollback/redirect readiness and protection of dependent service outcomes.
- Data, records, keys, identities, permissions, infrastructure, vendor obligations, domains, documentation and financial charges receive explicit disposition with retained evidence.
- Exceptions are bounded, owned, risk-accepted and visible; neither one hidden straggler nor one influential consumer can silently create permanent unsupported service.

### Common failures

Preview without expiry; “GA” used as marketing; maturity based only on feature count; experimental paths holding production data without safeguards; deprecation by release note alone; removal dates without consumer inventory; replacement that lacks critical behavior; forced migration during peak change; success measured by announcement; traffic metrics missing batch or dormant use; compatibility shims becoming permanent; exceptions with no owner; deleting resources before rollback expires; retaining credentials after shutdown; losing audit records or encryption keys; domains becoming takeover targets; cost charges continuing; and teams disbanding before disposition evidence is accepted.

### Compact example

A platform is replacing a legacy build service used by eight owned repositories. Its catalog records the old capability as deprecated, the supported replacement, compatibility window, removal target, owner and weekly evidence refresh. Instrumentation combines authenticated calls, queue activity, artifact reads and scheduled-job scans rather than relying on portal visits. Each consumer receives a tested migration plan and rollback checkpoint; two need a supported adapter, and one obtains a time-bounded exception approved by its service and risk owners. The removal date moves until all eight consumers are migrated and a full workload cycle observes zero legacy requests. Retirement then disables new work while keeping a controlled redirect and rollback interval. Disposition exports required records, verifies retention and retrieval, revokes identities and secrets, removes network and DNS exposure, closes licenses and cost allocations, sanitizes residual storage, and assigns the archive owner. Only the evidence gate—not the original date—closes the capability.

### Connections

Lifecycle governance consumes capability contracts, versioning, observability, SLOs, recovery, fleet, security, migration, support, roadmap and sourcing decisions from PLAT-001–096. It supplies cohort and disposition evidence for platform outcome measurement, anti-monopoly review and defensible strategy in PLAT-098–100.

## Governing Question

What promise applies to each platform capability now, which evidence justifies its next state, how will every affected user retain an acceptable outcome through change, and what proves that retirement leaves no unowned service, data, security or cost residue?

Lifecycle labels coordinate risk. A user who sees “preview” must know whether production data, on-call support and compatibility are allowed. An operator who sees “deprecated” must know which contract still holds and until when. A finance owner who sees “retired” must know whether subscriptions and stored data remain.

The lifecycle belongs to the capability, not merely its code. Documentation, APIs, identities, data, support, telemetry, vendor contracts and consuming-team practices can all outlive a deployment. Governance must trace the whole socio-technical boundary.

## Why This Matters

Platforms make early experiments easy to adopt broadly. Without gates, a successful prototype becomes a production dependency while retaining experimental staffing, security and recovery. Accidental permanence converts learning shortcuts into shared systemic risk.

General availability creates obligations. Users plan around compatibility, service objectives, support and notice. Declaring GA without operational evidence borrows trust from future incidents and migrations.

Retirement is unavoidable. Products lose fitness, security models change, suppliers end support, costs rise and better capabilities emerge. Refusing to retire produces sprawling portfolios, fragmented expertise, unpatched dependencies and confusing golden paths.

Removal can also cause harm. Platform consumers have their own roadmaps, release constraints, regulated evidence and seasonal peaks. A technically simple migration may require months of validation. Central teams cannot treat all downstream effort as free.

Residual assets create long tails. A stopped workload may leave snapshots, logs, keys, service accounts, DNS records, audit obligations, invoices and knowledge needed for disputes. Safe disposition must be designed before owners and context disappear.

## Prerequisites and Retrieval

Retrieve the capability catalog and lifecycle policy; user segments and critical journeys; API, configuration, CLI, event and data contracts; owners and on-call schedules; support and service objectives; availability, error-budget, incident and recovery history; security classification, threats and control evidence; accessibility evidence; release and compatibility policy; authenticated usage, traffic, batch, queue, artifact and scheduled-job telemetry; repository/configuration searches; consumer registry and contacts; adoption and retention cohorts; cost and unit economics; vendor support and contract dates; vulnerabilities and end-of-life notices; data lineage, retention and legal holds; identities, secrets, network and domains; migration plans and exceptions; prior transition decisions; and asset/configuration inventories.

Distinguish lifecycle state from delivery status; experimental from unsupported; preview from free production service; GA from finished; adoption from fitness; version from lifecycle; deprecation from removal; warning from communication; migration from forced cutover; consumer from recent caller; zero traffic from zero dependency; replacement from equivalent outcome; compatibility from permanent duplication; retirement from deletion; deletion from verified disposition; archive from abandonment; exception from indefinite support; target date from evidence gate; last use from last possible use; and ownership record from reachable accountable owner.

## Learning Objectives

After completing this module, you should be able to:

1. define lifecycle states with unambiguous service, support, data, compatibility and exit semantics;
2. design evidence gates for experimental, preview, general-availability, limited, deprecated and retired transitions;
3. prevent experiments and previews from becoming accidental production dependencies;
4. create a complete consumer inventory using identity, traffic, configuration and human evidence;
5. publish deprecation notices and in-product warnings with usable replacements and dates;
6. plan migration capacity, coexistence, rollback, exception and support across consuming cohorts;
7. decide retirement using verified predicates rather than announcements or elapsed time;
8. disposition data, access, infrastructure, contracts, documentation and knowledge safely;
9. audit residual traffic, risk, cost and user outcomes after retirement; and
10. govern lifecycle decisions without coercion, indefinite exceptions or abandonment.

## Core Exposition

### Define a lifecycle policy

Publish the allowed states, meanings, transition authorities, required evidence, normal review cadence and exceptional paths. Keep state names few enough that users can act on them.

Define semantics from a consumer perspective: permitted workload and data, support, service objective, compatibility, security evidence, notice, contribution and exit.

Version the policy. Existing capabilities need an explicit adoption plan when semantics change.

### Separate capability and implementation

A stable platform capability may change internal providers or components without changing its consumer contract. Conversely, a small API removal can retire user-visible behavior even if the service remains.

Give capabilities stable catalog identity and link implementations, interfaces and dependencies. Lifecycle decisions apply at the correct contract boundary.

Avoid equating a repository, vendor product or cluster with the complete capability. Include people, process, policy, data and operation.

### Govern the proposed state

A proposal records the problem, affected users, evidence, alternatives, owner, intended learning and relationship to strategy. It promises no delivery.

Reject duplicates or problems outside platform scope early. Record the decision so recurrent requests can add evidence rather than restart debate.

Set a review or expiry for proposals. An infinite idea backlog is not a lifecycle.

### Bound experiments

Experiments answer named uncertainties with fixed time, capacity, users and data. State prohibited production or sensitive use unless safeguards explicitly allow it.

Provide isolation, cleanup, ownership, observability and stop criteria. Do not attach experiments to critical paths without a supported fallback.

At expiry, advance with evidence, extend for a newly stated question, or dispose. Quiet continuation is not an allowed transition.

### Use preview as a contract

A preview tests integrated fitness with named cohorts and production-shaped journeys. Publish limits, support hours, compatibility risk, change expectations and exit.

Control enrollment so participant count does not outrun support and learning capacity. Participants must understand obligations without signing away basic safety.

Measure outcome, operability, accessibility, security, cost and support—not only signups or satisfaction among champions.

### Gate general availability

GA requires demonstrated user fitness; documented, versioned interfaces; production security and privacy; service objectives; monitoring; on-call; capacity; recovery; support; cost ownership; and lifecycle commitments.

Verify failure and restoration, not only happy-path load. Confirm consuming teams can operate their part of the contract.

Authorized product and operating owners accept the obligation. A launch event, sales promise or feature-complete label cannot substitute.

### Limit a capability deliberately

Use limited status when a capability remains supported for bounded users or uses but is not open to new adoption. State eligibility, service promise and review.

Limited can support regulatory, regional or legacy needs while avoiding false general availability. It must not become a place to hide missing ownership.

Decide whether limitation leads to renewed investment, continuing niche service or deprecation.

### Monitor lifecycle fitness

Continuously observe journey success, adoption, retention, reliability, security, support, cost, accessibility, dependency health and user research.

Segment evidence by cohort and lifecycle. Low use can signal low need, poor discoverability, exclusion or a critical infrequent recovery path.

Review state after incidents, control failures, vendor changes, maintainer loss, cost discontinuities and strategy shifts.

### Define deprecation triggers

Triggers include superior replacement, duplicated capability, weak outcomes, unsustainable cost, unacceptable risk, supplier end of support, incompatible strategy or vanished user need.

Record the consequence of continuing and retiring. Deprecation should solve a portfolio problem, not merely make architecture aesthetically uniform.

Do not punish low adoption without investigating why. Mandatory platforms can also deserve deprecation when they fail outcomes.

### Design the replacement or alternative

Map old critical journeys, edge cases, evidence and operational behavior to the proposed future. Not every feature needs preservation, but every legitimate outcome needs a decision.

Offer replacement, export, supported adapter or explicit statement that the need will no longer be served. Name gaps and owners.

Test with representative consumers before announcing a removal window that assumes equivalence.

### Write the deprecation contract

Publish what is deprecated, why, affected versions and interfaces, replacement, compatibility, warning start, support promise, target removal, migration guide, owner and help route.

Use date semantics precisely. A review date, earliest removal date and committed shutdown date are different.

Provide machine-readable catalog status and warnings at the point of use where safe. Release notes alone reach only attentive users.

### Discover every consumer

Combine service identity, authenticated calls, audit logs, configuration scans, dependency graphs, queues, artifact access, scheduled jobs, credentials, billing and human confirmation.

Observe at least one complete relevant workload cycle. Infrequent disaster recovery, annual reporting and dormant fallback paths may be real consumers.

Assign every finding to a reachable owner and record false positives, unknowns and confidence. Unknown ownership is a blocker, not proof of no consumer.

### Plan cohorts and capacity

Group consumers by consequence, complexity, version, readiness and organizational constraints. Pilot representative cases before scaling.

Model platform migration/support capacity and consuming-team capacity. Avoid peak business, release freezes and simultaneous unrelated migrations.

Protect incident headroom and rollback support. Full utilization makes migration risk nonlinear.

### Provide migration tooling

Offer inventory, readiness checks, converters, dual-read/write or compatibility paths, test harnesses, runbooks and observable progress where appropriate.

Keep automation idempotent, explainable and reversible. Do not silently discard fields that lack a replacement.

Version tools and verify them against current source and target contracts. A stale migration guide is an incident generator.

### Rehearse and migrate

Begin with low-blast-radius but representative consumers. Capture journey, data, performance, security and recovery evidence.

Define checkpoints, rollback conditions and who may decide. Preserve old state until the declared rollback window and validation complete.

Scale only when early cohorts demonstrate the outcome without unacceptable support or guardrail effects.

### Govern exceptions

Require owner, reason, consequence, compensating controls, support boundary, capacity, expiry and next decision. Publish aggregate exception debt.

An exception can protect a legitimate constraint; it cannot silently compel indefinite platform operation. Leadership must fund extension or accept migration/retirement risk.

Review exceptions before their expiry. Auto-renewal hides unresolved structural problems.

### Verify retirement readiness

Reconcile the consumer inventory: migrated, no longer needed, or approved exception with another plan. Verify target outcomes after transition.

Observe zero unsupported use across relevant cycles and failure paths. Scan residual configuration and credentials; do not trust one traffic dashboard.

Confirm rollback or redirect, data plan, access closure, dependency removal, communications, support routing, cost closure and disposition ownership.

### Execute a staged shutdown

Where consequence warrants, block new enrollment, then new writes or work, then reads after export/retention evidence, before destroying state.

Use a reversible dark period or controlled reject response to reveal hidden callers. Provide stable, non-sensitive errors and replacement guidance.

Monitor user and service outcomes throughout. Abort or extend when the gate fails; schedule pressure does not make missing evidence true.

### Disposition data and records

Classify data for transfer, archive, retention, legal hold, deletion or sanitization. Preserve lineage, schema, integrity, retrieval means and keys for retained records.

Verify receipt by a new owner before deleting the old copy. Verify deletion at every replica, backup and supplier boundary according to policy.

Keep evidence without retaining unnecessary sensitive content. Archive formats must remain readable for their required period.

### Close identities and infrastructure

Revoke service accounts, human roles, tokens, certificates, keys and vendor access. Remove firewall rules, routes, queues, schedules, images, storage and compute.

Treat DNS names, domains, package names and endpoints carefully; abandonment can enable takeover. Maintain redirects or reservations for the justified period.

Scan after closure for resources, traffic, vulnerabilities and charges. A deployment deletion is only one step.

### Close contracts and finances

Terminate licenses, subscriptions, support, reservations and data-processing arrangements under their notice terms. Reconcile final usage and invoices.

Remove cost allocations and budgets only after residual charges are understood. Preserve warranties, audit rights or claims needed after service ends.

Record supplier deletion and access evidence. Contract expiry does not execute technical disposition automatically.

### Transfer knowledge and ownership

Move relevant research, decisions, incidents, schemas, migration history and operating knowledge to replacement or archive owners.

Update catalogs, golden paths, training, support search and architecture maps. Mark obsolete documentation rather than leaving plausible instructions live.

Do not dissolve the team until evidence ownership and the post-retirement contact are accepted.

### Observe after retirement

Monitor retired endpoints, redirects, support contacts, security signals, cost and replacement outcomes through a declared window.

Investigate hidden callers rather than immediately restoring unsupported service. Use an incident path for harmful surprises.

At window end, decide which redirect, domain, archive and evidence responsibilities persist and close the retirement record.

## Definitions and Notation

Let lifecycle states be $Q=\{proposed, experimental, preview, GA, limited, deprecated, retired, archived\}$ and $T\subseteq Q\times Q$ the authorized transition relation. Each edge $(a,b)$ has gate predicate $G_{a,b}$, owner $o$, evidence snapshot $E$, decision time $\tau$ and review/expiry $\rho$.

For consumer set $U$, partition each consumer into migrated $U_m$, no-longer-needs $U_n$, or approved-exception $U_e$. Readiness requires $U=U_m\cup U_n\cup U_e$ with current accountable ownership and no unclassified member.

Let $z_w$ be observed unsupported use across required workload window $w$, $D$ verified data disposition, $A$ access/secret closure, $R$ dependency and redirect readiness, and $C$ contractual/cost closure. Then

$$
G_{retire}=(U=U_m\cup U_n\cup U_e)\land(z_w=0)\land D\land A\land R\land C.
$$

The model is a governance predicate, not proof that all unknown dependencies were discovered. Confidence comes from independent discovery sources, adequate observation windows, failure probes and post-retirement monitoring.

## Mechanisms, Invariants, or Proof Structure

### Twelve-step lifecycle mechanism

1. Define lifecycle states, consumer promises, transition authority and expiry semantics.
2. Give each capability stable identity, owner, boundary, contracts and current state.
3. Bound proposed, experimental and preview work by learning, users, data and time.
4. Require product, operational, security, recovery, support and cost evidence for GA.
5. Monitor segmented outcome, use, risk, reliability, support and economic fitness.
6. Select a deprecation trigger and validate replacement or explicit future alternative.
7. Publish the deprecation contract through catalog, interface and direct-owner channels.
8. Discover consumers and dependencies from multiple technical and human sources.
9. Migrate in supported cohorts with capacity, verification, rollback and exceptions.
10. Evaluate retirement predicates and execute a staged, observable shutdown.
11. Disposition data, access, infrastructure, contracts, costs, documentation and knowledge.
12. Monitor the retired surface and close only when residual obligations have owners.

### State-contract invariant

Every state tells users what workloads, data, support, service, compatibility, change and exit promises apply, with owner and review/expiry.

### Evidence-gate invariant

Transitions require their declared evidence and authorized acceptance; dates, output completion, popularity and executive urgency cannot substitute.

### Consumer-outcome invariant

Every known consumer retains an accepted outcome through migration, cessation or bounded exception, with consuming-team capacity and consequence represented.

### Compatibility invariant

During deprecation, the published old contract continues for its window, the target is fit for stated outcomes, and shims have ownership and removal gates.

### Disposition invariant

Retirement accounts for data, records, keys, identity, access, infrastructure, domains, contracts, costs, documentation and knowledge, not only runtime deletion.

### Exception invariant

Every exception has owner, risk, compensating control, support boundary, expiry and decision path; exception debt remains visible to portfolio governance.

### Proof sketch: zero recent traffic cannot prove retirement safety

Construct two deprecated capabilities with zero calls during a 30-day observation. Capability A serves only daily workflows and has no residual dependencies. Capability B is the configured annual recovery path for a regulated service and retains sensitive backups and active credentials. Their recent traffic is identical while retirement consequence differs. Therefore zero recent traffic alone is insufficient evidence of retirement safety; workload-cycle coverage, configuration/dependency discovery, data and access evidence are also necessary.

### Executable retirement gate

This synthetic audit checks eight consumers, zero legacy requests and six evidence predicates. It demonstrates conjunction and reconciliation, not universal notice periods or workload windows.

<!-- bijux-verify: {"id":"capability-retirement-gate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"consumers=8\nmigrated=8/8\nlegacy_requests=0\nopen_blockers=0\nrequired_evidence=6/6\nredirect_ready=yes\ngate=pass\n"}} -->
```python
consumers = {f"service-{number}": "migrated" for number in range(1, 9)}
legacy_requests = 0
blockers = []
evidence = {
    "notice": True,
    "replacement": True,
    "data_disposition": True,
    "access_revocation": True,
    "cost_closure": True,
    "archive_owner": True,
}
redirect_ready = True
reconciled = all(state in {"migrated", "ceased", "exception"} for state in consumers.values())
gate = reconciled and legacy_requests == 0 and not blockers and all(evidence.values()) and redirect_ready

print(f"consumers={len(consumers)}")
print(f"migrated={sum(state == 'migrated' for state in consumers.values())}/{len(consumers)}")
print(f"legacy_requests={legacy_requests}")
print(f"open_blockers={len(blockers)}")
print(f"required_evidence={sum(evidence.values())}/{len(evidence)}")
print(f"redirect_ready={'yes' if redirect_ready else 'no'}")
print(f"gate={'pass' if gate else 'fail'}")
```

### Verification strategy

Validate catalog state against runtime and owners; test state semantics with users; inspect experiment expiries; reproduce GA reliability and recovery evidence; trace deprecation warnings through interfaces; reconcile consumers across identity, traffic, configuration, billing and interviews; observe full workload cycles; sample cohort migrations and rollbacks; challenge exceptions; inject hidden callers during a reversible dark period; verify exports and archive retrieval; scan credentials, DNS, infrastructure and charges; obtain supplier deletion evidence; and monitor retired endpoints and replacement outcomes through the declared closure window.

## Alternatives and Trade-Offs

1. Few lifecycle states are understandable but may hide materially different promises.
2. Many granular states improve precision but increase catalog and user confusion.
3. Time-based advancement supplies cadence but can promote capabilities without evidence.
4. Evidence-based gates protect users but require measurement and accountable judgment.
5. Open previews broaden discovery but can accumulate uncontrolled production dependence.
6. Cohort previews bound risk but may miss diverse or excluded users.
7. Long compatibility windows aid consumers but multiply support and security surface.
8. Short windows reduce duplication but transfer schedule and validation risk downstream.
9. Dual operation supports rollback but raises consistency, cost and cognitive load.
10. One-way cutover simplifies architecture but increases irreversible failure consequence.
11. Automated migration scales but can reproduce silent semantic loss.
12. Guided migration handles edge cases but consumes scarce support capacity.
13. Strict exception expiry preserves momentum but may harm legitimate constrained services.
14. Flexible exceptions protect local outcomes but can create permanent legacy operation.
15. Immediate resource deletion lowers cost but destroys rollback and evidence options.
16. Extended dark retention preserves recovery but maintains attack surface and expense.
17. Long redirects help dormant users but retain domains, certificates and ownership.
18. Complete archival supports audit but increases privacy, key and readability obligations.

## Failure Modes and Misconceptions

1. “Lifecycle is release status” ignores user and operational promises.
2. “Experimental means no safeguards” permits unacceptable harm.
3. “Preview users accept every risk” erases platform accountability.
4. “Popular preview should become GA” substitutes adoption for fitness.
5. “GA means feature complete” prevents continuing improvement.
6. “GA can be declared by delivery” omits operational acceptance.
7. “Limited means unsupported” makes the label unsafe.
8. “Low use means low value” ignores critical infrequent journeys.
9. “Deprecation means broken now” violates the compatibility window.
10. “A release note is sufficient notice” misses actual owners and runtime users.
11. “A removal date is a retirement plan” omits evidence predicates.
12. “A replacement exists, so migration is easy” ignores outcome gaps.
13. “Central migration capacity is enough” ignores consumer roadmaps.
14. “All consumers appear in traffic” misses batch, dormant and recovery paths.
15. “Thirty quiet days prove no dependency” may miss annual behavior.
16. “Configuration searches are complete” miss dynamic and human dependencies.
17. “A compatibility shim is free” creates another owned capability.
18. “Automation makes migration safe” can scale semantic loss.
19. “One successful cohort proves every case” ignores segmentation.
20. “Rollback means keep everything forever” confuses a window with permanence.
21. “Exceptions are failures” can ignore legitimate constraints.
22. “Exceptions can auto-renew” hides ownership and accumulating debt.
23. “Retirement equals turning it off” ignores disposition.
24. “Zero traffic permits immediate deletion” destroys rollback and records.
25. “Deleting primary storage deletes all data” ignores replicas and backups.
26. “Revoking one account closes access” misses tokens, keys and vendors.
27. “Expired DNS is harmless” creates takeover and user-confusion risk.
28. “Contract expiry stops charges and processing” assumes technical execution.
29. “Old documentation is obviously obsolete” leaves plausible unsafe paths.
30. “The team can disband after shutdown” abandons residual obligations.

## Worked Examples

### Example 1

An experiment reaches its expiry with weak outcome evidence. It is disposed rather than silently relabeled preview, preserving capacity and trust in state semantics.

### Example 2

A popular preview fails restore testing and has no on-call owner. Its GA gate stays closed while reliability work proceeds.

### Example 3

An infrequently used certificate-recovery path looks inactive. Configuration and incident exercises identify it before the observation-only retirement would break recovery.

### Example 4

An API emits structured deprecation warnings containing replacement and sunset links while direct notices reach registered service owners.

### Example 5

A replacement drops one audit field. The migration gate pauses until an adapter preserves the regulated evidence or risk authority accepts a different outcome.

### Example 6

Fifty teams cannot migrate in one quarter. Cohorts ordered by consequence and readiness keep support load and rollback capacity within bounds.

### Example 7

One consumer receives a six-month exception with funded support, compensating monitoring, named risk owner and non-renewing decision date.

### Example 8

A reversible reject window reveals a monthly batch caller absent from dashboards. The caller gets an owner and migration instead of a surprise outage.

### Example 9

Runtime deletion leaves DNS, a vendor token and reserved capacity. Post-retirement scans find and close each residual asset and charge.

### Example 10

Archived audit records are encrypted with a retiring key. The disposition plan preserves controlled retrieval and rotation rather than creating unreadable compliance evidence.

## Cross-Program Connections

- Product Management contributes lifecycle promises, cohort research, adoption and retirement outcomes.
- API Engineering contributes compatibility, versioning, deprecation warnings and sunset contracts.
- Site Reliability Engineering contributes GA readiness, service objectives, migration headroom and decommissioning.
- Security Engineering contributes data disposition, credential revocation, attack-surface closure and evidence.
- Data Engineering contributes lineage, retention, archive readability, deletion and migration validation.
- Systems Engineering contributes lifecycle state machines, transition gates, dependencies and residual risk.
- Organizational Design contributes ownership continuity, decision rights and consuming-team capacity.
- Finance contributes ongoing cost, contract closure, exception funding and retirement economics.
- Human-Computer Interaction contributes understandable status, change communication and accessible alternatives.
- Technology Governance contributes exception, risk acceptance, audit, appeal and anti-coercion controls.

## References

1. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/). Retrieved 2026-09-02.
2. CNCF TAG App Delivery. [Platform Engineering Maturity Model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/). Retrieved 2026-09-02.
3. DORA. [Platform Engineering](https://dora.dev/capabilities/platform-engineering/). Retrieved 2026-09-02.
4. Kubernetes. [Deprecation Policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/). Retrieved 2026-09-02.
5. Kubernetes. [Deprecated API Migration Guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/). Retrieved 2026-09-02.
6. Semantic Versioning. [Semantic Versioning 2.0.0](https://semver.org/). Retrieved 2026-09-02.
7. IETF. [RFC 8594: The Sunset HTTP Header Field](https://www.rfc-editor.org/rfc/rfc8594.html). Retrieved 2026-09-02.
8. IETF. [RFC 9745: The Deprecation HTTP Response Header Field](https://www.rfc-editor.org/rfc/rfc9745.html). Retrieved 2026-09-02.
9. GOV.UK Service Manual. [How the Live Phase Works](https://www.gov.uk/service-manual/phases/live/). Retrieved 2026-09-02.
10. GOV.UK Service Manual. [Retiring Your Service](https://www.gov.uk/service-manual/agile-delivery/retiring-your-service). Retrieved 2026-09-02.
11. GOV.UK Service Manual. [Managing and Improving Your Service Through Its Lifecycle](https://www.gov.uk/service-manual/agile-delivery/running-your-service-in-a-sustainable-way). Retrieved 2026-09-02.
12. Google SRE. [SRE Engagement Model](https://sre.google/workbook/engagement-model/). Retrieved 2026-09-02.
13. Google SRE. [Service Best Practices](https://sre.google/sre-book/service-best-practices/). Retrieved 2026-09-02.
14. NIST. [Systems Security Engineering](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final). Retrieved 2026-09-02.
15. NIST. [Guidelines for Media Sanitization](https://csrc.nist.gov/pubs/sp/800/88/r2/final). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define experimental, preview and GA gates for a platform database-provisioning capability that may process regulated data.

### Exercise 2

A deprecated service has 20 known consumers: 16 migrated, 2 ceased use, 1 approved exception and 1 unknown owner. Traffic is zero for 60 days. Evaluate retirement readiness.

### Exercise 3

Design a deprecation contract and migration sequence for an API replacement that does not initially preserve one high-consequence audit field.

### Exercise 4

A retired capability’s compute is gone, but backups, DNS, vendor access and documentation remain. Produce a disposition plan and evidence gate.

### Exercise 5

An executive demands shutdown on the announced date while two teams cannot safely migrate. Design the governance response without allowing indefinite legacy support.

## Answers to the Exercises

### Answer 1

Experimental: named learning question, isolated tenants, synthetic or explicitly approved data, no critical path, fixed expiry, owner, cleanup and fallback. Preview: selected regulated and non-regulated cohorts, reviewed data/control scope, production-shaped integration, bounded service/support, telemetry, recovery exercise, compatibility warning and exit.

GA additionally requires validated critical journeys and accessibility; versioned API/data contracts; capacity and unit cost; service objectives and on-call; threat/control evidence; backup and restore; audit and deletion; support; migration; lifecycle owner and notice policy. Time or adoption cannot advance a state without these predicates.

### Answer 2

The consumer partition is incomplete: the unknown owner is neither migrated, ceased nor an accepted exception. Zero observed traffic does not close that gap and may not cover the consumer’s workload cycle. Retirement is not ready.

Use identity, credentials, configuration, dependency, billing, repository and human searches to identify the owner and possible dormant use. Resolve the consumer through verified migration, confirmed no-longer-needed outcome or a bounded exception. Then validate data, access, redirect, dependency, cost and disposition predicates before staged shutdown; retain post-retirement monitoring.

### Answer 3

State old and new API identifiers, reason, supported old window, earliest removal, replacement gaps, warning mechanism, owner, support and migration guide. Treat preservation of the audit outcome as mandatory for affected consumers rather than claiming feature equivalence.

Develop a versioned field or supported adapter, validate round-trip and audit retrieval, and pilot a representative regulated consumer. Migrate low-consequence consumers only if mixed operation is safe; do not force the high-consequence cohort. When evidence passes, schedule cohorts with capacity, rollback and observation. Any exception names risk, support, expiry and funding.

### Answer 4

Classify backups by transfer, retention, legal hold, deletion and sanitization; verify archive integrity, readability, ownership and key availability, then obtain deletion evidence for unneeded copies. Remove vendor identities, tokens and subprocessors after required export and validate revocation.

Keep DNS or a controlled redirect for the justified dormant-user window, with certificate and owner, then retire or reserve it safely. Mark documentation deprecated, preserve required decisions/records and remove actionable obsolete instructions. Scan infrastructure, access, traffic, vulnerabilities and charges. Close only when each artifact has evidence and a continuing owner where necessary.

### Answer 5

Present the failed retirement predicates, affected outcomes and evidence to the authorized service and risk owners. Do not make the announced date true by hiding unsafe consumers. Pause new enrollment, preserve the supported old contract, and assess whether the replacement, schedule or consuming-team capacity can change.

For each team, define a funded migration plan or time-bounded exception with compensating controls, support boundary, consequence, owner and non-automatic expiry. Update the canonical notice and communicate why. Leadership explicitly accepts the extension cost and residual risk. Escalate again at the next evidence gate; if continued service becomes unacceptable, coordinate an owned service-outcome decision rather than abandoning teams through a technical shutdown.
