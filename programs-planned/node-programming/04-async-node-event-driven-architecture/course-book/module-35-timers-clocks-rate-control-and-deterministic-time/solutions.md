# Module 35 Reasoned Solutions — Timers, Clocks, and Rate Control

## A. Clock selection

Audit timestamps use wall time because humans and persisted records need calendar meaning. Deadlines and elapsed durations use monotonic time. Deterministic event ordering uses a sequence counter. Tests use injected manual time. A zero-delay timer means no earlier than the threshold and only when the event loop reaches the timer phase; it is not an appointment.

## B. Periodic work

`setInterval` can make later ticks eligible while work remains active. Fixed-delay scheduling awaits completion, then sleeps the delay. Fixed-rate scheduling tracks absolute next-start deadlines and must decide whether to skip, coalesce, or catch up missed ticks. Catch-up bursts often worsen overload. `unref` is appropriate only when the timer should not be the sole reason the process remains alive.

## C. Policy distinctions

Debounce coalesces a burst into one action after quiet. Throttle permits at most a configured frequency. Rate limiting rejects or delays to protect capacity. Polling observes external state repeatedly. Retry repeats a failed operation under eligibility and budget rules. The answer must state ownership of pending timers and queued calls.

## D. Manual clock

The clock stores sleepers ordered by deadline and creation ID. `advanceBy` moves monotonic time, removes due sleepers from internal storage, removes abort listeners, then resolves them. `pollUntil` checks, computes `remaining`, throws when no time remains, and sleeps for `min(interval, remaining)`. Attaching rejection assertions before advancing avoids tests that briefly create unhandled rejections.

## E. TaskHarbor and transfer

TaskHarbor uses the clock for deadlines and diagnostic durations. Terminal category and source order do not depend on measured milliseconds. For the cache, wall time may appear in metadata, while monotonic time controls expiry. One refresh promise can be shared by concurrent callers; shutdown aborts and joins it. Manual time drives expiry and refresh without real sleeps.

## F. Retry and timer solutions

The retry schedule is derived from attempt state and one absolute deadline. Every attempt consumes time; backoff is capped and jittered through an injected deterministic function in tests. Before sleeping or starting another attempt, recompute remaining budget. If no useful budget remains, return a deadline terminal state rather than starting work guaranteed to exceed the contract.

A timer handle is owned together with the promise or callback waiting on it. Clearing only the handle can leave a promise pending forever; cleanup must settle or reject the waiter as well. `unref` is a process-liveness choice, not cancellation.

Manual-clock tests own arithmetic, equal-deadline order, and abort cleanup. Real integration tests own Node phase interaction, process liveness, and actual timer-handle behavior. The fake clock should not pretend to be the whole event loop.

## G. Temporal-policy answers

Fixed delay after completion prevents overlap but drifts relative to wall time. Fixed rate with skip preserves an approximate cadence while dropping ticks during long work. One-pending-run bounds backlog at one and runs again immediately after completion. Overlap permits concurrent executions and therefore requires a separate capacity and state-consistency proof. The correct choice follows the product policy, not the name “interval.”

One overall retry deadline is computed once from a monotonic clock. Before each delay and attempt, derive remaining budget; do not allocate a fresh timeout. A deterministic jitter source makes exact tests possible. Timer handles are disposed when the attempt settles. If an operation ignores cancellation, the wrapper may stop waiting but cannot claim that underlying work stopped.

## H. Timer-storm answers

One timeout per queued job retains one callback closure, handle, deadline value, and often the job context. Finishing jobs early still requires disposing every handle. An ordered deadline heap plus one active timer reduces host handles but adds heap maintenance, stale-entry handling, and one rescheduling authority. The simpler design remains appropriate when the documented concurrent timer count is small.

`unref` changes whether the handle alone keeps the process alive; it does not cancel the callback. Disposal prevents future invocation. Normal settlement transfers the timer to terminal state and should remove application references. An unrefed timer can still fire while another referenced resource keeps the process running, so unref is not a cleanup mechanism.
