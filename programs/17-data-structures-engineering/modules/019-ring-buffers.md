---
module_id: DSE-019
program: Data Structures Engineering
level: 1
module_number: 19
title: Ring Buffers
status: complete
last_verified: 2026-08-29
---

# Ring Buffers

## One-Page Review

### Governing question

How can fixed storage carry an indefinitely long logical stream while preserving FIFO order, distinguishing full from empty, making overload visible, and publishing each slot safely under the declared concurrency topology?

### Essential definitions

- A **ring buffer** reuses a fixed array cyclically: logical positions advance while physical positions wrap.
- **Read** and **write cursors** identify the next element to consume and the next slot to fill.
- **Occupancy** is the number of published, unconsumed elements; **free space** is usable capacity minus occupancy.
- A **sentinel-slot encoding** leaves one physical slot unused so equal cursors mean empty and the next write cursor equaling the read cursor means full.
- A **counted encoding** stores a cursor and size, allowing all physical slots to be usable.
- **Reject**, **block**, and **overwrite-oldest** are distinct full-buffer policies.
- **Reservation** grants a producer slots; **publication/commit** makes initialized contents observable.
- A **contiguous span** is one non-wrapping region available to read or write; a logical range may need two spans.
- **SPSC**, **MPSC**, and **MPMC** mean single/multiple producer and single/multiple consumer. They are different proof topologies.
- **Sequence numbers** distinguish repeated physical-slot uses and can coordinate reservation and availability.

### Central model, mechanism, or theorem

Let physical capacity be `C>0`, head `h`, and occupancy `n`, with `0<=h<C` and `0<=n<=C`. Logical element `R[i]` resides at

\[
p(i)=(h+i)\bmod C,\qquad 0\le i<n.
\]

The next write slot is `p(n)`. Enqueue constructs there and increments `n`; dequeue reads/destroys at `h`, advances `h=(h+1) mod C`, and decrements `n`. This counted representation uses all C slots. A two-cursor sentinel representation instead has usable capacity `C-1`; changing the encoding changes the proof and public capacity.

### Critical invariants

1. Logical FIFO order maps injectively to exactly the published live slots.
2. Empty, full, occupancy, and advertised capacity agree under one stated encoding.
3. No modulo operation occurs for zero physical capacity, and cursor arithmetic obeys the language's integer rules.
4. A producer initializes a slot before publishing it; a consumer does not reuse it before consumption is published.
5. Rejecting a full insertion leaves state unchanged; overwriting reports exactly which data was lost.
6. Reservation and commit cannot strand capacity or expose partly initialized data.
7. A one/two-span API preserves logical order, bounds, alignment, and lease lifetime.
8. Every concurrency claim names producer/consumer counts, synchronization edges, linearization points, progress, and shutdown behavior.

### Common failures

- Treating equal read/write cursors as both full and empty without a count, flag, phase, or sentinel slot.
- Advertising C usable elements while silently reserving one of C slots.
- Applying a bit mask when capacity is not a power of two.
- Publishing a cursor before the payload is initialized, or reusing a slot before the reader finishes.
- Calling `volatile` a portable thread-synchronization mechanism.
- Sampling two moving cursors and presenting their difference as an exact concurrent size.
- Turning overflow into silent overwrite in a work queue or audit stream.
- Returning one contiguous region across a wrap, or committing more bytes than were reserved.
- Reusing an SPSC implementation with multiple producers or consumers.
- Assuming finite stress tests prove data-race freedom, progress, or fixed-width counter safety.

### Compact example

A capacity-four counted ring receives A,B,C,D. A fifth offer is rejected without mutation. Under a separately requested overwrite policy, E replaces oldest A and the head advances, leaving B,C,D,E. After consuming B,C and appending F,G, logical order is D,E,F,G while head is physical slot three and the live range wraps. The trace establishes those finite policy and mapping cases only.

### Connections

[DSE-017](017-queues.md) defines FIFO and backpressure; [DSE-018](018-deques.md) defines the broader two-ended abstraction; [DSE-012](012-dynamic-arrays-and-geometric-growth.md) contrasts growth. The [program roadmap](../ROADMAP.md) next studies ropes and piece tables, while concurrent algorithms remain grounded in the [Concurrent and Parallel Programming roadmap](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md).

## Governing Question

Which abstract capacity, state encoding, overload policy, cursor arithmetic, publication protocol, bulk interface, and evidence make a ring buffer correct for its actual workload and concurrency topology?

## Why This Matters

Network interfaces, audio paths, telemetry collectors, loggers, device drivers, parsers, and thread-to-thread channels often process a stream longer than available memory. A ring buffer bounds memory and reuses allocation. Its regular layout can reduce allocation traffic and improve locality, and monotonic positions can make batches convenient.

Those benefits do not make it “just an array with modulo.” A ring must encode full versus empty, define whether capacity counts slots or bytes, choose what overload does, manage object lifetimes, and handle wrap. Concurrent forms add ownership transfer and memory-model obligations. Device-visible rings add cache-coherence and ownership protocols. The same circular picture can therefore describe incompatible APIs and proofs.

Production correctness starts with semantics. A monitoring history may intentionally retain only the newest observations. A payment work queue must not silently erase the oldest job. A real-time audio producer may prefer overwrite, rejection, or a bounded fallback depending on whether continuity, freshness, or losslessness dominates. The mechanism must serve that policy and expose its consequences.

## Prerequisites and Retrieval

Before this module, retrieve:

- ADT/representation separation and invariant proofs from [DSE-001](001-abstract-data-types-and-concrete-representations.md) and [DSE-002](002-representation-invariants.md);
- preconditions, postconditions, failure, aliases, and ownership from [DSE-003](003-operation-contracts.md);
- cost, allocation, locality, and memory-layout models from [DSE-004](004-time-space-and-allocation-cost.md), [DSE-005](005-contiguous-and-linked-layouts.md), and [DSE-006](006-memory-locality-and-cache-behavior.md);
- generic element constraints and slot lifetime obligations from [DSE-007](007-genericity-and-type-constraints.md), together with the checked-cost reasoning above;
- iterator and evidence methods from [DSE-008](008-iterators-and-traversal-protocols.md), [DSE-009](009-property-based-testing-of-data-structures.md), and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md);
- fixed/dynamic arrays and FIFO/deque semantics from [DSE-011](011-fixed-arrays.md), [DSE-012](012-dynamic-arrays-and-geometric-growth.md), [DSE-017](017-queues.md), and [DSE-018](018-deques.md).

## Learning Objectives

After completing this module, you should be able to:

1. derive logical-to-physical mapping and FIFO transitions for a bounded ring;
2. compare sentinel, count, full-flag, phase-tag, and monotonic-counter encodings;
3. specify reject, block, partial, and overwrite overload policies without ambiguity;
4. prove object initialization, destruction, and wraparound arithmetic invariants;
5. design safe one-span/two-span reserve/commit and peek/release interfaces;
6. frame variable-size records across byte-ring boundaries and recovery cases;
7. state an SPSC release/acquire ownership-transfer proof without generalizing it;
8. explain why MPSC/MPMC reservation, ordered publication, progress, and reclamation need different algorithms;
9. test wrap, exact capacity, counter limits, partial failures, concurrency, and shutdown;
10. benchmark throughput, tail latency, drops, cache behavior, and batching under declared load.

## Core Exposition

**Start with the abstract stream, not the cursors.** A bounded FIFO ring represents a finite sequence `R=<r0,...,r(n-1)>`. Successful enqueue appends one element; successful dequeue removes and returns r0. The ring differs from a general deque because its ordinary streaming interface has one admission end and one consumption end, fixed storage, and a deliberate full policy. A growable `VecDeque` uses ring layout, but “ring buffer” does not imply growth, two-ended mutation, or a specific library API.

Capacity needs a unit. An element ring can hold at most K elements. A byte ring holds B bytes, while variable records additionally consume headers, padding, and perhaps wrap markers. A descriptor ring may bound outstanding ownership transfers even when payloads live elsewhere. State both physical slots and usable/application capacity.

**The counted mapping is simple but not free.** For physical capacity C>0, head h, and occupancy n, logical i maps to `(h+i)%C`. Because distinct logical indices in `[0,n)` differ by less than or equal to C-1, they cannot be congruent modulo C; the mapping is injective. Head is the next read position. Tail can be derived as `(h+n)%C`. Empty is n=0 and full is n=C.

The sequential transitions are direct. Enqueue when n<C constructs at tail, then increments n. Dequeue when n>0 reads/moves and ends the lifetime at h, advances h, then decrements n. A reference-holding runtime clears the removed slot so retention matches abstract ownership. A low-level generic implementation constructs and destroys exactly once.

If C=0, modulo is undefined. Reject construction, represent a disabled ring separately, or grow before mapping. If `h+n` can overflow its machine type before modulo, compute with a proved bounded form such as conditional subtraction. Power-of-two masking `x & (C-1)` is equivalent to modulo only when C is a nonzero power of two and integer semantics support the derivation.

**Full/empty encoding is a design choice.** A sentinel-slot representation maintains read r and write w. Empty is r=w; full is `next(w)=r`; C physical slots yield C-1 usable positions. It avoids a shared count and can fit SPSC role separation well. Its API must not promise C usable values.

A counted representation stores n. It uses all C slots but a concurrent count written by both sides may become a contention point or require atomic read-modify-write. A separate full bit disambiguates r=w but needs an owner/synchronization rule. Phase-tagged cursors pair an index with a wrap phase. Monotonic counters let physical positions be `counter%C` and occupancy be `write-read`, but only under a proved bounded-distance and counter-overflow model.

Fixed-width unsigned subtraction is modular. If the ring ensures the true cursor distance never exceeds usable capacity and that capacity is below the ambiguous half-range required by the chosen comparison, modular differences can remain meaningful. That is a theorem with type-width and lifetime assumptions, not permission to ignore rollover. Signed overflow is undefined in languages such as C++, and persisted counters may outlive assumptions.

**Overload is part of the abstraction.** Reject-on-full returns failure and leaves values, cursors, and loss counters unchanged. Blocking enqueue waits for space and requires wakeup, cancellation, timeout, fairness, and shutdown contracts outside the array mapping. A partial bulk operation returns the exact accepted count. An all-or-nothing bulk operation reserves the entire request or performs no insertion.

Overwrite-oldest accepts a new value by destroying or replacing the oldest and advancing both logical ends. This is appropriate for bounded histories and freshest-sample telemetry only when loss is intended. Boost's current circular buffer documents overwrite-on-full; that library choice is not a universal ring rule. Return the evicted value where feasible or increment a durable loss metric. Never make a lossless queue silently lossy because capacity planning failed.

Backpressure policy includes what producers do after rejection: retry with a bound, shed named work, spill to a durable store, degrade fidelity, or fail the request. Infinite retry can become unbounded latency. Overwrite can hide sustained overload if drops are not observed. Capacity merely delays overload when long-run arrival rate exceeds service rate.

**Wrap divides logical ranges into at most two spans.** With head h and n elements, the first readable span length is `min(n,C-h)` and the second is `n-first`. The writable free range has the analogous shape from tail. A bulk-copy implementation visits the suffix then prefix in logical order.

A zero-copy API makes lifetime explicit. `reserve(k)` may return one contiguous region no larger than k, or two regions totaling an allowed amount. The producer initializes only granted bytes/elements and calls `commit(m)` with `m` within the grant. Publication happens at commit, not reserve. A consumer `peek` obtains published spans and later `release(m)`; the producer cannot reuse those slots earlier.

Reservations introduce failure states. A producer that exits after reserving but before committing can strand capacity unless cancellation or ownership cleanup exists. Multiple producers can reserve out of order: later completed data cannot necessarily advance one global published cursor past an unfinished hole. Mature designs use per-slot availability, ordered commit, or a sequencer. LMAX Disruptor explicitly separates claiming a sequence from publishing it; its producer modes, gating sequences, consumer graph, and wait strategy are broader than a FIFO ring sketch.

**Variable-size records need framing.** A byte ring can prefix each record with a checked length and type. If a header or payload reaches the physical end, the design can split it, insert a padding/wrap record, or require a contiguous reservation and waste the suffix. Readers must validate lengths against maximum record and currently published bytes before advancing.

A corrupt length must not send the reader outside storage or permanently desynchronize it. Specify checksum or validation scope, alignment, endianness, committed bit/sequence, and restart recovery. If a crash can occur between payload write and header commit, persistent rings need a recoverable transaction protocol. An in-memory process-local ring does not automatically become crash consistent when mapped to a file.

Zephyr's official byte-ring claim/finish interfaces illustrate that a contiguous grant can be smaller than requested and that finish size must not exceed claimed size. The documentation also distinguishes data-item mode from byte mode. Use exact API contracts rather than projecting an element-queue model onto a byte stream.

**SPSC removes contenders, not memory ordering.** With exactly one producer and one consumer, each role can own one cursor. Under a sentinel layout, producer reads its write cursor, acquire-loads the consumer's read cursor to prove a free slot, initializes the slot, then release-stores the new write cursor. Consumer acquire-loads that cursor before reading the initialized slot, then release-stores its advanced read cursor after finishing so the producer can reuse the slot.

The release/acquire pairs carry two different ownership transfers: initialized data to the consumer and reclaimed storage to the producer. The exact operations follow the implementation language and platform memory model. The C++ working draft specifies that an acquire operation reading from a release sequence synchronizes with it; Linux kernel documentation provides its own barrier/`READ_ONCE`/`WRITE_ONCE` patterns. Do not translate primitives by name alone.

`volatile` can express device access or constrain compiler treatment under a particular language/platform, but it is not a portable replacement for atomic synchronization. Sequential consistency cannot repair two producers writing the same supposedly exclusive slot. First prove topology and slot ownership, then choose sufficient ordering.

The legacy archive's bounded Rust SPSC laboratory is useful evidence about proof shape: non-cloneable producer/consumer roles, initialization-state reasoning, acquire/release publication, and destruction after endpoint access ends. It is not copied here, and its proof does not establish MPSC/MPMC, blocking semantics, fairness, or another language's memory model.

**Multiple producers or consumers change the algorithm.** Two producers can observe the same free write slot unless reservation is atomic. A fetch-add can allocate unique sequences, but availability and bounded wrap still need checks; failed or delayed producers create publication gaps. Multiple consumers analogously need exclusive claims before moving a value.

MPMC bounded queues may attach a sequence number to every slot, use compare-and-swap loops, and define exact progress. DPDK's current ring library exposes separate single/multi-producer and single/multi-consumer modes plus different all-or-nothing bulk and best-effort burst operations. That is evidence that topology and bulk semantics belong in the API, not an instruction to reproduce its algorithm.

Lock-free means system-wide progress under a defined model, not that each call has a bounded latency. An operation can starve. Allocation, logging, fallback, or blocking waits can weaken the progress path. Per-slot sequence wrap, ABA-like reuse, destruction, cancellation, and thread failure need explicit analysis. Prefer a locked bounded queue when its semantics and auditability fit better.

**Hardware-visible rings add another ownership domain.** Device descriptor queues commonly alternate ownership between software and hardware. Ordinary CPU atomics may not flush caches, order memory-mapped I/O, or notify a device. The platform specifies DMA mapping, coherent/noncoherent memory, descriptor barriers, doorbells, completion observation, and teardown. Never transfer the SPSC CPU-thread proof directly to DMA.

**Observability is intentionally weaker or more expensive.** A concurrent `size()` that separately samples read and write cursors can combine states that never coexisted. It may be documented as approximate, computed under a lock/snapshot protocol, or omitted. Full/empty decisions used for correctness must occur inside the algorithm, not from a diagnostic metric.

Track accepted, rejected, overwritten, high-water, retry, wait, and stall counts as appropriate. Counters themselves can wrap or contend. Decide whether metrics are exact or approximate, and avoid making the hot path slower based only on intuition.

**Verification combines models, schedules, and measurements.** A sequential model is a list plus the declared full policy. Generate enqueue, dequeue, bulk, clear, reserve/commit, and peek/release actions. Compare values, occupancy, returned counts, losses, and live slots after each action. Force capacity zero/one, exact full, every head/tail adjacency, repeated wraps, counter values near limits, oversized records, corrupt headers, and interrupted reservations.

Concurrent validation identifies linearization points and checks histories against the specification. Exercise stalled producer after reservation, stalled consumer before release, wrap/reuse, full/empty races, shutdown, cancellation, and the declared thread counts. Use language race detectors, sanitizers, model checkers, and architecture diversity where applicable. None replaces proof review.

Benchmarks report toolchain, hardware, topology, capacity, element size, batch distribution, producer/consumer rates, affinity, warmup, duration, and trial variation. Measure throughput and latency distributions together with drops/retries, CPU, allocations, cache effects, and high-water. Compare against a simple locked bounded queue and channel under the real workload. A ring is successful when it meets the system contract, not when a synthetic loop produces the largest operations-per-second number.

The executable trace below checks a sequential counted ring with explicit reject and overwrite modes. `None` is reserved as an educational spare marker.

<!-- bijux-verify: {"id":"bounded-ring-policy-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"values=D,E,F,G\nhead_index=3\nsize=4\ncapacity=4\nrejected=True\ndropped=1\nwrapped=True\ninvariant=True\nevidence=finite_ring_policy_trace\n","stderr":""}} -->
```python
class RingBuffer:
    def __init__(self, capacity):
        if capacity < 0:
            raise ValueError("negative capacity")
        self.storage = [None] * capacity
        self.head = 0
        self.size = 0
        self.dropped = 0

    def offer(self, value, *, overwrite=False):
        if value is None or not self.storage:
            return False
        if self.size == len(self.storage):
            if not overwrite:
                return False
            self.storage[self.head] = value
            self.head = (self.head + 1) % len(self.storage)
            self.dropped += 1
            return True
        tail = (self.head + self.size) % len(self.storage)
        self.storage[tail] = value
        self.size += 1
        return True

    def poll(self):
        if self.size == 0:
            raise LookupError("empty ring")
        value = self.storage[self.head]
        self.storage[self.head] = None
        self.head = (self.head + 1) % len(self.storage)
        self.size -= 1
        return value

    def values(self):
        if not self.storage:
            return []
        return [self.storage[(self.head + i) % len(self.storage)]
                for i in range(self.size)]

    def invariant(self):
        if not 0 <= self.size <= len(self.storage):
            return False
        if self.storage and not 0 <= self.head < len(self.storage):
            return False
        if not self.storage:
            return self.head == 0 and self.size == 0
        live = {(self.head + i) % len(self.storage)
                for i in range(self.size)}
        return all((value is not None) == (index in live)
                   for index, value in enumerate(self.storage))


ring = RingBuffer(4)
for item in ("A", "B", "C", "D"):
    assert ring.offer(item)
rejected = not ring.offer("E")
assert ring.offer("E", overwrite=True)
assert ring.poll() == "B"
assert ring.poll() == "C"
assert ring.offer("F")
assert ring.offer("G")
print("values=" + ",".join(ring.values()))
print(f"head_index={ring.head}")
print(f"size={ring.size}")
print(f"capacity={len(ring.storage)}")
print(f"rejected={rejected}")
print(f"dropped={ring.dropped}")
print(f"wrapped={ring.head + ring.size > len(ring.storage)}")
print(f"invariant={ring.invariant()}")
print("evidence=finite_ring_policy_trace")
```

This execution does not establish concurrent safety, crash consistency, real-time bounds, or superiority over another queue.

## Definitions and Notation

- `C`: number of physical slots/bytes, required positive whenever modulo C is evaluated.
- `K`: advertised usable capacity; K=C for the counted model and K=C-1 for a one-sentinel model.
- `R=<r0,...,r(n-1)>`: logical FIFO sequence of published, unconsumed elements.
- `h` or `read`: physical/logical cursor for the next consumption.
- `t` or `write`: physical/logical cursor for the next admission/reservation.
- `n`: exact sequential occupancy, with `0<=n<=K`.
- `p(i)=(h+i) mod C`: physical location of logical element i in the counted model.
- `next(x)=(x+1) mod C`: successor physical index when C>0.
- **live slot**: storage containing an initialized, published, unconsumed value.
- **free slot**: storage owned by a producer and safe to initialize.
- **reserved slot**: granted to a producer but not necessarily published.
- **linearization point**: event at which an operation takes effect in the concurrent abstract history.
- **release/acquire publication**: language-defined synchronization that orders payload access through an atomic state transition.
- **false sharing**: cache-line coherence traffic caused by independently used data sharing a coherence granule.

## Mechanisms, Invariants, or Proof Structure

For a sequential counted ring, prove representation validity (`C>0`, normalized h, bounded n), then mapping injectivity, then transition preservation. Enqueue's precondition n<C identifies `p(n)` as non-live; construction followed by n increment adds exactly the new last element. Dequeue's precondition n>0 identifies h as live; moving/destroying it, advancing h, and decrementing n maps each old logical i+1 to new i.

For a sentinel ring, replace that proof with `r,w` and usable capacity C-1. Empty is r=w; full is next(w)=r. Count equals `(w-r) mod C` under normalized indices. Do not mix formulas from the counted representation.

For SPSC, add a slot-state cycle: free → producer-owned/reserved → initialized → release-published → consumer-owned → consumed → release-reclaimed → free. Unique roles exclude same-side contention. The acquire observing the opposite release establishes payload/reuse visibility. Shutdown and destruction occur only after endpoint access is excluded.

For multiple participants, unique sequence reservation, bounded-capacity admission, per-slot availability, ordered visibility, failure after reservation, counter wrap, and progress need a new proof. No finite test or atomic primitive erases those obligations.

## Alternatives and Trade-Offs

| Design | Benefit | Cost or proof obligation |
|---|---|---|
| Counted ring | all C slots usable; simple sequential model | shared count can contend; exact count synchronization |
| Sentinel slot | simple equal-cursor empty test; role-friendly | one slot unusable; advertised capacity differs |
| Full flag/phase tag | all slots usable | extra state and ownership/atomic consistency |
| Monotonic counters | natural sequence identity and batching | width, difference, wrap, and persistence proof |
| Reject on full | preserves accepted data | caller needs backpressure/failure policy |
| Overwrite oldest | freshest bounded history | deliberate loss, destruction, and metrics |
| Blocking bounded queue | clear waiting/backpressure semantics | locks/wakeups, cancellation, fairness, latency |
| One/two-span zero copy | avoids intermediate copy | lease, partial span, commit/release complexity |
| Per-slot sequence MPMC | parallel reservation/consumption | CAS contention, gaps, wrap, progress proof |
| Growable deque | adapts to bursts | allocation, relocation, unbounded-memory risk |

Use the least complicated design satisfying actual capacity, loss, latency, ownership, and topology requirements. Specialized lock-free code is not an automatic upgrade over a reviewed lock-based queue.

## Failure Modes and Misconceptions

- **“Head equals tail means empty and full.”** One state cannot encode both without additional information.
- **“The array length is the capacity.”** False for a sentinel-slot design unless the API distinguishes physical and usable capacity.
- **“Modulo fixes overflow.”** The addition can overflow before modulo, and signed-overflow rules matter.
- **“Masking is faster modulo.”** It is wrong for non-power-of-two capacity; measured compiler/hardware behavior decides performance.
- **“Overwrite is just successful enqueue.”** It destroys or evicts accepted data and must be an explicit policy with evidence.
- **“A reserve pointer is already readable.”** Only committed, properly published bytes are consumer-visible.
- **“One cursor publishes every completed producer.”** Out-of-order multi-producer completion can leave holes.
- **“SPSC atomics make MPMC safe.”** Extra participants violate exclusive cursor/slot ownership.
- **“Volatile provides thread safety.”** Portable concurrency requires the language/platform synchronization contract.
- **“Size is exact because both cursors are atomic.”** Separately sampled cursors may not describe one instant.
- **“Lock-free means every call finishes quickly.”** Lock-free permits individual starvation and says nothing about scheduler delay.
- **“CPU-thread rings prove DMA rings.”** Device visibility, coherency, barriers, and ownership use platform-specific rules.
- **“Stress passed, therefore proof complete.”** Rare schedules, rollover, lifetime, and progress claims require more evidence.

## Worked Examples

### Example 1

For C=5, h=3, n=4, logical A,B,C,D map to physical 3,4,0,1. The readable spans are slots 3..4 then 0..1. Conclusion: physical discontinuity does not change FIFO order.

### Example 2

A sentinel representation has C=4, r=1, w=0. `(w-r) mod 4=3`, and `next(w)=1=r`, so it is full with only three usable values. Conclusion: physical capacity four does not imply usable capacity four.

### Example 3

A counted ring with C=0 attempts `(h+n)%C` during insertion and fails before it can report full. Construction that rejects zero or an operation that branches before mapping is required. Conclusion: zero-capacity policy precedes arithmetic.

### Example 4

A lossless job ring containing A,B rejects C and remains A,B. A latest-sample history containing A,B accepts C, destroys/returns A, records one drop, and becomes B,C. Conclusion: identical layout can implement incompatible overload semantics.

### Example 5

At tail six in an eight-byte ring, a four-byte request has a first span of two and second span of two. A one-span API returns two; a two-span API may return both. Committing four after receiving only two from the first API is invalid. Conclusion: grants, not requests, bound commit.

### Example 6

A producer reserves record sequence 10 and stalls; another reserves 11 and completes. Advancing a single published cursor to 11 would let the consumer cross uninitialized 10. Conclusion: multi-producer reservation needs gap-aware publication or ordered commit.

### Example 7

In SPSC, the producer writes payload X then release-publishes write=next. The consumer's acquire load observes that write value before reading X. Reversing publication and initialization permits an uninitialized read. Conclusion: publication order transfers initialized ownership.

### Example 8

A 16-bit monotonic-counter ring of capacity 100 cannot simply use signed `write-read` forever. Its proof must use defined unsigned modular arithmetic, keep true distance bounded, and exclude ambiguous comparisons across rollover. Conclusion: counter width is part of the representation theorem.

### Example 9

A metrics thread loads read=90, then producer advances write from 100 to 120 while consumer advances read to 115, and metrics loads write=120. It reports 30 although no sampled instant necessarily had that occupancy. Conclusion: independent atomic samples can be approximate yet unsuitable for admission decisions.

### Example 10

A DMA producer descriptor is written in CPU cache and a doorbell is rung without the platform-required device barrier/flush. A correct in-process SPSC release store does not ensure the device sees the descriptor. Conclusion: hardware rings require the device's coherency and I/O contract.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns memory models, linearizability, progress, contention, SPSC/MPMC algorithms, and model checking.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns raw storage, initialization, integer rules, atomics, alignment, and object destruction.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects cache coherence, DMA, devices, memory ordering, and bounded hardware resources.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) connects packet descriptor rings, batching, backpressure, and overload.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) connects kernel buffers, memory barriers, scheduling, wakeups, and per-core queues.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) connects log buffers, group commit, framing, durability, and recovery.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) connects streaming windows, bounded ingestion, lag, loss, and observability.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns untrusted lengths, arithmetic corruption, stale data, denial of service, and safe teardown.

## References

1. Linux Kernel documentation, [Circular Buffers](https://docs.kernel.org/core-api/circular-buffers.html). Fixed finite head/tail model, power-of-two helpers, SPSC limitation, and kernel-specific producer/consumer memory-barrier patterns.
2. Zephyr Project, [Ring Buffers](https://docs.zephyrproject.org/latest/kernel/data_structures/ring_buffers.html). Current byte/data modes, claim/finish zero-copy operations, partial contiguous grants, concurrency restrictions, and synchronization note.
3. DPDK Project, [Ring Library](https://doc.dpdk.org/guides/prog_guide/ring_lib.html). Current fixed FIFO properties, single/multi producer/consumer modes, bulk-versus-burst semantics, and implementation discussion.
4. Boost C++ Libraries, [`circular_buffer`](https://www.boost.org/doc/libs/latest/doc/html/circular_buffer.html). Current fixed-capacity sequence API and explicit overwrite behavior when full.
5. Rust Project, [`std::collections::VecDeque`](https://doc.rust-lang.org/std/collections/struct.VecDeque.html). Current growable ring-buffer API, capacity, two-slice representation, reserve behavior, and contiguity operation.
6. ISO C++ working draft, [Order and Consistency](https://eel.is/c%2B%2Bdraft/atomics.order). Acquire/release meanings, synchronization relation, relaxed operations, and sequential consistency in the C++ memory model.
7. LMAX Exchange, [Disruptor User Guide](https://lmax-exchange.github.io/disruptor/user-guide/). Current sequencing architecture, single/multi-producer modes, claim/publish discipline, gating sequences, batching, and wait policies.
8. LMAX Exchange, [Disruptor Technical Paper](https://lmax-exchange.github.io/disruptor/disruptor.html). Primary design account for sequence claiming, publication, consumer progress, memory barriers, and batching.
9. FreeBSD Project, [`buf_ring(9)`](https://man.freebsd.org/cgi/man.cgi?query=buf_ring&sektion=9). Kernel bounded ring interface and documented enqueue/dequeue operating constraints.
10. Paul E. McKenney et al., Linux Kernel documentation, [Memory Barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html). Platform-specific ordering vocabulary, compiler/CPU barrier concerns, and circular-buffer connection.

## Exercises

### Exercise 1

Specify a sequential counted ring and a sentinel-slot ring. Derive empty, full, usable capacity, occupancy, and logical-to-physical mapping for each without mixing state variables.

### Exercise 2

Trace a capacity-five counted ring through enqueue A..E, two dequeues, enqueue F,G, one rejected H, and overwrite H. Show logical order, head, size, physical live slots, and loss after every operation.

### Exercise 3

Design a variable-record byte ring's reserve/commit and peek/release API, including wrap, alignment, partial grants, corrupt lengths, abandoned reservation, and restart behavior.

### Exercise 4

Write the obligation register for a bounded SPSC ring in a language with acquire/release atomics, then explain precisely which obligations fail if a second producer is added.

### Exercise 5

Choose a ring design for a network telemetry collector that must bound memory, prefer recent observations during overload, expose loss, batch disk writes, and shut down cleanly. Provide verification and benchmark plans.

## Answers to the Exercises

### Answer 1

Counted: require C>0, `0<=h<C`, `0<=n<=C`; empty n=0, full n=C, usable capacity C, and logical i maps to `(h+i)%C`; tail is `(h+n)%C`. Sentinel: require C>=2 for positive usable capacity, normalized read r/write w; empty r=w, full `next(w)=r`, usable capacity C-1, occupancy `(w-r)%C`, and logical i maps to `(r+i)%C` for i below occupancy. The counted model's n disambiguates equal derived head/tail; the sentinel deliberately prevents write from advancing into read. Each needs its own transition proof and zero-capacity handling.

### Answer 2

Start h=0,n=0. Enqueue A..E fills slots 0..4, order ABCDE, h=0,n=5. Dequeue A gives BCDE,h=1,n=4; dequeue B gives CDE,h=2,n=3, slots 2..4 live. Enqueue F uses `(2+3)%5=0`, yielding CDEF; G uses slot1, yielding CDEFG,h=2,n=5 with all slots live. Reject H leaves every field/value unchanged and loss zero. Overwrite H replaces/destroys oldest C at h=2, advances h to3, keeps n=5, increments loss, and yields DEFGH physically at slots 3,4,0,1,2. Verify returned/rejected evidence, not only final order.

### Answer 3

Represent byte capacity, committed read/write sequences, and reservation ownership separately. `reserve(max)` returns one or two aligned writable spans and a lease token; total granted bytes never exceeds free space. Producer writes a checked header/payload and commits at most the grant, with a valid committed marker or ordered cursor publication. Cancellation releases an unpublished reservation; process failure either discards an identifiable incomplete record on restart or requires a documented nonpersistent scope. `peek` exposes only complete committed records/spans; it validates header availability, maximum length, alignment/padding/wrap markers, checksum if used, and published-byte bound. `release` advances only within the lease. A corrupt record stops, skips via a proved resynchronization marker, or quarantines the ring—never trusts the length for unchecked arithmetic.

### Answer 4

Record exactly one non-shareable producer endpoint and consumer endpoint; storage lifetime outlives both; cursor types/widths and sentinel/count encoding are fixed; producer exclusively reserves/writes one free slot; initialization precedes release publication; consumer acquire-observes publication before reading; consumption precedes release reclamation; producer acquire-observes reclamation before reuse; live values are destroyed once; close/drop excludes new operations; progress excludes hidden blockers. With two producers, both can load the same write cursor, decide the same slot is free, race on payload, and publish conflicting advances. Atomic cursor loads/stores do not allocate unique reservations. Repair requires a different algorithm with atomic claims, bounded admission, gap-aware availability, producer failure handling, sequence wrap, progress, and possibly per-slot metadata.

### Answer 5

Use a fixed byte or element ring with explicit overwrite-oldest only if records are independently framed and “recent over complete” is approved. Return/record overwritten records or exact drop counts, maintain high-water and lag metrics, and batch committed spans to a disk writer. Separate reserve from publication, ensure the writer releases only after copying/owning data, and define close as stop admission, publish/cancel outstanding reservations, drain committed records, flush according to durability policy, then release resources. Model-test sequential overwrite identities and wrap; fuzz lengths and partial spans; explore producer/writer schedules, stalled leases, close races, counter limits, and metric wrap; use race/sanitizer tools. Benchmark realistic record sizes/bursts, capacities, batch thresholds, producer/writer imbalance, CPU/allocations, throughput, p50/p95/p99 latency, drops, lag, high-water, shutdown time, and disk-failure behavior against a locked bounded queue. The design cannot claim losslessness, crash durability, or wait freedom without additional mechanisms and evidence.
