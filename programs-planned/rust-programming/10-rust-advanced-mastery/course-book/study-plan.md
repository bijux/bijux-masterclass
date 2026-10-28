# Course 10 Study Plan — Advanced Rust Mastery

Ten dense study days fit into two calendar weeks. The goal is not to maximize reading time; it is to make **How do you design and evolve a Rust system whose type relationships, unsafe boundaries, compiler behavior, compatibility promises, verification evidence, and operating limits survive independent change?** answerable through construction and explanation.

## Daily rhythm

Use a **architecture defense record** across the course. Each day begins by reconstructing yesterday’s decisive relationship and ends by tracing one capstone invariant. Preserve the first prediction, the observed result, the principled repair, and the shortcut you rejected.

## Day 1 — Module 91: Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen

**Question:** When difficult Rust code surprises you, which compiler representation and which proof obligation actually decide the result?

**Retrieval:** Without notes, restate the invariant carried from Module 90 — Production Readiness, Capacity Planning, Rollouts, and Incident Learning. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 91](./module-91-reading-rust-through-the-compiler-hir-mir-borrow-checking-and-codegen/index.md) with a **compiler-phase record** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-91-reading-rust-through-the-compiler-hir-mir-borrow-checking-and-codegen/workbook.md) before observation. The day’s minimum result is: **Separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Compiler Evidence Notebook](../labs/module-01-compiler-evidence-notebook/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 91 in the [AxiomStore guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases.** End with one simpler design that would be preferable under a narrower requirement.

## Day 2 — Module 92: Advanced Trait Solving: Goals, Projections, and Type Equality

**Question:** How do you design and debug APIs when the compiler must prove nested trait goals and normalize associated types before ordinary operations become legal?

**Retrieval:** Without notes, restate the invariant carried from Module 91 — Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 92](./module-92-advanced-trait-solving-goals-projections-and-type-equality/index.md) with a **trait-goal and projection graph** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-92-advanced-trait-solving-goals-projections-and-type-equality/workbook.md) before observation. The day’s minimum result is: **Rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Projection-Driven Pipeline](../labs/module-02-projection-driven-pipeline/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 92 in the [AxiomStore guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints.** End with one simpler design that would be preferable under a narrower requirement.

## Day 3 — Module 93: GATs, Higher-Ranked Bounds, and Lending Interfaces

**Question:** How can an API return views tied to each borrow of `self` without pretending that every yielded value has one fixed lifetime?

**Retrieval:** Without notes, restate the invariant carried from Module 92 — Advanced Trait Solving: Goals, Projections, and Type Equality. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 93](./module-93-gats-higher-ranked-bounds-and-lending-interfaces/index.md) with a **lifetime family map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-93-gats-higher-ranked-bounds-and-lending-interfaces/workbook.md) before observation. The day’s minimum result is: **Distinguish one associated type from a lifetime-indexed family of associated types.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Lending Table](../labs/module-03-lending-table/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 93 in the [AxiomStore guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish one associated type from a lifetime-indexed family of associated types.** End with one simpler design that would be preferable under a narrower requirement.

## Day 4 — Module 94: Const Generics, Witness Types, and Compile-Time Invariants

**Question:** Which numeric and state facts belong in types, which remain runtime data, and how do you avoid turning a library into an unusable type-level calculator?

**Retrieval:** Without notes, restate the invariant carried from Module 93 — GATs, Higher-Ranked Bounds, and Lending Interfaces. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 94](./module-94-const-generics-witness-types-and-compile-time-invariants/index.md) with a **const witness proof** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-94-const-generics-witness-types-and-compile-time-invariants/workbook.md) before observation. The day’s minimum result is: **Use const parameters when a numeric fact changes representation, layout, or legal composition.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Bounded Matrix](../labs/module-04-bounded-matrix/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 94 in the [AxiomStore guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Use const parameters when a numeric fact changes representation, layout, or legal composition.** End with one simpler design that would be preferable under a narrower requirement.

## Day 5 — Module 95: Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries

**Question:** When should an API hide one concrete type, erase many concrete types behind a contract, or preserve explicit variants—and what information is lost at each boundary?

**Retrieval:** Without notes, restate the invariant carried from Module 94 — Const Generics, Witness Types, and Compile-Time Invariants. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 95](./module-95-opaque-and-erased-types-impl-trait-dyn-trait-any-and-plugin-boundaries/index.md) with a **open and erased variation map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-95-opaque-and-erased-types-impl-trait-dyn-trait-any-and-plugin-boundaries/workbook.md) before observation. The day’s minimum result is: **Distinguish opaque return types from trait objects and explain why different branches of `impl Trait` must share one hidden concrete type.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Erased Validator Registry](../labs/module-05-erased-validator-registry/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 95 in the [AxiomStore guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish opaque return types from trait objects and explain why different branches of `impl Trait` must share one hidden concrete type.** End with one simpler design that would be preferable under a narrower requirement.

## Midpoint reconstruction

Do not add a sixth topic on the recovery day. Reconstruct **Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen, Advanced Trait Solving: Goals, Projections, and Type Equality, GATs, Higher-Ranked Bounds, and Lending Interfaces, Const Generics, Witness Types, and Compile-Time Invariants, Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries** as one dependency chain, rerun the two investigations that changed your model most, and describe the current AxiomStore state from an empty page. Repair incomplete work, then take a real break; consolidation is part of the course rather than unused time.

## Day 6 — Module 96: Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits

**Question:** What exact proof makes a safe API implemented with unsafe code sound across every constructor, method, failure path, destructor, and thread-safety claim?

**Retrieval:** Without notes, restate the invariant carried from Module 95 — Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 96](./module-96-auditing-unsafe-abstractions-validity-provenance-drop-panic-and-auto-traits/index.md) with a **unsafe state-and-operation dossier** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-96-auditing-unsafe-abstractions-validity-provenance-drop-panic-and-auto-traits/workbook.md) before observation. The day’s minimum result is: **Write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Inline Batch](../labs/module-06-inline-batch/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 96 in the [AxiomStore guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation.** End with one simpler design that would be preferable under a narrower requirement.

## Day 7 — Module 97: From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size

**Question:** How do type-level architecture and compiler decisions become concrete symbols, call paths, layouts, and artifact size—and which observations are stable enough to guide design?

**Retrieval:** Without notes, restate the invariant carried from Module 96 — Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 97](./module-97-from-source-to-machine-code-monomorphization-dispatch-layout-and-code-size/index.md) with a **source-to-artifact observation** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-97-from-source-to-machine-code-monomorphization-dispatch-layout-and-code-size/workbook.md) before observation. The day’s minimum result is: **Explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Dispatch Observatory](../labs/module-07-dispatch-observatory/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 97 in the [AxiomStore guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication.** End with one simpler design that would be preferable under a narrower requirement.

## Day 8 — Module 98: Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration

**Question:** Which verification technique can falsify which kind of Rust claim, and how do you combine them without pretending that test volume equals proof?

**Retrieval:** Without notes, restate the invariant carried from Module 97 — From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 98](./module-98-verification-beyond-examples-compile-fail-property-model-fuzz-miri-and-concurrency-exploration/index.md) with a **verification claim matrix** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-98-verification-beyond-examples-compile-fail-property-model-fuzz-miri-and-concurrency-exploration/workbook.md) before observation. The day’s minimum result is: **Classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Model-Checked Log](../labs/module-08-model-checked-log/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 98 in the [AxiomStore guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims.** End with one simpler design that would be preferable under a narrower requirement.

## Day 9 — Module 99: Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship

**Question:** How do you evolve a Rust library, data format, feature graph, and workspace without silently breaking downstream source, behavior, tools, or stored data?

**Retrieval:** Without notes, restate the invariant carried from Module 98 — Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 99](./module-99-long-lived-apis-semver-msrv-features-migrations-and-workspace-stewardship/index.md) with a **compatibility and migration matrix** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-99-long-lived-apis-semver-msrv-features-migrations-and-workspace-stewardship/workbook.md) before observation. The day’s minimum result is: **Analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Versioned SDK](../labs/module-09-versioned-sdk/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 99 in the [AxiomStore guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data.** End with one simpler design that would be preferable under a narrower requirement.

## Day 10 — Module 100: Architectural Synthesis: Building and Defending a Long-Lived Rust System

**Question:** Can you turn ten courses of mechanisms into one restrained architecture whose guarantees, unsafe core, verification evidence, compatibility policy, and operating limits can survive independent review?

**Retrieval:** Without notes, restate the invariant carried from Module 99 — Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 100](./module-100-architectural-synthesis-building-and-defending-a-long-lived-rust-system/index.md) with a **architecture defense record** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-100-architectural-synthesis-building-and-defending-a-long-lived-rust-system/workbook.md) before observation. The day’s minimum result is: **Construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Architecture Council](../labs/module-10-architecture-council/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 100 in the [AxiomStore guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy.** End with one simpler design that would be preferable under a narrower requirement.

## Final integration

After Day 10, complete the [final review](final-review.md), run the strongest available course route, and implement this unseen capstone change: **Implement the AXIOM02 format extension without creating a parallel validation or persistence architecture, and defend every compatibility and unsafe consequence.**

Seven days later, rebuild the ten-module sequence and the core **architecture defense record** without the book. Write a fresh example for every relationship you cannot recover. Re-reading a solution without recreating the model does not count as retained learning.
