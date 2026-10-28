# Module 36 — Async Iterables, Generators, and Pull-Based Sequences

> **Question:** How do you represent a sequence whose next value arrives asynchronously while preserving demand, cleanup, cancellation, and bounded memory?

## Why this comes now

Module 35 established the preceding async contract. This module adds the next responsibility without discarding that earlier ownership and compatibility discipline.

## Outcomes

By the end of the module, you can:

- describe the AsyncIterator next, return, and throw protocols;
- distinguish one-shot iterators from repeatable async iterables;
- use async generators with finally-based cleanup;
- explain how for-await handles early break and iterator return;
- bridge push producers to pull consumers through an explicit bounded queue;
- define close, failure, cancellation, and producer-backpressure semantics;

## 1. Async iteration is a protocol

An async iterator has a `next` method returning a promise of an iterator result. The result is either `{ done: false, value }` or a terminal `{ done: true, value }`. An async iterable has `[Symbol.asyncIterator]` and returns an iterator. Often one object implements both.

This protocol makes arrival time part of traversal without forcing the entire sequence into memory. `for await` repeatedly awaits `next`. It also performs cleanup: an abrupt `break`, `return`, or thrown error asks the iterator to close through `return` when available.

The protocol says nothing about repeatability. A generator instance is one-shot. A factory object can create a fresh generator for every traversal. Document which behavior consumers receive.

## 2. Pull is not automatically backpressure

An async iterator is consumed by pull: the consumer requests the next item. But the underlying producer may still be push-based. An EventEmitter adapter can receive a thousand events before the consumer asks for the second item. The adapter then needs a buffer, drop policy, block policy, or failure policy.

Backpressure exists only when producer progress is coupled to available capacity. If `push` returns a promise that resolves when the bounded queue has space, cooperative producers can wait. If producers cannot wait—such as an external event source—the queue must reject, drop, coalesce, or disconnect according to an explicit overload policy.

Course 5 studies Node streams and their built-in backpressure contracts. Here, you build the smaller async-queue mechanism directly so the hidden buffer cannot remain mysterious.

## 3. Async generators store state across suspension

An async generator combines a state machine with the iterator protocol. Local variables survive between `yield` points. `try/finally` runs when iteration ends normally, throws, or is closed through `return`.

```ts
async function* poll(signal: AbortSignal): AsyncGenerator<string> {
  try {
    while (true) {
      signal.throwIfAborted();
      yield await readNext(signal);
    }
  } finally {
    await closeSource();
  }
}
```

The cleanup guarantee depends on the consumer using the protocol. If code calls `next()` and then abandons the iterator without `return`, cleanup may not run promptly. High-level `for await` handles early loop exit, but custom consumers must own closure explicitly.

## 4. Close and failure are distinct terminal states

A queue closes when no more values will arrive. Pending consumers receive `done: true` after buffered values are drained. A queue fails when no more valid values will arrive because of an error; pending and future consumers should reject after the chosen buffer policy. Decide whether buffered values are delivered before failure or discarded immediately.

Pending producers also need a terminal outcome. Closing a bounded queue while producers wait for capacity should reject those pushes; silently resolving would claim the value was accepted. A consumer’s early `return` may close a single-consumer queue and reject producers, or it may only detach that subscriber in a broadcast architecture. State the topology.

## 5. Cancellation and listener cleanup

A pending `next` or `push` can accept an `AbortSignal`. On abort, remove its waiter from the queue and reject with the signal reason. Leaving the waiter installed creates a ghost operation that may later consume capacity or receive a value after its caller has stopped waiting.

The queue itself may also have a lifetime signal. When that signal aborts, transition the queue to a terminal state exactly once and settle all waiters. Repeated close, fail, or abort calls should be idempotent or rejected according to one documented rule.

## 6. A bounded queue state model

A single-consumer bounded queue has four relevant collections or states: buffered values, waiting consumers, waiting producers, and terminal state. Most operations can be reasoned about as transfers among them.

On push: deliver directly to a waiting consumer; otherwise buffer if capacity exists; otherwise register the producer. On next: remove a buffered value and admit one waiting producer; otherwise return terminal; otherwise register the consumer. On close: stop new producers, let buffered values drain, then finish consumers. On fail: stop both sides and reject according to policy.

Write these transitions before coding. Queue bugs often come from handling happy-path values while forgetting a producer blocked during closure or an aborted consumer in the middle of the waiter array.

## 7. Async iteration as a public library surface

Returning `AsyncIterable<T>` hides the concrete iterator but also hides some controls. Consumers cannot necessarily ask for queue depth, cancellation, or replay. Provide a separate owner object when those controls are part of the contract. Avoid returning an async generator that closes over a mutable service without explaining whether multiple consumers are allowed.

Type declarations should preserve item types and terminal errors as far as JavaScript’s exception model allows. Runtime errors still travel through promise rejection; TypeScript does not encode a checked error type for async iteration.

## 8. What this changes in TaskHarbor

TaskHarbor adds `events(signal): AsyncIterable<HarborEvent>` for consumers that prefer pull-based observation. Internally, the adapter uses a bounded queue and one EventHub subscription. Breaking the loop unsubscribes and closes the queue. If the consumer falls behind, the adapter follows a documented overflow policy rather than growing without bound.

The scheduler remains authoritative. Event iteration can be disabled entirely without changing final outcomes.

## 9. Deep case study: an event bridge without backpressure

A library converts EventEmitter events into an async iterable by pushing every event into an array. The consumer processes ten items per second while the producer emits ten thousand. The `for await` syntax looks pull based, but the bridge is push driven and unbounded. Memory grows with the producer-consumer gap.

A correct bridge needs a capacity and a policy: block or slow the producer when possible, reject new items, drop oldest, drop newest, coalesce, or fail the sequence. EventEmitter itself cannot await producer backpressure, so the bridge may need to reject overflow explicitly. Pull syntax at the consumer boundary does not create upstream flow control by magic.

## 10. Iterator terminal-state table

Separate these transitions:

| Transition | Consumer observation | Producer obligation |
|---|---|---|
| normal close after drain | `{ done: true }` | release waiters after buffered items |
| failure | rejected `next()` | reject pending producer and consumer waiters |
| consumer early return | iterator `return()` | detach source, decide fate of buffer and producers |
| abort | rejected or typed terminal result | remove abort listener and release capacity |

Conflating close and failure loses information; ignoring early return leaks source subscriptions.

## 11. Single-consumer versus broadcast sequences

A queue naturally assigns each item to one consumer. A broadcast stream requires per-subscriber positions or buffers and a slow-subscriber policy. Do not add a second consumer to a single-consumer queue and assume both see all items. Cardinality and delivery semantics belong in the public type and documentation.

## 12. Concurrent `next()` calls

An async iterator may receive another `next()` call before the previous one settles. Some iterators serialize these requests; others reject concurrent pulls. Async generators queue requests internally, but a custom queue implementation must define its own behavior. If multiple pending consumers are allowed, the source assigns items in request order. If only one active `next` is allowed, enforce it with a clear error.

The laboratory queue supports one consumer but can have several pending `take` calls from that consumer. Its consumer-waiter queue therefore needs FIFO behavior. Early `return()` must settle every pending waiter; otherwise a caller can break from iteration while another pull remains permanently pending.

## 13. Transformation pipelines over async iterables

Mapping, filtering, taking, and batching async values can be expressed as async generators. Every adapter adds a cancellation and cleanup obligation. `take(5)` must close its upstream iterator after the fifth item. `map` must propagate upstream failure. `filter` can pull many inputs before yielding one output, so demand at the output does not imply one-for-one upstream work.

When adapters are composed, `return()` should travel upstream through `finally`. This is the sequence counterpart of task joining: the outer consumer owns closure of the traversal chain.

## 14. Retention and item lifetime

A buffered sequence owns item references until delivery or discard. Large items make a small numeric capacity expensive. Document capacity in both item count and, where relevant, bytes. If an item is a view into mutable backing storage, define how long it remains valid. Course 5 will apply these questions to Buffer chunks and streams.

## 15. Demand, storage, and delivery are three separate counters

An async iterable API often says “bounded” while bounding only one queue. A complete capacity model tracks at least three quantities: producer demand that has not yet been accepted, accepted items stored for a consumer, and consumer requests waiting for a future item. Depending on the product, bytes may matter more than item count. One enormous item can violate a memory promise even when the queue contains only one entry.

For a bounded queue, define the commit point. Before commit, `push` may reject without owning the item. After commit, the queue owns the item until one of three terminal paths occurs: delivery to a consumer, explicit queue cancellation with a documented discard policy, or queue failure with cleanup. A waiting producer is not yet committed merely because it has returned a promise. The promise represents a pending admission decision.

This model prevents a common false-backpressure design: an event listener eagerly receives every producer event, appends each item to an unbounded array, and exposes an async iterator over that array. The consumer is pull-based, but the producer is not controlled. Real backpressure requires admission to propagate to the producer or an explicit overload policy when propagation is impossible.

## 16. Iterator adapters must preserve terminal behavior

A synchronous `map` is simple because callback execution and iteration happen in one stack. An async adapter must also preserve cancellation, upstream `return()`, failure identity, and in-flight work. Consider `take(10)`: after the tenth item, it should close the upstream iterator rather than merely stop calling `next`. Consider `mapAsync` with concurrency greater than one: it must define output order, maximum started work, what happens after one mapping failure, and whether already-started operations are joined.

Write an adapter contract using five fields:

| Field | Required question |
|---|---|
| demand | how many upstream pulls may be outstanding? |
| order | source order, completion order, or explicit keys? |
| failure | fail immediately, accumulate, or represent as items? |
| close | when is upstream `return()` invoked? |
| cancellation | which signal reaches upstream and in-flight callbacks? |

This is the bridge from iterator syntax to runtime architecture. Later stream courses can add byte-oriented buffering and Node stream interoperation; this module establishes the protocol obligations that those abstractions must still honor.

## Practice sequence

1. Predict the module-specific investigation cases before running the checker or Node.
2. Draw the state, ownership, queue, or lifecycle model required by this chapter.
3. Complete [the workbook](workbook.md), recording the first causal difference between your prediction and the observed result.
4. Build [Bounded Async Queue](../../labs/module-36-bounded-async-queue/README.md) from the starter without opening the reference.
5. Integrate the corresponding TaskHarbor increment and add evidence at the layer that owns the claim.
6. Complete the unseen transfer and explain one unsupported guarantee explicitly.
7. Compare with [the reasoned solutions](solutions.md) only after your own design passes its tests.

## Ready to continue

You are ready to leave Module 36 when you can derive its behavior from the underlying runtime model, not from remembered output; when the laboratory’s terminal paths are all tested; and when you can apply the same mechanism to a different domain without weakening ownership, boundedness, cancellation, or deterministic-reporting requirements.

## Primary references

- Node.js API documentation: <https://nodejs.org/api/>
- ECMAScript specification: <https://tc39.es/ecma262/>
- TypeScript documentation: <https://www.typescriptlang.org/docs/>

## Continue

[Module 37](../module-37-async-context-correlation-and-diagnostic-boundaries/index.md)
