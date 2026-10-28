# Laboratory 56 — Panic-Safe Batch Builder

This is the independent product for **Course 6, Module 56: Raw Pointers, Provenance, and Uninitialized Memory**. Read the [module chapter](../../course-book/module-56-raw-pointers-provenance-and-uninitialized-memory/index.md) and complete its [workbook](../../course-book/module-56-raw-pointers-provenance-and-uninitialized-memory/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a fixed-size array through `MaybeUninit` while an element constructor can return an error or panic. The product must drop exactly the initialized prefix and never treat the suffix as live values.

## Why this laboratory exists

This lab focuses on the interval between allocation and full initialization, where the type system cannot yet treat the buffer as `[T]`. A guard must know exactly how many elements are live and destroy that prefix if construction returns or unwinds early. The finished owner may exist only after every slot has been initialized.

## Contract

`try_build_array::<T,E,N>` calls a closure once for each index in order. On success it returns `[T; N]`. On error it returns the original error and drops every previously constructed element exactly once. Panic follows the same cleanup path through an initialized-prefix guard.

## Required milestones

1. Write the initialized-prefix invariant before code.
2. Create `[MaybeUninit<T>; N]` without first constructing invalid `T` values.
3. Update the count only after a successful slot write.
4. Implement a guard that drops only the live prefix.
5. Transfer ownership into the final array without running guard cleanup.

## Adversarial cases

- error at index zero
- error after several successful values
- success for N=0
- success for non-Copy values
- panic after several values using `catch_unwind` in the test
- drop counters prove exact cleanup

## Evidence to produce

- a state invariant relating capacity, initialized prefix, and next write position;
- a drop-counting element that records exactly-once destruction;
- panic injection at every construction index;
- tests for zero length, complete success, ordinary error, and unwind cleanup;
- a proof that `Vec::set_len` or slice construction occurs only after full initialization.

## Prohibited shortcuts

Do not set the final length before initialization completes, read a `MaybeUninit<T>` slot early, assume the element constructor cannot panic, use `mem::forget` to avoid cleanup reasoning, catch a panic and call the design sound, or run destructors over uninitialized storage. The guard's initialized count is the authority for cleanup.

## Transfer

Use the same prefix invariant for an FFI function that writes up to a capacity and reports an initialized count. Explain which count values must be rejected.

## Comparing with the reference

Compare the two state machines at each write and each exit. Verify that ownership of initialized elements transfers exactly once to the finished collection and that the guard becomes inert only after transfer. A passing success test is weak evidence; the decisive comparison is destructor counts for every injected panic index.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the contract, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer this question without the chapter:

> How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
