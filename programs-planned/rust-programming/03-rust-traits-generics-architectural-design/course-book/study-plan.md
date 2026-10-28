# Course 3 Study Plan — Traits, Generics, and Architectural Design

Ten dense study days fit into two calendar weeks. The goal is not to maximize reading time; it is to make **How should a Rust architecture represent shared behavior, type relationships, runtime variation, protocol states, and downstream extension without importing an inheritance model?** answerable through construction and explanation.

## Daily rhythm

Use a **architecture decision record** across the course. Each day begins by reconstructing yesterday’s decisive relationship and ends by tracing one capstone invariant. Preserve the first prediction, the observed result, the principled repair, and the shortcut you rejected.

## Day 1 — Module 21: Traits as Behavioral Contracts

**Question:** What behavior truly belongs in a shared contract, and which laws must every implementation preserve?

**Retrieval:** Without notes, restate the invariant carried from Module 20 — Pinning and Address-Sensitive Design. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 21](./module-21-traits-as-behavioral-contracts/index.md) with a **trait-law table** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-21-traits-as-behavioral-contracts/workbook.md) before observation. The day’s minimum result is: **Define a trait whose methods express a coherent behavioral contract.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Contract Boundaries](../labs/module-01-contract-boundaries/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 21 in the [Review Engine guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Define a trait whose methods express a coherent behavioral contract.** End with one simpler design that would be preferable under a narrower requirement.

## Day 2 — Module 22: Associated Types and Type Families

**Question:** When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?

**Retrieval:** Without notes, restate the invariant carried from Module 21 — Traits as Behavioral Contracts. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 22](./module-22-associated-types-and-type-families/index.md) with a **associated-type relationship map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-22-associated-types-and-type-families/workbook.md) before observation. The day’s minimum result is: **Choose between generic parameters and associated types from relationship cardinality.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Associated Families](../labs/module-02-associated-families/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 22 in the [Review Engine guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Choose between generic parameters and associated types from relationship cardinality.** End with one simpler design that would be preferable under a narrower requirement.

## Day 3 — Module 23: Coherence and Implementation Ownership

**Question:** Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?

**Retrieval:** Without notes, restate the invariant carried from Module 22 — Associated Types and Type Families. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 23](./module-23-coherence-and-implementation-ownership/index.md) with a **coherence ownership map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-23-coherence-and-implementation-ownership/workbook.md) before observation. The day’s minimum result is: **Predict whether an implementation satisfies coherence and orphan rules.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Coherence Adapters](../labs/module-03-coherence-adapters/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 23 in the [Review Engine guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Predict whether an implementation satisfies coherence and orphan rules.** End with one simpler design that would be preferable under a narrower requirement.

## Day 4 — Module 24: Static Polymorphism and Opaque Types

**Question:** When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?

**Retrieval:** Without notes, restate the invariant carried from Module 23 — Coherence and Implementation Ownership. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 24](./module-24-static-polymorphism-and-opaque-types/index.md) with a **static-dispatch map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-24-static-polymorphism-and-opaque-types/workbook.md) before observation. The day’s minimum result is: **Design generic functions and types with the weakest sufficient bounds.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Static Pipeline](../labs/module-04-static-pipeline/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 24 in the [Review Engine guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Design generic functions and types with the weakest sufficient bounds.** End with one simpler design that would be preferable under a narrower requirement.

## Day 5 — Module 25: Trait Objects and Dynamic Polymorphism

**Question:** When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?

**Retrieval:** Without notes, restate the invariant carried from Module 24 — Static Polymorphism and Opaque Types. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 25](./module-25-trait-objects-and-dynamic-polymorphism/index.md) with a **dynamic-dispatch map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-25-trait-objects-and-dynamic-polymorphism/workbook.md) before observation. The day’s minimum result is: **Derive whether a trait is dyn-compatible and repair it without erasing its meaning.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Dynamic Command Bus](../labs/module-05-dynamic-command-bus/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 25 in the [Review Engine guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Derive whether a trait is dyn-compatible and repair it without erasing its meaning.** End with one simpler design that would be preferable under a narrower requirement.

## Midpoint reconstruction

Do not add a sixth topic on the recovery day. Reconstruct **Traits as Behavioral Contracts, Associated Types and Type Families, Coherence and Implementation Ownership, Static Polymorphism and Opaque Types, Trait Objects and Dynamic Polymorphism** as one dependency chain, rerun the two investigations that changed your model most, and describe the current Review Engine state from an empty page. Repair incomplete work, then take a real break; consolidation is part of the course rather than unused time.

## Day 6 — Module 26: Composition and OOP-Style Design Without Inheritance

**Question:** How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?

**Retrieval:** Without notes, restate the invariant carried from Module 25 — Trait Objects and Dynamic Polymorphism. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 26](./module-26-composition-and-oop-style-design-without-inheritance/index.md) with a **composition diagram** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-26-composition-and-oop-style-design-without-inheritance/workbook.md) before observation. The day’s minimum result is: **Model encapsulation, substitution, and delegation without class inheritance.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Composed Renderer](../labs/module-06-composed-renderer/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 26 in the [Review Engine guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Model encapsulation, substitution, and delegation without class inheritance.** End with one simpler design that would be preferable under a narrower requirement.

## Day 7 — Module 27: Typestate and Capability-Oriented APIs

**Question:** Which illegal operations can be removed from the API by representing protocol state and authority in types?

**Retrieval:** Without notes, restate the invariant carried from Module 26 — Composition and OOP-Style Design Without Inheritance. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 27](./module-27-typestate-and-capability-oriented-apis/index.md) with a **typestate transition graph** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-27-typestate-and-capability-oriented-apis/workbook.md) before observation. The day’s minimum result is: **Encode a finite protocol with marker states and consuming transitions.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Typestate Publication](../labs/module-07-typestate-publication/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 27 in the [Review Engine guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Encode a finite protocol with marker states and consuming transitions.** End with one simpler design that would be preferable under a narrower requirement.

## Day 8 — Module 28: Boundary Traits and Adapters

**Question:** How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?

**Retrieval:** Without notes, restate the invariant carried from Module 27 — Typestate and Capability-Oriented APIs. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 28](./module-28-boundary-traits-and-adapters/index.md) with a **adapter boundary map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-28-boundary-traits-and-adapters/workbook.md) before observation. The day’s minimum result is: **Design extension traits, closure adapters, and conversion boundaries with precise contracts.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Boundary Ports](../labs/module-08-boundary-ports/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 28 in the [Review Engine guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Design extension traits, closure adapters, and conversion boundaries with precise contracts.** End with one simpler design that would be preferable under a narrower requirement.

## Day 9 — Module 29: Public API Evolution

**Question:** How can a public trait-based API evolve when downstream crates may both call it and implement it?

**Retrieval:** Without notes, restate the invariant carried from Module 28 — Boundary Traits and Adapters. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 29](./module-29-public-api-evolution/index.md) with a **compatibility matrix** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-29-public-api-evolution/workbook.md) before observation. The day’s minimum result is: **Classify public trait changes by downstream source-compatibility risk.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Evolvable SDK](../labs/module-09-evolvable-sdk/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 29 in the [Review Engine guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Classify public trait changes by downstream source-compatibility risk.** End with one simpler design that would be preferable under a narrower requirement.

## Day 10 — Module 30: Architectural Synthesis

**Question:** Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?

**Retrieval:** Without notes, restate the invariant carried from Module 29 — Public API Evolution. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 30](./module-30-architectural-synthesis/index.md) with a **architecture decision record** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-30-architectural-synthesis/workbook.md) before observation. The day’s minimum result is: **Map axes of variation before selecting polymorphism mechanisms.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Inspection Platform](../labs/module-10-inspection-platform/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 30 in the [Review Engine guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Map axes of variation before selecting polymorphism mechanisms.** End with one simpler design that would be preferable under a narrower requirement.

## Final integration

After Day 10, complete the [final review](final-review.md), run the strongest available course route, and implement this unseen capstone change: **Add a versioned rule capability to Review Engine while preserving source compatibility, deterministic rule order, and a clear static-versus-dynamic boundary.**

Seven days later, rebuild the ten-module sequence and the core **architecture decision record** without the book. Write a fresh example for every relationship you cannot recover. Re-reading a solution without recreating the model does not count as retained learning.
