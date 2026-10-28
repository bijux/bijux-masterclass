# Compiler investigation — Module 27: Typestate and Capability-Oriented APIs

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-27-typestate-and-capability-oriented-apis/index.md)

This set tests whether the model from Module 27 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-typestate-transition.rs`](01-typestate-transition.rs) | Which compile-time or runtime rule decides the behavior of **typestate transition**, and what evidence would distinguish the closest competing explanation? |
| [`02-unavailable-state-method.rs`](02-unavailable-state-method.rs) | Which compile-time or runtime rule decides the behavior of **unavailable state method**, and what evidence would distinguish the closest competing explanation? |
| [`03-private-marker-construction.rs`](03-private-marker-construction.rs) | Which compile-time or runtime rule decides the behavior of **private marker construction**, and what evidence would distinguish the closest competing explanation? |
| [`04-consumed-transition-value.rs`](04-consumed-transition-value.rs) | Which compile-time or runtime rule decides the behavior of **consumed transition value**, and what evidence would distinguish the closest competing explanation? |
| [`05-single-use-capability.rs`](05-single-use-capability.rs) | Which compile-time or runtime rule decides the behavior of **single use capability**, and what evidence would distinguish the closest competing explanation? |
| [`06-incomplete-builder.rs`](06-incomplete-builder.rs) | Which compile-time or runtime rule decides the behavior of **incomplete builder**, and what evidence would distinguish the closest competing explanation? |
| [`07-state-erasure-enum.rs`](07-state-erasure-enum.rs) | Which compile-time or runtime rule decides the behavior of **state erasure enum**, and what evidence would distinguish the closest competing explanation? |
| [`08-sealed-state-parameter.rs`](08-sealed-state-parameter.rs) | Which compile-time or runtime rule decides the behavior of **sealed state parameter**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
