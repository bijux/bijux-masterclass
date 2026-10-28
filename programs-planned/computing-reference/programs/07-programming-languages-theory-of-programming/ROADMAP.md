# 07. Programming Languages: Theory of Programming

**Program code:** `TPROG`

**Purpose:** Build the mathematical foundations for specifying, proving, analyzing, and deriving programs, connecting logic, type theory, semantics, and static analysis.

**Level-II professional outcome:** Ready to read graduate programming-languages research, write formal specifications and proofs, use proof assistants and model checkers, and reason rigorously about program correctness.

**Prerequisites:** discrete mathematics and logic; Programming Languages & Semantics Levels I-II or equivalent; algorithms.

**Primary ownership:** logic for programs; lambda calculi; type theory; program logics; refinement; separation logic; abstract interpretation; program analysis; model checking; proof assistants.

**Explicit exclusions:** language feature survey (Program 01); compiler engineering (Program 08); computability and complexity of problems (Program 15); testing practice (Program 13).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Logic, Relations, and Proofs About Programs

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Propositions, Predicates, and Formal Specifications** | `001-propositions-predicates-and-formal-specifications.md` |
| 002 | **Natural Deduction** | `002-natural-deduction.md` |
| 003 | **Induction and Structural Induction** | `003-induction-and-structural-induction.md` |
| 004 | **Relations, Closures, and Invariants** | `004-relations-closures-and-invariants.md` |
| 005 | **Partial and Total Correctness** | `005-partial-and-total-correctness.md` |
| 006 | **Preconditions, Postconditions, and Assertions** | `006-preconditions-postconditions-and-assertions.md` |
| 007 | **Loop Invariants as Proof Obligations** | `007-loop-invariants-as-proof-obligations.md` |
| 008 | **Termination Measures** | `008-termination-measures.md` |
| 009 | **Proof by Simulation** | `009-proof-by-simulation.md` |
| 010 | **Writing a Machine-Checkable Program Specification** | `010-writing-a-machine-checkable-program-specification.md` |

### Block 02 — Lambda Calculi and Core Languages

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Untyped Lambda Calculus** | `011-untyped-lambda-calculus.md` |
| 012 | **Binding, Alpha Conversion, and Substitution** | `012-binding-alpha-conversion-and-substitution.md` |
| 013 | **Beta and Eta Equivalence** | `013-beta-and-eta-equivalence.md` |
| 014 | **Confluence and Normalization** | `014-confluence-and-normalization.md` |
| 015 | **Simply Typed Lambda Calculus** | `015-simply-typed-lambda-calculus.md` |
| 016 | **Products, Sums, and Recursive Types** | `016-products-sums-and-recursive-types.md` |
| 017 | **Polymorphic Lambda Calculus** | `017-polymorphic-lambda-calculus.md` |
| 018 | **Subtyping Calculi** | `018-subtyping-calculi.md` |
| 019 | **Operational Correspondence** | `019-operational-correspondence.md` |
| 020 | **Encoding a Core Programming Language in a Calculus** | `020-encoding-a-core-programming-language-in-a-calculus.md` |

### Block 03 — Type Theory and Curry-Howard

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Types as Propositions and Programs as Proofs** | `021-types-as-propositions-and-programs-as-proofs.md` |
| 022 | **Intuitionistic Propositional Logic** | `022-intuitionistic-propositional-logic.md` |
| 023 | **Dependent Function and Pair Types** | `023-dependent-function-and-pair-types.md` |
| 024 | **Inductive Types and Eliminators** | `024-inductive-types-and-eliminators.md` |
| 025 | **Universes and Type Formation** | `025-universes-and-type-formation.md` |
| 026 | **Equality Types** | `026-equality-types.md` |
| 027 | **Refinement Types** | `027-refinement-types.md` |
| 028 | **Linear and Affine Logic** | `028-linear-and-affine-logic.md` |
| 029 | **Effect and Capability Typing** | `029-effect-and-capability-typing.md` |
| 030 | **Proving Small Theorems by Constructing Programs** | `030-proving-small-theorems-by-constructing-programs.md` |

### Block 04 — Program Logics

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Hoare Triples and the Consequence Rule** | `031-hoare-triples-and-the-consequence-rule.md` |
| 032 | **Assignment, Sequence, and Conditional Rules** | `032-assignment-sequence-and-conditional-rules.md` |
| 033 | **While Rules and Invariant Discovery** | `033-while-rules-and-invariant-discovery.md` |
| 034 | **Procedure Calls and Modular Verification** | `034-procedure-calls-and-modular-verification.md` |
| 035 | **Weakest Preconditions** | `035-weakest-preconditions.md` |
| 036 | **Strongest Postconditions** | `036-strongest-postconditions.md` |
| 037 | **Recursive Procedures** | `037-recursive-procedures.md` |
| 038 | **Exceptions and Abrupt Control** | `038-exceptions-and-abrupt-control.md` |
| 039 | **Nondeterministic Programs** | `039-nondeterministic-programs.md` |
| 040 | **Verifying a Stateful Algorithm with Hoare Logic** | `040-verifying-a-stateful-algorithm-with-hoare-logic.md` |

### Block 05 — State, Aliasing, and Separation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Heap Models and Assertions About Memory** | `041-heap-models-and-assertions-about-memory.md` |
| 042 | **Aliasing as a Proof Problem** | `042-aliasing-as-a-proof-problem.md` |
| 043 | **Separating Conjunction** | `043-separating-conjunction.md` |
| 044 | **The Frame Rule** | `044-the-frame-rule.md` |
| 045 | **Linked-Structure Proofs** | `045-linked-structure-proofs.md` |
| 046 | **Ownership and Permission Logics** | `046-ownership-and-permission-logics.md` |
| 047 | **Concurrent Separation Logic** | `047-concurrent-separation-logic.md` |
| 048 | **Resource Invariants** | `048-resource-invariants.md` |
| 049 | **Memory Safety Proofs** | `049-memory-safety-proofs.md` |
| 050 | **Verifying an In-Place Data Structure** | `050-verifying-an-in-place-data-structure.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Denotational and Domain-Theoretic Foundations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Compositional Denotations** | `051-compositional-denotations.md` |
| 052 | **Complete Partial Orders** | `052-complete-partial-orders.md` |
| 053 | **Continuous Functions** | `053-continuous-functions.md` |
| 054 | **Least Fixed Points** | `054-least-fixed-points.md` |
| 055 | **Domains for Recursive Types** | `055-domains-for-recursive-types.md` |
| 056 | **Powerdomains for Nondeterminism** | `056-powerdomains-for-nondeterminism.md` |
| 057 | **State and Continuation Semantics** | `057-state-and-continuation-semantics.md` |
| 058 | **Logical Relations** | `058-logical-relations.md` |
| 059 | **Full Abstraction** | `059-full-abstraction.md` |
| 060 | **Relating Denotational and Operational Semantics** | `060-relating-denotational-and-operational-semantics.md` |

### Block 07 — Refinement and Program Derivation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Refinement Orders** | `061-refinement-orders.md` |
| 062 | **Specification Statements** | `062-specification-statements.md` |
| 063 | **Data Refinement** | `063-data-refinement.md` |
| 064 | **Simulation Relations** | `064-simulation-relations.md` |
| 065 | **Refinement Calculus** | `065-refinement-calculus.md` |
| 066 | **Deriving Loops from Specifications** | `066-deriving-loops-from-specifications.md` |
| 067 | **Refining Nondeterminism** | `067-refining-nondeterminism.md` |
| 068 | **Correct-by-Construction Components** | `068-correct-by-construction-components.md` |
| 069 | **Refinement Types in Practice** | `069-refinement-types-in-practice.md` |
| 070 | **Deriving an Executable Program from a Relational Specification** | `070-deriving-an-executable-program-from-a-relational-specification.md` |

### Block 08 — Abstract Interpretation and Static Analysis

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Concrete and Abstract Semantics** | `071-concrete-and-abstract-semantics.md` |
| 072 | **Galois Connections** | `072-galois-connections.md` |
| 073 | **Sound Abstraction** | `073-sound-abstraction.md` |
| 074 | **Fixed-Point Computation** | `074-fixed-point-computation.md` |
| 075 | **Widening and Narrowing** | `075-widening-and-narrowing.md` |
| 076 | **Interval and Congruence Domains** | `076-interval-and-congruence-domains.md` |
| 077 | **Dataflow Analysis as Abstract Interpretation** | `077-dataflow-analysis-as-abstract-interpretation.md` |
| 078 | **Pointer and Alias Analysis** | `078-pointer-and-alias-analysis.md` |
| 079 | **Relational Abstract Domains** | `079-relational-abstract-domains.md` |
| 080 | **Designing a Sound Static Analyzer** | `080-designing-a-sound-static-analyzer.md` |

### Block 09 — Temporal Reasoning and Model Checking

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Transition Systems and Traces** | `081-transition-systems-and-traces.md` |
| 082 | **Safety and Liveness Properties** | `082-safety-and-liveness-properties.md` |
| 083 | **Linear Temporal Logic** | `083-linear-temporal-logic.md` |
| 084 | **Computation Tree Logic** | `084-computation-tree-logic.md` |
| 085 | **Explicit-State Model Checking** | `085-explicit-state-model-checking.md` |
| 086 | **Symbolic Model Checking** | `086-symbolic-model-checking.md` |
| 087 | **Partial-Order Reduction** | `087-partial-order-reduction.md` |
| 088 | **Bounded Model Checking** | `088-bounded-model-checking.md` |
| 089 | **Counterexample-Guided Refinement** | `089-counterexample-guided-refinement.md` |
| 090 | **Model Checking a Concurrent Protocol** | `090-model-checking-a-concurrent-protocol.md` |

### Block 10 — Mechanized Metatheory and Proof Engineering

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Proof Assistant Kernels and Trusted Bases** | `091-proof-assistant-kernels-and-trusted-bases.md` |
| 092 | **Inductive Definitions in Lean, Coq, or Isabelle** | `092-inductive-definitions-in-lean-coq-or-isabelle.md` |
| 093 | **Mechanizing Operational Semantics** | `093-mechanizing-operational-semantics.md` |
| 094 | **Mechanizing Type Soundness** | `094-mechanizing-type-soundness.md` |
| 095 | **Automation, Tactics, and Decision Procedures** | `095-automation-tactics-and-decision-procedures.md` |
| 096 | **Proof Objects and Proof Maintenance** | `096-proof-objects-and-proof-maintenance.md` |
| 097 | **Verified Extraction and Code Generation** | `097-verified-extraction-and-code-generation.md` |
| 098 | **Certified Data Structures and Algorithms** | `098-certified-data-structures-and-algorithms.md` |
| 099 | **Reading and Reproducing a PL Metatheory Paper** | `099-reading-and-reproducing-a-pl-metatheory-paper.md` |
| 100 | **Auditing a Formal Development for Assumptions and Gaps** | `100-auditing-a-formal-development-for-assumptions-and-gaps.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
