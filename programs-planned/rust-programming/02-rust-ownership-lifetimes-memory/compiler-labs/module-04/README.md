# Compiler investigation — Module 14: RAII, Drop, Unwinding, and Failure Atomicity

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-14-raii-drop-unwinding-and-failure-atomicity/index.md)

This set tests whether the model from Module 14 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-direct-drop-call.rs`](01-direct-drop-call.rs) | Which compile-time or runtime rule decides the behavior of **direct drop call**, and what evidence would distinguish the closest competing explanation? |
| [`02-move-field-from-drop-type.rs`](02-move-field-from-drop-type.rs) | Which compile-time or runtime rule decides the behavior of **move field from drop type**, and what evidence would distinguish the closest competing explanation? |
| [`03-option-take-transition.rs`](03-option-take-transition.rs) | Which compile-time or runtime rule decides the behavior of **option take transition**, and what evidence would distinguish the closest competing explanation? |
| [`04-field-drop-order.rs`](04-field-drop-order.rs) | Which compile-time or runtime rule decides the behavior of **field drop order**, and what evidence would distinguish the closest competing explanation? |
| [`05-explicit-drop-releases-guard.rs`](05-explicit-drop-releases-guard.rs) | Which compile-time or runtime rule decides the behavior of **explicit drop releases guard**, and what evidence would distinguish the closest competing explanation? |
| [`06-consuming-commit.rs`](06-consuming-commit.rs) | Which compile-time or runtime rule decides the behavior of **consuming commit**, and what evidence would distinguish the closest competing explanation? |
| [`07-panicking-destructor-compiles.rs`](07-panicking-destructor-compiles.rs) | Which compile-time or runtime rule decides the behavior of **panicking destructor compiles**, and what evidence would distinguish the closest competing explanation? |
| [`08-forgotten-guard-compiles.rs`](08-forgotten-guard-compiles.rs) | Which compile-time or runtime rule decides the behavior of **forgotten guard compiles**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
