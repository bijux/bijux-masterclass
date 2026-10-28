# Laboratory 57 — Aligned Byte Buffer

**Course 6 · Module 57: Manual Allocation and Owning Unsafe Abstractions**

[Chapter](../../course-book/module-57-manual-allocation-and-owning-unsafe-abstractions/index.md) · [Workbook](../../course-book/module-57-manual-allocation-and-owning-unsafe-abstractions/workbook.md) · [FrameVault guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Manual Allocation and Owning Unsafe Abstractions**: How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state? The product must make **Construct and validate `Layout` values without unchecked size arithmetic** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **allocator layout record** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a fixed-length, zero-initialized byte owner using the global allocator. The public API is safe; the implementation owns one exact allocation layout and exposes only slices tied to ordinary borrows.

## Product-specific design pressure

This lab turns the allocator's raw pointer and layout pair into one ordinary owner. It teaches that allocation identity, length, requested alignment, initialization, slice access, movement, and deallocation are one invariant—not independent conveniences. Empty values are modeled without calling the allocator while retaining their validated alignment metadata.

## Contract

`AlignedBytes::new_zeroed(length, alignment)` accepts power-of-two alignment through `Layout`. Empty values own no allocation. Nonempty values own exactly one allocation and deallocate it with the stored layout. The type does not grow, clone raw ownership, cast bytes to typed values, or add manual `Send`/`Sync`.

## Required milestones

1. Write the two-state invariant: empty/no allocation and nonempty/one allocation.
2. Validate layout before allocation and treat null as failure.
3. Expose `as_slice` and `as_mut_slice` with borrow-tied lifetimes.
4. Deallocate exactly once through `Drop`.
5. Prove requested alignment through the pointer address in tests.

## Adversarial cases

- zero length with valid alignment
- invalid non-power-of-two alignment
- one byte
- large but bounded length
- mutation through slice
- move of owner
- drop after read error in helper

## Evidence to produce

- a two-state invariant for empty and allocated values;
- tests for zeroed bytes, mutation, non-power-of-two rejection, zero length, and requested alignment;
- proof that null allocation becomes an error before constructing the owner;
- proof that every deallocation uses the exact stored layout;
- a table showing why each slice borrow prevents conflicting safe access.

## Prohibited shortcuts

Do not expose an owning raw pointer, deallocate with a recomputed or different layout, call the global allocator with a zero-size request, create a typed slice from arbitrary bytes, manually assert `Send` or `Sync`, clone raw ownership, or use `Vec<u8>` as a way to avoid the allocation exercise. Keep the unsafe surface private and minimal.

## Transfer

Adapt the owner to a foreign API that fills bytes and reports `written`. Decide whether zero initialization or an initialized-length field gives the smaller proof.

## Comparing with the reference

Compare constructors, zero states, and destructors before comparing method names. Confirm that requested alignment remains observable for empty values, nonempty pointers satisfy it, slices are tied to owner borrows, and no move duplicates ownership. Re-derive the `Drop` proof without reading its SAFETY comment.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the contract, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer this question without the chapter:

For **Laboratory 57 — Aligned Byte Buffer**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Aligned Byte Buffer**.
2. Draw the smallest **allocator layout record** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to FrameVault so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Construct and validate `Layout` values without unchecked size arithmetic.
- Distinguish allocation capacity from initialized logical length.
- Handle zero-length allocations without passing an invalid layout to the allocator.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 57 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **allocator layout record**. Defend why your design is simpler than one plausible alternative under the new requirements.
