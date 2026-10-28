# Compiler investigation — Module 13: Scoped Access and Escape Prevention

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-13-scoped-access-and-escape-prevention/index.md)

This set tests whether the model from Module 13 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-hrtb-owned-result.rs`](01-hrtb-owned-result.rs) | Which compile-time or runtime rule decides the behavior of **hrtb owned result**, and what evidence would distinguish the closest competing explanation? |
| [`02-hrtb-reference-escape.rs`](02-hrtb-reference-escape.rs) | Which compile-time or runtime rule decides the behavior of **hrtb reference escape**, and what evidence would distinguish the closest competing explanation? |
| [`03-fnonce-consumes-capture.rs`](03-fnonce-consumes-capture.rs) | Which compile-time or runtime rule decides the behavior of **fnonce consumes capture**, and what evidence would distinguish the closest competing explanation? |
| [`04-fnmut-captured-counter.rs`](04-fnmut-captured-counter.rs) | Which compile-time or runtime rule decides the behavior of **fnmut captured counter**, and what evidence would distinguish the closest competing explanation? |
| [`05-scratch-view-return.rs`](05-scratch-view-return.rs) | Which compile-time or runtime rule decides the behavior of **scratch view return**, and what evidence would distinguish the closest competing explanation? |
| [`06-owned-ranges-escape.rs`](06-owned-ranges-escape.rs) | Which compile-time or runtime rule decides the behavior of **owned ranges escape**, and what evidence would distinguish the closest competing explanation? |
| [`07-naive-self-reference.rs`](07-naive-self-reference.rs) | Which compile-time or runtime rule decides the behavior of **naive self reference**, and what evidence would distinguish the closest competing explanation? |
| [`08-opaque-borrowed-iterator.rs`](08-opaque-borrowed-iterator.rs) | Which compile-time or runtime rule decides the behavior of **opaque borrowed iterator**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
