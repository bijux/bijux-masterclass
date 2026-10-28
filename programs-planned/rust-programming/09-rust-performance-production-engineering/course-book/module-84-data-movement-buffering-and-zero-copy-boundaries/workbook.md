# Module 84 Workbook — Data Movement, Buffering, and Zero-Copy Boundaries

[Chapter](index.md) · [MetricRail guide](../capstone.md) · [Solutions](solutions.md)

A “zero-copy” claim is meaningless until its endpoints are named. This workbook makes you trace bytes from producer to final owner and distinguish payload copies from moves, shared views, metadata copies, kernel transitions, and lifetime retention.

## Part 1 — Predict

### 1. Move, clone, and copy

A `Vec<u8>` is moved into a channel, a `Bytes` value is cloned, and a ten-byte `String` is created from a slice. For each operation, predict:

- whether payload bytes move;
- whether an allocation occurs;
- whether reference counting occurs;
- which allocation remains alive afterward.

### 2. A small slice of a large frame

A 16-byte tenant identifier is stored as `Bytes::slice` from an 8 MiB frame. One million identifiers are retained. Predict why the visible data size is not the retained memory size. Give two repair strategies with different copy/lifetime trade-offs.

### 3. Borrow across an async boundary

A parser returns fields borrowing a connection buffer. The fields are sent to a spawned task while the connection immediately reuses the buffer. Predict the compiler and product problem. Choose an ownership boundary that keeps the parser cheap without making the buffer immortal.

### 4. Vectored writes

A response consists of a header, body, and newline. `write_vectored` is called once. Predict what can be concluded if it returns fewer bytes than the total. Design the state needed to resume correctly across partial writes.

### 5. Coalescing

A team coalesces every response into one contiguous buffer “to reduce syscalls.” Predict when this helps and when it adds unnecessary allocation and copying. Name the measurements needed.

### 6. Kernel boundaries

A service receives bytes from a TCP socket into userspace, parses borrowed slices, and writes a snapshot file. Is the path zero copy? Answer using an explicit start and end boundary rather than a slogan.

## Part 2 — Diagnose and repair

### Case A — Shared backing-store leak

A parser stores tiny `Bytes` slices in a long-lived map. RSS grows in steps equal to complete request-frame sizes. Diagnose the mechanism and design an experiment that distinguishes backing-store retention from a map-entry leak.

### Case B — Copy removal creates aliasing pressure

A patch shares one mutable buffer among pipeline stages behind a mutex. Copies disappear, but contention and tail latency worsen. Explain why “fewer copies” did not imply less total work.

### Case C — Serialization buffer growth

A reusable output buffer grows to the largest snapshot and is never shrunk. Ordinary snapshots are small. Repair the design while avoiding a new allocation for every response.

### Case D — Miscounting ownership moves

A review counts moving a `Vec<u8>` into a function as a copy of all bytes and rejects the design. Correct the model and identify what still happens at the machine and lifecycle levels.

## Part 3 — Focused exercises

### Exercise 1 — Copy ledger

Trace one MetricRail record through:

```text
socket → connection buffer → frame → parsed fields → broker message → aggregate map → snapshot bytes → socket/file
```

For every arrow, label: borrow, move, shared view, payload copy, encoding, syscall/kernel transfer, or durable write. Also record the owner and release event.

### Exercise 2 — Promotion threshold

Design a policy deciding when a borrowed field becomes:

- a compact `String`;
- a `Bytes` view;
- an `Arc<str>`;
- an immediate aggregate lookup with no durable field.

Use field size, repetition, lifetime, backing allocation size, and sharing topology.

### Exercise 3 — Partial write machine

Write pseudocode for completing a vectored write after arbitrary short writes. It must advance across slices correctly, handle interruption, and distinguish retryable progress from terminal failure.

### Exercise 4 — Prove a narrow claim

Write one honest zero-copy claim for an in-memory parser and one claim you must refuse for an end-to-end network-to-disk path.

## Part 4 — Independent laboratory

Build the [Borrowed Record Window](../../labs/module-04-borrowed-record-window/README.md). The window owns `Bytes`; parsed records borrow from it; selected records can be promoted into compact owned values. Enforce line bounds before parsing, preserve record order, and prove that borrowed records cannot outlive the window. Add a test showing that promotion does not retain the original backing storage.

## Part 5 — Capstone transfer

Replace line-level `String` ownership with a bounded bytes-first ingestion path. Parsing should borrow transiently. The broker should receive only the compact state required for aggregation. Existing hot series should avoid new identifier allocations. Snapshot rendering should preflight output bounds and choose between direct buffered writing and bounded coalescing from evidence, not style preference.

Document the byte journey and mark every intentional copy. A copy with a clear ownership purpose is not a defect.

## Part 6 — Reconstruct and defend

1. Why is moving a `Vec<u8>` not a payload copy?
2. How can a 16-byte view retain 8 MiB?
3. When should borrowed fields become owned?
4. What must a partial-write loop remember?
5. Why can shared mutable buffers increase latency?
6. What are the limits of userspace zero-copy claims?
7. How do buffering and batching change failure scope?
8. Defend one copy that improves the whole system.

### Exercise 6 — Audit one byte journey end to end

Trace one input record from the operating-system read buffer through line framing, UTF-8 validation, field parsing, identifier validation, store insertion, and snapshot rendering. At every transition record the current owner, the borrowed view, the exact copy or allocation, the lifetime that ends the view, and the reason the transition exists. Mark each copy as required by ownership, required by representation, or accidental. Propose one removal, but also state the boundary that prevents extending the borrow safely. A credible answer may conclude that an owned copy is the correct cost because the stored identifier outlives the input buffer.

### Data-movement acceptance gate

Do not label an implementation “zero copy” unless you name the exact interval over which bytes are not copied. The review must include fragmentation, buffer compaction, retained backing storage, and worst-case frame size. A borrowed slice that pins a megabyte buffer to preserve a ten-byte field may reduce copying while increasing memory pressure; the complete cost model decides whether the change is an improvement.

