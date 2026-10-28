# Course 10 — Advanced Rust Mastery

## Compiler Reasoning, Type Architecture, Soundness, and Long-Lived Systems

Course 10 is the synthesis course. It teaches compiler-phase reasoning, advanced trait solving, GATs and HRTBs, const-generic witnesses, opaque and erased types, whole-abstraction unsafe review, source-to-artifact analysis, verification strategy, API and data evolution, and architectural restraint.

> **Governing question:** How do you design and evolve a Rust system whose type relationships, unsafe boundaries, compiler behavior, compatibility promises, verification evidence, and operating limits survive independent change?

## Entry point

You should have completed the preceding nine courses or equivalent work. You should be able to explain ownership, memory, traits, functional dataflow, macros, unsafe systems boundaries, concurrency, async protocols, and production evidence without relying on API-name recall alone.

The immediate prerequisite is [Course 9: Rust Performance and Production Engineering](../09-rust-performance-production-engineering/course-book/index.md). Entering mid-program is reasonable only when you can complete the previous course’s final review and one independent construction without following its solution.

## Ten-day route

| Day | Module | Capability added | Independent laboratory |
|---:|---|---|---|
| 1 | [91 — Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen](course-book/module-91-reading-rust-through-the-compiler-hir-mir-borrow-checking-and-codegen/index.md) | Separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases | [Compiler Evidence Notebook](labs/module-01-compiler-evidence-notebook/README.md) |
| 2 | [92 — Advanced Trait Solving: Goals, Projections, and Type Equality](course-book/module-92-advanced-trait-solving-goals-projections-and-type-equality/index.md) | Rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints | [Projection-Driven Pipeline](labs/module-02-projection-driven-pipeline/README.md) |
| 3 | [93 — GATs, Higher-Ranked Bounds, and Lending Interfaces](course-book/module-93-gats-higher-ranked-bounds-and-lending-interfaces/index.md) | Distinguish one associated type from a lifetime-indexed family of associated types | [Lending Table](labs/module-03-lending-table/README.md) |
| 4 | [94 — Const Generics, Witness Types, and Compile-Time Invariants](course-book/module-94-const-generics-witness-types-and-compile-time-invariants/index.md) | Use const parameters when a numeric fact changes representation, layout, or legal composition | [Bounded Matrix](labs/module-04-bounded-matrix/README.md) |
| 5 | [95 — Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries](course-book/module-95-opaque-and-erased-types-impl-trait-dyn-trait-any-and-plugin-boundaries/index.md) | Distinguish opaque return types from trait objects and explain why different branches of `impl Trait` must share one hidden concrete type | [Erased Validator Registry](labs/module-05-erased-validator-registry/README.md) |
| 6 | [96 — Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits](course-book/module-96-auditing-unsafe-abstractions-validity-provenance-drop-panic-and-auto-traits/index.md) | Write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation | [Inline Batch](labs/module-06-inline-batch/README.md) |
| 7 | [97 — From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size](course-book/module-97-from-source-to-machine-code-monomorphization-dispatch-layout-and-code-size/index.md) | Explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication | [Dispatch Observatory](labs/module-07-dispatch-observatory/README.md) |
| 8 | [98 — Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration](course-book/module-98-verification-beyond-examples-compile-fail-property-model-fuzz-miri-and-concurrency-exploration/index.md) | Classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims | [Model-Checked Log](labs/module-08-model-checked-log/README.md) |
| 9 | [99 — Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship](course-book/module-99-long-lived-apis-semver-msrv-features-migrations-and-workspace-stewardship/index.md) | Analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data | [Versioned SDK](labs/module-09-versioned-sdk/README.md) |
| 10 | [100 — Architectural Synthesis: Building and Defending a Long-Lived Rust System](course-book/module-100-architectural-synthesis-building-and-defending-a-long-lived-rust-system/index.md) | Construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy | [Architecture Council](labs/module-10-architecture-council/README.md) |

The route is cumulative. Day 1 establishes this course’s vocabulary and Day 10 requires an architectural change that preserves all earlier guarantees.

## Working method

State the proof obligation, follow the compiler and abstraction boundary, select independent evidence, and defend compatibility under change. Use the module-specific reasoning record named in each chapter. Freeze predictions before compiling, preserve causal diagnostics, and compare the lab reference only after recording your own design.

## Capstone — AxiomStore

AxiomStore is a versioned embedded record engine with lending views, const bounds, runtime validators, one private initialized-prefix abstraction, deterministic storage, migrations, compatibility fixtures, and a claim-specific verification matrix.

The [engineering guide](course-book/capstone.md) supplies the ten integration steps. The executable [capstone directory](capstone/README.md) contains the product and tests. Each increment must name the changed invariant, the component that owns it, state after failure, and the earlier guarantee that must remain unchanged.

## Scope

The course selects stable mechanisms that serve real product requirements. It does not reward obscure syntax, nightly-feature collecting, unsafe code retained for display, or lower-level compiler output used where source-level reasoning is already decisive.

The program ends with independent transfer: you should be able to enter an unfamiliar Rust system, identify its authorities and proof boundaries, make a cross-cutting change, and state what remains uncertain.

## Exit standard

Complete this independent construction:

> Build a versioned embedded journal whose borrowed read API, runtime validators, bounded transaction representation, compatibility policy, unsafe-or-safe storage decision, and verification matrix are derived from an invariant ownership map.

Then complete this capstone extension:

> Implement the AXIOM02 format extension without creating a parallel validation or persistence architecture, and defend every compatibility and unsafe consequence.

The next step is independent advanced Rust work.

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
