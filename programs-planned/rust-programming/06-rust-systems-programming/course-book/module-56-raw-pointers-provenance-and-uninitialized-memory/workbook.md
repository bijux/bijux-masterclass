# Workbook — Module 56: Raw Pointers, Provenance, and Uninitialized Memory

[Chapter](index.md) · [Laboratory](../../labs/module-06-panic-safe-batch-builder/README.md) · [FrameVault guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Raw Pointers, Provenance, and Uninitialized Memory** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation?* Preserve your first prediction and record decisive facts in a **initialization and provenance map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 55 — Unsafe Rust as a Proof Boundary that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation?**
3. Draw the smallest **initialization and provenance map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

A raw pointer is copied after its allocation is freed. Is copying itself the dereference error?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

`&packed.field as *const _` is used on an unaligned field. What can already be wrong?

For **Prediction 2**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

A byte pointer is cast to `*const u32`. Which obligations remain?

For **Prediction 3**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

`ptr::read` extracts a `String`, then the original location is dropped normally. What happens?

For **Prediction 4**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

`ptr::write` overwrites an initialized `String`. What happens to the old value?

For **Prediction 5**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

`MaybeUninit<bool>` is uninitialized. May it be read as `bool`?

For **Prediction 6**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

`NonNull<T>` is present. Does it prove one live `T` exists?

For **Prediction 7**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

A raw slice length crosses two adjacent allocations. Is the numeric range enough?

For **Prediction 8**, record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

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

### Interleaved reasoning pass

1. For **Distinguish raw pointers from references and explain why conversion does not transfer ownership**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the initialization and provenance map.
2. For **Use raw borrow operators when creating a reference would itself be invalid**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the initialization and provenance map.
3. For **Derive pointer arithmetic from one allocation and checked element counts**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the initialization and provenance map.
4. For **Use `MaybeUninit` to represent storage that is not yet a valid `T`**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the initialization and provenance map.

5. Identify one guarantee from an earlier course that a careless implementation of **Raw Pointers, Provenance, and Uninitialized Memory** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Panic-Safe Batch Builder](../../labs/module-06-panic-safe-batch-builder/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- a state invariant relating capacity, initialized prefix, and next write position;
- a drop-counting element that records exactly-once destruction;
- panic injection at every construction index;
- tests for zero length, complete success, ordinary error, and unwind cleanup;
- a proof that `Vec::set_len` or slice construction occurs only after full initialization.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

### Laboratory acceptance trace

Before opening the reference implementation for **Panic-Safe Batch Builder**, record:

- the public behavior that demonstrates **Distinguish raw pointers from references and explain why conversion does not transfer ownership**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

### Capstone invariant trace

For the Module 56 FrameVault increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. What allocation does each pointer derive from?
2. Which bytes are initialized at the exact operation?
3. Which reference or raw access permissions coexist?
4. How does unwind cleanup know exactly which values are live?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Construct `[T; N]` fallibly with `MaybeUninit`, an initialized-prefix guard, and a callback that fails at a selected index. Use a drop-counting type to test every failure index and the success path. Add a callback that panics and use `catch_unwind` only in the test harness to verify the initialized prefix is dropped. Explain why setting the length/count before a successful write would make the guard unsound.

### Closed-book defense

In five minutes, answer “How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation?” using the **initialization and provenance map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside FrameVault. A list of APIs without the deciding relationship is incomplete.
