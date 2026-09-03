---
module_id: LSDS-026
program: Large-Scale Data Systems Engineering
level: 1
module_number: 26
title: Stage Scheduling
status: complete
last_verified: 2026-09-03
---

# Stage Scheduling

## One-Page Review

### Governing question

How should a large-scale data system decide which ready stages and partition tasks to admit, prioritize, place, launch, preempt, or defer so dependency correctness, resource feasibility, locality, fairness, deadlines, recovery, and governance remain explicit under contention?

### Essential definitions

- A **ready stage** has every required upstream edge satisfied under its availability contract; ready does not mean admitted or placed.
- **admission control** decides whether a job or stage may enter execution given capacity, quotas, policy, and overload state.
- A **resource request vector** declares required CPU, memory, accelerator, storage, network, licenses, or other constrained quantities.
- **placement** binds a task attempt to a feasible worker or slot.
- **locality** measures how close computation is to required input or cached state; locality delay waits briefly for a better placement opportunity.
- **fairness** defines how shared capacity is divided over time; it differs from equal task count and from strict priority.
- **aging** increases effective priority with wait time to reduce starvation.
- **preemption** removes or suspends lower-priority work to make capacity available; **eviction** is the resulting removal and may waste work.
- **gang scheduling** admits a required set of tasks together when partial placement cannot make progress safely.
- **backfilling** runs smaller eligible work in capacity gaps without violating protected reservations or deadlines.

### Central model, mechanism, or theorem

Scheduling is a constrained online decision. A stage is eligible only if dependencies and policy are satisfied. A task fits worker `n` only if its request vector `r` is componentwise no greater than the worker's currently allocatable vector `a_n`, and all labels, topology, isolation, data, and device constraints hold. CPU fit cannot compensate for insufficient memory or accelerator capacity.

A priority function may combine service class, deadline slack, critical-path contribution, wait age, locality, recovery urgency, and fair-share deficit, but its terms require explicit units and guardrails. Greedy priority can improve one job while starving another or fragmenting resources. Correct evaluation measures queue time, slowdown, deadline success, fairness over time, utilization, locality, wasted/preempted work, tail task duration, and end-to-end committed results—not scheduler throughput alone.

### Critical invariants

- A stage is queued only after its exact dependency, artifact, schema, and policy prerequisites are satisfied.
- Admission and placement account for every nonfungible resource and constraint, not CPU alone or current observed usage.
- Resource reservation and binding are race-safe; failed binding releases reservations.
- Fair-share, quota, priority, aging, deadline, and preemption rules are deterministic enough to explain and audit.
- Locality waiting is bounded and cannot cause indefinite starvation or violate a protected deadline.
- Preemption respects non-preemptible regions, commit boundaries, checkpoint cost, minimum runtime, and side effects.
- Speculative and retry attempts are charged to capacity and fairness rather than treated as free.
- Scheduler state survives or reconstructs queue, reservation, attempt, and commit identity without double launch.
- Multi-tenant policy prevents one queue, user, job, or sensitive workload from bypassing isolation.
- Adaptive changes record the evidence, bounds, plan version, and resulting task/output identities.

### Common failures

Frequent failures are scheduling an entire downstream stage when only partial upstream output exists, confusing readiness with capacity, using actual CPU usage instead of resource requests for safe placement, ignoring memory/network/accelerator dimensions, strict priority starvation, FIFO head-of-line blocking, unlimited locality delay, backfilling across protected reservations, preempting almost-finished or non-idempotent work, treating speculation as free, allocating more partitions than network buffers support, trusting stale worker offers, and optimizing cluster utilization while deadline, fairness, or completion tails regress.

### Compact example

A deterministic toy scheduler has 8 CPU units, 24 memory units, and one accelerator. Three stages are ready. Scores combine modeled remaining critical path with capped wait age. Accelerator training scores 21 and is selected first; an aged audit stage scores 18 and fits next. Ingest scores 16 but its 8 memory units no longer fit the 4 remaining, so it is deferred. Reserved capacity is 6 CPU, 20 memory, and one accelerator. This illustrates multidimensional fit and aging, not a production-optimal policy.

### Connections

[LSDS-024](024-directed-acyclic-graph-execution.md) defines ready dependency structure, and [LSDS-025](025-lazy-evaluation-and-plan-construction.md) supplies the selected physical plan. [LSDS-027](../ROADMAP.md) adds retry and speculation; [LSDS-030](../ROADMAP.md) deepens resource-aware execution.

## Governing Question

A DAG exposes what may run. The scheduler decides what will run now, where, and with which resources. These are different questions. Hundreds of stages can be structurally ready while the cluster has capacity for only a few. A task may fit the aggregate free CPU yet fit no individual worker because memory is fragmented or the only accelerator is reserved.

The scheduler operates with imperfect information. Task sizes are estimates, workers change, data locations disappear, users submit new jobs, and failures create urgent recovery work. Each decision affects future decisions: placing a memory-heavy task on the only large-memory node may block a later task that cannot run elsewhere.

The governing question is how to turn readiness into safe, fair, and efficient execution without hiding policy inside an opaque score. A durable answer separates eligibility, admission, ordering, placement, launch/binding, runtime control, and commit, then records evidence for each.

## Why This Matters

Stage scheduling controls user-visible latency and cluster economics. A correct computation that waits six hours in queue misses its service objective. A scheduler that reaches 95 percent CPU utilization but thrashes memory, congests shuffle, or starves small interactive work is not successful.

Contention makes local heuristics interact. Delay scheduling improves locality but can leave slots idle. Backfilling improves utilization but can delay a reserved large job. Preemption serves urgent work but wastes completed computation and can repeat side effects. Speculation reduces some tails while doubling pressure on a saturated bottleneck.

Resource dimensions are not interchangeable. Eight free CPU cores do not help a task needing a missing GPU, 100 GiB contiguous memory, regional data access, a software license, or a specific trusted execution environment. Placement must test the full request and policy vector against a concrete node.

Fairness has human consequences. Queue weights, priorities, and quotas determine whose experiments, reports, incident repairs, accessibility jobs, or public services finish. Policy needs named ownership, transparency, appeal, and periodic evidence rather than being treated as a neutral implementation detail.

## Prerequisites and Retrieval

Recall locality and partition placement from [LSDS-004](004-data-locality.md), task graphs/stages from [LSDS-005](005-distributed-task-graphs.md) and [LSDS-006](006-stages-tasks-and-dependencies.md), dependency width from [LSDS-007](007-narrow-and-wide-transformations.md), worker serialization from [LSDS-008](008-serialization-across-workers.md), and scale accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md).

Retrieve MapReduce task attempts from [LSDS-021](021-mapreduce-execution-model.md), skew/partitioning from [LSDS-023](023-partitioners-and-combiners.md), DAG readiness and critical paths from [LSDS-024](024-directed-acyclic-graph-execution.md), and lazy/physical plan identities from [LSDS-025](025-lazy-evaluation-and-plan-construction.md).

You should understand vectors and componentwise comparison, queues/heaps, percentiles, DAG critical paths, partitions, retries, worker/node topology, quotas, idempotency, and the difference between a logical task and one execution attempt.

## Learning Objectives

After this module, you should be able to:

1. distinguish dependency readiness, admission, prioritization, placement, binding, launch, and commit;
2. model stage/task demands and worker allocatable capacity as multidimensional vectors;
3. explain FIFO, fair sharing, weighted shares, dominant-resource reasoning, priority, aging, deadlines, and reservations;
4. evaluate locality delay, backfilling, gang scheduling, preemption, and speculation under explicit constraints;
5. connect stage-level critical paths to partition-level skew and resource bottlenecks;
6. prevent starvation, head-of-line blocking, resource fragmentation, stale offers, and queue overload;
7. design race-safe reservation/binding and scheduler recovery state;
8. test scheduling policy with deterministic traces, adversarial workloads, failure, and policy drift;
9. measure queueing, slowdown, fairness, utilization, locality, wasted work, and deadline outcomes; and
10. govern multi-tenant scheduling with transparent policy, isolation, audit, and human review.

## Core Exposition

Scheduling begins with a dependency event: a stage's required upstream artifacts become valid. The DAG scheduler marks the stage eligible. A resource scheduler may still withhold admission because its tenant exceeds quota, the queue is paused, cluster health is degraded, required policy evidence is missing, or no feasible resource shape exists.

### Separate the scheduling pipeline

A useful state model is:

1. **blocked** on graph, data, schema, or policy prerequisites;
2. **eligible** when prerequisites are satisfied;
3. **admitted** when quota/overload policy accepts the work;
4. **queued** under a service class and fair-share accounting domain;
5. **reserved** on concrete resources during a scheduling transaction;
6. **bound/launched** with a worker and attempt identity;
7. **running** under runtime limits and heartbeat/lease;
8. **successful-uncommitted**, **committed**, **failed**, **canceled**, or **lost**.

Exact engines use different names. The separation prevents a green upstream status, a queue entry, or a successful attempt from being mistaken for a committed result.

### Resource vectors and feasibility

Represent request as `r=(cpu,memory,gpu,ephemeral_storage,network_class,...)`. For numeric consumable dimensions, `r_i <= a_i` is necessary. Labels and topology add predicates: architecture, zone, data residency, device model, node pool, isolation, license, and affinity/anti-affinity.

Requests are scheduling promises, while limits and observed usage serve runtime control and accounting. Placing from momentary observed low usage overcommits memory when tasks later reach peak. Some resources may be safely overcommitted with throttling; others cause eviction, corruption, or failure. State the policy by dimension.

Aggregate cluster capacity can mislead. Two nodes each with 8 GiB free cannot host a 12-GiB task. Four free single GPUs cannot satisfy a task requiring four GPUs connected on one node. Network or storage bandwidth may be unmodeled and become the true constraint.

### Stage versus task scheduling

A stage contains partition tasks. Stage scheduling orders and admits related sets; task scheduling chooses individual placements. A stage with 10,000 partitions need not launch all tasks at once. Wave execution can cap concurrency to memory, shuffle fetch, sink rate, or fair-share limits.

Some stages require a minimum parallel gang: synchronized training, barrier execution, or an algorithm that deadlocks when only part of its participants start. Gang admission must reserve the full feasible set atomically or defer it. Ordinary data-parallel stages often benefit from incremental task launch instead.

### Readiness and partial availability

Blocking exchanges commonly make a downstream stage ready only after required upstream map outputs are committed. Pipelined edges may enable consumers earlier. Multi-input stages need the availability contract for every input. Scheduler readiness cannot be inferred from a single predecessor stage label.

Partial readiness can lower latency but increases failure coupling and resource overlap. If consumers retain buffers while waiting for a slow producer, memory pressure or distributed deadlock can appear. Model buffer bounds, backpressure, rollback, retry, and simultaneous resource demand.

### FIFO and head-of-line blocking

FIFO is explainable: older eligible work runs first, sometimes with priority classes. It can be efficient for homogeneous jobs. A large first job that cannot fit may block many small feasible jobs, and long batch work can delay urgent interactive work.

Backfilling scans past the head and launches work that fits. Conservative backfilling protects a reservation or deadline for the head job. Unprotected backfilling can repeatedly consume newly free fragments and starve the large request. Record the protected capacity and expected release assumptions.

### Fair sharing and dominant resources

Fair sharing allocates capacity among pools, tenants, users, or jobs over time. Weighted fairness gives different entitlements. Minimum shares can protect latency; maximum shares and quotas bound one domain. Borrowing unused share improves utilization, but borrowed capacity may later be reclaimed or preempted.

With multiple resources, equal CPU shares can be unfair when one job is memory-heavy and another CPU-heavy. Dominant-resource reasoning compares each user's largest fraction of a resource capacity. It is one policy family, not a universal answer: placement fragmentation, nonfungible devices, topology, licenses, and priorities still matter.

Fairness windows matter. An instantaneous snapshot may show unequal allocation while a tenant recovers a deficit from earlier deprivation. Track allocation and demand over defined intervals, plus slowdown and deadline outcomes.

### Priority, aging, deadlines, and critical path

Strict priority serves emergencies but can starve lower classes. Aging raises effective priority with time. Cap and shape aging so an old massive job does not unexpectedly preempt critical services. Separate user-set priority from protected system classes and authorize who can set each.

Deadline scheduling estimates remaining critical-path work and slack: `slack = deadline - now - predicted_remaining`. Negative slack indicates the current estimate misses the deadline even with immediate service. Predictions need uncertainty and should not justify limitless preemption.

Critical-path-aware scheduling prioritizes work likely to delay a sink. Partition skew complicates stage-level estimates: one hot task may dominate. Speeding noncritical tasks can still free resources or reduce risk, so criticality is an input rather than the sole score.

### Locality and delay scheduling

Data-local placement avoids remote reads; rack/zone locality can reduce network and egress. Waiting briefly may produce a local slot. The scheduler trades expected locality benefit against idle capacity and queue delay.

Use bounded wait levels and fallbacks. Record where data actually resides, not just original block metadata; caches may be lost or stale. For replicated data, balance locality with hotspot risk. For regulated data, residency is a hard feasibility constraint, not a soft locality score.

### Placement, reservation, and binding

A scheduling decision reads a changing cluster snapshot. Between feasibility check and launch, another scheduler or event can consume capacity. Reserve then bind under versioned state or an equivalent optimistic concurrency protocol. If permit or binding fails, unreserve every acquired resource and requeue with reason/backoff.

Stale heartbeats can make dead workers appear feasible. Leases, generation numbers, node conditions, and attempt identities prevent late acknowledgments from reviving obsolete decisions. Reconciliation compares desired scheduler state with observed worker/runtime state.

### Fragmentation and bin packing

Packing tasks tightly can leave whole nodes free and reduce cost, but can also co-locate correlated failures and saturate memory/network. Spreading improves fault and topology distribution but may increase cross-node traffic and idle fragments.

Resource shapes drive fragmentation. If most free nodes have 2 CPU/30 GiB while queued tasks need 8 CPU/8 GiB, large memory totals do not help. Track schedulable demand by shape and constraint, not only aggregate utilization.

### Preemption and eviction

Preemption is justified when protected work cannot otherwise meet policy. Choose victims using priority, fair-share excess, resource usefulness, checkpoint/commit state, work already spent, restart cost, and side-effect safety. Killing four CPU-only tasks does not help a request blocked on a GPU.

Graceful preemption can checkpoint or finish a safe boundary. It costs time and may miss the urgent need. Avoid preempting tasks in atomic commit, non-idempotent effects, or minimum-runtime windows. Charge wasted work and repeated I/O to policy evaluation.

### Dynamic capacity and adaptive parallelism

Elastic systems request or release workers, but new capacity has provisioning delay, quotas, topology, image/data warm-up, and cost. Scaling a stage from observed intermediate bytes can improve task size; it can also create many tiny partitions, exceed network-buffer assumptions, or change output layout.

Adaptive decisions must respect configured min/max parallelism, grouping/partition compatibility, downstream contracts, and retry identity. Record the measurement, decision, plan version, and artifact layout. Autoscaling is not instantaneous admission.

### Scheduler overload and control-plane scale

Millions of tasks create queue, heap, heartbeat, event, metric, and state-store load. An overloaded scheduler can delay offers so badly that workers idle. Batching decisions and events improves throughput but can increase latency and stale snapshots.

Measure scheduling-cycle latency, queue operations, offer-to-launch time, binding failures, stale decisions, event backlog/drops, state size, recovery time, and reconciliation drift. Apply backpressure to submissions rather than accepting unbounded queue growth.

### Observability and evaluation

For each job/stage/task, record blocked, eligible, admitted, queued, reserved, launched, running, and commit times; resource request/limit; feasible-node counts and rejection reasons; chosen locality; queue/pool/tenant; priority and score components; fair-share entitlement/usage/deficit; preemption; retry/speculation; and output identity.

Evaluate on workload traces, adversarial synthetic cases, canaries, and failure injection. Report utilization by resource, queue wait percentiles, slowdown `(completion-arrival)/service`, deadline success, locality distribution, fragmentation, starvation incidents, preempted/wasted work, tail duration, cost, and committed-output latency by tenant/service class.

### Security, governance, and human impact

Scheduling attributes can disclose tenant names, job purpose, sensitive dataset locations, or urgency. Limit visibility and redact logs while preserving accountable decisions. Queue administration, priority elevation, node labels, and preemption permissions require least privilege and audit.

Policy review should ask who receives guarantees, who bears preemption, whether accessibility/public-interest/incident workloads need protected capacity, and whether historical usage entrenches inequity. Provide understandable denial/defer reasons, appeal paths, quota-change governance, periodic disparity analysis, and emergency-policy expiry.

## Definitions and Notation

- `r(t)`: task request vector; `a(n)`: allocatable resource vector on node `n`.
- `r(t) <= a(n)`: componentwise numeric fit, necessary but not sufficient for placement.
- `F(t,n)`: all label, topology, isolation, device, data, policy, and compatibility predicates for task `t` on node `n`.
- **eligible**: dependencies/policy prerequisites satisfied; **admitted**: accepted under capacity/quota policy.
- **service time**: time actually needed with allocated resources; **queue time**: eligible-to-launch delay.
- **slowdown**: elapsed response time divided by isolated or modeled service time, with an explicit floor for tiny jobs.
- **dominant share**: maximum fraction of each cluster resource allocated to a tenant under a declared capacity domain.
- **slack**: deadline minus current time minus predicted remaining duration.
- **fair-share deficit**: time-windowed difference between entitled and received service under a declared policy.
- **reservation**: provisional capacity claim before binding; **binding**: authoritative placement association.
- **preemption victim**: running/reserved work displaced to satisfy higher policy value.
- **locality level**: process/node/rack/zone/region/remote or another declared topology scale.

## Mechanisms, Invariants, or Proof Structure

Audit stage scheduling in this order:

1. Verify exact upstream artifact, data, schema, security, and control prerequisites for eligibility.
2. Define job, stage, task, attempt, queue, tenant, service class, and committed-output identities.
3. Declare every resource dimension, request/limit semantics, labels, topology, devices, isolation, and residency predicate.
4. Apply admission quotas, overload limits, reservations, and gang/minimum-parallelism rules before queue growth becomes unsafe.
5. Compute explainable ordering from fair-share, priority, aging, deadline slack, critical path, locality, and recovery terms.
6. Test concrete-node feasibility and fragmentation; reserve and bind under race-safe versioned state.
7. Launch bounded task waves respecting network, memory, sink, and fair-share concurrency.
8. Define locality waits, backfill protections, preemption victims, checkpoints, cancellation, retry, and speculation charging.
9. Reconcile stale workers, lost leases, duplicate acknowledgments, scheduler restart, dynamic capacity, and adaptive parallelism.
10. Evaluate correctness, queueing, fairness, deadlines, utilization, locality, waste, tails, cost, and human impact by cohort.

The placement proof is conjunctive: graph eligibility, admission, numeric resource fit, categorical/topology feasibility, fresh node state, successful reservation, successful binding, and valid attempt identity must all hold. A score never overrides a failed feasibility predicate.

The policy argument must state objectives and trade-offs. There is no scalar "best schedule" independent of arrival sequence, resource shapes, durations, uncertainty, tenant entitlements, deadlines, data location, failures, and human policy. Compare declared outcomes over representative and adversarial traces.

<!-- bijux-verify: {"id":"resource-aware-stage-selection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ready=('ingest', 'train', 'audit')\nscores=(('train', 21), ('audit', 18), ('ingest', 16))\nselected=('train', 'audit')\ndeferred=(('ingest', 'insufficient_memory'),)\nreserved=(('cpu', 6), ('memory', 20), ('gpu', 1))\n","stderr":""}} -->
```python
capacity = {"cpu": 8, "memory": 24, "gpu": 1}
stages = {
    "ingest": {"request": {"cpu": 4, "memory": 8, "gpu": 0}, "critical": 14, "age": 2},
    "train": {"request": {"cpu": 4, "memory": 16, "gpu": 1}, "critical": 20, "age": 1},
    "audit": {"request": {"cpu": 2, "memory": 4, "gpu": 0}, "critical": 8, "age": 10},
}


def score(stage):
    return stage["critical"] + min(stage["age"], 10)


def first_shortage(request, available):
    for resource in ("gpu", "memory", "cpu"):
        if request[resource] > available[resource]:
            return f"insufficient_{resource}"
    return None


ready = tuple(stages)
ranked = tuple(sorted(stages, key=lambda name: (-score(stages[name]), name)))
available = dict(capacity)
selected = []
deferred = []
for name in ranked:
    request = stages[name]["request"]
    shortage = first_shortage(request, available)
    if shortage is None:
        selected.append(name)
        for resource, amount in request.items():
            available[resource] -= amount
    else:
        deferred.append((name, shortage))

reserved = tuple((resource, capacity[resource] - available[resource]) for resource in capacity)
print(f"ready={ready}")
print(f"scores={tuple((name, score(stages[name])) for name in ranked)}")
print(f"selected={tuple(selected)}")
print(f"deferred={tuple(deferred)}")
print(f"reserved={reserved}")
```

The resource ordering makes the first reported shortage deterministic; another missing dimension could also block placement. The model omits nodes, topology, quotas, fair-share history, duration uncertainty, and binding races.

## Alternatives and Trade-Offs

**FIFO versus fair sharing.** FIFO is simple and predictable for homogeneous work. Fair sharing improves multi-tenant responsiveness but needs weights, windows, demand handling, and audit.

**Strict priority versus aging.** Strict priority protects emergencies but can starve ordinary work. Aging bounds starvation but complicates guarantees and can elevate huge old jobs; cap and authorize it.

**Immediate placement versus locality delay.** Immediate placement reduces idle time. Bounded delay can save transfer/egress and reduce network congestion. Measure opportunity arrival and deadline cost.

**Packing versus spreading.** Packing consolidates free nodes and can reduce cost. Spreading lowers correlated failure and hotspot risk. The right choice varies by resource, topology, recovery, and autoscaling model.

**Incremental versus gang launch.** Incremental launch uses partial capacity and fits ordinary data parallelism. Barrier algorithms may require an atomic gang; partial launch can hold resources without progress.

**Backfill versus reservation.** Backfill improves use of gaps. Reservations protect large/deadline work from perpetual fragmentation. Conservative backfill combines them but depends on duration estimates.

**Preempt versus wait.** Preemption serves urgent work but wastes computation and can amplify I/O/effects. Waiting preserves work but may miss service objectives. Use restart cost and safe boundaries.

**Static versus adaptive parallelism.** Static partitions improve predictability and output stability. Adaptive sizing responds to intermediate data but changes task count, buffer demands, and layout; record decisions and bounds.

## Failure Modes and Misconceptions

**"Ready means runnable."** Dependencies may be satisfied while quota, capacity, node shape, data, credentials, or residency make placement impossible.

**"The cluster has enough total memory."** Fragmentation and per-node/device topology can leave no feasible placement.

**"CPU and memory can be averaged into one score."** Resource vectors require componentwise fit; excess CPU cannot replace missing memory or GPU.

**"Observed low usage permits safe overcommit."** Tasks can later reach requested peaks. Overcommit policy must account for throttling and eviction by resource.

**"FIFO never starves."** A nonfitting head can block feasible work; unprotected backfill can then starve the head indefinitely.

**"Fair means every job gets equal task slots."** Jobs and tenants demand different resources; fairness requires a declared domain, entitlement, window, and metric.

**"Locality should always win."** Waiting for locality can idle capacity or miss deadlines; residency, unlike preference, is a hard constraint.

**"Preemption frees the requested resource."** Victims must release the actual blocking shape/device/location, and restart/side-effect cost matters.

**"Speculation is free tail insurance."** It consumes share, network, cache, sink capacity, and scheduler events and can worsen congestion.

**"More parallelism always shortens a stage."** Tiny tasks, network buffers, scheduler overhead, sink limits, skew, and contention can reverse the benefit.

**"High utilization proves good scheduling."** Queue tails, deadline misses, unfair slowdown, waste, and invalid output can worsen at high utilization.

**"Scheduler decisions are neutral."** Quotas, weights, priorities, and preemption encode organizational choices with disparate effects.

## Worked Examples

### Example 1

An aggregate stage is blocked until every required exchange partition is committed. Ninety-nine percent upstream completion does not make it fully ready under a blocking contract. A pipelined engine may admit consumers earlier, but must budget overlapping resources, bounded buffers, rollback, and producer failure.

### Example 2

A cluster reports 64 free CPU and 256 GiB memory, spread across 32 nodes with 8 GiB free each. A task requesting 4 CPU and 16 GiB fits aggregate totals but no node. Report feasible-node count zero and `insufficient per-node memory`, not `cluster busy`.

### Example 3

FIFO head is a gang needing eight GPUs; only six are free. Small CPU jobs wait behind it. Unprotected backfill improves current utilization but may occupy CPUs on GPU nodes and delay the gang when two GPUs return. Protect the reservation's exact node/resource shape or backfill only work that cannot threaten it.

### Example 4

Tenant A uses half CPU and one quarter memory; tenant B uses one quarter CPU and half memory. Each has dominant share one half. Equal task counts would be meaningless because shapes differ. Device locality and per-node fragmentation can still prevent a feasible next allocation even when dominant shares tie.

### Example 5

An old audit stage has critical work 8 and age 10; a newer ingest stage has critical work 14 and age 2. With age capped at 10, audit scores 18 and ingest 16. This transparent toy policy shows starvation protection, but production units, weights, service classes, and preemption guards need review.

### Example 6

A data-local slot is expected within two seconds and remote transfer would add 30 seconds. Waiting is rational if deadline slack exceeds the risk. After the bounded wait, launch remotely or re-evaluate. Repeatedly resetting the timer on every offer can create accidental infinite delay.

### Example 7

An urgent incident job needs one GPU. Preempting ten CPU-only tasks does not help. The only candidate GPU task is 95 percent complete and checkpointable in 20 seconds. Compare incident slack with checkpoint and restart cost, then record victim reasoning and charge waste to the priority policy.

### Example 8

Two schedulers select the same last slot from stale snapshots. A versioned reservation lets one succeed; the other receives a conflict, unreserves local auxiliary claims, refreshes state, and requeues. Without reconciliation, both may launch and exceed capacity or one may leak a reservation.

### Example 9

Adaptive sizing sees 2 TiB after an exchange and targets 2 GiB per task, suggesting about 1,024 tasks within configured bounds. Before applying it, verify skew, maximum parallelism, upstream subpartition/network-buffer cost, downstream partition contract, output files, and retry identity. Average bytes cannot split one hot key.

### Example 10

A public-benefits report shares a cluster with exploratory analytics. Strict historical usage favors the larger analytics group, while report delays affect claimants. Protected capacity and deadlines need domain, affected-community, accessibility, privacy, security, and operations review; denial reasons and appeals must be visible without exposing sensitive job data.

## Cross-Program Connections

- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies priority queues, online algorithms, matching, bin packing, approximation, and adversarial analysis.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies process scheduling, resource requests/limits, preemption, isolation, and admission control.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects readiness to work/span, barriers, starvation, and synchronization.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies leases, stale state, reconciliation, retries, and scheduler recovery.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies locality topology, congestion, flow limits, and transfer/egress cost.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) connects resource-aware scheduling to query admission, memory grants, and workload management.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) connects service objectives, backfills, dependencies, and data-pipeline operations.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies clusters, quotas, autoscaling, workload identity, observability, and multi-tenancy.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies node trust, residency, priority authorization, isolation, and scheduler audit.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies coupled-resource trade-offs, feedback, capacity models, and emergent risk.

## References

1. Apache Spark. [Job Scheduling](https://spark.apache.org/docs/latest/job-scheduling.html). Accessed 2026-09-03.
2. Apache Spark. [Configuration: Scheduling](https://spark.apache.org/docs/latest/configuration.html). Accessed 2026-09-03.
3. Apache Flink. [Jobs and Scheduling](https://nightlies.apache.org/flink/flink-docs-stable/docs/internals/job_scheduling/). Accessed 2026-09-03.
4. Apache Flink. [Adaptive Batch Execution](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/adaptive_batch/). Accessed 2026-09-03.
5. Apache Flink. [Elastic Scaling](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/elastic_scaling/). Accessed 2026-09-03.
6. Kubernetes. [Scheduling Framework](https://kubernetes.io/docs/concepts/scheduling-eviction/scheduling-framework/). Accessed 2026-09-03.
7. Kubernetes. [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/). Accessed 2026-09-03.
8. Kubernetes. [Pod Priority and Preemption](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/). Accessed 2026-09-03.
9. Apache Hadoop. [YARN Architecture](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html). Accessed 2026-09-03.
10. Apache Hadoop. [CapacityScheduler](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html). Accessed 2026-09-03.
11. Apache Hadoop. [FairScheduler](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/FairScheduler.html). Accessed 2026-09-03.
12. Ali Ghodsi et al. [Dominant Resource Fairness: Fair Allocation of Multiple Resource Types](https://www.usenix.org/conference/nsdi11/dominant-resource-fairness-fair-allocation-multiple-resource-types). NSDI 2011. Accessed 2026-09-03.

## Exercises

### Exercise 1

Run the compact scheduler by hand. Recompute scores, selected stages, first shortage, reserved vector, and explain why the result is not globally optimal evidence.

### Exercise 2

Design eligibility, admission, placement, reservation, binding, and recovery for a join stage with blocking exchanges and stale worker offers.

### Exercise 3

Compare FIFO, weighted fair sharing, dominant-resource reasoning, strict priority, and aging for CPU-heavy, memory-heavy, GPU, and gang workloads.

### Exercise 4

Specify an experiment evaluating locality delay, protected backfill, and preemption under skew, failures, and scheduler overload.

### Exercise 5

Specify named review and evidence for a multi-tenant scheduler serving public-interest, accessibility, regulated, incident, and exploratory workloads.

## Answers to the Exercises

### Answer 1

Scores are train `20+1=21`, audit `8+min(10,10)=18`, and ingest `14+2=16`. Train consumes `(4 CPU,16 memory,1 GPU)`, leaving `(4,8,0)`. Audit consumes `(2,4,0)`, leaving `(2,4,0)`. Ingest needs `(4,8,0)` and the deterministic check reports memory first, though CPU also lacks capacity. Reserved totals are `(6,20,1)`. Greedy scoring ignores future arrivals, nodes/topology, tenant shares, duration uncertainty, data movement, fragmentation, deadlines, and alternative objectives; it is an executable policy illustration, not an optimality proof.

### Answer 2

Mark the join eligible only when every required map-output partition from both inputs is committed under matching schema/key/partition versions. Admission checks tenant quota, queue health, reducer-wave concurrency, shuffle-fetch/network and memory bounds, and residency. Placement tests each task's request against a fresh concrete node plus data/topology/security predicates. Reserve capacity and fetch/slot tokens under generation/version checks, then bind one attempt identity; on conflict or launch failure, unreserve all claims and requeue with backoff. Leases and heartbeats detect lost workers. Scheduler recovery reloads authoritative queue/reservation/attempt state, reconciles workers, invalidates stale generations, and never accepts output from an obsolete or losing attempt.

### Answer 3

FIFO is clear but a nonfitting GPU gang can block all later work. Weighted fair sharing distributes service among tenants but needs resource-aware accounting and can fragment devices. Dominant-resource reasoning balances each tenant's largest capacity fraction for CPU/memory, yet GPUs/topology/gang feasibility remain discrete placement constraints. Strict priority protects incident work but can starve exploratory work and waste victims. Aging bounds starvation but needs caps and service-class guards. A practical policy separates hard feasibility/admission, uses weighted/dominant fair-share deficits within classes, authorizes emergency priority, ages eligible wait, reserves gangs, and reports time-windowed allocation, slowdown, deadlines, fragmentation, and preemption by cohort.

### Answer 4

Replay representative arrival/resource/data-locality traces plus adversarial large-head, hotspot, GPU-fragmentation, synchronized failure, and event-flood cases. Randomize or enumerate bounded locality waits, reservation horizons, backfill limits, and victim rules. Inject worker loss, stale offers, binding conflicts, cache loss, stragglers, autoscaling delay, and scheduler restart. Compare against no-delay FIFO and nonpreemptive baselines. Measure committed-output latency, queue percentiles, slowdown, deadline success, local/rack/remote placement, resource utilization, feasible-node count, fragmentation, gang wait, preempted/wasted work, retries/speculation, event backlog/drops, scheduling-cycle latency, fairness by tenant/class, and confidence across repeated traces. Verify no duplicate launch/commit or policy violation.

### Answer 5

Pin scheduler code/config, queue hierarchy, entitlement/weight/quota, service and emergency classes, aging/deadline/locality/preemption rules, capacity/node labels, residency/trust policy, identity, trace snapshots, duration/resource estimates, and appeal/override procedures. Evaluate disparate queue wait, slowdown, deadline success, preemption, denial, and resource access by relevant workload and affected-user cohorts, including low-volume groups and emergencies. Named review includes service/domain owners, public-interest and affected-community representatives, disability/accessibility specialists, privacy/legal/records/jurisdiction authorities, security/identity, fairness/statistics, platform/runtime/network/capacity operators, incident command, labor/operations where relevant, and independent assurance. Publish comprehensible policy and reasons, protect job metadata, log overrides, expire emergency rules, and provide correction/appeal without weakening isolation.
