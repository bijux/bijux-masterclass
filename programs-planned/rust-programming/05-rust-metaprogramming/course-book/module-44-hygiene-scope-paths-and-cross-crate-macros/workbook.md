# Workbook — Module 44: Hygiene, Scope, Paths, and Cross-Crate Macros

[Return to the chapter](index.md) · [Open the CommandForge engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Hygiene, Scope, Paths, and Cross-Crate Macros** as an engineering mechanism rather than repeat its syntax. The governing question is:

> Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?

For each expansion, mark every identifier as definition-crate-owned, invocation-site-supplied, or generated-local. Then predict resolution after dependency renaming, caller shadowing, and nested-module invocation.

## Part 1 — Predict

For each specimen about **hygiene and cross-crate resolution**, record the expected outcome, the first decisive source shape, the earliest phase that knows the fact, the smallest repair preserving the requirement, and one tempting change that would obtain a pass by weakening this module’s public contract.

| # | Specimen | Your committed prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-04/case-01.rs) | Pass or fail? Name the exact phase and rule. |
| 2 | [`case-02.rs`](../../compiler-labs/module-04/case-02.rs) | Pass or fail? Name the exact phase and rule. |
| 3 | [`case-03.rs`](../../compiler-labs/module-04/case-03.rs) | Pass or fail? Name the exact phase and rule. |
| 4 | [`case-04.rs`](../../compiler-labs/module-04/case-04.rs) | Pass or fail? Name the exact phase and rule. |
| 5 | [`case-05.rs`](../../compiler-labs/module-04/case-05.rs) | Pass or fail? Name the exact phase and rule. |
| 6 | [`case-06.rs`](../../compiler-labs/module-04/case-06.rs) | Pass or fail? Name the exact phase and rule. |
| 7 | [`case-07.rs`](../../compiler-labs/module-04/case-07.rs) | Pass or fail? Name the exact phase and rule. |
| 8 | [`case-08.rs`](../../compiler-labs/module-04/case-08.rs) | Pass or fail? Name the exact phase and rule. |

Run this course’s cases from the program root with:

```bash
python3 tools/run_compiler_labs.py 05-rust-metaprogramming
```

Do not accept “the macro failed” as an explanation. Distinguish matcher failure, parser failure, semantic validation, expansion, name resolution, type checking, build-script validation, and runtime behavior.

## Part 2 — Diagnose and repair

An exported macro expands to `Registry::new()` and calls a helper macro by bare name. It works in the defining crate because local imports happen to provide both names. A downstream crate renames the dependency, shadows `Registry`, and cannot access the private helper function. The macro author calls the failures “user setup errors.”

### Repair sequence

1. Classify every name in the expansion as supplied by the invocation, owned by the defining crate, or intentionally resolved at the invocation site.
2. Use `$crate::qualified::path` for items owned by the defining crate. Do not assume the downstream dependency name.
3. Make every definition-owned item reached by exported expansion publicly visible enough for the invocation site; `$crate` does not bypass visibility.
4. Pass caller-owned expressions and paths as metavariables. Do not invent invocation-site local names and assume the caller can see or bind them.
5. Test from an integration crate and, for a public package, from a fixture that renames the dependency and uses the macro under shadowing imports.

### Required proof

Produce three artifacts:

- a hygiene and cross-crate resolution record that names the authority and the generated or checked surface;
- the smallest invocation, item, or build input that reproduces the original defect;
- a positive or negative test that would fail if the superficial repair replaced the principled one.

Your repair is incomplete if it merely changes token spelling. Explain how the accepted language, generated surface, evaluation semantics, names, errors, and compatibility obligations changed.

## Part 3 — Focused exercises

### Exercise 1 — Name provenance ledger

Classify names in an exported macro expansion: `Vec`, a crate helper type, a caller handler path, a temporary local, and a generated public item.

### Exercise 2 — Dependency rename

Explain why spelling `my_crate::helper()` in an exported macro is fragile. Show the robust declarative path.

### Exercise 3 — Visibility boundary

A macro uses `$crate::private::build()`. Why can expansion still fail outside the crate?

### Exercise 4 — Caller path capture

Choose `ident`, `path`, or `expr` for a handler reference that may be `module::function::<T>`. Explain the choice.

### Exercise 5 — Local collision

An expression macro introduces `let result = ...` and later refers to it. What collision risks remain, and how can structure reduce them?

### Exercise 6 — Cross-crate fixture

Describe a fixture that proves an exported macro survives dependency renaming, missing prelude imports, a shadowing local type, and nested module invocation.

For every answer that proposes a macro, add a one-sentence rejection criterion: what simpler condition would make ordinary Rust preferable?

## Part 4 — Independent laboratory

### Product: Exported Registry Macro

Open [`labs/module-04-exported-registry-macro/README.md`](../../labs/module-04-exported-registry-macro/README.md) only after completing the prediction table. The starter is intentionally a valid baseline, not a half-written answer.

Before implementation, complete this module-specific design record:

| Decision | Your answer |
|---|---|
| definition-crate paths | |
| invocation-site names | |
| generated-local identifiers | |
| `$crate` use | |
| visibility requirements | |
| dependency-renaming fixture | |
| caller-shadowing fixture | |
| exported API surface | |

Build the smallest valid **hygiene and cross-crate resolution** surface first. Add one accepted case, one rejection owned by this mechanism, and one case that expands successfully before ordinary Rust rejects a later obligation. Compare with the reference only after those three phase boundaries are protected by tests.

## Part 5 — Capstone transfer

Define the public path strategy for CommandForge’s generated code. The proc-macro crate must emit absolute standard-library paths and a stable runtime-crate path. Add `extern crate self as commandforge;` so the same path works inside the runtime crate.

The capstone increment must leave a visible design record: one diagram or table, one positive test, one negative test, and one statement of what this mechanism deliberately does **not** own.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What does `$crate` solve and what does it not solve?
2. Which names should resolve at the invocation site?
3. Why are in-crate macro tests insufficient?
4. How does dependency renaming affect generated paths?

Then perform a ten-minute reconstruction: recreate the smallest useful example for this module from an empty file, including one rejected input. If reconstruction requires copying the chapter, return to the mental model before continuing.

### Completion standard

Use the chapter’s readiness statement as the threshold:

Continue when you can explain, for every name in an expansion:

- where it originates;
- where it resolves;
- whether dependency renaming affects it;
- whether privacy permits access;
- whether it becomes public API;
- how a downstream test proves the claim.

Do not continue if your macro works only because the caller imported the same helpers as the defining module.

Before advancing, defend these module-specific points:

- why `$crate` solves only defining-crate paths
- which names intentionally resolve at the call site
- how visibility differs from path resolution
- what downstream test proves the macro is actually portable
