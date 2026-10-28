# Module 63: Shared State: Locks and Protected Invariants

**Course 7, day 3 · Module 63 of 90**  

**63/90** · [Course overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [BatchWeave guide](../capstone.md)

## The question

> Which exact invariant does a lock protect, how small can the protected transition be, and what state remains valid after contention or panic?

## Why this comes now

The first two modules preferred ownership transfer and disjoint borrowing because those designs remove synchronization obligations. Some products nevertheless contain genuinely shared mutable state: an inventory, a cache, a lifecycle registry, or a queue. A mutex is appropriate only after that shared state and its invariant are named.

The weak model says “put the data behind a mutex.” The strong model says “this lock serializes this transition over these fields, every reader observes the invariant while holding the same lock, no blocking effect occurs while the guard is live, and panic recovery has a stated policy.” This module develops that stronger model before condition variables and worker queues add waiting behavior.

This module is not complete when you can name the primitive. It is complete when you can state the ownership transfer, the synchronization edge, the progress argument, the failure behavior, and the schedule-dependent facts that remain intentionally unspecified.

## What you will be able to do

- name the state invariant protected by each `Mutex` or `RwLock` rather than treating the primitive as a generic thread-safety wrapper;
- distinguish shared liveness supplied by `Arc` from exclusion supplied by a lock;
- keep guard scope limited to the smallest complete state transition;
- avoid performing user callbacks, channel sends, file I/O, or expensive computation while holding a guard;
- choose between one coarse invariant lock and several locks with an explicit ordering protocol;
- explain mutex poisoning as a product recovery signal rather than a memory-safety guarantee;
- evaluate whether `RwLock` workload assumptions justify its more complex progress behavior;
- design concurrent tests around preserved invariants rather than exact schedules.

## Core model

### A lock protects a relation, not a field

Suppose an inventory stores `available`, `reserved`, and immutable `capacity`. The product invariant is:

```text
available + reserved == capacity
```

If each mutable field has a separate mutex, another thread can observe the transition halfway through: `available` has decreased while `reserved` has not increased. Every individual access is race-free, yet the product state is invalid. Put fields that participate in one atomic business transition under one synchronization boundary.

A good state declaration looks like:

```rust
struct State {
    available: u64,
    reserved: u64,
}

struct Inventory {
    capacity: u64,
    state: Mutex<State>,
}
```

The mutex does not merely protect `state`; it makes reservation and release linearizable transitions over the capacity relation.

### The lock protocol includes every observer

An invariant is not protected when writers lock but readers inspect the fields through another unsynchronized path. All operations that depend on the relation must use the same protocol. That includes debugging output, metrics snapshots, and error construction when they read multiple fields.

Private fields are therefore an architectural tool. If callers can separately lock internal pieces or hold guards across arbitrary code, the type cannot enforce its own transition boundary. Prefer methods that return owned snapshots or small copied facts rather than public guards.

### Guard scope is semantic scope

A `MutexGuard` expresses exclusive access and unlocks through RAII. Its lexical lifetime should match one complete in-memory transition and no more. Holding it while hashing a payload, writing a file, sleeping, invoking a callback, or sending to a bounded channel increases contention and can create deadlock cycles involving unrelated resources.

The usual pattern is:

```text
lock → validate current state → mutate all related fields → copy required facts
     → drop guard → perform effects
```

Dropping before the transition is complete exposes invalid intermediate state. Dropping after effects begin couples the lock to external latency. The correct scope follows the invariant, not arbitrary line count.

### Coarse and fine locks trade proof complexity

One coarse lock may reduce parallelism but provides one simple invariant boundary. Several locks can permit independent progress only when the state really decomposes. They also require a global order when an operation acquires more than one.

A review should record:

| Lock | Protected facts | Operations | May be held with | Order |
|---|---|---|---|---|
| accounts | balances and total | transfer, snapshot | audit | 1 |
| audit | append index | record transfer | none after callback | 2 |

If the table is hard to state, the design may have crossed the point where fine-grained locking is worth its cost.

### `RwLock` is a policy, not a faster mutex

A read-write lock permits multiple readers or one writer. It helps when reads are long enough, sufficiently frequent, and the platform’s fairness behavior fits the product. It may hurt when critical sections are tiny, writes are frequent, or writer starvation matters.

The standard library does not promise one universal fairness policy. Therefore do not make a correctness argument that requires writers to be preferred or queued in a specific order. Correctness must survive allowed scheduling; performance claims require measurement in Course 9.

### Poisoning reports interrupted protected work

A standard mutex becomes poisoned when a thread panics while holding its guard. Poisoning is advisory. It does not prove the state is corrupt, and ignoring it does not create a data race. It tells the next locker that a protected transition may have been interrupted.

Choose a product policy:

- propagate failure and stop the subsystem;
- inspect and repair the state before clearing poison;
- recover the inner value because the transition is known panic-free or self-validating;
- rebuild from authoritative state.

Blind `unwrap()` turns advisory state into an unexamined process panic. Blind `into_inner()` suppresses a potentially important invariant failure. Both need a stated reason.

### Never call unknown code while holding a lock

User callbacks, formatting implementations, logging sinks, allocators with hooks, and channel sends can block, panic, or re-enter the same object. Calling them with a guard live expands the lock graph beyond what the type can review.

Copy or move a stable snapshot out, release the guard, then call. If the callback must decide a transition, split the protocol into prepare and commit phases with a revision check rather than lending the guard to arbitrary code.

### Invariant tests outlive schedule tests

A concurrent test should coordinate meaningful interleavings with barriers or channels, run many independent operations, join all threads, and assert the final invariant. Sleeping for ten milliseconds is not evidence that a specific ordering occurred.

For an inventory, tests can reserve and release from many threads, then assert:

```text
available <= capacity
reserved <= capacity
available + reserved == capacity
```

Intermediate snapshots may also be checked through a public method that locks consistently. The test should not reach into private state or rely on which worker wins.

## Use the idea in a complete program

The following inventory keeps the entire capacity relation under one mutex and returns owned snapshots:

```rust
use std::sync::{Mutex, PoisonError};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Snapshot {
    pub capacity: u64,
    pub available: u64,
    pub reserved: u64,
}

#[derive(Debug, PartialEq, Eq)]
pub enum InventoryError {
    Insufficient { requested: u64, available: u64 },
    InvalidRelease { requested: u64, reserved: u64 },
    StateInterrupted,
}

#[derive(Debug)]
struct State {
    available: u64,
    reserved: u64,
}

pub struct Inventory {
    capacity: u64,
    state: Mutex<State>,
}

impl Inventory {
    pub fn new(capacity: u64) -> Self {
        Self {
            capacity,
            state: Mutex::new(State { available: capacity, reserved: 0 }),
        }
    }

    pub fn reserve(&self, amount: u64) -> Result<Snapshot, InventoryError> {
        let mut state = self.state.lock().map_err(Self::poisoned)?;
        if amount > state.available {
            return Err(InventoryError::Insufficient {
                requested: amount,
                available: state.available,
            });
        }
        state.available -= amount;
        state.reserved += amount;
        Ok(self.snapshot_from(&state))
    }

    pub fn release(&self, amount: u64) -> Result<Snapshot, InventoryError> {
        let mut state = self.state.lock().map_err(Self::poisoned)?;
        if amount > state.reserved {
            return Err(InventoryError::InvalidRelease {
                requested: amount,
                reserved: state.reserved,
            });
        }
        state.reserved -= amount;
        state.available += amount;
        Ok(self.snapshot_from(&state))
    }

    pub fn snapshot(&self) -> Result<Snapshot, InventoryError> {
        let state = self.state.lock().map_err(Self::poisoned)?;
        Ok(self.snapshot_from(&state))
    }

    fn snapshot_from(&self, state: &State) -> Snapshot {
        debug_assert_eq!(state.available + state.reserved, self.capacity);
        Snapshot {
            capacity: self.capacity,
            available: state.available,
            reserved: state.reserved,
        }
    }

    fn poisoned<T>(_: PoisonError<T>) -> InventoryError {
        InventoryError::StateInterrupted
    }
}
```

The linearization point for `reserve` occurs while the guard is held when both fields have been updated. No observer can see the intermediate subtraction. Errors copy the relevant state while locked and then release through return. The public API never exposes a guard.

The example chooses fail-closed poisoning: an interrupted transition becomes `StateInterrupted`. That is defensible because the type lacks a repair source. A different product might validate `available + reserved == capacity`, recover the state, and clear poison. The recovery policy belongs in the type’s contract and tests.

No `Arc` appears inside `Inventory`; callers add `Arc<Inventory>` only when several threads need shared ownership. This separation keeps liveness and exclusion conceptually distinct.

## Practice sequence

1. Rewrite three “mutex protects field” statements as complete invariant statements.
2. Draw guard lifetime around one state transition and move effects outside it.
3. Compare one-lock and two-lock transfer designs through a lock-order table.
4. Choose and defend a poisoning policy for a recoverable cache and a financial ledger.
5. Review a callback-under-lock design for reentrancy and blocking.
6. Build invariant-focused concurrent tests without timing guesses.
7. Complete Protected Inventory and define BatchWeave’s queue-state invariant.

The corresponding independent product is [Protected Inventory](../../labs/module-03-protected-inventory/README.md). The same reasoning then changes one explicit invariant in [BatchWeave](../capstone.md).

## Ready to continue

Continue only when you can do all of the following without using the chapter as a script:

- state the relation protected by every lock in a design;
- show why `Arc` and `Mutex` answer different questions;
- place guard drop after the complete transition and before external effects;
- state a poisoning policy rather than blindly unwrap or ignore;
- write a lock-order table when more than one lock can be held.

## Primary Rust references

- [`Mutex`](https://doc.rust-lang.org/std/sync/struct.Mutex.html)
- [`MutexGuard`](https://doc.rust-lang.org/std/sync/struct.MutexGuard.html)
- [`RwLock`](https://doc.rust-lang.org/std/sync/struct.RwLock.html)
- [Poisoning in `std::sync`](https://doc.rust-lang.org/std/sync/index.html#poisoning)
- [`Arc`](https://doc.rust-lang.org/std/sync/struct.Arc.html)

The course book is self-contained. These references are for checking the exact library contract and following changes in the language or standard library; they are not substitutes for the reasoning developed above.

## Continue

[Open the workbook](workbook.md) · [Open Protected Inventory](../../labs/module-03-protected-inventory/README.md) · [Open the BatchWeave increment](../capstone.md) · [Review the reasoned solutions](solutions.md)
