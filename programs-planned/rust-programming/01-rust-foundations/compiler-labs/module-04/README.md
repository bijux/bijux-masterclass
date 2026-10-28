# Compiler investigation — Module 4: Borrowing, References, Slices, and Strings

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-04-borrowing-references-slices-and-strings/index.md)

This set tests whether the model from Module 4 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-shared-then-mutable.rs`](01-shared-then-mutable.rs) | Which compile-time or runtime rule decides the behavior of **shared then mutable**, and what evidence would distinguish the closest competing explanation? |
| [`02-two-indexed-mutable-borrows.rs`](02-two-indexed-mutable-borrows.rs) | Which compile-time or runtime rule decides the behavior of **two indexed mutable borrows**, and what evidence would distinguish the closest competing explanation? |
| [`03-return-reference-to-local.rs`](03-return-reference-to-local.rs) | Which compile-time or runtime rule decides the behavior of **return reference to local**, and what evidence would distinguish the closest competing explanation? |
| [`04-mutate-during-iteration.rs`](04-mutate-during-iteration.rs) | Which compile-time or runtime rule decides the behavior of **mutate during iteration**, and what evidence would distinguish the closest competing explanation? |
| [`05-slice-outlives-owner.rs`](05-slice-outlives-owner.rs) | Which compile-time or runtime rule decides the behavior of **slice outlives owner**, and what evidence would distinguish the closest competing explanation? |
| [`06-reborrow.rs`](06-reborrow.rs) | Which compile-time or runtime rule decides the behavior of **reborrow**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
