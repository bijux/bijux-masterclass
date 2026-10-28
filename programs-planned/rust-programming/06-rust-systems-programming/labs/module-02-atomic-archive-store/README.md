# Laboratory 52 — Atomic Archive Store

This is the independent product for **Course 6, Module 52: Files, Durability, and Transactional Replacement**. Read the [module chapter](../../course-book/module-52-files-durability-and-transactional-replacement/index.md) and complete its [workbook](../../course-book/module-52-files-durability-and-transactional-replacement/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a file replacement component that preserves the previous valid destination until a complete staged file has been written, flushed, synchronized, and renamed.

## Why this laboratory exists

This lab isolates one persistence transaction so the commit point cannot hide behind an archive model. The difficult part is not calling `write_all`; it is reporting what remains visible and what may be durable after each failure. Build the state machine before reading the reference and keep pre-commit failure separate from post-commit synchronization failure.

## Contract

`replace_bytes` stages in the destination directory, creates the temporary file with `create_new`, writes all bytes, flushes, calls `sync_all`, closes the handle, then renames. Pre-rename failure leaves the old destination unchanged. A parent-directory synchronization failure is reported as a post-commit state because the replacement has already occurred. The API does not claim universal crash durability and exposes stage-specific errors.

## Required milestones

1. Separate encoding from filesystem effects.
2. Generate bounded collision-resistant temporary names and open atomically.
3. Preserve stage, source path, destination path, and `io::Error`.
4. Clean up an abandoned temp without hiding the primary error.
5. Test old-value preservation and successful replacement.

## Adversarial cases

- existing temporary-name collision
- destination parent missing
- read-only or otherwise unwritable destination directory where testable
- empty payload
- replacement of an existing file
- cleanup after an injected writer failure

## Evidence to produce

- a state diagram from old destination through staged candidate and committed replacement;
- a failure table covering create, write, flush, file sync, rename, and parent sync;
- tests that inspect destination bytes after representative pre-commit failures;
- proof that the temporary file is created in the destination directory with `create_new`;
- a qualified success claim for each supported target family.

## Prohibited shortcuts

Do not truncate the destination in place, stage on an unrelated filesystem, reuse a predictable temporary file without exclusive creation, call a single write and assume completeness, hide cleanup failure as the primary error, or describe rename as universally durable and replacing on every platform. The old value must remain untouched until the explicit commit operation.

## Transfer

Adapt the protocol to a configuration snapshot and write a claim ladder distinguishing flush, file sync, rename, and directory durability.

## Comparing with the reference

Locate the exact commit point in both implementations. Then compare how each design represents a parent-directory sync failure that occurs after the new pathname is already installed. Prefer the API that prevents a caller from interpreting a committed new value as an untouched old value.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the contract, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer this question without the chapter:

> What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
