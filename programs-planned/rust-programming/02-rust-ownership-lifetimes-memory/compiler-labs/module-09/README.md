# Compiler investigation — Module 19: Subtyping, Variance, PhantomData, and Drop Checking

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-19-subtyping-variance-phantomdata-and-drop-checking/index.md)

This set tests whether the model from Module 19 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-lifetime-shortening.rs`](01-lifetime-shortening.rs) | Which compile-time or runtime rule decides the behavior of **lifetime shortening**, and what evidence would distinguish the closest competing explanation? |
| [`02-mut-reference-invariance.rs`](02-mut-reference-invariance.rs) | Which compile-time or runtime rule decides the behavior of **mut reference invariance**, and what evidence would distinguish the closest competing explanation? |
| [`03-cell-invariance.rs`](03-cell-invariance.rs) | Which compile-time or runtime rule decides the behavior of **cell invariance**, and what evidence would distinguish the closest competing explanation? |
| [`04-function-argument-contravariance.rs`](04-function-argument-contravariance.rs) | Which compile-time or runtime rule decides the behavior of **function argument contravariance**, and what evidence would distinguish the closest competing explanation? |
| [`05-owned-t-outlives.rs`](05-owned-t-outlives.rs) | Which compile-time or runtime rule decides the behavior of **owned t outlives**, and what evidence would distinguish the closest competing explanation? |
| [`06-destructor-keeps-borrow-live.rs`](06-destructor-keeps-borrow-live.rs) | Which compile-time or runtime rule decides the behavior of **destructor keeps borrow live**, and what evidence would distinguish the closest competing explanation? |
| [`07-invariant-marker-size.rs`](07-invariant-marker-size.rs) | Which compile-time or runtime rule decides the behavior of **invariant marker size**, and what evidence would distinguish the closest competing explanation? |
| [`08-cross-brand-id.rs`](08-cross-brand-id.rs) | Which compile-time or runtime rule decides the behavior of **cross brand id**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
