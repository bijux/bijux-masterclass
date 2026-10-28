# Laboratory 50 — Generated Code Build

This is the independent product for **Course 5, Module 50: Build Scripts, Generated Code, and Compile-Time Architecture**. Read the [module chapter](../../course-book/module-50-build-scripts-generated-code-and-compile-time-architecture/index.md) and complete its [workbook](../../course-book/module-50-build-scripts-generated-code-and-compile-time-architecture/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Read `schema/commands.tsv` during compilation, validate it, and generate typed Rust under Cargo’s `OUT_DIR`. The checked-in table is the only owner of command name, numeric code, and help text.

Input format:

```text
list	10	List all records
show	20	Show one record
```

The library includes the generated file and exposes an ordered `COMMANDS` slice plus lookup by name and code.

## Required behavior

- Emit `cargo::rerun-if-changed=schema/commands.tsv`.
- Parse exactly three tab-separated fields per nonempty line.
- Reject duplicate names, duplicate codes, invalid identifiers, zero codes, and empty help.
- Preserve source order or sort by a documented key; the reference preserves source order.
- Render deterministic Rust with correctly escaped string literals.
- Write only under `OUT_DIR`.
- Validate the full input before writing the output.

## Adversarial cases

Test tabs inside text, malformed rows, duplicates, invalid codes, missing file, a clean build, and repeated builds with unchanged output. Inspect the generated file and verify that it contains no absolute construction path or timestamp.

## Build sequence

Keep parser and renderer as ordinary functions in `build.rs` so they can be reasoned about separately. Build a normalized row vector, validate all rows, render in memory, and write once.

## Transfer

Add one optional deprecated flag to the schema without duplicating command metadata in runtime code. Specify backward compatibility for old three-field rows.

## Reproducibility proof

Build generation starts with a byte-level input contract. Test blank lines, wrong field counts, invalid identifiers, duplicate names, duplicate numeric codes, out-of-range codes, and tabs inside unsupported fields. Diagnostics must include physical line numbers.

Declare `cargo::rerun-if-changed` for the exact checked-in input. Generate only under `OUT_DIR`, use deterministic source order, and escape every string through a Rust-literal strategy rather than manual quoting. Run the renderer twice on the same validated rows and compare bytes.

The library should expose ordinary lookup functions over the included generated table. Runtime behavior must not reread the schema. In the final review, identify which facts belong to the TSV, which belong to the parser, which are verified by the Rust compiler after inclusion, and which remain runtime policy.

## Working route

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Generated Code Build**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
