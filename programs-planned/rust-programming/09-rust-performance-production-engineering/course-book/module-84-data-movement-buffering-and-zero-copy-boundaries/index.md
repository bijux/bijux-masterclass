# Module 84 — Data Movement, Buffering, and Zero-Copy Boundaries

**Course 9 · Day 4 · Module 84 of 100**
`█████████████████████░░░░` **84/100**

[Program](../../../README.md) · [Course 9](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-04-borrowed-record-window/README.md) · [MetricRail guide](../capstone.md)

[← Module 83: Allocation, Memory Footprint, and Ownership Cost](../module-83-allocation-memory-footprint-and-ownership-cost/index.md) · [Module 85: Runtime Efficiency: Contention, Queueing, Batching, and Async Load →](../module-85-runtime-efficiency-contention-queueing-batching-and-async-load/index.md)

## The question

> Where do bytes move, who owns them at each boundary, and when does avoiding a copy improve the whole system rather than merely relocate lifetime and retention cost?

## Why this comes now

Module 83 established that ownership and lifetime determine memory cost. Module 84 follows the bytes as they cross buffers and APIs. “Zero copy” is frequently used without a boundary: it may mean no copy after a frame is in userspace, no copy while parsing, or no copy between application components. Those are different claims with different evidence.

The mature objective is not to minimize copy count unconditionally. It is to choose where ownership changes, how long backing storage remains live, and whether a copy reduces coupling, retention, fragmentation, or synchronization enough to be worthwhile.

### Prerequisite bridge

Module 83 established **Allocation, Memory Footprint, and Ownership Cost**. Before continuing, verify that you can set and verify a memory budget that includes steady state, burst behavior, and cleanup. This module preserves that capability and adds the ability to trace bytes across kernel, transport, framing, parsing, domain, storage, and response layers. Module 85, **Runtime Efficiency: Contention, Queueing, Batching, and Async Load**, will rely on both when it asks: *When work is correct and bounded, where do contention, waiting, scheduling, queueing, batching, and blocking determine throughput and tail latency?*

### Scope boundary

This module owns the reasoning for **data movement, buffering, and zero-copy boundaries** inside Course 9. The course teaches measurement and operational reasoning, not folklore optimization. It does not promise universal performance rankings, complete security proof, or production readiness from one green pipeline. Every conclusion is scoped to a workload, artifact, environment, and time. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

After completing this module, you will be able to:

- trace bytes across kernel, transport, framing, parsing, domain, storage, and response layers
- distinguish copying bytes from moving ownership of a buffer handle
- use slices, `bytes::Bytes`, and split/freeze operations while explaining their retention semantics
- choose vectored I/O, scatter/gather, or coalescing from message shape and system-call cost
- recognize when zero-copy parsing is incompatible with queueing, mutation, or independent retention
- define canonical ownership-transfer points where copying is deliberate and bounded
- test chunking, aliasing, lifetime, and backpressure behavior at data boundaries

## Core model

### The governing model

Use a byte journey: `origin → buffer → view → domain → sink`. At each arrow record whether bytes are copied, whether ownership moves, whether storage is shared, and what retains it. “Zero copy” is never a complete claim unless the start and end boundaries are named. The design goal is minimum justified movement under a comprehensible lifetime and memory budget, not the lowest possible copy count.

### 1. A copy ledger

Begin at the actual source. A file read or socket read usually transfers bytes into userspace storage. Framing may compact buffers. Parsing may create borrowed views. Domain conversion may allocate owned identifiers. Persistence or response generation may copy again. Count bytes and boundaries, not just calls to `clone`.


### 2. Ownership transfer is not byte copying

Moving a `Vec<u8>` or `Bytes` value transfers or shares a small handle; it does not duplicate the payload. Cloning `Bytes` creates another shared view, while cloning `Vec<u8>` duplicates elements. That difference matters, but shared views can retain a large backing allocation long after most bytes are irrelevant.


### 3. The `Bytes` lifecycle

`BytesMut` supports mutable accumulation. Freezing can produce immutable `Bytes`, and splitting can create views with shared ownership. These operations are useful for framed protocols and fan-out, yet they create retention relationships. A 20-byte slice may retain the entire frame allocation until all views drop.


### 4. Borrowed parsing boundaries

Borrowing fields from a frame is ideal when validation and consumption happen before the frame is reused or released. It becomes awkward when records enter queues, caches, or maps with longer lifetimes. A disciplined design parses into a borrowed record, validates, then promotes only durable fields into owned domain values.


### 5. Vectored I/O and coalescing

Scatter/gather operations can present multiple buffers to one system call. They help when a protocol naturally has headers and payloads or when combining them would allocate. They do not guarantee one physical copy or one syscall completion. Conversely, coalescing many tiny buffers can improve locality and simplify downstream code.


### 6. Copying can be the cheaper contract

One bounded copy can decouple lifetimes, release a huge source buffer, enable compact storage, simplify cancellation, and reduce synchronization. Measure end-to-end. A zero-copy design that pins buffers across queues or tenants may consume more memory and coordination than a deliberate copy.

A byte journey has two parallel histories: payload movement and ownership movement. Moving a `Vec<u8>` transfers a handle without copying payload bytes; cloning a shared `Bytes` handle may avoid copying while extending the backing allocation’s lifetime. A useful copy ledger records both histories rather than inferring one from the other.

### A module-specific decision table

| Boundary | Possible representation | Question before avoiding a copy |
|---|---|---|
| socket to connection buffer | mutable receive storage | is kernel-to-userspace transfer inside the claim? |
| frame to parsed fields | borrowed slices | can every field remain within the frame lifetime? |
| parsed record to queue | owned compact values or shared frame | which bytes must cross the task boundary? |
| queue to durable store | owned key and aggregate | would sharing retain unrelated payload bytes? |
| snapshot to response | formatted buffer or vectored pieces | how are partial writes and lifetimes handled? |
| cache or retry record | compact ownership | how long can the original frame remain live? |

### Working procedure

1. Choose the start and end of the claimed byte path.
2. Draw every buffer, slice, handle, and owner along that path.
3. Mark actual payload copies separately from moves, reference-count changes, and formatting.
4. Record retained backing size and lifetime for every shared view.
5. Test normal, fragmented, coalesced, and boundary-size input.
6. Compare the no-copy candidate with a compact-copy candidate on latency, peak memory, retained memory, and API complexity.
7. Keep the simpler copy when the local bandwidth saving does not improve the complete operation.

### Failure patterns and principled repairs

#### Claiming a parser is zero copy without naming whether the boundary starts at a userspace frame, a socket, or durable storage.

A zero-copy claim without a start and end boundary is unfalsifiable. Name the buffers and the exact copy that is absent.

#### Cloning a shared byte view for a small field and overlooking retention of the full backing allocation.

A small shared view can retain a large frame. Measure backing allocation lifetime, not only the handle size.

#### Borrowing every field even though the record must outlive the frame or cross a task boundary.

Borrowed fields cannot outlive their frame or cross arbitrary task boundaries. Promote only the durable fields before that boundary.

#### Coalescing blindly and adding an allocation to every small response.

Coalescing can simplify writes but allocates and copies every payload. Compare it with vectored or incremental output for the actual response sizes.

#### Using vectored I/O as if it guaranteed that the operating system accepts or transmits all slices in one operation.

Vectored I/O still permits partial progress and platform limits. The write loop must advance across slices correctly.

#### Counting ownership moves as payload copies or treating payload sharing as free of lifecycle cost.

Moving an owner is usually handle movement, while shared ownership can be cheap immediately but expensive in retention. Keep both ledgers separate.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For trace bytes across kernel, transport, framing, parsing, domain, storage, and response layers, construct one positive and one causal negative example. Mark the first decisive fact in the **byte journey** and state which evidence could falsify the claim.

2. **Outcome 2.** For distinguish copying bytes from moving ownership of a buffer handle, construct one positive and one causal negative example. Mark the first decisive fact in the **byte journey** and state which evidence could falsify the claim.

3. **Outcome 3.** For use slices, `bytes::Bytes`, and split/freeze operations while explaining their retention semantics, construct one positive and one causal negative example. Mark the first decisive fact in the **byte journey** and state which evidence could falsify the claim.

4. **Outcome 4.** For choose vectored I/O, scatter/gather, or coalescing from message shape and system-call cost, construct one positive and one causal negative example. Mark the first decisive fact in the **byte journey** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

```rust
use bytes::{Bytes, BytesMut};

fn split_frame(mut buffer: BytesMut, header_len: usize) -> Option<(Bytes, Bytes)> {
    if buffer.len() < header_len {
        return None;
    }
    let payload = buffer.split_off(header_len).freeze();
    let header = buffer.freeze();
    Some((header, payload))
}

fn main() {
    let buffer = BytesMut::from(&b"HEADpayload"[..]);
    let (header, payload) = split_frame(buffer, 4).expect("complete frame");
    assert_eq!(&header[..], b"HEAD");
    assert_eq!(&payload[..], b"payload");
}
```

Read the example by labeling every value with its backing allocation. When a slice is created, note that no payload bytes move but the slice cannot outlive its owner. When a `Bytes` view is cloned, note the reference-count action and the retained backing capacity. When a compact `String` is built, record the copy and the new independent lifetime.

Then change the workload: retain one 12-byte field from a 1 MiB frame for ten minutes. The locally “copy-free” design now has an obvious product cost. This counterexample is more educational than a rule that copying is either always bad or always acceptable.

### MetricRail consequence

MetricRail’s connection reader accumulates one bounded line, parses borrowed fields from that buffer, and promotes tenant and metric only after validation. The broker command owns the durable record; it does not retain the connection buffer. This is the principal data-movement decision of the service.

Document the payload path from socket to `BytesMut`, borrowed parse result, owned `Record`, `BTreeMap` key, cloned snapshot row, rendered `String`, and socket write. The guide deliberately avoids claiming kernel-level zero copy. Snapshot rendering performs explicit formatting copies because the stable response must outlive the store borrow and be bounded before transmission.

The load client now bounds response lines as well as request lines. This is an important boundary lesson: a benchmarking helper is still a network client and must not allocate unbounded memory from a hostile or misconfigured endpoint.

### Boundary case: partial writes defeat a simple copy count

Suppose snapshot output is represented as a header slice, one slice per row, and a footer slice. A vectored write appears to avoid coalescing all rows into one `String`. The design is not complete until it handles partial progress: the operating system may consume only part of one slice and none of the rest. The writer must advance both the slice index and the offset inside the current slice without duplicating or skipping bytes.

That state machine also affects lifetimes. Every referenced row must remain alive until the final byte is accepted or the operation fails. If the store remains borrowed during the complete network write, a slow client can block updates or retain a large snapshot. Cloning rows before writing releases the store but increases peak memory. Formatting into one bounded buffer makes failure and ownership simple at the cost of a copy.

MetricRail chooses the bounded buffer for the course material because the snapshot limit is explicit and the response can be validated before transmission. A vectored or streaming design is a valid later experiment, but its comparison must include partial-write correctness, store-borrow duration, slow-client behavior, and peak retained memory—not only the number of application copies.

## Practice sequence

1. Draw a copy ledger for MetricRail ingest and snapshot output.
2. In the Borrowed Record Window lab, prove which views remain valid after buffer mutation and which must become owned.
3. Measure a compact-copy and shared-view design across small fields in small and large backing frames.
4. Test fragmented reads, coalesced lines, maximum-size lines, and partial writes.
5. Record any lifetime complexity introduced by the lower-copy design.
6. Defend one intentional copy as a simplification of ownership, retention, or failure handling.

Use the [workbook](workbook.md) to freeze predictions and complete the causal repairs. Build the module laboratory before reading its reference implementation, then transfer the mechanism into the [MetricRail engineering guide](../capstone.md).

## Ready to continue

Continue only when you can:

- define a zero-copy claim with explicit start and end buffers;
- distinguish payload copying from ownership movement;
- calculate backing-memory retention for a shared view;
- identify the task or storage boundary that requires ownership promotion;
- explain partial-write obligations for vectored output;
- trace every MetricRail payload copy without claiming more than the implementation proves.

## Primary Rust references

- The `bytes` crate documentation for `Bytes`, `BytesMut`, splitting, freezing, and shared backing storage
- The Rust standard library documentation for slices, `Read`, `Write`, and vectored I/O
- Operating-system documentation when making claims about kernel copying or scatter/gather behavior

These references are for verification and deeper lookup after the chapter’s model is understood. The course-book chapter remains the complete learning route for the required concepts.

## Continue

Continue to [Module 85 — Runtime Efficiency: Contention, Queueing, Batching, and Async Load](../module-85-runtime-efficiency-contention-queueing-batching-and-async-load/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
