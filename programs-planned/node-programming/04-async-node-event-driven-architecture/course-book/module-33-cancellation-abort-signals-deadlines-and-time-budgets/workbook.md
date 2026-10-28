# Module 33 Workbook — Cancellation, Abort Signals, Deadlines, and Time Budgets

## A. Classify cancellation outcomes

For each scenario, state what is known and what remains ambiguous.

1. A timer promise is aborted before its threshold.
2. A file write is aborted after some bytes may have reached the operating system.
3. An HTTP request times out after the server may have committed a payment.
4. A queued task is cancelled before its producer is invoked.

Do not use “rolled back” unless a separate transaction proves it.

## B. Compose causes

Design a child operation that may stop because of user cancellation, process shutdown, fail-fast policy, or a local deadline.

5. Which component owns each controller?
6. How will the child preserve the first decisive reason?
7. What should happen when the parent signal is already aborted at entry?
8. How are listeners removed after success, failure, or cancellation?

## C. Derive one absolute budget

A top-level command has 2 seconds. It performs three attempts with backoff and calls a helper that currently starts its own 1-second timeout.

9. Show how nested relative timeouts can exceed 2 seconds.
10. Rewrite the policy around one monotonic deadline.
11. Decide whether cleanup is inside or outside the user-visible budget and defend the choice.

## D. Construct `withinBudget`

Implement a helper that accepts a finite nonnegative budget, an operation receiving an `AbortSignal`, and an optional parent signal. Preserve the original abort reason, clear timers in `finally`, and document that a noncooperative operation may continue after the helper stops waiting.

Test pre-abort, success, operation rejection, deadline, parent abort, and listener/timer cleanup. Use an injected clock or controlled deferred operation rather than random sleeps.

## E. Independent laboratory

Complete [Deadline Budget](../../labs/module-33-deadline-budget/README.md). Add an ambiguous-commit scenario to the design record and specify the idempotency or reconciliation mechanism a real remote effect would require.

## F. TaskHarbor transfer

Give the run one controller and each task a derived controller. Distinguish `timed-out` from `cancelled`. A dependency on either terminal state becomes blocked. Add tests for a pre-aborted run, task timeout, run timeout, and cleanup after normal success.

## G. Unseen transfer

Design cancellation for a three-stage document export: render, write temporary file, replace destination. Mark every checkpoint, committed effect, cleanup action, and retry implication.

## I. Race analysis

A task has a 100 ms local deadline. At almost the same time, fail-fast aborts the run. Design tests that accept either physical ordering but require one immutable terminal cause. Then design a deterministic policy in which an already-observed task timeout takes precedence over later run cancellation.

## J. Resource-gap exercise

A function awaits `open`, then awaits `registerHandle(handle)`, then enters `try/finally`. Show the leak window. Redesign so cleanup ownership is established synchronously after `open` returns. Explain whether `registerHandle` belongs before or after the owner is established.

## K. API contract writing

Write a cancellation section for a hypothetical `uploadFile(path, { signal })`. It must distinguish local read cancellation, request transmission, remote commit ambiguity, cleanup, and retry safety. Avoid promising that abort removes already uploaded bytes.

## L. Cancellation precedence matrix

Analyze four near-simultaneous races: parent abort versus local timeout, successful completion versus abort, acquisition completion versus abort, and operation failure versus cleanup failure. Define the terminal result for each ordering and state whether the public API preserves one cause, a cause chain, or a structured aggregate.

Write tests with controlled deferred promises and a manual clock. Random sleeps are not accepted. Your evidence must show listener removal and timer disposal on every terminal path.

## M. Deadline propagation exercise

An HTTP-like operation performs lookup, validation, execution, and report writing under a two-second product deadline. Allocate one absolute deadline rather than four independent timeouts. For each phase, state when remaining budget is checked, whether the phase can be interrupted, and what result is returned when the deadline expires during non-cancellable work.

Design a `CancellationError` shape that preserves a machine-readable reason, the originating signal or policy, and an optional cause. Explain why every abort should not be normalized to the same message when callers must distinguish parent shutdown from local timeout.

## H. Defense

Explain why abort is one-shot, why a signal is observation rather than authority, why timeout is not rollback, and why `Promise.race` alone is not cancellation.
