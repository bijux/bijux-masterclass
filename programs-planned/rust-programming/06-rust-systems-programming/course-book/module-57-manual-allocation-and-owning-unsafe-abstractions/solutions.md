# Reasoned solutions — Module 57: Manual Allocation and Owning Unsafe Abstractions

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md)

Use these solutions after freezing your own analysis. The code result matters less than locating the first broken contract and identifying who owns the repair.

Read each answer as a boundary proof: identify the missing fact, the component able to establish it, and the state that must remain unchanged when the proof fails.

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
