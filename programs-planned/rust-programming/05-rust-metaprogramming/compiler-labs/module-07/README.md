# Compiler investigation — Module 47: Custom Derive Macros

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-47-custom-derive-macros-and-structural-generation/index.md)

This set tests whether the model from Module 47 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`case-01/`](case-01) | Which compile-time or runtime rule decides the behavior of **derive macros can preserve generic parameters without adding unrelated bounds**, and what evidence would distinguish the closest competing explanation? |
| [`case-02/`](case-02) | Which compile-time or runtime rule decides the behavior of **derive input includes enum declarations as well as structs**, and what evidence would distinguish the closest competing explanation? |
| [`case-03/`](case-03) | Which compile-time or runtime rule decides the behavior of **derive-generated associated items use ordinary Rust namespaces**, and what evidence would distinguish the closest competing explanation? |
| [`case-04/`](case-04) | Which compile-time or runtime rule decides the behavior of **a structural derive can generate metadata without field-type trait bounds**, and what evidence would distinguish the closest competing explanation? |
| [`case-05/`](case-05) | Which compile-time or runtime rule decides the behavior of **a derive should reject unsupported input explicitly**, and what evidence would distinguish the closest competing explanation? |
| [`case-06/`](case-06) | Which compile-time or runtime rule decides the behavior of **existing where clauses are preserved in generated implementations**, and what evidence would distinguish the closest competing explanation? |
| [`case-07/`](case-07) | Which compile-time or runtime rule decides the behavior of **derive output is subject to ordinary generic well-formedness**, and what evidence would distinguish the closest competing explanation? |
| [`case-08/`](case-08) | Which compile-time or runtime rule decides the behavior of **unit structs have a defined zero-field structural result**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
