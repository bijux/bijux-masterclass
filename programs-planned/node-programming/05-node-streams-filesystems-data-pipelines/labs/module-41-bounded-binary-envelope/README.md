# Laboratory 1 — Bounded Binary Envelope

**Module 41: Binary Data: Buffer, Uint8Array, Encodings, and Memory Views**

## Product

Implement a versioned binary envelope with a fixed header, big-endian fields, product limits, canonical length checks, explicit copy-versus-view APIs, and mutation tests.

This is an independent mechanism study. It deliberately excludes FlowLedger’s other stages so failures can be attributed to one contract.

## Governing question

> When a Node.js API gives you bytes, which allocation owns them, which views alias them, and at what exact boundary do bytes become text or typed values?

## Public surface

- `encodeEnvelope(kind, payload, maxPayloadBytes)` returns one canonical V1 envelope.

- `decodeEnvelope(input, options)` rejects unsupported versions, truncation, length mismatch, and over-limit payloads.

- `copyPayload` policy is explicit: the reference defaults to an owned payload and permits a view only when the caller asks for it.

- `readHeader` in the starter remains a narrow observation helper; it is not a complete decoder.

## Required invariants

- The header is exactly seven bytes: version, big-endian kind, and big-endian payload length.

- Every successful decode consumes the complete visible input; trailing bytes are rejected.

- No untrusted length controls allocation before the product limit and remaining input are checked.

- Owned decode results do not change when the source buffer is mutated.

- Kind values and configured limits are validated as integers in their declared ranges.

## Implementation sequence

1. Draw the seven-byte header and annotate each offset and width.

2. Complete encoding with initialized allocation and checked integer fields.

3. Implement decode without advancing past an unproved range.

4. Add the owned-payload behavior, then deliberately add and document the optional view behavior.

5. Write canonical vectors and round-trip tests.

6. Add adversarial mutation, truncation, over-limit, and trailing-byte tests.

Do not begin by reading the reference. The starter defines the vocabulary and a baseline, not the final design.

## Adversarial cases

- inputs of 0–6 bytes;

- unsupported version values;

- kind values outside `0..=65535` during encoding;

- a declared length exactly at the limit and one byte beyond it;

- a length smaller or larger than the remaining bytes;

- a source view with a nonzero byte offset into a larger buffer;

- source mutation after owned decode and after view decode;

Add cases in the smallest order that falsifies an incorrect model. Avoid arbitrary sleeps; use exact chunks, counters, injected callbacks, or explicit state transitions.

## Prohibited shortcuts

- using `input.buffer` without preserving the visible offset and length;

- returning a view while documenting an owned payload;

- allocating from the declared length before validating it;

- accepting trailing bytes merely because the first envelope parsed;

- using an assertion to suppress an indexed-access warning;

A shortcut is prohibited because it removes the mechanism the laboratory exists to teach, not because one implementation style is preferred.

## Completion evidence

1. a byte-layout diagram and canonical hex vector;

2. round-trip and malformed-input tests;

3. an aliasing test that distinguishes copy and view modes;

4. a short explanation of why the product limit is checked before allocation;

5. a transfer design for the thumbnail record described in the workbook;

## Independent transfer

Design a binary thumbnail record containing a media type, width, height, and payload. State which fields are validated before allocation and whether the decoded record owns its payload.

Your transfer design must reconstruct the module ledger for the new domain. Renaming the laboratory types is not transfer.

## Comparing with the reference

After your tests pass, inspect `reference/` and locate the first meaningful difference. Adopt it only when it proves an invariant your design misses; otherwise retain the simpler design.
