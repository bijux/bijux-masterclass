# Compiler investigation — Module 7: Errors, Parsing, Files, and Persistence

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-07-errors-parsing-files-and-persistence/index.md)

This set tests whether the model from Module 7 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-question-mark-needs-result.rs`](01-question-mark-needs-result.rs) | Which compile-time or runtime rule decides the behavior of **question mark needs result**, and what evidence would distinguish the closest competing explanation? |
| [`02-option-question-mark-in-result.rs`](02-option-question-mark-in-result.rs) | Which compile-time or runtime rule decides the behavior of **option question mark in result**, and what evidence would distinguish the closest competing explanation? |
| [`03-error-source-type.rs`](03-error-source-type.rs) | Which compile-time or runtime rule decides the behavior of **error source type**, and what evidence would distinguish the closest competing explanation? |
| [`04-use-after-partial-parse-move.rs`](04-use-after-partial-parse-move.rs) | Which compile-time or runtime rule decides the behavior of **use after partial parse move**, and what evidence would distinguish the closest competing explanation? |
| [`05-writer-must-be-mutable.rs`](05-writer-must-be-mutable.rs) | Which compile-time or runtime rule decides the behavior of **writer must be mutable**, and what evidence would distinguish the closest competing explanation? |
| [`06-swallowed-error.rs`](06-swallowed-error.rs) | Which compile-time or runtime rule decides the behavior of **swallowed error**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
