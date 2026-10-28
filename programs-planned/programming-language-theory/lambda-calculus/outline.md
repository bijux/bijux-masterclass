# λ-Calculus Theory

## Module 1 – Syntax, Binding, Substitution

* **M1.1** – Abstract syntax of λ-terms (variables, application, abstraction, grammar).
* **M1.2** – Free vs bound variables, scope, capture.
* **M1.3** – α-conversion and α-equivalence classes.
* **M1.4** – Capture-avoiding substitution (formal definition, failure of naïve substitution).
* **M1.5** – Structural induction and recursion on terms (basic lemmas about syntax).

---

## Module 2 – Binding Representations and Mechanization

* **M2.1** – Named vs nameless syntax and α-classes.
* **M2.2** – De Bruijn indices: nameless λ-terms and shifting/substitution.
* **M2.3** – Locally nameless representation: `open`/`close`, free vs bound vars.
* **M2.4** – Substitution and renaming lemmas: α-respect, preservation of free vars.
* **M2.5** – Mechanizing λ-calculus in Coq/Agda/Lean (encoding binders and substitution).

---

## Module 3 – Reduction, Equivalence, Normal Forms

* **M3.1** – β-reduction (one-step, multi-step, β-equivalence).
* **M3.2** – η-conversion and βη-equivalence.
* **M3.3** – Normal forms, weak/head/strong normalization, non-termination (Ω, etc.).
* **M3.4** – Confluence / Church–Rosser theorem (statement, proof strategy).
* **M3.5** – Standardization theorem and its computational consequences.

---

## Module 4 – Böhm Trees, Solvability, and Separation

* **M4.1** – Solvable vs unsolvable terms; head normal forms and head reduction.
* **M4.2** – Böhm trees: infinitary normal forms, construction and basic properties.
* **M4.3** – Lévy–Longo trees and alternative infinitary representations.
* **M4.4** – Böhm-out and separation theorems: distinguishing non-equivalent terms.
* **M4.5** – Connections to models and observational equivalence (H*, λβη, full abstraction).

---

## Module 5 – The λ-Calculus as a Programming Language

* **M5.1** – Church encodings of booleans, conditionals, pairs, products.
* **M5.2** – Church numerals and arithmetic (succ, plus, mult, pred).
* **M5.3** – Fixed-point combinators (Y, Θ): definitions and properties.
* **M5.4** – Defining recursive functions (factorial, map, fold, etc.) via fixed points.
* **M5.5** – Relationship to combinatory logic (S, K, I; λ→SKI translation).

---

## Module 6 – Operational Semantics and Abstract Machines

* **M6.1** – Small-step semantics (→) for λ-calculus under a chosen strategy.
* **M6.2** – Big-step semantics (⇓) and its equivalence/limitations vs small-step.
* **M6.3** – Evaluation strategies: call-by-name, call-by-value, call-by-need; weak vs strong.
* **M6.4** – Evaluation contexts, determinism, and stuck states.
* **M6.5** – Abstract machines (e.g. Krivine/CEK): environments, closures, stacks.

---

## Module 7 – Explicit Substitution Calculi ($\lambda\sigma$)

* **M7.1** – Motivation: substitution as a first-class operation and implementation concerns.
* **M7.2** – Syntax of explicit substitution calculi (e.g. λσ): terms and substitution constructs.
* **M7.3** – Reduction rules for explicit substitutions and interaction with β-reduction.
* **M7.4** – Properties: confluence, normalization issues, comparison with standard λ-calculus.
* **M7.5** – Explicit substitutions in interpreters, abstract machines, and mechanized proofs.

---

## Module 8 – Simply Typed λ-Calculus (STLC): Core System

* **M8.1** – Types and typing judgements Γ ⊢ t : A (syntax of types).
* **M8.2** – Function types, contexts, structural rules (weakening, exchange).
* **M8.3** – Typing rules for variables, abstraction, application.
* **M8.4** – Type derivations as trees; substitution lemma for typed terms.
* **M8.5** – Algorithmic type checking for STLC and uniqueness of types.

---

## Module 9 – STLC Metatheory and Data Types

* **M9.1** – Canonical forms lemma (shape of values given a type).
* **M9.2** – Progress theorem (well-typed terms don’t get stuck).
* **M9.3** – Preservation theorem (types are invariant under evaluation).
* **M9.4** – Strong normalization of STLC (logical relations / reducibility candidates – schema and variants).
* **M9.5** – Products, sums, unit, empty types and their Curry–Howard interpretation.

---

## Module 10 – PCF and Observational Equivalence

* **M10.1** – PCF syntax and types: Nat, Bool, function types, fixpoint operator.
* **M10.2** – Operational semantics for PCF and contextual closure.
* **M10.3** – Contextual and observational equivalence of programs.
* **M10.4** – A simple denotational model of PCF and adequacy (termination vs ⊥).
* **M10.5** – Full abstraction for PCF (problem statement) and the road to game semantics.

---

## Module 11 – Recursive Types and General Recursion

* **M11.1** – Iso-recursive types: μ-types with roll/unroll, examples (lists, trees).
* **M11.2** – Equi-recursive types and type equality; cycles in type graphs.
* **M11.3** – Operational semantics and typing rules for μ-types and recursive data.
* **M11.4** – Metatheory: type safety, loss of strong normalization, domain-theoretic reading.
* **M11.5** – Recursive types in real languages and typed IRs (algebraic datatypes, folds/unfolds).

---

## Module 12 – System F and Parametric Polymorphism

* **M12.1** – Syntax of System F: type variables, type abstraction Λα.t, type application t [A].
* **M12.2** – Typing rules for ∀-types and polymorphic terms.
* **M12.3** – Church encodings in System F (lists, trees, etc. with better types).
* **M12.4** – Expressiveness vs undecidable type inference in System F.
* **M12.5** – Parametricity and “free theorems” (logical relations for polymorphic types).

---

## Module 13 – Hindley–Milner and Type Inference

* **M13.1** – Let-polymorphism and type schemes (∀-quantification at let-bound definitions).
* **M13.2** – Constraint generation and unification for simple types.
* **M13.3** – Algorithm W: specification, examples, and implementation details.
* **M13.4** – Soundness, completeness, and principal typings in HM.
* **M13.5** – HM in practice and its relationship to rank-1 System F (ML/Haskell cores).

---

## Module 14 – Beyond System F: Higher Types and Dependency

* **M14.1** – Higher-kinded types and System Fω (types of type constructors).
* **M14.2** – Subtyping in λ-calculus, variance issues, basic subtype systems.
* **M14.3** – Intersection and union types; connections to normalization and completeness.
* **M14.4** – Introduction to dependent types (λΠ-calculus, types depending on terms).
* **M14.5** – Core calculi of Coq/Agda/Lean and their λ-calculus foundations (survey-level).

---

## Module 15 – Denotational and Categorical Semantics

* **M15.1** – Domain theory basics: posets, CPOs, directed suprema.
* **M15.2** – Scott-continuous functions and least fixpoints (Knaster–Tarski, etc.).
* **M15.3** – Domain models for (untyped) λ-calculus: solving D ≅ [D → D].
* **M15.4** – Cartesian closed categories (CCC) as models of STLC.
* **M15.5** – Soundness, adequacy, and observational equivalence (semantic vs operational).

---

## Module 16 – Control, Effects, and Real Languages

* **M16.1** – Control operators: call/cc, continuations, and their λ encodings.
* **M16.2** – CPS translations (call-by-value, call-by-name) and correctness ideas.
* **M16.3** – λμ-calculus and the link to classical versus intuitionistic logic.
* **M16.4** – Monads and algebraic effects in λ-calculus (state, exceptions, IO).
* **M16.5** – λ-calculus as the core of real languages and tools (ML/Haskell/Scheme cores, compiler IRs, proof assistant kernels).

---

## Module 17 – Linear Types and Resource-Aware Extensions

* **M17.1** – Syntax of linear λ-calculus: linear arrows, multiplicity annotations.
* **M17.2** – Typing rules for linearity: no weakening/contraction for linear variables.
* **M17.3** – Semantics and properties: affine vs strict linear, connections to quantum λ.
* **M17.4** – Encodings and applications: linear data structures, session types, resources.
* **M17.5** – Metatheory: type safety, normalization, and links to linear logic via Curry–Howard.

---

## Module 18 – Game Semantics and Advanced Models

* **M18.1** – Basics of games: arenas, moves, plays as sequences.
* **M18.2** – Strategies as term denotations: innocent vs general strategies.
* **M18.3** – Modeling untyped λ: fixed points and recursion in game models.
* **M18.4** – Typed game models for STLC/System F and categorical connections.
* **M18.5** – Full abstraction and applications: PCF, effects, and higher-order features.

---

## Module 19 – Historical and Philosophical Perspectives

* **M19.1** – Origins: Church’s λ-calculus, Turing machines, and equivalence.
* **M19.2** – Philosophical foundations: computability, effective calculability, Church–Turing thesis.
* **M19.3** – Influence on languages and tools (Lisp, ML, Haskell, proof assistants).
* **M19.4** – Open problems and directions: quantum computation, concurrency, higher categories.
* **M19.5** – Ethical and philosophical implications: formal verification and trust in software.

---

## Module 20 – Quantum and Concurrent Extensions

* **M20.1** – Syntax for quantum λ-calculus: qubits, linear structure, superposition operations.
* **M20.2** – Typing for quantum λ-calculus: linearity, no-cloning, measurement.
* **M20.3** – Concurrent λ-calculus: processes, channels, links to π-calculus.
* **M20.4** – Semantics: quantum domains/linear-algebraic models; process algebras and bisimulation.
* **M20.5** – Applications: quantum algorithms, distributed computation, and protocols.
