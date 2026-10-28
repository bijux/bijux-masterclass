# Laboratory 13 — Scoped Visitors

**Course 2 · Module 13: Scoped Access and Escape Prevention**

[Chapter](../../course-book/module-13-scoped-access-and-escape-prevention/index.md) · [Workbook](../../course-book/module-13-scoped-access-and-escape-prevention/workbook.md) · [Memory Workspace guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Scoped Access and Escape Prevention**: Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable? The product must make **Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **scope and escape table** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

## Design record

Before implementation, complete this record for **Scoped Visitors**:

| Question | Required answer |
|---|---|
| Module decision | How does **Scoped Access and Escape Prevention** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **scope and escape table** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Scoped Visitors**.
2. Draw the smallest **scope and escape table** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Memory Workspace so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 13 — Scoped Visitors**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Scoped Visitors**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation.
- Read and design for<'a> higher-ranked callback bounds as universal quantification over borrow duration.
- Account for closure capture and Fn, FnMut, and FnOnce requirements at scoped boundaries.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 13 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **scope and escape table**. Defend why your design is simpler than one plausible alternative under the new requirements.
