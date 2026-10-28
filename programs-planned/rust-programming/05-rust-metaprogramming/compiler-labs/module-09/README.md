# Compiler investigation — Module 49: Function-Like Procedural Macros and Typed DSLs

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-49-function-like-procedural-macros-and-typed-dsls/index.md)

This set tests whether the model from Module 49 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`case-01/`](case-01) | Which compile-time or runtime rule decides the behavior of **function-like procedural macros can parse a custom comma-separated grammar**, and what evidence would distinguish the closest competing explanation? |
| [`case-02/`](case-02) | Which compile-time or runtime rule decides the behavior of **cross-entry uniqueness is a semantic validation rule**, and what evidence would distinguish the closest competing explanation? |
| [`case-03/`](case-03) | Which compile-time or runtime rule decides the behavior of **explicit separators are part of a DSL grammar**, and what evidence would distinguish the closest competing explanation? |
| [`case-04/`](case-04) | Which compile-time or runtime rule decides the behavior of **an empty grammar can have a deliberate normalized result**, and what evidence would distinguish the closest competing explanation? |
| [`case-05/`](case-05) | Which compile-time or runtime rule decides the behavior of **the emitted value still has an ordinary Rust type**, and what evidence would distinguish the closest competing explanation? |
| [`case-06/`](case-06) | Which compile-time or runtime rule decides the behavior of **normalized generation can preserve authored source order**, and what evidence would distinguish the closest competing explanation? |
| [`case-07/`](case-07) | Which compile-time or runtime rule decides the behavior of **a DSL parser should reject unsupported literal categories locally**, and what evidence would distinguish the closest competing explanation? |
| [`case-08/`](case-08) | Which compile-time or runtime rule decides the behavior of **generated static data can be consumed through ordinary iterator APIs**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
