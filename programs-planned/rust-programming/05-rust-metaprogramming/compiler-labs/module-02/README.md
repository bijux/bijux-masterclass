# Compiler investigation — Module 42: Declarative Macro Matchers

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-42-declarative-macros-matchers-fragments-and-repetition/index.md)

This set tests whether the model from Module 42 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`case-01.rs`](case-01.rs) | Which compile-time or runtime rule decides the behavior of **expr and ty fragments delegate Rust grammar parsing**, and what evidence would distinguish the closest competing explanation? |
| [`case-02.rs`](case-02.rs) | Which compile-time or runtime rule decides the behavior of **literal fragments reject nonliteral expressions**, and what evidence would distinguish the closest competing explanation? |
| [`case-03.rs`](case-03.rs) | Which compile-time or runtime rule decides the behavior of **repetition can generate ordered statements from ordered input**, and what evidence would distinguish the closest competing explanation? |
| [`case-04.rs`](case-04.rs) | Which compile-time or runtime rule decides the behavior of **metavariables must appear at compatible repetition depth**, and what evidence would distinguish the closest competing explanation? |
| [`case-05.rs`](case-05.rs) | Which compile-time or runtime rule decides the behavior of **macro matching performs no arbitrary lookahead to resolve local ambiguity**, and what evidence would distinguish the closest competing explanation? |
| [`case-06.rs`](case-06.rs) | Which compile-time or runtime rule decides the behavior of **one repetition can support an optional trailing separator**, and what evidence would distinguish the closest competing explanation? |
| [`case-07.rs`](case-07.rs) | Which compile-time or runtime rule decides the behavior of **expr fragments have restricted safe followers**, and what evidence would distinguish the closest competing explanation? |
| [`case-08.rs`](case-08.rs) | Which compile-time or runtime rule decides the behavior of **caller expressions can be bound once before repeated use**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
