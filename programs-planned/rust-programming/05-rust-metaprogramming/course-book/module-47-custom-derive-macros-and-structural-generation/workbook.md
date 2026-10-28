# Workbook — Module 47: Custom Derive Macros and Structural Generation

[Chapter](index.md) · [Laboratory](../../labs/module-07-field-names-derive/README.md) · [CommandForge guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Custom Derive Macros and Structural Generation** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you inspect a Rust item, preserve its generics and constraints, and generate a lawful implementation without pretending to perform type checking?* Preserve your first prediction and record decisive facts in a **derive expansion ledger**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 46 — Procedural Macro Execution and TokenStream Engineering that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you inspect a Rust item, preserve its generics and constraints, and generate a lawful implementation without pretending to perform type checking?**
3. Draw the smallest **derive expansion ledger** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen about **derive structure and generic preservation**, record the expected outcome, the first decisive source shape, the earliest phase that knows the fact, the smallest repair preserving the requirement, and one tempting change that would obtain a pass by weakening this module’s public contract.

| # | Specimen | Your committed prediction |
|---:|---|---|
| 1 | [`main.rs`](../../compiler-labs/module-07/case-01/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 2 | [`main.rs`](../../compiler-labs/module-07/case-02/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 3 | [`main.rs`](../../compiler-labs/module-07/case-03/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 4 | [`main.rs`](../../compiler-labs/module-07/case-04/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 5 | [`main.rs`](../../compiler-labs/module-07/case-05/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 6 | [`main.rs`](../../compiler-labs/module-07/case-06/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 7 | [`main.rs`](../../compiler-labs/module-07/case-07/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 8 | [`main.rs`](../../compiler-labs/module-07/case-08/src/main.rs) | Pass or fail? Name the exact phase and rule. |

Run this course’s cases from the program root with:

```bash
python3 tools/run_compiler_labs.py 05-rust-metaprogramming
```

Do not accept “the macro failed” as an explanation. Distinguish matcher failure, parser failure, semantic validation, expansion, name resolution, type checking, build-script validation, and runtime behavior.

## Part 2 — Diagnose and repair

A derive extracts the first identifier from token text, supports only nongeneric named structs, assumes every field implements `Display`, ignores existing where clauses, silently treats tuple structs as empty, and panics on unions. Generated code compiles only for the demonstration type.

### Repair sequence

1. Parse the complete `DeriveInput` and classify struct, enum, and union forms explicitly.
2. Define the supported input set. Reject unsupported forms with a diagnostic at the relevant item or field rather than producing meaningless output.
3. Use `split_for_impl()` and preserve every generic parameter and existing where predicate. Add bounds only for fields that generated behavior actually uses.
4. Parse helper attributes through one documented grammar, reject unknown keys and duplicates, and attach errors to the offending metadata.
5. Generate the smallest implementation. Let Rust name resolution and trait checking establish semantic facts the derive cannot know from syntax alone.

### Required proof

Produce three artifacts:

- a derive structure and generic preservation record that names the authority and the generated or checked surface;
- the smallest invocation, item, or build input that reproduces the original defect;
- a positive or negative test that would fail if the superficial repair replaced the principled one.

Your repair is incomplete if it merely changes token spelling. Explain how the accepted language, generated surface, evaluation semantics, names, errors, and compatibility obligations changed.

## Part 3 — Focused exercises

### Exercise 1 — Generic preservation

Given `struct Pair<T, const N: usize> where T: Clone { values: [T; N] }`, sketch the implementation header a derive must generate.

### Exercise 2 — Minimal bounds

A derive generates field names only. Should it add `T: Display`, `T: Debug`, or `T: FieldNames` for generic fields?

### Exercise 3 — Input support table

Define behavior for named structs, tuple structs, unit structs, enums, and unions for a `FieldNames` derive.

### Exercise 4 — Attribute grammar

Design `#[field_names(skip)]` and `#[field_names(rename = "external")]`. What combinations are invalid?

### Exercise 5 — Syntax versus semantics

Can a derive prove that a path written as `Option<T>` resolves to `std::option::Option`?

### Exercise 6 — Union rejection

Why should unsupported union input produce `syn::Error` rather than panic or an empty implementation?

For every answer that proposes a macro, add a one-sentence rejection criterion: what simpler condition would make ordinary Rust preferable?

### Interleaved reasoning pass

1. For **Parse `DeriveInput` and distinguish structs, enums, and unions**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the derive expansion ledger.
2. For **Support only documented item shapes and reject others at useful spans**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the derive expansion ledger.
3. For **Inspect named, unnamed, and unit fields without losing source order**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the derive expansion ledger.
4. For **Parse derive helper attributes and reject unknown or duplicate options**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the derive expansion ledger.

5. Identify one guarantee from an earlier course that a careless implementation of **Custom Derive Macros and Structural Generation** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

### Product: Field Names Derive

Open [`labs/module-07-field-names-derive/README.md`](../../labs/module-07-field-names-derive/README.md) only after completing the prediction table. The starter is intentionally a valid baseline, not a half-written answer.

Before implementation, complete this module-specific design record:

| Decision | Your answer |
|---|---|
| supported item shapes | |
| generic preservation | |
| where-clause preservation | |
| field-policy grammar | |
| duplicate and conflict rules | |
| generated associated items | |
| invented-bound audit | |
| combined-error strategy | |

Build the smallest valid **derive structure and generic preservation** surface first. Add one accepted case, one rejection owned by this mechanism, and one case that expands successfully before ordinary Rust rejects a later obligation. Compare with the reference only after those three phase boundaries are protected by tests.

### Laboratory acceptance trace

Before opening the reference implementation for **Field Names Derive**, record:

- the public behavior that demonstrates **Parse `DeriveInput` and distinguish structs, enums, and unions**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement `CommandArgs` derive for named structs. Preserve generics, parse field helper attributes, distinguish required fields from syntactic `Option<T>`, generate deterministic usage, and let `FromStr` bounds be checked by Rust.

The capstone increment must leave a visible design record: one diagram or table, one positive test, one negative test, and one statement of what this mechanism deliberately does **not** own.

### Capstone invariant trace

For the Module 47 CommandForge increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. Which facts can a derive learn from syntax and which remain type-system facts?
2. How do you preserve generic declarations correctly?
3. When is adding a generated trait bound justified?
4. Why is rejecting unsupported input better than inventing semantics?

Then perform a ten-minute reconstruction: recreate the smallest useful example for this module from an empty file, including one rejected input. If reconstruction requires copying the chapter, return to the mental model before continuing.

### Completion standard

Use the chapter’s readiness statement as the threshold:

Continue when you can state:

- exactly which item shapes the derive accepts;
- what structural facts it can know;
- which semantic facts remain for type checking;
- how helper attributes are parsed and validated;
- how generics and `where` clauses survive;
- which bounds are generated and why;
- which runtime path the expansion assumes;
- how unsupported input is diagnosed.

Do not continue if the derive drops generics, ignores unknown attributes, or recognizes types by spelling while claiming semantic certainty.

Before advancing, defend these module-specific points:

- why derive inspects syntax rather than resolved field semantics
- how `split_for_impl` preserves the source declaration
- why skipped fields must not acquire bounds
- which helper-attribute change would be breaking

### Closed-book defense

In five minutes, answer “How do you inspect a Rust item, preserve its generics and constraints, and generate a lawful implementation without pretending to perform type checking?” using the **derive expansion ledger**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside CommandForge. A list of APIs without the deciding relationship is incomplete.
