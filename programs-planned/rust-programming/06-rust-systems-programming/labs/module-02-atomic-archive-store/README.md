# Laboratory 52 — Atomic Archive Store

**Course 6 · Module 52: Files, Durability, and Transactional Replacement**

[Chapter](../../course-book/module-52-files-durability-and-transactional-replacement/index.md) · [Workbook](../../course-book/module-52-files-durability-and-transactional-replacement/workbook.md) · [FrameVault guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Files, Durability, and Transactional Replacement**: What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state? The product must make **Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **durability timeline** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a file replacement component that preserves the previous valid destination until a complete staged file has been written, flushed, synchronized, and renamed.

## Product-specific design pressure

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

For **Laboratory 52 — Atomic Archive Store**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Atomic Archive Store**.
2. Draw the smallest **durability timeline** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to FrameVault so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability.
- Handle short reads and writes through the `Read` and `Write` contracts.
- Use `OpenOptions` to make creation and truncation policy explicit.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 52 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **durability timeline**. Defend why your design is simpler than one plausible alternative under the new requirements.
