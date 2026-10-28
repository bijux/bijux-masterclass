# Course 4 Final Review — Reasoned Solutions

These notes describe the causal standard for a strong answer. They are not a script.

## Scenario 1

The asynchronous file read is a host wait. JSON parsing and validation are synchronous JavaScript regions after resumption. A cooperative repair bounds input, validates in chunks, and yields through an ordinary phase. Streaming becomes appropriate when the input should not be retained whole; workers become appropriate when CPU cost remains too high. The audit writer needs a bounded owner and a join at normal shutdown.

## Scenario 2

`Promise.any` proves that one input fulfilled. It does not cancel or join losers. A supervisor gives every attempt a controller, aborts losers after a winner, and awaits all terminal cleanup. For effects, timeout or lost response leaves commit ambiguous; retry requires idempotency or reconciliation.

## Scenario 3

Nested fresh timeouts can sum beyond the caller’s total. One monotonic deadline is inherited; each helper computes remaining time and may impose only a smaller limit. Abort reasons remain typed. Invariant-restoring cleanup may continue under a separately bounded owner after the response budget expires.

## Scenario 4

Mutable event payloads give listeners write authority. Async listeners create unowned promises. Retained captures create leaks. Publish immutable snapshots after authoritative transitions, return disposers, define reentrancy and observer-failure policy, and use a bounded joined queue for mandatory async observation.

## Scenario 5

`setInterval` supplies recurring eligibility and can overlap work. A poller waits after each attempt or uses explicit fixed-rate skip policy. One manual clock controls `now` and sleep; tests advance exact boundaries. `unref` means the timer does not keep the process alive by itself, not that it stops existing.

## Scenario 6

The EventEmitter remains push driven; the array can grow without bound. A bridge needs finite capacity and overflow semantics. Normal close drains, failure rejects, abort removes waiters, and early return detaches the source. Broadcast requires per-subscriber delivery state and is not obtained by adding a second consumer to a queue.

## Scenario 7

Tenant authorization is explicit capability, not ambient diagnostics. AsyncLocalStorage context follows resources created under its scope and can be retained by long-lived resources. Keep stores small and immutable. Diagnostics channels use stable names and optional subscribers. Deferred interleaving tests prove isolation.

## Scenario 8

Capacity must gate producer invocation. A supervisor owns a running set, starts lazily, captures every terminal state, and joins even under fail-fast. Continue mode admits independent work; fail-fast stops new admission and cancels siblings. Indexed outcomes provide exact accounting and deterministic presentation.

## Scenario 9

`process.exit` can truncate work. The executable transitions ready → quiescing → draining → forcing if needed → closed, under one deadline. Startup acquires resources transactionally and rolls back in reverse order. Cleanup failure normally requires nonzero exit because clean shutdown was not achieved.

## Scenario 10

Priority affects only the simultaneously ready set and uses source order as tie-breaker. Retry adds attempt state, classification, backoff, and one inherited deadline. It must not duplicate unsafe effects. Both changes update validation, types, observations, output, tests, and compatibility. Existing graph and accounting invariants remain explicit regression properties.

## Independent construction standard

The campaign runner has one parent owner, finite admission and active capacity, cooperative cancellation, typed immutable events, small diagnostic context, one terminal outcome per accepted recipient, and a lifecycle host that stops admission before drain. Final order is based on stable campaign/recipient identity rather than callback completion.
