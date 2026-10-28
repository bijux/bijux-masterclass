# Laboratory 73 — Bounded Length Codec

This is the independent product for **Course 8, Module 73**. Read the [module chapter](../../course-book/module-73-async-io-buffers-streams-and-framing/index.md) and complete its [workbook](../../course-book/module-73-async-io-buffers-streams-and-framing/workbook.md) before consulting the reference implementation.

## Learning target

> How can a codec recover complete messages from arbitrary byte partitions while bounding hostile lengths and preserving every undecoded byte?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a four-byte big-endian length-delimited codec over `BytesMut`. It must encode canonically, decode incrementally, preserve coalesced following frames, and distinguish clean EOF from truncated input.

## Why this laboratory exists

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

> How can a codec recover complete messages from arbitrary byte partitions while bounding hostile lengths and preserving every undecoded byte?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
