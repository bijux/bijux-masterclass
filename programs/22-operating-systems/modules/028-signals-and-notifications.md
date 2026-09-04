---
module_id: OS-028
program: Operating Systems
level: 1
module_number: 28
title: Signals and Notifications
status: complete
last_verified: 2026-09-04
---

# Signals and Notifications

## One-Page Review

### Governing question

How can a process use asynchronous notifications without confusing event occurrence, pending state, delivery, handler execution, interruption, payload, or durable work ownership?

### Essential definitions

- A **signal** is a numbered asynchronous notification generated for a process or a particular thread.
- **generation** is the event that makes a signal pending or immediately deliverable.
- **pending** means generated but not yet delivered or synchronously accepted.
- A **signal mask** is the per-thread set of signals currently blocked from ordinary delivery.
- A **disposition** is the process-wide default, ignore, or handler action for a signal.
- An **async-signal-safe operation** has the platform-defined safety needed when invoked by an asynchronous handler; ordinary thread safety is not enough.
- A **standard signal** generally represents coalesced state, while real-time signals support queued instances and ordered delivery under specified rules.

### Central model, mechanism, or theorem

For signal `s`, model disposition `D(s)`, each thread mask `M_t`, process-pending state `P_p`, thread-pending state `P_t`, and any queued real-time records `Q(s)`. Generation selects process or thread scope. Delivery selects an eligible thread, removes one pending occurrence according to signal class, applies the disposition, and may interrupt normal execution.

Signals are bounded notifications, not reliable general-purpose message logs. Correct designs block managed signals before creating threads, accept them synchronously in one owner or perform only minimal async-safe handler work, translate them into ordinary program events, and recheck the authoritative predicate.

### Critical invariants

- Signal ownership states which thread accepts which set and which signals retain default behavior.
- Mask changes close check-then-sleep and initialization races by using atomic wait interfaces or pre-thread blocking.
- Handlers touch only permitted state and operations, preserve required context such as `errno`, and never acquire unsafe locks.
- Standard-signal multiplicity is not used as a work count; authoritative state or a queued channel owns work.
- Every interrupted operation handles success, partial progress, `EINTR`, restart, cancellation, and deadline correctly.
- Process and thread targets are identity-safe against PID or thread-lifetime reuse where the platform provides stronger handles.
- Shutdown, fork, exec, child reaping, overflow, and lost peer behavior have explicit policy.

### Common failures

Common mistakes are doing allocation or logging in a handler, assuming thread-safe means signal-safe, using a boolean flag as a count, unblocking a managed signal in multiple threads, calling `pause` after a racy predicate check, blindly retrying a partially completed operation, treating `SA_RESTART` as universal, confusing delivery with durable acknowledgment, losing child-state transitions through incomplete reaping, sending to a reused PID, and queuing real-time signals without overload policy.

### Compact example

A service blocks `SIGTERM`, `SIGINT`, and `SIGHUP` in the initial thread before creating workers. A dedicated control thread uses `sigwaitinfo` to accept them. It converts termination into an idempotent shutdown request, reload into a versioned configuration transaction, and each wake into ordinary synchronized state. Workers never run asynchronous handlers for that set, and repeated notifications merely prompt reevaluation of authoritative state.

### Connections

[OS-015](015-process-states-and-wait-queues.md) explains sleeping and wakeups; [OS-026](026-pipes-and-byte-streams.md) provides byte-stream transport; [OS-027](027-shared-memory.md) provides shared state that a signal can announce but not replace.

## Governing Question

Signals cross ordinary control flow. Delivery can occur while a thread holds a library lock, has partially updated an invariant, or is between checking a predicate and sleeping. A handler therefore executes under constraints unlike a normal callback.

The governing question is how to make notifications prompt safe state transitions without pretending that a small, coalescing, resource-limited mechanism is a durable queue. The solution separates notification from work, assigns signal ownership, and handles every race at masking, waiting, interruption, and lifecycle boundaries.

## Why This Matters

Signals express termination, terminal input, timers, child changes, faults, resource limits, and application control. Supervisors and shells depend on them. They can wake an event loop or control thread without a permanent polling cost.

Misuse creates rare deadlocks and corruption. A handler interrupts allocation and allocates again. A flag loses repeated work. A parent notices one child exit but leaves other zombies. A service reloads configuration directly in the handler. A PID is recycled before a delayed sender acts.

Reliable systems use signals as a narrow control plane: observe, record minimally, and hand off. Rich data, authorization, retries, and durability live in a stronger channel.

## Prerequisites and Retrieval

Recall process and thread identity, `fork` and `exec` from [OS-012](012-process-creation-and-program-loading.md), wait predicates from [OS-015](015-process-states-and-wait-queues.md), critical sections from [OS-021](021-critical-sections-in-the-kernel.md), and IPC lifecycle from [OS-026](026-pipes-and-byte-streams.md).

Retrieve these distinctions:

- generation, pending, delivery, handler entry, and application action are different moments;
- disposition is process-wide while the blocking mask is per thread;
- process-directed and thread-directed signals use different targeting rules;
- standard signals coalesce while real-time signals can queue within limits;
- async-signal safety is stricter than reentrancy or ordinary thread safety;
- a restarted system call may still require deadline and partial-progress reasoning;
- notification indicates that state may have changed; it does not transfer the state itself.

## Learning Objectives

After this module, you should be able to:

1. model disposition, masks, pending sets, targeting, and delivery;
2. distinguish standard and real-time queueing and ordering guarantees;
3. design minimal asynchronous handlers and synchronous acceptance loops;
4. close mask-and-wait races and manage signals in multithreaded processes;
5. handle interruption, partial progress, restart, timers, and child reaping;
6. evaluate signalfd-style event-loop integration, identity-safe sending, and overflow;
7. construct tests and assurance claims with explicit platform, timing, and failure scope.

## Core Exposition

### Generation, pending, and delivery

A signal is generated when its triggering event occurs or a sender requests it. It can be generated for the process or a specific thread. If blocked, it normally remains pending. Delivery occurs when the system selects an eligible thread and applies the current disposition.

The gap matters. A process can change masks or disposition while a signal is pending. Application logic must not treat the send call, pending bit, handler entry, or completed work as equivalent acknowledgment stages.

### Dispositions

Each signal has a process-wide disposition: default action, ignore, or a caught handler. Default actions include terminate, terminate with core, stop, continue, or ignore. `SIGKILL` and `SIGSTOP` cannot be caught, blocked, or ignored.

Use `sigaction` rather than weaker legacy installation interfaces. Its mask and flags make handler-time blocking, extended information, alternate stacks, and restart policy explicit. `fork` copies dispositions; `exec` resets caught dispositions while ignored dispositions have different inheritance behavior.

### Per-thread masks

Every thread has its own blocking mask, inherited at thread creation. In a multithreaded program, block the managed set in the initial thread before creating any workers. All workers inherit it, and one designated thread can synchronously accept the signals.

If a process-directed signal is unblocked in several threads, the system may choose an eligible one. Designs that assume a particular worker receives it are unsound without thread-directed generation or controlled masks.

### Pending state and standard signals

Standard signals do not form an occurrence queue in the usual case. Repeated generation while the same signal is already pending can collapse into one pending indication, and ordering among different pending standard signals is not a portable work-order guarantee.

Use a signal as “state may need attention.” Drain the authoritative child table, pipe, queue, counter, or device until its predicate is false. Do not use one handler invocation as proof of one external event.

### Real-time signals

POSIX real-time signals support queued instances with values and specified ordering rules. They offer more information than standard signals, but queue capacity remains finite and send can fail. Priority ordering can also starve higher-numbered signals under sustained lower-numbered traffic.

Define queue limits, sender authentication, overflow, retry, deadline, and receiver failure. If loss is unacceptable, own the data in durable or flow-controlled storage and use the signal only as a wakeup.

### Asynchronous handler context

A handler can interrupt code while it owns internal locks or maintains temporary invariants. Calling a non-async-signal-safe routine can deadlock or produce undefined behavior. Common conveniences such as allocation, formatted I/O, and most application logging are unsuitable.

Keep handlers tiny: save and restore `errno` when required, update only permitted lock-free or `volatile sig_atomic_t` state under the language contract, or perform a carefully bounded async-safe write to a pre-created channel. Avoid locks, heap ownership, complex control flow, and arbitrary callbacks.

### The self-pipe pattern

A handler can write a small token to a nonblocking pipe whose read end belongs to the normal event loop. The byte wakes `poll` or a related interface; normal code then reads the pipe and examines authoritative state.

The pipe can fill, so the handler cannot block. A failed wake write is acceptable only if an existing unread token or another mechanism guarantees a later state check. The token is edge notification, not durable work identity.

### Synchronous acceptance

`sigwait`, `sigwaitinfo`, or a timed variant accepts a blocked signal in ordinary thread context. This permits allocation, locks, logging, and state machines according to normal threading rules. The signal must remain blocked in threads that should not receive it asynchronously.

Synchronous acceptance simplifies reasoning but does not enlarge signal queue semantics. The control thread still reaps all children, coalesces idempotent reloads, validates sender data, and handles shutdown ordering.

### Atomic wait transitions

The classic race is: check a flag, observe false, receive a signal that sets it, then call `pause` and sleep forever. Atomically replacing the mask while waiting through `sigsuspend`, `pselect`, or an appropriate platform interface closes the check-then-sleep window.

The surrounding code blocks the signal, examines the predicate, and invokes the atomic wait with a mask that permits delivery. On return it loops and checks again. Wakeup itself is never the predicate.

### Linux descriptor integration

Linux `signalfd` turns acceptance of a blocked set into records readable through a descriptor, allowing `poll`, `select`, or `epoll` integration. Reads consume pending signals represented by returned records. Managed signals must remain blocked so their default action or handler does not race the descriptor path.

This is Linux-specific and carries descriptor lifecycle, nonblocking-read, readiness, fork, exec, and event-loop generation concerns. It does not receive `SIGKILL` or `SIGSTOP`, and it does not transform signals into an unbounded queue.

### Interrupted operations

Signal delivery can interrupt a blocking interface. Outcomes depend on the interface, transferred progress, handler flags, and platform. Some calls restart with `SA_RESTART`; others return `EINTR`; some report a positive partial count.

Retry only after examining the result. Preserve accepted or received prefixes, recompute remaining deadline against a monotonic clock, honor cancellation, and prevent duplicate side effects. `EINTR` is control flow, not permission to discard progress.

### Timers and deadlines

Interval timers and POSIX timers can generate signals, but standard timer signals may coalesce. Count expirations through an interface that reports overruns or by comparing authoritative monotonic time, not by counting handler calls.

Absolute deadlines avoid extending a timeout after repeated interruptions. Wall-clock changes should not silently alter an elapsed-time safety bound; choose the clock explicitly.

### Child-state notification

`SIGCHLD` tells a parent that child state may have changed. Several changes can coalesce. The handler or control path therefore calls a nonblocking wait operation in a loop until no more relevant children are ready, retaining status for each.

Disposition and flags affect stop and exit notification behavior. Correct supervisors handle fork failure, early child exit before bookkeeping, PID reuse, orphan policy, reaping, restart limits, and shutdown races.

### Fault signals

Synchronous fault signals such as invalid memory access arise from a particular thread's execution. Returning from a handler without correcting a recoverable, platform-defined condition can repeat the fault or enter undefined behavior.

Crash handlers should avoid ambitious recovery and unsafe diagnostics. An alternate signal stack can improve the chance of handling stack exhaustion, but it also needs correct allocation, guards, per-thread setup, and bounded handler behavior. Preserve reliable external crash evidence where possible.

### Process and thread targeting

`kill` can target a process, process group, or special PID domain under permission checks. `pthread_kill` targets a thread in a process according to its interface. Linux has lower-level thread identifiers and stronger process handles such as pidfds for some operations.

Numeric identities can be reused after lifecycle end. A sender must bind authority and identity to a live object or validate generation, especially when signals trigger privileged control actions.

### Terminal and job-control signals

Terminals and shells use process groups and sessions to direct interactive, stop, continue, and hangup behavior. A service launched under a supervisor should understand which signals the supervisor sends, grace intervals, process-group scope, and escalation.

Do not appropriate job-control signals as arbitrary application messages without considering default actions and inherited shell behavior.

### Fork and exec

A child inherits masks and copies dispositions at `fork`; pending-set rules and `exec` transformations differ. In a multithreaded child after fork, only async-signal-safe operations are generally safe until exec, because locks held by vanished threads may remain locked.

Launch paths set desired masks and dispositions deliberately and use atomic close-on-exec for wake descriptors. Accidental ignored dispositions or blocked signals can survive into a new image and surprise it.

### Shutdown and idempotency

Termination is a request for a state transition, not authorization for immediate complex cleanup in a handler. Normal code atomically moves `RUNNING -> DRAINING -> STOPPED`, stops admission, cancels or drains bounded work, closes dependencies in order, and meets a deadline.

Repeated termination should be idempotent or intentionally escalate. Reload should build and validate new state before publication, preserving the old valid configuration on failure.

### Observability

Record signal number, acceptance path, sender metadata when trustworthy, pending delay, coalescing-sensitive state, wake-channel overflow, interrupted calls, retries, child statuses, shutdown stage, and deadline. Avoid unsafe handler logging.

Metrics gathered only after normal-context handoff are easier to trust. Testing must account for probes changing timing and signal ordering.

### Security and assurance

Signal permission is coarse control authority, not an authenticated rich request. Validate any queued value and consult a stronger channel for parameters. Bound sender rates, real-time queue use, wake tokens, and control operations.

Safety arguments state which signals remain fatal, which are managed, maximum reaction time, behavior during overload, and what happens if the receiver is wedged. External supervisors and hardware watchdogs may be needed because a signal cannot make deadlocked application code execute safely.

## Definitions and Notation

For signal `s`, let `D(s)` be its process disposition. Thread `t` has blocked mask `M_t` and thread-pending set `P_t`; the process has process-pending set `P_p`. Real-time queue `Q(s)` contains bounded ordered instances where supported. A process-directed signal is deliverable to an eligible thread `t` when `s` is pending and `s` is not in `M_t`.

Let authoritative application state be `A` and notification state be `N`. Delivery changes `N` or wakes a checker; the normal control path reads and transitions `A`. Correctness must not require a one-to-one mapping between standard-signal generations and transitions of `A`.

A syscall result has transferred progress `k`, remaining work `r`, and deadline `T`. Retry advances by `k` and recomputes remaining time from `T`; it never repeats committed side effects merely because a signal occurred.

## Mechanisms, Invariants, or Proof Structure

A reviewable signal design follows nine obligations:

1. Inventory signals, default actions, dispositions, masks, and process or thread targets.
2. Assign one ownership path for every managed signal before worker creation.
3. Treat standard signals as coalescing notification and bound real-time queues.
4. Restrict handlers to proven async-safe actions and transfer work to normal context.
5. Use atomic mask-and-wait interfaces and recheck authoritative predicates in loops.
6. Preserve partial syscall progress, absolute deadlines, cancellation, and restart semantics.
7. Define child reaping, timer overruns, fork, exec, identity reuse, and shutdown.
8. Bound overload and validate sender authority and any attached value.
9. Test adversarial timing while separating platform guarantees from observed schedules.

The executable model coalesces standard notifications and demonstrates why application work must be drained from authoritative state.

<!-- bijux-verify: {"id":"toy-signal-coalescing","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"generated=5\npending-bits=1\nhandler-runs=1\nwork-drained=5\n","stderr":""}} -->
```python
generated = 5
pending_standard_signal = False
work = []

for item in range(generated):
    work.append(item)
    pending_standard_signal = True

pending_bits = int(pending_standard_signal)
handler_runs = int(pending_standard_signal)
pending_standard_signal = False
drained = 0
while work:
    work.pop(0)
    drained += 1

print(f"generated={generated}")
print(f"pending-bits={pending_bits}")
print(f"handler-runs={handler_runs}")
print(f"work-drained={drained}")
```

The toy is a state illustration, not an operating-system signal test. It omits threads, delivery timing, masks, memory order, handlers, queue limits, failures, and syscalls.

## Alternatives and Trade-Offs

- Minimal handlers reduce unsafe surface but require a handoff channel and normal-context latency.
- Synchronous wait threads simplify logic but reserve a thread and require disciplined inherited masks.
- Self-pipes integrate portably with descriptor loops but can fill and carry only bounded notification tokens.
- Linux signalfd integrates structured records with epoll but is platform-specific.
- Standard signals are ubiquitous and coalescing; real-time signals queue values but consume limited resources.
- `SA_RESTART` reduces visible interruptions but can complicate prompt cancellation and deadline handling.
- Signals provide low-overhead control notification; sockets or queues provide richer framing, flow control, and acknowledgment.
- Alternate stacks can support bounded fault reporting but add per-thread memory and lifecycle complexity.
- Process-wide shutdown signals compose with supervisors but need idempotent internal state transitions.

## Failure Modes and Misconceptions

1. **“A handler is just another callback.”** it can interrupt unsafe code and invariants.
2. **“Thread-safe means async-signal-safe.”** the latter has stricter interruption constraints.
3. **“Every standard signal generation is delivered.”** repeated pending instances can coalesce.
4. **“Dispositions are per thread.”** dispositions are process-wide; masks are per thread.
5. **“Blocking discards a signal.”** a nonignored signal normally becomes pending until accepted or unblocked.
6. **“A signal identifies completed work.”** it generally says relevant state may have changed.
7. **“Checking then calling pause is safe.”** delivery in the gap can cause indefinite sleep.
8. **“`SA_RESTART` restarts everything.”** interface and progress semantics vary.
9. **“Retrying after `EINTR` repeats nothing.”** partial or external side effects may already exist.
10. **“One `waitpid` handles `SIGCHLD`.”** multiple child transitions can require a drain loop.
11. **“Queued signals cannot be lost.”** queues are bounded and sends can fail.
12. **“A PID always names the intended process.”** numeric identities can be reused.
13. **“Returning from a fault handler recovers.”** the faulting condition may remain invalid.
14. **“Handler logs prove timing.”** unsafe logging and measurement perturbation can invalidate the evidence.

## Worked Examples

### Example 1

Five identical standard signals arrive while blocked. One pending bit remains. On acceptance, normal code drains five queued work items from the authoritative queue.

### Example 2

A handler calls formatted logging while another thread was interrupted inside the same library's locked state. The handler deadlocks. A nonblocking wake token and normal-context logger avoid reentry.

### Example 3

The main thread unblocks `SIGTERM` before creating workers. A later worker inherits a different mask and unexpectedly receives termination. Blocking the full managed set before any thread creation establishes ownership.

### Example 4

A loop sees `shutdown=false`; `SIGTERM` sets it; the loop then calls `pause`. No further signal arrives. `sigsuspend` with a prepared mask combines unblocking and sleep atomically.

### Example 5

A read returns 400 bytes of a 1,000-byte frame before interruption. Restarting the original read target discards progress. The parser retains 400 and requests the remaining 600.

### Example 6

Three children exit close together and one `SIGCHLD` is observed. The parent loops nonblocking waits until none are ready, recording all three statuses and preventing zombies.

### Example 7

A self-pipe fills during a burst. The handler's nonblocking write fails, but an earlier unread token remains and the event loop drains all authoritative state. Counting pipe bytes as events would be incorrect.

### Example 8

A real-time sender reaches the receiver's queue limit. Its send fails. The design either retries under a deadline or retains work in a flow-controlled queue; it never reports delivery.

### Example 9

A delayed controller sends a reload to numeric PID 412 after the original service exited. The PID now belongs to another process. A lifecycle-bound handle or generation check prevents misdelivery.

### Example 10

A service receives two termination requests. The first begins bounded draining; the second either leaves that idempotent transition unchanged or invokes a documented escalation path. Neither performs cleanup in the handler.

## Cross-Program Connections

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies memory ordering, cancellation, and thread coordination. [Security Engineering](../../25-security-engineering/ROADMAP.md) frames signal permission, identity reuse, and control authority.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects bounded reaction, watchdogs, observability, and assurance. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) generalizes notifications versus durable state, failure detectors, idempotency, and epochs.

Within this program, [OS-026](026-pipes-and-byte-streams.md), [OS-027](027-shared-memory.md), [OS-029](../ROADMAP.md), and [OS-030](../ROADMAP.md) compare IPC semantics and composition.

## References

- Linux man-pages project, [signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html), current page checked 2026-09-04. Dispositions, masks, pending state, targeting, handlers, standard and real-time signals, and inheritance.
- Linux man-pages project, [sigaction(2)](https://man7.org/linux/man-pages/man2/sigaction.2.html), current page checked 2026-09-04. Handler installation, masks, flags, extended information, restart, and errors.
- Linux man-pages project, [sigprocmask(2)](https://man7.org/linux/man-pages/man2/sigprocmask.2.html), current page checked 2026-09-04. Blocking masks, pending delivery, multithreading cautions, and errors.
- Linux man-pages project, [sigwaitinfo(2)](https://man7.org/linux/man-pages/man2/sigwaitinfo.2.html), current page checked 2026-09-04. Synchronous acceptance, information, timeouts, interruption, and thread behavior.
- Linux man-pages project, [sigsuspend(2)](https://man7.org/linux/man-pages/man2/sigsuspend.2.html), current page checked 2026-09-04. Atomic temporary masks, waiting, return behavior, and race avoidance.
- Linux man-pages project, [signal-safety(7)](https://man7.org/linux/man-pages/man7/signal-safety.7.html), current page checked 2026-09-04. Reentrancy, atomicity, async-signal-safe interfaces, errno, fork, and deviations.
- Linux man-pages project, [signalfd(2)](https://man7.org/linux/man-pages/man2/signalfd.2.html), current page checked 2026-09-04. Descriptor-based acceptance, masks, records, readiness, fork, exec, and limitations.
- Linux man-pages project, [kill(2)](https://man7.org/linux/man-pages/man2/kill.2.html), current page checked 2026-09-04. Process and process-group targets, permission, existence tests, and errors.
- Linux man-pages project, [pidfd_send_signal(2)](https://man7.org/linux/man-pages/man2/pidfd_send_signal.2.html), current page checked 2026-09-04. Linux process-handle signaling, information, flags, permissions, and identity.
- Linux man-pages project, [waitpid(2)](https://man7.org/linux/man-pages/man2/waitpid.2.html), current page checked 2026-09-04. Child state, nonblocking drains, status, SIGCHLD interactions, and errors.
- The Open Group, [General Information: Signal Concepts](https://pubs.opengroup.org/onlinepubs/9799919799/functions/V2_chap02.html), POSIX.1-2024, checked 2026-09-04. Generation, delivery, actions, masks, pending state, queueing, and async-signal safety.

## Exercises

### Exercise 1

Design signal ownership for a multithreaded service handling termination, reload, child exit, and fatal faults. Specify masks, dispositions, acceptance paths, and inheritance.

### Exercise 2

Prove a mask-and-wait loop avoids the lost-wakeup race. Include predicate updates, spurious return, cancellation, and timeout.

### Exercise 3

Design a self-pipe handoff whose pipe can fill. State why wake-token loss does not lose authoritative work and how shutdown is bounded.

### Exercise 4

Specify correct handling for interrupted reads, writes, sleep, and child waits. Include partial progress, absolute deadline, restart, and idempotency.

### Exercise 5

Construct an assurance review for signal-driven shutdown under overload. Cover identity, permissions, reaction bounds, deadlock, evidence, and external escalation.

## Answers to the Exercises

### Answer 1

In the initial thread, install deliberate dispositions and block termination, reload, and child signals before creating workers. A dedicated control thread synchronously accepts that set, translates it into ordinary synchronized state, drains all child statuses, and executes versioned reload and idempotent shutdown. Workers inherit the blocked mask. Fatal synchronous faults retain a bounded crash policy, optionally with correctly provisioned per-thread alternate stacks, rather than joining the control set.

The launch path documents which dispositions and masks cross fork and exec and restores the child program's expected state. Wake descriptors use close-on-exec. No asynchronous handler performs allocation, locks, or logging. Repeated termination invokes a documented escalation rule, and reload preserves the old configuration if validation fails.

### Answer 2

Block the signal before examining predicate `A`. While `A` is false, call `sigsuspend` or an equivalent atomic interface with a temporary mask that unblocks it during sleep. Generation before the call leaves it pending and the atomic transition delivers it; generation after sleep begins wakes the thread. There is no exposed interval between unblocking and sleeping.

On every return, restore or retain the intended blocked mask and recheck `A`; delivery is not proof of truth. Cancellation changes `A` through the same synchronization. A timed form uses an absolute deadline or recomputes remaining monotonic time so unrelated signals cannot extend the bound.

### Answer 3

Create a nonblocking close-on-exec pipe before handlers can run. The handler saves `errno`, marks an allowed coalescing flag if required, attempts one bounded async-safe write, ignores full-pipe failure under the invariant that a prior unread byte already makes the loop readable, then restores `errno`. It never blocks.

The event loop drains the pipe and then drains or evaluates authoritative state until quiescent. Work lives in a separately synchronized bounded queue or state machine, so token count need not equal work count. Shutdown closes ownership in normal context, prevents new work, drains within a deadline, and tolerates handler activity according to an explicit descriptor-lifetime protocol.

### Answer 4

For every call, first interpret a positive result as committed partial progress and advance the buffer cursor. Retry `EINTR` only when the operation is safe to continue; do not replay an external side effect whose completion is uncertain. For reads and writes, retain exact prefixes. For sleep, recompute remaining time from an absolute monotonic deadline. `SA_RESTART` is treated as an interface-specific convenience, never as the whole policy.

For child waits, loop nonblocking until no relevant status is ready, even after one notification. Cancellation and shutdown are checked between retries. Request identifiers or idempotent state transitions protect operations that can be observed externally. Every path distinguishes completed, partial, timed out, canceled, peer-ended, and failed outcomes.

### Answer 5

Define managed and fatal signals, sender authority, process identity binding, control-thread masks, shutdown stages, maximum admission-stop and process-exit times, repeated-signal escalation, and supervisor grace intervals. Analyze a receiver deadlocked outside signal-safe recovery, full real-time or self-pipe queues, worker mask errors, PID reuse, child-reaping bursts, and dependencies that do not close.

Test each delivery point around initialization, locks, blocking calls, overload, fork, exec, and shutdown; preserve kernel, runtime, topology, raw timing, and failures. Static review audits handler operations and mask inheritance. Named OS, runtime, operations, security, real-time, safety, and independent-verification reviewers assess whether an external supervisor or watchdog is required. The toy coalescing model is not certification.
