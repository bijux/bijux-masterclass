# Module 35 — Timers, Clocks, Rate Control, and Deterministic Time

> **Question:** How do you make time-dependent behavior testable and honest when timers provide delayed eligibility rather than exact execution?

## Why this comes now

Module 34 established the preceding async contract. This module adds the next responsibility without discarding that earlier ownership and compatibility discipline.

## Outcomes

By the end of the module, you can:

- distinguish wall-clock timestamps, monotonic elapsed time, timer thresholds, and schedule policy;
- explain ref and unref behavior for timer handles;
- design delay, deadline, debounce, throttle, and rate-limit behavior from explicit contracts;
- inject a clock and sleeper so tests advance time deterministically;
- avoid nested timeout inflation by propagating one deadline;
- test boundary instants and cleanup without real sleeps;

## 1. Time has several meanings

A timestamp answers “when according to a civil clock?” Elapsed time answers “how long did this take?” A timer answers “make this callback eligible no earlier than this threshold.” A schedule policy answers “when should the product attempt this operation?” Treating all four as `Date.now()` creates brittle logic.

Civil clocks can jump because of synchronization or manual adjustment. Use them for user-visible dates and persisted timestamps. Use a monotonic clock for elapsed budgets and latency. Node exposes monotonic measurements through `performance.now()` and high-resolution process APIs. Persisting a monotonic value is meaningless across process restarts because its origin is process-local.

Name the concept in the interface. `createdAtEpochMs` is clearer than `time`. `remainingBudgetMs` is different from `retryAfterMs`.

## 2. Timers establish lower bounds, not appointments

`setTimeout(callback, 50)` means the callback cannot become eligible before approximately fifty milliseconds have elapsed. It may run later because the event loop is blocked, the process is suspended, or other callbacks run first. An interval can drift when callbacks take time. A production design should decide whether it wants fixed delay after completion, fixed target times, skipped missed ticks, or catch-up execution.

Never use a timer callback’s observed lateness as proof that the host clock changed. The event loop may simply have been busy. Similarly, a deadline timer firing does not interrupt synchronous code already running; cancellation is observed at the next cooperative point.

## 3. Ref, unref, and process liveness

Node timer handles normally keep the event loop alive. Calling `unref()` means the timer alone should not prevent process exit. This is a lifecycle decision, not a performance optimization. A background cache cleanup timer may be unrefed because unfinished cleanup is acceptable at natural process exit. A timer enforcing a critical shutdown deadline should remain referenced while shutdown is active.

Do not scatter `unref()` calls. The component that owns process-liveness policy should decide whether incomplete timed work may be abandoned. Tests should verify both the timer behavior and the documented process-lifetime contract where feasible.

## 4. Debounce, throttle, rate limit, and retry are different

Debounce waits for a quiet period and collapses repeated triggers into one later action. Throttle limits how often an action may run while triggers continue. A rate limiter controls admitted work over a window or token budget. Retry schedules additional attempts after failure. These mechanisms have different state and cancellation semantics.

For each, specify leading or trailing behavior, what happens to superseded callers, whether results are shared, whether cancellation rejects waiting callers, and how shutdown handles pending work. A ten-line utility copied from the internet often leaves these questions implicit.

Retries also need an overall deadline and idempotency policy. Course 4 concentrates on the scheduler mechanics; later service courses add remote side effects and retry safety.

## 5. Inject the clock, not the date format

A narrow testable boundary might be:

```ts
interface Clock {
  now(): number;
  sleep(milliseconds: number, signal?: AbortSignal): Promise<void>;
}
```

Production uses a monotonic source and abortable timers. Tests use a manual clock with a priority queue of sleepers. Advancing the manual clock resolves every sleeper whose deadline is now due, in deterministic insertion order for equal deadlines. The manual clock should not automatically flush arbitrary promise microtasks; tests should explicitly await the operation after advancing.

Keep formatting of civil timestamps outside the scheduling interface. A clock that returns formatted strings cannot support arithmetic safely.

## 6. One deadline through nested operations

A parent operation should compute one deadline. Children receive the remaining budget or the deadline itself. If a child needs a stricter cap, it uses the earlier of the parent deadline and its local maximum.

```ts
class Budget {
  constructor(
    readonly deadline: number,
    private readonly clock: Pick<Clock, 'now'>,
  ) {}

  remaining(): number {
    return Math.max(0, this.deadline - this.clock.now());
  }

  child(maximum: number): Budget {
    return new Budget(
      Math.min(this.deadline, this.clock.now() + maximum),
      this.clock,
    );
  }
}
```

The child cannot accidentally extend the parent. Tests can advance to one millisecond before, exactly at, and one millisecond after the deadline.

## 7. Deterministic timing tests

A deterministic timing test controls the trigger, clock, and completion. It does not call `setTimeout` merely to “give the code time.” For a debouncer, invoke it several times, advance less than the quiet period, assert no call, advance to the boundary, and assert exactly one call with the documented arguments. For a poller, advance through each interval and assert the number of attempts and final deadline behavior.

Also test disposal. Cancelling a scheduled operation should remove its timer from the manual queue and settle its promise according to policy. Advancing far into the future must not resurrect cancelled callbacks.

## 8. What this changes in TaskHarbor

TaskHarbor receives a `Clock` boundary. Task deadlines, run deadlines, event timestamps, and tests no longer call global time APIs directly. The production clock uses monotonic elapsed time for budgets and civil time only for rendered metadata. Scheduler tests can complete delay tasks by advancing a manual clock rather than sleeping.

This separation makes the later fail-fast and graceful-shutdown tests fast and deterministic.

## 9. Deep case study: interval drift and overlapping work

A service uses `setInterval(runRefresh, 1000)`. A refresh sometimes takes 1.8 seconds. New callbacks continue becoming eligible, and the implementation can overlap refreshes or accumulate delayed executions depending on how `runRefresh` is written. The interval expresses recurring eligibility, not “start exactly every second with no overlap.”

For nonoverlapping periodic work, schedule the next wait after the current operation completes. Decide whether the period is measured from prior start or prior finish. If fixed-rate behavior matters, compute the next absolute deadline and skip or coalesce missed ticks rather than starting a burst of catch-up work. Each policy has different semantics under overload.

## 10. Clock taxonomy

Use the right clock for the claim:

- wall time for human timestamps and persisted calendar values;
- monotonic elapsed time for deadlines and durations;
- logical sequence numbers for deterministic event ordering;
- injected manual time for tests.

Wall clocks can move backward or jump forward. A duration derived from `Date.now()` is vulnerable to clock adjustment. A monotonic source should own timeout arithmetic.

## 11. Rate-control decision table

Debounce waits for quiet, throttle limits frequency, a rate limiter protects capacity, polling checks external state, and retry repeats after failure. They are not interchangeable. For each design, record who owns pending work, whether calls are dropped, delayed, coalesced, or rejected, what happens on shutdown, and whether timers keep the process alive.

## 12. Retry timing, jitter, and one total deadline

Retry is a time policy over repeated attempts. It needs eligibility rules, delay calculation, jitter, maximum attempts, and one total deadline. Exponential backoff without a deadline can exceed the caller’s budget. Independent clients using identical deterministic delays can synchronize into a retry storm. Jitter spreads load, but random tests become unstable unless the randomness source is injected.

Represent retry as a state machine: before-attempt, running-attempt, waiting-backoff, succeeded, exhausted, cancelled, or deadline-reached. Compute each delay from attempt number, cap it, apply an injected jitter function, then truncate it to remaining budget. A task entering backoff still owns a timer and must remove it on cancellation.

## 13. Timer handles as resources

A timer handle affects both callback delivery and process liveness. Clearing it prevents future callback execution. `unref` changes only whether the handle keeps the event loop alive; it does not cancel the callback while the process remains alive. `refresh` changes timing without creating a new handle. Treat these as separate operations.

Timer ownership should be local and terminal. A debounce component owns at most one pending timer; a retry operation owns one current backoff timer; a lifecycle host owns one grace-deadline timer. Long-lived collections of forgotten handles are resource leaks even when callbacks are tiny.

## 14. Manual-clock fidelity

A fake clock need not emulate every Node timing detail. It must faithfully implement the product contract being tested: monotonic advancement, ordering among equal deadlines, cancellation, and no early completion. Over-modeling event-loop phases inside a unit clock creates a second runtime. Keep phase-order experiments in integration tests and use the manual clock for deadline logic.

## 15. Scheduling policy requires an explicit time domain

A timer API is incomplete until it states what its numbers mean. Wall-clock timestamps answer “what civil time is it?” Monotonic durations answer “how much time elapsed?” Deadlines answer “after what monotonic instant should this operation stop waiting?” Retry delays answer “how long before another attempt may start?” These values are not interchangeable even when all are represented as numbers.

Suppose an operation receives `timeoutMs: 5000` and calls three nested helpers. Giving each helper a fresh five-second timeout permits the operation to consume fifteen seconds. Convert the initial policy into one absolute monotonic deadline. Each helper derives its remaining budget from that deadline. The design then has one temporal authority and one answer to “how much time remains?”

Manual clocks should preserve the same domain. A fake wall clock that controls `Date.now()` but not scheduled callbacks cannot test timer behavior. A queue-based manual scheduler that advances deadlines but ignores cancellation cannot test resource cleanup. State which clock operations the product consumes, then fake that interface completely enough for the claim under test.

## 16. Rate control is a state machine, not a utility-name choice

“Debounce,” “throttle,” “rate limit,” and “batch” are often selected by name before their state transitions are specified. Derive the policy instead:

- Which arrivals are remembered?
- Which result is returned to each caller?
- Is leading execution allowed?
- Is trailing execution required?
- What happens during an in-flight operation?
- Does cancellation reject pending callers, discard work, or allow the current operation to finish?
- Which timestamp controls the next legal start?

For a serial rate limiter, useful state may include `idle`, `scheduled`, and `running`; a queued request count; one next-eligible monotonic time; and one owned timer handle. A trailing debounce needs a replaceable pending value and an owned completion promise. A periodic poller needs a decision about overlap: skip, queue one, or allow concurrent runs. Encoding these states directly prevents a collection of booleans and timer IDs from admitting contradictory combinations.

TaskHarbor uses deadlines rather than periodic timers, but the same reasoning controls task timeouts and shutdown grace periods. The scheduler must cancel owned timer handles when a task settles so that a completed run does not remain alive because an obsolete timeout is still referenced.

## Practice sequence

1. Predict the module-specific investigation cases before running the checker or Node.
2. Draw the state, ownership, queue, or lifecycle model required by this chapter.
3. Complete [the workbook](workbook.md), recording the first causal difference between your prediction and the observed result.
4. Build [Deterministic Scheduler](../../labs/module-35-deterministic-scheduler/README.md) from the starter without opening the reference.
5. Integrate the corresponding TaskHarbor increment and add evidence at the layer that owns the claim.
6. Complete the unseen transfer and explain one unsupported guarantee explicitly.
7. Compare with [the reasoned solutions](solutions.md) only after your own design passes its tests.

## Ready to continue

You are ready to leave Module 35 when you can derive its behavior from the underlying runtime model, not from remembered output; when the laboratory’s terminal paths are all tested; and when you can apply the same mechanism to a different domain without weakening ownership, boundedness, cancellation, or deterministic-reporting requirements.

## Primary references

- Node.js API documentation: <https://nodejs.org/api/>
- ECMAScript specification: <https://tc39.es/ecma262/>
- TypeScript documentation: <https://www.typescriptlang.org/docs/>

## Continue

[Module 36](../module-36-async-iterables-generators-and-pull-based-sequences/index.md)
