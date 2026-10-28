---
module_id: SEPAT-072
program: Software Engineering: Patterns
level: 2
module_number: 72
title: Proactor
status: complete
last_verified: 2026-08-29
---

# Proactor

## One-Page Review

### Governing question

How can an application initiate many asynchronous operations and process their completions without blocking threads while preserving operation identity, buffer lifetime, cancellation races, partial results, ordering, bounded outstanding work, and exactly one logical terminal handling path?

### Essential definitions

- A **Proactor** dispatches completion events for asynchronous operations that an operating system, runtime, or delegated processor has already attempted.
- An **asynchronous operation processor** accepts an operation description, performs or arranges the work, and records a completion result.
- A **completion demultiplexer/queue** aggregates terminal or progress records from many operations and lets dispatch threads wait for them.
- A **completion handler** interprets an operation result and advances application/protocol state; it does not perform the original I/O merely because readiness was reported.
- An **operation context/control block** binds stable operation ID, owner/generation, buffer/resources, requested action, deadline, cancellation state, and handler.
- **in flight** means accepted for asynchronous processing but not yet terminally reaped by the application.
- A **short completion** reports fewer bytes/items than requested; it can be successful progress rather than failure or whole-message completion.
- A **composed operation** chains primitive asynchronous operations to provide a higher-level contract such as “read exactly one frame.”
- **cancellation request** asks the processor to stop or alter an operation; success is a race-dependent outcome, not retroactive proof that no effect occurred.
- **logical completion exactly once** means application state consumes one terminal outcome per operation identity even if notifications, retries, or wrapper paths duplicate.

### Central model, mechanism, or theorem

For operation \(o\), use lifecycle

\[
created\rightarrow submitted\rightarrow in\_flight\rightarrow completing\rightarrow terminal,
\]

with cancellation as an orthogonal request flag. Exactly one transition wins from `in_flight` to terminal result

\[
R_o\in\{success(n),eof,error(e),cancelled,timeout\},
\]

and every completion notification is deduplicated by \((owner,generation,operation\_id)\). Cancellation and deadline do not overwrite a success that already won; the handler observes the actual result and reconciles external effects.

If accepted operation rate is \(\lambda\) and mean in-flight duration \(W\), Little's Law gives average outstanding work

\[
N=\lambda W
\]

under a stable measured system. Submission slots, completion capacity, buffers, downstream limits, and handler service must be sized above bursts/tails yet bounded; otherwise asynchronous initiation only relocates overload.

### Critical invariants

- Every accepted operation has stable ID, owner/generation, one terminal-result cell, buffer/resource ownership, deadline, handler, and observable lifecycle.
- Initiation distinguishes rejected, completed-inline, and pending outcomes and normalizes them to exactly one logical completion path.
- Input/output buffers and referenced control data remain valid, immutable or exclusively owned as required until the platform's terminal completion contract permits release/reuse.
- Completion order is never inferred from submission order; sequence-dependent effects use explicit operation/entity ordering and serialization.
- Short reads/writes, EOF, zero progress, errors, and platform-specific flags are interpreted by the operation contract, not collapsed into Boolean success.
- Cancellation, timeout, close, and completion races always reap terminal evidence; late/stale results are generation-checked and cannot mutate a new owner.
- Outstanding submissions, bytes, completion backlog, composed steps, executor work, and downstream effects are bounded with admission/backpressure.
- Completion handlers perform bounded nonblocking work or offload it; a blocked completion dispatcher delays unrelated terminal processing and resource release.
- Multi-threaded completion dispatch preserves per-owner serialization through affinity, strands, locks, actors, or explicit partitioning.
- Shutdown stops admission, requests cancellation where appropriate, drains/reaps or explicitly abandons under a proven API contract, releases resources, and records unresolved effects.

### Common failures

Common failures include calling an API “Proactor” when handlers still perform readiness I/O, reusing a buffer after submission, stack-allocating operation state, assuming cancellation prevents completion, freeing on timeout before the original operation is reaped, handling inline and queued completion twice, ignoring initiation failure because a callback was expected, treating short I/O as a complete frame, assuming FIFO completion, issuing dependent writes concurrently, unbounded outstanding operations, completion-queue overflow, blocking/throwing handlers, concurrent handlers corrupting one connection, descriptor/handle reuse without generation, close without draining, retrying an ambiguous write with new identity, and measuring submission throughput while completions/resources accumulate.

### Compact example

Two operations are submitted with owned buffers. Cancellation is requested for both. `write-1` completes successfully first with four bytes—the cancellation lost, so the success/effect must be honored. `read-1` later completes cancelled. A duplicate `write-1` notification is ignored by its terminal cell. Both buffers are released only after their actual terminal completions.

### Connections

[SEPAT-071](071-reactor.md) contrasts readiness-driven handling; [SEPAT-073](../ROADMAP.md) adds a synchronous worker layer behind an asynchronous boundary. Proactor also connects to [Operating Systems](../../22-operating-systems/ROADMAP.md), [Network Engineering](../../24-network-engineering/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), and [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

When the operating system or runtime can own the progress of I/O after submission, how should the application represent, bound, cancel, complete, and retire each operation without confusing notification, state mutation, and resource lifetime?

Proactor inverts the Reactor responsibility. A Reactor says “the handle may be ready; attempt the operation.” A Proactor says “the requested operation reached a completion condition; here is its result.” This can reduce readiness state machinery and use kernel completion facilities efficiently. It makes operation lifetime, buffer ownership, result correlation, and cancellation semantics central.

## Why This Matters

File servers, databases, proxies, high-throughput storage, Windows servers, Linux `io_uring` applications, and cross-platform asynchronous libraries can keep many operations in flight without one blocked thread per operation. Submission and completion batching can reduce transitions and improve utilization.

Asynchrony also expands the interval during which application memory and authority are loaned to another processor. An operation may complete inline or later, after cancellation or close, and out of order relative to peers. If the completion queue is not drained, buffers and slots remain occupied even though devices finished. Production quality depends on a precise operation state machine rather than callback familiarity.

## Prerequisites and Retrieval

You should understand nonblocking and asynchronous I/O, buffers/pointers, ownership/lifetimes, queues, memory ordering, partial stream I/O, cancellation, deadlines, idempotency, backpressure, and Reactor. Retrieve these facts:

1. Submission acceptance is not operation success; immediate initiation failure may produce no later completion under some APIs.
2. An asynchronous operation can complete before the initiating function returns or enqueue a later record depending on abstraction.
3. TCP and file operations can complete with fewer bytes than requested while still succeeding.
4. Multiple independent operations may complete in any order even when submissions were ordered.
5. Cancellation races with normal completion and often produces a terminal completion that must still be observed.
6. Buffer/control-block lifetime rules differ by operation, platform, registration mode, and library version.
7. Bounded completion processing is part of resource safety: completed-but-unreaped operations still consume application/kernel state.

## Learning Objectives

After completing this module, you should be able to:

- identify Proactor participants and trace initiate, accept/reject, progress, completion enqueue, dispatch, and retirement;
- distinguish operation acceptance, inline completion, pending state, progress/short result, terminal completion, handler completion, and business effect;
- design operation contexts with stable identity, generation, buffers, deadlines, cancellation, handler, and terminal deduplication;
- normalize synchronous/inline and queued results without double completion or lost errors;
- handle partial reads/writes and compose higher-level operations under byte, step, time, and memory bounds;
- reason about cancellation/timeout/close races and stale results without premature resource release;
- bound submission/completion rings, in-flight bytes, per-owner concurrency, downstream effects, and dispatch work;
- preserve per-connection/entity ordering with multi-threaded completion dispatch;
- compare native completion, readiness-backed emulation, thread-pool offload, Reactor, and synchronous alternatives;
- verify through deterministic state models, platform integration, short/out-of-order completions, cancellation races, saturation, shutdown, security, and recovery.

## Core Exposition

### Identify the participants

The initiator creates an operation context and calls an asynchronous operation. The asynchronous operation processor accepts or rejects it and performs the operation. On completion, it places a result plus correlation on a completion queue/demultiplexer. The Proactor waits for results and dispatches the associated completion handler, which advances application state and may initiate subsequent operations.

The operation context is durable control state, not incidental callback capture. It includes logical owner, lifecycle generation, operation ID/type, handle, buffer segments and ownership, requested/actual bytes, sequence, deadline/timer, cancellation state, completion cell, trace, and cleanup actions.

### Normalize initiation outcomes

APIs vary: initiation can fail immediately; complete synchronously; or report pending and complete later. Some abstractions guarantee that a handler is never invoked inline; others may invoke or resume immediately. Document the contract and create one normalization layer.

Reserve operation identity/resources before initiation. On immediate rejection, transition through the same logical terminal handler or an explicitly equivalent path exactly once. If inline success also later queues a notification under a platform option, deduplicate. Never assume every non-success return means pending or every accepted call guarantees a callback without checking official semantics.

### Own buffers through terminal completion

The processor may read from or write into application memory after initiation returns. Buffers must remain allocated, correctly aligned/registered where required, and not mutated/reused concurrently until terminal completion permits release. The operation context and buffer lifetime should be tied structurally.

For a receive, exclusive mutable ownership normally transfers to the in-flight operation and returns with the result. For a transmit, immutable bytes must remain stable. Registered/fixed buffer pools reduce allocation and registration overhead but need generation, leasing, quotas, zeroing/classification policy, and completion-driven return.

### Interpret completion results precisely

A completion contains operation-specific result: bytes/items, EOF, cancellation, timeout, error code, flags, peer/address, or more-progress indication. Successful zero bytes can have distinct meanings by operation. Do not reduce the result to `ok` before protocol logic sees it.

One primitive read does not equal one frame, and one write need not consume all bytes. Advance offsets and issue the next primitive operation only while the composed contract, deadline, pressure, and owner generation remain valid.

### Build bounded composed operations

A composed “read frame” may submit header read(s), validate length, allocate/lease bounded storage, then submit body read(s). It owns the chain and exposes one logical completion. Enforce maximum primitive steps, bytes, duration, retries, and memory. Preserve partial evidence for diagnosis without leaking sensitive content.

Cancellation of a composed operation must coordinate the currently in-flight primitive and prevent a completed earlier step from starting the next after cancellation/deadline. The outer terminal cell wins once; all primitive completions are still reaped and resources released.

### Expect out-of-order completion

Device/runtime scheduling, parallelism, caching, network conditions, and dispatcher threads can reorder independent completions. Use operation IDs and explicit sequence dependencies. If protocol requires ordered writes, allow one write in flight per stream or use a serializing queue whose next operation begins only after the prior result.

Do not infer business event order from completion dequeue order. Completion ports may queue in one order but dispatch/dequeue across threads differently; application effects require their own ordering/conditional state.

### Treat cancellation as a race

Requesting cancellation means “attempt to cancel subject to API scope and state.” The original operation may already have completed, may complete partially/successfully, may return a cancellation result, or may be uncancellable. The application must observe the actual terminal result.

Record `cancel_requested` separately from `result`. A normal success after cancellation request is still success and may have external effects. Do not free buffers or start a conflicting replacement until terminal completion establishes ownership return. Cancellation API success often says the request was issued, not that no completion will arrive.

### Implement deadlines as competing outcomes

A timer and operation completion race. Whichever first claims the logical terminal decision may request cancellation or accept success according to policy, but the underlying operation still must be reaped. Distinguish deadline-exceeded business outcome from the eventual kernel result used for cleanup/reconciliation.

Use monotonic time. A result arriving after deadline may be ignored for response yet still show bytes were transmitted or a file write completed; external effects need idempotency, versioning, compensation, or reconciliation.

### Guarantee one logical completion

Use an atomic/serialized terminal cell keyed by owner/generation/operation. Every path—immediate error, inline result, queued completion, timeout, cancellation, close, duplicate wrapper notification—attempts one transition. The winner schedules application handling; losers contribute diagnostics/cleanup only.

“Exactly once” here is local state consumption, not exactly-once I/O or business effect. A write can succeed while its completion is delayed or process crashes. Durable remote effects require their own protocol.

### Bound outstanding operations

Limit in-flight operation count and bytes globally, per connection/tenant, per operation type, and per downstream resource. Submission queues/rings have finite entries; buffer pools and kernel pinned memory are finite. When capacity is unavailable, pause upstream admission/read/production, queue only within a bound, reject, or shed under explicit semantics.

Little's Law connects throughput, duration, and outstanding work. Tail latency and hung devices make average sizing unsafe; deadlines, circuit breakers and conservative headroom matter. Submission batching can improve throughput but increases burst size, cancellation scope, and completion pressure.

### Drain completion capacity

Completion queues/rings are finite or consume finite memory. Dispatch must keep pace, acknowledge/reap entries according to API, and return buffers/slots promptly. A blocked completion handler can cause queue overflow or resource deadlock even though I/O devices are healthy.

Separate fast result harvesting from application work if necessary: copy minimal result metadata into a bounded owned queue, release platform entries, then dispatch. But do not release operation buffers until copied/ownership rules permit. Monitor overflow/dropped indicators and treat any possible lost completion as correctness-critical.

### Keep handlers bounded

Completion handlers validate owner/generation, interpret result, advance a small state machine, schedule the next operation or bounded worker task, release resources, and return. CPU-heavy parsing, blocking database calls, synchronous logging, user callbacks, or locks stall other completions.

If handlers run on multiple threads, use stable affinity/strand per connection or protect state explicitly. A concurrency setting limits active dispatcher threads, not downstream concurrency automatically. Handler code must be safe if one completion initiates an operation that completes inline.

### Close and shut down safely

Stop admission, mark owner closing and reject new operations, request cancellation where useful, continue draining terminal results, prevent completions from starting new chains, and release each resource once. Set a shutdown deadline and define behavior for operations whose platform cannot cancel promptly.

Closing a handle does not universally mean all completion records vanish. Keep contexts until the documented contract says they are done. In process termination, durable application effects and recovery ledgers, not memory cleanup, decide what remains unresolved.

### Map implementations without erasing semantics

Windows I/O completion ports are native completion facilities for overlapped operations. Linux `io_uring` exposes submission and completion queues with operation correlation in user data. Cross-platform libraries may implement a Proactor interface over native completions, readiness plus nonblocking calls, or a thread pool for file/DNS work.

The abstraction can be useful, but cancellation, inline completion, buffer stability, supported operations, ordering, threading, and error behavior remain backend-specific. Verify the deployed backend instead of generalizing from the API surface.

### Compare with Reactor and offload

In Reactor, readiness arrives and handler performs I/O. In Proactor, operation is initiated before waiting and completion carries its result. Thread-pool offload can emulate asynchronous completion but uses blocked worker threads and inherits their capacity/cancellation semantics. A coroutine/future can sit atop any of these.

Choose based on operation support, buffer ownership, platform portability, cancellation, workload, observability, and team correctness—not callback versus `await` syntax.

### Secure the operation plane

Untrusted peers can cause many long-lived reads, tiny completions, pinned buffers, expensive composed chains, cancellation churn, or output stalls. Authenticate/admit, limit operation/byte/deadline per identity, validate lengths before buffer leasing, cap registered/pinned memory, and isolate tenants.

Zero or reclassify pooled buffers before reuse across security domains. Avoid raw pointers, secrets, or personal data in externally visible completion correlation/telemetry. Validate completion metadata and control commands at trust boundaries.

### Observe and verify

Measure initiation attempted/accepted/rejected/inline/pending, in-flight count/bytes/age, submission occupancy, completion occupancy/lag/batch/overflow, operation duration/result/short count, cancel requested/result/race, timeout versus eventual result, composed steps, buffer pool use/age, handler duration, stale/duplicate result, per-owner ordering, and shutdown residue.

Test immediate failure, inline and delayed completion, every short length including zero, EOF/errors, out-of-order results, duplicate notification, cancel before/during/after completion, timeout race, close/handle reuse, buffer mutation/reuse sentinels, submission/CQ/buffer saturation, handler blocking/exception, multi-thread dispatch, process crash/recovery, backend variation and graceful/forced shutdown.

## Definitions and Notation

| Symbol or term | Meaning |
| --- | --- |
| \(o\) | One logical asynchronous operation identity |
| \(R_o\) | Actual terminal result of operation \(o\) |
| \(B_o\) | Buffers/resources loaned to \(o\) until terminal ownership return |
| \(g_o\) | Owner lifecycle generation recorded at submission |
| \(\lambda\) | Accepted operation rate under a measured stable workload |
| \(W\) | Mean in-flight duration from acceptance to terminal completion |
| \(N\) | Mean number of outstanding operations, \(N=\lambda W\) |
| SQ/CQ | Submission queue and completion queue |
| short completion | Successful result with less progress than requested |
| terminal cell | Serialized/atomic record admitting one logical terminal transition |
| composed operation | Higher-level contract implemented by several primitive asynchronous operations |

Little's Law is an accounting relationship under stable long-run conditions; it does not prove finite tails, independence, capacity, or liveness. Cancellation is a request dimension, not a terminal result by itself.

## Mechanisms, Invariants, or Proof Structure

### Terminal uniqueness argument

Assume every path resolves stable `(owner,generation,operation)` and performs an atomic compare-and-set from nonterminal to one result. At most one path succeeds, so application terminal handling runs at most once. Cleanup paths for duplicate/late notifications remain idempotent. The argument does not prove the operation/effect occurred once.

### Buffer-lifetime argument

Assume buffer lease \(B_o\) is acquired before submission, inaccessible for conflicting reuse while operation is accepted/in flight, and released only after the platform terminal contract is reaped. Then the processor cannot validly access memory already reassigned through this path. Unsafe pointers, undocumented APIs, process termination and device/DMA defects are outside the argument.

### Cancellation-race argument

Cancellation request and normal completion compete, but neither frees resources. The actual platform terminal result is always observed. Application policy may decide timeout/cancel response earlier, while cleanup/reconciliation processes later success/error. Thus a late success is not misclassified as “never happened,” and state mutation is generation/idempotency guarded.

### Executable finite model

The model submits two buffer-owning operations, requests cancellation, delivers completions out of order, shows one cancellation losing to success, and ignores a duplicate terminal notification. It does not perform I/O, threads, atomic instructions, deadlines, partial chains, or durable effects.

<!-- bijux-verify: {"id":"proactor-completion-races","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"submitted=read-1,write-1 in_flight=2\ncancel=read-1,write-1 requested=2\ncompletion=write-1 outcome=success bytes=4 cancel_lost=True\ncompletion=read-1 outcome=cancelled bytes=0 cancel_lost=False\nduplicate=ignored terminal=2 buffers_released=True\n","stderr":""}} -->
```python
class Proactor:
    def __init__(self):
        self.operations = {}
        self.terminal = {}

    def submit(self, operation_id, buffer_data):
        self.operations[operation_id] = {
            "state": "in_flight",
            "buffer": buffer_data,
            "cancel_requested": False,
        }

    def request_cancel(self, operation_id):
        self.operations[operation_id]["cancel_requested"] = True

    def complete(self, operation_id, outcome, byte_count):
        operation = self.operations[operation_id]
        if operation["state"] == "terminal":
            return "ignored", False
        operation["state"] = "terminal"
        cancel_lost = operation["cancel_requested"] and outcome == "success"
        self.terminal[operation_id] = {"outcome": outcome, "bytes": byte_count}
        operation["buffer"] = None
        return outcome, cancel_lost


proactor = Proactor()
proactor.submit("read-1", bytearray(8))
proactor.submit("write-1", b"data")
print(f"submitted=read-1,write-1 in_flight={len(proactor.operations)}")

proactor.request_cancel("read-1")
proactor.request_cancel("write-1")
requested = sum(item["cancel_requested"] for item in proactor.operations.values())
print(f"cancel=read-1,write-1 requested={requested}")

outcome, cancel_lost = proactor.complete("write-1", "success", 4)
print(f"completion=write-1 outcome={outcome} bytes=4 cancel_lost={cancel_lost}")
outcome, cancel_lost = proactor.complete("read-1", "cancelled", 0)
print(f"completion=read-1 outcome={outcome} bytes=0 cancel_lost={cancel_lost}")

duplicate, _ = proactor.complete("write-1", "success", 4)
released = all(item["buffer"] is None for item in proactor.operations.values())
print(f"duplicate={duplicate} terminal={len(proactor.terminal)} buffers_released={released}")
```

## Alternatives and Trade-Offs

| Design | Advantage | Cost or limitation | Best fit |
| --- | --- | --- | --- |
| Native Proactor/completion | Processor owns progress; efficient batching | Buffer/cancel/backend complexity | Supported high-concurrency I/O |
| Reactor/readiness | Broad portable readiness semantics | Handler performs incremental I/O | Network handles and explicit state control |
| Blocking thread per flow | Straight-line resource lifetime | Thread/scheduling scale and cancellation | Bounded concurrency or validated virtual threads |
| Bounded blocking pool | Simple facade for unsupported async operations | Workers block; pool is capacity boundary | File/DNS/legacy APIs |
| Coroutine/future facade | Sequential-looking composition | Hides backend/inline/cancel/lifetime unless documented | Application ergonomics over a sound runtime |
| One completion thread | Serialized state and simple ownership | One-thread handler bottleneck | Moderate loads or fast handlers |
| Completion thread pool | Scales handler processing | Per-owner races/order and locks/affinity | Independent operations with serialization plan |
| Fixed/registered buffers | Lower registration/allocation overhead | Pinned memory, pool exhaustion and data hygiene | Measured high-throughput stable buffer classes |

Batching submissions/completions amortizes overhead but increases latency variance and burst resource use. Polling can reduce latency at continuous load while wasting CPU when idle. Select only after workload and power/cost evidence.

## Failure Modes and Misconceptions

- **“Async means Proactor.”** Some async facades use readiness or blocking workers; inspect who performs the operation.
- **“Accepted means successful.”** It means responsibility for later result under the API contract.
- **“The callback always comes later.”** Completion may be inline or scheduled according to abstraction.
- **“Cancel succeeded, so no bytes moved.”** Normal/partial completion may have won; observe the result.
- **“Timeout frees the buffer.”** The original operation may still access it until terminally reaped.
- **“One completion equals one application message.”** Short stream operations need composition/framing.
- **“Submission order gives completion order.”** Parallel operations can finish/dequeue/dispatch out of order.
- **“FIFO completion queue preserves handler order.”** Multiple dispatcher threads and platform rules can reorder observation.
- **“Completion exactly once means effect exactly once.”** It is local notification handling, not external effect uniqueness.
- **“Unlimited in-flight improves throughput.”** It consumes slots, buffers, pinned memory, device/downstream capacity and tail latency.
- **“The kernel owns cleanup.”** The application must reap completions and release contexts/buffers.
- **“Close cancels everything uniformly.”** Close/cancel/completion semantics vary by API and operation.
- **“Await removes lifetime races.”** Compiler/runtime state machines still own buffers, cancellation and resumption context.
- **“A completion handler may block because I/O is done.”** It stalls resource retirement and unrelated completions.
- **“Cross-platform API means identical guarantees.”** Backends can differ in support, cancel, inline behavior and buffer rules.

## Worked Examples

### Example 1

**Situation.** An async read can fail immediately for an invalid handle, complete inline from cache, or return pending.

**Reasoning.** Allocate operation ID/context before initiation. Normalize all three outcomes into one terminal cell and handler scheduling contract. Immediate rejection must release ownership; inline completion must not also be consumed from a later wrapper event unless deduplicated; pending retains resources.

**Conclusion.** One logical completion path must cover every initiation outcome defined by the API.

### Example 2

**Situation.** A 12-byte header read completes successfully with 5 bytes.

**Reasoning.** Advance composed offset to 5, retain the buffer, and submit another bounded read for 7 bytes while owner/generation/deadline remain valid. Do not parse an incomplete header or label success as a whole frame.

**Conclusion.** Primitive success can be partial progress inside a composed operation.

### Example 3

**Situation.** Two writes for one TCP stream are submitted concurrently; the second completion arrives first.

**Reasoning.** Completion order cannot define stream composition. If ordering is required, keep one write in flight and initiate the next from completion, or use an API with explicitly verified linked/ordered semantics. Buffers remain independently owned until each result.

**Conclusion.** Sequence-dependent operations require explicit serialization beyond completion correlation.

### Example 4

**Situation.** Cancellation is requested after a four-byte write already completed in the device/runtime but before the application dequeues its result.

**Reasoning.** Cancellation cannot erase the write. The completion reports success; application records cancel-lost, releases buffer, and reconciles protocol/business state. Retrying under a new identity could duplicate an effect.

**Conclusion.** Cancellation expresses intent to stop future progress, not historical rollback.

### Example 5

**Situation.** A deadline timer fires while a database/file operation is completing.

**Reasoning.** One logical response cell may choose timeout, request cancellation, and stop downstream chaining. The actual operation completion must still be reaped. A late success updates reconciliation/effect state even if no success response is returned.

**Conclusion.** Separate client/business deadline outcome from platform cleanup and effect truth.

### Example 6

**Situation.** A buffer pool returns a receive buffer immediately after cancellation request; another tenant leases it before the old read completes.

**Reasoning.** The old processor may write into new tenant memory, causing corruption/disclosure. Keep lease until terminal cancellation/success/error is observed, then sanitize according to classification and increment slot generation before reuse.

**Conclusion.** Completion, not cancellation request, returns buffer ownership.

### Example 7

**Situation.** The application submits 4,096 operations into a ring but processes completions slowly while doing CPU work.

**Reasoning.** CQ occupancy grows; completed operations retain contexts/buffers and may overflow/drop according to platform behavior. Keep harvesting bounded and fast, offload CPU work, size CQ with tail/burst evidence, cap submissions, and alert before saturation.

**Conclusion.** Submission capacity and completion service form one closed resource loop.

### Example 8

**Situation.** Four completion threads update the same connection parser concurrently.

**Reasoning.** Completed reads/timers/writes can interleave and corrupt state despite correct I/O. Assign connection completions to one strand/loop or guard explicit state and ordering. Avoid holding locks across user/blocking work.

**Conclusion.** Completion concurrency needs an application ownership policy.

### Example 9

**Situation.** A cross-platform library uses native completion on Windows, readiness on one Unix backend, and worker threads for file I/O.

**Reasoning.** The facade may consistently schedule handlers, but buffer rules, cancellation strength, resource cost and inline/error paths differ. Write contract tests for every deployed backend and expose unsupported/weaker guarantees.

**Conclusion.** Portable syntax does not create portable operational semantics.

### Example 10

**Situation.** A clinical archive submits asynchronous encrypted-record writes; shutdown requests cancellation after an acknowledgement was sent upstream.

**Reasoning.** Upstream acknowledgement before durable write completion is unsafe. Buffer/key/context remain until terminal result; cancellation may lose to success or leave ambiguity. Record stable operation ID, verify durable completion contract, publish/ack afterward, and reconcile shutdown residue under privacy/key controls.

**Conclusion.** High-stakes completion must align transport acknowledgement with durable effect evidence, not submission.

## Cross-Program Connections

- [Operating Systems](../../22-operating-systems/ROADMAP.md): asynchronous syscalls, queues, memory mapping, DMA, handles and scheduler semantics implement the processor.
- [Network Engineering](../../24-network-engineering/ROADMAP.md): stream partial I/O, ordering, close/reset and flow control define operation results.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): ambiguous effects, deadlines, idempotency and reconciliation extend beyond local completion.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): request deadlines, response lifecycle, cancellation and overload connect operation state to service contracts.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): ring sizing, pinned-memory limits, handler pools, telemetry, draining and backend qualification make Proactors operable.
- [SEPAT-071](071-reactor.md) contrasts readiness; [SEPAT-073](../ROADMAP.md) inserts bounded queues between async and blocking layers.

## References

1. Schmidt, Douglas C., Michael Stal, Hans Rohnert, and Frank Buschmann. *Pattern-Oriented Software Architecture, Volume 2*. Wiley, 2000. Proactor and related concurrency patterns.
2. Lavender, Irfan, and Douglas C. Schmidt. “Active Object: an Object Behavioral Pattern for Concurrent Programming”; and Proactor pattern materials collected in POSA2/ACE literature.
3. Microsoft. “I/O Completion Ports.” Win32 documentation. <https://learn.microsoft.com/en-us/windows/win32/fileio/i-o-completion-ports>. Accessed 2026-08-29.
4. Microsoft. “Synchronous and Asynchronous I/O.” Win32 documentation. <https://learn.microsoft.com/en-us/windows/win32/fileio/synchronous-and-asynchronous-i-o>. Accessed 2026-08-29.
5. Kerrisk, Michael. “io_uring(7).” Linux manual page. <https://man7.org/linux/man-pages/man7/io_uring.7.html>. Accessed 2026-08-29.
6. Kerrisk, Michael. “io_uring_enter(2).” Linux manual page. <https://man7.org/linux/man-pages/man2/io_uring_enter.2.html>. Accessed 2026-08-29.
7. Boost C++ Libraries. “Core Concepts and Functionality: The Proactor Design Pattern.” Current Boost.Asio documentation. <https://www.boost.org/latest/doc/html/boost_asio/overview/core.html>. Accessed 2026-08-29.
8. libuv. “Design overview,” version 1.x documentation. <https://docs.libuv.org/en/v1.x/design.html>. Accessed 2026-08-29.
9. Stevens, W. Richard, Bill Fenner, and Andrew M. Rudoff. *UNIX Network Programming, Volume 1*, 3rd ed. Addison-Wesley, 2003.
10. Kerrisk, Michael. *The Linux Programming Interface*. No Starch Press, 2010.
11. IETF. *RFC 9293: Transmission Control Protocol (TCP)*. August 2022. <https://www.rfc-editor.org/rfc/rfc9293>.
12. Gregg, Brendan. *Systems Performance*, 2nd ed. Addison-Wesley, 2020. Throughput, latency, utilization and queueing evidence.

Submission/completion, inline behavior, queue sizing, buffer stability, supported operations, cancellation, ordering and close semantics change by OS, kernel, runtime, library and configuration. Current official sources were checked on 2026-08-29; verify every deployed backend.

## Exercises

### Exercise 1

Name the Proactor participants and distinguish operation acceptance, pending state, short progress, terminal completion, completion-handler return, and business effect.

### Exercise 2

A stable service accepts 20,000 operations/s with mean in-flight duration 4 ms. Use Little's Law to estimate average outstanding operations. If each owns 16 KiB, estimate average buffer bytes. Explain why these averages cannot size the production limits alone.

### Exercise 3

Design a composed asynchronous “read exactly one length-prefixed frame” operation with a 2 MiB maximum, 3-second deadline, cancellation, fixed buffer pool, owner generation, and one logical completion. Cover immediate/inline/pending and every primitive result.

### Exercise 4

Diagnose a server that submits unlimited writes, reuses buffers after requesting cancellation, assumes FIFO completion across four threads, performs database calls in handlers, and closes without draining. Provide remediation and verification.

### Exercise 5

Design a Proactor-based controller for durable emergency-flight telemetry recording. Address identity, buffers, batching, ordering, deadlines/cancellation, durable acknowledgement, encryption, pressure, backend failover, shutdown/crash recovery, observability, and required external evidence.

## Answers to the Exercises

### Answer 1

The initiator builds context and requests work from the asynchronous operation processor. Acceptance means the processor/runtime owns responsibility for a later result under its contract; pending means no terminal result yet. Short progress is a successful primitive result with fewer units than requested and may continue a composed operation. Terminal completion is success/EOF/error/cancel/timeout evidence returned through the completion demultiplexer. The Proactor dispatches its completion handler; handler return means local bounded state processing ended. A business effect may require durable file/database/remote semantics and reconciliation beyond all of these.

### Answer 2

Little's Law gives

\[
N=\lambda W=20{,}000\times0.004=80
\]

average outstanding operations. Average owned buffer memory is

\[
80\times16\text{ KiB}=1280\text{ KiB}=1.25\text{ MiB}.
\]

Production limits require arrival/duration tails, bursts, correlations, operation mix, composed steps, CQ/SQ sizes, buffer fragmentation/registration, metadata, retries, device stalls, handler delay, tenant fairness and recovery headroom. Little's Law assumes stable averages and does not bound percentiles or prove capacity.

### Answer 3

Create outer context `(owner_id,generation,operation_id)` with atomic terminal cell, monotonic 3-second timer, cancel flag, header offset, body offset, leased-buffer IDs and cleanup. Before each primitive submission verify current owner/generation/nonterminal/deadline. Normalize immediate rejection, inline result and pending to one primitive-result path. Read fixed header incrementally: positive short results advance; zero means EOF policy; cancellation/error terminates; `would block` is normally hidden by true async backend but backend-specific pending is handled.

After full header, validate encoding and length `0..2 MiB` before leasing body buffers. If pool unavailable, apply bounded admission rather than unbounded allocation. Read body through as many short completions as needed with maximum step/byte/time bounds. When complete, validate frame and attempt outer success once. Timer attempts timeout once and requests cancellation of current primitive; it does not release buffers. Cancel/close prevents new primitives. Every later primitive result is reaped, generation-checked, cannot win the outer cell twice, and releases only its owned resources. Return pooled buffers after all relevant terminal contracts, sanitizing/incrementing slot generation. Tests cover all split points, zero/EOF, immediate/inline/pending, error, cancel/timeout races, duplicate/late completion, close/reuse, pool exhaustion and oversized/malformed length.

### Answer 4

Unlimited writes exhaust SQ/CQ entries, buffers, pinned memory and peer/downstream capacity. Cancellation request does not return buffer ownership, so reuse corrupts data. Completion order across threads is not submission order; database calls stall completion draining; close can leave terminal records/resources unresolved. Bound in-flight writes/bytes per connection/tenant/global and one ordered write per stream unless verified ordering primitives exist. Propagate output high/low-watermark pressure upstream.

Lease immutable buffers until actual terminal completion, then sanitize/recycle with generation. Assign each connection to a strand/affinity or serialize its results. Keep handlers small; submit database work to a bounded owned executor/workflow with operation/generation/idempotency. Shutdown stops admission, marks closing, requests cancel, drains/reaps, blocks new chains, and records ambiguous durable effects before deadline/forced policy.

Measure submission acceptance/rejection, in-flight age/bytes, SQ/CQ occupancy/overflow, short/error results, handler duration, DB queue, cancellation outcomes, stale/duplicate completions and shutdown residue. Test buffer sentinels, out-of-order results, four-thread races, slow peer/DB, CQ saturation, cancellation at every point, close/descriptor reuse, handler exception and process restart/reconciliation.

### Answer 5

Assign stable aircraft/session/flight/record-batch/message/operation identities and sequence numbers; completion correlation never substitutes for these. Lease encrypted or plaintext-domain-separated fixed buffers under strict classification, zero on cross-domain reuse, and keep keys/buffers/context valid until terminal completion. Batch within bounded bytes/time/deadline while preserving sequence and record integrity; explicit gaps/duplicates are reconciled.

Submit durable writes with a documented fsync/storage durability contract. Acknowledge upstream only after required durable completion, not submission. Cancellation/flight handoff/timeout races still reap the original result; late success is recorded, and retries use stable idempotency/offset/version so data is not duplicated. Bound SQ/CQ, in-flight bytes, device concurrency and handler work; stop intake or spill to a separately durable bounded fallback under explicit safety policy. Completion handlers remain short and serialized per flight/stream.

Encrypt with managed key identity/version, protect completion/control metadata, authenticate sources, and enforce tenant/aircraft access. Backend failover records the last durable sequence and verifies storage/key availability before resuming; do not assume Windows/Linux/library semantics match. Shutdown drains/reaps or records unresolved operations; crash recovery scans durable manifests/checksums and reconciles accepted acknowledgements, incomplete batches and duplicates.

Observe sequence/deadline slack, submission/completion lag and occupancy, short/error/cancel races, buffer/key pool, durable latency, gaps/duplicates, backend health and recovery state. Test power/process/device/region/key failures, partial/late/out-of-order completions, CQ saturation, cancellation/shutdown, corruption, overload and fallback restoration. Production claims require named aviation, safety, storage, security/cryptography, operations and regulatory reviewers plus hardware-in-the-loop, fault-injection, durability/power-loss and recovery-drill evidence.
