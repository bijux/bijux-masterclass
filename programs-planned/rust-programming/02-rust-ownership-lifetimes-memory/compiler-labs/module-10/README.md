# Compiler investigation — Module 20: Pinning and Address-Sensitive Design

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-20-pinning-and-address-sensitive-design/index.md)

This set tests whether the model from Module 20 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-normal-value-moves.rs`](01-normal-value-moves.rs) | Which compile-time or runtime rule decides the behavior of **normal value moves**, and what evidence would distinguish the closest competing explanation? |
| [`02-box-pin-phantom-pinned.rs`](02-box-pin-phantom-pinned.rs) | Which compile-time or runtime rule decides the behavior of **box pin phantom pinned**, and what evidence would distinguish the closest competing explanation? |
| [`03-get-mut-requires-unpin.rs`](03-get-mut-requires-unpin.rs) | Which compile-time or runtime rule decides the behavior of **get mut requires unpin**, and what evidence would distinguish the closest competing explanation? |
| [`04-pin-reborrow.rs`](04-pin-reborrow.rs) | Which compile-time or runtime rule decides the behavior of **pin reborrow**, and what evidence would distinguish the closest competing explanation? |
| [`05-stack-pin-escape.rs`](05-stack-pin-escape.rs) | Which compile-time or runtime rule decides the behavior of **stack pin escape**, and what evidence would distinguish the closest competing explanation? |
| [`06-move-out-of-pinned-box.rs`](06-move-out-of-pinned-box.rs) | Which compile-time or runtime rule decides the behavior of **move out of pinned box**, and what evidence would distinguish the closest competing explanation? |
| [`07-safe-address-token.rs`](07-safe-address-token.rs) | Which compile-time or runtime rule decides the behavior of **safe address token**, and what evidence would distinguish the closest competing explanation? |
| [`08-unnecessary-pin-compiles.rs`](08-unnecessary-pin-compiles.rs) | Which compile-time or runtime rule decides the behavior of **unnecessary pin compiles**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
