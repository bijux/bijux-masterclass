# 06. Programming Languages: Metaprogramming

**Program code:** `META`

**Purpose:** Develop disciplined command of programs that inspect, generate, transform, or specialize programs while preserving readability, safety, tooling, and compatibility.

**Level-II professional outcome:** Ready to build and review macros, decorators, annotation processors, schema/code generators, typed derivation systems, build-time generators, and embedded DSLs.

**Prerequisites:** Programming Languages & Semantics Level I; one statically typed and one dynamic language; basic compiler front-end concepts.

**Primary ownership:** textual and syntactic macros; reflection; annotations and decorators; generics and templates as metaprogramming; AST transformation; code generation; staging and specialization; typed metaprogramming; DSL construction; metaprogramming governance.

**Explicit exclusions:** full parsing and compiler back ends (Program 08); general language semantics (Program 01); software pattern catalogues (Program 11).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Metaprogramming Models and Boundaries

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Programs About Programs** | `001-programs-about-programs.md` |
| 002 | **Compile-Time, Build-Time, Load-Time, and Run-Time Metaprogramming** | `002-compile-time-build-time-load-time-and-run-time-metaprogramming.md` |
| 003 | **Text Substitution and Its Failure Modes** | `003-text-substitution-and-its-failure-modes.md` |
| 004 | **Syntactic Structure Versus Textual Structure** | `004-syntactic-structure-versus-textual-structure.md` |
| 005 | **Reflection and Introspection** | `005-reflection-and-introspection.md` |
| 006 | **Code Generation from Structured Models** | `006-code-generation-from-structured-models.md` |
| 007 | **Declarative Versus Procedural Generation** | `007-declarative-versus-procedural-generation.md` |
| 008 | **Generated Code as a Maintained Artifact** | `008-generated-code-as-a-maintained-artifact.md` |
| 009 | **Choosing Metaprogramming Instead of Ordinary Abstraction** | `009-choosing-metaprogramming-instead-of-ordinary-abstraction.md` |
| 010 | **Establishing a Metaprogramming Safety Boundary** | `010-establishing-a-metaprogramming-safety-boundary.md` |

### Block 02 — Macros and Syntactic Transformation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Preprocessor Macros and Conditional Compilation** | `011-preprocessor-macros-and-conditional-compilation.md` |
| 012 | **Expression and Statement Macros** | `012-expression-and-statement-macros.md` |
| 013 | **Macro Expansion Order** | `013-macro-expansion-order.md` |
| 014 | **Name Capture and Accidental Binding** | `014-name-capture-and-accidental-binding.md` |
| 015 | **Hygienic Macro Principles** | `015-hygienic-macro-principles.md` |
| 016 | **Pattern-Based Macros** | `016-pattern-based-macros.md` |
| 017 | **Procedural Macros** | `017-procedural-macros.md` |
| 018 | **Quasiquotation and Unquotation** | `018-quasiquotation-and-unquotation.md` |
| 019 | **Source Locations and Diagnostic Preservation** | `019-source-locations-and-diagnostic-preservation.md` |
| 020 | **Testing Macro Expansion** | `020-testing-macro-expansion.md` |

### Block 03 — Reflection, Annotations, and Decorators

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Runtime Type and Member Inspection** | `021-runtime-type-and-member-inspection.md` |
| 022 | **Annotations and Metadata** | `022-annotations-and-metadata.md` |
| 023 | **Decorators and Function Wrapping** | `023-decorators-and-function-wrapping.md` |
| 024 | **Dynamic Attribute and Method Access** | `024-dynamic-attribute-and-method-access.md` |
| 025 | **Proxy Objects and Interception** | `025-proxy-objects-and-interception.md` |
| 026 | **Dependency Injection Through Reflection** | `026-dependency-injection-through-reflection.md` |
| 027 | **Serialization Through Metadata** | `027-serialization-through-metadata.md` |
| 028 | **Validation Through Annotations** | `028-validation-through-annotations.md` |
| 029 | **Reflection Cost and Caching** | `029-reflection-cost-and-caching.md` |
| 030 | **Containing Reflection Behind Typed Interfaces** | `030-containing-reflection-behind-typed-interfaces.md` |

### Block 04 — Generics, Templates, and Derivation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Parametric Generics as Compile-Time Abstraction** | `031-parametric-generics-as-compile-time-abstraction.md` |
| 032 | **C++ Template Instantiation** | `032-c-template-instantiation.md` |
| 033 | **Template Specialization and Selection** | `033-template-specialization-and-selection.md` |
| 034 | **Type Traits and Compile-Time Queries** | `034-type-traits-and-compile-time-queries.md` |
| 035 | **Const Evaluation and Compile-Time Functions** | `035-const-evaluation-and-compile-time-functions.md` |
| 036 | **Generic Derivation for Equality and Serialization** | `036-generic-derivation-for-equality-and-serialization.md` |
| 037 | **Trait and Type-Class Derivation** | `037-trait-and-type-class-derivation.md` |
| 038 | **Phantom Types and Compile-Time State** | `038-phantom-types-and-compile-time-state.md` |
| 039 | **Type-Level Lists and Heterogeneous Structures** | `039-type-level-lists-and-heterogeneous-structures.md` |
| 040 | **Controlling Template Complexity and Diagnostics** | `040-controlling-template-complexity-and-diagnostics.md` |

### Block 05 — Practical Code Generation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Schema-Driven Code Generation** | `041-schema-driven-code-generation.md` |
| 042 | **API Client and Server Stub Generation** | `042-api-client-and-server-stub-generation.md` |
| 043 | **Database Model Generation** | `043-database-model-generation.md` |
| 044 | **Parser and Serializer Generation** | `044-parser-and-serializer-generation.md` |
| 045 | **Configuration Model Generation** | `045-configuration-model-generation.md` |
| 046 | **Build-System Integration** | `046-build-system-integration.md` |
| 047 | **Deterministic and Reproducible Generation** | `047-deterministic-and-reproducible-generation.md` |
| 048 | **Incremental Regeneration and Change Detection** | `048-incremental-regeneration-and-change-detection.md` |
| 049 | **Golden Tests for Generated Output** | `049-golden-tests-for-generated-output.md` |
| 050 | **Designing a Maintainable Generator Interface** | `050-designing-a-maintainable-generator-interface.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Macro Systems and Hygiene

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Lexical Context and Scope Sets** | `051-lexical-context-and-scope-sets.md` |
| 052 | **Marks, Renaming, and Hygienic Expansion** | `052-marks-renaming-and-hygienic-expansion.md` |
| 053 | **Intentional Capture** | `053-intentional-capture.md` |
| 054 | **Phase Separation** | `054-phase-separation.md` |
| 055 | **Compile-Time Environments** | `055-compile-time-environments.md` |
| 056 | **Macro-Defining Macros** | `056-macro-defining-macros.md` |
| 057 | **Expansion as a Compiler Pass** | `057-expansion-as-a-compiler-pass.md` |
| 058 | **Typed Macro Expansion** | `058-typed-macro-expansion.md` |
| 059 | **Macro Debuggers and Expansion Traces** | `059-macro-debuggers-and-expansion-traces.md` |
| 060 | **Designing a Composable Macro System** | `060-designing-a-composable-macro-system.md` |

### Block 07 — Staging, Specialization, and Partial Evaluation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Multi-Stage Programming** | `061-multi-stage-programming.md` |
| 062 | **Binding-Time Analysis** | `062-binding-time-analysis.md` |
| 063 | **Static and Dynamic Expressions** | `063-static-and-dynamic-expressions.md` |
| 064 | **Partial Evaluation** | `064-partial-evaluation.md` |
| 065 | **Program Specialization** | `065-program-specialization.md` |
| 066 | **Generating Loops and Kernels** | `066-generating-loops-and-kernels.md` |
| 067 | **Staged Interpreters** | `067-staged-interpreters.md` |
| 068 | **Just-in-Time Specialization** | `068-just-in-time-specialization.md` |
| 069 | **Cross-Stage Persistence** | `069-cross-stage-persistence.md` |
| 070 | **Evaluating the Cost Model of Staged Code** | `070-evaluating-the-cost-model-of-staged-code.md` |

### Block 08 — Typed and Dependently Typed Metaprogramming

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Types as Compile-Time Data** | `071-types-as-compile-time-data.md` |
| 072 | **Kind-Level Programming** | `072-kind-level-programming.md` |
| 073 | **Type Families and Associated Computations** | `073-type-families-and-associated-computations.md` |
| 074 | **GADTs for Typed Syntax** | `074-gadts-for-typed-syntax.md` |
| 075 | **Singleton Types** | `075-singleton-types.md` |
| 076 | **Dependent Pairs and Evidence Passing** | `076-dependent-pairs-and-evidence-passing.md` |
| 077 | **Compile-Time Proof Search** | `077-compile-time-proof-search.md` |
| 078 | **Elaboration from Rich Surface Syntax** | `078-elaboration-from-rich-surface-syntax.md` |
| 079 | **Typed Generic Programming** | `079-typed-generic-programming.md` |
| 080 | **Keeping Type-Level Programs Comprehensible** | `080-keeping-type-level-programs-comprehensible.md` |

### Block 09 — Domain-Specific Languages

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **External and Embedded DSL Trade-Offs** | `081-external-and-embedded-dsl-trade-offs.md` |
| 082 | **Fluent Interfaces as Shallow DSLs** | `082-fluent-interfaces-as-shallow-dsls.md` |
| 083 | **Tagless-Final DSLs** | `083-tagless-final-dsls.md` |
| 084 | **Free Encodings for Embedded DSLs** | `084-free-encodings-for-embedded-dsls.md` |
| 085 | **Typed Query DSLs** | `085-typed-query-dsls.md` |
| 086 | **Build and Configuration DSLs** | `086-build-and-configuration-dsls.md` |
| 087 | **Rule and Policy Languages** | `087-rule-and-policy-languages.md` |
| 088 | **Staged Numerical DSLs** | `088-staged-numerical-dsls.md` |
| 089 | **Source Mapping and DSL Diagnostics** | `089-source-mapping-and-dsl-diagnostics.md` |
| 090 | **Evolving a DSL Without Trapping Its Users** | `090-evolving-a-dsl-without-trapping-its-users.md` |

### Block 10 — Production Metaprogramming Engineering

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Versioning Generators and Generated Interfaces** | `091-versioning-generators-and-generated-interfaces.md` |
| 092 | **Security Risks in Code Generation and Evaluation** | `092-security-risks-in-code-generation-and-evaluation.md` |
| 093 | **Sandboxing User-Supplied Metaprograms** | `093-sandboxing-user-supplied-metaprograms.md` |
| 094 | **Static Analysis of Generated Code** | `094-static-analysis-of-generated-code.md` |
| 095 | **Debugging Across Generated and Source Layers** | `095-debugging-across-generated-and-source-layers.md` |
| 096 | **IDE, Refactoring, and Language-Server Support** | `096-ide-refactoring-and-language-server-support.md` |
| 097 | **Performance Budgets for Compile-Time Computation** | `097-performance-budgets-for-compile-time-computation.md` |
| 098 | **Migration Away from Overused Metaprogramming** | `098-migration-away-from-overused-metaprogramming.md` |
| 099 | **Reviewing Metaprogramming for Transparency and Necessity** | `099-reviewing-metaprogramming-for-transparency-and-necessity.md` |
| 100 | **Designing a Governed Metaprogramming Platform** | `100-designing-a-governed-metaprogramming-platform.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
