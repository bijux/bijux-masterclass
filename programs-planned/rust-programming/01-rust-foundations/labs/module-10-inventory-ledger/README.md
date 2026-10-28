# Laboratory 10 — Inventory Ledger

**Course 1 · Module 10: Integration and Independent Change**

[Chapter](../../course-book/module-10-integration-and-independent-change/index.md) · [Workbook](../../course-book/module-10-integration-and-independent-change/workbook.md) · [Taskboard guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Integration and Independent Change**: Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression? The product must make **Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **whole-program invariant map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

### Purpose

Build a separate safe-Rust application from a behavioral specification only. Do not copy taskboard module names blindly. The lab is the final transfer test.

A local lending ledger tracks items and loans:

```text
ledger add-item "The Rust Book"
ledger register "Mina"
ledger lend <item-id> <member-id>
ledger return <item-id>
ledger list available
ledger list loaned
ledger member <member-id>
ledger stats
```

### Required domain rules

- item and member IDs are positive newtypes and unique in their collections;
- names/titles are trimmed, bounded, and delimiter-safe;
- an item is either available or loaned to exactly one member;
- only available items can be lent;
- only loaned items can be returned;
- member views list loans in item-ID order;
- all public reports are deterministic;
- ID allocation detects exhaustion;
- invalid operations preserve state.

### Persistence

Design one versioned text format with explicit grammar. It must store members, items, loan state, and next-ID metadata. The loader validates cross-record references: every loaned member ID must exist. Construct complete temporary state before returning a ledger.

Saving uses a same-directory temporary file and canonical ordering. Document the exact durability boundary.

### Architecture

Choose modules from responsibilities. A likely shape includes domain, command, storage, application, and binary, but combining domain files or separating member/item logic may be better. Submit a dependency graph before code.

### Independent extension

After the base proof passes, add one feature selected from:

- remove member only when no active loans;
- search item titles;
- rename member;
- list overdue items using an injected date value rather than hidden current time.

Write behavior and impact matrices before implementation.

### Acceptance defense

Explain:

- ownership of names, titles, and report views;
- why loan state is modeled as it is;
- how cross-record validation works;
- failure state at every save stage;
- generic I/O bounds;
- lifetime annotations, if any;
- public API inventory;
- complexity of list/search/stats;
- evidence limitations.

The lab fails if it uses string statuses, public mutable fields, panic-based input parsing, partial-load mutation, non-deterministic output, or an untested storage grammar.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Inventory Ledger**.
2. Draw the smallest **whole-program invariant map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Taskboard so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 10 — Inventory Ledger**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Inventory Ledger**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation.
- Preserve failure atomicity, deterministic behavior, and public invariants while refactoring across architectural layers.
- Review unfamiliar Rust for ownership workarounds, swallowed errors, invalid-state models, and missing evidence.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 10 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **whole-program invariant map**. Defend why your design is simpler than one plausible alternative under the new requirements.
