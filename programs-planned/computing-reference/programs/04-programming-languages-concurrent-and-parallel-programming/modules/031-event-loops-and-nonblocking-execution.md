---
module_id: CONPAR-031
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 31
title: Event Loops and Nonblocking Execution
status: complete
last_verified: 2026-08-29
---

# Event Loops and Nonblocking Execution

## One-Page Review

### Governing question

How can one or a few loop threads coordinate many concurrent operations without letting any callback, priority queue, hidden blocking call, or lifecycle transition monopolize progress?

### Essential definitions

- An **event loop** repeatedly waits for eligible events and dispatches associated work.
- **Run-to-completion** means one callback segment runs until it returns or reaches a runtime-defined suspension boundary.
- **Nonblocking I/O** returns without waiting for the external operation to finish; readiness or completion is reported later.
- A **reactor** dispatches readiness and lets application code perform nonblocking I/O.
- A **proactor** dispatches completion of operations submitted earlier.
- A **task/macrotask** is ordinary queued work in a runtime-defined source or phase.
- A **microtask** is higher-priority deferred work drained at runtime-defined checkpoints.
- **Event-loop lag** is delay between when work becomes eligible/scheduled and when the loop runs it.
- **Cooperative fairness** requires callbacks to bound work and yield through a queue that lets competing sources progress.
- **Hidden blocking** is synchronous work concealed behind an asynchronous-looking interface or worker-pool dependency.

### Central model, mechanism, or theorem

At each turn, a loop selects eligible work according to its runtime policy, executes one callback segment without preemption, drains any required priority work, performs other phases, and waits when nothing is ready. Throughput comes from overlapping waiting, not parallel callback execution on one loop. If callback service time or a self-replenishing priority queue is unbounded, unrelated eligible work has no bounded response time.

### Critical invariants

Every operation has an owner from registration through completion/cancellation/close. Callbacks are bounded in input and time. Readiness is treated as permission to attempt I/O, not proof the full request completes. Edge-triggered sources drain until would-block while preserving fairness. Microtask recursion is bounded. CPU and blocking work is partitioned or sent to a bounded pool. Pool saturation has admission/backpressure. Timers express “not before,” not exact deadlines. State is revalidated after suspension. Shutdown stops admission, cancels/drains, closes handles once, and waits for terminal ownership.

### Common failures

Teams put synchronous file, DNS, crypto, compression, parsing, or foreign calls inside loop callbacks; add `async` but never suspend; yield only to a self-replenishing microtask queue; assume zero-delay timers run immediately or in universal order; read only once after edge-triggered readiness; drain one descriptor forever; queue unbounded worker jobs; mutate state across `await` without revalidation; close a handle while completion still owns it; or treat loop responsiveness as dependency readiness.

### Compact example

An I/O task queues two microtasks while a timer is already eligible. Under a checkpoint policy that drains microtasks after the task, the trace is I/O task, parse microtask, authorize microtask, timer task. If authorize recursively queues itself without a bound, the timer can starve. Yielding via another microtask does not return authority to ordinary task selection.

### Connections

[Choosing a Concurrency Model from the Workload](010-choosing-a-concurrency-model-from-the-workload.md) frames the workload decision; [Thread Pools and Bounded Work Queues](019-thread-pools-and-bounded-work-queues.md) owns blocking offload. The [program roadmap](../ROADMAP.md) continues with callbacks, futures, and async/await.

## Governing Question

How should engineers derive an event-loop design from event sources, callback budgets, ownership, fairness, failure, and shutdown—and decide which operations belong on the loop, in a bounded worker pool, or behind another service?

An event loop is a cooperative scheduler. Its main safety property is serialized callback execution; its main risk is that one owner can delay everybody.

## Why This Matters

Network servers, browsers, UI frameworks, language runtimes, storage clients, embedded controllers, and message brokers use event loops to manage many operations without one blocked thread per operation. A loop can monitor thousands of sockets while only ready work consumes callback time.

This efficiency is conditional. A 200 ms parser inside one callback adds roughly 200 ms delay to every eligible callback on that loop. A recursively replenished microtask chain can starve timers and I/O. Offloading to a fixed worker pool moves blocking but can saturate the pool and grow an unbounded queue. Edge-triggered readiness can lose progress when code fails to drain to would-block.

The durable model separates three resources: the loop thread that orchestrates; operating-system readiness/completion mechanisms; and bounded workers or services that execute blocking/CPU work. Each has an admission limit, service-time distribution, queue, cancellation contract, and shutdown owner.

## Prerequisites and Retrieval

Retrieve:

- concurrency/asynchrony distinctions from [Concurrency, Parallelism, and Asynchrony](001-concurrency-parallelism-and-asynchrony.md);
- tasks and fibers from [Processes, Threads, Tasks, and Fibers](002-processes-threads-tasks-and-fibers.md);
- safety/liveness/progress from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- starvation from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- ownership transfer from [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md);
- bounded pools from [Thread Pools and Bounded Work Queues](019-thread-pools-and-bounded-work-queues.md); and
- publication between loop/workers from [Visibility and Publication](024-visibility-and-publication.md).

Retrieval prompt: explain why nonblocking I/O permits overlap while a long CPU callback on the same loop still serializes all clients.

## Learning Objectives

After completing this module, a learner can:

1. model loop iterations, event sources, callback segments, and suspension;
2. distinguish readiness, completion, reactor, proactor, and worker offload;
3. reason about task, microtask, timer, and runtime-specific partial order;
4. set callback work budgets from responsiveness objectives;
5. diagnose synchronous, CPU, microtask, descriptor, and pool starvation;
6. design edge/level-triggered read and write loops;
7. preserve state and lifetime across reentrancy, cancellation, and close;
8. measure lag, utilization, queueing, and per-source fairness; and
9. choose multi-loop, thread-pool, process, or service boundaries.

## Core Exposition

### The loop as a scheduler

An abstract loop:

1. incorporate newly eligible timers, I/O, completions, messages, and close events;
2. select work according to phase/source/fairness policy;
3. run one callback segment;
4. perform required checkpoints such as draining microtasks;
5. update lifecycle state; and
6. wait until the next eligibility/deadline when no work is runnable.

Real runtimes differ. WHATWG defines task sources, task queues, microtask checkpoints, and rendering opportunities. libuv defines timer, pending, poll, check, and close behavior. Node adds runtime-specific next-tick and promise queues. Never turn a simple “sync, microtask, timer” teaching trace into a universal phase order.

Specify only ordering edges the product needs.

### Run-to-completion

One callback segment normally runs synchronously until it returns, throws, or reaches an operation that returns control to the runtime. The loop does not time-slice arbitrary application code.

This simplifies shared state on one loop: another loop callback cannot interleave halfway through a segment. But library calls can invoke user callbacks synchronously, and nested event pumping exists in some UI/runtime contexts. Document reentrancy.

After an asynchronous suspension, other callbacks can mutate state before continuation. Treat the continuation as a new segment: revalidate generation, cancellation, ownership, deadline, and object lifetime.

### Readiness versus completion

Linux `epoll` readiness says an operation can be attempted without the monitored blocking condition; it does not promise a full message, full write, or peer liveness. Nonblocking read/write can return partial progress or would-block.

A reactor receives readiness and performs nonblocking operations until policy says yield. A proactor submits an operation and later receives completion. Windows IOCP is completion-oriented; Unix pollers are commonly readiness-oriented, though libraries present mixed abstractions.

Portable runtimes hide differences, but lifecycle semantics remain: registration, in-flight operation, completion, cancellation race, close, and memory reclamation.

### Level-triggered and edge-triggered sources

Level-triggered readiness remains reportable while the condition holds. It is easier to use but can repeatedly surface a descriptor not yet serviced.

Edge-triggered readiness reports transitions. The application typically sets nonblocking mode and drains until would-block. Reading once can leave data available without a new edge, stalling the connection.

Draining without a byte/operation budget can starve other descriptors. Maintain a ready set and round-robin after a quota. “Drain to EAGAIN” and fairness must be reconciled by remembering that the descriptor remains logically ready when voluntarily yielding.

### Tasks, microtasks, and partial order

In the WHATWG model, each event loop has a microtask queue and performs checkpoints that dequeue microtasks until empty. Promise reactions and explicitly queued microtasks can therefore run before selection of a later ordinary task.

The defensible trace records:

- current synchronous segment completes before deferred work;
- FIFO/order guarantees within the exact source where specified;
- microtask checkpoint guarantees of the selected runtime; and
- context-dependent relations as unspecified.

Do not assert one order between timers, immediates, I/O callbacks, rendering, or close events across runtimes/contexts unless the specification does.

### Microtask starvation

A microtask can enqueue another microtask. If the checkpoint drains until empty, a self-replenishing chain can prevent ordinary task selection. `await Promise.resolve()` or equivalent can remain in the same priority class and fail as a fairness yield.

Bound recursive priority work and yield through a runtime mechanism that permits target competing phases/sources to run. The correct primitive is runtime-specific. Tests should assert that a competing task progresses before a large job completes, not sleep and hope.

Microtasks are good for short invariant completion and promise reactions. They are poor work queues for unbounded batches.

### Timers and clocks

A timer deadline usually means eligible no earlier than a threshold. It can run later because callbacks, microtasks, scheduler delays, sleep, throttling, or clock policy intervene. Zero delay does not mean immediate.

Use a monotonic clock for elapsed-time budgets. Define periodic behavior: fixed-delay, fixed-rate/catch-up, skip missed periods, or coalesce. Unbounded catch-up can monopolize the loop after a pause.

Deadlines must be checked at actual start/commit points. A callback queued before deadline can run after it. Safety-critical real-time guarantees require a different bounded scheduling analysis.

### Blocking I/O and hidden pools

Nonblocking networking can use OS pollers. File I/O, name lookup, cryptography, compression, and foreign libraries may lack a suitable nonblocking path and run in a worker pool. libuv currently uses a global thread pool for filesystem, selected DNS, and user work.

An asynchronous API may therefore:

1. do synchronous setup on the loop;
2. enqueue blocking work;
3. wait behind other pool jobs;
4. execute on a worker;
5. enqueue completion to the loop; and
6. run synchronous result processing on the loop.

Pool queueing and result parsing can dominate. Record which resource each segment uses.

### CPU work

An `async` function is not automatically nonblocking. Parsing a large document, sorting, regex over adversarial input, serialization, image processing, or a tight loop remains synchronous until it yields.

Options:

- reject/bound input;
- stream/incrementally parse;
- process a bounded chunk and yield through a fair phase;
- offload to a CPU worker pool/process;
- use native parallel implementation; or
- move work to a specialized service.

Chunking suits interruptible computations and preserves low setup cost. Worker offload enables parallelism but adds copying/shared-memory, queueing, cancellation, crash, and pool-capacity concerns.

### Callback budgeting

Convert responsiveness into a first bound. If work costs approximately `c` microseconds per item and callbacks should relinquish within `B` microseconds, initial chunk `k≤floor(B/c)`. This is an estimate, not proof: cost distribution, GC, caching, input adversaries, and platform variation matter.

Measure p50/p95/p99/max callback duration, event-loop lag, eligible-to-start delay, and per-source service. Adapt chunk size cautiously to monotonic elapsed time. Always impose an absolute input/step limit.

Fairness is a product policy: interactive requests, control messages, bulk work, and maintenance may have different budgets, but no untrusted client gets unbounded synchronous service.

### Queueing and admission

Event-loop systems still have queues: kernel readiness, runtime tasks, timers, microtasks, application requests, writes, and worker jobs. Nonblocking submission can make overload worse by accumulating work.

For each queue define:

- capacity;
- admission/rejection;
- priority and fairness;
- timeout/cancellation while queued;
- memory per item;
- producer backpressure;
- shutdown behavior; and
- observability.

Backpressure receives its own module later. Here the invariant is simpler: outstanding work is bounded and owned.

### Reentrancy and state machines

Serialized callbacks do not eliminate concurrency bugs. A method can start I/O, return, and resume after another callback closes or repurposes its object. Use explicit states and generations:

`OPEN,g → READING,g → CLOSING,g → CLOSED,g`.

Completion checks matching generation and state. Close is idempotent, prevents new work, resolves in-flight ownership, and delivers one terminal result. Never reuse request memory while the runtime can still complete it.

Callbacks supplied by users can call back into the component synchronously. Establish whether mutations occur before or after invocation and use guard states.

### Cancellation

Cancellation is a request and a race. Completion may win before cancellation reaches the operation. Define outcomes:

- cancelled before start;
- interrupted with partial progress;
- completion won;
- cancellation unsupported;
- outcome uncertain and queryable.

Remove queued work when possible, but do not free its state until the queue/runtime relinquishes ownership. If a worker cannot be interrupted safely, discard/idempotently handle its result and keep capacity accounted until it ends.

### Shutdown

Graceful shutdown:

1. enter DRAINING and stop admission;
2. signal/cancel owned operations;
3. continue running the loop to receive completions/close callbacks;
4. drain or reject queued work by policy;
5. close handles exactly once;
6. wait for worker tasks or terminate isolated workers by contract;
7. reconcile terminal outcomes; and
8. exit only when no referenced owner keeps the loop alive.

Stopping the loop immediately can strand callbacks and leak resources. Keeping a forgotten timer/handle referenced can prevent exit. Test every state at shutdown initiation.

### Multiple loops

One loop eventually reaches one-core callback capacity. Multiple loops on different threads/processes can shard connections or actors. This adds routing, load balance, cross-loop messaging, shared-state synchronization, connection migration, and coordinated shutdown.

Do not share loop handles across threads unless the runtime documents it. libuv, for example, ties a loop to one thread and does not make loop/handle APIs thread-safe except where stated.

Partition by stable ownership keys and keep most state local. Cross-loop calls become messages with bounded queues.

### Observability and diagnosis

Measure:

- loop lag and utilization;
- callback/service-time distributions by source;
- ready/queued counts and age;
- microtask/priority depth;
- timer lateness;
- bytes/operations per descriptor turn;
- worker queue depth, wait, service, and saturation;
- cancellations, late completions, and dropped results;
- handles/requests by lifecycle state; and
- shutdown drain duration.

High utilization may mean useful load or monopolization. Low utilization with high latency may mean pool/dependency waits. Correlate loop, worker, kernel, and application traces.

### Security and resilience

An attacker can send input that triggers worst-case parsing, regex, compression, serialization, or excessive callbacks, turning cooperative scheduling into denial of service. Bound input, algorithmic complexity, callback work, fan-out, and queues.

Worker pools also need tenant fairness; one client can occupy all workers. Isolate crash-prone native code in processes. Treat callback exceptions/rejections as owned terminal outcomes, not silent loop corruption.

Loop responsiveness proves only local scheduling progress. It does not prove a database, broker, or downstream service is ready.

## Definitions and Notation

Let callback `i` become eligible at `e_i`, begin at `s_i`, and finish/yield at `f_i`:

- queue/lag `L_i=s_i-e_i`;
- service segment `C_i=f_i-s_i`; and
- response `R_i=f_i-e_i=L_i+C_i`.

For target callback budget `B` and estimated per-item cost `c>0`, initial chunk `k≤floor(B/c)`, then validate empirically.

Let `O` be outstanding owned operations. Admission invariant `0≤|O|≤K` requires capacity to be reserved before submission and released exactly once at terminal ownership transfer.

“Nonblocking” describes return/wait behavior, not zero work, fairness, parallelism, or bounded latency.

## Mechanisms, Invariants, or Proof Structure

Use this design review:

1. **Inventory event sources and queues.**
2. **Name loop/runtime selection and checkpoint rules.**
3. **Segment each operation** into loop, OS wait, worker, and continuation work.
4. **Bound callback work** by input, steps, and elapsed monotonic time.
5. **Prove I/O progress:** partial operations, would-block, edge/level behavior, quotas.
6. **Prove fairness:** microtasks/priority sources cannot replenish without bound.
7. **Bound admission and pool queues.**
8. **Model state/generation across suspension and synchronous reentrancy.**
9. **Define cancellation/completion races and exactly-once terminal ownership.**
10. **Define shutdown from every state.**
11. **Measure lag, service, queueing, pool saturation, and per-source progress.**
12. **Test adversarial inputs, overload, failures, and target/runtime versions.**

The executable model processes an I/O task that queues two microtasks, drains the microtask checkpoint, then services an already queued timer.

<!-- bijux-verify: {"id":"event-loop-task-microtask-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial_tasks=['io-ready', 'timer']\ncallback_order=['task:io-ready', 'microtask:parse', 'microtask:authorize', 'task:timer']\nmicrotasks_before_timer=2\ntasks_completed=2\ncallbacks_completed=4\n","stderr":""}} -->
```python
tasks = ["io-ready", "timer"]
microtasks = []
callbacks = []
task_index = 0
microtask_count_before_timer = 0

while task_index < len(tasks):
    task = tasks[task_index]
    task_index += 1
    callbacks.append(f"task:{task}")
    if task == "io-ready":
        microtasks.append("parse")
        microtasks.append("authorize")
    microtask_index = 0
    while microtask_index < len(microtasks):
        microtask = microtasks[microtask_index]
        microtask_index += 1
        callbacks.append(f"microtask:{microtask}")
        if task != "timer":
            microtask_count_before_timer += 1
    microtasks = []

print("initial_tasks=['io-ready', 'timer']")
print(f"callback_order={callbacks}")
print(f"microtasks_before_timer={microtask_count_before_timer}")
print(f"tasks_completed={task_index}")
print(f"callbacks_completed={len(callbacks)}")
```

Limitations: this is one stipulated FIFO task/checkpoint policy, not WHATWG, Node, libuv, browser rendering, Python, Rust, or OS behavior. It does not perform I/O, timing, readiness, completion, recursion, worker offload, cancellation, reentrancy, overload, or shutdown and proves no fairness or latency bound.

## Alternatives and Trade-Offs

**Thread per connection/request** delegates preemption to the OS and tolerates blocking, at stack, scheduling, and scale cost.

**Event loop/reactor** handles high I/O concurrency efficiently but makes callback fairness an application responsibility.

**Proactor/completion API** reduces readiness loops but requires in-flight buffer/lifetime ownership.

**Bounded worker pool** contains blocking or CPU work; queueing, saturation, cancellation, and head-of-line blocking remain.

**Cooperative chunking** avoids transfer overhead for interruptible work but uses one loop core and needs a fair yield.

**Multiple loop shards/processes** add parallelism and fault isolation with routing and coordination complexity.

**Actor/channel runtime** packages mailbox ownership and scheduling, while still requiring bounded message handling.

**Synchronous design** can be simplest for low concurrency or batch work and should not be rejected merely for lacking async syntax.

## Failure Modes and Misconceptions

1. **Event loop means events run in parallel.** One loop normally runs one callback segment at a time.
2. **Async syntax means nonblocking.** Synchronous regions still monopolize the loop.
3. **Nonblocking means no waiting anywhere.** OS, pool, device, or downstream wait moves elsewhere.
4. **Readiness means the whole operation completes.** Partial I/O and would-block remain.
5. **Edge-triggered notification can be read once.** Failure to drain/remember readiness can stall.
6. **Drain-until-empty is always fair.** One descriptor can starve peers.
7. **Microtask yield gives all sources a turn.** A replenished priority queue can starve them.
8. **Zero-delay timer is immediate.** It is only eligible according to runtime policy.
9. **Timer order is universal.** Phases and contexts differ.
10. **Worker offload gives infinite capacity.** Pools and queues saturate.
11. **One loop removes races.** Suspension/reentrancy creates logical interleavings.
12. **Cancellation frees state immediately.** Completion may still own it.
13. **Close cancels every completion automatically.** Runtime contracts vary.
14. **High loop utilization proves throughput.** It may indicate monopolization.
15. **Low loop utilization proves health.** The worker pool or dependency may be stuck.
16. **More loops automatically scale.** Routing, shared state, NUMA, and imbalance can dominate.
17. **Logging cannot affect schedules.** It adds work/I/O and can mask timing.
18. **Responsive loop means service ready.** Dependency/admission state is separate.

## Worked Examples

### Example 1

**Situation.** A socket becomes readable under level-triggered polling.

**Reasoning.** Callback reads some bytes and stops. If bytes remain, readiness persists and can be reported again.

**Conclusion.** Correctness is straightforward, though repeated hot descriptors need quotas.

### Example 2

**Situation.** Edge-triggered callback reads once and returns while data remains.

**Reasoning.** No new transition may occur, so no new edge arrives.

**Conclusion.** Drain nonblocking I/O to would-block or remember logical readiness.

### Example 3

**Situation.** Promise/microtask recursively queues itself while a timer is eligible.

**Reasoning.** A checkpoint that drains until empty never reaches ordinary task selection.

**Conclusion.** Bound priority work and yield through a fairness-capable phase.

### Example 4

**Situation.** An async request awaits a file read, then parses a 200 MB document synchronously.

**Reasoning.** I/O waiting overlaps; parsing after resumption monopolizes the loop.

**Conclusion.** Bound/stream/chunk or offload CPU parsing.

### Example 5

**Situation.** File and DNS work share a four-worker pool.

**Reasoning.** Four long file operations can delay unrelated DNS even while loop utilization is low.

**Conclusion.** Measure pool queueing and isolate/bound workloads.

### Example 6

**Situation.** Timer scheduled for 10 ms runs at 80 ms.

**Reasoning.** Eligibility is not execution; prior callback/microtask/scheduler work delayed it.

**Conclusion.** Measure lateness and never interpret timers as real-time guarantees.

### Example 7

**Situation.** Continuation resumes after another callback closed and reopened a slot.

**Reasoning.** Same index now names a new generation. Without validation, stale completion corrupts it.

**Conclusion.** Carry generation and revalidate state after suspension.

### Example 8

**Situation.** Cancellation and successful completion race.

**Reasoning.** Exactly one terminal transition owns result delivery and capacity release; cancellation can lose.

**Conclusion.** Define outcome precedence and keep memory until runtime ownership ends.

### Example 9

**Situation.** Shutdown stops the loop immediately after closing handles.

**Reasoning.** Close/completion callbacks cannot run, leaving ownership and resources unresolved.

**Conclusion.** Stop admission, drain terminal callbacks, reconcile, then exit.

### Example 10

**Situation.** A medical UI's responsive event loop is claimed to prove alarm delivery.

**Reasoning.** Loop lag does not prove device input, prioritization, deadline, audio/display output, acknowledgement, or hazard response.

**Conclusion.** Named clinical, UI, real-time, hardware, concurrency, security, quality, and functional-safety reviewers need target evidence; no approval is implied.

## Cross-Program Connections

- **Operating systems:** pollers, IOCP, timers, scheduling, and signals supply events.
- **Programming languages:** callbacks, futures, async state machines, and runtime queues expose the model.
- **Networking:** partial reads/writes, readiness, connection lifetime, and backpressure dominate loop design.
- **Performance engineering:** queueing, lag, utilization, callback budgets, and tail latency reveal saturation.
- **Security:** adversarial synchronous complexity and unbounded queues cause denial of service.
- **Distributed systems:** timeouts/cancellation do not undo remote commitment.
- **Software engineering:** explicit ownership/state machines make shutdown and late completion reviewable.
- **Safety engineering:** cooperative responsiveness is not a hard real-time guarantee.

## References

1. Douglas Schmidt. “Reactor: An Object Behavioral Pattern for Demultiplexing and Dispatching Handles for Synchronous Events.” 1995.
2. Douglas Schmidt et al. *Pattern-Oriented Software Architecture, Volume 2*. Wiley, 2000.
3. WHATWG. “HTML Standard: Event loops and microtask checkpoints.” Living Standard accessed 2026-08-29.
4. libuv Project. “Design overview,” libuv 1.x documentation. Accessed 2026-08-29.
5. Linux man-pages project. “`epoll(7)`,” man-pages 6.18. 2026.
6. Microsoft. “I/O Completion Ports.” Windows documentation accessed 2026-08-29.
7. Node.js Project. “Don't Block the Event Loop (or the Worker Pool).” Accessed 2026-08-29.
8. Node.js Project. “Event loop, timers, and `nextTick`.” Current documentation accessed 2026-08-29.
9. George Varghese. *Network Algorithmics*. Morgan Kaufmann, 2005.
10. Raj Jain. *The Art of Computer Systems Performance Analysis*. Wiley, 1991.

## Exercises

### Exercise 1

Define event loop, run-to-completion, nonblocking I/O, readiness, completion, task, and microtask.

### Exercise 2

Trace an I/O task that queues two microtasks while a timer is eligible under a drain-after-task checkpoint. Then explain what changes if the second microtask recursively replenishes itself.

### Exercise 3

Diagnose a route that awaits file I/O, performs unbounded parsing, uses `await resolvedPromise` as its yield, and submits crypto to an unbounded worker queue. Repair fairness and capacity.

### Exercise 4

Compare one event loop, a thread per connection, bounded worker offload, cooperative chunking, and multi-loop sharding for a service mixing sockets, files, and CPU transforms.

### Exercise 5

An industrial controller uses edge-triggered I/O, timers, worker offload, cancellation, and MMIO. Specify progress, lifetime, overload, shutdown, timing evidence, and the human-review boundary.

## Answers to the Exercises

### Answer 1

An event loop selects eligible events/work and dispatches callbacks. Run-to-completion means a callback segment is not preempted by another ordinary loop callback before it returns or suspends. Nonblocking I/O returns rather than waiting for completion. Readiness says an operation can be attempted; completion says a submitted operation finished with a result.

A task is ordinary queued work in a runtime-defined source/phase. A microtask is priority deferred work drained at specified checkpoints. Exact ordering is runtime-specific.

### Answer 2

The I/O task runs to completion and queues microtasks parse then authorize. The checkpoint drains parse and authorize in enqueue order. Only after the queue empties does the loop select the timer. Trace: task:I/O, microtask:parse, microtask:authorize, task:timer.

If authorize continually queues another microtask and checkpoints drain until empty, the timer can starve. A cap prevents infinite work; a fairness repair yields through a runtime phase that allows ordinary tasks/I/O, not merely another microtask. Test that the timer progresses before the large job completes.

### Answer 3

The file wait is asynchronous, but parsing after resumption blocks the loop. A resolved-promise yield queues a microtask and can keep ordinary phases starved. An unbounded crypto queue converts overload into memory/latency growth.

Bound input and parse complexity; stream or process chunks with monotonic time/step budgets and a runtime-appropriate ordinary-phase yield, or offload to a bounded CPU pool/process. Give crypto a bounded queue/concurrency limit, tenant fairness, timeout/cancellation, and rejection/backpressure. Measure loop lag, callback duration, worker wait/service, queue depth/age, and late results. Preserve ordering and idempotent terminal outcomes.

### Answer 4

One loop is efficient for many nonblocking sockets but one-core callback-bound. Thread per connection tolerates blocking and gains OS preemption at stack/context-switch cost. A bounded worker pool handles file/blocking and CPU work but adds queueing and saturation. Cooperative chunking suits interruptible modest CPU work without transfer cost. Multi-loop shards use cores but add routing and cross-loop lifecycle.

Use one or several ownership-sharded loops for sockets, bounded file/CPU pools (possibly separate to avoid head-of-line blocking), and cooperative chunking only for bounded transforms. Select shard count and pool capacity from measurement. Bound every queue and define cancellation/shutdown across resources.

### Answer 5

For edge-triggered I/O, use nonblocking operations, drain to would-block with quotas and remembered readiness, and prove no descriptor starvation. Buffers/requests carry generation and remain live until completion/cancel ownership ends. Bound loop callbacks, worker queue, per-client work, and MMIO submissions; define completion-versus-cancel precedence and exactly-once capacity release.

Shutdown stops admission, cancels/drains, receives close/worker completions, reconciles commands, then exits. Timers use monotonic clocks and measured lateness but do not prove deadlines. MMIO/device order requires platform barriers, cache/DMA rules, acknowledgement, timeout, and fault recovery.

Test deterministic schedules, overload, late completion, edge draining, pool saturation, every shutdown state, target timing distributions, hardware-in-loop I/O, device faults, and restart. Named concurrency/runtime, OS/driver, architecture, hardware, controls, real-time, cybersecurity, domain, quality, regulatory, and functional-safety reviewers must approve target claims. This answer is not deployment approval.
