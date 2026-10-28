# 01. Programming Languages & Semantics

**Program code:** `PLS`

**Purpose:** Build a language-independent model of how programs are represented, typed, evaluated, composed, and given precise meaning.

**Level-II professional outcome:** Ready to reason across language families, review language designs, explain runtime and type-system trade-offs, and enter advanced language implementation or formal-semantics work.

**Prerequisites:** discrete mathematics; proficiency in at least two contrasting languages; basic data structures and algorithms.

**Primary ownership:** syntax and binding; dynamic and static semantics; type systems; evaluation strategies; state and effects; module systems; runtime semantics; comparative language design.

**Explicit exclusions:** deep object-oriented practice (Program 02); deep functional practice (Program 03); concurrent/parallel programming practice (Program 04); compiler construction (Program 08); computability and complexity (Program 15).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Language Structure and Meaning

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Programs, Languages, and Observable Behavior** | `001-programs-languages-and-observable-behavior.md` |
| 002 | **Lexical Structure, Tokens, and Concrete Syntax** | `002-lexical-structure-tokens-and-concrete-syntax.md` |
| 003 | **Grammars, Parse Trees, and Abstract Syntax** | `003-grammars-parse-trees-and-abstract-syntax.md` |
| 004 | **Names, Bindings, and Environments** | `004-names-bindings-and-environments.md` |
| 005 | **Lexical Scope, Dynamic Scope, and Shadowing** | `005-lexical-scope-dynamic-scope-and-shadowing.md` |
| 006 | **Values, Identity, Equality, and Representation** | `006-values-identity-equality-and-representation.md` |
| 007 | **Expressions, Statements, and Evaluation Contexts** | `007-expressions-statements-and-evaluation-contexts.md` |
| 008 | **Static Semantics and Dynamic Semantics** | `008-static-semantics-and-dynamic-semantics.md` |
| 009 | **Determinism, Nondeterminism, and Program Outcomes** | `009-determinism-nondeterminism-and-program-outcomes.md` |
| 010 | **Comparing Language Designs Through Semantic Questions** | `010-comparing-language-designs-through-semantic-questions.md` |

### Block 02 — Types and Static Guarantees

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Type Judgments and Typing Rules** | `011-type-judgments-and-typing-rules.md` |
| 012 | **Primitive, Product, Sum, and Recursive Types** | `012-primitive-product-sum-and-recursive-types.md` |
| 013 | **Function Types and First-Class Procedures** | `013-function-types-and-first-class-procedures.md` |
| 014 | **Parametric Polymorphism and Generic Abstraction** | `014-parametric-polymorphism-and-generic-abstraction.md` |
| 015 | **Nominal and Structural Type Equivalence** | `015-nominal-and-structural-type-equivalence.md` |
| 016 | **Subtyping, Subsumption, and Behavioral Compatibility** | `016-subtyping-subsumption-and-behavioral-compatibility.md` |
| 017 | **Covariance, Contravariance, and Invariance** | `017-covariance-contravariance-and-invariance.md` |
| 018 | **Constraint-Based Type Inference** | `018-constraint-based-type-inference.md` |
| 019 | **Algebraic Data Types and Exhaustive Matching** | `019-algebraic-data-types-and-exhaustive-matching.md` |
| 020 | **Type Safety, Progress, and Preservation Intuition** | `020-type-safety-progress-and-preservation-intuition.md` |

### Block 03 — Evaluation, Functions, and Control

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Substitution-Based Evaluation** | `021-substitution-based-evaluation.md` |
| 022 | **Environment-Based Evaluation** | `022-environment-based-evaluation.md` |
| 023 | **Call by Value, Name, Need, and Sharing** | `023-call-by-value-name-need-and-sharing.md` |
| 024 | **Closures and Captured Environments** | `024-closures-and-captured-environments.md` |
| 025 | **Recursion, Fixed Points, and Tail Calls** | `025-recursion-fixed-points-and-tail-calls.md` |
| 026 | **Evaluation Order and Side-Effect Visibility** | `026-evaluation-order-and-side-effect-visibility.md` |
| 027 | **Exceptions and Nonlocal Control Transfer** | `027-exceptions-and-nonlocal-control-transfer.md` |
| 028 | **Generators, Coroutines, and Suspension** | `028-generators-coroutines-and-suspension.md` |
| 029 | **Continuations and Continuation-Passing Style** | `029-continuations-and-continuation-passing-style.md` |
| 030 | **Explicit State Machines as a Control Model** | `030-explicit-state-machines-as-a-control-model.md` |

### Block 04 — State, Memory, and Resource Semantics

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Variables, Locations, Stores, and Mutation** | `031-variables-locations-stores-and-mutation.md` |
| 032 | **Aliasing and Interference** | `032-aliasing-and-interference.md` |
| 033 | **Value Semantics, Reference Semantics, and Copying** | `033-value-semantics-reference-semantics-and-copying.md` |
| 034 | **Stack Discipline, Heap Objects, and Lifetimes** | `034-stack-discipline-heap-objects-and-lifetimes.md` |
| 035 | **Manual Allocation and Deallocation** | `035-manual-allocation-and-deallocation.md` |
| 036 | **Tracing Garbage Collection** | `036-tracing-garbage-collection.md` |
| 037 | **Reference Counting and Cycle Management** | `037-reference-counting-and-cycle-management.md` |
| 038 | **Ownership, Borrowing, and Move Semantics** | `038-ownership-borrowing-and-move-semantics.md` |
| 039 | **Linear, Affine, and Uniqueness Types** | `039-linear-affine-and-uniqueness-types.md` |
| 040 | **Resource Safety Across C, Rust, Java, and Python** | `040-resource-safety-across-c-rust-java-and-python.md` |

### Block 05 — Abstraction, Modules, and Paradigm Boundaries

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Abstract Data Types and Representation Independence** | `041-abstract-data-types-and-representation-independence.md` |
| 042 | **Interfaces, Signatures, and Information Hiding** | `042-interfaces-signatures-and-information-hiding.md` |
| 043 | **Modules, Namespaces, and Separate Compilation** | `043-modules-namespaces-and-separate-compilation.md` |
| 044 | **Generics, Traits, Protocols, and Type Classes** | `044-generics-traits-protocols-and-type-classes.md` |
| 045 | **Encapsulation Without Objects** | `045-encapsulation-without-objects.md` |
| 046 | **Pattern Matching as a Decomposition Mechanism** | `046-pattern-matching-as-a-decomposition-mechanism.md` |
| 047 | **Pure and Effectful Computation** | `047-pure-and-effectful-computation.md` |
| 048 | **Static Linking, Dynamic Linking, and Module Identity** | `048-static-linking-dynamic-linking-and-module-identity.md` |
| 049 | **Cross-Language Interoperability Boundaries** | `049-cross-language-interoperability-boundaries.md` |
| 050 | **Imperative, Object, Functional, Logic, and Dataflow Models** | `050-imperative-object-functional-logic-and-dataflow-models.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Formal Semantic Methods

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Small-Step Operational Semantics** | `051-small-step-operational-semantics.md` |
| 052 | **Big-Step Natural Semantics** | `052-big-step-natural-semantics.md` |
| 053 | **Evaluation Contexts and Reduction Strategies** | `053-evaluation-contexts-and-reduction-strategies.md` |
| 054 | **Denotational Semantics and Compositional Meaning** | `054-denotational-semantics-and-compositional-meaning.md` |
| 055 | **Axiomatic Semantics and Hoare-Style Reasoning** | `055-axiomatic-semantics-and-hoare-style-reasoning.md` |
| 056 | **Contextual Equivalence and Observational Equivalence** | `056-contextual-equivalence-and-observational-equivalence.md` |
| 057 | **Bisimulation and Coinductive Reasoning** | `057-bisimulation-and-coinductive-reasoning.md` |
| 058 | **Normalization, Confluence, and Church-Rosser Reasoning** | `058-normalization-confluence-and-church-rosser-reasoning.md` |
| 059 | **Mechanizing Semantics in a Proof Assistant** | `059-mechanizing-semantics-in-a-proof-assistant.md` |
| 060 | **Testing an Interpreter Against a Formal Semantics** | `060-testing-an-interpreter-against-a-formal-semantics.md` |

### Block 07 — Advanced Type Systems

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **System F and Explicit Polymorphism** | `061-system-f-and-explicit-polymorphism.md` |
| 062 | **Existential Types and Abstract Representation** | `062-existential-types-and-abstract-representation.md` |
| 063 | **Higher-Kinded Types and Type Constructors** | `063-higher-kinded-types-and-type-constructors.md` |
| 064 | **GADTs and Type Refinement by Pattern Matching** | `064-gadts-and-type-refinement-by-pattern-matching.md` |
| 065 | **Type Classes, Coherence, and Dictionary Passing** | `065-type-classes-coherence-and-dictionary-passing.md` |
| 066 | **Row Polymorphism and Extensible Records** | `066-row-polymorphism-and-extensible-records.md` |
| 067 | **Refinement Types and Predicate-Constrained Values** | `067-refinement-types-and-predicate-constrained-values.md` |
| 068 | **Dependent Types and Propositions as Types** | `068-dependent-types-and-propositions-as-types.md` |
| 069 | **Gradual Typing and Blame** | `069-gradual-typing-and-blame.md` |
| 070 | **Effect Types, Capability Types, and Ownership Types** | `070-effect-types-capability-types-and-ownership-types.md` |

### Block 08 — Effects, Concurrency, and Interaction Semantics

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Monads as a Semantic Structuring Device** | `071-monads-as-a-semantic-structuring-device.md` |
| 072 | **Algebraic Effects and Effect Handlers** | `072-algebraic-effects-and-effect-handlers.md` |
| 073 | **Delimited Continuations and Control Effects** | `073-delimited-continuations-and-control-effects.md` |
| 074 | **Asynchronous Functions and Promise Semantics** | `074-asynchronous-functions-and-promise-semantics.md` |
| 075 | **Cancellation and Structured Concurrency Semantics** | `075-cancellation-and-structured-concurrency-semantics.md` |
| 076 | **Language-Level Memory Models and Happens-Before** | `076-language-level-memory-models-and-happens-before.md` |
| 077 | **Actor Semantics and Mailbox Ordering** | `077-actor-semantics-and-mailbox-ordering.md` |
| 078 | **Transactional Memory Semantics** | `078-transactional-memory-semantics.md` |
| 079 | **Session Types and Protocol-Typed Communication** | `079-session-types-and-protocol-typed-communication.md` |
| 080 | **Semantics of Remote Calls and Partial Failure** | `080-semantics-of-remote-calls-and-partial-failure.md` |

### Block 09 — Runtime Semantics and Representation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Runtime Object Layout and Tagged Values** | `081-runtime-object-layout-and-tagged-values.md` |
| 082 | **Closure Conversion and Environment Representation** | `082-closure-conversion-and-environment-representation.md` |
| 083 | **Dynamic Dispatch, Vtables, and Inline Caches** | `083-dynamic-dispatch-vtables-and-inline-caches.md` |
| 084 | **Exception Tables, Stack Unwinding, and Cleanup** | `084-exception-tables-stack-unwinding-and-cleanup.md` |
| 085 | **Garbage-Collector Semantics and Write Barriers** | `085-garbage-collector-semantics-and-write-barriers.md` |
| 086 | **Foreign-Function Interfaces and Representation Contracts** | `086-foreign-function-interfaces-and-representation-contracts.md` |
| 087 | **Reflection, Dynamic Loading, and Runtime Type Information** | `087-reflection-dynamic-loading-and-runtime-type-information.md` |
| 088 | **Module Initialization and Global State Ordering** | `088-module-initialization-and-global-state-ordering.md` |
| 089 | **JIT Compilation and Speculative Semantics** | `089-jit-compilation-and-speculative-semantics.md` |
| 090 | **Sandboxing, Capabilities, and Runtime Isolation** | `090-sandboxing-capabilities-and-runtime-isolation.md` |

### Block 10 — Language Design, Evolution, and Evaluation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Deriving a Language from Domain Requirements** | `091-deriving-a-language-from-domain-requirements.md` |
| 092 | **Choosing Evaluation, Mutation, and Error Models** | `092-choosing-evaluation-mutation-and-error-models.md` |
| 093 | **Designing Nullability and Partiality** | `093-designing-nullability-and-partiality.md` |
| 094 | **Designing Generic Abstraction and Ad Hoc Polymorphism** | `094-designing-generic-abstraction-and-ad-hoc-polymorphism.md` |
| 095 | **Designing Compatibility and Versioning Rules** | `095-designing-compatibility-and-versioning-rules.md` |
| 096 | **Balancing Safety, Predictability, and Control** | `096-balancing-safety-predictability-and-control.md` |
| 097 | **Language Evolution and Feature Interaction** | `097-language-evolution-and-feature-interaction.md` |
| 098 | **Domain-Specific Languages and Semantic Narrowing** | `098-domain-specific-languages-and-semantic-narrowing.md` |
| 099 | **Comparative Case Studies in Modern Language Design** | `099-comparative-case-studies-in-modern-language-design.md` |
| 100 | **Conducting a Language Design and Semantics Review** | `100-conducting-a-language-design-and-semantics-review.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
