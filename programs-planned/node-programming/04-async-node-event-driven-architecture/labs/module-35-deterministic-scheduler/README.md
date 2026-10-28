# Deterministic Scheduler

## Product

Build a manual monotonic clock and a deadline-bounded polling helper. The design must make timer state inspectable and tests deterministic without patching global timers.

Read [Module 35](../../course-book/module-35-timers-clocks-rate-control-and-deterministic-time/index.md).

## Public contract

```ts
export interface Clock {
  now(): number;
  sleep(milliseconds: number, signal?: AbortSignal): Promise<void>;
}

export class ManualClock implements Clock {
  advanceBy(milliseconds: number): void;
  pending(): number;
}
```

`pollUntil` accepts a check function, interval, absolute deadline, clock, and optional signal.

## Invariants

Time is monotonic and cannot advance by a negative or nonfinite amount. Invalid sleeps reject before registration. Equal-deadline sleepers settle in registration order. Abort removes the sleeper exactly once. Closing one sleeper does not disturb others. The poller never sleeps beyond its remaining budget and never creates an extra full interval at the deadline.

## Required tests

Cover zero-duration sleep, equal deadlines, staggered deadlines, pre-abort, abort after registration, exact polling deadline, successful check before deadline, exception from the check function, and `pending() === 0` after every terminal path. Attach expected-rejection observers before advancing the clock so the test itself does not create an unhandled-rejection interval.

## Rate-control analysis

Add a short design note comparing how this clock could support debounce, throttle, rate limiting, and retry. Do not implement all four; explain the different state each would need.

## Clock fidelity and resource ownership

The manual clock must preserve deadline ordering, stable tie-breaking, cancellation, and monotonic advancement. It must reject backward time movement. A callback scheduled by another callback at the current instant needs an explicit policy: run in the same advance cycle or await another advance. State and test the choice.

Track every timer handle as an owned resource. Completion, rejection, and cancellation must remove obsolete timers. Compare the manual-clock result with a small real-timer smoke test without using the smoke test as exact timing evidence.

## Deadline scheduler extension

As an extension, replace multiple pending timeout handles with one next-deadline timer and an ordered in-memory schedule. Compare implementation complexity, retained closures, cancellation behavior, and testability with the original design. Do not assume the extension is automatically superior.

## Rate-policy comparison artifact

Submit traces for debounce, throttle, serial interval, and overlapping interval under the same arrival sequence. Explain which differences are contractual and which timestamps are merely observations of the real clock.

## Independent transfer

Use the clock to implement a lease with expiry and explicit renewal. Specify whether renewal is allowed exactly at the deadline, how cancellation interacts with waiting clients, and which time is persisted for human diagnostics.

## Implementation stages

Store sleepers in a deterministic ordered structure. Establish exact abort-listener ownership. Separate advancement of internal time from settlement of extracted due sleepers. Build `pollUntil` on the interface. As an extension, add retry with injected jitter and one absolute deadline.

## Review questions

Which clock is monotonic? What happens at exactly the deadline? Can a cleared timer leave a promise unresolved? Does an unrefed timer still fire? Which ordering is guaranteed for equal manual deadlines?

## Completion evidence

Provide state-transition tests with no real sleeps, a pending-handle count after every terminal path, and one integration note describing what the manual clock deliberately does not model.
