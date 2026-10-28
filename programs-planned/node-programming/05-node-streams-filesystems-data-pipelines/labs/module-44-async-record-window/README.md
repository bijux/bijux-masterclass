# Laboratory 4 — Async Record Window

**Module 44: Async Iteration, Web Streams, and Adapter Boundaries**

## Product

Build one-shot and repeatable async sources, cancellation-aware batching and take adapters, and Node/Web Stream round trips with explicit early-return and chunk-ownership tests.

This is an independent mechanism study. It deliberately excludes FlowLedger’s other stages so failures can be attributed to one contract.

## Governing question

> When should a streaming computation be expressed as a Node stream, an async iterable, or a Web Stream, and what lifecycle semantics are changed by crossing between them?

## Public surface

- `batch(source, size, signal?)` yields independent readonly batches.

- `take(source, count)` yields at most the requested number and stops upstream work early.

- `repeatable(values)` produces a fresh async iterator per iteration.

- `webRoundTrip(chunks)` verifies a Node/Web byte-stream adapter boundary.

## Required invariants

- Each yielded batch owns an array that later iteration does not mutate.

- Batch size is a positive integer and take count is a nonnegative integer.

- Abort is checked before retaining additional items.

- Early return reaches upstream cleanup.

- Byte content survives the adapter round trip exactly.

## Implementation sequence

1. Implement the repeatable in-memory source.

2. Implement batching and prove array independence.

3. Implement take and instrument upstream `finally`.

4. Add cancellation to a producer blocked before the next item.

5. Build the Node/Web round trip.

6. Write a protocol table for early return, error, and normal exhaustion.

Do not begin by reading the reference. The starter defines the vocabulary and a baseline, not the final design.

## Adversarial cases

- batch size zero and negative;

- empty source and final partial batch;

- count zero and count larger than source;

- abort between items;

- early return while upstream owns cleanup;

- a Web Stream already locked by another reader;

- an upstream error after earlier yielded batches;

Add cases in the smallest order that falsifies an incorrect model. Avoid arbitrary sleeps; use exact chunks, counters, injected callbacks, or explicit state transitions.

## Prohibited shortcuts

- yielding one mutable batch array repeatedly;

- collecting the whole source before batching;

- assuming every AsyncIterable is repeatable;

- ignoring iterator `return()` during early stop;

- using adapters without tests for cancellation and error;

A shortcut is prohibited because it removes the mechanism the laboratory exists to teach, not because one implementation style is preferred.

## Completion evidence

1. batch identity tests;

2. an upstream-finally cleanup test;

3. zero-count and early-return tests;

4. byte-exact adapter tests;

5. a written one-shot versus repeatable API decision;

## Independent transfer

Design an API that tails a log file as an AsyncIterable of validated records. Explain who owns the FileHandle, what early return does, and whether a second iteration reopens the file.

Your transfer design must reconstruct the module ledger for the new domain. Renaming the laboratory types is not transfer.

## Early-return trace

Add an instrumented upstream async generator that records `started`, `yielded`, `returned`, `failed`, and `finally` transitions. Consume only part of it through `take`, break from the consumer loop, and prove that upstream cleanup runs exactly once. Repeat with an error thrown before the next value and with cancellation observed while the producer is waiting.

For the Node/Web adapter exercise, classify every object by ownership: backing byte storage, Node wrapper, Web wrapper, reader lock, and consumer-visible chunk. Record whether the adapter preserves byte values, chunk boundaries, repeatability, and cancellation behavior; only byte-value preservation is required by the laboratory. Finally, explain why an API returning `AsyncIterable<T>` does not by itself promise that two iterations are valid. Your implementation must state whether it returns a one-shot iterator or a repeatable iterable and must test the chosen contract directly.

## Comparing with the reference

After your tests pass, inspect `reference/` and locate the first meaningful difference. Adopt it only when it proves an invariant your design misses; otherwise retain the simpler design.
