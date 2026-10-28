# Course 5 Reference Desk — Rust Metaprogramming

Use this page while designing or reviewing. It is a decision aid, not a replacement for the module explanations.

## Governing question

> Which facts deserve one compile-time source of truth, which generation mechanism is the least powerful adequate choice, and how can expanded code remain diagnosable ordinary Rust?

## Working record

Keep a authority map, accepted grammar, token and repetition trace, hygiene/path map, expansion ledger, diagnostic contract, phase map, generated-surface inventory, and reproducibility record. A design is not ready when the record still contains unnamed owners, contradictory states, implicit failure, accidental order, unbounded accumulation, or a claim with no matching evidence.

## Decision rules

| Decision | Rule |
|---|---|
| Mechanism choice | Prefer ordinary Rust; use the least powerful generation mechanism that owns one real source of truth. |
| Grammar | Define accepted and rejected syntax before writing matcher arms or parser code. |
| Hygiene | Make definition-site and invocation-site names deliberate, especially across crates. |
| Diagnostic | Treat invalid syntax and unsupported structures as part of the public macro contract. |
| Generation | Normalize validated input before emitting deterministic ordinary Rust. |

## Module quick reference

| Module | Mechanism | Minimum usable outcome |
|---:|---|---|
| 41 | Metaprogramming Boundaries and the Expansion Model | Separate runtime abstraction from compile-time generation |
| 42 | Declarative Macros: Matchers, Fragments, and Repetition | Read a matcher as a grammar rather than as textual substitution |
| 43 | Recursive Macro Parsing and Token-Tree Techniques | Model recursive macro rules as parser states and transitions |
| 44 | Hygiene, Scope, Paths, and Cross-Crate Macros | Distinguish textual scope, path-based scope, and expansion-site lookup for declarative macros |
| 45 | Macro Diagnostics, Testing, and Public API Design | Treat invocation grammar and generated Rust as two related public APIs |
| 46 | Procedural Macro Execution and TokenStream Engineering | Explain when and how a procedural macro executes |
| 47 | Custom Derive Macros and Structural Generation | Parse `DeriveInput` and distinguish structs, enums, and unions |
| 48 | Attribute Macros and Item Transformation | Parse attribute arguments independently from the attached item |
| 49 | Function-Like Procedural Macros and Typed DSLs | Design a bounded custom grammar with explicit compatibility space |
| 50 | Build Scripts, Generated Code, and Compile-Time Architecture | Explain the Cargo build-script lifecycle and communication protocol |

## Claim boundary

Separate language guarantees, library contracts, product policy, target observations, and measured artifact facts. When an exact API or version detail matters, follow the primary source from [Source Notes](../../SOURCE_NOTES.md).

## Mechanism ladder

Choose the least powerful mechanism that can own the relationship:

1. ordinary value, function, enum, trait, or parser;
2. `macro_rules!` for a local syntactic relationship expressible by token matching and repetition;
3. custom derive when an item’s structure should generate one repetitive implementation;
4. attribute macro when one attached item must be validated or augmented;
5. function-like procedural macro for a custom compile-time language with semantic checks;
6. build script for validated external inputs and Cargo-directed generation.

The deletion test asks what handwritten authority would replace the generator and which relationship could drift. “Fewer lines” is not enough.

## Expansion ledger

For every generator, record:

```text
source of truth | accepted grammar | rejected syntax | parsed/normalized model |
emitted Rust | names and paths | evaluation/ownership semantics |
diagnostic phase | deterministic order | compatibility surface
```

Reason about two programs: the generator and the expanded Rust program. A macro can accept input successfully and still emit code that later fails name resolution, type checking, borrowing, or runtime tests.

## Declarative macros

- fragment kinds delegate parts of Rust grammar; `tt` is not a universal substitute;
- repetition depth in matcher and transcriber must remain compatible;
- optional trailing separators should be one deliberate grammar, not overlapping catch-all rules;
- bind caller expressions once when evaluation count matters;
- expand to one expression, item sequence, type, or pattern valid in the invocation position;
- use `$crate` for definition-crate paths in exported declarative macros;
- treat accepted punctuation and invocation shape as public API.

Recursive token munchers need explicit parser state, a guaranteed progress measure, a terminal rule, and causal error rules. Prefer a procedural parser when cross-entry semantics, rich diagnostics, or maintainability exceed what token-tree recursion can express clearly.

## Procedural macros

A procedural macro receives tokens, not typed Rust semantics. It can parse syntax and inspect item structure, but it cannot assume type checking has already established trait implementations or resolved arbitrary expressions.

Keep entry points thin:

```text
TokenStream → parse → validate → normalized model → generate → TokenStream
```

Preserve generics, where clauses, visibility, unrelated attributes, and spans where the macro does not own them. Combine independent errors so one compile reveals more than the first defect.

## Derive, attribute, or function-like?

- derive: the item remains the primary declaration; generate companion implementations from its structure;
- attribute: the attached item is validated or transformed; preserve the parts the attribute does not own;
- function-like: the invocation is a standalone DSL with its own grammar and cross-entry rules.

## Build scripts

A build script must declare its inputs through Cargo rerun directives, validate external data before emission, write generated Rust under `OUT_DIR`, and produce deterministic output. Environment variables, target information, files, and tool invocations are build inputs and therefore part of reproducibility.

## Macro testing matrix

Test four layers separately:

1. accepted syntax that expands and runs;
2. rejected macro syntax;
3. valid syntax rejected by macro semantic validation;
4. valid expansion rejected by ordinary Rust name/type/borrow checking.

Inspect generated surfaces when practical, but do not make unstable compiler wording the only contract. Test the causal category and the important message fragment.

## Course 5 readiness

You are ready for Course 6 when you can reject unnecessary macros, write a precise grammar, trace expansion and name resolution, preserve evaluation semantics, build a derive and attribute around ordinary parsing/validation functions, design a typed DSL, and audit a build script as executable compile-time code.
