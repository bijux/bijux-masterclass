# Module 67: Atomics, Happens-Before, and Memory Ordering

**Course 7, day 7 · Module 67 of 90**  

**67/90** · [Course overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [BatchWeave guide](../capstone.md)

## The question

> Which fact does an atomic operation publish, which earlier writes become visible because of it, and what is the weakest ordering that proves the required relationship?

## Why this comes now

Locks and channels package synchronization into higher-level protocols. Atomics expose a smaller mechanism: indivisible operations on one value plus memory-ordering constraints. This can reduce coordination overhead and express counters or compact state machines, but it also removes much of the structure that made earlier proofs visible.

The right starting point is not a table saying “Relaxed is fast, SeqCst is safe.” It is the happens-before relation required by the product. Some atomics are independent statistics and need only atomicity. Others publish ordinary memory and require a release/acquire edge. Compare-exchange loops need a linearization point and separate success/failure ordering. This module teaches those derivations before Module 68 places atomics around unsafely shared storage.

This module is not complete when you can name the primitive. It is complete when you can state the ownership transfer, the synchronization edge, the progress argument, the failure behavior, and the schedule-dependent facts that remain intentionally unspecified.

## What you will be able to do

- separate atomicity of one location from visibility of other memory;
- reason with sequenced-before, synchronizes-with, and happens-before relations;
- use relaxed atomics for independent counters whose exact snapshots are advisory;
- derive release/acquire publication when one atomic state makes ordinary writes visible;
- select valid success and failure orderings for compare-exchange loops;
- use `fetch_update` or CAS to make check-and-transition one linearization point;
- reserve sequential consistency for protocols that need one global atomic order rather than using it as unexplained insurance;
- document atomic state machines, legal transitions, observation guarantees, and wraparound limits.

## Core model

### Atomicity is local

An atomic load or read-modify-write cannot be torn, and conflicting accesses through the same atomic object do not form a data race. This says nothing by itself about a multi-variable invariant. Two relaxed counters can each be individually valid while a snapshot observes a combination that never existed as one product state.

Use atomics when the state can genuinely be represented as independent facts or one atomic transition. If correctness requires several fields to change together, a mutex-protected state or packed atomic representation may be clearer.

### Happens-before is the visibility argument

Within one thread, operations are sequenced before later operations according to Rust’s execution rules. Across threads, certain synchronization operations create a synchronizes-with edge. The transitive closure yields happens-before. When ordinary write A happens-before ordinary read B of the same location, B observes a value consistent with that ordering and no data race occurs.

A common publication pattern is:

```text
producer: write payload fields
producer: flag.store(READY, Release)
consumer: flag.load(Acquire) reads READY
consumer: read payload fields
```

If the acquire load reads the value written by the release store, the prior payload writes become visible to later consumer reads. An acquire load that observes an older value establishes no such edge. The proof is conditional on what value was observed.

### Relaxed is complete for some jobs

`Relaxed` preserves atomicity and modification order for the atomic itself but adds no inter-thread ordering for other memory. That is sufficient for independent metrics such as “number of attempts so far” when:

- no ordinary data is published through the counter;
- no invariant relies on a coherent multi-counter snapshot;
- the final authoritative result is computed from joined outcomes or protected state;
- wraparound behavior is understood.

A relaxed live snapshot may show completed count before started count due to independent observations. If the UI requires `completed <= started` at every observation, those values are not independent metrics; protect or encode the relation differently.

### Release/acquire publishes prior work

Release prevents earlier operations in the same thread from being reordered after the release in the abstract memory model. Acquire prevents later operations from moving before the acquire. When the acquire observes the release (or an appropriate release sequence), the pair synchronizes.

The atomic value often represents state: `EMPTY`, `WRITING`, `READY`. The state machine and memory ordering must agree. A `READY` release store is meaningful only after initialization is complete. A consumer must not read payload before an acquire observation of `READY`.

### Read-modify-write orderings have two sides

`compare_exchange(current, new, success, failure)` has a success path that reads and writes and a failure path that only reads. The failure ordering cannot be `Release` or `AcqRel` because no write occurs on failure. It is commonly `Relaxed` when failure only supplies a new candidate, or `Acquire` when the observed value itself publishes data needed before retry/return.

Use the weakest ordering that closes the proof, but write the proof first. “AcqRel/Acquire everywhere” can be correct and still obscure which edge matters. Incorrectly weak orderings may pass every test on a strong memory architecture.

### CAS loops require a linearization point

A quota reservation needs one successful transition from `remaining` to `remaining - amount`. A loop is:

1. load or receive the current value;
2. reject if insufficient;
3. attempt compare-exchange;
4. on failure, retry from the newly observed value;
5. on success, the operation linearizes at that atomic update.

`fetch_update` can express this safely when the transition is a closure from current value to optional next value. The closure may run more than once and must not perform irreversible effects.

Beware the ABA pattern: a value can change A→B→A, so equality with A does not prove the state was untouched. Version tags or a different protocol may be required.

### Sequential consistency is a stronger global relation

Sequentially consistent atomic operations participate in one total order consistent with each thread’s program order. This can simplify protocols involving several atomics whose relative observations matter. It does not make non-atomic conflicting access safe, prevent deadlock, or make a multi-step business operation atomic.

Choose `SeqCst` when the proof needs that global order or when a simpler protocol deliberately accepts its potential cost. Do not claim weaker orderings are inherently “unsafe”; they are wrong only when they fail the required relation.

### Fences separate ordering from one atomic access

Fences can establish ordering around multiple atomic operations, but their synchronization rules are less local and easier to misuse. Prefer release/acquire on the atomic that carries publication when possible. A fence-based protocol must identify the atomic read/write that connects the threads; a fence does not broadcast ordinary memory by itself.

Fences are important in low-level structures and device interaction, but they should appear only after a complete relation is written. Course 6’s external-boundary discipline applies: small unsafe or atomic cleverness must not replace a readable public protocol.

### An atomic state machine needs a ledger

Document:

| State/value | Meaning | Writer transition | Reader observation | Required ordering | Published data |
|---|---|---|---|---|---|
| 0 | created | constructor | any | none | immutable fields |
| 1 | running | CAS 0→1 | status | Relaxed if no payload | none |
| 2 | complete | store Release | load Acquire sees 2 | release/acquire | result buffer |
| 3 | cancelled | CAS | status | Relaxed when queue close carries wake | none |

Also state overflow and reuse. A `usize` sequence counter eventually wraps. If equality distinguishes generations, wraparound can resurrect stale observations unless the product bounds reuse or uses a wider/tagged model.

## Use the idea in a complete program

This progress tracker uses relaxed counters because they publish no other memory. A release/acquire phase transition publishes an immutable final summary stored before completion:

```rust
use std::sync::atomic::{AtomicU8, AtomicUsize, Ordering};
use std::sync::Mutex;

const CREATED: u8 = 0;
const RUNNING: u8 = 1;
const COMPLETE: u8 = 2;
const CANCELLED: u8 = 3;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct LiveSnapshot {
    pub started: usize,
    pub finished: usize,
    pub phase: u8,
}

pub struct Progress {
    phase: AtomicU8,
    started: AtomicUsize,
    finished: AtomicUsize,
    final_summary: Mutex<Option<String>>,
}

impl Progress {
    pub fn new() -> Self {
        Self {
            phase: AtomicU8::new(CREATED),
            started: AtomicUsize::new(0),
            finished: AtomicUsize::new(0),
            final_summary: Mutex::new(None),
        }
    }

    pub fn start(&self) -> bool {
        self.phase
            .compare_exchange(CREATED, RUNNING, Ordering::Relaxed, Ordering::Relaxed)
            .is_ok()
    }

    pub fn record_started(&self) {
        self.started.fetch_add(1, Ordering::Relaxed);
    }

    pub fn record_finished(&self) {
        self.finished.fetch_add(1, Ordering::Relaxed);
    }

    pub fn complete(&self, summary: String) {
        *self.final_summary.lock().unwrap_or_else(|p| p.into_inner()) = Some(summary);
        self.phase.store(COMPLETE, Ordering::Release);
    }

    pub fn final_summary(&self) -> Option<String> {
        if self.phase.load(Ordering::Acquire) != COMPLETE {
            return None;
        }
        self.final_summary
            .lock()
            .unwrap_or_else(|p| p.into_inner())
            .clone()
    }

    pub fn live(&self) -> LiveSnapshot {
        LiveSnapshot {
            started: self.started.load(Ordering::Relaxed),
            finished: self.finished.load(Ordering::Relaxed),
            phase: self.phase.load(Ordering::Relaxed),
        }
    }
}
```

The mutex already synchronizes access to `final_summary`; the release/acquire phase is therefore partly redundant in this exact representation. That is pedagogically useful: it shows that memory order should follow the actual publication path. A lock-free read of final data would require a different safe representation or an unsafe abstraction. Here the acquire phase mainly gives an explicit lifecycle observation before locking.

The live counters are advisory. Separate relaxed loads can observe `finished > started` transiently even when each worker increments started first. The authoritative final report must derive counts from indexed terminal outcomes after joins. BatchWeave will state this difference openly.

`start` uses relaxed CAS because the state transition does not publish other memory; constructor initialization is already visible through the ownership mechanism that shared `Progress`. If starting were the publication boundary for mutable configuration, stronger ordering or a lock would be required.

## Practice sequence

1. Draw a release/acquire publication graph and state the observed-value condition.
2. Classify counters as advisory or invariant-bearing.
3. Repair a check-then-act quota with CAS or `fetch_update`.
4. Choose compare-exchange failure ordering from what the failure path reads.
5. Write an atomic state-machine ledger.
6. Identify one ABA risk and one wraparound assumption.
7. Complete Atomic Progress and integrate honest BatchWeave metrics.

The corresponding independent product is [Atomic Progress](../../labs/module-07-atomic-progress/README.md). The same reasoning then changes one explicit invariant in [BatchWeave](../capstone.md).

## Ready to continue

Continue only when you can do all of the following without using the chapter as a script:

- state what relaxed ordering does and does not guarantee;
- derive one release/acquire edge from publication requirements;
- identify the linearization point of a CAS transition;
- choose a valid failure ordering and justify it;
- separate advisory live metrics from authoritative final state.

## Primary Rust references

- [`std::sync::atomic`](https://doc.rust-lang.org/std/sync/atomic/)
- [`Ordering`](https://doc.rust-lang.org/std/sync/atomic/enum.Ordering.html)
- [`AtomicUsize`](https://doc.rust-lang.org/std/sync/atomic/struct.AtomicUsize.html)
- [Rustonomicon: atomics](https://doc.rust-lang.org/nomicon/atomics.html)
- [Rust Reference: behavior considered undefined](https://doc.rust-lang.org/reference/behavior-considered-undefined.html)

The course book is self-contained. These references are for checking the exact library contract and following changes in the language or standard library; they are not substitutes for the reasoning developed above.

## Continue

[Open the workbook](workbook.md) · [Open Atomic Progress](../../labs/module-07-atomic-progress/README.md) · [Open the BatchWeave increment](../capstone.md) · [Review the reasoned solutions](solutions.md)
