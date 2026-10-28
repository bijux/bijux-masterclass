# Concurrency and parallelism reference desk

This page is a retrieval aid after the chapters have established the models. It is not a substitute for the course sequence.

## Core distinctions

| Term | Precise meaning in this course |
|---|---|
| Concurrency | Multiple operations may be in progress during overlapping time, whether or not they execute simultaneously. |
| Parallelism | Multiple operations execute at the same time on different execution resources. |
| Data race | Concurrent unsynchronized access to one location where at least one access writes; undefined behavior and prevented by safe Rust. |
| Race condition | Product correctness depends on relative timing or schedule. Safe Rust can contain race conditions. |
| Safety | No undefined behavior and no violated safe-API invariant. |
| Liveness | The system can make required progress or terminate. |
| Determinism | The specified result does not depend on the legal schedule. |
| Linearization point | The conceptual instant at which a concurrent operation takes effect. |
| Backpressure | A producer is prevented from outrunning the bounded capacity of downstream work. |
| Happens-before | A relation that makes prior effects visible and ordered before later effects. |

## Send and Sync

`Send` means ownership of a value may cross a thread boundary. `Sync` means shared references to a value may be used from multiple threads; equivalently, `T: Sync` allows `&T: Send`. They are unsafe auto traits because an incorrect manual implementation can make safe code unsound. Most types receive them structurally. `Rc`, `Cell`, and `RefCell` deliberately do not satisfy the required thread-safety contracts; `Arc`, atomics, `Mutex`, and `RwLock` provide synchronized alternatives.

A type being `Send + Sync` does not prove that a protocol is deadlock-free, deterministic, bounded, or logically correct.

## Thread choices

| Need | Mechanism |
|---|---|
| Thread may own all captured values and outlive caller scope | `thread::spawn` with owned `'static` captures |
| Thread borrows stack data and must finish before scope exits | `thread::scope` |
| Divide one computation into two owned branches | two scoped spawns or `rayon::join` |
| Many CPU-bound independent items | Rayon parallel iterator |
| Long-lived service with bounded work | explicit worker group and bounded queue |

Every spawn requires a completion story: join, scoped completion, deliberate detachment, or process lifetime. This course rejects accidental detachment.

## Lock selection

Start with the invariant, not the primitive.

- `Mutex<T>`: one invariant requires exclusive access while inspected or changed.
- `RwLock<T>`: many readers may coexist, but writer progress and platform policy are not guaranteed by the API.
- atomics: one or a few machine-sized state transitions can be proved with explicit ordering.
- message passing: transfer ownership rather than share mutable state.
- immutable data in `Arc<T>`: share without synchronization when no mutation is required.

A larger lock can be easier to prove than several fine-grained locks. Use smaller locks only when the invariant can be decomposed and the liveness benefit is real.

## Condition-variable rule

A condition variable is not the condition. The protected state is the condition.

```rust
let mut state = mutex.lock().expect("state lock poisoned");
while !predicate(&state) {
    state = condvar.wait(state).expect("state lock poisoned");
}
```

The loop handles spurious wakeups and the fact that another thread may change the state before the woken thread reacquires the mutex. Change the state while holding the mutex, then notify. `notify_one` or `notify_all` is a scheduling hint, not a substitute for state.

## Channel protocol checklist

1. What type crosses the channel?
2. Is the channel bounded?
3. What does a full queue do to the producer?
4. How many senders exist?
5. Who owns the receiver?
6. What is the explicit shutdown message or disconnect event?
7. What happens if the receiver disappears?
8. Are results ordered by arrival or by product identity?
9. How are errors, cancellation, and panic represented?
10. Which thread joins which workers?

## Lock-order review

For every operation holding more than one lock, list the acquisition order. Build a directed graph with an edge `A → B` when code may hold `A` while waiting for `B`. A cycle is a deadlock possibility. “The code is fast” and “tests never hung” are not proofs that the graph is acyclic.

## Atomic ordering decision guide

Use atomics only after naming the state machine and the data they synchronize.

- `Relaxed`: the atomic value itself must be updated atomically, but it does not publish unrelated memory.
- `Release` store: prior writes in the current thread become available to a matching acquire observer.
- `Acquire` load: later reads in the current thread observe writes sequenced before the release that supplied the value.
- `AcqRel`: a read-modify-write both acquires prior state and releases its own prior writes.
- `SeqCst`: adds one global order among sequentially consistent operations; it does not repair an invalid state machine.

For compare-exchange, reason separately about success and failure ordering. Failure performs a load, so it cannot use `Release` or `AcqRel`.

## Parallel reduction law

A parallel reduction requires an identity `e` and a combine operation `⊕` such that, for the values involved:

```text
e ⊕ x = x
x ⊕ e = x
(x ⊕ y) ⊕ z = x ⊕ (y ⊕ z)
```

Floating-point addition is not exactly associative. A parallel sum can therefore differ in low-order bits from a sequential left fold. The product must choose a tolerance, a stable algorithm, or a different representation rather than pretending the schedule is irrelevant.

## Honest claims

After a successful design, prefer claims such as:

- “safe Rust prevents data races in the public API”;
- “the queue capacity is fixed at construction”;
- “every worker is joined before `run` returns”;
- “result rendering follows manifest order, not completion order”;
- “metrics are monotonic but not a transactionally consistent snapshot”;
- “the SPSC queue supports exactly one producer and one consumer.”

Avoid claims such as “thread-safe,” “lock-free,” “deterministic,” or “bounded” without naming the operation, progress class, result surface, and resource being bounded.

## Primary references

- Rust standard library: `std::thread`, `std::sync`, `std::sync::mpsc`, and `std::sync::atomic`.
- The Rust Reference and Rustonomicon sections on undefined behavior, data races, `Send`, `Sync`, and atomics.
- Rayon 1.12 documentation for parallel iterators, work stealing, `join`, scopes, and thread pools.

[Return to the course overview](index.md)
