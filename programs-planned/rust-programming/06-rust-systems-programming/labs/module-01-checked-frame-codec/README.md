# Laboratory 51 — Checked Frame Codec

This is the independent product for **Course 6, Module 51: Binary Data Contracts: Bytes, Endianness, and Checked Parsing**. Read the [module chapter](../../course-book/module-51-binary-data-contracts/index.md) and complete its [workbook](../../course-book/module-51-binary-data-contracts/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you turn untrusted bytes into typed values without confusing representation, validation, allocation, and meaning?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a small versioned binary frame format. Each frame contains a kind byte, a little-endian payload length, the payload, and an integrity checksum. The decoder must treat every byte as untrusted and report the exact offset of failure.

## Why this laboratory exists

This lab removes files, paths, allocation owners, and FFI so the byte grammar is the only source of difficulty. You must be able to point from every decoded value back to a checked range and explain why a malformed declaration cannot trigger an unchecked index or an unbounded allocation. Read the reference only after your own cursor invariant and error-offset policy are written.

## Contract

The format begins with `BFC1`, then a little-endian `u16` frame count. Each frame is `kind: u8`, `payload_len: u32`, `checksum: u32`, then payload bytes. Kinds 1 and 2 are valid. At most 64 frames and 1 MiB total payload are accepted. Trailing bytes are rejected. The checksum is FNV-1a and is explicitly non-cryptographic.

## Required milestones

1. Write the byte grammar and offset table before the parser.
2. Implement a cursor whose state advances only after a successful range check.
3. Perform checked conversion and checked aggregate-length arithmetic before allocation.
4. Encode one canonical representation and prove round-trip symmetry.
5. Add truncation tests at every byte boundary of a valid two-frame input.

## Adversarial cases

- bad magic and unknown kind
- declared length larger than remaining bytes
- aggregate payload above the limit
- checksum mismatch
- one trailing byte
- zero frames and an empty payload

## Evidence to produce

- a byte-offset table for every field in one valid frame;
- a cursor invariant stating when position may advance;
- exhaustive truncation tests over every prefix of a golden frame;
- boundary tests for zero, maximum, one-above-limit, and overflowing lengths;
- an explanation of why checksum success establishes corruption detection rather than authenticity.

## Prohibited shortcuts

Do not index before a range check, cast wire integers with `as`, allocate directly from an untrusted declaration, transmute bytes into a Rust struct, ignore trailing bytes, or reduce all malformed inputs to one undifferentiated error. The starter owns the wire constants and domain vocabulary; the validation order remains your work.

## Transfer

Apply the same method to a sensor packet with a timestamp, sample count, and signed 16-bit samples. State endianness and check `count * 2` before slicing.

## Comparing with the reference

Compare the two decoders field by field. Check whether they reject before allocation, preserve the first causal byte offset, leave cursor state unchanged on failed reads, and emit one canonical encoding. A shorter parser is not better if its proof must be reconstructed from incidental indexing.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the contract, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer this question without the chapter:

> How do you turn untrusted bytes into typed values without confusing representation, validation, allocation, and meaning?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
