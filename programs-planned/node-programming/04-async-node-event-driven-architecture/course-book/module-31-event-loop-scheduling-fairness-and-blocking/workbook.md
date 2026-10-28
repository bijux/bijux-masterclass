# Module 31 Workbook — Scheduling, Fairness, and Blocking

Do not execute the snippets until you have written a schedule ledger. For every callback, record who makes it ready, which queue or phase owns it, and which earlier operation must finish first.

## A. Predict a partial order

Given this ESM program, list only relations that are guaranteed. Do not invent a total order between the timer and immediate.

```ts
console.log('A');
process.nextTick(() => console.log('B'));
queueMicrotask(() => console.log('C'));
Promise.resolve().then(() => console.log('D'));
setTimeout(() => console.log('E'), 0);
setImmediate(() => console.log('F'));
console.log('G');
```

1. Which labels must precede every asynchronous label?
2. Which callbacks are microtasks, and which callback belongs to Node’s next-tick queue?
3. Which relation between `E` and `F` is safe to put in a public test?
4. What changes if the timer and immediate are scheduled from an I/O callback?

## B. Find the hidden blocking region

An `async` import function awaits `readFile`, then parses and sorts 500,000 records before its next `await`.

5. Draw the operation as host wait followed by JavaScript regions.
6. Explain why its promise-shaped API does not make the parse or sort non-blocking.
7. Propose three different repairs and state the cost or later-course dependency of each.
8. Reject the repair `await Promise.resolve()` inside the loop with a queue-level explanation.

## C. Preserve an atomic transition

A registry sets `status = 'running'`, awaits an audit write, and only then sets `startedAt`. Another callback reads the registry during the suspension.

9. Identify the invalid observable state.
10. Move the suspension or redesign the transition so `status` and `startedAt` become visible together.
11. State what the audit record can truthfully report if writing it fails after the state transition.

## D. Construct cooperative work

Implement `cooperativeMap` with:

- positive finite chunk validation;
- source-ordered output;
- one real event-loop yield between nonfinal chunks;
- optional abort checking before each chunk;
- no promise per source item;
- a test proving another immediate can run before a large mapping completes.

Do not assert a wall-clock maximum. Assert causal progress with a controlled trace.

## E. Independent laboratory

Complete [Event Loop Observatory](../../labs/module-31-event-loop-observatory/README.md). Extend its trace with one recursive microtask experiment, but cap the recursion so the test cannot hang. Explain why the experiment demonstrates starvation risk rather than a portable complete event-loop order.

## F. TaskHarbor transfer

Add a run trace that records `accepted`, `started`, `yielded`, `resumed`, and `completed` for one simulated task. The trace is observational. The scheduler’s task record remains authoritative. Add a test that final outcomes remain manifest ordered even when completion order is reversed.

## G. Unseen transfer

Design a cooperative in-memory search over a million strings. Specify chunk size, yield primitive, abort checkpoints, output ordering, and the largest synchronous region. Explain when the design should be replaced by worker threads rather than further chunk tuning.

## I. Advanced portability exercise

A test expects this exact output:

```text
sync,nextTick,promise,timeout,immediate
```

Run context is not stated. Rewrite the test as three smaller claims: one ECMAScript ordering claim, one Node-specific claim, and one application-level claim. Mark any remaining complete trace as observational metadata that must include Node version and module mode.

## J. Blocking-budget exercise

A synchronous validator processes records at these measured costs: ordinary 3 µs, worst-case 40 µs. The service wants ordinary yields within 8 ms and worst-case yields within 20 ms.

- Derive a conservative chunk size.
- Explain why one fixed size may still be insufficient when record costs vary widely.
- Design an adaptive alternative based on monotonic elapsed time.
- State how adaptive yielding affects deterministic output and cancellation checkpoints.

## K. Evidence checklist

Submit a schedule graph, a blocking-budget calculation, an adversarial trace, and a test that remains valid when timer and immediate order changes. Include the exact claim each artifact falsifies.

## L. Scheduler authority review

For each of the following claims, label it **ECMAScript guarantee**, **Node API contract**, **application policy**, or **one-environment observation**: a promise reaction created in the current callback runs after that callback; a zero-delay timer runs before an immediate; TaskHarbor reports outcomes in manifest order; a recursive next-tick chain can delay timers. For each non-observational claim, name the evidence you would place in a long-lived test suite.

Then redesign the cooperative mapper for a transformation that must commit results in batches of 100. State what is atomic, where cancellation is checked, how partial candidate state is discarded, and which yield reaches an ordinary event-loop phase.

## H. Closed-book defense

Draw the call stack, next-tick queue, microtask queue, timer eligibility, and immediate phase. Then answer: what does “ready” mean, what does “running” mean, and why does single-threaded callback execution prevent memory data races but not logical races across turns?
