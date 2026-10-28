# Compiler investigation — Module 3: Ownership, Moves, Copying, and Destruction

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-03-ownership-moves-copying-and-destruction/index.md)

This set tests whether the model from Module 3 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-assignment-moves-string.rs`](01-assignment-moves-string.rs) | Which compile-time or runtime rule decides the behavior of **assignment moves string**, and what evidence would distinguish the closest competing explanation? |
| [`02-function-consumes-argument.rs`](02-function-consumes-argument.rs) | Which compile-time or runtime rule decides the behavior of **function consumes argument**, and what evidence would distinguish the closest competing explanation? |
| [`03-partial-move.rs`](03-partial-move.rs) | Which compile-time or runtime rule decides the behavior of **partial move**, and what evidence would distinguish the closest competing explanation? |
| [`04-copy-versus-owned-tuple.rs`](04-copy-versus-owned-tuple.rs) | Which compile-time or runtime rule decides the behavior of **copy versus owned tuple**, and what evidence would distinguish the closest competing explanation? |
| [`05-loop-move.rs`](05-loop-move.rs) | Which compile-time or runtime rule decides the behavior of **loop move**, and what evidence would distinguish the closest competing explanation? |
| [`06-explicit-drop.rs`](06-explicit-drop.rs) | Which compile-time or runtime rule decides the behavior of **explicit drop**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
