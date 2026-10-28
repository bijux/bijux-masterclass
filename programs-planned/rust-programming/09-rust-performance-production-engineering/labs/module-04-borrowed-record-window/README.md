# Laboratory 4 — Borrowed Record Window

[Common laboratory method](../../../START_HERE.md#laboratory-method) · [Module 84 chapter](../../course-book/module-84-data-movement-buffering-and-zero-copy-boundaries/index.md)

## Product

Build a `RecordWindow` that owns one immutable `bytes::Bytes` allocation and records validated ranges for tab-separated records. Borrowed access returns `BorrowedRecord<'_>` views into the window. Promotion creates an `OwnedRecord` that remains valid after the window drops.

This product makes a narrow zero-copy claim: after the `Bytes` frame exists, inspecting record keys does not copy their payload bytes. It does **not** claim zero copies across sockets, allocation, or durable storage.

## Format and invariants

Each nonempty line contains `key<TAB>signed-integer`. The window must:

- enforce a configured nonzero maximum line length;
- validate line boundaries and field count at construction;
- store ranges that always lie within the backing bytes;
- preserve source order;
- return no reference that outlives `&self`;
- expose `len`, `is_empty`, borrowed lookup/iteration, and selective promotion;
- avoid retaining a giant backing allocation after promotion.

Range arithmetic must use checked logic. UTF-8 is part of the format contract for keys; malformed input receives a typed `WindowError` rather than a panic.

## Construction route

1. Parse the backing bytes once and collect validated byte ranges, not copied strings.
2. Decide whether line endings include `\r\n` and implement the choice consistently.
3. Store enough range metadata to reconstruct key and numeric slices safely.
4. Make borrowed access derive directly from `&self`, so Rust enforces the lifetime.
5. Implement promotion by copying only the compact key and numeric value.
6. Add a test that drops the window and continues using the promoted record.
7. Document that `Bytes::slice` or stored ranges may retain the complete backing frame while the window lives.

## Byte and lifetime ledger

Draw:

```text
Bytes owner
  ├── range metadata (owned, small)
  ├── BorrowedRecord<'window> (temporary views)
  └── OwnedRecord (independent compact allocation)
```

Explain why sending a borrowed record to a `'static` task is invalid, and compare two repairs: move/clone the entire `Bytes` frame versus promote only one record. The better choice depends on how much of the frame is needed and for how long.

## Adversarial cases

Test empty input, one line, final line without newline, exact maximum length, one byte above, empty key, extra field, invalid integer, invalid UTF-8, and many small records in one frame. Verify that an error does not expose unchecked partial ranges.

## Transfer

Add a method that promotes only records matching a predicate. Measure visible promoted bytes and retained backing bytes for three strategies: borrowed views, `Bytes` slices, and compact owned records. Explain the crossover.

## Completion

The laboratory is complete when construction validates all stored ranges, borrowed records are lifetime-correct, promotion breaks backing-store retention, and the zero-copy claim names its exact endpoints.

Inspect `solution/` after completing the range model. Compare invariants and lifetime boundaries rather than copying range representation. A parser that returns `String`s for every field may be safe but does not satisfy this product’s learning contract.

## Byte-lifetime ledger

For every public operation, draw the relation among the source buffer, cursor, borrowed record window, decoded fields, and caller. Mark which mutation invalidates which view. Include the empty buffer, a field split across chunks, a record at the maximum allowed length, multiple records in one buffer, and compaction after earlier records have been consumed. The ledger must explain why no returned view can outlive or overlap an incompatible mutation of the source.

Compare two implementations: borrowing fields directly and copying fields into owned records. Measure or count copies, but also report retained backing capacity and API restrictions. Conclude with the workload conditions under which each design is preferable. The laboratory is not complete if “zero copy” is used without naming the precise boundary and retention cost.

## Mutation and compaction proof

Add a test in which a caller holds a borrowed window while attempting to advance or compact the source. The public API should make the incompatible mutation impossible rather than relying on a warning in documentation. After the view ends, compact the consumed prefix and prove that subsequent offsets and records remain correct. Also test that an incomplete trailing record stays buffered without being exposed as complete or copied prematurely.

## Completion question

Can a caller point to the exact operation that ends every borrowed view, and can the implementation explain every remaining copy? Answer with the public signatures and one concrete buffer-state trace. If either answer depends on caller discipline that the types do not enforce, revise the API before treating the laboratory as complete.

