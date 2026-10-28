# Compiler investigation — Module 15: Box, Deref, Dynamically Sized Types, and Cow

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-15-box-deref-dynamically-sized-types-and-cow/index.md)

This set tests whether the model from Module 15 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-direct-recursion.rs`](01-direct-recursion.rs) | Which compile-time or runtime rule decides the behavior of **direct recursion**, and what evidence would distinguish the closest competing explanation? |
| [`02-boxed-recursion.rs`](02-boxed-recursion.rs) | Which compile-time or runtime rule decides the behavior of **boxed recursion**, and what evidence would distinguish the closest competing explanation? |
| [`03-move-out-of-unpinned-box.rs`](03-move-out-of-unpinned-box.rs) | Which compile-time or runtime rule decides the behavior of **move out of unpinned box**, and what evidence would distinguish the closest competing explanation? |
| [`04-box-array-unsizes.rs`](04-box-array-unsizes.rs) | Which compile-time or runtime rule decides the behavior of **box array unsizes**, and what evidence would distinguish the closest competing explanation? |
| [`05-question-sized.rs`](05-question-sized.rs) | Which compile-time or runtime rule decides the behavior of **question sized**, and what evidence would distinguish the closest competing explanation? |
| [`06-dst-field-not-last.rs`](06-dst-field-not-last.rs) | Which compile-time or runtime rule decides the behavior of **dst field not last**, and what evidence would distinguish the closest competing explanation? |
| [`07-invariant-breaking-derefmut.rs`](07-invariant-breaking-derefmut.rs) | Which compile-time or runtime rule decides the behavior of **invariant breaking derefmut**, and what evidence would distinguish the closest competing explanation? |
| [`08-cow-borrowed-owned.rs`](08-cow-borrowed-owned.rs) | Which compile-time or runtime rule decides the behavior of **cow borrowed owned**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
