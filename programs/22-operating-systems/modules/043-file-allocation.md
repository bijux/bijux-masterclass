---
module_id: OS-043
program: Operating Systems
level: 1
module_number: 43
title: File Allocation
status: complete
last_verified: 2026-09-04
---

# File Allocation

## One-Page Review

### Governing question

How should a filesystem map changing logical file ranges to finite storage while preserving contents, isolation, accounting, locality, concurrency, and crash-recovery invariants?

### Essential definitions

- A **logical range** is an interval of byte offsets in a file.
- An **allocation unit** is the smallest storage region managed by an allocator; it can differ from an I/O or filesystem block.
- A **block map** associates logical blocks with physical storage one entry at a time or through indirect indexes.
- An **extent** maps a contiguous logical range to a contiguous physical range plus state.
- A **hole** is an unallocated logical range whose filesystem reads return zeros.
- An **unwritten extent** reserves physical space but reads as zeros until safely converted after data write.
- **Delayed allocation** reserves capacity while postponing exact physical placement until writeback.
- **Copy-on-write** allocates private storage before modifying a range shared by multiple logical owners.

### Central model, mechanism, or theorem

Let `M_f` map each logical range of file `f` to `hole`, `delalloc`, `unwritten(p)`, `written(p)`, `inline`, or `shared(p,owners)`. Allocation is a state transition coordinated with free-space state `A`, reference counts `R`, quota reservations `Q`, file size `S_f`, cached dirty data, and recovery metadata.

Correctness requires interval coverage without incompatible overlap, exclusive ownership for ordinary written blocks, positive validated reference counts for shared blocks, zero-filled reads from holes and unwritten extents, sufficient reservation before deferred writes, and atomic recoverable updates across mapping and allocator metadata. Placement policy changes performance; it must not change file contents.

### Critical invariants

- Every logical byte has one compatible mapping state, and mapping-tree intervals are ordered, bounded, and non-overlapping.
- Every allocated physical unit is either free or owned by the exact recorded mappings and metadata, never both.
- Newly exposed bytes read as zero until caller data has been safely written.
- Delayed allocation carries a reservation or an explicitly documented failure contract.
- Shared extents are never modified in place until copy-on-write establishes private ownership.
- Truncate, hole punch, collapse, insertion, and clone update size, mappings, reference counts, quota, cache, and timestamps coherently.
- Recovery yields an old or new consistent mapping/allocation state without cross-file disclosure, double allocation, or permanent leaks.

### Common failures

Common mistakes are equating logical size with allocation, exposing stale device contents through unwritten space, reserving memory but not disk capacity, treating reported extents as immutable addresses, modifying reflink-shared blocks in place, freeing blocks before invalidating cached data or references, assuming preallocation makes writes infallible, ignoring partial-block zeroing, and repairing allocation metadata without checking file mappings and reference counts.

### Compact example

A 24-block logical file contains two written extents separated by a hole. Four newly dirtied blocks carry delayed allocation. At writeback, the allocator reserves a contiguous run, writes data, and converts it to written state only after initialization; the hole remains logically zero. If the transaction fails, reservations and partial mappings unwind without publishing stale bytes.

### Connections

[OS-037](037-copy-on-write.md), [OS-039](039-shared-pages-and-page-cache.md), and [OS-042](042-inodes-and-metadata.md) supply sharing, caching, and inode state. [OS-044](../ROADMAP.md) develops the complementary free-space allocator, while [OS-047](../ROADMAP.md) covers crash consistency.

## Governing Question

Applications see a flat byte sequence, but filesystems store data in blocks, extents, device zones, objects, or inline records. The mapping changes under writes, truncation, cloning, compression, defragmentation, and recovery.

The governing question is how to maintain that mapping without losing bytes, leaking old data, double-allocating space, or making performance policy part of correctness. The answer separates logical semantics, physical placement, reservation, initialization, ownership, publication, and persistence.

## Why This Matters

Allocation determines whether large files scale, sequential I/O remains contiguous, sparse data stays sparse, and storage exhaustion is reported predictably. It also links the page cache to free-space accounting and persistent metadata.

Allocation errors are security errors. Publishing an uninitialized block can reveal another file's contents. Incorrect shared-extent reference counts can corrupt multiple files. A crash between changing a file map and changing free-space state can create either a leak or double ownership.

Allocation interfaces also affect application design. Databases preallocate, virtual-machine images use holes and zero ranges, backup tools discover data ranges, and deduplicating systems share blocks. Each operation has filesystem-specific support and granularity.

## Prerequisites and Retrieval

Review [OS-024](024-atomic-operations.md), [OS-037](037-copy-on-write.md), [OS-039](039-shared-pages-and-page-cache.md), [OS-041](041-files-directories-and-namespaces.md), and [OS-042](042-inodes-and-metadata.md).

Retrieve these distinctions:

- file offsets are logical addresses; device offsets are physical placement;
- logical size, mapped ranges, allocated space, reserved capacity, and quota charge differ;
- holes and unwritten extents both read as zeros but have different physical ownership;
- dirty page-cache data can exist before a stable physical mapping is selected;
- extent contiguity reduces mapping metadata but does not guarantee uninterrupted device service;
- preallocation reserves space, while synchronization addresses persistence;
- reflink shares storage, whereas an ordinary copy creates independent contents;
- allocator metadata and file mappings form one cross-structure ownership invariant.

## Learning Objectives

After this module, you should be able to:

1. compare contiguous, linked, indexed-block, multilevel-indirect, and extent-based mappings;
2. model holes, delayed allocation, unwritten extents, written extents, inline data, and shared mappings;
3. trace buffered write, direct write, preallocation, hole punch, truncation, insertion, collapse, clone, and copy-on-write;
4. specify locality, fragmentation, reservation, quota, and out-of-space policies;
5. reason about cache coherence, concurrent mapping change, and extent-query limitations;
6. construct atomicity and crash-recovery obligations across mappings, allocator state, and reference counts;
7. test allocation behavior with adversarial ranges, failures, sharing, corruption, and evidence.

## Core Exposition

### Logical address space

A regular file presents offsets from zero through its logical size. Reads inside holes return zero; reads at or beyond end follow end-of-file semantics. The application need not know where bytes reside physically.

Mapping operations use half-open intervals `[start,end)`. Checked arithmetic prevents `offset+length` overflow and distinguishes an empty request from a range extending beyond maximum file size.

### Allocation units

Devices expose sectors and transfer constraints; filesystems group storage into blocks, clusters, segments, or objects. The allocation unit can exceed the smallest write and create read-modify-write obligations for partial updates.

Suballocation and tail packing reduce internal fragmentation but add shared-container metadata. Large units reduce map size and improve sequential I/O while wasting more space for small or fragmented files.

### Contiguous allocation

The simplest map stores a physical start and length. Translation is constant time and sequential placement is excellent, but growth fails when adjacent space is unavailable.

Moving a growing file restores contiguity at high write and recovery cost. Pure contiguous allocation is therefore best for immutable or size-known objects, not arbitrary mutable files.

### Linked allocation

Linked allocation stores a pointer from each unit to the next. Growth can use any free unit, but random access follows a chain and corruption can lose the suffix or create cycles.

Centralized variants keep links in a table for faster traversal and simpler blocks. The table becomes large and important metadata that still needs validation and recovery.

### Indexed blocks

An indexed scheme stores block addresses in direct and indirect blocks. Single, double, and triple indirection expand maximum size while keeping small files cheap.

Random lookup follows a bounded tree, but a long contiguous run still consumes many pointer entries. Every index block is allocation metadata requiring checksums, ownership checks, and ordered updates.

### Extents

An extent describes logical start, physical start, length, and state. One record can represent thousands of contiguous blocks, reducing metadata and lookup work.

Extent trees support large and fragmented files. Split, merge, insert, and delete operations preserve sorted non-overlap, bounded length, tree balance, and transaction limits.

### Inline data

Very small contents can live inside the inode or another metadata record. This saves a separate data allocation and I/O, but consumes metadata space and complicates growth.

When content outgrows inline capacity, conversion allocates blocks, copies bytes, and publishes the external mapping atomically. Failure leaves the valid inline form or the valid external form.

### Sparse files and holes

Seeking beyond end and writing can create an unmapped gap. Filesystem reads synthesize zeros without allocating storage for every logical byte.

Tools must preserve hole semantics deliberately. Reading and rewriting all zeros can expand allocation; assuming every zero range is a hole can discard deliberately stored zeros or other encoding state.

### Partial-block boundaries

Hole punch and truncation can begin or end inside an allocation unit. Whole interior units may be freed, while boundary fragments usually require zeroing to preserve the promise that removed bytes read as zero.

The implementation orders cache invalidation, boundary writes, mapping changes, and block release so stale cached bytes cannot reappear.

### Unwritten extents

Preallocation can reserve physical ranges without initializing every byte immediately. Marking them unwritten makes filesystem reads return zeros until completed writes convert covered ranges to written.

Conversion may split an extent around the written subrange. Publication occurs after data initialization so a crash or racing read cannot expose prior device contents.

### Delayed allocation

Buffered writes can dirty cache pages while deferring exact block choice. Seeing a larger dirty range at writeback lets the allocator choose longer extents and improve locality.

Delay shifts failure timing. The filesystem reserves capacity and quota, or documents that a later writeback can fail despite an earlier successful write. Memory pressure, synchronization, and background thresholds force conversion.

### Reservation accounting

A reservation promises enough allocatable capacity for deferred work without yet naming blocks. Global free count, per-user quota, metadata overhead, copy-on-write worst case, and emergency reserves all affect admission.

Reservations are released on cancellation and consumed exactly once on allocation. Overcommit improves utilization but weakens guarantees and requires explicit failure propagation.

### Placement goals

Allocators try to keep related logical blocks physically near one another, place data near metadata where useful, spread independent workloads, and leave large free runs for future growth.

The correct policy depends on media and workload. Rotational seek cost, SSD parallelism and erase behavior, zoned write rules, device failure domains, and multi-device profiles reward different placements.

### Block groups and allocation groups

Partitioning a filesystem into allocation regions bounds searches and lock contention. Directories, inodes, and related data can be placed together, while top-level subtrees are spread across regions.

Per-group summaries accelerate choice but must match authoritative bitmaps or trees. Region-local allocation improves concurrency; imbalance and nearly-full groups can defeat locality.

### Fragmentation

External fragmentation leaves free capacity in runs too small for desired extents. Internal fragmentation wastes unused bytes inside allocated units. File fragmentation counts or weights mapping discontinuities.

Measure workload-relevant effects: extent count, I/O request count, latency, write amplification, and free-run distribution. A high extent count is not automatically harmful on every device.

### Preallocation

Preallocation reserves a range in advance to reduce later out-of-space failures and fragmentation. Linux exposes portable `posix_fallocate` semantics and richer filesystem-dependent `fallocate` operations.

Success does not prove data durability or immunity from every failure. Quota changes, device errors, copy-on-write needs, and implementation contracts still matter.

### Hole punch and zero range

Hole punch deallocates eligible whole units while keeping file size and making reads return zero. Zero-range operations can instead create or retain allocated unwritten extents.

These are observably similar through reads but differ in allocation, future write guarantees, extent reports, quota, and snapshot interactions.

### Range collapse and insertion

Collapsing removes a byte range and shifts later contents downward; insertion creates a hole and shifts later contents upward. Granularity and filesystem support restrict the operation.

Both transform many mappings and cached offsets. They require exclusive serialization with I/O, mappings, direct access, and extent queries.

### Truncation and extension

Shrinking changes logical size, zeros a partial terminal block as required, invalidates cache beyond end, removes mappings, decrements shared references, and releases quota. Ordering prevents old tail bytes from returning after re-extension.

Extending size alone commonly creates a hole. It does not necessarily allocate blocks, and reads of the new range return zero.

### Reflink and shared extents

A reflink clone creates another logical mapping to the same physical ranges and increments sharing metadata. Reads share bytes without immediate copying.

Any write to a shared range allocates private space, copies or overwrites the required bytes, and atomically remaps the writer. The old physical range remains until every owner releases it.

### Copy-on-write failure handling

Copy-on-write reserves worst-case data and metadata, writes the new version, and publishes a new mapping only after initialization. Failure before publication frees the private candidate and preserves all sharers.

Partial writes can split shared and private extents. Reference counts, reverse mappings, checksums, and quota records participate in the same recoverable transition.

### Compression and encryption

Compressed storage maps a logical range to an encoded physical region whose size and update granularity differ. A small overwrite can require rewriting a larger compression unit.

Encryption can add alignment and encoded-extent constraints. Extent-reporting flags must warn that device bytes are not directly interpretable file contents.

### Buffered write path

A buffered write copies data into page-cache folios, marks them dirty, updates size as required, and reserves or selects storage according to policy. Later writeback converts delayed mappings, builds I/O, and records completion errors.

Write return can precede allocation and device I/O. Synchronization joins dirty data, mapping metadata, size, and error reporting into the requested durability boundary.

### Direct I/O and DAX

Direct I/O bypasses much ordinary page-cache data flow but still needs mapping, allocation, zeroing, and synchronization with buffered access. Alignment and atomic-write capabilities are filesystem and device properties.

DAX-like access maps persistent memory more directly. Mapping invalidation, copy-on-write, truncation, and cache coherence remain required; “direct” does not eliminate metadata transactions.

### Extent reporting

Linux FIEMAP reports logical and physical extent information plus flags for delayed, unknown, encoded, inline, unwritten, merged, and shared state. Callers allocate a result array and continue until the last extent is reported.

The report is an observation, not authority to access a mounted device behind the filesystem. Concurrent allocation can stale it immediately, and encoded ranges cannot be interpreted as plain blocks.

### `SEEK_DATA` and `SEEK_HOLE`

These seek modes let applications discover data and hole boundaries when supported. A filesystem is permitted to provide conservative reporting, such as treating every range as data and only end of file as a hole.

Backup and sparse-copy tools therefore preserve contents even if sparseness is approximate. Unsupported operations and concurrent changes are normal cases.

### Allocation concurrency

Writers to distinct ranges can proceed concurrently when mapping trees, reservation counters, groups, and transaction credits permit. Overlapping write, truncate, punch, clone, and extent query require stronger exclusion or version validation.

Lock ordering spans inode, page cache, mapping tree, allocation region, quota, reference count, and journal. Bounded transaction restart cannot expose an intermediate map.

### Mapping and cache coherence

Cached pages are indexed by logical offset, while mappings determine backing storage. Remap operations invalidate or serialize cached and direct-I/O access before blocks are reassigned.

Writeback revalidates mappings when concurrent change is possible. An I/O completion for an obsolete mapping must not clear newer dirty state or update the wrong extent.

### Crash consistency

Allocating a block requires coordinated updates to free-space metadata, the file mapping, reference counts, quota, and sometimes checksums. Publishing mapping first risks cross-file disclosure; consuming space first can leak it on crash.

Journaling or copy-on-write root publication makes the compound transition recoverable. Recovery validates both directions: mapped blocks are owned, and allocated blocks are reachable or deliberately reserved.

### Out-of-space behavior

Allocation can fail because data blocks, metadata blocks, transaction credits, quota, region-local capacity, device zones, or copy-on-write reserves are exhausted. Aggregate free bytes alone do not guarantee success.

Errors propagate to the write, synchronization call, mapping operation, and later close or status channel as specified. Silent data loss is never an acceptable delayed-allocation policy.

### Repair and reverse mapping

A checker compares file maps against allocation metadata, shared reference counts, and optional reverse mappings. It detects overlap, multiply owned ordinary blocks, unreachable allocations, invalid extents, and count mismatches.

Repair chooses an authority only with evidence and records losses. Guessing ownership from one damaged index can convert a contained leak into cross-file corruption.

### Observability and experiments

Record logical operation and range, mapping states before and after, allocation group, extent lengths, reservations, quota, fragmentation, cache state, writeback, I/O and journal outcomes, synchronization, crash point, and recovery checks.

Benchmark cold and warm runs, capacity levels, concurrency, device geometry, filesystem and mount options. Separate semantic evidence from placement and performance observations.

### Security and assurance

Adversarial tests target offset overflow, stale data exposure, race-driven double allocation, shared-block overwrite, quota bypass, reservation leaks, stale extent reports, malformed trees, decompression bounds, writeback errors, and crashes.

Assurance names allocator, mapping, page-cache, storage, recovery, security, performance, and independent-verification reviewers. A fast sequential benchmark cannot certify isolation or recovery.

## Definitions and Notation

For file `f`, let logical domain `L_f=[0,S_f)` and mapping `M_f([x,y))` take states `H` (hole), `D` (delayed), `U(p)` (unwritten allocation), `W(p)` (written allocation), `I` (inline), or `C(p,k)` (shared physical range with reference count `k`).

Let `A(p)` be allocator ownership, `R(p)` shared reference count, `Q_f` quota charge, and `V_f` mapping version. Intervals are half-open, ordered by logical start, bounded by maximum file offset, and non-overlapping except where one operation holds unpublished candidate state.

For block size `B`, logical block `i=floor(offset/B)` and within-block displacement `d=offset mod B`. A simple contiguous extent `(l,p,k)` translates logical block `i` in `[l,l+k)` to `p+(i-l)`.

Define `durable(f,t)` only relative to declared persistence points for data, mappings, size, allocation, quota, reference counts, and directory publication. In-memory map visibility alone is insufficient.

## Mechanisms, Invariants, or Proof Structure

1. **Validate the range.** Check type, nonnegative offset and length, overflow, maximum size, alignment, operation mode, and filesystem support.
2. **Authorize and reserve.** Apply credentials, flags, immutable state, quota, free-space, metadata-credit, and copy-on-write worst-case policy.
3. **Stabilize conflicts.** Serialize overlapping I/O, page-cache, size, mapping, clone, truncate, and query operations with a documented lock or version order.
4. **Select placement.** Choose an eligible region and extent length using locality and fragmentation policy without weakening semantics.
5. **Initialize safely.** Represent holes or unwritten state until new physical bytes contain caller data or guaranteed zeros.
6. **Update ownership.** Couple file map, allocator, reverse map, shared reference count, quota, and checksum changes in one recoverable transaction.
7. **Publish atomically.** Expose the new mapping and size only at the defined linearization point; unwind candidates on failure.
8. **Maintain cache coherence.** Invalidate or serialize stale cached ranges and associate writeback completion with the exact mapping generation.
9. **Persist in order.** Write data before mappings that expose it, commit metadata, flush as required, and propagate late errors.
10. **Recover both directions.** Prove every reachable mapping owns valid storage and every allocated unit is reachable, reserved, or safely reclaimable.
11. **Bound work and retry.** Limit extent splits, tree depth, transaction size, reservations, zeroing, decompression, retries, and repair scanning.
12. **Preserve evidence.** Retain mapping versions, ranges, reservations, allocator choices, I/O, transaction, crash, recovery, and limitation records.

<!-- bijux-verify: {"id":"extent-map-translation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"logical=0 physical=100 state=written\nlogical=4 state=hole reads=zero\nlogical=8 physical=200 state=written\nextents=2 allocated-blocks=8 logical-blocks=12\n","stderr":""}} -->
```python
extents = [(0, 100, 4), (8, 200, 4)]


def map_block(logical: int) -> tuple[str, int | None]:
    for start, physical, length in extents:
        if start <= logical < start + length:
            return "written", physical + logical - start
    return "hole", None


for logical in (0, 4, 8):
    state, physical = map_block(logical)
    if state == "hole":
        print(f"logical={logical} state=hole reads=zero")
    else:
        print(f"logical={logical} physical={physical} state=written")
print(f"extents={len(extents)} allocated-blocks=8 logical-blocks=12")
```

The executable model demonstrates extent translation and a hole between mapped ranges. It omits allocation policy, bytes, partial blocks, cache, reservations, sharing, concurrency, persistence, and real filesystem behavior.

## Alternatives and Trade-Offs

- Contiguous maps minimize lookup and fragmentation but make unpredictable growth expensive.
- Linked allocation makes growth flexible but weakens random access and corruption containment.
- Indirect blocks offer regular bounded indexing but use one pointer per block; extents compress contiguous runs but require split and merge logic.
- Small units reduce internal fragmentation but enlarge maps and allocator overhead; large units reverse the trade-off.
- Inline data accelerates tiny files but complicates growth and metadata sizing.
- Delayed allocation improves placement and batching but shifts failure and requires honest reservations and late-error handling.
- Preallocation reduces later space risk but consumes quota and can reserve unused capacity.
- Copy-on-write clones are fast and space-efficient but add reference counts, write amplification, and out-of-space risk on modification.
- Compression saves capacity and I/O but adds CPU, variable mapping, and larger rewrite units.
- Global allocation can find better runs but contends; region-local allocation scales but can strand space.
- Online defragmentation improves layout while consuming bandwidth, temporary space, and copy-on-write churn.
- Precise extent reporting helps diagnostics but costs synchronization; approximate queries remain safer as observations.

## Failure Modes and Misconceptions

- **“File size equals allocated bytes.”** Holes, unwritten, inline, compressed, shared, and metadata storage break equality.
- **“A hole stores zero blocks.”** It stores no data allocation for that range; metadata and boundary blocks may still exist.
- **“Unwritten means free.”** Physical space is reserved but reads are logically zero.
- **“Delayed means unaccounted.”** Correct delayed allocation carries reservation or a documented weaker failure model.
- **“Preallocation makes future writes impossible to fail.”** I/O, metadata, quota changes, and copy-on-write can still fail.
- **“Extent count measures performance.”** Media, request merging, cache, workload, and extent size determine impact.
- **“FIEMAP returns stable device addresses.”** Results can stale and never authorize mounted-device access.
- **“Zero range and hole punch are identical.”** Read results can match while allocation and guarantees differ.
- **“Truncate only changes size.”** It coordinates cache, mappings, reference counts, quotas, partial-block zeroing, and recovery.
- **“Reflink is a normal copy.”** Storage remains shared until copy-on-write.
- **“Write can overwrite a shared block.”** It must first establish private ownership.
- **“Free-space count proves allocation will succeed.”** Metadata, alignment, region, quota, and transaction constraints can fail.
- **“Journaled means allocation cannot leak.”** Transaction design and replay correctness still require proof.
- **“Repair should trust whichever tree parses.”** Cross-structure evidence is required before changing ownership.

## Worked Examples

### Example 1

An extent `(logical 0, physical 10, length 1000)` replaces one thousand block pointers. Appending contiguously extends it; allocating elsewhere adds a second extent.

### Example 2

A 10 GiB virtual disk image contains 200 MiB of written ranges. Its logical size supports guest offsets, while a sparse-aware copy avoids allocating the holes.

### Example 3

A database preallocates an unwritten 1 GiB range. Reads return zeros, and later writes convert only initialized subranges to written without exposing prior disk contents.

### Example 4

Buffered writes dirty 16 adjacent blocks. Delayed allocation observes the full run at writeback and chooses one extent instead of sixteen early scattered blocks.

### Example 5

A hole punch begins halfway through one block and ends halfway through another. Interior blocks are freed; the two boundary fragments are zeroed and retained as needed.

### Example 6

Shrinking a file releases the final mappings and zeros the retained terminal block beyond new end. Re-extending later cannot reveal the removed tail.

### Example 7

Two snapshots share extent `p` with reference count two. A write by one snapshot allocates `q`, initializes it, switches that logical range to `q`, and decrements `p` to one.

### Example 8

A FIEMAP result marks a range delayed and physical location unknown. A diagnostic reports reservation state rather than inventing a stable device address.

### Example 9

The filesystem reports free data blocks but cannot split an extent tree within remaining transaction credits. Allocation fails honestly rather than publishing an unlogged map.

### Example 10

Crash injection after consuming an allocation but before map publication tests replay. Recovery either completes the committed map or returns the candidate block to free space, never assigns it twice.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects interval trees, B-trees, bitmaps, reference counts, fragmentation, and checksums. [Data Engineering](../../19-data-engineering/ROADMAP.md) connects file layout, partitioning, compaction, locality, and storage accounting.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies cross-layer requirements, failure analysis, traceability, and assurance. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects object placement, replication, leases, shared ownership, and recovery.

Within this program, [OS-039](039-shared-pages-and-page-cache.md) and [OS-042](042-inodes-and-metadata.md) supply cache and inode foundations; [OS-044](../ROADMAP.md), [OS-045](../ROADMAP.md), and [OS-047](../ROADMAP.md) deepen free-space, cache, and crash behavior.

## References

- Linux kernel documentation, [ext4 inode data mappings](https://docs.kernel.org/filesystems/ext4/ifork.html), current page checked 2026-09-04. Direct and indirect block maps, extent trees, inline data, extent structure, depth, length, and unwritten encoding.
- Linux kernel documentation, [ext4 Block and Inode Allocation Policy](https://docs.kernel.org/filesystems/ext4/allocators.html), current page checked 2026-09-04. Multiblock allocation, delayed allocation, locality, block groups, directory placement, and fragmentation policy.
- Linux kernel documentation, [iomap Library Design](https://docs.kernel.org/filesystems/iomap/design.html), current page checked 2026-09-04. Hole, delayed, mapped, unwritten, and inline mappings, shared and dirty flags, iterators, validity, and write obligations.
- Linux kernel documentation, [iomap Supported File Operations](https://docs.kernel.org/filesystems/iomap/operations.html), current page checked 2026-09-04. Buffered and direct I/O, writeback, seeking data and holes, swap constraints, unsharing, and extent reporting.
- Linux kernel documentation, [Fiemap Ioctl](https://docs.kernel.org/filesystems/fiemap.html), current page checked 2026-09-04. Range queries, result capacity, extent continuation, delayed, unknown, encoded, inline, unwritten, merged, and shared flags.
- Linux man-pages project, [fallocate(2)](https://man7.org/linux/man-pages/man2/fallocate.2.html), current page checked 2026-09-04. Allocation, keep-size, hole punch, range collapse, zero range, range insertion, unsharing, granularity, support, and errors.
- Linux man-pages project, [lseek(2)](https://man7.org/linux/man-pages/man2/lseek.2.html), current page checked 2026-09-04. `SEEK_DATA`, `SEEK_HOLE`, sparse-file discovery, permitted conservative implementations, and errors.
- Linux man-pages project, [truncate(2)](https://man7.org/linux/man-pages/man2/truncate.2.html), current page checked 2026-09-04. Shrinking, extension and zero reads, descriptor operation, type constraints, limits, and errors.
- Linux man-pages project, [posix_fallocate(3)](https://man7.org/linux/man-pages/man3/posix_fallocate.3.html), current page checked 2026-09-04. Portable file-space allocation intent, size effects, errors, and emulation caveats.
- Linux man-pages project, [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html), current page checked 2026-09-04. Data and required metadata synchronization, `fdatasync`, delayed error reporting, and directory-entry boundary.

## Exercises

### Exercise 1

Compare contiguous, linked, multilevel-indexed, and extent allocation for small files, random access, unpredictable growth, corruption, and large sequential workloads.

### Exercise 2

Specify buffered delayed allocation from write admission through reservation, placement, writeback, extent conversion, synchronization, error, and recovery.

### Exercise 3

Design truncate, hole punch, zero range, collapse, and insert operations. Cover partial blocks, cache, mappings, size, quota, concurrency, and crashes.

### Exercise 4

Specify reflink cloning and copy-on-write replacement with reference counts, reservations, failures, checksums, and recovery.

### Exercise 5

Build a validation and performance plan for a file allocator. Include fragmentation, capacity pressure, corruption, concurrency, interfaces, crash injection, evidence, and reviewers.

## Answers to the Exercises

### Answer 1

Contiguous allocation stores start and length, provides constant translation and excellent runs, but unpredictable growth can require relocation. Linked allocation accepts scattered growth with simple per-unit state, but random lookup is linear without a central table and pointer damage can lose or cycle a suffix. Multilevel indexing bounds lookup by tree depth and represents arbitrary placement but consumes one pointer per block plus index blocks.

Extents compress contiguous runs and scale through a balanced tree, making them strong for large sequential files and still correct under fragmentation. They require careful split, merge, balance, and transaction handling. Use workload distributions—not one archetype—to compare metadata bytes, lookup I/O, append failure, fragmentation, repairability, maximum size, and corruption containment.

### Answer 2

Validate offset and length, authorize the write, and reserve quota, data capacity, worst-case mapping metadata, and copy-on-write space before accepting dirty cache data under a strong reservation contract. Mark logical ranges delayed, update visible size safely, and attach the reservation to the exact dirty range. At writeback, lock or version the range, choose eligible contiguous storage, consume the reservation, create unwritten mappings where needed, and submit initialized data.

After successful I/O, convert only completed ranges to written, update size, blocks, checksums, quotas, and dirty generations, and commit the mapping/allocator transaction. On partial or failed I/O, retain dirty state or report error, remove failed candidates, and restore or release reservation exactly once. Synchronization waits for data and mapping persistence and reports late errors. Recovery exposes only mappings whose data-initialization and ownership protocol completed.

### Answer 3

All operations validate checked half-open ranges and filesystem granularity, then exclusively stabilize overlapping page-cache, direct-I/O, mmap, size, and mapping activity. Truncate shrink zeroes the retained boundary tail, invalidates pages beyond new end, removes mappings, decrements shared references, releases quotas, and publishes size in recoverable order. Extension commonly publishes holes.

Hole punch retains size, frees eligible whole units, and zeroes partial boundaries. Zero range creates zero-reading allocated or unwritten state. Collapse removes a range and shifts later logical mappings downward; insert shifts them upward and creates a hole. Each journals or copy-on-writes mapping, allocator, quota, timestamps, and reference counts; failure leaves old or complete new intervals. Crash tests target every split, boundary zero, cache invalidation, ownership update, and root publication.

### Answer 4

Clone stabilizes source and destination ranges, verifies alignment and compatibility, reserves mapping and reference-count metadata, then installs destination mappings to the source physical ranges and increments shared ownership atomically. Existing destination mappings are released only within the same recoverable transition. Checksums describe the shared contents without implying one mutable owner.

On a write, reserve worst-case private data and metadata, allocate an unshared candidate, copy unchanged partial-unit bytes and apply caller data, calculate checksums, and persist initialization before publishing the new mapping. Publication decrements old reference counts and updates reverse maps, quota, and timestamps. Failure before publication discards the candidate and leaves every sharer unchanged. Recovery reconciles maps, reverse maps, counts, allocation, and quota and never exposes half-initialized private bytes.

### Answer 5

Generate empty, tiny inline, contiguous, fragmented, sparse, preallocated-unwritten, delayed, compressed, encrypted, reflinked, huge, nearly full, quota-limited, and multigroup files. Exercise append, overwrite, direct and buffered I/O, mmap, truncate, punch, zero, collapse, insert, clone, unshare, FIEMAP, `SEEK_DATA`, `SEEK_HOLE`, unsupported modes, offset overflow, boundary alignment, concurrent overlap, memory pressure, writeback errors, and device failure.

Measure extent and free-run distributions, lookup and allocation latency, I/O request shape, throughput, amplification, reservation accuracy, metadata overhead, and fragmentation across cold and warm states without turning performance into a correctness claim. Inject crashes at allocation, initialization, map, reference-count, quota, journal, and flush boundaries; verify bidirectional ownership and zero-disclosure invariants after recovery. Preserve filesystems, kernels, mount options, device geometry, seeds, traces, disk images, raw results, and limitations. Named allocation, mapping, cache, storage, recovery, security, performance, and independent-verification reviewers assess the evidence.
