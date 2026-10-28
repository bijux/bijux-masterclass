---
module_id: DSE-073
program: Data Structures Engineering
level: 2
module_number: 73
title: B+ Trees
status: complete
last_verified: 2026-08-30
---

# B+ Trees

## One-Page Review

### Governing question

How should an engineer design a page-resident B+ tree so exact lookup, ordered range scan, split publication, concurrency, and crash recovery all preserve one explicit routing and leaf-chain contract?

### Essential definitions

- A **B+ tree** is a balanced multiway search tree whose logical data entries reside at leaves; internal pages contain routing separators and child references.
- A **separator** directs search between children. Its value may be copied from a leaf and may be truncated, but its exact lower-bound, upper-bound, or fence-key semantics must be specified.
- A **leaf chain** links leaves in key order so a range scan descends once and then advances leaf to leaf.
- **Fan-out** is the number of children represented by an internal page; leaf capacity and internal fan-out usually differ.
- A **fence/high key** bounds a page's key range. A **right link** permits movement to the next page when a concurrent split makes the current page too far left.
- A **posting list** or composite `(user_key,record_id)` order represents duplicates without making separator or cursor behavior ambiguous.
- **Clustered/primary** and **secondary** leaf entries carry different payloads: full records or stable row locators/version identities.
- A **structural modification operation** changes routing, links, root, or allocation rather than only one leaf's logical contents.

### Central model, mechanism, or theorem

For internal fan-out at least f and L leaf pages, a balanced B+ tree has height `O(log_f L)`. Exact lookup visits one root-to-leaf path; a range returning z leaf entries visits that path plus the leaf pages covering the result, conventionally `O(log_f L + z/b_leaf)` page visits under capacity/occupancy assumptions.

Insertion finds the target leaf, inserts by total order, and splits an overflowing leaf. The right leaf's first key (or a valid distinguishing prefix) is copied into the parent; unlike classic B-tree promotion, the data entry remains at a leaf. Leaf links and fences must become search-safe with parent routing. Internal overflow recursively splits, and a new root grows height uniformly.

Correctness has three coupled views: the routing tree sends a key to a leaf whose interval can contain it; the leaf chain covers the same leaves exactly once in global order; and durable allocation/publication recovers a root, routing graph, and chain that agree. A proof of one view does not imply the others.

### Critical invariants

1. Internal separators are ordered and each child obeys the declared half-open/closed range convention.
2. All logical data entries occur in leaves; copied internal separators are not duplicate records.
3. Every leaf is at the same tree depth.
4. Leaf entries are globally ordered under one duplicate/tie-break policy.
5. Following next links from the leftmost leaf visits every live leaf once, in routing order, without cycles.
6. Split/merge/redistribution conserves logical entries and maintains parent separators, fences, and links.
7. Root identity, page generations, latches/versions, WAL, and allocation ownership survive concurrent and crash boundaries.

### Common failures

- Using classic B-tree median-removal rules for a B+ leaf split and losing the copied boundary entry.
- Leaving parent separators stale after a leaf's first key changes under redistribution or deletion.
- Treating duplicate user keys as a total order or assuming a cursor can resume from key alone.
- Publishing a right leaf link without a safe fence protocol, or parent routing without reachable leaf state.
- Scanning sibling pointers without pins, versions, snapshot rules, or safe page reclamation.
- Computing fan-out from average compressed sizes and violating worst-case split feasibility.
- Equating leaf linkage with transaction isolation, or checksum success with tree/chain correctness.
- Reporting logarithmic lookup while ignoring output pages, heap fetches, buffer state, latches, and tail latency.

### Compact example

With leaf capacity three, inserting `10,20,5,6,12,30,7,17` splits sorted four-entry leaves at two entries. The root separators become `[10,20]`; leaves are `[5,6,7] -> [10,12,17] -> [20,30]`. Separators 10 and 20 remain as leaf data entries. An inclusive scan `[6,20]` returns `6,7,10,12,17,20` by one descent and linked-leaf traversal.

### Connections

DSE-071 supplies pages and I/O evidence; DSE-072 supplies multiway height and structural transformations while its record-placement rule differs. DSE-074 uses sorted input and fill policy for bulk loading. Database Engineering adds collations, uniqueness, MVCC, predicate/range locking, optimizer statistics, WAL, vacuum, and online index lifecycle.

## Governing Question

How can leaf-only record placement and ordered leaf linkage improve fan-out and range access without weakening routing, concurrency, durability, or evidence standards?

## Why This Matters

Ordered storage workloads rarely ask only whether one key exists. They ask for prefixes, time intervals, pagination, minimum/maximum, ordered joins, and the next hundred entries. A classic B-tree may encounter data at internal levels, complicating dense sequential traversal. A B+ tree uses internal pages purely for routing and keeps the logical ordered sequence at one level. Internal entries can be compact; a range scan descends once, then walks leaves.

This organization underlies many database and filesystem indexes, but “B+ tree” is not a complete specification. Separators can mean the least key in the right child, a greatest key in the left, or a shortened distinguishing fence. Leaves can store full rows, row IDs, version references, or posting lists. Links may be forward-only, doubly linked, or augmented at every level. Deletion may merge eagerly, defer cleanup, or retain half-dead pages. Concurrency and recovery protocols depend on these choices.

The engineering goal is to make those decisions observable and testable. The abstract map/range semantics need proof. Encoded pages need hostile-input validation. Concurrent split and scan protocols need schedule arguments and tests. Recovery needs crash-point evidence. Performance needs cold/warm, point/range, read/write, amplification, and tail measurements. None can substitute for another.

## Prerequisites and Retrieval

Retrieve:

- lower/upper bound, lexicographic composite ordering, iterators, and half-open ranges;
- B-tree height, occupancy, preemptive split, rotation, merge, and root change;
- page IDs/generations, slotted pages, overflow, pin/latch/dirty, WAL, and allocation recovery;
- snapshots, MVCC, predicate protection, linearizability, latch coupling, optimistic validation, and reclamation;
- checksums, checked decoding, property/fuzz testing, crash injection, and benchmark methodology.

Diagnostic retrieval: explain why an internal separator copied from the first entry of a right leaf is not a second logical record. It is routing metadata; the authoritative data entry remains in the leaf. A traversal or verifier that counts both has confused physical representation with logical contents.

## Learning Objectives

After this module, you can:

1. distinguish classic B-tree and B+ record/separator semantics;
2. define child intervals, duplicate ordering, leaf-chain, occupancy, and root invariants;
3. derive point and output-sensitive range page costs;
4. trace leaf/internal splits, separator copying, redistribution, merge, and root changes;
5. design exact lookup, lower-bound seek, forward range scan, and resumable cursor contracts;
6. map variable entries to validated pages and recoverable allocation/publication;
7. reason about latch coupling, optimistic validation, right links/high keys, snapshots, and reclamation;
8. construct layered proof, model, fuzz, schedule, crash, and performance evidence.

## Core Exposition

**Define the logical index.** Let each leaf entry have total-order identity `(key,tie)`, where tie may be row ID, primary key, or version-stable locator. For a unique index, validation rejects two live entries with equal user key. For nonunique indexes, a search for key k seeks lower bound `(k,-infinity)` and scans until user key changes. Posting lists compress duplicates but add ordering, update, overflow, and MVCC rules.

**Define separator intervals.** A common convention stores separator `s_i` as a lower bound for child `i+1`: child 0 covers keys below `s_0`; middle child i covers `[s_(i-1),s_i)`; final child covers `[s_last,+infinity)`. Equality descends right. Other conventions work, but search, split, deletion, validation, and recovery must use the same one. If separators are truncated, prove they still distinguish adjacent child maxima/minima under the collation.

**Separate leaf and internal capacity.** Leaves contain keys plus payload/locator, visibility metadata, slots, links, and perhaps overflow references. Internal pages contain separators, child IDs, fences, and structural metadata, often yielding greater fan-out. Variable compression means capacity is measured in encoded bytes. Bound maximum entry sizes or overflow them so every required split can produce legal pages.

**Point lookup descends by gaps.** At each internal page, lower/upper bound selects a child according to separator convention. Validate page range/fence and version, pin/latch as required, then descend. At the leaf, lower-bound the composite entry and apply visibility/uniqueness rules. A secondary-index hit may require a heap/primary lookup; include that in cost evidence.

**Range scan is seek plus stream.** Seek the lower endpoint through the routing tree. Within the leaf, start at lower bound; emit visible entries while within upper bound; then pin/validate the next leaf before releasing current state under the chosen protocol. Stop at the bound, limit, cancellation, or error. Define inclusive/exclusive endpoints, reverse scans, duplicate continuation, snapshot, retry, and resume tokens. A key-only token can skip/repeat duplicates; use the total entry identity plus snapshot/generation policy.

**Leaf split copies a boundary.** Insert into a logical sorted candidate, choose a feasible byte/count split, allocate right leaf, distribute every entry once, and set right's first entry as the parent lower-bound separator (or derive a safe distinguishing prefix). That entry stays in right. Update fences and sibling links. Parent insertion can split internal pages, where routing separators are redistributed/promoted according to internal convention. Root overflow creates a new root.

**Ordering of concurrent publication matters.** A basic latch-coupled tree may hold enough ancestors to install the parent before exposing changes. A B-link protocol permits a split to expose right link and high key so a search arriving through stale parent routing detects it is beyond the high key and moves right. The proof depends on link direction, fence monotonicity, latch order, memory visibility, page lifetime, and later parent insertion. Merely adding `next` is not the algorithm.

**Deletion is policy-rich.** Removing an entry may change the leaf's first key, requiring parent separator maintenance. Underflow can borrow entries from a sibling and update the intervening separator, or merge leaves, repair links, delete one parent entry, and propagate. Some systems avoid eager merges to reduce write contention, reclaim empty pages under restrictions, or mark pages half-dead before unlink. State the resulting occupancy/height/space guarantees rather than quoting textbook bounds.

**Leaf links are a second topology.** Tree descent and leaf chain must identify the same live leaf set and order. A verifier starts at root to collect leaves/ranges, then follows the leftmost chain and compares identities, generations, order, fences, backlink symmetry if present, and cycles. Concurrent verification needs a stable snapshot or versioned restart; independent live reads may mix structural states.

**The bounded model makes copy semantics visible.** This exclusive in-memory model has a single internal root and leaves of capacity three. It splits overflowing leaves, rebuilds lower-bound separators, maintains forward links, validates routing and chain equivalence, and performs an inclusive range scan.

<!-- bijux-verify: {"id":"bounded-b-plus-leaf-chain-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"leaf_capacity=3\ninserted=10,20,5,6,12,30,7,17\nroot_separators=10,20\nleaves=5,6,7|10,12,17|20,30\nseparator_copies_in_leaves=True\nheight_edges=1\nlookup_17=True\nlookup_15=False\nrange_6_20=6,7,10,12,17,20\nchain_order=5,6,7,10,12,17,20,30\nvalid=True\nevidence=bounded_b_plus_leaf_chain_model\n","stderr":""}} -->
```python
class Leaf:
    def __init__(self, entries=None):
        self.entries = [] if entries is None else entries
        self.next = None


class BPlusTree:
    def __init__(self, capacity):
        self.capacity = capacity
        self.leaves = [Leaf()]
        self.separators = []

    def rebuild(self):
        self.separators = [leaf.entries[0] for leaf in self.leaves[1:]]
        for index, leaf in enumerate(self.leaves):
            leaf.next = self.leaves[index + 1] if index + 1 < len(self.leaves) else None

    def leaf_index(self, key):
        index = 0
        while index < len(self.separators) and key >= self.separators[index]:
            index += 1
        return index

    def insert(self, key):
        leaf = self.leaves[self.leaf_index(key)]
        position = 0
        while position < len(leaf.entries) and leaf.entries[position] < key:
            position += 1
        leaf.entries.insert(position, key)
        if len(leaf.entries) > self.capacity:
            cut = (len(leaf.entries) + 1) // 2
            right = Leaf(leaf.entries[cut:])
            leaf.entries = leaf.entries[:cut]
            index = self.leaves.index(leaf)
            self.leaves.insert(index + 1, right)
        self.rebuild()

    def lookup(self, key):
        return key in self.leaves[self.leaf_index(key)].entries

    def range_scan(self, low, high):
        result = []
        leaf = self.leaves[self.leaf_index(low)]
        while leaf is not None:
            for key in leaf.entries:
                if low <= key <= high:
                    result.append(key)
                if key > high:
                    return result
            leaf = leaf.next
        return result

    def chain(self):
        result = []
        leaf = self.leaves[0]
        while leaf is not None:
            result.extend(leaf.entries)
            leaf = leaf.next
        return result

    def valid(self):
        nonempty = all(0 < len(leaf.entries) <= self.capacity for leaf in self.leaves)
        local = all(all(leaf.entries[i] < leaf.entries[i + 1] for i in range(len(leaf.entries) - 1)) for leaf in self.leaves)
        separators = self.separators == [leaf.entries[0] for leaf in self.leaves[1:]]
        links = all(self.leaves[i].next is self.leaves[i + 1] for i in range(len(self.leaves) - 1)) and self.leaves[-1].next is None
        ordered = self.chain() == sorted(self.chain())
        return nonempty and local and separators and links and ordered


values = [10, 20, 5, 6, 12, 30, 7, 17]
tree = BPlusTree(3)
for value in values:
    tree.insert(value)

leaves = "|".join(",".join(str(value) for value in leaf.entries) for leaf in tree.leaves)
copies = all(separator in tree.chain() for separator in tree.separators)
print(f"leaf_capacity={tree.capacity}")
print("inserted=" + ",".join(str(value) for value in values))
print("root_separators=" + ",".join(str(value) for value in tree.separators))
print(f"leaves={leaves}")
print(f"separator_copies_in_leaves={copies}")
print("height_edges=1")
print(f"lookup_17={tree.lookup(17)}")
print(f"lookup_15={tree.lookup(15)}")
print("range_6_20=" + ",".join(str(value) for value in tree.range_scan(6, 20)))
print("chain_order=" + ",".join(str(value) for value in tree.chain()))
print(f"valid={tree.valid()}")
print("evidence=bounded_b_plus_leaf_chain_model")
```

The model assumes unique integers, a single root level, count capacity, exclusive atomic operations, forward-only links, and separator rebuilding from all leaves. It has no internal split, deletion, bytes, pages, files, buffer pool, concurrency, snapshot, WAL, crash, or performance behavior. It proves no production B+ implementation.

**Persistence treats split as recoverable structure.** A leaf split may update left and right pages, their links/fences, parent, allocator, root, and free/retired state. Specify structural log records or page-oriented redo/undo, page LSNs, allocation intent, WAL-before-data, idempotence, torn-page repair, and root selection. Recovery must tolerate any prefix of physical writes and produce one logical routing/chain state, not merely checksum-valid pages.

**Payload semantics matter.** A clustered leaf may store the full record, making scans sequential but splits expensive. A secondary leaf stores a locator, increasing fan-out but causing heap/primary probes and stale-version handling. Covering columns trade reads for space/write amplification. Prefix compression and separator truncation improve density but require collation-stable decoding and restart points. Overflow bounds must prevent one entry from making a legal split impossible.

**Isolation is above latching.** Page latches keep structures memory-safe; they do not prevent phantoms in a transaction's key range. MVCC visibility filters leaf versions, while predicate/key-range locks, serializable validation, or another documented mechanism protects logical range semantics. A scan crossing leaves must retain its transaction snapshot and handle concurrent deletes, splits, page retirement, cancellation, and errors without silent gaps or duplicates.

**Test each evidence layer.** Exhaust small tree/chain states. Compare randomized insert/delete/lookup/range sequences with a sorted multimap oracle. Mutate encoded bytes and fuzz parsers. Model split/merge/scan schedules, version wrap, and reclamation. Crash at every log, allocation, page, link, parent, root, checkpoint, and free boundary, then reopen and independently audit. Benchmark distributions, duplicates, point/range mix, result widths, cold/warm cache, write bursts, and recovery only after correctness passes.

**Operate the index.** Version formats and collations; retain golden fixtures; supply dump, verify, rebuild, migration, rollback, and salvage tools. Observe height, internal/leaf occupancy, chain length, split/redistribution/merge, root changes, posting/overflow, point and range pages, returned/filtered entries, heap probes, cache hits, latch waits/restarts, scan retries, WAL/write amplification, retired pages, corruption, recovery time, and p50–p999 latency.

## Definitions and Notation

Let an entry identity be `e=(key,tie,payload_or_locator)`. `Leaf(e)` is its authoritative physical leaf. Internal page u has separators `S(u)` and children `C(u)` with `|C|=|S|+1`. Under right-lower-bound semantics, separator `S[i]` bounds `C[i+1]`; equality descends right. `Next(l)` is l's forward leaf link. `FenceLow/FenceHigh` are page bounds when present.

Let f be effective minimum/average internal fan-out as explicitly qualified, b_leaf effective leaf entries, L leaf pages, h height, and z returned entries. `O(log_f L + z/b_leaf)` is an idealized page-visit shape, not a latency or physical-read guarantee. `PageId:generation` protects logical identity reuse. LSN, latch/version, pin, snapshot, and transaction range protection belong to distinct layers.

## Mechanisms, Invariants, or Proof Structure

### Routing proof

1. Define total entry order and separator interval convention.
2. Validate internal sorted separators and exact child count.
3. Prove every child's entries lie in its ancestor-composed interval.
4. For leaf split, partition all entries once and copy a valid right lower bound upward.
5. For internal split, preserve all child intervals and recursively repair parent/root.
6. Induct on height to prove lookup reaches the only leaf interval that can contain the entry.

### Range proof

1. Lower-bound seek reaches the first possible leaf/entry.
2. Each leaf is internally sorted by total identity.
3. Next links enumerate exactly the routing leaves once and in order.
4. Endpoint and visibility rules emit exactly desired logical entries.
5. Resume/retry carries enough identity and snapshot state to prevent accidental skip/duplicate.
6. Concurrent use additionally proves fence/version/reclamation behavior.

### Durability proof

1. Validate page bytes, IDs/generations, fences, links, separators, and allocation ownership.
2. Define safe publication order or atomic recovery intent for new pages, links, parent, and root.
3. Make redo idempotent and undo/compensation, page LSN, flush, and torn-write behavior explicit.
4. Delay reuse until readers, I/O, logs, and replicas cannot reference the retired generation.
5. Recover from each crash prefix, then compare routing leaves, chain leaves, logical oracle, and allocator.
6. Scope fault-test results to exercised code, environments, and histories.

## Alternatives and Trade-Offs

| Choice | Benefit | Cost/proof burden |
|---|---|---|
| Full rows in leaves | clustered range locality | lower fan-out, costly splits |
| Stable row locators | compact secondary index | extra lookup and version lifecycle |
| Composite duplicate entries | simple total order | repeated keys and space |
| Posting lists | duplicate compression | overflow/update/MVCC complexity |
| Full separators | simple comparison | lower internal fan-out |
| Truncated separators | greater fan-out | collation/routing proof |
| Forward links | simple range scan | reverse scan needs alternatives |
| Doubly linked leaves | efficient reverse movement | extra atomic repair surface |
| Latch coupling | direct structural safety | contention/ancestor retention |
| B-link high keys | concurrent stale-parent recovery | stronger fence/link/reclaim proof |
| Eager merge | occupancy and space | write/latch churn |
| Lazy deletion | low foreground cost | bloat and weaker bounds |
| WAL in-place | localized writes | multi-page recovery protocol |
| Copy-on-write | root publication/snapshots | amplification and garbage collection |

## Failure Modes and Misconceptions

- **“B+ is just another spelling of B-tree.”** Leaf-only records change split, search, and scan semantics.
- **“Promote the median out of a leaf.”** Copy a valid boundary; do not delete the authoritative leaf entry.
- **“Separator equals child minimum forever.”** Redistribution/deletion may require repair; truncated fences may use another rule.
- **“Equal keys can go anywhere.”** Define total tie order and cursor bounds.
- **“Linked leaves prove valid ranges.”** Links may omit, duplicate, cycle, or disagree with routing.
- **“Next pointer makes concurrent scans safe.”** Require fences, validation, snapshots, and safe lifetime.
- **“Pin equals latch equals transaction lock.”** Residency, structural exclusion, and logical isolation differ.
- **“Average compression defines capacity.”** Worst cases and overflow determine guaranteed split feasibility.
- **“Checksum-valid recovery is correct.”** Reachability, links, separators, root, and allocator must agree.
- **“Range cost is O(log n).”** Include output leaves, filtering, heap probes, and retries.
- **“Benchmarks prove no missing records.”** Use logical oracle, schedules, crashes, and independent audits first.

## Worked Examples

### Example 1

**Problem.** Split leaf `[5,10,12,20]` at capacity three.

**Derivation.** Produce `[5,10]` and `[12,20]`; copy 12 into parent under right-lower-bound semantics. Twelve remains a leaf record.

**Conclusion.** Separator copy differs from classic B-tree promotion.

### Example 2

**Problem.** Route equality at separators `[10,20]`.

**Derivation.** With right-lower-bound intervals `<10`, `[10,20)`, and `>=20`, key 10 selects child one and 20 child two.

**Conclusion.** Equality direction is part of the format/algorithm contract.

### Example 3

**Problem.** Scan `[6,20]` in the model.

**Derivation.** Seek 6 in first leaf, emit 6,7, follow links, emit 10,12,17, then 20 and stop after the inclusive bound.

**Conclusion.** Range access is one descent plus ordered leaf traversal.

### Example 4

**Problem.** Resume a nonunique scan after `(key=7,row=42)`.

**Derivation.** Resume strictly after composite `(7,42)` under the same snapshot/collation. Resuming after user key 7 alone may skip other sevens; at 7 may repeat entries.

**Conclusion.** Cursor identity must match total leaf order.

### Example 5

**Problem.** Deleting the first entry of a right child changes 20 to 23.

**Derivation.** If parent separator is exact right minimum, update it to 23 atomically/recoverably with leaf change, or use a fence convention where retained 20 remains a valid lower bound and prove routing.

**Conclusion.** Separator maintenance follows declared semantics.

### Example 6

**Problem.** A split is visible through right link before parent update.

**Derivation.** Under a proven B-link protocol, stale descent lands left, compares target with high key, and moves right. Without reliable high key/link and page lifetime, it can miss or dereference reuse.

**Conclusion.** Safe incomplete parent propagation requires the full protocol.

### Example 7

**Problem.** A leaf chain contains A→C while routing contains A,B,C.

**Derivation.** Point lookup through routing may find B, but range scanning skips it. Audit must compare routing-derived leaf sequence with linked sequence.

**Conclusion.** Both topologies are correctness-critical.

### Example 8

**Problem.** A secondary range returns 1,000 locators across 8 leaves.

**Derivation.** Index cost includes root path plus 8 leaves, but fetching 1,000 scattered rows can dominate. Covering/clustered layouts alter payload and write trade-offs.

**Conclusion.** Index page complexity is not end-to-end query cost.

### Example 9

**Problem.** Crash leaves a checksum-valid right leaf allocated but unreachable.

**Derivation.** Recovery uses logged split/allocation intent to install routing/link or reclaim. A checksum says bytes are intact, not which logical outcome owns the page.

**Conclusion.** Allocation and reachability are part of atomicity.

### Example 10

**Problem.** A benchmark reports p50 point lookup only.

**Derivation.** Add cold/warm point and range widths, duplicates, heap probes, concurrency, p99/p999, split bursts, WAL/bytes, cache/latch/restarts, faults, and recovery objectives.

**Conclusion.** Workload and failure evidence must match intended service.

## Cross-Program Connections

- **Database Engineering:** composite indexes, collations, clustering, covering, uniqueness, MVCC, phantoms, query plans, vacuum, and online rebuild refine leaf semantics.
- **Concurrent and Parallel Programming:** B-link algorithms, latch coupling, optimistic versions, safe reclamation, linearization, and progress shape structural publication.
- **Operating Systems:** page cache/direct I/O, async completion, durability barriers, and device errors affect observed requests and recovery.
- **Security Engineering:** hostile encodings, overflow chains, corrupted links, stale generations, resume-token integrity, and resource limits are trust boundaries.
- **Data Engineering:** partition-local indexes, sorted bulk load, range extraction, and remote scans depend on leaf layout and chain locality.
- **Formal Methods:** refinement connects abstract ordered multimaps, routing intervals, leaf topology, concurrent histories, and crash states.

## References

1. Philip L. Lehman and S. Bing Yao, [“Efficient Locking for Concurrent Operations on B-Trees”](https://www.cs.cmu.edu/afs/cs/academic/class/15712-f08/www/readings/Lehman81.pdf), *ACM TODS* 6(4), 1981. Primary high-key/right-link concurrency algorithm and proof argument.
2. Rudolf Bayer and Edward M. McCreight, [“Organization and Maintenance of Large Ordered Indexes”](https://link.springer.com/article/10.1007/BF00288683), *Acta Informatica* 1, 1972. Original page-oriented multiway tree organization, occupancy, update, and height analysis from which B+ variants refine record placement.
3. Carnegie Mellon Database Group, [“Tree Indexes”](https://15445.courses.cs.cmu.edu/fall2024/notes/08-indexes1.pdf), 15-445/645 notes, 2024. Authoritative educational B+ tree operations and engineering choices.
4. PostgreSQL Global Development Group, [“B-Tree Indexes”](https://www.postgresql.org/docs/current/btree.html), current documentation accessed 2026-08-30. Official operator, implementation, deletion, and deduplication behavior.
5. PostgreSQL Global Development Group, [`nbtree` README](https://github.com/postgres/postgres/blob/master/src/backend/access/nbtree/README), current source documentation accessed 2026-08-30. Maintainer invariants for high keys, sibling links, splits, scans, and deletion.
6. SQLite Project, [“Database File Format: B-tree Pages”](https://sqlite.org/fileformat.html#b_tree_pages), current documentation accessed 2026-08-30. Official leaf/interior formats, payload, overflow, and page layout.
7. SQLite Project, [“B-Tree Module”](https://sqlite.org/btreemodule.html), official module specification accessed 2026-08-30. Cursor, transaction, balancing, allocation, and savepoint contracts.
8. SQLite Project, [“Architecture of SQLite”](https://sqlite.org/arch.html), current documentation accessed 2026-08-30. Official B-tree, page-cache, transaction, and virtual-machine boundaries.

## Exercises

### Exercise 1

Define B+ tree, data entry, separator/fence, fan-out, leaf chain, composite duplicate order, and structural modification. State routing, balance, leaf, chain, and durability invariants plus point/range page-cost shapes.

### Exercise 2

With leaf capacity three and right-lower-bound separators, insert `8,9,10,11,15,20,17`; draw leaves, root separators, links, exact lookups 17/12, and inclusive range `[9,17]`. Explain copied boundaries.

### Exercise 3

Design correct forward range and resumable cursor APIs for duplicates and MVCC. Cover endpoint semantics, seek, link traversal, visibility, split/delete races, cancellation/errors, retry, token identity, and snapshot expiry.

### Exercise 4

Design a durable variable-length B+ implementation with separator truncation, overflow/posting lists, links/fences, concurrency, WAL/recovery/allocation, verification, migration, and observability. State what must be proven versus tested.

### Exercise 5

Audit a system that removes the boundary entry on leaf split, routes equality left despite right-lower-bound docs, resumes duplicates by user key, follows unpinned next pages, immediately reuses merges, writes split pages without structural WAL, and claims correctness from p50 point benchmarks.

## Answers to the Exercises

### Answer 1

A B+ tree stores authoritative data entries in equal-depth leaves and routing separators/children internally. A separator/fence bounds child/page ranges; fan-out counts internal children; the leaf chain orders leaves for scans; composite `(key,tie)` handles duplicates; structural modifications change routing/link/root/allocation.

Internal separators and child ranges obey one endpoint convention; internal m keys have m+1 children; leaves hold all records in total order at equal depth; the next chain visits the same live leaves once in routing order; split/merge conserve entries and update separators/fences/links; identity/generation, latches, WAL, root, and allocator remain recoverable. Point visits O(log_f L) pages and ideal range O(log_f L + z/b_leaf), with buffers, filtering, heap probes, retries, and device costs separate.

### Answer 2

Insert 8,9,10 gives `[8,9,10]`. Inserting 11 splits `[8,9] | [10,11]`, copying 10 to root. Insert 15 right gives `[10,11,15]`. Insert 20 splits it into `[10,11] | [15,20]`, producing root `[10,15]`. Insert 17 gives leaves `[8,9] -> [10,11] -> [15,17,20]` and unchanged separators `[10,15]`.

Lookup 17 routes after 15 and succeeds; 12 routes between 10 and 15 and fails in `[10,11]`. Inclusive `[9,17]` emits `9,10,11,15,17`. Ten and fifteen exist both as routing copies and authoritative leaf entries; logical traversal counts only leaves.

### Answer 3

API declares inclusive/exclusive bounds over total composite order, snapshot/isolation, direction, limit, cancellation, and error/partial-result behavior. Seek lower bound through validated routing, pin/validate leaf, filter MVCC-visible entries, acquire/validate next before releasing required state, and stop exactly at upper bound. A proven high-key/right-link or latch/version restart protocol handles splits; deletion and reclamation retain page generation until scans/I/O are safe.

Resume token contains last emitted composite identity, collation/index/version identity, direction/bounds, and snapshot or explicit weak-consistency contract; resume strictly after it. Authenticate opaque tokens where clients are untrusted, bound lifetime/size, and return explicit snapshot-expired/index-rebuilt errors. Test duplicates, empty leaves, boundary changes, split/merge, retry, cancel, and faults for gaps/duplicates.

### Answer 4

Specify version/endian, page ID/generation/type/LSN/checksum, slots, leaf/internal cells, child IDs, links/fences, collation, total duplicate order, maximum items, overflow/posting ownership, and root metadata. Prove truncated separators distinguish adjacent ranges and every allowed byte distribution can split/redistribute/merge under declared occupancy. Parser validates checked offsets/counts/order/ranges/types/chains/resource bounds before typed access.

Use latch coupling or proven high-key/right-link/version restart with ordered latches and delayed reclamation; separately implement MVCC/predicate semantics. WAL or copy-on-write covers allocation, left/right/link/fence, parent/root, retirement, page LSN, flush/torn behavior, idempotent recovery, and allocator reconciliation. Snapshot/offline auditor compares routing and chain topology, logical oracle, page bytes, and ownership.

Prove abstract routing/range transformations and concurrency/crash protocol assumptions; test serialized bytes, randomized map/ranges, bounded schedules, fuzz, and every crash point; measure cold/warm point/range, heap probes, tails, contention, amplification, and recovery. Version formats/collations with fixtures, migration/rollback, dump/verify/rebuild, and complete telemetry.

### Answer 5

Removing the copied leaf boundary loses a logical record; retain it and insert routing metadata. Right-lower-bound equality must route right everywhere or the convention/docs must change atomically with format and tests. Key-only resume cannot identify a position among duplicates; use total entry identity and snapshot. Unpinned/unvalidated next pages can be evicted, changed, or recycled; use pin plus latch/version/fence protocol.

Immediate reuse creates ABA for readers, I/O, WAL, replicas, and cursors; delay by generation and reclamation proof. Independent split writes can recover contradictory leaf, link, parent, root, and allocation states; add recoverable structural intent and crash tests. P50 point speed proves none of logical range correctness, concurrency, durability, corruption behavior, or tail performance. Require proof/oracle/schedule/fuzz/crash/audit gates, then representative range and recovery benchmarks.
