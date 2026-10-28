# Reasoned Solutions — Module 73: Async I/O, Buffers, Streams, and Framing

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the JobWire guide](../capstone.md)

The central correction is that transport chunks have no application meaning. Meaning begins only after bounded framing and protocol parsing.

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
