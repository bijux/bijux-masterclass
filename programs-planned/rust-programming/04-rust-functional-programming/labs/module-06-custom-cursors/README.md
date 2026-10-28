# Laboratory 36 — Custom Cursors

**Course 4 · Module 36: Custom Iterators and Collection Protocols**

[Chapter](../../course-book/module-36-custom-iterators-and-collection-protocols/index.md) · [Workbook](../../course-book/module-36-custom-iterators-and-collection-protocols/workbook.md) · [LedgerFlow guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Custom Iterators and Collection Protocols**: What laws must a custom traversal obey, and who owns the collection when iteration begins? The product must make **Implement a correct custom `Iterator` by defining state and exhaustion behavior** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **collection protocol map** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What laws must a custom traversal obey, and who owns the collection when iteration begins?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

The executable work is in `labs/module-06-custom-cursors/README.md`. This is a law laboratory: each implemented trait makes a promise stronger than “the examples passed.”

### Part A — `Fields<'a>` state machine

Represent only the unprocessed suffix. On each `next` call, consume one raw comma-delimited segment, trim it, skip empties, and either yield a borrowed slice or continue. Draw states for:

- untouched input;
- remaining suffix;
- trailing comma;
- all-empty input;
- permanent exhaustion.

The lower size hint is zero because remaining raw segments may all be empty. The upper bound may be remaining comma count plus one. Do not implement `ExactSizeIterator`.

### Part B — `EventLog` traversal ownership

Provide two deliberate `IntoIterator` implementations:

- owned `EventLog` yields owned `Event` values;
- `&EventLog` yields `&Event` values.

Do not expose mutable iteration because the future log invariant may require event order and identity to remain controlled. Show with tests that borrowed traversal leaves the log available and consuming traversal transfers its storage.

### Part C — collection protocols

`Diagnostics` supports both `FromIterator<String>` and `Extend<String>`. Explain why one creates a collection from a complete stream while the other grows existing state.

`UniqueIds` cannot lawfully implement ordinary `FromIterator<u64>` if duplicate rejection must be reported. Expose `try_from_iter` instead. Returning a partial collection on duplicate is not the contract.

### Part D — `Stride<I>`

Reject step zero at construction. The first `next` yields the source’s first item; later calls skip `step - 1` items and yield the next. Derive the size hint separately before and after the first call. Test exact iterators and an iterator with only an upper bound.

### Law matrix

Your evidence must cover:

| Law | Proof case |
|---|---|
| fused exhaustion | at least two `next` calls after `None` |
| order preservation | source order under all traversal modes |
| conservative size hint | actual remaining count always inside bounds |
| owned/borrowed distinction | source availability after traversal |
| duplicate failure | first duplicate and no panic |
| extension order | existing diagnostics followed by new items |

### Transfer

Build a separate front/back cursor over a slice and implement `DoubleEndedIterator`. Test mixed `next`/`next_back` sequences, odd and even lengths, crossing in the middle, and permanent exhaustion. Do not add `ExactSizeIterator` until the remaining count is actually exact.

### Defense

Every marker trait must be defended as a semantic promise. Explain why a truthful weak hint is better than a precise-looking lie, why mutable iteration is an API decision rather than a convenience, and why fallible collection needs a different constructor shape.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Custom Cursors**.
2. Draw the smallest **collection protocol map** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to LedgerFlow so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 36 — Custom Cursors**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Custom Cursors**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Implement a correct custom `Iterator` by defining state and exhaustion behavior.
- Provide owned, shared, and mutable `IntoIterator` implementations only where their semantics are useful.
- Implement `FromIterator` and `Extend` for a domain collection with explicit invariant policy.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 36 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **collection protocol map**. Defend why your design is simpler than one plausible alternative under the new requirements.
