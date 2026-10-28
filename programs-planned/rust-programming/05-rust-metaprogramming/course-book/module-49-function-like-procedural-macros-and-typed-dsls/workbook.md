# Workbook — Module 49: Function-Like Procedural Macros and Typed DSLs

[Return to the chapter](index.md) · [Open the CommandForge engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Function-Like Procedural Macros and Typed DSLs** as an engineering mechanism rather than repeat its syntax. The governing question is:

> How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?

Follow the complete DSL pipeline: token grammar, syntax AST, semantic validation, normalized model, generated Rust, then ordinary type checking. A prediction must identify the earliest stage that owns duplicates, unsupported values, unresolved handler paths, and type mismatches.

## Part 1 — Predict

For each specimen about **DSL phase separation and normalization**, record the expected outcome, the first decisive source shape, the earliest phase that knows the fact, the smallest repair preserving the requirement, and one tempting change that would obtain a pass by weakening this module’s public contract.

| # | Specimen | Your committed prediction |
|---:|---|---|
| 1 | [`main.rs`](../../compiler-labs/module-09/case-01/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 2 | [`main.rs`](../../compiler-labs/module-09/case-02/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 3 | [`main.rs`](../../compiler-labs/module-09/case-03/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 4 | [`main.rs`](../../compiler-labs/module-09/case-04/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 5 | [`main.rs`](../../compiler-labs/module-09/case-05/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 6 | [`main.rs`](../../compiler-labs/module-09/case-06/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 7 | [`main.rs`](../../compiler-labs/module-09/case-07/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 8 | [`main.rs`](../../compiler-labs/module-09/case-08/src/main.rs) | Pass or fail? Name the exact phase and rule. |

Run this course’s cases from the program root with:

```bash
python3 tools/run_compiler_labs.py 05-rust-metaprogramming
```

Do not accept “the macro failed” as an explanation. Distinguish matcher failure, parser failure, semantic validation, expansion, name resolution, type checking, build-script validation, and runtime behavior.

## Part 2 — Diagnose and repair

A route DSL is parsed and emitted in one loop. Duplicate names overwrite earlier entries in a hash map, entry order depends on hashing, type paths are stored as strings, missing terminators are accepted accidentally, and generated code reports later errors far from the declaration.

### Repair sequence

1. Write the grammar and parse it into an AST that preserves source spans for every declaration.
2. Validate syntax-independent rules over the AST: duplicate names, duplicate routes, unsupported methods, empty literals, and incompatible options.
3. Normalize only after successful validation. Choose deterministic order deliberately—source order or sorted order—and state it as contract.
4. Generate compact ordinary Rust from the normalized model. Keep type and handler paths as parsed Rust syntax, not strings.
5. Attach semantic errors to the later conflicting entry while mentioning the original declaration where practical. Add malformed-input and deterministic-expansion tests.

### Required proof

Produce three artifacts:

- a DSL phase separation and normalization record that names the authority and the generated or checked surface;
- the smallest invocation, item, or build input that reproduces the original defect;
- a positive or negative test that would fail if the superficial repair replaced the principled one.

Your repair is incomplete if it merely changes token spelling. Explain how the accepted language, generated surface, evaluation semantics, names, errors, and compatibility obligations changed.

## Part 3 — Focused exercises

### Exercise 1 — Five-stage trace

Trace `routes! { GET "/users" => list; }` through tokens, AST, validation, normalized model, and emitted Rust.

### Exercise 2 — Parser/validator split

Why should duplicate-route detection not be embedded in the parser’s token-consumption logic?

### Exercise 3 — Terminator contract

Should every catalog entry require `;`? Evaluate permissive optional terminators against future evolution.

### Exercise 4 — Duplicate diagnostics

How do you report duplicate command names while preserving useful spans?

### Exercise 5 — Determinism

Compare source-order generation with lexicographically sorted generation. Which should a command catalog use?

### Exercise 6 — Type-checker boundary

The DSL references `Args` and `handler`. Which rules belong to DSL validation and which belong to Rust?

For every answer that proposes a macro, add a one-sentence rejection criterion: what simpler condition would make ordinary Rust preferable?

## Part 4 — Independent laboratory

### Product: Route Table DSL

Open [`labs/module-09-route-table-dsl/README.md`](../../labs/module-09-route-table-dsl/README.md) only after completing the prediction table. The starter is intentionally a valid baseline, not a half-written answer.

Before implementation, complete this module-specific design record:

| Decision | Your answer |
|---|---|
| surface grammar | |
| syntax AST | |
| cross-entry semantic state | |
| normalization rules | |
| duplicate identity | |
| deterministic ordering | |
| generated declarations | |
| ordinary-Rust obligations after expansion | |

Build the smallest valid **DSL phase separation and normalization** surface first. Add one accepted case, one rejection owned by this mechanism, and one case that expands successfully before ordinary Rust rejects a later obligation. Compare with the reference only after those three phase boundaries are protected by tests.

## Part 5 — Capstone transfer

Implement `command_catalog!` with explicit table and lookup declarations, semicolon-terminated entries, duplicate-name rejection, deterministic source order, parsed handler metadata paths, and generation of exactly the named table and lookup function.

The capstone increment must leave a visible design record: one diagram or table, one positive test, one negative test, and one statement of what this mechanism deliberately does **not** own.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. Why must parsing and semantic validation be distinct?
2. Which DSL rules require cross-entry state?
3. What ordering guarantee does the generated catalog provide?
4. Which relationships should generated Rust ask the type checker to prove?

Then perform a ten-minute reconstruction: recreate the smallest useful example for this module from an empty file, including one rejected input. If reconstruction requires copying the chapter, return to the mental model before continuing.

### Completion standard

Use the chapter’s readiness statement as the threshold:

Continue when you can show:

- a written grammar;
- syntax AST types;
- semantic invariants;
- a normalized model;
- multi-span relationship diagnostics;
- deterministic order policy;
- compact generated Rust;
- a compatibility plan;
- a reason the language belongs at compile time.

Do not continue if parsing, validation, and generation occur in one function or if the DSL accepts arbitrary tokens that it ignores.

Before advancing, defend these module-specific points:

- why a single parse-and-emit function is difficult to review
- which rules require cross-entry state
- which relationships should be delegated to the type checker
- what size or volatility would make a data file preferable
