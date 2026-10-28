# Course 10 — Advanced Rust Mastery

## Compiler Reasoning, Type Architecture, Soundness, and Long-Lived Systems

## The promise

Course 10 is the synthesis course. It teaches compiler-phase reasoning, advanced trait solving, GATs and HRTBs, const-generic witnesses, opaque and erased types, whole-abstraction unsafe review, source-to-artifact analysis, verification strategy, API and data evolution, and architectural restraint.

> **Governing question:** How do you design and evolve a Rust system whose type relationships, unsafe boundaries, compiler behavior, compatibility promises, verification evidence, and operating limits survive independent change?

Course 9 established how to measure, secure, release, and operate a Rust system. Course 10 completes the program by reviewing the system under change: advanced type relationships, compiler phases, unsafe soundness, verification strategy, downstream compatibility, artifact cost, and architectural migration must agree.

## Before Day 1

You should have completed the preceding nine courses or equivalent work. You should be able to explain ownership, memory, traits, functional dataflow, macros, unsafe systems boundaries, concurrency, async protocols, and production evidence without relying on API-name recall alone.

From a blank page, sketch one earlier product or a comparable program. Mark an owner, a valid and invalid state, a failure path, cleanup, and a public promise. Repair any relationship you cannot explain before adding this course’s mechanisms.

## Outcomes

- Separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases.
- Rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints.
- Distinguish one associated type from a lifetime-indexed family of associated types.
- Use const parameters when a numeric fact changes representation, layout, or legal composition.
- Distinguish opaque return types from trait objects and explain why different branches of `impl Trait` must share one hidden concrete type.
- Write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation.
- Explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication.
- Classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims.
- Analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data.
- Construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy.
- Integrate all ten mechanisms in AxiomStore without creating competing authorities.
- Complete and defend an unseen change using a architecture defense record.

## The ten-day line

| Day | Module | Governing question | Capability that must become visible | Laboratory |
|---:|---|---|---|---|
| 1 | [91 — Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen](./module-91-reading-rust-through-the-compiler-hir-mir-borrow-checking-and-codegen/index.md) | When difficult Rust code surprises you, which compiler representation and which proof obligation actually decide the result? | **Separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases.** | [Compiler Evidence Notebook](../labs/module-01-compiler-evidence-notebook/README.md) |
| 2 | [92 — Advanced Trait Solving: Goals, Projections, and Type Equality](./module-92-advanced-trait-solving-goals-projections-and-type-equality/index.md) | How do you design and debug APIs when the compiler must prove nested trait goals and normalize associated types before ordinary operations become legal? | **Rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints.** | [Projection-Driven Pipeline](../labs/module-02-projection-driven-pipeline/README.md) |
| 3 | [93 — GATs, Higher-Ranked Bounds, and Lending Interfaces](./module-93-gats-higher-ranked-bounds-and-lending-interfaces/index.md) | How can an API return views tied to each borrow of `self` without pretending that every yielded value has one fixed lifetime? | **Distinguish one associated type from a lifetime-indexed family of associated types.** | [Lending Table](../labs/module-03-lending-table/README.md) |
| 4 | [94 — Const Generics, Witness Types, and Compile-Time Invariants](./module-94-const-generics-witness-types-and-compile-time-invariants/index.md) | Which numeric and state facts belong in types, which remain runtime data, and how do you avoid turning a library into an unusable type-level calculator? | **Use const parameters when a numeric fact changes representation, layout, or legal composition.** | [Bounded Matrix](../labs/module-04-bounded-matrix/README.md) |
| 5 | [95 — Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries](./module-95-opaque-and-erased-types-impl-trait-dyn-trait-any-and-plugin-boundaries/index.md) | When should an API hide one concrete type, erase many concrete types behind a contract, or preserve explicit variants—and what information is lost at each boundary? | **Distinguish opaque return types from trait objects and explain why different branches of `impl Trait` must share one hidden concrete type.** | [Erased Validator Registry](../labs/module-05-erased-validator-registry/README.md) |
| 6 | [96 — Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits](./module-96-auditing-unsafe-abstractions-validity-provenance-drop-panic-and-auto-traits/index.md) | What exact proof makes a safe API implemented with unsafe code sound across every constructor, method, failure path, destructor, and thread-safety claim? | **Write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation.** | [Inline Batch](../labs/module-06-inline-batch/README.md) |
| 7 | [97 — From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size](./module-97-from-source-to-machine-code-monomorphization-dispatch-layout-and-code-size/index.md) | How do type-level architecture and compiler decisions become concrete symbols, call paths, layouts, and artifact size—and which observations are stable enough to guide design? | **Explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication.** | [Dispatch Observatory](../labs/module-07-dispatch-observatory/README.md) |
| 8 | [98 — Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration](./module-98-verification-beyond-examples-compile-fail-property-model-fuzz-miri-and-concurrency-exploration/index.md) | Which verification technique can falsify which kind of Rust claim, and how do you combine them without pretending that test volume equals proof? | **Classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims.** | [Model-Checked Log](../labs/module-08-model-checked-log/README.md) |
| 9 | [99 — Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship](./module-99-long-lived-apis-semver-msrv-features-migrations-and-workspace-stewardship/index.md) | How do you evolve a Rust library, data format, feature graph, and workspace without silently breaking downstream source, behavior, tools, or stored data? | **Analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data.** | [Versioned SDK](../labs/module-09-versioned-sdk/README.md) |
| 10 | [100 — Architectural Synthesis: Building and Defending a Long-Lived Rust System](./module-100-architectural-synthesis-building-and-defending-a-long-lived-rust-system/index.md) | Can you turn ten courses of mechanisms into one restrained architecture whose guarantees, unsafe core, verification evidence, compatibility policy, and operating limits can survive independent review? | **Construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy.** | [Architecture Council](../labs/module-10-architecture-council/README.md) |

The table is a dependency chain, not a menu. A later module may use an earlier mechanism but may not silently weaken its ownership, failure, ordering, capacity, safety, compatibility, or evidence contract.

## Decision rules

| Decision | Rule used throughout this course |
|---|---|
| Decisive phase | Use the earliest compiler, runtime, platform, or product phase that can establish the fact. |
| Advanced type | Derive GAT, HRTB, projection, const, or erasure machinery from a concrete relationship. |
| Unsafe review | Audit from every safe entry point through all states, drops, panics, and auto-trait consequences. |
| Verification | Map each claim to independent positive and causal negative evidence and state the remaining gap. |
| Evolution | Preserve callers, implementors, stored data, feature graphs, MSRV, artifacts, and migration paths deliberately. |

Use these rules during prediction and review. When a rule does not decide the case, write the missing product requirement instead of selecting an API by habit.

## The reasoning record

The ten module-specific records culminate in a **architecture defense record**. State the proof obligation, follow the compiler and abstraction boundary, select independent evidence, and defend compatibility under change. Keep the record small enough to inspect but complete enough to expose the first unsupported assumption.

## Scope and handoff

The course selects stable mechanisms that serve real product requirements. It does not reward obscure syntax, nightly-feature collecting, unsafe code retained for display, or lower-level compiler output used where source-level reasoning is already decisive.

The program ends with independent transfer: you should be able to enter an unfamiliar Rust system, identify its authorities and proof boundaries, make a cross-cutting change, and state what remains uncertain.

## Capstone — AxiomStore

AxiomStore is a versioned embedded record engine with lending views, const bounds, runtime validators, one private initialized-prefix abstraction, deterministic storage, migrations, compatibility fixtures, and a claim-specific verification matrix.

Open the [engineering guide](capstone.md) before Day 1 so the final architecture is visible. Implement only the current increment. The independent laboratory remains separate so that the mechanism can be learned without hiding behind accumulated capstone code.

## Completion

The course is complete when you can build and defend:

> Build a versioned embedded journal whose borrowed read API, runtime validators, bounded transaction representation, compatibility policy, unsafe-or-safe storage decision, and verification matrix are derived from an invariant ownership map.

and then change the capstone under this constraint:

> Implement the AXIOM02 format extension without creating a parallel validation or persistence architecture, and defend every compatibility and unsafe consequence.

A passing test suite is necessary. It is not sufficient unless you can explain why the tests are capable of falsifying the claim and which target-, scheduler-, workload-, peer-, or policy-dependent facts remain outside them.

## Continue

- [Ten-day plan](study-plan.md)
- [Module 91 — Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen](./module-91-reading-rust-through-the-compiler-hir-mir-borrow-checking-and-codegen/index.md)
- [AxiomStore engineering guide](capstone.md)
- [Course reference](reference.md)
- [Final review](final-review.md)
- [Compiler and design investigations](../compiler-labs/README.md)
- [Independent laboratories](../labs/)
