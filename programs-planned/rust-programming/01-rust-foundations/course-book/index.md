# Course 1 — Rust Foundations

## Values, Ownership, and Complete Programs

Learn to read Rust as a typed language, make ownership and failure visible, model valid states, and finish a complete tested program without depending on framework magic.

## Why this course exists

Rust becomes difficult when syntax, ownership, domain modeling, error handling, and project structure are taught as separate lists. This course instead follows one program from expressions to a complete persistent command-line product. Every new feature answers a concrete question: what value exists, who owns it, which states are valid, how failure is represented, and which boundary proves the behavior. The result is not merely familiarity with syntax; it is the ability to make an independent change and explain why the program remains correct.

## Before you begin

Basic programming experience with variables, conditions, loops, functions, and collections in any mainstream language. No systems-programming or Rust experience is assumed.

Keep a type-and-state trace, ownership ledger, and failure table beside the code. The record changes shape as the course advances, but its purpose is constant: make the decisive relationship visible before syntax hides it.

## What you will be able to do

- Distinguish package, crate, target, module, compiler, Cargo profile, and build artifact, then use compiler diagnostics as structured evidence rather than trial-and-error instructions.
- Derive the type and value of blocks, branches, tuples, arrays, function bodies, and semicolon-sensitive expressions before compiling.
- Choose `if`, `match`, `for`, `while`, or `loop` from data shape and termination knowledge, then state the invariant maintained by the control flow.
- Trace ownership through bindings, calls, returns, aggregates, destructuring, and scope exit; distinguish moves, `Copy`, explicit `Clone`, and destruction.
- Choose owned values, shared references, mutable references, slices, `String`, and `&str` from the operation’s authority and lifetime requirements.
- Model domain values with structs, newtypes, enums, methods, and exhaustive patterns so contradictory states are difficult or impossible to construct.
- Use `Vec`, `HashMap`, slices, and iterators while predicting whether traversal borrows, mutates, or consumes the collection and what invalidation or ordering consequences follow.
- Represent absence with `Option`, recoverable failure with `Result`, and invariant failure deliberately; propagate errors without routine `unwrap` or silent fallback.
- Separate parsing, validation, domain mutation, rendering, and file I/O so failed input cannot partially corrupt accepted state.
- Write foundational generic functions, trait implementations, conversions, and lifetime relationships without inventing abstractions before real duplication exists.
- Split a product into restrained modules, a reusable library, and a thin binary while keeping representation private and the public API intentional.
- Write unit, integration, and documentation tests that prove different boundaries; use rustfmt, Clippy, rustdoc, and Cargo’s build/test routes deliberately.
- Build and maintain a versioned local storage format with deterministic output and contextual malformed-input errors.
- Implement an unseen cross-layer feature from a behavioral specification, update regression evidence, and preserve earlier invariants.
- Explain every important function signature in terms of ownership, mutation authority, failure, and public contract rather than saying only that the compiler accepts it.

## What this course deliberately leaves for later

This course deliberately stays in safe Rust and the standard library. Advanced lifetime design, smart-pointer architecture, unsafe code, macros, concurrency, async runtimes, and performance measurement belong to later courses.

## Ten-day route

1. [Module 1: Compilation, Expressions, and Types](module-01-compilation-expressions-and-types/index.md) — How does Rust turn source text into a typed program, and what type and value does every expression produce?
2. [Module 2: Control Flow, Functions, and Invariants](module-02-control-flow-functions-and-invariants/index.md) — How can control flow make every path, boundary, and loop invariant visible enough to test and review?
3. [Module 3: Ownership, Moves, Copying, and Destruction](module-03-ownership-moves-copying-and-destruction/index.md) — Who owns each resource after every assignment, call, return, destructure, and scope exit?
4. [Module 4: Borrowing, References, Slices, and Strings](module-04-borrowing-references-slices-and-strings/index.md) — Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?
5. [Module 5: Structs, Enums, Methods, and Pattern Matching](module-05-structs-enums-methods-and-pattern-matching/index.md) — How can the type system make valid states representable and contradictory states difficult or impossible to construct?
6. [Module 6: Collections, Iterators, and Closures](module-06-collections-iterators-and-closures/index.md) — Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?
7. [Module 7: Errors, Parsing, Files, and Persistence](module-07-errors-parsing-files-and-persistence/index.md) — Which failures are part of the product contract, where are they detected, and what state is visible after failure?
8. [Module 8: Generics, Traits, Conversions, and Lifetime Basics](module-08-generics-traits-conversions-and-lifetime-basics/index.md) — What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?
9. [Module 9: Crates, Modules, Public APIs, Tests, and Documentation](module-09-crates-modules-public-apis-tests-and-documentation/index.md) — Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?
10. [Module 10: Integration and Independent Change](module-10-integration-and-independent-change/index.md) — Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?

## How the learning surfaces fit

The chapter is the authoritative explanation. The workbook exposes the model you actually hold through prediction, repair, construction, transfer, and defense. The independent lab removes accumulated capstone complexity so one mechanism remains visible. The capstone increment then asks that mechanism to coexist with every earlier decision.

The cumulative product is **Taskboard**: a persistent typed command-line task board that grows from pure functions into a library, binary, storage format, tests, documentation, and an independently designed feature. Do not read the complete implementation before attempting the corresponding increment; the value of the capstone is the sequence of design decisions, not possession of the finished source.

Use the [compiler investigations](../compiler-labs/README.md), the [ten-day study plan](study-plan.md), the [Taskboard engineering guide](capstone.md), the [course reference](reference.md), and the [independent final review](final-review.md).

## Completion standard

The course is complete when you can satisfy the public behavior, explain the decisive rule without notes, repair a misleading implementation without weakening its requirement, and transfer the mechanism to the final independent product. A passing test suite without a causal model is incomplete; a persuasive explanation without working evidence is also incomplete.

## Course handoff

Course 2 keeps the same ownership model but studies it at the level of places, provenance, destruction, sharing, layout, and address sensitivity.

[Return to the program start](../../README.md) · [Open the sixty-module map](../../COURSE_MAP.md)
