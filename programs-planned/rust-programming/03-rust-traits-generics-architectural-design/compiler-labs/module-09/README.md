# Compiler investigation — Module 29: Public API Evolution

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-29-public-api-evolution/index.md)

This set tests whether the model from Module 29 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-required-method-addition.rs`](01-required-method-addition.rs) | Which compile-time or runtime rule decides the behavior of **required method addition**, and what evidence would distinguish the closest competing explanation? |
| [`02-default-method-collision.rs`](02-default-method-collision.rs) | Which compile-time or runtime rule decides the behavior of **default method collision**, and what evidence would distinguish the closest competing explanation? |
| [`03-new-supertrait-obligation.rs`](03-new-supertrait-obligation.rs) | Which compile-time or runtime rule decides the behavior of **new supertrait obligation**, and what evidence would distinguish the closest competing explanation? |
| [`04-blanket-impl-downstream-conflict.rs`](04-blanket-impl-downstream-conflict.rs) | Which compile-time or runtime rule decides the behavior of **blanket impl downstream conflict**, and what evidence would distinguish the closest competing explanation? |
| [`05-sealed-compatibility-surface.rs`](05-sealed-compatibility-surface.rs) | Which compile-time or runtime rule decides the behavior of **sealed compatibility surface**, and what evidence would distinguish the closest competing explanation? |
| [`06-nonexhaustive-matching.rs`](06-nonexhaustive-matching.rs) | Which compile-time or runtime rule decides the behavior of **nonexhaustive matching**, and what evidence would distinguish the closest competing explanation? |
| [`07-version-adapter.rs`](07-version-adapter.rs) | Which compile-time or runtime rule decides the behavior of **version adapter**, and what evidence would distinguish the closest competing explanation? |
| [`08-strengthened-bound.rs`](08-strengthened-bound.rs) | Which compile-time or runtime rule decides the behavior of **strengthened bound**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
