---
module_id: OS-051
program: Operating Systems
level: 2
module_number: 51
title: Per-CPU State
status: complete
last_verified: 2026-09-04
---

# Per-CPU State

## One-Page Review

### Governing question

When should kernel state be replicated per logical CPU, and what addressing, execution-context, aggregation, memory-ordering, hotplug, and teardown rules make that replication correct as well as fast?

### Essential definitions

- **Per-CPU state** gives each possible logical CPU a distinct instance of a variable or structure.
- A **per-CPU offset** identifies a variable within each CPU's area; combining it with a CPU-specific base yields an ordinary address.
- A **current-CPU operation** selects and accesses the executing CPU's instance as one protected primitive under its documented semantics.
- **CPU pinning** prevents a task from migrating while it retains a pointer or multi-operation relationship to the current CPU's state.
- **Local serialization** prevents conflicting contexts on one CPU from entering a protected region; it does not automatically exclude remote CPUs.
- A **remote access** reads or modifies another CPU's instance and therefore needs an explicit concurrency and cache-coherence contract.
- **Aggregation** combines shards into a system-wide view whose freshness and consistency depend on the read protocol.
- **CPU hotplug** moves a logical CPU through ordered preparation, startup, online, teardown, and dead states while resources and work are drained safely.

### Central model, mechanism, or theorem

Represent variable `x` as shards `x[c]` for each possible CPU `c`. A current-CPU operation computes `addr(x,c)=base[c]+offset(x)` and accesses that shard without a migration gap covered by the primitive. A multi-operation critical section must additionally pin execution or use a local lock whose contract remains valid for the kernel configuration and interrupt context.

Per-CPU partitioning removes inter-CPU write sharing only when ownership is local. It trades cheap updates for aggregation, memory footprint, skew, remote-access rules, and hotplug lifecycle. Exact global decisions usually require a stronger protocol than summing concurrently changing shards; approximate telemetry can accept bounded staleness and reap the scalability benefit.

### Critical invariants

- A retained current-CPU pointer is dereferenced only while execution remains pinned to the same CPU or the pointer is treated explicitly as a remote shard.
- Every writer context—task, soft interrupt, hard interrupt, NMI, remote CPU, or hotplug callback—is covered by the declared exclusion rule.
- Current-CPU read-modify-write guarantees are not promoted into cross-CPU atomicity or memory-ordering guarantees.
- Aggregation states whether it is approximate, generation-consistent, or exact and never uses an approximate sum for an exact safety limit.
- Offline drains or transfers timers, queues, counters, references, and callbacks before the shard becomes unavailable.
- Online publication occurs only after initialization, and failed startup rolls back already initialized instances in reverse-safe order.
- Layout keeps independently written shards and hot fields from producing unintended cache-line sharing.

### Common failures

Common mistakes are indexing by current CPU twice across a migration point, keeping a per-CPU pointer after re-enabling preemption, assuming interrupt disabling excludes remote CPUs, using an unprotected local update when interrupts can reenter it, mixing remote writes with non-atomic local read-modify-write operations, treating an aggregate as an instantaneous snapshot, iterating only online CPUs for storage allocated to possible CPUs, freeing offline state while deferred callbacks still reference it, and ignoring configuration changes such as fully preemptible real-time kernels.

### Compact example

Two CPUs update private request counters without contending on one global cache line: CPU 0 records three requests and CPU 1 records two. A telemetry reader sums the shards to five. That sum is exact only for the closed example; if updates continue during collection, it is a useful approximate observation unless a snapshot protocol freezes, sequences, or otherwise coordinates writers.

### Connections

[OS-013](013-threads-and-execution-contexts.md), [OS-014](014-context-switching.md), [OS-021](021-critical-sections-in-the-kernel.md), [OS-022](022-spinlocks-and-interrupt-context.md), and [OS-024](024-atomic-operations.md) establish execution, migration, locking, and atomicity. [OS-052](../ROADMAP.md) and [OS-053](../ROADMAP.md) extend the model to SMP synchronization and scalable locks.

## Governing Question

A global counter, queue, allocator cache, statistics block, or scratch buffer is simple to name but expensive to update from many CPUs. Every shared write can move cache-line ownership, serialize atomic instructions, and amplify contention.

Replicating state per CPU removes much of that sharing. It also creates new obligations: the current CPU can change, interrupt contexts can reenter local code, other CPUs can inspect shards, processors can go offline, and system-wide readers can observe shards at different moments. The governing question asks when the trade is valid and how to express every boundary explicitly.

## Why This Matters

Per-CPU state appears in schedulers, memory allocators, networking, tracing, interrupt accounting, timers, RCU, and device drivers. A mistake can corrupt a freelist, lose an event, strand work on an offline CPU, deadlock hotplug, or merely make a supposedly fast path slower through false sharing.

Performance gains can be dramatic because most updates remain in a CPU's nearby cache. Yet aggregate reads become more expensive, memory grows with the maximum supported CPU count, and large systems expose lifecycle cases that small fixed machines rarely exercise.

The abstraction also teaches a durable design lesson: sharding changes the consistency model. Engineers must specify who owns each shard, how migration changes ownership, and what a global observer is entitled to conclude.

## Prerequisites and Retrieval

Review [OS-007](007-kernel-data-structures.md), [OS-008](008-kernel-memory-allocation.md), [OS-013](013-threads-and-execution-contexts.md), [OS-014](014-context-switching.md), [OS-021](021-critical-sections-in-the-kernel.md), [OS-022](022-spinlocks-and-interrupt-context.md), [OS-023](023-mutexes-semaphores-and-condition-variables.md), and [OS-024](024-atomic-operations.md).

Retrieve these distinctions:

- logical CPU identity and task identity are independent;
- preemption can move a runnable task between CPUs even without simultaneous execution of that task;
- disabling local interrupts affects only the current CPU;
- atomicity of one operation does not establish ordering for surrounding memory;
- a reference protects lifetime only under its declared ownership protocol;
- cache-line ownership traffic can dominate arithmetic cost;
- possible, present, active, and online CPU sets answer different lifecycle questions;
- exact snapshots, monotonic bounds, and approximate telemetry need different algorithms.

## Learning Objectives

After this module, you should be able to:

1. explain static and dynamic per-CPU addressing using bases and offsets;
2. select current-CPU, pinned-pointer, raw, local-lock, atomic, or remote-access primitives from context;
3. enumerate task, soft-interrupt, hard-interrupt, NMI, and remote-writer concurrency;
4. design approximate and exact aggregation protocols without overstating snapshot meaning;
5. initialize, publish, drain, migrate, and destroy state through CPU hotplug and module teardown;
6. evaluate memory footprint, NUMA placement, false sharing, batching, and read-side cost;
7. test per-CPU state under migration, interrupt reentry, hotplug, memory pressure, and real-time configurations.

## Core Exposition

### Why partition by CPU

Per-CPU state works best for frequent updates whose meaning is naturally additive, batchable, or locally owned. Examples include event counts, allocator magazines, deferred-work lists, network statistics, and scratch storage.

It is a poor default for authoritative singleton state, rare updates with frequent exact reads, or objects whose ownership follows a task, device queue, NUMA node, or tenant more naturally than a CPU.

### Logical CPUs

A logical CPU is the scheduler and kernel execution unit identified by a CPU number. Simultaneous multithreading siblings are separate logical CPUs even when they share core resources.

CPU numbers index topology and per-CPU instances, but lifecycle masks determine whether an instance is possible, physically present, online, or active for scheduling. Code selects the mask that matches allocation and operation semantics.

### Static per-CPU variables

Statically declared per-CPU variables reserve one logical object whose linker and boot machinery instantiate storage for each possible CPU. The apparent variable is not an ordinary single address.

Static allocation is efficient and available early, but its footprint multiplies by the supported possible-CPU count. Large structures need explicit memory-budget review.

### Dynamic per-CPU allocation

Dynamic allocation creates a per-CPU object at runtime and returns a typed per-CPU reference or offset. The allocator arranges one instance per required CPU area and supplies alignment.

Failure is handled before publication. Teardown must prevent new access, drain users, release per-CPU contents that own resources, and only then free the allocation.

### Base-plus-offset addressing

Conceptually, `addr(x,c)=base[c]+offset(x)`. The offset is common across instances; the base selects one CPU's per-CPU region. Architectures can keep the current base in a segment, dedicated register, or another optimized mechanism.

Treating a per-CPU offset as an ordinary pointer bypasses the selection step. APIs preserve address-space intent and make current versus explicit CPU access visible.

### Current-CPU operations

Current-CPU operations combine selection and access so migration cannot occur between separately computing the CPU and modifying its instance. Architectures can implement simple updates with compact instructions and no globally locked cache-line operation.

The guarantee is specific. It can ensure one update lands wholly on one current shard, while the task may migrate immediately before or after. That is adequate for an aggregate event counter and inadequate for a multi-step relationship that must stay on one CPU.

### Retaining a current pointer

Obtaining a pointer and using it across several instructions requires the execution context to remain on that CPU. Pinning, preemption disabling, or a suitable local lock establishes that condition under its API.

The pointer normally becomes invalid as a current-CPU pointer once the region ends. It may still designate some CPU's allocated memory, but using it then is remote access with a different synchronization contract.

### Raw operations

Raw per-CPU operations omit protections or checks provided by current-CPU forms. They are appropriate only when the caller already proves a stable CPU and correct context.

Using a raw operation merely because it benchmarks faster moves proof obligations to every caller. The interface should encode those preconditions and allow debugging tools to check them.

### Preemption control

Disabling preemption prevents task migration and involuntary scheduling for the bounded region. It is CPU-local execution control, not mutual exclusion against interrupts or other CPUs.

Long regions harm latency, and sleeping while preemption is disabled violates context rules. Prefer a single current-CPU primitive or a scoped local abstraction when possible.

### Interrupt contexts

Hard interrupts, soft interrupts, and nonmaskable interrupts can access state while task code is interrupted. Each shared field needs an explicit writer-context inventory.

Disabling preemption alone cannot exclude an interrupt. Disabling local hard interrupts does not necessarily exclude NMI or remote access. The narrowest correct primitive follows the actual contexts.

### Local locks

A local lock names and documents protection of per-CPU data. On configurations where it maps to preemption or interrupt control it can carry little runtime cost; on fully preemptible real-time kernels it can become a real per-CPU lock.

This abstraction preserves intent across configurations better than relying on incidental side effects of another lock. Its scope, nesting, interrupt variant, and sleepability remain explicit.

### Local atomic operations

Some local or current-CPU read-modify-write operations are atomic with respect to execution contexts on the owning CPU under their contract. They can avoid the cache-coherence cost of a globally atomic instruction.

They are not safe against arbitrary remote writes. Mixing a local non-locked increment with a remote update can lose one modification even if each looks indivisible locally.

### Remote reads

A reader can iterate explicit CPU instances to aggregate statistics. It must stabilize the set of CPUs and ensure each shard's storage remains alive during traversal.

Individual reads can use atomic, sequence, or lock protocols when fields span multiple words or must be mutually consistent. A read-only remote access still incurs cache and topology costs and can race local writers semantically.

### Remote writes

Remote writes are exceptional because they defeat local ownership and can invalidate assumptions behind cheap current-CPU updates. Prefer sending work to the owning CPU, publishing a global command, or using a truly shared atomic object when semantics demand cross-CPU modification.

If remote writes are required, all local and remote operations use one compatible atomic or locking protocol. Documentation names the owner transfer and memory-ordering edges.

### Memory ordering

Per-CPU placement changes address selection, not the architecture's memory model. A local counter increment does not automatically publish another object to a remote observer.

Producer-consumer relationships use release, acquire, barriers, locks, or RCU as required. The proof distinguishes atomicity of the shard update from ordering of payload, flags, queue links, and aggregate reads.

### Counters and approximate aggregation

For telemetry, each CPU can increment its own shard and a reader can sum all online or possible shards. If writers continue, the result combines values from different instants.

This approximate sum is often appropriate for metrics. It must not be advertised as a linearizable total or used to enforce a hard global quota without conservative bounds.

### Exact aggregation

An exact snapshot can stop or coordinate writers, collect shards under a global generation, use per-shard sequence validation, or transfer counts into an atomic global epoch. Each method imposes update or read cost.

Define exactness: one linearization instant, membership in a closed interval, no lost increments across epoch rotation, or monotonic lower bound. “Accurate” is too vague to review.

### Thresholds and batching

A common design lets each CPU accumulate a local delta and periodically fold it into a global atomic count. This reduces shared updates while bounding global staleness by the sum of local thresholds.

Safety limits reserve distributed slack before local spending. If a hard capacity is `K`, unconstrained local caches cannot each assume all remaining capacity.

### Per-CPU queues

Locally produced work can enter a per-CPU queue with minimal contention and be consumed on that CPU. Migration of producers is harmless only if enqueue selection and update form one protected operation.

Load imbalance, CPU isolation, and offline require stealing, redirection, or draining. Queue entries retain their referenced objects until execution or cancellation reaches a terminal state.

### Allocator caches

Per-CPU magazines satisfy common allocations without a global lock. Refill and drain exchange batches with node or global pools, amortizing synchronization.

Memory accounting includes objects hidden in local caches. Shrinkers, hotplug, and memory pressure need bounded drain paths that do not recurse into the allocator unsafely.

### Cache-line layout

Separate CPU areas usually prevent different CPUs' corresponding variables from sharing physical cache lines, but packing and allocator layout must be verified. Within one area, interrupt and task fields can still interfere.

Alignment reduces false sharing and increases memory. Group fields by joint access pattern, measure coherence traffic, and avoid padding every field without evidence.

### NUMA placement

Per-CPU areas should be placed near their CPUs when topology and allocator support permit. Local updates then use nearby memory; aggregation crosses nodes and can become expensive.

CPU hot-add or topology constraints can produce fallback placement. Observability records actual node placement rather than assuming CPU number implies locality.

### Boot initialization

Early boot establishes possible CPU masks and per-CPU areas before ordinary allocators and scheduling are fully available. Boot CPU access may use special initialization rules.

Secondary CPUs receive initialized architectural and subsystem state in ordered startup callbacks. No callback consumes a shard before its prerequisites are published.

### CPU hotplug state machine

CPU hotplug uses ordered states so subsystems start and stop in dependency order. Preparation can allocate resources in sleepable context; starting configures CPU-local state; online makes service available.

Teardown reverses dependencies. Callback registration and CPU transitions are serialized, and failure invokes rollback for instances already advanced.

### Online initialization

Allocate or validate the shard, initialize locks, counters, queues, timers, and private resources, then publish readiness with required ordering. Route interrupts or work only after the consumer is ready.

Repeated online cycles must not leak resources or reuse stale generation state. Initialization distinguishes first presence from re-online after a prior drain.

### Offline drain

Stop new work targeting the CPU, migrate interrupts and runnable work, cancel or move timers, drain queues and allocator caches, fold counters, wait for callbacks, and mark the shard unavailable in dependency order.

Offline completion means no forbidden future access remains. Merely clearing the online mask does not cancel references already captured by remote readers or deferred work.

### Possible versus online iteration

Static per-CPU storage is often sized for possible CPUs so future online events need no structural reallocation. Initialization and destruction may therefore iterate possible CPUs; active service and work routing usually iterate an online or active mask.

Choosing the wrong mask can leak never-online resources, omit offline accumulated counters, or send work to a CPU that cannot execute it.

### Module and subsystem teardown

Teardown removes hotplug callbacks in the correct API order, blocks new entry, drains current and offline instances, waits for RCU or deferred callbacks, releases owned resources, and frees dynamic per-CPU memory last.

Rollback paths receive equal testing. Partial registration across existing online CPUs can fail and must undo only the instances successfully initialized.

### Observability

Expose CPU identity, lifecycle generation, shard value or queue depth, aggregation method, timestamp interval, missed or retried samples, remote access, allocation node, and hotplug transition.

Readers avoid causing the contention they measure. Sampling every shard too frequently can turn private cache lines into shared read traffic and disturb isolated CPUs.

### Testing and assurance

Force migration between selection and access in deliberately unsafe test variants, interrupt local critical sections, issue remote reads and writes, and online and offline CPUs while queues, timers, and callbacks are active. Test one CPU, sparse CPU IDs, maximum possible counts, and repeated cycles.

Run ordinary preemption, full preemption, real-time, lock debugging, race detection, memory sanitizers, and weak-memory architectures where applicable. Measure cache misses, line transfers, hotplug latency, aggregate error, memory footprint, and tail latency separately from correctness.

Assurance names scheduler, interrupt, hotplug, memory-management, architecture, real-time, RCU, performance, and independent reviewers. A correct sum in a sequential simulation is not evidence of migration or interrupt safety.

## Definitions and Notation

Let `C_possible`, `C_present`, `C_online`, and `C_active` be CPU sets with platform-defined lifecycle relations. Let per-CPU object `X={x_c | c in C_possible}` and `addr(X,c)=base_c+offset_X`.

Let execution context `E=(c,kind,p,m,g)` contain current CPU `c`, context kind `kind` in `{task,softirq,hardirq,nmi,hotplug}`, preemption state `p`, migration state `m`, and lifecycle generation `g`.

Let local update `U_c` be permitted only if its primitive covers every competing context for `x_c`. Let remote operation `R_{d,c}` mean CPU `d` accesses shard `c`; it is correct only under a protocol compatible with local operations.

Let aggregate observations occur at times `t_c`, giving `S=sum x_c(t_c)`. This is a linearizable snapshot only if the collection protocol proves an instant `t*` such that `S=sum x_c(t*)`; otherwise its documented approximation or bound applies.

## Mechanisms, Invariants, or Proof Structure

1. **Choose the owner.** Prove that CPU sharding matches update locality better than task, queue, node, or global ownership.
2. **Define lifecycle sets.** State whether allocation, initialization, routing, aggregation, and destruction use possible, present, online, or active CPUs.
3. **Declare contexts.** Enumerate task, softirq, hardirq, NMI, remote, and hotplug access for every field.
4. **Select access primitives.** Use current-CPU operations, pinning, local locks, atomic operations, or shared locks whose guarantees cover those contexts.
5. **Order related memory.** Add explicit publication and consumption edges for payload, flags, queues, generations, and references.
6. **Specify aggregation.** Label views approximate, bounded, epoch-consistent, or linearizable and match them to decisions.
7. **Control remote access.** Prefer owner-CPU execution; otherwise make local and remote operations use one compatible protocol.
8. **Publish after initialization.** Make a shard routable only after all dependencies and generation state are visible.
9. **Drain before offline.** Redirect new work, finish or transfer old work, fold resources, and wait for retained users.
10. **Destroy after quiescence.** Remove callbacks, exclude new references, wait for deferred access, and free last.
11. **Measure the trade.** Record memory, cache traffic, update and aggregate cost, skew, hotplug latency, and real-time effects.
12. **Preserve evidence.** Retain topology, configurations, CPU masks, seeds, traces, sanitizer results, performance counters, and limitations.

<!-- bijux-verify: {"id":"per-cpu-counter-aggregation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"cpu=0 requests=3\ncpu=1 requests=2\naggregate=5\nshards-independent=True\n","stderr":""}} -->
```python
requests = {0: 0, 1: 0}

for cpu in (0, 0, 1, 0, 1):
    requests[cpu] += 1

for cpu in sorted(requests):
    print(f"cpu={cpu} requests={requests[cpu]}")
print(f"aggregate={sum(requests.values())}")
print(f"shards-independent={set(requests) == {0, 1}}")
```

The example demonstrates deterministic sharded counting and aggregation only. Its final independence line reflects distinct dictionary keys, not memory addresses or cache lines. It models no migration, parallel execution, atomics, interrupts, ordering, hotplug, NUMA placement, or kernel API.

## Alternatives and Trade-Offs

- One global atomic counter gives simple reads but contended updates; per-CPU counters reverse that cost profile.
- Current-CPU single operations minimize critical sections but express only local updates; pinned pointers support compound work and increase latency risk.
- Local locks document scope and adapt across configurations but can cost more on real-time kernels; raw preemption control is compact and easier to misuse.
- Owner-CPU message passing preserves local invariants but adds queueing latency; remote atomics act immediately and reintroduce coherence traffic.
- Approximate aggregation is cheap enough for telemetry but unsuitable for exact quotas; coordinated snapshots give precision at synchronization cost.
- Large local batches amortize global synchronization but increase skew and stranded resources; small batches track totals more closely.
- Allocating for possible CPUs simplifies hot-add but multiplies memory by the supported maximum; on-demand allocation complicates lifecycle and failure.
- Cache-line padding reduces false sharing but increases footprint and TLB pressure; dense packing saves memory and can couple writers.
- Per-CPU placement maximizes update locality but makes global scans NUMA-expensive; per-node state offers an intermediate granularity.
- Retaining offline shards preserves counters and stable indexing but consumes resources; folding and freeing reduces footprint and complicates generations.
- Strict hotplug serialization simplifies teardown proofs but extends transition latency; asynchronous drain improves responsiveness and requires retained state.
- Frequent observability gives fresh shard detail but perturbs caches and isolated CPUs; sampled aggregation lowers overhead and freshness.

## Failure Modes and Misconceptions

- **“Per-CPU means race free.”** Same-CPU interrupt reentry and remote access can still conflict.
- **“Reading the CPU number pins execution.”** Migration can occur before the later access.
- **“A current-CPU pointer remains current.”** It is current only within the pinning or local-lock scope.
- **“Disabling preemption excludes interrupts.”** It prevents task migration, not all local reentry.
- **“Disabling local interrupts excludes other CPUs.”** It is not inter-CPU mutual exclusion.
- **“A local atomic is globally atomic.”** Remote operations need a compatible protocol.
- **“Current-CPU operations order other memory.”** Publication needs explicit memory-ordering primitives.
- **“Summing shards yields an instantaneous total.”** Concurrent collection usually samples different times.
- **“Online CPUs define allocated storage.”** Possible CPUs often determine static capacity.
- **“Offline makes references disappear.”** Queued, remote, and deferred users must drain.
- **“CPU numbers imply NUMA locality.”** Actual allocation placement and topology must be inspected.
- **“Padding always improves performance.”** It trades coherence against memory and cache footprint.
- **“Non-real-time locking assumptions transfer to real-time kernels.”** Primitive behavior and context constraints can differ.
- **“A sequential shard test proves scalability.”** It exercises neither coherence nor concurrency.

## Worked Examples

### Example 1

A network receive path increments a current-CPU packet counter once per packet. A monitoring reader periodically sums shards and labels the result interval-based rather than instantaneous.

### Example 2

Task code obtains a pointer to CPU 2's allocator cache, is preempted and resumes on CPU 5, then mutates the old pointer. Pinning around pointer lifetime prevents this unintended remote write.

### Example 3

A task and hard interrupt both update a two-field local structure. Preemption disabling alone is insufficient; the design uses the matching interrupt-safe local protection and a sequence for readers.

### Example 4

A remote CPU resets a shard while its owner performs an unlocked local increment. One update can be lost, so reset becomes an owner-CPU command or both paths adopt a compatible atomic exchange protocol.

### Example 5

Each CPU accumulates at most 31 events before folding to a global value. With eight active shards, the global value can lag by at most 248 under the stated flush rule.

### Example 6

A hard global capacity of 100 cannot be handed independently to four caches as 100 each. The refill path reserves disjoint batches from a shared authoritative budget.

### Example 7

During CPU offline, a per-CPU work queue rejects new routing, transfers queued items, waits for an executing callback, folds statistics, then releases private storage.

### Example 8

A hotplug startup callback fails on CPU 6 after CPUs 0 through 5 initialized. The registration path invokes teardown for successful instances and publishes no partially registered service.

### Example 9

Two hot counters within adjacent CPU areas unexpectedly share a physical line because of layout. Alignment removes coherence bouncing but increases the allocation enough to require a footprint check.

### Example 10

A metrics collector scans 512 CPUs every millisecond and becomes the dominant remote reader. Hierarchical per-node aggregation reduces cross-socket traffic while preserving the required reporting interval.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects cache coherence, memory ordering, logical processors, NUMA, interrupts, and atomic instructions. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects sharding, local ownership, work queues, barriers, and snapshots.

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects distributed counters, queues, allocator caches, sequence counters, and aggregation. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects lifecycle states, rollback, resource accounting, configuration variants, fault injection, and evidence.

Within this program, [OS-052](../ROADMAP.md) expands SMP synchronization, [OS-054](../ROADMAP.md) develops RCU, [OS-055](../ROADMAP.md) adds NUMA placement, and [OS-057](../ROADMAP.md) connects state to load balancing.

## References

- Linux kernel documentation, [this_cpu operations](https://docs.kernel.org/core-api/this_cpu_ops.html), current page checked 2026-09-04. Per-CPU bases and offsets, current-CPU primitives, read-modify-write behavior, pointers, remote-access cautions, and counters.
- Linux kernel documentation, [Semantics and Behavior of Local Atomic Operations](https://docs.kernel.org/core-api/local_ops.html), current page checked 2026-09-04. CPU-local atomicity, preemption requirements, interrupt contexts, remote access, and current-CPU alternatives.
- Linux kernel documentation, [CPU hotplug in the Kernel](https://docs.kernel.org/core-api/cpu_hotplug.html), current page checked 2026-09-04. Possible, present and online masks, hotplug states, callback registration, ordering, rollback, startup, and teardown.
- Linux kernel documentation, [Proper Locking Under a Preemptible Kernel](https://docs.kernel.org/locking/preempt-locking.html), current page checked 2026-09-04. Migration hazards, protection of per-CPU data, preemption control, and interrupt-local behavior.
- Linux kernel documentation, [Lock types and their rules](https://docs.kernel.org/locking/locktypes.html), current page checked 2026-09-04. Local locks, preemption and interrupt control, spin locks, owner rules, and PREEMPT_RT differences.
- Linux kernel documentation, [How realtime kernels differ](https://docs.kernel.org/core-api/real-time/differences.html), current page checked 2026-09-04. Per-CPU protection, local locks, preemption, soft interrupts, timers, and real-time configuration semantics.
- Linux kernel documentation, [Linux kernel memory barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), current page checked 2026-09-04. Atomicity, ordering, barriers, acquire and release, multicopy behavior, and device interactions.
- Linux kernel documentation, [What is RCU?](https://docs.kernel.org/RCU/whatisRCU.html), current page checked 2026-09-04. Read-side protection, grace periods, deferred reclamation, publication, and quiescent-state reasoning.
- Linux kernel documentation, [SMP IRQ affinity](https://docs.kernel.org/core-api/irq/irq-affinity.html), current page checked 2026-09-04. Interrupt routing across CPUs, affinity masks, default affinity, and CPU-local workload placement.
- Linux kernel documentation, [Reducing OS jitter due to per-CPU kthreads](https://docs.kernel.org/admin-guide/kernel-per-CPU-kthreads.html), current page checked 2026-09-04. Per-CPU kernel threads, work placement, interrupts, timers, workqueues, RCU callbacks, and CPU isolation.

## Exercises

### Exercise 1

Design per-CPU request accounting for approximate dashboards and exact billing. Specify update, aggregation, epoch, migration, and overflow behavior.

### Exercise 2

Choose protection for a per-CPU structure accessed from tasks, soft interrupts, hard interrupts, NMI, and a remote reset path on ordinary and real-time kernels.

### Exercise 3

Design a per-CPU allocator cache with global capacity, batching, NUMA placement, memory pressure, and CPU-hotplug support.

### Exercise 4

Specify initialization, rollback, offline drain, and module teardown for a per-CPU queue whose items retain external object references.

### Exercise 5

Build a correctness and performance evaluation for per-CPU state. Include migration, weak memory, false sharing, sparse CPU IDs, hotplug, and observability effects.

## Answers to the Exercises

### Answer 1

Dashboard updates use one current-CPU increment whose selection and modification cannot be separated by migration. A reader stabilizes storage lifetime, samples every relevant shard, records start and end timestamps and CPU-set generation, and labels the sum approximate. Use wide unsigned shards and define wrap handling.

Billing rotates explicit epochs. A coordinator publishes a new epoch with release ordering; each CPU observes it, atomically exchanges or transfers its old shard exactly once, and acknowledges the generation. The collector waits for every CPU that could have produced in the old epoch, including shards taken offline during rotation, then closes the epoch. Hotplug startup joins only the published generation; teardown transfers its final count before acknowledgment. Retry identifiers prevent double folding. The exact claim is no lost or duplicated accepted events per closed epoch, not a simultaneous total during an open epoch.

### Answer 2

First inventory which fields are touched by each context. A single current-CPU primitive can update an independent counter if its contract covers local reentry. A compound structure shared by task and softirq uses the matching bottom-half-safe local lock; hard-interrupt access requires the interrupt-safe form. If NMI also writes, ordinary interrupt masking is insufficient, so redesign toward NMI-safe atomics, lockless slots, or a separate NMI shard.

The remote reset must not mix with non-atomic local read-modify-write. Prefer queueing a reset request to the owner and using generation or exchange semantics; otherwise every path uses a compatible truly atomic operation. On real-time kernels, rely on documented local-lock and raw-lock semantics rather than assuming a normal spin lock disables preemption. No protected region sleeps unless its primitive permits it. Release and acquire ordering publishes reset generations and associated payload independently of counter atomicity.

### Answer 3

Give each CPU a bounded magazine allocated near its NUMA node. Fast allocation and free pin only for the local magazine operation; refill and drain move batches under a node-pool lock. The global capacity authority reserves each batch before transfer, so the sum of issued reservations never exceeds capacity. Local hidden objects remain included in accounting.

Choose high and low watermarks from measured contention, footprint, and skew. Memory pressure requests drain through owner-CPU work or safely steals under a compatible protocol. Startup initializes an empty magazine before publishing the CPU online to the allocator. Offline stops routing, waits for active local operations, returns every object and reservation to its node pool, and marks a new generation. Allocation-node fallbacks are recorded. Repeated hotplug and partial refill failure leave no duplicate object, quota leak, or reference.

### Answer 4

Register a hotplug state with declared dependency order. For every already online CPU, allocate the queue, initialize lock and generation, establish worker context, then publish readiness. If CPU `n` fails, remove readiness and tear down only successful instances in reverse-safe order; preserve each item reference until moved or cancelled.

Offline first prevents new selection through the routing generation, redirects producers, and waits for any producer that captured the old generation. It stops the worker, transfers runnable items or completes cancellation exactly once, waits for executing callbacks, releases item references, and marks the queue drained. Module removal unregisters callbacks through the hotplug API, excludes new external calls, performs the same drain for online and retained offline shards, waits for RCU and other deferred readers, releases workers and item resources, and frees dynamic per-CPU storage last.

### Answer 5

Model allowed contexts and verify every access against its primitive. Force preemption between CPU selection, pointer acquisition, and use; generate task, softirq, hardirq, and supported NMI reentry; combine local updates with remote reads and deliberately forbidden remote writes. Run repeated online, startup failure, routing, offline, rollback, and unload while queues and callbacks are active. Cover one CPU, sparse identifiers, maximum possible CPUs, wraparound, allocation failure, and weak-memory publication.

Use lock dependency checking, race detectors, address and undefined-behavior sanitizers, reference-leak checks, and architecture-specific stress. Inspect generated code for current-CPU primitives where relevant. Measure update cost, aggregate cost and error, cache-line transfers, false-sharing sensitivity, memory and TLB footprint, NUMA locality, batch skew, hotplug time, interrupt latency, and real-time behavior. Measure observability overhead by comparing runs with and without collection. Preserve source, configuration, topology, masks, placement, seeds, traces, counters, raw samples, failures, reviewer roles, and limitations.
