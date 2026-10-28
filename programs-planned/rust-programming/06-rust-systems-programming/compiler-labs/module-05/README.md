# Compiler investigation — Module 55: Unsafe Rust as a Proof Boundary

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-55-unsafe-rust-and-safety-proofs/index.md)

This set tests whether the model from Module 55 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`case-01.rs`](case-01.rs) | Which compile-time or runtime rule decides the behavior of **raw-pointer dereference requires an explicit unsafe block**, and what evidence would distinguish the closest competing explanation? |
| [`case-02.rs`](case-02.rs) | Which compile-time or runtime rule decides the behavior of **unsafe functions still use explicit unsafe blocks under the 2024 discipline**, and what evidence would distinguish the closest competing explanation? |
| [`case-03.rs`](case-03.rs) | Which compile-time or runtime rule decides the behavior of **unsafe trait implementation carries an explicit implementor promise**, and what evidence would distinguish the closest competing explanation? |
| [`case-04.rs`](case-04.rs) | Which compile-time or runtime rule decides the behavior of **unsafe attributes expose global symbol obligations**, and what evidence would distinguish the closest competing explanation? |
| [`case-05.rs`](case-05.rs) | Which compile-time or runtime rule decides the behavior of **raw-pointer dereference is an unsafe operation**, and what evidence would distinguish the closest competing explanation? |
| [`case-06.rs`](case-06.rs) | Which compile-time or runtime rule decides the behavior of **calling an unsafe function requires an unsafe context**, and what evidence would distinguish the closest competing explanation? |
| [`case-07.rs`](case-07.rs) | Which compile-time or runtime rule decides the behavior of **unsafe operations are not implicitly allowed inside `unsafe fn`**, and what evidence would distinguish the closest competing explanation? |
| [`case-08.rs`](case-08.rs) | Which compile-time or runtime rule decides the behavior of **`no_mangle` is an unsafe attribute in Rust 2024**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
