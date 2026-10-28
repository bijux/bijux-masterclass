# Compiler investigation — Module 23: Coherence and Implementation Ownership

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-23-coherence-and-implementation-ownership/index.md)

This set tests whether the model from Module 23 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-local-trait-foreign-type.rs`](01-local-trait-foreign-type.rs) | Which compile-time or runtime rule decides the behavior of **local trait foreign type**, and what evidence would distinguish the closest competing explanation? |
| [`02-foreign-trait-local-type.rs`](02-foreign-trait-local-type.rs) | Which compile-time or runtime rule decides the behavior of **foreign trait local type**, and what evidence would distinguish the closest competing explanation? |
| [`03-foreign-trait-foreign-type.rs`](03-foreign-trait-foreign-type.rs) | Which compile-time or runtime rule decides the behavior of **foreign trait foreign type**, and what evidence would distinguish the closest competing explanation? |
| [`04-overlapping-blanket-impls.rs`](04-overlapping-blanket-impls.rs) | Which compile-time or runtime rule decides the behavior of **overlapping blanket impls**, and what evidence would distinguish the closest competing explanation? |
| [`05-newtype-ownership.rs`](05-newtype-ownership.rs) | Which compile-time or runtime rule decides the behavior of **newtype ownership**, and what evidence would distinguish the closest competing explanation? |
| [`06-extension-trait-scope.rs`](06-extension-trait-scope.rs) | Which compile-time or runtime rule decides the behavior of **extension trait scope**, and what evidence would distinguish the closest competing explanation? |
| [`07-sealed-trait-implementation.rs`](07-sealed-trait-implementation.rs) | Which compile-time or runtime rule decides the behavior of **sealed trait implementation**, and what evidence would distinguish the closest competing explanation? |
| [`08-type-alias-identity.rs`](08-type-alias-identity.rs) | Which compile-time or runtime rule decides the behavior of **type alias identity**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
