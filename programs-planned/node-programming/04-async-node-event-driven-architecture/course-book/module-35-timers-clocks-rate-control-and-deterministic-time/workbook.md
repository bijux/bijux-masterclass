# Module 35 Workbook — Timers, Clocks, and Rate Control

## A. Classify time

1. Choose wall, monotonic, logical, or manual time for an audit timestamp, a request deadline, deterministic event order, and a unit test.
2. Explain why one `Date.now()` abstraction is not sufficient for all four.
3. State what a zero-delay timer actually guarantees.

## B. Diagnose periodic overlap

A refresh uses `setInterval` but can run longer than the interval.

4. List the possible overlap and backlog behaviors.
5. Design fixed-delay nonoverlapping refresh.
6. Design fixed-rate refresh that skips missed ticks.
7. Decide whether a pending timer should keep the process alive.

## C. Distinguish policies

For search suggestions, API quota, health polling, and transient network failure, choose among debounce, throttle, rate limit, poll, and retry. State what happens to calls that arrive while the policy is active.

## D. Construct a manual clock

Implement `now`, `sleep`, and `advanceBy`. Sleepers at the same deadline must resolve in creation order. Abort removes a sleeper. Advancing time must not execute arbitrary user callbacks synchronously inside internal state mutation; settle sleepers after the due set is isolated.

Use the clock to implement `pollUntil` under one absolute deadline. The final sleep must use only remaining time.

## E. Independent laboratory

Complete [Deterministic Scheduler](../../labs/module-35-deterministic-scheduler/README.md). Add exact-boundary, same-deadline ordering, pre-abort, and no-pending-sleeper-after-terminal tests.

## F. TaskHarbor transfer

Inject a `Clock` into task duration, task timeout, run timeout, and scheduler tests. Clarify which output is semantic and which duration is diagnostic. A manual clock must not change task ordering policy.

## G. Unseen transfer

Design an expiring cache with refresh-ahead. Specify wall timestamps versus monotonic expiry, overlapping refresh policy, request behavior during refresh, shutdown cleanup, and deterministic tests.

## I. Retry-budget design

Design retry for a transient operation under a 900 ms total budget, at most four attempts, base delay 50 ms, factor 2, cap 200 ms, and injected jitter ±20%. Show one possible schedule and demonstrate how remaining budget truncates the final delay or attempt.

## J. Timer-resource review

For debounce, periodic refresh, retry, and shutdown grace, identify the timer owner, cleanup point, and `ref`/`unref` policy. Give one failure mode caused by clearing a timer but forgetting an associated promise waiter.

## K. Fake-clock scope

List which claims belong in manual-clock unit tests and which require a real Node integration test. Explain why emulating next-tick and microtask queues inside `ManualClock` would make it a misleading second scheduler.

## L. Temporal-policy derivation

Design a serial periodic poller with a one-second target interval and work that may take longer than one second. Compare fixed-delay-after-completion, fixed-rate-with-skip, fixed-rate-with-one-pending-run, and overlapping execution. For each, draw the state machine, bound the number of owned timers, and explain cancellation behavior.

Convert a three-attempt retry policy into one absolute deadline. Include deterministic jitter derived from an injected source and show how remaining budget limits both delay and attempt execution.

## M. Timer-storm analysis

A service schedules one timeout per queued job and receives 100,000 jobs. Derive the retained state and callback cost even when most jobs finish before their timeout. Redesign the system with one ordered deadline structure and one next-deadline timer. State what complexity is introduced and when the simpler per-operation timer remains the better engineering choice.

Create a table for `ref`, `unref`, disposal, and normal timer settlement. Explain how each affects process liveness and resource ownership. Include the case where an unrefed timer still fires because another resource keeps the process alive.

## N. Clock-interface review

Design the smallest clock interface required by three clients: a timeout wrapper, a retry loop, and a periodic scheduler. Decide whether they need wall time, monotonic time, scheduled callbacks, sleep promises, or all four. Reject a single oversized interface when it allows tests to fake only half of the temporal contract.

For each client, name the timer owner and terminal cleanup path.

## H. Defense

Explain timer eligibility, drift, `ref`/`unref`, absolute deadlines, and why a fake clock that only replaces `Date.now` cannot control promise-based sleeps.
