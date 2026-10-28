# Workbook — Module 56: Raw Pointers, Provenance, and Uninitialized Memory

[Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether the chapter has become an operational model. Freeze answers before compiling or reading the reference implementation. A correct result without the governing reason is incomplete.

## Part 1 — Predict

### Prediction 1

A raw pointer is copied after its allocation is freed. Is copying itself the dereference error?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

`&packed.field as *const _` is used on an unaligned field. What can already be wrong?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

A byte pointer is cast to `*const u32`. Which obligations remain?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

`ptr::read` extracts a `String`, then the original location is dropped normally. What happens?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

`ptr::write` overwrites an initialized `String`. What happens to the old value?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

`MaybeUninit<bool>` is uninitialized. May it be read as `bool`?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

`NonNull<T>` is present. Does it prove one live `T` exists?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

A raw slice length crosses two adjacent allocations. Is the numeric range enough?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

## Part 2 — Diagnose and repair

### Boundary trace

For every raw pointer, record allocation origin, provenance, numeric range, alignment, initialized subrange, active aliasing permission, lifetime owner, and destruction responsibility. For partially initialized storage, show the prefix length after each successful element construction.

For **Raw Pointers, Provenance, and Uninitialized Memory**, choose table columns that expose the actual states rather than copying a generic checklist. Every row must name the owner, the fact established, the fact still delegated, the visible failure effect, and the component responsible for cleanup or rollback.

### Weak repairs to reject

For each prediction, identify a superficially convenient repair that violates the module contract. Reject at least these module-specific shortcuts:

- forming a reference before pointer validity is established;
- treating a non-null address as proof of liveness;
- using pointer arithmetic outside the originating allocation;
- assuming zeroed bytes form an arbitrary valid `T`;
- calling `assume_init` before every field or element is initialized;
- forgetting cleanup for a panic during element construction;

Replace each with the smallest repair that preserves the requirement and state what evidence would distinguish the two designs.

## Part 3 — Focused exercises

### Construction 1

Implement a fixed-capacity batch builder with an initialized-prefix guard.

Required evidence: Support an element constructor that can fail after any index.

### Construction 2

Write the safety proof for converting a fully initialized array of slots.

Required evidence: Explain how cleanup ownership moves and why no element is dropped twice.

### Construction 3

Compare `read`, `read_unaligned`, and `copy_nonoverlapping` for a four-byte header.

Required evidence: State why safe byte conversion remains preferable.

### Construction 4

Audit an integer-to-pointer round trip.

Required evidence: Identify what provenance assumptions it makes and redesign to preserve the original pointer when possible.

### Construction 5

Transfer the initialized-prefix method to an FFI output array.

Required evidence: Define who allocates, how many elements the foreign call initialized, and who drops them.

## Part 4 — Independent laboratory

Build [Panic-Safe Batch Builder](../../labs/module-06-panic-safe-batch-builder/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- a state invariant relating capacity, initialized prefix, and next write position;
- a drop-counting element that records exactly-once destruction;
- panic injection at every construction index;
- tests for zero length, complete success, ordinary error, and unwind cleanup;
- a proof that `Vec::set_len` or slice construction occurs only after full initialization.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. What allocation does each pointer derive from?
2. Which bytes are initialized at the exact operation?
3. Which reference or raw access permissions coexist?
4. How does unwind cleanup know exactly which values are live?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Construct `[T; N]` fallibly with `MaybeUninit`, an initialized-prefix guard, and a callback that fails at a selected index. Use a drop-counting type to test every failure index and the success path. Add a callback that panics and use `catch_unwind` only in the test harness to verify the initialized prefix is dropped. Explain why setting the length/count before a successful write would make the guard unsound.
