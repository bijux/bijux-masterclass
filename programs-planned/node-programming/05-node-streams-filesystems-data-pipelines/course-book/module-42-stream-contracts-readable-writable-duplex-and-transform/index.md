# Module 42 — Stream Contracts: Readable, Writable, Duplex, and Transform

**Progress: 42/100**

## The governing question

> What state does a Node.js stream own, which side is readable or writable, and which observation proves that the resource has actually completed?

## Why this module comes now

Module 41 established the semantics of individual byte ranges. A stream is not a larger Buffer. It is a stateful protocol that produces or accepts a sequence over time, owns internal queues, publishes events, and eventually reaches terminal states. The reader must understand those states before composing pipelines.

Module 41 described one bounded region of bytes. A stream replaces that single value with an evolving protocol: chunks may arrive later, internal queues may fill, and readable and writable halves can reach terminal states independently. The object-model work from Course 2 matters here because stream properties and events expose state, not a declarative history. Course 4’s lifecycle discipline matters because the code that creates a stream graph must also own its termination.

The central correction is to stop asking “does this object contain the data?” and ask “which operation may occur next, which queue owns pending data, and which terminal observation closes this side of the protocol?”

## Observable outcomes

By the end of this module, you can:

- distinguish Readable, Writable, Duplex, Transform, PassThrough, byte mode, and object mode

- trace readable and writable state without mixing incompatible consumption styles

- separate end, finish, close, error, destroy, and abort observations

- implement a small custom stream while respecting callback and terminal contracts

- choose stream APIs only when incremental data and bounded buffering are actual requirements

## The module ledger

Use this ledger while reading examples and before writing the laboratory design. It is deliberately specific to this module.

| Dimension | Question to answer |
|---|---|
| role | Is this value readable, writable, duplex, transforming, or only observing? |
| unit | Does one chunk represent bytes, decoded strings, or domain objects? |
| consumption mode | Will the reader use `pipe`, events, `read`, or async iteration—and only one primary mode? |
| queue state | What is buffered on the readable side and what is queued on the writable side? |
| terminal state | Which of `end`, `finish`, `close`, `error`, or destruction applies to each side? |
| owner | Which scope constructs, connects, destroys, and awaits the complete graph? |

## A stream is a protocol plus buffered state

Readable and Writable name directions relative to the JavaScript consumer. A Readable produces chunks that the consumer reads. A Writable accepts chunks that the consumer writes. Duplex owns both directions, which are independent unless the product links them. Transform is a Duplex whose readable output is derived from writable input. These names describe capabilities, not files or sockets specifically.

Each side owns an internal queue. highWaterMark is a threshold used by the protocol, not a hard memory cap and not necessarily the largest chunk. In byte mode it is generally measured in bytes; in object mode it is measured in objects. A one-megabyte object still counts as one object. Capacity claims must therefore be stated in the unit the stream actually controls.

## Readable consumption style is a design choice

Readable streams can be consumed through data events, readable/read calls, pipe, pipeline, or async iteration. Mixing styles can move the stream between paused and flowing states in ways that obscure ownership and loss. A module should select one primary consumption style and encapsulate it. Application code in this course prefers pipeline for linear byte flows and async iteration for explicit control-flow transforms.

Attaching a data listener starts flowing consumption. Calling pause does not undo chunks already delivered. Async iteration creates a loop-shaped owner for each chunk and gives early exit a defined destroy behavior unless a non-destroying iterator is selected. The choice changes cleanup semantics, so it belongs in the API decision rather than being treated as syntax.

## Terminal events answer different questions

end means a readable has no more data. finish means a writable has accepted end and flushed its implementation callbacks. close means the underlying resource has closed. error reports failure but does not, by itself, prove every side is closed. destroyed is local state, not a promise that operating-system cleanup is complete. The correct terminal observation depends on what the caller owns.

For a complete pipeline, await stream/promises.pipeline. For a single stream whose readable or writable lifecycle you own, await finished with the appropriate options and cleanup. If a FileHandle, child process, or external resource is also owned, its terminal condition remains separate from the stream wrappers.

## Custom stream implementations obey callback discipline

A custom Writable calls its _write callback exactly once after the chunk has been accepted or rejected. A custom Readable calls push when data is available and pushes null exactly once to signal end. A Transform never runs _transform concurrently for one instance; this serial property can simplify incremental parser state. Throwing asynchronously instead of passing an error to the callback can escape the stream lifecycle.

Stream implementation hooks are not ordinary public methods. The public write, read, pipe, and destroy methods coordinate buffering and terminal state around them. Calling internal methods directly bypasses that protocol.

## Object mode changes unit, not responsibility

Object-mode transforms are useful after framing and validation have converted bytes into trusted domain values. They should not receive arbitrary unbounded objects from hostile input without upstream limits. The transition from byte mode to object mode is a trust boundary: before it, chunks are partial representation; after it, each item should satisfy a defined schema.

Duplex streams can use readableObjectMode and writableObjectMode independently. This is useful for a parser that accepts bytes and emits records, or a serializer that accepts records and emits bytes. The two high-water marks use different units and should be configured separately.

## Readable and writable termination are different statements

Readable `end` means the source has no more data to provide. Writable `finish` means all data passed to `end()` has been processed by the writable implementation. `close` concerns release of the underlying resource and is not guaranteed to mean that semantic processing succeeded. A duplex stream can finish its writable side while its readable side remains open, or end its readable side while still accepting writes.

A product operation usually needs a stronger condition than any one event. The owner should await the completion primitive that covers the complete graph and then interpret that completion relative to external commit. This is why a Transform callback, a readable `end`, and a final-file rename belong to three different levels of the design.

## Choose one primary consumption mode

Node exposes events, `pipe`, async iteration, and manual `read()` because different integrations need different control. Mixing modes can move a readable into flowing state unexpectedly, consume chunks twice conceptually, or make cleanup difficult to reason about. A library should choose one primary consumption protocol and expose adapters deliberately rather than attaching opportunistic `data` listeners.

Observation is different from consumption. A state monitor can listen for terminal events without becoming the data consumer. A debugging listener that retains chunks, however, has changed memory behavior and should be treated as a branch rather than harmless observation.

## Custom streams are protocol implementations

Implementing `_read`, `_write`, or `_transform` means implementing a callback and state protocol. The callback must be invoked exactly once. Exceptions and callback errors become stream failure. A Transform must not call its callback before it has finished using the input chunk if the chunk can be mutated or reused by the producer.

Start with the smallest custom stream that reveals the needed policy. Many tasks are better represented by async generators or existing Transform constructors. A custom class is justified when the component owns incremental internal state, needs a precise stream role, or must integrate with stream-specific pressure and lifecycle signals.

## Worked case — A counted byte transform

```ts
import { Transform, type TransformCallback } from 'node:stream';

export class ByteCounter extends Transform {
  #bytes = 0;

  get bytes(): number { return this.#bytes; }

  override _transform(
    chunk: Buffer,
    _encoding: BufferEncoding,
    callback: TransformCallback,
  ): void {
    this.#bytes += chunk.length;
    callback(null, chunk);
  }
}
```

ByteCounter is a transparent Transform: it preserves chunk identity while recording the number of visible bytes. The counter is meaningful only after the pipeline has completed successfully or failed at a known point. Reading it mid-pipeline is a live observation, not an authoritative total. The class assumes byte mode; object-mode input would make chunk.length an unrelated domain property.

## Extended case analysis

Consider a gzip Transform connected to a file sink. The gzip readable side can emit its final compressed bytes before the file sink has flushed them. Observing the transform’s `end` event does not authorize publication of the destination. The pipeline owner must wait for the sink’s writable completion and then perform any file synchronization and rename required by the product. A correct trace therefore contains several legitimate “finished” moments, each answering a different question.

## What this mechanism establishes

A correct implementation establishes these local facts:

- The transform callback is invoked exactly once per accepted chunk.

- The byte counter describes bytes that actually passed through the transform.

- The collector does not retain aliases to producer-owned mutable chunks.

It does **not** establish the stronger claims hidden by these shortcuts:

- using a `data` listener as both observer and consumer;

- returning on source `end` without awaiting the destination;

Those distinctions are part of the public contract. Later modules may add stronger guarantees, but they must not be backdated into this mechanism.

## Decision procedure

1. Name the stream direction from the caller’s perspective.

2. State whether the unit is bytes, strings, or objects.

3. Choose one consumption style and one completion primitive.

4. Identify every internal or external queue and its measurement unit.

5. State who destroys the stream after error, cancellation, or early return.

6. Keep custom hook callbacks single, causal, and terminally complete.

Make each answer visible in an API, graph, or test. Labels such as “streaming,” “safe,” and “atomic” are incomplete until representation, owner, bound, and terminal evidence are named.

## Common wrong models

### Treating close as successful completion

A stream can close after error or destruction. Success must be established by the operation that owns the full protocol.

### Mixing data events and async iteration

Two consumption models compete for the same chunks and make flow state difficult to reason about.

### Using objectMode as a safety boundary

It changes buffering units; it does not validate objects or bound their retained size.

### Calling _write or _transform directly

Internal hooks rely on public stream machinery for buffering and lifecycle.

## Apply the mechanism in FlowLedger

Define FlowLedger’s byte-mode and object-mode boundaries. Add transparent counting transforms and a single completion authority for each linear pipeline.

Before editing FlowLedger, record the changed edge, owner, bound, and success observation. Update implementation, errors, tests, documentation, and report as one feature.

## Independent transfer

Design a Duplex that accepts commands as objects and emits encoded response bytes. Specify separate modes, high-water-mark units, and terminal ownership.

The transfer is successful when the new design preserves the module’s governing relationship without copying the laboratory’s domain names or relying on its exact data shape.

## Practice sequence

1. Reconstruct the module ledger from memory.
2. Read the worked case and mark every copy, view, queue, wait, and terminal observation.
3. Predict all eight Module 42 investigations before running them.
4. Complete the workbook’s diagnosis section without broad assertions or whole-input shortcuts.
5. Build **Stream State Observatory** from the starter package.
6. Compare only after your adversarial tests pass, beginning with the first different design decision.
7. Transfer the mechanism into FlowLedger and explain one earlier-course invariant that could regress.

## Readiness standard

Continue only when you can:

- Distinguish Readable, Writable, Duplex, Transform, PassThrough, byte mode, and object mode

- Trace readable and writable state without mixing incompatible consumption styles

- Separate end, finish, close, error, destroy, and abort observations

- Implement a small custom stream while respecting callback and terminal contracts

- Choose stream APIs only when incremental data and bounded buffering are actual requirements
- explain which observation is necessary but insufficient for product completion;
- state one capacity or durability guarantee this module deliberately does not make;
- defend the laboratory’s failure path without reading the reference source.

## Primary references

- [https://nodejs.org/docs/latest-v24.x/api/stream.html](https://nodejs.org/docs/latest-v24.x/api/stream.html)

The chapter is self-contained. These links are primary-source routes for checking version-sensitive Node.js details.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-42-stream-state-observatory/README.md)
- [FlowLedger engineering guide](../capstone.md)
