# Reasoned solutions — Module 62: Structured Threads: Scopes, Joins, and Panic Boundaries

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the BatchWeave guide](../capstone.md)

Scoped threads are not a trick for defeating `'static`. They express that child execution is subordinate to one parent operation. The strongest solutions make borrowed-data lifetime, complete joining, failure classification, and mutation commit policy visible together.

The answers below are reasoning models, not scripts to imitate. A different implementation can be stronger when it proves the same contract more directly. Compare ownership, synchronization, progress, failure, and determinism—not only surface syntax.

## Part 1 — Prediction solutions

### Prediction 1

No. The closure value only needs to contain no short-lived references. Moving an owned `String` gives the worker ownership, so the closure can satisfy the bound even though both closure and string are dropped when the thread finishes.

### Prediction 2

Ordinary spawn cannot prove the thread finishes before the local vector is dropped. Enclose the spawn in `thread::scope`; then the child may borrow the vector because scope exit waits for child completion.

### Prediction 3

Independent slicing syntax does not by itself prove non-overlap because the first mutable borrow can remain active. Use `split_at_mut(10)` or `chunks_mut` to derive disjoint borrows from one exclusive borrow.

### Prediction 4

The reference is invalid because the child-local `String` is destroyed at child exit. Scope bounds thread lifetime; it does not move the local owner into the parent or extend the owner’s lifetime.

### Prediction 5

An early return abandons explicit accounting for the remaining children. The scope will still enforce completion, but the product loses per-child outcome aggregation and may propagate an implicit panic unexpectedly. Join all handles and decide after collection.

### Prediction 6

Joining produces `Ok(Err(ParseError))`; a panic produces `Err(panic_payload)`. Keep these branches distinct because they have different product meaning.

### Prediction 7

No. Equal item counts do not imply equal cost. Scoped threads prove lifetime safety, while load balance requires a decomposition or scheduler appropriate to work variance.

### Prediction 8

A scoped handle is tied to the scope lifetime. Allowing it to escape could permit a later join or use after the borrowed environment has ended, so the type system prevents storage beyond the scope.

## Part 2 — Repair reasoning

The matrix should be mutably borrowed once, split into disjoint row bands, and each band moved into a scoped closure. That removes whole-input clones and makes the result policy unambiguous: all workers mutate one intended output in non-overlapping regions. Every child must finish before the matrix is returned.

If normalization cannot fail after validation, in-place mutation is coherent. If failures can occur during transformation and the product requires all-or-nothing output, each worker should build an owned candidate band and the parent should commit only after every result succeeds. Scoped borrowing alone does not supply transactional semantics.

## Part 3 — Focused construction guidance

### Construction 1

The source slice outlives the scope; each child lifetime is contained by the scope; parent reuse occurs after all child borrows end. The API proves lifecycle containment, not prompt completion or deadlock freedom.

### Construction 2

Reject or return `None` for empty input, choose a nonzero chunk length, spawn over borrowed chunks, return local maxima, join all, and reduce with `max`. No source allocation is required.

### Construction 3

`chunks_mut` yields disjoint exclusive slices. Move each slice into one child. Scope exit returns the exclusive access to the parent, after which the original slice may be read or mutated again.

### Construction 4

Store an enum per child such as `Completed(T)`, `Domain(E)`, or `Panicked`, indexed by partition. Join every handle, then derive the operation-level result from the complete set.

### Construction 5

Scoped threads provide direct thread control and borrowing but static partitioning. Rayon provides work stealing and concise parallel iterators, at the cost of an ecosystem dependency and less direct worker-protocol control. The workload and failure contract decide.

## Part 4 — Laboratory comparison

The reference should not clone the input or hide it behind a mutex. Inspect how chunk size is chosen when workers exceed elements, whether mutable regions are truly disjoint, and whether all joins occur before error return. A strong test verifies parent reuse after the scope rather than merely checking the numerical answer.

## Part 5 — Capstone comparison

The inspection stage is deliberately scoped because it borrows a parsed manifest for a finite calculation. Execution is different: jobs enter a queue, may outlive the call site that parsed temporary arguments, and need owned payloads. Using two different thread boundaries is a sign of accurate architecture, not inconsistency.

## Part 6 — Reconstruction and defense

The defense should state that `'static` constrains contained references, scopes contain child lifetime, and disjoint mutable work is established through partitioning before spawn. It must also separate lifetime safety from load balance and describe whether errors permit partial mutation. “The compiler accepts it” does not answer the commit policy.

A strong defense states what is guaranteed for every allowed schedule, what is merely likely on one machine, and what the design intentionally leaves unspecified.
