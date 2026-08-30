---
module_id: DBE-021
program: Database Engineering
level: 1
module_number: 21
title: Pages, Blocks, and Database Files
status: complete
last_verified: 2026-08-30
---

# Pages, Blocks, and Database Files

## One-Page Review

### Governing question

How does a database translate logical relation addresses into bounded page and file operations while preserving layout, allocation, durability, integrity, and recoverability across the storage stack?

### Essential definitions

A database **page** is the engine's unit of managed in-memory and persistent data transfer. A **logical block number** identifies a page within a relation or storage object. A **segment** is one file in a size-bounded sequence representing that object. A **tablespace** maps logical database ownership to storage locations. A page commonly contains a header, item/slot directory, free space, records, and access-method-specific space. An **extent** groups pages for allocation. A **torn page** contains only part of an intended page write. A **checksum** detects some corruption; it does not repair data or prove durability.

### Central model, mechanism, or theorem

For fixed page size `P` and `N` pages per segment, logical block `b` maps to segment `floor(b/N)`, page index `b mod N`, and byte offset `(b mod N)*P`. A page layout is valid when all offsets are within `[0,P]`, header/directory grow upward, records/special area grow downward, and `lower <= upper <= special <= P`. A logical page write crosses database buffers, system calls, OS cache, filesystem, controller, and device; success at an upper layer is not durable completion unless the engine's documented flush/order protocol reaches the required failure boundary.

### Critical invariants

- Page size, format version, checksum mode, byte order, and relation/file identity are discovered from authoritative metadata.
- Logical block translation uses engine/version rules; filenames are not stable user-level table identity.
- Page regions never overlap and every pointer, length, alignment, and special-area boundary stays in range.
- Allocated, initialized, dirty, flushed, durable, free, reusable, and OS-reclaimed space are distinct states.
- A checksum mismatch is corruption evidence; a checksum match is not proof of correct semantics or complete durability.
- WAL/journal ordering and page writes follow the target engine's documented recovery protocol.
- Physical backup copies a consistent state with every required log, metadata, and auxiliary file.
- Forensics occurs on protected copies using version-matched tools; production files are never hand-edited.

### Common failures

Failures include equating database page size with OS page, filesystem block, or device sector; assuming one table means one file; computing offsets without segment/fork rules; trusting sparse-file apparent size as allocated space; treating deleted space as returned to the OS; editing relation files while the server runs; believing `write()` or rename alone guarantees durability; disabling checksums to hide corruption; restoring a data file without matching log/control state; reading page bytes with the wrong engine version or endianness; and interpreting cache hit rate without workload or page residency evidence.

### Compact example

With 8192-byte pages and four pages per pedagogical segment, block 7 maps to segment 1, page index 3, byte offset 24576. Eleven logical pages occupy two full 32768-byte segments plus one 24576-byte segment, totaling 90112 logical bytes. A page with 24-byte header, three 4-byte item identifiers, and aligned payloads 104, 200, and 56 bytes has `lower=36`, `upper=7832`, and 7796 free bytes. A one-byte change alters the toy checksum, demonstrating detection but not repair.

### Connections

[DBE-010](010-life-of-a-transactional-write.md) traces a write through buffers, logs, and durable commit. [DBE-022](../ROADMAP.md) examines record/tuple representation inside pages; subsequent modules cover slotted pages, free-space maps, buffer pools, replacement, prefetch, and storage observability.

## Governing Question

SQL presents relations and rows, while storage engines manipulate pages and files. Between them sits an address and format contract: which logical object owns a page, where its bytes live, how free space is represented, when a changed page becomes durable, and how damage is detected and recovered. Confusing any layer can turn a diagnostic command into corruption.

The governing question is not “what is the page size?” It is how fixed-size database pages interact with variable-length records, multiple files and auxiliary forks, allocation metadata, buffer management, write-ahead logging or journaling, operating-system caches, device atomicity, checksums, backups, and versioned formats. The answer is engine- and version-specific at the byte level, but the invariants are general.

## Why This Matters

Page organization determines I/O amplification, cache reach, scan cost, index fanout, update placement, fragmentation, and recovery units. A small row can require a full-page read. A random update can dirty a page containing many unrelated rows. A page split or relation extension can produce latency spikes. Wide values may overflow to separate storage and turn one logical fetch into several physical reads.

Reliability also lives here. Power loss can interrupt a page write. A controller can acknowledge data still held in volatile cache. Bit rot, firmware faults, memory errors, cables, filesystems, or operator mistakes can corrupt bytes. WAL and journals support recovery only under their documented ordering and storage assumptions. Checksums improve detection but do not identify the correct replacement page.

Capacity is not a single byte count. Logical relation size, allocated blocks, sparse extents, free space inside pages, reusable pages, WAL/journal volume, filesystem allocation, snapshots, replicas, backups, and reclaimable operating-system space differ. Production planning must measure the right layer.

## Prerequisites and Retrieval

Retrieve binary representation, bytes and offsets, powers of two, integer division/modulo, files and file descriptors, OS virtual memory, filesystem blocks/extents, sectors and atomic writes, buffering, caches, checksums, transactions, write-ahead logging, crash recovery, indexes, and backups.

Distinguish database page from virtual-memory page, filesystem block, allocation extent, and device sector; logical block from physical sector; relation from file; file length from allocated bytes; free page space from free filesystem capacity; written from flushed from durable; corruption detection from correction; crash-consistent copy from transactionally consistent backup; and format parser success from semantic validity.

## Learning Objectives

After this module, you should be able to:

1. translate logical page addresses into segment-relative byte offsets;
2. distinguish relations, forks/tablespaces, segments, files, pages, extents, and device units;
3. validate page-region offsets, lengths, alignment, and free-space invariants;
4. explain page allocation, initialization, reuse, truncation, and OS reclamation;
5. trace reads and writes through database, OS, filesystem, controller, and device caches;
6. explain torn pages and the roles of WAL/journals, full-page images, and atomicity assumptions;
7. interpret checksums as bounded detection evidence;
8. design safe physical backup, restore, and page-forensics procedures;
9. reason about page-size tradeoffs and I/O/cache amplification; and
10. gather authoritative size, allocation, integrity, I/O, and recovery evidence.

## Core Exposition

A database page is an engine-defined fixed-size byte array. PostgreSQL commonly uses an 8 KiB block size determined when built; InnoDB documents an instance page size configured at initialization; SQLite stores a database-wide page size in the file header. These facts are not interchangeable. Discover the value from the running engine/file metadata, record version/build, and never infer it from a generic default.

Operating systems also use “page,” filesystems use blocks and extents, and storage devices expose logical/physical sectors or larger internal erase units. Sizes can differ. Database I/O may be buffered, direct, vectored, or combined. Alignment requirements and atomicity guarantees belong to the exact stack; an 8 KiB database page is not automatically written atomically because the drive reports 4 KiB sectors.

A logical relation may have several physical components. PostgreSQL relations can have main and auxiliary forks and can be split into numbered segment files. InnoDB tables and indexes live in system, general, or file-per-table tablespaces; a file-per-table `.ibd` file is not “just heap rows” because clustered/secondary indexes and metadata share engine-managed structures. SQLite's primary database, rollback journal, WAL, and shared-memory files form a protocol-dependent set.

Engine filenames and identifiers are internal addresses, not durable application names. Object IDs can change after rewrite, restore, rebuild, truncate, or version-specific operations. Use supported catalogs and tools to map logical objects to physical paths. Do not construct paths from table names or move individual files between clusters.

For a simple segmented relation, logical block division yields segment and within-segment index. Real engines may use forks, tablespaces, relation generations, encryption, compression, and size limits around that mapping. Validate integer range and file length before reading. A block address without cluster identity, tablespace, relation identity, fork, and version is incomplete forensic evidence.

Inside a page, engines need metadata and records. PostgreSQL documents a header, item identifier array, free space, items, and optional special space. The header includes boundaries such as lower/upper/special and a page LSN/checksum field. Item identifiers make a stable logical slot possible even when tuple bytes move during compaction. DBE-023 develops slotted-page mechanics.

Page invariants begin with bounds. Header and slot directory must end at or before the start of free space; record payloads must fit before special space; offsets plus lengths must not overflow or overlap forbidden regions; alignment padding must be included; item states/types must be valid; version and page type must agree with the owning access method. A parser must fail closed on malformed arithmetic.

Free space is often the gap between upward-growing metadata and downward-growing payload, but reusable holes and dead items complicate the picture. “Free bytes” can mean contiguous insertion space, total reclaimable bytes after compaction, or space advertised in a separate map. The value useful to an allocator may be approximate and stale by design.

Pages have roles. Heap/table pages hold tuples or records; B-tree interior and leaf pages hold routing or data entries; overflow pages hold displaced payload; free-space/visibility/pointer maps track metadata; allocation pages track extents; undo/log areas hold recovery state. Page type determines special fields and validation rules. Do not decode an index page as a heap page.

Allocation reserves address space for future content. Engines may allocate one page, groups, or extents to reduce metadata and fragmentation. An allocated page can be uninitialized, initialized empty, partially full, full, reusable, pending cleanup, or unreachable due to corruption. File growth can reserve blocks, create sparse holes, or physically initialize bytes depending on engine/OS configuration.

Deletion usually does not shrink a file. Space can become reusable inside a page or as a free page/extent while remaining allocated to the relation/tablespace. Returning space to the operating system may require truncation, vacuum/rebuild, table move, or dropping a file-per-table object, with locks, rewrite space, WAL/log, and replication implications. “Database freed 20 GB” must state at which layer.

A sparse file's logical length can greatly exceed allocated filesystem blocks. Snapshots and copy-on-write systems can retain old extents after the live file shrinks. Compression/deduplication change physical bytes. Capacity evidence should record logical object size, file apparent size, allocated bytes, internal free/reusable bytes, snapshot retention, growth rate, and headroom.

Reads typically locate a page, consult the buffer pool, and on a miss issue storage I/O into a buffer frame. The OS/filesystem/device may add caches; direct I/O may bypass some. Readahead or database prefetch can fetch neighbors. A single logical page miss can trigger more physical bytes because of request merging, filesystem/device granularity, RAID, encryption, compression, or remote storage.

Writes usually modify an in-memory buffer and mark it dirty. A background writer/checkpointer later writes the page. Transaction commit often makes log records durable rather than forcing every dirty data page. Write-ahead means the recovery log needed to redo a page change reaches durable storage before the data page version that depends on it. Exact LSN, flush, and checkpoint rules are engine-specific.

System calls such as `write` can copy data into an OS cache without making it power-loss durable. `fsync`/equivalent requests durability under a filesystem/device contract, but controller caches, drive firmware, barriers, mount options, virtualization, and cloud storage semantics matter. Databases depend on storage honoring flush and ordering promises; dishonest hardware can defeat recovery protocols.

A torn page contains a mixture of old and new sectors or otherwise incomplete page image after failure. If the engine assumes page-write atomicity larger than the storage guarantees, recovery can fail even with WAL that logs only logical changes. Engines mitigate using full-page images, doublewrite buffers, rollback journals, WAL frames, checksums, or storage atomic-write facilities. Do not generalize one engine's mechanism to another.

PostgreSQL page LSN identifies the latest WAL record affecting the page and helps recovery decide whether redo is needed. It is not a wall-clock timestamp. SQLite rollback journal/WAL protocols preserve alternative page images or append frames with commit/checksum metadata. InnoDB uses redo plus its own page integrity and doublewrite mechanisms. Later recovery modules treat ordering and replay in depth.

Checksums detect some changes by recomputing a function over page identity/content and comparing stored metadata. PostgreSQL documents optional cluster-wide data-page checksums verified on read; SQLite WAL frames carry cumulative checksums; other engines have page checksum variants. Coverage differs: temporary/internal files or some metadata may not be protected. Record algorithm, seed/page identity, enabled state, and verification scope.

A matching checksum means only that bytes match that checksum relation with collision probability/algorithm limits. It does not prove the page belongs to the correct file/block, contains semantically valid records, reflects the latest committed state, or was durably written. A mismatch indicates damage or misinterpretation; bypassing verification can enable controlled recovery but must never become normal operation.

Encryption and checksums solve different problems. Encryption without authentication hides content but may not detect modification. Authenticated encryption can provide integrity within its nonce/key/associated-data protocol. Compression needs validation and decompression bounds. Key loss makes intact pages unreadable; backups must include protected key-management and restore evidence without embedding keys in data copies.

Page size trades fanout and overhead against amplification and contention. Larger pages amortize headers and improve sequential throughput/B-tree fanout but transfer more irrelevant bytes on random misses, enlarge dirty-write units, and can increase latch contention or torn-write exposure. Smaller pages improve fine-grained random I/O and cache occupancy but deepen trees and increase metadata/I/O count. Workload, record width, storage, compression, and engine constraints determine the choice.

Cache reach is roughly `buffer_bytes/page_size` frames, not records; record density and index working set determine useful reach. A 1 GiB buffer at 8 KiB holds at most 131072 frames before metadata overhead. Pinning, dirty pages, background policies, multiple relations, and access skew affect usable residency. Hit ratio alone can be high while critical misses remain slow or writes stall on dirty eviction.

File and page formats are versioned protocols. Fields can be repurposed; checksum algorithms, compression, encryption, row formats, page types, and metadata evolve. Use a version-matched server or supported offline utility. Upgrades that rewrite formats need space, time, rollback, backup, and verification plans. Copying a data file into another major version is not a migration.

Physical backup must capture a recoverable combination of data files and logs/control metadata. Copying files one by one from a running server can combine pages from different times. Supported online backup protocols establish a checkpoint/base and retain required WAL/journal/redo; storage snapshots need filesystem freeze/database coordination and multi-volume atomicity. A backup is unproven until isolated restore and integrity/application checks pass.

Never copy only the apparent table file as a logical backup. Dependencies include catalogs, tablespaces, transaction/undo state, logs, auxiliary forks, keys, configuration, and version. Logical dump has different properties: it reconstructs schema/rows through SQL and may avoid physical-format coupling, but costs more and does not preserve every physical detail.

For corruption response, stop unsafe writes, preserve original media/logs, record symptoms and versions, take immutable copies, calculate external hashes, and work on clones. Use engine-supported verification and recovery first. Map every damaged block to logical objects and recovery sources. A hex edit can make a checksum pass while destroying transactional invariants; never improvise on the only copy.

Monitoring should include relation/tablespace logical and allocated size, internal free/reusable space, filesystem/inode capacity, growth, buffer reads/hits, dirty pages, flush/checkpoint latency, IOPS/throughput, queue depth, read/write latency percentiles, temp/spill I/O, checksum/media errors, short reads, fsync failures, and backup/restore validation. Correlate by device, tablespace, relation, page class, and workload.

Testing storage logic requires boundary blocks around segment transitions, zero/last page, short files, sparse holes, malformed headers, overlapping offsets, max lengths, wrong page type/version, checksum mismatch, torn sectors, full filesystem, failed extension, short read/write, interrupted flush, crash at ordering points, and restore across supported versions. Fault injection must use disposable environments and explicit storage assumptions.

## Definitions and Notation

For page size `P>0`, pages per segment `N>0`, and logical block `b>=0`:

- `segment(b)=floor(b/N)`;
- `index(b)=b mod N`;
- `offset(b)=index(b)*P` within that segment;
- logical relation bytes for `B` allocated pages are `B*P` before auxiliary files/metadata;
- with header end `lower`, payload start `upper`, and special start `special`, valid layout requires `0<=lower<=upper<=special<=P`;
- contiguous free bytes are `upper-lower` under this simplified layout.

Real engines add forks, tablespaces, generations, extents, compression, encryption, and version-specific address rules.

## Mechanisms, Invariants, or Proof Structure

A page/file review should:

1. identify engine/build/version, cluster/file identity, page size, format, byte order, checksum/encryption/compression modes;
2. map database/object/tablespace/fork/segment/block through supported catalogs and tools;
3. validate file length/allocation and every page header, pointer, length, alignment, region, and page type;
4. distinguish logical size, allocated bytes, internal free/reusable space, sparse holes, snapshots, and OS-reclaimable space;
5. trace read/write paths across buffer, syscall, OS, filesystem, controller, device, and remote durability boundaries;
6. verify WAL/journal/redo ordering, page atomicity assumptions, checkpoints, and torn-page defenses;
7. verify checksum coverage and treat mismatch as evidence requiring protected recovery;
8. test backup as a full consistent data/log/metadata/key set through isolated restore;
9. reproduce faults only in disposable environments and preserve immutable forensic copies; and
10. correlate size, I/O, cache, dirty/flush, integrity, error, and recovery metrics with workloads.

The finite model below translates logical blocks into pedagogical segments, calculates relation segment lengths, validates a simplified page layout, and detects a one-byte change with a deliberately weak additive checksum. It is not a parser for any database format.

<!-- bijux-verify: {"id":"finite-page-file-layout","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"addresses=((0, 0, 0, 0), (3, 0, 3, 24576), (4, 1, 0, 0), (7, 1, 3, 24576), (8, 2, 0, 0), (10, 2, 2, 16384))\nsegment_lengths=((0, 32768), (1, 32768), (2, 24576))\nlogical_bytes=90112\naligned_payloads=(104, 200, 56)\npage_bounds=(36, 7832, 8192)\ncontiguous_free=7796\nlayout_valid=True\nchecksums=(12288, 12289)\ncorruption_detected=True\n","stderr":""}} -->
```python
page_size = 8192
pages_per_segment = 4
block_numbers = (0, 3, 4, 7, 8, 10)
allocated_pages = 11


def address(block):
    segment, index = divmod(block, pages_per_segment)
    return block, segment, index, index * page_size


def align8(length):
    return (length + 7) // 8 * 8


addresses = tuple(address(block) for block in block_numbers)
segment_lengths = []
remaining = allocated_pages
segment = 0
while remaining:
    pages = min(remaining, pages_per_segment)
    segment_lengths.append((segment, pages * page_size))
    remaining -= pages
    segment += 1

header_bytes = 24
item_id_bytes = 4
payloads = tuple(align8(length) for length in (100, 200, 50))
lower = header_bytes + len(payloads) * item_id_bytes
special = page_size
upper = special - sum(payloads)
layout_valid = 0 <= lower <= upper <= special <= page_size

page_image = bytes((0, 1, 2, 3)) * (page_size // 4)
damaged = bytearray(page_image)
damaged[100] = 1
checksums = (sum(page_image) % 65536, sum(damaged) % 65536)

print(f"addresses={addresses}")
print(f"segment_lengths={tuple(segment_lengths)}")
print(f"logical_bytes={allocated_pages * page_size}")
print(f"aligned_payloads={payloads}")
print(f"page_bounds={(lower, upper, special)}")
print(f"contiguous_free={upper - lower}")
print(f"layout_valid={layout_valid}")
print(f"checksums={checksums}")
print(f"corruption_detected={checksums[0] != checksums[1]}")
```

The additive checksum is intentionally weak and must not be used for storage integrity. The model omits real headers, item states, page types, forks, extents, sparse allocation, OS/device I/O, WAL/journals, concurrency, compression, encryption, and recovery.

## Alternatives and Trade-Offs

Fixed-size pages simplify addressing, caching, checksums, and I/O scheduling, but variable record sizes create fragmentation and overflow. Larger pages improve scan/fanout/header efficiency; smaller pages reduce random-read and dirty-write amplification. Extent allocation reduces metadata and fragmentation but reserves space in larger units. File-per-table improves placement and OS reclamation while increasing file count and metadata operations; shared tablespaces centralize allocation but retain freed space internally.

Buffered I/O leverages the OS cache but can duplicate database caching and obscure flush timing. Direct I/O provides more control and alignment constraints but still depends on device/controller semantics. Physical backup is fast and format-coupled; logical backup is portable and reconstruction-heavy. Checksums add detection CPU/I/O metadata; disabling them removes evidence rather than removing corruption risk.

## Failure Modes and Misconceptions

- “A page is a page.” Database, VM, filesystem, and device units have different contracts.
- “One table is one file.” Tablespaces, indexes, forks, segments, overflow, logs, and metadata break that mapping.
- “File length equals used disk.” Sparse extents, compression, snapshots, and internal free space differ.
- “Delete returns space to the OS.” It often makes space reusable only inside the database.
- “A successful write is durable.” Upper-layer acknowledgment may precede stable-media flush.
- “WAL makes torn pages impossible.” Recovery depends on page atomicity/full-image/doublewrite/journal mechanisms.
- “Checksum success proves correctness.” It is bounded corruption detection, not semantic or recency proof.
- “Checksum failure can be ignored.” Bypass is a controlled recovery tactic, not a repair.
- “Copying live data files is a backup.” Files/logs can represent incompatible times without a backup protocol.
- “A hex editor can fix one page.” Unsupported edits can destroy cross-page and transactional invariants.

## Worked Examples

### Example 1

For 8 KiB pages, block 10 in an unsegmented file begins at byte 81920. Under the pedagogical four-page segments it maps to segment 2, index 2, byte 16384. Real translation must also name tablespace, relation generation, fork, and engine version.

### Example 2

Eleven pages at 8192 bytes give 90112 logical bytes. With four-page segments, file lengths are 32768, 32768, and 24576. Auxiliary forks/logs, sparse allocation, filesystem metadata, and snapshots make total storage different.

### Example 3

A page has `lower=36`, `upper=7832`, `special=8192`; contiguous free space is 7796. If an item claims offset 7800 and length 100, it crosses special space and must be rejected even if the page checksum matches.

### Example 4

A 100-byte record aligns to 104 bytes at an 8-byte boundary. Forgetting four padding bytes causes the next record to overlap. Alignment belongs in every size/offset calculation and must avoid integer overflow.

### Example 5

A database reports 30 GB reusable after vacuum, but filesystem allocation is unchanged. The pages are available for future database writes; the OS cannot allocate those blocks elsewhere. A rewrite/truncate may reclaim them at temporary-space and locking cost.

### Example 6

The server modifies an 8 KiB page whose device atomic unit is smaller; power fails after some sectors. Recovery succeeds only if the engine's log/full-page/doublewrite/journal protocol and flush ordering cover that torn image. File-system journaling alone is not a universal database guarantee.

### Example 7

A stored checksum differs on read. Record file/block, expected/actual checksum, engine logs, storage errors, and snapshot; stop unsafe writes and preserve copies. Retrieve a correct page from backup/replica plus logs using supported recovery, rather than recomputing a checksum over corrupted bytes.

### Example 8

A one-terabyte sparse file occupies 100 GB of filesystem blocks. Copying it with a tool that materializes holes can require one terabyte at the destination. Backup capacity and duration must use allocated/logical behavior of the exact tool and snapshot layer.

### Example 9

A snapshot captures data volume A before its matching log volume B. Each snapshot is individually atomic but the pair is inconsistent. Coordinate database backup mode/checkpoint, multi-volume snapshot atomicity, and retained logs, then prove with an isolated restore.

### Example 10

Buffer hit ratio rises from 98% to 99%, yet p99 latency worsens because the remaining misses hit a saturated remote device and dirty-page checkpoints stall writes. Correlate misses by relation/page type, queue depth, flush latency, dirty inventory, checkpoint rate, and workload—not ratio alone.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies arrays, offsets, free lists, trees, and external-memory structures.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies virtual memory, filesystems, caches, direct I/O, flushes, and crash behavior.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies cache lines, memory integrity, persistence, controllers, and device geometry.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) governs capacity, fault domains, observability, backup, restore, and incident response.
- [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) supplies block storage, snapshots, virtualization, durability claims, and multi-volume coordination.

## References

1. PostgreSQL Global Development Group, [Database Page Layout](https://www.postgresql.org/docs/18/storage-page-layout.html), PostgreSQL 18 storage internals.
2. PostgreSQL Global Development Group, [Database File Layout](https://www.postgresql.org/docs/18/storage-file-layout.html), PostgreSQL 18 storage internals.
3. PostgreSQL Global Development Group, [Data Checksums](https://www.postgresql.org/docs/18/checksums.html), PostgreSQL 18 reliability documentation.
4. SQLite Project, [Database File Format](https://www.sqlite.org/fileformat.html), SQLite page, header, freelist, WAL, and journal format documentation.
5. SQLite Project, [Atomic Commit](https://www.sqlite.org/atomiccommit.html), SQLite storage and filesystem-assumption documentation.
6. Oracle, [Physical Structure of an InnoDB Index](https://dev.mysql.com/doc/refman/8.4/en/innodb-physical-structure.html), MySQL 8.4 Reference Manual.
7. Oracle, [Files Created by CREATE TABLE](https://dev.mysql.com/doc/refman/8.4/en/create-table-files.html), MySQL 8.4 tablespace/file documentation.
8. Oracle, [InnoDB Disk I/O and File Space Management](https://dev.mysql.com/doc/refman/8.4/en/innodb-disk-management.html), MySQL 8.4 Reference Manual.

## Exercises

### Exercise 1

For page size 16384 and 64 pages per segment, translate blocks 0, 63, 64, 65, and 130 into `(segment,index,offset)`. Compute logical bytes for 131 allocated pages and final segment length.

### Exercise 2

A 4096-byte page has 32-byte header, five 4-byte slots, 128-byte special area, and raw records 101, 200, and 17 bytes aligned to 8. Compute lower, upper, special, contiguous free space, and validate the region invariant.

### Exercise 3

Explain why write-ahead logging needs an explicit storage ordering/durability contract. Include dirty buffers, WAL durability, data-page write, torn page, OS/controller caches, and recovery.

### Exercise 4

Design a safe response to a checksum failure on a primary database page. Cover containment, evidence preservation, replica/backup validation, supported recovery, data reconciliation, root cause, and return to service.

### Exercise 5

Create a production evidence package for changing database storage placement. Include logical/physical mapping, sizes, headroom, page/checksum formats, I/O baselines, snapshots/backups, restore, failure injection, rollback, observability, security, and version compatibility.

## Answers to the Exercises

### Answer 1

Block 0 maps `(0,0,0)`; 63 `(0,63,1032192)`; 64 `(1,0,0)`; 65 `(1,1,16384)`; 130 `(2,2,32768)`. Logical bytes are `131*16384=2146304`. Two full segments contain 64 pages each; the final segment has three pages and length 49152 bytes. Real engines add their own segment/fork rules.

### Answer 2

Aligned record sizes are 104, 200, and 24, totaling 328. `lower=32+5*4=52`. `special=4096-128=3968`. `upper=3968-328=3640`. Contiguous free space is `3640-52=3588`, and `0<=52<=3640<=3968<=4096`, so the simplified regions do not overlap. Unused slots and actual engine metadata still require their own validation.

### Answer 3

The transaction changes a buffer and emits recovery log. Before a data page containing that change can be considered safely written, the log needed to redo it must cross every volatile layer to the promised durable boundary. Later page write can be torn if smaller units persist separately; recovery needs full-image/doublewrite/journal or guaranteed atomicity in addition to logical redo. `write()` completion can mean only OS-cache acceptance, and even flush depends on filesystem/controller/device honoring barriers. Document and test the entire chain with the target engine.

### Answer 4

Record the exact error, object/file/block, engine/build, checksum mode, recent incidents, and storage logs; stop or isolate writes according to vendor guidance. Preserve immutable hashes and copies of data/log/control files before experimenting. Check replicas and backups without promoting unverified corruption, run supported offline/online integrity tools, and identify all logical objects/rows affected. Recover from a known-good backup/replica plus required logs using supported procedures, then reconcile constraints/application totals and perform isolated restore tests. Diagnose memory, filesystem, controller, device, firmware, virtualization, and operational causes; replace faulty layers and monitor before returning traffic. Never “fix” only the stored checksum.

### Answer 5

Inventory cluster/database/tablespace/relation/fork/file/block mappings with authoritative tools, page size/format/checksum/encryption/compression modes, logical and allocated sizes, internal free space, snapshots, growth, and temporary headroom. Baseline throughput/IOPS/latency/queue, buffer misses, dirty/flush/checkpoint behavior, and replication. Capture coordinated backups and keys/logs, prove isolated restore, and test full disk, short I/O, interrupted move, checksum failure, crash at cutover, and rollback on disposable systems. Use least-privilege paths and protected evidence; verify version/page compatibility and object identity after move. Define cutover fencing, multi-volume atomicity, monitoring thresholds, cancellation, rollback/forward repair, and post-cutover integrity plus workload comparisons.
