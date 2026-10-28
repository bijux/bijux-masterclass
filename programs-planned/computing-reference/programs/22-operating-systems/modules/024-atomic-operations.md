---
module_id: OS-024
program: Operating Systems
level: 1
module_number: 24
title: Atomic Operations
status: complete
last_verified: 2026-09-04
---

# Atomic Operations

## One-Page Review

### Governing question

When does an indivisible memory operation suffice for kernel synchronization, and what additional ordering, invariant, progress, and lifetime arguments are required to make an atomic algorithm correct?

### Essential definitions

- An **atomic operation** appears indivisible with respect to relevant competing accesses under its specified memory model.
- A **read-modify-write (RMW)** atomically reads a value, computes a result, and conditionally or unconditionally writes it.
- **compare-and-exchange (CAS)** writes a desired value only if the object equals an expected value and reports the observed outcome.
- **load-linked/store-conditional (LL/SC)** conditionally stores when no disqualifying event invalidated the reservation.
- **relaxed ordering** provides atomicity without inter-thread ordering beyond the atomic object's modification rules.
- **acquire** prevents later accesses from moving before a successful observation; **release** publishes earlier accesses before its store or RMW.
- **sequential consistency** places participating operations in one total order consistent with program order under the language or kernel model.
- The **ABA problem** occurs when a value changes from A to B and back to A, causing equality-based validation to miss intervening change.

### Central model, mechanism, or theorem

Atomicity answers whether one operation tears or interleaves. Ordering answers what other memory becomes visible. Invariants answer whether one word represents all required state. Progress answers whether retries finish. Lifetime answers whether referenced storage remains valid.

A publication pattern initializes payload `D`, performs a release store of flag or pointer `P`, then a reader performs an acquire load of `P` before consuming `D`. The release/acquire pair can establish the required happens-before relationship when the reader observes the published value. A relaxed flag cannot carry that payload visibility merely because it is atomic.

### Critical invariants

- Every access to an atomic object uses compatible atomic operations or a specifically documented exception.
- The atomic width, alignment, type, signedness, and overflow semantics match the API and architecture contract.
- Each RMW transition preserves the entire state invariant encoded in that atomic object.
- Memory order is no stronger or weaker than the publication, ownership, and synchronization proof requires.
- CAS and LL/SC retry loops handle failure, interference, spurious failure, backoff, and termination policy.
- Version, tag, hazard, reference, epoch, or grace-period protocols prevent ABA and stale-object reclamation where applicable.
- Device memory, persistent memory, and ordinary coherent RAM are not synchronized through interchangeable assumptions.

### Common failures

Common mistakes are treating atomic as sequentially consistent, using relaxed publication, mixing atomic and ordinary accesses, splitting a compound invariant across independently atomic fields, ignoring CAS failure ordering, retrying without updating expected state, assuming CAS detects ABA, using generic atomics for reference counts, relying on signed overflow folklore, confusing lock-free with wait-free, benchmarking uncontended operations only, and freeing an object after an atomic pointer swap while readers still hold it.

### Compact example

A stack head contains pointer A. Reader R snapshots A and pauses. Another thread removes A, uses B, then reuses the same address A. Plain CAS by R sees A and succeeds, although the stack changed. A tagged head `(A,0)` progresses through `(B,1)` to `(A,2)`, so R's comparison against `(A,0)` fails. Tag wrap and object reclamation still need a complete design; a finite tag alone is not universal protection.

### Connections

[OS-021](021-critical-sections-in-the-kernel.md) defines invariants, ordering, and lifetime; [OS-023](023-mutexes-semaphores-and-condition-variables.md) shows atomics beneath blocking fast paths. [OS-025](../ROADMAP.md) develops deadlock and progress. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies coherence, fences, CAS, LL/SC, and cache behavior.

## Governing Question

Atomic instructions are small, but the algorithms around them are not. An increment can safely count independent events, yet two atomic fields can expose an impossible combination. A release store can publish initialized data, yet it cannot keep that data alive after a reader obtains a pointer. A successful CAS can validate equality, yet miss A-to-B-to-A history.

Kernel code also spans compiler and hardware models. The compiler may reorder ordinary operations; processors may observe stores differently; architecture primitives have alignment and progress constraints; kernel APIs add their own ordering guarantees. Device registers obey separate access rules.

The governing question is how to select the atomic state representation and exact operation order, then prove atomicity, visibility, invariant preservation, progress, and reclamation without importing assumptions from a different model.

## Why This Matters

Atomics underpin counters, flags, reference ownership, lock fast paths, queues, bitmaps, per-CPU aggregation, and read-mostly structures. They can avoid blocking and reduce lock metadata for genuinely small state transitions.

Misuse creates failures that vanish under debugging. Relaxed publication can reveal uninitialized data. A retry loop can livelock under contention. ABA can corrupt a free list. Reference-count overflow can resurrect or prematurely release privileged objects.

Performance is conditional. One contended cache line serializes CPUs and creates coherence traffic. A lock can outperform a complex retry loop, particularly when protected work is large or fairness matters. Correct representation and measurement precede “lock-free” optimization.

## Prerequisites and Retrieval

Recall critical-section invariants from [OS-021](021-critical-sections-in-the-kernel.md), interrupt contexts from [OS-022](022-spinlocks-and-interrupt-context.md), and mutex fast paths and ownership from [OS-023](023-mutexes-semaphores-and-condition-variables.md). Understand binary representation, caches, compiler optimization, and happens-before.

Retrieve these distinctions:

- indivisibility, visibility, compound-state consistency, progress, and lifetime are separate;
- an atomic load or store can be relaxed, acquire, release, or stronger according to its contract;
- acquire without a matching observed release does not magically publish unrelated data;
- lock-free means system-wide progress, not bounded progress for every participant;
- a reference count protects lifetime only after a safe reference acquisition;
- ordinary RAM atomics do not replace MMIO accessors or DMA synchronization;
- an observed architecture behavior is not a portable model guarantee.

## Learning Objectives

After this module, you should be able to:

1. distinguish atomic load/store, exchange, fetch operations, CAS, and LL/SC;
2. select relaxed, acquire, release, acquire-release, or sequentially consistent ordering from a publication proof;
3. encode and validate state-machine invariants in one atomic representation where appropriate;
4. construct ABA, mixed-access, overflow, and stale-lifetime counterexamples;
5. classify obstruction-free, lock-free, and wait-free progress claims;
6. analyze contention, cache-line placement, retry, backoff, and real-time tails;
7. use litmus tests, kernel memory-model tools, KCSAN, stress, and architecture evidence with accurate limits.

## Core Exposition

### Atomicity is scoped

An operation is atomic for a specified object, width, alignment, access class, and model. A naturally aligned machine load may be indivisible on one architecture, but portable kernel code uses documented accessors. Larger objects may require locks or architecture-specific support.

Atomicity prevents a torn intermediate value; it does not make a sequence of two atomic operations indivisible. If `head` and `count` must change together, readers can observe a new head with an old count unless one combined state, lock, versioned snapshot, or other protocol protects the relation.

### Atomic loads, stores, and RMW

Loads observe, stores replace, exchange swaps unconditionally, and fetch-add, bit operations, or similar RMWs update atomically. CAS is conditional and returns success plus an observed value according to the API. Interfaces differ in whether expected is updated on failure.

Non-RMW operations can have different ordering from RMW variants even within one API family. Read the precise contract; a type named atomic does not make every surrounding expression atomic.

### CAS loops

A CAS loop loads expected state, computes desired state, attempts replacement, and on failure recomputes from the newly observed value. It must validate that desired computation remains legal and avoid applying irreversible side effects before success.

Weak CAS may fail spuriously and is suited to a loop; strong CAS avoids that specified spurious failure but still loses to interference. Failure ordering cannot generally be release because no value was published. Language and kernel interfaces constrain legal order pairs.

### LL/SC loops

LL reads and establishes a reservation; SC writes only if the reservation remains valid. Intervening writes, context events, granule conflicts, or implementation conditions can fail SC. Algorithms retry from a new linked load.

LL/SC can avoid equality-only ABA at the reservation level for one attempt, but it does not solve storage reclamation or unbounded retry. Architecture specifications define reservation granules and forward-progress constraints.

### Relaxed ordering

Relaxed atomic operations are useful when only the atomic value matters: statistics, independent counters, or state whose ordering is supplied elsewhere. They participate in the object's atomic modification behavior but do not publish arbitrary surrounding ordinary stores.

A relaxed counter may safely produce a unique ticket while the data associated with that ticket needs separate synchronization. “Atomic” in a type name is not shorthand for full fence.

### Release and acquire publication

A producer initializes payload fields, then release-stores a published pointer or ready flag. A consumer acquire-loads that same atomic and, when it observes the release sequence as defined by the model, may read the initialized payload.

Publishing before initialization reverses the required edge. Acquire-loading one flag does not order payload published through an unrelated atomic without a connecting model rule. Draw the happens-before chain explicitly.

### Sequential consistency

Sequentially consistent atomic operations add a single total-order property for participating operations. This simplifies some reasoning but does not combine separate operations into a transaction, repair object lifetime, or impose ordering on device accesses beyond their contracts.

Stronger ordering may incur cost or constrain optimization, but weakening requires proof. Begin with a clear correct model, then reduce strength with litmus and implementation review rather than guessing for speed.

### Compare-exchange state machines

Packing status, generation, owner, and flags into one word can make a compound transition atomic. Define every valid encoded state and transition, reject reserved combinations, handle integer wrap, and ensure bit-field operations cannot create illegal mixtures.

The state word may still point to external data. Atomic transition protects the word, while release/acquire publishes content and a separate protocol preserves the pointee's lifetime.

### ABA

CAS validates present equality, not intervening history. Reused pointers, free-list nodes, indices, and generation values create ABA. Tagged pointers or version counters expand identity; hazard pointers, epochs, RCU, or reference protocols delay reuse; LL/SC changes validation semantics.

Finite tags wrap. Pointer tagging has alignment, canonical-address, architecture, sanitizer, and provenance constraints. ABA mitigation must be evaluated with maximum outstanding lifetime and reuse rate.

### Reference counts

Reference counts encode ownership and destruction eligibility, not arbitrary arithmetic. Purpose-built kernel `refcount_t` semantics address saturation and misuse differently from `atomic_t`. Decrement-to-zero usually needs release of prior operations and ordering before destruction according to the API.

A nonzero count does not help if code read a stale pointer before safely incrementing. Acquisition must be protected by a lock, RCU read-side region, atomic conditional increment, or another protocol that prevents zero and free from racing.

### Atomic bit operations

Bitmaps compact flags and resource claims. Atomic test-and-set can claim one bit; clear can release under documented ordering. Operations on different bits can still contend on the same word and cache line.

Bit number, word layout, endian presentation, non-atomic variants, and ordering semantics differ across interfaces. A set bit may indicate ownership, eligibility, or state only if lifecycle and transition rules define it.

### Mixed atomic and ordinary access

Mixing atomic and ordinary accesses can create a data race or evade instrumentation unless the kernel model explicitly permits the pattern and accessors prevent compiler invention or tearing. Initialization-before-publication and access after quiescence are common controlled phases, but their boundaries need proof.

Diagnostic readers are not exempt. Use appropriate one-copy accessors or synchronization and label approximate snapshots where cross-field consistency is not guaranteed.

### Progress properties

Obstruction-free operations finish when eventually running alone. Lock-free algorithms guarantee some operation completes system-wide despite interference. Wait-free algorithms bound steps for each operation. These terms do not imply fairness, low tail latency, or resistance to preemption.

A lock-free loop can starve one CPU, and an interrupt can repeatedly disrupt LL/SC. Reclamation may block even when the update is lock-free. State the exact operation and execution model in progress claims.

### Contention and backoff

One atomic RMW obtains exclusive cache-line ownership and can serialize contending CPUs. Tight retries repeatedly invalidate caches and waste bandwidth. Backoff, batching, sharding, per-CPU counters, combining, or locks may improve throughput.

Backoff changes latency and fairness. Randomized delays complicate reproducibility; unbounded retries are unsuitable for hard timing paths. Measure retry counts, coherence events, service distributions, and useful work.

### False sharing and layout

Independent atomics on one cache line interfere despite no logical sharing. Alignment or padding can isolate hot fields, at memory-footprint cost. Layout assumptions depend on architecture cache geometry and allocator placement.

Per-CPU storage avoids common RMW contention but requires aggregation, hotplug, migration, and bounded staleness. Exact global values may still need synchronization.

### Interrupt and preemption contexts

Atomics do not sleep and can fit interrupt contexts, but a retry loop can still be unbounded. Atomic context in kernel terminology is not the same as an atomic variable. Interrupt-safe access also needs lifetime, ordering, and bounded-work review.

Disabling preemption can protect CPU-local selection; it does not make a global read-modify-write atomic. Local interrupt masking does not exclude remote CPUs.

### Device and persistent memory

MMIO registers can have side effects, widths, ordering, and access methods incompatible with ordinary atomics. DMA involves devices outside CPU coherence or with explicit synchronization. Persistent memory requires durability ordering beyond visibility.

Use subsystem and architecture accessors. Never cast device storage to an atomic type to reuse a CPU algorithm without an explicit specification.

### Verification and evidence

Litmus tests encode small concurrent executions and query allowed outcomes under a specified model. The Linux Kernel Memory Model and tooling can check kernel patterns. Architecture models and compiler behavior remain separate layers that must align with the kernel contract.

KCSAN detects sampled races and supports assertions under its documented model. Stress, fault injection, compiler variants, architecture tests, static review, and model checking provide complementary evidence. A clean result is scoped evidence, not proof.

### Security and assurance

Overflow, ABA, stale lifetime, and speculative or ordering mistakes can become use-after-free, authority reuse, disclosure, or denial of service. Treat identifiers and reference transitions as security boundaries.

Real-time and safety review bounds retries, contention, interference, reclamation, and fallback. Named specialists assess model assumptions and residual risk; this chapter claims no certification.

## Definitions and Notation

Let atomic object `A` have value domain `V` and modification order `mo_A` under the relevant model. Let `RMW(A,f)` atomically replace `x` by `f(x)`. Let CAS be `CAS(A,expected,desired)` and return success or the observed value.

Let `W_rel(P)` release-publish pointer or flag `P` after payload writes `D`; let `R_acq(P)` acquire-observe that publication before payload reads. Write `W_rel(P) ->sw R_acq(P)` for synchronizes-with when model conditions hold and `->hb` for resulting happens-before.

Let tagged identity be `(value,generation)`. Let retry count be `k`, and define progress claims only relative to scheduler and interference assumptions. Lifetime protocol `L` is separate from atomic state transition `T`.

## Mechanisms, Invariants, or Proof Structure

A reviewable atomic algorithm proceeds through eight obligations:

1. Define object width, alignment, domain, representation, and all access modes.
2. Define valid states and show every RMW preserves the encoded invariant.
3. Draw publication and observation edges; justify each memory order and failure order.
4. Enumerate CAS or LL/SC interference, spurious failure, recomputation, and side effects.
5. Construct ABA, wrap, overflow, mixed-access, and stale-reference counterexamples.
6. Prove obstruction-free, lock-free, wait-free, or bounded-retry claims under stated execution assumptions.
7. Separate coherent memory from MMIO, DMA, and persistence semantics.
8. Validate with model tools, race detection, stress, multiple architectures, and scoped evidence.

The executable model demonstrates equality-only ABA and tagged comparison.

<!-- bijux-verify: {"id":"toy-atomic-aba","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"plain-snapshot=A\nplain-current=A\nplain-cas=would-succeed\ntagged-current=A@2\ntagged-cas=would-fail\n","stderr":""}} -->
```python
plain_snapshot = "A"
plain_current = "A"
plain_current = "B"
plain_current = "A"

tagged_snapshot = ("A", 0)
tagged_current = ("A", 0)
tagged_current = ("B", 1)
tagged_current = ("A", 2)

print(f"plain-snapshot={plain_snapshot}")
print(f"plain-current={plain_current}")
print("plain-cas=" + ("would-succeed" if plain_current == plain_snapshot else "would-fail"))
print(f"tagged-current={tagged_current[0]}@{tagged_current[1]}")
print("tagged-cas=" + ("would-succeed" if tagged_current == tagged_snapshot else "would-fail"))
```

The sequential value history contains no real CAS, concurrency, wrap, memory order, pointer provenance, or reclamation. It illustrates missed history only.

## Alternatives and Trade-Offs

- Relaxed ordering permits optimization but cannot publish unrelated payload alone.
- Acquire and release encode directional publication with less global constraint than sequential consistency.
- Sequential consistency simplifies some reasoning while remaining weaker than a compound transaction.
- CAS supports conditional transitions but admits equality-based ABA and retry contention.
- LL/SC observes interference differently but has reservation and progress constraints.
- Packed atomic state makes transitions indivisible but restricts range and complicates encoding.
- Per-CPU counters scale writes but make exact aggregation and hotplug harder.
- Locks give ownership and blocking fairness options; lock-free paths avoid owner blocking but expand progress and reclamation proofs.
- Tags detect some reuse; delayed reclamation addresses underlying lifetime at storage and complexity cost.

## Failure Modes and Misconceptions

1. **“Atomic means fully ordered.”** ordering strength is a separate property.
2. **“Two atomic fields form an atomic record.”** readers can observe mixed generations.
3. **“Relaxed ready flag publishes payload.”** it lacks the required release/acquire edge.
4. **“Acquire orders everything.”** it must observe a matching publication under model rules.
5. **“Sequential consistency makes a transaction.”** multiple operations can still interleave.
6. **“CAS failure can be ignored.”** expected state and desired computation must be refreshed.
7. **“CAS detects intervening change.”** ABA defeats equality-only validation.
8. **“A wide tag eliminates ABA.”** finite tags wrap and reclamation remains.
9. **“Atomic counter is a reference counter.”** lifetime and saturation semantics differ.
10. **“Lock-free means every thread progresses.”** that is closer to wait-free, with assumptions.
11. **“Atomics are contention-free.”** one cache line can serialize the machine.
12. **“Preemption disable makes global updates atomic.”** remote CPUs remain.
13. **“CPU atomics work on device registers.”** MMIO and DMA have separate contracts.
14. **“A passing litmus or stress test proves the algorithm.”** model and coverage are scoped.

## Worked Examples

### Example 1

An independent packet counter uses relaxed fetch-add because no payload visibility depends on it. Reading an approximate total is acceptable under the documented metric contract.

### Example 2

A producer initializes descriptor fields then release-stores its pointer. A consumer acquire-loads that pointer before reading fields. Reversing initialization and publication permits incomplete data.

### Example 3

Head and count are separate atomics. A reader sees new head and old count. Packing both into one versioned state or locking the compound invariant prevents the mixed snapshot.

### Example 4

A CAS loop increments only if below a limit. After failure it must recompute against the observed current value; reusing the original desired value can exceed the limit or spin forever.

### Example 5

A free-list head changes A to B to reused A. Plain CAS succeeds from a stale snapshot. A generation tag detects this occurrence, while epoch or hazard reclamation prevents unsafe reuse.

### Example 6

A reader loads a refcounted pointer and increments after another CPU decrements zero and frees it. Safe acquisition under RCU or a lock is needed before conditional increment.

### Example 7

Sixty-four CPUs increment one global atomic counter. Throughput collapses from cache-line movement. Per-CPU counters plus periodic aggregation trade exact freshness for scale.

### Example 8

An LL/SC loop in an interrupt-heavy path repeatedly loses its reservation. System-wide progress elsewhere does not bound this operation. A lock, retry limit, or redesigned ownership may give better timing.

### Example 9

Code casts an MMIO register to an atomic integer and fetch-ors a bit. The device defines read side effects and write width, so the CPU RMW is invalid. Use documented register access and serialization.

### Example 10

An LKMM litmus test permits an outcome the author assumed forbidden. The design adds a release/acquire edge and reruns model, compiler, architecture, KCSAN, and stress evidence rather than adding an unexplained full barrier.

## Cross-Program Connections

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops language memory models, lock-free progress, ABA, and reclamation. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains coherence, atomic instructions, fences, caches, and device memory.

[Security Engineering](../../25-security-engineering/ROADMAP.md) frames overflow, stale authority, and use-after-free. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies timing, hazard, evidence, and assurance boundaries.

Within this program, [OS-025](../ROADMAP.md) compares deadlock with livelock and starvation, while later memory and driver modules apply atomic publication and hardware-access rules.

## References

- Linux Kernel documentation, [Atomic Types](https://docs.kernel.org/core-api/wrappers/atomic_t.html), current page checked 2026-09-04. RMW and non-RMW operations, ordering variants, signed arithmetic, and API guidance.
- Linux Kernel documentation, [Atomic Bitops](https://docs.kernel.org/core-api/wrappers/atomic_bitops.html), current page checked 2026-09-04. Atomic and non-atomic bit operations, ordering, return values, and instrumentation.
- Linux Kernel documentation, [Linux Kernel Memory Barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), current page checked 2026-09-04. Compiler and CPU ordering, acquire, release, atomics, locks, devices, and minimum guarantees.
- Linux Kernel documentation, [refcount_t API Compared to atomic_t](https://docs.kernel.org/core-api/refcount-vs-atomic.html), current page checked 2026-09-04. Saturating reference semantics, increments, decrements, ordering, and lifetime-oriented differences.
- Linux Kernel documentation, [Explanation of the Linux-Kernel Memory Consistency Model](https://docs.kernel.org/dev-tools/lkmm/docs/explanation.html), current page checked 2026-09-04. Events, program order, dependencies, reads-from, coherence, fences, and RCU ordering.
- Linux Kernel documentation, [Litmus Tests](https://docs.kernel.org/dev-tools/lkmm/docs/litmus-tests.html), current page checked 2026-09-04. Test structure, herd invocation, outcomes, and kernel memory-model interpretation.
- Linux Kernel documentation, [Linux Kernel Memory Model](https://docs.kernel.org/dev-tools/lkmm/index.html), current page checked 2026-09-04. Tool suite, documentation, simple and complex cases, and model resources.
- Linux Kernel documentation, [KCSAN](https://docs.kernel.org/dev-tools/kcsan.html), current page checked 2026-09-04. Sampling race detection, watchpoints, assertions, weak memory, configuration, and limitations.
- Linux Kernel documentation, [Sequence Counters and Sequential Locks](https://docs.kernel.org/locking/seqlock.html), current page checked 2026-09-04. Sequence operations, writer serialization, reader retry, barriers, and pointer lifetime cautions.
- GNU Compiler Collection, [Built-in Functions for Memory Model Aware Atomic Operations](https://gcc.gnu.org/onlinedocs/gcc/_005f_005fatomic-Builtins.html), current page checked 2026-09-04. Atomic operations, memory orders, compare-exchange, lock-free implementation, and target patterns.
- RISC-V International, [A Extension for Atomic Instructions](https://docs.riscv.org/reference/isa/unpriv/a-st-ext.html), current page checked 2026-09-04. LR/SC, AMOs, acquire and release bits, reservation sets, ordering, and progress constraints.
- Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), current page checked 2026-09-04. Locked operations, compare exchange, memory ordering, cache coherence, alignment, and architecture rules.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching atomic swap, acquire and release, spinlocks, reference counts, interrupts, and multicore races.

## Exercises

### Exercise 1

Classify ten atomic uses by required atomicity, ordering, compound invariant, progress, and lifetime. Select operations and justify their memory orders.

### Exercise 2

Write a publication proof for a descriptor pointer using release and acquire. Construct counterexamples for relaxed publication, unrelated acquire, and early publication.

### Exercise 3

Design a bounded tagged free-list head. Analyze ABA, tag wrap, pointer representation, reclamation, CAS retry, and failure ordering.

### Exercise 4

Compare global atomic, sharded per-CPU, spinlock, and mutex counters under contention. Design correctness and performance experiments across architectures and loads.

### Exercise 5

Construct an assurance review for an atomic state machine on a safety-relevant interrupt path. Cover progress, overflow, lifetime, verification, and human judgment.

## Answers to the Exercises

### Answer 1

An independent statistics increment needs atomic RMW but can often be relaxed. A ready flag that publishes payload needs producer release and consumer acquire. A unique ID fetch-add needs atomicity and defined wrap handling; it needs stronger ordering only if it also publishes state. A reference count uses the dedicated API and a safe acquisition protocol. A compound `(state,generation)` transition belongs in one encoded CAS or under a lock.

For each use, list all accesses, valid states, required visibility, failure order, retry side effects, overflow, contention, and reclamation. Do not choose sequential consistency merely to avoid writing the proof, though it can be a correct starting point.

### Answer 2

Producer writes every descriptor field, then release-stores pointer P. Consumer acquire-loads P and, only when non-null and observing the publication, reads fields. The release synchronizes with the acquire under the model, ordering prior field writes before subsequent reads. Reclamation separately keeps the descriptor alive.

A relaxed store and relaxed load preserve pointer atomicity but do not carry payload order. Acquire on unrelated flag Q lacks the required connection to P. Publishing P before initialization orders the wrong program sequence even with release. Litmus tests encode each case, but the proof remains tied to the kernel, compiler, and architecture contracts.

### Answer 3

Pack an aligned index or validated pointer representation with a generation into one supported atomic width. Every successful head replacement increments generation; CAS compares both. Validate reserved encodings and detect arithmetic wrap. Compute maximum reuse rate times maximum stale-observer lifetime; if wrap is reachable, a tag is insufficient.

Use epochs, hazard pointers, RCU, or locked reclamation to prevent storage reuse while a snapshot can survive. Recompute desired head after CAS failure, use legal acquire-release success and acquire or relaxed failure orders according to payload needs, and apply backoff or fallback under contention. Architecture pointer provenance and canonical-address rules may prohibit informal pointer packing.

### Answer 4

Define whether exact instantaneous count, eventual total, saturation, and overflow behavior are required. Global relaxed fetch-add is simple but contended. Per-CPU counters scale writes but need migration-safe access, aggregation, hotplug, and accepted staleness. A spinlock protects compound count metadata in non-sleeping contexts; a mutex permits sleepable longer work and may improve waiter behavior.

Cross CPU count, topology, architectures, contention, read frequency, migration, hotplug, overflow, and interrupt use. Verify totals and state invariants, then measure throughput, latency distributions, retries, cache traffic, energy, and observer overhead. Preserve compiler, kernel, firmware, layout, workload, and raw results. One benchmark does not establish a universal primitive.

### Answer 5

Define every encoded state and legal transition, width, alignment, overflow, compare failure, retry, and terminal safe state. Prove release/acquire publication and separate lifetime. Bound interference and retries or provide a reviewed fallback; a merely lock-free system-wide claim is insufficient for a task deadline. Exclude MMIO unless the device specification explicitly supports the operation.

Use LKMM litmus tests, compiler and architecture inspection, KCSAN, stress, fault injection, wrap acceleration, contention, interrupt storms, and reclamation tests with configuration provenance. Analytical review covers unobserved schedules and timing assumptions. Named kernel, memory-model, architecture, concurrency, real-time, security, safety, independent-verification, and acceptance owners assess evidence and residual risk. This chapter claims no certification.
