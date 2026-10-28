---
module_id: DBE-092
program: Database Engineering
level: 2
module_number: 92
title: LSM-Based Key-Value Stores
status: complete
last_verified: 2026-09-05
---

# LSM-Based Key-Value Stores

## One-Page Review

### Governing question

How does a log-structured merge-tree turn random updates into sequential, immutable writes while preserving correct point lookup, range scan, deletion, crash recovery, and bounded operational debt?

### Essential definitions

- A **log-structured merge-tree (LSM-tree)** stores recent changes in memory and periodically merges immutable sorted runs across storage levels.
- A **write-ahead log (WAL)** durably records an accepted mutation before the mutable in-memory table is acknowledged.
- A **memtable** is the mutable ordered in-memory component; an **immutable memtable** is frozen for flushing.
- An **SSTable** is an immutable sorted-string table containing keyed versions over a bounded key range.
- **Compaction** reads selected runs and writes replacement runs, reconciling versions and tombstones under snapshot-retention rules.
- A **tombstone** is a versioned deletion marker. It cannot be discarded merely because no value is visible in the current run.
- **Leveled compaction** keeps limited overlap in most levels; **tiered** or **size-tiered compaction** allows several similarly sized overlapping runs before merging them.
- **Read amplification**, **write amplification**, and **space amplification** count extra physical work or bytes relative to the logical operation or live dataset.
- A **Bloom filter** can prove that a key is absent from a run with no false negatives under correct construction, while positive results remain probabilistic.
- **Compaction debt** is pending merge work whose growth threatens read cost, free space, and future write admission.

### Central model, mechanism, or theorem

An accepted update is appended to the WAL and inserted into a memtable. A full memtable freezes, flushes as a new immutable sorted run, and becomes readable before its WAL segment is retired. Reads search components from newest to oldest, using sequence numbers, range metadata, indexes, filters, and caches to avoid irrelevant work. Compaction atomically installs new runs before obsolete inputs are reclaimed.

For logical key $k$ at snapshot sequence $s$, visibility selects the greatest sequence $q \le s$ among versions of $k$. A selected tombstone means absent. This newest-visible-version rule must hold across memtables, runs, caches, compactions, restarts, and replicas.

### Critical invariants

- acknowledged mutations survive every modeled crash covered by the durability contract;
- every readable version has one stable ordering identity, not merely a wall-clock timestamp;
- lookup considers every component that may contain a newer visible version;
- compaction preserves the result for every retained snapshot before removing inputs;
- Bloom filters and range metadata may create false-positive work but never false-negative omission;
- tombstones remain until no retained snapshot or unreconciled older run can reveal deleted data;
- manifest publication makes either the old file set or the new file set authoritative after recovery;
- compaction throughput eventually exceeds flush demand, with explicit headroom for repair and peaks.

### Common failures

- calling a WAL-backed memtable durable without testing WAL sync and recovery;
- treating append throughput as sustainable throughput while compaction debt grows;
- dropping tombstones by age and resurrecting older values;
- sizing only the live dataset and running out of space during overlapping compaction;
- applying a Bloom filter to the wrong key representation or snapshot rule;
- assuming every LSM has the same amplification because implementation and workload dominate;
- using client time as version order under clock skew;
- benchmarking uniform point operations while production uses ranges, skew, large values, snapshots, and deletes.

### Compact example

Runs contain `a@7=3`, `b@8=DEL`, and older `a@2=1`, `b@3=2`, `c@4=4`. At snapshot 8, the greatest eligible version makes `a` equal 3, hides `b`, and leaves `c` equal 4. A compaction may emit `a@7=3`, `b@8=DEL`, `c@4=4`; it may drop the tombstone only after proving that no older `b` can reappear and no retained snapshot needs it.

### Connections

Prerequisites include [B+ Tree Structure](031-b-tree-structure.md), [Index Maintenance and Write Amplification](039-index-maintenance-and-write-amplification.md), [ACID and Transaction Boundaries](041-acid-and-transaction-boundaries.md), [Multi-Version Concurrency Control](046-multi-version-concurrency-control.md), and [Crash Recovery](078-crash-recovery.md). The roadmap's next module, [Document Databases](../ROADMAP.md), separates a logical document model from the storage engines that may implement it. [Operating Systems](../../22-operating-systems/ROADMAP.md) owns filesystem, page-cache, I/O, and crash primitives; [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns general probabilistic and ordered structures.

## Governing Question

An update-heavy key-value store wants high ingest throughput, durable acknowledgement, point reads, ordered scans, deletion, snapshots, and predictable tails. Overwriting a page in place can turn scattered keys into scattered I/O. Appending every mutation is fast, but an unbounded log makes reads and recovery progressively worse. How can a storage engine defer and batch reorganization without losing truth about which version is visible?

The answer is not “writes are sequential.” An LSM-based engine is a lifecycle of durable logging, ordered memory, immutable files, lookup routing, version reconciliation, compaction scheduling, snapshot retention, and safe garbage collection. Its performance is the interaction of workload, layout, cache, storage, and background capacity. This module develops that lifecycle and the evidence needed to operate it.

## Why This Matters

LSM-family designs underlie many embedded and distributed databases because they transform foreground random mutation into sequential append and batched rewriting. That can improve write throughput and exploit modern storage well. It also transfers work into background compaction, increases the number of places a read may consult, and makes deletion a temporal proof rather than immediate erasure.

Production incidents often appear far from the original write: level-zero files overlap until reads fan out; snapshots pin obsolete bytes; tombstones expand; compaction consumes bandwidth needed by foreground reads; a full disk prevents the rewrite needed to reclaim space; or recovery replays a WAL whose corresponding table was already installed. Correctness and operability therefore share the same mechanisms.

The LSM-tree paper provides the foundational cost argument. Real engines add sequence numbers, block indexes, Bloom filters, caches, manifests, rate limiting, checksums, column families, value separation, and distributed ownership. Those are not decorative optimizations. Each changes assumptions, failure modes, and evidence.

## Prerequisites and Retrieval

Retrieve the difference between logical and physical writes, immutable and mutable state, ordered search, probabilistic membership, WAL durability, checksums, atomic rename or manifest publication, MVCC visibility, and snapshot retention. Be able to explain why a successful process write is not necessarily stable storage, why a false-negative filter is unsafe, and why removing a version can change an older snapshot.

From earlier database modules, retrieve B+ tree search and update paths, index maintenance, transaction boundaries, version visibility, logging, checkpointing, and crash recovery. LSM does not replace those concerns; it chooses a different physical organization and recovery boundary.

State the environment before evaluating an engine: exact version and configuration; key and value sizes; compression and checksum settings; memtable and block sizes; compaction style; level targets and fanout; filter policy; cache budget; filesystem and device; sync mode; concurrency; snapshot/TTL/delete behavior; dataset and free-space limits; and workload distribution. Product defaults change, so current claims require current official documentation.

## Learning Objectives

After completing this module, you should be able to:

1. derive the end-to-end mutation, flush, lookup, compaction, and recovery paths of an LSM engine;
2. state visibility, filter, manifest, and tombstone invariants precisely;
3. reason about read, write, and space amplification without presenting simplified models as universal measurements;
4. compare leveled, tiered, hybrid, and key-value-separated designs from workload evidence;
5. diagnose write stalls, level-zero overlap, tombstone debt, cache pressure, and pinned obsolete files;
6. design crash, corruption, snapshot, deletion, and full-disk tests with explicit oracles;
7. distinguish embedded storage-engine guarantees from distributed database guarantees;
8. make an auditable production choice with capacity headroom and recovery evidence.

## Core Exposition

**Begin with the logical contract.** A key-value operation may be unconditional `put`, conditional update, delete, merge, point get, range scan, or snapshot read. Define whether a write is durable when acknowledged, whether reads are linearizable or snapshot-based, how concurrent versions order, whether range scans are consistent, and whether deletion has a retention deadline. The storage engine cannot infer the application invariant from bytes.

Let an internal entry be $(k,q,t,v)$: user key $k$, sequence $q$, type $t$ such as value or tombstone, and optional value $v$. Internal ordering commonly sorts by user key and then by descending sequence. For snapshot $s$, a read selects the first version with matching $k$ and $q \le s$. The ordering identity must be stable and assigned by the write protocol. A client wall clock is not a safe substitute.

**Separate WAL and memtable roles.** The WAL is a recovery record; the memtable is an efficient current index. A mutation generally enters the WAL and memtable under an ordering and acknowledgement protocol. If the engine promises durable acknowledgement, the required WAL bytes and ordering metadata must reach the promised persistence domain before success is returned.

Group commit can amortize sync cost across mutations while adding queue delay. Disabling sync changes the durability contract. A battery-backed controller, device cache, filesystem, virtual disk, and cloud volume each affect what “persisted” means. Test the actual stack with abrupt termination and power-loss-equivalent mechanisms where safe.

**Freeze before flush.** When a memtable reaches a threshold, the engine makes it immutable and installs a new mutable memtable. Reads consult both. A background flush sorts or preserves sorted order, writes blocks, indexes, filters, checksums, and footer metadata, syncs as required, then atomically adds the SSTable to the current version. Only after the installed table covers the logged mutations can corresponding WAL retention advance.

Several immutable memtables can accumulate if flush cannot keep up. Eventually the engine slows or stalls writers to prevent unbounded memory and level-zero growth. This is backpressure preserving bounded resources, not necessarily a bug. The operational question is why arrival exceeds sustainable flush and compaction service.

**Treat SSTables as immutable evidence.** An SSTable groups sorted internal entries into data blocks and carries metadata such as smallest/largest keys, block handles, checksums, compression, and perhaps filters. Immutability permits concurrent readers, caching, simple publication, and sequential construction. It does not make files indestructible: truncated writes, corrupt blocks, lost metadata, wrong comparators, and missing files require detection and recovery policy.

A point lookup searches newest plausible components first. Range bounds exclude runs that cannot contain $k$; an index locates candidate blocks; a Bloom filter can reject definite absence; cache may avoid I/O. A positive filter result only means “possibly present.” Once versions are found, sequence and snapshot rules determine the answer. Searching merely until any value appears is wrong if a newer tombstone or value exists elsewhere.

**Understand level zero.** Flushes commonly enter level zero, where files can overlap arbitrarily because each represents a time interval of writes. A point read may probe many overlapping level-zero files. Later leveled tiers restrict overlap, often to at most one file per level for a point key, though exact implementations differ. Level-zero file count and bytes are early indicators of compaction debt and tail-read risk.

**Compaction is semantic reconciliation.** A compaction selects input runs, performs an ordered merge, applies version and deletion retention rules, creates replacement files, verifies them, and publishes a new manifest/version. Old files remain available to readers holding the previous version until references drain. Publication and reclamation are separate.

For each key, the merge sees versions in internal order. It may discard overwritten versions only if no retained snapshot can observe them. It may discard a tombstone only if no older value outside the compaction can later become visible and replication, backup, change-data, TTL, or legal-retention obligations permit it. “Older than seven days” is not a proof by itself.

**Make publication crash-safe.** Construct output under a non-authoritative identity, finish contents and checksums, persist according to the contract, record an atomic manifest/version edit, and only then retire inputs. Recovery must select a complete authoritative version, ignore or clean orphan candidates, and never combine an unpublished output with missing inputs. Exact filesystem and manifest semantics are implementation-dependent and must be tested.

**Compare compaction families.** Leveled compaction partitions most levels into non-overlapping key ranges. It usually bounds point-read fanout and space overhead but may rewrite an item repeatedly as overlapping lower-level data enters. Tiered or size-tiered compaction accumulates multiple similarly sized runs and merges them together. It often lowers rewrite work for heavy ingest but raises read and temporary-space amplification. Universal compaction is a product implementation of run-based policies with its own selection rules; it is not a synonym for every tiered algorithm.

Hybrid policies can tier the newest data and level older data, treat hot and cold ranges differently, or use time windows for expiring series. The labels do not predict results without fanout, run count, overlap, selection, compression, tombstone, snapshot, and workload details.

**Use amplification as accounting, not branding.** Define logical user bytes $U$, physical bytes written $P_w$, physical bytes read $P_r$, and live logical bytes $D$. A measured write amplification can be $WA=P_w/U$ over a named interval and boundary. Read amplification may count device reads, blocks, files, bytes, or CPU probes; state which. Space amplification may be physical retained bytes divided by live logical bytes, again naming WAL, snapshots, replicas, indexes, and temporary compaction files.

A simplified size-ratio model uses memtable capacity $M$, database size $N$, and level size ratio $T>1$. The number of disk levels is approximately $L=\lceil\log_T(N/M)\rceil$ when assumptions about full levels and uniform distribution hold. This estimates shape, not exact amplification. Skew, compression, overwrite rate, file boundaries, compaction picker, snapshots, and device behavior can dominate.

**Bloom filters trade memory for avoided negative probes.** For $n$ inserted keys, $m$ bits, and $h$ independent hash locations, the classical false-positive approximation is $p\approx(1-e^{-hn/m})^h$. The minimizing real-valued choice is near $h=(m/n)\ln 2$. For 10 bits per key, $h\approx6.93$ and the idealized $p$ is about 0.0082. Hash dependence, blocked filters, prefixes, caching, and implementation overhead change observed behavior.

The safety property is one-sided: a key that was inserted into the filter domain must never be rejected as absent. Comparator, prefix extractor, timestamp suffix, and format-version changes can violate that premise. Filters help missing point lookups most; large range scans usually cannot skip every relevant block with a whole-key filter.

**Design indexes and blocks together.** Fence pointers map key ranges to blocks. Smaller blocks reduce irrelevant bytes for point reads but increase index/filter metadata and I/O operations. Larger blocks favor scans and compression but amplify small lookups. Restart points or prefix compression reduce key storage while requiring bounded reconstruction. Checksums should cover the representation actually read, with clear behavior for corruption.

**Cache the right layer.** A block cache stores decompressed or compressed blocks depending on design; the operating-system page cache may duplicate bytes; indexes and filters compete with data. A row cache can accelerate hot keys but risks stale or snapshot-incompatible answers unless keyed by version semantics. Partition cache budgets and observe hit rates by component and workload, not one aggregate percentage.

**Large values alter the equation.** If values dwarf keys, compaction repeatedly rewrites cold value bytes. Key-value separation stores sorted keys and value references in the LSM while appending values elsewhere. WiscKey demonstrated this design point for SSDs. It can reduce LSM write amplification but adds value-log garbage collection, indirection, range-scan costs, crash ordering, and dangling-reference risks. There is no free elimination of rewriting.

**Snapshots turn garbage into live history.** A long-running snapshot can require old versions and old files. Compaction may still reorganize data but cannot reclaim needed history. Track oldest snapshot sequence and age, pinned bytes, retained versions, and responsible clients. Bound or cancel pathological snapshots only under an explicit API contract.

**TTL and delete are different clocks.** TTL may be evaluated at read, compaction, or both. Expired data may remain physically present until compaction. A tombstone may need propagation across all older runs before removal. If a replica restores an old SSTable after tombstone garbage collection, deleted data can resurrect. Align tombstone grace with repair, backup, restore, and maximum disconnection assumptions rather than a convenient duration.

**Range scans expose layout choices.** A range iterator merges candidate runs while suppressing shadowed versions and tombstones. Its cost depends on overlap, run count, block locality, cache, readahead, and result width. Bloom filters optimized for exact keys do not transform a many-run merge into one sequential read. Benchmark point and range workloads separately and together.

**Compaction scheduling is resource governance.** Compaction consumes read bandwidth, write bandwidth, CPU, cache, file descriptors, and temporary space. Too little capacity grows debt; too much foreground competition increases tails. Rate limits, priorities, subcompactions, and admission control must coordinate with flush, repair, backup, bulk ingest, and query service.

Let logical flush arrival be $a$ bytes/s and average downstream physical compaction work per flushed byte be $w$. Required steady compaction service is at least $aw$ bytes/s under the same accounting boundary. Equality provides no recovery headroom. If debt is $B$ bytes and spare service above current arrival work is $c-aw>0$, ideal drain time is at least $B/(c-aw)$; real time is longer under contention and changing amplification.

**Recognize write stalls as an invariant boundary.** Common triggers include too many immutable memtables, too many level-zero files, a level far beyond target, pending compaction bytes, insufficient free space, or rate-limited background work. Record stall reason and duration. Raising thresholds can postpone but enlarge the eventual problem. Repair sustainable service, workload shape, or capacity.

**Bulk load deliberately.** Sorting data externally and ingesting validated SSTables can bypass ordinary write paths. It must still honor comparator, internal-key format, sequence/snapshot rules, checksums, range overlap, encryption, manifest publication, and replication. A malformed “compatible” file can corrupt semantics more efficiently than individual writes.

**Keep distributed guarantees separate.** An embedded LSM engine may provide atomic batches, snapshots, WAL recovery, and file checksums on one node. A distributed database must additionally own routing, replication, consensus or conflict resolution, membership, shard movement, cross-shard transactions, repair, and backup. Replicated WALs do not automatically make compaction choices globally safe; each replica must preserve logical history and validate repaired state.

**Observe causal chains.** Collect logical write rate and bytes; WAL sync latency; mutable/immutable memtable count; flush rate and duration; files and bytes per level; overlap; pending compaction bytes; compaction input/output/read/write bytes; stall reason and duration; Bloom usefulness and false-positive observations; cache by class; read blocks/files/bytes; tombstones; oldest snapshot; obsolete pinned bytes; free and temporary space; device latency; CPU; errors; and recovery results.

Correlate metrics by time, column family or tenant, level, shard, operation, and deployment. A high compaction rate may mean healthy service or emergency catch-up. Low write amplification may coexist with unacceptable read amplification. Averages can hide one hot range repeatedly rewritten.

**Validate with stateful oracles.** Maintain a simple reference map with sequence-aware snapshots. Generate puts, deletes, merges, batches, and scans; compare every visible result. Inject crashes before and after WAL sync, flush completion, file sync, and manifest publication. Corrupt blocks and manifests; fill storage; hold snapshots; stop compaction; skew keys; restart repeatedly; and restore backups older than tombstone retention.

Verify durable acknowledged operations after recovery, no unacknowledged operation beyond the stated allowance, sorted unique visible scans, snapshot stability, delete non-resurrection, checksum detection, bounded resource behavior, and eventual debt drainage. A passed finite campaign is evidence for tested histories and environment, not a proof of all executions.

The executable fixture models only newest-visible-version selection across finite sorted runs. It is not a WAL, SSTable parser, Bloom filter, compaction engine, snapshot implementation, crash test, distributed store, or performance benchmark.

<!-- bijux-verify: {"id":"finite-lsm-merge","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"visible_a=3\nvisible_b=deleted\nvisible_c=4\nrange_keys=a,c\nnewest_sequence_wins=true\ntombstone_prevents_resurrection=true\nsorted_output=true\nevidence=finite_lsm_merge\n","stderr":""}} -->
```python
runs = [
    [("a", 7, 3), ("b", 8, None)],
    [("a", 2, 1), ("b", 3, 2), ("c", 4, 4)],
]
snapshot = 8

versions = {}
for run in runs:
    for key, sequence, value in run:
        if sequence <= snapshot:
            versions.setdefault(key, []).append((sequence, value))

visible = {}
for key, candidates in versions.items():
    sequence, value = max(candidates)
    visible[key] = value

keys = sorted(key for key, value in visible.items() if value is not None)
print(f"visible_a={visible['a']}")
print("visible_b=deleted" if visible["b"] is None else f"visible_b={visible['b']}")
print(f"visible_c={visible['c']}")
print(f"range_keys={','.join(keys)}")
print(f"newest_sequence_wins={str(visible['a'] == 3).lower()}")
print(f"tombstone_prevents_resurrection={str(visible['b'] is None).lower()}")
print(f"sorted_output={str(keys == sorted(keys)).lower()}")
print("evidence=finite_lsm_merge")
```

## Definitions and Notation

- $k$ is a user key; $v$ is a value; $q$ is a monotonically ordered sequence identity; $s$ is a snapshot sequence.
- $M$ is effective mutable-memory capacity, $N$ is live logical database size, $T>1$ is an illustrative level size ratio, and $L$ is an approximate count of disk levels.
- A **component** is a memtable or immutable sorted run participating in lookup.
- A **run** is a sorted immutable sequence of internal entries. An SSTable may hold one run or a partition of one, depending on terminology.
- A **level** is a policy-managed collection of files or runs with size and overlap rules.
- A **version** or **manifest state** identifies the authoritative set of files and their metadata.
- A **flush** converts an immutable memtable into durable table files and publishes them.
- A **compaction picker** selects input files/runs and output range or level according to policy.
- A **sequence number** orders mutations for visibility; it does not necessarily equal transaction commit time across arbitrary systems.
- A **snapshot** fixes a visibility boundary such as sequence $s$.
- A **tombstone** is a deletion version; **garbage collection** is physical reclamation after proof that state is unobservable and unneeded.
- $U$ is logical user bytes, $P_w$ physical written bytes, $P_r$ physical read bytes, $D$ live logical bytes, and $B$ pending compaction debt under explicitly named boundaries.
- $m$ is Bloom-filter bits, $n$ inserted keys, $h$ hash locations, and $p$ the idealized false-positive probability.
- **Level zero (L0)** is the initial on-disk collection whose files commonly overlap in user-key space.
- **Write stall** is delayed or rejected foreground admission caused by resource or maintenance limits.
- **Key-value separation** keeps key/index metadata in the LSM and values in a separately reclaimed log.

## Mechanisms, Invariants, or Proof Structure

**Visibility argument.** Assume every accepted mutation has a unique ordered sequence, every lookup enumerates every component that can contain key $k$, and component pruning has no false negatives. Filtering candidates to $q\le s$ and taking the greatest $q$ therefore returns the latest mutation visible at snapshot $s$. If its type is tombstone, absence is the logical result. The argument fails if a component is omitted, sequence order is inconsistent, or a cache ignores snapshot identity.

**Compaction preservation obligation.** Let input file set $I$ be replaced by output set $O$. For every retained snapshot $s$ and key in the affected ranges, querying with $O$ plus unaffected files must equal querying with $I$ plus unaffected files. Sorting and merging alone do not prove this: version dropping, tombstone dropping, merge operands, TTL, range deletions, and external value references each add premises.

**Crash-publication argument.** Before manifest publication, all authoritative inputs remain referenced, so incomplete outputs can be ignored. After durable publication, complete verified outputs are referenced and inputs remain physically present until no reader/version needs them. Recovery chooses a durable manifest state and replays WAL records not covered by installed tables. This depends on actual ordering and persistence primitives; atomic filename change alone does not prove directory entries or file data are durable.

**Bloom safety.** Under the premise that the same normalized key and hash/filter definition are used for construction and lookup, every inserted key sets all tested bits. A zero tested bit therefore proves absence from that filter domain. All-one bits do not prove presence because other keys may have set them. Corruption, incompatible prefix rules, or metadata mismatch invalidates the premise and must fail safely.

**Level-count derivation.** Under the simplified assumption that level capacities grow geometrically as $M,MT,MT^2,\ldots$, the deepest level index sufficient for $N$ satisfies $MT^L\ge N$. Dividing by $M$ and taking logarithm base $T$ gives $L\ge\log_T(N/M)$, hence $L=\lceil\log_T(N/M)\rceil$. This is a shape estimate, not a theorem about files probed or bytes rewritten by a concrete engine.

**Debt stability.** If new work arrives indefinitely at average physical demand $aw$ and available compaction service is $c$, bounded debt requires long-run service to exceed demand over the relevant workload regime. When $c\le aw$, scheduling can rearrange pain but cannot drain the queue. Bursts also require buffers and recovery headroom; average stability alone does not bound tails.

**Tombstone safety.** A tombstone for key $k$ may be removed only if every possible older value for $k$ has been eliminated or remains forever shadowed in all states that can rejoin, and no supported snapshot/history consumer needs the delete. This includes local runs, disconnected replicas, repair sources, backups, external value logs, and change feeds named by the system contract.

## Alternatives and Trade-Offs

**B+ trees versus LSM trees.** B+ trees maintain a search structure through in-place or copy-on-write page changes, commonly favoring bounded point/range navigation and stable read cost. LSM trees batch and defer organization, commonly favoring heavy ingest. Storage hardware, cache, concurrency control, compression, and workload can reverse simplistic expectations. Measure complete systems.

**Leveled versus tiered.** Leveled layouts spend rewriting to constrain overlap and read fanout. Tiered layouts postpone rewriting and retain more runs. Choose with read/write/range mix, overwrite/delete rate, space, device endurance, tail objectives, and recovery needs. Hybrid policies often dominate a pure label.

**Whole-key versus prefix filters.** Whole-key filters help exact misses. Prefix filters can help bounded prefix seeks only if comparator and prefix-extractor semantics align for every key and query. A changing prefix definition can make old filters unusable; version metadata and fallback are required.

**Integrated values versus separation.** Integrated values simplify atomic file construction and sequential scans but rewrite values during compaction. Separation reduces those bytes for large values while adding indirection and garbage collection. Evaluate point reads, ranges, overwrite locality, value-log cleaning, crash recovery, and backup together.

**Larger versus smaller memtables.** Larger memtables can improve batch size and reduce flush frequency but increase memory, recovery replay, and flush burst size. Multiple memtables or column families complicate fair budgeting. An enormous buffer postpones rather than removes downstream work.

**More versus fewer levels.** A larger size ratio can reduce level count while increasing compaction granularity and overlap consequences; a smaller ratio changes write/read/space behavior differently. Textbook asymptotics omit picker and file-boundary effects. Tune from traces and controlled experiments.

**Direct I/O versus page cache.** Direct I/O can avoid double caching and make cache ownership explicit. Buffered I/O can exploit mature kernel policies and simplify implementation. Alignment, readahead, memory pressure, checksums, encryption, and observability differ. Neither is universally faster or safer.

**Foreground versus background maintenance.** Aggressive maintenance limits debt but competes with requests; permissive maintenance improves short bursts but risks cliffs. Admission control and rate limiting make the trade explicit. Hidden debt turns a latency choice into an outage later.

## Failure Modes and Misconceptions

- **“An LSM performs one sequential write per update.”** WAL, flush, manifest, compaction, replication, value log, and metadata all contribute physical work.
- **“Bloom filters make reads constant-time.”** They only avoid some negative probes and consume memory/CPU; present keys, ranges, and false positives still touch data.
- **“A tombstone means the bytes are gone.”** It is logical precedence metadata until safe physical reclamation.
- **“Old tombstones can be deleted after a fixed grace.”** Safety depends on repair, restore, snapshots, and older-run coverage, not age alone.
- **“Compaction is housekeeping.”** It is part of correctness, performance stability, reclamation, and recovery.
- **“Average compaction bandwidth is enough.”** Headroom must cover peaks, debt drainage, failures, repair, and shared-resource contention.
- **“Low write amplification proves a good configuration.”** Reads, space, stalls, endurance, recovery, and cost may be unacceptable.
- **“Level zero is just another level.”** Arbitrary overlap makes its read and compaction behavior distinct.
- **“Immutable files eliminate corruption.”** They simplify publication and concurrency but still require checksums, verified metadata, and recovery.
- **“A database using RocksDB has RocksDB's contract.”** Wrapping systems add replication, caching, transactions, GC, and configuration that change guarantees.
- **“Client timestamps identify the latest value.”** Clock skew and concurrency make them unsafe without a defined ordering protocol.
- **“Benchmark completion proves sustainable service.”** A short run can end before debt, cache eviction, snapshots, or space pressure mature.
- **“Delete and TTL are equivalent.”** Their visibility clocks, propagation, backup, and compliance semantics can differ.
- **“More compaction threads always help.”** Device saturation and CPU/cache contention can worsen foreground tails.
- **“Recovery can simply replay every WAL.”** Replaying records already covered by installed state must be idempotent or correctly delimited.

## Worked Examples

### Example 1

**Situation.** A key has versions `x@2=red`, `x@6=blue`, and `x@9=green`. What do snapshots 5, 8, and 10 observe?

Filter to sequence at most the snapshot, then choose the greatest sequence. Snapshot 5 selects `x@2=red`; snapshot 8 selects `x@6=blue`; snapshot 10 selects `x@9=green`. Physical run age is irrelevant if the sequence order is intact.

**Conclusion.** Newest means newest eligible logical sequence, not newest file timestamp or first arbitrary file found.

### Example 2

**Situation.** WAL records 101 through 120 are synchronized. The memtable freezes, an SSTable for 101–120 is written, and the process crashes before manifest publication.

Recovery sees the old authoritative manifest, so it must ignore or clean the orphan SSTable. It replays synchronized WAL records 101–120 into memory and may later flush them again. Deleting the WAL before publication would lose acknowledged data; installing both independently without idempotent version handling could duplicate merge effects.

**Conclusion.** WAL retirement follows durable installation; output construction alone is not installation.

### Example 3

**Situation.** Four L0 files have ranges `[a,m]`, `[c,f]`, `[d,z]`, and `[x,z]`. A point lookup asks for `e`; another asks for `w`.

Key `e` lies in the first three ranges, so metadata alone permits three file probes; `w` lies only in `[d,z]`, so it permits one. A correct Bloom filter may reject some candidates. Unlike non-overlapping leveled files, L0 cannot generally route a key to one file.

**Conclusion.** File count plus overlap distribution, not file count alone, determines L0 point-read fanout.

### Example 4

**Situation.** A system assigns 10 Bloom-filter bits per key. Estimate the ideal number of hashes and false-positive probability.

With $m/n=10$, $h\approx10\ln2\approx6.93$, so use about 7 hash locations. The idealized probability is $(1-e^{-7/10})^7\approx0.00819$, about 0.82%. This assumes classical independent hashing and excludes blocked layout and metadata overhead.

**Conclusion.** The equation provides a calibration point; measured filter behavior for the exact implementation remains necessary.

### Example 5

**Situation.** A tombstone `acct@50=DEL` reaches one compacted level, but an older `acct@12=active` remains in a deeper non-input file. No snapshot older than 50 remains. May compaction drop the tombstone?

No. A later lookup that reaches the deeper file could resurrect `active` after the tombstone disappears. The compaction needs proof that no older version exists outside its reconciliation scope, or it must preserve the tombstone. Distributed repair and backups may extend that scope further.

**Conclusion.** Snapshot expiry is necessary in this case but not sufficient for safe tombstone removal.

### Example 6

**Situation.** Logical flush arrival is 40 MB/s, and measured downstream compaction writes average 6 physical bytes per flushed byte. Available sustained compaction service is 300 MB/s. Debt is 360 GB.

Demand is $40\times6=240$ MB/s, leaving ideal spare service of 60 MB/s. Using decimal units, ideal drain time is $360{,}000/60=6{,}000$ seconds, or 100 minutes. Foreground contention and changing amplification make actual time longer. If service falls to 240 MB/s, debt never drains under steady load.

**Conclusion.** Healthy-looking foreground throughput can coexist with hours of recovery work; operate on debt and spare service.

### Example 7

**Situation.** Live logical data is 1 TB. Current SSTables occupy 1.18 TB, obsolete files pinned by snapshots occupy 0.35 TB, compaction needs up to 0.30 TB temporary output, and WAL/metadata need 0.05 TB. Is a 1.5 TB volume sufficient?

The immediate worst modeled footprint is $1.18+0.35+0.30+0.05=1.88$ TB, excluding safety margin and growth. The volume is already structurally unable to perform the reclaiming compaction safely. Waiting for 1.5 TB utilization can deadlock reclamation.

**Conclusion.** Capacity planning must include pinned and temporary bytes, not only live data or current table files.

### Example 8

**Situation.** A 1 KB key has a 4 MB value updated frequently. Compare integrated and separated storage qualitatively.

Integrated compaction repeatedly reads and writes the 4 MB value whenever its key range moves, but lookups and scans have simple locality. Separation compacts the key and pointer while appending the value once, reducing LSM rewrite bytes. It adds a second lookup, value-log garbage collection, crash-order requirements, and potentially random range-scan I/O.

**Conclusion.** Key-value separation targets large-value rewrite amplification by accepting indirection and a new reclamation system.

### Example 9

**Situation.** A benchmark writes for ten minutes with compaction disabled, reports 500,000 operations/s, and exits before reads or restart.

The run measured buffer/WAL admission until memory and L0 limits, not sustainable service. It omitted compaction debt, read fanout, write stalls, space, recovery, and durability verification. Extend the run through steady state, enable production policy, measure all physical bytes, exercise reads and snapshots, and drain debt after offered load stops.

**Conclusion.** Deferred work must be included in the measurement window and accounting boundary.

### Example 10

**Situation.** During a crash campaign, an engine returns success for sequence 700, crashes after output-file sync but before manifest sync, and restarts with sequence 700 visible from WAL replay. A candidate output file remains unreferenced.

The logical oracle passes if the acknowledgement contract required WAL persistence and replay restores the mutation. Recovery should treat the unreferenced output as orphan, not as an additional authority. Repeating the campaign at every persistence boundary and verifying scans, snapshots, and checksums tests more than process restart alone.

**Conclusion.** Recovery correctness concerns authoritative state and visible history, not whether every pre-crash file survives.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies ordered dictionaries, merge algorithms, Bloom filters, hashing, cache-aware layout, and amortized analysis. This module composes them into a durable versioned storage lifecycle.

[Operating Systems](../../22-operating-systems/ROADMAP.md) owns filesystem persistence, direct and buffered I/O, scheduling, page cache, device queues, file descriptors, memory pressure, and crash behavior. An LSM contract must name rather than assume those mechanisms.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects offered load, queue stability, resource headroom, observability, fault injection, and recovery evidence. Compaction debt is a queue with production consequences.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns replicated ordering, consensus, anti-entropy, membership, and partitions. An LSM is a local storage organization unless a larger protocol supplies those guarantees.

[Data Engineering](../../19-data-engineering/ROADMAP.md) connects logs, state stores, compaction, change data, replay, TTL, and workload operations. Broker log compaction and LSM compaction have related vocabulary but different contracts and must not be conflated.

[Security Engineering](../../25-security-engineering/ROADMAP.md) adds encryption keys, tenant isolation, secure deletion limits, integrity, backup access, and hostile input. Logical tombstone visibility does not prove physical erasure from files, replicas, or backups.

## References

- Patrick O'Neil, Edward Cheng, Dieter Gawlick, and Elizabeth O'Neil, [The Log-Structured Merge-Tree (LSM-Tree)](https://doi.org/10.1007/s002360050048), *Acta Informatica* 33, 1996. Foundational multi-component merge-tree design and cost motivation.
- Fay Chang et al., [Bigtable: A Distributed Storage System for Structured Data](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/), OSDI 2006. Memtables, immutable SSTables, locality groups, compaction, and tablet recovery in a distributed system.
- Google LevelDB, [Implementation notes](https://github.com/google/leveldb/blob/main/doc/impl.md), current document checked 2026-09-05. Sequence-tagged keys, memtables, levels, lookup, compaction, and recovery boundaries in a concrete implementation.
- RocksDB, [Leveled Compaction](https://github.com/facebook/rocksdb/wiki/Leveled-Compaction), current official wiki checked 2026-09-05. Level targets, overlap, file selection, and implementation-specific amplification.
- RocksDB, [Universal Compaction](https://github.com/facebook/rocksdb/wiki/Universal-Compaction), current official wiki checked 2026-09-05. Run-based compaction policy and its space/read/write trade-offs.
- RocksDB, [RocksDB Bloom Filter](https://github.com/facebook/rocksdb/wiki/RocksDB-Bloom-Filter), current official wiki checked 2026-09-05. Full and partitioned filters, prefix use, and current implementation considerations.
- RocksDB, [Write Stalls](https://github.com/facebook/rocksdb/wiki/Write-Stalls), current official wiki checked 2026-09-05. Memtable, level-zero, pending-compaction, and rate-control stall mechanisms.
- Niv Dayan, Manos Athanassoulis, and Stratos Idreos, [Monkey: Optimal Navigable Key-Value Store](https://dl.acm.org/doi/10.1145/3035918.3064054), SIGMOD 2017. Memory allocation across LSM levels and read/update trade-offs.
- Lanyue Lu et al., [WiscKey: Separating Keys from Values in SSD-Conscious Storage](https://www.usenix.org/conference/fast16/technical-sessions/presentation/lu), FAST 2016. Key-value separation, reduced LSM value rewriting, and value-log trade-offs.
- Yangchun Li et al., [PebblesDB: Building Key-Value Stores using Fragmented Log-Structured Merge Trees](https://dl.acm.org/doi/10.1145/3132747.3132765), SOSP 2017. Guard-based fragmentation and a different point in the write/read/space design space.

## Exercises

### Exercise 1

Define WAL, memtable, SSTable, compaction, tombstone, and snapshot. For each, state whether it is a logical contract, physical mechanism, or metadata/control concept, noting any overlap.

### Exercise 2

A key has versions `p@4=A`, `p@9=DEL`, and `p@13=B` across three runs. Derive results for snapshots 7, 11, and 15. Then explain which versions a compaction may discard while snapshots 7 and 11 remain active.

### Exercise 3

An engine develops write stalls: logical writes are 25 MB/s, downstream physical compaction demand is 8 bytes per logical byte, measured service is 170 MB/s, L0 files grow, and free space is 12%. Diagnose the queue, compute its average imbalance, and propose a safe evidence-driven response.

### Exercise 4

Compare leveled compaction, tiered compaction, and key-value separation for (a) 95% missing point reads with 200-byte values, (b) append-heavy 8 MB values with rare ranges, and (c) frequent ordered scans with strict space limits. State assumptions and reject any choice that lacks necessary evidence.

### Exercise 5

A store removes tombstones after 48 hours. A replica can be disconnected for seven days, and weekly backups can restore SSTables that contain pre-delete values. Design a deletion and recovery protocol that prevents resurrection, supports snapshots, and states what “deleted” can honestly mean for logical visibility and physical erasure.

## Answers to the Exercises

### Answer 1

The **WAL** is a physical recovery mechanism whose persistence ordering supports a logical durability contract. The **memtable** is a mutable physical ordered index for recent versions. An **SSTable** is an immutable physical sorted file plus indexes, filters, checksums, and bounds. **Compaction** is a physical/background mechanism with semantic obligations: it replaces runs while preserving retained-snapshot results. A **tombstone** is logical version metadata represented physically in memory/files; it makes a selected key absent. A **snapshot** is a logical visibility boundary, implemented through sequence/version metadata and retention control. The categories overlap because physical mechanisms exist to realize logical guarantees, but naming the layer prevents claiming more than the mechanism proves.

### Answer 2

At snapshot 7, eligible versions contain only `p@4=A`, so the result is A. At snapshot 11, `p@9=DEL` is greatest and the result is absent. At snapshot 15, `p@13=B` is greatest and the result is B. While snapshots 7 and 11 remain, all three versions can be necessary: sequence 4 supplies snapshot 7, the tombstone supplies snapshot 11, and sequence 13 supplies current/later reads. After snapshot 7 ends, sequence 4 may be removable only if no other snapshot or external history obligation needs it; while snapshot 11 remains, the tombstone cannot be dropped. The compaction must also consider older versions outside its inputs and distributed restore/repair scope.

### Answer 3

Average physical demand is $25\times8=200$ MB/s while service is 170 MB/s, so debt grows by at least 30 MB/s under the stated boundary. Growing L0 and low free space show the deferred queue is already affecting routing and threatens the temporary space needed to compact. First protect correctness and space: preserve WAL and manifest invariants, throttle/admit fewer writes, stop optional bulk work, protect reserve space, and avoid deleting live inputs. Measure compaction read/write/CPU/device saturation, overlap, snapshots, tombstones, per-range skew, and stall causes. Add or isolate service, reduce offered load, release safe pinned history, or change policy only through controlled tests. Raising stall thresholds alone worsens the cliff. Recovery is demonstrated when service exceeds physical arrival with headroom, debt drains, L0 falls, free space recovers, and foreground latency/durability remain within contract.

### Answer 4

For missing point reads with small values, leveled layout plus correctly configured Bloom filters is a strong candidate because bounded overlap and negative filtering reduce probes; validate filter memory and update cost. For huge append-heavy values and rare ranges, key-value separation or a tiered policy may reduce value rewriting, but must pass value-log GC, indirection, crash, and space tests. For frequent ordered scans under strict space limits, leveled compaction is the leading candidate because fewer overlapping runs and lower retained-run space generally help; verify rewrite endurance and ingest tails. These are conditional model answers, not universal selections. Acceptable alternatives must name key distribution, update/delete rate, snapshots, device, cache, durability, range size, compression, and measured read/write/space amplification plus recovery. A product label without that evidence is not an acceptable design answer.

### Answer 5

Forty-eight-hour tombstone removal is unsafe because both a seven-day replica and a weekly restore can reintroduce older values. Retain deletion/version evidence longer than the maximum disconnected-replica, repair, restore, and snapshot horizon with operational margin, or require stale replicas/restores to bootstrap from a snapshot whose deletion frontier is at least as new as the tombstone before serving. Record per-range deletion frontiers and sequence epochs; fence stale replicas; reconcile every older run; make backup restoration apply an authoritative deletion log or a post-frontier full image; and test a restore containing the pre-delete value. Bound snapshot age or preserve tombstones/versions for supported snapshots. “Logically deleted” can mean current authorized reads select a tombstone after a named commit point. “Physically erased” requires separate evidence across active files, obsolete files, value logs, replicas, caches, backups, media lifecycle, and encryption keys; if backups retain bytes by policy, do not claim immediate physical erasure.
