# 03. Programming Languages: Functional Programming

**Program code:** `FP`

**Purpose:** Develop practical and theoretical command of programming with immutable values, first-class functions, algebraic data, compositional effects, and equational reasoning.

**Level-II professional outcome:** Ready to build and review production functional or functional-first software in Haskell, Scala, F#, OCaml, Clojure, Rust, or functional Python ecosystems.

**Prerequisites:** Programming Languages & Semantics Level I; recursion and data structures; basic discrete mathematics.

**Primary ownership:** pure functions; immutable data; higher-order programming; algebraic data types; pattern matching; lazy and strict FP; effect composition; functional architecture; functional concurrency; equational reasoning.

**Explicit exclusions:** general PL semantics (Program 01); formal programming theory (Program 07); general software design (Program 09); distributed-system algorithms (Program 27).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Functional Values and Evaluation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Expressions, Values, and Referential Transparency** | `001-expressions-values-and-referential-transparency.md` |
| 002 | **Pure Functions and Explicit Inputs** | `002-pure-functions-and-explicit-inputs.md` |
| 003 | **First-Class and Higher-Order Functions** | `003-first-class-and-higher-order-functions.md` |
| 004 | **Lexical Closures in Functional Programs** | `004-lexical-closures-in-functional-programs.md` |
| 005 | **Function Composition and Pipelines** | `005-function-composition-and-pipelines.md` |
| 006 | **Partial Application and Currying** | `006-partial-application-and-currying.md` |
| 007 | **Strict and Non-Strict Evaluation** | `007-strict-and-non-strict-evaluation.md` |
| 008 | **Immutable Bindings and Persistent State** | `008-immutable-bindings-and-persistent-state.md` |
| 009 | **Expression-Oriented Control Flow** | `009-expression-oriented-control-flow.md` |
| 010 | **Translating Imperative Code into Functional Form** | `010-translating-imperative-code-into-functional-form.md` |

### Block 02 — Recursion and Structural Computation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Recursive Definitions and Base Cases** | `011-recursive-definitions-and-base-cases.md` |
| 012 | **Structural Recursion over Lists** | `012-structural-recursion-over-lists.md` |
| 013 | **Tail Recursion and Accumulator Design** | `013-tail-recursion-and-accumulator-design.md` |
| 014 | **Mutual Recursion** | `014-mutual-recursion.md` |
| 015 | **Recursive Trees and Rose Trees** | `015-recursive-trees-and-rose-trees.md` |
| 016 | **Divide-and-Conquer in Functional Style** | `016-divide-and-conquer-in-functional-style.md` |
| 017 | **Map, Filter, and FlatMap** | `017-map-filter-and-flatmap.md` |
| 018 | **Left and Right Folds** | `018-left-and-right-folds.md` |
| 019 | **Unfolds and Generative Recursion** | `019-unfolds-and-generative-recursion.md` |
| 020 | **Deriving Recursive Programs from Data Definitions** | `020-deriving-recursive-programs-from-data-definitions.md` |

### Block 03 — Algebraic Data and Pattern Matching

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Product Types and Records** | `021-product-types-and-records.md` |
| 022 | **Sum Types and Variants** | `022-sum-types-and-variants.md` |
| 023 | **Recursive Algebraic Data Types** | `023-recursive-algebraic-data-types.md` |
| 024 | **Pattern Matching and Exhaustiveness** | `024-pattern-matching-and-exhaustiveness.md` |
| 025 | **Option Types and Explicit Absence** | `025-option-types-and-explicit-absence.md` |
| 026 | **Result Types and Explicit Failure** | `026-result-types-and-explicit-failure.md` |
| 027 | **Smart Constructors and Validated Data** | `027-smart-constructors-and-validated-data.md` |
| 028 | **Newtypes and Domain-Specific Types** | `028-newtypes-and-domain-specific-types.md` |
| 029 | **Phantom Types and Compile-Time Distinctions** | `029-phantom-types-and-compile-time-distinctions.md` |
| 030 | **Modeling State Machines with Algebraic Data** | `030-modeling-state-machines-with-algebraic-data.md` |

### Block 04 — Polymorphism and Functional Abstraction

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Parametric Polymorphism in Functional Code** | `031-parametric-polymorphism-in-functional-code.md` |
| 032 | **Type Inference and Principal Types** | `032-type-inference-and-principal-types.md` |
| 033 | **Ad Hoc Polymorphism and Type Classes** | `033-ad-hoc-polymorphism-and-type-classes.md` |
| 034 | **Functorial Mapping** | `034-functorial-mapping.md` |
| 035 | **Applicative Structure** | `035-applicative-structure.md` |
| 036 | **Monadic Sequencing** | `036-monadic-sequencing.md` |
| 037 | **Semigroups and Monoids** | `037-semigroups-and-monoids.md` |
| 038 | **Foldable and Traversable Structures** | `038-foldable-and-traversable-structures.md` |
| 039 | **Generic Functional Programming** | `039-generic-functional-programming.md` |
| 040 | **Reading Types as Design Specifications** | `040-reading-types-as-design-specifications.md` |

### Block 05 — Effects, Errors, and Functional Programs

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Separating Pure Logic from Effects** | `041-separating-pure-logic-from-effects.md` |
| 042 | **Functional Error Handling** | `042-functional-error-handling.md` |
| 043 | **State Passing and the State Abstraction** | `043-state-passing-and-the-state-abstraction.md` |
| 044 | **Reader-Style Dependency Passing** | `044-reader-style-dependency-passing.md` |
| 045 | **Writer-Style Accumulation** | `045-writer-style-accumulation.md` |
| 046 | **Input and Output at the Program Boundary** | `046-input-and-output-at-the-program-boundary.md` |
| 047 | **Parsing with Combinators** | `047-parsing-with-combinators.md` |
| 048 | **Validation with Independent Errors** | `048-validation-with-independent-errors.md` |
| 049 | **Property-Based Testing of Pure Functions** | `049-property-based-testing-of-pure-functions.md` |
| 050 | **Organizing a Functional Application into a Pure Core and Impure Shell** | `050-organizing-a-functional-application-into-a-pure-core-and-impure-shell.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Lambda Calculus and Functional Foundations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Untyped Lambda Terms and Binding** | `051-untyped-lambda-terms-and-binding.md` |
| 052 | **Alpha Equivalence and Capture Avoidance** | `052-alpha-equivalence-and-capture-avoidance.md` |
| 053 | **Beta Reduction and Substitution** | `053-beta-reduction-and-substitution.md` |
| 054 | **Normal Forms and Evaluation Strategies** | `054-normal-forms-and-evaluation-strategies.md` |
| 055 | **Church Encodings** | `055-church-encodings.md` |
| 056 | **Fixed-Point Combinators** | `056-fixed-point-combinators.md` |
| 057 | **Simply Typed Lambda Calculus for Functional Programmers** | `057-simply-typed-lambda-calculus-for-functional-programmers.md` |
| 058 | **System F in Functional Programming** | `058-system-f-in-functional-programming.md` |
| 059 | **Lambda Calculus as an Intermediate Language** | `059-lambda-calculus-as-an-intermediate-language.md` |
| 060 | **Relating Lambda Calculus to Real Functional Languages** | `060-relating-lambda-calculus-to-real-functional-languages.md` |

### Block 07 — Advanced Functional Types and Effects

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Higher-Kinded Types in Practice** | `061-higher-kinded-types-in-practice.md` |
| 062 | **GADTs in Functional Program Design** | `062-gadts-in-functional-program-design.md` |
| 063 | **Existential Packaging and Module Abstraction** | `063-existential-packaging-and-module-abstraction.md` |
| 064 | **Type-Level Programming** | `064-type-level-programming.md` |
| 065 | **Refinement and Dependent-Type Techniques** | `065-refinement-and-dependent-type-techniques.md` |
| 066 | **Free Structures for Effectful Programs** | `066-free-structures-for-effectful-programs.md` |
| 067 | **Tagless-Final Encodings** | `067-tagless-final-encodings.md` |
| 068 | **Algebraic Effects and Handlers** | `068-algebraic-effects-and-handlers.md` |
| 069 | **Effect Polymorphism** | `069-effect-polymorphism.md` |
| 070 | **Capability-Oriented Functional APIs** | `070-capability-oriented-functional-apis.md` |

### Block 08 — Recursion Schemes and Compositional Structure

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Catamorphisms Beyond Fold** | `071-catamorphisms-beyond-fold.md` |
| 072 | **Anamorphisms Beyond Unfold** | `072-anamorphisms-beyond-unfold.md` |
| 073 | **Hylomorphisms and Fusion** | `073-hylomorphisms-and-fusion.md` |
| 074 | **Paramorphisms and Access to Original Structure** | `074-paramorphisms-and-access-to-original-structure.md` |
| 075 | **Zygomorphisms and Multiple Results** | `075-zygomorphisms-and-multiple-results.md` |
| 076 | **Fixed Points of Functors** | `076-fixed-points-of-functors.md` |
| 077 | **Optics: Lenses** | `077-optics-lenses.md` |
| 078 | **Optics: Prisms and Traversals** | `078-optics-prisms-and-traversals.md` |
| 079 | **Compositional Interpreters** | `079-compositional-interpreters.md` |
| 080 | **Choosing Abstractions Without Obscuring the Program** | `080-choosing-abstractions-without-obscuring-the-program.md` |

### Block 09 — Functional Concurrency, Parallelism, and Streaming

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Immutable Data and Deterministic Parallelism** | `081-immutable-data-and-deterministic-parallelism.md` |
| 082 | **Parallel Evaluation Strategies** | `082-parallel-evaluation-strategies.md` |
| 083 | **Futures and Promises in Functional APIs** | `083-futures-and-promises-in-functional-apis.md` |
| 084 | **Actors and Functional Message Handling** | `084-actors-and-functional-message-handling.md` |
| 085 | **Composing Transactions in Functional Programs** | `085-composing-transactions-in-functional-programs.md` |
| 086 | **Functional Reactive Programming** | `086-functional-reactive-programming.md` |
| 087 | **Pull-Based Streams** | `087-pull-based-streams.md` |
| 088 | **Push-Based Streams and Backpressure** | `088-push-based-streams-and-backpressure.md` |
| 089 | **Resource-Safe Streaming** | `089-resource-safe-streaming.md` |
| 090 | **Reasoning About Cancellation and Failure in Functional Concurrency** | `090-reasoning-about-cancellation-and-failure-in-functional-concurrency.md` |

### Block 10 — Production Functional Engineering

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Module Systems and Functional Component Boundaries** | `091-module-systems-and-functional-component-boundaries.md` |
| 092 | **Functional Domain Modeling at Scale** | `092-functional-domain-modeling-at-scale.md` |
| 093 | **Persistent Data Structure Cost Models** | `093-persistent-data-structure-cost-models.md` |
| 094 | **Strictness Analysis and Space Leaks** | `094-strictness-analysis-and-space-leaks.md` |
| 095 | **Allocation, Boxing, and Runtime Representation** | `095-allocation-boxing-and-runtime-representation.md` |
| 096 | **Fusion and Intermediate-Structure Elimination** | `096-fusion-and-intermediate-structure-elimination.md` |
| 097 | **Interoperability with Object-Oriented and Systems Code** | `097-interoperability-with-object-oriented-and-systems-code.md` |
| 098 | **Testing Effectful Functional Programs** | `098-testing-effectful-functional-programs.md` |
| 099 | **Refactoring Toward Functional Clarity** | `099-refactoring-toward-functional-clarity.md` |
| 100 | **Reviewing a Production Functional System for Semantics, Cost, and Change** | `100-reviewing-a-production-functional-system-for-semantics-cost-and-change.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
