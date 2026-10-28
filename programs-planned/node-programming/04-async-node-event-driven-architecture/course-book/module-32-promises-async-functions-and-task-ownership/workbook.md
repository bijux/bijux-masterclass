# Module 32 Workbook — Promises, Async Functions, and Task Ownership

## A. Trace start time

For each expression, state what synchronous work begins before the caller receives a promise and where the first suspension occurs.

```ts
async function load(): Promise<string> {
  trace.push('entered');
  const text = await readFile('input.txt', 'utf8');
  trace.push('resumed');
  return text;
}
const promise = load();
trace.push('returned');
```

1. Order the three trace labels under successful reading.
2. Explain why an exception before the first `await` still becomes a rejected promise.
3. Explain what the caller owns after `load()` returns.

## B. Select a combinator by policy

For each policy, choose `all`, `allSettled`, `race`, `any`, or a custom supervisor, and justify what extra cancellation or joining logic remains necessary.

4. Every independent validation result must be reported.
5. All values are required; the first rejection makes the aggregate unsuccessful.
6. The first successful replica response is sufficient, but losing requests must be stopped and cleaned up.
7. A timeout races an operation, but the operation may ignore cancellation.

## C. Diagnose orphaned work

A CLI starts background audit writes with `void writeAudit(record)` and exits after the main command.

8. List the possible lost evidence and unhandled failures.
9. Design an audit owner that bounds queued records and joins before normal exit.
10. State the shutdown behavior when the audit sink itself is unavailable.

## D. Build a nursery

Implement a nursery that:

- accepts lazy producers and unique IDs;
- captures synchronous throw and asynchronous rejection;
- closes admission when `join` begins;
- returns one typed outcome per accepted source in source order;
- makes repeated `join` calls share the same completion promise;
- exposes no raw mutable task registry.

Test duplicate IDs, zero tasks, mixed completion order, synchronous throw, rejection, and spawn-after-close.

## E. Independent laboratory

Complete [Owned Promise Nursery](../../labs/module-32-owned-promise-nursery/README.md). Add a test that proves a second `join()` does not start tasks again and returns the same terminal array identity or a documented equivalent immutable value.

## F. TaskHarbor transfer

Replace ad hoc task promises with a run-owned registry. Every accepted task must receive exactly one terminal outcome. Add an accounting assertion:

```text
accepted = succeeded + failed + timed-out + cancelled + blocked
```

Explain why a live “running count” is not sufficient final evidence.

## G. Unseen transfer

Design a replica reader that returns the first valid response. Losers must be aborted, all attempts must be joined, and failures must retain endpoint identity. Describe the difference between the user-visible result and the complete internal outcome report.

## I. Error-ownership clinic

A batch uses:

```ts
for (const input of inputs) {
  void process(input).catch(console.error);
}
```

List at least five contracts this code cannot prove. Rewrite it for two products: a best-effort telemetry sender and a required migration batch. The two designs should not have the same terminal policy.

## J. Cleanup-aware join

Construct a task whose main operation rejects, then whose asynchronous cleanup also fails. Decide how the nursery outcome represents both failures. Compare:

- replacing the primary failure with cleanup failure;
- using an aggregate error;
- preserving primary failure and attaching cleanup context.

State which policy TaskHarbor uses and why.

## K. Combinator counterexamples

Give one counterexample showing why each statement is false:

1. `Promise.all` cancels siblings after rejection.
2. `Promise.race` limits operation duration.
3. `Promise.any` proves losers had no effect.
4. `allSettled` bounds concurrency.
5. a global unhandled-rejection handler owns task cleanup.

## L. Promise lifecycle table

Construct a table for six operations: a created but unreturned promise, a returned promise, a nursery-owned promise, a detached telemetry send, a `Promise.race` loser, and a cleanup promise started in `finally`. Record who starts it, who observes rejection, who can request cancellation, who joins it, and what product state proves completion.

Repair a `Promise.race([operation(), timeout()])` helper so that the losing timer is disposed, the operation receives cancellation, and the caller can distinguish timeout from operation failure. Explain what cannot be guaranteed when the operation ignores cancellation.

## M. Detached work review

Review a command handler that sends an audit record with `void sendAudit(record)` and immediately returns success. Decide whether audit delivery is required product behavior, best-effort observation, or shutdown-owned background work. For each policy, specify who retains the promise, how rejection is reported, whether shutdown waits, and what bounded queue or drop policy applies.

Now design a `TaskScope` whose `spawn` method accepts a lazy producer and whose `closeAndJoin` method is idempotent. State what happens when a producer throws synchronously, when a task rejects after close begins, and when cleanup itself rejects. Do not solve the exercise by converting all failures into strings.

## H. Closed-book defense

Explain why `Promise.race` does not cancel losers, why `void` does not own a promise, and why catching a rejection without recording a terminal outcome can still violate the parent operation’s contract.
