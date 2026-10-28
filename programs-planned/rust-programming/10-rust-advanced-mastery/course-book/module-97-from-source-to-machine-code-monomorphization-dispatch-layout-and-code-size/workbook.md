# Workbook — Module 97: From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size

[Chapter](index.md) · [Laboratory](../../labs/module-07-dispatch-observatory/README.md) · [AxiomStore guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size** has become a usable model rather than remembered vocabulary. Its governing question is: *How do type-level architecture and compiler decisions become concrete symbols, call paths, layouts, and artifact size—and which observations are stable enough to guide design?* Preserve your first prediction and record decisive facts in a **source-to-artifact observation**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 96 — Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do type-level architecture and compiler decisions become concrete symbols, call paths, layouts, and artifact size—and which observations are stable enough to guide design?**
3. Draw the smallest **source-to-artifact observation** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each case, submit: expected category (`compile-pass`, `compile-fail`, `run-pass`, `run-fail`, or `manual-review`), first decisive phase or event, governing relationship, and the strongest conclusion the outcome would justify.

Your prediction sheet must make the source-to-artifact observation record visible. For one case, change exactly one assumption and explain why the decisive phase or outcome moves.

### Prediction 1 — Generic instances

A generic function is called with `u32` in two modules and `u64` once. Predict the possible source-level instantiations and why visible symbols may differ from that count.

### Prediction 2 — Trait-object call cost

A hot loop calls `&dyn Score`. Can source alone establish that the indirect call dominates runtime?

### Prediction 3 — repr(C) size claim

A struct gains `repr(C)` and becomes smaller on one target. Is smaller size a guarantee?

### Prediction 4 — Vanished helper

A helper has no symbol in an optimized binary. What can be concluded?

## Part 2 — Diagnose and repair

Each repair must leave a more precise source-to-artifact observation record. Reject fixes that merely erase the type, lifetime, state, compatibility, or artifact fact that the exercise is designed to expose.

### Repair 1 — Generic equals duplication

A review declares that every generic call creates duplicate machine code.

Required direction: Inventory concrete reachable instantiations and inspect one pinned artifact; record compiler transformations and avoid universal claims.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the source-to-artifact observation record changes.

### Repair 2 — Dynamic dispatch equals heap

A design rejects `dyn Trait` because it assumes every object allocates.

Required direction: Separate dispatch from ownership. Borrowed trait objects need no heap allocation; boxed ownership is a separate choice.

For **Repair 2 — Dynamic dispatch equals heap**, submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the source-to-artifact observation record changes.

### Repair 3 — Layout observation becomes format

A serialized format writes native struct bytes after observing a convenient layout.

Required direction: Use explicit encoding. Target layout is not a durable wire format unless a precise stable representation contract exists.

For **Repair 3 — Layout observation becomes format**, submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the source-to-artifact observation record changes.

## Part 3 — Focused exercises

### Exercise 1 — Dispatch parity

Implement generic, enum, and trait-object paths with one semantic oracle.

Completion standard: All variants produce identical results before measurement.

### Exercise 2 — Artifact record

Inspect symbols and assembly under two profiles.

Completion standard: Every observation includes toolchain, target, features, and expiry condition.

### Exercise 3 — Layout notebook

Record size/alignment observations and separate them from guarantees.

Completion standard: No target observation is described as portable Rust semantics.

### Exercise 4 — Size attribution

Add one generic instantiation and one formatting path, then compare artifact contributions.

Completion standard: The report avoids blaming an abstraction without symbol/section evidence.

### Cross-course transfer

Choose one artifact from Courses 1–10 and reassess it through **From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size**. Reconstruct its current invariant owner, then decide whether the source-to-artifact observation record reveals a genuine defect. A justified no-change decision is valid when the advanced mechanism would add proof or compatibility cost without removing a real invalid state.

### Applied case study — choosing dispatch with two artifacts

A rule engine has twelve tiny built-in rules called in a hot loop and an optional runtime plugin directory. Release measurements show the generic built-in path produces a larger binary, while a synthetic benchmark reports a small throughput advantage. A maintainer proposes converting all rules to trait objects to reduce code size. Another proposes genericizing the plugin path.

Design an experiment that preserves semantic parity. Define the generic, enum, and dynamic variants; specify the same workload, input distribution, compiler profile, target, and correctness oracle. Record call count, binary or section size, and latency separately. Explain why source lines, number of trait implementations, and debug-build timing are not adequate proxies.

Then make an architectural decision rather than a benchmark-only decision. Which boundary should use static dispatch, which should use dynamic dispatch, and what evidence could reverse the choice? Include the effects of inlining, monomorphization, branch prediction, plugin openness, compile time, and public API evolution. End by classifying every conclusion as a language fact, library design decision, or artifact observation.

### Interleaved reasoning pass

1. For **Explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the source-to-artifact observation.
2. For **Compare static dispatch, enum dispatch, and trait-object dispatch through behavior, extension model, call shape, and measured artifact cost**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the source-to-artifact observation.
3. For **Inspect symbols, section sizes, assembly, and layout observations for one pinned target and profile without claiming portability**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the source-to-artifact observation.
4. For **Identify where inlining, dead-code elimination, link-time optimization, and codegen units can obscure naïve source-to-symbol expectations**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the source-to-artifact observation.

5. Identify one guarantee from an earlier course that a careless implementation of **From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Dispatch Observatory](../../labs/module-07-dispatch-observatory/README.md) from its `starter/` package.

Build static, enum, and dynamic scoring paths over one oracle, then produce a pinned artifact observation that distinguishes dispatch, ownership, and code-size effects.

Before implementation, freeze Dispatch Observatory’s public behavior and the source-to-artifact observation record. After implementation, complete its transfer task in a domain with different ownership, version, capacity, extension, or failure policy; renaming types does not demonstrate transfer.

### Laboratory acceptance trace

Before opening the reference implementation for **Dispatch Observatory**, record:

- the public behavior that demonstrates **Explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Compare AxiomStore’s const-specialized codec paths and dynamically dispatched validators without changing semantics. Record one artifact-specific conclusion and retain the generic/dynamic architecture only if product requirements, not folklore, justify it.

Update AxiomStore’s source-to-artifact observation record before code. Record the changed invariant owner, new failure paths, compatibility effect, and falsifying evidence. Then run the full capstone route because this module can invalidate guarantees outside its local file.

### Evidence quality review

Before leaving the module, compare the source-level cost story you expected with the artifact you actually inspected. Separate call-path, symbol, layout, and size observations; name the profile and target; and record one optimization conclusion you refuse to generalize. The reflection should end with an architecture decision that remains unchanged despite the artifact result.

### Capstone invariant trace

For the Module 97 AxiomStore increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Explain one semantic guarantee and one artifact observation about the same code, then state why neither can replace the other.

Finish without notes by reconstructing the source-to-artifact observation record. Name the requirement, the simpler design, the decisive rejected construction, the state after failure, and the evidence that could falsify your claim. End by stating one condition under which this mechanism should be removed.

The defense is complete only when another reader can reproduce the reasoning behind Dispatch Observatory and the AxiomStore increment without seeing your final implementation.

### Closed-book defense

In five minutes, answer “How do type-level architecture and compiler decisions become concrete symbols, call paths, layouts, and artifact size—and which observations are stable enough to guide design?” using the **source-to-artifact observation**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside AxiomStore. A list of APIs without the deciding relationship is incomplete.
