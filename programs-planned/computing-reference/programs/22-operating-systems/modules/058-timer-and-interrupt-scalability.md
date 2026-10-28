---
module_id: OS-058
program: Operating Systems
level: 2
module_number: 58
title: Timer and Interrupt Scalability
status: complete
last_verified: 2026-09-04
---

# Timer and Interrupt Scalability

## One-Page Review

### Governing question

How should an operating system represent, route, execute, defer, migrate, and retire timers and interrupts across many processors so latency and correctness remain bounded without creating global contention, interrupt storms, needless wakeups, or unaccounted interference?

### Essential definitions

- A **clocksource** supplies a monotonically advancing counter used to measure time.
- A **clock event device** delivers an event at a programmed time, either periodically or in one-shot mode.
- A **timer** requests callback or wakeup processing at or after a deadline under stated clock, slack, context, and cancellation semantics.
- A **high-resolution timer** uses time-ordered nanosecond-based expiry rather than a coarse timeout wheel.
- A **timer wheel** groups ordinary timeout events into buckets optimized for common cancellation and coarse expiration behavior.
- A **tickless** configuration suppresses periodic scheduling ticks while a CPU is idle or meets full-dynticks conditions.
- An **interrupt request (IRQ)** maps an interrupt source through controller and kernel state to one or more handlers.
- A **hard interrupt handler** runs in restricted interrupt context; a **threaded handler** performs deferred work in schedulable thread context.
- A **softirq** is deferred kernel work that can run after hard-interrupt return or in a per-CPU kernel thread under pressure.
- **Interrupt affinity** constrains the CPUs eligible to receive a given interrupt; the effective mask can differ from the requested mask.

### Central model, mechanism, or theorem

For each event `e`, track release time `r_e`, deadline `d_e`, allowable lateness or slack `s_e`, execution cost `c_e`, routing set `A_e`, and execution context. A legal coalesced firing time `f_e` satisfies `d_e <= f_e <= d_e+s_e`; hard deadlines have zero or explicitly bounded slack. The platform minimizes a measured objective such as `wakeups + contention + migration + energy + latency_penalty + overload_penalty`, subject to time-ordering, interrupt-flow, affinity, lifetime, synchronization, and service constraints.

Scalability comes from partitioning common state per CPU or per queue, batching work, coalescing flexible deadlines, and doing minimal bounded work in hard-interrupt context. It does not mean delaying everything: urgent events need prompt service, while unbounded arrival rates require moderation, polling, admission, or backpressure because no handler structure can create capacity.

### Critical invariants

- A timer callback runs no earlier than its applicable deadline unless its API explicitly permits early expiration.
- Cancellation and teardown establish whether a callback is absent, pending, executing, rearming, or fully synchronized before state is freed.
- Monotonic deadlines do not jump when wall-clock time is corrected; real-time deadlines follow their documented clock semantics.
- Each interrupt occurrence follows its controller's mask, acknowledge, end-of-interrupt, edge, level, sharing, and replay protocol.
- Hard-interrupt work is bounded and cannot sleep; deferrable or blocking work runs in an appropriate later context.
- Per-CPU timer and interrupt state is migrated or drained safely during CPU hotplug.
- Effective IRQ routing, not merely a requested hint, determines placement evidence.
- Overload handling preserves forward progress through budgets, batching, moderation, polling, priority, and backpressure.

### Common failures

Common mistakes are using a busy wait for a sleepable delay, confusing wall time with monotonic elapsed time, assuming nanosecond representation guarantees nanosecond wakeup, arming every periodic task at the same instant, canceling a timer without synchronizing an executing callback, rearming during teardown, moving per-CPU timers without lifetime coordination, doing blocking work in hard-interrupt context, acknowledging an edge or level interrupt incorrectly, routing all device queues to one CPU, assuming an affinity hint was applied, letting softirq work run without a budget, and reporting average interrupt rate while hiding bursts, queue depth, tail latency, or lost service.

### Compact example

Four flexible timers have legal firing windows `[100,105]`, `[103,107]`, `[107,110]`, and `[109,112]`. A greedy legal schedule fires the first two at 105 and the last two at 110, reducing four wakeups to two. This illustrates deadline-window intersection only; it does not model callback cost, clock-event resolution, CPU placement, concurrent insertion, power-state exit, or hard deadlines.

### Connections

[OS-004](004-interrupts-and-exceptions.md), [OS-014](014-context-switching.md), [OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-051](051-per-cpu-state.md), and [OS-056](056-processor-affinity.md) connect scalable events to privilege transitions, scheduling, evidence, local ownership, and routing.

## Governing Question

Time and external events enter every operating-system subsystem. At small scale, one periodic tick, one timer list, and one interrupt line can look sufficient. At many cores and millions of events, shared locks, cache-line bouncing, broadcast wakeups, vector limits, and deferred-work queues become first-order design constraints.

The governing question joins correctness and cost. A timer must respect its clock and lifetime contract; an interrupt must respect device and controller flow; both must deliver service under concurrency, hotplug, power management, and overload. Performance shortcuts that violate those contracts are not scalability.

## Why This Matters

Timers drive scheduling, retransmission, leases, timeouts, rate limits, storage, networking, and control loops. Interrupts report device completion, input, errors, interprocessor requests, and platform events. A shared bottleneck or storm in either path affects the entire system.

The trade-offs are sharp. Coalescing saves wakeups and energy but adds delay. Interrupt moderation improves throughput but can hurt latency. Per-CPU queues reduce contention but complicate migration and remote insertion. Tick suppression reduces noise but transfers housekeeping work and changes observation paths.

Rare lifecycle races are especially dangerous. A callback can outlive its owner, a level interrupt can retrigger forever, or CPU offlining can strand queued work. Durable engineering specifies synchronization and teardown as carefully as the steady-state fast path.

## Prerequisites and Retrieval

Review [OS-002](002-privilege-levels-and-protection-rings.md), [OS-003](003-system-calls-and-user-kernel-transitions.md), [OS-004](004-interrupts-and-exceptions.md), [OS-007](007-kernel-data-structures.md), [OS-014](014-context-switching.md), [OS-016](016-scheduling-objectives.md), [OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-022](022-spinlocks-and-interrupt-context.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-054](054-kernel-read-copy-update.md), [OS-056](056-processor-affinity.md), and [OS-057](057-load-balancing-across-cores.md).

Retrieve these distinctions:

- clocksource reading and clock-event delivery are different responsibilities;
- monotonic, boot, wall, raw, process-CPU, and thread-CPU clocks have different semantics;
- resolution, precision, accuracy, wakeup latency, and deadline slack are not synonyms;
- hard interrupt, softirq, threaded interrupt, kernel worker, and process contexts permit different operations;
- edge-triggered and level-triggered interrupt flows require different acknowledgement and masking order;
- per-CPU ownership reduces sharing but makes remote operations and hotplug explicit;
- interrupt affinity, task affinity, memory placement, and device queue placement are separate controls;
- overload must be controlled at the producer, queue, or service boundary rather than hidden in an unbounded handler loop.

## Learning Objectives

After this module, you should be able to:

1. distinguish clocksources, clock events, ticks, timer wheels, high-resolution timers, deadlines, slack, and latency;
2. design per-CPU timer bases with safe insertion, cancellation, callback, migration, rearming, and teardown;
3. trace edge, level, shared, per-CPU, threaded, managed, and interprocessor interrupt paths;
4. divide work among hardirq, softirq, polling, threaded, workqueue, and process contexts;
5. coordinate IRQ affinity, queues, workers, memory, isolation, nohz, and CPU hotplug;
6. control storms and overload through batching, moderation, budgets, backpressure, and recovery;
7. build experiments and assurance evidence for latency, throughput, energy, fairness, and lifecycle correctness.

## Core Exposition

### Timekeeping architecture

Timekeeping converts hardware counters into kernel clock values and exposes consistent reads under concurrent updates. A clocksource must be sufficiently stable, monotonic for its role, and convertible without overflowing the represented interval.

Timer expiration is a separate concern. A clock event device programs a future notification; the timer subsystem decides which deadline to program and which callbacks become ready when the event arrives.

### Clock domains

Elapsed-time timeouts normally use a monotonic clock so wall-clock steps do not shorten or extend them unexpectedly. Calendar alarms use a real-time clock whose value can be corrected. Boot-time clocks may include suspension while ordinary monotonic time may follow another documented rule.

Store the clock identity with every absolute deadline. Converting once between clock domains and then assuming their offset is permanent creates errors after synchronization, suspend, or namespace changes.

### Resolution and wakeup latency

An API can represent nanoseconds even when hardware, configuration, power states, and scheduler delay make actual wakeups coarser. Resolution describes distinguishable clock or event granularity; latency describes delay between eligibility and execution.

Measure the distribution from programmed deadline through hardware delivery, interrupt handling, callback readiness, scheduler wakeup, and thread execution. A single timestamp at the end cannot identify which stage delayed service.

### Periodic tick

A periodic tick supplies scheduling and time-accounting work at a fixed rate. It is simple and bounds how long some maintenance waits, but every tick interrupts a CPU even when nothing useful is due.

At scale, unnecessary ticks consume energy and disturb cache and latency-sensitive work. Modern designs program the next required event and suppress periodic ticks when invariants allow.

### Idle tick suppression

Idle tickless operation stops periodic ticks while a CPU has no runnable work and schedules the next required event. Longer idle intervals permit deeper power states.

Entry and exit have cost, and a newly inserted earlier timer may need to reprogram or wake the target CPU. The design trades recurring noise for more careful deadline and remote-enqueue coordination.

### Full dynticks

Full-dynticks operation can stop the scheduling tick while a CPU runs a single eligible userspace task and no dependency requires the tick. It is intended for specialized low-jitter or high-performance workloads.

Kernel entry, multiple runnable tasks, POSIX CPU timers, accounting, tracing, and other dependencies can retain or restart the tick. Treat tick suppression as observed state, not a boot-option promise.

### Housekeeping CPUs

Housekeeping processors execute work offloaded from isolated or full-dynticks CPUs, including unbound timers, workqueues, kernel threads, and some accounting. Offload reduces target noise and concentrates demand elsewhere.

Provision housekeeping for peak and failure conditions. One overloaded housekeeping CPU can delay timers, RCU work, device service, monitoring, and recovery for the whole isolated set.

### Timer wheel

A timer wheel buckets ordinary timeout events by expiry ranges. Many timeouts are canceled before firing and do not need strict nanosecond ordering; bucket operations can be cheap and bounded.

Wheel granularity and cascading behavior are part of the contract. A wheel is appropriate for coarse timeout management, not automatically for precision scheduling whose deadlines require exact ordering.

### High-resolution timers

High-resolution timers use a time-ordered structure and one-shot clock events to represent precise expiry. Their nanosecond basis avoids forcing precision requirements into a coarse wheel optimized for another workload.

Precision has cost: ordered insertion, reprogramming, interrupt frequency, and power-state exits. Use high resolution only where the service objective benefits from it.

### Per-CPU timer bases

Per-CPU bases keep common insertion, expiration, and cancellation local and avoid one global lock. Each CPU programs the earliest relevant local expiry.

Remote insertion can acquire another base, queue a request, or choose a local execution policy depending on API semantics. The path must reprogram an idle target when the new timer precedes its current event.

### Timer ordering

Timers with the same or nearby expiry do not automatically have application ordering semantics. Data structures define a deterministic implementation order only if the API promises one.

Callbacks that depend on each other use explicit synchronization or a single owner. Never derive correctness from observed incidental order among equal deadlines.

### Absolute and relative deadlines

A relative timeout computes an absolute deadline from a selected clock at arm time. Repeating relative sleeps can accumulate callback and scheduling delay.

Periodic control often advances an absolute phase deadline, detecting missed periods explicitly. This prevents drift while still requiring a policy for catching up, skipping, or shedding work.

### Timer slack and coalescing

Slack defines how late a flexible timer may fire. Intersecting allowable windows lets the kernel combine wakeups, extend idle time, and batch callbacks.

Slack is a latency budget, not free delay. Hard deadlines, retransmission control, and safety timeouts need domain-specific bounds; applying global coalescing can violate correctness.

### Callback execution context

Some timer callbacks execute in interrupt or softirq context and cannot sleep. Others enqueue work for thread or process context. The API contract determines locking, allocation, and blocking rules.

Callbacks should be short, bounded, and explicit about rearming. Long work delays unrelated expirations on the same CPU and creates misleading timer-latency symptoms.

### Cancellation states

Cancellation can find a timer inactive, pending on a queue, selected for expiry, executing, or rearming. A non-synchronizing cancel may only remove a pending instance and can return while the callback runs.

Synchronous cancellation waits or coordinates until execution is impossible, subject to context restrictions and deadlock rules. The owner cannot hold a lock that the callback needs while waiting for it to finish.

### Rearming races

A periodic or self-rearming callback can enqueue a new instance while teardown cancels the old one. A generation flag, stopped state, and synchronized cancellation prevent resurrection after owner destruction.

Publish teardown state before cancellation, make the callback check it before rearming, and release memory only after all executions and references quiesce.

### Timer migration

CPU idle, isolation, hotplug, or policy can move timers between bases. Migration preserves clock, deadline, slack, callback identity, and cancellation semantics while changing queue ownership.

Lock ordering and state validation prevent a timer from existing on two bases or none. After movement, reprogram both affected clock-event devices if their earliest expiry changes.

### Deferrable timers

A deferrable timer does not wake an otherwise idle CPU merely to run background work. It executes when the CPU next becomes active or another nondeferrable event occurs.

Use deferrable behavior only when unbounded idle delay is acceptable. Leases, watchdogs, and correctness deadlines generally cannot rely on eventual activity.

### Interrupt sources and controllers

Devices and processors assert interrupt sources through one or more interrupt controllers. The controller maps hardware identifiers and delivery state into a logical IRQ and target CPUs.

Controllers differ in masking, acknowledgement, end-of-interrupt, retrigger, priority, routing, and vector limitations. Generic interfaces hide common structure but do not erase hardware-specific constraints.

### Edge-triggered flow

An edge records a transition. If another edge arrives while masked or before state is recorded, hardware and controller behavior determine whether it is latched or lost.

Handlers acknowledge and order device-state reads according to the protocol. They must drain or preserve every represented event without assuming the line remains asserted.

### Level-triggered flow

A level remains asserted while the device condition persists. Masking prevents immediate reentry while the handler services the cause; clearing device state and issuing end-of-interrupt in the correct order prevents a storm.

If the cause is not cleared, unmasking retriggers promptly. This is useful for avoiding lost work and dangerous when the device or handler is broken.

### Shared interrupt lines

Several devices can share a logical line on supported hardware. Each handler checks whether its device owns the event and returns the appropriate disposition.

A slow, incorrect, or always-claiming handler harms every sharer. Registration, removal, device cookies, and synchronization prevent calling freed state during concurrent interrupt delivery.

### Message-signaled interrupts

MSI and MSI-X let a device signal through messages and often provide multiple vectors for separate queues. Multiple vectors improve routing and parallelism while consuming finite controller and per-CPU vector resources.

Allocate queues and vectors from measured useful concurrency. Hundreds of mostly idle queues increase memory, bookkeeping, and suspend or hotplug pressure without increasing service.

### Per-CPU interrupts

Some interrupts are inherently per CPU, such as local timer or interprocessor events. Their handler and state follow CPU lifecycle rather than ordinary movable device affinity.

Registration and teardown cover every participating CPU, including later online processors. Per-CPU identity avoids sharing but multiplies initialization and drain obligations.

### Interrupt affinity

IRQ affinity selects eligible target CPUs. Requested masks can be constrained by controller support, online CPUs, managed-vector policy, and subsystem decisions.

Read effective affinity and per-CPU interrupt counts. A configuration file or affinity hint is intent, not proof that hardware delivered events there.

### Managed interrupts

Managed interrupt vectors are allocated with affinity information and follow device queue and CPU lifecycle. The kernel can migrate them when CPUs go offline, while user changes may be restricted.

Isolation behavior can be best effort when a managed mask contains no suitable online housekeeping CPU. Capacity plans include a valid nonisolated target where the device permits one.

### Interrupt distribution

Spreading queue interrupts across CPUs increases parallel service and avoids one hot target. Packing low-rate interrupts can preserve idle CPUs and cache locality.

Balance actual work rather than vector count. One queue can carry most traffic, and a CPU can spend more time in deferred processing than its hard-interrupt counter suggests.

### Hard interrupt handlers

The primary handler identifies and stabilizes the event with minimal bounded work. It cannot sleep and must respect interrupt, locking, and allocation constraints.

Mask or quiesce the source, capture essential status, acknowledge under the device protocol, schedule later work, and return. Unbounded packet or completion loops do not belong in the hard path.

### Threaded interrupts

A threaded handler moves substantial service into a schedulable kernel thread while a small primary handler protects the device protocol. Thread context permits blocking operations under documented rules.

Scheduling priority and affinity now influence interrupt completion latency. A starved thread can leave the source masked or the device queue full, so admission and observability cover it.

### Softirqs

Softirqs execute deferred work with restricted semantics, often on the CPU that received or raised the event. They reduce thread scheduling overhead but can monopolize return paths under sustained load.

Budgets bound one activation, and remaining work can continue in a per-CPU kernel thread so ordinary scheduling regains control. Budget selection trades throughput against latency for other work.

### NAPI and polling

Network NAPI converts repeated receive interrupts into budgeted polling. The interrupt schedules a polling instance; polling drains up to a budget and reenables interrupt delivery when the queue is caught up.

Under load, batching amortizes interrupt and cache costs. Under light traffic, interrupts preserve latency and avoid continuous polling. Correct completion prevents both missed wakeups and interrupt-poll livelock.

### Threaded NAPI

Threaded NAPI runs an instance in a dedicated kernel thread. Its affinity can align polling with the queue's IRQ and application path.

The mapping between vectors, NAPI instances, and queues is driver-specific. Observe it rather than assuming identifier order, and account for scheduler priority and contention.

### Interrupt moderation

Hardware or driver moderation waits for a count or time threshold before interrupting. It reduces event rate and increases batch size at the cost of added completion latency.

Static settings rarely fit idle, burst, and saturation phases equally. Adaptive moderation uses bounded feedback and preserves explicit maximum latency requirements.

### Interprocessor interrupts

Processors send IPIs for rescheduling, TLB invalidation, function calls, stop coordination, and other cross-CPU work. A broadcast IPI scales with target count and interrupts unrelated execution.

Batch requests, narrow target masks, avoid redundant sends, and keep handlers bounded. The next module treats TLB shootdowns as a particularly important IPI-driven protocol.

### Interrupt storms

A storm is an event rate that consumes disproportionate service, possibly because a source remains asserted, a device fails, or valid traffic exceeds capacity. Rate alone does not distinguish fault from legitimate overload.

Detect per-source rate, handler time, retriggers, queue progress, and device status. Masking protects the system but can lose service; recovery needs quarantine, reset, escalation, and an explicit data-integrity contract.

### Overload and backpressure

When arrival work exceeds handler capacity, queues grow or events collapse. Batching improves efficiency but cannot solve an indefinitely positive arrival-service gap.

Apply producer moderation, queue limits, receive-side distribution, flow control, admission, load shedding, or device reset according to semantics. Reserve service for control and recovery paths.

### Cache and NUMA locality

Place an interrupt, its deferred work, application consumer, descriptors, and buffers near the relevant device and memory when locality matters. Cross-node handoff can cost more than spreading nominal interrupt counts saves.

Do not overload the local group merely to avoid remote access. Measure queue delay, DMA locality, cache transfer, and interconnect bandwidth jointly.

### Isolation and jitter

Low-jitter CPUs seek to exclude movable IRQs, unbound timers, workqueues, and kernel threads. Full dynticks can suppress the local scheduling tick under strict conditions.

Per-CPU interrupts, unavoidable kernel entry, firmware events, NMIs, watchdogs, and SMT sibling activity can remain. State the achieved boundary and retain housekeeping capacity.

### CPU hotplug

Offlining a CPU migrates movable timers and interrupts, drains per-CPU work, and invokes subsystem callbacks. Managed queues and local clock-event devices follow their lifecycle rules.

Order prevents new events from targeting a draining CPU, waits for in-flight handlers, transfers queued work, and only then destroys local state. Online failure unwinds partially initialized resources.

### Suspend and resume

Suspend can stop CPUs and clocks, concentrate interrupts, and require a broadcast or wake-capable event source. Resume reconciles elapsed clock domains and reprograms deadlines.

Timers specify whether suspended time counts. Devices establish which interrupts can wake the platform and how pending status survives the transition.

### Virtualization

Guests receive virtual clocks, timers, and interrupts whose delivery depends on hypervisor scheduling and host devices. Posted interrupts and paravirtual clocks reduce exits but do not remove host contention.

Separate guest programming latency, host delivery, vCPU scheduling, and guest handler time. A guest-only trace cannot prove physical interrupt latency.

### Security and denial of service

Untrusted software can arm many timers, create wakeup churn, or drive interrupt-heavy devices. Quotas, aggregation, permissions, queue bounds, and accounting limit cross-tenant impact.

Timer and IRQ metadata must resist identifier reuse and use-after-free. Fault handling avoids logging each event so diagnostics do not amplify a storm.

### Observability

Record timer insertion, cancellation, expiry, callback start and end, reprogramming, migration, lateness, clock, slack, target CPU, and owner. For IRQs, record source, vector, requested and effective affinity, counts, handler time, threaded time, softirq and poll work, queue depth, masking, retriggers, and loss.

Correlate with CPU utilization, run-queue delay, frequency, idle states, wakeups, power, NUMA traffic, device throughput, application latency, hotplug, and configuration generation. Sampling must remain bounded under storms.

### Experiment design

Test coarse and high-resolution timers, zero and nonzero slack, aligned and randomized phases, local and remote insertion, cancellation races, periodic rearming, idle and full-dynticks modes, hotplug, suspend, and overload.

Test edge, level, shared, MSI-X, managed, threaded, polling, moderation, affinity, device failure, queue skew, isolation, and vector pressure. Repeat from cold and warm power states and retain full latency distributions.

### Assurance

Map timer-order, no-early-fire, cancellation, one-base ownership, and teardown invariants to targeted tests and traces. Map interrupt mask, acknowledge, replay, affinity, bounded-hardirq, queue-progress, hotplug, and recovery invariants similarly.

Reviewers include timekeeping, scheduler, IRQ-controller, driver, networking, power, real-time, architecture, performance, security, and operations specialists. Hardware errata and unverifiable firmware behavior remain explicit limitations.

## Definitions and Notation

For timer `e`, let `r_e` be release or arm time, `d_e` the earliest legal firing deadline, `s_e` allowed nonnegative slack, `f_e` actual firing time, and `c_e` callback service cost. Legal coalescing requires `d_e <= f_e <= d_e+s_e`. Lateness is `max(0,f_e-d_e)`; callback completion delay additionally includes `c_e` and any deferred scheduling.

For interrupt source `i`, let `lambda_i` be arrival rate, `b_i` average events retired per service activation, `c_i` service cost, `A_i` effective target CPUs, and `mu_i` sustainable service rate under current placement. Stability requires admitted long-run work below effective service capacity, with burst buffers and latency bounds. This queueing condition is necessary but not sufficient because priority, device protocol, batching, memory, power, and shared resources matter.

Resolution, precision, accuracy, deadline, slack, delivery latency, handler latency, completion latency, throughput, loss, and jitter are separate measures. State the clock, percentile, interval, workload, and topology with every claim.

## Mechanisms, Invariants, or Proof Structure

1. **Choose semantics.** Name the clock, deadline, slack, recurrence, callback context, interrupt flow, loss policy, and completion obligation.
2. **Partition state.** Use per-CPU or per-queue bases for common paths and define remote operations explicitly.
3. **Order safely.** Maintain timer order and IRQ mask, acknowledge, replay and end-of-interrupt protocols under concurrency.
4. **Bound hard work.** Capture essential state in hardirq and defer bounded batches to the proper context.
5. **Coordinate locality.** Align clock events, IRQs, queues, polling, threads, memory and devices without hotspotting.
6. **Control frequency.** Apply slack, coalescing, one-shot events, moderation and polling within service contracts.
7. **Handle overload.** Budget work, preserve scheduler service, backpressure producers and reserve recovery capacity.
8. **Synchronize lifetime.** Cover cancellation, rearming, in-flight callbacks, device removal and identifier reuse.
9. **Support lifecycle.** Drain and rebuild state across idle, isolation, hotplug, suspend, resume and virtualization.
10. **Measure end to end.** Observe programmed deadlines, delivery, callback, deferred service, queue progress, application completion and energy.
11. **Test adversarially.** Exercise simultaneous deadlines, storms, failed devices, skew, full queues, race windows and partial initialization.
12. **Retain evidence.** Preserve topology, clock and device configuration, traces, raw distributions, failures, reviewers and limitations.

<!-- bijux-verify: {"id":"timer-slack-coalescing","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"fire-at=105 timers=0,1\nfire-at=110 timers=2,3\noriginal-wakeups=4\ncoalesced-wakeups=2\nwakeups-saved=2\n","stderr":""}} -->
```python
windows = [(100, 105), (103, 107), (107, 110), (109, 112)]
groups = []

for timer_id, (earliest, latest) in sorted(enumerate(windows), key=lambda item: item[1][1]):
    if not groups or groups[-1][0] < earliest:
        groups.append((latest, [timer_id]))
    else:
        groups[-1][1].append(timer_id)

for firing, timers in groups:
    print(f"fire-at={firing} timers=" + ",".join(str(timer) for timer in timers))
print(f"original-wakeups={len(windows)}")
print(f"coalesced-wakeups={len(groups)}")
print(f"wakeups-saved={len(windows) - len(groups)}")
```

The executable example computes a minimum point cover for fixed intervals using the standard earliest-ending greedy choice. It does not arm kernel timers, prove wakeup timing, model callback cost, account for CPU placement or clock-event resolution, or authorize slack for a real application.

## Alternatives and Trade-Offs

- A global timer queue simplifies ordering but becomes a shared hotspot; per-CPU bases scale local operations and complicate remote insertion and migration.
- Timer wheels make ordinary coarse timeouts cheap but provide bucketed precision; high-resolution ordered queues serve precise deadlines with greater programming and insertion cost.
- Periodic ticks simplify maintenance but wake idle CPUs; one-shot tickless operation saves energy and needs careful reprogramming.
- Zero slack minimizes intentional delay but multiplies wakeups; bounded slack coalesces work and consumes latency budget.
- Relative periodic sleeps are simple and drift with service time; absolute phase deadlines resist drift and require missed-period policy.
- Hardirq service minimizes handoff latency but cannot block and can monopolize CPUs; threaded service is schedulable and adds wakeup delay.
- Interrupt delivery handles light traffic promptly; budgeted polling amortizes heavy traffic and can waste work when idle.
- Many MSI-X queues improve parallelism but consume vectors and state; fewer queues conserve resources and can serialize throughput.
- Spreading interrupts avoids hotspots but activates more CPUs; packing them preserves idle domains and raises local contention.
- Interrupt moderation improves batch efficiency and energy but adds delay; immediate delivery improves light-load latency and increases event rate.
- Local IRQ, poller and consumer placement improves cache and NUMA behavior but can overload one domain; wider placement adds capacity and data movement.
- Synchronous cancellation gives a strong lifetime boundary but can block or deadlock if misused; asynchronous cancellation requires external quiescence.
- Full dynticks reduces periodic noise but shifts work to housekeeping CPUs and constrains workloads; ordinary ticks are simpler and more observable.
- Masking a storm protects CPUs but interrupts device service; continued handling preserves service and can livelock the system.

## Failure Modes and Misconceptions

- **“Nanosecond API means nanosecond wakeup.”** Representation, hardware, power and scheduling determine realized latency.
- **“Wall time is suitable for elapsed timeouts.”** Corrections can move it discontinuously.
- **“A periodic relative sleep preserves phase.”** Work and scheduling delay accumulate drift.
- **“Timer cancellation means the callback cannot be running.”** Only the documented synchronized operation establishes that boundary.
- **“A callback cannot rearm after cancellation.”** Concurrent execution can resurrect it without a stopped-state protocol.
- **“Per-CPU means lock-free.”** Local and remote operations still synchronize ownership and ordering.
- **“Tickless means no interrupts.”** Devices, IPIs, watchdogs and required timers remain.
- **“Interrupt affinity is the same as task affinity.”** They are separate routing constraints.
- **“An affinity hint is an effective route.”** Hardware and subsystem policy may choose differently.
- **“Threaded interrupts remove latency constraints.”** Scheduling and priority become part of the path.
- **“Polling cannot lose events.”** Incorrect completion races can miss a reenable transition.
- **“More vectors always scale.”** Vector, queue, memory, suspend and hotplug costs can dominate.
- **“Average interrupt rate proves capacity.”** Bursts, service time, queue depth and tail latency decide overload.
- **“Masking fixes a level-triggered storm.”** The uncleared source returns when unmasked.
- **“A clean idle benchmark proves isolation.”** Active devices and kernel paths create different interference.

## Worked Examples

### Example 1

Four maintenance timers permit several units of slack. Window intersection coalesces them into two wakeups, while a zero-slack control timer retains its own programmed deadline.

### Example 2

A periodic monitor sleeps relatively after each callback and drifts by callback time. Advancing an absolute phase deadline preserves cadence and reports skipped intervals after overload.

### Example 3

Teardown marks an object stopped, synchronously cancels its timer, and then frees memory. The callback checks stopped before rearming, preventing resurrection.

### Example 4

A level-triggered device remains asserted because the handler unmasks before clearing status. Correct device acknowledgement and end-of-interrupt ordering stops immediate retrigger.

### Example 5

A NIC uses eight MSI-X queues but all effective affinities target CPU 0. Aligning queues, NAPI instances, consumers and buffers across local cores removes the hotspot.

### Example 6

Under a packet burst, NAPI polls up to a budget and leaves residual work for another activation. Ordinary tasks regain scheduler service while batching remains efficient.

### Example 7

An isolated CPU still receives a managed storage interrupt because no eligible housekeeping CPU exists in the vector's managed mask. The capacity plan adds a supported target.

### Example 8

A failed device asserts a level interrupt continuously. The system measures no queue progress, masks and quarantines the source, preserves diagnostics, and resets under a data-integrity policy.

### Example 9

CPU offlining first blocks new timer and IRQ placement, redirects movable interrupts, migrates timers, drains deferred work, synchronizes handlers, and then releases per-CPU state.

### Example 10

A guest observes 20-microsecond handler execution but millisecond completion outliers. Host tracing reveals vCPU scheduling delay between physical delivery and guest entry.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects clocks, counters, interrupt controllers, vectors, cache coherence, power states, NUMA, and virtualization. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects queues, ownership, cancellation, lifetime, work stealing, backpressure, and race analysis.

[Network Engineering](../../24-network-engineering/ROADMAP.md) connects interrupt-driven I/O, queues, polling, moderation, backpressure, packet loss, latency, and throughput. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes feedback control, hazard analysis, lifecycle assurance, overload modes, and evidence. Within this program, [OS-057](057-load-balancing-across-cores.md) covers placement and [OS-059](../ROADMAP.md) covers TLB-shootdown IPIs.

## References

- Linux kernel documentation, [High-resolution timers](https://docs.kernel.org/timers/hrtimers.html), current page checked 2026-09-04. Separation from timeout wheels, nanosecond representation, ordered timer structures and high-resolution design.
- Linux kernel documentation, [NO_HZ: Reducing Scheduling-Clock Ticks](https://docs.kernel.org/timers/no_hz.html), current page checked 2026-09-04. Periodic, idle-tickless and full-dynticks modes, dependencies, trade-offs and adaptive ticks.
- Linux kernel documentation, [Timekeeping](https://docs.kernel.org/core-api/timekeeping.html), current page checked 2026-09-04. Clocksource access, clock choices, cycles, nanoseconds, wrap handling, accessor semantics and driver guidance.
- Linux kernel documentation, [Delay and sleep mechanisms](https://docs.kernel.org/timers/delay_sleep_functions.html), current page checked 2026-09-04. Atomic versus sleepable context, busy waits, sleeps, slack, duration ranges and selection guidance.
- Linux kernel documentation, [Linux generic IRQ handling](https://docs.kernel.org/core-api/genericirq.html), current page checked 2026-09-04. IRQ abstractions, descriptors, flow handlers, threaded handlers, affinity, synchronization, startup and teardown.
- Linux kernel documentation, [SMP IRQ affinity](https://docs.kernel.org/core-api/irq/irq-affinity.html), current page checked 2026-09-04. Default, requested and effective masks and per-IRQ routing controls.
- Linux kernel documentation, [Affinity managed interrupts](https://docs.kernel.org/core-api/irq/managed_irq.html), current page checked 2026-09-04. Managed-vector allocation, affinity, vector pressure, CPU hotplug, suspend and isolation limitations.
- Linux kernel documentation, [CPU Isolation](https://docs.kernel.org/admin-guide/cpu-isolation.html), current page checked 2026-09-04. Housekeeping, scheduler domains, IRQ isolation, full dynticks, workqueues, kernel entry and limitations.
- Linux kernel documentation, [Reducing OS jitter due to per-CPU kthreads](https://docs.kernel.org/admin-guide/kernel-per-CPU-kthreads.html), current page checked 2026-09-04. Per-CPU timer, IRQ, softirq, worker and RCU activity, affinity and tracing.
- Linux kernel documentation, [NAPI](https://docs.kernel.org/networking/napi.html), current page checked 2026-09-04. Interrupt-poll transitions, budgets, completion, scheduling, threaded NAPI, affinity, software coalescing and configuration.

## Exercises

### Exercise 1

Design timers for a service with a hard lease deadline, periodic metrics, idle cleanup, retransmission, and shutdown. Choose clocks, slack, recurrence, callback context, cancellation, and evidence.

### Exercise 2

Trace edge-triggered, level-triggered, threaded, and NAPI-driven interrupt handling. State mask, acknowledge, deferral, completion, reenable, and failure obligations.

### Exercise 3

Design queue, vector, IRQ, polling-thread, application-thread, and memory placement for a dual-socket high-rate NIC under skew and CPU hotplug.

### Exercise 4

Specify a safe CPU-isolation plan for a low-jitter workload. Include ticks, timers, interrupts, kernel threads, workqueues, housekeeping, SMT, devices, and limitations.

### Exercise 5

Build a verification and assurance plan for timer and interrupt scalability. Cover correctness, performance, energy, overload, lifecycle, virtualization, and reproducibility.

## Answers to the Exercises

### Answer 1

Use an appropriate monotonic clock for elapsed lease and retransmission deadlines so wall-clock correction does not alter safety. Give the lease zero or explicitly proven slack and execute only bounded state capture in timer context, handing blocking renewal or failure work to a priority-controlled thread. Advance retransmission from absolute scheduled deadlines with capped backoff, attempt limits, and an explicit late-event policy.

Metrics tolerate measured slack and coalesce across instances; absolute phase deadlines prevent drift and missed periods are counted rather than replayed without bound. Idle cleanup uses a deferrable timer only if arbitrarily long idle delay is safe. Shutdown first publishes stopped state, prevents new arms, synchronously cancels or joins every callback without holding callback-needed locks, drains deferred work, and releases state. Evidence records clock, deadline, slack, arm, expiry, callback, handoff, lateness, cancellation result, rearm generation, workload, power state and failure injection.

### Answer 2

For an edge source, preserve every latched event, acknowledge in controller and device order, capture status, defer bounded work, and handle edges arriving while masked according to hardware semantics. For a level source, mask as needed, service and clear the asserted device condition, issue end-of-interrupt in the prescribed order, and unmask only when immediate retrigger represents real remaining work. A shared line additionally requires each handler to identify ownership and removal to synchronize all in-flight users.

A threaded interrupt uses a bounded primary handler to stabilize and wake the thread; scheduling priority, affinity, completion and device unmasking become explicit. NAPI disables or suppresses queue interrupts, schedules polling, processes no more than its budget, and completes plus reenables only after proving the queue is drained without racing a new arrival. Failed devices, no-progress loops, full queues and teardown lead to bounded masking, quarantine, reset or loss reporting rather than infinite service.

### Answer 3

Discover NIC, PCIe, NUMA, cache, core, SMT, vector and memory topology. Allocate only the number of queues with demonstrated parallel work, spread their managed vectors across physical cores local to the NIC, align each NAPI or polling thread and application consumer with its queue group, and allocate rings and buffers near the dominant DMA and CPU path. Reserve separate redundant housekeeping and control capacity.

Measure per-queue arrivals, batches, drops, depth, IRQ effective affinity and counts, hardirq time, softirq or threaded time, poll budget exhaustion, application completion, cache and NUMA traffic, and latency. Under flow skew, redirect or software-steer within the local group before crossing sockets, then compare delay against remote-access cost. Hotplug blocks new targeting, quiesces queues, redirects vectors, drains polling and handlers, moves consumers and memory policy, validates effective state, and restarts. A prevalidated reduced-queue mode covers vector or CPU shortage.

### Answer 4

Reserve at least two measured housekeeping CPUs where scale and failure require redundancy. Isolate the workload from scheduler domains with the supported runtime mechanism, use full dynticks only when one userspace task and all kernel dependencies permit it, and move unbound timers, workqueues and kernel threads to housekeeping. Route every movable IRQ away, provision valid targets for managed interrupts, disable unused devices and watchdogs only under system safety policy, and keep application syscalls and page faults within the measured jitter budget.

Exclude the physical core's SMT sibling from unrelated work or document its interference. Trace per-CPU interrupts, timers, softirqs, kernel threads, workqueues, context switches, IPIs, RCU and residual ticks during active device, maintenance and failure workloads. State unavoidable local timers, IPIs, NMIs, firmware and hypervisor activity. Test housekeeping overload and loss, hotplug, tracing disabled and enabled, device storms, memory pressure and teardown. Isolation means a measured bounded boundary, not silence.

### Answer 5

For timers, verify clock selection, no-early-fire behavior, slack bounds, ordering assumptions, resolution, insertion and cancellation races, executing callbacks, rearming, one-base ownership, remote enqueue, migration, drift, missed periods, clock correction, idle, full dynticks, suspend, hotplug and teardown. Collect deadline-to-expiry and deadline-to-completion distributions plus wakeups, power states and energy.

For interrupts, test edge, level, shared, per-CPU, MSI-X, threaded and managed flows; affinity requests and effective routes; masking, acknowledgement, retrigger, loss, synchronization and removal; softirq and polling budgets; moderation; queue skew; vector pressure; storms; device failure; isolation; hotplug; suspend and virtualization. Measure arrival, handler, deferred and application-completion latency, batch size, queue depth, loss, CPU time, scheduling delay, throughput and energy. Preserve kernel, configuration, firmware, topology, devices, clocks, power policy, workload, raw traces, counter overhead, seeds, reviewers, negative results and limitations.
