---
module_id: OS-053
program: Operating Systems
level: 2
module_number: 53
title: Scalable Locking
status: complete
last_verified: 2026-09-04
---

# Scalable Locking

## One-Page Review

### Governing question

How can a kernel preserve synchronization invariants while preventing lock contention, cache-line movement, queueing, unfairness, and topology from collapsing throughput or tail latency as CPU count and workload concurrency grow?

### Essential definitions

- **Lock scalability** is how useful work, wait time, cache traffic, and latency change as participating CPUs and workload intensity increase.
- **Contention** occurs when concurrent operations compete for an incompatible ownership mode.
- **Critical-section demand** combines acquisition rate and hold time; it determines how much serialized service the lock must provide.
- A **coherence hotspot** is a cache line whose ownership or state changes frequently across processors.
- A **queueing lock** gives waiters explicit positions and typically lets each waiter spin on locally associated state rather than one shared word.
- **Optimistic spinning** waits briefly while the owner is running, then blocks when continued spinning is unlikely to help.
- **Sharding** partitions protected state and synchronization by a stable key, reducing conflicts at the cost of multi-shard operations.
- **admission control** bounds the number of contenders entering an expensive serialized or downstream region.
- A **scalability knee** is the load or CPU count beyond which added concurrency yields little work and sharply increases waiting or coherence cost.

### Central model, mechanism, or theorem

For lock class `L`, measure arrival rate `lambda`, mean hold time `H`, utilization `rho=lambda*H`, wait distribution `W`, and coherence cost `K`. As `rho` approaches one, queueing delay grows rapidly; cache-line handoff and owner descheduling can worsen the service time itself. A serial fraction `s` also bounds ideal speedup by `S(p) <= 1/(s+(1-s)/p)` for `p` processors.

Scalability comes first from reducing shared mutable work: shorten the region, move computation outside, partition ownership, batch transitions, use per-CPU or per-node state, or adopt a read-mostly versioned design. Queueing and optimistic lock algorithms improve admission and handoff behavior but cannot make inherently serialized work parallel. Every optimization must preserve the original invariant, ordering, lifetime, fairness, and context contract.

### Critical invariants

- Protected state and its linearization point remain identical or are deliberately respecified and verified after decomposition.
- No fast path bypasses permission, lifetime, ordering, accounting, or error transitions previously enforced under the lock.
- Shard selection is stable for the operation, and multi-shard work follows a cycle-free order or rollback protocol.
- Queue nodes and optimistic wait state remain alive through cancellation, timeout, preemption, handoff, and teardown.
- Reader optimization provides the promised snapshot and writer progress; it does not silently turn exact state into approximate observation.
- Fairness, priority, NUMA locality, and real-time bounds are explicit requirements rather than accidental benchmark outcomes.
- Measurements include useful throughput, wait and hold distributions, coherence traffic, CPU consumption, and correctness instrumentation.

### Common failures

Common mistakes are replacing one global lock with many locks while retaining one global cache-line counter, splitting a critical section without preserving its transaction, using try-lock failure as silent work loss, spinning when the owner is descheduled, assuming reader-writer locks scale with many readers despite shared reader-count writes, allowing unbounded reader starvation of writers, acquiring shards in input-dependent order, measuring only throughput at one CPU count, ignoring debug overhead or NUMA placement, and interpreting lower average latency as a bound on pathological waits.

### Compact example

If eight percent of execution remains serialized under one lock, ideal speedup is at most about 7.27 on 16 CPUs, 10.60 on 64 CPUs, and 12.5 even with infinitely many CPUs. Real lock handoff, coherence, scheduling, and imbalance lower those bounds. Optimizing code outside that serialized path cannot remove its ceiling; the design must reduce demand or partition the invariant.

### Connections

[OS-051](051-per-cpu-state.md) supplies sharded state and aggregation. [OS-052](052-smp-kernel-synchronization.md) supplies correctness, ordering, lifetime, and lock graphs. [OS-054](../ROADMAP.md) and [OS-055](../ROADMAP.md) extend read-mostly and NUMA-aware designs.

## Governing Question

A lock can be correct on two CPUs and unusable on 128. More callers increase not just waiting but cache-line transfers, atomic retry, scheduler interaction, wakeup storms, and cross-socket traffic. The owner can make slower progress because the lock word itself is under attack.

The governing question asks how to scale without weakening semantics. The answer begins with workload and invariant decomposition, then selects handoff, waiting, reader, sharding, and admission mechanisms based on measured conflict and topology.

## Why This Matters

Kernel hot locks limit scheduling, memory allocation, networking, filesystems, timers, and device queues. A single bottleneck can flatten total throughput while consuming every additional CPU in unsuccessful acquisition.

Latency matters alongside throughput. A design can increase aggregate work but starve a writer, delay a high-priority task, or make a rare cross-node acquisition take milliseconds. Production incidents often occur beyond the load used by average-case microbenchmarks.

Scalable locking also affects maintainability. Fine-grained schemes add state transitions, lock orders, retries, and reclamation. Optimization is durable only when the new proof and operational signals remain understandable.

## Prerequisites and Retrieval

Review [OS-019](019-fair-scheduling.md), [OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-021](021-critical-sections-in-the-kernel.md), [OS-022](022-spinlocks-and-interrupt-context.md), [OS-024](024-atomic-operations.md), [OS-025](025-deadlock-conditions-and-avoidance.md), [OS-051](051-per-cpu-state.md), and [OS-052](052-smp-kernel-synchronization.md).

Retrieve these distinctions:

- correctness, progress, fairness, and scalability are separate claims;
- lock hold time and arrival rate jointly determine serialized demand;
- cache coherence makes a small shared word globally expensive;
- spinning is useful only when expected residual hold time is short and the owner can run;
- more read concurrency does not help when readers update shared lock metadata;
- partitioning changes the protocol for cross-partition operations;
- averages conceal queueing tails and starvation;
- benchmark workload, topology, configuration, and instrumentation define the scope of evidence.

## Learning Objectives

After this module, you should be able to:

1. identify lock bottlenecks using demand, utilization, wait, hold, and coherence evidence;
2. distinguish test-and-set, queueing, ticket-like, optimistic spinning, sleeping, and hybrid behavior;
3. reduce contention through critical-section shortening, sharding, per-CPU state, batching, delegation, and admission control;
4. select reader-writer, per-CPU reader, sequence, immutable, or RCU designs from read and update semantics;
5. preserve atomicity, lock order, lifetime, fairness, priority, and hotplug across decomposition;
6. reason about NUMA placement, owner scheduling, wakeups, oversubscription, and real-time constraints;
7. design reproducible scalability experiments that retain correctness and raw evidence.

## Core Exposition

### Define scalability

State the objective: linear or bounded throughput growth, stable tail latency, bounded CPU overhead, writer progress, predictable real-time blocking, or efficient energy use. One design rarely optimizes all of them.

Normalize by useful completed operations, not attempted acquisitions. A lock that keeps all CPUs busy while little work completes is not scalable.

### Preserve the correctness baseline

Before optimization, document the protected invariant, fields, operations, linearization points, lock order, context constraints, memory ordering, lifetime, and recovery paths. Capture tests that distinguish every legal state transition.

This baseline prevents a faster implementation from achieving performance by dropping accounting, weakening snapshots, or moving errors outside the transaction.

### Measure demand

Lock demand is approximately acquisition rate times mean hold time, but distributions matter. A rare long holder creates a convoy even when the mean looks small.

Measure by lock class and call site: acquisitions, contentions, wait time, hold time, mode, CPU, owner state, and protected work. Relate those numbers to request throughput and phase.

### Queueing near saturation

As utilization approaches full serialized capacity, small increases in arrival rate produce disproportionate queueing. Bursts can reach saturation even when long-run utilization is moderate.

Backpressure before the knee can improve throughput and latency by avoiding useless contenders and downstream overload. More worker threads are not a universal cure.

### Coherence amplification

Simple test-and-set waiters repeatedly read or modify a shared lock word. Invalidations and failed atomic operations consume interconnect bandwidth and delay the owner.

Test-and-test-and-set reduces write attempts by reading while busy, but all waiters still observe the shared line. Backoff spaces attempts and trades handoff latency for less traffic.

### Queueing locks

A queueing lock gives each contender a node and predecessor relationship. Waiters spin on locally associated state, and unlock hands ownership to a successor.

This improves fairness and reduces one-line storms at scale. It adds queue-node lifetime, cancellation, preemption, and empty-to-nonempty race obligations.

### MCS-style local spinning

An MCS-style waiter enqueues a node and spins on a flag in that node. The predecessor performs a directed handoff, keeping most waiting traffic local.

Stack-allocated nodes must outlive acquisition and release, and one thread needs distinct nodes for independent nesting. Timeout or abort is substantially more complex than unconditional acquisition.

### Compact queued spin locks

A kernel can encode fast-path ownership and queue state compactly, using a direct atomic acquisition when uncontended and a queue under contention. Compactness reduces every embedded lock's footprint.

The slow path still requires fair-enough handoff, architecture ordering, pending-state transitions, and resilience to waiter preemption. Implementation detail does not change caller semantics.

### Ticket-like ordering

Ticket locks give waiters monotonically ordered positions, offering simple FIFO behavior. Every waiter polling a shared grant word can still receive each unlock invalidation.

They work well at modest scale and predictable short holds; deep queues, oversubscription, and NUMA can make strict order expensive.

### Optimistic mutex spinning

A sleeping mutex can spin briefly when its owner is currently executing, because release may occur before a block and wake cycle completes. An optimistic spinning queue limits which waiter competes.

Stop spinning when rescheduling is needed, the owner stops running, or policy predicts a long wait. Owner tracking and lifetime must remain safe during observation.

### Spin versus sleep threshold

Spinning costs CPU time `C_spin` for the remaining hold interval. Sleeping costs enqueue, context-switch, and wake latency `C_sleep`. A hybrid chooses spin when predicted `C_spin < C_sleep` under latency and priority constraints.

Predictions use owner-on-CPU state, recent hold distribution, queue depth, topology, and oversubscription. Fixed thresholds age poorly across hardware and workloads.

### Owner preemption and lock convoys

If a lock owner is descheduled, spinning waiters cannot make progress. Oversubscribed systems can waste entire quanta waiting for an off-CPU owner.

Sleeping, optimistic stop rules, priority inheritance, or scheduler-aware handoff mitigate this. Critical sections remain bounded and avoid faults or blocking operations.

### Shorten the critical section

Move parsing, allocation, copying, validation, and callbacks outside the lock while retaining references and revalidating state before commit. Precompute a candidate transition, lock briefly, verify generation, publish, and unlock.

This turns a long transaction into optimistic preparation plus a short linearization point. Failure and retry must not leak resources or duplicate effects.

### Reduce acquisition frequency

Batch several updates under one acquisition, accumulate per-CPU deltas, or hand work to an owner. The lock sees fewer arrivals, lowering `rho` even if hold time per acquisition grows.

Batch size trades throughput against latency, fairness, memory, and loss window. A batch must be bounded so one producer cannot monopolize the resource.

### Shard by stable key

Partition a table, queue, allocator, or counter by hash, device, CPU, node, tenant, or object identity. Independent operations then use different locks and cache lines.

Choose enough shards for conflict reduction without excessive memory or scan cost. Dynamic workload skew can place most demand on one shard despite a large nominal count.

### Cross-shard operations

Operations spanning shards acquire them in a canonical order, use try-lock and restart, employ a transaction context, or route through a coordinator. The design defines its atomic observation point.

Hash resizing and object migration must keep lookups correct across old and new ownership. Generation markers and deferred reclamation prevent stale-shard use.

### Wound-wait and wait-die

When callers discover an unpredictable set of objects, a fixed object-order acquisition may be unavailable. Transaction timestamps can force younger or older contenders to back off, release acquired locks, wait on the contended object, and retry.

The acquire context persists across retry to guarantee progress. Rollback must undo provisional state, and API misuse requires strong validation.

### Per-CPU and per-node state

Per-CPU updates eliminate shared lock acquisition on the hottest path; aggregation and exact limits become the expensive operations. Per-node state reduces cross-socket traffic while preserving more local sharing.

Hotplug drains or transfers shards, and remote writes follow compatible synchronization. [OS-051](051-per-cpu-state.md) develops these obligations.

### Delegation and combining

Contenders can enqueue operations for a lock owner or combiner, which applies several transitions during one ownership period. Delegation reduces handoffs and improves cache locality.

Each request needs lifetime, completion, cancellation, ordering, and error semantics. The combiner must yield or bound work so new callers and high-priority operations progress.

### Read-mostly immutable versions

Writers build a new immutable version and atomically publish its root. Readers avoid modifying shared reader-count state and can traverse without a traditional read lock under an appropriate lifetime protocol.

Copy cost, reclamation lag, stale-version memory, and writer serialization move off the read path. Exact multi-version semantics remain explicit.

### Sequence counters

Sequence counters give lockless retrying readers a consistent copy of small non-pointer data while serialized writers mark updates. They scale when writes are rare and reader retries remain bounded.

Long or preempted writers can make readers spin; frequent writers waste copied work. Reclaimable pointers need an independent lifetime mechanism.

### RCU

RCU read-side operations avoid a shared reader count in common configurations, letting readers scale while updaters publish replacements and defer reclamation through grace periods.

Writers still serialize conflicting changes. Memory footprint and callback backlog can grow when readers or CPUs delay grace periods. [OS-054](../ROADMAP.md) treats RCU in depth.

### Per-CPU reader-writer semaphores

A per-CPU reader-writer semaphore shifts reader bookkeeping away from one shared counter, often using RCU so read acquisition avoids atomic modification. Writer acquisition becomes much more expensive because it must exclude and wait for distributed readers.

This asymmetry fits overwhelmingly read-mostly control state with rare sleepable writes. It is unsuitable when writers need low predictable latency.

### Reader-writer fairness

Traditional reader-writer locks can scale poorly when all readers update one ownership word. Policies that admit new readers indefinitely can starve a queued writer.

Writer-pending gates bound starvation but can form read convoys. Evaluate read throughput, writer wait distribution, mode switching, and workload phases together.

### False sharing after lock removal

Removing a lock does not help if formerly protected counters remain packed into one cache line and different CPUs write them. Data layout is part of the synchronization design.

Align independently written hot fields or partition structures, then measure memory, TLB, and cache costs. Padding cold fields blindly wastes capacity.

### NUMA topology

A lock owner and protected data can reside on a remote node. Queue handoff across sockets, strict FIFO order, and centralized waiter structures create topology-dependent latency.

Per-node shards, hierarchical aggregation, cohort locks, or locality-aware handoff reduce remote traffic but can weaken global fairness. Remote starvation must remain bounded if required.

### Admission control

Limit concurrency before a serialized lock or downstream device rather than allowing thousands of waiters. A semaphore, token budget, queue, or worker pool can create controlled pressure.

Admission itself must not become the new hotspot. Hierarchical tokens and per-node queues distribute the decision while a global budget preserves capacity.

### Backoff

Backoff delays repeated acquisition attempts based on failure count, queue state, or randomness. It reduces synchronized storms and coherence traffic.

Excessive or unbounded backoff harms handoff latency and fairness. Randomized tests retain seeds, and production policy caps delay and responds to rescheduling.

### Try-lock and fallback

Try-lock supports opportunistic maintenance, deadlock avoidance, or a fallback path. Failure means contention, not permission to omit required correctness work.

Fallback may enqueue, defer, choose a slower shared structure, drop an explicitly lossy statistic, or restart from stable state. The contract labels which behavior is allowed.

### Fairness and priority

FIFO handoff bounds overtaking but may pass ownership to a descheduled or remote waiter. Opportunistic handoff improves locality and can starve unlucky contenders.

Real-time workloads require bounded priority inversion and compatible priority inheritance. Raw spinning regions and cross-lock chains receive worst-case rather than average analysis.

### Hotplug and teardown

Queue nodes, per-CPU shards, per-node locks, delegated requests, and optimistic owner references remain valid through CPU offline and subsystem removal. New admission stops before draining.

Offline transfers or completes locally owned work, and teardown waits for queued contenders, callbacks, readers, and retry paths before freeing lock-associated state.

### Instrumentation

Lock statistics track contention, wait and hold times, acquisition counts, bounce indicators, and contention call sites by lock class. Scheduler and hardware counters add owner runtime, migrations, cache misses, and interconnect traffic.

Instrumentation overhead can serialize hot paths and alter layout. Measure its cost, use sampling where appropriate, and reproduce findings with independent signals.

### Workload design

Vary CPU and thread count, read/write mix, shard skew, batch size, critical-section duration, memory pressure, interrupt load, oversubscription, priority, topology, and hotplug. Include realistic work outside the lock.

Report the saturation curve, not one favorable point. Find the knee and show throughput, useful CPU, tail latency, fairness, and error behavior beyond it.

### Correctness under optimization

Run lock dependency, race, memory, reference, and atomic-context checkers alongside stress. Inject allocation failure, cancellation, timeout, owner preemption, CPU offline, and teardown during deep queues.

Compare operation histories against the baseline state machine. A speedup with missing transitions or relaxed results is a correctness regression.

### Assurance

Retain source revision, configuration, topology, affinity, frequency policy, workload generator, seeds, raw lock statistics, performance counters, latency histograms, traces, checker outputs, and failures.

Assurance names subsystem, locking, scheduler, architecture, NUMA, real-time, performance, and independent reviewers. A synthetic microbenchmark does not certify production scalability.

## Definitions and Notation

For lock class `L`, let acquisition arrival rate be `lambda_L`, hold-time random variable `H_L`, utilization approximation `rho_L=lambda_L*E[H_L]`, and wait variable `W_L`. Queueing grows sharply as `rho_L` approaches one under ordinary stability assumptions.

Let serial fraction `s` yield ideal speedup bound `S(p)<=1/(s+(1-s)/p)` on `p` processors. This bound excludes coherence, scheduling, communication, imbalance, and added synchronization overhead, so measured speedup can be lower.

Let conflict probability under sharding be `P(key_a=key_b)` for independent operations `a` and `b`; skew makes it larger than the uniform `1/n` expectation for `n` shards.

Let lock strategy `Q=(admit,queue,wait,handoff,cancel)` specify admission, waiter placement, spin or sleep behavior, ownership transfer, and cancellation. Correctness also imports the protected invariant, memory ordering, context, lifetime, and lock-order graph from [OS-052](052-smp-kernel-synchronization.md).

## Mechanisms, Invariants, or Proof Structure

1. **Preserve semantics.** Record invariants, linearization, ordering, lifetime, errors, and progress before changing synchronization.
2. **Measure demand.** Attribute arrival, hold, wait, bounce, owner, call site, and workload phase to stable lock classes.
3. **Find the knee.** Sweep concurrency and topology beyond saturation while recording useful work, CPU cost, tails, and fairness.
4. **Remove protected work.** Precompute outside, retain references, lock for validation and commit, and retry without duplicate effects.
5. **Reduce arrivals.** Batch, delegate, cache, or accumulate locally while bounding latency, skew, and resources.
6. **Partition ownership.** Choose stable shards or nodes and define resizing, migration, and cross-shard atomicity.
7. **Choose waiting and handoff.** Match spinning, sleeping, optimistic, queued, fair, or locality-aware behavior to owner progress and context.
8. **Optimize readers deliberately.** Select reader-writer, sequence, immutable, per-CPU reader, or RCU semantics with writer and reclamation costs.
9. **Bound progress risks.** Cover owner preemption, starvation, priority inversion, oversubscription, cancellation, hotplug, and teardown.
10. **Verify data layout.** Remove hidden shared counters, false sharing, remote placement, and centralized admission hotspots.
11. **Reprove correctness.** Exercise every transition with dependency, race, memory, reference, and fault evidence.
12. **Retain reproducibility.** Preserve hardware, configuration, affinity, workload, raw observations, statistics, failures, and limitations.

<!-- bijux-verify: {"id":"serial-fraction-speedup-bound","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"cpus=1 upper-bound=1.00\ncpus=4 upper-bound=3.23\ncpus=16 upper-bound=7.27\ncpus=64 upper-bound=10.60\ninfinite-cpu-limit=12.50\n","stderr":""}} -->
```python
serial_fraction = 0.08

for cpu_count in (1, 4, 16, 64):
    bound = 1 / (serial_fraction + (1 - serial_fraction) / cpu_count)
    print(f"cpus={cpu_count} upper-bound={bound:.2f}")
print(f"infinite-cpu-limit={1 / serial_fraction:.2f}")
```

The executable example recomputes an ideal Amdahl-style bound for a fixed serial fraction. It does not measure locks or include coherence, queueing, scheduler, topology, imbalance, memory, I/O, correctness, or real-time effects.

## Alternatives and Trade-Offs

- Test-and-set locks are compact with strong uncontended paths but create shared-line traffic under contention; queueing locks add waiter state and localize spinning.
- FIFO handoff bounds overtaking but can choose a remote or descheduled successor; opportunistic handoff improves locality and weakens fairness.
- Spinning avoids sleep overhead for short active owners but wastes capacity for long or preempted owners; blocking saves CPU and adds wake latency.
- Fine-grained sharding increases parallelism but complicates scans, resizing, and multi-shard atomicity; coarse locks keep a simple transaction and cap concurrency.
- Large batches reduce acquisition frequency but raise per-item latency and monopolization; small batches track fairness and pay more handoffs.
- Per-CPU state gives nearly private writes but expensive aggregation; per-node state offers less isolation and cheaper global collection.
- Reader-writer locks give direct exclusion semantics but can bounce shared reader metadata; RCU or sequence readers move costs to writers, retry, and reclamation.
- Per-CPU reader semaphores make readers extremely cheap and writers extremely expensive; ordinary semaphores balance the modes more evenly.
- Admission control prevents contention collapse but can underutilize burst capacity; unrestricted entry responds quickly at low load and fails abruptly near saturation.
- NUMA-local handoff reduces interconnect traffic but can starve another node; global fairness improves equity and incurs remote transfers.
- Padding and alignment reduce false sharing but increase cache and TLB footprint; compact layout saves memory and can couple writers.
- Heavy instrumentation locates contention precisely but perturbs hot paths; sampling reduces overhead and loses event detail.

## Failure Modes and Misconceptions

- **“A faster lock makes serialized code scale.”** It reduces overhead but cannot remove the serial fraction.
- **“More shards always mean fewer conflicts.”** Skew, cross-shard work, scans, and memory can dominate.
- **“Removing the lock removes cache contention.”** Shared counters and false sharing can remain.
- **“Reader-writer locks make reads free.”** Shared reader bookkeeping can be a coherence hotspot.
- **“Spinning is faster than sleeping.”** Only when the owner can release before spin cost exceeds block and wake cost.
- **“FIFO is always best.”** It improves fairness and can harm locality or hand off to an off-CPU waiter.
- **“Try-lock failure permits dropping work.”** Only an explicitly lossy contract allows that fallback.
- **“Splitting a critical section preserves its transaction.”** Generation validation and commit semantics must be rederived.
- **“Canonical shard order is optional.”** Input-dependent order can introduce deadlock.
- **“Average wait demonstrates good latency.”** Maxima, percentiles, starvation, and priority blocking matter.
- **“One CPU-count benchmark proves scalability.”** A curve across the knee and topologies is required.
- **“Debug results equal production cost.”** Instrumentation changes timing, code, cache layout, and contention.
- **“Higher throughput proves correctness.”** Missing work can look faster.
- **“The fastest synthetic lock wins in production.”** Workload, context, topology, fairness, and lifecycle determine fit.

## Worked Examples

### Example 1

A global packet-statistics lock saturates at 16 CPUs. Per-CPU counters remove update contention; a periodic interval-labeled aggregate pays the scan cost.

### Example 2

Waiters on one test-and-set word generate a cache storm. A queueing lock directs each unlock to one successor and lets most waiters poll local nodes.

### Example 3

A mutex owner is running and normally releases in two microseconds. Optimistic spinning avoids a context switch, but stops immediately when the owner is descheduled.

### Example 4

Hash-table locks are sharded uniformly, yet one tenant supplies 80 percent of requests to one key. Hot-key isolation or semantic partitioning is needed beyond adding shards.

### Example 5

A transfer locks source and destination shards by numeric shard identifier. Concurrent reverse transfers follow the same order and cannot form a two-lock cycle.

### Example 6

GPU work discovers buffer locks in caller-controlled order. A wound-wait context backs off, releases provisional locks, waits on the contended buffer, and retries with the same age.

### Example 7

A read-mostly policy table replaces a shared-reader-count lock with immutable RCU versions. Readers scale, while writers serialize and wait for grace-period reclamation.

### Example 8

A per-CPU reader semaphore removes reader atomics but a configuration writer now waits for distributed readers. The design fits rare administrative updates, not latency-critical writes.

### Example 9

Per-node queues reduce remote lock traffic. A global fairness gate periodically admits an old request from another node so locality does not become starvation.

### Example 10

A benchmark gains throughput after batching but loses one percent of updates due to a broken retry path. State-machine counts expose the invalid speedup before performance is accepted.

## Cross-Program Connections

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects queueing locks, contention, work combining, sharding, lock-free reads, and progress. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects coherence protocols, interconnects, cache topology, atomics, NUMA, and SMT.

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects concurrent hash tables, partitioning, queues, immutable versions, resizing, and reclamation. [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) connects saturation, experimental design, observability, capacity, and tail latency.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies requirement preservation, trade studies, hazards, configuration matrices, evidence, and assurance. Within this program, [OS-054](../ROADMAP.md) deepens RCU, [OS-055](../ROADMAP.md) treats placement, and [OS-060](../ROADMAP.md) diagnoses multiprocessor contention.

## References

- Linux kernel documentation, [Generic Mutex Subsystem](https://docs.kernel.org/locking/mutex-design.html), current page checked 2026-09-04. Fast, optimistic-spin, and sleeping paths; owner state; waiter serialization; MCS-style queues; and semantics.
- Linux kernel documentation, [Percpu rw semaphores](https://docs.kernel.org/locking/percpu-rw-semaphore.html), current page checked 2026-09-04. Reader scalability, RCU-assisted acquisition, expensive writers, initialization, teardown, and API trade-offs.
- Linux kernel documentation, [Lock Statistics](https://docs.kernel.org/locking/lockstat.html), current page checked 2026-09-04. Contention, wait and hold distributions, acquisitions, cacheline bounces, call sites, configuration, and interpretation.
- Linux kernel documentation, [Kernel Lock Torture Test Operation](https://docs.kernel.org/locking/locktorture.html), current page checked 2026-09-04. Contention workloads, reader and writer stress, hold time, CPU hotplug, shutdown, statistics, and test controls.
- Linux kernel documentation, [Wound/Wait Deadlock-Proof Mutex Design](https://docs.kernel.org/locking/ww-mutex-design.html), current page checked 2026-09-04. Dynamic lock sets, acquire contexts, wound-wait and wait-die, rollback, slow paths, progress, and validation.
- Linux kernel documentation, [Lock types and their rules](https://docs.kernel.org/locking/locktypes.html), current page checked 2026-09-04. Sleeping, CPU-local, spinning, reader-writer, per-CPU reader, real-time, owner, nesting, and context rules.
- Linux kernel documentation, [Sequence counters and sequential locks](https://docs.kernel.org/locking/seqlock.html), current page checked 2026-09-04. Lockless reader retries, writer serialization, preemption, pointer limitations, latch variants, and associated locks.
- Linux kernel documentation, [A Tour Through RCU's Requirements](https://docs.kernel.org/RCU/Design/Requirements/Requirements.html), current page checked 2026-09-04. Reader scalability, locality, grace periods, memory ordering, CPU hotplug, real-time requirements, and counter bounds.
- Linux kernel documentation, [this_cpu operations](https://docs.kernel.org/core-api/this_cpu_ops.html), current page checked 2026-09-04. Per-CPU addressing, local updates, cache-line avoidance, remote-access restrictions, and aggregation trade-offs.
- Linux kernel documentation, [Linux kernel memory barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), current page checked 2026-09-04. Ordering, locks, atomics, acquire, release, architecture effects, cache coherence, and multicopy behavior.

## Exercises

### Exercise 1

Diagnose a global allocator lock that scales through eight CPUs and collapses by 32. Specify evidence, hypotheses, and experiments before redesign.

### Exercise 2

Redesign a locked hash table for skewed reads, writes, resize, and cross-key transactions. Preserve its linearization and lifetime contract.

### Exercise 3

Choose among a mutex, queueing spin lock, reader-writer lock, sequence counter, per-CPU reader semaphore, and RCU for three contrasting workloads.

### Exercise 4

Design a hybrid spin-and-sleep policy with fairness, owner-preemption, priority, NUMA, cancellation, and teardown behavior.

### Exercise 5

Build a correctness and scalability evaluation for a lock redesign. Include saturation, topology, real-time, hotplug, instrumentation, and reproducibility.

## Answers to the Exercises

### Answer 1

First preserve allocator invariants and record acquisition rate, hold-time distribution, wait distribution, contention sites, owner CPU and scheduling state, cacheline bounces, failed atomics, throughput, allocation latency, memory pressure, and NUMA placement while sweeping threads and CPUs past 32. Separate ordinary allocation, refill, drain, reclaim, and debug paths. Hypotheses include serialized capacity, long reclaim holders, lock-word coherence, owner preemption, false sharing, remote memory, and oversubscription.

Repeat with fixed affinity, one versus several sockets, controlled object sizes, pressure levels, critical-section instrumentation, and production-like debugging. If refill dominates, introduce bounded per-CPU magazines backed by per-node pools: reserve capacity globally, serve local operations without the global lock, exchange batches, and drain on pressure and hotplug. Keep the global path out of local allocation, eliminate adjacent shared counters, and prove that every object belongs to exactly one location and total reservations respect capacity. Re-run the full curve and failure suite; accept only if useful work and tails improve without leaks or missing accounting.

### Answer 2

Shard buckets by a stable hash and place shard locks and hot metadata on independent cache lines. Read and update of one key use one shard. Acquire two-key transactions in canonical shard order, deduplicate equal shards, and publish their joint state while both locks are held. For unpredictable key sets, consider a persistent wound-wait acquire context and complete rollback.

Resize builds a new table under a resize generation, migrates buckets or publishes an immutable root, and keeps old storage alive for readers. Operations either use the generation they validated or retry; they never search an already moved bucket without following the migration marker. Hot-key statistics detect skew, allowing isolated shards or semantic splitting without silently changing per-key serialization. RCU can protect read-mostly bucket versions while shard locks serialize writers. Tests cover duplicate keys, reverse transactions, resize overlap, deletion and reclamation, skew, allocation failure, cancellation, and teardown.

### Answer 3

For a process-context object with balanced short reads and writes and moderate contention, begin with a mutex or ordinary reader-writer semaphore only after measuring read concurrency benefit. For tiny non-sleeping critical sections with many contending CPUs, a queueing spin implementation can localize waiter traffic, provided owner preemption and interrupt context are bounded.

For small scalar snapshots with rare serialized writers and readers willing to retry, a sequence counter provides cheap reads but needs non-preempted writers and separate pointer lifetime. For an overwhelmingly read-mostly sleepable control gate with very rare writers, a per-CPU reader semaphore makes the deliberate reader/writer asymmetry explicit. For a pointer-based read-mostly structure whose readers may see an old or new immutable version, RCU gives scalable reads, separate writer locking, and deferred reclamation. The choice follows snapshot, context, update latency, reader progress, lifetime, memory, and real-time requirements rather than raw uncontended timing.

### Answer 4

Acquire atomically on the fast path. On contention, enqueue one waiter node with lifetime covering cancellation and handoff. Spin only while the owner identity is safely observed, the owner is running, no reschedule or higher-priority constraint applies, queue position permits competition, and a bounded time or iteration budget remains. Use recent hold distributions and topology as hints, never correctness inputs.

Otherwise mark the waiter sleepable and block without losing a directed wakeup. Unlock release-publishes protected state and hands off according to the documented fairness policy. A locality preference can bypass only within a bounded quota before the oldest or highest-priority eligible waiter wins. Cancellation atomically removes or transfers node responsibility; teardown stops admissions, wakes terminal failures, and drains every node. Real-time mode uses compatible priority inheritance or avoids unbounded spinning and bypass. Measure remote handoffs, owner-off-CPU episodes, spin waste, sleep transitions, fairness, priority blocking, and tails.

### Answer 5

Freeze the baseline invariant, transition model, lock graph, ordering, lifetime, context, errors, and progress requirements. Run dependency, race, memory, reference, and atomic-context checking; inject allocation failure, owner preemption, signals, cancellation, timeout, interrupt load, reclaim, CPU offline, and teardown. Compare completed histories and accounting against a model so missing work cannot appear as speed.

Sweep one CPU through beyond saturation; threads below, equal to, and above CPUs; one and multiple sockets; uniform and hot-key distributions; read/write phases; batch sizes; critical-section lengths; memory pressure; priorities; ordinary and real-time kernels; and CPU hotplug. Record throughput, useful CPU, acquisition and contention counts, hold and wait histograms, starvation, fairness, priority blocking, cache misses, line transfers, interconnect traffic, migrations, energy, and latency percentiles. Run with detailed instrumentation and lower-overhead independent counters, quantify perturbation, retain hardware and firmware, source and configuration, affinity and frequency policy, workload seeds, raw traces and statistics, failures, reviewer roles, and limitations.
