# Module 83 Solutions — Allocation, Memory Footprint, and Ownership Cost

[Workbook](workbook.md) · [Chapter](index.md) · [MetricRail guide](../capstone.md)

## Part 1 — Ledger reasoning

### 1. `Vec` representation versus footprint

The 24-byte vector value usually stores pointer, length, and capacity. Capacity planning must include the vector’s element allocation, inline size of every `Record`, two separate string allocations per record unless small-string optimization is provided by another type, each string’s capacity rather than only length, allocator overhead, and any temporary or duplicated buffers. Also count how long the collection lives and whether capacity remains after elements are removed. `size_of` is a representation observation, not a transitive ownership walk.

### 2. Clone taxonomy

`String::clone` allocates and copies its current bytes. `Vec<u64>::clone` allocates and copies all elements. `Arc::clone` increments an atomic strong count and shares the same allocation; payload bytes are not copied, but the allocation remains alive until the last strong owner drops. `Bytes::clone` usually creates another shared view over backing storage; it can retain a much larger frame than the visible slice. Moving any of these transfers the small owner value without copying the payload, although later drops and cache movement still have cost. The important dimensions are bytes copied, allocation performed, synchronization, and lifetime extension.

### 3. Borrowed parsing

Borrowed records are ideal for validation and immediate aggregation while the input buffer is alive. Cross-task queueing generally needs owned or shared storage because the producer buffer may be reused or dropped. Long-term storage should own compact durable data. Error reporting may borrow source slices only while the source remains alive; durable diagnostics should store offsets or compact owned context. Every reference is kept valid by the input owner, not by the reference itself.

### 4. Capacity retention

Two thousand retained 8 MiB buffers represent roughly 16 GiB before connection/task overhead. A reasonable policy may reuse capacity below a normal threshold, shrink or replace buffers above a high-water mark after the request, and bound the number of pooled large buffers. Hysteresis prevents oscillation: keep ordinary capacity, discard exceptional peaks. The threshold should follow observed distributions and the connection memory budget.

### 5. Preallocation

A maximum is a rejection boundary, not a prediction. Preallocating the maximum multiplies rare-case capacity by every concurrent request. Initial capacity can use a measured percentile with growth allowed up to a hard limit, or exact count metadata only after that metadata is validated and checked against the limit. The allocation policy should be explicit and measured.

### 6. Interning

Interning helps when many long-lived records repeat a bounded vocabulary and comparisons/allocations dominate. It is risky when attacker-controlled identifiers create unbounded global entries, entries never expire, synchronization becomes hot, or numeric identity leaks across tenant or process boundaries. A bounded per-tenant interner or map entry reuse can be safer than a global immortal table.

## Part 2 — Repairs

### Case A

The patch traded copies for frame retention. If each tiny key references a large request buffer, the whole buffer remains live. Parse and validate borrowed fields, then use the aggregate map’s entry API: look up with the borrowed key and allocate a compact `String` only for a new series. Existing hot keys require no new durable allocation, and request buffers can be released after aggregation.

### Case B

Bound the pool by item count and total retained capacity. Reject or discard buffers above a high-water mark when returned, and consider replacing them with ordinary-capacity buffers. Record reuse hit rate, allocation churn, and retained bytes. A pool that hides allocations by retaining the worst burst forever violates the memory contract.

### Case C

`Arc` adds a heap allocation for values that could be inline, atomic reference-count traffic, shared-lifetime coupling, and delayed reclamation. Immutable process-wide configuration may need shared ownership. A result passed to one consumer should move. A request-local record should remain owned by its task. Shared snapshots may justify `Arc` when readers outlive the publishing operation. Ownership topology, not clone avoidance, chooses the type.

### Case D

The implementation may replace many small short-lived allocations with one large retained buffer, add pooling that holds peak capacity, or perform more copying/locking around a shared arena. Fewer allocator calls can coexist with higher live memory and worse tail latency. Decide using the product’s latency, throughput, peak, and steady-state budgets together.

## Part 3 — Model answers

### Exercise 1

A conservative checked model is:

```text
peak = fixed
     + C × (connection_task + max_connection_buffer)
     + Q × max_owned_record
     + S × max_series_state
     + O × snapshot_multiplier
     + allocator/runtime headroom
```

Use checked multiplication and addition. Configured maximum buffers, queue slots, series count, and snapshot size can be strict bounds. Per-object allocator overhead, runtime stacks, hash-table load factor, fragmentation, and library internals are measured allowances. State exclusions explicitly instead of calling the formula complete process RSS.

### Exercise 2

Network receipt writes into a bounded connection buffer. Framing borrows a line slice. Parsing borrows tenant and metric strings and parses numeric fields. Queueing either copies a compact validated record or sends it synchronously to the owner. Aggregation looks up with borrowed keys and allocates only when a new `(tenant, metric)` series is inserted. Snapshot rendering borrows aggregate entries, sorts compact references or keys as required, and allocates bounded output. The input buffer drops or is reused immediately after durable promotion.

### Exercise 3

A suitable boundary is:

```rust
struct BorrowedRecord<'a> {
    tenant: &'a str,
    metric: &'a str,
    timestamp_ms: u64,
    value: f64,
}

fn apply(store: &mut Store, record: BorrowedRecord<'_>) -> Result<(), StoreError> {
    // Look up by borrowed key; allocate owned keys only on vacant entry.
    Ok(())
}
```

The store owns keys; the parser does not. Entry lookup can reuse existing allocations for hot identifiers. Do not store a `Bytes` slice for a ten-byte key if it keeps a multi-megabyte frame alive.

### Exercise 4

Warm to ordinary steady state, record allocation calls/bytes and resident/heap observations, then apply a legal boundary burst. Continue ordinary traffic after the burst and observe whether memory returns. Allocation churn is calls and bytes over time; retained memory is live capacity after work completes; peak is the maximum during the burst. Tag measurements with connection count, queue occupancy, series cardinality, and buffer capacities so causes can be distinguished.

## Part 4 — Laboratory review

The parser should reject input above `max_input_bytes` and record count above `max_records` before reserving the result vector. `parse_borrowed` validates field count, key, and numeric value without allocating the key. `parse_batch` promotes one key per accepted record. Pre-counting lines adds a scan but allows exact bounded reservation; the cost is acceptable for this laboratory and should be measured before generalizing to very large streaming input.

## Part 5 — MetricRail transfer

Startup must reject internally inconsistent limits. Every queue or retained map should have a product bound. Large connection buffers should not remain indefinitely after exceptional legal input. The memory ledger should separate strict configured maxima from observed allocator/runtime allowances. “Bounded application state” is a defensible claim; “the process can never use more than X bytes” is not unless every runtime and allocator component is included.

## Part 6 — Defense

`size_of` sees only the vector handle. Allocation count, allocated bytes, live bytes, and retained capacity answer different questions. Removing a clone can extend a large owner’s lifetime. `Arc::clone` copies no payload but changes liveness and uses atomic counting. Borrow validity comes from the owner. Compact promotion prevents small slices retaining large frames. A budget includes all bounded concurrent owners plus measured allowances and checked arithmetic. A deliberate allocation is correct when it establishes a compact durable ownership boundary and allows a larger transient buffer to be released.
