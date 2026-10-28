# Course 5 — Rust Metaprogramming

## Declarative Macros, Procedural Macros, DSLs, and Build-Time Authority

## The promise

Course 5 treats metaprogramming as language and authority design. It covers declarative grammar, recursive token processing, hygiene, diagnostics, procedural-macro phases, derives, attributes, typed DSLs, and deterministic build generation.

> **Governing question:** Which facts deserve one compile-time source of truth, which generation mechanism is the least powerful adequate choice, and how can expanded code remain diagnosable ordinary Rust?

Course 4 established explicit dataflow and effect boundaries. Course 5 keeps runtime behavior in ordinary Rust and introduces compile-time authority only where one declaration must own a repeated relationship. The new responsibility is to design grammars, expansion, diagnostics, and generated code without creating a second source of truth.

## Before Day 1

You should be able to design traits and public APIs, reason about ordinary Rust expansion targets, write tests at several boundaries, and separate deterministic core logic from effects.

From a blank page, sketch one earlier product or a comparable program. Mark an owner, a valid and invalid state, a failure path, cleanup, and a public promise. Repair any relationship you cannot explain before adding this course’s mechanisms.

## Outcomes

- Separate runtime abstraction from compile-time generation.
- Read a matcher as a grammar rather than as textual substitution.
- Model recursive macro rules as parser states and transitions.
- Distinguish textual scope, path-based scope, and expansion-site lookup for declarative macros.
- Treat invocation grammar and generated Rust as two related public APIs.
- Explain when and how a procedural macro executes.
- Parse `DeriveInput` and distinguish structs, enums, and unions.
- Parse attribute arguments independently from the attached item.
- Design a bounded custom grammar with explicit compatibility space.
- Explain the Cargo build-script lifecycle and communication protocol.
- Integrate all ten mechanisms in CommandForge without creating competing authorities.
- Complete and defend an unseen change using a generation authority and reproducibility record.

## The ten-day line

| Day | Module | Governing question | Capability that must become visible | Laboratory |
|---:|---|---|---|---|
| 1 | [41 — Metaprogramming Boundaries and the Expansion Model](./module-41-metaprogramming-boundaries-and-expansion-model/index.md) | Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs? | **Separate runtime abstraction from compile-time generation.** | [Decision Table Generator](../labs/module-01-decision-table-generator/README.md) |
| 2 | [42 — Declarative Macros: Matchers, Fragments, and Repetition](./module-42-declarative-macros-matchers-fragments-and-repetition/index.md) | How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics? | **Read a matcher as a grammar rather than as textual substitution.** | [Typed Map Macro](../labs/module-02-typed-map-macro/README.md) |
| 3 | [43 — Recursive Macro Parsing and Token-Tree Techniques](./module-43-recursive-macro-parsing-and-token-tree-techniques/index.md) | How can a declarative macro process a nontrivial token language with explicit parser state, guaranteed progress, and bounded complexity? | **Model recursive macro rules as parser states and transitions.** | [State Machine DSL](../labs/module-03-state-machine-dsl/README.md) |
| 4 | [44 — Hygiene, Scope, Paths, and Cross-Crate Macros](./module-44-hygiene-scope-paths-and-cross-crate-macros/index.md) | Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming? | **Distinguish textual scope, path-based scope, and expansion-site lookup for declarative macros.** | [Exported Registry Macro](../labs/module-04-exported-registry-macro/README.md) |
| 5 | [45 — Macro Diagnostics, Testing, and Public API Design](./module-45-macro-diagnostics-testing-and-public-api-design/index.md) | How do you prove that a macro accepts the intended language, rejects misuse for the intended reason, and remains an evolvable public API? | **Treat invocation grammar and generated Rust as two related public APIs.** | [Diagnostic Enum Macro](../labs/module-05-diagnostic-enum-macro/README.md) |
| 6 | [46 — Procedural Macro Execution and TokenStream Engineering](./module-46-procedural-macro-execution-and-tokenstream-engineering/index.md) | What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled? | **Explain when and how a procedural macro executes.** | [TokenStream Inspector](../labs/module-06-token-stream-inspector/README.md) |
| 7 | [47 — Custom Derive Macros and Structural Generation](./module-47-custom-derive-macros-and-structural-generation/index.md) | How do you inspect a Rust item, preserve its generics and constraints, and generate a lawful implementation without pretending to perform type checking? | **Parse `DeriveInput` and distinguish structs, enums, and unions.** | [Field Names Derive](../labs/module-07-field-names-derive/README.md) |
| 8 | [48 — Attribute Macros and Item Transformation](./module-48-attribute-macros-and-item-transformation/index.md) | How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own? | **Parse attribute arguments independently from the attached item.** | [Checked Handler Attribute](../labs/module-08-checked-handler-attribute/README.md) |
| 9 | [49 — Function-Like Procedural Macros and Typed DSLs](./module-49-function-like-procedural-macros-and-typed-dsls/index.md) | How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust? | **Design a bounded custom grammar with explicit compatibility space.** | [Route Table DSL](../labs/module-09-route-table-dsl/README.md) |
| 10 | [50 — Build Scripts, Generated Code, and Compile-Time Architecture](./module-50-build-scripts-generated-code-and-compile-time-architecture/index.md) | How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority? | **Explain the Cargo build-script lifecycle and communication protocol.** | [Generated Code Build](../labs/module-10-generated-code-build/README.md) |

The table is a dependency chain, not a menu. A later module may use an earlier mechanism but may not silently weaken its ownership, failure, ordering, capacity, safety, compatibility, or evidence contract.

## Decision rules

| Decision | Rule used throughout this course |
|---|---|
| Mechanism choice | Prefer ordinary Rust; use the least powerful generation mechanism that owns one real source of truth. |
| Grammar | Define accepted and rejected syntax before writing matcher arms or parser code. |
| Hygiene | Make definition-site and invocation-site names deliberate, especially across crates. |
| Diagnostic | Treat invalid syntax and unsupported structures as part of the public macro contract. |
| Generation | Normalize validated input before emitting deterministic ordinary Rust. |

Use these rules during prediction and review. When a rule does not decide the case, write the missing product requirement instead of selecting an API by habit.

## The reasoning record

The ten module-specific records culminate in a **generation authority and reproducibility record**. Name the phase and source of truth, write the accepted grammar, inspect the expansion, and test causal rejection before adding generation. Keep the record small enough to inspect but complete enough to expose the first unsupported assumption.

## Scope and handoff

The course generates ordinary Rust but does not make macros the default abstraction. It avoids using generation for runtime policy, postpones low-level unsafe implementation, and treats third-party procedural-macro crates as compiler-phase dependencies with explicit version and reproducibility implications.

Course 6 leaves the compiler boundary and crosses external byte, file, process, allocator, ABI, callback, and foreign-resource boundaries.

## Capstone — CommandForge

CommandForge combines a declarative diagnostic catalog, a custom argument derive, a checked handler attribute, a typed command-catalog DSL, and deterministic build-script input while keeping runtime command behavior in ordinary Rust.

Open the [engineering guide](capstone.md) before Day 1 so the final architecture is visible. Implement only the current increment. The independent laboratory remains separate so that the mechanism can be learned without hiding behind accumulated capstone code.

## Completion

The course is complete when you can build and defend:

> Build a small generated command or protocol catalog using at least two distinct macro mechanisms. Every generated fact must have one authority, targeted invalid-input diagnostics, and expansion tests.

and then change the capstone under this constraint:

> Add a new CommandForge field policy and command kind, tracing the change through grammar, semantic validation, expansion, runtime behavior, tests, and compatibility.

A passing test suite is necessary. It is not sufficient unless you can explain why the tests are capable of falsifying the claim and which target-, scheduler-, workload-, peer-, or policy-dependent facts remain outside them.

## Continue

- [Ten-day plan](study-plan.md)
- [Module 41 — Metaprogramming Boundaries and the Expansion Model](./module-41-metaprogramming-boundaries-and-expansion-model/index.md)
- [CommandForge engineering guide](capstone.md)
- [Course reference](reference.md)
- [Final review](final-review.md)
- [Compiler and design investigations](../compiler-labs/README.md)
- [Independent laboratories](../labs/)
