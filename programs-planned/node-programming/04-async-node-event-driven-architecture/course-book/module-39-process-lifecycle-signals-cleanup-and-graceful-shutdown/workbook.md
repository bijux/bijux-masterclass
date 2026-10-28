# Module 39 Workbook — Process Lifecycle and Graceful Shutdown

## A. Model lifecycle states

1. Draw `new`, `starting`, `ready`, `quiescing`, `draining`, `forcing`, and `closed`.
2. Identify legal transitions and idempotent repeated operations.
3. State when the process may advertise readiness.
4. State which component owns signal listeners.

## B. Repair immediate exit

A SIGTERM handler calls `process.exit(0)`.

5. List work and output that may be truncated.
6. Replace it with stop-admission, cancel/drain, join, cleanup, and `exitCode`.
7. Decide what exit status to use if cleanup fails after all domain work succeeded.

## C. Startup rollback

A service opens a log file, connects to a database, starts a listener, then fails loading configuration.

8. Derive reverse-order cleanup.
9. Preserve the primary startup error and cleanup errors.
10. Explain why partially initialized global state is dangerous.

## D. One grace deadline

11. Use one absolute deadline across drain and force phases.
12. Explain why giving every resource its own full timeout inflates shutdown.
13. Decide what happens on a second signal.

## E. Independent laboratory

Complete [Graceful Lifecycle Harness](../../labs/module-39-graceful-lifecycle-harness/README.md). Add tests for startup failure at every acquisition point, repeated shutdown, signal removal, cleanup failure, and one resource that ignores cancellation until the force phase.

## F. TaskHarbor transfer

Keep signal handling in `main.ts`. The reusable scheduler accepts a signal but installs no global handlers. On shutdown, stop accepting a new run, abort the active run, await its complete summary, render diagnostics, set exit code, and return.

## G. Unseen transfer

Design lifecycle for a daemon with an HTTP listener, background refresh, audit writer, and temporary directory. Give an ordered shutdown plan and one grace budget.

## I. Fatal-boundary review

Compare expected task rejection, unhandled rejection caused by a floating promise, and uncaught exception inside a listener. Decide which scope should have owned each and whether the process can safely continue.

## J. Repeated-signal policy

Design behavior for first SIGTERM, second SIGTERM during drain, and SIGINT during startup. Preserve one shutdown promise. State when force begins and what remains joined.

## K. Output and exit

A CLI writes a 5 MB report to piped stdout and calls `process.exit(1)`. Explain the truncation risk and design a natural-exit boundary. Map exit codes for usage error, task failure, cancellation, and cleanup failure.

## L. Lifecycle failure tree

Startup acquires a lock file, opens a report stream, installs a signal handler, and starts a scheduler; scheduler start then fails. Write the rollback order and the result when closing the report stream also fails. Do not discard either failure.

During shutdown, the first signal begins a ten-second grace period and the second signal arrives after three seconds. Specify whether the second signal is ignored, shortens the deadline, or requests immediate abort. Write process-level tests for the selected policy.

## M. Cleanup dependency graph

Not every resource can be closed independently. A reporter may need the scheduler’s final summary; a server must stop admission before its connection tasks drain; a temporary directory must outlive files written inside it. Draw a cleanup dependency graph and derive a legal reverse-order plan rather than assuming one flat stack is sufficient.

Add a cleanup action that hangs. Show how one overall grace deadline reaches it, how escalation requests abort, and how the lifecycle report represents an incomplete cleanup without waiting forever.

## N. Operator-facing shutdown contract

Write the exact human and machine-readable output for clean drain, grace expiry with successful abort, cleanup failure, and fatal startup rollback. Assign exit statuses without conflating domain failure with infrastructure failure. Explain which information belongs in stderr, structured diagnostics, and the final lifecycle report.

## H. Defense

Explain `process.exitCode` versus `process.exit`, why `exit` cannot perform async cleanup, when `beforeExit` can fire, and why shutdown completion is a joined state transition rather than a signal callback.
