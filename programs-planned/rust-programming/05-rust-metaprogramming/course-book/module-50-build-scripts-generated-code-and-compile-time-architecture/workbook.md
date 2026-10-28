# Workbook — Module 50: Build Scripts, Generated Code, and Compile-Time Architecture

[Chapter](index.md) · [Laboratory](../../labs/module-10-generated-code-build/README.md) · [CommandForge guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Build Scripts, Generated Code, and Compile-Time Architecture** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?* Preserve your first prediction and record decisive facts in a **generation authority and reproducibility record**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 49 — Function-Like Procedural Macros and Typed DSLs that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?**
3. Draw the smallest **generation authority and reproducibility record** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen about **build reproducibility and source authority**, record the expected outcome, the first decisive source shape, the earliest phase that knows the fact, the smallest repair preserving the requirement, and one tempting change that would obtain a pass by weakening this module’s public contract.

| # | Specimen | Your committed prediction |
|---:|---|---|
| 1 | [`main.rs`](../../compiler-labs/module-10/case-01/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 2 | [`main.rs`](../../compiler-labs/module-10/case-02/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 3 | [`main.rs`](../../compiler-labs/module-10/case-03/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 4 | [`main.rs`](../../compiler-labs/module-10/case-04/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 5 | [`main.rs`](../../compiler-labs/module-10/case-05/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 6 | [`main.rs`](../../compiler-labs/module-10/case-06/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 7 | [`main.rs`](../../compiler-labs/module-10/case-07/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 8 | [`main.rs`](../../compiler-labs/module-10/case-08/src/main.rs) | Pass or fail? Name the exact phase and rule. |

Run this course’s cases from the program root with:

```bash
python3 tools/run_compiler_labs.py 05-rust-metaprogramming
```

Do not accept “the macro failed” as an explanation. Distinguish matcher failure, parser failure, semantic validation, expansion, name resolution, type checking, build-script validation, and runtime behavior.

## Part 2 — Diagnose and repair

A build script scans a directory recursively, depends on file iteration order, writes generated code into `src/`, embeds absolute paths and timestamps, reruns on every package change, and duplicates command codes already declared in a macro. Local incremental builds appear successful while clean builds differ.

### Repair sequence

1. Name one checked-in external input and one generated output under `OUT_DIR`. Never modify source files from `build.rs`.
2. Emit precise `cargo::rerun-if-changed` and `cargo::rerun-if-env-changed` instructions for declared inputs only.
3. Parse and validate the complete input before writing. Detect duplicates, malformed rows, invalid ranges, and nondeterministic order.
4. Generate to a temporary in-memory buffer or temporary file, then write one deterministic output with no timestamps, absolute paths, or host-only assumptions.
5. Remove overlapping authority. If exit codes come from the external table, no macro or runtime module independently redeclares them.

### Required proof

Produce three artifacts:

- a build reproducibility and source authority record that names the authority and the generated or checked surface;
- the smallest invocation, item, or build input that reproduces the original defect;
- a positive or negative test that would fail if the superficial repair replaced the principled one.

Your repair is incomplete if it merely changes token spelling. Explain how the accepted language, generated surface, evaluation semantics, names, errors, and compatibility obligations changed.

## Part 3 — Focused exercises

### Exercise 1 — Host versus target

Why is `cfg!(target_os = "linux")` inside `build.rs` usually about the wrong machine during cross-compilation?

### Exercise 2 — Rerun contract

A script reads `config/codes.tsv` and `COMMAND_PREFIX`. Which Cargo directives should it emit?

### Exercise 3 — OUT_DIR discipline

Why is writing `src/generated.rs` from a build script harmful even if the file is gitignored?

### Exercise 4 — Transactional generation

Design a build-script sequence that never leaves partially generated Rust after an input error.

### Exercise 5 — Deterministic input

A directory supplies schema fragments. How do you make generation reproducible?

### Exercise 6 — Authority review

Command names are in the DSL, handler metadata is generated by attributes, argument fields by derives, diagnostic codes by `macro_rules!`, and exit codes by TSV. Identify one illegal overlap.

For every answer that proposes a macro, add a one-sentence rejection criterion: what simpler condition would make ordinary Rust preferable?

### Interleaved reasoning pass

1. For **Explain the Cargo build-script lifecycle and communication protocol**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the generation authority and reproducibility record.
2. For **Read host and target configuration correctly**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the generation authority and reproducibility record.
3. For **Declare rebuild inputs with `cargo::rerun-if-changed` and `cargo::rerun-if-env-changed`**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the generation authority and reproducibility record.
4. For **Write generated files only under `OUT_DIR`**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the generation authority and reproducibility record.

5. Identify one guarantee from an earlier course that a careless implementation of **Build Scripts, Generated Code, and Compile-Time Architecture** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

### Product: Generated Code Build

Open [`labs/module-10-generated-code-build/README.md`](../../labs/module-10-generated-code-build/README.md) only after completing the prediction table. The starter is intentionally a valid baseline, not a half-written answer.

Before implementation, complete this module-specific design record:

| Decision | Your answer |
|---|---|
| checked-in source data | |
| schema and semantic validation | |
| rerun directives | |
| normalized ordering | |
| generated module interface | |
| temporary-write protocol | |
| replacement behavior | |
| source-of-truth ownership | |

Build the smallest valid **build reproducibility and source authority** surface first. Add one accepted case, one rejection owned by this mechanism, and one case that expands successfully before ordinary Rust rejects a later obligation. Compare with the reference only after those three phase boundaries are protected by tests.

### Laboratory acceptance trace

Before opening the reference implementation for **Generated Code Build**, record:

- the public behavior that demonstrates **Explain the Cargo build-script lifecycle and communication protocol**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Finish CommandForge’s build architecture. Validate `config/exit_codes.tsv`, generate constants and lookup data under `OUT_DIR`, include them from runtime code, and prove deterministic output, precise rerun triggers, and one-owner authority.

The capstone increment must leave a visible design record: one diagram or table, one positive test, one negative test, and one statement of what this mechanism deliberately does **not** own.

### Capstone invariant trace

For the Module 50 CommandForge increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What are the declared inputs and outputs of the build script?
2. How does clean-build correctness differ from incremental success?
3. Which data belongs in a build script rather than a procedural macro?
4. How do you prevent overlapping compile-time authority?

Then perform a ten-minute reconstruction: recreate the smallest useful example for this module from an empty file, including one rejected input. If reconstruction requires copying the chapter, return to the mental model before continuing.

### Completion standard

Use the chapter’s readiness statement as the threshold:

Finish when you can defend:

- every source of truth;
- every generated surface;
- every compile-time dependency;
- every environmental input;
- every rebuild trigger;
- deterministic ordering and escaping;
- host-versus-target assumptions;
- failure atomicity of generation;
- runtime behavior left outside macros;
- the reason each generator survives deletion.

The final standard is not “I can write macros.” It is:

> I can design, test, constrain, and delete compile-time machinery until the remaining system has one honest authority per fact.

Before advancing, defend these module-specific points:

- what Cargo knows from rerun directives
- why generated output belongs under `OUT_DIR`
- how partial output is prevented
- which generated interface must remain stable for downstream Rust

### Closed-book defense

In five minutes, answer “How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?” using the **generation authority and reproducibility record**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside CommandForge. A list of APIs without the deciding relationship is incomplete.
