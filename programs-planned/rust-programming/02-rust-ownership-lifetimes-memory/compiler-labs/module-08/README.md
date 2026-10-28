# Compiler investigation — Module 18: Memory Representation, Validity, and Layout

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-18-memory-representation-validity-and-layout/index.md)

This set tests whether the model from Module 18 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-repr-c-layout.rs`](01-repr-c-layout.rs) | Which compile-time or runtime rule decides the behavior of **repr c layout**, and what evidence would distinguish the closest competing explanation? |
| [`02-default-layout-observation.rs`](02-default-layout-observation.rs) | Which compile-time or runtime rule decides the behavior of **default layout observation**, and what evidence would distinguish the closest competing explanation? |
| [`03-unsized-local.rs`](03-unsized-local.rs) | Which compile-time or runtime rule decides the behavior of **unsized local**, and what evidence would distinguish the closest competing explanation? |
| [`04-size-of-val-slice.rs`](04-size-of-val-slice.rs) | Which compile-time or runtime rule decides the behavior of **size of val slice**, and what evidence would distinguish the closest competing explanation? |
| [`05-owner-versus-payload.rs`](05-owner-versus-payload.rs) | Which compile-time or runtime rule decides the behavior of **owner versus payload**, and what evidence would distinguish the closest competing explanation? |
| [`06-zero-sized-values.rs`](06-zero-sized-values.rs) | Which compile-time or runtime rule decides the behavior of **zero sized values**, and what evidence would distinguish the closest competing explanation? |
| [`07-option-size-observations.rs`](07-option-size-observations.rs) | Which compile-time or runtime rule decides the behavior of **option size observations**, and what evidence would distinguish the closest competing explanation? |
| [`08-transmute-requires-unsafe.rs`](08-transmute-requires-unsafe.rs) | Which compile-time or runtime rule decides the behavior of **transmute requires unsafe**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
