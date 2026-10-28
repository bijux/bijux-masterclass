---
module_id: DBE-023
program: Database Engineering
level: 1
module_number: 23
title: Slotted Pages
status: complete
last_verified: 2026-08-30
---

# Slotted Pages

## One-Page Review

### Governing question

How can a fixed-size page hold variable-size records, reclaim fragmented space, and preserve a useful logical record reference even when payload bytes move inside the page?

### Essential definitions

A **slotted page** separates a directory of small record locators from record payloads. A **slot** or **item identifier** records an offset, length, and state for one item. A **record identifier** (RID) commonly combines page identity and slot index. **Contiguous free space** is the immediately allocatable gap between directory and payload frontier; **total free space** also includes reusable holes. **Compaction** moves live payloads together and rewrites their slot offsets. **Slot reuse** assigns a freed index to a new record and can make a stale RID name different data unless a higher-level protocol prevents or detects it.

### Central model, mechanism, or theorem

In the canonical teaching layout, a fixed header and slot directory grow upward while payloads grow downward. If `L=H+nS` is the directory end and `U` is the lowest packed payload offset, insertion of length `r` needing a new slot is possible when `r+S <= U-L`; reuse of a free slot needs only `r <= U-L`. Compaction may change payload offsets but preserves each live slot index, so page-plus-slot references remain valid across that compaction. This stability ends when the slot is freed, the page is rewritten, or the engine’s documented lifetime ends.

### Critical invariants

- `0 <= H <= L <= U <= special <= page_size`, with checked arithmetic.
- Every live slot has a valid state, positive permitted length, and interval inside the payload region.
- Live payload intervals do not overlap one another, directory, header, or special space.
- Directory count and boundary metadata agree; free slots never expose stale payload as live.
- Compaction copies bytes safely, updates every moved slot, and publishes the page atomically under latch/log rules.
- Slot ordering semantics—identity order, key order, or physical order—come from the exact page type and engine.
- A page checksum or LSN does not replace structural validation.
- A RID is an internal/versioned locator, not a durable application identifier.

### Common failures

Failures include treating total free bytes as one contiguous insertion region; forgetting slot overhead; moving records without updating locators; renumbering live slots during heap-page compaction; assuming all engines keep slots in insertion order; following malformed offsets before bounds checks; overlapping copies during compaction; reusing a slot while stale references remain; exposing half-compacted pages to readers or recovery; advertising free space before the page mutation commits; and repairing a slot table by guessing from recognizable payload bytes.

### Compact example

On a 256-byte pedagogical page with 16-byte header and 4-byte slots, inserting payloads of 40, 30, and 50 bytes produces directory end 28, payload frontier 136, and 108 contiguous free bytes. Deleting the 30-byte item leaves 108 contiguous but 138 total free bytes. Compaction moves the 50-byte payload from offset 136 to 166, keeps its slot index 2, and makes all 138 bytes contiguous. A later 60-byte insert can reuse freed slot 1 without growing the directory, but `(page 7, slot 1)` now denotes a different record.

### Connections

[DBE-021](021-pages-blocks-and-database-files.md) defines page boundaries, and [DBE-022](022-record-and-tuple-layout.md) defines record bytes. [DBE-024](../ROADMAP.md) uses pages inside heap files; [DBE-025](../ROADMAP.md) tracks page-level free-space availability.

## Governing Question

Variable-length records create a tension. Packing payloads directly makes iteration simple, but deleting or enlarging one record leaves holes or forces movement. Exposing raw offsets as record addresses then makes every movement invalidate external references. A slotted page inserts a stable level of indirection: clients name a directory entry, while that entry points to the current payload location.

The mechanism is simple enough to sketch and subtle enough to corrupt a database. The page must account for directory growth and payload growth, distinguish contiguous from fragmented free space, maintain non-overlap, coordinate concurrent readers, log changes for crash recovery, and define when slot identity can be reused. Different page types also give the directory different meanings. The governing problem is therefore lifecycle-correct indirection, not merely drawing arrows from slots to records.

## Why This Matters

Slotted pages are a bridge between logical access and mutable bytes. Heap scans, tuple identifiers, B-tree cells, update placement, vacuum, page splits, free-space maps, recovery, and inspection all depend on their invariants. One corrupt offset can misdirect a parser into another record, free space, or page metadata. One stale free-space estimate can cause a failed insert and retry; one stale RID can return the wrong row if reuse is not governed.

Page-local compaction avoids changing every reference when payloads move. It can reclaim holes without rewriting the whole relation, but costs memory copying, latch duration, log volume, and dirty-page work. Whether to compact, reuse a hole, move a record, split a page, or choose another page is a policy decision informed by workload and page type.

Operationally, “the page has 2 KiB free” is incomplete. It may mean a contiguous gap, total holes, reclaimable dead tuples, space available only after pruning, or an approximate value in a free-space map. Engineers need precise state and evidence to explain insert failures, fragmentation, page density, and maintenance behavior.

## Prerequisites and Retrieval

Retrieve arrays, offsets, lengths, exclusive intervals, checked integer arithmetic, variable-size allocation, fragmentation, stable versus unstable identifiers, page and tuple layout, latches, transactions, write-ahead logging, checksums, B-tree ordering, and heap files.

Distinguish slot index from payload offset; live from dead from free/redirection state; contiguous from total from reclaimable space; page compaction from file compaction; physical order from logical/key order; page latch from transaction lock; checksum validity from structure validity; and reference stability across movement from stability across deletion/reuse.

## Learning Objectives

After this module, you should be able to:

1. derive slotted-page boundaries and insertion capacity;
2. validate slot intervals, states, and non-overlap;
3. distinguish contiguous, fragmented, and reclaimable space;
4. trace insertion, deletion, compaction, update, and slot reuse;
5. explain which references compaction preserves and which it does not;
6. compare heap-page and ordered-page directory semantics;
7. design latch/log publication for page mutations;
8. diagnose malformed and half-applied page operations safely;
9. estimate compaction trade-offs from workload evidence; and
10. test page operations with boundary and crash cases.

## Core Exposition

A page begins with engine-defined metadata: page type and format, boundaries, state flags, recovery position, checksum, transaction/pruning hints, or access-method data. The directory contains fixed-size or compact entries. Payloads occupy another region, often from the opposite end. The unused gap permits either another directory entry, another payload, or both.

The two-ended layout is a convention, not a universal direction. PostgreSQL documents a header and item-identifier array growing from the front while items are allocated backward from the free-space end. SQL Server documents data rows growing after the header while its two-byte slot array grows backward from the page end. Both implement indirection, but copying one engine's offset arithmetic into another would be wrong.

SQLite B-tree pages likewise have a cell-pointer array and cell content region. Its pointer array is arranged in key order; freeblocks and one-to-three-byte fragments may occur in the cell region; page defragmentation packs cells at the end. A heap page's slot number may act as a stable local identity, while an ordered B-tree directory may be rearranged to preserve key order. “Slot” does not imply one universal identity contract.

For a teaching page of size `P`, header `H`, `n` directory entries each `S` bytes, and optional special region starting at `Q`, let `L=H+nS`. Let `U` be the lowest byte of the packed payload suffix. The immediately free interval is `[L,U)` and has length `U-L`. A new record of stored length `r` fits with a new slot only if both `S` and `r` fit. If a free slot entry can be reused, directory growth is unnecessary.

Real formats add alignment, variable slot metadata, reserved bytes, minimum record sizes, overflow rules, prefix compression, page trailers, and transaction state. Use exact format rules. Always calculate with an exclusive end and checked addition/subtraction; unsigned underflow can transform an impossible insert into a huge apparent gap.

A slot normally carries offset and length plus state bits. States may mean live/normal, unused, dead, redirected, forwarding, ghost, or access-method-specific forms. Offset zero cannot be assumed free unless specified. State must be validated before interpreting other bits, and impossible combinations must fail closed.

The RID `(page_id, slot_index)` introduces page-local indirection. When compaction moves a live payload and rewrites its slot offset, the RID stays the same. This is valuable for heap references and index locators. But the page ID itself can be reused after deallocation, a slot can be freed and reused, a table rewrite can create new physical identities, and MVCC can create another tuple version. An application key has a different lifetime and purpose.

Insertion first determines record's stored size under the tuple format, including alignment and possible overflow reference. It chooses or confirms a page, acquires the required latch, revalidates space under that latch, selects a free slot or reserves a new one, reserves payload bytes, copies the record, publishes slot and boundary state in the engine-defined order, writes recovery information, marks the buffer dirty, and updates higher-level free-space metadata. The exact log-before-data and latch protocol is engine-specific.

Reservation and publication order matters even in memory. Publishing a live slot before complete payload bytes lets a concurrent reader see partial data. Copying payload first into space not yet reachable and publishing the slot last is a common pattern, but recovery, checksums, memory ordering, and engine-specific critical sections still govern correctness. A high-level language assignment is not automatically a crash-atomic page mutation.

Deletion has logical and physical forms. Under MVCC, delete may mark a tuple version and retain it for snapshots or recovery. Later pruning/vacuum determines that bytes are reclaimable. Immediate physical deletion may mark the slot free and create a hole. Do not reclaim a record while a reader, undo chain, index entry, or replica/recovery process can still require it.

A hole is an unused interval inside the payload region. Some formats chain freeblocks, retain fragment counts, or simply recover holes during compaction. Total free bytes equal the central unallocated gap plus eligible holes/fragments. A record larger than every individual hole may still fail without compaction even when their sum is sufficient.

Compaction constructs a new packed arrangement of live payloads and updates slots. An in-place algorithm must handle overlapping source/destination ranges correctly; copying in the wrong order with an unsafe primitive destroys bytes. A safer conceptual algorithm builds a validated move plan or scratch image, copies all live records, validates the prospective page, then publishes it under the engine's latch/log protocol.

Compaction should preserve live slot indices where the page's identity contract requires it. It may reorder physical payload bytes without changing scan or key order because the directory mediates access. However, ordered directories themselves may need insertion/deletion shifts. In that design, record identity may live elsewhere or be intentionally unstable. State the contract for the page type.

Free slot reuse saves directory bytes. It also creates an ABA problem: an observer retains `(p,s)`, the original record is deleted, and a different record takes the same `(p,s)`. The numeric address looks unchanged although identity changed. Engines control this through latches, MVCC visibility, pins, generations elsewhere, validation against tuple metadata, or by limiting who may retain physical identifiers. A bare RID is not proof of object identity.

Updates that shrink can overwrite or relocate and leave a hole. Growth may fit in adjacent space, use another hole, compact, move to the free frontier, create a forwarding/redirection entry, create a new MVCC version, or choose another page. Each choice changes write amplification, reference stability, fragmentation, recovery, and read indirection. The tuple format and concurrency scheme constrain the policy.

Slots also affect scans. A directory lets the engine enumerate candidate records without parsing free space. A heap scan can visit live slots and consult tuple visibility. An ordered B-tree scan follows logical/key directory order, not physical byte order. State bits can skip known-unused entries, but hints must be safe when stale.

The page boundary fields and directory count must agree. In PostgreSQL's documented layout, `pd_lower` determines the item-identifier extent, `pd_upper` the payload frontier, and `pd_special` the access-method region. In SQLite, cell count determines pointer-array length, while header fields locate cell content, freeblocks, and fragments. Validation must be per format/page type rather than a generic five-field guess.

Structural validation begins without dereferencing slots. Verify page identity/type/version/size, checksum or authenticated envelope where applicable, and all top-level boundaries. Derive maximum entry count from available bytes. Then validate each state and interval, using widened checked arithmetic. Sort live intervals by offset to prove non-overlap. Validate freeblock chains for bounds, ordering, cycles, minimum sizes, and totals. Only then decode record payload.

A checksum match says bytes satisfy a checksum relation; it does not prove offsets are in range, intervals disjoint, or states semantically possible. Conversely, a checksum failure means normal interpretation is unsafe, even if slot/payload shapes look plausible. Recovery should use supported logs, replicas, backups, or repair tooling on protected copies—not a hand-edited directory.

Page mutation interacts with WAL/journaling. Recovery must never observe directory and payload changes in an impossible combination. The log may describe logical insert/delete, physical byte ranges, a full-page image, or another engine-specific operation. Page LSN/generation and checksum must correspond to the final image. Fault tests should crash at each reservation, copy, slot publication, boundary update, log flush, and page-write point.

Concurrency requires a page latch or equivalent memory-structure protocol separate from transaction locks. A latch protects short physical invariants while a lock/MVCC rule protects logical isolation. Holding a latch during expensive compaction increases contention; releasing it halfway exposes invalid structure. Engines may plan outside and revalidate inside, limit compaction work, or defer maintenance.

Free-space maps summarize candidate pages but can be approximate or stale. The inserting thread must recheck actual contiguous/usable space under the page latch. After deletion, space may not be immediately reusable; after compaction, the map may lag. DBE-025 treats cross-page free-space discovery in detail.

Observability should distinguish insert attempts, no-space retries, compactions, bytes moved, holes, contiguous versus total free, dead/prunable bytes, slot utilization, free-slot reuse, page splits, latch wait/hold time, WAL bytes, dirty pages, and corruption findings. Sample safely through supported engine tools; scanning raw production files can race with writers or bypass encryption/checksums.

The following finite model demonstrates heap-style slot stability during compaction and the stale-RID hazard after slot reuse. It uses a 256-byte page, 16-byte header, four-byte slots, no alignment, no special space, and abstract payload identities. It is not a vendor format, concurrent implementation, WAL protocol, or byte parser.

<!-- bijux-verify: {"id":"slotted-page-lifecycle","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial_slots=((216, 40, 'live'), (186, 30, 'live'), (136, 50, 'live'))\ninitial_bounds=(28, 136, 108)\nafter_delete=(108, 138)\nafter_compact=((216, 40, 'live'), (0, 0, 'free'), (166, 50, 'live'))\ncompacted_bounds=(28, 166, 138)\nstable_payloads=True\nreused=(1, (7, 1), 106, 60)\nfinal_bounds=(28, 106, 78)\nvalid=True\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass
class Slot:
    offset: int
    length: int
    state: str
    payload: str | None


class Page:
    size = 256
    header = 16
    slot_size = 4

    def __init__(self) -> None:
        self.slots: list[Slot] = []
        self.upper = self.size

    @property
    def lower(self) -> int:
        return self.header + len(self.slots) * self.slot_size

    def contiguous_free(self) -> int:
        return self.upper - self.lower

    def total_free(self) -> int:
        holes = sum(slot.length for slot in self.slots if slot.state == "free")
        return self.contiguous_free() + holes

    def insert(self, payload: str, length: int) -> int:
        reusable = next((i for i, slot in enumerate(self.slots) if slot.state == "free"), None)
        slot_cost = 0 if reusable is not None else self.slot_size
        assert length + slot_cost <= self.contiguous_free()
        self.upper -= length
        new_slot = Slot(self.upper, length, "live", payload)
        if reusable is None:
            self.slots.append(new_slot)
            return len(self.slots) - 1
        self.slots[reusable] = new_slot
        return reusable

    def delete(self, index: int) -> None:
        slot = self.slots[index]
        assert slot.state == "live"
        slot.state = "free"
        slot.payload = None

    def compact(self) -> None:
        cursor = self.size
        for slot in self.slots:
            if slot.state == "live":
                cursor -= slot.length
                slot.offset = cursor
            else:
                slot.offset = 0
                slot.length = 0
        self.upper = cursor

    def valid(self) -> bool:
        live = sorted(
            (slot.offset, slot.offset + slot.length)
            for slot in self.slots if slot.state == "live"
        )
        return (
            self.header <= self.lower <= self.upper <= self.size
            and all(self.upper <= start < end <= self.size for start, end in live)
            and all(left[1] <= right[0] for left, right in zip(live, live[1:]))
        )


page = Page()
for identity, length in (("A", 40), ("B", 30), ("C", 50)):
    page.insert(identity, length)
initial_slots = tuple((s.offset, s.length, s.state) for s in page.slots)
initial_payloads = (page.slots[0].payload, page.slots[2].payload)
initial_bounds = (page.lower, page.upper, page.contiguous_free())
page.delete(1)
after_delete = (page.contiguous_free(), page.total_free())
page.compact()
after_compact = tuple((s.offset, s.length, s.state) for s in page.slots)
compacted_bounds = (page.lower, page.upper, page.contiguous_free())
stable_payloads = initial_payloads == (page.slots[0].payload, page.slots[2].payload)
reused_index = page.insert("D", 60)
reused = (reused_index, (7, reused_index), page.slots[reused_index].offset, 60)

print(f"initial_slots={initial_slots}")
print(f"initial_bounds={initial_bounds}")
print(f"after_delete={after_delete}")
print(f"after_compact={after_compact}")
print(f"compacted_bounds={compacted_bounds}")
print(f"stable_payloads={stable_payloads}")
print(f"reused={reused}")
print(f"final_bounds={(page.lower, page.upper, page.contiguous_free())}")
print(f"valid={page.valid()}")
```

The model deliberately discards freed length during compaction and reuses the slot. A real engine must additionally govern bytes, alignment, MVCC, generations, ordered indexes, latching, logging, recovery, and checksums.

## Definitions and Notation

For page size `P`, header end `H`, fixed slot size `S`, allocated slot count `n`, payload frontier `U`, and special-space start `Q`:

- directory end `L=H+nS`;
- contiguous free interval `[L,U)` and bytes `F_c=U-L`;
- eligible hole intervals `h_j=[a_j,b_j)` with bytes `b_j-a_j`;
- total immediately reclaimable bytes `F_t=F_c+sum_j(b_j-a_j)` under the page's state rules;
- a live slot `i` denotes interval `[o_i,o_i+r_i)`.

Validity requires checked arithmetic, `0<=H<=L<=U<=Q<=P`, permitted slot states, and every live interval within the payload region and disjoint from all other live intervals. An insertion of stored length `r` needs `r+S<=F_c` for a new slot or `r<=F_c` for a reusable slot in this simplified packed model.

## Mechanisms, Invariants, or Proof Structure

A safe page operation follows a proof obligation, not only a mutation recipe:

1. Authenticate page identity, type, format version, expected size, and integrity envelope.
2. Validate header boundaries and derive the maximum possible directory length.
3. Validate every slot state and interval without decoding payloads; prove non-overlap.
4. Determine logical visibility/reclaimability separately from physical free state.
5. Acquire the required latch, then revalidate slot and space state.
6. Build a checked insertion/deletion/move plan including directory cost, alignment, and special space.
7. Emit or reserve recovery information according to the engine protocol.
8. Copy payload with overlap-safe semantics; publish slot and boundary changes in a reader-safe critical section.
9. Revalidate the prospective page, update recovery/checksum metadata, mark dirty, and release the latch.
10. Update approximate higher-level space metadata and verify through supported inspection/fault tests.

Compaction stability follows directly from indirection: a RID resolves through slot `s`, and compaction changes only that slot's stored offset while leaving `s` and its logical payload association unchanged. The claim requires exclusive mutation, complete slot updates, and no slot freeing/reuse. Once any premise fails, the stability conclusion no longer follows.

## Alternatives and Trade-Offs

Direct packed records minimize directory overhead but make movement invalidate raw offsets and complicate variable-length deletion. Fixed-size slots simplify arithmetic and random lookup but impose per-record cost. Variable/encoded slots save space but complicate bounds checks. Forwarding records preserve a location across cross-page movement but add another read and chain-management risk.

Immediate compaction maximizes contiguous space but spends CPU, memory bandwidth, latch time, WAL, and dirty writes. Deferred compaction makes mutations cheaper but increases fragmentation and failed-page probes. Hole reuse avoids moving records but needs size selection and can create small fragments. Page split or cross-page move avoids long local work but changes higher-level structures.

Identity-ordered heap slots favor stable local locators. Key-ordered cell arrays favor ordered navigation and may shift entries. A generation-tagged RID reduces stale-reuse ambiguity but costs bits/storage and still needs wraparound rules. Logical keys remain more durable but require index lookup and can themselves change under application semantics.

## Failure Modes and Misconceptions

- “Total free means the next record fits.” The bytes may be split into holes.
- “A slot is the record.” It is metadata that locates and describes payload.
- “Compaction changes every RID.” Proper heap-style indirection preserves live slot indices.
- “Slot indices never change meaning.” Freeing and reuse can create stale-RID aliasing.
- “All slot arrays are insertion ordered.” Some are key ordered or page-type specific.
- “Delete makes bytes immediately reusable.” MVCC readers, undo, indexes, or recovery can retain them.
- “Copy records and fix slots later.” Readers/crash recovery can observe the invalid intermediate page.
- “A checksum-clean page is structurally sound.” Offsets, states, and intervals still need validation.
- “The free-space map is authoritative.” Candidate metadata may be approximate or stale.
- “Editing the bad offset repairs the page.” It can hide evidence and violate transactional/index invariants.

## Worked Examples

### Example 1

With `P=256`, `H=16`, `S=4`, and three slots, `L=28`. Payloads occupy `[136,186)`, `[186,216)`, and `[216,256)` in physical-offset order, so `U=136` and contiguous space is 108 bytes. Directory order need not equal physical-offset order.

### Example 2

A new 106-byte record appears to fit in 108 contiguous bytes, but a new slot costs four bytes. It needs 110, so insertion fails. If a free slot exists, the same payload fits because directory growth is zero. Capacity calculations must include metadata.

### Example 3

Deleting the 30-byte middle payload creates hole `[186,216)`. The central gap remains 108 bytes while total eligible space becomes 138. A 120-byte record cannot be placed without compaction even though the total exceeds 120.

### Example 4

Compaction keeps payload A at slot 0 and moves C from offset 136 to 166 while it remains slot 2. `(page 7,slot 2)` still resolves to C. Any raw pointer to offset 136 is invalid, showing why the slot is the supported indirection.

### Example 5

After slot 1 is freed, inserting D reuses it. A stale `(7,1)` formerly meant B and now means D. Consumers must not retain bare physical locators beyond the engine's documented lifetime or must validate version/generation/tuple identity.

### Example 6

Slots claim `[100,140)` and `[130,170)`. Each interval is individually inside a 256-byte page, yet they overlap. Validation sorts live intervals and rejects because 140 is greater than the next start 130.

### Example 7

An update grows a 40-byte record to 70 bytes. No adjacent hole exists, but 90 contiguous bytes remain. The engine can copy the new version at the frontier, update its slot atomically, and turn the old interval into a hole; under MVCC it may instead require a distinct slot/version until older snapshots end.

### Example 8

A B-tree cell-pointer array is key ordered. Inserting a middle key shifts pointer entries even though cell bodies remain elsewhere. Treating pointer index as a stable heap RID would be incorrect; page-type semantics control identity.

### Example 9

A crash occurs after payload copy but before slot publication. If the new bytes were unreachable and the WAL protocol replays or discards them, recovery can restore a valid page. If the slot was published first without recoverable payload, readers/recovery see a live entry pointing to incomplete data.

### Example 10

An insert repeatedly chooses a page advertised with 500 free bytes but finds only 100 contiguous and non-reclaimable holes. The engine rechecks under latch, updates the stale summary, and tries another page or compacts by policy. Operators measure retries, false-positive candidates, compaction cost, and map refresh lag.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies arrays, indirection, free lists, interval validation, and packed-memory structures.
- [Programming Languages — Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) supplies checked arithmetic, overlap-safe copying, parsing, and memory-order reasoning.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies pages, latches, cache residency, writes, and crash boundaries.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies hostile-input validation, resource caps, integrity, and evidence preservation.
- [Software Engineering — Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies property, model, fuzz, and fault-injection testing.

## References

1. PostgreSQL Global Development Group, [Database Page Layout](https://www.postgresql.org/docs/18/storage-page-layout.html), PostgreSQL 18 page headers, item identifiers, free space, and stable slot-index documentation.
2. SQLite Project, [Database File Format](https://www.sqlite.org/fileformat.html#b_tree_pages), SQLite B-tree pointer arrays, cell regions, freeblocks, fragments, and defragmentation documentation.
3. Microsoft, [Pages and Extents Architecture Guide](https://learn.microsoft.com/en-us/sql/relational-databases/pages-and-extents-architecture-guide?view=sql-server-ver17), SQL Server page header, rows, free space, and slot-array documentation.
4. Oracle, [Physical Structure of an InnoDB Index](https://dev.mysql.com/doc/refman/8.4/en/innodb-physical-structure.html), MySQL 8.4 index-page organization documentation.
5. Oracle, [InnoDB On-Disk Structures](https://dev.mysql.com/doc/refman/8.4/en/innodb-on-disk-structures.html), MySQL 8.4 physical-storage documentation.
6. Raghu Ramakrishnan and Johannes Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, record and page organization foundations.
7. Hector Garcia-Molina, Jeffrey D. Ullman, and Jennifer Widom, *Database Systems: The Complete Book*, 2nd ed., Pearson, 2008, secondary-storage and record-layout foundations.

## Exercises

### Exercise 1

A 4096-byte page has a 32-byte header, 128-byte special region, 4-byte slots, five allocated slots, and packed live payload totaling 600 bytes. Compute directory end, payload frontier, contiguous free bytes, and the largest record insertable with a new slot versus a reusable slot.

### Exercise 2

A page has contiguous free space 90 and holes of 25, 40, and 12 bytes. Determine whether records of 80, 100, and 150 bytes can be inserted without compaction when a free slot exists, and whether they can fit after compaction. Ignore alignment.

### Exercise 3

Design structural validation for a page with live, free, and redirected slots plus a freeblock chain. Include arithmetic, overlap, cycles, payload decoding order, and resource limits.

### Exercise 4

Compare immediate compaction, hole reuse, forwarding, and cross-page movement for an update-heavy variable-record workload. Cover reference stability, reads, writes, latches, logging, fragmentation, and recovery.

### Exercise 5

Design a crash/concurrency test campaign for slotted-page insertion, deletion, compaction, and slot reuse. State the oracles and evidence needed to distinguish structural validity from transactional correctness.

## Answers to the Exercises

### Answer 1

Usable space ends at `4096-128=3968`. Directory end is `32+5*4=52`. Packed payload frontier is `3968-600=3368`, so contiguous free space is `3368-52=3316`. With a new four-byte slot, the largest record is 3312 bytes; with a reusable slot it is 3316 bytes. Real formats may impose alignment, maximum inline length, or page-type minimums.

### Answer 2

Without compaction and with a reusable slot, 80 fits the 90-byte contiguous gap. Records 100 and 150 do not; no individual hole helps, and this simple policy does not combine holes. Total space after compaction is `90+25+40+12=167`, so all three sizes fit individually after compaction. This says nothing about simultaneous insertion of all three, which would require 330 bytes.

### Answer 3

First validate page identity, version, type, integrity envelope, and top-level bounds using widened checked arithmetic. Derive the maximum directory count and require the declared count to fit. Validate each state before its state-specific fields: live intervals must have legal lengths and lie wholly in payload space; free entries expose no live target; redirections point to a permitted target and obey chain/cycle/depth rules. Sort live intervals to prove non-overlap with one another and metadata. Walk the freeblock chain with a visited set, monotone/bounds/minimum-size rules, checked totals, and no overlap with live intervals. Only after structure passes should bounded tuple decoders run. Cap slot count, chain depth, allocation, decompression, and diagnostic output.

### Answer 4

Immediate compaction maximizes contiguous space and preserves live heap-slot IDs, but moves many bytes, lengthens latches, dirties/logs more data, and magnifies crash-critical work. Hole reuse minimizes movement when a suitable hole exists but needs selection metadata and can worsen small-fragment distribution. Forwarding preserves an old locator across movement but adds reads, chain limits, cleanup, and recovery states. Cross-page movement finds space elsewhere and may avoid local compaction, but changes physical identity or needs forwarding/new MVCC version and updates higher structures. Choose using width/change distributions, read locality, latch contention, WAL budget, failure behavior, and engine rules.

### Answer 5

Use a reference model and generate boundary sizes, full directories, free-slot/no-free-slot cases, adjacent and scattered holes, overlapping/malformed intervals, and repeated reuse. Run concurrent readers, inserters, deleters, and compactors under race instrumentation; crash after log reservation/flush, payload reservation/copy, slot publication, boundary/checksum update, dirty marking, and free-space-map update. After each restart, use version-matched recovery and assert page bounds, legal states, non-overlap, slot-to-payload identity for live pre-crash records, no prematurely reclaimed visible versions, constraints/index agreement, and committed/aborted transaction outcomes. Preserve operation seeds, exact tool/build/storage settings, logs, page hashes/images, and SQL-level reconciliation. A structurally valid page can still expose an uncommitted row, so both structural and transaction/reference-model oracles are required.
