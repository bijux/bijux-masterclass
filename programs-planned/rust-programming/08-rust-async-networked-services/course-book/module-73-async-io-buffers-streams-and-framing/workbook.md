# Workbook — Module 73: Async I/O, Buffers, Streams, and Framing

[Chapter](index.md) · [Laboratory](../../labs/module-03-bounded-length-codec/README.md) · [JobWire guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Async I/O, Buffers, Streams, and Framing** has become a usable model rather than remembered vocabulary. Its governing question is: *How do arbitrary, partial byte transfers become complete bounded messages without confusing readiness, reads, buffers, frames, or protocol meaning?* Preserve your first prediction and record decisive facts in a **buffer and frame ledger**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 72 — Tokio Runtimes, Tasks, and Structured Async Lifecycles that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do arbitrary, partial byte transfers become complete bounded messages without confusing readiness, reads, buffers, frames, or protocol meaning?**
3. Draw the smallest **buffer and frame ledger** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

1. A TCP peer sends one 100-byte frame. Must the first `read` return 100 bytes?
2. A single read returns two complete frames and half of a third. What should one decoder call return and what remains?
3. The decoder reads a four-byte length, advances the buffer past it, then discovers the payload is incomplete. What state has been lost?
4. A peer sends length `0xffff_ffff`; the decoder calls `reserve(length)` before checking a 64 KiB maximum. What is the product failure?
5. EOF arrives with an empty decode buffer. How does that differ from EOF with two prefix bytes buffered?
6. A task times out during `write_all`. Can it retry the same frame on the same stream from the beginning safely?
7. Three wakeups occur for readability before one poll. How many reads is the task entitled to infer?
8. A tiny `Bytes` slice is retained from a 16 MiB receive allocation. What memory fact may surprise the service?

## Part 2 — Diagnose and repair

A server uses `read(&mut [0; 4096])`, parses whatever it received as one UTF-8 command, and writes responses from several spawned tasks through cloned socket handles. Diagnose framing, text, partial write, serialization, cancellation, and close-order defects.

Repair the design with one bounded frame codec, one connection protocol task, and one serialized writer. State whether responses may be reordered and how that decision is represented.

## Part 3 — Focused exercises

### Exercise 1 — Split matrix

For encoded frames of lengths 0, 1, 7, and the configured maximum, feed every possible two-part split and prove the same decoded result.

### Exercise 2 — Coalescing

Encode five frames, concatenate them, feed all bytes at once, and repeatedly decode until `None`. Prove no bytes are lost.

### Exercise 3 — Truncation

Generate every proper prefix of one encoded frame and call `decode_eof`. Classify incomplete length versus incomplete payload in the error.

### Exercise 4 — Cancellation ledger

Analyze `next`, `send`, `flush`, and `close` on a framed transport. State what connection policy follows if a response send is cancelled.

### Exercise 5 — Retention

Create a design that converts a large receive buffer into small `Bytes` payloads. Add a policy that copies small long-lived values when retention would pin an excessive allocation.

### Interleaved reasoning pass

1. For **Distinguish readiness from transfer completion**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the buffer and frame ledger.
2. For **Handle partial reads and partial writes without message-boundary assumptions**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the buffer and frame ledger.
3. For **Explain the contracts of `AsyncRead`, `AsyncWrite`, `AsyncBufRead`, `Stream`, and `Sink`**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the buffer and frame ledger.
4. For **Use `Bytes` and `BytesMut` to separate shared immutable payloads from mutable receive buffers**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the buffer and frame ledger.

5. Identify one guarantee from an earlier course that a careless implementation of **Async I/O, Buffers, Streams, and Framing** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Bounded Length Codec](../../labs/module-03-bounded-length-codec/README.md). Required evidence includes:

- exact frame grammar;
- checked arithmetic before reserve;
- every split point for representative frames;
- multiple coalesced frames;
- clean and truncated EOF;
- maximum and maximum-plus-one behavior;
- canonical round trips;
- a written cancellation policy for interrupted output.

### Laboratory acceptance trace

Before opening the reference implementation for **Bounded Length Codec**, record:

- the public behavior that demonstrates **Distinguish readiness from transfer completion**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Add JobWire’s `LengthCodec` and a pure text-message parser above it. Frame payloads are UTF-8 and have a configured maximum. The codec must not know command names. The parser must not read sockets. Add chunk-invariance tests that feed the same transcript under many partitions.

State the maximum memory retained per connection before a broker request is accepted.

### Capstone invariant trace

For the Module 73 JobWire increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

1. Why is readiness not completion?
2. What does a zero-byte TCP read mean?
3. Why should incomplete bytes remain buffered?
4. Which checks precede allocation?
5. What is the difference between `Stream` end and temporary lack of an item?
6. Why is frame output cancellation a protocol question?

### Independent transfer

Design a newline-delimited codec for log lines with a 32 KiB maximum. Decide how to handle `\r\n`, an unterminated final line at EOF, invalid UTF-8, and a peer that sends no newline. Compare its trade-offs with length-prefix framing.

### Closed-book defense

In five minutes, answer “How do arbitrary, partial byte transfers become complete bounded messages without confusing readiness, reads, buffers, frames, or protocol meaning?” using the **buffer and frame ledger**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside JobWire. A list of APIs without the deciding relationship is incomplete.
