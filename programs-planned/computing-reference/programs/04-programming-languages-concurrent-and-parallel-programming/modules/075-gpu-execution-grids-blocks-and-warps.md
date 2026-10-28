---
module_id: CONPAR-075
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 75
title: GPU Execution Grids, Blocks, and Warps
status: complete
last_verified: 2026-08-29
---

# GPU Execution Grids, Blocks, and Warps

## One-Page Review

### Governing question

How should logical work be mapped to GPU grids, blocks/work-groups, threads/work-items, and warps/wavefronts/sub-groups so correctness does not depend on unspecified scheduling and performance remains portable?

### Essential definitions

- A **kernel** is a device function invoked over a parallel index space.
- A **grid** (or global ND-range) is the set of kernel instances for one dispatch.
- A **thread block/work-group** is a schedulable group whose work-items can use group-local memory and group-scoped synchronization.
- A **thread/work-item** is one logical kernel instance with identifiers and private state.
- A **warp/wavefront** is a hardware execution group of lanes; its size and scheduling rules are architecture-specific.
- A **sub-group** is a programming abstraction for a subset of a work-group with collective operations; size and guarantees may be implementation- or kernel-defined.
- A **global ID** identifies one work-item; a **local ID** identifies it inside its group; a **group ID** identifies the group.
- A **partial group/warp** contains lanes whose logical IDs fall outside the data domain or have exited.
- A **barrier** requires every participating member in its scope to arrive and supplies specified memory ordering.
- **occupancy/residency** concerns how many groups/warps can reside on a compute unit given register, local-memory, thread, and architectural limits.
- A **grid-stride loop** lets each launched work-item process multiple indices separated by total grid size.
- A **launch** is commonly asynchronous with the host; submission success is distinct from execution completion.

### Central model, mechanism, or theorem

For one-dimensional data of length n and block size B, logical global thread `g=block_id·B+local_id`. A one-element mapping acts only when `g<n`; choosing grid size `G=ceil(n/B)` covers each index once. Correctness additionally requires blocks be executable in any order, unless a specified cooperative mechanism provides broader synchronization. Within a group, barriers and shared state obey their exact scope. Hardware may partition work-items into warps/wavefronts, but implicit lockstep is not a portable synchronization proof.

### Critical invariants

Index linearization matches declared dimensions and uses overflow-safe arithmetic; every logical item is covered exactly as intended; extra work-items have no invalid effects; blocks/work-groups do not depend on unspecified relative order or simultaneous residency; all required group members reach each barrier in converged control; memory ordering and atomic scope match communicating participants; subgroup algorithms use queried/declared size and participation masks; partial warps are safe; launch dimensions and resource use satisfy device/kernel limits; host/device lifetimes include asynchronous completion; every launch and delayed execution error is checked; and results do not depend on race winners.

### Common failures

Programmers swap x/y/z linearization, underlaunch or duplicate items, overflow 32-bit products, omit the `g<n` guard, return before a later group barrier, spin on another block that cannot become resident, use warp lockstep as a fence, assume warp size 32 across vendors, call collectives with inconsistent participation masks, confuse local memory with per-thread local variables, select maximum block size as optimal, ignore registers/local memory limiting residency, free host/device storage before asynchronous work finishes, check only immediate launch status, or expect atomic serialization order to be deterministic.

### Compact example

For n=19 and B=8, `G=ceil(19/8)=3`; 24 work-items are issued. Global IDs 0–18 cover data exactly once and IDs 19–23 must be inactive. The third block is still a full scheduling/synchronization unit: inactive data lanes cannot simply skip a barrier needed by active lanes.

### Connections

[Explicit Vector Intrinsics](074-explicit-vector-intrinsics.md) contrasts CPU-exposed vector lanes with GPU scalar-thread programming. [Work Partitioning and Granularity](045-work-partitioning-and-granularity.md) supplies decomposition trade-offs. The [program roadmap](../ROADMAP.md) next covers GPU memory hierarchies, coalescing/divergence/occupancy, fusion, pipelines, and profiling.

## Governing Question

Which parts of GPU execution are contractual programming-model guarantees, which are implementation scheduling choices, and how can launch geometry express logical work without smuggling hardware folklore into correctness?

The hierarchy serves different roles. Global IDs express work ownership. Work-groups define a collaboration and synchronization boundary. Sub-groups expose selected collective behavior. Warps and wavefronts describe hardware grouping. Good kernels exploit relevant hardware facts for performance while remaining correct under every scheduling order the programming model permits.

## Why This Matters

GPUs obtain throughput from enormous numbers of lightweight work-items and fast switching among ready execution groups. A grid can contain far more blocks than the device can host at once; the scheduler distributes them across compute units. This scalability relies on blocks being largely independent and able to run in any order.

Many GPU bugs arise by confusing spatial identity with temporal order. Adjacent thread IDs need not execute before later IDs. Blocks with smaller IDs are not guaranteed to start first. Threads in one warp should not communicate through ordinary memory merely because they often issue together. Host code may proceed before a launch begins.

The same concepts appear under different names in CUDA, HIP, OpenCL, and SYCL. Learning the common model—index space, collaboration scope, execution subgroup, device scheduling, and asynchronous command dependencies—supports portable reasoning without erasing API-specific guarantees.

## Prerequisites and Retrieval

Retrieve:

- decomposition, chunks, load balance, and useful work from [Work Partitioning and Granularity](045-work-partitioning-and-granularity.md);
- lane masks and divergence from [SIMD Execution and Vector Lanes](071-simd-execution-and-vector-lanes.md);
- lifecycle and joining from [Creating and Joining Threads](011-creating-and-joining-threads.md); and
- barrier safety from [Barriers, Latches, and Phasers](016-barriers-latches-and-phasers.md).

Retrieval prompt: given n logical items, state which identifier owns each item, which work-items communicate, their synchronization scope, what happens to excess IDs, and whether any step assumes an execution order not guaranteed by the API.

## Learning Objectives

After completing this module, a learner can:

1. map CUDA/HIP grids, blocks, threads, and warps to OpenCL/SYCL ND-ranges, work-groups, work-items, and sub-groups;
2. derive one-, two-, and three-dimensional IDs and prove coverage;
3. design bounds-safe one-item and grid-stride mappings;
4. distinguish programming hierarchy, hardware execution grouping, residency, and issue order;
5. reason about divergence, active masks, partial warps, and independent thread scheduling;
6. apply barriers, fences, atomics, and collectives at correct scopes;
7. avoid cross-block deadlock and unsupported grid-wide synchronization;
8. choose valid launch dimensions from device and kernel resource limits;
9. validate asynchronous launch, completion, errors, and buffer lifetime; and
10. build reproducibility, performance, security, and high-stakes review evidence.

## Core Exposition

### Programming-model hierarchy

A host submits a kernel over a global index space. CUDA and HIP call the complete dispatch a grid, its groups thread blocks, and individual instances threads. OpenCL and SYCL commonly say ND-range, work-group, and work-item. These are close conceptual mappings, but exact limits, non-uniform group support, collective requirements, memory scopes, and errors come from each specification.

One-, two-, and three-dimensional identifiers make data mapping convenient. Dimensions are a coordinate system, not extra hardware. In a CUDA-style block, x varies fastest, then y, then z when linearized. Local linear ID is `lx + Bx·(ly + By·lz)`. The corresponding block linearization depends on grid dimensions. A wrong factor can map multiple work-items to one element or leave holes.

Use size types wide enough for maximum extents and checked host-side multiplication. A valid device limit per dimension does not imply their product is valid. Validate block dimension product, grid dimensions, dynamic local memory, and the kernel-specific maximum before launch.

### One-item mapping and coverage

For n elements and B threads per block, choose `G=(n+B−1)/B` only with overflow-safe ceiling division. Thread `g=block_id·B+local_id` acts if `g<n`. Every i in `[0,n)` has unique quotient/remainder `(floor(i/B),i mod B)`, proving exact coverage; G's final block may have inactive IDs.

The executable teaching model displays this mapping. It runs sequentially in Python and does not launch GPU work, model scheduling, barriers, warps, memory, or performance.

<!-- bijux-verify: {"id":"grid-coverage-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"items=19\nblocks=3\nthreads_per_block=8\nissued_threads=24\nactive_indices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]\ninactive_global_ids=[19, 20, 21, 22, 23]\ncoverage_complete=True\nduplicates=False\n","stderr":""}} -->
```python
items = 19
threads_per_block = 8
blocks = (items + threads_per_block - 1) // threads_per_block
active_indices = []
inactive_global_ids = []

for block_id in range(blocks):
    for local_id in range(threads_per_block):
        global_id = block_id * threads_per_block + local_id
        if global_id < items:
            active_indices.append(global_id)
        else:
            inactive_global_ids.append(global_id)

print(f"items={items}")
print(f"blocks={blocks}")
print(f"threads_per_block={threads_per_block}")
print(f"issued_threads={blocks * threads_per_block}")
print(f"active_indices={active_indices}")
print(f"inactive_global_ids={inactive_global_ids}")
print(f"coverage_complete={sorted(active_indices) == list(range(items))}")
print(f"duplicates={len(active_indices) != len(set(active_indices))}")
```

The bounds guard must surround every effect that requires a valid logical item. Yet a thread whose data ID is inactive may still need to participate in a work-group barrier. Separate “has data” from “is a member of the launched group.”

### Grid-stride loops

Instead of one element, work-item g can process `i=g, g+T, g+2T,...<n`, where T is total launched work-items. This decouples logical size from grid size, supports device-scaled launches, and amortizes setup. Coverage follows from unique remainder modulo T for each i when T>0.

Grid-stride loops can improve reuse and testability—a small launch can process a large input—but may change memory order, cache behavior, and per-thread workload. Ensure index addition cannot overflow. If per-element work is highly variable, static strides may imbalance; queues or compaction may help with new synchronization costs.

Do not confuse persistent work-items with guaranteed residency. A deliberately persistent kernel launches a bounded number of groups intended to remain and draw work. Its design must use documented occupancy/residency limits, queue atomics, termination, fairness, preemption/watchdog constraints, and coexistence policy.

### Blocks/work-groups as independence units

All work-items in a block execute on one compute unit for their residency and can access group-local/shared memory and barriers. The grid can exceed physical compute units because completed groups free resources for later groups. Therefore ordinary kernels must tolerate groups executing in any order, concurrently or serially.

A block cannot safely spin waiting for a flag from another block: the producer block might not be resident because waiting blocks occupy every resource slot. This is a scheduling-dependent deadlock. Split phases into separate kernel launches, use a specified cooperative grid launch whose residency conditions are satisfied, or redesign with atomics/queues whose progress assumptions are supported.

Block size is a collaboration and resource choice. It determines barrier membership, local-memory tile shape, partial warps, and register/local-memory allocation per block. A huge block may reduce how many blocks reside; a tiny block may waste warp lanes and scheduling capacity. Maximum legal size is rarely automatically optimal.

### Warps, wavefronts, and sub-groups

Hardware partitions a resident block into execution groups. NVIDIA calls 32-thread groups warps. AMD uses wavefronts whose size varies by architecture family; current HIP documentation distinguishes 64 for CDNA and 32 for RDNA. These values are current target facts, not universal GPU constants.

A programming sub-group exposes collectives such as ballot, shuffle, reduce, and barrier over an implementation-selected subset of a work-group. SYCL specifies that portable code must not assume order, a particular subdivision, or forward progress beyond guarantees. Query sizes and use APIs that declare required subgroup sizes only when device support is checked.

Warp/wavefront membership usually follows linear local IDs. A two-dimensional block shape changes which adjacent data coordinates share a hardware group because x linearizes fastest. Layout and block shape therefore affect coalescing and divergence, even though dimensionality itself is logical.

### SIMT execution and divergence

Work-items have scalar-like program state. Hardware issues instructions to active lanes in an execution group. When conditions vary, paths may execute with different active masks and reconverge. Divergence reduces useful lanes for path instructions, but is not automatically incorrect.

Correctness cannot rely on every lane executing each source statement simultaneously. NVIDIA independent thread scheduling explicitly invalidated some historical warp-synchronous patterns. Use documented subgroup/warp synchronization with an exact participation mask for communication. Active lanes can exclude threads that returned, took another path, or lie in a partial warp.

Calls to a collective must agree about participating members. A shuffle that names a source lane not active in the collective can yield unspecified behavior under its API. Compute the membership mask before divergence where required and ensure named lanes participate. Prefer group algorithms supplied by the programming model or reviewed library.

### Barriers and converged control

A work-group barrier waits for all required members and supplies a specified memory fence/scope. Every member must reach the same barrier instance or none, unless the API defines a narrower construct. Branching so half a block returns before `barrier()` while the remainder waits is invalid or deadlocking.

Bounds-safe tiled kernels often let inactive data threads load a neutral value into shared memory, participate in the barrier, and predicate final output. Alternatively choose a launch form with only full groups when the API permits and handle the tail separately. Never put a group barrier inside a loop whose iteration count differs by thread.

A barrier is not a universal cache flush or grid barrier. Its memory-order effects apply to specified address spaces and participants. Atomics have operation order plus memory order/scope; a device-scoped release/acquire protocol differs from a work-group barrier. Match scope to every communicating participant and keep non-atomic conflicting access race-free.

### Intra-group shared algorithms

Shared/local memory supports tiling, reuse, transposition, histograms, and communication. A typical phase has each thread load one or more elements, synchronize, compute from the shared tile, synchronize before overwriting if needed, then store. The first barrier publishes loads; the second prevents fast work-items from destroying values still in use.

Initialization must cover every shared location that can be read, including boundary tiles. Dynamic shared-memory sizes are launch inputs and must be computed without overflow and within kernel/device limits. Shared arrays are per block, not shared across the grid.

Bank conflicts, capacity, and access patterns influence performance and belong to the next modules. Here the correctness rule is that initialization, synchronization, lifetime, indexing, and memory ordering are complete for all work-items and paths.

### Races and atomics

Unique global IDs make a pointwise store race-free if each maps to a unique output. Histograms, reductions, queues, and scatter can make many threads update one location. Non-atomic conflicting accesses form a data race under the relevant device language and can produce undefined/unspecified results.

Atomics serialize updates to one location according to their scope/order, but the order among competing lanes may be unspecified. Integer addition can yield a deterministic total if no overflow semantic issue exists; floating atomic addition can vary by order. Compare-and-swap loops must handle contention and representation details. Local aggregation followed by fewer global atomics can reduce contention but adds barriers and shared-memory logic.

Do not elect a “winner” by ordinary same-warp writes. Even if hardware serializes writes, which lane wins may be undefined. Use an atomic operation whose return/value semantics define the election or a subgroup collective with specified tie-breaking.

### Launch geometry and device limits

Query device limits for grid dimensions, threads per block, dimensions per block, shared/local memory, subgroup sizes, and supported features. Kernel resource use—registers, local memory, barriers, and compiler attributes—can lower the valid or resident block size below a device-wide maximum.

Launch configuration balances enough groups to distribute work, enough threads per group to fill execution groups, local-memory tile shape, register use, tails, and per-thread work. Occupancy is the fraction/number of possible resident warps, not a correctness requirement or direct speed guarantee. A latency-independent compute-bound kernel may perform well below maximum occupancy; spilling to raise occupancy can hurt.

Use occupancy and launch calculators as candidate generators, then measure. Keep correctness independent of the number of simultaneously resident groups. Record compiler resource reports and reject launch/resource combinations that exceed limits with a clear error.

### Host-device asynchrony

Kernel submission commonly returns before device completion. Host code must not free, reuse, unmap, or mutate buffers until the relevant event/stream/queue dependency completes under the memory model. Operations in different streams/queues may overlap unless dependencies order them. Default-stream details are API-specific.

Some errors appear synchronously at submission—invalid dimensions or arguments—while execution faults appear only when the queue is synchronized or an event is queried. Check both layers. Associate error context with kernel, binary, device, launch dimensions, stream, inputs, and correlation ID without leaking sensitive data.

Timing asynchronous kernels requires device events or synchronization around the measured interval. A host timer around submission measures enqueue overhead, not completion. Warm-up, compilation, power state, transfers, and dependencies must be declared.

### Portability across APIs and devices

CUDA, HIP, OpenCL, and SYCL share hierarchy concepts but differ in naming, capability queries, non-uniform group rules, subgroup guarantees, memory scopes, synchronization, compilation, and error models. Write a semantic execution contract before mapping it to APIs.

Avoid assuming fixed subgroup size, exact group scheduling, compute-unit count, lockstep, independent subgroup progress, uniform group availability, or grid-wide barrier. Use feature queries and specialized variants when performance needs a property. Retain a general version.

Device kernels also face type-size, floating, address-space, recursion, allocation, and library differences. Compile and run the supported device matrix; a source that builds for one backend has not established portability.

### Verification strategy

Prove ID mapping algebraically and test it on a sequential model. On device, fill outputs with sentinels, record per-index visit counts in a debug kernel, and verify exactly one visit where required. Test n=0,1,B−1,B,B+1,multiple blocks, maximum/overflow-adjacent sizes, 2D/3D extents, and all block shapes.

Use race/sanitizer tools where available, but retain reasoned barrier and memory-scope review. Deliberately permute block behavior with delays and vary grid/block sizes to expose schedule assumptions. Run on devices with different compute-unit counts, subgroup sizes, and independent scheduling. Force partial groups and divergent paths.

Test asynchronous lifetimes by delayed kernels, queue overlap, cancellation/error, and early host reuse attempts in controlled harnesses. Check launch and completion errors. Compare output with an independent CPU/reference implementation under exact or declared numeric equivalence.

### Performance and operations

Measure end-to-end latency, kernel time, launch overhead, transfers, occupancy/residency, active lanes, branch efficiency, memory transactions, stalls, achieved bandwidth/throughput, and resource usage as appropriate. Do not optimize all metrics simultaneously; identify the limiting resource.

Benchmark representative data sizes, shapes, sparsity, divergence, work variance, cache state, concurrency, and devices. Compare block shapes and grid-stride work while keeping semantics fixed. Report binary/toolchain, driver/runtime, device/firmware, clocks/power mode, launch, repetitions, uncertainty, and correctness.

Production monitors need device loss, timeout, launch/completion error, memory pressure, queue latency, fallback rate, and performance by device class. Define CPU fallback or service degradation where required. A GPU may reset or be preempted; idempotency and checkpoint boundaries belong in the larger pipeline.

## Definitions and Notation

- `n`: number of logical work items.
- `B`: one-dimensional work-items per block/work-group.
- `G=ceil(n/B)`: groups for one-item mapping when B>0.
- `b`: group ID.
- `l`: local ID within a group.
- `g=bB+l`: global linear ID in the one-dimensional mapping.
- `T=GB`: total launched work-items.
- `W`: target warp/wavefront/subgroup lane count when explicitly established.
- `k`: active participation mask for a subgroup operation.
- `R_t`: per-thread register demand.
- `M_b`: per-block shared/local-memory demand.
- `C`: compute-unit resource capacity vector.
- `E`: host-visible completion event/dependency.
- `O`: required output equivalence relation.

Ceiling division must avoid overflow; one safe form for positive B and n>0 is `1+(n-1)/B`, with n=0 handled separately.

## Mechanisms, Invariants, or Proof Structure

### One-item coverage proof

For every i in `[0,n)`, Euclidean division yields unique `b=floor(i/B)` and `l=i mod B`, with `0≤l<B` and `b<G`; hence one launched thread owns i. Any launched g≥n is guarded and has no data effect. This requires B>0, sufficient launch dimensions, and overflow-free index arithmetic.

### Grid-stride coverage proof

For T>0, each i has unique remainder `g=i mod T` and quotient q with `i=g+qT`. Thread g visits that sequence until n, giving complete nonoverlapping coverage. The implementation must make addition/progress overflow-safe and ensure every launched g follows the same ownership rule.

### Barrier invariant

For each dynamic barrier instance, the required participant set is fixed by its scope and every member reaches it exactly once before proceeding. Required prior writes happen-before required later reads under the barrier's memory semantics. Data predicates may vary; barrier participation may not.

### Block-independence argument

Permute or serialize block executions arbitrarily. If a kernel's result and termination remain within O because blocks share no unsynchronized dependencies, it satisfies ordinary scalable scheduling. Any proof using concurrent residency or group-ID time order requires a stronger documented cooperative mechanism.

### Asynchronous lifetime invariant

Every memory object and kernel argument remains valid and unchanged as required until completion event E orders host reuse/free and dependent device operations. Submission success creates no completion happens-before edge by itself.

## Alternatives and Trade-Offs

| Mapping | Main benefit | Principal limitation |
|---|---|---|
| One item per thread | simple ownership and coalescing | overlaunch/tails and launch scale |
| Grid-stride loop | grid-size independence and reuse | more per-thread work and possible imbalance |
| One group per tile | shared reuse and local collaboration | barriers, boundary tiles, resource demand |
| Subgroup collective | efficient cross-lane operation | size/participation portability |
| Multiple kernel phases | natural grid-wide boundary | launch/intermediate-state overhead |
| Cooperative grid sync | in-kernel global phases | capability and residency constraints |
| Persistent kernel | amortized launch and dynamic work | queue, fairness, termination, coexistence complexity |
| Atomic global update | simple cross-group combination | contention and order nondeterminism |

Choose the simplest mapping whose ownership and synchronization proof matches the algorithm. Treat hardware-specific forms as guarded variants.

## Failure Modes and Misconceptions

- **“Thread IDs execute in increasing order.”** IDs name work; schedulers choose time.
- **“One block maps to one core forever.”** it resides on one compute unit, while assignment/order are dynamic.
- **“All blocks run together.”** grids commonly exceed residency.
- **“Blocks can spin-wait for each other.”** waiting blocks can prevent producers from residing.
- **“A warp is a language thread group.”** it is hardware-specific; subgroups carry programmable guarantees.
- **“Warp size is always 32.”** vendor and architecture families differ.
- **“Lockstep is a memory fence.”** use specified synchronization and masks.
- **“Inactive data threads may return before any barrier.”** group membership remains.
- **“A barrier orders the whole grid.”** its scope is limited.
- **“Atomics make results deterministic.”** contender order can remain unspecified.
- **“Local variables are shared local memory.”** per-thread local storage is private and may spill globally.
- **“Maximum block size maximizes performance.”** resource residency and workload shape matter.
- **“Maximum occupancy means maximum speed.”** it is one latency-hiding capacity metric.
- **“Launch return means work finished.”** execution is commonly asynchronous.
- **“No immediate error means success.”** faults may surface at synchronization.
- **“Host timers measure kernel time.”** without completion they measure submission.

## Worked Examples

### Example 1

**Coverage.** n=19,B=8 launches three blocks and guards IDs 19–23. **Conclusion:** overlaunch is safe only with complete effect bounds.

### Example 2

**2D linearization.** For block `(Bx,By)=(16,8)`, local `(x,y)=(3,2)` linearizes to `3+16·2=35`. **Conclusion:** x-fastest mapping determines warp neighbors.

### Example 3

**Grid-stride.** With T=6,n=14, thread 2 processes 2,8; thread 5 processes 5,11. All residues cover 0–13 once. **Conclusion:** a bounded grid can own arbitrary n.

### Example 4

**Barrier divergence.** Threads with `g≥n` return, while active threads later wait at a block barrier. The partial block deadlocks/violates the contract. Load neutral values and keep all members participating. **Conclusion:** data activity and synchronization membership differ.

### Example 5

**Cross-block deadlock.** Every resident block waits for a flag written by a not-yet-resident higher block. No resource slot remains. Split launches. **Conclusion:** ordinary block scheduling gives no concurrent-residency progress guarantee.

### Example 6

**Warp-synchronous race.** One lane writes shared data and another reads without an explicit warp/subgroup synchronization. Independent scheduling exposes stale data. **Conclusion:** execution grouping does not replace a specified happens-before edge.

### Example 7

**Atomic nondeterminism.** Thirty-two lanes atomically add floats to one accumulator. Every update occurs, but differing serialization orders can change rounding. **Conclusion:** race freedom does not guarantee bitwise reproducibility.

### Example 8

**Resource limit.** A 1024-thread block is device-legal but its registers/local memory allow only one resident block, while 256-thread blocks allow several and hide latency better. **Conclusion:** legal maximum is a candidate, not an optimum.

### Example 9

**Asynchronous lifetime.** Host enqueues a kernel then frees its device buffer before recording/waiting for completion. The kernel may access reclaimed storage. **Conclusion:** object lifetime follows dependency completion, not submission return.

### Example 10

**Radiation reconstruction kernel.** Mapping must preserve voxel/projection coordinates, calibration, units, bounds, masks, reduction order/error, image generation, launch/device capability, barrier/race safety, asynchronous lifetime, fault detection, deadlines, and CPU comparison. Named radiology, medical-physics, reconstruction/numerical, GPU/compiler, hardware/platform, real-time, software-safety, security/privacy, quality/regulatory, and independent verification reviewers must approve requirements and evidence; none is claimed here. **Conclusion:** exact grid coverage and GPU speed do not establish clinical safety.

## Cross-Program Connections

- **Algorithms:** maps, tiles, reductions, scans, queues, and graph frontiers imply different group boundaries.
- **Computer architecture:** compute units, execution groups, schedulers, registers, and local memory price launches.
- **Programming languages:** device memory models, scopes, address spaces, exceptions, and undefined behavior constrain kernels.
- **Distributed systems:** blocks resemble unordered independent partitions more than globally synchronized threads.
- **Numerical computing:** atomic/reduction order and heterogeneous floating behavior govern reproducibility.
- **Testing:** schedule perturbation, race tools, boundary launches, forced devices, and CPU oracles expose bugs.
- **Build/operations:** compiler, runtime, driver, device capability, binaries, queues, errors, and resets form provenance.
- **Security:** bounds, untrusted dimensions, shared data, timing, and device isolation require review.
- **Performance engineering:** occupancy, active lanes, stalls, and transfers are evidence, not semantics.
- **Safety engineering:** asynchronous failures and target-specific artifacts require traceability and independent review.

## References

1. John Nickolls, Ian Buck, Michael Garland, and Kevin Skadron, “Scalable Parallel Programming with CUDA,” *ACM Queue* 6(2), 2008. <https://doi.org/10.1145/1365490.1365500>
2. Erik Lindholm, John Nickolls, Stuart Oberman, and John Montrym, “NVIDIA Tesla: A Unified Graphics and Computing Architecture,” *IEEE Micro* 28(2), 2008. <https://doi.org/10.1109/MM.2008.31>
3. NVIDIA, *CUDA Programming Guide: Programming Model*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html>
4. NVIDIA, *CUDA Programming Guide: Advanced Kernel Programming and SIMT Execution*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html>
5. AMD, *Introduction to the HIP Programming Model*, current documentation; retrieved 2026-08-29. <https://rocm.docs.amd.com/projects/HIP/en/develop/understand/programming_model.html>
6. Khronos OpenCL Working Group, *OpenCL Unified API Specification*, current 3.1 documentation; retrieved 2026-08-29. <https://registry.khronos.org/OpenCL/specs/unified/html/OpenCL_API.html>
7. Khronos OpenCL Working Group, *OpenCL C Unified Specification*, current documentation; retrieved 2026-08-29. <https://registry.khronos.org/OpenCL/specs/unified/html/OpenCL_C.html>
8. Khronos SYCL Working Group, *SYCL 2020 Specification*, revision 12, 2026. <https://registry.khronos.org/SYCL/specs/sycl-2020/html/sycl-2020.html>
9. Khronos Group, *SYCL Reference: Work-Group and Sub-Group Algorithms*, current documentation; retrieved 2026-08-29. <https://github.khronos.org/SYCL_Reference/iface/group-algorithms-library.html>
10. ISO/IEC, *ISO/IEC 60559:2020 — Floating-Point Arithmetic*, 2020. <https://www.iso.org/standard/80985.html>

## Exercises

### Exercise 1

For n=1000 and B=256, derive G, total issued IDs, active/inactive IDs, and prove exact coverage using overflow-safe formulas.

### Exercise 2

Linearize a 3D block and grid, map a 3D tensor, and identify overflow, bounds, and warp-neighbor pitfalls.

### Exercise 3

Repair a tiled kernel in which out-of-range work-items return before a barrier. Specify initialization, barrier instances, and tail output.

### Exercise 4

Compare multiple kernel launches, cooperative grid synchronization, and a persistent queue for a three-phase irregular algorithm across small and large GPUs.

### Exercise 5

A regulated fraud-scoring service offloads batches to heterogeneous GPUs. Define mapping, numeric, concurrency, async-lifetime, compatibility, security, operational, and human-review evidence.

## Answers to the Exercises

### Answer 1

For positive n use `G=1+(n-1)/B=1+999/256=4`. Total issued T is 1024 after checked multiplication. IDs 0–999 are active and 1000–1023 inactive, 24 extra. For each i in `[0,1000)`, quotient `b=floor(i/256)` lies 0–3 and remainder `l=i mod 256` lies 0–255; unique Euclidean division gives `i=256b+l`, so one launched thread owns i. Conversely every g in 0–1023 is unique by block/local coordinates; guard `g<1000` suppresses extras. Validate B>0, device dimensions, T/product and g arithmetic in a sufficiently wide type, and n=0 as a separate no-work launch path.

### Answer 2

For local dimensions `(Bx,By,Bz)`, local linear ID is `x+Bx(y+Byz)`. For group coordinates and grid dimensions `(Gx,Gy,Gz)`, group linear ID is `gx+Gx(gy+Gygz)`. A tensor coordinate can use global components `X=gxBx+x`, and similarly Y/Z, guarded against extents. Use checked products for `BxBy`, block volume, `GxGy`, total groups/items, and tensor strides; validate per-dimension and product limits. x varies fastest in CUDA-style linearization, so warps group neighboring x until rows cross. Choosing Bx smaller than warp size makes one warp span y rows, which can alter coalescing/divergence. Tensor storage order may not match coordinate order; derive addresses separately. Partial coordinates must still participate in required group barriers.

### Answer 3

Replace early return with `valid=(global_id<n)`. Every work-item writes one shared slot: valid threads load input; invalid threads write a neutral or sentinel value suitable for the computation. All members reach barrier 1, compute only reads initialized slots, and all reach barrier 2 before any next-iteration overwrite if the algorithm reuses the tile. Only valid owners store final outputs. If later control varies, barrier instances remain uniform across the group. Prove neutral values do not change valid outputs or predicate their uses. Test zero/small/full/partial tiles, every remainder, guard pages, divergent data, race tools, and several group sizes.

### Answer 4

Separate launches provide a device-wide phase boundary through queue/event dependencies, work on any grid size, and free resources between phases; they cost submissions and global intermediate traffic. Cooperative grid synchronization can retain state and synchronize all groups only on devices/launches supporting it and only when the full cooperative grid residency rules are satisfied; it reduces portability and launch scale. A persistent queue adapts irregular work and amortizes launches, but needs atomics, termination detection, fairness, bounded resource residency, error/cancellation, watchdog/coexistence, and memory ordering. For broad portability start with launches, fuse only measured phases, use cooperative variants behind capability checks, and consider persistence for sustained dynamic workloads with an operational owner. Compare complete latency, load balance, memory traffic, occupancy, and failure behavior on smallest/largest supported devices.

### Answer 5

Specify batch/item ownership, feature schema, exact indexing, padding, model version, numeric precision/rounding/reduction tolerance, and deterministic result scope. Prove grid/grid-stride coverage, bounds, barrier convergence, race freedom or atomic semantics, subgroup portability, and overflow-safe launches. Maintain CPU/reference comparison and force every GPU/device/fallback path across batch and group boundaries, divergent data, errors, device loss, and delayed completion. Bind buffer lifetime to events; check submission and asynchronous failures; define retries/idempotency and prevent duplicate decisions. Query capabilities and qualify compiler/runtime/driver/device combinations. Measure end-to-end latency percentiles, throughput, transfers, queueing, resource use, and fallback under production distributions. Minimize/encrypt customer data and models, restrict/audit device and artifact access, isolate tenants, and define retention/incident response. Named fraud/risk, statistical/model-validation, numerical, GPU/compiler, platform, concurrency, security/privacy, operations/SRE, quality/regulatory, and independent assurance reviewers approve requirements, thresholds, bias/model evidence, and residual risk. GPU equivalence and speed do not validate the model or authorize regulated decisions.
