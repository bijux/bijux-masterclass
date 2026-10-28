# Workbook — Module 42: Declarative Macros: Matchers, Fragments, and Repetition

[Chapter](index.md) · [Laboratory](../../labs/module-02-typed-map-macro/README.md) · [CommandForge guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Declarative Macros: Matchers, Fragments, and Repetition** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics?* Preserve your first prediction and record decisive facts in a **matcher and fragment trace**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 41 — Metaprogramming Boundaries and the Expansion Model that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics?**
3. Draw the smallest **matcher and fragment trace** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen about **matcher grammar and evaluation semantics**, record the expected outcome, the first decisive source shape, the earliest phase that knows the fact, the smallest repair preserving the requirement, and one tempting change that would obtain a pass by weakening this module’s public contract.

| # | Specimen | Your committed prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-02/case-01.rs) | Pass or fail? Name the exact phase and rule. |
| 2 | [`case-02.rs`](../../compiler-labs/module-02/case-02.rs) | Pass or fail? Name the exact phase and rule. |
| 3 | [`case-03.rs`](../../compiler-labs/module-02/case-03.rs) | Pass or fail? Name the exact phase and rule. |
| 4 | [`case-04.rs`](../../compiler-labs/module-02/case-04.rs) | Pass or fail? Name the exact phase and rule. |
| 5 | [`case-05.rs`](../../compiler-labs/module-02/case-05.rs) | Pass or fail? Name the exact phase and rule. |
| 6 | [`case-06.rs`](../../compiler-labs/module-02/case-06.rs) | Pass or fail? Name the exact phase and rule. |
| 7 | [`case-07.rs`](../../compiler-labs/module-02/case-07.rs) | Pass or fail? Name the exact phase and rule. |
| 8 | [`case-08.rs`](../../compiler-labs/module-02/case-08.rs) | Pass or fail? Name the exact phase and rule. |

Run this course’s cases from the program root with:

```bash
python3 tools/run_compiler_labs.py 05-rust-metaprogramming
```

Do not accept “the macro failed” as an explanation. Distinguish matcher failure, parser failure, semantic validation, expansion, name resolution, type checking, build-script validation, and runtime behavior.

## Part 2 — Diagnose and repair

A `map!` macro accepts arbitrary token trees, inserts them into a `HashMap`, evaluates keys twice to check duplicates, accepts both commas and semicolons through overlapping rules, and returns a sequence of statements rather than one block expression. The invocation looks convenient, but the accepted language is ambiguous and the expansion changes caller semantics.

### Repair sequence

1. Define one invocation grammar before writing matchers: a key type, a value type, then zero or more `expr => expr` entries separated by commas with an optional trailing comma.
2. Use the narrowest fragments that preserve the required syntax. Use `ty` for declared types and `expr` for evaluated entries; do not use `tt` as a universal escape hatch.
3. Bind each key and value once inside the repetition before insertion. This makes evaluation count inspectable and protects expressions with side effects.
4. Expand to one block expression whose final value is the map. Keep temporary names inside the block and choose paths that do not depend on caller imports.
5. Write positive and negative cases for empty input, trailing commas, malformed entries, duplicate runtime keys, and expressions with observable evaluation.

### Required proof

Produce three artifacts:

- a matcher grammar and evaluation semantics record that names the authority and the generated or checked surface;
- the smallest invocation, item, or build input that reproduces the original defect;
- a positive or negative test that would fail if the superficial repair replaced the principled one.

Your repair is incomplete if it merely changes token spelling. Explain how the accepted language, generated surface, evaluation semantics, names, errors, and compatibility obligations changed.

## Part 3 — Focused exercises

### Exercise 1 — Fragment selection

Choose fragment kinds for a visibility, type name, generic type, field expression, literal diagnostic code, attribute, and arbitrary nested token group. Explain one failure caused by choosing `tt` where `expr` or `ty` was intended.

### Exercise 2 — Repetition invariant

Explain the rule relating metavariable repetition depth between matcher and transcriber. Repair a macro that captures `$name` inside `$(...)*` but emits `$name` outside repetition.

### Exercise 3 — Evaluation audit

Write an expansion sketch for two map entries whose keys increment counters. Prove that each caller expression is evaluated once and in source order.

### Exercise 4 — Follow-set diagnosis

Why is `$e:expr [` rejected while `$e:expr,` is accepted? Give a future-compatibility explanation rather than saying “the compiler is picky.”

### Exercise 5 — Opaque forwarding

A helper macro receives an `expr` fragment and tries to match the literal token `3` in a second macro. Explain why it does not work and give two repairs.

### Exercise 6 — Trailing separators

Design rules that accept one or more entries with an optional trailing comma without creating a second overlapping grammar.

For every answer that proposes a macro, add a one-sentence rejection criterion: what simpler condition would make ordinary Rust preferable?

### Interleaved reasoning pass

1. For **Read a matcher as a grammar rather than as textual substitution**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the matcher and fragment trace.
2. For **Choose fragment specifiers according to the accepted public language**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the matcher and fragment trace.
3. For **Design unambiguous separators, delimiters, optional clauses, and cardinality**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the matcher and fragment trace.
4. For **Keep matcher and transcriber repetition at compatible nesting depths**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the matcher and fragment trace.

5. Identify one guarantee from an earlier course that a careless implementation of **Declarative Macros: Matchers, Fragments, and Repetition** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

### Product: Typed Map Macro

Open [`labs/module-02-typed-map-macro/README.md`](../../labs/module-02-typed-map-macro/README.md) only after completing the prediction table. The starter is intentionally a valid baseline, not a half-written answer.

Before implementation, complete this module-specific design record:

| Decision | Your answer |
|---|---|
| invocation grammar | |
| fragment kind for every metavariable | |
| separator and trailing-separator policy | |
| repetition-depth invariant | |
| expansion position | |
| caller-expression evaluation count | |
| temporary-name policy | |
| duplicate-key runtime behavior | |

Build the smallest valid **matcher grammar and evaluation semantics** surface first. Add one accepted case, one rejection owned by this mechanism, and one case that expands successfully before ordinary Rust rejects a later obligation. Compare with the reference only after those three phase boundaries are protected by tests.

### Laboratory acceptance trace

Before opening the reference implementation for **Typed Map Macro**, record:

- the public behavior that demonstrates **Read a matcher as a grammar rather than as textual substitution**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement the declarative diagnostic catalog. One declaration must generate the enum, stable code lookup, message lookup, reverse lookup, and deterministic `ALL` table. Audit every metavariable’s fragment kind and repetition depth.

The capstone increment must leave a visible design record: one diagram or table, one positive test, one negative test, and one statement of what this mechanism deliberately does **not** own.

### Capstone invariant trace

For the Module 42 CommandForge increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. Which caller expressions does the expansion evaluate and how often?
2. Why is `tt` not a default fragment?
3. What does a macro’s accepted punctuation commit you to publicly?
4. Why must the expansion be valid in its invocation position?

Then perform a ten-minute reconstruction: recreate the smallest useful example for this module from an empty file, including one rejected input. If reconstruction requires copying the chapter, return to the mental model before continuing.

### Completion standard

Use the chapter’s readiness statement as the threshold:

Continue when you can read a `macro_rules!` definition and state:

- its grammar and cardinality;
- the role of every separator;
- the fragment class of every metavariable;
- the repetition depth of every capture;
- the expansion category;
- expression evaluation count and order;
- ownership consequences;
- the point at which the grammar should migrate to procedural parsing.

Do not continue if your debugging method is to change `expr` to `tt`, add catch-all arms, or raise recursion limits without explaining the grammar.

Before advancing, defend these module-specific points:

- why each fragment is narrower than `tt`
- how matcher repetition corresponds to transcriber repetition
- where caller expressions move or borrow
- which punctuation is now part of the public API

### Closed-book defense

In five minutes, answer “How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics?” using the **matcher and fragment trace**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside CommandForge. A list of APIs without the deciding relationship is incomplete.
