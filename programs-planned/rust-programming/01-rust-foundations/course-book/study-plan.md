# Course 1 study plan — Rust Foundations

This plan turns ten chapters into ten days of deliberate practice. A day is complete only when the model, independent laboratory, and Taskboard increment agree. If the lab passes while the explanation remains vague, repair the model before moving on.

## Daily rhythm

| Time | Work | Required output |
|---|---|---|
| 08:30–09:00 | closed-book reconstruction | one page of the previous mechanism from memory |
| 09:00–11:00 | authoritative chapter and typed examples | annotated model and changed-assumption predictions |
| 11:15–12:30 | compiler or boundary specimens | frozen predictions and causal comparison |
| 13:30–15:00 | repair and focused construction | smallest principled repair plus rejected shortcut |
| 15:15–17:30 | independent laboratory | working behavior, adversarial tests, design record |
| 18:30–20:00 | Taskboard increment | integrated change and regression evidence |
| 20:00–20:30 | explanation and retrieval | invariant, decisive rule, failure state, transfer case |

Take real breaks. Dense work is not continuous screen time. The weekend between Days 5 and 6 is for repair, reconstruction, and rest rather than new material.

## Day 1 — Compilation, Expressions, and Types

**Governing question:** How does Rust turn source text into a typed program, and what type and value does every expression produce?

### Morning: derive the model

Read [Module 1](module-01-compilation-expressions-and-types/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-01-compilation-expressions-and-types/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 1 — Measurement Report](../labs/module-01-measurement-report/README.md). Build a small library and binary that summarize borrowed `f64` measurements.

### Evening: integrate the course product

The course capstone is **Taskboard**, a persistent command-line task board. Create the Taskboard package, its help surface, and a title-validation function. The important product lesson is that even the first small function has a type contract and tests. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“How does Rust turn source text into a typed program, and what type and value does every expression produce?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 2 — Control Flow, Functions, and Invariants

**Governing question:** How can control flow make every path, boundary, and loop invariant visible enough to test and review?

### Morning: derive the model

Read [Module 2](module-02-control-flow-functions-and-invariants/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-02-control-flow-functions-and-invariants/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 2 — Control-Flow Policy Engine](../labs/module-02-control-flow-policy/README.md). Build a pure library that simulates textual work-item operations before typed domain modeling is available.

### Evening: integrate the course product

The course capstone is **Taskboard**, a persistent command-line task board. Write pure policy functions for identifiers, priorities, and state-transition sketches. Keep command parsing out until the decisions can be tested without I/O. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“How can control flow make every path, boundary, and loop invariant visible enough to test and review?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 3 — Ownership, Moves, Copying, and Destruction

**Governing question:** Who owns each resource after every assignment, call, return, destructure, and scope exit?

### Morning: derive the model

Read [Module 3](module-03-ownership-moves-copying-and-destruction/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-03-ownership-moves-copying-and-destruction/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 3 — Ownership Intake Pipeline](../labs/module-03-ownership-intake/README.md). Accept owned input, normalize it, move valid records into storage, and return rejected input in a typed result. Account for every owner after success and failure; clone only when the contract genuinely requires two independent values.

### Evening: integrate the course product

The course capstone is **Taskboard**, a persistent command-line task board. Move owned task titles into board storage and document the owner after each operation. Avoid cloning simply because a caller's postcondition was never stated. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Who owns each resource after every assignment, call, return, destructure, and scope exit?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 4 — Borrowing, References, Slices, and Strings

**Governing question:** Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?

### Morning: derive the model

Read [Module 4](module-04-borrowing-references-slices-and-strings/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-04-borrowing-references-slices-and-strings/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 4 — Borrowed Catalog](../labs/module-04-borrowed-catalog/README.md). Implement borrowed lookup, slice-based listing, and one narrow mutation path. Returned views must remain tied to the catalog, and read-only operations must not allocate merely to satisfy ownership.

### Evening: integrate the course product

The course capstone is **Taskboard**, a persistent command-line task board. Refactor read operations to borrow the board and updates to use one narrow mutable path. The signatures should make inspection, mutation, and ownership transfer visibly different. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Model shared and mutable references as permissions constrained by aliasing and validity;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 5 — Structs, Enums, Methods, and Pattern Matching

**Governing question:** How can the type system make valid states representable and contradictory states difficult or impossible to construct?

### Morning: derive the model

Read [Module 5](module-05-structs-enums-methods-and-pattern-matching/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-05-structs-enums-methods-and-pattern-matching/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 5 — Typed Workflow State Machine](../labs/module-05-state-machine/README.md). Build an independent package whose public API makes task identity, priority, status, and legal transitions explicit. The laboratory is not a reduced capstone copy; it is a focused proof that you can turn a state graph into a private, testable model.

### Evening: integrate the course product

The course capstone is **Taskboard**, a persistent command-line task board. Replace stringly records with `Task`, `TaskId`, `Priority`, `Status`, and `Command`. The state graph should make contradictory combinations unrepresentable. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“How can the type system make valid states representable and contradictory states difficult or impossible to construct?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 6 — Collections, Iterators, and Closures

**Governing question:** Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?

### Morning: derive the model

Read [Module 6](module-06-collections-iterators-and-closures/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-06-collections-iterators-and-closures/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 6 — In-Memory Task Board](../labs/module-06-in-memory-board/README.md). Build a typed, deterministic in-memory task board. This is the first lab where collection behavior, state-machine rules, and ownership design must work together.

### Evening: integrate the course product

The course capstone is **Taskboard**, a persistent command-line task board. Implement board operations, deterministic listing, filtering, search, and statistics. For each traversal, state whether it borrows, mutates, or consumes the collection. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 7 — Errors, Parsing, Files, and Persistence

**Governing question:** Which failures are part of the product contract, where are they detected, and what state is visible after failure?

### Morning: derive the model

Read [Module 7](module-07-errors-parsing-files-and-persistence/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-07-errors-parsing-files-and-persistence/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 7 — Versioned Record Codec](../labs/module-07-record-codec/README.md). Build a complete persistence boundary independent of `taskboard`. The lab proves that you can transfer the method to a new domain rather than reproduce capstone names.

### Evening: integrate the course product

The course capstone is **Taskboard**, a persistent command-line task board. Add typed command and storage errors, a versioned codec, transactional loading, and explicit save behavior. Invalid input must not partially mutate the board. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Which failures are part of the product contract, where are they detected, and what state is visible after failure?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 8 — Generics, Traits, Conversions, and Lifetime Basics

**Governing question:** What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?

### Morning: derive the model

Read [Module 8](module-08-generics-traits-conversions-and-lifetime-basics/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-08-generics-traits-conversions-and-lifetime-basics/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 8 — Trait and Lifetime Boundary](../labs/module-08-traits-and-lifetimes/README.md). Build a reusable but bounded report system. The lab tests whether you can distinguish justified genericity from abstraction for its own sake.

### Evening: integrate the course product

The course capstone is **Taskboard**, a persistent command-line task board. Use standard conversion traits and generic readers and writers where they remove real duplication. Add only the lifetime annotations required by returned borrowed data. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Write generic functions and types whose bounds correspond to operations actually performed;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 9 — Crates, Modules, Public APIs, Tests, and Documentation

**Governing question:** Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?

### Morning: derive the model

Read [Module 9](module-09-crates-modules-public-apis-tests-and-documentation/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-09-crates-modules-public-apis-tests-and-documentation/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 9 — Library Boundary Refactor](../labs/module-09-library-boundaries/README.md). Build a package with a reusable library and thin binary. The lab tests architecture, visibility, public documentation, and multi-level evidence.

### Evening: integrate the course product

The course capstone is **Taskboard**, a persistent command-line task board. Split reusable logic from the binary, minimize public visibility, and cover the contract with unit, integration, CLI, and documentation tests. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 10 — Integration and Independent Change

**Governing question:** Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?

### Morning: derive the model

Read [Module 10](module-10-integration-and-independent-change/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-10-integration-and-independent-change/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 10 — Inventory Ledger](../labs/module-10-inventory-ledger/README.md). Build a separate safe-Rust application from a behavioral specification only. Do not copy taskboard module names blindly. The lab is the final transfer test.

### Evening: integrate the course product

The course capstone is **Taskboard**, a persistent command-line task board. Implement an independently selected cross-layer feature and defend the entire path from domain invariant to exit status. This is the transfer proof for Course 1. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;


## Mid-course reconstruction

After Day 5, rebuild the five-module dependency chain without notes. Select the two compiler specimens that changed your model most, rerun them, and explain why the wrong prediction was plausible. Repair every incomplete lab before opening Day 6; later mechanisms assume that the earlier contract is stable.

## Final consolidation

After Day 10, use the [course reference](reference.md) to compress the material, not to relearn it. Complete the [final review](final-review.md) from an empty directory. Then defend Taskboard by tracing one successful operation and one adversarial failure through every layer touched by the course.
