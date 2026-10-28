# Compiler investigation — Module 24: Static Polymorphism and Opaque Types

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-24-static-polymorphism-and-opaque-types/index.md)

This set tests whether the model from Module 24 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-method-specific-bound.rs`](01-method-specific-bound.rs) | Which compile-time or runtime rule decides the behavior of **method specific bound**, and what evidence would distinguish the closest competing explanation? |
| [`02-narrow-impl-bound.rs`](02-narrow-impl-bound.rs) | Which compile-time or runtime rule decides the behavior of **narrow impl bound**, and what evidence would distinguish the closest competing explanation? |
| [`03-independent-impl-trait-arguments.rs`](03-independent-impl-trait-arguments.rs) | Which compile-time or runtime rule decides the behavior of **independent impl trait arguments**, and what evidence would distinguish the closest competing explanation? |
| [`04-named-generic-equality.rs`](04-named-generic-equality.rs) | Which compile-time or runtime rule decides the behavior of **named generic equality**, and what evidence would distinguish the closest competing explanation? |
| [`05-opaque-branch-mismatch.rs`](05-opaque-branch-mismatch.rs) | Which compile-time or runtime rule decides the behavior of **opaque branch mismatch**, and what evidence would distinguish the closest competing explanation? |
| [`06-opaque-static-dispatch.rs`](06-opaque-static-dispatch.rs) | Which compile-time or runtime rule decides the behavior of **opaque static dispatch**, and what evidence would distinguish the closest competing explanation? |
| [`07-opaque-capability-limit.rs`](07-opaque-capability-limit.rs) | Which compile-time or runtime rule decides the behavior of **opaque capability limit**, and what evidence would distinguish the closest competing explanation? |
| [`08-generic-type-transition.rs`](08-generic-type-transition.rs) | Which compile-time or runtime rule decides the behavior of **generic type transition**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
