# Laboratory 4 — Borrowed Catalog

**Course 1 · Module 4: Borrowing, References, Slices, and Strings**

[Chapter](../../course-book/module-04-borrowing-references-slices-and-strings/index.md) · [Workbook](../../course-book/module-04-borrowing-references-slices-and-strings/workbook.md) · [Taskboard guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Borrowing, References, Slices, and Strings**: Which temporary permissions does an operation require, and how narrowly can those permissions be scoped? The product must make **Model shared and mutable references as permissions constrained by aliasing and validity** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **borrow map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

### Product contract

Use:

```rust
pub type Record = (u64, String);
```

Implement:

```rust
pub fn find(records: &[Record], id: u64) -> Option<&Record>;
pub fn rename(records: &mut [Record], id: u64, replacement: &str) -> bool;
pub fn first_word(title: &str) -> &str;
pub fn matching_titles<'a>(records: &'a [Record], query: &str) -> Vec<&'a str>;
pub fn total_title_bytes(records: &[Record]) -> usize;
```

The explicit lifetime in `matching_titles` is supplied; Module 8 explains why output is tied to `records` rather than `query`.

### Constraints

- no `.clone()` in production code;
- no `&String` parameters;
- no `&Vec<Record>` parameters;
- listing/searching does not consume the collection;
- renaming performs one mutable search and changes one record;
- returned title slices borrow record strings;
- byte total is explicitly bytes, not characters;
- tests include multibyte UTF-8 text.

### Borrow defense

For each function, state:

- owner of records/titles;
- shared or exclusive access;
- whether result is owned or borrowed;
- final use that ends each borrow;
- caller operations blocked while returned references remain used.

### Adversarial test

Attempt this in a separate specimen:

```rust
let matches = matching_titles(&records, "parser");
rename(&mut records, 1, "decoder");
println!("{matches:?}");
```

Predict the failure. Then reorder use so mutation becomes valid.

### Proof

Run full format/check/clippy/test and a source search for `.clone()`.

Reference: `labs/module-04-borrowed-catalog/solution/`.

## Design record

Before implementation, complete this record for **Borrowed Catalog**:

| Question | Required answer |
|---|---|
| Module decision | How does **Borrowing, References, Slices, and Strings** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **borrow map** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Borrowed Catalog**.
2. Draw the smallest **borrow map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Taskboard so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 4 — Borrowed Catalog**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Borrowed Catalog**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Model shared and mutable references as permissions constrained by aliasing and validity.
- Shorten borrow scopes, reborrow correctly, and split disjoint data instead of cloning or over-owning.
- Design slice-based APIs and distinguish String, str, &String, and &str by ownership and representation.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 4 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **borrow map**. Defend why your design is simpler than one plausible alternative under the new requirements.
