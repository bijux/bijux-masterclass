# Laboratory 46 — TokenStream Inspector

This is the independent product for **Course 5, Module 46: Procedural Macro Execution and TokenStream Engineering**. Read the [module chapter](../../course-book/module-46-procedural-macro-execution-and-tokenstream-engineering/index.md) and complete its [workbook](../../course-book/module-46-procedural-macro-execution-and-tokenstream-engineering/workbook.md) before consulting the reference implementation.

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

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **TokenStream Inspector**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
