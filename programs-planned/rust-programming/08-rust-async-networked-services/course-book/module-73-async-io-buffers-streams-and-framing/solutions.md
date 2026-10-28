# Reasoned Solutions — Module 73: Async I/O, Buffers, Streams, and Framing

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-03-bounded-length-codec/README.md) · [JobWire guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 73: Async I/O, Buffers, Streams, and Framing**. Compare the reasoning against this question: *How do arbitrary, partial byte transfers become complete bounded messages without confusing readiness, reads, buffers, frames, or protocol meaning?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Prediction solutions

1. No. The read may return any positive prefix, subject to OS and buffer behavior.
2. One decoder call normally returns one frame. The second complete frame and partial third remain for subsequent decode calls.
3. The decoder has lost the framing prefix needed to interpret the retained payload bytes. It must peek until the whole frame is available or retain explicit decode state.
4. The peer can trigger excessive allocation or reserve failure before policy is enforced. Reject the length first and use checked total arithmetic.
5. Empty buffer is clean EOF. Leftover prefix bytes are a truncated frame and should be reported.
6. Not generally. A prefix may already be visible. Continuing from the beginning can duplicate or corrupt framing. Close or use a protocol with resumable writes.
7. None. Wakeups are scheduling hints. Read until the operation would block or product policy says stop.
8. The slice may keep the original allocation alive. Copying a small long-lived payload can reduce retained capacity.

## Part 2 — Repair reasoning

The original server confuses read boundaries with messages and permits response interleaving. A complete repair wraps the byte stream in one bounded codec, parses messages only after full frames, and gives one task or sink owner exclusive output serialization. If responses may complete out of order, every response needs a request identifier and the protocol must permit reordering. Otherwise queue them in request order.

UTF-8 validation belongs above framing. A malformed payload can close only the connection, while an internal application error may produce a structured response if the protocol state remains synchronized.

## Part 3 — Focused exercise guidance

Split tests should operate over encoded bytes, not rely on actual socket scheduling. Each partition sequence feeds the decoder incrementally and then drains all frames. Truncation tests invoke EOF only after the final prefix. The retention exercise should measure or reason about capacity, not merely payload length.

For cancellation, reading into a framed object can be safe when the object survives with its buffer. Sending may be unsafe to abandon because output can be partially committed to the stream. A single connection writer and “close on interrupted frame” policy make that boundary explicit.

## Part 4 — Laboratory comparison

A strong codec never consumes an incomplete frame, never reserves from unchecked peer input, emits all coalesced frames, and distinguishes clean from truncated EOF. The strongest tests prove chunk invariance rather than checking one convenient read pattern.

## Part 5 — Capstone comparison

JobWire’s codec should accept and emit bytes only. A separate parser validates UTF-8 and command fields. This separation allows protocol tests without sockets and frame tests without command semantics. Per-connection retained memory includes the codec buffer, one decoded payload, parser-owned strings, and pending response state; name each bound.

## Part 6 — Reconstruction and defense

A complete defense states that I/O readiness permits another attempt, while transfer counts are authoritative. Framing accumulates arbitrary chunks into bounded messages. Protocol parsing assigns meaning only after framing. Cancellation analysis follows buffered state and externally visible prefixes rather than assuming `await` is transactional.

## Deep reasoning and transfer

### Decisive model

> How do arbitrary, partial byte transfers become complete bounded messages without confusing readiness, reads, buffers, frames, or protocol meaning?

Build a **buffer and frame ledger**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish readiness from transfer completion.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Handle partial reads and partial writes without message-boundary assumptions.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Explain the contracts of `AsyncRead`, `AsyncWrite`, `AsyncBufRead`, `Stream`, and `Sink`.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Use `Bytes` and `BytesMut` to separate shared immutable payloads from mutable receive buffers.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Design a decoder that preserves incomplete input and extracts multiple complete frames.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish readiness from transfer completion.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the buffer and frame ledger.

### Reference implementation comparison

For [Bounded Length Codec](../../labs/module-03-bounded-length-codec/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In JobWire, Module 73 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Async I/O, Buffers, Streams, and Framing**, which relationship decides this question: “How do arbitrary, partial byte transfers become complete bounded messages without confusing readiness, reads, buffers, frames, or protocol meaning?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to JobWire?
