# Laboratory 11 — Borrow Surgery

**Course 2 · Module 11: Places, Move Paths, and Advanced Borrowing**

[Chapter](../../course-book/module-11-places-move-paths-and-advanced-borrowing/index.md) · [Workbook](../../course-book/module-11-places-move-paths-and-advanced-borrowing/workbook.md) · [Memory Workspace guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Places, Move Paths, and Advanced Borrowing**: Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely? The product must make **Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **place and move-path map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Implement the package in `labs/module-01-borrow-surgery/starter` without reading the solution.

A small portfolio holds positions in an ordered slice. The library must rebalance quantity between two distinct positions while preserving total quantity and all unrelated metadata.

### Public surface

```rust
pub struct Position { /* private */ }
pub struct RebalanceReceipt { /* private */ }
pub enum RebalanceError { /* ... */ }

pub fn rebalance(
    positions: &mut [Position],
    from: usize,
    to: usize,
    quantity: u64,
) -> Result<RebalanceReceipt, RebalanceError>;
```

Constructors and read-only accessors are required for testing.

### Contract

- indices must be distinct and in range;
- quantity must be nonzero;
- source must contain enough quantity;
- target addition must not overflow;
- every expected failure leaves every position unchanged;
- success changes only the two quantities;
- total quantity is preserved;
- returned receipt owns the symbols and resulting quantities needed after borrows end;
- no `Position` clone is permitted;
- the function accepts a slice, not a vector.

### Required technique

Use a safe helper that obtains two disjoint mutable references with `split_at_mut`. Validation must occur before mutation.

### Tests

At minimum:

- forward and reverse index order;
- same index;
- source and target out of range independently;
- zero quantity;
- insufficient source;
- target overflow;
- preservation after every error;
- total preservation over a matrix of small values;
- metadata unchanged.

### Design note
Submit a place/loan trace and explain why neither cloning nor `Rc<RefCell<Position>>` is justified.

## Design record

Before implementation, complete this record for **Borrow Surgery**:

| Question | Required answer |
|---|---|
| Module decision | How does **Places, Move Paths, and Advanced Borrowing** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **place and move-path map** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Borrow Surgery**.
2. Draw the smallest **place and move-path map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Memory Workspace so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 11 — Borrow Surgery**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Borrow Surgery**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations.
- Model loans over places and explain when fields, indices, slices, and method receivers can or cannot be borrowed disjointly.
- Use reborrowing, non-lexical lifetime shortening, two-phase borrowing, and split APIs without relying on folklore.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 11 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **place and move-path map**. Defend why your design is simpler than one plausible alternative under the new requirements.
