# Compiler investigation — Module 39: Combinator APIs, Laws, and Cost Models

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-39-combinator-laws-and-cost-models/index.md)

This set tests whether the model from Module 39 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`case-01.rs`](case-01.rs) | Which compile-time or runtime rule decides the behavior of **predicate composition can retain short-circuit semantics**, and what evidence would distinguish the closest competing explanation? |
| [`case-02.rs`](case-02.rs) | Which compile-time or runtime rule decides the behavior of **different closure expressions have distinct concrete types**, and what evidence would distinguish the closest competing explanation? |
| [`case-03.rs`](case-03.rs) | Which compile-time or runtime rule decides the behavior of **placing runtime choice inside one closure preserves one closure type**, and what evidence would distinguish the closest competing explanation? |
| [`case-04.rs`](case-04.rs) | Which compile-time or runtime rule decides the behavior of **a context adapter can preserve the source error type**, and what evidence would distinguish the closest competing explanation? |
| [`case-05.rs`](case-05.rs) | Which compile-time or runtime rule decides the behavior of **a stateful predicate does not satisfy an Fn-only combinator contract**, and what evidence would distinguish the closest competing explanation? |
| [`case-06.rs`](case-06.rs) | Which compile-time or runtime rule decides the behavior of **normalization idempotence can be tested as a law on a bounded domain**, and what evidence would distinguish the closest competing explanation? |
| [`case-07.rs`](case-07.rs) | Which compile-time or runtime rule decides the behavior of **lazy and eager APIs can coexist with distinct names and return shapes**, and what evidence would distinguish the closest competing explanation? |
| [`case-08.rs`](case-08.rs) | Which compile-time or runtime rule decides the behavior of **one closure expression has one inferred parameter and return type**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
