# Owned Promise Nursery

## Product

Build a parent-owned nursery for asynchronous operations. The nursery accepts lazy task producers, starts each accepted producer exactly once, converts every fulfillment or rejection into a typed terminal outcome, closes further admission when joining begins, and returns outcomes in acceptance order.

Read [Module 32](../../course-book/module-32-promises-async-functions-and-task-ownership/index.md) first.

## Public contract

```ts
export type TaskOutcome<T> =
  | { readonly id: string; readonly index: number; readonly status: 'fulfilled'; readonly value: T }
  | { readonly id: string; readonly index: number; readonly status: 'rejected'; readonly error: unknown };

export class TaskNursery<T> {
  spawn(id: string, run: () => Promise<T>): number;
  close(): void;
  join(): Promise<readonly TaskOutcome<T>[]>;
}
```

The producer is lazy input to `spawn`; callers must not pre-create its promise. `spawn` returns the stable acceptance index. `join` owns complete observation and must be safe to call repeatedly.

## Invariants

- IDs are nonempty and unique.
- A rejected producer never becomes an unhandled rejection.
- Synchronous throw and asynchronous rejection have the same terminal category.
- Beginning `join` closes admission.
- Every accepted index appears exactly once in the result.
- Result order follows acceptance order, not settlement order.
- Repeated `join` calls never start or observe work twice.
- The registry remains private and cannot be mutated by callers.

## Required tests

Cover an empty nursery, duplicate ID, mixed fast and slow fulfillment, synchronous throw, delayed rejection, join called twice, close called twice, and spawn after close. Include one test in which task completion is deliberately reversed. Do not use elapsed time as the ordering proof; use deferred promises whose resolution you control.

## Design questions

Explain where the nursery’s ownership begins and ends. Does `spawn` return before its producer settles? What does `join` prove? What does the nursery deliberately not provide—cancellation, capacity control, fail-fast policy, or task dependencies? Those omissions are acceptable only when stated.

## Lifecycle boundary test

Add a task whose main promise settles but whose owned cleanup remains pending. Decide whether `join` waits for cleanup and encode that choice in the public contract. Test a cleanup rejection separately from task rejection. This prevents “promise settled” from being confused with “owned operation complete.”

## Rejection observation proof

Install a temporary `unhandledRejection` observer in one test and demonstrate that nursery-owned rejections are already observed. Remove the observer in `finally`. The test supplements typed outcomes; it does not turn a global process event into the nursery’s normal API.

## Independent transfer

Adapt the design to own initialization of several optional plugins. Change the result policy so one required plugin failure makes the overall result unsuccessful while optional plugin failures remain reported. Do not discard the complete per-plugin outcome set.

## Implementation stages

Start with the outcome union and immutable acceptance index. Add duplicate-ID validation before producer invocation. Wrap producer start with a promise boundary that captures synchronous throw. Memoize the join promise. Only after the basic ownership proof works should you add optional cancellation as an extension; cancellation must not weaken complete joining.

## Reference comparison

When comparing with `reference/`, trace one task from `spawn` through promise creation, settlement wrapper, registry retention, aggregate join, and terminal array. Every stored field should answer a lifecycle question. Remove any field that exists only because the reference used it, and justify any alternative representation.

## Completion evidence

Provide a reverse-completion test, a synchronous-throw test, a delayed rejection test, repeated join evidence, and a design note distinguishing promise settlement from product completion. Include the intended behavior of cleanup failure even if the laboratory’s task body has no external resource.
