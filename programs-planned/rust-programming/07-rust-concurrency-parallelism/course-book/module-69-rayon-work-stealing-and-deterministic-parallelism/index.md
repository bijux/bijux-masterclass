# Module 69 — Rayon, Work Stealing, and Deterministic Parallelism

**Course 7 · Day 9 · Module 69 of 100**
`█████████████████░░░░░░░░` **69/100**

[Program](../../../README.md) · [Course 7](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-09-parallel-histogram/README.md) · [BatchWeave guide](../capstone.md)

[← Module 68: Lock-Free Protocols, Reclamation, and Unsafe Send/Sync](../module-68-lock-free-protocols-reclamation-and-unsafe-send-sync/index.md) · [Module 70: Integrated Concurrent Architecture, Testing, and Audit →](../module-70-integrated-concurrent-architecture-testing-and-audit/index.md)

## The question

> How can divisible computation use a work-stealing pool while preserving item meaning, reduction laws, failure policy, result ordering, and a defensible cost model?

## Why this comes now

Modules 61–68 exposed low-level thread topology, blocking coordination, liveness, and atomics. Many CPU-bound workloads do not need a hand-built worker protocol. They need data parallelism: divide a collection or recursive computation, execute pieces in a shared pool, and combine results. Rayon packages this scheduling model behind parallel iterators, `join`, scopes, and thread pools.

The abstraction removes explicit queue code; it does not remove semantic obligations. Parallel closures must satisfy ownership bounds. Reduction operators need identities and associativity. Side effects cannot rely on traversal order. Tiny tasks can cost more to schedule than they save. Failures may be discovered in different orders. This module teaches Rayon as an algebra and scheduling boundary, not a `.par_iter()` performance switch.

This module is not complete when you can name the primitive. It is complete when you can state the ownership transfer, the synchronization edge, the progress argument, the failure behavior, and the schedule-dependent facts that remain intentionally unspecified.

### Prerequisite bridge

Module 68 established **Lock-Free Protocols, Reclamation, and Unsafe Send/Sync**. Before continuing, verify that you can reject a lock-free structure when the product requires mpmc blocking backpressure, dynamic reclamation, or simpler auditability. This module preserves that capability and adds the ability to distinguish task parallelism, data parallelism, and a long-lived message-driven worker service;. Module 70, **Integrated Concurrent Architecture, Testing, and Audit**, will rely on both when it asks: *How do ownership, bounded work, synchronization, liveness, panic, cancellation, atomics, deterministic reporting, and test evidence become one product whose strongest claims are reviewable?*

### Scope boundary

This module owns the reasoning for **rayon, work stealing, and deterministic parallelism** inside Course 7. The course uses operating-system threads and Rayon. Async runtimes, sockets, network protocols, and async cancellation remain Course 8 topics. Lock-free code is taught as a proof exercise, not as a default replacement for locks and channels. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- distinguish task parallelism, data parallelism, and a long-lived message-driven worker service;
- explain work stealing without relying on worker identity or execution order;
- derive closure `Send` and captured-state `Sync` requirements from parallel execution;
- track item ownership and ordering through indexed parallel iterators;
- state identity and associativity laws for `fold`, `reduce`, and grouped aggregation;
- recognize floating-point, string concatenation, and side-effect reductions whose order changes meaning;
- design fallible parallel work with explicit error selection and cancellation expectations;
- choose task granularity, custom pool size, and sequential cutoffs from a cost hypothesis that Course 9 can measure.

## Core model

### Rayon schedules tasks, not named workers

Rayon maintains a thread pool and decomposes parallel operations into tasks. Workers execute local tasks and may steal work from others. The exact worker that processes an item, the order of execution, and the timing of steals are intentionally unspecified.

Therefore do not store product meaning in thread-local worker numbers or assume that adjacent input items run together. Stable identity must come from the input or explicit indices. The scheduling abstraction is free to rebalance skewed workloads.

### Parallel iterators preserve a semantic item stream

A slice’s `par_iter` yields shared references, `par_iter_mut` yields disjoint mutable references, and `into_par_iter` consumes owned items according to the type’s implementation. The same ownership questions from Course 4 apply, now with `Send`/`Sync` bounds.

Indexed parallel iterators know exact length and relative position. Order-sensitive consumers such as collection into a vector can preserve the indexed order even though execution and completion are out of order. Unindexed sources may not offer the same positional guarantees. State which interface supplies order rather than assuming every parallel iterator behaves like a sequential loop.

### Closures must support concurrent invocation

A parallel map closure can run simultaneously on several worker threads. Shared captured references require the referent to be `Sync`; moved per-item values must be `Send`. Mutation of one captured variable through ordinary borrowing is rejected unless the decomposition proves disjointness or synchronization mediates access.

Avoid `Arc<Mutex<Vec<_>>>` as the default output sink. Mapping and collecting lets Rayon allocate and write disjoint output positions. Fold/reduce lets each task accumulate locally and combine later. These patterns reduce contention and make meaning independent of schedule.

### `fold` creates local accumulators

Parallel `fold` differs from one sequential fold. Rayon may create many accumulators by calling the identity closure, process subsets independently, and emit partial values. A later `reduce` combines them. The identity must be cheap and valid for every partition, including empty partitions.

For histograms, each task can build a local map. Reduction merges maps. No lock is needed in the hot loop because each accumulator is owned by one task. The cost tradeoff is additional local allocation and merge work.

### Reduction laws are product contracts

A parallel reduction tree is not fixed. To obtain schedule-independent meaning, the combining operation should have:

- an identity `e` such that `combine(e, x) == x` and `combine(x, e) == x`;
- associativity such that grouping does not change the result.

Commutativity is not always required when the iterator preserves order and the operation uses an ordered consumer, but unordered combination should not rely on argument order. Integer count addition is associative when overflow is ruled out. Floating-point addition is not mathematically associative because rounding differs. String concatenation is associative in content but order-sensitive.

When exact reproducibility matters, use deterministic partitions and a fixed combination order or choose a numerically stable, documented algorithm.

### Fallible parallel work needs a selection policy

Rayon offers fallible collection and reduction patterns, but the first error observed by the parallel scheduler may not be the lowest source index. If the product requires deterministic diagnostics, attach indices, allow all bounded work or collect sufficient errors, then select by stable policy.

Short-circuiting is cooperative. Work already executing may continue. Do not perform irreversible effects in a closure on the assumption that no later item runs after an error. Keep the parallel core pure or idempotent; commit effects after deterministic validation.

### Granularity decides whether parallelism helps

Scheduling, splitting, synchronization, local allocation, and merging have costs. Parallelizing a hundred integer additions is likely slower than a sequential loop. Parallelizing independent expensive parses may help. Useful levers include:

- sequential cutoff for small inputs;
- chunking to increase work per task;
- avoiding per-item allocation;
- local accumulation;
- custom pool size;
- keeping blocking I/O out of a CPU pool.

Course 9 will benchmark. Here, state a falsifiable cost hypothesis instead of claiming speed from API choice.

### Custom pools bound and isolate parallelism

`ThreadPoolBuilder` can create a pool with a defined thread count. `pool.install` runs a parallel operation in that pool. This helps tests, prevents a library from silently consuming the process-global pool policy, and lets BatchWeave reserve a small report-stage pool distinct from its manual worker engine.

Do not create a new pool per tiny request. Pool construction is a resource decision. Also avoid assuming a fixed mapping between tasks and threads inside a custom pool.

### Manual workers and Rayon solve different shapes

Use manual queues when work arrives through a protocol, requires bounded backpressure, explicit cancellation wakeups, long-lived worker state, or lifecycle events. Use Rayon when a finite collection or recursive computation can be decomposed into largely pure tasks and combined algebraically.

BatchWeave uses both: manual workers execute heterogeneous manifest jobs under bounded queue and failure policy; Rayon computes the final pure report histogram over a complete outcome slice. One mechanism does not need to dominate the architecture.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For distinguish task parallelism, data parallelism, and a long-lived message-driven worker service, construct one positive and one causal negative example. Mark the first decisive fact in the **work-partition and reduction map** and state which evidence could falsify the claim.

2. **Outcome 2.** For explain work stealing without relying on worker identity or execution order, construct one positive and one causal negative example. Mark the first decisive fact in the **work-partition and reduction map** and state which evidence could falsify the claim.

3. **Outcome 3.** For derive closure `Send` and captured-state `Sync` requirements from parallel execution, construct one positive and one causal negative example. Mark the first decisive fact in the **work-partition and reduction map** and state which evidence could falsify the claim.

4. **Outcome 4.** For track item ownership and ordering through indexed parallel iterators, construct one positive and one causal negative example. Mark the first decisive fact in the **work-partition and reduction map** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

This histogram uses local `BTreeMap` accumulators and a deterministic final map. It can run in a caller-supplied pool and has a sequential cutoff:

```rust
use rayon::prelude::*;
use rayon::{ThreadPool, ThreadPoolBuilder};
use std::collections::BTreeMap;

#[derive(Debug)]
pub enum HistogramError {
    InvalidThreadCount,
    PoolBuild(String),
}

pub fn build_pool(threads: usize) -> Result<ThreadPool, HistogramError> {
    if threads == 0 {
        return Err(HistogramError::InvalidThreadCount);
    }
    ThreadPoolBuilder::new()
        .num_threads(threads)
        .build()
        .map_err(|error| HistogramError::PoolBuild(error.to_string()))
}

fn merge(
    mut left: BTreeMap<String, usize>,
    right: BTreeMap<String, usize>,
) -> BTreeMap<String, usize> {
    for (key, count) in right {
        *left.entry(key).or_default() += count;
    }
    left
}

pub fn histogram(pool: &ThreadPool, labels: &[String]) -> BTreeMap<String, usize> {
    if labels.len() < 256 {
        return labels.iter().fold(BTreeMap::new(), |mut map, label| {
            *map.entry(label.clone()).or_default() += 1;
            map
        });
    }

    pool.install(|| {
        labels
            .par_iter()
            .fold(BTreeMap::new, |mut local, label| {
                *local.entry(label.clone()).or_default() += 1;
                local
            })
            .reduce(BTreeMap::new, merge)
    })
}
```

Each task owns its local map, so the hot loop needs no mutex. The merge operation adds counts and is associative as long as `usize` overflow is excluded by the product’s maximum input count. `BTreeMap` provides deterministic key order for rendering; task and merge order remain unspecified.

The cutoff is a policy hypothesis, not a universal optimum. Tests should verify equality with a sequential oracle for varied sizes and thread counts. Benchmarks in Course 9 decide whether 256 is appropriate for the target workload.

The pool is supplied by the caller, which makes resource policy visible. BatchWeave constructs one report pool at engine configuration time and uses it only after workers have produced a complete immutable outcome slice.

## Practice sequence

1. Trace ownership and item type through `par_iter`, `par_iter_mut`, and `into_par_iter`.
2. State identity and associativity for three reductions and find a counterexample.
3. Replace a mutex-protected hot-loop accumulator with fold/reduce.
4. Make error selection deterministic by source index.
5. Separate pure CPU work from blocking I/O.
6. Write a cost hypothesis and sequential cutoff.
7. Complete Parallel Histogram and add BatchWeave’s report stage.

The corresponding independent product is [Parallel Histogram](../../labs/module-09-parallel-histogram/README.md). The same reasoning then changes one explicit invariant in [BatchWeave](../capstone.md).

## Ready to continue

Continue only when you can do all of the following without using the chapter as a script:

- explain why work stealing forbids worker-identity assumptions;
- state when positional output order is preserved;
- prove a reduction’s identity and associativity or reject parallel reduction;
- explain why fallible parallel execution may discover errors nondeterministically;
- choose manual workers or Rayon from workload shape and lifecycle needs.

## Primary Rust references

- [Rayon crate documentation](https://docs.rs/rayon/1.12.0/rayon/)
- [`ParallelIterator`](https://docs.rs/rayon/1.12.0/rayon/iter/trait.ParallelIterator.html)
- [`IndexedParallelIterator`](https://docs.rs/rayon/1.12.0/rayon/iter/trait.IndexedParallelIterator.html)
- [`ThreadPoolBuilder`](https://docs.rs/rayon/1.12.0/rayon/struct.ThreadPoolBuilder.html)
- [Rayon FAQ](https://github.com/rayon-rs/rayon/blob/main/FAQ.md)

The course book is self-contained. These references are for checking the exact library contract and following changes in the language or standard library; they are not substitutes for the reasoning developed above.

## Continue

Continue to [Module 70 — Integrated Concurrent Architecture, Testing, and Audit](../module-70-integrated-concurrent-architecture-testing-and-audit/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
