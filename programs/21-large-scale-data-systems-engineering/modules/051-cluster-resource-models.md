---
module_id: LSDS-051
program: Large-Scale Data Systems Engineering
level: 2
module_number: 51
title: Cluster Resource Models
status: complete
last_verified: 2026-09-04
---

# Cluster Resource Models

## One-Page Review

### Governing question

How should a cluster represent machine capacity and workload demand so that admission, placement, isolation, fairness, and capacity decisions correspond to the resources tasks actually need?

### Essential definitions

- A **resource model** defines resource types, units, capacity, demand, allocation, consumption, constraints, and enforcement semantics.
- A **capacity vector** lists a node's quantities across dimensions such as CPU, memory, storage, network, and accelerators.
- **allocatable capacity** is physical capacity minus system reservations, unavailable devices, and required safety margin.
- A **request** is capacity used for admission and placement; a **limit** is an enforcement ceiling; **usage** is observed consumption.
- A **task shape** is its request vector plus qualitative constraints such as topology, device type, persistence, and exclusivity.
- A **compressible resource** can be throttled while preserving the process, such as CPU time; exhaustion of a **non-compressible resource**, such as memory, often requires denial or termination.
- A **scalar resource** is represented by quantity; a **discrete resource** consists of indivisible instances; a **range/set resource** carries identities such as ports or device IDs.
- **fragmentation** is free capacity that cannot satisfy pending shapes because it is split across dimensions, nodes, topology, or time.
- **overcommit** admits requests beyond a physical dimension under an explicit statistical and enforcement policy.
- A workload's **dominant share** is its largest fraction of total capacity consumed in any modeled resource dimension.

### Central model, mechanism, or theorem

For node $n$, let physical capacity be $C_n$, platform reservation $S_n$, and safety headroom $H_n$. Its allocatable vector is

$$A_n=C_n-S_n-H_n$$

For task $j$ with request vector $r_j$, a necessary scalar fit condition on node $n$ is

$$\sum_{j\in P_n} r_{j,d}+r_{new,d}\le A_{n,d}$$

for every modeled dimension $d$. It is not sufficient: device identity, NUMA/socket alignment, zone/rack, storage attachment, ports, affinity, gang size, duration, and policy can invalidate the placement. A sound model keeps request, limit, reservation, allocation, and observed usage distinct and connects every promised dimension to measurement and enforcement.

### Critical invariants

- Resource names and units are canonical; binary/decimal bytes, cores/millicores, rates, totals, and device counts are not mixed.
- Allocatable excludes operating-system, daemon, eviction, failure, and performance headroom rather than advertising nameplate capacity.
- Admission uses declared or inferred requests, never instantaneous low usage alone.
- Every hard promise has an enforcement mechanism and every enforced resource has observable accounting.
- Aggregate fit is checked per node and per indivisible/topological constraint; cluster-wide free totals do not prove placement.
- Requests reflect simultaneous working-set demand at the scheduler's time scale, including startup, shuffle, spill, checkpoint, and recovery peaks.
- Overcommit has bounded factors, protected workload classes, reclaim/throttle/evict behavior, and overload evidence.
- Heterogeneous devices retain type, capability, locality, health, sharing, and lifecycle identity.
- Reservation, allocation, actual consumption, unavailable capacity, and reclaimable slack reconcile for each dimension.
- Model changes are versioned, simulated against traces, canaried, and reversible.

### Common failures

Common failures include treating every task as one slot; advertising physical rather than allocatable memory; interpreting CPU requests as usage caps; scheduling from averages while ignoring coincident peaks; declaring disk bytes but ignoring IOPS/bandwidth; treating GPUs as identical integers; summing free resources across nodes; ignoring task duration and gangs; overcommitting non-compressible memory without an eviction policy; trusting mutable labels as hardware truth; omitting system and recovery work; letting stale inventory admit dead devices; and optimizing utilization while stranded capacity, queue delay, throttling, OOMs, or tail latency worsen.

### Compact example

Two nodes each have 8 CPU and 16 GiB allocatable. After placing one `(6 CPU, 4 GiB)` task on the first and one `(2 CPU, 12 GiB)` task on the second, the cluster has 8 CPU and 16 GiB free in aggregate. Yet a new `(4 CPU, 8 GiB)` task fits neither node: one lacks CPU and the other lacks memory. The resource total is sufficient; the vector placement is fragmented.

### Connections

[LSDS-004](004-data-locality.md) adds location value, [LSDS-006](006-stages-tasks-and-dependencies.md) defines executable units, [LSDS-039](039-skewed-keys-and-heavy-hitters.md) changes realized demand, and [LSDS-049](049-backpressure-across-operators.md) exposes capacity deficits. [LSDS-052](../ROADMAP.md) uses this model for allocation behavior.

## Governing Question

A scheduler sees neither “a machine” nor “a job” directly. It sees representations: inventories of allocatable resources, requests attached to runnable units, placement constraints, ownership and priority, and telemetry that may lag reality. Every scheduling decision is only as meaningful as those representations.

A one-dimensional slot model works only when workloads and machines are sufficiently uniform. Data systems are not. A scan task may be CPU-light and storage-bandwidth-heavy; a hash join can require large non-compressible memory; shuffle stresses network and disk; a model task may need a particular accelerator and local high-bandwidth memory; a stateful service may require a volume in one zone. Treating these as equal slots creates interference and stranded capacity.

The governing question is how to choose dimensions and semantics rich enough for safety and useful placement without building an unmeasurable optimizer. The answer must connect physical inventory, platform reservation, requests, limits, runtime use, topology, time, QoS, enforcement, and evidence.

## Why This Matters

Resource models sit beneath admission, fairness, bin packing, locality, preemption, and autoscaling. If memory is underrequested, placement appears efficient until simultaneous working sets cause eviction or OOM. If requests are inflated, utilization appears low while jobs wait. If network is invisible, a CPU-balanced placement can collapse a rack uplink.

The model also determines what policy can express. Scalar CPU and memory cannot represent “two mutually connected accelerators on the same NUMA node,” a licensed token, or a volume accessible in one zone. Labels can filter nodes but do not automatically reserve consumable capacity. A scheduler needs both quantitative resources and qualitative constraints.

Accounting affects fairness and cost. A CPU-heavy tenant and memory-heavy tenant cannot be compared fairly using task counts. Dominant-resource reasoning considers each tenant's largest capacity share, while cost attribution may weight dimensions by actual scarcity and price. Neither works if requests and inventory are unreliable.

Finally, scheduling safety differs from runtime performance. A task can fit its request yet throttle at its limit, miss a deadline because of noisy I/O, or allocate more memory than requested. Models must be calibrated against outcomes and state their guarantees rather than treating admission as proof of performance.

## Prerequisites and Retrieval

Review data locality in [LSDS-004](004-data-locality.md), task graphs/stages in [LSDS-005](005-distributed-task-graphs.md) and [LSDS-006](006-stages-tasks-and-dependencies.md), cluster failure assumptions in [LSDS-009](009-cluster-failure-assumptions.md), spill/shuffle in [LSDS-032](032-map-side-buffering-and-spill.md) through [LSDS-034](034-hash-based-shuffle.md), and backpressure/recovery in [LSDS-048](048-state-snapshots-and-recovery.md) and [LSDS-049](049-backpressure-across-operators.md).

You should understand vectors, bin packing, queues, percentiles, working sets, CPU scheduling, virtual memory, cgroups, storage IOPS/throughput, network topology, NUMA, accelerators, quotas, reservations, and basic cluster telemetry.

## Learning Objectives

After this module, you should be able to:

1. specify physical, reserved, unavailable, headroom, and allocatable capacity vectors;
2. distinguish requests, limits, allocations, reservations, usage, and outcomes;
3. classify resources by divisibility, compressibility, persistence, topology, identity, and renewability;
4. test multidimensional node fit and explain resource fragmentation;
5. represent accelerators, ports, volumes, licenses, and topology-dependent resources;
6. reason about overcommit, reclaim, throttling, eviction, and QoS by dimension;
7. calibrate requests for batch, streaming, shuffle, stateful, and recovery phases;
8. connect resource accounting to fairness, bin packing, locality, and cost;
9. detect stale inventory, unmodeled bottlenecks, and request-quality failures; and
10. validate a model with trace replay, adversarial workload mixtures, canaries, and conservation checks.

## Core Exposition

### Begin with workload phases and promises

Inventory what the platform promises: admission safety, isolation floor, maximum burst, device exclusivity, deadline feasibility, or merely best effort. Then decompose workloads into phases. Input scan, build-side materialization, shuffle fetch, aggregation, checkpoint, restore, and compaction have different shapes.

A request should describe capacity needed simultaneously over the scheduling interval, not lifetime work. CPU-seconds is useful for cost prediction but cannot alone place a task that needs four cores now. Peak working set matters for memory; bytes, IOPS, queue depth, and bandwidth can all matter for storage.

### Construct allocatable capacity

Machine inventory starts with physical CPU topology, memory by NUMA domain, storage devices/capacity/performance, NICs/links, accelerators, and attached resources. Subtract firmware/hardware reservations, operating system, node agents, logs/images, control work, unavailable/cordoned devices, eviction threshold, failure margin, and promised performance headroom.

Do not use one uniform percentage without evidence. System CPU and memory can scale differently with pod/task count, network rate, device plugins, logging, and checkpoint traffic. Allocatable should change through an authenticated, versioned inventory path and become unschedulable when health is uncertain.

### Keep request, limit, usage, and outcome separate

The scheduler reserves requests to decide fit. A runtime enforces some limits. Usage samples what happened. Outcome records throttling, reclaim, eviction, OOM, deadline, and application performance. These quantities answer different questions.

Low current usage does not make a request disposable if it protects a future burst. A CPU limit may throttle; a memory limit commonly leads to allocation failure or termination. A missing request may cause the scheduler to treat real demand as zero even when a runtime limit exists. Document platform-specific semantics.

### Model resources by behavior

CPU time is divisible and renewable; contention can be time-shared and throttled. Memory capacity is divisible in units but non-compressible at exhaustion. Disk space persists until deletion, while IOPS and bandwidth renew over time. Ports and device instances are discrete identities. Network capacity belongs to paths and shared failure domains, not only nodes.

For every dimension record unit, accounting interval, granularity, divisibility, reclaimability, compressibility, oversubscription policy, enforcement point, topology scope, health source, and observation delay. The same label “GPU” can hide model, memory, interconnect, slice, driver, and sharing differences.

### Test vector fit per node

Represent node $n$ by allocatable vector $A_n$ and task $j$ by request vector $r_j$. The componentwise inequality is a first filter. Then apply predicates for architecture, operating system, zone, storage accessibility, device capability, affinity/anti-affinity, ports, security/isolation, maintenance, and policy.

Cluster totals cannot be substituted for node fit. Ten free CPUs distributed one per node cannot place an eight-CPU task. CPU on one node and memory on another cannot be combined for an ordinary process. Co-scheduled gangs require simultaneous fit for several tasks.

### Understand task shapes and fragmentation

Normalize each request as fractions of candidate-node or cluster capacity to see its shape. CPU-heavy and memory-heavy tasks can complement each other. Identical large shapes can strand slivers. Discrete accelerators and topology constraints create fragmentation even when scalar utilization looks low.

Measure pending demand that is infeasible despite free aggregate capacity, free vectors per node, dominant residual dimension, largest fit-able shape, device/topology fragmentation, and unusable tail capacity. Compaction through migration/preemption has disruption cost; preventing pathological placement is often cheaper.

### Represent heterogeneity truthfully

Nodes differ by CPU generation/instruction set, memory bandwidth, NUMA layout, local storage, network, accelerators, failure domain, energy profile, and performance variability. A resource model can expose named classes/capabilities, quantitative benchmark tiers, or device instances.

Avoid encoding every benchmark as a permanent type. Too little detail causes unpredictable performance; too much creates tiny pools and queueing. Use durable workload-relevant capabilities, verified node features, and measured performance classes with compatibility rules.

### Model devices and topology

Accelerators, NICs, and local disks may be indivisible, partitionable, or time-shared. Allocation must preserve identity and ensure that the runtime configures exactly the granted device. Dynamic allocation can select among device claims while accounting for node accessibility.

Topology matters when CPU, memory, PCIe device, and NIC should align on one NUMA/socket path. A scalar count of two GPUs does not prove peer-to-peer connectivity. Represent allowed combinations or have a device/topology allocator return a feasible claim that the scheduler incorporates atomically.

### Include storage and network explicitly where useful

Local ephemeral storage needs capacity accounting for writable layers, scratch, shuffle/spill, logs, and images. Capacity alone does not protect IOPS or bandwidth. Persistent volumes add attachment limits, topology, access mode, performance class, and lifecycle ownership.

Network modeling is difficult because flows share paths. At minimum expose network-intensive workload classes, rack/zone locality, interface capabilities, and observed congestion. More detailed models may reserve bandwidth or use topology-aware placement, but stale traffic forecasts can mislead. Pair admission with runtime congestion control.

### Account for overhead and sidecars

The schedulable unit consumes more than the user task: runtime, sidecars, sandbox, daemon overhead, page cache, buffers, shuffle services, logs, image storage, and per-task control metadata. Decide which overhead belongs to node reservation and which is added to each task request.

Avoid double subtraction. If pod/task overhead is included in the schedulable request, do not also bury it in a broad node reserve. Validate accounting by reconciling allocations and actual host consumption under different task counts.

### Define resource time semantics

Capacity resources describe simultaneous occupancy; renewable-rate resources describe service per interval; work estimates describe integral demand. Duration affects when capacity returns and whether backfill can use a gap. Reservations may start later and require advance feasibility.

Batch stages can release executors or change shape. Streaming tasks may hold stable slots but spike during checkpoint/recovery. Gang jobs need all members together. A static peak request is safe but wasteful; phase-aware resizing improves utilization only with trustworthy transitions and fallback capacity.

### Overcommit deliberately

Overcommit is safest for statistically multiplexable, reclaimable, or throttled resources. CPU requests can exceed continuously used CPU when limits/weights protect critical classes. Memory overcommit is riskier because coincident working sets force reclaim, eviction, or OOM. Device and huge-page resources are often non-overcommittable.

Define overcommit factor per pool/class/dimension, protected reservations, burst credits, reclaim priority, throttling/eviction sequence, and emergency margin. Evaluate joint peaks, not independent per-workload percentiles whose correlation is unknown. Recovery, retry, and diurnal synchrony can make all tenants peak together.

### Express QoS and reclaimability

Map request/limit relationships and priority into explicit QoS: guaranteed, burstable, or best effort, for example. State what can be throttled, reclaimed, checkpointed, migrated, preempted, or killed; how quickly capacity becomes usable; and what data/state is lost.

Reclaimable capacity is not immediately allocatable hard capacity. A victim may require grace, checkpoint, termination, volume detach, and cleanup. Model reclaim latency and uncertainty when admitting urgent work.

### Connect accounting to fairness

For total resource vector $R$ and user allocation $x_i$, dominant share is $\max_d(x_{i,d}/R_d)$. Dominant Resource Fairness equalizes dominant shares under its assumptions and offers useful multi-resource properties. It is not a complete production scheduler: placement, heterogeneity, locality, priorities, indivisible resources, and time remain.

Quota, entitlement, limit, and current allocation are distinct. Fairness based on inaccurate requests can reward inflation or punish efficient users. Measure both reserved share and actual consumption/outcomes, but do not remove guarantees merely because a task was temporarily idle.

### Connect resource model to scheduling architecture

A monolithic scheduler can evaluate global placement but faces scalability and evolvability trade-offs. Two-level offers let a cluster manager allocate resources while frameworks choose tasks, but information hiding and offer rejection can delay placement. Shared-state schedulers use optimistic concurrency and must resolve conflicts. Central optimizers can encode rich cost models if they decide quickly enough.

Regardless of architecture, define the authoritative inventory, allocation transaction, stale-read behavior, conflict/fencing, reconciliation, and recovery. A mathematically rich resource vector does not help if concurrent schedulers double-allocate it.

### Calibrate requests from evidence

Collect phase-aware usage distributions by stable workload class: CPU runnable time/throttling, memory working set/OOM, disk capacity/IOPS/bandwidth/latency, network bytes/retransmits/queueing, device utilization/memory, and application throughput/latency. Preserve concurrency and correlation.

Recommendations should include confidence, minimum samples, safety margin, and last observation. Cold starts and new versions need conservative defaults. Detect chronic underrequest, overrequest, limit throttling, unused allocation, and class drift. A recommender advises; policy determines whether changes are automatic.

### Observe model error

Track requested, allocated, reserved, unavailable, reclaimable, and used quantities per node/pool/tenant/dimension. Track pending reasons, fit failures, scheduling attempts, fragmentation, offer rejection, allocation conflicts, inventory age, throttling, pressure, eviction/OOM, device errors, and SLA outcomes.

Reconcile capacity: physical equals reserved plus unavailable plus allocatable; allocatable equals allocated requests plus free request capacity under stated rounding. Usage need not sum to allocation, but unexplained host consumption should be attributed to platform overhead or model error.

### Evolve the model safely

Adding a dimension can make formerly schedulable work pending; changing units can over-admit by orders of magnitude. Version resource schemas, defaulting, capability discovery, and workload declarations. Reject ambiguous quantities and unknown hard requirements.

Replay representative traces through the proposed model and compare feasibility, queue delay, utilization, fragmentation, locality, churn, and simulated overload. Canary pools and workload classes, monitor model error, preserve rollback, and migrate durable reservations deliberately.

## Definitions and Notation

Let dimensions be $D$. Node $n$ has physical capacity $C_{n,d}$, system reservation $S_{n,d}$, safety headroom $H_{n,d}$, unavailable capacity $U_{n,d}$, and allocatable $A_{n,d}=C_{n,d}-S_{n,d}-H_{n,d}-U_{n,d}$. Task $j$ declares request $r_{j,d}$ and possibly limit $l_{j,d}$; observed use is $u_{j,d}(t)$.

Let $P_n$ be tasks placed on node $n$. Scalar feasibility requires $\sum_{j\in P_n}r_{j,d}\le A_{n,d}$ for all $d$, subject to rounding. Predicate $F(j,n)$ represents qualitative/topological feasibility. Gang feasibility additionally requires a simultaneous assignment for all members.

For cluster total $R_d=\sum_n A_{n,d}$ and tenant allocation $x_{i,d}$, dominant share is $s_i=\max_d(x_{i,d}/R_d)$. Fragmentation is not one universal scalar; report residual vectors and pending shapes, or define a workload-specific fraction of free capacity that cannot serve the pending distribution.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. Enumerate workload phases and the promises admission/placement must support.
2. Inventory physical resources, topology, health, reservations, overhead, and headroom in canonical units.
3. Classify dimensions by scalar/discrete/set, divisible/indivisible, compressible/non-compressible, renewable/persistent, exclusive/shareable, and local/path scope.
4. Define request, limit, reservation, allocation, observed usage, and outcome independently.
5. Test componentwise node fit, then identity, topology, affinity, security, storage, port, and gang predicates.
6. Model duration, phase changes, reclaim latency, and recovery peaks.
7. State overcommit factors, QoS, enforcement, reclaim/evict order, and failure behavior per dimension/class.
8. Connect allocation accounting to quota, fairness, cost, locality, and scheduler concurrency.
9. Reconcile physical/reserved/unavailable/allocatable/allocated/free capacity and attribute host use.
10. Validate with trace replay, workload mixtures, fragmentation cases, stale inventory, overload, failure/recovery, canary, and rollback.

Componentwise inequalities prove only scalar capacity safety if inventory is current and allocation is atomic. They do not prove topology feasibility or performance. Conversely, aggregate cluster capacity can satisfy a request vector while no node can: the compact example is a constructive counterexample. Any scheduling proof must therefore state placement granularity and predicates.

## Alternatives and Trade-Offs

- **Fixed slots** are simple and predictable for uniform workloads, but waste capacity and hide heterogeneous bottlenecks.
- **CPU/memory vectors** capture major constraints with manageable complexity, but omit storage, network, devices, topology, and time.
- **Extended named resources** allow devices/licenses to be counted, but integer counts may hide capability and connectivity.
- **Dynamic device claims** express instance selection and topology more accurately, but add lifecycle, driver, and scheduling coordination.
- **Hard reservations** improve safety and latency predictability, but lower utilization when demand is bursty.
- **Overcommit** improves utilization under statistical multiplexing, but correlated peaks create throttling, eviction, and tail risk.
- **Peak static requests** are safe for variable phases, but strand resources; phase-aware resize improves packing while adding transition risk.
- **Centralized global optimization** can consider rich constraints, but must control decision latency and availability.
- **Two-level offers** preserve framework-specific scheduling, but lose global task detail and may incur rejection cycles.
- **Shared-state schedulers** scale decision making, but require optimistic concurrency, conflict control, and reconciliation.
- **Request-based fairness** preserves declared guarantees; usage-based accounting reflects consumption but can penalize burst entitlement or reward underdeclaration.

## Failure Modes and Misconceptions

- “One task equals one slot.” Task shapes differ across CPU, memory, I/O, network, devices, and topology.
- “Nameplate capacity is schedulable.” System services, failures, eviction threshold, and performance margin consume it.
- “Request means current use.” It is a scheduling reservation; usage is measured separately.
- “Limit means reservation.” A ceiling does not necessarily reserve capacity.
- “Free cluster totals prove fit.” Resources can be fragmented across nodes or constraints.
- “CPU and memory behave alike.” CPU is normally throttled; memory exhaustion often terminates or evicts.
- “Disk space represents storage performance.” IOPS, throughput, queueing, and attachment can dominate.
- “All GPUs are interchangeable.” Model, memory, partition, interconnect, locality, software, and health matter.
- “A node label reserves a consumable resource.” Labels filter; accounting must prevent double allocation.
- “Average use sizes a request.” Concurrent peaks, startup, checkpoint, recovery, and skew matter.
- “Overcommit creates capacity.” It accepts overload risk and needs enforcement/reclaim policy.
- “Idle guaranteed capacity is free.” Reusing it requires reclaim within the promised time.
- “Dominant-resource fairness solves scheduling.” It does not solve placement, locality, heterogeneity, priority, or time.
- “High utilization proves model quality.” Queue delay, fragmentation, throttling, OOM, and tail latency can worsen.
- “Inventory is truth forever.” Health and topology become stale; admission needs freshness/fencing.
- “More dimensions always improve scheduling.” Unmeasured or unstable dimensions add false precision and fragmentation.

## Worked Examples

### Example 1

A 64-GiB node reserves 6 GiB for OS/agents, 4 GiB eviction headroom, and 2 GiB for unavailable hardware mapping. Allocatable memory is $64-6-4-2=52$ GiB, not 64 GiB.

### Example 2

Four tasks request 1 CPU each and limit at 2 CPU. Placement reserves 4 CPU; observed use might be 1.5 CPU total; runtime demand can burst toward 8 CPU and throttle if only 6 CPU is physically available. The three values answer different questions.

### Example 3

Two 8-CPU/16-GiB nodes hold shapes `(6,4)` and `(2,12)`. Free vectors are `(2,12)` and `(6,4)`. A `(4,8)` task fails both despite aggregate free `(8,16)`: multidimensional fragmentation.

### Example 4

A node advertises four accelerator integers, but two are incompatible models and only one pair shares the required interconnect. A task needing two connected model-X devices needs a typed topology-aware claim, not count `2`.

### Example 5

A shuffle task requests 2 CPU, 4 GiB memory, and 100 GiB scratch. Its 100 GiB fits disk capacity, yet 500 concurrent tasks saturate IOPS and bandwidth. Adding an I/O class or rate-aware admission may be more useful than falsely guaranteeing exact per-task IOPS.

### Example 6

At steady state a stream task uses 3 GiB, but restore needs 9 GiB while rebuilding indexes. A 4-GiB request passes normal dashboards and fails every recovery. Phase-aware reservation or a recovery-sized request protects recoverability.

### Example 7

Cluster allocatable is 100 CPU and 1,000 GiB. Tenant A holds 40 CPU/100 GiB, so its shares are 0.40 and 0.10 and dominant share 0.40. Tenant B holds 20 CPU/400 GiB, with shares 0.20 and 0.40 and the same dominant share.

### Example 8

A best-effort batch task uses idle CPU on a guaranteed service node. The scheduler may call that capacity reclaimable, but urgent admission must include detection, grace, checkpoint, kill, and cleanup latency. Until reclaimed, it is not equivalent to free hard capacity.

### Example 9

An inventory agent stops reporting a failed accelerator but the scheduler cache still advertises it. New tasks repeatedly bind and fail. A freshness deadline makes stale device capacity unavailable; reconciliation revokes allocations and alerts on the capacity discrepancy.

### Example 10

This executable first-fit fixture checks scalar vector placement and exposes fragmentation. It does not model limits, usage, topology, discrete device identity, concurrency, fairness, preemption, time, or runtime enforcement.

<!-- bijux-verify: {"id":"multiresource-fragmentation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"free=((2, 12), (6, 4)) aggregate=(8, 16)\nrequest=(4, 8) fits=() fragmented=True\n","stderr":""}} -->
```python
capacity = ((8, 16), (8, 16))
allocated = ((6, 4), (2, 12))
request = (4, 8)

free = tuple(
    (node[0] - used[0], node[1] - used[1])
    for node, used in zip(capacity, allocated)
)
aggregate = (sum(item[0] for item in free), sum(item[1] for item in free))
fits = tuple(
    index for index, item in enumerate(free)
    if request[0] <= item[0] and request[1] <= item[1]
)
aggregate_fits = request[0] <= aggregate[0] and request[1] <= aggregate[1]
fragmented = aggregate_fits and not fits

print("free=" + repr(free) + " aggregate=" + repr(aggregate))
print("request=" + repr(request) + " fits=" + repr(fits) + " fragmented=" + repr(fragmented))
```

## Cross-Program Connections

- **Operating systems:** CPU scheduling, virtual memory, cgroups, NUMA, devices, page cache, and I/O control determine enforcement reality.
- **Distributed systems:** inventory consistency, leases, fencing, optimistic concurrency, failure domains, and reconciliation protect allocations.
- **Algorithms:** multidimensional bin packing, matching, min-cost flow, online decisions, and approximation expose quality/latency trade-offs.
- **Platform engineering:** workload APIs, quotas, resource classes, schedulers, admission, node agents, autoscalers, and telemetry operationalize the model.
- **Reliability engineering:** headroom, overload, reclaim, recovery peaks, pressure signals, eviction, and canaries turn capacity into service outcomes.
- **Security engineering:** authenticated inventory, tenant-scoped quota, device isolation, unforgeable claims, and anti-inflation policy protect shared capacity.
- **FinOps:** reservations, allocations, use, scarcity, stranded capacity, and workload outcomes support explainable cost attribution.
- **Data engineering:** scan, shuffle, join, spill, state, checkpoint, and compaction phases supply workload-specific shapes.

## References

1. Verma et al. [Large-scale Cluster Management at Google with Borg.](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) Primary production cluster-manager paper covering requests, limits, allocatable resources, task packing, overcommitment, isolation, availability, and operational lessons.
2. Schwarzkopf et al. [Omega: Flexible, Scalable Schedulers for Large Compute Clusters.](https://research.google/pubs/omega-flexible-scalable-schedulers-for-large-compute-clusters/) Primary shared-state scheduler paper covering parallel scheduling and optimistic concurrency.
3. Hindman et al. [Mesos: A Platform for Fine-Grained Resource Sharing in the Data Center.](https://www.usenix.org/conference/nsdi11/mesos-platform-fine-grained-resource-sharing-data-center) Primary two-level resource-offer and fine-grained cluster-sharing paper.
4. Apache Hadoop. [YARN Resource Model.](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/ResourceModel.html) Current official multidimensional resource, unit, minimum/maximum allocation, profile, and resource-type configuration model.
5. Ghodsi et al. [Dominant Resource Fairness: Fair Allocation of Multiple Resource Types.](https://digicoll.lib.berkeley.edu/record/136796/files/EECS-2011-18.pdf) Primary multi-resource allocation model, dominant-share definition, algorithm, and fairness-property paper.
6. Gog et al. [Firmament: Fast, Centralized Cluster Scheduling at Scale.](https://www.usenix.org/conference/osdi16/technical-sessions/presentation/gog) Primary min-cost-flow placement and centralized scheduling-quality/latency paper.
7. Kubernetes. [Resource Management for Pods and Containers.](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) Current requests, limits, units, CPU/memory/ephemeral-storage/huge-page, extended-resource, enforcement, and scheduling semantics.
8. Kubernetes. [Node Allocatable Resources.](https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/) Current system/kube reservations, eviction thresholds, allocatable reporting, and node enforcement guidance.
9. Kubernetes. [Resource Bin Packing.](https://kubernetes.io/docs/concepts/scheduling-eviction/resource-bin-packing/) Current multidimensional requested-to-capacity scoring and resource weighting.
10. Kubernetes. [Dynamic Resource Allocation.](https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/) Current structured device claims, allocation, selection, node access, and lifecycle semantics.
11. Kubernetes. [Resource Managers.](https://kubernetes.io/docs/concepts/resource-management/resource-managers/) Current CPU, memory, device, and topology-manager alignment mechanisms.
12. Linux Kernel. [Control Groups v2.](https://docs.kernel.org/admin-guide/cgroup-v2.html) Current CPU, memory, I/O, pressure, delegation, and hierarchical resource-control interfaces.
13. NVIDIA. [MIG User Guide.](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/) Current accelerator partitioning, instance profiles, isolation, placement, enumeration, and lifecycle details illustrating non-scalar device semantics.

## Exercises

### Exercise 1

A node has 32 CPU and 128 GiB physical capacity. Reserve 3 CPU/12 GiB for system work, 1 CPU/8 GiB for safety, and mark 16 GiB unavailable. Compute allocatable CPU and memory. Can tasks `(10,40)`, `(8,32)`, and `(9,24)` fit simultaneously by the scalar test?

### Exercise 2

Two nodes each have free vector `(8 CPU, 16 GiB)`. Place `(6,4)` on one and `(2,12)` on the other, then assess a pending `(4,8)` task. Explain why adding either 2 CPU to the first or 4 GiB to the second changes feasibility.

### Exercise 3

Total capacity is 200 CPU and 800 GiB. Tenant A receives `(60,80)` and tenant B `(20,240)`. Compute dominant shares. State important production concerns the calculation omits.

### Exercise 4

Design a resource representation for a task needing 8 CPU, 64 GiB, 500 GiB scratch, two mutually connected 40-GiB accelerators near one high-speed NIC, and a zone-bound persistent volume.

### Exercise 5

Design a validation plan for replacing fixed executor slots with a multidimensional request model for mixed batch and streaming data workloads. Include inventory, units, phases, request quality, overcommit, fragmentation, fairness, security, failure/recovery, evidence, rollout, and rollback.

## Answers to the Exercises

### Answer 1

Allocatable CPU is $32-3-1=28$ and memory is $128-12-8-16=92$ GiB. The tasks total 27 CPU and 96 GiB, so they fail the scalar memory condition by 4 GiB despite fitting CPU. This says nothing yet about topology, disk, network, devices, overhead, or performance.

### Answer 2

After placement, free vectors are `(2,12)` and `(6,4)`, aggregate `(8,16)`. `(4,8)` fits neither: the first lacks 2 CPU and the second lacks 4 GiB. Adding 2 CPU to the first produces `(4,12)`; adding 4 GiB to the second produces `(6,8)`. Either creates a node-local feasible vector, illustrating shape-specific fragmentation.

### Answer 3

A's shares are $60/200=0.30$ CPU and $80/800=0.10$ memory, so dominant share is 0.30. B's are 0.10 CPU and 0.30 memory, also 0.30. The equality omits per-node placement, heterogeneity, locality, devices, indivisibility, duration, priority, quota weights, request truthfulness, actual use, performance, and reclaim/preemption cost.

### Answer 4

Use scalar requests for 8 CPU, 64 GiB, and 500 GiB scratch, supplemented by a scratch performance class if capacity alone is insufficient. Create a typed device claim selecting two 40-GiB accelerator instances with required model/profile and peer-connectivity constraint. Add CPU/memory/device/NIC NUMA alignment and NIC capability/topology requirements. Bind a persistent-volume claim whose topology restricts candidate nodes to its zone and whose attachment/access mode is feasible. The allocator must atomically reserve the exact device identities and volume attachment along with scalar node fit; authenticated health/inventory and runtime configuration must match the grant.

### Answer 5

Inventory physical and allocatable CPU, memory, scratch capacity/performance, network, devices, topology, platform overhead, health, and freshness using canonical units. Derive phase-aware request distributions for scan, shuffle, join, spill, checkpoint, restore, and compaction; define defaults/confidence for new versions. Keep request, limit, allocation, use, throttling, eviction/OOM, and application outcome separate. Replay representative traces and adversarial mixes to compare feasibility, queue delay, locality, utilization, dominant residual resources, fragmentation, fairness, and cost. Test correlated peaks, hot keys, stale inventory, node/device loss, checkpoint/recovery spikes, and reclaim latency under explicit per-class overcommit/QoS policy. Authenticate resource declarations and inventory, constrain tenant inflation/extended resources, and reconcile capacity/allocation. Canary isolated pools and workload classes, compare scheduler decisions and runtime outcomes, alert on model error, version APIs/defaults, and retain a tested route back to fixed slots until reservations and durable workloads are safely migrated.
