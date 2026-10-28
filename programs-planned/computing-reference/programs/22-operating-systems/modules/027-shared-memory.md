---
module_id: OS-027
program: Operating Systems
level: 1
module_number: 27
title: Shared Memory
status: complete
last_verified: 2026-09-04
---

# Shared Memory

## One-Page Review

### Governing question

How can processes share memory for high-throughput communication without losing synchronization, object lifetime, layout compatibility, protection, crash recovery, or bounded-resource guarantees?

### Essential definitions

- **shared memory** is a memory object mapped into more than one process so mappings can refer to common underlying storage.
- A **mapping** associates a process virtual-address interval with an object, offset, protection, and sharing mode.
- `MAP_SHARED` makes qualifying updates visible through other mappings of the same region; `MAP_PRIVATE` creates copy-on-write private modifications.
- A **publication protocol** defines when initialized shared state becomes observable and how readers establish synchronization.
- **process-shared synchronization** uses primitives whose representation and configuration permit coordination across processes.
- **false sharing** occurs when logically independent hot fields occupy one cache-coherence unit and cause avoidable invalidation traffic.
- **relative reference** stores an offset or index rather than a process-specific virtual address.

### Central model, mechanism, or theorem

Model a shared object as bytes `O[0:S]`, a set of mappings `M_i=(base_i, offset_i, length_i, protection_i)`, and protocol state `Q`. A process address `base_i+x` refers to object byte `offset_i+x` only for `0<=x<length_i`. Different bases can identify the same object byte.

Mapping makes storage common; it does not make compound operations atomic or ordered. Correctness therefore requires a layout contract, synchronized publication, exclusive or atomic mutation, generation-aware lifecycle, and bounds checks before every offset translation.

### Critical invariants

- Object size and every mapped interval cover all accessed bytes for the full access lifetime.
- Shared structures contain portable values, offsets, or handles—not raw pointers meaningful only in one address space.
- Every conflicting access is ordered by a process-shared synchronization protocol or a correctly specified atomic algorithm.
- Initialization publishes a fully valid layout version and generation before consumers use payload state.
- Resizing, unmapping, unlinking, restart, and recovery cannot strand a live participant with invalid storage assumptions.
- Permissions, names, descriptors, seals, and inherited mappings expose only intended authority.
- Capacity, wait time, abandoned-owner behavior, and corrupt-state recovery are explicitly bounded.

### Common failures

Common mistakes are using `MAP_PRIVATE`, storing raw pointers, assuming volatile provides synchronization, placing a default process-private mutex in the region, reading before initialization is published, truncating beneath active mappings, confusing unlink with immediate destruction, using a crash-abandoned lock without recovery, reusing a slot without a generation, trusting corrupt lengths or offsets, and interpreting a fast benchmark as proof of workload-wide superiority.

### Compact example

A creator atomically creates a named object, sizes it, maps it shared, writes a versioned header and bounded ring metadata, initializes process-shared synchronization, then publishes `READY` with release semantics. Consumers validate size, magic, version, generation, and offsets before attaching; acquire synchronization before reading payload; detect owner death or stale heartbeat; and detach before the coordinator unlinks and eventually destroys the object.

### Connections

[OS-023](023-mutexes-semaphores-and-condition-variables.md) supplies synchronization primitives; [OS-026](026-pipes-and-byte-streams.md) contrasts kernel-buffered byte streams. [OS-028](../ROADMAP.md) adds asynchronous signal notification.

## Governing Question

Shared memory removes mandatory data copies between cooperating address spaces, but it also removes the kernel-mediated message boundary and much of the lifecycle discipline that pipes provide. The application owns representation, synchronization, capacity, corruption detection, and recovery.

The governing question is not merely how to map the same pages. It is how to establish a reviewable protocol in which every participant agrees on what the bytes mean, when they may be observed, which process owns each transition, and what happens when a participant stops halfway through one.

## Why This Matters

Shared memory supports media buffers, databases, telemetry rings, browser components, language runtimes, accelerator queues, and low-latency services. It can reduce serialization and copying and allow direct random access to large datasets.

Its failures are correspondingly sharp. A stale pointer can corrupt unrelated state. An unsynchronized flag can expose partially initialized payload. A crashed writer can leave a lock or record permanently incomplete. A permissive name can disclose secrets to another user. Resizing can turn an apparently valid load into a fault.

Performance claims also require discipline. Cache coherence, NUMA placement, page faults, false sharing, synchronization contention, and recovery bookkeeping can dominate copy costs. The right comparison includes end-to-end latency, tail behavior, resource bounds, and operational complexity.

## Prerequisites and Retrieval

Recall address translation and page mappings, process creation from [OS-012](012-process-creation-and-program-loading.md), concurrency hazards from [OS-021](021-critical-sections-in-the-kernel.md), and mutexes, semaphores, and condition variables from [OS-023](023-mutexes-semaphores-and-condition-variables.md).

Retrieve these distinctions:

- a shared object, its name, its descriptor, and each mapping have separate lifetimes;
- virtual addresses may differ while object-relative offsets agree;
- storage visibility does not imply language-level synchronization;
- atomicity, ordering, durability, and crash consistency are distinct properties;
- mapping protection limits local operations but is not an application authorization protocol;
- unlink removes a name, not necessarily existing mappings or references;
- a shared-memory transport still needs framing, admission, and error contracts.

## Learning Objectives

After this module, you should be able to:

1. explain named, anonymous, inherited, file-backed, and descriptor-backed shared mappings;
2. design a versioned position-independent layout with validated offsets and bounded capacity;
3. specify initialization and publication using process-shared synchronization or justified atomics;
4. separate descriptor, name, mapping, object, and participant lifecycles;
5. analyze resize, crash, stale-participant, security, cache, NUMA, and resource failures;
6. choose among shared memory, pipes, sockets, and message queues using operational evidence;
7. construct tests and assurance arguments without overstating atomicity, visibility, durability, or performance.

## Core Exposition

### Objects and mappings

POSIX shared memory uses `shm_open` to create or open a named object, `ftruncate` to establish its size, and `mmap` with `MAP_SHARED` to place it into an address space. The descriptor may be closed after a successful mapping without invalidating that mapping.

Regular files can also back shared mappings. Linux additionally offers anonymous mappings inherited across `fork` and descriptor-backed anonymous objects through `memfd_create`. These mechanisms differ in discovery, permission, persistence, sealing, portability, and cleanup, but all require a separate data protocol.

### Shared versus private mappings

With `MAP_SHARED`, qualifying updates affect the shared object and are visible through peer mappings according to the platform contract. With `MAP_PRIVATE`, writes are private copy-on-write changes and do not implement an interprocess update channel.

The flag does not turn arbitrary source-language accesses into safe concurrent operations. Data races remain governed by the language and synchronization implementation. Use primitives explicitly supported for interprocess use or a rigorously specified atomic protocol.

### Creation and initialization

A new POSIX shared-memory object begins at length zero. A creator using `O_CREAT|O_EXCL` can win creation atomically, establish restrictive permissions, size the object, map it, initialize metadata and synchronization, and only then publish readiness.

Joiners must not infer readiness from name existence. They validate object size and an initialization state machine such as `EMPTY -> INITIALIZING -> READY`, with generation and creator identity. If the creator dies in `INITIALIZING`, recovery policy decides whether an authorized coordinator reconstructs or replaces the object.

### Layout contracts

A shared layout needs magic, format version, total size, byte order where relevant, feature flags, alignment rules, generation, capacity, and validated locations of variable regions. Fixed-width fields make cross-build review easier, but compiler ABI, padding, alignment, and atomic representation still matter.

Do not persist process-local pointers, function addresses, descriptors, mutex implementations of unknown compatibility, or allocator internals. Different processes can map at different bases. Store offsets or indices and translate only after verifying range, alignment, overflow, and object generation.

### Address translation

For mapping `M_i`, object offset `y` translates to `base_i+(y-offset_i)` only when the entire referenced interval lies inside both the object and mapping. Validate addition before performing it: an attacker-controlled `offset+length` can wrap.

Null can use a distinguished offset value. References to reused slots should pair an index with a generation so a delayed consumer cannot confuse a new object with the old occupant.

### Synchronization

Shared storage does not serialize producers and consumers. A process-shared mutex, semaphore, or condition variable must be configured and initialized according to its API before concurrent use. Default thread-only configuration is insufficient merely because its bytes reside in shared pages.

For lock-free structures, define atomic types, alignment, memory orders, single- or multi-producer assumptions, wrap arithmetic, reclamation, and progress. Release publication followed by acquire observation can order payload initialization, but only if every relevant access participates in the same protocol.

### A bounded ring

Let capacity be `C`, monotonic producer position `H`, and consumer position `T`. Occupancy is `H-T`, constrained by `0<=H-T<=C` in a non-overflowing logical domain. Physical slot is `position mod C`.

Real counters wrap, so comparison rules must remain valid within a stated maximum distance. Multiple producers need reservation and commit states; advancing the public head before a record is complete exposes torn data. Each slot can carry sequence and generation metadata to distinguish free, reserved, committed, and consumed states.

### Waiting and notification

Busy waiting offers low wake latency under brief contention but consumes CPU and performs poorly when the owner is descheduled. Semaphores, process-shared condition variables, or platform wait primitives can block until a predicate may have changed.

Wait in a predicate loop. A notification is not ownership of a slot, and wakeups can be spurious, coalesced, delayed, or raced. Hybrid designs spin under a measured budget, then block, while still checking shutdown and participant liveness.

### Crash and owner death

A process can die while holding a mutex, after reserving a slot, or midway through writing a record. Ordinary locks may remain unavailable forever. Where robust process-shared mutexes are supported, the next owner can be told that protected state may be inconsistent; it must repair state and mark the mutex consistent or abandon it.

Lock-free does not mean crash-recoverable. A dead producer can leave an uncommitted reservation. Protocols need commit markers, owner identity, epochs, leases or coordinator decisions, and idempotent repair. Time alone cannot prove death without a failure-detector assumption.

### Lifecycle layers

Name lifetime controls discovery. Descriptor lifetime controls a process reference used to map or manage the object. Mapping lifetime controls addressability in one process. Object storage lifetime depends on platform references and deletion state. Protocol participant lifetime belongs to the application.

`shm_unlink` removes the name; existing mappings can continue. A new object can later reuse the same name while old mappings refer to the old object. Generation identifiers prevent accidental federation of those distinct lifetimes.

### Resizing and truncation

Concurrent resize is a protocol operation, not a harmless allocator call. Peers may retain mapping lengths and references. Access to pages beyond a shortened backing object can fault; platform behavior around modifications concurrent with mapping use has important limits.

Prefer fixed maximum size, replace-and-handoff, or a quiescent resize protocol. A replacement publishes a new descriptor or name plus generation, waits for participants to acknowledge migration, and reclaims the old object only after no valid access remains.

### Protection and authority

Creation mode, `umask`, ownership, ACLs, namespaces, directory or naming policy, descriptor passing, and operating-system confinement determine who can attach. Apply least privilege at creation and avoid predictable public names for secret-bearing regions.

After initialization, mappings can use `mprotect` to reduce local access, but another authorized process may retain a writable mapping. Linux memfd seals can restrict supported mutations such as size changes under specified conditions. These are defense layers, not substitutes for participant authentication and protocol validation.

### Persistence and durability

Shared visibility is not durable storage. POSIX shared-memory objects commonly have kernel persistence rather than reboot durability. File-backed mappings require explicit durability reasoning; `msync` concerns mapped-file synchronization but does not alone establish an application transaction or recoverable multi-field update.

Persistent-memory paths add hardware, filesystem, instruction, ordering, and recovery requirements. Never infer crash consistency from `MAP_SHARED`, a successful store, or even a synchronization call without a complete platform-specific persistence protocol.

### Cache coherence and false sharing

Coherent hardware helps cores observe shared cache lines, but synchronization still establishes allowed program order. Writers to different fields on one hot cache line can repeatedly invalidate each other's copies. Padding or sharding may help, at the cost of memory and possibly worse locality.

Measure cache misses, coherence traffic, lock contention, retries, and tail latency. Do not assume padding size or cache geometry across platforms without discovery and evidence.

### NUMA and page faults

Physical placement can make local access cheap and remote access expensive. First-touch behavior, process migration, memory policy, and workload distribution influence placement. Pre-faulting or locking pages can change latency but consumes resources and requires privileges or limits.

Benchmark representative producer-consumer placement and data sizes. A throughput win on one socket may become a tail-latency loss across sockets.

### Resource accounting

Bound object size, number of objects, mapped virtual space, resident pages, locked pages, queue occupancy, participants, retries, and wait time. Creation can fail because of permissions, descriptor limits, address-space limits, or backing-store exhaustion.

An unbounded shared arena only moves denial of service outside a process heap. Admission and per-tenant quotas must cover both data and metadata.

### Observability

Record object generation, version, size, participant attach and detach, occupancy, reservation age, commit gaps, wait duration, wakeups, owner death, repair, corruption, faults, and migration state. Avoid exposing payload secrets or stable public names.

Debuggers and snapshots can observe inconsistent multi-field state unless they participate in the protocol. Diagnostic readers need a snapshot, sequence-lock retry, or explicit best-effort label.

### Security and assurance

Treat every shared byte as untrusted when another security domain can write it. Validate headers, offsets, sizes, enum values, state transitions, owner identities, and checksums before use. Never form a pointer or allocate from shared metadata before bounds and overflow checks.

Safety-relevant use requires explicit timing, corruption, crash, restart, isolation, and recovery bounds. Tests support but do not replace analytical review and named human acceptance of platform assumptions and residual risk.

## Definitions and Notation

Let an object contain `S` bytes. Mapping `M_i=(B_i,O_i,L_i,P_i)` has process-local base `B_i`, object offset `O_i`, length `L_i`, and protection `P_i`. Object interval `[y,y+n)` is addressable through it only if `O_i<=y`, `y+n<=O_i+L_i`, arithmetic does not overflow, and protection permits the access.

For a ring, capacity is `C`, logical head is `H`, tail is `T`, and occupancy is `N=H-T`, with `0<=N<=C`. Slot `k` is `k mod C`; a generation or sequence `G_k` distinguishes reuse. State `Q` includes initialization, participant, reservation, and shutdown state.

Visibility means another mapping can observe updates under applicable synchronization. Atomicity means an operation is indivisible at its specified abstraction. Durability means state survives a stated failure boundary. These terms are not interchangeable.

## Mechanisms, Invariants, or Proof Structure

A reviewable shared-memory design follows nine obligations:

1. Select the object mechanism and specify name, descriptor, mapping, and deletion lifetimes.
2. Define versioned layout, alignment, endianness, capacity, and position-independent references.
3. Validate every size, offset, length, generation, and state transition before use.
4. Publish initialization and payload through process-shared synchronization with explicit ordering.
5. Prove bounded ring or allocator invariants across reservation, commit, consumption, wrap, and reuse.
6. Define waits, overload, cancellation, shutdown, owner death, partial update, and repair.
7. Prevent resize, unmap, unlink, replacement, and restart from racing live access.
8. Enforce least authority and treat writable peers and shared metadata as threat inputs.
9. Measure page, cache, NUMA, contention, fault, and recovery behavior under representative load.

The executable model demonstrates offset translation and a single-producer, single-consumer bounded ring. It is arithmetic evidence, not a concurrent implementation.

<!-- bijux-verify: {"id":"toy-shared-ring","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"offsets=0,1,2,3,0\nconsumed=alpha|beta|gamma\noccupancy=1\nnext=delta\n","stderr":""}} -->
```python
capacity = 4
slots = [None] * capacity
head = 0
tail = 0

for item in ["alpha", "beta", "gamma", "delta"]:
    assert 0 <= head - tail < capacity
    slots[head % capacity] = item
    head += 1

offsets = [position % capacity for position in range(head + 1)]
consumed = []
for _ in range(3):
    assert 0 < head - tail <= capacity
    consumed.append(slots[tail % capacity])
    tail += 1

print("offsets=" + ",".join(map(str, offsets)))
print("consumed=" + "|".join(consumed))
print(f"occupancy={head - tail}")
print("next=" + slots[tail % capacity])
```

The toy uses unbounded integers and sequential execution. It omits atomics, memory order, cache behavior, multiple processes, generation metadata, crashes, corruption, blocking, and lifecycle.

## Alternatives and Trade-Offs

- Named POSIX objects support unrelated processes but require secure discovery and stale-object cleanup.
- Anonymous inherited mappings avoid public names but couple setup to process ancestry or descriptor transfer.
- File-backed mappings aid inspection and potential persistence but add filesystem and durability concerns.
- Memfd-style objects support descriptor authority and Linux sealing but reduce portability.
- Mutex-protected structures simplify reasoning but can contend and require owner-death policy.
- Lock-free rings can reduce blocking but increase memory-order, wrap, reclamation, and crash complexity.
- Fixed-size layouts simplify validation but can waste memory or require replacement for growth.
- Dynamic shared allocators improve flexibility but enlarge corruption and synchronization surfaces.
- Shared memory can reduce copies while pipes or sockets provide stronger framing, isolation, and peer-lifecycle mediation.

## Failure Modes and Misconceptions

1. **“Mapped in both processes means synchronized.”** common storage does not order conflicting accesses.
2. **“`volatile` makes IPC safe.”** it neither supplies mutual exclusion nor a complete memory-order protocol.
3. **“Any mutex in shared pages works.”** the primitive must explicitly support and be configured for process sharing.
4. **“The same object has the same address.”** mappings can use different process-local bases.
5. **“Raw pointers are portable offsets.”** a pointer embeds one address-space interpretation.
6. **“Name existence means initialization completed.”** creation precedes sizing, layout construction, and publication.
7. **“Unlink immediately invalidates mappings.”** name removal and referenced object lifetime differ.
8. **“Closing the descriptor unmaps memory.”** descriptor and mapping lifetimes are separate.
9. **“A lock-free queue survives process death.”** reservations and reclamation can still be abandoned.
10. **“Truncation safely tells readers the new size.”** active mappings and accesses can fault or race.
11. **“`MAP_SHARED` means durable.”** visibility and crash persistence are separate.
12. **“Padding always improves performance.”** it trades coherence against footprint and locality.
13. **“Offsets are safe because they are not pointers.”** arithmetic, bounds, alignment, and generation still require validation.
14. **“One fast microbenchmark proves the design.”** topology, contention, faults, recovery, and tail latency may reverse the result.

## Worked Examples

### Example 1

Two unrelated processes map the same object at different bases. Stored offset 256 identifies the same object byte for both; a stored raw address from the creator is meaningless or dangerous in the joiner.

### Example 2

A creator exposes the name, then slowly initializes the header. A joiner sees zero length or partial fields. An `INITIALIZING` state plus release-published `READY` prevents premature interpretation.

### Example 3

A programmer uses `MAP_PRIVATE` and wonders why updates do not reach the peer. Copy-on-write pages provide private modifications; the transport requires `MAP_SHARED` plus synchronization.

### Example 4

Two producers increment a shared head with ordinary loads and stores. Both reserve the same slot. Mutual exclusion or an atomic reservation algorithm is required, followed by a distinct commit publication.

### Example 5

A producer dies after reserving slot 12 but before commit. Consumers cannot wait forever. Sequence metadata and a coordinator-authorized repair policy identify and retire or reconstruct the abandoned reservation.

### Example 6

A peer supplies `offset=2^64-8` and `length=32`. Addition wraps if checked afterward. Reject using subtraction-based bounds or checked arithmetic before address formation.

### Example 7

The coordinator unlinks an old generation and creates a new object under the same name. Existing processes remain on the old object. A generation handshake prevents the two groups from assuming one shared queue.

### Example 8

Two counters updated by different processes share one cache line. Correct results arrive slowly under contention. Separating hot ownership domains reduces invalidations, verified against the larger footprint.

### Example 9

A process truncates a mapped object while readers still access the removed range. Readers can fault. Replace-and-handoff with acknowledgements avoids changing storage beneath live references.

### Example 10

A diagnostic process copies header fields without synchronization and reports impossible occupancy. A sequence counter around the snapshot makes it retry when a writer overlaps the observation.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies rings, indexing, generations, and reclamation. [Database Engineering](../../18-database-engineering/ROADMAP.md) connects mapped storage to transactions, logging, and crash recovery.

[Security Engineering](../../25-security-engineering/ROADMAP.md) frames shared writable state as authority and input validation. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies capacity, failure, observability, and assurance analysis. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) generalizes publication, epochs, failure detection, and membership.

Within this program, [OS-023](023-mutexes-semaphores-and-condition-variables.md), [OS-026](026-pipes-and-byte-streams.md), [OS-028](../ROADMAP.md), [OS-029](../ROADMAP.md), and [OS-030](../ROADMAP.md) connect synchronization and IPC choices.

## References

- Linux man-pages project, [shm_overview(7)](https://man7.org/linux/man-pages/man7/shm_overview.7.html), current page checked 2026-09-04. POSIX shared-memory lifecycle, interfaces, persistence, permissions, and synchronization.
- Linux man-pages project, [shm_open(3)](https://man7.org/linux/man-pages/man3/shm_open.3.html), current page checked 2026-09-04. Creation, zero initial length, flags, descriptors, unlinking, errors, and examples.
- Linux man-pages project, [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html), current page checked 2026-09-04. Shared and private mappings, protection, offsets, fork inheritance, caveats, and faults.
- Linux man-pages project, [ftruncate(2)](https://man7.org/linux/man-pages/man2/ftruncate.2.html), current page checked 2026-09-04. Object sizing, extension, truncation, seals, limits, and errors.
- Linux man-pages project, [mprotect(2)](https://man7.org/linux/man-pages/man2/mprotect.2.html), current page checked 2026-09-04. Mapping protection changes, alignment, access faults, and platform considerations.
- Linux man-pages project, [msync(2)](https://man7.org/linux/man-pages/man2/msync.2.html), current page checked 2026-09-04. Mapped-file synchronization flags, alignment, completion, invalidation, and errors.
- Linux man-pages project, [memfd_create(2)](https://man7.org/linux/man-pages/man2/memfd_create.2.html), current page checked 2026-09-04. Anonymous RAM-backed descriptors, close-on-exec, sealing, huge pages, and errors.
- Linux man-pages project, [pthread_mutexattr_setpshared(3)](https://man7.org/linux/man-pages/man3/pthread_mutexattr_setpshared.3.html), current page checked 2026-09-04. Process-shared mutex attributes, portability, and errors.
- Linux man-pages project, [pthread_mutexattr_setrobust(3)](https://man7.org/linux/man-pages/man3/pthread_mutexattr_setrobust.3.html), current page checked 2026-09-04. Robust mutex owner death, inconsistent protected state, recovery, and nonrecoverability.
- The Open Group, [mmap](https://pubs.opengroup.org/onlinepubs/9799919799/functions/mmap.html), POSIX.1-2024, checked 2026-09-04. Portable mapping, shared-object, synchronization-object, and unmapping requirements.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching address spaces, page tables, fork, locking, sleep and wakeup, and shared kernel structures.

## Exercises

### Exercise 1

Design a versioned shared-memory header and attachment protocol. Include initialization, offsets, bounds, permissions, generation, creator failure, and compatibility.

### Exercise 2

Specify a bounded ring for multiple producers and one consumer. Separate reservation and commit, define memory ordering, wrap, waiting, and producer death.

### Exercise 3

Construct a lifecycle table for name, descriptor, mapping, object, and participant across create, attach, close, unlink, restart, and replacement.

### Exercise 4

Analyze a resize beneath active mappings and redesign it using fixed capacity, quiescence, or replace-and-handoff. Include failure and rollback.

### Exercise 5

Build an assurance plan comparing shared memory with pipes for a safety-relevant telemetry channel. Cover performance, isolation, corruption, recovery, and evidence.

## Answers to the Exercises

### Answer 1

Use magic, major and minor format version, total object size, header size, feature flags, generation, initialization state, creator identity, capacity, region offsets and lengths, and integrity metadata. Create with exclusive semantics and restrictive permissions, size and map, initialize process-shared primitives and payload, then release-publish `READY`.

A joiner opens, checks identity and permissions, obtains size, maps only a valid interval, acquire-loads state, and validates every field with checked arithmetic before translating offsets. It rejects incompatible mandatory features. A coordinator detects creator failure in `INITIALIZING` under an explicit liveness assumption and either securely replaces the generation or performs a defined repair; arbitrary joiners do not guess.

### Answer 2

Use monotonic logical head and tail with a maximum distance no greater than `C`; each physical slot has a sequence and state. A producer atomically reserves a unique logical position only when capacity permits, writes the bounded record, then release-publishes its committed sequence. The consumer acquire-observes the next sequence, reads payload, and publishes the slot free for a future generation.

State integer width and wrap comparison, producer count, atomic lock-freedom assumptions, cache layout, and wait predicate. A dead producer can strand a reservation, so add owner and epoch metadata plus coordinator repair, or use a robust locked design. Notification is advisory; all actors recheck state. Backpressure bounds queued reservations and wait time.

### Answer 3

The name exists from successful creation until unlink and supports discovery. Each descriptor exists from open or inheritance until close and can establish mappings or management operations. Each mapping remains in one process until unmap or process exit and can outlive descriptor close. Object storage survives while platform references require it, even after name removal. Participant membership persists only under the protocol's attach and detach rules.

Restart can retain or replace an object according to policy. Replacement uses a new generation, publishes its handle or name, rejects cross-generation references, waits for acknowledged detachment or a justified reclamation boundary, then removes the old generation. No layer is used as evidence that another layer ended.

### Answer 4

Shrinking beneath readers invalidates their size assumptions and may make access fault. In-place growth also leaves old mappings too short. Fixed capacity avoids the transition if a defensible maximum is affordable. Quiescent resize blocks new access, waits for all active references to exit, changes size, remaps every participant, validates, then resumes; coordinator failure needs takeover or rollback state.

Replace-and-handoff creates and fully initializes a new object, publishes a new generation, migrates bounded state, asks participants to attach and acknowledge, stops writes to the old object, then reclaims it after the defined grace rule. Failure before publication discards the new object; failure after publication is resolved by generation and coordinator election policy, never by silently truncating the old mapping.

### Answer 5

Specify throughput, latency percentiles, maximum queueing, data size, topology, page-fault policy, and overload. Benchmark both transports with representative cores, NUMA placement, contention, failures, and instrumentation. Shared memory is assessed for atomic protocol, corruption containment, stale mappings, owner death, bounds, permissions, and recovery. Pipes are assessed for copying, framing, capacity, descriptor lifecycle, peer closure, and kernel isolation.

Fault injection covers producer crash at each state transition, corrupt metadata, slow consumer, exhausted capacity, restart, cancellation, permission error, and cleanup. Preserve raw data and environment. Named OS, concurrency, security, performance, operations, safety, and independent-verification reviewers judge whether reduced copies justify the larger shared failure domain. A passing toy or benchmark is not certification.
