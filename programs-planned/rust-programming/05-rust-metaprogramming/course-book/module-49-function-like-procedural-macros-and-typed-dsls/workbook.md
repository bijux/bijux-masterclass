# Workbook — Module 49: Function-Like Procedural Macros and Typed DSLs

[Chapter](index.md) · [Laboratory](../../labs/module-09-route-table-dsl/README.md) · [CommandForge guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Function-Like Procedural Macros and Typed DSLs** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?* Preserve your first prediction and record decisive facts in a **DSL syntax-to-model map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 48 — Attribute Macros and Item Transformation that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?**
3. Draw the smallest **DSL syntax-to-model map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

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

### Interleaved reasoning pass

1. For **Design a bounded custom grammar with explicit compatibility space**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the DSL syntax-to-model map.
2. For **Implement `syn::parse::Parse` for syntax nodes rather than splitting strings**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the DSL syntax-to-model map.
3. For **Separate syntax AST, semantic validation, normalized model, and generation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the DSL syntax-to-model map.
4. For **Detect duplicates and cross-entry conflicts with useful multi-span errors**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the DSL syntax-to-model map.

5. Identify one guarantee from an earlier course that a careless implementation of **Function-Like Procedural Macros and Typed DSLs** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

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

### Laboratory acceptance trace

Before opening the reference implementation for **Route Table DSL**, record:

- the public behavior that demonstrates **Design a bounded custom grammar with explicit compatibility space**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement `command_catalog!` with explicit table and lookup declarations, semicolon-terminated entries, duplicate-name rejection, deterministic source order, parsed handler metadata paths, and generation of exactly the named table and lookup function.

The capstone increment must leave a visible design record: one diagram or table, one positive test, one negative test, and one statement of what this mechanism deliberately does **not** own.

### Capstone invariant trace

For the Module 49 CommandForge increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

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

### Closed-book defense

In five minutes, answer “How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?” using the **DSL syntax-to-model map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside CommandForge. A list of APIs without the deciding relationship is incomplete.
