# Compiler investigation — Module 9: Crates, Modules, Public APIs, Tests, and Documentation

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-09-crates-modules-public-apis-tests-and-documentation/index.md)

This set tests whether the model from Module 9 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-private-library-item.rs`](01-private-library-item.rs) | Which compile-time or runtime rule decides the behavior of **private library item**, and what evidence would distinguish the closest competing explanation? |
| [`02-public-type-private-field.rs`](02-public-type-private-field.rs) | Which compile-time or runtime rule decides the behavior of **public type private field**, and what evidence would distinguish the closest competing explanation? |
| [`03-reexport-path.rs`](03-reexport-path.rs) | Which compile-time or runtime rule decides the behavior of **reexport path**, and what evidence would distinguish the closest competing explanation? |
| [`04-integration-crate-root.rs`](04-integration-crate-root.rs) | Which compile-time or runtime rule decides the behavior of **integration crate root**, and what evidence would distinguish the closest competing explanation? |
| [`05-doctest-question-mark-context.rs`](05-doctest-question-mark-context.rs) | Which compile-time or runtime rule decides the behavior of **doctest question mark context**, and what evidence would distinguish the closest competing explanation? |
| [`06-public-field-invariant-hole.rs`](06-public-field-invariant-hole.rs) | Which compile-time or runtime rule decides the behavior of **public field invariant hole**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
