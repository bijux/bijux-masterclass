# Reasoned solutions — Module 68: Lock-Free Protocols, Reclamation, and Unsafe Send/Sync

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the BatchWeave guide](../capstone.md)

The purpose of the SPSC lab is to expose the theorem behind a safe lock-free-looking API. Strong solutions minimize topology, keep unsafe kernels private, connect initialization to index state, and refuse generalization whose reclamation or progress proof has not been supplied.

The answers below are reasoning models, not scripts to imitate. A different implementation can be stronger when it proves the same contract more directly. Compare ownership, synchronization, progress, failure, and determinism—not only surface syntax.

## Part 1 — Prediction solutions

### Prediction 1

Two producers can load the same tail and write the same supposedly uninitialized slot, violating exclusive access and possibly dropping one value. Keep one non-cloneable producer or use a different algorithm.

### Prediction 2

The consumer has not established that producer initialization happens-before its read. Acquire-load tail and proceed only after observing the release-published new tail.

### Prediction 3

A consumer can observe the new tail and read before initialization, causing invalid `T` access. Write the slot first, then release-store tail.

### Prediction 4

`set_len` tells `Vec<T>` that all elements are initialized; dropping or indexing uninitialized elements is invalid. Use `MaybeUninit<T>` storage and track initialized slots in the protocol.

### Prediction 5

A non-`Send` `T` could be written on one thread and moved out on another. Require `T: Send` in the unsafe `Sync` implementation.

### Prediction 6

Uninitialized slots would be dropped, and already popped slots could be dropped again. Only the current initialized queue region may be destroyed.

### Prediction 7

A reader may have loaded the pointer before unlink and dereference it afterward. Use a proven reclamation scheme or defer deallocation until global quiescence.

### Prediction 8

The ring has one producer and one consumer, immediate full/empty returns, no blocking wake, and no MPMC cancellation protocol. It does not meet the capstone’s topology or liveness contract.

## Part 2 — Repair reasoning

The original structure has no salvageable local patch because role, representation, ordering, and destruction are all wrong. Rebuild around a constructor that creates exactly one endpoint of each role, fixed `MaybeUninit` slots, head/tail state, release/acquire ownership transfer, and inner destruction after all `Arc` owners disappear. If product topology is MPMC, choose a lock-based queue or mature library rather than stretching this proof.

## Part 3 — Focused construction guidance

### Construction 1

Initialized slots form the modular interval from head up to but excluding tail. Full leaves one physical slot unused. Producer owns tail when not full; consumer owns head when not empty. After last endpoint drop, no concurrent role remains.

### Construction 2

Producer acquire-loads head before reuse and release-stores tail after initialization. Consumer acquire-loads tail before read and release-stores head after moving out. Own-index loads are relaxed because only that role writes them.

### Construction 3

Return separate structs with private fields and no `Clone`. Add `PhantomData<Cell<()>>` to make each endpoint `!Sync` while allowing ownership movement when `T: Send`.

### Construction 4

When `Inner` drops, all endpoint `Arc`s are gone. Walk modularly from final head to tail and call `assume_init_drop` once per unread slot. No other slot is initialized.

### Construction 5

A reader can hold an unprotected pointer after unlink. Hazard pointers announce protected nodes; epochs delay reclamation until earlier readers quiesce. Both require mature global protocols beyond CAS success.

## Part 4 — Laboratory comparison

Read the `SAFETY:` comments as proof links. Each should name role uniqueness, index state, initialization, and ordering. Verify endpoint auto-trait behavior, not just FIFO tests. The reference is not permission to reuse the unsafe core in unrelated topologies.

## Part 5 — Capstone comparison

The correct capstone contribution is a rejection record. BatchWeave’s lock-based queue is easier to cancel, block, close, and audit. A specialized SPSC path might later connect one worker to one dedicated sink, but only with an independent lifecycle and benchmark justification.

## Part 6 — Reconstruction and defense

The defense must state progress class precisely, derive slot ownership and publication, justify unsafe `Sync`, and account for drop. It should explain ABA and reclamation rather than claiming they are solved. The strongest design may be the decision not to deploy the lock-free structure.

A strong defense states what is guaranteed for every allowed schedule, what is merely likely on one machine, and what the design intentionally leaves unspecified.
