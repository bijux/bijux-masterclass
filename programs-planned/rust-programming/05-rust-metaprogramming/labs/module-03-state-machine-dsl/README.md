# Laboratory 43 — State Machine DSL

**Course 5 · Module 43: Recursive Macro Parsing and Token-Tree Techniques**

[Chapter](../../course-book/module-43-recursive-macro-parsing-and-token-tree-techniques/index.md) · [Workbook](../../course-book/module-43-recursive-macro-parsing-and-token-tree-techniques/workbook.md) · [CommandForge guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Recursive Macro Parsing and Token-Tree Techniques**: How can a declarative macro process a nontrivial token language with explicit parser state, guaranteed progress, and bounded complexity? The product must make **Model recursive macro rules as parser states and transitions** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **recursive grammar state** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

1. Read the product contract and run the starter’s baseline checks for **State Machine DSL**.
2. Draw the smallest **recursive grammar state** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to CommandForge so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 43 — State Machine DSL**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **State Machine DSL**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Model recursive macro rules as parser states and transitions.
- Prove that each recursive step consumes input or reaches a base case.
- Use internal arms and accumulators without exposing implementation syntax.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 43 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **recursive grammar state**. Defend why your design is simpler than one plausible alternative under the new requirements.
