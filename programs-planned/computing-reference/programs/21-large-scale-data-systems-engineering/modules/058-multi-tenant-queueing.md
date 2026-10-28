---
module_id: LSDS-058
program: Large-Scale Data Systems Engineering
level: 2
module_number: 58
title: Multi-Tenant Queueing
status: complete
last_verified: 2026-09-04
---

# Multi-Tenant Queueing

## One-Page Review

### Governing question

How should a shared data platform order and admit work from many tenants so guarantees, priorities, deadlines, efficiency, and eventual progress remain enforceable across multiple resources and a changing queue hierarchy?

### Essential definitions

- A **tenant** is an authenticated accounting and policy principal, not merely a submitted username or namespace string.
- A **leaf queue** accepts workloads; a **parent queue** aggregates capacity, policy, and usage across descendants.
- **admission** reserves quota/resources and authorizes a workload to become runnable; queue order alone does not guarantee placement.
- A **guarantee/minimum** is protected capacity under declared demand conditions; a **maximum/quota** is an upper bound.
- **borrowing** lets a queue use another queue's idle or shared capacity subject to a reclamation contract.
- **fair share** is an allocation target under contention; **fairness debt** captures historical under-service or over-service.
- A workload's **dominant share** is its largest fraction of any cluster resource; **DRF** seeks fairness over dominant shares.
- **head-of-line blocking** occurs when an unplaceable queue head prevents eligible later work from using capacity.
- **aging** increases effective priority or protection with wait/service history to prevent starvation.
- **backfilling** admits smaller/shorter work into gaps without violating an earlier reservation or service promise.

### Central model, mechanism, or theorem

Let tenant/queue $i$ use vector $u_i$ in capacity vector $C$. Its dominant share is

$$d_i=\max_k\frac{u_{i,k}}{C_k},$$

and a simple weighted score is $d_i/w_i$. A fair selector can consider the eligible queue with the smallest weighted share, but selection is followed by vector, topology, quota, admission-check, and gang feasibility. Hierarchical policy recursively selects among children while enforcing every ancestor guarantee/maximum. Queue correctness requires stable tenant/workload identity, atomic admission, durable usage/debt, bounded priority scope, borrowing/reclamation rules, and starvation protection. DRF is one allocation policy, not proof of low latency, placement feasibility, or fairness over jobs, people, cost, or historical service.

### Critical invariants

- Authentication and authorized placement bind every workload to exactly one canonical tenant and leaf queue generation.
- Usage, reservations, pending demand, debt, and limits aggregate through every ancestor without double counting.
- The sum of sibling guarantees fits effective parent capacity under the declared resource/flavor scope.
- No descendant can exceed the effective minimum of its own and ancestor maxima.
- Queue ordering never bypasses resource-vector, topology, security, residency, device, volume, gang, or health feasibility.
- Borrowed capacity remains attributable to borrower and owner, has a published reclaim policy, and creates no permanent entitlement.
- Priority is scoped and quota-governed; tenants cannot self-assign cluster-global urgency.
- Retries, speculation, requeue, and scheduler failover retain original tenant/history and do not reset age or consumption.
- Skips/backfill are bounded and auditable so large or constrained work is not starved by easy small work.
- Policy changes are versioned, validated, reconciled, canaried, and reversible without orphaning admitted work.

### Common failures

Common failures include trusting user-supplied queue names; configuring guarantees larger than parent capacity; treating quota as reserved capacity; comparing CPU-only shares in a CPU-and-memory cluster; equating FIFO with one job running at a time; letting an unplaceable head block all successors; backfilling without protecting the reservation; allowing priority inflation; charging only successful attempts; resetting historical usage on retry or queue move; lending without reclamation; preempting below a guarantee; multiplying dynamic queues until scheduler state collapses; and claiming fairness from equal job counts while resource-seconds, slowdown, deadlines, or people-level outcomes remain unequal.

### Compact example

On a cluster with 100 CPU and 200 GiB, analytics uses (20,80), so its dominant share is 0.40. ETL uses (40,40), also 0.40, but has weight 2, giving a weighted score 0.20. Research uses (10,60), dominant/weighted share 0.30. A simple weighted-DRF selector considers ETL next. Its next request still must fit its queue maxima, ancestors, resource flavor, and physical placement.

### Connections

[LSDS-051](051-cluster-resource-models.md) defines multi-resource demand, [LSDS-052](052-static-and-dynamic-allocation.md) separates reservation from use, [LSDS-053](053-fair-and-capacity-scheduling.md) establishes fairness/guarantees, [LSDS-056](056-preemption.md) reclaims entitlements, and [LSDS-057](057-memory-cpu-and-i-o-isolation.md) enforces admitted allocations on nodes.

## Governing Question

A multi-tenant data cluster accepts interactive queries, scheduled pipelines, streaming services, notebooks, experiments, repair jobs, and best-effort backfills. Their owners have different budgets and objectives. A single global FIFO queue lets a large arrival delay everything behind it; unconstrained priority lets one tenant dominate; equal job counts ignore resource size; static partitions waste idle capacity; and unrestricted borrowing makes guarantees unenforceable when owners return.

Queueing has several layers. The admission queue decides which workloads may reserve quota. A scheduler chooses runnable work and physical placement. A framework may maintain its own pools of tasks. A storage or service dependency has another queue. Optimizing one layer can move waiting elsewhere. Durable events must distinguish submitted, eligible, quota-admitted, placement-pending, running, throttled, preempting, and completed.

The governing question is how to authenticate tenant identity, build a comprehensible hierarchy, declare feasible guarantees and maxima, select fairly across heterogeneous resources, integrate priority/deadlines, lend idle capacity, avoid head-of-line starvation, account retries and history, scale dynamic queues, and prove outcomes across all tenants.

## Why This Matters

Queue policy is an executable allocation of organizational power. It determines whose incident repair starts, whose report misses a deadline, whose experiment waits, and who pays for borrowed capacity. Small configuration errors can become systematic inequity or production outages.

Efficiency and isolation pull in different directions. Dedicated partitions make guarantees obvious but strand capacity. Shared pools raise utilization but need fair selection and safe reclamation. Backfill consumes gaps but can delay a large reservation. Historical usage discourages monopolization but can punish a tenant long after demand changes. The contract must say what “fair” means over what interval and resources.

Data workloads are multidimensional and indivisible. A GPU job and a memory-heavy join can each be dominant in different resources. A gang needs many placements simultaneously. A local-volume task cannot use arbitrary quota. A queue may deserve service yet have no feasible node because capacity is fragmented. Queue order and physical feasibility must be coordinated without conflation.

Retries and speculation complicate accounting. If failed attempts are free, unreliable jobs externalize cost. If a resubmission gets fresh age, tenants can game priority. If every attempt is charged without distinguishing platform-caused failures, users bear infrastructure defects. The ledger needs logical workload identity, attempt lineage, cause, and explicit compensation policy.

Finally, queue state is durable control-plane state. Scheduler failover, delayed usage events, configuration reloads, namespace deletion, and tenant renames can corrupt accounting. Versioned policy, idempotent events, reconciliation, and audit are as important as the ordering algorithm.

## Prerequisites and Retrieval

Review multi-resource vectors in [LSDS-051](051-cluster-resource-models.md), reservations and elasticity in [LSDS-052](052-static-and-dynamic-allocation.md), fair/capacity scheduling in [LSDS-053](053-fair-and-capacity-scheduling.md), placement in [LSDS-054](054-data-local-task-placement.md), work movement/speculation in [LSDS-055](055-work-stealing-and-speculation.md), preemption in [LSDS-056](056-preemption.md), and runtime isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md).

You should understand vectors, max-min fairness, priority, quotas, hierarchy, resource flavors, gang scheduling, leases, attempts, preemption, queueing delay, percentiles, service-level objectives, identity/authentication, and transactional state.

## Learning Objectives

After this module, you should be able to:

1. distinguish submission, admission, scheduling, framework, and dependency queues;
2. design tenant identity, queue placement, hierarchy, ACL, and lifecycle rules;
3. validate guarantees, maxima, concurrency, and parent-child resource invariants;
4. compute dominant and weighted dominant shares for multi-resource usage;
5. compare FIFO, priority, fair sharing, historical usage, deadlines, and reservations;
6. design borrowing, lending, reclamation, and preemption contracts;
7. prevent head-of-line blocking, small-job bias, large-job starvation, and priority gaming;
8. account attempts, retries, speculation, requeues, failures, and queue moves durably;
9. operate dynamic queue/configuration changes without state or policy escape; and
10. validate utilization, latency, fairness, starvation, cost, security, and human impact.

## Core Exposition

### Define the queueing layers

Draw the full path: submission gateway, tenant queue, quota admission, cluster placement, framework task pools, executor queues, storage/network/service queues, and result publication. Assign each state one owner and stable timestamps. “Queued for 20 minutes” is useless if it mixes admission denial with resource fragmentation or dependency backpressure.

Decide whether the unit is job, workload, gang, stage, or task. A workload-level admission queue can reserve its full vector; task-level fair scheduling can then share within it. Avoid double fairness that unintentionally squares weights or lets a framework hide internal demand.

### Establish canonical tenant identity

Resolve authenticated principal, organization/project, billing owner, security boundary, and policy class at submission. Map them to a leaf queue through administrator-owned rules. Reject unknown or ambiguous destinations rather than falling into an unlimited default.

Do not trust a workload label to claim a privileged queue. Enforce submit/admin ACLs, priority-class permissions, namespace/project mappings, and impersonation audit. Keep immutable workload identity even if display names or organizations change.

### Design hierarchy by durable ownership

Use a shallow, comprehensible tree: root, major organizational or service-class boundary, and leaf queues where work submits. Parent queues aggregate constraints and allocate among children. Avoid one queue per ephemeral run; it multiplies policy objects, metrics, reconciliation, and orphan risk.

Document inheritance and override rules for guarantees, maxima, weights, priority scope, preemption, concurrency, and ACLs. A child cannot create capacity its parent lacks. Queue deletion or move needs a migration plan for pending, admitted, running, and historical records.

### Validate guarantees and maxima

A guarantee/minimum means protected access when the queue has eligible demand and effective cluster capacity exists. A maximum caps use even if resources are idle. Quota commonly means a ceiling, not pre-reserved physical capacity. State whether guarantees are hard reservations, scheduling targets, or preemption-backed promises.

For each resource flavor/topology, ensure sibling guarantees do not exceed the parent's effective guarantee/capacity unless overbooking is explicitly modeled. Propagate maxima downward: effective child maximum is bounded by every ancestor. Validate units and resource names before activation.

### Limit control-plane concurrency

CPU and memory quota do not prevent thousands of submitted applications, coordinators, pending pods, or metadata objects. Add per-user/queue running-workload, pending-workload, task, coordinator, and object limits. Admission checks should reserve control-plane as well as worker capacity.

Apply rate limits and bounded queues at submission. Return explicit retry/backoff information. Unlimited pending work can overwhelm schedulers and make meaningful waiting-time promises impossible.

### Choose FIFO deliberately

FIFO orders by eligible arrival, often with priority first. It is understandable and can be appropriate inside a homogeneous queue. It does not necessarily run only one application: schedulers may allocate to the first job until it cannot use an offer, then consider others.

Define the timestamp: original submission, eligibility after dependencies, retry, or administrative move. Preserve it against resubmission gaming. Pure FIFO suffers head-of-line blocking and gives no slowdown protection when sizes vary.

### Scope priority

Priority represents an authorized service policy, not a user's subjective importance. Use a small documented set, quota their consumption, and fence tenant-local priorities so they cannot outrank system or other-tenant work. Within a tenant, priority can express production over experimentation.

Add aging or deadline-aware escalation only with bounds. Global strict priority can starve lower classes forever. Priority inversion can also occur when a high-priority task depends on low-priority producers; propagate or reserve dependency service carefully.

### Apply max-min and weighted fairness

Single-resource max-min fairness raises the smallest allocation until demand is satisfied or capacity exhausted. Weights scale entitlements: compare normalized allocation rather than raw units. Work conservation lends unused share to active demand.

Fair allocation is a target, not an ordering shortcut. Indivisible tasks, placement, minimum allocation sizes, and stale usage create approximation. Measure convergence and slowdown, and state the time horizon over which weights should hold.

### Use dominant-resource reasoning

For multiple resources, compare each user's largest normalized share. A CPU-heavy and memory-heavy tenant can be treated symmetrically in their dominant resources. Weighted DRF divides dominant share by policy weight when choosing the most under-served active principal.

Define the capacity denominator: whole cluster, partition, resource flavor, or topology domain. Include only schedulable resources and consistent reservations. DRF does not solve task placement, fragmentation, deadlines, or historical fairness by itself.

### Decide the fairness principal

Fairness per job rewards tenants who submit many jobs. Fairness per user fails when service accounts represent whole teams. Fairness per queue/project may hide unequal people. Choose an authenticated principal aligned with governance, then optionally share recursively within it.

Sybil resistance matters: creating namespaces, accounts, or queues must not multiply share. Mergers/splits and service-account rotation need ledger continuity. Publish how weights are set and reviewed.

### Include historical usage carefully

Instantaneous fairness forgets yesterday's monopolization and may oscillate with bursty demand. A resource-time ledger or decayed usage can prioritize tenants that consumed less over a declared window. Weight CPU-seconds, GiB-seconds, accelerator-seconds, and other costs deliberately.

Long memory can punish a tenant after an emergency or organizational change; short memory enables burst gaming. Persist samples through failover and make clock/window semantics explicit. Separate usage correction from arbitrary manual score editing.

### Distinguish reservations from fair share

A reservation promises future capacity for a workload or time window. Fair sharing allocates currently available capacity among active demand. Backfilling may use a reservation's idle gap only if it cannot delay the reserved start under the declared confidence policy.

Reserve complete resource/topology vectors, not abstract slots. Expire abandoned reservations and charge holding cost. A reservation without physical feasibility or reclaim authority is merely hopeful metadata.

### Manage borrowing and lending

Let queues exceed nominal guarantees when siblings are idle to preserve work conservation. Record borrowed amount per resource/flavor and the lender/cohort policy. Cap lending if the owner needs rapid return or if reclaim would be destructive.

The borrower contract states notice, grace, checkpointability, preemption order, and compensation. Borrowing creates usage, not a new guarantee. When owners return, first stop new borrowed allocations, then allow natural completion or invoke [LSDS-056](056-preemption.md) according to the SLO.

### Avoid head-of-line blocking

If the head needs a scarce GPU, large gang, unavailable volume, or impossible topology, strict FIFO can strand unrelated CPU/memory. Classify why it cannot fit. Permit bounded bypass for later jobs that use disjoint capacity, while retaining a reservation, age, or skip budget for the head.

Do not skip permanently. Track qualifying opportunities, not scheduler loops, and stop backfill before it threatens the protected start. Split queues by incompatible resource flavor only when ownership and fairness remain coherent.

### Protect large and constrained workloads

Small tasks often pack easily and complete quickly, so throughput-oriented policies can starve large jobs. Use aging, reservations, gang admission, maximum bypass counts, or a fraction of capacity for large/constrained demand. Estimate duration only where predictions are calibrated.

Fragmentation is not queue unfairness, though it can cause unfair outcomes. Record “selected but unplaceable” separately from “not selected.” Coordinate compaction/preemption or topology-aware admission rather than inflating priority blindly.

### Handle deadlines and SLO classes

Earliest-deadline-first can improve feasible deadline completion but a doomed job can consume capacity pointlessly. Estimate remaining work, parallelism, dependencies, and attainable capacity; reject or renegotiate infeasible deadlines. Reserve slack for uncertainty and recovery.

Do not translate every SLO into global priority. Interactive, scheduled, streaming, repair, and best-effort classes may need separate admission budgets plus fair sharing within each. Measure missed deadlines and displaced work together.

### Account attempts and failures

Charge every running attempt's actual resource-time, including speculation and retries, while retaining logical-workload grouping. Record failure cause so platform-caused loss can receive explicit credit without erasing physical cost. Requeue preserves original age/debt unless policy documents otherwise.

Prevent cancel/resubmit from resetting history. A moved workload keeps its ledger, attempts, and admission generation. Exactly-once ledger events need stable allocation IDs and idempotent start/stop reconciliation.

### Coordinate with preemption

Preemption enforces priority or minimum-share/reclamation promises after waiting thresholds. It must not push victims below protected guarantees or outside priority fences. Victim cost and recovery remain part of the decision; queue arithmetic alone does not make disruption free.

Use hysteresis and cooldown so queues do not trade victims repeatedly as demand fluctuates. Reconcile borrowing, usage, pending demand, and released capacity before declaring fairness restored.

### Operate dynamic configuration safely

Validate proposed trees offline: unique paths, leaf/parent roles, ACLs, mappings, resource names/units, guarantees, maxima, weights, priority fences, and preemption rules. Diff effective inherited policy, not only source text. Reject partial or internally inconsistent reloads atomically.

Version every decision with the policy generation. On rollback, reconcile admitted workloads under a declared grandfather/migrate/preempt policy. Queue rename is an identity migration, not delete-and-recreate if history matters.

### Observe queue-to-outcome flow

Emit timestamps and reasons for submission, eligibility, admission-check wait, quota wait, selection, placement attempts, reservation, start, preemption, retry, and completion. Track pending/running vectors, guarantees/maxima, borrowed/lent resources, dominant/weighted shares, usage history, debt, skips, and rejected mappings.

Report wait and slowdown by tenant, class, size, resource flavor, topology, and outcome. Aggregate percentiles without hiding small tenants or permanently pending jobs. Alert on starvation age, guarantee deficit, cap breach, priority concentration, excessive retries, and scheduler state growth.

### Validate fairness and human impact

Replay trace arrival/order/resource vectors and compare FIFO, priority, fair, historical, deadline, and backfill policies. Include adversarial many-small-job submission, under-requesting, priority inflation, queue hopping, constrained gangs, dynamic queues, failures, and demand bursts.

Check invariants first, then utilization, throughput, queue time, slowdown, deadlines, guarantee attainment, dominant-share convergence, starvation, preemption/lost work, cost, and affected teams. Shadow decisions, canary selected queues, publish explainable reason codes, and retain rollback.

## Definitions and Notation

Let $C_k$ be schedulable capacity of resource $k$. Tenant $i$ has current allocated/charged vector $u_i$, demand $r_i$, policy weight $w_i>0$, guarantee $g_i$, maximum $m_i$, historical/debt state $h_i$, and eligible workload set $E_i$.

Resource share is $s_{i,k}=u_{i,k}/C_k$, dominant share is $d_i=\max_k s_{i,k}$, and a simple weighted dominant score is $z_i=d_i/w_i$. Capacity denominators must match the partition/flavor/topology in which tasks compete. Zero or unavailable resources are excluded or make demand infeasible rather than permitting division.

For hierarchy node $q$, usage $U_q$ is the deduplicated sum of descendant allocations, and pending demand $D_q$ aggregates eligible descendants. Effective maximum is bounded by all ancestors. Borrowed vector $b_q=\max(0,U_q-g_q)$ is only meaningful under a defined guarantee/cohort scope.

Let workload $j$ have eligible time $a_j$, effective priority $p_j(t)$, feasible-placement predicate $F_j(n)$, and bypass count $x_j$. Ordering produces a candidate; admission requires queue/ancestor capacity and a physical placement satisfying $F$. Slowdown may be measured as response time divided by an agreed solo/service-time estimate, with uncertainty disclosed.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence:

1. Resolve authenticated tenant, billing/security ownership, canonical leaf queue, and immutable workload identity.
2. Validate the complete hierarchy, inheritance, ACLs, guarantees, maxima, weights, concurrency, priorities, and resource scopes.
3. Record submission and eligibility separately; run dependency/admission checks before treating demand as schedulable.
4. Compute current/reserved/historical resource vectors through ancestors using idempotent allocation events.
5. Select among active queues using declared FIFO, priority, fair, dominant-share, history, deadline, or reservation policy.
6. Prove queue/ancestor quota plus vector/topology/device/gang/security feasibility before atomic admission.
7. Apply bounded bypass/backfill, borrowing, and preemption while preserving reservations, guarantees, and starvation protection.
8. Charge all attempts/retries/speculation and retain age/debt across requeue, move, failure, and scheduler restart.
9. Observe reasoned state transitions, waits, shares, outcomes, policy generations, abuse signals, and human impact.
10. Replay representative/adversarial traces, shadow, canary, reconcile configuration change, and retain rollback.

If every leaf allocation event is counted once in each ancestor, then parent usage equals the union of descendant allocations. Atomic admission checking effective maxima prevents a new allocation from knowingly exceeding a queue or ancestor limit. This assumes no event loss/duplication and consistent policy generation; reconciliation is required in a distributed controller.

Weighted dominant-share order considers the active tenant with smallest $d_i/w_i$, but indivisible tasks can overshoot and physical placement can reject the candidate. Thus the score supplies a fairness direction, not a complete allocator. Repeatedly skipping an infeasible candidate needs bounded bypass plus reservation/aging to preserve liveness.

Borrowing is work-conserving when unused entitlement can serve another queue. It preserves the owner's future guarantee only if admission stops new borrowing and natural completion or safe preemption returns sufficient usable capacity within the promised time. Without that reclamation mechanism, the “guarantee” is not operationally proven.

## Alternatives and Trade-Offs

- **One global FIFO queue:** simple and auditable; head-of-line delay and no tenant isolation.
- **Static partitions:** clear ownership and fault boundaries; idle resources strand while other tenants wait.
- **Hierarchical queues:** compose organization and policy; inheritance and state migration add complexity.
- **Strict priority:** fast urgent service; starvation and priority inflation without quotas/fences.
- **Aging priority:** eventual progress; old low-value work can outrank new emergencies if unbounded.
- **Round robin by job:** simple turn taking; ignores job size and multi-resource consumption.
- **Max-min fairness:** protects small allocations for one resource; multiple resources need a declared extension.
- **Weighted DRF:** balances dominant multi-resource shares; does not solve placement, deadlines, or historical justice.
- **Historical usage fairness:** discourages repeated monopolization; window/decay choices can punish legitimate bursts.
- **Guarantees plus borrowing:** high utilization with protected owners; reclamation disrupts borrowers.
- **Hard maxima:** contain tenants predictably; can leave otherwise useful capacity idle.
- **Backfilling:** improves gap utilization; inaccurate durations or weak reservations delay queue heads.
- **Separate service-class queues:** clearer SLO budgets; cross-class capacity and dependency priority remain hard.
- **Dynamic queues:** flexible delegation; unbounded cardinality, policy escape, and orphan history threaten operations.
- **Per-job fairness:** easy framework semantics; tenants gain share by submitting more jobs.
- **Per-tenant fairness:** Sybil-resistant when identity is governed; internal team allocation needs another layer.

## Failure Modes and Misconceptions

- **“Namespace equals tenant.”** identity, billing, security, and organizational ownership may not align.
- **“Quota guarantees capacity.”** a ceiling blocks excess use but does not reserve physical resources.
- **“Configured minima always fit.”** parent, flavor, topology, failures, and overbooked siblings can contradict them.
- **“FIFO runs one job at a time.”** many implementations allocate concurrently when the head cannot use all offers.
- **“Priority is fairness.”** strict priority expresses precedence and can starve lower classes.
- **“Equal job count is equal treatment.”** jobs consume different vectors, time, and value.
- **“CPU fairness is cluster fairness.”** memory, GPU, storage, network, and control-plane resources also bind.
- **“DRF solves placement.”** dominant shares do not create a feasible node, topology, volume, or gang.
- **“Backfill cannot hurt.”** it delays reservations when duration or release estimates are wrong.
- **“Skipping an infeasible head is always safe.”** unlimited bypass starves large/constrained work.
- **“Borrowed capacity becomes the borrower's baseline.”** borrowing is reclaimable under the published contract.
- **“Successful attempts are the only usage.”** failed, speculative, and preempted attempts consumed resources too.
- **“Retry deserves a fresh timestamp.”** this permits resubmission gaming and erases suffered delay.
- **“More queues improve isolation.”** high cardinality can overwhelm the control plane and fragment fairness.
- **“High utilization proves good scheduling.”** tail wait, slowdown, starvation, deadlines, and human impact may regress.
- **“Rollback deletes new state.”** admitted workloads and usage/debt under the new generation need reconciliation.

## Worked Examples

### Example 1

Root has 100 CPU guaranteed capacity. Children A and B each claim a 60-CPU hard guarantee. The configuration cannot honor both under simultaneous demand. Reject it or redefine them as weights/targets with explicit overbooking; do not wait for production contention to reveal the contradiction.

### Example 2

A user submits 100 one-core jobs while another submits one 100-core job. Per-job round robin can give the first tenant nearly all turns. Recursive per-tenant fairness first chooses between authenticated tenants, then schedules jobs within each tenant, preventing job-count Sybil behavior.

### Example 3

A GPU gang is first in FIFO but no eight-GPU topology exists today. CPU-only jobs behind it can run without consuming GPUs. Bounded bypass admits them while preserving the gang's age, skip count, and a future topology reservation; silent indefinite skipping would be starvation.

### Example 4

Analytics has a 40-CPU guarantee and temporarily uses 80 while research is idle. Research returns with 30 CPU demand. New analytics borrowing stops. If natural completion cannot return 30 within the SLO, the published preemption protocol reclaims eligible borrowed tasks without taking analytics below 40.

### Example 5

A production repair and experimental notebook share one tenant. Tenant-local priority lets repair run first, but a priority fence prevents that numeric value from outranking another tenant's contracted emergency class. Administrators quota who may create global service priorities.

### Example 6

A workload fails three times after consuming 50 CPU-hours per attempt. Charging only the eventual success reports 50 instead of 200 CPU-hours and rewards unreliability. The ledger charges every allocation ID, groups them under logical workload identity, and separately credits platform-caused failures according to explicit policy.

### Example 7

A reservation promises a 20-node job at 14:00. Backfill admits jobs predicted to finish before then, preserving cleanup margin and reclaimability. One job overruns; the scheduler must use its declared preemption/checkpoint contract or record a reservation breach. “Expected duration” was not a guarantee.

### Example 8

A queue is renamed during a scheduler failover. Recreating it with zero history gives the same tenant the smallest usage score and extra service. A migration maps stable queue identity to the new path while retaining allocations, pending age, historical usage, borrowing, and policy generation.

### Example 9

Dashboard metrics show equal dominant shares among three large tenants, but a small tenant's only job has waited two days because its volume is unavailable. Aggregate fairness is not liveness. The job needs an explicit infeasibility reason, storage remediation or alternative placement, and an age/SLO policy—not a higher DRF score alone.

### Example 10

The fixture calculates weighted dominant shares for one declared capacity scope and chooses the currently most under-served tenant.

<!-- bijux-verify: {"id":"weighted-dominant-share","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"weighted_dominant=(('etl', 0.2), ('research', 0.3), ('analytics', 0.4))\nnext=etl\n","stderr":""}} -->
```python
capacity = (100, 200)  # CPU, GiB
tenants = (
    ("analytics", (20, 80), 1),
    ("etl", (40, 40), 2),
    ("research", (10, 60), 1),
)

scores = []
for name, usage, weight in tenants:
    dominant = max(value / total for value, total in zip(usage, capacity))
    scores.append((name, round(dominant / weight, 2)))

scores.sort(key=lambda item: (item[1], item[0]))
print(f"weighted_dominant={tuple(scores)}")
print(f"next={scores[0][0]}")
```

The result is an ordering candidate only. The ETL workload can start next only if its request passes all queue, resource, topology, placement, and admission constraints.

## Cross-Program Connections

- **Algorithms:** max-min allocation, weighted fair queueing, constrained packing, aging, backfill, and online decisions shape scheduling.
- **Distributed systems:** identity, idempotent ledgers, leases, consensus, failover, reconciliation, and generation changes preserve state.
- **Data engineering:** DAGs, gangs, streaming services, retries, speculation, shuffle, locality, and deadlines determine demand and recovery cost.
- **Platform engineering:** namespaces/projects, queues, quotas, priority classes, admission, autoscaling, preemption, and observability expose policy.
- **Reliability engineering:** starvation, overload, reservation breach, scheduler failure, degraded capacity, canary, and rollback constrain operation.
- **Security/governance:** authentication, ACLs, Sybil resistance, priority authority, billing ownership, audit, and privacy define tenants.
- **Economics:** guarantees, borrowing, resource-time, opportunity cost, chargeback, and unused reservation cost express trade-offs.
- **Human systems:** weights and priorities distribute waiting and organizational power; outcome review must include small and disadvantaged tenants.

## References

1. Ghodsi et al. [Dominant Resource Fairness: Fair Allocation of Multiple Resource Types.](https://www.usenix.org/conference/nsdi11/dominant-resource-fairness-fair-allocation-multiple-resource-types) Primary DRF definition, properties, mechanism, and evaluation.
2. Apache Hadoop. [Fair Scheduler.](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/FairScheduler.html) Current queues, weights, shares, DRF, limits, placement, reservations, and preemption thresholds.
3. Apache Hadoop. [CapacityScheduler.](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html) Current hierarchical capacity, user limits, priorities, reservations, ordering, and preemption behavior.
4. Apache Spark. [Job Scheduling.](https://spark.apache.org/docs/latest/job-scheduling.html) Current FIFO/fair scheduling, pools, weights, minimum shares, and concurrent-job context.
5. Kueue. [Cluster Queue.](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/) Current nominal quota, borrowing/lending, resource flavors, cohort, fair sharing, and admission semantics.
6. Kueue. [Admission Fair Sharing.](https://kueue.sigs.k8s.io/docs/concepts/admission_fair_sharing/) Current historical-usage ordering, decay/sampling, resource weights, queue weights, and observability.
7. Kueue. [Workload Priority Class.](https://kueue.sigs.k8s.io/docs/concepts/workload_priority_class/) Current workload-level queue ordering and priority separate from pod-level behavior.
8. Apache YuniKorn. [Partition and Queue Configuration.](https://yunikorn.apache.org/docs/user_guide/queue_config/) Current hierarchical queues, guarantees/maxima, limits, ACLs, placement, ordering, priority fencing, and preemption settings.
9. Kubernetes. [Resource Quotas.](https://kubernetes.io/docs/concepts/policy/resource-quotas/) Current namespace aggregate compute/storage/object limits, scopes, priority-class quota, and enforcement semantics.
10. Kubernetes. [Limit Ranges.](https://kubernetes.io/docs/concepts/policy/limit-range/) Current per-object minimum, maximum, default request/limit, ratio, and admission enforcement.
11. Hindman et al. [Mesos: A Platform for Fine-Grained Resource Sharing in the Data Center.](https://www.usenix.org/conference/nsdi11/mesos-platform-fine-grained-resource-sharing-data-center) Primary two-level resource-offer, framework isolation, fairness, and sharing paper.
12. Verma et al. [Large-Scale Cluster Management at Google with Borg.](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) Primary production account of priority, quota, admission, overcommitment, rescheduling, and machine sharing.
13. Schwarzkopf et al. [Omega: Flexible, Scalable Schedulers for Large Compute Clusters.](https://research.google/pubs/omega-flexible-scalable-schedulers-for-large-compute-clusters/) Primary shared-state scheduling paper covering parallel decisions, conflicts, policy evolution, and production workloads.

## Exercises

### Exercise 1

On capacity (120 CPU, 240 GiB), tenant A uses (36,48) with weight 1 and B uses (24,96) with weight 2. Compute each dominant and weighted dominant share and identify the simple selector's next tenant.

### Exercise 2

Design a three-level queue hierarchy for system repair, two product organizations, interactive work, scheduled pipelines, and experiments. Specify identity, guarantees, maxima, weights, priority fences, concurrency, and ACLs.

### Exercise 3

Design bounded backfill for a 16-GPU gang at the head of a queue. State feasibility reasons, reservations, duration uncertainty, bypass limits, and liveness evidence.

### Exercise 4

Specify a durable accounting ledger for original attempts, speculative clones, retries, preemptions, platform failures, queue moves, and scheduler failover.

### Exercise 5

Design a production comparison of FIFO, strict priority, weighted DRF, historical usage, and guarantee-plus-borrowing. Include adversarial tenants, metrics, canary, and rollback.

## Answers to the Exercises

### Answer 1

A's shares are CPU $36/120=0.30$ and memory $48/240=0.20$, so dominant/weighted share is $0.30/1=0.30$. B's shares are $24/120=0.20$ and $96/240=0.40$, so dominant share is 0.40 and weighted share is $0.40/2=0.20$. The simple selector considers B next. Its pending request must still fit maxima, ancestors, flavor/topology, and physical placement; the calculation is not an admission proof.

### Answer 2

Use root children `system` and `products`. Only authenticated platform principals submit to `system.repair`; give it a small protected guarantee, capped emergency priority, strict concurrency, and no tenant override. Under `products`, create stable organization parents A/B with contract weights or guarantees and maxima. Each has leaves `interactive`, `pipelines`, and `experiments`; tenant identity maps by administrator-owned organization/project rules, with submit ACLs scoped to members. Fence priorities within each organization, allow only documented service classes, cap coordinators/pending/running work, give interactive bounded share/deadline budget, pipelines fair/history-aware service, and experiments borrowable/preemptible capacity. Validate sibling guarantees against parent, propagate ancestor caps, keep Sybil-resistant organization accounting, and publish lending/reclaim rules.

### Answer 3

Record that the head needs 16 GPUs in an admissible topology and distinguish quota from physical fragmentation or unavailable flavor. Reserve the earliest credible 16-GPU placement and stop admitting work that would delay it. Backfill only eligible jobs whose predicted completion plus cleanup/risk margin precedes the reservation or that are safely checkpointable/preemptible. Bound bypass by qualifying opportunities and wall time, preserve original eligible age, and cap cumulative consumed gap. Calibrate duration intervals, not means. Prove liveness with reservation attainment/start time and bounded skips; report breaches, prediction errors, fragmentation, and preemption cost.

### Answer 4

Key the ledger by immutable tenant, logical workload, allocation, attempt, resource/flavor/topology, and policy generation. Idempotent start/resize/stop events integrate actual resource-time; an allocation cannot be opened or closed twice. Primary, speculative, failed, and preempted attempts all charge physical use and link to one logical workload. Record cause and separate explicit platform-failure credits without deleting consumption. Requeue/retry retains eligible time, debt, and lineage; queue moves change path attribution prospectively under a migration transaction while stable owner/history persists. Scheduler failover replays the event log, reconciles live runtime allocations, closes or repairs ambiguous intervals, and audits corrections.

### Answer 5

Replay representative arrivals, vectors, durations, topology, gangs, failures, and class/tenant mix. Add adversarial many-job Sybils, under-requesting, priority inflation, cancel/resubmit, queue hopping, impossible heads, burst borrowing, dynamic-queue churn, and scheduler restart. Compare utilization/throughput with submission-to-eligibility/admission/placement/start time, slowdown by size/tenant, deadlines, guarantee attainment, maximum breaches, dominant-share convergence, history/debt, starvation age, bypasses, reservations, borrowed/lent/reclaimed vectors, preemptions/lost work, retries, control-plane load, cost, and affected-team outcomes. Verify identity/ACL/hierarchy/accounting invariants first. Shadow decisions, explain differences, canary selected queues with hard starvation/guarantee/security gates, preserve policy generations and prior configuration, and reconcile admitted work/history during rollback.
