# Workbook — Module 15: Box, Deref, Dynamically Sized Types, and Cow

[Return to the chapter](index.md) · [Open the Memory Workspace engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Box, Deref, Dynamically Sized Types, and Cow** without relying on surface syntax. Keep the module question in view: *When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Box, Deref, Dynamically Sized Types, and Cow** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-direct-recursion.rs`](../../compiler-labs/module-05/01-direct-recursion.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-boxed-recursion.rs`](../../compiler-labs/module-05/02-boxed-recursion.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-move-out-of-unpinned-box.rs`](../../compiler-labs/module-05/03-move-out-of-unpinned-box.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-box-array-unsizes.rs`](../../compiler-labs/module-05/04-box-array-unsizes.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-question-sized.rs`](../../compiler-labs/module-05/05-question-sized.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-dst-field-not-last.rs`](../../compiler-labs/module-05/06-dst-field-not-last.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-invariant-breaking-derefmut.rs`](../../compiler-labs/module-05/07-invariant-breaking-derefmut.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-cow-borrowed-owned.rs`](../../compiler-labs/module-05/08-cow-borrowed-owned.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 02-rust-ownership-lifetimes-memory
```

## Part 2 — Diagnose and repair


A parser represents every string, number, vector, and node as `Box<...>`. Public methods accept `&Box<T>`, clones are used to traverse, and a `NonEmptyName` implements `DerefMut<Target = String>`.

### Problems

- allocations occur without structural need;
- APIs couple callers to one owner wrapper;
- deep clones replace borrowing;
- recursive indirection exists at every field rather than recursive edges;
- mutable dereferencing bypasses the non-empty invariant;
- boxed `Vec<T>` retains two levels of indirection without fixing length.

### Repair

- store scalar and ordinary owned fields inline;
- use `Box<Node>` only on recursive edges or measured cold variants;
- accept `&Node`/`&str`, not `&Box<Node>`/`&Box<str>`;
- traverse by borrowing;
- expose `NonEmptyName::as_str` and validated replacement methods;
- choose `Vec<T>` for growth or `Box<[T]>` for fixed ownership;
- document clone as a deep independent-copy operation if retained.

### Required analysis

Draw allocation topology before and after. Count allocations for a seven-node binary tree under both designs. Explain which changes are semantic and which are performance-motivated observations requiring later benchmarks.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:


1. Repair three infinitely sized recursive types by placing minimal indirection.
2. Compare `Box<Node>` children with one `Box<(Node, Node)>` and state allocation/traversal differences.
3. Refactor functions accepting `&Box<String>` to the weakest useful borrowed target.
4. Design a `NonEmpty` wrapper without `DerefMut`; preserve validation on replacement.
5. Write a `size_of_val` function over `T: ?Sized` and test sized, slice, and `str` referents.
6. Convert `Vec<T>` to `Box<[T]>`, prove length remains, and explain capacity semantics.
7. Implement a normalizer returning `Cow<'_, str>` with a truly allocation-free borrowed branch.
8. Audit a caller that immediately uses `into_owned`; decide whether `Cow` remains justified.
9. Build iterative and recursive evaluators for a boxed expression tree; consider depth failure.
10. Decide whether capstone immutable snapshots should use `String`, `Box<str>`, or `Rc<str>` before Module 16.



## Part 4 — Independent laboratory



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

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-05-boxed-expressions](../../labs/module-05-boxed-expressions/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

### Outcomes mapped

- Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership.
- Explain Deref, deref coercion, method lookup, and why custom Deref is not ordinary inheritance.
- Reason about sized and dynamically sized types, fat pointers, metadata, unsizing, boxed slices, and boxed strings.
- Use Cow only when the common path can borrow and a well-defined transformation sometimes requires ownership.
- Choose among inline ownership, Box, Rc, handles, arenas, and borrowed views from topology and cost.


Add immutable document snapshots.

A live `Document` stores editable `String` fields. `DocumentSnapshot` owns fixed text and title as `Box<str>`, plus handle and revision. Creating a snapshot performs an explicit copy because the snapshot must remain independent of future edits.

Do not expose `&Box<str>`; accessors return `&str`. Do not implement `Deref` for the snapshot itself because a document snapshot is not conceptually a string pointer.

Add a normalizer returning `Cow<'_, str>` for search queries. It must borrow an already normalized query and allocate only when case/whitespace normalization changes content. Tests must inspect the `Borrowed`/`Owned` variant rather than claim allocation behavior from timing.

The next module evaluates whether multiple consumers should share one snapshot through `Rc<DocumentSnapshot>` or receive independent copies.



### Capstone defense

Redesign an expression tree and text-normalization API, showing which allocations are necessary and which are conditional.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

- Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership.
- Explain Deref, deref coercion, method lookup, and why custom Deref is not ordinary inheritance.
- Reason about sized and dynamically sized types, fat pointers, metadata, unsizing, boxed slices, and boxed strings.
- Use Cow only when the common path can borrow and a well-defined transformation sometimes requires ownership.
- Choose among inline ownership, Box, Rc, handles, arenas, and borrowed views from topology and cost.

### Closed-book checkpoint

1. Explain why direct recursive ownership has no finite size.
2. Place `Box` at the minimal recursive edge for an unseen type.
3. Distinguish moving a box from moving its referent and from pinning.
4. Expand a dereference-coercion chain without claiming a clone.
5. Reject an invariant-breaking `DerefMut` implementation.
6. Explain why `str` and `[T]` are dynamically sized and how references remain sized.
7. Use `T: ?Sized` accurately.
8. Choose between `Vec<T>` and `Box<[T]>` by phase capability.
9. State when `Cow` actually avoids ownership allocation.
10. Defend every box in the lab/capstone through structural necessity.

### Transfer defense

Redesign an expression tree and text-normalization API, showing which allocations are necessary and which are conditional.

Your answer must include:

1. Why is a directly recursive enum infinitely sized?
2. How can `Vec<Node>` break recursion without `Box<Node>` per child?
3. What ownership does `Box<T>` express?
4. Does moving a box move/clone the pointee semantically?
5. What is a DST?
6. What metadata is conceptually associated with `&str`?
7. Why can `Box<dyn Trait>` be sized?
8. When is `Rc` justified in a tree?
9. Why is `Deref` inappropriate for many domain wrappers?
10. What does `Cow::to_mut` do for borrowed data?
11. When should `Cow` be replaced with ownership?
12. What capacity property does `Box<str>` express?
13. Does boxing imply pinning?
14. What cost does one box per node add?
15. What robustness issue remains for very deep recursion?

#### Answer notes

Indirection gives recursive owners a finite representation. `Vec` itself owns indirect storage. `Box` is one owner, not shared liveness or pinning. DST pointers carry metadata. `Rc` is justified by shared liveness/DAG semantics, not clone convenience. `Cow` clones only on required ownership/mutation but spreads a lifetime; own durable data. Deep recursive algorithms and destruction may overflow stacks despite memory safety.

#### Transfer task

Design a pattern AST that borrows source tokens, supports one plugin-owned matcher, and can be converted to a source-independent owned form. Compare allocation topologies for `Vec<Node>` arena versus boxes.
