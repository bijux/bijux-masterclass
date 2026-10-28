# Laboratory 3 — Ownership Intake Pipeline

This is the independent product for **Course 1, Module 3: Ownership, Moves, Copying, and Destruction**. Read the [module chapter](../../course-book/module-03-ownership-moves-copying-and-destruction/index.md) and complete its [workbook](../../course-book/module-03-ownership-moves-copying-and-destruction/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Who owns each resource after every assignment, call, return, destructure, and scope exit?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

### Product contract

Use:

```rust
pub type Record = (u64, String);
```

Implement:

```rust
pub fn normalize_title(title: String) -> String;
pub fn insert(records: Vec<Record>, id: u64, title: String) -> Vec<Record>;
pub fn transfer(
    pending: Vec<Record>,
    completed: Vec<Record>,
    id: u64,
) -> (Vec<Record>, Vec<Record>, bool);
pub fn retain_with_audit(record: Record) -> (Record, String);
```

### Requirements

- normalization trims/collapses whitespace and returns one owned title;
- insertion moves normalized title into a record and vector;
- transfer moves one record between vectors without cloning;
- failed transfer returns both collections unchanged;
- `retain_with_audit` returns the original record and an independently owned audit message;
- every clone in tests/reference data is classified; production implementation should need none in the first three operations.

### Ownership defense

For each function, submit an ownership ledger. For `transfer`, trace:

```text
pending vector -> parameter -> mutable local
record element -> remove return -> local record -> completed element
completed vector -> parameter -> mutable local -> returned tuple field
```

### Test requirements

- normalization consumes original and produces expected title;
- insertion preserves prior records and appends one;
- successful transfer preserves record ID/title exactly;
- failed transfer preserves values/order;
- audit output and retained record both survive return;
- no duplicate record appears after transfer.

### Why `retain_with_audit` is not a clone exercise

The audit message is not a second raw title owner; it is a new formatted product value. `format!` reads fields and creates a distinct message while the record remains owned for return. This demonstrates independent output without cloning the record.

### Proof

Run full format/check/clippy/test. Then search production source for `.clone()` and explain every match.

Reference: `labs/module-03-ownership-intake/solution/`.

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

> Who owns each resource after every assignment, call, return, destructure, and scope exit?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Ownership Intake Pipeline**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
