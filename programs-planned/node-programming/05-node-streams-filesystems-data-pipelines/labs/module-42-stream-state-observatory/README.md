# Laboratory 2 — Stream State Observatory

**Module 42: Stream Contracts: Readable, Writable, Duplex, and Transform**

## Product

Build instrumented Readable, Writable, and Transform implementations that record state transitions, queue lengths, terminal events, and the difference between end, finish, close, error, and destroy.

This is an independent mechanism study. It deliberately excludes FlowLedger’s other stages so failures can be attributed to one contract.

## Governing question

> What state does a Node.js stream own, which side is readable or writable, and which observation proves that the resource has actually completed?

## Public surface

- `ByteCounter` passes chunks through while exposing the byte count after processing.

- `CollectingWritable` owns copies of accepted chunks and returns a complete buffer after finish.

- `observe(chunks)` returns a terminal trace, byte count, output, and final state snapshot.

## Required invariants

- The transform callback is invoked exactly once per accepted chunk.

- The byte counter describes bytes that actually passed through the transform.

- The collector does not retain aliases to producer-owned mutable chunks.

- The laboratory distinguishes readable end, transform finish/end, writable finish, and close.

- Pipeline settlement, not event ordering alone, decides operation success.

## Implementation sequence

1. Implement the transparent byte counter and its empty-input behavior.

2. Implement the collecting sink with defensive copies.

3. Add event tracing without attaching a consuming `data` listener.

4. Run the graph through `pipeline` and return only after settlement.

5. Inject source, transform, and sink failures separately.

6. Write a state table for each stream immediately before and after completion.

Do not begin by reading the reference. The starter defines the vocabulary and a baseline, not the final design.

## Adversarial cases

- empty source;

- one chunk and many chunks;

- a zero-length chunk;

- a transform error after earlier successful chunks;

- a destination error during final write;

- early source destruction;

- a mutable input chunk changed after it is pushed;

Add cases in the smallest order that falsifies an incorrect model. Avoid arbitrary sleeps; use exact chunks, counters, injected callbacks, or explicit state transitions.

## Prohibited shortcuts

- using a `data` listener as both observer and consumer;

- returning on source `end` without awaiting the destination;

- calling a transform callback twice;

- retaining incoming chunks without copying when the API promises stable output;

- assuming `close` proves semantic success;

A shortcut is prohibited because it removes the mechanism the laboratory exists to teach, not because one implementation style is preferred.

## Completion evidence

1. a trace explaining each terminal event;

2. failure tests for all three stages;

3. a chunk-mutation test for the collecting sink;

4. a statement of the one completion authority;

5. a half-close analysis for an independent duplex scenario;

## Independent transfer

Design a Duplex that accepts commands as objects and emits encoded response bytes. Specify separate modes, high-water-mark units, and terminal ownership.

Your transfer design must reconstruct the module ledger for the new domain. Renaming the laboratory types is not transfer.

## Terminal-state review

Before accepting the implementation, build a table with one row for the source, transform readable side, transform writable side, and destination. For each row, record the event or promise that proves input acceptance has ended, output production has ended, the underlying resource has closed, and the complete operation has succeeded. Those are different claims. A source `end` event says nothing about whether the destination has flushed its final bytes; a `close` event can follow either success or destruction.

Run the same table against one injected source error, one transform error, and one destination error. Mark which events may still occur after the decisive failure and explain why those later observations do not replace the owning `pipeline` promise. Finally, mutate an input `Buffer` immediately after `push` and show whether your collector records the historical bytes or a later alias. This trace is the laboratory's proof that stream state, byte ownership, and operation completion have not been collapsed into one vague idea of “done.”

## Comparing with the reference

After your tests pass, inspect `reference/` and locate the first meaningful difference. Adopt it only when it proves an invariant your design misses; otherwise retain the simpler design.
