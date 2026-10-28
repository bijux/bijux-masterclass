---
module_id: OS-008
program: Operating Systems
level: 1
module_number: 8
title: Kernel Memory Allocation
status: complete
last_verified: 2026-09-04
---

# Kernel Memory Allocation

## One-Page Review

### Governing question

How should a kernel obtain, place, initialize, account for, and reclaim memory while respecting execution context, physical layout, latency, locality, security, and failure constraints?

### Essential definitions

- A **page-frame allocator** manages physical memory in page-sized units, often grouping free frames into power-of-two blocks.
- A **buddy allocator** splits a larger aligned block to satisfy an order and coalesces free partners when their addresses and orders make them buddies.
- A **slab or object cache** divides backing pages into reusable, typed or size-classed objects and may retain constructed state or debugging metadata.
- **Internal fragmentation** is unusable space inside granted allocations; **external fragmentation** is free space that exists but not in a shape or placement satisfying a request.
- An **allocation context** states whether the caller may sleep, reclaim, perform I/O, use reserves, or accept failure.
- **Virtual contiguity** means adjacent virtual addresses; **physical contiguity** means adjacent page frames. Neither implies the other.
- A **memory reserve** preserves capacity for paths needed to restore progress; it is not general spare capacity.

### Central model, mechanism, or theorem

Treat allocation as a constrained request rather than a byte count:

`request = size × alignment × physical_shape × addressability × node × context × lifetime × initialization × failure_policy`.

The allocator chooses an admissible source and may split, refill, reclaim, compact, or fall back according to that contract. Success is correct only if the returned region meets every promised property. Failure handling is part of the caller's design, and freeing is correct only when ownership has ended and the matching allocator, size, order, and context rules are satisfied.

### Critical invariants

- Every allocatable byte or page is in exactly one well-defined state: reserved, free in one allocator structure, or owned by one live allocation contract.
- Free blocks do not overlap; buddy lists contain correctly aligned blocks of their stated order; coalescing never crosses a zone or incompatible mobility boundary.
- Allocation context is at least as restrictive as the call path: non-sleeping paths never enter reclaim or other blocking work.
- Object-cache metadata, freelists, redzones, constructors, and ownership states agree before an object becomes visible.
- Returned memory satisfies documented alignment, addressability, NUMA, zeroing, physical-contiguity, and DMA requirements—no stronger property is inferred.
- Every successful allocation has one compatible release after its final use; partial construction and failure unwind all acquired resources exactly once.
- Reserves, watermarks, accounting, and limits preserve system progress and prevent one origin or tenant from consuming unbounded kernel memory.

### Common failures

Common mistakes are allocating while holding a lock that reclaim may need, using a sleeping mode in interrupt context, requesting high-order pages when scattered pages suffice, assuming `vmalloc` memory is physically contiguous, treating `GFP_ATOMIC` as guaranteed success, failing to check multiplication overflow, exposing uninitialized padding, mismatching allocator and release function, double freeing, retaining stale pointers, exhausting emergency reserves, ignoring NUMA fallback, and benchmarking only average latency on an idle machine.

### Compact example

A network driver needs receive descriptors in hard-interrupt context. Initialization allocates a bounded pool with the device's DMA API, maps it under the device's addressing constraints, zeroes security-sensitive fields, and publishes descriptors only after initialization. The interrupt path takes a descriptor without sleeping; if the pool is empty, it applies a declared drop-and-account policy. Teardown stops device DMA, prevents new acquisitions, drains in-flight ownership, unmaps each descriptor, and releases it through the matching API. A general kernel heap allocation in the interrupt would not establish DMA reachability, bounded latency, or physical layout.

### Connections

[OS-006](006-boot-process-and-kernel-initialization.md) establishes early memory discovery and allocator handoff. [OS-007](007-kernel-data-structures.md) supplies free lists and ownership structures; [OS-019](../ROADMAP.md) develops virtual memory; [OS-021](../ROADMAP.md) develops kernel synchronization; and [OS-041](../ROADMAP.md) develops NUMA. Hardware addressability belongs to [Computer Architecture](../../23-computer-architecture/ROADMAP.md), while bounded resource evidence belongs to [Systems Engineering](../../26-systems-engineering/ROADMAP.md).

## Governing Question

Kernel code cannot rely on an unlimited, uniform heap. It allocates before the normal memory manager exists, from interrupt and process contexts, for CPUs and devices with different addressability, on NUMA machines, and while memory pressure can recursively invoke filesystems, block I/O, or drivers. A request can fail despite abundant total free memory because the caller needs alignment, a contiguous run, a particular zone, or a nearby node.

The allocator is also part of the kernel's security boundary. An unchecked element count can wrap to a small allocation followed by an overwrite. Reused memory can disclose secrets if it is not initialized at the correct trust boundary. A corrupted freelist can turn a later allocation into a controlled write. A use-after-free can make legitimate allocator reuse appear to mutate a live object.

The governing question is therefore not simply “which function returns bytes?” It is how to express the real resource contract, select the correct allocator layer, preserve progress under pressure, bind ownership to lifetime, and collect evidence that both fast and failure paths behave within their claims.

## Why This Matters

Allocation is on nearly every kernel path. Process creation needs task and stack objects; file systems need inodes and buffers; networking needs packet metadata; virtual memory needs page tables; drivers need DMA-visible storage. A small fast-path regression multiplies across the machine, while a rare reclaim deadlock can stop it entirely.

Memory pressure couples otherwise separate subsystems. A filesystem allocation may enter reclaim, which writes dirty pages through that filesystem and tries to reacquire a lock held by the allocator's caller. A request on one NUMA node may fall back remotely, preserving correctness but increasing latency and interconnect traffic. A high-order allocation may invoke compaction and stall even when an order-zero fallback would have been cheap.

Failure policy shapes availability. Returning an error may be correct for a new user request but impossible after a transaction has crossed an irreversible boundary. Preallocating before commitment, reserving a bounded pool, or structuring operations so they can unwind is generally safer than declaring an allocation unable to fail. Emergency capacity must be protected for agents that actually restore memory or I/O progress.

## Prerequisites and Retrieval

Recall from [OS-004](004-interrupts-and-exceptions.md) that hard-interrupt context cannot sleep. Recall from [OS-006](006-boot-process-and-kernel-initialization.md) that early boot begins with firmware memory descriptions and transitions into steady-state allocators. Recall from [OS-007](007-kernel-data-structures.md) that reachability, ownership, and reclamation are separate.

Retrieve these distinctions:

- a virtual address is not a physical address and may not even have backing until a fault or mapping operation;
- page order `k` denotes `2^k` base pages, not `k` pages;
- available bytes do not imply an available aligned contiguous block;
- allocation success does not imply zeroed contents unless the API contract says so;
- a non-sleeping request may fail more readily because it forbids reclaim and waiting;
- an object returned to a cache is dead to its former owner even if the bytes have not changed;
- allocator bookkeeping, caller ownership, device ownership, and user visibility are distinct states.

## Learning Objectives

After completing this module, you should be able to:

- derive an allocation contract from size, alignment, placement, context, lifetime, initialization, and failure requirements;
- explain early boot allocation and the transition to steady-state page and object allocators;
- simulate buddy splitting and coalescing and state the invariants that make them safe;
- distinguish page-frame, size-class, typed-object, virtually contiguous, and DMA allocation;
- explain internal and external fragmentation, mobility grouping, reclaim, and compaction;
- select allocation context and fallback behavior without creating recursion or reserve abuse;
- reason about per-CPU caches, NUMA placement, watermarks, and tail latency;
- prevent overflow, information exposure, allocator mismatch, double free, and use-after-free;
- design fault injection, accounting, tracing, sanitizers, and workload-representative benchmarks;
- identify deployment or safety claims requiring accountable human review.

## Core Exposition

### Specify the complete request

Begin with the minimum bytes and required alignment. Use overflow-checked array and flexible-structure helpers rather than multiplying untrusted counts manually. State whether the memory must be physically contiguous, merely virtually contiguous, accessible by a device, below an address boundary, local to a NUMA node, movable, reclaimable, executable, persistent, or visible to user space.

Then describe the call path. Can it sleep? Does it hold a spinlock? Can it recurse from reclaim? Is it an interrupt, fault, teardown, or recovery path? What latency is permitted? May the request trigger filesystem or device I/O? Can the caller accept a smaller object, scattered pages, deferred work, a preallocated reserve, dropped work, or an error?

Finally describe lifetime and initialization. Who owns the result, when is it published, what fields must be zero, and which release API matches it? Does a device retain access after the CPU stops using the object? Can an RCU reader or callback retain a pointer? These answers determine more than the nominal allocator name.

### From boot allocator to page allocator

Before normal kernel allocation is operational, boot code needs memory for page tables, topology descriptions, allocator metadata, and subsystem initialization. An early allocator commonly records usable physical ranges and reservations, then makes simple aligned allocations from those ranges. It must exclude the kernel image, firmware data, device windows, initrd, and already allocated metadata.

Once page metadata, zones, locks, and CPU state are ready, unused early allocations can be released into the steady-state page allocator where the architecture permits. The handoff needs a ledger: every physical interval is reserved, permanently owned, or transferred exactly once. Losing a range wastes memory; transferring a live range enables corruption.

The steady-state allocator manages page frames within topology and addressability boundaries. In Linux, zones describe physical ranges with constraints, per-CPU page sets serve common small requests locally, and global free areas organize larger power-of-two blocks. These are implementation-specific mechanisms illustrating general layering.

### Buddy allocation

For base-page size `P`, an order-`k` block contains `2^k` pages and `P × 2^k` bytes. A request searches for the smallest available order at least as large as required. If only a higher-order block exists, the allocator repeatedly splits it into two equal buddies, returns or continues splitting one, and inserts the other into the next lower free set.

For a block index `b` measured in base pages, the order-`k` buddy index is `b xor 2^k`, provided both blocks lie in the same managed arena and satisfy alignment. On release, the allocator checks whether that buddy is free at the same order. If so, it removes both children, inserts their aligned parent at order `k + 1`, and repeats.

The key invariant is partitioning: free blocks do not overlap allocated blocks or each other, and each free block appears once at its correct order. The XOR relation alone does not authorize merging across a zone boundary, hole, reserved region, mobility class, or incompatible state.

Buddy allocation makes coalescing efficient and naturally aligns power-of-two runs. It rounds requests to powers of two and suffers when long-lived pages fragment the arena. Order-zero success says little about the probability or latency of a high-order request.

### Object and size-class caches

Kernel objects are often smaller than a page and repeatedly created. An object allocator obtains pages from the lower layer, divides them into slots, and tracks free and occupied objects. General caches group requests into size classes; typed caches can know object size, alignment, constructor rules, and debugging policy.

Reusing cached objects avoids returning to the page allocator on every operation and can preserve initialized state when the API makes that safe. It also creates obligations. Constructors must not leave identity, credentials, pointers, or locks in a state inherited by the next owner. Destructors and release paths must handle partial initialization. Padding can contain old data even when visible fields appear initialized.

Per-CPU freelists make common allocation and release local, reducing shared-lock and cache-line traffic. Refilling or draining them accesses shared or per-node state. Local caches consume memory, make global free counts approximate, and can strand capacity unevenly across CPUs. CPU hotplug needs an explicit drain and transfer protocol.

### Physical and virtual contiguity

A page allocator can return a physically contiguous order block. A kernel heap built on it may provide physical contiguity only within documented size and implementation limits. A virtual-area allocator can reserve one continuous virtual range and map unrelated page frames behind it, allowing large CPU-accessible buffers without requiring a physically continuous run.

Virtual contiguity is often sufficient for CPU algorithms and is hostile to code that translates only the first address and assumes the rest follows physically. Some virtual allocators also add page-table setup, translation lookups, and TLB costs. They may not be valid in atomic context.

Devices introduce a third address space: the DMA address observed by the device. An IOMMU may map scattered physical pages into a contiguous device-visible range, but only the DMA API establishes that contract and handles cache coherency, masks, and mapping lifetime. A CPU pointer, physical address, and DMA address are not interchangeable.

### Allocation context and reclaim recursion

Allocation flags describe what the allocator may do, not how important the programmer feels. A normal sleepable request may wait and enter direct reclaim. A non-sleeping request forbids those paths and therefore needs a failure or reserve-backed fallback. Linux documents `GFP_KERNEL`, `GFP_NOWAIT`, and `GFP_ATOMIC` as distinct policies; exact flags and guarantees must be read from the targeted kernel version.

Reclaim can call into storage, filesystems, writeback, shrinkers, callbacks, and other memory users. If the caller holds a resource that a reentered path needs, the allocation can deadlock. Scoped restrictions or prior allocation are preferable to scattering overly restrictive flags, because unnecessary restrictions make failures more likely and obscure the true dependency.

An atomic allocation is not a success guarantee. Emergency reserves exist to preserve progress for eligible callers. Spending them on optional work can prevent the network, storage, or memory-management action that would free resources. Bounded preallocated pools make capacity and exhaustion behavior explicit.

### Pressure, watermarks, reclaim, and compaction

Allocators keep some free capacity to satisfy bursts and progress-critical work. Zone watermarks can wake background reclaim before exhaustion and make direct allocators reclaim or throttle under deeper pressure. Per-CPU counters and caches complicate the exact global view, so thresholds account for drift and batch movement.

Reclaim attempts to release clean cache, write dirty data, invoke registered shrinkers, or otherwise make pages reusable. It can recover bytes without producing a large contiguous run. Compaction migrates movable pages to concentrate free space. It consumes CPU and memory bandwidth and can stall a requester; pinned or unmovable pages limit success.

Mobility grouping tries to keep movable, reclaimable, and unmovable allocations from interleaving destructively. This is a policy aid, not a proof that fragmentation disappears. High-order callers need a fallback, admission limit, or pre-reserved region when failure or latency is unacceptable.

### NUMA and topology

On a NUMA system, local memory generally offers lower access cost than remote memory for the executing CPU. Placement policy may prefer, bind, or interleave across nodes, subject to allowed-node constraints and fallback. A local allocation followed by thread migration can become remote; a remote fallback may preserve service at a performance cost.

Per-node object caches and page lists reduce cross-node traffic but can strand memory and complicate balancing. Allocation measurement must record CPU affinity, node policy, fallback, page migration, and first-touch behavior. Reporting only total free memory hides whether the required node or zone is depleted.

Topology also changes synchronization cost. A single allocator lock or globally written statistic can bounce across sockets. Batching improves throughput but increases temporal and spatial imbalance. The appropriate batch size depends on object lifetime, pressure, CPU count, and workload burstiness.

### Initialization, hardening, and ownership

Fresh allocation does not generally mean zero-filled memory. Use a zeroing API or explicit complete initialization when prior contents could cross a trust boundary. Zero-before-release can be necessary for secrets, while zero-on-allocation prevents stale exposure to the next owner; the threat model determines which points are required. Compiler optimization, device copies, crash dumps, and caches complicate secret erasure claims.

Allocator hardening may encode freelist pointers, randomize layout, quarantine freed objects, poison memory, add redzones, or validate metadata. These measures improve detection or exploitation resistance but have overhead and do not repair an incorrect lifetime protocol. Kernel Address Sanitizer targets out-of-bounds and use-after-free classes; Kernel Memory Sanitizer targets uses of uninitialized values; leak detection and page-owner tracing address different evidence.

Ownership transitions must be explicit: allocated and private, partially initialized, published, borrowed, device-owned, retired, quarantined, and reusable are different states. Releasing memory while a timer, worker, interrupt, RCU reader, or device can still access it is a caller lifetime bug even if the allocator behaves perfectly.

### Failure handling and accounting

Every allocation point needs a failure decision. Before externally visible commitment, unwind in reverse acquisition order. After commitment, use pre-reserved resources, roll-forward recovery, deferred work, or a defined degraded mode. Retrying without evidence of progress can turn memory pressure into an infinite stall.

No-fail allocation transfers risk rather than removing it. It may wait indefinitely, trigger disruptive reclaim, or deadlock if the caller prevents progress. Use it only when a reviewed invariant proves failure cannot be surfaced and the request and context permit eventual progress; preallocation or transaction redesign is often clearer.

Attribute memory to its origin: subsystem, tenant, cgroup, namespace, request class, or device. Enforce limits before global exhaustion, and make charges follow ownership transfers. Untrusted user-triggered kernel allocations require accounting and amplification bounds. A tiny request must not create unbounded metadata, deferred work, or pinned memory.

### Measurement and evidence

Measure allocation and free latency distributions, failure counts, reclaim and compaction time, requested versus granted bytes, free blocks by order, cache refill and drain, remote-node fallback, reserve use, and memory retained in per-CPU caches. Record workload, kernel configuration, allocator, CPU and node placement, memory pressure, and instrumentation overhead.

Fault injection should exercise every fallible allocation and partial-construction unwind. Pressure tests mix allocations of different sizes and lifetimes, not merely repeat one size. Concurrency tests vary CPUs, interrupts, teardown, and hotplug. Sanitizers, poisoning, and leak tools are complementary observations; a clean run is not a proof of absence.

Tail latency matters because a fast cache hit and a reclaim-compaction slow path share one API. Benchmark cold startup, steady state, fragmentation, near-limit operation, and recovery. Validate that observability does not itself require large allocations or locks on the failing path.

## Definitions and Notation

Let `P` be the base-page size. An order-`k` block has

`pages(k) = 2^k` and `bytes(k) = P × 2^k`.

If a request needs `n` pages, the smallest covering order is

`k = ceil(log2(n))`, for `n > 0`,

and the internal page waste is `2^k - n` when no suballocation uses the remainder. For a block starting at page-frame index `b`, its candidate same-order buddy begins at `b xor 2^k`; arena membership and state must still be checked.

Let `F_k` be the set of free order-`k` blocks. A buddy partition requires blocks in all `F_k` to be aligned to `2^k`, pairwise disjoint, and disjoint from allocated or reserved frames. If both children of an admissible parent are free at order `k`, the canonical coalesced representation removes them from `F_k` and inserts the parent into `F_(k+1)`.

For an object request of `s` bytes served by class size `c ≥ s`, internal waste is `c - s`, excluding allocator metadata and slab-edge loss. External fragmentation cannot be inferred from total free bytes; it depends on the distribution, alignment, zones, nodes, mobility, and pinned state of free and occupied regions.

Define an allocation contract `C = (s, a, q, z, n, x, i, l, f)`: size `s`, alignment `a`, physical or device shape `q`, addressability/zone `z`, node policy `n`, execution context `x`, initialization `i`, lifetime `l`, and failure policy `f`. A result is admissible only if it satisfies every component of `C`.

## Mechanisms, Invariants, or Proof Structure

Review kernel allocation through eight obligations.

**Shape integrity.** Size calculations do not overflow; granted size and alignment cover the object; physical, virtual, and DMA contiguity are distinguished.

**Partition integrity.** Reserved, free, cached, quarantined, and allocated regions form a non-overlapping ownership partition. Buddy order and slab membership metadata agree with physical state.

**Context integrity.** Reclaim, waiting, I/O, callbacks, and locks permitted by the allocation mode are compatible with every caller and nested path.

**Lifetime integrity.** Publication, references, callbacks, interrupts, device access, teardown, and release establish one final handoff back to the matching allocator.

**Progress integrity.** Watermarks, reserves, pools, limits, reclaim, compaction, and retry rules preserve agents capable of freeing resources and bound optional consumption.

**Locality integrity.** Zone and NUMA placement meet hard constraints, while fallbacks and migrations are visible as performance events rather than hidden correctness assumptions.

**Security integrity.** Initialization, accounting, isolation, hardening, and overflow checks prevent stale disclosure, cross-tenant amplification, and metadata exploitation within their stated coverage.

**Evidence integrity.** Tests distinguish cache hits from slow paths, inject failure at each acquisition, reproduce fragmentation and topology, and scope sanitizer or benchmark claims.

The executable model below implements buddy splitting and coalescing for a 16-page arena. It checks a partition after each operation; it is not a concurrent allocator.

<!-- bijux-verify: {"id":"toy-buddy-allocation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial=4:0\nalloc-a=0:2\nalloc-b=4:1\nafter-alloc=1:6,3:8\nafter-free-a=1:6,2:0,3:8\nafter-free-b=4:0\n","stderr":""}} -->
```python
class BuddyArena:
    def __init__(self, maximum_order):
        self.maximum_order = maximum_order
        self.free = {order: set() for order in range(maximum_order + 1)}
        self.free[maximum_order].add(0)
        self.owned = {}

    def allocate(self, requested_order):
        source = requested_order
        while source <= self.maximum_order and not self.free[source]:
            source += 1
        if source > self.maximum_order:
            return None
        start = min(self.free[source])
        self.free[source].discard(start)
        while source > requested_order:
            source -= 1
            self.free[source].add(start + (1 << source))
        self.owned[start] = requested_order
        self.check_partition()
        return start, requested_order

    def release(self, allocation):
        start, order = allocation
        if self.owned.get(start) != order:
            return False
        self.owned.pop(start)
        while order < self.maximum_order:
            buddy = start ^ (1 << order)
            if buddy not in self.free[order]:
                break
            self.free[order].discard(buddy)
            start = min(start, buddy)
            order += 1
        self.free[order].add(start)
        self.check_partition()
        return True

    def check_partition(self):
        pages = []
        for start, order in self.owned.items():
            pages.extend(range(start, start + (1 << order)))
        for order, starts in self.free.items():
            for start in starts:
                assert start % (1 << order) == 0
                pages.extend(range(start, start + (1 << order)))
        assert sorted(pages) == list(range(1 << self.maximum_order))

    def summary(self):
        entries = []
        for order in range(self.maximum_order + 1):
            for start in sorted(self.free[order]):
                entries.append(f"{order}:{start}")
        return ",".join(entries) or "empty"


arena = BuddyArena(4)
print("initial=" + arena.summary())
a = arena.allocate(2)
print(f"alloc-a={a[0]}:{a[1]}")
b = arena.allocate(1)
print(f"alloc-b={b[0]}:{b[1]}")
print("after-alloc=" + arena.summary())
arena.release(a)
print("after-free-a=" + arena.summary())
arena.release(b)
print("after-free-b=" + arena.summary())
```

Passing proves the sequential partition and expected coalescing only for this fixed arena and request sequence. It does not model zones, holes, per-CPU caches, concurrency, metadata corruption, reclaim, compaction, NUMA, DMA, or a production kernel.

## Alternatives and Trade-Offs

**Buddy blocks versus arbitrary extents.** Buddy allocation gives simple alignment, splitting, and coalescing. Arbitrary extents can fit sizes more tightly but require more complex indexing and merge logic.

**General size classes versus typed caches.** General caches reduce the number of allocator instances. Typed caches can encode construction, alignment, accounting, and diagnostics but retain memory and expand operational surface.

**Physical versus virtual contiguity.** Physical runs serve devices or huge mappings but fragment and become expensive at higher orders. Virtual contiguity composes scattered frames for CPU access but adds mapping cost and does not meet raw physical constraints.

**On-demand allocation versus preallocation.** On-demand use tracks actual load and saves idle memory. Preallocation bounds critical-path latency and failure but reserves capacity that other work cannot use freely.

**Per-CPU versus shared caches.** Per-CPU state improves locality and contention. Shared caches simplify accounting and pooling; batching between them trades synchronization for imbalance.

**Local NUMA placement versus fallback.** Strict locality provides predictable placement but can fail amid remote free capacity. Fallback improves availability while creating remote access and performance variability.

**Immediate reuse versus quarantine.** Immediate reuse maximizes capacity and locality. Quarantine delays reuse to expose stale accesses but consumes memory and can worsen pressure.

## Failure Modes and Misconceptions

1. **“Free memory means the allocation should succeed.”** Shape, order, alignment, zone, node, reserves, and context constrain usable memory.
2. **“Order four means four pages.”** It means `2^4`, or sixteen, base pages.
3. **“A kernel virtual buffer is physically contiguous.”** Only the chosen API's documented contract establishes physical layout.
4. **“A DMA address is a physical address.”** IOMMUs and platform mapping make device addresses a distinct contract.
5. **“Atomic allocation cannot fail.”** It forbids sleeping and may access limited reserves; callers still need an exhaustion policy.
6. **“Retrying makes an allocation reliable.”** Retry without possible progress can livelock or deadlock.
7. **“No-fail removes failure.”** It can convert failure into unbounded latency, reclaim disruption, or dependency deadlock.
8. **“Zeroing fields prevents disclosure.”** Padding, unions, trailing storage, and device-visible regions also require a trust-boundary review.
9. **“Freeing ends all access.”** Timers, workers, readers, interrupts, and devices may retain ownership.
10. **“The same pointer can be freed through any heap API.”** Allocator identity and release contract must match.
11. **“Total fragmentation is one percentage.”** Internal waste and unavailable physical shapes across zones and nodes are different phenomena.
12. **“Per-CPU caches are globally free memory.”** Capacity may be locally retained and global counts may be approximate.
13. **“A sanitizer pass proves memory safety.”** It observes configured executions and bug classes, not all histories.
14. **“Average allocation latency predicts production.”** Reclaim, compaction, refills, topology, and pressure dominate the tail.

## Worked Examples

### Example 1

**Question:** A driver needs 64 KiB for CPU-only statistics. Must it request physically contiguous pages?

**Reasoning:** CPU code needs an addressable virtual range, not necessarily adjacent frames. A virtual allocator or segmented representation avoids a fragile high-order physical request.

**Conclusion:** Demand physical shape only when an interface actually requires it.

### Example 2

**Question:** Four adjacent order-zero pages are free. Does an order-two allocation necessarily succeed?

**Reasoning:** They must form one correctly aligned buddy block in the same arena and compatible state. Adjacent frames crossing boundaries or represented as unavailable cannot be merged.

**Conclusion:** Count, adjacency, alignment, and allocator membership jointly determine eligibility.

### Example 3

**Question:** A spinlock holder calls a normal sleeping allocator. What can go wrong?

**Reasoning:** The allocator may sleep or enter reclaim. Sleeping under a spinlock is invalid, and reclaim may need the same lock or subsystem.

**Conclusion:** Allocate before the critical section, use a bounded non-sleeping pool, or redesign the ownership transition.

### Example 4

**Question:** A cache returns an object whose visible fields were reset, but a user-visible copy includes structure padding. Is it safe?

**Reasoning:** Padding may retain bytes from the previous owner and cross a trust boundary.

**Conclusion:** Serialize explicit fields or initialize the complete exported representation.

### Example 5

**Question:** An order-zero allocator succeeds rapidly in a stress test. What does that say about huge-page allocation?

**Reasoning:** Small requests can use scattered free pages and per-CPU caches. Huge pages need large aligned runs and may trigger compaction.

**Conclusion:** Test the actual orders, fragmentation histories, and slow-path latency.

### Example 6

**Question:** A request bound to NUMA node 0 fails while node 1 has free memory. Is the allocator broken?

**Reasoning:** A strict binding contract forbids fallback. A preferred policy could fall back but would change access cost.

**Conclusion:** Placement policy determines whether remote capacity is admissible.

### Example 7

**Question:** A network receive path uses emergency reserves for optional telemetry. Why is that dangerous?

**Reasoning:** Telemetry can consume capacity reserved for operations that drain packets or restore memory progress.

**Conclusion:** Optional work must fail or defer before it threatens progress reserves.

### Example 8

**Question:** A constructor allocates three children and the third allocation fails. What must the unwind do?

**Reasoning:** The first two children and parent-private state are owned but unpublished. They must be released once in reverse dependency order without invoking teardown that assumes full initialization.

**Conclusion:** Partial-construction states need explicit ownership and compatible destructors.

### Example 9

**Question:** KASAN reports a write into a freed object after allocator reuse. Is the allocator necessarily at fault?

**Reasoning:** The former owner may have retained a callback or pointer beyond release; reuse merely made the lifetime error visible.

**Conclusion:** Trace ownership and asynchronous access before changing allocator policy.

### Example 10

**Question:** A flight-control kernel preallocates command buffers and passes allocator fault tests. Does that certify bounded safe operation?

**Reasoning:** Capacity assumptions, interrupt timing, DMA ownership, corruption containment, reset paths, hardware behavior, and safe-state transitions remain system claims.

**Conclusion:** Named real-time, safety, hardware, and security reviewers must assess evidence and residual risk; this module claims no certification.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) develops free lists, trees, bitmaps, and allocation algorithms. This module adds physical topology, interrupt context, reclaim recursion, devices, privileged failure, and lifecycle constraints. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains caches, TLBs, NUMA, IOMMUs, DMA, and memory ordering.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects overflow, stale-data disclosure, use-after-free exploitation, isolation, quotas, and hardening. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies synchronization and reclamation models for per-CPU caches and object lifetime.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames capacity, backpressure, degraded modes, hazard evidence, and accountable acceptance. Successors [OS-019](../ROADMAP.md), [OS-031](../ROADMAP.md), [OS-041](../ROADMAP.md), and [OS-060](../ROADMAP.md) deepen virtual memory, swapping, NUMA, and out-of-memory behavior.

## References

- Linux Kernel documentation, [Memory Allocation Guide](https://docs.kernel.org/core-api/memory-allocation.html), current page checked 2026-09-04. Allocator selection, GFP contexts, reclaim behavior, zeroing, arrays, and virtual versus physical contiguity.
- Linux Kernel documentation, [Memory Management APIs](https://docs.kernel.org/core-api/mm-api.html), current page checked 2026-09-04. Page, object, size, alignment, context, NUMA, and release API contracts.
- Linux Kernel documentation, [Physical Memory](https://docs.kernel.org/mm/physical_memory.html), current page checked 2026-09-04. Zones, per-CPU page sets, buddy free areas, watermarks, managed pages, and topology.
- Linux Kernel documentation, [Slab Allocation](https://docs.kernel.org/mm/slab.html), current page checked 2026-09-04. Current slab structures and the relationship between slabs, folios, pages, and partial lists.
- Linux Kernel documentation, [Short users guide for the slab allocator](https://docs.kernel.org/admin-guide/mm/slab.html), current page checked 2026-09-04. SLUB diagnostics, validation, poisoning, redzones, tracing, and performance trade-offs.
- Linux Kernel documentation, [page owner: Tracking about who allocated each page](https://docs.kernel.org/mm/page_owner.html), current page checked 2026-09-04. Page allocation provenance, stack aggregation, fragmentation analysis, and instrumentation cost.
- Linux Kernel documentation, [Page migration](https://docs.kernel.org/mm/page_migration.html), current page checked 2026-09-04. Moving physical page locations while preserving user-visible virtual addresses and limits from unmovable pages.
- Linux Kernel documentation, [NUMA Memory Policy](https://docs.kernel.org/admin-guide/mm/numa_memory_policy.html), current page checked 2026-09-04. Default, preferred, bound, and interleaved placement scopes and fallback semantics.
- Linux Kernel documentation, [Kernel Address Sanitizer](https://docs.kernel.org/dev-tools/kasan.html), current page checked 2026-09-04. Instrumentation modes and detection of out-of-bounds and use-after-free errors.
- Linux Kernel documentation, [Kernel Memory Sanitizer](https://docs.kernel.org/dev-tools/kmsan.html), current page checked 2026-09-04. Detection of uses of uninitialized values and origin reporting.
- Linux Kernel documentation, [Kernel Memory Leak Detector](https://docs.kernel.org/dev-tools/kmemleak.html), current page checked 2026-09-04. Reachability-style leak scanning, operation, and limitations.
- Linux Kernel documentation, [Dynamic DMA mapping Guide](https://docs.kernel.org/core-api/dma-api.html), current page checked 2026-09-04. Device-visible addressing, coherent allocation, mapping, synchronization, and release contracts.
- Jeff Bonwick, [The Slab Allocator: An Object-Caching Kernel](https://www.usenix.org/conference/usenix-summer-1994-technical-conference/slab-allocator-object-caching-kernel), USENIX, 1994. Primary design paper on object caches, constructors, coloring, pressure response, statistics, and debugging.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching implementation of early allocation, page freelists, locking, and page-table ownership.

## Exercises

### Exercise 1

Derive allocation contracts for a process descriptor, page table, 1 MiB CPU-only buffer, DMA command ring, interrupt-path request, and user-triggered variable array. Include size, alignment, shape, placement, context, initialization, lifetime, accounting, and failure.

### Exercise 2

For a 32-page buddy arena, execute allocations of orders 2, 3, 0, and 2, then free them in a sequence that demonstrates both failed and successful coalescing. Draw every free set and prove the partition invariant.

### Exercise 3

Design an object cache for a frequently allocated network-flow record. Cover size and alignment, constructor state, per-CPU capacity, NUMA, refill, drain, accounting, zeroing, teardown, poisoning, and memory pressure.

### Exercise 4

Design a benchmark comparing page allocation, a general size-class heap, a typed cache, and a virtually contiguous allocator. Include size/lifetime mixtures, CPU and NUMA placement, fragmentation, pressure, fault injection, instrumentation, and tail latency.

### Exercise 5

A safety controller requires command buffers during overload and cannot miss a deadline. Construct an assurance argument for its pool capacity, interrupt behavior, DMA lifetime, corruption detection, exhaustion policy, reset path, observability, and human review.

## Answers to the Exercises

### Answer 1

A process descriptor is a typed, aligned object allocated in sleepable creation context, initialized privately, accounted to the creating domain, published under process-table lifetime rules, and fallible before creation commits. A page table needs page alignment, architecture-defined physical and zeroing properties, a node policy, and release only after page-table walkers and TLB obligations end. The CPU-only 1 MiB buffer usually needs virtual rather than physical contiguity, can be allocated sleepably, and needs a segmented fallback if mapping resources fail.

The DMA ring uses the device DMA API, device mask and coherency contract, required ring alignment, bounded entries, and unmapping only after the device stops. The interrupt request uses a preallocated bounded pool or non-sleeping mode with explicit drop/defer behavior. The user-sized array uses checked multiplication, a per-origin limit and charge, complete initialization before exposure, and reversible failure. Each release must match the allocator and wait for CPU, callback, reader, and device ownership to end.

### Answer 2

Represent the initial arena as `F_5 = {0}`. Allocating order 2 splits starts 0 into free buddies at starts 16/order 4, 8/order 3, and 4/order 2, returning `(0,2)`. Allocating order 3 takes `(8,3)`. Allocating order 0 splits `(4,2)`, leaving `(6,1)` and `(5,0)`, and returns `(4,0)`. Allocating order 2 splits `(16,4)`, leaving `(24,3)` and `(20,2)`, and returns `(16,2)`.

Free `(0,2)`; it cannot merge because buddy `(4,2)` is split. Free `(4,0)`; it merges with `(5,0)` into `(4,1)`, then with `(6,1)` into `(4,2)`, then with `(0,2)` into `(0,3)`, but stops because `(8,3)` remains owned. Free `(8,3)`; it merges with `(0,3)` into `(0,4)`, but `(16,4)` is split. Free `(16,2)`; it merges with `(20,2)` into `(16,3)`, with `(24,3)` into `(16,4)`, and with `(0,4)` into `(0,5)`. At every state, expand all free and owned blocks into page indices and verify each index 0 through 31 appears exactly once.

### Answer 3

Create a cache aligned for its hot fields and architecture requirements, with a constructor that initializes locks and stable structural fields but never retains identity or credentials across owners. Allocate slabs from the appropriate node and account them to the subsystem or triggering tenant. Use bounded per-CPU freelists for fast non-sleeping access, with batched refill from per-node partial slabs and hotplug drain to an online owner.

Define high and low cache limits, pressure-driven shrinking, and a reserve solely for receive or teardown progress. Zero all externally observable record fields before publication; poison or quarantine freed records in diagnostic configurations. Teardown prevents new lookup, drains timers and RCU readers, releases flow ownership, returns objects, drains CPU caches, then destroys backing slabs. Measure remote-node fallbacks, retained free objects, refill latency, reserve depletion, and failures under mixed flow lifetimes.

### Answer 4

Use identical semantic requests and separate cases where each allocator is admissible. Sweep bytes from tiny objects through multi-page buffers; mix short, medium, and pinned lifetimes with uniform, bursty, and adversarial arrival. Run cold and warm caches on one CPU, many CPUs, one NUMA node, and cross-node placements. Create fragmentation with long-lived anchors, then test under clean memory, watermark pressure, reclaim, and compaction.

Measure latency distributions, throughput, failures, requested and granted bytes, metadata, cache refills, lock wait, remote traffic, page-table and TLB cost, reclaim and compaction time, and free blocks by order. Inject every allocation failure and verify unwind. Record allocator configuration, sanitizer or profiling overhead, CPU binding, policy, kernel version, repetitions, and uncertainty. Do not compare virtual and physical allocators on a request whose shape makes one invalid.

### Answer 5

Derive pool capacity from the maximum admitted command rate, worst acknowledged service time, retries, simultaneous channels, reset interval, and a reviewed safety margin. Allocate and DMA-map before enabling interrupts; prove that the interrupt path neither sleeps nor consumes unrelated emergency reserves. Use generation-tagged ownership states for free, CPU-filled, device-owned, completed, quarantined, and retired buffers. Stop submissions and DMA before reuse or release.

When the pool is empty, execute a predefined safe response: reject new noncritical commands, prioritize shutdown traffic through a separately bounded reserve, signal overload, and transition actuators according to the hazard analysis. Protect metadata with synchronization and integrity checks; detect stale completions, duplicate release, out-of-range indices, and deadline expiry. Test peak and sustained overload, lost interrupts, device reset, corrupted descriptors, delayed completions, CPU hotplug, and observation failure on deployed hardware. A named real-time engineer, device owner, safety authority, security reviewer, and acceptance owner must review assumptions, independence, coverage, and residual risk. This chapter and toy model provide no certification.
