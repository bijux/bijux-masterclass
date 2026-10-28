# Reasoned solutions — Module 51: Binary Data Contracts: Bytes, Endianness, and Checked Parsing

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md)

Use these solutions after freezing your own analysis. The code result matters less than locating the first broken contract and identifying who owns the repair.

Read each answer as a boundary proof: identify the missing fact, the component able to establish it, and the state that must remain unchanged when the proof fails.

## Prediction analysis

### Prediction 1

**Problem.** A parser reads a `u64` length with `as usize` and then slices. Predict the two distinct failures possible on 32-bit and 64-bit targets.

**Reasoned answer.** The cast can truncate on a narrower target; on any target the slice can still be shorter than the declared length. Checked conversion and checked slicing solve different obligations.

### Prediction 2

**Problem.** A cursor increments its offset before calling `get`. The input is truncated. Which state is now false?

**Reasoned answer.** The cursor offset no longer describes consumed bytes. The mutation occurred before proof, so diagnostics and recovery are corrupted.

### Prediction 3

**Problem.** A file stores `u32::to_ne_bytes`. Can another architecture decode it portably?

**Reasoned answer.** No. Native-endian storage has no stable cross-target representation unless the format explicitly fixes the target.

### Prediction 4

**Problem.** A name uses `String::from_utf8_lossy`. Does the decoder still preserve the original identity?

**Reasoned answer.** No. Distinct invalid byte sequences can map through replacement characters, so lossy text is unsuitable as an authoritative name.

### Prediction 5

**Problem.** Each payload is limited to 1 MiB, but entry count is one million. Is the allocation policy bounded?

**Reasoned answer.** Not unless entry count and total decoded payload are also bounded with checked accumulation.

### Prediction 6

**Problem.** The checksum matches. Is the producer authenticated?

**Reasoned answer.** No. A non-cryptographic checksum is an integrity signal, not proof of identity or authorization.

### Prediction 7

**Problem.** The parser returns `&[u8]` payloads. May the input vector be mutated while views exist?

**Reasoned answer.** No. The shared borrows keep the relevant buffer immutably borrowed.

### Prediction 8

**Problem.** The decoder accepts valid entries and ignores trailing bytes. What compatibility risk appears?

**Reasoned answer.** Corruption or concatenated data can be silently accepted, and future versions become ambiguous. Trailing-byte policy must be explicit.

## Construction guidance

### Length conversion

Use `usize::try_from`, then compare with product limits, then perform checked addition. Each step proves a separate claim.

### Transactional cursor

The correct cursor derives the candidate range from the unchanged state and commits offset/slice changes only after success.

### Text identity

Portable logical names need a specified encoding. Host names that do not fit must be rejected or explicitly mapped, never silently rewritten.

### Trailing bytes

Strict rejection makes corruption visible. A format that permits extensions should encode extension length or version rather than rely on ignored tails.

### Transfer

The sensor packet must constrain sample count before multiplying by sample width, and the multiplication itself must be checked.

## Boundary-trace reference

A strong solution trace for this module must trace the decoder from the raw byte slice through each checked range, integer conversion, length calculation, UTF-8 validation, allocation decision, and domain constructor. Your table must include the cursor offset before and after every successful read and the exact state preserved on truncation. It should reveal the earliest point at which an invalid assumption would become observable and the unique owner responsible for cleanup or rollback.

## Weak repairs to reject

Reject solutions built around these shortcuts:

- casting an untrusted `u64` length with `as usize`;
- advancing the cursor before `get` proves the range;
- allocating from a per-entry length without a cumulative budget;
- accepting lossy UTF-8 as archive identity;
- treating a checksum as producer authentication;
- ignoring trailing bytes without a version rule;

A principled repair makes the missing fact explicit in a type, checked operation, state transition, safety contract, platform qualification, or foreign-call contract. It does not merely move the assumption to a less visible line.

## Causal proof table

| Claim | Evidence that establishes it | Evidence that is still missing |
|---|---|---|
| A fixed-width integer is available | `get` returned the exact byte range and `try_into` proved its width | The integer may still violate the format’s semantic range |
| A declared payload fits this input | checked conversion, checked addition, and a successful slice lookup | The cumulative archive budget may still be exceeded |
| A logical name is valid text | strict UTF-8 decoding succeeded | The name may still violate the portable-path grammar |
| The record is structurally valid | all fields, lengths, tags, and checksum agree | The record is not thereby authenticated or authorized |
| Parsing completed | the cursor equals the input length under a strict trailing-byte policy | Extraction policy and host-path safety are separate later decisions |

This table prevents one successful check from being promoted into a stronger claim. In particular, “the checksum matched” cannot substitute for bounds validation, and “the slice exists” cannot substitute for an allocation budget.

## Counterexample clinic

A per-entry 1 MiB limit still permits exhaustion when an attacker declares millions of small entries. The repair needs at least entry-count and cumulative-payload limits, both accumulated with checked arithmetic before allocation. Likewise, `from_utf8_lossy` can make two invalid byte names display identically; a decoder that uses the rewritten string as identity has silently changed the archive rather than merely rendered it.

A strong parser therefore has two transaction boundaries. Each field read commits the cursor only after the requested range exists. The whole record becomes a domain value only after every syntactic and semantic check succeeds. On failure, the caller receives a stable offset and no partially valid record.

## Completion check

Use the chapter’s readiness statement as the first threshold:

You are ready when you can derive every slice boundary and allocation from checked arithmetic, explain why no Rust value is reinterpreted from external bytes, and distinguish structural validity from extraction policy.

Then perform this destructive regression check: remove one checked-add or checked-conversion branch and confirm that a truncation or overflow fixture exposes the exact regression. The resulting failure should be caught for the causal reason predicted in the workbook, not by an unrelated panic or syntax error.
