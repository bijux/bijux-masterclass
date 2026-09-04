---
module_id: OS-060
program: Operating Systems
level: 2
module_number: 60
title: Diagnosing Multiprocessor Kernel Contention
status: complete
last_verified: 2026-09-04
---

# Diagnosing Multiprocessor Kernel Contention

## One-Page Review

### Governing question

How should engineers locate, explain, and safely reduce multiprocessor kernel contention when many CPUs compete through locks, atomic cache lines, queues, interrupts, allocators, translations, and shared topology, while distinguishing causal serialization from ordinary saturation and measurement artifacts?

### Essential definitions

- **Contention** occurs when concurrent operations compete for a shared resource and at least one is delayed, retried, or denied.
- **Serialization** is enforced ordering through a resource or protocol; it can be necessary even when no measurable queue forms.
- **Saturation** occurs when admitted demand reaches effective service capacity; it need not involve a lock.
- **Wait time** is time from beginning an acquisition attempt until ownership or completion becomes available.
- **Hold time** is the interval during which one owner retains the protected resource.
- **Contention rate** is contended acquisitions divided by total acquisitions under a stated workload and observation method.
- **Lock convoy** is a sequence of waiters whose progress is dominated by serialized handoff, scheduling, or a delayed owner.
- **False sharing** is coherence interference between independent data that occupies the same cache line.
- **Off-CPU analysis** attributes blocked time to waits, wakeups, I/O, throttling, or scheduling rather than executing instructions.
- **Observer effect** is behavior changed by tracing, counters, logging, debug configuration, or sampling overhead.

### Central model, mechanism, or theorem

For operation `i`, decompose response time as `R_i=Q_i+W_i+H_i+X_i`, where `Q` is scheduling or admission delay, `W` is synchronization wait or retry time, `H` is serialized protected work, and `X` is remaining execution. Aggregate contention cost is not simply lock hold time: a short critical section can cause large wait through fan-in, owner preemption, cache-line transfer, interrupts, NUMA distance, or unfair handoff.

Diagnose through converging evidence: reproduce a service-level symptom; sweep concurrency; localize on-CPU and off-CPU cost; measure acquisition, wait, hold, retry, owner, queue, topology, and call-site distributions; form a falsifiable causal hypothesis; change one mechanism; and confirm both performance and protected invariants. A counter name or hot symbol alone is not a root cause.

### Critical invariants

- Every diagnosis begins with an application-visible symptom and workload boundary rather than a favored lock or tool.
- Wait, hold, acquisition, contention, retry, throughput, latency, CPU, and topology evidence share a synchronized interval and configuration.
- A lock dependency graph proves possible ordering hazards, not runtime contention magnitude.
- Instrumentation overhead, dropped records, sampling bias, enabled debug features, and clock semantics are recorded.
- Owner delay is separated from waiter spin or sleep so remediation targets the causal side.
- Cache-line contention is distinguished from logical lock contention and from unrelated data on the same line.
- A remediation preserves mutual exclusion, ordering, lifetime, visibility, fairness, bounded progress, interrupt, and hotplug invariants.
- Improvement is validated across load, core count, NUMA placement, workload phase, failure, and tail distributions.

### Common failures

Common mistakes are blaming the hottest lock without its wait distribution, treating 100 percent CPU as useful work, averaging only contended acquisitions and calling it per-operation cost, confusing lockdep warnings with a contention profile, enabling every tracer at once, ignoring dropped trace events, measuring a debug kernel and generalizing to production, shortening a critical section while owner preemption still dominates, replacing a lock with atomics that bounce one cache line, sharding without balancing skew, adding reader concurrency while starving writers, and celebrating throughput while tail latency, fairness, correctness, or recovery worsens.

### Compact example

A lock has 10,000 acquisitions, 2,500 contended acquisitions, 50 milliseconds of total waiter delay, and 20 milliseconds of total hold time. Contention rate is 25 percent, mean wait per contended acquisition is 20 microseconds, mean hold per acquisition is 2 microseconds, and the ratio is 10. That ratio suggests amplification worth investigating; it does not prove whether the cause is queue fan-in, preempted owners, topology, priority, or measurement bias.

### Connections

[OS-021](021-critical-sections-in-the-kernel.md), [OS-022](022-spinlocks-and-interrupt-context.md), [OS-051](051-per-cpu-state.md), [OS-053](053-scalable-locking.md), and [OS-059](059-tlb-shootdowns.md) connect diagnosis to protected invariants, execution context, partitioning, scalable mechanisms, and cross-CPU coordination.

## Governing Question

Multiprocessor slowdown rarely announces itself as “this lock is the cause.” It appears as throughput flattening, tail-latency spikes, idle CPUs beside queued work, excessive system time, cache misses, failed trylocks, blocked threads, interrupt delay, allocator stalls, or cross-CPU traffic. Several mechanisms can produce the same symptom.

The governing question is how to move from symptom to a causal serialization path with evidence strong enough to justify a correctness-sensitive change. The answer combines workload science, scheduler and locking semantics, cache and NUMA topology, trace integrity, and adversarial validation.

## Why This Matters

Kernel contention places a serial or coherence tax beneath every application sharing the affected path. Adding processors can make performance worse because more requesters increase queue length, cache-line ownership transfer, interprocessor interrupts, and scheduling disruption.

The tempting fixes are dangerous. Removing or narrowing a lock can violate lifetime, atomicity, interrupt exclusion, memory ordering, or device protocols. Replacing it with reader-biased synchronization can starve updates. Per-CPU state can make aggregation and hotplug incorrect.

Diagnosis itself can perturb the system. Function tracing, stack collection, lock debugging, console output, and high-rate events change timing and contention. Credible conclusions triangulate low-overhead counters, targeted traces, controlled reproductions, and a before-and-after service result.

## Prerequisites and Retrieval

Review [OS-014](014-context-switching.md), [OS-015](015-process-states-and-wait-queues.md), [OS-016](016-scheduling-objectives.md), [OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-021](021-critical-sections-in-the-kernel.md), [OS-022](022-spinlocks-and-interrupt-context.md), [OS-023](023-mutexes-semaphores-and-condition-variables.md), [OS-024](024-atomic-operations.md), [OS-025](025-deadlock-conditions-and-avoidance.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-057](057-load-balancing-across-cores.md), and [OS-059](059-tlb-shootdowns.md).

Retrieve these distinctions:

- on-CPU execution, runnable waiting, blocked waiting, interrupt time, and throttling are different delay categories;
- lock acquisition count, contention count, wait time, hold time, and retry count have different denominators;
- sleeping locks, spinning locks, reader-writer locks, sequence counters, RCU, atomics, and per-CPU state shift costs differently;
- logical resource contention and physical cache-line contention can exist independently;
- throughput scalability, fairness, average latency, and tail latency can disagree;
- lock correctness tools and runtime performance tools answer different questions;
- workload skew, topology, owner placement, priority, and interrupt state can dominate lock implementation;
- a performance change remains incomplete until protected invariants and failure paths are reverified.

## Learning Objectives

After this module, you should be able to:

1. distinguish contention, serialization, saturation, queueing, spinning, blocking, retrying, false sharing, and observer effects;
2. construct synchronized metrics for acquisitions, wait, hold, ownership, call sites, queues, CPUs, topology, and service outcomes;
3. combine scaling curves, profiles, off-CPU analysis, lock statistics, trace events, dependency checking, and torture tests appropriately;
4. trace owner and waiter delay through preemption, interrupts, NUMA, cache coherence, wakeups, handoff, and priority;
5. form and falsify hypotheses for locks, atomics, allocators, reference counts, scheduler queues, IPIs, RCU, and device paths;
6. select sharding, partitioning, batching, delegation, local aggregation, read-mostly, queue, or admission remedies;
7. validate performance, correctness, fairness, overload, hotplug, and lifecycle after remediation.

## Core Exposition

### Start from a symptom

State what failed: throughput stopped scaling, a percentile exceeded its objective, CPU cost rose per request, a deadline was missed, or recovery stalled. Name the workload, concurrency, topology, kernel, duration, and phase.

Without that boundary, diagnosis becomes a search for interesting counters. A lock can be highly contended yet irrelevant to the user-visible critical path, while a rare long hold can dominate tail latency.

### Contention versus saturation

Contention means competitors delay one another at shared state. Saturation means demand has consumed service capacity. A CPU-bound workload can saturate all cores with little synchronization, and a single lock can contend while overall CPU utilization remains low.

Test both. Compare admitted work with processor, device, memory, quota, and queue capacity, then attribute waiting to specific resources.

### Serialization versus waiting

A serialized critical section can have no observed wait at light load. It becomes a bottleneck when arrival rate and hold time produce overlapping demand.

The absence of contended acquisitions in one run does not prove scalability. Sweep concurrency and load until the intended operating envelope, including bursts and failure work, is represented.

### Build a scaling curve

Measure throughput and latency at one, two, four, and increasing processors or clients while holding offered work and configuration interpretable. Calculate speedup `S(n)=T(n)/T(1)` and efficiency `E(n)=S(n)/n`.

A falling efficiency curve localizes when coordination becomes important but not which resource causes it. Memory bandwidth, quotas, frequency, NUMA, devices, and load imbalance can produce the same shape.

### Demand versus achieved throughput

Closed-loop benchmarks can hide saturation because clients wait before issuing more work. Open-loop tests can expose queue growth but overload the system beyond meaningful service.

Record offered rate, admitted rate, completed rate, loss, queue depth, and latency. Distinguish a capacity limit from self-throttled demand.

### Response-time decomposition

Break an operation into admission or run-queue delay, synchronization wait, protected work, remaining execution, I/O, and completion. Use common trace identifiers and clocks so intervals can be joined.

Percentiles do not add algebraically without paired samples. Per-request traces establish whether long lock waits actually occur in the same requests as long service latency.

### On-CPU profiling

Sampling identifies instructions and call paths consuming CPU. Spin loops, atomic retry loops, cache-miss-heavy lock functions, interrupt handlers, and repeated scans can appear prominently.

An on-CPU profile misses sleeping wait. A hot unlock function can mean frequent harmless acquisitions, and a hot spin function can identify waiters while the causal owner runs elsewhere.

### Off-CPU analysis

Off-CPU analysis attributes time between descheduling and wakeup or resumed execution. It reveals mutex waits, completion waits, I/O, throttling, reclaim, and scheduler delay invisible to CPU samples.

Capture blocking call site, wait object identity where safe, waker, wakeup time, and scheduling delay. Being awakened is not the same as running.

### Acquisition metrics

Count total acquisitions, contended acquisitions, trylock failures, reader and writer modes, call sites, and CPUs. Rates need a common interval and workload denominator.

A contention percentage can rise while total cost falls if acquisitions become shorter or rarer. Pair counts with wait and service distributions.

### Wait-time metrics

Wait time measures the direct delay experienced before acquisition. Report total, mean per all acquisition, mean per contended acquisition, maximum, percentiles, and cumulative contribution by lock class and call site.

Means can hide rare convoys. Sampling long waits with owner state often yields more actionable evidence than recording every trivial acquisition.

### Hold-time metrics

Hold time starts when ownership becomes effective and ends at release. Long holds often indicate work that can move outside the critical section, but short holds can still contend at high fan-in.

Include interrupt-disabled and preemption-disabled duration when relevant. A lock holder delayed by an NMI, fault, nested lock, or higher-priority work can extend observed hold beyond its nominal instructions.

### Owner analysis

For a long wait, identify the owner, its CPU, call site, state, priority, preemption and interrupt context, nested locks, and topology. The waiter is where pain is visible; the owner path is often where cause lives.

Owner identity can change during queueing. Preserve generation or acquisition identifiers so a late sample is not attributed to the wrong holder.

### Spinlock contention

Spinlocks trade scheduling overhead for busy waiting and are suitable only for short non-sleeping critical sections under their context rules. Contended spinning consumes execution resources and coherence bandwidth.

Measure spin duration, queue position, owner execution, cache-line transfer, and whether the owner is runnable but preempted. More waiters do not make the protected operation faster.

### Sleeping-lock contention

Mutexes can block waiters and let other tasks use the CPU. Their cost includes queue management, descheduling, wakeup, handoff, and run-queue delay.

Short but contended mutex holds can suffer more from sleep and wake overhead than protected work. Adaptive spinning or optimistic paths shift that boundary and require workload validation.

### Owner preemption

A lock owner can be descheduled while waiters spin or sleep. Affinity, priority, quotas, oversubscription, interrupts, and CPU isolation affect how quickly it resumes.

Priority inheritance addresses defined inversion cases, not general overload. Diagnose scheduling state before rewriting the lock algorithm.

### Lock convoys

A convoy forms when many waiters serialize behind an owner and handoff overhead or scheduling sustains the queue. Bursty arrivals can leave a convoy long after the original long hold ends.

Observe queue length, arrival, handoff, wakeup, owner CPU, and drain rate. Reducing one exceptional hold, batching arrivals, or partitioning the resource can break different convoy causes.

### Reader-writer contention

Reader-writer locks improve concurrency only when readers overlap enough to repay more complex shared state. Cache-line updates to reader counts can bottleneck, and policy can starve readers or writers.

Report mode-specific wait and hold distributions plus starvation intervals. A high read ratio alone does not justify the mechanism.

### Sequence-counter retries

Sequence counters make readers retry when a writer overlaps. Readers do not block the writer, but long or frequent writes can cause unbounded reader work under unlucky timing.

Measure successful reads, retries, retry depth, writer duration, and preemption rules. Low lock wait can hide high retry CPU and latency.

### RCU contention

RCU removes conventional locking from read-side access but shifts work to updates, grace periods, callbacks, memory retention, and occasional reader restrictions.

Diagnose callback backlog, grace-period delay, CPU stalls, update serialization, barriers, and memory pressure. A stall warning is a symptom with several possible causes, not proof that RCU itself is defective.

### Atomic operations

An atomic instruction can serialize cache-line ownership even without a software lock. Shared reference counts, statistics, queue heads, state flags, and compare-exchange loops can become coherence hotspots.

Measure failed retries, line transfers, remote cache events, call sites, and update necessity. Replacing a lock with more atomic read-modify-write operations can worsen scaling.

### False sharing

Independent variables on one cache line can bounce between writers. No logical lock identity explains the delay, and each individual update may look cheap.

Map hot addresses to structure fields, allocation layout, CPUs, and ownership. Padding fixes a physical sharing problem but increases memory footprint and must respect ABI and cache-line variability.

### NUMA placement

A lock or shared counter homed on one node makes remote CPUs pay additional coherence and interconnect cost. Protected data can also be remote from the owner that acquires the lock.

Compare local and remote acquisition, hold, and access paths. Partitioning by node can reduce traffic and complicate global ordering and aggregation.

### Cache-line granularity

Logical locks, owner fields, queue nodes, statistics, and adjacent mutable data can share cache lines. Instrumentation counters added beside a lock can create the contention being measured.

Inspect layout in the measured build and separate read-mostly, owner-written, and waiter-written fields. Do not assume source declaration order equals final layout.

### Queue-lock behavior

Queued spinlocks direct each waiter toward bounded predecessor or queue state rather than one shared test-and-set line. This improves fairness and coherence behavior under contention.

Queue construction, unlock handoff, cancellation, virtualization, and NUMA still cost. Low contention can favor a simpler fast path, so inspect both regimes.

### Per-CPU state

Per-CPU counters and caches remove shared updates from the common path. Aggregation, limit enforcement, hotplug, draining, and memory overhead move elsewhere.

Use approximate reads where semantics permit or a versioned snapshot protocol where they do not. A global exact counter cannot be replaced by local estimates without revisiting its contract.

### Sharding

Shard a table, queue, allocator, or lock by a stable key so unrelated operations proceed independently. Choose shard count and mapping from concurrency, cache, NUMA, resize, and skew.

One hot key can retain the original bottleneck, while cross-shard operations need ordering or transactions. Measure distribution rather than assuming hash uniformity.

### Hierarchical aggregation

Aggregate first per CPU, cache group, or NUMA node, then combine at a slower global level. This bounds wide coherence traffic and matches topology.

Hierarchies add staleness and failure states. Define when local state becomes globally visible and how CPUs leaving the hierarchy drain ownership.

### Batching

Batching amortizes acquisition and shared-state updates across several operations. It can greatly improve throughput when work is abundant.

Larger batches increase individual wait, unfairness, memory retention, and cancellation complexity. Bound batch size by both throughput and latency objectives.

### Delegation

Delegation assigns one owner to mutate shared state while other CPUs submit requests. It converts lock competition into queueing and can improve cache locality.

The owner is a service center with finite capacity. Backpressure, fairness, failure, CPU placement, queue bounds, and synchronous completion semantics remain necessary.

### Optimistic techniques

Optimistic reads or updates proceed without exclusive ownership and validate a version before commit. They excel when conflicts are rare and retry work is cheap.

High conflict wastes work and can starve progress. Instrument validation failures, retries, discarded work, and fallback activation.

### Reduce critical-section scope

Move computation, allocation, formatting, copying, and I/O outside the lock when the protected snapshot and commit can be separated safely. Precompute before acquisition and publish a small change.

Do not move validation outside without rechecking under ownership. Shorter time is irrelevant if the operation becomes racy.

### Split locks by invariant

One lock often protects several fields because it began as a simple design. Split only after identifying independent invariants and operations.

Cross-invariant operations need ordering, combined acquisition, versioning, or transactions. Lock splitting can trade contention for deadlock and inconsistent snapshots.

### Data ownership redesign

The strongest fix can remove sharing: route each object to one CPU or shard owner, transfer immutable messages, and merge results asynchronously.

Ownership changes API semantics, failure recovery, memory placement, and balancing. Document migration and handoff before calling the structure contention-free.

### Interrupt and softirq contention

Interrupt handlers can contend on driver, queue, allocator, and networking state while delaying lock owners. Softirq processing can monopolize a CPU and alter scheduling evidence.

Correlate IRQ affinity, hardirq and softirq duration, queue identity, NAPI budget, application consumers, and lock events. Moving the application alone may increase cross-CPU sharing.

### Scheduler contention

Run queues, wakeup paths, load balancing, timers, and task state are shared at different topology scopes. Oversubscription and frequent wakeups can make scheduler locks and cache lines prominent.

Diagnose workload behavior, affinity, migrations, wakeup fan-out, and quotas before tuning scheduler internals. A hot scheduling symbol can be downstream of an application synchronization storm.

### Allocator contention

Allocators use per-CPU and per-node caches to reduce global coordination. Workloads that allocate across CPUs, free remotely, exhaust local caches, or trigger reclaim can reach slower shared paths.

Record object sizes, allocation and free CPUs, cache hit and refill, node, reclaim, compaction, and lock wait. Pooling can help and can retain excessive memory or break lifetime assumptions.

### Reference-count contention

A shared object's reference count can bounce on every lookup even when the payload is read-only. Batched, per-CPU, deferred, or ownership-based references reduce updates under suitable lifetime rules.

Overflow, resurrection, last-reference detection, weak references, and teardown are correctness boundaries. Never optimize reference traffic without a complete lifetime proof.

### TLB-shootdown contention

Mapping churn creates interprocessor interrupts, acknowledgement fan-out, and later refill cost. Shared address spaces with wide CPU residency amplify the path.

Join shootdown traces to the mapping producer and application phase. Reducing counted shootdowns through broader flushes can increase collateral cost.

### Lock statistics

Lock statistics summarize acquisitions, contention, wait and hold times by lock class and call site when the kernel is configured appropriately. They provide breadth before high-detail tracing.

Understand fields and denominators for the running version. Reset counters before a synchronized interval, preserve configuration, and account for instrumentation overhead.

### Event tracing

Static tracepoints expose stable event schemas for scheduling, locking, IRQ, workqueue, memory, and subsystem activity where available. Filters, triggers, histograms, and instances narrow collection.

Check buffer capacity and lost-event indicators. An incomplete trace cannot prove absence or preserve durations whose endpoints were dropped.

### Function tracing

Function and function-graph tracing reveal call paths and durations when no suitable event exists. Filtering to a narrow path reduces overhead and data volume.

Tracing every function on a contended production machine can change scheduling profoundly. Reproduce with and without instrumentation and prefer targeted triggers around the symptom.

### Histograms and triggers

In-kernel histograms aggregate high-rate fields without exporting every event. Synthetic events can join start and end points or trigger a detailed snapshot after an outlier.

Aggregation loses individual context and depends on correct keys. Validate clock, units, collisions, reset boundaries, and dropped or unmatched events.

### Lock dependency validation

Lockdep reasons about lock classes, acquisition ordering, interrupt contexts, and possible deadlocks. It is essential after changing synchronization structure.

It is not a production contention profiler. Debug tracking adds overhead, and a clean dependency graph says nothing about wait magnitude or scalability.

### Lock torture

Lock torture exercises primitives with configurable contender count and critical-region behavior. It validates progress and stress behavior under controlled synthetic contention.

It does not reproduce an application's ownership, data access, topology, interrupt, or phase distribution. Use it to complement workload-specific tests.

### Lockup and stall detectors

Soft and hard lockup watchdogs and RCU stall detectors identify CPUs that fail to schedule, respond, or pass quiescent states for long intervals. Their reports help localize catastrophic progress failures.

Slow consoles, tracing overhead, debugger stops, firmware, interrupts-disabled loops, preemption-disabled loops, and real contention can all trigger symptoms. Interpret the full context.

### Observer effect

Each tool has runtime and memory cost. Debug kernels can change structure layout, code generation, lock paths, timing, and scheduling.

Use a ladder: service metrics, low-overhead counters, sampling, targeted events, then short detailed traces. Calibrate overhead with a control run and preserve lost-data evidence.

### Form a causal hypothesis

A good hypothesis names the workload event, contender set, resource identity, owner path, delay mechanism, topology, and predicted observable change. For example: remote frees exhaust local caches, then all workers wait on a node allocator lock.

Try to falsify it by moving allocation ownership, removing skew, changing topology, or instrumenting the proposed chain. Correlation between a hot lock and bad latency is only the beginning.

### Validate remediation

Repeat identical load sweeps and adverse scenarios after one controlled change. Compare confidence intervals and distributions for service, waiting, holding, retries, CPU, coherence, memory, and fairness.

Re-run correctness, dependency, stress, hotplug, interrupt, cancellation, and teardown tests. Performance evidence never waives the invariant proof.

### Assurance

Retain workload generators, commands, kernel and debug configuration, topology, clock, raw counters, traces, losses, analysis code, hypotheses, rejected alternatives, patches, and rollback criteria.

Reviewers include synchronization, scheduler, architecture, NUMA, memory, device, tracing, performance, security, and subsystem owners. State which production workloads and hardware were not represented.

## Definitions and Notation

For operation `i`, let `Q_i` be scheduling or admission delay, `W_i` synchronization wait or retry time, `H_i` serialized hold time attributed to its service, and `X_i` other execution. The diagnostic decomposition `R_i=Q_i+W_i+H_i+X_i` requires paired timestamps; population percentiles cannot be summed as if they belonged to one request.

For lock `l`, let `A_l` be acquisitions, `C_l` contended acquisitions, `W_l` total measured wait, and `H_l` total measured hold. Contention rate is `C_l/A_l`; mean wait per contended acquisition is `W_l/C_l`; mean amortized wait is `W_l/A_l`; mean hold is `H_l/A_l`. State treatment of recursive, reader, failed, sampled, and incomplete events.

For throughput `T(n)` at concurrency or processor count `n`, speedup is `T(n)/T(1)` and efficiency is `T(n)/(n*T(1))`. A falling curve detects lost scaling but does not uniquely identify synchronization.

## Mechanisms, Invariants, or Proof Structure

1. **State the symptom.** Define service failure, workload, phase, topology, load, duration, and comparison baseline.
2. **Classify capacity.** Separate saturation, throttling, load imbalance, device limits, memory bandwidth, and synchronization.
3. **Build scaling evidence.** Sweep load and cores while collecting throughput, latency, fairness, CPU, queues, energy, and errors.
4. **Localize time.** Combine on-CPU sampling, off-CPU waits, scheduler delay, interrupts, faults, and application traces.
5. **Measure synchronization.** Capture acquisition, contention, retry, wait, hold, owner, call site, resource identity, and topology distributions.
6. **Control observation.** Record configuration, overhead, sample rate, filters, buffer loss, clock, debug effects, and missing data.
7. **Trace causality.** Connect workload event to waiter, owner, protected work, handoff, queue, cache line, memory and service result.
8. **Falsify alternatives.** Perturb skew, placement, priority, ownership, batch size, load, topology and instrumentation one at a time.
9. **Choose structural remedy.** Reduce sharing or frequency through ownership, sharding, locality, batching, delegation, or admission.
10. **Preserve correctness.** Re-prove exclusion, ordering, visibility, lifetime, fairness, progress, interrupt and lifecycle invariants.
11. **Repeat adversarially.** Validate idle through overload, tails, NUMA, hotplug, failure, recovery, cancellation and teardown.
12. **Retain evidence.** Preserve raw data, analysis, uncertainty, negative results, reviewers, limitations and rollback thresholds.

<!-- bijux-verify: {"id":"kernel-lock-contention-metrics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"acquisitions=10000\ncontention-rate=25.00%\nmean-wait-contended-us=20.00\nmean-wait-all-us=5.00\nmean-hold-us=2.00\nwait-to-hold-ratio=10.00\n","stderr":""}} -->
```python
acquisitions = 10_000
contended = 2_500
total_wait_ns = 50_000_000
total_hold_ns = 20_000_000

contention_rate = contended / acquisitions
mean_wait_contended_us = total_wait_ns / contended / 1_000
mean_wait_all_us = total_wait_ns / acquisitions / 1_000
mean_hold_us = total_hold_ns / acquisitions / 1_000
print(f"acquisitions={acquisitions}")
print(f"contention-rate={contention_rate:.2%}")
print(f"mean-wait-contended-us={mean_wait_contended_us:.2f}")
print(f"mean-wait-all-us={mean_wait_all_us:.2f}")
print(f"mean-hold-us={mean_hold_us:.2f}")
print(f"wait-to-hold-ratio={mean_wait_contended_us / mean_hold_us:.2f}")
```

The executable example checks denominators and units for aggregate counters. It does not sample a kernel, reconstruct distributions, identify an owner or call site, account for instrumentation, establish causality, or recommend a synchronization change.

## Alternatives and Trade-Offs

- Sampling has bounded overhead and misses sleeping time; tracing reconstructs sequences and can perturb them.
- Lock statistics give broad rankings but aggregate context; targeted event traces preserve call-site and owner relationships with more data.
- Function tracing reaches paths without tracepoints but changes execution more; static events expose fewer deliberate stable points.
- Spinlocks avoid sleep and wake overhead but burn CPU and coherence bandwidth; mutexes yield CPUs and add scheduler latency.
- Reader-writer locking permits parallel reads but updates shared reader state and can starve; an ordinary mutex has simpler fairness and ownership.
- Sequence reads avoid blocking but retry under writers; locked reads provide bounded single-attempt work and serialize.
- RCU makes reads inexpensive but delays reclamation and moves cost to updates and grace periods; direct locking gives immediate lifetime boundaries.
- Per-CPU state eliminates common shared updates but complicates exact aggregation and hotplug; global state is simple and contended.
- Sharding increases parallelism but suffers skew and cross-shard transactions; one lock preserves a simple atomic invariant.
- Batching amortizes ownership transfers but raises latency and unfairness; fine-grained service responds quickly and moves cache lines more often.
- Delegation localizes mutation but makes one owner a capacity bottleneck; direct locking distributes execution and shared ownership.
- Lock splitting reduces unrelated serialization but adds ordering and snapshot complexity; coarse locking simplifies proof and limits scale.
- Padding removes false sharing but expands memory and cache footprint; compact layout saves space and can couple writers physically.
- Affinity improves owner and memory locality but restricts balancing; migration absorbs skew and increases cache and NUMA movement.

## Failure Modes and Misconceptions

- **“The hottest lock is the root cause.”** Frequency, wait contribution, owner path and service correlation determine relevance.
- **“High CPU utilization proves useful work.”** Spinning, retries, interrupts and cache misses consume CPU.
- **“Low CPU utilization rules out contention.”** Sleeping waiters can leave processors idle.
- **“Contention percentage measures impact.”** Wait distribution and workload denominator are also required.
- **“Mean wait predicts tail latency.”** Convoys and rare owners can dominate extremes.
- **“A short critical section cannot bottleneck.”** High fan-in and coherence can amplify it.
- **“Lockdep is a contention profiler.”** It validates dependency rules and possible deadlocks.
- **“Lock torture reproduces production.”** It stresses primitives under synthetic behavior.
- **“An atomic removes serialization.”** Read-modify-write still owns a cache line exclusively.
- **“Padding fixes logical contention.”** It fixes only unwanted physical line sharing.
- **“Sharding guarantees scaling.”** Hot keys and cross-shard operations can retain bottlenecks.
- **“More readers justify a reader-writer lock.”** reader metadata and writer starvation can cost more.
- **“Fewer acquisitions means lower latency.”** Larger batches can increase waits and unfairness.
- **“A debug trace is passive truth.”** instrumentation changes timing and can lose events.
- **“Throughput improvement proves a safe fix.”** synchronization invariants and adverse lifecycle behavior still require proof.

## Worked Examples

### Example 1

Throughput flattens at eight workers while CPUs remain busy. Sampling shows atomic retry loops, and address-level evidence maps them to one global reference count rather than a lock.

### Example 2

A mutex's average hold is two microseconds but rare 20-millisecond holds coincide with allocation and reclaim. Moving allocation preparation outside ownership removes tail convoys.

### Example 3

Waiters spin on one socket while the owner is preempted on another by higher-priority work. Raising waiter aggressiveness worsens the symptom; scheduling and placement repair the owner delay.

### Example 4

Two independent per-CPU counters share a cache line because CPUs write adjacent array elements. Layout separation removes coherence traffic without changing logical locking.

### Example 5

A read-mostly table uses a reader-writer lock, but its reader count bounces globally and one writer starves. Versioned immutable publication improves both readers and update bounds.

### Example 6

A sharded allocator scales for uniform sizes but one object class maps all requests to one shard. Per-class evidence reveals skew and guides a better ownership map.

### Example 7

An RCU stall report occurs only with function tracing and a slow console. Control runs and lost-event accounting distinguish observer overload from the original workload.

### Example 8

A hot scheduler lock appears after thousands of workers wake simultaneously. Batching application notifications removes wakeup fan-out rather than modifying the scheduler lock.

### Example 9

Mapping churn triggers wide TLB shootdowns. Reusing stable virtual arenas reduces the producer rate and outperforms tuning the IPI acknowledgement path.

### Example 10

A per-CPU replacement removes a counter lock but loses exact limit enforcement during hotplug. A reserved local budget plus synchronized refill restores the invariant and retains common-path scale.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects cache coherence, line ownership, atomics, NUMA, memory bandwidth, interrupts, counters, and topology. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects mutual exclusion, queues, lock-free retries, RCU, sharding, work distribution, fairness, and progress.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects queueing, sharding, ownership, backpressure, skew, tail amplification, saturation, and causal tracing across service boundaries. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes causal hypotheses, hazard analysis, trade studies, lifecycle verification, and assurance. Within this program, [OS-053](053-scalable-locking.md) supplies mechanisms and [OS-057](057-load-balancing-across-cores.md) through [OS-059](059-tlb-shootdowns.md) supply multiprocessor causes.

## References

- Linux kernel documentation, [Lock Statistics](https://docs.kernel.org/locking/lockstat.html), current page checked 2026-09-04. Acquisition, contention, wait and hold metrics, call sites, configuration, reports and field interpretation.
- Linux kernel documentation, [Kernel Lock Torture Test Operation](https://docs.kernel.org/locking/locktorture.html), current page checked 2026-09-04. Synthetic contender and critical-region stress, primitive selection, parameters, output and failure interpretation.
- Linux kernel documentation, [Lockdep Design](https://docs.kernel.org/locking/lockdep-design.html), current page checked 2026-09-04. Lock classes, dependency chains, usage states, interrupt safety, validation and proof concepts.
- Linux kernel documentation, [Lesson 1: Spin Locks](https://docs.kernel.org/locking/spinlocks.html), current page checked 2026-09-04. SMP locking purpose, interrupt context, reader-writer variants, compiler behavior and design guidance.
- Linux kernel documentation, [ftrace](https://docs.kernel.org/trace/ftrace.html), current page checked 2026-09-04. Trace instances, buffers, filters, function and latency tracers, output, loss, clocks and control.
- Linux kernel documentation, [Event Tracing](https://docs.kernel.org/trace/events.html), current page checked 2026-09-04. Static events, formats, filters, triggers, PID selection, enablement and trace data.
- Linux kernel documentation, [Event Histograms](https://docs.kernel.org/trace/histogram.html), current page checked 2026-09-04. In-kernel aggregation, keys, values, synthetic events, variables, snapshots and latency analysis.
- Linux kernel documentation, [Softlockup and Hardlockup Detectors](https://docs.kernel.org/admin-guide/lockup-watchdogs.html), current page checked 2026-09-04. Watchdog semantics, thresholds, configuration, nohz behavior and diagnostic scope.
- Linux kernel documentation, [Using RCU's CPU Stall Detector](https://docs.kernel.org/RCU/stallwarn.html), current page checked 2026-09-04. Stall causes, warnings, timing, false positives, tracing and debugging effects.
- Linux kernel documentation, [Scheduler Statistics](https://docs.kernel.org/scheduler/sched-stats.html), current page checked 2026-09-04. Per-CPU runtime and wait, scheduling, wakeup, domain-balance, migration and versioned fields.

## Exercises

### Exercise 1

Design a diagnostic investigation for throughput flattening at 16 cores with high system CPU, occasional idle processors, and no obvious application lock.

### Exercise 2

Interpret a lock with high acquisition count, low contention rate, large total wait, short median hold, and rare extreme holds. Specify the next evidence required.

### Exercise 3

Compare sharding, per-CPU state, batching, delegation, RCU, sequence counters, reader-writer locks, and atomics for a read-mostly kernel registry with exact teardown.

### Exercise 4

Specify a targeted tracing plan that joins application latency, scheduler delay, lock wait, owner execution, IRQs, and cache-line topology while controlling observer effect.

### Exercise 5

Build a verification and assurance plan for replacing a global lock with NUMA-local shards. Include correctness, skew, fairness, overload, hotplug, failure, and rollback.

## Answers to the Exercises

### Answer 1

Define offered and achieved request rates, latency distribution, loss, workload phase, kernel, topology, affinity, quotas, devices and memory placement. Sweep clients and cores from one through saturation while recording user, system, interrupt, softirq, runnable, blocked, idle, throttled and stolen time. Compare per-request CPU cost and scaling efficiency; occasional idle CPUs prompt checks for affinity, pinned owners, NUMA, serial resources and load imbalance.

Begin with low-overhead CPU and hardware sampling for spin, atomic retry, scheduler, allocator, IRQ, page-table and cache-miss paths, plus off-CPU attribution for blocked waits and wakeup delay. Add lock statistics for a synchronized interval, then targeted events or function graphs around the highest wait-contribution paths. Join waiter to owner, address, call site, CPU, cache line, node, nested state and application request. Falsify device saturation, memory bandwidth, quota, wakeup storms and observer effects before modifying synchronization. Repeat one controlled remedy across the original sweep and validate invariants.

### Answer 2

High acquisition count with low contention can still create large aggregate delay if the path is ubiquitous. Large total wait with a short median hold suggests a heavy tail, convoy, owner preemption, interrupt or nested work, though denominator and instrumentation errors remain alternatives. Recompute total and mean wait per all and contended acquisition, percentiles and maximum using one interval; separate read and write modes and call sites.

Trigger a bounded trace on long waits that captures lock instance and class, waiter and owner identities, acquisition generation, owner CPU and topology, owner scheduling and interrupt state, nested locks, critical-section path, handoff, wakeup and subsequent run delay. Correlate these events with application outliers. Check trace loss and overhead against a control. If rare holds contain reclaim or allocation, move or precompute it experimentally; if owner preemption dominates, change placement or scheduling in a controlled falsification before redesigning the lock.

### Answer 3

Immutable-version publication with RCU can make lookups cheap while exact teardown waits for a grace period and reference or ownership boundaries; update frequency, callback backlog and retained memory must fit. Sequence counters suit small copyable snapshots but readers can retry under long writers and cannot safely retain pointers without a lifetime mechanism. Reader-writer locking gives straightforward mutable access but shared reader state and writer starvation may dominate.

Sharding by stable key reduces unrelated registry mutation and needs skew control plus ordered cross-shard teardown. Per-CPU caches accelerate repeated local lookup but exact global removal must invalidate or version every local reference and handle hotplug. Batching amortizes registrations or removals and adds visibility delay. Delegation centralizes mutation and makes its bounded queue and owner a service limit. Atomics help isolated fields but a global reference or version line can bounce. A sound design often combines immutable objects, sharded update ownership, RCU reads, and explicit synchronized teardown, validated under skew and failure.

### Answer 4

Instrument application request start and completion with a correlation identifier and one documented clock. Enable scheduler wakeup and switch events, narrow lock acquisition and release events or lock statistics, IRQ and softirq events for relevant vectors, and targeted function-graph tracing only around the suspected owner path. Record CPU, task, priority, lock identity, acquisition generation, call site, owner, wait and hold endpoints, run-queue delay, interrupt nesting and topology.

Use event filters, a separate trace instance, per-CPU buffers, stack sampling only on long waits, and histogram triggers that snapshot detailed tracing after a latency threshold. Size buffers, report overwritten or dropped records, bound capture duration, and avoid console streaming. Measure baseline workload with tracing off, counters only, target events, and detailed trigger separately. Join events offline and require temporal causality from request to waiter to owner delay to handoff to completion; unmatched endpoints remain missing evidence rather than zero duration.

### Answer 5

State the global lock's invariants: protected objects, atomic operations, ordering, lifetime, limits, interrupt contexts, fairness, progress, hotplug and teardown. Define shard ownership and mapping, per-shard invariants, cross-shard transaction order, global snapshot semantics, resize, node failure, CPU migration and draining. Prove each operation either touches one stable shard or acquires and validates multiple shards in a deadlock-free protocol; preserve references until all readers and in-flight operations quiesce.

Test uniform and adversarial hot-key distributions, cross-shard operations, node-local and remote callers, one through maximum cores, read and write phases, overload, allocation failure, owner preemption, interrupt entry, CPU and memory hotplug, shard resize, cancellation, recovery and teardown. Measure service distributions, throughput, fairness, per-shard wait and hold, retries, queue depth, cache and NUMA traffic, memory and energy. Run dependency and stress checks plus subsystem invariants. Rollback quiesces arrivals, drains and merges shards under a versioned boundary, republishes the global owner, waits for old references, and verifies counts and objects before freeing local state.
