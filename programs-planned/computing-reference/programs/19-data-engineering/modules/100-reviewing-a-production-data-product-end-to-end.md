---
module_id: DE-100
program: Data Engineering
level: 2
module_number: 100
title: Reviewing a Production Data Product End to End
status: complete
last_verified: 2026-09-03
---

# Reviewing a Production Data Product End to End

## One-Page Review

### Governing question

How can an accountable review determine whether a production data product is valuable, correct, understandable, secure, operable, economical, evolvable, and recoverable for its actual consumers—and produce a decision whose claims trace to current evidence instead of a polished architecture diagram or averaged checklist?

### Essential definitions

- A **production data product** is an owned consumer-facing capability combining data, meaning, contract, interfaces, lineage, quality, policy, operations, support, economics, and lifecycle.
- A **review scope** names the product/version, consumer outcomes, environments, state boundaries, dependencies, change or decision, and excluded surfaces.
- A **review claim** is a falsifiable statement about product behavior under named conditions; an **evidence item** is a dated, attributable observation supporting or challenging it.
- A **gate** is a mandatory acceptance condition whose failure cannot be canceled by high scores elsewhere.
- A **finding** is a specific gap between required and observed state with evidence, impact, owner, disposition, and due date.
- A **risk** is uncertainty about an objective and its consequences, recorded with scenario, likelihood/evidence, impact, controls, owner, and residual exposure.
- A **decision** is `ready`, `conditionally ready`, or `not ready` for the named scope; it is not a timeless certification.
- **Traceability** links consumer outcome → contract/objective → design/control → verification → operational evidence → decision.
- **Independent reconciliation** compares product output with an authoritative expectation not derived through the same possibly faulty path.
- A **control plane** changes or describes the product; a **data plane** carries or serves its data. Both must be reviewed and observable.
- **Operational evidence** is behavior measured in realistic runs, failures, replays, access decisions, queries, incidents, and drills—not configuration intent alone.
- A **review receipt** freezes the reviewed identities, evidence digests, participants, findings, exceptions, decision, expiry, and triggers for re-review.

### Central model, mechanism, or theorem

Let mandatory review gates be $G=\{g_1,\ldots,g_n\}$ with outcome $g_i\in\{pass,fail,unknown,not\ applicable\}$. Readiness is conjunctive over applicable gates:

$$
Ready=\bigwedge_{i:g_i\ applicable}(g_i=pass).
$$

An average or weighted score is useful for prioritization but cannot prove readiness: one failed authorization, correctness, deletion, ownership, or recovery gate remains a blocker even when every other dimension scores highly.

For each accepted claim $q$, require an evidence chain

$$
q\rightarrow\{e_1,\ldots,e_k\},\qquad e_j=(scope,time,source,method,result,limitations,digest).
$$

Evidence relevance decays when product version, workload, data distribution, dependency, policy, scale, objective, or environment changes. The decision is valid only for its frozen scope and review interval, subject to explicit invalidation triggers.

### Critical invariants

- The review starts from consumer decisions and business outcomes, not a technology inventory; it includes harmed/non-user stakeholders and prohibited uses.
- Product, contract, state/snapshot, schema, code/config/runtime, policy, environment, sources, dependencies, and serving identities are frozen in the review receipt.
- Every critical claim has direct current evidence, scope and limitations; design documents and provider features are not substituted for observed behavior.
- Source-to-consumer counts, amounts, keys, time boundaries, corrections, duplicates, deletions and lineage reconcile independently.
- Quality and SLO indicators are defined at consumer-visible boundaries with eligible populations, unknown telemetry handling, objectives and error budgets.
- Threats, classification, least privilege, negative authorization, secrets, audit, retention, deletion, residency and incident/recovery paths are exercised, not merely configured.
- Backfills, replays, retries, late data, schema evolution, version coexistence, dependency failure and overload remain bounded and idempotent/effect-safe.
- Capacity and cost cover representative peak, skew, failure, catch-up and query workloads; economics use SLO-qualified useful outcomes and conserved allocation.
- Ownership spans product, data, code, infrastructure, policy, on-call, incident command, consumer support, exceptions and retirement—with deputies and escalation.
- Failed or unknown mandatory gates block readiness unless an authorized, time-bounded, scope-specific exception states compensating controls and residual risk.

### Common failures

Reviewing a diagram rather than a deployed version; starting with tools instead of consumers; omitting source or downstream boundaries; accepting “job green” as data correctness; relying on row counts from the same pipeline; checking schema but not meaning, grain, units, time, corrections or policy; averaging away a critical failure; converting unknown to pass; validating only a happy-path sample; trusting a provider feature as configured end-to-end behavior; ignoring backfill, late data, duplicates, overload, external dependencies and recovery; reviewing access grants without denied-case tests; presenting allocated cost without conserved totals or good-unit denominators; assigning findings to “data team”; granting permanent exceptions; and issuing a timeless “approved” label with no version or re-review triggers.

### Compact example

A customer-value product passes 10 of 12 mandatory gates. Its architecture, contracts, reconciliation, SLOs, security, deployment, capacity, cost, lineage, and version plan pass. Consumer acceptance is missing for a billing export, and the last recovery exercise restored files but not current policy or serving. A score of 83% looks strong; the conjunctive decision is `not ready`. **Conclusion:** a review surfaces blockers and directs work. It does not manufacture confidence by averaging incomparable obligations.

### Connections

[DE-073](073-reconciliation-tests.md) supplies independent correctness, [DE-076](076-data-contracts.md) supplies producer-consumer promises, [DE-089](089-auditability-and-provenance.md) supplies evidence identity, [DE-096](096-freshness-and-completeness-slos.md) supplies consumer-visible reliability, [DE-098](098-disaster-recovery-for-data-products.md) supplies recovery acceptance, and [DE-099](099-versioning-and-deprecating-datasets.md) supplies lifecycle gates. [SYSENG-100](../../26-systems-engineering/modules/100-conducting-a-whole-system-review-of-a-software-intensive-capability.md) contributes whole-system review discipline; this capstone applies it to data state, semantics, pipelines, serving, governance, and consumers.

## Governing Question

For the exact product and decision under review, do dated and reproducible evidence chains demonstrate valuable consumer outcomes, a complete and consistent contract, controlled source-to-serving transformations, independent correctness, reliable SLOs, secure and privacy-respecting access, bounded operations and change, sufficient failure capacity and disaster recovery, explainable unit economics, owned support and retirement—and which failed or unknown gate prevents an honest production decision?

## Why This Matters

Data products fail compositionally. Each component may look healthy while their combination is wrong. A connector reports success but drops one tenant. A table is complete relative to staged input while the source extract was partial. A schema validates but `amount` silently changed units. A dashboard responds quickly with stale data. A recovery restores bytes and old permissions. A cost optimization lowers spend by deleting history needed for corrections. A catalog lists an owner who cannot make decisions during an incident.

Specialized reviews help but fragment the truth. Security reviews focus on threats and access. Data-quality reviews inspect rules. Architecture reviews inspect components. SRE reviews inspect availability. Finance reviews inspect bills. Privacy reviews inspect processing and retention. Consumer acceptance checks business behavior. An end-to-end review does not replace specialists; it joins their claims through one frozen product boundary and asks whether all required properties hold at once.

The review is a decision system, not a documentation contest. Its purpose is to decide whether to launch, expand, migrate, accept a material change, continue under conditions, or retire. It should reveal uncertainty early, focus scarce work on consequential gaps, and preserve a receipt others can audit. A thick packet with no decision scope or evidence lineage is weaker than a short record whose claims reproduce.

Evidence has context. A load test on uniform keys does not cover production skew. A backfill tested on one day does not cover years of schema history. A green restore of a tiny snapshot does not establish a four-hour product RTO. A successful query under an administrator does not establish least privilege. A 99.9% job-success rate does not establish consumer freshness or completeness. Reviewers must distinguish specification, proof, deterministic computation, empirical test, production observation, provider documentation, expert judgment, and accepted business risk.

Reviews can themselves create risk. A checklist invites box-ticking. A single score encourages compensating a critical failure with unrelated polish. A large panel diffuses accountability. Surprise gates delay launches and incentivize concealment. Permanent approval becomes stale. The remedy is a known contract, progressive evidence creation during development, a small accountable decision body, explicit mandatory gates, scoped exceptions, and continuous invalidation/re-review triggers.

This capstone integrates the program. It asks whether acquisition, ingestion, storage, modeling, orchestration, streaming, table formats, quality, metadata, governance, serving, reliability, economics, recovery and versioning form one credible product. The result is not certainty. It is a transparent decision with bounded claims, actionable findings, and known residual risk.

## Prerequisites and Retrieval

Retrieve decision context: launch/change/migration/expansion/continuation/retirement decision; product and contract version; state/snapshot and source boundary; environments/regions/tenants; review owner and decision authority; planned date; constraints; prior decisions/findings/incidents; and explicit in-scope/out-of-scope surfaces.

Retrieve consumer and outcome evidence: users and non-user stakeholders, decisions/workflows, criticality, value hypothesis and KPI, prohibited/misuse cases, accessibility needs, contracts/SLAs, acceptance tests, support history, usage and adoption, downstream lineage, exports/copies, version pins, feedback, manual fallbacks, harm if stale/wrong/unavailable, and signed acceptance or unresolved objections.

Retrieve semantic and source evidence: authoritative sources and owners, acquisition agreements, schemas/stable IDs, keys/grain/population, definitions/units/time zones/enums/defaults, event/effective/processing time, late/correction/deletion behavior, reference-data editions, provenance, source control totals, known gaps/bias, licensing, consent/purpose/residency, and change notification.

Retrieve architecture and execution evidence: context/container/data-flow diagrams tied to deployment; trust and failure boundaries; batch/stream topology; transformations and versioned code/config/runtime; environments; orchestration DAGs, schedules, checkpoints and run metadata; idempotency/deduplication; transactions; retries/timeouts/backpressure; backfills/replays; storage/table format, partition/layout/compaction; catalogs/lineage; serving stores, APIs, caches and materializations; dependencies and vendors.

Retrieve verification evidence: unit/property/contract/integration/end-to-end tests; representative fixtures; source-to-output reconciliation; schema/constraint checks; quality dimensions and thresholds; old/new diffs; historical/backfill tests; streaming order/late/duplicate tests; negative tests; access/privacy/deletion tests; load/skew/failure/recovery tests; test environment/scale; results, failures, limitations, evidence digests and dates.

Retrieve operations evidence: SLOs/SLIs and eligibility, dashboards and alerts, runbooks, on-call/escalation, incident command, recent incidents/postmortems, deployment/canary/rollback, observability signals and correlation, data incident triage, dependency health, quotas/capacity, backlog/drain, cost allocation/unit economics, disaster recovery points/times, last drill, maintenance, ownership/deputies, support, audit and continuous review triggers.

Retrieve lifecycle evidence: product/version registry, current alias, compatibility policy, consumer inventory and telemetry coverage, schema evolution, migration/backfill plan, deprecation/sunset/retirement, retention/deletion/legal holds, disaster-recovery preservation, archive/citation requirements, physical disposition, and unresolved version/exception debt.

Distinguish planned from deployed; configured from effective; component from product; producer output from consumer observation; source count from independently controlled expectation; metric from objective; average from tail; attempt from useful result; observed absence from proven absence; direct consumer from copied data; current alias from immutable version; backup from recovered product; allocated cost from causal/value evidence; finding from risk; owner from executor; exception from pass; and review validity from permanent certification.

Create a review charter:

| Concern | Required review content |
|---|---|
| Decision | Exact question, authority, possible outcomes, date and constraints |
| Scope | Product/version/state/environment/consumers/dependencies and exclusions |
| Claims | Falsifiable outcomes and mandatory gates with pass criteria |
| Evidence | Source, method, result, date, identity, digest and limitations |
| Participants | Product, producer, consumer, operations, security/privacy, finance/domain roles |
| Findings | Gap, impact, evidence, owner, disposition, due date and verification |
| Risk | Scenario, affected objective, controls, residual, authority and expiry |
| Receipt | Decision, rationale, blockers/exceptions, reviewed identities and triggers |

Write a falsifiable claim: “Customer-value product v2 serves 29 owned consumers through table and API surfaces from seven authoritative sources; stable IDs, customer grain, USD/reporting-date semantics and correction/deletion behavior are contracted; daily source-to-output controls reconcile counts and value with zero unexplained difference; 99.9% of eligible consumer-hours meet 45-minute freshness and 99.99% completeness with an error-budget policy; negative authorization and deletion tests pass; peak/skew/zone-loss tests meet latency and drain objectives; a full product recovery drill achieved 8-minute point and 2h41m consumer-service capability; every run is traceable to sources/code/schema/policy; effective cost per SLO-good million records reconciles to the bill; all v1 consumers migrated; and no mandatory gate is failed or unknown at review receipt R.”

## Learning Objectives

After completing this module, you should be able to:

1. charter a scoped data-product review around a real decision, consumer outcomes and frozen identities;
2. construct claim-to-evidence traceability across contract, architecture, verification, operations and governance;
3. review acquisition, semantics, batch/stream processing, storage, metadata, serving and downstream use as one flow;
4. evaluate independent reconciliation, quality, SLOs, observability, incidents and support at consumer-visible boundaries;
5. assess security, privacy, retention, deletion, audit, misuse and external obligations through effective tests;
6. challenge backfill, replay, evolution, deployment, overload, dependency and recovery behavior under realistic conditions;
7. evaluate capacity, cost allocation and unit economics without trading away correctness or resilience;
8. operate mandatory gates, findings, risk acceptance, time-bounded exceptions and decision receipts;
9. define continuous evidence, expiry and material-change triggers so readiness does not become stale; and
10. lead a focused review that is rigorous, non-ceremonial, actionable and auditable.

## Core Exposition

### Charter the decision and freeze the reviewed product

State the decision as a verb: launch v2 to all consumers; accept source migration; expand to regulated data; make the new alias current; continue after an incident; or retire v1. Name the authority and allowed outcomes. `Ready` means all mandatory gates pass for the scope. `Conditionally ready` means narrowly defined noncritical conditions are accepted with owners, controls and expiry. `Not ready` means one or more mandatory gates fail or remain unknown. Avoid “approved with concerns” when nobody knows whether production may proceed.

Freeze identity in the receipt: enduring product and contract version, current alias target, table snapshots or transaction boundaries, source versions/positions, schemas, transformation commit and image, configuration/rules/reference data, policy bundle, environment/region/account, serving deployment, consumer cohort and dependency versions. A diagram describing an intended system cannot prove a different deployed system. Record exclusions and why they do not invalidate the decision.

Tailor mandatory gates to impact, but never remove fundamentals silently. A public research extract and real-time fraud features need different thresholds, not different standards of honesty. Use earlier reviews and automated evidence so the final review synthesizes instead of discovering basics. Require artifacts ahead of the meeting and return incomplete submissions rather than spending the session reading documents aloud.

### Begin with consumers, value, harms, and contracts

Ask who uses the product, for which decision, at what frequency, with what tolerance for error, lateness, absence and change. Include contractual partners, indirect downstreams, people represented in the data, operators and teams paying for the service. Define non-goals and prohibited uses. Verify that a product exists because it changes an outcome, reduces risk or enables a required capability—not because a pipeline can be built.

Review the contract as a whole. Confirm fields, stable identities, types, keys, grain, population, units, time semantics, null/default/enums, history, corrections, deletions, quality, freshness/completeness/availability, access, classification, delivery, support and version policy. Use representative examples and boundary cases. Confirm consumer acceptance maps to the contract rather than a screenshot.

Challenge incentives. A KPI may reward row volume while consumers need accuracy. A freshness target may encourage publishing incomplete state. A unit-cost target may encourage dropping validation or history. A review should state trade-offs and counter-metrics. For high-impact decisions, identify how incorrect data could harm people or create unfair exclusion even when the intended consumer is satisfied.

### Trace sources, meaning, and transformations end to end

Walk one representative record and one aggregate from origin to consumer. For each source, establish authority, ownership, acquisition protocol, completeness expectation, schema, event/effective time, duplicate/change/delete semantics, licensing/purpose and known limitations. Identify where identity, units, time zones, populations, reference data, joins, filters, imputations, aggregations and corrections change.

Every transformation needs durable intent and evidence. Pin code, configuration, runtime and reference data. Review determinism and sources of nondeterminism: current time, unordered inputs, floating aggregation, external lookups and mutable libraries. Verify keys and grain before joins; bound fan-out; define conflict precedence; preserve raw/authoritative receipts; and make destructive overwrites recoverable. Batch boundaries and streaming watermarks should implement the same contract or document intentional differences.

Use lineage to navigate and assess blast radius, not as proof of correctness. Compare declared design lineage with observed runtime lineage and storage/catalog reality. Missing edges, dynamic SQL, manual uploads and exported copies become findings. Confirm every published distribution points back to sources, runs, code, schemas, quality results and policy appropriate to its version.

### Prove correctness and quality independently

Start with conservation and reconciliation. At each trust boundary, account for expected, accepted, rejected, quarantined, duplicate, corrected, deleted and published records or amounts. Use independent source acknowledgments, control totals, ledgers, signed manifests or domain invariants. A pipeline count copied through all stages is not independent. Explain every difference by policy and preserve drill-down identifiers.

Review quality dimensions in consumer context: completeness, validity, consistency, uniqueness, accuracy where ground truth exists, timeliness, distribution, integrity, accessibility and understandability. Every metric names population, denominator, event/state boundary, threshold, owner and response. A 99.9% valid-column rate can hide all failures in a critical tenant. Segment by risk-relevant cohorts and inspect tails.

Test historical behavior: empty/full partitions, late and out-of-order events, duplicates, corrections, deletes, schema changes, reference-data changes, backfills, replay and partial source failure. Test metamorphic and property invariants where exact expected rows are cumbersome. Review quarantines and rejects as product outcomes rather than making them disappear from completeness.

### Review architecture, state, orchestration, and serving

Inspect architecture through failure and ownership boundaries. Identify data plane, control plane, state stores, queues, catalogs, schedulers, secrets/keys, observability, serving, external dependencies and administrative domains. Record consistency and transaction boundaries. Confirm the design does not imply atomicity where only eventual or per-partition behavior exists.

For orchestration, review dependency graph, triggers, schedules, parameters, environment separation, run identity, retries/timeouts, idempotency, concurrency, checkpoints, partial failure, backfill admission and operational state. A retry must not duplicate consumer effects. A backfill must not collide with incremental writes or starve recurring work. Operators need pause, resume, cancel, inspect, reconcile and safely rerun.

For storage, review format, schema/partition evolution, snapshots, compaction, file/object consistency, retention, concurrency and catalog integration. For serving, review workload fit, isolation, query/interface contract, pagination/filter limits, caching/invalidation, materialization refresh, concurrency, tail latency, partial results and exposure of freshness/version/quality. Follow one consumer request back through serving state to the publication receipt.

### Evaluate reliability and observability at the product boundary

Define SLIs from good eligible consumer events or intervals. Freshness is not job duration; completeness is not job success. State eligibility, windows, time basis, unknown telemetry, delayed truth and correction policy. Set objectives from consumer impact, report marginal and joint indicators where necessary, and connect error budgets to release/backfill/risk decisions.

Review telemetry for sources, queues, watermarks, state/checkpoints, transforms, quality, publication, serving, access and consumers. Correlate product/version, source boundary, run/attempt, partition/tenant, snapshot, code/schema/policy and request identifiers across metrics, logs, traces and lineage. Ensure the observability path itself has retention, access, cost and failure behavior. A dashboard without tested alerts, owner and action is decoration.

Inspect incidents and near misses. Were they detected before consumers? Did runbooks work? Did communications identify affected versions and windows? Were corrections reconciled? Did postmortem actions close? Test failure signals, alert routing and runbook steps. Use production history as evidence without assuming absence of incidents proves safety.

### Exercise security, privacy, governance, and audit

Threat-model sources, ingestion, storage, orchestration, metadata, serving, exports, recovery and administrative paths. Consider spoofed producers, tampered records, malicious payloads/queries, object-level authorization failures, exfiltration, credential compromise, supply chain, denial/cost amplification, inference, re-identification, deletion of evidence and insider access. Review third parties and shared responsibility.

Verify classification and purpose propagate to columns, versions, derivatives, logs and exports. Test positive and negative authorization using realistic identities and object/tenant boundaries. Review least privilege, workload identity, secret/key lifecycle, encryption, network controls, masking/tokenization, audit immutability/access and break-glass use. Configuration screenshots do not show effective access.

Trace retention, deletion, consent/permission changes, legal holds, residency and disposal. Execute a deletion through source, base, derived tables, indexes, caches, exports, features, backups and recovery workflow, with evidence and exceptions. Confirm observability avoids leaking sensitive data. Review who can change policies and whether control-plane actions are audited and recoverable.

### Challenge change, deployment, backfill, and lifecycle

Inspect CI/CD from proposed change to evidence and promotion. Require data-aware tests, representative staging, versioned migrations, compatibility checks, policy scans, deployment identity, canary/shadow, output comparison, rollback/forward repair and separation of duties proportional to impact. Rollback must account for data written under the new version; code rollback alone can corrupt state.

Exercise backfill and replay with explicit source/snapshot/code/schema/reference versions, interval/partition plan, concurrency and cost, idempotency, output isolation, reconciliation, cutover and cleanup. Bound admission and provide a kill switch. Validate late data and corrections during the backfill. Preserve run receipts so consumers can distinguish original and restated history.

Review contract versioning and deprecation. Identify current and pinned versions, structural and semantic compatibility, consumer inventory coverage, replacement readiness, coexistence, migration acceptance, notices, exceptions, sunset and retirement gates. Ensure retention and disaster recovery preserve required history without resurrecting retired aliases or deleted data.

### Test capacity, performance, overload, and economics

Model demand in useful units and distributions: records, bytes, keys, partitions, queries, fan-out, state, joins, backfills, corrections and failure replay. Find each stage’s sustainable useful service envelope and bottleneck. Test steady, burst, peak, skew, large records, hot keys, dependency throttling, worker/zone loss, checkpoint overlap, query concurrency and recovery. Record the knee, breaking behavior, bounded queue/age, shedding/priority and backlog drain while new work continues.

Review autoscaling as a delayed control loop: signals, min/max, quotas, startup/state movement, hysteresis, scale-down safety and fallback. Confirm failure reserve and control-plane capacity. A worker maximum above quota or parallelism is fictional. A low mean CPU does not disprove a hot partition, memory, I/O, network, sink or metadata bottleneck.

Reconcile costs to authoritative effective billing and direct/shared/central/unallocated categories. Record allocation rule and coverage. Report cost per SLO-good useful and, where possible, business-value unit with workload and quality context. Verify optimizations do not shift cost downstream, reduce retention/recovery, increase incidents/backlog or relax correctness. Assess forecast, growth, commitments, idle/failover reserve and retirement residue.

### Prove incident response and disaster recovery

Review incident ownership, declaration, severity, roles, communications, evidence preservation, data-impact analysis, consumer notification, correction/restatement and learning. Data incidents can persist after infrastructure recovers; define the affected source/event/partition/version/time population and provide machine-usable correction state.

For disaster recovery, review business impact, RPO/RTO/MTD, failure domains and the complete recovery set: data/history, schemas/contracts, metadata/catalog, lineage/provenance, code/runtime/config, orchestration/checkpoints, policy/identity/keys, serving/routing, deletion intents and audit. Confirm copies are independent from relevant geographic, administrative, credential and corruption failures.

Require a representative full-product drill. Fence writers, choose a clean consistent point, restore in isolation, replay uniquely and in order, apply current policy/deletions, reconcile independently, canary, promote and catch up. Measure from incident/detection through consumer service and record actual recovery point/time capability, capacity, failures and manual steps. A successful backup or database restore is not this gate.

### Assess ownership, support, and socio-technical operation

Map responsibilities across source, product, transformation, platform, security/privacy, domain semantics, finance, on-call, incident command, consumer support, migration, exception and retirement. Names need authority, time allocation, deputies and escalation. A catalog owner field pointing to a defunct group is worse than an explicit unknown because it masks the gap.

Review operator cognitive work. Can an on-call person identify affected consumers and data boundaries under pressure? Do dashboards share identifiers with runbooks? Are dangerous tools guarded, observable and stoppable? Are alerts actionable and load sustainable? Can responders access documentation and credentials during identity/region failure? Exercise communication between producer, platform, security and consumers.

Review supplier and organizational dependencies: vendor support hours, rate/export limits, contract/SLA, portability, exit, source owner change, regulatory authority and funding. A technically redundant product can fail when no team owns a semantic decision or vendor escalation. Record assumptions and residual risks beyond the engineering team’s control.

### Run the review as an evidence and decision workflow

Before the session, publish charter, gates and evidence index. Validate artifact identities and automated checks. Assign domain reviewers to claims, not documents. During review, walk consumer outcome to sources and back, sample evidence reproduction, challenge highest-impact failure scenarios, distinguish facts from assumptions, and capture findings live. Avoid designing the whole solution in the meeting; assign focused follow-up.

For each gate, record `pass`, `fail`, `unknown`, or `not applicable` with rationale and evidence. `Not applicable` needs justification; `unknown` does not become partial credit. Scores may rank improvement opportunities after the gate decision but cannot cancel blockers. Duplicate findings should share one durable owner and verification path.

Classify findings by affected objective and urgency, not embarrassment. Record exact gap, evidence, scenario/impact, required outcome, owner/deputy, due date, dependencies, interim control and closure evidence. Separate issue remediation from accepted residual risk. Verify closures independently where consequence warrants it; a comment saying “done” is not evidence.

### Issue a scoped receipt and keep it current

The decision record states ready/conditional/not-ready, exact scope and identities, mandatory gate outcomes, findings, accepted risks/exceptions, rationale, participants/authority, evidence manifest/digests, effective/expiry dates and re-review triggers. For conditional readiness, specify allowed traffic/consumers/features, compensating controls, monitoring, kill criteria and automatic expiry. Never make an exception broader or longer than the evidence supports.

Trigger re-review on contract/semantic/key/grain/population/policy changes; new sensitive data or purpose; material source/dependency/region/vendor/runtime/serving changes; SLO or recovery-objective changes; major volume/skew/consumer growth; incidents or error-budget exhaustion; version migration; control failure; ownership loss; and evidence expiry. The trigger can reopen only affected gates if traceability proves isolation.

Continuously produce evidence in normal operation: contracts, lineage, run receipts, reconciliations, quality/SLOs, access decisions, billing, version/consumer state, recovery tests and incident outcomes. Periodic whole-product reviews then validate composition and changing context rather than recreating history. The ultimate quality signal is whether consumers can make intended decisions safely and teams can explain, change, operate and recover the product within promises.

## Definitions and Notation

Let a review scope be

$$
S=(product,contract,state,implementation,policy,environment,consumers,dependencies,decision,time).
$$

An evidence item $e$ has identity, scope, observation time, source, method, result, limitations and digest. Evidence supports a claim only when its scope covers the relevant coordinates of $S$ or a documented argument establishes transferability.

For mandatory gates $G_A\subseteq G$, readiness is $\bigwedge_{g\in G_A}[g=pass]$. Define unknown count $U=|\{g\in G_A:g=unknown\}|$ and failed count $F=|\{g\in G_A:g=fail\}|$. Then unconditional readiness requires $U=F=0$. A governance policy may permit conditional readiness for selected noncritical failures, but it changes the decision predicate explicitly; it does not relabel failure as pass.

Traceability graph $T=(N,E)$ contains outcome, contract, design/control, verification, operational evidence, finding/risk and decision nodes. A claim is reviewable when a path connects it to dated evidence and ownership, and counterevidence/failures remain visible. Graph reachability is necessary for traceability but says nothing about evidence truth or sufficiency.

For reconciliation boundary $b$, let $E_b$ be expected identities/amount, $P_b$ published, $R_b$ rejected/quarantined, $D_b$ duplicates removed, $X_b$ governed exclusions/deletions and $U_b$ unexplained. A domain-specific conservation relation accounts for these sets or measures. Readiness generally requires $U_b=0$ at critical boundaries, while approved expected differences are explicit.

Let evidence age at review be $A_e=t_{review}-t_e$. A fixed maximum age is only a baseline. Material changes invalidate evidence even when $A_e$ is small; stable scope may preserve evidence beyond a nominal period when policy permits and transferability is justified.

## Mechanisms, Invariants, or Proof Structure

### End-to-end production review mechanism

1. Charter the exact decision, authority, product/consumer scope, frozen identities, exclusions, gates and evidence policy.
2. Validate consumer outcomes, harms/non-goals, value, ownership, acceptance and the complete contract.
3. Trace sources, authority, semantics, time, transformation, lineage and serving to representative consumer observations.
4. Reconcile independently across trust boundaries; test quality, history, corrections, duplicates, deletes and partial failure.
5. Review architecture, orchestration, state, storage, metadata, serving, dependencies and operability through failure boundaries.
6. Validate consumer-visible SLIs/SLOs, error budgets, correlated observability, alerts, incidents and support.
7. Exercise threats, effective authorization, secrets/keys, audit, privacy, retention/deletion, residency and recovery policy.
8. Challenge deployment, migration, backfill/replay, schema/contract evolution, coexistence, rollback and retirement.
9. Load/failure test useful capacity, queues, overload, autoscaling, catch-up; reconcile cost and SLO-good unit economics.
10. Drill incident response and full-product disaster recovery with clean point, fencing, policy, reconciliation and consumer service.
11. Record each gate, finding, risk and time-bounded exception; decide ready, conditional or not ready without averaging blockers.
12. Issue an immutable review receipt, verify remediation, monitor conditions and reopen gates on material change or evidence expiry.

### Conditional claim: an average score cannot establish mandatory-gate readiness

**Claim.** For at least two mandatory Boolean gates, no threshold on their arithmetic mean below 1 can guarantee their conjunction.

**Proof.** Let $n\ge2$ gates contain one failure encoded 0 and $n-1$ passes encoded 1. Their mean is $(n-1)/n$, which approaches 1 as $n$ grows, while the conjunction remains false. Any threshold admitting this mean declares readiness despite a mandatory failure. Threshold 1 is equivalent to requiring every Boolean gate pass, so the mean contributes no compensating logic. Real reviews also contain unknown/not-applicable states and must preserve them explicitly.

### Conditional claim: component evidence does not imply end-to-end correctness

**Claim.** Passing correctness checks inside every pipeline component does not imply the consumer product is correct when the checks share an incomplete input assumption or omit composition semantics.

**Proof by counterexample.** A source extract drops one tenant before the first controlled boundary. Every downstream stage preserves and reconciles 100% of its input, and each component check passes. The consumer contract requires all tenants, so end-to-end completeness fails. An independent source expectation at acquisition detects the gap. This establishes insufficiency, not that component checks lack value.

### Executable mandatory-gate illustration

This deterministic fixture evaluates twelve mandatory gates. Ten pass; consumer acceptance and full-product recovery fail. It reports `not-ready` despite an 83.3% pass rate. It illustrates conjunction and evidence accounting only; it does not assess the truth, sufficiency, independence, freshness, or applicability of real evidence.

<!-- bijux-verify: {"id":"mandatory-product-review-gates","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"mandatory_gates=12\npassed=10\nfailed=2\nunknown=0\npass_rate=0.833\ndecision=not-ready\nblockers=consumer-acceptance,recovery-drill\n","stderr":""}} -->
```python
gates = {
    "consumer-acceptance": "fail",
    "contract-semantics": "pass",
    "source-reconciliation": "pass",
    "quality-slos": "pass",
    "security-privacy": "pass",
    "lineage-audit": "pass",
    "deployment-backfill": "pass",
    "capacity-overload": "pass",
    "unit-economics": "pass",
    "operations-incidents": "pass",
    "recovery-drill": "fail",
    "version-retirement": "pass",
}

passed = [name for name, result in gates.items() if result == "pass"]
failed = [name for name, result in gates.items() if result == "fail"]
unknown = [name for name, result in gates.items() if result == "unknown"]
decision = "ready" if len(passed) == len(gates) else "not-ready"

print(f"mandatory_gates={len(gates)}")
print(f"passed={len(passed)}")
print(f"failed={len(failed)}")
print(f"unknown={len(unknown)}")
print(f"pass_rate={len(passed) / len(gates):.3f}")
print(f"decision={decision}")
print(f"blockers={','.join(failed + unknown)}")
```

## Alternatives and Trade-Offs

- **One comprehensive review versus progressive specialist reviews:** one session exposes composition but overwhelms participants; progressive reviews build evidence continuously but need a final integration decision.
- **Fixed checklist versus risk-tailored gates:** fixed gates improve consistency; tailoring focuses impact. Maintain a nonnegotiable core and document additions/exclusions.
- **Gate conjunction versus maturity score:** conjunction protects mandatory outcomes; scores prioritize improvements. Report both separately and never use maturity to cancel blockers.
- **Central review board versus product-owned review:** central experts improve consistency/independence but bottleneck delivery; product ownership increases context/speed but risks blind spots. Use accountable owners plus targeted independent reviewers.
- **Synchronous meeting versus asynchronous evidence review:** meetings resolve contested cross-domain claims; asynchronous review scales and enables reproduction. Validate most evidence asynchronously and reserve meetings for decisions.
- **Snapshot certification versus continuous assurance:** a receipt is auditable but ages; continuous checks detect drift but can miss semantic/context change. Combine continuous evidence with scoped periodic/retriggered synthesis.
- **Broad scope versus bounded decision:** broad scope finds system interactions but becomes unactionable; narrow scope closes faster but may omit a failure path. Start from consumer outcome and make exclusions explicit.
- **Production evidence versus controlled tests:** production is representative but uncontrolled and may lack rare failures; tests inject known conditions but simplify reality. Corroborate both.
- **Manual domain review versus automated gates:** humans evaluate meaning and trade-offs; automation is repeatable and frequent. Automate stable predicates while preserving accountable semantic judgment.
- **Independent reconstruction versus shared control totals:** independence detects common-mode pipeline faults; it costs effort and may introduce a second flawed implementation. Use authoritative receipts and review both methods.
- **Blocking launch versus conditional readiness:** blocking protects critical objectives; conditions can enable bounded learning. Conditions require limited scope, controls, monitoring, kill criteria and expiry.
- **Detailed finding backlog versus few critical outcomes:** detail aids execution but obscures priorities; aggregation clarifies decisions but hides owners. Link atomic findings to a small set of objectives/risks.
- **Universal template versus domain-specific annexes:** a universal template supports portfolio comparison; domain annexes cover finance, health, ML or regulated semantics. Keep core evidence vocabulary shared.
- **Evidence retention versus minimization:** long retention supports audit and trend; sensitive logs/results create privacy/cost risk. Retain digests, decisions and necessary artifacts under classified policy.

## Failure Modes and Misconceptions

- **Architecture-diagram review.** Intended boxes and arrows replace deployed identities, values and behavior.
- **Tool-first scope.** “Review the Spark job” omits source acquisition, catalog, serving and consumer decisions.
- **No decision authority.** Participants discuss findings but nobody can block, condition or accept risk.
- **Timeless approval.** A label survives incompatible changes, incidents, owner loss and stale evidence.
- **Checklist theater.** Fields are completed with links that no reviewer reproduces.
- **Average-score laundering.** Many easy passes hide one failed correctness, security or recovery gate.
- **Unknown as partial pass.** Missing consumer or telemetry evidence becomes optimism instead of a blocker.
- **Not-applicable convenience.** A hard gate is removed without scope-based justification.
- **Configuration as behavior.** Enabled encryption, backup or policy is assumed effective end to end.
- **Provider certification inheritance.** Provider controls are treated as product controls despite customer configuration and application semantics.
- **Happy-path fixtures.** Empty, late, duplicate, malformed, skewed, deleted and historical data remain untested.
- **Same-path reconciliation.** Expected and actual totals share the fault and agree perfectly.
- **Rows without meaning.** Schema/count checks ignore grain, units, population and time basis.
- **Accuracy without ground truth.** A metric is labeled accuracy while measuring only format validity.
- **Job SLO substitution.** Scheduler success stands in for consumer freshness/completeness.
- **Average latency/capacity.** Tail queries, hot keys, bursts, failover and catch-up disappear.
- **Retry equals resilience.** Non-idempotent effects duplicate and overload dependencies.
- **Backfill as ordinary run.** History, schema evolution, late corrections and concurrent writes are ignored.
- **Rollback fantasy.** Old code cannot read state written by the new deployment.
- **Lineage absolutism.** A generated graph is assumed complete and correct without runtime/catalog comparison.
- **Owner field as ownership.** The named group lacks authority, deputy, on-call or migration capacity.
- **Security role listing.** Review checks grants but never tests denied object/tenant cases.
- **Privacy at the source only.** Derived data, logs, caches, exports, models and backups escape deletion/purpose rules.
- **Audit volume equals auditability.** Events lack stable identities, integrity, retention or usable queries.
- **Cost minimum as value.** Lower spend comes from missed SLOs, deleted history or shifted consumer work.
- **Allocated equals causal.** A complete bill split is treated as proof a product caused or benefited from every cost.
- **Backup equals DR.** Files restore without catalog, policy, lineage, serving or consumer acceptance.
- **Tabletop equals measured capability.** Roles are discussed but transfer, replay, validation and capacity are not exercised.
- **One quiet month proves no consumers.** Quarterly/annual, cached and external use remains hidden.
- **Deprecation date equals retirement.** Replacement, migration, copies, recovery and exceptions remain unresolved.
- **Permanent exception.** A failed gate becomes normal with no owner, expiry or compensating test.
- **Finding assigned to “team.”** No accountable individual/role, due date or closure evidence exists.
- **Closing by assertion.** The implementer marks done without rerunning the failed evidence.
- **Review as blame.** Teams hide uncertainty instead of surfacing it early enough to manage.
- **Review as design meeting.** The decision is delayed by inventing architecture live rather than assigning follow-up.
- **Review once at launch.** Evidence and composition decay throughout changes, scale, incidents and retirement.

## Worked Examples

### Example 1

A sales mart reconciles every transform stage but misses a region omitted by the upstream export filter. Independent source control totals by region detect the gap. The review fails acquisition completeness even though downstream component tests are flawless, then adds an expected-source manifest before re-review.

### Example 2

A stream reports 99.99% job success and low processing latency. Consumer-visible freshness is poor because event-time watermarks stall for one partition. The review replaces job success with eligible key/window freshness and completeness, adds partition-age alerts and tests source silence versus pipeline lag.

### Example 3

A dataset adds a nullable sensitive column. Schema compatibility passes, but `SELECT *` exports expose it to a role whose allowlist was never updated. Negative authorization and export tests fail the security gate. The producer projects explicit columns, propagates classification and retests before launch.

### Example 4

A backfill of three years uses current exchange rates instead of versioned daily rates. Counts match and code is deterministic, yet finance totals cannot reproduce history. The review blocks publication, pins reference editions and requires per-currency/day reconciliation plus restatement communication.

### Example 5

A feature product meets online latency but training data uses a different point-in-time join and correction window. Online/offline sampled values diverge and model evaluation shifts. The review fails contract/correctness, unifies versioned feature definitions and adds leakage-safe temporal fixtures.

### Example 6

A capacity test reaches target average throughput on uniform keys. Production has a tenant causing 30% of events and a sink quota. A skew/zone-loss test produces growing backlog and misses drain time. The review rejects a worker-count remedy until repartitioning, isolation and sink quota are validated.

### Example 7

All storage backups are green. A drill restores the table but the catalog points to expired metadata and historical grants expose restricted columns. Recovery is not consumer-ready. The team protects the dependency-closed recovery set, applies current policy and adds negative access/reconciliation to the RTC stop condition.

### Example 8

The product’s monthly cost falls 25% after retention is cut. Unit cost per raw row improves, but correction coverage and disaster recovery fail. The review uses cost per SLO-good unit, includes incidents/rework and blocks the optimization until retention meets contract and recovery horizons.

### Example 9

V1 has no observed queries for 60 days, yet an annual regulatory extract and partner copy exist outside logs. The version-retirement gate stays unknown. Owners attest use, migrate and reconcile the exports, then a targeted denial canary and preserved-history plan support retirement.

### Example 10

A product passes 10 of 12 gates. Leadership proposes accepting its 83% score. Consumer acceptance for billing and a full recovery drill are failed. The decision remains `not ready`; each blocker receives an owner and test. Two weeks later both pass against the same frozen version and a new receipt records `ready`.

## Cross-Program Connections

- [DE-010](010-designing-a-reproducible-data-boundary.md), [DE-020](020-validating-an-analytical-model-against-business-questions.md), [DE-040](040-testing-a-multi-stage-batch-pipeline.md), and [DE-050](050-designing-an-operable-data-workflow.md) provide earlier vertical reviews of boundaries, analytical modeling, batch and orchestration.
- [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) and [DE-070](070-operating-a-transactional-table-format.md) provide streaming and storage operational evidence.
- [DE-071](071-completeness-validity-accuracy-and-consistency.md), [DE-073](073-reconciliation-tests.md), [DE-076](076-data-contracts.md), and [DE-080](080-building-quality-gates-for-a-data-product.md) form the correctness and contract core.
- [DE-081](081-technical-operational-and-business-metadata.md), [DE-082](082-dataset-and-column-lineage.md), [DE-083](083-data-catalogs.md), [DE-086](086-access-control-for-analytical-data.md), [DE-088](088-retention-and-deletion.md), and [DE-089](089-auditability-and-provenance.md) form the metadata and governance evidence chain.
- [DE-091](091-warehouses-query-engines-and-serving-stores.md), [DE-094](094-data-apis.md), [DE-095](095-feature-and-training-dataset-pipelines.md), [DE-096](096-freshness-and-completeness-slos.md), [DE-097](097-pipeline-capacity-and-cost.md), [DE-098](098-disaster-recovery-for-data-products.md), and [DE-099](099-versioning-and-deprecating-datasets.md) provide product-serving and lifecycle gates.
- [API-090](../../28-api-and-service-engineering/modules/090-evolving-an-api-without-coordinated-consumer-releases.md) connects interface-wide evolution, while this module adds persistent historical state, reconciliation, batch/stream and data governance.
- [PLAT-090](../../29-platform-engineering/modules/090-reviewing-platform-failure-blast-radius.md) connects shared-platform dependencies and failure cuts.
- [SYSENG-078](../../26-systems-engineering/modules/078-acceptance-criteria.md) and [SYSENG-100](../../26-systems-engineering/modules/100-conducting-a-whole-system-review-of-a-software-intensive-capability.md) connect evidence-based acceptance and whole-system boundaries.

## References

- Google, “Evolving SRE Engagement: Production Readiness Reviews,” *Site Reliability Engineering*. <https://sre.google/sre-book/evolving-sre-engagement-model/>
- Google, “Improve and Optimize Data Processing Pipelines,” *Site Reliability Engineering Workbook*. <https://sre.google/workbook/data-processing/>
- Amazon Web Services, *Data Analytics Lens*, current AWS Well-Architected guidance. <https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/analytics-lens.html>
- World Wide Web Consortium, *Data Catalog Vocabulary (DCAT) — Version 3*, W3C Recommendation. <https://www.w3.org/TR/vocab-dcat-3/>
- World Wide Web Consortium, *Data on the Web Best Practices: Data Quality Vocabulary*. <https://www.w3.org/TR/vocab-dqv/>
- OpenLineage project, “Object Model,” current specification documentation. <https://openlineage.io/docs/spec/object-model/>
- Apache Iceberg project, “Table Spec,” current specification. <https://iceberg.apache.org/spec/>
- National Institute of Standards and Technology, *The NIST Cybersecurity Framework 2.0*. <https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20>
- National Institute of Standards and Technology, *Privacy Framework: A Tool for Improving Privacy through Enterprise Risk Management*. <https://www.nist.gov/privacy-framework/privacy-framework>
- OWASP Foundation, “OWASP API Security Project.” <https://owasp.org/www-project-api-security/>
- OpenTelemetry project, “Signals,” current documentation. <https://opentelemetry.io/docs/concepts/signals/>
- FinOps Foundation, “Unit Economics,” current FinOps Framework capability. <https://www.finops.org/framework/capabilities/unit-economics/>

## Exercises

### Exercise 1

Recompute the executable decision and prove its general average-score claim for 100 mandatory gates with one failure. Then design a policy for `not applicable`, `unknown`, conditional readiness and exception expiry that does not relabel blockers as passes.

### Exercise 2

Create an end-to-end evidence graph for an hourly payments dataset from three source systems through streaming normalization, lake table, daily reconciliation, warehouse model and partner API. Include frozen identities, claims, independent evidence, owners, limitations and at least three failure paths.

### Exercise 3

A product reports 99.95% job success, 99.9% schema validity, \$0.08 per million input rows, a 15-minute backup interval and no incidents in 90 days. Critique what each observation establishes and design the missing consumer-visible correctness, reliability, security, economics and recovery evidence.

### Exercise 4

Design a 90-minute production review session and its asynchronous preparation for a customer feature product with online/offline stores, personal data, 40 consumers, one critical model, peak skew, two regions and a pending v2 migration. Define participants, gate order, evidence sampling, decision outcomes and follow-up receipt.

### Exercise 5

An estate has 500 “production-ready” badges without version scope, 35% unknown owners, schema-only tests, 55% lineage coverage, CPU-only dashboards, no cost reconciliation, and backups never restored. Design a risk-prioritized adoption program for evidence-gated product reviews without stopping every product simultaneously.

## Answers to the Exercises

### Answer 1

The fixture contains 12 gates, 10 passes and two failures, so pass rate is $10/12=0.8333\ldots$, printed `0.833`; conjunction is false and the decision is `not-ready`. For 100 gates with 99 passes and one failure, average is 0.99 while conjunction remains false. Thus even an apparently excellent score cannot establish all mandatory predicates.

`Not applicable` requires a scope-based rationale and reviewer/authority approval; remove it from the applicable conjunction but retain it visibly. `Unknown` remains a blocker for a mandatory gate because absence of evidence is not pass. Conditional readiness is permitted only for predefined noncritical gate classes or an explicit risk decision; record limited consumers/traffic/features, compensating controls, monitoring, kill conditions, owner, due date and automatic expiry. Exceptions preserve the original `fail`/`unknown`, name who accepts residual risk, and expire or trigger re-review. Closure requires new evidence and a revised receipt, not editing history.

### Answer 2

Freeze product/contract, reviewed hour and source positions, schemas, normalization code/image/config, lake snapshot, reconciliation rule version, warehouse model version, API deployment/policy and three source identities. Outcome claims include no committed payment loss/duplication, amount/currency integrity, one-hour completeness, authorized partner access, correction behavior and recovery. Link each to contract clauses and owners.

For each source, use an independently produced transaction/count/amount receipt by partition/currency/hour. At ingestion record accepted/rejected/duplicate identities and source acknowledgment. Link runtime lineage/run IDs to code/schema and lake snapshot. Reconcile lake unique payments and signed amounts to source controls, including explicit rejects/deletes. Reconcile warehouse aggregates independently by currency/merchant/day. At API, run contract examples, negative partner/merchant authorization, freshness/version headers and response-to-warehouse keys. Attach SLO windows, alerts, load/skew/failure results, billing allocation and recovery drill receipt.

Failure path one: source three silently omits a merchant; downstream internal counts agree, independent source manifest fails. Path two: duplicate replay crosses checkpoint; source-to-lake identity conservation and partner sampled effects detect it. Path three: API object authorization exposes another merchant; negative tests and access audit fail despite correct data. Additional paths include stale warehouse materialization, currency-reference drift and regional recovery with old policy. Every evidence node records source/method/date/result/limitations/digest and accountable owner; missing coverage remains visible.

### Answer 3

Job success shows scheduler/execution status under its definition, not source completeness, correct values or consumer freshness. Schema validity measures structural conformance on its denominator, not semantic accuracy or missing records; inspect the failing 0.1% by risk cohort. \$0.08 per million input rows is a technical ratio without full-cost conservation, useful output, SLO or consumer value. A 15-minute backup schedule is an intended point frequency, not readable clean recovery point or consumer RTO. No incidents may reflect good behavior, low exposure or weak detection/reporting.

Define eligible consumer intervals/events and measure joint/marginal freshness, completeness, correctness and availability with unknown telemetry bad or explicit. Reconcile source control totals, unique keys and financial/domain amounts across rejects, duplicates, corrections and deletes. Test semantics, historical/backfill and consumer examples. Add negative object/tenant authorization, classification, secret/key, deletion-through-derivatives/backups, audit and threat tests.

Measure full effective cost conservation across compute, storage, requests, network, licenses, observability, support and reserve; divide by SLO-good outputs and relevant business decisions, with downstream shifts. Run representative peak/skew/dependency/zone tests, backlog drain and alert/runbook exercises. Perform full-product recovery from isolated clean copies through catalog, schemas, lineage, current policy, serving, reconciliation and consumer access; measure actual point and time from incident to declared service. Review incidents plus synthetic detection because absence alone is not proof.

### Answer 4

Asynchronously publish charter, exact v2 decision/scope, identities, mandatory gates and evidence index one week ahead. Product owner owns submission; source/domain owners validate semantics; ML consumer owns outcome/leakage acceptance; data engineer owns pipelines/online-offline reconciliation; platform/SRE owns capacity/regions/operations; security/privacy owns personal-data controls; FinOps reviews cost; review lead controls decision; 40 consumer owners provide inventory status, with representatives attending and critical model owner mandatory.

Automated checks validate links/digests, contracts, schemas, lineage coverage, quality/SLO windows, access/deletion tests, load/recovery reports, costs and v1/v2 status. Reviewers leave questions before the meeting. The 90 minutes: 0–10 charter/decision and unresolved prior findings; 10–25 consumer/model outcome, harms and v2 acceptance; 25–40 source semantics and point-in-time online/offline reconciliation; 40–52 privacy/security/deletion and negative access; 52–64 peak skew, two-region failure, SLOs/incidents; 64–74 deployment/backfill/version migration/rollback; 74–82 full-product recovery and economics; 82–90 gate roll-call, decision and owners.

Sample one customer feature from source/event time through offline snapshot, online value and model request; reproduce one discrepancy, one denied identity, one skew test and one recovery receipt. Outcomes are ready, narrowly conditional, or not ready for frozen v2/cohort. Receipt records every gate, evidence digest, blockers, risks/exceptions, allowed scope, monitors/kill criteria, owner/dates, expiry and triggers. Follow-ups rerun failed evidence; they do not retroactively alter the original receipt.

### Answer 5

Declare badges historical claims, not revoke production blindly. Inventory products, consumers, sensitivity, business/regulatory impact, incidents, change rate, data volume, external exposure and shared dependencies. Prioritize safety/finance/personal/regulatory and externally served products, ownerless high-use surfaces, known data incidents and concentrated platform failure cuts. Freeze new unconditional badges until a versioned receipt schema exists.

Establish a small mandatory core: owned consumer contract; source authority and independent reconciliation; quality/freshness/completeness; effective security/privacy/deletion; lineage/audit identity; operable deployment/backfill; representative capacity/overload; full-cost good-unit economics; incident ownership; product recovery; and version/retirement. Add domain annexes. Train review leads and product owners; provide evidence templates and automation, not one giant central board.

Improve enabling systems in parallel. Resolve owners with deputies/escalation, starting with high impact. Combine runtime, SQL, catalog, BI and export evidence to raise lineage coverage and show unknowns. Add source receipts and semantic/contract tests beyond schemas. Instrument useful throughput, backlog/watermarks, consumer SLOs, dependencies, access and costs instead of CPU alone. Normalize bills and preserve unallocated remainder. Start component restores, then representative full-product drills; remediate shared recovery gaps once for dependent products.

Pilot on a small diverse cohort, measure review time/findings/incidents and refine. Review remaining products in risk waves while continuous gates apply to new material changes. Use conditional receipts for bounded lower-risk gaps with controls and expiry; failed critical gates block only the relevant launch/expansion where continued current operation has a separately assessed risk. Trigger immediate review on incidents, sensitive expansion, owner loss or major migration. Publish estate coverage, unknowns, failed gates, overdue exceptions and verified closure—not a new vanity badge count.
