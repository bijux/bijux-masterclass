# Reasoned Solutions — Module 57: Manual Allocation and Owning Unsafe Abstractions

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-07-aligned-byte-buffer/README.md) · [FrameVault guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 57: Manual Allocation and Owning Unsafe Abstractions**. Compare the reasoning against this question: *How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Prediction analysis

### Prediction 1

**Problem.** A nonzero allocation returns null. May the owner store `NonNull::dangling` and continue?

**Reasoned answer.** No. That would misrepresent missing storage as a valid nonempty allocation.

### Prediction 2

**Problem.** An empty owner calls `dealloc` on a dangling pointer. Is that part of the chosen contract?

**Reasoned answer.** No. The zero-length state should skip deallocation because no allocation occurred.

### Prediction 3

**Problem.** Drop reconstructs alignment differently from construction. What can happen?

**Reasoned answer.** Deallocation with a mismatched layout violates the allocator contract.

### Prediction 4

**Problem.** A slice is returned with an unconstrained generic lifetime. What escape becomes possible?

**Reasoned answer.** The slice can outlive and be used after the allocation owner is dropped.

### Prediction 5

**Problem.** The buffer is reallocated while a slice is live. Which guarantee fails?

**Reasoned answer.** The slice can point to moved or freed storage.

### Prediction 6

**Problem.** `alloc_zeroed` is used for an arbitrary `T`. Does zero always represent a valid `T`?

**Reasoned answer.** No. Many types reject the all-zero bit pattern.

### Prediction 7

**Problem.** A raw owner is made `Clone` by copying fields. What is the destructor outcome?

**Reasoned answer.** Two values believe they own one allocation, causing double deallocation.

### Prediction 8

**Problem.** An unsafe `Send` implementation is added without concurrency analysis. Is byte element type enough proof?

**Reasoned answer.** No. Ownership, aliasing, and internal access behavior must be proved.

## Construction guidance

### Constructor

Validate through `Layout`, allocate only for nonzero size, convert null to an error, and commit fields only after success.

### Invariant

The type uniquely owns either no allocation or one allocation whose exact layout is stored and whose byte range is initialized.

### Slices and Drop

Borrow lifetimes prevent escape; drop checks the real-allocation state and uses the stored layout exactly once.

### Scope control

No growth avoids invalidating references and realloc failure; no generic `T` avoids element validity, drop, variance, and zero-sized cases.

### Foreign transfer

If the foreign call reports a written length, the wrapper must check it against capacity before exposing only the initialized prefix.

## Boundary-trace reference

A strong solution trace for this module must trace the owner through empty construction, layout validation, allocation request, allocation failure, initialized allocation, shared borrow, mutable borrow, move, and `Drop`. The exact layout used for deallocation must be recoverable from every allocated state. It should reveal the earliest point at which an invalid assumption would become observable and the unique owner responsible for cleanup or rollback.

## Weak repairs to reject

Reject solutions built around these shortcuts:

- calling the allocator for a zero-sized request without a defined policy;
- storing length but not alignment or layout;
- exposing an owning raw pointer from a safe method;
- deallocating with a reconstructed but different layout;
- asserting `Send` or `Sync` manually without need;
- using manual allocation where `Vec<u8>` satisfies the product;

A principled repair makes the missing fact explicit in a type, checked operation, state transition, safety contract, platform qualification, or foreign-call contract. It does not merely move the assumption to a less visible line.

## Owning-buffer invariant table

| State | Pointer | Length | Layout | Permitted operations |
|---|---|---:|---|---|
| empty | dangling/non-owning sentinel | 0 | retained requested alignment, no allocation | slices of length zero, move, drop |
| allocated | unique non-null allocation pointer | `n > 0` | exact size/alignment used for allocation | safe slice borrowing, move, drop |
| mutably borrowed | same allocation | unchanged | unchanged | no competing access through the owner |
| moved | ownership transferred | inaccessible through old binding | transferred | old binding cannot deallocate |
| dropped | no owner remains | — | exact layout used once | no further access |

The allocator contract is two-sided: successful allocation establishes storage for one exact `Layout`; deallocation must receive the same pointer/layout pair exactly once. Storing only capacity while recomputing alignment later makes that proof fragile.

## Empty and failure cases

Zero-sized allocation requests deserve a deliberate representation because the global allocator API does not make arbitrary zero-size allocation/deallocation pairs a normal owning case. Keep the requested alignment as metadata even when no allocation occurs so later API observations remain truthful.

On allocation failure, do not construct a partially valid safe owner. Validate the layout first, request allocation, handle null through the chosen policy, initialize before exposing slices, and only then publish the owner. Avoid manual `Send` or `Sync` implementations; let the contained fields and safe API determine auto-trait behavior unless a separate proof requires intervention.

## Completion check

Use the chapter’s readiness statement as the first threshold:

You are ready when you can state the owner invariant for every constructor and destructor state, explain why a byte-specific fixed allocation is smaller than a generic vector, and show that every unsafe block follows from private fields and ordinary borrows.

Then perform this destructive regression check: test zero length, invalid alignment, several valid alignments, mutation, movement, and destruction; then remove stored alignment and explain why correct drop can no longer be proved. The resulting failure should be caught for the causal reason predicted in the workbook, not by an unrelated panic or syntax error.

## Deep reasoning and transfer

### Decisive model

> How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state?

Build a **allocator layout record**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Construct and validate `Layout` values without unchecked size arithmetic.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Distinguish allocation capacity from initialized logical length.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Handle zero-length allocations without passing an invalid layout to the allocator.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Pair every successful allocation with exactly one matching deallocation layout.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Design `Drop` and construction failure so no state leaks or double-frees.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Construct and validate `Layout` values without unchecked size arithmetic.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the allocator layout record.

### Reference implementation comparison

For [Aligned Byte Buffer](../../labs/module-07-aligned-byte-buffer/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In FrameVault, Module 57 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Manual Allocation and Owning Unsafe Abstractions**, which relationship decides this question: “How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to FrameVault?
