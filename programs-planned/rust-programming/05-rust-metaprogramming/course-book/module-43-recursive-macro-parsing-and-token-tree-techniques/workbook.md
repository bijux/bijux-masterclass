# Workbook — Module 43: Recursive Macro Parsing and Token-Tree Techniques

[Return to the chapter](index.md) · [Open the CommandForge engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Recursive Macro Parsing and Token-Tree Techniques** as an engineering mechanism rather than repeat its syntax. The governing question is:

> How can a declarative macro process a nontrivial token language with explicit parser state, guaranteed progress, and bounded complexity?

Trace every recursive rule as a parser transition. Record the current state, the input consumed, the accumulator produced, and the base case. A macro that eventually hits recursion limit has not proved progress merely because it is recursive.

## Part 1 — Predict

For each specimen about **recursive parser progress**, record the expected outcome, the first decisive source shape, the earliest phase that knows the fact, the smallest repair preserving the requirement, and one tempting change that would obtain a pass by weakening this module’s public contract.

| # | Specimen | Your committed prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-03/case-01.rs) | Pass or fail? Name the exact phase and rule. |
| 2 | [`case-02.rs`](../../compiler-labs/module-03/case-02.rs) | Pass or fail? Name the exact phase and rule. |
| 3 | [`case-03.rs`](../../compiler-labs/module-03/case-03.rs) | Pass or fail? Name the exact phase and rule. |
| 4 | [`case-04.rs`](../../compiler-labs/module-03/case-04.rs) | Pass or fail? Name the exact phase and rule. |
| 5 | [`case-05.rs`](../../compiler-labs/module-03/case-05.rs) | Pass or fail? Name the exact phase and rule. |
| 6 | [`case-06.rs`](../../compiler-labs/module-03/case-06.rs) | Pass or fail? Name the exact phase and rule. |
| 7 | [`case-07.rs`](../../compiler-labs/module-03/case-07.rs) | Pass or fail? Name the exact phase and rule. |
| 8 | [`case-08.rs`](../../compiler-labs/module-03/case-08.rs) | Pass or fail? Name the exact phase and rule. |

Run this course’s cases from the program root with:

```bash
python3 tools/run_compiler_labs.py 05-rust-metaprogramming
```

Do not accept “the macro failed” as an explanation. Distinguish matcher failure, parser failure, semantic validation, expansion, name resolution, type checking, build-script validation, and runtime behavior.

## Part 2 — Diagnose and repair

A state-machine macro tries to parse all states and transitions in one matcher. It accepts an arbitrary sequence of token trees, recursively calls itself without removing input on one branch, appends generated code during parsing, and reports every mistake as “no rules expected this token.” The grammar cannot be reviewed independently from emission.

### Repair sequence

1. Write the external grammar in plain text and identify its separators, terminators, and entry categories.
2. Split the macro into a small public rule and private `@state` rules. Every recursive rule must consume input or transition to a terminal state.
3. Carry an accumulator for normalized state and transition tokens. Do not emit the public item until parsing and local validation have reached the terminal rule.
4. Place specific malformed-input rules before a generic fallback so missing arrows, separators, and terminators receive targeted `compile_error!` messages.
5. Cap the grammar. If validation requires arbitrary lookup, rich spans, or many interacting states, move to a procedural macro rather than extending a TT muncher indefinitely.

### Required proof

Produce three artifacts:

- a recursive parser progress record that names the authority and the generated or checked surface;
- the smallest invocation, item, or build input that reproduces the original defect;
- a positive or negative test that would fail if the superficial repair replaced the principled one.

Your repair is incomplete if it merely changes token spelling. Explain how the accepted language, generated surface, evaluation semantics, names, errors, and compatibility obligations changed.

## Part 3 — Focused exercises

### Exercise 1 — Grammar before matcher

Write an EBNF-like grammar for `state_machine!` with a visibility, enum name, state list, and transition list. Mark the token that terminates each production.

### Exercise 2 — Progress proof

For each recursive rule in a TT muncher, write the size of remaining input before and after the call. Identify a rule that can recurse without consuming tokens.

### Exercise 3 — Accumulator shape

Compare accumulating raw tokens with accumulating normalized pairs such as `(Source => Target)`. Which makes the terminal emitter easier to audit?

### Exercise 4 — Duplicate limitations

Explain why reliable duplicate-state detection is awkward in `macro_rules!`. State a bounded declarative solution and the point at which a procedural macro is justified.

### Exercise 5 — Targeted fallback

Design malformed-input rules for a missing `=>`, missing semicolon, and unknown top-level section. Explain rule ordering.

### Exercise 6 — Complexity review

Estimate how many times a one-token-at-a-time muncher revisits the remaining stream. Propose a grammar change that reduces expansion work.

For every answer that proposes a macro, add a one-sentence rejection criterion: what simpler condition would make ordinary Rust preferable?

## Part 4 — Independent laboratory

### Product: State Machine DSL

Open [`labs/module-03-state-machine-dsl/README.md`](../../labs/module-03-state-machine-dsl/README.md) only after completing the prediction table. The starter is intentionally a valid baseline, not a half-written answer.

Before implementation, complete this module-specific design record:

| Decision | Your answer |
|---|---|
| token grammar | |
| parser states | |
| input consumed by each transition | |
| accumulator shape | |
| base cases | |
| malformed-input rules | |
| recursion or complexity bound | |
| generated state-machine surface | |

Build the smallest valid **recursive parser progress** surface first. Add one accepted case, one rejection owned by this mechanism, and one case that expands successfully before ordinary Rust rejects a later obligation. Compare with the reference only after those three phase boundaries are protected by tests.

## Part 5 — Capstone transfer

Prototype the command-catalog grammar first as a written grammar and a normalized model. Do not implement the procedural macro yet. Identify local syntax rules, cross-entry semantic rules, and type-checker-owned rules.

The capstone increment must leave a visible design record: one diagram or table, one positive test, one negative test, and one statement of what this mechanism deliberately does **not** own.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. How do you prove recursive macro termination?
2. Why should parsing and emission use separate conceptual phases?
3. When does a TT muncher become the wrong mechanism?
4. How does rule order affect diagnostics?

Then perform a ten-minute reconstruction: recreate the smallest useful example for this module from an empty file, including one rejected input. If reconstruction requires copying the chapter, return to the mental model before continuing.

### Completion standard

Use the chapter’s readiness statement as the threshold:

Continue when you can explain a recursive macro as:

- a finite set of parser states;
- a public grammar and internal state grammar;
- a decreasing measure;
- a base case;
- an accumulator shape;
- a generated runtime structure and cost;
- a set of targeted failure states;
- a clear threshold for procedural migration.

Do not continue if recursion is “working” only because the input is tiny, the recursion limit was raised, or unknown tokens are ignored.

Before advancing, defend these module-specific points:

- the progress argument for every recursive rule
- why one catch-all rule would hide grammar defects
- which facts are syntax and which are semantic
- when a procedural parser would be clearer
