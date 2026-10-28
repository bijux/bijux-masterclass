# Compiler investigation — Module 30: Architectural Synthesis

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-30-architectural-synthesis/index.md)

This set tests whether the model from Module 30 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-hybrid-dispatch.rs`](01-hybrid-dispatch.rs) | Which compile-time or runtime rule decides the behavior of **hybrid dispatch**, and what evidence would distinguish the closest competing explanation? |
| [`02-hybrid-associated-type-mismatch.rs`](02-hybrid-associated-type-mismatch.rs) | Which compile-time or runtime rule decides the behavior of **hybrid associated type mismatch**, and what evidence would distinguish the closest competing explanation? |
| [`03-registry-dyn-compatibility.rs`](03-registry-dyn-compatibility.rs) | Which compile-time or runtime rule decides the behavior of **registry dyn compatibility**, and what evidence would distinguish the closest competing explanation? |
| [`04-builder-state-gate.rs`](04-builder-state-gate.rs) | Which compile-time or runtime rule decides the behavior of **builder state gate**, and what evidence would distinguish the closest competing explanation? |
| [`05-coherence-adapter-need.rs`](05-coherence-adapter-need.rs) | Which compile-time or runtime rule decides the behavior of **coherence adapter need**, and what evidence would distinguish the closest competing explanation? |
| [`06-opaque-report-view.rs`](06-opaque-report-view.rs) | Which compile-time or runtime rule decides the behavior of **opaque report view**, and what evidence would distinguish the closest competing explanation? |
| [`07-object-lifetime-in-registry.rs`](07-object-lifetime-in-registry.rs) | Which compile-time or runtime rule decides the behavior of **object lifetime in registry**, and what evidence would distinguish the closest competing explanation? |
| [`08-sealed-integrated-extension.rs`](08-sealed-integrated-extension.rs) | Which compile-time or runtime rule decides the behavior of **sealed integrated extension**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
