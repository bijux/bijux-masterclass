# Module 65 — Message Passing, Backpressure, and Shutdown

**Course 7 · Day 5 · Module 65 of 100**
`████████████████░░░░░░░░░` **65/100**

[Program](../../../README.md) · [Course 7](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-05-bounded-map-pipeline/README.md) · [BatchWeave guide](../capstone.md)

[← Module 64: Coordination: Condvars, Barriers, and Phase Protocols](../module-64-coordination-condvars-barriers-and-phase-protocols/index.md) · [Module 66: Liveness: Deadlock, Cancellation, and Recovery →](../module-66-liveness-deadlock-cancellation-and-recovery/index.md)

## The question

> Which values cross ownership boundaries, how is capacity bounded, and which explicit protocol event proves that every sender, receiver, and worker can terminate?

## Why this comes now

Locks let several threads coordinate access to one state. Channels provide a different boundary: a sender transfers ownership of a message to a receiver. That often makes protocols easier to review because the receiver becomes the unique owner of the message after receive. It does not remove shared state, backpressure, or lifecycle questions. Channel capacity can be unbounded, sends can block, cloned senders can keep receivers alive forever, and a disconnected channel can mean success, cancellation, panic, or a forgotten handle.

This module develops message passing as a typed protocol. The message enum, topology, capacity, sender ownership, receiver ownership, and shutdown rule must agree. A channel is not an architecture until those facts are written.

This module is not complete when you can name the primitive. It is complete when you can state the ownership transfer, the synchronization edge, the progress argument, the failure behavior, and the schedule-dependent facts that remain intentionally unspecified.

### Prerequisite bridge

Module 64 established **Coordination: Condvars, Barriers, and Phase Protocols**. Before continuing, verify that you can test coordination through causal handshakes rather than sleep-based scheduling assumptions. This module preserves that capability and adds the ability to model channel operations as ownership transfer rather than shared access;. Module 66, **Liveness: Deadlock, Cancellation, and Recovery**, will rely on both when it asks: *Why can every blocked operation eventually continue or terminate, and what happens when cancellation, panic, or partial infrastructure failure interrupts the normal path?*

### Scope boundary

This module owns the reasoning for **message passing, backpressure, and shutdown** inside Course 7. The course uses operating-system threads and Rayon. Async runtimes, sockets, network protocols, and async cancellation remain Course 8 topics. Lock-free code is taught as a proof exercise, not as a default replacement for locks and channels. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- model channel operations as ownership transfer rather than shared access;
- choose bounded, zero-capacity, or unbounded channels from an explicit resource and latency policy;
- draw sender/receiver topology and identify which endpoints are clonable;
- state whether disconnect is normal completion, cancellation, or infrastructure failure;
- design typed messages whose terminal states cannot be confused with ordinary work;
- avoid holding locks or guards while performing potentially blocking sends;
- preserve deterministic result assembly despite nondeterministic receive order;
- prove shutdown by accounting for every sender clone, receiver, queued message, and worker join.

## Core model

### Sending transfers ownership

When `Sender<T>::send` succeeds, the sender no longer owns `T`; the receiver eventually receives ownership. This boundary is often stronger than sharing `Arc<Mutex<T>>` because no two threads need simultaneous mutation rights over the message.

The transfer does not make the value immutable or globally unique forever. The message may contain `Arc` values, handles, or IDs referring to other shared resources. Review the full ownership graph, not only the outer `T`.

A failed send returns the unsent value. That matters for cleanup and retry. Dropping a job on disconnect may leak a product obligation even though Rust drops its memory correctly.

### Capacity is part of correctness

`mpsc::channel` is conceptually unbounded from the product’s point of view: send does not wait for a fixed queue slot. If producers outrun consumers, memory grows until another limit intervenes. `sync_channel(capacity)` bounds queued messages and blocks senders when full. Capacity zero creates a rendezvous: sender and receiver must meet.

Choose capacity by protocol:

- bounded memory and producer backpressure;
- acceptable number of in-flight ownership obligations;
- expected work variance;
- risk of a wait cycle when send occurs while holding another resource;
- shutdown responsiveness.

A large integer is not a proof. State what it bounds and what remains unbounded, such as message payload size or result storage.

### Topology determines behavior

The standard `mpsc` channel supports multiple producers and one receiver. Senders are clonable; the receiver is not. A common worker-pool mistake is attempting to clone one receiver for several workers. Alternatives include:

- one dispatcher receives and forwards to per-worker channels;
- one receiver owner distributes work through shared queue state;
- create one channel per worker and choose a dispatch policy;
- use a different channel implementation in a later product when MPMC semantics are required.

Course 7 intentionally builds one bounded MPMC queue with `Mutex` and `Condvar` so its backpressure and closure protocol remain visible.

### Messages encode the protocol

A loosely typed message such as `String` forces the receiver to infer whether it contains work, an error, or shutdown. Use an enum:

```rust
pub enum WorkerMessage {
    Job(Job),
    Stop,
}
```

Even this may be weaker than channel closure. A `Stop` count must match workers and can sit behind queued work. Closure is broadcast lifecycle state: no future work will be sent. For richer systems, result messages can be:

```rust
pub enum WorkerEvent {
    Completed(JobOutcome),
    InfrastructureFault { worker: usize, message: String },
}
```

The protocol should make every terminal path explicit and avoid using a domain payload as a magic sentinel.

### Disconnect has a cause

Receive returns disconnect only when every sender is dropped. An accidentally retained clone can keep a receiver blocked forever. Conversely, a worker panic can drop its sender and cause disconnect earlier than intended.

Therefore the coordinator should know:

- which component owns the original sender;
- when it is dropped;
- which workers own clones;
- whether workers may create more clones;
- how panic affects sender lifetime;
- whether disconnect is expected after all jobs or a run-level fault.

Do not use “channel closed” as a complete explanation. State who closed it and why.

### Backpressure can form deadlock cycles

A bounded send may block. If the sender holds a lock needed by the receiver, both wait forever. If the coordinator fills a work channel and workers fill a bounded result channel while the coordinator is still sending, the system can form a cycle:

```text
coordinator waits for work capacity
workers wait for result capacity
coordinator is the only result receiver
```

Repair by draining results concurrently, using an adequate bounded topology with a dedicated collector, or making one side unbounded under a proven total-result limit. BatchWeave uses a bounded work queue and an unbounded standard result channel whose total message count is bounded by the manifest job limit; this avoids the cycle while retaining a product memory bound.

### Stable identity decouples receive order

Workers complete according to schedule and workload. Result messages should carry a stable job index. The coordinator stores outcomes by index and renders only after terminal accounting. This gives deterministic output without serializing work.

Sorting by an unstable or nonunique display name is weaker than preserving source identity. Assign identity during parsing, before concurrency. If duplicate domain IDs are rejected, source index still remains useful for diagnostics and exact ordering.

### Shutdown is a protocol, not a final line

A finite channel-based operation needs a complete sequence. One common form is:

1. establish worker endpoints;
2. submit accepted work;
3. close the work source or drop all work senders;
4. receive all terminal outcomes or detect worker faults;
5. drop the coordinator’s result sender so disconnect can occur;
6. join every worker;
7. fill or report any missing outcomes;
8. return.

Cancellation may reorder these actions, but every endpoint and handle still needs one owner and one terminal transition. The shutdown proof should work when zero jobs exist, the first job fails, the queue fills, or one worker panics.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For model channel operations as ownership transfer rather than shared access, construct one positive and one causal negative example. Mark the first decisive fact in the **channel topology** and state which evidence could falsify the claim.

2. **Outcome 2.** For choose bounded, zero-capacity, or unbounded channels from an explicit resource and latency policy, construct one positive and one causal negative example. Mark the first decisive fact in the **channel topology** and state which evidence could falsify the claim.

3. **Outcome 3.** For draw sender/receiver topology and identify which endpoints are clonable, construct one positive and one causal negative example. Mark the first decisive fact in the **channel topology** and state which evidence could falsify the claim.

4. **Outcome 4.** For state whether disconnect is normal completion, cancellation, or infrastructure failure, construct one positive and one causal negative example. Mark the first decisive fact in the **channel topology** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

This small mapper creates one bounded channel per worker because the standard receiver is not clonable. Results carry stable indices, and every sender plus handle has a visible shutdown point:

```rust
use std::sync::mpsc::{self, SyncSender};
use std::thread;

#[derive(Debug)]
pub enum MapError {
    WorkerPanicked { worker: usize },
    ResultChannelClosed,
}

pub fn map_bounded(values: Vec<i64>, workers: usize) -> Result<Vec<i64>, MapError> {
    assert!(workers > 0);
    let (result_tx, result_rx) = mpsc::channel::<(usize, i64)>();
    let mut work_txs: Vec<SyncSender<(usize, i64)>> = Vec::new();
    let mut handles = Vec::new();

    for worker in 0..workers {
        let (work_tx, work_rx) = mpsc::sync_channel::<(usize, i64)>(1);
        let result_tx = result_tx.clone();
        work_txs.push(work_tx);
        handles.push((worker, thread::spawn(move || {
            while let Ok((index, value)) = work_rx.recv() {
                if result_tx.send((index, value.saturating_mul(value))).is_err() {
                    break;
                }
            }
        })));
    }
    drop(result_tx);

    for (position, item) in values.iter().copied().enumerate() {
        let worker = position % work_txs.len();
        work_txs[worker]
            .send((position, item))
            .expect("workers remain alive in this closed example");
    }
    drop(work_txs);

    let mut output = vec![0; values.len()];
    for _ in 0..values.len() {
        let (index, value) = result_rx.recv().map_err(|_| MapError::ResultChannelClosed)?;
        output[index] = value;
    }

    let mut first_panic = None;
    for (worker, handle) in handles {
        if handle.join().is_err() && first_panic.is_none() {
            first_panic = Some(MapError::WorkerPanicked { worker });
        }
    }
    first_panic.map_or(Ok(output), Err)
}
```

This example is intentionally small and exposes limitations. Round-robin dispatch can be imbalanced when item cost varies. The `expect` on send assumes workers cannot panic because the worker body contains no intended panic path; a production engine must return the unsent job and classify infrastructure failure. The result channel is unbounded, but total results are bounded by `values.len()`.

Dropping `work_txs` closes every per-worker input after submission. Dropping the coordinator’s `result_tx` is essential: after worker clones disappear, the result receiver can observe disconnect. The example receives an exact count rather than waiting for disconnect, then joins every worker.

BatchWeave will improve the topology with one shared bounded MPMC queue, dynamic work distribution, typed outcomes, cancellation, and complete missing-outcome repair.

## Practice sequence

1. Draw endpoint ownership for MPSC, per-worker channels, and a shared MPMC queue.
2. Classify channel capacity as a resource and backpressure policy.
3. Replace a string sentinel with typed work and lifecycle state.
4. Find a bounded-channel wait cycle involving a mutex or result queue.
5. Prove disconnect by accounting for all sender clones.
6. Assemble out-of-order completions into deterministic source order.
7. Complete Bounded Map Pipeline and add BatchWeave’s result protocol.

The corresponding independent product is [Bounded Map Pipeline](../../labs/module-05-bounded-map-pipeline/README.md). The same reasoning then changes one explicit invariant in [BatchWeave](../capstone.md).

## Ready to continue

Continue only when you can do all of the following without using the chapter as a script:

- state which ownership obligation crosses each send;
- explain what channel capacity bounds and what it does not;
- draw every endpoint owner and clone;
- state whether disconnect is expected or erroneous in each phase;
- prove that shutdown terminates without a retained sender or blocked cycle.

## Primary Rust references

- [`std::sync::mpsc`](https://doc.rust-lang.org/std/sync/mpsc/)
- [`Sender`](https://doc.rust-lang.org/std/sync/mpsc/struct.Sender.html)
- [`SyncSender`](https://doc.rust-lang.org/std/sync/mpsc/struct.SyncSender.html)
- [`Receiver`](https://doc.rust-lang.org/std/sync/mpsc/struct.Receiver.html)
- [The Rust Book: message passing](https://doc.rust-lang.org/book/ch16-02-message-passing.html)

The course book is self-contained. These references are for checking the exact library contract and following changes in the language or standard library; they are not substitutes for the reasoning developed above.

## Continue

Continue to [Module 66 — Liveness: Deadlock, Cancellation, and Recovery](../module-66-liveness-deadlock-cancellation-and-recovery/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
