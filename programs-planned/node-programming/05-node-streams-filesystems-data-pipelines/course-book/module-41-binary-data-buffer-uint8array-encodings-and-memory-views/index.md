# Module 41 — Binary Data: Buffer, Uint8Array, Encodings, and Memory Views

**Progress: 41/100**

## The governing question

> When a Node.js API gives you bytes, which allocation owns them, which views alias them, and at what exact boundary do bytes become text or typed values?

## Why this module comes now

Course 4 established ownership of asynchronous work. Course 5 begins one layer lower: the values moving through that work are often not strings or objects but bounded regions of memory. Before streams can be understood, the reader must be able to distinguish allocation, view, copy, encoding, length, offset, and interpretation.

The preceding courses already taught a strict separation between external values and trusted domain state. Binary data makes that separation easier to violate because a `Buffer` looks concrete even when it is only a view into someone else’s allocation. Course 2’s identity reasoning now applies to byte ranges; Course 4’s task ownership now applies to operations that may retain those ranges after suspension. A byte API therefore needs both a value contract and a storage contract.

This module also establishes a convention used throughout Course 5: representation names are part of variable and report names. `sourceBytes`, `canonicalBytes`, and `compressedBytes` are not interchangeable counters. The program should never require a reader to infer which representation a length or digest describes.

## Observable outcomes

By the end of this module, you can:

- distinguish Buffer, Uint8Array, ArrayBuffer, DataView, Blob, string, and their conversion boundaries

- predict whether an operation copies bytes or creates an aliasing view

- parse and encode fixed binary fields with explicit endianness and checked ranges

- validate text and binary-to-text encodings instead of relying on permissive truncation

- design byte APIs that state ownership, mutation, and lifetime expectations clearly

## The module ledger

Use this ledger while reading examples and before writing the laboratory design. It is deliberately specific to this module.

| Dimension | Question to answer |
|---|---|
| backing store | Which `ArrayBuffer` owns the physical bytes, and can another view mutate it? |
| visible range | What are the exact `byteOffset` and `byteLength` exposed by this value? |
| copy policy | Does the callee observe temporarily, retain a shared view, or own a copy? |
| interpretation | Are these bytes opaque, UTF-8, hexadecimal text, or fixed-width fields? |
| integer proof | Which arithmetic establishes every offset and length before access or allocation? |
| canonical form | Can two different byte sequences represent the same logical value, and is that allowed? |

## Allocation, view, and interpretation are different facts

An ArrayBuffer is a region of memory. A Buffer or Uint8Array is a typed view over some region of an allocation, with its own byte offset and visible length. A string is not another view of those bytes; producing a string decodes bytes according to an encoding and creates a JavaScript string. The same bytes can therefore have several interpretations without changing the underlying storage, and several views can observe the same mutation. Treating all of these values as interchangeable hides the most important facts.

For every byte value, write four entries: backing allocation, visible byte range, mutability, and interpretation. If a function accepts Uint8Array, ask whether it retains the view, copies the visible range, or reads it only during the call. If it returns Buffer.subarray(), the returned value aliases the original allocation. If it returns Buffer.from(existingBuffer), it owns a copy. That difference is part of the API contract, not an implementation footnote.

## Buffer is a Uint8Array with Node-specific behavior

Buffer extends Uint8Array, so many APIs accept either. Similar names do not always imply similar copy behavior. In particular, Buffer slice historically creates a view, whereas TypedArray slice creates a copy. Subarray consistently expresses a view across both families. A public API should prefer explicit names such as copyPayload and viewPayload rather than force callers to remember legacy method behavior.

Buffer.alloc creates initialized bytes. Buffer.allocUnsafe skips initialization and is justified only when every byte is overwritten before any read or exposure. The word unsafe here describes possible disclosure of old process memory, not TypeScript unsoundness. In instructional and ordinary application code, initialized allocation is usually the correct baseline because its proof is local and obvious.

## Encoding and decoding are validating boundaries

UTF-8 maps variable-length byte sequences to Unicode scalar values represented by JavaScript strings. A chunk boundary can split one character, so decoding each chunk independently can introduce replacement characters. Hex and base64 are not character encodings in the same sense; they are binary-to-text representations. Some Buffer conversion routines accept malformed input permissively or truncate at the first invalid portion. A protocol that requires canonical input must validate syntax before conversion.

The correct order is: establish a maximum encoded length, validate the alphabet and structural rules, convert, then validate the decoded length and domain meaning. For UTF-8 input that must reject malformed sequences, use a fatal TextDecoder or another explicit validator. Never infer byte length from string.length because JavaScript counts UTF-16 code units, not encoded bytes.

## Endianness is part of the format contract

A multi-byte integer has no portable byte order until the format specifies one. readUInt32BE and writeUInt32BE express network-style big endian; the LE variants express little endian. Endianness belongs in the format specification, test vectors, and method names. Reading with the host platform order is not a valid format because the bytes must be interpreted identically on every machine.

Checked parsing validates offset plus field width before reading. It also validates semantic limits before allocating or slicing a payload. A length prefix is a claim from the input, not permission to allocate. The parser first checks that the prefix is within the product limit and within the remaining input, then copies or views the payload according to the promised ownership contract.

## Byte boundaries need integer and overflow discipline

JavaScript numbers can exactly represent integers only through Number.MAX_SAFE_INTEGER, while Buffer lengths and offsets have their own implementation limits. Binary formats normally use narrower fixed-width fields. Parse into the smallest faithful representation, use checked arithmetic for offset plus length, and reject impossible totals before calling allocation or slicing APIs.

A robust cursor never advances on failed validation. Compute candidateEnd, prove it is an integer within the input, then commit the new cursor. This failure-atomic rule makes error offsets trustworthy and prevents later fields from being interpreted from the wrong position.

## A view is a capability, not merely a collection

A view grants access to a particular region of a backing store. The capability includes more than the values currently visible: it includes the ability to observe later mutation and, for mutable views, to perform mutation. A function that returns `input.subarray(0, 16)` has exported a capability tied to the input allocation. That can be efficient, but it is not an owned result. The caller must know whether the source remains live, whether another component can mutate it, and whether retaining sixteen bytes also retains a multi-megabyte backing allocation.

Copying is therefore neither automatically wasteful nor automatically safe. It is the operation that deliberately changes the ownership contract. Copy at a boundary where independent lifetime or immutability is required; keep a view when the lifetime is local, mutation is controlled, and retention is acceptable. Tests should distinguish the two contracts by mutating the source and, where practical, by checking that a small long-lived result does not retain an unexpectedly large input.

## Binary parsing is a sequence of proof obligations

A parser should not read a field and then discover whether the read was legal. Before each access it proves that the required width is present. Before each payload allocation it proves the declared length is within the product limit. Before advancing its cursor it proves `offset + length` is safe and within the visible range. Only after those checks does it commit the new cursor.

This ordering makes failure atomic at the parser-state level. A malformed field does not leave the cursor pointing into an invented record, and the reported offset still identifies the location at which trust failed. The discipline scales from a seven-byte teaching header to archive indexes, network frames, image metadata, and database pages.

## Encoding APIs do not define your protocol policy

Node provides conversions; your format defines validity. A permissive hex or base64 conversion may be useful for human input, while a signed manifest may require canonical alphabet, padding, and case. UTF-8 replacement decoding may be appropriate for log display, while a protocol identifier may need fatal rejection. The API call does not answer those policy questions.

Write the policy before the conversion: accepted alphabet, normalization, maximum encoded size, maximum decoded size, and whether non-canonical but decodable input is rejected. Then test malformed prefixes, odd lengths, invalid padding, split UTF-8 sequences, and values exactly at the byte limit.

## Worked case — A bounded binary envelope

```ts
import { Buffer } from 'node:buffer';

const HEADER_BYTES = 7;

export interface Envelope {
  readonly version: 1;
  readonly kind: number;
  readonly payload: Buffer;
}

export function decodeEnvelope(input: Uint8Array, maxPayloadBytes: number): Envelope {
  const bytes = Buffer.from(input.buffer, input.byteOffset, input.byteLength);
  if (bytes.length < HEADER_BYTES) throw new Error('truncated header');
  if (bytes[0] !== 1) throw new Error(`unsupported version ${bytes[0]}`);
  const kind = bytes.readUInt16BE(1);
  const length = bytes.readUInt32BE(3);
  if (length > maxPayloadBytes) throw new Error('payload exceeds limit');
  const end = HEADER_BYTES + length;
  if (!Number.isSafeInteger(end) || end !== bytes.length) {
    throw new Error('declared length does not match envelope');
  }
  return { version: 1, kind, payload: Buffer.from(bytes.subarray(HEADER_BYTES, end)) };
}
```

The temporary Buffer view over input does not copy. The returned payload does copy, so the Envelope remains stable even if the caller later mutates the original Uint8Array. The length prefix is checked against both a product limit and the actual remaining bytes before the copy. The decoder rejects trailing bytes, which makes the envelope canonical rather than silently accepting concatenated data.

## Extended case analysis

Imagine a cache that returns the first 32 bytes of a 200 MB file by keeping `fileBuffer.subarray(0, 32)`. Functionally the cache seems tiny; physically each entry can retain the complete file allocation. Replacing the result with `Buffer.from(...)` changes the retained-memory behavior without changing the visible bytes. The correct choice depends on cache lifetime and whether the original file buffer is intentionally shared. This is why “zero copy” is not a complete performance claim: fewer copies can create longer retention and less obvious mutation authority.

## What this mechanism establishes

A correct implementation establishes these local facts:

- The header is exactly seven bytes: version, big-endian kind, and big-endian payload length.

- Every successful decode consumes the complete visible input; trailing bytes are rejected.

- No untrusted length controls allocation before the product limit and remaining input are checked.

It does **not** establish the stronger claims hidden by these shortcuts:

- using `input.buffer` without preserving the visible offset and length;

- returning a view while documenting an owned payload;

Those distinctions are part of the public contract. Later modules may add stronger guarantees, but they must not be backdated into this mechanism.

## Decision procedure

1. Name the logical representation: raw bytes, encoded text, decoded string, or typed fields.

2. Record the backing allocation and visible range for every view.

3. Decide whether the API promises borrowed observation, shared mutation, or an owned copy.

4. Validate lengths and integer arithmetic before allocation, slicing, or decoding.

5. Specify endianness and canonical encoding in the format contract.

6. Test aliasing explicitly by mutating the source after the operation.

Make each answer visible in an API, graph, or test. Labels such as “streaming,” “safe,” and “atomic” are incomplete until representation, owner, bound, and terminal evidence are named.

## Common wrong models

### Assuming Buffer.slice copies

It aliases the original allocation. A long-lived small slice can retain a large backing store and can observe later mutation.

### Using string.length as byte length

It counts UTF-16 code units. Buffer.byteLength or an actual encoded buffer is required for byte budgets.

### Trusting Buffer.from(text, hex) as validation

Malformed hex can be truncated. Validate canonical syntax before conversion.

### Allocating from an untrusted length prefix

The prefix is data to validate, not an allocation instruction.

## Apply the mechanism in FlowLedger

Define FlowLedger byte limits and the raw-byte accounting layer. Add a copy-safe buffer utility, SHA-256 input tap, and tests that distinguish visible ranges from backing allocations.

Before editing FlowLedger, record the changed edge, owner, bound, and success observation. Update implementation, errors, tests, documentation, and report as one feature.

## Independent transfer

Design a binary thumbnail record containing a media type, width, height, and payload. State which fields are validated before allocation and whether the decoded record owns its payload.

The transfer is successful when the new design preserves the module’s governing relationship without copying the laboratory’s domain names or relying on its exact data shape.

## Practice sequence

1. Reconstruct the module ledger from memory.
2. Read the worked case and mark every copy, view, queue, wait, and terminal observation.
3. Predict all eight Module 41 investigations before running them.
4. Complete the workbook’s diagnosis section without broad assertions or whole-input shortcuts.
5. Build **Bounded Binary Envelope** from the starter package.
6. Compare only after your adversarial tests pass, beginning with the first different design decision.
7. Transfer the mechanism into FlowLedger and explain one earlier-course invariant that could regress.

## Readiness standard

Continue only when you can:

- Distinguish Buffer, Uint8Array, ArrayBuffer, DataView, Blob, string, and their conversion boundaries

- Predict whether an operation copies bytes or creates an aliasing view

- Parse and encode fixed binary fields with explicit endianness and checked ranges

- Validate text and binary-to-text encodings instead of relying on permissive truncation

- Design byte APIs that state ownership, mutation, and lifetime expectations clearly
- explain which observation is necessary but insufficient for product completion;
- state one capacity or durability guarantee this module deliberately does not make;
- defend the laboratory’s failure path without reading the reference source.

## Primary references

- [https://nodejs.org/docs/latest-v24.x/api/buffer.html](https://nodejs.org/docs/latest-v24.x/api/buffer.html)
- [https://nodejs.org/docs/latest-v24.x/api/util.html#class-utiltextdecoder](https://nodejs.org/docs/latest-v24.x/api/util.html#class-utiltextdecoder)

The chapter is self-contained. These links are primary-source routes for checking version-sensitive Node.js details.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-41-bounded-binary-envelope/README.md)
- [FlowLedger engineering guide](../capstone.md)
