---
module_id: OS-004
program: Operating Systems
level: 1
module_number: 4
title: Interrupts and Exceptions
status: complete
last_verified: 2026-09-04
---

# Interrupts and Exceptions

## One-Page Review

### Governing question

How can an operating system regain control for processor, timer, and device events while preserving interrupted state, servicing the correct source, and resuming or terminating execution safely?

### Essential definitions

- An **exception** is an architecturally defined event associated with instruction execution that transfers control to a handler; architecture manuals differ in their taxonomies.
- An **interrupt** is commonly an asynchronous event raised independently of the current instruction stream, such as a timer or device completion.
- A **trap** is a control transfer to a handler; on RISC-V it includes interrupts and exceptions, while x86 also uses narrower fault, trap, and abort classes.
- An **interrupt controller** accepts sources, records pending state, applies enable and priority rules, routes a selected event to a processor, and participates in acknowledgement or end-of-interrupt protocols.
- An **interrupt service routine** (ISR) is the immediate software path that identifies and services an interrupt under restricted execution-context rules.
- An **edge-triggered** source signals a transition; a **level-triggered** source remains asserted while its service condition holds.
- A **precise exception** presents an architectural state from which software can identify the responsible instruction and apply the specified resume or termination rule.

### Central model, mechanism, or theorem

Event handling is a state-preserving protocol:

`running -> recognized -> entered -> classified -> contained -> serviced -> completed -> resumed_or_terminated`.

Correctness requires that accepted events are neither lost nor serviced as the wrong source, interrupted state remains protected, cause-specific state changes occur exactly as the contract permits, controller completion happens in the right order, and return resumes only a valid context. The same entry machinery can carry recoverable conditions, deliberate service requests, external completions, fatal faults, and debugging events; their causes and policies must remain distinct.

### Critical invariants

- Every accepted vector or cause selects a configured handler under protected control state.
- Entry preserves enough processor and software context to classify the event and choose a legal continuation.
- Immediate handling performs only work valid in interrupt or exception context; sleepable and lengthy work is deferred where required.
- Edge and level sources follow controller- and device-specific mask, acknowledge, clear, and end-of-interrupt ordering.
- Nested and concurrent handlers cannot corrupt stacks, per-CPU state, shared device state, or return frames.
- A recoverable exception changes state so retry or resume makes progress; an unrecoverable one terminates or escalates explicitly.
- Return restores an authorized context without dropping a pending event or disclosing privileged state.

### Common failures

Frequent errors are treating every exception as an error, treating every interrupt as external, assuming x86 fault/trap terminology is universal, clearing a level source in the wrong order, doing blocking work in a hard-interrupt path, confusing interrupt masking with mutual exclusion, enabling nesting before entry state is safe, retrying without repairing the fault cause, ignoring spurious or shared interrupts, and measuring average handler time while missing tail-latency storms.

### Compact example

A network device asserts a level-triggered interrupt because completions are present. The controller selects a permitted CPU and vector. Entry saves processor state and reaches a protected handler. The handler confirms that this device is the source, masks or otherwise stabilizes delivery as its protocol requires, records enough work, clears the device condition, and acknowledges or signals end-of-interrupt in the documented order. Bulk packet processing is deferred under a budget. Return resumes a valid context; if work remains, the deferred mechanism continues without keeping hard interrupts disabled indefinitely.

### Connections

[OS-002](002-privilege-levels-and-protection-rings.md) defines controlled privileged entry, and [OS-003](003-system-calls-and-user-kernel-transitions.md) develops deliberate synchronous requests. [OS-022](../ROADMAP.md) develops locks in interrupt context, while [OS-058](../ROADMAP.md) develops timer and interrupt scalability. Hardware mechanisms connect to [Computer Architecture](../../23-computer-architecture/ROADMAP.md), and adversarial event handling connects to [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

A processor cannot simply run one application instruction stream until that stream volunteers to stop. A timer must let the scheduler recover control. Devices must report completion and errors. Invalid instructions, translation misses, protection violations, arithmetic conditions, breakpoints, and deliberate service instructions require defined responses. These events can arrive at inconvenient points and some can nest inside others.

The operating system must transform each accepted event into a safe change of control. It preserves the interrupted context, establishes trusted state, identifies the cause, performs or schedules bounded work, coordinates with interrupt-controller and device protocols, then resumes, retries, redirects, terminates, or escalates. A mistake can lose device work, repeat an instruction forever, corrupt a return frame, deadlock the kernel, or allow one source to monopolize a processor.

The core question is therefore how to make asynchronous and synchronous control transfers composable with scheduling, concurrency, memory faults, device state, debugging, and protection rather than how to write one handler function.

## Why This Matters

Interrupts make preemption and efficient device use possible. Without a timer, compute-bound code may retain a processor indefinitely. Without completion notification, software must poll continuously or tolerate long delays. Exceptions make virtual memory, debugging, instruction emulation, lazy resource management, and controlled system calls possible.

These mechanisms also create some of a kernel's most constrained paths. Entry may run with interrupts masked, on a small per-CPU stack, before ordinary runtime assumptions hold, or while interrupted code owns locks. Handler latency affects unrelated work. Device state can change concurrently with software. A flood of events can become a denial of service even when each individual event is valid.

Terminology itself matters. Architecture manuals assign precise meanings to “exception,” “interrupt,” “fault,” “trap,” and “abort.” Operating systems add terms such as IRQ, hard interrupt, soft interrupt, threaded interrupt, and signal. Engineers who import one architecture's taxonomy into another can choose the wrong resume address, clearing sequence, or recovery policy.

## Prerequisites and Retrieval

Recall from [OS-003](003-system-calls-and-user-kernel-transitions.md) that an entry instruction is a deliberate synchronous transition and that entry does not imply authorization. You should understand privilege levels, registers, stacks, instructions, memory mappings, devices, concurrency, and basic scheduling.

Retrieve these distinctions:

- synchronous describes a causal relationship to instruction execution, not a guarantee of successful recovery;
- asynchronous delivery can still be sampled and accepted only at architecture-defined boundaries;
- masking postpones selected delivery but does not necessarily clear a device condition or exclude another processor;
- acknowledgement, source clearing, and end-of-interrupt are distinct protocol actions;
- saving processor state does not automatically save every kernel software invariant;
- a user-space signal is an OS abstraction and is not identical to a hardware interrupt.

## Learning Objectives

After completing this module, you should be able to:

- distinguish synchronous exceptions, asynchronous interrupts, deliberate traps, and operating-system notifications;
- compare x86, Arm, and RISC-V terminology without asserting false equivalence;
- trace event recognition through vectoring, entry, classification, service, completion, and return;
- explain precise state, resume address, retry, skip, redirect, termination, and escalation choices;
- reason about edge-triggered and level-triggered interrupt protocols;
- identify constraints on hard-interrupt context and decide what work to defer;
- analyze masking, priority, nesting, affinity, sharing, and interrupt-controller state;
- diagnose lost interrupts, storms, livelock, reentrancy, stack corruption, and incorrect end-of-interrupt ordering;
- design measurements for interrupt latency, service time, queueing, and tail behavior;
- define evidence and accountable human review for high-consequence event handling.

## Core Exposition

### A taxonomy scoped to an architecture

At a portable conceptual level, an interrupt is asynchronous with respect to the currently executing instruction, while an exception is synchronous and attributable to instruction execution or an architecturally defined condition. Both transfer control through protected entry machinery. This vocabulary is useful, but a real implementation must use its architecture's definitions.

Intel classifies processor-detected exceptions as faults, traps, or aborts partly by the reported instruction boundary and restart implications. A fault generally reports the faulting instruction so a repaired condition can retry; a trap generally reports after the trapping instruction; an abort may not support reliable restart. These words must not be projected mechanically onto Arm or RISC-V.

RISC-V uses **trap** as the umbrella control transfer caused by an exception or interrupt and encodes whether the cause is interrupting. Arm distinguishes synchronous exceptions, IRQ, FIQ, and system error classes and routes them according to exception level and configuration. Comparable obligations exist, but cause encodings, saved state, masks, priorities, and return instructions differ.

### Precise state and continuation

Handling starts with a precise question: what architectural state does the handler observe, and what should happen next? For a recoverable page fault, the saved program counter commonly identifies an instruction to retry after mapping or permission state is repaired. For a breakpoint, the reported position and resume rule follow that breakpoint's architectural semantics. For a device interrupt, the interrupted instruction is usually unrelated to the device event and should eventually resume without modification.

A **precise** exception establishes a documented boundary: instructions before it have the architecture's committed effects, the responsible instruction and later ones have the specified uncommitted or visible state, and saved control state identifies the continuation. Architectures can expose imprecise or asynchronous error reporting for some machine conditions; software cannot invent instruction-level rollback when the architecture does not provide it.

Recovery must make progress. Retrying an instruction without installing the missing mapping, resolving the emulation, or changing policy recreates the same exception. Skipping an instruction without a contract may corrupt program semantics. Fatal kernel exceptions need a containment policy that considers locks, shared state, and whether continuation would compound corruption.

### Recognition, prioritization, and vectoring

Interrupt sources signal an interrupt controller or a processor-local facility. The controller records pending state, applies masks and priority, chooses a target processor, and presents an identifier or vector. Some systems have cascaded controllers or interrupt domains that translate hardware identifiers into kernel IRQ identities.

Pending, enabled, active, and asserted are different states. A masked interrupt can remain pending. A level-triggered device can reassert immediately if its underlying condition remains. An active interrupt may require a controller-specific end-of-interrupt before another instance can be delivered. Priority determines selection among eligible events, not whether lower-priority work can be forgotten.

The vector is untrusted in the sense that kernel code must still ensure it lies in a configured table and corresponds to initialized state. Unexpected, reserved, or spurious vectors need bounded handling and diagnostics. A shared line requires each candidate driver to inspect device state and claim only events it owns.

### Entry and the interrupted context

Hardware saves an architecture-defined subset of state and selects an entry target. Low-level code establishes the remainder: a safe stack, per-CPU context, register save area, address-space assumptions, and bookkeeping for nesting, tracing, or context tracking. The handler must know whether it interrupted user mode, ordinary kernel code, another handler, or a non-maskable path.

The interrupted context determines what is legal. If ordinary kernel code held a lock when interrupted, a handler that tries to acquire the same non-reentrant lock can deadlock. If the handler runs on a bounded interrupt stack, deep call chains or large local objects can overflow it. If entry temporarily disables preemption or selected interrupts, blocking is invalid until a context that permits scheduling is reached.

Enabling nested delivery too early exposes partially saved state. Keeping all events masked too long raises latency and can lose capacity in finite device queues. Entry code therefore establishes the minimum safe invariants before changing mask or priority state according to architecture and kernel policy.

### Edge and level semantics

An edge-triggered input records a transition. If another edge occurs while software is handling the first, the controller must retain sufficient pending information or the event can be coalesced or lost. Software commonly acknowledges the recorded edge early, then loops or rechecks device state so work arriving during handling is observed.

A level-triggered input remains asserted while its condition holds. If software signals end-of-interrupt or unmasks before clearing the device condition, the controller may deliver the interrupt again immediately, producing a storm. A common pattern masks and acknowledges, services or stabilizes the source, clears the device condition, then unmasks; exact ordering belongs to the controller and device specifications.

Neither trigger style says how many units of device work exist. One interrupt may represent many completions, and several events may coalesce into one delivery. Correct drivers drain or budget observable device state rather than assuming a one-interrupt-to-one-operation count.

### Immediate and deferred work

The immediate handler does the work required to make the event safe: identify the source, capture volatile status, prevent uncontrolled retriggering, acknowledge according to protocol, and schedule further processing. It should remain bounded because other interrupts and tasks may be delayed while it runs.

Work that may sleep, take contended sleepable locks, allocate with blocking behavior, parse large inputs, or consume an unbounded queue belongs in a deferred or threaded context. Linux exposes several mechanisms with different scheduling and concurrency rules; their names are implementation details, while the enduring split is urgent stabilization versus schedulable bulk work.

Deferral requires ownership. The immediate path and deferred path must agree who owns descriptors, buffers, status bits, device references, and re-enable actions. Scheduling the same deferred work twice must be safe or prevented. Teardown must stop new delivery, synchronize with in-flight handlers, drain or cancel work, and only then free resources.

### Masking, nesting, and multiprocessor concurrency

Local interrupt masking affects delivery on one processor and usually only selected priority classes. It does not stop another processor from accessing shared state. It is therefore not a replacement for a multiprocessor lock. Conversely, taking a lock does not prevent an interrupt on the same processor from deadlocking on that lock unless the locking protocol also manages local delivery.

Nesting improves response to higher-priority events but increases stack use, reentrancy, ordering complexity, and worst-case interference. Priority inversion can occur when a high-priority handler depends on work delayed by a lower-priority context. Non-maskable interrupts are reserved for exceptional uses but still require carefully limited assumptions; “non-maskable” does not mean immune to every architecture control or safe to run arbitrary code.

Affinity routes sources among processors. Concentrating interrupts can preserve cache locality but overload one CPU. Spreading them can improve throughput while increasing shared-state contention and cache movement. Managed affinity, CPU hotplug, per-CPU queues, and device queue topology must agree.

### Completion, return, and downstream effects

Completion means both software and controller state are coherent. The handler has recorded or finished the device work, applied the required acknowledge or end-of-interrupt action, and left the source masked or enabled according to ownership. For exceptions, completion means the saved context has a defined retry, resume, redirect, termination, or escalation disposition.

Return code restores only valid architectural state. It must account for whether entry came from user or kernel mode, whether a signal or scheduler action should intervene, whether tracing changed the context, and whether nested work remains. The originally interrupted task may not resume immediately; the scheduler can choose another runnable task.

An exception originating in user execution may become an OS signal, language runtime exception, debugger stop, process termination, or transparent recovery. Those are downstream policies. A hardware exception is not itself a Unix signal, and the mapping can depend on cause, address, credentials, process state, and kernel configuration.

### Latency, throughput, and overload

Decompose event response as

`T_response = T_detection + T_pending + T_masked + T_priority + T_entry + T_immediate + T_deferred + T_queue`.

Not every measurement includes every term. Device timestamps may observe generation to completion, tracing may observe entry to handler exit, and synthetic injection may omit the physical device. Report the clock, endpoints, CPU affinity, rate, concurrency, power state, kernel configuration, and percentiles.

An interrupt storm can consume nearly all CPU time while useful throughput collapses. Budgeted polling hybrids address this by disabling or moderating repeated interrupts, processing a bounded batch, then reenabling notification when the queue drains. Moderation trades per-event latency for amortized throughput. Overload policy must protect progress for other sources and expose drops, throttling, and saturation.

## Definitions and Notation

Let event `e` have cause `cause(e)`, origin `origin(e)`, priority `prio(e)`, and trigger mode `mode(e) ∈ {edge, level, synchronous}`. Let `P`, `M`, and `A` be controller sets of pending, masked, and active interrupt identities. Let `V` map accepted causes to protected entry vectors.

An interrupt `i` is eligible when

`i ∈ P ∧ i ∉ M ∧ prio(i) exceeds the active acceptance threshold`.

For a synchronous exception, eligibility instead follows the architecture's instruction semantics and delegation rules. A handler entry is valid only if `cause(e) ∈ domain(V)` and the selected target and saved-state area are protected.

For a level source `i`, safe quiescence requires `device_condition(i) = false` before or consistently with unmasking under the specified controller protocol. For an edge source, correctness requires that the pending representation and handler loop account for edges arriving during service to the capacity promised by hardware.

Let `C_before` be the interrupted context and `C_after` the candidate continuation. Return requires `valid(C_after)` and a cause-specific relation `recover(cause, C_before, C_after)`. That relation may encode retry after repair, resume after the trapping instruction, redirection to a user handler, process termination, or no return. This notation is a review model, not a complete semantics for any cited architecture.

## Mechanisms, Invariants, or Proof Structure

Review event handling through seven obligations.

**Source integrity.** Hardware identifiers map to initialized kernel objects. Shared handlers confirm ownership, and unexpected or spurious sources cannot index arbitrary memory or loop without bound.

**Entry integrity.** Protected vectors, stacks, saved state, per-CPU identity, privilege, and nesting metadata reach a defined state before general handler code or nested delivery.

**Context integrity.** The handler uses only operations permitted in its context. It does not sleep while scheduling is forbidden, reacquire an interrupted non-reentrant lock, overflow the interrupt stack, or call code with hidden blocking behavior.

**Protocol integrity.** Edge or level semantics determine mask, acknowledge, source-clear, and end-of-interrupt ordering. Device and controller state cannot disagree indefinitely.

**Concurrency integrity.** Local masking, locks, atomics, affinity, and deferred work cover their actual CPUs and objects. Nested, shared, hot-unplug, and teardown paths preserve ownership.

**Progress integrity.** Recoverable exceptions repair or redirect before retry. Interrupt work is bounded, lower-priority sources eventually run, and storm handling preserves useful system progress.

**Return integrity.** The continuation follows cause-specific semantics, contains fatal state when necessary, and restores only authorized registers, privilege, address-space state, and event masks.

The executable model below checks a small priority-and-mask policy. It does not model real controller registers, instruction precision, concurrency, or device clearing.

<!-- bijux-verify: {"id":"toy-event-router","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"selected=timer\nafter-mask=device\nexception=page_fault:retry-after-repair\nedge-count=2\nlevel-cleared=yes\n","stderr":""}} -->
```python
pending = {"device": 2, "timer": 5}
masked = set()


def select_event():
    eligible = [(priority, name) for name, priority in pending.items()
                if name not in masked]
    return max(eligible)[1] if eligible else None


print(f"selected={select_event()}")
masked.add("timer")
print(f"after-mask={select_event()}")
print("exception=page_fault:retry-after-repair")
edges = ["rx", "rx"]
print(f"edge-count={len(edges)}")
level_asserted = True
level_asserted = False  # The toy device condition is serviced before unmask.
print("level-cleared=" + ("yes" if not level_asserted else "no"))
```

Passing proves only the five printed results of an in-memory Python model. It cannot establish a hardware priority rule, prevent lost edges, prove acknowledgement ordering, bound real latency, or validate an operating-system handler.

## Alternatives and Trade-Offs

**Interrupts versus polling.** Interrupts avoid continuous checking at low rates but add entry and scheduling overhead. Polling can provide predictable batch throughput at high rates but consumes CPU when idle. Adaptive schemes switch under measured load and need stable transition rules.

**Immediate versus deferred handling.** More immediate work can clear hardware quickly and reduce handoff overhead, but lengthens constrained context. Earlier deferral improves responsiveness but adds queueing, synchronization, and ownership transitions.

**Edge versus level signaling.** Edges avoid continuous assertion but require sufficient pending capacity and careful race handling. Levels naturally represent an outstanding condition but retrigger until that condition is cleared. Hardware topology often determines the choice.

**Masking versus fine-grained synchronization.** Broad masking simplifies some uniprocessor reasoning while raising latency and failing to exclude other CPUs. Fine-grained locks and atomics improve concurrency but require interrupt-aware ordering and deadlock analysis.

**Fixed versus dynamic affinity.** Fixed routing supports locality and predictability. Dynamic balancing adapts to load but can move cache state, disturb real-time budgets, and conflict with device queue ownership.

**Dedicated versus shared vectors.** Dedicated message-signaled interrupts can isolate queues and scale across CPUs. Shared lines conserve scarce vectors and support legacy hardware but require source probing and tolerate unrelated handler invocation.

**Coalescing versus immediate notification.** Coalescing lowers interrupt rate and amortizes work. It adds queueing latency and can hide bursts. Workload-specific rate, latency, and loss objectives must drive moderation.

## Failure Modes and Misconceptions

1. **“Every exception is a failure.”** Page faults, breakpoints, emulation, and service instructions can be expected control paths.
2. **“Every interrupt comes from a device.”** Timers, interprocessor interrupts, performance facilities, and other processor-local sources also interrupt.
3. **“Fault, trap, and abort mean the same thing everywhere.”** Their formal use is architecture-specific.
4. **“Masking clears the interrupt.”** It commonly blocks delivery while pending or asserted state remains.
5. **“Acknowledgement clears the device.”** Controller acceptance and device-condition clearing are separate operations.
6. **“One interrupt means one completion.”** Sources coalesce, queues batch, and shared lines represent multiple devices.
7. **“Interrupt masking is a multiprocessor lock.”** Other processors continue to access shared data.
8. **“A hard-interrupt handler may sleep briefly.”** Sleeping can violate scheduling context and deadlock ownership.
9. **“A wake or vector identifies the source conclusively.”** Shared and spurious interrupts require bounded validation.
10. **“Retrying a fault always progresses.”** The cause must be repaired or the same exception recurs.
11. **“Non-maskable means unconstrained.”** NMI-like contexts have stricter reentrancy, stack, locking, and observability limits.
12. **“Average handler time characterizes responsiveness.”** Masked intervals, queues, storms, and high percentiles determine worst cases.
13. **“Deferred work removes overload.”** It moves work; budgets, backpressure, and drop policy remain necessary.
14. **“A user signal is a hardware interrupt.”** It is a process-level OS delivery abstraction that may arise from several causes.

## Worked Examples

### Example 1

**Question:** A page fault occurs on a valid lazily allocated page. Why can execution retry?

**Reasoning:** The architecture reports a precise saved context. The kernel validates the access, allocates or locates a page, updates protected translation state, and arranges required invalidation. The original instruction then sees a changed mapping.

**Conclusion:** Retry is correct only because the handler repairs the cause and the architecture defines the restart state.

### Example 2

**Question:** A level-triggered device interrupts again immediately after return. What should be inspected?

**Reasoning:** The device condition may still be asserted, or software may unmask or issue end-of-interrupt before clearing it. The exact register and ordering requirements come from both controller and device specifications.

**Conclusion:** Diagnose the complete mask, acknowledge, device-clear, end-of-interrupt, and unmask protocol.

### Example 3

**Question:** Two packet completions arrive but the controller delivers one interrupt. Is one completion necessarily lost?

**Reasoning:** Interrupts signal that work may exist; they need not count work items. A handler that drains the completion ring observes both. A handler that assumes exactly one item can strand the second.

**Conclusion:** Service authoritative device queue state, not an imagined one-interrupt-to-one-item mapping.

### Example 4

**Question:** Why can a handler deadlock while acquiring a lock that ordinary kernel code uses safely?

**Reasoning:** The interrupt may have preempted the same CPU while the interrupted code held that non-reentrant lock. The owner cannot resume until the handler returns, and the handler waits for the owner.

**Conclusion:** Shared locking protocols must account for local interrupt context as well as other CPUs.

### Example 5

**Question:** A shared interrupt invokes a driver whose device has no pending status. Should it report an error?

**Reasoning:** Another device may own the shared assertion, or the event may be spurious. The driver checks bounded status and reports “not mine” according to the kernel API without modifying unrelated device state.

**Conclusion:** Vector delivery narrows candidates but does not always prove source ownership.

### Example 6

**Question:** A timer interrupt arrives while hard interrupts are locally masked. What happens?

**Reasoning:** Subject to architecture and controller behavior, it may become pending and be delivered when eligible. The masked interval contributes to latency. Finite or coalescing state may prevent counting repeated timer events individually.

**Conclusion:** Mask duration and pending semantics belong in responsiveness analysis.

### Example 7

**Question:** Why defer network packet processing after acknowledging an interrupt?

**Reasoning:** Capturing source state and preventing uncontrolled retriggering is urgent. Parsing an unbounded receive queue would monopolize constrained context. Budgeted deferred work permits other events and tasks to progress.

**Conclusion:** Deferral separates hardware stabilization from schedulable bulk processing but needs ownership and backpressure.

### Example 8

**Question:** A fatal exception occurs in kernel code while shared state may be half-updated. May the kernel simply skip the instruction?

**Reasoning:** The architecture may not define a meaningful skip, and software invariants may already be broken. Continuing can spread corruption. Containment, diagnostic capture, subsystem recovery, or fail-stop behavior depends on proven recovery boundaries.

**Conclusion:** Fatal-event policy must prefer known containment over invented continuation.

### Example 9

**Question:** Moving all storage interrupts to one CPU improves cache locality but raises tail latency. Why?

**Reasoning:** Queue ownership and data stay warm, but bursts serialize behind one processor's masked intervals and handler budget. Other CPUs cannot absorb the event load.

**Conclusion:** Affinity trades locality against parallel service capacity and must be measured at load and high percentiles.

### Example 10

**Question:** A railway controller's emergency input uses a highest-priority interrupt. Does priority prove timely safe action?

**Reasoning:** Delivery also depends on masking, controller configuration, electrical behavior, entry time, higher or non-maskable activity, handler bounds, lock dependencies, actuator latency, and fault containment. Priority is one configured mechanism.

**Conclusion:** A named safety authority must review end-to-end deadlines, independence, fault injection, physical safeguards, and residual risk; this module claims no certification.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns exception precision, saved registers, vector selection, controller protocols, cache effects, and interrupt instructions. This module owns how an operating system composes them with handlers, scheduling, drivers, and process-visible outcomes.

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops reentrancy, atomics, locks, and memory ordering. [Security Engineering](../../25-security-engineering/ROADMAP.md) develops malicious event floods, confused devices, unsafe recovery, and control-flow integrity. [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) consumes signals and error outcomes exposed to applications.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) adds event-response requirements, hazard analysis, independent assurance, and lifecycle evidence. Later modules connect these mechanisms to [OS-022](../ROADMAP.md) interrupt-context locking, [OS-035](../ROADMAP.md) page faults, [OS-058](../ROADMAP.md) multiprocessor scalability, and [OS-061](../ROADMAP.md) device drivers.

## References

- Intel Corporation, [*Intel® 64 and IA-32 Architectures Software Developer's Manuals*](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), current index checked 2026-09-04. Primary x86 source for interrupts, exceptions, fault/trap/abort classes, vectors, saved state, and return.
- Arm Limited, [*AArch64 Exception Model*](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/Exception%20model.pdf), 2019. Official overview of synchronous, IRQ, FIQ, and system-error classes, exception levels, vectoring, and return.
- RISC-V International, [*RISC-V Ratified Specifications Library*](https://docs.riscv.org/reference/home/index.html), current library checked 2026-09-04. Primary index for exception and interrupt traps, cause registers, delegation, status, and trap return.
- RISC-V International, [*RISC-V Advanced Interrupt Architecture*](https://docs.riscv.org/reference/aia/index.html), version 1.0, revised 2025. Primary ratified interrupt-controller and message-signaled-interrupt architecture source.
- Linux Kernel documentation, [Entry/exit handling for exceptions, interrupts, system calls and KVM](https://docs.kernel.org/core-api/entry.html), current page checked 2026-09-04. Documents context tracking, interrupt-state transitions, and constrained entry ordering.
- Linux Kernel documentation, [Linux generic IRQ handling](https://docs.kernel.org/core-api/genericirq.html), current page checked 2026-09-04. Documents flow handlers, interrupt-chip operations, edge and level handling, affinity, and synchronization.
- Linux Kernel documentation, [The irq_domain Interrupt Number Mapping Library](https://docs.kernel.org/core-api/irq/irq-domain.html), current page checked 2026-09-04. Documents mappings between hardware interrupt identifiers and Linux IRQ descriptors.
- Linux Kernel documentation, [Kernel-level exception handling on x86](https://docs.kernel.org/arch/x86/exception-tables.html), current page checked 2026-09-04. Describes fixup tables for selected kernel faults rather than universal recovery.
- Linux Kernel documentation, [NMI Trace Events](https://docs.kernel.org/trace/events-nmi.html), current page checked 2026-09-04. Documents Linux tracing of NMI entry and exit with architecture-dependent availability.
- Linux man-pages project, [`signal(7)`](https://man7.org/linux/man-pages/man7/signal.7.html), current page checked 2026-09-04. Documents process-visible Linux signal generation, delivery, interruption, and execution context.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching implementation of RISC-V traps, timer and device interrupts, system calls, and page-fault-related control flow.

## Exercises

### Exercise 1

Classify an external device completion, timer tick, invalid instruction, page fault, breakpoint, system-call instruction, and interprocessor interrupt by causality and likely continuation. State which labels require an architecture-specific definition.

### Exercise 2

Write the event-state trace for a level-triggered storage interrupt from device assertion through controller state, entry, immediate handling, deferred completion work, end-of-interrupt, unmask, and return. Explain how the wrong clearing order creates a storm.

### Exercise 3

A hard-interrupt handler shares a queue with process context on four CPUs. Design the synchronization and ownership protocol. Cover local interruption, other CPUs, memory ordering, sleep restrictions, teardown, and CPU hot-unplug.

### Exercise 4

Design an experiment that compares interrupt-per-completion, fixed coalescing, adaptive moderation, and polling for a network queue. Define workload, endpoints, clocks, latency percentiles, throughput, CPU cost, drops, fairness, and overload behavior.

### Exercise 5

A medical infusion controller relies on a periodic timer and an alarm interrupt. Construct an assurance plan covering priority, maximum masking, nesting, handler bounds, clock and controller faults, overload, watchdogs, physical safety mechanisms, and accountable human review.

## Answers to the Exercises

### Answer 1

A device completion, timer tick, and interprocessor interrupt are commonly asynchronous interrupts relative to the current instruction stream. Invalid instruction and page fault are synchronous exceptions caused while executing an instruction. A breakpoint and system-call instruction are deliberate synchronous events, though exact labels and saved program-counter semantics depend on the architecture and instruction.

Continuation differs. A device or timer handler normally resumes the unrelated interrupted context after recording work. A valid page fault can repair translation and retry. An invalid instruction may be emulated, delivered to a runtime or process, or terminate execution. A breakpoint commonly redirects to debugger policy. A system-call instruction dispatches a requested service and resumes according to its ABI. Terms such as fault, trap, abort, IRQ, and FIQ must be interpreted from the named architecture rather than assigned universally.

### Answer 2

The device makes its completion condition true and asserts its level. The controller records it pending; if enabled and above threshold, it selects a CPU and marks or presents the source. Entry preserves architectural state and establishes a kernel interrupt context. The immediate handler validates the source, masks or stabilizes it according to the controller flow, captures volatile status, and transfers ownership of completion records to bounded deferred work.

Software services or drains the device condition, records completions, and clears the cause at the device. It then performs the controller's required acknowledge or end-of-interrupt and unmasks in the specified order. Deferred work continues under a budget and rechecks for arrivals during the handoff. Return restores valid state or schedules another task. If software unmasks or completes controller handling while the level remains asserted, the source immediately becomes eligible again; repeated entries without clearing useful work form a storm.

### Answer 3

Define one owner for each queue slot and indexes with acquire/release publication. A spinlock or lock-free protocol must cover all four CPUs; local interrupt masking alone is insufficient. If process context uses the same non-reentrant lock, its interrupt-aware acquisition disables the relevant local handler before taking the lock so that it cannot be interrupted while owning it. The hard handler never sleeps and performs only bounded allocation or uses preallocated storage.

Teardown first prevents new device delivery, removes publication paths, and synchronizes with handlers on every CPU. It drains or cancels deferred work before freeing the queue and device state. Hot-unplug reroutes or disables affinity only after the target CPU stops accepting the source and migrates per-CPU ownership under the controller contract. Tests include interruption at every publication boundary, simultaneous producers, full and empty wrap, nested unrelated interrupts, teardown during handling, and CPU removal under load.

### Answer 4

Use identical hardware, queue depth, CPU placement, packet sizes, directions, offered-load steps, and duration. Include sparse interactive traffic, steady throughput, and bursts beyond service capacity. Timestamp device generation or earliest observable arrival, interrupt entry, immediate exit, deferred start, and application-visible completion with synchronized clocks or carefully stated clock domains.

For each mode report median and high-percentile end-to-end latency, throughput, interrupt rate, batches per interrupt, CPU cycles or utilization, queue depth, drops, useful work per wake, and interference with an unrelated latency-sensitive task. Repeat across affinities, power states, and contention. Sweep fixed thresholds; define the adaptive controller's feedback and stability; let polling include idle CPU cost. Under overload, measure recovery time, fairness, throttling, and whether queues remain bounded. Do not infer device-to-application latency from handler duration alone.

### Answer 5

Specify dosage and alarm hazards, timer period and jitter limits, response deadlines, safe state, clock assumptions, and independence requirements. Inspect exact processor and controller priority, mask, routing, nesting, and saved-state configuration. Measure the longest masked interval and handler response at maximum credible load, including nested higher-priority events, device storms, memory pressure, startup, shutdown, update, and fault recovery. Bound handler loops, stack use, lock dependencies, and deferred work.

Inject missing, repeated, delayed, misrouted, and spurious timer and alarm events; stuck levels; controller faults; clock drift and stoppage; CPU overload; handler overrun; and corrupted device status. Verify watchdogs, redundant time bases where required, dosage limits, mechanical or electrical interlocks, independent alarms, and transition to safe state. Operational evidence covers configuration control, boot integrity, monitoring, maintenance, and incident response. A named safety engineer, clinical domain authority, security reviewer, and acceptance owner must assess traceability, test coverage, independence, common-cause failures, unresolved findings, and residual risk. This chapter and its toy model claim no external validation or medical certification.
