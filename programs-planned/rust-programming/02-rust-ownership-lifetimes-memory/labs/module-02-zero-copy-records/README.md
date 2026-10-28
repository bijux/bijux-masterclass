# Laboratory 12 — Zero-Copy Records

**Course 2 · Module 12: Lifetime Relationships and Borrowed APIs**

[Chapter](../../course-book/module-12-lifetime-relationships-and-borrowed-apis/index.md) · [Workbook](../../course-book/module-12-lifetime-relationships-and-borrowed-apis/workbook.md) · [Memory Workspace guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Lifetime Relationships and Borrowed APIs**: What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent? The product must make **Translate lifetime syntax into constraints among borrows rather than durations attached to values** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **lifetime constraint graph** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Implement `labs/module-02-zero-copy-records/starter`.

Parse a line-oriented metadata block without allocating key or value strings when input is already valid.

Input:

```text
name: Ada
language: Rust
role: systems engineer
```

### Public types

```rust
pub struct Field<'source> { /* key/value slices */ }
pub struct Record<'source> { /* source plus fields */ }
pub enum ParseError { /* line, reason */ }
```

### Contract

- the record and every field borrow from caller-owned source;
- blank lines are ignored;
- keys and values are trimmed by slicing, not allocation;
- empty keys are rejected with one-based line number;
- duplicate keys are rejected;
- `get` returns a value tied to the record/source;
- `into_fields` may consume the record while preserving source-lifetime slices;
- `to_owned` produces an independent owned representation;
- no reference may derive from a local normalized buffer.

### Required lifetime work

Implement at least one method where receiver elision is sufficient and one consuming method returning `'source`. Document the difference.

### Adversarial tests

- source dropped before attempted record use must be a compile-fail example in docs;
- Unicode input;
- leading/trailing whitespace;
- duplicate after trimming;
- empty and whitespace-only lines;
- owned conversion remains usable after source destruction.

## Design record

Before implementation, complete this record for **Zero-Copy Records**:

| Question | Required answer |
|---|---|
| Module decision | How does **Lifetime Relationships and Borrowed APIs** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **lifetime constraint graph** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Zero-Copy Records**.
2. Draw the smallest **lifetime constraint graph** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Memory Workspace so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 12 — Zero-Copy Records**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Zero-Copy Records**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Translate lifetime syntax into constraints among borrows rather than durations attached to values.
- Derive elision and explicit relationships for one-source and multiple-source APIs.
- Use lifetime shortening and subtyping in ordinary covariant borrowed views without extending provenance.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 12 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **lifetime constraint graph**. Defend why your design is simpler than one plausible alternative under the new requirements.
