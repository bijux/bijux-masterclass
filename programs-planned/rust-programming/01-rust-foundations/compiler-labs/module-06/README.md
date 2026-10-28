# Compiler investigation — Module 6: Collections, Iterators, and Closures

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-06-collections-iterators-and-closures/index.md)

This set tests whether the model from Module 6 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-into-iter-consumes-vector.rs`](01-into-iter-consumes-vector.rs) | Which compile-time or runtime rule decides the behavior of **into iter consumes vector**, and what evidence would distinguish the closest competing explanation? |
| [`02-mutate-while-shared-iter.rs`](02-mutate-while-shared-iter.rs) | Which compile-time or runtime rule decides the behavior of **mutate while shared iter**, and what evidence would distinguish the closest competing explanation? |
| [`03-collect-needs-type.rs`](03-collect-needs-type.rs) | Which compile-time or runtime rule decides the behavior of **collect needs type**, and what evidence would distinguish the closest competing explanation? |
| [`04-index-can-panic.rs`](04-index-can-panic.rs) | Which compile-time or runtime rule decides the behavior of **index can panic**, and what evidence would distinguish the closest competing explanation? |
| [`05-hash-order-is-not-contract.rs`](05-hash-order-is-not-contract.rs) | Which compile-time or runtime rule decides the behavior of **hash order is not contract**, and what evidence would distinguish the closest competing explanation? |
| [`06-filter-borrows-source.rs`](06-filter-borrows-source.rs) | Which compile-time or runtime rule decides the behavior of **filter borrows source**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
