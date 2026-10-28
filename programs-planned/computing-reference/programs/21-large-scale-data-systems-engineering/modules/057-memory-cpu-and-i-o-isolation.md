---
module_id: LSDS-057
program: Large-Scale Data Systems Engineering
level: 2
module_number: 57
title: Memory, CPU, and I/O Isolation
status: complete
last_verified: 2026-09-04
---

# Memory, CPU, and I/O Isolation

## One-Page Review

### Governing question

How should a shared data cluster reserve, account, prioritize, cap, and observe CPU, memory, and storage I/O so one workload can exploit spare capacity without destabilizing its node or violating another workload's service objective?

### Essential definitions

- **resource isolation** constrains interference and attributes resource consumption across workload boundaries.
- A **request/reservation** is capacity used for admission and protected service; a **limit/cap** bounds runtime consumption.
- A **weight/share** controls proportional service during contention; it is not an absolute reservation or ceiling.
- **CPU bandwidth** is runnable processor time over a period; **CPU affinity/cpuset** restricts which logical CPUs may execute a workload.
- **memory protection** biases reclaim away from protected memory; a **hard memory limit** bounds charged usage and can lead to OOM termination.
- **working set** is memory needed for useful execution under a declared observation window; it is not identical to RSS or total charged memory.
- **I/O weight** allocates device service under contention; an **I/O maximum** caps bytes or operations per interval for a device path.
- **writeback attribution** charges buffered writes to the workload that dirtied pages when the kernel/filesystem supports it.
- **pressure stall information (PSI)** measures time some or all tasks are stalled for CPU, memory, or I/O availability.
- A **noisy neighbor** causes another colocated workload's latency or throughput to degrade through a shared resource.

### Central model, mechanism, or theorem

For resource $k\in\{cpu,memory,io\}$ on node $n$, define allocatable capacity $A_{n,k}=C_{n,k}-S_{n,k}$ from physical/effective capacity $C$ minus system reserve $S$. Admit workload $j$ only if the sum of trustworthy requests fits the relevant vector/topology. At runtime, hierarchical weights distribute contended service, protection preserves critical working sets, and hard limits bound unsafe bursts. Isolation succeeds only if the enforcement point covers the actual bottleneck and interference stays within the victim's service objective:

$$\Delta O_v(j)=O_v(\text{colocated with }j)-O_v(\text{baseline})\leq \epsilon_v.$$

Requests, weights, limits, affinity, topology, and pressure feedback solve different problems. No single knob proves isolation across CPU execution, memory reclaim/cache, device queues, filesystem writeback, network storage, last-level cache, or memory bandwidth.

### Critical invariants

- Admission uses allocatable—not physical—capacity and reserves resources for the OS, agents, storage, and recovery.
- Resource identity follows every process/thread and descendant; escape into an uncontrolled group is rejected.
- CPU request/weight, CPU cap, and cpuset/exclusive placement remain semantically distinct.
- Memory accounting includes relevant anonymous memory, page cache, kernel objects, sockets, swap, and shared-page policy.
- Hard memory exhaustion is contained to the intended boundary before node-wide OOM whenever the platform permits.
- I/O controls bind the real block device or service path and account buffered/direct I/O consistently enough for policy.
- Hierarchical child guarantees/caps never exceed effective parent capacity; empty or throttled parents cannot be bypassed.
- NUMA, SMT, cache, memory-bandwidth, device, and topology placement match the isolation claim.
- Metrics expose usage, throttling, reclaim, OOM, stalls, queueing, and application outcome together.
- Policy is validated under mixed workload phases, overload, failure, resize, and controller/runtime restart.

### Common failures

Common failures include treating a CPU request as an exclusive core; using a CPU limit that adds periodic latency; setting memory limit equal to a steady-state average; omitting page cache or off-heap memory; disabling OOM handling without a containment plan; trusting RSS as the working set; applying I/O weights to the wrong device; assuming direct- and buffered-I/O controls behave identically; ignoring network-attached storage; placing CPU and memory on different NUMA nodes; giving every child a guarantee that the parent cannot honor; starving node agents; measuring utilization without throttling/PSI; and declaring isolation from synthetic microbenchmarks while production stage tails regress.

### Compact example

A node has (32 CPU, 128 GiB memory, 1,000 MiB/s local I/O) and reserves (4,16,100) for the system, leaving (28,112,900). Existing requests are (20,80,500); a candidate requests (6,24,250). The post-admission vector is (26,104,750), so it fits with (2,8,150) headroom. This proves request-level admission only—not that bursts, memory bandwidth, cache contention, writeback, or remote storage meet their objectives.

### Connections

[LSDS-032](032-map-side-buffering-and-spill.md) and [LSDS-033](033-sort-based-shuffle.md) create memory/I/O coupling, [LSDS-047](047-checkpoint-barriers.md) creates checkpoint bursts, [LSDS-049](049-backpressure-across-operators.md) exposes downstream stalls, [LSDS-051](051-cluster-resource-models.md) defines vectors, [LSDS-052](052-static-and-dynamic-allocation.md) assigns them, and [LSDS-056](056-preemption.md) reclaims them.

## Governing Question

Cluster schedulers decide where work may run, but node kernels and runtimes decide how colocated work actually shares processors, memory, and storage paths. Admission can be correct while runtime behavior is disastrous: a batch scan consumes page cache and evicts a service's working set; a CPU-capped executor pauses at the end of each quota period; checkpoint writeback fills a device queue; or memory reclaim stalls every task before an OOM kill.

The resources differ fundamentally. CPU time is renewable: throttled work can run later. Memory is occupied state: reclaim may require scanning, writeback, swap, compaction, or termination. I/O is a queued service over a path that may include filesystem cache, local devices, network, and remote storage quotas. One abstraction cannot erase those differences.

The governing question is how to translate workload intent into reservations, proportional weights, ceilings, affinity, and topology; enforce those settings through a complete hierarchy; reserve the host; observe both kernel pressure and dataflow outcomes; and adapt without oscillation or unsafe overcommit.

## Why This Matters

Large-scale data workloads are phase-changing. A task may scan and decompress, build a hash table, spill, shuffle, merge, checkpoint, and publish. CPU, memory, and I/O dominance changes across those phases. Static average utilization hides short bursts that determine tail latency and trigger node instability.

Sharing raises utilization and reduces cost, but shared-resource interference is nonlinear. Memory pressure increases reclaim and page faults, which produce I/O, which blocks CPU and slows progress, which retains memory longer. A storage queue filled by checkpoint writes can delay shuffle reads and create backpressure. Isolation must reason about these causal loops rather than tune each metric independently.

Correct resource declarations also underpin scheduling fairness. Requests that are far below actual use permit over-admission and push risk onto neighbors. Inflated requests waste capacity and distort shares. Limits that are too tight make a job appear intrinsically slow when it is actually throttled. Measurement, defaults, validation, and accountable ownership are therefore part of the isolation system.

Node survival is a hard boundary. Kubelets, runtimes, loggers, storage daemons, monitoring agents, SSH/emergency tools, and the kernel need CPU, memory, and I/O during overload. If workloads can consume the final bytes or saturate the device used for recovery, the controller that should evict them may itself fail.

Isolation is also a security and governance concern. A tenant may intentionally fork outside its group, create uncharged processes, manipulate priorities, or exploit shared caches and timing. Mechanisms must follow process ancestry, constrain delegated administration, authenticate configuration, and audit policy changes. Performance isolation reduces some denial-of-service risk but is not a complete confidentiality boundary.

## Prerequisites and Retrieval

Review buffer/spill and sorting behavior in [LSDS-032](032-map-side-buffering-and-spill.md) and [LSDS-033](033-sort-based-shuffle.md), streaming state/checkpoints in [LSDS-043](043-stateful-operators.md) through [LSDS-048](048-state-snapshots-and-recovery.md), backpressure in [LSDS-049](049-backpressure-across-operators.md), resource vectors in [LSDS-051](051-cluster-resource-models.md), allocation/fairness in [LSDS-052](052-static-and-dynamic-allocation.md) and [LSDS-053](053-fair-and-capacity-scheduling.md), and preemption in [LSDS-056](056-preemption.md).

You should understand processes/threads, scheduler runnable time, cgroup hierarchies, virtual memory, anonymous and file-backed pages, reclaim, OOM, swap, NUMA, SMT, filesystem buffering/writeback, block devices, queues, throughput/latency, percentiles, resource requests/limits, and dataflow stages.

## Learning Objectives

After this module, you should be able to:

1. distinguish reservation, request, weight, cap, affinity, protection, and eviction semantics;
2. derive allocatable CPU, memory, and I/O after explicit system/recovery reserves;
3. choose shared CPU weights, bandwidth caps, or exclusive CPU placement for a workload objective;
4. account and control anonymous, file-cache, kernel, socket, swap, and off-heap memory;
5. apply I/O weights/maximums to real device and writeback paths without false guarantees;
6. coordinate NUMA, SMT, cache, memory bandwidth, storage, and device topology;
7. connect throttling, reclaim, OOM, and I/O queues to task/stage/job behavior;
8. maintain hierarchical, escape-resistant enforcement across lifecycle and resize;
9. design safe feedback, overload, eviction, and rollback policies; and
10. validate isolation with pressure, interference, outcomes, fairness, and cost evidence.

## Core Exposition

### Start with service objectives and threat model

Name what isolation protects: throughput, p99 latency, deadline, checkpoint duration, node availability, minimum progress, or tenant fairness. Identify aggressors and shared paths. A CPU-bound batch task threatens runnable time and caches; a sort threatens memory and storage; a checkpoint threatens writeback and network/object storage.

State whether the threat model includes accidental bursts, sustained overload, malicious escape, measurement error, controller failure, and hardware faults. A best-effort performance policy and a hostile multi-tenant boundary need different controls.

### Reserve the node before admitting workloads

Inventory physical capacity, then subtract operating-system, orchestration, storage, logging, monitoring, security, and recovery reserves. Reserve by resource and topology: CPU on specific cores, memory per NUMA node, and I/O headroom on devices required for logs/checkpoints/recovery.

Advertise allocatable capacity consistently to schedulers and runtime controllers. A scheduler that admits against 128 GiB while the node enforces only 112 GiB for workloads creates unavoidable pressure. Test reserve availability during peak logging, eviction, checkpoint restore, and node drain.

### Separate admission requests from runtime limits

Requests express expected protected consumption and drive placement/fairness. Limits constrain runtime use. A workload can request 2 CPU and be allowed to burst to 6; under contention its weight should protect the request-equivalent share while the cap prevents it from monopolizing all cycles.

Memory cannot be treated like CPU bursting. Usage above a request occupies pages until reclaimed or freed. A memory hard limit can terminate work; a request may influence admission and protection but cannot manufacture RAM. I/O request semantics require a schedulable device/service capacity model, which many platforms do not provide uniformly.

### Build a complete hierarchy

Place every workload process and descendant under one authoritative resource group. Enable controllers at the correct ancestors, set parent budgets, and ensure child requests/caps compose within them. Sidecars, subprocesses, native libraries, helpers, and orphaned descendants must remain charged.

Hierarchy lets organization, tenant, job, and task policies compose. It also creates traps: a child's high weight cannot obtain CPU when its parent is heavily capped; many child protections can overcommit a parent's memory; and a permissive delegated subtree can weaken policy. Reconcile desired and actual controller state after runtime restart.

### Understand CPU weights

CPU weight is proportional competition among runnable peers, not reserved wall-clock time. If only one group is runnable, it may consume spare CPU. Under contention, effective shares depend on weights at each hierarchy level and the scheduler's accounting. A sleeping workload does not bank unused cycles unless a separate mechanism says so.

Use weights for work-conserving sharing and soft priority. Validate with runnable mixed workloads, not idle neighbors. Observe actual CPU service, run-queue delay, PSI, context switches, migrations, and application throughput/latency.

### Understand CPU bandwidth caps

A CPU quota/maximum limits processor time per period. It bounds consumption even when capacity is idle, useful for containment and licensing/cost rules. Once the budget is consumed, runnable threads wait until replenishment, which can create periodic latency and underutilization.

Choose periods/caps with request concurrency and latency in mind. A multithreaded executor can burn a group budget quickly. Track throttled periods and throttled duration; high CPU usage alone cannot reveal quota-induced stalls. Avoid default CPU caps for latency-sensitive workloads unless the isolation benefit justifies the tail cost.

### Use affinity and exclusive CPUs carefully

CPU affinity restricts execution to selected logical CPUs. Exclusive allocation can reduce run-queue interference and migrations, but shared last-level cache, memory bandwidth, SMT siblings, interrupts, and NUMA remain. Reserve housekeeping CPUs so kernel and node agents remain responsive.

Allocate full physical cores when sibling interference matters, align with devices and memory, and document whether logical CPUs, cores, sockets, or cache domains are promised. Pinning fragmented CPUs across NUMA nodes may be worse than weighted sharing.

### Account memory comprehensively

Track anonymous heap, native/off-heap allocations, mapped files, page cache, kernel structures, socket buffers, tmpfs/shared memory, and swap according to the actual controller. JVM or runtime heap limits do not cover every charged byte. Shared pages need a declared attribution model.

Use multiple views: current charged usage, anonymous/file split, working-set approximation, active/inactive pages, faults, reclaim, swap, OOM events, and application allocation/GC. RSS alone omits important consumers and can double-count or misrepresent shared/file-backed memory.

### Apply memory protection and thresholds

Protection/minimum/low settings bias reclaim so critical working sets survive contention. A high threshold can apply throttling/reclaim pressure before the hard maximum. A hard maximum is a containment boundary: allocations may stall, reclaim intensifies, and an OOM policy may terminate one or more processes in the group.

Do not set every workload's protection to its peak; total effective protection must fit physical memory after reserves. Calibrate from phase-aware working sets and failure cost. Treat memory pressure as state degradation before OOM, not a binary healthy/dead signal.

### Design OOM containment

Prefer workload-scoped OOM handling over node-wide victim selection when available. Decide whether one process or the whole task group must die for consistency; a half-dead distributed executor can retain leases or serve corrupt partial state. Propagate termination to the scheduler and retry/fence using logical attempt semantics.

Never disable OOM termination without a bounded alternative: unkillable allocation stalls can freeze the node. Reserve recovery capacity, test allocator and kernel behavior, record OOM reason/counters, and distinguish container limit OOM from node exhaustion.

### Treat page cache as both value and contention

File-backed cache can accelerate repeated scans and shuffle, but it occupies reclaimable memory and creates writeback. A workload that reads once may evict a service's hot pages. A writer can dirty pages faster than storage drains them, then encounter global throttling.

Account page cache to the originating workload where supported, choose buffered/direct I/O based on access pattern and enforcement semantics, and monitor dirty/writeback/reclaim. Do not subtract all cache from usage as “free”; reclaim latency is part of performance.

### Understand I/O enforcement points

Identify the actual block device behind a path, including logical volumes, device mapper, RAID, local SSD, persistent volume, or network filesystem. Device weights divide service only when workloads contend at the controlled scheduler. Maximums cap bytes/operations but may not reflect latency or downstream service quotas.

Buffered writes may be delayed and issued by kernel writeback threads; correct attribution depends on kernel/filesystem support. Direct I/O follows another path. Test the exact mount, filesystem, device stack, access mode, block size, concurrency, read/write mix, and queue discipline used in production.

### Include remote storage and network

Block-I/O controls do not govern object-store requests, network filesystem servers, cross-zone links, or remote database quotas by themselves. Apply concurrency, request-rate, byte-rate, and priority controls at the client/service/network layer, and reserve network/recovery headroom.

An application may be locally I/O-idle while stalled on remote storage. Correlate device and network/service telemetry with task progress. Do not claim “I/O isolation” when only one local layer is controlled.

### Align NUMA and topology

On NUMA machines, CPU placement and memory allocation must agree. Remote memory adds latency and consumes interconnect bandwidth. Large memory requests may span nodes; devices attach to specific sockets; last-level cache and memory controllers form further contention domains.

Coordinate CPU, memory, and device hint providers before admission. Reject placements that cannot meet a hard topology contract. Revalidate after CPU hotplug, node reconfiguration, or manager-state loss, and drain safely before changing policies that invalidate existing assignments.

### Recognize uncore interference

Even perfect CPU-time isolation cannot isolate last-level cache, memory bandwidth, prefetchers, translation structures, power/frequency, or thermal limits. SMT siblings share execution resources. A memory-intensive batch task can slow a latency service without consuming its CPU quota.

Use topology-aware placement, cache/memory-bandwidth controls where available, workload compatibility policies, and feedback from victim outcomes. If hardware lacks trustworthy enforcement, reserve headroom or avoid the co-location instead of overstating guarantees.

### Map controls to dataflow phases

Scan/decode is I/O and CPU heavy; hash build consumes memory; sort spills couple memory thresholds to I/O; shuffle adds network and disk; aggregation changes cardinality; checkpoint dirties state and creates bursts. Record phase in telemetry so the same task is not assigned one static diagnosis.

Coordinate operator buffer sizes, parallelism, spill thresholds, fetch concurrency, and checkpoint cadence with node controls. A tighter memory limit can increase spill, causing I/O contention that slows unrelated jobs. A CPU cap can delay consumers and amplify upstream buffers.

### Manage elastic resize safely

Changing CPU weights/caps is usually reversible but can abruptly change latency. Raising memory limits may be safe if capacity exists; lowering them below current usage can trigger reclaim or OOM. Moving cpusets/NUMA memory can require task restart. I/O policy changes may affect queued operations slowly.

Validate requested versus effective settings, serialize incompatible changes, and use generation-scoped reconciliation. Rate-limit fleet changes, canary by workload class, and retain rollback values. Autoscaling must not count throttled capacity as physical scarcity without diagnosing policy.

### Use pressure as a control signal

CPU utilization says busy, not whether work waits. Memory bytes say occupancy, not reclaim pain. Device throughput says volume, not queue delay. PSI “some” and “full,” run-queue delay, throttling, reclaim, faults, OOM, device latency/depth, and application progress expose contention.

Pressure feedback must use sustained windows, hysteresis, and cause attribution. Reacting to a single spike can move or throttle work unnecessarily; waiting for OOM is too late. Control actions should name expected effect and revert when it fails.

### Protect fairness and prevent gaming

Charge actual usage and scarce shared services while using declared requests for admission/guarantees. Detect systematic under-requesting, but allow legitimate phase bursts within policy. Apply namespace/tenant quotas and defaults so omitted constraints do not become unlimited access.

Do not let privileged workloads modify their groups, raise weights, disable OOM containment, access raw devices, or fork into host groups. Authenticate policy changes and preserve audit evidence. Cross-tenant performance tests must avoid exposing sensitive workload traces.

### Validate isolation empirically

For each protected victim, establish a solo baseline across representative phases and load. Add one aggressor dimension at a time, then realistic mixtures: CPU saturation, memory footprint/bandwidth/reclaim, cached scans, dirty writeback, random/sequential device access, remote storage, checkpoint bursts, and compound pressure.

Measure victim objective delta, aggressor progress, node survival, fairness, utilization, throttling, PSI, reclaim/OOM, I/O latency/queue, and cost. Inject controller removal, runtime restart, process escape attempts, node-agent pressure, storage slowdown, hotplug/state mismatch, and telemetry loss. Canary and rollback by policy generation.

## Definitions and Notation

Let node $n$ expose capacity vector $C_n=(C_{cpu},C_{mem},C_{io})$ and system/recovery reserve $S_n$, giving allocatable $A_n=C_n-S_n$. Workload $j$ declares request $r_j$, runtime cap $m_j$, weight $w_j$, placement/affinity $P_j$, and observed usage $u_j(t)$. Admission requires $\sum r_j+r_{new}\preceq A_n$ plus topology and policy feasibility.

During CPU contention among siblings, weights influence proportional processor service; a cap independently restricts maximum bandwidth. For memory, protection $l_j$ and high/hard thresholds $h_j,m_j$ express reclaim preference, pressure onset, and containment. These symbols are conceptual because platform interfaces and exact semantics differ.

For storage device/path $d$, let $b_{j,d}$ and $q_{j,d}$ denote byte/operation caps, $w_{j,d}$ weight, and $L_d(t)$ observed latency/queue pressure. A policy is effective only when actual I/O from $j$ is attributable at $d$. Remote-service limits require separate path variables.

Let protected victim objective $O_v$ be latency, inverse throughput, or another “lower is better” measure. Interference is $\Delta O_v(j)=O_v(v+j)-O_v(v)$ under matched conditions. Acceptable isolation requires $\Delta O_v(j)\leq\epsilon_v$ with confidence while aggressor and system outcomes remain viable.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence:

1. Define workload objectives, adversaries, phases, enforcement boundary, and relevant hardware/service paths.
2. Inventory capacity by topology and subtract tested system, control-plane, storage, and recovery reserves.
3. Require trustworthy request vectors for admission; define burst/limit and tenant quota separately.
4. Attach every process/descendant to a generation-scoped hierarchy with enabled controllers and composable parent budgets.
5. Configure CPU weights/caps/affinity, memory protection/high/max/OOM, and device/path I/O weights/caps according to semantics.
6. Align CPUs, memory, cache domains, devices, and NUMA while acknowledging unregulated shared resources.
7. Connect runtime events to task attempts, spill/shuffle/checkpoint/state, backpressure, and scheduler recovery.
8. Observe effective configuration, usage, throttling, PSI, reclaim/OOM, I/O queue/latency, and application objectives.
9. Apply bounded, hysteretic resize/eviction/remediation with authorization, audit, canary, and rollback.
10. Reproduce isolation across solo baselines, adversarial co-location, mixed phases, overload, failure, restart, and escape attempts.

If admission uses requests and $\sum r_j\preceq A_n$, requested capacity fits by construction. This does not prove instantaneous usage fits, because workloads may burst above requests, resource dimensions may be correlated, and unmodeled resources/topology may bind. Runtime caps, protection, overload handling, and validation close different gaps.

A hierarchical CPU weight can only divide the service made available to its parent. Therefore increasing a child's weight cannot overcome a tight ancestor cap. Similarly, memory protection promises cannot all be absolute when their effective sum exceeds physical allocatable memory. Configuration must be checked from workload leaf through root.

An interference experiment supports the declared bound only for its tested workload versions, phases, topology, concurrency, devices, controller configuration, and observation distribution. Extrapolating a microbenchmark to every dataflow is invalid; continuous canaries and production telemetry detect drift.

## Alternatives and Trade-Offs

- **Dedicated nodes:** strong coarse isolation and simple attribution; lower utilization, slower elasticity, and larger capacity fragments.
- **Shared nodes with requests/weights:** work-conserving utilization; tail interference remains on uncapped/unmodeled resources.
- **Hard CPU caps:** bound consumption predictably; periodic throttling can inflate latency while CPUs sit idle.
- **CPU weights only:** allow efficient bursting; do not bound an aggressor when peers sleep or protect exclusive-core needs.
- **Exclusive full cores:** reduce run-queue/SMT interference; consume fragmented capacity and still share caches/memory bandwidth.
- **Memory hard limits:** contain footprint/OOM scope; poor sizing causes reclaim stalls or kills rather than graceful slowdown.
- **Memory protection:** preserves important working sets under pressure; overcommitted protection makes promises conflict.
- **Swap enabled:** can avoid immediate OOM and retain cold pages; unpredictable latency and I/O amplification may harm data jobs.
- **Swap disabled:** clearer resident-memory boundary; abrupt OOM under transient pressure.
- **Buffered I/O:** benefits from cache/coalescing; delayed writeback complicates latency and attribution.
- **Direct I/O:** clearer application/device path for suitable engines; alignment, portability, and cache-loss costs increase.
- **I/O weights:** share a contended controlled device; cannot guarantee latency or govern unrelated remote paths.
- **I/O maximums:** bound an aggressor; may waste idle bandwidth and need per-device calibration.
- **Static policy:** predictable and auditable; phase changes waste capacity or cause unnecessary throttling.
- **Feedback control:** adapts to phases and outcomes; delays, coupling, noise, and bad attribution can oscillate.
- **Avoid co-location:** safest when hardware controls are incomplete; sacrifices utilization that compatible workloads could provide.

## Failure Modes and Misconceptions

- **“A request is a runtime reservation everywhere.”** It may drive admission/weight while physical service still depends on contention and implementation.
- **“A limit improves performance isolation automatically.”** A cap can introduce throttling tails and leave idle capacity unused.
- **“Four logical CPUs mean four physical cores.”** SMT siblings and topology make the units different.
- **“Pinned CPUs isolate the whole processor.”** cache, memory bandwidth, interrupts, power, and thermal behavior remain shared.
- **“Heap equals memory.”** native/off-heap, page cache, mappings, kernel, socket, tmpfs, and shared pages also matter.
- **“Page cache is free.”** reclaim and writeback have latency and can evict another workload's useful pages.
- **“Memory usage below max is healthy.”** reclaim, faults, PSI, GC, and bandwidth contention can be severe first.
- **“Disabling OOM prevents failures.”** it can turn contained termination into node-wide stalls.
- **“I/O weight governs every storage request.”** it applies only at supported, correctly mapped contention points.
- **“Device throughput proves good I/O service.”** latency and queue depth may be unacceptable at high throughput.
- **“Remote object storage is block I/O.”** client concurrency, network, request quota, and service behavior need separate controls.
- **“Child settings override the parent.”** ancestor caps and weights bound all descendants.
- **“Utilization measures contention.”** throttling, queue delay, PSI, reclaim, and outcome deltas are required.
- **“One stress tool validates isolation.”** real phase mixtures, topology, access patterns, and failures can behave differently.
- **“Resize is harmless.”** memory decreases, cpuset movement, and device remapping can kill or stall work.
- **“Performance isolation is a confidentiality boundary.”** shared-resource timing and other channels require separate security analysis.

## Worked Examples

### Example 1

A node has 64 CPUs but reserves four for the OS, storage daemon, and agents. Advertising 64 to the scheduler permits workload saturation to starve the very processes needed for eviction and recovery. Advertising 60 and pinning housekeeping appropriately preserves the operational boundary; the reserve must be tested under failure logging and restore, not guessed.

### Example 2

Two runnable sibling groups have CPU weights 3:1 and no caps. Under sustained contention they should receive roughly proportional service through that hierarchy, but when the first sleeps the second may use the CPUs. The ratio is not a promise of three cores versus one, and an ancestor capped at two CPUs limits both together.

### Example 3

An executor capped at two CPUs has eight runnable threads. They consume the period's budget early, then all wait for replenishment. Average CPU may match two cores while request latency spikes periodically. Throttled-time and run-queue telemetry distinguish this from slow application code.

### Example 4

A JVM heap is limited to 20 GiB inside a 24-GiB memory group. Native buffers, thread stacks, memory-mapped shuffle, page cache, and kernel/socket charges consume another 6 GiB. The group can OOM despite heap compliance. Size and observe the complete charged footprint, or intentionally separate controlled caches.

### Example 5

A scan reads 200 GiB once and fills file cache, evicting a colocated service's hot index. Both stay below hard limits because cache is reclaimable, yet the service page-faults and violates p99. Memory protection, cache-aware placement, read hints/direct I/O where appropriate, or non-colocation addresses an interference that RSS-only dashboards miss.

### Example 6

A checkpoint writer is given low I/O weight on the underlying NVMe. Buffered dirty pages accumulate, and later writeback competes with shuffle reads. Verify that writeback is attributed to the writer's group on the actual filesystem/device stack; otherwise the configured weight gives false confidence. Also limit checkpoint concurrency and dirty-memory pressure.

### Example 7

An object-store scan shows almost no local block-device traffic but saturates the node NIC and remote request quota. Local I/O maximums cannot isolate it. Client request/byte concurrency, network policy, storage-service quotas, and cross-node placement must protect the shared path.

### Example 8

A four-core task is pinned to CPUs on NUMA node 0 while its 80-GiB allocation lands mostly on NUMA node 1. CPU exclusivity does not prevent remote-memory latency and interconnect contention. Coordinated CPU/memory topology admission either finds aligned resources or rejects the strict request.

### Example 9

Lowering a running stateful operator's memory maximum from 32 to 20 GiB while it uses 28 GiB triggers aggressive reclaim and possible OOM, increasing checkpoint time and upstream backpressure. A safe resize first reduces buffers/parallelism, checkpoints, verifies usage decline, then changes the hard boundary—or restarts on a correctly sized placement.

### Example 10

The fixture performs request-level vector admission after a system reserve. It deliberately makes no runtime-isolation claim.

<!-- bijux-verify: {"id":"isolation-admission-vector","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"allocatable=(28, 112, 900)\npost_request=(26, 104, 750)\nheadroom=(2, 8, 150)\nadmit=True\n","stderr":""}} -->
```python
capacity = (32, 128, 1000)       # CPU, GiB, MiB/s
system_reserve = (4, 16, 100)
existing_requests = (20, 80, 500)
candidate_request = (6, 24, 250)

allocatable = tuple(c - s for c, s in zip(capacity, system_reserve))
post_request = tuple(a + b for a, b in zip(existing_requests, candidate_request))
headroom = tuple(a - p for a, p in zip(allocatable, post_request))
admit = all(value >= 0 for value in headroom)

print(f"allocatable={allocatable}")
print(f"post_request={post_request}")
print(f"headroom={headroom}")
print(f"admit={admit}")
```

Production admission also validates topology, hierarchy, request credibility, workload class, and unmodeled bottlenecks, then relies on runtime enforcement and outcome measurement.

## Cross-Program Connections

- **Operating systems:** process scheduling, virtual memory, reclaim/OOM, cgroups, filesystems, writeback, and block queues supply enforcement.
- **Computer architecture:** SMT, NUMA, caches, memory controllers/bandwidth, interrupts, devices, power, and thermals define residual sharing.
- **Distributed systems:** leases, attempt fencing, controller reconciliation, node failure, and durable configuration connect local enforcement to cluster state.
- **Data structures/algorithms:** buffers, hash tables, external sorting, cache policies, queues, and feedback control determine resource demand.
- **Data engineering:** scans, spill, shuffle, checkpoint, state, compaction, and skew create coupled phase-specific pressure.
- **Platform engineering:** requests/limits, QoS classes, admission, quotas, topology managers, node allocatable, eviction, and telemetry expose policy.
- **Reliability engineering:** host reserves, overload containment, OOM scope, degradation, canaries, rollback, and recovery protect availability.
- **Security and economics:** escape prevention, authorization, audit, denial-of-service boundaries, utilization, cost, and energy govern sharing.

## References

1. Linux Kernel. [Control Group v2.](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html) Current hierarchy, delegation, CPU, memory, I/O, cpuset, pressure, writeback, and controller semantics.
2. Linux Kernel. [Pressure Stall Information.](https://docs.kernel.org/accounting/psi.html) Current CPU, memory, and I/O some/full stall accounting and trigger interface.
3. Kubernetes. [Resource Management for Pods and Containers.](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) Current requests, limits, CPU/memory enforcement, huge pages, local ephemeral storage, and scheduling semantics.
4. Kubernetes. [Control CPU Management Policies on the Node.](https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies/) Current shared/static CPU pools, exclusive assignment, reservations, reconciliation, and topology options.
5. Kubernetes. [Control Memory Management Policies on a Node.](https://kubernetes.io/docs/tasks/administer-cluster/memory-manager/) Current guaranteed memory, NUMA hints, reserved memory, policy state, and admission constraints.
6. Kubernetes. [Control Topology Management Policies on a Node.](https://kubernetes.io/docs/tasks/administer-cluster/topology-manager/) Current CPU, memory, and device hint coordination across NUMA topology.
7. Kubernetes. [Pod Quality of Service Classes.](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/) Current Guaranteed/Burstable/BestEffort classification, eviction ordering, and cgroup-v2 Memory QoS behavior.
8. Kubernetes. [Node-Pressure Eviction.](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/) Current node signals, thresholds, reclaim, victim ranking, grace, and resource-pressure behavior.
9. Docker. [Resource Constraints.](https://docs.docker.com/engine/containers/resource_constraints/) Current runtime CPU, memory, swap, OOM, affinity, and device constraint interface.
10. systemd. [Resource Control.](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html) Current cgroup-v2 unit hierarchy and CPU, memory, I/O, tasks, and device resource-control settings.
11. Lo et al. [Improving Resource Efficiency at Scale with Heracles.](https://research.google/pubs/improving-resource-efficiency-at-scale-with-heracles/) Primary feedback-controlled CPU, memory, and network isolation study for colocated latency-critical and batch workloads.
12. Verma et al. [Large-Scale Cluster Management at Google with Borg.](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) Primary production account of requests, limits, overcommitment, machine sharing, priority, and process-level isolation.
13. Hindman et al. [Mesos: A Platform for Fine-Grained Resource Sharing in the Data Center.](https://www.usenix.org/conference/nsdi11/mesos-platform-fine-grained-resource-sharing-data-center) Primary resource-offer and fine-grained cluster sharing design across heterogeneous frameworks.

## Exercises

### Exercise 1

Explain the different guarantees made by a CPU request/weight, CPU bandwidth cap, and exclusive cpuset. Give one failure mode for each.

### Exercise 2

A node has (48 CPU, 256 GiB, 2,000 MiB/s) and reserves (6,32,300). Existing requests are (34,180,1,100); a candidate requests (6,52,500). Compute allocatable, post-request headroom, and the simplified admission decision.

### Exercise 3

Design memory isolation for a 24-GiB-heap executor whose native buffers, page cache, mappings, sockets, and checkpoint bursts vary. Include admission, protection, high/max behavior, OOM, swap, telemetry, and recovery.

### Exercise 4

An I/O limit appears ineffective for buffered checkpoint writes to a persistent volume backed by network storage. Provide a layer-by-layer diagnostic and corrected control design.

### Exercise 5

Design a production isolation experiment and rollout for colocating latency-sensitive queries with batch sort/shuffle. Include baselines, aggressors, topology, metrics, safety, failure tests, canary, and rollback.

## Answers to the Exercises

### Answer 1

A CPU request commonly drives admission and relative weight/protected share under contention; it may allow bursting and is not an exclusive core. Failure: under-requesting causes over-admission and poor neighbor service. A bandwidth cap is an absolute time-per-period ceiling; it contains use even when idle capacity exists. Failure: multithreaded bursts exhaust budget early and create periodic tail latency. An exclusive cpuset restricts execution to assigned logical CPUs and avoids runnable peers there. Failure: SMT siblings, shared cache/memory bandwidth, interrupts, or remote NUMA memory still interfere, and fragmented pinned capacity may be wasted. Verify effective hierarchy and outcome for all three.

### Answer 2

Allocatable is $(48-6,256-32,2000-300)=(42,224,1700)$. Post-request use is $(34+6,180+52,1100+500)=(40,232,1600)$. Headroom is $(2,-8,100)$, so simplified vector admission rejects because memory exceeds allocatable by 8 GiB. Spare CPU and I/O cannot substitute for memory. A real decision also checks request credibility, NUMA/device topology, hierarchy, remote paths, and workload class.

### Answer 3

Measure phase-aware total charged memory rather than heap alone: anonymous/native, mappings, page cache, kernel/socket, tmpfs/shared pages, and swap. Set the request/protection for a defensible critical working set plus overhead, reserve node/recovery memory, and admit against allocatable NUMA capacity. Put an early high/reclaim threshold below a hard maximum with enough distance for spill/GC/checkpoint response; size max for credible burst rather than average. Bound or disable swap according to latency objectives, never disable OOM without containment, and choose whole-executor OOM if partial death violates task semantics. Observe current/type breakdown, working-set proxy, faults, reclaim, PSI, dirty/writeback, GC/native metrics, high/max/OOM events, spill/checkpoint, and stage tails. On termination, fence the attempt and recover from validated shuffle/checkpoint/input state. Test burst, leaks, cache pressure, storage slowdown, resize, and node-agent reserve.

### Answer 4

Resolve application path through mount, filesystem, volume implementation, device mapper/local device, network client, NIC, server, and object/storage quotas. Determine whether writes are buffered, who owns dirty pages, where writeback is charged, and whether the configured controller/scheduler supports weights or maxima at that layer. Compare application-issued bytes, dirty/writeback, group-attributed I/O, block-device bytes/latency/depth, network flows, and server request metrics. A local block rule may control only cache flush to a virtual device while the bottleneck is client concurrency or remote service. Correct with supported writeback attribution/device controls, per-workload dirty/concurrency limits, client request/byte rate, network/storage QoS, checkpoint staggering, and protected recovery headroom. Validate the exact access mode and mixed neighbors.

### Answer 5

Establish solo query and batch baselines across scan, hash, spill, shuffle, and checkpoint phases on the target hardware. Add controlled CPU runnable load, cache/memory-bandwidth load, memory footprint/reclaim, sequential/random buffered/direct I/O, dirty writeback, network/remote storage, then representative compound mixtures. Vary SMT/NUMA/cache/device placement and concurrency. Record query p50/p99/throughput, batch progress, CPU service/throttling/run queue/PSI, memory types/faults/reclaim/PSI/OOM/GC, device bytes/IOPS/latency/depth/writeback, network/storage latency, node-agent health, fairness, utilization, cost, and energy. Test controller/runtime restart, escape attempts, storage slowdown, telemetry loss, resize, OOM, and recovery. Define hard query/node thresholds and batch minimum progress, shadow the policy, canary compatible workload classes and a small node pool, halt on safety/outcome regression, and restore versioned settings or de-colocate while reconciling assignments.
