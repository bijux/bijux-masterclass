# Course 1 — Rust Foundations

## Values, Ownership, Errors, and Complete Programs

## The promise

Course 1 makes ordinary Rust legible. It teaches you to read expressions as typed values, track ownership deliberately, model states with data types, treat failures as part of the interface, and finish a small program whose behavior is protected at several boundaries.

> **Governing question:** How do Rust’s types, ownership rules, state models, and error boundaries combine into a complete program you can explain end to end?

The program begins here: source text becomes typed expressions, values acquire owners, and small decisions become complete program behavior.

## Before Day 1

You should already understand variables, conditions, loops, functions, and collections in at least one programming language. No systems-programming or memory-management background is assumed.

From a blank page, sketch one earlier product or a comparable program. Mark an owner, a valid and invalid state, a failure path, cleanup, and a public promise. Repair any relationship you cannot explain before adding this course’s mechanisms.

## Outcomes

- Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”.
- Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior.
- Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger.
- Model shared and mutable references as permissions constrained by aliasing and validity.
- Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity.
- Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions.
- Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values.
- Write generic functions and types whose bounds correspond to operations actually performed.
- Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type.
- Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation.
- Integrate all ten mechanisms in Taskboard without creating competing authorities.
- Complete and defend an unseen change using a whole-program invariant map.

## The ten-day line

| Day | Module | Governing question | Capability that must become visible | Laboratory |
|---:|---|---|---|---|
| 1 | [1 — Compilation, Expressions, and Types](./module-01-compilation-expressions-and-types/index.md) | How does Rust turn source text into a typed program, and what type and value does every expression produce? | **Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”.** | [Measurement Report](../labs/module-01-measurement-report/README.md) |
| 2 | [2 — Control Flow, Functions, and Invariants](./module-02-control-flow-functions-and-invariants/index.md) | How can control flow make every path, boundary, and loop invariant visible enough to test and review? | **Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior.** | [Control-Flow Policy Engine](../labs/module-02-control-flow-policy/README.md) |
| 3 | [3 — Ownership, Moves, Copying, and Destruction](./module-03-ownership-moves-copying-and-destruction/index.md) | Who owns each resource after every assignment, call, return, destructure, and scope exit? | **Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger.** | [Ownership Intake Pipeline](../labs/module-03-ownership-intake/README.md) |
| 4 | [4 — Borrowing, References, Slices, and Strings](./module-04-borrowing-references-slices-and-strings/index.md) | Which temporary permissions does an operation require, and how narrowly can those permissions be scoped? | **Model shared and mutable references as permissions constrained by aliasing and validity.** | [Borrowed Catalog](../labs/module-04-borrowed-catalog/README.md) |
| 5 | [5 — Structs, Enums, Methods, and Pattern Matching](./module-05-structs-enums-methods-and-pattern-matching/index.md) | How can the type system make valid states representable and contradictory states difficult or impossible to construct? | **Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity.** | [Typed Workflow State Machine](../labs/module-05-state-machine/README.md) |
| 6 | [6 — Collections, Iterators, and Closures](./module-06-collections-iterators-and-closures/index.md) | Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow? | **Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions.** | [In-Memory Task Board](../labs/module-06-in-memory-board/README.md) |
| 7 | [7 — Errors, Parsing, Files, and Persistence](./module-07-errors-parsing-files-and-persistence/index.md) | Which failures are part of the product contract, where are they detected, and what state is visible after failure? | **Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values.** | [Versioned Record Codec](../labs/module-07-record-codec/README.md) |
| 8 | [8 — Generics, Traits, Conversions, and Lifetime Basics](./module-08-generics-traits-conversions-and-lifetime-basics/index.md) | What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose? | **Write generic functions and types whose bounds correspond to operations actually performed.** | [Trait and Lifetime Boundary](../labs/module-08-traits-and-lifetimes/README.md) |
| 9 | [9 — Crates, Modules, Public APIs, Tests, and Documentation](./module-09-crates-modules-public-apis-tests-and-documentation/index.md) | Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary? | **Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type.** | [Library Boundary Refactor](../labs/module-09-library-boundaries/README.md) |
| 10 | [10 — Integration and Independent Change](./module-10-integration-and-independent-change/index.md) | Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression? | **Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation.** | [Inventory Ledger](../labs/module-10-inventory-ledger/README.md) |

The table is a dependency chain, not a menu. A later module may use an earlier mechanism but may not silently weaken its ownership, failure, ordering, capacity, safety, compatibility, or evidence contract.

## Decision rules

| Decision | Rule used throughout this course |
|---|---|
| Type choice | Choose from the domain range, sign, precision, and overflow policy—not from example habit. |
| Ownership choice | Consume only when the caller should lose the value; borrow for temporary access; clone only when the product needs two independent owners. |
| State model | Prefer one enum state over several flags that can contradict each other. |
| Failure model | Use `Option` for absence and `Result` for an operation that can fail with useful information. |
| Test boundary | Test the public behavior at the narrowest boundary that can observe the promise. |

Use these rules during prediction and review. When a rule does not decide the case, write the missing product requirement instead of selecting an API by habit.

## The reasoning record

The ten module-specific records culminate in a **whole-program invariant map**. Trace type, value, owner, state, and error from source input to visible output. Keep the record small enough to inspect but complete enough to expose the first unsupported assumption.

## Scope and handoff

The course stays in safe Rust and mostly in the standard library. It introduces the ownership, trait, iterator, lifetime, module, and testing vocabulary required by later courses, but it does not yet pursue advanced lifetime algebra, smart-pointer architecture, unsafe code, concurrency, async runtimes, or macro construction.

Course 2 returns to ownership at a deeper level: places, loans, lifetimes, destruction, shared liveness, representation, variance, and pinning.

## Capstone — Taskboard

Taskboard is a local persistent command-line work queue. Its small domain forces types, ownership, parsing, state transitions, storage, errors, modules, tests, and process behavior to work together without hiding the language behind a framework.

Open the [engineering guide](capstone.md) before Day 1 so the final architecture is visible. Implement only the current increment. The independent laboratory remains separate so that the mechanism can be learned without hiding behind accumulated capstone code.

## Completion

The course is complete when you can build and defend:

> Build a small persistent inventory program from a behavioral contract. It must use typed states, contextual errors, deterministic storage, a library/binary split, and tests that protect both successful and failing behavior.

and then change the capstone under this constraint:

> Add one cross-layer Taskboard feature—such as due dates or labels—without weakening deterministic storage, typed transitions, or failure atomicity.

A passing test suite is necessary. It is not sufficient unless you can explain why the tests are capable of falsifying the claim and which target-, scheduler-, workload-, peer-, or policy-dependent facts remain outside them.

## Continue

- [Ten-day plan](study-plan.md)
- [Module 1 — Compilation, Expressions, and Types](./module-01-compilation-expressions-and-types/index.md)
- [Taskboard engineering guide](capstone.md)
- [Course reference](reference.md)
- [Final review](final-review.md)
- [Compiler and design investigations](../compiler-labs/README.md)
- [Independent laboratories](../labs/)
