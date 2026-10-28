# Laboratory 15 — Boxed Expression Tree

This is the independent product for **Course 2, Module 15: Box, Deref, Dynamically Sized Types, and Cow**. Read the [module chapter](../../course-book/module-15-box-deref-dynamically-sized-types-and-cow/index.md) and complete its [workbook](../../course-book/module-15-box-deref-dynamically-sized-types-and-cow/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product


Build a typed arithmetic expression tree with minimal recursive indirection.

```text
labs/module-05-boxed-expressions/
├── starter/
└── solution/
```

### Required model

```rust
pub enum Expr {
    Number(i64),
    Neg(Box<Expr>),
    Add(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
}
```

Implement:

- constructors that hide box placement;
- checked evaluation returning an error on overflow;
- node count and maximum depth by borrowing;
- infix rendering with unambiguous parentheses;
- constant folding that consumes the tree and reuses ownership where possible;
- iterative evaluation or depth validation for adversarial trees;
- no deep clone in any read-only traversal.

### Required reasoning

- why direct recursion is unsized;
- allocation count for each constructor;
- why `Box` is exclusive ownership, not graph sharing;
- why moving the box is not equivalent to pinning;
- whether deriving `Clone` belongs in the public API.

### Acceptance

```bash
cargo test -p rust-olm-lab-05-boxed-expressions --all-targets
cargo clippy -p rust-olm-lab-05-boxed-expressions --all-targets -- -D warnings
```

### Construction and observation contract

The public constructors must make the recursive representation an implementation detail. A caller should write `Expr::add(left, right)`, not repeat `Box::new` throughout application code. This matters because indirection placement is part of the representation strategy, not part of arithmetic semantics. Keep the fields private if you use structs around variants, or document clearly that exposing enum variants also exposes representation choices.

Evaluation must use checked arithmetic. Define an error that identifies the operation that overflowed; returning only `None` loses the distinction between addition, multiplication, and negation. Traversals such as `node_count`, `depth`, and rendering take `&self`. A read-only traversal that clones subtrees fails the ownership review even when tests pass.

Constant folding is the ownership exercise. It consumes `self`, recursively folds children, and replaces an operation with `Number` only when both folded children are constants and checked evaluation succeeds. When a branch cannot collapse, reconstruct it from the already-owned folded children. Do not clone the original tree merely to retain a fallback.

### Adversarial cases
Add tests for a one-node tree, left- and right-skewed trees, nested negation, all three overflow routes, rendering precedence, and folding that partially simplifies without changing meaning. Include a generated tree near your chosen depth limit. State whether the limit prevents stack exhaustion during construction, validation, evaluation, or all three; those are different claims.

Your design note includes an allocation sketch for at least three expressions. Count boxes, not abstract syntax nodes. Explain which value owns every allocation after construction, during a consuming fold, and after the folded result is returned.

### Review questions
The lab is complete only when you can answer why `Box<Expr>` makes the enum sized, why `Box<[Expr]>` would encode a different arity model, and why neither heap allocation nor a stable box handle creates a pinning guarantee.

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

> When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Boxed Expression Tree**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
