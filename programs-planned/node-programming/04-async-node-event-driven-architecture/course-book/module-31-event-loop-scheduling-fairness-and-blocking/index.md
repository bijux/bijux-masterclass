# Module 31 — Event Loop, Scheduling, Fairness, and Blocking

> **Question:** When does asynchronous Node.js work actually run, what ordering can you rely on, and how can one callback prevent every other operation from making progress?

## Why this comes now

Course 3 ended with trustworthy library contracts. Module 31 now adds scheduling: the same public API can become incorrect when work starts, suspends, or blocks at the wrong time.

## Outcomes

By the end of the module, you can:

- separate JavaScript call-stack execution, microtasks, Node-specific next-tick work, event-loop phases, and operating-system completion;
- predict guaranteed partial orders without inventing a universal total order;
- explain run-to-completion and why a single CPU-heavy callback blocks unrelated timers and I/O callbacks;
- identify starvation caused by recursive microtask or next-tick scheduling;
- break long CPU work into bounded chunks while preserving deterministic result order;
- write tests that assert contractual ordering rather than one machine-specific trace;

## 1. The event loop is a scheduler, not a second JavaScript thread

Node.js normally executes JavaScript for one isolate on one thread. The event loop does not make two JavaScript callbacks run simultaneously. It chooses which ready callback receives the thread next. Once a callback begins, ordinary JavaScript runs to completion unless it explicitly reaches an asynchronous boundary by returning to the host. This property is useful: a short synchronous state transition cannot be interleaved halfway through by another timer callback. It is also dangerous: a long parser, compression loop, regular expression, or synchronous filesystem call monopolizes the isolate.

Keep four layers separate. The JavaScript stack contains the function currently running. ECMAScript jobs contain promise reactions and `queueMicrotask` callbacks. Node adds a next-tick queue with special priority. The libuv event loop organizes timers, I/O polling, check callbacks such as `setImmediate`, and close callbacks. Beneath those layers, the operating system or a libuv worker pool may complete work, but completion still needs a JavaScript callback to receive the main thread. “The I/O happened in the background” does not mean its JavaScript continuation can run while the event loop is blocked.

A useful schedule ledger has five columns: operation, who makes it ready, queue or phase, earliest legal time, and what can delay it. That ledger is more accurate than memorizing a circular event-loop diagram without connecting it to a program.

## 2. Run-to-completion and the meaning of readiness

A callback being ready is not the same as a callback running. A zero-millisecond timer means “eligible after at least this delay,” not “execute immediately” and not “execute before every immediate.” A completed filesystem request means its callback can be queued; it does not preempt the code currently on the stack. Promise resolution makes reactions eligible as microtasks, but the current JavaScript turn still finishes first.

This distinction explains many apparent races. Suppose a function updates three related fields synchronously and only then returns. No timer observes the object after the first field but before the third. In contrast, placing an `await` between those updates allows other work to run before the continuation. The `await` is therefore not cosmetic. It changes the atomic region visible to the rest of the process.

When reviewing an async function, mark every suspension point. State established before a suspension can be observed by other callbacks while the function is paused. State that must change as one transition should be computed before the suspension or protected by a higher-level protocol. JavaScript’s single-threaded callback execution prevents data races in the narrow machine-memory sense, but it does not prevent logical races across turns.

## 3. Microtasks, next-tick work, timers, and immediates

Promise reactions and `queueMicrotask` callbacks use the ECMAScript microtask mechanism. Node’s `process.nextTick` queue is separate and is drained at Node-defined boundaries. Timers become eligible after their thresholds. `setImmediate` callbacks run in the check phase. Exact traces can depend on where scheduling occurred, whether the top level is CommonJS or ESM, whether I/O completed, and which platform is running. A course that teaches one universal ordering such as “timeout always beats immediate” is teaching a coincidence as a contract.

The reliable method is to state partial orders. Synchronous statements in one callback finish before any callback scheduled from that callback. Microtasks created during a callback run before Node proceeds to the next ordinary event-loop phase. A timer never runs before its threshold. A callback scheduled recursively through `process.nextTick` can postpone ordinary phases. Between a zero-delay timer and an immediate created in a context where both could become ready, do not build product correctness on a total order that the API does not promise.

Tests should encode those partial orders. Assert that initialization precedes observation, that cleanup microtasks finish before a later phase where required, or that result reconstruction is independent of completion order. Avoid brittle snapshots of every callback label unless the experiment itself is the product.

## 4. Starvation is a progress failure

A program can remain technically alive while making no useful progress. Recursive scheduling through `process.nextTick` or microtasks can keep replenishing a higher-priority queue faster than Node reaches timers or I/O. The process uses CPU, but external requests appear frozen. This is starvation rather than deadlock: no cycle of locks exists, yet lower-priority work never receives service.

Fairness requires an explicit yield to a later event-loop turn. For long in-memory work, process a bounded chunk, record progress, then yield with an operation such as a promise around `setImmediate` or the timers-promises scheduler API available on the pinned Node line. Chunk size is a product parameter. A chunk that is too small increases scheduling overhead; a chunk that is too large damages responsiveness. Course 9 will measure the trade-off. Here, the goal is to make the fairness boundary visible and configurable.

Never claim that `await Promise.resolve()` yields to timers or I/O. It schedules the continuation as another microtask and can preserve starvation. The kind of yield matters because queues have different priorities.

## 5. Blocking work and the illusion of asynchronous APIs

An API returning a promise does not guarantee that all of its work is non-blocking. An async function may perform substantial synchronous work before its first `await`. JSON parsing, schema validation, template rendering, cryptographic setup, and sorting all execute on the event-loop thread unless moved elsewhere. Some Node APIs delegate to a worker pool; others are direct operating-system calls; synchronous variants block by definition. The caller must reason about the actual implementation boundary, not the presence of `async` in a signature.

Use a blocking budget. For each callback, estimate or bound input size, algorithmic complexity, and worst-case synchronous work. Reject or partition hostile inputs before an expensive operation. Do not process an unbounded array in one callback merely because each element’s body is small. Ten million small bodies still form one large blocking region.

Worker threads are intentionally postponed to Course 8. Course 4 first teaches the more common repair: keep the event loop responsive by bounding input, avoiding synchronous host APIs on request paths, and chunking CPU work when the computation can be interrupted safely.

## 6. A complete cooperative batch processor

A cooperative processor owns three contracts: result order, cancellation, and fairness. It may process source items in chunks, but it should usually return results in source order rather than completion-turn order. It should check an `AbortSignal` between chunks, because cancellation cannot interrupt arbitrary synchronous JavaScript in the middle of a chunk. It should yield through an ordinary phase, not only through another microtask.

```ts
import { setImmediate as yieldTurn } from 'node:timers/promises';

export async function cooperativeMap<T, U>(
  values: readonly T[],
  chunkSize: number,
  map: (value: T, index: number) => U,
  signal?: AbortSignal,
): Promise<readonly U[]> {
  if (!Number.isInteger(chunkSize) || chunkSize <= 0) {
    throw new RangeError('chunkSize must be a positive integer');
  }

  const output: U[] = [];
  for (let start = 0; start < values.length; start += chunkSize) {
    signal?.throwIfAborted();
    const end = Math.min(start + chunkSize, values.length);
    for (let index = start; index < end; index += 1) {
      output.push(map(values[index]!, index));
    }
    if (end < values.length) {
      await yieldTurn(undefined, { signal });
    }
  }
  return output;
}
```

The function does not pretend to provide parallelism. It preserves responsiveness by returning scheduling authority between chunks. Its cancellation latency is bounded by one chunk, so the chunk-size decision is part of the public behavior.

## 7. A decision procedure for scheduling defects

When an async program appears out of order or unresponsive, proceed mechanically.

First, identify the currently running callback and every suspension point. Second, classify newly scheduled work as next-tick, microtask, timer, I/O continuation, immediate, or close callback. Third, separate guaranteed order from observed order. Fourth, look for an unbounded synchronous region or a recursively replenished high-priority queue. Fifth, decide whether the product needs ordering, fairness, or both. Ordering may require explicit sequencing; fairness may require a later-phase yield; neither is repaired by random sleeps.

Finally, make the claim testable. A correct test might assert that all results remain source ordered across several chunk sizes, that an abort is observed no later than one chunk boundary, and that a scheduled immediate runs before the complete million-item job finishes. A weak test measures one wall-clock duration on one machine and treats it as a universal guarantee.

## 8. What this changes in TaskHarbor

TaskHarbor will eventually run dependency-aware jobs with bounded concurrency. This module establishes its schedule vocabulary. Manifest parsing and graph validation remain synchronous and bounded. Job execution crosses explicit async boundaries. Completion order is allowed to vary, but final reporting is source ordered. Long operations must either be naturally asynchronous or cooperate with cancellation and fairness.

The first capstone increment is an event trace around one simulated job: accepted, started, yielded, resumed, and completed. The trace is observation, not the state authority. The authoritative state remains the scheduler’s task record. This distinction will matter when EventEmitter arrives in Module 34.

## 9. Deep case study: an apparently asynchronous importer

Consider an import command that reads a file asynchronously, parses a large JSON array, validates each record, and writes a summary. Only the file read is asynchronous. Once the promise resumes, `JSON.parse`, validation, sorting, and rendering all execute synchronously on the event-loop thread. A health timer can be eligible for hundreds of milliseconds without running. Adding `async` to the validator changes nothing; code before its first suspension still blocks.

The correct analysis separates **host wait** from **JavaScript service time**. Record the file read as a host operation whose completion makes a callback ready. Record parsing as one synchronous region whose cost grows with input size. Record validation either as another monolithic region or as bounded chunks separated by a real event-loop yield. This ledger makes the design choice visible: reject oversized inputs, stream them in a later course, move CPU work to a worker in Course 8, or cooperatively partition safe-to-interrupt work now.

A weak repair inserts `await Promise.resolve()` every thousand records. That creates another microtask and can keep lower-priority phases starved. The requirement is not “use await”; the requirement is “return scheduling authority far enough for timers and I/O continuations to run.” A `setImmediate`-based yield, with a documented chunk-size policy, satisfies that narrower Course 4 goal.

## 10. Schedule claims: guarantee, policy, or observation

Use three labels in design notes:

| Claim | Example | Evidence |
|---|---|---|
| language or platform guarantee | the current synchronous callback completes before a promise reaction created inside it runs | specification or primary Node documentation |
| application policy | TaskHarbor reconstructs terminal results in manifest order | unit and integration tests over reordered completion |
| observation | on this run, an immediate appeared before a zero-delay timer | trace only; never a correctness dependency |

The distinction prevents traces from becoming accidental APIs. An observatory can record a complete order; a production component should depend only on documented partial orders and its own explicit sequencing.

## 11. Review checklist for a scheduling boundary

Before accepting an asynchronous design, answer these questions in order:

1. What synchronous work happens before the first suspension?
2. Which callbacks can become ready while that work runs?
3. Which partial orders are required by the product?
4. Which order is merely convenient for one test?
5. Can a next-tick or microtask chain replenish itself indefinitely?
6. What bounds one uninterrupted CPU region?
7. Which yield reaches an ordinary event-loop phase?
8. Is final output reconstructed by source identity rather than callback arrival order?
9. What is the maximum cancellation latency between checkpoints?
10. Which later course mechanism would be required if cooperative chunking is insufficient?

## 12. Portability clinic: testing the contract across Node releases

Event-loop explanations often fail because they confuse a useful implementation picture with a stable API promise. Node’s phase model is important, but a test suite should not require an incidental trace unless the trace itself is the program under test. ESM evaluation, top-level promise jobs, I/O context, platform timer granularity, and changes in libuv can alter an observed sequence while preserving every documented product guarantee.

Classify every scheduling test before writing it:

- A **language-order test** verifies relations such as synchronous execution before a promise continuation created inside that turn.
- A **Node contract test** verifies behavior promised by a Node API, such as a timer not running before its threshold or a disposed immediate not invoking its callback.
- An **application-order test** verifies sequencing your own code establishes, such as TaskHarbor writing a terminal outcome before publishing `taskSucceeded`.
- An **observatory test** records one environment and is informative rather than normative.

The categories require different assertions. An observatory may snapshot all labels together with Node version and execution context. A production test should assert only the edges that matter. For example, instead of requiring `['sync', 'microtask', 'timer', 'immediate']`, assert that `sync` precedes all scheduled work, the microtask runs before a later explicitly awaited immediate, and final results are independent of timer/immediate order.

## 13. Quantifying a blocking budget

“Do not block the event loop” is too vague to guide design. Establish a workload bound and a responsiveness objective. If a transformation takes approximately 2 microseconds per record and a callback should yield within 10 milliseconds, a first chunk estimate is 5,000 records. That estimate is not a permanent truth; Course 9 will measure it under representative load. Here it gives a reviewable starting policy.

The chunk must account for worst-case inputs, not only average data. Regular expressions with pathological behavior, sorting with expensive comparators, and validation that builds large diagnostics can violate a simple per-record estimate. Place input-size checks before the expensive region, cap diagnostic accumulation, and test an adversarial record at the edge of the documented limit.

A cooperative algorithm should also decide what happens to partial work after cancellation. A pure map can discard its private output. An operation mutating shared state needs candidate-state construction or a per-chunk commit protocol. Fair scheduling and failure atomicity are separate requirements; yielding more frequently does not automatically make partial mutation safe.

## Practice sequence

1. Predict the module-specific investigation cases before running the checker or Node.
2. Draw the state, ownership, queue, or lifecycle model required by this chapter.
3. Complete [the workbook](workbook.md), recording the first causal difference between your prediction and the observed result.
4. Build [Event Loop Observatory](../../labs/module-31-event-loop-observatory/README.md) from the starter without opening the reference.
5. Integrate the corresponding TaskHarbor increment and add evidence at the layer that owns the claim.
6. Complete the unseen transfer and explain one unsupported guarantee explicitly.
7. Compare with [the reasoned solutions](solutions.md) only after your own design passes its tests.

## Ready to continue

You are ready to leave Module 31 when you can derive its behavior from the underlying runtime model, not from remembered output; when the laboratory’s terminal paths are all tested; and when you can apply the same mechanism to a different domain without weakening ownership, boundedness, cancellation, or deterministic-reporting requirements.

## Primary references

- Node.js API documentation: <https://nodejs.org/api/>
- ECMAScript specification: <https://tc39.es/ecma262/>
- TypeScript documentation: <https://www.typescriptlang.org/docs/>

## Continue

[Module 32](../module-32-promises-async-functions-and-task-ownership/index.md)
