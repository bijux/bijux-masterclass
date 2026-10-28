# Module 33 Reasoned Solutions — Cancellation, Abort Signals, Deadlines, and Time Budgets

## A. Outcome classification

An aborted timer can usually be classified as not having delivered its timer completion. A partially issued file write may have changed external state. A remote timeout proves only lack of a timely response. A queued producer cancelled before invocation has the strongest nonstart guarantee because the application still owns admission. These cases share a signal API but not the same effect semantics.

## B. Cause composition

Each authority owns its own controller: the executable owns shutdown, the user boundary owns user cancellation, the supervisor owns fail-fast, and the task wrapper owns its local deadline. A derived signal observes their union. Entry checks an already-aborted parent before starting work. Every linked listener and timeout is removed in `finally`. The terminal outcome retains `signal.reason` or a typed wrapper so recovery can distinguish causes.

## C. Absolute budget

Three helpers each starting a full relative timeout can serially consume multiples of the caller’s total budget. Store one monotonic deadline and compute remaining time before each attempt, backoff, and nested operation. A child may impose a smaller local cap but never extend the parent. Cleanup policy is product specific: essential invariant-restoring cleanup must run even when the response budget expires, while the caller can be told that final cleanup continues under a separately bounded shutdown obligation.

## D. Helper semantics

A sound `withinBudget` validates the budget before invoking the operation, links parent and deadline signals, checks pre-abort, awaits the operation, and clears the timer on every terminal path. It documents cooperation. If the operation ignores the signal, the helper may reject while the underlying effect continues; the caller must not interpret that as noncommit.

## E. TaskHarbor and transfer

TaskHarbor maps a local typed deadline reason to `timed-out`; other run abort reasons map to `cancelled`. Dependents become blocked because their prerequisite did not succeed. Tests should use controlled clocks or executor gates and verify that no timeout listener remains after normal completion.

For the document export, rendering can be abandoned before publication, temporary-file writes require cleanup of the candidate, and replacement commits a visible destination change. Cancellation after replacement cannot be reported as rollback. Retrying is safe only when replacement is idempotent or the destination version is checked.

## F. Race and acquisition solutions

A physical race can produce either first abort reason; tests should assert that the first recorded terminal transition never changes afterward and that cleanup is identical. Deterministic precedence requires an owning state machine, not just `AbortSignal.any`: it checks or records a task timeout transition before processing later parent cancellation for that task.

The resource leak exists after `open` but before `try/finally`. Establish a local owner or disposer immediately, then perform asynchronous registration. If registration fails, the local cleanup closes the handle. Once a longer-lived component accepts ownership, the local owner can transfer or disarm under an explicit synchronous transition.

The upload contract states that pre-abort prevents start, later abort stops cooperative local reads and the client wait, request bytes may already have been transmitted, remote commit may be ambiguous, local handles are closed before rejection, and automatic retry requires an idempotency key or status reconciliation.

## G. Cancellation precedence answers

Cause precedence should be a public policy, not whichever callback wins a race accidentally. A defensible default is: return success only when the operation’s state transition completed before cancellation became authoritative; otherwise preserve the earliest authoritative cancellation cause, while attaching later operation or cleanup failures as causes or an aggregate. Acquisition needs a post-acquire abort check because the resource can become owned in the narrow interval after the earlier check. If that check observes cancellation, release the resource before rejecting.

Controlled tests create deferred acquisition, operation, and cleanup promises. They attach the rejection assertion before advancing a manual clock, settle the competing event in each order, and inspect listener and timer counts afterward. A random sleep demonstrates only one schedule. The principled repair owns both the timer and abort listener in `finally`; a weak repair merely ignores late settlements.
