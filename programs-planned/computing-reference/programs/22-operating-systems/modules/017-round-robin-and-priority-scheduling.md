---
module_id: OS-017
program: Operating Systems
level: 1
module_number: 17
title: Round-Robin and Priority Scheduling
status: complete
last_verified: 2026-09-04
---

# Round-Robin and Priority Scheduling

## One-Page Review

### Governing question

How do time quanta and priorities turn a runnable set into repeatable processor allocations without mistaking responsiveness for fairness or precedence for guaranteed capacity?

### Essential definitions

- **round-robin (RR)** gives each runnable peer at one priority a bounded quantum, then normally moves an unfinished peer behind its equals.
- A **quantum** or time slice is the maximum continuous processor service granted by the policy before reconsideration, subject to blocking and higher-priority preemption.
- **fixed-priority scheduling** chooses an eligible task from the highest-priority nonempty class.
- **preemption** removes a running task so a preferred runnable task can execute.
- **starvation** is unbounded postponement of eligible work under allowed arrivals and policy behavior.
- **priority inversion** occurs when higher-priority work is delayed, directly or transitively, by lower-priority work holding a needed resource.
- **priority inheritance** temporarily propagates urgency through a blocking chain; a **priority ceiling** constrains acquisition using predeclared resource ceilings.
- **aging** increases preference as waiting accumulates to constrain starvation.

### Central model, mechanism, or theorem

Maintain one FIFO queue `Q_p` for each priority `p`. Choose the head of the highest-priority nonempty queue. Run it until it blocks, finishes, is preempted by higher priority, or consumes quantum `q`. After quantum expiration, enqueue an unfinished task at the tail of `Q_p`.

This mechanism provides rotation among continuously runnable peers only under stated queue, arrival, and accounting rules. It does not guarantee service while higher-priority demand can saturate the processor. Priority inversion requires resource-protocol analysis; changing dispatch order alone does not release a lock.

### Critical invariants

- Every runnable task occupies exactly one eligible queue or one running slot, never both.
- Selection always uses the policy's highest eligible class and documented peer order.
- Runtime charging and quantum expiration use a declared clock, scope, and interruption policy.
- Blocking removes a task before it can be selected; wakeup enqueues it once according to defined placement rules.
- Priority changes atomically remove and reinsert affected runnable tasks or update the running task consistently.
- Inherited priority is the maximum required donation under the resource graph and is removed when the relevant dependency ends.
- Admission, throttling, and privilege limits prevent real-time priority from silently consuming unbounded system capacity.

### Common failures

Common mistakes are calling RR inherently fair, assuming a short quantum always improves response, letting timer accounting drift, resetting a slice on every interruption, inserting wakeups strategically at the head, starving low priorities, using nice values as fixed real-time priorities, raising a lock holder without propagating a chain, leaking inherited priority after unlock, applying inheritance to CPU overload, omitting interrupt and kernel-thread interference, and using an average benchmark as a deadline proof.

### Compact example

Tasks A and B have priority 2 and require 5 and 3 units; C has priority 1 and requires 2. With all arriving at zero and `q=2`, the schedule is `A2, B2, A2, B1, A1, C2`. B completes at 7, A at 8, and C at 10. RR rotates A and B, but C receives nothing until the higher class drains. If priority-2 arrivals continue at sufficient demand, C can starve.

### Connections

[OS-015](015-process-states-and-wait-queues.md) defines runnable transitions, [OS-016](016-scheduling-objectives.md) defines metrics, and [OS-018](../ROADMAP.md) adds feedback. [OS-021](../ROADMAP.md) and [OS-022](../ROADMAP.md) develop the locks and blocking protocols that create inversion.

## Governing Question

Round-robin appears simple: place runnable tasks in a circle and give each a turn. Priority scheduling also appears simple: run the most important task. Their combination is where semantics matter. Which events consume a quantum? Where does a woken task enter? Does a higher priority preempt immediately? What happens when a high-priority task waits for a low-priority lock owner?

These choices determine latency, throughput, starvation, and susceptibility to gaming. The same numeric “priority” can mean real-time precedence, a proportional-share hint, an application label, or a control-group weight. The same quantum can be wall time, actual runtime, or a policy-specific virtual amount.

The governing question is therefore how to state queue order, preemption, accounting, blocking, priority mutation, overload, and resource dependencies precisely enough to predict every allowed transition.

## Why This Matters

RR provides understandable sharing for peers and bounds uninterrupted service when timer preemption works. Priority distinguishes urgent from deferrable work. These ideas underpin interactive systems, media, network processing, embedded controllers, and real-time policies.

They also create sharp failure modes. High-priority CPU-bound demand can starve all lower work. A low-priority lock holder can delay a critical task while medium tasks preempt it. Too-short quanta amplify context-switch and cache costs; too-long quanta hurt response. Unprivileged priority controls can become denial-of-service capabilities.

Production systems layer group bandwidth, runtime limits, affinity, hierarchy, and privilege over per-task policy. Correct evaluation must include those layers rather than treating textbook queues as the whole machine.

## Prerequisites and Retrieval

Recall state and wake rules from [OS-015](015-process-states-and-wait-queues.md), objective conflicts from [OS-016](016-scheduling-objectives.md), and direct and indirect switch cost from [OS-014](014-context-switching.md). Understand FIFO queues, locks, timers, and response-time metrics.

Retrieve these distinctions:

- priority orders eligible contenders; reservation supplies capacity under assumptions;
- RR rotates peers in one class; it does not allocate across unequal classes;
- a timer interrupt creates a scheduling opportunity, not necessarily a switch;
- wall-clock time, executing runtime, and charged budget can differ;
- priority inversion is blocking through resources, not merely a lower-priority task running earlier;
- inheritance mitigates bounded resource blocking, not processor overload;
- observed dispatch latency is not a proven worst-case bound.

## Learning Objectives

After this module, you should be able to:

1. simulate RR, fixed-priority FIFO, and fixed-priority RR schedules;
2. define quantum expiration, peer ordering, wake placement, and preemption rules;
3. analyze response, completion, starvation, and switch-frequency trade-offs;
4. distinguish nice, static priority, relative weight, quota, and real-time bandwidth;
5. construct priority-inversion chains and evaluate inheritance and ceiling protocols;
6. identify admission, privilege, timer, accounting, multicore, and teardown hazards;
7. design empirical tests without claiming universal performance or deadline assurance.

## Core Exposition

### Pure round-robin

One FIFO runnable queue holds peers. The scheduler removes the head, runs it for at most `q`, and appends it if unfinished and still runnable. A task that blocks leaves the queue; a wake rule determines where it returns. A task that finishes consumes no further turns.

If `n` peers remain continuously runnable on one CPU and dispatch overhead is ignored, a task receives at most `q` before rotation and waits roughly `(n-1)q` between turns. This is an illustrative bound only when arrivals, interrupts, higher classes, nonpreemptive regions, and overhead are constrained.

### Quantum selection

A shorter quantum increases scheduling opportunities and may reduce peer response. It also increases switches, cache disruption, timer activity, and scheduler overhead. A longer quantum amortizes those costs but approaches FIFO behavior for short observations.

Quantum accounting must say whether interrupt time, stolen virtual-machine time, throttling, migration, and kernel work count. Resetting a quantum after every wake or preemption can reward strategic blocking. Carrying all remainder can penalize legitimate I/O. The policy must choose and expose its semantics.

### Fixed-priority FIFO and RR

In fixed-priority FIFO, a task normally runs until it blocks, yields, finishes, or a higher priority preempts it. Same-priority peers do not rotate solely because time passes. In fixed-priority RR, peers rotate on quantum expiration. Both immediately prefer higher eligible priority under their preemption rules.

Numeric direction and ranges are API-specific. Linux real-time static priorities are distinct from normal-policy nice values. Portable code queries supported bounds and treats permission, reset-on-fork, resource-limit, and policy semantics explicitly.

### Arrival and wake placement

Tail insertion gives existing peers precedence within a FIFO class. Head insertion can improve wake response but starve queued peers if a task blocks and wakes frequently. Some policies preserve remaining quantum; others replenish. These are observable policy rules, not implementation trivia.

Simultaneous events need an order: quantum expiration, wakeup, priority change, CPU hotplug, and cancellation may coincide. A deterministic model defines event ordering; a production kernel protects transitions under run-queue synchronization.

### Starvation and aging

Strict priority permits starvation whenever higher-priority demand can keep the processor busy. Aging gradually elevates waiting work. Periodic boosts reset classes. Reserved bandwidth guarantees a minimum service supply. Each changes the original priority meaning.

Aging needs rate, cap, reset, and hierarchy rules. Too aggressive a rate erases urgency; too slow a rate fails the requirement. Starvation tests must include adversarial continuing arrivals, not only a finite batch that eventually drains.

### Priority inversion

Let high task H need mutex M held by low task L. If medium task N preempts L, H waits indirectly for N even though N does not use M. This is priority inversion. The blocking duration depends on L's critical section, nested locks, preemption, interrupts, and resource graph.

Priority inheritance raises L to H's effective priority while H depends on it. If L blocks on a mutex held by another task, donation must propagate through the chain. When L releases M, it removes only donations associated with dependencies that ended and recomputes its effective priority.

### Priority ceilings

A ceiling protocol assigns each resource a priority related to potential users and restricts acquisition or elevates holders according to the chosen protocol. It can bound blocking and prevent selected deadlock patterns when the resource graph and ceilings are correct.

Ceilings require known resource use and disciplined locking. Dynamic resources and callbacks complicate analysis. Neither ceiling nor inheritance supplies CPU when admitted high-priority demand itself exceeds capacity.

### Linux policy distinctions

Linux documents normal, batch, idle, FIFO, RR, and deadline-related policies with different attributes. `sched_rr_get_interval` reports the RR quantum for a task under applicable policy. `sched_get_priority_min` and `max` report supported static-priority ranges. `pthread_setschedparam` configures a thread subject to permissions and attributes.

Nice values affect normal scheduling rather than becoming FIFO or RR real-time priority. Resource limits and capabilities constrain priority and CPU use. Real-time group bandwidth and cgroup controls add hierarchy and throttling. Version, configuration, namespace, and privilege matter.

### Overload and containment

Without containment, a runaway highest-priority task can monopolize a CPU and prevent recovery, logging, or administrative work. Runtime limits, group bandwidth, watchdogs, admission, reserved control capacity, and safe-mode transitions are possible defenses.

Throttling changes guarantees: a task may be highest priority yet ineligible because its budget is exhausted. Diagnostics must expose both priority and throttled state. A system cannot promise unrestricted fixed-priority execution and simultaneous guaranteed service to lower work on the same finite CPU.

### Multicore scheduling

Per-CPU queues reduce contention but require placement and balancing. A high-priority task on one CPU may coexist with lower-priority work elsewhere because affinity, partitioning, migration state, or resource constraints prevent movement. “Highest priority runs” needs a scope.

Global priority scheduling can improve use of available CPUs but adds migration, shared run-queue, cache, and synchronization cost. Partitioned scheduling simplifies some analysis but depends on a feasible assignment and failure policy.

### Measurement

Record releases, enqueue, dispatch, preemption, block, wake, completion, quantum expiration, priority changes, donations, throttling, and migration. Measure response and completion by class, switch rates, CPU supply, starvation intervals, inversion duration, and deadline misses.

Vary quantum, runnable count, critical-section length, arrivals, affinity, topology, interrupts, tracing, and load. Preserve configuration and raw traces. Synthetic results demonstrate the modeled workload, not a universal best quantum.

### Security and assurance

Changing priority is an authority operation because it can deny service. Validate credentials, limits, delegation, inheritance across creation, and cleanup on exit. Shared-core placement can also be constrained by a security policy.

Real-time and safety claims require worst-case execution and blocking estimates, admission, timer and interrupt bounds, failure modes, and independent review. Passing examples and observed maxima are not certification.

## Definitions and Notation

Let `Q_p` be the FIFO queue at priority `p`, with larger `p` higher in this module's abstract model. Let quantum be `q > 0`. For task `i`, let base priority be `b_i`, effective priority `e_i`, remaining service `r_i`, and remaining slice `z_i`. Let `holds(i)` and `waits(i)` describe its resource edges.

Selection is `head(Q_max)` where `max` is the highest priority with a nonempty eligible queue. A donation edge `H -> L` exists when H waits for a resource held by L. A simple inheritance condition is `e_L >= e_H` while that dependency is active, recursively propagated through blocking chains.

Core properties include unique placement, highest-class selection, bounded slice accounting, atomic priority relocation, dependency-scoped donation, and capacity containment. These properties need architecture and kernel synchronization beneath the abstract queue model.

## Mechanisms, Invariants, or Proof Structure

A reviewable policy proof follows these obligations:

1. Define task states, queue ownership, priority order, peer order, and simultaneous-event rules.
2. Define the runtime clock, quantum debit, replenishment, preemption, yield, block, and wake semantics.
3. Prove every transition preserves unique running or queued placement.
4. Analyze finite and continuing arrivals for response, starvation, and gaming.
5. Trace resource dependencies, donation propagation, removal, deadlock, and maximum blocking.
6. Incorporate hierarchy, bandwidth, permissions, affinity, multicore capacity, and failure control.
7. Separate model arithmetic, implementation behavior, empirical evidence, and assurance.

The executable simulator applies strict priority between queues and RR within a priority.

<!-- bijux-verify: {"id":"toy-priority-round-robin","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"timeline=A:2,B:2,A:2,B:1,A:1,C:2\ncompletion=B:7,A:8,C:10\nlow-priority-first-run=8\n","stderr":""}} -->
```python
from collections import deque

remaining = {"A": 5, "B": 3, "C": 2}
queues = {2: deque(["A", "B"]), 1: deque(["C"])}
quantum = 2
now = 0
timeline = []
completion = []
first_run = {}

while any(queues.values()):
    priority = max(p for p, queue in queues.items() if queue)
    task = queues[priority].popleft()
    first_run.setdefault(task, now)
    used = min(quantum, remaining[task])
    remaining[task] -= used
    now += used
    timeline.append(f"{task}:{used}")
    if remaining[task]:
        queues[priority].append(task)
    else:
        completion.append(f"{task}:{now}")

print(f"timeline={','.join(timeline)}")
print(f"completion={','.join(completion)}")
print(f"low-priority-first-run={first_run['C']}")
```

The model assumes simultaneous arrivals, one CPU, exact service, no blocking, no overhead, no new jobs, and higher numeric priority. It demonstrates peer rotation and lower-class postponement, not a bound for a real scheduler.

## Alternatives and Trade-Offs

- Short quanta improve peer rotation but increase transfer and cache cost.
- Long quanta amortize overhead but approach FIFO response for peers.
- Strict priority preserves urgency ordering but permits starvation.
- Aging bounds some waiting but weakens static-priority meaning.
- Inheritance adapts to actual blocking but needs correct transitive donation and removal.
- Ceilings can bound blocking but require a known, accurate resource-use model.
- Head wake placement improves one task's response but permits queue jumping and gaming.
- Per-CPU queues scale well; global selection can use capacity more flexibly.
- Runtime throttling contains monopolization but can cause high-priority deadline misses.

## Failure Modes and Misconceptions

1. **“RR is fair.”** It rotates selected peers; cross-class and hierarchical fairness require more rules.
2. **“Quantum is wall time.”** Policies can charge actual runtime and treat interruptions differently.
3. **“Shorter always responds faster.”** Switch and cache overhead can consume useful service.
4. **“FIFO and RR differ only in name.”** Same-priority time-slice rotation is the key distinction.
5. **“A timer tick always switches tasks.”** Selection can retain the current task.
6. **“Highest priority always runs globally.”** Eligibility, affinity, CPU scope, throttling, and locks constrain it.
7. **“Nice is real-time priority.”** Normal-policy weighting and static RT priority are distinct.
8. **“Finite tests disprove starvation.”** Starvation needs continuing adversarial demand.
9. **“Inversion means any lower task ran.”** It is dependency-mediated delay.
10. **“Inheritance solves overload.”** Donation helps a resource holder; it creates no capacity.
11. **“One donation level is enough.”** Nested blocking requires transitive handling.
12. **“Unlock restores base priority.”** Other active donations may remain.
13. **“Pinning makes timing safe.”** Interrupts, locks, budgets, and shared hardware remain.
14. **“Maximum measured response is a bound.”** Coverage does not prove worst-case timing.

## Worked Examples

### Example 1

Three equal-priority tasks needing 5, 3, and 2 units rotate with `q=2`. The queue changes after every expiration, unfinished tasks rejoin the tail, and completion order differs from arrival order.

### Example 2

Add a priority-3 task at time 3. It preempts the current priority-2 task under immediate-preemption rules. Whether the interrupted task keeps its remaining slice must be explicitly defined.

### Example 3

A priority-1 maintenance task waits behind a continuous priority-2 stream. RR inside priority 2 does nothing for it. Aging, reserved capacity, or admission can address the starvation under different contracts.

### Example 4

An interactive task sleeps after one millisecond and wakes repeatedly. Always placing it at the head with a fresh slice lets it jump over CPU-bound peers. Carrying charge or using weighted virtual time limits gaming.

### Example 5

H blocks on mutex M held by L while medium N is runnable. N preempts L, extending H's wait. Inheritance raises L until it releases M; then N can run before L again.

### Example 6

L holds M1 and waits for M2 held by V. H's donation must flow H to L to V. When V releases M2, effective priorities are recomputed from remaining dependency edges rather than blindly reset.

### Example 7

A runaway FIFO task never blocks. A configured group runtime limit throttles it so recovery work can run. Its high priority remains, but it is temporarily ineligible; monitoring must report the throttle.

### Example 8

Two CPUs use partitioned queues. The highest-priority task is pinned to busy CPU 0 while lower work runs on CPU 1. This respects affinity but disproves an unscoped “highest priority always runs” claim.

### Example 9

A quantum benchmark reports lower mean response at one millisecond, but under memory pressure cache misses double and throughput falls. Report both distributions and work completed instead of selecting one metric.

### Example 10

A controller uses fixed priorities derived from hazard and response-time analysis, bounds critical sections, applies a reviewed inheritance protocol, reserves recovery capacity, and tests overload. Named owners still approve assumptions and residual risk.

## Cross-Program Connections

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops mutexes, condition variables, and priority inversion. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains timers, interrupts, caches, and multicore topology.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies requirements, overload, hazards, and assurance. [Security Engineering](../../25-security-engineering/ROADMAP.md) frames scheduling authority and denial of service.

Within this program, [OS-018](../ROADMAP.md) generalizes dynamic priority feedback, [OS-019](../ROADMAP.md) develops fair scheduling, [OS-020](../ROADMAP.md) treats real-time and multiprocessor scheduling, and [OS-022](../ROADMAP.md) deepens blocking primitives.

## References

- Linux man-pages project, [sched(7)](https://man7.org/linux/man-pages/man7/sched.7.html), current page checked 2026-09-04. Linux scheduling policies, static priorities, RR, FIFO, nice, reset-on-fork, limits, and privilege.
- Linux man-pages project, [sched_rr_get_interval(2)](https://man7.org/linux/man-pages/man2/sched_rr_get_interval.2.html), current page checked 2026-09-04. RR quantum retrieval, task scope, errors, and Linux notes.
- Linux man-pages project, [sched_get_priority_max(2)](https://man7.org/linux/man-pages/man2/sched_get_priority_max.2.html), current page checked 2026-09-04. Runtime discovery of policy-specific static-priority ranges.
- Linux man-pages project, [sched_setattr(2)](https://man7.org/linux/man-pages/man2/sched_setattr.2.html), current page checked 2026-09-04. Policy, priority, flags, utilization clamps, deadline parameters, privilege, and validation.
- Linux man-pages project, [getpriority(2) / setpriority(2)](https://man7.org/linux/man-pages/man2/setpriority.2.html), current page checked 2026-09-04. Nice values, scope, permissions, ranges, and Linux thread distinctions.
- Linux man-pages project, [getrlimit(2)](https://man7.org/linux/man-pages/man2/getrlimit.2.html), current page checked 2026-09-04. Real-time priority and CPU-time limits, signals, privilege, and inheritance.
- Linux man-pages project, [pthread_setschedparam(3)](https://man7.org/linux/man-pages/man3/pthread_setschedparam.3.html), current page checked 2026-09-04. Per-thread policy and parameters, priority, permissions, and errors.
- Linux man-pages project, [futex(2)](https://man7.org/linux/man-pages/man2/futex.2.html), current page checked 2026-09-04. Priority-inheritance operations, compare-and-block behavior, timeouts, and higher-level protocols.
- Linux Kernel documentation, [Real-Time Group Scheduling](https://docs.kernel.org/scheduler/sched-rt-group.html), current page checked 2026-09-04. Group runtime, period, bandwidth, interfaces, admission, and throttling.
- Linux Kernel documentation, [RT-mutex Implementation Design](https://docs.kernel.org/locking/rt-mutex-design.html), current page checked 2026-09-04. Priority inheritance, waiter trees, owner state, chain walking, and locking.
- Linux Kernel documentation, [CFS Scheduler](https://docs.kernel.org/scheduler/sched-design-CFS.html), current page checked 2026-09-04. Normal-task virtual runtime and distinction from array-based priority scheduling.
- Linux Kernel documentation, [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), current page checked 2026-09-04. CPU weight, max, burst, idle, partitions, hierarchy, and resource distribution.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching runnable queues, timer preemption, scheduler loops, locks, sleep, wakeup, and multiprocessor execution.

## Exercises

### Exercise 1

Simulate the compact example by hand. Add a priority-3 task D requiring one unit at time 3, state simultaneous-event rules, and recompute the timeline and completion times.

### Exercise 2

Compare quanta 1, 2, and 6 for three equal-priority tasks with services 5, 3, and 2. Compute response, completion, and switch count under a declared overhead-free model, then discuss indirect cost.

### Exercise 3

Construct a transitive priority-inheritance graph with three locks and four tasks. Trace effective priorities during acquisition, blocking, release, timeout, and cancellation.

### Exercise 4

Design a starvation and gaming test suite for fixed-priority RR, including continuing arrivals, sleep-wakeup behavior, priority changes, bandwidth throttling, affinity, and multicore placement.

### Exercise 5

Build an assurance review for a fixed-priority controller sharing kernel and device resources with best-effort work. Cover admission, blocking, timers, overload, privileges, evidence, and human judgment.

## Answers to the Exercises

### Answer 1

Choose the rule that arrivals at a boundary are processed before selecting the next task and preempt immediately. A runs from 0 to 2; B starts at 2. D arrives at 3, so B has used one unit and is preempted with two service units and one slice unit remaining. D runs 3 to 4 and completes. Resume policy must say whether B keeps its remainder; if it does, B runs 4 to 5, then A 5 to 7, B 7 to 8 and completes, A 8 to 10 and 10 to 11, then C 11 to 13.

Completion is D=4, B=8, A=11, C=13 for this declared rule. Resetting B's slice or appending it differently can change peer timing. The exercise demonstrates why a policy specification must settle boundary ordering and slice preservation.

### Answer 2

With initial A,B,C, quantum 1 gives first starts 0,1,2 and rotates until C completes at 6, B at 8, A at 10. Quantum 2 gives starts 0,2,4 and the timeline A2,B2,C2,A2,B1,A1, completing C=6, B=9, A=10. Quantum 6 behaves FIFO: starts 0,5,8 and completes A=5, B=8, C=10.

Ignoring the final dispatch, quantum 1 has the most task changes and best initial peer response; quantum 6 has the fewest and worst later-peer response. Real evaluation charges scheduler and switch time, cache and TLB recovery, timer behavior, workload blocking, and arrival distributions, so arithmetic alone cannot select a universal quantum.

### Answer 3

Let H at priority 90 wait for M1 held by L at 10; L waits for M2 held by V at 20; V waits for M3 held by W at 30. Donation propagates 90 through L, V, and W so W can finish the dependency chain ahead of unrelated medium work. On W releasing M3, remove the V-to-W edge and recompute W from its base and other waiters; V remains donated while it releases M2, then L remains donated until M1 is released.

If H times out, remove H's waiter edge and recompute every affected owner; do not leave priority 90 behind. Cancellation follows the same resource-safe removal and cleanup protocol. Cycles require deadlock detection or prevention rather than infinite chain walking. Actual protocols define waiter ordering, maximum depth, and synchronization.

### Answer 4

Generate a never-ending high-priority stream while measuring low-class service; a finite trace is insufficient. Vary arrival rate around capacity, task count, quanta, and service distributions. Add a task that repeatedly sleeps just before expiration and wakes at selection boundaries; compare fresh, preserved, and charged slice rules. Mutate priorities while queued and running, and verify unique placement.

Exercise runtime throttling and replenishment boundaries, restricted privileges, CPU affinity, migration, hotplug, and imbalanced per-CPU queues. Record releases, enqueue, dispatch, charge, preemption, wake, throttle, and completion. Assert both state invariants and metric outcomes; retain seeds and configuration. The suite still samples schedules and cannot prove absence of starvation for all executions.

### Answer 5

Derive base priorities from urgency and response-time analysis rather than labels. Validate execution demand, periods, deadlines, affinity, timer resolution, interrupt routing, nonpreemptive regions, every shared-resource chain, and transitive inheritance or ceiling behavior. Admission includes kernel threads, device callbacks, recovery work, and bandwidth limits.

Define overload, exhausted budget, runaway high priority, CPU loss, timer failure, device loss, missed deadline, and safe-state behavior. Restrict priority authority and preserve administrative recovery capacity. Combine analytical bounds with trace, stress, and fault evidence; observed maxima are not bounds. Named real-time, kernel, driver, concurrency, platform, security, safety, independent-verification, and acceptance owners review assumptions and residual risk. This chapter claims no certification.
