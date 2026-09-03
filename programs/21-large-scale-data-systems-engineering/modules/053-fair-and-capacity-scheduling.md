---
module_id: LSDS-053
program: Large-Scale Data Systems Engineering
level: 2
module_number: 53
title: Fair and Capacity Scheduling
status: complete
last_verified: 2026-09-04
---

# Fair and Capacity Scheduling

## One-Page Review

### Governing question

How should a shared data cluster divide multiple resource types among organizations, queues, users, applications, and jobs so that capacity commitments are credible, spare resources remain useful, starvation is bounded, and placement stays efficient?

### Essential definitions

- **fairness subject** is the identity whose share is governed: tenant, queue, user, project, application, or job.
- **max-min fairness** increases smaller allocations until a demand or capacity constraint binds before increasing larger ones.
- **weighted fairness** assigns different entitlement rates; comparison uses allocation divided by weight.
- A workload's **dominant share** is its largest fraction of cluster capacity across modeled resource dimensions.
- **Dominant Resource Fairness (DRF)** applies max-min reasoning to dominant shares for multi-resource demands under its model.
- A **capacity queue** has configured guaranteed/entitled capacity and often a maximum; idle capacity may be borrowed by other queues.
- **hierarchical scheduling** distributes capacity/fairness among parent queues and recursively among children.
- **work conservation** means eligible demand can use otherwise idle capacity, even beyond its steady entitlement.
- **preemption** reclaims running allocations to restore priority, minimum share, reservation, or capacity policy.
- **temporal fairness** evaluates service over a declared interval, not only one instantaneous allocation.
- **headroom** is additional capacity a subject may receive under current demand, limits, placement, and policy.

### Central model, mechanism, or theorem

For total resource capacity $R_d$ and subject $i$ holding allocation $x_{i,d}$, define dominant share

$$s_i=\max_d\frac{x_{i,d}}{R_d}$$

and weighted dominant share $s_i/w_i$ for positive weight $w_i$. A simplified DRF allocator repeatedly gives a feasible demand bundle to the eligible subject with the smallest weighted dominant share. A hierarchical capacity scheduler first derives each active queue's entitlement within its parent, allows bounded borrowing of unused capacity, and later restores an under-served entitlement through natural completion or preemption. This arithmetic does not solve node placement, indivisible resources, locality, rigid gangs, priorities, strategic requests, or time; those remain explicit scheduling constraints.

### Critical invariants

- The fairness subject, resource basis, accounting boundary, weight, demand, and evaluation interval are explicit.
- Queue capacities reconcile within each parent and preserve configured minimum/maximum rules under cluster-size changes.
- Idle capacity is work-conservingly borrowable only with defined reclaimability and no false guarantee to the borrower.
- Requests/allocations are charged once to the authenticated subject and all relevant parent queues.
- Multi-resource comparisons use canonical allocatable capacity and valid demand vectors; task count is not substituted.
- No subject exceeds its demand, hard maximum, user limit, or authorized resource class.
- Starvation protection, priority, deadlines, reservations, and preemption precedence are explicit rather than hidden in “fair.”
- Placement/locality waits are bounded so a queue cannot reserve its turn forever or lose entitlement indefinitely.
- Preemption names victims, grace, state/retry cost, expected freed resources, and a feasible beneficiary placement.
- Evidence reports both allocations and user-visible outcomes across tenants, including small/interactive and long/batch work.

### Common failures

Common failures include saying “fair” without naming the subject or interval; equalizing task counts across unequal shapes; using memory-only shares in a CPU-and-memory cluster; treating configured capacity as physically reserved; lending capacity without a reclaim path; applying queue percentages independently rather than hierarchically; letting one user consume an entire departmental queue; preempting victims that do not make the beneficiary fit; ignoring locality and gang constraints; letting tiny tasks game allocation counts; accepting inflated requests as truthful demand; judging only instantaneous shares; and reporting utilization while queue delay, starvation, churn, or victim cost deteriorates.

### Compact example

A 12-CPU/12-GiB cluster serves A tasks shaped `(3 CPU, 1 GiB)` and B tasks shaped `(1 CPU, 3 GiB)`. Alternately assigning the feasible task of the subject with the smaller dominant share yields A, B, A, B, A, B. Final allocations are A `(9,3)` and B `(3,9)`; both dominant shares are $9/12=0.75$, and all capacity is used. Equal task counts happen here because the shapes are complementary, not because task equality defines fairness.

### Connections

[LSDS-051](051-cluster-resource-models.md) defines capacity/demand vectors, and [LSDS-052](052-static-and-dynamic-allocation.md) defines changing grants. [LSDS-004](004-data-locality.md) creates locality/fairness tension. [LSDS-054](../ROADMAP.md) deepens placement, while [LSDS-056](../ROADMAP.md) deepens preemption mechanics.

## Governing Question

A shared cluster must translate organizational agreements into repeated placement decisions. Finance may own 30 percent, research 20 percent, production a protected minimum, and a common pool the rest. Within each group, many users and jobs compete. When research is idle, leaving its share empty wastes capacity; when it returns, reclaiming borrowed resources disrupts someone else.

“Fair” is not one policy. Equal CPU, equal memory, equal dominant share, equal slowdown, equal progress, equal cost, and equal service over a day produce different allocations. Capacity scheduling begins with explicit organizational entitlements; fair scheduling often begins with equal or weighted sharing among active demand. Production schedulers combine them hierarchically.

The governing question is how to specify the subject and entitlement, account for multiple resources and time, lend slack without converting it into a promise, protect small or important work, preserve placement/locality, and measure whether the resulting outcomes match the policy.

## Why This Matters

FIFO can make a short diagnostic wait behind a day-long batch job. Pure strict priority can starve low classes. Equal task counts favor tasks with larger resource vectors. Equal CPU ignores memory; equal memory ignores CPU. A correct resource model is necessary before fair division has meaning.

Capacity commitments allow organizations to consolidate clusters without surrendering predictable access. Work conservation allows inactive capacity to accelerate others. These goals conflict at reclaim time. If preemption is disabled, an entitlement is restored only as tasks finish. If tasks last hours, “guaranteed 30 percent” may be operationally false for hours.

Fairness also interacts with efficiency. Waiting briefly for a local slot can improve throughput and leave everyone better off; waiting without a bound can deny service. Packing complementary shapes raises utilization, but placement constraints can keep a mathematically fair allocation infeasible. Rigid jobs may need reservation/gang scheduling rather than incremental shares.

Finally, scheduler policy is a security boundary. Users can select queues, priorities, names, requests, and task granularity unless admission prevents it. Identity, authorization, quota, request validation, and auditable policy changes are essential to fairness.

## Prerequisites and Retrieval

Review data locality in [LSDS-004](004-data-locality.md), stages/tasks in [LSDS-006](006-stages-tasks-and-dependencies.md), stage scheduling in [LSDS-026](026-stage-scheduling.md), task retry in [LSDS-027](027-task-retry-and-speculation.md), skew in [LSDS-039](039-skewed-keys-and-heavy-hitters.md), cluster resource models in [LSDS-051](051-cluster-resource-models.md), and static/dynamic allocation in [LSDS-052](052-static-and-dynamic-allocation.md).

You should understand resource vectors, max-min allocation, weights, hierarchies, quotas, priorities, placement, locality, preemption, queues, percentiles, and basic mechanism-design caveats.

## Learning Objectives

After this module, you should be able to:

1. define fairness subject, resource basis, entitlement, demand, weight, and time interval;
2. compute single-resource max-min, weighted, and dominant-resource shares;
3. distinguish fair shares, capacity guarantees, maxima, quotas, reservations, and actual allocations;
4. design hierarchical queues whose child policies reconcile with parent capacity;
5. lend unused capacity work-conservingly while preserving a credible reclaim path;
6. bound starvation and integrate priority, aging, deadlines, and small-job protection;
7. account for placement, locality, indivisible tasks, gangs, heterogeneity, and fragmentation;
8. design preemption that frees a feasible resource vector at acceptable victim cost;
9. resist identity, queue, priority, request, and task-splitting abuse; and
10. validate allocation and outcome fairness with traces, adversarial mixtures, and policy invariants.

## Core Exposition

### Name the fairness contract

Write a precise sentence: “Among active projects in parent queue analytics, allocate CPU and memory by weighted dominant share over five-minute windows, subject to minimum capacity, maximum, priority, and placement.” This identifies who, what, and when.

Do not infer moral or social fairness from a resource algorithm. Scheduler fairness is a technical policy chosen by accountable owners. Different services may justifiably have different weights, guarantees, deadlines, or preemption protection.

### Separate guarantees and observations

Configured capacity is an entitlement rule, not necessarily dedicated hardware. Guaranteed minimum, maximum capacity, fair share, instantaneous allocation, actual usage, and completed work are separate. A queue with no demand consumes zero even if its configured capacity is 30 percent.

A guarantee needs an activation condition and restoration time. If resources are lent, state whether completion, cooperative drain, or forced preemption restores them. Without a bound, the guarantee is merely an eventual preference.

### Begin with single-resource max-min fairness

Max-min allocation raises all unsatisfied subjects equally until one reaches demand or capacity exhausts, then redistributes remaining capacity among those still demanding. Weighted max-min raises normalized allocation $x_i/w_i$ equally.

For capacity 12 and demands 2, 5, and 20, equal max-min gives 2 to the first, then divides remaining 10 equally: 5 and 5. It never allocates above demand. This water-filling intuition becomes more complex with multiple resources and indivisible tasks.

### Use dominant shares for multiple resources

DRF compares a subject by its largest share of any total resource. A CPU-heavy user and memory-heavy user can receive complementary bundles while their dominant shares converge. Weighted DRF compares $s_i/w_i$.

The model assumes known demand vectors and commonly divisible resource reasoning. Production tasks arrive as indivisible bundles placed on heterogeneous nodes. Implementations approximate the ideal through successive feasible assignments, so placement order and fragmentation matter.

### Define the capacity hierarchy

Represent organization policy as a rooted queue tree. A parent owns a share or entitlement within its parent; children divide that parent allocation by configured capacities or weights. Absolute capacity changes as cluster resources or accessible partitions change.

Validate children according to the platform's mode: configured capacities/weights, minima, and maxima must be coherent. Charge each allocation to its leaf and ancestors. A child cannot borrow around its parent's maximum, and unused descendants should not make accounting disappear.

### Distinguish steady and instantaneous share

Steady share describes expected entitlement considering configured peers. Instantaneous share depends on which queues are active and their current demand. When only A is active in a work-conserving cluster, A may use nearly all capacity; when B arrives, shares change.

Dashboards should show both. Borrowers need to know excess capacity is reclaimable. Owners need to know when their steady entitlement will become available after demand returns.

### Borrow slack work-conservingly

If a queue is below demand or inactive, lend its unused entitlement within authorized maxima. Choose how excess flows: among siblings by weight/fairness, upward to ancestors, or within resource partitions/labels. Avoid permanent idle islands.

Borrowed capacity is not a new guarantee. Track borrowed amount and victim/reclaim candidates. Long non-preemptible tasks can convert lending into de facto ownership, so admission may restrict their duration or require reservations.

### Bound starvation

Max-min sharing gives active subjects service under its assumptions, but placement and policy can still starve. Strict priority, FIFO within a saturated queue, large gangs, rare locality, max-running-app limits, and infeasible shapes require explicit handling.

Use minimum shares, aging, service deficits, reservation, deadline policy, or bounded locality delay as appropriate. State what can still starve—for example infeasible work, work above maximum, or low priority during sustained emergency—and make it observable.

### Protect small and interactive work

Equal shares can reduce short-job delay compared with FIFO, but thousands of tiny jobs can create scheduler/control overhead or game per-application fairness. Limit active applications per user/queue, aggregate identity correctly, and use admission.

If optimizing slowdown or deadlines, model it explicitly. Size-based policies require estimates and can be manipulated. Reserve a bounded interactive pool or use aging so long jobs retain progress.

### Include temporal service

Instantaneous equality can be misleading. A user that consumed the entire cluster overnight may appear equal to a newcomer at noon. Decide whether history matters: rolling allocation share, dominant resource-seconds, attained service, cost, or deficit against entitlement.

Choose window length from contract and workload duration. Short windows react quickly but churn; long windows forgive current starvation too slowly. Preserve audit across scheduler restarts and define decay/reset.

### Handle demand and request truthfulness

Demand is runnable feasible work capped by policy, not every submitted item. Inflated resource requests can increase reservation or distort dominant share; underrequests cause interference. DRF's strategy properties hold under its formal model, not every production extension.

Validate request ranges, derive recommendations from use/outcomes, charge reserved resources, and enforce tenant limits. Do not blindly schedule from actual usage: guarantees must remain available for legitimate bursts.

### Account for locality

The next fair subject may lack a local task for the free node. Scheduling a remote task preserves instantaneous share but increases network cost; waiting briefly lets another subject use the node and may improve throughput. Delay scheduling makes this trade explicit.

Bound skips by time/opportunities and relax locality levels progressively. Charge service based on actual allocation, not turns offered. Do not let impossible locality hold the queue head indefinitely.

### Account for placement and fragmentation

An ideal fair vector may not map to nodes. Track per-node fit, topology, devices, volumes, affinity, and residual shapes. A queue can be under its fair share but unable to place its pending task; giving it abstract entitlement does not create a feasible node.

Choose whether to reserve capacity for a large shape, backfill smaller work, migrate/preempt to defragment, or reject infeasible demand. Make reservation bounded so one impossible job does not idle the cluster.

### Handle rigid and gang workloads

Incremental fair assignment may give a rigid job some resources that cannot make progress while blocking others. Gang scheduling reserves/allocates the full group atomically, or waits. This can reduce work conservation.

Use admission and bounded reservations based on feasibility and priority. Account reserved-but-not-running capacity to the responsible subject. Backfill only work guaranteed to finish or be preemptible before the reservation.

### Integrate priorities carefully

Priority may order work within a queue, alter weights, define protected classes, or permit preemption. These semantics are not interchangeable. Unbounded strict priority can starve ordinary work.

Authorize priority classes, constrain their quota, and define tie-breaking/aging. Emergency priority needs incident/audit ownership. Do not let every user declare the highest value.

### Preempt to restore policy

Natural completion is cheapest but may be too slow. Preemption can restore minimum share, capacity, reservation, or priority. Select victims whose removal makes a specific beneficiary placement feasible; minimizing victim priority alone may free the wrong shape/node.

Account grace time, checkpoint/state/shuffle loss, retry, external effects, disruption budgets, and cascade. Prevent repeated preemption of the same subject and oscillation around a threshold. Verify the beneficiary still needs and can use the freed capacity before killing.

### Apply user and application limits

A departmental queue guarantee should not let one user monopolize it whenever colleagues become active. Per-user maximum/limit factor and maximum active applications bound concentration and scheduler overhead.

Identity aggregation matters across service accounts, groups, nested queues, and federated clusters. Prevent account splitting from multiplying entitlement. Exceptions require explicit ownership and expiry.

### Treat labels and partitions as separate capacity pools

GPU nodes, regulated data zones, regions, or reserved hardware may form resource partitions. A queue's percentage of the whole cluster does not imply access to every partition. Define entitlement and maximum per accessible partition/resource type.

When topology changes or nodes fail, absolute guarantees shrink. Expose the capacity basis and degraded mode. Avoid counting inaccessible capacity in fair-share denominators.

### Measure fairness and efficiency together

Report entitlement, demand, allocation, usage, dominant share, weighted share, deficit/surplus, borrowed amount, pending age, starvation episodes, preemption, and restoration time per subject and resource. Include hierarchy and partition.

Jain's index $J=(\sum x_i)^2/(n\sum x_i^2)$ summarizes equality for chosen $x_i$, but it cannot decide who deserves what or incorporate unmet demand automatically. Compute it on normalized service only when its interpretation matches policy.

Connect shares to queue delay, completion/slowdown, deadlines, streaming freshness, throughput, locality, fragmentation, utilization, failures, and cost. A perfectly equal but idle allocation is not efficient; a fully utilized cluster can be severely unfair.

### Secure and govern policy

Authenticate subjects and authorize queue, priority, resource type, reservation, and move operations. Version queue configuration, weights, minima, maxima, placement rules, and preemption settings. Validate changes before atomic activation and preserve rollback.

Audit submissions, identity mapping, policy evaluations, administrative moves, preemptions, overrides, and configuration authors. Avoid exposing other tenants' sensitive workload names or usage details while providing enough transparency to explain decisions.

### Validate with adversarial mixtures

Replay traces preserving arrival, duration, resource shape, hierarchy, locality, and failures. Test one/no/all active queues, demand below/above entitlement, complementary/conflicting shapes, small/large jobs, gangs, rare devices, hot keys, and long tasks.

Inject queue return after borrowing, preemption delay/failure, stale configuration, scheduler failover, node loss, capacity shrink, identity abuse, inflated requests, account splitting, and priority abuse. Compare against FIFO/static partitions and require both policy invariant and outcome evidence.

## Definitions and Notation

Let resources be $d\in D$ with allocatable totals $R_d$. Subject $i$ has demand vector $a_i$, allocation $x_i$, positive weight $w_i$, minimum/entitlement $g_i$, and maximum $M_i$. Its dominant share is $s_i=\max_d(x_{i,d}/R_d)$ and weighted dominant share $s_i/w_i$.

For a single normalized service quantity $z_i$, weighted max-min compares $z_i/w_i$. Jain's equality index is $J=(\sum_i z_i)^2/(n\sum_i z_i^2)$ for $n$ subjects, with $z_i$ chosen consistently. It does not encode weights unless inputs are normalized and does not prove demand satisfaction.

Let temporal service over window $[t_0,t_1]$ be $X_{i,d}=\int_{t_0}^{t_1}x_{i,d}(t)dt$. An entitlement deficit can compare actual resource-time with a declared target, but placement and useful work require additional evidence.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. Name fairness subjects, identity mapping, hierarchy, resources, weights, demand, and time interval.
2. Define minimum/guarantee, fair share, maximum, quota, reservation, priority, allocation, usage, and outcome separately.
3. Reconcile child policies within every parent and capacity partition.
4. Compute single/multi-resource ideal shares without exceeding demand or maxima.
5. Convert ideal shares into feasible node/device/topology placements and account fragmentation/locality/gangs.
6. Define work-conserving borrowing, borrower accounting, activation, and bounded reclaim/restoration.
7. Bound starvation using minima, aging/deficit, reservation, admission, or deadline rules.
8. Define preemption trigger, feasible beneficiary, victim cost/protection, grace, fencing, and retry.
9. Secure queue/priority/identity/configuration surfaces and resist request/task/account manipulation.
10. Validate instantaneous and temporal allocation plus end-to-end outcomes under adversarial multi-tenant traces.

In the simplified divisible DRF model, progressive allocation to the smallest dominant share equalizes subjects until demand or a resource binds and is work-conserving when a feasible demanded bundle remains. Adding weights normalizes comparison. This result does not automatically survive indivisible placement, heterogeneous servers, arbitrary constraints, time-varying demand, strategic task shaping, or priorities; implementations must evaluate those extensions directly.

## Alternatives and Trade-Offs

- **FIFO** is simple and predictable by arrival order, but long head jobs delay short or interactive work.
- **Static capacity partitions** make ownership clear, but waste inactive capacity and fragment shared data/resources.
- **Work-conserving capacity queues** preserve organizational entitlements while lending slack, but need reclaim/preemption semantics.
- **Single-resource fair sharing** is inexpensive, but misrepresents heterogeneous CPU/memory/device demand.
- **DRF** gives principled multi-resource comparison under its model, but does not solve placement, locality, time, gangs, or priorities.
- **Weighted sharing** represents unequal entitlement, but weights require governance and clear normalization.
- **Strict priority** protects urgent work, but can starve lower classes and invites privilege abuse.
- **Aging/deficit service** bounds starvation, but carries history and may conflict with current urgency.
- **Delay scheduling** improves locality/throughput with bounded waiting, but temporarily deviates from instantaneous order.
- **Preemption** restores policy faster, but destroys work/state and can cause cascades or oscillation.
- **Reservations/gang scheduling** enable rigid jobs, but reduce work conservation and risk head-of-line blocking.
- **Usage-based charging** reflects consumption, while request-based charging protects reservations; production systems often need both views.

## Failure Modes and Misconceptions

- “Fair means equal.” Equality of which subject, resource, outcome, and interval must be stated.
- “Equal task counts are fair.” Task shapes and duration differ.
- “Queue capacity is dedicated hardware.” It is often a scheduling entitlement over active cluster capacity.
- “Guaranteed means immediate.” Restoration may await completion or preemption.
- “Borrowed capacity belongs to the borrower.” It remains reclaimable under the contract.
- “Memory fairness covers the cluster.” CPU, storage, network, and devices can dominate.
- “DRF is a complete scheduler.” Placement, topology, locality, priorities, gangs, and time remain.
- “Under-share means schedulable.” Pending shapes can be infeasible or fragmented.
- “Preempting enough total resources makes room.” They must be the right vector on a feasible node/topology.
- “Priority and fairness are the same dimension.” Priority orders/protects; fairness divides according to policy.
- “Work conservation always helps.” Borrowing long non-preemptible work can violate restoration objectives.
- “A fair instant implies fair history.” Service can be unequal over the contract window.
- “Jain's index proves justice.” It measures equality of chosen inputs, not entitlement legitimacy or demand.
- “Requests are truthful demand.” Users and estimators can inflate, understate, or split work.
- “High utilization implies good scheduling.” Starvation, slowdown, locality, churn, and failures may be unacceptable.
- “Changing queue weights is harmless.” It changes entitlements and may trigger widespread preemption.

## Worked Examples

### Example 1

One resource has capacity 12 and demands `(2,5,20)`. Equal max-min water filling gives `(2,5,5)`: the first two stop at demand and the last receives the remainder. Equal thirds `(4,4,4)` would waste two units offered to the first while leaving demand elsewhere.

### Example 2

With weights `(1,2)` and abundant demand, capacity 12 divides `(4,8)` under weighted max-min because normalized allocations are both 4. The weights express policy; they do not prove either user's work benefits linearly.

### Example 3

A 100-CPU/400-GiB cluster allocates A `(30,40)` and B `(10,120)`. Each has dominant share 0.30: A is CPU-dominant and B memory-dominant. Equal CPU or equal memory alone would miss the complementary demand.

### Example 4

Parent `analytics` owns 60 percent. Children `production` and `research` divide it 2:1, so their steady shares of whole capacity are 40 and 20 percent. If research is idle, production may borrow toward its maximum; research's return triggers bounded restoration, not an immediate physical teleport of running tasks.

### Example 5

Queue A is owed capacity but its next task needs a 64-GiB node; only 32-GiB fragments are free. Preempting 64 GiB spread across four unrelated nodes does not help. Victims must create a feasible node or the scheduler should reserve/defragment deliberately.

### Example 6

The fair job has no node-local task. Waiting up to two scheduling opportunities lets another job take local slots; then the first relaxes to rack-local or remote. The bound trades a short share delay for higher throughput without indefinite starvation.

### Example 7

A six-worker gang receives three incremental slots and cannot start, while other jobs wait. A bounded reservation either assembles all six by a deadline or releases the three; reserved capacity is charged to the gang's subject.

### Example 8

A borrower runs four-hour non-checkpointable tasks in another queue's idle share. When the owner returns, completion-only restoration takes hours. If the guarantee promises ten minutes, admission must restrict such borrowing or enable tolerable preemption.

### Example 9

Normalized services are `(1,1,2)` for three equal subjects. Jain's index is $16/(3\times6)=8/9\approx0.889$. The number summarizes inequality but does not reveal whether subject three had double weight or the others lacked demand.

### Example 10

This executable performs six simplified feasible DRF assignments for complementary task shapes. It omits weights, finite demands, node placement, indivisibility effects beyond whole tasks, hierarchy, locality, time, reservations, priorities, and preemption.

<!-- bijux-verify: {"id":"simplified-dominant-share-allocation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"assignments=('A', 'B', 'A', 'B', 'A', 'B')\nA=(9, 3) share=0.75 B=(3, 9) share=0.75\ntotal=(12, 12)\n","stderr":""}} -->
```python
capacity = (12, 12)
shapes = {"A": (3, 1), "B": (1, 3)}
allocation = {"A": [0, 0], "B": [0, 0]}
assignments = []

for _ in range(6):
    shares = {
        name: max(values[0] / capacity[0], values[1] / capacity[1])
        for name, values in allocation.items()
    }
    used = tuple(sum(allocation[name][d] for name in allocation) for d in range(2))
    eligible = [
        name for name, shape in shapes.items()
        if all(used[d] + shape[d] <= capacity[d] for d in range(2))
    ]
    chosen = min(eligible, key=lambda name: (shares[name], name))
    for dimension in range(2):
        allocation[chosen][dimension] += shapes[chosen][dimension]
    assignments.append(chosen)

a = tuple(allocation["A"])
b = tuple(allocation["B"])
total = tuple(a[d] + b[d] for d in range(2))
share_a = max(a[0] / capacity[0], a[1] / capacity[1])
share_b = max(b[0] / capacity[0], b[1] / capacity[1])
print("assignments=" + repr(tuple(assignments)))
print("A=" + repr(a) + " share=" + str(share_a) + " B=" + repr(b) + " share=" + str(share_b))
print("total=" + repr(total))
```

## Cross-Program Connections

- **Algorithms and optimization:** water filling, multi-resource allocation, matching, bin packing, and online scheduling define ideal/feasible gaps.
- **Economics and mechanism design:** entitlements, strategy resistance, borrowing, opportunity cost, and efficiency/fairness trade-offs shape policy.
- **Platform engineering:** queue hierarchies, quotas, priorities, reservations, admission, preemption, and audit expose the contract.
- **Security engineering:** authenticated identity, authorized queues/priorities, anti-splitting, request validation, and protected telemetry prevent gaming.
- **Reliability engineering:** restoration time, victim disruption, recovery capacity, degraded pools, and failover determine whether guarantees are credible.
- **Data engineering:** stage width, shuffle, locality, skew, caches, state, and task duration determine feasible useful service.
- **FinOps:** steady entitlement, borrowed capacity, resource-time, scarce devices, and outcome cost support organizational accountability.
- **Governance:** weights and capacities encode organizational choices and require owners, review, versioning, expiry, and appeals.

## References

1. Ghodsi et al. [Dominant Resource Fairness: Fair Allocation of Multiple Resource Types.](https://digicoll.lib.berkeley.edu/record/136796/files/EECS-2011-18.pdf) Primary dominant-share, progressive allocation, strategy-proofness, envy-freeness, sharing-incentive, and Pareto-efficiency paper under its model.
2. Verma et al. [Large-scale Cluster Management at Google with Borg.](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) Primary production cluster-management paper covering priority, quota, admission, resource reclamation, packing, and workload isolation.
3. Jain, Chiu, and Hawe. [A Quantitative Measure of Fairness and Discrimination for Resource Allocation in Shared Computer Systems.](https://www.cs.wustl.edu/~jain/papers/ftp/fairness.pdf) Primary fairness-index definition, properties, and interpretation paper.
4. Apache Hadoop. [CapacityScheduler.](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html) Current hierarchical capacity, absolute/percentage/vector resources, elasticity, maxima, user limits, priorities, ordering, labels, reservations, and preemption configuration.
5. Apache Hadoop. [Fair Scheduler.](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/FairScheduler.html) Current fair/DRF/FIFO policies, hierarchical queues, weights, minimum shares, active-app limits, preemption timeouts, and steady/instantaneous shares.
6. Apache Hadoop. [Capacity Scheduler Preemption.](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html#Preemption) Current proportional capacity preemption, monitoring, thresholds, conservative DRF, and intra-/cross-queue controls.
7. Apache Hadoop. [YARN Resource Model.](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/ResourceModel.html) Current multi-resource names, units, types, minimum/maximum allocation, and profile model underlying scheduling shares.
8. Apache Spark. [Job Scheduling: Fair Scheduler Pools.](https://spark.apache.org/docs/latest/job-scheduling.html#fair-scheduler-pools) Current within-application FIFO/fair pools, weights, minimum shares, and pool assignment.
9. Apache Mesos. [Allocation Module.](https://mesos.apache.org/documentation/latest/allocation-module/) Official hierarchical DRF allocator, roles, quotas, weights, filters, and allocation-cycle interface documentation.
10. Hindman et al. [Mesos: A Platform for Fine-Grained Resource Sharing in the Data Center.](https://www.usenix.org/conference/nsdi11/mesos-platform-fine-grained-resource-sharing-data-center) Primary two-level resource-offer, DRF, locality, framework filtering, and work-conserving cluster-sharing paper.
11. Kubernetes. [Resource Quotas.](https://kubernetes.io/docs/concepts/policy/resource-quotas/) Current namespace aggregate quotas, scopes, priority-class quotas, requests/limits accounting, and admission behavior.
12. Kubernetes. [Pod Priority and Preemption.](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/) Current priority authorization concerns, victim selection, graceful termination, feasibility limitations, and disruption interactions.
13. Kubernetes. [Pod Topology Spread Constraints.](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) Current domain eligibility, skew, hard/soft constraints, affinity interaction, and placement behavior illustrating allocation-versus-feasibility limits.

## Exercises

### Exercise 1

Allocate single-resource capacity 24 with equal max-min fairness to demands `(3,9,30,30)`. Show the water-filling result and verify capacity/demand constraints.

### Exercise 2

A cluster has 100 CPU and 500 GiB. A holds `(40,50)`, B `(10,200)`, and C `(20,50)`, with weights `(2,1,1)`. Compute dominant and weighted dominant shares and identify who is next in simplified weighted DRF if all have feasible demand.

### Exercise 3

A parent queue owns 70 percent. Its children have relative shares 4:2:1. Compute their steady whole-cluster shares. The smallest child is idle and the largest borrows its share; define what must happen when the smallest returns.

### Exercise 4

Normalized service over a window is `(2,2,2,6)`. Compute Jain's index. Explain at least four reasons it cannot by itself establish policy fairness.

### Exercise 5

Design a production review for hierarchical fair/capacity scheduling across batch, interactive, streaming, accelerator, and rigid workloads. Include identities, resources, time, borrowing, locality, placement, preemption, security, observability, testing, and rollout.

## Answers to the Exercises

### Answer 1

Raise all four to 3, consuming 12; the first reaches demand. Divide the remaining 12 among three, raising each by 4. Allocation is `(3,7,7,7)`. It sums to 24, no allocation exceeds demand, and the unsatisfied subjects have equal allocation. The second has demand 9 but capacity exhausts before reaching it.

### Answer 2

A's shares are 0.40 CPU and 0.10 memory, dominant 0.40, weighted 0.20. B's are 0.10 and 0.40, dominant/weighted 0.40. C's are 0.20 and 0.10, dominant/weighted 0.20. A and C tie for smallest weighted dominant share; a deterministic tie-break and feasible bundle decides next. The calculation omits node placement, task shape, demand limits, and hierarchy.

### Answer 3

Relative total is 7, so whole-cluster steady shares are $70\%\times4/7=40\%$, $20\%$, and $10\%$. Borrowing can let the largest use the idle 10 percent within its maximum. On return, the smallest becomes entitled to service; new completions should flow to it or bounded preemption should restore 10 percent within the promised interval. The borrower was never guaranteed the extra share. Placement may require reclaiming a feasible vector, not arbitrary totals.

### Answer 4

$J=(2+2+2+6)^2/(4(2^2+2^2+2^2+6^2))=144/(4\times48)=0.75$. It does not encode weights/entitlements, unmet demand, resource dimensions, placement feasibility, or whether service produced useful outcomes. It also depends on the chosen interval and normalized quantity; the fourth subject may legitimately have triple weight or the others may have no demand.

### Answer 5

Define authenticated subjects at tenant/queue/user/application/job levels and a versioned hierarchy with parent/child capacities, weights, minima, maxima, user/active-app limits, reservations, priorities, and resource partitions. Use allocatable CPU, memory, storage/network classes, and typed devices with canonical request accounting; compute ideal weighted dominant shares without exceeding demand. Define steady versus instantaneous/temporal entitlement, work-conserving borrowing, borrower charges, activation, and bounded restoration. Apply bounded locality delay, feasible node/device/topology placement, fragmentation/reservation rules, and atomic gang treatment. Preemption must identify a still-pending feasible beneficiary, right-vector victims, protection/grace, state/shuffle/checkpoint/retry/external-effect cost, fencing, and anti-oscillation. Authorize queue/priority/move/config changes; prevent identity splitting and request/task-size gaming. Observe entitlement/demand/allocation/use, weighted dominant shares, deficits/surplus/borrowing, pending/starvation, locality, fragmentation, preemption/restoration, victim outcomes, completion/slowdown/deadlines/freshness, utilization, failures, and cost. Replay correlated traces and adversarial mixes; inject idle-owner return, capacity shrink, node/scheduler failure, infeasible gangs, stale policy, and abuse. Canary pools/queues, compare FIFO/static/fair baselines, gate on both invariants and outcomes, atomically activate versioned policy, and retain rollback with audited reconciliation.
