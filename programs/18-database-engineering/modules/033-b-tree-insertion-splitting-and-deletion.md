---
module_id: DBE-033
program: Database Engineering
level: 1
module_number: 33
title: B+ Tree Insertion, Splitting, and Deletion
status: complete
last_verified: 2026-08-30
---

# B+ Tree Insertion, Splitting, and Deletion

## One-Page Review

### Governing question

How can a B+ tree absorb inserts and deletes while preserving sorted search, occupancy, reachability, recoverability, and concurrency guarantees when one logical mutation can change several pages?

### Essential definitions

An **insertion position** is the total-order location of a new physical key in a leaf. A **split** replaces one overflowing page by two ordered siblings and publishes a parent separator for the new right page. **Separator propagation** can overflow an internal page and recurse upward; splitting the root creates a new root. **Logical deletion** makes an entry/version ineligible for future reads, **physical entry deletion** removes its index representation, and **page reclamation** makes storage reusable only after no valid observer can reference the old page incarnation. **Underflow repair** restores a chosen minimum occupancy by **redistribution** from a sibling or **merge** with a sibling, then repairs the parent. A **fence/high key** bounds a page's key range; a **right link** lets a B-link search recover when a concurrent split has not yet been published in the parent.

### Central model, mechanism, or theorem

In the stable teaching model, descend by the complete comparator, insert/delete in the target leaf, and repair upward. Overflow is repaired by partitioning ordered entries, linking the new right page, and inserting its lower bound plus downlink into the parent. Underflow is repaired by borrowing while updating the separating pivot, or by merging and removing one parent separator/downlink. Root overflow increases height; a root with one remaining child can decrease height. Local order, range partition, occupancy, uniform leaf depth, parent/child reachability, and leaf-chain order imply that search and range-scan behavior from DBE-032 remains valid. Production publication, logging, visibility, and reclamation require stronger protocols than this stable-state argument.

### Critical invariants

- Leaf entries and internal pivots follow one complete physical comparator, including duplicate tie-breakers.
- Every live key belongs to exactly one reachable leaf range; parent separators agree with their declared convention.
- A split publishes a valid right-reachable state before depending on a possibly delayed parent downlink.
- Non-root pages satisfy byte/slot occupancy policy in stable states; temporary exceptions are named protocol states.
- All leaves remain at one depth; internal child count matches the separator convention.
- A redistribution repairs both sibling contents and their parent pivot; a merge removes exactly one child relationship.
- WAL or another recovery protocol makes every persisted intermediate state redoable/undoable as specified; page writes need not occur together.
- Logical visibility, physical tuple removal, unlinking, and storage reuse are separate transitions.
- A page identifier cannot be reused while a reader may interpret it as the former page; generation/epoch/pin rules close that race.
- Validation checks the root, every reachable page, sibling chain, key ranges, occupancy, cycles, and orphan/leak accounting.

### Common failures

Failures include splitting by entry count when byte occupancy is what matters; copying the wrong separator; forgetting to repair a parent after borrow; losing duplicates through an incomplete comparator; publishing a parent downlink before the new child is durable/reachable; treating several page writes as physically atomic; eagerly merging under a production latch protocol that cannot make it safe; confusing an MVCC delete with immediate index removal; recycling an unlinked page too early; permitting half-splits forever; letting sequential inserts create a hot right edge; testing only final key membership; and assuming minimum fill is universally one-half.

### Compact example

For order-four leaves with maximum three and minimum two entries, root leaf `(5,10,15)` overflows on 20 and becomes leaves `(5,10)` and `(15,20)` under new root separator 15. Inserting 25 and 30 splits the right leaf, producing separators `(15,25)`. Deleting 30 underflows `(25)`, so it merges left and removes separator 25. Deleting 5 underflows the left leaf, but the right sibling has three entries: borrow 15 and change the separator from 15 to 20. Deleting 10 then merges the two minimum siblings and shrinks the root to leaf `(15,20,25)`.

### Connections

This module depends on [DBE-031](031-b-tree-structure.md)'s structural conventions and [DBE-032](032-b-tree-search-and-range-scan.md)'s navigation contract. DBE-026–030 provide buffer, writeback, and integrity prerequisites. DBE-034 contrasts hash mutation; DBE-035–039 extend index design, selectivity, and write amplification.

## Governing Question

The governing question is not simply “where should the key be inserted?” A correct answer declares the logical operation, physical comparator, page layout, separator convention, occupancy unit, concurrency protocol, recovery contract, and reclamation rule. A mutation may be transactionally invisible, structurally reachable through a sibling, absent from a parent, and not yet reclaimable—all at once without being corrupt, if those are documented transient states.

The chapter therefore separates three layers. The **abstract map layer** specifies keys, values, uniqueness, and transaction visibility. The **stable structural layer** specifies the tree after repairs finish. The **operational layer** specifies latches, publication order, WAL records, crash states, cleanup, and reuse. The executable program models only the stable structural layer and deliberately says so.

## Why This Matters

B+ tree reads are cheap only because writes continuously preserve the routing facts those reads trust. A misplaced pivot can make committed rows unreachable. A missing link can truncate a range scan. Premature page reuse can turn an ordinary race into arbitrary interpretation of unrelated bytes. A recovery procedure that replays half of a split incorrectly can make a previously acknowledged transaction disappear.

Mutation policy also shapes performance. Page size and fill factor determine fan-out and height. Variable-width keys make entry-count splits misleading. Sequential identifiers concentrate contention at the rightmost leaf; random identifiers scatter writes but may reduce locality and cause more splits. Deletion can recover space eagerly, lazily, during vacuum, during compaction, or during rebuild. Each choice trades foreground latency, write amplification, fragmentation, concurrency, and background debt.

## Prerequisites and Retrieval

Retrieve from [DBE-031](031-b-tree-structure.md) the right-child-minimum separator convention: for separators `K1,...,Kr`, child zero holds keys below `K1`, and child `i>0` begins at `Ki`. Recall the complete physical key `(logical_key,tie_breaker)`, uniform leaf depth, leaf links, high keys, and the distinction between stable and transient invariants. From [DBE-032](032-b-tree-search-and-range-scan.md), retrieve upper-bound internal descent, lower-bound leaf positioning, and right-link correction.

From [DBE-026](026-buffer-pools.md), retrieve pins, latches, dirty state, and page generations. From [DBE-028](028-dirty-pages-and-writeback.md), retrieve write-ahead ordering and why dirty pages reach storage independently. From [DBE-029](029-checksums-and-page-corruption.md), retrieve page validation and quarantine. Before proceeding, be able to trace insert into a sorted array, distinguish a transaction lock from a page latch, and explain why “unlinked” does not imply “safe to reuse.”

## Learning Objectives

After completing this module, you should be able to:

1. trace leaf insertion, leaf split, separator propagation, internal split, and root creation;
2. derive correct pivots under a declared parent separator convention;
3. trace deletion through redistribution, merge, parent repair, and root shrink;
4. distinguish logical deletion, physical index cleanup, structural page deletion, and reclamation;
5. state stable and allowed transient invariants separately;
6. reason about variable-width keys, duplicates, compression, fill factor, and split selection;
7. explain latch coupling, optimistic restart, B-link publication, and incomplete-split completion;
8. design WAL/recovery for multi-page mutation without assuming atomic page persistence;
9. analyze write amplification, fragmentation, hot pages, and maintenance policy; and
10. build invariant, crash, concurrency, and differential tests with useful observability.

## Core Exposition

Begin with the logical contract. A unique index rejects a new logical key if a conflicting visible key exists under the engine's transaction rules. A non-unique index still needs a total physical order, commonly by appending a row locator or another tie-breaker. The uniqueness check, visibility wait, and physical insertion may involve multiple versions; a structural equality comparison alone does not decide transaction-level uniqueness.

For a stable insert, descend to the candidate leaf using the exact search protocol. Retain or reacquire the path information required by the implementation. After latching the leaf, revalidate its generation, high key, and search position because another writer may have split it since the earlier read. Insert the encoded entry at lower/upper-bound position determined by duplicate policy. Mark the page dirty and log the change according to recovery rules.

If the page fits, no structural repair is needed. “Fits” is a byte-layout judgment: slot, key, payload, prefix-compression restart, alignment, fence, checksum, and reserved recovery/concurrency space all matter. Maximum entry count is useful only in a fixed-width teaching model. An engine may first compact dead slots, remove safe garbage, deduplicate equal keys, or retry encoding before it splits.

If it still does not fit, choose a split point. The two output ranges must be nonempty where required, ordered, independently encodable, and compatible with minimum/free-space policy. A half-by-byte split often balances future capacity better than half-by-count. Yet workload-aware policies may leave extra room on the expected insertion side, keep duplicate runs together, or choose a short discriminating pivot. Such policies must never violate range correctness.

For the right-min convention, the parent pivot for the new right leaf is a value that separates every left entry from every right entry and routes the first right entry right. In a simple uncompressed model, copy the minimum complete key of the right leaf. Real engines may truncate a pivot suffix while retaining a separator that is strictly sufficient under the comparator. Copying the median blindly can be wrong when B-tree and B+ tree conventions differ.

The publication order is a protocol, not a cosmetic implementation detail. A B-link design initializes and logs the right page, moves entries, sets the left page's high key/right link, preserves the former sibling relationship, and only then installs the parent downlink. A search reaching the old left page can observe that the target is beyond its high key and move right even before the parent is repaired. Exact latch and WAL order is implementation-specific; the durable principle is that every observable intermediate state has a recovery/search interpretation.

Installing the new `(pivot,right_child)` in the parent may overflow it. Split an internal page into ordered child ranges, propagate a separating pivot upward, and repeat. Internal representations differ over whether one pivot is copied or moved, so derive the operation from the representation rather than memorizing “promote the median.” If the old root splits, allocate a new root that points to both halves and atomically publish the root metadata under the engine protocol. Height increases by one, and all old leaves remain at equal depth.

A root split does not require every reader to see the new root immediately if the protocol lets a reader starting from the old root move right and eventually descend correctly. PostgreSQL's B-tree implementation explicitly relies on this B-link property. Other designs publish a versioned root pointer and make readers restart. Mixing assumptions from these protocols is unsafe.

Deletion begins above the page structure. In MVCC, deleting a row usually creates transaction/version state; readers with older snapshots may still require its index entry. Later, an access method may remove a known-dead tuple, compact a posting list, or reclaim a slot. Still later, a page may become structurally empty, be unlinked, wait through a safety horizon, and enter a free-space pool. These are distinct operations with distinct evidence.

The classic stable deletion algorithm removes the target entry and tests non-root minimum occupancy. If the page remains legal, only separator repair may be needed when the page's minimum changed. If it underflows and an adjacent sibling under the same parent has spare occupancy, redistribute: move the sibling boundary entry, then replace the parent pivot with the new minimum of the right child. If no sibling can spare, merge adjacent pages, repair sibling links, remove one child/pivot from the parent, and recurse if the parent underflows.

At the root, special rules avoid meaningless unary levels. If an internal root retains one child after repair, make that child the new root and decrease height. An empty tree becomes one designated empty leaf or another documented empty representation. The root is normally exempt from non-root minimum occupancy. These exceptions belong in the invariant statement, not as silent special cases.

Eager merge is not universally desirable or safe. Insert/delete oscillation can repeatedly split and merge the same pages. Merging touches siblings and parent, increasing latching, WAL, dirty pages, and conflict. Production systems often tolerate low occupancy, remove dead tuples before splitting, mark empty pages through multi-stage deletion, or compact/rebuild later. PostgreSQL documentation describes bottom-up and simple deletion passes intended to avoid anticipated splits; its source-level design also separates half-dead/unlinked/deleted/recyclable states.

Concurrency protocols must prevent lost updates and misrouting without deadlock. Conservative latch crabbing holds parent while latching child until the child is known safe for the operation, then releases ancestors. Optimistic designs descend with versions/read latches and restart if the target is unsafe or changed. B-link designs permit rightward correction through high keys/links. Writers need a global latch acquisition order or restart rule; “lock whichever sibling is convenient” invites cycles.

Concurrent deletion is harder than removing an array element. A reader may hold a pin, be following a sibling link, or have remembered a page identifier. Page unlink must leave searches a valid route; reclamation waits until no permitted observer can treat the identifier as the old page. Buffer pins, epochs, hazard pointers, generation numbers, transaction horizons, or combinations can establish safety. A checksum alone cannot detect a valid but wrong reused page unless identity/range metadata participates.

Recovery treats a structural mutation as a series of logged atomic actions, not a magical multi-page write. WAL must reach stable storage before any corresponding data page is flushed. Records carry enough identity and before/after/redo information to make replay idempotent and reject stale page incarnations. PostgreSQL, for example, can log a split at one level separately from the later parent insertion and mark an incomplete split so recovery or a later operation can finish it. Searches remain correct through the right link.

The commit status of the logical row and completion of structural cleanup are also separate. After crash recovery, the tree may contain entries for transactions that abort or versions later found dead; visibility filters and cleanup reclaim them. Structural validation should therefore not equate every physical entry with a currently visible logical row. Conversely, every committed visible row that requires an index entry must be findable under the recovery contract.

Duplicates and variable-length keys complicate boundaries. If duplicate logical keys span pages, tie-breakers define their physical ranges. Prefix/suffix truncation must preserve strict routing even when user keys compare equal. Posting-list deduplication changes one physical tuple into several logical locators. A split policy may keep duplicates together for compression, but an oversized duplicate run must still be representable. Tests need maximum encodings, pathological prefixes, collations, NULLs, and equal user keys.

Performance has several amplifiers. A leaf-only insert normally dirties one page and emits one logical record; a split allocates/dirties siblings, parent, perhaps neighbor links, and WAL. Cascading splits multiply this across height. Eager merges do similar work for deletion. Fill factor reserves capacity at bulk build/rebuild time but costs space/read fan-out. Lower fill helps updates; higher fill improves density. Workload evidence, not a universal percentage, chooses it.

Monotone keys make the rightmost leaf and its ancestors hot. Possible responses include right-biased split policy, larger pages, key salting/partitioning, sequence allocation that spreads writers, buffering, or a different access method. Each changes range locality or semantics. Random UUID-like keys distribute contention but can increase page scattering and split frequency. Measure rather than repeat folklore.

Observability should count inserts/deletes, no-split inserts, cleanup-before-split successes, leaf/internal/root splits, bytes/fill before and after, parent propagation depth, redistributions, merges, root growth/shrink, latch wait/restarts, right-link corrections, incomplete-split completion, WAL bytes/records, dirty pages, flush latency, dead/live tuples, fragmentation, page-deletion age, reclamation backlog, and p50/p99. Bound labels and avoid exposing indexed values.

Testing starts with a reference ordered multimap and structural validator. Generate insert/delete/search/range histories including duplicates and absent deletes; compare logical results after every operation. Exercise minimum/maximum encodings and every split position. Inject crashes after each logged subaction and replay twice. Schedule readers/writers at high-key, parent-publication, unlink, and reuse boundaries. Scan all reachable pages plus allocation metadata to find cycles, multiply reachable pages, orphans, leaks, stale downlinks, bad generations, and separator drift.

The executable model below is intentionally a single-threaded, in-memory, two-level tree with fixed-width distinct integer keys. It demonstrates leaf split/root creation, another leaf split, merge, redistribution with separator repair, root shrink, and full stable-state validation. It does not model pages, internal splits beyond this bounded height, duplicates, latches, MVCC, WAL, failure, or reclamation.

<!-- bijux-verify: {"id":"bplus-stable-mutations","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"after_insert_20=(root=(15,),leaves=((5, 10), (15, 20)))\nafter_insert_30=(root=(15, 25),leaves=((5, 10), (15, 20), (25, 30)))\nafter_delete_30=(action='merge-left',root=(15,),leaves=((5, 10), (15, 20, 25)))\nafter_delete_5=(action='borrow-right',root=(20,),leaves=((10, 15), (20, 25)))\nafter_delete_10=(action='merge-right-root-shrink',root_leaf=(15, 20, 25))\nheight=1\ninvariants=True\n","stderr":""}} -->
```python
MAX_ENTRIES = 3
MIN_ENTRIES = 2
leaves = [[5, 10, 15]]


def separators() -> tuple[int, ...]:
    return tuple(leaf[0] for leaf in leaves[1:])


def snapshot() -> tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    return separators(), tuple(tuple(leaf) for leaf in leaves)


def leaf_index(key: int) -> int:
    position = 0
    pivots = separators()
    while position < len(pivots) and pivots[position] <= key:
        position += 1
    return position


def ordered_add(values: list[int], key: int) -> list[int]:
    position = 0
    while position < len(values) and values[position] < key:
        position += 1
    if position < len(values) and values[position] == key:
        raise ValueError("the bounded model uses distinct keys")
    return values[:position] + [key] + values[position:]


def insert(key: int) -> None:
    position = leaf_index(key)
    leaves[position] = ordered_add(leaves[position], key)
    if len(leaves[position]) > MAX_ENTRIES:
        middle = len(leaves[position]) // 2
        left = leaves[position][:middle]
        right = leaves[position][middle:]
        leaves[position : position + 1] = [left, right]


def delete(key: int) -> str:
    position = leaf_index(key)
    leaf = leaves[position]
    entry = 0
    while entry < len(leaf) and leaf[entry] != key:
        entry += 1
    if entry == len(leaf):
        return "absent"
    leaves[position] = leaf[:entry] + leaf[entry + 1 :]
    if len(leaves) == 1 or len(leaves[position]) >= MIN_ENTRIES:
        return "no-repair"
    if position > 0 and len(leaves[position - 1]) > MIN_ENTRIES:
        borrowed = leaves[position - 1][-1]
        leaves[position - 1] = leaves[position - 1][:-1]
        leaves[position] = [borrowed] + leaves[position]
        return "borrow-left"
    if position + 1 < len(leaves) and len(leaves[position + 1]) > MIN_ENTRIES:
        borrowed = leaves[position + 1][0]
        leaves[position + 1] = leaves[position + 1][1:]
        leaves[position] = leaves[position] + [borrowed]
        return "borrow-right"
    if position > 0:
        leaves[position - 1 : position + 1] = [leaves[position - 1] + leaves[position]]
        return "merge-left"
    leaves[0:2] = [leaves[0] + leaves[1]]
    return "merge-right-root-shrink" if len(leaves) == 1 else "merge-right"


def valid() -> bool:
    if not leaves or len(leaves) > MAX_ENTRIES + 1:
        return False
    flat = [key for leaf in leaves for key in leaf]
    if flat != sorted(flat) or len(flat) != len(set(flat)):
        return False
    if any(not leaf or len(leaf) > MAX_ENTRIES for leaf in leaves):
        return False
    if len(leaves) > 1 and any(len(leaf) < MIN_ENTRIES for leaf in leaves):
        return False
    pivots = separators()
    return len(pivots) + 1 == len(leaves) and pivots == tuple(leaf[0] for leaf in leaves[1:])


insert(20)
after_insert_20 = snapshot()
insert(25)
insert(30)
after_insert_30 = snapshot()
action_30 = delete(30)
after_delete_30 = snapshot()
action_5 = delete(5)
after_delete_5 = snapshot()
action_10 = delete(10)

print(f"after_insert_20=(root={after_insert_20[0]},leaves={after_insert_20[1]})")
print(f"after_insert_30=(root={after_insert_30[0]},leaves={after_insert_30[1]})")
print(f"after_delete_30=(action={action_30!r},root={after_delete_30[0]},leaves={after_delete_30[1]})")
print(f"after_delete_5=(action={action_5!r},root={after_delete_5[0]},leaves={after_delete_5[1]})")
print(f"after_delete_10=(action={action_10!r},root_leaf={tuple(leaves[0])})")
print("height=1")
print(f"invariants={valid()}")
```

## Definitions and Notation

Let `<I` be the complete physical key order. For a page `P`, let `range(P)=[low(P),high(P))` under a half-open convention, `used(P)` be encoded bytes including structural overhead, and `capacity(P)` be usable bytes. A policy may define minimum stable occupancy `min(P)` in bytes or entries; root exceptions are explicit.

For an internal page with right-min pivots `K1,...,Kr` and children `C0,...,Cr`, `Ki=min_key(Ci)` in the simple model and descent chooses child `upper_bound(K,target)`. A split produces `(L,R,p)` satisfying every key in `L <I p`, every key in `R >=I p`, complete coverage of the original range, and `p` sufficient to route to `R`. With truncated pivots, `p` need not equal a stored leaf key but must preserve this separation under the engine comparator.

Let `h` be height in pages, `s` the number of split levels, `m` merge levels, `W` WAL bytes, and `D` distinct pages dirtied. A simple no-split insert is `O(h)` navigation plus page modification. A cascading split remains `O(h)` structural levels, but latency and write cost depend on `s`, `W`, `D`, allocation, contention, and flush behavior.

## Mechanisms, Invariants, or Proof Structure

A defensible insertion workflow is:

1. Bind transaction/snapshot, index incarnation, comparator, uniqueness, and encoded physical key.
2. Descend and latch/version-validate the target; move right or restart if range evidence changed.
3. Resolve uniqueness/visibility according to the access-method and transaction-lock contract.
4. Compact/remove only entries proven safe; insert in total order if the page fits.
5. Otherwise allocate/initialize a right page and choose an encodable, policy-compliant split boundary.
6. Log and publish sibling/high-key state so search has a valid route through every exposed intermediate state.
7. Install the parent pivot/downlink; recursively split internal pages and create/publish a new root if needed.
8. Release latches in the protocol order, retain cleanup markers if necessary, and report evidence.

A stable deletion workflow is:

1. Establish that logical/version semantics permit physical entry removal.
2. Locate, validate, latch, and remove/compact the exact physical entry.
3. Repair a changed minimum separator even when occupancy remains legal.
4. If policy requires underflow repair, redistribute from a sibling with surplus or merge adjacent siblings.
5. Update links and remove/replace the exact parent relationship; recurse on parent underflow.
6. Shrink a unary root under the root-publication protocol.
7. Mark an unlinked page retired; reclaim only after the reader/recovery safety horizon.

Stable-state correctness follows by induction. A non-overflow insert preserves sorted membership locally. A split partitions the original ordered range without loss/duplication, adds a correct parent route, and leaves leaf depth unchanged; recursive parent splits preserve the same property, while root creation increases every leaf path equally. Deletion without underflow removes only the target. Redistribution transfers one boundary range and repairs its pivot. Merge unions adjacent ranges and removes exactly the redundant route. Recursive repair and root shrink preserve uniform depth. This is a proof sketch: a concrete engine additionally owes concurrency linearization, crash recovery, visibility, compression, and reclamation proofs.

## Alternatives and Trade-Offs

Top-down preemptive splitting avoids returning to a full parent but may split pages an operation would not ultimately need; bottom-up repair can use actual overflow but needs path recovery/latches. Byte-balanced, count-balanced, append-biased, duplicate-aware, and prefix-aware split selection optimize different workloads. Larger pages raise fan-out but increase transfer/latch/write units; smaller pages reduce amplification but increase height.

Eager redistribution/merge maintains density but amplifies writes and contention. Lazy deletion/cleanup reduces foreground work and oscillation but grows fragmentation and maintenance debt. Deduplication/posting lists delay splits for duplicates but complicate update and scan logic. Rebuild/online compaction can restore global density at substantial resource and coordination cost.

Conservative latch coupling is easier to reason about but blocks more. Optimistic version/restart designs favor read concurrency at retry cost. B-link correction tolerates delayed parent publication but adds high keys, sibling links, cleanup states, and proof obligations. Copy-on-write trees publish new immutable paths and simplify reader synchronization, but allocate/write more and require root/version garbage collection.

## Failure Modes and Misconceptions

- “Split the page in half” is incomplete: half by bytes, entries, key space, or future workload differ.
- “Promote the median” ignores whether the representation copies a right minimum or moves an internal pivot.
- “The parent changes first” can make a reader follow a downlink to an uninitialized/unreachable child.
- “All pages of a split flush together” is not a storage guarantee; WAL/recovery defines survivable order.
- “Deleting a row deletes its index tuple now” ignores snapshots, transaction state, and deferred cleanup.
- “An empty page is free” ignores sibling/parent observers, recovery, and page-identity reuse.
- “Borrowing only moves one key” forgets the parent separator repair and sometimes child downlinks.
- “Merge is always good” ignores split/merge oscillation, latch fan-out, WAL, and foreground latency.
- “Fifty-percent minimum is the definition” confuses a textbook parameter with product policy and byte layout.
- “Duplicate keys need no order” breaks deterministic boundaries, uniqueness checks, and concurrent navigation.
- “A right link fixes every race” is false without high-key validation, safe reclamation, and bounded recovery.
- “Checksums prove structure” misses validly checksummed stale pointers, orphans, cycles, and range errors.
- “One successful search validates a split” misses keys near the boundary, range links, crash states, and parent drift.
- “Sequential IDs are always optimal” ignores right-edge latch and allocation contention.

## Worked Examples

### Example 1

A fixed-width leaf holds `(5,10,15)` with maximum three entries. Insert 20 gives four ordered entries, split `(5,10)|(15,20)`, and copy 15 as the new right minimum into a new root. Search 15 routes right under the declared convention. Conclusion: the separator is derived from routing semantics, not a memorized median slogan.

### Example 2

A 4 KiB page contains eight 300-byte entries and forty 20-byte entries. Splitting 24/24 by count produces roughly 3.84 KiB versus 1.76 KiB before metadata, potentially leaving the first page overfull. A byte-aware boundary near equal encoded size is required. Conclusion: entry count is an invalid capacity proxy for variable-width records.

### Example 3

Leaf `L` splits into `L` and `R`. The protocol initializes/logs `R`, changes `L.high` and `L.right` to reach `R`, then later installs the parent downlink. A reader sent by the old parent to `L` compares its target against `L.high` and follows right. Conclusion: delayed parent repair can be safe only because publication order and search correction agree.

### Example 4

An internal page overflows after receiving a child pivot. It partitions its child ranges and propagates another pivot; the old root also overflows, so a new root points to both root halves. Every old leaf path gains exactly one common ancestor. Conclusion: cascading split increases height only at root creation and preserves uniform leaf depth.

### Example 5

After deleting 5, left leaf `(10)` underflows while right sibling `(15,20,25)` has surplus. Move 15 left, producing `(10,15)|(20,25)`, and replace parent separator 15 with 20. Leaving pivot 15 would route target 17 right even though no right key begins before 20. Conclusion: redistribution and pivot repair are one correctness operation.

### Example 6

Leaves `(5,10)` and `(15,20)` are both at minimum. Deleting 5 cannot borrow, so merge into `(10,15,20)` and remove the right child relationship. If their parent root now has one child, promote it as root. Conclusion: merge changes two structural levels and may shrink height.

### Example 7

Transaction T deletes a row while an older snapshot can still see it. Immediate physical index removal would make that reader miss a visible version. The logical delete commits first; safe cleanup later proves the entry dead to all relevant snapshots. Conclusion: transaction visibility gates physical deletion.

### Example 8

A crash occurs after a leaf split WAL record but before the parent insertion record. Recovery replays the leaf/right-link state; search remains complete through right correction, and an incomplete-split marker permits later parent completion. Conclusion: correctness comes from logged intermediate states, not simultaneous page writes.

### Example 9

An empty page is unlinked at time 100, but reader R pinned it at time 99. Reusing its page number for another index at time 101 can make R interpret valid unrelated bytes. Reclamation waits for R's protection horizon and validates generation/incarnation. Conclusion: unlinking and reuse require separate evidence.

### Example 10

Two workloads insert one million keys: monotone timestamps concentrate writers at the rightmost leaf; random keys distribute latch pressure but scatter dirty pages and range locality. Compare throughput, p99, split depth, WAL bytes, cache misses, and range cost. Conclusion: key distribution changes the bottleneck, so no universal key policy follows from asymptotic height.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies balanced-tree invariants, ordered maps, and amortized reasoning.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies inductive proofs, reference models, adversarial generation, and workload-sensitive analysis.
- [Programming Languages — Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies latch ordering, optimistic validation, linearization, epochs, and safe reclamation.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies pages, writeback, crashes, cache effects, and persistence ordering.
- [Software Engineering & Patterns](../../11-software-engineering-patterns/ROADMAP.md) supplies state-machine design, explicit contracts, and fault-injection testing.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies tail-latency, contention, telemetry, and maintenance-debt control.

## References

1. Rudolf Bayer and Edward M. McCreight, [Organization and Maintenance of Large Ordered Indices](https://link.springer.com/article/10.1007/BF00288683), *Acta Informatica* 1, 1972, original B-tree balancing foundations.
2. Philip L. Lehman and S. Bing Yao, [Efficient Locking for Concurrent Operations on B-Trees](https://web.stanford.edu/class/cs345d-01/rl/blink.pdf), *ACM Transactions on Database Systems* 6(4), 1981, high-key/right-link concurrency algorithm.
3. Goetz Graefe, [Modern B-Tree Techniques](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/p669-graefe.pdf), *Foundations and Trends in Databases* 3(4), 2011, split, prefix, concurrency, and maintenance design survey.
4. Goetz Graefe, [A Survey of B-Tree Logging and Recovery Techniques](https://doi.org/10.1145/2109196.2109197), *ACM Transactions on Database Systems* 37(1), 2012, recovery design taxonomy.
5. PostgreSQL Global Development Group, [B-Tree Index README](https://github.com/postgres/postgres/blob/master/src/backend/access/nbtree/README), current high keys, right links, root/sibling splits, incomplete splits, WAL, page deletion, and reclamation notes.
6. PostgreSQL Global Development Group, [B-Tree Insertion Source](https://github.com/postgres/postgres/blob/master/src/backend/access/nbtree/nbtinsert.c), current insertion, uniqueness, split, and parent-completion implementation.
7. PostgreSQL Global Development Group, [B-Tree Indexes](https://www.postgresql.org/docs/current/btree.html), current bottom-up deletion, simple deletion, deduplication, and operator-class behavior.
8. SQLite Project, [B-Tree Module Source](https://sqlite.org/src/file/src/btree.c), current official implementation source for page balancing and transaction integration.
9. SQLite Project, [Atomic Commit](https://www.sqlite.org/atomiccommit.html), official journal, flush-order, crash, and recovery model.
10. Ramakrishnan and Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, stable B+ tree insertion/deletion foundations.

## Exercises

### Exercise 1

Under maximum three/minimum two leaf entries and right-min separators, trace inserts `5,10,15,20,25,30`, then deletes `30,5,10`. Record every leaf, pivot, repair action, and root height.

### Exercise 2

Derive the correct parent repair for borrowing the greatest entry from a left sibling and for borrowing the smallest entry from a right sibling. State it for complete physical keys and explain how duplicate logical keys affect the answer.

### Exercise 3

Design WAL/recovery states for a leaf split whose parent update is separate. Specify record identity, page initialization, high-key/right-link publication, incomplete marker, parent insertion, idempotent replay, and behavior after a crash at each boundary.

### Exercise 4

Compare eager redistribution/merge, lazy dead-entry cleanup, posting-list deduplication, and periodic rebuild for a write-heavy MVCC secondary index. Choose a policy and give workload assumptions, correctness boundaries, metrics, and rollback triggers.

### Exercise 5

Design a concurrent/fault test campaign for page split, cascading root split, empty-page deletion, and eventual reuse. Include an oracle, scheduled race points, crash points, invariants, resource bounds, and evidence needed before claiming safety.

## Answers to the Exercises

### Answer 1

Insert 5,10,15 into root leaf `(5,10,15)`. Insert 20: split `(5,10)|(15,20)`, create root `(15)`, height 2. Insert 25 gives right `(15,20,25)`. Insert 30: split it into `(15,20)|(25,30)`, root becomes `(15,25)`. Delete 30: right `(25)` underflows; left sibling `(15,20)` cannot spare, so merge left to `(15,20,25)` and remove pivot 25, leaving root `(15)`. Delete 5: left `(10)` underflows; right has three, borrow 15 to get `(10,15)|(20,25)` and replace root pivot with 20. Delete 10: left `(15)` underflows, neither minimum sibling can spare, so merge `(15,20,25)`; the unary internal root is removed and the leaf becomes root, height 1. At each stable point keys are sorted, unique in this model, reachable once, and leaf depth is uniform.

### Answer 2

With adjacent `L|R` and right-min parent pivot `p=min(R)`: borrowing the greatest key `x` from a surplus `L` into the front of underfull `R` makes the new pivot `x`, because `x` is now `min(R)`. Borrowing the smallest key `y` from surplus `R` into the end of underfull `L` makes the new pivot the new `min(R)` after removing `y`. Moves must include payload/child relationship appropriate to leaf/internal representation. Logical duplicates require complete `(logical,tie_breaker)` keys or a proven truncated separator; using only the logical value may not strictly separate the page ranges.

### Answer 3

Identify the index/page generations and operation/record LSNs. Allocate and initialize `R`; a split record (or declared sequence) writes moved tuples, `R` range/links, the former neighbor repair where required, and `L`'s new high key/right link, while marking `L` incomplete. WAL is durable before any affected page flush. The later parent record inserts `(pivot,R)` and clears the marker atomically in its recovery meaning; root creation also publishes versioned metadata. Crash before durable split leaves the old page authoritative; after split but before parent record, redo restores right-reachable siblings and retains incomplete status; after parent record, redo installs the downlink and clears it. Page LSN/generation checks make repeated replay idempotent. Search follows high-key/right links throughout; recovery or a later writer completes missing parent publication. Exact field/latch order must follow the chosen engine, not this abstract template.

### Answer 4

For a write-heavy MVCC secondary index with frequent non-key updates, choose safe dead-entry cleanup before anticipated splits, duplicate posting lists where equality semantics permit, tolerate bounded low occupancy, and schedule online rebuild when fragmentation/debt thresholds persist. Avoid eager merge because split/merge oscillation and multi-page latching harm foreground p99. Correctness requires snapshot-safe deadness, total duplicate order, valid search routes, crash-safe cleanup, and delayed reclamation. Measure split avoidance, live/dead bytes, page density distribution, WAL/write bytes, latch waits/restarts, range read amplification, vacuum/rebuild debt, throughput, and p99. Canary the policy; roll back/disable deduplication or trigger rebuild if latency, recovery time, fragmentation, or scan cost exceeds predeclared thresholds. A read-mostly static index might rationally choose denser eager maintenance instead.

### Answer 5

Use a transaction-aware reference ordered multimap plus full structural traversal. Generate distinct/duplicate/maximum-width keys and insert/delete/search/range histories. Place barriers after right-page initialization, link/high-key publication, each parent propagation, new-root publication, logical delete, unlink, retirement, horizon passage, and reuse. Run readers at old/new roots and boundaries; crash after every durable record, recover twice, and compare visible results. Assert order, exact reachability, separator ranges, occupancy in stable states, uniform depth, valid links/generations, no cycles, no lost/duplicated committed entries, permitted stale versions only, no early reuse, bounded retries/latches/WAL, and allocation accounting without orphan/leak. Preserve seeds, schedules, toolchain/version, logs, page images, LSNs, and invariant reports. Passing sampled schedules is evidence for those executions, not a proof of all interleavings; pair it with protocol review or formal/model checking where risk requires.
