# Module 51 — Binary Data Contracts: Bytes, Endianness, and Checked Parsing

**Course 6 · Day 1 · Module 51 of 100**
`█████████████░░░░░░░░░░░░` **51/100**

[Program](../../../README.md) · [Course 6](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-01-checked-frame-codec/README.md) · [FrameVault guide](../capstone.md)

[← Module 50: Build Scripts, Generated Code, and Compile-Time Architecture](../../../05-rust-metaprogramming/course-book/module-50-build-scripts-generated-code-and-compile-time-architecture/index.md) · [Module 52: Files, Durability, and Transactional Replacement →](../module-52-files-durability-and-transactional-replacement/index.md)

## The question

> How do you turn untrusted bytes into typed values without confusing representation, validation, allocation, and meaning?

## Why this comes now

The first five courses mostly operated after Rust values already existed. Systems work begins earlier. A file, pipe, device, or foreign function does not hand you a valid domain value; it hands you bytes plus a convention. Course 2 taught that bit patterns and Rust validity are not interchangeable. Module 51 turns that memory insight into an engineering method for real binary interfaces. Before touching raw pointers, you must be able to parse hostile bytes safely with ordinary Rust.

### Prerequisite bridge

Module 50 established **Build Scripts, Generated Code, and Compile-Time Architecture**. Before continuing, verify that you can review a multi-generator architecture for duplicate authority, hidden effects, and compatibility risk. This module preserves that capability and adds the ability to define a binary format as a versioned contract rather than a sequence of convenient writes. Module 52, **Files, Durability, and Transactional Replacement**, will rely on both when it asks: *What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?*

### Scope boundary

This module owns the reasoning for **binary data contracts: bytes, endianness, and checked parsing** inside Course 6. The course covers single-threaded systems boundaries and narrow unsafe abstractions. Threads, atomics, async I/O, networking, and production measurement are deferred so each external contract remains visible. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Define a binary format as a versioned contract rather than a sequence of convenient writes.
- Trace byte offsets, item widths, endianness, and length arithmetic before allocating.
- Build a bounds-first cursor that never advances after failure.
- Separate structural validity, textual validity, integrity checks, and domain validation.
- Explain when a borrowed view is possible and when an owned value is the more honest boundary.
- Design errors that identify the byte offset and the contract that failed.

## Core model

### Systems programming starts before values exist

A Rust value already satisfies strong validity rules. A `u32` is four bytes interpreted as an integer; a `String` owns bytes that are valid UTF-8; a reference is aligned, non-null, points to initialized data of the right type, and obeys aliasing rules. External input has none of those guarantees. It is only a byte sequence whose producer may be buggy, malicious, newer than your program, or built for a different machine.

The first systems habit is therefore to stop saying “read a struct from the file.” A file does not contain a Rust struct. It contains a specified byte representation. The parser proves, one field at a time, that enough bytes exist and that each field satisfies the format contract. Only then may it construct Rust values.

This distinction prevents a common unsafe shortcut: copying file bytes into a `repr(C)` value or using `transmute`. Even when size and alignment happen to match, padding, invalid enum discriminants, endianness, pointer fields, and version evolution make the representation unsuitable. The robust path is explicit decoding.

### Write the format before the parser

A binary format should be describable without Rust syntax. For FrameVault, the initial contract is:

```text
archive      = magic entry-count entry*
magic        = 8 bytes: 46 52 4d 56 4c 54 30 31   # FRMVLT01
entry-count  = u32 little-endian
entry        = kind flags name-len payload-len checksum name payload
kind         = u8: 1=file, 2=command-capture
flags        = u8: currently zero
name-len     = u16 little-endian
payload-len  = u64 little-endian
checksum     = u32 little-endian, FNV-1a over payload
name         = name-len bytes, valid UTF-8 logical path
payload      = payload-len arbitrary bytes
```

The contract also needs limits: maximum entries, maximum name length, maximum individual payload, maximum total decoded payload, accepted flag bits, and whether trailing bytes are legal. Limits are not optional performance tuning. Without them, a ten-byte input can request an allocation of several exabytes.

Versioning belongs in the format from its first release. A parser should reject an unknown magic or version explicitly; silently guessing creates ambiguous data and makes future migration dangerous.

### Use a cursor whose state changes only after proof

A checked cursor couples the remaining slice with an absolute offset:

```rust
#[derive(Debug, Clone, Copy)]
struct Cursor<'a> {
    remaining: &'a [u8],
    offset: usize,
}

impl<'a> Cursor<'a> {
    fn take(&mut self, count: usize) -> Result<&'a [u8], DecodeError> {
        let bytes = self.remaining.get(..count).ok_or(
            DecodeError::UnexpectedEnd {
                offset: self.offset,
                needed: count,
                remaining: self.remaining.len(),
            },
        )?;
        self.remaining = &self.remaining[count..];
        self.offset += count;
        Ok(bytes)
    }
}
```

The important property is transactional cursor movement. `get(..count)` proves the range first. State changes only after success. A cursor that increments its offset and then discovers the slice is short makes later diagnostics untrustworthy and complicates recovery.

Small typed methods such as `read_u8`, `read_u16_le`, and `read_u64_le` should be implemented in terms of `take`. This centralizes bounds reasoning. Each method converts an exact-size slice into an array using `try_into`; it does not reinterpret memory or depend on host alignment.

### Endianness is part of the contract

The machine’s native byte order is not a file-format decision. Use explicit conversion methods:

```rust
fn read_u32_le(cursor: &mut Cursor<'_>) -> Result<u32, DecodeError> {
    let bytes: [u8; 4] = cursor.take(4)?.try_into().expect("exact width");
    Ok(u32::from_le_bytes(bytes))
}
```

The `expect` here does not assert anything about hostile input. The preceding `take(4)` and array conversion establish an internal invariant: the slice length is exactly four. A version without the assertion can map the impossible conversion error, but the important review question is whether the assertion depends only on local checked logic.

Never decode with `from_ne_bytes` unless the format explicitly says “native endian,” which makes the data target-dependent. Network protocols traditionally use big-endian; many modern formats choose little-endian. Either choice can work when it is written into the contract.

### Treat length arithmetic as hostile input

A length field is not safe because it fits in `u64`. It must fit the host `usize`, satisfy product limits, and combine with other lengths without overflow. Convert and add with checked operations:

```rust
let payload_len = usize::try_from(raw_payload_len)
    .map_err(|_| DecodeError::LengthDoesNotFit { offset })?;
let record_len = usize::from(name_len)
    .checked_add(payload_len)
    .ok_or(DecodeError::LengthOverflow { offset })?;
```

Then compare against a configured maximum before allocation or slicing. Maintain a checked total across entries. A parser that validates each payload independently can still be forced to allocate too much through many small entries.

Do not “fix” a failed conversion with `as usize`. On a narrower target, truncation can turn a huge declared length into a small value, desynchronize the parser, and undermine every later check.

### Validate nested text at the boundary

Binary containers often embed text. The payload may remain arbitrary bytes, but a logical entry name needs a documented encoding. FrameVault chooses UTF-8 for archive names because names are exchanged across platforms and must be stable in the file format.

```rust
let name_bytes = cursor.take(usize::from(name_len))?;
let name = std::str::from_utf8(name_bytes)
    .map_err(|_| DecodeError::InvalidNameUtf8 { offset: name_offset })?;
```

This does not mean host paths are always UTF-8. Module 53 distinguishes `Path` and `OsStr` from portable archive names. The encoder either rejects a host path that cannot be represented by the archive contract or requires the caller to provide an explicit logical name. Lossy conversion is display policy, not storage policy.

### Integrity is not authenticity

A checksum can detect accidental corruption and many malformed edits. It does not prove who produced the data. FrameVault uses FNV-1a because it is compact enough to implement during a systems course and makes the integrity boundary visible. The documentation states plainly that it is not cryptographic.

Compute the checksum over exactly the bytes named by the contract. Validate it after the payload bounds have been established. Report the expected and observed values. Do not reuse the checksum as an authorization decision or call it tamper-proof.

The distinction between integrity, authenticity, and confidentiality is part of systems correctness. A precise program says which property it provides and which it does not.

### Keep structural and domain validation separate

Decoding answers whether bytes form a structurally valid archive. Domain validation answers questions such as whether two logical names conflict, whether an extraction policy allows a name, or whether command captures are permitted in a given mode.

This separation improves diagnostics and reuse. A verifier may need to report a well-formed archive that violates a local policy. An inspector may list entries without extracting them. If structural parsing silently applies one application’s policy, the format becomes difficult to reuse and errors become misleading.

A useful pipeline is:

```text
bytes → structural parse → integrity checks → owned or borrowed archive model
      → policy validation → operation
```

Each arrow should have an explicit error type or error variant.

### Borrowed views and owned models answer different questions

A parser can return entry views borrowing from the input buffer. This avoids copying payloads and preserves exact bytes. It also ties every view to the buffer’s lifetime and makes mutation or long-term storage more constrained.

An owned model copies names and payloads. That is appropriate when the archive must outlive the read buffer, cross an FFI ownership boundary, or be modified before re-encoding.

Do not choose borrowed parsing only because “zero copy” sounds advanced. Choose it when the surrounding ownership topology can keep the source alive and immutable for the required duration. Course 6 uses both: focused parsers demonstrate borrowed views, while the capstone’s foreign handle owns an archive model so C callers are not coupled to a Rust input borrow.

### Errors should preserve the failing offset

A binary error without an offset forces the reader to reverse-engineer parser state. Store the absolute byte offset at which the violated field begins. For nested structures, also store the entry index or logical field name.

```rust
pub enum DecodeError {
    BadMagic { found: [u8; 8] },
    UnexpectedEnd { offset: usize, needed: usize, remaining: usize },
    UnsupportedKind { offset: usize, value: u8 },
    InvalidNameUtf8 { offset: usize },
    PayloadTooLarge { offset: usize, declared: u64, limit: usize },
    ChecksumMismatch { entry: usize, expected: u32, actual: u32 },
    TrailingBytes { offset: usize, count: usize },
}
```

Offsets are evidence. They are only trustworthy when cursor movement is transactional and every conversion identifies its source position.

### Worked example: decode one entry without trusting any field

Assume the cursor has already consumed the magic and entry count. The next byte offset is 12. A defensible decoder records each field start before reading it:

```rust
fn decode_entry(
    cursor: &mut Cursor<'_>,
    limits: Limits,
    index: usize,
) -> Result<Entry, DecodeError> {
    let kind_offset = cursor.offset();
    let kind = EntryKind::try_from(cursor.read_u8()?)
        .map_err(|value| DecodeError::UnsupportedKind {
            entry: index,
            offset: kind_offset,
            value,
        })?;

    let flags_offset = cursor.offset();
    let flags = cursor.read_u8()?;
    if flags != 0 {
        return Err(DecodeError::UnsupportedFlags {
            entry: index,
            offset: flags_offset,
            value: flags,
        });
    }

    let name_len_offset = cursor.offset();
    let name_len = usize::from(cursor.read_u16_le()?);
    if name_len == 0 || name_len > limits.max_name_bytes {
        return Err(DecodeError::NameLength {
            entry: index,
            offset: name_len_offset,
            declared: name_len,
            limit: limits.max_name_bytes,
        });
    }

    let payload_len_offset = cursor.offset();
    let raw_payload_len = cursor.read_u64_le()?;
    let payload_len = usize::try_from(raw_payload_len).map_err(|_| {
        DecodeError::LengthDoesNotFit {
            entry: index,
            offset: payload_len_offset,
            declared: raw_payload_len,
        }
    })?;
    if payload_len > limits.max_payload_bytes {
        return Err(DecodeError::PayloadTooLarge {
            entry: index,
            offset: payload_len_offset,
            declared: raw_payload_len,
            limit: limits.max_payload_bytes,
        });
    }

    let expected_checksum = cursor.read_u32_le()?;
    let name_offset = cursor.offset();
    let name_bytes = cursor.take(name_len)?;
    let name = std::str::from_utf8(name_bytes)
        .map_err(|_| DecodeError::InvalidNameUtf8 {
            entry: index,
            offset: name_offset,
        })?;
    let payload_offset = cursor.offset();
    let payload = cursor.take(payload_len)?;
    let actual_checksum = fnv1a(payload);
    if actual_checksum != expected_checksum {
        return Err(DecodeError::ChecksumMismatch {
            entry: index,
            offset: payload_offset,
            expected: expected_checksum,
            actual: actual_checksum,
        });
    }

    Ok(Entry::new(kind, name.to_owned(), payload.to_vec()))
}
```

This routine has no unsafe code because the format does not require any. Every conversion follows a proof already established by a checked slice. The `payload.to_vec()` allocation occurs only after the declared size fits `usize`, falls below the per-entry limit, and fits in the remaining bytes. A total-payload limit belongs one level above this function because it relates multiple entries.

Notice what is not proved here. `Entry::new` may still reject a logical path or duplicate name. The checksum does not establish authenticity. A file entry payload is not yet a file. Keeping those facts outside the decoder makes the boundary testable.

### Canonical encoding is a compatibility tool

A reader may accept several byte sequences that represent the same semantic value, but a writer should usually emit one canonical form. FrameVault version 1 writes entries in the model’s declared order, uses zero flags, uses the shortest fixed-width fields already defined by the format, and appends no trailing bytes. Canonical output supports reproducible archives and stable golden tests.

The encoder performs the inverse checks before writing. It rejects an entry count above `u32::MAX`, a name above `u16::MAX`, product limits, and totals that overflow. Encoding an in-memory value can fail; “it is already a Rust value” does not mean it fits the external format.

A useful symmetry table is:

| Format fact | Decoder proof | Encoder proof |
|---|---|---|
| entry count | declared count is bounded and enough entries follow | model length fits field and policy |
| name length | field fits remaining bytes and UTF-8 | UTF-8 byte length fits field and policy |
| payload length | converts to `usize`, fits policy and remaining bytes | vector length fits field and policy |
| checksum | observed payload hashes to field value | field is computed from exact emitted payload |
| trailing bytes | rejected after final entry | never emitted |

Round-trip tests need both directions:

```text
decode(encode(value)) == value
encode(decode(canonical_bytes)) == canonical_bytes
```

The second property applies only to canonical input. An accepting reader may normalize historical or noncanonical forms when the format explicitly permits them.

### Adversarial test matrix

Do not hand-pick only a few malformed examples. Generate truncation at every boundary of a known valid archive. For each prefix `bytes[..cut]`, decoding must return an error and never panic. Mutate each length field to zero, its maximum accepted value, one above the limit, `u64::MAX`, and a value larger than the remaining input. Mutate kind and flags independently. Corrupt names and checksums. Append one and many trailing bytes.

The error variant and offset are part of the contract. A test that only asserts `is_err()` can allow a later refactor to report the wrong field or allocate before rejection. For representative cases, assert the structured variant.

Fuzzing later broadens the search, but the hand-derived matrix proves that you understand the grammar. A fuzzer is not a substitute for knowing where the boundaries are.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For define a binary format as a versioned contract rather than a sequence of convenient writes, construct one positive and one causal negative example. Mark the first decisive fact in the **binary layout and range proof** and state which evidence could falsify the claim.

2. **Outcome 2.** For trace byte offsets, item widths, endianness, and length arithmetic before allocating, construct one positive and one causal negative example. Mark the first decisive fact in the **binary layout and range proof** and state which evidence could falsify the claim.

3. **Outcome 3.** For build a bounds-first cursor that never advances after failure, construct one positive and one causal negative example. Mark the first decisive fact in the **binary layout and range proof** and state which evidence could falsify the claim.

4. **Outcome 4.** For separate structural validity, textual validity, integrity checks, and domain validation, construct one positive and one causal negative example. Mark the first decisive fact in the **binary layout and range proof** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

FrameVault begins with a format module containing the magic bytes, limits, checked cursor, encoder, decoder, checksum, and typed errors. The first increment must round-trip empty archives, text and binary payloads, reject truncation at every byte boundary, reject oversized declarations before allocation, reject unknown flags, and reject trailing bytes.

The matching independent laboratory is [Checked Frame Codec](../../labs/module-01-checked-frame-codec/README.md). It isolates the mechanism so you can test the proof without carrying the whole capstone in your head.

## Practice sequence

Complete the [workbook](workbook.md) before changing the codec. Freeze the offset and error category you expect for each malformed input, then build the Checked Frame Codec lab and compare its cursor invariants with FrameVault's decoder. The transfer task is complete only when a new length-prefixed format can be reviewed without relying on indexing intuition.

## Ready to continue

You are ready when you can derive every slice boundary and allocation from checked arithmetic, explain why no Rust value is reinterpreted from external bytes, and distinguish structural validity from extraction policy.

## Primary Rust references

- [Rust standard library: integer byte conversions](https://doc.rust-lang.org/std/primitive.u32.html#method.from_le_bytes)
- [Rust standard library: slice access](https://doc.rust-lang.org/std/primitive.slice.html#method.get)
- [Rust Reference: memory model](https://doc.rust-lang.org/reference/memory-model.html)

## Continue

Continue to [Module 52 — Files, Durability, and Transactional Replacement](../module-52-files-durability-and-transactional-replacement/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
