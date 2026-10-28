# Compiler investigation — Module 10: Integration and Independent Change

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-10-integration-and-independent-change/index.md)

This set tests whether the model from Module 10 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-move-into-command.rs`](01-move-into-command.rs) | Which compile-time or runtime rule decides the behavior of **move into command**, and what evidence would distinguish the closest competing explanation? |
| [`02-shared-view-blocks-mutation.rs`](02-shared-view-blocks-mutation.rs) | Which compile-time or runtime rule decides the behavior of **shared view blocks mutation**, and what evidence would distinguish the closest competing explanation? |
| [`03-iterator-terminal-consumes.rs`](03-iterator-terminal-consumes.rs) | Which compile-time or runtime rule decides the behavior of **iterator terminal consumes**, and what evidence would distinguish the closest competing explanation? |
| [`04-generic-sort-bound.rs`](04-generic-sort-bound.rs) | Which compile-time or runtime rule decides the behavior of **generic sort bound**, and what evidence would distinguish the closest competing explanation? |
| [`05-incompatible-iterator-branches.rs`](05-incompatible-iterator-branches.rs) | Which compile-time or runtime rule decides the behavior of **incompatible iterator branches**, and what evidence would distinguish the closest competing explanation? |
| [`06-local-rendered-output.rs`](06-local-rendered-output.rs) | Which compile-time or runtime rule decides the behavior of **local rendered output**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
