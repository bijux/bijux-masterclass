# Laboratory 73 — Bounded Length Codec

**Course 8 · Module 73: Async I/O, Buffers, Streams, and Framing**

[Chapter](../../course-book/module-73-async-io-buffers-streams-and-framing/index.md) · [Workbook](../../course-book/module-73-async-io-buffers-streams-and-framing/workbook.md) · [JobWire guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Async I/O, Buffers, Streams, and Framing**: How do arbitrary, partial byte transfers become complete bounded messages without confusing readiness, reads, buffers, frames, or protocol meaning? The product must make **Distinguish readiness from transfer completion** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **buffer and frame ledger** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How can a codec recover complete messages from arbitrary byte partitions while bounding hostile lengths and preserving every undecoded byte?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a four-byte big-endian length-delimited codec over `BytesMut`. It must encode canonically, decode incrementally, preserve coalesced following frames, and distinguish clean EOF from truncated input.

## Product-specific design pressure

The product removes sockets so chunking correctness can be proved exhaustively. It tests the framing layer before protocol syntax and makes allocation order visible.

## Contract

Payloads are bounded by constructor configuration and `u32`. No incomplete frame is consumed. Length and total arithmetic are checked before reserve. `decode_eof` reports leftover incomplete input. Equal payloads encode to equal bytes.

## Required milestones

1. Freeze the byte grammar.
2. Implement encode with checked bounds.
3. Implement decode without consuming incomplete input.
4. Implement EOF behavior.
5. Add split, coalescing, maximum, and round-trip tests.

## Adversarial cases

- empty payload
- one-byte delivery
- all split points
- several coalesced frames
- maximum payload
- maximum plus one
- incomplete prefix at EOF
- incomplete payload at EOF

## Evidence to produce

- a byte-layout diagram
- proof that reserve follows validation
- chunk-invariance tests
- canonical round trips
- a cancellation policy for interrupted writes when the codec is used with a socket

## Prohibited shortcuts

- calling reserve from the peer length before checking it
- treating a read as a frame
- discarding leftover bytes at EOF
- consuming the prefix too early
- embedding command parsing in the codec

## Transfer

Transfer the design to a newline codec with a 32 KiB line maximum. Decide whether an unterminated final line is valid and how `CRLF` is normalized.

## Comparing with the reference

The reference is stronger only if every partition produces the same frames and final buffer. Inspect consumption order and EOF before comparing convenience methods.

The `solution/` directory is a reference after independent work, not a sequence of blanks to copy. Compare invariants, task ownership, cancellation behavior, bounds, and tests before comparing line count.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Begin in `starter/`. Do not open `solution/` until the state diagram, failure cases, and transfer design are written or a precise blocker is recorded.

The laboratory is complete when its tests pass and you can answer the governing question without the chapter:

For **Laboratory 73 — Bounded Length Codec**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Bounded Length Codec**.
2. Draw the smallest **buffer and frame ledger** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to JobWire so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish readiness from transfer completion.
- Handle partial reads and partial writes without message-boundary assumptions.
- Explain the contracts of `AsyncRead`, `AsyncWrite`, `AsyncBufRead`, `Stream`, and `Sink`.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 73 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **buffer and frame ledger**. Defend why your design is simpler than one plausible alternative under the new requirements.
