# Module 97 Solutions — From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size

[Workbook](workbook.md) · [Chapter](index.md) · [AxiomStore guide](../capstone.md)

These are reasoned reference answers. Compare your predicted phase, invariant owner, and failure state before comparing syntax. A different implementation is stronger when it preserves the same contract with a smaller proof surface.

## Part 1 — Prediction

### Prediction 1 — Generic instances

There are two concrete type uses, but inlining, deduplication, dead-code elimination, and compiler sharing may alter visible symbols in one artifact.

### Prediction 2 — Trait-object call cost

No. The source identifies dispatch form; a representative profile must establish frequency and cost. The compiler may devirtualize in some artifacts.

### Prediction 3 — repr(C) size claim

No. `repr(C)` supplies documented representation/ABI constraints, not universal compactness. Exact size remains target-conditioned.

### Prediction 4 — Vanished helper

It may have been inlined or removed. The semantic operation can still have cost at call sites; inspect generated code and profiles before claiming elimination.

## Part 2 — Diagnose and repair

Judge every repair against the source-to-artifact observation record: the decisive relationship must become clearer, not disappear behind cloning, erasure, broad bounds, visibility, unchecked construction, or deleted validation.

### Repair 1 — Generic equals duplication

**Causal defect.** A review declares that every generic call creates duplicate machine code.

**Principled repair.** Inventory concrete reachable instantiations and inspect one pinned artifact; record compiler transformations and avoid universal claims.

A strong answer updates the source-to-artifact observation record and includes a negative case that fails for the original cause.

### Repair 2 — Dynamic dispatch equals heap

**Causal defect.** A design rejects `dyn Trait` because it assumes every object allocates.

**Principled repair.** Separate dispatch from ownership. Borrowed trait objects need no heap allocation; boxed ownership is a separate choice.

A strong answer updates the source-to-artifact observation record and includes a negative case that fails for the original cause.

### Repair 3 — Layout observation becomes format

**Causal defect.** A serialized format writes native struct bytes after observing a convenient layout.

**Principled repair.** Use explicit encoding. Target layout is not a durable wire format unless a precise stable representation contract exists.

A strong answer updates the source-to-artifact observation record and includes a negative case that fails for the original cause.

## Part 3 — Focused exercises

### Exercise 1 — Dispatch parity

The construction should answer: Implement generic, enum, and trait-object paths with one semantic oracle.

The decisive acceptance criterion is: All variants produce identical results before measurement.

Evaluate the result through the source-to-artifact observation record; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 2 — Artifact record

The construction should answer: Inspect symbols and assembly under two profiles.

The decisive acceptance criterion is: Every observation includes toolchain, target, features, and expiry condition.

Evaluate the result through the source-to-artifact observation record; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 3 — Layout notebook

The construction should answer: Record size/alignment observations and separate them from guarantees.

The decisive acceptance criterion is: No target observation is described as portable Rust semantics.

Evaluate the result through the source-to-artifact observation record; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 4 — Size attribution

The construction should answer: Add one generic instantiation and one formatting path, then compare artifact contributions.

The decisive acceptance criterion is: The report avoids blaming an abstraction without symbol/section evidence.

Evaluate the result through the source-to-artifact observation record; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Cross-course transfer

Full credit may conclude that **From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size** should not be retrofitted into the earlier artifact. The comparison must identify the current owner, the proof benefit, maintenance cost, and a concrete failure that would change.


### Applied case study — choosing dispatch with two artifacts

The experiment needs three semantically identical implementations behind one oracle: a generic call path for built-ins, a closed enum dispatch path, and a `dyn Rule` path. They must receive the same records in the same order and emit byte-for-byte or value-for-value equivalent results. Measurements must use the same optimized profile, target, feature set, toolchain, warm-up, sample policy, and invocation count. Record runtime and artifact size independently; a smaller binary does not imply lower latency, and a faster microbenchmark does not settle extension policy.

The likely architecture keeps built-ins static or enum-dispatched because the set is closed, known to the library, and called frequently. Runtime plugins remain dynamically dispatched because the concrete type is host-selected and heterogeneous. Genericizing the plugin boundary would require making the entire host type depend on every plugin set or recompiling for additions, which contradicts the requirement. Erasing built-ins solely to save a measured amount of code may be justified only if the pinned artifact exceeds a real size budget and the latency cost remains acceptable.

Inlining and monomorphization are compiler opportunities, not guarantees. Dynamic calls may reduce duplication but add indirection; branch prediction can make either path workload-sensitive. Compile time and API evolution are separate costs.

That monomorphization creates distinct concrete instantiations is a language/compiler model fact. Choosing a hybrid boundary is a design decision. Exact symbol sizes, section changes, and latency deltas are observations about the pinned artifact. A new target, rule size distribution, or hard binary budget could reverse the built-in choice without changing Rust semantics.

## Part 4 — Independent laboratory

A complete [Dispatch Observatory](../../labs/module-07-dispatch-observatory/README.md) satisfies its public contract and makes the source-to-artifact observation record inspectable. The reference implementation is not canonical; compare accepted input, rejected input, state after failure, ownership/lifetime surface, deterministic behavior, and extension authority in that order.

Build static, enum, and dynamic scoring paths over one oracle, then produce a pinned artifact observation that distinguishes dispatch, ownership, and code-size effects.

The transfer variant for Dispatch Observatory must alter at least two substantive dimensions and preserve an independent oracle; a domain-name substitution is not evidence of mastery.

## Part 5 — Capstone transfer

Compare AxiomStore’s const-specialized codec paths and dynamically dispatched validators without changing semantics. Record one artifact-specific conclusion and retain the generic/dynamic architecture only if product requirements, not folklore, justify it.

A strong capstone change keeps the responsibility described by the source-to-artifact observation record local. Reject any design that spreads the mechanism across unrelated AxiomStore modules without a named requirement.

## Part 6 — Reconstruct and defend

Explain one semantic guarantee and one artifact observation about the same code, then state why neither can replace the other.

The defense passes when it reconstructs the source-to-artifact observation record from the requirement, shows a causal rejected construction, compares a simpler alternative, maps evidence, and names residual risk. Terminology without that chain is not mastery.
