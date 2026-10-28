---
module_id: PLAT-034
program: Platform Engineering
level: 1
module_number: 34
title: Deployment Capability
status: complete
last_verified: 2026-09-02
---

# Deployment Capability

## One-Page Review

### Governing question

How should a platform move one verified artifact and compatible configuration into an environment, expose it progressively, prove user outcomes, and recover safely without confusing resource reconciliation, rollout completion, traffic movement, release approval, or business correctness?

### Essential definitions

- A **deployment** is the controlled realization of a release candidate in a target environment.
- A **release candidate** is an immutable artifact digest plus compatible configuration, schema/data changes, evidence, and declared operational requirements.
- A **deployment capability** is a versioned platform product that validates, realizes, observes, promotes, pauses, aborts, rolls back, and records deployments.
- A **rollout** is the transition from one workload revision to another; it may replace replicas, shift traffic, or both.
- **promotion** advances a verified candidate or rollout state after policy/evidence evaluation; it does not rebuild the artifact.
- A **canary** exposes a new revision to a bounded population or traffic share while comparing outcomes.
- A **blue-green deployment** prepares a separate revision and switches traffic between active and preview stacks.
- An **analysis gate** evaluates scoped evidence and returns success, failure, error, or inconclusive according to declared policy.
- **rollback** restores a previously accepted application revision or traffic path; it does not automatically reverse data, messages, or external side effects.
- A **deployment record** is an immutable event linking requester, artifact/configuration digests, environment, strategy, evidence, transitions, outcome, and recovery actions.

### Central model, mechanism, or theorem

Represent a candidate as $C=(a,c,m,p,e)$: artifact digest $a$, configuration digest $c$, migration/change set $m$, rollout policy $p$, and supply-chain/release evidence $e$. In environment $E$, deployment controller $D_v$ realizes desired revision $r$ and observes infrastructure $I(t)$, traffic $T(t)$, application $A(t)$, and user/business outcomes $U(t)$. Promotion at gate $g$ is allowed only if identity, compatibility, policy, readiness, and bounded outcome predicates hold. Controller completion is necessary evidence, never sufficient evidence of release success.

### Critical invariants

- The deployed artifact is the verified immutable digest accepted by policy; environments do not rebuild it.
- Every deployment binds exact artifact, configuration, environment, capability/strategy, policy, and migration versions.
- One authoritative delivery controller owns each mutable desired-state field; emergency changes are reconciled back deliberately.
- Preflight checks establish target identity, capacity, policy, dependencies, compatibility, backups, and rollback/recovery feasibility before mutation.
- Readiness controls admission of new work; rollout availability and progress are interpreted with observed generation and application outcomes.
- Traffic weights express routing proportions, not guaranteed request counts or representative cohorts.
- Analysis signals are scoped to revision, population, time window, data freshness, baseline, and decision action; missing or inconclusive data never silently passes.
- Database/schema, messages, caches, clients, and external effects use expand-contract and compatibility windows; workload rollback alone is not recovery.
- Pause, abort, rollback, roll-forward, and manual intervention are distinct owned transitions with bounded authority.
- Completion records actual artifact/configuration, selected platform revisions, traffic history, evidence, exceptions, and user outcome after observation.

### Common failures

Deploying tags; rebuilding per environment; mixing artifact creation with release; letting CI hold permanent cluster-admin credentials; using one mutable manifest with hidden substitutions; considering “applied” or “pods ready” successful; setting canary weights without checking real routing; analyzing global metrics that dilute canary failures; using tiny samples or stale dashboards; treating missing telemetry as success; auto-rolling back an incompatible database migration; deploying servers before clients can understand responses; changing configuration and code without attribution; running overlapping controllers; deleting the stable revision too early; and making manual production edits without durable reconciliation.

### Compact example

A production deployment request references OCI digest $a_7$, configuration digest $c_4$, environment `payments-prod`, strategy revision `canary-3`, and a backward-compatible schema expansion. Admission verifies provenance/signature, environment policy, dependency health, quota, backup freshness, and old/new schema compatibility. The controller creates the candidate revision with zero public traffic, runs synthetic tests, then shifts 1%, 10%, 25%, and 50% through weighted routing. Each step evaluates candidate-versus-baseline error, latency, saturation, payment authorization outcomes, telemetry freshness, and minimum sample/exposure time. Failure sets candidate weight to zero while leaving the stable revision available; migration contraction waits until all old binaries and rollback windows expire. The final record binds every digest, weight, analysis result, decision, and observed runtime revision.

### Connections

This capability consumes verified artifacts from [PLAT-032](032-artifact-and-image-management.md), governed environments from [PLAT-033](033-environment-provisioning.md), and workload/lifecycle primitives from [PLAT-024](024-pods-workloads-and-controllers.md) and [PLAT-029](029-health-readiness-and-lifecycle.md). It coordinates later configuration, secrets, policy, observability, reliability, and incident-response capabilities.

## Governing Question

What durable deployment contract can move an accepted candidate through target realization, exposure, evidence, and recovery while making every authority boundary, compatibility assumption, automated decision, and user-visible outcome reviewable?

Deployment is a socio-technical control loop. A source/build system decides what artifact exists. An artifact policy decides whether it is acceptable. An environment provides bounded capability. A delivery controller changes desired state. Workload and traffic controllers realize it. Applications and dependencies produce outcomes. Humans and policies decide whether to proceed.

Collapsing these responsibilities into “the pipeline” makes failures opaque and credentials broad. A platform capability should expose one coherent experience while preserving the distinctions needed for security, diagnosis, and recovery.

## Why This Matters

Production changes fail in combinations. A valid image may be incompatible with environment policy. Ready pods may serve errors under real traffic. A healthy application may overwhelm a dependency. A safe server change may break an older client. A successful workload rollback may leave a destructive schema or duplicated payment.

Deployment capability turns those combinations into explicit contracts and controlled transitions. It standardizes artifact verification, target discovery, rollout strategies, evidence, records, and recovery while allowing application teams to supply domain-specific health and compatibility knowledge.

Speed comes from reducing batch size, handoffs, and uncertainty—not from deleting checks. Frequent digest-bound releases with fast feedback and reliable rollback are safer than rare, enormous change windows whose contents cannot be attributed.

Automation increases blast radius when its assumptions are wrong. Progressive exposure, bounded concurrency, canaries, and independent policy reduce correlated change, but only if evidence is representative and the stable path remains recoverable.

## Prerequisites and Retrieval

Retrieve immutable artifacts and attestations, environment identities, Kubernetes Deployments/ReplicaSets/StatefulSets/Jobs, probes and readiness, Services and Gateway API, DNS/TLS, traffic weighting, metrics/logs/traces, SLOs, statistical sampling, configuration and secrets, database migrations, backward/forward compatibility, idempotency, queues, transactions, GitOps/reconciliation, RBAC, audit, and incident response.

You should distinguish build from release from deployment; desired state from observed state; apply from reconcile from rollout; readiness from liveness from user success; controller revision from application version; traffic weight from traffic observed; rollback from roll-forward and data recovery; audit evidence from logs; and progressive delivery from merely slow delivery.

## Learning Objectives

After completing this module, you should be able to:

1. specify a deployment candidate and target as immutable, compatible inputs;
2. design a versioned deployment API, state machine, and authority model;
3. validate supply-chain, environment, capacity, dependency, data, and recovery preconditions;
4. choose rolling, recreate, blue-green, canary, shadow, or partition strategies from risk and workload semantics;
5. design traffic exposure and analysis gates with representative evidence;
6. coordinate configuration, secrets, schemas, messages, clients, and external effects;
7. distinguish pause, abort, rollback, roll-forward, and disaster recovery;
8. operate declarative/GitOps reconciliation without competing writers; and
9. measure deployment capability quality through user outcomes and recoverability.

## Core Exposition

### Define the release candidate

A deployable candidate is not “whatever is on main.” It contains an immutable artifact digest; configuration schema and version; secret references and credential expectations; database/message/API compatibility changes; resource/runtime requirements; supported target classes; rollout policy; verification evidence; and ownership.

Keep artifact bytes environment-independent when possible. Environment-specific configuration and secret references are separately versioned inputs. If target-specific binaries are unavoidable, treat each as a distinct artifact with its own digest and evidence.

The candidate declares compatibility ranges: minimum environment capability revision, database schema window, API consumer/producer versions, configuration schema, feature flags, and architecture. This lets preflight reject a release before mutation.

Give the candidate a durable release ID, but never let that friendly ID replace component digests. One release record may refer to several platform manifests, migrations, or configuration objects.

### Define the deployment API and state machine

Inputs are candidate ID/digests, target environment ID, strategy class/revision, requested window or urgency, change/risk metadata, and authorized exceptions. The platform resolves defaults and shows the effective contract before execution.

Model states such as requested, validating, awaiting approval, reconciling, pre-exposure, analyzing, progressing, paused, promoted, completed, degraded, aborting, rolled back, failed, and superseded. State transitions include actor/controller, reason, evidence, time, and retry semantics.

Separate desired deployment from individual execution attempt. A retry after timeout may observe that the original mutation succeeded. Use a stable deployment ID and idempotency token so retries resume rather than duplicate.

Status conditions expose observed generation, artifact/configuration digests, stable/candidate revisions, traffic state, analysis, blockers, and ownership. A single `success` boolean cannot support operations.

### Establish authority boundaries

The build service publishes artifacts but cannot deploy production. The deployment requester proposes a candidate/target. Policy and approval authorize. A hosted delivery controller receives short-lived environment-scoped identity. Workload/traffic controllers reconcile bounded resources. Application owners define domain analysis; the platform governs execution and minimum policy.

Avoid permanent cluster-admin credentials in CI. Prefer pull/reconcile models or hosted push controllers with workload identity, target-scoped RBAC, explicit audiences, and brief lifetimes. Repository write access should not automatically imply production authority.

Separate mutation permissions for workload, routing, migrations, secrets/configuration, and rollback. Progressive controllers often modify ReplicaSets, Services, or routes; their service accounts are security-critical.

Emergency access is time-bounded, strongly authenticated, recorded, and reconciled into the declared source or explicitly reverted. The normal controller is fenced before an emergency writer changes owned fields.

### Verify artifacts and target policy

Resolve a digest and retrieve its authenticated evidence. Verify subject digest, signer/builder identity, source, build type, admitted parameters/materials, required SBOM/scan/release decisions, and current revocation or quarantine policy. Existence of provenance is not verification.

Resolve the environment by immutable ID and verify tier, region, policy profile, capability revision, tenant, and deployment authority. Names such as `prod` are not sufficient when multiple accounts or clusters exist.

Bind the decision to policy version and evidence digests. A release previously accepted for staging may not satisfy production requirements. Re-check at deployment because vulnerability, signer, exception, or environment policy may have changed.

Record the selected multi-platform manifest at runtime as well as the requested index digest. Otherwise platform-specific incidents remain ambiguous.

### Run preflight before mutation

Preflight validates target connectivity and identity, namespace/account ownership, quotas and surge capacity, scheduler placement, artifact pull, configuration schema, secret references, dependency availability and quotas, route ownership, TLS/DNS, telemetry paths, maintenance freezes, policy, backups, and rollback/recovery material.

Simulate or server-side validate rendered resources where supported. Detect immutable-field replacement, selector overlap, name collision, missing APIs/CRDs, admission denials, and configuration/schema mismatch.

For progressive rollout, reserve capacity for stable and candidate revisions plus termination overlap. With desired replicas $n$, surge $s$, terminating overlap $q$, and non-rollout workload headroom $h$, a necessary capacity bound is $n+s+q+h$ replicas' resources; topology and specialized devices further constrain it.

Classify failures as candidate, target, policy, dependency, platform, provider, or approval. Correct rejection is not deployment-service downtime.

### Choose a strategy from failure semantics

**Rolling update** gradually replaces interchangeable replicas and limits unavailable/surge counts. It is efficient, but old and new revisions overlap and traffic may not be precisely controllable. Kubernetes progress deadlines report stalls; they do not automatically roll back.

**Recreate** terminates old before new. It accepts downtime and avoids overlapping incompatible singleton behavior, but abrupt rollback still requires rebuilding availability.

**Blue-green** prepares a full preview stack and changes routing after tests/approval. It offers rapid traffic reversal while both stacks remain viable, at extra capacity and with data/shared-dependency complexity.

**Canary** exposes a bounded share/cohort, evaluates evidence, and grows. It reduces blast radius only if routing, sample, duration, and dependencies make the canary representative.

**Partitioned/sharded rollout** progresses by tenant, region, zone, shard, node pool, or client cohort. It aligns with failure domains and supports holdouts but complicates version compatibility and fleet inventory.

**Shadowing** duplicates requests to a non-authoritative candidate without using its response. It reveals behavior/performance but must prevent side effects, protect data, and interpret duplicated load.

### Understand native rolling behavior

Kubernetes Deployment creates a new ReplicaSet for Pod-template changes and scales old/new sets according to `maxUnavailable` and `maxSurge`. Percentages round differently; small replica counts need explicit calculation. Terminating pods can temporarily increase resource consumption.

Readiness gates whether a pod receives new Service traffic, while `minReadySeconds` delays its availability classification. A meaningful progress deadline is longer than startup, readiness stabilization, scheduling, image pull, and expected transient delay.

Deployment completion means all desired replicas are updated and available and no old replicas run. It does not prove latency, correctness, dependency safety, or business success. An `Available=True` condition may coexist with progression or failures elsewhere.

Revision history covers Pod templates, not every ConfigMap, Secret, route, database, or external change. Retention enables workload rollback only while the relevant ReplicaSet and external inputs still exist.

### Control traffic deliberately

Replica weighting without a traffic router approximates exposure through pod counts; connection reuse, topology, session affinity, load-balancer behavior, and readiness can distort it. A traffic API such as Gateway HTTPRoute can express relative backend weights.

For weights $w_c$ and $w_s$, intended candidate share is $w_c/(w_c+w_s)$ when the implementation conforms and both backends are eligible. This is a routing proportion, not a guarantee for a finite interval or user cohort.

Start with synthetic/internal traffic, then small production exposure, then progressive steps. Route by random request share, stable user/tenant cohort, header, geography, or cell according to risk. Stable cohorts improve behavioral comparisons; random requests spread risk but can mix one user's session across versions.

Observe configured route, controller status/conditions, data-plane realization, and actual request attribution. A stored weight of 10 does not prove 10% of requests reached the candidate.

### Design analysis as a decision system

Every gate defines question, subject revision, population, baseline, metrics/events, query, window, delay, minimum samples/traffic, thresholds, treatment of missing/stale/partial data, success/failure/inconclusive outcomes, and action.

Use layered signals: infrastructure scheduling/restarts/OOM; application errors/latency/saturation; dependency health and quotas; business outcomes such as payments authorized; security/policy events; and qualitative checks for high-risk changes.

Compare candidate with a contemporaneous baseline when shared traffic/dependencies vary. Absolute SLO thresholds protect users; relative deltas catch regressions beneath broad budgets. Avoid selecting metrics after seeing results.

Low traffic cannot support arbitrary statistical confidence. Require minimum exposure time and sample count, or route a stable synthetic cohort. Inconclusive evidence should pause or require bounded manual judgment, not silently promote.

Protect the analysis path. Queries, templates, dashboards, plugins, identities, and telemetry pipelines are part of deployment authority. Record exact results and evaluation versions.

### Coordinate configuration and secrets

Bind effective configuration digest/schema and secret-reference version to the deployment. If live mutable configuration changes during analysis, attribution fails. Freeze relevant inputs or record every transition and restart/reload effect.

Use expand-contract configuration: release consumers that understand both old/new shapes, publish new configuration, observe, then retire the old path. Feature flags separate exposure from artifact rollout but introduce their own identity, targeting, audit, and rollback.

Secret rotation can require dual credentials, workload reload, dependent acceptance, revocation, and rollback. Rolling pods with a new reference is not proof that each process loaded it.

Avoid bundling unrelated code, configuration, policy, secret, and infrastructure changes into one deployment. When combined changes are required, declare ordering and recovery for each.

### Coordinate data and external effects

Prefer backward/forward compatible schema transitions: expand schema, deploy code that supports old/new, migrate/backfill idempotently, switch reads/writes, observe, then contract only after old binaries and rollback windows expire.

A destructive migration before workload rollout can make rollback impossible. A migration transaction does not cover application traffic, message consumers, caches, search indexes, or third-party side effects.

Message/event changes require producers and consumers to coexist. Use versioned schemas, tolerant readers, additive fields, idempotent handlers, replay strategy, and explicit poison/dead-letter behavior. Rollback may reintroduce a consumer that cannot parse new events.

For irreversible business effects, favor roll-forward, feature disablement, compensation, or traffic isolation. State clearly which recovery action is safe at each deployment step.

### Distinguish pause, abort, rollback, and roll-forward

**Pause** freezes automatic progression while preserving current exposure. It is useful for inconclusive evidence or human inspection but prolongs mixed-version state and must have timeout/ownership.

**Abort** stops the candidate and restores traffic according to strategy. Confirm data-plane realization; configured zero weight may not terminate established connections.

**Rollback** deploys a prior accepted artifact/configuration within the current environment and data state. Re-verify current policy and compatibility. Fast rollback windows may skip progressive steps only under explicit risk policy.

**Roll-forward** deploys a corrected new version. Prefer it when schema/data/external effects make an old binary unsafe or when a small fix is faster than restoration.

**Disaster recovery** restores lost environment/data capability and is broader than release rollback. Do not label backup restoration as an ordinary rollout transition.

### Use declarative reconciliation carefully

Store desired release state declaratively, version its history, and reconcile automatically. A pull controller reduces inbound credentials, but the repository, controller identity, artifact policy, and target RBAC still form a trust chain.

Separate source intent, rendered manifests, policy results, and observed cluster state. Generated output should be reproducible and reviewable. Do not commit sensitive rendered secrets.

Define sync waves/dependencies for namespaces/policy, configuration, migrations, workloads, routes, and cleanup. Health checks must reflect actual resource semantics. Automatic pruning can delete removed resources; protect data and shared ownership.

Prevent loops among GitOps, progressive rollout, autoscaling, operators, and manual tools. Specify field ownership and ignore only fields intentionally controlled elsewhere. Drift visibility remains even when another controller owns a field.

### Deploy across regions and cells

Limit concurrent failure domains. Progress through cell/region cohorts with explicit bake time and global stop policy. A candidate safe in one region may fail elsewhere due to architecture, data, configuration, quota, provider version, or traffic mix.

Preserve enough stable capacity outside the active cohort to serve or fail over. Progressive deployment and disaster failover can compete for the same reserve; coordinate them.

Data-plane routing, DNS, caches, and clients propagate at different speeds. Record actual regional revisions and traffic, not only central desired state.

Global rollback is a workflow across partially progressed regions, data changes, and dependencies. Sometimes holding mixed versions is safer than rapidly changing every region again.

### Produce an immutable deployment record

Record candidate and every component digest, target identity/revision, controller/strategy version, requester/approvers, policy and exceptions, preflight, resource diff, migration, stable/candidate revisions, traffic changes, analysis inputs/results, pause/abort actions, completion evidence, and selected runtime manifests.

Link source/build provenance and artifact evidence rather than copying mutable summaries. Redact secret values while retaining reference/version and rotation evidence.

Records support incident response, compliance, causal analysis, rollback selection, fleet queries, and capability improvement. Logs alone are incomplete and may expire or contain unstructured contradictions.

### Measure the deployment capability

Measure request-to-start, queue/approval, preflight, rollout and analysis duration, time to user-outcome confidence, frequency, batch size, failure by category, abort/rollback/roll-forward rate, recovery time, paused age, stale mixed revisions, change attribution, and deployment-induced SLO impact.

Do not optimize raw deployment frequency without reliability and outcomes. Do not punish teams for safe early aborts; catching a regression at 1% is a capability success relative to full exposure.

Capacity planning includes controller/API rate, artifact pulls, surge, routing objects, metrics query load, analysis plugins, and human approval load. Limit concurrency by shared dependency and failure domain, not only cluster.

The following synthetic inventory demonstrates deployment-control coverage.

<!-- bijux-verify: {"id":"deployment-control-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"deployments=9\ndigest_pinned=9\nprogressive=5\nautomated_analysis=4\nmanual_gate=3\nrollback_ready=8\ndatabase_change=3\nmulti_region=2\nverified=9\n","stderr":""}} -->
```python
deployments = [
    {"name":"api-prod",       "digest_pinned":True, "progressive":True,  "automated_analysis":True,  "manual_gate":True,  "rollback_ready":True,  "database_change":True,  "multi_region":True,  "verified":True},
    {"name":"worker-prod",    "digest_pinned":True, "progressive":True,  "automated_analysis":True,  "manual_gate":False, "rollback_ready":True,  "database_change":False, "multi_region":True,  "verified":True},
    {"name":"web-prod",       "digest_pinned":True, "progressive":True,  "automated_analysis":True,  "manual_gate":False, "rollback_ready":True,  "database_change":False, "multi_region":False, "verified":True},
    {"name":"billing-prod",   "digest_pinned":True, "progressive":True,  "automated_analysis":True,  "manual_gate":True,  "rollback_ready":True,  "database_change":True,  "multi_region":False, "verified":True},
    {"name":"search-prod",    "digest_pinned":True, "progressive":True,  "automated_analysis":False, "manual_gate":True,  "rollback_ready":True,  "database_change":False, "multi_region":False, "verified":True},
    {"name":"batch-stage",    "digest_pinned":True, "progressive":False, "automated_analysis":False, "manual_gate":False, "rollback_ready":True,  "database_change":True,  "multi_region":False, "verified":True},
    {"name":"docs",           "digest_pinned":True, "progressive":False, "automated_analysis":False, "manual_gate":False, "rollback_ready":True,  "database_change":False, "multi_region":False, "verified":True},
    {"name":"preview",        "digest_pinned":True, "progressive":False, "automated_analysis":False, "manual_gate":False, "rollback_ready":False, "database_change":False, "multi_region":False, "verified":True},
    {"name":"edge-dev",       "digest_pinned":True, "progressive":False, "automated_analysis":False, "manual_gate":False, "rollback_ready":True,  "database_change":False, "multi_region":False, "verified":True},
]

print(f"deployments={len(deployments)}")
for field in ("digest_pinned", "progressive", "automated_analysis", "manual_gate", "rollback_ready", "database_change", "multi_region", "verified"):
    print(f"{field}={sum(deployment[field] for deployment in deployments)}")
```

The counts identify policy coverage; they do not prove that any deployment, analysis, rollback, migration, or regional strategy is safe.

## Definitions and Notation

Let candidate $C=(a,c,m,p,e)$ contain artifact digest, configuration digest, migration/change set, rollout policy, and evidence. Let target $E$ identify an immutable environment record and capability revision.

Let $D_v(C,E)$ be deployment controller/strategy revision $v$. At time $t$, observe infrastructure/controller state $I(t)$, traffic realization $T(t)$, application/dependency state $A(t)$, and user/business outcomes $U(t)$.

For gate $g$, let $Q_g(C,E,t)$ be a conjunction of artifact authenticity/authorization, compatibility, policy, readiness, sample/freshness, and outcome predicates. Promotion requires $Q_g=\mathrm{true}$; false aborts according to policy, while unknown/inconclusive pauses or escalates.

For candidate and stable traffic weights $w_c,w_s\ge 0$ with positive sum, intended candidate share is $q_c=w_c/(w_c+w_s)$. Observed share $\hat q_c=x_c/(x_c+x_s)$ over a window can differ because of sampling, eligibility, sessions, topology, retries, and router behavior.

Let $r_s$ be the stable revision and $r_c$ candidate. Workload rollback changes desired revision toward $r_s$ but cannot imply restoration of database state $B(t)$ or external effect history $X(t)$.

## Mechanisms, Invariants, or Proof Structure

The deployment assurance chain is:

1. resolve immutable candidate, target, strategy, and owner identities;
2. verify artifact evidence and current consumer/environment policy;
3. validate compatibility, capacity, dependencies, data transitions, and recovery;
4. authorize a short-lived target-scoped controller identity;
5. realize candidate resources without premature public exposure;
6. verify resource conditions and pre-exposure conformance;
7. expose progressively by traffic or failure-domain cohort;
8. evaluate scoped, fresh, sufficiently sampled infrastructure/application/user evidence;
9. promote, pause, abort, roll back, or roll forward under explicit policy; and
10. verify steady state and write an immutable deployment record.

This chain does not prove correctness. Artifact attestations, environment inventory, workload controllers, routing, telemetry, statistics, dependencies, humans, schemas, and recovery assumptions can fail. Its purpose is to bound change, expose evidence, and preserve action paths.

The invariants are digest identity, exact input binding, single field ownership, preflight/recovery feasibility, interpreted readiness/progress, observed traffic, fail-safe analysis, compatibility windows, distinct recovery transitions, stable revision retention, and complete records.

## Alternatives and Trade-Offs

**Push versus pull delivery:** push gives immediate orchestration and simple cross-system workflows but needs target credentials/network access. Pull reduces inbound authority and continuously reconciles, but repository/controller compromise and field ownership remain risks.

**Rolling versus blue-green:** rolling uses less capacity and native controllers but mixes revisions gradually and offers coarse traffic control. Blue-green supports preview and rapid reversal but doubles capacity and shares data/dependencies.

**Random canary versus stable cohorts:** random traffic yields broad sampling but may split sessions and diffuse user impact. Tenant/user/cell cohorts improve attribution and containment but may be unrepresentative.

**Automated versus manual promotion:** automation is fast and consistent when signals are trustworthy. Manual review handles qualitative or inconclusive risk but adds delay and cognitive load. High-quality gates define when each owns the decision.

**Rollback versus roll-forward:** rollback is fast when old code remains compatible with current data/effects. Roll-forward is safer after irreversible transitions but depends on rapid diagnosis/build verification. Decide per rollout step.

**Feature flags versus artifact rollback:** flags decouple exposure and can disable behavior instantly, but add mutable control state, targeting, stale paths, and testing burden. They complement rather than replace deployment records.

**One global rollout versus cell progression:** global changes finish quickly but correlate risk. Cells contain impact and reveal environment-specific issues while extending mixed-version compatibility and operational time.

## Failure Modes and Misconceptions

- **“Apply succeeded, so deployment succeeded.”** apply only submitted desired resources.
- **“All pods ready means users are healthy.”** readiness governs new traffic and may omit domain outcomes.
- **“ProgressDeadlineExceeded rolls back Kubernetes automatically.”** native Deployment reports stalled progress; a higher-level controller must act.
- **“Ten percent weight means exactly ten percent of users.”** weights are relative routing intent affected by sessions, eligibility, topology, and sample size.
- **“No metric data means no regression.”** missing or stale data is unknown and should pause/fail according to policy.
- **“A global error rate can evaluate a small canary.”** stable traffic can hide candidate failures; attribute by revision/cohort.
- **“Rollback reverses the release.”** data, events, caches, clients, and external effects can persist.
- **“Blue-green requires no compatibility.”** both stacks commonly share databases, queues, identities, and clients.
- **“Git history is a deployment record.”** it does not prove effective digests, target, traffic, evidence, or runtime outcome.
- **“A pull controller needs no credentials.”** it has target reconciliation authority and needs constrained identity.
- **“Manual edits are harmless during an incident.”** they can fight reconciliation and must be fenced/recorded.
- **“Progressive delivery is a list of pauses.”** value comes from representative exposure and decision evidence.
- **“More gates always improve safety.”** redundant noisy gates delay feedback and cause bypass; each gate needs a decision purpose.
- **“Old ReplicaSets guarantee rollback.”** configuration, secrets, routes, data, evidence, and current policy may no longer be compatible.

## Worked Examples

### Example 1

A release request specifies `api:stable`. The tag moves between approval and pull. The platform resolves and verifies digest `sha256:a7`, records it in desired state, and rejects any runtime image ID outside the accepted index/manifest graph. Conclusion: deployment identity begins with immutable artifact resolution.

### Example 2

A three-replica Deployment uses 25% surge and 25% unavailable. Percentage rounding and terminating overlap make intuitive “one at a time” assumptions unsafe. The team calculates actual controller behavior, ensures spare capacity, and sets explicit values aligned with service capacity. Conclusion: rollout parameters must be derived for real replica counts and termination time.

### Example 3

A new revision's pods are ready, but payment authorization success falls while HTTP 200 rate remains stable. A business-outcome gate attributes the regression to candidate traffic and aborts at 5%. Conclusion: transport success cannot replace user/domain evidence.

### Example 4

HTTPRoute weights are 90 stable/10 candidate, yet 2% of requests hit candidate because long-lived connections and session affinity dominate. The controller observes actual revision-attributed requests and extends/changes the cohort before analysis. Conclusion: configured weights require data-plane verification.

### Example 5

Canary telemetry disappears. Treating an empty query as zero errors would promote blindly. The gate verifies freshness, expected series, minimum traffic and samples, returns inconclusive, pauses, and pages the telemetry owner. Conclusion: observability failure is a deployment decision state.

### Example 6

A migration drops a column before new code rolls out. Candidate failure triggers workload rollback, but old code requires the removed column. The durable design expands first, runs compatible binaries, contracts only after the rollback window. Conclusion: data compatibility determines rollback feasibility.

### Example 7

A blue-green preview passes synthetic tests. After traffic switch, shared database connection saturation harms both stacks. Post-promotion analysis switches traffic back, but operators must also reduce candidate connections. Conclusion: isolated compute does not isolate shared dependencies.

### Example 8

A GitOps controller restores 100% candidate weight while a progressive controller tries to hold 10%. Explicit ownership gives the rollout controller traffic fields and GitOps ignores only those fields while still detecting drift. Conclusion: declarative systems need field-level authority boundaries.

### Example 9

Region A passes, but Region B uses another architecture manifest and older dependency endpoint. Cell progression stops before Region B, preflight catches incompatibility, and global capacity remains stable. Conclusion: multi-region rollout is a sequence of distinct compatibility experiments.

### Example 10

A critical regression occurs after schema expansion and new events, but before contraction. Policy chooses fast workload rollback because old code tolerates the additive schema/events; traffic returns to stable, candidate remains for diagnosis, and records preserve exposure/effects. Conclusion: recovery choice is valid only relative to the current compatibility window.

## Cross-Program Connections

- **Distributed Systems:** reconciliation, partial failure, idempotency, eventual routing, and state machines define deployment execution.
- **Statistics:** sampling, baselines, confidence, multiple metrics, selection bias, and missing data shape analysis gates.
- **Database Systems:** expand-contract schemas, transactions, backfills, replication, and recovery determine rollback feasibility.
- **Computer Security:** artifact verification, short-lived identity, RBAC, policy, audit, and break-glass govern authority.
- **Networking:** weighted routing, DNS/TLS, sessions, propagation, topology, and long-lived connections determine exposure.
- **Software Engineering:** compatibility, feature flags, release decomposition, versioning, and change attribution reduce risk.
- **Reliability Engineering:** SLOs, error budgets, blast radius, canaries, rollback, and incident response connect change to outcomes.
- **Human-Computer Interaction:** status, explanations, approvals, overrides, and actionable failure categories determine safe operator decisions.

## References

1. Kubernetes, “Deployments,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
2. Kubernetes, “Managing Workloads,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/management/
3. Kubernetes, “Container Lifecycle Hooks,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/
4. Kubernetes, “Disruptions,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/pods/disruptions/
5. Kubernetes Gateway API, “HTTP Traffic Splitting,” official documentation, retrieved 2026-09-02. https://gateway-api.sigs.k8s.io/guides/user-guides/traffic-splitting/
6. Kubernetes Gateway API, “HTTPRoute,” official documentation, retrieved 2026-09-02. https://gateway-api.sigs.k8s.io/api-types/httproute/
7. Argo Rollouts, “Canary Deployment Strategy,” official documentation, retrieved 2026-09-02. https://argo-rollouts.readthedocs.io/en/stable/features/canary/
8. Argo Rollouts, “Blue-Green Deployment Strategy,” official documentation, retrieved 2026-09-02. https://argo-rollouts.readthedocs.io/en/stable/features/bluegreen/
9. Argo Rollouts, “Analysis and Progressive Delivery,” official documentation, retrieved 2026-09-02. https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
10. OpenGitOps, “GitOps Principles,” project specification, retrieved 2026-09-02. https://opengitops.dev/
11. Supply-chain Levels for Software Artifacts, “Verifying Artifacts,” SLSA v1.2 specification, retrieved 2026-09-02. https://slsa.dev/spec/v1.2/verifying-artifacts
12. Sigstore, “Kubernetes Policy Controller,” official documentation, retrieved 2026-09-02. https://docs.sigstore.dev/policy-controller/overview/

## Exercises

### Exercise 1

Define candidate, deployment, rollout, promotion, canary, blue-green, analysis gate, pause, abort, rollback, roll-forward, and deployment record. For each, state one boundary it does not guarantee.

### Exercise 2

Trace a digest-pinned production deployment from request through artifact/target verification, preflight, realization, traffic steps, analysis, promotion, steady-state verification, and record creation. Identify authority and evidence at every transition.

### Exercise 3

A platform deploys mutable tags, grants CI cluster-admin, calls apply success “released,” sends 10% canary traffic without attribution, treats missing metrics as pass, runs a destructive migration first, and deletes stable replicas immediately. Diagnose at least nine failures and correct them.

### Exercise 4

Design a progressive rollout for a low-traffic multi-tenant financial API with long-lived sessions, one shared database, two regions, mobile clients that update slowly, and a regulatory manual approval. Specify cohorts, compatibility, capacity, evidence, timing, gates, and recovery.

### Exercise 5

During a 25% canary, application metrics are healthy but a downstream queue grows, telemetry is delayed by eight minutes, a feature flag changes independently, and a schema backfill is 60% complete. Decide whether to promote, pause, abort, rollback, or roll forward; provide an evidence and recovery plan.

## Answers to the Exercises

### Answer 1

A candidate binds artifact/configuration/change/evidence but does not prove target compatibility. Deployment realizes a candidate but does not imply success. Rollout transitions revisions but may not control traffic. Promotion authorizes progression but does not rebuild or prove permanent safety. Canary bounds exposure but may be unrepresentative. Blue-green separates compute stacks but often shares data/dependencies. An analysis gate evaluates declared signals but cannot cover unknown failure modes. Pause freezes progression but leaves current exposure. Abort stops/reverses candidate exposure but not side effects. Rollback restores prior workload intent but not data/time. Roll-forward introduces a corrective version but needs verification. A deployment record preserves evidence but does not itself make the change correct.

### Answer 2

The requester identity proposes exact candidate and environment IDs. Artifact policy verifies digest, provenance/signature, source/builder/materials, scan/quarantine, and evidence versions. Environment policy verifies target identity, tier, capability, and authority. Preflight evidence covers rendered diff, APIs, quota/surge, placement, secrets/configuration, dependencies, routes, backups, and compatibility. A short-lived delivery identity creates candidate resources; workload status with observed generation and pre-exposure tests proves bounded readiness. A traffic controller identity changes explicit weights/cohorts. Each analysis binds stable/candidate revisions, actual attributed traffic, window, freshness, samples, baseline, metrics/business outcomes, thresholds, and decision. Promotion authority advances steps. Final verification observes desired/actual revision, zero old exposure where intended, runtime manifest, SLO/user outcomes, migrations, and cleanup. The immutable record links every actor, digest, policy, transition, exception, and result.

### Answer 3

Mutable tags break artifact identity; deploy a verified digest. Cluster-admin CI combines source and production authority; use hosted target-scoped short-lived identity. Apply only submits desired state; observe reconciliation, rollout, traffic, application, and user outcomes. A 10% configured weight needs actual revision attribution, representative cohort, minimum samples/time, and router status. Missing metrics are unknown; pause/fail with telemetry ownership. Destructive-first migration destroys rollback compatibility; expand, deploy compatible code, migrate, observe, then contract. Deleting stable replicas removes rapid recovery; retain them through bake/rollback policy. Further failures include no target/preflight/capacity check, no supply-chain verification, no dependency/business gates, no durable configuration/change binding, no distinct abort/rollback plan, and no immutable deployment record.

### Answer 4

Use digest/configuration binding and additive server/API/schema changes compatible with old mobile clients. Allocate stable and candidate capacity in each region plus failover reserve; protect the shared database with connection/concurrency limits. Begin synthetic and employee/approved tenant traffic, then stable tenant cohorts rather than per-request random routing because sessions are long-lived. Progress one region/cell first while the other remains stable, with minimum time long enough for financial workflows and low traffic; supplement with controlled synthetic transactions but do not treat them as customer evidence. Gates verify artifact/target policy, workload and route realization, per-revision errors/latency, authorization/business outcomes, database saturation, downstreams, actual sample count, security events, and telemetry freshness. Regulatory approval receives exact evidence before larger exposure. Abort routes cohort to stable; workload rollback is allowed only while schema/events remain additive. Slow clients keep compatibility until measured retirement. Global progression follows a regional bake and preserves failover capacity.

### Answer 5

Do not promote: the downstream queue is a negative system outcome, eight-minute telemetry delay makes the current window incomplete, independent flag mutation destroys attribution, and the incomplete backfill may change performance/semantics. Pause progression first if current 25% exposure is within safety limits; freeze or record/restore the flag, wait beyond telemetry delay, attribute queue production/consumption by revision/cohort, inspect dependency saturation and backfill interaction, and establish current schema compatibility. If queue age threatens SLO or data safety, abort candidate exposure immediately. Rollback is safe only if old code tolerates the expanded/current schema and new messages; otherwise disable the feature or roll forward with a verified concurrency/query fix. Do not contract schema. Record flag, backfill position, queue effects, delayed telemetry, traffic realization, and decision. Resume only after fresh windows meet candidate, downstream, business, and minimum-sample gates.
