---
module_id: PLAT-088
program: Platform Engineering
level: 2
module_number: 88
title: Regional and Multi-Cluster Platforms
status: complete
last_verified: 2026-09-02
---

# Regional and Multi-Cluster Platforms

## One-Page Review

### Governing question

How should a platform divide control, workloads, traffic, data, trust, and operations across zones, clusters, cells, regions, and jurisdictions so that locality and resilience claims survive real correlated failures without introducing unsafe global coupling?

### Essential definitions

- A **zone** is a provider-defined failure and placement domain within a region; its independence is an assumption to validate, not a universal physical guarantee.
- A **region** is a geographic and administrative service domain with declared provider, network, control, data, and failure characteristics.
- A **cluster** is an independently addressable scheduling/control domain; multiple clusters in one region do not automatically create regional independence.
- A **cell** is a repeatable bounded service unit containing the regional platform and workload dependencies needed to limit failure and scaling.
- A **ClusterSet** is a group of clusters governed by a multi-cluster contract such as common identity, discovery, policy, or workload placement.
- **regional autonomy** is the ability to continue defined local outcomes when global or peer-region coordination is unavailable.
- **placement eligibility** applies hard capability, residency, trust, data, health, capacity, and recovery constraints before any cost/latency optimization.
- **traffic steering** maps a client or request to an eligible endpoint using health, locality, capacity, policy, session, and data-authority evidence.
- **home region** is the authoritative region for an entity, tenant, shard, or write domain under a named ownership policy.
- **active-active** means multiple regions simultaneously serve an outcome; it does not imply all regions accept conflicting writes to the same data.
- **failover** transfers defined service or authority from an impaired domain to a prepared target; **failback** reconciles divergent state and deliberately returns or redistributes authority.
- **regional evacuation** is a controlled movement or rejection of traffic, workload, data authority, and operational control under a tested capacity and consistency plan.

### Central model, mechanism, or theorem

For workload or request $w$ and region $r$ at time $t$, define hard eligibility

$$
Eligible(w,r,t)=Residency(w,r)\land Trust(w,r)\land Capability(w,r)
\land DataReady(w,r,t)\land DependencyReady(w,r,t)\land FreshHealth(r,t)
\land CapacityAfterFailover(w,r,t)\land RecoveryReady(w,r,t).
$$

Only then optimize latency, cost, carbon, or balance over the eligible set. During failure of region set $F$, safety requires both enough eligible capacity outside $F$ and a valid data-authority transition. Routing reachability alone cannot establish service recoverability.

### Critical invariants

- Every zone, cluster, cell, region, provider, account, jurisdiction, and shared dependency has stable identity, ownership, trust, lifecycle, capacity, and failure-correlation metadata.
- Regional service promises name exact outcomes, failure sets, RPO/RTO, degraded modes, tenant classes, and evidence—not generic “multi-region” status.
- Hard placement constraints for residency, trust, capability, data authority, recovery, and health cannot be overridden by latency or cost scores.
- A region retains defined identity verification, policy, discovery, workload execution, incident access, and observability during global-plane partition.
- Global control planes use partitioned authority, bounded fan-out, stale-intent limits, idempotency, and conflict rules; one manager cannot unconstrainedly corrupt every region.
- Service identity and discovery distinguish logical service, cluster, region, endpoint, version, health source, and data authority; name sameness never supplies authorization.
- Traffic moves only to endpoints with fresh independent health, sufficient headroom, ready dependencies, compatible state, and allowed locality; withdrawal and recovery are monotonic enough to prevent flapping.
- Data writes have a declared ownership/conflict model, replication semantics, lag visibility, durability boundary, and reconciliation path before active-active or failover is claimed.
- Capacity plans cover loss of declared correlated domains plus concurrent maintenance, recovery traffic, quotas, IPs, certificates, control APIs, and stateful resources.
- Deployment, policy, trust, artifacts, schemas, and observability remain compatible across the maximum supported regional skew and can be stopped or rolled back by cell.
- Failover and failback are fenced, idempotent, observable state machines with explicit authority transfer, DNS/session/queue/data handling, abort criteria, and audit.
- Exercises isolate real dependencies, use representative traffic/data/tenants, measure outcome-level loss and time, and reconcile every emergency change afterward.

### Common failures

Calling three clusters “multi-region” when they share one region; treating availability zones as perfectly independent; central identity, DNS, registry, Git, KMS, telemetry, or fleet manager as an unexamined cut set; routing before data and dependencies; sending all writes to all regions without conflict semantics; assuming asynchronous replicas meet zero RPO; discovering cold quotas during failover; scaling standby only after the failed control plane is needed; health checks that test a load balancer rather than user outcome; DNS TTL treated as convergence bound; long-lived connections ignored; ClusterSet name sameness mistaken for tenant identity; placement labels trusted from clusters; global policy rollout to every cell; failing over into incompatible versions; leaving failback undefined; and game days that disable only an application pod rather than the regional dependency boundary.

### Compact example

A platform serves tenants from three regional cells, each with local identity verification, policy cache, service discovery, deployment agent, telemetry buffer, and independent incident access. Tenants have a home region; stateless reads may use two eligible regions, while writes use a fenced single-writer lease and asynchronously replicate with visible lag. A placement engine filters residency, trust, profile, dependency, data, capacity, health freshness, and restore evidence before scoring proximity. Global traffic uses regional semantic probes and slow-start recovery; intra-cluster traffic prefers same-zone endpoints only where capacity can absorb skew. Loss of one region fences its writer, confirms replica recovery point, promotes authority in a permitted region, scales reserved capacity, and shifts cohorts. Failback creates a new plan after reconciliation rather than reversing DNS. Quarterly evacuation disables regional control dependencies, not merely workloads, and measures tenant journeys, RPO/RTO, operator access, audit, and eventual cleanup.

### Connections

Regional design consumes platform SLO/capacity models from PLAT-081–082, fleet identity and cells from PLAT-083, dependency maps from PLAT-084, upgrade orchestration from PLAT-085, backup/restore from PLAT-086, and incident command from PLAT-087. It applies earlier identity, tenancy, discovery, networking, policy, supply-chain, audit, API, and observability contracts at geographic scale.

## Governing Question

Which platform outcomes need zonal, cluster, cell, regional, provider, or jurisdictional distribution, and what control/data/traffic design makes each claimed failure set survivable and testable?

Multi-region is not an architectural virtue by itself. It increases copies, links, controllers, identities, deployment states, data replicas, routing decisions, and operating cost. Those additions can improve locality and continuity, or they can create global common-mode failures and irreconcilable data.

The durable design starts with outcome and hazard. Some services need only multi-zone scheduling. Some need a warm recovery region. Some need active reads near users but centralized writes. A small set genuinely needs simultaneous multi-region write service and can fund its data semantics.

## Why This Matters

Regions fail rarely but consequentially. More common failures—identity, configuration, rollout, quota, DNS, provider API, certificate, network, registry, or human control—can cross regions if architecture centralizes them. Geographic distance is not operational independence.

Locality matters outside disaster recovery. Latency, data residency, sovereignty, egress cost, market access, and tenant isolation may require regional service. Those constraints can conflict: nearest is not always legally or technically eligible.

Traffic is easier to move than authority. A global load balancer can route to a second region in seconds while the destination lacks current data, write authority, keys, capacity, dependencies, or compatible policy. This produces a larger incident while dashboards celebrate successful failover.

Multi-region systems are continuously in partial transition: deployments propagate, replicas lag, endpoints change, certificates rotate, and regions partition. Explicit skew, conflict, staleness, and recovery rules are normal control-plane behavior rather than exceptional runbook details.

## Prerequisites and Retrieval

Retrieve failure domains, common-cause analysis and cells; Kubernetes clusters, zones, node labels, topology spread, Services, EndpointSlices and traffic distribution; Multi-Cluster Services API and ClusterSets; Gateway/API and global load balancing; DNS caching, TTL and connection persistence; fleet inventory and identity; scheduling/placement constraints; capacity and overload; SLO/RPO/RTO; data replication, consensus, quorum, leader/fencing, sharding, CRDT/conflict resolution and PITR; identity federation, PKI, KMS and policy distribution; GitOps and progressive delivery; network segmentation and service mesh; observability/audit; incident command; regional evacuation, recovery and failback; residency/privacy; and cost allocation.

Distinguish zone from region; cluster from cell; geographic distribution from independent failure; high availability from continuity; endpoint health from service readiness; locality preference from hard residency; logical service identity from namespace/name coincidence; discovery from routing; active-active serving from multi-writer data; replica freshness from committed durability; traffic failover from authority transfer; RTO from DNS TTL; standby capacity from quota; regional autonomy from permanent divergence; failback from rollback; and tested evacuation from architecture review.

## Learning Objectives

After completing this module, you should be able to:

1. derive zonal, cluster, cell, regional, provider, and jurisdiction topology from outcome-specific hazards and objectives;
2. model stable regional inventory, correlation, autonomy, capacity, data, trust, dependency, and recovery evidence;
3. design hierarchical global/regional control planes that tolerate partitions and bound shared-manager blast radius;
4. implement hard-constrained workload placement and locality-aware traffic steering without confusing proximity with eligibility;
5. define multi-cluster service identity, discovery, authorization, endpoint health, and version semantics;
6. choose single-writer, partitioned-owner, active-read, or multi-writer data patterns with explicit RPO, consistency, and reconciliation;
7. calculate failover headroom and prepare quota, network, key, artifact, control-plane, and stateful capacity before failure;
8. orchestrate fenced, idempotent regional failover and failback across traffic, data, identity, queues, and external effects;
9. operate version, policy, telemetry, incident, and security boundaries across regional partitions; and
10. verify regional claims through representative dependency isolation, evacuation, recovery, and reconciliation exercises.

## Core Exposition

### Start from outcomes and failure sets

For each platform journey—authenticate, resolve, deploy, schedule, enforce policy, read/write data, retrieve artifacts, observe, audit, and recover—state required availability, latency, RPO/RTO, residency, tenants, and degraded mode.

Name the failures to survive: node, zone, cluster, cell, region, account, provider service, control plane, identity, network, KMS, DNS, registry, operator compromise, or correlated rollout. “Region loss” is incomplete if recovery still depends on a regional identity endpoint.

Select the least complex topology meeting the objective. Multi-zone may be enough; backup/restore, pilot light, warm standby, active-passive, active-read, partitioned active-active, and multi-writer active-active provide different loss, time, cost, and semantic profiles.

### Define topology and identity

Assign immutable IDs to provider, account/project, jurisdiction, region, zone, cell, cluster, network, and control plane. Keep mutable display names and endpoints separate.

Inventory parentage and correlation: two zones may share regional API, IAM, KMS, backbone, quota, or rollout. Two providers may share DNS registrar, source control, identity, certificates, operators, or submarine cable.

Record owner/on-call, tenant/trust tier, data classes, lifecycle, profile, versions, network reachability, dependencies, capacity, health source/freshness, autonomy limit, and recovery evidence. Do not accept security-sensitive labels solely from the cluster being classified.

### Design repeatable regional cells

A cell packages cluster profile, network, ingress/egress, identity/policy, service discovery, data/cache, artifact access, telemetry/audit, capacity, and recovery contracts into a bounded unit.

Repeatability reduces snowflakes, but parameters must express provider, jurisdiction, capacity, and local integration differences. Pin effective versions and preserve observed conformance.

Keep cell scale bounded so failure, deployment, overload, and evacuation are tractable. Growth adds cells or shards rather than increasing one unique global control domain indefinitely.

### Map hidden common dependencies

Traverse runtime, control, build, trust, data, provider, organizational, and recovery edges for each regional outcome. Test cold paths such as certificate renewal, token issuance, artifact pull, autoscaling, restore, incident login, and DNS changes.

Classify dependency scope and fail behavior. Local token verification may continue while global issuance is unavailable; cached policy may be safe until expiry; queued deploys may pause without affecting running workloads.

Eliminate circular recovery dependencies or create an independently accessible nucleus. If global DNS, SSO, and fleet manager all depend on the impaired platform, operators cannot execute regional failover.

### Choose global and regional control planes

Global planes coordinate catalog, placement policy, fleet releases, global routing intent, trust and governance. Regional planes should enforce local policy, schedule, serve discovery, buffer status, and preserve incident/recovery access within declared autonomy.

Use hierarchical desired state with version, issuer, signature, effective time, expiry, and scope. A region applies only authorized intent for its identity and rejects stale, conflicting, or incompatible revisions according to policy.

Partition global mutating authority by cell, region, environment, or trust tier. Rate-limit fan-out and require rings. A catalog may aggregate globally without giving its reader universal mutation rights.

### Define partition behavior

For each control dependency, define maximum disconnected duration, cached state, expiry, allowed local changes, buffered observations, conflict resolution, and reconnection procedure.

Choose fail-open or fail-closed per outcome and threat. Running workloads may continue under cached authorization while new privileged deploys stop. Do not use one default for every operation.

When connectivity returns, exchange durable revisions and reconcile; do not let “last writer wins” silently replace emergency regional policy or replay obsolete global commands.

### Separate placement eligibility from scoring

First filter regions/clusters by jurisdiction/residency, tenant/trust, capability/version, data authority/freshness, dependency readiness, health freshness, capacity after correlated failure, support state, and recovery evidence.

Then score eligible targets by client/data proximity, latency, balance, egress/cost, carbon, fragmentation, and preference. A cheap or close ineligible region remains forbidden.

Explain every decision using authoritative inputs and their age. Placement is re-evaluated on material state change but protected from flapping through hysteresis, dwell time, and disruption budgets.

### Define multi-cluster service identity

Separate logical service ID from namespace/name, cluster-local Service, regional instance, endpoint, version, tenant, and trust identity. Namespace sameness can simplify Multi-Cluster Services discovery, but governance must guarantee that same names refer to authorized compatible exporters.

ServiceExport expresses intent to export a Service; ServiceImport and EndpointSlices represent imported multi-cluster backends. Treat implementation maturity, ClusterSet membership, controller trust, DNS behavior, and source-cluster attribution as part of the contract.

Discovery answers what endpoints exist. Authorization answers whether a caller may use them. Routing answers which eligible endpoint should receive a request. Do not combine these into a DNS name alone.

### Govern endpoint publication

Publish endpoint identity, source cluster/region, ports/protocol, service/API version, tenant scope, readiness, capacity, data role, locality, and health evidence. Sign or authenticate controller assertions.

Withdraw endpoints on local semantic failure, stale health, incompatible data, quarantine, or authority loss—not only pod readiness. Propagation delay and stale caches mean withdrawal is not instantaneous.

Use leases/expiry for dynamic endpoints and tombstones for removal. Prevent an unreachable cluster’s last-known healthy endpoints from remaining globally routable forever.

### Steer traffic hierarchically

Global steering selects eligible region/cell; regional load balancing selects cluster; cluster Services select endpoints. Each layer must preserve hard policy and expose the decision.

Prefer locality where latency and egress benefit, but reserve capacity for skew. Kubernetes traffic distribution preferences can favor same-zone endpoints, while strict local traffic policies may drop traffic with no local endpoint. Understand precedence and overload implications.

Use slow start, outlier handling, connection limits, circuit breaking and retry budgets. A recovered region should not immediately receive full traffic before caches, autoscaling, dependencies and data are ready.

### Treat DNS as one control, not the failover proof

DNS TTL influences resolver caching but does not bound all convergence. Recursive resolvers, clients, negative caching, JVM/application caches, connection pools, HTTP keepalive, QUIC, and mobile networks may retain old paths.

Use short TTLs only with capacity and query-load analysis. Combine DNS with load-balancer health, connection draining, endpoint expiry, and application retry semantics.

Measure actual client migration distributions. Preserve a safe response from the old region or fence writes while stale clients remain.

### Design data ownership explicitly

Single-writer with replicated readers simplifies conflict but requires writer failover. Partitioned ownership assigns tenant/shard home regions and can scale active-active without concurrent writes to one key. Multi-writer requires domain conflict semantics, not just database replication.

Define consistency, durability, replication mode, lag, failure detection, fencing, promotion, split-brain prevention, read-your-writes/session behavior, schema compatibility, and external effects.

Synchronous cross-region replication can reduce RPO but adds latency and shared quorum dependency. Asynchronous replication improves locality/availability but permits loss or stale reads. State the trade rather than promising all three.

### Fence authority during failover

Before promoting a writer or control authority, prove or conservatively assume the old authority cannot accept conflicting work. Use quorum/lease fencing, provider isolation, token revocation, network policy, epoch numbers, or data-store mechanisms.

Attach epoch/home-region identity to writes and messages. Consumers reject stale epochs. A global router alone cannot fence clients reaching an old endpoint directly.

Record the recovery point and possible lost/duplicated work. Reconcile queues, outboxes, partner calls and user-visible effects before claiming consistent recovery.

### Prepare capacity for correlated loss

Calculate demand after declared failure plus background, retries, recovery, control-plane, observability, and maintenance load. Model tenant and regional traffic distributions rather than dividing fleet total evenly.

Reserve compute, nodes, IPs, load-balancer targets, NAT/egress, storage throughput/attachments, database connections, DNS, certificates, KMS/API quotas, registry bandwidth and operator concurrency.

Warm capacity must be reachable and schedulable. Scaling from zero may depend on the failed provider control API, missing zone labels, image pulls, quotas, or unavailable identity. Test at peak-like load.

### Deploy and upgrade without global blast radius

Build once and promote immutable artifacts, but deploy through representative per-region/cell rings. Preserve compatible regional skew for the maximum rollout and partition window.

Gate on local user/control/data/policy journeys and global effects. A release that succeeds everywhere separately may still break cross-region protocol or replication.

Stop globally or locally based on evidence. During partition, regions must know whether to retain current state, expire risky intent, or accept authorized emergency local change.

### Distribute identity, trust and policy

Prefer local verification of short-lived credentials with bounded cached trust while governing issuer/rotation dependencies. Decide what happens when issuance, revocation, policy data, or KMS is unavailable.

Partition credentials and managers so one regional compromise cannot mutate all cells. Regional break glass must be independently available and externally audited.

Respect residency and privacy in telemetry, identity claims, backups, and control metadata as well as primary data. Global catalogs should expose only necessary metadata.

### Observe regional outcomes independently

Run synthetics from clients and regions, plus local and global signals for traffic, errors, latency, saturation, placement, endpoint publication, data role/lag, replication, DNS, identity/policy, control queues, and audit.

Track signal origin, path and freshness. A global dashboard dependent on the failed region can go blank; a regional system self-report can claim health while externally unreachable.

Correlate requests with region/cell/cluster/endpoint and data epoch without trusting user-supplied labels. Avoid leaking sensitive topology or tenant identity through propagated context.

### Define failover as a state machine

Use states such as Suspected, Declared, Fencing, TargetValidating, AuthorityPromoting, CapacityScaling, TrafficShifting, Reconciling, Stabilized and Failed. Each has actor, preconditions, evidence, deadline, abort and idempotency.

Validate target identity/trust, dependency health, data point/consistency, capacity/quotas, versions/policy, security, observability, incident access and recovery before traffic. Sequence authority and traffic by data model.

Shift cohorts with stop conditions. Preserve old-region evidence and avoid destructive cleanup during uncertainty. Communicate data loss, degraded features and tenant actions precisely.

### Treat failback as a new transition

The original region may return with stale data, queued commands, old endpoints, expired credentials, drift and unknown compromise. Do not reverse the failover script.

Choose whether the recovery region remains home, the original becomes a replica, or authority moves back. Re-seed data, reconcile external effects, rotate identity, validate capacity/dependencies and use a new epoch.

Move traffic gradually and soak. Dispose of emergency capacity and exceptions only after evidence; update topology and recovery records to match the chosen steady state.

### Test real regional claims

Exercise zone loss, cluster loss, global-control partition, identity/DNS/KMS/registry failure, data-replication lag, writer isolation, region/API outage, account compromise, and evacuation. Use failure boundaries that include dependencies.

Start with simulations and shadows, then bounded production game days. Include representative tenants, stateful writes, long-lived sessions, queued work, peak-like capacity, operator handoff and security controls.

Measure detection/declaration, fence time, recovered data point, capacity readiness, client migration, semantic journey recovery, RTO/RPO, reconciliation and cleanup. A traffic switch alone is not a passed exercise.

### Govern complexity and cost

Attribute duplicated infrastructure, cross-region transfer, replication, global control, observability, licenses, exercises, and on-call expertise to the outcomes they protect.

Measure regional utilization and failover headroom separately. Do not “optimize” reserved recovery capacity away without changing the service objective and evidence.

Retire unused regions/cells through dependency, data, DNS, trust, backup, audit, billing and tombstone workflows. Dormant regional infrastructure still carries attack surface and drift.

## Definitions and Notation

Let topology domains be $D=Z\cup C\cup L\cup R\cup P$, representing zones, clusters, cells, regions and providers/accounts. A correlation relation $Corr(d_1,d_2,k)$ records shared failure cause $k$ with evidence and time.

For workload $w$, $E_w(t)\subseteq R$ is the set of regions satisfying hard eligibility at $t$. Let demand be $\lambda_w(r,t)$, usable capacity $\mu_w(r,t)$, and failure set $F$. A necessary capacity condition is

$$
\sum_{r\in E_w(t)\setminus F}\mu_w(r,t)
\geq \sum_r\lambda_w(r,t)+RecoveryLoad_w(t),
$$

subject also to per-region, dependency, quota and data-authority constraints; aggregate inequality alone is insufficient.

Let data state use epoch $e$, authority $a(e)$, committed point $p_r$, and replication lag $\ell_{r_1,r_2}$. A promotion is safe only if prior authority is fenced, target recovery point is accepted, and every new write carries the new epoch.

For client $x$, observed failover time is when its requests reach an accepted target and preserve required semantics. DNS update time plus TTL is not substituted for this measurement.

Regional evidence $V(o,F,t)$ binds outcome, failure set, target topology, tenant/data cohorts, test version, actual RPO/RTO, capacity, dependencies, authority transitions, reconciliation, time and observer.

## Mechanisms, Invariants, or Proof Structure

### Regional platform mechanism

1. **Specify:** define outcomes, latency/residency, failure sets, RPO/RTO, degraded modes and tenants.
2. **Model:** inventory zones, clusters, cells, regions, providers, trust and correlation.
3. **Map:** identify runtime, control, data, build, identity, provider and recovery dependencies.
4. **Partition control:** assign global/regional authority, autonomy, stale-intent, conflict and reconnection rules.
5. **Place:** filter by hard eligibility, then score locality, balance, cost and preferences.
6. **Discover and route:** publish authenticated service/endpoints with locality, health, version, capacity and data role.
7. **Govern data:** define home/partition/write authority, consistency, replication, fencing, RPO and reconciliation.
8. **Reserve:** provision correlated-failure capacity, quotas, keys, networks, artifacts, control and operator access.
9. **Change safely:** deploy through cell/region rings under compatible skew and local/global stop gates.
10. **Fail over:** fence, validate, promote authority, scale, shift traffic, reconcile and stabilize idempotently.
11. **Fail back or re-home:** treat returned state as untrusted/stale, reconcile, create a new epoch and transition gradually.
12. **Verify and govern:** exercise real dependency boundaries, measure outcomes, repair gaps, attribute cost and retire safely.

### Topology identity invariant

Every decision and observation binds immutable region/cell/cluster IDs and authoritative correlation metadata. Mutable names, labels, endpoints and provider display strings cannot silently change failure or trust identity.

### Eligibility invariant

Residency, trust, capability, data, dependency, health freshness, failure capacity and recovery readiness are hard filters. Optimization cannot select outside the eligible set.

### Regional autonomy invariant

Loss of global coordination leaves each region able to preserve declared local outcomes and safety for a bounded interval, after which explicit expiry/degradation rules apply; reconnect uses versioned reconciliation.

### Traffic and data invariant

An endpoint receives traffic only when service/version/tenant compatibility, capacity and health are fresh and its data role permits the operation. Write authority is fenced by epoch independently of routing.

### Capacity invariant

Usable capacity and quotas outside any declared failure set cover demand, retries, control, recovery and maintenance while preserving protected tenant/service budgets.

### Transition evidence invariant

Failover/failback state, authority, actions, data points, client migration, semantic tests, loss/time and reconciliation are independently observed and audited; command acceptance or DNS change is not completion.

### Proof sketch: multiple regions cannot prove regional resilience

Construct two deployments with identical healthy clusters in three regions. In the first, each region has independent identity verification, artifacts, policy, data recovery, control and operator access. In the second, all regions require one identity/KMS/registry/control plane located in region A. Under normal observations they are identical. When A and its services fail, only the first preserves regional outcomes. Therefore region count cannot prove regional resilience; dependency independence and exercised outcome evidence are necessary.

### Executable placement-eligibility audit

This synthetic audit classifies nine candidate regions by the first hard placement failure. It demonstrates filter-before-score logic, not real regional safety or provider independence.

<!-- bijux-verify: {"id":"regional-placement-eligibility-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"eligible=3\nresidency=1\ntrust=1\ndata=1\nstale_health=1\ncapacity=1\nrecovery=1\n"}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    name: str
    residency: bool
    trust: bool
    data_ready: bool
    health_age_seconds: int
    failover_capacity: bool
    recovery_tested: bool


regions = [
    Region("north-a", True, True, True, 4, True, True),
    Region("north-b", True, True, True, 7, True, True),
    Region("west-a", True, True, True, 9, True, True),
    Region("outside-jurisdiction", False, True, True, 3, True, True),
    Region("untrusted-account", True, False, True, 2, True, True),
    Region("replica-lagged", True, True, False, 5, True, True),
    Region("health-unknown", True, True, True, 91, True, True),
    Region("cold-quota", True, True, True, 6, False, True),
    Region("restore-untested", True, True, True, 8, True, False),
]

freshness_limit = 30
counts = {
    "eligible": 0,
    "residency": 0,
    "trust": 0,
    "data": 0,
    "stale_health": 0,
    "capacity": 0,
    "recovery": 0,
}

for region in regions:
    if not region.residency:
        counts["residency"] += 1
    elif not region.trust:
        counts["trust"] += 1
    elif not region.data_ready:
        counts["data"] += 1
    elif region.health_age_seconds > freshness_limit:
        counts["stale_health"] += 1
    elif not region.failover_capacity:
        counts["capacity"] += 1
    elif not region.recovery_tested:
        counts["recovery"] += 1
    else:
        counts["eligible"] += 1

for key, value in counts.items():
    print(f"{key}={value}")
```

### Verification strategy

Unit-test topology identity, hard-filter precedence, stale/unknown behavior, routing hysteresis, endpoint expiry, epoch fencing, failover states, idempotency, capacity arithmetic and conflict reconciliation. Contract-test MCS/discovery, DNS/load balancers, identity/policy, replication, GitOps and provider APIs across supported regional skew. Rehearse zone/cluster/cell/region, global-manager, DNS, identity, KMS, registry, telemetry, network and account failures. Fault-inject replica lag, split authority, stale endpoints, quota exhaustion, retry storms, long-lived sessions and controller partitions. Use representative tenant/data cohorts and peak-like load. Measure semantic recovery, client migration, RPO/RTO, reconciliation and cleanup; audit residency, trust, emergency access and cost/headroom preservation.

## Alternatives and Trade-Offs

- **Multi-zone versus multi-region:** zones are simpler and lower latency; regions cover broader faults and residency but add data/control/operational complexity.
- **One regional cluster versus multiple cells:** one cluster pools capacity; cells bound blast radius, variants and evacuation size at greater overhead.
- **Central versus hierarchical control:** central control gives consistent global view; hierarchical regional control preserves autonomy and contains credentials but needs reconciliation.
- **Push versus pull configuration:** push offers immediate command; pull fits regional isolation and buffering. Both require scoped identity, versions, expiry and stops.
- **Global service name versus explicit regional names:** global names simplify clients; explicit names expose authority/locality. Offer logical identity with inspectable routing.
- **DNS versus anycast/proxy steering:** DNS is broad and cacheable but converges variably; proxies steer connections precisely but become critical global infrastructure.
- **Locality preference versus strict locality:** preference falls back when local endpoints vanish; strict locality preserves boundaries/source identity but can drop traffic.
- **Active-passive versus active-active:** passive simplifies writes and conflict; active improves utilization/latency and exercises capacity but multiplies consistency paths.
- **Single writer versus multi-writer:** single authority is easier to fence; multi-writer improves local availability only with domain conflict semantics.
- **Synchronous versus asynchronous replication:** synchronous reduces loss but adds latency/coupling; asynchronous improves autonomy but admits RPO and stale reads.
- **Home-region sharding versus global data:** home regions align ownership/residency; global data simplifies access but magnifies consensus and compliance scope.
- **Hot standby versus warm/pilot light:** hot capacity lowers RTO and control-plane reliance; warm/cold reduces cost but adds scale/quota/image risk.
- **Uniform regional parity versus intentional tiers:** parity simplifies failover; tiers control cost and jurisdiction differences but require explicit degraded modes.
- **Automated versus commanded failover:** automation reduces detection delay; ambiguous partitions and data authority can cause split brain. Automate preconditions and retain governed authority.
- **Fast traffic shift versus staged cohorts:** fast limits source harm; staged shifts expose destination capacity/data defects before global overload.
- **Failback versus permanent re-home:** failback restores planned topology; re-home avoids another risky transition but changes latency, cost and governance.
- **Multi-cloud versus single-provider regions:** multi-cloud can reduce provider common cause; shared dependencies and lowest-common-denominator operations may dominate.
- **Maximum resilience versus economic efficiency:** every independent copy and control path costs money and expertise; tie each to a named outcome and failure set.

## Failure Modes and Misconceptions

- **“Three clusters mean multi-region.”** Their actual region and shared dependencies determine scope.
- **“Three regions mean resilience.”** Global identity, DNS, KMS, registry or control may be the cut set.
- **“Availability zones never fail together.”** Regional services, configuration and correlated hazards can cross zones.
- **“Nearest region is best.”** Residency, trust, data, dependencies, capacity and recovery are hard constraints.
- **“Placement labels are authoritative.”** Compromised or stale clusters can misreport; verify sensitive facts independently.
- **“Service name sameness proves identity.”** Namespace/name convention does not authorize an exporter or ensure compatibility.
- **“Discovery routes traffic.”** Endpoint knowledge, authorization, selection and data authority are separate.
- **“Pod Ready means regional endpoint healthy.”** User semantics, dependencies, capacity and data role may fail.
- **“DNS TTL bounds failover.”** Resolver/client caches and persistent connections outlive it.
- **“Low TTL is free.”** It increases query/control dependency and does not move open connections.
- **“Global load balancing handles disaster recovery.”** It cannot create data, keys, capacity, dependencies or authority.
- **“Active-active means write anywhere.”** Many active systems use one writer or partitioned ownership.
- **“Asynchronous replica means no data loss.”** Lag and promotion point define RPO.
- **“Synchronous replication guarantees availability.”** Cross-region quorum/latency can reduce write availability.
- **“Routing away fences the old writer.”** Direct/stale clients may still reach it; use data/control fencing.
- **“Standby can scale when needed.”** Cold quotas, IPs, images, APIs and failed dependencies may block it.
- **“Half-used fleet has 50% failover headroom.”** Demand and dependencies are not uniformly movable.
- **“Autoscaling supplies resilience.”** It may depend on the failed regional/provider control plane.
- **“Identical configuration gives independence.”** One bad global rollout can fail identical cells together.
- **“Different providers eliminate correlation.”** DNS, identity, code, keys, network and operators may remain shared.
- **“Regional autonomy means accepting all writes.”** Safe degradation may stop privileged or conflicting work.
- **“Last known healthy is healthy.”** Evidence expires; unknown endpoints must leave eligible routing.
- **“Fail-open or fail-closed is global policy.”** Choose by operation, consequence and cached evidence.
- **“Failover is one switch.”** fencing, data, capacity, traffic, queues, security and validation are ordered states.
- **“Failback reverses failover.”** Returned state is stale/divergent and needs a new transition.
- **“Traffic restored means recovery complete.”** Data loss, queues, identity, audit and emergency changes require reconciliation.
- **“A game day can delete one pod.”** Regional claims require isolating relevant dependency/control boundaries.
- **“Synthetic traffic represents all tenants.”** Include stateful, regulated, long-lived and low-volume cohorts.
- **“Reserved capacity is waste.”** It purchases a declared recovery objective; removing it changes the promise.
- **“Every workload needs multi-region.”** Complexity can reduce reliability when the outcome does not require it.

## Worked Examples

### Example 1

A service runs in three clusters, all in one cloud region. Inventory corrects the “multi-region” label and shows regional DNS, KMS and database as cut sets. The team first delivers multi-zone resilience, then funds a warm second-region cell only for outcomes whose RTO requires it.

### Example 2

Two regions export the same namespaced Service through MCS. Admission verifies ClusterSet membership, owner, API version and tenant scope before export. EndpointSlices retain source-cluster identity; callers authorize logical service identity rather than trusting the DNS name alone.

### Example 3

Same-zone traffic preference reduces latency and egress, but one zone receives 70% of clients. Local endpoints overload. The platform scales each zone by local demand, sets cross-zone fallback, monitors skew and keeps strict locality only for workloads whose policy requires it.

### Example 4

Global DNS marks a region unhealthy and changes records, yet 18% of clients keep old connections for nine minutes. The old cell continues safe reads, rejects writes after epoch fencing, and sends retry guidance. Recovery measurement uses actual accepted requests, not record publication time.

### Example 5

A tenant’s home-region writer fails with 47 seconds of asynchronous lag. Incident command fences the old epoch, reports the accepted recovery point, promotes the allowed replica and reconciles outbox/provider effects. The service meets its one-minute RPO but does not claim zero loss.

### Example 6

A warm region has compute headroom but cannot attach enough volumes because quota was never raised. A game day catches this before production. The capacity contract adds attachment, IP, database, KMS, load-balancer, certificate and registry budgets plus quarterly verification.

### Example 7

Global policy connectivity fails. Regions continue cached runtime authorization for 30 minutes, reject new privileged deployments after five minutes, buffer audit locally and permit independently authenticated incident access. Reconnect compares revisions and preserves an approved emergency local rule.

### Example 8

A fleet release crosses regions in minutes and breaks every identical DNS controller. The redesign uses one cell per topology/provider cohort, semantic DNS probes, bounded fan-out and a global stop. Identical artifacts remain, but exposure is deliberately non-simultaneous.

### Example 9

After failover, the original region returns with queued deployments and old certificates. The platform keeps it fenced, re-seeds data, discards obsolete commands by epoch, rotates trust, validates dependencies and makes it a replica. Business chooses not to fail back, and inventory/home-region state changes explicitly.

### Example 10

A multi-cloud exercise disables the primary provider but fails because both providers rely on the same corporate SSO and DNS registrar account. Recovery architecture adds separate emergency identity, delegated DNS control, externally stored runbooks and tests those paths before renewing the multi-cloud claim.

## Cross-Program Connections

- **Systems Engineering:** hazards, failure correlation, assurance cases, feedback delay and state machines define regional claims.
- **Distributed Systems:** consensus, partitions, CAP trade-offs, epochs, fencing, replication, clocks and conflict resolution govern data authority.
- **Networking:** DNS, anycast, load balancing, connection persistence, locality, routing convergence and circuit breaking move traffic.
- **Data Engineering:** sharding, lineage, replication lag, watermarks, replay and reconciliation make regional data meaningful.
- **Security Engineering:** trust domains, federation, KMS/PKI, compromise containment, residency and break glass constrain topology.
- **API and Service Engineering:** service identity, compatibility, discovery, idempotency, retries and traffic policy span clusters.
- **Reliability Engineering:** SLO/RPO/RTO, cells, overload, game days, incident response and disaster recovery provide evidence.
- **Operations Research:** constrained placement, capacity reservation, demand distributions and cost optimization shape decisions.
- **Governance and Privacy:** jurisdiction, tenant contracts, audit, data movement and notification limit eligible regions.
- **Platform Product Management:** outcome tiers, developer experience, chargeback and roadmap choices justify complexity economically.

## References

1. Kubernetes SIG Multicluster. [Multicluster Services API Overview](https://multicluster.sigs.k8s.io/concepts/multicluster-services-api/). Retrieved 2026-09-02.
2. Kubernetes SIG Multicluster. [ServiceExport](https://multicluster.sigs.k8s.io/api-types/service-export/). Retrieved 2026-09-02.
3. Kubernetes SIG Multicluster. [ServiceImport](https://multicluster.sigs.k8s.io/api-types/service-import/). Retrieved 2026-09-02.
4. Kubernetes. [Running in Multiple Zones](https://kubernetes.io/docs/setup/best-practices/multiple-zones/). Retrieved 2026-09-02.
5. Kubernetes. [Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/). Retrieved 2026-09-02.
6. Kubernetes. [Virtual IPs and Service Proxies](https://kubernetes.io/docs/reference/networking/virtual-ips/). Retrieved 2026-09-02.
7. Kubernetes. [Service API](https://kubernetes.io/docs/reference/kubernetes-api/service-resources/service-v1/). Retrieved 2026-09-02.
8. Kubernetes. [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/). Retrieved 2026-09-02.
9. Kubernetes. [Production Environment](https://kubernetes.io/docs/setup/production-environment/). Retrieved 2026-09-02.
10. Cluster API. [Introduction](https://main.cluster-api.sigs.k8s.io/). Retrieved 2026-09-02.
11. Google Cloud. [Multi-Regional Deployment Archetype](https://cloud.google.com/architecture/deployment-archetypes/multiregional). Retrieved 2026-09-02.
12. AWS. [Multi-Region Fundamental 1: Understanding the Requirements](https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-multi-region-fundamentals/fundamental-1.html). Retrieved 2026-09-02.
13. AWS. [Multi-Region Fundamental 4: Operational Readiness](https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-multi-region-fundamentals/fundamental-4.html). Retrieved 2026-09-02.
14. AWS. [Use Defined Recovery Strategies to Meet Recovery Objectives](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_planning_for_recovery_disaster_recovery.html). Retrieved 2026-09-02.
15. Google. [Site Reliability Engineering: Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Choose a regional topology for a platform with global reads, tenant-home-region writes, regulated residency, a 15-minute RTO, and one-minute RPO. State outcomes, failure sets, cells, control planes, data authority, and evidence.

### Exercise 2

Design multi-cluster service discovery and traffic steering for clusters with different regions, versions, tenant scopes, capacity, and data roles. Include identity, publication, withdrawal, authorization, and staleness.

### Exercise 3

Calculate and validate failover capacity for loss of the busiest region when traffic, stateful attachments, KMS, DNS, registry, control APIs, retries, and recovery work are unevenly distributed.

### Exercise 4

Create a regional failover and failback state machine for an asynchronously replicated single-writer service with long-lived clients, queued external effects, and a possibly partitioned old region.

### Exercise 5

Design a game-day program that tests zonal, cluster, cell, regional, global-control, identity, DNS, KMS, registry, telemetry, account, and provider correlation without creating uncontrolled production risk.

## Answers to the Exercises

### Answer 1

Use repeatable multi-zone regional cells in allowed jurisdictions, with at least one prepared recovery cell outside each declared regional failure. Global reads route only to replicas meeting freshness/session policy. Partition tenants by immutable home region; a fenced single writer accepts their writes, with asynchronous replication whose measured lag stays within one minute or blocks the promise.

Use a hierarchical global catalog/placement plane and regional identity verification, policy, discovery, execution, telemetry buffering and incident access. Global loss permits bounded reads/running workloads but stops new privileged changes after expiry. Partition manager credentials and rollout rings.

Reserve target compute, IP, volume, database, network, KMS, DNS, registry and control capacity for the busiest-region loss plus retry/recovery load. Evidence comes from representative evacuation with data epoch promotion, actual recovery point, client migration, tenant read/write/deploy/auth journeys, residency checks, 15-minute acceptance, reconciliation and clean failback/re-home.

### Answer 2

Give logical service, regional instance, cluster Service, endpoint and version separate stable identities. Authorize ServiceExport only for owned compatible service/tenant contracts and authenticated ClusterSet members. ServiceImport/EndpointSlice records retain source cluster/region, ports, version, health source/time, capacity and data role.

Endpoint publication uses leases and semantic probes; stale, quarantined, incompatible, data-unready or unauthorized exporters withdraw and leave tombstones. Discovery never grants caller authorization. Regional and workload identity policy checks tenant/service before routing.

Filter endpoints by trust, residency, version, data authority, dependencies, health freshness and capacity, then prefer local region/zone. Add hysteresis, slow start, connection limits, fallback and retry budgets. Test DNS caches and long-lived sessions; measure actual client paths and ensure old epochs cannot write after routing changes.

### Answer 3

Model demand per tenant/service and source region at peak, then remove the busiest region and every dependency correlated with it. Add retry amplification, recovery transfers, observability, control-plane work and one maintenance margin. Do not rely only on aggregate CPU.

For each surviving eligible region verify compute/node pools, schedulable topology, IP/NAT/egress, load-balancer targets, volume count/throughput/attachments, database connections/storage/replication, KMS/API/DNS/certificate quotas, registry bandwidth, identity/policy, and operator concurrency. Respect residency and data-home constraints, which may make nominal capacity unusable.

Reserve or pre-provision gaps; exercise at peak-like distribution with the source isolated. Measure scale time, throttling, saturation, protected-tenant budgets and semantic outcomes. If cold control APIs cannot meet 15 minutes, fund warm capacity or revise the objective explicitly.

### Answer 4

States are Suspected, Declared, Fencing, TargetValidating, AuthorityPromoting, CapacityScaling, TrafficShifting, Reconciling, Stabilized, and later Re-homePlanning/Failback. Fence old writer by quorum/lease epoch and network/provider controls before promotion; if fencing cannot be proved, stop conflicting writes.

Select an accepted replica point and disclose possible loss. Promote a new epoch, attach it to writes/messages, scale reserved capacity, validate identity/dependencies/data/telemetry, then shift client cohorts. Old/stale connections may read safely but reject old-epoch writes. Reconcile queue IDs, outbox, partner effects and user transactions idempotently.

On return, keep the old region quarantined. Inventory stale data, queued commands, credentials and external state; re-seed from current authority and rotate trust. Decide permanent re-home or a new authority transition. Failback uses a new epoch, fresh capacity/dependency gates, staged traffic and reconciliation—not reverse DNS.

### Answer 5

Maintain simulations and automated dependency/placement/capacity checks, then bounded production exercises. Rotate zone and cluster loss; isolate an entire cell; partition global management; disable identity issuance while verifying cached local validation; test DNS/KMS/registry/telemetry and recovery access; simulate account/provider failure with external communication.

Each exercise has exact scope, commander, tenant/data cohorts, safety limits, abort/recovery, evidence and communication. Use representative stateful writes, long-lived clients, queue/external effects, low-volume regulated tenants and peak-like demand. Do not call a pod deletion a regional test.

Measure detection/declaration, fencing, replica point/RPO, capacity readiness, endpoint withdrawal, real client migration, semantic journeys, RTO, operator access, audit, reconciliation, failback/re-home and emergency cleanup. Gaps become owned recovery debt; successful evidence expires when topology, versions, keys, dependencies, capacity or procedures materially change.
