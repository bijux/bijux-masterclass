# Course 3 — Traits, Generics, and Architectural Design

## Behavioral Contracts, Variation, and Evolvable APIs

## The promise

Course 3 turns traits and generics into architectural tools rather than syntax exercises. It teaches contracts and laws, associated type families, coherence, static and dynamic dispatch, composition, typestate, adapters, and compatibility-aware public APIs.

> **Governing question:** How should a Rust architecture represent shared behavior, type relationships, runtime variation, protocol states, and downstream extension without importing an inheritance model?

Course 2 established how values live, borrow, share liveness, clean up, and occupy memory. Course 3 keeps those memory contracts and moves outward to architecture: which types may promise shared behavior, who may implement a contract, when variation is static or dynamic, and how public extension remains coherent.

## Before Day 1

You should be comfortable with ownership and borrowing, trait basics, generic functions, lifetime annotations, smart-pointer liveness, and private invariant-bearing types.

From a blank page, sketch one earlier product or a comparable program. Mark an owner, a valid and invalid state, a failure path, cleanup, and a public promise. Repair any relationship you cannot explain before adding this course’s mechanisms.

## Outcomes

- Define a trait whose methods express a coherent behavioral contract.
- Choose between generic parameters and associated types from relationship cardinality.
- Predict whether an implementation satisfies coherence and orphan rules.
- Design generic functions and types with the weakest sufficient bounds.
- Derive whether a trait is dyn-compatible and repair it without erasing its meaning.
- Model encapsulation, substitution, and delegation without class inheritance.
- Encode a finite protocol with marker states and consuming transitions.
- Design extension traits, closure adapters, and conversion boundaries with precise contracts.
- Classify public trait changes by downstream source-compatibility risk.
- Map axes of variation before selecting polymorphism mechanisms.
- Integrate all ten mechanisms in Review Engine without creating competing authorities.
- Complete and defend an unseen change using a architecture decision record.

## The ten-day line

| Day | Module | Governing question | Capability that must become visible | Laboratory |
|---:|---|---|---|---|
| 1 | [21 — Traits as Behavioral Contracts](./module-21-traits-as-behavioral-contracts/index.md) | What behavior truly belongs in a shared contract, and which laws must every implementation preserve? | **Define a trait whose methods express a coherent behavioral contract.** | [Contract Boundaries](../labs/module-01-contract-boundaries/README.md) |
| 2 | [22 — Associated Types and Type Families](./module-22-associated-types-and-type-families/index.md) | When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API? | **Choose between generic parameters and associated types from relationship cardinality.** | [Associated Families](../labs/module-02-associated-families/README.md) |
| 3 | [23 — Coherence and Implementation Ownership](./module-23-coherence-and-implementation-ownership/index.md) | Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation? | **Predict whether an implementation satisfies coherence and orphan rules.** | [Coherence Adapters](../labs/module-03-coherence-adapters/README.md) |
| 4 | [24 — Static Polymorphism and Opaque Types](./module-24-static-polymorphism-and-opaque-types/index.md) | When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees? | **Design generic functions and types with the weakest sufficient bounds.** | [Static Pipeline](../labs/module-04-static-pipeline/README.md) |
| 5 | [25 — Trait Objects and Dynamic Polymorphism](./module-25-trait-objects-and-dynamic-polymorphism/index.md) | When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable? | **Derive whether a trait is dyn-compatible and repair it without erasing its meaning.** | [Dynamic Command Bus](../labs/module-05-dynamic-command-bus/README.md) |
| 6 | [26 — Composition and OOP-Style Design Without Inheritance](./module-26-composition-and-oop-style-design-without-inheritance/index.md) | How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance? | **Model encapsulation, substitution, and delegation without class inheritance.** | [Composed Renderer](../labs/module-06-composed-renderer/README.md) |
| 7 | [27 — Typestate and Capability-Oriented APIs](./module-27-typestate-and-capability-oriented-apis/index.md) | Which illegal operations can be removed from the API by representing protocol state and authority in types? | **Encode a finite protocol with marker states and consuming transitions.** | [Typestate Publication](../labs/module-07-typestate-publication/README.md) |
| 8 | [28 — Boundary Traits and Adapters](./module-28-boundary-traits-and-adapters/index.md) | How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model? | **Design extension traits, closure adapters, and conversion boundaries with precise contracts.** | [Boundary Ports](../labs/module-08-boundary-ports/README.md) |
| 9 | [29 — Public API Evolution](./module-29-public-api-evolution/index.md) | How can a public trait-based API evolve when downstream crates may both call it and implement it? | **Classify public trait changes by downstream source-compatibility risk.** | [Evolvable SDK](../labs/module-09-evolvable-sdk/README.md) |
| 10 | [30 — Architectural Synthesis](./module-30-architectural-synthesis/index.md) | Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition? | **Map axes of variation before selecting polymorphism mechanisms.** | [Inspection Platform](../labs/module-10-inspection-platform/README.md) |

The table is a dependency chain, not a menu. A later module may use an earlier mechanism but may not silently weaken its ownership, failure, ordering, capacity, safety, compatibility, or evidence contract.

## Decision rules

| Decision | Rule used throughout this course |
|---|---|
| Trait boundary | State behavioral laws before choosing methods or defaults. |
| Associated type | Use it when an implementation owns one related type family; use a generic parameter when callers select independently. |
| Dispatch | Use static dispatch for compile-time composition and dynamic dispatch for runtime heterogeneity or extension. |
| Typestate | Encode a protocol stage when method availability should change after a consuming transition. |
| Evolution | Review both downstream callers and downstream implementors before publishing a public trait or enum. |

Use these rules during prediction and review. When a rule does not decide the case, write the missing product requirement instead of selecting an API by habit.

## The reasoning record

The ten module-specific records culminate in a **architecture decision record**. State the law, type relationship, implementation owner, dispatch choice, and evolution obligation before introducing a trait boundary. Keep the record small enough to inspect but complete enough to expose the first unsupported assumption.

## Scope and handoff

The course focuses on behavioral and architectural variation. It deliberately postpones iterator-centered functional architecture, macro generation, unsafe systems boundaries, and concurrent execution.

Course 4 keeps these contracts but asks how values, failure, demand, and effects compose through closures, iterators, reductions, and persistent transformations.

## Capstone — Review Engine

Review Engine evaluates submissions against ordered policies. Generic source and reporting ports, a heterogeneous rule registry, coherence-safe adapters, typestate construction, and deterministic results make the choice of variation mechanism visible.

Open the [engineering guide](capstone.md) before Day 1 so the final architecture is visible. Implement only the current increment. The independent laboratory remains separate so that the mechanism can be learned without hiding behind accumulated capstone code.

## Completion

The course is complete when you can build and defend:

> Build a plugin-capable inspection service with one static pipeline, one dynamic registry, a typestate builder, reusable contract tests, and a written compatibility policy.

and then change the capstone under this constraint:

> Add a versioned rule capability to Review Engine while preserving source compatibility, deterministic rule order, and a clear static-versus-dynamic boundary.

A passing test suite is necessary. It is not sufficient unless you can explain why the tests are capable of falsifying the claim and which target-, scheduler-, workload-, peer-, or policy-dependent facts remain outside them.

## Continue

- [Ten-day plan](study-plan.md)
- [Module 21 — Traits as Behavioral Contracts](./module-21-traits-as-behavioral-contracts/index.md)
- [Review Engine engineering guide](capstone.md)
- [Course reference](reference.md)
- [Final review](final-review.md)
- [Compiler and design investigations](../compiler-labs/README.md)
- [Independent laboratories](../labs/)
