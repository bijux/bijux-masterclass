# Compiler investigation — Module 1: Compilation, Expressions, and Types

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-01-compilation-expressions-and-types/index.md)

This set tests whether the model from Module 1 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-semicolon-changes-return.rs`](01-semicolon-changes-return.rs) | Which compile-time or runtime rule decides the behavior of **semicolon changes return**, and what evidence would distinguish the closest competing explanation? |
| [`02-immutable-binding.rs`](02-immutable-binding.rs) | Which compile-time or runtime rule decides the behavior of **immutable binding**, and what evidence would distinguish the closest competing explanation? |
| [`03-array-length-is-type.rs`](03-array-length-is-type.rs) | Which compile-time or runtime rule decides the behavior of **array length is type**, and what evidence would distinguish the closest competing explanation? |
| [`04-if-arms-one-type.rs`](04-if-arms-one-type.rs) | Which compile-time or runtime rule decides the behavior of **if arms one type**, and what evidence would distinguish the closest competing explanation? |
| [`05-parse-needs-target-type.rs`](05-parse-needs-target-type.rs) | Which compile-time or runtime rule decides the behavior of **parse needs target type**, and what evidence would distinguish the closest competing explanation? |
| [`06-shadowing-can-change-type.rs`](06-shadowing-can-change-type.rs) | Which compile-time or runtime rule decides the behavior of **shadowing can change type**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
