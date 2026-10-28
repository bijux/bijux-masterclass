# Compiler investigation — Module 17: Interior Mutability and Runtime Borrows

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-17-interior-mutability-and-runtime-borrows/index.md)

This set tests whether the model from Module 17 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-mutate-through-shared-self.rs`](01-mutate-through-shared-self.rs) | Which compile-time or runtime rule decides the behavior of **mutate through shared self**, and what evidence would distinguish the closest competing explanation? |
| [`02-cell-scalar.rs`](02-cell-scalar.rs) | Which compile-time or runtime rule decides the behavior of **cell scalar**, and what evidence would distinguish the closest competing explanation? |
| [`03-refcell-conflict-runtime.rs`](03-refcell-conflict-runtime.rs) | Which compile-time or runtime rule decides the behavior of **refcell conflict runtime**, and what evidence would distinguish the closest competing explanation? |
| [`04-try-borrow-conflict.rs`](04-try-borrow-conflict.rs) | Which compile-time or runtime rule decides the behavior of **try borrow conflict**, and what evidence would distinguish the closest competing explanation? |
| [`05-nested-reborrow-compiles.rs`](05-nested-reborrow-compiles.rs) | Which compile-time or runtime rule decides the behavior of **nested reborrow compiles**, and what evidence would distinguish the closest competing explanation? |
| [`06-once-cell-lazy.rs`](06-once-cell-lazy.rs) | Which compile-time or runtime rule decides the behavior of **once cell lazy**, and what evidence would distinguish the closest competing explanation? |
| [`07-stale-once-cell-design.rs`](07-stale-once-cell-design.rs) | Which compile-time or runtime rule decides the behavior of **stale once cell design**, and what evidence would distinguish the closest competing explanation? |
| [`08-rc-refcell-cycle.rs`](08-rc-refcell-cycle.rs) | Which compile-time or runtime rule decides the behavior of **rc refcell cycle**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
