---
module_id: OS-015
program: Operating Systems
level: 1
module_number: 15
title: Process States and Wait Queues
status: complete
last_verified: 2026-09-04
---

# Process States and Wait Queues

## One-Page Review

### Governing question

How can a kernel stop a task that cannot make progress and later make it runnable without losing an event, running it twice, or confusing readiness with completion?

### Essential definitions

- A **task state** summarizes scheduling eligibility and lifecycle, not the source line currently executing.
- A **runnable** task may be selected by a scheduler; a **running** task currently owns a processor.
- A **blocked** task is ineligible until a predicate, timeout, signal, or cancellation condition changes.
- A **wait queue** records waiters associated with a condition and coordinates their transition between blocked and runnable states.
- A **wait predicate** is the protected fact a waiter needs, such as `items > 0`; the queue notification is only a hint to recheck it.
- A **lost wakeup** occurs when a waiter commits to sleep after the condition became true and after the only relevant notification passed.
- A **spurious wakeup** is a permitted return or wake without the desired predicate being true.
- An **exclusive wakeup** selects a bounded waiter set; a broadcast makes all eligible waiters compete again.

### Central model, mechanism, or theorem

For predicate `P` protected by synchronization domain `L`, the waiter follows:

`hold(L) -> while not P: publish_waiter -> release_and_block -> reacquire(L) -> recheck P`.

The producer follows:

`hold(L) -> make P true -> publish state -> select/wake waiters -> release(L)`.

Exact ordering varies, but no interval may exist in which `P` becomes true, the producer observes no registered waiter, and the consumer then blocks without rechecking. Correctness belongs to predicate, queue, task state, scheduler enqueue, memory ordering, and object lifetime together.

### Critical invariants

- A live task is running on at most one CPU, queued runnable at most once, or represented by a valid blocked wait entry.
- The predicate and waiter publication share a lock or an equivalent proven atomic-ordering protocol.
- Every wake transition from blocked to runnable is idempotent or otherwise protected against duplicate enqueue.
- Waiters recheck predicates after wakeup, interruption, timeout, and competition.
- A wait entry and its containing object outlive every producer, timer, signal path, poll registration, and deferred wake that can reference them.
- Cancellation and teardown close admission, wake or remove waiters, synchronize callbacks, and only then reclaim state.
- Diagnostics distinguish state snapshots from durable causal explanations.

### Common failures

Common mistakes are sleeping after checking outside the queue lock, using `if` instead of `while`, treating a notification as stored state, waking before publishing data, double-enqueueing a task, holding a spinlock across sleep, missing timeout-versus-wakeup races, freeing a wait object while a timer can fire, broadcasting on every item, assuming FIFO fairness, interpreting a process-state letter as a full diagnosis, and counting wakeups as completed work.

### Compact example

A consumer locks a bounded queue, checks `count == 0`, registers its wait record, and atomically releases the lock while blocking. A producer locks the same queue, inserts an item, updates `count`, wakes one eligible consumer, and unlocks. The consumer reacquires the lock and loops on `count == 0`; another consumer may have taken the item. Shutdown sets `closed`, broadcasts, and each waiter exits when `closed && count == 0`. Teardown joins consumers and cancels timers before destroying the queue.

### Connections

[OS-013](013-threads-and-execution-contexts.md) defines thread lifecycle, [OS-014](014-context-switching.md) explains the transfer after blocking, [OS-016](../ROADMAP.md) develops scheduler objectives, and [OS-021](../ROADMAP.md) develops kernel synchronization. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies condition-variable and happens-before reasoning.

## Governing Question

Polling wastes processor time when useful progress depends on input, a timer, another task, or a device. Blocking releases the processor, but introduces a distributed state transition. The waiter changes its scheduler state and queue membership while a producer, interrupt, timer, signal, or teardown path may concurrently change the predicate.

The central hazard is the gap between “condition false” and “task asleep.” If the producer changes the condition and sends its only notification inside that gap, the task can sleep forever despite available work. Avoiding that gap requires a shared synchronization protocol, not a faster wake instruction.

The governing question is how state, predicate, queue, memory visibility, interruption, timeout, fairness, and lifetime form one proof. An API named `wait` or a task displayed as sleeping proves none of these properties alone.

## Why This Matters

Wait paths underlie mutexes, condition variables, process exit, I/O readiness, page faults, device completion, timers, memory reclaim, job control, and shutdown. A lost wakeup can hang a system rarely and irreproducibly. Duplicate wakeup can place one task on two run queues. Premature reclamation can turn a late timer into privileged use-after-free.

Performance is also structural. Busy waiting may be appropriate for a very short bounded interval but wastes capacity when waits are long. Broadcast wakeups cause a thundering herd. Strict ordering may reduce throughput. Timeout polling adds latency and load. Priority-blind queues can create inversion or starvation.

Operationally, state names are observations. A blocked task may be healthy, deadlocked, starved, or waiting for failed hardware. Diagnosis needs predicate ownership, queue duration, stack, wake source, scheduler delay, and system context.

## Prerequisites and Retrieval

Recall thread-private and shared state from [OS-013](013-threads-and-execution-contexts.md), switch invariants from [OS-014](014-context-switching.md), and interrupt context from [OS-004](004-interrupts-and-exceptions.md). You should understand locks, atomics, memory ordering, timers, signals, and resource lifetime.

Retrieve these distinctions:

- running is a subset of runnable, while blocked is not schedulable;
- a condition is state; a wakeup is an event about possible state change;
- queue membership does not itself protect the predicate;
- interruptible and uninterruptible waits express different interruption policy, not importance;
- readiness says an operation may progress; completion says a particular operation finished;
- timeout, wake, cancellation, and teardown may race;
- a snapshot state code does not identify root cause.

## Learning Objectives

After this module, you should be able to:

1. model running, runnable, blocked, stopped, zombie, and dead lifecycle states without treating them as universal ABI values;
2. derive a race-free sleep/wakeup protocol from a protected predicate;
3. explain lost and spurious wakeups, exclusive wake, broadcast, and thundering-herd behavior;
4. distinguish condition waits, completions, futex waits, readiness polling, timers, and child-process waits;
5. review timeout, signal, cancellation, shutdown, and object-lifetime races;
6. design observability that separates wait duration, wakeup latency, scheduler delay, and work completion;
7. evaluate fairness, throughput, latency, and real-time trade-offs.

## Core Exposition

### Task states are models

An instructional state machine may include `new -> runnable -> running -> blocked -> runnable -> dead`, with stopped and zombie branches. Production kernels refine these labels, encode transient flags, and expose only selected views. State is meaningful only with its transition rules and synchronization.

A zombie has finished execution but retains exit information until its parent or another designated reaper collects it. It is not a blocked executable task. A stopped task is prevented from running by control policy. A runnable task waiting in a run queue differs from a blocked task waiting for a predicate.

### Predicate before notification

The durable fact is the predicate. A queue with `count > 0` remains usable even if no notification is remembered. A condition variable or wait queue usually does not accumulate arbitrary past signals. Therefore consumers check under the synchronization that producers use to change the fact.

Waiters loop because wake can be spurious, a signal can interrupt, a timeout can expire, or a competing waiter can consume the resource first. The loop also makes the code robust to implementations that wake more tasks than ultimately acquire work.

### Closing the lost-wakeup window

A lock-based condition variable atomically releases the predicate mutex and blocks, then reacquires it before return. A kernel wait queue commonly publishes an entry and blocked state under a lock before testing or relinquishing the CPU. Lock-free variants require an equally explicit atomic state machine and memory-order proof.

The producer changes `P` under the paired protocol and performs the wake at the documented point. Publishing data after wake can let a scheduled consumer see stale or incomplete state. Moving wake outside a lock can be correct, but only after proving waiter visibility, predicate visibility, and object lifetime.

### From blocked to runnable

Wakeup normally changes eligibility, not execution. It must arbitrate concurrent wakers, remove or mark the wait entry, set runnable state, select a destination run queue, and enqueue once. Scheduler policy then decides when the task runs. Wake-to-run delay is not the low-level wake operation's duration.

On multicore systems the waker and waiter may execute on different CPUs. Locks, atomic transitions, barriers, interprocessor notifications, affinity, idle state, and run-queue ownership participate. Local interrupt masking alone does not serialize another CPU.

### Exclusive wake and broadcast

When one new item can satisfy one waiter, waking one eligible waiter avoids needless contention. A broadcast is appropriate when a global transition such as shutdown may change every waiter's result, or when multiple units became available and selection cannot cheaply match them.

Exclusive wake does not automatically promise FIFO fairness. Priority, queue insertion, cancellation, affinity, scheduler policy, and repeated arrivals can alter order. If fairness is a requirement, specify and test it directly.

### Futex-style waiting

A futex lets uncontended synchronization stay in user space and invokes the kernel for blocking and wakeup. The wait operation compares a user-space word with an expected value and blocks only if it still matches, closing a common check-then-sleep race. Higher-level libraries remain responsible for their mutex or condition state machine.

The word's lifetime, alignment, mapping, and sharing must remain valid. Wake counts, robust-owner death, priority inheritance, timeouts, and signals are separate semantics. A futex is a building block, not by itself a complete mutex contract.

### Readiness and event multiplexing

`poll` and `epoll` wait for readiness on file descriptors. Readiness means a requested operation would not block under the interface's rules; it does not reserve data or promise that another thread cannot consume it. Applications must handle operations that still fail, short transfer, closure, and descriptor reuse.

Level-triggered notification reports a condition while it remains true. Edge-triggered notification reports transitions and requires draining until the operation would block. Registration, modification, close, duplicated descriptors, and concurrent consumers create lifecycle and ownership questions.

### Completion, counters, and process wait

A completion represents occurrence of a specific event and may retain a token-like done state, unlike a bare condition notification. Semaphores represent countable capacity. `eventfd` exposes a counter through a descriptor. Child wait interfaces collect lifecycle changes and reap exit state. These abstractions are not interchangeable merely because each can block.

Choose the primitive whose stored state matches the domain: predicate, one-shot or reusable completion, quantity, stream readiness, or child lifecycle. Document whether events coalesce, accumulate, wake one, wake all, or can be consumed.

### Timeouts, signals, and cancellation

A timeout adds another producer racing to resolve the wait. Code must define one winner, cancel or synchronize the other path, and interpret boundary cases consistently. Relative sleeps can drift after repeated interruption; deadline-oriented designs recompute from an absolute objective where supported.

Signals and cancellation turn return into a multi-outcome protocol. A caller must distinguish predicate satisfied, interrupted, timed out, canceled, object closed, and error. Cleanup cannot free state while a wake callback or timer still owns a reference.

### Shutdown and lifetime

Safe teardown first prevents new wait registrations, publishes closure, wakes affected tasks, and waits for them to leave or removes them under the protocol. It then cancels and synchronizes timers, interrupts, poll callbacks, and deferred work before freeing the queue and predicate state.

Reference counting alone does not close new admission. A closed flag alone does not drain in-flight callbacks. Joining workers alone does not cancel a timer that references their shared object. Teardown needs an ordered ownership proof.

### Observability and evidence

Measure wait-entry time, wake-request time, runnable-enqueue time, actual run time, predicate-acquisition time, and completion when these distinctions matter. Scheduler statistics and tracepoints can expose parts of the chain, with configuration and overhead limitations.

Long waits may be intended. Flag them only against a service objective and known predicate. Record queue identity, wake reason, timeout, signal, CPU, priority, stack, and owner while protecting sensitive data. Sampling can miss short waits and tracing can perturb timing.

### Real-time and safety boundaries

Real-time systems bound blocking, priority inversion, interrupt interference, wake processing, scheduler delay, and competing waiter behavior. Broadcasts and unbounded queues are suspect. Priority inheritance or priority-aware wake can help only within a complete scheduling and locking analysis.

Safety-relevant waits need defined timeout and degraded behavior, independent monitoring where required, fault injection, hardware-loss handling, and named human acceptance. Observed wake latency is evidence, not certification.

## Definitions and Notation

Let `P(x)` be the predicate over shared state `x`, protected by synchronization domain `L`. Let `W` be the waiter set. Let task `T_i` have state `state_i` and at most one scheduler or wait-queue owner. Let events `register_i`, `publish_P`, `wake_i`, `enqueue_i`, and `run_i` name protocol milestones.

Define wakeup latency `Lw = time(run_i) - time(wake_i)` only after fixing timestamp locations. Define total wait `Tw = time(predicate_acquired) - time(wait_begin)`. Neither equals work completion latency.

Core properties are:

- **no lost wake:** after `P` becomes durably true, a waiter cannot newly block on the obsolete false observation;
- **single placement:** a task is running, runnable-queued, or blocked-queued in one valid ownership state;
- **visibility:** observing the wake protocol provides the ordering required to re-read predicate state;
- **recheck:** wake return never substitutes for evaluating `P`;
- **bounded lifetime:** wait entries, predicates, and callbacks remain alive through their final possible access;
- **outcome clarity:** success, timeout, interruption, cancellation, closure, and error are distinguishable as required.

## Mechanisms, Invariants, or Proof Structure

A proof review follows six obligations:

1. Identify the exact predicate and every writer.
2. Show how a waiter publishes itself before it can cease checking the predicate.
3. Show how a producer publishes the predicate and finds a waiter without a gap.
4. Prove wake changes blocked to runnable at most once and scheduler placement remains unique.
5. Enumerate spurious, competing, timeout, signal, cancellation, and shutdown outcomes and require recheck.
6. Close admission and synchronize every asynchronous reference before reclamation.

This executable state exploration contrasts an unsafe check-then-sleep ordering with registered waiting.

<!-- bijux-verify: {"id":"toy-lost-wakeup","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"unsafe=blocked-with-work\nsafe=runnable-with-work\npredicate=ready\n","stderr":""}} -->
```python
predicate = False
unsafe_waiter = "checking"
predicate = True
unsafe_waiter = "blocked"

safe_predicate = False
safe_waiter = "registered"
safe_predicate = True
if safe_waiter == "registered":
    safe_waiter = "runnable"

print("unsafe=blocked-with-work" if predicate and unsafe_waiter == "blocked" else "unsafe=ok")
print("safe=runnable-with-work" if safe_predicate and safe_waiter == "runnable" else "safe=bad")
print("predicate=ready" if predicate else "predicate=not-ready")
```

The unsafe sequence deliberately places the producer between check and block. The safe sequence is only an abstract ordering illustration; it omits real locks, atomics, memory models, schedulers, signals, timers, and queue lifetime.

## Alternatives and Trade-Offs

- Busy waiting avoids sleep overhead for short bounded waits but consumes CPU and can delay the producer.
- Blocking conserves capacity for longer waits but adds queueing, scheduling, and lifecycle machinery.
- Wake-one limits contention when one unit exists; broadcast handles global transitions but can create a herd.
- FIFO ordering is predictable; priority ordering can improve urgency while risking starvation without policy.
- Level-triggering is forgiving of partial drains; edge-triggering reduces repeated notice but requires disciplined draining.
- Relative timeouts are simple; absolute deadlines better control accumulated drift.
- Embedded wait entries reduce allocation; separate entries simplify some reuse but expand ownership.
- Rich tracing improves diagnosis while adding overhead, storage, authority, and schedule perturbation.

## Failure Modes and Misconceptions

1. **“A wakeup is saved work.”** Usually the predicate is durable; notification may be transient.
2. **“Check then sleep is close enough.”** The gap is precisely where a lost wakeup occurs.
3. **“Use `if` after waking.”** Competition and spurious returns require a loop.
4. **“Wake means running.”** It normally means runnable; policy and load determine dispatch.
5. **“Queue membership protects data.”** Predicate state needs its own documented synchronization.
6. **“One wake means one completion.”** Wake can be spurious, coalesced, interrupted, or consumed by a competitor.
7. **“Broadcast is safest.”** It can create severe contention and still needs predicate recheck.
8. **“Wait queues are FIFO.”** Ordering is implementation and policy dependent unless guaranteed.
9. **“A futex is a mutex.”** It is a compare-and-block/wake mechanism used by higher-level protocols.
10. **“Readiness reserves input.”** Another consumer can change readiness before the operation.
11. **“Timeout eliminates hangs.”** Timeout cleanup can race with a late wake and corrupt lifetime.
12. **“Uninterruptible means high priority.”** It describes interruption policy, not scheduler importance.
13. **“A sleeping state proves deadlock.”** Healthy I/O waits and failed dependencies can look alike.
14. **“Observed maximum wait is a bound.”** Coverage and environment determine what was observed.

## Worked Examples

### Example 1

An unsafe consumer checks `count == 0`, unlocks, and later registers to sleep. A producer inserts an item and finds no waiter. The consumer then blocks forever. Combining check, registration, and release under one protocol closes the gap.

### Example 2

Two consumers wake for one item. Consumer A reacquires the lock first and decrements `count`. Consumer B then sees zero and waits again. A `while` loop makes both schedules correct.

### Example 3

A bounded queue wakes one consumer for each inserted item but broadcasts when `closed` becomes true. Ordinary work limits contention; closure lets every waiter discover its terminal outcome.

### Example 4

A futex waiter compares a word with expected value 4. A producer changes it to 5 before the syscall. The kernel comparison fails, so the waiter returns rather than sleeping on an obsolete observation. The library still rechecks its complete predicate.

### Example 5

An edge-triggered socket consumer reads only one message and stops while more data remains. No new edge is required, so work stalls. Draining until the operation would block restores the edge-triggered contract.

### Example 6

A device completion races a timeout. An atomic winner field lets exactly one path publish the result; the loser drops its reference. Teardown synchronously cancels the timer and device callback before freeing the request.

### Example 7

A child exits and becomes a zombie. Its parent wait call collects status and releases retained bookkeeping. Treating the zombie as an ordinary blocked process would obscure its completed execution and lifecycle ownership.

### Example 8

A service shows many voluntary switches because workers block efficiently on empty queues. Latency is healthy. A later incident shows few switches because workers spin while a failed producer never publishes work. Counts need predicate and workload context.

### Example 9

A priority-aware waiter wakes behind a lower-priority lock owner. Scheduler priority alone cannot repair the inversion; the lock and wake protocol need bounded critical sections and an analyzed inheritance or ceiling mechanism.

### Example 10

Shutdown closes admission, sets `closed`, broadcasts, joins workers, synchronizes poll callbacks and timers, verifies waiter count zero, and frees state. Reversing the last steps permits late asynchronous use-after-free.

## Cross-Program Connections

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops condition variables, semaphores, atomics, and happens-before. [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies queue invariants. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies capacity, timeout, degraded-mode, and assurance reasoning.

Within this program, [OS-016](../ROADMAP.md) and [OS-017](../ROADMAP.md) explain when runnable tasks execute; [OS-021](../ROADMAP.md) and [OS-022](../ROADMAP.md) deepen locks, semaphores, and condition variables; [OS-056](../ROADMAP.md) develops event-driven I/O.

## References

- Linux man-pages project, [futex(2)](https://man7.org/linux/man-pages/man2/futex.2.html), current page checked 2026-09-04. Compare-and-block, wake, shared words, timeouts, and higher-level synchronization.
- Linux man-pages project, [pthread_cond_wait(3)](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3.html), current page checked 2026-09-04. Atomic unlock-and-wait, reacquisition, predicates, cancellation, and timed waits.
- Linux man-pages project, [epoll_wait(2)](https://man7.org/linux/man-pages/man2/epoll_wait.2.html), current page checked 2026-09-04. Readiness waiting, timeouts, signals, event limits, and concurrent registration.
- Linux man-pages project, [poll(2)](https://man7.org/linux/man-pages/man2/poll.2.html), current page checked 2026-09-04. Descriptor readiness, closure, errors, timeouts, and signal-mask variants.
- Linux man-pages project, [eventfd(2)](https://man7.org/linux/man-pages/man2/eventfd.2.html), current page checked 2026-09-04. Counter semantics, blocking, semaphore mode, readiness, inheritance, and lifecycle.
- Linux man-pages project, [nanosleep(2)](https://man7.org/linux/man-pages/man2/nanosleep.2.html), current page checked 2026-09-04. Relative sleep, interruption, remainder, rounding, drift, and scheduling delay.
- Linux man-pages project, [wait(2)](https://man7.org/linux/man-pages/man2/wait.2.html), current page checked 2026-09-04. Child state changes, blocking, status collection, zombies, signals, and options.
- Linux Kernel documentation, [Driver Basics](https://docs.kernel.org/driver-api/basics.html), current page checked 2026-09-04. Wait-queue APIs, wait conditions, exclusive waits, timeouts, and wakeup barriers.
- Linux Kernel documentation, [Completions](https://docs.kernel.org/scheduler/completion.html), current page checked 2026-09-04. Completion state, initialization, waiting, signaling, reinitialization, context, and lifetime.
- Linux Kernel documentation, [Unreliable Guide To Locking](https://docs.kernel.org/kernel-hacking/locking.html), current page checked 2026-09-04. Sleeping, interrupt contexts, locks, callbacks, reference counts, and deadlocks.
- Linux Kernel documentation, [Linux Kernel Memory Barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), current page checked 2026-09-04. Ordering, sleep and wake functions, locking, multicopy effects, and limits of guarantees.
- Linux Kernel documentation, [Scheduler Statistics](https://docs.kernel.org/scheduler/sched-stats.html), current page checked 2026-09-04. Run, wait, wakeup, and domain statistics with configuration and version constraints.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching process states, scheduler, sleep and wakeup, lost-wakeup avoidance, locks, pipes, and process exit.

## Exercises

### Exercise 1

Construct timelines for an unsafe check-then-sleep consumer and a correct lock-based wait loop. Mark predicate, waiter visibility, lock ownership, blocked state, wake, runnable enqueue, and recheck.

### Exercise 2

Design a bounded queue supporting multiple producers and consumers, timeout, cancellation, and close. Specify predicates, wake-one versus broadcast choices, outcomes, and destruction protocol.

### Exercise 3

Compare a condition variable, futex, completion, semaphore, eventfd, and epoll for six concrete waiting problems. Explain stored state and lifecycle for each choice.

### Exercise 4

Design tracing for intermittent long request waits. Separate wait duration, wake processing, wake-to-run latency, predicate reacquisition, work, and response. State observer effects and privacy controls.

### Exercise 5

Review a real-time device waiter with interrupt completion and a timeout. Cover memory ordering, one-winner resolution, priority, affinity, shutdown, device loss, overload, evidence, and human assurance.

## Answers to the Exercises

### Answer 1

Unsafe: consumer reads false, producer acquires the unrelated or released lock, writes true and observes no waiter, producer wakes nobody, consumer publishes its waiter and blocks. Work exists with no future notification. Correct: consumer holds `L`, reads false, publishes its entry and blocked intent, then releases `L` as part of the wait protocol. The producer must acquire `L` before publishing true, so it either acts before registration and the consumer sees true, or after registration and can wake it. On return the consumer reacquires `L` and loops.

### Answer 2

Use predicates `not_empty = count > 0 || closed` and `not_full = count < capacity || closed` under one mutex. Producers loop on full, consumers loop on empty, and every queue mutation occurs under the mutex. Insert wakes one consumer; removal wakes one producer. Close is idempotent, rejects new inserts, and broadcasts both conditions so every waiter can return closed after draining policy is applied.

Timeout and cancellation return distinct outcomes and cannot abandon an owned slot or item. Cleanup runs with a defined lock state. Destruction closes admission, waits for active calls and waiters to leave, cancels external callbacks, verifies count and ownership, destroys synchronization, then frees memory.

### Answer 3

A condition variable fits a protected arbitrary predicate. A futex supports a user-space synchronization state machine needing kernel blocking. A completion fits a particular occurrence with retained done state. A semaphore fits countable interchangeable capacity. An eventfd exposes a counter through descriptor readiness and integrates with descriptor event loops. Epoll multiplexes readiness across many descriptors but does not own their domain operations.

For each problem, choose based on whether state is predicate, expected word, completion token, quantity, counter, or readiness set. Also specify accumulation, consumption, wake cardinality, cancellation, close, reuse, mapping or descriptor lifetime, and teardown. Similar blocking syntax is not semantic interchangeability.

### Answer 4

Assign a request correlation ID and instrument wait begin, registration, producer predicate publication, wake request, runnable enqueue if available, actual schedule-in, lock reacquisition, predicate success, work completion, and response. Derive total wait, notification processing, wake-to-run, post-run contention, work, and downstream time separately. Capture wait reason, queue, CPU, migration, priority, load, timeout, signal, and sampled stack.

Calibrate clock and tracing overhead, compare tracing on and off, retain raw artifacts, report missing events and distributions, and avoid interpreting samples as complete coverage. Restrict access, redact payloads, bound retention, and protect tenant identifiers. A long blocked interval is classified only after linking it to its predicate and owner.

### Answer 5

The interrupt publishes device result before completing the waiter under architecture-correct ordering. A timer races through one atomic resolution state; exactly one path owns result publication, wake, and terminal accounting, while both release their references. Priority and affinity analysis includes interrupt routing, scheduler policy, lock holders, migration, and other runnable tasks.

Shutdown closes new requests, disables and synchronizes the device interrupt, cancels timers synchronously, resolves outstanding operations, wakes and joins task context, and only then frees state. Define safe behavior for device loss, late interrupt, timeout boundary, CPU loss, and overload. Measure end-to-end deadline behavior under fault and stress without treating observed maxima as proof. Named driver, concurrency, real-time, platform, safety, independent-verification, and acceptance owners review the argument; this module claims no certification.
