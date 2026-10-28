# Course 1 — Rust Foundations

## Values, Ownership, Errors, and Complete Programs

Course 1 makes ordinary Rust legible. It teaches you to read expressions as typed values, track ownership deliberately, model states with data types, treat failures as part of the interface, and finish a small program whose behavior is protected at several boundaries.

> **Governing question:** How do Rust’s types, ownership rules, state models, and error boundaries combine into a complete program you can explain end to end?

## Entry point

You should already understand variables, conditions, loops, functions, and collections in at least one programming language. No systems-programming or memory-management background is assumed.

The immediate prerequisite is basic programming experience. Entering mid-program is reasonable only when you can complete the previous course’s final review and one independent construction without following its solution.

## Ten-day route

| Day | Module | Capability added | Independent laboratory |
|---:|---|---|---|
| 1 | [1 — Compilation, Expressions, and Types](course-book/module-01-compilation-expressions-and-types/index.md) | Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project” | [Measurement Report](labs/module-01-measurement-report/README.md) |
| 2 | [2 — Control Flow, Functions, and Invariants](course-book/module-02-control-flow-functions-and-invariants/index.md) | Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior | [Control-Flow Policy Engine](labs/module-02-control-flow-policy/README.md) |
| 3 | [3 — Ownership, Moves, Copying, and Destruction](course-book/module-03-ownership-moves-copying-and-destruction/index.md) | Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger | [Ownership Intake Pipeline](labs/module-03-ownership-intake/README.md) |
| 4 | [4 — Borrowing, References, Slices, and Strings](course-book/module-04-borrowing-references-slices-and-strings/index.md) | Model shared and mutable references as permissions constrained by aliasing and validity | [Borrowed Catalog](labs/module-04-borrowed-catalog/README.md) |
| 5 | [5 — Structs, Enums, Methods, and Pattern Matching](course-book/module-05-structs-enums-methods-and-pattern-matching/index.md) | Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity | [Typed Workflow State Machine](labs/module-05-state-machine/README.md) |
| 6 | [6 — Collections, Iterators, and Closures](course-book/module-06-collections-iterators-and-closures/index.md) | Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions | [In-Memory Task Board](labs/module-06-in-memory-board/README.md) |
| 7 | [7 — Errors, Parsing, Files, and Persistence](course-book/module-07-errors-parsing-files-and-persistence/index.md) | Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values | [Versioned Record Codec](labs/module-07-record-codec/README.md) |
| 8 | [8 — Generics, Traits, Conversions, and Lifetime Basics](course-book/module-08-generics-traits-conversions-and-lifetime-basics/index.md) | Write generic functions and types whose bounds correspond to operations actually performed | [Trait and Lifetime Boundary](labs/module-08-traits-and-lifetimes/README.md) |
| 9 | [9 — Crates, Modules, Public APIs, Tests, and Documentation](course-book/module-09-crates-modules-public-apis-tests-and-documentation/index.md) | Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type | [Library Boundary Refactor](labs/module-09-library-boundaries/README.md) |
| 10 | [10 — Integration and Independent Change](course-book/module-10-integration-and-independent-change/index.md) | Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation | [Inventory Ledger](labs/module-10-inventory-ledger/README.md) |

The route is cumulative. Day 1 establishes this course’s vocabulary and Day 10 requires an architectural change that preserves all earlier guarantees.

## Working method

Trace type, value, owner, state, and error from source input to visible output. Use the module-specific reasoning record named in each chapter. Freeze predictions before compiling, preserve causal diagnostics, and compare the lab reference only after recording your own design.

## Capstone — Taskboard

Taskboard is a local persistent command-line work queue. Its small domain forces types, ownership, parsing, state transitions, storage, errors, modules, tests, and process behavior to work together without hiding the language behind a framework.

The [engineering guide](course-book/capstone.md) supplies the ten integration steps. The executable [capstone directory](capstone/README.md) contains the product and tests. Each increment must name the changed invariant, the component that owns it, state after failure, and the earlier guarantee that must remain unchanged.

## Scope

The course stays in safe Rust and mostly in the standard library. It introduces the ownership, trait, iterator, lifetime, module, and testing vocabulary required by later courses, but it does not yet pursue advanced lifetime algebra, smart-pointer architecture, unsafe code, concurrency, async runtimes, or macro construction.

Course 2 returns to ownership at a deeper level: places, loans, lifetimes, destruction, shared liveness, representation, variance, and pinning.

## Exit standard

Complete this independent construction:

> Build a small persistent inventory program from a behavioral contract. It must use typed states, contextual errors, deterministic storage, a library/binary split, and tests that protect both successful and failing behavior.

Then complete this capstone extension:

> Add one cross-layer Taskboard feature—such as due dates or labels—without weakening deterministic storage, typed transitions, or failure atomicity.

The next step is [Course 2: Ownership, Lifetimes, and Memory](../02-rust-ownership-lifetimes-memory/course-book/index.md).

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
