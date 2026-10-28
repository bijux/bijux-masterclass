---
module_id: PLAT-085
program: Platform Engineering
level: 2
module_number: 85
title: Upgrade Orchestration
status: complete
last_verified: 2026-09-02
---

# Upgrade Orchestration

## One-Page Review

### Governing question

How should a platform discover, plan, authorize, execute, observe, pause, recover, and prove upgrades across interdependent control planes, clusters, add-ons, nodes, APIs, data, and workloads without treating version installation as evidence of compatibility or safety?

### Essential definitions

- An **upgrade** is a governed transition from a known source state to a supported target state, including code, configuration, schemas, APIs, data, policy, trust, and operational behavior.
- An **upgrade unit** is the smallest independently scheduled and evidenced target, such as a management plane, cluster control plane, node pool, add-on, operator, database, or workload cohort.
- A **compatibility relation** states whether two specific versions, schemas, protocols, or behaviors may coexist for a bounded interval and set of operations.
- A **preflight** is a non-mutating assessment of target eligibility, prerequisites, deprecated use, capacity, recovery readiness, and evidence freshness.
- A **wave** is a set of upgrade units allowed to change concurrently under a shared disruption and risk budget.
- A **ring** is an ordered exposure cohort selected to reveal representative failures before broader promotion.
- A **gate** is a versioned decision rule over fresh evidence that yields pass, fail, or inconclusive; it is not merely a dashboard someone may inspect.
- **soak** is a defined observation interval long enough to expose selected delayed, periodic, load-dependent, and recovery failures.
- **rollback** restores a prior runnable state without violating data or API compatibility; **roll-forward** reaches a corrected later state; **replacement** builds a known-good unit and evacuates the old one.
- A **point of no return** is a transition after which automated rollback is not proven safe, commonly because of irreversible data, schema, cryptographic, or external side effects.
- **upgrade debt** is supported work deferred toward a deadline, including skipped patches, approaching version skew, expiring APIs, add-on incompatibility, and stale recovery evidence.
- An **upgrade campaign** is a durable, resumable workflow that binds source/target revisions, dependency plan, approvals, evidence, state, and outcome across all waves.

### Central model, mechanism, or theorem

Represent an upgrade campaign as a directed acyclic execution graph after strongly connected compatibility groups are collapsed. For unit $u$, let $Pred(u)$ be its prerequisites, $Compat(u,s,t)$ its coexistence predicate, $Ready(u)$ its preflight result, $D(W)$ the disruption of wave $W$, $B$ the authorized disruption budget, and $Gate(W,t)$ the fresh post-change evidence at time $t$. A wave may start only if

$$
Start(W)=\bigwedge_{u\in W}\left(Ready(u)\land Compat(u,s_u,t_u)\land
\bigwedge_{p\in Pred(u)}Completed(p)\right)\land D(W)\leq B.
$$

Promotion requires explicit pass evidence after the required soak. Failure or inconclusive evidence stops new work; it does not infer success from elapsed time. Every mutation carries campaign and attempt identity so retries reconcile rather than duplicate effects.

### Critical invariants

- Source and target are immutable, resolvable revisions with support, provenance, compatibility, deprecation, and security evidence.
- Actual observed state and evidence freshness—not intended state or command acceptance—determine eligibility and completion.
- Every dependency edge has an upgrade direction, coexistence window, owner, test, and failure/recovery consequence.
- Preflight detects unsupported version skips, removed APIs, stale clients, incompatible add-ons, unavailable capacity, and untested recovery before mutation.
- Control-plane, worker, node, add-on, API, data, and workload transitions respect vendor/project version-skew and ordering contracts.
- A wave cannot exceed service, quorum, topology, capacity, tenant, or correlated-failure disruption budgets.
- Canaries are representative enough to reveal consequence; later rings do not begin until gates and soak pass with fresh, attributable evidence.
- Gate inputs distinguish new-version behavior, baseline behavior, platform health, user journeys, data correctness, security, and telemetry health.
- Every campaign is pause-safe and restart-safe; leases, idempotency keys, checkpoints, and observed generation prevent concurrent or duplicated mutation.
- Rollback is offered only where tested across current data and contracts; otherwise the workflow exposes roll-forward, failover, restore, or replacement.
- Emergency overrides are time-bounded, least-privileged, independently audited, and cannot silently redefine completion.
- Completion includes conformance, residual/deprecation scans, recovery evidence, inventory/support updates, and disposition of the superseded state.

### Common failures

Updating everything at once; choosing only easy canaries; upgrading production first because test differs; skipping intermediate minor versions; ignoring management-provider compatibility; trusting a green install job; treating PDB presence as disruption safety; draining quorum peers together; depleting spare capacity; leaving webhooks or CRDs incompatible; discovering removed APIs during rollout; overwriting incident repairs; measuring only CPU and 5xx; promoting through missing telemetry; using an untested rollback after schema migration; resuming a stale campaign against changed reality; letting two controllers mutate one unit; accepting mixed-version state forever; and declaring completion while old nodes, clients, objects, credentials, or images remain.

### Compact example

A fleet moves from Kubernetes minor $n$ to $n+1$. Inventory pins cluster, control-plane, node-image, add-on, CRD, webhook, client, and workload revisions. Preflight verifies supported sequential transition, provider support, deprecated API usage, backup/restore evidence, spare capacity, PDB semantics, webhook compatibility, and node-drain feasibility. The campaign upgrades its management capability before dependent clusters, then one disposable cluster, one representative production cell, and wider rings. Within a cluster it upgrades control plane, validates API/storage/admission, replaces worker pools by zone within aggregate disruption limits, then upgrades add-ons in dependency order. Gates compare user and control journeys with a concurrent baseline, require fresh telemetry, and soak across scheduled jobs. A failed storage check stops promotion; because downgrade is not proven after the storage migration, the workflow restores traffic to the old cell and rolls forward the canary instead of advertising rollback.

### Connections

Upgrade orchestration consumes fleet identity and lifecycle from PLAT-083, dependency semantics from PLAT-084, service objectives and capacity from PLAT-081–082, and API, policy, supply-chain, audit, and observability contracts from earlier modules. It supplies controlled change and evidence to backup/restore, shared-platform incident response, disaster recovery, cost, and scaling in PLAT-086–090.

## Governing Question

What evidence makes a multi-component upgrade safe to start, safe to continue, safe to resume, and complete—and which transitions require containment or roll-forward rather than rollback?

Upgrade orchestration is a coordination problem under partial knowledge. Components have ordering and skew constraints; clusters differ; observations lag; a controller may fail halfway; data may cross an irreversible boundary; and users experience coupled journeys rather than isolated package versions.

The platform must therefore manage a durable state transition, not run an imperative script. Installation is one mutation inside a larger proof obligation: the target is supported, dependencies can coexist, disruption is bounded, behavior remains acceptable, and a credible recovery path exists at each boundary.

## Why This Matters

Platforms accumulate control planes, providers, operating systems, node images, runtimes, network/storage plugins, operators, webhooks, CRDs, identity agents, telemetry collectors, databases, and workload APIs. Their support windows do not align. Security deadlines can force changes while normal availability and compliance obligations remain.

Upgrades reveal hidden dependencies. A webhook parses a newly added field incorrectly; an old client calls a removed API; a node image changes cgroup behavior; a storage driver supports the target cluster version but not the deployed kernel; or a management controller cannot reconcile a newer workload cluster. Package-level compatibility matrices miss runtime paths and organization-specific policy.

Automation increases both consistency and blast radius. A controller can safely resume thousands of bounded actions, but it can also reproduce one bad decision everywhere. Rings, independent evidence, global stop conditions, and partitioned authority are therefore part of the safety mechanism, not process overhead.

Deferral also has risk. When clusters remain at the edge of supported skew, the next control-plane change first requires catching up nodes. Deprecated APIs become urgent removals. Old images lose patches. Upgrade debt must be visible as deadlines and constrained choices rather than hidden in “stable” systems.

## Prerequisites and Retrieval

Retrieve declarative APIs, reconciliation, idempotency, optimistic concurrency, leases, finalizers and conditions; cluster/fleet identity and lifecycle; Kubernetes component version skew and upgrade order; Cluster API or provider lifecycle contracts; package, image and artifact provenance; API deprecation and conversion; CRDs and admission webhooks; node cordon, drain, eviction, graceful termination and disruption budgets; quorum and consensus maintenance; storage/data migrations and restore; progressive delivery and canary analysis; SLOs, error budgets, telemetry and audit; capacity/headroom; dependency graphs; incident command; change authorization; and cryptographic/key rotation.

Distinguish install from upgrade; support from tested compatibility; source/target intent from observed state; compatibility from semantic equivalence; readiness from health; PDB from complete disruption protection; component rollback from system rollback; reversible code from irreversible data; retry from duplicate execution; pause from cancellation; failed from inconclusive; canary from low-value test; soak from arbitrary waiting; wave from ring; and campaign completion from “all commands exited zero.”

## Learning Objectives

After completing this module, you should be able to:

1. model platform upgrades as durable dependency-aware state machines with immutable source and target revisions;
2. discover upgrade units, compatibility constraints, version-skew rules, irreversible transitions, and recovery choices;
3. design preflights for APIs, clients, webhooks, CRDs, data, capacity, disruption, backup, and evidence freshness;
4. construct topologically valid waves and representative rings under aggregate disruption and correlated-failure budgets;
5. orchestrate management planes, cluster control planes, nodes, add-ons, workloads, schemas, and trust material in a safe order;
6. define baseline-aware gates and soak intervals for user, control, data, security, recovery, and observability behavior;
7. build pause-, retry-, takeover-, and resume-safe controllers using leases, idempotency, checkpoints, and observed generation;
8. select rollback, roll-forward, failover, restore, or replacement according to proven reversibility;
9. govern exceptions, emergency acceleration, audit, support deadlines, and upgrade debt; and
10. verify campaign completion through conformance, residue scans, inventory, recovery, and evidence retention.

## Core Exposition

### Define the upgrade contract

Start with an upgrade request that names business/security reason, owner, affected services and tenants, source revisions, target revisions, deadline, support policy, expected behavior changes, disruption budget, evidence requirements, and recovery strategy. Avoid mutable tags such as `latest`.

The contract distinguishes desired outcome from execution method. “Every eligible production cluster runs profile digest $d$ with Kubernetes $n+1$, driver $x$, and policy bundle $p$” remains meaningful if a provider changes its mechanics.

Record exclusions and known unknowns. A disconnected cluster, unsupported acquired system, or workload awaiting vendor certification cannot disappear from scope. It becomes a governed exception with owner, consequence, compensating control, deadline, and next decision.

### Inventory actual source state

Read trustworthy observed state for every unit: cluster ID, management authority, current component/image/config/schema/API versions, provider, topology, workloads, add-ons, policies, data class, support dates, drift, exceptions, health, capacity, and evidence time.

Do not infer current state from Git, a release database, or the previous campaign. Compare desired, last applied, locally observed, provider observed, and externally probed values. A partially failed earlier upgrade may create a mixed state requiring a different path.

Freeze a campaign snapshot for planning, then revalidate affected facts before each mutation. The snapshot provides reproducibility; revalidation prevents execution against obsolete reality.

### Discover upgrade units and boundaries

Create units small enough to checkpoint and recover: management provider, cluster control plane, each failure-domain-aware node pool, network plugin, storage plugin, DNS, ingress, identity agent, policy engine, telemetry pipeline, operator/CRD bundle, database/schema, workload cohort, and external integration.

Keep coupled transitions visible. A CRD storage-version migration and its conversion webhook may form one compatibility group. A database writer and schema may require expand/migrate/contract stages rather than one atomic unit.

Give each unit a stable ID, owner, authority, source, target, lifecycle, dependencies, predicted disruption, recovery modes, and proof obligations. One vague “cluster upgrade” node conceals the sequence where most failures occur.

### Build a semantic dependency graph

Edges state more than “A depends on B.” Record whether B must upgrade before A, remain backward compatible while A changes, stay available during A’s mutation, or wait until A stops emitting an old format. Attach environment, operation, versions, evidence, owner, and validity.

Examples include management provider before managed target; API server before kubelet under supported skew; CRD/conversion path before new objects; readers before writers for incompatible data; telemetry backend before emitting new schema; trust verifier before issuer algorithm change; and workload capacity before draining nodes.

Collapse true compatibility cycles into a coordinated group or redesign with a bridge release. Do not arbitrarily topologically sort a cycle. A bridge that reads old/new and writes old, followed by migration and later contract, converts the cycle into safe stages.

### Resolve version paths and support windows

Use the exact project, distribution, provider, and add-on contract for the deployed versions. A Kubernetes minor upgrade proceeds sequentially; component skew constrains order and narrows when highly available API servers are mixed.

Resolve every intermediate target, patch, machine image, artifact digest, schema migration, and configuration default. An allowed direct package jump may still cross multiple behavioral or data migrations that require observation.

Compute the latest safe start date from release support, security deadline, campaign duration, blackout windows, and recovery margin. Upgrade debt is actionable when it names the constraint that will close and the work needed before it does.

### Qualify immutable artifacts

Verify signatures/provenance, vulnerability policy, bill of materials, reproducible identity, source registry, license, and environment promotion for images, charts, binaries, firmware, policy bundles, and migration tools.

Render effective configuration and compare default changes. Pin image digests and chart dependencies. Test installation and upgrade paths separately; a clean-install test cannot exercise persisted state, old fields, conversion, or residue.

Retain the exact source artifact until recovery is no longer needed and retention policy permits disposition. “Rollback image unavailable” is an orchestration defect.

### Run non-mutating preflight

Preflight checks manifest/API compatibility, removed and deprecated API use, stored resource versions, client discovery, admission webhook rules and parsing, CRD conversion, operator support, provider quotas, certificate lifetime, DNS/network, policy, image availability, backup freshness, restore evidence, capacity, PDB semantics, topology, and change conflicts.

Use server-side dry run, target-version test clusters, API warning/audit metrics, static scans, replayed objects, representative workload tests, and provider plans. No one source proves readiness.

Results are pass, fail, or inconclusive with evidence time and expiry. Missing telemetry, unknown inventory, or a timed-out probe is not a pass. High-risk failures block automatically; explicitly governed exceptions require compensating evidence.

### Prove recoverability before mutation

Identify recovery point and recovery time requirements for platform state and hosted services. Verify backups cover the actual source versions, encryption keys, external resources, and metadata necessary to restore.

Restore into an isolated target and run semantic checks. A snapshot that can be listed is not restore evidence. For quorum stores, database schemas, external APIs, or cryptographic transitions, document whether the old binary can consume post-change data.

Mark points of no return. Require additional approval and a proven roll-forward, failover, restore, or replacement path before crossing them. Disable generic rollback buttons when the prerequisite is false.

### Reserve capacity and disruption budgets

Capacity includes replacement nodes, control-plane quorum, IP addresses, load-balancer targets, volumes/attachments, registry bandwidth, API rate limits, scheduling headroom, and operators. Reserve it for the campaign rather than hoping normal autoscaling supplies it.

Express disruption at multiple layers: per workload/PDB, tenant, zone, cluster, cell, shared dependency, and fleet. Concurrent upgrades that are individually safe may violate an aggregate journey or regional budget.

Use the Eviction API for voluntary pod movement where applicable, but model exceptions. PDBs do not protect direct deletion, all controller-driven rolling changes, involuntary failures, external quorum, or insufficient replacement capacity. A PDB can also block forever when the workload is already unhealthy.

### Choose representative rings

Typical rings are disposable conformance, internal/noncritical, representative low-consequence production, one unit per major topology/provider/workload class, and increasingly broad cohorts. Ring identity is campaign-specific, not a permanent label of neglect.

Select canaries to cover the risk hypothesis: provider, zone, data/storage class, network path, tenant shape, load, add-on combination, stateful workload, policy, and scheduled behavior. An empty development cluster provides weak evidence for a busy regulated production cell.

Never place all canaries in one correlated failure domain. Preserve a concurrent unchanged baseline where possible so environmental incidents and telemetry changes are not attributed to the target incorrectly.

### Construct safe waves

Topologically order dependency groups, then pack eligible units into waves under disruption, capacity, correlated-failure, operator, and evidence constraints. Limit concurrency independently at fleet, region, cluster, node pool, and dependency levels.

Separate “may coexist” from “may mutate concurrently.” Two node pools can run mixed versions but draining both zones together may violate workload availability. Two clusters can upgrade independently but share a saturated registry or identity service.

Emit an explainable plan: why each unit is in its wave, which prerequisites passed, which budget it consumes, and which gate promotes it. Replanning creates a new plan revision and audit event; it does not silently reorder active work.

### Upgrade management capability first

For a lifecycle manager, verify that its API contract and provider versions support both current and target managed states. Upgrade a shadow or lower-consequence management environment first and exercise reconciliation, adoption, pause, deletion protection, and recovery.

Partition manager authority and rollout concurrency. A broken new controller must not mutate every cluster. Preserve local cluster safety if the manager becomes unavailable.

Management upgrade completion requires successful reconciliation of existing objects, not only healthy controller pods. Check queues, webhook conversion, leader election, credentials, API throttling, and status ownership.

### Orchestrate cluster control planes

Follow the distribution’s exact component order and skew policy. For Kubernetes, the API server transition precedes controllers/scheduler and then node components under supported prerequisites. Highly available API-server instances remain within permitted skew.

Before the control plane changes, verify etcd/platform-state recovery, admission webhook compatibility, removed APIs, aggregated APIs, controllers, clients, certificates, capacity, and quorum topology. During the change, preserve enough healthy members across failure domains.

Afterward, test API discovery, reads/writes, watch/relist, admission, authentication/authorization, scheduling, controller convergence, lease renewal, audit delivery, and stored-object round trips. A responding `/readyz` endpoint is necessary but insufficient.

### Replace or upgrade worker nodes safely

Prefer immutable node-pool replacement when provider and workload semantics permit it: create target nodes, validate bootstrap/network/storage/identity/telemetry, cordon and drain bounded old nodes, observe rescheduling, then delete only after evidence.

Respect zone, workload, quorum, local storage, volume attachment, topology spread, graceful termination, daemon readiness, and surge capacity. Check that PDB selectors and desired replica counts express intended availability.

For in-place operations, define reboot boundaries, kernel/runtime/kubelet order, rollback capability, and local data. Kubernetes minor kubelet changes require the supported drain process. Never rely on a node returning merely because package installation succeeded.

### Sequence add-ons, operators, and CRDs

Classify add-ons as prerequisites, coupled components, or followers of the control-plane/node transition. Network, DNS, proxy, storage, identity, policy, ingress, metrics, and fleet agents each have different compatibility windows.

For CRDs, review served/stored versions, conversion webhook availability, schema/defaulting changes, controller compatibility, finalizers, and downgrade behavior. Back up custom resources and test representative old objects against the target.

Upgrade controllers and CRDs according to their published contract; do not assume Helm hook order proves semantic readiness. Gate on reconciliation of existing resources, not pod availability alone.

### Coordinate application and data compatibility

Use expand/migrate/contract for incompatible API or schema evolution. First deploy readers/writers compatible with both shapes, then expand schema/API, migrate and verify data, switch writers, observe, and only later remove old behavior.

Track asynchronous messages, caches, scheduled jobs, offline clients, backup/restore tools, analytics, and external partners. A quiet endpoint may still receive seasonal or recovery traffic.

Separate traffic rollback from data rollback. Routing users to the old application does not undo messages emitted, records transformed, or external side effects. Define reconciliation for partial effects.

### Define multidimensional gates

Pre-change gates cover eligibility and recovery. During-change gates cover control-plane quorum, mutation errors, disruption, capacity, and observability. Post-change gates cover user journeys, API semantics, data correctness, workload health, security/policy, audit, performance, saturation, cost, and recovery.

Each gate names query/test version, target and baseline, threshold, sample minimum, observation window, freshness, missing-data policy, decision owner, and action. Use absolute safety thresholds plus comparative regression bounds where appropriate.

Telemetry pipeline health is itself a gate. If the new version stops emitting errors, a naive error-rate gate improves. Independent synthetic journeys, audit, control-state checks, and ingestion freshness reduce this blind spot.

### Set soak from failure latency

Choose soak to cover hazards, not a standard number of minutes. Include controller resync and certificate refresh, autoscaling, cache expiry, leader election, compaction, backup, scheduled/batch work, traffic peaks, tenant diversity, and provider maintenance where relevant.

Long-latency hazards may require holding a representative ring while unrelated safe work proceeds. State explicitly which risks remain unobserved when deadlines shorten soak.

Soak evidence must remain fresh and attributable. A campaign paused for two days does not inherit a previously passed five-minute gate without revalidation.

### Make the controller resumable

Persist campaign, plan revision, unit state, attempt, source/target observations, idempotency key, lease/fencing token, timestamps, evidence links, approvals, point-of-no-return state, and last error. Use explicit states such as Planned, Preflighting, Ready, Mutating, Verifying, Soaking, Promoted, Paused, Recovering, Failed, and Complete.

One authoritative controller holds a renewable lease per unit. Every external mutation is idempotent or reconciled from observed state. Status distinguishes command accepted, provider operating, component installed, converged, verified, and promoted.

After restart or takeover, reacquire fencing, read reality, compare campaign intent and observed generation, and choose resume, verify, compensate, or escalate. Never rerun the last shell command blindly.

### Stop globally and locally

Local stop isolates one unit when its failure is independent and budgets remain valid. Ring stop prevents further promotion when a target-related signal fails. Global stop halts all campaigns for shared dependency failure, telemetry blindness, widespread regression, or incident command.

Stopping means no new mutations, preserving ongoing operations at safe boundaries, keeping evidence, and maintaining recovery access. It does not necessarily kill a control-plane replacement halfway or strand a database migration.

Define who can pause, resume, abort, or cross a point of no return. Automation may pause on objective evidence; human approval must not override hard invariants without a separately designed emergency path.

### Choose recovery by reversibility

Rollback requires retained source artifacts/configuration, backward-compatible persisted state, old clients/protocols, valid credentials, tested automation, and sufficient time/capacity. Verify all before presenting it.

Roll-forward is often safer after data/storage/API transformation: correct the target and continue. Failover moves service to an unchanged cell. Restore reconstructs state to a recovery point and reconciles external effects. Replacement builds a clean supported unit and evacuates the failed one.

Record partial completion. Recovery may leave mixed versions, drained nodes, migrated data, or temporarily disabled controllers. The next plan starts from this observed state, not from the original source assumption.

### Govern emergency upgrades

Security or support emergencies may compress testing and soak, but do not erase constraints. Pre-authorize reduced-risk paths: qualified artifacts, standing representative canaries, reserved capacity, tested restore, fast gates, vendor contacts, and incident command.

An emergency override records actor, reason, exact waived gate, time bound, residual risk, compensating control, and review. It cannot convert unknown evidence to passed or make an irreversible downgrade valid.

After stabilization, complete delayed validation, remove temporary access/configuration, reconcile desired state, and update the upgrade contract from observed failure modes.

### Prove completion and learn

Completion requires every in-scope unit at the target or an approved unexpired exception; conformance and user journeys passing; no unsupported skew; deprecated/removed API and old-client scans resolved; old nodes/images/controllers/configuration disposed according to policy; inventory/support dates updated; and recovery evidence current.

Retain plan revisions, approvals, mutations, evidence, gate decisions, exceptions, incidents, and final disposition. Link evidence to campaign, unit, target digest, test version, time, and observer.

Review prediction quality: unexpected dependencies, gate false positives/negatives, actual disruption, duration, recovery, manual actions, and debt created. Feed durable findings into profiles, preflights, dependency mapping, capacity, and recovery—not only a retrospective document.

## Definitions and Notation

Let the campaign graph be $G=(U,E)$, where each unit $u\in U$ has immutable source revision $s_u$, target revision $t_u$, owner, authority, observed generation $g_u$, and state $q_u$. An edge $(p,u,k)$ records a typed prerequisite or compatibility relation $k$.

Let $R_0,\ldots,R_m$ be ordered exposure rings and $W_{r,0},\ldots,W_{r,n}$ be waves within ring $r$. Let $d_j(u)$ be predicted disruption consumption for budget dimension $j$, and $B_j$ the authorized limit. A wave is budget-feasible when

$$
\forall j:\quad \sum_{u\in W}d_j(u)+Existing_j\leq B_j.
$$

For gate $i$, $x_i(W)$ is its measurement, $b_i$ a concurrent or historical baseline where valid, $n_i$ sample count, $f_i$ evidence freshness, and $\tau_i$ its threshold contract. Define

$$
Pass_i(W)=Fresh(f_i)\land n_i\geq n_i^{min}\land
AbsoluteSafe(x_i)\land Regression(x_i,b_i)\leq\tau_i.
$$

An absent, stale, or malformed measurement yields inconclusive, not pass. Promotion after soak duration $T_r$ requires every hard gate to pass throughout its required evaluation window and no stop condition:

$$
Promote(R_r)=Elapsed(R_r)\geq T_r\land
\bigwedge_i Pass_i(R_r)\land \neg Stop(R_r).
$$

Let $Rev(u,q)$ mean a tested recovery from state $q$ to the prior system behavior exists for the exact current data/contracts. Rollback is valid only when $Rev$ is true; package availability alone is insufficient.

## Mechanisms, Invariants, or Proof Structure

### Upgrade campaign mechanism

1. **Register:** bind owner, reason, scope, source/target digests, deadline, budgets, evidence, and recovery policy.
2. **Observe:** capture actual state, drift, health, capacity, dependencies, versions, and freshness.
3. **Resolve:** select sequential targets, compatibility bridges, artifact digests, and support constraints.
4. **Preflight:** evaluate APIs, clients, data, add-ons, webhooks, capacity, disruption, recovery, security, and telemetry.
5. **Plan:** collapse compatibility groups, topologically order units, choose representative rings, and pack safe waves.
6. **Authorize:** approve plan revision, exceptions, point-of-no-return transitions, and emergency constraints.
7. **Execute:** acquire fenced leases and reconcile one idempotent transition at a time from observed state.
8. **Verify:** evaluate fresh multidimensional gates against explicit thresholds and baselines.
9. **Soak:** observe risk-aligned latency while continuously enforcing stop conditions.
10. **Promote or recover:** advance only on pass; otherwise pause, rollback, roll forward, fail over, restore, or replace according to proof.
11. **Close:** run conformance and residue scans, update inventory/support state, dispose of superseded assets, and retain evidence.
12. **Learn:** compare predicted and actual compatibility, disruption, duration, gates, dependencies, and recovery.

### Identity and state invariant

Every action and observation binds campaign ID, plan revision, unit ID, attempt, immutable source/target, observed generation, and fencing token. Therefore a retry or controller takeover cannot silently apply an old decision to a new state.

### Compatibility invariant

Each active mixed-version edge has an explicit supported coexistence relation for the operations actually used. “Both versions are supported” does not imply they interoperate or permit arbitrary upgrade order.

### Disruption invariant

Before and during every mutation, total disruption remains within workload, tenant, quorum, topology, cluster, cell, and shared-dependency limits. New unrelated failures consume the same budget and may stop the campaign.

### Evidence invariant

Promotion depends only on attributable, sufficiently sampled, fresh evidence with a defined missing-data policy. The component under test cannot be the sole observer of its own correctness.

### Recovery invariant

The controller exposes only recovery actions whose preconditions are true for current persisted state and external effects. Crossing a point of no return invalidates unsupported rollback branches explicitly.

### Completion invariant

A campaign is complete only when desired and observed targets agree, conformance and residue checks pass, exceptions are governed, recovery evidence and inventory are updated, and superseded assets are dispositioned.

### Proof sketch: local success cannot establish campaign safety

Suppose every unit’s installer exits successfully and every component becomes locally Ready. Construct two systems with identical local results. In the first, versions coexist compatibly and user behavior is preserved. In the second, a new writer emits a schema an old asynchronous consumer cannot read; that consumer is dormant during local checks. The installer and readiness observations are identical, but end-to-end safety differs. Therefore local success cannot prove campaign safety. Dependency compatibility, representative execution, time-bounded soak, and residue/recovery evidence provide stronger—but still scoped—assurance.

### Executable wave-planning audit

The following synthetic audit classifies eight candidate units. It topologically admits only units whose prerequisites are complete, preflight is fresh and passing, rollback or declared roll-forward recovery exists, and wave risk fits the remaining budget. It does not prove production safety or optimize a real fleet.

<!-- bijux-verify: {"id":"upgrade-wave-planning-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"admitted=3\nblocked_prerequisite=1\nblocked_preflight=1\nblocked_stale=1\nblocked_recovery=1\nblocked_budget=1\nrisk_used=6\n"}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Unit:
    name: str
    prerequisites_complete: bool
    preflight: str
    evidence_age_minutes: int
    recovery: str
    risk: int


units = [
    Unit("management-provider", True, "pass", 4, "rollback", 2),
    Unit("canary-control-plane", True, "pass", 7, "roll-forward", 3),
    Unit("canary-node-pool", True, "pass", 9, "replace", 1),
    Unit("dependent-control-plane", False, "pass", 3, "rollback", 1),
    Unit("storage-driver", True, "fail", 2, "rollback", 1),
    Unit("identity-agent", True, "pass", 61, "rollback", 1),
    Unit("schema-migration", True, "pass", 5, "none", 1),
    Unit("broad-worker-wave", True, "pass", 5, "replace", 5),
]

budget = 6
freshness_limit = 30
used = 0
counts = {
    "admitted": 0,
    "blocked_prerequisite": 0,
    "blocked_preflight": 0,
    "blocked_stale": 0,
    "blocked_recovery": 0,
    "blocked_budget": 0,
}

for unit in units:
    if not unit.prerequisites_complete:
        counts["blocked_prerequisite"] += 1
    elif unit.preflight != "pass":
        counts["blocked_preflight"] += 1
    elif unit.evidence_age_minutes > freshness_limit:
        counts["blocked_stale"] += 1
    elif unit.recovery not in {"rollback", "roll-forward", "restore", "replace"}:
        counts["blocked_recovery"] += 1
    elif used + unit.risk > budget:
        counts["blocked_budget"] += 1
    else:
        counts["admitted"] += 1
        used += unit.risk

for key, value in counts.items():
    print(f"{key}={value}")
print(f"risk_used={used}")
```

### Verification strategy

Unit-test graph resolution, state transitions, fencing, retries, budget arithmetic, expiry, and gate three-valued logic. Contract-test providers and management controllers across supported source/target pairs. Rehearse upgrades on restored production-shaped state with removed APIs disabled, representative objects, old/new clients, admission, add-ons, node drains, and data migrations. Fault-inject controller restarts, provider timeouts, telemetry loss, registry failure, stuck eviction, quorum loss, webhook failure, and partial external effects. Run shadow/dry plans and compare predicted with observed order and disruption. Game-day rollback, roll-forward, failover, restore, and replacement at pre- and post-irreversible boundaries. Audit campaign identity, authorization, immutable artifacts, evidence lineage, overrides, residue, and completion.

## Alternatives and Trade-Offs

- **In-place upgrade versus replacement:** in-place can reduce spare capacity and preserve local state; replacement offers immutable rollback and drift removal but needs capacity and careful data/network identity transfer.
- **Automated versus operator-driven:** automation gives consistency, checkpointing, and fleet scale; human control helps novel cases but is slow and inconsistent. Automate invariants and evidence while preserving bounded intervention.
- **Rolling versus blue-green platform:** rolling consumes less duplicate infrastructure; blue-green improves isolation and traffic restoration but complicates state, identity, and external integrations.
- **Large waves versus narrow waves:** large waves reduce campaign duration and mixed-version exposure; narrow waves reduce blast radius but increase operational time and exposure to drift.
- **Fixed cohorts versus risk-selected rings:** fixed cohorts are simple; risk-selected rings better cover topology and workload hypotheses but require current inventory.
- **Fast versus long soak:** fast promotion meets security/support deadlines; longer soak detects periodic and delayed failures. Tie time to hazard latency and state residual risk.
- **Metric gates versus synthetic journeys:** metrics provide breadth and trends; synthetics test semantics independently but cover fewer paths. Use both with control-state evidence.
- **Historical versus concurrent baseline:** historical baselines cover longer seasonality; concurrent baselines isolate current environmental effects but consume unchanged capacity and may share failure.
- **Fail closed versus fail open on missing evidence:** fail closed protects high-consequence change; fail open preserves deadline progress but may spread blind. Define per gate and allow only explicit bounded override.
- **Rollback versus roll-forward:** rollback may restore code quickly before irreversible change; roll-forward avoids incompatibility after data/schema transitions but requires prepared target repairs.
- **Provider-native versus platform-wide orchestration:** native tooling understands local mechanics; a platform orchestrator coordinates dependencies and global budgets. Wrap provider actions instead of reimplementing them.
- **Central versus cell-local controller:** central planning gives a fleet view; cell-local execution contains outage and credentials. Hierarchical intent with fenced local execution often balances them.
- **Strict conformance versus exception cohorts:** strictness reduces variants; temporary exceptions allow real vendor and business constraints. Every exception needs owner, expiry, evidence, and consequence.
- **Patch-first versus direct target:** reaching latest source patch may reduce known bugs; it adds a transition. Follow project/provider guidance and validate every actual path.
- **Drain versus direct termination:** eviction honors PDB and graceful behavior; direct termination may be required for compromised or permanently stuck nodes but raises availability/data risk.
- **One campaign versus component campaigns:** one graph sees dependencies; smaller campaigns simplify ownership. Link campaigns through explicit prerequisites and global disruption budgets.
- **Continuous upgrades versus maintenance windows:** continuous small change reduces debt; windows align people and business constraints but create batches. Preserve emergency and rollback capacity in either model.
- **Schema compatibility bridge versus coordinated cutover:** bridges reduce synchronized risk and allow soak; they add temporary complexity. Coordinated cutover is shorter but concentrates failure.

## Failure Modes and Misconceptions

- **“Supported versions are compatible.”** Support lists do not prove coexistence for the deployed operations, provider, add-ons, or data.
- **“The target is healthy because its pods are Ready.”** Readiness can miss reconciliation, semantic, data, audit, and user-journey failures.
- **“The release pipeline passed, so upgrade is safe.”** Clean installs and unit tests omit persisted state, skew, residue, and fleet variation.
- **“We can skip intermediate minors.”** Projects may require sequential transitions and intermediate migrations even when artifacts install.
- **“The manager can always upgrade its clusters.”** Its provider/API contract may not support the target until the manager itself changes.
- **“PDBs guarantee no downtime.”** They cover selected voluntary evictions, not every deletion, rollout, involuntary failure, or external quorum.
- **“One node at a time is safe.”** One per cluster may still drain all replicas of a shared regional service or one member in several quorums.
- **“Canary means the smallest cluster.”** A tiny idle cluster may exercise none of the risk carried by production.
- **“No errors means pass.”** The telemetry path may be broken or the affected job may be dormant.
- **“A fixed ten-minute soak is enough.”** Failure latency depends on caches, resync, certificates, backups, traffic peaks, and scheduled work.
- **“Rollback means reinstall the old binary.”** Post-change data, objects, keys, protocols, and external effects may be unreadable or irreversible.
- **“Traffic rollback restores the system.”** It does not reverse emitted messages, migrated data, or third-party actions.
- **“Retry the failed command.”** The command may already have partially succeeded; reconcile observed state with idempotency and fencing.
- **“Two controllers make progress faster.”** Concurrent authority can duplicate or conflict unless leases and fencing guarantee one writer.
- **“Pause freezes the world.”** Dependencies, credentials, support windows, load, and observed state continue changing.
- **“Stale preflight remains valid.”** Revalidate time-sensitive capacity, health, evidence, and conflicts before mutation.
- **“All green clusters may advance together.”** Common dependencies and correlated topologies create aggregate blast radius.
- **“A schema migration is an implementation detail.”** It may be the point of no return governing system recovery.
- **“Old API objects are the only deprecation risk.”** Clients, manifests, admission rules, controllers, scripts, backups, and dormant jobs may call removed versions.
- **“Helm success means the operator reconciles.”** Hook/order success does not prove existing resources converge under the new controller.
- **“Node replacement is stateless.”** Local volumes, attachments, identity, topology, warm caches, and egress allowlists can make it stateful.
- **“Emergency means bypass safety.”** It changes tolerated evidence and timing through explicit authority; invariants and recovery still matter.
- **“An exception removes the unit from scope.”** It remains visible with consequence, control, owner, and deadline.
- **“The campaign ends at target version.”** Conformance, residue, inventory, recovery evidence, old assets, and exceptions remain.
- **“Mixed versions are always bad.”** Supported skew is useful for bounded rollout; indefinite unowned skew is upgrade debt.
- **“Mixed versions are always safe.”** Coexistence is component- and operation-specific and may narrow other allowable versions.
- **“Only availability matters.”** Security, authorization, data correctness, audit, privacy, cost, and recoverability can regress while serving traffic.
- **“The upgraded system can self-certify.”** Independent probes and observers are necessary against silent telemetry or status defects.
- **“Blackout windows eliminate risk.”** They defer planned change while vulnerabilities, debt, and certificate/support deadlines continue.
- **“A successful previous fleet predicts this one.”** Different topology, state, traffic, add-ons, and drift require current evidence.

## Worked Examples

### Example 1

A Kubernetes fleet at minor $n$ plans $n+1$. The graph places a compatible management provider first, then cluster control planes, controller/scheduler components, node pools, and version-coupled add-ons. Preflight finds kubelets already at the oldest allowed skew, so delaying them would block the next control-plane campaign; the plan upgrades them in bounded zone waves and records the debt avoided.

### Example 2

An API-removal scan finds no stored objects at the deprecated version but audit metrics show an overnight backup verifier still calls it. The target-version test cluster disables the API and reproduces failure. The client is upgraded and a full backup/restore rehearsal passes before the platform campaign resumes.

### Example 3

A three-zone stateful workload has five replicas and a PDB permitting one unavailable pod. The naive plan drains one node per zone concurrently, placing three replicas at risk. The aggregate planner follows workload placement, admits only one relevant drain, verifies rescheduling and quorum, then advances.

### Example 4

A new CRD controller stores a transformed representation. The old controller cannot read it. The campaign marks first persisted conversion as a point of no return, verifies restore and roll-forward, holds the old control cell for traffic failover, and removes the misleading automated rollback branch.

### Example 5

An identity-agent canary shows lower error rate but synthetic token renewal fails. Telemetry inspection reveals the new agent stopped exporting failure counters. The evidence gate becomes inconclusive, triggers ring stop, and blocks promotion even though conventional dashboards are greener.

### Example 6

A controller crashes after requesting three replacement nodes but before recording success. On takeover, the fenced reconciler reads provider resources by idempotency key, adopts the existing requests, and continues verification. It does not create three more nodes.

### Example 7

A critical vulnerability shortens the soak from a weekly batch boundary to two hours. Incident authority records the waived periodic-job gate, shifts that job into an immediate synthetic rehearsal, reduces wave size, reserves rollback capacity, and schedules post-stabilization validation. Missing evidence remains documented, not relabeled pass.

### Example 8

The smallest development cluster passes, but it has no network policy, CSI volumes, or admission webhooks. The ring design adds one representative low-consequence production cell with those combinations. A webhook field-parsing error appears there and stops the campaign before broad exposure.

### Example 9

A fleet is halfway upgraded when the central orchestrator loses its database. Cell-local agents finish only their current safe mutation and stop. After restore, plan identity and fencing prevent stale commands; each agent reports observed target state, allowing the campaign to verify or resume per unit.

### Example 10

Final validation finds all clusters report the target, but an old node image remains in one autoscaling launch template and a vendor client still uses the deprecated endpoint. The campaign remains Closing until the template is pinned to the new digest, the client is governed as an expiring exception, residue scans pass, and inventory/support deadlines update.

## Cross-Program Connections

- **Systems Engineering:** hazard analysis, state machines, assurance cases, feedback delay, and common-cause failure structure campaign safety.
- **API and Service Engineering:** compatibility, versioning, deprecation, idempotency, asynchronous contracts, and progressive delivery define safe service transitions.
- **Distributed Systems:** consensus quorum, leases, fencing, partial failure, eventual observation, and split authority govern orchestration correctness.
- **Data Engineering:** expand/migrate/contract, lineage, replay, backfill, schema compatibility, and quality gates determine reversibility.
- **Security Engineering:** artifact provenance, vulnerability deadlines, trust/key rotation, least privilege, emergency access, and audit constrain upgrades.
- **Reliability Engineering:** SLOs, error budgets, canaries, baselines, stop conditions, incident response, and recovery provide operational evidence.
- **Software Testing and Quality:** contract, conformance, fault-injection, target-version, regression, and residue testing expose more than install success.
- **Operations Research:** precedence-constrained scheduling and multidimensional resource budgets explain wave construction and campaign duration.
- **Formal Methods:** invariants, temporal state transitions, three-valued evidence, and model checking can verify pause/retry/recovery behavior.
- **Governance and Compliance:** approvals, exceptions, evidence lineage, separation of duties, and retention make accelerated change accountable.

## References

1. Kubernetes. [Version Skew Policy](https://kubernetes.io/releases/version-skew-policy/). Retrieved 2026-09-02.
2. Kubernetes. [Deprecated API Migration Guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/). Retrieved 2026-09-02.
3. Kubernetes. [Kubernetes Deprecation Policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/). Retrieved 2026-09-02.
4. Kubernetes. [Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/). Retrieved 2026-09-02.
5. Kubernetes. [Specifying a Disruption Budget for Your Application](https://kubernetes.io/docs/tasks/run-application/configure-pdb/). Retrieved 2026-09-02.
6. Kubernetes. [Safely Drain a Node](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/). Retrieved 2026-09-02.
7. Kubernetes. [Operating etcd Clusters for Kubernetes](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/). Retrieved 2026-09-02.
8. Cluster API. [Upgrading Management and Workload Clusters](https://main.cluster-api.sigs.k8s.io/tasks/upgrading-clusters.html). Retrieved 2026-09-02.
9. Cluster API. [clusterctl Upgrade](https://main.cluster-api.sigs.k8s.io/clusterctl/commands/upgrade). Retrieved 2026-09-02.
10. Cluster API. [Version Support](https://main.cluster-api.sigs.k8s.io/reference/versions). Retrieved 2026-09-02.
11. Argo Rollouts. [Canary Deployment Strategy](https://argoproj.github.io/argo-rollouts/features/canary/). Retrieved 2026-09-02.
12. Argo Rollouts. [Analysis and Progressive Delivery](https://argoproj.github.io/argo-rollouts/features/analysis/). Retrieved 2026-09-02.
13. etcd. [Disaster Recovery](https://etcd.io/docs/v3.6/op-guide/recovery/). Retrieved 2026-09-02.
14. Google. [Site Reliability Engineering: Reliable Product Launches at Scale](https://sre.google/sre-book/reliable-product-launches/). Retrieved 2026-09-02.
15. Google. [Site Reliability Engineering: Managing Critical State](https://sre.google/sre-book/managing-critical-state/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Design an upgrade campaign model for a fleet containing a management cluster, three workload-cluster profiles, network/storage/identity add-ons, and stateful tenants. Include identity, states, dependency edges, rings, waves, gates, and completion evidence.

### Exercise 2

Construct a preflight for a Kubernetes minor upgrade that can detect removed APIs, incompatible webhooks/CRDs/controllers, unsupported skew, unsafe drains, insufficient capacity, and invalid recovery assumptions.

### Exercise 3

A database migration allows the new application to read/write both schemas, but the old application cannot read newly written rows. Define an expand/migrate/contract plan, points of no return, traffic recovery, and gate logic.

### Exercise 4

Design retry and takeover semantics for an orchestrator that may crash after any provider call, lose its database temporarily, or run during network partition. State the invariants that prevent duplicate and conflicting mutation.

### Exercise 5

Plan an emergency fleet upgrade for a remotely exploitable vulnerability with a 24-hour deadline. Explain what may be compressed, what cannot be waived, how residual risk is recorded, and how completion is proved.

## Answers to the Exercises

### Answer 1

Use stable IDs for campaign, plan revision, management unit, each cluster/control plane, each topology-aware node pool, add-on, tenant workload/data group, and every attempt. States progress from Planned through Preflighting, Ready, Mutating, Verifying, Soaking and Promoted, with Paused, Recovering, Failed and Complete branches.

Edges encode provider-before-target, control-plane-before-worker, network/storage compatibility, identity availability, workload capacity before drain, data reader/writer ordering, and recovery dependencies. Collapse only truly coordinated compatibility groups. Select disposable, internal, representative production, profile/topology, then broad rings; pack waves under cluster, zone, tenant, quorum, capacity, and shared-service budgets.

Gates cover manager reconciliation, API/admission, scheduling, node/bootstrap, network/storage, identity, workload journeys, data correctness, security/audit, telemetry health and restore. Completion requires targets observed, conformance and residue scans, governed exceptions, current restore evidence, updated inventory/support, and disposition of old nodes/images/controllers.

### Answer 2

Resolve exact source, sequential target, distribution/provider support, management-controller contract, machine images, and add-on matrices. Scan source/manifests/rendered configuration, audit and warning metrics, clients, scripts, scheduled jobs, backup tooling, stored resource versions, CRD served/stored versions, conversion webhooks and admission rules. Exercise representative objects in a target-version cluster with removed APIs disabled.

Inventory API-server, controller, kubelet and proxy versions and calculate allowed skew at every intermediate state. Simulate each node drain through the Eviction API; evaluate PDB selectors, desired/current health, topology, quorum, local storage, attachments, termination and replacement headroom. Check quotas, IPs, volumes, registry and API capacity.

Verify actual snapshots, keys and external metadata by isolated restore and semantic tests. Mark data/storage transitions that make old binaries incompatible. Emit pass/fail/inconclusive with evidence time and expiry; block unsupported skip, stale evidence, unhandled removal, unsafe disruption, missing capacity, or unproven recovery.

### Answer 3

First deploy a bridge release that reads old and new but continues writing old. Expand storage/schema additively, validate old behavior, then backfill with idempotent checkpoints and quality reconciliation. Switch a small target cohort to new writes while both readers remain; compare data and user journeys with baseline. Once any new-only row exists, old-application traffic rollback is invalid unless a reverse transform is proven.

On failure before new writes, route to the old release and revert additive code if desired. After the point of no return, route affected traffic to a healthy target cell, pause writers, repair/roll forward, or restore to a prior recovery point while reconciling external effects. Only after every reader, consumer, restore job and partner accepts the new form should the campaign contract old fields and dispose of bridge code.

Gates cover dual-read equivalence, write correctness, migration counts/checksums, lag, rejected messages, old/new client journeys, backup/restore, and telemetry freshness. The contract stage has a separate approval and long soak because it removes recovery compatibility.

### Answer 4

Persist campaign and plan revision, unit/attempt, immutable source/target, state, observed generation, idempotency key, lease/fencing token, provider operation ID, checkpoint and evidence. Only a current fenced lease holder may mutate. Provider create/update calls use stable idempotency keys or discoverable campaign labels; deletes require exact resolved identity and current preconditions.

After a timeout or crash, the controller observes provider and local state before choosing the next transition. It adopts an already-created resource, waits for an active operation, verifies a converged target, or starts a new attempt only when absence is authoritative. Database loss causes cell agents to finish only defined safe atomic boundaries and stop; recovered orchestration increments fencing before resuming.

The identity/state invariant prevents stale plan execution, single-writer fencing prevents split authority, idempotency prevents duplicate external effects, compatibility/disruption checks are revalidated, and the recovery invariant prevents blind rollback. Audit records every takeover and reconciled ambiguous result.

### Answer 5

Prepare qualified target digests, a current dependency/asset inventory, standing canaries, target-version tests, reserved surge capacity, provider contacts, and rehearsed recovery. Incident authority may shorten soak, run rings continuously, reduce normal notice, and accept documented coverage gaps. It should shrink waves, preserve representative diversity, increase independent synthetic/control checks, and use global stop conditions.

Do not waive artifact identity, authentication/authorization, supported version path, quorum, hard disruption limits, controller fencing, evidence freshness semantics, or recovery truth. An unknown result remains unknown. Crossing an irreversible migration still requires a viable roll-forward, failover, restore, or replacement path.

Each exception records actor, vulnerable scope, exact waived gate, deadline, consequence and compensating control such as isolation or feature disablement. Completion requires every asset remediated or time-bounded isolated, conformance and exploit-negative tests passing, old vulnerable images/templates removed, inventory updated, credentials and temporary access reconciled, restore evidence current, and deferred long-latency validation scheduled and owned.
