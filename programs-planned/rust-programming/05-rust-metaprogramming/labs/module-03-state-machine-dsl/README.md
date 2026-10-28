# Laboratory 43 — State Machine DSL

This is the independent product for **Course 5, Module 43: Recursive Macro Parsing and Token-Tree Techniques**. Read the [module chapter](../../course-book/module-43-recursive-macro-parsing-and-token-tree-techniques/index.md) and complete its [workbook](../../course-book/module-43-recursive-macro-parsing-and-token-tree-techniques/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How can a declarative macro process a nontrivial token language with explicit parser state, guaranteed progress, and bounded complexity?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a bounded declarative state-machine language:

```rust
state_machine! {
    pub enum Publication {
        states [Draft, Review, Published];
        transitions {
            Draft => Review;
            Review => Draft;
            Review => Published;
        }
    }
}
```

The generated enum is ordinary Rust. `can_transition` is generated through a recursive internal rule that consumes one transition per step. This is intentionally a small token-tree parser: the exercise ends before duplicate detection or arbitrary semantic analysis turns it into a poor procedural macro.

## Required behavior

- Generate the enum with derives suitable for equality and debugging.
- Preserve state declaration order.
- Generate `can_transition(self, next) -> bool`.
- Recursive helper rules must have an explicit terminal case and consume one transition per call.
- A malformed top-level shape receives a targeted compile error.
- No runtime strings represent states.

## Adversarial cases

Test every legal edge, several illegal edges, reflexive transitions, and a terminal state. Add a compile-fail case for a missing `=>` and another for a missing semicolon. Explain why duplicate-state validation is outside this lab’s declarative boundary.

## Build sequence

Write the grammar, implement the public matcher, implement the terminal helper, then the one-transition recursive helper. Inspect the expansion mentally before adding features.

## Transfer

Add an optional `initial State;` declaration and generate `Default`. Keep it token-local; reject a proposal to verify graph reachability inside `macro_rules!`.

## Grammar and termination proof

Write the accepted grammar before adding recursive rules. Separate the public entry rule from internal parser states such as “collecting states,” “checking one transition,” and “emitting output.” Every recursive invocation must consume at least one token-tree unit or move to a terminal emission rule.

Use negative cases for an undeclared source state, an undeclared target state, a missing semicolon, and a malformed state list. Distinguish errors your macro can diagnose locally from errors intentionally delegated to Rust. A duplicate enum variant, for example, may be left to ordinary Rust if adding reliable duplicate detection would turn a bounded teaching grammar into an opaque token algorithm.

Finally, trace one valid transition from invocation tokens through the accumulator to the emitted `match`. The trace must identify the current parser state and the remaining input after each recursive step.

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

> How can a declarative macro process a nontrivial token language with explicit parser state, guaranteed progress, and bounded complexity?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **State Machine DSL**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
