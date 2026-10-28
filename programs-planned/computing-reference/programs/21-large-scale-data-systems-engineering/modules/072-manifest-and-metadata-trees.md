---
module_id: LSDS-072
program: Large-Scale Data Systems Engineering
level: 2
module_number: 72
title: Manifest and Metadata Trees
status: complete
last_verified: 2026-09-04
---

# Manifest and Metadata Trees

## One-Page Review

### Governing question

How should a large analytical table organize metadata between a snapshot root and millions of content files so planning is selective, incremental commits reuse unchanged structure, readers obtain one consistent view, and metadata maintenance does not become the next scaling bottleneck?

### Essential definitions

- A **metadata root** is the snapshot-owned object from which every file relevant to that snapshot can be discovered.
- A **metadata tree** is a hierarchy whose internal nodes summarize and reference lower nodes and whose leaves describe content files.
- A **manifest list** is a snapshot-level index of manifest files and their coarse summaries.
- A **manifest** is an immutable collection of entries for data or delete files, normally sharing a partition-spec and content type.
- A **manifest entry** records a content file's path, state, partition tuple, size, row count, column metrics, sequence/provenance, and optional integrity data.
- **inclusive pruning** may retain false positives but must never exclude a file that could satisfy the query.
- **metadata amplification** is metadata bytes, objects, requests, or CPU required per unit of useful data planning or change.
- **structural sharing** lets a new snapshot reuse immutable metadata subtrees that remain valid.
- **checkpointing** materializes accumulated logical changes into a bounded replay base.
- A **metadata rewrite** repacks or rebuilds metadata without changing the table's logical rows.

### Central model, mechanism, or theorem

For snapshot $s$, let root $R_s$ reference internal nodes $N$ and leaf entries $E$. A query predicate $q$ traverses a node only when its conservative summary may overlap $q$. If $C(q)$ is the set of content files that can contain a matching row, a sound planner must return candidate set $P(q)$ satisfying

$$C(q)\subseteq P(q)\subseteq F_s.$$

False positives cost planning and I/O; false negatives violate correctness. A balanced hierarchy with fanout $b$ and $n$ leaves has ideal height about $\lceil\log_b n\rceil$, but real cost also depends on node sizes, selectivity, caching, request latency, skew, and parallelism. New snapshots should rewrite only paths affected by additions/removals and reuse immutable unaffected nodes. Periodic metadata compaction or checkpoints bound tiny-node counts and replay depth without changing snapshot membership.

### Critical invariants

- A snapshot root resolves to one immutable, complete, version-compatible metadata graph.
- Each live content file has one unambiguous live entry in the snapshot's logical state.
- Parent summaries conservatively cover every descendant relevant to their pruning semantics.
- Unknown, missing, truncated, encrypted, NaN-bearing, or evolution-incompatible statistics weaken pruning; they never justify exclusion.
- Field and partition identities, not display names or directory positions, bind metrics across schema and partition evolution.
- Added, existing, and deleted entry states plus sequence/provenance fields are interpreted under the format version that wrote them.
- Structural sharing never mutates metadata reachable from an older snapshot.
- Checkpoints and metadata rewrites preserve the same logical file set, delete applicability, schema/spec bindings, and audit lineage.
- Metadata caches are keyed by immutable identity or validated version and cannot combine nodes from different snapshots.
- Metrics cover root load, nodes and bytes read, pruning at each level, candidate files, cache behavior, replay depth, corruption, and rewrite effectiveness.

### Common failures

Common failures include one flat file list that every query must parse; one manifest per data file; giant manifests that cannot be fetched or decoded cheaply; summaries computed from only part of a node; using an exclusive predicate for an inclusive index; treating missing bounds as empty; comparing encoded bounds under the wrong logical type; matching evolved fields by name; mixing partition specifications; retaining thousands of tiny manifests after small commits; rebuilding all metadata on every append; trusting mutable path-keyed caches; losing deletion or sequence semantics during compaction; and optimizing metadata bytes while multiplying object-store requests.

### Compact example

A snapshot contains 10,000 data files in 100 manifests of 100 entries. The manifest list stores each manifest's day range. A query for one day retains 4 manifests, then file-level bounds retain 37 files. The planner reads 1 manifest list plus 4 manifests instead of 100 manifests, and schedules 37 rather than 10,000 files. If one manifest has an unknown day bound, it must also be retained. A later append reuses the 100 old manifests and adds one new manifest; a maintenance rewrite may later combine undersized manifests, but must publish a new snapshot-equivalent metadata graph rather than mutate the old nodes.

### Connections

[LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md) defines content layout, [LSDS-048](048-state-snapshots-and-recovery.md) introduces checkpoint recovery, [LSDS-061](061-distributed-logical-and-physical-plans.md) supplies distributed planning, [LSDS-067](067-runtime-filtering-and-dynamic-pruning.md) adds runtime evidence, [LSDS-070](070-diagnosing-a-distributed-query-from-plan-to-network.md) supplies diagnostic discipline, and [LSDS-071](071-table-snapshots-and-atomic-commit.md) supplies the publication and retention contract.

## Governing Question

A snapshot that names ten files is easy to describe. A snapshot that covers tens of millions of data and delete files cannot put every descriptor in one frequently rewritten object. Query coordinators would spend seconds or minutes downloading and decoding metadata before scheduling work. Small streaming commits could create vast numbers of tiny metadata objects; large rewrites could create objects too large for memory, network, or single-thread decoding. The table needs an index over its own files.

That index is correctness-bearing. It decides which objects a query will inspect, which delete files apply, what schemas and partition specifications interpret fields, and which entries remain reachable. A false positive merely wastes work. A false negative silently loses rows or deletes and is therefore unacceptable. Metadata structure must balance selective pruning, incremental update, bounded object counts, parallel planning, caching, evolution, corruption detection, and maintenance.

The governing question is not simply “how large should a manifest be?” It is how to build and operate a versioned metadata tree whose summaries are conservative, whose identities survive evolution, whose immutable nodes can be shared, whose replay or traversal cost stays bounded, and whose maintenance can be proven logically neutral.

## Why This Matters

At scale, metadata is a distributed data system inside the data system. It has storage formats, indexes, snapshots, caches, compaction, skew, version compatibility, security boundaries, failure recovery, and observability. Optimizing Parquet scans while requiring the coordinator to deserialize gigabytes of manifests merely moves the bottleneck.

Planning latency affects every query, including queries that ultimately read no rows. A selective point query may be dominated by listing, root lookup, manifest fetches, decompression, object allocation, and predicate evaluation. Concurrent queries can stampede the same roots and nodes. A damaged summary can be worse than a damaged performance hint because readers may trust it to exclude data.

Good metadata trees also make commits cheaper. Immutable nodes allow structural sharing: an append can introduce a small leaf collection and a new root while reusing old manifests. That reduces rewrite amplification and creates stable cache keys. However, indefinite reuse plus many small commits fragments metadata. Maintenance must therefore repack leaves, merge checkpoints, or rebuild indexes while preserving logical state and old-snapshot readability.

## Prerequisites and Retrieval

Review storage layout in [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md), checkpoint recovery in [LSDS-048](048-state-snapshots-and-recovery.md), distributed plans in [LSDS-061](061-distributed-logical-and-physical-plans.md), dynamic pruning in [LSDS-067](067-runtime-filtering-and-dynamic-pruning.md), distributed diagnosis in [LSDS-070](070-diagnosing-a-distributed-query-from-plan-to-network.md), and snapshot publication in [LSDS-071](071-table-snapshots-and-atomic-commit.md).

You should understand immutable objects, trees and directed acyclic graphs, fanout, logarithms, range and set summaries, Bloom filters, three-valued logic, schemas, stable field IDs, partition transforms, column metrics, MVCC, object-store request cost, checksums, caches, compaction, checkpoints, and optimistic commits.

Before an incident, retain a root descriptor, snapshot identity, format/protocol version, schema and partition-spec registries, manifest inventory, representative nodes, planner trace, cache state, relevant object-store request metrics, and checksums. A reconstructed file list without the original root and version may conceal the exact inconsistency being investigated.

## Learning Objectives

After this module, you should be able to:

1. Model a snapshot as a rooted immutable metadata graph rather than a directory listing.
2. Design manifest-list, manifest, and entry schemas with stable identity and evolution semantics.
3. Prove that hierarchical pruning is inclusive and therefore cannot produce false negatives.
4. Estimate traversal height, metadata bytes, request count, replay work, and write amplification.
5. Choose node size and fanout using workload measurements rather than a universal constant.
6. Explain how structural sharing reduces commit cost and how fragmentation accumulates.
7. Design checkpoints and metadata rewrites that preserve logical table state.
8. Diagnose planning latency across root lookup, fetch, decode, pruning, cache, and file scheduling.
9. Test corrupt, missing, stale, skewed, evolved, and adversarial metadata cases.
10. Specify metrics and audits that detect metadata correctness and scaling regressions.

## Core Exposition

### From files to a metadata graph

Let $F_s$ be the live content-file set of snapshot $s$. A flat representation stores all descriptors in one object. Its full-scan metadata cost may be efficient sequentially, but every commit rewrites the object and every selective query must open it. Splitting descriptors into leaves permits incremental updates and parallel reads, but creates the need for a root or internal index.

A common shape runs from a catalog reference to table metadata and a snapshot, then to a manifest list or checkpoint root, then to manifests, sidecars, or checkpoint parts, and finally to data-file and delete-file entries.

The exact names differ among table formats. The durable abstraction is a root that pins the snapshot, internal nodes that name and summarize children, and leaves that carry file-level facts. Some systems use a tree, some a DAG because snapshots share nodes, and some use an ordered log plus periodic checkpoints. A planner may see a tree during one read even though the history forms a larger DAG.

### Leaf entries are typed facts

A useful entry carries more than a path. It normally includes content kind, immutable file identity or path, format, byte size, row or record count, partition tuple, schema/spec identity, sort information, column bounds, null/NaN counts, value counts, deletion semantics, sequence or commit provenance, encryption/integrity metadata, and an entry state such as added, existing, or deleted.

Every field needs an interpretation contract. Are lower and upper bounds inclusive? Are strings truncated? How are binary values ordered? What does an absent bound mean? Can a count be unknown? Which schema types decode the bytes? Does a sequence identify logical data age or the file-writing snapshot? Ambiguity makes cross-engine interoperability unsafe.

Metrics are advisory for pruning but correctness-bearing once used. If a writer cannot compute a trustworthy bound, it should encode unknown. Unknown retains the file. It must not be silently represented as an empty range. Statistics also require confidentiality review: min/max strings, distinct sketches, or key ranges can reveal sensitive values even when data files are encrypted.

### Internal nodes summarize conservatively

Suppose node $u$ has descendant content set $D(u)$. Its summary $S(u)$ may include partition lower/upper bounds, null/NaN presence, file and row counts, bytes, content kind, sequence ranges, or index pointers. For a query $q$, `may_match(S(u), q)` may return true for a nonmatching subtree, but it must return true whenever any descendant file could match.

Formally, with $M(f,q)$ meaning file $f$ can contain a qualifying row:

$$\left(\exists f\in D(u):M(f,q)\right)\Rightarrow \operatorname{may\_match}(S(u),q).$$

The converse need not hold. This one-way implication is the pruning safety condition. It must survive null semantics, NaN, collation, type promotion, timestamp zone rules, decimal scale, truncated bounds, partition transforms, and unknown values.

Hierarchical pruning first rejects whole internal nodes, then rejects individual leaves or files. Each level should record how many candidates entered, how many were rejected, and why. Otherwise operators see only final planning time and cannot tell whether the root summaries, leaf metrics, cache, or decoder failed to help.

### Fanout, size, and cost

In an ideal balanced $b$-ary tree containing $n$ leaf entries, height is approximately

$$h=\lceil\log_b n\rceil.$$

This is a useful shape model, not a latency prediction. Large fanout reduces height but makes each node larger, more expensive to rewrite, decode, and cache. Small fanout increases levels and requests. Object-store latency can make 100 small GETs worse than one larger GET; memory limits can make one huge manifest worse than parallel moderate ones.

Model planning cost as

$$T_{plan}=T_{root}+T_{fetch}+T_{decode}+T_{prune}+T_{schedule},$$

with fetch cost depending on bytes, request count, cache hits, concurrency, throttling, and locality. Report each component. An average hides tail objects and skewed manifests, so retain distributions by node type and size.

### Structural sharing and copy-on-write

Immutable metadata makes old nodes safe to reuse. If an append adds files for one partition, the new snapshot can reference old manifests plus a new manifest. If an internal tree is used, it can copy the path from the changed leaf to the root and reuse all other subtrees. The update cost approaches the changed paths rather than total table size.

Sharing imposes lifecycle obligations. A node cannot be physically deleted while any retained snapshot, branch, tag, or active-read guarantee can reach it. Cache entries can be keyed by content hash or immutable location and safely shared, but authorization and tenant boundaries still apply. A metadata rewrite creates new nodes and a new published root; it never edits shared nodes in place.

### Log replay and checkpoints

An ordered transaction log represents state as a base plus actions. Reconstructing version $v$ from the beginning costs work proportional to history. A checkpoint materializes table state at version $c$; a reader loads the checkpoint then replays actions $(c,v]$. Multi-part checkpoints form a small tree: a checkpoint manifest names parts, and parts hold state entries.

Checkpoint interval trades write work against read replay. Too frequent wastes commit resources and produces metadata churn. Too sparse increases cold-start latency and failure exposure during long replay. Trigger policy can include action count, replay bytes/time, checkpoint age, commit rate, reader population, and existing checkpoint health. A checkpoint must be complete, version-bound, integrity-checked, and optional until atomically discoverable. Readers need a defined fallback to an earlier valid checkpoint plus later log entries.

### Manifest accumulation and rewrite

Small commits often create small manifests. If every snapshot adds one, a query may fetch thousands of objects even when total metadata bytes seem modest. Conversely, continuously merging all manifests makes every commit expensive and increases conflict surface. Foreground writers should produce reasonably sized nodes; asynchronous maintenance should consolidate fragmentation under an explicit policy.

A metadata rewrite reads live entries, groups them by stable compatibility boundaries such as content kind and partition specification, writes replacement manifests, verifies equivalence, and publishes a new snapshot. It should preserve file identities, live/deleted semantics required by history, data and file sequence meanings, schema/spec bindings, delete applicability, partition tuples, metrics, and snapshot audit information. Count equality alone is insufficient: two different file sets can have the same count.

### Evolution and heterogeneous leaves

Tables evolve schemas, partition specifications, sort orders, delete encodings, statistics, and protocol features. Old content stays bound to the IDs and rules under which it was written. A manifest may therefore carry a partition-spec ID and schema context. A current query predicate is projected through each relevant historical specification. Display names are not stable identity.

Internal summaries spanning heterogeneous children must either carry enough identity to interpret each group or weaken themselves. For example, combining two different partition transforms into one range without tagging the transform is unsafe. It may be better to keep separate manifests per specification and let the upper level identify them.

Readers must reject unsupported required protocol features. Silently ignoring a new entry kind, deletion vector, encryption mode, or row-lineage field may produce plausible but incorrect data. Optional unknown statistics can usually degrade to no pruning; unknown required semantics cannot.

### Caching and concurrency

Metadata is highly cacheable because committed objects are immutable. Cache keys should include immutable location plus length/checksum/version, or a content identity. The mutable catalog reference requires validation or short-lived policy; an old root can return a consistent but stale snapshot, while mixing a new root with stale mutable children is worse.

Use request coalescing so many queries fetching the same cold node share one load. Bound decode memory and concurrency; a cache stampede can overload the object store or coordinator. Negative caching of missing objects requires particular care during eventual publication and recovery. Corruption and authorization failures should not be cached as permanent absence without policy.

Concurrent metadata maintenance follows the atomic commit protocol from LSDS-071. It plans against base snapshot $b$, produces equivalent replacement nodes, validates that the relevant file set and semantics have not changed, then publishes. If the head moved, it may rebase only if equivalence still holds. A rewrite racing with a delete or append needs operation-specific conflict handling.

### Security, integrity, and audit

Metadata exposes paths, partitions, bounds, counts, schemas, histories, and sometimes encryption-key references. Apply least privilege separately to table roots, metadata, content, maintenance, and audit. A reader that can access data but not required metadata cannot safely read the table; a user who can read metadata may still learn sensitive facts.

Protect objects with transport integrity, checksums, authenticated catalogs, and immutable writes. Validate root-to-child identity, declared lengths, formats, required fields, ordering constraints, and duplicates. Store writer, operation, snapshot, parent, application transaction, and maintenance provenance. Repair tools should produce an auditable new root, not patch historical objects invisibly.

### Operational workflow

For slow planning, first pin the table reference and snapshot. Separate catalog lookup, root read, checkpoint/log replay, manifest-list read, manifest fetch, decode, pruning, cache, and split construction. Count nodes and bytes at every level, cache outcomes, request latency, retries/throttling, candidate reduction, and coordinator memory/CPU. Compare the same query and snapshot across warm and cold caches.

For suspected inconsistency, stop destructive maintenance. Preserve the root and graph, verify object existence and checksums, traverse reachability independently, and compare planner candidates with a conservative full metadata scan. Identify the first node whose summary or entry violates its child facts. Repair only after determining whether the defect is a writer bug, corruption, unsupported version, stale cache, unauthorized mutation, or cleanup race.

## Definitions and Notation

Let:

- $s$ be a snapshot and $R_s$ its immutable metadata root;
- $G_s=(V_s,E_s)$ be the reachable metadata graph;
- $F_s$ be the live content-file set represented by $G_s$;
- $D(u)$ be the descendant content files of metadata node $u$;
- $S(u)$ be the conservative summary stored for $u$;
- $q$ be a query predicate;
- $C(q)=\{f\in F_s: f\text{ can contain a row satisfying }q\}$;
- $P(q)$ be the planner's candidate file set after metadata pruning;
- $n$ be the number of leaves or entries and $b$ an idealized fanout;
- $h=\lceil\log_b n\rceil$ be idealized tree height;
- $B_m$ and $O_m$ be metadata bytes and objects read;
- $B_d$ be content bytes selected;
- $A_b=B_m/B_d$ be byte amplification when $B_d>0$;
- $H$ and $M$ be cache hits and misses, with hit ratio $H/(H+M)$ when the denominator is positive;
- $c$ be a checkpoint version and $v$ the target version;
- $L(c,v)$ be log actions replayed after checkpoint $c$;
- $\Delta F^+$ and $\Delta F^-$ be files added and removed by a logical change.

The central safety property is $C(q)\subseteq P(q)$. The useful precision ratio is $|C(q)|/|P(q)|$ when candidates are known and nonempty, but production systems often cannot know $C(q)$ without reading data. Use scanned/matched rows or controlled fixtures as empirical approximations and label them accordingly.

Do not compare amplification across unlike scopes. Metadata bytes per selected content byte becomes undefined or misleading for a query selecting zero content. Report raw metadata bytes/objects and a defined zero-result convention. Distinguish metadata stored, metadata reachable, metadata fetched, metadata decoded, and metadata retained in cache.

## Mechanisms, Invariants, or Proof Structure

### Sound-pruning argument

Assume every leaf test is inclusive and every internal summary satisfies:

$$\exists f\in D(u):M(f,q)\Rightarrow \operatorname{may\_match}(S(u),q).$$

Traversal begins at $R_s$. It descends through every node whose summary may match and evaluates every retained leaf entry inclusively. Consider any $f\in C(q)$. Every ancestor of $f$ has a matching descendant—namely $f$—so the implication requires each ancestor to be retained. The leaf test also retains $f$. Therefore $f\in P(q)$, and $C(q)\subseteq P(q)$. A false negative requires a violated summary/test contract, wrong interpretation identity, unreadable node treated as empty, or traversal bug.

### Snapshot-consistency argument

A reader resolves $R_s$ once, verifies the snapshot/version, and traverses only immutable descendants reachable from it. Concurrent snapshot $s+1$ may reuse or add nodes but cannot mutate $G_s$. Therefore the reader's graph and $F_s$ remain stable for its planning interval, subject to retention preserving objects. A mutable child, path collision, premature deletion, or cache key that omits identity breaks the premise.

### Rewrite-equivalence obligation

Let old graph $G$ and replacement graph $G'$ represent snapshot semantics $Q(G)$ and $Q(G')$, including live files, delete applicability, schema/spec bindings, sequence/provenance, and required metrics semantics. A metadata-only rewrite is correct only if

$$Q(G')=Q(G).$$

Compare canonical keyed entries, not only counts or aggregate bytes. Validate duplicates, omissions, entry state, IDs, metrics, and integrity. Publish $G'$ as a new snapshot/root transition; keep $G$ reachable for retained readers.

### Checkpoint-replay obligation

Let state application be deterministic function $\operatorname{apply}$. A checkpoint at $c$ is valid for target $v$ when

$$\operatorname{apply}(S_c,L(c,v))=\operatorname{apply}(S_0,L(0,v)).$$

Test this over production-derived histories, including aborts, protocol changes, deletes, retries, and maintenance. If the newest checkpoint is corrupt or incomplete, discovery must not hide the older valid recovery path.

### Failure-injection matrix

Inject truncation, checksum mismatch, missing internal node, duplicate entry, conflicting entry state, wrong schema/spec ID, unsupported feature, stale root cache, stale leaf cache, timeout, throttling, partial checkpoint, maintenance crash, concurrent commit, and premature cleanup. Expected behavior is either a correct conservative plan, a verified fallback, or an explicit failure—never silent exclusion.

## Alternatives and Trade-Offs

**Flat snapshot metadata** is simple and can scan sequentially, but has high rewrite and selective-planning cost at large $n$. It suits small tables or compact checkpoint parts, not unlimited growth.

**Hierarchical manifests** support pruning, structural sharing, and parallel fetch. They add formats, summary correctness, fanout policy, and maintenance. Two levels are often enough; deeper trees help extreme scale but raise traversal and implementation complexity.

**Ordered logs with checkpoints** make commits append-oriented and history explicit. Cold reads pay replay, gap discovery, and checkpoint validation. Checkpoint cadence becomes an operational control.

**Embedded column metrics** avoid separate index coordination and travel with entries. They enlarge metadata and may expose sensitive values. External indexes can be richer but require snapshot binding and failure semantics.

**Range summaries** are compact and effective for clustered data, but weak for scattered values and sensitive to ordering semantics. **Bloom filters or sketches** improve membership/selectivity estimates at added bytes, CPU, versioning, and false-positive complexity; they must not introduce false negatives.

**Large nodes** reduce requests and often improve sequential throughput. They increase decode latency, coordinator memory, cache admission cost, rewrite amplification, and tail impact. **Small nodes** improve parallelism and update locality but increase requests, headers, listings, and fragmentation.

**Foreground merging** keeps metadata tidy but lengthens commits and expands conflicts. **Asynchronous rewriting** isolates user writes but accepts temporary fragmentation and needs safe concurrency, budgets, and observability.

**Path-keyed caches** are easy but unsafe if paths are mutable. **Content-addressed or version-qualified caches** are robust but need identity/checksum plumbing. Shared caches save bandwidth while increasing tenant isolation and eviction-policy concerns.

## Failure Modes and Misconceptions

1. **“The metadata is only an optimization.”** Once pruning or delete applicability uses it, incorrect metadata changes results.
2. **False negatives in summaries.** Partial scans, wrong type decoding, truncated-bound misuse, or NaN/null errors exclude valid files.
3. **Unknown means empty.** Missing statistics are interpreted as no values rather than cannot decide.
4. **Identity by name.** Renamed or reordered fields bind old metrics to the wrong current column.
5. **Mixed partition semantics.** Ranges from different transforms/specifications are compared without their IDs.
6. **Duplicate live entries.** One file appears multiple times, causing duplicate rows or undefined delete behavior.
7. **Tiny-manifest explosion.** Low bytes conceal high request, decode, and object-management cost.
8. **Monolithic manifest growth.** One node dominates latency and memory and is rewritten for small changes.
9. **Unbounded replay.** A missing, stale, or perpetually deferred checkpoint turns every cold read into full history reconstruction.
10. **Partial checkpoint discovery.** Readers select a checkpoint before every part is durable and verified.
11. **Count-only rewrite validation.** Equal file counts conceal omissions and substitutions.
12. **Sequence loss.** Rewriting entries resets age/provenance and changes which deletes apply.
13. **Mutable-node caching.** A path is reused for different bytes and readers combine snapshots.
14. **Cache stampede.** Parallel coordinators simultaneously fetch and decode the same cold graph.
15. **Premature metadata deletion.** Old roots or shared nodes disappear while retained snapshots still reference them.
16. **Silent feature downgrade.** An older reader ignores required semantics and produces plausible wrong results.
17. **Statistics leakage.** Bounds reveal identifiers or sensitive categories outside intended data authorization.
18. **Coordinator-only tuning.** More heap masks metadata growth while increasing pause and blast radius.
19. **Universal target size.** One manifest-size constant is copied across workloads with different latency, bandwidth, commit, and selectivity profiles.
20. **Repair by mutation.** Historical metadata is edited in place, destroying reproducibility and cache safety.

## Worked Examples

### Example 1

A snapshot has 2,000 manifests. The manifest list's partition summaries retain 18 for a seven-day query. File-level summaries within those manifests retain 640 of 18,000 entries. Report both pruning stages: `2000 -> 18 manifests` and `18000 -> 640 files`. Reporting only 640/total-table files hides whether upper-level pruning worked.

### Example 2

An internal node summarizes descendants with integer bounds `[10, 90]`. One child actually contains value 104 because the summary was computed before the last child was added. Predicate `x = 104` rejects the node and loses a row. Immutability alone does not help: the immutable summary is wrong. Rebuild the node and publish a corrected snapshot; do not edit it in place.

### Example 3

A schema renames field ID 17 from `customer` to `account`. Old manifests store bounds for ID 17. A reader binding by field ID can still prune correctly; one binding by display name may ignore the bounds or, worse, attach another field's bounds after name reuse. Stable identity is a correctness mechanism.

### Example 4

One thousand streaming commits each add a 20 KiB manifest. Total metadata is only about 20 MiB, but a cold plan makes roughly 1,000 requests. A rewrite combines compatible entries into 20 manifests near 1 MiB. Logical file membership is unchanged, while request count falls sharply. The actual target is chosen from measured latency, memory, and commit patterns.

### Example 5

A table has $n=1,000,000$ leaf groups and ideal fanout $b=100$. The idealized height is $\lceil\log_{100}(1,000,000)\rceil=3$. This does not promise three object requests: a query may retain many nodes per level and fetch them in parallel or serially. The calculation describes depth, not total work.

### Example 6

A Delta-style log has a valid checkpoint at version 4,000 and target version 4,083. The reader loads the checkpoint and replays 83 commits. If the checkpoint manifest references a missing part, the reader must fail or fall back according to protocol; treating the part as empty would silently omit live actions.

### Example 7

A metadata rewrite reads 450,000 live entries and writes 120 replacement manifests. It verifies keyed equality of path, content kind, partition, schema/spec, sequence, metrics, and delete semantics. Another append commits during the rewrite. The maintenance transaction validates whether it can reuse the append's new manifest and replace only the unchanged old set; it does not blindly overwrite the new head.

### Example 8

A query selects no content files. It reads 3 MiB of metadata. The ratio `metadata bytes / selected data bytes` is undefined, not infinite proof of bad design. Report `metadata_bytes=3 MiB`, `candidate_files=0`, node counts, and latency; compare zero-result queries as their own cohort.

### Example 9

A cache keyed only by `metadata/current.json` stores root 51. The path is overwritten with root 52, while one coordinator retains cached bytes. That reader is consistently stale, but a second bug caches child paths without version validation and can mix states. Immutable unique object names plus a validated mutable reference eliminate the ambiguous child cache.

### Example 10

The executable fixture performs two-level inclusive pruning and preserves an unknown summary.

<!-- bijux-verify: {"id":"metadata-tree-pruning","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"manifests_considered=3\nmanifests_retained=2\nfiles_considered=3\nfiles_retained=f2.parquet,f3.parquet\nunknown_manifest_retained=yes\n","stderr":""}} -->
```python
query_low, query_high = 17, 19
manifests = [
    {"name": "m1", "bounds": (0, 9), "files": [("f1.parquet", 1, 8)]},
    {"name": "m2", "bounds": (10, 29), "files": [("f2.parquet", 10, 18), ("f3.parquet", 19, 22)]},
    {"name": "m3", "bounds": None, "files": [("f4.parquet", 80, 90)]},
]

def overlaps(bounds):
    if bounds is None:
        return True
    low, high = bounds
    return not (high < query_low or low > query_high)

retained_manifests = [m for m in manifests if overlaps(m["bounds"])]
retained_files = [
    name
    for manifest in retained_manifests
    for name, low, high in manifest["files"]
    if overlaps((low, high))
]

print(f"manifests_considered={len(manifests)}")
print(f"manifests_retained={len(retained_manifests)}")
print(f"files_considered={sum(len(m['files']) for m in retained_manifests)}")
print(f"files_retained={','.join(retained_files)}")
print(f"unknown_manifest_retained={'yes' if any(m['bounds'] is None for m in retained_manifests) else 'no'}")
```

## Cross-Program Connections

- **Data structures:** persistent trees, copy-on-write DAGs, Bloom filters, interval indexes, cache replacement, and amortized compaction provide the underlying models.
- **Database systems:** B-trees, LSM trees, MVCC, write-ahead logs, checkpoints, statistics, and cost-based planning supply close analogies, though object-store constraints differ.
- **Distributed systems:** immutable naming, conditional publication, idempotency, fault injection, partial failure, and reachability-based garbage collection govern correctness.
- **Storage engineering:** request latency, range reads, compression, checksums, encryption, consistency, and lifecycle policy determine physical cost.
- **Query engines:** predicate projection, split generation, coordinator memory, parallel fetch, dynamic filters, and plan caching consume the metadata graph.
- **Schema engineering:** stable field IDs, type promotion, partition evolution, protocol features, and backward compatibility determine whether old nodes remain interpretable.
- **Platform engineering:** catalogs, caches, credentials, service limits, observability, repair tooling, and maintenance scheduling turn the format into a reliable service.
- **Security and governance:** file paths, statistics, retention, audit lineage, legal holds, tenant isolation, and key references make metadata a governed asset.
- **Reliability engineering:** SLOs for planning, corruption detection, recovery drills, fallbacks, and bounded maintenance validate operational behavior.

## References

1. Apache Iceberg, [Table Format Specification](https://iceberg.apache.org/spec/). Current. Defines manifests, manifest lists, snapshots, sequence numbers, partition summaries, scan planning, and metadata fields.
2. Apache Iceberg, [Terms](https://iceberg.apache.org/terms/). Current. Provides concise definitions of manifest lists, manifests, data files, and partition specifications.
3. Apache Iceberg, [Spark Queries: Metadata Tables](https://iceberg.apache.org/docs/latest/spark-queries/). Current. Documents observable manifest and partition-summary metadata.
4. Apache Iceberg, [Maintenance](https://iceberg.apache.org/docs/latest/maintenance/). Current. Covers snapshot expiration, orphan removal, and manifest rewriting.
5. Delta Lake, [Transaction Log Protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md). Current. Defines log actions, checkpoints, protocol features, and table state reconstruction.
6. Delta Lake, [Delta Kernel](https://docs.delta.io/delta-kernel/). Current. Documents transaction commits and checkpoint creation for connectors.
7. Delta Kernel, [Distributed Log Replay](https://docs.delta.io/kernel/rust/reading/parallel_scan_metadata.html). Current. Describes sequential commit replay and parallel processing of checkpoint parts.
8. Delta Lake, [Table Batch Reads and Writes](https://docs.delta.io/delta-batch/). Current. Covers time travel and log/checkpoint retention behavior.
9. Apache Hudi, [Metadata](https://hudi.apache.org/docs/metadata/). Current. Describes scalable metadata and file-listing support.
10. Apache Hudi, [Timeline](https://hudi.apache.org/docs/next/timeline/). Current. Describes timeline instants and table-state actions.
11. Apache Paimon, [Manifest](https://paimon.apache.org/docs/master/concepts/spec/manifest/). Current. Describes snapshot, manifest list, manifest file, and data-file hierarchy.
12. Apache Parquet, [Page Index](https://parquet.apache.org/docs/file-format/pageindex/). Current. Defines column and offset indexes used for lower-level pruning.
13. Apache Avro, [Specification](https://avro.apache.org/docs/current/specification/). Current. Defines the container and schema-evolution foundation used by some metadata files.

## Exercises

### Exercise 1

A node has descendants with integer ranges `[2,8]`, `[14,20]`, and one unknown range. What conservative parent range and unknown marker should it publish? Can predicate `x=100` prune the node?

### Exercise 2

A table has 1,000,000 entries. With ideal fanout 100, compute the idealized height. Explain why this number is not the request count for a range query.

### Exercise 3

A snapshot's manifest list retains 12 of 600 manifests. Those 12 contain 24,000 entries, of which 300 survive file pruning. Compute retention percentages at both levels and state what cannot be inferred.

### Exercise 4

Design an equivalence key and comparison for a metadata-only rewrite. Include at least six facts beyond file count and explain how concurrent commits affect publication.

### Exercise 5

A checkpoint at version 9,000 is followed by 700 commits, and cold planning replay is now slow. Propose an evidence-driven checkpoint policy and a failure test for multi-part checkpoint discovery.

## Answers to the Exercises

### Answer 1

Known lower/upper bounds combine to `[2,20]`, but the parent must also record that a descendant bound is unknown. Predicate `x=100` cannot safely prune the node because the unknown child could contain 100. A format may omit the combined bound entirely or retain it with an explicit unknown/containment flag; either representation must cause inclusive traversal.

### Answer 2

$\lceil\log_{100}(1,000,000)\rceil=3$ because $100^3=1,000,000$. A query can retain multiple children at each level, fetch nodes in parallel, hit or miss caches, and read checkpoint/log objects outside the ideal tree. Height bounds dependency depth in the ideal model; it does not equal objects read or network round trips.

### Answer 3

Manifest retention is $12/600=2\%$. File retention within retained manifests is $300/24,000=1.25\%$. The figures do not reveal true row selectivity, files outside the retained manifests, metadata bytes, request latency, cache effects, data bytes, or whether retained files actually contain matching rows. They also cannot prove soundness; a controlled completeness check is needed.

### Answer 4

Key entries by immutable file identity/path plus content kind. Compare live state, partition tuple and spec ID, schema binding, byte size, row count, data/file sequence or commit provenance, delete applicability, column metrics with unknown semantics, encryption/integrity fields, and required feature flags. Canonical sets must be equal and duplicate-free. Publish the replacement against its base snapshot; if the head moves, revalidate or incorporate compatible new nodes rather than discarding concurrent work.

### Answer 5

Measure replay actions, bytes, decode CPU, wall time, reader frequency, commit rate, checkpoint creation cost, object count, and tail latency. Trigger from a bounded replay budget or age with hysteresis, then verify fleet outcomes; `700` alone is not a universal threshold. Write checkpoint parts under unique immutable names, verify their counts/checksums, then make the checkpoint discoverable. Inject a missing or corrupt part before discovery and after discovery. Readers must ignore an unpublished checkpoint and must explicitly fail or use a protocol-defined earlier checkpoint plus log replay when a published checkpoint is unusable; they must never treat a missing part as empty.
