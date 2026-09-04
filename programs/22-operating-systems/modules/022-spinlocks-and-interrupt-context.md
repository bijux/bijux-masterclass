---
module_id: OS-022
program: Operating Systems
level: 1
module_number: 22
title: Spinlocks and Interrupt Context
status: complete
last_verified: 2026-09-04
---

# Spinlocks and Interrupt Context

## One-Page Review

### Governing question

When shared kernel state is reachable from task and interrupt contexts, which spinlock and interrupt-state protocol prevents both inter-CPU races and local reentrant deadlock without violating latency or real-time constraints?

### Essential definitions

- A **spinlock** is a non-sleeping mutual-exclusion abstraction whose exact behavior depends on kernel configuration and lock type.
- **hard-interrupt context** executes in response to a hardware interrupt under restricted scheduling and blocking rules.
- **soft-interrupt context** is deferred interrupt work with its own preemption and serialization semantics.
- **IRQ-safe locking** prevents a relevant local interrupt from entering a handler that would acquire the held lock.
- **IRQ save/restore** records the caller's prior interrupt state, disables interrupts as required, then restores that exact state.
- A **raw spinlock** retains strict low-level spinning semantics where ordinary spinlocks may become sleeping locks on PREEMPT_RT.
- **preemption count or state** tracks nesting of contexts that constrain task preemption under implementation rules.
- **interrupt latency** is delay from an interrupt becoming pending to permitted handler service; long masked sections contribute to it.

### Central model, mechanism, or theorem

Let accessor contexts for lock `L` include remote CPUs and possibly a local interrupt handler. The lock excludes simultaneous CPUs; local IRQ control prevents the handler from preempting a task that holds the same lock and spinning forever. A common task-side protocol is:

`flags = irqsave(); spin_lock(L); mutate; spin_unlock(L); irqrestore(flags)`.

The handler, already in its documented interrupt state, uses the matching lock form. The precise API and ordering come from the target kernel. If NMI-like context can access the state, ordinary IRQ masking may still be insufficient and the design may need stronger primitives or ownership restructuring.

### Critical invariants

- The lock's protected invariant and every task, hard-IRQ, soft-IRQ, threaded-IRQ, NMI-like, and remote-CPU accessor are documented.
- No holder executes an operation that can sleep, fault, or acquire an illegal dependency in its current context.
- Local interrupt and bottom-half state are restored to the exact state observed on entry, with balanced nesting.
- The selected lock type has the required semantics on every supported preemption and PREEMPT_RT configuration.
- All nested acquisitions obey a global lock-class order, including handler and teardown paths.
- Lock hold and IRQ-masked duration are bounded under admitted work and measured under representative interference.
- Device disable, interrupt synchronization, deferred-work drain, and reclamation close teardown races.

### Common failures

Common mistakes are using plain spin locking in task context when a local handler takes the same lock, assuming local IRQ disable excludes remote CPUs, enabling interrupts rather than restoring saved state, nesting unmatched IRQ operations, sleeping while locked, holding a lock across device I/O with unbounded completion, taking locks in reversed handler order, treating softirq and hard IRQ as identical, using ordinary spinlocks where raw semantics are required on PREEMPT_RT, and optimizing average hold time while ignoring latency tails.

### Compact example

A network ring is mutated by process configuration code and a hard-interrupt handler on multiple CPUs. Process code saves local IRQ state, disables interrupts, acquires the ring lock, changes head, tail, and ownership together, unlocks, then restores the saved state. The handler takes the same lock but performs only bounded non-sleeping work and defers expensive processing. Shutdown masks the device source, synchronizes the IRQ, drains deferred work, takes the lock to detach the ring, and frees it only after no accessor remains.

### Connections

[OS-004](004-interrupts-and-exceptions.md) defines interrupt entry, [OS-021](021-critical-sections-in-the-kernel.md) defines invariant and lifetime proofs, and [OS-023](../ROADMAP.md) contrasts sleepable primitives. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains interrupt masking, atomic instructions, caches, and memory ordering.

## Governing Question

A spinlock protects against simultaneous lock holders, but it does not automatically prevent a local interrupt from preempting its holder and trying to acquire the same lock. The handler cannot sleep and the interrupted holder cannot resume, so both wait forever. Conversely, disabling local interrupts without a lock leaves remote CPUs free to corrupt the object.

The safe protocol depends on the whole context matrix. State reached only from task context may use a mutex. State shared with a hard interrupt needs a non-sleeping design and local reentry control. State shared with soft interrupts may require bottom-half control. NMI-like access has stronger restrictions. A threaded interrupt is schedulable but has priority and teardown concerns.

The governing question is not “should this use a spinlock?” It is which contexts contend, which can preempt locally, which may sleep, which configuration transformations apply, and how long exclusion may delay urgent work.

## Why This Matters

Incorrect interrupt locking produces system-wide deadlock, data corruption, missed device service, or use-after-free. These failures often need precise coincidence between task code, device interrupts, another CPU, and teardown, so ordinary testing may miss them.

Correct but oversized sections harm latency. Interrupt masking delays all affected local handlers, not only the one related to the lock. Spinning consumes processor time and creates cache-line contention. A bounded average says little about rare long paths, page faults, debug output, or hardware interactions.

Real-time kernel configurations alter assumptions. Linux documents that ordinary spinlock types may map to sleeping implementations on PREEMPT_RT, while raw spinlocks retain strict semantics. Code must select by required semantics, not historical intuition.

## Prerequisites and Retrieval

Recall context matrices, invariants, lock ordering, and lifetime from [OS-021](021-critical-sections-in-the-kernel.md). Recall interrupt entry from [OS-004](004-interrupts-and-exceptions.md), task preemption from [OS-014](014-context-switching.md), and wait restrictions from [OS-015](015-process-states-and-wait-queues.md).

Retrieve these distinctions:

- lock acquisition excludes other holders; IRQ masking prevents selected local entry;
- preemption disable does not disable interrupts or exclude other CPUs;
- hard IRQ, soft IRQ, threaded IRQ, work queue, and NMI-like contexts differ;
- `irqsave` captures state; unconditional enable invents a new state;
- spinlock, raw spinlock, mutex, and local lock semantics depend on configuration;
- mutual exclusion does not by itself close object lifetime;
- hold-time average, observed maximum, and analytical latency bound are different claims.

## Learning Objectives

After this module, you should be able to:

1. build a context and preemption matrix for task, hard IRQ, soft IRQ, threaded IRQ, work queue, NMI-like, and remote-CPU paths;
2. distinguish plain, IRQ-disabling, IRQ-save, bottom-half, raw, and sleepable lock protocols;
3. explain nested interrupt-state restoration and construct early-enable counterexamples;
4. identify sleeping, faulting, lock-order, memory-order, and lifetime hazards inside handlers;
5. account for PREEMPT_RT and supported configuration semantics;
6. measure lock hold, spin wait, IRQ-off, preemption-off, and end-to-end device latency;
7. design teardown and assurance evidence without overstating runtime tools.

## Core Exposition

### Build the context matrix

For each protected object, enumerate task syscalls, kernel threads, hard interrupt handlers, threaded handlers, soft interrupts, timers, work queues, NMI-like diagnostics, remote CPUs, and teardown. Mark whether each path can run concurrently and whether it can preempt another locally.

The matrix determines the minimum protocol. If only task contexts access state, a mutex may be preferable. If a hard handler accesses it, the critical mutation cannot sleep. If task code can be interrupted by that handler, the task side must prevent local handler entry while it holds the shared spinlock.

### Plain spin locking

Plain spin locking excludes other lock holders and supplies documented acquire and release ordering. It can be appropriate when all callers already run in a context where relevant local interruption is impossible or when no local handler shares the lock.

Adding a new interrupt caller changes the proof. Call-site preconditions must be durable and checkable; relying on “currently called with interrupts off” without documentation invites later self-deadlock.

### IRQ disable versus IRQ save

An IRQ-disable lock form assumes or establishes a defined interrupt state and may pair with unconditional re-enable only where entry was known enabled and nesting rules allow it. An IRQ-save form records prior state and later restores it, composing safely with callers that already have interrupts disabled.

Restoration ordering matters: release the shared lock before re-enabling a handler that can acquire it. Flags are tied to the matching acquisition scope and should not be mixed across locks or returned from unrelated helpers.

### Nested state

Suppose an outer path entered with interrupts enabled, saves `enabled`, and disables. An inner helper saves `disabled`. The inner restore must keep interrupts disabled; only the outer restore may re-enable. An unconditional inner enable exposes the outer critical section to unexpected interruption.

Balanced nesting also applies to preemption and bottom-half controls. Underflow, double restore, early return, and error unwinding should be covered by assertions and structured cleanup.

### Local IRQ control is not SMP exclusion

While CPU 0 has local interrupts disabled, CPU 1 can execute task or interrupt code against the same object. The spinlock supplies inter-CPU exclusion. Local IRQ control closes only the preemption edge from selected handlers on CPU 0.

On a uniprocessor build, implementation optimization can hide this distinction. Design for the stated concurrency contract rather than behavior observed on one CPU count.

### Hard-interrupt constraints

Hard-interrupt handlers must use APIs permitted in that context. They cannot wait on ordinary mutexes, perform blocking allocation, sleep for hardware, or call arbitrary code that may fault. They should acknowledge or quiesce the source, capture bounded state, and defer expensive work.

Handler locks must account for nesting and interrupt priority where the platform permits it. A lock taken by an NMI-like path needs a protocol explicitly safe against ordinary IRQ-masking assumptions.

### Soft interrupts and bottom halves

Deferred interrupt execution reduces hard-handler work but remains constrained. Soft-interrupt work can run concurrently on other CPUs and may preempt or be interleaved with task paths according to kernel rules. Bottom-half disabling is a local serialization tool, not remote-CPU exclusion.

If task and soft-interrupt contexts share a lock, the task-side form commonly controls local bottom halves plus takes the lock. Exact APIs and PREEMPT_RT transformations must be read from current kernel documentation.

### Threaded interrupts

A threaded handler runs in schedulable task context and can use more sleepable mechanisms, but a small hard primary handler may still execute. Priority, affinity, oneshot masking, device state, and shutdown synchronization define the design.

Threading an interrupt is not permission for unbounded work. It competes under scheduler policy and may introduce priority inversion through mutexes. Latency analysis follows both primary and threaded portions.

### Spinlock versus raw spinlock

On non-real-time kernels, ordinary and raw spinlocks may appear similar in common paths. Linux lock-type documentation explains that PREEMPT_RT changes ordinary spinlock behavior while raw spinlocks remain strict spinning locks and retain low-level atomic-context expectations.

Use raw locks only where semantics require them, because they extend nonpreemptible or IRQ-constrained work and real-time blocking. Do not select them merely to silence a context warning; redesign work placement if possible.

### Preemption and per-CPU state

Disabling preemption can stabilize task access to per-CPU data by preventing migration, but interrupts may still access that CPU's data. A local lock abstraction can express CPU-local ownership and transform appropriately on real-time kernels when used correctly.

Per-CPU state reduces cache contention but needs aggregation, CPU hotplug, migration, and teardown rules. A pointer into per-CPU storage cannot safely escape beyond the protection that fixed its CPU.

### Memory ordering

Spinlock acquisition and release order protected memory under their documented contract. Code outside the lock, device memory operations, lockless flags, and DMA may require additional accessors or barriers. CPU memory barriers and device I/O ordering are not interchangeable.

Unlocking before data publication or waking another context through an unrelated flag without release/acquire pairing can expose incomplete state. State the publication edge rather than sprinkling barriers around symptoms.

### Lock ordering across contexts

If process path holds A and takes B while an interrupt holds B and takes A, IRQ masking for one lock does not repair the AB-BA graph. Include handler, deferred, timer, error, and teardown acquisitions in one lock-class order.

Lockdep can validate many executed class and IRQ-state dependencies. Correct annotations matter; false suppression can hide genuine paths. A clean run is coverage evidence, not proof.

### Hold-time and contention budgets

Bound operations performed while spinning or masked. Avoid loops over attacker-controlled or unbounded collections, slow console output, device polling, memory reclaim, and callbacks of unknown behavior. Snapshot under lock and process outside where invariants allow.

Measure acquisition count, contention, wait, hold time, IRQ-off duration, preemption-off duration, handler response, and device completion. Report distributions and worst observed samples with workload and instrumentation context.

### Interrupt lifecycle and teardown

Disabling a device source prevents new hardware assertions only under device semantics. Synchronizing the interrupt waits for in-flight handlers as documented. Deferred work, timers, and threaded handlers require their own cancellation or synchronization.

A safe sequence commonly closes admission, masks the device, synchronizes IRQ execution, drains deferred work, detaches shared state under its lock, waits for readers or references, and frees. Error and partial-probe paths need the same ownership proof.

### Diagnostics and verification

Use lockdep for dependency and IRQ-state rules, lockstat for contention, ftrace irqsoff or preemptoff-style tracers for long disabled regions where supported, trace events for lifecycle, and stress or fault injection for rare interleavings.

Instrumentation changes timing and may itself be unavailable in the target build. Preserve kernel configuration, tool version, trace clock, loss, filters, CPU masks, workload, and raw output.

### Security and assurance

An attacker may drive interrupt rate, queue length, or error logging to extend critical sections and deny service. Bound work and rate-limit diagnostics. Trace data can expose device and tenant activity.

Safety-relevant interrupt paths need reviewed worst-case service, masking, nesting, lock contention, device failure, overload, and recovery. Runtime evidence complements analysis; it does not certify bounds.

## Definitions and Notation

Let `C={task, hardirq, softirq, threaded_irq, work, nmi, remote}` be abstract contexts. For lock `L`, let `A(L)` be its accessor set, `P(L)` its permitted protocol, `H_L` hold duration, `S_L` spin-wait duration, and `D_irq` local interrupt-disabled duration.

Let interrupt state be `I in {enabled,disabled}` in the toy model. `save_disable()` returns prior `I` and sets disabled; `restore(f)` sets the saved prior state `f`. Actual kernels have architecture- and nesting-specific state beyond this Boolean abstraction.

Required properties include mutual exclusion across CPUs, prevention of local self-reentry, exact state restoration, context-admissible operations, acyclic nesting, ordered publication, bounded exclusion, and quiescent reclamation.

## Mechanisms, Invariants, or Proof Structure

A reviewable interrupt-locking argument follows eight steps:

1. Define the protected invariant and enumerate every accessor context.
2. Mark concurrency and local preemption edges in a context matrix.
3. Choose a lock and local-state protocol covering both remote and local edges.
4. Prove operations inside are admissible and bounded for the strictest caller.
5. Prove saved IRQ, bottom-half, and preemption state restore exactly through every exit.
6. Add handler and task acquisitions to the global lock-class graph.
7. Define publication, device ordering, interrupt synchronization, deferred drain, and reclamation.
8. Validate supported kernel configurations and label measurement coverage.

The executable model demonstrates why nested save/restore differs from unconditional enable.

<!-- bijux-verify: {"id":"toy-nested-irq-restore","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"nested-safe=disabled\nfinal-safe=enabled\nnaive-inner=enabled-too-early\n","stderr":""}} -->
```python
irq_enabled = True

def save_disable():
    global irq_enabled
    previous = irq_enabled
    irq_enabled = False
    return previous

def restore(previous):
    global irq_enabled
    irq_enabled = previous

outer = save_disable()
inner = save_disable()
restore(inner)
print("nested-safe=" + ("enabled" if irq_enabled else "disabled"))
restore(outer)
print("final-safe=" + ("enabled" if irq_enabled else "disabled"))

irq_enabled = True
outer = save_disable()
irq_enabled = True
print("naive-inner=" + ("enabled-too-early" if irq_enabled else "disabled"))
```

This Boolean sequential model has no CPU, interrupt controller, handler, lock, memory ordering, or architecture state. It illustrates nesting logic only.

## Alternatives and Trade-Offs

- Plain spin locking is minimal but unsafe against a local handler sharing the lock.
- IRQ-save locking composes with unknown caller state but masks local interrupts and increases latency.
- Bottom-half control targets deferred context but does not cover hard IRQ or remote CPUs.
- Threaded interrupts permit sleepable design but add scheduling, priority, and split-handler complexity.
- Raw spinlocks preserve strict semantics on PREEMPT_RT but enlarge nonpreemptible blocking.
- Per-CPU ownership removes common sharing but adds aggregation, migration, and hotplug work.
- Deferring work shortens hard handlers but expands queue and teardown lifetime.
- Fine-grained locks reduce hold time but increase order and reclamation complexity.
- Rich tracing finds tails while perturbing precisely timed paths.

## Failure Modes and Misconceptions

1. **“A spinlock disables interrupts.”** Lock and local interrupt control are separate semantics.
2. **“IRQ disable is an SMP lock.”** Remote CPUs continue executing.
3. **“Preemption disabled means IRQ-safe.”** Interrupts may still preempt locally.
4. **“Unlock then enable is always correct.”** The prior state may already have been disabled.
5. **“Nested disable calls are harmless with one enable.”** Unbalanced restoration exposes outer state.
6. **“Hard IRQ and soft IRQ are interchangeable.”** Entry, concurrency, and blocking rules differ.
7. **“Threaded IRQ means no hard handler.”** A primary hard portion may remain.
8. **“Spinlock code may briefly sleep.”** Any sleep can deadlock or violate atomic context.
9. **“Raw spinlock fixes real-time issues.”** It may worsen nonpreemptible latency.
10. **“Per-CPU means race-free.”** interrupts, migration, aggregation, and hotplug remain.
11. **“The lock orders device I/O automatically.”** device accessors and DMA rules are separate.
12. **“IRQ synchronization drains all work.”** timers, threads, and deferred callbacks may remain.
13. **“Lockdep proves safety.”** it covers modeled dependencies along executed paths.
14. **“Worst observed IRQ-off time is a bound.”** coverage and instrumentation limit the claim.

## Worked Examples

### Example 1

Task code takes L plainly; the device interrupt preempts it and spins on L. The task cannot resume to unlock. IRQ-save acquisition on the task side closes this local edge while L excludes remote CPUs.

### Example 2

CPU 0 disables local interrupts and mutates a global list without a lock. CPU 1 concurrently changes it. Local state control did nothing to protect the SMP invariant.

### Example 3

An outer caller already has interrupts disabled. An inner helper unconditionally enables them after its section. A handler now enters inside the outer invariant. Saving and restoring prior state preserves nesting.

### Example 4

A hard handler allocates with a sleeping mode while holding a lock. Under pressure it blocks illegally. Preallocate, use an admissible bounded pool with handled exhaustion, or defer allocation to task context.

### Example 5

Process code uses A then B; a handler uses B then A. Making both IRQ-safe still leaves an inter-CPU AB-BA cycle. Reorder or redesign ownership.

### Example 6

A soft-interrupt poll loop and task configuration share state. Task-side bottom-half-safe locking prevents local deferred reentry; the lock protects remote execution. The hard handler touches only a separate handoff field.

### Example 7

On PREEMPT_RT, code assumes ordinary spin locking disables preemption exactly like a raw lock. Current lock-type semantics contradict the assumption. Select by required behavior and test both supported configurations.

### Example 8

A handler queues work and returns. Device removal synchronizes the IRQ but frees state before queued work runs. Draining or canceling the work before reclamation closes the remaining lifetime.

### Example 9

An attacker fills a ring so a handler scans thousands of entries under lock. Average hold time stays small in normal tests; adversarial queue depth breaks the IRQ-off budget. Bound work per invocation.

### Example 10

Lockdep reports no order error, while irqsoff tracing finds rare console output inside the masked section. Dependency correctness and latency bounds are distinct review dimensions.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains interrupt masks, priorities, atomic instructions, cache coherence, MMIO, and memory barriers. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops mutual exclusion, ordering, and progress.

[Security Engineering](../../25-security-engineering/ROADMAP.md) frames interrupt flooding, denial of service, and trace sensitivity. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies latency budgets, hazards, failure modes, and assurance.

Within this program, [OS-023](../ROADMAP.md) compares sleepable synchronization, [OS-024](../ROADMAP.md) deepens atomics, and [OS-025](../ROADMAP.md) treats memory ordering.

## References

- Linux Kernel documentation, [Lock Types and Their Rules](https://docs.kernel.org/locking/locktypes.html), current page checked 2026-09-04. Spin, raw spin, mutex, local, reader-writer, context, and PREEMPT_RT semantics.
- Linux Kernel documentation, [Lesson 1: Spin Locks](https://docs.kernel.org/locking/spinlocks.html), current page checked 2026-09-04. Spinlock use, IRQ-save forms, reader-writer variants, and compiler considerations.
- Linux Kernel documentation, [Unreliable Guide To Locking](https://docs.kernel.org/kernel-hacking/locking.html), current page checked 2026-09-04. Task, hard-interrupt, soft-interrupt, locking, callbacks, reference counting, and deadlock.
- Linux Kernel documentation, [Generic IRQ Handling](https://docs.kernel.org/core-api/genericirq.html), current page checked 2026-09-04. IRQ descriptors, flow, request, disable, synchronize, affinity, threading, and lifecycle APIs.
- Linux Kernel documentation, [Linux Kernel Memory Barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), current page checked 2026-09-04. Lock ordering, interrupt considerations, CPU barriers, device operations, and minimum guarantees.
- Linux Kernel documentation, [Lockdep Design](https://docs.kernel.org/locking/lockdep-design.html), current page checked 2026-09-04. Lock classes, IRQ state, dependency chains, recursion, annotations, and validation.
- Linux Kernel documentation, [Lock Statistics](https://docs.kernel.org/locking/lockstat.html), current page checked 2026-09-04. Contention, wait and hold times, call sites, configuration, and interpretation.
- Linux Kernel documentation, [Proper Locking Under a Preemptible Kernel](https://docs.kernel.org/locking/preempt-locking.html), current page checked 2026-09-04. Per-CPU data, preemption, migration, rules, and preempt-safe locking.
- Linux Kernel documentation, [Entry/Exit Handling](https://docs.kernel.org/core-api/entry.html), current page checked 2026-09-04. Interrupt, syscall, and exception entry state, RCU, lockdep, tracing, and ordering.
- Linux Kernel documentation, [ftrace](https://docs.kernel.org/trace/ftrace.html), current page checked 2026-09-04. irqsoff, preemptoff, wakeup, function and event tracing, clocks, buffers, and overhead.
- Linux Kernel documentation, [Using the Linux Kernel Tracepoints](https://docs.kernel.org/trace/events.html), current page checked 2026-09-04. Event discovery, enablement, filtering, formats, and trace interface behavior.
- Linux Kernel documentation, [RT-mutex Implementation Design](https://docs.kernel.org/locking/rt-mutex-design.html), current page checked 2026-09-04. Priority inheritance, waiter state, owner transitions, chain walking, and locking.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching spinlocks, interrupt masking, nesting, multicore exclusion, device interrupts, and sleep transitions.

## Exercises

### Exercise 1

Build a context matrix for a network ring accessed from configuration task, hard IRQ, soft-interrupt polling, watchdog timer, debug reader, and removal. Choose protocols and justify every exclusion edge.

### Exercise 2

Trace three nested IRQ-save sections entered from enabled and disabled initial states. Include early error returns and prove exact restoration.

### Exercise 3

Audit a driver for sleeping operations and lock-order cycles across task, hard IRQ, threaded IRQ, work queue, and teardown paths. Propose a durable ownership redesign.

### Exercise 4

Design a latency experiment measuring spin wait, hold time, IRQ-off time, interrupt response, and device completion across normal and PREEMPT_RT kernels.

### Exercise 5

Construct an assurance review for an IRQ-safe critical section in a safety-relevant device path. Cover bounds, overload, teardown, evidence, and human judgment.

## Answers to the Exercises

### Answer 1

List every field and invariant first. Keep the hard handler bounded: acknowledge or mask the source and publish descriptors under an IRQ-safe ring lock. Soft polling uses the matching lock and bounded batch size. Task configuration uses IRQ-save locking for fields shared with the hard handler and a mutex outside for sleepable control operations. Debug either uses compatible protection or reads a separately published snapshot.

The watchdog needs a non-sleeping or deferred path consistent with its timer context. Removal closes admission, masks the device, synchronizes the IRQ, cancels timer, disables polling, drains work, detaches the ring under lock, waits for readers, then frees. Remote CPUs are excluded by locks, not local masking. NMI-like access is excluded or given a separate protocol.

### Answer 2

Starting enabled: outer saves enabled and disables; middle saves disabled; inner saves disabled. Inner restore remains disabled, middle restore remains disabled, and outer restore returns enabled. Starting disabled, every saved state is disabled and the final state remains disabled. The proof is stack-like: each exit restores exactly its own captured predecessor.

Every error edge must pass through matching cleanup in reverse acquisition order. Do not reuse one flags value for multiple unmatched scopes or unconditionally enable. Assertions can track nesting and expected lock ownership, while runtime tools test executed paths.

### Answer 3

Inventory allocation, user copy, waits, device commands, logging, callbacks, and nested acquisitions. Hard IRQ performs only non-sleeping bounded capture. Threaded IRQ and work queue own slow processing under mutexes. Task configuration sends requests through that owner rather than holding spinlocks across device waits. Teardown participates in the same ownership protocol.

Create one lock-class graph including callbacks and error paths, choose a stable order, and eliminate cross-domain nesting through queues or snapshots. Allocate before spin entry, defer callbacks, bound lists, and make failure explicit. Validate IRQ-state assumptions on supported preemption configurations and preserve lifecycle synchronization.

### Answer 4

Instrument acquisition attempt, success, release, local IRQ disable and restore, handler pending and entry where observable, and device completion. Derive spin wait, hold, IRQ-off, pending-to-handler, and end-to-end distributions. Use lockstat, selected trace events, and irqsoff-style tracing separately and together to estimate observer cost.

Cross task and interrupt load, queue depth, CPUs, affinity, nested interrupts, logging, device errors, hotplug, and thermal states on documented normal and PREEMPT_RT builds. Preserve configs, trace clocks, buffer loss, tools, raw events, and workload seeds. Observed maxima are not analytical bounds.

### Answer 5

Define device state invariant, every context, maximum interrupt rate, batch size, hold work, nesting, and lock order. Use documented lock types for the deployed real-time configuration. Bound spin, hold, IRQ-off, preemption-off, handler, threaded work, priority inversion, and device response under admitted load.

Define interrupt storms, stuck device, CPU loss, late callbacks, partial initialization, tracing failure, removal, and safe-state behavior. Combine static order and context review, lockdep, contention and irqsoff traces, stress, fault injection, and independent timing with analytical bounds. Named driver, kernel, concurrency, real-time, platform, security, safety, independent-verification, and acceptance owners review assumptions and residual risk. This chapter claims no certification.
