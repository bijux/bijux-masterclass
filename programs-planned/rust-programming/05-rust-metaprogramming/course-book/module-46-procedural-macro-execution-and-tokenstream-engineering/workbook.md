# Workbook — Module 46: Procedural Macro Execution and TokenStream Engineering

[Return to the chapter](index.md) · [Open the CommandForge engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Procedural Macro Execution and TokenStream Engineering** as an engineering mechanism rather than repeat its syntax. The governing question is:

> What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?

Describe the input as token trees—groups, delimiters, identifiers, literals, and punctuation spacing—before assigning Rust meaning. Separate what the procedural macro can inspect syntactically from what later name resolution and type checking establish.

## Part 1 — Predict

For each specimen about **token-stream structure and spans**, record the expected outcome, the first decisive source shape, the earliest phase that knows the fact, the smallest repair preserving the requirement, and one tempting change that would obtain a pass by weakening this module’s public contract.

| # | Specimen | Your committed prediction |
|---:|---|---|
| 1 | [`main.rs`](../../compiler-labs/module-06/case-01/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 2 | [`main.rs`](../../compiler-labs/module-06/case-02/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 3 | [`main.rs`](../../compiler-labs/module-06/case-03/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 4 | [`main.rs`](../../compiler-labs/module-06/case-04/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 5 | [`main.rs`](../../compiler-labs/module-06/case-05/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 6 | [`main.rs`](../../compiler-labs/module-06/case-06/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 7 | [`main.rs`](../../compiler-labs/module-06/case-07/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 8 | [`main.rs`](../../compiler-labs/module-06/case-08/src/main.rs) | Pass or fail? Name the exact phase and rule. |

Run this course’s cases from the program root with:

```bash
python3 tools/run_compiler_labs.py 05-rust-metaprogramming
```

Do not accept “the macro failed” as an explanation. Distinguish matcher failure, parser failure, semantic validation, expansion, name resolution, type checking, build-script validation, and runtime behavior.

## Part 2 — Diagnose and repair

A procedural macro converts its input to a string, splits on spaces, reads the current directory, prints debugging output, panics on malformed syntax, and emits unqualified names. It passes one example but breaks on punctuation spacing, raw identifiers, nested groups, cross-compilation, and shadowed imports.

### Repair sequence

1. Treat `TokenStream` as structured tokens with groups, identifiers, punctuation, literals, and spans. Do not use source-text splitting as a Rust parser.
2. Keep the macro entry point thin: parse into an explicit representation, validate, generate tokens, and convert accumulated errors to compiler output.
3. Use spans from the offending input token for diagnostics and generated identifiers derived from user syntax. Use stable call-site spans only for genuinely generated support tokens.
4. Avoid file and environment effects unless the mechanism explicitly owns them. Procedural macros run during compilation and carry build-script-like security concerns.
5. Generate absolute or runtime-crate-qualified paths, deterministic item order, and no debug output. Return `compile_error!`-equivalent errors rather than panicking for user mistakes.

### Required proof

Produce three artifacts:

- a token-stream structure and spans record that names the authority and the generated or checked surface;
- the smallest invocation, item, or build input that reproduces the original defect;
- a positive or negative test that would fail if the superficial repair replaced the principled one.

Your repair is incomplete if it merely changes token spelling. Explain how the accepted language, generated surface, evaluation semantics, names, errors, and compatibility obligations changed.

## Part 3 — Focused exercises

### Exercise 1 — Token structure

Classify the tokens in `route!(GET "/users/{id}" => handlers::show::<User>)`, including nested path punctuation and the literal.

### Exercise 2 — Cheap clone meaning

The Reference describes `TokenStream` as cheap to clone. Why does that not justify repeatedly reparsing or duplicating semantic work?

### Exercise 3 — Span policy

Choose spans for an unknown attribute key, a generated implementation block, and a generated identifier derived from a field.

### Exercise 4 — Error accumulation

When should a derive report several field-attribute errors at once instead of returning after the first?

### Exercise 5 — Security boundary

Explain why a procedural macro dependency deserves trust similar to a build-script dependency.

### Exercise 6 — Deterministic expansion

Name four sources of nondeterministic generated output and repair each.

For every answer that proposes a macro, add a one-sentence rejection criterion: what simpler condition would make ordinary Rust preferable?

## Part 4 — Independent laboratory

### Product: TokenStream Inspector

Open [`labs/module-06-token-stream-inspector/README.md`](../../labs/module-06-token-stream-inspector/README.md) only after completing the prediction table. The starter is intentionally a valid baseline, not a half-written answer.

Before implementation, complete this module-specific design record:

| Decision | Your answer |
|---|---|
| raw token input | |
| group and delimiter structure | |
| punctuation spacing | |
| span observations | |
| normalized inspection output | |
| deterministic ordering | |
| unsupported semantic claims | |
| failure behavior | |

Build the smallest valid **token-stream structure and spans** surface first. Add one accepted case, one rejection owned by this mechanism, and one case that expands successfully before ordinary Rust rejects a later obligation. Compare with the reference only after those three phase boundaries are protected by tests.

## Part 5 — Capstone transfer

Create the `commandforge-macros` crate and a four-phase internal structure: parse, validate, normalize, generate. Pin the minimal proc-macro dependencies and ensure user mistakes become spanned compile errors rather than panics.

The capstone increment must leave a visible design record: one diagram or table, one positive test, one negative test, and one statement of what this mechanism deliberately does **not** own.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. Why is token text not a Rust AST?
2. What security rights does a procedural macro execute with?
3. How should spans be chosen for generated code?
4. Which effects would make expansion non-reproducible?

Then perform a ten-minute reconstruction: recreate the smallest useful example for this module from an empty file, including one rejected input. If reconstruction requires copying the chapter, return to the mental model before continuing.

### Completion standard

Use the chapter’s readiness statement as the threshold:

Continue when you can explain:

- when the macro executes;
- what token structure it receives;
- what spans can and cannot establish;
- why token text is not a resolved AST;
- where syntax parsing ends and semantic validation begins;
- why invalid input should not panic;
- how deterministic output is established;
- what build-time security and cost the dependency introduces.

Do not continue if your proc macro is one large function converting the input to a string, splitting it, and parsing generated source text back into tokens.

Before advancing, defend these module-specific points:

- what a procedural macro knows before type checking
- why stringifying and reparsing tokens is fragile
- which span is used for each emitted error
- which effects would make expansion non-reproducible
