---
module_id: CONPAR-035
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 35
title: Cooperative Scheduling
status: complete
last_verified: 2026-08-29
---

# Cooperative Scheduling

## One-Page Review

### Governing question

When running work retains the processor until it yields, what contracts make responsiveness, fairness, cancellation, priority, and capacity reviewable rather than matters of task goodwill?

### Essential definitions

- **Cooperative scheduling** transfers execution at explicit yield, suspension, blocking, termination, or runtime-inserted cooperation points rather than arbitrary instruction-level preemption.
- A **runnable task** is eligible for processor service.
- A **dispatch** selects a runnable task; a **time slice/chunk** is its work before returning control.
- A **yield point** is a program/runtime boundary that gives the scheduler another selection opportunity.
- **Run to completion** means a callback/turn is not interleaved by another task on the same agent until it returns.
- **Fairness** constrains whether continuously eligible tasks eventually receive service.
- **Starvation** is unbounded denial of useful service despite continued system activity.
- **Scheduler latency** is time from becoming runnable to beginning service.
- **Blocking** occupies a worker while awaiting a condition; **suspension** releases it while retaining task state.
- A **cooperation budget** bounds work, time, operations, or instructions between scheduling opportunities.

### Central model, mechanism, or theorem

A cooperative task is a sequence of bounded service chunks separated by scheduler returns. A single-worker scheduler owns a run queue and chooses one ready task at each turn. If the ready set is finite, every chunk is bounded, dispatch is weakly fair, and no higher-priority source replenishes indefinitely, a continuously ready task eventually runs. Removing any premise can reintroduce starvation; an `await` is a fairness boundary only when its exact protocol actually returns control to an appropriate queue.

### Critical invariants

No task executes an unbounded non-yielding region on a shared worker. Yield type reaches the intended competing queue. Readiness is stored in task state, not inferred from wake count. Each runnable task is queued at most once. Cancellation and deadline are checked at bounded safe points. Partial state at each yield is valid or private. Locks and scarce permits are not retained across arbitrary yields without proof. Priority has an anti-starvation policy. Blocking work uses bounded dedicated capacity. Shutdown stops admission, wakes sleepers, drains/cancels owned tasks, and joins them.

### Common failures

A CPU loop never yields; a task yields only to a microtask queue that it continually replenishes; `sleep(0)` is treated as a portable fairness guarantee; ready tasks are enqueued repeatedly; polling spins without a wake source; long chunks violate latency while tiny chunks waste overhead; cancellation is checked only after all work; partial mutations become visible between chunks; one priority class monopolizes service; blocking I/O occupies every executor worker; or detached tasks survive shutdown.

### Compact example

Round-robin tasks A=5, B=3, C=1 work units with quantum 2 run as A2, B2, C1, A2, B1, A1. Completion order is C, B, A; no chunk exceeds two units. This proves the policy for a finite deterministic model, not wall-clock fairness: units may have unequal cost, arrivals may be unbounded, and a production executor may use priorities, work stealing, or preemption.

### Connections

[Async/Await State Machines](034-async-await-state-machines.md) explains suspension; [Event Loops and Nonblocking Execution](031-event-loops-and-nonblocking-execution.md) explains queue phases. The [program roadmap](../ROADMAP.md) next develops cancellation and timeouts.

## Governing Question

How should engineers design, quantify, implement, and test cooperative scheduling so every shared worker has bounded non-yielding work and every owned task has a defensible progress story?

Cooperation is a progress protocol, not a call to `yield` sprinkled through code.

## Why This Matters

Event loops, async executors, generators, green threads, embedded loops, actor turns, UI dispatchers, and simulation engines all depend on work returning control. Cooperative execution reduces involuntary interleavings and can make local invariants easier: within one turn, another task on that agent does not interrupt ordinary code.

The same property creates a liveness hazard. One callback can parse a hostile document, one future can spin, or one actor can drain an unbounded mailbox and deny all peers. A promise-returning function can still perform a long synchronous prefix. An await of already-ready data may not yield to timers, I/O, or lower-priority tasks.

Modern runtimes are often hybrid. OS threads are preempted; language tasks cooperate at awaits; an executor may apply poll budgets; a runtime may inject safepoints; work stealing moves runnable tasks. Classify the layer. Calling an entire system “cooperative” or “preemptive” loses the mechanism needed for correctness.

## Prerequisites and Retrieval

Retrieve:

- task and thread distinctions from [Processes, Threads, Tasks, and Fibers](002-processes-threads-tasks-and-fibers.md);
- liveness from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- deterministic traces from [Determinism and Reproducibility](007-determinism-and-reproducibility.md);
- workload decomposition from [Choosing a Concurrency Model from the Workload](010-choosing-a-concurrency-model-from-the-workload.md);
- event-loop phases from [Event Loops and Nonblocking Execution](031-event-loops-and-nonblocking-execution.md);
- future readiness from [Futures and Promises](033-futures-and-promises.md); and
- state-machine suspension from [Async/Await State Machines](034-async-await-state-machines.md).

Retrieval prompt: find the longest path between scheduler-return opportunities and name the competing queue that becomes eligible at the chosen yield.

## Learning Objectives

After completing this module, a learner can:

1. distinguish cooperative tasks, preempted threads, and hybrid runtime layers;
2. define runnable state, dispatch, yield, chunk, wakeup, and scheduler latency;
3. state sufficient assumptions for finite-delay progress without overclaiming fairness;
4. choose work-count and time budgets with measurement feedback;
5. explain why different yields serve different queues;
6. implement a deterministic round-robin scheduler model;
7. make partial progress and cancellation safe at every yield;
8. isolate blocking and CPU work with bounded ownership;
9. audit priority, wake coalescing, duplicate queueing, and shutdown; and
10. distinguish correctness evidence from empirical latency evidence.

## Core Exposition

### Classify the scheduling layer

An OS can preempt a runtime worker while the language task running on it remains cooperative relative to peer tasks. An async executor may poll a future until it returns pending/ready, but a runtime budget can force library operations to return pending periodically. An actor processes one message per turn yet workers are preemptively scheduled.

Record four facts: scheduling unit, authority that dispatches it, points where authority is returned, and processor/thread pool that executes it. Only then can “cannot be interrupted” or “may migrate” be meaningful.

### Task states and queue ownership

A useful state machine is NEW, RUNNABLE, RUNNING, WAITING, TERMINAL. Admission moves NEW to RUNNABLE and queues it. Dispatch atomically claims RUNNABLE to RUNNING. A yield makes it RUNNABLE and queues once; a wait records a wake source and becomes WAITING; completion becomes TERMINAL.

Wakeups change WAITING to RUNNABLE at most once. Repeated wake signals can coalesce; readiness data lives in synchronized task/operation state. Duplicate queue entries can poll one state machine concurrently or waste service, so schedulers use queued/running flags or atomic state transitions.

### Yield points define responsiveness

In a cooperative model, a task can delay peers for the duration of its current chunk. Suitable boundaries include awaiting incomplete I/O, returning from a callback, explicit scheduler yield, processing a bounded batch, or a runtime-inserted budget check.

Not every await yields. A ready future can continue in the same poll or schedule a high-priority reaction. Not every yield reaches the desired work. In browsers and JavaScript runtimes, recursively queued microtasks can delay ordinary task queues; a later-turn task source may be required. `sleep(0)`, thread yield, and platform scheduler APIs have implementation-specific semantics and weak fairness guarantees.

Name the queue/phase that should run and select a documented boundary that makes it eligible.

### Cooperation budgets

Budget can count records, bytes, loop iterations, VM reductions, polls, or elapsed time. Work count is deterministic but units may have variable cost. Time budgets track latency better but require clock reads and still cannot interrupt one expensive operation.

Choose an initial chunk from a responsiveness objective and measured upper-percentile unit cost, then validate under representative load. If a task should return within `B` milliseconds and conservative cost per item is `c`, an initial count is at most `floor(B/c)`, with safety margin. This estimate is empirical, not a proof about future hardware or inputs.

Check time periodically rather than every trivial instruction. Reject or separately handle a single item whose own worst case exceeds budget.

### Fairness assumptions and limits

Round robin is intuitively fair when the runnable set is finite and each dispatch consumes a bounded quantum. Yet finite waiting also assumes arrivals do not continually occupy privileged queues, tasks are not duplicated, the scheduler itself runs, and a unit of work terminates.

Weak fairness says a continuously enabled task eventually executes. Strong fairness addresses tasks enabled infinitely often but not continuously. Production APIs rarely promise these formal properties without qualifications. State the implemented queue policy and measure waiting distributions rather than labeling a runtime “fair.”

Work conservation—never idle when runnable work exists—improves utilization but does not imply fairness. A LIFO work queue can remain busy while starving an old task. FIFO reduces that risk but priority and affinity can override it.

### Round robin, weights, and deficit

Basic round robin appends a yielding task to the tail. A quantum bounds service per turn. Equal turns are not equal CPU time when tasks perform unequal-cost operations.

Weighted round robin gives a class more turns. Deficit round robin accumulates credits and subtracts actual work cost, helping variable-size jobs. Both require bounded cost accounting and protection against overflow or dishonest estimates. Completely fair scheduling approximates proportional service using virtual runtime, but adds data structures and policy.

Choose a policy by latency classes, throughput, tenant isolation, and predictability. The scheduler must not let a task select arbitrary priority without authorization.

### Priority and starvation

Priority is needed for latency-sensitive control work, but a continuously replenished high-priority queue can starve maintenance or cleanup. Mitigations include aging, quotas, bounded high-priority bursts, reserved capacity, deadlines, and admission control.

Priority inversion occurs when high-priority work waits for a resource held by low-priority work while medium-priority work consumes the scheduler. Priority inheritance can help lock-based systems, but async ownership and remote dependencies often need protocol redesign. Keep critical sections small and avoid holding scarce resources while yielding.

### Voluntary yield versus suspension

A voluntary yield remains runnable and requests another dispatch. Suspension becomes waiting until an event/wakeup. Polling a condition by yield repeatedly wastes turns; register a wake source and suspend. Conversely, suspending without a reliable wake path can lose progress forever.

Yield may be merely a hint. POSIX `sched_yield`, language thread yields, and zero-duration sleeps do not create portable ordering or fairness. For tests, inject a scheduler boundary you control instead of relying on wall-clock sleeps.

### Cooperative cancellation

Cancellation cannot interrupt arbitrary code between safe points unless another preemptive mechanism exists. Check the token/deadline before starting a chunk, within sufficiently long pure loops, after resumption, and before publishing partial results.

The maximum cancellation response includes the longest non-checking region plus scheduler delay and cleanup. If one cryptographic or compression call is uninterruptible for seconds, checking between calls does not meet a 50 ms objective.

At each check, leave state valid. Private candidate output can be discarded. Shared mutations need per-chunk commits, compensations, or an immutable snapshot swap. Frequent checks improve latency but do not make non-idempotent effects atomic.

### Blocking poisons cooperative pools

A blocking call does not return authority to the language scheduler. On one event-loop thread it stops every task. On an `m`-worker pool, `m` blocking tasks can stop all async progress, including events needed to unblock them.

Use nonblocking operations or a separately bounded blocking executor. Bound its queue and concurrency, propagate cancellation where the API supports it, observe late completions, and include it in shutdown. Offloading unbounded work simply moves overload to another queue.

CPU-bound work may be cooperatively chunked when state is safely divisible and responsiveness matters. For sustained throughput, use bounded parallel workers and retain cooperative points for cancellation/coordination.

### Wakeups and self-wake loops

A future returning pending must arrange a wake when progress may be possible. Unconditionally waking itself then returning pending keeps it runnable and can consume the executor. This is cooperative livelock: turns occur, but external progress does not.

Wake coalescing means a wake is not a work counter. Store actual pending items or readiness flags. A producer publishes state then wakes; a consumer checks state, registers the current waker under a race-safe protocol, and suspends only when a future wake remains possible.

### Work stealing and locality

Multi-worker cooperative executors may use local deques and steal tasks. Local execution improves cache locality; stealing balances load. Affinity, pinned tasks, non-transferable data, and actor isolation restrict movement. A task can be fairly queued globally yet delayed behind a long chunk on its chosen worker.

Evaluate per-worker run queues, steal attempts, runnable age, and max poll/chunk duration. Global throughput can hide a starved affinity group.

### Backpressure and admission

Fair dispatch cannot save a scheduler whose runnable queue grows without bound. Admission must limit queued tasks, retained payloads, and per-tenant share. Reject, shed, coalesce, or push back before allocation and side effects exceed budget.

Spawning one task per input and asking each to cooperate still retains one frame per input. Often a fixed worker set should pull from a bounded queue. Scheduling and flow control are separate, coupled contracts.

### Scheduler policy is a governed interface

Quantum, weight, priority, affinity, and queue capacity are product behavior, even when hidden behind a runtime. A configuration change can shift tail latency, tenant share, cleanup progress, and memory use without changing application source. Give each parameter an owner, valid range, default, rollout plan, and rollback signal.

Do not let untrusted callers label every request urgent or choose unlimited quantum. Translate authenticated service classes into bounded internal policy. Account by the resource actually protected—processor time, bytes, requests, or device occupancy—and prevent one identity from multiplying share through many tasks.

For reproducibility, record scheduler policy and relevant runtime version alongside traces. A deterministic test scheduler should define tie-breaking explicitly. Production scheduling remains nondeterministic, so assertions should target invariants and service bounds rather than one accidental total order. Policy changes require workload replay or controlled rollout because improvements in throughput can regress interactive or shutdown latency.

### Cleanup and shutdown

Shutdown is scheduled work. First stop admission, then signal cancellation, wake waiting tasks so they can observe it, continue dispatching cleanup, enforce a deadline, and join terminal ownership. Immediately stopping the executor can strand frames and resources.

Cleanup tasks need service even during overload; reserve capacity or prioritize them with a bounded policy. Record tasks that fail or exceed the shutdown deadline and define forced termination consequences.

### Observability and testing

Measure runnable queue length, task age, scheduler latency, chunk/poll duration, yields, wakes, duplicate enqueues, steals, blocking-pool saturation, cancellations, and cleanup time. Histograms and maxima matter; averages hide starvation.

Deterministic tests model arrivals, readiness, yields, and priorities. Assert each expected task receives service within a policy-specific turn bound. Then load-test wall-clock objectives with hostile workloads. Instrumentation perturbs timing, so corroborate with sampling/profiling where appropriate.

## Definitions and Notation

For task `i`, let `r_i` be the time it becomes runnable, `s_i` its next service start, and scheduler latency `L_i=s_i-r_i`. Let chunk duration be `C_i=end_i-s_i`.

A work quantum `q` limits counted units per dispatch; a time objective `B` targets `C_i<=B` under stated inputs and measurement environment. Count-based `q` does not prove the time inequality.

Let ready queue `R(t)` contain unique runnable task identities. The queue invariant is `multiplicity(i,R)<=1`. A dispatch changes one task RUNNABLE to RUNNING; yield returns it to the tail only if still live.

For `n` continuously runnable tasks under pure round robin and unit-cost chunks bounded by `B`, a task waits at most approximately `(n-1)B` between turns, excluding scheduler overhead. This bound fails with arrivals into higher-priority queues, unequal/unbounded chunks, affinity blockage, or scheduler stalls.

## Mechanisms, Invariants, or Proof Structure

Audit a cooperative scheduler in this order:

1. name scheduling unit, dispatcher, workers, and preemptive layers;
2. enumerate task states and unique-queue transitions;
3. identify every yield, suspension, wake, and terminal boundary;
4. bound the longest non-yielding and non-cancellation-check region;
5. state queue order, quantum, weights, priorities, and aging policy;
6. prove readiness is stored and wake registration cannot be lost;
7. make partial state valid/private at every yield;
8. isolate blocking/CPU work with bounded admission;
9. bound runnable tasks, payloads, detached work, and cleanup;
10. define affinity, stealing, and priority-inversion behavior;
11. stop admission, cancel, wake, drain, and join during shutdown; and
12. test deterministic turn bounds and empirical latency objectives separately.

The executable model applies quantum-two round robin to three finite tasks. Work units are abstract and equal by stipulation.

<!-- bijux-verify: {"id":"cooperative-round-robin-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"schedule=['A2', 'B2', 'C1', 'A2', 'B1', 'A1']\ncompletion=['C', 'B', 'A']\nturns=6\nmax_slice=2\nA_service=5\nB_service=3\nC_service=1\nremaining=0\n","stderr":""}} -->
```python
queue = [["A", 5], ["B", 3], ["C", 1]]
quantum = 2
schedule = []
completion = []
service = {"A": 0, "B": 0, "C": 0}

while queue:
    name, remaining = queue[0]
    queue = queue[1:]
    used = quantum if remaining >= quantum else remaining
    remaining -= used
    service[name] += used
    schedule.append(f"{name}{used}")
    if remaining:
        queue.append([name, remaining])
    else:
        completion.append(name)

print(f"schedule={schedule}")
print(f"completion={completion}")
print(f"turns={len(schedule)}")
print(f"max_slice={quantum}")
print(f"A_service={service['A']}")
print(f"B_service={service['B']}")
print(f"C_service={service['C']}")
print("remaining=0")
```

Limitations: this finite single-worker model has equal-cost units, no arrivals, waits, wake races, priority, cancellation, blocking, affinity, overhead, failures, deadlines, stealing, or clocks. It demonstrates one queue policy, not production fairness or latency.

## Alternatives and Trade-Offs

**Preemptive threads** limit damage from non-cooperating user code at instruction/timer boundaries but introduce arbitrary interleavings, synchronization cost, and larger stacks.

**Cooperative tasks** make ordinary segments run to completion and can use compact frames. Responsiveness depends on bounded cooperation.

**Hybrid executors** combine preempted workers with cooperative tasks and runtime budgets. They improve resilience but require reasoning at both layers.

**Round robin** is simple and predictable for equal work. **Weighted/deficit policies** support classes and variable costs but add accounting and configuration risk.

**Event-driven suspension** avoids polling and idle service. **Periodic yield/polling** is simpler for some algorithms but wastes turns or adds detection latency.

**Cooperative chunking** retains local state cheaply for divisible work. **Bounded worker offload** handles blocking or indivisible CPU calls but adds a second queue and late-completion ownership.

**One task per item** isolates failures and latency but retains many frames. **Fixed workers pulling bounded work** constrain memory and admission.

## Failure Modes and Misconceptions

- “Cooperative means single-threaded.” Multiple preempted workers can run cooperative tasks.
- “Preemptive means fair.” Priorities and locks can still starve work.
- “Await always yields.” Ready operands can continue immediately.
- “Any yield reaches I/O.” Queue priority and phase decide.
- “Round robin bounds wall time.” Only when chunk cost and other assumptions are bounded.
- “Wake once means one event.” Wakes may coalesce or be redundant.
- “More yields always help.” Too-small chunks add overhead and expose partial-state boundaries.
- “Async code cannot block.” Synchronous prefixes and foreign calls can occupy workers.
- “Cancellation is immediate.” Response is bounded by the next safe check plus scheduling/cleanup.
- “Fair scheduling prevents overload.” Admission and retained frames need separate bounds.
- “Priority solves latency.” It can move starvation to another class.
- “Averages prove fairness.” A starved tail can coexist with good mean latency.
- “Yielding inside a lock is harmless.” It extends exclusion across arbitrary peer work.
- “Stopping the executor completes shutdown.” It may strand resources and owned tasks.

## Worked Examples

### Example 1

A callback scans an unbounded array on a UI loop. Partition into chunks sized from a latency objective, preserve source index/result order, check cancellation, and yield to the UI task queue. If one record itself is unbounded, reject or offload it; chunking only between records cannot constrain that record.

### Example 2

A JavaScript loop calls `await Promise.resolve()` every thousand iterations, yet timers remain delayed because continuations replenish microtasks. Use a documented later-turn scheduling primitive for the target runtime. The repair is about which queue becomes eligible, not the spelling of await.

### Example 3

Task A repeatedly self-wakes and returns pending without readiness changes. It stays runnable and consumes polls. Store actual readiness, register a producer wake, and return pending only when another actor can create progress. Rate-limiting the spin treats a symptom.

### Example 4

Round robin gives A and B one turn each, but A's “unit” performs 50 ms and B's performs 1 ms. Turn fairness is not time fairness. Calibrate by measured cost, split A's unit, or use deficit/time budgets; preserve a maximum indivisible-operation policy.

### Example 5

High-priority requests arrive continuously, so cleanup never runs and permits leak. Reserve cleanup capacity or impose a bounded priority burst plus aging. Admission should reject excess urgent work rather than borrowing indefinitely from lifecycle progress.

### Example 6

Four cooperative executor workers enter a blocking library call; completions requiring those workers cannot run. Move the call to a bounded blocking pool with queue rejection and late-result observation, or adopt a nonblocking API. Adding an unbounded thread per call moves the failure to memory and context switching.

### Example 7

A batch mutates a shared ledger after each item and yields every hundred. Cancellation exposes a valid but unintended prefix. Build private candidate state and atomically publish at completion, or explicitly define per-chunk commits, idempotency, and resume/compensation metadata.

### Example 8

A task is woken three times before dispatch. The scheduler coalesces it into one queue entry; the task reads three messages from its real queue. If messages existed only as wake counts, two would be lost. Scheduling notification and protocol data must be separate.

### Example 9

A work-stealing runtime shows excellent total throughput, but a non-transferable UI executor has one 400 ms chunk. Global metrics hide its starvation. Track runnable age and maximum chunk per affinity domain, and reject blocking work at the UI boundary.

### Example 10

An industrial robot's cooperative controller checks emergency stop only between path segments, and one segment computes for 800 ms. A 50 ms stop requirement is not met by cooperative intent. The system needs independently enforced safety mechanisms, verified worst-case execution time, bounded checkpoints, safe-state transitions, and hardware evidence. Named controls, real-time, robotics, functional-safety, cybersecurity, operations, and regulatory reviewers must approve it; this chapter cannot.

## Cross-Program Connections

- **Algorithms:** incremental algorithms expose bounded safe interruption points.
- **Operating systems:** preemption, priorities, affinity, and blocking interact with language schedulers.
- **Real-time systems:** worst-case execution and response analysis require stronger platform guarantees.
- **Distributed systems:** local fairness cannot guarantee remote service or rollback.
- **Software engineering:** scheduling policy is an owned component contract, not utility code.
- **Security:** hostile inputs exploit algorithmic complexity and event-loop blocking as denial of service.
- **Platform engineering:** worker counts, queue bounds, and shutdown determine operational behavior.
- **Observability:** tail scheduler latency and runnable age reveal starvation hidden by throughput.

## References

1. Python Software Foundation. “asyncio — Tasks: Task Object.” <https://docs.python.org/3/library/asyncio-task.html#task-object>.
2. WHATWG. “HTML Standard: Event Loops.” <https://html.spec.whatwg.org/multipage/webappapis.html#event-loops>.
3. Node.js Project. “Timers: Scheduling Timers.” <https://nodejs.org/api/timers.html>.
4. Node.js Project. “Don't Block the Event Loop (or the Worker Pool).” <https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop>.
5. Rust Project. “std::task::Waker.” <https://doc.rust-lang.org/std/task/struct.Waker.html>.
6. Tokio Project. “Preemption.” <https://tokio.rs/blog/2020-04-preemption>.
7. Tokio Project. “Bridging with sync code.” <https://tokio.rs/tokio/topics/bridging>.
8. Go Project. “Go Scheduler Design Doc.” <https://go.dev/src/runtime/HACKING>.
9. The Open Group. “sched_yield.” <https://pubs.opengroup.org/onlinepubs/9799919799/functions/sched_yield.html>.
10. Linux Kernel Documentation. “CFS Scheduler.” <https://docs.kernel.org/scheduler/sched-design-CFS.html>.

## Exercises

### Exercise 1

State sufficient assumptions under which finite-task round robin provides a finite turn delay. Why is this not automatically a wall-clock bound?

### Exercise 2

A browser loop yields with an already-resolved promise but starves timers. Diagnose the queue error and specify the evidence needed for a repair.

### Exercise 3

Design a cancellable cooperative map over one million records with a 10 ms initial chunk objective. Address indivisible records, partial results, ordering, and measurement.

### Exercise 4

Define shutdown for a scheduler containing runnable tasks, event-waiting tasks, and blocking-pool tasks. Include admission, wakeup, cancellation, deadlines, and evidence.

### Exercise 5

A radiation-treatment controller cooperatively checks abort only between optimization iterations; a single iteration has unverified duration. Explain why the abort claim is unsupported and name required human evidence.

## Answers to the Exercises

### Answer 1

Assume a finite set of continuously runnable tasks, unique queue membership, tail requeue, a dispatcher that continues running, no privileged arrivals, and a finite bounded chunk for each task. Then each task is selected after at most the other queued tasks' turns. Wall time also includes variable chunk cost, scheduler overhead, preemption of workers, affinity stalls, and blocking; a work quantum alone cannot bound those.

### Answer 2

Promise reactions use the microtask checkpoint, and recursively replenishing that queue can delay ordinary timer tasks. Select a documented task/later-turn primitive whose processing model allows the timer queue to advance. Verify with a controlled trace, bounded chunk measurement, timer-delay distribution, cancellation behavior, and tests on supported runtime/browser versions; do not infer a universal ordering from one observation.

### Answer 3

Keep input and candidate output under one owner; process a bounded count estimated from conservative per-record cost; periodically measure elapsed time; check cancellation before and within chunks; then yield through the target scheduler phase. Preserve results by source index. On cancellation discard private candidate output or publish only documented transactional chunks. Reject/offload a record whose indivisible cost violates budget. Load-test percentile and maximum chunk duration on bounded hostile inputs and retune without calling the initial estimate a guarantee.

### Answer 4

Stop new admission first. Signal cancellation to every owned task. Wake event waiters so they can observe it, and keep dispatching runnable cleanup. Ask blocking operations to cancel where supported while retaining ownership of late completion. Enforce a documented graceful deadline, record tasks/resources still live, apply a separately approved forced policy, join all terminable work, and stop workers last. Evidence includes state counts, queue drain, resource/permit balance, late outcomes, and repeated deterministic shutdown tests.

### Answer 5

Cooperative abort latency includes the remaining indivisible iteration, scheduler delay, stop actuation, and verification. Without a verified maximum iteration time, no bound follows. Required evidence includes named radiation oncology, medical physics, controls/real-time, software, functional-safety, cybersecurity, human-factors, quality, and regulatory reviewers; hazard/requirements traceability; worst-case execution analysis; hardware-in-the-loop and fault injection; independent dosimetry/interlocks; applicable-standard assessment; residual-risk acceptance; and deployment validation. This module claims none of that approval.
