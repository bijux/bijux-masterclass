# Module 62 — Structured Threads: Scopes, Joins, and Panic Boundaries

**Course 7 · Day 2 · Module 62 of 100**
`████████████████░░░░░░░░░` **62/100**

[Program](../../../README.md) · [Course 7](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-02-scoped-slice-analysis/README.md) · [BatchWeave guide](../capstone.md)

[← Module 61: Threads, Schedules, Send, Sync, and Race Freedom](../module-61-threads-schedules-send-sync-and-race-freedom/index.md) · [Module 63: Shared State: Locks and Protected Invariants →](../module-63-shared-state-locks-and-protected-invariants/index.md)

## The question

> How can borrowed data, thread lifetime, completion, and panic handling be enclosed by one parent operation rather than leaked into the rest of the program?

## Why this comes now

Module 61 used owned values because ordinary spawned threads may outlive the stack frame that created them. That is often the correct product boundary, but it can force allocation or cloning when a finite operation only needs temporary parallel access to existing data. Scoped threads let the compiler prove a stronger fact: every child finishes before the scope returns, so children may borrow data that outlives the scope.

The important lesson is not “scoped threads remove `'static`.” It is structured concurrency: child lifetime, cancellation decisions, joins, and panic observation remain inside the lexical operation that created the children. This module also corrects a common misunderstanding of `'static`: it is a bound on references contained by a value, not a promise that the value itself lives forever.

This module is not complete when you can name the primitive. It is complete when you can state the ownership transfer, the synchronization edge, the progress argument, the failure behavior, and the schedule-dependent facts that remain intentionally unspecified.

### Prerequisite bridge

Module 61 established **Threads, Schedules, Send, Sync, and Race Freedom**. Before continuing, verify that you can recognize race conditions that contain no data race, including check-then-act and winner-selection protocols. This module preserves that capability and adds the ability to explain the real meaning of a `t: 'static` bound and why owned values can satisfy it;. Module 63, **Shared State: Locks and Protected Invariants**, will rely on both when it asks: *Which exact invariant does a lock protect, how small can the protected transition be, and what state remains valid after contention or panic?*

### Scope boundary

This module owns the reasoning for **structured threads: scopes, joins, and panic boundaries** inside Course 7. The course uses operating-system threads and Rayon. Async runtimes, sockets, network protocols, and async cancellation remain Course 8 topics. Lock-free code is taught as a proof exercise, not as a default replacement for locks and channels. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- explain the real meaning of a `T: 'static` bound and why owned values can satisfy it;
- use `thread::scope` to borrow immutable and disjoint mutable data safely;
- partition mutable state before spawning rather than attempt to prove disjointness after overlap exists;
- treat a scope as a lifecycle boundary, not merely a lifetime workaround;
- choose whether to join handles explicitly inside the scope or rely on scope completion and panic propagation;
- separate worker panic from domain failure and define aggregation behavior for both;
- avoid returning references to child-local values or allowing scoped handles to escape;
- compare owned threads, scoped threads, and Rayon decomposition by lifetime, workload, and control needs.

## Core model

### `'static` is about contained references

An ordinary `thread::spawn` requires the closure and return value to be `Send + 'static`. The `'static` bound does not mean the closure object is immortal. It means the closure does not contain borrowed references whose validity could expire while the spawned thread is still running.

An owned `String` satisfies `'static` because it owns its bytes and contains no short reference. A `&'static str` satisfies it because its reference is valid for the program. A reference to a local `String` does not. Leaking memory or cloning everything is not the conceptual repair; choose an ownership or lifecycle boundary that matches the operation.

### A scope proves child completion before exit

`thread::scope` creates a region in which spawned threads may borrow from the enclosing stack. The library and type system ensure that all scoped threads complete before the call returns. That gives a lifetime relation:

```text
borrowed input lifetime ────────────────┐
                                       │
scope lifetime            ───────      │
child execution             ───        │
```

The child cannot outlive the scope, and the scope cannot outlive the borrowed input. This is a compile-time termination boundary for thread lifetime, not a guarantee that the child will finish quickly or avoid deadlock.

### Partition first, then spawn

A safe parallel mutation usually begins by decomposing one mutable borrow into non-overlapping sub-borrows. `chunks_mut`, `split_at_mut`, and iterator-based partitioning make disjointness visible before concurrency begins.

The wrong order is:

1. share one mutable collection;
2. spawn several workers;
3. use runtime indices and hope accesses do not overlap.

The strong order is:

1. obtain one exclusive borrow;
2. split it into disjoint exclusive regions;
3. move one region into each scoped closure;
4. let the scope prove all regions are returned before parent use resumes.

This pattern needs no lock because there is no shared mutable location.

### Structured concurrency contains obligations

A child task should not become an untracked side effect of a parent function. The parent operation owns:

- creation of children;
- any cancellation token or queue closure;
- collection of results;
- observation of panics;
- joining or scope completion;
- cleanup before return.

Lexical scope helps, but product semantics still need a decision. If one child reports a domain error, do others continue? If one panics, should the scope panic after joining all children, or should the parent translate the panic into data? `thread::scope` provides a lifecycle mechanism; you define the failure protocol.

### Implicit and explicit joins differ in error control

A scoped thread handle may be joined explicitly. If it is not, the scope joins it before returning and propagates a panic according to the scope contract. Explicit joins are useful when the product must associate a panic with a partition, aggregate several failures, or continue examining other results.

Do not write an explicit join loop that returns on the first error. The same lifecycle defect from Module 61 applies. Join every child, record failures, then decide the aggregate result.

### Panic is not an ordinary domain result

A worker can return `Result<T, E>` for expected failure and may also panic. The resulting shape after `join` is conceptually:

```text
Result<Result<T, DomainError>, PanicPayload>
```

Flattening both into one string loses policy. Domain errors can name invalid input or a failed operation. Panic usually indicates a violated internal assumption or an unexpected dependency failure. A batch product may contain panic per job, but it should still label it differently and complete all lifecycle obligations.

### Borrowed output must come from an enclosing owner

A scoped thread may return a reference into data borrowed from outside the scope, subject to ordinary lifetime relationships. It cannot return a reference to a local value created inside the child; that owner is destroyed when the child exits. Scope changes the maximum thread lifetime, not the fundamental owner/reference rule.

Prefer returning owned summaries for most parallel work. Borrowed results are useful when they identify elements in a stable enclosing collection, but they can prolong borrows and restrict later mutation.

### Choose the boundary by product shape

Use owned `spawn` when work is independent, may outlive a local operation, or belongs to a long-lived service. Use scoped threads when finite children need temporary access to enclosing data and explicit low-level thread control. Use Rayon when the computation is naturally divisible data-parallel work and work-stealing scheduling is more important than per-thread protocol control.

The mechanism is selected by lifetime, topology, and failure semantics—not by which API avoids a clone in the smallest example.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For explain the real meaning of a `T: 'static` bound and why owned values can satisfy it, construct one positive and one causal negative example. Mark the first decisive fact in the **join and panic tree** and state which evidence could falsify the claim.

2. **Outcome 2.** For use `thread::scope` to borrow immutable and disjoint mutable data safely, construct one positive and one causal negative example. Mark the first decisive fact in the **join and panic tree** and state which evidence could falsify the claim.

3. **Outcome 3.** For partition mutable state before spawning rather than attempt to prove disjointness after overlap exists, construct one positive and one causal negative example. Mark the first decisive fact in the **join and panic tree** and state which evidence could falsify the claim.

4. **Outcome 4.** For treat a scope as a lifecycle boundary, not merely a lifetime workaround, construct one positive and one causal negative example. Mark the first decisive fact in the **join and panic tree** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

This function summarizes borrowed values and mutates disjoint chunks without copying the source collection:

```rust
use std::thread;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Summary {
    pub count: usize,
    pub sum: i64,
    pub min: i32,
    pub max: i32,
}

pub fn summarize_scoped(values: &[i32], workers: usize) -> Option<Summary> {
    if values.is_empty() || workers == 0 {
        return None;
    }

    let chunk_len = values.len().div_ceil(workers);
    thread::scope(|scope| {
        let handles: Vec<_> = values
            .chunks(chunk_len)
            .map(|chunk| {
                scope.spawn(move || Summary {
                    count: chunk.len(),
                    sum: chunk.iter().map(|value| i64::from(*value)).sum(),
                    min: *chunk.iter().min().expect("chunk is nonempty"),
                    max: *chunk.iter().max().expect("chunk is nonempty"),
                })
            })
            .collect();

        let mut combined = None;
        for handle in handles {
            let part = handle.join().expect("worker has no panic path");
            combined = Some(match combined {
                None => part,
                Some(current) => Summary {
                    count: current.count + part.count,
                    sum: current.sum + part.sum,
                    min: current.min.min(part.min),
                    max: current.max.max(part.max),
                },
            });
        }
        combined
    })
}

pub fn normalize_scoped(values: &mut [i64], workers: usize) {
    if values.is_empty() || workers == 0 {
        return;
    }
    let chunk_len = values.len().div_ceil(workers);
    thread::scope(|scope| {
        for chunk in values.chunks_mut(chunk_len) {
            scope.spawn(move || {
                for value in chunk {
                    *value = value.saturating_abs();
                }
            });
        }
    });
}
```

The immutable summary borrows chunks from `values`; the mutable normalization moves disjoint `&mut [i64]` regions into children. The scope proves that all child borrows end before the function returns. No `Arc`, `Mutex`, or clone is needed.

The example uses `expect` only on a deliberately closed internal proof: chunks are nonempty because `chunks` never yields empty chunks, and the worker body contains no intended panic path. A production library that invokes user callbacks or fallible code should not preserve that assumption. It should join explicitly, record panic separately, and avoid returning before all children are accounted for.

The work distribution can be imbalanced when chunks have unequal computational cost. Scoped threads provide lifetime structure, not work stealing. Module 69 will revisit the same reduction under Rayon.

## Practice sequence

1. Classify several values that do and do not satisfy a `'static` bound and explain the references they contain.
2. Translate an ordinary-spawn implementation into a scoped borrow without adding clones.
3. Split a mutable slice into disjoint regions before spawning.
4. Trace nested `Result` values from domain failure and panic through explicit joins.
5. Design a scope that joins every child after one child fails.
6. Compare static chunking with dynamic work distribution for skewed workloads.
7. Complete Scoped Slice Analysis and transfer the lifecycle model into BatchWeave.

The corresponding independent product is [Scoped Slice Analysis](../../labs/module-02-scoped-slice-analysis/README.md). The same reasoning then changes one explicit invariant in [BatchWeave](../capstone.md).

## Ready to continue

Continue only when you can do all of the following without using the chapter as a script:

- explain why an owned `String` can satisfy `'static` without living forever;
- draw the enclosing-data, scope, and child lifetime relationship;
- partition mutable data before spawning and prove non-overlap;
- distinguish domain failure from panic in a join result;
- choose scoped threads only when their lifetime and topology match the product.

## Primary Rust references

- [`std::thread::scope`](https://doc.rust-lang.org/std/thread/fn.scope.html)
- [`std::thread::ScopedJoinHandle`](https://doc.rust-lang.org/std/thread/struct.ScopedJoinHandle.html)
- [`slice::chunks`](https://doc.rust-lang.org/std/primitive.slice.html#method.chunks)
- [`slice::chunks_mut`](https://doc.rust-lang.org/std/primitive.slice.html#method.chunks_mut)
- [The Rust Book: Fearless Concurrency](https://doc.rust-lang.org/book/ch16-00-concurrency.html)

The course book is self-contained. These references are for checking the exact library contract and following changes in the language or standard library; they are not substitutes for the reasoning developed above.

## Continue

Continue to [Module 63 — Shared State: Locks and Protected Invariants](../module-63-shared-state-locks-and-protected-invariants/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
