# Module 36 Workbook — Async Iterables and Pull-Based Sequences

## A. Trace the protocol

1. Write the shapes of `AsyncIterable<T>`, `AsyncIterator<T>`, and `IteratorResult<T>`.
2. Explain what `for await` does after `break`.
3. Distinguish a repeatable async iterable from a one-shot iterator.
4. Explain why yielding a promise from an async generator does not expose a nested promise to the consumer.

## B. Find false backpressure

An EventEmitter-to-iterator adapter stores emitted values in an unbounded array.

5. Why does consumer-side `for await` not bound that array?
6. Choose one overflow policy and state what the producer and consumer observe.
7. Explain when real producer backpressure is impossible with EventEmitter.

## C. Design queue states

Draw states for open, closing-with-buffer, closed, failed, and consumer-returned. Include waiting producers and consumers.

8. What happens to buffered items after normal close?
9. What happens after failure?
10. What happens when the consumer breaks early?
11. May a second consumer attach?

## D. Construct a bounded queue

Implement `push`, `take`, `close`, `fail`, and `[Symbol.asyncIterator]`. When full, `push` waits and its promise owns one pending producer. Consuming an item admits exactly one waiting producer. All abort listeners are removed on settlement.

## E. Independent laboratory

Complete [Bounded Async Queue](../../labs/module-36-bounded-async-queue/README.md). Add tests for FIFO producer admission, close-after-drain, failure discarding buffered values, early return, producer abort, and second-consumer rejection.

## F. TaskHarbor transfer

Expose lifecycle events as a bounded async sequence. Decide overflow behavior for a slow observer. The sequence must close after run completion, detach its event subscription on early return, and remain observational rather than authoritative.

## G. Unseen transfer

Design a paginated API cursor as an async iterable. State page fetch ownership, prefetch policy, cancellation, retry, rate limits, and behavior when the consumer stops after the first item of a page.

## I. Concurrent-pull exercise

Call `next()` three times before pushing values. Specify which waiter receives each value and what normal close returns to the remaining waiter. Then call `return()` while two pulls are pending and prove neither promise remains unresolved.

## J. Adapter cleanup

Implement conceptual `take(source, count)` and `map(source, transform)` async generators. Show the `try/finally` required to call upstream `return()` on early consumer break. Test upstream failure and transform failure separately.

## K. Capacity in bytes

A queue capacity of ten accepts 20 MB buffers. Rewrite the capacity policy around both item count and retained bytes. State overflow behavior and how a blocked producer learns that capacity is available.

## L. Async adapter contract

Specify a `takeUntil` adapter over an async iterable. Define behavior when the predicate throws, the signal aborts, the limit is already satisfied, upstream `return()` fails, or the consumer stops early. Your solution must preserve the primary failure while making cleanup failure observable.

Next design `mapConcurrent(source, width, mapper)`. State pull bound, active bound, output order, failure policy, cancellation propagation, and what happens to already-started mapper calls after the first failure.

## M. Multi-consumer design choice

A caller asks to let several consumers iterate the same asynchronous event source. Compare work sharing, broadcasting, replay, and independent source subscriptions. For each model, define item ownership, slow-consumer policy, capacity, terminal state, and whether one consumer’s cancellation affects the others.

Design a broadcast queue with per-consumer cursors and a global retention bound. Explain what happens when one consumer falls behind the retention window. A solution that silently grows one array forever is not bounded.

## N. Pull and retention review

A parser yields borrowed views into a reusable buffer. Explain why the next pull cannot safely overwrite that buffer while the prior view remains in use. Compare copying each item, leasing the buffer, and changing the item representation. State which later stream or memory mechanisms could alter the trade-off.

Add one test that detects accidental source retention after the consumer finishes.

## H. Defense

Explain why async iteration is a protocol rather than a queue, why close and failure differ, and why one consumer pulling slowly does not automatically slow a push-only producer.
