# Workbook — Module 41: Metaprogramming Boundaries and the Expansion Model

[Chapter](index.md) · [Laboratory](../../labs/module-01-decision-table-generator/README.md) · [CommandForge guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Metaprogramming Boundaries and the Expansion Model** has become a usable model rather than remembered vocabulary. Its governing question is: *Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs?* Preserve your first prediction and record decisive facts in a **mechanism-selection record**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 40 — Functional Architecture Synthesis that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs?**
3. Draw the smallest **mechanism-selection record** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen about **mechanism selection and phase ownership**, record the expected outcome, the first decisive source shape, the earliest phase that knows the fact, the smallest repair preserving the requirement, and one tempting change that would obtain a pass by weakening this module’s public contract.

| # | Specimen | Your committed prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-01/case-01.rs) | Pass or fail? Name the exact phase and rule. |
| 2 | [`case-02.rs`](../../compiler-labs/module-01/case-02.rs) | Pass or fail? Name the exact phase and rule. |
| 3 | [`case-03.rs`](../../compiler-labs/module-01/case-03.rs) | Pass or fail? Name the exact phase and rule. |
| 4 | [`case-04.rs`](../../compiler-labs/module-01/case-04.rs) | Pass or fail? Name the exact phase and rule. |
| 5 | [`case-05.rs`](../../compiler-labs/module-01/case-05.rs) | Pass or fail? Name the exact phase and rule. |
| 6 | [`case-06.rs`](../../compiler-labs/module-01/case-06.rs) | Pass or fail? Name the exact phase and rule. |
| 7 | [`case-07.rs`](../../compiler-labs/module-01/case-07.rs) | Pass or fail? Name the exact phase and rule. |
| 8 | [`case-08.rs`](../../compiler-labs/module-01/case-08.rs) | Pass or fail? Name the exact phase and rule. |

Run this course’s cases from the program root with:

```bash
python3 tools/run_compiler_labs.py 05-rust-metaprogramming
```

Do not accept “the macro failed” as an explanation. Distinguish matcher failure, parser failure, semantic validation, expansion, name resolution, type checking, build-script validation, and runtime behavior.

## Part 2 — Diagnose and repair

A team proposes a `define_commands!` macro that accepts command names, reads environment variables, opens a configuration file, validates runtime permissions, constructs a registry, prints help, and dispatches handlers. The proposal combines five authorities: syntax declaration, external data, runtime policy, I/O, and dispatch. Every future change would require understanding expansion, build behavior, and runtime behavior at once.

### Repair sequence

1. Write a source-of-truth table. For every fact, name who declares it, who validates it, who consumes it, and when it becomes known.
2. Move runtime values and permission checks into ordinary functions. Keep runtime dispatch in ordinary Rust unless a compile-time relation actually needs generation.
3. Use a small declarative macro only for the declaration that must appear in several Rust syntactic positions, such as an enum variant and exhaustive match arms.
4. Use a build script only for checked external data that exists before compilation and must become Rust source. Make the input path and rerun rule explicit.
5. Run the deletion test: remove the generator mentally and estimate the manual duplication. If deletion produces only a short table or one ordinary function, reject the generator.

### Required proof

Produce three artifacts:

- a mechanism selection and phase ownership record that names the authority and the generated or checked surface;
- the smallest invocation, item, or build input that reproduces the original defect;
- a positive or negative test that would fail if the superficial repair replaced the principled one.

Your repair is incomplete if it merely changes token spelling. Explain how the accepted language, generated surface, evaluation semantics, names, errors, and compatibility obligations changed.

## Part 3 — Focused exercises

### Exercise 1 — Mechanism matrix

Classify ten requirements—runtime string normalization, enum/code/message association, third-party configuration loaded at startup, deriving field metadata, validating an attached function, parsing a route DSL, and generating constants from a checked TSV file—by the least powerful suitable mechanism. For each, identify the source of truth and the phase that first knows enough to validate it.

### Exercise 2 — Two-program trace

Take a macro that emits an implementation requiring `T: Display`. Trace what the generator can know, what expansion produces, and where a missing `Display` implementation is rejected.

### Exercise 3 — Position audit

For one expression macro, one item macro, and one type macro, state legal invocation positions and one invalid position. Explain why balanced tokens are not enough.

### Exercise 4 — Deletion test

Evaluate whether a macro is justified for a three-row command table that is only iterated at runtime. Then change the requirement so the same declaration must generate an enum, exhaustive dispatch, and documentation metadata.

### Exercise 5 — Failure taxonomy

Classify these failures: missing comma in a DSL, duplicate literal route, unresolved generated path, unsatisfied generated trait bound, malformed TSV input, and unavailable runtime file.

### Exercise 6 — Authority ledger

Design an authority ledger for CommandForge covering command name, handler signature, argument fields, diagnostic code, and exit status.

For every answer that proposes a macro, add a one-sentence rejection criterion: what simpler condition would make ordinary Rust preferable?

### Interleaved reasoning pass

1. For **Separate runtime abstraction from compile-time generation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the mechanism-selection record.
2. For **Identify the source of truth and generated surface of a proposed macro**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the mechanism-selection record.
3. For **Explain expansion as a staged production of ordinary Rust tokens**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the mechanism-selection record.
4. For **Distinguish matcher, parser, name-resolution, type-checking, build, and runtime failures**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the mechanism-selection record.

5. Identify one guarantee from an earlier course that a careless implementation of **Metaprogramming Boundaries and the Expansion Model** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

### Product: Decision Table Generator

Open [`labs/module-01-decision-table-generator/README.md`](../../labs/module-01-decision-table-generator/README.md) only after completing the prediction table. The starter is intentionally a valid baseline, not a half-written answer.

Before implementation, complete this module-specific design record:

| Decision | Your answer |
|---|---|
| requirement being centralized | |
| ordinary-Rust reference design | |
| least powerful adequate mechanism | |
| single source of truth | |
| generated surfaces | |
| facts still checked by ordinary Rust | |
| failure phase | |
| deletion criterion | |

Build the smallest valid **mechanism selection and phase ownership** surface first. Add one accepted case, one rejection owned by this mechanism, and one case that expands successfully before ordinary Rust rejects a later obligation. Compare with the reference only after those three phase boundaries are protected by tests.

### Laboratory acceptance trace

Before opening the reference implementation for **Decision Table Generator**, record:

- the public behavior that demonstrates **Separate runtime abstraction from compile-time generation**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Create CommandForge’s authority ledger and phase map before writing any macro. Record every generated surface and one explicit non-goal for each mechanism. The increment is complete when no command fact has two independent owners.

The capstone increment must leave a visible design record: one diagram or table, one positive test, one negative test, and one statement of what this mechanism deliberately does **not** own.

### Capstone invariant trace

For the Module 41 CommandForge increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. Why is repetition alone insufficient to justify a macro?
2. Which failure phase owns an unresolved path emitted by a successful macro?
3. What makes a build script different from a runtime configuration parser?
4. Which CommandForge facts must remain ordinary Rust?

Then perform a ten-minute reconstruction: recreate the smallest useful example for this module from an empty file, including one rejected input. If reconstruction requires copying the chapter, return to the mental model before continuing.

### Completion standard

Use the chapter’s readiness statement as the threshold:

Continue when you can take an unfamiliar macro proposal and produce:

- an ordinary-Rust reference design;
- a precise source of truth;
- a generated-surface list;
- a phase-aware failure table;
- an evaluation-order statement;
- a deletion-test conclusion.

Do not continue if your reason for a macro is “less typing,” “looks cleaner,” or “the type is complicated.” Those may be outcomes, but they are not ownership of a compile-time relationship.

Before advancing, defend these module-specific points:

- why repetition alone is not sufficient justification
- which facts become duplicated if generation is removed
- why the selected mechanism is weaker than the alternatives above it
- what change would make the macro unnecessary

### Closed-book defense

In five minutes, answer “Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs?” using the **mechanism-selection record**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside CommandForge. A list of APIs without the deciding relationship is incomplete.
