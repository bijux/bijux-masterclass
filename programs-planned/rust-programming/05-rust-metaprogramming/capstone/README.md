# CommandForge

## Course role

CommandForge combines a declarative diagnostic catalog, a custom argument derive, a checked handler attribute, a typed command-catalog DSL, and deterministic build-script input while keeping runtime command behavior in ordinary Rust.

CommandForge is not a showcase of ten independent features. It is the place where the course’s mechanisms must coexist without creating a second owner for state, validation, order, failure, compatibility, or resource policy.

## Invariants carried through the product

- Every generated fact has exactly one compile-time source of truth.
- Declarative syntax has an explicit accepted grammar and causal rejection rules.
- Expansion resolves definition-owned names through robust paths and preserves call-site inputs.
- Derives and attributes preserve supported generics, visibility, signatures, and user attributes.
- Typed DSLs separate syntax parsing, semantic validation, normalized model, and generation.
- Build generation declares inputs, writes deterministically under OUT_DIR, and never edits source.

## Module-to-product map

| Module | Mechanism added | Acceptance criterion |
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

## Reading route

1. Read the CommandForge contract and non-goals in the [engineering guide](../course-book/capstone.md).
2. Locate the type or component that owns each invariant above.
3. Run the baseline tests and one end-to-end demonstration before changing code.
4. Implement only the current module increment and its adversarial test.
5. Trace success, rejection, partial failure, cleanup, order, and capacity through the public surface.
6. Re-run the complete course route, then explain which claims remain conditioned on a compiler, target, scheduler, peer, workload, or operating system.

CommandForge is the cumulative product for Rust Course 5. It is a small command framework whose compile-time layers each have one authority:

- `diagnostic_catalog!` owns diagnostic variants, stable diagnostic codes, messages, reverse lookup, and catalog order.
- `#[derive(CommandArgs)]` owns repetitive decoding derived from an ordinary argument struct and its field helper attributes.
- `#[command_handler]` validates a handler boundary, preserves the function, and generates a typed descriptor.
- `command_catalog!` owns cross-command name uniqueness, catalog order, descriptor association, and lookup generation.
- `build.rs` owns checked external exit-code data and generates Rust under `OUT_DIR`.
- ordinary Rust owns command behavior, application routing, output, and errors.

## Commands

```text
commandforge list
commandforge explain <command>
commandforge run add --left <i64> --right <i64>
commandforge run slug --text <text>
commandforge run repeat --text <text> [--times <u32>]
commandforge run contains --text <text> --needle <text>
commandforge demo
commandforge help
commandforge version
```

## Verification

```bash
cargo test --manifest-path Cargo.toml --all-targets
cargo test --manifest-path Cargo.toml --doc
cargo clippy --manifest-path Cargo.toml --all-targets -- -D warnings
cargo run --manifest-path Cargo.toml -- demo
```

Read `../course-book/capstone.md` before modifying the architecture. The guide explains the source-of-truth map, generated surfaces, negative contracts, testing strategy, and each module increment.
