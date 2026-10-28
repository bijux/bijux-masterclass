# Course 5 — Rust Metaprogramming

## Declarative Macros, Procedural Macros, DSLs, and Build-Time Authority

Course 5 treats metaprogramming as language and authority design. It covers declarative grammar, recursive token processing, hygiene, diagnostics, procedural-macro phases, derives, attributes, typed DSLs, and deterministic build generation.

> **Governing question:** Which facts deserve one compile-time source of truth, which generation mechanism is the least powerful adequate choice, and how can expanded code remain diagnosable ordinary Rust?

## Entry point

You should be able to design traits and public APIs, reason about ordinary Rust expansion targets, write tests at several boundaries, and separate deterministic core logic from effects.

The immediate prerequisite is [Course 4: Functional Rust](../04-rust-functional-programming/course-book/index.md). Entering mid-program is reasonable only when you can complete the previous course’s final review and one independent construction without following its solution.

## Ten-day route

| Day | Module | Capability added | Independent laboratory |
|---:|---|---|---|
| 1 | [41 — Metaprogramming Boundaries and the Expansion Model](course-book/module-41-metaprogramming-boundaries-and-expansion-model/index.md) | Separate runtime abstraction from compile-time generation | [Decision Table Generator](labs/module-01-decision-table-generator/README.md) |
| 2 | [42 — Declarative Macros: Matchers, Fragments, and Repetition](course-book/module-42-declarative-macros-matchers-fragments-and-repetition/index.md) | Read a matcher as a grammar rather than as textual substitution | [Typed Map Macro](labs/module-02-typed-map-macro/README.md) |
| 3 | [43 — Recursive Macro Parsing and Token-Tree Techniques](course-book/module-43-recursive-macro-parsing-and-token-tree-techniques/index.md) | Model recursive macro rules as parser states and transitions | [State Machine DSL](labs/module-03-state-machine-dsl/README.md) |
| 4 | [44 — Hygiene, Scope, Paths, and Cross-Crate Macros](course-book/module-44-hygiene-scope-paths-and-cross-crate-macros/index.md) | Distinguish textual scope, path-based scope, and expansion-site lookup for declarative macros | [Exported Registry Macro](labs/module-04-exported-registry-macro/README.md) |
| 5 | [45 — Macro Diagnostics, Testing, and Public API Design](course-book/module-45-macro-diagnostics-testing-and-public-api-design/index.md) | Treat invocation grammar and generated Rust as two related public APIs | [Diagnostic Enum Macro](labs/module-05-diagnostic-enum-macro/README.md) |
| 6 | [46 — Procedural Macro Execution and TokenStream Engineering](course-book/module-46-procedural-macro-execution-and-tokenstream-engineering/index.md) | Explain when and how a procedural macro executes | [TokenStream Inspector](labs/module-06-token-stream-inspector/README.md) |
| 7 | [47 — Custom Derive Macros and Structural Generation](course-book/module-47-custom-derive-macros-and-structural-generation/index.md) | Parse `DeriveInput` and distinguish structs, enums, and unions | [Field Names Derive](labs/module-07-field-names-derive/README.md) |
| 8 | [48 — Attribute Macros and Item Transformation](course-book/module-48-attribute-macros-and-item-transformation/index.md) | Parse attribute arguments independently from the attached item | [Checked Handler Attribute](labs/module-08-checked-handler-attribute/README.md) |
| 9 | [49 — Function-Like Procedural Macros and Typed DSLs](course-book/module-49-function-like-procedural-macros-and-typed-dsls/index.md) | Design a bounded custom grammar with explicit compatibility space | [Route Table DSL](labs/module-09-route-table-dsl/README.md) |
| 10 | [50 — Build Scripts, Generated Code, and Compile-Time Architecture](course-book/module-50-build-scripts-generated-code-and-compile-time-architecture/index.md) | Explain the Cargo build-script lifecycle and communication protocol | [Generated Code Build](labs/module-10-generated-code-build/README.md) |

The route is cumulative. Day 1 establishes this course’s vocabulary and Day 10 requires an architectural change that preserves all earlier guarantees.

## Working method

Name the phase and source of truth, write the accepted grammar, inspect the expansion, and test causal rejection before adding generation. Use the module-specific reasoning record named in each chapter. Freeze predictions before compiling, preserve causal diagnostics, and compare the lab reference only after recording your own design.

## Capstone — CommandForge

CommandForge combines a declarative diagnostic catalog, a custom argument derive, a checked handler attribute, a typed command-catalog DSL, and deterministic build-script input while keeping runtime command behavior in ordinary Rust.

The [engineering guide](course-book/capstone.md) supplies the ten integration steps. The executable [capstone directory](capstone/README.md) contains the product and tests. Each increment must name the changed invariant, the component that owns it, state after failure, and the earlier guarantee that must remain unchanged.

## Scope

The course generates ordinary Rust but does not make macros the default abstraction. It avoids using generation for runtime policy, postpones low-level unsafe implementation, and treats third-party procedural-macro crates as compiler-phase dependencies with explicit version and reproducibility implications.

Course 6 leaves the compiler boundary and crosses external byte, file, process, allocator, ABI, callback, and foreign-resource boundaries.

## Exit standard

Complete this independent construction:

> Build a small generated command or protocol catalog using at least two distinct macro mechanisms. Every generated fact must have one authority, targeted invalid-input diagnostics, and expansion tests.

Then complete this capstone extension:

> Add a new CommandForge field policy and command kind, tracing the change through grammar, semantic validation, expansion, runtime behavior, tests, and compatibility.

The next step is [Course 6: Rust Systems Programming](../06-rust-systems-programming/course-book/index.md).

## Reading and execution routes

- [Course book](course-book/index.md)
- [Ten-day study plan](course-book/study-plan.md)
- [Course reference](course-book/reference.md)
- [Final review](course-book/final-review.md)
- [Compiler and design investigations](compiler-labs/README.md)
- [Laboratories](labs/)

```bash
make static-proof
make compiler-labs
make check
make test
make starters
make docs
make proof
```

Static inspection and compilation answer different questions. The strongest completion route uses the pinned toolchain, executes tests and investigations, renders the book, and preserves the resulting evidence with the code under review.
