---
module_id: PLAT-083
program: Platform Engineering
level: 2
module_number: 83
title: Cluster and Fleet Management
status: complete
last_verified: 2026-09-02
---

# Cluster and Fleet Management

## One-Page Review

### Governing question

How should a platform create, identify, group, configure, upgrade, observe, quarantine, recover, and retire clusters as a fleet while limiting shared-manager blast radius, preventing configuration snowflakes, respecting workload and jurisdiction boundaries, and preserving local safety when central connectivity fails?

### Essential definitions

- A **cluster** is an independently addressable scheduling and control domain with its own identity, lifecycle, state, trust, failure, and workload boundary.
- A **fleet** is a governed set of clusters sharing declared contracts, lifecycle processes, inventory, policy, and operational objectives; geographic proximity or one dashboard alone does not make a fleet.
- A **cell** is a bounded, repeatable deployment unit that contains failures and scaling, often including one or more clusters plus regional dependencies.
- **cluster identity** is a stable, non-secret identifier distinct from mutable display name, endpoint, credentials, region, or current manager.
- A **cluster class/profile** is a versioned desired contract for topology, Kubernetes/distribution version, network, identity, policy, add-ons, observability, and lifecycle.
- A **cohort** is a group selected for a rollout or support purpose; a **ring** is an ordered cohort representing increasing exposure or consequence.
- **fleet drift** is a material difference between declared desired contract and trustworthy observed state.
- **conformance** is evidence that a cluster or provider satisfies a versioned behavioral and operational contract; matching configuration text is only one input.
- **placement** assigns workload or fleet work to eligible clusters under capability, policy, capacity, topology, resilience, cost, and data constraints.
- **quarantine** removes a cluster from new placement or sensitive fleet actions while preserving evidence and a controlled recovery path.
- A **management plane** stores fleet intent and coordinates lifecycle; a cluster’s local control plane must retain defined safety when the manager is slow, unreachable, or compromised.
- **retirement** is an irreversible governed workflow that drains workloads and dependencies, preserves or deletes data/evidence correctly, revokes trust/access, removes routes, and proves absence from active inventory.

### Central model, mechanism, or theorem

Let cluster $c$ have desired profile revision $p_c$, observed state $o_c$, health/evidence freshness $h_c$, eligibility constraints $E(c,w)$ for workload $w$, and active exceptions $X_c$. A fleet decision is safe only if

$$
Eligible(c,w)=Conform(o_c,p_c)\land Fresh(h_c)\land E(c,w)
\land Capacity(c,w)\land \neg Quarantined(c)\land Valid(X_c).
$$

Fleet changes proceed through bounded rings $R_0,\ldots,R_n$ with independent health gates, soak, stop, and rollback/replacement criteria. The management plane never treats “command sent” as convergence, “same profile digest” as observed conformance, or “temporarily unreachable” as healthy.

### Critical invariants

- Every cluster has a unique stable ID, owner, purpose, tenant/trust tier, environment, provider/region/zones, lifecycle state, support window, and authoritative manager.
- Desired profile and observed evidence are separate, versioned, freshness-bounded, and attributable; manager state cannot self-certify remote convergence.
- Cluster creation, adoption, upgrade, quarantine, recovery, transfer, and retirement are explicit idempotent state machines with durable status.
- Fleet-wide identity, trust, policy, network, DNS, telemetry, artifact, backup, and API contracts have named owners and compatibility rules.
- Workload placement evaluates actual cluster capability, capacity, health, data/residency, failure correlation, and disruption—not labels supplied by an untrusted cluster alone.
- Rollouts start with representative low-consequence canaries, cap concurrent blast radius, soak across delayed failures, and stop automatically on user/control/evidence thresholds.
- A central manager outage cannot disable local authorization, workload execution, incident access, or safe recovery beyond the declared dependency contract.
- Shared hub credentials and controllers are least-privileged, partitioned, rate-limited, audited, and unable to mutate the entire fleet through one unconstrained identity.
- Drift classification distinguishes expected rollout, emergency repair, benign difference, unsupported state, compromise, and stale observation before remediation.
- Quarantine blocks new placement and high-risk changes while keeping observable, attributable, tested paths to investigate, drain, rebuild, or restore.
- Retirement proves workload/data/dependency disposition, route/DNS removal, credential/trust revocation, backup/evidence handling, billing stop, and inventory tombstone.
- Fleet objectives cover cohort health, rollout safety, inventory freshness, convergence, upgrade age, recovery, and management-plane blast radius—not just cluster count.

### Common failures

Cluster name reused as identity; spreadsheet as authoritative inventory; credentials stored in catalog; cluster self-labels trusted for regulated placement; one “standard” profile with undocumented patches; imperative bootstrap that cannot reproduce; central Git branch treated as observed state; all clusters updated together; canaries all in one easy region; no soak; rollback across incompatible data/API changes; hub admin credential across fleet; push manager needs inbound access everywhere; pull agent can apply arbitrary unsigned intent; disconnected cluster assumed healthy; automatic drift repair overwrites incident mitigation; quarantine deletes evidence; cluster deletion before workload/data discovery; DNS and trust left behind; support window exceeded silently; and fleet dashboard green because stale clusters stopped reporting.

### Compact example

A fleet assigns immutable cluster IDs and stores non-secret inventory plus observed signed status. Three profiles cover regulated production, general production, and ephemeral development; each composes pinned network, identity, policy, add-on, telemetry, and backup revisions. A release moves through disposable test, internal canary, one representative production cell, then progressively wider region/tenant rings. Gates combine platform journeys, API/control-plane health, workload disruption, policy/audit evidence, and observation freshness. An unreachable cluster becomes `Unknown`, stops receiving new placement, and retains local policy. A compromised cluster is quarantined, workloads fail over only where data semantics allow, and the cluster is rebuilt from verified profile. Retirement revokes credentials/routes/trust after draining and disposition evidence, while retaining a tombstone.

### Connections

Fleet management consumes cluster capacity/SLO evidence from PLAT-081–082 and every identity, isolation, policy, supply-chain, and audit contract from PLAT-071–080. It applies reconciliation and API design from PLAT-051–070 at cluster scale. It supplies the topology for dependency mapping, upgrade orchestration, overload, incidents, disaster recovery, cost, and scaling in PLAT-084–090.

## Governing Question

When should clusters be treated as interchangeable members of a governed fleet, and when must their distinct trust, topology, lifecycle, and failure properties remain visible?

Fleet management is not remote `kubectl` in a loop. It is lifecycle control over independent control planes, each of which can be unavailable, compromised, partially upgraded, drifted, overloaded, or running workloads whose disruption matters.

Good fleet architecture creates repeatable cells and shared contracts while containing management-plane failure. It automates the common case without erasing cluster identity, locality, evidence, or the human ability to stop and recover.

## Why This Matters

Multiple clusters arise from failure containment, scale, region/data residency, tenant isolation, provider boundaries, lifecycle cadence, acquisition, edge/disconnected operation, and experimental needs. Creating clusters without a fleet contract multiplies variants, credentials, policy gaps, and upgrade toil.

Centralization introduces common-mode risk. A bad fleet policy, compromised manager, expired shared certificate, broken DNS route, or unbounded controller can affect hundreds of clusters faster than humans respond. Automation must include staged exposure, partitioned authority, and autonomous stop conditions.

Cluster state is eventually observed. A manager may record desired version while an upgrade is stalled; an unreachable cluster may continue serving or may be compromised. Fleet decisions need freshness and independent evidence, not optimistic last-known labels.

Retirement is as important as creation. Orphan clusters retain public endpoints, credentials, trust, data, backups, cost, and attack surface. “Delete API returned success” is not proof of safe disposition.

## Prerequisites and Retrieval

Retrieve Kubernetes components, cluster lifecycle and version skew; declarative APIs, controllers, idempotency, finalizers and status conditions; Cluster API and provider contracts; multi-cluster inventory, identity and work APIs; cells and failure domains; identity federation, PKI, workload identity and credential plugins; tenancy/isolation; network, DNS and service discovery; policy/admission; GitOps/pull and push delivery; artifact evidence; observability/audit; SLOs, error budgets and capacity; workload placement/scheduling; progressive rollout; backup/restore; incident response; data classification/residency; cost allocation; deprecation; and secure deletion.

Distinguish cluster ID from name/endpoint; inventory from credential store; desired profile from observed state; conformance from configuration equality; creation from adoption; unreachable from unhealthy; unhealthy from compromised; quarantine from deletion; rollout cohort from permanent tier; workload placement from configuration distribution; central intent from local enforcement; push from pull trust; cluster failover from data failover; rollback from downgrade; replacement from repair; drain from eviction success; and deletion from retirement completion.

## Learning Objectives

After completing this module, you should be able to:

1. justify cluster/cell boundaries using failure, scale, trust, residency, lifecycle, and operating cost;
2. design stable cluster identity, authoritative inventory, ownership, lifecycle state, and freshness semantics;
3. define composable versioned profiles for infrastructure, Kubernetes, network, identity, policy, add-ons, telemetry, and recovery;
4. implement declarative create, adopt, upgrade, quarantine, rebuild, transfer, and retire workflows;
5. design hub/spoke, push/pull, hierarchical, and cell-local management with partitioned authority and offline safety;
6. evaluate placement from observed capability, capacity, health, policy, locality, and failure correlation;
7. roll out fleet changes through representative rings with health/evidence gates, soak, stop, and rollback/replacement;
8. detect, classify, reconcile, and audit drift without overwriting emergency repair or spreading compromise;
9. define fleet SLOs and test manager outage, credential compromise, partition, failed upgrade, and regional recovery; and
10. migrate snowflake or manually managed clusters into supported cohorts without unsafe forced convergence.

## Core Exposition

### Decide why a cluster boundary exists

Document each boundary’s durable purpose: independent failure cell, hard tenant/trust isolation, region/residency, provider/account ownership, scale ceiling, distinct lifecycle, edge connectivity, or disposable experimentation. “Different team requested one” is not sufficient by itself.

Clusters add control-plane cost, upgrades, add-ons, observability, networking, identity, policy, and incident surfaces. Too few clusters increase blast radius and heterogeneous scheduling; too many create fleet toil and fragmented capacity.

Model correlated dependencies outside clusters: shared identity issuer, registry, DNS, transit network, fleet manager, CI/CD, policy data, secrets, and provider region. Ten clusters are not ten failure domains if one shared service disables them.

Use repeatable cells. A cell defines cluster profile, regional dependencies, workload/data allocation, capacity, failure containment, and evacuation semantics. Horizontal growth adds cells rather than one ever-larger unique cluster where feasible.

### Establish stable cluster identity

Assign an immutable opaque fleet-scoped ID at creation/adoption. Keep human display name, DNS endpoint, provider resource ID, and ClusterSet membership as attributes. Names and endpoints change or may be reused.

Identity records include issuer/manager, creation event, ownership, and transfer/retirement history. Prevent simultaneous duplicate IDs. Never derive security authority solely from a self-reported label.

Authenticate cluster-to-manager and manager-to-cluster channels with short-lived workload/federated credentials or governed certificates. Bind credentials to exact cluster ID, manager, audience, operations, and expiry.

When ownership or manager changes, use a transfer state machine that verifies both authorities, rotates access, updates inventory, and prevents concurrent control.

### Build authoritative inventory

Inventory holds non-secret stable ID, display name, lifecycle state, owner/on-call, purpose, tenant/trust tier, provider/account/region/zones, network domain, profile desired/observed, Kubernetes/distribution versions, support deadline, capabilities, capacity summary, endpoints by access class, data classification, backup class, last observation, and active exceptions.

Separate authoritative desired fields from observed status and derived search fields. Record writer identity and freshness. A cluster manager should own its observation fields; humans should not edit health into existence.

ClusterProfile and About-style APIs illustrate standardized inventory and cluster properties. Treat alpha or evolving APIs according to their published maturity; wrap them behind your durable fleet contract.

Inventory exposes credential acquisition references or plugins, not bearer tokens or static kubeconfigs. Access is identity-bound, short-lived, authorized per cluster/role, and audited.

### Model lifecycle as explicit states

Use states such as Requested, Provisioning, Bootstrapping, Validating, Ready, Degraded, Quarantined, Upgrading, Draining, Retiring, Retired, and Failed. Define allowed transitions, actor, preconditions, deadlines, compensations, and terminal evidence.

Creation spans provider quota, network, machines/control plane, identity/trust, policy, add-ons, telemetry/audit, backup, conformance, inventory, and placement eligibility. Do not make Ready mean merely “API responds.”

Adoption is not relabeling. Discover actual configuration, trust, workloads, data, versions, add-ons, ownership, credentials, exposure, backup, and unsupported dependencies. Place into an exception cohort until conformance is proven.

Idempotency keys and durable status make retries safe. Finalizers protect external cleanup, but recovery must handle stuck finalizers without converting force deletion into routine practice.

### Define composable cluster profiles

Separate profile layers: infrastructure/region/zones; Kubernetes/distribution and machine images; network/CNI/DNS/ingress/egress; storage/CSI; identity/PKI; security/policy/admission; telemetry/audit; backup/recovery; fleet agent; and workload platform add-ons.

Pin every layer to immutable version/digest and compatibility contract. Record effective composition and ownership. “Latest” prevents historical reproduction and controlled rollout.

Limit variants through supported profiles and parameters. A parameter states allowed variability and tests; an undocumented patch creates a snowflake. Specialized profiles need user demand, accountable owner, lifecycle/funding, and retirement path.

Profile change is a fleet release. Validate schema, dependency compatibility, upgrade order, resource/capacity impact, security, rollback, and observability before rings.

### Choose management topology

A central hub simplifies inventory and policy but concentrates credentials, availability, and blast radius. Partition hubs by cell, environment, trust, region, or tenant; provide a higher-level catalog without one universal mutator.

Push management initiates from hub to cluster and needs reachable APIs and hub-held authority. Pull agents fetch authenticated desired state and suit restricted inbound networks, but agent compromise and intent verification remain risks.

For disconnected/edge clusters, define tolerated offline duration, cached policy/trust expiry, local administration, status buffering, artifact availability, conflict resolution, and safe behavior after stale intent. “Last known healthy” becomes Unknown after a deadline.

The local cluster retains authorization, admission, scheduling, and incident recovery according to its contract when the fleet manager fails. Central convenience must not be a synchronous dependency for every local action.

### Partition fleet authority

Use per-cell or per-cluster identities with least privilege. Separate lifecycle, configuration, workload placement, inventory observation, and break-glass roles. A catalog reader cannot mutate; a rollout controller cannot issue cluster-admin credentials universally.

Constrain work distribution to owned namespaces/resources and verify signed/pinned intent. A Work-style API must still authenticate manager, target cluster, workload, revision, and authorization.

Rate-limit and scope fan-out. A single policy change should not enqueue the entire fleet without concurrency, rings, cancellation, and per-cluster status.

Audit manager decisions and local enforcement. Independent cluster audit helps detect a compromised hub claiming success or issuing unauthorized work.

### Define fleet conformance

Conformance includes API behavior, identity, policy, network, storage, telemetry, backup/restore, capacity, lifecycle, and security—not only Kubernetes conformance or identical manifests.

Create a versioned test suite with static profile checks, API/functional probes, policy negative tests, workload identity, connectivity, DNS, storage lifecycle, telemetry/audit delivery, node/control-plane failure, backup restore, and manager-disconnection tests.

Run at creation, before/after upgrades, periodically, and after material drift. Store test version, cluster ID/profile, artifact/config digests, time, result, failures, and exceptions.

Kubernetes conformance is valuable for portable API behavior, but a conformant cluster can still violate organization-specific isolation, recovery, or observability requirements.

### Observe actual state and freshness

Use local agents/controllers, provider APIs, active probes, audit, and independent synthetic journeys. Each observation includes source, time, revision, and confidence.

Distinguish desired, last applied, locally observed, externally probed, and user-experienced states. A central Git commit proves intent only. A successful apply response may precede rollout or controller failure.

Define freshness per field: version/profile may tolerate minutes; security revocation or quarantine needs seconds; backup restore evidence may be periodic. Mark stale data Unknown and exclude the cluster from sensitive placement.

Monitor fleet inventory completeness, observation freshness, cohort/profile distribution, support age, upgrade state, drift, exceptions, conformance, capacity, SLO/error budget, and management control actions.

### Detect and classify drift

Compare normalized effective desired and observed state. Preserve unknown/unsupported fields and ownership. Avoid false drift from server defaulting, ordering, generated values, or version conversion.

Classify drift: expected during rollout; authorized emergency repair; benign provider default; unsupported/manual mutation; failed convergence; stale observation; or suspected compromise. Response differs.

Auto-remediate only changes known safe and owned by the fleet manager. Pause on emergency annotations, unclear ownership, repeated oscillation, destructive change, or security evidence. Record decision and notify owner.

After incident mitigation, reconcile the desired model deliberately: retain and codify the repair or revert with approval. Do not let the controller immediately undo the action required to recover it.

### Place workloads from trustworthy constraints

Placement inputs include workload owner, environment, tenant/trust, data class/residency, required capabilities/versions, capacity, latency/locality, failure-domain spread, dependency/data location, cost, disruption budget, cluster health/freshness, and active exceptions.

Separate eligibility from optimization. Hard policy first removes unsafe clusters; scoring then selects among eligible choices. Never let a favorable cost or capacity score override residency or trust.

Use authoritative inventory and locally attested/verified status. A compromised cluster must not self-label `regulated=true` and attract sensitive work.

Placement creates an auditable binding with workload revision, policy/profile, candidate set, exclusions, scores, decision, and time. Re-evaluate when cluster state changes, but move stateful workloads only under data-consistency and disruption contracts.

### Design rollout rings

Choose rings by consequence and representativeness: disposable integration; platform-owned non-production; internal canary; low-criticality production cell; representative provider/region/profile; then progressive remainder. Do not select only the easiest clusters.

Set maximum concurrent clusters, regions, tenants, nodes/workloads disrupted, and control-plane operations. Randomize within safe cohorts or deliberately cover topology.

Gates include cluster lifecycle/conformance, platform journey SLO/error budget, API/etcd/capacity, node/workload health, policy/admission, audit/telemetry freshness, incidents, user reports, and delayed workload behavior. Soak matches likely delayed failures.

Stop automatically on thresholds and manually on credible concern. Separate pause, rollback, roll-forward, repair, and replace. If state/API data migrated incompatibly, rollback may be unsafe.

### Manage versions and compatibility

Maintain a tested compatibility matrix across Kubernetes control plane/nodes/clients, distribution, OS/image, runtime, CNI/CSI, admission/conversion webhooks, CRDs/APIs, add-ons, agents, and workload requirements.

Kubernetes version-skew and API deprecation policies set upstream bounds, while distributions and lifecycle tools may impose tighter rules. Retrieve the policy for the exact target release; do not hard-code today’s release counts as an eternal fleet rule.

Inventory deprecated API usage, stored versions, webhook compatibility, and client versions before upgrade. Exercise round-trip data and backup restore.

Keep supported cohorts few enough to patch. Publish end-of-support and migration dates. A perpetually old cluster narrows future upgrade paths and accumulates security and compatibility risk.

### Handle unreachable and compromised clusters

Connectivity failure yields Unknown after freshness deadline. Stop new placement and nonessential rollout; preserve local operation; use independent provider/network/edge probes; and avoid deleting/recreating based only on missing heartbeat.

Quarantine suspected compromise: revoke/rotate fleet and workload credentials as scoped, remove from routing/placement, isolate network, preserve evidence, snapshot as authorized, and prevent the cluster from influencing hub state. Decide drain, rebuild, or retirement based on trust and data.

Do not blindly fail over stateful workloads. Verify replicated data consistency, fencing, single-writer semantics, DNS/traffic, credentials, and recovery objectives. Split brain can be worse than unavailability.

Test manager compromise as well as cluster compromise. Partition authority and maintain independent cutoff so one hub cannot continually re-enroll quarantined clusters.

### Recover and rebuild

Prefer reproducible replacement for ambiguous control-plane drift or compromise when workload/data recovery supports it. Repair may be appropriate for understood faults where preserving local state is required.

Recovery sources include immutable profile/artifacts, provider state, secrets/trust restoration, etcd or managed backup, workload desired state, persistent data backup/replication, inventory tombstone/history, and audit evidence. Define which is authoritative.

Rebuild under a new cluster instance ID when identity/trust continuity would be misleading. Preserve lineage from replaced cluster. Do not reuse credentials or silently transfer health history.

Qualify regional/cell recovery under fleet capacity from PLAT-082: mass create, agent reconnect, policy/add-on apply, workload placement, image pull, storage attach, DNS, and telemetry can overload shared services.

### Retire clusters completely

Freeze new placement and profile changes. Inventory workloads, data, volumes/snapshots, identities/secrets, load balancers/IPs/DNS/certificates, network peers/firewalls, registries, backups, audits, leases, external integrations, licenses and cost.

Migrate or dispose under owner and data policy. Drain with disruption and state semantics; verify traffic is zero and dependencies no longer point to the cluster. Preserve required evidence and backup retention.

Revoke cluster/fleet/workload credentials, trust bundles, bootstrap tokens, access plugins, routes and manager permissions. Delete infrastructure only after irreversible gates and separate approval where warranted.

Record a non-secret retired tombstone with stable ID, lineage, disposition evidence, time, actor, retained artifacts, and exceptions. Reconcile provider billing and external scans so hidden resources are discovered.

### Measure fleet outcomes

Track eligible-ready clusters by cohort; inventory and observation freshness; profile convergence time; drift age; support/version age; rollout success/stop/rollback and exposure; conformance; upgrade lead time; quarantine/recovery; retirement completion; fleet-manager SLO; and user journey outcomes by cell.

Measure correlated blast radius: number and consequence of clusters sharing manager, credential, policy release, identity, registry, DNS, network, provider region, and add-on version. Count alone is not impact.

Track fleet toil, exceptions, unsupported variants, manual actions, and cost per supported profile/cell. Optimization that consolidates a shared dependency may raise systemic risk.

Use results to adjust rings, partitions, profiles, support cohorts, capacity, and deprecation. Do not reward rollout speed without safety and convergence.

### Migrate a snowflake estate

Discover clusters independently from provider accounts, network/DNS, identity, billing, and existing tools; do not assume the spreadsheet is complete. Assign stable IDs and owners without immediately mutating.

Observe versions, configuration, workloads/data, access, trust, policies, add-ons, connectivity, backups, APIs, capacity, incidents and cost. Classify supported, adoptable with remediation, temporarily exceptional, rebuild/migrate, or retire.

Introduce inventory/freshness and short-lived access first. Define minimal profiles and conformance. Adopt low-risk clusters into canary cohorts, dual-observe existing managers, and progressively enable reconciliation.

Never force convergence over undocumented workload dependencies. Use expiring exceptions and explicit replacement/retirement plans. Finish by revoking legacy shared credentials and proving no unmanaged active clusters remain in authoritative discovery sources.

## Definitions and Notation

Let fleet $F$ contain clusters $c\in C$. For cluster $c$:

- $id_c$ is stable identity and $n_c$ mutable display name;
- $p_c$ is desired profile revision and $o_c(t)$ observed state;
- $\Delta(c)=diff(p_c,o_c)$ is classified drift;
- $f_c=t-now(observation_c)$ is observation age (nonnegative by convention);
- $H_c$ is health/conformance evidence;
- $K_c$ is capability set and $Q_c$ available capacity;
- $T_c$ is trust/data/residency classification;
- $X_c$ is bounded exceptions;
- $L_c$ is lifecycle state.

For workload $w$ with requirements $(K_w,Q_w,T_w)$, candidate eligibility is

$$
E(c,w)=Ready(L_c)\land K_w\subseteq K_c\land Q_c\succeq Q_w
\land Compatible(T_c,T_w)\land Fresh(f_c)\land Conform(H_c,p_c)\land Valid(X_c).
$$

Let rollout ring $R_i\subseteq C$, maximum concurrent exposure $b_i$, gate predicate $g_i$, and soak $s_i$. Advancement requires every completed action attributable, $|active_i|\le b_i$, $g_i=true$ throughout the relevant observation/soak rule, and no unresolved stop condition.

## Mechanisms, Invariants, or Proof Structure

### Fleet lifecycle mechanism

1. State durable reasons for cluster/cell boundaries and map shared failure dependencies.
2. Assign stable cluster identity, owner, purpose, trust/tenant tier, topology, and authoritative manager.
3. Maintain desired and observed inventory separately with attributable writers and field-specific freshness.
4. Define composable pinned profiles, compatibility matrices, supported variants, and conformance suites.
5. Reconcile explicit create, adopt, validate, ready, degrade, quarantine, upgrade, drain, retire, and failed states.
6. Partition management topology, identities, permissions, fan-out, rate limits, and local offline/recovery authority.
7. Observe cluster state independently enough to validate convergence, capacity, policy, audit, backup, and user journeys.
8. Classify drift before repair and preserve emergency/incident changes until desired intent is reconciled.
9. Place workloads only on eligible clusters using hard trust/data/capability/health constraints before optimization.
10. Roll out profile/version changes through representative bounded rings with gates, soak, stop, and recovery choices.
11. Quarantine/rebuild/restore and retire with trust, data, traffic, dependency, cost, and evidence closure.
12. Measure fleet outcomes/common-mode risk and requalify profiles, rings, partitions, and support windows continuously.

### Identity invariant

Cluster identity is stable and unambiguous across name, endpoint, manager, profile, repair, and lifecycle changes. Replacement creates explicit lineage rather than silently inheriting the old identity and health.

### Intent-observation invariant

Every fleet claim distinguishes desired, dispatched, applied, locally observed, externally verified, and user-experienced state with freshness. No central intent record self-certifies remote convergence.

### Blast-radius invariant

Every fleet action has bounded concurrent cluster/cell/region/tenant exposure, partitioned credentials, stop conditions, and a recovery path that does not require continuing the harmful action.

### Local-safety invariant

Loss or compromise of a fleet manager cannot silently disable declared local authorization, admission, workload execution, incident access, or evidence preservation across the fleet.

### Retirement invariant

A cluster becomes Retired only after workload/data disposition, traffic/dependency removal, trust/access revocation, infrastructure/billing reconciliation, and evidence/tombstone completion are verified.

### Proof sketch: equal desired digests cannot prove fleet conformance

Suppose clusters $A$ and $B$ reference the same desired profile digest $p$. In world $W_1$, both agents apply $p$ and all components converge. In world $W_2$, $B$ is partitioned before application, has an emergency manual change, or fails a controller step, while its central desired reference remains $p$. The manager’s desired records are identical in both worlds, but observed conformance differs.

Therefore equality of desired configuration—or a successful dispatch—cannot establish equal actual state. Conformance needs attributable, freshness-bounded observation and behavioral tests from the cluster and, for important properties, an independent boundary. Those observations can still be incomplete or compromised; evidence quality bounds the claim.

### Executable fleet eligibility audit

The synthetic audit classifies ten clusters by first fleet eligibility failure. It illustrates explicit unknown and quarantine handling, not a real fleet assessment.

<!-- bijux-verify: {"id":"fleet-eligibility-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"eligible=5\nnot_ready=1\nstale=1\ndrifted=1\nquarantined=1\nunsupported=1\n"}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Cluster:
    name: str
    ready: bool
    observation_age_minutes: int
    profile_matches: bool
    quarantined: bool
    capability: str


clusters = [
    Cluster("prod-a", True, 2, True, False, "standard"),
    Cluster("prod-b", True, 3, True, False, "standard"),
    Cluster("prod-c", True, 1, True, False, "standard"),
    Cluster("prod-d", True, 4, True, False, "standard"),
    Cluster("prod-e", True, 5, True, False, "standard"),
    Cluster("creating", False, 1, True, False, "standard"),
    Cluster("unreachable", True, 45, True, False, "standard"),
    Cluster("manual-patch", True, 2, False, False, "standard"),
    Cluster("incident", True, 1, True, True, "standard"),
    Cluster("legacy", True, 2, True, False, "legacy"),
]

counts = {
    "eligible": 0,
    "not_ready": 0,
    "stale": 0,
    "drifted": 0,
    "quarantined": 0,
    "unsupported": 0,
}

for cluster in clusters:
    if not cluster.ready:
        counts["not_ready"] += 1
    elif cluster.observation_age_minutes > 10:
        counts["stale"] += 1
    elif not cluster.profile_matches:
        counts["drifted"] += 1
    elif cluster.quarantined:
        counts["quarantined"] += 1
    elif cluster.capability != "standard":
        counts["unsupported"] += 1
    else:
        counts["eligible"] += 1

for name, count in counts.items():
    print(f"{name}={count}")
```

### Verification strategy

Validate identity uniqueness, transfer, credential scope, inventory writer/freshness, lifecycle transitions/idempotency, finalizers, profile composition, compatibility, and conformance evidence. Create duplicate-name, stale-status, unsupported-version, manual-drift, and compromised-agent cases.

Fault managers, agents, network partitions, identity/registry/DNS, provider regions, cluster APIs, admission, telemetry, and backups. Attempt unauthorized cross-cluster work and malicious self-label placement. Verify local safety, hub cutoff, quarantine, evidence, and controlled recovery.

Canary profile changes through representative rings, inject delayed failures, and prove gates stop exposure within bounds. Restore/rebuild a cell under fleet recovery load. Retire a test cluster and independently search provider, network, DNS, identity, billing, backup, and inventory sources for residue.

## Alternatives and Trade-Offs

1. **Few large clusters versus many cells:** consolidation improves utilization; cells bound blast radius and lifecycle at management cost.
2. **Central hub versus partitioned managers:** one hub simplifies policy; partitions reduce common-mode authority and outage.
3. **Push versus pull:** push offers immediate orchestration; pull works behind restricted networks but must verify intent and agent scope.
4. **Persistent versus ephemeral clusters:** persistence suits state and locality; replacement reduces drift but requires strong data/workload separation.
5. **Uniform profile versus supported variants:** uniformity reduces matrix size; variants satisfy real trust/provider/workload differences.
6. **Full automation versus approval gates:** automation scales routine changes; human judgment helps novel high-consequence transitions.
7. **Automatic drift repair versus alert-only:** repair restores known state quickly; alerts preserve emergency changes and ambiguous ownership.
8. **Central placement versus team selection:** central policy sees fleet constraints; team choice retains domain context but risks unsafe labels.
9. **Traffic-weighted canaries versus topology coverage:** traffic reflects user exposure; topology coverage catches provider/region/profile-specific defects.
10. **Rollback versus replace/roll-forward:** rollback is fast when compatible; replacement avoids hidden drift and unsafe downgrade.
11. **Shared fleet credential versus per-cell identity:** sharing is simpler; partitioned identities bound compromise.
12. **Online-only management versus disconnected operation:** online enables freshness; offline support needs cached trust, conflict and expiry semantics.
13. **Central add-on bundle versus layered ownership:** bundle eases rollout; layers isolate responsibility and version cadence.
14. **Live cluster adoption versus rebuild:** adoption preserves workloads; rebuild produces cleaner provenance but requires migration.
15. **Global service identity versus cluster-local identity:** global identity eases mobility; local scoping contains trust and naming collisions.
16. **Immediate quarantine versus investigation-first:** immediate isolation bounds threat; premature action can disrupt critical state and evidence.
17. **Delete versus retain retired tombstone:** deletion minimizes metadata; tombstones prevent ID reuse and preserve custody.
18. **Provider abstraction versus native features:** abstraction improves portability; native capabilities may better satisfy resilience, cost, or compliance.

## Failure Modes and Misconceptions

- **“A fleet is clusters in one UI.”** Governance, identity, lifecycle, contracts, and objectives make a fleet.
- **“Cluster name is identity.”** Names and endpoints are mutable and reusable.
- **“Inventory can store kubeconfigs.”** Catalog and credential authority need separate, short-lived access paths.
- **“Desired equals actual.”** Intent, dispatch, apply, convergence, and user outcome differ.
- **“Same manifests mean conformance.”** Defaults, versions, provider state, failures, and behavior can differ.
- **“Unreachable means down.”** It means observation is unknown; destructive assumptions can worsen incidents.
- **“Last known healthy remains healthy.”** Evidence expires by field-specific freshness.
- **“Self-reported labels are placement authority.”** Trust-sensitive claims need authoritative or verified sources.
- **“More clusters always improve resilience.”** Shared dependencies and managers can preserve common-mode failure.
- **“One manager is operationally simplest.”** It may centralize compromise and outage across every cluster.
- **“Pull mode is inherently secure.”** The agent and desired-state channel still carry mutation authority.
- **“Push mode needs cluster-admin.”** Least privilege and partitioned identities should match exact operations.
- **“Cluster API removes lifecycle design.”** Declarative machinery still requires contracts, providers, states, recovery, and evidence.
- **“One profile should fit everything.”** Durable trust, residency, provider and workload constraints may justify variants.
- **“Every difference is drift.”** Rollout, defaulting, emergencies, stale observation, and unsupported fields need classification.
- **“Auto-remediation is always safer.”** It can erase incident mitigation or oscillate with another owner.
- **“Canary means one dev cluster.”** It must represent relevant topology and behavior.
- **“Success in ring zero proves production.”** Exposure, traffic, data, provider and delayed failure differ.
- **“Roll back every failed upgrade.”** API/data migrations or skew may make downgrade unsafe.
- **“Version skew is just control plane versus nodes.”** Clients, webhooks, CRDs, add-ons, runtime and distribution restrictions matter.
- **“Kubernetes upstream support guarantees tool support.”** Providers and lifecycle tools may be stricter.
- **“Placement is a scheduler score.”** Hard trust, residency, health and capability eligibility comes first.
- **“Failover is workload rescheduling.”** Stateful data, fencing, identity, traffic, and dependencies must converge.
- **“Quarantine means delete immediately.”** Preserve evidence and controlled recovery while blocking exposure.
- **“A cluster can certify its own uncompromised state.”** Important claims need independent evidence and bounded trust.
- **“Central outage may block local recovery.”** That is a hazardous synchronous dependency unless explicitly justified.
- **“Delete cluster completes retirement.”** Routes, trust, data, backups, credentials, cost and dependencies remain.
- **“Reusing identity simplifies replacement.”** It corrupts lineage, audit and trust assumptions.
- **“Fleet health is percent Ready.”** Freshness, cohort harm, rollout, drift, capacity, user journeys and common-mode risk matter.
- **“Forced convergence fixes snowflakes.”** It can break undocumented critical dependencies; discovery and staged adoption come first.

## Worked Examples

### Example 1

Two clusters share the name `payments-prod` after a region migration. Audit and placement join records incorrectly. The fleet introduces immutable IDs, records provider IDs and lineage, keeps the old ID as Retired tombstone, and treats name as display metadata. New credentials and observations bind to the new ID.

### Example 2

A central Git repository shows all clusters on profile `p17`, but three agents are partitioned and one webhook rollout failed. Desired inventory stays `p17`; observed profile, conformance, freshness and user probes show distinct states. Sensitive placement excludes stale/failed clusters until verified convergence.

### Example 3

A shared fleet controller holds cluster-admin credentials for 400 clusters. The architecture partitions controllers and workload identities by production cell, separates inventory/read from lifecycle/configuration roles, limits work APIs to owned namespaces/resources, and keeps an independent revocation path. A compromise now has bounded reach.

### Example 4

A network add-on release succeeds in a small development cluster but fails only with large route tables. Rollout rings add representative scale/provider/region cells, capacity and connectivity gates, and a six-hour soak. Maximum concurrent production cells is two. The gate stops before widespread loss.

### Example 5

During an incident, an operator changes a DNS setting locally. The drift controller would revert it in seconds. An authenticated expiring emergency hold pauses that owned field, records reason/actor, and alerts. After recovery, the team either codifies the change in the profile or removes it; expiry cannot renew silently.

### Example 6

An edge cluster loses manager connectivity for two days. It continues local authorization, admission, scheduling, cached artifact use, and bounded operations. Central status becomes Unknown after ten minutes and new remote placement stops. Buffered audit/status reconcile by sequence after reconnect; expired trust/policy follows predefined safe behavior.

### Example 7

A suspected compromised cluster advertises spare capacity. Independent audit and attestation disagree. Placement quarantines it, traffic is removed, manager/cluster credentials rotate, and snapshots/evidence are preserved. Stateful failover waits for fencing and data consistency. The cluster is rebuilt with a new ID linked to the retired compromised instance.

### Example 8

An acquired estate has 70 snowflake clusters. Provider, billing, DNS and identity discovery finds eight absent from the spreadsheet. The platform assigns IDs/owners, observes without mutation, defines three target profiles, adopts conforming clusters, remediates supported differences, rebuilds high-risk unknowns, and retires unused clusters. Legacy credentials remain until each transition is verified, then are revoked.

### Example 9

A Kubernetes upgrade is within upstream skew but an older admission webhook cannot decode a new served version and a CSI driver lacks provider support. The fleet compatibility matrix and preflight tests block rollout. Owners upgrade webhook/driver, verify deprecated API use and restore, then restart rings. Upstream skew is a necessary, not sufficient, condition.

### Example 10

Retiring a cluster begins by freezing placement and discovering workloads, persistent volumes, public endpoints, DNS, certificates, network peers, identities, backups, audits and costs. Owners migrate data/workloads; traffic and dependency queries reach zero; credentials/trust/routes revoke; infrastructure deletes; billing scan clears; and a tombstone preserves ID and disposition evidence.

## Cross-Program Connections

1. **Distributed systems:** independent control planes, partial observation, partitions, reconciliation and common-mode dependencies define fleet behavior.
2. **Systems engineering:** cells, boundaries, interfaces, lifecycle states, emergent risk and assurance cases shape fleet governance.
3. **Security engineering:** partitioned identity, least privilege, quarantine, trust rotation, evidence and compromise response limit fleet blast radius.
4. **Networking:** region/cell topology, DNS, routing, service discovery, ingress/egress and partitions determine reachability and failover.
5. **Data engineering:** authoritative inventory, schemas, freshness, lineage, placement data and disposition require governed data products.
6. **Release engineering:** profiles, compatibility matrices, rings, canaries, soak, rollback and deprecation apply delivery practices to infrastructure.
7. **Site reliability engineering:** SLOs, capacity, failure domains, incident control, recovery and toil measure fleet operation.
8. **Database/storage engineering:** persistent volumes, replication, fencing, backup/restore and residency constrain cluster replacement/failover.
9. **Organizational design:** central, domain and product ownership plus escalation/support models determine sustainable federation.
10. **Economics and FinOps:** per-cell fixed cost, capacity fragmentation, provider choice, lifecycle and orphan detection balance resilience against spend.

## References

1. Kubernetes SIG Cluster Lifecycle. [The Cluster API Book](https://cluster-api.sigs.k8s.io/). Retrieved 2026-09-02.
2. Kubernetes SIG Cluster Lifecycle. [Cluster API Concepts](https://cluster-api.sigs.k8s.io/user/concepts). Retrieved 2026-09-02.
3. Kubernetes SIG Multicluster. [ClusterProfile API Overview](https://multicluster.sigs.k8s.io/concepts/cluster-profile-api/). Retrieved 2026-09-02.
4. Kubernetes SIG Multicluster. [About API Overview](https://multicluster.sigs.k8s.io/concepts/about-api/). Retrieved 2026-09-02.
5. Kubernetes SIG Multicluster. [Work API Overview](https://multicluster.sigs.k8s.io/concepts/work-api/). Retrieved 2026-09-02.
6. Kubernetes SIG Multicluster. [Multicluster Services API Overview](https://multicluster.sigs.k8s.io/concepts/multicluster-services-api/). Retrieved 2026-09-02.
7. Kubernetes. [Version Skew Policy](https://kubernetes.io/releases/version-skew-policy/). Retrieved 2026-09-02.
8. Kubernetes. [Deprecation Policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/). Retrieved 2026-09-02.
9. Kubernetes. [Kubernetes Conformance](https://www.cncf.io/training/certification/software-conformance/). Retrieved 2026-09-02.
10. Kubernetes. [Operating Clusters](https://kubernetes.io/docs/tasks/administer-cluster/). Retrieved 2026-09-02.
11. Kubernetes. [Multi-Tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/). Retrieved 2026-09-02.
12. Argo CD. [ApplicationSet Cluster Generator](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Cluster/). Retrieved 2026-09-02.
13. Flux. [Manage Kubernetes Clusters with Cluster API and Flux](https://fluxcd.io/flux/use-cases/cluster-api/). Retrieved 2026-09-02.
14. Cloud Native Computing Foundation TAG App Delivery. [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Design cluster identities, inventory, profiles, and lifecycle states for a fleet spanning three providers, regulated and general workloads, and intermittently connected edge sites.

### Exercise 2

Design management-plane topology and authority partitions for 600 clusters so one hub compromise or outage cannot mutate or disable the whole fleet.

### Exercise 3

Create rollout rings and gates for Kubernetes, network, admission, and fleet-agent upgrades across heterogeneous production cells.

### Exercise 4

Plan response to a cluster that is unreachable, self-reports stale healthy status, and may have leaked its fleet credential while hosting stateful workloads.

### Exercise 5

Define a complete retirement and verification workflow for 40 legacy clusters with unknown workloads, public endpoints, backups, and billing ownership.

## Answers to the Exercises

### Answer 1

Assign opaque stable fleet IDs independent of display/provider names. Inventory owner/on-call, purpose, tenant/trust, provider/account/region/zones, edge connectivity class, lifecycle, desired/observed profile, version/support, capacity/capability, data/residency, backup, access provider, exceptions and observation freshness. Store no credentials.

Compose profiles from provider infrastructure, Kubernetes/distribution, network/storage, identity/trust, policy/admission, telemetry/audit, backup, and fleet agent. Create regulated-provider variants only where durable controls differ; general profiles share contracts; edge profile defines cached trust/artifacts, offline duration, local authority, buffering and conflict behavior.

Use Requested→Provisioning→Bootstrapping→Validating→Ready plus Degraded/Unknown, Quarantined, Upgrading, Draining, Retiring, Retired and Failed. Adoption observes before mutation. Conformance tests identity, isolation, network, storage, policy, telemetry, backup/restore, manager loss and support compatibility. Placement uses authoritative constraints and excludes stale/unknown clusters.

### Answer 2

Partition managers by environment/trust and regional cell, with a read-oriented global catalog. Use per-cell/per-cluster workload identities and separate lifecycle, configuration/work distribution, inventory observation and emergency roles. No global cluster-admin key; credential acquisition is short-lived, audience-bound and audited.

Push or pull follows connectivity, but all desired intent is authenticated, pinned, scoped, rate-limited and attributable. Cap concurrent fan-out and require rollout rings/gates. Independent local audit and manager cutoff detect/stop malicious work. Clusters retain local auth/admission/scheduling and recovery when hubs fail.

Replicate desired/inventory state without replicating universal mutation authority. Test one hub outage, credential theft, malicious profile, network partition and revocation. Verify affected scope, local safety, quarantine, rehoming/restore, and no cross-partition escalation. Preserve offline break-glass paths governed outside the compromised hub.

### Answer 3

Build a compatibility matrix for control plane/nodes/clients, distribution, OS/runtime, CNI/CSI, CRDs/APIs, conversion/admission, add-ons, fleet agent and workloads. Preflight deprecated APIs, stored data round-trip, capacity, provider support, backup/restore and rollback/downgrade limits.

Use disposable integration, platform non-prod, internal canary, low-criticality production, then representative provider/region/profile/scale/data cohorts before remainder. Bound concurrent clusters, regions, nodes/workloads and tenants. Separate coupled changes when diagnosis/rollback requires it.

Gate on lifecycle/conformance, platform journey SLO/burn, API/etcd/capacity, node/workload disruption, networking/storage, policy/admission, audit/telemetry freshness, incidents and user reports. Soak for delayed routing/storage/controller issues. Automatic/manual stop supports pause, repair, roll-forward, rollback only when compatible, or replace. Record every cluster transition and exposure.

### Answer 4

Mark observations Unknown after freshness deadline, stop new placement and fleet rollout, and do not delete or fail over solely on heartbeat loss. Use independent provider, network, endpoint and audit evidence. Revoke or constrain the suspected fleet credential through an authority the cluster cannot override; isolate manager and workload routes proportionately.

Preserve forensic evidence and local logs; engage owner/security. Quarantine from placement/routing. For stateful workloads, establish fencing, replication consistency, backup integrity, single-writer and recovery objectives before failover. Split brain is a primary risk.

If compromise cannot be excluded, rebuild from verified profile/artifacts with a new cluster ID and lineage, rotate workload/manager trust, restore data under evidence, and verify conformance before placement. Retire the old identity only after data, traffic, credential, infrastructure and evidence closure.

### Answer 5

Discover independently from all provider accounts, billing, DNS/IP/load balancers, network peers, identity/PKI, backup stores, registries and existing tools. Assign stable IDs and owners; freeze new placement/deployment while preserving incident access. Observe before mutating and classify active, migrate/rebuild, or retire.

For each cluster inventory workloads/controllers, persistent volumes/snapshots/databases, data policy/holds, traffic, endpoints, DNS/certificates, identities/secrets, network rules, backups/audit, integrations, licenses and cost. Get owner approval for migration or governed disposition, drain with disruption/data semantics, and verify zero traffic/dependencies.

Revoke fleet, admin, workload, bootstrap and trust credentials; remove routes/DNS/network/provider resources; preserve required evidence/backups; reconcile invoices and external scans. Record deletion and failures. Keep a non-secret Retired tombstone with identity, lineage, actors/times and disposition references. Completion requires independent source searches find no unmanaged active residue.
