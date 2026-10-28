---
module_id: OS-014
program: Operating Systems
level: 1
module_number: 14
title: Context Switching
status: complete
last_verified: 2026-09-04
---

# Context Switching

## One-Page Review

### Governing question

How can an operating system stop one execution context, preserve exactly the state needed to resume it, select another context, and transfer control without corrupting either context or mistaking the transfer cost for the scheduler's policy?

### Essential definitions

- A **context switch** transfers a processor from one schedulable context to another after saving the outgoing context and restoring the incoming one.
- A **mode transition** changes privilege or execution mode while the same task continues; a system call need not cause a context switch.
- A **voluntary switch** follows an action such as blocking for input or waiting; an **involuntary switch** follows preemption, quantum expiration, or a higher-priority runnable task.
- **Architectural state** is software-visible processor state such as the program counter, stack pointer, general registers, control state, and selected extension state.
- **microarchitectural state** includes caches, predictors, translation caches, and pipelines; it affects cost but is not normally restored as a task image.
- An **address-space identifier (ASID)** or **process-context identifier (PCID)** tags translations so selected TLB entries can survive an address-space change under architecture rules.
- A **switch boundary** is the interval in which scheduler ownership and the processor's current-task identity move from the outgoing task to the incoming task.

### Central model, mechanism, or theorem

Represent task `i` by saved architectural state `R_i`, kernel stack `K_i`, address-space context `A_i`, scheduler state `Q_i`, and owned extension state `X_i`. A correct transfer from `i` to `j` establishes:

`running(i) -> saved(i) -> current := j -> address(j) -> restored(j) -> running(j)`.

The arrows express an implementation protocol, not ordinary user-visible events. Interrupt entry may save a trap frame, the scheduler may save a smaller callee-saved context, and return-from-exception may restore the rest. Correctness depends on matching save and restore conventions and on publishing scheduler state under the required locks and barriers.

### Critical invariants

- At most one processor owns a non-migratable running task context at a time.
- Every non-running resumable task has a complete saved representation for its next restore path.
- The current-task pointer, active kernel stack, address-space context, and accounting owner describe the same task before ordinary execution resumes.
- An outgoing task becomes non-running before another processor may run it; a migrating task is queued or running in exactly one place.
- Address-space activation obeys page-table lifetime, ASID or PCID generation, and TLB invalidation rules.
- Extended state belongs to the correct task whether the kernel uses eager or lazy save and restore.
- A context switch does not by itself establish a language-level happens-before edge between unrelated shared-memory accesses.

### Common failures

Common mistakes are calling every syscall a context switch, saving too little state, restoring registers with the wrong ABI convention, switching stacks before state is reachable, exposing one task as current on two CPUs, reusing an address-space tag without invalidation, freeing page tables during activation, losing floating-point or vector state, sleeping while preemption is forbidden, charging interrupt time to the wrong task, reading cumulative switch counters as latency, benchmarking only warm-cache switches, and treating the switch routine as the entire scheduling system.

### Compact example

Task A enters the kernel because a timer interrupt made task B eligible. Entry code saves A's user return state on A's kernel stack. Scheduler code accounts A's runtime, changes its state from running to runnable, enqueues it, selects B, and invokes the architecture switch path. That path saves the kernel continuation needed for A, makes B the processor's current task and stack owner, activates B's address space if required, restores B's saved kernel continuation, and returns through B's earlier scheduler call. Later exception return restores B's user registers. The scheduler chose B; the context-switch mechanism merely made that choice executable.

### Connections

[OS-004](004-interrupts-and-exceptions.md) explains trap entry, [OS-013](013-threads-and-execution-contexts.md) defines task-private state, [OS-015](../ROADMAP.md) develops wait queues, and [OS-016](../ROADMAP.md) develops scheduling policy. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies privilege, register, cache, TLB, and pipeline mechanisms.

## Governing Question

A running thread is distributed across hardware registers, a kernel stack, scheduler metadata, address-space machinery, and sometimes floating-point, vector, debug, accelerator, or protection state. Stopping it safely is not equivalent to copying a single structure. Some state was already saved by interrupt entry, some follows the calling convention, some is owned lazily, and some is deliberately discarded and reconstructed.

The switch also crosses ownership boundaries. A run-queue lock protects scheduler state, architecture code changes stacks and address spaces, tracing observes the boundary, accounting assigns time, and a returning function may resume in a different task from the one that called the switch primitive. Bugs here can resume at the wrong instruction, expose another task's register contents, run a task concurrently on two processors, or use stale translations after page tables are freed.

The governing question is therefore not merely “which registers are copied?” It is how the system establishes a coherent new current context across architectural, virtual-memory, scheduler, synchronization, accounting, security, and lifecycle domains.

## Why This Matters

Context switching enables blocking, preemption, multiprogramming, isolation, priorities, and responsive sharing of processors. Without it, a task waiting for storage, a network packet, or a timer could strand a CPU, and an uncooperative task could monopolize execution.

Its direct cost includes entry, scheduling, state save and restore, address-space activation, and return. Its indirect cost can be larger: displaced cache lines, TLB misses, predictor disruption, migration, lost locality, and contention after wakeup. The cost depends on workload, processor, mitigations, topology, cache state, address-space relationship, extension use, and measurement method. There is no honest universal “cycles per context switch” constant.

Correctness and cost interact. Lazy state management can avoid work but adds ownership transitions and fault paths. Long quanta reduce switch frequency but hurt latency. Affinity preserves locality but can create imbalance. Real-time systems need bounded interference and blocking analysis, not only average throughput. Security controls may intentionally flush or partition state at a transition.

## Prerequisites and Retrieval

Recall from [OS-004](004-interrupts-and-exceptions.md) that exception entry constructs a return context. Recall from [OS-011](011-processes-and-address-spaces.md) that threads can share or change address spaces. Recall from [OS-013](013-threads-and-execution-contexts.md) that each thread has private registers, stacks, scheduler state, signal state, and TLS while sharing process resources.

Retrieve these distinctions:

- mechanism transfers control; policy chooses who runs;
- a privilege transition can return to the same task;
- user registers, kernel continuation state, and extension state can use different save paths;
- architectural state must be restored, while microarchitectural state mostly becomes interference;
- per-CPU current-task state must agree with the active stack and accounting owner;
- a TLB is not the page table and a TLB flush does not free page tables;
- cumulative counts, scheduler delay, switch duration, wakeup latency, and application response time are different metrics.

## Learning Objectives

After this module, you should be able to:

1. distinguish context switches from mode transitions, interrupts, scheduler decisions, migrations, and user-level coroutine transfers;
2. partition task state into entry-saved, switch-saved, address-space, extension, and reconstructed components;
3. explain a switch protocol and state its ownership, run-queue, stack, and memory-management invariants;
4. compare eager and lazy state handling, tagged and flushed translations, and kernel and user scheduling;
5. identify correctness, security, real-time, and lifecycle failures around the switch boundary;
6. design measurements that separate direct switch cost from wakeup, scheduling, migration, and cache effects;
7. evaluate switch-frequency trade-offs without assuming that fewer switches always improve a system.

## Core Exposition

### What changes and what does not

A system call, interrupt, or exception normally changes privilege and enters the kernel on behalf of the current task. If the kernel handles the event and returns to that task, there was a mode transition but no task context switch. A switch occurs only when the processor's schedulable ownership changes.

A switch need not change every resource. Threads in one process may share an address space, so switching between them can retain the same top-level page-table context. A kernel thread may borrow or avoid a user address space under implementation-specific rules. Conversely, migration moves a task between CPUs and changes locality even if its address space is unchanged.

### Sources of a switch

A task switches voluntarily when it cannot or chooses not to continue: it waits on a condition, performs blocking I/O, sleeps until a deadline, joins another task, or explicitly yields. The kernel must first publish the wait condition and task state without losing a concurrent wakeup.

An involuntary switch follows a scheduling event while the task remains logically able to run. A timer can end a time slice, a newly runnable task can outrank the current one, a CPU can require load balancing, or policy can throttle a budget. Interrupt entry creates an opportunity to reconsider scheduling; it does not guarantee that another task will be selected.

### State partitioning

The save set is architecture and kernel dependent. A useful partition is:

- **return state:** user program counter, user stack pointer, flags or status, and registers required by exception return;
- **kernel continuation:** kernel stack pointer and callee-saved registers needed to resume the blocked or preempted kernel path;
- **address-space state:** page-table root, address-space tag, protection keys, and related generation metadata;
- **extension state:** floating-point, SIMD, vector, matrix, debug, performance-monitoring, or accelerator state;
- **scheduler state:** run state, queue membership, CPU assignment, policy, priority, runtime, deadline, and accounting data;
- **per-CPU binding:** current-task pointer, active kernel stack, local scheduler context, and architecture-specific thread fields.

Not every field is copied at the lowest switch function. Entry code may have already saved volatile user registers. A switch function can rely on its kernel ABI to preserve only callee-saved registers and its return address. Exception return later restores the trap frame. Correct review follows the entire entry-switch-return chain.

### Kernel stacks and control transfer

Each ordinary kernel task context needs a stable place for nested calls, saved registers, and return frames. Before abandoning the outgoing stack, the kernel records a continuation reachable from task metadata. It then activates the incoming stack and resumes at that task's saved continuation.

The apparent control flow is unusual: task A calls a low-level switch, but when A eventually runs again, that call returns in A, possibly long after task B and many others ran. Local variables remain meaningful only because they reside on A's preserved kernel stack and because their referenced objects remain alive.

Interrupt stacks, entry stacks, shadow stacks, or architecture-specific exception stacks can complicate this picture. Their existence does not remove the need to identify which task owns the resumable continuation and how entry frames connect to it.

### Scheduler boundary and locking

The scheduler must transform one coherent state into another. A simplified path is:

1. enter with scheduling permitted and relevant preemption state known;
2. account time and determine the outgoing task's next state;
3. enqueue it if still runnable, or confirm its wait protocol if blocked;
4. select and dequeue an eligible incoming task;
5. transfer run-queue and processor ownership under the scheduler's locking rules;
6. invoke architecture-specific address-space, stack, register, and task activation;
7. finish bookkeeping and release locks in the context expected by the implementation;
8. process pending work and return to kernel or user execution.

The exact lock handoff can span the low-level switch. Therefore generic code must not infer ownership solely from the source-level call stack. Assertions about preemption count, interrupt state, run-queue lock ownership, and task state are valuable boundary checks.

### Address spaces and translations

When incoming and outgoing tasks use different address spaces, the kernel activates the incoming page-table context. Architectures may flush translations, tag them with an ASID or PCID, or preserve selected global entries. Tags are finite and reusable, so the operating system needs generation and invalidation rules that prevent an old translation from being interpreted as belonging to a new address space.

Page-table lifetime is concurrent with switching. An address space cannot be destroyed while a CPU can still use its tables or cached translations. Reference counts, CPU masks, shootdown protocols, barriers, and grace periods cooperate to close this race. The architecture specification defines ordering and invalidation instructions; the kernel defines the lifecycle protocol around them.

Switching between threads that share an address space can avoid top-level activation work, but it does not eliminate TLB or cache interference. Migration to a different CPU may encounter cold local structures, and another task can evict shared cache lines without changing address spaces.

### Extended processor state

Eager switching saves and restores extension state at every relevant task switch. It has a simple ownership model and predictable cost but may move large state that neither task uses. Lazy switching records the owner and traps or otherwise mediates the next use, avoiding some copies but expanding the correctness and security state machine.

Modern designs often choose eager handling for some state and optimized conditional handling for other components. Review must cover first use, nested kernel use, interrupts, migration, task exit, hotplug, virtualization, signal frames, and leakage across protection domains. “Lazy is faster” is not a sufficient design argument.

### Memory ordering and synchronization

The switch implementation uses locks, atomics, and architecture barriers to publish task and run-queue state. Those mechanisms create specific kernel-internal ordering. The mere fact that task B ran after task A on one CPU does not automatically synchronize their ordinary shared-memory accesses under a programming-language memory model.

Applications synchronize through mutexes, atomics, condition variables, semaphores, channels, or other specified protocols. Kernel wait and wake paths likewise require a predicate and ordering contract. A context switch can be an observed consequence of blocking, but it is not the application's synchronization primitive.

### Accounting and observability

Systems expose context-switch counts, CPU time, scheduler delay, migrations, run-queue statistics, trace events, and performance counters. Linux `getrusage` separates voluntary and involuntary switch counts; `/proc/PID/stat` supplies task statistics; scheduler statistics and `sched_switch` trace events expose other views. Each interface has enablement, permission, unit, version, and overhead constraints.

A trace timestamp difference around a switch includes the instrumented boundary, not necessarily all cache and translation recovery. Wakeup-to-run latency begins before the switch. End-to-end response includes queueing and work. Performance counters can reveal cache or TLB behavior but require attribution, multiplexing, privilege, and sampling analysis.

### Direct and indirect cost

Let useful execution time be `U`, measured direct transfer time be `D`, and measured recovery or interference time attributed by an explicit model be `I`. For an observation window with `n` switches, one illustrative efficiency is:

`E = U / (U + D + I)`.

This is an accounting model, not a universal decomposition: work can overlap, counterfactual cache behavior is difficult to identify, and instrumentation perturbs the path. Report distributions and workload metadata rather than one average.

### User-level context switching

Coroutines, fibers, language runtimes, and green threads can transfer among user contexts without asking the kernel to schedule a different kernel thread. Such a transfer may save a smaller register set and avoid privilege entry, but the kernel still sees the carrier thread as running. A blocking syscall can strand all user contexts on that carrier unless the runtime uses asynchronous I/O, multiple carriers, or scheduler integration.

User runtimes must preserve ABI state, stack lifetimes, TLS assumptions, signals, foreign calls, exceptions, unwinding, sanitizers, debuggers, and profiler visibility. Lower mechanism cost can buy greater integration complexity.

### Security and isolation

Architectural registers must not leak between tasks. Extension, debug, performance, protection, and speculative state require equally explicit policies. Some mitigations flush or restrict prediction and translation structures at selected domain transitions; their need and cost depend on processor, threat model, firmware, kernel, and configuration.

Trace access and timing measurements can also expose sensitive activity. Production observability needs least privilege, bounded retention, tenant separation, and an explicit decision about whether tracing changes the property being measured.

### Real-time and assurance boundaries

Real-time analysis cares about preemption latency, dispatch latency, blocking, interrupt interference, migration, cache refill, TLB work, and the worst permitted extension-state path. An average switch benchmark proves none of these bounds. CPU isolation and affinity can reduce interference but also reduce redundancy and load-balancing options.

Safety-relevant systems need reviewed task sets, priorities, budgets, stack bounds, shutdown behavior, overload policy, measurement coverage, hardware configuration, and residual risk. A chapter, trace, or toy model is evidence input, not certification.

## Definitions and Notation

Let `T_i` be task `i`, `R_i` its saved architectural registers, `K_i` its kernel stack and continuation, `A_i` its address-space context, `X_i` its extension state, and `Q_i` its scheduler state. Let `cpu(T_i)` be the CPU that currently owns a running task or `none` when it is not running.

Let task state be one of `running`, `runnable`, `blocked`, `stopped`, or `dead`, refined by implementation-specific transient states. Let `current_c` name the current task of CPU `c`. Let `owner(X)` identify the task whose extension state is resident where lazy ownership exists.

Define a switch event `S(i, j, c)` as CPU `c` transferring schedulable ownership from `T_i` to `T_j`. Define `D_k` as measured direct duration for observed switch `k`, and `L_k` as a separately defined latency such as wakeup-to-run. These quantities must not be silently substituted for one another.

Required properties include:

- **uniqueness:** `cpu(T_i)` names at most one CPU;
- **coherence:** if `current_c = T_i`, the active stack, address-space context, and accounting context match `T_i`;
- **resumability:** a non-running live task has a complete valid restore path;
- **queue integrity:** a task is not simultaneously running and queued, or queued twice, unless an explicitly modeled transient owns that representation;
- **translation safety:** every usable tagged translation belongs to the active address space and current tag generation;
- **extension confidentiality:** restored extension state belongs to the incoming protection context;
- **lifecycle safety:** referenced task, stack, page-table, and tracing objects outlive every CPU that can access them.

## Mechanisms, Invariants, or Proof Structure

A reviewable switch argument can use five layers.

1. **Entry completeness.** Prove that the interrupt, exception, syscall, or voluntary-block path preserves all state needed to resume the outgoing execution. Name which layer owns volatile registers and the user return frame.
2. **Scheduler exclusivity.** Under run-queue and task-state synchronization, prove the outgoing task ceases to be running before it can be enqueued or migrated, and the incoming task is removed from competing ownership before activation.
3. **Architecture coherence.** Prove stack, current-task identity, address space, extension ownership, and required barriers move in an order that exposes no mixed context to normal execution.
4. **Return completeness.** Prove the restored kernel continuation reaches the appropriate exception-return or blocked-call continuation and restores remaining state exactly once.
5. **Lifetime closure.** Prove exit, address-space destruction, CPU hotplug, tracing teardown, and migration wait for all references and stale hardware use to end.

For an abstract cost window, the following executable model keeps direct switch time separate from useful runtime. It does not execute threads or measure hardware.

<!-- bijux-verify: {"id":"toy-switch-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"useful-ms=6.00\nswitch-ms=0.40\nelapsed-ms=6.40\nefficiency=93.75%\n","stderr":""}} -->
```python
from decimal import Decimal

timeline = [
    ("run-A", Decimal("3.00")),
    ("switch-A-B", Decimal("0.20")),
    ("run-B", Decimal("2.00")),
    ("switch-B-A", Decimal("0.20")),
    ("run-A", Decimal("1.00")),
]

useful = sum((duration for name, duration in timeline if name.startswith("run")), Decimal(0))
switch = sum((duration for name, duration in timeline if name.startswith("switch")), Decimal(0))
elapsed = useful + switch
efficiency = Decimal(100) * useful / elapsed

print(f"useful-ms={useful:.2f}")
print(f"switch-ms={switch:.2f}")
print(f"elapsed-ms={elapsed:.2f}")
print(f"efficiency={efficiency:.2f}%")
```

The arithmetic gives `U = 6.00 ms`, `D = 0.40 ms`, elapsed time `6.40 ms`, and `E = 93.75%`. It excludes scheduler search, wakeup delay, interrupts, migration, cache and TLB recovery, instrumentation, and overlapping effects. Those exclusions prevent a bookkeeping example from becoming a hardware-performance claim.

## Alternatives and Trade-Offs

- **Cooperative versus preemptive scheduling:** cooperation simplifies some invariants but lets a task delay peers; preemption improves responsiveness while expanding synchronization and reentrancy requirements.
- **Long versus short quanta:** long quanta amortize direct switch cost and retain locality; short quanta can reduce interactive delay but increase switching and interference.
- **Eager versus lazy extension state:** eager transfer simplifies ownership and timing; lazy or conditional transfer avoids unused copies but adds traps, metadata, and leakage risks.
- **Flush versus tag translations:** flushing is conceptually direct; ASIDs or PCIDs preserve useful translations but require finite-tag reuse and generation correctness.
- **Affinity versus migration:** affinity preserves locality and predictability; migration improves balance and availability but can make caches, NUMA placement, and timing worse.
- **Kernel threads versus user fibers:** kernel scheduling integrates blocking, priorities, accounting, and multicore execution; user switching can be cheaper but shifts blocking and tooling integration to the runtime.
- **Rich tracing versus perturbation:** detailed events improve diagnosis; probes consume time, storage, and authority and can alter the schedule.
- **Average optimization versus worst-case control:** throughput tuning targets common paths; real-time assurance must include rare state, invalidation, interrupt, and mitigation paths.

## Failure Modes and Misconceptions

1. **“Every syscall switches context.”** It changes privilege, but often returns to the same task.
2. **“The scheduler and switch routine are the same.”** Policy selects a task; architecture mechanism transfers state.
3. **“Save all registers in one structure.”** Entry, calling convention, switch code, and exception return can divide responsibility.
4. **“Only general registers matter.”** Address-space, extension, debug, protection, and scheduler state can affect correctness or confidentiality.
5. **“Switching threads never touches the MMU.”** Shared address spaces help, but per-thread protection or architecture state and migration can still matter.
6. **“Tagged TLB entries never need flushing.”** Tags are finite, reused, and governed by generation and invalidation protocols.
7. **“Disabling preemption solves scheduler races.”** It is local and does not replace inter-CPU synchronization or interrupt rules.
8. **“A switch is a memory barrier for applications.”** Application ordering comes from its specified synchronization operations.
9. **“The caller returns in the next task.”** Each task resumes its own preserved switch call and stack continuation.
10. **“Voluntary means harmless.”** Blocking can lose wakeups, violate lock rules, or create unbounded priority inversion.
11. **“A context-switch count measures overhead.”** It is a count, not duration, cache recovery, or end-to-end latency.
12. **“A tight ping-pong benchmark is representative.”** It selects warm paths, fixed topology, particular system calls, and a synthetic workload.
13. **“Fewer switches always improve performance.”** Delaying preemption or wakeup can reduce responsiveness, parallelism, and device utilization.
14. **“Average switch time establishes a deadline bound.”** Rare invalidations, extension use, interrupts, migrations, and queueing dominate worst cases.

## Worked Examples

### Example 1

A task executes a read syscall whose data is already cached. The processor enters the kernel, copies data, and returns to the same task. There are privilege transitions and an exception frame, but no scheduler ownership transfer. Instrument syscall entry and exit separately from `sched_switch`.

### Example 2

A task waits on an empty queue. While holding the queue protocol's lock, it verifies the predicate, marks itself blocked, links its wait entry, and releases ownership through the scheduler path. A producer changes the predicate and wakes it under the matching ordering contract. The switch is a consequence; predicate synchronization prevents a lost wakeup.

### Example 3

A timer interrupts task A. Entry saves A's user return frame, but the scheduler chooses A again because no peer outranks it. This is interrupt entry plus scheduling evaluation, not a task switch. A trace should show interrupt events without an A-to-B switch.

### Example 4

Two threads in one process switch on one CPU. Their top-level address space is shared, yet their stacks, TLS, signal masks, registers, scheduler state, and kernel continuations differ. Avoiding a page-table-root change reduces one component but does not guarantee warm caches or zero cost.

### Example 5

Two processes use distinct address spaces with ASID tags. When a finite tag is recycled, the kernel associates it with a new generation and invalidates translations that could retain the old meaning. Reassigning the integer alone would allow stale physical mappings to cross isolation boundaries.

### Example 6

Task A uses vector registers and task B does not. An eager design saves A and restores B's initialized vector state every switch. A conditional design tracks use and ownership, but must handle B's first vector instruction, signals, migration, exit, and kernel vector use. Benchmark both with used and unused extension state.

### Example 7

A profiler reads voluntary and involuntary switch counts for a service. Counts rise after a deployment, but latency falls because workers block promptly rather than spin and starve the I/O thread. Counts are diagnostic context, not a monotonic performance objective.

### Example 8

A ping-pong test pins two tasks to one CPU and measures event-to-event time. The result includes signaling, wakeup, scheduler selection, two transfers, clock reads, and tracing—not just low-level register save and restore. Report the measured operation instead of relabeling it “switch cycles.”

### Example 9

A task migrates from CPU 0 to CPU 3 after waking. Its architectural restore is correct, but its working set and translations are cold on CPU 3, and its memory is remote. Direct switch duration stays modest while request latency rises. Per-CPU traces and topology metadata reveal the distinction.

### Example 10

A real-time controller reserves one CPU, routes selected interrupts elsewhere, pins its critical task, pre-faults memory, bounds stacks, and measures wakeup-to-output latency under stress. Review still includes firmware events, thermal controls, rare extension state, overload, and hardware failure. A low median context-switch time is insufficient assurance.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains privilege transitions, calling conventions, register files, caches, TLBs, ASIDs, speculation, and atomic ordering. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) explains happens-before and why scheduling order alone is not synchronization.

[Programming Languages: Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) connects stacks, coroutines, unwinding, ABI state, TLS, and runtime schedulers. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames latency budgets, capacity, observability, fault containment, and assurance.

Within this program, [OS-015](../ROADMAP.md), [OS-016](../ROADMAP.md), [OS-017](../ROADMAP.md), [OS-018](../ROADMAP.md), and [OS-019](../ROADMAP.md) develop task states, policy, algorithms, multicore scheduling, and real-time scheduling. [OS-021](../ROADMAP.md) develops the kernel synchronization that protects switch boundaries.

## References

- Linux man-pages project, [sched(7)](https://man7.org/linux/man-pages/man7/sched.7.html), current page checked 2026-09-04. Scheduling policies, priorities, preemption, CPU-time control, and autogroup behavior.
- Linux man-pages project, [sched_yield(2)](https://man7.org/linux/man-pages/man2/sched_yield.2.html), current page checked 2026-09-04. Explicit yielding semantics, policy dependence, caveats, and errors.
- Linux man-pages project, [getrusage(2)](https://man7.org/linux/man-pages/man2/getrusage.2.html), current page checked 2026-09-04. Per-process and per-thread CPU accounting and voluntary and involuntary context-switch counts.
- Linux man-pages project, [perf_event_open(2)](https://man7.org/linux/man-pages/man2/perf_event_open.2.html), current page checked 2026-09-04. Performance events, context-switch records, sampling, attribution, permissions, and multiplexing.
- Linux man-pages project, [proc_pid_stat(5)](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html), current page checked 2026-09-04. Process state, CPU times, processor, priority, and scheduling-related task statistics.
- Linux Kernel documentation, [Scheduler Statistics](https://docs.kernel.org/scheduler/sched-stats.html), current page checked 2026-09-04. Run, wait, wakeup, and domain statistics with version and enablement constraints.
- Linux Kernel documentation, [Using the Linux Kernel Tracepoints](https://docs.kernel.org/trace/events.html), current page checked 2026-09-04. Event discovery, enabling, filtering, and tracepoint interface behavior.
- Linux Kernel documentation, [Entry/Exit Handling for Exceptions, Interrupts, Syscalls and KVM](https://docs.kernel.org/core-api/entry.html), current page checked 2026-09-04. Entry state, lockdep, RCU, tracing, instrumentation, and ordering constraints.
- Linux Kernel documentation, [The TLB](https://docs.kernel.org/arch/x86/tlb.html), current page checked 2026-09-04. x86 TLB flushing trade-offs, invalidation scope, and performance counters.
- Linux Kernel documentation, [CPU Idle Time Management](https://docs.kernel.org/admin-guide/pm/cpuidle.html), current page checked 2026-09-04. Scheduler idle-loop interaction, idle-state selection, latency, and tick effects.
- RISC-V International, [The RISC-V Instruction Set Manual, Supervisor-Level ISA](https://docs.riscv.org/reference/isa/priv/supervisor.html), current page checked 2026-09-04. Trap state, `satp`, ASIDs, address translation, and fence requirements.
- Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), current page checked 2026-09-04. Architectural registers, privilege, interrupts, task management, paging, PCIDs, and invalidation instructions.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching context structures, per-process kernel stacks, scheduler switching, sleep, wakeup, locks, and RISC-V trap return.

## Exercises

### Exercise 1

Trace a timer-driven switch from user task A to user task B. Partition state among hardware or assembly entry, A's trap frame, A's kernel switch frame, scheduler metadata, address-space activation, B's switch frame, and exception return. State the invariant at each ownership transfer.

### Exercise 2

For the toy timeline, recompute useful time, direct switch time, elapsed time, and efficiency. Then add `0.30 ms` of explicitly attributed recovery after each of two switches. Explain why the revised number is still not a general hardware claim.

### Exercise 3

Design a benchmark matrix that separates same-process and cross-process switches, same-CPU and migration cases, warm and pressured caches, used and unused vector state, idle and loaded run queues, and tracing off and on. Define observed variables and limitations.

### Exercise 4

Review an ASID allocator with eight-bit tags on a long-running multicore system. Specify allocation, generation rollover, per-CPU activation, invalidation, migration, address-space destruction, and CPU hotplug obligations.

### Exercise 5

Construct an assurance argument for a preemptive real-time task whose deadline depends on dispatch. Include wait and wake paths, scheduler policy, locks, interrupts, migration, address spaces, extension state, tracing, hardware configuration, overload, and human review.

## Answers to the Exercises

### Answer 1

Timer entry preserves A's user return PC, stack, status, and required registers on an entry or task-associated frame while establishing kernel mode and a valid kernel stack. The entry invariant is that A remains current and resumable even though it is interrupted. Scheduler code accounts A, decides it remains runnable, and under run-queue synchronization moves it from running ownership to one valid queue position.

Selection removes B from runnable competition and reserves it for this CPU. The low-level path stores A's kernel stack pointer and callee-saved continuation, changes current-task and active-stack ownership coherently, activates B's address space with lifetime and TLB rules, and restores B's continuation. B's returning scheduler path completes lock and bookkeeping obligations. Exception return restores B's saved user frame. At no point may A or B be current on two CPUs, queued twice, or represented by a mixed stack and address space.

### Answer 2

The useful intervals sum to `3.00 + 2.00 + 1.00 = 6.00 ms`. Two direct intervals sum to `0.40 ms`, so elapsed is `6.40 ms` and efficiency is `6.00 / 6.40 = 0.9375`, or `93.75%`.

Two recovery charges add `0.60 ms`; under that declared accounting model, total is `7.00 ms` and attributed efficiency is about `85.71%`. Recovery may overlap useful work, counterfactual cache misses are hard to identify, and the hard-coded durations omit scheduler search, wakeup, interrupts, migration, measurement, and workload variation. The result explains the model, not a processor.

### Answer 3

Use a factorial matrix with same-process versus separate address spaces; pinned same-CPU versus permitted migration; warmed private working sets versus controlled cache pressure; vector instructions absent versus a declared vector footprint; zero, moderate, and overloaded peer run queues; and identical runs with tracing disabled and enabled. Record processor, topology, kernel, firmware, mitigations, power policy, clock source, affinity, memory placement, and tool versions.

Measure the exact ping-pong operation distribution, switch trace intervals, wakeup-to-run latency, migrations, CPU time, switch counts, cache and TLB events where reliable, and application completion. Include calibration and observer overhead. Randomize run order, repeat across boots, retain raw artifacts, and report quantiles and tails. The matrix remains workload-specific and does not isolate every causal microarchitectural effect or establish worst-case bounds.

### Answer 4

Treat a tag as `(value, generation)`, not an eternal address-space identity. Allocation may use a free value within the current generation. On exhaustion or rollover, establish an architecture-correct global or per-CPU invalidation boundary before old tagged translations can be confused with new assignments. A CPU records which generation it has observed and validates the address space during activation.

Migration applies the destination CPU's activation and invalidation rules. Destruction removes new reachability, waits for every CPU that could retain or use the address space, invalidates as required, and only then frees tables. Hotplug must join or leave the generation protocol without preserving untracked translations. Wrap arithmetic, concurrent allocation, delayed shootdowns, virtualization, and noncoherent invalidation are adversarial cases. Exact barriers and fences come from the target architecture and kernel design.

### Answer 5

Define release, deadline, useful work, admissible jitter, safe output, and overload action. Trace the predicate-changing producer through wakeup, run-queue insertion, preemption decision, low-level transfer, cache and TLB recovery, and output. Bound priority inversion, every critical section, nonpreemptible interval, interrupt path, migration, page fault, allocation, extension-state operation, and mitigation relevant to the configuration.

Choose policy, priority, affinity, CPU isolation, interrupt routing, memory locking, stack margin, address-space arrangement, and budgets from analysis rather than folklore. Measure wakeup-to-output distributions under representative and adversarial load while retaining configuration and traces; do not replace analytical bounds with observed maxima. Test overload, missed releases, tracing failure, CPU loss, and shutdown. Named real-time, scheduler, architecture, concurrency, platform, safety, independent-verification, and acceptance owners must review assumptions and residual risk. This module claims no certification.
