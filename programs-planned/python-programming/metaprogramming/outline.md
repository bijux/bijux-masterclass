# Theory of Metaprogramming

### Module 01 – Conceptual Foundations

* M01C01 – What Is Metaprogramming? Object vs Meta Language, Meta-Levels
* M01C02 – Code as Data: Syntax, ASTs, IRs, Semantics
* M01C03 – Taxonomy of Metaprogramming Techniques
* M01C04 – Expressiveness vs Safety vs Complexity
* M01C05 – When Metaprogramming Is Justified
### Module 02 – Representation, Binding & Rewriting

* M02C06 – Concrete vs Abstract Syntax Trees (CST vs AST)
* M02C07 – Binding, α-Conversion, Scope & Environments
* M02C08 – Intermediate Representations & Lowering
* M02C09 – Term Rewriting & Program Transformations
* M02C10 – Semantic Preservation & Correctness of Transforms
### Module 03 – Macro Systems & Hygienic Metaprogramming

* M03C11 – Textual vs Syntactic Macros
* M03C12 – Hygienic Macros & Name Capture
* M03C13 – Quasiquotation & Pattern Languages (Keystone #1)
* M03C14 – Expansion Phases & Macro Phase Ordering
* M03C15 – Macro Debuggability & Tooling
### Module 04 – Generics, Overloading & Parametricity

* M04C16 – Parametric Polymorphism as Controlled Metaprogramming
* M04C17 – Ad-Hoc Polymorphism & Overload Resolution
* M04C18 – Traits, Concepts & Typeclasses as Meta-Interfaces
* M04C19 – Monomorphization vs Shared Generics
* M04C20 – Type Inference, Constraints & Meta-Search

---

...

## Module 05 – Type-Level Programming & Static Invariants

* **M05C21 – Kinds & Type-Level Values**
  Kinds as “types of types”. Value-level vs type-level vs kind-level. Promoted values and higher-kinded types.

* **M05C22 – Type Functions, Families & Associated Types**
  Type-level functions. Open vs closed families, associated types in traits/typeclasses. Definitional vs propositional equality at the type level.

* **M05C23 – Type-Level Data & Inductive Encodings**
  Type-level naturals, lists, and other inductive encodings. Types expressing length, shape, or dimension constraints (e.g., length-indexed vectors).

* **M05C24 – Typestates, Phantom Types & Protocol Encoding**
  Protocol states and permissions encoded in types: builder patterns, session types, units/regions/effects tracked via phantom types.

* **M05C25 – Limits: Undecidability, Termination & Complexity**
  When type-level computation reaches Turing-completeness. Undecidable type checking, exponential blowups, syntactic termination checks and restrictions.
## Module 06 – Staging, Partial Evaluation & Compile-Time Execution

* **M06C26 – Staging & Multi-Stage Programming**
  Explicit staging annotations (quote/splice). Distinguish object-level from meta-level. Stage correctness as a core invariant.

* **M06C27 – Cross-Stage Safety & Stage Polymorphism (Keystone #2)**
  Which values may flow across stages, and under what rules. Stage polymorphism and its dangers. Preventing use-before-definition across stage boundaries.

* **M06C28 – Partial Evaluation & Specialization**
  Evaluate what can be known early. Offline vs online partial evaluation; relation to constant folding, specialization, and devirtualization.

* **M06C29 – Compile-Time Execution Models (Const-Eval)**
  Constexpr / `const fn` / compile-time functions. Purity and determinism constraints; what must be forbidden at compile time.

* **M06C30 – Stage Explosion & Compile-Time Blow-Ups**
  How aggressive staging and specialization explode variant counts and compile times. Heuristics and design rules to keep meta-work bounded.

---
## Module 07 – Reflection, Introspection & Runtime Meta

* **M07C31 – Nominal vs Structural Reflection**
  Runtime access to type metadata. Nominal (name-based) vs structural (shape-based) reflection; degrees of power and corresponding risks.

* **M07C32 – RTTI, Dynamic Dispatch & Shape-Driven Introspection**
  Vtables, sum-type tags, downcasts. How object models and algebraic data types expose runtime structure to meta-code.

* **M07C33 – Dynamic Code Loading, JIT & Plugin Systems**
  Dynamic linking, shared libraries, JIT compilation, plugin architectures. ABI stability, symbol resolution, versioning.

* **M07C34 – Interception, Proxies & Aspect-Like Layers**
  Proxies, interception handlers, aspect-style weaving of cross-cutting concerns (logging, security, monitoring) without source modification.

* **M07C35 – Security & Isolation of Meta Layers**
  Attack surface of reflection/JIT/plugins. Sandboxing untrusted meta-code, capability models, JIT hardening, and policy constraints.

---
## Module 08 – DSLs, Code Generation & Synthesis

* **M08C36 – External vs Embedded DSLs**
  Design trade-offs: standalone languages with custom syntax vs EDSLs embedded using macros, operators, and types.

* **M08C37 – Spec-to-Code Pipelines (IDLs, Schemas, Protocols)**
  IDLs, schema languages and their compilers. Meta enforcing consistency between schemas and generated stubs/bindings/clients.

* **M08C38 – Template-Based vs Structured Code Generation**
  Text templating vs AST/IR-driven generation. Safety, refactorability, and robustness; when string-based generators are acceptable vs dangerous.

* **M08C39 – Constraint-Based & Search-Based Program Synthesis**
  High-level intro to synthesis: deriving programs from tests or logical specs. SMT, enumerative search, and relationships to automated meta-refactoring.

* **M08C40 – Generated Code Ownership & Round-Tripping**
  Principles for treating generated code as read-only artifacts vs editable code; regeneration strategies, diffing, and avoiding “lost manual edits” disasters.

---
## Module 10 – Systemic Reliability, Failure Modes & Global Constraints 

* **M10C46 – The Macro Paradox (Keystone #3)**
  How increasing meta-power can *decrease* overall reliability and maintainability. Case studies of languages and libraries that overreached.

* **M10C47 – Phase-Clean Toolchains (Parse → Expand → Type → Lower → Optimize → Generate)**
  Where metaprogramming hooks should live. Invariants per phase, and why cross-phase leaks create brittle, unmaintainable systems.

* **M10C48 – Diagnostics, Error Locality & Observability**
  Design of error messages and diagnostics in meta-heavy systems. Mapping errors back to *user* code, not just expanded/generated artifacts.

* **M10C49 – Compile-Time Cost Models & Meta-Budgeting**
  Reasoning about compile-time cost, code size, cache pressure, and specialization explosion. How to define and enforce a “meta budget.”

* **M10C50 – Meta Patterns & Anti-Patterns**
  Positive patterns (IR-first transforms, verified DSLs, typed codegen pipelines) vs anti-patterns (stringly-typed generators, opaque macros, hidden global state, cross-phase backdoors).

---
## Module 11 – Meta-Architecture & Structural Design 

* **M11C51 – Principles for Typed Macro Systems**
  Designing macro systems integrated with the type system: typed quasiquotes, type-directed expansion, and avoiding unsound escape hatches.

* **M11C52 – IR-First Meta Layers & Pipelines**
  Structural IR as the primary manipulation medium. Pipelines of passes, each with clear contracts and invariants.

* **M11C53 – Multi-Phase Meta-Pipelines**
  Layered metaprogramming: parse-time macros, type-time reasoning, IR-time rewrites, and link-time specialization. Avoiding phase entanglement.

* **M11C54 – Composable, Tiered Meta Layers**
  Tiered capabilities: declarative macros → typed macros → procedural/extensible stages → reflection. Designing systems where simple use cases do not require maximal power.

* **M11C55 – Meta-Oriented Language & Library Design**
  Methodology for language/compiler teams: requirements elicitation, threat models, performance budgets, and how to shape language features to support safe meta-ecosystems.

---
## Module 12 – Research Directions & Unified Theory

* **M12C56 – Typed Partial Evaluation & Futamura Projections**
  Specialization of interpreters into compilers. Typed partial evaluation, binding-time analysis, and the classical Futamura projections.

* **M12C57 – Metaprogramming for Verified Performance Engineering**
  Meta-driven optimizations: auto-SIMD, tiling, fusion/fission, memory layout specialization. Balancing provable performance vs controllable complexity.

* **M12C58 – Generative IR Systems: e-Graphs & Equality Saturation**
  Equality saturation and e-graphs as meta-optimizers. Rule sets, search spaces, and extracting optimal code.

* **M12C59 – Minimalist & Safe Meta in Constrained Environments**
  Metaprogramming in Zig, WASM, region/linear systems, and safety-first environments. How to design “just enough meta.”

* **M12C60 – Toward a Unified Theory of Metaprogramming**
  Unifying macros, types, staging, reflection, and synthesis under a single perspective: programs as manipulable mathematical objects across multiple strata.
