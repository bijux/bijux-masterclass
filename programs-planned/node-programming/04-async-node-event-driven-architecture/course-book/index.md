# Async Node.js and Event-Driven Architecture

A synchronous program can often be explained by following one stack. An asynchronous Node.js program needs a richer model: which callback is running, which work is merely ready, which promise owns a result, which scope owns completion, what can be cancelled, where demand accumulates, which context follows an operation, and how the process proves that accepted work is terminal before exit.

Course 4 builds that model without hiding behind a framework. It begins with event-loop scheduling, then makes promise ownership explicit. Cancellation and deadlines add cooperative stop semantics. Event contracts and async iterables add observation and sequence boundaries. Injected clocks make time testable. AsyncLocalStorage and diagnostics add correlation without becoming domain authority. Supervision adds finite task ownership. Process lifecycle closes the tree. TaskHarbor integrates all ten modules in one dependency-aware orchestrator.

## Entry standard

Start only when you can independently:

- build and test a strict TypeScript ESM package;
- validate `unknown` input before trusting it;
- distinguish JavaScript runtime behavior from TypeScript declarations;
- reason through closure capture, object identity, private state, and explicit disposal;
- design generic public library contracts;
- inspect emitted declarations and package exports;
- make a cross-layer library change without bypassing runtime validation.

If those skills are unstable, repair them in Courses 1–3 first. Async code amplifies unclear boundaries; it does not repair them.

## The course reasoning ledger

For every asynchronous operation, record:

| Dimension | Question |
|---|---|
| admission | which component is allowed to start the work? |
| promise ownership | which scope retains and eventually joins its result handle? |
| suspension | at which awaits, timers, events, or queue waits can other work observe state? |
| state authority | which component owns ready, running, and terminal state? |
| cancellation | who may request stop, what cause is preserved, and what may already be committed? |
| time | which clock and deadline govern the operation? |
| observation | which events or diagnostics report state without owning it? |
| capacity | what bounds active work, queued work, listeners, timers, or retained history? |
| lifecycle | what cleanup and join must occur before the parent or process returns? |
| determinism | which final outputs remain stable despite schedule variation? |

## The ten-module progression

1. [Event Loop, Scheduling, Fairness, and Blocking](module-31-event-loop-scheduling-fairness-and-blocking/index.md)
2. [Promises, Async Functions, and Task Ownership](module-32-promises-async-functions-and-task-ownership/index.md)
3. [Cancellation, Abort Signals, Deadlines, and Time Budgets](module-33-cancellation-abort-signals-deadlines-and-time-budgets/index.md)
4. [EventEmitter and Typed Event Contracts](module-34-event-emitter-and-typed-event-contracts/index.md)
5. [Timers, Clocks, Rate Control, and Deterministic Time](module-35-timers-clocks-rate-control-and-deterministic-time/index.md)
6. [Async Iterables, Generators, and Pull-Based Sequences](module-36-async-iterables-generators-and-pull-based-sequences/index.md)
7. [Async Context, Correlation, and Diagnostic Boundaries](module-37-async-context-correlation-and-diagnostic-boundaries/index.md)
8. [Task Supervision, Failure Policies, and Bounded Concurrency](module-38-task-supervision-failure-policies-and-bounded-concurrency/index.md)
9. [Process Lifecycle, Signals, Cleanup, and Graceful Shutdown](module-39-process-lifecycle-signals-cleanup-and-graceful-shutdown/index.md)
10. [Integrated Event-Driven Architecture and Independent Change](module-40-integrated-event-driven-architecture-and-independent-change/index.md)

## How to use the material

Read the chapter before opening the lab reference. Predict investigation outcomes before type checking or execution. In every debugging exercise, preserve the hard requirement; do not “repair” ownership by ignoring a promise, fairness by adding a random sleep, cancellation by calling it rollback, or shutdown by forcing process exit. Complete the independent lab, then transfer the mechanism into TaskHarbor. Finish each day by reconstructing the model without notes.

## Supporting surfaces

- [Observable outcomes](outcomes.md)
- [Ten-day study plan](study-plan.md)
- [Async reference desk](reference.md)
- [TaskHarbor engineering guide](capstone.md)
- [Final review](final-review.md)
- [Final review solutions](final-review-solutions.md)
