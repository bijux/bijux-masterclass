# Module 36 Reasoned Solutions — Async Iterables and Pull-Based Sequences

## A. Protocol

An async iterable supplies `[Symbol.asyncIterator]`; an async iterator supplies `next()` returning a promise of `IteratorResult<T>`. Early loop exit invokes `return()` when present, giving the source a cleanup opportunity. An iterable can create a fresh iterator per call; a one-shot queue may return only one iterator and reject subsequent claims.

## B. Backpressure

The adapter’s array grows before the consumer asks for values. `for await` controls consumer demand only at the adapter boundary. If the emitter cannot await publication, true blocking backpressure cannot propagate. The adapter must use a finite buffer and choose overflow rejection, dropping, coalescing, or detachment. That choice is product semantics.

## C. State model

Normal close preserves buffered items and yields done only after drain. Failure usually rejects pending and future reads and may discard buffered data according to contract. Consumer return detaches the source and must settle blocked producers. A single-consumer queue rejects another iterator claim; broadcast requires a different data structure.

## D. Queue implementation

A full queue stores a producer waiter containing value, resolve, reject, signal, and abort listener. Taking one buffered value frees one slot and admits exactly one producer in FIFO order. Every terminal path removes listeners. Early iterator return fails or closes the queue according to the documented contract so no producer remains suspended forever.

## E. TaskHarbor and transfer

TaskHarbor’s event sequence subscribes to the typed hub, uses finite capacity, and closes on run completion. Early return unsubscribes. A slow observer may receive an explicit overflow failure; it must not delay scheduler authority unless the API was designed as awaitable publication.

For a paginated cursor, each `next` may own a page fetch. Prefetch of one page can improve latency but adds retained state and cancellation responsibility. Early return aborts an in-flight prefetch and discards unused page items under a documented policy.

## F. Pull and adapter solutions

Pending pulls form a FIFO consumer queue. Each pushed item resolves the oldest waiter. Normal close resolves all remaining waiters with done only after accepted buffered items are delivered. Early return must detach upstream and settle every waiter according to the queue’s terminal policy.

An async-generator adapter should obtain the upstream iterator explicitly or rely on `for await` inside `try/finally`; on early termination, closure propagates. Transform failure rejects the outer sequence and closes upstream. `take` closes upstream as soon as its count is reached, rather than leaving the source active.

Count-only capacity is insufficient for variable-size items. Track retained bytes and admit only when both limits permit. Capacity release after consumption wakes an appropriate producer. This prepares the reader for stream high-water marks without pretending the queue already implements Node streams.

## G. Adapter and close answers

`takeUntil` must call upstream `return()` when it terminates before natural exhaustion. Predicate failure remains the primary failure; cleanup failure should be attached as a cause or represented in an aggregate rather than replacing it. Consumer early return reaches the adapter’s own `return`, which forwards close upstream exactly once.

A concurrent mapper stores lazy pulls and mapper calls under separate bounds. Source order requires indexed slots; completion order can yield as soon as each mapper settles but is a different API. On failure, request cancellation, stop new pulls, join already-started work, close upstream, and return one documented failure shape. Simply rejecting on the first mapper error leaves work and cleanup unowned.

## H. Multi-consumer answers

Work sharing delivers each item to one consumer. Broadcast delivers every item to every live consumer and therefore needs per-consumer lag policy. Replay additionally retains history. Independent subscriptions duplicate source work. Calling all four “multiple consumers” conceals different ownership and capacity contracts.

A bounded broadcast queue can retain a fixed sequence window and store one cursor per consumer. When a cursor falls behind the oldest retained sequence, the consumer receives an explicit lag error or snapshot-resync requirement. Silently dropping data or retaining history without bound violates the declared protocol.
