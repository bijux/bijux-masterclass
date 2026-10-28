# Compiler investigation — Module 28: Boundary Traits and Adapters

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-28-boundary-traits-and-adapters/index.md)

This set tests whether the model from Module 28 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-blanket-extension.rs`](01-blanket-extension.rs) | Which compile-time or runtime rule decides the behavior of **blanket extension**, and what evidence would distinguish the closest competing explanation? |
| [`02-extension-import.rs`](02-extension-import.rs) | Which compile-time or runtime rule decides the behavior of **extension import**, and what evidence would distinguish the closest competing explanation? |
| [`03-fn-versus-fnmut.rs`](03-fn-versus-fnmut.rs) | Which compile-time or runtime rule decides the behavior of **fn versus fnmut**, and what evidence would distinguish the closest competing explanation? |
| [`04-tryfrom-validation.rs`](04-tryfrom-validation.rs) | Which compile-time or runtime rule decides the behavior of **tryfrom validation**, and what evidence would distinguish the closest competing explanation? |
| [`05-generic-port-associated-error.rs`](05-generic-port-associated-error.rs) | Which compile-time or runtime rule decides the behavior of **generic port associated error**, and what evidence would distinguish the closest competing explanation? |
| [`06-trait-object-associated-error.rs`](06-trait-object-associated-error.rs) | Which compile-time or runtime rule decides the behavior of **trait object associated error**, and what evidence would distinguish the closest competing explanation? |
| [`07-behavioral-fake.rs`](07-behavioral-fake.rs) | Which compile-time or runtime rule decides the behavior of **behavioral fake**, and what evidence would distinguish the closest competing explanation? |
| [`08-bound-placement.rs`](08-bound-placement.rs) | Which compile-time or runtime rule decides the behavior of **bound placement**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
