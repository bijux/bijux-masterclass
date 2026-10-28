# Laboratory 13 — Scoped Visitors

This is the independent product for **Course 2, Module 13: Scoped Access and Escape Prevention**. Read the [module chapter](../../course-book/module-13-scoped-access-and-escape-prevention/index.md) and complete its [workbook](../../course-book/module-13-scoped-access-and-escape-prevention/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product


Build `ScopedText`, a safe text-processing component that owns one reusable scratch buffer and exposes transformed records only inside callback scope.

The executable surfaces are under:

```text
labs/module-03-scoped-visitors/
├── starter/
└── solution/
```

### Required behavior

`ScopedText` must provide:

```rust
pub struct ScopedText { /* private */ }

impl ScopedText {
    pub fn new() -> Self;

    pub fn with_normalized<R>(
        &mut self,
        raw: &str,
        operation: impl for<'view> FnOnce(&'view str) -> R,
    ) -> R;

    pub fn visit_words<F>(&mut self, raw: &str, visitor: F)
    where
        F: for<'word> FnMut(&'word str);
}
```

Normalization trims leading/trailing whitespace, collapses each run of Unicode whitespace to one ASCII space, and lowercases characters with Rust's Unicode lowercase expansion. `visit_words` must expose words from the normalized scratch buffer without allocating one `String` per word.

### Adversarial cases

Use Turkish dotted capital I, German sharp-s behavior as provided by Unicode lowercase mappings, empty input, and a string with several kinds of whitespace. Do not promise locale-aware case folding; state exactly what `char::to_lowercase` provides.

### Acceptance

```bash
cargo test -p rust-olm-lab-03-scoped-visitors --all-targets
cargo clippy -p rust-olm-lab-03-scoped-visitors --all-targets -- -D warnings
```

A solution fails conceptually if it returns references into scratch storage or leaks memory even if its positive tests pass.

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

> Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Scoped Visitors**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
