# Laboratory 64 — Phase Gate

This is the independent product for **Course 7, Module 64**. Read the [module chapter](../../course-book/module-64-coordination-condvars-barriers-and-phase-protocols/index.md) and complete its [workbook](../../course-book/module-64-coordination-condvars-barriers-and-phase-protocols/workbook.md) before consulting the reference implementation.

## Learning target

> How can a group wait for durable phase predicates, tolerate spurious wakeups, and enter a terminal state that releases every waiter?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a reusable phase gate with states `Created`, `Prepared`, `Running`, `Finished`, and `Cancelled`. Threads may wait until a minimum phase or a terminal cancellation. Legal transitions are monotonic and protected by one mutex plus condition variable.

## Why this laboratory exists

The lab removes queue payloads so the only difficulty is predicate-based coordination. It also includes one fixed-cohort barrier exercise to contrast phase state with rendezvous.

## Contract

Waiters loop under the mutex. Advancing to the same phase is idempotent; backward or post-terminal transitions fail. Cancellation is terminal and notifies all. Timed waits use one monotonic deadline. The barrier helper accepts a fixed participant count, joins every participant, reports worker panic, checks sum overflow, and makes no cancellation claim.

## Required milestones

1. Define the phase order and transition errors.
2. Implement `wait_until` as a predicate loop.
3. Implement deadline-based waiting without resetting the budget.
4. Implement terminal cancellation and notify-all.
5. Add a fixed-cohort barrier demonstration.

## Adversarial cases

- spurious wake simulation through irrelevant notification
- waiter starts after phase already advanced
- backward transition
- double cancellation
- timeout near deadline
- barrier participant count one
- cohort sum overflow
- waiters released by cancellation

## Evidence to produce

- predicate definitions
- transition table
- timeout budget trace
- causal waiter-release tests
- barrier participant obligations and complete join accounting

## Prohibited shortcuts

- using `if` around wait
- treating notification as state
- sleeping before notify
- resetting timeout after wake
- using a barrier when participants can cancel

## Transfer

Transfer the gate to a media pipeline. Then allow one decoder to fail before the barrier and replace the barrier phase with cancellable state plus condition-variable waiting.

## Comparing with the reference

Compare predicate loops and terminal behavior. The reference should let late waiters proceed immediately, keep timeout against one deadline, and never require a notification history to reconstruct truth.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the protocol, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer the governing question without the chapter:

> How can a group wait for durable phase predicates, tolerate spurious wakeups, and enter a terminal state that releases every waiter?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
