---
module_id: CONPAR-095
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 95
title: Concurrent Memory Allocators
status: complete
last_verified: 2026-08-29
---

# Concurrent Memory Allocators

## One-Page Review

### Governing question

How can a concurrent program choose or design allocation paths that preserve object lifetime, alignment, unique allocation, safe reclamation, bounded memory, and failure semantics while reducing metadata contention, remote frees, fragmentation, false sharing, and NUMA traffic?

### Essential definitions

- An **allocator** maps size/alignment requests to disjoint live storage and reclaims storage after lifetime ends.
- A **size class** rounds requests into managed slot sizes; the difference contributes internal fragmentation.
- An **arena/heap** is an allocator shard containing metadata and spans/pages; multiple arenas reduce central contention but may increase footprint.
- A **front-end cache** supplies fast allocations from a thread/CPU-local cache; a middle/back end refills caches and obtains/releases pages.
- A **remote free** occurs when a worker different from the allocation/home owner deallocates an object.
- A **superblock/slab/span/page** is a larger region subdivided into slots, with allocator-specific meanings.
- **internal fragmentation** wastes bytes inside allocated size-class slots; **external fragmentation** leaves free space unusable for requested layouts.
- **blowup** is allocator/system memory growth disproportionate to live application memory, often through too many caches/arenas or ownership imbalance.
- **false sharing** occurs when independently used objects/metadata share cache lines whose ownership bounces.
- **reuse distance/quarantine** controls when freed addresses can be reallocated; immediate reuse raises temporal-safety/ABA pressure.
- **ABA** is a value/address changing A→B→A so a stale observer mistakes the reused identity for the original.
- **OOM policy** defines failure/exception/abort/retry behavior for allocation exhaustion; overcommit makes allocation success different from later physical-memory success.
- **usable size** can exceed requested size; applications must not assume allocator-specific excess storage portably.

### Central model, mechanism, or theorem

Allocator correctness requires: every successful live allocation is suitably aligned and disjoint; exactly one valid deallocation matches its allocation family after the last access; metadata transitions are linearizable or otherwise satisfy the declared concurrency contract; reclaimed storage is not reused while any reader can access the old object; and failure leaves state valid. Performance decomposes into fast-path hits, refill/central/OS paths, remote-free processing, synchronization, page faults, fragmentation, and locality. Sharding/caching lowers contention but trades memory, migration, and reclamation latency.

### Critical invariants

Requested size/alignment and allocation/deallocation family match; zero/overflow/huge requests follow defined policy; live regions never overlap; metadata cannot be corrupted by concurrent allocate/free; object construction/destruction and publication/reclamation have language-level happens-before; double/invalid/cross-heap free is rejected or never occurs; remote-free queues cannot lose/duplicate objects and are bounded/drained; addresses are not reused before hazard/epoch/reference lifetime ends; per-cache/arena memory has global limits; NUMA placement follows consumers; fork/signal/cancellation behavior is documented; OOM is checked; statistics distinguish reserved/committed/resident/live/cached; and shutdown drains owners before allocator destruction.

### Common failures

Teams benchmark only allocator calls, free while readers remain, mix `new/delete`, `malloc/free`, aligned or library heaps, ignore multiplication overflow, use pointer identity as permanent generation, push the same block twice to a freelist, claim lock-free because the common path is local, let per-thread caches scale without bound, strand memory in dead-thread arenas, confuse RSS with live bytes, return memory to the OS and assume latency-free reuse, let remote frees create NUMA bouncing, align objects yet pack them into the same cache line, replace the allocator without ABI/library audit, allocate in signal handlers, fork from multithreaded state unsafely, or treat a microbenchmark win as application benefit.

### Compact example

Requests `[17,33,64,65]` rounded to size classes `[32,64,64,128]` reserve 288 bytes for 179 requested, so internal waste is 109 bytes and utilization `179/288≈.621528`. This exact arithmetic does not measure metadata, external fragmentation, page rounding, caches, alignment, residency, or allocator performance.

### Connections

[Hazard Pointers](055-hazard-pointers.md) defines one safe-reclamation mechanism. [Epoch-Based Reclamation](056-epoch-based-reclamation.md) defines another. [False Sharing and Cache-Line Contention](029-false-sharing-and-cache-line-contention.md) explains allocator-induced coherence. [NUMA-Aware Allocation and Scheduling](093-numa-aware-allocation-and-scheduling.md) governs page placement. The [program roadmap](../ROADMAP.md) next uses sanitizers to detect lifetime and race defects.

## Governing Question

Which allocation/lifetime/ownership patterns dominate the application, what allocator mechanisms serve them safely, and do reduced contention/tail latency outweigh fragmentation, cache footprint, NUMA, security, and operational costs under representative workloads?

An allocator is a concurrent state machine and a resource governor, not merely a faster `malloc` symbol.

## Why This Matters

Dynamic allocation lies on hot paths in servers, task runtimes, graphs, parsers, and message pipelines. A central lock serializes. Modern allocators shard by arenas, threads, CPUs, size classes, or pages and cache freed objects locally. These techniques often transform throughput, but they retain memory, complicate remote frees, move objects away from consumers, and conceal long-tail refill/page-fault costs.

Allocator bugs are severe: double-free, use-after-free, metadata races, size overflow, misalignment, mismatched APIs, and ABA can corrupt unrelated state or become security vulnerabilities. Correct allocator internals cannot repair an application's premature free.

Selection therefore combines lifetime proof, memory accounting, workload distributions, NUMA/security/failure constraints, and application-level measurement. Specialized pools can be ideal for bounded homogeneous objects; general allocators remain necessary for diverse lifetimes and libraries.

## Prerequisites and Retrieval

Retrieve:

- ownership, lifetime, publication, and reclamation from [Designing a Correct Multithreaded Component](020-designing-a-correct-multithreaded-component.md), [Hazard Pointers](055-hazard-pointers.md), and [Epoch-Based Reclamation](056-epoch-based-reclamation.md);
- atomics, ABA, progress, false sharing, and contention from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md), [ABA Problems and Tagged References](054-aba-problems-and-tagged-references.md), [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md), and [False Sharing and Cache-Line Contention](029-false-sharing-and-cache-line-contention.md); and
- page/NUMA/hybrid resource mapping from [NUMA-Aware Allocation and Scheduling](093-numa-aware-allocation-and-scheduling.md) and [Hybrid Threads, SIMD, GPU, and Message Passing](094-hybrid-threads-simd-gpu-and-message-passing.md).

Retrieval prompt: inventory allocation APIs/ABIs and owners; size/alignment/lifetime distributions; allocating/freeing thread/CPU/node; remote-free rate; live/reserved/committed/resident/cached bytes; arenas/caches/classes/pages; object publication/reclamation; thread churn; OOM/overcommit; fork/signal/cancellation; device/pinned/huge memory; security hardening; allocator/toolchain versions/config; latency percentiles; application validity; and rollback.

## Learning Objectives

After completing this module, a learner can:

1. state allocator safety, lifetime, alignment, and failure invariants;
2. distinguish arenas, local caches, size classes, spans, central lists, and OS back ends;
3. reason about remote frees, ABA/address reuse, and reclamation;
4. quantify internal fragmentation and interpret external fragmentation/memory accounting;
5. diagnose metadata contention, cache misses, false sharing, page faults, and NUMA locality;
6. bound per-thread/per-CPU caches and handle thread exit;
7. choose general allocators, arenas, pools, monotonic regions, or object reuse;
8. design representative concurrency/churn/OOM/fork/failure tests;
9. compare allocators through full application time, tails, memory, and correctness; and
10. scope security, operations, and high-stakes review.

## Core Exposition

### Safety before speed

A successful allocation returns storage meeting requested API alignment and size, distinct from all other live allocations. The caller establishes object lifetime according to its language. Exactly one matching deallocation occurs after the last access and destructor. Allocation failure follows the API: null, exception, handler, or abort configuration.

Check `count*size` overflow before allocation unless a checked API guarantees it. Zero-size semantics vary; never dereference without a positive-size contract. Over-aligned objects require matching supported APIs. Reallocation may move and invalidates the old pointer on success according to its contract.

Thread-safe allocator functions do not make objects thread-safe. Publication and reclamation require happens-before/hazard/epoch/reference protocols. A stale pointer after free is invalid even if the allocator has not reused the bytes.

### Architecture of scalable allocators

Small requests map to size classes. A local front end pops/pushes slots without a global lock in its fast path. Empty/full caches batch-transfer to a central structure; spans/pages come from a back end/OS. Large objects often bypass small caches.

Arenas shard locks and metadata. Thread caches remove most synchronization. Per-CPU caches bound footprint by CPUs rather than transient threads but depend on platform mechanisms and migration semantics. Sharded free lists reduce contention/localize metadata. Each allocator has specific rules; avoid universal descriptions.

Fast-path progress is not whole-operation progress. Refill, page mapping, cache scavenging, stats, purge, and remote frees may lock or block. State progress per path and configuration.

### Executable fragmentation arithmetic

This deterministic size-class model calculates only rounding waste. It does not implement allocation or measure metadata, external fragmentation, pages, caches, residency, safety, or performance.

<!-- bijux-verify: {"id":"allocator-size-class-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requests=[17, 33, 64, 65]\nclasses=[32, 64, 64, 128]\nrequested_bytes=179\nreserved_slot_bytes=288\ninternal_waste_bytes=109\nslot_utilization=0.621528\n","stderr":""}} -->
```python
requests = [17, 33, 64, 65]
size_classes = [16, 32, 64, 128]


def class_for(size):
    for candidate in size_classes:
        if size <= candidate:
            return candidate
    raise ValueError("request exceeds modeled classes")


classes = [class_for(size) for size in requests]
requested = sum(requests)
reserved = sum(classes)
print(f"requests={requests}")
print(f"classes={classes}")
print(f"requested_bytes={requested}")
print(f"reserved_slot_bytes={reserved}")
print(f"internal_waste_bytes={reserved - requested}")
print(f"slot_utilization={requested / reserved:.6f}")
```

### Allocation and free paths

Document each path: local cache hit; local miss/refill; central transfer; new span/page; large allocation; local free; remote free; cache overflow; purge/release. For each, identify synchronization, metadata writes, page faults, syscalls, and worst/tail behavior.

Batching amortizes central locks but retains memory and creates bursts. Adaptive cache sizing trades miss rate against footprint. Thread churn can strand caches; thread-exit cleanup and abandoned arenas matter. Per-CPU designs must handle thread migration/preemption through supported mechanisms.

Remote frees need a safe path to the owning page/heap: atomic remote list, mailbox, central handoff, or ownership-independent metadata. The freeing thread cannot mutate owner-only structures unsafely. Queue draining must prevent loss, duplication, unbounded backlog, and teardown races.

### Reuse, ABA, and reclamation

Allocator reuse makes address equality temporal. A lock-free stack may read pointer A, another thread removes/frees/reallocates the address, and A reappears with a different object. Tagged/versioned pointers reduce some ABA but wrap/alignment/atomic-width assumptions must hold. Hazard pointers, epochs, QSBR, reference counting, or type-specific ownership delay reuse.

Allocator quarantine can aid detection/security but is not a proof that no stale reader remains; bounded quarantine eventually reuses. Memory tagging or sanitizers can detect classes of bugs, not replace lifetime proof. Generation IDs belong in logical references where identity persists.

The allocator must not interpret application reclamation. An application returning a pointer promises no valid future use under its API.

### Fragmentation and memory accounting

Internal fragmentation includes size-class rounding/alignment. External fragmentation depends on span occupancy, lifetime mix, page release constraints, and address-space layout. Arena/cache fragmentation can strand free objects away from demand. Huge pages improve TLB/back-end behavior but magnify retention and NUMA granularity.

Distinguish requested/live payload, allocator active/allocated, metadata, cached free, retained/reserved virtual, committed, and resident physical bytes. RSS includes/shared/excludes platform-specific pages and can lag. Memory returned through advice may remain virtually reserved.

Track peak and steady distributions by size/lifetime/arena/node. A throughput win that doubles peak memory may cause OOM or reduce cluster density.

### Contention and false sharing

Profile allocator call rate/time/percentiles, fast/slow path, locks/atomics, cache refill/flush, remote frees, page faults/syscalls, and CPU/cache/coherence. Sampling/profiling support varies and adds overhead.

Allocator metadata can bounce, as can adjacent objects allocated to different threads in one cache line. Per-thread arenas alone do not prevent application false sharing. Align/pad only objects whose independent writes justify memory cost; object placement and size classes may defeat assumptions.

Central-lock time can appear inside unrelated callers. Per-thread throughput averages hide one remote-free owner or purge tail. Preserve critical-path and percentiles.

### NUMA and ownership transfer

Pages often follow the thread/CPU that first populates allocator spans, not necessarily future object consumers. Per-arena/thread/CPU caches improve locality for allocate/use/free-on-same-owner patterns. Producer-allocates/consumer-frees pipelines create remote data and remote frees.

Options: consumer allocates; transfer tasks with data; node-local pools; explicit arenas; remote-free mailboxes; replication; or accept remote access. Measure page placement/controllers/interconnect and queue balance. Too many node-local pools strand capacity.

Migration or purge/repopulate costs require a stable horizon. On thread exit or repartition, reclaim/move abandoned cache capacity safely. Coordinate with NUMA policy and cpusets.

### Specialized allocation

Monotonic/region allocation makes many allocations cheap and reclaims them together; it is valid only when lifetimes share a region boundary. Fixed-size pools offer bounded latency/fragmentation but need capacity/backpressure and safe cross-thread free. Object reuse avoids allocation but requires reset, generation, privacy/secret scrubbing, and capacity discipline.

Stack/value/storage-inline techniques remove heap traffic but can grow stack/copies and change ABI. Batch allocation and intrusive containers reduce metadata. Language garbage collectors/runtimes have different barriers/moving/safepoint semantics; do not replace their allocator blindly.

Libraries may allocate/free across module boundaries. An allocator replacement must cover ABI, dynamic/static linking, plugins, aligned/sized deallocation, sanitizer/profiler interposition, exceptions, and platform rules. One family must free what its matching family allocated.

### OOM, fork, signals, and shutdown

Overcommit can make virtual allocation succeed and physical use fail later. Preflight cannot prove future availability. Define quotas/high-water, bounded pools, backpressure, shedding, checkpoint/abort, and whether allocation failure is recoverable. Avoid retry storms and emergency allocation in OOM handlers.

After fork in a multithreaded process, allocator locks/state may reflect vanished threads; only async-signal-safe operations are permitted before exec under relevant platform rules. Do not allocate in signal handlers unless explicitly guaranteed. Prefer fork-before-threads or fork+exec patterns per platform.

At shutdown stop producers, join/drain consumers and remote frees, destroy objects, flush/destroy pools after users, then runtime. Detached threads must not touch torn-down allocator state. Device/pinned allocations follow their own APIs/completion.

### Security and hardening

Heap corruption is a security boundary. Use overflow checks, authenticated/encoded freelists or hardening offered by the allocator, guard/quarantine/tagging where appropriate, randomized layout, zeroization for secrets, and least diagnostic exposure. Hardening costs memory/time and must be configuration-controlled.

Do not log raw addresses or secret payloads. Allocation profiles expose type/traffic/user activity; control access/retention. Validate untrusted sizes/alignments and cap per-request/tenant/object counts.

Custom allocators expand trusted code. Prefer mature maintained implementations unless domain bounds justify a small verifiable pool. Fuzz and run sanitizers, but keep production defenses.

### Evaluation

Start with application traces/distributions, then build replay/microbenchmarks that cover size/alignment/lifetime, producer/free pairs, threads/CPUs/NUMA, bursts/quiescence, thread churn, remote frees, working set, OOM, and fork/shutdown if applicable. Synthetic results do not replace application runs.

Compare same revision/input/output/resources/affinity and allocator versions/config. Measure time-to-valid-solution, throughput and latency tails, allocator CPU/locks/paths, live/peak/reserved/committed/resident/cached memory, fragmentation, page faults/syscalls, NUMA/coherence, startup/purge/shutdown, energy, invalid outputs/crashes.

Test debug/hardened and production configurations separately. Randomize/repeat, account for page-cache/warm state, and evaluate long steady runs. Select the simplest allocator/pool whose correctness, footprint, tails, portability, and operations satisfy the envelope; retain rollback.

### High-stakes limits

In clinical, infrastructure, financial, or safety systems, allocator substitution can change timing, failure mode, address reuse, and determinism. Require concurrency/lifetime, platform, security, operations, domain, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers. Allocation throughput never establishes system safety.

## Definitions and Notation

- `s`: requested size; `a`: alignment; `c(s,a)`: selected size class/slot.
- `L`: live requested payload bytes.
- `A`: allocator active/slot bytes; `R`: reserved virtual; `C`: committed; RSS: resident measure with platform semantics.
- internal utilization `U=L/A` for a precisely sampled set, `0<=U<=1`.
- `H`: local fast-path hit rate; `F`: refill/slow-path rate.
- `Q_remote`: remote frees outstanding; `Q_max`: bound.
- `g`: logical allocation/object generation.
- **home**: allocator page/arena/cache responsible for a slot, not necessarily current CPU.
- Obs: API/config, workload, paths, memory accounting, locality, correctness, and limitations.

## Mechanisms, Invariants, or Proof Structure

### Allocation-safety proof

Validate size arithmetic/alignment/family; successful live ranges are disjoint; metadata transitions publish one slot once; failures preserve allocator state; zero/large requests follow contract.

### Lifetime/reclamation proof

Object publication/destruction has happens-before; no reader can access after deallocation; hazard/epoch/reference protocol delays reuse; logical generation defeats stale identity; every allocation frees exactly once through matching owner/family.

### Cache/remote-free proof

Local caches have bounded capacity and refill/flush invariants. Remote-free enqueue/dequeue is race-safe, lossless, duplicate-free, bounded, eventually drained, and cannot outlive home heap.

### Memory/locality proof

Requested/active/reserved/committed/resident/cached metrics are defined; per-arena/node capacity holds; page/object placement matches access or documented tradeoff; fragmentation/release and thread-exit behavior are measured.

### Empirical benefit proof

Representative concurrency/churn/lifetimes/OOM/shutdown pass correctness/sanitizer/fault tests. Application full valid time/tails improve without unacceptable peak memory, NUMA, security, portability, or operational regression.

## Alternatives and Trade-Offs

| Design | Main benefit | Principal limitation |
|---|---|---|
| central heap | simple/global reuse | contention |
| multiple arenas | shard locks | blowup/stranding |
| per-thread cache | very fast common path | thread-count footprint/churn |
| per-CPU cache | bounded by CPUs/local | platform/migration complexity |
| sharded page free lists | locality/less contention | metadata/design complexity |
| remote-free mailbox | preserves owner locality | backlog/drain latency |
| fixed-size pool | bounded/simple slots | capacity/type rigidity |
| monotonic region | cheap bulk lifetime | no individual reclamation |
| object reuse | avoids allocation | reset/retention/stale-state risk |
| hardened allocator | detects/resists corruption | time/memory overhead |

## Failure Modes and Misconceptions

- **“Thread-safe allocator makes lifetime safe.”** application reclamation remains.
- **“Address equality means object identity.”** reuse/ABA breaks it.
- **“Local fast path means lock-free allocator.”** slow/back-end paths differ.
- **“More arenas always scale.”** memory blowup and remote reuse can dominate.
- **“Thread caches are free.”** footprint grows with threads/classes.
- **“free returns memory to OS.”** cache/retention/purge semantics vary.
- **“RSS equals live heap.”** accounting layers differ.
- **“Internal fragmentation is all fragmentation.”** spans/arenas/pages strand space.
- **“Remote free is just another free.”** owner metadata/locality/draining matter.
- **“Alignment prevents false sharing.”** adjacent allocations can still share lines.
- **“Quarantine proves no UAF.”** it delays reuse only.
- **“Allocation success proves physical memory.”** overcommit/touch can fail later.
- **“OOM retry will eventually work.”** retry storms worsen pressure.
- **“Any heap can free any pointer.”** families/ABIs must match.
- **“Microbenchmark winner is best.”** workload/lifetimes/memory/tails decide.
- **“Custom pool is automatically safer.”** it expands trusted concurrent code.
- **“Fork/signal can call ordinary allocation.”** platform safety restrictions apply.
- **“Faster allocation proves deployment safety.”** domain review remains.

## Worked Examples

### Example 1

**Size rounding.** A 33-byte request maps to 64 bytes in the modeled classes. **Conclusion:** class design trades lookup/reuse against waste.

### Example 2

**Premature free.** Producer returns a node while a lock-free reader lacks a hazard. Allocator correctness cannot prevent UAF. **Conclusion:** reclamation precedes reuse.

### Example 3

**ABA reuse.** A stack node address is freed/reallocated before CAS. Tagged identity or safe reclamation is required. **Conclusion:** pointers are temporal.

### Example 4

**Remote-free pipeline.** Producer allocates, consumer frees; owner mailbox drains batches with bound/backpressure. **Conclusion:** model transfer explicitly.

### Example 5

**Thread churn.** Thousands of short threads retain minimum caches. Per-CPU cache/pool or thread reuse reduces footprint. **Conclusion:** worker lifecycle matters.

### Example 6

**Arena stranding.** One arena has free objects while another requests pages. More shards lower locks but raise RSS. **Conclusion:** measure global reuse.

### Example 7

**False-shared objects.** Two 24-byte mutable objects share a line across workers. Padding/class change helps at memory cost. **Conclusion:** allocator placement affects coherence.

### Example 8

**Overcommit fault.** Large allocation succeeds; first touch fails under pressure. Quota/preallocation/backpressure handles it. **Conclusion:** success and residency differ.

### Example 9

**Region win.** Per-request objects share a lifetime and bulk free; a bounded arena removes hot allocation and simplifies ownership. **Conclusion:** exploit domain lifetime.

### Example 10

**Railway control service.** Allocator changes must preserve message/train/track/sensor/time/configuration generations, bounded latency/memory, no lost/duplicated commands, deterministic failure/shedding, checkpoint/restart, hardening/audit, and safe-state gates. Named railway signaling/control, real-time/concurrency, allocator/platform, safety/security, operations, quality/certification/regulatory, human-factors, ethics, accessibility, and independent validation reviewers must approve evidence; none is claimed here. **Conclusion:** allocator throughput does not certify control safety.

## Cross-Program Connections

- **Languages:** lifetime, ownership, alignment, exceptions, destructors, and memory models define allocator contracts.
- **Algorithms:** freelists, size classes, sharding, batching, reclamation, and ABA drive design.
- **Architecture:** caches, coherence, pages, TLBs, NUMA, and atomics shape paths.
- **Operating systems:** virtual memory, overcommit, mapping, advice, fork, signals, and OOM govern back ends.
- **Runtimes:** tasks, thread churn, pools, garbage collection, and device memory compose allocation.
- **Security:** UAF/double-free/overflow/metadata corruption require hardening and testing.
- **Performance:** paths, percentiles, fragmentation/accounting and application replay provide evidence.
- **Operations:** quotas, pressure, shedding, profiles, shutdown, rollback, and versioning sustain services.
- **Testing/formal methods:** sanitizers, fuzzing, linearizability and fault injection complement proof.
- **Safety:** allocation remains subordinate to valid safe behavior.

## References

1. ISO/IEC, *C17 Standard, Dynamic Memory Management*, ISO/IEC 9899:2018. <https://www.iso.org/standard/74528.html>
2. The Open Group, *POSIX malloc()* specification, Issue 8, 2024. <https://pubs.opengroup.org/onlinepubs/9799919799/functions/malloc.html>
3. jemalloc Project, *jemalloc(3)*, current documentation; retrieved 2026-08-29. <https://jemalloc.net/jemalloc.3.html>
4. Google, *TCMalloc Design*, current documentation; retrieved 2026-08-29. <https://github.com/google/tcmalloc/blob/master/docs/design.md>
5. Google, *TCMalloc Tuning*, current documentation; retrieved 2026-08-29. <https://github.com/google/tcmalloc/blob/master/docs/tuning.md>
6. Daan Leijen, Benjamin Zorn, and Leonardo de Moura, “mimalloc: Free List Sharding in Action,” Microsoft Research, 2019. <https://www.microsoft.com/en-us/research/wp-content/uploads/2019/06/mimalloc-tr-v1.pdf>
7. Microsoft, *mimalloc Source and Design Documentation*, current repository; retrieved 2026-08-29. <https://github.com/microsoft/mimalloc>
8. Emery D. Berger et al., “Hoard: A Scalable Memory Allocator for Multithreaded Applications,” ASPLOS, 2000. <https://www.cs.umass.edu/~emery/pubs/berger-asplos2000.pdf>
9. Linux man-pages Project, *mmap(2)*, release 6.18. <https://man7.org/linux/man-pages/man2/mmap.2.html>
10. Linux man-pages Project, *fork(2)*, release 6.18. <https://man7.org/linux/man-pages/man2/fork.2.html>

## Exercises

### Exercise 1

For requests `[1,16,17,31,32,33,63,64]` and classes `[16,32,64]`, compute each class, requested/slot totals, waste, and utilization.

### Exercise 2

Specify a safe bounded remote-free mailbox protocol including enqueue, owner drain, duplicate defense, shutdown, thread exit, ABA/reclamation, and OOM.

### Exercise 3

Design a memory-accounting dashboard distinguishing live/requested, active slots, metadata, cached, retained/reserved, committed, resident, page faults, fragmentation and NUMA.

### Exercise 4

Design an allocator comparison for a producer-consumer server with thread churn and tail SLOs. Include workload, correctness/fault tests, metrics, configurations, and acceptance.

### Exercise 5

Transfer allocator reasoning to a concurrent medication-infusion controller. Specify lifetime/resource, real-time/failure, security, validation, publication, and named human reviewer invariants without claiming review.

## Answers to the Exercises

### Answer 1

Classes are `[16,16,32,32,32,64,64,64]`. Requested total is 257; slot total 320; waste 63; utilization `257/320=.803125`. This omits alignment beyond classes, metadata, page/span/external fragmentation, caches, residency and failed requests.

### Answer 2

Each object has immutable home heap/page and generation; only a live owner's final deallocator may enqueue `(address,generation)` once after reclamation protocol proves no readers. A bounded MPSC mailbox publishes entries with release/acquire or stronger required semantics; full queues apply backpressure or a safe central slow path, never drop. Owner validates home/generation/allocation state, atomically marks freed, batches into its local list, and detects duplicates in debug/hardened metadata. Address reuse waits for hazard/epoch/reference completion and queue drain; generation never substitutes for reclamation. On owner/thread exit, transfer home ownership under a stopped generation and drain before destroying metadata. Shutdown stops producers, joins readers/freers, drains mailboxes, verifies counts, then destroys. OOM/refill follows explicit null/exception/abort/shedding without corrupting queues.

### Answer 3

At consistent sample times expose requested live payload by size/lifetime; allocator active slot/span bytes and internal utilization; metadata; per-thread/CPU cache free bytes; central free/dirty/muzzy/retained categories using allocator definitions; reserved virtual, committed, resident/RSS/PSS with platform caveats; mapped/huge pages; allocation/free/remote/refill/purge rates; minor/major faults and syscalls; arena/cache/thread count; per-node residency/local/remote traffic; peak/steady/tails. Reconcile where definitions permit but never force equality. Tag allocator/version/config, workload phase, sampling overhead and unavailable counters; alert on sustained capacity, cache blowup, remote backlog or fragmentation, not one sample.

### Answer 4

Replay representative request arrival, sizes/alignments/lifetimes, producer/free pairs, object graphs, bursts/quiescence, working sets and thousands of short-lived versus pooled threads. Keep code/input/output/resources/affinity fixed across system allocator and selected versioned/configured alternatives. Run race/address/undefined/leak sanitizers where compatible, lifetime assertions, double/invalid-free negative tests, queue/OOM/overcommit pressure, thread exit, cancellation, fork+exec/shutdown and fault injection. Measure valid throughput/latency tails, allocator path/lock/refill/remote-free/purge CPU, requested/active/reserved/committed/resident/peak memory, fragmentation, faults/syscalls, NUMA/coherence, startup/shutdown and energy over long repetitions. Accept only if SLO and full application benefit improve with no correctness, peak-memory, security, portability, or operations regression; retain rollback.

### Answer 5

Give each command/sensor/pump/configuration object a generation, one owner and bounded lifetime; allocate from capacity-preflighted fixed pools outside real-time critical sections where possible. Publication/reclamation is race-free; no reuse until all readers/actuators acknowledge; remote frees are bounded/drained; align/isolate hot state; all size arithmetic and API families match. Define pool exhaustion, deadline miss, thread/device failure, cancellation and restart as fail-closed transition to a clinically approved safe state; no unbounded allocation/retry or logging in critical paths. Harden metadata, authenticate inputs, least privilege, zero secrets, minimize/redact profiles and audit every configuration. Validate model checking/stress/sanitizers off-target, worst-case pool/latency evidence on target, fault/OOM/power/restart, duplicate/stale commands, independent pump simulation, dose/unit/rate bounds and workflow. Named infusion nursing/clinical pharmacology, biomedical/control/real-time, concurrency/allocator/platform, safety/security/privacy, operations, quality/regulatory/certification, ethics, accessibility/human-factors, and independent validation reviewers are required. No external review, clinical safety, hard real-time proof, approval, or deployment authorization is claimed.
