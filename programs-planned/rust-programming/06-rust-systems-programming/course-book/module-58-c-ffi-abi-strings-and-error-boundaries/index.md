# Module 58 — C FFI: ABI, Strings, Pointers, and Error Boundaries

**Course 6 · Day 8 · Module 58 of 100**
`██████████████░░░░░░░░░░░` **58/100**

[Program](../../../README.md) · [Course 6](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-08-c-abi-archive-validator/README.md) · [FrameVault guide](../capstone.md)

[← Module 57: Manual Allocation and Owning Unsafe Abstractions](../module-57-manual-allocation-and-owning-unsafe-abstractions/index.md) · [Module 59: Foreign Resources, Callbacks, and Wrapper Architecture →](../module-59-foreign-resources-callbacks-and-wrapper-architecture/index.md)

## The question

> How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?

## Why this comes now

The aligned owner is one self-contained unsafe abstraction. FFI combines Rust’s rules with a foreign language and toolchain. Module 58 starts from the ABI contract, not from linker syntax. It uses the Rust 2024 forms `unsafe extern` for imports and `#[unsafe(no_mangle)]` for exported symbols, then builds wrappers that expose only C-compatible representations.

### Prerequisite bridge

Module 57 established **Manual Allocation and Owning Unsafe Abstractions**. Before continuing, verify that you can review auto traits, variance, and reallocation before generalizing an owner. This module preserves that capability and adds the ability to distinguish abi compatibility from semantic validity and ownership. Module 59, **Foreign Resources, Callbacks, and Wrapper Architecture**, will rely on both when it asks: *How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations?*

### Scope boundary

This module owns the reasoning for **c ffi: abi, strings, pointers, and error boundaries** inside Course 6. The course covers single-threaded systems boundaries and narrow unsafe abstractions. Threads, atomics, async I/O, networking, and production measurement are deferred so each external contract remains visible. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Distinguish ABI compatibility from semantic validity and ownership.
- Declare imported functions through `unsafe extern "C"` and document each call contract.
- Export C symbols with stable names and `repr(C)` data structures.
- Use pointer-plus-length for arbitrary bytes and `CStr`/`CString` for NUL-terminated text.
- Prevent Rust panics from crossing non-unwinding foreign boundaries.
- Design error codes and out-parameters that remain valid without Rust layout assumptions.

## Core model

### An ABI is a calling convention, not a safety proof

`extern "C"` tells Rust how arguments, return values, registers, stack, and symbol linkage should follow a C-compatible convention for supported types. It does not prove that a pointer is live, a string is terminated, an integer value is in range, or two libraries agree on ownership.

Every foreign function needs a written contract independent of its Rust declaration. Header, Rust signature, and implementation must agree on exact-width types, nullability, length units, ownership transfer, thread use, and error reporting.

### Rust 2024 makes imported unsafety explicit

Foreign declarations appear in an unsafe external block:

```rust
unsafe extern "C" {
    fn foreign_hash(data: *const u8, length: usize) -> u32;
}
```

Items are unsafe to call unless specifically declared safe under the language rules, because Rust cannot inspect the foreign implementation. Each call site uses an unsafe block and proves the foreign preconditions. The external block’s `unsafe` marks the unchecked import boundary; it does not make every call correct.

### Exported symbols carry a global obligation

A Rust function exported under a stable C name uses a C ABI and an unsafe symbol attribute:

```rust
#[unsafe(no_mangle)]
pub unsafe extern "C" fn framevault_validate(
    bytes: *const u8,
    length: usize,
    report: *mut FvReport,
) -> i32 { /* ... */ }
```

The symbol name must be unique and compatible with every declaration used by linkers and foreign callers. Changing the signature without changing the external contract can cause undefined behavior even when Rust crates compile separately.

### Use C-compatible representations deliberately

`#[repr(C)]` gives structs and enums the corresponding Rust C representation rules, but only fields with FFI-safe types should cross. Prefer fixed-width integers from `std::ffi` or primitive integer widths agreed by the header. Avoid Rust references, slices, `String`, `Vec`, `Option` over arbitrary types, trait objects, and Rust enums with unspecified representation.

For a report:

```rust
#[repr(C)]
pub struct FvReport {
    pub entry_count: u32,
    pub payload_bytes: u64,
    pub error_offset: usize,
}
```

Document padding and initialization requirements if foreign code allocates the structure. Zero every field before returning on failure or define exactly which fields are valid for each status.

### Pointer plus length is a contract pair

A C byte slice is commonly represented as `(*const u8, usize)`. The function must define whether null is permitted when length is zero. A typical contract is:

- if `length == 0`, `bytes` may be null;
- if `length > 0`, `bytes` is non-null, aligned for `u8`, readable for `length` bytes, and remains live for the call;
- no concurrent mutation occurs while Rust reads;
- total length fits the Rust slice API contract.

Rust can check null and numeric limits. It cannot reliably test whether an arbitrary non-null address is mapped and readable. That remains the foreign caller’s safety obligation.

### C strings and byte strings are different interfaces

`CStr` represents a borrowed NUL-terminated C string. `CString` owns bytes with one trailing NUL and rejects interior NUL bytes. Use them only when the foreign API is actually NUL-terminated text.

A path, binary payload, or text that may contain NUL needs pointer-plus-length or a platform-specific string API. Converting arbitrary bytes with `CStr::from_ptr` searches for a terminator and is unsafe because the scan can run beyond valid memory if the contract is false.

Also specify encoding. C strings are byte strings; UTF-8 is a separate agreement.

### Ownership transfer must be visible in function names and types

If Rust returns allocated memory to C, define how C releases it. Do not tell C to call the platform `free` on memory allocated by Rust unless the allocator contract explicitly supports that pairing. A common pattern is an opaque handle returned by `open` and consumed by `free`, both implemented in the same library.

If C gives Rust ownership, state which deallocator applies and whether partial failure transfers ownership. Borrowed pointers should never be stored after the call unless the foreign contract guarantees a longer lifetime and the Rust wrapper represents it safely.

### Error codes need stable meanings

C interfaces cannot return `Result`. Use a stable integer status plus out-parameters or an error-query function. Define each code in a header and keep unknown future codes possible.

FrameVault uses:

```text
0  success
1  invalid argument or pointer contract detectable at boundary
2  invalid archive data
3  allocation failure
4  panic contained at boundary
```

Detailed Rust errors remain internal. The report carries a byte offset for parse failures when available. No borrowed pointer to a temporary Rust error string is returned.

### Do not unwind across a C boundary

A Rust panic crossing an `extern "C"` boundary is not a normal error mechanism and can abort or violate the ABI contract depending on the ABI and configuration. Exported functions should be panic-free by construction or contain panics:

```rust
let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
    // validate and execute
}));
```

Catching panic is a last-resort boundary guard, not permission to use panic for expected errors. Also consider that abort-on-panic builds do not unwind and therefore cannot be caught.

### Foreign callbacks reverse the trust direction

When Rust calls a function pointer supplied by C, the callback’s ABI, nullability, context pointer, reentrancy, and lifetime become part of the contract. The callback must not retain temporary pointers unless explicitly permitted. It must not unwind into Rust through a non-unwind ABI.

Module 59 develops callbacks through an opaque session API. Module 58 first establishes a stateless validator whose ownership is simpler.

### Header and Rust implementation are one versioned API

Treat the C header as a public artifact. Tests should compare sizes and offsets where supported, compile a small C consumer in environments that provide a C toolchain, and verify symbol presence in release builds. The course package includes a checked-in header and Rust-side ABI tests; external C compilation remains part of the executable verification route on a prepared machine.

### Stateless validator boundary, step by step

The exported report is initialized before any fallible work:

```rust
#[repr(C)]
#[derive(Clone, Copy, Debug, Default)]
pub struct FvReport {
    pub entry_count: u32,
    pub payload_bytes: u64,
    pub error_offset: usize,
}
```

The function contract is written both in Rust documentation and the header. The unsafe body should become safe as quickly as possible:

```rust
#[unsafe(no_mangle)]
/// # Safety
/// When `length > 0`, `bytes` must identify `length` readable bytes for the
/// duration of the call. `report` must be non-null, aligned, and writable.
pub unsafe extern "C" fn framevault_validate(
    bytes: *const u8,
    length: usize,
    report: *mut FvReport,
) -> i32 {
    if report.is_null() {
        return FV_INVALID_ARGUMENT;
    }

    // SAFETY: the caller contract requires `report` to be writable and aligned.
    unsafe { report.write(FvReport::default()) };

    let input = if length == 0 {
        &[]
    } else {
        if bytes.is_null() {
            return FV_INVALID_ARGUMENT;
        }
        // SAFETY: the caller contract supplies one readable live byte range.
        unsafe { std::slice::from_raw_parts(bytes, length) }
    };

    match std::panic::catch_unwind(|| validate_bytes(input)) {
        Ok(Ok(summary)) => {
            let output = FvReport {
                entry_count: summary.entry_count,
                payload_bytes: summary.payload_bytes,
                error_offset: 0,
            };
            // SAFETY: same writable out-pointer contract as above.
            unsafe { report.write(output) };
            FV_OK
        }
        Ok(Err(error)) => {
            // Write only the documented parse offset field.
            unsafe { (*report).error_offset = error.offset().unwrap_or(usize::MAX) };
            FV_INVALID_ARCHIVE
        }
        Err(_) => FV_PANIC_CONTAINED,
    }
}
```

The pointer contract cannot be proven inside the function. The null cases are only the detectable subset. The function remains unsafe to call from Rust, while C naturally relies on the header contract.

### ABI type checklist

Before exposing a type, ask:

- Is its layout specified for the ABI?
- Are all field types ABI-safe?
- Is its alignment acceptable to the foreign language?
- Is padding initialized if the foreign side reads raw bytes?
- Can a future version extend it without changing the caller’s allocation size?
- Is ownership of every pointer field stated?
- Are boolean and enum values constrained?

A versioned “size” field is one common extension strategy:

```c
typedef struct {
    uint32_t struct_size;
    uint32_t entry_count;
    uint64_t payload_bytes;
    size_t error_offset;
} FvReport;
```

The callee can write only fields that fit the caller-provided size. FrameVault version 1 keeps a fixed report for course clarity, and its release notes treat size changes as ABI-breaking.

### String return alternatives

Avoid returning a pointer to a temporary `String`. Safer patterns include:

1. caller-provided buffer plus required length;
2. opaque Rust-owned string plus a matching free function;
3. stable numeric codes with formatting left to the caller;
4. callback receiving a temporary byte slice under a call-scoped contract.

FrameVault uses stable codes and structured fields in the validator, then call-scoped names during session enumeration. This avoids global last-error storage.

### C compiler smoke test

On CI with a C toolchain, compile a tiny program against the generated static or dynamic library and checked-in header. The program should validate a known archive, inspect report fields, open an opaque session, enumerate, and free. This catches header drift and linker-symbol issues that Rust-side calls cannot fully prove.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For distinguish ABI compatibility from semantic validity and ownership, construct one positive and one causal negative example. Mark the first decisive fact in the **ABI table** and state which evidence could falsify the claim.

2. **Outcome 2.** For declare imported functions through `unsafe extern "C"` and document each call contract, construct one positive and one causal negative example. Mark the first decisive fact in the **ABI table** and state which evidence could falsify the claim.

3. **Outcome 3.** For export C symbols with stable names and `repr(C)` data structures, construct one positive and one causal negative example. Mark the first decisive fact in the **ABI table** and state which evidence could falsify the claim.

4. **Outcome 4.** For use pointer-plus-length for arbitrary bytes and `CStr`/`CString` for NUL-terminated text, construct one positive and one causal negative example. Mark the first decisive fact in the **ABI table** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

FrameVault exports a stateless `framevault_validate` C function over pointer-plus-length bytes and a `repr(C)` report. It checks null cases it can observe, converts the input to a slice under a documented safety contract, catches unwinding panics where the build strategy permits, maps errors to stable codes, and never returns Rust-owned borrowed text.

The matching independent laboratory is [C ABI Archive Validator](../../labs/module-08-c-abi-archive-validator/README.md). It isolates the mechanism so you can test the proof without carrying the whole capstone in your head.

## Practice sequence

Complete the [workbook](workbook.md) with the C declaration beside each Rust declaration. Build the C ABI Archive Validator lab, classify every pointer as input, output, borrowed, or owning, and verify null, overlap, panic, representation, and status-code rules before examining FrameVault's header and exported functions.

## Ready to continue

You are ready when you can write the C header and Rust signature together, enumerate every pointer and ownership precondition, distinguish detectable invalid arguments from unverifiable pointer validity, and guarantee that ordinary Rust errors and panics do not leak through the ABI.

## Primary Rust references

- [Rust Reference: external blocks](https://doc.rust-lang.org/reference/items/external-blocks.html)
- [Rustonomicon: FFI](https://doc.rust-lang.org/nomicon/ffi.html)
- [Rust standard library: CStr](https://doc.rust-lang.org/std/ffi/struct.CStr.html)
- [Rust standard library: CString](https://doc.rust-lang.org/std/ffi/struct.CString.html)
- [Rust Reference: type layout](https://doc.rust-lang.org/reference/type-layout.html)

## Continue

Continue to [Module 59 — Foreign Resources, Callbacks, and Wrapper Architecture](../module-59-foreign-resources-callbacks-and-wrapper-architecture/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
