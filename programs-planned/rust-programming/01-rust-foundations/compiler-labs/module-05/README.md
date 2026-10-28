# Compiler investigation — Module 5: Structs, Enums, Methods, and Pattern Matching

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-05-structs-enums-methods-and-pattern-matching/index.md)

This set tests whether the model from Module 5 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-private-newtype-field.rs`](01-private-newtype-field.rs) | Which compile-time or runtime rule decides the behavior of **private newtype field**, and what evidence would distinguish the closest competing explanation? |
| [`02-non-exhaustive-match.rs`](02-non-exhaustive-match.rs) | Which compile-time or runtime rule decides the behavior of **non exhaustive match**, and what evidence would distinguish the closest competing explanation? |
| [`03-moved-enum-payload.rs`](03-moved-enum-payload.rs) | Which compile-time or runtime rule decides the behavior of **moved enum payload**, and what evidence would distinguish the closest competing explanation? |
| [`04-option-is-not-sentinel.rs`](04-option-is-not-sentinel.rs) | Which compile-time or runtime rule decides the behavior of **option is not sentinel**, and what evidence would distinguish the closest competing explanation? |
| [`05-method-receiver-mismatch.rs`](05-method-receiver-mismatch.rs) | Which compile-time or runtime rule decides the behavior of **method receiver mismatch**, and what evidence would distinguish the closest competing explanation? |
| [`06-let-else-diverges.rs`](06-let-else-diverges.rs) | Which compile-time or runtime rule decides the behavior of **let else diverges**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
