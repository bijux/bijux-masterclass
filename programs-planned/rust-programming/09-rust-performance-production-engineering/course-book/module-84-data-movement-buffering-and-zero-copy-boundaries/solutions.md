# Reasoned Solutions — Module 84: Data Movement, Buffering, and Zero-Copy Boundaries

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-04-borrowed-record-window/README.md) · [MetricRail guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 84: Data Movement, Buffering, and Zero-Copy Boundaries**. Compare the reasoning against this question: *Where do bytes move, who owns them at each boundary, and when does avoiding a copy improve the whole system rather than merely relocate lifetime and retention cost?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Byte-journey reasoning

### 1. Move, clone, and copy

Moving a `Vec<u8>` copies only its small owner fields—pointer, length, and capacity—into the destination; the payload allocation remains where it was and ownership changes. Cloning `Bytes` normally increments shared ownership metadata and creates another view without copying payload bytes, but the backing allocation’s lifetime extends. Creating a `String` from a slice allocates and copies those ten bytes into compact independent storage. These operations differ in payload traffic, allocation, synchronization, and liveness.

### 2. A small slice of a large frame

A `Bytes` slice references shared backing storage, so any live slice can keep the complete 8 MiB allocation alive. One million views can therefore retain enormous backing capacity even though visible lengths total only 16 MiB. Copy compact durable identifiers into `String`/`Box<str>`, or redesign storage so views come from compact per-field backing allocations. Copying is often the correct way to end an accidental lifetime dependency.

### 3. Borrow across an async boundary

The spawned task may outlive the mutable borrow and the connection wants to reuse the storage, so references cannot remain valid. Parse borrowed fields only within the buffer’s validity scope, validate them, then promote the minimal durable record to owned strings/bytes before queueing. Alternatively, move a shared immutable frame into the task, but account for retained frame size and task lifetime.

### 4. Vectored writes

A successful call may write only a prefix of the concatenated slices. State must include the current slice index and offset inside that slice. After `n` bytes, consume complete slices and advance within the first partial slice. Retry interrupted operations according to the I/O contract; treat zero progress where progress is required or terminal errors explicitly. Never resend the already written prefix.

### 5. Coalescing

Coalescing may help when many tiny fragments create high syscall or protocol overhead and the total output is bounded. It hurts when responses are already contiguous, small, or can be written efficiently through buffering/vectored I/O, because it adds allocation, copy, and peak memory. Measure output size distribution, fragment count, syscall count, throughput, tail latency, and peak/live bytes.

### 6. Kernel boundaries

The parser may be zero-copy **from the userspace receive buffer to borrowed field views**. The full network-to-disk path is not generally zero-copy: the kernel transfers bytes into userspace, encoding may create new bytes, and file writes cross another boundary. A narrow claim names the endpoints; an end-to-end slogan hides them.

## Part 2 — Repairs

### Case A

If RSS rises in frame-sized steps while entry count and visible key bytes remain stable, backing-store retention is likely. Record each retained view’s visible length and backing-frame identifier/size, then compare a version that copies keys into compact storage. If memory falls while map cardinality is unchanged, the cause is retention rather than leaked entries.

### Case B

The patch replaced bandwidth/allocation cost with lock acquisition, cache-line bouncing, blocked stages, longer critical sections, and lifecycle coupling. Independent stage-local buffers may permit parallel progress and simpler ownership. Compare copied bytes against lock wait, critical-section time, throughput, and tail latency; optimize the dominant product cost rather than copy count in isolation.

### Case C

Reuse ordinary capacities but discard or shrink exceptional buffers above a high-water mark after use. Bound the number and total capacity of pooled buffers. Hysteresis avoids repeated grow/shrink cycles. The policy should be based on snapshot-size distribution and retained-memory budget.

### Case D

A Rust move transfers ownership of the allocation handle; it does not traverse and duplicate payload bytes. The small handle value is copied through registers or stack memory, and the destination becomes responsible for drop. Cache effects and later deallocation still exist, but classifying a move as a payload copy leads to wrong architecture decisions.

## Part 3 — Model answers

### Exercise 1

A defensible ledger might be:

- socket → connection buffer: kernel/userspace transfer into owned bounded storage;
- buffer → frame: borrowed or shared slice, no payload copy;
- frame → parsed fields: borrows plus numeric decoding;
- fields → broker message: compact owned copy only for durable identifiers, numeric fields moved;
- message → aggregate map: lookup by borrowed key; allocate only for new series;
- map → snapshot bytes: deterministic encoding into bounded output or buffered writer;
- snapshot → socket/file: I/O transfer; short writes handled;
- owners release when the request, message, map entry, or output operation ends.

### Exercise 2

Use an immediate borrowed lookup when the consumer finishes before the frame changes. Use a compact `String`/`Box<str>` when one durable owner needs an independent field. Use `Arc<str>` when multiple long-lived owners truly share one compact string. Use a `Bytes` view when multiple consumers share a reasonably sized immutable frame and retention is bounded. Backing allocation size and lifetime are as important as visible field size.

### Exercise 3

Maintain `(slice_index, offset)`. Present remaining slices with the first adjusted by `offset`. On `written > 0`, subtract from the current remainder, advancing across completed slices. On interruption, retry. On terminal error, return the number already committed plus the error if the API needs recovery. On zero write without a documented nonblocking condition, treat as inability to progress rather than loop forever.

### Exercise 4

Honest: “MetricRail’s parser returns tenant and metric slices borrowing directly from one validated in-memory frame; no payload copy occurs between frame ownership and field inspection.” Refuse: “MetricRail is zero copy from TCP packet to durable snapshot,” because kernel/user transitions, aggregation ownership, encoding, and durable writes involve other copies or transformations.

## Part 4 — Laboratory review

`RecordWindow` should own the backing `Bytes` and store validated record ranges. Borrowed access derives slices from that owner, so lifetime ties are explicit. Promotion copies only the selected key and value representation, allowing the window to drop. Tests should cover empty input, malformed lines, maximum line length, ordering, and promoted records remaining valid after the window is gone.

## Part 5 — MetricRail transfer

The critical boundary is frame-to-aggregate state. Borrow during framing and validation, then allocate only when a new durable series identity is required. Existing series should be found using borrowed query keys. Snapshot output must be checked against its configured maximum before unbounded growth. The design document should celebrate intentional compact copies that release large transient buffers.

## Part 6 — Defense

A vector move transfers its handle. Shared views can retain their full backing allocation. Borrowed fields become owned when they cross the owner’s lifetime or task boundary. Partial writes require slice/offset state. Shared mutable buffers can add synchronization and prevent parallelism. Userspace claims do not erase kernel or durable-storage boundaries. Larger buffers and batches increase peak memory and retry/failure scope. A compact durable copy is correct when it breaks an oversized or unstable lifetime dependency.

## Deep reasoning and transfer

### Decisive model

> Where do bytes move, who owns them at each boundary, and when does avoiding a copy improve the whole system rather than merely relocate lifetime and retention cost?

Build a **byte journey**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Trace bytes across kernel, transport, framing, parsing, domain, storage, and response layers.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Distinguish copying bytes from moving ownership of a buffer handle.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Use slices, `bytes::Bytes`, and split/freeze operations while explaining their retention semantics.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Choose vectored I/O, scatter/gather, or coalescing from message shape and system-call cost.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Recognize when zero-copy parsing is incompatible with queueing, mutation, or independent retention.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Trace bytes across kernel, transport, framing, parsing, domain, storage, and response layers.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the byte journey.

### Reference implementation comparison

For [Borrowed Record Window](../../labs/module-04-borrowed-record-window/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In MetricRail, Module 84 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Data Movement, Buffering, and Zero-Copy Boundaries**, which relationship decides this question: “Where do bytes move, who owns them at each boundary, and when does avoiding a copy improve the whole system rather than merely relocate lifetime and retention cost?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to MetricRail?
