# Module 83 — Allocation, Memory Footprint, and Ownership Cost

**Course 9 · Day 3 · Module 83 of 100**
`█████████████████████░░░░` **83/100**

[Program](../../../README.md) · [Course 9](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-03-allocation-budgeted-batch-parser/README.md) · [MetricRail guide](../capstone.md)

[← Module 82: CPU Profiling, Cost Models, and Hot-Path Optimization](../module-82-cpu-profiling-cost-models-and-hot-path-optimization/index.md) · [Module 84: Data Movement, Buffering, and Zero-Copy Boundaries →](../module-84-data-movement-buffering-and-zero-copy-boundaries/index.md)

## The question

> Which bytes are owned, borrowed, reserved, retained, duplicated, or temporarily allocated, and which of those states actually dominate product cost?

## Why this comes now

CPU profiles do not explain why memory grows, why an apparently allocation-light design retains gigabytes, or why a small handle keeps a large backing buffer alive. Module 83 adds ownership cost to the production model. Rust makes ownership explicit, but explicit ownership does not automatically make the chosen lifetime, capacity, or representation economical.

You will distinguish inline size, heap allocation, reserved capacity, live payload, retained backing storage, temporary peaks, and allocator overhead. The key question is not “does this allocate?” but “which bytes remain live, for how long, because of which owner, under which workload?”

### Prerequisite bridge

Module 82 established **CPU Profiling, Cost Models, and Hot-Path Optimization**. Before continuing, verify that you can recognize phase-shifting optimizations that make a microbenchmark faster while leaving end-to-end cost unchanged. This module preserves that capability and adds the ability to distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count. Module 84, **Data Movement, Buffering, and Zero-Copy Boundaries**, will rely on both when it asks: *Where do bytes move, who owns them at each boundary, and when does avoiding a copy improve the whole system rather than merely relocate lifetime and retention cost?*

### Scope boundary

This module owns the reasoning for **allocation, memory footprint, and ownership cost** inside Course 9. The course teaches measurement and operational reasoning, not folklore optimization. It does not promise universal performance rankings, complete security proof, or production readiness from one green pipeline. Every conclusion is scoped to a workload, artifact, environment, and time. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

After completing this module, you will be able to:

- distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count
- trace ownership operations that allocate, clone, reallocate, promote, or retain data
- explain when borrowing reduces work and when it only complicates lifetimes without changing allocation
- design capacity policies from observed size distributions instead of guessing large defaults
- use arenas, interning, small-value representations, or reuse only when their lifecycle matches the product
- identify memory leaks, logical retention, fragmentation, cache growth, and queue buildup as different phenomena
- set and verify a memory budget that includes steady state, burst behavior, and cleanup

## Core model

### The governing model

Memory cost is a lifecycle, not `size_of::<T>()`. For each significant value, record `representation → allocation → capacity → owner → retention condition → release event`. A vector may be 24 bytes on the stack while retaining megabytes elsewhere. An `Arc` clone may allocate nothing yet prolong a large graph. A borrowed slice may avoid copying but keep an entire input buffer live. The right optimization follows retained bytes and allocation frequency, not type names.

### 1. Representation is only the first layer

`size_of` reports the inline representation of a type under the current target. It does not include heap allocations reached through pointers, allocator metadata, padding outside the value, or shared ownership elsewhere. A `Vec<T>` stores pointer, length, and capacity inline; its element storage is separate. Production memory claims need a clearly stated accounting boundary.


### 2. Allocation count and live bytes

Many small allocations can cost CPU and fragment memory even when total live bytes are modest. One large retained capacity can dominate footprint while allocation count looks excellent. Measure both. Also distinguish requested capacity from resident memory, because operating-system and allocator behavior are target observations rather than Rust language guarantees.


### 3. Ownership operations have different costs

Moving an owning pointer is usually a small field copy; cloning the owner may duplicate a buffer, increment a reference count, or perform type-defined work. `to_owned`, `to_string`, `collect`, `format!`, and map insertion often allocate. The method name does not reveal the whole cost: capacity reuse, small inputs, and implementation details matter. Count at the product boundary.


### 4. Borrowing and retention

Borrowing can remove copies, but a long-lived borrow can retain the owner. A tiny `&str` into a multi-megabyte buffer keeps the buffer alive. Converting the tiny field to an owned string may reduce peak retention despite adding an allocation. Lifetime topology and memory topology must be analyzed together.


### 5. Capacity and reuse policies

Preallocation is valuable when the size estimate is accurate and the lifecycle is repeated. A huge default capacity merely moves cost earlier and raises the minimum footprint. Reuse avoids allocator traffic but can preserve a rare peak forever. Policies such as shrink-after-large-burst, maximum reusable capacity, and tenant-local pools need explicit bounds.


### 6. Specialized representations

Interning helps when many long-lived values repeat and the intern table itself is bounded. Arenas help when many values share one lifetime and bulk release matches the product. Stack-oriented small-value representations can avoid common allocations but increase inline size and complexity. Each technique trades one lifecycle for another; none is a universal “zero allocation” switch.

Memory is a time-dependent graph. A snapshot of type sizes cannot show backing allocations, shared owners, queue residence, or peak overlap. Production analysis therefore follows allocation events and ownership edges over the operation’s lifetime, then compares the resulting live-byte curve with the configured resource envelope.

### A module-specific decision table

| Memory quantity | What it includes | Common mistake |
|---|---|---|
| inline size | fields stored directly in the value | treating it as total collection memory |
| logical length | initialized elements or bytes in use | assuming unused capacity does not exist |
| reserved capacity | backing storage available without growth | preallocating the maximum for every request |
| retained bytes | storage kept alive by current owners | overlooking a tiny shared slice’s large backing buffer |
| peak live bytes | overlapping allocations at the worst moment | measuring only steady state |
| allocation churn | allocate/free frequency and size classes | optimizing count while live bytes increase |
| resident memory | process pages currently resident | treating it as exact Rust heap ownership |

### Working procedure

1. Draw every owning value, shared owner, borrowed view, and backing allocation for the operation.
2. Mark creation, growth, clone, queue, storage, and drop events on a timeline.
3. Separate logical payload from reserved and retained storage.
4. Measure allocation count, allocated bytes, peak live bytes, and steady retained bytes independently.
5. Vary the workload feature expected to drive memory: line length, concurrent connections, unique series, queue depth, or snapshot size.
6. Propose a representation or lifetime change and predict which ownership edge disappears.
7. Rerun CPU, latency, and correctness checks; fewer allocations do not automatically mean a better product.

### Failure patterns and principled repairs

#### Using `size_of` as the total memory footprint of a collection or service.

`size_of` describes the inline handle, not its heap, capacity, or shared backing storage. Add the allocation graph before making a footprint claim.

#### Replacing owned data with references without examining how long the owner must remain alive.

References can lengthen the owner’s lifetime. Compare retained backing bytes with the cost of copying the small durable field.

#### Calling every clone expensive or every `Arc::clone` free; the semantic and retention costs differ.

A deep clone, `String::clone`, and `Arc::clone` have different immediate work, but all can alter liveness or synchronization. Name the exact clone and ownership consequence.

#### Preallocating for the maximum possible request on every connection.

Maximum-size preallocation multiplies rare capacity by concurrency. Start from measured distributions and retain a separate hard limit.

#### Keeping reusable buffers of arbitrary peak capacity forever.

Buffer reuse can turn one peak request into permanent per-connection retention. Add a shrink or discard policy tied to observed capacity.

#### Introducing an arena or interner before proving that object lifetimes and repetition patterns match it.

Arenas and interners are lifecycle policies, not generic speed tools. Prove repeated values, compatible reclamation, and bounded growth first.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count, construct one positive and one causal negative example. Mark the first decisive fact in the **allocation ledger** and state which evidence could falsify the claim.

2. **Outcome 2.** For trace ownership operations that allocate, clone, reallocate, promote, or retain data, construct one positive and one causal negative example. Mark the first decisive fact in the **allocation ledger** and state which evidence could falsify the claim.

3. **Outcome 3.** For explain when borrowing reduces work and when it only complicates lifetimes without changing allocation, construct one positive and one causal negative example. Mark the first decisive fact in the **allocation ledger** and state which evidence could falsify the claim.

4. **Outcome 4.** For design capacity policies from observed size distributions instead of guessing large defaults, construct one positive and one causal negative example. Mark the first decisive fact in the **allocation ledger** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

```rust
#[derive(Debug)]
struct BufferPool {
    reusable: Vec<Vec<u8>>,
    max_buffer_capacity: usize,
}

impl BufferPool {
    fn take(&mut self) -> Vec<u8> {
        self.reusable.pop().unwrap_or_default()
    }

    fn give_back(&mut self, mut buffer: Vec<u8>) {
        buffer.clear();
        if buffer.capacity() <= self.max_buffer_capacity {
            self.reusable.push(buffer);
        }
    }
}

fn main() {
    let mut pool = BufferPool { reusable: Vec::new(), max_buffer_capacity: 4096 };
    let mut buffer = pool.take();
    buffer.extend_from_slice(b"metric");
    pool.give_back(buffer);
    assert_eq!(pool.reusable.len(), 1);
}
```

Use the example to build two ledgers. The representation ledger records inline fields, length, and capacity. The lifetime ledger records who can keep the backing allocation alive. Change one clone into a borrow and ask whether the owner must now outlive a queue or cache. Then copy only the small durable field and compare peak and retained memory.

The exercise is not to ban allocation. Allocation is often the correct boundary between a short-lived input and durable state. The goal is to make that boundary intentional and bounded.

### MetricRail consequence

MetricRail parses tenant and metric as borrowed slices first, validates them, and only then promotes them to compact owned identifiers. This order prevents allocation for malformed input and prevents durable state from retaining an entire connection buffer. The `Record` fields are private so finite-value validation cannot be bypassed by constructing a struct literal.

Create a memory budget for connection buffers, broker commands, series keys, aggregates, and snapshots. `max_identifier_storage_bytes` bounds durable identifier ownership separately from `max_series`; one short identifier and one maximum-length identifier must not be treated as equivalent capacity.

Measure high-cardinality insertion and snapshot peaks. Snapshot generation deliberately clones durable rows into a stable response model, so the guide must account for overlap between store state, snapshot rows, and rendered output. A later streaming design would reduce peak memory but change locking and response-failure semantics; it is not assumed to be automatically superior.

### Boundary case: optimization by retention

A proposed change replaces each owned metric name with a shared slice into the connection buffer. Allocation count falls sharply, and the ingest microbenchmark improves. Under a soak test, however, resident memory grows until every connection has retained its largest frame. The implementation did not leak unreachable memory; it kept reachable backing allocations alive through valid shared owners.

Construct the accounting explicitly. One 24-byte handle may retain a 64 KiB backing buffer. Multiply the buffer by retained records, queue residence, and concurrent connections rather than multiplying the handle size. Then compare with copying the validated metric name into a compact allocation. The copy performs more immediate work but lets the receive buffer return to a bounded reuse policy.

The production decision depends on the field-to-frame ratio and lifetime. Sharing can still win for large fields consumed quickly within one request. Compact ownership wins when a small field becomes durable or crosses a queue whose residence is variable. The course’s memory model should let you predict that result before a profiler labels the copy “expensive.”

## Practice sequence

1. Produce an allocation and ownership ledger for one MetricRail ingest and one snapshot.
2. Use the Allocation-Budgeted Batch Parser lab to distinguish allocation count from peak live bytes.
3. Measure normal, boundary, and high-cardinality workloads. Record capacity growth and retained memory after the workload ends.
4. Compare a shared-slice representation with compact ownership for a small field taken from a large frame.
5. Add a regression check for durable identifier bytes and a scenario check for snapshot peak memory.
6. Write a decision that names the allocation retained intentionally and the one removed because it had no product value.

Use the [workbook](workbook.md) to freeze predictions and complete the causal repairs. Build the module laboratory before reading its reference implementation, then transfer the mechanism into the [MetricRail engineering guide](../capstone.md).

## Ready to continue

Continue only when you can:

- distinguish inline size, capacity, allocated bytes, retained bytes, and resident memory;
- draw the owners that keep one backing allocation alive;
- explain why borrowing can increase total retention;
- choose preallocation from a workload distribution rather than a maximum;
- justify one clone by the lifetime boundary it establishes;
- state MetricRail’s memory envelope across connections, queue, store, and snapshot.

## Primary Rust references

- The Rust standard library documentation for `Vec`, `String`, `Box`, `Rc`, and `Arc`
- The Rust Performance Book guidance on heap allocation and cloning
- Allocator and operating-system documentation for measurements that claim process-level behavior

These references are for verification and deeper lookup after the chapter’s model is understood. The course-book chapter remains the complete learning route for the required concepts.

## Continue

Continue to [Module 84 — Data Movement, Buffering, and Zero-Copy Boundaries](../module-84-data-movement-buffering-and-zero-copy-boundaries/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
