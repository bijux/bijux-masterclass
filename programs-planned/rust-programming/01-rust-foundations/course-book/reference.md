# Course 1 Reference Desk — Rust Foundations

Use this page while designing or reviewing. It is a decision aid, not a replacement for the module explanations.

## Governing question

> How do Rust’s types, ownership rules, state models, and error boundaries combine into a complete program you can explain end to end?

## Working record

Keep a type trace, ownership ledger, state-transition table, error map, and public-boundary map. A design is not ready when the record still contains unnamed owners, contradictory states, implicit failure, accidental order, unbounded accumulation, or a claim with no matching evidence.

## Decision rules

| Decision | Rule |
|---|---|
| Type choice | Choose from the domain range, sign, precision, and overflow policy—not from example habit. |
| Ownership choice | Consume only when the caller should lose the value; borrow for temporary access; clone only when the product needs two independent owners. |
| State model | Prefer one enum state over several flags that can contradict each other. |
| Failure model | Use `Option` for absence and `Result` for an operation that can fail with useful information. |
| Test boundary | Test the public behavior at the narrowest boundary that can observe the promise. |

## Module quick reference

| Module | Mechanism | Minimum usable outcome |
|---:|---|---|
| 1 | Compilation, Expressions, and Types | Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project” |
| 2 | Control Flow, Functions, and Invariants | Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior |
| 3 | Ownership, Moves, Copying, and Destruction | Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger |
| 4 | Borrowing, References, Slices, and Strings | Model shared and mutable references as permissions constrained by aliasing and validity |
| 5 | Structs, Enums, Methods, and Pattern Matching | Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity |
| 6 | Collections, Iterators, and Closures | Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions |
| 7 | Errors, Parsing, Files, and Persistence | Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values |
| 8 | Generics, Traits, Conversions, and Lifetime Basics | Write generic functions and types whose bounds correspond to operations actually performed |
| 9 | Crates, Modules, Public APIs, Tests, and Documentation | Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type |
| 10 | Integration and Independent Change | Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation |

## Claim boundary

Separate language guarantees, library contracts, product policy, target observations, and measured artifact facts. When an exact API or version detail matters, follow the primary source from [Source Notes](../../SOURCE_NOTES.md).

Use this page after deriving the ideas in the chapters. It compresses decisions; it does not replace the reasoning that justifies them.

## Program anatomy

| Term | Meaning | Common confusion |
|---|---|---|
| package | one `Cargo.toml` plus its targets | not the same as a crate |
| target | a library, binary, example, test, or benchmark Cargo builds | one package may have several |
| crate | one compilation unit | modules live inside a crate |
| module | namespace and privacy structure inside a crate | not a dependency package |
| expression | produces a value and has a type | a trailing semicolon discards the value to `()` |
| statement | performs an action in a block | most statements do not become the block value |

For every function, trace the final expression and every early return. For every branch, derive one common type. Choose numeric behavior—checked, saturating, wrapping, or rejecting—from the domain contract rather than debug/release accident.

## Ownership decision table

| The operation must… | Prefer |
|---|---|
| keep a value beyond the call | take ownership or construct an owned result |
| inspect without retaining | `&T` |
| mutate in place without retaining | `&mut T` |
| inspect a contiguous region | `&[T]` or `&str` |
| represent optional presence | `Option<T>` |
| report recoverable failure | `Result<T, E>` |
| duplicate independently owned data | `Clone`, only when duplication is part of the requirement |

A move changes which binding may use a value. It does not imply that every byte is physically copied. A borrow is a temporary permission tied to a real owner; it is not a hidden duplicate.

## Modeling valid states

Prefer one source of truth:

- a struct groups facts that exist together;
- an enum represents one of several states or commands;
- a newtype distinguishes values with the same representation but different meaning;
- private fields keep constructors and transitions authoritative;
- exhaustive `match` makes new variants visible to the compiler.

Replace contradictory Boolean flags with one enum. Replace sentinel values with `Option`. Replace free-form strings with a closed type when the vocabulary is closed.

## Collections and traversal

| Form | Item shape | Collection afterward |
|---|---|---|
| `for item in &items` / `items.iter()` | `&T` | still owned and usable |
| `for item in &mut items` / `items.iter_mut()` | `&mut T` | still owned and usable after the loop |
| `for item in items` / `items.into_iter()` | `T` | consumed |

Prefer `get` when absence is ordinary. Index only when the invariant proving the index is local and obvious. Do not rely on `HashMap` iteration order for user-visible output; sort a derived view when determinism matters.

## Errors and persistence

Ask four questions:

1. Is this absence, recoverable failure, or an invariant violation?
2. Which layer first knows enough to classify it?
3. What context will the caller need?
4. What state remains visible after failure?

Parse text into a typed command before mutating domain state. Parse a complete stored representation before replacing live state. Keep line numbers and original causes. Missing storage may mean an empty product when the contract says so; malformed storage must not silently mean empty.

## Public boundary checklist

- Is the binary a thin effect shell over a library?
- Are public fields necessary, or should constructors and accessors protect invariants?
- Are unit tests close to private logic and integration tests written against the public surface?
- Do documentation examples compile?
- Does `cargo check --all-targets` cover every target you claim?
- Do formatting and Clippy policies reveal rather than hide design problems?

## Course 1 readiness

You are ready for Course 2 when you can trace ownership through a complete command, explain every borrowed parameter, model legal state transitions with types, preserve context through errors, and add a cross-layer Taskboard feature without making internal fields public or cloning around a missing design decision.
