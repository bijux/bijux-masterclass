---
module_id: OS-038
program: Operating Systems
level: 1
module_number: 38
title: Memory-Mapped Files
status: complete
last_verified: 2026-09-04
---

# Memory-Mapped Files

## One-Page Review

### Governing question

How should an operating system bind a file range to virtual memory so ordinary loads and stores obey permissions, sharing, coherence, truncation, writeback, durability, and teardown semantics under faults and concurrency?

### Essential definitions

- A **file mapping** associates a virtual interval with bytes of a file at a page-aligned offset.
- A **virtual memory area (VMA)** records one virtually contiguous region with common mapping attributes.
- A **shared mapping** propagates modifications according to its shared-file contract.
- A **private mapping** presents a copy-on-write view whose changes are not written through to the file.
- A **major fault** commonly requires storage work; a **minor fault** can often install already resident content, subject to platform definitions.
- **Writeback** transfers dirty cached content toward its filesystem or backing device.
- **Direct access (DAX)** maps supported memory-like storage without the ordinary page-cache copy.

### Central model, mechanism, or theorem

A mapping is `M=(V,F,o,l,p,s,g)`: virtual interval `V`, file identity `F`, offset `o`, length `l`, protections `p`, sharing mode `s`, and generation `g`. Address `a in V` corresponds to file position `o+(a-start(V))`. A fault validates `M`, current file size and extent, permissions, cache or DAX state, and generation before installing a translation.

For shared writes, modified bytes enter the file's coherent cached or direct-access state and follow explicit synchronization and filesystem durability rules. For private writes, COW creates private state that is not propagated as a shared file modification. Unmap removes translations and mapping ownership; it is not a universal durability primitive.

### Critical invariants

- Address-to-file offset arithmetic is overflow-safe, page-aligned where required, and bounded by the mapping and current object rules.
- Requested protections never exceed file, mount, executable-memory, or device policy.
- Shared mapped access and ordinary file I/O follow the platform's stated coherence contract.
- Private modifications never become shared file updates through that mapping.
- Fault completion revalidates mapping, file size, extent, and generation after I/O or unlocked waits.
- Dirty data, writeback errors, truncation, hole punching, and storage failure have defined outcomes.
- Unmap, exit, exec, fork, and descriptor close update independent lifetimes and release each reference exactly once.

### Common failures

Common mistakes are assuming a mapping depends on keeping its original descriptor open, treating `MAP_PRIVATE` as a durable file editor, using `munmap` as a successful persistence acknowledgment, accessing beyond current file content during truncation, ignoring partial-page rules, holding address-space locks across unsafe filesystem work, confusing page-cache visibility with stable storage, and diagnosing mapped I/O from fault counts alone.

### Compact example

A process maps file bytes 8 KiB–12 KiB at virtual address `0x400000` with shared read/write access. A store at virtual offset 700 maps to file offset 8892. The first write fault validates the VMA and current file extent, obtains or allocates the page-cache folio, invokes the filesystem's write-fault preparation, installs a writable translation, and marks the content dirty. A later `msync(...,MS_SYNC)` requests writeback completion for the range; filesystem and device persistence guarantees still determine what survives power loss.

### Connections

[OS-032](032-page-tables.md) through [OS-037](037-copy-on-write.md) provide mappings, demand faults, replacement, and private copies. [OS-039](../ROADMAP.md), [OS-040](../ROADMAP.md), and [OS-041](../ROADMAP.md) extend page-cache sharing, pressure diagnosis, and allocator behavior.

## Governing Question

Memory mapping makes file bytes look like memory, but it does not erase either abstraction. Loads and stores operate through page tables and faults; the filesystem still owns names, sizes, extents, permissions, dirty state, writeback, and recovery.

The governing question is how to preserve both contracts while either side can change. Correctness spans syscall validation, VMA lifetime, page-cache coherence, filesystem fault callbacks, truncation invalidation, COW, TLBs, and storage durability.

## Why This Matters

Mapped files support executable images, shared libraries, databases, indexes, IPC, zero-copy-like access patterns, persistent-memory applications, and large random-access datasets. They can reduce explicit copy and syscall overhead and let demand paging fetch only touched regions.

The interface also creates hidden work. One load can block on storage; one store can allocate blocks and dirty memory; one truncation can invalidate translations across processes. Errors that an explicit `read` or `write` would return may instead appear as synchronous signals.

Production designs must distinguish visibility, writeback, filesystem commit, controller flush, and power-failure persistence. “The bytes changed in memory” is evidence for only the first part of that chain.

## Prerequisites and Retrieval

Review [OS-032](032-page-tables.md), [OS-034](034-demand-paging.md), [OS-035](035-page-faults.md), [OS-036](036-virtual-memory-page-replacement.md), and [OS-037](037-copy-on-write.md).

Retrieve these distinctions:

- virtual range, file range, page-cache folio, filesystem extent, and device block are different units;
- mapping lifetime, open-file-description lifetime, and descriptor lifetime are related but not identical;
- shared visibility, dirty tracking, writeback submission, writeback completion, filesystem commit, and durable media persistence differ;
- `MAP_SHARED` and `MAP_PRIVATE` define propagation semantics, not whether physical pages happen to be shared;
- page-fault locks, VMA locks, reverse-map locks, inode locks, invalidation locks, and folio locks protect different objects;
- current file size can change after mapping creation;
- cached mappings and DAX mappings take different data paths;
- a minor fault, major fault, and application stall are not interchangeable measurements.

## Learning Objectives

After this module, you should be able to:

1. validate mapping address, length, offset, protection, sharing, descriptor, and file-type inputs;
2. derive virtual-address-to-file-offset translation and partial-page boundaries safely;
3. trace read and write faults through VMA, cache or DAX, filesystem, page-table, and invalidation layers;
4. distinguish shared visibility, private COW, synchronization, writeback, and durable persistence;
5. reason about concurrent read, write, truncate, hole punch, unmap, fork, exit, and replacement;
6. diagnose mapped-I/O latency, coherence faults, writeback errors, and stale-state races;
7. build tests and assurance evidence for mapped-file lifecycle correctness.

## Core Exposition

### Mapping creation

An `mmap`-like operation receives an address hint or requirement, length, protections, flags, descriptor, and file offset. The kernel validates arithmetic, alignment, supported file type, access mode, executable policy, address availability, and resource limits.

Success creates VMA metadata; it need not read file contents or populate PTEs. Demand faults can defer allocation and I/O until access.

### Address and offset arithmetic

For virtual start `b`, address `a`, and file offset `o`, corresponding file position is `o+(a-b)`. Every subtraction, addition, rounding, and end computation must reject underflow and overflow.

Offsets are commonly page-aligned, while lengths need not be. Page-table coverage rounds outward, but user-visible access and file-byte semantics retain the requested interval and final-page rules.

### Placement and overlap

Without a fixed-placement contract, an address is generally a hint and the kernel chooses a suitable free interval. A returned pointer must be checked against the API's failure sentinel before use.

Replacing an existing mapping can destroy unrelated state, so fixed modes require precise platform semantics and race-aware reservation. Address-space layout randomization and guard regions also constrain placement.

### Protection validation

Read, write, and execute protections are checked against the opened file, mapping type, mount policy, architecture, and security controls. A writable shared mapping normally needs an appropriately writable file description; private mappings follow their documented access rules.

Do not grant execute or write permission merely because the faulting operation requests it. Later `mprotect` changes require their own authorization and invalidation.

### Shared and private semantics

A shared mapping makes updates visible to other participants and, for file-backed mappings, carries them toward the file under the interface contract. A private mapping creates a COW view whose modifications do not propagate to the file through that mapping.

Physical page sharing is an implementation choice. A private reader may initially use the same cache page as shared readers, then break COW on write.

### Descriptor and object lifetime

After a successful mapping, closing the original descriptor does not ordinarily remove the mapping. The mapping retains the object references it needs. Descriptor reuse therefore cannot redirect an existing VMA to another file.

Unlinking a pathname removes a directory entry, not necessarily the open object or mapping. Final storage reclamation waits for the filesystem's remaining-reference rules.

### Demand read faults

A read to an unpopulated file mapping traps. The handler stabilizes the current VMA, derives file offset, verifies size and permissions, and looks up the cache or direct-access mapping.

For cached I/O, it can join an in-progress fill or read data into a folio. After waiting, it revalidates mapping and extent before installing a read translation.

### Major and minor faults

A cache-resident page without a PTE may need only mapping work; a cold page may require storage. Platforms expose minor and major counters with specific definitions, but those counters do not directly measure storage operations or latency.

Readahead can make later faults minor while charging I/O to an earlier event. Compression, network filesystems, DAX, and device mappings further weaken naive interpretations.

### Shared write faults

The first shared write can fault even when reads already work. The filesystem's page-write preparation validates current size and extent, allocates blocks if necessary, excludes truncation or invalidation races, and establishes dirtying semantics.

Only then is a writable PTE installed. The store marks architectural and memory-management dirty state, and later writeback observes it.

### Private write faults

A private write follows COW rather than shared-file dirtying. The handler allocates or promotes private state, copies stable visible bytes, publishes a writable private PTE, and leaves the file's shared contents unchanged.

Later external modifications to the underlying file and their visibility through a private mapping are governed by platform rules; applications should not build synchronization on unspecified behavior.

### The page cache

Cached file mappings normally obtain data from the same page cache used by buffered file I/O. A unified cache lets mapped stores and ordinary reads observe coherent in-memory content under the platform and filesystem contract.

This avoids a separate mapped-file copy, but couples mapping faults to cache lookup, readahead, dirty limits, writeback, invalidation, and reclamation.

### Coherence with read and write

When a process modifies a shared cached mapping, a subsequent ordinary read should observe coherent file-cache data as specified. Ordinary writes must likewise invalidate or update mapped cache state so mappings do not retain stale bytes.

Direct I/O and network or special filesystems can impose alignment, invalidation, or coherence limitations. The application must use documented combinations rather than assume one universal model.

### Dirty tracking

Hardware dirty bits, software write protection, filesystem callbacks, and folio state cooperate to identify modified content. Dirtying without filesystem preparation can expose holes, violate size rules, or miss metadata allocation.

Dirty is not durable. It means memory contains a newer version requiring later propagation or explicit discard policy.

### Writeback

Background policy writes dirty mapped pages based on age, pressure, and filesystem rules. An explicit synchronization call can request scheduling or completion for a mapped range and report detected errors.

Writeback may include data and metadata dependencies, transactions, remote acknowledgments, or device caches. Count bytes submitted, completed, failed, and retried separately.

### `msync` semantics

Portable code supplies the documented synchronous or asynchronous flag and page-aligned address. Synchronous operation waits for the specified update operation; asynchronous operation schedules or permits background progress according to the platform.

The call does not make application invariants crash-consistent by itself. Ordering among multiple fields, file-size changes, metadata, and other files needs a recovery protocol and appropriate filesystem primitives.

### Visibility versus durability

Another process can observe shared dirty cache bytes before they reach stable storage. Conversely, an I/O completion can still sit behind volatile controller state unless the storage stack's persistence contract closes that boundary.

Specify the failure model: process crash, kernel crash, power loss, device loss, or distributed-server failure. Each requires different evidence.

### Partial final pages

Files rarely end exactly on a page boundary. POSIX-like systems define zero-fill behavior for the remaining bytes of the final mapped page and restrict propagation beyond the object end under their rules.

Access to later pages beyond the object can fault with a bus-like error. Never infer that rounded PTE coverage extends the file's valid byte range.

### Truncation races

Another thread or process can shrink the file while mappings remain. The filesystem invalidates affected cached ranges and unmaps or poisons translations under its rules; later access beyond the new end cannot return stale freed blocks.

Fault handlers that waited on I/O must recheck size, extent, and validity cookies. Installing a page from the pre-truncate layout is a data-integrity and confidentiality bug.

### File growth and holes

A mapping length can exceed the current file size, but that does not authorize accesses beyond valid content. File growth may make later positions valid according to platform behavior and mapping lifetime.

Sparse holes read as zeros. A shared write may allocate an extent and metadata; failure leaves defined hole or partial-write state rather than exposing old device contents.

### Hole punching and extent remapping

Hole punch, reflink, deduplication, and extent remapping change physical backing without necessarily changing virtual addresses. They must coordinate cache invalidation, writeback, page faults, and reverse mappings.

Generation or validity tokens detect stale filesystem mappings across unlocked operations. Locks cannot simply be held across every I/O and fault without deadlock analysis.

### Unmapping

`munmap` removes all or part of a virtual mapping, splits or trims VMA metadata, zaps PTEs, performs required TLB invalidation, updates reverse maps, and releases references when no range remains.

Other threads can race accesses with teardown. The address-space locking contract determines whether a fault completes, retries, or observes no mapping. After successful unmap, dereference is invalid regardless of whether the virtual address is later reused.

### Fork, exit, and exec

Mappings normally cross fork with the same attributes. Shared mappings continue their shared contract; private mappings use COW separation. The child acquires its own VMA and object references.

Exit and successful exec tear down old mappings. Cleanup must write or preserve dirty shared content according to platform and filesystem rules, but applications needing confirmed synchronization use the explicit contract instead of relying on process termination.

### Page replacement

Clean cached mapped pages can be evicted and faulted back. Dirty pages need writeback or another preserved representation. Mapped pages require reverse-map traversal and PTE invalidation before frame reuse.

Pins, locks, active I/O, and DAX can alter reclaimability. Refault and pressure evidence distinguishes useful cache eviction from thrashing.

### DAX mappings

DAX maps supported memory-like storage directly, bypassing the ordinary page-cache copy. Fault handlers establish device-backed translations, including write-fault preparation and filesystem extent validation.

Direct mapping does not make persistence automatic. Applications need the documented mapping flags, CPU cache-management instructions, ordering, filesystem support, and error handling for their durability guarantee.

### Device and special mappings

Character devices, shared memory, and other objects can expose mapping operations without ordinary file-cache semantics. Their fault, close, invalidation, and pin rules belong to the provider's contract.

Validate ranges and privilege carefully. Mapping device registers or physical memory can have side effects and security consequences unlike regular file bytes.

### Locking and deadlock

Mapped-file faults connect VMA, reverse-map, page-table, invalidation, inode, filesystem transaction, folio, and writeback locks. Linux documents explicit ordering because read, write, truncate, and fault paths can call into one another.

Never hold a spin lock across blocking storage. Revalidate after dropping locks, and test indirect page faults caused by copying user buffers while filesystem locks are held.

### Error delivery

Creation errors return from the mapping syscall. Access-time errors such as invalid permission, backing I/O failure, poisoned memory, or beyond-end access can arrive as synchronous faults or signals under platform policy.

Writeback errors may surface through synchronization or later filesystem operations. Define which component records and acknowledges an error so it is not silently lost or reported forever.

### Observability and experiments

Record mapping creation and failure, VMA count, mapped bytes, resident and proportional bytes, minor and major faults, cache hit, readahead, fault latency, folio lock wait, storage I/O, dirty bytes, writeback latency and errors, invalidation, COW, TLB work, and signals.

Preserve kernel, filesystem, mount, storage, page-size, DAX, readahead, dirty-limit, NUMA, file-layout, workload, cache-state, concurrency, and failure-injection configuration with raw timelines.

### Security and assurance

Validate file access and mapping bounds, zero new or hole-backed storage, preserve execute policy, reject stale extents after truncation, sanitize reused frames, and restrict mapping diagnostics. A mapping must not outlive authorization in ways forbidden by the object contract.

Adversaries can race truncate and fault, exhaust VMAs, dirty memory faster than writeback, induce sparse allocation, exploit arithmetic boundaries, and probe timing. Bound resources and independently review cross-layer failure behavior.

## Definitions and Notation

Let mapping `M=(b,e,F,o,l,p,s,g)` contain virtual interval `[b,e)`, file identity `F`, offset `o`, requested length `l`, protection `p`, sharing mode `s`, and generation `g`. For `a in [b,e)`, file position is `phi_M(a)=o+(a-b)` when arithmetic and current object bounds are valid.

Let cached version be `C(F,x,t)`, on-storage durable version under failure model `D(F,x,t)`, and private COW version `P(M,x,t)`. Shared visibility can update `C` before `D`; private writes update `P` without making the same change to `C` through that mapping.

Fault resolution `R(M,a,q,t)` uses access `q` and current time-varying file state to return `map-cache`, `map-dax`, `break-cow`, `retry`, `signal`, or `fail`.

## Mechanisms, Invariants, or Proof Structure

A reviewable mapped-file implementation follows twelve obligations:

1. Validate address, length, offset, overflow, alignment, flags, descriptor, object type, and protection.
2. Create VMA and object references atomically or unwind without altering unrelated mappings.
3. Translate address to file position with explicit page and final-byte boundaries.
4. Stabilize VMA, file identity, size, extent, cache or DAX state, and generation during faults.
5. Separate shared write preparation, private COW, genuine denial, and delegated tracking.
6. Revalidate after I/O, allocation, or any unlocked wait and reject stale completion.
7. Preserve coherence among shared mappings and supported ordinary file I/O paths.
8. Track dirty content and propagate data, metadata, completion, and error under explicit sync rules.
9. Coordinate truncate, hole punch, remap, unmap, fork, exit, exec, reclaim, and device access.
10. Order PTE changes, reverse maps, cache invalidation, and CPU or device translation invalidation.
11. Bound faults, VMA growth, dirty memory, writeback, retries, and adversarial resource use.
12. Test visibility, private isolation, durability boundaries, races, and failures with preserved evidence.

The executable toy contrasts one possible shared cached view with a private COW snapshot.

<!-- bijux-verify: {"id":"mapped-file-views","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial file=DATA shared=DATA private=DATA\nafter-private file=DATA shared=DATA private=XATA\nafter-shared file=DYTA shared=DYTA private=XATA\n","stderr":""}} -->
```python
file_cache = bytearray(b"DATA")
shared_view = file_cache
private_view = None

def read_private():
    return file_cache if private_view is None else private_view

def private_write(offset, value):
    global private_view
    if private_view is None:
        private_view = bytearray(file_cache)
    private_view[offset] = value

def show(label):
    file_text = file_cache.decode()
    shared_text = shared_view.decode()
    private_text = read_private().decode()
    print(f"{label} file={file_text} shared={shared_text} private={private_text}")

show("initial")
private_write(0, ord("X"))
show("after-private")
shared_view[1] = ord("Y")
show("after-shared")
```

The toy chooses snapshot-on-first-private-write behavior and equates the file with one cache array. It omits unspecified private visibility of later file changes, pages, faults, writeback, persistence, filesystems, locks, truncation, errors, and processes.

## Alternatives and Trade-Offs

- Explicit `read` and `write` expose operation boundaries but require calls and buffer management.
- Memory mapping offers direct address-based access but moves I/O and errors into faults.
- Shared mappings simplify shared data access but couple dirtying, coherence, and writeback.
- Private mappings isolate modifications but incur COW and do not persist edits through the mapping.
- Eager population reduces later fault variance but increases startup I/O and resident pressure.
- Demand paging avoids untouched work but creates access-time latency and failure.
- Large pages reduce translation overhead but coarsen I/O, dirty tracking, and invalidation.
- Aggressive readahead helps sequential access but wastes bandwidth and cache on random workloads.
- Synchronous writeback provides a completion point but increases foreground latency.
- Asynchronous writeback improves responsiveness but needs later error and durability handling.
- Page-cache mappings unify buffered I/O but add cache and writeback machinery.
- DAX removes the cache copy but adds media, CPU-cache, alignment, and persistence constraints.

## Failure Modes and Misconceptions

1. **“`mmap` reads the whole file.”** successful creation can leave all pages unpopulated.
2. **“The descriptor must remain open.”** the mapping retains its own object lifetime after success.
3. **“`MAP_PRIVATE` edits the file later.”** its COW modifications are not shared file updates.
4. **“`MAP_SHARED` means durable immediately.”** visibility and persistence are different stages.
5. **“`munmap` is a durability acknowledgment.”** explicit synchronization and storage contracts are needed.
6. **“Rounded pages extend valid file bytes.”** beyond-end access follows object and partial-page rules.
7. **“File size cannot change while mapped.”** truncate and growth can race active mappings.
8. **“One lock protects the mapping.”** VMAs, PTEs, cache, extents, and writeback have distinct locks.
9. **“Minor fault means cheap.”** lock contention and page-table work can still be costly.
10. **“Major fault equals one disk read.”** readahead, networks, compression, and cache state complicate attribution.
11. **“Dirty bit means data is safe.”** it means propagation remains necessary.
12. **“DAX stores are automatically persistent.”** cache flush, ordering, filesystem, and media rules still apply.
13. **“Unlink invalidates existing mappings.”** object lifetime can continue without the pathname.
14. **“Passing one-process tests proves coherence.”** cross-process, I/O, truncate, failure, and recovery cases remain.

## Worked Examples

### Example 1

A 1 GiB file is mapped but only two pages are touched. Demand faults read those regions, avoiding eager transfer of the remaining file; VMA and virtual-size accounting still cover the full mapping.

### Example 2

The application closes descriptor 5, which is reused for another file. Its old mapping continues to reference the original object because VMA lifetime is not descriptor-number lifetime.

### Example 3

One process stores through a shared cached mapping and another calls `read`. Unified cache coherence exposes the dirty in-memory bytes even though stable storage has not yet been updated.

### Example 4

A private mapping reads cache bytes, then writes one page. COW produces private state; an `msync` on that private change does not turn it into a shared file modification.

### Example 5

A fault waits for a page read while another process truncates the file below that offset. Size and extent revalidation rejects stale installation and delivers the platform's beyond-end outcome.

### Example 6

A shared store targets a sparse hole. Write-fault preparation allocates and zeroes backing before granting write access, preventing disclosure of old device content.

### Example 7

Partial `munmap` removes the middle of a mapping. The kernel splits VMA metadata, zaps only that interval, invalidates translations, and retains object references for the surviving pieces.

### Example 8

Writeback submits dirty pages successfully but a later device error prevents completion. Error accounting reaches the synchronization caller rather than being erased when pages are cleaned optimistically.

### Example 9

A DAX application observes its store immediately through a shared mapping. Without the required cache flush and ordering sequence, a power failure can still lose it; visibility did not prove persistence.

### Example 10

A dashboard shows fewer major faults after larger readahead, but read amplification, cache eviction, and p99 fault latency worsen for random access. Raw I/O and refault evidence rejects the tuning.

## Cross-Program Connections

[Programming Languages: Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) connects mapping APIs, signals, pointer lifetime, and explicit synchronization. [Database Engineering](../../18-database-engineering/ROADMAP.md) connects buffer management, write-ahead logging, page formats, recovery, and mapped storage.

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies page tables, TLBs, caches, dirty bits, persistent-memory ordering, and device mappings. [Security Engineering](../../25-security-engineering/ROADMAP.md) frames file authorization, W^X, stale extents, zeroing, side channels, and denial of service.

Within this program, [OS-035](035-page-faults.md) and [OS-037](037-copy-on-write.md) explain access-time handling; [OS-039](../ROADMAP.md), [OS-040](../ROADMAP.md), and [OS-050](../ROADMAP.md) expand shared cache, pressure, and filesystem integration.

## References

- Linux man-pages project, [mmap(2) and munmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html), current page checked 2026-09-04. Address, length, offset, protection, shared and private mappings, fixed placement, partial pages, fork, unmapping, DAX flags, and errors.
- Linux man-pages project, [msync(2)](https://man7.org/linux/man-pages/man2/msync.2.html), current page checked 2026-09-04. Range synchronization, synchronous and asynchronous modes, invalidation, alignment, completion, and errors.
- Linux kernel documentation, [Process Addresses](https://docs.kernel.org/mm/process_addrs.html), current page checked 2026-09-04. VMA, mmap, reverse-map, and page-table locks; fault stability; invalidation; page-table teardown; atomicity; and lock ordering.
- Linux kernel documentation, [Locking](https://docs.kernel.org/filesystems/locking.html), current page checked 2026-09-04. Filesystem mmap operations, fault and page-write callbacks, invalidate locking, folio locking, truncate races, and error contracts.
- Linux kernel documentation, [Memory Management APIs](https://docs.kernel.org/core-api/mm-api.html), current page checked 2026-09-04. File-fault helpers, mapping and folio operations, dirtying, writeback, readahead, invalidation, and COW mappings.
- Linux kernel documentation, [Direct Access for files](https://docs.kernel.org/filesystems/dax.html), current page checked 2026-09-04. Page-cache bypass, DAX file mappings, fault callbacks, extent zeroing, locking, active state, and limitations.
- Linux kernel documentation, [iomap design](https://docs.kernel.org/filesystems/iomap/design.html), current page checked 2026-09-04. File extents, holes, unwritten and shared mappings, validity cookies, stale detection, page-cache operations, DAX, and zeroing.
- MIT PDOS, [6.1810 Lab: mmap](https://pdos.csail.mit.edu/6.1810/2025/labs/mmap.html), 2025 course material. Teaching VMA metadata, lazy faults, permissions, shared and private modes, dirty writeback, unmap, exit, fork, reference counts, and simplifications.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching treatment of virtual memory, files, caching, locking, faults, and filesystem recovery boundaries.

## Exercises

### Exercise 1

Design validation and VMA state for a file-mapping syscall. Cover address, length, offset, flags, protections, file lifetime, placement, overflow, and unwind.

### Exercise 2

Specify read-fault, shared-write-fault, and private-write-fault paths. Include cache lookup, filesystem preparation, COW, revalidation, publication, and errors.

### Exercise 3

Analyze a truncate racing a fault and a partial unmap racing access. Define locks, generations, invalidation, cleanup, and terminal outcomes.

### Exercise 4

Construct a crash-consistent update protocol for a shared mapped data structure. Distinguish visibility, writeback, ordering, filesystem commit, and recovery.

### Exercise 5

Build a performance and assurance test plan for cached and DAX mappings. Cover access patterns, faults, coherence, pressure, durability, hostile races, and reviewers.

## Answers to the Exercises

### Answer 1

Validate nonzero length, overflow-safe virtual and file ends, required offset alignment, exactly one supported sharing mode, known flags, file type, descriptor access, requested read/write/execute permissions, resource limits, and placement semantics. Reject unauthorized executable or writable shared mappings. Reserve a nonoverlapping interval unless an explicit replacement mode applies.

Create VMA state containing virtual bounds, requested length, file identity and retained reference, offset, protections, sharing, page-size policy, operations, and generation. Publish it atomically under address-space mutation locks. If any allocation, callback, or insertion fails, remove only new state and release every acquired reference; existing mappings and descriptor state remain unchanged.

### Answer 2

A read fault stabilizes the VMA, computes the file position, validates permissions and current size, then joins or starts cache fill or resolves DAX backing. After I/O or allocation it rechecks VMA, generation, file extent, and truncation state before installing a readable PTE.

A shared write fault invokes filesystem page-write preparation under required invalidation, inode, extent, and folio rules, allocates and zeroes holes, revalidates, then installs write access and dirty tracking. A private write instead stabilizes visible source bytes and breaks COW into private state. Genuine protection and beyond-end accesses receive defined faults; I/O and allocation errors preserve old state. Every path balances folio, VMA, file, and candidate references.

### Answer 3

Truncate serializes extent and size change with cache invalidation, finds reverse mappings, removes affected PTEs, performs translation invalidation, and prevents new faults from installing the old layout. A fault that waited carries file identity, offset, and validity generation; mismatch makes it discard its folio or mapping candidate and reclassify against the new end.

Partial unmap holds address-space mutation authority, trims or splits VMA metadata, makes the removed interval unreachable to new faults, zaps PTEs, updates reverse maps, invalidates TLBs, and drops references only for eliminated pieces. A racing access either completes under old stabilization before teardown or faults against current no-mapping state. Neither path frees page tables while lockless walkers can still reach them.

### Answer 4

Choose a recoverable representation such as two records plus generation, checksum, and commit marker, or a write-ahead log. Modify shared cache bytes in an order that never makes an incomplete version appear committed. Request data writeback and wait using the platform's synchronous primitive, then persist required metadata and ordering barriers under filesystem and storage rules before publishing the durable commit indicator.

Define recovery to select only a complete generation and repair or ignore partial state. Account for torn writes, process crash, kernel crash, power loss, delayed allocation, writeback error, and DAX cache persistence separately. Interprocess locks govern live consistency; they do not replace crash ordering. Test by injecting failure at every boundary and reopening through an independent path.

### Answer 5

Exercise sequential, random, sparse, read-only, shared-write, private-write, mixed buffered I/O, fork, truncation, hole punch, replacement, and working-set overflow. Control page and folio size, cache state, readahead, dirty thresholds, NUMA placement, filesystem, mount, storage, DAX state, concurrency, and repetitions.

Measure creation, VMA count, mapped, resident and proportional bytes, minor and major faults, fault latency, cache hits, readahead amplification, I/O, dirtying, writeback latency and error, invalidation, COW, TLB work, PSI, throughput, and tail latency. Inject stale extent, I/O error, allocation failure, poison, truncate-fault and unmap-fault races, dirty floods, and crash points. Preserve raw timelines and configurations. Named VM, filesystem, storage, architecture, security, performance, reliability, and independent-verification reviewers assess residual risk; passing mmap tests alone do not certify coherence or durability.
