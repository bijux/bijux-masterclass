---
module_id: DBE-031
program: Database Engineering
level: 1
module_number: 31
title: B+ Tree Structure
status: complete
last_verified: 2026-08-30
---

# B+ Tree Structure

## One-Page Review

### Governing question

Which structural invariants let a page-oriented B+ tree represent a large ordered key space with bounded height, correct navigation, efficient scans, and recoverable concurrent evolution?

### Essential definitions

A **B+ tree** is a height-balanced multiway search tree whose record entries reside at the leaf level; internal nodes contain separator/pivot keys and child references. The **fanout** is the number of children of an internal node. **Occupancy** is used capacity relative to the format's maximum/minimum rule. A **separator** partitions adjacent child key ranges; its exact equality/inequality convention must be declared. The **root** has exceptional minimum occupancy. A **leaf chain** links leaves in key order for sequential access. **Height** is the number of page levels on a root-to-leaf path under this chapter's convention. A **clustered** tree stores base rows in key order; a **secondary** tree stores index keys plus a row locator/primary key according to its engine.

### Central model, mechanism, or theorem

For declared maximum fanout `m`, every internal node has at most `m` children; non-root internal nodes have at least `ceil(m/2)` children in the simple textbook model; leaves have a declared maximum and minimum entry count; keys are strictly ordered under the complete comparator; an internal node with `c` children has `c-1` separators; separators and children induce disjoint, exhaustive key intervals; all leaves have equal depth; and leaf sibling links enumerate the same ordered leaf set. These invariants yield logarithmic page height when minimum occupancy holds, but production formats modify details for variable-width keys, prefix truncation, duplicates, concurrency, and deletion states.

### Critical invariants

- The root is unique, every reachable non-root node has exactly one logical parent in the stable model, and no child cycle exists.
- Internal key count equals child count minus one; all referenced pages have the expected index/type/incarnation.
- Keys within every node are ordered under one total comparison including NULL/collation/direction and a tie-breaker where needed.
- Each child subtree lies within the separator interval assigned by its parent.
- All record-bearing leaves occur at one depth and every represented record is reachable exactly as the format permits.
- Non-root nodes satisfy declared byte/count occupancy; the root follows explicit empty/single-level exceptions.
- Leaf links are ordered, bounded, acyclic, mutually consistent where bidirectional, and cover the live leaf frontier.
- Page headers, checksums, LSNs, sibling/high-key metadata, and buffer identities agree with structural interpretation.

### Common failures

Failures include leaving “order” undefined; mixing B-tree and B+ tree record placement; assuming separator equality convention; omitting the rightmost child; ordering text with a different collation after build; treating logical duplicates as identical physical keys; checking entry count instead of byte occupancy; overlooking prefix-compressed/truncated separators; accepting leaves at different depths; losing/looping a leaf sibling link; following a stale/reused page identifier; interpreting a concurrent split as corruption; trusting a root/catalog pointer without incarnation; and equating locally valid pages with a globally valid tree.

### Compact example

Under the chapter's order-4 convention, root separators `(15,30)` and children `L0,L1,L2` represent leaf keys `(5,10)`, `(15,20,25)`, `(30,40)`. Separators equal the minimum key of their right child, so intervals are `<15`, `>=15 and <30`, and `>=30`. Each leaf has 2–3 entries, the root has three children, all records occur at depth two, and links `L0→L1→L2` enumerate the sorted keys. Changing separator 15 to 16 or skipping L1 in the leaf chain violates different invariants even though every leaf remains locally sorted.

### Connections

This module uses [DBE-021](021-pages-blocks-and-database-files.md) through [DBE-030](030-tracing-a-record-from-logical-row-to-persistent-bytes.md) for page, buffer, persistence, integrity, and record-locator context. DBE-032 covers search/range scans and DBE-033 covers mutations. Data Structures Engineering supplies multiway trees and invariant checking; concurrency supplies latch/right-link protocols; query engineering supplies ordering and access-path semantics.

## Governing Question

The governing question is structural rather than procedural. Before proving search, split, or delete algorithms, specify the tree language: page/node types, maximum/minimum capacity in bytes or entries, root exceptions, separator convention, complete key comparator, duplicate representation, payload/locator placement, sibling/high-key metadata, and transitional states permitted by concurrency/recovery.

“B+ tree of order 100” is insufficient because sources use order for maximum children, maximum keys, or minimum degree. Variable-width database keys make count-only capacity approximate. This chapter always states `m` as maximum internal children and separately states leaf entry bounds; real page fit remains byte-based.

## Why This Matters

Database indexes must keep billions of ordered entries reachable with few page reads. High fanout makes height small because one internal page partitions many subtrees. Leaves concentrate record entries and link them for scans. The structure supports equality, range, prefix, ordering, uniqueness, and index-only/clustered access, but only under its comparator and representation.

Structural corruption can return wrong answers rather than merely slow queries. A missing downlink makes a key range unreachable; a wrong separator routes searches away; an inconsistent leaf link skips ranges; a collation change invalidates stored order; a stale page link reads another object incarnation. Page checksums may all pass because these are relational invariants.

Production concurrency complicates snapshots of structure. A split can publish a right sibling/high key before the parent downlink is installed. Lehman–Yao-style designs use right links and high keys so searches move right when parent information is stale. Verifiers must distinguish documented transient states, recovery remnants, and true corruption under the correct locking/snapshot protocol.

## Prerequisites and Retrieval

Retrieve page/slot/record layout, buffer tags, latches, WAL-ordered writeback, checksums, and safe inspection from DBE-021–030. Retrieve multiway trees, total ordering, logarithms, invariants, recursion/induction, and graphs from [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md).

Before continuing, prove that an internal node with `c` children needs `c-1` separators under an alternating interval representation; explain why all leaves at one depth differs from all pages being equally full; and define a total composite-key order including directions, NULL placement, collation, and unique physical tie-breaker.

This chapter uses unique integers and an equality-to-right-minimum separator convention. It does not model a particular PostgreSQL, InnoDB, or SQLite page. Search mechanics, split/merge algorithms, and concurrent correctness proofs are scoped to later modules.

## Learning Objectives

After completing this module, you should be able to:

1. define B-tree versus B+ tree, node types, fanout, height, occupancy, separators, and leaf links precisely;
2. state key, child, interval, balance, reachability, occupancy, and sibling invariants under a declared convention;
3. derive height/capacity bounds from fanout and minimum occupancy;
4. explain root exceptions, one-page trees, duplicates, composite keys, and variable-width capacity;
5. map logical nodes to slotted/checksummed/WAL-managed database pages;
6. distinguish clustered, secondary, heap-locator, and index-only payload arrangements;
7. account for prefix compression, truncated pivots, high keys, right links, and concurrent transitional states;
8. design structural validation and corruption containment; and
9. avoid transferring constants or binary layouts across engines.

## Core Exposition

A B-tree stores keys and possibly records in internal and leaf nodes; a B+ tree keeps navigational separators in internal nodes and record entries at leaves. Database products often call their variants “B-tree” even when leaf-oriented data and sibling links resemble B+ trees. Use the engine's terminology while describing actual invariants.

Let maximum internal fanout be `m`. An internal node with children `C_0...C_{c-1}` has separators `K_1...K_{c-1}`. In this chapter, `K_i=min(C_i subtree)` for `i>=1`; `C_0` contains keys `<K_1`, middle `C_i` contains `K_i<=key<K_{i+1}`, and final contains `>=K_{c-1}`. Other designs store upper bounds, fence keys, or truncated pivots, changing equalities but not the requirement for exhaustive nonoverlapping routing.

Every node's entries are sorted by the index comparator, not raw byte lexicographic order unless the format says so. A composite comparator processes key columns in order with per-column ascending/descending, NULL policy, collation/operator class, and type semantics. Non-unique logical keys need a physical tie-breaker such as record/primary-key identifier so page order and separator intervals are unambiguous. Included payload columns do not affect ordering.

Leaves store `(key,payload-or-locator)` entries. A heap secondary index typically carries a tuple locator; a clustered index leaf carries the base row; an InnoDB secondary record contains primary-key columns used to reach the clustered record. Covering/include columns can let queries avoid base-row fetches but enlarge leaves. Payload organization changes fanout and cache/write cost.

Balanced means all reachable live leaves have the same depth, not that sibling counts match. If each non-root internal node has at least `a=ceil(m/2)` children and the root (when nonleaf) has at least two, a height-`h` tree has at least `2*a^(h-2)` leaves for `h>=2`. Conversely with at most `m` children, it has at most `m^(h-1)` leaves. Leaf entry bounds translate leaf count to record capacity. Root-as-leaf handles empty/small trees separately.

For example with `m=128` and height 4, maximum leaves are `128^3=2,097,152`; at 100 entries/leaf this is about 209.7 million entries under ideal count assumptions. Actual fanout varies with headers, page size, variable keys, prefix compression, locators, MVCC/dead entries, fragmentation, fill policy, and concurrency metadata.

Occupancy prevents tall sparse trees, but databases often define it in usable bytes rather than key counts. Variable key sizes mean two nodes with equal counts can differ radically in fullness. Fill factor/reserved headroom is a construction/tuning policy, not necessarily the minimum structural validity threshold. Root and nodes involved in deletion/concurrency may have explicit exceptions.

Prefix compression can omit repeated leading bytes from leaf entries; separator truncation stores the shortest pivot sufficient to distinguish adjacent child ranges. A pivot therefore need not equal a complete user key. Validation must reconstruct/compare according to the format rather than demand literal equality from a textbook diagram.

Nodes are pages with headers/type/level/flags, item directories/cells, keys, downlinks or payload, high/fence keys, siblings, free space, LSN/checksum, and special metadata. Logical order can differ from physical cell offset order because a directory provides indirection. Every pointer is a page identity within an index incarnation, not just an integer suitable for arbitrary reuse.

The root identity is stored in index metadata/catalog and may change during root growth/shrink. Root correctness includes reachability and incarnation. A one-page tree is both root and leaf. Empty trees may use an empty root leaf or another documented representation. Verifiers cannot impose non-root occupancy on the root.

Leaf sibling links enable scans without returning to parents. A singly linked right chain must be acyclic, ordered, terminate, and cover the leaf frontier. Bidirectional links also require reciprocal consistency. High/fence keys define page ranges. Links are performance and concurrent-navigation structure, but missing links can affect correctness for scan implementations that rely on them.

In a stable classical tree, every non-root node has exactly one parent and every node is reachable once. Concurrent B-link variants temporarily allow a new sibling reachable via right link before a parent downlink exists. PostgreSQL's nbtree source notes document high keys and right links used to recover from concurrent splits. Structural checks must run with an engine-defined locking/snapshot protocol and permit only recognized bounded states.

Physical consistency begins bottom-up: validate I/O/checksum, page/index identity, format/type/level, item bounds/nonoverlap, local key order, link/downlink validity, then global intervals, parent coverage, equal leaf depth, sibling frontier, and heap/index relationships. Never follow an unvalidated corrupt offset/pointer. Verification code is itself a parser over hostile state.

Logical consistency adds collation/operator semantics, duplicate uniqueness/tie-breakers, payload/locator reachability, visibility, included columns, and correspondence to base records. PostgreSQL's `amcheck`, for example, documents B-tree invariants and optional heap/index coverage checks with distinct cost and detection limits. A clean structural scan cannot prove absence of corruption.

Operational diagnostics record index/schema/incarnation, root, page level/type, key range/high key, siblings, parent/downlinks, occupancy bytes, dead entries, LSN/checksum, and exact engine/build/collation. On violation, quarantine the access path if safe, preserve evidence, prevent propagation, compare trusted recovery sources, and prefer supported rebuild/recovery only after the base data and comparator are trusted.

The executable model declares order 4: internal nodes have at most four children; non-root internals would require at least two; leaves have two to three entries except a root leaf; separators equal right-child minima. It validates one root/three leaves plus intentionally bad separator/link variants. It omits pages, payload, duplicates, mutations, concurrency, recovery, and vendor behavior.

<!-- bijux-verify: {"id":"bplus-structure-invariants","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"root_keys=(15, 30)\nroot_children=('L0', 'L1', 'L2')\nleaf_chain=('L0', 'L1', 'L2')\nleaf_keys=(5, 10, 15, 20, 25, 30, 40)\nheight=2\nbalanced=True\nseparators_valid=True\noccupancy_valid=True\nall_records_in_leaves=True\nbad_separator_detected=True\nbad_leaf_link_detected=True\n","stderr":""}} -->
```python
nodes = {
    "L0": {"leaf": True, "keys": (5, 10), "next": "L1"},
    "L1": {"leaf": True, "keys": (15, 20, 25), "next": "L2"},
    "L2": {"leaf": True, "keys": (30, 40), "next": None},
    "R": {"leaf": False, "keys": (15, 30), "children": ("L0", "L1", "L2")},
}


def sorted_unique(values: tuple[int, ...]) -> bool:
    return all(values[index] < values[index + 1] for index in range(len(values) - 1))


def depth(name: str) -> int:
    node = nodes[name]
    if node["leaf"]:
        return 1
    child_depths = tuple(depth(child) for child in node["children"])
    if len(set(child_depths)) != 1:
        return -1
    return 1 + child_depths[0]


def separator_check(separator_keys: tuple[int, ...]) -> bool:
    children = nodes["R"]["children"]
    expected = tuple(nodes[child]["keys"][0] for child in children[1:])
    return separator_keys == expected


def leaf_chain(first: str, override: dict[str, str | None] | None = None) -> tuple[str, ...]:
    chain = []
    seen = set()
    current = first
    while current is not None and current not in seen:
        seen.add(current)
        chain.append(current)
        if override is not None and current in override:
            current = override[current]
        else:
            current = nodes[current]["next"]
    return tuple(chain)


root = nodes["R"]
leaves = root["children"]
chain = leaf_chain("L0")
leaf_keys = tuple(key for leaf in chain for key in nodes[leaf]["keys"])
balanced = depth("R") == 2
separators_valid = separator_check(root["keys"])
occupancy_valid = (
    2 <= len(root["children"]) <= 4
    and len(root["keys"]) == len(root["children"]) - 1
    and all(2 <= len(nodes[leaf]["keys"]) <= 3 for leaf in leaves)
    and all(sorted_unique(nodes[leaf]["keys"]) for leaf in leaves)
)
all_records_in_leaves = not any("records" in nodes[name] for name in ("R",))
bad_separator_detected = not separator_check((16, 30))
bad_leaf_link_detected = leaf_chain("L0", {"L0": "L2"}) != leaves

print(f"root_keys={root['keys']}")
print(f"root_children={root['children']}")
print(f"leaf_chain={chain}")
print(f"leaf_keys={leaf_keys}")
print(f"height={depth('R')}")
print(f"balanced={balanced}")
print(f"separators_valid={separators_valid}")
print(f"occupancy_valid={occupancy_valid}")
print(f"all_records_in_leaves={all_records_in_leaves}")
print(f"bad_separator_detected={bad_separator_detected}")
print(f"bad_leaf_link_detected={bad_leaf_link_detected}")
```

The model's absence of a `records` field in the root represents its leaf-only record convention; real internal pivot tuples still contain navigation data. The validator assumes stable state and unique integer keys, so it cannot justify concurrent or duplicate-key implementations.

## Definitions and Notation

Let maximum internal children be `m>=3`, minimum non-root internal children `a=ceil(m/2)`, maximum leaf entries `l_max`, and declared minimum non-root leaf entries `l_min`. Height `h=1` means a root leaf. For `h>=2`, root has 2..m children and non-root internal nodes have `a..m`.

For child ranges under this chapter's convention, parent separators satisfy `K_i=min(C_i)` for right child `i`, and intervals are `C_0:(-infinity,K_1)`, `C_i:[K_i,K_{i+1})`, `C_last:[K_last,+infinity)`. The comparator includes the full physical key. `N` counts record entries, `L` leaves, and `F` usable byte fill; count bounds are models unless key/entry width is bounded.

Minimum leaves at height `h>=2` are `2*a^(h-2)` and maximum `m^(h-1)`. Thus capacity lies between those leaf counts times applicable leaf occupancy, subject to root/small-tree exceptions. Variable-size pages/entries require byte-based refinements.

## Mechanisms, Invariants, or Proof Structure

A structural validation proceeds as follows:

1. Bind exact index incarnation, root metadata, format/version, comparator/collation, page size, and stable/concurrent-state protocol.
2. Validate root page physically before following references.
3. For every node, validate checksum/header/index identity, level/type, slots/cells, local order, and byte occupancy.
4. For internal nodes, validate `children=keys+1`, unique/bounded downlinks, and separator-induced child intervals.
5. Carry lower/upper key bounds recursively and prove every child entry/subtree respects them.
6. Prove all live record leaves share depth and every expected reachable page is accounted for under the state model.
7. Walk leaf links independently; prove order, no cycles, termination, reciprocity if applicable, and frontier equivalence.
8. Validate high/fence/right-link states and allowed incomplete parent propagation under concurrency protocol.
9. Validate payload/locator/base-table relationships separately from tree shape.
10. Report the first unsafe parse boundary and preserve evidence; never “repair” by guessing a separator or link.

The height bound follows by induction. The root supplies at least two children at level 2. Each additional internal level multiplies the minimum subtree count by at least `a`, yielding at least `2*a^(h-2)` leaves. Maximum fanout similarly yields at most `m^(h-1)`. The argument assumes every non-root internal node satisfies the declared occupancy and every leaf is at one depth.

## Alternatives and Trade-Offs

B-trees can store records internally; B+ trees centralize records in leaves and favor scans/high internal fanout. Clustered leaves avoid a heap lookup but make primary-key size/order and page movement central. Secondary leaves with compact locators increase fanout but require base lookup. Included payload trades fewer lookups for larger leaves.

Prefix compression and separator truncation raise fanout but complicate comparison/reconstruction. Fixed fill targets make bulk build predictable; reserved headroom reduces immediate splits but increases height/storage. Sibling/high-key metadata supports concurrency/scans but adds invariant surface. Copy-on-write trees simplify reader snapshots/recovery in some designs but increase path copying and reclamation complexity.

## Failure Modes and Misconceptions

- “Order has a standard meaning.” Define maximum children/keys/minimum degree explicitly.
- “B-tree and B+ tree are synonyms.” Product names vary; record placement and leaf links must be stated.
- “Every node is half full.” Root/exceptions, byte occupancy, build fill, deletion states, and variable keys complicate this.
- “Separator is a data row.” It may be a truncated navigation pivot without leaf payload.
- “Equal user keys break ordering.” A complete physical tie-breaker can total-order duplicates.
- “Sorted pages imply a valid tree.” Cross-page ranges, reachability, depth, links, and base correspondence remain.
- “All leaves at one depth means equal performance.” Cache state, compression, payload, contention, and overflow differ.
- “A pointer integer is enough identity.” Index incarnation/page generation/type must agree.
- “A missing parent link is always corruption.” Some concurrent split protocols temporarily rely on right links/high keys.
- “Right links are optional optimization.” If scans/search recovery rely on them, they are correctness structure.
- “Checksum validates separators.” It validates covered bytes, not global interval meaning.
- “Rebuild from the index.” Rebuild normally trusts base data and comparator; a corrupt source cannot be assumed.
- “Height predicts latency exactly.” Buffer/cache/device/prefetch/concurrency and per-page CPU dominate actual tails.
- “One vendor page diagram is portable.” Formats, pivots, payloads, MVCC, links, and recovery differ.

## Worked Examples

### Example 1

Root keys `(15,30)` with three children are valid only under a declared convention. Here 15 belongs to the middle/right child. Under an upper-bound-left convention, equality routes differently. Code and proof must match.

### Example 2

An internal node has four separators but four children. It needs five child intervals, so one range is unreachable or ambiguous. The local invariant is `child_count=separator_count+1`.

### Example 3

Leaves at depths 3 and 4 are each sorted and half full, but the tree is not height balanced. A search cost/correctness proof assuming one leaf level no longer applies.

### Example 4

Two leaf entries share email key `a@example.org`. Adding primary key/heap locator to the physical comparison distinguishes them; uniqueness enforcement remains a separate logical constraint.

### Example 5

Ten 200-byte keys and ten 20-byte keys have equal entry count but radically different page occupancy. Count-based order is an analytical simplification; real splits use usable bytes and format rules.

### Example 6

Leaf L0's next pointer skips L1 to L2. Root descent can still find L1, while a range scan beginning in L0 misses its keys. Independent frontier/link validation detects the discrepancy.

### Example 7

A pivot stores `Sm` rather than full boundary `Smith, Ada, id=42` because the truncated prefix suffices between adjacent ranges. Literal right-minimum equality is invalid for this format; comparison sufficiency is the invariant.

### Example 8

During a concurrent split, old page high key becomes 50 and right link points to the new page covering `>=50`; parent still points only to old. A search for 70 descends stale, observes high key, moves right. Verification needs the protocol's allowed transition.

### Example 9

An index page checksum passes but its downlink names a freed page reused by another index. Complete index incarnation/page type/generation checks reject it before interpreting foreign entries.

### Example 10

With `m=128`, height four, and 100 leaf entries, ideal maximum is `128^3*100=209,715,200`. This capacity model is not a memory/I/O promise and ignores byte variability, fill, metadata, dead entries, compression, and root/internal payload.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies multiway trees, graphs, invariants, and amortized structure.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies logarithmic bounds, induction, I/O models, and adversarial cases.
- [Programming Languages — Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies latches, atomic publication, optimistic validation, and reclamation.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies paging, cache/I/O locality, and persistent-memory boundaries.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies observability, corruption response, fault injection, and capacity evidence.

## References

1. Rudolf Bayer and Edward M. McCreight, [Organization and Maintenance of Large Ordered Indices](https://rtheunissen.github.io/bst/docs/references/1972_bayer_mccreight.pdf), *Acta Informatica* 1, 1972.
2. Douglas Comer, [The Ubiquitous B-Tree](https://dl.acm.org/doi/10.1145/356770.356776), *ACM Computing Surveys* 11(2), 1979.
3. Philip L. Lehman and S. Bing Yao, [Efficient Locking for Concurrent Operations on B-Trees](https://www.csd.uoc.gr/~hy460/pdf/p650-lehman.pdf), *ACM TODS* 6(4), 1981.
4. PostgreSQL Global Development Group, [B-Tree Index README](https://github.com/postgres/postgres/blob/master/src/backend/access/nbtree/README), current high-key, right-link, pivot, duplicate, split, deletion, and concurrency design notes.
5. PostgreSQL Global Development Group, [B-Tree Index Header](https://github.com/postgres/postgres/blob/master/src/include/access/nbtree.h), current pivot/non-pivot and included-column format notes.
6. PostgreSQL Global Development Group, [amcheck](https://www.postgresql.org/docs/current/amcheck.html), current B-tree structural verification and limitations.
7. Oracle, [Clustered and Secondary Indexes](https://dev.mysql.com/doc/refman/8.4/en/innodb-index-types.html), current MySQL 8.4 clustered-row and secondary-primary-key organization.
8. SQLite Project, [Database File Format: B-tree Pages](https://www.sqlite.org/fileformat.html#b_tree_pages), official interior/leaf, child/key, depth, cell, and overflow invariants.
9. Goetz Graefe, [Modern B-Tree Techniques](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/p669-graefe.pdf), *Foundations and Trends in Databases* 3(4), 2011.
10. Ramakrishnan and Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, tree-index foundations.

## Exercises

### Exercise 1

Under `m=6`, non-root minimum children 3, leaf capacity 5 with minimum 3, and height 4, derive minimum/maximum leaves and record entries, including root exceptions.

### Exercise 2

Validate root separators `(20,50)` for leaves `(1,10,19)`, `(20,30,49)`, `(50,60)` under right-minimum and upper-bound-left conventions. State intervals and equality routing.

### Exercise 3

Design a byte-oriented page/node validator for variable composite keys, prefix compression, included payload, high key, siblings, downlinks, checksums, LSNs, and page identity. Separate safe local parsing from global traversal.

### Exercise 4

Explain how logical duplicates, NULLs, descending fields, and locale collation form a complete physical ordering. Analyze what happens after an incompatible collation change.

### Exercise 5

Design a production tree-integrity audit that distinguishes stable corruption from allowed concurrent split/deletion states and connects findings to base-table, replica, backup, containment, and repair evidence.

## Answers to the Exercises

### Answer 1

For height 4, minimum leaves are `2*3^(4-2)=18`; with at least 3 entries each, minimum records are 54, assuming a nonempty tree of this height and no special underfull states. Maximum leaves are `6^(4-1)=216`; at 5 entries each, maximum records are 1,080. Height 1 is a root leaf with its own empty/small rule; at height at least 2 the root minimum is two children rather than three. Byte-variable entries make these count results an idealized declared-format bound.

### Answer 2

Under right-minimum equality, separators are exactly minima of the second and third leaves: 20 and 50; intervals are `<20`, `[20,50)`, `>=50`, so equality goes right. Under an upper-bound-left convention, separator 20 would normally bound/include the left range, but left maximum is 19; literal `(20,50)` as inclusive maxima is not canonical and equality routing differs. The same bytes cannot be validated without declaring whether pivots are lower bounds of right children, upper bounds of left children, or fence/truncated separators.

### Answer 3

First bind index incarnation, format, comparator/collation, page size, compression rules, and stable-state protocol. Validate I/O/checksum before parsing; then header identity/type/level/count/free bounds, slot/cell offsets/nonoverlap, prefix reconstruction bounds, key datum formats, included payload separation, high-key and sibling/downlink page identities, and LSN/state flags. Never follow a pointer until locally validated. Global traversal carries lower/upper bounds, detects cycles/multiple parents, checks child count/separators, equal leaf depth, occupancy bytes, right-link/high-key ranges, and leaf-frontier equivalence. Resource-bound recursion, keys, page visits, and diagnostics.

### Answer 4

Define a lexicographic comparator over each key column's type/operator class, ASC/DESC direction, explicit NULL placement, and exact collation version; append a stable physical tie-breaker such as primary key/TID for equal logical keys. Included columns do not order. An incompatible collation change can make stored text order and separator ranges disagree with new comparisons while checksums remain valid, causing wrong navigation/results. Detect version drift, prevent unsafe use, and rebuild with documented engine procedures after validating base data and uniqueness semantics.

### Answer 5

Run against an engine-defined consistent/locked snapshot or use its official verifier, recording engine/build, index incarnation/root, comparator/collation, recovery point, and allowed transitional flags. Verify physical pages, local ordering, intervals/downlinks, levels, occupancy, links/high keys, and base-table coverage as separate layers. Recheck suspicious transient states under the documented protocol rather than guessing. Preserve raw evidence securely, quarantine the index/access path where safe, prevent suspect replication/backup expiry, and compare independently verified sources. Rebuild only after base data and comparator are trusted; then verify queries, structure, replicas, restart/restore, and root cause. A clean audit proves neither future nor uncovered correctness.
