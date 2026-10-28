# Compiler investigation — Module 22: Associated Types and Type Families

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-22-associated-types-and-type-families/index.md)

This set tests whether the model from Module 22 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-associated-projection.rs`](01-associated-projection.rs) | Which compile-time or runtime rule decides the behavior of **associated projection**, and what evidence would distinguish the closest competing explanation? |
| [`02-ambiguous-associated-type.rs`](02-ambiguous-associated-type.rs) | Which compile-time or runtime rule decides the behavior of **ambiguous associated type**, and what evidence would distinguish the closest competing explanation? |
| [`03-generic-relationship-multiplicity.rs`](03-generic-relationship-multiplicity.rs) | Which compile-time or runtime rule decides the behavior of **generic relationship multiplicity**, and what evidence would distinguish the closest competing explanation? |
| [`04-associated-type-uniqueness.rs`](04-associated-type-uniqueness.rs) | Which compile-time or runtime rule decides the behavior of **associated type uniqueness**, and what evidence would distinguish the closest competing explanation? |
| [`05-generic-associated-type.rs`](05-generic-associated-type.rs) | Which compile-time or runtime rule decides the behavior of **generic associated type**, and what evidence would distinguish the closest competing explanation? |
| [`06-lending-borrow-overlap.rs`](06-lending-borrow-overlap.rs) | Which compile-time or runtime rule decides the behavior of **lending borrow overlap**, and what evidence would distinguish the closest competing explanation? |
| [`07-unspecified-associated-type.rs`](07-unspecified-associated-type.rs) | Which compile-time or runtime rule decides the behavior of **unspecified associated type**, and what evidence would distinguish the closest competing explanation? |
| [`08-gat-dyn-incompatibility.rs`](08-gat-dyn-incompatibility.rs) | Which compile-time or runtime rule decides the behavior of **gat dyn incompatibility**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
