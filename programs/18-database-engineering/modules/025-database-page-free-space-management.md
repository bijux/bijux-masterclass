---
module_id: DBE-025
program: Database Engineering
level: 1
module_number: 25
title: Database Page Free-Space Management
status: complete
last_verified: 2026-08-30
---

# Database Page Free-Space Management

## One-Page Review

### Governing question

How can a database find a page likely to accept a record without scanning every page, while remaining correct when free-space information is quantized, stale, concurrent, damaged, or only conditionally reclaimable?

### Essential definitions

**Actual allocatable space** is what a latched page can accept under its current format and state. A **free-space map** (FSM) is auxiliary metadata summarizing candidate capacity across pages. A **bucket** quantizes a byte value into a smaller category. A **summary tree** stores an aggregate—often a maximum—so search can prune subtrees. A **false positive** advertises a page that no longer fits; it causes validation failure and retry. A **false negative** misses a page that fits; it causes avoidable search/extension but must not corrupt data. **Reclaimable space** cannot be allocated until visibility, cleanup, compaction, or other conditions hold. **Allocation metadata** answers whether pages/extents are owned; it is distinct from bytes available inside an owned page.

### Central model, mechanism, or theorem

Let leaf `q_i` be a conservative quantized summary for page `i`, and each internal tree node equal the maximum of its children. If the root is below the request bucket, no represented leaf qualifies; otherwise descending through a child whose maximum meets the request yields a candidate in logarithmic tree height. This proves only a property of the summary snapshot. Correct insertion still pins/latches the candidate, validates ownership/type and exact page space, then inserts or updates the summary and retries. Safe staleness affects performance; it must never authorize overwriting page data.

### Critical invariants

- Relation/tablespace generation, page number, allocation/ownership, page type, and summary entry refer to the same object state.
- Summary values use a documented unit, rounding direction, saturation rule, and definition of “available.”
- Every internal max equals or safely bounds its represented children under the implementation's repair/concurrency protocol.
- A candidate is revalidated on the actual page under the required latch before reservation.
- Slot, alignment, tuple, special-space, compression, and maximum-entry costs are included by the exact page function.
- Dead/versioned/fragmented space is not advertised as allocatable until cleanup makes it so.
- Failed insertion updates or penalizes stale optimistic entries and guarantees bounded retry/fallback progress.
- Metadata repair/rebuild never infers live-page ownership or frees bytes from an unauthenticated page image.

### Common failures

Failures include equating database free space with filesystem capacity; summing page holes that cannot hold one record; storing exact bytes when coarse categories suffice; rounding optimistically; trusting an FSM without latching the page; advertising dead tuples before snapshots release them; forgetting slot/alignment/row-format costs; hot-spotting the single fullest page; letting stale high entries cause retry storms; letting stale low entries cause uncontrolled growth; confusing extent allocation bitmaps with in-page capacity; WAL-logging hints as if they were primary truth—or failing to log metadata that is primary truth; and “repairing” summaries without scanning validated owning pages.

### Compact example

Eight pages have actual free bytes `(12,91,47,64,5,80,33,72)`. With 16-byte conservative buckets, summaries are `(0,80,32,64,0,80,32,64)` and root maximum 80. A 70-byte request selects page 1. If another inserter has reduced its actual space to 60, validation fails, the summary becomes 48, and retry selects page 5 with 80. After insertion page 5 has 10. If page 7 later gains 80 bytes but its stale summary remains 64, a new 70-byte search misses it; validated-page repair changes its bucket to 80 and makes it discoverable.

### Connections

[DBE-023](023-slotted-pages.md) defines exact page-local space, and [DBE-024](024-heap-files.md) needs cross-page candidate selection. [DBE-026](../ROADMAP.md) adds buffer pins/latches; [DBE-028](../ROADMAP.md) explains dirty metadata and writeback.

## Governing Question

Without auxiliary metadata, finding space in an `N`-page relation can require reading pages until one fits. A free-space structure turns this into a metadata search, but the answer ages immediately: concurrent writers consume space, deletes become reclaimable later, compaction changes contiguity, and crashes can leave hint metadata behind primary data.

Correct architecture separates discovery from authority. The summary proposes a candidate. The owning data page, interpreted under the current access method and protected by the correct latch, decides whether the record fits. If not, the database repairs the hint and retries or extends. This separation permits compact, approximate, lazily maintained, and sometimes reconstructible summaries without weakening data integrity.

## Why This Matters

Free-space management determines insert latency, relation growth, page density, cache traffic, latch contention, WAL/log volume, fragmentation, and maintenance. A poor structure can turn a constant-looking insert into repeated random page probes. A policy that always chooses the fullest eligible page can create a hot latch. A stale-low map can grow a table while reusable capacity sits idle.

The topic also prevents dangerous capacity reasoning. Free bytes inside a page, free pages inside an extent, unallocated extents in a tablespace, sparse filesystem blocks, snapshot-retained extents, and storage-pool headroom are different ledgers. Freeing one does not automatically increase another.

Finally, free-space metadata tests the boundary between correctness-critical state and optimization hints. Some engines can rebuild the structure from data pages and allow conservative loss; others incorporate allocation metadata whose loss changes ownership. Engineers must identify which state is authoritative before deciding logging, checksums, repair, and backup requirements.

## Prerequisites and Retrieval

Retrieve slotted-page bounds, tuple stored size, heap insertion, arrays, bitmaps, trees, quantization, integer rounding, latches, MVCC/undo, WAL/journaling, extents/tablespaces, checksums, buffer pools, and fault recovery.

Distinguish actual from advertised space; exact from quantized; false positive from false negative; immediately allocatable from reclaimable; page capacity from extent allocation; internal reuse from filesystem release; data truth from reconstructible hint; shared-memory cache from persistent map; logical relation identity from physical generation; and search policy from structural correctness.

## Learning Objectives

After this module, you should be able to:

1. derive bucket encodings and their rounding error;
2. construct and validate a max-summary tree;
3. trace candidate search, page recheck, retry, insertion, and summary update;
4. explain safe consequences of optimistic and pessimistic staleness;
5. distinguish page free-space summaries from allocation maps and filesystem capacity;
6. reason about concurrency, contention, fairness, and progress;
7. classify free-space metadata as authoritative or reconstructible by engine;
8. design repair, rebuild, and crash-recovery checks;
9. diagnose bloat, retry storms, and unnecessary extension; and
10. evaluate free-space strategies using workload and fault evidence.

## Core Exposition

The exact question “can this record fit?” belongs to the page access method. It considers header and slot-directory boundaries, available free line pointers, tuple alignment, record size, special space, maximum tuple/slot counts, compression representation, overflow policy, page state, and possibly space recoverable by an allowed prune/compact operation. A generic `upper-lower` subtraction can be wrong.

Cross-page selection needs a cheaper representation. At one extreme, a linked list holds pages in a “has space” class. It is compact but gives weak size discrimination and can be expensive to repair. A directory can store exact bytes per page but consumes metadata and update traffic. Buckets/bitmaps compress values. Hierarchical trees aggregate maxima or category availability, permitting logarithmic discovery and fast “none represented” decisions.

Quantization chooses an error direction. With bucket width `g`, conservative floor encoding `q(f)=floor(f/g)*g` never advertises more than the measured `f`, but can hide up to `g-1` usable bytes for a request tested against the lower bound. Category schemes instead encode fullness ranges. The search comparison must match the encoding semantics; mixing floor values with an optimistic threshold breaks the guarantee.

Exactness is not automatically better. A one-byte-per-page summary can keep a relation's map far smaller and hotter than eight-byte exact counters. The record's final fit is rechecked anyway. The right precision balances metadata footprint, cache locality, write/update frequency, false positives/negatives, record-size distribution, and page size.

PostgreSQL 18 documents one byte per represented heap page and max trees within and across FSM pages. The documented inspection interface states values are rounded at 1/256 of `BLCKSZ` and are not kept fully current. PostgreSQL's source README explains search by descending nodes whose maximum meets the request, updating a leaf then bubbling maxima upward, and repair/self-correction because the FSM acts as a hint. These are implementation facts, not a universal prescription.

SQL Server documents Page Free Space pages with one byte for each tracked page and coarse fullness categories for heap and LOB pages. It separately uses allocation maps for extents/pages. This illustrates two axes: ownership/allocation and residual capacity. An allocated page can be nearly empty; a free extent has no row page whose internal gap should be consulted.

Oracle documents automatic segment space management using bitmaps. Bitmap/category approaches support fast class membership and distribute searches but do not expose arbitrary exact byte counts. InnoDB's B-tree placement is constrained by key order; when a target leaf lacks space, page split/merge policy applies, so a heap-style choose-any-page FSM does not transfer directly.

The summary hierarchy resembles a segment tree. Leaf entries represent pages; a parent stores the maximum child category. A request begins at the root. If the maximum is too small, search fails without visiting leaves. Otherwise choose an eligible child until reaching a page entry. Across multiple metadata pages, upper levels summarize lower-level roots.

Tree validation requires more than root equality. Every node must have legal encoding and topology; each parent must equal or conservatively bound its existing children; leaf-to-data-page mapping must remain within current relation size/generation; unused leaves must have safe values; and cycles or impossible level/page addresses must be rejected. A root that looks plausible can hide an incorrect subtree.

Selection policy chooses among multiple eligible children. Always choosing the leftmost or fullest can concentrate insertions and latch contention. Round-robin/next-slot hints spread work; choosing near a recent page improves locality; randomized power-of-two choices can distribute contention; partitioned maps reduce shared hot nodes. Policy hints may tolerate races if their corruption affects only selection quality and they have a safe reset.

The insert lifecycle is: compute stored size; search metadata; pin and latch the candidate data page; validate identity/type/checksum/bounds and exact allocatable space; optionally prune/compact only if transaction rules permit; reserve slot/payload and apply WAL/undo; publish tuple; recompute page free space; update the summary; and retry/extend on failure. Buffer/latch order must avoid deadlocks between data and metadata pages.

Optimistic staleness means `advertised > actual`. It arises when another insert consumes space before the map update, updates are deferred/lost, or a summary parent stays high. A candidate then fails recheck. Correct behavior lowers/recomputes the entry and retries. Without feedback or a retry bound, many sessions can repeatedly select the same unusable page and stall.

Pessimistic staleness means `advertised < actual`. Deletion, pruning, compaction, rollback, or lost updates can create unadvertised capacity. Correctness remains intact, but the database may extend, consume different pages, or increase fragmentation. Periodic maintenance, page visits, vacuum, or targeted repair repopulates the map.

Quantization creates deliberate approximation even with fresh entries. A conservative lower bucket can miss a page near the threshold. A coarse fullness range can nominate a page that fails for a particular row. Therefore measure error distributions relative to actual stored row sizes—not just average map accuracy.

Immediately allocatable space differs from potentially reclaimable space. A page may contain dead tuple versions still visible to an old snapshot, deleted index entries awaiting cleanup, holes requiring compaction, or compressed data whose post-update size is uncertain. Advertising those bytes early can overwrite required data. A cleanup operation first proves reclaimability and changes the page; only then does the summary increase.

Updates complicate demand. A row-sized estimate can change with nulls, encoding, compression, out-of-line movement, alignment, version headers, or index record representation. Reserve against the exact stored object for the target page type. Growth headroom/fill factor is policy: leaving space for future updates can reduce splits/movement but lowers density.

Map updates can be eager or lazy. Eager updates reduce staleness but add contention and dirty/log traffic for every tuple change. Lazy updates batch work and keep hot data-page critical sections shorter, but increase retries and growth. Hybrid designs update on threshold crossings, failed probes, cleanup, or eviction/maintenance.

Whether metadata is WAL-logged depends on recoverability semantics. If an FSM is only a hint and insertion always validates the primary page, it may be rebuilt or conservatively reset after crash. If a bitmap establishes page/extent ownership, losing an update can double-allocate storage and is correctness-critical. Never copy one component's “not logged” policy to another without proving reconstruction and safe failure behavior.

Crash analysis enumerates orders: data-page change durable but map old; map change durable but data page old; relation extended but summary refers beyond durable size; parent updated but leaf torn; leaf valid but parent stale; recovery replays page change without auxiliary hint. Each state must lead to safe retry, repair, or recovery—not overwrite.

Repair begins from authoritative validated pages and allocation metadata. For each currently owned data page, compute exact allocatable space through the access method, quantize under current rules, rebuild leaves and parent summaries, and discard entries beyond relation size/generation. Repair does not mark unknown pages free or accept a checksum-failed page as empty. Corruption response preserves originals and uses supported tools.

Free-space maps themselves consume pages, buffer frames, I/O, checksums, backups, and maintenance. Their size grows roughly with represented page count divided by compression/entries per metadata page, plus upper levels. A compact hierarchy is usually shallow, but very large/partitioned relations and many small objects change cache behavior.

Monitoring should include insert probes/retries, candidates rejected for insufficient space or wrong page identity, summary updates, false-positive/negative samples, quantization error, pages extended, actual versus advertised distributions, map size/cache misses, hot metadata/data latches, compactions/prunes, dead/reclaimable bytes, page density, relation/filesystem growth, WAL/log from metadata/data changes, repair count/duration, and replica recovery behavior.

Testing needs empty/full/exact-fit pages; slot-limit despite byte space; sizes around every bucket boundary; saturated encodings; invalid tree topology/parents; stale-high/stale-low leaves; relation truncation/generation change; concurrent candidates; cleanup races; full disk; crash at data/map/parent/extension points; checksum failure; map loss/rebuild; and restored backup consistency. Workloads need skewed sizes and hot keys, not only uniform inserts.

The executable model below uses eight leaves, 16-byte conservative buckets, a max tree, left-first search, actual-page revalidation, stale-high retry, stale-low repair, and simple insert accounting. It is not PostgreSQL, SQL Server, Oracle, InnoDB, a concurrent allocator, or a recovery implementation.

<!-- bijux-verify: {"id":"free-space-summary-tree","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"encoded=(0, 80, 32, 64, 0, 80, 32, 64)\nroot=80\ncandidate_70=1\nstale_retry=(1, 60, 48)\nselected_70=(5, 80, 10)\ncandidate_25=1\nafter_25=(35, 32)\nfalse_negative=(None, 7, 80, 64)\nrepaired_candidate=7\ntree_valid=True\n","stderr":""}} -->
```python
class MaxSummary:
    def __init__(self, actual: list[int], quantum: int = 16) -> None:
        assert len(actual) > 0 and len(actual) & (len(actual) - 1) == 0
        self.actual = actual
        self.quantum = quantum
        self.base = len(actual)
        self.tree = [0] * (2 * self.base)
        for page in range(self.base):
            self.update(page)

    def encode(self, free_bytes: int) -> int:
        return free_bytes // self.quantum * self.quantum

    def update(self, page: int) -> None:
        node = self.base + page
        self.tree[node] = self.encode(self.actual[page])
        node //= 2
        while node:
            self.tree[node] = max(self.tree[node * 2], self.tree[node * 2 + 1])
            node //= 2

    def search(self, required: int) -> int | None:
        threshold = (required + self.quantum - 1) // self.quantum * self.quantum
        if self.tree[1] < threshold:
            return None
        node = 1
        while node < self.base:
            left = node * 2
            node = left if self.tree[left] >= threshold else left + 1
        return node - self.base

    def valid(self) -> bool:
        return all(
            self.tree[node] == max(self.tree[node * 2], self.tree[node * 2 + 1])
            for node in range(1, self.base)
        )


summary = MaxSummary([12, 91, 47, 64, 5, 80, 33, 72])
encoded = tuple(summary.tree[summary.base:])
root = summary.tree[1]
candidate_70 = summary.search(70)
summary.actual[candidate_70] = 60  # another writer consumed space before recheck
summary.update(candidate_70)
stale_retry = (candidate_70, summary.actual[candidate_70], summary.tree[summary.base + candidate_70])
selected = summary.search(70)
before = summary.actual[selected]
summary.actual[selected] -= 70
summary.update(selected)
selected_70 = (selected, before, summary.actual[selected])
candidate_25 = summary.search(25)
summary.actual[candidate_25] -= 25
summary.update(candidate_25)
after_25 = (summary.actual[candidate_25], summary.tree[summary.base + candidate_25])
summary.actual[7] = 80  # cleanup created space, but its summary update was delayed
false_negative = (summary.search(70), 7, summary.actual[7], summary.tree[summary.base + 7])
summary.update(7)
repaired_candidate = summary.search(70)

print(f"encoded={encoded}")
print(f"root={root}")
print(f"candidate_70={candidate_70}")
print(f"stale_retry={stale_retry}")
print(f"selected_70={selected_70}")
print(f"candidate_25={candidate_25}")
print(f"after_25={after_25}")
print(f"false_negative={false_negative}")
print(f"repaired_candidate={repaired_candidate}")
print(f"tree_valid={summary.valid()}")
```

The exact output proves only this finite summary lifecycle. The model deliberately makes tree entries conservative and permits delayed updates; it omits relation identity, page bytes, allocation, slots, cleanup eligibility, latches, WAL, checksums, contention policy, and crash recovery.

## Definitions and Notation

For page `i`, let `f_i` be exact immediately allocatable bytes under a latched page check. With quantum `g>0`, conservative encoded bytes are `q_i=g*floor(f_i/g)`, so `q_i<=f_i<q_i+g`. A full binary summary tree has leaves `q_i` and parent `m_v=max(m_left,m_right)`.

For request `r`, the teaching model uses threshold `t=g*ceil(r/g)`. A leaf with `q_i>=t` guarantees `f_i>=r` at measurement time, while a fitting page with `r<=f_i<t` can be missed. Concurrency can invalidate either relationship after measurement, so actual-page validation remains mandatory. Other engines use other category/rounding/search conventions.

## Mechanisms, Invariants, or Proof Structure

A correct free-space workflow is:

1. Resolve current relation/tablespace generation, access method, page size, allocation and map format.
2. Compute exact stored request size including slot/alignment/page-type rules.
3. Search summary metadata using its documented encoding and policy; validate tree/bitmap topology while reading.
4. Reject candidates outside current owned relation pages before data access.
5. Pin/latch the candidate and validate identity, page structure, integrity, state, and exact allocatable space.
6. If insufficient, recompute/lower the entry and retry with bounded progress or fallback.
7. If sufficient, mutate the page under WAL/undo/latch rules, then recompute and publish the summary safely.
8. Increase summaries only after cleanup has made bytes immediately reusable.
9. Extend only through allocation/initialization protocols and invalidate stale entries after truncation/rewrite.
10. Audit with actual-versus-advertised samples, fault recovery, rebuild, capacity, and workload evidence.

The max-tree search proof is inductive. The root represents the maximum leaf. If it is below `t`, every leaf is below `t`. Otherwise at least one child maximum meets `t`; choosing such a child preserves the existence claim until a leaf is reached. The proof concerns tree values in one snapshot, not actual data-page space or concurrent stability.

## Alternatives and Trade-Offs

Exact arrays provide precision and direct lookup but consume bytes and update/cache bandwidth. Quantized arrays are compact and sufficient for candidate discovery. Max trees add update/search work and metadata pages but prune large ranges. Bitmaps/category lists make class membership cheap but provide coarse sizes. Linked lists are simple but vulnerable to stale membership, hot heads, and repair cost.

Eager maintenance reduces staleness while increasing latch, log, and dirty-page pressure. Lazy maintenance favors write throughput but increases retries and relation growth. Conservative encoding avoids stale-free overwrites when paired with page validation but misses marginal fits. Optimistic categories find more candidates but require robust rejection feedback.

Choosing fullest eligible pages improves density but can hotspot; spreading writes lowers contention but may leave more partially filled pages. Locality-aware selection helps prefetch and write combining; randomization helps concurrency. Fill-factor/headroom policies deliberately report some physical free capacity as unavailable for ordinary insertion.

## Failure Modes and Misconceptions

- “Free space is one number.” Page, extent, tablespace, file, snapshot, and storage-pool ledgers differ.
- “The FSM is the allocator.” It proposes; the data page and allocation metadata authorize.
- “Exact counters are always superior.” Metadata footprint and update contention can dominate.
- “A max-tree root proves a row fits.” It proves only a represented summary condition.
- “Stale metadata is corruption.” Reconstructible hints can be safely stale; ownership maps cannot.
- “Deleted bytes are free.” Visibility/undo/recovery and compaction may still block reuse.
- “More total holes means a wide tuple fits.” One page needs sufficient allocatable space.
- “One failed candidate justifies extension.” Feedback/retry can find existing capacity.
- “Rebuild can trust unreadable pages as empty.” Integrity failure requires containment and recovery.
- “No WAL is fine for every space map.” Only state with proven reconstruction and safe loss may use hint semantics.

## Worked Examples

### Example 1

With 16-byte floor buckets, 91 bytes encodes as 80 and 47 as 32. Error is 11 and 15 bytes respectively, always in `[0,15]`. The encoding never claims more than the measurement.

### Example 2

Leaves `(0,80,32,64,0,80,32,64)` have root 80. A 70-byte request rounds threshold upward to 80; descending left-first reaches page 1. The tree avoids checking pages whose subtree maximum is below 80.

### Example 3

Before page 1 is latched, another writer reduces actual free from 91 to 60. The advertised 80 is stale-high. The inserter rejects the page, updates it to bucket 48, and retries rather than overwriting bytes or extending immediately.

### Example 4

Retry selects page 5 at actual 80. After inserting 70 bytes, actual free is 10 and conservative bucket zero. The summary update bubbles upward; future large searches no longer choose that branch unless another leaf qualifies.

### Example 5

A 25-byte request has threshold 32 and left-first search selects page 1, whose actual 60 fits. After insertion, actual 35 encodes 32. Page 2 at actual 47 would also fit; selection policy, not logical page order, decides among represented candidates.

### Example 6

Cleanup raises page 7 actual free from 72 to 80, but its map remains 64. A 70-byte query finds no candidate after other 80 buckets were consumed/lowered. This safe false negative can cause extension; repairing page 7's entry makes it discoverable.

### Example 7

A page contains 2 KiB of dead tuples visible to a long-running snapshot and 500 immediately free bytes. Advertising 2.5 KiB permits unsafe reuse. The summary reports only the access method's 500-byte allocatable result until cleanup proves the dead versions reclaimable.

### Example 8

The tree root is 96 but both children are at most 64. Even if all leaves are legal, parent aggregation is corrupt. Search validation detects the impossible parent, rebuilds from validated children or resets conservatively, and never treats the discrepancy as data-page free space.

### Example 9

After relation truncation, an old leaf refers to page 900 while current relation size ends at 700. Candidate resolution checks generation/size, clears or ignores the stale entry, and never reads an unrelated/reused page as part of the relation.

### Example 10

Insert p99 rises with 30 page probes per row while disk capacity is ample. Evidence shows one stale-high hot page, delayed feedback, and latch contention. The remedy is targeted entry correction/search spreading and verification—not an immediate table rewrite or more filesystem space.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies segment trees, bitmaps, quantization, free lists, and invariants.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies logarithmic search, approximation error, adversarial cases, and contention-aware policies.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies allocation bitmaps, files/extents, caching, latches, and persistence boundaries.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies capacity ledgers, observability, repair, fault injection, and incident handling.
- [Programming Languages — Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies race, publication, progress, and hot-spot reasoning.

## References

1. PostgreSQL Global Development Group, [Free Space Map](https://www.postgresql.org/docs/18/storage-fsm.html), PostgreSQL 18 map hierarchy and per-page summary documentation.
2. PostgreSQL Global Development Group, [`pg_freespacemap`](https://www.postgresql.org/docs/18/pgfreespacemap.html), PostgreSQL 18 precision and freshness caveats.
3. PostgreSQL Global Development Group, [Free Space Map implementation README](https://github.com/postgres/postgres/blob/master/src/backend/storage/freespace/README), search, update, concurrency, and self-repair design documentation.
4. Microsoft, [Pages and Extents Architecture Guide](https://learn.microsoft.com/en-us/sql/relational-databases/pages-and-extents-architecture-guide?view=sql-server-ver17), SQL Server PFS, GAM, SGAM, and IAM distinctions.
5. Oracle, [Database Concepts](https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/database-concepts.pdf), Oracle Database 23 bitmap-managed storage and automatic segment space management concepts.
6. Oracle, [InnoDB Physical Index Structure](https://dev.mysql.com/doc/refman/8.4/en/innodb-physical-structure.html), MySQL 8.4 ordered-page fill, split, and merge contrast.
7. Raghu Ramakrishnan and Johannes Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, file organization and free-space foundations.
8. Hector Garcia-Molina, Jeffrey D. Ullman, and Jennifer Widom, *Database Systems: The Complete Book*, 2nd ed., Pearson, 2008, page/file organization foundations.

## Exercises

### Exercise 1

For quantum 32, encode actual free bytes `(0,31,32,63,64,95,96,127)`. Give the root maximum, per-page quantization errors, and candidate pages guaranteed by the teaching threshold for requests 31, 64, and 97.

### Exercise 2

Build the array-form max tree for leaves `(16,48,0,32,80,16,64,0)`. Show a left-first search path for threshold 64, then update leaf 4 from 80 to 16 and bubble changes to the root.

### Exercise 3

Design a concurrency-safe insertion retry loop for a stale approximate map. Cover identity, latching, exact fit, feedback, progress, extension, and lock ordering.

### Exercise 4

Classify the failure consequences and recovery requirements for (a) a reconstructible per-page free-space hint, (b) a page-ownership allocation bitmap, and (c) a filesystem free-block bitmap. Explain why one logging policy cannot serve all three.

### Exercise 5

Create a production investigation for a growing table that reports substantial free space yet continues extending. Include definitions, samples, workload distributions, concurrency, visibility, maps, allocation layers, tests, and safe remediation.

## Answers to the Exercises

### Answer 1

Floor encodings are `(0,0,32,32,64,64,96,96)`. Errors are `(0,31,0,31,0,31,0,31)` and root maximum is 96. Request 31 rounds threshold to 32, so pages 2–7 whose encodings are at least 32 are guaranteed candidates except pages with zero; specifically 2,3,4,5,6,7. Request 64 has candidates 4,5,6,7. Request 97 rounds to 128 and has none, even page 7's actual 127 cannot fit 97? It actually can, illustrating that this deliberately conservative upward-threshold policy may create a false negative of as much as one quantum boundary; actual-page search conventions can reduce this differently but must preserve safe recheck semantics.

### Answer 2

Using one-based tree storage with leaves at indices 8–15: level above leaves is `(48,32,80,64)`, next level `(48,80)`, and root 80. Threshold 64 rejects the left root child 48, enters right child 80, then its left child 80, reaching leaf 4. Updating leaf 4 to 16 changes its parent from max(80,16)=80 to max(16,16)=16; the right upper node becomes max(16,64)=64; the root becomes max(48,64)=64. Unaffected branches remain unchanged.

### Answer 3

Compute exact stored demand under the target access method, search the current relation-generation map, and reject candidates outside owned pages. Pin/latch the candidate in documented order, validate page identity/type/integrity and exact allocatable space, and either insert under WAL/undo rules or release after publishing a recomputed lower summary. Track attempted candidates/version changes so retries make progress; spread searches to avoid a hot stale entry and cap probes before a safe rescan/repair/extension path. Extension must serialize allocation/initialization and handle full disk/short write. Avoid holding a data-page latch while acquiring metadata locks in an order that conflicts with update/repair paths.

### Answer 4

A reconstructible hint may safely be stale or lost if every allocation revalidates primary pages; crash recovery can reset/rebuild it, so logging may be reduced under a proven engine design. A page-ownership bitmap is primary allocation truth: a lost bit can double-allocate a page or leak it, so updates need atomic/logged recovery and strong integrity. A filesystem free-block bitmap governs storage beneath the database; corruption can cross files and requires filesystem journal/check/repair semantics. Their authorities, failure scopes, and reconstruction sources differ, so copying “hint, not WAL-logged” from (a) to (b) or (c) is unsafe.

### Answer 5

Define reported free space by layer and whether it is exact, quantized, current, contiguous, immediately allocatable, or only reclaimable. Sample validated data pages across size/age/partition strata and compare actual access-method space with map entries; capture row stored-size tails, slot/overflow costs, insert retries, chosen pages, extensions, latch contention, map cache/update lag, dead versions, long snapshots/undo retention, compaction needs, fill policy, and relation/tablespace/filesystem/snapshot capacity. Reproduce with concurrent production-shaped inserts and crashes on a disposable copy. Remedies may include clearing stale-high entries, repopulating stale-low summaries through supported maintenance, ending legitimate visibility blockers, tuning selection/update policy, or governed rewrite/shrink only when measured benefit exceeds log/headroom/replica/backup risk. Validate constraints, heap-index agreement, page integrity, growth, retries, latency, replicas, and isolated restore afterward.
