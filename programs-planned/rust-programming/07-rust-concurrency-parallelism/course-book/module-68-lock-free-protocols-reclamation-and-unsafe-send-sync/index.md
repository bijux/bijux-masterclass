# Module 68: Lock-Free Protocols, Reclamation, and Unsafe Send/Sync

**Course 7, day 8 · Module 68 of 70**  

**68/70** · [Course overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [BatchWeave guide](../capstone.md)

## The question

> What proof permits shared raw storage to be accessed without a lock, and where do role confusion, ABA, destruction, or memory reclamation invalidate a locally plausible algorithm?

## Why this comes now

Course 6 established unsafe Rust as a proof boundary. Module 67 established atomic publication. This module combines them once, in a deliberately narrow topology: one producer, one consumer, fixed-capacity storage, and no concurrent allocation or reclamation. The purpose is not to normalize lock-free programming. It is to make the proof surface visible enough that you can recognize when a production problem requires a mature library or a simpler lock-based design.

The bounded SPSC queue avoids the hardest general problem—reclaiming nodes while unknown readers may still hold pointers. It still requires manual `Sync`, initialization-state reasoning, release/acquire publication, exclusive endpoint roles, and correct destruction. Those obligations show why “replace mutex with atomics” is not a local refactor.

This module is not complete when you can name the primitive. It is complete when you can state the ownership transfer, the synchronization edge, the progress argument, the failure behavior, and the schedule-dependent facts that remain intentionally unspecified.

## What you will be able to do

- distinguish obstruction-free, lock-free, and wait-free progress claims from ordinary nonblocking API behavior;
- explain why `UnsafeCell` is necessary for mutation through shared references and why it removes automatic `Sync`;
- use `MaybeUninit<T>` to represent slots whose initialization state is governed by a concurrent protocol;
- justify unsafe `Send` or `Sync` implementations from exclusive role ownership and atomic publication;
- derive the SPSC ring’s empty/full conditions, slot ownership, and release/acquire edges;
- implement destruction only after all endpoints are gone and drop exactly initialized elements;
- identify ABA, use-after-free, and reclamation obligations in pointer-based lock-free structures;
- reject a lock-free structure when the product requires MPMC blocking backpressure, dynamic reclamation, or simpler auditability.

## Core model

### Progress classes are precise claims

A nonblocking method name does not imply a lock-free algorithm. Common system-wide progress terms are:

- **obstruction-free:** one operation completes if it eventually runs in isolation;
- **lock-free:** in a finite number of system steps, some operation completes, though one thread may starve;
- **wait-free:** every operation completes in a bounded number of its own steps.

These claims require an algorithm and execution model, not the absence of `Mutex` in source. A spin loop around a CAS may be lock-free and still consume a core under contention. An allocator called inside the operation can introduce hidden locks. State only the progress property actually proved.

### `UnsafeCell` marks unsynchronized interior access

Rust assumes data reachable through `&T` is not mutated unless the mutation is mediated by an interior-mutability primitive. `UnsafeCell<T>` is the fundamental escape hatch. It permits mutation through shared references, but it does not provide synchronization or make aliasing safe. It is intentionally not `Sync`.

A concurrent abstraction containing `UnsafeCell` must establish that conflicting accesses never occur. For the SPSC ring, unique producer and consumer endpoint types plus atomic indices assign each slot to at most one role at a time.

### `MaybeUninit` separates storage from a live value

An allocated slot can exist before a `T` has been written and after a `T` has been moved out. Treating every slot as initialized would cause invalid reads or double drops. `MaybeUninit<T>` lets the protocol represent raw storage.

The type system does not track which ring slots are initialized. The queue proof must connect index state to initialization:

```text
head == tail        no readable slot
head != tail        slot at head is initialized
next(tail) == head  no writable slot
otherwise           slot at tail is uninitialized and writable
```

Unsafe reads and writes are valid only under these state facts.

### Endpoint types enforce one producer and one consumer

The constructor returns two non-cloneable endpoints. `Producer<T>` owns permission to mutate the tail position and write the current tail slot. `Consumer<T>` owns permission to mutate head and read the current head slot. Both share an `Arc<Inner<T>>` for lifetime.

Make endpoints `Send` so each may move to its designated thread, but not `Sync`, so a shared reference to one endpoint cannot be used concurrently. A `PhantomData<Cell<()>>` can express the non-`Sync` marker without runtime state. The safety proof depends on the public API preserving these role counts.

### One empty slot distinguishes full from empty

Allocate `requested_capacity + 1` slots and keep head/tail indices modulo that length. Then:

```text
empty: head == tail
full:  next(tail) == head
usable capacity: slots.len() - 1
```

Producer writes at `tail`, then publishes new tail. Consumer reads at `head`, then publishes new head. The extra slot avoids a separate full flag and keeps role ownership simple. Construction must reject zero capacity and overflow in `capacity + 1`.

### Release/acquire transfers slot ownership

Producer sequence:

1. load its own tail relaxed;
2. compute next;
3. acquire-load head to ensure space and observe consumer release;
4. write `T` into the uninitialized tail slot;
5. release-store next tail, publishing initialization.

Consumer sequence:

1. load its own head relaxed;
2. acquire-load tail; equality means empty;
3. read/move initialized `T` from head slot;
4. release-store next head, publishing that the slot is reusable.

The acquire loads pair with the opposite role’s release stores. Each role has exclusive access to its own index, so relaxed loads of that index are sufficient.

### Unsafe `Sync` is the abstraction theorem

`Inner<T>` contains `UnsafeCell<MaybeUninit<T>>` and is not automatically `Sync`. An unsafe implementation such as `unsafe impl<T: Send> Sync for Inner<T>` asserts:

- at most one producer endpoint exists;
- at most one consumer endpoint exists;
- endpoints are not concurrently shared;
- indices assign disjoint slot access;
- release/acquire orders initialization and reuse;
- `T` crosses from producer to consumer, so `T: Send` is required;
- destruction occurs only after endpoint access has ended.

Every bullet must be enforced by private fields and constructors. Comments adjacent to unsafe operations connect local code to these global facts.

### Drop is part of the concurrent protocol

When the last `Arc<Inner<T>>` is dropped, no endpoint can still access the ring. `Inner::drop` may then walk from head to tail and destroy each initialized, unread element exactly once. Already popped elements were moved out and must not be dropped again. Never run this cleanup concurrently with producer or consumer operations.

Endpoint drop may leave unread elements; that is acceptable if inner drop reclaims them. A richer queue might support explicit close or drain, but those are separate product semantics.

### Reclamation is the hard general case

A linked lock-free queue can remove a node from the shared structure while another thread still holds a raw pointer obtained earlier. Deallocating immediately creates use-after-free. Common solutions include hazard pointers, epoch-based reclamation, reference counting, or never reclaiming until global quiescence. Each introduces its own progress and memory-bound tradeoffs.

ABA compounds the problem: a pointer value can be removed, freed, reallocated at the same address, and appear unchanged. Pointer equality no longer proves object identity. Do not design a general lock-free linked structure from CAS snippets. Use a mature, reviewed implementation or choose locks when the product does not require the additional proof surface.

### False sharing can erase the intended benefit

Head and tail are independently written by different cores. If they occupy the same cache line, cache coherence can cause contention even though logical ownership is disjoint. Padding may help, but cache-line size and layout are target observations, not universal guarantees. Course 9 will measure rather than assume.

The correct conclusion is not “pad every atomic.” It is that lock-free correctness and lock-free performance are separate claims.

## Use the idea in a complete program

The central operations of a bounded SPSC ring can be expressed as follows. The full laboratory includes construction, endpoint markers, error types, and destruction:

```rust
use std::cell::UnsafeCell;
use std::mem::MaybeUninit;
use std::sync::atomic::{AtomicUsize, Ordering};

struct Inner<T> {
    slots: Box<[UnsafeCell<MaybeUninit<T>>]>,
    head: AtomicUsize,
    tail: AtomicUsize,
}

// SAFETY: the public constructor creates exactly one producer and one consumer;
// endpoint types are non-Clone and !Sync. Atomic indices transfer exclusive slot
// ownership, and T moves from the producer thread to the consumer thread.
unsafe impl<T: Send> Sync for Inner<T> {}

impl<T> Inner<T> {
    fn next(&self, index: usize) -> usize {
        if index + 1 == self.slots.len() { 0 } else { index + 1 }
    }

    unsafe fn try_push(&self, value: T) -> Result<(), T> {
        let tail = self.tail.load(Ordering::Relaxed);
        let next = self.next(tail);
        if next == self.head.load(Ordering::Acquire) {
            return Err(value);
        }

        // SAFETY: the producer role is unique; `next != head` proves the tail
        // slot is not owned by the consumer and is currently uninitialized.
        unsafe { (*self.slots[tail].get()).write(value) };
        self.tail.store(next, Ordering::Release);
        Ok(())
    }

    unsafe fn try_pop(&self) -> Option<T> {
        let head = self.head.load(Ordering::Relaxed);
        if head == self.tail.load(Ordering::Acquire) {
            return None;
        }

        // SAFETY: the consumer role is unique; observing tail after Acquire
        // proves the producer completed initialization of the head slot.
        let value = unsafe { (*self.slots[head].get()).assume_init_read() };
        self.head.store(self.next(head), Ordering::Release);
        Some(value)
    }
}
```

The unsafe methods are private implementation kernels. Safe producer and consumer methods call them only while role uniqueness holds. The comments do not merely restate “pointer is valid”; they identify the role, index condition, initialization state, and ordering edge that make the operation valid.

This queue is bounded and nonblocking in its API: full and empty return immediately. It is not BatchWeave’s queue. BatchWeave needs multiple producers/consumers, blocking backpressure, cancellation wakeups, and straightforward shutdown. Generalizing this ring to MPMC would change slot reservation, progress, and destruction proofs substantially.

A test passing millions of wraparounds is useful but cannot establish soundness. Miri or sanitizers may detect some defects, but the primary artifact is the safety proof and private API boundary.

## Practice sequence

1. Classify progress claims precisely and reject “lock-free” by source appearance.
2. Map every slot state to initialization and role ownership.
3. Derive release/acquire edges for push and pop.
4. Write the unsafe `Sync` proof from public endpoint restrictions.
5. Trace unread elements through endpoint drop and inner destruction.
6. Identify where a linked structure would require reclamation and ABA control.
7. Complete Bounded SPSC Ring and document why BatchWeave keeps a lock-based queue.

The corresponding independent product is [Bounded SPSC Ring](../../labs/module-08-spsc-ring/README.md). The same reasoning then changes one explicit invariant in [BatchWeave](../capstone.md).

## Ready to continue

Continue only when you can do all of the following without using the chapter as a script:

- state the exact SPSC topology and why endpoints are not cloneable or `Sync`;
- prove a push slot is uninitialized and exclusively producer-owned;
- prove a pop slot is initialized and exclusively consumer-owned;
- connect every unsafe operation to an index and memory-ordering fact;
- explain why pointer-based MPMC reclamation is a different class of problem.

## Primary Rust references

- [`UnsafeCell`](https://doc.rust-lang.org/std/cell/struct.UnsafeCell.html)
- [`MaybeUninit`](https://doc.rust-lang.org/std/mem/union.MaybeUninit.html)
- [Rustonomicon: Send and Sync](https://doc.rust-lang.org/nomicon/send-and-sync.html)
- [Rustonomicon: atomics](https://doc.rust-lang.org/nomicon/atomics.html)
- [Rust Reference: data races](https://doc.rust-lang.org/reference/behavior-considered-undefined.html)

The course book is self-contained. These references are for checking the exact library contract and following changes in the language or standard library; they are not substitutes for the reasoning developed above.

## Continue

[Open the workbook](workbook.md) · [Open Bounded SPSC Ring](../../labs/module-08-spsc-ring/README.md) · [Open the BatchWeave increment](../capstone.md) · [Review the reasoned solutions](solutions.md)
