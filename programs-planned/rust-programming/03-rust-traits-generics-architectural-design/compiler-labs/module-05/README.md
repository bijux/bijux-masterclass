# Compiler investigation — Module 25: Trait Objects and Dynamic Polymorphism

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-25-trait-objects-and-dynamic-polymorphism/index.md)

This set tests whether the model from Module 25 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-explicit-dyn.rs`](01-explicit-dyn.rs) | Which compile-time or runtime rule decides the behavior of **explicit dyn**, and what evidence would distinguish the closest competing explanation? |
| [`02-generic-method-dyn-incompatibility.rs`](02-generic-method-dyn-incompatibility.rs) | Which compile-time or runtime rule decides the behavior of **generic method dyn incompatibility**, and what evidence would distinguish the closest competing explanation? |
| [`03-self-return-dyn-incompatibility.rs`](03-self-return-dyn-incompatibility.rs) | Which compile-time or runtime rule decides the behavior of **self return dyn incompatibility**, and what evidence would distinguish the closest competing explanation? |
| [`04-associated-constant-dyn-incompatibility.rs`](04-associated-constant-dyn-incompatibility.rs) | Which compile-time or runtime rule decides the behavior of **associated constant dyn incompatibility**, and what evidence would distinguish the closest competing explanation? |
| [`05-associated-type-specification.rs`](05-associated-type-specification.rs) | Which compile-time or runtime rule decides the behavior of **associated type specification**, and what evidence would distinguish the closest competing explanation? |
| [`06-self-sized-escape.rs`](06-self-sized-escape.rs) | Which compile-time or runtime rule decides the behavior of **self sized escape**, and what evidence would distinguish the closest competing explanation? |
| [`07-borrowed-object-lifetime.rs`](07-borrowed-object-lifetime.rs) | Which compile-time or runtime rule decides the behavior of **borrowed object lifetime**, and what evidence would distinguish the closest competing explanation? |
| [`08-heterogeneous-registry.rs`](08-heterogeneous-registry.rs) | Which compile-time or runtime rule decides the behavior of **heterogeneous registry**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
