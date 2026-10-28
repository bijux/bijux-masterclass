# Compiler investigation — Module 16: Rc, Weak, and Ownership Graphs

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-16-rc-weak-and-ownership-graphs/index.md)

This set tests whether the model from Module 16 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-rc-owner-clone.rs`](01-rc-owner-clone.rs) | Which compile-time or runtime rule decides the behavior of **rc owner clone**, and what evidence would distinguish the closest competing explanation? |
| [`02-rc-deep-clone.rs`](02-rc-deep-clone.rs) | Which compile-time or runtime rule decides the behavior of **rc deep clone**, and what evidence would distinguish the closest competing explanation? |
| [`03-mutate-shared-rc.rs`](03-mutate-shared-rc.rs) | Which compile-time or runtime rule decides the behavior of **mutate shared rc**, and what evidence would distinguish the closest competing explanation? |
| [`04-get-mut-unique.rs`](04-get-mut-unique.rs) | Which compile-time or runtime rule decides the behavior of **get mut unique**, and what evidence would distinguish the closest competing explanation? |
| [`05-make-mut-diverges.rs`](05-make-mut-diverges.rs) | Which compile-time or runtime rule decides the behavior of **make mut diverges**, and what evidence would distinguish the closest competing explanation? |
| [`06-weak-expiration.rs`](06-weak-expiration.rs) | Which compile-time or runtime rule decides the behavior of **weak expiration**, and what evidence would distinguish the closest competing explanation? |
| [`07-strong-cycle-compiles.rs`](07-strong-cycle-compiles.rs) | Which compile-time or runtime rule decides the behavior of **strong cycle compiles**, and what evidence would distinguish the closest competing explanation? |
| [`08-value-versus-pointer-equality.rs`](08-value-versus-pointer-equality.rs) | Which compile-time or runtime rule decides the behavior of **value versus pointer equality**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
