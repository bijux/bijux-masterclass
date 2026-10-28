# Laboratory 93 — Lending Table

**Course 10 · Module 93: GATs, Higher-Ranked Bounds, and Lending Interfaces**

[Chapter](../../course-book/module-93-gats-higher-ranked-bounds-and-lending-interfaces/index.md) · [Workbook](../../course-book/module-93-gats-higher-ranked-bounds-and-lending-interfaces/workbook.md) · [AxiomStore guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **GATs, Higher-Ranked Bounds, and Lending Interfaces**: How can an API return views tied to each borrow of `self` without pretending that every yielded value has one fixed lifetime? The product must make **Distinguish one associated type from a lifetime-indexed family of associated types** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **lifetime family map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Replace the starter’s fully owned table with a cursor that lends one row view at a time from an input buffer. Each view must be tied to the mutable borrow used for the current `next` call. While that view exists, the cursor cannot advance. When the reader needs retention, an explicit owned conversion copies only the selected row or fields.

This is a lifetime-family laboratory, not a challenge to write the shortest parser. The central proof is that one method call chooses a fresh item lifetime and that no borrowed row can outlive either the cursor loan or its backing input.

### Public API

Define a lending trait with a generic associated type equivalent in responsibility to:

```rust
pub trait LendingCursor {
    type View<'a>
    where
        Self: 'a;

    fn next<'a>(&'a mut self) -> Option<Self::View<'a>>;
}
```

`RowView` should expose the raw row, borrowed fields, and an explicit `to_owned` conversion. The cursor must handle empty input, a final row without a newline, consecutive empty rows according to one documented policy, and exhaustion. Avoid allocating during ordinary borrowed traversal.

### Negative API evidence

Add compile-fail documentation or a dedicated specimen for both forbidden actions:

1. retain a row view and call `next` again on the same cursor;
2. return a row view after the cursor or source has been destroyed.

The failures must arise from the lending relationship. Manufacturing `'static` data, leaking the input, or cloning every row is not a repair.

### Borrow ledger

For two consecutive calls, draw the source lifetime, cursor lifetime, mutable-loan lifetime, row-view lifetime, and owned-conversion lifetime. Explain why the item family is indexed by the call’s loan rather than only by the original input lifetime. Include a case where the cursor could compact or replace internal storage on advance; this makes the non-overlap requirement operational rather than decorative.

### Transfer

Add `with_next`, a callback-based operation that exposes one temporary view under a higher-ranked bound. The callback may compute an owned result, but it may not return the borrowed view. Compare the ergonomics and constraints of the direct GAT method with the callback method.

### Using the reference

Build from `starter/` first. Once your negative API cases and edge rows are complete, compare with `solution/`. Focus on lifetime relationships, empty-row policy, and conversion boundaries. The reference is intentionally small; extend its tests rather than assuming its surface is exhaustive.

### Mechanism-specific completion standard

You can explain why the item cannot be named as one fixed associated type, why a fresh borrow is selected on every call, and where ownership should be introduced for retention. If callers can advance while a view is live, the core invariant is broken.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Lending Table**.
2. Draw the smallest **lifetime family map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to AxiomStore so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Whole-laboratory completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish one associated type from a lifetime-indexed family of associated types.
- Design a lending cursor whose returned view cannot outlive the borrow that produced it.
- Read `for<'a>` as universal quantification chosen by the caller rather than a long concrete lifetime.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 93 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **lifetime family map**. Defend why your design is simpler than one plausible alternative under the new requirements.
