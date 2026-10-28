# Reasoned Solutions — Module 68: Lock-Free Protocols, Reclamation, and Unsafe Send/Sync

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-08-spsc-ring/README.md) · [BatchWeave guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 68: Lock-Free Protocols, Reclamation, and Unsafe Send/Sync**. Compare the reasoning against this question: *What proof permits shared raw storage to be accessed without a lock, and where do role confusion, ABA, destruction, or memory reclamation invalidate a locally plausible algorithm?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

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

## Deep reasoning and transfer

### Decisive model

> What proof permits shared raw storage to be accessed without a lock, and where do role confusion, ABA, destruction, or memory reclamation invalidate a locally plausible algorithm?

Build a **atomic state machine**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish obstruction-free, lock-free, and wait-free progress claims from ordinary nonblocking API behavior.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Explain why `UnsafeCell` is necessary for mutation through shared references and why it removes automatic `Sync`.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Use `MaybeUninit<T>` to represent slots whose initialization state is governed by a concurrent protocol.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Justify unsafe `Send` or `Sync` implementations from exclusive role ownership and atomic publication.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Derive the SPSC ring’s empty/full conditions, slot ownership, and release/acquire edges.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish obstruction-free, lock-free, and wait-free progress claims from ordinary nonblocking API behavior.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the atomic state machine.

### Reference implementation comparison

For [Bounded SPSC Ring](../../labs/module-08-spsc-ring/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In BatchWeave, Module 68 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Lock-Free Protocols, Reclamation, and Unsafe Send/Sync**, which relationship decides this question: “What proof permits shared raw storage to be accessed without a lock, and where do role confusion, ABA, destruction, or memory reclamation invalidate a locally plausible algorithm?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to BatchWeave?
