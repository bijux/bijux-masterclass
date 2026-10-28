# Course 3 study plan — Traits, Generics, and Architectural Design

This plan turns ten chapters into ten days of deliberate practice. A day is complete only when the model, independent laboratory, and Review Engine increment agree. If the lab passes while the explanation remains vague, repair the model before moving on.

## Daily rhythm

| Time | Work | Required output |
|---|---|---|
| 08:30–09:00 | closed-book reconstruction | one page of the previous mechanism from memory |
| 09:00–11:00 | authoritative chapter and typed examples | annotated model and changed-assumption predictions |
| 11:15–12:30 | compiler or boundary specimens | frozen predictions and causal comparison |
| 13:30–15:00 | repair and focused construction | smallest principled repair plus rejected shortcut |
| 15:15–17:30 | independent laboratory | working behavior, adversarial tests, design record |
| 18:30–20:00 | Review Engine increment | integrated change and regression evidence |
| 20:00–20:30 | explanation and retrieval | invariant, decisive rule, failure state, transfer case |

Take real breaks. Dense work is not continuous screen time. The weekend between Days 5 and 6 is for repair, reconstruction, and rest rather than new material.

## Day 1 — Traits as Behavioral Contracts

**Governing question:** What behavior truly belongs in a shared contract, and which laws must every implementation preserve?

### Morning: derive the model

Read [Module 21](module-21-traits-as-behavioral-contracts/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-21-traits-as-behavioral-contracts/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 21 — Contract Boundaries](../labs/module-01-contract-boundaries/README.md). Build a small pricing library for `Book`, `CourseLicense`, and `SupportPlan`.

### Evening: integrate the course product

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Define the Review Engine's source, rule, and reporter contracts with behavioral laws. Separate required methods from defaults and identify what tests must enforce. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“What behavior truly belongs in a shared contract, and which laws must every implementation preserve?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Define a trait whose methods express a coherent behavioral contract;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 2 — Associated Types and Type Families

**Governing question:** When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?

### Morning: derive the model

Read [Module 22](module-22-associated-types-and-type-families/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-22-associated-types-and-type-families/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 22 — Associated Families](../labs/module-02-associated-families/README.md). Implement a source whose implementation chooses its row and error families, then add a borrowed row-view family indexed by the borrow lifetime. Demonstrate which invalid type combinations an independently selectable generic API would permit.

### Evening: integrate the course product

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Attach item, output, and error families to the implementations that choose them. Use associated types where callers should not select arbitrary combinations. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Choose between generic parameters and associated types from relationship cardinality;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 3 — Coherence and Implementation Ownership

**Governing question:** Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?

### Morning: derive the model

Read [Module 23](module-23-coherence-and-implementation-ownership/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-23-coherence-and-implementation-ownership/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 23 — Coherence Adapters](../labs/module-03-coherence-adapters/README.md). Integrate two foreign-style model types with two local formatting and validation contracts.

### Evening: integrate the course product

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Add local adapters, closure-backed rules, and sealed built-in markers without violating coherence. Record which crate owns every implementation relationship. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Predict whether an implementation satisfies coherence and orphan rules;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 4 — Static Polymorphism and Opaque Types

**Governing question:** When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?

### Morning: derive the model

Read [Module 24](module-24-static-polymorphism-and-opaque-types/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-24-static-polymorphism-and-opaque-types/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 24 — Static Pipeline](../labs/module-04-static-pipeline/README.md). Build a statically composed validation pipeline whose source code selects concrete validator types.

### Evening: integrate the course product

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Keep source and reporter boundaries statically dispatched, using the weakest sufficient bounds and opaque types only where concrete names would leak irrelevant detail. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Design generic functions and types with the weakest sufficient bounds;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 5 — Trait Objects and Dynamic Polymorphism

**Governing question:** When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?

### Morning: derive the model

Read [Module 25](module-25-trait-objects-and-dynamic-polymorphism/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-25-trait-objects-and-dynamic-polymorphism/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 25 — Dynamic Command Bus](../labs/module-05-dynamic-command-bus/README.md). Build a command bus that owns heterogeneous command handlers behind a dyn-compatible interface.

### Evening: integrate the course product

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Introduce the ordered heterogeneous rule registry with `Box<dyn Rule>`. Document what is erased, why runtime heterogeneity is required, and how object lifetimes are owned. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Derive whether a trait is dyn-compatible and repair it without erasing its meaning;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 6 — Composition and OOP-Style Design Without Inheritance

**Governing question:** How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?

### Morning: derive the model

Read [Module 26](module-26-composition-and-oop-style-design-without-inheritance/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-26-composition-and-oop-style-design-without-inheritance/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 26 — Composed Renderer](../labs/module-06-composed-renderer/README.md). Build a report-rendering system with two base formats and two optional wrappers.

### Evening: integrate the course product

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Compose parsing, policy, evaluation, and reporting through owned components and adapters. Do not invent an inheritance hierarchy for responsibilities that can be delegated. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Model encapsulation, substitution, and delegation without class inheritance;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 7 — Typestate and Capability-Oriented APIs

**Governing question:** Which illegal operations can be removed from the API by representing protocol state and authority in types?

### Morning: derive the model

Read [Module 27](module-27-typestate-and-capability-oriented-apis/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-27-typestate-and-capability-oriented-apis/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 27 — Typestate Publication](../labs/module-07-typestate-publication/README.md). Implement `Draft -> Reviewed -> Published` with state-specific evidence.

### Evening: integrate the course product

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Build the engine through typestate so execution is unavailable until source, policy, and reporter are present. Keep the state machinery out of the finished engine's public behavior. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Which illegal operations can be removed from the API by representing protocol state and authority in types?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Encode a finite protocol with marker states and consuming transitions;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 8 — Boundary Traits and Adapters

**Governing question:** How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?

### Morning: derive the model

Read [Module 28](module-28-boundary-traits-and-adapters/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-28-boundary-traits-and-adapters/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 28 — Boundary Ports](../labs/module-08-boundary-ports/README.md). Build a small inspection service with a domain core independent from input and output mechanisms.

### Evening: integrate the course product

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Add narrow ports, production adapters, fakes, and conversion boundaries. Each trait must correspond to a real substitution need rather than a desire to mock everything. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Design extension traits, closure adapters, and conversion boundaries with precise contracts;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 9 — Public API Evolution

**Governing question:** How can a public trait-based API evolve when downstream crates may both call it and implement it?

### Morning: derive the model

Read [Module 29](module-29-public-api-evolution/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-29-public-api-evolution/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 29 — Evolvable SDK](../labs/module-09-evolvable-sdk/README.md). Start from a small public plugin contract and evolve it through two versions.

### Evening: integrate the course product

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Review the public extension surface from both downstream perspectives: callers and implementors. Preserve evolution room with sealing, non-exhaustive data, and compatibility tests. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“How can a public trait-based API evolve when downstream crates may both call it and implement it?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Classify public trait changes by downstream source-compatibility risk;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 10 — Architectural Synthesis

**Governing question:** Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?

### Morning: derive the model

Read [Module 30](module-30-architectural-synthesis/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-30-architectural-synthesis/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 30 — Inspection Platform](../labs/module-10-inspection-platform/README.md). Build a separate miniature inspection platform from a product brief only.

### Evening: integrate the course product

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Implement an unseen Review Engine extension and update the variation map first. Defend why each boundary uses an enum, generic, trait object, closure, or concrete type. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Map axes of variation before selecting polymorphism mechanisms;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;


## Mid-course reconstruction

After Day 5, rebuild the five-module dependency chain without notes. Select the two compiler specimens that changed your model most, rerun them, and explain why the wrong prediction was plausible. Repair every incomplete lab before opening Day 6; later mechanisms assume that the earlier contract is stable.

## Final consolidation

After Day 10, use the [course reference](reference.md) to compress the material, not to relearn it. Complete the [final review](final-review.md) from an empty directory. Then defend Review Engine by tracing one successful operation and one adversarial failure through every layer touched by the course.
