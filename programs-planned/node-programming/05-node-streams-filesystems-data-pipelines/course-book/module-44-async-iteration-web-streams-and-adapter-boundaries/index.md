# Module 44 — Async Iteration, Web Streams, and Adapter Boundaries

**Progress: 44/100**

## The governing question

> When should a streaming computation be expressed as a Node stream, an async iterable, or a Web Stream, and what lifecycle semantics are changed by crossing between them?

## Why this module comes now

Module 43 established linear pipeline ownership. Node now exposes several interoperable sequence protocols. Async iterables make control flow explicit; Node streams integrate deeply with operating-system resources; Web Streams support platform APIs and transferable abstractions. Adapters preserve data only when the reader also preserves cancellation, backpressure, chunk types, and close behavior.

Module 43 proved how a push-oriented stream graph regulates demand. Module 44 adds a second vocabulary: async iterables let consumers request one item at a time through `next()`. The mechanisms can interoperate, but their lifecycle contracts are not identical. Course 2’s iterator protocol and Course 4’s async-generator cleanup now meet Node stream destruction and Web Stream locking.

The design goal is not to convert everything into one fashionable abstraction. It is to choose the boundary whose demand, cancellation, and close operations match the product and to make adapter consequences explicit.

## Observable outcomes

By the end of this module, you can:

- consume Readable streams through async iteration without losing cleanup ownership

- write async generators that propagate cancellation and close upstream work on early return

- adapt among Node streams, async iterables, and Web Streams while tracing backpressure direction

- distinguish one-shot iterators from repeatable iterable factories

- select an abstraction based on lifecycle and boundary requirements rather than style preference

## The module ledger

Use this ledger while reading examples and before writing the laboratory design. It is deliberately specific to this module.

| Dimension | Question to answer |
|---|---|
| sequence identity | Is the value one-shot, repeatable, or a factory that creates a fresh sequence? |
| demand owner | Who calls `next`, reads, or pulls the next chunk? |
| early stop | What does `return()` or loop exit do to the upstream resource? |
| error channel | Does failure reject iteration, error the stream, or both through an adapter? |
| lock state | Does an adapter acquire an exclusive reader or writer lock? |
| chunk contract | Are adapters preserving bytes, strings, objects, and ownership semantics? |

## Async iteration turns demand into control flow

A for-await loop requests the next item only after the previous body iteration completes. This naturally couples downstream work to upstream demand and often makes transformations clearer than event listeners. The loop owner can use try/finally to release resources. Breaking early normally invokes iterator.return; for a Node Readable async iterator this can destroy the stream, which is appropriate only when the loop owns it.

Readable.iterator with destroyOnReturn false changes that policy. It should be used only when another scope still owns the remaining stream. Early return without an explicit owner is not resource reuse; it is an orphaned source.

## Async generators are state machines with cleanup

An async generator can transform an AsyncIterable without creating a custom Transform class. Its local variables become retained state across yields. The generator should check an AbortSignal around waits, use finally for cleanup, and avoid retaining large chunks after emitting a smaller result. Yielding a subarray can retain the entire source allocation if the consumer keeps it.

Generator code can express one-to-many and many-to-one transformations naturally. The cost model must account for any buffered accumulator. A line splitter, for example, must bound the unfinished line rather than rely on demand alone.

## Node and Web Streams share concepts but not identical APIs

Readable.toWeb and Readable.fromWeb bridge stream families. A Web ReadableStream is acquired through a reader lock; a Node Readable uses EventEmitter state and destroy semantics. Cancellation, close, and error translation are part of the adapter. The reader must test which side owns cancellation and what happens to the underlying resource when the adapted consumer stops.

Chunk types also matter. A byte-oriented Web stream may use Uint8Array, while Node commonly uses Buffer. Since Buffer is a Uint8Array, type compatibility can hide allocation and aliasing differences. Normalize ownership at the boundary if the adapted consumer may retain or mutate chunks.

## One-shot versus repeatable sources is a public contract

A stream instance and an iterator object are generally one-shot. An object whose Symbol.asyncIterator method constructs a fresh source can be repeatable. APIs should not accept AsyncIterable and then silently iterate it twice. If two passes are required, request a factory, materialize within a bound, or redesign the algorithm for one pass.

Testing should include a source that throws when iterated twice. This detects accidental replay assumptions that arrays conceal.

## Adapter boundaries can erase useful capabilities

A Readable has readableLength, destruction state, and Node-specific diagnostics. An AsyncIterable exposes only next, return, and throw. A Web Stream exposes locking and desired-size concepts. Adapting to the smallest abstraction can improve decoupling, but callers can no longer observe or control omitted capabilities. That is beneficial only when those capabilities are not part of the public contract.

Prefer accepting AsyncIterable for pure item transformations and returning AsyncIterable when no Node resource must be exposed. Prefer Node streams for fs, child-process, compression, and existing stream pipeline integration. Use Web Streams at web-platform boundaries, not merely to rename familiar operations.

## Async iteration is a lifecycle protocol

`for await` repeatedly requests values and awaits each result. Exiting early invokes the iterator’s `return()` when present, giving generators an opportunity to run `finally` cleanup. A Node Readable’s async iterator also owns interaction with the stream; early exit commonly destroys the stream unless a different iterator option is chosen. That behavior must be part of the API promise.

A function returning an `AsyncIterable<T>` may be returning a one-shot resource wrapper or a repeatable value. The type alone does not distinguish them. Use documentation, factories, or explicit naming so callers do not assume a consumed file stream can be iterated again.

## Adapters preserve less than they appear to

Converting Node streams to Web Streams or vice versa maps chunks, pressure, errors, and cancellation through an adapter. It does not erase differences in locking, object mode, close semantics, or chunk types. A Web `ReadableStream` has an explicit lock while a default reader is active. A Node stream may carry Buffers and expose events not represented by the Web interface.

Treat each adapter as a protocol boundary. Test early cancellation, error propagation, and exact chunk data. Do not rely on the fact that a happy-path round trip produced the same concatenated bytes; that proves little about cleanup or pressure.

## Async-generator adapters can express domain stages clearly

For record-level transformations, an async generator often communicates logic more directly than a custom Transform: consume a typed item, validate or transform it, yield zero or more typed items, and run cleanup in `finally`. The generator still needs a bounded upstream and must not retain unbounded history.

When the surrounding system is a stream pipeline, adapt at a deliberate edge rather than repeatedly moving back and forth. Every conversion adds another owner and another terminal mapping to the lifecycle proof.

## Worked case — A cancellation-aware batching generator

```ts
export async function* batch<T>(
  source: AsyncIterable<T>,
  size: number,
  signal?: AbortSignal,
): AsyncGenerator<readonly T[]> {
  if (!Number.isInteger(size) || size <= 0) throw new RangeError('size must be positive');
  let current: T[] = [];
  try {
    for await (const item of source) {
      signal?.throwIfAborted();
      current.push(item);
      if (current.length === size) {
        yield current;
        current = [];
      }
    }
    if (current.length > 0) yield current;
  } finally {
    current = [];
  }
}
```

The generator is one-pass and bounds its own retained item count by size. It cannot bound the size of each T, so a byte budget requires a different policy. The yielded array is no longer mutated after yield because a new array is created. Clearing current in finally releases a partially built batch after abort or early return. Cancellation does not automatically stop a source that ignores iterator.return or its own signal; that obligation remains upstream.

## Extended case analysis

A `take(source, 10)` adapter returns after ten records. If `source` is a file-backed Readable, early return must release the file resource. If `source` is a repeatable in-memory iterable, no destruction is needed. The same generic signature can therefore hide different cleanup consequences. A strong adapter either owns early close correctly or states that the caller retains source ownership.

## What this mechanism establishes

A correct implementation establishes these local facts:

- Each yielded batch owns an array that later iteration does not mutate.

- Batch size is a positive integer and take count is a nonnegative integer.

- Abort is checked before retaining additional items.

It does **not** establish the stronger claims hidden by these shortcuts:

- yielding one mutable batch array repeatedly;

- collecting the whole source before batching;

Those distinctions are part of the public contract. Later modules may add stronger guarantees, but they must not be backdated into this mechanism.

## Decision procedure

1. Identify whether the source is a resource, a sequence, or both.

2. State whether the value is one-shot or repeatable.

3. Choose the abstraction whose lifecycle operations match the caller’s responsibility.

4. Trace demand and cancellation in both directions through every adapter.

5. Normalize chunk ownership when an adapter crosses Buffer and Uint8Array expectations.

6. Test early return, source error, consumer error, abort, and repeated iteration.

Make each answer visible in an API, graph, or test. Labels such as “streaming,” “safe,” and “atomic” are incomplete until representation, owner, bound, and terminal evidence are named.

## Common wrong models

### Assuming async iteration makes every source bounded

The iterator controls demand, but a source or transform may still buffer independently.

### Breaking a loop and reusing the stream

The default Node async iterator can destroy the Readable on early return.

### Adapting without testing cancellation

Data may flow while the underlying handle or reader lock remains open after stop.

### Yielding tiny views of huge buffers

The consumer can retain the entire backing allocation.

## Apply the mechanism in FlowLedger

Express FlowLedger’s record transforms as async-generator stages where that improves clarity. Preserve pipeline cancellation and keep the byte-to-record trust boundary explicit.

Before editing FlowLedger, record the changed edge, owner, bound, and success observation. Update implementation, errors, tests, documentation, and report as one feature.

## Independent transfer

Design an API that tails a log file as an AsyncIterable of validated records. Explain who owns the FileHandle, what early return does, and whether a second iteration reopens the file.

The transfer is successful when the new design preserves the module’s governing relationship without copying the laboratory’s domain names or relying on its exact data shape.

## Practice sequence

1. Reconstruct the module ledger from memory.
2. Read the worked case and mark every copy, view, queue, wait, and terminal observation.
3. Predict all eight Module 44 investigations before running them.
4. Complete the workbook’s diagnosis section without broad assertions or whole-input shortcuts.
5. Build **Async Record Window** from the starter package.
6. Compare only after your adversarial tests pass, beginning with the first different design decision.
7. Transfer the mechanism into FlowLedger and explain one earlier-course invariant that could regress.

## Readiness standard

Continue only when you can:

- Consume Readable streams through async iteration without losing cleanup ownership

- Write async generators that propagate cancellation and close upstream work on early return

- Adapt among Node streams, async iterables, and Web Streams while tracing backpressure direction

- Distinguish one-shot iterators from repeatable iterable factories

- Select an abstraction based on lifecycle and boundary requirements rather than style preference
- explain which observation is necessary but insufficient for product completion;
- state one capacity or durability guarantee this module deliberately does not make;
- defend the laboratory’s failure path without reading the reference source.

## Primary references

- [https://nodejs.org/docs/latest-v24.x/api/stream.html#streams-compatibility-with-async-generators-and-async-iterators](https://nodejs.org/docs/latest-v24.x/api/stream.html#streams-compatibility-with-async-generators-and-async-iterators)
- [https://nodejs.org/docs/latest-v24.x/api/webstreams.html](https://nodejs.org/docs/latest-v24.x/api/webstreams.html)

The chapter is self-contained. These links are primary-source routes for checking version-sensitive Node.js details.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-44-async-record-window/README.md)
- [FlowLedger engineering guide](../capstone.md)
