# Course 5 reference — Rust Metaprogramming

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
