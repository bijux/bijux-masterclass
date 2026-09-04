---
module_id: OS-021
program: Operating Systems
level: 1
module_number: 21
title: Critical Sections in the Kernel
status: complete
last_verified: 2026-09-04
---

# Critical Sections in the Kernel

## One-Page Review

### Governing question

How should kernel code identify and protect shared invariants across CPUs, preemption, interrupts, deferred work, and teardown without creating deadlock, illegal blocking, or stale-object access?

### Essential definitions

- A **critical section** is code whose shared invariant requires a synchronization or exclusion protocol; it is not defined solely by lock syntax.
- A **concurrency domain** is the complete set of contexts that can access the protected state, such as process, hard-interrupt, soft-interrupt, NMI, and remote CPU contexts.
- **mutual exclusion** prevents overlapping protected mutation; **memory ordering** governs visibility and order of memory accesses.
- A **spinlock** waits without sleeping under its platform semantics; a **mutex** may block and schedule.
- **preemption disabling** prevents the current task from being involuntarily replaced on its CPU; it does not exclude another CPU.
- **interrupt masking** constrains selected interrupt entry on one CPU; it is not global mutual exclusion.
- A **lock ordering** is a directed relation requiring one lock class to be acquired before another.
- **lifetime synchronization** ensures an object remains reachable and alive through every access; a data lock alone may not provide it.

### Central model, mechanism, or theorem

For shared object `O`, define invariant `I(O)`, accessor contexts `C(O)`, protection protocol `P(O)`, lifetime protocol `L(O)`, and global lock order `<`. A valid critical section proves:

`enter_P -> establish exclusive or permitted access -> read/mutate while I is temporarily open -> restore I -> publish under required ordering -> exit_P`, while `L(O)` keeps the object alive.

The primitive must be admissible in every calling context. If hard interrupt and process context share the same state, ordinary process-context locking can deadlock when the interrupt preempts the holder unless the protocol masks that interrupt or restructures ownership. If two CPUs access state, local masking alone is insufficient.

### Critical invariants

- Every shared field belongs to one documented invariant and synchronization domain.
- All access paths, including error, tracing, timer, interrupt, callback, and teardown paths, follow compatible protection.
- A context never sleeps, faults, or takes a sleepable dependency while its current exclusion state forbids it.
- Lock acquisition follows an acyclic global class order or a separately proved protocol.
- Unlock publishes protected writes with the primitive's documented ordering; lockless readers use matching semantics.
- Object reachability and lifetime remain valid until all in-flight contexts and deferred references quiesce.
- Debug and production configurations preserve the claimed semantics, including real-time kernel variants.

### Common failures

Common mistakes are protecting only writers, disabling local interrupts as an SMP lock, holding a spinlock across allocation or I/O that may sleep, taking a process-context lock from an interrupt that can preempt its holder, using an atomic counter to protect a compound invariant, omitting release/acquire ordering, introducing AB-BA order, returning early without unlock, freeing after list removal without waiting for readers, relying on timing tests alone, and assuming a lock type has identical behavior on every kernel configuration.

### Compact example

A device queue is accessed by process context and its hard interrupt. Process code saves and disables the relevant local interrupt state, acquires the queue spinlock, changes list and count together, restores the invariant, unlocks, and restores interrupt state. The interrupt acquires the same lock without attempting to sleep. Remote CPUs are excluded by the lock; local interrupt masking prevents self-deadlock. Teardown disables device admission, synchronizes the interrupt, drains deferred work, removes reachability, waits for readers, and only then frees the queue.

### Connections

[OS-004](004-interrupts-and-exceptions.md) defines interrupt entry, [OS-013](013-threads-and-execution-contexts.md) distinguishes contexts, and [OS-015](015-process-states-and-wait-queues.md) explains sleeping. [OS-022](../ROADMAP.md) deepens spinlocks and interrupt context; [OS-023](../ROADMAP.md) compares blocking primitives.

## Governing Question

Kernel concurrency does not come only from threads. A syscall can be preempted, a hard interrupt can interrupt it, soft or deferred work can run later or concurrently, another CPU can access the same object, and teardown can revoke the object's lifetime. The same function may be called from several of these contexts.

Consequently, finding a race and adding a lock is incomplete. The lock may sleep in an atomic context, an interrupt may reenter the holder, another path may bypass it, a nested order may deadlock, or an object may be freed immediately after a reader obtains its pointer. Correctness begins by enumerating access paths and invariants.

The governing question is how to prove exclusion, visibility, context admissibility, lock order, progress, and lifetime together—and how to preserve that proof as configuration and call paths evolve.

## Why This Matters

Kernel synchronization bugs operate with broad authority. A corrupted list can damage unrelated processes; a deadlock can freeze a machine; a stale pointer can become a privilege escalation. Rare schedules make failures difficult to reproduce.

Overlocking is also harmful. Long critical sections increase interrupt latency, contention, and real-time blocking. A global lock can serialize independent CPUs. Lockless designs may improve read scaling but expand memory-order and lifetime proof obligations.

Kernel configurations change semantics. Linux lock-type documentation distinguishes raw spinlocks, spinlocks, mutexes, and local locks, including PREEMPT_RT behavior. Portable subsystem reasoning must depend on documented semantics rather than assumptions derived from one build.

## Prerequisites and Retrieval

Recall hardware and compiler ordering, atomics, interrupts, task contexts, and wait states. From [OS-014](014-context-switching.md), remember that preemption changes the current task; from [OS-015](015-process-states-and-wait-queues.md), remember that blocking requires a valid scheduler context.

Retrieve these distinctions:

- data-race freedom, invariant preservation, object lifetime, and forward progress are separate properties;
- local preemption control, local interrupt control, and inter-CPU exclusion cover different adversaries;
- atomicity of one field does not protect a relation among fields;
- a lock's ordering applies to accesses within its documented contract, not arbitrary lockless code;
- removing reachability does not prove all prior readers finished;
- lock class order differs from runtime instance identity;
- testing discovers executions but does not prove the absence of an untested race.

## Learning Objectives

After this module, you should be able to:

1. inventory process, preemption, interrupt, deferred, NMI, and remote-CPU access paths;
2. state protected invariants separately from primitive choice;
3. choose among mutexes, spinlocks, raw spinlocks, atomics, sequence counters, RCU, and ownership partitioning;
4. explain local interrupt and preemption controls without overstating their scope;
5. construct lock-order graphs and detect AB-BA cycles;
6. integrate reachability, reference counting, grace periods, callbacks, and teardown;
7. use lockdep, lockstat, KCSAN, assertions, stress, and fault injection with accurate evidence labels.

## Core Exposition

### Start with the invariant

An invariant describes relations that must hold at externally observable boundaries. A queue may require `count == number_of_linked_nodes`, unique membership, and valid head and tail links. Updating only `count` atomically does not protect these relations.

Document which fields the invariant owns, when it may be temporarily false, and which functions require or establish protection. Comments such as “protected by `queue.lock`” are useful only if every access path and lifetime transition follows the rule.

### Enumerate concurrency sources

List normal process paths, syscalls, kernel threads, timer callbacks, hard interrupts, threaded interrupts, soft interrupts, tasklets or equivalent deferred work, work queues, NMI-like contexts, tracing hooks, error recovery, and teardown. Then ask which can run simultaneously and which can preempt another locally.

SMP creates concurrency even when preemption is disabled. Interrupt masking is per CPU. NMI-like contexts may ignore ordinary interrupt masks. A proof must name the actual platform and kernel guarantees.

### Context admissibility

Process context can often sleep, but not while holding spin-style locks, with preemption or interrupts disabled under relevant rules, or inside other atomic sections. Hard-interrupt and traditional soft-interrupt contexts cannot use ordinary blocking operations. Threaded interrupt or work-queue callbacks may sleep but still obey subsystem ownership and teardown.

Allocation, logging, tracing, copying user memory, and acquiring nested locks can sleep or fault depending on API and flags. Call graphs—not function names—determine admissibility.

### Local controls

Disabling preemption keeps the current task on the local CPU and is useful for CPU-local data under documented rules. It does not stop interrupts and does not exclude remote CPUs. Disabling local interrupts prevents selected local interrupt handlers but still does not exclude remote CPUs.

Saving and restoring prior interrupt state matters: blindly enabling interrupts on exit can violate the caller's state. Nesting must be balanced. Use established APIs so lockdep and real-time transformations can model the relationship.

### Spinlocks and mutexes

A spinlock is suitable when a protected section cannot sleep and expected hold time is short. A mutex permits the waiter to block and is appropriate in schedulable context for longer or contended sections. Neither choice repairs an oversized invariant or inconsistent access discipline.

Linux PREEMPT_RT changes behavior of some lock types, while raw spinlocks preserve strict spinning semantics for low-level contexts. Therefore code that relies on implicit preemption or interrupt effects of a type must consult current lock-type contracts.

### Atomic operations

Atomics provide indivisible operations on one object with specified ordering. They fit independent counters, flags, and carefully designed state machines. A reference counter should use a reference-count API whose overflow and use-after-free semantics match ownership, rather than a generic atomic merely because both hold integers.

Compound check-then-act protocols need atomic read-modify-write, a lock, or a proven lock-free algorithm. Mixing atomic and non-atomic access to the same state requires explicit language and kernel-model justification.

### Memory ordering

Mutual exclusion and memory visibility are related but not identical. Lock acquire and release operations provide documented ordering around the critical section. Lockless publication uses release operations paired with acquire or dependency rules as required by the kernel memory model.

`volatile` does not provide inter-CPU atomicity or synchronization. Barriers do not create ownership or keep objects alive. Architecture-specific observations from one test do not replace portable ordering primitives.

### Lock ordering and deadlock

If code can hold A while acquiring B, record edge `A -> B`. An acquisition graph must remain acyclic for a simple global-order proof. Separate instances may share one lock class, and callbacks can introduce hidden edges.

AB-BA deadlock occurs when one path holds A waiting for B while another holds B waiting for A. Interrupt self-deadlock is a special case: process code holds a lock, an interrupt preempts it, and the handler tries the same lock. Lockdep models classes and dependencies to discover many invalid orders.

### Reader-writer and sequence techniques

Reader-writer locks permit concurrent readers but can increase cache traffic and starve one side depending on semantics. Sequence counters let readers retry when a writer overlaps. Writers require serialization, and readers must not follow pointers that can be invalidated without a separate lifetime protocol.

Sequence techniques suit small, repeatable snapshots. An unbounded reader retry is problematic under continuous writers or real-time constraints. Copying data during a read attempt must not cause irreversible side effects.

### RCU and lifetime

Read-copy-update separates read-side access from update and reclamation. An updater publishes a replacement or removes reachability, then waits for an appropriate grace period before freeing prior state. Exact read-side and update APIs depend on the RCU flavor and context.

RCU does not automatically serialize writers, make every operation atomic, or protect an object after a pointer escapes the read-side lifetime. Reference counts can extend ownership after safe acquisition; they do not alone close new acquisition during teardown.

### Teardown protocol

Robust teardown closes new admission, disables external producers, removes discoverability, synchronizes interrupts and callbacks, cancels timers and deferred work, waits for grace periods or references, and frees only after all paths are quiescent.

Order matters. Removing a list entry before disabling a device may let an interrupt reinsert or access it. Dropping the last reference while a callback can acquire a new one is unsafe. Model every asynchronous producer.

### Contention and scalability

Measure hold time, wait time, acquisitions, contention, handoff, cache movement, interrupt latency, and protected work. Lockstat and tracing can help under documented configuration. Observer overhead and changed timing remain limitations.

Reduce contention by shrinking invariants, partitioning by CPU or object, batching, using read-mostly techniques, or changing ownership. More locks improve concurrency only if their order and cross-object invariants remain understandable.

### Verification tools

Lockdep checks runtime dependency classes and state rules along executed paths. KCSAN samples and delays accesses to detect data races under its model. Assertions catch state violations. Static analysis, sanitizers, stress, fault injection, and model checking cover different failure classes.

A clean run proves only that no modeled violation was detected in covered executions. Disablement, annotation, sampling, architecture, workload, and configuration belong in the evidence record.

### Security and assurance

Synchronization faults can become memory corruption, information leaks, denial of service, and confused authority. Debug traces and lock owner information can themselves be sensitive. Production diagnostics require access and retention controls.

Real-time and safety review bounds critical-section and interrupt-disabled duration, contention, priority inversion, retries, and teardown. Named maintainers and assurance owners must review residual risks; this chapter claims no certification.

## Definitions and Notation

For shared object `O`, let `I(O)` be its invariant, `C(O)` its accessor contexts, `P(O)` its access protocol, and `L(O)` its lifetime protocol. Let lock classes be vertices `V` and nested acquisitions be directed edges `E`; a simple global lock-order proof requires graph `G=(V,E)` to be acyclic.

Let `H(l)` be the maximum hold time of lock class `l`, `W(l)` an observed or analyzed wait, and `R(O)` the set of outstanding references. These quantities need workload and platform assumptions; an observed maximum is not a bound.

Safety properties include mutual exclusion or allowed reader concurrency, invariant restoration before publication, context admissibility, acyclic nesting, matching memory order, and reclamation only after `R(O)` and asynchronous reachability are closed.

## Mechanisms, Invariants, or Proof Structure

A critical-section proof can proceed in eight steps:

1. Define the shared object and exact invariant.
2. Enumerate every accessor and concurrent or preempting context.
3. Choose a protocol admissible in their intersection or split work across contexts.
4. Prove entry, mutation, publication, and exit preserve the invariant and ordering.
5. Add each nested acquisition to a global lock-class graph and reject cycles.
6. Prove progress under contention, preemption, interrupts, cancellation, and failure.
7. Define admission closure, reference acquisition, grace periods, callback synchronization, and reclamation.
8. Test with multiple tools and preserve configuration and coverage limitations.

The executable graph check illustrates how one new dependency can invalidate an otherwise acyclic lock order.

<!-- bijux-verify: {"id":"toy-lock-order-cycle","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"base-order=acyclic\ncandidate-order=cycle\ncycle=A->B->C->A\n","stderr":""}} -->
```python
def find_cycle(edges):
    graph = {}
    for source, target in edges:
        graph.setdefault(source, []).append(target)
        graph.setdefault(target, [])
    state, stack = {}, []

    def visit(node):
        if state.get(node) == "visiting":
            start = stack.index(node)
            return stack[start:] + [node]
        if state.get(node) == "done":
            return None
        state[node] = "visiting"
        stack.append(node)
        for target in graph[node]:
            cycle = visit(target)
            if cycle:
                return cycle
        stack.pop()
        state[node] = "done"
        return None

    for node in graph:
        cycle = visit(node)
        if cycle:
            return cycle
    return None

base = [("A", "B"), ("B", "C")]
candidate = base + [("C", "A")]
cycle = find_cycle(candidate)
print("base-order=cycle" if find_cycle(base) else "base-order=acyclic")
print("candidate-order=cycle" if cycle else "candidate-order=acyclic")
print("cycle=" + "->".join(cycle))
```

The toy checks a static three-class graph. It does not model trylocks, conditional edges, IRQ state, runtime instances, recursive acquisition, memory ordering, or kernel lockdep.

## Alternatives and Trade-Offs

- Coarse locks simplify invariants but serialize independent work.
- Fine-grained locks improve potential concurrency while expanding ordering and lifetime proofs.
- Spinlocks avoid scheduling in short atomic sections but waste CPU and forbid sleep.
- Mutexes support blocking and priority protocols but require schedulable context.
- Per-CPU ownership reduces sharing but needs migration, aggregation, and hotplug protocols.
- Reader-writer locking helps read concurrency but can increase overhead and starvation risk.
- Sequence counters make readers cheap but require retry-safe data and separate pointer lifetime.
- RCU scales read-mostly access but defers reclamation and complicates update and teardown.
- Lock-free atomics avoid mutex ownership while increasing memory-order, progress, and reclamation complexity.

## Failure Modes and Misconceptions

1. **“A critical section is whatever lies between lock calls.”** The protected invariant and access set define it.
2. **“Only writers need locking.”** Readers can see torn compound state or stale lifetime.
3. **“Interrupts disabled means no concurrency.”** Remote CPUs and stronger interrupt contexts remain.
4. **“Preemption disabled is an SMP lock.”** It constrains only local task replacement.
5. **“Spinlocks are always literal spinning.”** Configuration-specific semantics, including PREEMPT_RT, matter.
6. **“Atomic fields make the structure atomic.”** Cross-field invariants still need a protocol.
7. **“Volatile is synchronization.”** It does not supply required atomicity or inter-CPU ordering.
8. **“A barrier fixes lifetime.”** Ordering cannot keep freed storage alive.
9. **“Removing from a list permits immediate free.”** Prior readers and callbacks may retain references.
10. **“Reference count closes teardown.”** New acquisition must also be prevented.
11. **“Each pairwise order looks safe.”** The global graph can contain a longer cycle.
12. **“Read-side retry is always cheap.”** writers can cause unbounded retry and latency.
13. **“Lockdep found nothing, so no deadlock exists.”** Only covered paths and modeled dependencies were checked.
14. **“Stress proves race freedom.”** Rare and unmodeled schedules remain.

## Worked Examples

### Example 1

A queue maintains linked nodes and count. Protecting only list pointers lets a lockless counter reader observe disagreement. Put both fields under one invariant or publish a snapshot with a proven protocol.

### Example 2

Process code holds lock L when its device interrupt fires locally and tries L. Local IRQ-safe locking around the process path prevents self-deadlock while the spinlock excludes remote CPUs.

### Example 3

Preemption is disabled around a per-CPU counter. A hard interrupt also updates it and loses an increment. The declared concurrency domain omitted the interrupt; add interrupt-safe access or separate counters.

### Example 4

Code allocates with a potentially sleeping mode while holding a spinlock. Memory pressure blocks it, violating context. Allocate before entry, use an admissible nonblocking allocation with handled failure, or redesign ownership.

### Example 5

Path one acquires A then B; callback path acquires B then C; teardown acquires C then A. No adjacent pair duplicates, yet the global cycle A-B-C-A permits deadlock.

### Example 6

A sequence-counter reader copies scalar geometry and retries if a writer overlapped. Extending it to dereference a replaceable pointer is unsafe unless RCU, reference acquisition, or another lifetime protocol protects the pointee.

### Example 7

An RCU updater removes a node and frees it immediately. A preexisting reader still holds the pointer. Waiting for the correct grace period before free closes this lifetime gap.

### Example 8

A refcounted callback object sets `closing`, disables registration, synchronizes callbacks, and waits for existing references. Waiting for count zero without closing registration could race forever or free before a new acquisition.

### Example 9

Lockstat shows a global lock's wait tail rises with CPU count. Partitioning state per device reduces contention, but cross-device transactions now require an explicit order and rollback invariant.

### Example 10

Lockdep passes, while KCSAN reports an unprotected diagnostic reader. The tools cover different properties: ordering of observed locks versus sampled conflicting memory accesses. Both findings update the proof.

## Cross-Program Connections

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops mutual exclusion, atomics, memory models, progress, and reclamation. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains atomic instructions, caches, interrupts, and ordering.

[Security Engineering](../../25-security-engineering/ROADMAP.md) frames races as integrity, confidentiality, and availability risks. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies hazard analysis, timing budgets, evidence, and assurance.

Within this program, [OS-022](../ROADMAP.md), [OS-023](../ROADMAP.md), [OS-024](../ROADMAP.md), and [OS-025](../ROADMAP.md) deepen lock contexts, blocking primitives, deadlock, and lock-free synchronization.

## References

- Linux Kernel documentation, [Unreliable Guide To Locking](https://docs.kernel.org/kernel-hacking/locking.html), current page checked 2026-09-04. User, interrupt, and soft-interrupt contexts, locks, reference counts, callbacks, and deadlocks.
- Linux Kernel documentation, [Lock Types and Their Rules](https://docs.kernel.org/locking/locktypes.html), current page checked 2026-09-04. Lock categories, owner semantics, context constraints, local locks, and PREEMPT_RT differences.
- Linux Kernel documentation, [Linux Kernel Memory Barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), current page checked 2026-09-04. Compiler and CPU ordering, locks, atomics, multicopy effects, and minimum guarantees.
- Linux Kernel documentation, [Lesson 1: Spin Locks](https://docs.kernel.org/locking/spinlocks.html), current page checked 2026-09-04. Spinlock use, interrupt state, reader-writer variants, and compiler behavior.
- Linux Kernel documentation, [Atomic Types](https://docs.kernel.org/core-api/wrappers/atomic_t.html), current page checked 2026-09-04. Atomic operations, ordering variants, non-RMW access, signed arithmetic, and API cautions.
- Linux Kernel documentation, [Lockdep Design](https://docs.kernel.org/locking/lockdep-design.html), current page checked 2026-09-04. Lock classes, dependency chains, state usage, recursion, annotations, and validation model.
- Linux Kernel documentation, [Lock Statistics](https://docs.kernel.org/locking/lockstat.html), current page checked 2026-09-04. Acquisition, contention, wait and hold timing, call sites, configuration, and interpretation.
- Linux Kernel documentation, [KCSAN](https://docs.kernel.org/dev-tools/kcsan.html), current page checked 2026-09-04. Sampling-based race detection, watchpoints, memory model, assertions, configuration, and limitations.
- Linux Kernel documentation, [What Is RCU?](https://docs.kernel.org/RCU/whatisRCU.html), current page checked 2026-09-04. Read-side primitives, publication, grace periods, update, and reclamation.
- Linux Kernel documentation, [Sequence Counters and Sequential Locks](https://docs.kernel.org/locking/seqlock.html), current page checked 2026-09-04. Writer serialization, reader retry, pointer hazards, lock association, and latch variants.
- Linux Kernel documentation, [refcount_t API Compared to atomic_t](https://docs.kernel.org/core-api/refcount-vs-atomic.html), current page checked 2026-09-04. Reference-count ordering, saturation, increment and decrement semantics, and differences from general atomics.
- Linux Kernel documentation, [Generic Mutex Subsystem](https://docs.kernel.org/locking/mutex-design.html), current page checked 2026-09-04. Ownership, fast and slow paths, optimistic spinning, implementation, and API constraints.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching lock invariants, interrupt masking, sleep and wakeup, process tables, buffer cache, and multicore races.

## Exercises

### Exercise 1

Audit a device queue accessed by syscall, hard interrupt, work queue, debug reader, and teardown. Define invariant, context matrix, primitive, interrupt rules, memory order, and lifetime sequence.

### Exercise 2

Build a lock-class graph from six nested paths, find cycles, and redesign ownership or acquisition order without using trylock as an unexplained escape.

### Exercise 3

Compare spinlock, mutex, per-CPU state, atomic state machine, seqlock, and RCU for a read-mostly routing table with occasional replacement and pointer traversal.

### Exercise 4

Design a verification campaign combining lockdep, KCSAN, lockstat, assertions, stress, fault injection, and configuration variants. State what each result does not prove.

### Exercise 5

Construct an assurance review for a kernel critical section on a real-time safety-relevant path. Cover bounds, interrupts, configuration, failure, evidence, and human judgment.

## Answers to the Exercises

### Answer 1

Let the invariant require list integrity, count agreement, unique request ownership, and no callback after close. Syscall and work-queue contexts may sleep outside the queue spin section; hard interrupt cannot. Debug reads either take the same compatible lock or consume a separately published snapshot. Teardown is a writer and lifetime owner.

Use an IRQ-safe spin protocol for the small list/count mutation shared with the device interrupt, saving prior interrupt state in process context. Move allocation, copying, and blocking outside. Lock release publishes changes. Teardown closes admission, disables and synchronizes the device interrupt, cancels work, removes queue reachability under the lock, waits for readers and references, verifies empty ownership, then frees. Test error and partial-initialization paths.

### Answer 2

Represent each held-then-acquired pair as a directed class edge and run cycle detection over the complete graph, including callbacks and teardown. For a cycle A-B-C-A, choose one durable global order, split an operation so it releases before crossing ownership domains, combine state under one owner, or use message passing. Update every path and assert ranks where practical.

Trylock can avoid waiting in one execution but needs a bounded retry, rollback, and progress proof; otherwise it changes deadlock into livelock or lost work. Dynamic lock sets require canonical ordering by stable key plus rules for object removal and key reuse.

### Answer 3

A mutex fits sleepable readers and writers but serializes all. A spinlock fits only short nonblocking contexts. Per-CPU copies improve local reads but require aggregation, update propagation, migration, and hotplug. One atomic cannot represent a traversable table; a complex atomic state machine needs safe reclamation.

A seqlock fits small copyable scalar snapshots, not ordinary pointer traversal without lifetime help. RCU fits frequent traversal and rare replacement: readers use the correct read-side region, writers serialize modifications, publish a new table, remove old reachability, and reclaim after a grace period. If callers retain entries beyond the read region, add safe reference acquisition. Select from measured workload and context requirements.

### Answer 4

Run lockdep with broad call-path and IRQ-state coverage to detect modeled dependency and usage violations; it cannot cover unexecuted paths or all non-lock races. Run KCSAN across stress and fault workloads for sampled conflicting accesses; a clean sample is not a proof. Use assertions for list, count, ownership, state, and lifetime invariants; assertions cover only chosen points.

Use lockstat and tracing for contention and hold-time distributions, accounting for observer effects. Inject allocation, timeout, interrupt, cancellation, hotplug, and teardown faults. Test SMP, uniprocessor, preemptible, real-time, debug, and production-relevant configurations. Preserve versions, config, seeds, raw logs, loss, and negative results. Static review and model checking complement runtime coverage.

### Answer 5

State the protected invariant, every task and interrupt context, maximum acquisition frequency, hold work, nesting, and blocking dependency. Use a primitive with documented semantics for the deployed preemption and real-time configuration. Bound interrupt-disabled, preemption-disabled, lock hold, contention, donation, retry, and cache-interference time under admitted load.

Define overload, stuck device, CPU loss, callback after close, partial initialization, diagnostic failure, and safe-state behavior. Combine static order analysis, kernel debug tools, stress, fault injection, platform tracing, and independent timing measurement with analytical bounds; observed maxima remain samples. Named kernel, driver, concurrency, real-time, platform, security, safety, independent-verification, and acceptance owners review assumptions and residual risk. This chapter claims no certification.
