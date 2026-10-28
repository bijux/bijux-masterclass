# Module 8 Solutions

## A. Categories

Command tokens are grammar/conversion failures. Missing fields and unknown format are validation/compatibility failures. Invalid transitions are domain failures. Missing file is handled by explicit repository policy; permission and write failures are storage errors. An impossible assertion normally indicates a programmer defect and should not be disguised as user input.

## B. Validation

Prove a non-null non-array record, validate each field independently, accumulate issues, and construct a fresh configuration only when the issue list is empty. Optional path absence differs from an invalid present value.

## C. Cause

Catch `error: unknown` and throw `new StorageError(\`cannot read ${path}\`, { cause: error })`. The caller can inspect category while diagnostics retain the low-level cause.

## D. Encoding

Sort by a named key, construct objects in the canonical field order, omit absent optional fields, stringify with two spaces, and append one newline. Snapshot-like exact-text tests protect the format, while semantic round-trip tests protect meaning.

## E–F. Design notes

StudyLedger must never assert parsed values into the domain. Validate state-specific required fields and duplicate IDs before ledger construction. `nextId` must exceed all retained IDs and remain a positive safe integer.

## G. Readiness answer

Thrown values are unknown. Translation adds boundary context and preserves cause. JSON syntax only creates JavaScript data. Validators establish shape and domain facts. Canonical encoding is product policy. Missing files need a narrow policy. A mutating command succeeds only when its required persistence effect completes.

## Extended solution

The loader must catch only the read operation to identify `ENOENT`, wrap other I/O failures, parse JSON in a separate try/catch, and validate the resulting unknown value. Invalid storage must not become empty state because that silently destroys evidence and may later overwrite recoverable data.

The hostile fixture can report unknown root key, duplicate ID, and several independent field issues together after the root and sessions array are known. Wrong format is also independent. Chronology depends on valid timestamps, so it should be checked only after both parse successfully.

Same-directory temporary write plus rename supports the narrow claim that ordinary readers will not observe a partially written JSON file during a successful single-process replacement. It does not prove crash durability, concurrent-writer correctness, or identical atomic replacement semantics on every platform.
