---
module_id: DBE-024
program: Database Engineering
level: 1
module_number: 24
title: Heap Files
status: complete
last_verified: 2026-08-30
---

# Heap Files

## One-Page Review

### Governing question

How does an unordered collection of data pages support insertion, lookup by physical locator, full scans, update, deletion, growth, and reclamation while preserving transaction and recovery correctness?

### Essential definitions

A **heap file** is a table-storage organization whose data pages are not maintained in search-key order; it is unrelated to the heap priority-queue data structure and the process-memory heap. A **heap page** holds row versions, often through slots. A **record identifier** (RID) names a physical page and slot under an engine-specific lifetime. A **full heap scan** examines allocated data pages and candidate slots, then applies visibility and predicates. **Page selection** chooses a page for insertion using free-space evidence. **Forwarding** leaves a locator that redirects to a moved record. **High-water mark** broadly denotes the allocated/used frontier in engines that expose such a concept; its exact semantics are vendor-specific.

### Central model, mechanism, or theorem

For `N` heap pages, a predicate with no usable access path has page-read cost on the order of `N` (modified by cache, parallelism, pruning, and visibility shortcuts), regardless of output cardinality. Insertion can be near constant expected work only when an auxiliary structure supplies a suitable candidate page; otherwise finding space can itself approach a scan. The heap imposes no durable logical row order. A RID can survive movement within a slot-mediated page, but delete/reuse, cross-page movement, rewrite, truncate, restore, or engine policy can invalidate or retarget it.

### Critical invariants

- Relation identity, fork/segment, page identity/type/version, and physical locator are validated together.
- Every allocated page is reachable exactly as the engine's extent/page metadata specifies; every live heap tuple is structurally contained by one page/overflow protocol.
- Slot and tuple invariants hold before logical decoding or visibility evaluation.
- Page-selection summaries are hints; actual space is rechecked under the page latch.
- Logical deletion and physical reclamation respect snapshots, locks, undo/log, indexes, replicas, and recovery.
- Every secondary-index entry resolves to the intended visible row version or is safely classified as transient/dead under engine rules.
- Scans do not infer SQL order from physical page/slot order.
- File truncation, page reuse, and RID reuse occur only after all references and recovery obligations permit them.

### Common failures

Failures include assuming insertion order is query order; calling any table a heap even when its rows live in a clustered index; scanning from filenames without catalogs; trusting stale free-space hints; ignoring slot overhead and row expansion; treating delete as immediate disk release; retaining physical RIDs as application identifiers; moving rows without maintaining indexes or forwarding state; counting on a high-water mark to shrink automatically; reading dead/invisible versions as live; and judging scan cost only from returned rows rather than pages, visibility work, overflow reads, cache, and predicate CPU.

### Compact example

In a pedagogical heap with 100 usable bytes per page and two bytes retained per allocated slot, rows A(40) and B(50) fill page 0 to 94 bytes; C(30) and D(60) fill page 1 to 94. Deleting B leaves its slot and gives page 0 56 free bytes. E(45) reuses B's slot, so the stale RID `(0,1)` now names E. Physical scan order is A,E,C,D rather than surviving insertion order A,C,D,E. F(95) requires a new third page. A full predicate scan reads all three pages even if only D and F qualify.

### Connections

[DBE-022](022-record-and-tuple-layout.md) defines tuple bytes and [DBE-023](023-slotted-pages.md) defines page-local indirection. [DBE-025](../ROADMAP.md) develops cross-page free-space management; [DBE-026](../ROADMAP.md) explains why heap scans may hit buffers rather than storage.

## Governing Question

A heap file trades physical search-key ordering for flexible placement. A new row can go to any eligible page, an update can create a new version where space exists, and a scan can visit pages sequentially. This makes heap storage a strong default for write-oriented or broadly accessed tables, but fast point/range search normally requires separate indexes.

“Unordered” does not mean random bytes or absent structure. Files/segments contain typed pages; pages contain headers, slots, tuple versions, and transaction metadata; auxiliary structures summarize free space and visibility; indexes locate rows; logs make changes recoverable. The absence is a maintained data-row ordering by a user search key. Every other structural and transactional invariant still applies.

## Why This Matters

Heap organization shapes the entire cost model. Inserts need page discovery. Full scans pay per page and tuple, not per returned result. Updates can create dead versions, forwarding records, or index maintenance. Deletes usually create reusable internal space before any operating-system capacity is returned. Wide rows can add overflow I/O. Clustering can decay as related rows land on unrelated pages.

Correct diagnosis depends on recognizing the organization. In a heap, a secondary index may contain a physical locator; in a clustered organization, the leaf itself contains the row and secondary indexes may carry the clustered key. A “key lookup,” RID lookup, bookmark lookup, or clustered lookup can therefore have different I/O, stability, and maintenance properties.

Heap behavior is also temporal. Fresh bulk-loaded pages may be dense and physically correlated with input, but concurrent inserts, updates, vacuum, page reuse, restore, and rewrites change that arrangement. An observed order or locality is evidence about one state, never a SQL guarantee.

## Prerequisites and Retrieval

Retrieve pages, files and segments, slotted pages, tuple layout, extents, free-space maps, buffer pools, indexes, keys, MVCC/undo, write-ahead logging, checkpoints, scans, selectivity, and filesystem allocation.

Distinguish heap file from memory heap and binary heap; data organization from access method; page order from SQL order; table scan from index scan; logical row from physical version; RID from key; internal reusable space from file shrinkage; allocated page from visible tuple; free-space hint from latched truth; and logical correlation from guaranteed clustering.

## Learning Objectives

After this module, you should be able to:

1. define heap organization precisely and identify non-heap contrasts;
2. trace insertion from candidate-page selection through durable publication;
3. derive simplified heap scan and storage costs;
4. explain RID lookup and its bounded lifetime;
5. trace delete, update, movement, forwarding, and version cleanup;
6. distinguish page reuse, relation growth, truncation, and OS reclamation;
7. explain how indexes and visibility metadata interact with a heap;
8. diagnose fragmentation, density, correlation, and scan behavior;
9. design safe heap inspection and maintenance; and
10. validate heap operations with model, workload, crash, and restore evidence.

## Core Exposition

A heap relation is an unordered page collection under a table access method. “File” is conceptual: the relation may span segment files, tablespaces, extents, forks, or storage objects. Conversely, one physical file can hold many engine objects. The authoritative catalogs and storage metadata—not a guessed filename—define relation ownership and page addresses.

Heap pages remain structured. A typical page has a header, slot/item directory, free space, tuple versions, and perhaps access-method-specific metadata. The table access method defines tuple headers, visibility, line-pointer states, page initialization, insertion, scanning, pruning, and recovery callbacks. DBE-021 through DBE-023 supply these lower layers.

Unordered means the engine does not maintain rows in key order across heap pages. Page numbers impose a physical traversal order, and slots impose some local enumeration order, but neither becomes an SQL ordering contract. Only an `ORDER BY` over a total ordering (with tie handling) requests ordered results. Parallel scans, plan changes, page movement, and maintenance can alter returned order.

Insertion begins by constructing or sizing the stored tuple. The engine seeks a candidate page with sufficient usable space, commonly through cached state, a free-space map, allocation metadata, or recent-page heuristics. It pins and latches that page, rechecks true space and page state, inserts through the slot protocol, records WAL/undo as required, updates indexes and transaction state, marks buffers dirty, and eventually refreshes auxiliary space metadata.

A candidate can be stale. Another transaction may consume the space; the page may need pruning; the tuple may grow because its physical representation differs from the estimate; a slot is also needed; or alignment/overflow rules may intervene. Correct insertion retries another page or extends the relation under the engine protocol. It never writes across a page boundary simply because an estimate said the row fit.

When no existing page is selected, the relation grows by allocating or extending pages/extents. Growth must coordinate concurrent extenders, initialize pages, log metadata/data as required, handle short writes and full storage, and avoid exposing uninitialized pages as valid. Preallocation reduces extension contention and fragmentation but consumes/reserves capacity earlier and can amplify initialization/recovery work.

Page selection is a policy. First-fit tends to reuse early space but may concentrate contention. Best-fit can reduce leftover fragments but costs search and may create unusably small gaps. Next-fit/recent-page policies improve locality. Append-biased placement produces initially correlated data but leaves old holes. Randomized or partitioned choices distribute latch contention. Real systems mix heuristics with approximate summaries.

DBE-025 covers the data structure for finding space. At this level, the key invariant is that any directory or map is advisory until the chosen page is latched and checked. False positives cause retry; false negatives cause avoidable growth. Neither may cause overwriting live data.

A RID commonly contains relation context plus page and slot, though exact formats vary. A secondary index in a heap-organized engine can map a search key to such a locator. The heap fetch validates the page/slot, follows permitted redirection, evaluates tuple visibility, and may recheck the predicate because concurrent changes or lossy access paths can make the candidate insufficient.

RID stability is bounded. Slotted-page compaction can move bytes while preserving the live slot. A growing update might move the row and leave a forwarding pointer or create a new version elsewhere. Delete and slot reuse can make the same numeric RID name another tuple. Relation rewrite, partition move, shrink, restore, page deallocation/reuse, or table recreation can invalidate page identity. Applications should store declared logical keys, never internal locators.

A full heap scan enumerates allocated data pages, pins/reads each, validates the page, visits candidate slots, applies visibility, decodes required columns, and evaluates predicates. It can skip pages using trustworthy visibility/zone/pruning metadata where supported, but a basic heap has no key order that permits stopping after a range boundary.

For `N` data pages, cold scan transfer is approximately `N*P` bytes before filesystem/device amplification, overflow values, indexes, prefetch, compression, and cache effects. CPU is proportional to candidate tuples plus decoding/predicate work. Returning one row can still read every page. Returning many rows can make a sequential heap scan cheaper than many random index lookups.

Buffer pools and operating systems change physical reads but not the logical pages considered. Repeated scans may be memory-resident; parallel scans divide ranges and coordinate allocation; synchronized scans may share work; prefetch overlaps latency. Report logical reads, physical reads, bytes, cache state, parallelism, predicate CPU, and elapsed time rather than calling a scan “one I/O.”

Visibility is not structural presence. Under MVCC, a page can contain several versions of one logical row, dead versions, aborted inserts, or deletion markers. A scan consults snapshot and transaction status/tuple metadata. An all-visible map may enable index-only or scan shortcuts, but such metadata must be conservatively maintained. Counting raw tuple-shaped byte sequences is not row counting.

Deletion commonly marks or versions a row; physical bytes remain until no snapshot/undo/recovery obligation needs them. Cleanup may free a slot or make page space reusable. The relation file usually does not shrink. Reclaiming OS space can require truncating empty tail pages, deallocating extents, moving/rebuilding the table, or engine-specific shrink operations with locking, log, replication, and fragmentation consequences.

An update that fits the engine's in-page/version rules may keep locality; otherwise it creates another version or moves data. Every secondary index must continue to find the correct logical row. Some engines use forwarding records; some update index locators; PostgreSQL can use heap-only tuple chains when indexed columns do not change and page conditions permit. Each mechanism has distinct visibility and maintenance rules.

Forwarding preserves an old lookup location by storing a redirect to the new location. It avoids updating every secondary index immediately but adds an extra page access and risks chains/cycles if poorly governed. Maintenance can remove forwarded records by rebuilding/reorganizing. A diagnostic must distinguish forwarding, MVCC version links, overflow pointers, and corrupted offsets.

Secondary indexes make selective heap access possible but impose write amplification and space. Insert adds entries; update may change keys/locators; delete leaves or marks entries until cleanup. An index entry can be dead, point to an invisible version, or require a heap visibility check. Covering/index-only strategies reduce heap fetches only under the engine's visibility and column-coverage rules.

The contrast with clustered storage matters. InnoDB documents that table row data resides in the clustered-index leaves, normally ordered by primary key, and secondary entries carry primary-key columns. It is not a heap merely because SQL omits `ORDER BY`. Oracle documents heap-organized tables as placing rows where they fit, contrasting them with index-organized tables. Product names do not replace inspection of the chosen storage engine and table organization.

Physical correlation measures how closely heap placement follows a logical value/order. Correlation can help range scans by making successive index entries lead to nearby pages. It may arise from bulk loading or clustering/rewrite but decays under later changes. Statistics are estimates. Reorganizing for correlation costs rewrite space, log, locks/concurrency coordination, replicas, backups, and future maintenance.

Fragmentation has several layers: holes within pages, sparsely populated pages, noncontiguous filesystem extents, forwarding/version chains, index disorder, and external overflow. “30% fragmented” is meaningless without definition and measurement method. A low page density may be intentional fill factor or MVCC headroom rather than waste.

Heap maintenance includes pruning/vacuum/garbage collection, statistics refresh, space-map repair, page compaction, tail truncation, reorganize/rewrite, and integrity checking. These operations compete for I/O, CPU, memory, latches/locks, WAL/log bandwidth, replica apply, and backup windows. They need cancellation, throttling, headroom, failure recovery, and post-checks.

Observability should include allocated/data pages, live/dead/versioned tuples, tuple and page density distributions, reusable and contiguous space, insertion retries/extensions, forwarded rows or version-chain lengths, scan logical/physical reads, overflow fetches, cache hit/residency, prefetch, sequential/random latency, index-to-heap fetches, WAL/log bytes, maintenance lag, relation growth, filesystem allocation, and replica lag.

Safe inspection starts with supported catalogs and engine tools. If byte inspection is necessary, record engine/build, relation identity, forks/segments, page size/type/version, checksums/encryption/compression, schema snapshot, transaction context, and raw hashes; use protected copies and version-matched parsers. Do not scan or edit live relation files outside the engine.

The executable model below demonstrates only first-fit page selection, retained slot overhead, unordered physical scan, RID reuse, and relation extension. It is not a database, tuple encoder, index, visibility implementation, free-space map, concurrent allocator, or recovery protocol.

<!-- bijux-verify: {"id":"heap-file-placement","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial_rids=(('A', (0, 0)), ('B', (0, 1)), ('C', (1, 0)), ('D', (1, 1)))\ninitial_pages=((94, 6), (94, 6))\nafter_delete_free=(56, 6)\nreused=('E', (0, 1), 'B')\nscan=('A', 'E', 'C', 'D')\npages=((89, 11), (94, 6))\nextended=('F', (2, 0), 3)\nfull_scan_pages=3\nmatches=('D', 'F')\nvalid=True\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass
class Slot:
    identity: str | None
    size: int


class HeapPage:
    capacity = 100
    slot_bytes = 2

    def __init__(self) -> None:
        self.slots: list[Slot] = []

    def used(self) -> int:
        return len(self.slots) * self.slot_bytes + sum(
            slot.size for slot in self.slots if slot.identity is not None
        )

    def free(self) -> int:
        return self.capacity - self.used()

    def can_insert(self, size: int) -> bool:
        reusable = any(slot.identity is None for slot in self.slots)
        return size + (0 if reusable else self.slot_bytes) <= self.free()

    def insert(self, identity: str, size: int) -> int:
        assert self.can_insert(size)
        for index, slot in enumerate(self.slots):
            if slot.identity is None:
                self.slots[index] = Slot(identity, size)
                return index
        self.slots.append(Slot(identity, size))
        return len(self.slots) - 1

    def delete(self, index: int) -> str:
        slot = self.slots[index]
        assert slot.identity is not None
        old = slot.identity
        self.slots[index] = Slot(None, 0)
        return old


class HeapFile:
    def __init__(self) -> None:
        self.pages: list[HeapPage] = []

    def insert(self, identity: str, size: int) -> tuple[int, int]:
        page = next((p for p in self.pages if p.can_insert(size)), None)
        if page is None:
            page = HeapPage()
            self.pages.append(page)
        page_id = self.pages.index(page)
        return page_id, page.insert(identity, size)

    def scan(self) -> tuple[str, ...]:
        return tuple(
            slot.identity
            for page in self.pages
            for slot in page.slots
            if slot.identity is not None
        )

    def valid(self) -> bool:
        return all(
            0 <= page.used() <= page.capacity
            and all(slot.size >= 0 for slot in page.slots)
            for page in self.pages
        )


heap = HeapFile()
initial_rids = tuple(
    (identity, heap.insert(identity, size))
    for identity, size in (("A", 40), ("B", 50), ("C", 30), ("D", 60))
)
initial_pages = tuple((page.used(), page.free()) for page in heap.pages)
stale_identity = heap.pages[0].delete(1)
after_delete_free = tuple(page.free() for page in heap.pages)
e_rid = heap.insert("E", 45)
reused = ("E", e_rid, stale_identity)
scan = heap.scan()
pages = tuple((page.used(), page.free()) for page in heap.pages)
f_rid = heap.insert("F", 95)
extended = ("F", f_rid, len(heap.pages))
matches = tuple(
    slot.identity
    for page in heap.pages
    for slot in page.slots
    if slot.identity is not None and slot.size >= 60
)

print(f"initial_rids={initial_rids}")
print(f"initial_pages={initial_pages}")
print(f"after_delete_free={after_delete_free}")
print(f"reused={reused}")
print(f"scan={scan}")
print(f"pages={pages}")
print(f"extended={extended}")
print(f"full_scan_pages={len(heap.pages)}")
print(f"matches={matches}")
print(f"valid={heap.valid()}")
```

The exact output proves only this bounded state transition. Real rows need headers and alignment; deletion may retain versions; RIDs have engine-specific lifetimes; selection is concurrent and approximate; extension, index maintenance, WAL, and recovery are absent.

## Definitions and Notation

Let heap relation `R` have allocated data pages `P_0...P_(N-1)`. Page `i` has usable capacity `C_i`, live/versioned stored bytes `D_i`, persistent page/slot metadata `M_i`, and immediately reusable bytes `F_i`, subject to `D_i+M_i+F_i<=C_i`. Additional dead bytes may be reclaimable only after visibility/maintenance conditions.

For a simplified full scan, logical page visits are `N` and transfer upper bound is approximately `sum_i C_i`; candidate-tuple work is `sum_i slots_i`. A RID is written `(relation_generation,page_id,slot_id[,generation])` to emphasize that page/slot alone omits identity context. These formulas are cost models, not guarantees of physical I/O or vendor locator shape.

## Mechanisms, Invariants, or Proof Structure

A defensible heap operation follows these obligations:

1. Resolve authoritative relation/access-method identity, physical components, format, and transaction context.
2. Validate allocation and page metadata before treating a page as a heap data page.
3. For insert, size the stored tuple, obtain a candidate, latch/pin it, and revalidate actual space and slot cost.
4. Publish tuple, slot, visibility/version state, index entries, boundary data, WAL/undo, checksum, and dirty state under the engine protocol.
5. For lookup/scan, validate RID/page/slot or enumerate allocated pages, then apply visibility and predicate rules.
6. For update/delete, retain old versions/locators until every snapshot, index, undo/log, replica, and recovery obligation releases them.
7. Update free-space/visibility/allocation summaries conservatively and tolerate safe staleness.
8. On extension/truncation/rewrite, serialize metadata changes and handle partial failure, cancellation, and recovery.
9. Cross-check heap and all indexes, constraints, row counts/aggregates, replicas, and restored backups.
10. Record versions, commands, cache/workload conditions, and limitations for every performance or correctness claim.

The scan lower-bound intuition is straightforward: without a usable summary or index that can rule out page `i`, an adversarial qualifying visible tuple could be on that page. A correct exhaustive predicate evaluation must therefore consider every such page. Cache may remove physical I/O and parallelism may reduce elapsed time, but neither removes the logical completeness requirement.

## Alternatives and Trade-Offs

Heap organization favors flexible placement, cheap bulk/sequential scans, and separate indexes chosen per workload. A clustered B-tree favors primary-key locality and direct keyed access but pays split/ordering costs and makes the clustering key part of physical design. An index-organized table can cover primary-key access but widens leaf rows and changes secondary lookup. Log-structured/columnar organizations optimize other write or analytic patterns.

First-fit reuses space but can create hotspots; append placement improves sequential write/locality but leaves holes; best-fit reduces some waste at search cost; approximate maps make selection fast but retry-prone. Forwarding avoids broad index rewrites but adds reads. Immediate cleanup recovers space sooner but conflicts with long snapshots and increases foreground work; deferred cleanup improves latency but grows bloat.

Rebuild/reorganization can restore density/correlation and remove forwarding/dead space, but consumes temporary storage, log bandwidth, CPU/I/O, locks, replica capacity, backup time, and operational risk. A permanently scheduled rewrite without measured benefit is not maintenance engineering.

## Failure Modes and Misconceptions

- “Heap means a priority queue or memory allocator.” Here it is unordered database row storage.
- “No `ORDER BY` returns insertion order.” Physical order is not a SQL guarantee.
- “Every database table is a heap.” Clustered/index-organized/columnar/log-structured organizations differ.
- “A free-space entry proves the row fits.” Space is revalidated under the page latch.
- “Delete shrinks the file.” It usually creates delayed internal reuse first.
- “A RID is the business key.” Page/slot identities can move, disappear, or be reused.
- “One matching row means one page read.” A selective predicate without an access path can scan the relation.
- “Raw tuple count equals visible row count.” MVCC and aborted/dead versions invalidate that inference.
- “Index entries always point directly to current bytes.” Visibility, forwarding, versions, and organization intervene.
- “Rebuild is harmless cleanup.” It is a capacity, concurrency, recovery, replication, and rollback event.

## Worked Examples

### Example 1

Pages have 100 usable bytes and retain two bytes per allocated slot. A(40) consumes 42; B(50) raises page 0 usage to 94. C(30) cannot fit because it needs 32, so the heap extends page 1. The tuple size alone was not the insertion requirement.

### Example 2

C(30) and D(60), plus two slots, fill page 1 to 94. Both pages have six free bytes. A later 95-byte value needs 97 with a slot and forces page 2, even though the heap has 12 aggregate free bytes.

### Example 3

Deleting B leaves its slot allocated but removes 50 payload bytes, so page 0 usage becomes 44 and free space 56. Whether a real database can reuse those bytes immediately depends on MVCC/undo/recovery and page compaction, not only arithmetic.

### Example 4

E(45) reuses slot 1 and consumes no new slot bytes, bringing usage to 89. The stale RID `(0,1)` that identified B now resolves to E in the model. Physical locators require lifecycle validation and must not escape as durable application identity.

### Example 5

After B's deletion and E's insertion, physical scan order is A,E,C,D, whereas surviving insertion chronology is A,C,D,E. Neither is a guaranteed query result order; only an explicit total `ORDER BY` supplies that contract.

### Example 6

A predicate `size>=60` returns D and F but still visits three pages in the model. Output cardinality two does not imply two-page work. A suitable index or summary could alter the plan, while warm buffers alter physical reads but not the logical scan.

### Example 7

An update makes A too large for page 0. The engine may create a new version on page 2 and maintain every index, or leave a forwarding entry under a supported protocol. Simply changing the RID in one secondary index leaves other indexes and concurrent snapshots inconsistent.

### Example 8

A heap has 40% free bytes but almost all are on cold early pages; an append-biased allocator keeps extending it. A map/selection-policy change might reuse space, but engineers first measure contention, tuple sizes, visibility/reclaimability, false-negative summaries, and locality rather than infer a leak.

### Example 9

A range query follows a secondary index whose keys are ordered but heap RIDs jump among pages. With high selectivity, random heap fetches can cost more than a sequential scan. Correlation, cache residency, covering columns, and visibility checks determine the crossover.

### Example 10

An online rewrite compacts 500 GB but generates heavy WAL and replica lag, then runs out of temporary storage. A production plan needs headroom including indexes/logs/snapshots, throttling and cancellation, replica capacity, a proven backup/restore, an irreversible-boundary decision, and post-rewrite constraint/workload validation.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies external-memory arrays, directories, free lists, and index-versus-scan cost models.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies files, extents, page cache, prefetch, asynchronous I/O, and truncation semantics.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies adversarial lower bounds, selectivity, cost crossover, and workload measurement.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies capacity, observability, fault handling, backup/restore, and operational change control.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) consumes scan/layout properties when extracting and loading relational data.

## References

1. PostgreSQL Global Development Group, [Database File Layout](https://www.postgresql.org/docs/18/storage-file-layout.html), PostgreSQL 18 heap access-method files, forks, and auxiliary storage.
2. PostgreSQL Global Development Group, [Database Page Layout](https://www.postgresql.org/docs/18/storage-page-layout.html), PostgreSQL 18 heap page and tuple location documentation.
3. PostgreSQL Global Development Group, [Free Space Map](https://www.postgresql.org/docs/18/storage-fsm.html), PostgreSQL 18 per-relation free-space summary documentation.
4. PostgreSQL Global Development Group, [System Columns](https://www.postgresql.org/docs/18/ddl-system-columns.html), PostgreSQL 18 `ctid` and transaction-related physical-column caveats.
5. Microsoft, [Heaps (Tables without Clustered Indexes)](https://learn.microsoft.com/en-us/sql/relational-databases/indexes/heaps-tables-without-clustered-indexes?view=sql-server-ver17), SQL Server heap organization and forwarding documentation.
6. Oracle, [Clustered and Secondary Indexes](https://dev.mysql.com/doc/refman/8.4/en/innodb-index-types.html), MySQL 8.4 InnoDB clustered organization contrast.
7. Oracle, [Database Concepts](https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/database-concepts.pdf), Oracle Database 23 heap-organized and index-organized storage concepts.
8. Raghu Ramakrishnan and Johannes Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, file organization and heap-file foundations.
9. Hector Garcia-Molina, Jeffrey D. Ullman, and Jennifer Widom, *Database Systems: The Complete Book*, 2nd ed., Pearson, 2008, secondary-storage and file-organization foundations.

## Exercises

### Exercise 1

Using the teaching model (100 usable bytes, two bytes per retained slot), insert sizes 55, 35, 20, 70 with first-fit selection. Give every RID, page usage/free space, and scan order. Then delete the 35-byte row and insert a 30-byte row; identify reuse and stale-RID risk.

### Exercise 2

A heap has 10000 pages of 8 KiB, 80% buffer residency, and a predicate that returns ten rows but has no usable access path. Estimate logical bytes considered and, under a deliberately simple independent-residency assumption, cold bytes read. State why this is not an elapsed-time prediction.

### Exercise 3

Design a safe heap RID fetch validator that can encounter a normal tuple, free slot, forwarding entry, invisible version, reused page, malformed page, or checksum failure.

### Exercise 4

Compare a heap plus secondary B-tree with clustered B-tree storage for random inserts, primary-key ranges, non-key selective queries, wide/changing primary keys, full scans, and updates. Give a workload-conditioned recommendation.

### Exercise 5

Create an evidence plan for reclaiming space from a bloated production heap while maintaining availability. Cover definitions, visibility blockers, capacity, indexes, logs, replicas, backups, fault tests, cutover, rollback/forward recovery, and post-validation.

## Answers to the Exercises

### Answer 1

55 uses page 0 slot 0 and 57 bytes. The 35-byte row uses page 0 slot 1; usage is `55+35+4=94`, free 6. The 20-byte row cannot fit and becomes page 1 slot 0, usage 22. The 70-byte row fits page 1 slot 1, making usage `20+70+4=94`. RIDs are `(0,0),(0,1),(1,0),(1,1)` and scan order follows those slots. Deleting the 35-byte row leaves page 0 with two retained slots and usage 59, free 41. The 30-byte row reuses `(0,1)`, yielding usage 89/free 11. A stale locator for the deleted row now names the new row.

### Answer 2

Logical scan bytes are `10000*8192=81920000` bytes, about 78.125 MiB. If 80% of pages are resident independently and nothing else changes, expected cold transfer is approximately `0.2*81920000=16384000` bytes, about 15.625 MiB. This is not elapsed time: cache distribution, concurrent eviction, prefetch/request size, compression, filesystem/device cache, overflow, parallelism, queueing, predicate CPU, visibility, and storage bandwidth/latency all matter. The ten-row result does not reduce page consideration.

### Answer 3

Resolve relation generation/access method and verify the requested page is allocated to it. Pin/read through the engine, verify page type/version/size and checksum/authentication before parsing, then validate page boundaries and the slot index. Branch on validated slot state: normal requires bounded tuple structure and snapshot visibility; free returns not found under the caller's lifetime contract; forwarding follows only a bounded, cycle-checked, ownership-validated target; invisible is not returned. Verify page generation/LSN/latch conditions against reuse and recheck after permitted races. Any malformed structure or integrity failure stops normal decoding and enters supported corruption handling on preserved evidence; never guess a tuple from recognizable bytes.

### Answer 4

A heap avoids maintaining primary-key physical order, so random inserts can use many eligible pages and secondary indexes can be selected independently; primary-key ranges require a secondary traversal plus heap fetches. A clustered B-tree provides locality and direct leaves for primary-key ranges, but random keys can split pages and a wide/changing clustering key enlarges and churns secondary indexes. Both can full-scan efficiently under suitable layout/cache, though clustered order may add range locality. Selective non-key queries need secondary indexes in both; heap locators versus clustered-key lookups change cost. Choose only after measuring insert distribution, key width/change, range/selectivity mix, covering potential, scans, cache, maintenance, and engine mechanisms.

### Answer 5

Define bloat separately as dead/versioned bytes, low page density, forwarding, tail empty pages, logical file size, and filesystem allocation. Identify long snapshots, replication slots/undo retention, failed maintenance, workload churn, tuple-width changes, and index state. Measure page/tuple distributions, reclaimable versus immediately reusable space, scan/lookup latency, WAL/log rate, replica lag, growth, and headroom including new heap, every index, logs, snapshots, and rollback copy. Rehearse cleanup/rewrite on production-shaped copies with concurrent workload, interruption, full disk, crash, replica failover, and isolated restore. Use supported online mechanisms, throttling, cancellation and cutover fences; preserve a backup and rollback only while formats/state remain compatible, otherwise define forward repair. Validate constraints, row counts and business aggregates, heap-index agreement, checksums, queries/plans/latency, replicas, backups, and actual OS allocation afterward.
