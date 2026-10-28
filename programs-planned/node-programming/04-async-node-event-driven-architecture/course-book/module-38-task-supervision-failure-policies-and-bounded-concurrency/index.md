# Module 38 — Task Supervision, Failure Policies, and Bounded Concurrency

> **Question:** How does a parent scope account for every child operation while limiting concurrency and making failure policy explicit?

## Why this comes now

Module 37 established the preceding async contract. This module adds the next responsibility without discarding that earlier ownership and compatibility discipline.

## Outcomes

By the end of the module, you can:

- represent asynchronous work as a parent-owned task tree;
- distinguish accepted, queued, running, and terminal work;
- limit concurrency by controlling producer invocation rather than promises already started;
- implement continue and fail-fast policies without orphaning running tasks;
- convert every accepted item into exactly one terminal outcome;
- reconcile nondeterministic completion into deterministic source-ordered results;

## 1. Structured concurrency is a discipline

Node promises do not automatically form a task tree, but applications can impose one. A parent operation accepts child work, owns its cancellation signal, records every handle, and does not finish until every child is terminal. This is structured concurrency as an architectural property: child lifetime is bounded by a parent scope.

Without that structure, shutdown, failure, and tests become guesswork. A request handler may return while background mutations continue. A batch may reject on the first failure while the remaining promises keep running. A test may end while timers remain active.

Draw the task tree. For each node, record who may start it, who may cancel it, who observes failure, and who joins it. If any child has no answers, it is orphaned.

## 2. Bounded concurrency starts producers lazily

Creating one promise per input already starts every async function. A semaphore acquired inside each task may bound the protected section but still creates a huge number of waiting closures and promises. A work scheduler should keep source descriptions inert and invoke at most `concurrency` producers at a time.

Use a shared next-index or explicit queue. Each worker pulls one description, invokes it, stores the terminal outcome, and continues. The number of live task promises remains bounded by the worker count plus small orchestration overhead.

Bounded concurrency is not rate limiting. Ten workers can start ten tasks immediately after every completion. Rate control adds time policy; Module 35 supplies that vocabulary.

## 3. Continue and fail-fast mean different terminal sets

In continue mode, one task failure does not cancel independent tasks. Every input runs unless another product rule blocks it. In fail-fast mode, the first decisive failure requests cancellation of the task group and prevents new tasks from starting. Already-running tasks must still be joined and may succeed, fail, or observe cancellation.

Fail-fast does not guarantee that exactly one task fails or that no task after the first source index starts. Scheduling is nondeterministic. The stable guarantee is that after the failure signal, no new task is deliberately admitted, running tasks receive cancellation, and every accepted input receives one terminal outcome.

Use `cancelled` for work stopped by policy and `not-started` or `cancelled-before-start` for descriptions never invoked. Do not label both as domain failure.

## 4. Panics, rejections, and domain failures

JavaScript has no typed distinction between a rejected promise caused by expected domain failure and one caused by a programming defect. The task boundary can still classify known error types, abort reasons, and unknown rejection values. Preserve unknown reasons and mark them as infrastructure or unexpected failure rather than coercing everything to a user message.

A synchronous throw from the producer invocation and an asynchronous rejection from its returned promise must follow the same supervision path. Wrap the invocation in `Promise.resolve().then(() => run(signal))` or an async try/catch that begins before the call.

Global `unhandledRejection` and `uncaughtException` handlers remain last-resort process diagnostics. A supervised task should not reach them.

## 5. Deterministic reconciliation

Workers write outcomes into slots keyed by source index. Live progress events may be completion ordered. The final aggregate validates that no slot is missing and returns a readonly source-ordered array. This validation catches scheduler bugs such as duplicate completion, forgotten cancellation, or an exception escaping before a slot is assigned.

Terminal accounting is a powerful invariant:

```text
accepted = succeeded + failed + cancelled + skipped
```

The exact categories vary, but the sum must match. Maintain separate live counters only as observations; reconstruct the authoritative summary from terminal outcomes after every child is joined.

## 6. Admission, queueing, and memory bounds

A concurrency limit bounds running work, not necessarily waiting work. If a public API accepts an unbounded iterable and first copies it into an array, memory remains unbounded. Define maximum batch size or consume descriptions incrementally. If callers can submit dynamically, define queue capacity and rejection or waiting behavior.

Course 4’s supervised group operates on a validated bounded array. Later queue and service courses introduce dynamic admission and external backpressure. The key discipline is to name each place work can accumulate: caller input, pending descriptions, running promises, result slots, event buffers, and diagnostic history.

## 7. Testing schedule independence

Use controlled tasks whose completions you can release in different orders. Run the same source set with concurrency one, two, and the maximum. Final source-ordered outcomes should remain semantically identical in continue mode. In fail-fast mode, exact cancellation frontier may vary, but terminal accounting and no-orphan guarantees must hold.

Test synchronous throw, asynchronous reject, pre-aborted signal, abort during wait, duplicate completion defense, and invalid concurrency. After the aggregate returns, no task-created timer or promise should remain intentionally active.

## 8. What this changes in TaskHarbor

TaskHarbor’s scheduler now owns a bounded number of running jobs. Ready jobs remain inert until a slot is available. Continue mode executes every dependency-ready task. Fail-fast mode aborts the run after the first failed or timed-out task, cancels pending jobs, joins running jobs, and produces one terminal outcome per manifest task.

Dependencies add a `blocked` state when a predecessor reaches a non-success terminal state. Module 40 integrates that graph policy.

## 9. Deep case study: semaphore after promise creation

A runner maps ten thousand inputs to `run(input)` promises and then awaits them through a semaphore wrapper. The semaphore bounds only how many result handlers enter a section; all ten thousand producers have already started and may allocate sockets, buffers, and timers. Capacity must control **producer invocation**, not merely awaiting.

Store lazy producers or source values. Start a producer only after a slot is acquired. Keep its promise in the parent’s running set until terminal settlement. This design bounds active work; an outer input queue still needs its own finite bound if input itself is unbounded.

## 10. Terminal accounting equation

For a finite accepted batch:

```text
accepted = succeeded + failed + timed-out + cancelled + blocked
```

Every source index appears in exactly one category. Fail-fast does not permit “untouched” entries to disappear; they become cancelled or skipped under an explicit terminal type. Running siblings are signalled and joined. This equation is stronger than checking that the running set reached zero.

## 11. Failure-policy matrix

| Policy | New admission after failure | Running siblings | Independent pending work | Final report |
|---|---|---|---|---|
| continue | allowed | joined normally | continues | all terminal outcomes |
| fail-fast | stopped | cancellation requested, then joined | cancelled | all terminal outcomes |
| quorum | policy dependent | may continue until quorum impossible | classified explicitly | quorum plus per-task report |

The policy must be encoded at the supervisor boundary rather than scattered through task bodies.

## 12. Fair admission and starvation inside a supervisor

A finite concurrency limit prevents unbounded active work but does not guarantee fair selection. A constant stream of high-priority tasks can starve lower priority. TaskHarbor’s batch is finite, so source-order tie breaking eventually reaches every ready task. A long-lived scheduler would need aging, weighted queues, quotas, or another explicit fairness policy.

Keep capacity and priority separate. Capacity answers how many can run. Priority answers which ready item starts next. Dependency state answers which items are eligible. Mixing them into one “score” often hides starvation and makes tests difficult.

## 13. Permit and task cleanup

When capacity is represented by a permit, ownership of the permit must follow the task wrapper through `finally`. Releasing before asynchronous cleanup ends can temporarily exceed the real resource bound. Failing to release after synchronous throw leaks capacity. The simplest batch supervisor can use `running.size`; more general systems may need a semaphore with an explicit lease object.

## 14. Supervisor observability

Live metrics such as running count, queued count, and completion count are useful but not authoritative final results. Updates can be observed between transitions and instrumentation can fail. Build the final summary from the joined terminal registry. Treat live counters as operational views that should converge to the authoritative state.

## 15. A supervisor needs an admission state machine

A concurrency limit is not merely a semaphore count. The supervisor must distinguish work that is proposed, accepted, queued, started, settling, and terminal. Memory is bounded only when both accepted-but-not-started work and active work have explicit limits. Calling every producer first and then waiting on a semaphore limits execution but not promise creation, input retention, sockets, or upstream side effects.

One useful state model is:

```text
open -> closing -> joined
  |        |
  +-> cancelled
```

Each accepted task receives a stable source index before it can start. The supervisor stores a lazy producer rather than an already-running promise. Starting consumes one active permit. Settlement records exactly one typed outcome and releases the permit in `finally`. Joining closes admission, waits for every accepted task to become terminal, and reconstructs results by source index.

## 16. Failure policy determines the legal terminal set

Continue mode and fail-fast mode cannot share an undocumented result policy. In continue mode, all accepted tasks should normally start subject to capacity and produce fulfillment, domain failure, or panic-like rejection outcomes. In fail-fast mode, the first decisive failure requests cancellation; tasks not yet started become cancelled, while already-started tasks may still fulfill, fail, or observe cancellation. The precise frontier is schedule-dependent, but every accepted identity still needs one terminal outcome.

This gives an accounting equation:

```text
accepted = fulfilled + failed + cancelled + panicked
```

The categories should be mutually exclusive and complete. Live counters are useful for observation, but the final joined outcome set is authoritative. Tests should inject reverse completion, synchronous producer throw, delayed rejection, cancellation-insensitive work, and failure while the queue is full. They should compare several concurrency widths and assert the claims that are intended to remain stable: source identity, terminal accounting, and result rendering—not identical execution traces.

## Practice sequence

1. Predict the module-specific investigation cases before running the checker or Node.
2. Draw the state, ownership, queue, or lifecycle model required by this chapter.
3. Complete [the workbook](workbook.md), recording the first causal difference between your prediction and the observed result.
4. Build [Supervised Task Group](../../labs/module-38-supervised-task-group/README.md) from the starter without opening the reference.
5. Integrate the corresponding TaskHarbor increment and add evidence at the layer that owns the claim.
6. Complete the unseen transfer and explain one unsupported guarantee explicitly.
7. Compare with [the reasoned solutions](solutions.md) only after your own design passes its tests.

## Ready to continue

You are ready to leave Module 38 when you can derive its behavior from the underlying runtime model, not from remembered output; when the laboratory’s terminal paths are all tested; and when you can apply the same mechanism to a different domain without weakening ownership, boundedness, cancellation, or deterministic-reporting requirements.

## Primary references

- Node.js API documentation: <https://nodejs.org/api/>
- ECMAScript specification: <https://tc39.es/ecma262/>
- TypeScript documentation: <https://www.typescriptlang.org/docs/>

## Continue

[Module 39](../module-39-process-lifecycle-signals-cleanup-and-graceful-shutdown/index.md)
