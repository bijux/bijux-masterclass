---
module_id: LSDS-060
program: Large-Scale Data Systems Engineering
level: 2
module_number: 60
title: Diagnosing Scheduler Delay and Resource Fragmentation
status: complete
last_verified: 2026-09-04
---

# Diagnosing Scheduler Delay and Resource Fragmentation

## One-Page Review

### Governing question

When work starts late despite apparently available cluster capacity, how can an operator locate the actual waiting stage, reconstruct placement feasibility, distinguish resource shortage from fragmentation or scheduler saturation, and choose a remedy that preserves workload and tenant invariants?

### Essential definitions

- **scheduler delay** is time attributable to scheduler-owned queueing, feasibility, scoring, reservation, permitting, binding, or retry—not every interval before useful work begins.
- **placement feasibility** means at least one eligible node satisfies the complete resource vector and every hard constraint simultaneously.
- **resource fragmentation** is unusable free capacity caused by its distribution across nodes, resource dimensions, topology, time, or policy boundaries.
- **allocatable capacity** is node capacity available to scheduled workloads after platform reservations and overhead.
- **request** is the resource quantity used for admission and placement; utilization after placement is different evidence.
- **head-of-line blocking** occurs when an infeasible earlier workload delays feasible later work under an ordering policy.
- **scheduler throughput saturation** occurs when eligible arrivals exceed sustained completed scheduling cycles.
- **unschedulable** means no current placement passes; **unresolvable** means ordinary cluster changes are not expected to repair the declared contradiction.
- **placement snapshot** is a versioned record of workload request, constraints, node state, policy, and per-stage rejection reasons.
- **stranded capacity** is free capacity that cannot satisfy relevant pending demand under current constraints.

### Central model, mechanism, or theorem

For pending workload $j$ and node $n$, define

$$F(j,n)=R(j,n)\land T(j,n)\land A(j,n)\land V(j,n)\land P(j,n),$$

where $R$ is resource-vector fit, $T$ topology/affinity fit, $A$ taint and authorization fit, $V$ volume/device/network fit, and $P$ policy fit. Workload $j$ is currently placeable only if $\exists n:F(j,n)$. Aggregate free capacity satisfying $\sum_n f_{n,k}\ge r_{j,k}$ for every resource $k$ is necessary in some models but not sufficient: one indivisible request must fit one eligible node, and all predicates must hold on that same node. Diagnosis first reconstructs the end-to-end timeline, then evaluates queue eligibility, scheduler health, per-node feasibility, and actuation. Remedy follows the violated predicate or bottleneck rather than the dashboard's largest number.

### Critical invariants

- Timestamps identify submission, eligibility, admission, active/backoff/unschedulable queue, scheduling attempt, reservation, bind, node readiness, framework registration, and useful start separately.
- A diagnosis names the scheduler, profile, policy generation, workload generation, and cluster-state observation window.
- Resource fit uses requests against allocatable capacity with consistent units and includes system and per-node overhead.
- All hard constraints are intersected on each node; counts from separate predicates are not combined as if they referred to the same candidates.
- Pending reasons are preserved per attempt and aggregated without erasing minority or final-node blockers.
- Proposed fixes do not silently weaken isolation, topology, availability, residency, device, volume, quorum, or tenant guarantees.
- Preemption or consolidation accounts for victim recovery, shuffle/state, disruption budgets, and capacity made usable—not merely nominally freed.
- Autoscaling is recommended only when an available node class can satisfy the pending request and quota/provider capacity permit it.
- Scheduler tuning does not trade correctness or fairness for throughput without explicit validation.
- Incident mitigation, causal correction, and longer-term capacity policy are recorded as separate decisions.

### Common failures

Common failures include measuring submission-to-start and blaming it all on the scheduler; treating node utilization as placement capacity; summing free CPU and memory across nodes for an indivisible request; checking affinity, taints, volumes, and resources separately without intersecting candidate sets; ignoring init-container, pod overhead, DaemonSet, ports, or extended resources; reading only the latest truncated event; adding nodes of the wrong class; lowering requests below safe working sets; deleting topology rules that protect availability or residency; preempting victims that do not create a feasible bin; overlooking scheduler cache/API/plugin latency; and fixing cluster placement while the real wait occurs inside a framework stage or dependency queue.

### Compact example

Two nodes expose free vectors of (4 CPU, 10 GiB) and (4 CPU, 4 GiB). A pending executor requests (6 CPU, 8 GiB). Aggregate free capacity is (8 CPU, 14 GiB), enough component-wise, but neither node supplies six CPU. The request is fragmented across bins. Adding another (4,10) node still does not help; rightsizing the request, adding a node with at least (6,8) allocatable, or safely reshaping existing placements can.

### Connections

[LSDS-051](051-cluster-resource-models.md) defines vectors and fragmentation, [LSDS-053](053-fair-and-capacity-scheduling.md) separates allocation policy from placement, [LSDS-054](054-data-local-task-placement.md) defines locality and topology, [LSDS-056](056-preemption.md) evaluates displacement, [LSDS-058](058-multi-tenant-queueing.md) explains ordering and head-of-line effects, and [LSDS-059](059-autoscaling-data-clusters.md) distinguishes pending demand from effective capacity.

## Governing Question

“Pending” is not a root cause. A workload can wait before admission because its dependency is incomplete, inside a tenant queue because quota is exhausted, in a scheduler backoff queue after failed attempts, during an admission webhook, while no node satisfies a volume zone, after binding while a node boots, inside a framework awaiting executors, or inside an application stage with no runnable tasks. Only some of these intervals belong to the cluster scheduler.

Likewise, “the cluster has 200 free CPUs” does not prove that a 32-CPU executor can start. Free CPU may be spread as four cores on fifty nodes, the memory accompanying those cores may be insufficient, eligible nodes may be in the wrong zone, or a device, host port, volume, taint, queue maximum, gang, or disruption rule may exclude them. Utilization may show idle CPU even though requests have reserved it for placed workloads.

The governing question is how to reconstruct ownership of delay, reproduce the exact placement predicate at the relevant time, quantify fragmentation for actual pending demand, diagnose control-plane throughput, and select a reversible remedy whose benefit is measured as useful work rather than merely fewer pending objects.

## Why This Matters

Scheduler delay consumes deadline and recovery margin before computation begins. In batch platforms it expands makespan and misses delivery windows. In streaming systems it prolongs lag recovery. In interactive services it turns load into queueing or timeouts. During an incident, blind remediation—add nodes, relax affinity, shrink requests, or preempt something—can increase cost and disruption while leaving the blocking predicate unchanged.

Fragmentation also hides inside apparently healthy aggregate metrics. Resource requests can reserve idle-looking capacity; heterogeneous node pools strand complementary resource dimensions; topology and volumes create isolated islands; and large indivisible requests need contiguous bins. A high average utilization may coexist with good placement, while a lower average may be operationally unusable. The useful question is whether the cluster can place the demand mix it promises.

Diagnosis is therefore a causal and historical task. Current state may differ from the failed attempt: nodes arrived, pods ended, policy reloaded, or events were compacted. Durable evidence must connect queue state, scheduler attempt, state snapshot, decision reasons, actuation, and eventual start. Without that chain, teams optimize anecdotes and cannot tell whether a fix worked.

## Prerequisites and Retrieval

Review cluster resource models in [LSDS-051](051-cluster-resource-models.md), dynamic allocation in [LSDS-052](052-static-and-dynamic-allocation.md), fairness and capacity scheduling in [LSDS-053](053-fair-and-capacity-scheduling.md), locality and topology in [LSDS-054](054-data-local-task-placement.md), speculation in [LSDS-055](055-work-stealing-and-speculation.md), preemption in [LSDS-056](056-preemption.md), isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md), multi-tenant queues in [LSDS-058](058-multi-tenant-queueing.md), and autoscaling in [LSDS-059](059-autoscaling-data-clusters.md).

You should understand resource requests and limits, allocatable capacity, vectors, bin packing, affinity and anti-affinity, topology, taints, volumes, gang scheduling, priority, quotas, event time, percentiles, queues, caches, retries, and distributed reconciliation.

## Learning Objectives

After this module, you should be able to:

1. decompose submission-to-useful-start latency into owned stages;
2. distinguish scheduler queue delay, scheduling-cycle latency, binding, provisioning, startup, and framework delay;
3. reconstruct a workload's complete placement predicate from versioned evidence;
4. prove why aggregate free resources do or do not imply a feasible node;
5. classify vector, bin, topology, device, storage, temporal, and policy fragmentation;
6. diagnose scheduler throughput saturation separately from unschedulable demand;
7. quantify stranded capacity against a declared pending workload distribution;
8. choose among rightsizing, node-shape changes, reservations, preemption, autoscaling, and constraint correction;
9. preserve fairness, availability, state, and security during mitigation; and
10. validate causal fixes through replay, controlled experiments, canaries, and regression guards.

## Core Exposition

### Build the end-to-end waiting timeline

Begin with immutable workload identity and one clock model. Record submitted, dependencies-satisfied, queue-eligible, quota-admitted, scheduler-observed, active-queue, attempt-start, reserve, permit, bind-requested, bind-observed, node-ready, container-start, readiness, framework-registered, task-dispatched, and useful-work timestamps. Not every system exposes every stage; mark absent evidence rather than inventing it.

Compute adjacent intervals before aggregating. Submission-to-eligibility belongs to dependencies or admission. Eligible-to-attempt may reflect queue order or scheduler throughput. Bind-to-ready belongs to provisioning and startup. Executor-ready-to-task belongs to the framework. End-to-end latency remains important, but ownership makes it actionable.

### Identify the scheduling authority

A cluster can run multiple schedulers, profiles, queues, and framework schedulers. Confirm which scheduler name/profile owned the object and whether another controller gated it. Capture configuration generation, plugin/extension versions, feature flags, and queue policy active at the attempt time.

Do not infer authority from a current default. A workload may have named a retired scheduler, been rewritten by admission, or waited in a framework after its coordinator was scheduled. Stable workload and attempt IDs connect layers without conflating them.

### Classify queue state precisely

Schedulers commonly distinguish active work eligible for an attempt, backoff work delayed after failure, and unschedulable work waiting for a relevant cluster event. Admission systems add dependency, quota, reservation, and policy-check states. Report time and transitions in each state.

A growing active queue with short feasibility cycles suggests scheduler throughput pressure. A stable unschedulable set with repeated resource failures suggests capacity or fragmentation. Backoff growth may indicate repeated futile retries. Head-of-line blocking can strand feasible work behind an impossible gang or large request depending on queue semantics.

### Reconstruct the resource request

Use the scheduler-visible request, not an application estimate or runtime utilization. Include each regular container's concurrent request, the appropriate maximum contribution of init containers, workload overhead, extended resources, accelerators, huge pages, ephemeral storage, and host ports. Use node allocatable after system reservations and resident workload requests.

Normalize units before comparison and retain original values for audit. A request of `4000m` CPU is four cores; memory unit confusion can change feasibility. Framework executors may add overhead beyond heap. Dynamic defaults or admission mutation require the post-mutation object generation.

### Evaluate all hard predicates per node

For each node, apply readiness and schedulability, resource vector, node selector/affinity, taints/tolerations, inter-workload affinity/anti-affinity, topology spread, volume binding/zone, device/plugin availability, ports, security/residency, and scheduler-specific filters. The candidate set is the intersection.

Avoid reasoning from separate counts such as “ten nodes have memory and six have the right zone.” The sets may not overlap. Preserve a reason vector per node or equivalently show how the candidate set shrinks at each filter. Order is useful for performance diagnostics but must not change semantic feasibility.

### Distinguish unschedulable from unresolvable

A temporarily full eligible node pool may become feasible when work completes or a node is added. A contradictory selector, nonexistent resource name, impossible affinity, or request larger than every permitted node class may be unresolvable under ordinary events. Classify with explicit assumptions.

Unresolvable work should fail admission early or enter a visible remediation state rather than consuming endless scheduler cycles. Re-evaluate when relevant policy, node-class catalogs, or constraints change. Do not permanently cache the classification without generation checks.

### Understand vector and bin fragmentation

Vector fragmentation occurs when nodes have complementary free dimensions: one has CPU without memory and another memory without CPU. Bin fragmentation occurs when aggregate capacity is divided into pieces smaller than an indivisible request. Both differ from total shortage.

For demand vector $r_j$ and node free vector $f_n$, resource fit requires $r_{j,k}\le f_{n,k}$ for every $k$ on the same node. Summing over nodes is not enough unless the workload can itself split. Quantify how many pending requests each current bin could fit, not just percentages free.

### Diagnose topology and policy fragmentation

Zones, racks, fault domains, data locality, anti-affinity, topology spread, residency, dedicated pools, taints, and queue partitions divide a physical cluster into policy-specific capacity islands. Capacity free in one island is irrelevant to work forbidden from entering it. A volume bound to one zone narrows eligibility even when compute is abundant elsewhere.

Name the protection each constraint provides before changing it. Anti-affinity may preserve correlated-failure tolerance; a taint may isolate sensitive work; topology spread may enforce availability. A technically feasible relaxation can be an unacceptable reliability or governance regression.

### Account for temporal fragmentation

Short tasks ending at different times can prevent a large gang from acquiring its full vector simultaneously. The cluster has enough capacity over a window but never enough at one instant. Backfill can improve utilization yet delay the protected start if duration estimates are wrong.

Reservations, bounded backfill, gang admission, or coordinated preemption can create a simultaneous window. Measure time-to-contiguous-capacity and reservation breaches. Do not confuse temporal fragmentation with steady-state shortage.

### Read scheduling reasons as evidence, not truth alone

Events and status conditions provide valuable reason codes, but they may aggregate node failures, truncate detail, reflect only the latest attempt, or become stale after state changes. Preserve counts and representative nodes for each failure reason, plus the exact attempt time.

Correlate events with scheduler logs, metrics, traces, queue state, and an object/node snapshot. If a message says both insufficient memory and affinity mismatch, determine whether repairing one leaves the other. The causal blocker is the final intersection, not the most frequent reason string.

### Diagnose scheduler throughput saturation

When feasible work waits, compare eligible arrival rate with successful scheduling throughput. Inspect active-queue depth/age, scheduling attempts, end-to-end and extension-point latency, retries, cache freshness, API request latency, conflicts, and binding throughput. Separate tail latency from averages.

Expensive affinity evaluation, topology rules, scoring plugins, extenders, admission calls, large node counts, high pod churn, and API throttling can reduce throughput. Profile by extension point and workload class before tuning. Increasing parallelism or percentage-of-nodes-to-score trades CPU and placement quality; validate correctness and fairness under contention.

### Distinguish placement from provisioning delay

If no current node fits but an allowed node class can, node autoscaling may request capacity. Track decision, provider acceptance, instance creation, node registration, readiness, image pull, and workload bind separately. “Scheduler pending” may persist while the provisioner is doing correct but slow work.

Verify cloud quota, provider capacity, node-pool maximum, labels, taints, architecture, zones, devices, and DaemonSet/system overhead. Adding the default node shape does not help a request larger than its allocatable vector or tied to an unavailable zone.

### Diagnose framework and application delay

A coordinator may be scheduled while its executors wait, or executors may be ready while no task launches. Spark exposes jobs, stages, tasks, executor state, scheduling pools, and event logs. Compare cluster placement timestamps with framework registration, stage submission, locality wait, task dispatch, and useful input processing.

Serial stages, insufficient partitions, locality preferences, barrier/gang requirements, fair-pool settings, speculation, dependency fetches, or driver overload can look like cluster underutilization. Fix the layer that owns the queue; adding nodes cannot parallelize a serial critical path.

### Quantify fragmentation against demand

There is no single workload-independent fragmentation percentage. Define a representative demand distribution by resource vector and constraint class. For each request class, compute currently feasible nodes, maximum additional placements, stranded capacity by resource, and sensitivity to node removals or additions.

Report the fraction and age of pending demand blocked by each predicate intersection. Include large and rare requests rather than weighting only by object count. A cluster can serve thousands of small pods while permanently starving one promised large job.

### Compare requests with utilization cautiously

Placement reserves requests; runtime telemetry measures use. Large request-to-use gaps may cause apparent fragmentation, but shrinking requests blindly can create contention, eviction, throttling, or OOM. Segment by workload phase, percentiles, limits, burst behavior, and failure history.

Rightsize from representative evidence with safety margin, canary, and rollback. For memory, account for peaks and non-reclaimable state. For CPU, decide whether throttling is acceptable. If guarantees depend on requests, changing them also changes fairness and capacity accounting.

### Select a remedy by violated predicate

True aggregate shortage calls for capacity, admission control, or demand reduction. Wrong bin shapes call for a better node mix or safe rightsizing. Topology scarcity calls for compatible zones, data movement, or an approved constraint change. Temporal fragmentation calls for reservation, bounded backfill, completion, or coordinated preemption. Scheduler saturation calls for plugin/API/profile work.

Make the predicted causal chain explicit: this action changes this predicate, creating this feasible node by this time. Prefer reversible, narrow changes. Record why plausible alternatives would not satisfy the intersection.

### Use preemption and defragmentation carefully

Preemption is useful only if selected victims jointly create a feasible placement on an eligible node within the time objective. Their priority and guarantees must permit displacement, and their state, shuffle, checkpoint, and recovery costs count. Removing random low-priority work across several nodes may free much aggregate capacity but no usable bin.

Defragmentation can move workloads to consolidate free vectors. Plan migrations as a constrained placement problem with temporary capacity and disruption bounds. Prevent loops in which autoscaling adds nodes while consolidation removes them or the scheduler immediately recreates the same shape.

### Preserve fairness and tenant boundaries

Large requests are harder to place, but indefinitely favoring small easy work violates liveness. Track bypass, age, reservations, and guarantee deficits. Conversely, a single oversized tenant request should not force unlimited expansion beyond its quota or consume protected capacity from others.

Diagnose per tenant, class, size, topology, and outcome. Scheduler throughput changes can alter ordering and fairness even when total throughput improves. Test priority, queue, quota, and borrowing invariants with the remediation.

### Build an incident workflow

Freeze destructive automation if state or availability is at risk. Identify affected workloads and SLOs, establish the timeline, capture generations and a placement snapshot, classify queue state, test feasibility, then inspect scheduler/provisioner/framework health. State a falsifiable hypothesis before action.

Mitigate with the narrowest safe lever, observe the predicted transition, and revert if it does not occur. Preserve evidence before objects or events disappear. Afterward separate immediate mitigation, causal configuration or code correction, and capacity-policy follow-through.

### Validate the diagnosis and prevent recurrence

Replay the captured workload/node/policy snapshot through the same or a faithful scheduling model. Construct minimal counterexamples for resource, topology, volume, and policy failures. Load-test feasible arrivals to measure sustainable scheduler throughput and tail latency.

Canary rightsizing, node-shape, plugin, scoring, preemption, or constraint changes. Require improvement in time to useful work without regression in OOM, eviction, disruption, availability, fairness, cost, or scheduler error. Add reason-specific alerts and regression fixtures for the proven failure.

## Definitions and Notation

Let node set $N$ have allocatable vectors $c_n$, resident requested vectors $u_n$, and free vectors $f_n=c_n-u_n$. Pending workload $j$ has request vector $r_j$, hard-constraint set $C_j$, eligible-node set $E_j\subseteq N$, queue eligibility time $t_e$, scheduling-attempt time $t_a$, bind time $t_b$, ready time $t_r$, and useful-start time $t_u$.

Resource-vector fit is $R(j,n)=1$ exactly when $r_{j,k}\le f_{n,k}$ for every required resource $k$. Complete feasibility $F(j,n)$ intersects resource, topology, taint/authorization, volume/device/network, and policy predicates. Current placeability is $\max_{n\in N}F(j,n)=1$.

Aggregate component-wise sufficiency $\sum_n f_{n,k}\ge r_{j,k}$ for all $k$ does not imply placeability for indivisible work. For request class $q$, define feasible-bin count $b_q=|\{n:F(q,n)\}|$ and current placement capacity $p_q$ as the maximum count placeable under declared indivisibility and constraints. Stranded capacity is meaningful only relative to this demand class or distribution.

Decompose wait as $D_{total}=D_{pre}+D_{queue}+D_{cycle}+D_{bind}+D_{provision}+D_{startup}+D_{framework}$. Boundaries depend on the platform and may overlap if work proceeds concurrently, so record timestamps before summing. Scheduler throughput saturation occurs when sustained eligible arrival $\lambda_e$ exceeds sustained successful scheduling rate $\mu_s$ and active-queue age grows.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence:

1. Resolve immutable workload/attempt identity, scheduler/profile, tenant queue, object generation, policy generation, and clock quality.
2. Reconstruct submission, dependency, admission, scheduler queues, attempts, reserve/permit/bind, provisioning, readiness, framework, and useful-start intervals.
3. Capture the scheduler-visible request vector, allocatable node vectors, overhead, node states, and all hard constraints at the relevant attempt.
4. Evaluate every predicate per node and retain candidate-set intersections plus reason-coded rejection evidence.
5. Classify temporary shortage, vector/bin/topology/temporal/policy fragmentation, unresolvable contradiction, or scheduler/control-plane throughput saturation.
6. Correlate node-autoscaler, provider, startup, framework, storage, and dependency timelines so delay remains with its owner.
7. Quantify impact by workload/tenant/class/size and test fairness, deadline, state, availability, security, and cost invariants.
8. Select a remedy that changes the violated predicate and predict the node/capacity/state transition it should cause.
9. Canary or bound the action, observe the predicted transition through useful work, and revert or freeze on safety regression.
10. Preserve snapshot/replay evidence, correct the durable cause, add regression coverage, and update capacity policy or alerts.

For indivisible $j$, if no node individually satisfies $R(j,n)$, aggregate free capacity cannot schedule it. This follows because placement chooses one $n$ and requires every component inequality there. The argument changes for a splittable workload, whose scheduler must expose smaller placement units.

If a proposed preemption set does not produce any node satisfying all predicates after victims exit, it cannot directly resolve the placement failure. Nominal freed resources elsewhere are irrelevant. This is a necessary feasibility check, not a complete safety proof: victim completion, state recovery, and concurrent changes remain.

Growing active-queue age with feasible snapshots and sustained $\lambda_e>\mu_s$ supports a throughput-bottleneck hypothesis. It does not identify the slow extension point; traces and controlled load isolate cache, API, filter, score, permit, bind, or external components.

## Alternatives and Trade-Offs

- **Aggregate utilization dashboard:** cheap fleet overview; cannot reproduce requests, indivisible bins, or hard constraints.
- **Per-node feasibility replay:** causal placement evidence; needs versioned workload, node, and policy state.
- **Scheduler events:** immediate operator clues; may be aggregated, truncated, latest-only, or stale.
- **Scheduler traces and profiles:** identify slow extension points; increase telemetry cost and cardinality.
- **More homogeneous nodes:** simpler packing and operations; may waste workload-specific resources.
- **Heterogeneous node shapes:** match diverse demand; create capacity islands and harder autoscaling choices.
- **Smaller workload units:** pack more easily and fail narrowly; add coordination, shuffle, and overhead.
- **Larger units:** reduce orchestration overhead; increase bin fragmentation and recovery cost.
- **Strict packing:** preserves empty nodes for large work and scale-down; concentrates correlated load and hotspots.
- **Spreading:** improves fault tolerance; can strand small residual vectors across many nodes.
- **Rightsizing requests:** recovers schedulable capacity; bad estimates weaken isolation and reliability.
- **Adding nodes:** resolves genuine compatible shortage; wrong shapes or zones add cost without feasibility.
- **Reservation or bounded backfill:** creates temporal contiguity; inaccurate duration/reclaim assumptions reduce utilization or breach starts.
- **Preemption/defragmentation:** can create a feasible bin; disrupts victims and may move expensive state.
- **Relaxing constraints:** can expand candidates quickly; may violate availability, security, locality, or residency intent.
- **Scheduler throughput tuning:** reduces feasible queue delay; may change placement quality, fairness, and control-plane load.

## Failure Modes and Misconceptions

- **“Pending time equals scheduler time.”** dependencies, quota, provisioning, startup, and frameworks own other intervals.
- **“Idle CPU means schedulable CPU.”** requests, memory, topology, and other predicates govern placement.
- **“Aggregate free resources fit.”** one indivisible request needs all resources on the same eligible node.
- **“Each constraint has candidates.”** their candidate sets may have an empty intersection.
- **“The latest event is the cause.”** it may describe a different attempt or changed cluster snapshot.
- **“The most frequent reason is the blocker.”** fixing it may leave every node rejected for another reason.
- **“Utilization should replace requests.”** the scheduler needs declared reservations before future use is known.
- **“Lower requests always improve efficiency.”** it can create contention, eviction, throttling, or OOM.
- **“Any new node helps.”** shape, zone, device, labels, taints, overhead, quota, and availability must match.
- **“All unschedulable work is temporary.”** contradictory or nonexistent constraints can be unresolvable.
- **“Preempt enough total resources.”** victims must create one fully feasible placement and be safely reclaimable.
- **“Anti-affinity is waste.”** it may encode correlated-failure or security separation.
- **“Packing is always optimal.”** it can concentrate failure and thermal, network, storage, or noisy-neighbor load.
- **“A faster scheduler fixes fragmentation.”** throughput cannot make an impossible placement feasible.
- **“More capacity fixes scheduler saturation.”** extra nodes may make filtering/scoring more expensive.
- **“The coordinator running means the job runs.”** framework executors, stages, locality, or dependencies may still wait.
- **“A successful bind ends delay.”** provisioning, pull, initialization, registration, and warmup precede useful work.
- **“Removing the pending object removes the problem.”** it also destroys historical evidence and may trigger retry elsewhere.

## Worked Examples

### Example 1

A report says submission-to-start was 18 minutes. The timeline shows 10 minutes awaiting an upstream dataset, two minutes in quota admission, 20 seconds in the scheduler, four minutes provisioning a GPU node, and the remainder pulling an image. Calling this “18 minutes of scheduler delay” sends every team to the wrong subsystem.

### Example 2

A pod needs 8 GiB and zone A. Ten nodes have 16 GiB free in zone B; three zone-A nodes have only 4 GiB. Memory and zone each look available when counted separately, but their intersection is empty. A compatible zone-A node or approved volume/data movement changes feasibility.

### Example 3

The scheduler reports insufficient CPU on 80 nodes and affinity mismatch on 20. Adding CPU to the 80 does not help if all 80 also fail an omitted residency constraint. A per-node reason matrix reveals the candidate intersection; aggregate reason counts do not.

### Example 4

A request asks for one GPU model that no registered device plugin advertises because of a spelling error. It is unresolvable through normal scale-out. Admission validation rejects the unknown resource name and points to the permitted catalog instead of retrying forever.

### Example 5

A 50-task gang needs simultaneous capacity. Short jobs continuously occupy newly free slots, so total free resource-hours are ample but 50 slots never coexist. A reservation with bounded backfill protects a start window and measures any breach; random node additions merely postpone diagnosis.

### Example 6

The active queue grows while replay shows most requests fit. Traces identify a custom scoring plugin whose remote call dominates tail cycle latency. Caching safe inputs and bounding the call reduces queue age under a controlled load test; node expansion would have increased scoring work.

### Example 7

A Spark application owns 100 ready executors, but a serial stage has one runnable task. Cluster placement is complete. The framework timeline identifies stage parallelism, so the remedy is plan or partition work rather than more nodes or scheduler tuning.

### Example 8

A low-priority pod occupies 6 CPU on node X. A pending pod needs 8 CPU and a volume fixed to node X's zone. Preempting two 4-CPU pods on other zones frees more aggregate CPU but creates no candidate. Victim selection must make node X or another volume-compatible node fully feasible.

### Example 9

Requests are reduced after weeks of low average memory. A monthly aggregation phase then OOMs repeatedly, producing retries and more queue pressure. Phase-aware percentiles and canary rightsizing would have retained peak margin and exposed the rare but contractual workload phase.

### Example 10

The fixture demonstrates component-wise aggregate sufficiency without a feasible indivisible bin.

<!-- bijux-verify: {"id":"fragmented-resource-fit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"aggregate_free=(8, 14)\naggregate_fits=True\nfeasible_nodes=()\n","stderr":""}} -->
```python
nodes = {
    "node-a": (4, 10),
    "node-b": (4, 4),
}
request = (6, 8)

aggregate = tuple(sum(free[index] for free in nodes.values()) for index in range(2))
aggregate_fits = all(need <= free for need, free in zip(request, aggregate))
feasible = tuple(
    name
    for name, free in nodes.items()
    if all(need <= available for need, available in zip(request, free))
)

print(f"aggregate_free={aggregate}")
print(f"aggregate_fits={aggregate_fits}")
print(f"feasible_nodes={feasible}")
```

The tuple represents CPU and GiB only; a production feasibility test must also include every topology, taint, volume, device, port, security, and policy predicate against a versioned snapshot.

## Cross-Program Connections

- **Algorithms:** multidimensional bin packing, matching, constraint satisfaction, queueing, backfill, and victim selection frame diagnosis.
- **Distributed systems:** stale caches, event time, generation changes, retries, partial failure, idempotence, and reconciliation shape evidence.
- **Data engineering:** DAG stages, partitions, executors, shuffle, locality, gangs, checkpoints, and skew determine useful parallelism.
- **Platform engineering:** requests, schedulers, plugins, affinity, taints, topology, volumes, node autoscaling, and events implement placement.
- **Reliability engineering:** deadlines, disruption budgets, failure domains, incident evidence, canaries, freeze paths, and rollback constrain remedies.
- **Performance engineering:** throughput, queue age, extension-point latency, API saturation, profiling, and controlled load isolate bottlenecks.
- **Security and governance:** residency, tenant quota, dedicated pools, priority authority, and audit make some fragmentation intentional.
- **Economics:** node shapes, stranded capacity, preemption loss, overprovisioning, and missed deadlines determine full cost.

## References

1. Kubernetes. [Scheduling Framework.](https://kubernetes.io/docs/concepts/scheduling-eviction/scheduling-framework/) Current scheduling-cycle, binding-cycle, extension-point, queue, reserve, permit, and bind concepts.
2. Kubernetes. [Scheduler Performance Tuning.](https://kubernetes.io/docs/concepts/scheduling-eviction/scheduler-perf-tuning/) Current node-scoring thresholds, scheduling profiles, and performance-versus-feasibility trade-offs.
3. Kubernetes. [Resource Bin Packing.](https://kubernetes.io/docs/concepts/scheduling-eviction/resource-bin-packing/) Current requested-resource scoring and extended-resource packing configuration.
4. Kubernetes. [Assigning Pods to Nodes.](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/) Current node selectors, affinity, anti-affinity, field matching, and node-isolation mechanisms.
5. Kubernetes. [Taints and Tolerations.](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) Current exclusion, preference, eviction, and dedicated-node semantics.
6. Kubernetes. [Pod Topology Spread Constraints.](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) Current skew, topology domain, eligibility, and unsatisfiable-policy semantics.
7. Kubernetes. [Pod Scheduling Readiness.](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-scheduling-readiness/) Current scheduling-gate mechanism for withholding work until external conditions are satisfied.
8. Kubernetes Autoscaler. [Cluster Autoscaler FAQ.](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md) Current unschedulable-pod, node-group, scale-up, scale-down, affinity, local-storage, and disruption constraints.
9. Apache Spark. [Monitoring and Instrumentation.](https://spark.apache.org/docs/latest/monitoring.html) Current job, stage, task, executor, event-log, metric, and history evidence surfaces.
10. Apache Spark. [Job Scheduling.](https://spark.apache.org/docs/latest/job-scheduling.html) Current application/job scheduling, FIFO/fair pools, parallel jobs, dynamic allocation, and executor behavior.
11. Apache Hadoop. [CapacityScheduler.](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html) Current queue capacity, placement, node labels, reservations, ordering, locality, preemption, and application limits.
12. Verma et al. [Large-Scale Cluster Management at Google with Borg.](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) Primary production account of admission, scheduling, resource requests, constraints, availability, and utilization.
13. Schwarzkopf et al. [Omega: Flexible, Scalable Schedulers for Large Compute Clusters.](https://research.google/pubs/omega-flexible-scalable-schedulers-for-large-compute-clusters/) Primary shared-state scheduling account of parallel decisions, conflicts, incremental placement, and production workloads.

## Exercises

### Exercise 1

Nodes A, B, and C have free vectors (8 CPU, 4 GiB), (4 CPU, 16 GiB), and (6 CPU, 8 GiB). A workload requests (6 CPU, 10 GiB). Determine aggregate sufficiency and per-node resource feasibility, then explain what the result proves and omits.

### Exercise 2

Design an end-to-end timestamp and identity schema for a Spark job that passes dependency and quota admission, starts a driver, waits for executors and node provisioning, then dispatches its first useful task.

### Exercise 3

A pending stateful workload reports insufficient memory, volume-zone conflict, and anti-affinity failures. Specify how to reconstruct the candidate intersection and choose a safe remedy without weakening availability accidentally.

### Exercise 4

Design a test that distinguishes scheduler throughput saturation from widespread infeasible demand. Include workload generation, instrumentation, hypotheses, controls, and stopping conditions.

### Exercise 5

Design a fragmentation-reduction program for a multi-tenant heterogeneous cluster. Include demand classes, metrics, rightsizing, node shapes, reservations or preemption, fairness, canarying, and rollback.

## Answers to the Exercises

### Answer 1

Aggregate free capacity is (18 CPU, 28 GiB), which satisfies (6,10) component-wise. Node A fails memory, node B fails CPU, and node C fails memory, so no node provides resource-vector fit. This proves current bin fragmentation for one indivisible unit under the two modeled resources. It omits allocatable/request construction, topology, taints, volumes, devices, ports, policy, concurrent changes, and the possibility that the workload can be split into smaller placement units.

### Answer 2

Use immutable tenant, logical-job, submission, application, driver-pod, executor-pod, scheduler-attempt, node-provisioning-operation, Spark stage, and task IDs. Record source event time and collection time for submitted, dependency-ready, queue-eligible, quota-admitted, driver scheduler-observed/attempted/bound/ready, executor requested, each executor scheduler state and attempts, node scale request/provider accept/register/ready, executor bound/container-ready/framework-registered, stage-submitted, task-dispatched, and first input/output. Attach workload, admission-policy, scheduler-profile, node-template, and application generations plus reason codes. Reconcile clocks and preserve missing stages explicitly. Adjacent durations then isolate admission, scheduler queue/cycle, provisioning, startup, executor registration, and framework dispatch.

### Answer 3

Capture the post-admission workload generation, scheduler profile/policy, volume binding and allowed topology, node allocatable/request vectors, labels, taints, and resident workloads at the failed attempt. Evaluate memory, volume zone, anti-affinity, and every other filter per node; show candidate sets after each intersection and retain all reason vectors. If volume-compatible nodes lack memory, add a compatible shape, safely rightsize with peak evidence, or move/replicate data under its durability policy. If anti-affinity protects failure domains, preserve it and create a new domain or move a conflicting replica safely. Do not delete the rule merely because its reason appears often. Canary the chosen action and verify binding, readiness, state recovery, availability, and no tenant-policy regression.

### Answer 4

Generate two labeled streams: known-feasible requests sized to existing empty bins with minimal constraints, and deliberately infeasible requests spanning oversized vectors, nonexistent labels, and conflicting affinity. Measure eligible arrivals, active/backoff/unschedulable queue age, attempts, successes, scheduling and binding cycles, extension-point latency, cache/API latency, and per-node rejection reasons. Under throughput saturation, feasible active-queue age grows when arrival exceeds successful-cycle rate and improves when load or the slow extension point is reduced. Under infeasible demand, known-feasible controls remain prompt while the unschedulable set persists with stable reasons. Hold cluster state/profile constant, increase load gradually, stop on control-plane/SLO limits, and repeat with the suspected plugin disabled in a test environment.

### Answer 5

Build demand classes by CPU, memory, device, ephemeral storage, topology, volume, tenant, and indivisibility, weighted by resource-time, SLO, and rare promised large work—not object count alone. Replay each class against node snapshots to measure feasible bins, maximum placements, stranded vectors, wait, bypass, and predicate intersections. Rightsize phase-aware requests with OOM/throttle margin; compare node-shape mixes and compatible autoscaler templates; reserve or use bounded backfill for temporal gangs; use topology-aware preemption/defragmentation only when victims create feasible bins and recovery is acceptable. Enforce queue guarantees/maxima and large-work liveness. Shadow recommendations, canary one pool or class, and gate on useful-start latency, utilization, OOM, eviction, state/shuffle loss, availability, fairness, cost, and scheduler throughput. Roll back shapes, requests, scoring, and placement policy by generation while reconciling in-flight migrations.
