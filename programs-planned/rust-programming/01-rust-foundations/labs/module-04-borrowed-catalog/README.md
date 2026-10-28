# Laboratory 4 — Borrowed Catalog

This is the independent product for **Course 1, Module 4: Borrowing, References, Slices, and Strings**. Read the [module chapter](../../course-book/module-04-borrowing-references-slices-and-strings/index.md) and complete its [workbook](../../course-book/module-04-borrowing-references-slices-and-strings/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

### Product contract

Use:

```rust
pub type Record = (u64, String);
```

Implement:

```rust
pub fn find(records: &[Record], id: u64) -> Option<&Record>;
pub fn rename(records: &mut [Record], id: u64, replacement: &str) -> bool;
pub fn first_word(title: &str) -> &str;
pub fn matching_titles<'a>(records: &'a [Record], query: &str) -> Vec<&'a str>;
pub fn total_title_bytes(records: &[Record]) -> usize;
```

The explicit lifetime in `matching_titles` is supplied; Module 8 explains why output is tied to `records` rather than `query`.

### Constraints

- no `.clone()` in production code;
- no `&String` parameters;
- no `&Vec<Record>` parameters;
- listing/searching does not consume the collection;
- renaming performs one mutable search and changes one record;
- returned title slices borrow record strings;
- byte total is explicitly bytes, not characters;
- tests include multibyte UTF-8 text.

### Borrow defense

For each function, state:

- owner of records/titles;
- shared or exclusive access;
- whether result is owned or borrowed;
- final use that ends each borrow;
- caller operations blocked while returned references remain used.

### Adversarial test

Attempt this in a separate specimen:

```rust
let matches = matching_titles(&records, "parser");
rename(&mut records, 1, "decoder");
println!("{matches:?}");
```

Predict the failure. Then reorder use so mutation becomes valid.

### Proof

Run full format/check/clippy/test and a source search for `.clone()`.

Reference: `labs/module-04-borrowed-catalog/solution/`.

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

> Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Borrowed Catalog**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
