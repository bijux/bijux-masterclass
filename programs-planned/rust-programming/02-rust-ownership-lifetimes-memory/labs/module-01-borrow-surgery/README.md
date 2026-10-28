# Laboratory 11 — Borrow Surgery

This is the independent product for **Course 2, Module 11: Places, Move Paths, and Advanced Borrowing**. Read the [module chapter](../../course-book/module-11-places-move-paths-and-advanced-borrowing/index.md) and complete its [workbook](../../course-book/module-11-places-move-paths-and-advanced-borrowing/workbook.md) before consulting the reference implementation.

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

## Working route

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Borrow Surgery**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
