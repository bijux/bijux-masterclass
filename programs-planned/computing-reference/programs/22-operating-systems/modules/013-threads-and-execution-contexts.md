---
module_id: OS-013
program: Operating Systems
level: 1
module_number: 13
title: Threads and Execution Contexts
status: complete
last_verified: 2026-09-04
---

# Threads and Execution Contexts

## One-Page Review

### Governing question

How should an operating system and its programs represent multiple execution streams that share resources while retaining distinct stacks, registers, scheduling, signals, and lifecycle?

### Essential definitions

- A **thread** is a schedulable execution stream with its own register state, stack, scheduling attributes, signal mask, and thread-local state inside a process resource domain.
- An **execution context** is the state and constraints under which code currently runs, such as user thread, kernel process context, hard interrupt, or deferred interrupt work.
- A **thread control block (TCB)** is implementation state used to identify and manage one thread, including links to process-wide resources and thread-local data.
- **Thread-local storage (TLS)** gives each thread a distinct instance of selected variables while code and ordinary process memory remain shared.
- A **joinable thread** retains termination state until another thread joins it; a **detached thread** releases that state automatically and cannot be joined.
- **Cancellation** is a protocol for requesting thread termination at defined points or asynchronously under stricter hazards; it is not safe arbitrary destruction.
- A **data race** occurs when conflicting accesses to one memory location are concurrent without the language's required synchronization, with at least one write.

### Central model, mechanism, or theorem

Model one thread as private execution state plus references to shared domains:

`thread = registers + stack + scheduler_state + signal_mask + TLS + shared_process_refs`.

Correctness requires two simultaneous contracts. The sharing contract says which objects can be accessed by multiple threads and which synchronization orders conflicting operations. The context contract says whether the current path may sleep, block, allocate, fault, migrate, or call a particular API. Code safe in a normal thread can be invalid in a signal handler or interrupt.

### Critical invariants

- Each live thread has a valid unique lifetime identity, kernel scheduling state, stack, register context, and references to every shared resource it may use.
- Thread publication occurs only after start routine, argument, TLS, signal mask, scheduling attributes, and stack are initialized.
- Shared mutable state follows a synchronization protocol that establishes both mutual exclusion or atomicity and required memory visibility.
- Join or detach consumes termination ownership exactly once; thread identifiers are not used after their lifetime ends.
- Cancellation and abnormal exits release owned locks and resources only through code designed for every permitted cancellation point.
- Signal delivery selects an eligible live thread and constructs handler state without confusing async-signal-safe execution with ordinary thread safety.
- Kernel code obeys its current execution-context restrictions, including preemption, interrupt, migration, and sleep rules.

### Common failures

Common mistakes are assuming threads execute in creation order, passing a pointer to expired stack data, allocating too-small stacks without guards, treating TLS as synchronized shared state, using a thread ID after join, leaking joinable termination state, detaching and then joining, canceling while invariants are half-updated, calling thread-safe but non-async-signal-safe functions in a handler, holding a spinlock while sleeping, using local interrupt masking as an SMP lock, and interpreting a race-free run as proof the code has no data race.

### Compact example

A process creates a joinable worker after fully initializing a heap-owned request. The worker has its own stack, registers, signal mask, and TLS error state, but shares the request queue and address space. A mutex-and-condition protocol publishes work and establishes visibility. Shutdown sets a protected stop flag, wakes the worker, joins it, collects its result, then frees the request and synchronization objects. A signal thread uses synchronous signal waiting rather than performing complex work in an asynchronous handler. Kernel callbacks that feed the queue use context-appropriate nonblocking paths and defer sleepable work.

### Connections

[OS-011](011-processes-and-address-spaces.md) defines the shared process resource graph, and [OS-012](012-process-creation-and-program-loading.md) defines creation and exec. [OS-014](../ROADMAP.md) develops context switching, [OS-015](../ROADMAP.md) wait queues, and [OS-021](../ROADMAP.md) kernel critical sections. Language memory models belong to [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md).

## Governing Question

Threads make concurrency cheap because instruction streams share an address space and other process resources. That same sharing removes the default memory barrier supplied by separate processes. One thread can observe, mutate, unmap, close, or free state another thread is using. The scheduler may run the child before the creator returns, migrate it between CPUs, preempt it inside a critical sequence, or never choose the interleaving a test expected.

“Execution context” also extends below user threads. A syscall runs on behalf of a thread in kernel process context and may often sleep. A hard interrupt can preempt it and cannot use ordinary blocking operations. Deferred work may run in a soft-interrupt, dedicated kernel thread, or work-queue context with different rules. The same function can be correct in one and invalid in another.

The governing question is how to state private state, shared state, ordering, lifetime, and context restrictions precisely enough that creation, execution, cancellation, signaling, exit, and cleanup remain correct under every allowed schedule.

## Why This Matters

Thread bugs are often timing dependent. An argument stored on a creator's stack can become invalid before the worker reads it. An unsynchronized increment can lose updates even when each machine instruction appears ordinary. A thread can exit while another retains its identifier or object pointer. Cancellation can leave a mutex locked forever.

Performance also depends on representation. Threads avoid process-level isolation and copying, but shared cache lines bounce among CPUs, locks serialize, stacks consume virtual and committed memory, and oversubscription adds scheduling and context-switch cost. Affinity can improve locality while harming load balance and resilience.

Kernel context mistakes have privileged consequences. Sleeping in atomic context, allocating with the wrong policy, taking locks in interrupt-inverted order, or freeing callback state before synchronization can deadlock or corrupt the entire machine. Context belongs in API design, not tribal knowledge.

## Prerequisites and Retrieval

Recall from [OS-004](004-interrupts-and-exceptions.md) that interrupts have restricted context and nested priority. Recall from [OS-007](007-kernel-data-structures.md) that reachability and ownership differ. Recall from [OS-011](011-processes-and-address-spaces.md) that threads share selected resource domains. You should understand stacks, registers, calls, atomics, mutexes, condition variables, and happens-before.

Retrieve these distinctions:

- concurrency means overlapping lifetimes; parallelism means simultaneous execution;
- thread safety is not async-signal safety and neither implies interrupt safety;
- a mutex protects a declared invariant, not “the function” in the abstract;
- atomicity of one variable does not order unrelated state unless the memory model says so;
- thread ID, kernel task ID, and application worker ID are different namespaces;
- thread termination, join, detach, and object reclamation are different events;
- preemption disabling, migration disabling, local interrupt masking, and SMP exclusion provide different guarantees.

## Learning Objectives

After completing this module, you should be able to:

- identify thread-private and process-shared state under POSIX-like and kernel models;
- explain user-level, one-to-one, many-to-one, and many-to-many thread implementation trade-offs;
- design thread creation, publication, return, join, detach, and final reclamation;
- select stack size, guard, TLS, signal mask, scheduling, and affinity policy;
- construct and diagnose a lost-update interleaving and state the needed happens-before edge;
- distinguish process-directed and thread-directed signals and safe handler behavior;
- reason about deferred and asynchronous cancellation with cleanup obligations;
- classify kernel process, hard-interrupt, soft/deferred, and nonpreemptible contexts;
- design stress, model, sanitizer, and performance evidence for threaded systems;
- identify real-time or safety claims requiring accountable human review.

## Core Exposition

### Private execution state and shared resources

Each thread needs a program counter, general and control registers, stack pointer, user stack, kernel stack while in the kernel, scheduler entity, accounting, signal mask, TLS base, and implementation bookkeeping. These are private in the sense that another thread does not execute with the same saved state, though debuggers and the kernel can inspect them under policy.

Threads in one POSIX process share the virtual address space, program code, globals, heap, mappings, process ID, open descriptor domain, filesystem context, signal dispositions, and many credentials and limits. Some kernel implementations store per-task versions while the runtime maintains process-wide semantics. Use the documented interface rather than assuming layout.

The sharing table is the basis of design. A variable being on one thread's stack does not make a pointer to it private. TLS gives distinct instances, but any pointer published to another thread creates shared access. A file descriptor number shared through one table can be closed or reused by a peer.

### Thread implementation models

In a one-to-one model, each user thread maps to a kernel-schedulable entity. Blocking one thread need not block peers, CPUs can run several in parallel, and the kernel schedules each directly. Creation, kernel stacks, task metadata, and context switches consume resources.

Many-to-one user threading schedules several user contexts on one kernel thread. Switching can be cheap and application-specific, but a blocking syscall can stop all unless integrated with nonblocking I/O, and there is no true multicore parallelism for that kernel entity.

Many-to-many systems multiplex user tasks over a pool of kernel threads. Language runtimes use related ideas for goroutines, fibers, or async tasks. They gain flexible scheduling and cheap logical tasks but must coordinate blocking calls, TLS expectations, signals, stack growth, debuggers, profiling, and scheduler interactions. A language task is not automatically an OS thread.

### Creation and publication

Initialize the argument object and every synchronization primitive before creation makes the child eligible to run. POSIX does not promise whether creator or child runs next after successful creation. Passing an address of loop-local or reusable stack storage is unsafe unless lifetime and synchronization extend through the worker's final access.

Thread attributes include detach state, stack address and size, guard size, scheduling policy and parameters, inheritance, affinity where supported, and other implementation settings. Creation can fail because of resource or policy limits; the output thread identifier may be unspecified on failure.

Publication needs a happens-before relation. The create operation commonly establishes visibility of prior initialization to the new thread under the API's memory model, while later work queues require their own mutex, atomic, semaphore, or channel protocol. A sleep or “likely scheduling delay” is never synchronization.

### Stacks and guards

Each thread needs enough stack for calls, locals, saved registers, signal frames, library code, and worst credible recursion. Reserving a large virtual range may be cheap, but committed memory and address-space limits still matter across thousands of threads. Small fixed stacks improve density while increasing overflow risk.

A guard region catches accesses that cross into an unmapped boundary, but it does not prove every overflow will hit before corrupting another object. Stack-clash defenses, compiler probes, alternate signal stacks, and bounded recursion address different failure modes.

User-supplied stacks transfer alignment, mapping, lifetime, guard, and reuse obligations to the application. The stack cannot be freed when the start routine returns if the thread library still needs termination state. Join or detach semantics tell when final resources become reclaimable.

### Thread-local storage

TLS supports per-thread variables such as error state, allocators, random generators, caches, and runtime control blocks. The compiler and loader calculate per-module layouts and use a thread pointer or descriptor to address the current instance. Dynamic library loading can require TLS layout extensions.

Thread-specific keys offer runtime-indexed values and optional destructors. A destructor may run during thread exit in repeated passes under implementation rules if it stores values again. Key deletion does not necessarily invoke destructors for live thread values.

TLS prevents accidental sharing of the variable instance; it does not make referenced objects private or eliminate initialization and teardown. Large TLS blocks multiply memory by thread count. Caches stored per thread can strand resources and complicate global accounting.

### Shared memory and data races

Consider two threads incrementing `x` through read-compute-write. Both can read 0, each compute 1, and both write 1. Every individual access completes, yet one update disappears. A mutex can serialize the compound invariant; a suitable atomic read-modify-write can implement this particular counter.

The programming-language memory model defines a data race and its consequences. In languages such as C and C++, a data race on ordinary memory yields undefined behavior, so reasoning only from an imagined hardware interleaving is insufficient. Compiler transformations and weak hardware ordering participate.

Synchronization establishes ordering and visibility. Mutex unlock-to-lock, thread creation and join, condition-variable protocols, and atomics with appropriate orders supply particular happens-before edges. Marking a variable volatile does not create them. Protect related fields under one invariant or a proven publication protocol.

### Blocking and futex-style synchronization

Efficient locks often attempt an uncontended operation entirely in user space and invoke the kernel only when waiting or waking is required. Linux futexes provide an atomic compare-and-block primitive around a user word; the higher-level library supplies ownership, queue, priority, timeout, and robustness semantics.

Waiters must check a predicate in a loop under the associated synchronization. Wakeups can be spurious, signals or timeouts can intervene, and another thread can consume the condition first. A wake operation is a hint to reevaluate, not transfer of an arbitrary object unless the protocol defines it.

Blocking while holding unrelated locks can deadlock and enlarge latency. A lock implementation also needs policy for fairness, priority inversion, owner death, cancellation, and process-shared memory. The cheapest fast path is not the entire correctness contract.

### Join, detach, and lifetime

A joinable thread retains a result and implementation resources after termination until exactly one successful join consumes them. Joining also provides a synchronization edge: writes performed by the completed thread become observable according to the API. Failing to join or detach accumulates retained state.

A detached thread releases its retained termination resources automatically. It cannot later be joined, and detaching twice or after another ownership action is erroneous. Detach does not guarantee the thread has stopped; application objects still require an independent completion and lifetime protocol.

Thread identifiers can be reused after a lifetime ends. Store application generation or a stable owned object if late messages must distinguish workers. Never treat a pthread identifier as a permanent numeric handle or compare it outside the API's defined operations.

### Cancellation and cleanup

Deferred cancellation is acted on at defined cancellation points when enabled, allowing code to bracket invariants and install cleanup handlers. Asynchronous cancellation can arrive at far more instructions and makes most resource manipulation unsafe unless the code and runtime are explicitly designed for it.

Cleanup handlers commonly unlock mutexes, release buffers, or restore state. They execute in a defined stack order for cancellation and some exit paths, but normal return from the start function can differ. Pair acquisition and cleanup registration so no cancellation window leaks or double releases.

Cancellation is cooperative policy, not process-level containment. A thread may disable it indefinitely, block in a noncancellation operation, or hold shared state that cannot be abandoned. Structured shutdown through flags, queues, stop tokens, and join is often easier to reason about.

### Signals and asynchronous handlers

Signal disposition is commonly process-wide while each thread has its own signal mask. A thread-directed signal targets a particular thread; a process-directed signal can be delivered to an eligible thread. Synchronous hardware exceptions generally concern the faulting execution context.

An asynchronous handler interrupts code at an arbitrary point and can observe library locks held. A function can be thread-safe under ordinary calls yet not async-signal-safe when reentered from a handler. Handlers should perform only specified safe operations, save and restore error state as required, and communicate minimal facts to normal context.

A dedicated signal-handling thread can block selected signals in all workers and synchronously wait for them, converting asynchronous delivery into ordinary thread logic. Fatal synchronous faults and some platform signals do not fit this pattern. Signal masks must be established before worker creation so inheritance is deliberate.

### Scheduling, affinity, and oversubscription

Kernel schedulers select runnable threads according to policy, priority, fairness, deadlines, affinity, cgroups, and CPU availability. A created thread is not promised immediate execution. Priority changes require authority and can starve lower work; real-time policies demand bounded blocking and admission analysis.

Affinity restricts eligible CPUs and can preserve cache or NUMA locality. The effective set is the intersection with online CPUs and administrative restrictions. Pinning too narrowly creates idle capacity elsewhere, hotspots, brittle hotplug behavior, and interference among co-located threads.

Oversubscription can hide I/O waits but adds context switching, cache disruption, memory for stacks, and scheduling latency. Thread count should follow measured workload structure and resource budgets, not CPU count alone. Runtime-managed task pools separate logical concurrency from kernel-thread count.

### Kernel execution contexts

Process context executes on behalf of a task and generally has a task identity and kernel stack. It may sleep only when preemption, locks, interrupt state, and API rules allow. A syscall, page fault, or kernel thread can run in process context, but holding a spinlock or disabling interrupts makes a region atomic with respect to sleeping.

Hard-interrupt context is entered asynchronously and cannot sleep. It needs bounded work, context-safe allocation, and locks compatible with interrupt nesting. Local interrupt disable prevents selected local delivery; it does not exclude other CPUs.

Deferred interrupt mechanisms vary. Some run in atomic soft-interrupt context; threaded interrupts and work queues run in schedulable thread context. Naming work “deferred” does not tell whether it may sleep. APIs should encode or document context, and callbacks must not guess based on current testing.

Preemption disabling prevents involuntary task switch on the local CPU under its scope; migration disabling keeps the task on one CPU but may not exclude preemption; CPU-local data access has matching rules. These mechanisms are not general locks for shared SMP state.

### Reentrancy and callbacks

Code can be reentered by another thread, a signal, an interrupt, a callback invoked while holding a lock, or recursion through allocation and I/O. Each route has different state and context. “Thread-safe” describes only the routes and contract actually reviewed.

Avoid hidden global scratch state, implicit current-thread assumptions, callbacks under internal locks, and destructor paths that invoke arbitrary code. Define whether a callback may block, unregister itself, call back into the subsystem, or run after cancellation begins.

Lifetime must cover code and data across callback dispatch. Unregistering prevents future selection but may need synchronization to wait for callbacks already in flight. This mirrors thread join at a subsystem boundary.

### Testing and evidence

Use race detectors and sanitizers for supported code paths, static lock analysis, deterministic schedulers, model checking for small protocols, randomized stress, and fault injection. Vary CPU count, affinity, priorities, signals, cancellation, memory pressure, timeouts, and shutdown timing.

Tests must force adversarial interleavings rather than rely on sleeps. Insert barriers at protocol boundaries, repeat creation and join, reuse identifiers and memory, cancel at every permitted point, and exercise failure after each acquisition. A test that passes once may simply have serialized accidentally.

Measure throughput, latency distributions, runnable delay, lock wait, context switches, migrations, cache misses, stack high-water marks, retained join state, and per-thread memory. Record compiler, language memory model, runtime, kernel, topology, affinity, workload, and instrumentation overhead.

## Definitions and Notation

Let thread `T_i` have private state `P_i` and references to shared state `S`. An operation `a` in `T_i` happens-before operation `b` in `T_j`, written `a →hb b`, when program order and defined synchronization compose to order them. Wall-clock order observed in one run does not alone establish `→hb`.

Two operations conflict when they access the same memory location, at least one writes, and they are not both compatible atomics. A data race exists when conflicting operations in different threads are not ordered by happens-before under the language contract.

For lifecycle, define states `new`, `live`, `terminated-joinable`, `joined`, and `detached`. A joinable thread follows

`new → live → terminated-joinable → joined`,

while a detached thread follows `new → live → detached` with implementation resources released at termination. Detach can occur while live or after termination within the API's rules, but exactly one reclamation owner remains.

Let context capabilities be `C(ctx) = {may_sleep, may_fault, may_allocate(mode), may_migrate, irq_state, preempt_state}`. Calling operation `op` is admissible only when its requirements are a subset of `C(ctx)` and its lock and reentrancy preconditions hold.

## Mechanisms, Invariants, or Proof Structure

Review threads and execution contexts through eight obligations.

**Identity integrity.** User thread IDs, kernel task IDs, application worker generations, and process membership identify live contexts without reuse ambiguity.

**State integrity.** Registers, stacks, TLS, scheduler attributes, signal masks, kernel stacks, and shared-resource references are initialized before publication and retained through final use.

**Sharing integrity.** Every shared mutable object has ownership, synchronization, visibility, cancellation, and reclamation rules under the language and OS memory models.

**Context integrity.** Sleep, fault, allocation, lock, preemption, migration, interrupt, signal, and callback restrictions match every call path.

**Lifecycle integrity.** Creation, start, return or exit, cancellation, cleanup, join or detach, identifier reuse, and object release occur in legal order exactly once.

**Scheduling integrity.** Priority, affinity, admission, blocking, wakeup, oversubscription, and migration preserve required fairness or deadline properties within stated bounds.

**Failure integrity.** Resource exhaustion, partial creation, owner death, timeout, signal, cancellation, and shutdown converge on defined states without leaked locks or references.

**Evidence integrity.** Analysis, models, race tools, stress, performance runs, platform behavior, and human review state schedules and properties covered.

The executable model below shows two legal schedules for unsynchronized read-then-write increments.

<!-- bijux-verify: {"id":"toy-thread-interleaving","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"serial-final=2\ninterleaved-final=1\nlost-update=yes\n","stderr":""}} -->
```python
def run_schedule(schedule):
    shared = {"value": 0}
    local = {"a": None, "b": None}
    for thread, operation in schedule:
        if operation == "read":
            local[thread] = shared["value"]
        else:
            shared["value"] = local[thread] + 1
    return shared["value"]


serial = [("a", "read"), ("a", "write"), ("b", "read"), ("b", "write")]
interleaved = [("a", "read"), ("b", "read"), ("a", "write"), ("b", "write")]
serial_final = run_schedule(serial)
interleaved_final = run_schedule(interleaved)
print(f"serial-final={serial_final}")
print(f"interleaved-final={interleaved_final}")
print("lost-update=" + ("yes" if interleaved_final < serial_final else "no"))
```

Passing proves the stated results for two sequential simulations. It does not execute parallel threads or model compiler transformations, atomics, caches, memory ordering, locks, signals, cancellation, kernel contexts, or a real scheduler.

## Alternatives and Trade-Offs

**Processes versus threads.** Processes provide separate address spaces and stronger default containment. Threads communicate through ordinary memory cheaply but share failures and require synchronization.

**Kernel threads versus user tasks.** Kernel-scheduled threads block and run in parallel naturally. User tasks switch cheaply and can encode application scheduling but need integration with blocking, signals, profiling, and CPU pools.

**Joinable versus detached lifecycle.** Joinable threads return results and provide explicit completion synchronization but retain resources until joined. Detached threads self-reclaim but require another way to coordinate application lifetime.

**Cancellation versus cooperative stop.** Cancellation integrates with blocking points and cleanup handlers but creates hidden control flow. Cooperative stop makes boundaries explicit but requires responsive polling or wakeup design.

**Asynchronous handlers versus signal thread.** Handlers react without a dedicated waiter but face severe reentrancy limits. A signal thread enables ordinary logic but does not handle every synchronous or fatal signal.

**Affinity versus scheduler freedom.** Affinity improves locality and isolation when planned. Scheduler freedom improves load balance and adaptation; both need topology-aware measurement.

**Spin versus block.** Spinning avoids sleep and wake overhead for very short waits but consumes CPU and worsens contention. Blocking saves CPU for longer waits but adds scheduler latency and is invalid in atomic context.

## Failure Modes and Misconceptions

1. **“Threads have separate heaps.”** Threads in a process normally share the address space and heap.
2. **“A stack variable is thread-private.”** Publishing its address makes its storage shared and lifetime-sensitive.
3. **“The creator runs until create returns.”** The child can run first under the API contract.
4. **“TLS is synchronization.”** It creates distinct variable instances but does not order shared pointees.
5. **“Atomic loads make a compound operation atomic.”** Read-compute-write needs one atomic operation or larger protocol.
6. **“Volatile prevents data races.”** It does not establish language-level synchronization.
7. **“Thread-safe means signal-safe.”** An asynchronous handler can interrupt the function while internal locks are held.
8. **“Detach stops a thread.”** It changes termination-resource ownership, not execution state.
9. **“Cancellation is immediate cleanup.”** Delivery mode, cancellation points, disabled regions, and handlers determine behavior.
10. **“A returned thread ID remains unique.”** It can be reused after join or detached termination.
11. **“Wake means the waiter owns the condition.”** It must reacquire synchronization and recheck the predicate.
12. **“Process context may always sleep.”** Locks, preemption, interrupt state, and API rules can forbid it.
13. **“Disabling local interrupts excludes other CPUs.”** It only changes eligible delivery on the local CPU.
14. **“Stress passing proves race freedom.”** Untested schedules and compiler behaviors remain.

## Worked Examples

### Example 1

**Question:** A loop creates workers using the address of one loop variable. Why can every worker see the same value?

**Reasoning:** The address names shared reused storage, and workers may read only after the creator has advanced or left scope.

**Conclusion:** Give each worker stable owned argument storage or synchronize access and lifetime.

### Example 2

**Question:** Two increments each read and write an aligned integer. Why can the result be one?

**Reasoning:** Both reads can observe zero before either write, and two writes of one overwrite each other.

**Conclusion:** Alignment and individually atomic accesses do not make the compound increment atomic.

### Example 3

**Question:** A terminated joinable thread no longer executes. Why does failing to join matter?

**Reasoning:** Its result and implementation termination resources remain reserved for a joiner.

**Conclusion:** Every created thread needs exactly one join-or-detach ownership decision.

### Example 4

**Question:** A detached worker signals completion, and the owner immediately frees its object. Is detach sufficient?

**Reasoning:** Detach says who reclaims thread metadata, not whether the completion signal is synchronized or all object accesses ended.

**Conclusion:** Use an explicit completion and object-lifetime protocol.

### Example 5

**Question:** A canceled worker holds a mutex when it reaches a cancellation point. What prevents deadlock?

**Reasoning:** A cleanup handler installed immediately after acquisition can restore the invariant and unlock during cancellation.

**Conclusion:** Cancellation-safe regions pair acquisition, cleanup registration, and cancellation state deliberately.

### Example 6

**Question:** A signal handler calls a thread-safe allocator. Why can it deadlock?

**Reasoning:** The signal may interrupt the same thread while that allocator holds an internal lock; ordinary thread safety does not cover asynchronous reentry.

**Conclusion:** Restrict handlers to the specified async-signal-safe subset or use synchronous signal waiting.

### Example 7

**Question:** Pinning eight workers to one CPU improves one benchmark run. Is it generally faster?

**Reasoning:** It may improve cache warmth but also serialize work and create runnable delay while other CPUs idle.

**Conclusion:** Measure locality, load balance, tail latency, and failure behavior under the intended topology.

### Example 8

**Question:** A kernel syscall path holds a spinlock and calls a function documented to sleep. What fails?

**Reasoning:** Scheduling away while holding the spinlock can deadlock waiters and violates atomic-context rules.

**Conclusion:** Move the blocking work, change the lock and invariant, or use a context-safe deferred path.

### Example 9

**Question:** Interrupt code disables local interrupts before editing a global list. Why is that insufficient on SMP?

**Reasoning:** Another CPU can enter and mutate the list concurrently.

**Conclusion:** Use synchronization that covers all writers, combined with interrupt control when local nesting also matters.

### Example 10

**Question:** A safety controller's thread schedule meets deadlines in stress tests. Does that prove the worst case?

**Reasoning:** Untested interleavings, interrupt load, priority inversion, cache interference, cancellation, faults, and hardware variation remain.

**Conclusion:** Named real-time, concurrency, safety, and platform reviewers must assess bounds and residual risk; this module claims no certification.

## Cross-Program Connections

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops data races, happens-before, locks, atomics, condition variables, cancellation, and parallel algorithms. This module adds OS task identity, signal, scheduling, stack, and kernel-context constraints.

[Programming Languages: Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) connects thread APIs, unsafe memory, ownership, FFI, and runtime behavior. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains cache coherence, memory ordering, atomic instructions, interrupts, and CPU topology.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames bounded concurrency, capacity, fault containment, and assurance. Successors [OS-014](../ROADMAP.md), [OS-015](../ROADMAP.md), [OS-016](../ROADMAP.md), and [OS-021](../ROADMAP.md) deepen switching, wait states, CPU scheduling, and kernel synchronization.

## References

- Linux man-pages project, [pthreads(7)](https://man7.org/linux/man-pages/man7/pthreads.7.html), current page checked 2026-09-04. POSIX thread shared and private attributes, identifiers, safety, signals, cancellation, and Linux implementation notes.
- Linux man-pages project, [pthread_create(3)](https://man7.org/linux/man-pages/man3/pthread_create.3.html), current page checked 2026-09-04. Start routine, inherited state, scheduling order, attributes, stacks, joinability, limits, and errors.
- Linux man-pages project, [pthread_join(3)](https://man7.org/linux/man-pages/man3/pthread_join.3.html), current page checked 2026-09-04. Termination waiting, result ownership, errors, deadlock, and retained joinable resources.
- Linux man-pages project, [pthread_detach(3)](https://man7.org/linux/man-pages/man3/pthread_detach.3.html), current page checked 2026-09-04. Detached lifecycle, automatic resource release, nonjoinability, and ownership cautions.
- Linux man-pages project, [pthread_cancel(3)](https://man7.org/linux/man-pages/man3/pthread_cancel.3.html), current page checked 2026-09-04. Cancellation request, state, type, points, cleanup, destructors, and join result.
- Linux man-pages project, [pthread_sigmask(3)](https://man7.org/linux/man-pages/man3/pthread_sigmask.3.html), current page checked 2026-09-04. Per-thread masks, inheritance, blocking and unblocking, and synchronous signal waiting.
- Linux man-pages project, [pthread_key_create(3)](https://man7.org/linux/man-pages/man3/pthread_key_create.3.html), current page checked 2026-09-04. Thread-specific keys, values, destructor iterations, deletion, and lifecycle.
- Linux man-pages project, [clone(2)](https://man7.org/linux/man-pages/man2/clone.2.html), current page checked 2026-09-04. Kernel task creation, resource sharing, thread groups, TLS, IDs, parent and child state, and flag constraints.
- Linux man-pages project, [futex(2)](https://man7.org/linux/man-pages/man2/futex.2.html), current page checked 2026-09-04. Compare-and-block semantics, wake operations, shared words, timeouts, and higher-level synchronization role.
- Linux man-pages project, [sched_setaffinity(2)](https://man7.org/linux/man-pages/man2/sched_setaffinity.2.html), current page checked 2026-09-04. Per-thread CPU masks, migration, permissions, administrative intersection, inheritance, and topology effects.
- Linux man-pages project, [signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html), current page checked 2026-09-04. Process- and thread-directed signals, masks, handler frames, synchronous waiting, and interruption.
- Linux Kernel documentation, [Unreliable Guide To Locking](https://docs.kernel.org/kernel-hacking/locking.html), current page checked 2026-09-04. User, hard-interrupt, and soft-interrupt contexts, preemption, locking, reference counting, callbacks, and common deadlocks.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching task state, kernel stacks, scheduling, sleep and wakeup, interrupts, locks, and process resource sharing.

## Exercises

### Exercise 1

Build a private-versus-shared table for POSIX threads covering registers, user and kernel stacks, TLS, signal mask, signal dispositions, address space, descriptors, open descriptions, credentials, working directory, scheduling, and accounting. Explain each lifecycle.

### Exercise 2

Enumerate all order-preserving interleavings of two read-then-write increments at the abstract operation level. Identify final values, conflicting operations, missing happens-before edges, and repairs using a mutex and atomic read-modify-write.

### Exercise 3

Design creation and shutdown for a pool of joinable workers with bounded queues, TLS caches, signals, cancellation-disabled invariant regions, partial creation failure, and repeated restart. Prove resource ownership.

### Exercise 4

Classify a function's admissibility in user thread, asynchronous signal handler, kernel process context, hard interrupt, soft interrupt, threaded interrupt, and work-queue context. Include sleeping, allocation, faults, locks, migration, callbacks, and teardown.

### Exercise 5

Construct an assurance review for a real-time multithreaded controller. Cover scheduling, priorities, affinity, stacks, shared state, signals, cancellation, interrupts, memory ordering, overload, measurement, and named human judgment.

## Answers to the Exercises

### Answer 1

Registers, user stack, kernel stack, TLS, signal mask, thread ID, scheduling state, CPU time, and cancellation state belong to one thread lifetime. Signal dispositions, address space, ordinary mappings, process identity, descriptor table under POSIX semantics, credentials, working directory, and most limits are process-wide. Descriptor entries refer to open descriptions whose offsets and status can be shared even across copied tables.

Some implementation details differ: Linux kernel tasks have individual credential pointers while the threading runtime maintains POSIX-wide changes, and kernel scheduling attributes are per task. Creation initializes private state and acquires shared references before publication. Thread exit releases private execution resources and references; join or detach determines final termination-state reclamation. Process-wide state ends only after the last relevant thread and external reference. API semantics, not field placement, define sharing.

### Answer 2

Each thread preserves its read before its write. The six interleavings are `Ra Wa Rb Wb`, `Ra Rb Wa Wb`, `Ra Rb Wb Wa`, `Rb Wb Ra Wa`, `Rb Ra Wb Wa`, and `Rb Ra Wa Wb`. The two serial schedules finish at two. The four schedules in which both reads precede both writes finish at one because each local computation uses zero.

The reads conflict with the other thread's write, and the writes conflict with each other; no cross-thread happens-before orders them. In a C-like language, ordinary accesses form a data race, so the abstract lost-update schedule is illustrative rather than a complete language execution semantics. A mutex around read-compute-write orders critical sections and protects the counter invariant. An atomic fetch-add performs one indivisible read-modify-write and suits this independent counter, with memory order chosen based on whether it also publishes other state.

### Answer 3

Create the queue, mutex, conditions, stop generation, and stable heap-owned worker records first. Block handled signals before creation so workers inherit the mask. Create workers one at a time in joinable state and record only successful IDs. Each worker initializes TLS, announces readiness under the pool mutex, then loops: wait while the queue is empty and not stopping, acquire one owned item, process it outside the queue lock, publish completion, and periodically drain its TLS cache.

Disable cancellation while queue and ownership invariants are transient; if cancellation is permitted during processing, install cleanup immediately after each acquisition. On partial creation failure, set stop, wake created workers, join all of them, drain owned items, destroy TLS caches and synchronization, then report failure. Normal shutdown closes admission, sets the generation's stop flag, wakes all, joins each worker exactly once, verifies queue and in-flight counts zero, releases thread records, then destroys shared state. Restart allocates a new generation so stale completions cannot join the new pool.

### Answer 4

Describe the function by requirements rather than one label. Ordinary user thread code may block and fault under its library contract; an asynchronous signal handler may call only specified safe operations and cannot take locks possibly held by interrupted code. Kernel process context may sleep and fault only when current locks, preemption, and API rules allow. Hard interrupt cannot sleep or take a lock that an interrupted local path holds without interrupt-safe exclusion.

Soft-interrupt context is typically atomic and can run concurrently on other CPUs; threaded interrupt and work-queue callbacks run in schedulable task context but still obey subsystem locks, teardown, and reentrancy. Allocation mode must match each context. CPU-local access requires migration or preemption guarantees named by its API. A callback callable from several contexts either restricts itself to their intersection or dispatches into separate paths. Unregistration closes new entry and synchronizes every in-flight context before code or data release.

### Answer 5

Define deadline, jitter, safe output, admitted workload, thread roles, and overload behavior. Assign scheduling policies and priorities from response-time analysis; bound every critical section and blocking dependency; use priority inheritance or another reviewed inversion control. Set affinity with CPU, cache, NUMA, interrupt, and hotplug analysis. Measure stack high-water under worst call depth, signal frames, and diagnostics, with guards and margin.

Specify each shared-state invariant and its mutex, atomic, or lock-free proof under the compiler and hardware memory models. Route signals synchronously where possible, avoid uncontrolled asynchronous cancellation, and make shutdown join all ownership. Include interrupt and kernel-thread interference, memory pressure, thermal effects, and fault recovery. Stress and trace deployed hardware without confusing observed maxima with proven bounds. A named real-time analyst, concurrency reviewer, kernel and platform owner, safety authority, independent verifier, and acceptance owner must assess assumptions, evidence, and residual risk. This chapter and sequential interleaving toy claim no external certification.
