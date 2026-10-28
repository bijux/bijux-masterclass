# Supervised Task Group

## Product

Build a finite-batch supervisor that invokes lazy task producers under a concurrency limit and returns one source-ordered terminal outcome per accepted task. Support continue and fail-fast policies without orphaning running work.

Read [Module 38](../../course-book/module-38-task-supervision-failure-policies-and-bounded-concurrency/index.md).

## Public contract

Each task has a stable ID and producer `(signal) => Promise<T>`. The runner accepts a positive concurrency limit, failure policy, and optional parent signal. Outcomes distinguish fulfillment, rejection, and cancellation and retain source identity.

## Capacity and ownership

Do not construct all task promises before capacity is available. The supervisor owns every promise from invocation until terminal settlement. The running set never exceeds the limit. The source batch is finite; if adapting the design to a service, define a separate admission bound for waiting inputs.

## Failure policies

Continue mode admits independent tasks after failure. Fail-fast stops new admission, requests cancellation of running siblings, joins them, and marks untouched inputs cancelled. Neither policy may return with an owned promise still running.

## Required tests

Use deferred tasks to prove the concurrency bound and reverse completion order. Cover zero tasks, invalid limit, duplicate IDs if IDs are enforced, synchronous throw, delayed rejection, pre-abort, mid-run abort, fail-fast with two active siblings, and exact terminal accounting.

## Accounting proof

After join, verify:

```text
accepted = fulfilled + rejected + cancelled
```

No source index may be missing or duplicated. A live running counter is diagnostic only.

## Admission and terminal-accounting evidence

The starter must accept lazy producers rather than promises. Measure producer invocation count before and after capacity becomes available. Add tests for queue saturation, duplicate IDs, synchronous throw, delayed rejection, cancellation-aware and cancellation-insensitive tasks, and repeated join.

For both continue and fail-fast modes, submit a terminal accounting table. Results must be indexed by acceptance order. A wall-clock trace may be included for explanation, but tests must not depend on one completion schedule.

## Fairness extension

Add one documented fairness rule and test it under a sustained stream of preferred work. The rule must not increase active concurrency beyond the configured limit or make final result identity depend on completion order.

## Blocked-admission evidence

Fill the queue, start another submission, then close the supervisor. Prove the blocked submission terminates with rejection-before-commit and does not appear in the joined accepted-outcome table.

## Independent transfer

Adapt the supervisor to a migration runner with dependencies between migration groups. Specify whether a failed group blocks dependents while unrelated groups continue, and how rollback limitations are represented.

## Implementation stages

Start with finite source-indexed tasks and a running map. Add lazy invocation and source-order outcomes. Introduce continue mode, then fail-fast cancellation and complete joining. Add live metrics only after the terminal accounting proof works.

## Review questions

What bounds active work and waiting input? Can priority starve a class? When is a capacity slot released? How are untouched tasks classified after fail-fast? Which data is the final authority?

## Completion evidence

Provide controlled reverse-completion tests, a concurrency trace, a fail-fast state diagram, the accounting equation, and one fairness analysis for adapting the runner to an unbounded service.
