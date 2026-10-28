---
module_id: LSDS-001
program: Large-Scale Data Systems Engineering
level: 1
module_number: 1
title: Workloads That Require Multiple Machines
status: complete
last_verified: 2026-08-29
---

# Workloads That Require Multiple Machines

## One-Page Review

### Governing question

When do data volume, work rate, deadline, availability, locality, or growth justify the cost and uncertainty of distributing storage or computation across machines?

### Essential definitions

- A **workload** is a distribution of data, operations, arrival patterns, deadlines, concurrency, locality, and failure expectations—not merely a dataset size.
- **Scale up** increases resources or capability within one failure/administrative unit; **scale out** divides work or state among multiple machines.
- **Parallelism** performs work simultaneously; **distribution** places work or state across independently failing, communicating components.
- **Partitionable work** can be divided into units with bounded dependencies; **serial fraction** is the portion that cannot benefit from the modeled parallel resources.
- **Aggregate throughput** is work completed per time across the system; **critical-path latency** is elapsed time along the slowest required dependency chain.
- A **failure domain** is a set of components likely to fail together because of a shared cause.
- **Coordination overhead** is time and capacity spent partitioning, scheduling, communicating, synchronizing, recovering, and combining rather than performing useful domain work.

### Central model, mechanism, or theorem

Distribution is justified only by a named unmet constraint. Estimate lower bounds independently:

`N_capacity = ceil(effective stored bytes / usable bytes per node)`

`N_rate = ceil(required work rate / sustainable work rate per node)`

`N_deadline = ceil(single-node useful work / available parallel work window)` under measured partitionability.

Then test whether `N >= max(N_capacity, N_rate, N_deadline, N_resilience, N_locality)` remains feasible after replication, skew, headroom, coordination, failures, and the serial fraction. Amdahl's fixed-work model bounds ideal speedup by `1 / (s + (1-s)/N)` before distributed overhead.

### Critical invariants

- The workload and service objective are measured at a declared boundary and time window.
- Capacity calculations include replicas, indexes, intermediate state, metadata, growth, recovery reserve, and operational headroom.
- Partitioning preserves correctness and exposes skew, hot keys, and cross-partition dependencies.
- No single component violates the stated availability or recovery objective.
- Network, storage, coordinator, and sink limits are included in the critical path.
- Benchmark evidence uses representative data distributions, concurrency, failures, and target hardware.

### Common failures

Common errors are calling data “big” without a constraint, choosing a cluster before profiling one node, dividing total bytes by advertised disk size, assuming `N` workers give `N` speedup, ignoring skew and shuffle, confusing redundancy with usable capacity, optimizing average latency while fan-out amplifies tails, scaling stateless compute around a serial sink, and claiming high availability from machine count alone.

### Compact example

An 18-TB logical dataset retained at three copies needs 54 TB before indexes and reserve. With 4 TB usable per storage node, capacity alone requires `ceil(54/4) = 14` nodes. If eight nodes satisfy ingest rate, capacity still dominates. This arithmetic is a lower bound: failure-domain placement, rebuild traffic, growth, metadata, and headroom can increase the design.

### Connections

[LSDS-002](../ROADMAP.md) develops horizontal partitioning, and [LSDS-004](../ROADMAP.md) develops locality. Workload contracts come from [Data Engineering](../../19-data-engineering/ROADMAP.md); physical limits connect to [Computer Architecture](../../23-computer-architecture/ROADMAP.md) and [Operating Systems](../../22-operating-systems/ROADMAP.md); general failure and consistency theory belongs to [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

A cluster is not a larger computer assembled from transparent parts. Each added machine introduces communication, partial failure, scheduling, ownership, monitoring, version skew, and cost. Those taxes are worthwhile when a measured requirement cannot be met economically or reliably within one machine or failure domain. Without that requirement, distribution is complexity without a governing constraint.

The right first question is not “Which distributed engine?” It is “Which workload dimension exceeds the feasible single-machine envelope, by how much, for how long, under which failures?” The answer may be storage capacity, ingest or scan throughput, computation deadline, concurrent demand, availability, geographic placement, isolation, or growth. Different constraints lead to different architectures.

Dean and Ghemawat's [MapReduce paper](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) begins from conceptually simple computations over datasets so large that hundreds or thousands of machines were required to finish in reasonable time. Its runtime handles partitioning, scheduling, communication, and failure. That historical result demonstrates both sides: distribution enables aggregate capacity, and the system must absorb complexities absent from the user function.

## Why This Matters

Premature distribution makes correctness and operations harder. A single process can use local transactions, function calls, one debugger, and direct memory. A distributed job deals with serialization, retries, duplicate attempts, data movement, slow workers, coordinator state, partial output, and recovery. These mechanisms should purchase a concrete benefit.

Waiting too long also fails. A machine with insufficient memory spills or thrashes; a daily job misses its publication window; one storage device cannot deliver the required scan rate; one host becomes an unacceptable failure domain; a remote dataset cannot be moved within the deadline. A disciplined scale decision reveals the limiting resource before outages force an emergency redesign.

The distinction matters financially. Distributed services often charge across compute time, stored replicas, requests, shuffle bytes, egress, coordination, and idle headroom. A faster job can cost more total resources. Conversely, using many inexpensive workers can be economically rational when work is embarrassingly parallel and deadlines matter. Architecture follows the workload and price/performance evidence.

## Prerequisites and Retrieval

You should understand CPU, memory, storage, network throughput, latency, files, databases, processes, and basic probability. Recall that a percentile is a property of a measured distribution, throughput differs from latency, and a replica is an additional copy rather than extra logical capacity. You should be able to manipulate ratios, maxima, and ceiling division and to distinguish a logical dataset from its physical encodings and intermediate state.

## Learning Objectives

After completing this module, you should be able to:

- characterize a data workload along volume, rate, deadline, concurrency, locality, and failure dimensions;
- distinguish scaling up, parallel processing, and distributed processing;
- derive capacity, rate, and deadline lower bounds for worker count;
- apply Amdahl's fixed-work speedup bound and explain its limitations;
- identify workloads that partition cleanly and those dominated by shared state or serial stages;
- account for replication, skew, shuffle, headroom, rebuild, and tail latency;
- distinguish availability requirements from raw machine count;
- design a scale experiment beginning with a strong single-node baseline;
- reject unjustified cluster designs and identify viable alternatives;
- scope human review for high-consequence distributed data workloads.

## Core Exposition

A workload description begins with **logical work**. Identify records, bytes, keys, operations, transformations, outputs, and correctness rules. Then describe distributions: sizes, key popularity, arrival bursts, event time, selectivity, fan-out, concurrency, and growth. Finally declare service objectives: completion deadline, freshness, throughput, latency percentiles, availability, recovery, durability, and cost boundary.

The adjective “large” is relative. Ten terabytes may fit comfortably on one storage server but exceed one GPU's memory. A 100-gigabyte table may be small for batch storage yet too large for a 200-millisecond join. A stream of tiny events can require multiple machines because of rate, while a petabyte archive can remain on cold storage if accessed rarely. State the violated constraint, not a fashionable size label.

**Scaling up** adds CPU cores, memory, faster storage, accelerators, or a larger machine. It preserves many single-machine advantages and should be evaluated seriously. Limits include maximum hardware size, nonlinear price, maintenance windows, failure-domain concentration, and unavailable aggregate I/O. Scaling up may remain the simplest and cheapest design even when a cluster is technically possible.

**Scaling out** partitions state or work across machines. It can increase aggregate capacity and parallel throughput, isolate tenants or jobs, place work near data, and survive selected component failures. It also makes coordination and recovery first-class. Scaling out is not identical to parallelism: one machine can run parallel threads, and several machines may form a distributed but effectively serial pipeline.

Classify the constraint. A **capacity constraint** occurs when the effective state cannot fit with required redundancy and headroom. A **rate constraint** occurs when sustained input or output exceeds a component's safe throughput. A **deadline constraint** occurs when total work cannot complete within a window. A **concurrency constraint** occurs when active requests exceed service capacity while meeting latency. A **resilience constraint** occurs when one failure domain cannot satisfy availability or recovery. A **locality constraint** occurs when data, users, or policy require computation in several places.

Start with a single-node baseline. Measure parsing, decompression, computation, memory, temporary state, storage reads/writes, and result emission separately. Use realistic encodings, data distribution, and concurrency. Saturate one resource at a time where possible. If one node uses 20% CPU and waits on a remote serial database, adding workers can amplify contention rather than improve throughput.

Capacity math must distinguish logical and physical bytes. Let logical data be `L`, replication or coding expansion be `r`, index/metadata factor `i`, temporary/intermediate factor `m`, growth factor `g`, and safe utilization `u < 1`. Approximate effective bytes as `L * r * (1+i+m) * g`, then divide by physical capacity times `u`. The factors may not multiply uniformly, so a real design models each tier separately.

Advertised disk capacity is not usable capacity. Reserve space for recovery, compaction, spills, operating system, metadata, imbalance, and failure. A cluster that fits only when perfectly balanced cannot restore redundancy after loss. Storage request-rate and bandwidth limits can dominate long before bytes fill the devices.

Rate math also needs the entire path. For ingest, include producer network, broker or filesystem, validation, indexing, replication, acknowledgement, and downstream sink. The minimum worker count is the maximum across bottleneck stages, not the sum of headline per-node throughput. Sustainable rate under mixed workload and target tail latency matters more than a short sequential benchmark.

Deadline math begins with useful work divided by available time, but parallel speedup is bounded. If a fraction `s` of fixed execution time is serial and the rest divides perfectly among `N` workers, ideal speedup is:

`Speedup_A(N) = 1 / (s + (1-s)/N)`.

With `s = 0.10` and `N = 14`, ideal speedup is about `6.09`, not fourteen. This formulation associated with [Amdahl's 1967 paper](https://doi.org/10.1145/1465482.1465560) excludes communication, imbalance, failure, and new overhead, so it is an optimistic bound under its assumptions.

Gustafson's [1988 reevaluation](https://doi.org/10.1145/42411.42415) considers scaled workloads: more processors may solve a larger parallel portion in the same elapsed time. The models answer different questions. Amdahl asks about accelerating fixed work; Gustafson asks about increasing problem size under a fixed time budget. Engineers must state which workload remains fixed.

Partitionability decides whether aggregate resources help. Record-local parsing, compression, image transformation, simulation trials, and many independent aggregates divide naturally. Global sort, graph traversal, exact distinct counting, joins on skewed keys, iterative models, and transactions across shared constraints require data exchange or coordination. Some still scale, but movement and synchronization can dominate.

Partitioning creates balance obligations. Equal byte ranges do not guarantee equal work if records vary in complexity. Hash partitions do not balance a key whose frequency dominates the dataset. A single hot partition determines stage completion. Measure distribution tails, per-key work, partition sizes, and worker task time rather than relying on averages.

**Data movement** is often the main distributed cost. Reading data near its storage avoids network traffic; a shuffle deliberately moves records to group related keys. Compare input bytes, filtered bytes, intermediate bytes, and output bytes. Compression trades CPU for network/storage. Broadcasting a small relation may avoid repartitioning a large one. These mechanisms are developed later; the foundational point is to budget movement explicitly.

Distribution changes failure assumptions. In a thousand-machine fleet, some component is frequently slow, restarting, partitioned, or under maintenance. The [Google File System paper](https://research.google/pubs/the-google-file-system/) designed around component failure as an expected condition for large clusters. That does not mean every failure is harmless. The application needs a fault model, replicated or reconstructible state, detection, retries with safe effects, repair capacity, and tested recovery.

More replicas do not automatically give availability. Correlated rack, zone, software, configuration, identity, control-plane, or human failures can affect all copies. Place replicas across the failure domains named by the objective and retain enough capacity to serve and rebuild during failures. A coordinator, metadata service, name service, authentication dependency, or sink can remain a single point of failure.

Fan-out amplifies latency tails. If a request waits for many parallel leaves, the slowest required leaf controls completion. Even a rare slow response becomes common at request level when many leaves participate. Dean and Barroso's [*The Tail at Scale*](https://research.google/pubs/the-tail-at-scale/) analyzes techniques for forming predictable services from variable components. Report end-to-end percentiles under fan-out, not only median worker latency.

Large clusters need scheduling and isolation. Workers differ, workloads contend, tasks have placement constraints, and reservations create fragmentation. Google's [Borg paper](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) describes admission, packing, overcommitment, sharing, availability support, and operational tooling across large heterogeneous fleets. A cluster manager removes repetitive mechanics from users; it does not eliminate capacity, interference, or policy decisions.

Geography can independently require several machines or sites. Serving distant users, processing near instruments, respecting placement policy, or continuing after a site failure may justify distribution even for small data. Wide-area links add latency, limited bandwidth, cost, and partitions. A geographic replica chosen for availability may also introduce consistency and failover semantics owned by later courses.

Serverless and managed services do not remove distribution. They transfer mechanism ownership while the application still experiences quotas, partition keys, retries, ordering, hot spots, cost, and partial failures. “Autoscaling” is a control loop with delay and maximum limits, not infinite instantaneous capacity.

Choose alternatives before committing to a cluster. Improve algorithm or representation; filter earlier; compress; use a stronger single machine; process incrementally; relax exactness; precompute; schedule a longer window; move compute to data; separate hot and cold paths; or use a managed specialized system. Each changes assumptions and may avoid distributed generality.

## Definitions and Notation

Let workload `W` have logical data volume `L`, input rate `lambda`, deadline `D`, single-node sustainable service rate `mu`, per-node usable capacity `C`, physical expansion factor `R`, and headroom factor `h > 1`. Simplified lower bounds are:

- `N_capacity = ceil(L * R * h / C)`;
- `N_rate = ceil(lambda * h / mu)`;
- `N_min = max(N_capacity, N_rate, N_deadline, N_resilience, N_locality)`.

Let `s` be serial fraction in the measured single-node runtime. Amdahl's ideal fixed-work speedup is `S_N = 1 / (s + (1-s)/N)`, with efficiency `E_N = S_N/N`. Real distributed time can be decomposed as:

`T_N = T_serial + T_parallel/N + T_partition + T_move + T_coordinate + T_imbalance + T_recovery`.

These terms depend on `N`, data distribution, and failures; they are not constants in general. A **strong-scaling experiment** holds total problem size fixed while changing resources. A **weak-scaling experiment** grows problem size with resources. A **bottleneck** is the limiting resource or dependency at the measured operating point; it can move after optimization.

## Mechanisms, Invariants, or Proof Structure

A defensible multi-machine decision proceeds in five steps. First, establish correctness and service objectives. Second, measure the strongest practical single-machine baseline. Third, derive independent capacity, rate, deadline, resilience, and locality lower bounds. Fourth, prototype the partition and quantify movement, skew, serial work, tails, failure recovery, and cost. Fifth, test target and degraded scenarios and record why simpler alternatives fail.

The following executable arithmetic demonstrates separate capacity and rate bounds plus Amdahl's ideal fixed-work speedup. It assumes 18 TB logical data, three full copies, 4 TB usable per storage node, 24 Gb/s required ingest, and 3 Gb/s sustainable ingest per worker. It is a unit-consistent toy model, not production sizing; indexes, growth, headroom, failure placement, rebuild, network topology, and price are intentionally excluded.

<!-- bijux-verify: {"id":"multi-machine-lower-bounds","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"capacity_nodes=14\nthroughput_nodes=8\nminimum_nodes=14\namdahl_speedup_at_14=6.09\n","stderr":""}} -->
```python
def ceil_div(numerator, denominator):
    return (numerator + denominator - 1) // denominator


logical_tb = 18
copy_count = 3
usable_tb_per_node = 4
required_ingest_gbps = 24
sustainable_ingest_gbps_per_node = 3

capacity_nodes = ceil_div(logical_tb * copy_count, usable_tb_per_node)
throughput_nodes = ceil_div(required_ingest_gbps, sustainable_ingest_gbps_per_node)
minimum_nodes = max(capacity_nodes, throughput_nodes)

serial_fraction = 0.10
ideal_speedup = 1 / (serial_fraction + (1 - serial_fraction) / minimum_nodes)

print(f"capacity_nodes={capacity_nodes}")
print(f"throughput_nodes={throughput_nodes}")
print(f"minimum_nodes={minimum_nodes}")
print(f"amdahl_speedup_at_14={ideal_speedup:.2f}")
```

The calculation proves only the stated arithmetic. A real plan must use bytes and bits consistently, separate storage and ingest roles if they differ, and validate sustained performance. The copy count may satisfy durability under some failures but does not itself establish availability.

## Alternatives and Trade-Offs

**Scale up versus scale out.** Scaling up reduces coordination and operational surface. Scaling out increases aggregate capacity and failure-domain options. Compare total cost, maximum size, repair, maintenance, performance variance, and required skills—not only purchase price.

**Batch versus incremental processing.** Recomputing a full dataset can be simple and reproducible but miss deadlines as history grows. Incremental processing reduces recurring work but introduces change capture, state, correction, and replay obligations.

**Exact versus approximate results.** Sampling, sketches, and approximate queries can fit one machine or reduce communication. They are acceptable only when error bounds and decision consequences are explicit. High-stakes exact constraints cannot be relaxed for convenience.

**Shared cluster versus dedicated resources.** Sharing improves utilization and elasticity but introduces interference, queues, and policy. Dedicated capacity improves isolation and predictability at the cost of idle resources. Reservations and priority can create hybrids.

**Replication versus recomputation.** Replication reduces read/recovery time but consumes storage and write bandwidth. Deterministic intermediate state may be cheaper to recompute, provided inputs remain available and the recovery deadline permits it.

**Move data versus move computation.** Centralizing data simplifies some processing but costs network, egress, time, and policy exposure. Running computation near sources reduces movement but complicates deployment and result combination. Select based on data/work ratio and constraints.

## Failure Modes and Misconceptions

1. **Multiple machines are inherently faster.** Communication, serial work, skew, and contention can make them slower.
2. **Data volume alone defines scale.** Rate, deadline, concurrency, locality, availability, and access pattern can dominate.
3. **Three replicas triple capacity.** They triple physical bytes while preserving one logical value.
4. **CPU utilization below 100% means spare capacity.** Memory, network, storage, locks, quotas, or tails may limit service.
5. **Average partition size predicts job time.** The slowest critical partition determines stage completion.
6. **Autoscaling removes capacity planning.** Scaling has signals, delays, quotas, granularity, warm-up, and cost.
7. **Retries make failure transparent.** Non-idempotent effects, lost coordinator state, poison records, and correlated failures remain.
8. **High availability follows from node count.** Shared dependencies and failure domains may defeat every replica.
9. **A microbenchmark predicts production.** Encoding, distributions, concurrency, interference, failures, and sinks change results.
10. **Once distributed, every stage should be parallel.** Small or serial stages may be safer and faster on one coordinator if they do not violate objectives.

## Worked Examples

### Example 1

**Question:** A 2-TB compressed archive is scanned once monthly with a 12-hour window. Does it require a cluster?

**Reasoning:** Measure one machine's sequential scan and processing rate. At 100 MB/s, raw scan time is about 5.6 hours before computation, within the window. A stronger single machine or incremental index may suffice.

**Conclusion:** Terabyte size alone does not justify distribution.

### Example 2

**Question:** A 200-GB fraud table must be joined against 80,000 events per second with a 100-ms objective. Why might several machines be required?

**Reasoning:** The table may fit one host, but concurrent rate and tail latency may exceed its CPU, memory-bandwidth, or network envelope. Partitioned keyed state can add aggregate service capacity, subject to hot-key and consistency analysis.

**Conclusion:** Rate and latency can dominate storage capacity.

### Example 3

**Question:** A job has serial fraction 0.25. What is its Amdahl limit as worker count grows?

**Reasoning:** `lim S_N = 1/s = 4`. Even perfect parallel execution cannot exceed fourfold fixed-work speedup under the model. Distribution overhead lowers the observed result.

**Conclusion:** Reduce serial work before buying unbounded workers.

### Example 4

**Question:** Why can 100 equal-size partitions run unevenly?

**Reasoning:** Records can have different parse costs, keys can produce different aggregation state, hardware can differ, and workers can contend or pause. Equal bytes do not imply equal CPU, memory, network, or elapsed work.

**Conclusion:** Balance the cost distribution, not merely partition count.

### Example 5

**Question:** A cluster adds workers but a job does not accelerate. What should be inspected?

**Reasoning:** Measure source/sink throughput, coordinator scheduling, serial stages, shuffle, hot partitions, task granularity, worker utilization, memory spills, network, and tail tasks. The limiting resource may be outside worker CPU.

**Conclusion:** Scaling diagnosis follows the critical path.

### Example 6

**Question:** Does three-zone placement guarantee survival of a zone failure?

**Reasoning:** Only if sufficient independent replicas, metadata/control services, network paths, identity, and serving capacity remain, and failover operates correctly. A shared software rollout can still fail all zones.

**Conclusion:** Availability is an end-to-end fault-model claim.

### Example 7

**Question:** A request fans out to 100 workers, each slow beyond the deadline with probability 0.001 independently. What is the chance at least one is slow?

**Reasoning:** The chance none is slow is `0.999^100`, about 0.905. Therefore at least one is slow about 9.5% of the time, far above 0.1%. Dependence can make the estimate better or worse.

**Conclusion:** Rare component tails become common at fan-out scale.

### Example 8

**Question:** When is geographic distribution required for a small dataset?

**Reasoning:** A 5-GB dataset may need local copies for disconnected instruments, regional latency, site-failure continuity, or placement policy. The driver is locality/resilience, not volume.

**Conclusion:** Small data can have inherently distributed constraints.

### Example 9

**Question:** Can more workers fix a slow exact global distinct count?

**Reasoning:** Workers can build partial sets, but exact combination must exchange or coordinate all distinct identities. If cardinality is enormous, network and final state dominate. An approximate sketch changes the contract and may be viable.

**Conclusion:** Algorithm and result semantics determine scalability.

### Example 10

**Question:** A disaster-warning pipeline must finish satellite-image analysis in eight minutes. Is a calculated 40-node minimum sufficient evidence?

**Reasoning:** No. Image distribution, cloud cover, model behavior, source arrival, network, accelerator variance, retries, degraded capacity, alert authority, false results, and downstream delivery require tests and named meteorological, emergency-management, remote-sensing, model, safety, operations, security, accessibility, and independent reviewers. No external review is claimed here.

**Conclusion:** High-consequence scale plans require domain validation and degraded-system evidence.

## Cross-Program Connections

Computer architecture supplies cache, memory, storage, accelerator, and interconnect limits that shape a node's envelope. Operating systems supply processes, filesystems, virtual memory, scheduling, and local failure behavior. Network engineering supplies bandwidth, delay, loss, topology, and congestion constraints. Algorithm engineering determines partitionability, work, communication, and approximation.

Data engineering defines pipelines, semantics, and service expectations; this program owns the cluster-scale execution and storage mechanisms. Distributed Systems Engineering develops general models of partial failure, time, consistency, replication, and consensus. Database Engineering owns transaction and query internals outside this program's analytical-scale mechanisms.

Warehouse-scale systems treat a datacenter as an integrated computer rather than independent servers; Barroso, Hölzle, and Ranganathan's open-access [*The Datacenter as a Computer*, third edition](https://doi.org/10.1007/978-3-031-01761-2) develops that perspective. The engineering lesson is that fleet-level performance depends on hardware, network, power, cooling, software, and workload together.

## References

- Gene M. Amdahl, [*Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities*](https://doi.org/10.1145/1465482.1465560), AFIPS Spring Joint Computer Conference, 1967. Primary fixed-work parallel-speedup argument.
- John L. Gustafson, [*Reevaluating Amdahl's Law*](https://doi.org/10.1145/42411.42415), Communications of the ACM 31(5), 1988. Primary scaled-workload perspective.
- Jeffrey Dean and Sanjay Ghemawat, [*MapReduce: Simplified Data Processing on Large Clusters*](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), OSDI, 2004. Primary cluster data-processing abstraction and implementation paper.
- Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung, [*The Google File System*](https://research.google/pubs/the-google-file-system/), SOSP, 2003. Primary workload-driven distributed storage and fault-tolerance paper.
- Jeffrey Dean and Luiz André Barroso, [*The Tail at Scale*](https://research.google/pubs/the-tail-at-scale/), Communications of the ACM 56(2), 2013. Primary analysis of latency variability and fan-out.
- Luiz André Barroso, Urs Hölzle, and Parthasarathy Ranganathan, [*The Datacenter as a Computer*, third edition](https://doi.org/10.1007/978-3-031-01761-2), 2019. Open-access warehouse-scale computing foundation.
- Abhishek Verma et al., [*Large-Scale Cluster Management at Google with Borg*](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/), EuroSys, 2015. Primary fleet scheduling, isolation, availability, and operational evidence.
- Matei Zaharia et al., [*Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing*](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf), NSDI, 2012. Primary lineage/recomputation-based cluster data abstraction.
- Martin Kleppmann and Chris Riccomini, [*Designing Data-Intensive Applications*, second edition](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/), O'Reilly Media, 2026. Current durable treatment of distributed-versus-single-node trade-offs and data-system foundations.

## Exercises

### Exercise 1

Name five independent workload constraints that can justify multiple machines, and give one example where a large dataset still does not require them.

### Exercise 2

A 30-TB logical store keeps two full copies, requires 25% free operational reserve, and uses nodes with 6 TB physical capacity. Derive a capacity lower bound. State at least four omitted factors.

### Exercise 3

A fixed-size job takes 120 minutes on one machine. Profiling estimates serial fraction 0.15. Compute ideal Amdahl speedup and runtime for 16 workers, then explain why an observed 14-minute runtime is plausible even if the model predicts less.

### Exercise 4

Compare scaling up and scaling out for a 6-TB graph analysis that currently takes ten hours and must finish in four. Produce an experiment plan rather than selecting a product.

### Exercise 5

A national genomic-surveillance program must process uploaded sequences within six hours during outbreaks and continue through a site outage. Define the technical evidence and named human-review roles required to justify a multi-site design. Include privacy, scientific validity, skew, cost, and degraded operation.

## Answers to the Exercises

### Answer 1

Independent constraints include physical storage capacity, sustained ingest/query rate, computation deadline, concurrent request/tail-latency capacity, availability/recovery across failure domains, and geographic or policy locality. Any five with boundaries suffice. A 20-TB compressed archive scanned quarterly in a 48-hour window may fit and finish on one storage-rich server; measured scan and compute rates, failure tolerance, and economics decide. “20 TB” alone does not.

### Answer 2

Two copies require `30 * 2 = 60 TB`. Keeping 25% free means usable fraction is `0.75`, so each 6-TB node contributes `4.5 TB` safe capacity. The lower bound is `ceil(60/4.5) = ceil(13.33...) = 14` nodes. Omissions include indexes/metadata, compression uncertainty, temporary spill and compaction, imbalance, future growth, failed-node/rebuild reserve, request/bandwidth limits, rack or zone placement, coordinator state, and storage overhead. The arithmetic does not establish durability or availability.

### Answer 3

`S_16 = 1 / (0.15 + 0.85/16) = 1 / 0.203125`, approximately `4.923`. Ideal runtime is `120 / 4.923`, approximately `24.38 minutes`. A 14-minute result exceeds the fixed-work model's ideal prediction, so at least one assumption differs: the “one machine” run may spill or throttle while distributed aggregate memory avoids it; caches, algorithm, input, hardware, or measured scope may differ; the serial fraction estimate may be wrong; or workers may perform less total work. Audit comparability before claiming superlinear speedup.

### Answer 4

First profile the single-node critical path: graph representation, memory footprint, storage read, CPU, traversal frontier, communication-equivalent work, and output. Test a larger-memory/faster-storage machine and an improved compressed/sparse representation. Establish whether the algorithm partitions by vertex/edge ranges, how frontier messages and high-degree vertices skew work, and which stages are serial. Then run strong-scaling experiments at 1, 2, 4, 8, and 16 nodes on identical input, recording elapsed stages, bytes moved, imbalance, memory, cost, failures, and result equality. Test a worker loss and degraded capacity. Choose scale up if it meets four hours with lower complexity and acceptable failure risk; choose scale out only if evidence meets correctness, deadline, recovery, and cost.

### Answer 5

Characterize normal and outbreak arrival distributions, sequence sizes, reference/model versions, quality-control work, pathogen-specific skew, deadline semantics, result destinations, retention and correction. Benchmark representative and adversarial samples on target compute, storage and network; model capacity, replication, headroom, source/sink limits, serial stages, locality and cost. Test site loss, link partition, delayed uploads, duplicate submissions, corrupted data, reference updates, privacy-control failure, backlog recovery and cross-site reconciliation. Prove result equivalence or defined tolerance and preserve provenance. Named reviewers should include genomic epidemiologists, laboratory/bioinformatics experts, public-health decision authorities, clinical/domain safety experts, privacy/legal and research-ethics authorities, cybersecurity, records/data governance, distributed-systems and data engineers, network/site operators, incident management, finance/procurement, accessibility/public communication, participating jurisdictions, and independent scientific and operational assurance. No automated model or chapter authorizes deployment; external review and outbreak exercises are required.
