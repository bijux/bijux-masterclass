---
module_id: OS-045
program: Operating Systems
level: 1
module_number: 45
title: Buffer Cache and Page Cache
status: complete
last_verified: 2026-09-04
---

# Buffer Cache and Page Cache

## One-Page Review

### Governing question

How should an operating system cache file data and filesystem blocks so reads, writes, mappings, reclaim, and direct I/O remain coherent while balancing latency, memory pressure, throughput, and durability?

### Essential definitions

- The **page cache** stores file-backed logical ranges in memory, commonly indexed by inode and file offset.
- A **folio** is a physically, virtually, and logically contiguous group of base pages managed as one cache unit.
- A **buffer head** is a legacy Linux descriptor for a block-sized region and its mapping or I/O state within a page or folio.
- An **uptodate** range contains valid contents for its logical file offsets.
- A **dirty** range contains a newer in-memory version that requires writeback under the persistence contract.
- **Writeback** submits dirty cached state to backing storage and tracks completion and errors.
- **Read-ahead** predicts future reads and initiates cache fill before demand reaches them.
- **Reclaim** frees or repurposes memory after proving cached state is discardable or successfully written back.

### Central model, mechanism, or theorem

Index each cached unit by object identity and aligned logical range: `K=(I,[a,b),v)`, where `v` is a mapping or coherency version when required. Each subrange transitions among `absent`, `loading`, `clean`, `dirty`, `writeback`, `error`, and `invalidating`, with separate reference, lock, mapping, and pin state.

A read can use cached bytes only after verifying identity, range, mapping generation, and uptodate state. A buffered write changes cache state and records dirty ownership before returning under its contract. Writeback associates I/O completion with the exact dirty generation, persists dependent allocation metadata in order, and preserves later writes. Reclaim may discard only reproducible clean state; dirty state requires successful writeback or explicit error handling.

### Critical invariants

- One logical file range has one coherent cached content version across read, write, and shared-mapping paths.
- Partially valid folios track validity and dirtiness at sufficient granularity; invalid bytes are never returned as file data.
- Dirty state is discoverable by writeback before a writer can rely on deferred persistence.
- Writeback completion clears only the generation it submitted and cannot erase a newer concurrent write.
- Truncate, hole punch, clone, direct I/O, and mapping changes serialize with cache lookup, fill, dirtying, and invalidation.
- Reclaim never discards the sole newer copy of data or a pinned, referenced, locked, or under-I/O unit.
- Visibility in cache, writeback submission, device completion, and durable recovery are reported as distinct events.

### Common failures

Common mistakes are treating a cache hit as automatically valid, assuming a whole folio is uptodate when only one filesystem block was read, clearing dirty state after an obsolete I/O completes, mixing buffered and direct writes without invalidation, dropping dirty data during reclaim, trusting read-ahead as demanded data, using cache residency as an authorization signal, and assuming `sync_file_range`-like writeout or `msync` alone proves every metadata and directory durability requirement.

### Compact example

A four-block folio initially has only blocks zero and one uptodate. A demand read for block two cannot return stale memory; it loads that block and marks only it valid. A write dirties block one. Writeback snapshots dirty generation seven, but a racing writer advances block one to generation eight; completion for seven must not clear generation eight.

### Connections

[OS-034](034-demand-paging.md), [OS-035](035-page-faults.md), and [OS-039](039-shared-pages-and-page-cache.md) establish demand loading and shared mappings. [OS-043](043-file-allocation.md) supplies backing mappings, while [OS-046](../ROADMAP.md) and [OS-047](../ROADMAP.md) connect cache writeback to recovery.

## Governing Question

Caching makes storage fast by retaining recently used bytes and batching writes, but it creates two representations of one logical file: volatile cached state and backing state. Memory mappings, ordinary I/O, direct I/O, allocation changes, and reclaim all interact with that representation.

The governing question is how to exploit temporal and spatial locality without violating content coherence or persistence claims. The answer uses explicit cache identity, fine-grained state, synchronization, versioned writeback, bounded speculation, and pressure-aware reclaim.

## Why This Matters

Most ordinary file reads and writes pass through a page cache. Its hit rate, read-ahead, dirty limits, writeback clustering, and reclaim policy can dominate application latency and system throughput.

Cache bugs corrupt data. A stale page after direct I/O can return an old value. A truncate race can write released blocks. An improperly cleared dirty bit can lose the only new version, while a writeback error hidden from applications creates false durability.

Caches also couple workloads. One streaming scan can evict a database working set; one dirty writer can consume memory and throttle unrelated tasks. Observability and isolation therefore matter alongside correctness.

## Prerequisites and Retrieval

Review [OS-031](031-address-translation.md), [OS-034](034-demand-paging.md), [OS-035](035-page-faults.md), [OS-039](039-shared-pages-and-page-cache.md), [OS-043](043-file-allocation.md), and [OS-044](044-filesystem-free-space-management.md).

Retrieve these distinctions:

- a virtual-memory page, physical page frame, page-cache folio, filesystem block, and device sector can have different sizes;
- cache identity uses file object and logical offset, not pathname or current physical block alone;
- present, uptodate, dirty, under writeback, mapped, referenced, and pinned are independent properties;
- clean file-backed data is reproducible; dirty data is not discardable until handled;
- buffered I/O and shared mappings can observe the same cache contents;
- direct I/O bypasses ordinary cached data transfer but not coherence obligations;
- writeback completion differs from application-requested durable recovery;
- read-ahead and eviction policy affect performance, not file semantics.

## Learning Objectives

After this module, you should be able to:

1. distinguish the historical buffer cache from a unified file page cache and metadata block buffering;
2. model cache indexing, folios, per-block validity, dirtiness, locks, references, mappings, and pins;
3. trace buffered read, read-ahead, buffered write, mapped write fault, writeback, direct I/O, invalidation, and reclaim;
4. specify dirty throttling, error propagation, fairness, and memory-pressure behavior;
5. reason about block-size mismatch, large folios, holes, delayed allocation, unwritten extents, and truncation;
6. design coherent interaction among page cache, filesystem mappings, storage, and durability APIs;
7. test races, failures, performance policies, and assurance evidence.

## Core Exposition

### Historical buffer caches

Early systems often cached raw device blocks separately from file pages. Filesystem code addressed a buffer by device and block number, while virtual memory cached file-backed pages by object and offset.

Duplicating the same bytes in two caches wastes memory and requires difficult cross-cache coherence. Modern designs tend toward a unified file cache while retaining metadata or compatibility descriptors where needed.

### Unified page cache

A unified page cache lets ordinary file reads, buffered writes, and shared file mappings converge on the same cached logical content. One update becomes visible across those access paths under synchronization rules.

Device caches and filesystem metadata buffers can still exist at other layers. “Unified” describes file data identity, not the absence of every other cache.

### Cache identity

The natural key is an address-space object derived from a stable file identity plus page or folio index. A pathname is mutable, and a physical extent can move, so neither is a sufficient key.

Truncation and object reuse remove stale entries before identity can be recycled. Mapping-generation checks protect paths where logical-to-physical mappings change concurrently.

### Pages and folios

A base page is an architecture memory-management unit. A folio lets the kernel manage several contiguous base pages belonging to one file mapping as a larger unit.

Larger folios reduce lookup, lock, and I/O overhead for suitable workloads but increase fill amplification and internal state requirements. The cache must still honor file end and filesystem-block boundaries.

### Filesystem blocks inside folios

Filesystem block size can be smaller than folio size. A read error or partial write may make some blocks valid and others invalid within the same folio.

Per-block or equivalent state tracks uptodate and dirty subranges. Marking the entire folio valid before every constituent block is initialized can expose stale memory.

### Buffer heads

Linux buffer heads describe block-sized slices, mappings, locks, dirty state, and I/O completion in the legacy path. They remain important for some filesystems and metadata operations.

They add per-block objects and state transitions. Newer iomap paths can use lighter per-folio bitmaps for sub-block validity and dirtiness, but migration must preserve all semantics.

### Cache lookup

A lookup searches an index such as an xarray by folio index. A found entry can be loading, invalidating, exceptional, or stale; presence alone is not a usable hit.

The caller acquires the required reference or lock, rechecks identity and state, and waits, retries, or fails according to its blocking contract.

### Demand read

On a miss, a reader creates or joins a loading entry, resolves the current file mapping, submits I/O for mapped data, synthesizes zeros for holes, and marks only successful ranges uptodate.

Errors wake waiters and remain observable. No waiter consumes bytes before initialization and end-of-file checks complete.

### Concurrent cache fill

Two misses for the same key must not create competing authoritative folios. Insertion or an entry lock elects one loader; other readers wait or use a nonblocking result.

If mapping or size changes during I/O, completion validates the relevant generation before publishing. Obsolete data is discarded or retried.

### Read-ahead

Sequential detection can submit future ranges before demand. Window size grows on confirmed sequential access and shrinks on random access, errors, pressure, or unused prefetched data.

Read-ahead is speculative. It must obey permissions already established for the open file, file end, memory budgets, and device constraints without delaying demanded I/O excessively.

### Synchronous and asynchronous read-ahead

Synchronous read-ahead expands the miss that blocked the caller; asynchronous read-ahead starts when demand reaches a trigger inside an existing window. Both attempt to overlap storage latency.

Metrics distinguish useful prefetched hits from unused pages, demand latency, I/O amplification, and cache pollution. A high raw read-ahead volume is not success.

### Buffered writes

A buffered write finds or instantiates folios, initializes untouched portions needed for partial-block correctness, copies caller bytes, updates size and mapping reservations, then marks affected subranges dirty.

Dirty publication is ordered after data modification so writeback cannot miss new bytes. The syscall may return before allocation, device I/O, or durability.

### Partial writes

A write covering only part of a filesystem block may require reading existing bytes or zeroing new-space boundaries. Short copy or fault must dirty only bytes actually accepted and release unused delayed-allocation reservations.

The implementation avoids exposing uninitialized portions and preserves prior bytes outside the write range.

### Shared writable mappings

A write fault on a shared file mapping obtains a writable cached folio, validates size and permissions, handles copy-on-write or allocation as required, and marks it dirty through the filesystem protocol.

CPU stores can occur after the initial fault, so dirty tracking and write protection must catch the transition. Unmap and truncate synchronize with active mappings.

### Dirty state

Dirty means cached contents or related state are newer than backing storage and require writeback. It does not mean I/O is currently running or that persistence will succeed.

Dirty tags let background scanners find work without scanning every clean entry. Ordering ensures a dirty range becomes discoverable before memory barriers permit dependent completion.

### Dirty accounting

Systems account dirty memory globally and per backing device, workload, or control group. Thresholds start background writeback and eventually throttle writers.

Accounting includes pages temporarily under writeback according to policy and reconciles on redirty, truncation, error, and completion. Approximate counters guide policy; exact state governs data safety.

### Dirty throttling

Without throttling, writers can fill memory faster than storage drains it, causing long stalls and reclaim deadlocks. Proportional throttling spreads delay before a hard limit.

Fairness considers device bandwidth and write origin. A slow backing device should not necessarily throttle unrelated clean-cache workloads to the same degree.

### Writeback selection

Background, periodic, reclaim-driven, and explicit synchronization can initiate writeback. Selection considers age, dirty amount, byte range, device congestion, cgroup ownership, and sync mode.

Clustering adjacent logical and physical ranges reduces requests. It must respect mapping boundaries, write ordering, atomicity, and zones.

### Writeback state machine

Writeback locks or otherwise stabilizes a folio, snapshots dirty subranges and generation, resolves stable mappings, clears or transfers dirty accounting according to protocol, marks I/O in flight, and submits requests.

Completion records success or error, performs required unwritten-extent conversion or metadata work, ends writeback, and wakes waiters. New dirtiness during I/O remains visible.

### Redirty races

A writer can modify a folio while an older version is under writeback if the filesystem permits it. Completion for generation `g` cannot declare generation `g+1` clean.

Separate dirty bits, sequence numbers, locks, or write-protection protocols identify what the I/O covered. This is an instance of the lost-update problem.

### Writeback errors

Device or mapping failures are recorded against the address space and observed by applicable file handles or synchronization calls. Clearing a dirty tag to avoid endless retry does not justify hiding the error.

Error-sequence designs let each observer detect failures since its last sample. Applications still must check write, flush, synchronization, and close outcomes under the platform contract.

### Holes and zero fill

Reading a hole fills cache bytes with logical zeros without device data. Writing a hole reserves or allocates storage and prevents stale physical contents from becoming visible.

Cache entries do not turn holes into durable allocations by themselves. Extent mapping and writeback coordinate final placement.

### Delayed allocation

Dirty cached data can exist with a reservation but no physical address. Writeback chooses placement, creates allocated or unwritten mappings, submits data, and commits conversions.

Cache reclaim must understand these reservations. Discarding a clean-after-error folio also releases only the unused reservation ranges owned by that write.

### Truncation

Shrinking a file changes size, excludes new access beyond end, waits for or cancels conflicting I/O, invalidates cached folios, zeros a retained partial block, and removes mappings.

Ordering prevents an old writeback completion from restoring data beyond new end or writing a block already reassigned elsewhere.

### Hole punch and range changes

Punch, collapse, insert, clone, and unshare change logical mappings beneath cached offsets. They take an invalidation lock or equivalent protocol against cache insertion, mapping, and I/O.

Partial boundary state is preserved or zeroed, and affected cached pages are invalidated or remapped before physical storage changes ownership.

### Direct I/O coherence

Direct I/O transfers between user buffers and storage without using the ordinary page-cache data path. Dirty overlapping cached ranges are flushed, and stale clean ranges are invalidated under filesystem rules.

Direct writes commonly invalidate before and after I/O to close races. If coherent invalidation cannot be obtained in a nonblocking path, the operation retries, falls back, or returns a documented error.

### Memory-mapped coherence

Shared mappings expose cached folios through process page tables. Buffered writes update the same logical cache, while invalidation must unmap or otherwise revoke stale translations.

Private mappings follow virtual-memory copy-on-write rules and do not ordinarily publish private changes to the file. The two forms require different dirty and reclaim accounting.

### Cache invalidation

Invalidation prevents new references, removes page-table mappings when needed, waits for pins or I/O, and erases index entries only when no caller can use them.

A failure to invalidate must be handled explicitly. Proceeding to reuse backing blocks while stale cache references remain risks cross-file corruption.

### References and pins

Index membership, callers, page tables, I/O, DMA, and long-term pins can each retain a folio. Reference counts protect lifetime; locks and state protect contents.

Pinned cache can block truncate, migration, reclaim, and filesystem operations. Systems observe and bound long-term pins rather than assuming all cache is reclaimable.

### Reclaim

Clean, unmapped, unreferenced cache is cheap to discard because backing storage can reproduce it. Dirty folios require writeback; locked, pinned, or congested folios are skipped or handled carefully.

Background reclaim maintains watermarks. Direct reclaim makes an allocating task perform work and can create latency spikes or recursion constraints in filesystem code.

### Replacement policy

LRU approximations, active/inactive generations, access bits, frequency estimates, and workload isolation decide which entries to scan. Sequential one-use data should not evict repeatedly reused working sets.

No policy predicts all workloads. Correctness is invariant under replacement choice; performance claims require representative traces and memory-pressure levels.

### Metadata cache reclaim

Inodes, dentries, buffer heads, extent nodes, and other filesystem metadata also consume memory. Shrinkers reclaim reconstructible objects while respecting references, dirty state, locks, and filesystem recursion constraints.

Dropping data pages alone may not relieve metadata-heavy pressure. Observability separates data cache, metadata caches, dirty, writeback, and pinned memory.

### Read advice

Application advice can identify sequential, random, soon-needed, or no-longer-needed ranges. It is a performance hint, not a content, scheduling, or durability guarantee.

Advice is interpreted against alignment and current residency. Dropping a dirty range still requires writeback or retains it; a hint cannot discard data unsafely.

### Residency queries

Interfaces such as `mincore` can report whether pages of a mapping are resident at an observation instant. Residency can change immediately and does not prove validity, physical placement, or future latency.

Access may be restricted because residency reveals side-channel information. Applications do not use it as an authorization or correctness condition.

### Synchronization boundaries

`fsync`, `fdatasync`, `msync`, whole-filesystem sync, and range-writeout interfaces have different data, metadata, waiting, and error contracts. Some interfaces initiate I/O without establishing crash durability.

Callers choose the primitive matching their recovery requirement and include directory synchronization for durable namespace publication where required.

### Device write caches

Filesystem writeback can reach a device queue while volatile controller caches still hold data. Flush and force-unit-access semantics connect completion ordering to the declared stable-storage model.

The page cache cannot compensate for a device that violates its advertised ordering or persistence contract. Fault tests include power-loss behavior at lower layers.

### Network filesystems

Client page caches interact with server caches, leases, delegations, attribute caching, and writeback acknowledgments. Close-to-open or stronger models determine when another client observes changes.

Writeback success at one layer may not mean server stable storage. Reconnect, conflict, credential, and lost-error handling are part of the filesystem contract.

### Observability and experiments

Record inode and range, hit or miss, folio and block sizes, validity and dirty masks, read-ahead cause, mapping version, lock wait, reclaim scan, writeback generation, bytes, device, latency, error sequence, synchronization, and recovery result.

Preserve memory size, pressure, filesystem, mount, device, workload seed, access trace, kernel version, and raw outputs. Cache-warm performance and crash durability require different evidence.

### Security and assurance

Adversarial tests race fill, write, mmap fault, truncate, punch, clone, direct I/O, invalidation, reclaim, writeback completion, object reuse, and unmount. Inject short I/O, corruption, stale mappings, pinning, memory pressure, and power loss.

Assurance names VM, VFS, filesystem, storage, concurrency, security, recovery, performance, and independent-verification reviewers. A high cache-hit ratio cannot certify coherence or durability.

## Definitions and Notation

Let stable file identity be `I`, folio size `P`, filesystem-block size `B`, and aligned cache interval `X=[kP,(k+1)P)`. Cache key `K=(I,k,v)` includes mapping version `v` when the protocol requires it.

For each block subrange `j`, state `S_t(K,j)` is one of `absent`, `loading`, `clean`, `dirty(g)`, `writeback(g)`, `error(e)`, or `invalidating`. Let `ref_t`, `map_t`, `pin_t`, and `io_t` count relevant lifetime constraints.

A usable hit requires matching identity and version, range within current file size, uptodate state for every requested byte, and a retained reference under the synchronization protocol. Presence alone is insufficient.

Define safe clean eviction only when no dirty generation exists, no I/O or invalidation conflict exists, and references, mappings, and pins satisfy the reclaim contract. Define durability separately over data, file metadata, device completion, and namespace metadata.

## Mechanisms, Invariants, or Proof Structure

1. **Bind cache identity.** Resolve stable object, logical range, size, and mapping generation rather than pathname or physical block alone.
2. **Elect one state owner.** Insert, lock, or join loading and mutation state so competing operations cannot publish incompatible folios.
3. **Validate every byte.** Track per-folio or per-block uptodate state and initialize holes and partial boundaries before exposure.
4. **Publish dirtiness.** Order data changes, dirty tags, reservations, size, and discoverability so writeback cannot miss accepted writes.
5. **Serialize mapping changes.** Coordinate truncate, punch, clone, direct I/O, mmap, allocation, invalidation, and cache insertion.
6. **Version writeback.** Associate submission and completion with exact dirty and mapping generations; preserve redirtied state.
7. **Propagate failure.** Retain address-space errors until every entitled observer can detect them through the documented API.
8. **Reclaim safely.** Evict only reproducible state with acceptable references, maps, pins, locks, and I/O; throttle or write back otherwise.
9. **Bound speculation and pressure.** Adapt read-ahead, dirty memory, local caches, and scan work without starving demand or forward progress.
10. **Order persistence.** Connect cache writeback to allocation metadata, filesystem commit, device flush, and namespace durability.
11. **Recover coherently.** After crash, expose only data and mappings justified by the persistence protocol and report lost writes honestly.
12. **Preserve evidence.** Retain state transitions, generations, ranges, I/O, errors, pressure, synchronization, crash points, and limitations.

<!-- bijux-verify: {"id":"page-cache-block-state","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial valid=1100 dirty=0000\nafter-read valid=1110 dirty=0000\nafter-write valid=1110 dirty=0100 generation=8\ncomplete-generation=7 remains-dirty=True\ncomplete-generation=8 remains-dirty=False\n","stderr":""}} -->
```python
valid = [True, True, False, False]
dirty_generation: list[int | None] = [None, None, None, None]


def bits(values: list[bool]) -> str:
    return "".join("1" if value else "0" for value in values)


print(f"initial valid={bits(valid)} dirty={bits([g is not None for g in dirty_generation])}")
valid[2] = True
print(f"after-read valid={bits(valid)} dirty={bits([g is not None for g in dirty_generation])}")
dirty_generation[1] = 8
print(f"after-write valid={bits(valid)} dirty={bits([g is not None for g in dirty_generation])} generation=8")
for completed in (7, 8):
    if dirty_generation[1] == completed:
        dirty_generation[1] = None
    print(f"complete-generation={completed} remains-dirty={dirty_generation[1] is not None}")
```

The executable model demonstrates sub-folio validity and generation-aware dirty completion. It omits actual bytes, locks, mappings, I/O, errors, reclaim, durability, and real kernel behavior.

## Alternatives and Trade-Offs

- Separate block and page caches simplify some subsystems but duplicate data and coherence work; a unified cache reduces duplication but couples VM and filesystem behavior.
- Base-page cache units limit read amplification but increase index and lock overhead; large folios reverse the trade-off.
- Per-block state handles block-size mismatch precisely but costs memory and transitions; whole-folio state is cheaper only when semantics permit it.
- Aggressive read-ahead hides latency for sequential access but pollutes cache and storage queues for random access.
- Write-behind batches and reorders I/O for throughput but delays failures and persistence.
- Low dirty limits smooth latency but throttle bursts; high limits absorb bursts but can create long writeback stalls.
- Global replacement uses memory flexibly but permits interference; per-workload protection improves isolation but can strand cache.
- Direct I/O avoids cache copying and pollution but adds alignment, invalidation, and mixed-access coherence costs.
- Buffer heads retain mature filesystem support but add per-block overhead; iomap-style folio state centralizes common paths but requires careful migration.
- Eager invalidation simplifies reuse but stalls on pins; deferred invalidation improves concurrency but extends state and recovery complexity.
- Synchronous writeback simplifies some error timing but sacrifices batching; asynchronous writeback requires durable error observation.
- Dropping caches makes cold experiments reproducible but is disruptive and does not represent steady-state production behavior.

## Failure Modes and Misconceptions

- **“Present means valid.”** A folio can be loading, partially uptodate, stale, invalidating, or erroneous.
- **“One valid block makes the folio uptodate.”** Every requested byte needs initialized state.
- **“Dirty means writeback is running.”** Dirty and under-writeback are distinct states.
- **“I/O completion can clear dirty unconditionally.”** It can cover an older generation than a racing write.
- **“A write returning means data reached storage.”** Buffered writes commonly return after dirtying memory.
- **“Clean cache is always evictable.”** References, mappings, pins, locks, and in-flight I/O can prevent eviction.
- **“Read-ahead changes semantics.”** It is bounded speculation and cannot replace demand validation.
- **“Direct I/O has no cache interaction.”** Overlapping dirty state must be flushed and stale state invalidated.
- **“Private mmap writes dirty the file.”** Private mappings normally create process-private copy-on-write state.
- **“Dropping cache drops dirty data.”** Safe reclaim writes it back or retains and reports failure.
- **“Range writeout proves crash durability.”** Interface waiting, metadata, and flush contracts differ.
- **“Residency predicts the next read.”** It is an instantaneous, race-prone observation.
- **“Cache hit rate alone measures quality.”** latency, amplification, fairness, pressure, and correctness also matter.
- **“Local cache tests prove distributed coherence.”** Server caches, leases, reconnect, and stable-write semantics differ.

## Worked Examples

### Example 1

A 16 KiB folio contains four 4 KiB filesystem blocks. A failed read of block three leaves the other successful blocks valid without exposing bytes from block three.

### Example 2

Two threads miss the same file offset. One installs a loading folio; the other joins it, preventing two I/O completions from racing to publish different contents.

### Example 3

A sequential reader triggers a growing read-ahead window. When it seeks randomly, unused-prefetch feedback shrinks the window and protects other working sets.

### Example 4

A partial buffered write faults while copying user bytes. Only the accepted range becomes dirty, and the filesystem releases delayed-allocation reservations for clean untouched ranges.

### Example 5

Writeback submits generation seven. A writer produces generation eight before completion; the old success ends its I/O but leaves the folio dirty for generation eight.

### Example 6

Direct overwrite of a cached range first flushes dirty cached bytes and invalidates clean aliases. Post-I/O invalidation prevents a racing fill from surviving with old storage contents.

### Example 7

Truncate shrinks below an in-flight cached write. Size and invalidation synchronization prevent completion from restoring the removed mapping or exposing the old tail after extension.

### Example 8

Memory pressure scans a clean sequential page and a dirty pinned database page. It evicts the reproducible clean page and skips the pinned one rather than discarding newer data.

### Example 9

A device returns an error during asynchronous writeback. The address-space error sequence advances, and a later `fsync` on an entitled handle reports the failure.

### Example 10

A client cache holds modified data acknowledged locally but not stable at a remote server. Its durability claim waits for the filesystem's stable-write protocol, not merely local page-cache completion.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects indexed caches, reference counts, state machines, replacement structures, and sequence validation. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects locality, memory hierarchies, cache lines, DMA, persistence, and device ordering.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects client caches, leases, invalidation, consistency, and stable writes. [Security Engineering](../../25-security-engineering/ROADMAP.md) frames stale-data disclosure, residency side channels, pinning abuse, and error integrity.

Within this program, [OS-034](034-demand-paging.md), [OS-039](039-shared-pages-and-page-cache.md), [OS-043](043-file-allocation.md), and [OS-044](044-filesystem-free-space-management.md) supply memory and storage foundations; [OS-046](../ROADMAP.md) and [OS-047](../ROADMAP.md) complete persistence and recovery reasoning.

## References

- Linux kernel documentation, [Memory Management Concepts](https://docs.kernel.org/admin-guide/mm/concepts.html), current page checked 2026-09-04. Page cache, dirty file data, reclaimable and unreclaimable memory, background and direct reclaim, and memory watermarks.
- Linux kernel documentation, [Overview of the Linux Virtual File System](https://docs.kernel.org/filesystems/vfs.html), current page checked 2026-09-04. Inodes, address spaces, page-cache operations, dirty inode handling, writeback, eviction, filesystem sync, and cache shrinkers.
- Linux kernel documentation, [Buffer Heads](https://docs.kernel.org/filesystems/buffer.html), current page checked 2026-09-04. Block descriptors, mapping and I/O state, dirty ordering, page dirtiness, writeback helpers, and legacy filesystem integration.
- Linux kernel documentation, [iomap Library Design](https://docs.kernel.org/filesystems/iomap/design.html), current page checked 2026-09-04. Mapping states, page-cache invalidation lock, folio locking, direct and buffered operation flags, mappings, and coherency responsibilities.
- Linux kernel documentation, [iomap Supported File Operations](https://docs.kernel.org/filesystems/iomap/operations.html), current page checked 2026-09-04. Per-block folio state, reads, read-ahead, buffered writes, mapped faults, delayed-allocation cleanup, writeback, direct I/O, and errors.
- Linux kernel documentation, [VM sysctl documentation](https://docs.kernel.org/admin-guide/sysctl/vm.html), current page checked 2026-09-04. Dirty background and foreground thresholds, expiration, writeback intervals, laptop mode, reclaim, and pressure controls.
- Linux man-pages project, [posix_fadvise(2)](https://man7.org/linux/man-pages/man2/posix_fadvise.2.html), current page checked 2026-09-04. Normal, sequential, random, needed, and no-reuse or no-longer-needed access advice and page-cache effects.
- Linux man-pages project, [readahead(2)](https://man7.org/linux/man-pages/man2/readahead.2.html), current page checked 2026-09-04. Initiating file read-ahead, page-cache population intent, descriptor requirements, alignment, blocking caveats, and errors.
- Linux man-pages project, [msync(2)](https://man7.org/linux/man-pages/man2/msync.2.html), current page checked 2026-09-04. Synchronizing mapped file ranges, asynchronous and synchronous modes, invalidation, alignment, and errors.
- Linux man-pages project, [mincore(2)](https://man7.org/linux/man-pages/man2/mincore.2.html), current page checked 2026-09-04. Snapshot-like page residency reporting, alignment, vector interpretation, races, and portability limits.

## Exercises

### Exercise 1

Specify a cache state machine for miss, concurrent fill, partial validity, buffered write, writeback, redirty, error, invalidation, and eviction.

### Exercise 2

Design read-ahead and replacement policies for mixed sequential, random, mapped, and multi-tenant workloads. State evidence and correctness boundaries.

### Exercise 3

Specify buffered writeback with delayed allocation, dirty throttling, mapping versions, partial failure, error observation, synchronization, and recovery.

### Exercise 4

Design coherent interaction among buffered I/O, shared and private mappings, direct I/O, truncate, hole punch, clone, and long-term pins.

### Exercise 5

Build a test and assurance plan for data and metadata caches under pressure. Include races, devices, remote filesystems, crashes, performance, and reviewers.

## Answers to the Exercises

### Answer 1

Key by stable object and aligned logical range, with mapping generation where remapping can race. On miss, atomically install a loading entry or join its waiters. The loader resolves the mapping, reads data or synthesizes holes, marks only initialized subranges valid, records errors, and wakes waiters. A buffered writer stabilizes the folio, initializes untouched required bytes, copies accepted data, publishes a new dirty generation and searchable tag, then releases it.

Writeback snapshots generation and dirty mask, validates mappings, starts I/O, and on completion clears only covered unchanged generations; redirtied bytes remain dirty. Errors advance an observer-visible sequence. Invalidation blocks insertion and access, revokes mappings, waits for I/O or pins under policy, and removes the index entry only after references are safe. Eviction accepts clean reproducible state with no disallowed reference, mapping, pin, lock, I/O, or invalidation state.

### Answer 2

Track per-stream sequentiality and useful-prefetch feedback. Start with a small window, grow after demanded hits near its trigger, shrink on seeks, unused pages, pressure, or device congestion, and prioritize demand over speculation. Replacement protects repeatedly reused entries from one-pass scans, attributes memory to workloads, and provides bounded global reclaim so idle partitions cannot strand memory.

Replay traces combining sequential scans, random databases, executable and mapped access, small-file metadata, and multiple tenants across memory sizes and devices. Measure demand latency, useful and unused prefetched bytes, storage amplification, hit ratios, eviction reuse distance, CPU, fairness, and tail stalls. Validate contents independently: any policy may change timing and residency but never returned bytes, dirty retention, access control, or persistence semantics.

### Answer 3

Validate range and reserve quota, space, and mapping metadata before accepting dirty state under a strong delayed-allocation contract. Copy bytes into valid folios, update size, assign a dirty generation, tag the address space, and charge dirty memory to the writer and backing device. Background thresholds start writeout; proportional limits throttle producers before reclaim loses forward progress.

Writeback snapshots subranges and generation, converts delayed reservations to stable unwritten or mapped extents, submits initialized data, and completes filesystem metadata work. Partial failure releases only unused reservations, retains or explicitly clears state according to retry policy, and advances the error sequence. A concurrent write receives a later generation that old completion cannot clear. `fsync` waits for applicable data and metadata, filesystem commit, and device persistence under the contract and reports errors since the observer's prior sample. Crash recovery exposes only committed mappings and justified data.

### Answer 4

Buffered reads, writes, and shared mappings use one logical cache; private mappings create process-private copy-on-write pages. Shared write faults validate size and permissions and enter the filesystem dirty protocol. Direct reads flush overlapping dirty cache first; direct writes flush and invalidate overlapping cache before I/O and invalidate again afterward or fail when coherence cannot be established.

Truncate and punch exclude new cache insertion, revoke shared mappings, wait for conflicting I/O and pins under documented policy, zero partial boundaries, invalidate affected folios, then change file mappings and release blocks. Clone and unshare coordinate cached dirty data with source and destination mapping generations. Long-term pins can block these transformations; APIs bound, reject, or explicitly manage them instead of reusing backing storage beneath a live pin.

### Answer 5

Exercise cold and warm reads, sequential and random traces, partial-block I/O, holes, delayed allocation, large folios, mmap shared and private writes, direct and buffered overlap, truncate, punch, clone, unshare, read-ahead hints, residency queries, dirty throttling, background and direct reclaim, metadata shrinkers, long-term pins, unmount, device congestion, short I/O, error sequences, and remote lease or reconnect behavior.

Inject races at lookup, fill, dirty publication, mapping change, invalidation, writeback submission and completion, redirty, reclaim, and object reuse. Inject crashes before and after filesystem commit and device flush, then compare recovered data to the declared durability point. Measure demand latency, hit and useful-prefetch ratios, dirty age, writeback bandwidth, scan cost, stalls, amplification, CPU, and fairness. Preserve kernels, filesystems, mounts, devices, memory limits, seeds, traces, raw outcomes, and limitations. Named VM, VFS, filesystem, storage, concurrency, security, recovery, distributed-systems, performance, and independent-verification reviewers assess claims.
