# Laboratory 46 — TokenStream Inspector

**Course 5 · Module 46: Procedural Macro Execution and TokenStream Engineering**

[Chapter](../../course-book/module-46-procedural-macro-execution-and-tokenstream-engineering/index.md) · [Workbook](../../course-book/module-46-procedural-macro-execution-and-tokenstream-engineering/workbook.md) · [CommandForge guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Procedural Macro Execution and TokenStream Engineering**: What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled? The product must make **Explain when and how a procedural macro executes** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **token-stream phase map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Implement a function-like procedural macro that turns its input token stream into a deterministic textual description of token-tree structure:

```rust
const SHAPE: &str = token_tree_shape!(alpha + (beta * 3));
```

The output should distinguish identifiers, literals, punctuation with spacing, and nested delimiter groups. The goal is to replace the misleading “procedural macros receive source strings” model with direct observation of structured tokens.

## Required behavior

- Use only the compiler-provided `proc_macro` API.
- Walk nested `TokenTree` values recursively.
- Record delimiter kind for groups.
- Record punctuation character and spacing.
- Emit one string literal expression.
- Produce deterministic output and no compile-time printing.
- Preserve unusual but valid token shapes such as raw identifiers and joint punctuation.

## Adversarial cases

Inspect an empty stream, nested groups, `::`, `=>`, a negative numeric expression, a string literal containing spaces, and a raw identifier. Explain why `-7` is not necessarily one negative-number token and why `input.to_string().split_whitespace()` is not a parser.

## Build sequence

The starter already proves the proc-macro crate boundary. Replace its constant output with a recursive token-tree formatter. Keep formatting isolated from the macro entry point.

## Transfer

Add a second macro that returns the top-level token count. State why this remains an observation tool rather than a semantic Rust analyzer.

## Observation discipline

The inspector describes token trees; it does not reconstruct source text or infer Rust types. Verify the distinction with `-5`, `a::b`, lifetimes, joint punctuation, nested delimiters, and a literal containing escaped characters. Record where punctuation spacing affects the description.

Run the same invocation twice and compare the emitted string byte-for-byte. The result must depend only on the supplied token stream, not on filesystem state, time, environment variables, or hash-map iteration. Preserve group nesting explicitly so `(a + b)` cannot be confused with a flat token sequence.

The final explanation must identify what information is unavailable: comments and most whitespace are not ordinary token-tree content, and semantic facts such as inferred types do not exist at this stage.

## Working route

1. Read the product contract and run the starter’s baseline checks for **TokenStream Inspector**.
2. Draw the smallest **token-stream phase map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to CommandForge so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 46 — TokenStream Inspector**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **TokenStream Inspector**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Explain when and how a procedural macro executes.
- Distinguish `TokenStream`, `TokenTree`, `Group`, `Ident`, `Punct`, `Literal`, and `Span`.
- Avoid treating token text as a fully resolved Rust AST.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 46 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **token-stream phase map**. Defend why your design is simpler than one plausible alternative under the new requirements.
