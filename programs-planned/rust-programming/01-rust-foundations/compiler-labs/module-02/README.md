# Compiler investigation — Module 2: Control Flow, Functions, and Invariants

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-02-control-flow-functions-and-invariants/index.md)

This set tests whether the model from Module 2 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-break-values-agree.rs`](01-break-values-agree.rs) | Which compile-time or runtime rule decides the behavior of **break values agree**, and what evidence would distinguish the closest competing explanation? |
| [`02-accumulator-needs-mutation.rs`](02-accumulator-needs-mutation.rs) | Which compile-time or runtime rule decides the behavior of **accumulator needs mutation**, and what evidence would distinguish the closest competing explanation? |
| [`03-while-needs-bool.rs`](03-while-needs-bool.rs) | Which compile-time or runtime rule decides the behavior of **while needs bool**, and what evidence would distinguish the closest competing explanation? |
| [`04-return-expression-lost.rs`](04-return-expression-lost.rs) | Which compile-time or runtime rule decides the behavior of **return expression lost**, and what evidence would distinguish the closest competing explanation? |
| [`05-loop-result-needs-context.rs`](05-loop-result-needs-context.rs) | Which compile-time or runtime rule decides the behavior of **loop result needs context**, and what evidence would distinguish the closest competing explanation? |
| [`06-range-end-is-exclusive.rs`](06-range-end-is-exclusive.rs) | Which compile-time or runtime rule decides the behavior of **range end is exclusive**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
