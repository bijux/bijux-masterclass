---
module_id: CONPAR-093
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 93
title: NUMA-Aware Allocation and Scheduling
status: complete
last_verified: 2026-08-29
---

# NUMA-Aware Allocation and Scheduling

## One-Page Review

### Governing question

How should threads, processes, pages, tasks, devices, and communication endpoints be placed so that most critical-path accesses use appropriate local resources, while preserving memory capacity, balance, correctness, portability, and recoverability?

### Essential definitions

- A **NUMA node** groups processors and memory with a locality relationship; access cost/bandwidth can differ by source CPU and target memory.
- **CPU affinity** constrains where a thread/process may execute; **memory policy** guides where pages are allocated.
- **first touch** means a demand-allocated page is commonly placed according to the policy/locality of the thread that first causes allocation, usually by writing anonymous memory.
- **local allocation** prefers memory associated with the executing CPU; **bind** restricts allocation to a node set; **preferred** favors nodes with fallback; **interleave** distributes allocations across a node set.
- A **cpuset** constrains allowed CPUs/memory nodes; it can override or narrow an application's choices.
- **page placement** maps physical pages to nodes; virtual allocation alone does not establish physical placement.
- **remote access** crosses a locality boundary and may have higher latency or consume interconnect bandwidth.
- **page migration** moves populated pages; it costs bandwidth, disrupts caches/TLBs, and may fail or only partially succeed.
- **automatic NUMA balancing** is an operating-system mechanism that observes access and may migrate pages/tasks; behavior and suitability are workload/system specific.
- **memory affinity** is the relationship between compute placement and the pages it accesses.
- **NIC/GPU affinity** aligns CPU threads and memory with nearby I/O/accelerator devices where topology exposes such locality.
- A **placement generation** identifies a coherent mapping of workers, data, pages, and devices.

### Central model, mechanism, or theorem

For worker r and memory node n, let `Q_rn` be bytes/accesses on the critical interval and `c_rn` their measured cost. A placement objective can minimize `sum Q_rn*c_rn` subject to CPU, memory-capacity, device, ownership, and balance constraints. This is a diagnostic optimization model, not a universal latency equation. Correct NUMA control requires both execution affinity and page policy/initialization: pinning threads after a serial initializer may leave pages remote; changing policy after population may affect only future allocation unless pages are explicitly migrated.

### Critical invariants

Actual topology and scheduler/cgroup constraints are discovered at runtime; logical IDs are never assumed to encode physical proximity; every worker's CPU/place and every important region's allocation/policy/page distribution are observable; initialization touches pages from their intended owners; page sizes and shared mappings are accounted for; capacity/high-water and fallback behavior are safe; task movement does not silently destroy data locality; NIC/GPU mappings align when beneficial; migrations are bounded, validated, and amortized; output/numeric behavior remains valid; and rollback restores a known placement/configuration.

### Common failures

Teams pin threads but not memory, initialize a parallel array from one thread, assume `malloc` physically allocates, equate node numbers with distance, use interleave as a universal cure, bind beyond allowed cpusets, oversubscribe cores, ignore SMT/cache sharing, migrate hot pages repeatedly, measure aggregate remote counters without attribution, compare different page-cache states, let work stealing move computation away from data, forget GPU/NIC locality, use huge pages without revisiting placement granularity, optimize average bandwidth while one socket controls completion, or claim lower remote traffic proves end-to-end speedup.

### Compact example

Four equal page blocks are intended for workers on nodes `[0,0,1,1]`. Serial first touch by a node-0 initializer yields page nodes `[0,0,0,0]`, so two of four blocks are remote. Parallel owner touch yields `[0,0,1,1]`, making all blocks local under this simplified model. It demonstrates placement logic only; real page allocation, sharing, migration, counters, and performance require system evidence.

### Connections

[False Sharing and Cache-Line Contention](029-false-sharing-and-cache-line-contention.md) addresses cache-line ownership within/between sockets. [Load Imbalance Across Nodes](088-load-imbalance-across-nodes.md) separates placement from work skew. [Roofline and Operational-Intensity Analysis](092-roofline-and-operational-intensity-analysis.md) supplies hierarchy traffic ceilings. The [program roadmap](../ROADMAP.md) next composes threads, SIMD, accelerators, and message passing.

## Governing Question

Which workers consume which pages and devices on the critical path, what placement policy makes those accesses local without violating capacity or balance, and is the measured benefit stable enough to repay initialization, migration, scheduling, and portability cost?

NUMA awareness is a mapping problem spanning runtime, allocator, operating system, scheduler, and algorithm. A single launch flag rarely owns all layers.

## Why This Matters

Modern multi-socket servers, chiplets, memory tiers, accelerators, and NICs expose nonuniform locality. A program can be race-free and balanced yet run slowly because compute is separated from pages or devices. Bandwidth-intensive kernels often saturate one memory controller when pages were initialized serially, while other controllers sit idle.

Affinity also stabilizes experiments. Unbound threads migrate, changing cache/NUMA behavior across runs. But excessive binding can block load balance, conflict with scheduler constraints, or overfill memory. Interleave can spread bandwidth while harming latency/local reuse. Dynamic/adaptive workloads require choices between moving tasks, data, or both.

Production-grade placement begins with discovery, models ownership, applies explicit policy, verifies actual results, and measures complete execution. It also handles allocation failure, cpuset changes, page migration, checkpoint/restart, and heterogeneous devices.

## Prerequisites and Retrieval

Retrieve:

- cache coherence, false sharing, memory ordering, and affinity effects from [False Sharing and Cache-Line Contention](029-false-sharing-and-cache-line-contention.md) and [Reasoning About a Weak-Memory Program](030-reasoning-about-a-weak-memory-program.md);
- scheduling, stealing, imbalance, topology, and scaling from [Load Balance and Scheduling Overheads](046-load-balance-and-scheduling-overheads.md), [Work Stealing](047-work-stealing.md), [Load Imbalance Across Nodes](088-load-imbalance-across-nodes.md), and [Scaling a Parallel Program Across Multiple Nodes](090-scaling-a-parallel-program-across-multiple-nodes.md); and
- memory traffic and GPU hierarchy from [Roofline and Operational-Intensity Analysis](092-roofline-and-operational-intensity-analysis.md) and [GPU Memory Hierarchies](076-gpu-memory-hierarchies.md).

Retrieval prompt: record allowed CPUs/nodes, sockets/NUMA/caches/cores/SMT, distance/bandwidth matrix, NICs/GPUs, scheduler/cgroup policy, ranks/threads/tasks, major regions/page sizes/mappings, allocation/touch order, ownership/access matrix, memory high-water, current affinity/policy/page distribution, migration/automatic-balancing state, critical phase/counters, candidate mapping, result oracle, and fallback.

## Learning Objectives

After completing this module, a learner can:

1. distinguish CPU binding, memory policy, page placement, and device affinity;
2. explain demand allocation and first-touch effects for important mapping types;
3. discover actual topology and allowed resources without assuming numeric IDs;
4. design owner-initialization, local, bind, preferred, and interleave policies;
5. model access cost under capacity, balance, ownership, and device constraints;
6. verify thread placement and physical page distribution using supported tools;
7. diagnose remote access, bandwidth imbalance, task movement, and device/NIC locality;
8. decide when bounded migration or automatic balancing is justified;
9. validate performance, memory capacity, correctness, and portability across placements; and
10. scope security, operations, and high-stakes review.

## Core Exposition

### Discover topology and constraints

Query, do not infer. Record sockets/packages, NUMA nodes, cores, processing units/SMT, cache sharing, memory capacity, distance matrices, GPUs, NICs, and OS support. Hardware-locality libraries expose topology and binding capabilities, but the process may see a restricted view inside a scheduler allocation/container/cgroup.

Allowed CPU and memory node masks are hard constraints. Linux cpusets can constrain memory allocation before a narrower application policy. CPU numbering can change with firmware, BIOS, VM/container, or scheduler. Save topology and effective masks with the run.

Measure topology-specific latency and sustainable bandwidth carefully with representative page size, access pattern, read/write mix, concurrency, and placement. A distance number is not nanoseconds or GB/s. Avoid intrusive benchmarks in production.

### CPU affinity is not memory placement

Binding a thread defines where it may run; it does not retroactively relocate pages. A virtual address allocation reserves address space/metadata, while physical anonymous pages commonly appear on demand when accessed. If one thread writes an entire array before workers are pinned, pages may concentrate near that initializer.

Owner first-touch initializes each block using the worker/place that will consume it. Keep initialization parallel, deterministic where needed, and aligned with page boundaries. False sharing at boundaries can still cause coherence traffic even when pages are local. With shared/read-mostly data, interleave or replication may outperform one owner, subject to memory and consistency.

File-backed/shared mappings, zero pages, allocator arenas, transparent/explicit huge pages, copy-on-write, device memory, and language runtimes can change the simple story. Consult platform semantics and verify actual placement.

### Executable placement model

This deterministic model compares serial and owner first-touch for four blocks. It neither allocates operating-system pages nor measures topology, migrations, traffic, or performance.

<!-- bijux-verify: {"id":"numa-first-touch-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"worker_nodes=[0, 0, 1, 1]\nserial_touch_page_nodes=[0, 0, 0, 0]\nserial_remote_blocks=2\nowner_touch_page_nodes=[0, 0, 1, 1]\nowner_remote_blocks=0\nserial_local_fraction=0.500000\nowner_local_fraction=1.000000\n","stderr":""}} -->
```python
worker_nodes = [0, 0, 1, 1]
serial_pages = [0, 0, 0, 0]
owner_pages = worker_nodes[:]


def remote_blocks(page_nodes):
    return sum(page != worker for page, worker in zip(page_nodes, worker_nodes))


serial_remote = remote_blocks(serial_pages)
owner_remote = remote_blocks(owner_pages)
print(f"worker_nodes={worker_nodes}")
print(f"serial_touch_page_nodes={serial_pages}")
print(f"serial_remote_blocks={serial_remote}")
print(f"owner_touch_page_nodes={owner_pages}")
print(f"owner_remote_blocks={owner_remote}")
print(f"serial_local_fraction={(len(worker_nodes) - serial_remote) / len(worker_nodes):.6f}")
print(f"owner_local_fraction={(len(worker_nodes) - owner_remote) / len(worker_nodes):.6f}")
```

### Memory policies

Default/local allocation generally follows the allocating/touching CPU subject to allowed resources and fallback. A bind policy restricts allocation to nodes and can fail or force undesirable behavior under pressure. Preferred policy favors a node/set with defined fallback. Interleave distributes pages across nodes, useful for shared streaming bandwidth but potentially remote for every worker.

Policies have scope: process/thread default or specific virtual ranges. In Linux, range policy can govern future allocations; changing policy does not necessarily move already populated pages unless migration flags/APIs are used. Semantics vary for anonymous, private file, shared, and huge-page mappings. Library interfaces are usually preferable to raw syscalls.

Choose by access. Private owner-compute regions favor local/bind/preferred with owner touch. Uniformly shared read-only streams may favor interleave or replication. A small frequently read table may fit shared cache. Capacity-limited data may need weighted distribution. Allocation failure and fallback must be safe and observable.

### Placement objective and constraints

Build an access matrix `Q_rn` from algorithmic ownership plus measurements. Estimate cost with local/remote latency/bandwidth and concurrency, but avoid claiming additivity when accesses overlap. Minimize critical-path cost, not aggregate traffic alone.

Constraints include per-node memory high-water/headroom, CPU/device eligibility, unique data ownership, cache/NUMA/NIC/GPU locality, thread balance, page granularity, shared state, and scheduler masks. Multi-objective choices trade compute balance against memory bandwidth and interconnect traffic.

Partition by stable domains. One rank per NUMA node plus local threads is often interpretable; more/fewer ranks can change MPI/shared-memory overhead. Overdecomposed tasks need locality hints and bounded stealing. Do not hard-code a layout without topology discovery.

### Verify actual affinity and placement

At startup and during diagnostics, record effective CPU masks and sampled/current CPU for each worker, OpenMP/runtime place mappings, rank-to-host/socket/node/core/device mapping, and oversubscription. Tool support may report requested policy even when strict enforcement failed; query return codes/capabilities.

For pages, inspect supported per-range/page residency, process NUMA maps/statistics, and memory-policy queries. Sampling can be costly and racy; aggregate counters may not attribute a region. Correlate page distribution with region addresses/ownership and per-node bandwidth/remote-access counters.

Verify after initialization, steady state, migration, and restore. A correct initial map can drift through task movement, reallocations, automatic balancing, allocator arenas, or adaptive repartitioning.

### Scheduling and locality

Static ownership keeps computation near data and is effective for regular work. Dynamic queues/work stealing improve load balance but can create remote accesses. Hierarchical scheduling first steals within a NUMA node, then across nodes; move a task only when saved idle time exceeds locality loss.

Attach a home/place/generation hint to tasks and allocate task-owned buffers locally. Do not make affinity hints correctness dependencies unless the runtime guarantees them. A stolen task can access home data remotely, migrate/recreate data, or transfer ownership; each has cost and synchronization implications.

Parallel libraries and nested runtimes can create extra pools and oversubscription. Coordinate rank, OpenMP/TBB/task runtime, BLAS, and device threads. Binding all layers independently can stack workers on the same core.

### Page migration and automatic balancing

Migration can repair bad first touch or follow a long-lived ownership change. It copies pages, consumes bandwidth, invalidates mappings/caches/TLB state, and may not move pinned/shared/huge/device-associated pages. Concurrent writers need OS-supported semantics, but application-level performance and ownership invariants still require validation.

Use a cost horizon: migrate only when predicted remote-access savings over stable future work exceed measurement, copy, disruption, and failure costs with margin. Add hysteresis/cooldown and byte/frequency caps. Avoid oscillation when tasks and pages chase each other.

Automatic NUMA balancing can help unknown/dynamic access, or interfere with deliberate placement and latency. Treat enablement as an experimental configuration; record kernel/settings and page/task movement, compare representative cases, and avoid system-wide changes without authorization.

### Huge pages and allocators

Huge pages reduce TLB pressure but coarsen placement/migration: different workers may share one huge page that can live on only one node. Align partitions to page size or decide that bandwidth/TLB benefit dominates. Transparent huge-page decisions can vary; record actual page sizes.

General allocators use arenas, caches, background threads, and metadata whose placement may follow first user or arena creator. Thread-local allocation is not proof that every page is local. Large explicit regions with range policy are easier to reason about. Free/reuse can hand a worker pages initialized elsewhere.

Track allocator statistics, region/page sizes, high-water, per-node capacity/fallback, and allocation latency. Module 095 later addresses concurrent allocator correctness/performance in depth.

### GPUs, NICs, and heterogeneous memory

Map CPU threads/ranks to intended GPUs and nearby NICs using discovered topology. Place host staging/pinned buffers near the CPU/NIC/device path where platform semantics permit. GPU peer, unified/managed memory, HBM, CXL/tiered memory, and migration have distinct rules; do not label all as NUMA nodes and assume CPU policy applies.

First-touch may occur on CPU while the long-lived consumer is a GPU. Explicit device allocation/prefetch/advice or runtime policy may be required. Measure host-device, peer, page-fault/migration, and network timelines. Validate multi-process GPU assignment and avoid accidental sharing/oversubscription.

### Performance experiment

Fix input, algorithm, precision/tolerance, output oracle, resources, code/toolchain, and timing boundaries. Compare unbound/default, verified owner-touch, interleave, and selected explicit mappings, plus automatic balancing only if relevant. Randomize/repeat allocations and placements.

Measure end-to-end and phase max/distributions, local/remote bytes/accesses, per-node bandwidth/controllers, cache/TLB/page faults, CPU migrations, task steals, memory per node, allocation/initialization/migration, NIC/GPU transfers, energy where relevant, and result validity. Track instrumentation overhead.

Perturb access patterns, working sets/page sizes, ranks/threads, placement, imbalance, capacity pressure, task movement, and restore. A change is accepted only if its predicted locality metric and complete valid objective improve without unsafe memory pressure or brittleness.

### Correctness, failure, and portability

Affinity normally should affect performance, not semantic correctness. Test with binding disabled, alternative legal placements, oversubscription, smaller allowed masks, and heterogeneous node shapes. Code that assumes a particular CPU/node ID or task placement is fragile.

Allocation/migration calls can fail or partially succeed. Check returns/status per page/range; define fallback, abort, or reduced placement. Never continue believing a strict map succeeded. On checkpoint/restart, rediscover topology and construct a new placement rather than serializing physical IDs.

Placement can change floating/reduction/task order. Preserve reproducibility/tolerance policy and validate. Failure of a socket/node/device uses the application's existing abort/restart or supported recovery model; NUMA policy is not recovery.

### Security, operations, and high-stakes limits

Topology, CPU masks, page maps, access counters, and device routes can reveal co-tenancy, workload shape, or sensitive regions. Restrict `/proc`, performance counters, and diagnostic artifacts by policy; redact host/process/address labels and retain minimally. Validate user-provided node masks, ranges, sizes, and migration targets; bound memory and migration to prevent denial.

Operations monitor effective binding, remote/local ratios, bandwidth imbalance, page faults/migrations, per-node memory pressure, task movement, device/NIC mapping, throttling, failures, and output checks. Define alerts, fallback configuration, and rollback.

High-stakes NUMA tuning requires domain, numerical, systems/performance, hardware/vendor, security/privacy, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation review. Better locality never proves result validity or deployment safety.

## Definitions and Notation

- R: workers; N: NUMA/memory nodes.
- `Q_rn`: measured/modeled accesses or bytes from worker r to memory node n.
- `c_rn`: measured cost coefficient for that access class.
- `M_n`, `Cap_n`: assigned memory and safe capacity/headroom on node n.
- `A_r`: allowed CPU/place set for worker r.
- `pi(r)`: CPU/place mapping; `mu(page)`: page-node mapping.
- `g`: placement/ownership generation.
- `C=sum Q_rn*c_rn`: simplified placement objective under declared assumptions.
- **owner touch**: the intended long-lived owner triggers page allocation/initialization.
- **locality ratio**: explicitly defined local traffic/access fraction; counter semantics required.
- Obs: topology, constraints, mapping, policies, residency, performance, result, and limitations.

NUMA “local” is relative to a worker/device and topology, not an intrinsic page property.

## Mechanisms, Invariants, or Proof Structure

### Topology/constraint proof

Discover effective topology and binding/memory capabilities inside the allocation; verify cpuset/cgroup/scheduler masks, device visibility, and actual resource counts. Reject hard-coded ID/proximity assumptions.

### Allocation/ownership proof

For every important page range, identify mapping type/page size/policy, allocating and first-touching worker, intended consumers, actual residency, per-node high-water, and fallback. Owner-touch aligns pages without false shared boundaries.

### Scheduling/locality proof

Each task's data home, execution place, access volume, steal/migration policy, and generation are explicit. Cross-node movement has a positive measured/amortized justification and preserves ownership/dependencies/numerics.

### Migration/failure proof

Preflight capacity and support; bound bytes/frequency; check every status; validate placement and result after migration; retain fallback/rollback. Restart rediscovers and remaps rather than restoring stale physical IDs.

### Empirical benefit proof

Under identical valid work, controlled mappings change the predicted remote/local and bandwidth metrics; repeated full critical-path time/resources improve within uncertainty across representative patterns without memory pressure or portability regression.

## Alternatives and Trade-Offs

| Policy/design | Main benefit | Principal limitation |
|---|---|---|
| default/local + owner touch | simple private-data locality | initializer/scheduling must align |
| strict bind | predictable allowed nodes | capacity failure/poor fallback |
| preferred | locality with fallback | placement may drift under pressure |
| interleave | aggregate bandwidth/shared stream | remote latency/private-data loss |
| replicate read-only data | local reads | memory/update consistency |
| static scheduling | stable data affinity | irregular imbalance |
| hierarchical stealing | balance with local preference | runtime/metadata complexity |
| page migration | follows changed ownership | copy/disruption/oscillation |
| automatic balancing | adapts without full model | nondeterminism/interference |
| huge pages | fewer TLB misses | coarse placement/migration |

## Failure Modes and Misconceptions

- **“Thread pinning pins memory.”** CPU and page placement are separate.
- **“malloc allocates physical pages locally.”** demand allocation/touch semantics matter.
- **“First touch always applies.”** mapping/policy/page type/runtime can differ.
- **“Node 0 is closest to CPU 0.”** discover topology.
- **“Interleave is always balanced.”** it may make private accesses remote.
- **“Bind cannot fail.”** masks/capacity/support and partial outcomes matter.
- **“Requested affinity is actual affinity.”** query and verify.
- **“Remote counters prove cause.”** scope/attribution and controlled changes are needed.
- **“Average locality predicts completion.”** critical worker/controller can dominate.
- **“Moving pages is free.”** copying and disruption require amortization.
- **“Automatic balancing always helps.”** deliberate placement can be undone.
- **“Work stealing only changes compute balance.”** it changes data locality.
- **“Huge pages improve every workload.”** placement granularity and capacity change.
- **“NUMA ends at CPU memory.”** NIC/GPU/tier locality also matters.
- **“One mapping is portable.”** allocations/topologies and allowed masks differ.
- **“Checkpoint physical node IDs.”** rediscover/remap on restore.
- **“Lower remote traffic guarantees speedup.”** full valid critical time decides.
- **“Locality proves correctness.”** semantic and domain validation are independent.

## Worked Examples

### Example 1

**Serial initialization.** One thread writes an array later split across sockets; pages cluster near it. Parallel owner touch restores distribution. **Conclusion:** initialize according to consumption.

### Example 2

**Shared table.** Every socket streams the same large read-only table. Replication fits memory and beats remote access; interleave is second best. **Conclusion:** access pattern and capacity choose policy.

### Example 3

**Capacity failure.** Strict bind targets a nearly full node. Preflight rejects rather than silently spilling/terminating mid-run. **Conclusion:** locality is constrained by headroom.

### Example 4

**Steal tradeoff.** A remote task costs 4 ms locally but waits 20 ms for its home worker. Cross-node steal wins despite remote data. **Conclusion:** compare critical-path savings.

### Example 5

**Huge-page collision.** Two owners share one huge page; it cannot be local to both. Realign regions or accept/measure tradeoff. **Conclusion:** page granularity constrains mapping.

### Example 6

**Migration thrash.** Adaptive tasks alternate sockets and pages follow every epoch. Hysteresis and stable ownership stop oscillation. **Conclusion:** move only for a stable horizon.

### Example 7

**Nested runtime.** MPI ranks, OpenMP, and BLAS each spawn threads, oversubscribing cores. Coordinated pools/binding restore locality. **Conclusion:** compose all runtimes.

### Example 8

**GPU/NIC path.** Host staging is allocated on a socket remote from the GPU's NIC. Correct rank/memory/device affinity lowers transfer time. **Conclusion:** locality crosses devices.

### Example 9

**Misleading aggregate.** Total remote reads fall, but the critical socket's controller saturates and job time rises. **Conclusion:** retain per-node critical evidence.

### Example 10

**Neonatal physiological simulation.** Placement changes must preserve patient/model/anatomy/sensor/time/unit/calibration/solver/partition/precision epochs, conservation/convergence/uncertainty, deadline/missing-sensor/failure behavior, device assignment, privacy/security, checkpoint/audit, conservative fallback, and publication gates. Named neonatology/critical-care, physiology, numerical/modeling, NUMA/HPC/hardware, safety/human-factors, privacy/security, operations, quality/regulatory, ethics, accessibility, and independent validation reviewers must approve evidence; none is claimed here. **Conclusion:** local memory access does not validate clinical simulation.

## Cross-Program Connections

- **Architecture:** caches, controllers, interconnects, chiplets, devices, and TLBs define nonuniformity.
- **Operating systems:** demand paging, policies, cpusets, schedulers, migration, and balancing implement placement.
- **Runtimes:** task pools, stealing, nested parallelism, and allocators can preserve or destroy affinity.
- **Distributed systems:** ownership, partition generations, migration economics, and topology recur across nodes.
- **Compilers/numerics:** layout, vectorization, reductions, and precision interact with locality.
- **Performance engineering:** topology discovery, page/counter attribution, traces, and controlled mappings supply evidence.
- **Storage/networks/GPUs:** I/O and accelerator paths have device locality beyond CPU pages.
- **Security/privacy:** page/topology/counter telemetry can reveal sensitive structure.
- **Operations:** capacity pressure, binding drift, thermals, failures, and rollback sustain placement.
- **Safety:** faster memory access remains subordinate to valid outcomes.

## References

1. Linux Kernel Project, *NUMA Memory Policy*, current documentation; retrieved 2026-08-29. <https://cdn.kernel.org/doc/html/latest/admin-guide/mm/numa_memory_policy.html>
2. Linux man-pages Project, *numa(7)*, release 6.18. <https://man7.org/linux/man-pages/man7/numa.7.html>
3. Linux man-pages Project, *mbind(2)*, release 6.18. <https://man7.org/linux/man-pages/man2/mbind.2.html>
4. Linux man-pages Project, *set_mempolicy(2)*, current documentation. <https://man7.org/linux/man-pages/man2/set_mempolicy.2.html>
5. Linux man-pages Project, *move_pages(2)*, release 6.18. <https://man7.org/linux/man-pages/man2/move_pages.2.html>
6. Linux man-pages Project, *cpuset(7)*, release 6.18. <https://man7.org/linux/man-pages/man7/cpuset.7.html>
7. hwloc Project, *CPU Binding API*, hwloc 2.14 documentation. <https://hwloc.readthedocs.io/en/hwloc-2.14.0/doxygen/html/group__hwlocality__cpubinding.html>
8. hwloc Project, *Memory Binding API*, hwloc 2.14 documentation. <https://hwloc.readthedocs.io/en/hwloc-2.14.0/doxygen/html/group__hwlocality__membinding.html>
9. OpenMP Architecture Review Board, *OpenMP API Specification 6.0*, 2024. <https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-6-0.pdf>
10. numactl Project, *numactl/libnuma Source and Documentation*, current repository; retrieved 2026-08-29. <https://github.com/numactl/numactl>

## Exercises

### Exercise 1

For eight equal blocks consumed by workers on nodes `[0,0,0,0,1,1,1,1]`, compute remote blocks/local fraction after serial node-0 touch, perfect owner touch, and two-page round-robin interleave `[0,1,0,1,0,1,0,1]`. State model limits.

### Exercise 2

Design topology discovery and verification for two sockets, four NUMA nodes, two GPUs, and two NICs under a scheduler cpuset. Include actual versus requested mappings and artifacts.

### Exercise 3

Choose policies for private partitions, a large shared read-only stream, a small shared table, and a long-lived adaptively reowned region. Include capacity/fallback and migration economics.

### Exercise 4

Design an experiment distinguishing bad first touch, work imbalance, NUMA latency/bandwidth, task stealing, allocator reuse, and automatic balancing. Specify controls and acceptance.

### Exercise 5

Transfer NUMA-aware placement to a multi-socket clinical genomics pipeline with local accelerators. Specify data/numeric, affinity/capacity, privacy/security, deadline/failure, validation, publication, and named human reviewer invariants without claiming review.

## Answers to the Exercises

### Answer 1

Serial pages all node 0: first four local, last four remote, so 4 remote and local fraction .5. Owner touch matches every worker: 0 remote and local fraction 1. Interleave page nodes versus workers mismatches positions 2,4,5,7 (one-based), so 4 remote and .5 local. This block model ignores page sharing/granularity, multiple accesses/weights, latency/bandwidth contention, cpusets, fallback, migration, caches, and performance.

### Answer 2

Inside the job, capture allowed CPU/memory masks, scheduler allocation, hwloc topology/distances/caches/cores/SMT and OS binding support, PCI/device tree linking GPUs/NICs, and per-node capacity. Define rank/thread places within allowed masks and one GPU/NIC assignment per intended rank; coordinate nested runtimes. Query effective CPU binding and current CPU for each worker, runtime affinity display, visible device IDs, and actual GPU/NIC selection. After parallel owner initialization, query policies and sample/aggregate page residency plus per-node memory. Save topology XML/text, masks, hostname/rank/thread/core/NUMA/GPU/NIC table, policies/page sizes/residency, tool/kernel/runtime versions, and failures—redacted as required.

### Answer 3

Private partitions use local/preferred or bound range policy plus page-aligned owner touch; strict bind only after capacity preflight with explicit failure. Large uniformly shared read-only streaming data can interleave across consumer nodes or replicate if capacity and update semantics allow; measure bandwidth/latency. A small shared table may replicate per node or rely on cache after measurement. Adaptive ownership uses generation-tagged task/data mapping; migrate only when predicted stable remote savings exceed copy/disruption with confidence, hysteresis/cooldown and byte caps, otherwise move computation or tolerate remote access. All policies define cpuset-aware node sets, memory high-water/fallback, actual-placement validation, numeric/result checks, and rollback.

### Answer 4

Fix input/work/result, resources and timing; capture topology/binding/policies/page sizes. Compare serial versus parallel owner touch without changing scheduling and inspect residency/remote traffic. Rotate equal partitions across nodes and compare per-worker useful work/max/mean to isolate imbalance. Pin compute and place pages local versus deliberately remote to calibrate latency/bandwidth, within safe bounds. Compare static/hierarchical stealing and record steals/task homes/remote access. Force fresh large allocations versus allocator reuse and map arena/page origins. Run controlled automatic-balancing off/on only when authorized and record page/task migrations. Repeat allocations/placements, retain phase maxima, controller bandwidth, counters, faults, capacity, initialization/migration/full time and validity. Accept a fix only when predicted locality cause and complete valid objective improve with uncertainty without unsafe memory pressure.

### Answer 5

Bind deidentified specimen/run/reference/database/toolchain/consent epochs and preserve read/variant/lineage provenance, schema, quality/coverage, precision/randomness and independent truth checks. Discover allowed CPUs/nodes/accelerator/NIC topology; assign pipeline shards and owner-touch private buffers near consumers, size per-node/device memory with headroom, coordinate runtimes, and place authenticated staging near device/I/O paths. Use bounded hierarchical scheduling and generation-tagged migration; fail closed on allocation/placement/device/site errors, deadline, stale references, partial aggregation, or invalid output; checkpoint idempotently and remap after restore. Enforce least privilege, purpose/consent/locality, encryption/authentication, pseudonymous IDs, redacted bounded page/counter traces, retention/audit. Validate independent datasets, placements/page sizes/pressures/failures/restores, result/numeric reproducibility, privacy/security and clinical workflow. Named clinical genetics/genomics, infectious-disease/clinical microbiology as applicable, bioinformatics/biostatistics, NUMA/HPC/accelerator, data-governance/privacy/security, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers are required. No external review, clinical validity, privacy guarantee, approval, or deployment authorization is claimed.
