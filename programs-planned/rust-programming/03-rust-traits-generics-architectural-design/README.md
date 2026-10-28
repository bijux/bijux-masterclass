# Course 3 — Traits, Generics, and Architectural Design

## Behavioral Contracts, Variation, and Evolvable APIs

Course 3 turns traits and generics into architectural tools rather than syntax exercises. It teaches contracts and laws, associated type families, coherence, static and dynamic dispatch, composition, typestate, adapters, and compatibility-aware public APIs.

> **Governing question:** How should a Rust architecture represent shared behavior, type relationships, runtime variation, protocol states, and downstream extension without importing an inheritance model?

## Entry point

You should be comfortable with ownership and borrowing, trait basics, generic functions, lifetime annotations, smart-pointer liveness, and private invariant-bearing types.

The immediate prerequisite is [Course 2: Ownership, Lifetimes, and Memory](../02-rust-ownership-lifetimes-memory/course-book/index.md). Entering mid-program is reasonable only when you can complete the previous course’s final review and one independent construction without following its solution.

## Ten-day route

| Day | Module | Capability added | Independent laboratory |
|---:|---|---|---|
| 1 | [21 — Traits as Behavioral Contracts](course-book/module-21-traits-as-behavioral-contracts/index.md) | Define a trait whose methods express a coherent behavioral contract | [Contract Boundaries](labs/module-01-contract-boundaries/README.md) |
| 2 | [22 — Associated Types and Type Families](course-book/module-22-associated-types-and-type-families/index.md) | Choose between generic parameters and associated types from relationship cardinality | [Associated Families](labs/module-02-associated-families/README.md) |
| 3 | [23 — Coherence and Implementation Ownership](course-book/module-23-coherence-and-implementation-ownership/index.md) | Predict whether an implementation satisfies coherence and orphan rules | [Coherence Adapters](labs/module-03-coherence-adapters/README.md) |
| 4 | [24 — Static Polymorphism and Opaque Types](course-book/module-24-static-polymorphism-and-opaque-types/index.md) | Design generic functions and types with the weakest sufficient bounds | [Static Pipeline](labs/module-04-static-pipeline/README.md) |
| 5 | [25 — Trait Objects and Dynamic Polymorphism](course-book/module-25-trait-objects-and-dynamic-polymorphism/index.md) | Derive whether a trait is dyn-compatible and repair it without erasing its meaning | [Dynamic Command Bus](labs/module-05-dynamic-command-bus/README.md) |
| 6 | [26 — Composition and OOP-Style Design Without Inheritance](course-book/module-26-composition-and-oop-style-design-without-inheritance/index.md) | Model encapsulation, substitution, and delegation without class inheritance | [Composed Renderer](labs/module-06-composed-renderer/README.md) |
| 7 | [27 — Typestate and Capability-Oriented APIs](course-book/module-27-typestate-and-capability-oriented-apis/index.md) | Encode a finite protocol with marker states and consuming transitions | [Typestate Publication](labs/module-07-typestate-publication/README.md) |
| 8 | [28 — Boundary Traits and Adapters](course-book/module-28-boundary-traits-and-adapters/index.md) | Design extension traits, closure adapters, and conversion boundaries with precise contracts | [Boundary Ports](labs/module-08-boundary-ports/README.md) |
| 9 | [29 — Public API Evolution](course-book/module-29-public-api-evolution/index.md) | Classify public trait changes by downstream source-compatibility risk | [Evolvable SDK](labs/module-09-evolvable-sdk/README.md) |
| 10 | [30 — Architectural Synthesis](course-book/module-30-architectural-synthesis/index.md) | Map axes of variation before selecting polymorphism mechanisms | [Inspection Platform](labs/module-10-inspection-platform/README.md) |

The route is cumulative. Day 1 establishes this course’s vocabulary and Day 10 requires an architectural change that preserves all earlier guarantees.

## Working method

State the law, type relationship, implementation owner, dispatch choice, and evolution obligation before introducing a trait boundary. Use the module-specific reasoning record named in each chapter. Freeze predictions before compiling, preserve causal diagnostics, and compare the lab reference only after recording your own design.

## Capstone — Review Engine

Review Engine evaluates submissions against ordered policies. Generic source and reporting ports, a heterogeneous rule registry, coherence-safe adapters, typestate construction, and deterministic results make the choice of variation mechanism visible.

The [engineering guide](course-book/capstone.md) supplies the ten integration steps. The executable [capstone directory](capstone/README.md) contains the product and tests. Each increment must name the changed invariant, the component that owns it, state after failure, and the earlier guarantee that must remain unchanged.

## Scope

The course focuses on behavioral and architectural variation. It deliberately postpones iterator-centered functional architecture, macro generation, unsafe systems boundaries, and concurrent execution.

Course 4 keeps these contracts but asks how values, failure, demand, and effects compose through closures, iterators, reductions, and persistent transformations.

## Exit standard

Complete this independent construction:

> Build a plugin-capable inspection service with one static pipeline, one dynamic registry, a typestate builder, reusable contract tests, and a written compatibility policy.

Then complete this capstone extension:

> Add a versioned rule capability to Review Engine while preserving source compatibility, deterministic rule order, and a clear static-versus-dynamic boundary.

The next step is [Course 4: Functional Rust](../04-rust-functional-programming/course-book/index.md).

## Reading and execution routes

- [Course book](course-book/index.md)
- [Ten-day study plan](course-book/study-plan.md)
- [Course reference](course-book/reference.md)
- [Final review](course-book/final-review.md)
- [Compiler and design investigations](compiler-labs/README.md)
- [Laboratories](labs/)

```bash
make static-proof
make compiler-labs
make check
make test
make starters
make docs
make proof
```

Static inspection and compilation answer different questions. The strongest completion route uses the pinned toolchain, executes tests and investigations, renders the book, and preserves the resulting evidence with the code under review.
