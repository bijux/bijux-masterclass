---
module_id: CONPAR-011
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 11
title: Creating and Joining Threads
status: complete
last_verified: 2026-08-29
---

# Creating and Joining Threads

## One-Page Review

### Governing question

What authority, memory-order, result, failure, lifetime, and resource guarantees cross the boundaries of thread start and successful join, and how does every created thread reach one accounted terminal state?

### Essential definitions

- A **thread** is an execution context within a process that has its own instruction state and usually stack while sharing process resources and address space.
- **Creation** allocates or requests a thread and establishes its entry function, attributes, and captured inputs; it may fail before execution begins.
- **Start** makes the thread eligible to run. Language specifications often define a publication edge from actions before start to actions in the new thread.
- A **joinable thread** retains completion state that an authorized participant can join to await termination and usually retrieve a result or failure.
- **Join** waits for a target thread to terminate and, when successful, establishes the API's completion and memory-visibility guarantees.
- A **join handle** is authority to observe and account for a thread's termination; ownership and multiplicity rules are API-specific.
- A **detached thread** cannot subsequently be joined through the detached handle. Detachment changes reclamation and observation, not whether the thread continues.
- A **daemon** or background status may allow process shutdown without waiting; exact semantics are runtime-specific.
- **Publication** makes initialized data visible to another thread through a specified happens-before or synchronizes-with relation.
- **Structured lifetime** requires child threads to finish, fail, or be cancelled within an owning scope rather than silently outliving it.
- **Cooperative cancellation** requests termination and relies on the worker to observe, unwind, and report a terminal outcome safely.

### Central model, mechanism, or theorem

Represent a thread lifecycle as:

Uncreated -> Created -> Started -> Terminated -> Joined,

with creation failure returning to no-thread, and an alternative Started -> Terminated -> Detached/Reclaimed path where the API permits detachment. A correct owner maintains exactly one completion obligation for every successful creation.

The memory-order proof uses two edges. Initialization sequenced before successful start becomes visible to the child according to the language start rule. Child writes sequenced before termination become visible after a successful join according to the join rule. A thread reference, sleep, timed wait, or observed flag is not a substitute unless its specification provides the required ordering.

### Critical invariants

Inputs outlive every child access or are transferred/copied safely. Successful creation produces exactly one owned lifecycle obligation. Creation failure produces no live thread and retains input cleanup authority. Start is invoked exactly as specified. Child results and failures are captured. Successful join occurs before dependent result use and reclamation. No thread joins itself or participates in a join cycle. Detachment is explicit and does not masquerade as cancellation. Process exit behavior is declared. Thread count and stack memory are bounded. Cancellation releases resources and reports one terminal outcome.

### Common failures

Teams pass pointers to expired stack variables; capture a loop variable whose value changes; assume construction alone publishes data; start a thread from an incompletely constructed object; ignore creation failure; drop or overwrite join handles; sleep instead of joining; read child results before successful join; join self or create mutual join; interpret a timed join return as termination; detach to silence a leak; assume detachment stops work; let background threads access shutdown resources; lose child exceptions; or create one native thread per item without admission control.

### Compact example

A parent initializes an input record, starts a worker, and the worker computes a result in shared memory. The specified start edge publishes the input to the worker. The worker's termination followed by a successful join publishes its result to the parent. If the parent merely waits 10 milliseconds and reads, neither completion nor visibility follows. The correct protocol owns the join handle, joins, checks failure, then consumes the result.

### Connections

[Choosing a Concurrency Model from the Workload](010-choosing-a-concurrency-model-from-the-workload.md) establishes when threads fit; [Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md) governs shared data; [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md) governs join cycles and cancellation. The [program roadmap](../ROADMAP.md) next develops mutexes, condition variables, semaphores, read-write locks, barriers, queues, lock ordering, and thread pools.

## Governing Question

How can engineers create a thread only after its inputs and ownership are valid, observe its completion with the correct synchronization edge, propagate its result or failure, and reclaim every resource without leaks, races, orphaned work, or shutdown surprises?

Thread creation is not a fire-and-forget function call. It begins a concurrent lifetime. Join is not merely waiting; it closes that lifetime, establishes visibility in common APIs, and makes error and reclamation responsibilities explicit.

## Why This Matters

The smallest thread program already contains a protocol. The creator prepares inputs, requests an execution context, decides who owns those inputs after success or failure, lets the child run concurrently, and eventually accounts for termination. If any edge is implicit, the result may be a dangling pointer, stale read, resource leak, lost failure, or thread surviving beyond its dependencies.

Thread APIs differ in important details. POSIX distinguishes joinable and detached threads, makes simultaneous joins of the same target undefined, and requires eventual join or detach for joinable-thread resource reclamation. Rust 1.98 represents join permission as an owned, non-cloneable `JoinHandle`; dropping it detaches, and successful `join` synchronizes child operations before later caller operations. Java SE 26 specifies start and join happens-before edges, provides platform and virtual threads, and has runtime-specific daemon behavior. Portable design starts from the selected API specification.

Native or platform threads are finite resources. Each may reserve stack address space, runtime metadata, scheduler state, thread-local storage, and kernel objects. Creation can fail under process, system, memory, or policy limits. A loop that creates one thread per request turns load into resource exhaustion even when each worker is correct.

Joining also affects liveness. Joining oneself cannot complete. Parent A joining B while B joins A creates a wait cycle. A parent holding a mutex while joining a child that needs the mutex deadlocks. Joining every child sequentially can hide parallel completion or delay failure response. Lifecycle structure must be designed alongside work structure.

## Prerequisites and Retrieval

Retrieve:

- thread, task, fiber, process, and scheduler distinctions from [Processes, Threads, Tasks, and Fibers](002-processes-threads-tasks-and-fibers.md);
- happens-before, data races, and result determinism from modules [004](004-safety-liveness-and-progress.md), [005](005-race-conditions-and-atomicity-violations.md), and [007](007-determinism-and-reproducibility.md);
- deadlock, cancellation, and terminal accounting from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- ownership transfer and cleanup authority from [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md);
- lifetime, aliasing, exceptions, and resource acquisition/release; and
- directed wait graphs, partial orders, state machines, and inductive invariants.

Retrieval prompt: draw parent and child timelines. Mark input initialization, successful start, child read, child result write, termination, successful join, and parent result read. Add the required ordering edges and explain which read becomes unjustified if join is replaced by sleep.

## Learning Objectives

After completing this module, a learner can:

1. model thread creation, start, execution, termination, join, detach, and reclamation as a lifecycle;
2. apply language-specific start and join visibility guarantees without inventing portability;
3. prove capture and argument lifetimes across successful and failed creation;
4. assign one join or detach obligation to every successfully created thread;
5. propagate child return values, exceptions, panics, and cancellation outcomes;
6. identify self-join, join-cycle, lock-while-join, and shutdown deadlocks;
7. bound thread count, stack memory, and creation rate from workload and platform evidence;
8. test lifecycle edges deterministically without substituting timing for synchronization; and
9. recognize safety-critical thread-lifecycle decisions requiring named authorized review.

## Core Exposition

### Separate construction, start, and execution

Some APIs combine allocation and start; others let code configure a thread object before `start`. Keep the conceptual states separate. Before successful start, the child must not execute. After start succeeds, parent and child run concurrently unless another ordering exists. After termination, the execution has stopped but join metadata may remain until observed or detached.

Creation can fail. Define the ownership transition:

- before the call, creator owns argument storage and cleanup;
- on failure, no child will consume it, so creator retains or restores ownership;
- on success, the documented capture or transfer rules apply and a completion obligation exists.

Never publish a handle as “running” before success. If a batch creates several threads and one creation fails, cancel/join already-created children or continue under an explicit partial-start protocol. Roll back shared registration and preserve every handle.

Thread attributes matter: detached state, stack size, scheduling policy, daemon status, name, and affinity can affect lifetime or resource behavior. Validate requested stack against recursion, foreign calls, guard behavior, and platform limits. Names aid diagnosis but are not stable identity or synchronization.

### Capture values and lifetimes

A worker may receive a deep copy, moved value, immutable shared object, or pointer/reference to shared state. Document which. The child can begin immediately after start and may outlive the creator's lexical scope unless joined before exit.

Classic hazards include passing the address of a loop-local descriptor reused for the next iteration, capturing the loop index by reference, referencing a stack object after its function returns, and starting a thread from a constructor before the object invariant is established. Allocate one stable descriptor per child, copy immutable values, move ownership, or use lifetime-enforcing scoped threads.

Garbage collection prevents some deallocation errors but not logical races. A Java child that captures a mutable list shares the same list. A Rust `move` closure transfers captured bindings, but shared ownership and interior mutability still have their own protocols. A POSIX `void *` argument conveys no lifetime proof.

Publish fully initialized state. Java specifies that a call to `Thread.start` happens-before any actions in the started thread. Rust's safe `spawn` signature and ownership bounds restrict borrowed data for unscoped threads, while scoped APIs offer narrower lifetimes. POSIX memory synchronization rules must be read with the creation API. Do not generalize one language's edge to a custom runtime.

### Start exactly once under one owner

Starting an already started thread is invalid or erroneous in common APIs. Treat the transition as single-use. If several components may request start, designate one authority or serialize the state transition. A Boolean checked without atomicity recreates check-then-act.

Starting from an incompletely constructed owner can expose fields before the constructor establishes its invariant and can invoke overridable behavior on a partially initialized object. Prefer factories: construct immutable dependencies, establish the object invariant, then start under an external owner.

Record creation identity separately from recycled platform identifiers. Thread IDs can be reused after lifetime ends. Correlate logs through a logical operation or generation ID, and do not use thread ID as authorization.

### Join is completion, visibility, and accounting

A successful join generally supplies three related outcomes:

1. the target execution has terminated;
2. its completion result or failure becomes available according to the API; and
3. its prior actions become ordered before post-join actions under the memory model.

Java SE 26 states that all actions in a thread happen-before another thread successfully returns from joining it. Rust 1.98 documents the same synchronization shape for `JoinHandle::join`. POSIX `pthread_join` waits for termination, exposes the exit value, and permits associated resources to be reclaimed.

Check success. An interrupted, timed-out, invalid, or failed join is not a completed join. Do not consume a result or free inputs that the target may still use. Preserve the handle and decide whether to retry, cancel, wait elsewhere, or escalate.

Join need not mean the child succeeded. A function can return an error; a Java uncaught exception terminates the thread and needs an explicit handler or result carrier; Rust join returns an error for a panic under its documented conditions. Normalize completion to Succeeded(value), Failed(error), or Cancelled(reason), while retaining language-specific details.

### Deterministic evidence for join ordering

Without join, parent and child actions may interleave. A shared flag written by the child and polled without synchronization can itself race. Sleep makes one timing more likely but supplies neither termination nor visibility.

<!-- bijux-verify: {"id":"join-orders-result-observation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"unjoined_schedules=3\nunjoined_stale_reads=1\njoined_schedules=1\njoined_stale_reads=0\n","stderr":""}} -->
```python
def schedules(events, before):
    results = []

    def visit(prefix, remaining):
        if not remaining:
            results.append(prefix)
            return
        for event in remaining:
            required = before.get(event, [])
            if all(item in prefix for item in required):
                visit(prefix + [event], [item for item in remaining if item != event])

    visit([], events)
    return results

unjoined = schedules(
    ["write", "finish", "read"],
    {"finish": ["write"]},
)
joined = schedules(
    ["write", "finish", "join_return", "read"],
    {
        "finish": ["write"],
        "join_return": ["finish"],
        "read": ["join_return"],
    },
)

unjoined_stale = sum(order.index("read") < order.index("write") for order in unjoined)
joined_stale = sum(order.index("read") < order.index("write") for order in joined)

print(f"unjoined_schedules={len(unjoined)}")
print(f"unjoined_stale_reads={unjoined_stale}")
print(f"joined_schedules={len(joined)}")
print(f"joined_stale_reads={joined_stale}")
```

The enumeration proves only the counts in this small partial-order model. It does not model weak memory, an actual API, join failure, multiple children, compiler behavior, or production thread scheduling.

### Detachment changes observation, not execution

Detaching tells the runtime no future join will collect that thread through the join mechanism and enables eventual resource reclamation under the API. It does not cancel the thread, wait for it, propagate errors, or make captured objects safe.

Use detachment only when another explicit owner tracks lifetime, failure, shutdown, and cleanup—or when the operation is intentionally process-lifetime and harmless at abrupt process termination. “We do not care” is not an ownership model. Logging, telemetry, and cleanup threads still access resources that shutdown can destroy.

POSIX joinable threads require eventual join or detach to avoid retained thread resources. Rust dropping a `JoinHandle` detaches. Java does not use an owned join handle in the same way; a `Thread` object reference and daemon status have different semantics. Preserve these distinctions.

### Joining safely

Never join the current thread. Build a wait-for graph when threads join one another. Enforce an acyclic ownership tree: parents may join descendants, children report upward, and siblings do not form arbitrary waits. If a child needs the parent's result, use dataflow or a higher-level coordinator instead of mutual join.

Release locks and scarce resources before join when the child may need them. Capturing a handle under lock, transitioning state to Joining, releasing, then waiting and reacquiring to publish completion is often safer. Revalidate state after reacquisition.

Join groups by first recording all handles, then joining all while collecting every failure. Failing fast by returning after the first error can orphan remaining children. Request cancellation on peers if policy requires, but still join/drain them before leaving scope.

### Cancellation and shutdown

Thread termination should usually be cooperative. Set or send cancellation through a synchronized mechanism, wake every blocking site, and let the worker unwind cleanup. Forced termination can leave locks held, invariants broken, foreign libraries inconsistent, and thread-local destructors skipped.

Define checkpoints and bounded blocking. An interrupt or stop token is a request with runtime-specific semantics, not proof of termination. The owner joins after requesting cancellation to establish actual completion. If a dependency cannot be interrupted, process isolation or timeout escalation may be required.

At process shutdown:

1. stop admission;
2. request cancellation or graceful completion;
3. wake blocked workers;
4. join owned threads within policy;
5. record unresolved work explicitly; and
6. only then destroy shared dependencies.

Daemon/background behavior is not graceful shutdown. A runtime may end the process while daemon work remains. Do not entrust durable commits or critical cleanup solely to such threads.

### Capacity and thread economics

Bound successful live creation. A thread budget accounts for application workers, runtime pools, libraries, monitors, and foreign components. Stack reservation multiplied by count can exhaust address space or committed memory before CPU saturates.

For CPU work, a bounded pool usually outperforms creation per item. For blocking work, more threads can overlap waits but must respect memory, external quotas, contention, and tail latency. Virtual or user-mode threads reduce some creation and stack costs but do not increase database connections, memory bandwidth, file descriptors, or downstream capacity.

Creation rate itself can dominate short tasks. Measure create, start, context-switch, join, and teardown overhead with representative runtime settings. Prefer tasks on long-lived executors once the workload is repeated and independently schedulable.

### Results, failures, and cleanup

Return owned result values through the join mechanism, a future, or a protected result slot. Define who destroys the result if the joiner is cancelled. Do not return a pointer to child stack storage.

Catch only failures the language permits and preserve diagnostic context. Include logical operation ID, thread name, input partition, and causal parent without exposing secrets. An uncaught child failure must reach supervision; logging alone is not terminal accounting.

Thread-local destructors may run during termination, and some APIs define join relative to them. Rust documents that `join` waits through thread-local destructors. Foreign unwinding can have special process-abort behavior. Keep cross-language exceptions from crossing unsupported thread roots.

## Definitions and Notation

Let lifecycle state (L_t) be Uncreated, Created, Started, Terminated, Joined, or Detached. Legal transitions depend on the selected API. A creation obligation function (O(t)) is zero before successful creation, one while join/detach accounting is outstanding, and zero after valid completion accounting.

Let events (init, start, child-read, child-write, terminate, join-return, parent-read) form a partial order. The required publication relations are (init happens-before child-read) through start semantics and (child-write happens-before parent-read) through successful join plus program order.

Let live thread count (N_live) obey configured bound (B), including framework and library threads in the chosen budget. Terminal accounting partitions successfully created threads into Joined, Detached-under-owner, or explicitly unresolved at forced process termination.

## Mechanisms, Invariants, or Proof Structure

Use this workflow:

1. **Choose the execution abstraction.** Confirm a thread is preferable to a task, async operation, or process.
2. **Specify lifecycle.** Creation, start, result, failure, cancellation, termination, join/detach, and reclamation.
3. **Assign ownership.** Capture inputs, join handle, result, and cleanup each have one owner on success and failure.
4. **Prove publication.** Cite actual start and join ordering rules.
5. **Bound capacity.** Include stack, runtime, external quotas, and creation rate.
6. **Prevent wait cycles.** Use an acyclic parent-child structure and release dependencies before join.
7. **Propagate failure.** Collect every child outcome and drain remaining children.
8. **Design shutdown.** Stop admission, cancel, wake, join, then destroy dependencies.
9. **Test adversarially.** Creation failure, immediate execution, delayed execution, panic, cancellation, join interruption, and shutdown.
10. **Record limitations.** Separate finite tests, API guarantees, and production assumptions.

Maintain these invariants:

- successful creation yields exactly one lifecycle obligation;
- failed creation leaves no live child and retains cleanup authority;
- captured inputs remain valid until the final child use;
- pre-start initialization and post-join observation use specified ordering;
- every child result or failure reaches supervision;
- no join edge forms a cycle or retains a needed lock;
- detach is explicit and has another lifetime owner;
- cancellation is followed by observed termination;
- live thread and stack use stay within budget; and
- shared dependencies outlive all accessing threads.

## Alternatives and Trade-Offs

**Create per operation** gives a direct lifecycle but pays creation and stack cost and can exhaust resources. **Submit to a bounded pool** amortizes thread cost and centralizes admission, but task cancellation and thread-local leakage require care.

**Joinable threads** expose completion, result, failure, and visibility. They retain join state until accounted for. **Detached threads** reduce handle management only when another supervisor owns lifetime and errors; otherwise they create orphaned work.

**Shared result state plus join** can avoid copying large values but still needs invariant and lifetime discipline. **Owned result return** makes transfer explicit. **Message or future results** support richer composition but add their own capacity and cancellation protocol.

**Cooperative cancellation** preserves cleanup and invariants but depends on checkpoints and interruptible waits. **Process isolation** provides a stronger termination boundary for uncooperative or unsafe foreign work at IPC and startup cost.

**Platform threads** provide direct operating-system scheduling and broad blocking compatibility. **Virtual/user-mode threads** reduce some per-thread overhead, but pinning, foreign calls, memory, downstream quotas, and runtime scheduling remain.

## Failure Modes and Misconceptions

- **“Creation always succeeds.”** Resource and policy limits require an explicit failure branch.
- **“The child starts after the next parent statement.”** It may run immediately after successful start.
- **“A captured reference stays valid.”** Lexical scope can end while the child remains live.
- **“Start is only scheduling.”** It can also be a specified publication edge.
- **“Sleep is a lightweight join.”** It proves neither completion nor memory visibility.
- **“Join means success.”** The child may return an error, panic, or be cancelled.
- **“A timed join returned, so the thread ended.”** Check the API's completion result.
- **“Drop/detach cancels.”** The thread normally continues without join authority.
- **“Daemon means safely managed.”** Process shutdown may abandon daemon work.
- **“Join while holding a lock is fine because the child is almost done.”** The child may need that lock.
- **“Thread IDs are permanent identities.”** Runtimes and systems may reuse them.
- **“Cheap threads remove capacity limits.”** External quotas, memory, CPU, and downstream services remain finite.

## Worked Examples

### Example 1

**Question:** A loop passes every child the address of the same mutable descriptor.

**Reasoning:** Immediate or delayed starts can observe different iterations, and the descriptor may expire.

**Conclusion:** Allocate stable per-child inputs, copy values, or use a lifetime-enforced scoped API.

### Example 2

**Question:** The fifth of eight creation calls fails.

**Reasoning:** Four live children and their handles already exist; pretending the batch never started leaks obligations.

**Conclusion:** Join/cancel those children or continue through a documented partial-start result.

### Example 3

**Question:** A parent initializes immutable input and calls Java `start` before the child reads it.

**Reasoning:** Java SE 26 specifies start happens-before child actions.

**Conclusion:** That input is published through the start edge, assuming no later unsynchronized mutation.

### Example 4

**Question:** A parent reads a child's shared result after sleeping but without join.

**Reasoning:** Elapsed time supplies no specified termination or visibility edge.

**Conclusion:** Join successfully or use another documented synchronization mechanism.

### Example 5

**Question:** A child panics and its Rust join handle is dropped.

**Reasoning:** Dropping detaches; no joiner receives the panic payload.

**Conclusion:** Retain and join the handle under a supervisor when failure matters.

### Example 6

**Question:** Thread A joins B while holding mutex M, and B needs M to return.

**Reasoning:** A waits for B; B waits for M owned by A.

**Conclusion:** Release M before join or redesign the ownership transition.

### Example 7

**Question:** Two threads attempt to join one another.

**Reasoning:** Each termination depends on the other's termination.

**Conclusion:** This is a join cycle; enforce an acyclic parent-child join graph.

### Example 8

**Question:** What did the executable partial-order model establish?

**Reasoning:** It enumerated three unjoined schedules with one premature read and one joined schedule where read follows termination and join.

**Conclusion:** It verifies that finite model only, not a real runtime or weak-memory execution.

### Example 9

**Question:** A cancelled joiner exits while its target continues.

**Reasoning:** Joiner cancellation does not necessarily cancel or detach the target.

**Conclusion:** Transfer the handle to supervision or complete cancellation and join before leaving scope.

### Example 10

**Question:** Can successful joins approve thread timing in an implantable cardiac controller?

**Reasoning:** Deadlines, hardware interrupts, scheduling analysis, physical hazards, and certification exceed lifecycle accounting.

**Conclusion:** No. Named authorized clinical, real-time, hardware, safety, verification, and regulatory reviewers must approve the real system. No external review is claimed.

## Cross-Program Connections

- **Programming languages:** type systems, closures, ownership, exceptions, and memory models define capture and join behavior.
- **Operating systems:** kernel threads, scheduling, stacks, identifiers, affinity, and process termination provide mechanisms.
- **Software engineering:** structured lifetime, supervision, logging, shutdown, and resource ownership make thread use maintainable.
- **Security:** thread creation limits, privilege context, secret-safe diagnostics, and untrusted foreign work affect containment.
- **Performance engineering:** creation cost, stacks, blocking, oversubscription, and tail latency determine capacity.
- **Formal methods:** state machines, happens-before, wait-for graphs, and conservation prove lifecycle safety.

## References

1. IEEE and The Open Group, *POSIX.1-2024*, “pthread_create,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_create.html) (retrieved 2026-08-29).
2. IEEE and The Open Group, *POSIX.1-2024*, “pthread_join,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_join.html) (retrieved 2026-08-29).
3. Oracle, *Java Language Specification, Java SE 26*, `17.4.5, [official specification](https://docs.oracle.com/javase/specs/jls/se26/html/jls-17.html#jls-17.4.5) (retrieved 2026-08-29).
4. Oracle, “Thread,” *Java SE 26 API*, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/lang/Thread.html) (retrieved 2026-08-29).
5. Rust Project, “JoinHandle,” Rust 1.98 standard library, [official API](https://doc.rust-lang.org/std/thread/struct.JoinHandle.html) (retrieved 2026-08-29).
6. Rust Project, “spawn,” Rust standard library, [official API](https://doc.rust-lang.org/std/thread/fn.spawn.html) (retrieved 2026-08-29).
7. David R. Butenhof, *Programming with POSIX Threads*, Addison-Wesley, 1997.
8. Brian Goetz et al., *Java Concurrency in Practice*, Addison-Wesley, 2006.
9. Maurice Herlihy et al., *The Art of Multiprocessor Programming*, second edition, Morgan Kaufmann, 2020.
10. Nathaniel J. Smith, “Notes on Structured Concurrency, or: Go Statement Considered Harmful,” 2018, [author essay](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/).

## Exercises

### Exercise 1

Design lifecycle states and ownership for creating six workers when any creation can fail. Include partial-start rollback and every handle.

### Exercise 2

Explain the start and join ordering edges for a parent-produced input and child-produced result. Identify three actions that do not substitute for them.

### Exercise 3

Construct a wait-for graph for a parent joining two children while holding resources. Redesign it to prevent join deadlock.

### Exercise 4

Specify shutdown for joinable workers blocked on a queue and foreign I/O. Include cancellation, wakeup, results, time bounds, and escalation.

### Exercise 5

A railway controller creates one thread per sensor and joins them each cycle. Assess what lifecycle evidence proves and where named human review is mandatory.

## Answers to the Exercises

### Answer 1

Start with six uncreated slots and creator ownership of all descriptors. Each success installs Started plus one owned join handle; failure installs no child for that slot. On first failure, stop further creation, request cancellation for every started worker, wake blocking sites, and join every recorded handle while collecting outcomes. Only after all joins may descriptors and shared dependencies be reclaimed. Alternatively return a partial-start object that owns all live handles and has an explicit close operation. Never discard earlier handles or free the failed argument as if it had transferred.

### Answer 2

Initialization sequenced before successful start is ordered before child actions by the selected API's start rule. Child writes before termination are ordered before parent actions after successful join by the join rule. Together they justify input and result visibility. Sleeping, reading a thread ID, checking an unsynchronized Boolean, logging, or merely holding a thread object do not supply those edges. A timed/failed join also does not justify post-termination assumptions until its API reports successful completion.

### Answer 3

Add parent -> child-A and parent -> child-B join edges. If parent holds M while A needs M, add A -> M -> parent, closing a cycle; similarly for any connection or queue capacity B needs. Under lock, capture handles and transition component state to Stopping, then release all resources needed by children. Request cancellation/wakeup, join both without those resources, collect every outcome, reacquire only to publish final state, and revalidate. Enforce descendants-only joins to prevent child-parent cycles.

### Answer 4

Stop admission, set cancellation through synchronized state, close or notify the work queue so waiters wake, and make workers checkpoint and unwind. Interrupt foreign I/O only through its supported mechanism. Join all handles and classify Succeeded, Failed, or Cancelled. A timeout triggers escalation but does not prove termination; preserve handles. If foreign work cannot stop safely, isolate it in a process whose termination and recovery are defined. Destroy queues, buffers, credentials, and logging only after joined completion or an explicitly recorded forced-shutdown policy.

### Answer 5

Lifecycle evidence can show creation failures are handled, inputs outlive use, start/join order publishes values, every thread terminates or is accounted for, and the software avoids modeled join cycles. It cannot establish sampling deadlines, sensor validity, scheduler worst cases, physical interlocks, fail-safe states, hazard coverage, or signaling certification. Named authorized railway signaling, real-time, hardware, functional-safety, verification, cybersecurity, and regulatory reviewers must approve those claims and deployment. This chapter claims no external review.
