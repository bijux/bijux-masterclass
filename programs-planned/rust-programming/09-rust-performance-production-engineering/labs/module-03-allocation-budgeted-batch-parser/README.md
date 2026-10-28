# Laboratory 83 — Allocation-Budgeted Batch Parser

**Course 9 · Module 83: Allocation, Memory Footprint, and Ownership Cost**

[Chapter](../../course-book/module-83-allocation-memory-footprint-and-ownership-cost/index.md) · [Workbook](../../course-book/module-83-allocation-memory-footprint-and-ownership-cost/workbook.md) · [MetricRail guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Allocation, Memory Footprint, and Ownership Cost**: Which bytes are owned, borrowed, reserved, retained, duplicated, or temporarily allocated, and which of those states actually dominate product cost? The product must make **Distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **allocation ledger** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a bounded tab-separated batch parser that borrows while validating and allocates only when a record becomes durable output. Each line is `key<TAB>signed-integer`. The public result owns compact keys; the intermediate `BorrowedRecord<'a>` proves that parsing itself does not need to allocate them.

The laboratory is not an exercise in deleting every allocation. The final `Record` deliberately owns its key so the input can be released. The goal is to place allocation at the correct lifetime boundary and make the batch’s memory envelope explicit.

## Limits and failure contract

`Limits` must bound total input bytes, record count, and key bytes. Validate total input size before scanning or reserving from attacker-controlled data. Determine record count before output allocation, reject a count over the limit, and reserve only that bounded count.

Each parse error must preserve the physical one-based line where relevant and distinguish:

- total input too large;
- too many records;
- wrong field count;
- invalid key;
- invalid integer.

Do not collapse every error into `&'static str`, panic on malformed input, or copy the whole bad line into the error.

## Construction route

1. Define the limits and error taxonomy first.
2. Implement `parse_borrowed(line, line_number, limits)` using slices into the input.
3. Check exactly two fields; reject empty/oversized/invalid keys under the stated grammar.
4. Parse the numeric field with checked `FromStr` behavior.
5. In `parse_batch`, reject total bytes and record count before allocating the result vector.
6. Parse lines in physical order and promote only `key` into an owned `String`.
7. Preserve deterministic output and causal line numbers.
8. Add tests for every boundary and failure category.

## Memory ledger

Document:

```text
input owner → line slice → key slice → owned key → output vector
```

For each step, record allocation, capacity, lifetime, and drop point. Explain why borrowing the output key would retain the complete input and why copying one validated key is the correct boundary.

Pre-counting lines adds a second traversal. That is acceptable for exact bounded reservation in this laboratory. Your report must state when a streaming parser or incremental growth would be preferable and what measurement would decide.

## Adversarial cases

Exercise zero records, one record without a final newline, exact byte/count/key limits, one above each limit, extra tabs, missing fields, blank keys, numeric overflow, malformed number, and an error on a late line after many valid lines. Failure must not return a partially accepted batch.

## Transfer

Extend the format with an optional bounded unit field. Keep the borrowed parser allocation-free and promote only durable fields. Update the memory budget and explain whether interning units is justified by repetition and bounded vocabulary.

## Completion

The laboratory is complete when limits are enforced before expensive commitment, the parser’s borrowed/owned boundary is explicit, failures preserve line context, the output can outlive the input, and tests cover exact boundaries rather than only ordinary examples.

Use `solution/` after your own implementation. Compare allocation placement, line accounting, and failure atomicity. A solution that allocates fewer objects but retains the full input is not superior.

## Memory evidence

Instrument the parser so the report distinguishes input bytes, temporary token storage, accepted owned fields, rejected-row diagnostics, vector capacity, and final retained records. Run at least three workloads: mostly valid short rows, mostly invalid rows with long messages, and valid rows containing near-limit fields. Record peak logical bytes and retained bytes after parsing completes. If allocator-level measurement is available, compare it with the internal accounting and explain what the counters omit.

Perform one ownership change at a time. For each change, state which allocation disappeared, which owner now keeps the data alive, and whether any backing buffer remains retained longer. The final design must not improve allocation count by allowing one small accepted field to retain an arbitrarily large input buffer.

## Failure-focused cases

Force the parser to encounter an overlong field after several valid rows, a malformed numeric field near the input limit, and many rejected rows whose diagnostics would otherwise retain large excerpts. Verify that accepted records remain valid, rejected data does not leak into retained storage, and diagnostic memory is itself bounded. Explain whether the parser offers all-or-nothing batch semantics or row-local acceptance, and ensure the memory accounting follows that declared policy.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Allocation-Budgeted Batch Parser**.
2. Draw the smallest **allocation ledger** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to MetricRail so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count.
- Trace ownership operations that allocate, clone, reallocate, promote, or retain data.
- Explain when borrowing reduces work and when it only complicates lifetimes without changing allocation.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 83 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **allocation ledger**. Defend why your design is simpler than one plausible alternative under the new requirements.
