# Laboratory 55 — Unsafe Slice Kernel

**Course 6 · Module 55: Unsafe Rust as a Proof Boundary**

[Chapter](../../course-book/module-55-unsafe-rust-and-safety-proofs/index.md) · [Workbook](../../course-book/module-55-unsafe-rust-and-safety-proofs/workbook.md) · [FrameVault guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Unsafe Rust as a Proof Boundary**: What additional obligation begins when the compiler can no longer prove a memory-safety condition, and how do you make that obligation small, local, and reviewable? The product must make **Name the operations Rust requires an unsafe context to perform** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **unsafe obligation ledger** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What additional obligation begins when the compiler can no longer prove a memory-safety condition, and how do you make that obligation small, local, and reviewable?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a safe API that returns two distinct mutable elements from one slice. First implement a safe reference version with `split_at_mut`, then implement a narrow raw-pointer kernel and prove that both expose the same behavior.

## Product-specific design pressure

This lab introduces unsafe code only after a complete safe behavioral specification exists. The kernel is small enough that every unchecked load can be mapped to a length, alignment, initialization, and aliasing fact. The design succeeds when ordinary callers cannot violate those facts through the safe wrapper, not when the unsafe loop merely passes sample tests.

## Contract

`pair_mut(slice, a, b)` returns `None` when either index is out of bounds or the indices are equal. Otherwise it returns two mutable references in the caller's requested order. All validation is safe. The unsafe block contains only pointer addition and dereference, with a complete safety argument.

## Required milestones

1. Write the safe reference implementation and its tests.
2. Draw the aliasing proof for both index orders.
3. Implement the raw kernel without one function-wide unsafe block.
4. Keep returned lifetimes tied to the input mutable borrow.
5. Use Clippy-compatible `SAFETY` comments at every block.

## Adversarial cases

- equal indices
- first index lower
- second index lower
- first out of bounds
- second out of bounds
- one-element and empty slices
- mutation through both returned references

## Evidence to produce

- a safe reference implementation used as the behavioral oracle;
- a safety ledger for every raw-pointer construction, offset, and dereference;
- equivalence tests across empty, short, odd-length, and maximum test inputs;
- proof that loop bounds imply each pointer offset remains in the allocation;
- a review of every safe public route that can reach the unsafe kernel.

## Prohibited shortcuts

Do not place the whole function in one unsafe block, accept raw pointers in the public safe API, use unchecked arithmetic without deriving its bound, extend a lifetime from a pointer, assume unsafe is automatically faster, or delete the safe oracle after the optimized form exists. Each unsafe operation needs its own local evidence.

## Transfer

Transfer the method to selecting three distinct mutable elements. Compare raw-pointer validation with repeated `split_at_mut` and choose the smaller proof.

## Comparing with the reference

Compare unsafe reachability and proof size. A reference solution with more lines may be superior if each operation has a smaller premise and the safe wrapper establishes it directly. Try breaking one precondition at a time and verify that the public API makes the bad state unrepresentable rather than merely undocumented.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the contract, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer this question without the chapter:

For **Laboratory 55 — Unsafe Slice Kernel**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Unsafe Slice Kernel**.
2. Draw the smallest **unsafe obligation ledger** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to FrameVault so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Name the operations Rust requires an unsafe context to perform.
- Distinguish compiler permission from semantic safety and undefined behavior.
- Write safety preconditions, internal invariants, and postconditions before an unsafe block.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 55 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **unsafe obligation ledger**. Defend why your design is simpler than one plausible alternative under the new requirements.
