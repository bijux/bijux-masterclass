---
module_id: DSE-076
program: Data Structures Engineering
level: 2
module_number: 76
title: Log-Structured Merge Trees
status: complete
last_verified: 2026-08-30
---

# Log-Structured Merge Trees

## One-Page Review

### Governing question

How can an LSM tree convert random logical updates into append/sequential writes while preserving newest-version, deletion, snapshot, recovery, and compaction correctness under bounded resources?

### Essential definitions

- A **log-structured merge tree (LSM tree)** buffers ordered updates in memory and periodically flushes immutable sorted runs that are merged/compacted over time.
- A **write-ahead/commit log (WAL)** durably records acknowledged mutations until an immutable run and manifest make them recoverable without that log segment.
- A **memtable** is the active in-memory ordered mutation structure; an **immutable memtable** is frozen for flush while a new active table accepts writes.
- An **SSTable/sorted run** is an immutable ordered file with data blocks plus indexes, filters, checksums, and metadata.
- A **sequence number/timestamp** orders versions according to the engine's transaction model. Wall-clock timestamps alone are not automatically a total or causal order.
- A **tombstone** is a versioned deletion marker that suppresses older values until it is safe to discard both marker and hidden versions.
- **Compaction** merges selected runs, resolves versions under snapshots/retention, writes new immutable runs, and atomically replaces inputs in the serving manifest.
- **Read, write, and space amplification** compare physical work/retained bytes to a declared logical workload; definitions and scope must be explicit.

### Central model, mechanism, or theorem

The write path appends a durable mutation to WAL, inserts it into the active memtable, freezes the table at a threshold, emits one sorted immutable run, and later compacts runs. Sorting/merge converts many scattered logical updates into large ordered writes. A read constructs one logical view by consulting the active and immutable memtables plus candidate runs, choosing the highest visible version per key and treating a visible tombstone as absence.

In a leveled design with size ratio T and data size N above memory/run base M, the number of levels is approximately `L=ceil(log_T(N/M))`, but exact write/read amplification depends on overlap, level targets, file selection, duplicate/update distribution, compaction policy, compression, and accounting. Tiered designs merge several similarly sized runs and often reduce write amplification at the expense of more simultaneous runs, read amplification, and temporary space. These are workload/policy trade-offs, not universal constants.

Compaction is correct only if output represents the same logical versioned map for every supported snapshot as inputs plus any overlapping state not selected. It may drop an overwritten value only when no supported reader needs it. It may drop a tombstone only when no older value can reappear from unexamined storage, replicas/repair, backups, or snapshots and the retention protocol permits it.

### Critical invariants

1. Every acknowledged mutation is recoverable from WAL or a durably installed immutable run/manifest state.
2. Entry identity includes key, sequence/version, kind, and value/metadata; comparison and visibility are deterministic.
3. Every run is internally ordered, immutable, checksummed, and described by verified range/sequence/format metadata.
4. Reads choose the newest visible version across all candidate sources and never return a value masked by a visible tombstone.
5. Compaction output conserves all versions required by active snapshots, retention, transactions, replication, repair, and recovery.
6. Manifest installation makes outputs visible and inputs obsolete atomically/recoverably; files are deleted only after reader/version safety.
7. Backpressure prevents memtable, L0/run count, compaction debt, WAL, disk, and temporary space from exceeding correctness reserves.

### Common failures

- Acknowledging after memtable insertion but before the configured WAL durability boundary.
- Deleting WAL when flush data exists but before its file footer/checksum and manifest addition are durable.
- Reading the first file that contains a key rather than comparing version sequence across overlapping sources.
- Dropping tombstones merely because they are old, allowing deleted values to resurrect.
- Compacting files without all required overlap, violating range/version reasoning.
- Deleting input files immediately after manifest update while readers still hold the old version.
- Treating Bloom-filter negatives, min/max metadata, or checksums as stronger than their actual guarantees.
- Optimizing average write throughput while compaction debt, p999 stalls, recovery time, or temporary space grows without bound.

### Compact example

An active memtable has `a@5=A5`, `d@6=D6`, and tombstone `e@7`. New and old runs contain older versions. Merge by key and descending sequence yields visible `a=A5,b=B1,c=C3,d=D6`; e is absent because its newest version is deletion. A compacted version-retaining run includes `e@7=DEL` until horizon/overlap evidence proves it safe to discard.

### Connections

DSE-071 supplies external I/O/page reasoning, DSE-074 sorted construction/ranges, DSE-075 immutable generation publication, DSE-077 SSTable format, DSE-078 filters, DSE-079 compaction policies, and DSE-080 amplification trade-offs. Database and Data Engineering add transactions, distributed repair, streaming state, checkpoints, and operational lifecycle.

## Governing Question

How do we turn the appealing “memory buffer plus sorted files” picture into a durable, snapshot-correct, resource-bounded storage engine whose compactions cannot lose or resurrect data?

## Why This Matters

In-place trees pay random writes and structural page updates on the foreground path. LSM trees append intent, buffer mutations, flush sorted runs, and move much of reorganization into background merges. This suits high-ingest databases, time-series stores, distributed wide-column systems, embedded key-value engines, search/index pipelines, and stream processors.

The deferred work does not disappear. Reads may consult several runs. Updates create multiple versions. Deletion becomes a marker. Compaction rereads and rewrites data, competes with foreground I/O, requires temporary space, and creates long tail stalls if debt grows. Recovery must reconcile WAL, memtables, files, manifest versions, and interrupted compactions. Snapshots and distributed repair delay garbage collection.

Therefore an LSM is not “fast writes” as a data structure. It is a pipeline with conservation laws and queues. Correctness specifies version order, visibility, tombstone horizons, file-set publication, and reader lifetime. Stability requires service capacity for average and burst compaction work. Evidence must cover logical oracles, encoded files, crash points, schedules, backpressure, and sustained workload tails.

## Prerequisites and Retrieval

Retrieve:

- ordered maps, merge sort/k-way merge, iterators, duplicate resolution, and external-memory costs;
- WAL, group commit, checksums, fsync/barriers, manifest/root publication, and generation recovery;
- MVCC snapshots, transaction sequence, tombstones, TTL, retention, and distributed repair;
- immutable files, filters/index metadata, cache hierarchy, file references, epochs, and delayed deletion;
- queuing/backpressure, amplification metrics, fault injection, reconciliation, and benchmark steady state.

Diagnostic retrieval: if a tombstone `x@9` is compacted with value `x@8` but another unselected lower-level run contains `x@3`, dropping both selected entries can resurrect x@3. The compactor must prove the output level/bottom coverage and snapshot/repair horizon before eliding the tombstone.

## Learning Objectives

After this module, you can:

1. specify WAL, memtable/freeze/flush, immutable run, manifest, read, and compaction lifecycles;
2. define total version order, snapshots, tombstones, TTL, merge operands, and conflict semantics;
3. trace point/range reads across overlapping sources with newest-visible resolution;
4. distinguish leveled, tiered/universal, FIFO/time-window, and hybrid compaction assumptions;
5. design atomic output installation, input retirement, WAL release, and crash recovery;
6. prove when obsolete versions/tombstones are retained or may be discarded;
7. control compaction debt, stalls, disk/WAL/temp space, scheduling, and tenant interference;
8. measure read/write/space amplification, latency tails, recovery, and data integrity with scoped evidence.

## Core Exposition

**Define the logical versioned map.** An internal entry can be `(user_key,sequence,kind,payload)`, ordered by user key then newest sequence first, with a deterministic kind/tie rule. Sequence allocation follows the transaction model: a batch may share sequence range; uncommitted entries must not leak; snapshots define a maximum visible sequence plus transaction/tenant rules. Merge operators and partial updates need an associative/deterministic contract or must retain inputs until evaluated safely.

**A write crosses explicit durability states.** Assign sequence/transaction identity, encode checksum-protected WAL record, append, satisfy configured group-commit durability, then expose in memtable. Some systems expose before sync under weaker acknowledged semantics; document it. When freezing a memtable, pair it with the WAL interval needed for recovery. A new active table/log accepts writes while the immutable table flushes.

**Flush creates a private immutable run.** Iterate the frozen table in internal-key order, build blocks/index/filter/footer, write to a temporary/new file identity, complete checksum and required durability, then append/install a version edit in the manifest. Only after that edit and its durability make the run recoverable may the corresponding WAL be recycled, subject to other tables/replicas/backups. A crash at every boundary must either replay WAL or use the installed run, never lose both.

**Reads merge sources.** Point lookup checks active/immutable memory and candidate on-disk files. Nonoverlapping levels need at most one candidate per level; L0 or tiered runs may overlap. Filters can skip a file only under their no-false-negative construction/format contract. Indexes locate blocks. Among found internal entries, choose newest snapshot-visible; tombstone returns absence. Range scans k-way merge iterators, coalesce versions per user key, filter visibility, and stop at bounds.

**The bounded model isolates resolution.** It merges three newest-to-oldest sources with explicit sequence numbers. Point lookup counts sources until a key version is found; full compaction selects each key's newest entry and deliberately retains deletion.

<!-- bijux-verify: {"id":"bounded-lsm-version-merge-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input_records=9\nunique_keys=5\ncompacted=a:5:A5,b:1:B1,c:3:C3,d:6:D6,e:7:DEL\nvisible=a=A5,b=B1,c=C3,d=D6\nread_a_runs_consulted=1\nread_b_runs_consulted=3\nlatest_a=A5\nlatest_e=DEL\ntombstone_e_suppresses=True\nsequence_order_valid=True\nvalid=True\nevidence=bounded_lsm_version_merge_model\n","stderr":""}} -->
```python
sources = [
    [("a", 5, "A5"), ("d", 6, "D6"), ("e", 7, None)],
    [("a", 4, "A4"), ("c", 3, "C3"), ("e", 2, "E2")],
    [("a", 1, "A1"), ("b", 1, "B1"), ("d", 1, "D1")],
]


def point(key):
    best = None
    consulted = 0
    for source in sources:
        consulted += 1
        for entry in source:
            if entry[0] == key and (best is None or entry[1] > best[1]):
                best = entry
        if best is not None:
            return best, consulted
    return None, consulted


def compact():
    newest = {}
    for source in sources:
        for key, sequence, value in source:
            current = newest.get(key)
            if current is None or sequence > current[0]:
                newest[key] = (sequence, value)
    return [(key, newest[key][0], newest[key][1]) for key in sorted(newest)]


def format_entry(entry):
    key, sequence, value = entry
    rendered = "DEL" if value is None else value
    return f"{key}:{sequence}:{rendered}"


compacted = compact()
visible = [(key, value) for key, _, value in compacted if value is not None]
a_entry, a_runs = point("a")
b_entry, b_runs = point("b")
e_entry, _ = point("e")
ordered_sources = all(source == sorted(source, key=lambda entry: entry[0]) for source in sources)
keys = [entry[0] for entry in compacted]
valid = ordered_sources and keys == sorted(set(keys)) and a_entry[2] == "A5" and e_entry[2] is None
print(f"input_records={sum(len(source) for source in sources)}")
print(f"unique_keys={len(compacted)}")
print("compacted=" + ",".join(format_entry(entry) for entry in compacted))
print("visible=" + ",".join(f"{key}={value}" for key, value in visible))
print(f"read_a_runs_consulted={a_runs}")
print(f"read_b_runs_consulted={b_runs}")
print(f"latest_a={a_entry[2]}")
print("latest_e=" + ("DEL" if e_entry[2] is None else e_entry[2]))
print(f"tombstone_e_suppresses={all(key != 'e' for key, _ in visible)}")
print(f"sequence_order_valid={ordered_sources}")
print(f"valid={valid}")
print("evidence=bounded_lsm_version_merge_model")
```

The point shortcut assumes sources are ordered newest-to-oldest by nonoverlapping sequence epochs, so the first source containing a key has its newest version. The model has unique integer-like string keys, no snapshots below latest, transactions, range iterator, TTL, merge operands, filters, blocks/files, WAL, manifest, I/O, concurrency, distributed repair, or compaction horizon. It retains the tombstone and establishes no safe-elision rule.

**Compaction selects a complete overlap closure.** For leveled compaction, choose input files from one level and every overlapping file in the output level; sometimes grandparents/other metadata constrain output splitting. If a version outside the selected closure can affect the same key/snapshot, output resolution must retain sufficient markers. Inputs are pinned to a manifest/version while merge runs; new writes/flushes belong to later versions.

**Publish outputs before retiring inputs.** Write private output files with validated footer/checksum/range/sequence metadata and durable bytes. Atomically/recoverably append a manifest version edit that adds outputs and removes inputs. Readers on old manifest retain file references; new readers see new version. Delete files only after no reader, backup, checkpoint, replica, recovery, or pending job requires them. Reconcile orphan output and obsolete input files after crash.

**Tombstone collection is global reasoning.** Conditions may include: compaction covers all older data for the key/range down to bottom; no supported snapshot can see pre-delete state; retention/grace elapsed; replication and repair guarantee no stale replica can reintroduce the value; backups/change streams no longer need it; TTL semantics are stable. A local age threshold alone is insufficient. Distributed systems often intentionally retain tombstones for repair safety.

**Leveled compaction bounds overlap aggressively.** L0 has overlapping flush files; lower numbered levels compact into larger nonoverlapping ranges, with size targets often scaled by T. Point reads can use one candidate per nonzero level plus L0, improving read amplification. Rewriting a small upper run into overlapping large lower data increases write amplification. File size, level base, dynamic sizing, subcompaction, and hot ranges change results.

**Tiered/universal compaction delays merging.** Keep multiple sorted runs and merge similarly sized/all selected runs when thresholds trigger. Each item is often rewritten fewer times for a given growth pattern, but reads consult more runs and temporary/steady space increases. FIFO/time-window policies can expire whole files for time-bounded workloads only if lateness, updates, tombstones, and query horizons satisfy their assumptions. Hybrid policies combine behaviors.

**Backpressure closes the feedback loop.** Track active/immutable memory, flush bandwidth, L0 files/bytes, level scores, pending compaction bytes, WAL retention, temporary space, write rate, compaction throughput, and device saturation. Slow/stall writes before memory or disk safety is lost. Reserve space for worst-case compaction output plus live inputs and manifest/WAL. Coordinate flush and compaction scheduling across tenants to prevent starvation.

**Metadata pruning must be trustworthy.** Per-file key bounds, sequence bounds, filters, indexes, properties, and checksums accelerate reads and planning. Validate them during creation/open; a false-negative filter or incorrect range can cause data loss at read time. Filters generally answer user-key membership, not version visibility. Checksums detect scoped corruption but do not prove manifest completeness or newest-version selection.

**Recovery is a state-machine audit.** Identify CURRENT/manifest, validate records and referenced files, replay committed WAL not represented in installed runs, discard/quarantine incomplete temporaries, preserve files referenced by any valid recovery version, and reconcile sequence allocation. Define paranoid versus salvage modes. Never silently ignore corrupt manifest/file/WAL and claim a current database.

**Test long-running equivalence.** Generate mutation histories with inserts, overwrites, deletes, TTL, transactions, snapshots, flushes, and compactions; compare every snapshot point/range with an independent versioned-map oracle. Exhaust small schedules. Fuzz file/manifest/WAL parsers. Crash after each append, sync, rename, manifest edit, file retirement, and directory operation under realistic reordering. Run sustained workloads until compaction debt and space stabilize.

## Definitions and Notation

Let M be effective memtable/run base size, T size ratio, N live/versioned data as declared, L levels, and R simultaneously consulted runs. An entry is `(k,s,kind,payload)`. Snapshot q admits entries under a defined `visible(s,q,transaction)` predicate. `DEL` is a tombstone; TTL expiry may synthesize deletion semantics under a time authority.

`WA=physical bytes written/logical bytes written`, `RA=physical/logical reads per operation or runs/blocks consulted`, and `SA=physical retained bytes/logical live bytes` are examples, not universal definitions. State whether WAL, cache, compaction reads, replication, compression, temporary space, obsolete files, and tombstones count. `VersionSet/ManifestGeneration` identifies a serving file set; file identity includes number/generation and checksum.

## Mechanisms, Invariants, or Proof Structure

### Write/recovery proof

1. Assign deterministic committed version identity and append a valid WAL record.
2. Cross the documented durability boundary before acknowledgment.
3. Insert identical mutation into memtable; freeze with its recovery log interval.
4. Write/check/sync immutable run, then install it through durable manifest edit.
5. Recycle WAL only after every represented mutation remains recoverable elsewhere.
6. Crash at any prefix and show replay plus installed files yields exactly acknowledged commits.

### Read/merge proof

1. Enumerate every source whose key/range and version may affect the snapshot.
2. Seek/iterate sources under their verified ordering and metadata.
3. For each user key, select newest transaction-visible internal entry.
4. Return value, apply merge/TTL, or suppress under tombstone exactly once.
5. Preserve total key order and endpoint/limit/resume semantics for ranges.
6. Pin manifest/files so compaction retirement cannot invalidate the read.

### Compaction proof

1. Pin input manifest and select complete required range/version overlap.
2. K-way merge internal entries without loss, duplicate creation, or order corruption.
3. Retain every version/tombstone required by supported snapshots and external horizons.
4. Write/check/sync outputs and validate range/sequence/footer properties.
5. Atomically install add-output/remove-input edit; old readers retain old version/files.
6. Reclaim inputs only after lifetimes; reconcile every crash prefix and orphan output.

## Alternatives and Trade-Offs

| Choice | Strength | Cost/proof burden |
|---|---|---|
| B/B+ in-place index | bounded point path | random writes/page contention |
| LSM buffering | sequentialized write path | compaction/read/space amplification |
| Leveled compaction | fewer read candidates | rewriting overlap |
| Tiered/universal | lower write amplification | more runs and space/read cost |
| FIFO/time-window | cheap expiry for time data | late/update/delete assumptions |
| Large memtable | fewer/larger flushes | memory, recovery, stall burst |
| Many small files | fine compaction parallelism | metadata/open/read amplification |
| Large files | lower metadata overhead | coarse overlap and long jobs |
| Full WAL sync | strong acknowledged durability | foreground/group-commit latency |
| Weaker WAL policy | throughput | explicit loss window |
| Eager tombstone purge | space/read savings | resurrection risk |
| Conservative retention | safety | space/read amplification |

## Failure Modes and Misconceptions

- **“LSM means no random I/O.”** Reads, metadata, compaction placement, WAL, and device behavior vary.
- **“Memtable is durable.”** Only under a proven WAL/persistent-memory protocol and acknowledged boundary.
- **“Flush lets us delete WAL immediately.”** File and manifest durability plus all dependent tables determine release.
- **“Newest file contains newest key.”** Use explicit sequence/version order across overlaps.
- **“Bloom negative proves absence universally.”** It is scoped to correctly built file membership, not other sources/visibility.
- **“Delete removes data.”** It inserts a tombstone until safe global garbage collection.
- **“Old tombstones are safe to drop.”** Check overlap, snapshot, replica/repair, backup, and retention horizons.
- **“Compaction is maintenance only.”** It is correctness-critical serving-state transformation.
- **“Immutable inputs can be deleted after manifest edit.”** Old readers and recovery versions may pin them.
- **“Tiered always wins writes; leveled always wins reads.”** Workload, ratio, overlap, cache, files, and metrics determine results.
- **“High throughput means stable system.”** Debt and tail stalls can accumulate beyond the benchmark window.
- **“Checksums prove no lost key.”** Reconcile manifest/file set and logical versioned oracle.

## Worked Examples

### Example 1

**Problem.** Resolve a in the compact model.

**Derivation.** Memtable has a@5, newer run a@4, old run a@1. Latest visible is A5; first-source shortcut is valid only because source sequence epochs are ordered.

**Conclusion.** Recency comes from sequence semantics, not filename intuition.

### Example 2

**Problem.** Resolve e.

**Derivation.** Tombstone e@7 is newer than E2, so latest view returns absent. Compaction retains e@7=DEL because no bottom/snapshot/repair horizon is modeled.

**Conclusion.** Deletion markers participate in ordinary version order.

### Example 3

**Problem.** Read b in three sources.

**Derivation.** Neither memory nor newer run contains b; old run returns B1 after three consultations. Correct filters could skip negative file/block work but cannot skip unrepresented sources.

**Conclusion.** Run overlap drives read amplification.

### Example 4

**Problem.** Crash after SSTable sync but before manifest add.

**Derivation.** Run is private/orphan; WAL remains necessary. Recovery replays WAL and later reclaims/quarantines the unreferenced file.

**Conclusion.** File existence does not equal serving-state installation.

### Example 5

**Problem.** Crash after manifest add but before WAL deletion.

**Derivation.** Installed run represents mutations; replay must use sequence/idempotence to avoid logical duplication, then redundant WAL can be released.

**Conclusion.** Recovery tolerates overlap between protection mechanisms.

### Example 6

**Problem.** Compact an L1 file without all overlapping L2 files.

**Derivation.** Output can coexist with hidden older versions or violate L2 nonoverlap, invalidating point candidate and tombstone-elision reasoning. Select complete overlap closure.

**Conclusion.** Compaction selection is part of correctness.

### Example 7

**Problem.** A snapshot q predates value v2 but compaction drops v1.

**Derivation.** Latest reads remain correct, but q loses its visible version. Retain v1 until oldest supported snapshot horizon advances.

**Conclusion.** Obsolete depends on all supported views.

### Example 8

**Problem.** Writes arrive 200 MiB/s and sustainable compaction is 150 MiB/s equivalent.

**Derivation.** Debt grows 50 MiB/s before amplification details; finite buffers eventually stall or exhaust disk. Reduce ingest, increase capacity/efficiency, or change policy.

**Conclusion.** Stable operation requires long-run service >= generated work.

### Example 9

**Problem.** A tiered merge needs 300 GiB output while retaining 300 GiB inputs on a disk with 200 GiB free.

**Derivation.** It cannot safely complete despite eventual live size. Reserve, choose smaller jobs/policy, add capacity, or reject writes before crisis.

**Conclusion.** Temporary space is a correctness constraint.

### Example 10

**Problem.** Benchmark ends before L0 compaction catches up.

**Derivation.** Report debt, files, WAL, space, stalls, and post-load drain. Run steady state or explicitly label burst absorption; p50 ingest alone is misleading.

**Conclusion.** Deferred work must appear in the evidence window.

## Cross-Program Connections

- **Database Engineering:** transaction sequence, snapshots, WAL, recovery, indexes, TTL, backup, replication, and schema/column families define logical storage semantics.
- **Data Engineering:** streaming state stores, checkpoints, changelogs, lake sorted files, compaction, partitioning, and late data reuse LSM mechanisms.
- **Distributed Systems:** replica repair, anti-entropy, consistency, clock/sequence assignment, tombstone grace, quorum, and topology changes govern safe deletion.
- **Operating Systems:** page cache/direct I/O, async writes, filesystem allocation, fsync, device queues, TRIM, and ENOSPC shape flush/compaction.
- **Security Engineering:** corrupt WAL/manifests/files, malicious keys/compression, filter false negatives, deletion retention, encryption rotation, and exhaustion are boundaries.
- **Performance Engineering:** cache/filter sizing, levels/ratio, scheduling, subcompaction, amplification, debt, stalls, and tail latency need sustained experiments.

## References

1. Patrick O'Neil, Edward Cheng, Dieter Gawlick, and Elizabeth O'Neil, [“The Log-Structured Merge-Tree (LSM-Tree)”](https://link.springer.com/article/10.1007/s002360050048), *Acta Informatica* 33, 1996. Original LSM-tree architecture and analytical motivation.
2. Google LevelDB, [“Implementation Notes”](https://github.com/google/leveldb/blob/main/doc/impl.md), current maintainer documentation accessed 2026-08-30. WAL, memtable, sorted tables, levels, manifest, and recovery organization.
3. RocksDB Project, [“RocksDB Overview”](https://github.com/facebook/rocksdb/wiki/RocksDB-Overview), current maintainer documentation accessed 2026-08-30. Memtable, WAL, SST, version, and compaction architecture.
4. RocksDB Project, [“Leveled Compaction”](https://github.com/facebook/rocksdb/wiki/Leveled-Compaction), current maintainer documentation accessed 2026-08-30. Level targets, overlap, files, reads, and compaction behavior.
5. RocksDB Project, [“Universal Compaction”](https://github.com/facebook/rocksdb/wiki/Universal-Compaction), current maintainer documentation accessed 2026-08-30. Tiered policy and read/write/space trade-offs.
6. Apache Cassandra, [“Storage Engine”](https://cassandra.apache.org/doc/stable/cassandra/architecture/storage-engine.html), current documentation accessed 2026-08-30. Commit log, memtable, SSTable, filters, compaction, and amplification.
7. Apache Cassandra, [“Compaction Overview”](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/compaction/overview.html), current documentation accessed 2026-08-30. Immutable runs, versions, tombstones, merge, and reader-safe file retirement.
8. RocksDB Project, [“Compaction”](https://github.com/facebook/rocksdb/wiki/Compaction), current maintainer documentation accessed 2026-08-30. Implemented leveled, universal, FIFO, and policy configuration context.

## Exercises

### Exercise 1

Specify an LSM write state machine from sequence assignment through WAL, acknowledgment, memtable freeze, run write, manifest install, WAL release, and recovery. Give every crash boundary and invariant.

### Exercise 2

For sources containing `x@9=DEL,x@7=V7`, an unselected lower run `x@3=V3`, snapshots at 8 and 10, and a lagging replica that may still send V3, determine what latest/snapshot reads return and what a compaction may discard.

### Exercise 3

Design point and range reads over active/immutable memtables, overlapping L0, nonoverlapping levels, filters/indexes, duplicates, tombstones, TTL, merge operands, snapshots, limits, resume, corruption, and concurrent compaction.

### Exercise 4

Design a crash-safe compaction protocol with overlap closure, version retention, outputs, checksums/properties, manifest edit, reader pinning, input deletion, orphan cleanup, ENOSPC reservation, and verification.

### Exercise 5

Audit a service that acknowledges before WAL sync, deletes WAL after file write but before manifest sync, trusts filter negatives after format migration, drops tombstones by age, deletes compacted inputs immediately, and reports only burst ingest throughput.

## Answers to the Exercises

### Answer 1

Assign deterministic transaction/sequence and encode checksummed WAL mutation. Append and cross configured durability/group-commit boundary before strong acknowledgment; insert the same committed mutation into active memtable. Freeze table with WAL interval and switch writers atomically to new active table/log. Write ordered blocks/index/filter/footer into a private run, verify/sync it, then durably append manifest edit adding its file/range/sequence. Release immutable table and WAL only when every covered mutation is recoverable from installed files and no other consumer needs the log.

Crash before WAL durability cannot be acknowledged under strong policy; after WAL/before memtable, replay restores; during/after run write but before manifest, ignore/reclaim private run and replay; after manifest before WAL deletion, installed run plus idempotent sequence replay remains correct; during log/file deletion, manifest/reference rules preserve required state. Test partial records, torn files/footer, fsync errors/reordering, CURRENT/manifest truncation, duplicate replay, sequence recovery, ENOSPC, and directory-entry durability.

### Answer 2

Latest snapshot 10 sees tombstone 9 and returns absent. Snapshot 8 cannot see tombstone 9, so it returns V7. Compaction involving only x@9 and x@7 cannot drop V7 while snapshot 8 is supported. It also cannot drop tombstone 9 merely after merging V7 because unselected V3 could resurrect for latest reads and the lagging replica/repair can reintroduce it.

It may retain all required versions, perhaps output x@9 DEL and x@7 V7. Tombstone/value collection requires oldest snapshot past their need, complete coverage of older x versions to bottom or a proven absence, and replica repair/grace/backup/change-stream horizons that prevent resurrection. Only then may it drop marker and hidden versions under the precise engine policy.

### Answer 3

Pin one manifest/version and snapshot. Search active then immutable memory and candidate L0 files plus at most policy-permitted files in nonoverlapping levels, but select by explicit sequence/transaction visibility, not first filename. Verified no-false-negative filters skip only their file/user-key membership; range/sequence properties and indexes locate blocks; corruption is explicit failure/redundant recovery, not absence.

Point chooses newest visible value/tombstone/merge result. Range creates internal-key iterators, k-way merges by user key and descending version, resolves duplicates/merge operands/TTL/tombstone for snapshot, emits total order within endpoints/limit, and resumes after full identity with snapshot/generation. File references keep compacted inputs alive; concurrent manifest updates do not change pinned view. Test all endpoints, many versions, deletes/expiry, filter migration, malformed metadata, snapshots, cancellation/retry, compaction schedules, and oracle equivalence.

### Answer 4

Pin input manifest and select files plus complete output-level overlap and any tombstone/version dependencies. Reserve worst-case output/temp/metadata space. K-way merge with exact internal order, retaining every snapshot/transaction/repair-required version and tombstone. Split legal sorted outputs; build verified indexes/filters/properties/footer/checksums; sync files and directory semantics as required.

Durably append one manifest edit adding outputs and removing inputs. New readers use new version; old readers pin old version/files. Retire and delete inputs only after readers, backups, checkpoints, replicas, and recovery no longer reference them. Crash before edit leaves orphan output; after edit inputs are obsolete but retained safely; recovery reconciles manifest, files, temporaries, pending deletions, and free space. Compare logical output with input oracle for every retained snapshot, validate ranges/order/properties, inject all write/sync/edit/delete errors, and verify no resurrection.

### Answer 5

Strong acknowledgment requires WAL durability (or explicitly weaker loss semantics); fix ordering/group commit and test power loss. A completed run without durable manifest is not serving/recovery state, so retain WAL until both file and version edit are durable. Migrated filters must be versioned/rebuilt/validated; false negatives are correctness failures, so distrust unsupported filters rather than return absence.

Tombstone age alone ignores old overlapping files, snapshots, replicas/repair, backup and TTL semantics; require complete safe horizons. Manifest removal does not end old reader lifetime; reference/epoch-pin input files then delete. Burst ingest can hide growing L0/debt/WAL/temp space and later stalls. Report sustained steady state, compaction drain, physical read/write/space amplification, p50–p999 reads/writes, stalls, recovery, ENOSPC, and fault/oracle results under representative updates/deletes/snapshots.
