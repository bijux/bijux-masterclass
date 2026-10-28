# Workbook — Module 68: Lock-Free Protocols, Reclamation, and Unsafe Send/Sync

[Return to the chapter](index.md) · [Open the BatchWeave engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether the chapter has become an operational model. Freeze predictions, protocol diagrams, and invariants before compiling. Concurrency is unusually forgiving of explanations written after observing one successful run; that is exactly why the reasoning record must come first.

## Part 1 — Predict

### Prediction 1

Producer endpoint is made `Clone`. Predict which safety proof fails.

Record: **role cardinality and conflicting slot access**.

### Prediction 2

Consumer reads a slot before acquire-loading the published tail. Predict initialization visibility.

Record: **publication ordering**.

### Prediction 3

Producer release-stores tail before writing the slot. Predict the consumer observation.

Record: **state publication order**.

### Prediction 4

The ring uses `Vec<T>` with uninitialized capacity and calls `set_len`. Predict drop/initialization hazards.

Record: **validity and `MaybeUninit` repair**.

### Prediction 5

`unsafe impl<T> Sync for Inner<T>` omits `T: Send`. Predict cross-thread value movement.

Record: **auto-trait bound**.

### Prediction 6

Inner drop destroys all slots rather than only head-to-tail initialized slots. Predict behavior.

Record: **double drop or invalid drop**.

### Prediction 7

A linked queue deallocates a removed node immediately after CAS. Predict another reader’s risk.

Record: **reclamation and use-after-free**.

### Prediction 8

The SPSC ring replaces BatchWeave’s blocking MPMC queue. Predict missing product requirements.

Record: **topology, backpressure, cancellation, and wake behavior**.

## Part 2 — Diagnose and repair

Review an alleged lock-free queue that stores `Vec<Option<T>>`, shares it through a raw pointer, has cloneable producer handles, updates head and tail with relaxed stores, and frees the buffer when either endpoint drops. The author added `unsafe impl Send + Sync` because tests pass.

Construct the safety-obligation register. Identify role multiplicity, unsynchronized `Option` access, missing publication, premature destruction, and absent full/empty proof. Replace it with the bounded SPSC design or reject the product requirement. Do not attempt an MPMC patch without a new algorithm and reclamation proof.

### Weak repairs to reject

Reject each of these shortcuts and replace it with the smallest repair that preserves the product requirement:

- changing all atomics to sequential consistency while leaving role and lifetime violations;
- adding a safety comment that says only “indices are valid”;
- making endpoints cloneable for ergonomic sharing;
- using `Option<T>` as if ordinary enum mutation became atomic;
- deallocating nodes immediately because they are no longer linked;
- choosing lock-free code for presumed speed without workload measurement;

For every repair, identify which of the six review dimensions it restores: ownership, visibility, exclusion, progress, failure, or determinism. A repair that improves one dimension may damage another; record both effects.

## Part 3 — Focused exercises

### Construction 1

Write the full SPSC slot-state table.

Required evidence: For empty, partial, full, wraparound, and endpoint drop, name initialized slots and role ownership.

### Construction 2

Derive every atomic ordering in push and pop.

Required evidence: Connect each acquire to the opposite release and state what data it publishes or reclaims.

### Construction 3

Design endpoint types that are `Send`, non-Clone, and not `Sync`.

Required evidence: Explain how type properties preserve one producer and one consumer.

### Construction 4

Implement `Drop` for unread values after all endpoints disappear.

Required evidence: Drop exactly the initialized head-to-tail region and justify absence of concurrent access.

### Construction 5

Review a Treiber stack node removal for reclamation.

Required evidence: Explain why successful unlink does not prove no reader holds the node and compare hazard/epoch alternatives at a conceptual level.

## Part 4 — Independent laboratory

Build [Bounded SPSC Ring](../../labs/module-08-spsc-ring/README.md) from the starter. Before opening the solution, produce:

- a complete safety-obligation register for unsafe `Sync`, push, pop, and drop;
- a slot-state diagram across wraparound;
- tests for empty, full, FIFO, wraparound, endpoint movement, and unread-drop cleanup;
- non-cloneable, non-`Sync` endpoint proof;
- a written rejection of unsupported MPMC or reclamation claims;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

## Part 5 — Capstone transfer

Do not replace BatchWeave’s queue. Instead, write an architecture decision record comparing the bounded blocking MPMC queue with the SPSC ring. Show that BatchWeave requires multiple workers, blocking producer backpressure, close-and-wake cancellation, and simple terminal draining. Record the lock-free ring as a specialized mechanism appropriate only for one-producer/one-consumer nonblocking transfer.

Required capstone evidence:

- a topology comparison table;
- a progress and wake-behavior comparison;
- a safety-proof surface comparison;
- a rejection of premature lock-free substitution;
- one candidate future subsystem where SPSC could be appropriate without changing product semantics;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What do lock-free and wait-free mean?
2. Why does `UnsafeCell` require an external synchronization proof?
3. How do head and tail determine slot initialization?
4. What facts justify unsafe `Sync` for the inner ring?
5. Why does node unlink not permit immediate deallocation?

### Independent transfer

Design a one-producer/one-consumer telemetry ring for fixed-size `Sample` values. State whether samples may be dropped on full, how shutdown is signaled, and who drains unread samples. Then change the requirement to four producers and explain why cloning the producer endpoint is unsound and why a new MPSC/MPMC algorithm—not a local CAS addition—is required.
