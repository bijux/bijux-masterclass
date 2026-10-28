# Compiler investigation — Module 11: Places, Move Paths, and Advanced Borrowing

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-11-places-move-paths-and-advanced-borrowing/index.md)

This set tests whether the model from Module 11 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-disjoint-fields.rs`](01-disjoint-fields.rs) | Which compile-time or runtime rule decides the behavior of **disjoint fields**, and what evidence would distinguish the closest competing explanation? |
| [`02-indexed-exclusive-borrows.rs`](02-indexed-exclusive-borrows.rs) | Which compile-time or runtime rule decides the behavior of **indexed exclusive borrows**, and what evidence would distinguish the closest competing explanation? |
| [`03-split-at-mut-proof.rs`](03-split-at-mut-proof.rs) | Which compile-time or runtime rule decides the behavior of **split at mut proof**, and what evidence would distinguish the closest competing explanation? |
| [`04-partial-move-whole-use.rs`](04-partial-move-whole-use.rs) | Which compile-time or runtime rule decides the behavior of **partial move whole use**, and what evidence would distinguish the closest competing explanation? |
| [`05-reborrow-exclusive.rs`](05-reborrow-exclusive.rs) | Which compile-time or runtime rule decides the behavior of **reborrow exclusive**, and what evidence would distinguish the closest competing explanation? |
| [`06-two-phase-method-borrow.rs`](06-two-phase-method-borrow.rs) | Which compile-time or runtime rule decides the behavior of **two phase method borrow**, and what evidence would distinguish the closest competing explanation? |
| [`07-shared-loan-still-used.rs`](07-shared-loan-still-used.rs) | Which compile-time or runtime rule decides the behavior of **shared loan still used**, and what evidence would distinguish the closest competing explanation? |
| [`08-separate-read-and-write-phases.rs`](08-separate-read-and-write-phases.rs) | Which compile-time or runtime rule decides the behavior of **separate read and write phases**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
