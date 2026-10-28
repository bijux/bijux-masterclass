# Module 41 Workbook — Binary Data: Buffer, Uint8Array, Encodings, and Memory Views

Complete this file before opening `solutions.md`. Record predictions in writing; a result observed after running code is not a prediction.

## 1. Predict the mechanism

### Aliasing after return

A decoder returns `input.subarray(7)`. The caller overwrites the source buffer before consuming the result. Predict the observed payload and identify which contract was missing.

### Visible range versus backing store

A `Uint8Array` shows bytes 100–119 of a larger buffer. Predict what `Buffer.from(view.buffer)` contains compared with `Buffer.from(view)`.

### Permissive hexadecimal input

Predict the result of decoding an odd-length or invalid hex string with `Buffer.from(text, "hex")`. Explain why successful conversion is not protocol validation.

### Length-prefix allocation

A four-byte prefix declares 2 GiB while only twelve bytes remain. Order the checks that must occur before any slice or allocation.

## 2. Diagnose and repair

### Stable payload ownership

Repair an envelope decoder that returns a shared view even though callers are promised an immutable, independently owned payload.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Canonical token decoding

Replace direct hex conversion with a validator that rejects odd length, non-hex characters, non-canonical case if the format requires lowercase, and decoded data above a product limit.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

### Failure-atomic cursor

Repair a cursor that increments its offset before proving a field is present. Preserve exact error offsets for truncated input.

State the preserved requirement, the causal defect, and the terminal evidence after repair.

## 3. Focused construction

1. Implement `copyVisibleBytes` and `viewVisibleBytes` with tests that prove their different mutation behavior.

2. Encode and decode unsigned 16-bit and 32-bit big-endian fields with range checks.

3. Add a product limit that is checked before payload allocation.

4. Create canonical test vectors and reject trailing bytes.

5. Add a mutation test for the input after decode and a retention discussion for small views of large buffers.

6. Write one structured error containing field name and byte offset.

For each construction, add a negative test against the obvious shortcut. Prefer exact byte counts, source indices, or injected operation counts to arbitrary delays.

### Mechanism experiment

Recreate the chapter's extended case in the smallest executable form. Vary at least three conditions drawn from the laboratory's adversarial list:

- inputs of 0–6 bytes;

- unsupported version values;

- kind values outside `0..=65535` during encoding;

Record which observation changes, which remains stable, and whether the difference belongs to representation, scheduling, capacity, or product semantics.

## 4. Independent laboratory — Bounded Binary Envelope

Implement a versioned binary envelope with a fixed header, big-endian fields, product limits, canonical length checks, explicit copy-versus-view APIs, and mutation tests.

Before implementation, submit:

- the public API and represented data at every boundary;

- the module-specific ledger from the chapter;

- the success and failure state machine;

- exact capacity limits and units;

- tests that distinguish the design from each prohibited shortcut in the laboratory brief.

Build from `starter/`. Open `reference/` only after your own happy-path and adversarial tests pass.

## 5. FlowLedger transfer

Define FlowLedger byte limits and the raw-byte accounting layer. Add a copy-safe buffer utility, SHA-256 input tap, and tests that distinguish visible ranges from backing allocations.

Write a short change record containing:

1. the stage or edge added to FlowLedger;
2. the previous invariant most at risk;
3. the new bound or terminal state;
4. the error and cancellation route;
5. the test that proves chunking or scheduling does not change promised semantics.

## 6. Independent transfer

Design a binary thumbnail record containing a media type, width, height, and payload. State which fields are validated before allocation and whether the decoded record owns its payload.

Produce a small executable proof and a design note. The proof must exercise the difficult boundary directly rather than converting the task into an already bounded in-memory array.

### Review artifact

Complete the module ledger with actual names from your implementation:

- **backing store:** Which `ArrayBuffer` owns the physical bytes, and can another view mutate it?

- **visible range:** What are the exact `byteOffset` and `byteLength` exposed by this value?

- **copy policy:** Does the callee observe temporarily, retain a shared view, or own a copy?

- **interpretation:** Are these bytes opaque, UTF-8, hexadecimal text, or fixed-width fields?

- **integer proof:** Which arithmetic establishes every offset and length before access or allocation?

- **canonical form:** Can two different byte sequences represent the same logical value, and is that allowed?

A row containing “Node handles it” is incomplete. Replace it with the responsible object, promise, event, bound, or publication step.

## 7. Closed-book defense

1. Why is `Buffer` compatibility with `Uint8Array` useful but insufficient as an ownership contract?

2. When is a view the stronger design than a copy?

3. Which byte count belongs in an external protocol limit?

4. What makes a binary representation canonical?

Finish by drawing the smallest diagram that captures the module’s owner, retained state, pressure or progress signal, and terminal observation.
