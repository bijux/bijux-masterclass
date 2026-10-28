# Course 1 Study Plan — Rust Foundations

Ten dense study days fit into two calendar weeks. The goal is not to maximize reading time; it is to make **How do Rust’s types, ownership rules, state models, and error boundaries combine into a complete program you can explain end to end?** answerable through construction and explanation.

## Daily rhythm

Use a **whole-program invariant map** across the course. Each day begins by reconstructing yesterday’s decisive relationship and ends by tracing one capstone invariant. Preserve the first prediction, the observed result, the principled repair, and the shortcut you rejected.

## Day 1 — Module 1: Compilation, Expressions, and Types

**Question:** How does Rust turn source text into a typed program, and what type and value does every expression produce?

**Retrieval:** Reconstruct the program entry model. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 1](./module-01-compilation-expressions-and-types/index.md) with a **type trace** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-01-compilation-expressions-and-types/workbook.md) before observation. The day’s minimum result is: **Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Measurement Report](../labs/module-01-measurement-report/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 1 in the [Taskboard guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”.** End with one simpler design that would be preferable under a narrower requirement.

## Day 2 — Module 2: Control Flow, Functions, and Invariants

**Question:** How can control flow make every path, boundary, and loop invariant visible enough to test and review?

**Retrieval:** Without notes, restate the invariant carried from Module 1 — Compilation, Expressions, and Types. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 2](./module-02-control-flow-functions-and-invariants/index.md) with a **control-flow table** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-02-control-flow-functions-and-invariants/workbook.md) before observation. The day’s minimum result is: **Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Control-Flow Policy Engine](../labs/module-02-control-flow-policy/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 2 in the [Taskboard guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior.** End with one simpler design that would be preferable under a narrower requirement.

## Day 3 — Module 3: Ownership, Moves, Copying, and Destruction

**Question:** Who owns each resource after every assignment, call, return, destructure, and scope exit?

**Retrieval:** Without notes, restate the invariant carried from Module 2 — Control Flow, Functions, and Invariants. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 3](./module-03-ownership-moves-copying-and-destruction/index.md) with a **ownership ledger** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-03-ownership-moves-copying-and-destruction/workbook.md) before observation. The day’s minimum result is: **Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Ownership Intake Pipeline](../labs/module-03-ownership-intake/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 3 in the [Taskboard guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger.** End with one simpler design that would be preferable under a narrower requirement.

## Day 4 — Module 4: Borrowing, References, Slices, and Strings

**Question:** Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?

**Retrieval:** Without notes, restate the invariant carried from Module 3 — Ownership, Moves, Copying, and Destruction. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 4](./module-04-borrowing-references-slices-and-strings/index.md) with a **borrow map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-04-borrowing-references-slices-and-strings/workbook.md) before observation. The day’s minimum result is: **Model shared and mutable references as permissions constrained by aliasing and validity.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Borrowed Catalog](../labs/module-04-borrowed-catalog/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 4 in the [Taskboard guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Model shared and mutable references as permissions constrained by aliasing and validity.** End with one simpler design that would be preferable under a narrower requirement.

## Day 5 — Module 5: Structs, Enums, Methods, and Pattern Matching

**Question:** How can the type system make valid states representable and contradictory states difficult or impossible to construct?

**Retrieval:** Without notes, restate the invariant carried from Module 4 — Borrowing, References, Slices, and Strings. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 5](./module-05-structs-enums-methods-and-pattern-matching/index.md) with a **state model** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-05-structs-enums-methods-and-pattern-matching/workbook.md) before observation. The day’s minimum result is: **Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Typed Workflow State Machine](../labs/module-05-state-machine/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 5 in the [Taskboard guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity.** End with one simpler design that would be preferable under a narrower requirement.

## Midpoint reconstruction

Do not add a sixth topic on the recovery day. Reconstruct **Compilation, Expressions, and Types, Control Flow, Functions, and Invariants, Ownership, Moves, Copying, and Destruction, Borrowing, References, Slices, and Strings, Structs, Enums, Methods, and Pattern Matching** as one dependency chain, rerun the two investigations that changed your model most, and describe the current Taskboard state from an empty page. Repair incomplete work, then take a real break; consolidation is part of the course rather than unused time.

## Day 6 — Module 6: Collections, Iterators, and Closures

**Question:** Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?

**Retrieval:** Without notes, restate the invariant carried from Module 5 — Structs, Enums, Methods, and Pattern Matching. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 6](./module-06-collections-iterators-and-closures/index.md) with a **collection and iteration trace** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-06-collections-iterators-and-closures/workbook.md) before observation. The day’s minimum result is: **Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions.** Keep one positive case and one causal negative case.

**Laboratory:** Build [In-Memory Task Board](../labs/module-06-in-memory-board/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 6 in the [Taskboard guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions.** End with one simpler design that would be preferable under a narrower requirement.

## Day 7 — Module 7: Errors, Parsing, Files, and Persistence

**Question:** Which failures are part of the product contract, where are they detected, and what state is visible after failure?

**Retrieval:** Without notes, restate the invariant carried from Module 6 — Collections, Iterators, and Closures. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 7](./module-07-errors-parsing-files-and-persistence/index.md) with a **error map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-07-errors-parsing-files-and-persistence/workbook.md) before observation. The day’s minimum result is: **Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Versioned Record Codec](../labs/module-07-record-codec/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 7 in the [Taskboard guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values.** End with one simpler design that would be preferable under a narrower requirement.

## Day 8 — Module 8: Generics, Traits, Conversions, and Lifetime Basics

**Question:** What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?

**Retrieval:** Without notes, restate the invariant carried from Module 7 — Errors, Parsing, Files, and Persistence. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 8](./module-08-generics-traits-conversions-and-lifetime-basics/index.md) with a **trait and lifetime contract** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-08-generics-traits-conversions-and-lifetime-basics/workbook.md) before observation. The day’s minimum result is: **Write generic functions and types whose bounds correspond to operations actually performed.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Trait and Lifetime Boundary](../labs/module-08-traits-and-lifetimes/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 8 in the [Taskboard guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Write generic functions and types whose bounds correspond to operations actually performed.** End with one simpler design that would be preferable under a narrower requirement.

## Day 9 — Module 9: Crates, Modules, Public APIs, Tests, and Documentation

**Question:** Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?

**Retrieval:** Without notes, restate the invariant carried from Module 8 — Generics, Traits, Conversions, and Lifetime Basics. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 9](./module-09-crates-modules-public-apis-tests-and-documentation/index.md) with a **module and API map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-09-crates-modules-public-apis-tests-and-documentation/workbook.md) before observation. The day’s minimum result is: **Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Library Boundary Refactor](../labs/module-09-library-boundaries/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 9 in the [Taskboard guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type.** End with one simpler design that would be preferable under a narrower requirement.

## Day 10 — Module 10: Integration and Independent Change

**Question:** Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?

**Retrieval:** Without notes, restate the invariant carried from Module 9 — Crates, Modules, Public APIs, Tests, and Documentation. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 10](./module-10-integration-and-independent-change/index.md) with a **whole-program invariant map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-10-integration-and-independent-change/workbook.md) before observation. The day’s minimum result is: **Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Inventory Ledger](../labs/module-10-inventory-ledger/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 10 in the [Taskboard guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation.** End with one simpler design that would be preferable under a narrower requirement.

## Final integration

After Day 10, complete the [final review](final-review.md), run the strongest available course route, and implement this unseen capstone change: **Add one cross-layer Taskboard feature—such as due dates or labels—without weakening deterministic storage, typed transitions, or failure atomicity.**

Seven days later, rebuild the ten-module sequence and the core **whole-program invariant map** without the book. Write a fresh example for every relationship you cannot recover. Re-reading a solution without recreating the model does not count as retained learning.
