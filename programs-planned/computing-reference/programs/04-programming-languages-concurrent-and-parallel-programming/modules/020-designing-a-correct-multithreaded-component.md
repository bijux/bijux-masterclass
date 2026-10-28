---
module_id: CONPAR-020
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 20
title: Designing a Correct Multithreaded Component
status: complete
last_verified: 2026-08-29
---

# Designing a Correct Multithreaded Component

## One-Page Review

### Governing question

How can a multithreaded component expose a simple public contract while correctly owning admission, mutable state, task identity, results, failures, cancellation, memory visibility, dependencies, and every path from construction through termination?

### Essential definitions

- A **component** is an encapsulated concurrent subsystem with an API, owned threads, state, resources, and lifecycle; its **abstract state machine** describes externally meaningful behavior.
- Its **representation invariant** holds for every reachable internal state.
- A **linearization point** is the instant at which a concurrent operation takes effect in an equivalent legal sequential history.
- An **ownership state** names the one location responsible for a task: caller, queued, active, or terminal.
- **safe publication** makes initialized state visible to threads that receive it through a specified synchronization edge.
- A **lifecycle gate** atomically decides whether an operation is allowed; **quiescence** means no operation can still change audited state.
- **graceful close** rejects new work but drains accepted work; **abort** requests cancellation and disposal.
- A **completion obligation** is the promise to produce exactly one terminal disposition for every accepted identity.

### Central model, mechanism, or theorem

Model lifecycle (L) as NEW, RUNNING, DRAINING, ABORTING, TERMINATED, or FAILED. Let accepted tasks be partitioned into queued set (Q), active set (A), and terminal map (T). Then:

(Accepted = Q disjoint-union A disjoint-union dom(T))

and therefore:

(|Accepted| = |Q| + |A| + |T|).

Submission linearizes at the lifecycle/admission authority: it adds a fresh identity to Q/A or rejects without ownership transfer. Dequeue transfers Q to A; a final disposition transfers Q/A to one T entry. Termination requires admission closed, Q/A empty, every worker joined, and Accepted=dom(T). This establishes safety only under the stated assumptions.

### Critical invariants

One mechanism owns each mutable field; no identity occupies two ownership states. Items and bytes remain bounded, results publish exactly once, and condition predicates share a synchronization discipline. No foreign behavior runs under an internal lock. Dependencies are acyclic. Cancellation combines state, wake-up, and observation. Startup rolls back. Shutdown atomically closes admission, wakes waiters, reconciles results, and joins workers. Publication has an explicit happens-before path.

### Common failures

Teams publish partial construction; split one invariant across unrelated locks; separate lifecycle checks from enqueue; leak mutable aliases; call user code under locks; lose results on failure; confuse cancellation requests with termination; use metrics for final accounting; create same-component dependency cycles; miss shutdown wake-ups; or terminate while agents remain live.

### Compact example

A component has two workers and queue capacity two. It accepts jobs j1 through j4, starts j1 and j2, and rejects j5. If close races with j6, exactly one gate order is legal: either j6 was accepted before close and must receive a terminal result, or close linearized first and caller retains j6. There is no “probably queued” outcome. Once all four accepted jobs are terminal and both workers join, the component may enter TERMINATED.

### Connections

[Thread Pools and Bounded Work Queues](019-thread-pools-and-bounded-work-queues.md) supplies bounded admission and worker accounting; [Thread-Safe Queues](017-thread-safe-queues.md) supplies ownership transfer and closure; [Lock Ordering and Deadlock Prevention](018-lock-ordering-and-deadlock-prevention.md) supplies dependency reasoning. The [program roadmap](../ROADMAP.md) next develops compiler and processor reordering, the basis for a deeper memory-model account of visibility.

## Governing Question

How should an engineer derive a correct multithreaded component from a public contract, rather than assembling threads, locks, queues, and flags and hoping their local behavior composes?

The answer is to design three models together: the abstract behavior clients may observe, the concrete ownership and synchronization mechanisms that implement it, and the lifecycle proof that accounts for every resource and obligation. A component is correct only when these models refine one another across normal execution, overload, failure, cancellation, and shutdown.

## Why This Matters

Most concurrency defects live between individually familiar mechanisms. A mutex can protect a field while the API still returns an unsafe alias. A thread-safe queue can be correct while submission races with shutdown. A pool can bound workers while retaining unbounded payload bytes. A future can deliver successful results while exceptions silently kill worker capacity. Joining workers can be correct while a callback still mutates component state afterward.

The component boundary is therefore the right unit of proof. It contains public operations, internal state, synchronization, owned execution agents, result obligations, and dependencies on external services. Correctness cannot be delegated to “thread-safe collections” because the relationships among collections frequently form the real invariant.

This module derives one illustrative bounded job component; the method also applies to caches, exporters, coordinators, schedulers, and background processors.

## Prerequisites and Retrieval

Retrieve:

- abstract versus concrete state, invariants, and linearization from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- ownership transfer and channel closure from [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md);
- start, join, worker ownership, and partial-start failure from [Creating and Joining Threads](011-creating-and-joining-threads.md);
- predicates, loops, notifications, and spurious wake-ups from [Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md);
- permit conservation from [Semaphores and Resource Counting](014-semaphores-and-resource-counting.md);
- queue closure and terminal accounting from [Thread-Safe Queues](017-thread-safe-queues.md);
- dependency graphs from [Lock Ordering and Deadlock Prevention](018-lock-ordering-and-deadlock-prevention.md); and
- bounded admission, task failure, cancellation, and shutdown from [Thread Pools and Bounded Work Queues](019-thread-pools-and-bounded-work-queues.md).

Retrieval prompt: draw one state diagram for a component that accepts identified jobs, runs them on two workers, records one result per accepted identity, rejects after close, and supports abort. For every arrow, name the lock or ownership transfer that makes it atomic.

## Learning Objectives

After completing this module, a learner can:

1. specify a concurrent component as an abstract state machine and public contract;
2. derive representation, ownership, capacity, result, and lifecycle invariants;
3. assign one synchronization or ownership authority to each mutable field;
4. identify linearization points for admission, dequeue, result publication, cancellation, and close;
5. establish safe publication and result visibility paths;
6. prevent internal and external dependency cycles and reentrant callbacks;
7. contain startup, worker, task, and downstream failures;
8. design graceful close, abort, quiescence, join, and final reconciliation;
9. build a verification matrix combining deterministic tests, schedule exploration, dynamic tools, and operational evidence; and
10. identify safety-critical claims that require named domain and assurance reviewers.

## Core Exposition

### Begin with the public contract

Suppose a `JobComponent` exposes `start()`, `submit(id, job)`, `cancel(id)`, `close()`, `abort()`, `result(id)`, and `join(deadline)`. Before choosing a language or lock, define each outcome.

`start` moves a fully initialized component from NEW to RUNNING or reports failure and rolls back. `submit` either accepts a fresh identity and creates a completion obligation, or rejects without taking ownership. `cancel` reports whether it cancelled queued work, requested cancellation of active work, observed terminal work, or found no owned identity. `close` is idempotent and prevents later acceptance while allowing accepted work to drain. `abort` additionally requests active cancellation and disposes queued work. `join` waits for termination but does not itself cause unsafe forced thread death. `result` returns or waits for a terminal disposition according to a documented timeout rule.

The contract does not promise FIFO completion, immediate cancellation, fairness, or rollback; those require additional mechanisms and evidence.

### Define the abstract state machine

Use lifecycle states:

- NEW: constructed, no worker may observe the component;
- RUNNING: submissions may be accepted;
- DRAINING: submissions are rejected; accepted work drains;
- ABORTING: submissions are rejected; queued work is cancelled and active work is asked to stop;
- TERMINATED: no owned worker or unfinished obligation remains; and
- FAILED: startup or component-level failure prevents normal service, with disposition rules still required.

Legal transitions are NEW -> RUNNING/FAILED, RUNNING -> DRAINING/ABORTING, DRAINING -> ABORTING/TERMINATED, ABORTING -> TERMINATED, and FAILED -> TERMINATED after cleanup.

### Partition task ownership

For every accepted identity, exactly one of these holds:

1. queued: the component owns the job but no worker does;
2. active: exactly one worker owns execution;
3. terminal: a result record owns the final disposition.

The caller owns a rejected job. This distinction is essential at the submit/close race. “The enqueue succeeded but the caller saw closed” can cause duplicate external work; “the caller saw success but enqueue failed” loses work. One critical section or one linearizable queue/lifecycle protocol must decide both ownership transfer and response.

Terminal dispositions include completed(value), failed(error), cancelled-before-start, cancelled-during-run if cooperation confirms it, and component-failed. Rejected is not an accepted terminal disposition because component ownership never began.

### Derive the representation invariant

A useful representation contains lifecycle L, bounded queue Q, active map A from identity to worker/cancellation state, terminal map T, worker set H, and configured worker and queue bounds W and K. The invariant includes:

- L belongs to the legal lifecycle set and transitions monotonically;
- Q, dom(A), and dom(T) are pairwise disjoint;
- their union equals Accepted;
- every queue entry has a unique identity and valid payload;
- (0 <= |A| <= W) and (0 <= |Q| <= K);
- retained payload bytes stay within a separate byte budget;
- every worker in H has exactly one owned lifetime and eventual join obligation;
- a terminal map entry is immutable;
- RUNNING is the only admission state;
- TERMINATED implies Q and A empty, all H joined, and Accepted = dom(T); and
- each condition variable predicate reads state protected by its associated mutex.

The invariant is not “all fields are thread-safe.” It relates fields. Moving an identity from Q to A must be one logical transaction. Publishing a result must remove it from A and add it to T without an observable gap that another operation mistakes for “unknown.”

### Assign synchronization authority

Make a field-ownership table. One simple design uses a single state mutex for lifecycle, Q metadata, A, T, and condition predicates. Workers remove a job under the mutex, release it, run user code, reacquire it, publish terminal state, and notify. This is often preferable to premature lock splitting because the central invariant is small and user work is outside the lock.

If queue storage has its own proven synchronization, specify a protocol connecting it to lifecycle and accounting. Two independently safe locks do not make the cross-field transition atomic. A global order can prevent deadlock, but it does not alone establish a consistent snapshot.

### Locate linearization points

For each operation, name the effect point:

- start: lifecycle changes from NEW to RUNNING after all workers are successfully created or made ready;
- submit accepted: fresh identity is inserted into the component-owned state under the admission gate;
- submit rejected: lifecycle/duplicate/capacity decision is made without ownership transfer;
- dequeue: identity moves atomically from Q to A;
- queued cancellation: identity moves atomically from Q to terminal-cancelled;
- running cancellation: cancellation request flag changes; confirmed terminal cancellation occurs later;
- completion/failure: identity moves from A to immutable T;
- close: lifecycle changes from RUNNING to DRAINING;
- abort: lifecycle changes to ABORTING and queued disposition begins under the same authority;
- termination: final preconditions hold and lifecycle becomes TERMINATED.

### Publish state safely

Construct all immutable configuration before any worker can receive `this` or an equivalent self-reference. Starting a thread from a constructor can expose default or partly initialized fields, and the worker can call overridable behavior before subclass initialization finishes.

Thread creation/start, mutex unlock-to-lock, condition wait/notify used with its predicate, channel send/receive, atomic release/acquire, and thread completion/join provide language-specific visibility only as guaranteed by the language memory model. “The CPU will flush the cache” is not a proof.

A worker publishes results through synchronization acquired by readers. Atomic readiness with non-atomic payload works only when paired release/acquire covers the payload and no later mutation races.

### Keep user behavior outside internal locks

Jobs, callbacks, log sinks, destructors, cancellation hooks, and extension points are foreign code. They can block, reenter, acquire locks in unknown order, invoke shutdown, or throw. Capture the necessary immutable inputs under the internal mutex, release it, invoke foreign code, then reacquire and validate the current generation/state before committing a result.

Define whether callbacks are part of completion: otherwise join can return while callbacks remain active. Logging is also foreign behavior; capture a small event under the lock and export it after unlock.

### Bound the whole component

Beyond workers and queue items, bound payload/result bytes, identity records, downstream requests, retries, blocked submitters, callbacks, telemetry, and shutdown time.

Capacity policy is part of the API. Reject, timed-wait, caller-runs, coalesce, or redirect have different ownership consequences. Blocking component workers can deadlock; caller-runs can execute foreign work under an unrelated caller lock. Backpressure must reach a producer capable of slowing down: unbounded caller retries defeat a bounded queue.

### Analyze dependencies and liveness

Draw a wait-for graph containing component mutexes, queue space, workers, result futures, callbacks, joins, external connection pools, and downstream acknowledgements. A worker that submits child work to the same full component and waits adds worker -> child; child requires a worker, forming a cycle. A callback executed under the state mutex that calls `close` creates a reentrant or lock cycle. A shutdown thread that holds a lock while joining a worker can wait for a worker that needs that lock to exit.

<!-- bijux-verify: {"id":"component-wait-for-graph","mode":"schematic","language":"text","toolchain":"none","reason":"The graph states abstract dependency edges across locks, workers, and futures and is not an executable program."} -->
```text
shutdown -> joins worker -> needs state mutex -> held by shutdown
worker -> waits child result -> child queued -> needs free worker
callback -> calls component -> needs state mutex -> held during callback
```

Prevent these cycles structurally: never join under an internal lock; never invoke foreign code under it; disallow or make nonblocking recursive submission; use structured helping only with a scheduler designed for it; isolate dependent work; impose lock order across owned locks; and put deadlines plus explicit failure semantics at external waits.

### Contain failures

Startup is a transaction. Create resources in an order that supports reverse cleanup. If the third of four worker starts fails, close admission, signal already-started workers, join them, dispose queued obligations, release handles, and report FAILED. Do not expose RUNNING before startup commits.

Each worker has an outer containment boundary that converts recoverable task failures to terminal results, restores reusable-thread context, and decrements active accounting exactly once. Remote effects need idempotency or an explicit outcome-unknown policy: local terminal publication is not exactly-once business effect.

### Design cancellation as a protocol

Queued cancellation arbitrates with dequeue under the ownership authority. If cancellation wins, Q -> T(cancelled-before-start). If dequeue wins, cancellation marks the active token and the worker must observe it at documented checkpoints.

Cancellation requires state, wake-up, and observation. A flag alone leaves sleepers blocked; a wake-up without persistent state can be missed. Arbitrary forced termination can strand locks and invariants, so define cooperative checkpoints, cleanup, and result precedence.

### Close, abort, and terminate

Graceful close changes RUNNING to DRAINING at the admission gate, rejects later submissions, wakes idle workers, and allows Q/A to reach terminal outcomes. When Q and A are empty, workers exit; an owner joins them; final reconciliation confirms every accepted identity in T; then TERMINATED is published and join waiters are notified.

Abort moves queued entries to terminal dispositions, signals active tokens, wakes conditions, and awaits cooperation. A deadline can report incomplete termination but cannot stop arbitrary code; forced reclamation needs process isolation. Calls are idempotent, close may escalate to abort, and owned workers may not self-join.

### Reconcile authoritative state

Approximate live counters do not prove completion. At quiescence, use authoritative state to confirm admission closed; Q and A empty; every accepted identity exactly once in T; all workers and callback agents joined; and no owned permit, handle, or downstream request remains. Report any unresolved identity and last transition.

### Verify at multiple layers

Combine static review; boundary unit tests; deterministic submit/close, cancel/dequeue, and finish/abort schedules; small-state model checking; race detectors; stress; fault injection; and production telemetry. None subsumes the others: connect each claim to evidence capable of supporting it.

## Definitions and Notation

Let lifecycle (L) be in {NEW, RUNNING, DRAINING, ABORTING, TERMINATED, FAILED}. Let (I) be all submitted identities, (R) rejected identities, (Q) the queued sequence, (A) the active identity-to-worker map, and (T) the immutable terminal identity-to-outcome map. Let (C_i) be cancellation state for identity i, (H) the set of owned worker handles, worker bound (W), queue item bound (K), and retained-byte bound (B).

Accepted identities are (E = set(Q) union dom(A) union dom(T)). The ownership invariant requires these three sets pairwise disjoint. Capacity requires (|Q| <= K), (|A| <= W), and retained bytes at most B. Rejection requires (R intersect E = empty). At final termination, (E = dom(T)), Q is empty, A is empty, and every handle in H has joined.

A history (H_s) is a sequence of invocation and response events. A concurrent implementation is linearizable if each completed operation can be placed between its invocation and response in a legal sequential history that preserves real-time order. A happens-before relation (->hb) is supplied only by synchronization rules of the implementation language; it is not wall-clock order.

Safety says prohibited states are unreachable. Liveness says desired transitions eventually occur under stated fairness, finite-work, cancellation-cooperation, and downstream-response assumptions. Quiescence is the absence of operations that can change the audited state.

## Mechanisms, Invariants, or Proof Structure

A disciplined derivation proceeds as follows:

1. **Write observable operations and outcomes.** Include overload, timeout, duplicate identity, failure, cancellation, and shutdown.
2. **Define abstract states and legal transitions.** Make lifecycle monotonic and state what restart would mean.
3. **Partition ownership.** Assign every accepted identity to exactly one queued, active, or terminal state.
4. **Derive the representation invariant.** Relate lifecycle, queue, workers, results, cancellation, capacity, and handles.
5. **Assign authority.** Map each field and cross-field transition to one lock, atomic protocol, or ownership transfer.
6. **Locate linearization points.** Test every race against a legal sequential explanation.
7. **Establish visibility.** Connect initialization, task input, cancellation, and results through language-defined happens-before edges.
8. **Analyze wait-for edges.** Include foreign callbacks, futures, joins, queues, and external pools.
9. **Specify abnormal paths.** Roll back partial startup; contain task failure; reconcile uncertain downstream effects.
10. **Prove termination conditionally.** State finite-work, cooperation, scheduler, and downstream assumptions; then wake, drain/dispose, join, and audit.

The following finite state-space exploration enumerates every ordering of one start, accept, dequeue, finish, close, and terminate event. Only orders respecting the lifecycle and accounting guards are accepted.

<!-- bijux-verify: {"id":"component-lifecycle-state-space","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidate_event_orders=720\nvalid_lifecycle_orders=3\ninvalid_lifecycle_orders=717\naccepted_terminal_reconciled=3\n","stderr":""}} -->
```python
events = ("start", "accept", "dequeue", "finish", "close", "terminate")
candidate_count = 0
valid_count = 0
reconciled_count = 0

def examine(order):
    lifecycle = "NEW"
    queued = 0
    active = 0
    accepted = 0
    terminal = 0
    valid = True

    for event in order:
        if event == "start" and lifecycle == "NEW":
            lifecycle = "RUNNING"
        elif event == "accept" and lifecycle == "RUNNING":
            queued += 1
            accepted += 1
        elif event == "dequeue" and lifecycle in ("RUNNING", "DRAINING") and queued == 1:
            queued -= 1
            active += 1
        elif event == "finish" and active == 1:
            active -= 1
            terminal += 1
        elif event == "close" and lifecycle == "RUNNING":
            lifecycle = "DRAINING"
        elif event == "terminate" and lifecycle == "DRAINING" and queued == 0 and active == 0:
            lifecycle = "TERMINATED"
        else:
            valid = False
            break

        if accepted != queued + active + terminal:
            valid = False
            break

    reconciled = valid and lifecycle == "TERMINATED" and accepted == terminal
    return valid, reconciled

def enumerate_orders(prefix, remaining):
    global candidate_count, valid_count, reconciled_count
    if len(remaining) == 0:
        candidate_count += 1
        valid, reconciled = examine(prefix)
        if valid:
            valid_count += 1
        if reconciled:
            reconciled_count += 1
        return

    for position in range(len(remaining)):
        next_prefix = prefix + (remaining[position],)
        next_remaining = remaining[:position] + remaining[position + 1:]
        enumerate_orders(next_prefix, next_remaining)

enumerate_orders((), events)
print(f"candidate_event_orders={candidate_count}")
print(f"valid_lifecycle_orders={valid_count}")
print(f"invalid_lifecycle_orders={candidate_count - valid_count}")
print(f"accepted_terminal_reconciled={reconciled_count}")
```

Limitations: the exploration contains one job, one worker transition, unique events, sequentially consistent abstract actions, guaranteed finite execution, no payloads, no duplicate IDs, no abort, and no real threads. It checks the stated small transition system, not an implementation, language memory model, fairness, performance, or universal component correctness.

## Alternatives and Trade-Offs

**One state mutex and condition variables** keep the representation proof local and suit modest contention. Long internal critical sections or many independent workloads may limit scalability.

**Separate locks** can reduce contention but require a stable lock order and an atomic protocol for invariants spanning them. Independent thread safety is not compositional proof.

**Actor ownership** assigns mutable state to one event loop and communicates by messages. It simplifies data-race reasoning but still needs bounded mailboxes, cancellation, failure supervision, and nonblocking handlers.

**Lock-free structures** can improve progress or contention properties for narrow operations. Memory reclamation, composition, linearization, and shutdown often become harder; “lock-free queue” does not make a lock-free component.

**Process isolation** supports forced reclamation and fault containment for untrusted work, at the cost of serialization, duplicated memory, process startup, IPC failure, and distributed reconciliation.

**Durable brokers and workflow systems** survive process loss and support redelivery. They require idempotency, leases, persistence, deduplication retention, poison-message policy, and operational ownership.

## Failure Modes and Misconceptions

1. **“Every field is thread-safe, so the component is thread-safe.”** Cross-field ownership and lifecycle invariants can still tear.
2. **Starting workers in a constructor.** A worker may observe partial initialization or overridable behavior before construction finishes.
3. **Checking closed before enqueueing.** Close can linearize between the check and ownership transfer.
4. **Two locks for one invariant.** Different observers can see a task in neither or both ownership states.
5. **User code under an internal lock.** Blocking, reentrancy, unknown lock order, and exceptions compromise progress and cleanup.
6. **Publishing mutable aliases.** A caller can race with the component after a seemingly safe getter returns.
7. **A cancellation boolean alone.** Sleeping workers may never wake; running jobs may never observe it.
8. **Interrupt means rollback.** External side effects and arbitrary invariants are not automatically reversed.
9. **A thread-safe queue makes shutdown safe.** Admission, result obligations, worker exit, and joining remain component protocols.
10. **Rejected and cancelled are synonyms.** Rejection retains caller ownership; cancellation disposes an already accepted obligation.
11. **A successful future proves exactly-once effect.** It proves only the declared local result behavior.
12. **Approximate counters prove quiescence.** Metrics can be stale and transitions can be in flight.
13. **Joining while holding the state lock.** A worker may need it to publish a result and exit.
14. **Race-detector silence proves correctness.** Executed schedules are only a sample.
15. **Termination means the queue is empty.** Active tasks, callbacks, handles, and effects may remain.
16. **One bounded queue means bounded memory.** Payloads, results, retries, and waiters may be unbounded.
17. **Ordinary tests prove safety-critical suitability.** Timing, hazards, hardware, and assurance require qualified review.

## Worked Examples

### Example 1

**Situation.** Jobs a, b, and c were accepted. a is queued, b is executing on worker 1, and c has result failed(E). A monitoring snapshot also lists b as queued.

**Reasoning.** Accepted must be the disjoint union of Q, dom(A), and dom(T). The duplicate b makes Q and dom(A) intersect, so both uniqueness and numeric reconciliation fail: the sum of container sizes is four while only three identities were accepted. The repair is not to subtract one in metrics. Dequeue must atomically remove b from Q and insert it into A under the ownership authority.

**Conclusion.** Identity-level disjointness is stronger and more diagnostic than equality of aggregate counters.

### Example 2

**Situation.** A submitter checks RUNNING, pauses, and a closer changes lifecycle to DRAINING. The submitter then appends job d and returns accepted.

**Reasoning.** No legal sequential ordering explains the implementation: if submit linearized first, d had to enter owned state before close; if close linearized first, d had to be rejected. A stale check plus later enqueue implements neither. Put lifecycle validation and ownership transfer in one critical section, or use a proven linearizable admission protocol. The response follows that single decision.

**Conclusion.** Admission and close need one atomic gate; separate thread-safe operations are insufficient.

### Example 3

**Situation.** A four-worker component starts workers h1 and h2, then creation of h3 fails.

**Reasoning.** Publishing RUNNING early could accept tasks without capacity. Keep NEW during preparation. On failure, signal and wake h1/h2, join them, release resources, publish FAILED, and return the error.

**Conclusion.** Startup is a commit-or-rollback resource transaction, not a loop that tolerates partial success silently.

### Example 4

**Situation.** A worker holds the component mutex while invoking an on-result callback. The callback calls `close()`, which tries to acquire the same non-reentrant mutex.

**Reasoning.** The wait-for cycle is immediate; a reentrant mutex would not solve blocking. Publish an immutable terminal record and capture the event under lock, then unlock, invoke and contain the callback, and account for its lifetime.

**Conclusion.** Foreign code belongs outside internal locks, with callback completion semantics explicitly specified.

### Example 5

**Situation.** A canceller and worker both target queued job e.

**Reasoning.** Under the state authority, one transition wins. Cancellation can move e to cancelled-before-start; otherwise dequeue moves e to A and cancellation marks its active token for checkpoints. Both preserve one terminal result.

**Conclusion.** Cancellation arbitrates ownership first and cooperates with active execution second.

### Example 6

**Situation.** A worker writes a result payload, sets a plain `ready` boolean, and a reader spins until the boolean appears true before reading the payload.

**Reasoning.** Neither flag nor payload has a synchronization relation, so the reader may loop or observe stale data. Use a shared mutex, channel, specified future, or language-correct release/acquire publication.

**Conclusion.** Wall-clock write order is not a visibility proof; result publication requires a happens-before edge.

### Example 7

**Situation.** Both workers run parent jobs. Each parent submits one child to the component and waits on its child result. Queue capacity is two.

**Reasoning.** Children queue, but parents retain both workers while waiting for children that require those workers. A larger queue changes nothing. Compute inline, release workers through composition, use proven scheduler helping, or isolate bounded execution.

**Conclusion.** The component must analyze worker/future dependencies; queue acceptance does not imply executable progress.

### Example 8

**Situation.** At abort, Accepted has 10 identities: 3 queued, 2 active, and 5 terminal.

**Reasoning.** Under the state lock, move the three queued identities to terminal cancelled-before-start, making Q zero and T eight. Mark cancellation requested for the two active identities and wake them. Abort cannot yet claim termination. Suppose one cooperates and publishes cancelled-during-run while the other finishes successfully; A becomes zero and T becomes ten. After workers exit and join, Accepted equals dom(T), so termination may publish.

**Conclusion.** Abort is a disposition and cooperation protocol, not an instantaneous erasure of work.

### Example 9

**Situation.** The queue holds at most 100 jobs, but each job may retain a 20 MiB payload; terminal results are retained forever.

**Reasoning.** The queue can retain roughly 2,000 MiB before overhead, while results grow forever. Add byte-weighted admission, cap results, and define acknowledgement/TTL/idempotency retention.

**Conclusion.** Boundedness must cover bytes and post-completion state, not only queue length.

### Example 10

**Situation.** A medical infusion controller proposes using this component to schedule actuator commands, claiming that linearizability and passing stress tests prove safe delivery deadlines.

**Reasoning.** The model audits identity, transitions, cancellation, and accounting, but not worst-case timing, hardware/sensor hazards, fail-safe states, regulation, or human interaction. Mean latency and race tests do not prove deadlines. Named controls/domain, real-time, hardware, hazard, and assurance reviewers need target evidence.

**Conclusion.** Do not authorize safety-critical deployment from this chapter or its finite model; qualified named human review and system-specific assurance are mandatory.

## Cross-Program Connections

- **Programming languages and semantics:** linearizability is a refinement from implementation histories to an abstract sequential specification.
- **Operating systems:** scheduling, thread creation, interruption, handles, and process isolation define resource and failure boundaries.
- **Distributed systems:** remote side effects require idempotency, durable identity, uncertain-outcome handling, and reconciliation.
- **Software engineering:** contracts, information hiding, dependency inversion, and test seams make concurrent reasoning reviewable.
- **Security engineering:** unbounded admission, identity collision, callback reentrancy, and tenant starvation are availability and isolation risks.
- **Cloud and platform engineering:** readiness, draining, orchestration deadlines, telemetry, and rolling termination depend on truthful lifecycle semantics.
- **Formal methods:** invariants, temporal properties, model checking, and refinement connect the abstract state machine to code.

## References

1. C. A. R. Hoare. “Monitors: An Operating System Structuring Concept.” *Communications of the ACM* 17(10), 1974.
2. Maurice P. Herlihy and Jeannette M. Wing. “Linearizability: A Correctness Condition for Concurrent Objects.” *ACM TOPLAS* 12(3), 1990.
3. Andrew D. Birrell. “An Introduction to Programming with Threads.” Digital Equipment Corporation Systems Research Center, 1989.
4. Brian Goetz et al. *Java Concurrency in Practice*. Addison-Wesley, 2006.
5. Gregory R. Andrews. *Foundations of Multithreaded, Parallel, and Distributed Programming*. Addison-Wesley, 2000.
6. IEEE and The Open Group. *POSIX.1-2024, Base Definitions and System Interfaces*, 2024.
7. Oracle. “`ExecutorService` and `ThreadPoolExecutor`, Java SE 26 API.” 2026. Accessed 2026-08-29.
8. Python Software Foundation. “`concurrent.futures` — Launching Parallel Tasks, Python 3.14.7 Documentation.” 2026. Accessed 2026-08-29.
9. Rust Project. “`std::sync` — Useful Synchronization Primitives, Rust 1.98.0.” 2026. Accessed 2026-08-29.
10. The Go Authors. “The Go Memory Model.” Current specification accessed 2026-08-29.

## Exercises

### Exercise 1

State the task-ownership partition and final termination condition for the component. Explain why rejection is not one of the accepted terminal outcomes.

### Exercise 2

Trace a component with one worker and queue capacity one through start, acceptance of x and y, rejection of z, close, completion of x, dequeue and failure of y, worker exit, and join. Give L, Q, A, T, and caller/component ownership after each event.

### Exercise 3

Diagnose this design: `submit` reads an atomic RUNNING flag, inserts into a thread-safe queue, then increments an accepted counter; `close` clears RUNNING, closes the queue, waits until the accepted counter equals the terminal counter, and joins workers while holding the result-map mutex. Identify at least four distinct correctness risks and propose a coherent repair.

### Exercise 4

Compare a single-lock component, an actor-owned component, and a lock-free-queue-based component for a telemetry exporter with bounded memory, occasional blocking network sends, callbacks, cancellation, and graceful process shutdown. Choose one and specify its remaining proof obligations.

### Exercise 5

An autonomous railway-door subsystem accepts commands concurrently from route logic, local controls, and diagnostics. Propose the concurrency component boundary, identities, lifecycle, admission, priority, cancellation, shutdown, and verification evidence. State which claims cannot be approved without named human domain and assurance reviewers.

## Answers to the Exercises

### Answer 1

For accepted set E, queued Q, active map A, and terminal map T:

(E = set(Q) disjoint-union dom(A) disjoint-union dom(T)).

Thus (|E|=|Q|+|A|+|T|). TERMINATED requires closed admission, Q/A empty, E=dom(T), joined agents, and reconciled resources. Rejection stays outside T because ownership and completion obligation never transferred; the caller retains the job.

### Answer 2

Initially L=NEW and Q=A=T=empty. Start gives RUNNING. Accept x directly into A; accept y into Q; reject caller-owned z at capacity. Close gives DRAINING. Completion moves x from A to T, dequeue moves y from Q to A, and failure moves y to T. Now Q/A are empty and E=dom(T). The worker exits, its owner joins it, and only then is TERMINATED published. The component never owns z.

### Answer 3

The split flag check makes close/enqueue ownership ambiguous. Queue close can race with insertion. Late counter increment lets terminal precede accepted. Counter equality does not prove identity reconciliation. Joining under the result mutex deadlocks if a worker needs it to publish and exit.

Repair these with one state protocol for lifecycle, identity, ownership transfer, and authoritative accounting. Run tasks outside it. Close under that authority, wake workers, wait in a predicate loop that releases the mutex, join outside locks, reconcile identities, then publish TERMINATED.

### Answer 4

Choose actor ownership: one event loop serializes lifecycle, queue metadata, active requests, results, and callback events. Put network sends in separately bounded asynchronous I/O and return completions as messages. Bound mailbox items/bytes, define overload, arbitrate cancellation with dispatch, close admission, drain/dispose, await I/O, and join.

Obligations remain: safe publication, unique identities, one terminal result, bounded retained state, no synchronous reentry, timeout/uncertain remote outcomes, specified priority, cooperative cancellation, supervision, shutdown deadlines, and reconciliation. A single lock is viable with foreign calls excluded; a lock-free queue leaves lifecycle and termination unresolved.

### Answer 5

Use a narrow coordinator before the independently assured actuator layer. Identify commands by generation, source, and sequence. Use monotonic INITIALIZING, READY, DEGRADED, SAFE_STOPPING, STOPPED states. Admission authenticates source, validates generation/domain, enforces byte/item bounds, and explicitly rejects or supersedes. Reserve safety capacity and analyze starvation and priority inversion.

Cancel only commands safe to cancel; active cancellation reports confirmed, rejected, or outcome-unknown. Shutdown closes ordinary admission, preserves authorized safe-state commands, reconciles identities, reaches the defined mechanical safe state, and joins agents without equating join with physical safety.

Evidence includes formal transitions, invariant/refinement and memory-model review, bounded checking, deterministic races, target timing, fault injection, hardware-in-the-loop tests, diagnostics, hazard traceability, independence, and configuration control. This does not approve deadlines, mechanics, priorities, hazards, security, compliance, or deployment; those require named railway control, safety/security, hardware/real-time, and independent approval reviewers.
