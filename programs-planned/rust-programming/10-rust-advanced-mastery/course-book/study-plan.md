# Ten-Day Study Plan — Rust Advanced Mastery

This course occupies ten focused days across two calendar weeks. The first five days establish compiler, trait, lifetime, const, and erasure reasoning. The second five days review unsafe abstractions, connect source to machine artifacts, build layered verification, govern evolution, and defend the final architecture.

Use an eight-to-ten-hour day with real breaks. The goal is not maximum page throughput. The goal is one independently reconstructable proof boundary per day.

## Day 1 — Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen

**Morning.** Read [Module 91](module-91-reading-rust-through-the-compiler-hir-mir-borrow-checking-and-codegen/index.md) and construct the compiler evidence ledger before compiling examples. Complete the frozen prediction section.

**Afternoon.** Build [Compiler Evidence Notebook](../labs/module-01-compiler-evidence-notebook/README.md). Start with the public contract and adversarial case, not with the reference implementation.

**Evening.** Apply the Module 91 AxiomStore increment, update the architecture and verification records, then reconstruct the module question without notes.

**Stop condition.** Do not advance until you can choose the earliest decisive compiler phase for a method-resolution, borrow, drop, and code-generation question, and can state what each observation leaves unknown.

## Day 2 — Advanced Trait Solving: Goals, Projections, and Type Equality

**Morning.** Read [Module 92](module-92-advanced-trait-solving-goals-projections-and-type-equality/index.md) and construct the trait-goal graph before compiling examples. Complete the frozen prediction section.

**Afternoon.** Build [Projection-Driven Pipeline](../labs/module-02-projection-driven-pipeline/README.md). Start with the public contract and adversarial case, not with the reference implementation.

**Evening.** Apply the Module 92 AxiomStore increment, update the architecture and verification records, then reconstruct the module question without notes.

**Stop condition.** Do not advance until you can draw a trait-goal graph, normalize an associated-type projection, locate the missing equality, and remove at least one unnecessary bound from a working API.

## Day 3 — GATs, Higher-Ranked Bounds, and Lending Interfaces

**Morning.** Read [Module 93](module-93-gats-higher-ranked-bounds-and-lending-interfaces/index.md) and construct the lifetime quantifier map before compiling examples. Complete the frozen prediction section.

**Afternoon.** Build [Lending Table](../labs/module-03-lending-table/README.md). Start with the public contract and adversarial case, not with the reference implementation.

**Evening.** Apply the Module 93 AxiomStore increment, update the architecture and verification records, then reconstruct the module question without notes.

**Stop condition.** Do not advance until you can say who chooses every lifetime in a GAT or higher-ranked bound, prove why a lent view cannot escape, and identify the exact boundary where retained data must become owned.

## Day 4 — Const Generics, Witness Types, and Compile-Time Invariants

**Morning.** Read [Module 94](module-94-const-generics-witness-types-and-compile-time-invariants/index.md) and construct the compile-time/runtime invariant table before compiling examples. Complete the frozen prediction section.

**Afternoon.** Build [Bounded Matrix](../labs/module-04-bounded-matrix/README.md). Start with the public contract and adversarial case, not with the reference implementation.

**Evening.** Apply the Module 94 AxiomStore increment, update the architecture and verification records, then reconstruct the module question without notes.

**Stop condition.** Do not advance until you can separate compile-time shape from runtime quantity, construct witnesses only through checked paths, and explain when a runtime value is simpler than another const parameter.

## Day 5 — Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries

**Morning.** Read [Module 95](module-95-opaque-and-erased-types-impl-trait-dyn-trait-any-and-plugin-boundaries/index.md) and construct the variation and erasure map before compiling examples. Complete the frozen prediction section.

**Afternoon.** Build [Erased Validator Registry](../labs/module-05-erased-validator-registry/README.md). Start with the public contract and adversarial case, not with the reference implementation.

**Evening.** Apply the Module 95 AxiomStore increment, update the architecture and verification records, then reconstruct the module question without notes.

**Stop condition.** Do not advance until you can choose among enums, generics, `impl Trait`, trait objects, and `Any` from the extension requirement, and can name the information erased at each boundary.

## Day 6 — Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits

**Morning.** Read [Module 96](module-96-auditing-unsafe-abstractions-validity-provenance-drop-panic-and-auto-traits/index.md) and construct the unsafe abstraction safety dossier before compiling examples. Complete the frozen prediction section.

**Afternoon.** Build [Audited Inline Batch](../labs/module-06-inline-batch/README.md). Start with the public contract and adversarial case, not with the reference implementation.

**Evening.** Apply the Module 96 AxiomStore increment, update the architecture and verification records, then reconstruct the module question without notes.

**Stop condition.** Do not advance until you can review `InlineBatch` from every safe entry point, reconstruct the initialized-prefix and drop proof, and decide whether the safe `Vec` alternative should replace it.

## Day 7 — From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size

**Morning.** Read [Module 97](module-97-from-source-to-machine-code-monomorphization-dispatch-layout-and-code-size/index.md) and construct the source-to-artifact observation record before compiling examples. Complete the frozen prediction section.

**Afternoon.** Build [Dispatch Observatory](../labs/module-07-dispatch-observatory/README.md). Start with the public contract and adversarial case, not with the reference implementation.

**Evening.** Apply the Module 97 AxiomStore increment, update the architecture and verification records, then reconstruct the module question without notes.

**Stop condition.** Do not advance until you can distinguish semantic dispatch guarantees from artifact observations, compare static, enum, and dynamic paths fairly, and scope every size or assembly claim to one build.

## Day 8 — Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration

**Morning.** Read [Module 98](module-98-verification-beyond-examples-compile-fail-property-model-fuzz-miri-and-concurrency-exploration/index.md) and construct the claim-to-evidence verification matrix before compiling examples. Complete the frozen prediction section.

**Afternoon.** Build [Model-Checked Log](../labs/module-08-model-checked-log/README.md). Start with the public contract and adversarial case, not with the reference implementation.

**Evening.** Apply the Module 98 AxiomStore increment, update the architecture and verification records, then reconstruct the module question without notes.

**Stop condition.** Do not advance until each important claim has a primary falsification method, causal negative space, an independent oracle where possible, and an explicit statement of what passing evidence cannot establish.

## Day 9 — Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship

**Morning.** Read [Module 99](module-99-long-lived-apis-semver-msrv-features-migrations-and-workspace-stewardship/index.md) and construct the compatibility and migration matrix before compiling examples. Complete the frozen prediction section.

**Afternoon.** Build [Versioned SDK](../labs/module-09-versioned-sdk/README.md). Start with the public contract and adversarial case, not with the reference implementation.

**Evening.** Apply the Module 99 AxiomStore increment, update the architecture and verification records, then reconstruct the module question without notes.

**Stop condition.** Do not advance until you can name all compatibility stakeholders, read a feature/MSRV matrix, preserve immutable old-format fixtures, and design migration so failed conversion does not become partial adoption.

## Day 10 — Architectural Synthesis: Building and Defending a Long-Lived Rust System

**Morning.** Read [Module 100](module-100-architectural-synthesis-building-and-defending-a-long-lived-rust-system/index.md) and construct the architecture defense dossier before compiling examples. Complete the frozen prediction section.

**Afternoon.** Build [Architecture Council](../labs/module-10-architecture-council/README.md). Start with the public contract and adversarial case, not with the reference implementation.

**Evening.** Apply the Module 100 AxiomStore increment, update the architecture and verification records, then reconstruct the module question without notes.

**Stop condition.** Finish only when the AXIOM02 extension fits the existing invariant map, the unsafe and compatibility dossiers are current, and you can remove an unjustified advanced mechanism without destabilizing the product.

## Weekend repair

After Day 5, rebuild the variation map from memory and re-run the first five laboratories without consulting solutions. After Day 10, perform the full architecture defense on a fresh checkout and implement one additional small compatibility change of your own.
