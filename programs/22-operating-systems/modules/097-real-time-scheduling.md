---
module_id: OS-097
program: Operating Systems
level: 2
module_number: 97
title: Real-Time Scheduling
status: complete
last_verified: 2026-09-04
---

# Real-Time Scheduling

## One-Page Review

### Governing question

How can an operating-system team turn timing requirements into an analyzable task model, select scheduling and synchronization mechanisms whose assumptions match the platform, and preserve deadline guarantees under blocking, interrupts, overload, multicore interference and operational change?

### Essential definitions

- A **hard real-time** deadline is part of correctness: a miss can make the result unsafe or invalid.
- A **firm real-time** result has no value after its deadline, although occasional misses may be tolerable at the system level.
- A **soft real-time** deadline expresses utility or quality that degrades with lateness rather than a binary correctness boundary.
- A **job** is one released instance of a recurring or event-triggered task.
- **Worst-case execution time**, `C_i`, is a justified upper bound on processor demand for one job under the modeled platform and path.
- A task's **relative deadline**, `D_i`, is the allowed interval from release to completion; its **period or minimum interarrival time**, `T_i`, constrains releases.
- **Release jitter**, `J_i`, bounds uncertainty in when an event becomes scheduler-visible.
- **Blocking**, `B_i`, bounds delay caused by lower-priority critical sections or other modeled nonpreemptive resources.
- **Response time** is completion time minus release time; **wakeup latency** is only one component of it.
- **Admission control** accepts a workload only when a stated schedulability test and resource model say its guarantees compose.
- A **reservation** limits a task or group to a runtime budget within a period, separating temporal entitlement from ordinary priority.

### Central model, mechanism, or theorem

For independent sporadic tasks on one preemptive processor under fixed priorities, a common response-time recurrence is

`R_i^(k+1) = C_i + B_i + sum over h in hp(i) of ceil((R_i^k + J_h) / T_h) C_h`.

Start with `R_i^0 = C_i + B_i`, iterate until the value stops changing or exceeds `D_i`, and require the converged response time to be no greater than the deadline. The result is conditional: execution bounds, release constraints, priority order, blocking analysis, interrupt accounting and processor model must all be valid. A utilization number or a low measured maximum cannot substitute for those assumptions.

### Critical invariants

- Every admitted activity has a named criticality, release model, execution bound, deadline, resource set and miss policy.
- All processor demand is charged somewhere, including interrupt threads, kernel work, timers, housekeeping, retries and recovery.
- Locking protocols bound priority inversion, including nested and transitive dependency chains.
- Runtime reservations, priorities, affinities and group bandwidth are admitted as one system rather than configured independently.
- Deadline-sensitive memory and I/O paths avoid unbounded faults, allocation, reclaim, firmware and device waits.
- Timing validation covers supported CPU, firmware, thermal, power, virtualization and workload states.
- Overload preserves an explicitly chosen safety hierarchy; it does not merely allow the highest requester to consume the machine.

### Common failures

Frequent failures are equating high priority with a deadline guarantee, treating average execution as WCET, using total utilization as a universal proof, ignoring blocking or release jitter, assigning every service real-time priority, starving housekeeping and recovery, confusing wakeup latency with end-to-end response, measuring only quiet systems, depending on relative sleeps that drift, allocating or faulting memory in critical paths, assuming PREEMPT_RT eliminates firmware and hardware latency, overlooking cgroup and global bandwidth limits, admitting reservations without all kernel demand, migrating tasks across interference domains, and presenting a finite stress-test maximum as an upper bound.

### Compact example

Three sporadic tasks execute on one isolated CPU in priority order. Their `(C,T,D,B)` values are `A=(1,4,4,0)`, `B=(1,5,5,0)` and `C=(2,10,10,1)` in milliseconds. Fixed-priority response-time analysis gives `R_A=1`, `R_B=2` and `R_C=7`; all meet their deadlines even though `C` suffers one millisecond of blocking. This conclusion is valid only if the measured system enforces the release, execution, blocking and interference bounds. Adding an uncharged interrupt source or a three-millisecond critical section invalidates the proof even if ordinary runs still look fast.

### Connections

Real-time scheduling connects concurrency protocols, timer and interrupt design, WCET analysis, memory residency, device and network bounds, CPU isolation, energy and thermal control, virtualization, control theory, mixed-criticality safety, observability and change governance.

## Governing Question

A real-time system is correct only when the right computation completes within the required interval. The scheduler is necessary but not sufficient. Release delivery, kernel preemption, locks, interrupts, memory, devices, shared buses, firmware and recovery work all consume or delay time.

The governing question is therefore not “which policy is fastest?” It is how to construct an evidence-backed temporal contract from event release through useful completion, determine whether all admitted contracts can coexist, enforce the allocation during overload, and keep the assumptions true as software and hardware change.

## Why This Matters

Deadline failures can destabilize a control loop, miss a protection window, corrupt a media pipeline, violate an exchange protocol or make an industrial action unsafe. Average throughput and percentile latency may look excellent while one rare unbounded path defeats correctness.

Real-time authority is also a system-wide privilege. A runaway FIFO thread can starve ordinary tasks, kernel services and the administrator attempting recovery. A reservation with no accounting for interrupts can move the overrun outside the charged task. Isolation that removes every housekeeping path can prevent the system from reporting or correcting a fault.

Sound engineering combines analysis, enforcement and observation. Analysis states what should be schedulable under explicit assumptions. Enforcement contains demand and blocking. Observation tests assumptions and detects drift, but finite measurements do not prove the absence of a longer latency.

## Prerequisites and Retrieval

Before studying this module, be able to:

- distinguish a process, thread, task, job, interrupt and deferred kernel activity;
- explain preemption, fixed and dynamic priority, affinity and run queues;
- reason about mutexes, priority inversion and critical sections;
- interpret monotonic clocks, timers and scheduling latency distributions;
- distinguish a bound, a measurement, an estimate and an assumption.

Retrieve the requirement's event source, action deadline and consequence of a miss; task releases and dependencies; criticality; code and data paths; WCET evidence; periods or minimum interarrival times; jitter; blocking resources; scheduling policy and priority; deadline reservation parameters; CPU topology and affinity; interrupt routing; kernel preemption model; real-time bandwidth controls; cgroups; clock and timer source; power and thermal policy; memory locking and page-fault behavior; device and firmware bounds; virtualization layers; tracing configuration; observed maxima and lost events; overload tests; recovery access; and exact kernel, firmware and configuration identities.

## Learning Objectives

After completing this module, you should be able to:

1. translate hard, firm and soft timing requirements into explicit job parameters;
2. distinguish priority dispatch, reservation, admission and overload control;
3. apply conditional utilization and fixed-priority response-time tests;
4. explain FIFO, round-robin, deadline and constant-bandwidth mechanisms;
5. bound priority inversion with an appropriate locking protocol;
6. account for kernel, interrupt, memory, device and multicore interference;
7. design CPU isolation without starving housekeeping or recovery;
8. validate timing assumptions with tracing while respecting measurement limits;
9. define safe degradation when admitted assumptions fail;
10. govern real-time configuration as privileged, versioned production policy.

## Core Exposition

### Start from the consequence of lateness

Classify the deadline by what happens after a miss. A hard deadline is a correctness boundary, not merely an ambitious service-level objective. A firm result becomes useless after its deadline. A soft workload retains diminishing value.

Specify the response to a miss: enter a safe state, discard stale output, reuse the last valid value, reduce quality, shed lower-criticality work or restart a component. “Log and continue” is not a complete policy for a safety-relevant miss.

### Model jobs rather than vague services

A periodic task releases jobs at a regular period. A sporadic task has a minimum interarrival time. An aperiodic task lacks that minimum unless an arrival envelope or server constrains it.

For task `i`, record release `r_i`, execution demand `C_i`, relative deadline `D_i`, period or minimum interarrival `T_i`, release jitter `J_i`, blocking `B_i` and criticality. Dependencies and precedence may make a collection of individually schedulable jobs miss an end-to-end deadline.

### Justify execution-time bounds

WCET is an upper bound for a declared code path, build, input space, cache and memory behavior, processor, firmware and operating condition. The maximum observed duration is only evidence about tested executions.

Separate CPU execution from suspension and device wait. Either bound suspension explicitly with a compatible analysis or restructure the path. Include retry limits, error handling, cache effects, interrupt execution and kernel services according to the chosen accounting model.

### Match the scheduler to the task model

Fixed-priority policies select the highest-priority runnable job. Rate-monotonic order assigns shorter periods higher priority under restrictive periodic assumptions. Deadline-monotonic order uses shorter relative deadlines when deadlines differ from periods.

Earliest-deadline-first selects the runnable job with the earliest absolute deadline. Its strong uniprocessor results depend on assumptions such as preemptibility, independent jobs and valid execution and arrival bounds. A policy name alone carries no guarantee.

### Understand FIFO and round-robin semantics

Under `SCHED_FIFO`, a runnable thread continues until it blocks, yields, is preempted by a higher-priority thread or changes policy/priority. Equal-priority peers do not receive an automatic time slice from FIFO.

`SCHED_RR` adds a quantum among equal-priority runnable threads. It does not reserve processor capacity or make an infeasible task set feasible. Both policies require bounded execution and an intentional priority assignment.

### Separate reservations from priorities

A reservation promises or caps runtime within a replenishment interval. Linux `SCHED_DEADLINE` exposes runtime, deadline and period parameters and implements earliest-deadline-first scheduling with a constant-bandwidth server model.

The runtime should cover the modeled demand, the deadline represent required completion, and the period constrain replenishment and arrivals. Admission control protects the aggregate model; runtime depletion throttles the entity so an overrun does not silently consume every peer's entitlement.

### Treat admission as a transaction

Admission must evaluate the whole affected scheduling domain: existing tasks, new reservation, group limits, interrupt and kernel demand, affinities and recovery capacity. Reject or renegotiate when the proof does not fit.

Configuration systems should not apply priorities first and bandwidth later through unrelated writes. Validate a complete desired state, apply it with rollback, and confirm the kernel accepted the intended parameters.

### Analyze fixed-priority response time

For a compatible single-processor model, response-time analysis accumulates a task's own execution, lower-priority blocking and every higher-priority release that can interfere within the candidate response window.

Iterate until the estimate stabilizes. Growth beyond the deadline demonstrates failure under the model. Convergence demonstrates schedulability only under the model; it does not validate inputs such as WCET or blocking bounds.

### Use utilization tests narrowly

`U = sum(C_i/T_i)` is a useful demand summary. Under some ideal EDF models, utilization no greater than one is sufficient. Fixed-priority sufficient bounds vary with task count and assumptions. Arbitrary deadlines, jitter, blocking, nonpreemptive regions and shared resources require stronger analysis.

Utilization below one is not a universal proof. A burst can create excessive demand before short deadlines even when long-run utilization is low.

### Bound priority inversion

A high-priority job can block on a resource held by a lower-priority job while medium-priority work prevents the holder from running. Priority inheritance temporarily raises the owner's effective priority so it can release the resource.

Nested dependencies require transitive propagation. Priority-ceiling protocols can prevent classes of deadlock and give analyzable blocking under their declared rules. Inventory every lock, nesting order and maximum critical-section duration; inheritance cannot bound an unbounded holder.

### Understand PREEMPT_RT

PREEMPT_RT makes most kernel execution preemptible, converts many spin-lock uses into sleeping real-time mutex behavior, and forces most interrupts into schedulable threads. These changes make more latency attributable and priority-controlled.

Some raw spinlock, interrupt-disabled, NMI, architecture, entry and low-level paths remain nonpreemptible. Threaded interrupts still consume CPU and need priorities and affinities. PREEMPT_RT reduces classes of latency; it does not create an automatic end-to-end deadline proof.

### Account for interrupt demand

An interrupt can delay a task before wakeup, preempt it after dispatch or trigger deferred work elsewhere. Route device IRQ threads deliberately, assign their priorities relative to consumers, and include arrival bursts and handler execution in analysis.

Nonmaskable interrupts and firmware system-management activity may sit outside ordinary scheduler control. Hardware latency detectors can reveal some such interference, but the platform must provide a defensible bound or be excluded from hard real-time claims.

### Engineer CPU isolation as a system

Affinity and CPU isolation reduce migrations and unrelated work. Partition deadline tasks, their IRQ threads and required kernel workers onto understood CPUs. Keep explicit housekeeping CPUs for timers, RCU callbacks, unbound work, logging and management.

Isolation flags differ in scope and kernel version. Verify effective run queues, interrupts, tick behavior, workqueues and callbacks after boot. A nominally isolated CPU is not proof that no other work executes there.

### Control memory latency

Page faults, copy-on-write, allocation, reclaim, compaction and swap can create long or state-dependent delays. Lock required memory when appropriate, prefault stacks and data, preallocate bounded pools, and avoid general-purpose allocation in critical windows.

Memory locking consumes scarce resident capacity and does not preload every future path automatically. Test stack growth, executable pages, shared libraries and error paths. Bound cache and memory-controller interference from other cores and devices.

### Control device and I/O latency

Device queues, DMA, firmware, buses, filesystem locks and error recovery lie outside pure CPU schedulability. Use bounded interfaces and dedicated queues where available. Define timeout, cancellation and stale-result behavior.

Asynchronous I/O does not eliminate latency; it changes which job waits or completes it. Include completion interrupts, driver workers and downstream actuator time in the end-to-end contract.

### Avoid clock and release drift

Use an appropriate monotonic clock for intervals. Repeated relative sleeps accumulate execution and wakeup delays because each next release is based on the late prior wakeup.

Absolute sleeps target a release sequence and expose overruns without accumulating phase drift. Handle interrupted sleeps and clock semantics explicitly. Wall-clock adjustments must not silently change control timing.

### Design multicore placement deliberately

Partitioned scheduling assigns tasks to processors and simplifies some analysis at the cost of bin-packing and limited migration. Global scheduling can use capacity flexibly but adds migration, cache and run-queue effects.

Shared last-level cache, memory controllers, interconnect, thermal limits and global locks couple apparently separate CPUs. State whether those effects are bounded, controlled through partitioning, or treated as an unsupported source of hard guarantees.

### Make overload behavior explicit

Overload occurs when actual demand or arrivals exceed the admitted model. A good design detects budget overruns and deadline misses, preserves critical control and observability, sheds optional work, and leaves recovery authority runnable.

Do not rely on priority alone: a high-priority runaway may block the monitor that would stop it. Use reservations, group bandwidth, watchdogs and out-of-band controls with tested safe-state transitions.

### Preserve administrative recovery bandwidth

Linux real-time bandwidth controls can reserve time for non-real-time work globally and within control groups. This prevents indefinitely runnable real-time work from consuming every cycle, but incorrect period/runtime settings can cause unexpected throttling or starvation.

Treat the recovery reserve as part of the safety case. Test access, telemetry, termination and rollback during deliberate runaway and interrupt-storm conditions.

### Handle mixed criticality

Mixed-criticality systems may admit optimistic budgets for normal operation and switch modes when a high-criticality task approaches its certified bound. The switch reduces or suspends lower-criticality services to preserve essential deadlines.

Mode changes need explicit triggers, hysteresis, state transfer and restoration rules. They cannot invent processor capacity after every high-criticality task simultaneously overruns its assured bound.

### Include virtualization layers

A guest's real-time thread competes first inside the guest and then through the host's vCPU scheduler. Host preemption, steal time, emulator threads, virtual interrupts, device backends and live migration can invalidate guest-only analysis.

Pin and reserve vCPUs, host threads, interrupts and memory together; avoid overcommit for hard guarantees; and include hypervisor and firmware versions in the platform identity. Measure both guest-visible and host-side latency.

### Reconcile timing with energy and thermal policy

Deep idle states, frequency selection and package wakeup can add latency. Disabling them may increase heat enough to trigger throttling, reducing execution capacity. Turbo behavior can make a measured fast path nondeterministic across core counts and temperatures.

Specify supported power, frequency, cooling and ambient states. Validate worst supported thermal equilibrium, not only a cold benchmark. OS-098 develops these energy-management trade-offs further.

### Observe the full latency path

Measure event timestamp, interrupt arrival, wakeup, runnable-to-running delay, execution segments, blocking, preemption, completion and downstream effect. Correlate clocks and preserve lost-event indicators.

Scheduler traces, `osnoise`, `timerlat`, hardware-latency detection and controlled cyclic workloads reveal different components. Tracing itself adds load and can perturb timing, so compare instrumented and low-instrumentation runs.

### Distinguish evidence from proof

A long stress run increases confidence that assumptions hold in tested states; it does not establish a mathematical upper bound. Analysis can prove a conditional result; it cannot prove incorrect WCET or hardware assumptions true.

Combine static reasoning, measurement, vendor evidence, fault injection and conservative margin. Record every residual unbounded component and downgrade the guarantee when the evidence supports only statistical latency.

### Govern real-time authority

Changing real-time policy, priority, affinity or reservation can deny service to the system. Grant the minimum capability to a narrow launcher or supervisor, constrain values by policy, and audit requested and effective settings.

Version task models with binaries, kernel, firmware and hardware. Re-run admission and timing validation after code, compiler, dependency, topology, power, device or kernel changes.

## Definitions and Notation

- `r_i`: release time of a job of task `i`.
- `C_i`: bounded processor execution demand of one job.
- `D_i`: relative deadline from release to required completion.
- `T_i`: period or minimum interarrival time.
- `J_i`: bound on release jitter.
- `B_i`: bound on lower-priority blocking or modeled nonpreemptive delay.
- `R_i`: worst-case response-time bound under the stated model.
- `hp(i)`: tasks assigned a higher fixed priority than task `i`.
- `U_i = C_i/T_i`: task utilization in a simple periodic or sporadic model.
- **absolute deadline:** `r_i + D_i` for a particular job.
- **critical instant:** release pattern that produces the modeled worst response under specified assumptions.
- **budget overrun:** execution beyond the admitted or configured runtime.
- **deadline miss:** useful completion after the required absolute deadline.
- **temporal isolation:** containment of one activity's processor demand so it cannot arbitrarily consume another's entitlement.
- **scheduler latency:** delay from a task becoming runnable until it begins or resumes execution.
- **end-to-end latency:** time from the originating event to the required external effect.

## Mechanisms, Invariants, or Proof Structure

1. **Requirement claim:** define the event, result, deadline, criticality and miss consequence.
2. **Task decomposition:** map the causal path into jobs, dependencies, processors, devices and kernel work.
3. **Arrival claim:** bound periods, minimum interarrival, bursts and release jitter.
4. **Demand claim:** justify WCET or reservation runtime for every path and supported platform state.
5. **Resource claim:** enumerate locks, nonpreemptive sections, memory, I/O and shared hardware.
6. **Policy claim:** choose priorities, deadlines, reservations, affinities and IRQ placement consistently.
7. **Blocking claim:** apply inheritance or ceiling rules and calculate the maximum permitted blocking.
8. **Schedulability claim:** use response-time, demand-bound or another model-compatible test.
9. **Admission invariant:** reject any configuration that invalidates aggregate demand or domain constraints.
10. **Enforcement invariant:** throttle, shed or transition modes when demand exceeds its admitted envelope.
11. **Platform invariant:** constrain firmware, power, thermal, topology, virtualization and kernel configuration.
12. **Recovery invariant:** preserve watchdog, telemetry and administrative execution under runaway load.
13. **Observation claim:** instrument every latency component and record loss and observer effects.
14. **Change invariant:** bind evidence to exact builds and revalidate when any modeled input changes.
15. **Residual-risk claim:** identify components supported only statistically and state the resulting guarantee class.

## Alternatives and Trade-Offs

- **Fixed priority versus EDF:** fixed priorities simplify operational inspection and some certification arguments; EDF adapts order to deadlines and can use a uniprocessor efficiently under compatible assumptions.
- **FIFO versus round-robin:** FIFO avoids equal-priority quantum rotation; round-robin prevents one equal-priority runnable thread from holding that level indefinitely.
- **Priority policy versus reservation:** priority decides precedence; reservation constrains temporal consumption and requires bandwidth parameters.
- **Partitioned versus global multicore scheduling:** partitioning limits migrations and analysis scope; global policies improve capacity sharing and add interference.
- **Priority inheritance versus priority ceiling:** inheritance reacts to ownership chains; ceilings require resource knowledge and can provide tighter blocking properties.
- **Dedicated CPUs versus shared CPUs:** dedication limits scheduler interference; sharing improves utilization and expands the demand model.
- **Busy waiting versus blocking:** busy waiting can avoid wakeup cost for very short waits; it consumes budget, power and capacity continuously.
- **Relative versus absolute sleep:** relative intervals are simple but drift; absolute releases preserve phase and expose overruns.
- **Locked memory versus pageable memory:** locking removes fault/reclaim paths for resident pages; it raises capacity and operational risks.
- **Deep idle versus shallow idle:** deep states save more energy; exit latency and timing variability grow.
- **Maximum frequency versus deterministic frequency:** maximum can reduce nominal execution; fixed supported states may make bounds easier to defend.
- **Broad tracing versus narrow probes:** broad traces reveal interactions; they add overhead, data loss risk and analytical noise.
- **Hard guarantee versus statistical objective:** a hard claim requires defensible bounds; a statistical objective can use distributions but must admit tail risk.
- **Fail-safe shutdown versus degraded operation:** shutdown minimizes exposure after invalidation; degradation may preserve essential service with a more complex proof.
- **Host virtualization versus bare metal:** virtualization improves consolidation and isolation management; it adds another scheduler and device path.

## Failure Modes and Misconceptions

1. **“Real-time means fast.”** It means meeting a timing contract; a slow bounded task can be real-time.
2. **“High priority guarantees the deadline.”** demand, blocking and higher-priority interference can still make it miss.
3. **“`SCHED_FIFO` reserves CPU.”** it defines precedence, not a runtime reservation.
4. **“Round-robin is fair across priorities.”** its quantum applies among equal-priority runnable threads.
5. **“Utilization below 100 percent proves feasibility.”** deadlines, bursts, jitter and blocking can still fail.
6. **“The largest measured execution is WCET.”** untested paths and platform states remain.
7. **“Average latency is enough for a hard deadline.”** rare misses determine correctness.
8. **“Wakeup latency equals response time.”** execution, blocking, preemption and device completion remain.
9. **“Priority inheritance eliminates blocking.”** it bounds some inversion only when holders and critical sections are bounded.
10. **“PREEMPT_RT makes every kernel path preemptible.”** raw, NMI, firmware and architecture regions remain.
11. **“Threaded IRQs are free.”** they need CPU time, priority, placement and arrival bounds.
12. **“An isolated CPU runs only my task.”** ticks, IRQs, workqueues and callbacks require verification.
13. **“Memory locking prevents all faults.”** unmapped, copy-on-write, stack and later-loaded pages can still fault.
14. **“Asynchronous I/O removes I/O from the deadline.”** completion remains on the causal path.
15. **“Relative sleeps preserve a periodic phase.”** lateness accumulates into drift.
16. **“Migration always improves response.”** cache loss and shared-domain contention can dominate.
17. **“Deadline admission includes every source automatically.”** unmodeled IRQ and kernel demand can remain.
18. **“Throttling is a scheduler bug.”** it may be the configured containment behavior after budget use.
19. **“Give all important work maximum priority.”** equal priorities erase ordering and can starve recovery.
20. **“Disable all housekeeping on real-time CPUs.”** required kernel work must execute somewhere.
21. **“A quiet stress test proves a bound.”** finite observation cannot establish an unseen maximum.
22. **“Virtual CPUs are dedicated CPUs.”** the host can preempt them unless the whole stack is reserved.
23. **“Disabling power saving can only improve timing.”** heat and throttling can reduce capacity.
24. **“Overload policy is unnecessary after admission.”** assumptions fail through faults, bursts and overruns.
25. **“A missed deadline can always be retried.”** a late result may be unsafe or stale.
26. **“Real-time configuration is harmless tuning.”** it can deny service and requires privileged governance.

## Worked Examples

### Example 1

A camera pipeline requires a frame every 20 milliseconds but can discard an occasional late frame. It is soft or firm according to downstream semantics, not hard merely because the period is short.

### Example 2

A protection relay must open a circuit within a bounded interval after a fault. The analysis starts at sensor-visible fault detection and ends at actuator effect; scheduling only the decision thread covers too little.

### Example 3

A FIFO task runs an unexpected infinite loop. Higher-priority tasks may preempt it, but ordinary logging and recovery at lower priority starve. A reservation and protected recovery budget contain the failure.

### Example 4

A low-priority telemetry thread holds a mutex needed by a control thread. Medium-priority compression prevents release. Priority inheritance boosts the holder, and a measured maximum critical section supplies `B_i`.

### Example 5

Three tasks have aggregate utilization `0.65`, yet the team still performs response-time analysis because blocking and deadline placement matter. The calculation in Answer 2 converges within every deadline.

### Example 6

A periodic loop sleeps 10 milliseconds after completing each iteration. Its two-millisecond execution makes releases drift. Switching to absolute monotonic release times retains phase and exposes missed periods.

### Example 7

An IRQ is moved away from an isolated CPU, but its driver completion worker remains on an unbound workqueue there. Trace evidence contradicts the isolation assumption and leads to an explicit housekeeping mask.

### Example 8

A task passes tests after memory locking but faults when a rare error handler grows the stack. Prefaulting representative stack depth and preallocating its report buffer close the specific path.

### Example 9

A guest control loop shows a 12-millisecond pause although guest run queues are empty. Host tracing reveals vCPU descheduling behind a backup job, so guest-only priority changes cannot repair it.

### Example 10

Disabling deep idle reduces wakeup tails in a cold test, but continuous load heats the package until frequency throttles and WCET grows. The supported policy is validated at thermal equilibrium with reserved margin.

## Cross-Program Connections

- **Computer architecture:** caches, interconnects, timers, interrupts, idle states and firmware define platform latency.
- **Algorithms:** EDF, response-time recurrence and demand analysis turn task assumptions into feasibility claims.
- **Concurrency:** mutex ownership, priority inheritance, ceilings and nonpreemptive sections determine blocking.
- **Systems engineering:** requirement traceability and assurance connect a deadline to an external safe outcome.
- **Embedded engineering:** sensors, actuators, buses and control loops define end-to-end timing.
- **Performance engineering:** tracing separates release, runnable, blocked, execution and completion latency.
- **Platform engineering:** cgroups, affinity, fleet configuration and rollback operationalize reservations.
- **Security engineering:** real-time privilege, denial of service and recovery capacity require policy controls.
- **Virtualization:** vCPU and host scheduling compose into a two-level temporal resource model.
- **Energy engineering:** power and thermal states trade energy against wakeup and execution bounds.

## References

1. Linux Kernel Documentation, [Deadline Task Scheduling](https://docs.kernel.org/scheduler/sched-deadline.html), EDF, constant-bandwidth servers, runtime/deadline/period parameters and admission; retrieved 2026-09-04.
2. Linux Kernel Documentation, [Real-Time Group Scheduling](https://docs.kernel.org/scheduler/sched-rt-group.html), global and control-group real-time bandwidth limits; retrieved 2026-09-04.
3. Linux Kernel Documentation, [Theory of Operation for PREEMPT_RT](https://docs.kernel.org/core-api/real-time/theory.html), preemptibility, sleeping spin locks, priority inheritance and threaded interrupts; retrieved 2026-09-04.
4. Linux Kernel Documentation, [How Realtime Kernels Differ](https://docs.kernel.org/core-api/real-time/differences.html), interrupt, locking, timer and per-CPU behavior under PREEMPT_RT; retrieved 2026-09-04.
5. Linux man-pages, [sched(7)](https://man7.org/linux/man-pages/man7/sched.7.html), FIFO, round-robin, deadline and privilege semantics; retrieved 2026-09-04.
6. Linux man-pages, [sched_setattr(2)](https://man7.org/linux/man-pages/man2/sched_setattr.2.html), deadline attributes, flags, admission errors and runtime updates; retrieved 2026-09-04.
7. Linux man-pages, [clock_nanosleep(2)](https://man7.org/linux/man-pages/man2/clock_nanosleep.2.html), monotonic clocks, absolute sleeps and interruption; retrieved 2026-09-04.
8. Linux Kernel Documentation, [OS Noise Tracer](https://docs.kernel.org/trace/osnoise-tracer.html), measurement of operating-system interference on CPUs; retrieved 2026-09-04.
9. Linux Kernel Documentation, [Timerlat Tracer](https://docs.kernel.org/trace/timerlat-tracer.html), timer IRQ and thread wakeup-latency observation; retrieved 2026-09-04.
10. Linux Kernel Documentation, [Hardware Latency Detector](https://docs.kernel.org/trace/hwlat_detector.html), detection of latency outside normal kernel control; retrieved 2026-09-04.
11. Linux Kernel Documentation, [RT-mutex Implementation Design](https://docs.kernel.org/locking/rt-mutex-design.html), priority inheritance, waiter ordering and ownership chains; retrieved 2026-09-04.

## Exercises

### Exercise 1

Classify an autonomous braking deadline, a live-video frame deadline and a market-data refresh deadline as hard, firm or soft. State the consequence of lateness and the end-to-end completion point for each.

### Exercise 2

For three fixed-priority sporadic tasks in priority order, use `(C,T,D,B)` values `A=(1,4,4,0)`, `B=(1,5,5,0)` and `C=(2,10,10,1)`. Calculate utilization and response-time bounds under the module's recurrence.

### Exercise 3

Design CPU, IRQ, kernel-worker and housekeeping placement for a four-core controller with two deadline tasks, one device IRQ path, logging and remote recovery. State what must be measured after boot.

### Exercise 4

A deadline workload passes a one-hour cyclic test but occasionally faults pages, shares a mutex with telemetry and runs in a virtual machine. Construct an evidence plan that separates measured behavior from defensible bounds.

### Exercise 5

Define admission, overrun and recovery policy for a service using deadline reservations. Include group bandwidth, criticality, observability, rollback and behavior when actual execution exceeds its runtime.

## Answers to the Exercises

### Answer 1

Autonomous braking is hard when late actuation violates the safety envelope. Its interval begins at the defined sensor or fused-event release and ends when the actuator has produced the required braking effect, not when software queues a command.

A live-video frame is commonly firm: after its display deadline the frame is discarded because showing stale content has no value, while an occasional controlled drop is acceptable. Completion is successful delivery into the display pipeline before presentation cutoff.

A market-data refresh is often soft when utility decays with age and later data supersedes it, but a regulated trading decision might impose a firm rejection boundary. Completion must be defined at the consuming model or trading gate. Domain consequence, not application name, determines the class.

### Answer 2

Total utilization is `1/4 + 1/5 + 2/10 = 0.65`. Response-time iteration gives `R_A=1`; `R_B` starts at 1 and converges to 2 after interference from A; `R_C` starts at `C+B=3`, then takes values 5, 6, 7 and 7 after higher-priority interference. Every bound is within its deadline.

<!-- bijux-verify: {"id":"fixed-priority-response-time","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"A response=1 deadline=4 schedulable=true\nB response=2 deadline=5 schedulable=true\nC response=7 deadline=10 schedulable=true\nutilization=0.650\n"}} -->
```python
from math import ceil

tasks = [
    {"name": "A", "execution": 1, "period": 4, "deadline": 4, "blocking": 0},
    {"name": "B", "execution": 1, "period": 5, "deadline": 5, "blocking": 0},
    {"name": "C", "execution": 2, "period": 10, "deadline": 10, "blocking": 1},
]

for index, task in enumerate(tasks):
    response = task["execution"] + task["blocking"]
    while True:
        interference = sum(
            ceil(response / higher["period"]) * higher["execution"]
            for higher in tasks[:index]
        )
        candidate = task["execution"] + task["blocking"] + interference
        if candidate == response or candidate > task["deadline"]:
            response = candidate
            break
        response = candidate
    schedulable = response <= task["deadline"]
    print(
        f'{task["name"]} response={response} deadline={task["deadline"]} '
        f'schedulable={str(schedulable).lower()}'
    )

utilization = sum(task["execution"] / task["period"] for task in tasks)
print(f"utilization={utilization:.3f}")
```

The calculation assumes one fully preemptive processor, independent sporadic tasks, the displayed fixed-priority order, zero release jitter, no self-suspension, valid execution bounds and at most the stated blocking. It excludes interrupts and other kernel work unless already incorporated. Violating any assumption invalidates the conclusion.

### Answer 3

Assign each deadline task to an analyzed CPU or compatible shared domain. Place the device's threaded IRQ at a priority and affinity that lets it release and serve its consumer within the end-to-end bound. Put unbound workqueues, logging, RCU callbacks, ordinary timers and remote administration on explicit housekeeping CPUs, reserving enough capacity for recovery. Keep one management path independent of a runaway real-time task.

After boot, inspect effective affinities, IRQ routing, scheduler class and priority, reservations, cgroup limits, tick behavior, timers, kernel threads, workqueues and RCU placement. Trace release-to-completion under interrupt bursts, logging pressure, recovery access, thermal equilibrium and deliberate overruns. Record unexpected execution on isolated CPUs and lost trace events.

### Answer 4

First define releases, deadlines and end-to-end completion. Measure execution segments, page faults, mutex waits, IRQ latency, runnable delay, vCPU steal and host scheduling concurrently. The one-hour maximum remains a sample, not a bound.

Prefault and lock the finite required memory set, then test error paths and stack growth. Inventory the telemetry critical section, apply a compatible inheritance or ceiling protocol, and justify its longest hold time. At the host, pin and reserve vCPU, emulator, device backend, interrupts and memory; eliminate overcommit for a hard claim. Combine repeated worst-state measurement with code-path analysis, vendor platform evidence and margin. Any firmware or hypervisor interval without a defensible upper bound downgrades the claim to statistical timing.

### Answer 5

Represent every task with runtime, deadline, period, CPU domain, criticality and group. Validate the aggregate task set plus IRQ, kernel and recovery demand before applying it, and reject a change that exceeds either deadline admission or hierarchical bandwidth. Apply the configuration transactionally and verify effective kernel state.

On runtime depletion, throttle the offending task according to reservation semantics, record an overrun separately from a deadline miss, and preserve high-criticality work. Repeated or safety-relevant overruns trigger a defined degraded mode or safe state; optional work is shed first. Reserve non-real-time bandwidth for telemetry and authenticated rollback. A watchdog outside the exhausted reservation can terminate or isolate a runaway. Version the admission input with binaries and platform state, and revalidate after any timing-relevant change.
