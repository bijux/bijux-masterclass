---
module_id: OS-065
program: Operating Systems
level: 2
module_number: 65
title: I/O Schedulers
status: complete
last_verified: 2026-09-04
---

# I/O Schedulers

## One-Page Review

### Governing question

How should an operating system order, merge, delay, throttle, and dispatch block I/O so that it meets throughput, latency, fairness, isolation, and durability goals for the actual device and workload without hiding overload or starving requests?

### Essential definitions

- An **I/O scheduler** selects and orders eligible block requests before hardware dispatch; it is distinct from the CPU scheduler and the device's internal firmware scheduler.
- **Queueing delay** is time from admission to device dispatch, while **service time** is time from dispatch to completion at the measured layer.
- **Response time** or latency is the end-to-end interval for the observed request and includes queueing plus service and other stack delays.
- **Throughput** is completed bytes or operations per unit time under a stated workload.
- **Fairness** describes how service, bandwidth, time, or delay is distributed among competing flows or groups.
- **Starvation** occurs when an eligible request can be postponed without a finite bound by other arrivals.
- **Merging** combines compatible adjacent requests; **plugging** briefly accumulates submissions to expose merge and batching opportunities.
- **Queue depth** is the number of outstanding requests at a defined layer; more depth can increase parallelism and latency simultaneously.
- A **deadline** is a scheduler-enforced upper bound or preference on waiting, not a guarantee of total completion time.
- A **work-conserving** scheduler leaves no usable device capacity idle when eligible work exists; intentional idling can still improve fairness or future locality.

### Central model, mechanism, or theorem

For request $i$, decompose observed latency as

$$
T_i = T_{admit,i}+T_{queue,i}+T_{dispatch,i}+T_{device,i}+T_{complete,i}.
$$

Scheduling directly controls only parts of this path. It chooses among eligible requests subject to ordering, barrier, zone, cgroup, priority, and hardware constraints. A policy is correct only if every accepted request reaches a terminal result, required ordering edges are preserved, starvation is bounded according to policy, and feedback remains stable under changing load.

Little's law, $L=\lambda W$, relates average in-flight work $L$, completion rate $\lambda$, and average time $W$ in steady state. It explains why excess queue depth raises latency after throughput saturates, but it neither predicts tail latency nor chooses a scheduler.

### Critical invariants

- Every accepted request is eligible, dispatched, throttled, canceled, or completed in exactly one tracked state and cannot disappear between queues.
- Scheduling never violates flush, FUA, dependency, integrity, zone, or stacked-device ordering constraints.
- Temporary resource shortage triggers defined requeue or backpressure rather than success, spin, or silent loss.
- Deadline and fairness mechanisms have explicit units, scopes, and starvation bounds; priority cannot accidentally become unlimited privilege.
- Queue depth and batching do not exceed device, tag, DMA, memory, or recovery capacity.
- Cgroup attribution follows the workload and writeback contract; device-number configuration is mapped to the intended current device.
- Runtime policy changes quiesce or migrate queued state without double dispatch or reordered barriers.
- Measurements distinguish admission, queue, issue, hardware, and completion time and retain workload, scheduler, topology, cache, and queue configuration.

### Common failures

Common mistakes are optimizing average throughput while ignoring tail latency, applying disk seek algorithms to an SSD unchanged, assuming `none` means no queueing, treating deadlines as completion guarantees, giving reads permanent precedence until writes starve, confusing I/O priority with universal enforcement, setting cgroup weights without active sibling competition, measuring only application latency without block tracepoints, increasing depth after throughput saturates, hiding overload in writeback, comparing schedulers with warm caches or unmatched workloads, breaking flush order while merging, and expecting one scheduler to dominate across all devices and service-level objectives.

### Compact example

A toy scheduler has three queued reads. One has passed its waiting deadline, so it is dispatched even though another request is nearer the current disk head. This demonstrates a starvation bound layered over locality. It does not model hardware queues, writes, merges, service time, cgroups, barriers, SSD parallelism, or a Linux elevator.

### Connections

[OS-016](016-scheduling-objectives.md), [OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-045](045-buffer-cache-and-page-cache.md), [OS-050](050-tracing-file-creation-to-stable-storage.md), [OS-064](064-block-and-character-devices.md), and [OS-066](../ROADMAP.md) connect I/O scheduling to policy, measurement, caching, persistence, block requests, and asynchronous I/O.

## Governing Question

An I/O scheduler receives more eligible work than a device should accept at once. It can reorder requests for locality, merge neighbors, reserve capacity for latency-sensitive work, distribute service among groups, or pass requests through with minimal intervention.

The governing question is not which named scheduler is “best.” It is which objective, workload model, device behavior, and layer of control justify a policy, and what evidence shows that the policy improves the chosen outcome without breaking ordering, progress, or isolation elsewhere.

## Why This Matters

Storage latency spans orders of magnitude. Rotational seek and rotation, flash translation, garbage collection, controller caches, network paths, virtualization, encryption, and writeback all change the service distribution. The same request order can help one device and harm another.

Queueing magnifies failures. A burst can delay interactive reads behind bulk writes. One tenant can occupy tags needed for recovery. Excess outstanding work can inflate tail latency long after throughput has saturated.

Scheduling policy also encodes power and authority. Real-time priority can starve a system. Cgroup controls affect tenants only when attribution survives filesystems and writeback. Durable design makes these scopes observable and treats overload control as part of correctness.

## Prerequisites and Retrieval

Review [OS-016](016-scheduling-objectives.md), [OS-017](017-round-robin-and-priority-scheduling.md), [OS-019](019-fair-scheduling.md), [OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-025](025-deadlock-conditions-and-avoidance.md), [OS-043](043-file-allocation.md), [OS-045](045-buffer-cache-and-page-cache.md), [OS-046](046-journaling.md), [OS-050](050-tracing-file-creation-to-stable-storage.md), [OS-055](055-numa-memory-placement.md), [OS-064](064-block-and-character-devices.md), and [OS-063](063-direct-memory-access.md).

Retrieve these distinctions:

- admission, filesystem/writeback delay, block queueing, dispatch, device service, and completion are separate intervals;
- logical adjacency, physical locality, erase-block locality, and controller-internal placement are different properties;
- fairness can allocate operations, bytes, device time, cost, queue depth, or latency protection;
- an average, percentile, maximum, deadline miss rate, and service-level objective answer different questions;
- priority, weight, maximum rate, and latency protection are different control models;
- flush and dependency ordering restrict which requests are eligible to reorder or merge;
- software queues, hardware queues, controller queues, and media parallelism have different capacities;
- buffered write completion and background writeback attribution can be separated in time and execution context.

## Learning Objectives

After this module, you should be able to:

1. decompose end-to-end I/O latency and identify which layer a scheduler can control;
2. compare FIFO, shortest-service, scan, deadline, proportional-share, latency-feedback, and pass-through policies;
3. explain blk-mq insertion, merging, dispatch, tags, hardware contexts, requeue, and completion interactions;
4. reason about locality and queue depth for rotational disks, SSDs, NVMe, arrays, virtual disks, and network storage;
5. configure and evaluate priorities, cgroup weights, maximum rates, latency controls, and writeback attribution;
6. preserve progress, fairness, barriers, zones, reset, and hotplug under scheduling and policy changes;
7. design reproducible experiments using workload definitions, block tracepoints, latency distributions, and causal evidence.

## Core Exposition

### Scheduling layer boundaries

An application can wait in a language runtime, filesystem, page cache, writeback queue, block layer, driver, controller, network, or medium. The block I/O scheduler sees only requests that have reached its queue.

Changing the elevator cannot repair delay before admission or inside opaque firmware directly. Begin diagnosis by locating time at each boundary rather than assigning all latency to “the disk.”

### Request state

Model a request as `created -> admitted -> queued -> selected -> dispatched -> in-flight -> completed`. Throttling can delay admission, merging can replace queued representations, and requeue can return accepted work to dispatch eligibility.

Every transition has one owner and timestamp. Timeout, reset, and completion paths arbitrate terminal ownership so the scheduler never loses or dispatches a request twice.

### Objectives

Common objectives include maximum throughput, minimum mean latency, bounded tail latency, deadline miss reduction, proportional bandwidth, tenant isolation, low overhead, energy efficiency, and predictable recovery.

Objectives conflict. Larger batches improve amortization but delay individuals. Intentional idling can preserve sequential locality or fairness but waste capacity when the prediction is wrong.

### Workload description

Describe operation mix, size distribution, address distribution, locality, read/write ratio, sync/async behavior, arrival process, concurrency, burstiness, working set, cache state, flushes, discards, zones, and tenant labels.

“Random 4K” is incomplete without queue depth, read fraction, address span, and duration. A scheduler result is conditional on the workload that produced it.

### Device description

Record logical and physical sizes, rotational status, hardware queues, tags, parallelism, cache policy, firmware, transport, NUMA topology, capacity usage, thermal state, and lower stacking.

The operating system sees a model reported by the device. SSD firmware can remap logical blocks, and virtual disks can hide a remote or shared lower layer.

### FIFO

First-in, first-out preserves arrival order and has low policy overhead. It is easy to reason about but ignores locality, size, priority, and differentiated latency needs.

FIFO does not guarantee fair completion when service times vary. One large or slow request can create head-of-line blocking for many short requests.

### Shortest service or seek first

Selecting the cheapest predicted request can reduce movement and improve throughput on rotational media. The classic shortest-seek rule uses distance from the current head as a proxy.

New distant requests can starve indefinitely, and logical distance is a weak proxy for modern storage. Add aging or deadlines and validate the cost model against the device.

### SCAN and C-SCAN

SCAN moves through logical addresses in one direction, then reverses; C-SCAN services in one direction and returns. They bound some starvation and produce more regular disk-arm movement than greedy nearest selection.

These algorithms assume address correlates with physical seek. They remain useful conceptual models, not universal prescriptions for flash, arrays, or virtual disks.

### Deadline scheduling

A deadline policy maintains locality-oriented order plus waiting-time limits. When a request expires, dispatch favors progress over locality. Read and write expiration can differ to protect synchronous reads while keeping writes moving.

The deadline bounds scheduler waiting under its assumptions, not total device completion. In-flight congestion, firmware, retries, or lower layers can still exceed an application objective.

### Read/write asymmetry

Reads often block application progress, while buffered writes can be accumulated. Preferential read service can reduce interaction latency, but unlimited preference starves writeback and eventually blocks dirtying tasks.

Define a write progress rule and account for flush dependencies. Some devices also have asymmetric media costs and internal write-amplification behavior.

### Anticipatory idling

After serving a synchronous request, a scheduler can idle briefly for the same flow's next request, preserving locality and preventing bulk asynchronous work from intervening.

Idling helps when future arrivals are predictable and seeks expensive. It wastes capacity on fast queueing devices or independent hardware queues when the prediction fails.

### Proportional-share scheduling

A proportional scheduler allocates service according to weights among active entities. The resource can be modeled as bytes, device time, or estimated cost.

Weights express relative entitlement only under contention. They do not impose a maximum rate or guarantee an absolute bandwidth when device capacity changes.

### BFQ

BFQ assigns budgets and schedules queues to provide proportional sharing and low-latency behavior. It can intentionally idle and apply heuristics that trade aggregate throughput for responsiveness.

Its effectiveness depends on device queueing and workload. Configure from measured objectives; disabling low-latency heuristics can favor maximum throughput in some cases.

### mq-deadline

mq-deadline provides deadline-oriented request ordering within the blk-mq environment. It uses expiration and batching policy to balance locality, read latency, and write progress.

Its sysfs tunables change policy assumptions, not hardware guarantees. Validate starvation, latency, and throughput under the real read/write workload.

### Kyber

Kyber controls request concurrency by operation class to target read and synchronous-write latency. Feedback adjusts tokens or depth rather than seeking physical locality.

Latency targets must be attainable for the device and measured at the scheduler's boundary. Too-low targets can suppress throughput without meeting an impossible service level.

### None scheduler

The `none` elevator minimizes scheduler reordering and sends work through blk-mq mechanisms. It can suit fast devices with capable internal scheduling and per-CPU or multi-queue parallelism.

“None” does not mean no queues, merges, tags, throttling, driver delay, firmware scheduling, or cgroup effects. Measure the whole path.

### blk-mq software queues

blk-mq receives I/O through software submission contexts associated with CPUs. Requests can merge, remain in a plug, enter an elevator, or proceed toward a hardware context.

Per-CPU paths reduce shared-lock contention, but CPU migration, NUMA placement, completion affinity, and shared tag sets still affect behavior.

### Hardware contexts

Hardware dispatch queues correspond to device capabilities or driver mappings. Tags bound outstanding requests and identify them through completion.

Mapping too many producers to too few queues creates contention; spreading too broadly can lose locality or exceed useful depth. Queue topology is a measurement parameter.

### Request insertion

Insertion places a prepared request into scheduler-managed state. The scheduler can organize by sector, deadline, priority, group, or cost while retaining operation and barrier constraints.

Insertion must be bounded and concurrency-safe. An elaborate policy whose CPU overhead rivals device service time is counterproductive for fast media.

### Merging

Front and back merging combine compatible adjacent requests to reduce commands and improve sequential access. Compatibility includes operation, flags, integrity, encryption, zone, and boundary rules.

Merging reduces request count but can increase latency and create larger failure scope. Never merge across a flush or other ordering boundary.

### Plugging

Plugging temporarily accumulates requests from one execution context, exposing adjacency before dispatch. Unplug occurs at defined boundaries, waits, or pressure points.

An unbounded plug hides work and can deadlock a task waiting for I/O it has not released. The block layer owns safe plug semantics.

### Dispatch

Dispatch selects an eligible request and offers it to a hardware queue. Driver resource shortage can return a defined resource state so blk-mq retries later.

Acceptance transfers responsibility for completion. Schedulers distinguish policy delay from driver backpressure so tuning does not mask exhausted descriptors or tags.

### Requeue

Requeue returns an uncompleted request to a known eligible state. It can handle temporary hardware resource shortages or recovery.

Bound and count requeues. Immediate requeue loops consume CPU and distort latency; permanent failures need terminal completion rather than infinite retry.

### Queue depth

Some depth is needed to expose media parallelism and permit scheduling. Beyond saturation, added depth mostly increases waiting and recovery scope.

Apply Little's law only to a stable interval with consistent boundaries. Tail latency, burstiness, closed-loop load generation, and service correlation require distributional evidence.

### Adaptive depth control

A controller can raise depth while throughput improves and reduce it when latency exceeds a target. Feedback needs a stable measurement window, bounded adjustment, hysteresis, and a defined overload response.

Delays in measurement and actuation can cause oscillation. Workload changes can make yesterday's operating point invalid.

### I/O priorities

Linux exposes I/O priority classes and levels, but enforcement depends on the active scheduler and path. Real-time class can starve other work and requires restricted authority.

Priority is metadata that must survive stacking and writeback attribution to matter. Verify effective behavior rather than assuming a system call establishes end-to-end precedence.

### Cgroup I/O weights

`io.weight` expresses proportional service among active sibling groups on a specified device. A group alone can consume the available capacity because the mechanism is work-conserving.

Interpret results relative to sibling demand and scheduler support. Device major/minor keys refer to current block devices, not durable application identity.

### Maximum-rate controls

`io.max` imposes byte-per-second or operations-per-second ceilings. Rate limiting protects neighbors and shapes bursts but can add latency and underuse capacity.

Define burst behavior, hierarchy, and buffered-write interaction. An application can dirty cache quickly even while writeback is throttled later.

### Latency protection

`io.latency` protects a group with a target by throttling peers when the target is missed. It is relative within a hierarchy and cannot make the device faster than its physical service distribution.

Choose attainable targets from baseline evidence. Observe miss counters, queue depth, induced delays, and total throughput to understand the trade.

### Cost models

An I/O cost controller estimates relative work from sequential and random rates, operation type, and size, then scales the model with observed device behavior.

Models are approximations. Calibration, firmware change, stacking, thermal throttling, and workload phase shifts can change accuracy.

### Writeback attribution

Buffered writers dirty memory now while background workers submit I/O later. Cgroup writeback coordinates memory and I/O domains so work can remain attributed to its origin where filesystem support exists.

Unsupported filesystems or shared inodes can weaken attribution. Measure the actual hierarchy and filesystem rather than assuming process membership controls every write.

### Dirty throttling

Writeback policy limits dirty memory and can block producers before requests reach the block scheduler. Large caches can make short benchmarks report application throughput far above storage throughput.

Include drain time or explicit durability operations when that matches the workload. Attribute latency to dirty throttling separately from elevator queueing.

### Flush and ordering

Flushes, FUA, journal dependencies, and barriers partition the reorderable request set. A scheduler can optimize within permitted regions but cannot cross a persistence edge.

Batching flushes may improve performance only when upper-layer semantics permit coalescing. Never drop a required flush because adjacent data requests appear equivalent.

### Zoned storage

Sequential zones restrict write order and maintain write pointers. The scheduler must respect zone locks, append semantics, open-zone limits, and reset dependencies.

Sector sorting that ignores zone state can create invalid commands. Zone constraints are eligibility conditions, not mere locality hints.

### Rotational devices

Seek distance, rotation, request size, read/write direction, and command queueing influence cost. Sorting and merging can materially improve throughput.

Logical sectors are only a proxy for geometry, and firmware can reorder commands. Deadline protection is still necessary to prevent locality from starving distant work.

### SATA SSDs

SSDs remove mechanical seeks but retain channel parallelism, flash translation, garbage collection, cache, erase, thermal, and queue-depth effects. Logical adjacency can influence controller behavior without mapping directly to cost.

Moderate depth can expose parallelism; excessive depth inflates tails and makes internal scheduling opaque. Compare elevator overhead against its fairness and latency benefit.

### NVMe

NVMe provides multiple submission and completion queues with high concurrency. A minimal elevator often performs well when the controller schedules internally, but host policy still matters for groups, latency and overload.

Queue-to-CPU affinity, NUMA locality, polling, interrupt routing, tag depth, and firmware are part of the scheduling experiment.

### Arrays and stacked devices

RAID, device mapper, encryption, multipath, and logical volumes transform one upper request into several lower operations. Locality and cost at the top can differ from the physical paths.

Limits and ordering compose downward; latency and errors compose upward. Avoid independent feedback controllers that oscillate against each other across layers.

### Network and virtual storage

Remote storage adds network congestion, server queues, retransmission, replica policy, and failover. A virtual disk adds host and hypervisor scheduling beneath the guest.

Guest tuning can only influence its visible queue. Correlate identifiers across layers when diagnosing long tails.

### Multi-tenant isolation

Isolation requires a named resource, attribution, policy, admission control, and evidence. Weights provide relative sharing; caps provide ceilings; latency controls protect selected groups; none alone promises every service objective.

Reserve recovery capacity so one tenant cannot consume all tags or memory needed to abort and reset. Test adversarial mixes, not only cooperative workloads.

### Starvation and aging

A scheduler prevents starvation through deadlines, aging, quotas, round-robin service, or bounded batches. State the actual bound and exceptions for recovery or barriers.

Track oldest wait by class and group. Mean latency can look healthy while one request remains queued indefinitely.

### Priority inversion

High-priority I/O can depend on lower-priority metadata, writeback, memory reclaim, locks, or flushes. Prioritizing only the visible data request does not accelerate its dependency.

Propagate priority carefully or use dependency-aware boosting with bounds. Unlimited donation can become a policy bypass.

### Scheduler switching

Linux can switch supported elevators through a queue sysfs interface. The transition must synchronize with queued and in-flight state under block-layer rules.

Treat switching as an experiment with rollback criteria. Record the prior scheduler and tunables; names available on one kernel and device may differ on another.

### Observability boundaries

Capture arrival or submit, queue insertion, merge, issue, requeue, completion, bytes, operation, sector, cgroup, priority, CPU, software and hardware queue, tag, and error.

Block tracepoints expose important boundaries. Device telemetry and application traces extend the path. Clock domain and sampling effects must be documented.

### Latency distributions

Report percentiles, histograms, maximums, deadline misses, and sample counts, not only averages. Separate reads, writes, flushes, sizes, groups, and phases.

Percentiles from different intervals cannot always be averaged. Preserve raw or mergeable histogram data and define the population precisely.

### Coordinated omission

A closed-loop generator waits for completion before issuing the next request. During a stall it sends less work, so its measured latency distribution can omit requests that would have arrived.

Use an open-loop rate when modeling external arrivals, or correct and disclose the methodology. Also measure overload and dropped work rather than forcing every rate to appear stable.

### Benchmark controls

Fix or record cache state, data set, alignment, scheduler, tunables, cgroups, filesystem, mount options, direct versus buffered mode, depth, duration, warmup, CPU affinity, NUMA, firmware, temperature, and competing work.

Randomize experiment order, repeat trials, report variance, and drain writeback when required. A single best run is not evidence of a general policy improvement.

### Fault and recovery tests

Inject mapping shortage, tag exhaustion, slow commands, timeouts, requeues, medium errors, path failover, reset, suspend, and removal. Confirm bounded progress and exactly-once completion.

Recovery traffic must not starve behind the workload that caused failure. Validate that policy state is rebuilt after reset or scheduler switch.

## Definitions and Notation

Let request $i$ have arrival $a_i$, scheduler issue $u_i$, device completion $c_i$, size $b_i$, operation $o_i$, group $g_i$, priority $p_i$, logical address $x_i$, and scheduler deadline $d_i$. Then

$$
W_i=u_i-a_i, \qquad S_i=c_i-u_i, \qquad T_i=c_i-a_i=W_i+S_i.
$$

For interval $\Delta$, throughput is $X=\sum_{i\in C} b_i/\Delta$ and IOPS is $|C|/\Delta$ for the precisely defined completed set $C$. A deadline miss indicator is $m_i=[u_i>d_i]$ when the deadline governs scheduler issue; using completion instead changes the metric.

For active sibling groups with weights $w_g$, an idealized work-conserving share is $w_g/\sum_h w_h$. Real service differs with request cost, idling, limits, hierarchy, device parallelism and idle groups. Fairness claims therefore name the allocation unit and interval.

Little's law $L=\lambda W$ applies to a stable system with consistent population and time boundaries. It does not justify increasing $L$ after $\lambda$ saturates, and averages do not establish a tail bound.

## Mechanisms, Invariants, or Proof Structure

A reviewable I/O scheduling design discharges these obligations:

1. **Boundary:** identify where requests enter policy and which latency components are controllable.
2. **Objective:** state throughput, latency, tail, fairness, isolation, energy, or recovery goals with metrics.
3. **Eligibility:** preserve operation, barrier, dependency, zone, integrity, and lifecycle constraints.
4. **Cost:** justify locality or service estimates for the actual device and stacking topology.
5. **Progress:** bound starvation, requeue, idling, batching, throttling, and retry.
6. **Capacity:** cap queue depth, tags, DMA, memory, and recovery reservations.
7. **Attribution:** carry priority and tenant identity through writeback and stacking where supported.
8. **Feedback:** establish stable sensors, actuation, windows, bounds, hysteresis, and overload behavior.
9. **Completion:** retain exactly one owner and terminal result across dispatch, timeout and reset.
10. **Reconfiguration:** switch policy and tunables without losing work or crossing ordering edges.
11. **Observability:** separate admission, queue, issue, service, completion and durability evidence.
12. **Experiment:** reproduce workload, device, cache, topology, configuration, faults and uncertainty.

No single result discharges the others. High throughput does not prove fairness. Low average latency does not prove bounded tails. A deadline mechanism does not prove end-to-end completion. A cgroup configuration does not prove attribution. Tracepoint timestamps show observed events, not uninstrumented firmware internals.

## Alternatives and Trade-Offs

- **FIFO versus locality sorting:** FIFO preserves arrival order; sorting reduces seek-like cost and risks distant waits.
- **SCAN versus shortest-seek:** scan provides directional progress; greedy nearest selection can improve immediate cost and starve outliers.
- **Deadlines versus pure throughput:** deadlines bound scheduler waiting; strict expiry can sacrifice merges and locality.
- **Work conservation versus idling:** immediate dispatch uses capacity; idling can preserve flow locality or fairness when predictions hold.
- **Merging versus latency:** merging reduces commands; waiting for merge opportunities delays requests and expands completion scope.
- **Deep versus shallow queues:** depth exposes parallelism; excess depth inflates tail latency and reset cost.
- **Host scheduling versus device scheduling:** host policy sees processes and groups; firmware sees device internals but often hides tenant intent.
- **None versus an elevator:** minimal host policy lowers CPU overhead; an elevator can enforce latency and fairness absent from hardware.
- **Proportional weights versus hard caps:** weights share spare capacity; caps protect ceilings but can leave capacity idle.
- **Rate control versus latency control:** rates are predictable admission limits; latency feedback adapts to device behavior and can oscillate.
- **Per-process versus cgroup policy:** process policy is direct; cgroups express hierarchical service ownership and writeback concerns.
- **Global versus per-hardware-queue scheduling:** global order enables broad fairness; local queues scale and complicate cross-queue policy.
- **Polling versus interrupt completion:** polling lowers wake latency at high load; interrupts reduce CPU use and add scheduling delay.
- **Static versus adaptive tunables:** static settings are reproducible; adaptive controls follow change but require stability evidence.

## Failure Modes and Misconceptions

- **“The scheduler controls all I/O latency.”** Delay can occur before it and below it.
- **“The highest throughput scheduler is best.”** Tail, fairness, recovery and CPU cost can dominate the objective.
- **“Sector order predicts SSD cost.”** Logical position need not reveal flash placement.
- **“None means no scheduling.”** blk-mq, drivers, controllers and lower layers still queue and reorder.
- **“A deadline guarantees completion by that time.”** It commonly bounds scheduler waiting or preference only.
- **“Reads should always precede writes.”** Unbounded preference can starve writeback and block the system.
- **“More queue depth gives more throughput.”** After saturation it mainly raises latency and recovery scope.
- **“Weights guarantee bandwidth.”** They express relative sharing among active peers under supported policy.
- **“A maximum rate protects latency automatically.”** Bursts, queues and other actors can still create tails.
- **“Priority is end-to-end.”** Filesystems, writeback, stacking, scheduler support and firmware can change it.
- **“Merging adjacent sectors is always safe.”** flags, barriers, integrity, zones and encryption can prohibit it.
- **“Requeue is harmless retry.”** Loops consume CPU, lose fairness and can prevent terminal failure.
- **“Buffered benchmark completion equals device work.”** Dirty pages can remain unwritten after the test.
- **“Average latency captures responsiveness.”** Rare stalls and starvation disappear in the mean.
- **“A percentile is portable without its population.”** workload, window and aggregation define it.
- **“One synthetic benchmark predicts production.”** arrival, cache, mix, stacking and faults differ.
- **“Scheduler switching is only a string change.”** queued state and tunables require synchronized transition.
- **“Passing traces prove firmware order.”** tracing observes defined software boundaries, not all device internals.

## Worked Examples

### Example 1

A rotational disk receives scattered bulk writes and synchronous metadata reads. Sector sorting reduces seeks, while read deadlines prevent the write stream from delaying metadata indefinitely.

### Example 2

An NVMe device reaches maximum throughput at depth 32. Increasing depth to 256 leaves throughput unchanged and multiplies tail latency, so admission control caps depth near the measured knee.

### Example 3

Two active cgroups have weights 100 and 300. Under a supported proportional scheduler and comparable costs, the target split is one quarter and three quarters; when the larger group is idle, the smaller uses all work-conserving capacity.

### Example 4

A latency target is below the device's unloaded 99th percentile. The controller throttles peers but cannot meet the target, reducing aggregate throughput. Baseline evidence leads operators to choose an attainable target.

### Example 5

A buffered writer appears to finish at memory speed. The experiment includes `fsync` and writeback drain, revealing dirty throttling and storage service that were outside the original timing window.

### Example 6

A stacked encrypted volume advertises a smaller segment limit than its physical device. The upper queue splits before encryption, and the lower scheduler preserves flush flags across transformed children.

### Example 7

Tag exhaustion causes a driver resource response. blk-mq re-dispatches after completions free tags; a counter and age bound expose whether one hardware queue repeatedly loses access.

### Example 8

A timed-out request races a normal completion. An atomic state grants terminal ownership to one path, while reset reserves a tag and cannot starve behind ordinary traffic.

### Example 9

An open-loop generator at 120% capacity shows growing queues and deadline misses. A closed-loop depth-one test had hidden overload by stopping arrivals during each stall.

### Example 10

The following toy chooses an expired request before the closest sector, then resumes nearest-sector selection. It models one deadline/locality rule only and does not represent Linux mq-deadline, request merging, write batching, hardware queues, cgroups, barriers, or service time.

<!-- bijux-verify: {"id":"deadline-locality-selection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"now=12 head=100\ndispatch=B reason=expired sector=180\ndispatch=C reason=nearest sector=105\ndispatch=A reason=nearest sector=96\n","stderr":""}} -->
```python
requests = [
    {"id": "A", "sector": 96, "deadline": 20},
    {"id": "B", "sector": 180, "deadline": 10},
    {"id": "C", "sector": 105, "deadline": 18},
]
now = 12
head = 100
print(f"now={now} head={head}")

while requests:
    expired = [r for r in requests if r["deadline"] <= now]
    if expired:
        chosen = min(expired, key=lambda r: (r["deadline"], r["id"]))
        reason = "expired"
    else:
        chosen = min(requests, key=lambda r: (abs(r["sector"] - head), r["id"]))
        reason = "nearest"
    requests = [r for r in requests if r["id"] != chosen["id"]]
    head = chosen["sector"]
    print(f"dispatch={chosen['id']} reason={reason} sector={head}")
```

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects media, controllers, queues, caches, interrupts, DMA, NUMA and device parallelism. [Database Engineering](../../18-database-engineering/ROADMAP.md) connects buffer pools, WAL, fsync, compaction, tail latency, interference and durability.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes control loops, queueing, saturation, objectives, hazards, experiments and assurance. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects multi-tenant resource controls, service levels, observability and safe tuning. Within this program, [OS-064](064-block-and-character-devices.md) defines requests and [OS-066](../ROADMAP.md) develops asynchronous I/O.

## References

- Linux kernel documentation, [Multi-Queue Block IO Queueing Mechanism](https://docs.kernel.org/block/blk-mq.html), current page checked 2026-09-04. Software and hardware queues, insertion, scheduling, dispatch, tags, resources and completion.
- Linux kernel documentation, [BFQ Budget Fair Queueing](https://docs.kernel.org/block/bfq-iosched.html), current page checked 2026-09-04. Proportional sharing, budgets, latency heuristics, idling, cgroups and throughput trade-offs.
- Linux kernel documentation, [Deadline I/O Scheduler Tunables](https://docs.kernel.org/block/deadline-iosched.html), current page checked 2026-09-04. Read/write expiration, batching, FIFO selection, priorities and tunables.
- Linux kernel documentation, [Kyber I/O Scheduler Tunables](https://docs.kernel.org/block/kyber-iosched.html), current page checked 2026-09-04. Read and synchronous-write latency targets and request throttling.
- Linux kernel documentation, [Switching Scheduler](https://docs.kernel.org/block/switching-sched.html), current page checked 2026-09-04. Runtime scheduler discovery, selection and per-elevator sysfs tunables.
- Linux kernel documentation, [Block I/O Priorities](https://docs.kernel.org/block/ioprio.html), current page checked 2026-09-04. Priority classes, levels, starvation risks and scheduler-dependent support.
- Linux kernel documentation, [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), current page checked 2026-09-04. I/O weights, maximum rates, latency protection, cost models, statistics and writeback attribution.
- Linux kernel documentation, [Block Layer Statistics](https://docs.kernel.org/block/stat.html), current page checked 2026-09-04. Request counts, sectors, time, in-flight work, discard, flush and accounting semantics.
- Linux kernel documentation, [Null Block Device Driver](https://docs.kernel.org/block/null_blk.html), current page checked 2026-09-04. Configurable model queues, depths, completion modes, blocking, zoned behavior and test use.
- Linux kernel documentation, [The Linux Kernel Tracepoint API](https://docs.kernel.org/core-api/tracepoint.html), current page checked 2026-09-04. Block insertion, merge, issue, error and completion tracepoints and their boundaries.

## Exercises

### Exercise 1

Select and justify scheduling policies for a rotational archive disk, a desktop SATA SSD, a multi-queue NVMe database device, and a network-backed virtual disk.

### Exercise 2

Design a multi-tenant policy for latency-sensitive reads, bulk writeback, swap, and recovery I/O using weights, caps, latency protection, priorities, and reserved capacity.

### Exercise 3

Given arrival, insertion, issue, device-completion, and application-completion timestamps, build a latency analysis that avoids boundary confusion and coordinated omission.

### Exercise 4

Design an adaptive queue-depth controller. Specify sensors, target, control law, bounds, hysteresis, failure behavior, and stability experiments.

### Exercise 5

Build a verification and assurance plan for changing a production fleet from one I/O scheduler to another across physical and virtual device classes.

## Answers to the Exercises

### Answer 1

For the rotational archive disk, begin with mq-deadline or BFQ according to whether the objective favors bounded request waits or proportional workload service. Preserve sector locality and merging, but test read deadlines and write progress under mixed work. For the desktop SATA SSD, compare mq-deadline, BFQ and none at realistic low and moderate depths; responsiveness and background-write isolation may justify host policy even without seeks.

For the NVMe database device, begin with none or a lightweight latency controller because multiple hardware queues and controller parallelism can make host sorting expensive. Measure sync read and WAL flush tails, CPU overhead, NUMA affinity and useful depth; introduce policy only for demonstrated isolation or latency needs. For network virtual storage, recognize that the dominant scheduler may live in host, server, or array. Use conservative host depth and group controls, preserve flush semantics, and correlate guest issue through remote completion. In every case record firmware, cache, stacking, scheduler, tunables and workload; no device label alone determines the winner.

### Answer 2

Place workload classes in sibling cgroups at the resource-sharing boundary that owns the block device. Give latency-sensitive reads a measured attainable latency target and adequate weight, cap bulk writeback by bytes or IOPS to prevent unlimited queue occupation, and give ordinary services proportional weights. Treat swap and filesystem metadata as dependencies whose delay can invert application priority. Reserve driver tags and memory for timeout, flush and reset so recovery cannot be starved by full ordinary queues.

Use real-time I/O priority only for tightly authorized and bounded operations because it can starve the system. Carry attribution through supported filesystems and inspect writeback statistics; otherwise document root attribution. Validate hierarchy and major/minor targeting after device changes. Under idle peers, allow work conservation unless a hard cap serves an external goal. Test read bursts, sustained dirtying, swap storms, flushes, device stalls and recovery. Observe per-group bytes, IOPS, queue depth, induced delay, target misses, oldest wait and total throughput, then define rollback when protection damages progress or an unattainable target suppresses capacity.

### Answer 3

Define one request correlation key and clocks. Let application submission be $a$, block insertion $b$, issue $u$, device-visible completion $c$, block completion $d$, and application return $e$. Report pre-block delay $b-a$, scheduler queue $u-b$, issue-to-device interval $c-u$ where actual device telemetry exists, completion processing $d-c$, wake and application delay $e-d$, and end-to-end $e-a$. If $c$ is unavailable, label $d-u$ as issue-to-block-completion rather than hardware service.

Stratify by operation, size, group, priority, queue, depth, cache state and phase. Report histograms, percentiles, maximums, miss rates, samples, throughput, errors and dropped events. Run open-loop arrivals for an external-rate model and record overload; compare a closed-loop concurrency model but disclose that it suppresses arrivals during stalls. Synchronize or calibrate clocks across guest, host and storage telemetry. Preserve raw events and calculate percentiles from the intended population rather than averaging percentile summaries.

### Answer 4

Use completed-request latency at a precisely defined boundary plus throughput, outstanding depth, errors and requeues as sensors. Choose an attainable percentile target from unloaded and saturated baselines. Start at a safe minimum depth, increase gradually while throughput improves and target latency holds, and decrease more rapidly when the target misses. Bound depth by tags, descriptors, memory, DMA and recovery reserve. Add hysteresis, minimum dwell time and a measurement window longer than normal service variation but shorter than required adaptation.

Freeze or fall back to a conservative depth when samples are insufficient, telemetry is lost, errors rise, reset occurs, or workload classification changes. Prevent integral windup and distinguish application idleness from controller throttling. Test step loads, bursts, bimodal service, garbage collection, thermal throttling, mixed sizes, read/write changes, device failover, delayed measurements and multiple nested controllers. Plot time-series depth, issue rate, throughput, percentile latency, queue age and actuator decisions, and reject settings that oscillate or starve low-volume classes.

### Answer 5

Inventory each device's type, model, firmware, rotational flag, queues, depth, cache, filesystem, stacking, cgroup hierarchy and current scheduler/tunables. Define success and rollback metrics for throughput, CPU cost, read/write and flush latency distributions, deadline misses, oldest wait, errors, resets, recovery and tenant shares. Create representative open- and closed-loop workloads plus production replay where safe. Control cache, writeback drain, data set, duration, warmup, affinity, NUMA, temperature and competing traffic.

Validate scheduler availability and switching on a canary, preserve flush and zone behavior, and inject tag shortage, slow requests, requeue, timeout, reset and path loss. Roll out by device class with randomized matched comparisons, multiple trials and sufficient observation across workload cycles. Use block insertion, merge, issue, requeue and completion traces plus cgroup and application telemetry. Record kernel, configuration, exact command, time, samples, raw histograms, negative results and rollback events. A fleet change is justified only within tested classes; virtual or firmware-divergent devices retain separate conclusions.
