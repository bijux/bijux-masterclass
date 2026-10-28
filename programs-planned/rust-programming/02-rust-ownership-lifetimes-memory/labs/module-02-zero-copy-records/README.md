# Laboratory 12 — Zero-Copy Records

This is the independent product for **Course 2, Module 12: Lifetime Relationships and Borrowed APIs**. Read the [module chapter](../../course-book/module-12-lifetime-relationships-and-borrowed-apis/index.md) and complete its [workbook](../../course-book/module-12-lifetime-relationships-and-borrowed-apis/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product


Implement `labs/module-02-zero-copy-records/starter`.


Parse a line-oriented metadata block without allocating key or value strings when input is already valid.

Input:

```text
name: Ada
language: Rust
role: systems engineer
```

### Public types

```rust
pub struct Field<'source> { /* key/value slices */ }
pub struct Record<'source> { /* source plus fields */ }
pub enum ParseError { /* line, reason */ }
```

### Contract

- the record and every field borrow from caller-owned source;
- blank lines are ignored;
- keys and values are trimmed by slicing, not allocation;
- empty keys are rejected with one-based line number;
- duplicate keys are rejected;
- `get` returns a value tied to the record/source;
- `into_fields` may consume the record while preserving source-lifetime slices;
- `to_owned` produces an independent owned representation;
- no reference may derive from a local normalized buffer.

### Required lifetime work

Implement at least one method where receiver elision is sufficient and one consuming method returning `'source`. Document the difference.

### Adversarial tests

- source dropped before attempted record use must be a compile-fail example in docs;
- Unicode input;
- leading/trailing whitespace;
- duplicate after trimming;
- empty and whitespace-only lines;
- owned conversion remains usable after source destruction.

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

> What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Zero-Copy Records**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
