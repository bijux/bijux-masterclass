---
module_id: LSDS-052
program: Large-Scale Data Systems Engineering
level: 2
module_number: 52
title: Static and Dynamic Allocation
status: complete
last_verified: 2026-09-04
---

# Static and Dynamic Allocation

## One-Page Review

### Governing question

When should a data workload hold a fixed resource allocation, and when should the platform vary its executors, slots, or parallelism over time without destabilizing execution, losing intermediate state, violating fairness, or making recovery impossible?

### Essential definitions

- **static allocation** grants a declared resource set for a workload's relevant lifetime or execution boundary.
- **dynamic allocation** changes the workload's granted resources in response to demand, supply, policy, or lifecycle events.
- **desired allocation** is the controller's target; **granted allocation** is what the resource manager currently assigns; **ready allocation** is what can execute useful work now.
- An **elastic workload** can make useful progress over a range of allocations; a **rigid/gang workload** needs a specified group simultaneously.
- **scale-up signal** is evidence of useful unmet parallel work, such as sustained runnable backlog rather than total queued records alone.
- **idle timeout** is the evidence window before a controller considers a worker removable.
- **stabilization/hysteresis** prevents small or transient signal changes from causing repeated resize.
- **graceful decommissioning** stops new work, preserves or migrates owned data/state, drains activity, and returns capacity safely.
- **allocation epoch** identifies a generation of grants so stale workers or acknowledgements cannot reclaim or use reassigned capacity.
- **allocation latency** is time from target change through grant, provisioning, registration, restore/warmup, and useful execution.

### Central model, mechanism, or theorem

Let $m(t)$, $g(t)$, and $q(t)$ be desired, granted, and ready worker counts. For minimum $m_{min}$ and maximum $m_{max}$,

$$m_{min}\le m(t)\le m_{max},\qquad q(t)\le g(t)$$

and effective capacity depends on readiness and per-worker service, not the desired count. A dynamic controller observes demand $y(t)$, computes a bounded target, rate-limits increases/decreases, and reconciles grants. Scale-down is safe only after every removable worker's tasks, shuffle blocks, cached partitions, state, transactions, and leases are either disposable, externally available, migrated, or recoverable within the declared objective. Dynamic allocation reallocates existing cluster capacity; node autoscaling changes physical supply and has a separate, slower control loop.

### Critical invariants

- Desired, granted, registered, ready, busy, idle, draining, lost, and released resources are measured separately.
- Allocation remains within workload, queue, tenant, and cluster bounds; a target is not an entitlement to unavailable capacity.
- Scale-up uses useful runnable demand after dependencies, locality, skew, and maximum parallelism—not raw backlog alone.
- Scale-down requires sustained idleness and ownership safety; “no running task” does not prove an executor is disposable.
- Shuffle, cache, broadcast, checkpoint, keyed state, local disk, and external transaction ownership have explicit removal rules.
- Allocation changes preserve stable task/effect identity and fence obsolete workers/epochs.
- Controllers have hysteresis, cooldown, rate limits, and bounded reactions to missing or stale telemetry.
- Fairness and quota remain enforced as workloads expand; elasticity cannot seize protected capacity indefinitely.
- Recovery and catch-up have minimum capacity/headroom even when steady-state utilization is low.
- Every resize decision is explainable, observable, and testable against workload outcomes and cost.

### Common failures

Common failures include equating executor count with useful capacity; scaling on total input lag despite a serial bottleneck; removing executors that own shuffle files or cached/state partitions; using a short idle timeout between narrow stages; scaling up faster than nodes can provision; letting job and node controllers amplify each other; treating worker loss as voluntary removal; restarting a streaming graph repeatedly for tiny gains; ignoring locality and warmup; setting minimum zero when recovery needs capacity; accepting stale release acknowledgements; allocating beyond quota; and celebrating lower executor-hours while completion time, reprocessing, external calls, or tail latency worsen.

### Compact example

A controller starts with two executors, doubles only when backlog exceeds two tasks per executor, caps at eight, and removes one only after two consecutive empty observations. For backlog samples `0,12,12,3,0,0,9,0,0`, the target sequence is `2,4,8,8,8,7,7,7,6`. Hysteresis avoids downscaling on the first empty interval, but this toy controller still ignores task duration, stage width, locality, provisioning latency, and shuffle ownership.

### Connections

[LSDS-051](051-cluster-resource-models.md) defines resource shapes and allocatable capacity. [LSDS-026](026-stage-scheduling.md) and [LSDS-027](027-task-retry-and-speculation.md) define runnable work and attempts. [LSDS-032](032-map-side-buffering-and-spill.md) and [LSDS-048](048-state-snapshots-and-recovery.md) expose removal state. [LSDS-059](../ROADMAP.md) later addresses cluster autoscaling as a separate supply controller.

## Governing Question

Static allocation buys predictability: a job knows its worker count, cached data remains nearby, and no allocation control loop can oscillate. It can also strand resources while stages are serial, inputs arrive slowly, or jobs wait on external systems. Dynamic allocation lets workloads borrow capacity when parallel work exists and return it when demand falls, improving sharing and sometimes cost.

Elasticity is not merely changing a number. New workers must be granted, provisioned, registered, warmed, given code/data, and assigned useful tasks. Removed workers may own intermediate blocks, broadcasts, caches, local state, checkpoint uploads, or open sink transactions. Streaming rescale can restart a graph and redistribute state. The transition itself consumes time and resources.

The governing question is therefore which allocation boundary matches the workload, which signals represent actionable demand, how ownership is preserved during removal, how multiple controllers interact, and which evidence proves that elasticity improves user and cluster outcomes rather than just changing resource graphs.

## Why This Matters

Data workloads change shape over their lifetime. A batch job may have a narrow metadata phase, a wide scan, a large shuffle, and a small final aggregation. A streaming job's arrival rate and key distribution vary while checkpoint and recovery briefly increase demand. A fixed peak allocation wastes capacity outside peaks; a fixed average allocation queues work during them.

Dynamic allocation can reduce queueing by returning idle workers to other tenants, but it may lengthen the elastic job. Cold-start latency can exceed the short stage it was meant to accelerate. Removing a worker can force shuffle recomputation, remote cache reads, or state restoration whose cost exceeds the saved idle time. Allocation policy must include transition cost.

Correctness is also involved. A stale executor can report completion after its capacity or partition has been reassigned. A scale-down can delete the only copy of intermediate data. A restart-based rescale can replay input and external effects. Allocation epochs, durable identities, decommission protocols, and checkpoint-aware recovery are therefore part of the design.

Finally, dynamic allocation changes multi-tenant behavior. A greedy elastic job can consume every returned slot, starving latency-sensitive work. Static reservations can protect services but lower utilization. Quotas, priorities, minimums, maximums, fairness, and preemption define who benefits and who bears transition risk.

## Prerequisites and Retrieval

Review stage scheduling in [LSDS-026](026-stage-scheduling.md), task retry/speculation in [LSDS-027](027-task-retry-and-speculation.md), intermediate materialization in [LSDS-028](028-intermediate-data-materialization.md), shuffle spill in [LSDS-032](032-map-side-buffering-and-spill.md), checkpoint/recovery in [LSDS-047](047-checkpoint-barriers.md) and [LSDS-048](048-state-snapshots-and-recovery.md), backpressure in [LSDS-049](049-backpressure-across-operators.md), and cluster resource vectors in [LSDS-051](051-cluster-resource-models.md).

You should understand DAG readiness, parallelism, resource requests, queues, feedback control, hysteresis, leases/fencing, shuffle/caching, checkpointing, decommissioning, quotas, and basic cost/latency measurement.

## Learning Objectives

After this module, you should be able to:

1. distinguish static, elastic, rigid, opportunistic, and reserved allocation contracts;
2. separate desired, granted, registered, ready, busy, draining, lost, and released capacity;
3. derive scale-up demand from runnable parallel work and service objectives;
4. design bounded ramp-up, idle evidence, hysteresis, cooldown, and stabilization;
5. protect shuffle, cache, broadcast, local state, and transactions during executor removal;
6. rescale stateful streaming and phase-varying batch jobs with explicit transition cost;
7. coordinate job allocation with quotas, fairness, preemption, and node supply;
8. prevent stale allocation events and worker generations from corrupting ownership;
9. evaluate allocation using latency, throughput, recovery, fairness, utilization, and cost; and
10. validate controllers with trace replay, perturbation, failure, and adversarial workload mixtures.

## Core Exposition

### Define the allocation boundary

Specify what changes: task slots inside fixed workers, worker/executor processes, operator parallelism, containers, virtual machines, or physical nodes. These boundaries have different startup, isolation, state movement, and billing costs. A job can dynamically request executors while cluster node count remains fixed.

Specify time scope. Static may mean fixed for a task, stage, job, session, reservation window, or service lifetime. Dynamic may resize only between stages, at checkpoint boundaries, or during execution. Avoid a binary label without boundary and time semantics.

### Classify workload elasticity

An embarrassingly parallel batch stage can use any worker count up to remaining tasks. A barrier stage may need all members. A join may have a limited partition count. A stateful keyed operator can rescale only by moving key groups and restoring consistent state. A coordinator or single output partition is serial.

For each stage/operator define minimum viable parallelism, useful maximum, granularity, malleability while running, gang constraints, state per partition, locality, and transition method. Adding workers beyond useful parallelism creates overhead, not capacity.

### Distinguish allocation states

Desired resources exist in controller state. Requested resources have been sent to a manager. Granted resources have reservations/containers. Registered workers have contacted the application. Ready workers have loaded code/configuration and necessary state. Busy workers perform useful work. Draining workers accept no new work. Released resources are acknowledged reusable.

Measure timestamps and counts at every transition. Otherwise a target of 100 can appear successful while only 40 workers are ready and the rest wait on images, volumes, registration, restore, or scheduler queueing.

### Choose static allocation deliberately

Static allocation is appropriate when demand is stable, startup/restore cost is high, local state/caches are valuable, strict latency needs warm headroom, the workload is rigid, or the platform lacks safe removal. Size it for declared service and recovery objectives rather than tradition.

Static does not require permanent waste. Reservations can be time-bounded; idle capacity can be offered opportunistically with reclaim rules; multiple stages can reuse workers. The key is that the workload's protected grant does not vary unexpectedly.

### Derive actionable scale-up demand

Count runnable tasks after dependencies, retries, locality constraints, partition limits, and admission. A million queued records behind one hot key do not justify a million workers. Estimate useful target from runnable work, task duration, per-worker concurrency, and desired drain/deadline.

A simple batch estimate is $m^*=\lceil W/(T\mu)\rceil$, where $W$ is remaining parallel work, $T$ target time, and $\mu$ sustainable work rate per ready worker, capped by parallelism, quota, and supply. Treat estimates as controller inputs, not guarantees.

### Bound scale-up

Use minimum, maximum, quota, and rate limits. Exponential ramp-up responds quickly to sustained backlog but can overshoot after a transient. Linear or capped increments are gentler but slower. Require backlog age or predicted deadline miss, not one noisy sample.

Allocation latency can make feedback stale. Track request-to-grant, grant-to-register, register-to-ready, and ready-to-first-use. Cancel obsolete requests and tag them by allocation epoch so delayed grants do not exceed the current target.

### Require evidence before scale-down

Idleness is not merely “no task at this instant.” A worker between stages, waiting for locality, holding shuffle blocks, serving cached data, uploading a checkpoint, or completing an external transaction may be valuable or unsafe to remove. Define idle eligibility from work and ownership.

Use sustained idle timeout, downscale stabilization, minimum interval, maximum decrement, and protected minimum. Scaling down more slowly than up often reflects asymmetric transition cost. Consider forecasted near-term stage demand and reservation deadlines.

### Preserve shuffle and intermediate data

An executor may own the only local shuffle blocks needed by future reducers. Removal then causes fetch failure or recomputation. Safe options include an external shuffle service, reliable remote shuffle storage, shuffle-block migration during decommission, retaining executors until dependent shuffle data expires, or accepting measured recomputation.

Track block ownership and dependency lifetime. An idle timeout shorter than the gap between map and reduce phases can thrash. Decommission completion means needed blocks are preserved or explicitly declared reproducible within the objective.

### Treat caches and broadcasts by value

Cached partitions and broadcasts are usually reproducible, but loss increases remote I/O and recomputation. Estimate reuse probability, rebuild bytes/work, locality, and stage criticality. Keep cache-rich executors longer or migrate only when savings exceed cost.

Do not mark cache as correctness state unless it truly is. Conversely, do not assume “cache” is cheap when it contains expensive parsed/reference data used by every short task.

### Rescale stateful streaming explicitly

Changing operator parallelism remaps keyed state. Many engines restore from a completed checkpoint/savepoint, restart tasks, redistribute state, and replay post-checkpoint input. Transition time depends on state bytes/files, backend, network/storage, skew, checkpoint age, and worker readiness.

Set minimum/max parallelism and key-group granularity early. Stabilize signals so small changes do not restart the graph repeatedly. Preserve sink transaction semantics and replay-safe effects. Validate watermarks, timers, in-flight records, and catch-up after resize.

### Use graceful decommissioning

Mark a worker draining and stop new assignments. Resolve in-flight tasks according to their retry/idempotency contract. Migrate or externalize necessary shuffle/cache/state, complete or abort transactions, detach storage/devices, revoke leases, and await bounded acknowledgement. Then release the resource.

A hard kill is failure, not graceful scale-down. It may be acceptable if recovery is designed and cheaper, but count its retries, lost work, data movement, and external effects. Bound drain time; stuck workers need fencing and a failure path.

### Fence allocation generations

Every grant and release carries workload, resource identity, and allocation epoch. The authoritative manager atomically transfers ownership. Workers from older epochs cannot launch tasks, commit partition output, renew leases, or return a resource now owned elsewhere.

Make allocate/release idempotent. Reconcile desired and actual state after coordinator restart, lost acknowledgements, duplicate events, or manager failover. Never infer release solely because the application stopped observing a worker.

### Separate failure from voluntary removal

Failure can occur at any time and may lose local data abruptly. Voluntary removal offers notice and should use the decommission path. Metrics and recovery logic must distinguish them; otherwise a controller can attribute failures to successful cost savings.

If infrastructure revokes opportunistic workers without notice, model them as failure-prone capacity. Place reproducible work there, preserve checkpoints/shuffle elsewhere, and retain sufficient stable capacity for progress.

### Coordinate fairness and quota

An elastic maximum is not a guaranteed allocation. The scheduler grants resources subject to tenant/queue quota, fair share, priorities, reservations, and preemption. A workload's minimum may itself be conditional on admission or reserved capacity.

Avoid hoarding through exaggerated backlog, excessive outstanding requests, slow offer rejection, or idle executors protected by local data forever. Charge allocations consistently and expose why a target was not granted. Multi-tenant experiments must inspect victim outcomes.

### Separate job allocation from node autoscaling

Job allocation redistributes slots/workers from existing supply. Node autoscaling provisions or terminates machines. The job controller may raise demand, which makes pods/containers pending, which triggers node supply. On removal, job decommission should precede node termination.

Different latencies and signals require coordination. If job downscale and node scale-up cross in flight, resources can arrive after demand vanished. Stabilization, cancellable requests, epochs, and shared state prevent oscillation. Do not count desired nodes as ready executors.

### Account for cold starts and locality

New capacity pays queueing, provisioning, image/code distribution, runtime initialization, authentication, dataset listing, broadcast fetch, JIT/cache warmup, state restore, and locality delay. A short stage can finish before workers help.

Use warm pools or static minimums when latency demands them, but include their cost. Compare marginal useful work from a new worker against startup and data movement. Prefer locality-aware grants when remote reads would saturate network/storage.

### Protect recovery capacity

Steady traffic may need four workers while recovery requires twelve to restore state and drain retained input within objective. A controller that learns only steady utilization can downscale away recovery headroom and never catch up after failure.

Declare protected minimums, maximum reachable capacity, source retention, restore concurrency, checkpoint storage limits, and net catch-up rate. Test recovery after the longest allowed downscale and under tenant competition.

### Stabilize interacting controllers

Use hysteresis: different thresholds/windows for up and down. Add cooldown after resize, rate limits, minimum meaningful change, and stabilization that considers pending grants. Avoid synchronized evaluation across thousands of jobs when possible.

Define precedence among manual override, service protection, failure recovery, allocation controller, queue policy, and node autoscaler. Log the observation, rule, bounds, target, epoch, and eventual result for every decision.

### Observe outcome, not just allocation

Measure desired/requested/granted/registered/ready/busy/draining/released resources; runnable/backlog age; stage/operator useful parallelism; startup/restore/decommission duration; lost/recomputed work; shuffle/cache/state bytes moved; throttling; failures; and allocation churn.

Connect these to completion time, streaming lag/freshness, throughput, tail latency, checkpoint health, recovery time, fairness, preemption, utilization, and total cost. Normalize cost per useful output, not executor-hours alone.

### Validate before broad activation

Replay traces while preserving stage dependencies, task durations, locality, failures, and multi-tenant concurrency. Simulate delayed grants, missing telemetry, oscillating demand, scarce quota, rigid jobs, serial bottlenecks, and controller restarts. Trace simulation is only as good as its workload model.

Canary by workload class and pool. Compare static and dynamic baselines with the same workload and cluster pressure. Inject executor loss during shuffle, decommission with active cache/state, checkpoint rescale, manager failover, late grants, and node termination. Retain an immediate static fallback and reconcile leaks before expanding.

## Definitions and Notation

Let $m(t)$ be desired worker count, $g(t)$ granted count, $q(t)$ ready count, $b(t)$ useful runnable backlog, and $c(t)$ busy count. Let $m_{min}$ and $m_{max}$ be policy bounds, $p$ useful parallelism ceiling, $L_a$ allocation latency, $L_d$ decommission latency, and $K$ transition cost.

For remaining parallel work $W$, target completion interval $T$, and sustainable ready-worker service $mu$, an estimate is $m^*=\lceil W/(T\mu)\rceil$, clipped to $[m_{min},\min(m_{max},p)]$. Supply, quota, and placement can make $g<m$; startup/restore can make $q<g$.

Let allocation epoch $e$ order ownership changes. A valid worker action must reference the currently accepted epoch for its resource/partition. Let $I$ be the idle evidence duration and $S$ the stabilization/cooldown interval. These are workload- and platform-specific measured parameters, not universal constants.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. Name the allocation unit and lifetime: slot, executor, container, operator parallelism, VM, or node.
2. Classify each stage/operator as elastic, rigid/gang, phase-malleable, or stateful and declare useful bounds.
3. Separate desired, requested, granted, registered, ready, busy, draining, lost, and released states.
4. Derive actionable demand from runnable parallel work, service objective, per-worker rate, locality, skew, and dependencies.
5. Bound scale-up/down with quota, min/max, hysteresis, stabilization, cooldown, rate limits, and allocation latency.
6. Prove safe removal for tasks, shuffle, cache, broadcasts, state, timers, checkpoints, storage, devices, leases, and sink transactions.
7. Fence allocation epochs and reconcile duplicate, delayed, lost, and reordered manager events.
8. Coordinate job allocation with fairness/preemption and the slower node-supply controller.
9. Reserve/test recovery and catch-up capacity under realistic multi-tenant pressure.
10. Compare end-to-end outcomes and cost against a static baseline with fault and transition injection.

A controller is bounded if targets stay within policy limits and in-flight grants are included in reconciliation. It is safe to release a worker only if no unique non-recoverable obligation remains and stale epochs cannot act. Neither property proves benefit: improvement is empirical and workload-dependent.

## Alternatives and Trade-Offs

- **Fixed workers for job lifetime** maximize predictability and reuse, but strand resources across narrow/idle phases.
- **Stage-boundary resizing** avoids mid-stage disruption and follows DAG width, but cannot react within long stages.
- **Backlog-driven executor allocation** is responsive and broadly applicable, but backlog can misstate useful parallelism.
- **Deadline/work models** connect allocation to outcomes, but require reliable remaining-work and service estimates.
- **Reactive use-all-available mode** is operationally simple for a dedicated cluster, but is unsuitable as a multi-tenant fairness policy by itself.
- **External shuffle service** permits executor removal without losing local shuffle ownership, but adds a privileged stateful service and capacity burden.
- **Shuffle tracking** avoids that service, but can retain executors until dependencies expire and depends on accurate lifecycle tracking.
- **Decommission migration** preserves blocks while returning workers, but consumes network/disk and delays release.
- **Restart-based streaming rescale** gives a clean checkpoint boundary, but causes downtime, state movement, and replay.
- **Opportunistic/revocable workers** improve use of idle capacity, but require failure-tolerant placement and stable progress capacity.
- **Warm pools/minimums** reduce cold-start latency, but consume paid idle capacity.

## Failure Modes and Misconceptions

- “Dynamic allocation is autoscaling.” Job grants and physical node supply are distinct controllers.
- “Target equals capacity.” Grants, readiness, placement, warmup, and restore intervene.
- “Backlog implies parallelism.” Dependencies, hot keys, partition counts, and serial stages cap usefulness.
- “No running task means idle.” Shuffle, cache, state, checkpoint, and transaction ownership remain.
- “Removing an executor is free.” It can cause migration, recomputation, remote I/O, replay, or failure.
- “More executors always finish faster.” Coordination, tiny tasks, skew, I/O saturation, and startup can dominate.
- “Scale down as quickly as scale up.” Removal often has greater correctness and transition cost.
- “Average utilization should set minimum.” Recovery, bursts, and latency may require idle headroom.
- “Executor loss and decommission are equivalent.” Only decommission provides a planned handoff opportunity.
- “A release request returns capacity.” Capacity is reusable only after authoritative acknowledgement and cleanup.
- “Local shuffle is just cache.” It may be the only materialized intermediate copy.
- “Stateful streaming can resize continuously.” Rescale may restart and restore the graph.
- “Minimum is guaranteed.” Without reservation/admission, it can remain an unsatisfied request.
- “Elastic jobs may use all idle capacity.” Quota, fairness, reservations, and reclaimability still apply.
- “Lower executor-hours proves success.” Completion, freshness, recovery, victims, recompute, and output cost matter.
- “Cooldown guarantees stability.” Delay, gain, interacting controllers, and noisy signals still require validation.

## Worked Examples

### Example 1

A fixed 20-executor job uses all workers during a 30-minute scan, five during a 20-minute keyed aggregation, and one during a 5-minute commit. Static allocation buys warm reuse but strands capacity in later phases; stage-boundary resizing can return it if transition cost is below the saved capacity value.

### Example 2

Remaining parallel work is 48,000 record-seconds, target is 120 seconds, and one ready worker sustains 50 records/s. The estimate is $\lceil48000/(120\times50)\rceil=8$ workers, then bounded by stage partitions, quota, minimum, maximum, and current supply.

### Example 3

A backlog of ten million records belongs to one unsplittable hot key. Operator useful parallelism for that key is one, so adding general workers does not increase its service. The remedy may be key decomposition or admission, not allocation.

### Example 4

An executor becomes task-idle after maps but owns shuffle blocks needed in two minutes. A 60-second idle timeout without shuffle preservation removes it, then reducers recompute maps. Shuffle tracking, external storage/service, or a longer dependency-aware timeout prevents the loop.

### Example 5

The desired count rises from 10 to 50. Twenty grants arrive, but only eight workers are ready while twelve pull an image and restore state. Report desired 50, granted 30 total, ready 18, and marginal throughput—not “scaled to 50.”

### Example 6

A streaming rescale from 16 to 32 subtasks restarts from a checkpoint containing 4 TiB of skewed state. Provisioning takes two minutes, restore 18 minutes, and catch-up 25 minutes. A five-minute demand spike cannot benefit; stabilization should compare forecast benefit with the 45-minute transition path.

### Example 7

An old grant for epoch 41 arrives after the controller has downscaled and reassigned the slot at epoch 43. The manager rejects registration/lease renewal for 41. Without epochs, desired bounds can be violated and an obsolete worker can commit output.

### Example 8

Steady state needs four workers, but restoring and draining retained input in one hour requires twelve. Minimum four is economically attractive and operationally unsafe unless twelve workers can be obtained within the recovery budget under cluster contention.

### Example 9

A job controller requests 30 more containers, making pods pending; the node controller starts machines. Demand clears and the job cancels, but nodes arrive six minutes later. Shared visibility of pending/cancelled epochs and stabilization lets the supply controller avoid or promptly reverse obsolete expansion.

### Example 10

This executable illustrates bounded ramp-up and delayed scale-down. It is not a production controller and ignores task service, in-flight grants, allocation latency, ownership, locality, fairness, failure, and interacting supply loops.

<!-- bijux-verify: {"id":"bounded-allocation-controller","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"allocations=(2, 4, 8, 8, 8, 7, 7, 7, 6)\nactions=('hold', 'up', 'up', 'hold', 'hold', 'down', 'hold', 'hold', 'down')\n","stderr":""}} -->
```python
backlog = (0, 12, 12, 3, 0, 0, 9, 0, 0)
minimum = 1
maximum = 8
allocation = 2
idle_intervals = 0
allocations = []
actions = []

for queued in backlog:
    action = "hold"
    if queued > allocation * 2:
        allocation = min(maximum, allocation * 2)
        idle_intervals = 0
        action = "up"
    elif queued == 0:
        idle_intervals += 1
        if idle_intervals >= 2 and allocation > minimum:
            allocation -= 1
            idle_intervals = 0
            action = "down"
    else:
        idle_intervals = 0
    allocations.append(allocation)
    actions.append(action)

print("allocations=" + repr(tuple(allocations)))
print("actions=" + repr(tuple(actions)))
```

## Cross-Program Connections

- **Control systems:** delayed feedback, hysteresis, gain, saturation, cooldown, and coupled loops explain oscillation and convergence.
- **Distributed systems:** leases, fencing, idempotent reconciliation, stale events, coordinator recovery, and ownership transfer protect allocation state.
- **Operating systems:** process/container startup, CPU/memory enforcement, local storage, devices, signals, and cleanup define transition reality.
- **Platform engineering:** schedulers, quotas, worker managers, node provisioners, warm pools, admission, and policy expose elasticity to workloads.
- **Reliability engineering:** protected minimums, decommission, checkpoint/restore, catch-up, fault injection, and recovery objectives bound safe savings.
- **Data engineering:** DAG readiness, partition count, shuffle ownership, cache reuse, keyed state, watermarks, and sinks determine useful elasticity.
- **Economics/FinOps:** marginal benefit, opportunity cost, reservations, billing granularity, recomputation, and victim cost determine net value.
- **Security engineering:** authenticated resource managers, epoch fencing, tenant quotas, isolation, and decommission sanitization prevent capacity abuse.

## References

1. Apache Spark. [Job Scheduling: Dynamic Resource Allocation.](https://spark.apache.org/docs/latest/job-scheduling.html#dynamic-resource-allocation) Current executor request/removal, backlog, idle timeout, cached-executor, and shuffle-preservation behavior.
2. Apache Spark. [Configuration: Dynamic Allocation.](https://spark.apache.org/docs/latest/configuration.html#dynamic-allocation) Current minimum/initial/maximum executors, allocation ratio, sustained backlog, shuffle tracking, decommission, and timeout controls.
3. Apache Spark. [Running on Kubernetes.](https://spark.apache.org/docs/latest/running-on-kubernetes.html) Current executor lifecycle, allocation batch sizing/delay, decommission, persistent storage, and Kubernetes-specific behavior.
4. Apache Spark. [Cloud Integration.](https://spark.apache.org/docs/latest/cloud-integration.html) Current object-store, commit, shuffle, dynamic allocation, and cloud decommission considerations.
5. Apache Flink. [Elastic Scaling.](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/elastic_scaling/) Current adaptive scheduler, declarative requirements, stabilization, reactive mode, restart/restore, and rescale limitations.
6. Apache Flink. [Adaptive Batch Scheduler.](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/adaptive_batch/) Current available-resource parallelism decisions, source inference, data-volume sizing, and bounds for batch jobs.
7. Apache Flink Kubernetes Operator. [Autoscaler.](https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/docs/internals/autoscaler/) Current vertex utilization/lag models, stabilization, restart/rescale, and resource-requirement integration.
8. Apache Hadoop. [Apache Hadoop YARN.](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html) Current resource-manager, application-master, node-manager, container negotiation, monitoring, and scheduling responsibilities.
9. Hindman et al. [Mesos: A Platform for Fine-Grained Resource Sharing in the Data Center.](https://www.usenix.org/conference/nsdi11/mesos-platform-fine-grained-resource-sharing-data-center) Primary resource-offer, fine-grained sharing, framework scheduling, rejection, locality, and failure paper.
10. Verma et al. [Large-scale Cluster Management at Google with Borg.](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) Primary production paper on admission, resource requests, task packing, overcommitment, priority, and availability.
11. Schwarzkopf et al. [Omega: Flexible, Scalable Schedulers for Large Compute Clusters.](https://research.google/pubs/omega-flexible-scalable-schedulers-for-large-compute-clusters/) Primary shared-state scheduler and optimistic concurrent allocation paper.
12. Kubernetes. [Horizontal Pod Autoscaling.](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) Current ratio-based replica control, missing metrics, stabilization windows, tolerance, and scale policy behavior.
13. Kubernetes. [Node Autoscaling.](https://kubernetes.io/docs/concepts/cluster-administration/node-autoscaling/) Current distinction between workload demand, unschedulable pods, node provisioning/consolidation, disruption, and physical supply.

## Exercises

### Exercise 1

A batch stage has 72,000 CPU-record-seconds remaining, a 180-second target, and measured per-ready-worker rate 80 records/s. Estimate worker target, then apply minimum 4, maximum 48, stage parallelism 32, and quota 20.

### Exercise 2

A controller sees backlog samples `0, 30, 30, 2, 0, 0`. It starts at 4, doubles when backlog exceeds three tasks per executor, caps at 16, and removes two after two consecutive zero samples. Compute targets and discuss missing production state.

### Exercise 3

Design the safe removal decision for an executor with no running tasks, 200 GiB of shuffle blocks, 40 GiB of cached reference data, a checkpoint upload, and an open sink transaction.

### Exercise 4

A streaming job uses eight workers steadily, needs 24 during recovery, has 12-minute node provisioning, 18-minute restore, live arrival 50,000/s, and recovered service 70,000/s. A failure leaves 24 million records. Estimate ideal backlog drain and total recovery path, then identify omitted constraints.

### Exercise 5

Design a production experiment comparing static and dynamic allocation for mixed batch and streaming workloads. Include demand signals, state machine, bounds, ownership, epochs, multi-tenant policy, interacting node supply, failures, evidence, canary, and rollback.

## Answers to the Exercises

### Answer 1

$m^*=\lceil72000/(180\times80)\rceil=\lceil5\rceil=5$. The minimum is 4, while maximum, stage parallelism, and quota caps are 48, 32, and 20; none reduces five. Request five ready workers, while reporting separately any grant/readiness delay and uncertainty in the rate estimate.

### Answer 2

At backlog 0 the target remains 4 with one idle sample. At 30, since $30>4\times3$, it rises to 8. The next 30 exceeds $8\times3$ and rises to 16. Backlog 2 holds 16 and resets idle evidence. The first zero holds 16; the second removes two, yielding targets `(4,8,16,16,16,14)`. A real controller needs runnable rather than raw backlog, outstanding grants, stage limits, task duration, allocation latency, quota, locality, ownership, drain state, failures, and cooldown.

### Answer 3

Do not classify the executor as safely idle. Determine whether every shuffle block is externally served, replicated/migrated, or recomputable within objective; estimate cache rebuild and future reuse; wait for or safely transfer/abort the checkpoint upload; complete, abort, or recover the sink transaction under a fenced epoch. Stop new assignments, drain bounded in-flight actions, revoke leases, preserve required data, record ownership outcomes, and release only after authoritative acknowledgement. If deadline expires, treat forced loss as a tested failure path and account for recomputation/recovery.

### Answer 4

Net drain at recovered capacity is $70{,}000-50{,}000=20{,}000$/s, so ideal drain is $24{,}000{,}000/20{,}000=1{,}200$ seconds, or 20 minutes. Adding 12-minute provisioning and 18-minute restore gives an optimistic 50-minute path. It omits grant queueing, image/startup, state skew, storage/network limits, checkpoint/retry load, warmup, watermark/window bursts, sink quotas, node failures, tenant competition, and whether 24 workers actually deliver 70,000/s.

### Answer 5

Use matched trace-replay and live canary cohorts preserving DAG dependencies, partitions, task durations, locality, shuffle/cache/state, failures, and tenant concurrency. Define useful runnable backlog/deadline signals; desired/requested/granted/registered/ready/busy/draining/released states; min/max/quota; asymmetric ramp; idle ownership rules; stabilization/cooldown; allocation epochs; and idempotent reconciliation. Provide external shuffle, tracking, migration, or explicit recomputation policy; checkpoint-safe streaming rescale and replay-safe sinks; stable recovery minimum; and graceful decommission with bounded forced-failure fallback. Coordinate pending/cancelled demand with node provisioning/consolidation and measure victims under fairness/preemption. Inject delayed/duplicate grants, manager restart, executor/node loss, shuffle fetch, state restore, open transaction, correlated peaks, and stale telemetry. Compare completion/freshness/tails, ready latency, churn, moved/recomputed work, recovery, fairness, utilization, and cost per useful output. Canary by workload/pool, gate expansion on stated regressions, keep static configuration as rollback, and reconcile leaked allocations before wider rollout.
