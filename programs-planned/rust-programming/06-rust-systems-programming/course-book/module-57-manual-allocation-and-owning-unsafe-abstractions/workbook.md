# Workbook — Module 57: Manual Allocation and Owning Unsafe Abstractions

[Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether the chapter has become an operational model. Freeze answers before compiling or reading the reference implementation. A correct result without the governing reason is incomplete.

## Part 1 — Predict

### Prediction 1

A nonzero allocation returns null. May the owner store `NonNull::dangling` and continue?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 2

An empty owner calls `dealloc` on a dangling pointer. Is that part of the chosen contract?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 3

Drop reconstructs alignment differently from construction. What can happen?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 4

A slice is returned with an unconstrained generic lifetime. What escape becomes possible?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 5

The buffer is reallocated while a slice is live. Which guarantee fails?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 6

`alloc_zeroed` is used for an arbitrary `T`. Does zero always represent a valid `T`?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 7

A raw owner is made `Clone` by copying fields. What is the destructor outcome?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

### Prediction 8

An unsafe `Send` implementation is added without concurrency analysis. Is byte element type enough proof?

Record: **compile status or runtime category**, **governing contract**, **first invalid transition**, and **smallest principled repair**.

## Part 2 — Diagnose and repair

### Boundary trace

Trace the owner through empty construction, layout validation, allocation request, allocation failure, initialized allocation, shared borrow, mutable borrow, move, and `Drop`. The exact layout used for deallocation must be recoverable from every allocated state.

For **Manual Allocation and Owning Unsafe Abstractions**, choose table columns that expose the actual states rather than copying a generic checklist. Every row must name the owner, the fact established, the fact still delegated, the visible failure effect, and the component responsible for cleanup or rollback.

### Weak repairs to reject

For each prediction, identify a superficially convenient repair that violates the module contract. Reject at least these module-specific shortcuts:

- calling the allocator for a zero-sized request without a defined policy;
- storing length but not alignment or layout;
- exposing an owning raw pointer from a safe method;
- deallocating with a reconstructed but different layout;
- asserting `Send` or `Sync` manually without need;
- using manual allocation where `Vec<u8>` satisfies the product;

Replace each with the smallest repair that preserves the requirement and state what evidence would distinguish the two designs.

## Part 3 — Focused exercises

### Construction 1

Implement `AlignedBytes::new_zeroed` with a typed error.

Required evidence: Handle invalid alignment, zero length, null allocation, and exact layout storage.

### Construction 2

Write the full invariant beside the private fields.

Required evidence: Cover liveness, initialization, uniqueness, and zero state.

### Construction 3

Implement slice methods and `Drop` with safety comments.

Required evidence: Tie returned lifetimes to borrows and deallocate once.

### Construction 4

Explain why the abstraction does not support growth or generic elements.

Required evidence: List the additional proof obligations avoided.

### Construction 5

Transfer the design to a fixed foreign output buffer.

Required evidence: Decide whether initialized length equals capacity or must be reported separately.

## Part 4 — Independent laboratory

Build [Aligned Byte Buffer](../../labs/module-07-aligned-byte-buffer/README.md) from the starter. Freeze the public boundary and adversarial cases before opening the solution. Produce the evidence required by the lab:

- a two-state invariant for empty and allocated values;
- tests for zeroed bytes, mutation, non-power-of-two rejection, zero length, and requested alignment;
- proof that null allocation becomes an error before constructing the owner;
- proof that every deallocation uses the exact stored layout;
- a table showing why each slice borrow prevents conflicting safe access.

Also identify one feature deliberately excluded because it would enlarge the trust, portability, concurrency, or unsafe proof surface.

## Part 5 — Capstone transfer

Implement the matching increment from the [capstone engineering guide](../capstone.md). Add one regression test that fails if this module’s central contract is removed.

## Part 6 — Reconstruct and defend

Answer these questions without the chapter:

1. What represents the empty state?
2. How is alignment validated and preserved?
3. Why can safe slice methods not outlive the owner?
4. Which exact layout is used at deallocation and why is it identical?

End by naming the strongest honest claim after success and one claim the implementation deliberately does not make.

### Independent transfer

Implement a byte owner whose alignment is configurable and whose length may be zero. Enumerate constructor states before code. Test invalid alignment, zero length, successful alignment, zero initialization, exclusive mutation, and one destruction. Add a method that fills the buffer without exposing raw pointers. Explain whether the type should implement `Clone`, `Send`, or `Sync`; do not add an implementation until the field-level and allocator-level contracts justify it.
