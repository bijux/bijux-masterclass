# Workbook — Module 01: Compilation, Expressions, and Types

[Return to the chapter](index.md) · [Open the Taskboard engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Compilation, Expressions, and Types** without relying on surface syntax. Keep the module question in view: *How does Rust turn source text into a typed program, and what type and value does every expression produce?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Compilation, Expressions, and Types** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-semicolon-changes-return.rs`](../../compiler-labs/module-01/01-semicolon-changes-return.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-immutable-binding.rs`](../../compiler-labs/module-01/02-immutable-binding.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-array-length-is-type.rs`](../../compiler-labs/module-01/03-array-length-is-type.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-if-arms-one-type.rs`](../../compiler-labs/module-01/04-if-arms-one-type.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-parse-needs-target-type.rs`](../../compiler-labs/module-01/05-parse-needs-target-type.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-shadowing-can-change-type.rs`](../../compiler-labs/module-01/06-shadowing-can-change-type.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 01-rust-foundations
```

## Part 2 — Diagnose and repair


Repair this program without changing the requested report behavior:

```rust
const LIMIT = 5;

fn scaled(value, factor: f64) -> f64 {
    value * factor;
}

fn label(score: i32) -> &str {
    if score >= 80 {
        "high"
    } else {
        0
    }
}

fn main() {
    let readings: [f64; 3] = [10.0, 12.0, 14.0, 16.0];
    let total = 0.0;
    for reading in readings {
        total += scaled(reading, 2.0);
    }
    println!("{} {total}", label(85));
}
```

### Diagnosis order

Do not patch top-to-bottom blindly. Classify errors:

1. `const LIMIT` lacks a required type.
2. `value` lacks a function-parameter type.
3. `scaled` declares `f64` but its semicolon makes the body `()`.
4. `label` returns borrowed text, but its lifetime can be `'static` because both results are literals; the `else` arm has the wrong type.
5. the array annotation says length three while the literal has four elements.
6. `total` must be mutable.
7. `LIMIT` is unused after repair unless incorporated or removed.

### One coherent repair

```rust
const LIMIT: usize = 4;

fn scaled(value: f64, factor: f64) -> f64 {
    value * factor
}

fn label(score: i32) -> &'static str {
    if score >= 80 { "high" } else { "normal" }
}

fn main() {
    let readings: [f64; LIMIT] = [10.0, 12.0, 14.0, 16.0];
    let mut total = 0.0;
    for reading in readings {
        total += scaled(reading, 2.0);
    }
    println!("{} {total}", label(85));
}
```

### Why this is more than syntax repair

The constant now participates in the array type and literal contract. The function signatures state all input/output types. The label function has one result type on every normal path. Mutation is localized to the accumulator.

### Test extraction

Move `scaled` and `label` to `src/lib.rs`, then add:

```rust
#[test]
fn score_boundary_is_explicit() {
    assert_eq!(label(79), "normal");
    assert_eq!(label(80), "high");
}
```

The boundary test is stronger than testing only 85 because it protects the comparison operator.

### Rejected repairs

- removing the array type and constant would compile, but it would discard the exercise's fixed-size contract;
- making every numeric value `f64` would make array length impossible and blur count/value semantics;
- returning `String` from `label` would allocate for fixed literals;
- declaring `total` before it is needed at a broader scope would increase mutable lifetime without benefit.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:


Create one package named `module-01-exercises` with a library and tests. Do not consult answers until the access threshold is met.

### Exercise 1 — Expression table

For each expression, record type and value before compiling:

```rust
{ 3 + 4 }
{ 3 + 4; }
if true { 8 } else { 9 }
(8)
(8,)
[0_u8; 4]
```

Add two examples of your own where one punctuation mark changes the type.

### Exercise 2 — Unit conversions

Implement:

```rust
pub fn celsius_to_fahrenheit(value: f64) -> f64;
pub fn fahrenheit_to_celsius(value: f64) -> f64;
pub fn kilometres_to_miles(value: f64) -> f64;
pub fn seconds_to_hours(value: u64) -> f64;
```

Test zero, one ordinary value, and a negative temperature. Use tolerance for floating-point comparisons.

### Exercise 3 — Fixed three-vector

Implement dot product for exactly three `f64` values:

```rust
pub fn dot3(left: [f64; 3], right: [f64; 3]) -> f64;
```

Explain why arrays, rather than slices, express this contract.

### Exercise 4 — Slice total

Implement a total over any borrowed number of `i64` values. Empty input returns zero because zero is the additive identity; contrast this with minimum.

### Exercise 5 — Honest bounds

Implement:

```rust
pub fn bounds(values: &[i32]) -> Option<(i32, i32)>;
```

No indexing. Test empty, singleton, duplicate, mixed-sign, and descending inputs.

### Exercise 6 — Mean

Implement:

```rust
pub fn mean(values: &[f64]) -> Option<f64>;
```

State the accepted numerical domain. Do not claim support for robust statistics or `NaN` ordering.

### Exercise 7 — Score classification

Implement a total function returning one of four static labels:

- `invalid` outside 0–100;
- `low` for 0–49;
- `normal` for 50–79;
- `high` for 80–100.

Write tests at every boundary.

### Exercise 8 — Shadowed parser

Write:

```rust
pub fn parse_percentage(input: &str) -> Result<u8, &'static str>;
```

Use shadowing for raw, trimmed, and parsed representations. Reject non-integers and values above 100. `Result` is preview syntax; use `map_err` and explicit `match` if needed.

### Exercise 9 — Package inspection

Create a library and binary. Use `cargo metadata` to identify both targets. Write a paragraph distinguishing package, library crate, binary crate, and module.

### Exercise 10 — Proof route

Make these pass with no warning suppression:

```bash
cargo fmt --all -- --check
cargo check --all-targets
cargo clippy --all-targets -- -D warnings
cargo test --all-targets
cargo doc --no-deps
```



## Part 4 — Independent laboratory



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

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: How does Rust turn source text into a typed program, and what type and value does every expression produce?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-01-measurement-report](../../labs/module-01-measurement-report/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

### Outcomes mapped

- Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”.
- Derive the type and value of blocks, branches, tuples, arrays, function bodies, and semicolon-sensitive expressions before compiling.
- Choose numeric types and conversions from domain constraints, including overflow and floating-point limitations, rather than from habit.
- Use compiler diagnostics, tests, rustfmt, Clippy, and rustdoc as separate evidence channels and explain what each channel does not prove.
- Build and verify a small library-plus-binary package with pure calculation separated from rendering.


Create the `taskboard` package skeleton. Do not read the final implementation during the attempt.

### Target behavior

```text
$ taskboard help
taskboard — a local persistent work queue
...
```

The binary should print a stable help screen and package version. Use:

```rust
env!("CARGO_PKG_VERSION")
```

for the version rather than duplicating the manifest string.

### Library boundary

Add to `src/lib.rs`:

```rust
pub const MAX_TITLE_CHARS: usize = 120;

pub fn title_is_valid(title: &str) -> bool {
    // implement the complete Day 1 rule
}
```

The Day 1 title contract:

- nonempty;
- no leading/trailing whitespace;
- at most 120 Unicode scalar values (`chars().count()`);
- no tab, carriage return, or newline.

`&str` borrowing is supplied syntax and explained in Module 4. For now, note that the validator does not need to own or modify the text.

### Required tests

- empty title;
- ordinary title;
- leading/trailing whitespace;
- exactly 120 characters;
- 121 characters;
- tab and line break;
- a multibyte Unicode title to distinguish character count from byte length.

Example boundary construction:

```rust
let exact = "é".repeat(MAX_TITLE_CHARS);
assert!(title_is_valid(&exact));
assert!(exact.len() > MAX_TITLE_CHARS); // UTF-8 bytes differ from char count
```

### Architecture constraint

`main.rs` may select and print help/version. Validation belongs in the library because it is behavior to be reused and tested without launching a process.

### Commit record
Commit message should describe the product fact, not the file operation, for example:

```text
establish taskboard package and title boundary
```

Record the exact types of `env!(...)`, `MAX_TITLE_CHARS`, `title`, and the validator result.

### Final-code comparison

The distributed capstone ultimately centralizes title validation in its model rather than exposing this exact Boolean API. That later refactor is intentional: Module 7 needs validation errors with context, not only true/false. Day 1 proves the rule before error modeling is available.



### Capstone defense

Given an unfamiliar package with several targets, explain what Cargo will build, predict the types of its key expressions, and repair one warning without changing behavior.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

- Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”.
- Derive the type and value of blocks, branches, tuples, arrays, function bodies, and semicolon-sensitive expressions before compiling.
- Choose numeric types and conversions from domain constraints, including overflow and floating-point limitations, rather than from habit.
- Use compiler diagnostics, tests, rustfmt, Clippy, and rustdoc as separate evidence channels and explain what each channel does not prove.
- Build and verify a small library-plus-binary package with pure calculation separated from rendering.

### Closed-book checkpoint

Close notes and source. Complete in 30 minutes.

#### Questions

1. Distinguish package, crate, target, and module in one sentence each.
2. What type/value does `{ 4 + 5; }` produce, and why?
3. Why can shadowing change a binding's type?
4. Why must both ordinary `if` branches produce compatible types?
5. When is `usize` the natural type?
6. Why does `[u8; 16]` differ from `[u8; 32]`?
7. Why should minimum of empty input be `None` rather than zero?
8. What does `cargo check` prove that rustfmt does not?
9. Why does a floating-point equality test usually use tolerance?
10. Write a function that returns the larger of two `i32` values using an `if` expression and no explicit `return`.

#### Prediction

Without compiling:

```rust
fn result(flag: bool) -> i32 {
    let value = if flag { 3 } else { 4 };
    {
        value * 2
    }
}
```

State the type of each block and output for both inputs. Then add one semicolon that causes a compile error and identify the new type.

#### Practical reconstruction

From an empty directory:

```bash
cargo new --lib checkpoint-one
```

Implement `bounds(&[i32]) -> Option<(i32, i32)>` and three tests without reading prior code.

### Transfer defense

Given an unfamiliar package with several targets, explain what Cargo will build, predict the types of its key expressions, and repair one warning without changing behavior.

Your answer must include:
