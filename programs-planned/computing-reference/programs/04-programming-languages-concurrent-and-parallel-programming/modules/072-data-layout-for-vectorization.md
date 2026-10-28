---
module_id: CONPAR-072
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 72
title: Data Layout for Vectorization
status: complete
last_verified: 2026-08-29
---

# Data Layout for Vectorization

## One-Page Review

### Governing question

How should logical data be mapped to bytes so that the fields consumed together are accessible efficiently by vector lanes without breaking semantics, interfaces, ownership, or end-to-end performance?

### Essential definitions

- A **logical schema** names values and relationships; a **physical layout** maps logical indices and fields to addresses.
- An **array of structures (AoS)** stores complete records consecutively: record 0's fields, then record 1's fields.
- A **structure of arrays (SoA)** stores one contiguous array per field.
- An **array of structures of arrays (AoSoA)** groups B records into blocks and stores each field contiguously within a block.
- **stride** is the address difference between logically adjacent elements along one dimension.
- **unit stride** places adjacent requested elements at adjacent element addresses.
- **alignment** constrains an address to a multiple of some byte boundary; **padding** occupies storage not belonging to a logical value.
- A **gather/scatter** uses per-lane addresses rather than one contiguous vector range.
- **spatial locality** is reuse of nearby bytes; **temporal locality** is reuse of the same bytes soon.
- **working set** is the data actively needed during an execution interval.
- **layout conversion** transforms equivalent logical values between physical mappings.
- A **view** describes extents, strides, element type, memory space, and ownership without necessarily owning storage.

### Central model, mechanism, or theorem

Let logical value `(i,f)` map to byte address `addr(i,f)`. For a vector group of records `i=b..b+VF-1` accessing field f, the layout determines the address sequence and therefore the bytes, cache lines, pages, and memory transactions touched. SoA makes `addr(i+1,f)-addr(i,f)=sizeof(f)`; AoS makes it the record stride; AoSoA makes it unit stride within B-record blocks. The optimal mapping minimizes total data movement and transformation cost for the weighted access workload while preserving object, bounds, alignment, alias, update, concurrency, and external-format contracts.

### Critical invariants

Logical-to-physical mapping is injective for live values; extents and strides cannot overflow address arithmetic; padding is initialized or never observed; active lanes remain in bounds; alignment claims are true; layout views carry correct lifetime, memory-space, and mutability metadata; writers cannot observe partially converted state; serialization and ABI formats remain versioned and separate from compute layout; AoSoA block/tail logic handles every element exactly once; concurrency avoids field-level races and false-sharing regressions; conversion cost, extra copies, and memory capacity are included in evaluation; and a scalar/reference representation establishes semantic equality.

### Common failures

Teams declare SoA universally superior, confuse logical row/column orientation with physical contiguity, forget structure padding, assume `alignas` aligns every subview, choose AoSoA block width equal to one current ISA, read padding or inactive tail elements, retain dangling non-owning views, expose compute layout as durable wire format, double memory during conversion without capacity planning, create false sharing between field owners, measure only the kernel while excluding transposition, or claim locality from source syntax without measuring addresses and traffic.

### Compact example

Sixteen records contain a 4-byte x field at offsets `0,16,...,240` in a 16-byte AoS record. An aligned cold scan of only x spans four 64-byte cache lines: 64 useful of 256 transferred bytes in this simplified model. SoA places x at offsets `0,4,...,60`, one line and 64/64 useful bytes. If every record field is immediately consumed, AoS may instead avoid managing several streams. Access workload, not vocabulary, selects the layout.

### Connections

[SIMD Execution and Vector Lanes](071-simd-execution-and-vector-lanes.md) defines lane, mask, gather/scatter, and tail semantics. [Work Partitioning and Granularity](045-work-partitioning-and-granularity.md) explains the costs of blocks and boundaries. The [program roadmap](../ROADMAP.md) continues with compiler auto-vectorization, intrinsics, GPU coalescing, memory hierarchies, and accelerator pipelines.

## Governing Question

Given a logical schema, access-frequency distribution, vector execution model, cache and memory system, update pattern, and interoperability boundary, which physical mapping minimizes end-to-end cost while remaining correct and maintainable?

This is a multi-objective design problem. A layout can make one loop perfectly contiguous while worsening another, increase vector utilization while destroying cache reuse, or accelerate a kernel while imposing a larger conversion cost around it. The chapter therefore treats layout as an explicit mapping with evidence, not as a stylistic choice.

## Why This Matters

Arithmetic units consume registers, but most real kernels begin and end with data movement. If adjacent lanes request adjacent values, hardware can often load or store a vector directly and memory systems can use fetched bytes effectively. If lanes request fields separated by a large record stride, a compiler may need gathers, scalar loads plus inserts, or shuffles after overfetching unwanted fields.

Layout also governs caches, translation lookaside buffers, GPU coalescing, prefetching, compression, transfers between host and device, and sharing between threads. It affects API ergonomics, schema evolution, allocation, checkpointing, and observability. A layout transformation is therefore architectural: it changes ownership and boundaries even when logical values remain identical.

The durable skill is to derive addresses from an access pattern, quantify useful and transferred bytes, and design a migration/validation boundary. Particular cache sizes and instruction costs change; the address reasoning persists.

## Prerequisites and Retrieval

Retrieve:

- lanes, masks, contiguous accesses, gathers, scatters, and scalable widths from [SIMD Execution and Vector Lanes](071-simd-execution-and-vector-lanes.md);
- chunk selection from [Work Partitioning and Granularity](045-work-partitioning-and-granularity.md);
- coherence ownership costs from [False Sharing and Cache-Line Contention](029-false-sharing-and-cache-line-contention.md); and
- immutable conversion snapshots from [Immutable Snapshots and Multi-Version State](067-immutable-snapshots-and-multi-version-state.md).

Retrieval prompt: for one hot loop, write the exact logical fields read and written per iteration, their physical addresses for four adjacent iterations, and the bytes fetched but unused. Repeat for the next most important loop.

## Learning Objectives

After completing this module, a learner can:

1. distinguish schema, representation, layout, view, memory space, and serialization format;
2. derive address formulas for AoS, SoA, AoSoA, row/column-major, and strided arrays;
3. calculate simplified useful-byte, cache-line, page, and transaction utilization;
4. compare contiguous, interleaved, gather/scatter, packed, and pointer-based layouts;
5. choose block sizes without embedding one ISA width into durable semantics;
6. reason about alignment, padding, tails, aliasing, lifetime, and address overflow;
7. analyze layout effects on caches, prefetching, TLBs, GPUs, NUMA, and false sharing;
8. design conversion, view, ABI, persistence, and schema-evolution boundaries;
9. validate semantic equality and benchmark total data movement; and
10. scope independent review for high-stakes data transformations.

## Core Exposition

### Begin with logical values and access vectors

A particle may logically contain position `(x,y,z)`, velocity `(vx,vy,vz)`, mass, identifier, and flags. That schema does not dictate byte order. Write each hot operation as an access vector: integration reads/writes six floating fields; collision broad-phase may read only positions; reporting may consume a whole particle; deletion may update identifiers and ownership metadata.

Associate each operation with frequency, batch size, target, read/write mode, selectivity, and latency importance. A layout decision optimized for a rare report should not dominate a billion integration iterations. Nor should raw frequency alone decide: conversion, random point queries, persistence, or real-time deadlines can impose constraints.

The address mapping is the source of truth. Let f have size `s_f`, record stride R, and offset `o_f`. AoS maps `addr(i,f)=base+iR+o_f`. SoA maps `addr(i,f)=base_f+i·s_f`. AoSoA with block size B maps record i to block `q=floor(i/B)` and lane `r=i mod B`; each block has a field-specific base and `addr(i,f)=block_base(q)+field_offset(f)+r·s_f`, with padding and alignment included.

### AoS: record locality

AoS makes all fields of one record close. It suits code that consumes or mutates complete records, object-oriented interfaces that pass one entity, point lookups, and external row-oriented formats. Allocation and lifetime are simple when a record is one object. Appending or moving one record is also conceptually direct.

When lanes access one field across many records, however, the stride is R. Cache lines contain fields the kernel does not use, and a vectorizer may need a gather or an interleaved load plus shuffles. Structure padding can enlarge R further. If the record holds pointers, following them loses spatial locality entirely even though the pointer fields themselves are consecutive.

AoS is not inherently unvectorizable. Instruction sets can support segment/interleaved loads, compilers can recognize regular strides, and a kernel using several fields may amortize deinterleaving. Measure the actual operation and target rather than rejecting the representation by name.

### SoA: field locality

SoA separates fields so adjacent records' values for one field are contiguous. A loop over x can use unit-stride loads and avoids transferring y, z, identifiers, or flags. Multiple field streams remain independently prefetchable. Columnar databases exploit a related principle: analytical queries can scan and compress selected columns without materializing every attribute of each row.

Costs move elsewhere. One logical record is assembled from several bases, so point operations and row-oriented APIs touch multiple streams. Allocation, resize, insertion, deletion, exception safety, and ownership must update arrays consistently. Separate allocations can increase metadata, TLB footprint, and fragmentation. Mutating one logical record requires a transaction-like invariant across fields when other threads can observe it.

Field arrays can use distinct types and compression, a major benefit when identifiers, flags, and numeric values have different widths. But lossless conversion must preserve correspondence: index i in every field denotes the same logical entity and generation.

### AoSoA: blocked field locality

AoSoA stores B logical records per block, with each field contiguous inside the block. It enables efficient lane loads within a block while keeping the fields for that block nearby. It can reduce the number of independent streams and support block-level ownership or tiling.

B is a tuning and interface parameter, not necessarily the current vector lane count. Choosing B as a common multiple or empirically suitable tile can support several widths; scalable-vector code can process a block in multiple groups. Too-small B increases metadata and boundary handling. Too-large B approaches global SoA and may exceed cache working sets. Padding every block to B wastes space for the final partial block and can complicate persistence.

Define block index and lane calculations with overflow-safe unsigned sizes. Store logical length separately from capacity. Tail values in unused slots are not logical records; operations must predicate them or initialize safe padding according to a documented policy.

### A finite traffic model

The following model compares an aligned, cold, field-only scan of sixteen conceptual records. It counts distinct 64-byte lines containing requested x fields. It does not emulate a cache, prefetcher, TLB, gather instruction, allocator, or measured processor.

<!-- bijux-verify: {"id":"field-scan-layout-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records=16\naos_x_offsets=[0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240]\nsoa_x_offsets=[0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60]\naos_lines=[0, 1, 2, 3]\nsoa_lines=[0]\nuseful_bytes=64\naos_bytes=256\nsoa_bytes=64\naos_utilization=0.250\nsoa_utilization=1.000\nlogical_match=True\n","stderr":""}} -->
```python
records = 16
field_bytes = 4
record_bytes = 16
line_bytes = 64

aos_x_offsets = [index * record_bytes for index in range(records)]
soa_x_offsets = [index * field_bytes for index in range(records)]
aos_lines = sorted({offset // line_bytes for offset in aos_x_offsets})
soa_lines = sorted({offset // line_bytes for offset in soa_x_offsets})
useful_bytes = records * field_bytes
aos_bytes = len(aos_lines) * line_bytes
soa_bytes = len(soa_lines) * line_bytes

logical_aos = [100 + index for index in range(records)]
logical_soa = list(logical_aos)
print(f"records={records}")
print(f"aos_x_offsets={aos_x_offsets}")
print(f"soa_x_offsets={soa_x_offsets}")
print(f"aos_lines={aos_lines}")
print(f"soa_lines={soa_lines}")
print(f"useful_bytes={useful_bytes}")
print(f"aos_bytes={aos_bytes}")
print(f"soa_bytes={soa_bytes}")
print(f"aos_utilization={useful_bytes / aos_bytes:.3f}")
print(f"soa_utilization={useful_bytes / soa_bytes:.3f}")
print(f"logical_match={logical_aos == logical_soa}")
```

The result is deliberately conditional on aligned bases, one cold pass, line-granular transfer, no neighboring reuse, and the chosen sizes. In a real cache, prior state, prefetch, eviction, write allocation, coherence, and adjacent operations change traffic. The model is useful because its premises are visible.

### Multidimensional layout and stride

For a two-dimensional logical array with extents M×N, row-major mapping places the last index at unit stride: `offset(i,j)=i·N+j`. Column-major places the first at unit stride: `offset(i,j)=j·M+i`. Neither is universally superior. The loop's innermost varying index should commonly match unit stride, or the loop/tile should be reorganized.

General views carry an extent and stride for each dimension. A submatrix can be non-contiguous even when its parent is contiguous. Leading dimensions may include padding. Libraries must pass actual strides, not recompute them from logical extents. An API that accepts only a pointer and dimensions silently assumes a mapping it cannot verify.

Tiling maps nearby indices into blocks sized for reuse in cache, shared memory, or registers. Matrix multiplication depends more on blocked reuse than on a simplistic row-versus-column choice. Space-filling or swizzled layouts can improve locality for particular traversal neighborhoods but complicate indexing, interoperability, and debugging.

### Alignment, padding, and object rules

Alignment can allow or improve vector loads, reduce boundary crossings, and meet device-transfer requirements. Allocate with a facility that guarantees the desired alignment and propagate it through offsets: an aligned base plus a non-multiple slice offset is no longer equivalently aligned. Verify runtime views before making compiler alignment promises.

Compilers insert padding inside and after structures to satisfy member and array-element alignment. Do not serialize raw structures as stable schemas: padding content may be indeterminate, layout can vary by ABI/compiler/options, endianness differs, and pointers are process-local. Define field-wise encoding with versions and explicit numeric representation.

Padding for vector tails is a different mechanism. It may permit full-width access only when storage, object lifetime, initialization, and access rules cover the padded region. Padding values must be neutral for reductions if computed, and stores must not expose them. Predication is still needed when padding is not owned.

### Interleaving, gathers, and transposition

Regular AoS fields form interleaved streams. Some ISAs provide segment or deinterleaving loads; a compiler may load a contiguous record group and shuffle fields into vectors. This transfers all loaded fields and consumes shuffle bandwidth, but can be efficient when several fields are used.

Gather/scatter handles arbitrary or regular-stride addresses without changing global layout. It avoids conversion and supports sparse selection. Its cost depends on address generation, lane masks, cache lines/pages touched, target instructions, and data distribution. A gather whose addresses land in one or two lines may be reasonable; a pointer-chasing gather across pages can dominate arithmetic.

On-the-fly transposition converts a tile into a register- or scratchpad-friendly arrangement, computes several operations, then possibly converts back. Amortize conversion over enough reuse. Fusion can eliminate intermediate conversions; conversely, incompatible producer/consumer layouts can create repeated transpose ping-pong.

### Packed, compressed, and sparse representations

Bit packing reduces bandwidth but adds extraction, masking, and cross-word boundary work. Narrow integers increase lane count, though widening conversions and overflow semantics matter. Dictionary, run-length, delta, and bit-sliced encodings may permit operations directly on compressed columns or may require decompression. Model total bytes and instructions.

Sparse formats encode only present values plus indices. Compressed sparse row favors row traversal; compressed sparse column favors column traversal. ELLPACK-like fixed row widths can improve regular lanes but waste padding for uneven rows. Hybrid formats classify rows. No single sparse layout dominates all degree distributions and operations.

Pointer-rich trees and graphs may benefit from arena allocation, index-based edges, hot/cold field splitting, clustering related nodes, or frontier compaction. These transformations change pointer stability and mutation cost. Generation-tagged indices can prevent stale references; compaction needs synchronization and snapshot semantics.

### Concurrency, false sharing, and NUMA

SoA can improve read lanes while creating a concurrency problem if different threads update adjacent field elements on the same cache line. Conversely, splitting frequently written fields can prevent unrelated cold fields from sharing traffic. Partition ownership, pad or align per-thread blocks where justified, and measure coherence events. Padding every element to a line usually destroys capacity and scan locality.

AoSoA blocks can be ownership units, but block boundaries must align with scheduling so two writers do not share a block unintentionally. Readers must see a consistent logical record when fields reside in separate arrays. Use immutability, versioning, locks, or publication protocols appropriate to the memory model; layout does not create atomic multi-field updates.

NUMA placement follows first touch or explicit policy on many systems. A perfect unit-stride layout in remote memory can lose to a less elegant local layout. Initialize and partition on intended nodes, record placement, and include cross-socket workload. On heterogeneous systems, memory-space ownership and transfer paths belong in the view type or runtime metadata.

### GPU coalescing and bank layout

GPU lanes issue memory requests as groups. Coalescing combines addresses into memory transactions; adjacent threads accessing adjacent words generally improve useful-byte ratio. An AoS field stride can turn one logical instruction into many segments, while SoA often produces contiguous requests. Exact transaction rules vary by architecture and must come from current target documentation.

Shared-memory banks introduce another mapping: regular strides can make many lanes target the same bank and serialize service. Padding a tile dimension can change the modular mapping and remove conflicts, but target bank count and word rules matter. Global coalescing and shared-bank freedom are separate properties; a transpose often stages through one layout to obtain both.

Host/device transfer changes the objective. If a CPU producer needs AoS and a GPU needs SoA, options include maintaining dual authoritative/cached representations, converting at transfer, changing the producer, or writing a gather-tolerant kernel. Version and invalidate replicas explicitly. Count PCIe/interconnect bytes, pinning, migration, conversion, and synchronization, not kernel time alone.

### Views, ownership, and layout polymorphism

A robust view describes base, logical extents, physical strides, element type, alignment if guaranteed, memory space, access mode, and lifetime/owner relationship. Index arithmetic validates multiplication/addition overflow before address formation. Empty dimensions and zero-length allocations have specified behavior.

Layout-polymorphic algorithms accept views and specialize or dispatch for supported mappings. They can choose a fast contiguous path and a correct general-stride path. Reject unsupported layouts explicitly instead of treating their bytes as a default mapping. Type systems can encode rank, extents, memory space, or layout, but runtime views remain necessary for dynamic slices and foreign buffers.

Ownership matters more than pointer shape. A non-owning SoA view into a converted cache must not outlive or race with cache invalidation. Copy-on-write and versioned snapshots can provide stable read views. Mutable aliases across AoS and SoA replicas require one source of truth and a synchronization protocol.

### Conversion economics and migration

Let baseline total time be repeated kernel time plus existing movement. A transformed system adds conversion, allocation, validation, cache management, and perhaps extra copies, while reducing selected kernel/memory costs. Break-even after K uses occurs only if cumulative per-use saving exceeds one-time and recurring layout overhead. Use distributions, not one average, when batch sizes and reuse vary.

Migration can temporarily require both layouts, raising peak memory. Plan capacity and failure atomicity. Convert into a new version, validate counts and digests or logical equality, then publish it; never expose a half-converted structure. Rollback needs the prior authoritative representation or a reversible conversion.

Keep durable wire/storage schema independent. On load, validate untrusted lengths and offsets before allocating or multiplying; decode to a safe logical/compute representation. On save, encode fields explicitly. Schema evolution then changes through named converters rather than accidental compiler layout.

### Evidence-driven selection

Trace or instrument field access, but protect sensitive data and avoid instrumentation bias. Use compiler remarks and assembly to determine whether accesses become unit-stride, interleaved, gathered, or scalar. Counters can estimate cache/TLB misses, bandwidth, transactions, and coherence. A roofline or arithmetic-intensity model can show when byte reduction is promising.

Benchmark complete pipelines for representative sizes, selectivities, distributions, reuse counts, producers/consumers, thread placements, and targets. Report logical bytes, estimated/observed transferred bytes, conversions, peak memory, latency percentiles, throughput, energy if relevant, and semantic comparison. Randomize or control alignment and cache state. Retain datasets and provenance where policy permits.

Correctness tests enumerate extents and strides, including empty, one, block-minus-one, block, block-plus-one, large, overflow-adjacent, misaligned, subview, transposed, and final partial block. Round-trip conversions, compare logical values, exercise concurrent publication, force every layout path, use sanitizers/guard pages, and fuzz untrusted metadata.

## Definitions and Notation

- `i`: logical record or element index.
- `f`: logical field.
- `s_f`: byte size of field f's stored representation.
- `o_f`: field f's byte offset within a record or block.
- `R`: AoS record stride in bytes, including padding.
- `B`: AoSoA records per block.
- `q=floor(i/B)`: AoSoA block index.
- `r=i mod B`: lane position within an AoSoA block.
- `E_k`: logical extent of dimension k.
- `S_k`: physical stride, in elements or bytes as explicitly stated, of dimension k.
- `CL`: cache-line size in a simplified traffic model.
- `U`: useful bytes requested by the operation.
- `X`: bytes transferred at the modeled memory boundary.
- `η=U/X`: useful-byte utilization for that boundary.
- `C`: conversion/allocation/publication cost.
- `Δ`: per-use saving after transformation.

`η` is boundary- and model-specific. It does not by itself predict runtime because latency, concurrency, reuse, prefetching, instructions, and capacity also matter.

## Mechanisms, Invariants, or Proof Structure

### Layout injectivity

For all distinct live logical cells `(i,f)≠(j,g)`, their physical byte ranges must not overlap unless intentional aliasing is part of the representation. Prove size/offset/stride arithmetic without overflow and allocated bounds cover every range. Separate logical tail length from padded capacity.

### AoSoA coverage proof

Euclidean division assigns every nonnegative i unique `(q,r)` with `i=qB+r` and `0≤r<B`. If blocks map uniquely and field offsets/ranges do not overlap, every logical field has one address. The proof requires B>0, bounded arithmetic, sufficient final-block allocation, and masks that exclude `i≥n`.

### Round-trip refinement

Let `decode_L` map physical layout L to logical values and `encode_M` create layout M. A correct conversion satisfies `decode_M(encode_M(decode_L(x)))=decode_L(x)` for every accepted x, including exceptional numeric representations and metadata. This proves logical preservation, not concurrent publication or performance.

### Break-even relation

For one conversion cost C and K uses saving Δ each, transformation improves modeled total time only when `K·Δ>C`; with recurring conversion `C_k`, require `ΣΔ_k>ΣC_k`. Measure rather than assume C and Δ, and include peak-memory or latency constraints that a scalar inequality cannot capture.

### Publication invariant

Readers observe either the complete old version or complete new version, never mixed field generations. Establish this with exclusive ownership, immutable snapshot plus atomic root publication, or another memory-model-correct protocol. Matching indices across arrays is insufficient without generation consistency.

## Alternatives and Trade-Offs

| Layout | Main benefit | Principal limitation |
|---|---|---|
| AoS | complete-record locality and simple interfaces | field scans stride and overfetch |
| SoA | unit-stride field scans and independent encoding | multi-array ownership and record assembly |
| AoSoA | bounded field contiguity and block locality | tuning, block tails, and metadata |
| Row-major | contiguous last dimension | column traversal strides |
| Column-major | contiguous first dimension | row traversal strides |
| General stride/view | flexible slicing and interoperability | fast paths need runtime facts |
| Gather/scatter | avoids global conversion | irregular address and cache/TLB cost |
| Packed/compressed | lowers capacity and bandwidth | decode, update, and boundary complexity |
| Sparse formats | omit structural zeros | indices, imbalance, operation-specific traversal |
| Dual representations | target-specific fast paths | consistency, memory, conversion, invalidation |

Prefer the simplest layout meeting measured dominant accesses and interfaces. Introduce blocked or replicated forms only with ownership, conversion, and invalidation designs. Preserve a general correct path when specialized assumptions may not hold.

## Failure Modes and Misconceptions

- **“SoA is always faster.”** full-record operations, small sets, or conversion can favor AoS.
- **“AoS cannot vectorize.”** interleaved loads, shuffles, or gathers may be profitable.
- **“AoSoA block size equals SIMD width.”** widths vary and scalable targets reject that assumption.
- **“Row-major means rows are always fast.”** loop order, slices, padding, and cache state matter.
- **“A contiguous virtual range is one transaction.”** alignment and target segment rules decide traffic.
- **“Alignment propagates to every slice.”** offsets can destroy the guarantee.
- **“Padding is safe data.”** it may be outside logical lifetime or uninitialized.
- **“Structure size is the sum of fields.”** internal/tail padding can enlarge stride.
- **“Gather fixes bad locality.”** it expresses addresses; it cannot remove cache/page traffic.
- **“Packing only saves memory.”** it changes decode, update, atomic, and vector behavior.
- **“Separate fields are independently mutable.”** they may form one logical consistency unit.
- **“A view owns its buffer.”** many views are non-owning and can dangle.
- **“Raw structs are a stable file format.”** ABI, padding, endianness, and pointers disagree.
- **“Kernel speedup is application speedup.”** conversion, transfer, and synchronization count.
- **“First-touch happens automatically where desired.”** initialization placement must be designed.
- **“One cache model proves traffic.”** caches, prefetchers, write policies, and workloads vary.

## Worked Examples

### Example 1

**AoS address derivation.** A 24-byte record has x at offset 8. Four adjacent x values occur at offsets 8, 32, 56, and 80, a 24-byte stride. **Conclusion:** logical adjacency does not imply physical contiguity.

### Example 2

**SoA point lookup.** Reading all eight fields of record 913 touches eight field bases and may reach several lines/pages, while AoS may fetch them together. **Conclusion:** field scans and record lookups optimize different dimensions.

### Example 3

**AoSoA tail.** With B=8 and n=18, blocks 0 and 1 are full; block 2 has active lanes 0 and 1. Capacity may include six padding slots, but only two are logical records. **Conclusion:** capacity and logical length must remain distinct.

### Example 4

**Subview alignment.** A 64-byte-aligned float base sliced from index 1 begins four bytes later and is not 64-byte aligned. **Conclusion:** alignment belongs to the effective address, not the allocation name.

### Example 5

**Loop interchange.** A row-major M-by-N array traversed with j innermost has unit stride; i innermost jumps N elements. Interchanging legal independent loops restores contiguous order. **Conclusion:** layout and traversal are co-designed.

### Example 6

**Conversion break-even.** AoS-to-SoA conversion costs 8 ms and each of four kernels saves 3 ms. Total saving is 12 ms, net 4 ms; with only two uses, it loses 2 ms. **Conclusion:** reuse count belongs in the decision.

### Example 7

**False sharing.** Two threads update disjoint adjacent four-byte counters in one field array but repeatedly invalidate their shared line. Assign line-sized thread blocks or aggregate locally. **Conclusion:** disjoint logical elements can share coherence ownership.

### Example 8

**Packed flags.** One bit per record reduces 64 flags from 64 bytes to 8, but concurrent updates to different bits may contend on the same word and require atomic masks. **Conclusion:** capacity compression changes update semantics.

### Example 9

**CPU/GPU disagreement.** A CPU point-query stage prefers AoS while a GPU field kernel prefers SoA. Maintaining two caches helps only if generation-based invalidation and transfer/conversion savings beat their cost. **Conclusion:** heterogeneous layout is a consistency architecture.

### Example 10

**Autonomous-vehicle perception tensor.** Reordering camera tensors between NHWC and NCHW must preserve batch, spatial, channel, pixel format, calibration, quantization scale/zero point, timestamps, validity masks, and bounds. Validate round trips, adversarial extents/strides, reference kernels, numeric tolerance, every accelerator path, conversion latency, memory peak, and stale-version rejection. Named perception, sensor/calibration, numerical, ML-model, compiler/SIMD/GPU, platform, real-time, software-safety, security/privacy, quality/regulatory, and independent verification reviewers must approve requirements and evidence; none is claimed here. **Conclusion:** a faster tensor mapping does not establish perception or vehicle safety.

## Cross-Program Connections

- **Data structures:** clustering, arenas, indices, compression, and hot/cold splitting alter locality and mutation.
- **Databases:** row and column stores reflect point/update versus analytical scan workloads.
- **Compilers:** dependence, interleaving, gather cost, and layout metadata govern vector plans.
- **Computer architecture:** lines, pages, TLBs, prefetchers, banks, NUMA, and memory transactions price addresses.
- **GPU programming:** coalescing and shared-bank mappings couple thread identity to layout.
- **Numerical computing:** matrix order, leading dimensions, tensor formats, and sparse schemes define kernels.
- **Distributed systems:** wire schemas and partitions should remain independent of process-local compute layout.
- **Concurrency:** field splitting changes atomicity, ownership, false sharing, and publication.
- **Security:** untrusted extents/strides, padding disclosure, stale views, and side-channel access patterns require review.
- **Software architecture:** views, conversions, versioning, provenance, and rollback make layout changes governable.

## References

1. Trishul M. Chilimbi, Mark D. Hill, and James R. Larus, “Cache-Conscious Structure Layout,” PLDI 1999. <https://doi.org/10.1145/301618.301633>
2. John D. McCalpin, “Memory Bandwidth and Machine Balance in Current High Performance Computers,” *IEEE Computer Society TCCA Newsletter*, December 1995. <https://www.cs.virginia.edu/~mccalpin/papers/bandwidth/bandwidth.html>
3. Daniel J. Abadi, Samuel R. Madden, and Nabil Hachem, “Column-Stores vs. Row-Stores: How Different Are They Really?” SIGMOD 2008. <https://doi.org/10.1145/1376616.1376712>
4. Intel, *Intel 64 and IA-32 Architectures Optimization Reference Manual*, version 050; retrieved 2026-08-29. <https://www.intel.com/content/www/us/en/developer/articles/technical/intel64-and-ia32-architectures-optimization.html>
5. Intel, *ISPC Performance Guide*, current documentation; retrieved 2026-08-29. <https://ispc.github.io/perfguide.html>
6. LLVM Project, *Auto-Vectorization in LLVM*, current documentation; retrieved 2026-08-29. <https://llvm.org/docs/Vectorizers.html>
7. RISC-V International, *“V” Standard Extension for Vector Operations, Version 1.0*, ratified specifications library; retrieved 2026-08-29. <https://docs.riscv.org/reference/isa/unpriv/v-st-ext>
8. NVIDIA, *CUDA Programming Guide: Memory Performance*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html#memory-performance>
9. Kokkos Project, *Programming Guide: View, Layouts, Strides, and Dimensions*, current documentation; retrieved 2026-08-29. <https://kokkos.org/kokkos-core-wiki/ProgrammingGuide/View.html>
10. ISO/IEC, *ISO/IEC 9899:2024 — Programming Languages — C*, 2024. <https://www.iso.org/standard/82075.html>

## Exercises

### Exercise 1

For a 32-byte AoS record with 8-byte fields x and y at offsets 0 and 8, derive addresses and simplified 64-byte-line utilization when scanning x for eight aligned records. Compare aligned SoA.

### Exercise 2

Define address formulas and tail handling for AoSoA with B=12, fields `{x:f32,id:u64,active:u8}`, and n=29. State padding, alignment, and overflow obligations.

### Exercise 3

Design a safe general-stride two-dimensional view and a contiguous fast path. Cover negative/zero strides if supported, empty dimensions, subviews, alignment, lifetime, and untrusted metadata.

### Exercise 4

A pipeline consumes AoS network messages, performs five field-wise vector kernels, then emits AoS. Build a conversion break-even model and validation/benchmark plan.

### Exercise 5

A medical-imaging service supports CPU, GPU, and archival representations. Specify layout, versioning, conversion, numeric, concurrency, privacy, operational, and human-review requirements without claiming clinical validity from performance.

## Answers to the Exercises

### Answer 1

AoS x addresses relative to an aligned base are 0, 32, 64, 96, 128, 160, 192, and 224. They touch four 64-byte lines. Useful x bytes are `8·8=64`; simplified transferred bytes are `4·64=256`, so `η=0.25`. Aligned SoA x addresses are 0, 8, ..., 56, touching one line, so modeled `η=64/64=1`. This assumes a cold field-only read, line-granular transfer, no reuse of y/other fields, no prefetch nuance, and aligned bases. If later work consumes the rest of each AoS line, its apparent overfetch may become useful.

### Answer 2

For i, set `q=floor(i/12)` and `r=i mod 12`. Within each block place 12 x values, then alignment padding for 12 64-bit ids, then 12 active bytes, plus tail padding making the next block meet its required alignment. Compute explicit `x_offset+r·4`, `id_offset+r·8`, and `active_offset+r`; do not assume the offsets are 48 and 144 without applying alignment policy. For n=29, blocks 0 and 1 are full and block 2 has active r=0..4. Store n separately; predicate remaining seven slots. Require B>0, checked multiplication/addition for block size and `q·block_size`, allocated capacity for three blocks, truthful base/field alignment, initialized padding only if any full access may observe it, no serialization of padding, and unique nonoverlapping field ranges.

### Answer 3

The view carries owner/lifetime token, base, element type/size/alignment, memory space, two extents, two signed or unsigned byte strides, mutability, and accessible allocation range. Validate rank, extent products, endpoint address calculations, multiplication/addition overflow, and every reachable address before use. Define empty extents without dereference. If negative strides are supported, base must identify logical `(0,0)` and min/max reachable offsets both remain in allocation; reject them otherwise. Define zero stride as broadcast read-only or reject mutable aliases. A contiguous fast path requires the expected unit stride and dense outer stride plus alignment/alias predicates; otherwise use a checked general path. Subviews derive new bounds/alignment, retain ownership, and cannot outlive the allocation. Fuzz hostile metadata and test zero/one dimensions, padding, transpose, reversal, large extents, and guard pages.

### Answer 4

Let conversion pair cost be `C_in+C_out`, per-batch allocation/publication cost A, and per-kernel saving `Δ_j` relative to direct AoS/gather execution. Convert when `Σ_{j=1..5}Δ_j > C_in+C_out+A`, subject to latency and peak-memory constraints. Include message decoding that may already copy, potential fusion, batch-size distribution, selectivity, cache state, and whether outputs need every field. Validate field-wise round trip including exceptional bits and metadata, tails, alignment, malformed lengths, cancellation, and atomic publication. Benchmark direct AoS, one conversion around all kernels, fused conversion/kernel, and persistent dual cache across realistic reuse; measure total latency, throughput, bytes, conversions, memory peak, and uncertainty on each host class. Inspect generated accesses and retain scalar logical comparison.

### Answer 5

Define one versioned logical image schema: dimensions, spacing/orientation, modality, units, pixel type, endianness, missing/sentinel/NaN rules, calibration, and provenance. Decode archival data field-wise; never memory-map raw process structures as trusted objects. Use CPU and GPU views with explicit extents, strides, memory space, owner generation, and numeric contract. Convert into immutable new generations, validate logical equality or specified numeric tolerance, then atomically publish; cancel safely and reject stale views. Test empty/min/max/adversarial dimensions, overflow, subviews, padding, guard pages, all CPU/GPU paths, transfers, failure recovery, and round trips. Measure end-to-end conversion, transfer, kernel, memory peak, placement, and latency distributions. Encrypt and minimize patient data, restrict/audit access, define retention/deletion, and use de-identified performance sets. Named radiology, medical physics, clinical workflow, numerical/imaging, SIMD/GPU/compiler, platform, software-safety, security/privacy, data-governance, operations, quality/regulatory, and independent validation reviewers approve requirements and residual risk. Layout equality and speed are not diagnostic validity, clinical approval, or deployment safety.
