# Rust Advanced Mastery

## Compiler Reasoning, Type Architecture, and Long-Lived Systems

This is Course 10 of the Rust Programming path and covers Modules 91–100. It is the program’s synthesis course. Its purpose is not to collect every unstable or obscure feature. It teaches you to read difficult Rust through the right compiler and runtime models, design advanced type relationships deliberately, audit unsafe abstractions as complete safe products, connect source choices to machine artifacts, select verification evidence by claim, and evolve a library and stored format without abandoning earlier guarantees.

The cumulative capstone is **AxiomStore**, a versioned embedded record engine. AxiomStore deliberately combines several mechanisms but gives each one a narrow responsibility:

- a GAT-based static codec lends record views from immutable snapshots;
- const parameters bound record and transaction representation;
- a trait-object registry supports runtime validation policy;
- one private `InlineBatch<T, N>` owns the unsafe initialized-prefix proof;
- an enum owns the closed set of built-in archive versions;
- compatibility fixtures and migrations preserve legacy data;
- a verification matrix connects every claim to evidence;
- artifact observations are scoped to a pinned build rather than promoted to language rules.

## The central discipline

Every design decision must answer seven questions:

1. Which product invariant needs an owner?
2. Which phase or runtime event can establish it?
3. Why is this mechanism stronger than a simpler alternative?
4. Which new proof obligation does the mechanism create?
5. Which downstream code, data, feature, toolchain, or artifact becomes a stakeholder?
6. Which evidence can falsify the claim?
7. Which residual risk remains after the evidence passes?

Course 10 is successful when your architecture becomes more restrained, not when it contains more advanced syntax.

## Prerequisites

Begin after completing Courses 1–9 or equivalent work. You should already be able to:

- build multi-crate libraries and binaries;
- reason about ownership, lifetimes, GAT-adjacent associated types, variance, pinning, trait objects, macros, unsafe boundaries, concurrency, async services, and production evidence;
- maintain a safe behavioral oracle while changing implementation mechanisms;
- distinguish language guarantees, library contracts, target observations, unsafe obligations, product policy, and measured artifact claims;
- version persistent data and implement bounded, failure-atomic operations.

Use the [course overview](course-book/index.md) for a concrete readiness diagnosis.

## Ten modules

91. [Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen](course-book/module-91-reading-rust-through-the-compiler-hir-mir-borrow-checking-and-codegen/index.md)
92. [Advanced Trait Solving: Goals, Projections, and Type Equality](course-book/module-92-advanced-trait-solving-goals-projections-and-type-equality/index.md)
93. [GATs, Higher-Ranked Bounds, and Lending Interfaces](course-book/module-93-gats-higher-ranked-bounds-and-lending-interfaces/index.md)
94. [Const Generics, Witness Types, and Compile-Time Invariants](course-book/module-94-const-generics-witness-types-and-compile-time-invariants/index.md)
95. [Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries](course-book/module-95-opaque-and-erased-types-impl-trait-dyn-trait-any-and-plugin-boundaries/index.md)
96. [Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits](course-book/module-96-auditing-unsafe-abstractions-validity-provenance-drop-panic-and-auto-traits/index.md)
97. [From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size](course-book/module-97-from-source-to-machine-code-monomorphization-dispatch-layout-and-code-size/index.md)
98. [Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration](course-book/module-98-verification-beyond-examples-compile-fail-property-model-fuzz-miri-and-concurrency-exploration/index.md)
99. [Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship](course-book/module-99-long-lived-apis-semver-msrv-features-migrations-and-workspace-stewardship/index.md)
100. [Architectural Synthesis: Building and Defending a Long-Lived Rust System](course-book/module-100-architectural-synthesis-building-and-defending-a-long-lived-rust-system/index.md)

## Ten independent laboratories

| Day | Laboratory | Proof surface |
|---:|---|---|
| 1 | Compiler Evidence Notebook | phase classification, place/drop trace, artifact-scoped observation |
| 2 | Projection-Driven Pipeline | associated families, equality constraints, typed error composition |
| 3 | Lending Table | GAT views, higher-ranked access, non-escape, owned conversion |
| 4 | Bounded Matrix | const shape, witness construction, runtime/compile-time separation |
| 5 | Erased Validator Registry | dyn compatibility, ownership, ordering, open versus closed variation |
| 6 | Audited Inline Batch | initialized prefix, panic/drop paths, auto-trait review |
| 7 | Dispatch Observatory | static/enum/dyn parity and artifact-scoped size evidence |
| 8 | Model-Checked Log | transition model, bounded exploration, verification gaps |
| 9 | Versioned SDK | callers, implementors, MSRV, features, fixtures, migration |
| 10 | Architecture Council | invariant ownership, mechanism rejection, unseen evolution |

Every lab has a usable starter and a complete reference implementation. The reference is one defended design, not a fill-in answer key.

## Course-book route

- [Course overview](course-book/index.md)
- [Ten-day study plan](course-book/study-plan.md)
- [AxiomStore engineering guide](course-book/capstone.md)
- [Advanced reference desk](course-book/reference.md)
- [Final independent review](course-book/final-review.md)
- [Compiler investigations](compiler-labs/README.md)
- [Laboratories](labs/)

## Commands

```bash
make static-proof
make compiler-labs
make check
make test
make starters
make fmt
make clippy
make docs
make proof
```

`make proof` is the strongest supplied route. It requires the pinned Rust toolchain and MkDocs. Optional Miri, fuzzing, symbol, and assembly investigations are described in the course book but remain separate because their availability and target behavior vary.

## Completion

Complete the course only after:

- all ten workbooks are frozen and reviewed;
- all ten independent labs and transfer tasks work;
- AxiomStore passes its complete test surface;
- the AXIOM02 extension is implemented without a step-by-step recipe;
- the unsafe dossier has been reviewed independently;
- the compatibility and verification matrices are current;
- the final architecture defense names at least five mechanisms deliberately rejected;
- residual risks are recorded rather than hidden behind a global completion claim.
