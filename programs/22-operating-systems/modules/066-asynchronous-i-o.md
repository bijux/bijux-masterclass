---
module_id: OS-066
program: Operating Systems
level: 2
module_number: 66
title: Asynchronous I/O
status: complete
last_verified: 2026-09-04
---

# Asynchronous I/O

## One-Page Review

### Governing question

How should an operating system accept I/O without making the submitting thread wait for completion, preserve request and buffer lifetime, report exactly one terminal result, and coordinate batching, dependencies, cancellation, timeout, backpressure, teardown, and security?

### Essential definitions

- **Synchronous I/O** returns control after the operation reaches the interface's completion point or fails.
- **Nonblocking I/O** returns immediately when an operation would otherwise wait; it does not itself execute the operation asynchronously.
- **Readiness notification** reports that an operation is likely to make progress now, while asynchronous completion reports the outcome of an operation already submitted.
- **Asynchronous I/O (AIO)** separates initiation from completion so a caller can have multiple operations in flight.
- A **submission queue entry (SQE)** describes one requested operation; a **completion queue entry (CQE)** reports one result and identifying metadata.
- A **request token** correlates completion with application-owned state and must remain unambiguous across reuse.
- **Backpressure** limits accepted or in-flight work when rings, workers, file systems, devices, memory, or completion consumers are saturated.
- **Cancellation** requests that unfinished work stop; it races normal completion and is not necessarily guaranteed to win.
- A **linked chain** expresses execution or failure dependencies among operations; it is stronger than submitting entries in source order.
- A **registered resource** is a file, buffer, event target, or other object held by an asynchronous context to reduce per-operation lookup or mapping cost.

### Central model, mechanism, or theorem

Represent an operation as

$$
R=(i,o,f,b,n,p,g,s,r),
$$

where $i$ is a unique token, $o$ the opcode, $f$ the referenced file or object, $b$ the buffer capability, $n$ the requested extent, $p$ the offset or parameters, $g$ a lifecycle generation, $s$ the request state, and $r$ its result. A successful submission transfers ownership of all referenced state until exactly one terminal completion returns it.

The durable state machine is `prepared -> submitted -> accepted -> executing -> terminal -> reaped`. Submission can be partial; cancellation and timeout contend with normal completion; close or process exit initiates teardown but does not retroactively erase accepted work. Correctness requires one winner for terminal state, stable resources through that transition, bounded queues, and completion consumption fast enough to prevent deadlock or unbounded loss.

### Critical invariants

- Each accepted operation has a unique live identity and produces exactly one terminal result under the interface contract.
- Buffers, files, credentials, offsets, and application metadata remain valid until the operation's terminal completion is consumed or explicitly transferred.
- A submission return count identifies exactly which prefix or entries were accepted; unaccepted work is never assumed in flight.
- Ring producers publish initialized entries before advancing tails, and consumers acquire published tails before reading entries.
- Completion results preserve short I/O, per-operation errors, flags, and cancellation races rather than collapsing them into batch success.
- Dependencies, drain points, file offsets, and durability edges are explicit; queue order alone is not treated as execution order.
- SQ, CQ, worker, memory, device, and application capacities all have bounded backpressure and recovery behavior.
- Teardown prevents new submissions, resolves or cancels accepted work, drains completions and callbacks, unregisters resources, then destroys the context.
- Untrusted SQEs, indices, lengths, opcodes, flags, and registered ranges are validated at every authority boundary.

### Common failures

Common mistakes are calling nonblocking I/O “asynchronous,” reusing a buffer after submission, using a stack control block, assuming every submitted entry was accepted, treating ring-tail publication as ordinary unsynchronized memory, assuming SQ order is completion order, using one token after slot reuse, ignoring short transfers, interpreting cancellation success as proof no completion can arrive, abandoning CQEs on shutdown, allowing completion-ring overflow, pinning unlimited registered buffers, believing io_uring makes every filesystem operation nonblocking, and measuring syscall reduction while omitting queueing, worker, device, and completion latency.

### Compact example

A request is submitted while cancellation and device completion race. An atomic terminal-state transition lets the cancellation path win once; the later completion observes a terminal generation and is ignored or reconciled according to the API without producing a second user-visible result. If completion wins first, cancellation reports that it lost. The buffer is reusable only after the terminal result transfers ownership back.

### Connections

[OS-024](024-atomic-operations.md), [OS-026](026-pipes-and-byte-streams.md), [OS-045](045-buffer-cache-and-page-cache.md), [OS-052](052-smp-kernel-synchronization.md), [OS-064](064-block-and-character-devices.md), [OS-065](065-i-o-schedulers.md), and [OS-067](../ROADMAP.md) connect AIO to atomic state, readiness, caching, concurrent rings, device semantics, scheduling, and zero-copy.

## Governing Question

Synchronous I/O couples a call stack to one operation. Asynchronous I/O decouples them: the application describes work, the kernel accepts some or all of it, execution proceeds through an appropriate path, and results return later through a queue, signal, callback, event, or wait interface.

The governing question is how to preserve the ownership and error clarity that a blocking call provides implicitly. Once hundreds of operations share rings and workers, identifiers, dependencies, cancellation, teardown, and capacity become explicit protocol design.

## Why This Matters

High-concurrency servers, databases, storage engines, proxies, and runtimes need to overlap I/O without dedicating a thread to every wait. Batching submissions and completions can reduce system calls, cache misses, and scheduling transitions.

The optimization also enlarges the lifetime surface. A pointer can remain reachable after its submitting function returns. A close can race work that holds a file reference. One slow completion consumer can fill a shared CQ and stall unrelated operations.

Asynchronous interfaces are security boundaries because they encode many operations in shared memory and retain resources. Validation, restrictions, accounting, cancellation, and process-exit behavior are therefore part of the design, not ancillary cleanup.

## Prerequisites and Retrieval

Review [OS-003](003-system-calls-and-user-kernel-transitions.md), [OS-014](014-context-switching.md), [OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-024](024-atomic-operations.md), [OS-026](026-pipes-and-byte-streams.md), [OS-028](028-signals-and-notifications.md), [OS-045](045-buffer-cache-and-page-cache.md), [OS-052](052-smp-kernel-synchronization.md), [OS-054](054-kernel-read-copy-update.md), [OS-063](063-direct-memory-access.md), [OS-064](064-block-and-character-devices.md), and [OS-065](065-i-o-schedulers.md).

Retrieve these distinctions:

- blocking, nonblocking, readiness, asynchronous initiation, asynchronous execution, and asynchronous completion are different properties;
- submission, acceptance, execution, device completion, kernel completion, notification, and result consumption are separate events;
- file-descriptor numbers, referenced file objects, registered slots, and direct descriptors have different lifetime rules;
- operation identity, ring slot, user token, and lifecycle generation must not be conflated;
- source order, SQ order, issue order, device order, and completion order can all differ;
- timeout notification, cancellation request, cancellation success, and proof of stopped device access are different claims;
- buffer registration, pinning, mapping, ownership, and zero-copy are separate mechanisms;
- syscall count, CPU time, throughput, average latency, tail latency, and queue depth measure different effects.

## Learning Objectives

After this module, you should be able to:

1. distinguish synchronous, nonblocking, readiness-driven, thread-backed, kernel AIO, and shared-ring models;
2. model submission, partial acceptance, execution, completion, reaping, cancellation, timeout, and teardown;
3. preserve file, buffer, credential, offset, token, and generation lifetime for in-flight operations;
4. reason about SQ/CQ ring capacity, memory ordering, batching, links, drains, multishot results, and backpressure;
5. evaluate registered files and buffers, polling modes, worker fallback, event integration, and resource accounting;
6. handle short I/O, per-operation errors, cancel/complete races, process exit, fork, exec, and device removal;
7. verify AIO protocols with state models, fault injection, race tests, trace correlation, and scoped performance evidence.

## Core Exposition

### Separate the six events

An application prepares a request, submits it, learns whether the kernel accepted it, waits or performs other work, receives completion, and consumes the result. Hardware-backed operations also have issue and device-completion events between acceptance and kernel completion.

Name these events in APIs and traces. “Submitted” must not ambiguously mean placed in user memory, accepted by the kernel, or issued to a device.

### Synchronous I/O

A synchronous read or write can still return short, be interrupted, hit page faults, wait in queues, or complete from cache. Its key property is that the call returns the result for that invocation.

Threads can create concurrency by issuing synchronous calls independently. This is a valid design baseline and often simpler than explicit AIO when concurrency is modest.

### Nonblocking I/O

Nonblocking mode asks an operation not to sleep merely because progress is unavailable. It returns would-block when no bytes or state transition can proceed.

The caller typically combines it with readiness notification and retries. No operation remains pending solely because a nonblocking call returned would-block.

### Readiness notification

`select`, `poll`, and `epoll` report file-descriptor readiness. Readiness is level information at a moment, so the actual operation must tolerate another consumer taking the resource or state changing.

Edge-triggered use requires draining until would-block and maintaining application state carefully. Readiness does not report the completion result of a request with a particular buffer and offset.

### Thread-backed asynchrony

A runtime can place synchronous calls on a worker pool and return futures or callbacks. This supports interfaces that lack native AIO and preserves familiar operation semantics.

It consumes threads, stacks, scheduler work, credentials context, and queue capacity. If a filesystem call blocks indefinitely, a bounded worker pool can starve unrelated operations.

### POSIX AIO

POSIX AIO uses asynchronous control blocks, functions such as `aio_read`, `aio_write`, `aio_error`, `aio_return`, `aio_cancel`, `aio_suspend`, and list I/O, with configurable notification.

The control block and buffer remain valid until completion. On Linux, library implementation details and supported object types matter; portable semantics should not be inferred from one implementation's use of worker threads.

### Linux native AIO

Linux native AIO uses a kernel context with `io_setup`, `io_submit`, `io_getevents`, `io_cancel`, and `io_destroy`. It historically fits particular file and direct-I/O paths rather than a universal operation set.

Submission can accept fewer requests than requested. Individual events carry result values; the application retains each control block and referenced buffer through completion.

### io_uring overview

io_uring exposes shared submission and completion rings plus operation entries. `io_uring_setup` creates a context, memory mappings expose ring state and entries, `io_uring_enter` submits or waits, and `io_uring_register` manages long-lived resources and restrictions.

Use a maintained library unless low-level control is itself the goal. The library centralizes feature negotiation, barriers, ring layout, syscall details, and compatibility.

### Shared ring structure

The SQ has producer and consumer indices, a mask or size, submission entries, and optionally an indirection array. The CQ similarly holds completion entries between kernel-produced tail and application-consumed head.

Indices grow and wrap according to the ABI; masking maps them to slots. Compute available capacity from monotonic index differences with supported integer widths, not from ambiguous equality alone.

### Ring memory ordering

The producer fully initializes an SQE before publishing the SQ tail with release semantics. The kernel observes the tail with acquire semantics before reading the entry. CQ publication follows the mirror relation.

Plain loads and stores may appear to work on a strong architecture and fail on another. Use the library or exact documented atomic operations rather than inventing barriers.

### Submission queue entries

An SQE specifies opcode, file reference, offset, buffer or vector, length, flags, user token, and operation-specific fields. Zero or initialize unused fields so stale data cannot become a future flag.

Validate all application-side bounds before publication. The kernel validates again because the ring is untrusted shared memory and can change concurrently unless copied or consumed under protocol.

### User data tokens

The user-data field is opaque correlation data returned in completions. It can encode an index or pointer only if the application guarantees lifetime, uniqueness, alignment, and safe validation.

Pair slots with generations so a late completion cannot match a newly allocated request in the same slot. Never dereference a completion-provided pointer before validating that it names a currently live operation.

### Submission acceptance

A submission call can process fewer SQEs than requested or report an error. Track the exact accepted set and leave the remainder prepared for retry or explicit failure.

Batch-level return values and operation-level CQE results are different. A successful submit does not mean an operation succeeded, or even that execution began immediately.

### Completion queue entries

A CQE normally contains the user token, signed result, and flags. Negative results encode per-operation errors; nonnegative results can be short byte counts, descriptors, or opcode-specific values.

Consume every CQE exactly once and advance the head only after copying the needed fields. A multishot request can produce several CQEs until a flag indicates termination.

### Completion order

Independent operations can finish in any order because caches, workers, filesystems, devices, priorities, and request sizes differ. SQ adjacency does not create an ordering edge.

Match by token and generation. If application semantics require ordering, express a link, drain, file-offset discipline, or higher-level dependency and understand its failure behavior.

### Short I/O

A successful asynchronous read or write can transfer fewer bytes than requested. The result is an extent, not a Boolean.

Advance buffer and offset safely and resubmit only when the file and protocol permit. Zero progress needs a defined EOF, would-block, retry, or error interpretation; infinite automatic retry can spin.

### File offsets

Explicit offsets permit independent operations. Shared file-position semantics can serialize or race depending on interface and operation.

Use explicit offsets for predictable parallel file I/O when supported. Append has filesystem-defined atomicity and ordering; do not emulate it with a racy seek-plus-write.

### Registered files

Registering files lets the context hold references in indexed slots, reducing per-operation descriptor lookup. Fixed or direct descriptors can avoid ordinary process file-table allocation for some operations.

An index is meaningful only in its ring and registration generation. Replacement and unregistration synchronize with in-flight users under the API; closing the original descriptor need not invalidate a held registered reference.

### Registered buffers

Registering user buffers can pin and map memory for repeated operations, reducing per-I/O setup. It consumes memory-lock accounting and can impede migration, reclaim, and copy-on-write.

Validate each subrange against the registered extent. Unregister only after in-flight references end, and bound total pinned memory per tenant and context.

### Provided buffer pools

A buffer-selection pool lets the kernel choose an available buffer for a receive-like request and return its identifier in the CQE. This reduces per-message submission overhead.

The application owns a returned buffer until it explicitly replenishes the pool. Reusing the identifier early allows two operations to write the same memory.

### Resource registration

Event targets, personalities, worker affinity, restrictions, ring descriptors, buffer rings, and other resources can be registered depending on kernel features.

Each registration changes lifetime and authority. Feature-query and error handling must precede use; applications cannot assume the build host's opcode set exists everywhere.

### Feature negotiation

Setup returns supported features, while probe or query mechanisms report operations and capabilities. Kernel versions alone are a weak proxy because backports and configuration differ.

Test capabilities at runtime, retain a safe fallback, and distinguish unsupported from temporarily unavailable or policy-denied.

### Batching

Batching amortizes system calls, locks, cache transfers, and doorbells. It can improve throughput and energy efficiency.

Waiting to fill a batch adds queueing delay. Cap batch size and dwell time, and measure tail latency and completion-consumer pressure alongside throughput.

### Linking

Linked SQEs express dependencies: subsequent work runs only under the link's success or completion rules. Hard links and ordinary links differ in how failure propagates.

Define whether partial I/O counts as success for the chain and what cleanup remains when a middle operation fails. A linked timeout has special race semantics rather than acting like a global transaction.

### Drain ordering

A drain requests that prior work reach the relevant completion state before the drained operation proceeds. It can establish a broad barrier at the cost of parallelism.

Use the narrowest dependency that captures the application invariant. A global drain can create head-of-line blocking and unexpected coupling among independent flows.

### Timeouts

An asynchronous timeout is itself an operation or dependency. Its completion says the timer fired or was canceled; it does not universally prove the target's hardware effects stopped.

After timeout, inspect the target operation's result and cancellation semantics. Storage and network protocols can leave an uncertain in-flight action that requires abort, reset, or idempotency handling.

### Cancellation

Cancellation identifies work by token, descriptor, or other selector and races queueing, execution, and normal completion. Outcomes include canceled, already complete, not found, or unsupported once issued.

Design for both winners. Exactly one application request reaches terminal state, while the cancel operation itself can have a separate CQE that must also be consumed.

### Completion-versus-cancel arbitration

Use an atomic state or serialized event loop to transition `in-flight` into one terminal outcome. A late event validates generation and finds terminal state rather than freeing resources twice.

Do not free a buffer merely because cancellation was requested. The interface's successful-cancel or target-completion evidence determines when ownership returns.

### Multishot operations

Multishot accept, receive, poll, or other operations can emit many completions from one submission. CQE flags indicate whether more results can follow and can carry selected-buffer metadata.

Keep the request state and resources live until the terminal CQE. Apply backpressure to the result stream; one long-lived request can otherwise fill the CQ.

### Readiness operations in io_uring

Poll-like opcodes integrate readiness into the completion queue and can be multishot. They still report state changes rather than completing an independent read or write automatically.

Recheck the operation and handle edge or level semantics. Cancellation and descriptor reuse require the same generation discipline as data operations.

### Worker fallback

Some operations can execute directly through a nonblocking kernel path; others are punted to asynchronous workers because filesystems or handlers may block.

The API remains asynchronous to the caller, but worker counts, credentials, scheduler latency, stack memory, and blocking dependencies affect capacity. Trace the actual execution path before claiming kernel-native scalability.

### Worker-pool backpressure

Bound queued and active work by class. A pool saturated with indefinitely blocking operations can prevent cancellations, metadata work, or unrelated files from progressing.

Use admission limits, separate trust domains where appropriate, deadlines, and operational metrics for queued, running, blocked, and completed work.

### SQ polling

SQ polling can let a kernel thread consume submissions without a syscall for each batch. It trades CPU and power for lower submission overhead and can have privilege, affinity, and idle-time implications.

It is not automatically faster. Compare at realistic load, include idle power, and register or reference files according to the negotiated feature set.

### I/O polling

Device polling can reap completions without interrupt wakeups for suitable direct-I/O paths and devices. It can reduce latency at high rates while consuming CPU.

Do not mix polling modes and unsupported files casually. Account CPU time, NUMA and queue affinity, and behavior at low utilization.

### Deferred task work

Some modes defer completion-related work until the application explicitly enters the ring. This can improve cache locality and control execution context.

An application that stops entering the kernel can stall its own completions. Event-loop design must guarantee progress even when no new submissions arrive.

### Eventfd integration

An eventfd can notify another loop or thread that completions are available. Its counter coalesces events and does not equal a precise count of CQEs under every configuration.

Drain the CQ as authoritative state. Prevent notification storms and ensure shutdown wakes every consumer that might otherwise block.

### epoll integration

The ring file descriptor can integrate with readiness loops where supported, and applications can combine socket readiness, eventfd, and completion processing.

Avoid two consumers racing the same CQ head without a defined multi-consumer protocol. Readiness can remain asserted until enough completions are consumed.

### Submission-queue capacity

When the SQ is full, producers must submit, wait, spill to a bounded application queue, or apply upstream backpressure. Overwriting unread entries corrupts the protocol.

Multiple producers need library-supported reservation and publication. Reserving a slot and being preempted before publication can stall naive contiguous-tail schemes.

### Completion-queue capacity

The CQ must accommodate completions even when applications submit aggressively or multishot sources burst. Some configurations report overflow or retain overflow state, but relying on it adds cost and risk.

Size the CQ from maximum in-flight and result multiplicity, consume promptly, monitor overflow counters, and stop admission before capacity is exhausted.

### Fairness

One ring or tenant can monopolize workers, pinned memory, file references, SQ slots, CQ capacity, or device requests. Kernel and application admission policies must define shares and caps.

Batch fairness matters too: continuously resubmitting one hot flow can starve cold flows in a single-threaded event loop even when the kernel is fair.

### Credentials and personalities

Asynchronous work needs a defined credential context. Registered personalities or worker execution must not accidentally use mutable credentials from the wrong thread.

Capture or select authority explicitly, restrict privileged registration, and test descriptor passing and process-credential changes.

### Restrictions

A ring created disabled can be configured with allowlisted operations and flags before enabling. Restrictions reduce an exposed ring's authority but do not validate application-level paths, lengths, or object policy alone.

Use defense in depth: process sandboxing, file-descriptor discipline, memory limits, cgroups, and opcode restrictions aligned with the workload.

### Shared rings across threads

Threads can share a ring, but SQ reservation, CQ consumption, token allocation, wakeup, and teardown need explicit ownership. Libraries provide safe synchronization patterns.

One designated CQ consumer simplifies ordering; multiple consumers can scale but must claim entries atomically and route results without duplicate handling.

### Fork and exec

Shared mappings, registered memory, worker state, and file references make fork semantics subtle. A child must not independently manipulate inherited ring state unless the interface and library support that ownership model.

Close-on-exec and registered-descriptor behavior belong to the threat and lifecycle model. Prefer creating rings in their long-term owning process after fork when practical.

### Filesystem semantics

Buffered and direct file I/O have different alignment, cache, writeback, locking, and completion behavior. AIO does not weaken filesystem atomicity or durability rules.

A write CQE can report bytes accepted into page cache rather than stable media. Use fsync or linked durability operations according to the application's persistence protocol.

### Socket semantics

Sockets naturally support readiness, async send and receive, accept, connect, and multishot patterns. Short transfers, message boundaries, ancillary data, shutdown, and peer close retain their ordinary semantics.

Do not assume one CQE equals one application message for a byte stream. Maintain framing and backpressure above the transport.

### Device semantics

Character and block devices define which asynchronous operations, cancellation, polling, and mappings they support. A driver may complete inline, through interrupts, or through workers.

Device removal must resolve accepted operations and wake completion consumers before resources vanish. Unknown hardware completion after timeout remains a driver recovery problem.

### Process exit and close

Closing the ring or exiting begins context teardown. The kernel must stop or finish work and release references, but applications should perform orderly cancellation and reaping to preserve their own invariants and error reporting.

Closing an ordinary file descriptor does not necessarily cancel operations that already hold file references. Treat operation lifetime independently from descriptor-table membership.

### Orderly shutdown

Move the application context through `running -> stopping -> draining -> closed`. Stop producers, reject new work, cancel or allow accepted work by policy, consume all terminal CQEs, unregister resources, then close the ring.

Keep completion dispatch alive until every request and cancel operation resolves. A shutdown path that stops the event loop before draining creates leaks and use-after-free.

### Observability

Record token and generation, opcode, object class, requested and completed bytes, offset, submit and accept time, issue path, worker use, completion time, result, flags, cancellation, timeout, queue depth, overflow, registered-resource counts, and context lifecycle.

Do not log sensitive buffers or raw pointer-valued tokens. Correlate with filesystem, block, network, and device traces using stable sanitized identifiers.

### Performance measurement

Measure operations per second, bytes, submission syscalls, batch sizes, CPU time by application and workers, context switches, queue depths, average and tail latency, cancellation latency, overflow, memory pins, and power.

Compare against synchronous threads and readiness loops under identical workload, cache, depth, affinity, device, and durability semantics. Syscall reduction alone is not an end-to-end result.

### Verification

Model request states and run cancel/complete/timeout/shutdown interleavings. Inject partial submission, per-operation error, short I/O, worker saturation, CQ stall, ring wrap, token reuse, descriptor replacement, buffer unregister, device loss, and process exit.

Use sanitizers, lock and memory debugging, syscall tracing, ring statistics, filesystem or block traces, and deterministic fake endpoints. Preserve kernel, library, features, setup flags, limits, workload, seeds, traces, negative results, and claim boundaries.

## Definitions and Notation

Let $P$ be the prepared set, $A$ accepted in-flight operations, $C$ terminal completions not yet consumed, and $F$ freed application state. Safety requires

$$
A \cap F = \varnothing
$$

for all referenced buffers, file contexts, and tokens. Consuming a terminal result transfers ownership and permits the corresponding state to enter $F$ when no other reference exists.

For operation $i$, let $t_p,t_s,t_a,t_x,t_c,t_r$ denote preparation, submission, acceptance, execution start, completion publication, and result reaping. A valid trace satisfies $t_p\le t_s\le t_a\le t_c\le t_r$; $t_x$ can be unobserved but lies after acceptance and before completion when execution occurs.

For a ring of capacity $N$ with monotonic producer tail $T$ and consumer head $H$, used capacity is $U=T-H$ under the ABI's modular-width constraints, and valid operation requires $0\le U\le N$. Release publication of $T$ follows entry initialization; acquire observation of $T$ precedes entry consumption.

Define terminal ownership as a compare-and-transition from `in-flight` to exactly one of `{completed, canceled, timed-out, failed}`. Timeout may be an observation that triggers cancellation rather than a target terminal state; the chosen API contract determines which transitions are user-visible.

## Mechanisms, Invariants, or Proof Structure

A reviewable asynchronous-I/O design discharges these obligations:

1. **Semantics:** distinguish nonblocking readiness, asynchronous initiation, execution, notification, and completion.
2. **Identity:** give every live operation an unambiguous token and generation across slot reuse.
3. **Acceptance:** account for partial submission and know the exact set owned by the kernel.
4. **Lifetime:** retain buffers, files, credentials, metadata, registrations, and contexts through terminal result.
5. **Publication:** apply correct release/acquire ordering to SQ and CQ entries and indices.
6. **Results:** preserve short transfer, error, flags, multishot continuation, and per-operation outcome.
7. **Dependencies:** encode required order through links, drains, offsets, locks, or durability operations.
8. **Capacity:** bound SQ, CQ, workers, pins, files, device depth, retries, and application backlog.
9. **Arbitration:** serialize completion, cancel, timeout, reset, and close into one terminal owner.
10. **Progress:** keep completion consumption and shutdown active until every accepted operation resolves.
11. **Authority:** validate opcodes, flags, ranges, descriptors, credentials, restrictions, and tenant accounting.
12. **Evidence:** test wrap, races, faults, fallbacks, object types, lifecycle, performance, and portability.

The proofs remain separate. A published SQE proves availability, not acceptance. Acceptance proves ownership transfer, not success. Cancellation submission proves only that a cancel request exists. A CQE proves the documented result at one interface boundary, not durable storage or application-level transaction commit.

## Alternatives and Trade-Offs

- **Synchronous threads versus explicit AIO:** threads reuse blocking semantics; AIO reduces stacks and crossings while externalizing state machines.
- **Readiness versus completion:** readiness fits operations attempted when possible; completion fits requests whose buffers and parameters are fixed up front.
- **POSIX AIO versus Linux native AIO:** POSIX favors portability; native AIO exposes Linux-specific kernel contexts and constraints.
- **Native AIO versus io_uring:** native AIO is narrower; io_uring unifies many operations with a larger feature and security surface.
- **System calls versus shared rings:** calls copy and validate at entry; rings amortize crossings and require memory-order discipline.
- **Small versus large batches:** small batches reduce waiting; large batches improve amortization and can pressure completions.
- **Registered versus per-operation resources:** registration reduces lookup and mapping; it extends pins, references, accounting, and teardown.
- **Independent versus linked operations:** independence maximizes concurrency; links encode order and propagate failure coupling.
- **Targeted links versus drains:** links express local dependencies; drains impose broad ordering and head-of-line blocking.
- **Interrupt versus polling:** interrupts save CPU at low load; polling can reduce latency while consuming CPU and power.
- **Direct execution versus workers:** direct paths reduce scheduling; workers support blocking handlers with bounded-pool risks.
- **One ring versus per-thread rings:** one ring centralizes flow control; several rings reduce contention and complicate global fairness.
- **One CQ consumer versus many:** one consumer simplifies ownership; many can scale if claiming and routing are correct.
- **Graceful drain versus aggressive cancel:** draining preserves ordinary outcomes; cancellation shortens shutdown and leaves race and side-effect ambiguity.

## Failure Modes and Misconceptions

- **“Nonblocking is asynchronous.”** Would-block returns without leaving an operation in flight.
- **“Readiness means the next call cannot block.”** State can change before the operation.
- **“A worker thread is not real AIO.”** It is asynchronous to the caller, with different scalability costs.
- **“Submission success means I/O success.”** The operation result arrives later and can be short or failed.
- **“A batch submits all entries.”** acceptance can be partial.
- **“SQ order is execution order.”** independent operations can issue and complete differently.
- **“One ring slot is a permanent request identity.”** slots wrap and are reused.
- **“A pointer token is safe when returned.”** its object may have been freed or reallocated without a generation rule.
- **“The CPU's ordinary stores publish SQEs.”** shared rings require documented release/acquire ordering.
- **“A CQE is always terminal.”** multishot operations can emit continuing results.
- **“Cancellation prevents every completion.”** cancel and completion race and both operations can report CQEs.
- **“Timeout proves side effects stopped.”** an issued device or remote operation can remain uncertain.
- **“Registered buffers are free optimization.”** they pin memory and extend authority and teardown.
- **“Closing an fd cancels accepted work.”** the operation can hold a file reference.
- **“io_uring makes every operation truly nonblocking.”** unsupported or blocking paths can use workers.
- **“A large CQ cannot overflow.”** bursts, multishot operations, and stalled consumers can exceed assumptions.
- **“Fewer syscalls proves lower latency.”** batching, queues, workers, devices, and reaping determine the path.
- **“Closing the ring is orderly shutdown.”** application resources and semantic outcomes still require coordinated drain.

## Worked Examples

### Example 1

A socket loop uses edge-triggered epoll and nonblocking reads. It drains until would-block; no read remains pending. A separate io_uring version submits receive operations and later consumes CQEs tied to fixed buffers.

### Example 2

An application submits 64 native-AIO control blocks but the syscall accepts 20. It tracks those 20 as in flight and retries the untouched 44 rather than waiting for completions that can never exist.

### Example 3

Two independent reads enter adjacent SQEs and complete in reverse order because one hits cache. Generation-bearing user tokens route each result to the correct future.

### Example 4

A registered buffer covers 1 MiB. An SQE selects buffer zero at offset 64 KiB for 128 KiB; application bounds checks and the kernel registration contract ensure the subrange stays within the pin.

### Example 5

A provided-buffer multishot receive returns buffer IDs 7, 2, and 9 in three CQEs. The application processes and replenishes each separately and keeps request state until the final CQE clears its continuation flag.

### Example 6

A linked write and fsync encode a durability dependency. A short write is handled as a chain failure under the application's policy rather than treating the later fsync as proof the intended full record persisted.

### Example 7

An SQ-polling configuration reduces submission calls at high depth but consumes one busy CPU during idle periods. The deployment retains ordinary submission for low-rate tenants after measuring power and tail latency.

### Example 8

A blocking filesystem operation falls back to a worker. A per-tenant admission bound prevents thousands of slow requests from consuming the entire shared worker pool and delaying cancellation.

### Example 9

Shutdown stops producers, submits cancellation for eligible requests, continues consuming target and cancel CQEs, unregisters fixed files and buffers, then closes the drained ring. No callback refers to destroyed application state.

### Example 10

The following state model lets cancellation win a race and ignores a later completion for the already terminal request. It demonstrates one-owner arbitration only; it performs no AIO syscall, device cancellation, memory ordering, buffer management, or kernel work.

<!-- bijux-verify: {"id":"aio-terminal-arbitration","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"event=cancel transition=submitted->canceled\nevent=complete action=ignored state=canceled\nterminal=canceled count=1\n","stderr":""}} -->
```python
state = "submitted"
terminal_count = 0

for event in ("cancel", "complete"):
    if state == "submitted":
        prior = state
        state = "canceled" if event == "cancel" else "completed"
        terminal_count += 1
        print(f"event={event} transition={prior}->{state}")
    else:
        print(f"event={event} action=ignored state={state}")

print(f"terminal={state} count={terminal_count}")
```

## Cross-Program Connections

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects futures, event loops, ownership, atomics, queues, cancellation and structured concurrency. [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) connects asynchronous contracts, idempotency, deadlines, backpressure, streaming, partial results and observability.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects shared-memory validation, pinned-resource limits, credential capture, sandbox restrictions and teardown. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes state machines, capacity, fault injection, evidence and assurance. Within this program, [OS-065](065-i-o-schedulers.md) develops queued dispatch and [OS-067](../ROADMAP.md) develops zero-copy and kernel bypass.

## References

- Linux man-pages project, [io_uring(7)](https://man7.org/linux/man-pages/man7/io_uring.7.html), current page checked 2026-09-04. Shared submission and completion rings, mappings, SQEs, CQEs and memory ordering.
- Linux man-pages project, [io_uring_setup(2)](https://man7.org/linux/man-pages/man2/io_uring_setup.2.html), current page checked 2026-09-04. Ring creation, sizes, polling, task-work, attachment, restrictions and negotiated features.
- Linux man-pages project, [io_uring_enter(2)](https://man7.org/linux/man-pages/man2/io_uring_enter.2.html), current page checked 2026-09-04. Submission, waiting, entry fields, operation flags, links, timeouts, cancellation and per-operation results.
- Linux man-pages project, [io_uring_register(2)](https://man7.org/linux/man-pages/man2/io_uring_register.2.html), current page checked 2026-09-04. Registered buffers, files, events, personalities, restrictions, worker controls and resource lifetime.
- Linux man-pages project, [aio(7)](https://man7.org/linux/man-pages/man7/aio.7.html), current page checked 2026-09-04. POSIX AIO control blocks, operations, notifications, lifetime and Linux implementation context.
- Linux man-pages project, [io_submit(2)](https://man7.org/linux/man-pages/man2/io_submit.2.html), current page checked 2026-09-04. Linux native AIO submission, control blocks, operation forms, partial acceptance and errors.
- Linux man-pages project, [io_getevents(2)](https://man7.org/linux/man-pages/man2/io_getevents.2.html), current page checked 2026-09-04. Native AIO completion retrieval, counts, timeouts, events and results.
- Linux man-pages project, [io_cancel(2)](https://man7.org/linux/man-pages/man2/io_cancel.2.html), current page checked 2026-09-04. Native AIO cancellation requests, results and failure cases.
- Linux man-pages project, [epoll(7)](https://man7.org/linux/man-pages/man7/epoll.7.html), current page checked 2026-09-04. Level and edge readiness, interest and ready lists, wakeups and concurrency.
- Linux man-pages project, [eventfd(2)](https://man7.org/linux/man-pages/man2/eventfd.2.html), current page checked 2026-09-04. Counter-based event notification, blocking, polling, descriptor lifetime and overflow.

## Exercises

### Exercise 1

Design an asynchronous file-copy pipeline with bounded reads, writes, registered buffers, short-I/O recovery, ordering, cancellation, durability, and shutdown.

### Exercise 2

Specify a multi-producer, single-consumer shared-ring protocol. Prove reservation, publication, wrap, identity, completion, and backpressure safety.

### Exercise 3

Trace cancellation racing normal completion, timeout, file close, device reset, and process shutdown. State when every referenced object can be freed.

### Exercise 4

Design a multi-tenant io_uring service that uses registered resources and worker fallback while preserving memory, CPU, descriptor, queue, and security isolation.

### Exercise 5

Build a verification and performance plan comparing synchronous threads, epoll with nonblocking I/O, Linux native AIO, and io_uring.

## Answers to the Exercises

### Answer 1

Allocate a fixed number of equal-sized buffers and assign each a slot plus generation. Register buffers and files only after enforcing memory-lock and descriptor budgets. For each chunk, submit an explicit-offset read. A nonnegative short result advances the source offset and remaining extent; EOF closes that chunk. Only a completed read owns initialized bytes. Submit a write for exactly those bytes, retrying permitted short writes with advanced buffer and destination offset. Do not return the buffer to the free pool until the write's terminal CQE.

Bound in-flight reads, writes, SQ reservations, CQ backlog and application-ready chunks. Preserve output order with explicit offsets; if the target requires append or sequential semantics, use a serialized dependency rather than assuming completion order. After all writes, submit fsync when durable completion is required. On error or cancellation, stop new chunks, resolve every accepted read and write, retain uncertain buffers, and report copied and durable extents separately. Shutdown continues reaping CQEs, unregisters only after references end, closes files, and frees buffers last. Test short zero and nonzero transfers, partial submission, CQ pressure, disk full, source truncation, cancel races and fsync failure.

### Answer 2

Maintain monotonic reservation and publication positions rather than letting producers write a shared tail unsafely. A producer atomically reserves capacity only when `reserved - consumed < N`, obtains one unique position, initializes the masked slot completely, and marks that position published with release semantics. If publication must be contiguous, use per-slot sequence numbers so a preempted producer does not let later producers expose a gap. The kernel or consumer acquires publication state before reading the SQE.

Each SQE carries a request slot and generation allocated from a live table. The completion producer initializes the CQE before release-publishing its tail. The single consumer acquire-loads the tail, copies result fields, validates token and generation, atomically terminalizes the request, then advances CQ head. It never overwrites or frees live request state. SQ-full applies upstream backpressure; CQ occupancy reserves space for worst-case multishot or stops submission. Prove index difference stays within capacity under modular arithmetic, no two producers own a slot, publication precedes consumption, one completion owns terminal state, and wrap cannot make an old token name a new request.

### Answer 3

The target request holds references to its file object, buffer, application record, ring and device-facing state after acceptance. Timeout atomically marks a recovery intent and submits or triggers cancellation; it does not free anything. Normal completion and successful cancellation compete for the target's terminal transition. The losing event still has any interface-level CQE consumed but cannot terminalize or release the target twice. Closing the ordinary descriptor removes a table entry while the accepted request's file reference remains.

Device reset serializes with issue and hardware completion, contains DMA or remote effects, and assigns a new generation before slots are reused. If cancellation cannot prove the operation stopped, keep its buffer quarantined until normal completion or reset containment does. Shutdown stops producers and continues the consumer until target, timeout, cancel, and reset-generated outcomes resolve. Then drop operation metadata and file references, return or unregister buffers after their final users, unregister fixed files, destroy the drained ring, and free the context. A process-exit kernel cleanup does not replace application-level accounting where partial side effects matter.

### Answer 4

Give each tenant a ring or enforce explicit tenant identity on every operation in a broker-owned ring. Cap SQ backlog, in-flight operations, CQ result multiplicity, registered files, pinned bytes, provided buffers, worker queue, device depth, submission rate and completion CPU. Reserve capacity for cancellation and shutdown. Split worker pools or admission classes when one tenant's blocking filesystem can otherwise starve others. Attribute CPU, memory-lock, block and network work to the intended cgroup where the path supports it.

Create rings disabled, register an allowlist of necessary opcodes and flags, then enable. Accept only broker-controlled descriptors or validate path-opening policy separately. Use fixed-width request schemas, bounds-checked registered subranges, generation-safe tokens, captured credentials, and no raw pointer trust. Revoke a tenant by stopping admission, canceling eligible work, draining all CQEs, unregistering its resources, and closing its context. Monitor queue age, pins, workers, errors, cancels, overflow and per-tenant latency. Test malicious lengths and indices, multishot floods, CQ abandonment, descriptor replacement, credential change, blocking mounts, memory pressure, device loss and process death.

### Answer 5

Define equivalent workloads by object type, operation mix, size, offsets, arrival model, concurrency, working set, cache state, direct or buffered mode, durability, network peer and device. For synchronous threads, account stacks, threads, context switches and pool queueing. For epoll, use nonblocking endpoints and track readiness-to-operation retries. For native AIO, record supported paths and partial acceptance. For io_uring, record library, kernel features, setup flags, registration, batch sizes, polling and worker fallback.

Measure application end-to-end and submit-to-CQE latency distributions, throughput, bytes, errors, short I/O, CPU by context, system calls, context switches, queue depth, worker occupancy, CQ overflow, pinned memory, power and shutdown time. Sweep concurrency and open-loop rates through saturation. Inject partial submissions, slow endpoints, faults, cancellation, timeout and exit. Pin or record CPU and NUMA placement, repeat randomized trials, preserve raw histograms and negative results, and compare identical completion and durability meanings. Conclude only for the tested kernel, library, object path, flags, workload and hardware; fewer system calls alone does not prove a superior design.
