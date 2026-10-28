---
module_id: LSDS-004
program: Large-Scale Data Systems Engineering
level: 1
module_number: 4
title: Data Locality
status: complete
last_verified: 2026-09-03
---

# Data Locality

## One-Page Review

### Governing question

When should a large-scale data system move computation toward data, move data toward computation, wait for a nearer resource, or deliberately sacrifice locality for fairness, capacity, resilience, and completion time?

### Essential definitions

- **Data locality** is the relationship between an operation's execution location and the locations of its required bytes or state.
- A **locality level** classifies distance, such as process, NUMA domain, node, rack, zone, region, or remote service.
- **Data-local scheduling** places computation where an eligible input copy is already available.
- **Compute-local placement** moves or caches data near a chosen execution resource.
- **Delay scheduling** waits briefly for a more local resource before accepting a farther placement.
- **Affinity** prefers or requires placement near named data, tasks, hardware, or topology.
- **Anti-affinity** separates replicas or tasks to reduce correlated failure or interference.
- **Cache locality** reuses a nearer copy whose identity, freshness, and eviction policy are governed.

### Central model, mechanism, or theorem

A locality decision is `D=(I,X,T,C,Q,F,E)`: input/state locations `I`; candidate execution resources `X`; topology and transfer characteristics `T`; compute and storage costs `C`; queue/resource state `Q`; failure, freshness, and policy constraints `F`; and evidence `E`.

For task `j` on candidate `x`, estimate:

`finish(j,x)=available(x)+startup(j,x)+compute(j,x)+sum_i transfer(bytes_(j,i), path(i,x))+contention(j,x)`.

Choose only among feasible candidates, and optimize the declared job, fairness, cost, and reliability objective—not network bytes alone. Waiting for locality is rational only when expected avoided remote cost exceeds waiting and opportunity cost under the service objective.

### Critical invariants

- Locality is defined for exact input versions and current locations, not stale catalog hints.
- Required replicas remain separated across declared failure domains even when co-location is cheaper.
- Scheduling honors security, residency, hardware, capacity, fairness, and recovery constraints before preference.
- Every transfer includes protocol, serialization, decompression, encryption, and contention cost where relevant.
- Cache hits are validated for identity and freshness; eviction or worker loss remains recoverable.
- Locality optimization does not silently change ordering, partitioning, transaction, or consistency semantics.
- Decisions and measurements distinguish useful bytes from shuffle, spill, replication, and retry traffic.
- Fallback from nearer to farther placement is bounded, observable, and tested under saturation and failure.

### Common failures

Frequent failures are equating local with fast, ignoring queue time, treating rack labels as accurate, co-locating all replicas, pinning work until the cluster idles, reading remote data repeatedly instead of caching, optimizing input locality while creating a larger shuffle, mistaking cache warmth for durable placement, and measuring average network bytes without job tails or fairness.

### Compact example

A 1.2-GB task can start now on a remote worker at 150 MB/s or in four seconds on its local worker at 600 MB/s. With two seconds of compute, remote completion is about ten seconds; local completion after waiting is about eight seconds. Waiting helps in this estimate, but a longer queue, cached remote copy, or urgent deadline can reverse the choice.

### Connections

[LSDS-003](003-range-hash-and-consistent-partitioning.md) determines where logical units may reside. [LSDS-005](../ROADMAP.md) develops distributed task graphs, whose edges expose movement. Locality also depends on [Operating Systems](../../22-operating-systems/ROADMAP.md), [Computer Architecture](../../23-computer-architecture/ROADMAP.md), [Platform Engineering](../../29-platform-engineering/ROADMAP.md), and [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

“Move compute to data” is a valuable heuristic, not a law. It was especially powerful in shared-nothing clusters where local disks held replicated filesystem blocks and computation was comparatively small. Modern systems also use object stores, disaggregated compute, accelerators, local caches, remote shuffle services, multiple regions, and elastic workers. The best action depends on the exact data copies, candidate resources, queue state, transfer path, failure constraints, and reuse horizon.

Locality has multiple scales. Bytes in the same process avoid serialization and interprocess transfer. Data in another NUMA domain is on one server but can have different memory cost. A local NVMe device differs from another process's cache on the same node. Same-rack traffic crosses a network switch; same-zone and cross-zone paths can differ in bandwidth, latency, failure exposure, and price. Cross-region placement can add orders of magnitude in latency and policy constraints. “Local” without a named boundary is not an engineering claim.

The governing question is therefore a constrained completion-time and system-cost problem: should work wait for a nearer feasible resource, run remotely now, cause a durable data movement, or create/reuse a cache? The answer must preserve correctness, fairness, isolation, resilience, security, and residency before optimizing distance.

## Why This Matters

Large analytical jobs read much more data than their executable code contains. Sending a small function to a node holding hundreds of megabytes can save scarce network capacity. Google's MapReduce design scheduled map tasks near Google File System input replicas for this reason. Hadoop's HDFS architecture explicitly states the principle of moving computation rather than large data and exposes block locations for scheduling.

Network traffic is shared. One remote task may be harmless; thousands can congest rack uplinks, storage gateways, or object-store request paths, slowing unrelated jobs and recovery. A shuffle can dominate a job even when every scan is local. Storage and network topology must therefore be analyzed for the whole graph, not one stage.

Locality also interacts with queueing. The node holding input can be busy while an idle remote node is ready. Waiting too long wastes compute and violates latency; launching remotely too quickly consumes bandwidth and discards an imminent local opportunity. The delay-scheduling paper demonstrated a practical way to trade a short wait for improved locality while retaining fairness in shared clusters. Current Spark documentation exposes process-, node-, rack-, and any-level fallbacks with configurable waits.

Replication creates placement choices. A scheduler can select among input replicas to balance work and use a nearer copy. Yet placing every replica and consumer together undermines failure tolerance. The same topology information that improves locality must also keep durable copies across independent domains. Locality and resilience can point in opposite directions.

Disaggregated storage changes the baseline. When authoritative data lives in an object or shared storage service, every cold worker reads remotely. Elastic compute and independent scaling become easier; local disk becomes a cache and temporary-work tier. Snowflake's published architecture is one example: shared persistent storage is separated from compute, while local caches reduce repeated network traffic. Cold-start, cache churn, request rate, egress, and cross-zone costs become essential evidence.

Locality is temporal. A dataset may be local when scheduled and evicted before execution. A cache may be warm for one repeated query and useless for a one-time scan. Moving a terabyte once can be rational if reused one hundred times, and wasteful if the consumer terminates immediately. Decisions need expected reuse and invalidation, not just distance at one instant.

## Prerequisites and Retrieval

Recall from [LSDS-002](002-horizontal-partitioning.md) that logical partition identity differs from placement, and from [LSDS-003](003-range-hash-and-consistent-partitioning.md) that ownership and replica maps can change by epoch. You should understand throughput, latency, queueing, bandwidth, caching, replication, failure domains, serialization, and critical paths.

Retrieve the difference between a preference and a hard constraint. Locality is usually a preference that may be relaxed. Data residency, accelerator compatibility, memory capacity, or safety isolation may be hard constraints. Encoding a preference as mandatory can strand work; treating a constraint as preference can violate policy or correctness.

## Learning Objectives

After completing this module, you should be able to:

- name locality levels from process and NUMA placement through region and remote service;
- distinguish authoritative placement, replicas, caches, and transient intermediate data;
- estimate transfer, compute, queue, startup, and contention costs for candidate placements;
- explain compute-to-data, data-to-compute, caching, prefetching, and data staging;
- apply bounded delay scheduling and explain its fairness trade-offs;
- trace locality through scans, shuffles, joins, stateful streams, and sinks;
- reconcile affinity with replica anti-affinity and failure-domain requirements;
- analyze locality in disaggregated storage and elastic-compute architectures;
- diagnose stale topology, cache churn, hot nodes, skew, and cross-zone traffic;
- design representative locality experiments and high-consequence review.

## Core Exposition

### Locality is a relation, not an attribute

Data is not simply local or remote. A specific task version requires specific input versions, state, libraries, and sometimes hardware. Those objects can have several authoritative replicas and caches. A worker has a topology position, available capacity, queue, devices, network paths, credentials, and failure status. Locality exists between that requirement set and that worker at a time.

Represent a data copy with object identity, content/version, location, storage tier, durability role, freshness, and availability. A scheduler using a stale block-location hint may place work on a node that has already lost or moved the block. The worker then fetches remotely or fails. Metadata freshness and fallback are part of the mechanism.

The closest copy may not be the fastest. A busy local disk, decompression bottleneck, noisy neighbor, small-page random access, or insufficient memory can make a farther high-throughput service faster. Conversely, a low-latency remote path can collapse under simultaneous fan-out. Measure sustained performance under concurrency rather than ranking distance by labels alone.

### A topology ladder

**Process-local** data may already be materialized in an executor heap or native buffer. It avoids network transfer but consumes scarce memory and can disappear with the process. Identity and eviction matter.

**NUMA-local and device-local** placement aligns CPU, memory, accelerators, and storage paths within one host. A process can be node-local in the cluster sense while repeatedly crossing sockets or copying between host and accelerator memory. Operating-system and architecture controls own this finer placement.

**Node-local** data resides on the same physical or virtual node, commonly on local disk or in another local process. Transfer still incurs filesystem, IPC, serialization, or memory-copy costs. Node failure can remove both compute and cache.

**Rack-local or zone-local** data traverses shared network infrastructure but avoids broader links. Topology labels must reflect real routing and failure relationships. A mislabeled rack can simultaneously degrade bandwidth assumptions and replica independence.

**Region-local and cross-region** paths add distance, bandwidth limits, egress or transfer price, residency constraints, and larger failure modes. Moving computation across regions can also move logs, intermediate state, and outputs, not only declared input.

**No preference** applies when input is equally accessible from all candidates, already broadcast, tiny, or generated. It should be explicit rather than inferred from missing metadata.

### Compute toward data

When input is large, stable, and replicated on worker-local storage, sending task code and small configuration to an input replica is attractive. Map tasks over distributed filesystem blocks are canonical. The scheduler enumerates eligible locations, chooses one with capacity, and retries elsewhere if needed.

Data-local execution needs compatible resources. A local node without enough memory, correct runtime, accelerator, security identity, or isolation is not feasible. Input locality also does not ensure output locality: a task may write to a remote sink or emit a large shuffle.

Repeated computation on the same partitions benefits from executor reuse and cache affinity. Excessive pinning reduces load balance and can let one failed executor invalidate much cached state. Durable recovery must not depend on an ephemeral cache unless loss is explicitly acceptable.

### Data toward compute

Moving data is rational when a specialized or scarce resource is fixed, when input is small, when remote capacity is immediately available, when reuse amortizes staging, or when storage is disaggregated by design. GPU preprocessing, broadcast joins, and elastic object-store scans are examples with different economics.

Staging copies data before execution and can hide transfer behind other work. Prefetching is useful only when predictions are accurate enough; unused prefetched bytes waste capacity and can evict valuable cache entries. A staged copy needs version identity and lifecycle cleanup.

Broadcasting sends a small shared input to many workers. It converts repeated remote reads or a large shuffle into replication. Size must include serialization, worker count, concurrent jobs, retries, and memory. A dimension table that is small on disk may expand dramatically in memory.

### Queueing and delay scheduling

For a task `j` and worker `x`, compare estimated completion rather than distance alone. Include worker availability, task startup, input transfer or local read, compute, output, and contention. Estimates are uncertain, so record observed error and avoid false precision.

Suppose a remote worker is free now, while a local worker becomes free after wait `w`. If local and remote execution otherwise match, waiting is favorable when `w + local_read < remote_read` and the wait does not violate fairness or deadlines. With several locality levels, a scheduler can wait briefly for process-local, then node-local, then rack-local capacity before accepting any feasible worker.

Delay must be bounded. Long mandatory affinity can leave idle workers while one node queues tasks. Fair scheduling also matters: repeatedly allowing one job to wait for locality can change who receives resources and cause head-of-line blocking. Delay scheduling lets other jobs use a slot during the wait, but its assumptions should be tested for the actual task durations, cluster load, and sharing policy.

Short tasks tolerate less delay because scheduling and transfer are a larger fraction of runtime. Long scan tasks may justify longer waits. Deadline-critical work can prefer immediate remote placement, while throughput-oriented work can protect shared network capacity. One global timeout rarely fits every stage.

### Graph-wide locality

A distributed task graph creates several data placements. Source blocks or objects have input locations. Narrow transformations may retain partition affinity. A shuffle writes intermediate partitions that reducers fetch. Stateful streaming operators have checkpoint and live-state locations. Sinks impose their own topology.

Optimizing source locality can worsen the critical path if it produces an expensive shuffle across racks. Co-partitioned joins can preserve locality when both inputs share compatible boundaries and placement. Broadcast joins trade one controlled replication for avoiding movement of a much larger side. The cost model should count every graph edge and locate bottleneck links.

Intermediate data is often less durable than input. Local shuffle files make producer and consumer placement consequential and can be lost with executors. A remote shuffle service changes failure and scaling behavior while adding network and service dependencies. Checkpoint placement affects recovery time: a nearby live state copy is fast, but durable recovery may require a farther store.

Speculative execution duplicates slow tasks. Launching a speculative copy on a remote worker can consume extra input and output bandwidth and may contend with the original. It is justified when expected tail reduction exceeds duplicate cost and sink semantics tolerate multiple attempts.

### Storage placement and failure domains

Replica placement must satisfy durability and availability before read locality. Keeping all copies in one rack makes rack-local reads cheap until that rack fails. Spreading replicas across zones improves independence but adds write and repair traffic. A read selector can prefer the nearest eligible replica while monitoring freshness and load.

Compute anti-affinity may spread redundant consumers across domains even when their input is colocated. Conversely, co-locating a producer and consumer can reduce traffic but create a shared fate. The design must say whether the objective is throughput, low latency, failure independence, or a weighted combination.

Topology is control-plane data. Validate node-to-rack-to-zone mappings, detect missing labels, and audit changes. Cloud instance labels do not always capture physical oversubscription or network paths. Empirical link measurements complement declared hierarchy without replacing policy boundaries.

### Disaggregated storage, caches, and elasticity

Separating durable storage from compute allows each to scale independently and lets multiple compute clusters share one authoritative dataset. It weakens cold-start locality because new workers have empty caches. Local SSDs can cache compressed source blocks, decoded columns, intermediate data, or results; each tier has different identity and invalidation requirements.

Cache value depends on hit probability, reuse distance, object size, fetch cost, decoding cost, and eviction. Report cold and warm behavior separately. A benchmark that primes caches but production workers churn rapidly is misleading. Conversely, disabling caches can understate a stable repeated-query workload.

Autoscaling can fight locality. Removing a warm worker saves idle compute but discards cached data and may trigger remote reads on replacement. Scaling out increases parallel demand on shared storage. Evaluate total completion and monetary cost, not worker count alone. Minimum residence time, cache-aware draining, and staged warm-up can help.

Multi-region systems must decide whether to move data, computation, or both. Residency and sovereignty may forbid copies. Cross-region outputs, logs, checkpoints, and debugging artifacts can violate the intended boundary even when source data stays put. Trace the entire information flow.

### Measurement and operations

Measure locality per level: input bytes and task counts process-local, node-local, rack/zone-local, and remote. Also measure wait time for locality, remote read throughput, link saturation, cache hit bytes, cache churn, queue delay, task duration, retries, speculative duplication, shuffle bytes, spill, and stage/job tails.

A high task-locality percentage can mislead when the few remote tasks contain most bytes. Byte locality can mislead when remote requests are tiny but latency-sensitive. Use both counts and weighted measures. Attribute traffic to scans, shuffle, broadcast, replication, repair, checkpointing, retries, and user output.

Diagnose the critical path. Reducing network bytes outside the slowest required chain may not improve completion. An overloaded local node can make strict locality slower than remote work. Test policies across load, skew, failure, cold caches, topology changes, and mixed tenants.

## Definitions and Notation

Let task set be `J`, candidate resources `X`, and required input objects for task `j` be `I_j`. Each object `i` has eligible current copies `L_i(t)` with version and freshness metadata. Topology distance `d(l,x)` names a path class; transfer estimate `tau(bytes,path,load)` includes protocol and contention.

Candidate `x` is feasible for `j` only if resource, security, residency, hardware, isolation, and recovery constraints hold. For feasible placement:

`finish(j,x)=A_x+S_(j,x)+C_(j,x)+sum_(i in I_j) tau(B_(j,i), path(i,x))+O_(j,x)`.

Here `A_x` is availability time, `S` startup, `C` compute/local I/O, `B` required bytes, and `O` output and modeled contention. For replicas, choose the eligible copy that minimizes the applicable path cost without violating freshness or consistency.

Task locality ratio at level `q` is tasks at `q` divided by all tasks. Byte locality ratio weights by required input bytes. Network amplification can be `network_bytes / useful_input_bytes`, with categories reported separately. Cache hit ratio should also distinguish request hits from byte hits.

For a possible durable staging action with transfer cost `M`, expected avoided future transfer `R * p * A` depends on reuse count `R`, hit probability `p`, and avoided cost `A`. Staging is economically favorable only after including cache capacity, eviction, invalidation, and failure cost; this inequality is an estimate, not a correctness proof.

## Mechanisms, Invariants, or Proof Structure

A locality design has seven obligations.

**1. Object identity.** Name every input/state version, authoritative copy, replica, cache, and transient result. Define freshness and invalidation.

**2. Feasible placement.** Apply capacity, runtime, device, security, residency, isolation, and failure-domain constraints before locality preferences.

**3. Topology model.** Record node, NUMA/device, rack, zone, region, and service paths as relevant. Validate metadata and measure real transfer under contention.

**4. End-to-end cost.** Estimate queue, startup, local/remote read, decoding, compute, shuffle, output, retries, and contention along the critical path.

**5. Scheduling policy.** Specify preference ordering, bounded waits, fairness, priorities, deadlines, fallback, preemption, and behavior when locality metadata is absent or stale.

**6. Failure and evolution.** Test worker, cache, disk, rack, zone, metadata, and network failures; topology changes; autoscaling; retry; speculative execution; and durable recovery.

**7. Evidence.** Retain workload distributions, cold/warm results, per-level task and byte locality, network categories, queue delay, tails, costs, decisions, exceptions, and consequence-appropriate review.

The executable model uses eight sequentially considered tasks, three workers, one authoritative home per task, fixed local and remote rates, and exact compute durations. It compares blind round-robin assignment with greedy earliest estimated finish.

<!-- bijux-verify: {"id":"locality-scheduling-comparison","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"round_robin remote_mb=3000 makespan_s=15.67\nround_robin assignments=t0:a,t1:b,t2:c,t3:a,t4:b,t5:c,t6:a,t7:b\nlocality_aware remote_mb=1200 makespan_s=12.00\nlocality_aware assignments=t0:a,t1:a,t2:b,t3:c,t4:c,t5:b,t6:a,t7:c\nnetwork_reduction=60.00%\n","stderr":""}} -->
```python
workers = ("a", "b", "c")
tasks = (
    ("t0", 1200, "a", 2),
    ("t1", 900, "a", 2),
    ("t2", 800, "b", 3),
    ("t3", 600, "b", 1),
    ("t4", 500, "c", 2),
    ("t5", 400, "c", 1),
    ("t6", 300, "a", 4),
    ("t7", 200, "a", 1),
)
local_rate = 600
remote_rate = 150


def schedule(policy):
    ready = {worker: 0.0 for worker in workers}
    assignments = []
    remote_mb = 0
    for index, (task_id, size_mb, home, compute_s) in enumerate(tasks):
        def finish(worker):
            rate = local_rate if worker == home else remote_rate
            return ready[worker] + compute_s + size_mb / rate

        if policy == "round_robin":
            worker = workers[index % len(workers)]
        else:
            worker = min(workers, key=lambda item: (finish(item), item))
        ready[worker] = finish(worker)
        remote_mb += 0 if worker == home else size_mb
        assignments.append(f"{task_id}:{worker}")
    return ",".join(assignments), remote_mb, max(ready.values())


round_robin = schedule("round_robin")
locality_aware = schedule("locality_aware")
print(
    f"round_robin remote_mb={round_robin[1]} "
    f"makespan_s={round_robin[2]:.2f}"
)
print(f"round_robin assignments={round_robin[0]}")
print(
    f"locality_aware remote_mb={locality_aware[1]} "
    f"makespan_s={locality_aware[2]:.2f}"
)
print(f"locality_aware assignments={locality_aware[0]}")
print(
    "network_reduction="
    f"{(round_robin[1] - locality_aware[1]) / round_robin[1]:.2%}"
)
```

The greedy policy assigns three tasks remotely because availability plus transfer still minimizes its local estimate. In this fixture it reduces remote input by 60% and estimated makespan by 3.67 seconds. This is not a scheduler benchmark or proof of optimality. It omits simultaneous scheduling, replicas, startup variation, output and shuffle, network contention, cache state, estimation error, failures, fairness, preemption, and deadlines.

## Alternatives and Trade-Offs

**Wait versus transfer.** Waiting protects network and may finish sooner when a local resource becomes available quickly. Immediate remote execution protects latency when queues are long. Use bounded, stage-aware estimates.

**Compute-to-data versus data-to-compute.** Large stable inputs favor shipping small code. Specialized hardware, tiny input, or repeated reuse can justify staging data near compute.

**Local disks versus shared object storage.** Local disks enable strong scan locality but couple storage and compute capacity. Shared storage enables elasticity and independent durability while making network and cache behavior central.

**Affinity versus load balance.** Strong affinity raises cache or input hits but can hotspot constrained nodes. Relaxation spreads work at transfer cost.

**Affinity versus failure independence.** Co-location reduces latency and increases shared fate. Replica anti-affinity may require farther writes and reads to preserve recovery.

**Warm cache versus elastic scale-down.** Keeping workers retains reuse and costs idle compute. Removing them saves compute and pays future cold-start transfer and decoding.

**Broadcast versus shuffle.** Broadcasting a small side replicates it to every consumer. Shuffling partitions both sides by a key. Compare expanded in-memory size, consumers, reuse, and network paths.

**Local shuffle versus remote shuffle service.** Local files can be fast and simple but tie intermediate survival to executors. Remote service adds network and operational dependency while decoupling compute turnover.

**Strict constraints versus soft preferences.** Constraints protect correctness and policy but reduce feasible capacity. Preferences can relax under load. Misclassification either strands work or violates requirements.

**Per-task versus graph-wide optimization.** The nearest worker for each input can still create a poor shuffle, sink bottleneck, or job tail. Optimize the declared global objective when feasible.

## Failure Modes and Misconceptions

1. **Local always means faster.** Queue, device contention, decoding, and resource mismatch can dominate distance.
2. **Same node means no movement.** IPC, filesystem, memory, NUMA, and accelerator transfers remain.
3. **Topology labels are inherently accurate.** Stale or wrong rack/zone metadata corrupts both cost and failure assumptions.
4. **Task locality percentage measures benefit.** A few remote tasks may hold most bytes or the critical path.
5. **Byte locality alone measures benefit.** Tiny latency-sensitive requests and bandwidth contention can matter more.
6. **Wait indefinitely for locality.** Mandatory waiting can leave capacity idle and violate fairness or deadlines.
7. **Never wait when a worker is idle.** A brief wait can avoid a long transfer and improve completion.
8. **Input locality optimizes the job.** Shuffle, output, checkpoint, and sink paths can dominate.
9. **A cache is a replica.** An evictable copy may lack durability, freshness, or recovery guarantees.
10. **A replica is safe because it is remote.** It may share rack, zone, power, account, control plane, or corruption source.
11. **Co-locate all copies for speed.** Correlated failure can remove every copy.
12. **Disaggregated storage eliminates locality.** Cache, region, zone, service endpoint, and intermediate placement still matter.
13. **Autoscaling only changes compute cost.** It changes cache warmth, storage fan-out, and shared-service load.
14. **Prefetching always hides I/O.** Wrong predictions waste bandwidth and evict useful data.
15. **Broadcast input is small because its file is small.** Deserialization and per-worker replication can expand it.
16. **Speculation is free tail insurance.** Duplicate tasks consume transfer, compute, and sink capacity.
17. **Stale location hints only hurt performance.** They can interact with missing versions or authority and return wrong data if identity checks are weak.
18. **A local checkpoint guarantees recovery.** Node loss can remove task and checkpoint together.
19. **Cross-zone traffic is only a price issue.** Latency, bandwidth, policy, and failure behavior also change.
20. **One locality timeout fits all tasks.** Task duration, input size, deadline, and contention differ.
21. **Balanced CPU means balanced cluster.** Network uplinks, storage gateways, memory, and devices may be saturated.
22. **Retries preserve locality.** Replacement nodes may be farther and caches cold.
23. **Residency applies only to source data.** Logs, spills, checkpoints, output, and diagnostics also carry information.
24. **The nearest replica is always eligible.** It may be stale, overloaded, unauthorized, or in the wrong failure state.
25. **Synthetic uniform tasks validate policy.** Real sizes, skew, cache churn, mixed tenants, and failure must be replayed.

## Worked Examples

### Example 1

**Question:** Is data in another process on the same host process-local?

**Reasoning:** No. It may be node-local but still require IPC, serialization, copying, permissions, and scheduling.

**Conclusion:** Name the locality boundary precisely.

### Example 2

**Question:** A local worker frees in two seconds; remote transfer adds seven seconds. Should the task wait?

**Reasoning:** If compute and output are otherwise equal and fairness/deadline permit, two seconds is less than the avoided seven. Uncertainty and opportunity cost still need bounds.

**Conclusion:** Compare estimated completion, not only immediate availability.

### Example 3

**Question:** Why can strict node affinity reduce throughput?

**Reasoning:** Hot data can constrain many tasks to a few nodes while other workers idle. A relaxed rack or remote fallback may finish more work despite transfer.

**Conclusion:** Locality preference must coexist with load balance.

### Example 4

**Question:** Three replicas occupy different nodes in one rack. Are they failure-independent?

**Reasoning:** They tolerate individual node loss but share rack power, switching, and possibly maintenance. Required rack or zone failures are not covered.

**Conclusion:** Physical separation must match the declared failure model.

### Example 5

**Question:** Why can 95% task locality accompany heavy network use?

**Reasoning:** The 5% remote tasks may contain most input bytes, and local map tasks may emit a large cross-rack shuffle.

**Conclusion:** Measure weighted locality and traffic category across the graph.

### Example 6

**Question:** Should an 80-MB dimension table be broadcast to 2,000 workers?

**Reasoning:** Disk size alone is insufficient. Measure serialized and expanded memory, concurrency, transfer tree, reuse, worker memory, and alternative shuffle cost.

**Conclusion:** Broadcast is a costed replication strategy.

### Example 7

**Question:** Why can scale-down make tomorrow's repeated query slower?

**Reasoning:** Removing warm workers discards cached blocks and decoded state. Replacement workers fetch and rebuild them from shared storage.

**Conclusion:** Elasticity decisions should price cache loss and warm-up.

### Example 8

**Question:** Can a scheduler trust a block location reported ten minutes ago?

**Reasoning:** The block may have moved, its node may have failed, or the required version may differ. Confirm identity and handle remote fallback or refresh.

**Conclusion:** Locality metadata needs freshness and safe miss behavior.

### Example 9

**Question:** When can remote execution beat local execution?

**Reasoning:** A free remote accelerator or fast service may offset transfer while the local CPU queues or lacks memory. Include output and contention before deciding.

**Conclusion:** Distance is one term in feasible completion cost.

### Example 10

**Question:** May a scheduler optimize locality for a national genomic-diagnostics pipeline without domain review?

**Reasoning:** No. Sample identity, consent, residency, clinical urgency, reference-version validity, auditability, degraded operation, and result delivery constrain placement. Named clinical-genomics, laboratory-quality, patient-safety, privacy, security, infrastructure, networking, disaster-recovery, accessibility, and independent assurance reviewers must evaluate representative and failure exercises. No external review is claimed here.

**Conclusion:** High-consequence locality policy requires domain and independent assurance beyond cost models.

## Cross-Program Connections

[LSDS-001](001-workloads-that-require-multiple-machines.md) frames locality as one reason to distribute. [LSDS-002](002-horizontal-partitioning.md) defines logical partitions, while [LSDS-003](003-range-hash-and-consistent-partitioning.md) maps keys into movable units. [LSDS-005](../ROADMAP.md) and later shuffle modules expose graph dependencies whose placement drives traffic.

[Operating Systems](../../22-operating-systems/ROADMAP.md) owns processes, scheduling, virtual memory, I/O, and NUMA mechanisms. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns caches, memory hierarchy, interconnects, and accelerators. This module lifts those locality costs into cluster dataflow decisions.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns workload scheduling, topology labels, node pools, autoscaling, isolation, and policy. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns replication, membership, consistency, and partial failure. [Data Engineering](../../19-data-engineering/ROADMAP.md) owns durable layout and pipeline behavior.

Primary systems illustrate the trade. MapReduce and HDFS couple input replicas with compute scheduling. Spark documents bounded fallback across locality levels. Delay scheduling reconciles shared-cluster fairness with a short locality wait. Snowflake's published shared-data architecture separates storage and compute and uses local cache to recover repeated-access locality.

## References

- Jeffrey Dean and Sanjay Ghemawat, [*MapReduce: Simplified Data Processing on Large Clusters*](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), OSDI, 2004. Primary data-local task scheduling and distributed execution design.
- Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung, [*The Google File System*](https://research.google/pubs/the-google-file-system/), SOSP, 2003. Primary distributed block placement, replication, and client access design.
- Matei Zaharia et al., [*Delay Scheduling: A Simple Technique for Achieving Locality and Fairness in Cluster Scheduling*](https://people.csail.mit.edu/matei/papers/2010/eurosys_delay_scheduling.pdf), EuroSys, 2010. Primary bounded-wait scheduling mechanism and evaluation.
- Apache Hadoop Project, [*HDFS Architecture Guide*](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html), checked 2026-09-03. Official current computation-to-data, replica placement, and rack-aware reading documentation.
- Apache Hadoop Project, [*HDFS Users Guide*](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html), checked 2026-09-03. Official current rack awareness, balancing, and operational guidance.
- Apache Spark Project, [*Tuning Guide: Data Locality*](https://spark.apache.org/docs/latest/tuning.html#data-locality), checked 2026-09-03. Official current process-, node-, rack-, and any-level scheduling explanation.
- Apache Spark Project, [*Configuration: Scheduling*](https://spark.apache.org/docs/latest/configuration.html#scheduling), checked 2026-09-03. Official current locality-wait controls.
- Benoit Dageville et al., [*The Snowflake Elastic Data Warehouse*](https://www.snowflake.com/wp-content/uploads/2019/06/Snowflake_SIGMOD.pdf), SIGMOD, 2016. Primary shared-data architecture and local compute-cache design.
- Abhishek Verma et al., [*Large-scale Cluster Management at Google with Borg*](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/), EuroSys, 2015. Primary placement, isolation, utilization, and correlated-failure scheduling design.
- Kubernetes Project, [*Control Topology Management Policies on a Node*](https://kubernetes.io/docs/tasks/administer-cluster/topology-manager/), checked 2026-09-03. Official current CPU, memory, device, and NUMA-alignment controls and limitations.

## Exercises

### Exercise 1

A 900-MB task needs two seconds of compute. Its local worker becomes available in three seconds and reads at 600 MB/s; a remote worker is free and transfers at 150 MB/s. Ignore other costs. Estimate both completion times and choose under a ten-second deadline.

### Exercise 2

A job reports 90 local tasks of 10 MB each and 10 remote tasks of 1 GB each. Compute task locality and byte locality. Explain which better represents network exposure.

### Exercise 3

Design a locality fallback policy for mixed 500-ms interactive tasks and five-minute batch scans. Include fairness, deadlines, stale hints, and observability.

### Exercise 4

Compare colocated HDFS-style storage/compute with object-store-backed elastic compute for repeated 20-TB scans, sporadic one-time queries, failure recovery, and cost. State what must be measured.

### Exercise 5

A regional emergency-imaging platform wants to move analysis near cached scans. Specify feasibility constraints, locality and recovery evidence, failure tests, and named human reviewers before deployment.

## Answers to the Exercises

### Answer 1

Local completion is wait `3 + 900/600 + 2 = 6.5` seconds. Remote completion is `900/150 + 2 = 8` seconds. Both meet ten seconds under the assumptions, and local is estimated 1.5 seconds faster while avoiding remote transfer. The decision should change if queue uncertainty threatens the deadline, the local copy is stale, output paths differ, or remote transfer is already cached.

### Answer 2

Task locality is `90/100=90%`. Local bytes are `90*10=900 MB`; remote bytes are `10*1000=10,000 MB`; total input is 10,900 MB, so byte locality is about `900/10900=8.26%`. The high task ratio hides that most bytes are remote. Byte locality better represents input transfer volume, but critical-path latency, link contention, and shuffle still require separate metrics.

### Answer 3

Classify locality as process, node, rack/zone, and any after hard feasibility checks. Interactive tasks should use near-zero or very short waits bounded by their latency budget; batch scans can wait longer when avoided transfer exceeds queue cost. Preserve weighted fairness by allowing another eligible job to use a slot while one waits, cap cumulative delay, and exempt urgent deadlines. Refresh stale location hints and permit identity-checked remote fallback. Measure wait by level, task and byte locality, deadline misses, queue delay, transfer, link saturation, stage tails, fairness shares, and estimation error. Test saturation, hot partitions, worker loss, missing topology, cold cache, and mixed arrivals.

### Answer 4

Colocated storage can place scan tasks on block replicas, reducing input traffic and providing warm persistent locality, but compute and storage scale together and replica placement consumes local capacity. Object storage scales durability separately and supports elastic independent warehouses, but cold workers fetch remotely and can overload shared paths; local caches help only with sufficient reuse and residence. Repeated 20-TB scans may justify retained caches or colocated layouts. Sporadic one-time queries may favor elastic shared storage despite cold reads. Measure cold/warm throughput, cache hit bytes and reuse distance, queue/startup, aggregate storage request rate, cross-zone bytes, shuffle/output, failure recovery, replica/cache rebuild, worker idle cost, storage cost, and deadline tails under concurrent tenants.

### Answer 5

Feasibility constraints include patient/study identity, image and model/reference version, clinical priority, residency, authorization, device compatibility, memory, isolation, audit logging, and declared failure domains. Evidence should report cache freshness and hit bytes, queue and transfer times, cross-region paths, completion tails by urgency, output delivery, fallback, and durable recovery. Test stale/missing scans, wrong-version caches, node/rack/region loss, partitioned networks, corrupted data, duplicate execution, retry storms, cache eviction, urgent preemption, and restore. Named review must include radiologists and clinical-imaging workflow owners, patient-safety and quality officers, privacy/data-governance, cybersecurity, network/platform and distributed-data engineers, disaster recovery, accessibility, and the applicable independent clinical-safety authority. Local checks and this answer do not provide external approval.
