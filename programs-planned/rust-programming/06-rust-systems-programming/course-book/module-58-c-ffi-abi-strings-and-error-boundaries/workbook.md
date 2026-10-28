# Workbook — Module 58: C FFI: ABI, Strings, Pointers, and Error Boundaries

[Chapter](index.md) · [Laboratory](../../labs/module-08-c-abi-archive-validator/README.md) · [FrameVault guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **C FFI: ABI, Strings, Pointers, and Error Boundaries** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?* Preserve your first prediction and record decisive facts in a **ABI table**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 57 — Manual Allocation and Owning Unsafe Abstractions that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?**
3. Draw the smallest **ABI table** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

A function is `extern "C"` but takes `String`. Is ABI spelling enough?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

A non-null pointer is passed with length 100. Can Rust prove 100 readable bytes exist?

For **Prediction 2**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

`CStr::from_ptr` receives a nonterminated buffer. What may happen?

For **Prediction 3**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

C frees a `CString::into_raw` pointer with its own `free`. Is that generally valid?

For **Prediction 4**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

A Rust panic reaches a C caller. Is it a stable error code?

For **Prediction 5**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

A `repr(C)` struct has an uninitialized output field on error. May C read it?

For **Prediction 6**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

The export uses `#[no_mangle]` in Edition 2024. What syntax is expected?

For **Prediction 7**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

A callback stores a pointer to a temporary entry name. What contract was violated?

For **Prediction 8**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

## Part 2 — Diagnose and repair

### Boundary trace

Place the C declaration and Rust declaration side by side. Trace each pointer, length, output slot, representation field, status code, and panic path from foreign call through safe parsing and back. Mark the point at which a Rust reference or slice may first exist.

For **C FFI: ABI, Strings, Pointers, and Error Boundaries**, choose table columns that expose the actual states rather than copying a generic checklist. Every row must name the owner, the fact established, the fact still delegated, the visible failure effect, and the component responsible for cleanup or rollback.

### Weak repairs to reject

For each prediction, identify a superficially convenient repair that violates the module contract. Reject at least these module-specific shortcuts:

- exporting `String`, `Vec`, Rust references, or `Result` directly;
- assuming `repr(C)` makes every field FFI-safe;
- creating a slice before applying the null-plus-zero rule;
- leaving output memory uninitialized on failure;
- allowing panic to unwind across the ABI;
- using platform-sized or undocumented enum representations in the header;

Replace each with the smallest repair that preserves the requirement and state what evidence would distinguish the two designs.

## Part 3 — Focused exercises

### Construction 1

Write a C header and matching Rust declarations for archive validation.

Required evidence: Use exact-width fields, explicit status codes, pointer-plus-length, and documented null rules.

### Construction 2

Implement boundary validation without pretending to validate mapped memory.

Required evidence: Check null/zero combinations and numeric limits; leave liveness as a safety precondition.

### Construction 3

Design an owned-string return API and its matching free function.

Required evidence: State allocator ownership and failure behavior.

### Construction 4

Show how to contain panic and map typed errors.

Required evidence: Keep expected errors as `Result`; reserve panic containment for boundary protection.

### Construction 5

Transfer the method to a C function that fills an output array.

Required evidence: Define capacity, written count, initialization, and ownership on every status.

### Interleaved reasoning pass

1. For **Distinguish ABI compatibility from semantic validity and ownership**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the ABI table.
2. For **Declare imported functions through `unsafe extern "C"` and document each call contract**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the ABI table.
3. For **Export C symbols with stable names and `repr(C)` data structures**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the ABI table.
4. For **Use pointer-plus-length for arbitrary bytes and `CStr`/`CString` for NUL-terminated text**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the ABI table.

5. Identify one guarantee from an earlier course that a careless implementation of **C FFI: ABI, Strings, Pointers, and Error Boundaries** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [C ABI Line Validator](../../labs/module-08-c-abi-archive-validator/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- a side-by-side C/Rust signature and field-layout table;
- a pointer contract for null, zero length, alignment, writability, and non-overlap;
- tests for valid input, malformed input, null output, null-plus-zero input, and initialized reports on failure;
- a status-code table with stable meanings;
- a C11 header consumer compiled with warnings treated as errors.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

### Laboratory acceptance trace

Before opening the reference implementation for **C ABI Line Validator**, record:

- the public behavior that demonstrates **Distinguish ABI compatibility from semantic validity and ownership**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

### Capstone invariant trace

For the Module 58 FrameVault increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. What exact C and Rust types correspond?
2. What null, length, alignment, writability, and overlap rules apply?
3. Which outputs are initialized on every return?
4. How are status codes and panic containment specified?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Specify a C function that validates a borrowed record and writes a fixed-layout report. First write the C header. Then write the Rust export with a null/zero matrix, output initialization rule, integer statuses, `#[unsafe(no_mangle)]`, explicit unsafe blocks, and panic containment. Test null output, null/zero input, null/nonzero input, malformed bytes, valid bytes, and a report offset. Explain which invalid raw pointers cannot be safely tested because merely passing them violates the caller contract.

### Closed-book defense

In five minutes, answer “How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?” using the **ABI table**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside FrameVault. A list of APIs without the deciding relationship is incomplete.
