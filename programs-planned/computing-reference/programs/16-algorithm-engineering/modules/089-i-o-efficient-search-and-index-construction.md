---
module_id: ALGE-089
program: Algorithm Engineering
level: 2
module_number: 89
title: I/O-Efficient Search and Index Construction
status: complete
last_verified: 2026-09-05
---

# I/O-Efficient Search and Index Construction

## One-Page Review

### Governing question

How do we build and query an ordered index when transferring pages dominates comparisons, while preserving ordering, occupancy, snapshot, duplicate-key, durability, and recovery contracts?

### Essential definitions

- An **index entry** maps a search key to a record, record identifier, child page, or posting list under a declared duplicate policy.
- A **page** is the allocation, transfer, checksum, and often recovery unit; its usable payload is smaller than its physical size.
- **Fanout** is the number of children addressable from an internal page after headers, keys, prefixes, and pointers are included.
- A **separator** partitions child key ranges; its exact convention—first key of right child, upper bound of left child, or fence key—must be fixed.
- **Bulk loading** constructs an index from a snapshot, commonly by sorting entries and building leaves then upper levels sequentially.
- A **point lookup** seeks one key; a **range query** locates a boundary then scans consecutive qualifying entries.
- **Write amplification** is physical bytes written per logical byte accepted at a named boundary; **read amplification** counts distinct structures/pages consulted per query.

### Central model, mechanism, or theorem

If leaf capacity is $\ell$ entries and internal fanout is $f\ge2$, a bottom-up tree over $N$ sorted entries has $L=\lceil N/\ell\rceil$ leaves and about

$$
h=1+\lceil\log_f L\rceil
$$

page levels when $L>1$ and the construction groups children as evenly as required. A cold point search follows one page per level, or $O(\!\log_f(N/\ell)+1)$ transfers. A range returning $K$ consecutive fixed-size entries adds $O(K/B+1)$ transfers when leaves are physically or logically scannable. Sorting unsorted input costs $\operatorname{Sort}_{M,B}(N)$ before an $O(N/B)$ bottom-up build; presorted trusted input can avoid that sort.

### Critical invariants

- Leaf entries are ordered by the complete comparator, including duplicate tie policy.
- Every snapshot entry appears exactly once unless the index is intentionally partial or multi-versioned.
- Each separator routes every legal key to a child that may contain it; fence ranges cover without gaps.
- Non-root occupancy stays within declared lower and upper bounds after construction or update.
- Sibling or extent links agree with logical leaf order when range scans rely on them.
- Checksums, page generations, root identity, and publication metadata bind one coherent index snapshot.
- Recovery never exposes a root that reaches incomplete, mismatched, or reclaimed pages.

### Common failures

Using binary search comparison count as an I/O estimate; computing fanout from physical page size; mixing separator conventions; splitting duplicate runs inconsistently; bulk-loading maximally full leaves without update reserve; repeatedly inserting already-known bulk data; accepting unsorted input without detection; publishing the root before pages are durable; reusing page IDs without generation protection; checking lookup samples but not coverage; overlooking variable keys, prefix truncation, overflow values, caching, concurrency, compaction, and device write granularity.

### Compact example

Twenty sorted entries with leaf capacity four create five leaves. Fanout three groups them into two parent pages and one root, so a cold search visits three abstract pages. Bottom-up construction writes each completed level sequentially. Repeated insertion would instead revisit root-to-leaf paths and trigger splits; which wins depends on whether the snapshot and sorting preconditions hold.

### Connections

[ALGE-011](./011-linear-and-binary-search.md) supplies comparison search, [ALGE-085](./085-external-memory-cost-models.md) supplies transfer accounting, [ALGE-086](./086-external-sorting.md) supplies sorted runs, and [ALGE-088](./088-cache-oblivious-design.md) supplies parameter-free search layouts. ALGE-090 next maps one design across memory, threads, and storage.

## Governing Question

Given a record snapshot, key and duplicate semantics, point/range/update workload, usable page geometry, memory budget, storage behavior, concurrency model, and durability target, which search structure and construction protocol minimize relevant movement while producing a verifiably coherent index?

## Why This Matters

Search over resident arrays is governed by comparisons and cache behavior. Search over persistent or remote data is governed by how many transfer units must be fetched, whether requests are sequential, and how much useful work each request supplies. A binary search makes only $O(\log N)$ comparisons but may touch one distant page per comparison. A page-oriented tree reduces height by placing many separators in one page.

Construction matters as much as lookup. Building a large index by individual inserts repeats root-to-leaf traversal, dirties pages in scattered order, and triggers splits. If a stable snapshot is available, external sorting followed by bottom-up page construction converts much of the work into sequential passes. The improvement depends on sorting cost, record sizes, fill policy, and publication constraints.

No universal index dominates. B-trees support predictable point and range operations. Buffered trees and log-structured merge designs batch writes but add deferred work and read paths. Hash indexes support exact lookup but not ordered ranges. Learned models can predict positions but need bounded correction and update handling. The engineering objective is not “fewest I/Os” in isolation; it is a verified trade among reads, writes, space, latency, throughput, recovery, and maintenance for a defined workload.

## Prerequisites and Retrieval

Retrieve pre/postconditions from [ALGE-002](./002-preconditions-postconditions-and-correctness.md), binary search from [ALGE-011](./011-linear-and-binary-search.md), stable sorting from [ALGE-018](./018-stable-sorting-and-indirect-sorting.md), external-memory notation from [ALGE-085](./085-external-memory-cost-models.md), external sorting and recovery from [ALGE-086](./086-external-sorting.md), and cache-oblivious layouts from [ALGE-088](./088-cache-oblivious-design.md). You should be able to prove interval narrowing and calculate ceilings and logarithms.

## Learning Objectives

After this module, you should be able to:

1. define key, comparator, duplicate, snapshot, visibility, and durability contracts for an index;
2. derive fanout, leaf count, height, point-search, range-scan, and build-transfer estimates;
3. implement and verify a small bottom-up static page index and its routing rule;
4. compare binary search, B-trees, buffered trees, LSM trees, hashes, and cache-oblivious layouts;
5. design bulk loading for sorted and unsorted inputs with fill and duplicate policies;
6. reason about variable keys, separators, prefix compression, overflow values, and range links;
7. design crash-safe page creation and atomic root publication; and
8. audit coverage, routing, occupancy, ordering, links, checksums, lineage, and query evidence.

## Core Exposition

### Freeze search semantics

Define the indexed snapshot, key extraction, total comparison order, null/NaN/collation rules, duplicate policy, and value reference. A non-unique index may store one entry per record, one key plus a posting list, or `(key,record_id)` as a unique composite key. These representations have different page occupancy and update behavior.

Define query semantics too. Equality may return any matching record, the first in stable order, or all matches. A range must specify inclusive/exclusive endpoints and snapshot visibility. Prefix truncation in internal separators is legal only if routing remains correct for every key under the comparator.

Comparator version belongs in index metadata. A locale, normalization rule, schema, or encoding change can invalidate order without corrupting bytes. Either rebuild under a new identity or prove compatibility; do not silently reuse pages.

### Convert page geometry into fanout

Let physical page size be $P$, fixed header/checksum/slot overhead be $H$, average encoded separator bytes be $k$, and child reference bytes be $r$. A first estimate is

$$
f\le\left\lfloor\frac{P-H+r}{k+r}\right\rfloor,
$$

because $f$ children need roughly $f-1$ separators. Real pages may use slot arrays, prefix compression, restart points, generation fields, alignment, and variable-length cells. Therefore fanout is a distribution, not always one constant.

Use a conservative minimum fanout for worst-case height and measured occupancy for typical behavior. An eight-byte average key is not a bound when adversarial keys can be kilobytes. Large values usually live out of line so leaf pages retain useful fanout; this adds another lookup and recovery relationship.

### Derive tree height and search cost

Suppose $N$ entries fill leaves up to $\ell$ entries, giving $L=\lceil N/\ell\rceil$. With fanout at most $f$, a dense bottom-up build uses $\lceil L/f\rceil$ parents, then repeats until one root remains. For $L>1$, levels are $1+\lceil\log_f L\rceil$ in the idealized balanced case. A point query reads one page at each level when none are cached.

Root and upper pages often remain cached, making observed reads smaller. That is a workload/system fact, not a different tree height. Report cold logical page path, cache hit distribution, and physical requests separately. Read-ahead may combine leaf scans; storage may split one logical page into several physical transfers.

### Specify separators precisely

Consider internal children $C_0,\ldots,C_q$ and separators $s_1,\ldots,s_q$ defined as the minimum key of the right child. Route key $x$ to child zero if $x<s_1$, child $i$ when $s_i\le x<s_{i+1}$, and the last child when $x\ge s_q$. Equality therefore goes right.

Another implementation may store maximum-left separators and route equality left. Both can be correct. Mixing construction and lookup conventions produces false negatives at boundaries. Duplicate keys complicate minima: if duplicates span leaves, equality search may need to move left to find the first occurrence or use composite keys/fence metadata.

### Execute a bottom-up static reference

The following reference bulk-loads unique sorted integer keys into immutable leaves, groups up to three children per internal node, and stores each right child’s minimum as a separator. It is an abstract page model: tuple objects are not disk pages and there is no durability.

<!-- bijux-verify: {"id":"static-page-index-reference","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"leaves: 5\nlevels: 3\nsearch 17: ('v17', 3)\nsearch 18: (None, 3)\nordered entries: 20\n","stderr":""}} -->
```python
def minimum_key(node):
    if node[0] == "leaf":
        return node[1][0][0]
    return minimum_key(node[2][0])


def build_static_index(entries, leaf_capacity, fanout):
    leaves = []
    for start in range(0, len(entries), leaf_capacity):
        leaves.append(("leaf", entries[start:start + leaf_capacity]))
    level = leaves
    levels = 1
    while len(level) > 1:
        parent_level = []
        for start in range(0, len(level), fanout):
            children = level[start:start + fanout]
            separators = [minimum_key(child) for child in children[1:]]
            parent_level.append(("internal", separators, children))
        level = parent_level
        levels += 1
    return level[0], len(leaves), levels


def search(root, key):
    node = root
    pages = 1
    while node[0] == "internal":
        child_number = 0
        while child_number < len(node[1]) and key >= node[1][child_number]:
            child_number += 1
        node = node[2][child_number]
        pages += 1
    for entry_key, value in node[1]:
        if entry_key == key:
            return value, pages
    return None, pages


entries = [(key, "v" + str(key)) for key in range(1, 40, 2)]
root, leaves, levels = build_static_index(entries, 4, 3)
print("leaves:", leaves)
print("levels:", levels)
print("search 17:", search(root, 17))
print("search 18:", search(root, 18))
print("ordered entries:", len(entries))
```

The run checks one routing convention and shape on the recorded interpreter. It does not establish byte fanout, balanced minimum occupancy, logarithmic performance, concurrency, page encoding, checksums, or crash safety.

### Bulk-load leaves

If input is not already sorted under the exact index comparator, sort it externally. Preserve record identity and duplicate policy through every run and merge. Verify sortedness rather than trusting a producer flag. If input is already certified sorted and snapshot-bound, leaf construction is a sequential pass.

Choose target fill below maximum when near-future random inserts are expected. Maximally full leaves minimize initial space and scan pages but split immediately under inserts. A read-only index can pack tightly. Avoid a tiny final leaf by redistributing the final two or more pages while respecting minimum and maximum occupancy.

Keep duplicate runs together when feasible if equality lookup returns all values, but a run larger than a page must span pages. Store continuation/fence metadata or composite keys so lookup can find the first page and range across the rest. A single unbounded posting list may require overflow pages and its own update protocol.

### Build internal levels

After leaves are finalized, emit their fence summaries in leaf order. Group child references into parent pages, choose separators under the declared convention, then repeat. Each level can be written sequentially. Construction memory needs only enough child summaries and output buffering unless the format requires global optimization.

Every page should record format/schema version, page kind, entry count, byte length, key bounds, child generations, checksum, and construction identity as applicable. Verify a child page before allowing a parent to reference it. The root is published last.

For fixed-size records, the post-sort build is $O(N/B)$ transfers because total entries and level metadata form a decreasing geometric series under fanout greater than one. Variable keys and overflow values require byte-based accounting; a page count alone can hide large payload movement.

### Support range queries

A point lookup finds the leaf containing the lower boundary. Consecutive leaves then supply range output. Leaf sibling links make this direct, but links must be version-consistent. Alternatively, a traversal stack can find successors through parents. Physical contiguity permits read-ahead; logical links alone may issue random requests.

For $K$ fixed-size consecutive results in a cold model, the transfer form is $O(\log_B N+K/B)$ under standard page-capacity assumptions. Projection, visibility filtering, overflow values, and non-covering record fetches add I/O. “Returned 1,000 rows” does not imply only their leaf pages were read.

### Buffer updates

A B-tree applies an update along a search path and sometimes splits or merges pages. Buffered trees attach batches of pending operations to internal nodes. When a buffer fills, many operations are flushed to children together, amortizing transfers [3]. Searches must consult relevant buffers as well as leaves, and durability must cover pending operations.

The LSM-tree similarly accumulates updates in a memory-resident component and merges them into larger sorted components [4]. Sequential batching reduces immediate random writes, while point reads may consult multiple components and background compaction rewrites data. Bloom filters, fences, and caches can reduce reads but introduce memory and false-positive behavior. Tiering versus leveling, size ratio, tombstones, and compaction scheduling change amplification; “LSM” alone does not determine a bound.

### Compare alternative search organizations

A sorted flat array is compact and supports binary search but has expensive middle insertion; it is strong for immutable snapshots. A B-tree supports dynamic ordered operations with bounded height. A hash index can approach constant expected probes for exact lookup but does not naturally answer ordered ranges. String indexes must account for comparison bytes, not just key count; the String B-tree combines external search-tree and string structures to support stronger string operations [5].

Cache-oblivious B-trees arrange data so searches achieve transfer-efficient bounds across unknown block sizes, but dynamic maintenance and layout complexity matter [6]. Learned indexes predict a position or child, then use a correctness-preserving local search; prediction error, model space, skew, updates, and adversarial distributions must be bounded or measured. A model is an accelerator, not the source of truth.

### Publish crash-safely

Build new pages under an immutable construction ID. Write child pages, validate counts/bounds/checksums, and make them durable to the promised boundary before writing parents that reference them. After the root and its metadata are durable, atomically publish a root pointer or catalog entry using the storage system’s documented primitive.

A process crash before publication leaves an orphan construction that can be garbage-collected after proving no committed root references it. A crash after publication must find every reachable page. In-place update instead needs write-ahead logging, shadow paging, copy-on-write, or another proven recovery protocol. An atomic rename on one filesystem does not imply atomic object-store or cross-device publication.

Page IDs should include generations or immutable content identities when reuse could create an ABA-like stale reference. Checksums detect selected corruptions but do not prove correct ordering or snapshot lineage. Encryption and compression add key/version and expansion concerns.

### Audit the completed index

Traverse every reachable page. Verify type, checksum, generation, byte bounds, local ordering, occupancy, and child count. Recompute child key bounds and prove separator routing. Confirm the leaf chain is ordered, acyclic, complete, and consistent with tree reachability. Compare a stable occurrence count or multiset against the source snapshot.

Generate queries at every minimum, maximum, separator, gap, duplicate boundary, and range endpoint. Use an independent sorted-array oracle. Test corruption, short write, missing page, stale generation, interrupted publication, and restart. Sampling ordinary queries will not expose systematic boundary defects.

Measure cold and warm point reads, ranges of varied selectivity, insert/update/delete mixes, batch sizes, compaction, cache occupancy, tail latency, bytes, requests, amplification, CPU, and recovery time. Include build sorting, temporary space, and publication in construction cost. Separate logical pages from physical requests.

## Definitions and Notation

Let $N$ be index entries, $P$ physical page bytes, $U$ usable payload bytes, $B$ model transfer words or records, $M$ fast-memory capacity, $\ell$ maximum leaf entries, $f$ internal fanout, $L=\lceil N/\ell\rceil$ leaf pages, $h$ page levels, and $K$ range-result entries. Let $R$ and $W$ be logical read and write operations; let $R_p,W_p$ be physical bytes or pages at a named boundary.

A **fence key** bounds a page’s legal key interval. A **separator** chooses among children. A **covering index** contains all data required for a query; a **non-covering index** requires record fetches. A **fill factor** is occupied usable capacity divided by eligible capacity. A **tombstone** records logical deletion pending reconciliation. A **root generation** identifies one published index version.

## Mechanisms, Invariants, or Proof Structure

### Point-search proof

Assume every internal page’s child intervals cover its own interval without gaps and separators implement the same boundary convention as search. Initially the root interval contains every indexed key. At each step, separator comparison selects the unique child interval that can contain query $x$. Induction preserves the claim until a leaf. Searching that leaf therefore returns the matching entry if present; absence is valid if the leaf’s ordered entries do not contain $x$.

### Bottom-up coverage proof

Sorted input is divided into disjoint consecutive leaf ranges whose concatenation is the input. Each parent contains a consecutive group of child pages, and parent groups form a disjoint consecutive cover of the previous level. Inductively, the root reaches every leaf exactly once. Combined with per-leaf coverage, every input occurrence is reachable exactly once.

### Publication invariant

Every page reachable from a published root is complete, checksum-valid under the recorded format, belongs to the intended snapshot/construction lineage, and was made durable before the reference that reaches it became visible. Reclamation touches only pages unreachable from every retained root and reader epoch. This is a protocol obligation, not a consequence of tree balance.

### Amortization discipline

Buffered and merge-based indexes defer work. State the potential or accounting unit used to charge future flush/merge bytes to accepted updates. Report worst-case and amortized latency separately. A favorable average does not prevent one large compaction or flush from violating a tail-latency objective.

## Alternatives and Trade-Offs

| Structure or build | Strength | Cost or risk | Suitable workload |
|---|---|---|---|
| sorted array plus binary search | compact, sequential bulk build | expensive updates | immutable snapshots |
| B/B+ tree | bounded point and range paths | scattered update I/O and splits | mixed ordered operations |
| bottom-up B-tree build | sequential pages after sort | snapshot and rebuild needed | large initial construction |
| buffered tree | amortized batched updates | search checks buffers; flush bursts | update batches plus ranges |
| LSM family | sequential ingestion and merge | read/space/write amplification | sustained write-heavy workloads |
| hash index | efficient equality lookup | no natural ordered ranges | exact-key workloads |
| cache-oblivious search tree | multilevel asymptotic locality | complex dynamic layout | unknown hierarchy parameters |
| learned position model | compact prediction on regular distributions | correction, drift, adversarial error | stable distributions with fallback |

Construction can also be online or offline, dense or reserve-filled, in-place or copy-on-write, serial or partitioned. Parallel bulk loading needs exact key-range ownership and reconciliation of partition boundaries; otherwise duplicate runs or gaps can corrupt global order.

## Failure Modes and Misconceptions

- **“Binary search is logarithmic, so it is I/O-optimal.”** Its probes may occupy distinct pages and ignore page fanout.
- **“A 16 KiB page has 16 KiB of keys.”** Headers, slots, pointers, checksums, alignment, prefix restarts, and fragmentation consume space.
- **“Any separator between children works.”** Construction and lookup must share an exact equality convention.
- **“Bulk load means insert in a loop.”** Bottom-up construction exploits global sorted order and writes each level directly.
- **“Full pages are always efficient.”** They may split immediately under the expected update distribution.
- **“Checksums prove a valid index.”** They do not establish order, coverage, separator correctness, or snapshot identity.
- **“One root write commits the tree.”** Referenced children must already meet the promised durability and visibility conditions.
- **“LSM trees eliminate writes.”** They defer and batch them, often rewriting data during compaction.
- **“Logical page reads equal device requests.”** Caches, read-ahead, compression, storage mapping, and remote systems change physical behavior.
- **“A learned prediction replaces search correctness.”** A bounded fallback and authoritative data structure remain necessary.

## Worked Examples

### Example 1

**Situation.** A sorted file has one million fixed-size entries, 200 entries per leaf, and internal fanout 100. Estimate page levels.

**Reasoning.** Leaves are $L=\lceil1{,}000{,}000/200\rceil=5{,}000$. Parent levels contain $\lceil5000/100\rceil=50$, then $\lceil50/100\rceil=1$ root. There are three levels: leaf, parent, root. A cold point search reads at most one page per level under the model.

**Conclusion.** High fanout converts a million-entry search into a three-page logical path.

### Example 2

**Situation.** Estimate fanout for 4096-byte pages, 128 bytes fixed overhead, 12-byte separators, and eight-byte child references.

**Reasoning.** Using $f$ references and $f-1$ separators, require $128+8f+12(f-1)\le4096$. Thus $20f\le3980$ and $f\le199$. Variable keys, slot arrays, alignment, and safety reserve can lower actual fanout.

**Conclusion.** The correct calculation uses usable encoding geometry, not physical bytes alone.

### Example 3

**Situation.** Trace the executable lookup for key 17.

**Reasoning.** Twenty odd keys form five leaves of at most four entries. Fanout three creates two internal parents and then one root. At each internal page, the search moves right while key 17 is at least the next child’s minimum separator. It reaches the leaf containing 17 and scans that leaf, visiting three abstract pages.

**Conclusion.** The trace validates one separator convention over an immutable unique-key index.

### Example 4

**Situation.** Construction stores each separator as the minimum of the right child, but lookup routes equality left. What query fails?

**Reasoning.** Suppose children begin with keys 10 and 20, so separator 20 denotes the right child’s minimum. Query 20 must go right. Equality-left routing sends it to the left page, whose maximum is below 20, producing a false negative even though the index is locally sorted.

**Conclusion.** Boundary tests at every separator are mandatory.

### Example 5

**Situation.** Ten leaves have capacity 100. A naive bulk loader fills nine leaves with 100 entries and leaves the tenth with 10, below a required 50% minimum. Repair it.

**Reasoning.** There are 910 entries. Redistribute them across ten leaves: nine can hold 91 and one 91, so every leaf has 91 entries. More generally, once page count is chosen, distribute the tail across the final pages while preserving order and capacity.

**Conclusion.** Sequential construction must enforce minimum occupancy rather than accepting an undersized tail.

### Example 6

**Situation.** A non-unique key occurs 600 times, while a leaf holds 200 composite entries. Can duplicates be kept on one leaf?

**Reasoning.** No. The run needs at least three leaves. If equality search follows only one candidate leaf, it misses values. Use `(key,record_id)` ordering plus a lower-bound search for `(key,-infinity)`, store duplicate-continuation fences, or use a posting structure whose overflow chain is itself verified.

**Conclusion.** Duplicate policy changes routing and physical representation.

### Example 7

**Situation.** Compare individual insertion with bulk loading for unsorted input.

**Reasoning.** Individual insertion performs a search path for each entry and may cause scattered page splits. Bulk loading first pays external sort, then scans sorted entries to form leaves and upper levels. If the index is constructed once from a large stable snapshot, sequential build commonly wins. If entries arrive continuously and immediate visibility is required, sorting the whole future data set is impossible; buffering or dynamic insertion is required.

**Conclusion.** Bulk loading is an algorithm enabled by snapshot and latency assumptions, not a universal replacement for updates.

### Example 8

**Situation.** A point query in a three-level tree reports one physical read. Is the height formula wrong?

**Reasoning.** No. The root and internal parent may be cached, while only the leaf misses. Tree height describes the logical path and cold upper bound. Physical reads depend on cache state, concurrency, prefetch, and storage mapping. Record both logical page visits and physical requests.

**Conclusion.** Cache hits refine observation without changing structural height.

### Example 9

**Situation.** A new copy-on-write index root is published before child-page flush completion, then power fails.

**Reasoning.** Recovery finds a valid root reference to missing or stale children. Root atomicity protected only the pointer, not the reachability invariant. The builder must complete and verify child durability, then parents, then root, and finally publish the root through a documented durable metadata operation.

**Conclusion.** Safe publication is ordered durability over the reachable graph.

### Example 10

**Situation.** An LSM configuration ingests 1 TiB and writes 9 TiB physically during flush and compaction. Reads average 1.2 component checks. Interpret the metrics.

**Reasoning.** At the measured storage boundary, write amplification is $9/1=9$. Average read amplification appears low, perhaps due to filters and caching, but the distribution and false positives matter; tail queries may consult more components. The numbers do not identify tiering/leveling quality without workload, tombstone, component, cache, and time-window context.

**Conclusion.** Amplification ratios are boundary- and workload-specific evidence, not structure names.

## Cross-Program Connections

- [Database Engineering DBE-021](../../18-database-engineering/modules/021-pages-blocks-and-database-files.md) develops concrete page and file organization.
- [Database Engineering DBE-031](../../18-database-engineering/modules/031-b-tree-structure.md) develops B-tree structure within database ownership.
- [Database Engineering DBE-041](../../18-database-engineering/modules/041-acid-and-transaction-boundaries.md) connects index visibility to transactions and recovery.
- [Data Structures Engineering DSE-031](../../17-data-structures-engineering/modules/031-binary-search-trees.md) supplies comparison-tree representation and invariants.
- [Operating Systems OS-031](../../22-operating-systems/modules/031-address-translation.md) explains caching and translation beneath memory-resident indexes.
- [Systems Engineering SYSENG-031](../../26-systems-engineering/modules/031-interface-identification.md) helps define comparator, snapshot, publication, and storage interfaces explicitly.

## References

1. Rudolf Bayer and Edward M. McCreight, “Organization and Maintenance of Large Ordered Indexes,” *Acta Informatica* 1, 173–189, 1972. [doi:10.1007/BF00288683](https://doi.org/10.1007/BF00288683). Checked 2026-09-05.
2. Jeffrey Scott Vitter, *Algorithms and Data Structures for External Memory*, Foundations and Trends in Theoretical Computer Science 2(4), 2008. [doi:10.1561/0400000014](https://doi.org/10.1561/0400000014). Checked 2026-09-05.
3. Lars Arge, “The Buffer Tree: A Technique for Designing Batched External Data Structures,” *Algorithmica* 37(1), 1–24, 2003. [doi:10.1007/s00453-003-1021-x](https://doi.org/10.1007/s00453-003-1021-x). Checked 2026-09-05.
4. Patrick O’Neil, Edward Cheng, Dieter Gawlick, and Elizabeth O’Neil, “The Log-Structured Merge-Tree (LSM-Tree),” *Acta Informatica* 33(4), 351–385, 1996. [doi:10.1007/s002360050048](https://doi.org/10.1007/s002360050048). Checked 2026-09-05.
5. Paolo Ferragina and Roberto Grossi, “The String B-Tree: A New Data Structure for String Search in External Memory and Its Applications,” *Journal of the ACM* 46(2), 236–280, 1999. [doi:10.1145/301970.301973](https://doi.org/10.1145/301970.301973). Checked 2026-09-05.
6. Michael A. Bender, Erik D. Demaine, and Martin Farach-Colton, “Cache-Oblivious B-Trees,” *SIAM Journal on Computing* 35(2), 341–358, 2005. [doi:10.1137/S0097539701389956](https://doi.org/10.1137/S0097539701389956). Checked 2026-09-05.
7. Goetz Graefe, “Modern B-Tree Techniques,” *Foundations and Trends in Databases* 3(4), 203–402, 2011. [doi:10.1561/1900000028](https://doi.org/10.1561/1900000028). Checked 2026-09-05.
8. Tim Kraska et al., “The Case for Learned Index Structures,” *Proceedings of SIGMOD 2018*, 489–504, 2018. [doi:10.1145/3183713.3196909](https://doi.org/10.1145/3183713.3196909). Checked 2026-09-05.

## Exercises

### Exercise 1

Define the difference between a separator, a fence key, and a leaf entry. Explain why one value may serve more than one role but the roles remain distinct.

### Exercise 2

An index holds 25 million fixed-size entries, 250 per leaf, with internal fanout 128. Derive leaf count, successive internal-page counts, levels, and a cold point-search page bound.

### Exercise 3

A bulk-built index returns false negatives only for keys equal to internal separators. Diagnose the defect, propose the smallest correction, and define the regression tests.

### Exercise 4

Compare a B+ tree built to 70% leaf occupancy with a tightly packed immutable sorted array for a workload containing 70% point reads, 20% short ranges, and 10% inserts. State what further facts decide the choice.

### Exercise 5

Design a crash-safe parallel bulk loader whose workers own disjoint key ranges. Specify partition boundaries, duplicate handling, page construction, verification, parent assembly, publication, cleanup, and evidence.

## Answers to the Exercises

### Answer 1

A leaf entry maps an indexed key to a value or record identity. A separator is consulted inside an internal page to select a child. A fence key states the legal lower or upper bound of a page, supporting routing validation and concurrency/recovery protocols. The minimum key of a right child may be copied as both separator and lower fence, but one role directs search while the other asserts range ownership. Updates, truncation, and page splits may give them different storage and maintenance rules.

### Answer 2

Leaves are $\lceil25{,}000{,}000/250\rceil=100{,}000$. The next levels contain $\lceil100{,}000/128\rceil=782$, then $\lceil782/128\rceil=7$, then $\lceil7/128\rceil=1$ root. The tree has four page levels, so a cold point lookup visits at most four pages under the simplified model. Cached upper pages can reduce physical reads but not logical height.

### Answer 3

Construction and search almost certainly disagree on equality routing—for example, separators are minimum-right keys while lookup sends equality left. Change lookup to choose the right child on equality, or rebuild separators under the lookup’s convention; changing only stored values in an existing persisted format requires compatibility care. Regression tests query every separator, predecessor, successor, global minimum/maximum, gaps, and duplicate boundaries, comparing with an independent sorted-array oracle. Audit every child interval against its parent separator.

### Answer 4

The sorted array is compact and strong for points/ranges on an immutable snapshot, but each insert requires rewriting or a delta structure. The 70%-filled B+ tree consumes more pages and may read more for scans, yet reserves local insertion capacity and supports dynamic maintenance. Decide using data size, cache residency, insert burst/location distribution, visibility latency, acceptable rebuild cadence, range length, record-fetch locality, concurrency, durability, write amplification, tail latency, and storage geometry. A valid design should compare an array-plus-delta/rebuild alternative, not pretend the array must update in place.

### Answer 5

Sample or sort under the final composite comparator, then choose nonoverlapping half-open key ranges; duplicate runs either stay within one owner or are partitioned by stable record identity. Each worker consumes a certified sorted slice, builds ordered leaves with valid occupancy and fences, writes immutable generated pages, and records counts, bounds, checksums, and source-run lineage. Verify worker outputs and prove adjacent bounds meet without gap or overlap. A coordinator assembles upper levels over worker leaf ranges, verifying children before parents. Make all reachable pages durable, then atomically publish one root generation. On failure, retain the old root and reclaim only unreferenced construction pages after reachability/reader checks. Evidence includes source/output occurrence reconciliation, separator-boundary queries, full page/link audit, injected worker/crash/short-write failures, restart tests, exact tool/storage versions, and separate logical/physical build metrics.
