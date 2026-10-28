---
module_id: CA-018
program: Computer Architecture
level: 1
module_number: 18
title: Atomic Instructions
status: complete
last_verified: 2026-09-04
---

# Atomic Instructions

## One-Page Review

### Governing question

What must an ISA, memory model and implementation guarantee so atomic loads, stores and read-modify-write operations support correct synchronization across cores, devices, compilers and failures?

### Essential definitions

- An **atomic operation** appears indivisible with respect to the architectural observers and granularity defined by the memory model.
- A **read-modify-write** (RMW) atomically reads a memory value, computes, conditionally or unconditionally writes, and returns a specified result.
- **compare-and-swap** (CAS) writes a desired value only if the observed value equals an expected value.
- **load-reserved/store-conditional** (LR/SC) forms a conditional update whose store succeeds only if a reservation remains valid.
- An **atomic memory operation** (AMO) combines arithmetic/logical transformation with atomic memory access.
- A **linearization point** is an abstract instant between invocation and response at which a linearizable operation takes effect.
- **memory order** constrains relationships between memory events beyond indivisibility at one location.
- **acquire** prevents specified later operations from becoming observed before the acquire; **release** prevents specified earlier operations from becoming observed after the release.
- **sequential consistency** supplies a single total order consistent with each thread’s program order for the covered atomic operations.
- A **fence** orders named classes/domains of memory operations without necessarily accessing data.
- A **reservation set** is implementation-maintained state governing an SC attempt.
- **coherence** constrains writes and reads to a single location; **consistency** constrains observations across locations.
- **lock-free** progress means system-wide progress despite individual delay; **wait-free** means each operation completes in bounded own steps.
- The **ABA problem** occurs when a value changes from A to B and back to A, evading value-only comparison.
- A **spurious failure** is a permitted conditional failure not caused by an apparent value mismatch, under exact API/ISA rules.

### Central model, mechanism, or theorem

Model an atomic RMW on location `x` as one event

`(old, M') = Atomic_x(M, f)` where `old=M[x]` and `M'=M[x := f(old)]`.

No permitted observer sees the operation split into an independent read and write at the declared granularity. Ordering annotations add relations among events: release publishes prior effects, acquire consumes corresponding synchronization, and stronger orders constrain more executions. Correctness needs both per-location atomicity/coherence and the cross-location memory-model relation; neither substitutes for the other.

### Critical invariants

- Supported atomic sizes and required alignment/granularity are explicit.
- Each RMW returns the specified old/new/status value and performs at most the permitted write.
- CAS success and failure compare exact bits and apply their distinct ordering semantics.
- LR/SC reservations can fail conservatively but never allow a successful SC after a disqualifying event.
- Atomicity extends through caches/coherence to every in-scope observer and memory domain.
- Acquire, release, fence and sequentially consistent relations match the active memory model.
- Faulting atomics do not leave unauthorized partial ordinary effects.
- Progress claims name contention, scheduling, interruption and implementation assumptions.

### Common failures

Frequent failures are treating volatile as atomic, replacing an RMW with a load followed by a store, assuming atomicity implies sequential consistency, confusing coherence with ordering, implementing release after the publishing store, using acquire on the wrong load, assuming CAS failure has success ordering, retrying a weak operation without bounds or cancellation, assuming LR reserves an address forever, allowing SC success after an interfering write, performing unaligned atomic accesses without specified support, using atomic RAM semantics for MMIO, ignoring ABA, and declaring a lock-free algorithm wait-free.

### Compact example

Starting with counter 10, atomic fetch-add by 3 returns old value 10 and leaves 13. CAS expecting 12 fails and leaves 13; CAS expecting 13 and desiring 21 succeeds. An LR reads 21, but an intervening write to 22 invalidates its reservation, so SC of 30 fails. A new LR reads 22 followed by uninterrupted SC succeeds and leaves 30. These are abstract atomic outcomes; ordering and progress require multi-agent evidence.

### Connections

Atomic instructions connect coherence, memory consistency, compilers, language memory models, operating systems, lock-free algorithms, device I/O, virtualization, security, formal methods and performance.

## Governing Question

Concurrency fails when a logically indivisible update becomes multiple interleavable actions or when publication ordering is absent. Atomic instructions provide hardware-visible primitives, but useful synchronization depends on the memory model surrounding them.

The governing question is which observers, bytes, locations and events share the guarantee. A processor-local implementation trick is insufficient if another core or device can observe a torn or reordered result.

## Why This Matters

Locks, reference counts, concurrent queues, schedulers and runtimes build on atomic operations. One wrong ordering annotation can expose initialized flags before initialized data. One overly broad reservation assumption can livelock under interrupts or false sharing.

Atomics are expensive in ways that depend on topology and contention. A correctness-preserving design may still collapse under cache-line bouncing. Performance evidence therefore measures latency, throughput, fairness and tail behavior separately from semantics.

Verification crosses abstraction layers: language atomics lower through compiler IR to ISA instructions, which interact with coherence, caches and memory domains. Litmus tests, formal models, stress tests and RTL properties each establish bounded aspects.

## Prerequisites and Retrieval

Before studying this module, be able to:

- distinguish ordinary loads/stores from architectural events;
- explain caches and coherence conceptually;
- reason about interleavings and partial orders;
- distinguish ISA semantics from language/compiler semantics;
- model precise exceptions and fixed-width values.

Retrieve ISA/profile/version; supported atomic extensions; sizes and alignment; memory types/domains; RMW operations; CAS or LR/SC semantics; returned values/status; reservation invalidation; forward-progress rules; acquire/release/SC encodings; fence domains; coherence scope; mixed-size rules; unaligned behavior; translation/fault atomicity; cacheability; MMIO restrictions; language memory model; compiler mappings; kernel barriers; virtualization; executable axiomatic/operational model; litmus suite; RTL/coherence properties; contention benchmarks; fault injection; silicon errata; and exact tool/hardware revisions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish atomicity, coherence, consistency and progress;
2. specify fetch/update, swap, CAS and LR/SC state transitions;
3. reason about acquire, release, relaxed and sequentially consistent order;
4. identify alignment, size, scope and memory-type boundaries;
5. explain reservation invalidation and permitted SC failure;
6. relate language/IR atomics to ISA instructions and fences;
7. analyze ABA, retry loops, fairness and lock-free progress;
8. design litmus, stress, formal and implementation evidence;
9. assess atomics across devices, virtualization and failures;
10. govern compatibility and errata for synchronization primitives.

## Core Exposition

### Separate indivisibility and ordering

Atomicity says an operation is not observably torn at the specified granularity. It does not automatically order independent accesses before or after it.

Ordering modes constrain additional events. Always state both the atomic event and its memory-order relation.

### Define the observer scope

The guarantee can cover hardware threads in one coherence domain, all processors, accelerators or selected devices. Shareability and memory attributes affect scope.

Software must not synchronize through a location outside the guaranteed domain. “Atomic on this core” is not a multiprocessor contract.

### Define access granularity

Specify supported byte sizes, required natural alignment and whether mixed-size overlapping accesses participate in one atomicity domain.

An aligned word can still cross an implementation boundary at unusual widths. The ISA guarantee, not a cache-line intuition, decides legality.

### Atomic loads and stores

Some aligned loads/stores are individually atomic without being RMW operations. They can carry relaxed, acquire, release or stronger ordering.

A plain access racing with an atomic one can be illegal at the language level even if hardware reads whole words. Preserve the language contract through lowering.

### Atomic exchange

Exchange writes a new value and returns the old value as one event. It can implement simple locks but produces ownership traffic on every attempt.

Define result width, write value, ordering and fault behavior. An exchange to MMIO is not assumed valid without device semantics.

### Fetch-and-update operations

Fetch-add, fetch-and, fetch-or, minimum and maximum apply a defined fixed-width function and return old or new value as specified.

Arithmetic wraps or follows exact signed/unsigned comparison rules. Overflow flags are not implied unless the instruction defines them.

### Compare-and-swap

CAS reads a location and compares exact expected bits. On success it writes desired value; on failure it leaves memory unchanged and reports the observed value/status.

Success and failure can have distinct orderings. Failure performs a load-like observation and cannot use every write-side order in higher-level models.

### Strong and weak CAS

Weak CAS may fail spuriously under its contract, enabling efficient mappings to primitives such as LR/SC. Strong CAS suppresses spurious failure at its interface, commonly through retry.

Callers must distinguish mismatch from retryable failure. A retry loop needs cancellation, fairness and backoff analysis.

### Load-reserved

LR loads a value and establishes implementation reservation state covering an architecture-constrained set. The reservation is not ordinary software-visible ownership.

Context switches, exceptions, other stores or implementation events may invalidate it. Software cannot assume a duration beyond the specified constrained sequence.

### Store-conditional

SC writes only if the reservation is valid and returns success/failure status. It must not write on failure.

Success implies no disqualifying event under the architectural reservation rules. Failure can be conservative, so retry loops require progress provisions.

### Constrain LR/SC loops

Some architectures define a constrained loop shape/length to receive forward-progress guarantees. Extra loads, branches or instructions can fall outside it.

Compilers and hand-written assembly must preserve the required sequence. Instrumentation inserted inside it can silently weaken progress.

### Understand reservation granularity

Hardware may reserve more bytes than the accessed word, perhaps a cache block. Stores to nearby locations can cause false invalidation.

Software should avoid contentious neighbors, but cannot rely on the reservation being exactly one word unless specified.

### Define acquire

Acquire on a load/RMW prevents named later observations from moving before it in the relevant model. When it reads from a publishing release, it can make prior data visible.

Acquire on an unrelated operation does not retroactively validate a prior relaxed load. Synchronization depends on the actual relation and location/value flow.

### Define release

Release on a store/RMW orders named earlier effects before publication. Initialization must occur before the release event in program/model order.

A fence placed after a relaxed publication may be too late. Use the architecture/compiler’s defined mapping, not mnemonic intuition.

### Combine acquire and release

An RMW can be acquire-release, ordering prior and later operations while participating atomically at its location.

This does not impose a universal total order on every relaxed access. Sequential consistency is a separate stronger contract.

### Sequential consistency

SC atomics participate in a single total order consistent with the required per-thread order. This aids intuitive reasoning but can require stronger mappings.

SC does not repair data races on non-atomic objects under a language model. Nor does it necessarily mean hardware literally executes one instruction at a time.

### Use fences

Fences constrain order between classes of prior and later memory operations, sometimes with predecessor/successor bits or domains.

They do not make an ordinary multi-instruction read-update-write atomic. They also require compiler barriers so source operations are not moved across them.

### Distinguish coherence

Coherence provides a consistent per-location write order and read-value constraints. It supports atomic RMW serialization at one location.

Memory consistency adds relations across locations. Coherent caches alone do not guarantee message-passing order.

### Locate a linearization point

For a linearizable object, each completed operation takes effect at some point between call and response, respecting real-time precedence.

The hardware event may span requests and invalidations, but the abstract history must admit a valid point. Progress and linearizability are independent properties.

### Analyze message passing

Writer stores data, then release-stores a ready flag. Reader acquire-loads the flag and, when it observes publication, reads data.

Replacing release/acquire with relaxed operations can permit flag observation without corresponding data visibility, depending on the memory models.

### Analyze locks

Lock acquisition commonly uses acquire RMW; unlock uses release store. Mutual exclusion also needs ownership and protocol correctness.

Busy waiting creates contention and scheduling hazards. Kernel primitives may sleep or hand off after an adaptive spin.

### Handle ABA

CAS comparing only A cannot detect A→B→A. Reusing nodes or counters makes this relevant in lock-free structures.

Tagged versions, hazard pointers, epochs or non-reuse policies address different cases. Wider atomic pairs may support tagged updates but add alignment/cost.

### Define progress carefully

Obstruction-free, lock-free and wait-free have distinct guarantees. Hardware forward progress, scheduler fairness and memory allocation affect the implementation proof.

An instruction that eventually succeeds only without interference does not make an arbitrary retry algorithm wait-free.

### Apply backoff

Contention loops can repeatedly invalidate one another. Exponential or randomized backoff reduces traffic at the cost of latency and tuning.

Measure fairness and tail latency. Aggregate throughput can hide starvation of one participant.

### Map language atomics

Language models define data races, modification order, happens-before and memory-order APIs. Compilers map these into IR atomic operations, ISA atomics and fences.

Mappings can exploit dependencies and architecture strength, but must preserve every allowed/forbidden program execution of defined source programs.

### Preserve compiler barriers

Inline assembly or intrinsics must tell the compiler which memory/register effects occur. A hardware fence without an adequate compiler constraint can still permit compile-time movement.

Conversely, a compiler barrier alone generates no hardware ordering unless the target model already provides it.

### Treat mixed-size access

Overlapping byte, word and doubleword operations complicate atomicity and coherence. ISA and language rules may restrict such races.

Test partial overlap, adjacent fields and packed structures. Do not generalize aligned word guarantees to overlapping heterogeneous accesses.

### Handle faults precisely

An atomic instruction that faults on translation, permission or alignment must follow exact ordinary-effect suppression. It cannot expose a successful write without the specified returned status/value.

Cross-page atomics are often restricted. If supported, both pages and the full byte range need atomic authorization/commit behavior.

### Separate normal memory and MMIO

Device registers can have read/write side effects and bus-specific atomic support. Cache-coherent RMW semantics do not automatically apply.

Use platform-defined atomic or locking mechanisms. A failed CAS that rereads an MMIO register can itself cause an unintended action.

### Integrate DMA and accelerators

Non-CPU agents participate only if the interconnect, IOMMU and coherence domain provide compatible visibility and ordering.

Flush/invalidate or explicit synchronization may be required for noncoherent DMA. CPU atomics cannot create coherence the platform lacks.

### Virtualize atomics

Hypervisors can execute guest atomics natively on mapped memory or emulate traps. Emulation must preserve atomicity against all competing agents.

Migration serializes memory and relevant reservation behavior; reservations typically need invalidation rather than transfer as hidden guesses.

### Verify with litmus tests

Litmus tests enumerate small concurrent programs and observed outcomes. Compare hardware results with an executable axiomatic model for the exact ISA/profile.

Failure to observe an allowed weak outcome is not proof it is forbidden. Formal model checking complements repeated experiments.

### Verify RMW histories

Record invocation, response, returned values and writes across threads. Check whether a legal linearization and per-location modification order exist.

Stress repeated equal values, wraparound, CAS mismatch, reservation invalidation and contention. Preserve seeds/topology and avoid logging that serializes the test.

### Verify implementation mechanisms

RTL/coherence properties prove exclusive ownership, serialization, invalidation, no failed-SC writes, fault suppression and ordering tags.

Inject cache evictions, snoops, interrupts, TLB changes and errors around atomic operations. Compare commit and coherence traces without conflating them.

### Measure performance separately

Measure uncontended/contended latency, throughput, coherence messages, energy, fairness and tail distributions across sockets and memory types.

Performance counters are evidence only when events and multiplexing are understood. Correctness does not follow from smooth benchmark curves.

### Govern lifecycle evidence

Bind language/compiler version, flags, IR, ISA/profile, model, kernel, memory attributes, topology, RTL and silicon revision. Preserve binaries and litmus outcomes.

Track errata for ordering, reservations, cross-boundary access or coherence. A kernel workaround remains explicit and scoped to affected revisions.

## Definitions and Notation

- `M`: architectural shared-memory state.
- `x`: aligned atomic location and declared access width.
- `RMW_x(f)`: indivisible read and update of `x` by function `f`.
- `old`: value read at the RMW linearization point.
- `expected`, `desired`: CAS comparison and replacement operands.
- `success`: CAS/SC status defined by the interface.
- `Res(h)`: reservation state for hardware thread `h`.
- `po`: program-order relation within a thread.
- `co`: coherence/modification order for one location.
- `rf`: reads-from relation connecting a read to its source write.
- `hb`: happens-before relation in a higher-level memory model.
- `aq`, `rl`: acquire and release ordering annotations.
- `SC`: sequentially consistent order or store-conditional by context; spell out ambiguity.
- `scope`: set of observers governed by an atomic/order guarantee.
- `linearize(op)`: abstract effect point between invocation and response.

Arithmetic examples use fixed-width bit-vector semantics unless an operation explicitly names signed comparison.

## Mechanisms, Invariants, or Proof Structure

1. **Granularity obligation:** prove size, alignment, mixed-size overlap and observer scope match the atomic contract.
2. **RMW obligation:** prove read, transformation, write and returned old/new value form one indivisible event.
3. **CAS obligation:** prove exact-bit comparison, success write, failure nonwrite and separate orderings.
4. **Reservation obligation:** prove LR creation, every required invalidation and no successful SC after disqualification.
5. **Progress obligation:** prove claimed LR/SC or algorithm progress under named loop, contention, scheduling and interruption assumptions.
6. **Coherence obligation:** prove atomic writes occupy one permitted per-location modification order for all in-scope agents.
7. **Acquire obligation:** prove later named operations cannot be observed before the synchronizing acquire.
8. **Release obligation:** prove earlier named operations cannot be observed after the publishing release.
9. **SC obligation:** prove covered sequentially consistent operations admit the required total order.
10. **Fence obligation:** prove predecessor/successor classes, domains and compiler constraints match intended order.
11. **Fault obligation:** prove alignment, translation, permission and error paths suppress unauthorized partial effects.
12. **Mapping obligation:** prove language/IR atomics lower to ISA events preserving defined-program outcomes.
13. **Platform obligation:** prove cacheability, MMIO, DMA, accelerator and virtualization scopes use valid mechanisms.
14. **Security obligation:** prove contention, speculation and denial-of-service claims under an explicit threat model.
15. **Evidence obligation:** bind source, compiler, model, kernel, topology, tests, RTL, hardware and errata versions.

## Alternatives and Trade-Offs

1. **CAS versus LR/SC:** CAS gives direct expected-value updates; LR/SC can avoid ABA at reservation level but fail spuriously.
2. **Strong versus weak CAS:** strong simplifies callers; weak maps efficiently and expects retry.
3. **Old versus new return value:** old supports fetch semantics; new can save local arithmetic.
4. **Relaxed versus stronger ordering:** relaxed enables optimization; stronger order simplifies reasoning.
5. **Acquire/release versus SC:** acquire/release targets synchronization edges; SC supplies a broader total-order model.
6. **Implicit order versus explicit fences:** implicit orders simplify use; fences compose flexible access groups.
7. **Narrow versus wide atomics:** narrow save bandwidth; wide updates carry versions/pairs atomically.
8. **Strict versus permissive alignment:** strict rules simplify serialization; permissive support eases packed layouts.
9. **Small versus large reservation sets:** small sets reduce false failure; large sets simplify tracking.
10. **Spin versus block:** spinning avoids sleep overhead under short holds; blocking saves resources under delay.
11. **Aggressive versus conservative retry:** rapid retry lowers uncontended delay; backoff improves contended traffic/fairness.
12. **Lock-based versus lock-free:** locks simplify invariants; lock-free structures avoid owner blocking with harder reclamation.
13. **CPU-only versus system-scope atomics:** narrow scope is cheaper; system scope synchronizes heterogeneous agents.
14. **Native versus virtualized atomic execution:** native is fast; emulation offers control but must serialize globally.
15. **Experimental versus formal memory-model evidence:** tests reveal implementations; formal analysis covers permitted outcome space.

## Failure Modes and Misconceptions

1. “Volatile means atomic.” It governs different compiler/access concerns.
2. “Aligned means atomic for every size.” The architecture lists supported granularities.
3. “Atomic means sequentially consistent.” Indivisibility and ordering are distinct.
4. “Coherence orders all locations.” It primarily constrains each location.
5. “A load then store equals RMW.” Another observer can interleave.
6. “CAS failure writes expected memory.” It must leave memory unchanged.
7. “CAS failure has success ordering.” Interfaces can specify weaker failure order.
8. “Weak CAS failure proves mismatch.” Spurious failure may be allowed.
9. “Strong CAS solves ABA.” Equal bits can reappear after intermediate change.
10. “LR locks an address.” It creates a conditional reservation, not ownership.
11. “Reservation size equals operand size.” Implementations may track more.
12. “SC eventually succeeds under arbitrary code.” Progress can require a constrained loop.
13. “A failed SC may still store before reporting failure.” Failure must not perform its conditional write.
14. “Acquire on any later load orders an earlier relaxed observation.” Synchronization depends on the correct event.
15. “A fence after publication creates release publication.” It may be too late.
16. “A hardware fence stops compiler motion automatically.” Compiler semantics must also constrain movement.
17. “SC atomics make non-atomic races safe.” Language race rules still apply.
18. “Unaligned atomic support guarantees cross-page success.” Translation/permission boundaries can restrict it.
19. “Normal RAM atomics apply to MMIO.” Device protocols can differ fundamentally.
20. “CPU coherence includes every DMA device.” Platform topology and attributes decide.
21. “Lock-free means every thread progresses.” It is system-wide progress.
22. “Wait-free means fast.” Bounds can be large; performance is separate.
23. “Backoff changes correctness.” It normally changes progress/performance assumptions.
24. “Litmus non-observation proves an outcome forbidden.” Rare allowed behaviors may not appear.
25. “Logging cannot affect a concurrency test.” It can serialize or perturb timing.
26. “A software workaround erases atomic errata.” Affected hardware remains a deviation.

## Worked Examples

### Example 1

Fetch-add on value 10 by 3 returns 10 and atomically changes the location to 13.

### Example 2

CAS expecting 12 observes 13, reports failure and leaves 13 unchanged; no desired-value write occurs.

### Example 3

CAS expecting 13 and desiring 21 observes 13, reports success and changes memory to 21.

### Example 4

LR reads 21; an interfering store writes 22 and invalidates the reservation; SC of 30 fails and memory stays 22.

### Example 5

A fresh LR reads 22 followed by an uninterrupted valid SC of 30 succeeds and memory becomes 30.

### Example 6

Release-store of `ready=1` after data initialization and acquire-load observing that release can publish the earlier data.

### Example 7

Two fetch-add operations on one counter serialize in some coherence order, returning distinct old values even if issued concurrently.

### Example 8

CAS on a pointer equal to A cannot distinguish unchanged A from A→B→A; a version tag changes the compared bits.

### Example 9

A naturally aligned CPU atomic to cacheable RAM can be valid while the identical width at an MMIO address is unsupported.

### Example 10

A litmus outcome forbidden by the formal model but observed on hardware is evidence of mapping, model, implementation or test-harness error requiring isolation.

## Cross-Program Connections

- **Caches/coherence:** ownership and serialization implement atomic updates at shared locations.
- **Memory consistency:** acquire, release, fences and SC constrain cross-location observations.
- **Compilers/languages:** race and happens-before semantics map into IR and ISA events.
- **Operating systems:** locks, schedulers, futexes and interrupt paths rely on atomics/barriers.
- **Data structures:** queues, stacks, counters and reclamation use RMW primitives.
- **Devices:** MMIO, DMA and accelerators require platform-scoped synchronization.
- **Virtualization:** guest atomics and migration must retain global indivisibility/order.
- **Formal methods:** axiomatic relations, linearizability and progress properties support proofs.
- **Security:** contention, denial of service and speculation cross synchronization boundaries.
- **Performance:** cache-line movement, retries and topology determine cost.

## References

1. RISC-V International, [A Extension for Atomic Instructions](https://docs.riscv.org/reference/isa/unpriv/a-st-ext.html), LR/SC, AMOs, acquire/release bits and progress constraints; retrieved 2026-09-04.
2. Arm, [Arm Architecture Reference Manual for A-profile Architecture](https://developer.arm.com/documentation/ddi0487/latest/), exclusive accesses, atomic operations, barriers and memory ordering; retrieved 2026-09-04.
3. Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), locked operations, atomicity, ordering and system behavior; retrieved 2026-09-04.
4. LLVM Project, [Memory Model for Concurrent Operations](https://llvm.org/docs/LangRef.html#memory-model-for-concurrent-operations), IR atomics, orderings and compiler semantics; retrieved 2026-09-04.
5. Linux Kernel, [Linux Kernel Memory Barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), kernel ordering primitives, compiler effects and architecture mappings; retrieved 2026-09-04.
6. WebAssembly Community Group, [Threads Proposal](https://github.com/WebAssembly/threads), shared memory and atomic instruction semantics for WebAssembly; retrieved 2026-09-04.
7. herdtools7 Project, [herdtools7](https://github.com/herd/herdtools7), litmus tests and executable weak-memory model tooling; retrieved 2026-09-04.
8. ISO C++ Draft, [Multi-threaded Executions and Data Races](https://eel.is/c++draft/intro.races), happens-before, modification order, data races and atomic semantics; retrieved 2026-09-04.

## Exercises

### Exercise 1

Specify abstract transitions and returned values for exchange, fetch-add, successful/failed CAS and successful/failed SC.

### Exercise 2

Execute a deterministic abstract sequence containing fetch-add, two CAS attempts and two LR/SC attempts with one reservation invalidation.

### Exercise 3

Explain why release/acquire message passing can publish data while atomic relaxed flag operations alone need not.

### Exercise 4

Design conformance evidence for LR/SC progress, invalidation, faults and ordering in a multicore out-of-order processor.

### Exercise 5

Construct assurance for a lock-free queue shared among CPUs and a coherent accelerator, including compiler, reclamation, progress and errata.

## Answers to the Exercises

### Answer 1

Exchange reads old, writes desired and returns old in one event. Fetch-add reads old, writes fixed-width `old+delta` and returns whichever old/new convention the instruction defines. CAS reads observed; equality writes desired and reports success, mismatch leaves memory unchanged and reports failure/observed value.

LR returns memory and creates a reservation. SC with valid reservation atomically writes and reports success; invalid reservation performs no write and reports failure. Each transition additionally carries its declared ordering and can take a precise fault path before ordinary effects.

### Answer 2

The model records abstract sequential outcomes; reservation invalidation is explicit.

<!-- bijux-verify: {"id":"atomic-operation-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"fetch_add old=10 delta=3 new=13\ncas expected=12 desired=20 observed=13 success=false memory=13\ncas expected=13 desired=21 observed=13 success=true memory=21\nlr value=21 reservation=true\ninterfering_store value=22 reservation=false\nsc desired=30 success=false memory=22\nlr value=22 reservation=true\nsc desired=30 success=true memory=30\n"}} -->
```python
memory = 10
reservation = False

old = memory
memory = old + 3
print(f"fetch_add old={old} delta=3 new={memory}")

for expected, desired in ((12, 20), (13, 21)):
    observed = memory
    success = observed == expected
    if success:
        memory = desired
    print(
        f"cas expected={expected} desired={desired} observed={observed} "
        f"success={str(success).lower()} memory={memory}"
    )

value = memory
reservation = True
print(f"lr value={value} reservation={str(reservation).lower()}")
memory = 22
reservation = False
print(f"interfering_store value={memory} reservation={str(reservation).lower()}")
success = reservation
if success:
    memory = 30
print(f"sc desired=30 success={str(success).lower()} memory={memory}")

value = memory
reservation = True
print(f"lr value={value} reservation={str(reservation).lower()}")
success = reservation
if success:
    memory = 30
reservation = False
print(f"sc desired=30 success={str(success).lower()} memory={memory}")
```

The trace proves only sequential abstract value/status effects. It supplies no concurrent atomicity, memory ordering, coherence, fairness, fault or hardware evidence.

### Answer 3

Writer performs ordinary data writes before a release store to the flag. Reader’s acquire load must observe the relevant release (or defined release sequence) before consuming data. The resulting synchronization/happens-before edge constrains visibility according to the language and ISA mappings.

Relaxed atomic flag operations preserve atomic modification of the flag but do not by themselves create the required cross-location ordering. Hardware/compiler may expose flag before data under permitted executions. Exact claims depend on the selected language, IR and ISA models.

### Answer 4

Prove LR establishes reservation, all architecturally required events invalidate it, no invalid SC writes, and every successful SC participates in coherent order. Exercise same-address/nearby stores, cache evictions, snoops, context switches, exceptions, TLB changes and multiple hardware threads.

Run constrained loops under permitted interference assumptions to test progress without claiming bounded wait. Inject translation, permission, alignment and bus faults and verify precise nonwrite paths. Use formal ordering properties and litmus tests for acquire/release/SC. Compare executable model, RTL commit and coherence traces with exact configuration/topology.

### Answer 5

Define queue linearization points, invariants, memory reclamation, ABA protection, language orders and accelerator coherence scope. Prove compiler lowering from source atomics through IR to ISA/fences and platform fabric. State lock-free progress assumptions for CPUs, accelerator, scheduler and allocation.

Stress topology, wraparound, equal values, empty/full races, delayed participants and reclamation. Validate DMA/IOMMU attributes, virtualization and reset. Use history checking, litmus/model analysis, RTL/fabric properties and hardware tests without intrusive logging. Track compiler, firmware, kernel, accelerator and silicon errata. Named algorithm, language/compiler, ISA, coherence, accelerator, OS, formal, performance, safety/security and independent-assurance reviewers assess their scopes. This module supplies no certification.
