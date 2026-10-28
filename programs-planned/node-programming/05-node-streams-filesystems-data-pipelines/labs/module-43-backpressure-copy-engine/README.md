# Laboratory 3 — Backpressure Copy Engine

**Module 43: Backpressure, Pipeline, Completion, and Failure**

## Product

Implement a bounded copy engine with a deliberately slow Writable, pressure observations, AbortSignal support, pipeline ownership, and evidence that memory does not grow with source length.

This is an independent mechanism study. It deliberately excludes FlowLedger’s other stages so failures can be attributed to one contract.

## Governing question

> How does a producer learn that downstream capacity is temporarily exhausted, and which component owns failure propagation and teardown across the complete chain?

## Public surface

- `writeWithBackpressure(destination, source, signal?)` returns counts only after writable completion.

- `DeferredSink` simulates a slow destination and exposes copied output for tests.

- `waitForDrain` in the starter is a narrow building block, not the complete owner.

## Required invariants

- Each source chunk is written exactly once.

- Production pauses after `write()` returns false and resumes only after capacity returns.

- Abort and destination failure settle the owning promise.

- The destination is ended exactly once on successful source exhaustion.

- The report does not retain source chunks.

## Implementation sequence

1. Build the slow sink and confirm a pressure signal occurs.

2. Implement the happy-path loop without duplicating the false-return chunk.

3. Add cancellable `drain` waiting.

4. Await writable completion after `end()`.

5. Add exact failure injection and teardown.

6. Write a capacity argument using bytes and queue thresholds.

Do not begin by reading the reference. The starter defines the vocabulary and a baseline, not the final design.

## Adversarial cases

- empty input;

- a chunk larger than the high-water mark;

- many tiny chunks;

- abort before the first write;

- abort while waiting for drain;

- destination error before and after pressure;

- source error after earlier successful writes;

Add cases in the smallest order that falsifies an incorrect model. Avoid arbitrary sleeps; use exact chunks, counters, injected callbacks, or explicit state transitions.

## Prohibited shortcuts

- writing the false-return chunk a second time;

- continuing production after false;

- calling `end()` without awaiting completion;

- collecting all source data to make the loop simpler;

- destroying with an error that no owner observes;

A shortcut is prohibited because it removes the mechanism the laboratory exists to teach, not because one implementation style is preferred.

## Completion evidence

1. a test that forces at least one pressure wait;

2. a no-duplication byte-for-byte output test;

3. abort and destination-error tests;

4. a capacity ledger beyond high-water marks;

5. a reasoned comparison with `pipeline`;

## Independent transfer

Design a network uploader whose request body is a Readable and whose response acknowledgment is the semantic commit. Separate write pressure, pipeline completion, HTTP response, and final product success.

Your transfer design must reconstruct the module ledger for the new domain. Renaming the laboratory types is not transfer.

## Pressure experiment

Instrument four quantities for every write attempt: source bytes offered, the Boolean returned by `write`, `writableLength`, and the moment the corresponding `drain` wait settles. Use a sink whose `_write` completion is manually released by the test so the schedule is controlled rather than timed. The trace must show that the chunk producing `false` has already been accepted and is not sent again.

Repeat the experiment with two high-water marks and explain what changed and what did not. A larger threshold may reduce waits but increases queued memory; it does not change the destination's semantic completion authority. Then abort while waiting for drain and account for every listener and promise created by the wait helper. The final report should state a conservative upper bound for retained source data, writable queue data, and test instrumentation. This makes the laboratory about a bounded pressure protocol, not merely a loop that happens to copy bytes.

## Comparing with the reference

After your tests pass, inspect `reference/` and locate the first meaningful difference. Adopt it only when it proves an invariant your design misses; otherwise retain the simpler design.
