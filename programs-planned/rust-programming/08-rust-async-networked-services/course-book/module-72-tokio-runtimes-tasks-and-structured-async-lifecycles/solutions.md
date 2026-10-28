# Reasoned Solutions — Module 72: Tokio Runtimes, Tasks, and Structured Async Lifecycles

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-02-task-nursery/README.md) · [JobWire guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 72: Tokio Runtimes, Tasks, and Structured Async Lifecycles**. Compare the reasoning against this question: *Once futures are understood as poll-driven state machines, how should a runtime own, schedule, observe, cancel, and finish the tasks that execute them?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Prediction solutions

1. Dropping the handle detaches. The task normally continues until completion or runtime shutdown.
2. Awaiting yields `Result<Result<u64, DomainError>, JoinError>`. The inner result is the domain outcome; the outer result reports task cancellation or panic.
3. Ordinary spawn permits the child to outlive the caller independently. A local borrow cannot cross that boundary based on a later control-flow intention. Use owned data or an enclosing structured scope designed for borrowing.
4. Tokio’s `JoinSet` aborts contained tasks when dropped. That is a cleanup backstop, not evidence that graceful work completed.
5. The runtime worker is blocked for five seconds and cannot poll unrelated ready tasks assigned to it.
6. No. Once blocking work begins, abort does not preempt arbitrary synchronous code. Cooperative cancellation or process isolation is needed for strong stopping behavior.
7. Reentrancy, logical races, unbounded spawning, ignored panics, cancellation-unsafety, and incomplete shutdown remain.
8. Children may continue detached, hold resources, mutate state, or panic unobserved. The group has not reached a complete terminal state.

## Part 2 — Repair reasoning

The original design has five independent defects. It accepts unbounded tasks, blocks runtime workers, loses most handles, permits output to follow completion rather than source order, and has no shutdown. A complete repair first bounds accepted work, then acquires a blocking permit before spawning a synchronous closure, retains every task in a set, tags each result with its source index, and drains the set after failure or cancellation.

`spawn_blocking` is appropriate for bounded, finite blocking calls integrated with an async service. A dedicated Rayon pool is stronger for partitionable CPU work with data-parallel reductions. A synchronous worker group is stronger when work is long-lived, needs strict thread count, or requires cooperative stop points not naturally expressed as many blocking closures.

## Part 3 — Focused exercise guidance

A task tree must include the owner of the owner: for example, the service supervisor owns both listener handles and the broker handle. Connection tasks belong to a `JoinSet`, not vaguely to “the runtime.” Job tasks belong to the broker or a job manager. Cancellation should flow downward; terminal status should flow upward.

For spawn diagnosis, the strongest repair shortens the non-`Send` value’s live range. If a guard protects only extraction of owned data, complete that operation synchronously, drop the guard, then await. Local execution is justified for thread-affine GUI state or a deliberately single-threaded object graph, not because a borrow was inconvenient.

Fail-fast policy should preserve the initiating domain failure and classify later sibling outcomes as completed-before-cancel, cancelled, panicked, or failed independently. Returning only the first observed item erases useful evidence.

## Part 4 — Laboratory comparison

A correct nursery has one owner for every child and a finite maximum child count. It never returns while a child remains unobserved. Tests should use notifications or channels to position children, not sleeps that assume scheduling. Stable indices separate presentation order from completion order.

## Part 5 — Capstone comparison

JobWire’s supervisor should treat an unexpected broker exit as fatal because the broker is state authority. A single connection protocol error is local. Listener failure is fatal unless explicitly retried. The shutdown owner signals admission loops first, then connections and jobs, waits a grace interval, aborts leftovers, and drains every handle. The HTTP service reads broker status but does not own it.

## Part 6 — Reconstruction and defense

A complete defense says that spawn gives the runtime an independently owned future; the application retains lifecycle ownership through a handle or set. Detach means “continue without this owner.” Abort means “request drop at a yield boundary.” Complete shutdown requires terminal observation. Blocking isolation protects runtime workers but still needs bounded admission and cooperative design where hard cancellation matters.

## Deep reasoning and transfer

### Decisive model

> Once futures are understood as poll-driven state machines, how should a runtime own, schedule, observe, cancel, and finish the tasks that execute them?

Build a **task ownership tree**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish a runtime, worker thread, task, future, reactor, and blocking pool.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Explain the `Send + 'static` requirements of ordinary multi-threaded task spawning.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Derive when a task should borrow through an enclosing async scope versus own cloned or moved data.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Use `JoinHandle` and `JoinSet` as explicit result, panic, cancellation, and cleanup obligations.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Distinguish dropping a join handle from aborting the task.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish a runtime, worker thread, task, future, reactor, and blocking pool.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the task ownership tree.

### Reference implementation comparison

For [Task Nursery](../../labs/module-02-task-nursery/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In JobWire, Module 72 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Tokio Runtimes, Tasks, and Structured Async Lifecycles**, which relationship decides this question: “Once futures are understood as poll-driven state machines, how should a runtime own, schedule, observe, cancel, and finish the tasks that execute them?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to JobWire?
