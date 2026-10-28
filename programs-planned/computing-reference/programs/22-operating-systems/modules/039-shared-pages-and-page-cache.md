---
module_id: OS-039
program: Operating Systems
level: 1
module_number: 39
title: Shared Pages and Page Cache
status: complete
last_verified: 2026-09-04
---

# Shared Pages and Page Cache

## One-Page Review

### Governing question

How should an operating system maintain one coherent, reclaimable in-memory representation of file content across processes, mappings, buffered I/O, writeback, and changing storage state without confusing sharing, residency, ownership, or durability?

### Essential definitions

- The **page cache** stores file content in memory, keyed by file identity and logical offset or index.
- An **address space** is the kernel object that relates a file's cached entries to filesystem operations; it is not a process virtual address space.
- A **folio** is a physically, virtually, and logically contiguous group of base pages managed as one memory unit in current Linux terminology.
- A **cache hit** finds usable current content; a **cache miss** requires allocation, retrieval, or another resolution.
- An **uptodate** cache entry contains valid content for the range under its filesystem contract.
- A **dirty** entry has modifications not yet propagated to its required backing representation.
- **Readahead** fetches cache content before an explicit demand for every included byte.

### Central model, mechanism, or theorem

Represent a cached entry as `E=(F,i,n,v,state,g,owners)`: file identity `F`, logical index `i`, span `n`, content version `v`, lifecycle state, generation `g`, and ownership or charge evidence. All supported cached reads and shared mappings of the same current `(F,range)` converge on compatible content version `v`; private COW versions are outside that shared identity.

Lifecycle is `absent -> allocating -> filling -> uptodate -> dirty -> writeback -> clean`, with invalidation, error, and reclaim edges. A transition is safe only when lookup identity, folio lock and references, filesystem extent, mapping generation, dirty state, and error propagation remain consistent. Residency or writeback completion does not by itself prove durability.

### Critical invariants

- At most one authoritative current cache entry covers a given file range within the cache's overlap rules.
- Readers never consume an entry as uptodate before successful fill and integrity checks complete.
- Shared mapped writes and supported buffered I/O converge on coherent cached content.
- Dirty data cannot be discarded or reused until preserved or explicitly invalidated under a legal policy.
- Truncation, hole punch, direct I/O, and remote invalidation cannot leave stale cache mappings accessible.
- Every lookup, mapping, private attachment, writeback, and transient user balances its own references.
- Reclaim, readahead, writeback, and cache growth are bounded and observable by file, workload, node, and memory domain.

### Common failures

Common mistakes are keying cache pages by descriptor rather than stable file identity, treating a reference count as mapping count, exposing a partially filled page, assuming dirty means durable, double-caching mapped and buffered reads, allowing truncate to race a stale refill, invalidating data under writeback without a policy, using hit ratio without byte and latency context, and letting streaming readahead evict a hot working set.

### Compact example

Two processes map the same shared file page while a third reads it through `read`. One cache folio keyed by the inode-like object and index supplies all three. A mapped store dirties that folio; the next buffered read sees the changed cache bytes before storage writeback. The writeback path locks and submits the folio, records any error, and marks it clean only after the required completion. Reclaim cannot free it while mapped, referenced, dirty without preservation, or under active writeback.

### Connections

[OS-035](035-page-faults.md) through [OS-038](038-memory-mapped-files.md) provide demand, replacement, COW, and mapping semantics. [OS-040](../ROADMAP.md), [OS-049](../ROADMAP.md), and [OS-050](../ROADMAP.md) extend pressure diagnosis, crash consistency, and filesystem integration.

## Governing Question

Without a unified cache, an ordinary read and a mapped read could hold independent copies of the same file bytes and disagree after a write. A shared page cache solves that coherence problem but becomes a meeting point for virtual memory, filesystems, storage, accounting, and reclaim.

The governing question is how to define identity and transition state precisely. One logical range can be absent, under read, mapped many times, dirtied, under writeback, truncated, invalidated, reclaimed, or represented by a larger folio while other threads act concurrently.

## Why This Matters

The page cache converts spare memory into lower I/O latency and higher throughput. It supports executables, shared libraries, mapped databases, ordinary file I/O, network filesystems, and content integrity. Its quality often dominates end-to-end storage performance.

Cache memory is not free. It competes with anonymous memory, consumes CPU for lookup and reclaim, and can amplify I/O through bad readahead or writeback. Shared content also complicates cgroup charging and tenant fairness.

Correctness failures can expose stale or uninitialized disk blocks, lose dirty data, violate mapped-I/O coherence, or use freed pages. The cache must be treated as a versioned concurrent data structure with filesystem-owned semantics.

## Prerequisites and Retrieval

Review [OS-032](032-page-tables.md), [OS-034](034-demand-paging.md), [OS-035](035-page-faults.md), [OS-036](036-virtual-memory-page-replacement.md), and [OS-038](038-memory-mapped-files.md).

Retrieve these distinctions:

- process address space and file cache address space are different objects;
- file identity and logical offset differ from pathname, descriptor number, virtual address, and device block;
- resident, referenced, mapped, uptodate, dirty, under writeback, pinned, and reclaimable are independent properties;
- map count, reference count, and memory-controller charge track different relationships;
- cache visibility, writeback completion, filesystem commit, and durable media state are separate;
- buffered, mapped, direct, and DAX I/O can take different paths;
- readahead usefulness is known only after demand or eviction feedback;
- a hit count without bytes, latency, and workload phase can mislead.

## Learning Objectives

After this module, you should be able to:

1. define cache identity by file object, logical index, span, and version;
2. trace miss, fill, lookup, shared write, dirtying, writeback, invalidation, and reclaim;
3. distinguish folio lock, reference, map count, dirty state, writeback, and LRU membership;
4. reason about mapped and buffered coherence, direct I/O, truncate, holes, remote filesystems, and integrity;
5. design readahead and large-folio policy for sequential, random, sparse, and mixed workloads;
6. diagnose cache pollution, refault, writeback congestion, stale data, and ownership unfairness;
7. construct concurrency tests and assurance evidence for cache lifecycle correctness.

## Core Exposition

### Cache identity

A cache key begins with a stable open file object such as an inode-associated mapping, not a pathname or descriptor number. Renaming a file does not change its content identity; reusing a descriptor must not alias old cache entries to a new file.

The second dimension is logical file position, commonly represented by page or folio index. Filesystem extent mapping later translates this logical position to storage.

### Address spaces and process mappings

In Linux terminology, `struct address_space` represents a file's cached content and operations. A process `mm` and its VMAs represent virtual address ranges. Many process VMAs can refer to one file address space.

Keeping the words distinct prevents a common category error: locking or destroying a VMA does not automatically lock or destroy the underlying cache entry.

### Pages and folios

Traditional explanations use page-sized cache entries. Current kernels can manage a folio spanning multiple base pages, reducing per-unit overhead and improving contiguous I/O.

The folio's index must align to its span, and overlapping cache entries are forbidden by the implementation's rules. Metrics report bytes and size distribution so one large folio is not confused with one base page.

### Lookup

A lookup searches the file mapping for the logical index and takes a reference before using a found entry. Concurrent removal means an unlocked pointer is insufficient. Some lockless searches provide a momentary result rather than an atomic snapshot.

A miss can race another miss. One insertion wins the key range; the loser discards or reuses its allocation without installing an overlap.

### Allocation and insertion

A new folio is charged to the relevant memory domain, added to cache indexing and reclaim structures, and returned with documented lock and reference state. Publication order prevents readers from mistaking allocated storage for valid file bytes.

Failure can result from memory pressure, cgroup limits, invalidated mappings, or unsupported folio size. Unwind removes only the candidate's state.

### Filling content

The filesystem maps logical ranges to holes, inline data, local extents, remote objects, compressed clusters, or other backing. It reads or synthesizes bytes, verifies required integrity, marks successful content uptodate, records errors otherwise, unlocks, and wakes waiters.

New allocations and holes must return zeros where the interface requires. Partial I/O cannot expose uninitialized remainder bytes.

### Joining in-progress fills

When another thread finds a locked non-uptodate folio, it may wait, retry, or use an asynchronous continuation. It holds a reference and follows lock ordering; it does not issue a conflicting fill blindly.

After wakeup it checks uptodate and error state again. A completed I/O can race truncation or invalidation, so mapping identity and generation remain relevant.

### Mapped reads

A mapped-file fault derives the file index from VMA offset and address, then looks up the same cache used by buffered I/O. Once an uptodate folio is stable, the handler installs a process PTE and updates map and access state.

One folio can be mapped at different virtual addresses in many processes. Reverse mappings support invalidation and reclaim without making virtual address part of cache identity.

### Buffered reads

An ordinary read copies from an uptodate cache folio into the caller's buffer. If absent, the read path fills the cache, often with readahead. Offset and short-read rules remain file semantics rather than cache policy.

User-copy faults and filesystem locks create deadlock risks. Implementations use documented lock ordering and may prefault buffers or retry outside locks.

### Shared mapped writes

A shared mapped store first obtains filesystem permission to make the page writable, including extent allocation and truncate exclusion when needed. The store changes the common cache folio and dirty tracking records that newer content exists.

Other shared mappings and buffered readers then observe coherent cached bytes under platform rules. CPU cache aliases and TLB permissions require architecture handling.

### Buffered writes

A buffered write locks or otherwise stabilizes the target folio, prepares filesystem blocks, copies bytes into cache, completes filesystem metadata work, and marks the folio dirty. Partial-copy and fault outcomes report exactly how many bytes became valid.

The write can overwrite only a subrange. Existing bytes outside it must remain coherent, including within a large folio.

### Dirty state

Dirty state means the cache version is newer than its required backing representation. It may be tracked at folio, buffer, block, range, inode, or filesystem transaction granularity.

Redirtying during writeback is legal. Clearing the dirty bit at submission without tracking concurrent modification risks losing the newer version.

### Writeback

Writeback chooses dirty entries, locks or tags them under the filesystem protocol, maps current extents, submits I/O, and records completion. It balances throughput, memory pressure, ordering, device congestion, and fairness.

A writeback bit means I/O is in progress, not that content is clean or durable. Waiters retain references and cannot hold locks that completion needs.

### Writeback errors

Storage or remote-server failures must be associated with the mapping and surfaced through defined synchronization or later file operations. One caller acknowledging an error must not accidentally hide it from unrelated ownership semantics.

Retry policy distinguishes transient failure from permanent loss. Infinite redirty and retry can consume memory and I/O without progress.

### Readahead

Readahead predicts nearby future demand after a read or fault misses or encounters a marker from a previous window. It allocates and starts I/O for entries not already present.

Sequential access benefits from larger windows and overlap; random or sparse access can waste bandwidth and evict useful cache. Track useful, unused, late, and reclaimed readahead bytes.

### Large folios

Larger folios reduce tree entries, faults, locks, and I/O submissions for contiguous access. They can also read unused bytes, increase allocation difficulty, dirty amplification, COW cost, and false sharing.

Adaptive size policy considers access pattern, file layout, filesystem support, memory fragmentation, and pressure. It falls back cleanly when a large allocation fails.

### Cache coherence

The unified-cache goal is that supported mapped and buffered paths use one current logical version. Coherence does not mean every CPU, device, or remote client observes each byte simultaneously without synchronization.

Application data-race rules, CPU cache coherence, filesystem locks, network leases, and storage ordering form additional layers. State which one a claim covers.

### Direct I/O

Direct I/O bypasses ordinary page-cache data transfer. To avoid stale cache or overwriting newer dirty content, the filesystem coordinates direct ranges with writeback and invalidation before and after I/O under its contract.

Alignment and partial-I/O behavior vary. Mixing direct and cached access requires documented support and explicit testing rather than assuming bypass means independence.

### DAX

DAX maps memory-like storage directly and does not use normal page-cache pages for file data. It still needs filesystem extent validation, fault handling, invalidation, cache-line persistence, and error policy.

Page-cache counters cannot diagnose a DAX path. Observability must identify the active I/O mode.

### Truncation and invalidation

Shrinking a file removes cache content beyond the new end, unmaps affected PTEs, and prevents concurrent fills from reinstalling stale entries. Partial final folios require zeroing or range invalidation under filesystem rules.

The invalidation lock or equivalent serializes page-cache fills with truncate, hole punch, and remapping. A stale completion is discarded after generation revalidation.

### Hole punch and remapping

Punching a hole changes valid backing to zeros; extent swap, reflink, or deduplication can redirect backing. Dirty data is flushed, discarded, or transformed under an explicit rule before cache invalidation.

The operation coordinates ordinary writes and mapped write faults as well as readers. Otherwise a writer can repopulate the old extent during the change.

### Network filesystems

A network cache adds server versions, leases, attributes, disconnected operation, local disk cache, and network failures. “Uptodate” is relative to the consistency contract and validated server state.

Callbacks or lease loss can invalidate cached folios. Offline modifications need conflict and recovery policy, not merely local dirty bits.

### Integrity and authenticity

Verified filesystems check data before marking a cache folio uptodate. Hash-tree blocks may themselves use cache and I/O, so recursion, locking, and failure containment matter.

Verification failure produces a defined read or fault error and never exposes unverified bytes as valid executable or data content.

### Executable and immutable content

Executable mappings often read shared clean cache pages, giving large memory savings across processes. File modification, executable policy, and instruction-cache coherence determine when old translations are invalidated.

Immutable or sealed content simplifies versioning but does not remove memory-error, reclaim, or integrity obligations.

### Reclaim

Clean, unpinned, eligible cache folios can be removed and later refilled. Mapped entries require unmapping and TLB invalidation; dirty entries require successful preservation or legal discard first.

Refault feedback reveals pages reclaimed too soon. Scanning repeatedly mapped, pinned, or private-data-blocked folios wastes CPU and signals eligibility problems.

### References and mapping counts

Page-cache ownership, PTE mappings, private filesystem data, pins, I/O, lookup users, and LRU membership can each affect lifecycle. Reference count is therefore not a substitute for map count or dirty state.

Freeing requires the exact implementation's terminal predicate. Diagnostic counters must use balanced acquisition and release units, especially for large folios.

### Memory accounting and fairness

Shared cache may be populated by one cgroup and heavily used by another. Ownership can remain with the instantiator or migrate under policy, creating observable fairness effects.

Report charge, active users, reclaim source, refaulting user, and protection scope. Equal eviction counts do not imply equal service impact.

### NUMA and locality

A shared folio occupies one node at a time while consumers can run across nodes. Replication, migration, or remote access trade memory capacity against latency and bandwidth.

Migration must preserve mappings, references, writeback, and filesystem identity. Machine-wide hit rate can hide expensive remote hits.

### Pressure and thrashing

Cache should expand into otherwise idle memory and contract under competing demand. Bad balance can either starve anonymous working sets or discard hot file content repeatedly.

Measure scans, evictions, refaults, I/O, PSI, and workload latency by type and domain. A high hit ratio can coexist with disastrous misses if the rare path dominates tail latency.

### Observability and experiments

Record lookups, hit and miss bytes, fill latency and errors, folio sizes, readahead issued and used, mapped and referenced state, dirty bytes and age, writeback submission and completion, invalidation, eviction, refault, direct and DAX paths, charges, NUMA, and application latency.

Preserve kernel, filesystem, mount, storage, network, page and folio size, memory and cgroup limits, readahead, writeback, NUMA, file layout, access trace, cache preparation, repetitions, and raw timelines.

### Security and assurance

Stable identity, range checks, zero-fill, integrity verification, execute policy, stale-extent rejection, and exact reference lifetimes prevent cross-file or cross-tenant disclosure. Cache diagnostics can reveal access patterns and require access control.

Adversaries can create alias storms, sparse files, dirty floods, random readahead, truncate races, pin leaks, hash failures, and refault churn. Bound work, memory, I/O, retries, and failure amplification.

## Definitions and Notation

Let cached entry `E=(F,i,n,v,s,g,O)` have file identity `F`, base-page index `i`, span `n`, content version `v`, state `s`, generation `g`, and ownership evidence `O`. It covers logical byte range `[iP,(i+n)P)` for base-page size `P`.

State set includes `absent`, `allocating`, `filling`, `uptodate`, `dirty`, `writeback`, `invalidating`, `error`, and `reclaimable`; some properties may coexist rather than forming one scalar enumeration. Let `H_t(F,i)` be a usable lookup result at time `t`, and refault interval `rho` measure eviction-to-next-demand distance under a stated clock.

Coherence obligation says supported shared cached accesses to current `(F,x)` resolve to compatible `v`; private COW version `v_p` is not part of that shared update relation.

## Mechanisms, Invariants, or Proof Structure

A reviewable page-cache design follows twelve obligations:

1. Define stable file and range identity, folio overlap rules, version, and generation.
2. Publish at most one authoritative cache entry for each covered current range.
3. Balance lookup, cache, mapping, I/O, private-data, pin, and transient references.
4. Expose content as uptodate only after complete fill, zeroing, and required integrity checks.
5. Make supported shared mapped and buffered paths converge on coherent cache versions.
6. Track dirtying during writeback and surface completion errors through defined ownership.
7. Coordinate direct I/O, DAX, truncate, holes, remap, remote invalidation, and executable use.
8. Revalidate mapping and extent generations after every I/O, allocation, or unlocked wait.
9. Unmap and invalidate translations before reclaim or reuse can expose stale content.
10. Bound allocation, readahead, dirty growth, writeback, reclaim scans, retries, and cache metadata.
11. Account shared use, NUMA placement, cgroup ownership, and fairness explicitly.
12. Test state transitions, concurrency, overload, integrity, and recovery with preserved raw evidence.

The executable toy illustrates a unified cached page serving two reads, one shared update, and later writeback.

<!-- bijux-verify: {"id":"shared-page-cache","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"reads=B,C cache-fills=1\ncached=ABXD backing=ABCD dirty=0\nafter-writeback backing=ABXD dirty=none\n","stderr":""}} -->
```python
page_size = 4
backing = {0: bytearray(b"ABCD"), 1: bytearray(b"EFGH")}
cache = {}
dirty = set()
cache_fills = 0

def get_page(index):
    global cache_fills
    if index not in cache:
        cache[index] = bytearray(backing[index])
        cache_fills += 1
    return cache[index]

def read_byte(offset):
    page = get_page(offset // page_size)
    return chr(page[offset % page_size])

def shared_write(offset, value):
    index = offset // page_size
    page = get_page(index)
    page[offset % page_size] = ord(value)
    dirty.add(index)

first = read_byte(1)
second = read_byte(2)
print(f"reads={first},{second} cache-fills={cache_fills}")
shared_write(2, "X")
print(f"cached={cache[0].decode()} backing={backing[0].decode()} dirty={min(dirty)}")
for index in sorted(dirty):
    backing[index] = bytearray(cache[index])
dirty.clear()
print(f"after-writeback backing={backing[0].decode()} dirty={'none' if not dirty else 'present'}")
```

The toy serializes one fixed-size cache, assumes successful complete I/O, and has no mappings, folios, locks, versions, readahead, partial writes, errors, eviction, persistence, filesystem, network, or security behavior.

## Alternatives and Trade-Offs

- A unified page cache improves mapped and buffered coherence but centralizes cross-subsystem complexity.
- Separate caches can simplify components but require explicit synchronization and risk stale duplicates.
- Base-page entries minimize unused read and dirty amplification but increase metadata and locking.
- Large folios amortize lookup and I/O but can waste memory and complicate partial updates.
- Aggressive readahead raises sequential throughput but pollutes cache on random or sparse access.
- Conservative readahead preserves memory but can leave storage latency on the demand path.
- Early writeback controls dirty growth but can issue small, inefficient writes.
- Delayed writeback batches I/O but increases memory pressure and failure exposure.
- Global cache policy shares capacity efficiently but complicates tenant ownership and fairness.
- Per-domain policy improves isolation but can duplicate content or strand capacity.
- Direct I/O avoids cache copies but requires coherence and alignment coordination.
- DAX removes normal cache pages but transfers fault, persistence, and media-error complexity elsewhere.

## Failure Modes and Misconceptions

1. **“The page cache is a process address space.”** it is keyed by file content, not one process's virtual addresses.
2. **“Pathname identifies a cache page.”** rename and hard links show why stable file identity is required.
3. **“One reference count describes sharing.”** cache, mappings, pins, I/O, and transient users differ.
4. **“Present means uptodate.”** allocated or filling entries may not contain valid content.
5. **“Dirty means durable.”** dirty records pending propagation.
6. **“Writeback submission means clean.”** completion and concurrent redirtying remain.
7. **“Mapped and buffered I/O need separate copies.”** a unified cache normally serves both.
8. **“Direct I/O never affects cache.”** coherence can require writeback and invalidation.
9. **“Truncate only changes file size.”** cached folios and process mappings must be invalidated.
10. **“More readahead is faster.”** unused reads consume bandwidth and evict useful content.
11. **“Higher hit ratio proves improvement.”** byte weighting, miss latency, and workload output matter.
12. **“Large folios are only an optimization.”** they change allocation, I/O, dirty, and reclaim units.
13. **“Shared cache has obvious ownership.”** producer, user, mapper, and refaulter can differ.
14. **“Passing read/write tests proves correctness.”** races, failures, reclaim, integrity, and recovery remain.

## Worked Examples

### Example 1

Two hard links open the same inode and read the same offset. Stable file identity leads both lookups to one cache entry even though pathname strings differ.

### Example 2

Two threads miss the same absent index and allocate candidates. Atomic cache insertion selects one; the loser releases its allocation and takes a reference to the winner.

### Example 3

A reader finds a locked filling folio. It waits with a reference, then checks uptodate and error state; it never consumes partially transferred bytes.

### Example 4

A shared mapped store changes byte 50. A later buffered read observes the dirty cached byte before writeback, demonstrating coherence but not persistence.

### Example 5

A writer modifies a folio while its earlier version is under writeback. Redirty tracking ensures completion of the old I/O does not mark the new bytes clean.

### Example 6

Readahead fetches 4 MiB for a sparse random workload that uses 8 KiB. Useful-byte and eviction metrics reveal pollution hidden by raw request throughput.

### Example 7

A truncate races a delayed fill. The invalidation generation changes, so I/O completion discards the old folio rather than reinstalling blocks beyond the new end.

### Example 8

Direct I/O targets a range containing dirty cache. The filesystem writes back or rejects the conflict, invalidates stale entries, and only then exposes direct results under its contract.

### Example 9

A network lease is revoked while clients map the file. The client invalidates relevant PTEs and cached versions before accepting a new server generation.

### Example 10

A cache policy raises hit ratio from 96% to 97%, but rare misses now wait on congested remote storage and p99.9 doubles. Tail and throughput evidence rejects the headline metric.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects concurrent indexes, range entries, references, queues, and cache replacement. [Database Engineering](../../18-database-engineering/ROADMAP.md) connects buffer pools, dirty pages, write-ahead logging, checkpoints, and recovery.

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies caches, memory ordering, DMA, TLBs, NUMA, and persistent-memory behavior. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) frames remote caches, leases, versions, invalidation, partitions, and conflict recovery.

Within this program, [OS-036](036-virtual-memory-page-replacement.md) governs eviction and [OS-038](038-memory-mapped-files.md) supplies mapping semantics; [OS-040](../ROADMAP.md), [OS-049](../ROADMAP.md), and [OS-050](../ROADMAP.md) develop pressure, crash consistency, and filesystem integration.

## References

- Linux kernel documentation, [Memory Management APIs](https://docs.kernel.org/core-api/mm-api.html), current page checked 2026-09-04. File mapping and page-cache lookup, folio allocation and locking, readahead, dirtying, writeback, invalidation, large folios, references, and errors.
- Linux kernel documentation, [Overview of the Linux Virtual File System](https://docs.kernel.org/filesystems/vfs.html), current page checked 2026-09-04. Address-space operations, read and readahead, dirty folios, write paths, invalidate and release, direct I/O, and filesystem ownership.
- Linux kernel documentation, [Locking](https://docs.kernel.org/filesystems/locking.html), current page checked 2026-09-04. Fault, page-write, invalidate, truncate, hole-punch, range-remap, folio, inode, and mapping lock relationships.
- Linux kernel documentation, [Process Addresses](https://docs.kernel.org/mm/process_addrs.html), current page checked 2026-09-04. Process VMAs, file reverse mappings, page tables, fault stability, teardown, atomicity, and cross-layer lock ordering.
- Linux kernel documentation, [Multi-Gen LRU](https://docs.kernel.org/mm/multigen_lru.html), current page checked 2026-09-04. File and anonymous generations, page-table and reverse-map aging, tiers, refault feedback, working-set estimation, and reclaim.
- Linux kernel documentation, [Network Filesystem Caching API](https://docs.kernel.org/filesystems/caching/netfs-api.html), current page checked 2026-09-04. Network cache resources, data objects, dirty state, invalidation, auxiliary data, consistency, and cache withdrawal.
- Linux kernel documentation, [fs-verity](https://docs.kernel.org/filesystems/fsverity.html), current page checked 2026-09-04. Page-cache read verification, uptodate publication, Merkle-tree data, mmap reads, errors, and authenticity scope.
- Linux man-pages project, [mincore(2)](https://man7.org/linux/man-pages/man2/mincore.2.html), current page checked 2026-09-04. Page residency observations, alignment, vector results, races, errors, and limitations.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching buffer cache, mapped files, virtual memory, locking, filesystem logging, and deliberate simplifications.

## Exercises

### Exercise 1

Design a concurrent page-cache lookup, fill, and insertion state machine. Cover duplicate misses, folio sizes, partial I/O, waiters, integrity, and cleanup.

### Exercise 2

Specify coherence among shared mappings, buffered reads and writes, direct I/O, and private COW. State supported combinations, locks, invalidation, and errors.

### Exercise 3

Design truncate, hole-punch, and extent-remap coordination with page faults, cache fill, dirty data, PTEs, and writeback.

### Exercise 4

Construct adaptive readahead and large-folio policy for sequential, random, and mixed tenants. Include feedback, fairness, and rollback evidence.

### Exercise 5

Build an assurance review for a shared cache serving local files, network files, executable mappings, and memory pressure. Cover threats, tests, evidence, and reviewers.

## Answers to the Exercises

### Answer 1

Key entries by stable file object, aligned logical index, span, and generation. Lookup takes a reference before leaving protected index traversal. On miss, allocate and charge a correctly aligned candidate, lock it, and atomically insert only if no current overlapping entry exists. A loser releases its candidate and joins the winner.

The fill path maps current backing, zeroes holes and required remainder bytes, reads all required content, performs integrity verification, records error or marks uptodate, then unlocks and wakes waiters. Partial failure never publishes uptodate. Waiters recheck state and mapping generation. Truncate or invalidation makes stale completion remove or discard its candidate. Cache, I/O, lookup, private-data, and mapping references balance on every edge.

### Answer 2

Shared mappings and buffered I/O use the same current cache folio. Mapped write faults run filesystem preparation before granting PTE write access; buffered writes stabilize the same range and mark it dirty. Readers observe coherent cache content subject to application synchronization. Private mappings break COW and do not update shared cache through their private writes.

Direct I/O first handles overlapping dirty cache and prevents concurrent cached writers, then performs I/O and invalidates or refreshes affected cache before releasing exclusion. Unsupported or misaligned combinations fail explicitly. All paths coordinate extent changes, report partial progress and errors, and invalidate CPU or device translations where required. DAX is identified as a separate supported path rather than treated as cached I/O.

### Answer 3

Acquire filesystem extent and invalidation authority in documented order. Stabilize dirty data: flush, transform, or reject according to the operation. Make the old range unavailable to new fills and mapped-write preparation, unmap affected PTEs through reverse mappings, invalidate TLBs, then remove or partially zero cached folios and change file size or extents atomically under the filesystem contract.

In-flight faults and reads carry a mapping validity generation and reference. After I/O or wait they compare it with current state; stale results are discarded. Writeback completion cannot reinsert removed backing or erase a newer dirty version. Release locks and references exactly once and surface permanent I/O or metadata failures without claiming the range transition completed.

### Answer 4

Classify streams using observed sequential runs, stride, reuse, and prior readahead consumption. Grow windows when prefetched bytes are consumed before demand stalls; shrink or disable them when bytes remain unused, are reclaimed first, or displace high-refault pages. Choose larger folios only for aligned, sufficiently contiguous demand and supported filesystems, with base-page fallback under allocation failure or pressure.

Budget speculative bytes and I/O per cgroup, file, node, and device so one streaming tenant cannot evict protected working sets. Measure useful and unused readahead bytes, demand latency, I/O amplification, allocation failure, folio sizes, eviction, refault, PSI, throughput, and p99.9 by phase. Preserve traces and configuration. Roll back when service or fairness thresholds regress even if aggregate hit ratio rises.

### Answer 5

Prove stable identity, nonoverlapping authoritative entries, fill-before-uptodate publication, zeroing, integrity-before-use, shared coherence, dirty preservation, redirty correctness, stale-generation rejection, translation invalidation, exact reference balance, bounded speculative work, and defined error reporting. State local, remote, process-crash, kernel-crash, and power-failure boundaries separately.

Inject duplicate misses, partial and failed reads, hash mismatch, shared mapped and buffered write races, redirty during writeback, truncate during fill, hole punch, direct-I/O overlap, lease revocation, network partition, mapped executable invalidation, pinned folios, reclaim and refault storms, cgroup conflicts, and count boundaries. Preserve cache state, safe mapping evidence, errors, latency, I/O, versions, and configuration. Named VM, filesystem, network, storage, architecture, security, performance, reliability, and independent-verification reviewers assess residual risk; cache tests alone do not certify end-to-end durability or distributed consistency.
