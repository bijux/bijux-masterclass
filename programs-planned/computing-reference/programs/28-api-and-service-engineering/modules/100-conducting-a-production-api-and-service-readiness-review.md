---
module_id: API-100
program: API & Service Engineering
level: 2
module_number: 100
title: Conducting a Production API and Service Readiness Review
status: complete
last_verified: 2026-09-02
---

# Conducting a Production API and Service Readiness Review

## One-Page Review

### Governing question

How can accountable reviewers decide—using current artifact-bound evidence rather than confidence, checklist averages, or deadline pressure—whether a specific API/service change is ready for a bounded production rollout, conditional exposure, or no-go?

### Essential definitions

- A **production readiness review (PRR)** is a risk-scaled evidence review of a specific service/change, rollout, operating model, consumer impact, and recovery plan.
- A **readiness claim** is a falsifiable statement that must hold for the proposed production scope, such as “replayed creates produce at most one charge.”
- **evidence** is a reproducible result bound to artifact, configuration, environment, workload, time, tool and owner; a document asserting that a test exists is not the test result.
- A **blocker** is an unmet non-negotiable invariant whose plausible consequence exceeds the authorized risk appetite; blockers cannot be averaged away.
- A **residual risk** is uncertainty remaining after controls/evidence, with explicit scenario, impact, likelihood basis, detection, mitigation, owner, expiry and decision authority.
- A **conditional go** permits only a narrower declared scope while enforceable conditions/guardrails hold; it is not “go and fix later.”
- A **rollout unit** is the smallest independently observable and reversible consumer/tenant/region/version/traffic cohort.
- **rollback** restores a prior deploy/config route where semantics allow; **roll-forward/recovery** repairs irreversible data/effects or incompatible migrations.
- A **readiness record** preserves scope, claims, evidence digests, findings, decisions, conditions, owners, dates, reviewers and follow-up outcomes.

### Central model, mechanism, or theorem

Let required critical claims be $C$, evidence record $e(c)$, unresolved blockers $B$, rollout/rollback/recovery readiness $Q$, and residual risks within authorized appetite $A$. A go decision requires conjunction:

$$
G=\left(\bigwedge_{c\in C} valid(e(c))\right)\land(B=\varnothing)\land Q\land A.
$$

An average maturity score is invalid: nine excellent areas cannot compensate for one unauthenticated administrative operation or unrecoverable destructive migration. Evidence strength is limited by the weakest relevant assumption—scope, freshness, fidelity, provenance or oracle. Decision scope may be narrowed until the conjunction becomes true and enforceable.

### Critical invariants

The exact artifact/config/schema/policy/topology/consumer/traffic/region rollout is identified and matches evidence. Product owner, service/API owner, operations/on-call, security/privacy/data and dependency/consumer owners are real and accept responsibilities. Contract, compatibility, authorization, tenant/object/property boundaries, input/errors/idempotency/consistency and effects are verified.

SLOs, telemetry health, capacity/fault headroom, deadlines/retries/shedding/backpressure, dependencies, gateway/discovery/mesh, deploy/migration/canary/rollback/recovery, incident/support/status/runbooks and consumer communication are tested. No critical finding is “accepted” by someone without authority. Exceptions are narrow, compensating, observable, expiring and rehearsed. The decision includes launch window, cohort gates, abort criteria, command roles, post-launch observation and re-review triggers. Review evidence is sanitized and immutable enough for audit/learning.

### Common failures

Generic checklist copied to every service; reviewing architecture instead of exact release; “tests green” without scope; screenshots without raw result; evidence from old artifact/config/data; self-assessment only; ownership by mailing list; missing consumers; additive schema assumed compatible; authentication treated as authorization; happy-path/no abuse; retry/load/capacity omitted; no failure/recovery; rollback claimed despite irreversible migration; canary without representative traffic or effect oracle; alert exists but delivery/runbook untested; status page no owner; third-party limits ignored; averages hide blockers; high score means go; conditional go has no enforcement; deadline/rank overrides risk silently; action items unowned/unexpired; and review ends at launch.

### Compact example

Payments p12 passes unit, contract, integration, security and load tests, but its migration makes `idempotency_key` uniqueness non-reversible before all p11 consumers drain. A 5% canary cannot expose duplicate effects from old retrying clients because they are excluded. The PRR records a blocker, not “95% ready.” The team first deploys backward-compatible dual-read/write plus uniqueness evidence, canaries by consumer version, rehearses roll-forward repair, and only then receives conditional go. **Conclusion:** review joins change topology, consumer reality, effects, and recovery; test volume alone is not readiness.

### Connections

This review synthesizes [Behavioral Contracts](021-api-contracts-and-behavioral-guarantees.md), [Threat Modeling](041-api-threat-modeling.md), [Object Authorization](046-object-level-authorization.md), [Async Replay and Evolution](070-designing-an-asynchronous-api-for-replay-and-evolution.md), [Failure Amplification](080-preventing-failure-amplification-across-service-calls.md), [Compatibility](081-backward-and-forward-compatibility.md), [Consumer Evidence](085-consumer-inventory-and-usage-evidence.md), [Independent Evolution](090-evolving-an-api-without-coordinated-consumer-releases.md), [Contract Testing](094-contract-testing.md), [Integration Testing](095-integration-and-end-to-end-api-testing.md), [Robustness](096-fuzzing-and-robustness-testing.md), [Telemetry](097-api-metrics-logs-and-traces.md), [Capacity](098-latency-and-capacity-testing.md), and [Onboarding](099-developer-portals-and-onboarding.md).

## Governing Question

How should reviewers scope, prepare, challenge, decide, record, execute, and learn from a production API/service readiness review so that the result is proportional, independent, actionable, and defensible?

## Why This Matters

Production failures usually cross review categories: a compatible field change triggers old SDK retry behavior; retry amplification saturates a dependency; overload logs leak tokens; a rollback returns code but not data; an operator cannot identify affected consumers. Separate green checks miss composition.

A PRR creates a deliberate integration point for evidence and accountability. Google SRE describes PRRs as analysis of all production concerns before operational responsibility, and reliable launch practice as lightweight, robust, thorough, scalable and adaptable. The checklist is a prompt for judgment, not the judgment itself.

Bad reviews impose toil without reducing risk. They reward document completion, encourage late theater, apply the same questions to every change, and let deadline pressure convert unknowns into approvals. Teams learn to game them.

An effective review begins early, scales by blast radius/novelty/reversibility, requests evidence from normal delivery systems, uses domain specialists where risk requires, and produces an enforceable launch/recovery decision. It also feeds recurring gaps back into platform controls and future design.

## Prerequisites and Retrieval

Retrieve the entire API program as relevant, especially [Outside-In Requirements](011-outside-in-api-requirements.md), [Contracts](021-api-contracts-and-behavioral-guarantees.md), [Predictable Endpoints](040-implementing-a-predictable-service-endpoint.md), [Threat Modeling](041-api-threat-modeling.md), [Object Authorization](046-object-level-authorization.md), [Async Evolution](070-designing-an-asynchronous-api-for-replay-and-evolution.md), [Reliability and Amplification](080-preventing-failure-amplification-across-service-calls.md), [Compatibility](081-backward-and-forward-compatibility.md), [Deprecation](084-deprecation-and-sunset.md), [Consumer Inventory](085-consumer-inventory-and-usage-evidence.md), [Product Ownership](089-api-product-ownership.md), [Gateways](091-api-gateways-and-edge-responsibilities.md), [Discovery](092-service-discovery-and-routing.md), [Mesh](093-service-mesh-relationships.md), [Testing](094-contract-testing.md), [Integration](095-integration-and-end-to-end-api-testing.md), [Robustness](096-fuzzing-and-robustness-testing.md), [Telemetry](097-api-metrics-logs-and-traces.md), [Capacity](098-latency-and-capacity-testing.md), and [Onboarding](099-developer-portals-and-onboarding.md).

Retrieve exact artifact/SBOM/provenance, configuration/flags/secrets/policies, contract/schema/migrations, topology/trust/data flows, product/audience/data/terms, consumer/dependency inventories, SLO/error budget, test/review results, threat/privacy/abuse assessments, capacity envelope, dashboards/alerts/telemetry health, deploy/canary/abort/rollback/roll-forward, backup/restore/DR, incident/on-call/runbooks/status/support, open findings/exceptions, launch forecast/window/command, and prior incidents/reviews.

## Learning Objectives

After completing this module, you can:

1. define a risk-scaled PRR scope from change, blast radius, novelty, privilege, state, consumers, traffic and reversibility;
2. convert vague checklist items into falsifiable readiness claims and artifact-bound evidence requests;
3. distinguish design description, intended control, test result, operational rehearsal, production observation and residual uncertainty;
4. review product/consumer, contracts, implementation, security/privacy/abuse, reliability, capacity, dependencies and operations as a composed system;
5. challenge deployment, migration, canary, abort, rollback, roll-forward, data repair and disaster recovery claims;
6. identify blockers and prevent maturity scores or authority gaps from hiding them;
7. construct enforceable go, conditional-go and no-go decisions with owners, conditions, expiry and re-review triggers;
8. run a safe launch command/observation process and reconcile actual outcomes with predictions;
9. preserve a sanitized decision/evidence record and convert findings into durable automated/platform improvements; and
10. explain why readiness is scoped/current evidence, never permanent certification.

## Core Exposition

### Trigger review early and proportionally

Define triggers: new public/privileged/high-data API; material contract/auth/data/consistency change; new gateway/mesh/discovery/dependency; migration; region/tenant expansion; large launch; changed reliability/capacity; operational ownership transfer; or incident-driven redesign.

Classify risk by user/business impact, data sensitivity, privilege/effects, external/uncontrolled consumers, state/migration irreversibility, dependency/blast radius, novelty, traffic/growth, failure detectability and recovery time. Do not collapse to a number; use factors to select depth and specialists.

Start during design for irreversible choices and re-evaluate near launch against exact artifacts. A lightweight low-risk template change can rely on automated evidence; a payment migration needs security/data/SRE/consumer scrutiny and rehearsal.

Name review sponsor, coordinator, accountable decision authority and independent reviewers. Authors supply evidence and answer; reviewers challenge assumptions. Independence is proportional, not adversarial ceremony.

### Freeze the proposed production scope

Write one release identity: repository/source revision, built artifact/image digests and provenance/SBOM, contracts/SDKs, database/event migrations, config/flags/policies/secrets/key revisions, infrastructure manifests/resources, gateway/routes/discovery/mesh, dependencies/versions, regions/tenants/consumer cohorts and rollout schedule.

Draw system/context, request/async/data/trust/deploy and failure-recovery flows. Mark external entry, termination/re-encryption, identity/context, authoritative state/effects, queues, caches, third parties, operator/admin and telemetry paths.

Define what changes and does not, user/consumer tasks, success/degradation/failure, max blast radius and rollback unit. If review evidence targets p11 but release rebuilt p12, the decision no longer applies.

Maintain a change ledger between review and launch. Re-review when artifact, critical config, contract/schema, dependency, scope or assumptions change beyond policy.

### Turn checklist topics into claims

“Has monitoring” becomes: “For each SLO failure and critical safety outcome, a tested signal detects within X, pages the active responder, links a usable runbook, and telemetry pipeline loss is visible.” “Has rollback” becomes: “The exact cohort can return to known-good application/config/schema compatibility within Y without losing/corrupting effects; rehearsal evidence attached.”

Each claim records criticality, rationale/failure scenario, scope, owner, evidence type/location/digest/date, assumptions, result, limitation and expiry. Evidence types have different strength: design inspection; static validation; unit/property/contract/integration/fuzz/load/security; failure/recovery rehearsal; canary; production history.

Prefer independent mechanisms for high-risk claims. Schema compatibility plus old-client contract tests plus usage inventory is stronger than one diff tool. Authorization needs negative object/tenant/action tests, threat review and boundary enforcement—not a screenshot of scopes.

Automate recurring evidence but keep its coverage visible. A green job whose selection excludes old clients is not supporting evidence for them.

### Review product, ownership, and consumers

Confirm problem/audience/non-goals, product owner and decision rights; API/service/on-call/security/privacy/data/dependency/support owners; support and lifecycle commitments; pricing/quota/terms/data/residency; launch forecast/communications.

Inventory internal/external/partner clients by application/version/operation/environment/owner/last seen, plus unknown-public-consumer policy. Map compatibility and rollout order. Usage evidence informs but absence over a short window is not proof of no consumer.

Check onboarding/docs/contracts/examples/SDKs/sandbox/status/support/changelog/deprecation/migration are current and audience-authorized. Ensure consumers can diagnose errors, rotate credentials, respect limits, retry safely and contact an owner.

For deprecation/removal, verify announcements/acknowledgments, migration tools, usage decline, exception owners and sunset behavior. A launch that strands one high-impact consumer is not ready because aggregate adoption is high.

### Review contract and boundary correctness

Trace every operation: resource/action, method/protocol, request validation, authn context, action/object/property/state authorization, domain command/query, transaction/effect, concurrency/idempotency, response/error and observability.

Verify OpenAPI/JSON Schema/Protobuf/GraphQL/AsyncAPI contracts are canonical/versioned and implemented. Examine ambiguity, null/absence, defaults, enums, numeric/time/Unicode, pagination/filter/order, errors/problem codes, content negotiation, headers, caching/conditionals, long/bulk/stream behavior and limits.

Check backward/forward/application compatibility across deployed versions, not only wire schema. Test old/new clients/providers, rolling mixed versions, unknown fields/enums, persisted queries/events, replay and independent release order.

Correctness under ambiguity: idempotency key/fingerprint/retention, response-loss retry, concurrency/ETag/version, atomic state/effect/outbox, dedupe, ordering/partition, consistency/read-after-write, partial result/degradation and outcome lookup. Require authoritative oracles.

### Review security, privacy, and abuse

Threat model assets/actors/trust/data flows/entry/admin/supply chain and abuse economics. Verify identity issuer/audience/expiry/key rotation, credential storage/rotation/revocation, scopes, tenant/action/object/property authorization, default deny and context propagation.

Test input/parsing/mass assignment/enumeration/exposure, injection/SSRF/file/URL, replay/signing, rate/quota/resource amplification, GraphQL cost, bulk/export, webhooks/events, gateway/mesh bypass, admin/debug and error/log leakage. Protect control planes and nonpublic docs/catalog.

Classify data, minimize collection/response/telemetry, define purpose/consent where required, encryption/key/retention/deletion/residency/access/audit and subject/incident workflows. Include backups/caches/logs/test/sandbox.

Verify build/dependency/image/SDK/spec provenance, review, vulnerability policy, secrets scanning and incident response. NIST SSDF provides high-level secure development practices; OWASP ASVS 5.0 provides versioned technical security verification requirements. Select applicable requirements and preserve exact version/evidence; claiming an acronym is not verification.

Security findings state exploit scenario/reachability/impact/affected versions/controls/detection/owner. Only authorized risk authority can accept residual security/privacy risk.

### Review reliability and distributed behavior

For each dependency/hop, define purpose, SLO/limit, identity, timeout/deadline, retry owner/max/backoff/jitter, idempotency, circuit/bulkhead/pool/queue, load shedding/backpressure, degradation, cache/staleness, discovery/health/drain and failure behavior.

Calculate worst-case retry/fan-out amplification and verify under fault/overload. Propagate deadlines/cancellation; distinguish logical calls/attempts/effects. Test dependency slow/down/partial/wrong, DNS/discovery stale, proxy/control-plane failure, instance/zone/region loss, clock/key/config changes and recovery.

For events/async: delivery/ack, duplicate/reorder/gap, partition/key, schema/version, poison/dead-letter/quarantine, replay/redrive, backpressure/lag, consumer state/effect and disaster recovery. For streaming: connection churn, message flow control, cancellation/resume and long-lived version changes.

Check data consistency/integrity, backups/restore, RPO/RTO, reconciliation/repair and operator safety. “Eventually consistent” is not a failure policy.

### Review capacity, performance, and cost

Require a current capacity envelope for exact artifact/config/resources and production-relevant logical workload mix/data/cache/auth/protocol/dependencies, using correct open/closed model. Evidence includes scheduled/dropped/admitted/correct/rejected/timeout/retry/effect, latency distributions, resource/queue/dependency bottleneck, saturation knee and variance.

Validate peak/launch/growth forecasts, tenant/key skew, bulk/expensive queries, cache cold/warm, autoscaling detection/provision/readiness/routing lag, quota/admission and cost per correct operation. Add deploy and failure-domain headroom.

Test beyond capacity for early cheap shedding, priority/degradation, bounded queues/deadlines/retries, no restart cascade and full recovery. Soak covers slow leaks/compaction/backlog/telemetry growth. Load generator/environment limits are separately proven.

Check downstream/third-party quotas and cost; a service that survives by overwhelming a dependency is not ready. Define capacity ownership, dashboards/alerts and revalidation triggers.

### Review telemetry, SLOs, and operations

SLOs reflect user/consumer correctness, latency, availability/freshness/degradation at named boundaries, with traffic inclusion and error-budget policy. Confirm recent baseline where existing, or launch guardrails for new service.

Metrics separate logical operations/attempts/effects with bounded route/error/version dimensions and aggregatable histograms. Logs are structured/redacted/correlated. Traces model gateway/service/dependency/retry/fan-out/async paths with untrusted context handling. Telemetry health/drop/export/query/alert delivery is monitored.

Run synthetic scenarios and validate metric deltas, trace topology, log redaction, dashboard queries, alert threshold/evaluation/delivery and runbook action. Include deploy/config/feature correlation. No-signal behavior and collector outage are explicit.

On-call has named primary/backup, access/training, dashboards, common/novel failure troubleshooting, safe commands, escalation/dependencies, incident roles, status/customer/support communication and postmortem/follow-up. Page load/false positives must be sustainable.

### Review deployment, migration, and reversibility

Build once with provenance; promote exact artifact. Validate configuration/secrets/policy/schema compatibility. Staged rollout uses small independently observable/reversible cohorts and representative high-risk consumers/traffic, not only easy health checks.

Define preconditions, step owner, duration, observation, success, abort threshold, hold and next step. Automated gates enforce critical thresholds, while incident commander can halt. Avoid simultaneous unrelated changes.

Rollback plan identifies code/config/route/schema/data compatibility and time. Forward-only database/event changes need expand/contract, mixed-version matrix, backup/restore or roll-forward repair. Rehearse exact commands/permissions/time and failure midway. Rollback that worsens data is not a rollback.

Define kill/degrade flags with secure authority, tested semantics, dependency on control plane and cleanup. Canaries require effect/correctness oracles and enough volume/duration for tail/rare failures. Consumer and server rollouts may be independent; stage order accordingly.

### Review disaster recovery and existential failure

List loss/corruption/unavailability of region, control plane, identity/key, database, broker, object store, configuration, registry, DNS, gateway/mesh, telemetry and third party. Define detection, failover/fail-closed/degradation, RPO/RTO, capacity/residency/consistency and authority.

Restore is proven by timed exercise that validates data/application semantics and credentials, not backup job success. Test failback and reconciliation to prevent split-brain/duplicate effects.

Identify manual irreducible recovery and ensure instructions, permissions, people and dependencies are available during outage. Protect backups/runbooks/credentials from the same failure domain and attacker.

If full DR is outside initial scope, constrain region/traffic/data and obtain authorized residual-risk decision with expiry—not an unqualified global launch.

### Conduct the review meeting as a decision

Pre-read contains scope, diagrams, claim/evidence matrix, unresolved findings, launch/recovery plan. Reviewers inspect evidence beforehand; meeting focuses on assumptions, composition, gaps, disagreements and decision—not reading a checklist aloud.

Classify findings: blocker; required pre-launch; enforceable conditional; post-launch improvement; not applicable with rationale. Record scenario/impact/evidence gap/action/owner/due/verification. Do not label unknown risk “low” merely because no incident occurred.

Decision options:

- **Go:** conjunction holds for stated scope; launch plan/gates active.
- **Conditional go:** narrower scope and enforceable conditions make conjunction hold; conditions have telemetry/owner/expiry/abort.
- **No-go:** blocker/critical unknown/operational inability remains; state evidence required for reconsideration.

Decision authority cannot waive legal/regulatory/security/data/operational obligations it does not own. Dissent and rationale remain in record. Scores can prioritize improvement but never substitute for blocker logic.

### Execute launch and post-launch verification

Before launch revalidate artifact/config/dependencies/consumer communication, staffing/access, capacity/error budget, dashboards/alerts, backup and rollback. Start launch record and command channel; declare roles/time zones.

At each cohort compare correct outcomes, latency/error/degradation, logical/attempt/effect, resource/queue/dependencies, auth/security denies, consumer/support and telemetry health against baseline/threshold. Hold long enough for relevant cadence; do not outrun observation.

Abort early at threshold. Preserve evidence and stabilize using rehearsed rollback/degrade/shed/recovery. Do not negotiate critical thresholds mid-incident without named authority and updated risk.

After full rollout maintain enhanced observation through delayed effects, billing, retries, batch jobs, token/key rotations, cache/compaction and consumer cycles. Reconcile predicted versus actual capacity/errors/support; close conditions only with evidence.

### Learn and improve the system

Review escaped incidents, near misses, false blockers, missing/low-value questions, approval delay and evidence toil. Convert recurring checks into build/policy/platform automation with visible coverage, not opaque compliance.

Curate templates from incidents and domain principles. Google SRE launch guidance notes checklist questions should be substantiated and concrete, and continually maintained. Delete obsolete questions; specialize unusual launches.

Feed findings upstream: contract/style rule, SDK default, gateway policy, auth library, load-test harness, telemetry convention, migration framework, catalog ownership, runbook or training. The PRR improves the paved road rather than repeatedly taxing teams.

Re-review on material scope/artifact/contract/data/security/dependency/topology/traffic/ownership/SLO/incident change or evidence expiry. Readiness is a living claim, not certification.

## Definitions and Notation

Let $C$ be critical readiness claims, $e(c)$ the evidence record for claim c, $valid(e)$ require applicable scope/artifact, sufficient oracle/coverage/fidelity, provenance, pass result and freshness, $B$ unresolved blockers, $Q$ enforceable rollout/abort/rollback/recovery capability, and $A$ residual risks within authorized appetite. Let $D$ be proposed production scope and $D'\subset D$ a narrowed conditional scope.

A **finding** connects a failure scenario to evidence gap/control/action. **Assumption debt** is a material unverified premise with owner/expiry. **guard period** is enhanced post-launch observation through relevant delayed cycles. **re-review trigger** invalidates the prior decision when scope or evidence changes.

## Mechanisms, Invariants, or Proof Structure

**Conjunctive gate.** Critical readiness is a conjunction; if any required $valid(e(c))$ is false, or B nonempty, Q false, or A false, then G is false. Arithmetic averages cannot change Boolean failure.

**Evidence-binding argument.** A result on artifact a/config x does not entail behavior for changed artifact b/config y unless a justified equivalence relation covers the relevant change. Therefore rebuilds/config changes can invalidate review evidence.

**Conditional-scope proof.** A conditional go is valid only if enforced $D'\subset D$ excludes the blocker scenario and all critical claims hold within D'. A verbal intention or unenforced traffic limit does not narrow actual exposure.

**Rollback counterexample.** Code rolls back, but forward migration deleted data old code requires. Deployment version returns while service cannot operate. Therefore binary rollback cannot entail system recovery; data/schema/effects require compatibility or roll-forward/restore evidence.

## Alternatives and Trade-Offs

Central review teams provide cross-system experience/independence but can bottleneck and lose local context. Peer/domain-specialist review scales ownership but may vary. Use risk-based specialists, standardized claims/evidence and independent challenge.

Large checklists improve breadth but invite box-ticking/obsolescence. Claim-driven templates remain purposeful but demand judgment. Curate a small core plus domain/change-specific modules and evidence automation.

Hard gates protect invariants but can motivate evasion when slow/opaque. Advisory review is fast but weak under deadline pressure. Make critical gates transparent, automated where trustworthy, and provide fast escalation/exception authority.

Preproduction evidence is controlled/reproducible but cannot recreate production. Canary/progressive delivery adds reality but exposes users. Combine strong preproduction evidence with small reversible observable cohorts and defense-in-depth.

Rollback minimizes exposure for reversible changes; roll-forward handles irreversible state but may take longer. Design expand/contract and repair before launch rather than choosing during incident.

## Failure Modes and Misconceptions

- “Completed checklist means ready” confuses prompts with evidence.
- “All tests passed” omits test scope, artifact, assumptions and gaps.
- “Risk score is high” cannot compensate for a blocker.
- “Security approved” may cover design, not exact release/runtime.
- “Backward compatible schema” may break application behavior.
- “No known consumers” is not evidence for public APIs.
- “Canary is safe” without representative exposure/effect oracle is false.
- “Rollback exists” may ignore schema/data/external effects.
- “Autoscaling provides capacity” ignores lag and shared bottlenecks.
- “Dashboard and alert exist” does not prove correct query/delivery/action.
- “Backups succeeded” does not prove restore/RPO/RTO.
- “Conditional go” without enforcement is ordinary go.
- “Owner is the team” may leave no responder or authority.
- “Launch finished” ignores delayed failures and conditions.

## Worked Examples

### Example 1

Nine domains score 5/5; object authorization is untested. Average is 4.5, yet attacker can read another tenant. **Conclusion:** critical gates are conjunctive, not averaged.

### Example 2

Contract tests passed p12, but release rebuilt with a different serializer. Evidence binding fails; rerun exact artifact. **Conclusion:** green history is not transferable by assumption.

### Example 3

Capacity supports 2,000/s only with warm cache and all zones. Launch expects cold cache plus zone maintenance. Scope mismatch is blocker. **Conclusion:** capacity evidence includes state/fault assumptions.

### Example 4

Conditional go limits to internal read-only tenants, enforced by audience route/policy and 1% cohort; mutation endpoint stays dark. **Conclusion:** narrow scope must be technically enforced and observable.

### Example 5

Old mobile client treats new enum as fatal although Protobuf wire check passes. Consumer-version test blocks. **Conclusion:** application compatibility exceeds wire compatibility.

### Example 6

Canary shows normal HTTP success but two effects per idempotency key after response loss. Domain effect metric triggers abort. **Conclusion:** canary oracle must match critical outcome.

### Example 7

Binary rollback succeeds after column removal, but old binary queries missing column. Rehearsal reveals unrecoverable path. **Conclusion:** rollback includes schema/data.

### Example 8

Alert expression detects synthetic failure, but pager route points to departed owner. Delivery drill fails. **Conclusion:** signal existence is not operational readiness.

### Example 9

Backups are green; restore takes eight hours versus two-hour RTO and lacks current keys. PRR records blocker/limited scope. **Conclusion:** restore evidence defines recovery.

### Example 10

Launch passes immediate guard, but nightly reconciliation reveals event gaps. Guard period was specified through batch cadence and catches it. **Conclusion:** observation must cover delayed mechanisms.

## Cross-Program Connections

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) supplies system boundaries, quality attributes, architecture decisions, evolutionary fitness and trade-offs.

[Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies build/release provenance, SLO/error budgets, incident/on-call, progressive delivery, rollback and postmortems.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies threat/risk, identity/access, data/privacy, secure development, abuse, audit, vulnerability and response evidence.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies requirements/assumptions, interface/hazard analysis, verification/validation, configuration, lifecycle, readiness and emergent-risk reasoning.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, time, consistency, messaging, retries, partitions, recovery and impossibility boundaries.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies paved controls, policy/evidence automation, portals/catalogs, environments, telemetry and operational ownership.

[Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) supplies compute/network/storage, identity, regions, autoscaling, DR, cost and infrastructure change evidence.

## References

1. Google, [Site Reliability Engineering: Evolving the SRE Engagement Model—Production Readiness Reviews](https://sre.google/sre-book/evolving-sre-engagement-model/).
2. Google, [Site Reliability Engineering: Reliable Product Launches at Scale](https://sre.google/sre-book/reliable-product-launches/).
3. Google, [Site Reliability Engineering: Launch Coordination Checklist](https://sre.google/sre-book/launch-checklist/).
4. Google, [Creating a Production Launch Plan](https://sre.google/resources/practices-and-processes/production-launch-planning/).
5. NIST, [SP 800-218: Secure Software Development Framework 1.1](https://csrc.nist.gov/pubs/sp/800/218/final), February 2022.
6. OWASP, [Application Security Verification Standard 5.0.0](https://owasp.org/www-project-application-security-verification-standard/), May 2025.
7. OpenAPI Initiative, [OpenAPI Specification 3.2.0](https://spec.openapis.org/oas/v3.2.0.html), September 2025.
8. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), June 2022.

## Exercises

### Exercise 1

Transform “has auth, monitoring, load tests, backups, rollback and docs” into falsifiable critical claims and evidence records for a money-moving API.

### Exercise 2

A service has valid evidence for 14 of 15 critical claims, no known operational blockers, and an untested tenant object-authorization claim. A weighted score is 96%. Determine the decision and route to reconsideration.

### Exercise 3

Design a conditional-go scope and launch gates for a new event-backed order API whose normal path is ready but cross-region failover and bulk mutation are not.

### Exercise 4

Review an expand/contract database migration with old/new clients, async consumers, irreversible external effects and a 10% canary. Define rollback/roll-forward/recovery evidence.

### Exercise 5

During launch, HTTP success and latency pass, queue lag grows, duplicate-effect metric rises, telemetry drops 20%, on-call suggests continuing to gather data, and marketing deadline is near. Decide and describe follow-up.

## Answers to the Exercises

### Answer 1

Auth becomes separate claims: exact issuer/audience/key rotation/credential flow works; every money action enforces current user/tenant/action/object/property/state authorization including negative cross-tenant tests; gateway/mesh/direct paths cannot bypass; admin/support audited. Monitoring: logical/attempt/effect and stable error/latency/resource/dependency metrics, redacted logs, causal traces, telemetry-drop signal; synthetic known failure triggers correct dashboard/page/runbook/on-call. Load: exact artifact/config/mix/data/auth path sustains declared peak/fault headroom under correctness/SLO/stable queues, sheds safely and recovers. Backups: encrypted/isolated and timed restore produces semantically valid data/keys within RPO/RTO, including failback. Rollback: exact code/config/schema/route and external-effect reconciliation rehearsed mid-migration. Docs: exact version task/error/idempotency/limits/rotation/migration quickstarts execute through public boundary and owners/support/lifecycle are valid. Each record binds digest, environment, tool, result, date, limitations, owner and expiry.

### Answer 2

No-go for any scope where the untested authorization claim applies. Readiness conjunction is false regardless of 96%; “no known blocker” is weak because the critical evidence is missing. Identify affected operations/tenants/data and threat scenario. Reconsider after exact-artifact negative tests across gateway/direct/service for tenant/user/action/object/property/state, identifier enumeration, stale/revoked context and alternate methods/bulk/GraphQL/events as applicable; inspect policy/selectors and verify receiving-service enforcement/audit. A conditional go is possible only if a technically enforced narrower scope excludes protected-object access (for example synthetic internal read-only data), all claims hold there, and conditions/telemetry/abort/expiry are authorized. Security/data authority, not schedule owner, accepts any residual risk.

### Answer 3

Scope one region, bounded internal/partner cohort, ordinary single-order read/create/cancel only; disable bulk route and cross-region failover via gateway/policy/feature configuration, not documentation. Use region-local data/queue, no automatic remote route; publish degraded/unavailable behavior. Preconditions include normal-path contract/auth/idempotency/event/dedupe/consistency/capacity/security/telemetry/on-call and region-local restore. Canary by consumer/version from 1% through stages; gates cover correct effects, logical/attempt/event/duplicate, latency/error/lag/resources, auth denies and telemetry health. Abort on duplicate/lost effect, lag slope, SLO/security/telemetry thresholds; rehearse code/config/schema rollback and event replay/reconciliation. Conditions name owners, max traffic/tenants/time, guard period and expiry; separate work proves cross-region identity/residency/consistency/capacity/failback and bulk atomicity/resource/idempotency before expansion.

### Answer 4

Compatibility matrix covers old/new producer/service/client/async consumer against old/expanded/contracted schema. Expand first with nullable/additive structures/indexes and old semantics; deploy dual-read/write or backfill with checkpoints/idempotent restart and reconciliation. Do not enable new writes until all readers tolerate them; inventory/verify old consumers. External effects use durable idempotency/result/outbox/dedupe and outcome reconciliation. Canary must include old retrying consumers and high-risk mutation/effect, not only reads, with authoritative one-effect oracle. Rollback before contraction returns application/config while expanded schema remains compatible. After contraction/deletion, binary rollback may be impossible: require backup/restore or roll-forward repair, exact permissions/time/RPO/RTO and external-effect reconciliation. Rehearse failure at each step, mixed-version drain, event replay and backfill restart; define point of no return and explicit decision gate.

### Answer 5

Abort/hold immediately. Growing lag means nonsteady backlog; duplicate effects violate a critical safety invariant; 20% telemetry loss makes other “passing” observations unreliable. The authorized abort criteria should not be renegotiated for marketing or extra data. Stop new cohort/traffic, shed or route to known-good, disable unsafe retries/mutation if rehearsed, preserve nonnegotiable auth/consistency, roll back/forward according to data/effect safety, and reconcile idempotency keys/events/authoritative effects. Restore telemetry pipeline and quantify blind interval; notify incident/support/affected consumers as policy requires. Root-cause retry/dedupe/order/consumer capacity plus exporter overload, repair duplicate effects, rerun fault/load/recovery and telemetry-drop tests on exact candidate. Record incident/deviation, invalidate decision evidence, update PRR/capacity/alerts/runbook and require new authorization; deadline is rescheduled rather than accepted as risk by an unauthorized party.
