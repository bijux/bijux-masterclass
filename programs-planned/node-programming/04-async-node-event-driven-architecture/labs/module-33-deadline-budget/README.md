# Deadline Budget

## Product

Build a budget wrapper and a small retry loop that use one explicit cancellation lineage. The product must distinguish parent abort, local deadline, operation failure, and successful completion. It must remove every timer and abort listener on every terminal path.

Read [Module 33](../../course-book/module-33-cancellation-abort-signals-deadlines-and-time-budgets/index.md).

## Public API

Expose a `Clock` abstraction, a typed `DeadlineExceededError`, and a helper conceptually equivalent to:

```ts
export function withinBudget<T>(
  budgetMs: number,
  operation: (signal: AbortSignal) => Promise<T>,
  options?: { readonly parent?: AbortSignal; readonly clock?: Clock },
): Promise<T>;
```

The operation receives a cooperative signal. The helper does not claim to interrupt arbitrary synchronous code or undo external effects.

## Required invariants

- Invalid budgets fail before operation invocation.
- An already-aborted parent prevents admission.
- The earliest parent or deadline cause is preserved.
- A successful operation clears its pending timer.
- Operation failure is not relabeled as timeout.
- Listener removal occurs after success, rejection, parent abort, and deadline.
- Retry delay and attempts fit under one absolute deadline.

## Adversarial tests

Use a manual clock or deferred promises to test exact deadline boundaries. Include an operation that ignores the signal and demonstrate the honest contract: the wrapper stops waiting, but the operation can still settle later. Test simultaneous parent abort and deadline without requiring a machine-specific race winner; assert only the documented cause policy.

## Design record

Write a cancellation-safety ledger for a hypothetical remote side effect. Identify what could already be committed at timeout and which idempotency or reconciliation mechanism would be needed before automatic retry.

## Commit points and cancellation gaps

Document the exact point at which the helper owns each timer, listener, child controller, and resource. Add an acquisition test in which abort occurs after the underlying resource becomes available but before control returns to the caller. The implementation must release that resource and preserve the cancellation cause. Include a table for parent abort, local timeout, success, operation failure, and cleanup failure.

The laboratory is complete only when listener and timer counts return to baseline after every terminal path. A rejection with the right message is insufficient if the helper leaves an owned callback reachable.

## Public cancellation vocabulary

Define a small machine-readable cancellation reason set for parent shutdown, local deadline, caller request, and supervisor fail-fast. Preserve the original cause when one policy wraps another. Tests should assert categories rather than depend only on error-message text.

## Independent transfer

Apply the budget model to a cache refresh with stale-value fallback. State whether the fallback consumes remaining budget, whether refresh may continue in the background, and which component owns that continuation.

## Implementation stages

First model deadline and parent causes as distinct typed errors. Add pre-abort before invoking the callback. Link signals and install cleanup before awaiting work. Inject a clock. Then add retry-under-budget as a separate layer so one attempt helper does not quietly reset the parent deadline.

## Review questions

Which controller owns each cause? When does the operation become admitted? Can the callback continue after the wrapper rejects? What cleanup is guaranteed complete? How does the test observe listener removal? What external effects remain ambiguous?

## Completion evidence

Submit exact-boundary tests, parent/deadline race tests, a noncooperative callback demonstration, and a public cancellation contract. The design should make clear that bounded waiting and bounded underlying execution are different claims.
