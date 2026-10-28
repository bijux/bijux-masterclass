# Workbook — Module 51: Binary Data Contracts: Bytes, Endianness, and Checked Parsing

[Chapter](index.md) · [Laboratory](../../labs/module-01-checked-frame-codec/README.md) · [FrameVault guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Binary Data Contracts: Bytes, Endianness, and Checked Parsing** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you turn untrusted bytes into typed values without confusing representation, validation, allocation, and meaning?* Preserve your first prediction and record decisive facts in a **binary layout and range proof**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 50 — Build Scripts, Generated Code, and Compile-Time Architecture that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you turn untrusted bytes into typed values without confusing representation, validation, allocation, and meaning?**
3. Draw the smallest **binary layout and range proof** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

A parser reads a `u64` length with `as usize` and then slices. Predict the two distinct failures possible on 32-bit and 64-bit targets.

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

A cursor increments its offset before calling `get`. The input is truncated. Which state is now false?

For **Prediction 2**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

A file stores `u32::to_ne_bytes`. Can another architecture decode it portably?

For **Prediction 3**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

A name uses `String::from_utf8_lossy`. Does the decoder still preserve the original identity?

For **Prediction 4**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

Each payload is limited to 1 MiB, but entry count is one million. Is the allocation policy bounded?

For **Prediction 5**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

The checksum matches. Is the producer authenticated?

For **Prediction 6**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

The parser returns `&[u8]` payloads. May the input vector be mutated while views exist?

For **Prediction 7**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

The decoder accepts valid entries and ignores trailing bytes. What compatibility risk appears?

For **Prediction 8**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

## Part 2 — Diagnose and repair

### Boundary trace

Trace the decoder from the raw byte slice through each checked range, integer conversion, length calculation, UTF-8 validation, allocation decision, and domain constructor. Your table must include the cursor offset before and after every successful read and the exact state preserved on truncation.

For **Binary Data Contracts: Bytes, Endianness, and Checked Parsing**, choose table columns that expose the actual states rather than copying a generic checklist. Every row must name the owner, the fact established, the fact still delegated, the visible failure effect, and the component responsible for cleanup or rollback.

### Weak repairs to reject

For each prediction, identify a superficially convenient repair that violates the module contract. Reject at least these module-specific shortcuts:

- casting an untrusted `u64` length with `as usize`;
- advancing the cursor before `get` proves the range;
- allocating from a per-entry length without a cumulative budget;
- accepting lossy UTF-8 as archive identity;
- treating a checksum as producer authentication;
- ignoring trailing bytes without a version rule;

Replace each with the smallest repair that preserves the requirement and state what evidence would distinguish the two designs.

## Part 3 — Focused exercises

### Construction 1

Design the exact byte layout for a two-entry archive and compute every offset by hand.

Required evidence: Produce an offset table from byte zero through the final payload; include integer widths and name/payload boundaries.

### Construction 2

Write a safe `Cursor::take` and three integer readers without indexing or unsafe code.

Required evidence: The cursor may mutate only after the requested range is proven.

### Construction 3

Define a limit model that prevents huge single allocations and huge aggregate allocations.

Required evidence: Include maximum entries, name size, per-payload size, and checked total payload.

### Construction 4

Explain whether a checksum failure belongs to structural parsing or application policy.

Required evidence: Place it in integrity validation after bounds are known; state why it is not authentication.

### Construction 5

Transfer the method to a sensor packet with a fixed header and variable samples.

Required evidence: Write the format, bounds, endianness, and error-offset policy before code.

### Interleaved reasoning pass

1. For **Define a binary format as a versioned contract rather than a sequence of convenient writes**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the binary layout and range proof.
2. For **Trace byte offsets, item widths, endianness, and length arithmetic before allocating**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the binary layout and range proof.
3. For **Build a bounds-first cursor that never advances after failure**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the binary layout and range proof.
4. For **Separate structural validity, textual validity, integrity checks, and domain validation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the binary layout and range proof.

5. Identify one guarantee from an earlier course that a careless implementation of **Binary Data Contracts: Bytes, Endianness, and Checked Parsing** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Checked Frame Codec](../../labs/module-01-checked-frame-codec/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- a byte-offset table for every field in one valid frame;
- a cursor invariant stating when position may advance;
- exhaustive truncation tests over every prefix of a golden frame;
- boundary tests for zero, maximum, one-above-limit, and overflowing lengths;
- an explanation of why checksum success establishes corruption detection rather than authenticity.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

### Laboratory acceptance trace

Before opening the reference implementation for **Checked Frame Codec**, record:

- the public behavior that demonstrates **Define a binary format as a versioned contract rather than a sequence of convenient writes**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

### Capstone invariant trace

For the Module 51 FrameVault increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. Which checked expression proves every slice boundary?
2. Which limits prevent both one huge allocation and many individually small allocations?
3. Where does structural decoding end and domain validation begin?
4. Why is canonical encoding a compatibility decision rather than a formatting preference?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Design a `SENSOR01` packet format with a timestamp, signed reading count, and a sequence of little-endian `i16` readings. The count is untrusted. State exact widths, maximum readings, cumulative byte calculation, and trailing-data policy before writing code. Implement decoding without indexing and produce an error offset for every malformed fixture. Then change the format so the reading payload may be compressed in a future version: decide which reserved field or version rule prevents an old decoder from silently misreading new bytes.

### Closed-book defense

In five minutes, answer “How do you turn untrusted bytes into typed values without confusing representation, validation, allocation, and meaning?” using the **binary layout and range proof**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside FrameVault. A list of APIs without the deciding relationship is incomplete.
