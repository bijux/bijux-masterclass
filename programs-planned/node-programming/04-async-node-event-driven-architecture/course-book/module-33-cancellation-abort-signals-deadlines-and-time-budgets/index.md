# Module 33 — Cancellation, Abort Signals, Deadlines, and Time Budgets

> **Question:** How can asynchronous work stop cooperatively without pretending that cancellation rewinds effects that already happened?

## Why this comes now

Module 32 established the preceding async contract. This module adds the next responsibility without discarding that earlier ownership and compatibility discipline.

## Outcomes

By the end of the module, you can:

- treat cancellation as a one-way request and terminal reason rather than rollback;
- use AbortController and AbortSignal without losing the original cancellation cause;
- distinguish relative timeouts from absolute deadlines and propagate one remaining budget;
- compose external cancellation, shutdown, and deadline signals;
- place cancellation checkpoints and cleanup in operations that can cooperate;
- state honestly when an external effect may have committed despite local timeout;

## 1. Cancellation is a request, not time travel

JavaScript cannot generally interrupt arbitrary code at an arbitrary instruction. `AbortController.abort()` marks a signal, stores a reason, and notifies listeners. The operation must observe the signal before it can stop. A synchronous loop that never checks the signal remains unstoppable until it returns. A database, remote server, or filesystem operation may have committed an effect before the caller notices cancellation.

Therefore cancellation answers “the caller no longer wants to wait or continue,” not “nothing happened.” Product state must represent ambiguous outcomes where necessary. A timed-out create request may require an idempotency key or later status lookup; retrying blindly can duplicate the effect. Those distributed concerns arrive in later courses, but the conceptual boundary begins here.

Use explicit terminal vocabulary: succeeded, failed, cancelled, timed out, or outcome unknown. Do not collapse cancellation into an ordinary validation error or assume every abort means the same operational cause.

## 2. AbortSignal is a one-shot broadcast capability

An `AbortSignal` begins non-aborted and transitions once. It carries a `reason`, emits an abort event, and supports `throwIfAborted`. Multiple operations can observe the same signal, which makes it suitable for cancelling a task subtree. The controller is the authority to request cancellation; the signal is the readonly observation capability. Pass signals widely and controllers narrowly.

Check `signal.aborted` or call `throwIfAborted` before beginning expensive work. Register listeners with `{ once: true }`, and remove them during cleanup if the operation can finish before cancellation. Otherwise long-lived signals can retain closures and resources. Promise-based Node APIs that accept signals should be preferred over manual races when they provide the required semantics.

Never reuse an aborted signal for a later operation. Abortion is permanent. Create a new controller for a new lifetime.

## 3. Timeout and deadline are different representations

A timeout is a duration measured from some local start. A deadline is an absolute instant by which the operation must finish. Nested timeouts can accidentally multiply the caller’s budget: three layers each applying a fresh five-second timeout may consume fifteen seconds. An absolute deadline or a shared budget object prevents that drift.

A budget stores a deadline using a monotonic clock where possible. Each child operation asks for the remaining duration and may cap it further. When no time remains, it fails before starting. Wall-clock time such as `Date.now()` can jump because of clock adjustment; elapsed-time decisions should use a monotonic source such as `performance.now()` or an injected clock.

Do not report millisecond precision that the scheduler cannot guarantee. A timer establishes the earliest eligibility threshold; callback execution may occur later because the event loop is busy.

## 4. Composing cancellation causes

A job can stop because the user cancelled, the process began shutdown, its parent failed fast, or its own deadline expired. Combining those causes into one signal is convenient, but the terminal report should retain the decisive reason.

Modern Node lines support `AbortSignal.any` and `AbortSignal.timeout`. A library may also implement a small composition helper to control cleanup and compatibility. The first signal to abort wins. Remove listeners once the combined signal aborts or the operation completes.

When mapping the reason, preserve a supplied Error object rather than replacing every cause with a generic “aborted.” If a timeout controller created the cancellation, return a typed timeout outcome. If the parent supplied a domain cancellation reason, retain it. This is how observability stays connected to policy.

## 5. Cancellation-safe code has checkpoints and cleanup

A cooperative operation should define where cancellation can take effect. For a loop, check between bounded chunks. For a queued task, check before admission and after waiting for capacity. For a multi-step side effect, distinguish work before and after the commit point. Always release local resources in `finally`.

Consider a semaphore permit. If cancellation occurs after acquisition but before the protected operation finishes, the permit still must be released. Wrap acquisition and release in a scope whose `finally` runs for fulfillment, rejection, and abort. Avoid a promise race that returns early while the losing operation still owns the permit.

Cancellation safety does not mean the operation has no effect. It means the program’s invariants remain valid and resources are not leaked when cancellation is observed at any documented checkpoint.

## 6. One budget around an operation

A robust helper takes a callback that accepts a signal. It creates a timeout controller for the remaining budget, links external cancellation, and clears every timer and listener in `finally`. It does not attempt to cancel a callback that ignores the signal.

```ts
export async function withinBudget<T>(
  milliseconds: number,
  operation: (signal: AbortSignal) => Promise<T>,
  parent?: AbortSignal,
): Promise<T> {
  if (!Number.isFinite(milliseconds) || milliseconds < 0) {
    throw new RangeError('milliseconds must be finite and non-negative');
  }

  const deadline = new AbortController();
  const timer = setTimeout(
    () => deadline.abort(new Error('deadline exceeded')),
    milliseconds,
  );
  timer.unref?.();

  const signal = parent
    ? AbortSignal.any([parent, deadline.signal])
    : deadline.signal;

  try {
    signal.throwIfAborted();
    return await operation(signal);
  } finally {
    clearTimeout(timer);
  }
}
```

The helper’s contract must state that the callback is cooperative. Returning from `withinBudget` after abort does not prove that an arbitrary external operation rolled back.

## 7. Testing cancellation without random sleeps

Cancellation tests should control the point at which an operation is waiting. Use deferred promises, manual clocks, or injected hooks. Start the operation, confirm it reached the waiting state, request abort, and assert cleanup and terminal classification. A test that sleeps for ten milliseconds and hopes the operation has started is probabilistic.

Test cancellation before start, during a wait, after successful completion, and after the signal is already aborted. Verify listener cleanup and idempotent repeated abort calls. When a deadline is involved, test the exact boundary through an injected clock rather than relying only on wall-clock timing.

## 8. What this changes in TaskHarbor

TaskHarbor gains one run-level controller and optional per-task deadlines. The run signal represents user cancellation, process shutdown, or fail-fast policy. Each task receives a derived signal. A timed-out task becomes `timed-out`; a parent-aborted task becomes `cancelled`. Dependent tasks become `blocked` when a required predecessor did not succeed.

The scheduler never claims that cancellation undoes an operation. The built-in Course 4 operations are deliberately local and cooperative, but the public outcome vocabulary is designed for later real effects.

## 9. Deep case study: timeout after remote commit

A client sends a request to a remote service and waits under a 500 ms budget. At 500 ms it aborts the local wait and reports a timeout. The remote service may already have committed the operation, may still be executing it, or may never have received it. The timeout classifies the client’s observation; it does not establish rollback or nonexecution.

This ambiguity changes API design. Retry requires an idempotency key or a reconciliation query. User messaging must avoid “the operation failed” when the only proven fact is “no response arrived before the deadline.” Cancellation reasons should preserve whether the source was user abort, parent shutdown, fail-fast policy, or deadline expiry. Collapsing all causes into `AbortError` removes information needed for safe recovery.

## 10. Deadline algebra

Represent an absolute deadline on a monotonic clock. A child operation receives the minimum of its parent deadline and any stricter local limit. Remaining budget is recomputed before each wait:

```text
remaining = deadline - now
child-deadline = min(parent-deadline, now + local-limit)
```

Starting a fresh full timeout at each nested layer inflates the operation beyond the caller’s budget. The same principle applies across retries: backoff, attempt time, and cleanup must all fit within one total deadline.

## 11. Cancellation-safety ledger

For every cancellation checkpoint, record:

- state that may already be committed;
- resource currently owned;
- listener or timer that must be removed;
- partial output that must be discarded or returned;
- permit or queue slot that must be released;
- terminal classification and preserved cause;
- whether a retry is safe, unsafe, or requires reconciliation.

This ledger prevents the phrase “supports AbortSignal” from hiding incomplete cleanup semantics.

## 12. Cancellation races and cause precedence

Several signals may become aborted near the same time. A parent can cancel while a local deadline expires; shutdown can arrive after fail-fast already requested stop. `AbortSignal.any` exposes whichever input cause wins according to actual timing. If the product needs deterministic precedence, do not rely on the race alone. Check already-aborted inputs in policy order before composing them, or route causes through one controller owned by the parent state machine.

Cause precedence is a product rule. A task already timed out should not later be relabeled “shutdown cancelled” merely because process termination followed. Conversely, a task never admitted because shutdown began should not be reported as timed out. Record the transition that first made the task terminal and preserve that cause.

## 13. Abort-aware resource acquisition

Cancellation can occur between acquiring a resource and registering cleanup. Keep that gap synchronous and minimal. After acquiring a file handle, permit, temporary path, or subscription, immediately establish the `try/finally` or disposer before the next suspension. When an API supports an abort signal, still ask whether abort releases partially acquired resources or only stops waiting.

A robust pattern is:

```text
check pre-abort
acquire
register owner/cleanup synchronously
check abort if acquisition was not signal-aware
perform work with bounded checkpoints
cleanup in finally
```

This is the async counterpart of Course 2’s explicit object lifecycle discipline.

## 14. Cancellation contracts in public APIs

A public function accepting `signal?: AbortSignal` should document:

- whether pre-abort prevents all work;
- which checkpoints observe later abort;
- which effects may already be committed;
- terminal error type and preserved reason;
- cleanup completion before rejection;
- whether the function creates background work that outlives rejection;
- whether caller retry is safe.

Without these statements, signal support is syntax rather than a meaningful contract.

## Practice sequence

1. Predict the module-specific investigation cases before running the checker or Node.
2. Draw the state, ownership, queue, or lifecycle model required by this chapter.
3. Complete [the workbook](workbook.md), recording the first causal difference between your prediction and the observed result.
4. Build [Deadline Budget](../../labs/module-33-deadline-budget/README.md) from the starter without opening the reference.
5. Integrate the corresponding TaskHarbor increment and add evidence at the layer that owns the claim.
6. Complete the unseen transfer and explain one unsupported guarantee explicitly.
7. Compare with [the reasoned solutions](solutions.md) only after your own design passes its tests.

## Ready to continue

You are ready to leave Module 33 when you can derive its behavior from the underlying runtime model, not from remembered output; when the laboratory’s terminal paths are all tested; and when you can apply the same mechanism to a different domain without weakening ownership, boundedness, cancellation, or deterministic-reporting requirements.

## Primary references

- Node.js API documentation: <https://nodejs.org/api/>
- ECMAScript specification: <https://tc39.es/ecma262/>
- TypeScript documentation: <https://www.typescriptlang.org/docs/>

## Continue

[Module 34](../module-34-event-emitter-and-typed-event-contracts/index.md)
