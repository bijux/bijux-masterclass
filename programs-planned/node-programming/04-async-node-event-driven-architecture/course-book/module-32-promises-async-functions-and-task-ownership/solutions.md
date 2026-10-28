# Module 32 Reasoned Solutions — Promises, Async Functions, and Task Ownership

## A. Start and suspension

Calling `load()` runs its body immediately through `trace.push('entered')` and the call to `readFile`. At the `await`, `load` returns a pending promise, allowing the caller to append `returned`. After reading completes, the continuation appends `resumed`. A synchronous throw inside an async function is converted into rejection of the returned promise, so the caller still needs rejection ownership.

The caller owns a handle to the eventual result, but handle possession alone does not define whether the operation may outlive a request, batch, or process phase. That lifecycle policy belongs to a parent scope.

## B. Combinator policy

Independent validation reporting fits `allSettled`, followed by typed conversion and source-index reconstruction. “All values required” fits `all`, though already-started siblings continue after the first observed rejection. First valid replica response resembles `any`, but the caller must abort and join losers. A timeout implemented with `race` only stops waiting; it does not stop an operation that ignores its signal. The correct answer therefore names both the aggregate combinator and the missing lifecycle work.

## C. Audit ownership

`void writeAudit` suppresses neither rejection nor process termination. The process may exit before writes finish, and later rejection may become unhandled. A bounded audit component owns a finite queue, one worker, and a `closeAndJoin` operation. During shutdown it stops admission, drains within policy, records sink failure, and sets an appropriate process result. If audit durability is mandatory, command success cannot be reported independently of that failure; if audit is best effort, the limitation must be explicit.

## D. Nursery construction

Lazy producers are invoked only from `spawn` or a controlled admission point. Each promise is immediately wrapped into a terminal-outcome promise so no rejection escapes. `join` closes admission, memoizes the aggregate promise, and returns outcomes ordered by accepted index. Duplicate IDs fail before producer invocation. Synchronous throw is captured by beginning with `Promise.resolve().then(producer)`.

The nursery may return a frozen array or the same memoized array; the contract should state which. What matters is that repeated joins do not duplicate work and that no accepted child remains unobserved.

## E. TaskHarbor and transfer

TaskHarbor’s terminal accounting must be reconstructed after all running work is joined. A live counter can be stale, can miss a rejected task whose decrement path failed, and cannot distinguish terminal categories. Stable indexed outcomes provide stronger evidence.

For the replica reader, the user receives the first valid value. Internally, the supervisor keeps endpoint-indexed outcomes for the winner, rejected endpoints, and aborted losers. That report supports cleanup and diagnostics without exposing completion order as the product result.

## F. Ownership and cleanup solutions

The fire-and-forget loop cannot prove bounded starts, completion before parent return, stable source identity, cleanup, retry policy, or final success/failure. A best-effort telemetry sender may use a bounded queue with explicit drop metrics and a finite shutdown flush. A migration batch must retain every task, stop or continue according to migration policy, join all accepted operations, and return a complete indexed report.

When the main operation and cleanup both fail, replacing the primary error loses the cause that triggered cleanup. An `AggregateError` is appropriate when both are independently important. Another defensible policy preserves the primary error and attaches cleanup failure through structured context or `cause`. TaskHarbor’s built-ins have simple cleanup; its wrappers preserve task failure and treat timer/listener cleanup as invariant work. A cleanup defect should surface as an infrastructure failure rather than silently alter a domain outcome.

The combinator counterexamples follow one rule: combinators aggregate settlement; they do not own producers. `all` leaves already-started siblings active, `race` only settles its aggregate first, `any` says nothing about loser effects, `allSettled` starts whatever promises already exist, and a global handler lacks the operation-specific lifecycle information needed to clean up.

## G. Detached-work answers

A promise may be deliberately detached only when the product contract says the effect is best effort and a bounded owner still observes rejection. Required audit delivery belongs in the command’s returned promise or in a process-owned queue that shutdown drains. Best-effort telemetry may use a bounded drop policy, but `void` is not itself an ownership policy.

`closeAndJoin` closes admission once, memoizes its aggregate promise, and observes synchronous throw through a promise boundary. Rejections retain `unknown` causes in typed outcomes. Cleanup failure is preserved separately from task failure. Converting everything to strings is weaker because it destroys causal identity and prevents higher layers from classifying failure.
