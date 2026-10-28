# Reasoned Solutions — Module 58: C FFI: ABI, Strings, Pointers, and Error Boundaries

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-08-c-abi-archive-validator/README.md) · [FrameVault guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 58: C FFI: ABI, Strings, Pointers, and Error Boundaries**. Compare the reasoning against this question: *How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Prediction analysis

### Prediction 1

**Problem.** A function is `extern "C"` but takes `String`. Is ABI spelling enough?

**Reasoned answer.** No. `String` has Rust-specific layout and ownership and is not a stable C ABI type.

### Prediction 2

**Problem.** A non-null pointer is passed with length 100. Can Rust prove 100 readable bytes exist?

**Reasoned answer.** No. Null checks do not validate arbitrary address ranges.

### Prediction 3

**Problem.** `CStr::from_ptr` receives a nonterminated buffer. What may happen?

**Reasoned answer.** The scan can read beyond valid memory, causing undefined behavior.

### Prediction 4

**Problem.** C frees a `CString::into_raw` pointer with its own `free`. Is that generally valid?

**Reasoned answer.** No. The matching Rust reclamation function or documented allocator pairing is required.

### Prediction 5

**Problem.** A Rust panic reaches a C caller. Is it a stable error code?

**Reasoned answer.** No. Unwinding across the boundary is not the contract and may abort or be undefined for the ABI.

### Prediction 6

**Problem.** A `repr(C)` struct has an uninitialized output field on error. May C read it?

**Reasoned answer.** Only if the contract says it is initialized; otherwise the function should initialize fields or mark them invalid by status.

### Prediction 7

**Problem.** The export uses `#[no_mangle]` in Edition 2024. What syntax is expected?

**Reasoned answer.** The unsafe attribute form `#[unsafe(no_mangle)]` makes the global obligation explicit.

### Prediction 8

**Problem.** A callback stores a pointer to a temporary entry name. What contract was violated?

**Reasoned answer.** The pointer was valid only during the callback unless retention was explicitly supported.

## Construction guidance

### Header pairing

Every C declaration must match ABI, integer widths, mutability, and struct representation. The header carries the same versioned contract as Rust docs.

### Pointer validation

Rust can reject obvious null misuse but cannot safely probe arbitrary addresses. The unsafe caller contract remains necessary.

### Owned string

Return an opaque pointer created by Rust and expose one Rust function that consumes it exactly once; document null on failure.

### Panic boundary

Wrap the internal safe operation, map typed errors first, and return a dedicated contained-panic status without exposing Rust panic payloads.

### Output array

The caller provides storage and capacity; the callee writes at most capacity and reports an initialized count that the wrapper validates.

## Boundary-trace reference

A strong solution trace for this module must place the C declaration and Rust declaration side by side. Trace each pointer, length, output slot, representation field, status code, and panic path from foreign call through safe parsing and back. Mark the point at which a Rust reference or slice may first exist. It should reveal the earliest point at which an invalid assumption would become observable and the unique owner responsible for cleanup or rollback.

## Weak repairs to reject

Reject solutions built around these shortcuts:

- exporting `String`, `Vec`, Rust references, or `Result` directly;
- assuming `repr(C)` makes every field FFI-safe;
- creating a slice before applying the null-plus-zero rule;
- leaving output memory uninitialized on failure;
- allowing panic to unwind across the ABI;
- using platform-sized or undocumented enum representations in the header;

A principled repair makes the missing fact explicit in a type, checked operation, state transition, safety contract, platform qualification, or foreign-call contract. It does not merely move the assumption to a less visible line.

## ABI contract matrix

| Boundary element | Rust side | C-side obligation |
|---|---|---|
| input bytes | `*const u8` plus `usize` | null only under the documented zero-length rule; otherwise readable for the call |
| output report | `*mut FvReport` | non-null, aligned, writable, and non-overlapping as required |
| report layout | `#[repr(C)]` fixed-width fields | compile against the matching header and allocate the declared size/alignment |
| status | stable integer constants | handle unknown future values without assuming a closed Rust enum |
| panic | contained where unwinding exists | no foreign callback or caller may unwind through the non-unwind ABI |

Initialize the output report before fallible parsing so every return code has a defined observable state. This avoids forcing C callers to guess which fields contain indeterminate bytes after failure.

## String and ownership clinic

A C string is a NUL-terminated byte protocol, not automatically UTF-8 and not suitable for arbitrary binary data. `CStr::from_ptr` is unsafe because the terminator search depends on the caller’s readable-memory promise. Pointer-plus-length is the clearer contract for archive bytes.

Never return a pointer into a temporary Rust `String`. Use a caller-provided buffer, stable numeric/status data, a call-scoped callback view, or an opaque Rust-owned allocation with a matching Rust free function. Allocation and deallocation authority must stay paired across the ABI.

Finally, compile a real C and C++ consumer against the checked-in header when the toolchain is available. Rust-side tests cannot detect every header spelling, language-compatibility, linker-symbol, or calling-convention drift.

## Completion check

Use the chapter’s readiness statement as the first threshold:

You are ready when you can write the C header and Rust signature together, enumerate every pointer and ownership precondition, distinguish detectable invalid arguments from unverifiable pointer validity, and guarantee that ordinary Rust errors and panics do not leak through the ABI.

Then perform this destructive regression check: call the boundary with null-plus-zero input, null output, invalid UTF-8, and a valid buffer, and inspect the report state on every return. The resulting failure should be caught for the causal reason predicted in the workbook, not by an unrelated panic or syntax error.

## Deep reasoning and transfer

### Decisive model

> How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?

Build a **ABI table**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish ABI compatibility from semantic validity and ownership.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Declare imported functions through `unsafe extern "C"` and document each call contract.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Export C symbols with stable names and `repr(C)` data structures.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Use pointer-plus-length for arbitrary bytes and `CStr`/`CString` for NUL-terminated text.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Prevent Rust panics from crossing non-unwinding foreign boundaries.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish ABI compatibility from semantic validity and ownership.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the ABI table.

### Reference implementation comparison

For [C ABI Line Validator](../../labs/module-08-c-abi-archive-validator/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In FrameVault, Module 58 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **C FFI: ABI, Strings, Pointers, and Error Boundaries**, which relationship decides this question: “How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to FrameVault?
