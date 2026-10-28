---
module_id: DSE-074
program: Data Structures Engineering
level: 2
module_number: 74
title: Bulk Loading and Range Scans
status: complete
last_verified: 2026-08-30
---

# Bulk Loading and Range Scans

## One-Page Review

### Governing question

How can a storage engine transform a large snapshot into a dense, verified ordered index and publish it safely, while guaranteeing that subsequent bounded range scans return exactly the intended visible entries?

### Essential definitions

- **Bulk loading** builds an index from a collection or stream as a batch, normally sorting by the complete index-entry order and constructing pages bottom-up instead of performing n independent tree insertions.
- An **entry identity** is the full total-order tuple, such as `(normalized_key,row_id,version_tie)`, not merely the displayed user key.
- A **run** is a sorted intermediate sequence produced when input exceeds memory; a multiway merge combines runs into one ordered stream.
- **Fill target** is desired initial page occupancy. It is not a proof that every page will have exactly that occupancy or remain so.
- A **tail policy** redistributes the final underfilled page, permits a documented exception, or changes earlier boundaries without violating maximum sizes.
- **Bottom-up construction** packs leaf pages first, then derives parent separators/child references level by level until one root remains.
- An **online build** uses a base snapshot plus a protocol for writes occurring during scan/sort/build, followed by validation and atomic catalog/root publication.
- A **range scan** seeks a lower bound, traverses ordered leaves, applies visibility/predicate rules, and stops at an upper bound, limit, cancellation, or error.

### Central model, mechanism, or theorem

Given n entries, internal memory M, and external block size B, comparison sorting costs

`Sort(n)=Theta((n/B) log_(M/B)(n/B))`

block transfers in the standard external-memory regime. After sorting, bottom-up page construction and a full verification pass are sequential `Theta(n/B)` transfers up to encoding and metadata. This can avoid the random path visits and repeated splits of n ordinary insertions.

For a B+ tree with internal fan-out f, leaf capacity b, L leaves, and z qualifying entries, a range scan has ideal logical page shape `O(log_f L + z/b)` plus filtering and any base-record fetches. Real cost depends on buffer state, readahead, leaf physical locality, compression, visibility density, storage request granularity, cancellation, and concurrent restarts.

Correctness requires: the sorted stream is complete and ordered under the target collation; every entry is encoded once in a legal leaf; leaf boundaries and links agree; upper levels route to the leaves; the built image matches its source snapshot plus captured changes; and publication exposes either the old index state or the verified new one under the product's catalog/recovery rules.

### Critical invariants

1. Source extraction has explicit snapshot/epoch, schema, collation, normalization, uniqueness, and null semantics.
2. Runs and their merge are globally ordered by complete entry identity, with no loss or accidental duplication.
3. Every page respects byte limits, minimum/exception policy, checksum/version, and overflow ownership.
4. Leaf chain order equals routing-derived leaf order; each authoritative entry appears exactly once.
5. Every parent separator is valid for adjacent child ranges; all leaves remain at equal depth.
6. Online change capture has a gap-free start/cutover boundary and idempotent replay/deduplication contract.
7. Only a completely validated, durable image is published; abandoned generations remain unreachable and recoverably reclaimable.

### Common failures

- Sorting only user keys, making duplicates, nulls, locale rules, or versions nondeterministic.
- Trusting caller-declared sorted input without monotonicity checks and provenance.
- Filling every early page to 100%, creating a tiny illegal tail and immediate hot-edge splits.
- Building parent separators before final leaf redistribution, leaving stale ranges.
- Comparing counts but not entry identities, allowing loss and duplication to cancel.
- Starting change capture after the base snapshot or stopping it before publication is guaranteed.
- Publishing the catalog entry before pages, root, checksums, and allocation metadata are durable.
- Claiming fast scans from logical leaf linkage while ignoring physical locality, heap probes, visibility filtering, and tails.

### Compact example

For eleven sorted primes, leaf capacity four, and a 75% fill target, the target is three entries. Packing produces `[2,3,5] -> [7,11,13] -> [17,19,23] -> [29,31]`; the final two-entry leaf is legal under the stated minimum. A one-level root holds separators `[7,17,29]`. Inclusive scan `[6,23]` returns `7,11,13,17,19,23` in order.

### Connections

External sorting comes from DSE-071; B+ routing and leaf topology from DSE-073. DSE-077 develops immutable sorted runs, and DSE-079 studies compaction. Database Engineering adds online DDL, MVCC snapshots, uniqueness, catalog publication, replication, and query plans; Data Engineering adds distributed shuffle, partition validation, and backfills.

## Governing Question

How do we obtain the throughput and density advantages of sorted bottom-up construction without sacrificing entry completeness, update capture, crash safety, or exact range semantics?

## Why This Matters

Inserting billions of entries one at a time repeatedly descends the tree, dirties paths, splits partially filled pages, writes logs, and scatters allocation. If the target is a new index generation, sorting entries once and writing pages mostly sequentially can reduce transfers, improve compression, produce predictable occupancy, and expose verification checkpoints. The same pattern appears in database index creation, table rebuilds, snapshot restores, data migrations, search indexing, and sorted-run systems.

Bulk loading is dangerous because the happy path is simple. A sorted file can be incomplete. A collation can change between extraction and build. Duplicate checks can be disabled without later proof. A final page can violate occupancy. Concurrent writes can fall between snapshot and capture. A crash can publish a root whose children are not durable. A count comparison can miss one dropped and one duplicated entry. An index can be logically ordered but physically fragmented, making scans slow.

Range scans are the consumer-side dual. Their proof depends on the exact ordering and topology created by the build. Endpoint, duplicate, visibility, and continuation semantics must survive page boundaries and concurrent modification. Treating bulk load and scan as one module reveals the end-to-end invariant: an entry extracted under a declared snapshot must be reachable through routing and emitted exactly when its total identity and visibility satisfy the requested interval.

## Prerequisites and Retrieval

Retrieve:

- stable/external merge sorting, k-way merge, checksums, and manifest provenance;
- B+ separator-copy rules, composite duplicate order, leaf links/fences, and output-sensitive range cost;
- encoded-byte page capacity, overflow, fill/fragmentation, page IDs/generations, and buffer/WAL rules;
- MVCC snapshots, online change capture, idempotence, catalog transactions, and replication cutover;
- checked parsers, property testing, reconciliation, crash injection, and cold/warm benchmarking.

Diagnostic retrieval: if 1,001 entries target 100 entries per leaf, naive groups create ten full pages and one one-entry tail. A legal builder may redistribute across eleven pages (for example roughly 91 each), use a documented root/special-page exception if applicable, or choose other byte-aware boundaries. It may not silently violate minimum occupancy.

## Learning Objectives

After this module, you can:

1. specify source snapshot, complete sort key, uniqueness, collation, null, and version semantics;
2. derive external-sort and sequential construction transfer shapes without converting them to latency claims;
3. construct legal leaves with byte-aware fill and tail redistribution;
4. synthesize linked leaves and upper routing levels bottom-up;
5. design offline and online build publication, cleanup, restart, and recovery protocols;
6. specify exact forward/reverse range, endpoint, duplicate, visibility, limit, and resume behavior;
7. reconcile input, runs, built pages, routing, leaf chain, allocator, and catalog using identity-sensitive evidence;
8. benchmark build and scan throughput, amplification, locality, concurrency, recovery, and tail latency responsibly.

## Core Exposition

**Freeze the index definition.** Record schema version, indexed expressions, collation/operator class, normalization, null order, ascending/descending components, uniqueness, partial predicate, included payload, locator/version semantics, page format, compression, and target generation. Hash or otherwise identify this definition in every run/build manifest. A build under one collation cannot be published under another merely because byte keys look sorted.

**Choose a source consistency contract.** An offline build may prevent writes and scan one stable image. An online build takes a database snapshot and begins change capture at a precisely related log sequence/epoch. Define whether long transactions, deletes, updates changing indexed keys, schema changes, failed transactions, and visibility at cutover are included. “Scan while writes continue” is not a protocol.

**Extract complete entries.** Generate the exact physical/logical leaf identity, not a lossy projection. Validate source row/partition counts, byte totals, rejected entries, and stable provenance. If expressions or normalization can fail, define whether the build aborts or records deterministic rejection; a supposedly complete index cannot silently skip values.

**Sort within bounded memory.** Accumulate entries until the memory budget, sort each run by total order, and write immutable run files with header/version, minimum/maximum, entry count, byte length, checksum, definition ID, source epoch, and toolchain/build identity. During k-way merge, validate each run's monotonicity and manifest, then validate global output monotonicity. Stable sorting alone does not define duplicates; the total key does.

**Enforce uniqueness from adjacency.** Once globally sorted, equal unique keys are adjacent. Report both identities and source provenance, then abort publication. For nonunique indexes, preserve the documented tie order or build posting groups without losing per-record identity/MVCC state. Disabling uniqueness during ingest is safe only if this final check is authoritative and cannot be bypassed.

**Pack leaves by encoded bytes.** The fill target is a desired upper packing threshold, often below maximum to reserve future growth. Account for page header, slots, fences, links, checksum, item headers, alignment, prefix restart points, visibility data, and overflow references. Before sealing a page, ensure remaining entries can form legal future pages. Tail handling can redistribute recent pages, lower the target, or use an explicit permitted exception. Recompute separators after final boundaries.

**Construct the leaf topology.** Allocate page IDs within a new generation, encode each leaf, set low/high fences and previous/next links if supported, compute checksum, and record page manifest metadata. Sequential logical allocation can improve scan locality but filesystem/device placement remains empirical. Validate adjacent last/first ordering, link symmetry, no cycle, and union identity.

**Build upper levels bottom-up.** For each group of child pages fitting one internal page, derive separators from the declared boundary/truncation rule, encode child IDs/generations and fences, and emit a parent. Repeat until one root remains. Avoid a singleton tail internal page by redistributing child groups subject to minimum/maximum byte capacity. All leaves already share depth; each parent round preserves it.

**The bounded model exercises packing and scans.** It validates already sorted unique input, uses count capacity four with 75% target, emits four linked leaves, derives right-lower-bound root separators, checks union/order/routes, and performs an inclusive scan. It is a finite construction model, not an external sorter or storage engine.

<!-- bijux-verify: {"id":"bounded-bulk-load-range-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input_count=11\ninput_sorted=True\nleaf_capacity=4\nfill_target=3\nleaf_pages=2,3,5|7,11,13|17,19,23|29,31\nroot_separators=7,17,29\nheight_edges=1\nscan_6_23=7,11,13,17,19,23\nleaf_pages_touched=4\nchain_order=2,3,5,7,11,13,17,19,23,29,31\nvalid=True\nevidence=bounded_bulk_load_range_model\n","stderr":""}} -->
```python
class Leaf:
    def __init__(self, entries):
        self.entries = entries
        self.next = None


class BulkTree:
    def __init__(self, entries, capacity, fill_fraction):
        if entries != sorted(entries) or len(entries) != len(set(entries)):
            raise ValueError("input must be sorted and unique")
        self.capacity = capacity
        self.target = max(1, int(capacity * fill_fraction))
        groups = [entries[index:index + self.target] for index in range(0, len(entries), self.target)]
        self.leaves = [Leaf(group) for group in groups]
        for index in range(len(self.leaves) - 1):
            self.leaves[index].next = self.leaves[index + 1]
        self.separators = [leaf.entries[0] for leaf in self.leaves[1:]]

    def leaf_index(self, key):
        index = 0
        while index < len(self.separators) and key >= self.separators[index]:
            index += 1
        return index

    def scan(self, low, high):
        result = []
        touched = 0
        leaf = self.leaves[self.leaf_index(low)]
        while leaf is not None:
            touched += 1
            for entry in leaf.entries:
                if low <= entry <= high:
                    result.append(entry)
                if entry > high:
                    return result, touched
            leaf = leaf.next
        return result, touched

    def chain(self):
        result = []
        leaf = self.leaves[0]
        while leaf is not None:
            result.extend(leaf.entries)
            leaf = leaf.next
        return result

    def valid(self, source):
        sizes = all(0 < len(leaf.entries) <= self.capacity for leaf in self.leaves)
        order = self.chain() == source
        separators = self.separators == [leaf.entries[0] for leaf in self.leaves[1:]]
        links = all(self.leaves[index].next is self.leaves[index + 1] for index in range(len(self.leaves) - 1))
        terminal = self.leaves[-1].next is None
        routes = all(entry in self.leaves[self.leaf_index(entry)].entries for entry in source)
        return sizes and order and separators and links and terminal and routes


source = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
tree = BulkTree(source, 4, 0.75)
scan, touched = tree.scan(6, 23)
pages = "|".join(",".join(str(entry) for entry in leaf.entries) for leaf in tree.leaves)
print(f"input_count={len(source)}")
print(f"input_sorted={source == sorted(source)}")
print(f"leaf_capacity={tree.capacity}")
print(f"fill_target={tree.target}")
print(f"leaf_pages={pages}")
print("root_separators=" + ",".join(str(entry) for entry in tree.separators))
print("height_edges=1")
print("scan_6_23=" + ",".join(str(entry) for entry in scan))
print(f"leaf_pages_touched={touched}")
print("chain_order=" + ",".join(str(entry) for entry in tree.chain()))
print(f"valid={tree.valid(source)}")
print("evidence=bounded_bulk_load_range_model")
```

The model assumes a complete sorted unique integer list, one root level, count-based capacity, a legal two-entry tail, exclusive memory, and atomic publication. It performs no extraction, run generation, external merge, byte encoding, file/device I/O, concurrency, logging, crash recovery, visibility filtering, or performance measurement.

**Validate the finished image independently.** Compare exact multiset/identity digests between source snapshot, sorted stream, and leaf traversal; counts and commutative hashes alone are too weak without collision and multiplicity controls. Check every page's bytes, format, checksum, bounds, slots, overflow, and generation. Traverse from root for ranges/depth/reachability, traverse leaf links for identical ordered leaves, and reconcile all allocated pages with reachable/temporary/free ownership.

**Online build needs gap-free catch-up.** Start change capture no later than the snapshot boundary. Encode insert/delete/update as idempotent entry-identity changes with source transaction/log position. Apply committed changes in order or under a proven commutative protocol; handle a key update as deleting old identity and inserting new. Establish a cutover barrier where base plus replay equals the chosen publication state, then revalidate uniqueness and invariants. Retain enough log for restart and replicas.

**Publish one verified generation.** Write pages and manifests, satisfy required durability, record root/generation/catalog metadata transactionally, and make readers choose the new index only after publication. A crash before publication leaves reclaimable private artifacts; a crash after publication must recover every referenced page. Never overwrite the old generation before rollback no longer requires it. Reclamation follows reader, backup, replica, WAL, and cursor lifetimes.

**Specify range semantics as an API.** Define composite lower/upper bounds, inclusivity, collation, null order, direction, snapshot, predicate/visibility, limit, and continuation. Seek with routing; scan leaves; stop using a validated fence or first entry past bound; fetch base rows if required; preserve order through filtering. Resume strictly after the last emitted total identity under the same snapshot, or disclose weaker semantics and possible gaps/duplicates.

**Engineer physical locality empirically.** Logical consecutive page IDs may not be physically sequential; readahead can overfetch narrow ranges; compression can trade bytes for CPU; covering entries reduce heap probes but enlarge leaves; high fill improves scans but increases early split pressure. Measure logical page visits, physical requests/bytes, cache hits, readahead useful/waste, decompression, heap probes, filtered versions, and p50–p999 latency across result widths.

**Make builds restartable.** Give each extraction, run, merge, page batch, validation, replay, and publication artifact an immutable manifest and checksum. Resume only after verifying inputs and definition IDs. Clean abandoned private generations under a journaled ownership protocol. Bound disk/memory/WAL usage and fail before exhausting production capacity. Surface progress and cancellation without publishing partial state.

## Definitions and Notation

Let n be source entries, M in-memory items/bytes as qualified, B transfer block, R sorted runs, P output pages, f internal fan-out, b leaf capacity, L leaf count, z returned entries, and g build generation. `e=(normalized_key,tie,payload_or_locator)` is total entry identity. `snapshot_s` is base visibility state; `log_start..cutover` is captured change interval.

`FillTarget(page)` is a byte/count target below or equal to maximum, not universal occupancy. `Root(g)` names the private/published root. `SourceDigest`, `RunDigest`, and `LeafDigest` need a stated collision/multiplicity/order method. Range `[lo,hi)`, `(lo,hi]`, and reverse order are distinct contracts. Page visit, physical I/O, emitted entry, filtered entry, and base fetch are separate metrics.

## Mechanisms, Invariants, or Proof Structure

### Construction proof

1. Freeze definition and snapshot; extract every eligible total identity exactly once.
2. Prove run sorting and k-way merge preserve the source multiset and global order.
3. Partition sorted entries into legal byte-bounded leaves, repairing the tail before sealing boundaries.
4. Prove leaf links/fences enumerate precisely those leaves and entries.
5. Inductively synthesize parents whose separator intervals cover each child exactly, ending in one root.
6. Independently reconcile source, pages, routing, chain, and allocation before publication.

### Online publication proof

1. Relate change-capture start to base snapshot without a gap.
2. Normalize committed changes into idempotent exact-identity effects.
3. Replay through a chosen cutover and prove base plus changes equals target logical index.
4. Make every page/root/allocation durable under generation g.
5. Atomically publish catalog/root or recover old/new selection; never expose private partial state.
6. Delay old/private reclamation until all relevant lifetimes and recovery paths expire.

### Range proof

1. Routing lower-bound reaches the first possible leaf/entry.
2. Leaf and chain order is the total entry order represented by the build.
3. Snapshot visibility and predicate select exactly eligible entries.
4. Endpoint rule emits no value outside the interval and stops only after completeness is known.
5. Limit/resume uses last total identity and compatible snapshot to preserve pagination semantics.
6. Concurrency protocol proves link/fence/version and reclamation behavior or restarts safely.

## Alternatives and Trade-Offs

| Choice | Strength | Cost/proof burden |
|---|---|---|
| Repeated insertion | reuses mature update path | random I/O, splits, low density |
| Bottom-up sorted build | sequential dense construction | sort space and separate code path |
| Offline build | simple snapshot/cutover | write unavailability |
| Online build | availability | capture, replay, cutover complexity |
| High fill target | scan density, compression | early split pressure |
| Reserved free space | absorbs future writes | larger initial index/scans |
| Full separators | simple correctness | lower fan-out |
| Truncated separators | compact upper levels | collation proof and migration |
| Full rows/covering leaves | fewer base fetches | larger entries and writes |
| Locators only | dense leaves | scattered base probes |
| Logical sequential IDs | easy chain/manifests | not proof of physical locality |
| Bulk replace generation | clean rollback | temporary space and catch-up |
| In-place rebuild | lower duplicate space | complex recovery and availability |

## Failure Modes and Misconceptions

- **“Input is already sorted.”** Verify total-order monotonicity and definition provenance.
- **“Stable sort solves duplicates.”** Define tie identity and uniqueness semantics first.
- **“Fillfactor is guaranteed occupancy.”** It is a target subject to bytes, tail, exceptions, and later workload.
- **“Pack until full, then handle the tail.”** Reserve feasibility or redistribute earlier pages.
- **“Counts match, so no loss occurred.”** A drop and duplicate can cancel; reconcile identities/multiplicity/order.
- **“Leaf links make the tree valid.”** Routing, fences, depth, reachability, and allocator also matter.
- **“Start capturing changes after scanning.”** Writes in the gap vanish.
- **“Replay every observed event.”** Apply committed, ordered/idempotent semantics with abort/retry handling.
- **“Rename the root file and the build is atomic.”** Catalog, storage durability, allocation, replicas, and recovery define atomicity.
- **“Range scan cost is logarithmic.”** Output pages, filtering, heap probes, and retries usually dominate wide ranges.
- **“Sequential page IDs mean sequential device I/O.”** Measure actual requests and placement.
- **“Fast build proves usable index.”** Require independent logical/physical/crash validation before publication.

## Worked Examples

### Example 1

**Problem.** Naively pack 1,001 fixed entries into capacity-100 leaves.

**Derivation.** Ten full leaves plus one one-entry tail may violate minimum occupancy. Redistribute over eleven pages, about 91 entries each, while respecting exact bounds.

**Conclusion.** Tail feasibility influences earlier boundaries.

### Example 2

**Problem.** Build the model's four leaves.

**Derivation.** Target is `floor(4*0.75)=3`; groups are 3,3,3,2 entries. Root lower-bound separators are first entries of leaves after the first: 7,17,29.

**Conclusion.** Final boundaries determine separators.

### Example 3

**Problem.** Detect a duplicate in a unique build.

**Derivation.** Sort `(normalized_key,row_id)` but compare adjacent normalized keys for uniqueness. Report both row IDs and abort; do not discard one nondeterministically.

**Conclusion.** Total order and unique constraint are related but distinct comparisons.

### Example 4

**Problem.** A locale/collation library changes between extraction and merge.

**Derivation.** Definition IDs differ, so reject resume/publication and rebuild with one pinned version or durable normalized sort representation.

**Conclusion.** Ordering semantics are part of format provenance.

### Example 5

**Problem.** Snapshot starts at LSN 100 but capture begins at 120.

**Derivation.** Committed key changes in `(100,120)` can be absent from both base and replay. Start capture before/equal snapshot or use a database-native protocol proving coverage.

**Conclusion.** Online builds require a gap-free temporal boundary.

### Example 6

**Problem.** An update changes index key A to B.

**Derivation.** Replay exact deletion of old entry identity and insertion of new identity once the transaction commits; idempotence/dedup handles retries.

**Conclusion.** “Latest row image” alone may not remove stale index entries.

### Example 7

**Problem.** Crash after page durability but before catalog publication.

**Derivation.** Old index remains authoritative; generation g pages are private and recoverably reclaimable/resumable from manifest. Readers never infer roots by scanning files.

**Conclusion.** Private generation separates construction from publication.

### Example 8

**Problem.** Scan inclusive `[6,23]` in the model.

**Derivation.** Routing lower bound 6 enters the first leaf because its interval is below separator 7; it emits from 7 through the leaf ending 23, then inspects the next leaf's 29 to establish stop. The result has six entries and four touched leaves in this simple protocol.

**Conclusion.** Stop evidence and fences affect pages touched.

### Example 9

**Problem.** Two builds share counts and XOR digest after a drop/duplicate.

**Derivation.** Weak commutative summaries can cancel or collide. Use exact sorted comparison where feasible or cryptographic, multiplicity-sensitive hierarchical reconciliation plus samples/invariants.

**Conclusion.** State what reconciliation evidence can and cannot prove.

### Example 10

**Problem.** Dense build improves logical leaf count but scan latency worsens.

**Derivation.** Investigate physical fragmentation, readahead waste, decompression CPU, larger covering entries, heap random reads, visibility filtering, cache eviction, and concurrent latch waits.

**Conclusion.** Density is one causal factor, not the service result.

## Cross-Program Connections

- **Database Engineering:** online CREATE INDEX, unique validation, MVCC, catalog transactions, WAL, replication, vacuum, and planner statistics operationalize builds.
- **Data Engineering:** snapshot extraction, external shuffle/sort, partition manifests, backfill catch-up, reconciliation, and atomic dataset publication use the same workflow.
- **Operating Systems:** cache/direct I/O, temporary-file allocation, readahead, async writes, barriers, ENOSPC, and cleanup determine resource behavior.
- **Distributed Systems:** sharded builds add partition epochs, global order/ranges, retries, worker loss, object-store commit, and coordinator recovery.
- **Security Engineering:** untrusted source/run/page bytes, collation confusion, checksum substitution, path/resource exhaustion, and token integrity are trust boundaries.
- **Performance Engineering:** memory/disk budgets, merge fan-in, parallelism, NUMA, compression, amplification, locality, tails, and recovery require controlled experiments.

## References

1. Alok Aggarwal and Jeffrey Scott Vitter, [“The Input/Output Complexity of Sorting and Related Problems”](https://www.cse.wustl.edu/~angelee/archive/cse341/fall14/papers/AggarwalVi88.pdf), *CACM* 31(9), 1988. Foundational external sorting transfer bounds.
2. Carnegie Mellon Database Group, [“Tree Indexes”](https://15445.courses.cs.cmu.edu/fall2024/notes/08-indexes1.pdf), 15-445/645 notes, 2024. Authoritative educational treatment of B+ trees, bulk loading, and scans.
3. PostgreSQL Global Development Group, [`CREATE INDEX`](https://www.postgresql.org/docs/current/sql-createindex.html), current documentation accessed 2026-08-30. Official concurrent build, fillfactor, parallel build, and publication-facing behavior.
4. PostgreSQL Global Development Group, [`tuplesort.c`](https://github.com/postgres/postgres/blob/master/src/backend/utils/sort/tuplesort.c), current source and design commentary accessed 2026-08-30. Maintainer external run generation, merge, memory, and parallel-sort implementation.
5. Oracle MySQL, [“Sorted Index Builds”](https://dev.mysql.com/doc/refman/8.4/en/sorted-index-builds.html), MySQL 8.4 documentation accessed 2026-08-30. Official scan, run, merge, and B-tree index-build phases.
6. Oracle MySQL, [“Physical Structure of an InnoDB Index”](https://dev.mysql.com/doc/refman/8.4/en/innodb-physical-structure.html), MySQL 8.4 documentation accessed 2026-08-30. Official fill factor, page structure, and sorted-build context.
7. PostgreSQL Global Development Group, [“Indexes and ORDER BY”](https://www.postgresql.org/docs/current/indexes-ordering.html), current documentation accessed 2026-08-30. Official ordered-index scan direction, ordering, and limit behavior.
8. PostgreSQL Global Development Group, [`nbtree` README](https://github.com/postgres/postgres/blob/master/src/backend/access/nbtree/README), current source documentation accessed 2026-08-30. Maintainer leaf links, high keys, scans, splits, deletion, and concurrent structural invariants.

## Exercises

### Exercise 1

Specify a complete offline bulk-load contract from index definition and snapshot through extraction, external sort, unique validation, leaf/tail packing, parent synthesis, independent audit, durable publication, and cleanup. Give I/O cost shapes and limitations.

### Exercise 2

For 1,001 fixed-size entries, leaf maximum 100, minimum 50 except root, and 90% target, construct a legal near-target leaf-size distribution. Explain why naive target-sized groups fail or succeed and derive parent separators.

### Exercise 3

Design an online secondary-index build under MVCC. Specify snapshot/capture boundary, change encoding, transaction outcomes, replay, uniqueness, cutover, catalog/WAL/replica behavior, crash restart, rollback, and old/private generation reclamation.

### Exercise 4

Specify a production forward range-scan API for composite duplicates. Cover endpoints, collation/nulls, visibility/predicate, seek, leaf/fence traversal, base fetches, limit, cancellation/error, retries, resume token, snapshot expiry, and evidence.

### Exercise 5

Audit a builder that trusts sorted input, sorts user key only, packs pages to 100%, starts capture after extraction, checks only counts/XOR, publishes before fsync, and claims fast ranges from sequential logical page IDs. Provide corrections and verification gates.

## Answers to the Exercises

### Answer 1

Freeze schema/expression/collation/null/unique/tie/payload/page/compression generation. Take stable snapshot, extract every eligible exact identity with provenance, form checksummed bounded-memory sorted runs, k-way merge while validating run/global monotonicity, and reject adjacent duplicate unique keys. Pack byte-bounded leaves under fill target while reserving legal tail feasibility; finalize links/fences, then build legal parent groups bottom-up and one root.

Independently validate bytes/checksums/ranges/depth, routing-versus-chain leaves, exact source/leaf identities and multiplicities, overflow, and allocator ownership. Durably write private generation and manifest, transactionally publish its root/catalog, retain old state for rollback, then safely reclaim abandoned/old pages. External sort has standard `Theta((n/B) log_(M/B)(n/B))` transfers; construction/audit are sequential Theta(n/B), but CPU, compression, physical layout, WAL, and latency require measurement.

### Answer 2

At 90%, target is 90 entries. Eleven naive target-sized groups would be ten groups of 90 and one of 101, which exceeds maximum; twelve groups would be eleven of 90 and one of 11, below minimum. Instead use eleven pages because `ceil(1001/100)=11` and place 91 entries in every page: `11*91=1001`. Each page is within 50..100 and close to target.

For right-lower-bound B+, leaf i after the first contributes its first complete entry key (or proven distinguishing prefix) as the parent separator. Exact separator values depend on the ordered input, not counts. If the root cannot reference all eleven leaves, group legal internal pages while avoiding a singleton tail and repeat upward.

### Answer 3

Start durable change capture at or before the base MVCC snapshot boundary and record exact committed entry effects with transaction/log identity. Extract visible base rows, build private generation, and replay committed insert/delete/key-update as idempotent deletion-old plus insertion-new; ignore aborts and deduplicate retries. Establish a cutover barrier/log position, drain through it, recheck unique constraints and full invariants, then make pages/root durable and publish catalog metadata transactionally.

Replicas must receive/rebuild compatible generation and publication order; retain WAL/change log until every restart/replica no longer needs it. A crash before publication leaves old catalog authoritative and private artifacts resumable/reclaimable; after publication recovery must find all referenced pages. Roll back catalog/root to retained old generation only under a defined protocol. Retire old/private pages after readers, snapshots, backups, replicas, cursors, and recovery references expire.

### Answer 4

Define total composite order, normalized collation/null handling, lower/upper inclusivity, direction, snapshot/isolation, predicate, limit, projection, cancellation, and partial-error semantics. Seek lower bound through validated routing, pin/version/latch leaf under proven protocol, emit only visible/predicate-matching entries in order, fetch base records with revalidation when required, and move by validated link/fence until bound or limit proves completion.

Resume token identifies index definition/generation, direction/bounds, last emitted complete identity, and snapshot/expiry; resume strictly beyond it. Authenticate/bound tokens for untrusted clients. On structural races validate/restart without silent gaps/duplicates; on expired snapshot/index replacement return explicit failure unless weak semantics are documented. Verify against an oracle across duplicates/endpoints/empty ranges, schedules and reclamation, crash/reopen, fuzzed pages, and benchmark widths/cache/heap probes/tails.

### Answer 5

Pin definition and verify total-order monotonicity; sorting user key alone is nondeterministic for duplicates/versions, so use complete identity and separate unique adjacency check. Use byte-aware target plus future-tail feasibility and overflow maximums rather than unconditional 100%. Capture must cover the snapshot boundary without a temporal gap and replay committed exact changes.

Counts and XOR can hide balanced loss/duplication and collisions; reconcile exact identities or strong multiplicity/order-sensitive hierarchical digests plus independent traversal. Durably write/check pages, manifest, allocation, and root before atomic catalog publication, with crash tests at every boundary and rollback generation. Logical page IDs do not prove physical sequentiality or scan speed; measure actual requests, readahead, cache, decompression, heap probes, visibility, concurrency, and p50–p999 after logical, byte, topology, recovery, and fault gates pass.
