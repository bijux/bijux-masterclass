---
module_id: CONPAR-076
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 76
title: GPU Memory Hierarchies
status: complete
last_verified: 2026-08-29
---

# GPU Memory Hierarchies

## One-Page Review

### Governing question

How should data be placed, moved, cached, shared, synchronized, and measured across host and GPU memory so that kernels are correct and total data movement—not just arithmetic—is controlled?

### Essential definitions

- An **address space** is a programming-model region with accessibility, scope, lifetime, and pointer rules; it is not necessarily one physical memory technology.
- **global/device memory** is persistent device-visible storage accessible across work-groups, commonly backed by device DRAM and caches.
- **shared/local memory** is programmer-managed group-scoped storage, commonly on a compute unit; CUDA says shared, OpenCL/SYCL say local.
- **private state** belongs to one work-item and may reside in registers or spill-backed device memory.
- CUDA **local memory** is per-thread, compiler-managed storage commonly backed by device memory; “local” therefore means a different thing from OpenCL/SYCL local address space.
- **constant/read-only memory** is immutable to kernels under a specified lifetime and may use broadcast-oriented caches.
- A **cache** transparently retains copies; a **scratchpad** such as shared/local memory is explicitly populated and synchronized.
- A **register spill** moves compiler-allocated private values to memory because of pressure, dynamic indexing, or other constraints.
- **tiling** loads a bounded region into faster group-local storage for reuse.
- **unified virtual addressing** gives coordinated pointer values/ranges; **unified/managed memory** additionally supports access from multiple processors, often with migration or shared coherence.
- **page migration** changes physical residency, usually after faults, hints, or runtime policy.
- **pinned host memory** is non-pageable host storage suitable for direct/asynchronous device transfer; it is a limited resource.
- **memory scope/order** defines which agents participate in synchronization and which accesses become visible.

### Central model, mechanism, or theorem

For each logical value, track `(owner, physical residency, address space, readers/writers, lifetime, transfer path, consistency edge)`. A tile is beneficial only when avoided lower-level traffic and improved access exceed tile loads/stores, synchronization, capacity, bank/occupancy, and conversion costs. Correctness requires every reader be ordered after the writer at a scope containing both, every address be valid in its space and lifetime, and host/device reuse wait for asynchronous completion. A shared pointer or virtual address alone proves none of residence, coherence, or order.

### Critical invariants

Every allocation has one declared owner and deallocation event; pointers are dereferenced only by permitted agents/address spaces; byte counts, pitches, offsets, and transfer ranges are overflow-safe and in bounds; asynchronous copies/kernels retain storage until completion; shared/local tiles initialize every read element and all group members reach required barriers; private arrays/spills are not mistaken for on-chip group storage; atomics/fences/barriers use scope covering communicators; constant data is not mutated while read; managed-memory placement and migration policy is capability-checked; replicas have version/invalidation rules; oversubscription and peer access have failure/fallback plans; and performance claims include transfers, faults, migration, cache state, ECC, and resource trade-offs.

### Common failures

Teams treat all memory named “local” as fast, assume a pointer tells physical residence, confuse unified virtual addressing with coherent shared memory, use shared memory without enough reuse, return before a tile barrier, omit the second barrier before overwriting a tile, exceed shared capacity or spill registers while optimizing, copy a two-dimensional pitch as a dense width, free a buffer after submission rather than completion, mutate host-visible managed pages concurrently without supported atomics, thrash migrated pages between CPU/GPU, overuse pinned memory, ignore peer topology, infer cache policy from an old architecture, or benchmark a warm kernel while excluding allocation and transfer.

### Compact example

Six adjacent outputs of a three-point stencil need 18 logical input reads if every output independently loads left/center/right. One group can load the eight-element interval spanning the six outputs plus halos into shared memory, then reuse it: a simplified lower-level load reduction of `18/8=2.25`. This is not a 2.25× speedup; barriers, occupancy, caches, banks, boundaries, and stores remain.

### Connections

[GPU Execution Grids, Blocks, and Warps](075-gpu-execution-grids-blocks-and-warps.md) defines work-group scope and barrier participation. [Data Layout for Vectorization](072-data-layout-for-vectorization.md) supplies address, stride, and transfer reasoning. [Happens-Before Relations](023-happens-before-relations.md) supplies synchronization vocabulary. The [program roadmap](../ROADMAP.md) next studies coalescing/divergence/occupancy and then fusion and heterogeneous pipelines.

## Governing Question

For each datum in a heterogeneous computation, where does it reside, which agents may access it, what makes writes visible, how often does it move, and which measured bottleneck justifies changing that plan?

The phrase “GPU memory” hides several independent axes: physical DRAM or on-chip storage, programming address space, cacheability, allocation API, ownership, accessibility, persistence, and consistency. Precise designs name all axes rather than selecting a memory keyword by folklore.

## Why This Matters

GPU arithmetic throughput has grown faster than the ability to move arbitrary data. A kernel with abundant operations can still spend most cycles waiting for device DRAM, address translation, page migration, or host-device transfers. Conversely, a carefully tiled kernel can convert redundant loads into on-chip reuse and expose enough ready warps to hide remaining latency.

Memory mistakes are also correctness and security failures. A group-local pointer passed outside its lifetime, an early buffer free, a weakly ordered producer/consumer flag, an overflowed copy extent, or an uninitialized boundary tile can corrupt results. Managed memory simplifies pointer ownership but can introduce invisible migration, capability-specific coherence, and operational instability.

The durable approach is a data-movement ledger plus memory-model proof. Hardware-specific tuning comes after those artifacts exist.

## Prerequisites and Retrieval

Retrieve:

- grids, group scope, barriers, resource residency, and asynchrony from [GPU Execution Grids, Blocks, and Warps](075-gpu-execution-grids-blocks-and-warps.md);
- mapping, strides, alignment, useful bytes, views, and conversions from [Data Layout for Vectorization](072-data-layout-for-vectorization.md);
- lanes, masks, and fault suppression from [SIMD Execution and Vector Lanes](071-simd-execution-and-vector-lanes.md); and
- ordering and visibility from [Happens-Before Relations](023-happens-before-relations.md).

Retrieval prompt: for one kernel pipeline, list every allocation, byte range, current physical location, address space, owner, readers/writers, copy/migration event, completion dependency, and release event. Which items are facts, runtime policies, or measurements?

## Learning Objectives

After completing this module, a learner can:

1. distinguish address space, physical storage, allocation kind, accessibility, scope, lifetime, and cache;
2. compare registers/private state, spills/local memory, shared/local scratchpads, global, constant, texture/image, and host memory;
3. design correct shared-memory tiles with halos, barriers, and capacity bounds;
4. calculate simplified reuse, useful-byte, copy, and migration costs without calling them speedups;
5. apply device memory consistency, barriers, fences, atomics, and system/peer scope;
6. distinguish explicit copies, pinned/mapped memory, unified addressing, managed memory, and SYCL USM kinds;
7. reason about page placement, first touch, prefetch/advice, thrashing, oversubscription, and peer topology;
8. diagnose register spills, cache/TLB behavior, shared-bank conflicts, and occupancy trade-offs;
9. verify bounds, lifetimes, transfers, races, placement, fallbacks, and end-to-end performance; and
10. scope privacy, safety, and external review for high-stakes device memory.

## Core Exposition

### Separate namespaces from hardware

CUDA's common spaces are registers, local, shared, global, constant, and texture/surface. OpenCL C names private, local, global, constant, and generic address spaces. SYCL describes private, local, global, and generic device spaces plus buffers/accessors and unified shared memory (USM). HIP follows CUDA-like terminology on AMD devices.

The overloaded word “local” is hazardous. CUDA local memory is private to one thread and usually backed by device memory/cache; it commonly holds spills or automatic arrays unsuitable for registers. OpenCL/SYCL local memory is visible to a work-group and commonly maps to an on-chip scratchpad (AMD LDS, CUDA shared memory). Translate by scope and semantics, never by spelling.

Address spaces constrain pointers and access. An OpenCL global pointer and local pointer can have different representations; cross-space casts or lifetime escapes may be invalid. Generic spaces improve expressiveness but do not erase accessibility or performance differences.

Physical implementation can change. Shared memory and L1 may share/configure on-chip capacity on some architectures. Constant/texture spaces can be views of device memory with specialized caches. A specification provides semantics; current vendor architecture guides and measurements provide physical cost.

### Registers and private state

Registers hold per-thread scalars and compiler temporaries with low access latency. They are allocated statically per kernel launch context, not dynamically cached. Higher per-thread register demand can reduce resident warps/blocks because the compute unit's register file is finite.

Large automatic arrays, dynamically indexed values, address-taken variables, calls, or register pressure can cause private data to spill to local memory backed by device memory. Source variables do not map one-to-one to registers; inspect compiler resource reports and generated code. A spill can introduce global-memory traffic while the source still says “local variable.”

Reducing registers by recomputing, changing unroll, narrowing live ranges, or capping compiler allocation may improve occupancy or may add instructions/spills. Measure. Correctness must never depend on a value remaining in a physical register.

### Global memory, caches, and translation

Global/device memory is the large persistent space visible to kernels and commonly backed by attached DRAM such as GDDR or HBM. Per-compute-unit L1/data caches and a device-wide L2 reduce some traffic; exact policies, line/sector sizes, allocation, write behavior, and coherence vary by generation and access kind.

Caches are transparent and finite. A first access may miss, adjacent lanes may coalesce into transactions, reused data may be evicted, and a working set can exceed cache/TLB capacity. Do not encode correctness through an assumed cached copy. Synchronization rules define visibility; caches implement them.

Virtual addressing adds page translation and TLBs. Scattered accesses across many pages can increase misses even when byte volume is modest. Huge pages or allocation policy may help on supported systems but change fragmentation, migration, and operations. Record the actual platform.

Device DRAM bandwidth is shared among compute units, copy engines, peers, displays/services, and concurrent workloads. Peak specification bandwidth is not sustained application bandwidth. ECC can add capacity/traffic effects. Measure useful and transferred bytes where counters permit.

### Shared/local scratchpads

Shared/local memory is allocated per resident work-group and explicitly managed. Work-items cooperatively load data, synchronize, reuse it, synchronize before overwrite when necessary, and store results. It is valuable for cross-thread communication, reuse, reorganizing access, reductions, and staging asynchronous copies.

Every read must follow an initialized write from a participating thread. Boundary work-items can load neutral/padded halo values but must still reach barriers. The first barrier publishes the tile; a second barrier is needed if some threads can overwrite storage for the next tile while others still consume the current one.

Static plus dynamic shared allocation must stay within per-block and per-compute-unit limits. Larger tiles can improve reuse while reducing resident blocks and increasing boundary cost. Alignment and padding can remove bank conflicts or create wasted capacity. The next module treats bank/coalescing/occupancy optimization; here they are costs in the tile decision.

### A tiled-reuse teaching model

The following sequential model computes six outputs of a three-point stencil. It compares logical lower-level reads without and with one perfectly staged tile. It does not model caches, transactions, banks, synchronization cost, occupancy, GPU instructions, or runtime.

<!-- bijux-verify: {"id":"stencil-tile-reuse-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"output_indices=[4, 5, 6, 7, 8, 9]\nnaive_loads=18\ntile_input_indices=[3, 4, 5, 6, 7, 8, 9, 10]\ntiled_loads=8\nmodeled_reuse_factor=2.250\noutputs=[12, 15, 18, 21, 24, 27]\nreference_match=True\nshared_bytes=32\n","stderr":""}} -->
```python
values = list(range(16))
output_indices = list(range(4, 10))
naive_outputs = []
naive_loads = 0

for index in output_indices:
    naive_outputs.append(values[index - 1] + values[index] + values[index + 1])
    naive_loads += 3

tile_input_indices = list(range(output_indices[0] - 1, output_indices[-1] + 2))
tile = [values[index] for index in tile_input_indices]
tiled_outputs = []
for offset in range(1, len(tile) - 1):
    tiled_outputs.append(tile[offset - 1] + tile[offset] + tile[offset + 1])

print(f"output_indices={output_indices}")
print(f"naive_loads={naive_loads}")
print(f"tile_input_indices={tile_input_indices}")
print(f"tiled_loads={len(tile)}")
print(f"modeled_reuse_factor={naive_loads / len(tile):.3f}")
print(f"outputs={tiled_outputs}")
print(f"reference_match={tiled_outputs == naive_outputs}")
print(f"shared_bytes={len(tile) * 4}")
```

In a real kernel, hardware caches may already eliminate some naive loads, while staging adds instructions and barriers. The correct comparison uses measured lower-level traffic and end-to-end time on representative inputs.

### Halo and multidimensional tiles

A stencil tile needs core outputs plus a halo determined by radius. For a one-dimensional radius r and O outputs, the input span has O+2r elements. In two dimensions, a `Tx×Ty` output tile with radius r needs `(Tx+2r)(Ty+2r)` inputs before considering boundary policy. Larger tiles reduce halo fraction but consume more storage and threads.

Assign cooperative loads so every tile element is covered. Some work-items may load multiple elements. Guard global coordinates and write an explicit boundary value or apply the domain's boundary condition—zero, clamp, mirror, periodic, or absent. The condition is scientific/application semantics, not a performance detail.

For matrix multiplication, tiles reuse rows/columns across multiply-accumulate operations. Layout, leading dimension, transposition, numeric accumulation, and synchronization determine correctness. Vendor libraries often outperform custom code and carry broader architecture ownership.

### Shared banks and conflict scope

Scratchpads are commonly divided into banks. Simultaneous lane addresses mapping to the same bank can serialize, except target-defined broadcast/multicast cases. Bank count, width, addressing, and dual-port behavior vary. Padding a row or transposing access can change modular mapping.

Conflict analysis derives bank index from byte address under the current target model. It is empirical/performance reasoning, not a portable semantic guarantee. A bank conflict does not normally cause a data race; missing synchronization or multiple unsafely ordered writers does.

Padding trades conflicts against shared capacity, occupancy, and copy volume. Profile the final target rather than preserving an old “+1 column” rule universally.

### Constant, read-only, texture, and image paths

Constant memory is grid-visible read-only data with application/program lifetime under its API. Specialized caches can broadcast efficiently when an execution group reads the same address; divergent addresses can serialize or fragment service. Capacity and update timing are limited. Kernel parameters may use a constant path automatically.

Texture/read-only/image facilities support cached reads optimized for spatial patterns and may add addressing modes, boundary handling, filtering, or format conversion. Those semantics can be useful for images but are not interchangeable with raw loads. Filtering precision and normalized coordinates belong in the numeric contract.

Never mutate backing storage while cached read-only/texture views observe it unless the API specifies a synchronization/update transition. Rebind or recreate views as required. Constantness is both a correctness promise and an optimization fact.

### Explicit host-device copies

Discrete systems have host DRAM and device DRAM connected by PCIe or another interconnect. Explicit design allocates on each side, copies inputs, runs kernels, and copies outputs. The ownership transitions are visible and can be overlapped with computation using streams/queues and copy engines.

Pageable host memory may require runtime staging through pinned buffers. Pinned memory supports reliable asynchronous DMA/direct access on appropriate APIs, but pinning too much reduces system paging flexibility and can harm the host. Pool and bound it; check allocation failure and operating limits.

Mapped/zero-copy host memory lets a GPU access host-resident pages without an explicit device copy on supported systems. It can avoid one-time copies or suit integrated GPUs, but discrete access latency/bandwidth and repeated traffic may be poor. Coalescing and one-pass access matter. It is not automatically cached or coherent in every mode.

Transfer byte counts include pitch, padding, formats, and selected regions. Two-dimensional allocations often return a pitch larger than logical row bytes. Copy each row with pitch-aware APIs/strides; never multiply logical width as if physical rows were dense unless proven.

### Unified addressing versus managed access

A unified virtual address space gives coordinated pointer identities/ranges and can let APIs infer an allocation's owning device. It does not alone mean the CPU can dereference device storage, the GPU can dereference arbitrary host storage, or caches are coherent.

Managed/unified memory creates allocations accessible from CPU and GPU under platform capabilities. CUDA documents several paradigms: explicit managed allocations, all-system-memory support, software or hardware coherence, and limited support. SYCL USM distinguishes device, host, and shared allocations with context/capability rules. HIP unified memory likewise separates the concept from a specific migratory implementation.

On migration-based systems, first touch and faults establish residency, pages move between processors, and oversubscription may evict pages. Prefetch and advice can express expected location or access, but are hints/policies whose behavior varies. A pointer stays stable while performance changes dramatically.

Concurrent CPU/GPU access requires explicitly supported coherence and atomics at system scope. A host write racing a kernel read is not made safe by shared allocation. Synchronize events or use documented cross-agent atomics/fences. Do not access pages from the host while a limited-support GPU kernel owns them if the API forbids it.

### Migration, thrashing, and oversubscription

Managed memory can simplify irregular or evolving data but makes movement demand-driven. A GPU touching pages one by one can fault/migrate serially. CPU and GPU alternating writes can bounce pages. Multiple GPUs can pull pages or access remote copies according to topology and policy.

Batch work by owner, prefetch before kernels, avoid fine-grained ping-pong, and place read-mostly/shared data with suitable advice only after capability checks. Profile page faults, migration bytes, remote access, and replay. Hints can be ignored or interpreted differently, so correctness cannot depend on placement.

Oversubscribing device memory can enable larger problems but may thrash until forward progress collapses. Establish a working-set budget, chunking/streaming fallback, admission control, memory-pressure monitoring, and allocation-failure recovery. Avoid relying on driver eviction policy for service-level objectives.

### Multiple GPUs and peer access

Each device may have attached memory, with peer links of varying topology, bandwidth, latency, and atomic/coherence capability. Unified addressing may identify peer pointers but access still requires peer enablement and supported topology. Traffic can traverse host bridges or share interconnect bottlenecks.

Choose ownership and partitioning so most accesses are local. Replicate read-only values with versioned update, partition mutable data, and communicate boundaries explicitly. Peer atomics and system scope are capability-specific. A multi-GPU barrier or collective belongs to a communication library/protocol, not ordinary device shared memory.

Topology changes across hosts. Query and record link/NUMA/device relationships; do not assign by ordinal alone. Device loss requires invalidating allocations/events and reconstructing or failing safely.

### Memory consistency and visibility

Scope and location are independent. Global memory is addressable by many work-items, but ordinary conflicting access remains a race. A block barrier can order local/global accesses among block members under its specified fence semantics; it does not synchronize another block. Device- or system-scoped atomics/fences can publish across wider participants when supported.

A release publisher writes data then releases a flag; an acquire consumer observing the flag can then read data, provided both operations use compatible location, order, and scope and the model grants the synchronizes-with edge. A fence alone without an atomic/coordination relation does not cause another agent to wait or identify the version.

Host-device command/event dependencies often provide the simplest phase boundary: copy input, kernel, copy output, host access. Within overlapping queues, make dependencies explicit. Buffer/accessor runtimes can infer some dependencies; USM/pointers commonly require the programmer to state them.

### Allocation, pooling, and lifetime

Device allocation can be expensive and synchronize. Pools/stream-ordered allocators amortize cost and enable asynchronous lifetime, but reuse is safe only after all prior uses are ordered before release and new use. An address recycled for another object must not be referenced by an old kernel/event.

Track size, alignment, device/context, allocation kind, owner, generation, last-use event, and sensitivity. Validate integer size calculations before allocating/copying. Zero-size behavior is API-specific. Clear sensitive buffers according to a verified method before reuse/free where threat models require it; compiler dead-store removal and allocator caching complicate erasure.

Memory leaks persist until context/application reset and can degrade long-running services. Monitor committed/resident/pool/managed usage, fragmentation, faults, and allocation latency. Set quotas per tenant/request.

### Performance evidence

Build a byte ledger: host input/output, device global reads/writes, tile loads, cache/TLB traffic, migrations, peer bytes, and repeated passes. Arithmetic intensity is operations per byte at a specified memory boundary; changing the boundary changes the number. A roofline-style bound helps identify bandwidth versus compute limits but relies on measured sustained ceilings.

Use compiler reports for registers, spills, stack/local memory, and shared bytes. Use profilers/counters for achieved bandwidth, cache hit/miss, sectors/transactions, page faults, migration, bank conflicts, stalls, and occupancy when available. Counter names and meanings are architecture/version-specific.

Benchmark cold/warm, explicit/managed, prefetched/unprefetched, fitting/oversubscribed, aligned/misaligned, representative layouts, concurrency, and device classes. Include allocation, transfers, synchronization, faults, conversions, and cleanup when they occur in the service path. Correctness comparison precedes timing.

### Verification and operational review

Test zero/small/large, tile-minus-one/tile/tile-plus-one, halo corners, pitches, subviews, maximum and overflow-rejected extents, allocation failures, asynchronous delayed use, cancellation, and device loss. Use guard/sanitizer/race tools and sentinel initialization. Force spill-heavy and shared-capacity boundaries in qualification.

For managed memory, test CPU-first/GPU-first touch, prefetch directions, alternating access, oversubscription, concurrent access only where supported, multiple devices, and reduced capability. Verify results and monitor migration/fault behavior without asserting one placement policy universally.

Security/privacy review covers stale pool contents, cross-tenant/device isolation, uninitialized padding, dump/profiler artifacts, host staging copies, peer access, encryption, access control, retention, and erasure. High-stakes numerical pipelines additionally bind calibration, units, formats, numeric policy, and independent domain validation.

## Definitions and Notation

- `A`: programming-model address space.
- `R`: current physical residency/location.
- `O_w`: owner authorized to mutate one representation/version.
- `L`: allocation lifetime interval from creation through ordered last use and release.
- `H`: host-visible memory region.
- `D_j`: memory attached or assigned to device j.
- `S_b`: shared/local scratchpad for work-group b.
- `r`: stencil halo radius.
- `T_x,T_y`: logical tile output extents.
- `U`: useful bytes consumed by the algorithm.
- `X_q`: bytes crossing memory boundary q.
- `I_q=operations/X_q`: arithmetic intensity at boundary q.
- `C_tile`: staging, barrier, capacity, and occupancy cost.
- `E`: completion/dependency event ordering lifetime and visibility.

Address equality does not imply equal R, accessibility, coherence, or ownership. Those are separate state.

## Mechanisms, Invariants, or Proof Structure

### Tile coverage proof

Map every tile element, including halos, to at least one loading work-item; guard global bounds and supply the specified boundary value. Prove each shared location read is initialized. Barrier 1 orders all tile writes before reads; barrier 2 orders all reads before overwrite/reuse. Output ownership covers each logical result exactly once.

### Reuse inequality

Let avoided lower-boundary traffic value be `B_saved` and staging/synchronization/resource cost be `C_tile` in a common measured objective. Tiling helps only if benefit from `B_saved` exceeds `C_tile` and any lost residency/parallelism. Logical load ratio alone is insufficient because caches may already supply reuse.

### Publication proof

Producer writes data, performs a release operation at scope containing consumer, and publishes a version/flag. Consumer acquire-observes that publication before reading data. Command event dependencies can provide an equivalent phase edge. Addressability or a fence without observation is insufficient.

### Managed-residency invariant

Correctness is independent of R and migration order. Every access is legal under current platform capability and ordered against conflicting agents. Advice/prefetch changes performance policy only. Allocation remains alive across faults/migration and a bounded fallback exists for capacity/feature failure.

### Asynchronous lifetime proof

For every copy/kernel/peer operation touching allocation x, its completion event happens-before x is reused, freed, unmapped, or host-mutated incompatibly. Stream order is used only where specified; cross-stream dependencies are explicit.

## Alternatives and Trade-Offs

| Mechanism | Main benefit | Principal limitation |
|---|---|---|
| Registers/private | lowest-cost thread state | finite file, spills, reduced residency |
| Shared/local tile | explicit reuse and collaboration | capacity, barriers, banks, occupancy |
| Transparent caches | no explicit staging | eviction/policy and limited control |
| Constant/read-only path | broadcast/spatial read optimization | size and divergent-access limits |
| Texture/image path | caching, addressing, filtering/formats | specialized semantics and precision |
| Explicit device copy | visible placement and movement | ownership/copy orchestration |
| Pinned/mapped host memory | async/direct device access | host resource and interconnect cost |
| Managed/shared memory | pointer convenience and dynamic placement | faults, migration, capability variance |
| Peer device memory | avoids host staging | topology, scope, bandwidth, failure |
| Pool allocation | amortized allocation and async reuse | lifetime, retention, quota complexity |

Choose by semantic scope and measured data flow. Preserve a bounded explicit/chunked path for platforms or pressure modes where convenience mechanisms fail.

## Failure Modes and Misconceptions

- **“Local means on-chip.”** terminology differs; CUDA local is commonly device-backed private storage.
- **“A source scalar is a register.”** compiler allocation and spills decide.
- **“Shared memory is always faster.”** staging, barriers, banks, and occupancy can lose.
- **“A cache hit is guaranteed after one load.”** capacity, scheduling, and policy intervene.
- **“Global memory is coherent enough for races.”** accessibility is not synchronization.
- **“A fence tells consumers data is ready.”** a coordination/observation edge is also required.
- **“Unified address means shared physical memory.”** it can name separate allocations/locations.
- **“Managed memory means no transfers.”** migration or remote access still moves data.
- **“A stable pointer means stable residence.”** pages can migrate behind it.
- **“First touch is deterministic policy.”** platform and runtime behavior can differ.
- **“Oversubscription just makes execution slower.”** thrashing can destroy progress/SLOs.
- **“Pinned memory is free performance.”** it is a scarce host resource.
- **“Pitch equals logical row bytes.”** alignment padding can differ.
- **“Peer access means peer atomics/coherence.”** query exact topology/capabilities.
- **“Free after launch is safe.”** asynchronous users may remain.
- **“Kernel timing captures memory cost.”** allocation, copies, faults, and sync may be excluded.

## Worked Examples

### Example 1

**Terminology trap.** A CUDA automatic array spills to local memory in device DRAM, while an OpenCL local array is group-shared scratchpad. **Conclusion:** translate memory by scope/lifetime/backing, not name.

### Example 2

**Stencil reuse.** Six radius-one outputs need eighteen logical loads but one eight-element tile. **Conclusion:** reuse potential is 2.25 in the simplified model, not a speedup guarantee.

### Example 3

**Missing second barrier.** Fast threads load the next tile while slow threads still read the current shared slots. Add a barrier before overwrite. **Conclusion:** publication and lifetime barriers have different roles.

### Example 4

**Spill regression.** Unrolling halves loop overhead but raises live registers, spills private arrays, and adds device loads. Compiler reports and counters reveal the loss. **Conclusion:** source instruction reduction can increase memory traffic.

### Example 5

**Pitched image.** Logical width is 1000 bytes but allocated pitch is 1024. Copying 1000·height as one dense range misaligns rows after the first. **Conclusion:** views/copies must carry physical stride.

### Example 6

**Managed ping-pong.** CPU updates one field after every GPU iteration, causing pages to migrate repeatedly. Batch CPU work, separate ownership fields, or use explicit copies/coherent support. **Conclusion:** pointer convenience can hide transfer pathology.

### Example 7

**System-scope race.** Host writes a shared allocation while a kernel reads it without a supported atomic/event edge. Shared accessibility does not define a value. **Conclusion:** cross-agent coherence still needs synchronization.

### Example 8

**Oversubscription.** A 40 GB working set on a 24 GB device repeatedly evicts pages during alternating passes. Chunking 8 GB working tiles restores bounded movement. **Conclusion:** capacity policy is algorithmic and operational.

### Example 9

**Peer topology.** GPU 0 can access GPU 1 through a fast link but GPU 2 traffic traverses a host bridge with no required peer atomic scope. Partition by topology and use a collective library. **Conclusion:** device ordinal is not a communication model.

### Example 10

**Medical image registration.** Device memory design must preserve dimensions, pitch, orientation, voxel units, calibration, masks, boundary conditions, numeric precision, tile halos, shared initialization, copy/migration ordering, failure recovery, privacy, and CPU/reference evidence. Named radiology, medical-physics, registration/numerical, GPU/compiler, hardware/memory, software-safety, security/privacy, operations, quality/regulatory, and independent verification reviewers must approve requirements and evidence; none is claimed here. **Conclusion:** correct tiling and bandwidth do not establish clinical validity or safety.

## Cross-Program Connections

- **Computer architecture:** registers, scratchpads, caches, TLBs, DRAM, interconnects, and NUMA price movement.
- **Programming languages:** address spaces, pointer provenance, atomics, lifetime, and data races define legality.
- **Algorithms:** tiling, blocking, fusion, streaming, compression, and partitioning reshape traffic.
- **Operating systems:** virtual memory, pinning, faults, migration, HMM/ATS, quotas, and device reset affect behavior.
- **Distributed systems:** multi-GPU ownership, versions, topology, collectives, and failure resemble distributed data placement.
- **Numerical computing:** precision, reductions, texture filtering, and boundary conditions define equivalence.
- **Security:** buffer bounds, stale pools, padding, host staging, peer access, and profiling artifacts expose data.
- **Testing:** sentinels, guards, race tools, delayed completion, pressure, faults, and target matrices provide evidence.
- **Performance engineering:** byte ledgers, rooflines, compiler reports, counters, and end-to-end timing locate limits.
- **Operations:** admission, pools, oversubscription, migration, device loss, fallback, and monitoring sustain services.

## References

1. Vasily Volkov and James W. Demmel, “Benchmarking GPUs to Tune Dense Linear Algebra,” SC 2008. <https://doi.org/10.1109/SC.2008.5214359>
2. Xinxin Mei and Xiaowen Chu, “Dissecting GPU Memory Hierarchy Through Microbenchmarking,” *IEEE TPDS* 28(1), 2017. <https://doi.org/10.1109/TPDS.2016.2549523>
3. NVIDIA, *CUDA Programming Guide: GPU Device Memory Spaces*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html#gpu-device-memory-spaces>
4. NVIDIA, *CUDA Programming Guide: Unified and System Memory*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html>
5. NVIDIA, *CUDA C++ Best Practices Guide: Device Memory Spaces*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#device-memory-spaces>
6. AMD, *Introduction to the HIP Programming Model: Memory Model*, current documentation; retrieved 2026-08-29. <https://rocm.docs.amd.com/projects/HIP/en/develop/understand/programming_model.html#memory-model>
7. AMD, *HIP Memory Management*, current documentation; retrieved 2026-08-29. <https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/memory_management.html>
8. Khronos OpenCL Working Group, *OpenCL C Unified Specification: Address Spaces*, current documentation; retrieved 2026-08-29. <https://registry.khronos.org/OpenCL/specs/unified/html/OpenCL_C.html#address-space-qualifiers>
9. Khronos SYCL Working Group, *SYCL 2020 Specification*, revision 12, Sections 3.8 and 4.8, 2026. <https://registry.khronos.org/SYCL/specs/sycl-2020/html/sycl-2020.html>
10. John D. McCalpin, “Memory Bandwidth and Machine Balance in Current High Performance Computers,” *IEEE Computer Society TCCA Newsletter*, December 1995. <https://www.cs.virginia.edu/~mccalpin/papers/bandwidth/bandwidth.html>

## Exercises

### Exercise 1

Classify CUDA register/local/shared/global/constant and OpenCL private/local/global/constant by scope, lifetime, likely backing, and synchronization—not by matching names.

### Exercise 2

Design a two-dimensional radius-one tiled stencil with output tile 16×16. Derive input tile size, shared bytes for f32, cooperative loading, boundary policy, barriers, and ownership.

### Exercise 3

Construct a release/acquire or command-event protocol for a GPU producer and CPU consumer sharing managed/USM memory. State platform capability and lifetime conditions.

### Exercise 4

Compare explicit copies, pinned mapped memory, and managed/shared memory for repeated 2 GB passes on integrated and discrete systems under oversubscription and CPU/GPU alternation.

### Exercise 5

A regulated genomics service uses multiple GPUs and managed memory. Specify placement, consistency, numeric, privacy, capacity/failure, performance, and human-review evidence.

## Answers to the Exercises

### Answer 1

CUDA registers are thread-scoped/lifetime kernel invocation and physically register-file when allocated; CUDA local is thread-private, kernel-lifetime, typically device-memory/cache-backed spill/automatic storage. CUDA shared is block-scoped, block-lifetime, commonly on-chip scratchpad. CUDA global is grid/device accessible, application/allocation lifetime, device DRAM/cache-backed. CUDA constant is grid-visible read-only to kernels, application/program lifetime, device-backed with specialized cache. OpenCL private corresponds semantically to per-work-item state (register or spill), not CUDA shared. OpenCL local corresponds to CUDA shared/LDS: work-group scope/lifetime. OpenCL global corresponds broadly to device global storage, and constant is globally visible read-only. Exact cache/backing is implementation-specific. Synchronization follows communicators: private needs none across threads because sharing is invalid; local/shared uses work-group barriers/atomics; global cross-group/host requires appropriate atomic/fence/event scope; constant updates occur through host/API-defined ordered transitions.

### Answer 2

A 16×16 output tile with radius one needs an 18×18 input tile, 324 f32 values or 1296 bytes before alignment/padding. A 16×16 group has 256 work-items, so assign each a linear local ID and load tile indices `p=local_id, local_id+256` while p<324. Convert p to tile x/y, then global coordinate relative to output origin minus halo. For out-of-domain coordinates write the specified boundary value—such as clamp, mirror, periodic, or zero; this must match the scientific specification. All members reach barrier 1 before stencil reads. Each work-item owns one valid core output and reads its 3×3 neighborhood. If storage is reused for another tile iteration, all members reach barrier 2 before overwrite. Check 18·18·4 arithmetic/capacity, bank padding if measured, group/resource limits, image pitch/strides, partial output blocks, unique output coverage, and exact numeric accumulation order.

### Answer 3

Allocate shared/managed memory in a context/platform that supports access by the selected CPU/GPU and the required system-scope consistency; otherwise use explicit copy. GPU writes data, then either completes a kernel/event whose dependency the host waits on, or performs a release atomic publication at system scope after data writes. The CPU waits for E or acquire-loads the same atomic/version and only then reads data. Ordinary host polling of a non-atomic flag is invalid. CPU must not concurrently mutate data unless a supported reciprocal protocol exists. Allocation remains alive and unmapped until GPU completion and CPU consumption; events/queues remain valid. On limited managed-memory systems, follow exclusivity rules and synchronize before host access. Test delayed execution, repeated generations, wrap-resistant versioning, cancellation/device loss, unsupported features, migration, and race tools. Event phase separation is generally simpler than fine-grained cross-agent atomics.

### Answer 4

Explicit copies make location and ownership clear: pay host-to-device once, run repeated GPU passes locally, copy final output; pinned staging enables asynchronous overlap but consumes scarce host resources. On a discrete system this is usually the bounded baseline for repeated 2 GB reuse. Mapped host memory avoids copies but every repeated GPU pass can traverse the interconnect, so it is mainly attractive for one-pass/small data or favorable coherent links. Managed/shared memory eases pointers and can migrate 2 GB to the GPU after first access or prefetch, performing similarly when it stays resident; alternating CPU/GPU access can ping-pong pages. On integrated coherent systems, host/shared access may avoid physical copies and be preferable, subject to capability/cache policy. Under device oversubscription, explicit chunking bounds residence; managed memory may evict/thrash and needs admission/prefetch/fallback. Benchmark allocation, pin, copy/migration/fault, all passes, sync, and cleanup with placement counters across both systems and access patterns.

### Answer 5

Define immutable reference/genome inputs, batch/sample ownership, coordinate/encoding, exact integer and floating/reduction semantics, and one authoritative generation per mutable result. Query topology, peer access, system atomics, managed-memory paradigm, and capacity; partition mostly local, replicate read-only data with versioning, and explicitly order boundary/collective exchange. Prefetch/place by phase but keep correctness independent of residence. Use events or valid device/system atomics for visibility; bind every allocation/pool entry to last-use completion. Establish per-request memory budgets, bounded chunked explicit-copy fallback, oversubscription admission, allocation/device-loss recovery, idempotent retry, and monitoring of faults/migration/peer bytes/pools. Compare CPU/reference and every device/driver path across sizes, pitches, tails, numeric extremes, concurrency, pressure, failure, and topology. Encrypt and minimize genomic data and staging/profiler artifacts, isolate tenants/devices/pools, audit access, and define retention/erasure. Named genomics, bioinformatics/statistics, numerical, GPU/compiler, memory/platform, distributed/multi-GPU, security/privacy, operations/SRE, quality/regulatory, and independent validation reviewers approve requirements, accuracy, bias, limitations, and residual risk. Memory correctness and speed do not establish biological or clinical validity.
