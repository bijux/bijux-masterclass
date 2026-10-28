# Module 39 — Process Lifecycle, Signals, Cleanup, and Graceful Shutdown

> **Question:** How does a Node.js process stop accepting work, finish what it can, release resources, and exit without hiding incomplete operations?

## Why this comes now

Module 38 established the preceding async contract. This module adds the next responsibility without discarding that earlier ownership and compatibility discipline.

## Outcomes

By the end of the module, you can:

- model startup, ready, quiescing, draining, forcing, closed, and failed lifecycle states;
- distinguish SIGINT and SIGTERM handling from beforeExit and exit events;
- prefer process.exitCode and natural shutdown over premature process.exit;
- make cleanup idempotent and order it by resource ownership;
- bound graceful drain with one deadline and force remaining resources afterward;
- preserve fatal error diagnostics without pretending unsafe continuation is reliable;

## 1. Shutdown is a state machine

A service does not move directly from running to gone. A useful lifecycle is: starting, ready, quiescing, draining, forcing if the grace period expires, and closed. Startup can fail after some resources have started, so rollback is part of the same model.

Quiescing stops admission. Draining waits for accepted work. Forcing interrupts or closes what remains. Closing releases owned resources. These phases should be observable and idempotent. A second shutdown request should join the existing shutdown rather than begin a competing cleanup sequence.

Assign one owner for each resource: listener, timer, task group, event subscription, temporary file, or context subsystem. Cleanup runs in the reverse order of dependency where appropriate.

## 2. Signals request lifecycle change

`SIGINT` commonly represents interactive interruption; `SIGTERM` commonly represents orchestrated termination. Platform support differs, especially on Windows. Signal handlers should request shutdown, not perform complex synchronous cleanup or call `process.exit` immediately.

Install handlers once, retain their function identities, and remove them when the host is disposed or tests finish. Repeated signals may escalate from graceful shutdown to forced termination according to a documented policy. Do not register a new anonymous handler for every run and leak them across tests.

## 3. process.exitCode versus process.exit

Setting `process.exitCode` allows Node to exit naturally when no referenced work remains. Calling `process.exit(code)` terminates immediately and can truncate buffered stdout or stderr, skip pending promise continuations, and abandon cleanup. It is appropriate only when the product explicitly chooses immediate termination.

A CLI main function should return a numeric status after awaited cleanup. The thin top-level module sets `process.exitCode`. Keep command logic testable without terminating the test process.

## 4. beforeExit and exit are not async cleanup hooks

The `beforeExit` event can run when the event loop would otherwise become empty and can schedule more work, but it is not emitted for every termination path. The `exit` event only permits synchronous work; asynchronous operations scheduled there will not complete. Neither replaces explicit lifecycle ownership.

Unhandled rejections and uncaught exceptions indicate a failure escaped its intended boundary. Log bounded diagnostics and begin best-effort shutdown if the program can do so safely, but do not assume arbitrary continued operation is sound. Some errors may leave state inconsistent.

## 5. One grace deadline

Graceful shutdown should compute one absolute deadline. Every resource receives the same remaining budget rather than a fresh full timeout. When the deadline expires, request force-close and still join the force operations as far as the environment permits.

A resource interface might separate `quiesce`, `drain(signal)`, and `force`. `drain` should settle when accepted work finishes. `force` should be idempotent. `close` releases final handles. The host collects failures from every phase rather than stopping after the first cleanup error and leaking the rest.

## 6. Startup rollback

If the third resource fails to start, the first two remain owned and need cleanup. Record successfully started resources and close them in reverse order. Preserve both the startup failure and any rollback failures, for example through an `AggregateError` with causes or a structured report.

Do not mark the process ready until every required resource is started and signal handlers are installed. Readiness is a product claim, not merely the moment the main function began.

## 7. Testing lifecycle behavior

Use fake resources with deferred drain promises. Start the host, request shutdown, verify quiesce order, release drains, and assert reverse close order. Test start failure rollback, repeated shutdown calls, grace expiry, force invocation, and cleanup failures. Inspect listener counts before and after to detect leaked signal handlers.

Process-level tests can spawn the CLI, wait for a readiness marker, send a signal, and assert exit status and final output. Keep these tests bounded with their own watchdog so a shutdown defect does not hang the suite.

## 8. What this changes in TaskHarbor

TaskHarbor’s CLI installs one run-level controller and handlers for supported termination signals. A signal aborts the scheduler, which stops starting new jobs, joins running jobs, renders the final terminal accounting, removes handlers, and returns an interruption exit status. A second signal can set a force flag.

The library API does not install global handlers. Process ownership belongs only in `main.ts`, preserving reuse and test isolation.

## 9. Deep case study: immediate exit after SIGTERM

A server listens for `SIGTERM`, logs “shutting down,” calls `process.exit(0)`, and loses in-flight responses, audit writes, and temporary-file cleanup. The signal handler acknowledged only receipt of a request to change lifecycle; it did not complete shutdown.

A lifecycle host translates the first signal into a transition from ready to quiescing. Admission stops. Accepted work drains or receives cancellation under one grace deadline. Remaining work is force-closed after the deadline. All owned tasks are joined, cleanup errors are recorded, signal listeners are removed, and `process.exitCode` is set. Natural exit then occurs when no referenced work remains.

## 10. Startup is a transaction

Initialization can fail after opening some resources. Register cleanup immediately after each successful acquisition. On later failure, release in reverse order and preserve both the startup error and cleanup failures. Do not install signal handlers before the lifecycle host is capable of handling them, and do not report ready until every required resource is active.

## 11. Lifecycle state and idempotence

A useful state machine is:

```text
new → starting → ready → quiescing → draining → forcing? → closed
                   ↘ startup-failed → closed
```

Repeated shutdown requests share one promise. Later signals may shorten policy, but they must not start duplicate cleanup. Every public method states which states permit it.

## 12. Uncaught exceptions and unhandled rejections

An uncaught exception or truly unhandled rejection can leave application state uncertain. A process-level handler may record diagnostics, but continuing normal service is often unsafe because invariants may already be violated. Do not use global handlers as routine error recovery. The stronger design owns expected failures at task boundaries and reserves process-fatal handling for defects or explicitly fatal conditions.

If a fatal handler initiates best-effort cleanup, keep it minimal and bounded. Avoid complex asynchronous recovery that assumes the program remains trustworthy. Production policy belongs in later observability and delivery courses, but Course 4 establishes the distinction between expected domain failure and process integrity failure.

## 13. Signal portability and repeated signals

Signal availability and behavior vary by platform. A CLI should document the environments it supports and keep signal-specific tests conditional where necessary. The first termination signal usually begins graceful shutdown. A second can escalate to force under policy, but escalation still should not duplicate cleanup or corrupt the shared shutdown promise.

## 14. Output flushing and exit status

Stdout and stderr writes can be asynchronous when connected to pipes. Rendering a final report and immediately calling `process.exit` can truncate it. Await or otherwise own important output where possible, set `exitCode`, and return. Exit status should distinguish successful completion, completed domain failure, usage/configuration failure, and lifecycle/infrastructure failure.

## 15. Lifecycle ownership begins during startup

Graceful shutdown cannot be added reliably after resources are created. Startup itself is a transaction. Every successful acquisition immediately registers an idempotent cleanup action with the lifecycle owner. If a later acquisition fails, rollback runs the already-registered actions in reverse order and preserves both the startup failure and any cleanup failures.

A practical lifecycle state machine separates:

```text
new -> starting -> running -> quiescing -> draining -> stopped
          |                         |
          +-------> failed <--------+
```

Transitions are monotonic. The second signal does not start a second shutdown; it may shorten the policy to immediate abort, but that escalation must be explicit. Repeated API calls return the same owned shutdown promise. Signal handlers request a transition and return; they do not scatter cleanup logic across callbacks.

## 16. Quiesce, drain, abort, and complete join are distinct

**Quiesce** stops accepting new work. **Drain** waits for accepted work to settle cooperatively. **Abort** requests cancellation or forcibly closes remaining resources after the grace deadline. **Complete join** waits until every owned task and cleanup action reaches a terminal state. A process is not gracefully stopped merely because its listener socket closed.

Use one absolute grace deadline for the whole shutdown tree. Giving every component a fresh timeout multiplies the total delay. Pass remaining budget to child cleanup operations. Record which components completed during drain, which required abort, and which cleanup operations failed. Set `process.exitCode` after the lifecycle result is known and allow ordinary completion to flush output; reserve immediate `process.exit` for explicitly documented emergency behavior.

Fatal boundaries require the same ownership clarity. An uncaught exception or unhandled rejection means the process may no longer satisfy its invariants. The handler can request emergency shutdown and record diagnostics, but it should not claim recovery without a product-specific proof. Tests should spawn the real CLI, send signals, create slow and cancellation-insensitive tasks, and assert exit status, bounded completion, and absence of orphaned child work.

## 17. Cleanup reports are product evidence

A shutdown routine that returns `void` forces operators to infer success from process disappearance. Prefer a typed lifecycle result containing the initiating reason, times for quiesce and completion, drained and aborted task counts, cleanup failures, and whether the grace deadline expired. The CLI can convert that result into a stable exit status and bounded diagnostic output.

This report also improves tests. Instead of sleeping and checking that the process eventually ended, assert exact resource terminal categories. Keep the report free of live handles and mutable objects so producing it does not extend the lifecycle it describes.

## Practice sequence

1. Predict the module-specific investigation cases before running the checker or Node.
2. Draw the state, ownership, queue, or lifecycle model required by this chapter.
3. Complete [the workbook](workbook.md), recording the first causal difference between your prediction and the observed result.
4. Build [Graceful Lifecycle Harness](../../labs/module-39-graceful-lifecycle-harness/README.md) from the starter without opening the reference.
5. Integrate the corresponding TaskHarbor increment and add evidence at the layer that owns the claim.
6. Complete the unseen transfer and explain one unsupported guarantee explicitly.
7. Compare with [the reasoned solutions](solutions.md) only after your own design passes its tests.

## Ready to continue

You are ready to leave Module 39 when you can derive its behavior from the underlying runtime model, not from remembered output; when the laboratory’s terminal paths are all tested; and when you can apply the same mechanism to a different domain without weakening ownership, boundedness, cancellation, or deterministic-reporting requirements.

## Primary references

- Node.js API documentation: <https://nodejs.org/api/>
- ECMAScript specification: <https://tc39.es/ecma262/>
- TypeScript documentation: <https://www.typescriptlang.org/docs/>

## Continue

[Module 40](../module-40-integrated-event-driven-architecture-and-independent-change/index.md)
