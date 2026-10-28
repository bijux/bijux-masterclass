# Laboratory 58 — C ABI Line Validator

This is the independent product for **Course 6, Module 58: C FFI: ABI, Strings, Pointers, and Error Boundaries**. Read the [module chapter](../../course-book/module-58-c-ffi-abi-strings-and-error-boundaries/index.md) and complete its [workbook](../../course-book/module-58-c-ffi-abi-strings-and-error-boundaries/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Expose a small C-compatible function that validates a byte buffer as newline-delimited UTF-8 records and fills a `repr(C)` report. The lab focuses on pointer-plus-length, out-parameter initialization, stable status codes, and panic containment.

## Why this laboratory exists

This lab treats the C declaration as part of the implementation. The Rust function is correct only when representation, pointer ranges, null rules, output initialization, status codes, and panic behavior match the foreign caller's model. The parser remains safe Rust; unsafe code should be limited to validating and translating the ABI boundary.

## Contract

`line_report(bytes,len,out)` returns 0 on valid UTF-8, 1 for detectable invalid arguments, 2 for invalid UTF-8, and 3 for contained panic. Null bytes are allowed only when length is zero. `out` is required and initialized before ordinary validation. The report stores line count, byte count, and invalid offset.

## Required milestones

1. Define the C header contract before Rust implementation.
2. Keep a pure safe analyzer separate from the exported boundary.
3. Convert raw input to a slice in one documented unsafe block.
4. Initialize the report before all fallible work.
5. Catch unwind at the boundary without using panic as an expected error.

## Adversarial cases

- null output
- null input with nonzero length
- null input with zero length
- empty input
- invalid UTF-8
- final line without newline
- embedded NUL treated as an ordinary byte

## Evidence to produce

- a side-by-side C/Rust signature and field-layout table;
- a pointer contract for null, zero length, alignment, writability, and non-overlap;
- tests for valid input, malformed input, null output, null-plus-zero input, and initialized reports on failure;
- a status-code table with stable meanings;
- a C11 header consumer compiled with warnings treated as errors.

## Prohibited shortcuts

Do not expose `String`, `Vec`, references, `bool`, Rust enums without a fixed representation, or `Result` across the ABI. Do not form a slice before checking the null/length rule, let a Rust panic unwind into C, write through an unvalidated output pointer, or assume the caller supplied non-overlapping storage without saying so.

## Transfer

Extend the interface with caller-provided storage for the first invalid line, including required-length reporting and no partial string ownership.

## Comparing with the reference

Read the header first, then audit the Rust body against it. Check output initialization on every return, the exact error offset for malformed bytes, and panic containment. A function that works from Rust tests but has no matching C declaration or foreign syntax check is not a finished FFI boundary.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the contract, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer this question without the chapter:

> How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
