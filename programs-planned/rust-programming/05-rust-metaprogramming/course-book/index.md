# Course 5 — Rust Metaprogramming

## Macros, Derives, Typed DSLs, and Compile-Time Systems

Use generation only where one checked declaration must own several Rust surfaces or validated build data, and keep the expanded program understandable as ordinary Rust.

## Why this course exists

The first forty modules already provide functions, generics, traits, enums, builders, iterators, closures, and data-driven tables. A macro is justified only when those mechanisms cannot keep mechanically related surfaces under one authority. This course therefore begins with mechanism refusal. It then treats each macro as a language plus an expansion contract: accepted syntax, rejected syntax, generated names and paths, ordinary Rust semantics after expansion, failure phase, determinism, and compatibility.

## Before you begin

Course 4, including strong ordinary-Rust design, trait architecture, iterator and error reasoning, effect boundaries, testing, and the ability to reject abstraction that does not pay for itself.

Keep a source-of-truth ledger, accepted grammar, expansion sketch, phase map, and compatibility record beside the code. The record changes shape as the course advances, but its purpose is constant: make the decisive relationship visible before syntax hides it.

## What you will be able to do

- Decide whether a requirement belongs in ordinary Rust, `macro_rules!`, a custom derive, an attribute macro, a function-like procedural macro, or a build script.
- Identify the single source of truth, generated surfaces, deliberately unsupported syntax, and deletion criterion before writing generation code.
- Read `macro_rules!` matchers as grammars and select fragment specifiers according to the public input language rather than convenience.
- Design repetitions whose nesting, separators, ownership, evaluation count, and output position are deliberate and testable.
- Build recursive token-tree parsers with explicit states, accumulators, base cases, progress arguments, and bounded complexity.
- Reason about hygiene, textual and path scope, invocation-site names, definition-crate names, `$crate`, visibility, and dependency renaming.
- Treat successful expansion, rejected syntax, semantic macro errors, generated Rust errors, and downstream compatibility as one public macro contract.
- Construct causal positive and negative tests that fail for the intended phase rather than for incidental invalid Rust.
- Explain procedural-macro execution, token groups, punctuation spacing, literals, spans, deterministic output, and the limits of syntactic knowledge.
- Write a custom derive that classifies supported structures, preserves generics and where clauses, parses helper attributes, combines errors, and avoids invented bounds.
- Write an attribute macro that validates only the contract it owns and preserves unrelated visibility, signature, attributes, and runtime semantics.
- Design a function-like procedural DSL through grammar, syntax AST, semantic validation, normalized model, and deterministic generation.
- Use build scripts with explicit input ownership, `rerun-if-changed`, checked external data, `OUT_DIR`, atomic replacement, and stable generated interfaces.
- Prevent competing authorities among source declarations, generated files, macro metadata, runtime registries, and documentation.
- Review a compile-time system by reconstructing the expanded ordinary Rust program and tracing each failure to the earliest phase that can know it.

## What this course deliberately leaves for later

The course covers stable declarative macros, procedural macros, and build scripts. Compiler plugins, nightly-only expansion APIs, code-generation services, and general compiler construction are outside its scope.

## Ten-day route

1. [Module 41: Metaprogramming Boundaries and the Expansion Model](module-41-metaprogramming-boundaries-and-expansion-model/index.md) — Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs?
2. [Module 42: Declarative Macros: Matchers, Fragments, and Repetition](module-42-declarative-macros-matchers-fragments-and-repetition/index.md) — How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics?
3. [Module 43: Recursive Macro Parsing and Token-Tree Techniques](module-43-recursive-macro-parsing-and-token-tree-techniques/index.md) — How can a declarative macro process a nontrivial token language with explicit parser state, guaranteed progress, and bounded complexity?
4. [Module 44: Hygiene, Scope, Paths, and Cross-Crate Macros](module-44-hygiene-scope-paths-and-cross-crate-macros/index.md) — Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?
5. [Module 45: Macro Diagnostics, Testing, and Public API Design](module-45-macro-diagnostics-testing-and-public-api-design/index.md) — How do you prove that a macro accepts the intended language, rejects misuse for the intended reason, and remains an evolvable public API?
6. [Module 46: Procedural Macro Execution and TokenStream Engineering](module-46-procedural-macro-execution-and-tokenstream-engineering/index.md) — What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?
7. [Module 47: Custom Derive Macros and Structural Generation](module-47-custom-derive-macros-and-structural-generation/index.md) — How do you inspect a Rust item, preserve its generics and constraints, and generate a lawful implementation without pretending to perform type checking?
8. [Module 48: Attribute Macros and Item Transformation](module-48-attribute-macros-and-item-transformation/index.md) — How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own?
9. [Module 49: Function-Like Procedural Macros and Typed DSLs](module-49-function-like-procedural-macros-and-typed-dsls/index.md) — How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?
10. [Module 50: Build Scripts, Generated Code, and Compile-Time Architecture](module-50-build-scripts-generated-code-and-compile-time-architecture/index.md) — How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?

## How the learning surfaces fit

The chapter is the authoritative explanation. The workbook exposes the model you actually hold through prediction, repair, construction, transfer, and defense. The independent lab removes accumulated capstone complexity so one mechanism remains visible. The capstone increment then asks that mechanism to coexist with every earlier decision.

The cumulative product is **CommandForge**: a compile-time validated command catalog combining a declarative diagnostic source of truth, an argument derive, a checked handler attribute, a typed catalog DSL, and deterministic build generation while leaving runtime command behavior in ordinary Rust. Do not read the complete implementation before attempting the corresponding increment; the value of the capstone is the sequence of design decisions, not possession of the finished source.

Use the [compiler investigations](../compiler-labs/README.md), the [ten-day study plan](study-plan.md), the [CommandForge engineering guide](capstone.md), the [course reference](reference.md), and the [independent final review](final-review.md).

## Completion standard

The course is complete when you can satisfy the public behavior, explain the decisive rule without notes, repair a misleading implementation without weakening its requirement, and transfer the mechanism to the final independent product. A passing test suite without a causal model is incomplete; a persuasive explanation without working evidence is also incomplete.

## Course handoff

Course 6 takes the phase and contract discipline developed here across byte, operating-system, unsafe, allocator, and foreign-language boundaries.

[Return to the program start](../../README.md) · [Open the ninety-module map](../../COURSE_MAP.md)
