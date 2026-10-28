# Compiler investigation — Module 26: Composition Without Inheritance

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-26-composition-and-oop-style-design-without-inheritance/index.md)

This set tests whether the model from Module 26 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-private-invariant.rs`](01-private-invariant.rs) | Which compile-time or runtime rule decides the behavior of **private invariant**, and what evidence would distinguish the closest competing explanation? |
| [`02-private-field-construction.rs`](02-private-field-construction.rs) | Which compile-time or runtime rule decides the behavior of **private field construction**, and what evidence would distinguish the closest competing explanation? |
| [`03-generic-delegation.rs`](03-generic-delegation.rs) | Which compile-time or runtime rule decides the behavior of **generic delegation**, and what evidence would distinguish the closest competing explanation? |
| [`04-recursive-wrapper-sizing.rs`](04-recursive-wrapper-sizing.rs) | Which compile-time or runtime rule decides the behavior of **recursive wrapper sizing**, and what evidence would distinguish the closest competing explanation? |
| [`05-closed-command-enum.rs`](05-closed-command-enum.rs) | Which compile-time or runtime rule decides the behavior of **closed command enum**, and what evidence would distinguish the closest competing explanation? |
| [`06-nonexhaustive-state-handling.rs`](06-nonexhaustive-state-handling.rs) | Which compile-time or runtime rule decides the behavior of **nonexhaustive state handling**, and what evidence would distinguish the closest competing explanation? |
| [`07-unmet-composition-bound.rs`](07-unmet-composition-bound.rs) | Which compile-time or runtime rule decides the behavior of **unmet composition bound**, and what evidence would distinguish the closest competing explanation? |
| [`08-capability-intersection.rs`](08-capability-intersection.rs) | Which compile-time or runtime rule decides the behavior of **capability intersection**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
