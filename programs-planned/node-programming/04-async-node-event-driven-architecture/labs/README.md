# Course 4 Independent Laboratories

The ten labs isolate one asynchronous mechanism at a time. Each has a compile-clean starter, a complete reference, and tests. Build from the contract rather than treating the reference as a patch.

| Module | Laboratory | Primary proof |
|---:|---|---|
| 31 | [Event Loop Observatory](module-31-event-loop-observatory/README.md) | When does asynchronous Node.js work actually run, what ordering can you rely on, and how can one callback prevent every other operation from making progress? |
| 32 | [Owned Promise Nursery](module-32-owned-promise-nursery/README.md) | Who owns an asynchronous operation after it has started, and how does the program prove that every promise eventually becomes an observed outcome? |
| 33 | [Deadline Budget](module-33-deadline-budget/README.md) | How can asynchronous work stop cooperatively without pretending that cancellation rewinds effects that already happened? |
| 34 | [Typed Event Hub](module-34-typed-event-hub/README.md) | How can events expose meaningful observations without becoming an untyped second state machine or a source of listener leaks and hidden failures? |
| 35 | [Deterministic Scheduler](module-35-deterministic-scheduler/README.md) | How do you make time-dependent behavior testable and honest when timers provide delayed eligibility rather than exact execution? |
| 36 | [Bounded Async Queue](module-36-bounded-async-queue/README.md) | How do you represent a sequence whose next value arrives asynchronously while preserving demand, cleanup, cancellation, and bounded memory? |
| 37 | [Correlation Context](module-37-correlation-context/README.md) | How can diagnostic context follow an asynchronous operation without turning ambient state into hidden domain authority? |
| 38 | [Supervised Task Group](module-38-supervised-task-group/README.md) | How does a parent scope account for every child operation while limiting concurrency and making failure policy explicit? |
| 39 | [Graceful Lifecycle Harness](module-39-graceful-lifecycle-harness/README.md) | How does a Node.js process stop accepting work, finish what it can, release resources, and exit without hiding incomplete operations? |
| 40 | [Event-Driven Job Engine](module-40-event-driven-job-engine/README.md) | Can you evolve a complete asynchronous Node.js system while preserving schedule, ownership, cancellation, event, context, boundedness, and shutdown contracts together? |

## Method

Read the module chapter, write the state or ownership model, implement the starter, add adversarial tests, and only then inspect the reference. Compare invariants and failure handling rather than line count.
