# Laboratory 1 — Measurement Report

This is the independent product for **Course 1, Module 1: Compilation, Expressions, and Types**. Read the [module chapter](../../course-book/module-01-compilation-expressions-and-types/index.md) and complete its [workbook](../../course-book/module-01-compilation-expressions-and-types/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How does Rust turn source text into a typed program, and what type and value does every expression produce?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

### Product contract

Build a small library and binary that summarize borrowed `f64` measurements.

```rust
pub struct Summary {
    pub count: usize,
    pub minimum: f64,
    pub maximum: f64,
    pub total: f64,
    pub mean: f64,
}

pub fn summarize(values: &[f64]) -> Option<Summary>;
pub fn render(summary: Option<Summary>) -> String;
```

Struct syntax is supplied for this lab and taught formally in Module 5. Treat `Summary` as a named tuple whose fields document result meaning.

### Required behavior

- Empty input returns `None` and renders `No measurements.\n`.
- Nonempty input computes count, minimum, maximum, total, and arithmetic mean.
- Calculation does not print.
- Rendering does not recalculate.
- Output is deterministic and uses two decimal places for numeric fields.
- The implementation does not index the slice.
- Tests cover empty, singleton, mixed-sign, duplicates, and ordinary multi-value input.
- Floating-point assertions use a documented tolerance.

### Design questions before code

1. Why is `Option<Summary>` more accurate than a `Summary` filled with zeros?
2. Which fields can be derived from others, and why retain them in the report value?
3. What numerical inputs does the lab accept?
4. Why should render accept an already computed result?
5. Which function is pure?

### Acceptance tests

At minimum:

```rust
#[test]
fn empty_input_has_no_summary() {
    assert_eq!(summarize(&[]), None);
}

#[test]
fn mixed_values_preserve_sign_and_range() {
    let summary = summarize(&[-2.0, 4.0, 10.0]);
    assert_eq!(summary.map(|value| value.minimum), Some(-2.0));
    assert_eq!(summary.map(|value| value.maximum), Some(10.0));
}
```

`Summary` needs `PartialEq` to compare an entire optional value. It cannot derive `Eq` because of `f64`.

### Required proof

```bash
cargo fmt --all -- --check
cargo check --all-targets
cargo clippy --all-targets -- -D warnings
cargo test --all-targets
cargo run --quiet
```

### Design note

Submit 300–500 words explaining:

- block/return types in `summarize`;
- empty-input semantics;
- why count uses `usize` and values use `f64`;
- why the result is named rather than a five-element tuple;
- one limitation of the numerical method.

### Reference implementation

After completing the independent attempt, compare with `labs/module-01-measurement-report/solution/`. Compare contracts and tests before code shape.

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

> How does Rust turn source text into a typed program, and what type and value does every expression produce?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Measurement Report**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
