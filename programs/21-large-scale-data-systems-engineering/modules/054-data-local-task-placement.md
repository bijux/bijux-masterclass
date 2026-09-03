---
module_id: LSDS-054
program: Large-Scale Data Systems Engineering
level: 2
module_number: 54
title: Data-Local Task Placement
status: complete
last_verified: 2026-09-04
---

# Data-Local Task Placement

## One-Page Review

### Governing question

When should a scheduler wait for compute near a task's input, cache, shuffle, state, or storage attachment, and when should it run immediately at a more distant location and pay movement cost?

### Essential definitions

- **data locality** is proximity between execution and the bytes/state it consumes under a declared topology and access path.
- A **locality preference** ranks placements by expected cost; a **hard locality constraint** declares distant placement invalid.
- **process-local** data is already in the target executor/process; **node-local** data is on the same machine.
- **rack/zone/region locality** describes increasingly broad failure/network domains; names do not guarantee equal bandwidth.
- **delay scheduling** temporarily skips an otherwise entitled task to await a better-locality opportunity, then relaxes locality after a bound.
- A **locality level** is one rung of the placement preference hierarchy, ending in unrestricted eligible placement.
- **movement cost** includes bytes, bandwidth, latency, congestion, request charges, decompression, cache pollution, and repeated reads.
- **locality metadata** maps input/state replicas or attachments to locations and has freshness, authority, and identity requirements.
- **data gravity** is the practical cost that makes moving compute to a large/regulated/stateful dataset preferable to moving the data.
- **remote storage** may be uniformly addressable without being uniformly fast, cheap, uncongested, or legally accessible.

### Central model, mechanism, or theorem

For task $j$ on candidate node $n$, define estimated completion cost

$$C(j,n)=W_j+Q_n+X(j,n)+E(j,n)+P(j,n)$$

where $W_j$ is locality wait already incurred, $Q_n$ queue/start cost, $X$ data/state transfer cost, $E$ execution cost under node interference/capability, and $P$ policy/risk penalty. A candidate must first satisfy hard resource, security, residency, storage-attachment, and failure-domain constraints. Delay is worthwhile only while the expected benefit of a better local placement exceeds added waiting and fairness/deadline risk. The scheduler progressively relaxes soft locality within bounded time or opportunities so locality improves throughput without causing starvation.

### Critical invariants

- Each input/cache/shuffle/state/volume location refers to a versioned object/partition and an authoritative, fresh topology identity.
- Hard constraints for residency, attachment, device, isolation, and failure domain are never relaxed as performance preferences.
- Candidate nodes pass resource/health/policy feasibility before locality scoring.
- Locality wait is bounded by time or genuine scheduling opportunities and resets only under explicit progress rules.
- Fair-share accounting charges actual allocations; skipped locality opportunities cannot reserve capacity indefinitely.
- Transfer estimates include shared-link congestion, storage/service quotas, decompression, retries, and cache effects—not bytes alone.
- Replicas marked local are healthy and readable; stale locality metadata falls back safely.
- Dynamic executor removal, node failure, cache eviction, and partition movement invalidate locality ownership promptly.
- Placement spreads correlated failure risk where required; performance locality does not defeat availability.
- Evidence compares end-to-end task/job outcomes, network/storage impact, fairness, and cost, not locality percentage alone.

### Common failures

Common failures include treating labels as verified topology; preferring a local overloaded node over a fast remote one; waiting indefinitely for a dead/local full node; confusing object-store endpoint reachability with equal cost; counting metadata locality after replica deletion; moving a small reusable broadcast repeatedly instead of broadcasting once; maximizing node-local percentage while rack links or disks saturate; ignoring decompression and compute heterogeneity; forcing affinity that causes fragmentation; losing shuffle/cache locality through dynamic allocation; placing all replicas/tasks in one failure domain; and claiming improvement from bytes avoided while completion time or other tenants worsen.

### Compact example

A 10-GiB input can run remotely now over an effective 1 GiB/s path, costing roughly 10 seconds of transfer, or wait four seconds for a node-local slot. If execution is otherwise equal and the prediction is credible, waiting saves about six seconds and network load. If the local slot is expected in 20 seconds, remote execution wins. The comparison changes with queue uncertainty, shared congestion, caching, deadlines, and failure.

### Connections

[LSDS-004](004-data-locality.md) introduces locality, [LSDS-012](012-metadata-servers-and-namespace.md) and [LSDS-013](013-replication-and-erasure-coding.md) define location/replica metadata, [LSDS-031](031-shuffle-architecture.md) adds intermediate locality, and [LSDS-051](051-cluster-resource-models.md) through [LSDS-053](053-fair-and-capacity-scheduling.md) define feasible and fair placement.

## Governing Question

Distributed data processing can move code to data or data to code. Serialized task code is often tiny compared with input partitions, so early MapReduce systems scheduled map work on machines holding input replicas. Modern clusters complicate the choice: input may reside in remote object storage, compute is heterogeneous, caches and shuffle are ephemeral, stateful operators own local state, and network paths have topology, congestion, and monetary cost.

Locality also competes with time. A suitable node may be busy. Waiting can avoid a large transfer and improve overall throughput; immediate remote execution may finish sooner and preserve fairness. The correct choice depends on task duration, expected wait, bytes, effective bandwidth, data reuse, congestion, deadline, and alternative candidates.

The governing question is how to maintain trustworthy location/topology metadata, separate hard from soft locality, estimate movement and waiting costs, relax preferences without starvation, coordinate with fairness/dynamic allocation, and validate the resulting placement under failure and load.

## Why This Matters

Network and storage are shared resources. One remote scan can consume bandwidth needed by many tasks; thousands can overload a rack uplink or object-store request budget. Data-local execution may convert network traffic into local disk or memory access, reduce tail latency, and increase cluster throughput.

Yet locality percentage is an incomplete objective. A node-local HDD read can be slower than remote cached data. A local CPU can be overloaded or lack required instruction/device capability. Waiting for locality can lengthen short jobs, and strict affinity can leave resources idle. Cost-based placement must consider execution and queues as well as distance.

Correctness, security, and availability impose non-negotiable constraints. A volume may attach only in one zone. Regulated data may not leave a jurisdiction. A state shard must have one fenced owner. Conversely, placing all processing and replicas in one rack increases correlated failure. The word “locality” must not blur preference and constraint.

Operational changes continuously invalidate assumptions. Replicas move, caches evict, executors scale down, shuffle blocks disappear, nodes drain, and topology labels change. Stale metadata can create repeated failed placements or unexpectedly remote reads. Locality is a live control problem, not a static annotation.

## Prerequisites and Retrieval

Review [LSDS-004](004-data-locality.md), storage metadata and replication in [LSDS-012](012-metadata-servers-and-namespace.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md), task/stage scheduling in [LSDS-005](005-distributed-task-graphs.md), [LSDS-006](006-stages-tasks-and-dependencies.md), and [LSDS-026](026-stage-scheduling.md), shuffle in [LSDS-031](031-shuffle-architecture.md) through [LSDS-034](034-hash-based-shuffle.md), and cluster allocation/fairness in [LSDS-051](051-cluster-resource-models.md) through [LSDS-053](053-fair-and-capacity-scheduling.md).

You should understand replicas, partitions, caches, shuffle, bandwidth/latency, topology/failure domains, scheduling queues, affinity, resource vectors, fairness, and basic cost estimation.

## Learning Objectives

After this module, you should be able to:

1. define process/node/rack/zone/region/no-preference locality for a concrete storage path;
2. separate hard residency/attachment/ownership constraints from soft performance preferences;
3. maintain versioned, fresh, authoritative location and topology metadata;
4. compare expected wait with transfer, execution, congestion, and deadline cost;
5. implement bounded progressive locality relaxation without fairness starvation;
6. place replicated, erasure-coded, cached, broadcast, shuffle, and stateful data correctly;
7. coordinate locality with dynamic allocation, heterogeneity, capacity, and preemption;
8. handle object storage and disaggregated systems where locality is path/cost rather than disk co-location;
9. detect stale metadata, hotspots, correlated placement, and locality gaming; and
10. validate locality policies using task/job outcomes, network/storage telemetry, fairness, resilience, and cost.

## Core Exposition

### Identify the bytes and state that matter

List task inputs: source splits/blocks, cached partitions, broadcast/reference data, shuffle blocks, keyed state, container images, model weights, local scratch, and attached volumes. Record size, version, replica/fragment locations, access pattern, reuse, mutability, and recovery source.

The largest bytes are not always dominant. Millions of small object requests can be limited by latency/quotas. A compressed 1 GiB object may expand to 20 GiB of CPU/memory work. A small shared metadata service can become the bottleneck.

### Define topology from real paths

Model executor/process, host, NUMA/socket, rack, zone, region, storage cell, and network path only where they change cost, policy, or failure. Verify node and storage topology through authoritative inventory; arbitrary user labels are not hardware truth.

Topology distance is not a metric by itself. Same-rack links can be congested; cross-zone bandwidth can be fast but costly; “same region” spans many paths. Pair categories with observed service and shared-capacity signals.

### Separate constraints from preferences

Hard constraints include legal residency, volume accessibility, device attachment, trusted execution, one-owner state fencing, and explicit availability placement. Violating them is invalid, regardless of performance.

Soft preferences include cached/process-local, node-local replica, same-rack, same-zone, and any eligible node. Express preferred weights/costs and a relaxation policy. Never encode a hard security rule as a preference that timeouts can relax.

### Build candidate feasibility first

Filter unhealthy/cordoned nodes, insufficient resource vectors, incompatible architecture/devices, unavailable volumes, forbidden domains, affinity/anti-affinity violations, and stale inventory. Only then rank feasible candidates by locality and other costs.

This ordering prevents a highly local but impossible node from dominating scoring. Preserve reason codes: “no local capacity,” “local replica stale,” and “residency forbids remote” demand different remedies.

### Estimate movement cost

For bytes $B$, effective throughput $eta$, setup latency $L$, request cost $K_r$, and decompression/deserialize work $K_c$, a first estimate is $X=L+B/\beta+K_r+K_c$. Use effective shared-path throughput, not NIC line rate.

Include read amplification, retries, erasure reconstruction, encryption, cross-zone/region charges, cache pollution, and concurrent transfers. If remote data becomes cached for several tasks, amortize cost under a defensible reuse probability.

### Estimate waiting cost

Waiting cost includes time already delayed, predicted release of preferred resources, deadline/slowdown penalty, fair-share deficit, and risk the local opportunity never arrives. Estimate from task completion distributions and eligible-node count, not one average.

If tasks are short and replicas numerous, a local slot may appear soon. If tasks are long or only one replica exists, strict waiting can dominate. Update the estimate as opportunities pass.

### Apply bounded delay scheduling

When the fair next task lacks preferred locality on the offered/free node, skip it temporarily and let another eligible task run. Track wait by wall time or genuine opportunities. Relax process-local to node-local to rack-local to unrestricted according to configured bounds.

Reset delay only when the task/job makes defined placement progress, not on every scheduler scan. Otherwise repeated resets starve it. Charge actual allocations; skipped turns do not consume resources, though temporal deficit may raise future priority.

### Choose time versus opportunity thresholds

Wall-time thresholds are intuitive but cluster load changes how many useful chances occur. Opportunity counts adapt to scheduling activity but must count only nodes that could satisfy the task except for locality. Counting incompatible nodes prematurely relaxes policy.

Calibrate by task duration, replica count, cluster size/load, locality benefit, and deadline. Avoid a universal value. Different locality rungs and workload classes deserve different bounds.

### Place replicated input

For replicated blocks, prefer a healthy local replica, then topology-near replicas, while distributing tasks across replica hosts to avoid disk/CPU hotspots. Location metadata must bind block/object version and replica health.

Do not concentrate all task attempts on one replica merely because it reports the shortest distance. Incorporate current disk/network queues and preserve failure independence. On replica loss, invalidate preference and choose another source.

### Place erasure-coded input

Reading one erasure fragment locally is not equivalent to a full local replica. Reconstruction may fetch $k$ fragments across racks and consume CPU. Model the actual read/reconstruction path and choose compute/location to minimize total movement without reducing durability.

Avoid moving fragments or tasks in ways that align all work with one failure domain. Repair traffic and analytical scans compete for network/storage; scheduling must observe both.

### Handle caches and broadcasts

Process-local cached data can justify executor affinity, especially when reuse is high and reconstruction costly. But cache contents are evictable; location metadata needs epoch/version and invalidation. A cache miss should fall back correctly rather than fail or read stale data.

For small shared inputs, broadcast once to workers rather than scheduling every task near one copy. Account distribution and memory cost. For huge reference data, partitioned co-location or storage-side filtering may be better.

### Handle shuffle locality

Map output commonly resides on producing executors/nodes or a shuffle service. Reducers fetch many partitions, so no single node is fully local. Placement should consider aggregate bytes by location, path congestion, merge/spill capacity, and whether shuffle storage is remote/disaggregated.

Dynamic allocation can remove executors and their blocks. Coordinate shuffle tracking, external service/storage, decommission migration, or recomputation. Stale block location causes fetch failure and retry storms.

### Handle stateful streaming

A keyed operator's state may be local plus remotely checkpointed. Keeping ownership on the same worker improves warm restart/cache, but failure or rescale requires restore/migration. Treat current state owner as a preference unless the consistency protocol makes it a fenced constraint.

Estimate state bytes/files, restore bandwidth, key skew, checkpoint freshness, catch-up, timers, and sink semantics. Placement across failure domains may be more important than immediate local reuse.

### Handle volumes and storage topology

Persistent volumes can have hard zone/node accessibility, attachment counts, access modes, and delayed binding. Schedule compute and volume atomically enough to avoid choosing incompatible locations. A soft “SSD” label is not equivalent to a bound volume.

For local persistent volumes, node loss may make data unavailable. Replication/recovery design determines whether rescheduling elsewhere is possible. For network volumes, topology still affects latency and link contention.

### Understand object-store locality

Object storage decouples compute from device placement, often yielding no meaningful node-local input. Still model endpoint/region, private path, cache, request/throughput quotas, cross-zone/region charges, and consistency/version identity. `NO_PREF` means no useful node preference under the model, not zero transfer cost.

Co-locate compute in the correct region/storage cell, batch/list requests, use range reads, cache responsibly, and spread request load. Benchmark effective paths with production-like concurrency.

### Include compute heterogeneity

A remote new-generation CPU may process/decompress twice as fast as a local old node. A GPU may justify weight movement. Estimate total completion, not bytes alone. Resource feasibility from [LSDS-051](051-cluster-resource-models.md) remains mandatory.

Avoid silently learning performance classes from tenant-sensitive workloads. Use governed benchmarks plus outcome telemetry, version models, and retain conservative behavior when confidence is low.

### Coordinate fairness and locality

Strict fair order can force remote work; strict locality can starve under-served jobs. Bounded delay lets other jobs use an opportunity while preserving a deadline for relaxation. Track the skipped subject's service deficit.

One job must not game preference by declaring every node non-local or withholding runnable alternatives. Validate data ownership, cap locality waits, and charge network/storage use as appropriate.

### Coordinate dynamic allocation

Executor scale-down discards process-local cache and perhaps shuffle/state locality. Scale-up adds cold workers that may pull large data. Allocation decisions should include locality value, block/state ownership, warmup, and migration.

Do not keep idle cache owners forever. Compare expected reuse and rebuild/movement cost with opportunity cost. Decommission invalidates ownership only after preservation/transfer is complete.

### Balance locality and failure domains

Putting compute near data can align both with one rack/zone. For replicated services or concurrent attempts, spread across independent domains when availability policy requires it. Do not read all replicas from the same physical path.

During zone degradation, relax soft locality but retain residency/security. Reserve network headroom for recovery and replica repair; remote failover can multiply traffic exactly when capacity is impaired.

### Prevent hotspots

Local preference can concentrate work on nodes holding popular blocks, cached partitions, or a heavy key. Incorporate node CPU/memory, disk queue, network, task count, and historical service tails. Replicate/cache/split popular data or relax locality sooner.

Prefer the lowest predicted marginal cost rather than closest label. Measure per-device/path utilization because node averages hide hotspots.

### Secure locality metadata and placement

Authenticate storage/node inventory and topology updates. Authorize data access independently of placement; running near data must not grant permission. Scope caches/shuffle to tenants or enforce isolation and cleanup.

Treat residency, sovereignty, confidential-compute, and tenant-separation rules as hard policy. Audit forced placements, relaxations, cross-domain transfers, administrative overrides, and metadata authors.

### Observe the decision path

Record task/input version, candidate counts and rejection reasons, preferred/selected locality, wait and relaxation rung, predicted/actual transfer, queue/start/execution time, cache hit, retries, and scheduler policy version.

Aggregate locality by bytes and time, not only task count. Connect it to network/storage utilization and tails, job completion/slowdown, fairness deficits, deadline misses, failure/recovery, energy, and monetary transfer/request cost.

### Validate under changing conditions

Replay traces preserving placement, replicas, task duration, bytes, topology, load, and tenant concurrency. Inject replica movement/loss, stale metadata, node drain, cache eviction, shuffle loss, link/storage throttling, zone failure, skew, and dynamic allocation.

Compare immediate-remote, strict-local, and bounded-delay policies. Canary by workload and topology. Require safety constraints, bounded waiting, no starvation, and improved end-to-end outcomes; preserve rollback when cost estimates drift.

## Definitions and Notation

Let task $j$ require input/state objects $O_j$ and candidate node $n$. Feasibility predicate $F(j,n)$ covers resource, health, attachment, residency, security, affinity, and failure policy. Locality level $\ell(j,n)$ is defined only after $F$ holds.

Let estimated cost be $C(j,n)=W_j+Q_n+X(j,n)+E(j,n)+P(j,n)$. A simple movement model is $X=L+B/\beta+K_r+K_c$ with bytes $B$, effective throughput $\beta$, setup latency $L$, request/monetary term $K_r$, and decode/deserialization term $K_c$ expressed in a common objective or reported separately.

Let locality wait bound at level $ell$ be $T_\ell$ or opportunity bound $N_\ell$. These bounds depend on workload and topology. A deadline constraint can limit total wait even when expected movement saving remains positive.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. Enumerate source, cache, broadcast, shuffle, state, image/model, scratch, and volume bytes with versions and reuse.
2. Define authoritative topology, storage paths, failure domains, metadata freshness, and invalidation.
3. Separate hard feasibility/residency/ownership rules from soft locality preferences.
4. Filter resource/health/policy candidates before locality scoring.
5. Estimate queue/wait, transfer, execution, congestion, monetary, deadline, and risk cost.
6. Define progressive locality levels with bounded time/opportunities and non-gaming reset rules.
7. Coordinate replicas/fragments, hotspots, caches/broadcasts, shuffle, streaming state, and volumes.
8. Reconcile fairness, dynamic allocation, preemption, heterogeneity, and failure-domain spread.
9. Secure metadata and data access; audit relaxation and cross-domain movement.
10. Validate outcomes under load, stale metadata, failures, rescale, congestion, and topology change.

If a local slot will become available in wait $w$ and remote transfer adds cost $x$, then waiting is beneficial in a simplified equal-execution/no-deadline model when $w<x$. This comparison is not a theorem for production: queue uncertainty, remote/local execution difference, congestion externalities, reuse, fairness, and deadlines alter the objective. Bounded relaxation guarantees only that a soft-locality preference cannot wait forever under qualifying opportunities.

## Alternatives and Trade-Offs

- **Immediate any-node placement** minimizes scheduler wait and complexity, but can amplify movement/congestion/cost.
- **Strict data-local placement** avoids remote reads, but can idle capacity, starve, hotspot replica nodes, and fail on stale locality.
- **Bounded delay scheduling** trades limited wait for locality and throughput, but needs calibrated levels/opportunities and fairness accounting.
- **Move compute to data** is efficient for large stable partitions, but constrained by resource heterogeneity and data-node isolation.
- **Move/cache data to compute** helps repeated work and disaggregated clusters, but consumes network/storage/memory and invalidation effort.
- **Broadcast reference data** eliminates per-task placement dependence for small shared inputs, but costs distribution and worker memory.
- **Replicate hot data** expands candidate nodes, but increases storage, consistency, and repair traffic.
- **Remote shuffle service/storage** weakens executor locality and enables elasticity, but adds a shared service/path bottleneck.
- **Hard affinity** enforces residency/attachment, but fragments capacity; soft preference improves flexibility but cannot enforce policy.
- **Global cost optimization** can consider many interactions, but stale estimates and decision latency can outweigh theoretical quality.

## Failure Modes and Misconceptions

- “Local always means faster.” Local devices/CPUs can be slower or overloaded.
- “Remote always means network.” Process-local versus node-local can still cross IPC/disk paths.
- “Same rack has a fixed cost.” Topology category does not reveal congestion or oversubscription.
- “Object storage has no locality.” Region/path/cache/requests/cost/residency remain.
- “No preference means no movement.” It only means candidates are equivalent under the placement model.
- “A replica location is timeless.” Movement, failure, corruption, and version change invalidate it.
- “Wait until a local node is free.” Without a bound, a dead/full node causes starvation.
- “Count every scheduler scan as an opportunity.” Only otherwise-feasible candidates are genuine chances.
- “Maximize local task percentage.” Weight by bytes/cost and check completion/fairness.
- “A node label proves data presence.” Authoritative versioned inventory must do so.
- “Shuffle is local to one reducer.” Reducers often fetch from many producers.
- “Cache affinity is free.” It can block scale-down and create hotspots.
- “Hard affinity improves performance safely.” It can make work infeasible and increase correlated failure.
- “Fairness forbids locality waiting.” Bounded delay can trade a small order deviation for shared throughput.
- “Preempt any remote task for a local one.” Victim cost and policy may exceed movement saved.
- “Bytes divided by line rate predicts transfer.” Shared throughput, latency, quotas, decode, retries, and request cost matter.

## Worked Examples

### Example 1

A 10-GiB split transfers remotely at effective 1 GiB/s, adding 10 seconds. A node-local slot is expected in four seconds with identical execution. Waiting has six-second estimated advantage; at 20 seconds predicted wait, remote execution is preferable before other costs.

### Example 2

A process-local cached partition saves 6 GiB of parse/reconstruction but its executor is busy for two seconds. Node-local uncached execution starts now and rebuilds in 15 seconds. A bounded process-local wait is valuable if the busy-time prediction and cache epoch are valid.

### Example 3

Three healthy HDFS replicas exist on racks A, B, and C. Rack A's disk queue is saturated; a rack-B node is free. Closest-label selection chooses A poorly. Cost-aware selection includes replica health, disk queue, compute readiness, and network path.

### Example 4

An erasure-coded object needs any 6 of 9 fragments. One fragment is node-local, five are cross-rack, and reconstruction costs CPU. Labeling the task “node-local” from one fragment hides most movement; score the full reconstruction plan.

### Example 5

A reducer needs 70 percent of its shuffle bytes from rack X and 30 percent elsewhere. Placing in rack X may reduce cross-rack bytes, unless its uplink/disk merge pool is saturated. Recompute the weighted path after maps retry or blocks migrate.

### Example 6

A stateful operator has 800 GiB locally cached state and a durable checkpoint. Keeping it on-node avoids restore, but the node is draining. Graceful migration/restore is mandatory; stale ownership is fenced, and future availability outweighs short-term locality.

### Example 7

A volume is attachable only in zone B. This is a hard feasibility predicate, not a preference to relax after a timeout. Within zone B, cached image and same-rack storage paths can remain soft scores.

### Example 8

Two tenants compete for a local slot. The fair next job skips twice for node locality while the other uses qualifying nodes; at its opportunity bound it relaxes to rack-local. Actual allocations and temporal deficit preserve fairness accounting.

### Example 9

Dynamic allocation wants to remove an idle executor holding 500 GiB of reusable cache. Expected reuse would avoid 100 seconds of remote reads, but keeping it blocks an urgent 30-minute job. Opportunity cost exceeds locality value, so the cache is discarded or migrated under policy.

### Example 10

This executable compares simplified local waiting with immediate remote transfer. It excludes queue uncertainty, execution heterogeneity, shared congestion, caching, fairness, deadlines, failures, and hard constraints.

<!-- bijux-verify: {"id":"local-wait-versus-remote-transfer","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"remote_transfer_seconds=10.0\nwaits=(4, 20) choices=('wait-local', 'run-remote') advantages=(6.0, -10.0)\n","stderr":""}} -->
```python
input_gib = 10
remote_gib_per_second = 1
remote_transfer_seconds = input_gib / remote_gib_per_second
waits = (4, 20)
choices = tuple(
    "wait-local" if wait < remote_transfer_seconds else "run-remote"
    for wait in waits
)
advantages = tuple(remote_transfer_seconds - wait for wait in waits)
print("remote_transfer_seconds=" + str(remote_transfer_seconds))
print("waits=" + repr(waits) + " choices=" + repr(choices) + " advantages=" + repr(advantages))
```

## Cross-Program Connections

- **Distributed storage:** replica/fragment placement, metadata, repair, volumes, caches, and object endpoints define data locations.
- **Networking:** topology, oversubscription, congestion, bandwidth, latency, path diversity, and cross-domain charges define movement cost.
- **Scheduling algorithms:** matching, delay scheduling, fairness deficits, bin packing, reservations, and cost models choose placements.
- **Platform engineering:** node inventory, labels, affinity, storage topology, schedulers, dynamic allocation, and telemetry operationalize locality.
- **Reliability engineering:** stale metadata, failure domains, drain, restore, recovery traffic, and degraded-mode policy constrain preference.
- **Security engineering:** residency, access authorization, trusted nodes, authenticated topology, cache isolation, and audit are hard boundaries.
- **Data engineering:** scan splits, broadcasts, shuffle, joins, state, skew, and reuse determine which bytes matter.
- **FinOps:** transfer/request charges, cache cost, idle wait, recomputation, and shared bottlenecks determine economic locality.

## References

1. Dean and Ghemawat. [MapReduce: Simplified Data Processing on Large Clusters.](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) Primary input splitting, replica-aware map placement, backup execution, network, and locality design paper.
2. Ghemawat, Gobioff, and Leung. [The Google File System.](https://research.google/pubs/the-google-file-system/) Primary distributed-filesystem paper covering chunk locations, replication, rack-aware placement, client data paths, recovery, and co-designed large-scale workloads.
3. Apache Spark. [Tuning: Data Locality.](https://spark.apache.org/docs/latest/tuning.html#data-locality) Current process/node/no-preference/rack/any levels and wait-versus-transfer behavior.
4. Apache Spark. [Configuration: Scheduling.](https://spark.apache.org/docs/latest/configuration.html#scheduling) Current per-level locality-wait, resource-registration wait, exclusion, and scheduling controls.
5. Apache Hadoop. [Fair Scheduler.](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/FairScheduler.html) Current node/rack locality opportunity thresholds, fair queues, weights, minima, and preemption context.
6. Apache Hadoop. [HDFS Architecture.](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html) Current block replication, rack awareness, replica placement, read selection, metadata, and failure model.
7. Apache Hadoop. [HDFS Erasure Coding.](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HDFSErasureCoding.html) Current stripe/block-group layout, reconstruction, placement, network, storage, and recovery behavior.
8. Hindman et al. [Mesos: A Platform for Fine-Grained Resource Sharing in the Data Center.](https://www.usenix.org/conference/nsdi11/mesos-platform-fine-grained-resource-sharing-data-center) Primary two-level offers, framework locality preferences, rejection filters, fairness, and replicated-data experiments.
9. Kubernetes. [Kubernetes Scheduler.](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/) Current filtering/scoring framework and explicit data-locality/constraint/interference placement concerns.
10. Kubernetes. [Assigning Pods to Nodes.](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/) Current required/preferred node affinity, inter-pod affinity, topology domains, and label trust cautions.
11. Kubernetes. [Scheduler Configuration.](https://kubernetes.io/docs/reference/scheduling/config/) Current filter/score plugins for node/resource/volume/topology/image locality and configurable profiles.
12. Kubernetes. [Storage Capacity.](https://kubernetes.io/docs/concepts/storage/storage-capacity/) Current storage topology, delayed binding, capacity tracking, and scheduler placement behavior.
13. Kubernetes. [Topology-Aware Volume Provisioning.](https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode) Current immediate versus wait-for-consumer binding and topology-constrained volume provisioning.

## Exercises

### Exercise 1

A 24-GiB input transfers remotely at effective 2 GiB/s plus 1.5 seconds setup. A local slot is predicted in 8 seconds. Compute the simple movement/wait comparison and state missing factors.

### Exercise 2

Design a progressive policy with process-, node-, rack-, and any-locality levels. Define what counts as an opportunity, when waits reset, and how fairness/deadlines cap relaxation.

### Exercise 3

A reducer fetches 400 GiB: 220 GiB from rack A, 120 from B, and 60 from C. Ignoring congestion and equal execution, compute cross-rack bytes when placed in each rack and choose the byte-minimizing rack.

### Exercise 4

Explain how placement should change for replicated blocks, erasure-coded stripes, object-store input, local persistent volume, executor cache, shuffle blocks, and keyed streaming state.

### Exercise 5

Design a production validation of a new locality policy. Include metadata authority/freshness, hard constraints, cost estimation, fairness, dynamic allocation, failures, security, metrics, experiments, canary, and rollback.

## Answers to the Exercises

### Answer 1

Transfer estimate is $1.5+24/2=13.5$ seconds. Eight seconds of local wait has a simple 5.5-second advantage, so wait-local wins in the simplified model. Missing factors include wait uncertainty, local/remote execution speed, shared-path congestion, request/cross-zone cost, decompression, retries, caching/reuse, fair-share deficit, deadline, replica health, and failure.

### Answer 2

Start process-local for a bounded interval/opportunity count, then node-local, rack-local, and any eligible placement. Count an opportunity only when a node satisfies every hard resource/health/security/residency/device/volume constraint and could run the task except for the current soft locality rung. Track wall time too so low scheduling activity cannot wait forever. Reset only after the task/job actually obtains a placement or under an explicit stage-generation rule, not on every scan. Apply a total deadline/slowdown cap, accrue temporal fairness deficit while skipped, and never relax hard policy.

### Answer 3

Placing in A keeps 220 GiB local-to-rack and crosses $120+60=180$ GiB. In B, cross-rack is $220+60=280$ GiB. In C, it is $220+120=340$ GiB. Rack A minimizes bytes in this model. Real placement also accounts for link/disk/compute queues, parallel flows, replicas, per-node fit, fault policy, and whether “rack-local” still traverses a shared switch.

### Answer 4

Replicated blocks offer several full-data candidates and require version/health plus hotspot-aware selection. Erasure-coded data requires a reconstruction plan across enough fragments, not one local fragment. Object storage usually yields no node preference but retains region/path/cache/quota/cost/residency concerns. A local persistent volume creates hard accessibility and attachment constraints. Executor cache is a versioned soft preference whose reuse value competes with idle capacity. Shuffle placement considers aggregate producer bytes and block survival/migration. Keyed streaming state prefers warm ownership but relies on fenced state assignment and durable checkpoint restore during failure/rescale. Each case begins with hard feasibility and then scores real end-to-end cost.

### Answer 5

Build authoritative versioned mappings for inputs/replicas/fragments/caches/shuffle/state/volumes and authenticated node/network/storage topology with health and freshness deadlines. Encode residency, trusted execution, attachment, device, ownership, and failure spread as hard filters; make performance locality a bounded progressive preference. Calibrate queue/wait and transfer models from bytes, effective concurrent throughput, setup/requests, decode, node performance, congestion, reuse, and monetary cost. Preserve fair-share/temporal deficit and validate opportunity counting/reset against gaming. Coordinate cache/shuffle/state ownership with executor scale-down, decommission, preemption, and rescale. Inject stale/moved/lost replicas, cache eviction, shuffle loss, link/storage throttling, node/zone drain, metadata outage, skew/hotspots, and remote fallback. Compare immediate-remote, strict-local, and bounded-delay cohorts using locality by bytes/time, wait, predicted/actual movement, queue/start/execution, cache hit, network/storage tails, completion/slowdown/deadlines, fairness, recovery, failure domains, and cost. Canary by workload/topology, audit cross-domain relaxation, gate on safety and outcome thresholds, and retain the prior scheduler profile/configuration for atomic rollback.
