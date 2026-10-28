# Compiler investigation — Module 12: Lifetime Relationships and Borrowed APIs

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-12-lifetime-relationships-and-borrowed-apis/index.md)

This set tests whether the model from Module 12 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-single-source-elision.rs`](01-single-source-elision.rs) | Which compile-time or runtime rule decides the behavior of **single source elision**, and what evidence would distinguish the closest competing explanation? |
| [`02-ambiguous-output-source.rs`](02-ambiguous-output-source.rs) | Which compile-time or runtime rule decides the behavior of **ambiguous output source**, and what evidence would distinguish the closest competing explanation? |
| [`03-independent-choice-enum.rs`](03-independent-choice-enum.rs) | Which compile-time or runtime rule decides the behavior of **independent choice enum**, and what evidence would distinguish the closest competing explanation? |
| [`04-reference-to-local.rs`](04-reference-to-local.rs) | Which compile-time or runtime rule decides the behavior of **reference to local**, and what evidence would distinguish the closest competing explanation? |
| [`05-explicit-shortening.rs`](05-explicit-shortening.rs) | Which compile-time or runtime rule decides the behavior of **explicit shortening**, and what evidence would distinguish the closest competing explanation? |
| [`06-temporary-dropped-too-soon.rs`](06-temporary-dropped-too-soon.rs) | Which compile-time or runtime rule decides the behavior of **temporary dropped too soon**, and what evidence would distinguish the closest competing explanation? |
| [`07-owned-type-static-bound.rs`](07-owned-type-static-bound.rs) | Which compile-time or runtime rule decides the behavior of **owned type static bound**, and what evidence would distinguish the closest competing explanation? |
| [`08-view-outlives-owner.rs`](08-view-outlives-owner.rs) | Which compile-time or runtime rule decides the behavior of **view outlives owner**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
