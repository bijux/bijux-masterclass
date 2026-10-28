# Compiler investigation — Module 21: Traits as Behavioral Contracts

[Compiler-investigation method](../README.md) · [Module chapter](../../course-book/module-21-traits-as-behavioral-contracts/index.md)

This set tests whether the model from Module 21 survives contact with small, adversarial programs. Predict each specimen without opening the machine-readable manifest or the module solutions.

| Specimen | Question to resolve before compiling |
|---|---|
| [`01-trait-import.rs`](01-trait-import.rs) | Which compile-time or runtime rule decides the behavior of **trait import**, and what evidence would distinguish the closest competing explanation? |
| [`02-missing-generic-bound.rs`](02-missing-generic-bound.rs) | Which compile-time or runtime rule decides the behavior of **missing generic bound**, and what evidence would distinguish the closest competing explanation? |
| [`03-default-method.rs`](03-default-method.rs) | Which compile-time or runtime rule decides the behavior of **default method**, and what evidence would distinguish the closest competing explanation? |
| [`04-ambiguous-method.rs`](04-ambiguous-method.rs) | Which compile-time or runtime rule decides the behavior of **ambiguous method**, and what evidence would distinguish the closest competing explanation? |
| [`05-self-sized-boundary.rs`](05-self-sized-boundary.rs) | Which compile-time or runtime rule decides the behavior of **self sized boundary**, and what evidence would distinguish the closest competing explanation? |
| [`06-supertrait-obligation.rs`](06-supertrait-obligation.rs) | Which compile-time or runtime rule decides the behavior of **supertrait obligation**, and what evidence would distinguish the closest competing explanation? |
| [`07-conditional-implementation.rs`](07-conditional-implementation.rs) | Which compile-time or runtime rule decides the behavior of **conditional implementation**, and what evidence would distinguish the closest competing explanation? |
| [`08-consuming-receiver.rs`](08-consuming-receiver.rs) | Which compile-time or runtime rule decides the behavior of **consuming receiver**, and what evidence would distinguish the closest competing explanation? |

## Work through the set

For each file, draw or write the smallest model that can decide it: types and expression results, owners and loans, trait obligations, iterator state, macro phase, raw-memory obligations, or operating-system boundary state. Then classify the outcome and name the first causal rule.

Compile only after the prediction is complete. A correct pass/fail guess with the wrong cause is not a successful investigation. When several errors appear, identify which one would remain after secondary errors were removed.

## Repair and transfer

Repair one rejecting or behaviorally defective specimen without deleting the requirement it was designed to express. Preserve the original product need while changing only the mechanism that violated it.

Next, alter one assumption—ownership mode, lifetime source, trait bound, adapter order, macro input, or boundary condition. Predict the result before compiling.

Finish by stating how the same rule constrains the module laboratory or cumulative capstone. This connects an isolated diagnostic to a real design decision.
