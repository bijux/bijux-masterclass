# Laboratory 3 — Lending Table

[Course 10](../../README.md) · [Common laboratory method](../../../START_HERE.md#laboratory-method)

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

### Completion standard

You can explain why the item cannot be named as one fixed associated type, why a fresh borrow is selected on every call, and where ownership should be introduced for retention. If callers can advance while a view is live, the core invariant is broken.
