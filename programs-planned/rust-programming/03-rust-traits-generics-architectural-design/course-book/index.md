# Course 3 — Traits, Generics, and Architectural Design

## Contracts, Polymorphism, Composition, and Evolvable APIs

Turn type-level knowledge into architecture: define lawful contracts, choose static or dynamic variation, compose behavior, encode protocols, adapt boundaries, and evolve public APIs without inheritance-shaped thinking.

## Why this course exists

The first two courses establish what values mean and how they remain valid. Architecture begins when several types must participate in the same product without surrendering their invariants. Rust offers enums, generics, traits, closures, trait objects, newtypes, and ordinary composition; none is the universal answer. This course teaches a mechanism-selection discipline based on who chooses the variation, when the choice is made, what information may be erased, and which downstream obligations become public.

## Before you begin

Course 2, including precise borrow relationships, cleanup and liveness reasoning, smart-pointer trade-offs, and the distinction between semantic guarantees and representation observations.

Keep a trait-law table, variation map, dispatch map, and downstream-compatibility matrix beside the code. The record changes shape as the course advances, but its purpose is constant: make the decisive relationship visible before syntax hides it.

## What you will be able to do

- Define a trait as a coherent behavioral contract with appropriate receivers, required primitives, derived defaults, supertraits, and explicit semantic laws.
- Distinguish inherent methods, free functions, traits, extension traits, and adapters by ownership of behavior and evolution responsibility.
- Choose generic parameters, associated types, associated constants, and equality constraints from the cardinality of the type relationship.
- Use introductory generic associated types only when an implementation owns a family of borrowed outputs indexed by a lifetime.
- Predict coherence and orphan-rule legality, detect overlapping blanket implementations, and use newtypes or local adapters to regain implementation ownership.
- Design generic APIs with the weakest sufficient bounds and understand when monomorphization is a benefit, cost, or irrelevant implementation detail.
- Use argument-position and return-position `impl Trait` while distinguishing caller-chosen types from implementation-hidden concrete types.
- Derive dyn compatibility, object lifetime requirements, and erased information before choosing a trait-object boundary.
- Choose among enums, generics, trait objects, closures, and functions from whether the variant set is closed, who chooses it, and when heterogeneity is required.
- Build behavior through composition, delegation, strategy, adapter, decorator, and command patterns without reproducing inheritance hierarchies.
- Encode narrow protocols and single-use authority with typestate or capability tokens while avoiding combinatorial state explosion.
- Design boundary traits and closure adapters that isolate external data and effects without creating framework-sized abstraction layers.
- Use `From`, `TryFrom`, `AsRef`, and `Borrow` according to semantic conversion and lookup contracts rather than superficial signature convenience.
- Evaluate public trait evolution from both downstream roles—caller and implementor—and use sealing, non-exhaustive models, adapters, or versioned traits deliberately.
- Produce and defend an architecture decision record that names variation axes, dispatch choices, erased information, laws, compatibility obligations, and rejected alternatives.

## What this course deliberately leaves for later

The course focuses on architectural variation and public API design. Iterator algebra, functional effect architecture, macro construction, unsafe boundaries, and concurrency remain responsibilities of later courses.

## Ten-day route

1. [Module 21: Traits as Behavioral Contracts](module-21-traits-as-behavioral-contracts/index.md) — What behavior truly belongs in a shared contract, and which laws must every implementation preserve?
2. [Module 22: Associated Types and Type Families](module-22-associated-types-and-type-families/index.md) — When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?
3. [Module 23: Coherence and Implementation Ownership](module-23-coherence-and-implementation-ownership/index.md) — Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?
4. [Module 24: Static Polymorphism and Opaque Types](module-24-static-polymorphism-and-opaque-types/index.md) — When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?
5. [Module 25: Trait Objects and Dynamic Polymorphism](module-25-trait-objects-and-dynamic-polymorphism/index.md) — When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?
6. [Module 26: Composition and OOP-Style Design Without Inheritance](module-26-composition-and-oop-style-design-without-inheritance/index.md) — How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?
7. [Module 27: Typestate and Capability-Oriented APIs](module-27-typestate-and-capability-oriented-apis/index.md) — Which illegal operations can be removed from the API by representing protocol state and authority in types?
8. [Module 28: Boundary Traits and Adapters](module-28-boundary-traits-and-adapters/index.md) — How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?
9. [Module 29: Public API Evolution](module-29-public-api-evolution/index.md) — How can a public trait-based API evolve when downstream crates may both call it and implement it?
10. [Module 30: Architectural Synthesis](module-30-architectural-synthesis/index.md) — Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?

## How the learning surfaces fit

The chapter is the authoritative explanation. The workbook exposes the model you actually hold through prediction, repair, construction, transfer, and defense. The independent lab removes accumulated capstone complexity so one mechanism remains visible. The capstone increment then asks that mechanism to coexist with every earlier decision.

The cumulative product is **Review Engine**: a policy evaluation engine with generic source and reporter boundaries, associated error families, a dynamic rule registry, coherence-safe adapters, typestate construction, and a defended extension surface. Do not read the complete implementation before attempting the corresponding increment; the value of the capstone is the sequence of design decisions, not possession of the finished source.

Use the [compiler investigations](../compiler-labs/README.md), the [ten-day study plan](study-plan.md), the [Review Engine engineering guide](capstone.md), the [course reference](reference.md), and the [independent final review](final-review.md).

## Completion standard

The course is complete when you can satisfy the public behavior, explain the decisive rule without notes, repair a misleading implementation without weakening its requirement, and transfer the mechanism to the final independent product. A passing test suite without a causal model is incomplete; a persuasive explanation without working evidence is also incomplete.

## Course handoff

Course 4 uses these contracts as the joints of explicit dataflow, fallible traversal, reduction, and effect isolation.

[Return to the program start](../../README.md) · [Open the sixty-module map](../../COURSE_MAP.md)
