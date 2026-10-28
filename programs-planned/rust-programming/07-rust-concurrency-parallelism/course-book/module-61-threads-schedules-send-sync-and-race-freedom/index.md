# Module 61: Threads, Schedules, Send, Sync, and Race Freedom

**Course 7, day 1 · Module 61 of 70**  

**61/70** · [Course overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [BatchWeave guide](../capstone.md)

## The question

> What may cross a thread boundary, what may be shared through a reference, and which correctness problems remain after Rust has ruled out data races?

## Why this comes now

Courses 1–6 taught you to follow one value through ownership, borrowing, cleanup, API, and external-boundary decisions. Concurrency adds a second axis: more than one execution agent may make progress between any two observations. The ownership model still matters, but a sequential trace is no longer enough. You must reason over a set of schedules.

Rust begins the concurrency story with a powerful negative guarantee: safe code cannot contain a data race. That guarantee is foundational, not complete. Two threads can update separate atomic values without a data race and still violate a quota. They can wait on locks in opposite order and deadlock. They can race to publish a result so that either valid result wins. They can produce the right collection in a different order on every run. This module builds the vocabulary that prevents “it compiles” from becoming a false proof of concurrent correctness.

This module is not complete when you can name the primitive. It is complete when you can state the ownership transfer, the synchronization edge, the progress argument, the failure behavior, and the schedule-dependent facts that remain intentionally unspecified.

## What you will be able to do

- distinguish concurrency, parallelism, scheduling, interleaving, data races, and broader race conditions;
- derive whether an owned value may move into a thread from its `Send` obligation;
- derive whether a shared reference may cross a thread boundary from the referent’s `Sync` obligation;
- explain why `Arc<T>` provides shared ownership but not automatic mutation safety;
- treat every `JoinHandle` as an explicit completion and failure obligation;
- separate schedule-independent product output from intentionally unspecified timing and completion order;
- construct a thread ledger that records value ownership, cleanup, joins, and publication edges;
- recognize race conditions that contain no data race, including check-then-act and winner-selection protocols.

## Core model

### Concurrency is a set of possible schedules

A sequential program admits one program order per thread of execution. A concurrent program still preserves each thread’s local program order, but the scheduler may interleave operations from different threads in many ways. A correctness claim must therefore quantify over every schedule allowed by the synchronization protocol, not the schedule you observed during a test.

A useful schedule trace names meaningful events rather than CPU instructions:

```text
T1: read quota = 1
T2: read quota = 1
T1: reserve one unit
T2: reserve one unit
```

There is no undefined unsynchronized memory access if `quota` is atomic. The protocol is nevertheless wrong because the read and reservation are one logical transition but were implemented as independent operations. This is a race condition without a data race.

Parallelism is narrower: work literally executes at the same time on multiple cores. A one-core machine can expose concurrency defects through interleaving. A many-core machine can execute a sound concurrent design in parallel. Correctness comes from the protocol, not from the number of cores.

### Data-race freedom is necessary, not sufficient

A data race requires conflicting unsynchronized accesses to the same memory location, with at least one write. Rust’s type system, `Send`/`Sync` rules, and synchronization APIs prevent such races in safe code. That excludes a large class of undefined behavior.

It does not establish:

- atomicity of a multi-step business transition;
- deadlock freedom;
- starvation freedom;
- bounded memory use;
- complete shutdown;
- deterministic result order;
- correct handling of panics;
- a valid memory-ordering proof for a custom atomic protocol.

State the strongest honest claim. “This safe program is data-race free” is a language-level property. “This reservation operation never exceeds capacity” is a product invariant that still requires a protocol and tests.

### `Send` governs ownership transfer

A type is `Send` when ownership of a value may be transferred safely to another thread. Most ordinary Rust types are `Send` because their components are `Send`. `Rc<T>` is not: its reference count is not synchronized. `Arc<T>` is designed for atomic shared ownership and is `Send` when the contained type satisfies the necessary bounds.

`Send` does not mean “cheap to move,” “immutable,” or “thread safe in every use.” A `File` can be `Send`; moving it transfers the cleanup obligation and current file position. A `MutexGuard` is intentionally not generally transferable because unlocking on a different thread conflicts with platform and API assumptions. Ask what ownership obligation moves, not only whether the compiler accepts the type.

Auto traits are structural. A wrapper containing a non-`Send` component usually becomes non-`Send` automatically. Course 6 taught that manually implementing an unsafe trait creates a proof obligation; Module 68 will apply that discipline to `Send` and `Sync`.

### `Sync` governs shared references

A type `T` is `Sync` when `&T` may be sent to another thread. A compact relationship is: `T` is `Sync` when `&T` is `Send`. This says that multiple threads may use shared references according to the operations exposed through `&T`.

`Cell<T>` and `RefCell<T>` permit unsynchronized mutation through a shared reference, so they are not `Sync`. `Mutex<T>` permits mutation through a shared reference, but only after acquiring exclusion, so it can be `Sync` when the protected `T` can safely cross the relevant ownership boundary.

Do not translate `Sync` into “all methods are atomic.” A `Vec<T>` can be `Sync` when `T` is `Sync` because shared references only expose shared operations. It does not permit two threads to push through the same `&Vec<T>`. The type’s API and borrow rules still define what shared access can do.

### `Arc` answers liveness, not mutation

`Arc<T>` answers: how can several owners keep one allocation alive across threads? It does not answer: how may the value be mutated, which invariant is protected, or in what order updates become visible.

Common combinations express different contracts:

```text
Arc<ImmutableConfig>       shared immutable lifetime
Arc<Mutex<State>>          shared ownership plus exclusive state transition
Arc<RwLock<Catalog>>       shared ownership plus many-reader/one-writer policy
Arc<AtomicBool>            shared ownership plus one atomic flag
```

The inner mechanism carries the synchronization meaning. Wrapping a flawed protocol in `Arc` only makes the flawed protocol live longer.

### A thread handle is a resource

`thread::spawn` returns a `JoinHandle<T>`. The handle represents a running computation, its return value, and a possible panic payload. Dropping it detaches the thread; it does not join. Detachment may be intentional for a process-lifetime service, but it is a product decision with shutdown consequences.

For ordinary finite work, record:

- who owns each handle;
- when joins occur;
- whether all handles are joined after an earlier failure;
- how panic is translated or propagated;
- which resources must remain alive until completion.

A loop that returns on the first failed join and abandons later handles has an incomplete failure protocol even if all worker code is safe.

### Determinism has several meanings

Concurrent execution order is usually nondeterministic. Product output need not be. Distinguish:

- **schedule determinism:** the same internal event order occurs; usually not promised;
- **result determinism:** the same logical result occurs for the same input;
- **render determinism:** results are presented in a stable order;
- **failure determinism:** the product has a defined rule when several failures race;
- **timing determinism:** completion times are stable; rarely promised.

A worker pool can assign indexed jobs dynamically, let completions arrive in any order, and assemble output by index. That preserves throughput freedom while giving readers reproducible results.

### The six-column thread ledger

Before writing a spawn loop, record one row per shared or transferred value:

| Value | Initial owner | Thread access | Transfer or sharing mechanism | Completion/cleanup owner | Published fact |
|---|---|---|---|---|---|
| input chunk 3 | coordinator | worker 3 owns | move into closure | worker drops after digest | digest in join result |
| configuration | coordinator | all workers read | `Arc<Config>` | last owner drops | immutable before spawn |
| result slot 3 | coordinator | coordinator writes after join | returned by `JoinHandle` | coordinator | join completion |

The ledger exposes vague phrases such as “workers share the data.” It also reveals when a value is unnecessarily shared rather than partitioned and moved.

## Use the idea in a complete program

The following function gives each worker exclusive ownership of one payload and uses join results as the publication boundary. Completion order is free; output order is stable because each result carries its source index.

```rust
use std::thread;

#[derive(Debug)]
pub enum DigestError {
    WorkerPanicked { index: usize },
}

fn digest(bytes: &[u8]) -> u64 {
    bytes.iter().fold(0xcbf2_9ce4_8422_2325, |hash, byte| {
        (hash ^ u64::from(*byte)).wrapping_mul(0x100_0000_01b3)
    })
}

pub fn digest_parallel(payloads: Vec<Vec<u8>>) -> Result<Vec<u64>, DigestError> {
    let mut handles = Vec::with_capacity(payloads.len());

    for (index, payload) in payloads.into_iter().enumerate() {
        handles.push((index, thread::spawn(move || digest(&payload))));
    }

    let mut output = vec![0; handles.len()];
    let mut first_panic = None;

    for (index, handle) in handles {
        match handle.join() {
            Ok(value) => output[index] = value,
            Err(_) if first_panic.is_none() => {
                first_panic = Some(DigestError::WorkerPanicked { index });
            }
            Err(_) => {}
        }
    }

    match first_panic {
        Some(error) => Err(error),
        None => Ok(output),
    }
}
```

The closure is `move` because each thread must own its payload. No synchronization protects the payload because no other thread can access it. The join operation does three jobs: it waits for completion, transfers the digest back, and observes panic. The loop continues joining after the first panic so that the function does not return while later workers remain detached.

The output vector is mutated only by the coordinator after joins. Worker completion order therefore does not affect rendered order. This is a strong example of eliminating shared mutation by moving disjoint work and returning values.

The design still has an explicit resource bound to discuss: it creates one operating-system thread per payload. That can be correct for a small bounded input, but it is not a general batch architecture. Module 65 introduces bounded worker topology; BatchWeave will not spawn one thread per job.

## Practice sequence

1. Draw two legal schedules for a pair of threads and identify which observations differ.
2. Classify ten standard types by `Send` and `Sync`, then derive the answer from components instead of memorizing it.
3. Rewrite a shared-mutation design by partitioning and moving disjoint ownership.
4. Trace all join handles through success and multiple-panic scenarios.
5. Construct a check-then-act race with atomics and explain why data-race freedom does not repair it.
6. Make an intentionally nondeterministic completion sequence produce deterministic rendered output.
7. Complete the independent lab and transfer the thread ledger into BatchWeave.

The corresponding independent product is [Thread Handoff Matrix](../../labs/module-01-thread-handoff-matrix/README.md). The same reasoning then changes one explicit invariant in [BatchWeave](../capstone.md).

## Ready to continue

Continue only when you can do all of the following without using the chapter as a script:

- derive `Send` and `Sync` questions from ownership and shared-reference use;
- explain one race condition that contains no data race;
- account for every spawned thread and every join handle on success and failure;
- separate completion order from result order;
- name the resource bound missing from a thread-per-item implementation.

## Primary Rust references

- [`std::thread`](https://doc.rust-lang.org/std/thread/)
- [`Send`](https://doc.rust-lang.org/std/marker/trait.Send.html)
- [`Sync`](https://doc.rust-lang.org/std/marker/trait.Sync.html)
- [`Arc`](https://doc.rust-lang.org/std/sync/struct.Arc.html)
- [Rustonomicon: Send and Sync](https://doc.rust-lang.org/nomicon/send-and-sync.html)

The course book is self-contained. These references are for checking the exact library contract and following changes in the language or standard library; they are not substitutes for the reasoning developed above.

## Continue

[Open the workbook](workbook.md) · [Open Thread Handoff Matrix](../../labs/module-01-thread-handoff-matrix/README.md) · [Open the BatchWeave increment](../capstone.md) · [Review the reasoned solutions](solutions.md)
