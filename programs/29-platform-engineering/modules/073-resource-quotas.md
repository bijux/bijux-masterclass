---
module_id: PLAT-073
program: Platform Engineering
level: 2
module_number: 73
title: Resource Quotas
status: complete
last_verified: 2026-09-02
---

# Resource Quotas

## One-Page Review

### Governing question

How should a platform allocate and enforce finite compute, memory, storage, network, control-plane, API, queue, database, provider, and human-operational capacity so tenants make progress fairly, critical work survives overload, bursts remain useful, cost stays governed, and quota never masquerades as guaranteed capacity?

### Essential definitions

- A **resource request** declares capacity used for placement/admission and often a workload’s expected steady need.
- A **resource limit** is an enforcement ceiling on an instance or operation; its behavior is resource-specific, such as CPU throttling or memory termination.
- A **quota** bounds aggregate allocation, object count, rate, concurrency, or another dimension within a scope.
- A **reservation/guarantee** is capacity protected for a tenant/class under stated failure and scheduling conditions; quota alone does not reserve supply.
- A **burst allowance** permits bounded use above a steady entitlement when spare capacity exists.
- A **budget** constrains monetary spend or alerts on it; it is not necessarily a real-time admission control.
- An **allocation quota** caps held resources; a **rate quota** caps operations per interval; a **concurrency quota** caps simultaneous operations.
- **headroom** is deliberately unallocated capacity for variance, failover, upgrades, recovery, system work, and bursts.
- **overcommit** admits declared limits above physical capacity based on requests and expected simultaneous use, accepting contention/eviction risk.
- **fairness** is the policy that determines comparative progress under contention; equality, weights, priorities, guarantees, and dominant-resource share are different policies.
- A **hierarchical quota** allocates capacity through organization, tenant, project, environment, and workload scopes without allowing descendant totals to escape ancestor bounds.
- A **quota lease** is a time-bounded allocation for scarce or long-running work that can expire, renew, and be reclaimed under explicit semantics.

### Central model, mechanism, or theorem

Let resources be $j\in R$, tenants $i\in T$, physical/effective capacity $C_j$, protected system reserve $H_j$, tenant guarantee $g_{ij}$, quota $q_{ij}$, and current admitted allocation $x_{ij}$. Feasibility requires

$$
0\le g_{ij}\le x_{ij}\le q_{ij},\qquad
\sum_i x_{ij}\le C_j-H_j
$$

for non-overcommitted resources and the analogous policy-specific bound for overcommitted ones. A quota is reachable only if placement, provider ceilings, fragmentation, and all ancestor/shared bottlenecks permit it; it is guaranteed only when capacity and scheduling protect $g_{ij}$. Admission evaluates the full resource vector atomically enough to avoid partial allocation. Under overload, priority protects declared critical work, fairness shares progress within a class, bounded queues absorb short bursts, and rejection/backpressure prevents collapse.

### Critical invariants

- Requests, limits, quotas, guarantees, bursts, capacity, and monetary budgets are distinct and labeled honestly.
- Every exhaustible resource has a named authority, unit, scope, refresh behavior, enforcement point, and observation.
- Tenant/project/workload quota cannot exceed effective ancestors or provider ceilings without an approved capacity plan.
- Admission is deterministic for one versioned quota snapshot and leaves no leaked partial reservation on failure.
- Critical system/recovery capacity is protected from ordinary workload and replay/batch consumption.
- Fairness is enforced across all material bottlenecks; CPU fairness does not excuse database, API, queue, or operator starvation.
- Requests/defaults reflect measured needs closely enough for scheduling and capacity planning; missing requests cannot obtain unbounded implicit share.
- Burst borrowing is revocable and never presented as a guarantee; reclamation and disruption semantics are explicit.
- Rate and concurrency limits return machine-readable retry/backpressure information and retries cannot amplify overload.
- Quota changes, overrides, leases, and emergency elevation have owner, reason, approval, expiry, audit, and rollback.
- Usage and quota telemetry is timely and scoped, but enforcement does not depend on a lagging billing/reporting pipeline.
- Deletion, failed workflows, orphaned provider resources, stuck finalizers, and expired leases return capacity through reconciliation.

### Common failures

Quota equals capacity; limit equals request; budget alert equals spend prevention; CPU/memory as the only resources; default request too small; memory overcommit treated like CPU; no object-count quota; quota larger than node/provider capacity; namespace quota without cluster headroom; child quotas exceeding parent; first-come-first-served called fair; priority without starvation control; burst with no reclamation; retry storm after 429; long queue with expired user intent; quota increase instead of leak cleanup; dashboards hours behind enforcement; per-tenant labels exploding metrics; system workloads sharing ordinary quota; scale-out blocked by provider IP/API quota; and deleted resources whose external capacity never returns.

### Compact example

Cluster cell has 1,000 CPU, 4 TiB memory, and 2,000 database connections. Platform reserves 15% CPU/memory and 300 connections for system, upgrades, and recovery. Tenant `tn-82` receives guarantee 80 CPU/256 GiB/120 connections, hard quota 160/512/180, plus token-bucket API rate 200/s with burst 400 and 20 concurrent environment creates. Scheduler admits against requests, connection broker against explicit leases, API gateway against tokens/concurrency, and provider reconciler against account quotas. Spare CPU may be borrowed, but eviction/reclamation favors guarantees and critical priority. A displayed “160 CPU quota” is not called reserved capacity; placement UI also reports current cell headroom, fragmentation, and provider constraints.

### Connections

This module extends tenant fairness from [PLAT-071](071-tenant-models.md) and infrastructure boundaries from [PLAT-072](072-namespace-account-and-cluster-isolation.md). It composes policy enforcement from [PLAT-066](066-policy-decision-and-enforcement-points.md), durable workflows from [PLAT-065](065-workflow-and-orchestration-layers.md), event replay controls from [PLAT-069](069-platform-eventing.md), health/telemetry contracts from [PLAT-047](047-health-and-telemetry-contracts.md), and cost-aware platform APIs from [PLAT-060](060-designing-a-domain-specific-platform-api.md).

## Governing Question

How can a platform translate finite, multidimensional, time-varying capacity into understandable entitlements and overload behavior without creating starvation, stranded reservations, false guarantees, or retry-driven collapse?

Quota is an allocation control, not merely a Kubernetes object or cloud-provider number. Workloads consume many resources with different enforcement physics: CPU can be time-shared, memory cannot be reclaimed without disruption, storage persists, IPs and load balancers are discrete, API calls are rates, long operations consume concurrency, and support teams have finite attention.

The design must connect product tiers and tenant requirements to actual bottlenecks. A 1,000-pod quota is useless if only ten load balancers or 200 database connections exist. A generous cloud API rate does not help if one admission webhook serializes all requests.

Quota should create predictable progress and controlled failure. That requires capacity models, reservations, fairness, queues, backpressure, reconciliation, evidence, and a product experience that explains what is constrained and why.

## Why This Matters

Shared platforms fail first at the resource nobody inventoried. A tenant may stay below CPU limits while exhausting API-server concurrency, IPs, storage IOPS, database locks, broker partitions, provider create operations, or controller work queues.

Incorrect declarations also waste capacity. Inflated requests prevent scheduling and raise cost; missing requests make low-priority workloads look cheap until contention. Limits too close to normal usage create throttling or termination, while limits far above capacity conceal risk.

Quota failures directly affect user trust. An unexplained `quota exceeded` after a long workflow feels arbitrary. A quota increase that cannot be placed is dishonest. A platform should preview effective constraints, identify the binding dimension, link ownership and remediation, and distinguish wait, resize, delete, purchase, or request-increase actions.

Overload is inevitable. Fairness and protected capacity decide whether leader election, reconciliation, deletion, incident response, and recovery continue while noncritical work is throttled. Quota design is therefore reliability architecture.

## Prerequisites and Retrieval

Retrieve capacity planning, queues and Little’s Law, scheduling, bin packing, fairness, priorities, rate limiting/token buckets, backpressure, retries, Kubernetes requests/limits/QoS/ResourceQuota/LimitRange/API Priority and Fairness, cloud service quotas, databases/connections, storage/network limits, multi-tenancy, SLOs, cost allocation, distributed leases, workflows, reconciliation, and observability.

Distinguish request from limit; quota from guarantee; capacity from allocatable capacity; reservation from actual use; average from peak; resource quantity from operation rate; rate from concurrency; queue length from wait time; priority from fairness; fairness from equality; burst from entitlement; borrowing from ownership; overcommit from oversubscription accident; namespace quota from provider quota; budget alert from enforcement; resource release from deletion request; and reported usage from authoritative admission state.

## Learning Objectives

After completing this module, you should be able to:

1. inventory allocation, rate, concurrency, object-count, storage, network, provider, and operational bottlenecks;
2. define requests, limits, quotas, guarantees, bursts, headroom, overcommit, and budgets precisely;
3. construct feasible multi-resource and hierarchical allocations;
4. design admission, reservation, lease, queue, and release state machines;
5. apply weighted fairness and priority without starving critical or small flows;
6. configure Kubernetes and provider quota controls as complementary layers;
7. return useful quota errors, previews, usage, and remediation to platform consumers;
8. observe saturation, throttling, queue age, fragmentation, leaks, and false headroom;
9. test overload, retries, failover, borrowing/reclamation, stale usage, and recovery; and
10. evolve quota policies and capacity without breaking live workloads or hiding unmet demand.

## Core Exposition

### Inventory every exhaustible resource

Start at user journeys and trace every constrained dependency. Include CPU, memory, ephemeral/storage capacity and IOPS, GPUs/devices, nodes, pods/objects, network bandwidth/connections/IPs/load balancers/NAT ports, API-server seats, admission calls, database connections/locks/transactions, cache, broker partitions/storage, queue workers, provider operations, external API rates, licenses, and human approvals/support.

For each resource record authority, unit, scope, capacity, allocatable share, reserve, current allocation/use, update latency, increase process, failure behavior, and cost. Identify hard system limits that cannot be raised.

Measure correlations. CPU and memory peaks may occur together; failover may double regional demand; a rollout consumes surge nodes, registry bandwidth, API calls, and database connections simultaneously.

Review inventory after architecture and provider changes. Quotas based on yesterday’s bottleneck can merely move failure elsewhere.

### Separate resource vocabulary

A request is an admission/scheduling declaration. A limit constrains an instance. An aggregate quota constrains a scope. A guarantee protects access to capacity. A burst permits opportunistic excess. Physical/effective capacity is what the system can safely serve. A budget governs money.

Document enforcement physics. Kubernetes CPU limits commonly throttle; memory limit pressure can terminate a container. Storage and device allocation persist. API limits reject or delay. Queue concurrency defers work. Provider quotas may be adjustable, fixed, regional, account-scoped, or resource-scoped.

Do not display a hard quota as “available.” Available-to-request depends on current allocation and ancestor/provider constraints; available-to-run also depends on placement, fragmentation, and actual supply.

Avoid one percentage called utilization that mixes requests, use, limits, and quota. Show each denominator.

### Build a capacity envelope

Start from physical/provider capacity and subtract system services, failure reserve, rollout surge, operational recovery, and uncertainty. The remainder is safely allocatable under stated assumptions.

Capacity differs by zone, node type, region, account, and time. Ten free CPUs fragmented across nodes may not place one eight-CPU pod if no node fits. GPUs, IPs, and volumes have topology constraints.

Model failure scenarios: zone loss, node drain, database failover, broker rebalance, provider throttling, identity outage, and traffic surge. A quota feasible only in steady state may violate an availability promise.

Publish capacity-plan assumptions and error bounds. Update them from observed demand without treating a short average as a safe peak.

### Define guarantees and headroom

Guarantees are meaningful only if matching capacity is reserved or scheduled preferentially through tested mechanisms. The sum of guarantees must fit the protected capacity envelope in each relevant failure domain.

Hold headroom for system components, critical reconciliation/deletion, incident response, failover, upgrades, autoscaler delay, and demand variance. Assign ownership; otherwise every team sees headroom as waste available to consume.

Borrow unused guarantee only under explicit policy. A borrower must tolerate reclamation, throttling, preemption, or delayed renewal. Stateful and irreversible work may be poor borrowers.

Track stranded guarantee and unmet guaranteed demand. Adjust through product/capacity review, not silent confiscation.

### Set requests and limits from behavior

Requests should approximate the resources required for acceptable operation, derived from load tests and production observations with headroom. Defaults prevent absent declarations but can become dangerously inaccurate.

Limits protect shared capacity and runaway behavior. Select per resource: CPU limit may cause latency through throttling; memory limit provides a hard containment boundary but termination is disruptive. Some workloads benefit from no CPU limit under an aggregate quota while retaining requests and fairness.

Account for startup, cache warmup, compaction, backups, migrations, and failure modes. Averages miss these peaks.

Continuously compare request, use distribution, throttling, termination, queueing, and SLO. Rightsizing suggestions require owner review and rollback, especially for sparse critical peaks.

### Use Kubernetes ResourceQuota and LimitRange correctly

ResourceQuota bounds aggregate requests/limits, object counts, and selected extended/storage resources in a namespace, possibly scoped by priority or other supported scope. It is admission control; it does not create nodes or reserve a provider service.

LimitRange constrains or defaults per-object/container requests and limits. Defaults help quota accounting, but a default that is too small distorts scheduling and a default limit can unexpectedly throttle/kill.

Ensure all containers, including sidecars and init behavior where applicable, are represented. Platform-injected sidecars consume tenant or platform capacity under an explicit allocation rule.

Test updates and races. Quota usage is controller/admission state, and a created object may not become runnable if cluster capacity, topology, storage, or another quota binds.

### Control object counts and persistent resources

Pods are not the only objects that burden a control plane. ConfigMaps, Secrets, Jobs, Services, LoadBalancers, PVCs, snapshots, CR instances, and failed/finished history consume etcd, controllers, network, storage, and provider resources.

Set object-count quotas based on measured controller/control-plane behavior. Cleanup TTLs and retention keep terminal jobs, events, revisions, and previews from accumulating indefinitely.

Persistent storage quota includes capacity class, snapshot/backup, IOPS/throughput, attachment, topology, and expansion. A PVC deletion request may remain protected by finalizers or provider retention.

Reconcile Kubernetes objects with cloud/provider inventory so leaked load balancers, disks, IPs, databases, and accounts still count against effective allocation until disposed.

### Govern rates and bursts

Token bucket model has refill rate $r$ and capacity $b$: it permits sustained rate $r$ and bursts up to available tokens $b$, subject to downstream concurrency/capacity. Sliding/fixed windows have different edge behavior.

Scope rate limits by authenticated tenant, workload, operation, resource, region, and dependency as needed. IP address is rarely a sufficient tenant identity.

Return clear limit identity, remaining/reset or retry semantics where safe, and an idempotent retry contract. Clients use exponential backoff and jitter and honor server hints.

Rate limit before expensive work, but keep critical health/recovery routes separate. Avoid a single global limiter that a noisy route can consume.

### Limit concurrency and long operations

Rate alone does not protect work that lasts minutes. Concurrency caps bound simultaneous builds, account creates, migrations, database restores, scans, and provider operations.

Acquire a durable lease/reservation before execution, bind it to tenant/operation/resource, renew with fencing where necessary, and release on terminal state. Expiry handles crashed workers, but reconciliation must avoid two owners after a lease ambiguity.

Separate queued, admitted, running, waiting-on-provider, and terminal counts. Decide whether waiting external calls continue to occupy scarce capacity.

Limit concurrency at each bottleneck: platform workflow, provider account/region, database, and downstream service. A higher upstream quota cannot override a lower provider ceiling.

### Build hierarchical quotas

Organizations allocate to business units, tenants, projects, environments, and workloads. Parent quota bounds descendants; child allocations should not make the hierarchy infeasible.

Choose whether unused sibling capacity can be borrowed and how it is reclaimed. Static partitioning is predictable but strands capacity; elastic hierarchy improves use but requires fair scheduling and disruption rules.

Avoid double-counting one workload in overlapping scopes. Define the tree or explicit DAG attribution and the authoritative allocation ledger.

Quota delegation must not allow a child administrator to raise its ancestor or mint guarantee. Changes are optimistic-concurrency controlled and auditable.

### Allocate across multiple resources fairly

Equal CPU quotas can be unfair when one tenant is memory-heavy and another GPU-heavy. Track vectors and identify dominant share—the largest fraction of any capacity consumed by a tenant—as one useful fairness signal.

Dominant Resource Fairness provides a formal allocation approach under specific assumptions; production platforms may need weights, priorities, topology, indivisible jobs, deadlines, and guarantees beyond that model.

Fairness means progress under contention, not identical raw quantities. Paid tiers, regulated recovery, or critical control work may have weights and guarantees, but the policy is explicit.

Prevent gaming through inflated requests or task splitting. Charge allocation based on the resource semantics the scheduler actually protects.

### Combine priority and fairness

Priority decides which class is protected first; fairness shares within a class. Priority without admission can fill a queue with work that will never run; priority without aging/limits can starve lower classes indefinitely.

Reserve critical capacity for control plane, leader election, node health, reconciliation, deletion, security response, and disaster recovery. Do not label ordinary team work “critical” to bypass quota.

Kubernetes API Priority and Fairness classifies requests into priority levels and flows, uses concurrency shares and bounded queuing/rejection, and distinguishes flow fairness. Some long-running request classes have special/exempt behavior; verify current semantics.

Test priority inversion and recursive calls such as admission webhook querying the API. A constrained high-priority operation waiting on low-priority work can deadlock or defeat protection.

### Design queues as bounded capacity controls

A queue absorbs temporary mismatch between arrival $\lambda$ and service $\mu$. If sustained $\lambda\ge\mu$, backlog and waiting time grow; queueing does not create capacity.

Bound length, age, payload size, tenant share, and retry attempts. Expire work whose user intent/deadline is no longer valid, with auditable terminal outcome.

Use fair or weighted scheduling so one tenant’s large batch does not block small interactive work. Shuffle sharding or per-cohort queues can reduce collision/blast radius.

Publish estimated wait carefully and update it; position is unstable under priorities and cancellations. Give users cancellation and duplicate-safe resubmission.

### Apply backpressure instead of retry amplification

When overloaded, reject early with a stable error, delay under a bounded queue, reduce producer rate, shed explicitly optional work, or degrade quality under contract. Silent drops are unacceptable for durable requests.

Retries consume quota and capacity. Budget retry attempts, use jitter, avoid synchronized clients, and distinguish throttling from permanent quota denial. Retrying a hard allocation shortage every second is harmful.

Propagate downstream saturation upstream. A portal accepting unlimited operations while workflows/providers are capped merely hides backlog.

Protect status/cancel/delete endpoints so users and operators can relieve overload even when create paths are throttled.

### Integrate provider and organization quotas

Cloud providers expose allocation, rate, and concurrent quotas at service, account/project, region, resource, or organization scopes. Some defaults are adjustable; some system limits are not.

Maintain machine-readable inventory of effective values, current allocation, requested increases, approval lead time, and quota authority. Do not discover a regional limit during failover.

Map platform products to provider consumption: cluster nodes, IP addresses, load balancers, disks, snapshots, API operations, databases, IAM objects, and log volume.

Reserve provider headroom for failover and incident response. Multiple platform tenants in one account need lower-level fairness; separate accounts may isolate quotas but still share organization/regional limits.

### Connect quota and cost without confusing them

Capacity use drives cost, but quotas are not invoices. Requests may reserve expensive capacity without consumption; egress/API/license cost may scale without CPU allocation.

Show estimated and actual cost alongside quota units. Budget thresholds can alert, require approval, reduce optional work, or deny new spend according to policy, but document timing and enforcement.

Do not terminate production resources automatically because a delayed billing feed crosses a budget unless that destructive policy is explicit and safe.

Charge shared headroom/system cost transparently. Incentives that punish accurate requests encourage under-declaration and instability.

### Expose quota as a platform product

Each plan/class publishes dimensions, units, defaults, guarantee versus ceiling, burst, rate/concurrency, scope, hierarchy, increase process, cost, SLO, and failure behavior.

Preview a request against current policy and capacity without promising future admission. On denial return binding dimension, requested/effective/used/reserved values as disclosure permits, authoritative scope, remediation, owner, and retryability.

Offer self-service increase requests with need, duration, evidence, cost, dependency/provider feasibility, and expiry. Temporary increase is a lease, not forgotten configuration.

Make deletion and rightsizing easy so consumers can return capacity. Provide forecasts before planned launches or migrations.

### Observe quota and fairness

For every resource track capacity, reserve, guarantee, quota, admitted allocation, actual use, pending demand, rejection, throttling, eviction/termination, queue length/age, borrowing, reclamation, fragmentation, and leaked allocation.

Measure per class/cohort and protect per-tenant drill-down. Avoid unbounded tenant/resource IDs as metric labels; use secure logs or queryable records for exact cases.

Track denied demand and abandoned requests, not only utilization. Low use can mean generous capacity, broken admission, or users gave up.

Correlate quota signals with SLOs and cost. A high quota with severe throttling, placement failure, or latency is not healthy.

### Reconcile and release allocations

Allocation state spans admission records, schedulers, Kubernetes objects, provider resources, queues, leases, databases, and billing. Reconcile these sources under explicit authority.

Failed create may leave provider resource. Delete may be stuck. Worker crash may leave lease. Expired token may be cached. Detect and safely adopt, retry, or dispose using stable IDs.

Never decrement quota merely because a delete was requested. Release when the governed resource is absent or transferred according to the resource contract.

Rebuild allocation ledger after restore and prevent double admission until reconciliation reaches a safe boundary.

### Evolve quota policy safely

Increasing ceilings may expose latent downstream constraints; validate capacity and provider quotas first. Lowering quota below current allocation needs grandfather, grace, migration, or controlled reclamation policy.

Version product classes and effective quota calculations. Record which policy admitted each live allocation. Do not retroactively evict stateful work without a contract.

Roll new defaults and fairness algorithms through representative cohorts. Compare allocation, latency, cost, starvation, and SLO outcomes; retain rollback.

Retire dimensions only after all enforcement, clients, dashboards, budgets, and provider mappings migrate. Unknown/unmetered resource is risk, not free supply.

### Test overload and recovery

Test each resource alone and correlated: CPU, memory, storage, objects, IPs, network, API seats, database connections, queues, provider rates/concurrency, and budget controls.

Generate noisy tenants, many small flows, one giant request, hot keys, retry storms, stale usage, lease loss, controller lag, provider 429, partial allocation, and delete failure.

Exercise zone loss, rollout surge, cluster evacuation, regional failover, control-plane saturation, and recovery while guarantees and system reserves are contested.

Verify error contracts, fairness, starvation bounds, cancellation, release, reconciliation, metrics, and audit. Capacity modeling is not proven until stress behavior matches it.

## Definitions and Notation

Let tenants $T$, resource dimensions $R$, effective capacity $C_j$, protected headroom $H_j$, guarantee $g_{ij}$, quota $q_{ij}$, admitted allocation $x_{ij}$, and observed use $u_{ij}$.

For non-overcommitted resource $j$:

$$
0\le g_{ij}\le x_{ij}\le q_{ij},\quad
0\le u_{ij},\quad
\sum_i x_{ij}\le C_j-H_j.
$$

Use can temporarily differ from admitted allocation by resource semantics; $u_{ij}<x_{ij}$ does not mean the guarantee/quota can be revoked instantly.

Tenant $i$ dominant allocation share is

$$
d_i=\max_{j\in R}\frac{x_{ij}}{C_j-H_j},
$$

where comparable scope and protected capacity are defined. Weighted policy may compare $d_i/w_i$. This is a signal unless the scheduler implements a specified allocation theorem.

For queued system with arrival rate $\lambda$, service rate $\mu$, average number $L$, and average wait $W$, Little’s Law gives $L=\lambda W$ under its steady-state conditions. When sustained demand exceeds service, no finite queue policy prevents growth without admission reduction or capacity increase.

Token bucket with refill $r$, capacity $b$, and current tokens $z(t)$ admits cost $c$ only when $z(t)\ge c$, then subtracts $c$; refill is bounded by $b$.

## Mechanisms, Invariants, or Proof Structure

### Quota design mechanism

1. Trace platform journeys and inventory every exhaustible resource and provider/system limit.
2. Define unit, scope, authority, capacity, reserve, request, limit, quota, guarantee, burst, and cost semantics.
3. Model failure/rollout/recovery capacity and topology fragmentation.
4. Allocate feasible ancestor/child guarantees and ceilings across the full resource vector.
5. Implement atomic admission or compensating reservation with stable request identity.
6. Enforce instance limits, aggregate quotas, rates, concurrency, object counts, and provider ceilings at their authorities.
7. Protect critical classes, then enforce fairness and bounded queues within classes.
8. Propagate backpressure and machine-readable denial without retry amplification.
9. Observe allocation, use, pending demand, saturation, rejection, fairness, cost, and leaks.
10. Reconcile leases, objects, provider effects, delete, and restored ledgers before releasing capacity.
11. Change quotas through versioned, approved, expiring policy with compatibility for live allocations.
12. Stress correlated bottlenecks, failures, failover, reclamation, and recovery.

### Feasibility invariant

No admission causes a hard resource, ancestor allocation, protected reserve, or provider ceiling to exceed its versioned bound. Multi-resource acquisition either commits coherently or releases partial reservations.

### Honesty invariant

The product distinguishes ceiling, guarantee, availability, and observed use. It never promises runnable capacity solely from unused quota.

### Fair-progress invariant

Within an admitted contention class, one flow/tenant cannot indefinitely prevent others with eligible work from progress, except where an explicitly higher-priority guarantee consumes all relevant capacity under policy.

### Release invariant

Capacity returns only after authoritative terminal/absence evidence or a safely expired fenced lease. A request to delete or a missing dashboard entry is insufficient.

### Proof sketch: quota does not imply guaranteed capacity

Suppose tenants $a$ and $b$ each have CPU quota 80 on a cluster with 100 allocatable CPU and no reservations. Tenant $b$ currently uses 80. Tenant $a$ uses zero, so its dashboard shows 80 unused quota.

If $a$ requests 80, quota admission alone permits the request within $q_a$, but only 20 physical CPU remains. Without preemption/reservation/capacity expansion, $a$ cannot run the full allocation. Thus unused quota does not imply available or guaranteed capacity. A guarantee requires capacity/scheduling policy that protects it under stated conditions. This proof sketch ignores topology and other resources; adding them creates more possible binding constraints, not fewer.

### Executable multidimensional audit

This synthetic audit classifies nine requests against CPU, memory, connection, rate, concurrency, and lifecycle bounds. It verifies deterministic local arithmetic only; it does not prove scheduling, fairness, provider capacity, or SLOs.

<!-- bijux-verify: {"id":"quota-vector-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"admitted=4\ncpu=1\nmemory=1\nconnections=1\nrate=1\nconcurrency=1\n"}} -->
```python
requests = [
    (20, 40, 10, 20, 2),
    (30, 50, 20, 30, 3),
    (10, 20, 5, 10, 1),
    (40, 60, 30, 40, 4),
    (101, 40, 10, 20, 2),
    (20, 201, 10, 20, 2),
    (20, 40, 51, 20, 2),
    (20, 40, 10, 101, 2),
    (20, 40, 10, 20, 11),
]
limits = (100, 200, 50, 100, 10)
names = ("cpu", "memory", "connections", "rate", "concurrency")
counts = {"admitted": 0, **{name: 0 for name in names}}

for request in requests:
    violations = [name for name, value, limit in zip(names, request, limits) if value > limit]
    if violations:
        counts[violations[0]] += 1
    else:
        counts["admitted"] += 1

for name, count in counts.items():
    print(f"{name}={count}")
```

### Verification strategy

Recompute capacity envelopes and hierarchy sums from authoritative inventory. Validate units, resource scopes, provider ceilings, topology, reserves, guarantees, and quota snapshots.

Generate requests at zero, exact boundary, one unit over, multi-resource conflict, ancestor exhaustion, stale quota revision, duplicate, concurrent, partial failure, and rollback.

Stress one tenant, many tenants, hot flows, long operations, retries, high-priority floods, queue expiry, lease crash, provider throttling, control-plane saturation, and cleanup failure.

Exercise zone loss, rollout, failover, restore, borrowing/reclamation, quota reduction, temporary increase expiry, and release reconciliation while measuring SLO and fairness.

## Alternatives and Trade-Offs

- **Hard partition versus elastic sharing.** Partitioning gives predictability but strands capacity; sharing improves use but requires fairness and reclamation.
- **Quota versus reservation.** Quota caps demand; reservation protects supply. Many products need both.
- **Requests-based versus usage-based admission.** Requests are predictable and schedulable; measured use is dynamic and may reward under-declaration.
- **CPU limits versus aggregate control.** Per-container limits contain bursts but can throttle latency; aggregate quota/fairness may use spare CPU more efficiently.
- **Static defaults versus rightsizing.** Defaults simplify onboarding; adaptive recommendations better match behavior but need evidence and rollback.
- **Namespace quota versus cluster/account quota.** Namespace scope supports tenant delegation; higher scopes protect shared/provider ceilings. They must compose.
- **Rate limit versus concurrency limit.** Rate controls arrivals; concurrency controls long-held work. Use both when duration varies.
- **Reject versus queue.** Rejection preserves latency/capacity; bounded queues smooth bursts but add stale intent and operational state.
- **FIFO versus fair queue.** FIFO is simple but a large tenant blocks others; fair scheduling costs state and may relax arrival order.
- **Strict priority versus weighted fairness.** Priority protects critical work; weights avoid starvation and express differentiated service.
- **Central ledger versus local enforcement.** Centralization coordinates hierarchy; local controls are fast/resilient. Versioned delegated allocations can combine them.
- **Persistent allocation versus leases.** Persistent state suits durable resources; leases reclaim crashed-operation capacity but need fencing and renewal.
- **Provider quota increase versus new account/cell.** Increase is operationally simple; new boundaries isolate quotas/blast radius but add fleet cost.
- **Burst borrowing versus no borrowing.** Borrowing improves utilization; borrowers must tolerate reclamation and unpredictability.
- **Tenant metrics versus cohort metrics.** Tenant detail aids support; cohort aggregation controls privacy/cardinality. Secure drill-down combines them.
- **Automated reduction versus owner migration.** Automation corrects waste quickly; owner-guided change protects sparse peaks and stateful SLOs.

## Failure Modes and Misconceptions

- “Quota reserves capacity” confuses ceiling with guarantee.
- “Unused quota is available” ignores physical capacity, topology, and ancestors.
- “Limit is the expected need” confuses ceiling with request.
- “Average usage is the right request” ignores peaks and failure behavior.
- “Memory overcommit behaves like CPU” ignores termination and reclaimability.
- “ResourceQuota covers the cluster” ignores other namespaces and provider layers.
- “CPU and memory are sufficient” misses control-plane, data, network, and external resources.
- “Object counts are harmless” ignores etcd/controllers/provider effects.
- “Cloud quota is platform fairness” ignores tenants sharing an account.
- “Separate accounts remove all ceilings” ignores regional/organization/provider limits.
- “A budget blocks spend” may be only delayed alerting.
- “FIFO is fair” lets large flows monopolize wait.
- “Priority guarantees progress” can starve lower classes or wait on lower work.
- “Queueing fixes overload” cannot beat sustained arrival above service.
- “429 should be retried immediately” creates synchronized overload.
- “Rate limits constrain long operations” ignores concurrency duration.
- “Expired lease means effect absent” ignores stale owner/provider commit.
- “Borrowed capacity belongs to borrower” defeats reclamation.
- “More quota solves every denial” can move failure to provider or placement.
- “Autoscaling creates instant capacity” ignores delay, quota, topology, and cost.
- “Usage dashboards drive enforcement” may be stale or aggregated.
- “Deleting an object releases capacity” ignores finalizers and external resources.
- “Low utilization means excess supply” may reflect denial or stranded fragments.
- “Equal quantities are fair” ignores different resource vectors and weights.
- “System work can use ordinary quota” risks losing recovery under overload.
- “No rejection means quota works” may mean requests wait or fail elsewhere.

## Worked Examples

### Example 1

A namespace has quota 100 CPU requests and 200 CPU limits. It currently requests 80 and uses 30. A new 30-CPU request is denied even though current use would fit, because scheduling/admission protects declared allocations rather than predicting simultaneous use.

The team rightsizes existing inflated requests from evidence instead of bypassing quota. A temporary increase has expiry and cluster-capacity validation.

### Example 2

Two tenants each show 80 unused CPU quota in a 100-CPU cluster. One submits first and consumes 80; the other cannot place. The portal relabels quota as ceiling, adds guaranteed capacity for premium tier, and shows cluster/headroom constraints.

The sum of protected guarantees stays within failure-adjusted capacity, while unguaranteed quota may intentionally exceed it.

### Example 3

A controller remains under pod CPU/memory quota but creates 500,000 ConfigMaps and saturates etcd/watchers. Object-count quota, controller rate limit, TTL cleanup, and API Priority/Fairness isolate it.

Critical leader election and node health retain capacity. The controller backs off on rejection rather than multiplying list/watch requests.

### Example 4

Environment creation averages one request per second but takes ten minutes. A rate limit of 10/s permits 6,000 concurrent provider operations and exhausts the account. Platform adds per-tenant and per-provider concurrency leases of 20 and 100, respectively.

Queued requests have deadlines/cancellation. Ambiguous expired leases reconcile provider operation identity before reuse.

### Example 5

A memory-heavy tenant and GPU-heavy tenant receive equal CPU shares but contend differently. Scheduler considers their multi-resource vectors and weighted dominant shares within their service class.

GPU jobs are indivisible and topology-bound, so the platform documents that the metric guides fairness rather than promising an ideal divisible-resource allocation.

### Example 6

During zone loss, workload quotas fit normal capacity but not remaining nodes. Recovery pods compete with batch replay. Reserved failure headroom and critical priority protect control/recovery; replay borrows only revocable capacity.

Placement accounts for per-zone fragmentation. The test verifies ordinary work is throttled and status/cancel/delete remain available.

### Example 7

A tenant receives a 30-day database-connection increase. The change validates database capacity and ancestor totals, records owner/reason/cost, and expires automatically. Before expiry the portal warns and proposes rightsize or extension.

If current allocation exceeds the restored quota, new admission stops; live connections are not killed absent an explicit reclamation contract.

### Example 8

Budget crosses 100% because egress billing arrives six hours late. The platform alerts and blocks new optional bulk exports under policy but does not delete production databases.

Real-time egress rate controls use network measurements, while billing remains financial authority. Both timestamps and uncertainty are visible.

### Example 9

A failed load-balancer deletion disappears from Kubernetes but persists at provider and consumes regional quota. Reconciliation keeps it charged to the operation/tenant until provider absence is confirmed, then retries cleanup idempotently.

Increasing regional quota would hide the leak. Orphan age/count and cleanup SLO are first-class signals.

### Example 10

After restoring quota ledger from backup, current provider resources exceed recorded allocation. Admission remains fenced while inventory reconstructs resources, leases, tenant ownership, and external operations.

The platform prefers temporary denial to double allocation. Reconciliation publishes the new versioned snapshot before reopening admission.

## Cross-Program Connections

- **Operating Systems:** CPU scheduling, memory pressure, cgroups, IO, process limits, and priority explain resource-specific enforcement.
- **Algorithms and Optimization:** bin packing, max-min/weighted fairness, dominant shares, fragmentation, and online admission shape allocation.
- **Distributed Systems:** leases, fencing, counters, stale state, queues, idempotency, and reconciliation protect quota authorities.
- **Kubernetes Engineering:** requests/limits, QoS, ResourceQuota, LimitRange, scheduling, eviction, priority, and API fairness implement several layers.
- **Cloud Engineering:** regional/account service quotas, organization ceilings, autoscaling, instance supply, IPs, APIs, and support lead times constrain capacity.
- **Database Engineering:** connections, locks, IOPS, transactions, storage, replication, and backup impose bottlenecks outside compute quota.
- **Reliability Engineering:** headroom, overload control, failure reserves, graceful degradation, SLO correlation, and recovery define safe capacity.
- **API and Service Engineering:** rate/concurrency limits, 429 semantics, idempotency, backoff, and admission errors form consumer-facing contracts.
- **FinOps:** requests, reservations, actual use, provider charges, budgets, showback, and incentives connect allocation with economics.
- **Product Management:** tiers, guarantees, burst, increase workflow, denial explanations, and unmet-demand signals make quota a usable product.

## References

1. Kubernetes. [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/). Retrieved 2026-09-02.
2. Kubernetes. [Limit Ranges](https://kubernetes.io/docs/concepts/policy/limit-range/). Retrieved 2026-09-02.
3. Kubernetes. [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/). Retrieved 2026-09-02.
4. Kubernetes. [Pod Quality of Service Classes](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/). Retrieved 2026-09-02.
5. Kubernetes. [API Priority and Fairness](https://kubernetes.io/docs/concepts/cluster-administration/flow-control/). Retrieved 2026-09-02.
6. Kubernetes. [Pod Priority and Preemption](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/). Retrieved 2026-09-02.
7. AWS. [Service Quotas User Guide](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html). Retrieved 2026-09-02.
8. Google Cloud. [Cloud Quotas Overview](https://cloud.google.com/docs/quotas/overview). Retrieved 2026-09-02.
9. Microsoft Azure. [Azure Subscription and Service Limits, Quotas, and Constraints](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits). Retrieved 2026-09-02.
10. IETF. [RFC 9333: RateLimit Fields for HTTP](https://datatracker.ietf.org/doc/html/rfc9333). November 2023. Retrieved 2026-09-02.
11. Ghodsi, Ali, et al. [Dominant Resource Fairness: Fair Allocation of Multiple Resource Types](https://www.usenix.org/conference/nsdi11/dominant-resource-fairness-fair-allocation-multiple-resource-types). NSDI 2011.
12. Little, John D. C. [A Proof for the Queuing Formula: L = λW](https://pubsonline.informs.org/doi/10.1287/opre.9.3.383). Operations Research 9(3), 1961.
13. Briscoe, Neil. [Understanding the Token Bucket Algorithm](https://www.redbooks.ibm.com/redpapers/pdfs/redp4285.pdf). IBM Redpaper, 2006.
14. FinOps Foundation. [FinOps Framework: Usage and Cost Allocation](https://www.finops.org/framework/capabilities/allocation/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Inventory quotas for a platform that vends Kubernetes workloads, databases, cloud accounts, builds, and event subscriptions. Include allocation, rate, concurrency, object, data, provider, and human bottlenecks.

### Exercise 2

Given 1,000 CPU, 4 TiB memory, and 2,000 database connections, design headroom, guarantees, hard quotas, burst, and hierarchy for four tenant tiers. Explain feasibility and false-guarantee risks.

### Exercise 3

Design overload control for environment vending with interactive requests, bulk migrations, provider rate/concurrency limits, workflow queues, retry, cancellation, and disaster recovery.

### Exercise 4

Audit a Kubernetes cluster where namespaces pass ResourceQuota checks but teams report Pending pods, CPU throttling, OOM termination, API 429s, PVC failures, and missing load balancers.

### Exercise 5

Design quota recovery after a database restore loses allocation records while Kubernetes, cloud providers, workflow leases, and billing show conflicting states.

## Answers to the Exercises

### Answer 1

Kubernetes: CPU/memory/ephemeral requests and limits; GPUs/devices; pods, Jobs, ConfigMaps, Secrets, Services, PVCs and CRs; storage class/capacity/IOPS/attachments; nodes/topology; API seats, watches, admission, controller queues; network bandwidth/connections/IPs/load balancers/NAT.

Database: instances, storage/IOPS, connections, concurrent operations, transactions/locks, backup/snapshot and provider API. Accounts: per-region allocation, create/update/delete rates, concurrent long operations, IAM/policies, IPs, API enablement, logs. Builds: runner CPU/memory/disk, concurrency, queue age, registry storage/push/pull, external API/licensing. Events: publish rate/size, partitions, storage/retention, consumer concurrency, replay and quarantine.

Also identity, secret/key operations, policy evaluations, workflow workers, catalog/search, support/approval and incident capacity. For each record unit, scope, authority, capacity/reserve, current allocation/use, enforcement, increase/refresh, release, cost, and SLO.

### Answer 2

First reserve, for example, 15% CPU/memory and 300 connections for platform, upgrades, failure, and recovery: allocatable tenant envelope is 850 CPU, 3.4 TiB, 1,700 connections under those assumptions. Protected guarantees across four tiers must sum within each dimension and topology/failure domain; e.g. 400/1.6 TiB/800 connections total guarantees leave further shared/burst capacity.

Hard quotas may sum above remaining capacity for unguaranteed burst, but UI labels them ceilings, not reservations. Each tenant has resource vector and ancestors; tier allocation cannot exceed parent. Connection and memory guarantees cannot be inferred from CPU. Stateful work may not borrow reclaimable capacity.

Validate node/zone fragmentation, database failover, provider limits, rollout surge, correlated peaks, and tenant count. Set per-tenant rate/concurrency and object limits separately. Observe stranded guarantee, denied guaranteed demand, actual use, pending demand, cost, and failures; adjust via versioned review.

### Answer 3

Use authenticated per-tenant token buckets for request rate/burst, tenant concurrent-operation caps, and provider account/region global concurrency/rate. Critical incident/recovery receives protected class; interactive requests get weighted fair progress; bulk migration uses revocable residual capacity and separate bounded queue.

Persist request and quota snapshot, acquire durable fenced leases atomically/compensating, then enqueue workflow. Queue has tenant fairness, maximum length/age, deadlines, cancellation, and admission preview. Workers honor provider 429/retry hints with jitter and retry budgets; an ambiguous provider call retains/reconciles its lease and operation ID.

Propagate saturation to API and protect status/cancel/delete. Reserve provider and worker headroom for disaster recovery; pause bulk replay during failure. Measure arrival/service, queue oldest age, admitted/running/provider-waiting, rejection, retries, lease age, fairness, and terminal outcomes. Test provider slowdown, crash, failover, and restoration.

### Answer 4

ResourceQuota passing proves only namespace admission dimensions. Inspect scheduler events and node/topology fragmentation for Pending pods; compare CPU requests/limits/use/throttling and memory working set/limits/OOM; inspect QoS/eviction. Validate LimitRange defaults and injected sidecars.

For API 429 inspect API Priority/Fairness flow/priority, seats, queue/rejection, expensive lists/watches/webhooks, latency, and controller retry. PVC failures require storage class, topology, capacity, attachment, expansion, snapshot/provider quotas. Missing load balancers require Service object quota plus provider regional account quota, IPs, API rates/concurrency, permissions, controller status, and orphan inventory.

Build the full constraint chain and return the binding dimension. Do not raise namespace CPU quota to address database connections or provider IPs. Reconcile deleted external resources and validate cluster failure/upgrade headroom.

### Answer 5

Fence new admission and quota reductions while preserving status, cancel, delete, and recovery capacity. Record restore points/versions for allocation database, Kubernetes, provider inventories, workflows/leases, and billing; none alone is complete truth.

Reconstruct allocations by stable tenant/resource/operation IDs. Query live Kubernetes objects and requests, provider resources and states, durable workflow steps/receipts, leases with fencing tokens, queues, and retained billing as corroboration. Treat ambiguous external operations as allocated until reconciled; do not reuse expired lease capacity if a stale worker/provider effect may commit.

Compare totals with ancestors, provider ceilings, reserves, and physical capacity. Quarantine orphan/mismatched resources, adopt legitimate effects or clean confirmed leaks idempotently. Publish a new immutable quota snapshot and audit differences. Reopen low-risk admission by cohort only after invariant checks; monitor duplicates, capacity, fairness, and SLO. Repair backup/restore tests and preserve incident evidence.
