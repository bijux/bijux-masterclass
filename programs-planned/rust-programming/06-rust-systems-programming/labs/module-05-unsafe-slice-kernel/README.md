# Laboratory 55 — Unsafe Slice Kernel

This is the independent product for **Course 6, Module 55: Unsafe Rust as a Proof Boundary**. Read the [module chapter](../../course-book/module-55-unsafe-rust-and-safety-proofs/index.md) and complete its [workbook](../../course-book/module-55-unsafe-rust-and-safety-proofs/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What additional obligation begins when the compiler can no longer prove a memory-safety condition, and how do you make that obligation small, local, and reviewable?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a safe API that returns two distinct mutable elements from one slice. First implement a safe reference version with `split_at_mut`, then implement a narrow raw-pointer kernel and prove that both expose the same behavior.

## Why this laboratory exists

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

> What additional obligation begins when the compiler can no longer prove a memory-safety condition, and how do you make that obligation small, local, and reviewable?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
