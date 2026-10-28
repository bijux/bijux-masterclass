---
module_id: OS-052
program: Operating Systems
level: 2
module_number: 52
title: SMP Kernel Synchronization
status: complete
last_verified: 2026-09-04
---

# SMP Kernel Synchronization

## One-Page Review

### Governing question

How should a multiprocessor kernel coordinate tasks, interrupts, and CPUs so shared state remains race free, ordered, live, and scalable across architectures and preemption models?

### Essential definitions

- **Symmetric multiprocessing (SMP)** lets peer logical CPUs execute kernel code concurrently over shared memory and devices.
- A **data race** is a pair of conflicting concurrent accesses without the synchronization required by the language and kernel memory models.
- A **critical section** is a region whose invariant requires controlled admission and defined memory ordering.
- A **spin lock** provides busy-waiting mutual exclusion for bounded non-sleeping regions and supplies acquire/release ordering under its contract.
- A **sleeping lock** blocks a waiter through the scheduler and is usable only in contexts that may sleep.
- An **atomic read-modify-write** changes one object indivisibly; its ordering of other memory depends on the exact operation variant.
- A **memory barrier** constrains observation order without by itself providing ownership or mutual exclusion.
- A **lock-order graph** contains an edge `A -> B` when code may acquire lock class `B` while holding `A`; a reachable cycle admits deadlock.
- A **completion** represents a one-way event whose waiter and signaler also obey object-lifetime and reinitialization rules.

### Central model, mechanism, or theorem

For shared object `O`, enumerate operations, invariants, and execution contexts `C={task,softirq,hardirq,NMI,remote CPU,hotplug}`. Choose a protocol that provides: atomic state transitions, happens-before edges for related memory, lifetime protection, a globally acyclic blocking order, compatible interrupt and preemption behavior, and forward progress under the expected scheduler and failure model.

Mutual exclusion and memory ordering are related but distinct. A lock normally supplies both for participants using that lock; an atomic counter can be indivisible without publishing adjacent fields; a barrier can order fields without preventing two writers. Correctness comes from one coherent protocol followed by every access, not from accumulating primitives around suspicious lines.

### Critical invariants

- Every shared field has one declared protection rule followed by task, interrupt, NMI, remote, and teardown paths.
- A lock is never acquired in a context where it may sleep, recurse illegally, or be interrupted by a path that reacquires it incompatibly.
- Successful publication orders complete initialization before reachability, and reclamation occurs only after all permitted readers quiesce.
- Lock-class acquisition edges remain acyclic, including error, interrupt, reclaim, callback, and nested-object paths.
- Waiters publish their wait state and recheck the predicate without a lost-wakeup window.
- Atomic operation names are interpreted exactly: failed conditional operations and relaxed or non-returning forms are not granted stronger ordering.
- Progress claims include bounded lock hold time, owner scheduling, priority behavior, and CPU-hotplug or shutdown transitions.

### Common failures

Common errors are treating `volatile` as synchronization, assuming atomicity implies ordering, using a sleeping lock in interrupt context, disabling local interrupts instead of excluding remote CPUs, taking locks in reverse order on an error path, calling unknown code while holding an internal lock, waiting for an event while holding a lock needed by the signaler, reinitializing a completion with active waiters, using a sequence counter around pointers that can be freed, reclaiming an RCU-protected object before a grace period, and transferring non-real-time spin-lock assumptions into a fully preemptible real-time kernel.

### Compact example

Suppose scheduler code can acquire `runqueue -> timer` and timer code can acquire `timer -> statistics`. Those edges form an acyclic order. A new statistics path that acquires `statistics -> runqueue` closes the cycle, so three CPUs can each hold one lock while waiting for the next. The correct review examines lock classes and all paths rather than hoping timing tests reproduce the deadlock.

### Connections

[OS-021](021-critical-sections-in-the-kernel.md), [OS-022](022-spinlocks-and-interrupt-context.md), [OS-023](023-mutexes-semaphores-and-condition-variables.md), and [OS-024](024-atomic-operations.md) establish the primitives. [OS-051](051-per-cpu-state.md) reduces sharing; [OS-053](../ROADMAP.md) and [OS-054](../ROADMAP.md) deepen scalable locking and RCU.

## Governing Question

On an SMP kernel, two CPUs can execute the same subsystem simultaneously while a device interrupt preempts one and a timer or NMI observes the same objects. Compiler transformation, CPU reordering, cache coherence, preemption, and callback lifetimes all shape what each context can observe.

The governing question is not merely which lock to add. It asks for a complete protocol: ownership, atomicity, ordering, admissible contexts, lifetime, lock order, waiting, progress, teardown, and evidence across every access path.

## Why This Matters

Synchronization errors corrupt scheduler queues, page tables, filesystems, sockets, reference counts, device state, and security decisions. Failures can be rare because they require precise overlap, weak-memory outcomes, interrupts, or shutdown timing.

Over-synchronization is also harmful. One cache-line lock can serialize hundreds of CPUs; long non-preemptible regions damage latency; unfair readers can starve writers; debug instrumentation can change the very timing being measured.

A disciplined design lets correctness and performance evolve independently. Explicit invariants and lock classes make it possible to shard state, add optimistic reads, or replace a lock without losing the original proof obligations.

## Prerequisites and Retrieval

Review [OS-013](013-threads-and-execution-contexts.md), [OS-014](014-context-switching.md), [OS-015](015-process-states-and-wait-queues.md), [OS-021](021-critical-sections-in-the-kernel.md), [OS-022](022-spinlocks-and-interrupt-context.md), [OS-023](023-mutexes-semaphores-and-condition-variables.md), [OS-024](024-atomic-operations.md), [OS-025](025-deadlock-conditions-and-avoidance.md), and [OS-051](051-per-cpu-state.md).

Retrieve these distinctions:

- concurrency includes CPUs, preemption, interrupts, NMI, callbacks, and teardown;
- atomicity, mutual exclusion, visibility ordering, and lifetime are separate properties;
- local interrupt control does not stop a remote CPU;
- spinning contexts cannot call operations that may sleep;
- reference acquisition must race safely with the final release;
- a condition wait is a predicate loop plus an atomic enqueue-and-sleep protocol;
- a lock order applies to error and callback paths as well as mainline code;
- performance evidence does not substitute for a synchronization proof.

## Learning Objectives

After this module, you should be able to:

1. derive synchronization requirements from invariants and a complete context inventory;
2. select spin, raw spin, mutex, reader-writer, atomic, sequence, completion, per-CPU, or RCU mechanisms;
3. distinguish indivisible operations from acquire, release, relaxed, and full ordering;
4. construct lock-class graphs and identify deadlock through ordinary, interrupt, reclaim, and callback paths;
5. design wait, wake, publication, reference, teardown, and CPU-hotplug protocols;
6. reason about contention, fairness, priority inversion, cache traffic, and real-time configurations;
7. validate SMP synchronization with model reasoning, runtime checkers, stress, fault injection, and measurement.

## Core Exposition

### Begin with the invariant

State what must remain true: a node appears in at most one queue, a reference count equals live ownership, a page-table entry never exposes uninitialized backing, or a device request completes exactly once. Without the invariant, a lock has no reviewable scope.

List each field participating in the invariant and every operation that reads or changes it. Fields that transition together often need one protocol even when stored in different structures.

### Inventory execution contexts

Kernel code can run in process context, soft interrupt, hard interrupt, NMI, worker, timer, remote cross-call, CPU-hotplug callback, or shutdown. Context determines whether it may sleep, be preempted, and interrupt another user of the state.

Include indirect calls: allocation can enter reclaim, tracing can invoke callbacks, wakeup enters scheduler code, and device removal can race completion. Hidden edges often create the hardest deadlocks.

### Define the race

A data race is not simply simultaneous source lines. Conflicting accesses without the required synchronization can allow compiler and hardware behavior that source-level intuition misses.

Intentional lockless access uses primitives such as single-access loads and stores, atomics, barriers, sequence validation, or RCU under a documented pattern. Plain racing access is not repaired by observing correct results on one architecture.

### Locks as protocols

A lock defines protected state, allowed contexts, acquisition and release semantics, recursion policy, nesting order, ownership, and lifetime. Every access to the protected invariant follows that contract.

Embedding a lock near data helps ownership but does not define interactions with outer locks. Documentation and assertions name the lock class and required preconditions.

### Spin locks

A spin lock repeatedly tests ownership instead of sleeping. It suits short critical sections where the holder will run promptly and the caller cannot sleep.

Contention wastes CPU cycles and moves the lock cache line. Work inside the region is bounded, nonblocking, and free of callbacks whose context is unknown.

### Interrupt-safe spin locking

If a hard interrupt on the same CPU can acquire the lock, task code must prevent that interrupt-local recursion while acquiring global exclusion. Save-and-disable variants preserve the caller's prior interrupt state.

Local interrupt disabling alone does not exclude remote holders. The spin lock supplies inter-CPU exclusion; the interrupt control prevents self-deadlock on the current CPU.

### Raw spin locks

Raw spin locks preserve truly spinning, non-sleeping semantics where architecture or low-level interrupt code requires them, including on real-time kernels. Their regions accept the strongest atomic-context restrictions.

They are not a performance badge. Selecting raw locking unnecessarily worsens latency and forbids operations that ordinary real-time-substituted locks could support.

### Mutexes and sleeping locks

A mutex can block a task and let the scheduler run other work. It is appropriate for longer process-context sections and may support priority inheritance under relevant configurations.

It cannot be acquired in hard interrupt or other non-sleeping context. Unlock ownership, signal interruption, timeout, and teardown behavior follow the particular API.

### Reader-writer locks

Reader-writer mechanisms allow concurrent readers while excluding writers. They help only when read-side concurrency outweighs extra atomic operations, larger state, cache traffic, and fairness costs.

Reader dominance can starve writers, while writer preference can raise read latency. Read-mostly structures may benefit more from sequence counters or RCU when their semantics fit.

### Atomic read-modify-write

Atomic exchange, compare-and-exchange, fetch-add, and bit operations provide indivisible transitions on one object. Compare-and-exchange loops retry when another CPU wins.

The operation's return and success path matter. Conditional failure can have weaker ordering; non-returning and relaxed variants may order nothing beyond the atomic object. Choose the narrowest semantics that still prove publication and consumption.

### Reference counters

Reference counters encode object lifetime, not arbitrary event counts. Incrementing a nonzero live reference must race safely with final decrement, and the zero transition triggers one destruction path.

Overflow, resurrection from zero, and use-after-final-release are security concerns. A reference primitive with saturation and purpose-specific checks is safer than a generic wrapping integer.

### Memory ordering

Acquire prevents later operations from moving before the acquisition; release prevents earlier operations from moving after publication. A matching synchronization relation lets a consumer observe initialized payload after seeing the published state.

A full barrier supplies broader order but still does not create ownership, preserve lifetime, or force another CPU to execute. Barriers are placed from a happens-before argument, not as superstition.

### Compiler and CPU observations

Single-access primitives constrain compiler invention, tearing, or repeated loads under their definitions. They do not automatically create inter-CPU synchronization.

The kernel memory model describes allowed executions across architectures. SMP barrier forms can compile cheaply on uniprocessor builds while still constraining compiler behavior as documented.

### Publication

A producer initializes an unreachable object, then performs a release publication through a pointer, flag, list operation, or lock. A reader acquires or enters the matching read protocol before dereferencing payload.

Publishing first and filling fields later exposes partial initialization. Lifetime must extend from discovery through the reader's final use.

### Sequence counters

A sequence counter lets readers sample data without locking: read a starting even sequence, copy fields, and retry if the sequence changed or was odd. Writers serialize and bracket updates.

Readers cannot safely follow pointers that writers may free without an additional lifetime mechanism. Writers also cannot be preempted indefinitely by readers that spin waiting for an even sequence in contexts that can interrupt them.

### Sequence locks and latches

A sequence lock combines writer serialization with sequence validation and can offer locking reader variants. A latch keeps two data copies so an interruptible reader can select a stable copy during writer updates.

These tools are semantic patterns, not universally faster substitutes. Copy cost, writer latency, reader retries, pointer lifetime, and real-time needs determine fit.

### RCU overview

Read-copy-update lets readers traverse a published version in a read-side critical section while writers replace references and defer reclamation until preexisting readers pass a grace period.

RCU provides lifetime and ordering under its APIs; it does not automatically serialize competing writers or make compound reader snapshots consistent. [OS-054](../ROADMAP.md) develops its variants and proof structure.

### Per-CPU state

Per-CPU state removes inter-CPU write sharing when each CPU owns its shard. Current-CPU operations still require correct migration and interrupt semantics, and aggregation defines its consistency.

Remote access can invalidate cheap local-operation assumptions. [OS-051](051-per-cpu-state.md) covers addressing, aggregation, and hotplug lifecycle in depth.

### Condition waiting

A waiter evaluates a predicate while holding its protecting lock, prepares or enqueues itself, releases the lock as part of the sleep protocol, and rechecks after every wake. The loop handles spurious wakes and competing consumers.

The signaler changes the predicate under its protocol before waking waiters. Reversing publication and wakeup creates a missed event or a waiter that sleeps after the only signal.

### Completions

A completion represents occurrence of an event rather than ownership of a region. Wait variants can be interruptible or time bounded; completion can release one or all eligible waiters according to the API.

The completion object outlives every waiter and signaler. Reinitialization occurs only under a protocol that excludes active races; otherwise a waiter can be lost or a late signal can touch freed memory.

### Cross-CPU calls

SMP cross-call primitives arrange for callbacks on selected online CPUs, often through interprocessor interrupts. The callback must satisfy strict context, duration, and blocking rules.

Synchronous waiting creates dependencies on target progress. Never wait while holding a resource the remote callback needs, and coordinate CPU hotplug so targets cannot disappear between selection and execution.

### Lock ordering

Assign a partial order to lock classes. Whenever code holds `A` and acquires `B`, record edge `A -> B`; the union across every path must remain acyclic.

Object identity can refine nesting, such as parent before child or lower address before higher, but equal-class nesting needs explicit subclasses or validated ordering. Error cleanup follows the same graph.

### Interrupt lock inversions

Suppose task code holds `A` with interrupts enabled and an interrupt acquires `B` then `A`; elsewhere code holds `A` then `B`. Even if the ordinary thread order seems consistent, interruption creates self-deadlock.

Lock analysis therefore tracks whether each class is ever held or acquired in hardirq or softirq contexts and whether those contexts are enabled at acquisition.

### Callback and reclaim hazards

Calling an external callback while holding an internal lock imports unknown lock edges and latency. Copy required state, retain lifetime, release internal locks, call outward, then revalidate if possible.

Memory allocation under locks can invoke reclaim that reenters filesystem or device paths. Allocation flags, reserves, preallocation, and reclaim annotations belong in the lock proof.

### Lock dependency validation

Runtime lock checking groups instances into lock classes, records observed acquisition edges and interrupt usage, and computes whether their closure admits deadlock. It can expose a multi-CPU cycle after observing each component separately.

Coverage remains essential: an unexecuted edge is unknown. Correct class keys, subclasses, annotations, and representative error and hotplug paths determine evidence quality.

### Contention and cache coherence

A contended lock serializes useful work and repeatedly transfers its cache line. Queueing locks can give waiters local spinning positions and bounded handoff behavior.

Measure hold time, wait time, queue length, acquisitions, cache-line transfers, preemption, owner off-CPU time, and tail latency. A low average can hide rare catastrophic stalls.

### Fairness and starvation

Fair locks bound bypass but may reduce throughput or prevent opportunistic handoff to a running nearby CPU. Unfair locks can maximize common-case throughput while starving a remote or low-priority waiter.

Select the progress property from subsystem requirements: starvation freedom, bounded wait, writer progress, priority ordering, or best-effort throughput.

### Priority inversion

A high-priority task can wait for a lock held by a low-priority task that is itself displaced by medium-priority work. Priority inheritance can boost the owner for suitable sleeping locks.

Spin locks, interrupt contexts, nested dependencies, and raw locks have different mitigation. Real-time analysis includes maximum critical-section and blocking chains rather than assuming priority alone governs latency.

### Real-time kernel differences

Fully preemptible real-time kernels can substitute sleeping implementations for ordinary spin and reader-writer locks, thread interrupts, and change soft-interrupt execution. Incidental preemption-disabling assumptions no longer hold.

Code expresses whether it needs raw atomic exclusion, local serialization, priority inheritance, or ordinary mutual exclusion using the matching abstraction. Test both configurations rather than hiding differences behind conditional guesses.

### CPU hotplug and teardown

Synchronization objects and shared structures must survive readers, waiters, remote calls, interrupts, and deferred callbacks during CPU offline and subsystem removal. First block new entry, then drain and wait, detach reachability, and free last.

Do not wait for a CPU callback after making that callback unable to run. Hotplug locks, online masks, callback generations, and work migration form part of the progress proof.

### Failure and cancellation

Timeout or signal interruption ends one wait, not necessarily the producer's use of the synchronization object. The caller cancels, joins, or retains storage until the producer reaches a terminal state.

Partial initialization and rollback acquire only documented locks and publish no invalid object. Panic and NMI paths use deliberately restricted mechanisms rather than opportunistically entering ordinary locking.

### Testing and assurance

Use model-based histories and memory-model litmus tests for small protocols; runtime lock dependency, race, atomic-sleep, and reference checkers for integration; and stress with preemption, interrupts, hotplug, memory pressure, failures, and weak-memory architectures.

Performance tests vary CPU count, socket topology, critical-section length, read/write mix, owner preemption, priorities, and instrumentation. Correctness outcomes and throughput are reported separately.

Assurance names subsystem, locking, architecture, scheduler, interrupt, memory-model, real-time, hotplug, security, performance, and independent reviewers. Passing a stress run cannot prove absence of an allowed weak-memory execution.

## Definitions and Notation

Let threads of control `T` include tasks and asynchronous contexts on CPUs. For shared state `O`, operation `a` has read set `R(a)`, write set `W(a)`, context `C(a)`, and lifetime interval `L(a)`.

Two operations conflict when `W(a)` intersects `R(b) union W(b)`. The protocol must order conflicts or permit them through a formally defined atomic or lockless rule.

Write `a hb-> b` when synchronization establishes a happens-before relation from `a` to `b`. Coherence of one location does not imply needed `hb` edges for other locations.

Let lock graph `G=(V,E)` contain lock classes `V` and edge `(A,B)` whenever one path can acquire `B` while holding `A`. A necessary deadlock-freedom obligation for blocking acquisition is that the reachable graph is acyclic, alongside context and progress assumptions.

Let publication `P=(init,release,acquire,use,quiesce,reclaim)`. Correctness requires initialization before release publication, matching reader acquisition before use, and reclamation after every eligible prepublication reader quiesces.

## Mechanisms, Invariants, or Proof Structure

1. **State the invariant.** Identify fields, legal states, transitions, and the precise failure that a conflicting interleaving would cause.
2. **Enumerate contexts.** Include tasks, softirq, hardirq, NMI, remote calls, callbacks, reclaim, hotplug, cancellation, and teardown.
3. **Assign one protocol.** Map every access to a lock, atomic, sequence, RCU, per-CPU, immutable, or single-owner rule.
4. **Prove ordering.** Derive acquire, release, barrier, lock, wakeup, and grace-period edges for related memory.
5. **Prove lifetime.** Make discovery, reference acquisition, use, cancellation, quiescence, and final reclamation race safely.
6. **Construct the lock graph.** Union ordinary, interrupt, reclaim, callback, error, hotplug, and nested-object edges and reject cycles.
7. **Validate context rules.** Exclude sleeping in atomic context, interrupt recursion, illegal nesting, unbounded raw regions, and unsupported NMI operations.
8. **Prove waiting.** Couple predicate change, waiter enrollment, wakeup, timeout, and object lifetime without missed events.
9. **Prove progress.** Bound hold time and dependency chains; cover fairness, priority inversion, owner preemption, target CPU availability, and shutdown.
10. **Minimize sharing.** Partition, batch, queue, or use read-mostly techniques only while preserving the first nine obligations.
11. **Exercise adversarial schedules.** Combine weak memory, migration, interrupts, hotplug, faults, cancellation, and resource pressure.
12. **Preserve evidence.** Retain configurations, topology, lock classes, traces, litmus outcomes, raw measurements, failures, and limitations.

<!-- bijux-verify: {"id":"lock-order-cycle","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"base-order-acyclic=True\ncandidate-edge=statistics->runqueue\ncandidate-creates-cycle=True\n","stderr":""}} -->
```python
def has_cycle(edges: tuple[tuple[str, str], ...]) -> bool:
    nodes = tuple(sorted({node for edge in edges for node in edge}))
    graph = {
        node: tuple(target for source, target in edges if source == node)
        for node in nodes
    }
    state = {node: 0 for node in nodes}

    def visit(node: str) -> bool:
        if state[node] == 1:
            return True
        if state[node] == 2:
            return False
        state[node] = 1
        if any(visit(target) for target in graph[node]):
            return True
        state[node] = 2
        return False

    return any(visit(node) for node in nodes)


base = (("runqueue", "timer"), ("timer", "statistics"))
candidate = ("statistics", "runqueue")
print(f"base-order-acyclic={not has_cycle(base)}")
print(f"candidate-edge={candidate[0]}->{candidate[1]}")
print(f"candidate-creates-cycle={has_cycle(base + (candidate,))}")
```

The executable example detects a cycle in one declared lock-class graph. It does not run threads, acquire locks, cover interrupt states, prove that the edge set is complete, model memory ordering, measure contention, or validate kernel code.

## Alternatives and Trade-Offs

- Spin locks avoid scheduler transitions for short atomic regions but burn CPU and amplify owner-preemption latency; mutexes sleep efficiently and require sleepable context.
- Raw spin locks preserve strict atomic semantics across real-time configurations but worsen latency; ordinary locks allow substitution and broader preemption.
- One coarse lock gives a simple invariant and graph but serializes unrelated work; fine-grained locks improve concurrency and multiply lifetime and ordering edges.
- Reader-writer locks permit parallel readers but add cache traffic and fairness cost; mutexes can outperform them for short or write-heavy sections.
- Sequentially consistent or fully ordered atomics simplify reasoning but constrain optimization; acquire, release, and relaxed operations reduce cost and demand precise proofs.
- Sequence counters give very cheap consistent-value reads but can retry and cannot alone protect reclaimable pointers; locking readers provide stronger progress at higher cost.
- RCU makes read-mostly traversal cheap but defers reclamation and requires separate writer serialization; locks give immediate reclamation after exclusion.
- Per-CPU state removes update sharing but shifts cost to aggregation and hotplug; global state gives simple exact observation and contended writes.
- Fair queueing locks bound bypass and improve large-system handoff; unfair locks may exploit locality for higher common-case throughput.
- Busy polling minimizes wake latency under short waits but consumes capacity; completions and wait queues sleep efficiently with scheduling overhead.
- Calling callbacks outside locks avoids imported lock edges but requires retained state and revalidation; calling inside preserves a snapshot and risks deadlock and latency.
- Extensive debug checking catches misuse but changes timing and cost; production-like testing is faster and has weaker diagnostic evidence.

## Failure Modes and Misconceptions

- **“Cache coherence eliminates data races.”** It propagates cache lines but does not supply the required synchronization protocol.
- **“`volatile` is a lock or barrier.”** It does not provide kernel inter-CPU mutual exclusion or general happens-before ordering.
- **“Atomic means fully ordered.”** Ordering depends on the exact atomic variant and success path.
- **“A barrier excludes writers.”** It orders observations without granting ownership.
- **“Interrupt disabling is a global lock.”** It affects local interrupt delivery, not remote CPUs.
- **“Any lock is safe in interrupt context.”** Sleeping and context-incompatible locks can deadlock or violate scheduler rules.
- **“The mainline lock order is enough.”** Error, reclaim, interrupt, callback, and teardown edges count too.
- **“A wakeup can precede predicate publication.”** That ordering can create a lost-wakeup window.
- **“Timeout means the signaler stopped using the object.”** Producer lifetime can extend beyond the waiter.
- **“Sequence validation protects pointers from reclamation.”** It needs an independent lifetime mechanism.
- **“RCU serializes writers.”** Writers commonly require their own lock or atomic protocol.
- **“Reference decrement alone publishes all teardown state.”** Ordering follows the precise reference API and surrounding barriers.
- **“Real-time kernels preserve incidental spin-lock behavior.”** Ordinary lock implementations and interrupt execution can change.
- **“No deadlock in stress means the graph is acyclic.”** Rare or unexecuted edges may remain.

## Worked Examples

### Example 1

Two CPUs enqueue the same node into different lists after racing on a plain state flag. An atomic state transition or one lock covering state and linkage preserves single membership.

### Example 2

Task code holds a spin lock and is interrupted by a handler that takes the same lock. The task-side interrupt-safe acquisition prevents local recursive deadlock while the lock excludes remote CPUs.

### Example 3

A producer fills a request and release-publishes its ready flag. A consumer acquire-loads the flag before reading fields, preventing observation of a ready but partially initialized request.

### Example 4

A failed compare-and-exchange observes that another CPU changed a state. The code does not assume success-path ordering on failure; it reloads and retries under the documented loop.

### Example 5

A sequence reader samples timekeeping fields, detects that the writer changed the sequence, discards the mixed sample, and retries. Pointer targets use separate lifetime protection.

### Example 6

A completion waiter times out but a worker still owns the request pointer. The caller cancels and joins or retains the object until the worker acknowledges a terminal state.

### Example 7

Observed edges `runqueue -> timer`, `timer -> statistics`, and `statistics -> runqueue` form a cycle. Runtime lock checking can reject the graph even if three-way deadlock never occurs during the run.

### Example 8

A filesystem allocates memory while holding an inode lock; reclaim reenters the filesystem and requests the same class. Preallocation or non-reclaiming allocation breaks the hidden dependency.

### Example 9

An ordinary spin lock becomes a sleeping priority-inheritance lock on a real-time kernel. Code that relied on its incidental preemption disabling switches to the explicit local or raw primitive its invariant needs.

### Example 10

CPU offline begins while another CPU schedules a synchronous cross-call to it. Stabilizing the online target set and ordering drain prevents waiting forever on a callback that can no longer execute.

## Cross-Program Connections

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects memory models, atomics, locks, conditions, lock-free structures, and liveness. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects coherence, weak ordering, interprocessor interrupts, NUMA, and atomic instruction costs.

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects concurrent queues, sequence counters, reference graphs, reclamation, and sharding. [Security Engineering](../../25-security-engineering/ROADMAP.md) connects race exploitation, reference overflow, lifetime safety, and denial of service.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies hazard analysis, interface contracts, fault injection, evidence, and assurance. Within this program, [OS-053](../ROADMAP.md) focuses on scalability, [OS-054](../ROADMAP.md) deepens RCU, and [OS-059](../ROADMAP.md) applies cross-CPU synchronization to TLB shootdowns.

## References

- Linux kernel documentation, [SMP primitives](https://docs.kernel.org/core-api/SMP.html), current page checked 2026-09-04. CPU identification, selected and all-CPU calls, callback constraints, online targets, and synchronous waiting.
- Linux kernel documentation, [Atomic types](https://docs.kernel.org/core-api/wrappers/atomic_t.html), current page checked 2026-09-04. Atomic operations, read-modify-write forms, failure paths, acquire, release, relaxed and full ordering, and barrier augmentation.
- Linux kernel documentation, [Linux kernel memory barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), current page checked 2026-09-04. Compiler and CPU ordering, dependencies, acquire and release, locks, multicopy behavior, devices, and examples.
- Linux kernel documentation, [Lock types and their rules](https://docs.kernel.org/locking/locktypes.html), current page checked 2026-09-04. Raw spin, spin, reader-writer, local and sleeping locks, ownership, context rules, nesting, and PREEMPT_RT differences.
- Linux kernel documentation, [Locking lessons](https://docs.kernel.org/locking/spinlocks.html), current page checked 2026-09-04. Spin locks, interrupt-safe use, reader-writer costs, memory ordering, and basic design guidance.
- Linux kernel documentation, [Sequence counters and sequential locks](https://docs.kernel.org/locking/seqlock.html), current page checked 2026-09-04. Writer serialization, reader retry, pointer restrictions, locking readers, latch variants, and API forms.
- Linux kernel documentation, [Runtime locking correctness validator](https://docs.kernel.org/locking/lockdep-design.html), current page checked 2026-09-04. Lock classes, dependency edges, interrupt usage, closure, annotations, recursion, and coverage.
- Linux kernel documentation, [Completions](https://docs.kernel.org/scheduler/completion.html), current page checked 2026-09-04. Wait and signal semantics, initialization, reinitialization, timeouts, interruption, and object lifetime.
- Linux kernel documentation, [How realtime kernels differ](https://docs.kernel.org/core-api/real-time/differences.html), current page checked 2026-09-04. Lock substitution, preemption, local locks, interrupt and softirq threading, and real-time-safe usage.
- Linux kernel documentation, [What is RCU?](https://docs.kernel.org/RCU/whatisRCU.html), current page checked 2026-09-04. Read-side protection, publication, grace periods, callbacks, reclamation, writer needs, and API fundamentals.

## Exercises

### Exercise 1

Derive synchronization for a shared request object accessed by submitting tasks, hard-interrupt completion, timeout workers, cancellation, and device removal.

### Exercise 2

Design a published read-mostly routing table using a lock, sequence counter, or RCU. Compare ordering, lifetime, writer serialization, reader progress, and teardown.

### Exercise 3

Construct and audit a lock-class graph for scheduler, timer, statistics, device, and memory-reclaim paths. Include interrupt-state annotations and callbacks.

### Exercise 4

Specify an exact condition-wait and completion protocol that remains safe across signal interruption, timeout, late completion, and object destruction.

### Exercise 5

Build a validation and performance plan for an SMP synchronization change across ordinary, weak-memory, large-NUMA, hotplug, and real-time systems.

## Answers to the Exercises

### Answer 1

Give the request a state machine such as allocated, queued, executing, completing, cancelled, done, and removed plus a purpose-specific reference count. A submit-side lock or atomic transition publishes fully initialized payload with release ordering before the device can see it. Interrupt completion uses only hardirq-safe primitives, atomically claims the single terminal transition, stores status, detaches queue linkage, and wakes or completes after predicate publication.

Timeout and cancellation acquire a reference before inspecting state, compete through the same terminal transition, and invoke hardware cancellation without holding locks the interrupt needs. A timed-out waiter cannot free the request until completion or cancellation acknowledges that no producer retains it. Device removal blocks new submissions, prevents new interrupt callbacks, drains or terminally fails queued and executing requests, synchronizes interrupt and deferred work, wakes waiters, waits for references, and destroys locks and memory last. Every error path maintains single linkage, single terminal completion, published status, and no resurrection from zero.

### Answer 2

A reader-writer lock gives readers one coherent table while held and lets a writer mutate or replace it exclusively; readers can sleep only where the lock permits, and contention and writer fairness shape progress. A sequence counter gives cheap nonblocking samples of copyable scalar structure; writers serialize and bracket mutation, readers retry on change, and pointer targets need separate lifetime protection. Long writers or frequent change can cause retry storms.

RCU release-publishes an immutable replacement pointer, readers enter an RCU read-side section and acquire it through the matching primitive, and writers serialize separately. The old table is reclaimed only after a grace period and any longer references. Readers can observe either complete version but not necessarily a multi-update transaction beyond the published root. Teardown blocks new publication, removes reachability, waits for readers and callbacks, and frees last. Choose from read/write frequency, table size, reader context, exact snapshot, reclamation delay, update latency, and real-time progress rather than interface fashion.

### Answer 3

Define stable lock classes and record every nested acquisition, including error release-and-retry paths. Mainline edges might be `runqueue -> timer`, `timer -> statistics`, and `device -> request`. Then inspect indirect edges: timer callback into scheduler, statistics allocation into reclaim, reclaim into device writeback, device completion into scheduler wakeup, hotplug into timer shutdown, and tracing callbacks from every held class.

Annotate whether each class is held or acquired with hardirq or softirq enabled and whether an interrupt can preempt its holder. Add object-order rules and subclasses for same-class nesting. Reject any reachable cycle, not merely adjacent reversal. Run dependency checking with workloads that exercise success, errors, interrupts, reclaim, callbacks, hotplug, and teardown; audit unexecuted static paths because runtime validation knows only observed edges. Record deliberate try-lock or drop-and-retry breaks as semantic protocols, not omitted edges.

### Answer 4

Protect predicate and waiter enrollment with one lock. The waiter loops: lock, test predicate, prepare wait while protected, atomically release and block through the wait API, finish wait, then retest. The signaler locks, changes the predicate and result, unlocks with release semantics, and wakes eligible waiters. Spurious wakeup merely repeats the loop.

For one operation event, embed a completion in an object whose reference lifetime covers worker and waiter. Initialize before publication. A timeout or signal removes only the wait; it then requests cancellation and joins, or drops its reference while the worker retains another. The worker writes final result before completing and drops its reference afterward. Reinitialization occurs only after the previous generation has no waiter or possible late signaler; otherwise allocate a new generation object. Destruction blocks new users, cancels and joins producers, wakes terminal waiters, waits for references and callbacks, then frees memory.

### Answer 5

Write invariants, context matrix, field-to-protocol map, happens-before relations, lifetime graph, lock-class graph, interrupt annotations, and progress bounds before testing. Use memory-model litmus tests for publication and atomic loops, model-based operation histories for the state machine, and static review for every access. Enable lock dependency, race, atomic-sleep, reference, address, and undefined-behavior checkers.

Stress CPU migration, hard and soft interrupts, NMI where supported, owner preemption, cancellation, timeout, reclaim, allocation failure, callbacks, CPU online and offline, and subsystem removal. Run one CPU, several sockets, maximum practical CPUs, weak-memory architectures, ordinary preemption, full preemption, and PREEMPT_RT. Measure hold and wait distributions, queue depth, cache-line transfers, owner off-CPU time, fairness, priority blocking, throughput, and tail latency with debugging both enabled and disabled. Preserve source and configuration, topology, lock classes, litmus tools and outcomes, workload seeds, traces, checker reports, raw performance data, failures, reviewers, and limitations.
