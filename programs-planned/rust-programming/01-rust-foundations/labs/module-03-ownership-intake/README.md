# Laboratory 3 — Ownership Intake Pipeline

**Course 1 · Module 3: Ownership, Moves, Copying, and Destruction**

[Chapter](../../course-book/module-03-ownership-moves-copying-and-destruction/index.md) · [Workbook](../../course-book/module-03-ownership-moves-copying-and-destruction/workbook.md) · [Taskboard guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Ownership, Moves, Copying, and Destruction**: Who owns each resource after every assignment, call, return, destructure, and scope exit? The product must make **Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **ownership ledger** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

## Design record

Before implementation, complete this record for **Ownership Intake Pipeline**:

| Question | Required answer |
|---|---|
| Module decision | How does **Ownership, Moves, Copying, and Destruction** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **ownership ledger** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Ownership Intake Pipeline**.
2. Draw the smallest **ownership ledger** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Taskboard so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 3 — Ownership Intake Pipeline**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Ownership Intake Pipeline**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger.
- Distinguish semantic moves, Copy duplication, explicit Clone cost, and destruction without relying on stack-versus-heap folklore.
- Predict partial moves and the remaining usable fields of an aggregate.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 3 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **ownership ledger**. Defend why your design is simpler than one plausible alternative under the new requirements.
