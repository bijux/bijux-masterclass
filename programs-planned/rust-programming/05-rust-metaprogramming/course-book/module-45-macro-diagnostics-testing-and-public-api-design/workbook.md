# Workbook — Module 45: Macro Diagnostics, Testing, and Public API Design

[Return to the chapter](index.md) · [Open the CommandForge engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Macro Diagnostics, Testing, and Public API Design** as an engineering mechanism rather than repeat its syntax. The governing question is:

> How do you prove that a macro accepts the intended language, rejects misuse for the intended reason, and remains an evolvable public API?

Classify every case as invocation-grammar rejection, explicit macro semantic rejection, generated-name or type failure, or runtime failure. Record where the primary diagnostic should point and which secondary compiler messages are merely consequences.

## Part 1 — Predict

For each specimen about **diagnostic causality and compatibility**, record the expected outcome, the first decisive source shape, the earliest phase that knows the fact, the smallest repair preserving the requirement, and one tempting change that would obtain a pass by weakening this module’s public contract.

| # | Specimen | Your committed prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-05/case-01.rs) | Pass or fail? Name the exact phase and rule. |
| 2 | [`case-02.rs`](../../compiler-labs/module-05/case-02.rs) | Pass or fail? Name the exact phase and rule. |
| 3 | [`case-03.rs`](../../compiler-labs/module-05/case-03.rs) | Pass or fail? Name the exact phase and rule. |
| 4 | [`case-04.rs`](../../compiler-labs/module-05/case-04.rs) | Pass or fail? Name the exact phase and rule. |
| 5 | [`case-05.rs`](../../compiler-labs/module-05/case-05.rs) | Pass or fail? Name the exact phase and rule. |
| 6 | [`case-06.rs`](../../compiler-labs/module-05/case-06.rs) | Pass or fail? Name the exact phase and rule. |
| 7 | [`case-07.rs`](../../compiler-labs/module-05/case-07.rs) | Pass or fail? Name the exact phase and rule. |
| 8 | [`case-08.rs`](../../compiler-labs/module-05/case-08.rs) | Pass or fail? Name the exact phase and rule. |

Run this course’s cases from the program root with:

```bash
python3 tools/run_compiler_labs.py 05-rust-metaprogramming
```

Do not accept “the macro failed” as an explanation. Distinguish matcher failure, parser failure, semantic validation, expansion, name resolution, type checking, build-script validation, and runtime behavior.

## Part 2 — Diagnose and repair

A public macro has only happy-path unit tests. Any malformed invocation falls through to a generic matcher error. A refactor silently changes evaluation order and accepts a previously rejected shorthand. The package calls the release compatible because the generated runtime output still matches one snapshot.

### Repair sequence

1. Write the accepted grammar and the intentionally rejected near-misses as part of the public contract.
2. Create positive tests for representative valid forms, expansion-behavior tests for evaluation count and order, and negative compiler fixtures for each important misuse.
3. Use targeted fallback rules or span-aware procedural errors. Test the intended cause, not merely nonzero compiler status.
4. Treat newly accepted syntax, changed expansion paths, generated item names, evaluation changes, and diagnostic movement as compatibility-relevant decisions.
5. Prefer semantic assertions over one giant token snapshot. Snapshot only small normalized surfaces whose exact shape is itself the contract.

### Required proof

Produce three artifacts:

- a diagnostic causality and compatibility record that names the authority and the generated or checked surface;
- the smallest invocation, item, or build input that reproduces the original defect;
- a positive or negative test that would fail if the superficial repair replaced the principled one.

Your repair is incomplete if it merely changes token spelling. Explain how the accepted language, generated surface, evaluation semantics, names, errors, and compatibility obligations changed.

## Part 3 — Focused exercises

### Exercise 1 — Test matrix

Design a four-quadrant test matrix for a macro: valid syntax/valid semantics, valid syntax/type error, invalid syntax, and valid expansion/wrong runtime semantics.

### Exercise 2 — Diagnostic ownership

Where should duplicate route literals be rejected: parser, semantic validator, generated runtime table, or runtime dispatch?

### Exercise 3 — Weak negative test

Why is “cargo check exits nonzero” insufficient for a compile-fail fixture?

### Exercise 4 — Compatibility surface

List five public-macro changes that can break downstream code even when the invocation text still parses.

### Exercise 5 — Fallback design

Write a targeted `macro_rules!` fallback for a missing numeric code in a diagnostic declaration and a final generic fallback. Explain why the specific rule comes first.

### Exercise 6 — Snapshot discipline

Choose which of these deserve exact snapshots: full `syn` debug AST, normalized route model, generated public constants, compiler prose, deterministic help table.

For every answer that proposes a macro, add a one-sentence rejection criterion: what simpler condition would make ordinary Rust preferable?

## Part 4 — Independent laboratory

### Product: Diagnostic Enum Macro

Open [`labs/module-05-diagnostic-enum-macro/README.md`](../../labs/module-05-diagnostic-enum-macro/README.md) only after completing the prediction table. The starter is intentionally a valid baseline, not a half-written answer.

Before implementation, complete this module-specific design record:

| Decision | Your answer |
|---|---|
| accepted language | |
| invalid syntax cases | |
| semantic invalidity cases | |
| diagnostic wording | |
| diagnostic span | |
| generated API | |
| compatibility-sensitive names | |
| negative-test matrix | |

Build the smallest valid **diagnostic causality and compatibility** surface first. Add one accepted case, one rejection owned by this mechanism, and one case that expands successfully before ordinary Rust rejects a later obligation. Compare with the reference only after those three phase boundaries are protected by tests.

## Part 5 — Capstone transfer

Specify CommandForge’s compile-pass, compile-fail, runtime, and deterministic-output matrix. Stable diagnostic codes and messages are generated by one declarative declaration; malformed catalog entries and handler signatures receive targeted compile-time errors.

The capstone increment must leave a visible design record: one diagram or table, one positive test, one negative test, and one statement of what this mechanism deliberately does **not** own.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What is the public API of a macro beyond its invocation grammar?
2. Why can accepting more syntax be a compatibility decision?
3. How do you prevent false-positive compile-fail tests?
4. Which generated details should remain intentionally unspecified?

Then perform a ten-minute reconstruction: recreate the smallest useful example for this module from an empty file, including one rejected input. If reconstruction requires copying the chapter, return to the mental model before continuing.

### Completion standard

Use the chapter’s readiness statement as the threshold:

Continue when you can provide evidence for:

- the complete accepted grammar;
- the generated public API;
- each important invalid form and its causal phase;
- runtime evaluation and ordering;
- downstream path behavior;
- compatibility constraints;
- the boundary between macro validation and generated type checking.

Do not continue if your test strategy is only “the crate builds” or if negative cases merely contain code that happens to be invalid.

Before advancing, defend these module-specific points:

- why compile failure alone is not sufficient negative evidence
- which errors the macro should emit directly
- which errors should remain ordinary Rust type errors
- how diagnostic and grammar changes affect versioning
