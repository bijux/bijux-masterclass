---
module_id: OS-070
program: Operating Systems
level: 2
module_number: 70
title: Designing an I/O Path for Latency or Throughput
status: complete
last_verified: 2026-09-04
---

# Designing an I/O Path for Latency or Throughput

## One-Page Review

### Governing question

How should an operating-system engineer design an I/O path for a stated latency distribution, throughput target, fairness requirement, durability contract, and failure model while controlling queues, batching, copies, interrupts, polling, locality, backpressure, and recovery across every layer?

### Essential definitions

- **End-to-end latency** is elapsed time from the application's chosen arrival point to its chosen terminal result, including admission, queueing, execution, completion, and wakeup.
- **Service time** is time an actively serving resource spends on a request; it excludes time waiting before service at that resource.
- **Queueing delay** is time eligible work waits for service, credits, tags, buffers, CPU, or another dependency.
- **Throughput** is completed useful work per unit time under a defined workload and correctness contract.
- **Bandwidth** is completed payload bytes per unit time; **IOPS** counts operations, so request size connects the two.
- **Queue depth** is outstanding work at a defined layer, not a single system-wide number.
- **Batching** amortizes fixed work over several operations while adding dwell time and a larger failure or fairness unit.
- **Backpressure** bounds admitted work when downstream capacity is unavailable, preserving memory and latency rather than building an unbounded queue.
- **Open-loop load** arrives independently of completion; **closed-loop load** lets each client issue more work only after completions free concurrency.
- A **service-level objective (SLO)** names the population, percentile, threshold, time window, exclusions, and correctness semantics of acceptable service.

### Central model, mechanism, or theorem

Decompose request latency as

$$
L=L_{admit}+L_{queue}+L_{prepare}+L_{device}+L_{complete}+L_{wakeup}.
$$

For a stable observed boundary, Little's Law gives

$$
N=\lambda W,
$$

where $N$ is average work in that system, $\lambda$ is completion rate, and $W$ is average residence time. The relation is an accounting identity under its assumptions, not a tail-latency guarantee. Increasing concurrency raises throughput only until a bottleneck saturates; beyond the knee it mostly raises queueing delay.

A sound design first fixes semantics and the measurement boundary, then assigns a bounded budget to every component. A latency-oriented path limits queues, batches, cache-line movement, remote topology, wakeups, and interference. A throughput-oriented path exposes parallelism, coalesces fixed costs, pipelines stages, and keeps bottlenecks busy. Both need admission control, fairness, cancellation, durability, error propagation, and a recovery path that remains live under saturation.

### Critical invariants

- Every metric names the same request population, start event, terminal event, clock, and semantic completion.
- The sum of queue capacities and retry paths is bounded by memory, tags, buffers, deadlines, and recovery needs.
- A request has one owner and one terminal result across submission, timeout, cancellation, completion, retry, reset, and removal.
- Publication makes descriptors and payload visible before a device, worker, or peer is notified.
- Batching never crosses ordering, durability, tenant, security, or deadline boundaries that require separation.
- Completion means no more than the lowest layer's verified guarantee; submitted, transferred, acknowledged, and durable remain distinct.
- Reserved capacity permits control, flush, timeout, and recovery work even when the data path is saturated.
- Backpressure occurs before unbounded queues consume memory and destroy tail latency.
- Queue, CPU, memory, interrupt, and device placement follow measured topology and do not silently serialize on one shared object.
- Optimization is accepted only when workload-representative evidence preserves correctness, fairness, recovery, and SLOs.

### Common failures

Common mistakes are optimizing mean latency while p99.9 explodes, reporting device time as application latency, using maximum queue depth as a target, comparing different durability semantics, measuring a closed-loop generator that hides overload, increasing batch size without a dwell deadline, polling idle queues at full CPU, pinning submission and completion to remote NUMA nodes, adding queues that contend on one lock, allowing retries to bypass admission control, dropping cancellation races, starving reads behind writeback, treating utilization as throughput, tuning one layer while a stacked layer clamps it, and benchmarking a cache rather than the intended device.

### Compact example

A path completes 100,000 operations per second with 200 microseconds mean residence time. Little's Law implies an average of 20 operations inside the measured boundary. If instrumentation instead reports 80 outstanding operations at the same completion rate, either mean residence time is about 800 microseconds, the boundaries differ, or the system is not in the assumed steady state. The calculation diagnoses accounting; it does not predict percentiles or identify the bottleneck.

### Connections

[OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-052](052-smp-kernel-synchronization.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-063](063-direct-memory-access.md), [OS-065](065-i-o-schedulers.md), [OS-066](066-asynchronous-i-o.md), [OS-067](067-zero-copy-and-kernel-bypass.md), [OS-068](068-storage-queues-and-nvme.md), and [OS-069](069-operating-system-support-for-persistent-memory.md) connect I/O design to measurement, concurrency, locality, scheduling, queues, direct paths, and durability.

## Governing Question

“Fast I/O” is not one objective. A transaction log may value bounded durable-write latency. A scan engine may value aggregate bandwidth. A metadata service may value small-read p99.9 under background writeback. A batch system may accept long individual waits if total completion time improves. Each objective chooses a different operating point.

The governing question is how to derive a path from a complete service contract. The path spans application admission, system calls or shared rings, virtual memory, filesystem, block layer, driver, DMA, transport, device firmware, media, completion, scheduler wakeup, and application processing. A local improvement can move cost to another stage, weaken semantics, or worsen the tail.

## Why This Matters

Modern storage can complete work quickly enough that locks, cache misses, address translation, descriptor construction, MMIO, interrupts, scheduler transitions, and accounting become material. A single shared queue can serialize a device designed for parallelism. Conversely, thousands of outstanding requests can conceal useful service behind milliseconds of queueing.

Latency and throughput interact nonlinearly near saturation. Small increases in offered load can produce large queue growth. Retries, background writeback, firmware maintenance, garbage collection, remote paths, and thermal limits add bursty service variation. Mean values hide the requests that encounter several such events at once.

An operating system must also preserve multi-tenant fairness and recovery. A path that reaches record IOPS by consuming every tag and CPU can be unable to send a flush, abort, health command, or reset request. Performance architecture is resource and failure architecture.

## Prerequisites and Retrieval

Review [OS-003](003-system-calls-and-user-kernel-transitions.md), [OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-024](024-atomic-operations.md), [OS-031](031-address-translation.md), [OS-039](039-shared-pages-and-page-cache.md), [OS-052](052-smp-kernel-synchronization.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-063](063-direct-memory-access.md), [OS-064](064-block-and-character-devices.md), [OS-065](065-i-o-schedulers.md), [OS-066](066-asynchronous-i-o.md), [OS-067](067-zero-copy-and-kernel-bypass.md), [OS-068](068-storage-queues-and-nvme.md), and [OS-069](069-operating-system-support-for-persistent-memory.md).

Retrieve these distinctions:

- request arrival, admission, submission, device acceptance, transfer, completion, wakeup, application observation, and durability are different events;
- service time, queueing time, response time, and inter-arrival time are different measurements;
- concurrency, queue capacity, active depth, batch size, and hardware parallelism are different quantities;
- IOPS, payload bandwidth, bus bandwidth, useful throughput, and CPU efficiency answer different questions;
- average, median, percentile, maximum, histogram, and deadline-miss ratio cannot substitute for one another;
- interrupt moderation, busy polling, hybrid polling, and blocking trade CPU and wakeup delay differently;
- open-loop and closed-loop generators behave differently under overload;
- merge, coalescing, reordering, and batching are distinct transformations;
- timeout, cancellation, retry, abort, reset, and terminal completion are distinct lifecycle events;
- logical completion, controller completion, and durable completion can have different ordering requirements.

## Learning Objectives

After this module, you should be able to:

1. translate workload semantics and SLOs into an end-to-end latency budget and throughput target;
2. model queue occupancy, service demand, utilization, bottlenecks, batching, and saturation without overclaiming from averages;
3. choose synchronous or asynchronous interfaces, queue topology, completion strategy, buffer ownership, copying, and scheduling policy;
4. design bounded admission, backpressure, prioritization, cancellation, timeout, retry, and recovery capacity;
5. reason about CPU, cache, NUMA, DMA, interrupt, controller, transport, and media locality;
6. build experiments that preserve workload, durability, caching, warmup, and failure semantics;
7. interpret traces, histograms, device counters, pressure metrics, and coordinated omissions as scoped evidence.

## Core Exposition

### Start from the contract

Write the contract before choosing an API. Identify operation mix, sizes, access distribution, read/write dependencies, durability, ordering, concurrency, arrival process, tenants, deadlines, overload behavior, and failure response.

A target such as “one million IOPS” is incomplete. One million cached 512-byte reads, 4 KiB random durable writes, and 1 MiB sequential reads exercise different paths and imply different useful work.

### Define the latency boundary

Application-visible latency usually begins when work becomes eligible for admission and ends when the application receives its promised result. Measuring only driver issue to completion omits upstream queueing and scheduler delay.

Record nested timestamps so components add consistently. Use one clock domain or measure and correct conversion. Trace overhead and missing events must be quantified.

### Decompose latency

Useful components include admission, software queue, allocation and mapping, filesystem, scheduler, driver preparation, device queue, transport, media, completion handling, wakeup, and postprocessing.

The decomposition prevents a false diagnosis. A device can complete in 50 microseconds while the request spends 5 milliseconds behind an application semaphore.

### Define throughput and useful work

Throughput counts operations that meet correctness and quality requirements. Retries, speculative work later discarded, background relocation, and checksum repair consume capacity but are not necessarily useful completions.

For fixed request size $s$, payload bandwidth is approximately $\lambda s$. With mixed sizes, use completed bytes over the interval rather than mean size multiplied by an unrelated IOPS average.

### Percentiles and tails

A p99 of 2 ms means 99 percent of the defined sample completed within 2 ms for that observation set. It says nothing about p99.9, maximum, burst duration, or which tenants suffered misses.

Report histograms or sufficient quantiles with sample count and window. Aggregate percentiles cannot be averaged across hosts; merge distributions or raw histograms with compatible buckets.

### Deadline misses

When users care about a threshold, report the miss ratio and sequences of misses. Two systems with equal p99 can differ if one produces isolated misses and another stalls for a minute.

Tie deadlines to admission. Work waiting in an unmeasured client queue still violates the user's experience even if device-side latency remains low.

### Little's Law

For a stable measured system, average number in system equals average throughput times average residence time. Ensure the same boundary and population define all three values.

Little's Law does not require exponential arrivals or service, but finite, stable observation and consistent accounting matter. It gives an average identity, not a queue-depth prescription or percentile model.

### The saturation knee

At low load, concurrency can cover idle gaps and expose device parallelism. Throughput rises while latency stays near service time. Near full utilization, small service variation creates queues. Past the knee, throughput flattens and latency climbs.

Latency-sensitive operation usually leaves headroom. Throughput-oriented operation may run closer to saturation but still needs bounded queues and recovery reserves.

### Bottleneck analysis

The maximum steady useful throughput is limited by the tightest resource: CPU cycles, memory bandwidth, lock serialization, IOMMU, PCIe, network, controller queues, media channels, firmware, or durability barriers.

Measure utilization and service demand at each candidate. A resource can be saturated by inefficient overhead while useful throughput remains low.

### Queue topology

There may be application queues, work queues, io_uring rings, filesystem queues, blk-mq software contexts, scheduler queues, hardware dispatch queues, controller queues, and media queues.

Inventory every queue's capacity, admission rule, owner, ordering, priority, timeout, cancellation, and observability. “Queue depth 32” is meaningless without a layer.

### Queue depth

Depth should expose enough independent work to cover service parallelism and variability. More depth increases memory, tag occupation, cancellation work, reset scope, and worst-case wait.

Use latency targets or a controller that adjusts concurrency from measured results. Maximum hardware capacity is an upper bound, not an optimum.

### Admission control

Admission decides whether to accept, delay, reject, shed, or downgrade work before scarce downstream resources are consumed. It should account for tenant, class, deadline, memory, tags, buffers, and recovery reserve.

Rejecting early with a clear overload result can preserve service for admitted work. An unbounded queue converts overload into timeouts and memory pressure.

### Backpressure

Backpressure propagates capacity information toward producers. Blocking, bounded channels, credits, rate limits, congestion signals, and asynchronous “try later” results are possible mechanisms.

Retries must reenter admission with budgets and jitter. Immediate unlimited retry creates positive feedback precisely when the path is least able to absorb it.

### Synchronous I/O

A synchronous call can be optimal for low concurrency, simple control flow, or an inherently serialized device. It naturally limits one thread's outstanding work.

Thread-per-request scaling adds stacks, wakeups, scheduling, and cache movement. Multiple synchronous workers can still provide bounded concurrency when simplicity outweighs peak throughput.

### Asynchronous I/O

Asynchronous submission separates issue from completion and lets a small number of threads maintain several in-flight operations. It enables pipelining and completion batching.

The application must own request identity, buffers, cancellation, short results, partial failure, and shutdown across the entire lifetime. Asynchrony moves waiting; it does not remove it.

### Shared submission and completion rings

Shared rings can amortize system calls and reduce descriptor copying. Producer and consumer indices require memory ordering, bounded arithmetic, and explicit wakeup behavior.

Submission queue polling can remove syscalls while active but dedicates kernel CPU and still needs a wakeup protocol after idle. Treat it as a resource allocation decision.

### Batching

Batching can amortize system calls, locks, MMIO doorbells, interrupts, DMA mappings, network framing, checksums, and persistence barriers.

Bound both batch count and dwell time. A size-only batch can wait forever at low arrival rates. Flush immediately for an expired deadline, ordering boundary, durability boundary, or administrative request.

### Merging and coalescing

Adjacent block requests can be merged to reduce per-request work. Interrupt moderation can group completions. Both improve efficiency but can add delay and blur attribution.

Do not merge across incompatible flags, protection domains, priorities, zones, or durability requirements. Preserve error reporting for constituent requests.

### Copies and data movement

Copies consume CPU and memory bandwidth but can improve locality, alignment, isolation, ownership simplicity, and caching. Removing a copy may introduce page pinning, registration, fragmentation, or cross-NUMA traffic.

Count bytes moved at every layer. Optimize the dominant movement under the real size distribution rather than assuming zero-copy wins universally.

### Registered and fixed buffers

Pre-registering buffers can amortize pinning and mapping for repeated I/O. It consumes locked memory, complicates reclamation, and expands the lifetime of access permissions.

Bound registered capacity per tenant, validate indices and lengths, revoke before teardown, and measure IOMMU and cache effects.

### DMA descriptors

Scatter-gather can avoid linearization but increases descriptor count and device parsing. Coalescing segments can reduce descriptors at the cost of copying or allocation.

Respect segment count, alignment, boundary, mask, and lifetime limits. A mapping failure is a normal backpressure or error path, not permission to reuse an invalid address.

### Interrupt-driven completion

Interrupts let CPUs sleep or perform other work until completion. MSI-X and multiple queues can preserve locality and parallelism.

Interrupt entry, moderation, handler work, softirq or threaded processing, and scheduler wakeup all add latency. Route vectors to CPUs that consume the completions, subject to isolation and fairness needs.

### Polling

Busy polling repeatedly checks completion state and can remove interrupt and wakeup delay. It spends CPU and memory-system capacity even when no work completes.

Polling works best for busy low-latency queues with dedicated cores. Measure energy, sibling interference, thermal behavior, and the effect on application processing.

### Hybrid polling

Hybrid polling sleeps for an estimated portion of service time and then polls near expected completion. It can reduce wasted CPU compared with full polling while retaining some latency benefit.

Estimation errors add sleep delay or excessive spin. Service distributions that change with queue depth, maintenance, or remote paths require adaptive and bounded behavior.

### Completion batching

Draining several completions per interrupt or poll amortizes fixed work and improves cache locality. An unbounded drain can monopolize a CPU and starve other queues.

Use a work budget, preserve fairness, and reschedule when more work remains. Measure the first completion's latency and the last completion's delay separately.

### CPU affinity and cache locality

Keeping submission, queue state, interrupt, and completion on a nearby CPU reduces cache-line bouncing. Per-CPU software queues can avoid a shared lock.

Over-pinning can leave idle capacity unusable and magnify imbalance. Migration needs an ownership protocol; it is not just changing an affinity mask.

### NUMA placement

Place buffers, rings, queue metadata, device interrupts, and worker threads near the device and one another when possible. Remote DMA and CPU access can consume interconnect bandwidth and add tail variability.

Topology is dynamic under failover and scheduler movement. Record actual placement during tests, not only intended configuration.

### Locking and contention

A path with many queues can still serialize on an allocator, inode, journal, statistics counter, completion list, or device lock. Profile cache-line contention and critical-section hold time.

Sharding reduces contention but introduces imbalance, cross-shard ordering, and aggregation cost. Align ownership with durable domain boundaries.

### I/O scheduling

Schedulers can reorder, merge, prioritize, and budget work for fairness or latency. A direct-dispatch policy reduces software work but delegates more behavior to device firmware and admission control.

Choose from workload evidence. A fast device can still need policy when background writes interfere with foreground reads or tenants compete.

### Read/write interference

Large writeback queues can delay reads through shared device resources, firmware housekeeping, or durability barriers. Writeback throttling can preserve a read-latency target by reducing dirtying pressure.

Measure at application and block boundaries. A write cap that protects device latency can move waiting into memory reclaim or an application queue.

### Priority and fairness

Priority should reserve bounded service for important work without starving lower classes. Strict priority can make background recovery or checkpointing never finish.

Use budgets, deadlines, weighted service, or reserved shares. Validate fairness over time windows and under adversarial request sizes.

### Durability cost

Write completion, cache flush, FUA, filesystem transaction commit, replica acknowledgement, and application durable acknowledgement have distinct costs.

Group commit can amortize barriers while adding dwell delay. Compare paths only at equivalent durability and recovery semantics.

### Timeouts and cancellation

A timeout is an observation that a deadline passed, not proof the device stopped. Cancellation races with issue and completion. The request and buffer remain owned until a terminal protocol resolves access.

Choose timeouts from SLO and recovery behavior, not arbitrary multiples of the mean. Too short creates retry storms; too long retains scarce resources and delays failover.

### Retry policy

Retry only errors classified as transient and operations safe to repeat or protected by idempotency. Bound count, elapsed time, and concurrency.

Retries consume the same bottleneck and must appear in telemetry. Hidden retries make device latency look acceptable while end-to-end latency violates the SLO.

### Recovery reserves

Reserve tags, queue entries, memory, worker time, and administrative capacity for flush, abort, health, reset, reconnect, and teardown.

A system that uses every resource for ordinary data can deadlock its recovery path. Test recovery while maximum admitted load is active.

### Stacked paths

Filesystems, device mapper, encryption, integrity, RAID, multipath, virtualization, network transport, and backend storage each add queues and constraints.

Observe the entire stack. Tuning a leaf queue may have no effect if an upper layer serializes or a lower remote target is saturated.

### Workload models

Specify size distribution, offsets, locality, read/write ratio, dependency, think time, burstiness, concurrency, data compressibility, cacheability, and duration.

Uniform random and fixed-size benchmarks are useful controls but rarely complete production models. Preserve representative traces carefully and scrub sensitive content.

### Open-loop versus closed-loop

Closed-loop clients wait for completions before issuing more, so slow service reduces offered load. This can hide overload and coordinated omission.

Open-loop generation follows an external arrival schedule and exposes queue growth and deadline misses. When the system cannot keep up, bound the generator's own queue and report dropped or late arrivals.

### Warmup and steady state

Caches, allocation, JIT compilation, queue construction, device power state, thermal limits, garbage collection, and write amplification change over time.

Separate cold-start, warmup, steady-state, and long-run degradation. A short run can measure cache fill rather than media or avoid firmware maintenance entirely.

### Cache control

State whether data is served by application cache, page cache, controller cache, or media. Working set relative to cache capacity and reuse distribution determine hit rates.

Dropping caches changes more than one variable and can require privilege. Use explicit datasets, independent runs, and observed hit evidence.

### Instrumentation

Collect application timestamps and outcomes, queue occupancy, admission decisions, batch dwell, block tracepoints, in-flight counts, latency histograms, interrupt and CPU placement, device logs, errors, retries, resets, and pressure.

Block statistics are cumulative and layer-specific. They can reset on boot or reattachment and may count merges differently. Derive rates from validated intervals and stable identity.

### Pressure and interference

I/O pressure measures time tasks stall because resources are unavailable. Per-cgroup views help attribute interference that device-wide counters cannot.

Correlate pressure with latency and queue data. Pressure is an effect signal, not by itself the exact root cause.

### Experiment design

Change one mechanism at a time after fixing semantics and workload. Randomize run order when thermal or temporal drift matters, repeat enough times, and retain raw distributions.

Include overload, mixed tenants, faults, cancellation, reset, failover, and recovery. A steady healthy benchmark validates only a narrow operating region.

### Choosing the operating point

Plot throughput, percentile latency, CPU, energy, queue depth, and error rate against offered load or concurrency. Select a point with required headroom before the latency cliff.

Automated controllers need hysteresis, bounded steps, safe defaults, and rollback. A metric delay can otherwise drive oscillation.

## Definitions and Notation

Let:

- $A_i$ be arrival time of request $i$ at the defined boundary;
- $C_i$ be terminal completion time of request $i$ under the promised semantics;
- $W_i=C_i-A_i$ be response time;
- $S_i$ be total active service demand across relevant resources;
- $Q_i=W_i-S_i$ be total waiting under a chosen decomposition;
- $\lambda$ be useful completion rate;
- $N$ be average number of requests inside the same boundary;
- $s_i$ be useful payload bytes for request $i$;
- $B$ be useful payload bandwidth;
- $U_r$ be utilization of resource $r$;
- $D_r$ be average service demand at resource $r$ per useful completion;
- $K_j$ be capacity of queue or resource pool $j$;
- $b$ be batch size and $T_b$ the maximum batch dwell;
- $d_i$ be request deadline;
- $I_i$ indicate whether request $i$ misses its deadline.

End-to-end response decomposes as

$$
W_i=Q_i+S_i,
$$

with a more detailed component sum chosen from observable events.

Little's Law is

$$
N=\lambda E[W]
$$

for a stable, consistently bounded population. Useful bandwidth over interval $T$ is

$$
B=\frac{\sum_{i\in completed(T)}s_i}{T}.
$$

Resource demand bounds throughput:

$$
\lambda \le \min_r \frac{1}{D_r}
$$

when each normalized resource supplies one unit of service capacity. Real resources can have several servers and nonlinear service, so adjust the capacity model explicitly.

The deadline-miss ratio is

$$
M=\frac{\sum_i I_i}{n},\qquad I_i=\begin{cases}1,&C_i>d_i\\0,&C_i\le d_i.\end{cases}
$$

Batch dwell is bounded by

$$
\operatorname{dispatch}\quad\text{when}\quad count\ge b\ \lor\ now-first\_arrival\ge T_b.
$$

These equations organize evidence. They do not assume a particular arrival distribution, scheduler, device, or percentile model unless one is stated separately.

## Mechanisms, Invariants, or Proof Structure

### Obligation 1: preserve semantic equivalence

Every candidate path implements the same data, ordering, durability, isolation, and error contract before its performance is compared.

Counterexample: buffered writes acknowledged from memory are compared with synchronous durable writes and declared faster.

### Obligation 2: use one measurement boundary

Arrival, completion, population, and queue counts refer to the same operations and boundary. Nested measurements are labeled rather than substituted.

Counterexample: application latency includes admission, while throughput counts only requests that reached the device, invalidating a Little's Law check.

### Obligation 3: bound every queue

Each queue and retry reservoir has a finite capacity and an overload action. The sum fits memory, tags, buffers, deadlines, and recovery requirements.

Counterexample: asynchronous submission accepts unlimited descriptors while the device remains at fixed throughput, so memory and p99 latency grow without bound.

### Obligation 4: publish safely

Descriptors, mapped payload, ownership, and request identity become visible before notification. Completion fields become visible before their result is accepted.

Counterexample: a producer rings a doorbell before the DMA descriptor's final fields are device-visible.

### Obligation 5: terminate exactly once

Submission, timeout, cancellation, retry, reset, and late completion converge on exactly one terminal application result and one buffer release.

Counterexample: timeout frees a buffer while a device can still DMA, then late completion writes into reused memory.

### Obligation 6: preserve deadline and fairness boundaries

Batching, merging, scheduling, and completion draining cannot indefinitely delay an older, higher-priority, or different-tenant request.

Counterexample: a low-rate request waits forever for a size-only batch to fill.

### Obligation 7: retain recovery capacity

Ordinary work cannot consume resources reserved for control and recovery. Resets and failover are tested at full admitted load.

Counterexample: all tags are occupied by timed-out data commands, leaving no tag for an abort or flush required to resolve them.

### Obligation 8: align topology

Queue state, buffers, submission CPUs, interrupt CPUs, workers, and devices have measured placement. Sharing and migration are explicit.

Counterexample: per-CPU queues appear scalable, but all completions update one remote-NUMA counter protected by a lock.

### Obligation 9: measure open-loop overload

The experiment records intended arrivals, actual admissions, drops, client-side waiting, completions, and late results. Load generation does not silently self-throttle.

Counterexample: one outstanding request per client makes offered load fall when latency rises, concealing the saturation cliff.

### Obligation 10: attribute tails

Trace correlation distinguishes admission, software, device, completion, wakeup, retry, and recovery delays for slow requests, not only averages.

Counterexample: a high device-completion percentile is blamed on media although traces show completion threads waiting for CPU.

### Obligation 11: contain tunable change

A tuning change records previous value, target identity, scope, workload, expected effect, rollback trigger, and measured result. Stacked layers are checked.

Counterexample: an operator changes a sysfs queue setting on a transient device name and affects the wrong volume after reattachment.

### Obligation 12: scope assurance

Results state hardware, firmware, kernel, filesystem, mount, scheduler, cache, topology, workload, duration, power state, faults, and confidence limits.

Counterexample: a five-second single-tenant synthetic run is used to guarantee production p99.99 during device reset.

## Alternatives and Trade-Offs

- **Synchronous threads versus asynchronous rings:** threads simplify ownership; rings reduce crossings and support more in-flight work but expand lifecycle complexity.
- **Interrupts versus polling:** interrupts save CPU at low activity; polling can reduce wakeup delay at sustained load while consuming dedicated resources.
- **Classic versus hybrid polling:** classic spin minimizes sleep uncertainty; hybrid mode saves CPU if service-time estimates remain useful.
- **Shallow versus deep queues:** shallow queues bound wait and failure scope; deeper queues expose parallelism and absorb bursts until they pass the saturation knee.
- **Small versus large batches:** small batches reduce dwell and fairness distortion; large batches amortize fixed costs.
- **Copies versus zero-copy:** copies cost bandwidth but simplify ownership and isolation; zero-copy can save movement while adding registration, pinning, and lifetime work.
- **Per-CPU versus shared queues:** per-CPU paths reduce contention; shared paths pool capacity and can simplify global ordering.
- **Direct dispatch versus scheduling:** direct dispatch reduces policy overhead; scheduling can preserve fairness, merge work, and protect latency classes.
- **Busy headroom versus maximum utilization:** headroom absorbs variation and faults; maximum utilization raises throughput in stable conditions but magnifies tails.
- **Open-loop versus closed-loop testing:** open-loop exposes overload; closed-loop models concurrency-limited clients and is easier to bound.
- **Fixed concurrency versus adaptive control:** fixed settings are predictable; adaptation tracks drift but can oscillate or chase noisy measurements.
- **Registered versus dynamic buffers:** registration amortizes mappings; dynamic buffers conserve pinned capacity and simplify tenant turnover.
- **Locality versus work stealing:** strict affinity preserves caches; stealing handles imbalance and failures but moves state.
- **Group commit versus per-request durability:** grouping amortizes persistence cost; individual commits reduce dwell and coupling.
- **Fail fast versus retry:** failing fast protects capacity and exposes uncertainty; bounded retry can mask transient faults for idempotent work.
- **Rich instrumentation versus minimum overhead:** detailed traces explain tails; always-on cost can perturb the path and must be budgeted.

## Failure Modes and Misconceptions

- **“Highest IOPS is best.”** useful performance depends on sizes, latency, correctness, CPU, fairness, and recovery.
- **“Average latency represents users.”** tails and correlated stalls can dominate experience.
- **“Device latency is end-to-end latency.”** admission and wakeup can be larger than device time.
- **“Queue depth is one number.”** every layer can queue independently.
- **“Maximum supported depth is optimal.”** it is capacity, not an operating target.
- **“More queues remove contention.”** shared allocators, locks, cache lines, journals, or devices can remain bottlenecks.
- **“Asynchronous means nonblocking.”** a path can block on allocation, page faults, ring space, or dependent work.
- **“Zero-copy means zero overhead.”** pinning, mapping, validation, cache misses, and ownership remain.
- **“Polling is always lower latency.”** idle spin, contention, power, and thermal throttling can make it worse.
- **“Interrupt moderation is free throughput.”** it adds completion dwell and burstiness.
- **“A larger batch only improves efficiency.”** it can violate deadlines, ordering, fairness, or durability separation.
- **“Utilization equals useful throughput.”** retries and overhead can saturate a resource without useful progress.
- **“One fast benchmark proves the design.”** workload and failure coverage define the claim.
- **“Closed-loop load reveals overload.”** completion-dependent generation can hide demand and coordinated omission.
- **“Percentiles can be averaged.”** aggregate quantiles require compatible distribution data.
- **“Warm cache results describe storage.”** they may describe memory and lookup overhead instead.
- **“Direct I/O always reaches media.”** caches and durability semantics still depend on the full path.
- **“Timeout stops I/O.”** access may continue until cancellation or recovery proves containment.
- **“Retries increase reliability without cost.”** they add load and can duplicate uncertain non-idempotent work.
- **“Backpressure is a performance failure.”** bounded refusal can preserve latency and availability.
- **“CPU affinity guarantees locality.”** memory, interrupts, device, and actual execution placement must agree.
- **“One scheduler is fastest.”** policy value depends on device and competing workloads.
- **“Counters explain the tail.”** cumulative aggregates need request-level correlation.
- **“Recovery is outside the data path.”** saturation and resource ownership determine whether recovery can run.

## Worked Examples

### Example 1

A storage service completes 100,000 operations per second with mean end-to-end residence time 200 microseconds. Using seconds,

$$
N=100{,}000\times 0.0002=20.
$$

Twenty requests should be inside that boundary on average in stable observation. A measured average of 80 signals a boundary mismatch, non-steady interval, or approximately four-times-greater residence time.

### Example 2

The following runnable calculation compares four measured operating points. It computes average concurrency from Little's Law and marks whether p99 remains within a 500-microsecond SLO:

<!-- bijux-verify: {"id":"io-operating-point-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"rate=50000 mean_us=120 average_in_system=6.0 p99_us=220 slo=True\nrate=100000 mean_us=200 average_in_system=20.0 p99_us=410 slo=True\nrate=120000 mean_us=500 average_in_system=60.0 p99_us=1600 slo=False\nrate=121000 mean_us=900 average_in_system=108.9 p99_us=4300 slo=False\nselected_rate=100000 selected_average_in_system=20.0\n","stderr":""}} -->
```python
points = [
    (50000, 120, 220),
    (100000, 200, 410),
    (120000, 500, 1600),
    (121000, 900, 4300),
]

eligible = []
for rate, mean_us, p99_us in points:
    average = rate * mean_us / 1000000
    within_slo = p99_us <= 500
    print(
        f"rate={rate} mean_us={mean_us} "
        f"average_in_system={average:.1f} p99_us={p99_us} slo={within_slo}"
    )
    if within_slo:
        eligible = eligible + [(rate, average)]

selected = max(eligible, key=lambda item: item[0])
print(
    f"selected_rate={selected[0]} "
    f"selected_average_in_system={selected[1]:.1f}"
)
```

The selected measured point is 100,000 completions per second. The next point gains 20 percent throughput but violates the tail target sharply. This table is illustrative evidence, not a general queueing prediction.

### Example 3

A batcher dispatches at 32 requests or 50 microseconds from the first arrival. At heavy load, batches reach 32 and amortize one doorbell. At low load, the timer sends partial batches so a lone request waits at most the configured dwell, subject to scheduler precision.

Ordering-sensitive flush requests force dispatch of prior writes and create a separate boundary. Mixing them into later writes merely to fill the batch would change durability semantics.

### Example 4

An NVMe queue using interrupts has 85-microsecond p99 and 4 percent CPU at 5,000 IOPS. Busy polling lowers p99 to 62 microseconds but consumes a full core. At 500 IOPS, polling produces the same p99 after thermal throttling and interferes with the application.

The design selects interrupts for the low-rate class and a dedicated polled queue for sustained latency-critical traffic. CPU and energy are part of the result, not externalities.

### Example 5

A service raises device queue depth from 32 to 256. Throughput changes from 700,000 to 715,000 IOPS, while p99 rises from 600 microseconds to 4.8 milliseconds and reset must resolve eight times more requests.

The 2.1 percent throughput gain does not justify the tail and recovery cost under a 1-millisecond SLO. Capacity 256 remains useful for other workloads; it is not selected as this workload's active limit.

### Example 6

Application logs report 12-millisecond slow writes. Block tracepoints show 400 microseconds between issue and completion. Correlated timestamps show 9 milliseconds before block issue, during memory reclaim, and 2 milliseconds waiting for the completion thread to run.

Changing device firmware cannot solve the dominant waits. Admission, dirty-page control, memory pressure, and completion CPU scheduling are the proper investigation surfaces.

### Example 7

Two tenants share one device. Tenant A issues 1 MiB requests at depth 128; tenant B issues 4 KiB reads with a 2-millisecond deadline. FIFO bytes allow A to occupy tags and device time long enough that B misses deadlines.

A scheduler or admission layer budgets service by class, limits A's outstanding bytes, and reserves tags for B. Fairness is evaluated in service cost and deadlines, not raw request count alone.

### Example 8

A remote storage write times out after the target may have committed it. Blind retry can apply a non-idempotent update twice. Releasing the buffer immediately can also race continuing DMA or transport use.

The request enters an uncertain state, retains ownership, and resolves through an idempotency key, operation-status query, transport abort, or path reset. Retry consumes its remaining deadline and admission budget.

### Example 9

A closed-loop benchmark runs 64 clients with one outstanding operation each. When the service slows, offered rate falls from 200,000 to 80,000 IOPS, and reported latency samples exclude arrivals that a real upstream producer would have generated.

An open-loop companion test schedules the production arrival distribution, reports intended, admitted, rejected, late, and completed operations, and bounds generator backlog. Together the tests describe both client-concurrency behavior and overload.

### Example 10

Four submission queues, buffers, and application threads are on NUMA node 0, while the device and completion vectors are on node 1. Profiling shows remote descriptor and payload traffic plus cache-line bouncing on a shared counter.

Moving the relevant queue, buffers, workers, and interrupt affinity together reduces p99. Moving only the submitting thread would not. The shared counter is sharded with periodic aggregation after its exactness requirements are reviewed.

## Cross-Program Connections

- **Performance engineering:** load generation, Little's Law, utilization, coordinated omission, percentiles, confidence, warmup, and experiment controls turn tuning into evidence.
- **Computer architecture:** cache lines, coherence, NUMA, interrupts, DMA, IOMMUs, PCIe, memory bandwidth, power, and thermal behavior bound the software path.
- **Data structures engineering:** rings, bounded queues, freelists, heaps, histograms, work stealing, and sequence numbers implement the hot path and lifecycle.
- **Database engineering:** buffer pools, WAL, group commit, checkpoints, compaction, read/write interference, and durable acknowledgement define semantic performance.
- **Distributed systems:** open-loop demand, admission, retries, idempotency, load shedding, tail amplification, quorum, and failover extend beyond one host.
- **Network engineering:** receive/transmit queues, interrupt moderation, polling, congestion, flow steering, batching, and zero-copy share the same design tensions.
- **Platform engineering:** SLOs, capacity reservations, topology inventory, safe tunables, canaries, rollback, pressure signals, and incident traces govern production changes.
- **API and service engineering:** bounded concurrency, cancellation, deadline propagation, overload responses, streaming, and idempotency expose I/O behavior at service boundaries.
- **Security engineering:** registered memory, shared rings, device passthrough, cross-tenant queues, timing interference, and privileged polling expand attack and isolation surfaces.
- **Systems engineering:** explicit boundaries, budgets, failure states, feedback stability, reserves, verification, and scoped assurance prevent local optimization from weakening the system.

## References

1. Linux Kernel Documentation, [Multi-Queue Block IO Queueing Mechanism](https://docs.kernel.org/block/blk-mq.html), software staging, hardware dispatch, merging, scheduling, tags, and resource handling; retrieved 2026-09-04.
2. Linux Kernel Documentation, [ABI stable symbols](https://docs.kernel.org/admin-guide/abi-stable.html), current stable sysfs interfaces for block-device queue capabilities, controls, statistics, and topology; retrieved 2026-09-04.
3. Linux Kernel Documentation, [Block layer statistics in `/sys/block/<dev>/stat`](https://docs.kernel.org/block/stat.html), in-flight work, merges, time, sectors, and flush counters; retrieved 2026-09-04.
4. Linux Kernel Documentation, [I/O statistics fields](https://docs.kernel.org/admin-guide/iostats.html), cumulative counter semantics, reset behavior, and device scope; retrieved 2026-09-04.
5. Linux Kernel Documentation, [PSI - Pressure Stall Information](https://docs.kernel.org/accounting/psi.html), system and cgroup I/O stall metrics and threshold triggers; retrieved 2026-09-04.
6. Linux Kernel Documentation, [The Linux Kernel Tracepoint API](https://docs.kernel.org/core-api/tracepoint.html), block request completion and error tracepoint interfaces; retrieved 2026-09-04.
7. Linux man-pages, [io_uring(7)](https://man7.org/linux/man-pages/man7/io_uring.7.html), shared submission and completion rings, ordering, batching, and application lifecycle; retrieved 2026-09-04.
8. Linux man-pages, [io_uring_setup(2)](https://man7.org/linux/man-pages/man2/io_uring_setup.2.html), ring setup flags, polling modes, sizing, restrictions, and errors; retrieved 2026-09-04.
9. fio project, [fio documentation](https://fio.readthedocs.io/en/master/fio_doc.html), workload controls, queue depth, rate, latency targets, percentiles, verification, and output; retrieved 2026-09-04.
10. Linux Kernel Documentation, [Block](https://docs.kernel.org/block/index.html), current block-layer documentation index for schedulers, polling, statistics, integrity, and testing; retrieved 2026-09-04.

## Exercises

### Exercise 1

A 4 KiB random-read service must sustain 150,000 requests per second, keep p99 below 800 microseconds, use no more than two CPU cores, and tolerate one path failure. Design the measurement boundary, budgets, queue topology, admission, completion mode, and recovery reserves.

### Exercise 2

At four operating points, measured tuples `(rate IOPS, mean latency microseconds, p99 microseconds)` are `(40,000, 150, 260)`, `(80,000, 220, 480)`, `(110,000, 500, 1,900)`, and `(112,000, 1,100, 8,000)`. Compute average in-system concurrency, identify the saturation knee, and choose a point for a 600-microsecond p99 SLO.

### Exercise 3

Design a batch and polling policy for traffic that alternates between sustained 200,000 IOPS bursts and 100 IOPS idle periods. Include count and time triggers, wakeup protocol, CPU budget, ordering boundaries, and observability.

### Exercise 4

A benchmark claims a zero-copy asynchronous path is three times faster than buffered synchronous I/O. Create a review checklist that determines whether the comparison is semantically fair and identifies where costs moved.

### Exercise 5

Design an overload and fault campaign for a multi-tenant storage path. Cover open-loop arrivals, fairness, retry storms, timeout races, reset at saturation, resource exhaustion, topology, telemetry, and the limits of the resulting claims.

## Answers to the Exercises

### Answer 1

Start latency when the service accepts an externally eligible request, before any admission wait, and end when the caller can consume a validated read result. Record nested timestamps for admission, software queue, block issue, device completion, completion processing, and caller wakeup. Define the request population, cache state, path, error treatment, and percentile window.

Allocate the 800-microsecond p99 budget, for example, across at most 100 microseconds admission and software wait, 500 microseconds path and device, 100 microseconds completion and wakeup, and 100 microseconds contingency. These are hypotheses to validate, not guaranteed constants. Use per-CPU or per-node software queues mapped to a bounded number of hardware queues, with buffers and completion vectors placed near the device. Begin with interrupts or hybrid polling because only two cores are available; dedicate busy polling only if measured benefit fits the CPU budget.

Apply per-tenant admission and a global concurrency ceiling selected below the measured tail cliff. Reserve tags, descriptors, buffers, and worker time for health, path transition, and in-flight resolution. On path failure, stop new issue to that path, preserve request ownership, classify uncertain completions, and fail over only idempotent or safely replayable reads. Measure the transition under 150,000-request-per-second open-loop demand and report rejects and late arrivals, not merely successful device completions.

### Answer 2

Using $N=\lambda W$ with microseconds converted to seconds gives average concurrency:

- $40{,}000\times150/1{,}000{,}000=6$;
- $80{,}000\times220/1{,}000{,}000=17.6$;
- $110{,}000\times500/1{,}000{,}000=55$;
- $112{,}000\times1100/1{,}000{,}000=123.2$.

Throughput rises substantially through 80,000 IOPS with p99 still below 600 microseconds. Moving to 110,000 gains 37.5 percent throughput but p99 rises almost fourfold and fails the SLO. From 110,000 to 112,000, throughput is nearly flat while latency and occupancy more than double. The knee lies between the second and third measurements.

Select 80,000 IOPS among the measured points because it is the highest one meeting the p99 target and has material headroom. Then sample intermediate rates to find a safe production point, repeat across duration and failures, and validate CPU and semantics. Little's Law corroborates occupancy growth but does not itself locate a percentile knee.

### Answer 3

Use a batcher that dispatches when either a count threshold is reached or the oldest request reaches a dwell threshold derived from its deadline. During 200,000-IOPS bursts, count-triggered batches amortize ring publication and doorbells. During 100-IOPS periods, the timer sends small batches promptly. Flush earlier for barriers, durable commits, tenant or protection changes, cancellation, and administrative commands.

Use interrupt completion while idle. During a sustained burst, enable bounded hybrid polling or route a dedicated queue to a polling worker if the measured latency reduction fits the CPU allocation. The submission-poll thread must observe its sleep flag; producers perform the documented wakeup when it sleeps. Require hysteresis and minimum residence time when switching modes so burst edges do not cause oscillation.

Record offered, admitted, batched, submitted, completed, rejected and late counts; batch-size and dwell histograms; poll and sleep time; wakeups; interrupts; CPU and energy; queue occupancy; p50 through extreme-tail latency; ordering and flush boundaries; and mode transitions. Test isolated requests immediately after the poller sleeps, bursts that end with partial batches, cancellation at dispatch, and device slowdown during a burst.

### Answer 4

First equalize operation sizes, offsets, read/write mix, dataset, working-set-to-cache ratio, run duration, warmup, concurrency, arrival process, filesystem and device, data verification, ordering, durability, error handling, and terminal completion definition. Determine whether buffered writes acknowledge from the page cache while the asynchronous path waits for device or durable completion. Verify direct and zero-copy claims from actual mappings and counters.

Account for application copies, kernel copies, page faults, pinning, registration, DMA mapping, IOMMU work, descriptor construction, system calls, ring synchronization, interrupts or polling, completion processing, scheduler wakeups, and cleanup. Include setup and teardown at the amortization horizon relevant to production. Measure CPU, memory bandwidth, cache misses, locked memory, queue occupancy, latency distributions, useful bandwidth, errors, retries, and recovery time.

Run cold, warm, read-hit, writeback, mixed-tenant, low-rate, high-rate, and long steady-state cases. Confirm the asynchronous generator does not use deeper concurrency while the synchronous baseline uses only one outstanding request unless that difference is the explicit subject. A valid conclusion may be that zero-copy improves one sustained large-transfer regime while buffered I/O wins reusable cached reads or low-duty workloads.

### Answer 5

Generate open-loop arrivals per tenant with recorded intended arrival times, realistic sizes and burst correlations. Bound the generator queue and report admission, rejection, lateness, completion, and lost-generator capacity. Combine latency-critical small requests with bandwidth-heavy large requests and background flush, checkpoint, discard, or repair. Assert per-class throughput floors, percentile and deadline targets, bounded queue memory, and starvation limits.

Inject transient errors, delayed completions, path loss, media errors, dropped interrupts where supported, and device reset while admitted load is at its ceiling. Force timeouts to race ordinary completion and cancellation. Verify one terminal result, retained buffer ownership until containment, bounded idempotent retry with jitter, and no retry bypass around admission. Exhaust ordinary tags, buffers, registered memory, worker slots, and queue entries while proving reserved control capacity remains usable.

Vary queue and interrupt affinity, NUMA placement, CPU pressure, memory pressure, device paths, scheduler, and stacked layers. Correlate application request IDs with admission, block issue and completion, retries, resets, pressure, interrupts, CPU placement, device health, and raw error codes. Preserve histograms, traces, configuration, firmware, kernel, topology, workload seed, and validation outcomes.

The campaign supports claims only for tested semantics, platforms, loads, durations, fault injections, and measurement accuracy. Synthetic error injection does not prove physical removal or firmware behavior. p99 does not establish p99.99. One topology does not establish all NUMA placements, and controlled overload does not prove safety against every correlated production failure.
