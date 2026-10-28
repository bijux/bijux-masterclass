# Module 39 Reasoned Solutions — Process Lifecycle and Graceful Shutdown

## A. States

Readiness begins only after all required resources are active. Quiescing stops admission. Draining waits for accepted work. Forcing cancels or closes work that exceeded the grace period. Closed means all owned handles and tasks are terminal. The executable boundary owns process signals because a reusable library cannot assume global lifecycle authority.

## B. Exit behavior

`process.exit` can truncate output and bypass pending asynchronous cleanup. The handler should initiate an idempotent shutdown promise, not perform the whole operation inline. After cleanup, set `process.exitCode`; natural event-loop completion exits. Cleanup failure normally produces a nonzero result even if domain work succeeded because the process cannot claim a clean stop.

## C. Startup rollback

Register a disposer immediately after each successful acquisition and execute in reverse order on failure. Preserve the startup error as primary and attach cleanup errors rather than replacing it. Avoid publishing partially initialized components through globals; keep them inside the startup scope until ready.

## D. Deadline

Compute one monotonic deadline and pass remaining time to each phase. Independent full timeouts can multiply shutdown duration. A second signal may request immediate force according to policy, but repeated calls should share the same shutdown promise and cleanup actions.

## E. TaskHarbor and transfer

`main.ts` installs and removes listeners. The scheduler remains reusable and receives only a signal. The daemon shutdown order is listener quiescence, background refresh cancellation, accepted request drain, audit flush, temporary cleanup, complete joins, and exit status. Dependencies may adjust exact order, but each owned resource must have one terminal proof.

## F. Fatal and exit solutions

Expected task rejection belongs to the task owner and becomes a typed outcome. A floating promise causing unhandled rejection indicates missing ownership. An uncaught listener exception indicates an event-boundary policy failure. Global handlers can record fatal context but are not substitutes for restoring unknown invariants; normal service should not continue casually.

The first signal starts quiescence. The second can request force while reusing the same shutdown state and promise. SIGINT during startup triggers rollback of acquired resources. Force changes how remaining work is stopped, not whether it is joined and accounted for.

Piped output may not flush before immediate exit. Write through an owned output path, await completion where the API permits, set `process.exitCode`, and return. Usage/configuration errors typically differ from completed domain failure; cleanup failure produces nonzero infrastructure status.

## G. Lifecycle and rollback answers

Rollback runs scheduler cleanup if startup crossed that ownership point, then removes the signal handler, closes the report stream, and releases the lock file in reverse acquisition order. When scheduler start and stream close both fail, preserve the startup failure as primary and the cleanup failure as structured secondary evidence. Discarding cleanup failure hides a leak; replacing startup failure loses the cause of rollback.

The selected repeated-signal policy must be explicit. A common policy starts graceful drain on the first signal and escalates to immediate abort on the second while still joining owned tasks. Process tests spawn the CLI, wait for a ready marker, send signals, and assert bounded exit, status, terminal report, and no lingering child. `process.exitCode` allows ordinary flushing; `process.exit()` is not the default cleanup mechanism.

## H. Cleanup-graph answers

Cleanup order follows dependency edges: quiesce the server, drain connections, finalize the scheduler summary, flush the reporter, then release enclosing temporary storage. A flat reverse stack works only when acquisition order accurately represents all dependencies. The design record should name exceptions.

One absolute grace deadline wraps the graph. A hanging cleanup receives cancellation or is abandoned only according to explicit policy; the lifecycle report marks it incomplete and preserves preceding failures. Starting a fresh timeout for every cleanup can make total shutdown unbounded.

## I. Operator-contract answer

Clean drain reports success and exit status zero. Grace expiry is a degraded shutdown even when abort succeeds and should be separately classified. Cleanup failure and startup rollback preserve causes and use infrastructure-failure status. Human stderr remains bounded; structured diagnostics carry detailed categories; the lifecycle result remains authoritative.
