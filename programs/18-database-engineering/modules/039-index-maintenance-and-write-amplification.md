---
module_id: DBE-039
program: Database Engineering
level: 1
module_number: 39
title: Index Maintenance and Write Amplification
status: complete
last_verified: 2026-08-30
---

# Index Maintenance and Write Amplification

## One-Page Review

### Governing question

How can engineers account for every index-related write, preserve query correctness while maintenance is deferred, and choose maintenance policies from measured read benefit, write amplification, space, recovery, and tail-latency evidence?

### Essential definitions

An **index mutation** inserts, deletes, or changes an index entry because authoritative row state changed. **Write amplification (WA)** is bytes written below a declared boundary divided by logical user bytes written above it during the same declared interval. **Maintenance debt** is valid deferred work—dead-entry removal, buffered-change merge, compaction, split consolidation, or statistics refresh—that future operations must pay. **Bloat** is retained physical space or structure that no longer provides proportional useful occupancy; it is engine- and measurement-specific, not merely “a large file.” A **page split** redistributes entries when a target B-tree page cannot accept an insertion. **Fill factor** reserves free space to trade initial density for later mutation locality. A **heap-only update (HOT)** is PostgreSQL's optimization that can avoid new index entries when indexed values are unchanged and the new row version fits appropriately on the same heap page. **Vacuum/garbage collection** makes obsolete versions reclaimable subject to visibility horizons. **Rebuild/reindex** constructs a new physical index from authoritative data and replaces the old representation through a documented availability protocol.

### Central model, mechanism, or theorem

For a measurement window, define logical payload bytes `L > 0`; database data, index, log, maintenance, and temporary bytes written as `D`, `I`, `G`, `M`, and `T`; host bytes `H=D+I+G+M+T`; and media bytes `P`. Then `WA_host=H/L`, `WA_device=P/H`, and, only when intervals and boundaries match, `WA_end=P/L=WA_host*WA_device`. This ledger prevents “one write” from hiding index fan-out, new row versions, WAL/full-page images, splits, vacuum, rebuilds, compaction, replicas, filesystems, or SSD garbage collection. Correct deferred maintenance additionally requires that queries see the authoritative logical state: new entries become visible at the right commit/snapshot, obsolete candidates cannot become returned rows, and cleanup never removes entries still needed by a permitted reader or recovery point.

### Critical invariants

- Every committed row version has all and only the logically required index representations for its index definitions, predicate membership, expressions, collation, and generation.
- Index and table visibility are reconciled: an index may produce obsolete candidates, but authoritative visibility/residual checks prevent false returned rows; it may not silently omit a required visible row.
- Cleanup respects the oldest relevant transaction, replica, backup, and recovery horizons before reclaiming versions or storage.
- Buffered changes, pending lists, and immutable runs are durable or reconstructible, query-visible as required, idempotent under replay, and eventually merged under a bounded-debt policy.
- WA claims name numerator, denominator, layer, interval, durability mode, compression, replication scope, warm-up, and included background work.
- Read benefit is evaluated beside DML latency, WAL/redo, bytes, cache displacement, vacuum/compaction debt, recovery time, and p99—not from index count or file size alone.

### Common failures

Failures include counting SQL statements instead of bytes; dividing background cleanup by zero logical bytes; excluding maintenance after a short benchmark; treating buffered writes as eliminated writes; confusing PostgreSQL HOT with in-place row mutation; assuming unchanged keys imply no index work in every engine; retaining redundant indexes “for safety”; using file size alone as bloat proof; rebuilding without concurrency/catch-up/rollback design; blocking cleanup with abandoned transactions or lagging replicas; scheduling every table at once; tuning fill factor globally; ignoring WAL full-page effects and replicas; forcing maintenance without temporary-space headroom; and celebrating average insert latency while split, merge, or checkpoint p99 stalls production.

### Compact example

During one window, applications write `140` logical bytes. The engine writes `200` data bytes, `128` index bytes, `328` log bytes, and later `160` maintenance bytes: `H=816`, so `WA_host=816/140≈5.829`. The device reports `979` media bytes, so `WA_device=979/816≈1.200` and compatible end-to-end WA is `979/140≈6.993`. The `160` maintenance bytes have zero new logical payload but remain attributable to the window that created the debt. Removing them would measure admission latency, not lifecycle write cost.

### Connections

Retrieve [B+ Tree Mutations](033-b-tree-insertion-splitting-and-deletion.md), [Composite and Covering Indexes](035-composite-and-covering-indexes.md), [Partial and Expression Indexes](036-partial-and-expression-indexes.md), and [Bitmap and BRIN-Style Indexes](037-bitmap-and-brin-style-indexes.md). Continue through the [Database Engineering roadmap](../ROADMAP.md) to DBE-040, Choosing Indexes from Workload Evidence, and DBE-041, ACID and Transaction Boundaries.

## Governing Question

How do row changes fan out into index, log, cleanup, compaction, rebuild, replica, and device writes; which work may safely be deferred; and what evidence justifies each index and maintenance policy over the full workload lifecycle?

## Why This Matters

An index is not a static acceleration file. It is a materialized access path maintained as authoritative data evolves. One insert can touch a heap/clustered record, several secondary trees, uniqueness checks, free-space metadata, a redo/WAL stream, doublewrite or filesystem layers, replicas, and eventually vacuum or compaction. Updates can be worse: old logical representations must cease qualifying while new ones become discoverable. Deletes often create tombstones or dead versions before reclaiming anything.

Indexes therefore exchange present and future work. A dense B-tree saves space and reads until random insertions split pages. A buffered secondary index turns random foreground I/O into later batch merge I/O. MVCC lets readers and writers proceed but retains old versions until horizons advance. An LSM design appends quickly and later rewrites overlapping runs. A concurrent rebuild preserves availability while paying source scan, new-index construction, catch-up, validation, and temporary double-storage costs. None makes maintenance free.

Poor accounting causes predictable incidents: benchmark windows stop before cleanup; a redundant index doubles secondary writes; a long transaction prevents reclamation; bloat consumes rebuild headroom; a vacuum, merge, checkpoint, or SSD garbage collection burst drives p99; or an “online” rebuild saturates I/O and replication. Durable engineering makes the write boundary explicit, measures debt and benefit together, and treats maintenance as correctness-sensitive background execution.

## Prerequisites and Retrieval

You should be able to trace B+ tree search/split behavior, distinguish heap/clustered and secondary storage, explain composite/covering/partial/expression index membership, reason about MVCC snapshots at a high level, and distinguish logical payload, database-page, log, filesystem, and device writes. Retrieve set predicates, page occupancy, stable row identity, WAL-before-data ordering, idempotent replay, and percentile latency. This chapter introduces operational accounting; later transaction, storage, and recovery modules formalize those mechanisms.

## Learning Objectives

After this module, you can:

1. enumerate index-entry effects for inserts, updates, deletes, predicates, expressions, uniqueness, and covering payloads;
2. define host, device, and fleet write amplification without mixing boundaries or intervals;
3. explain page splits, fill factor, locality, free-space reuse, and why fragmentation is workload-dependent;
4. distinguish obsolete logical entries, reusable page space, retained file allocation, and measured bloat;
5. explain MVCC cleanup horizons and PostgreSQL's precisely scoped HOT optimization;
6. reason about buffered changes, pending lists, immutable runs, compaction, tombstones, and maintenance debt;
7. design crash-safe, concurrency-safe vacuum, cleanup, and rebuild protocols;
8. identify WAL, checkpoint, filesystem, device, replica, backup, and temporary-space contributions;
9. construct workload experiments that include steady state and background maintenance; and
10. remove or reshape indexes only through observed usage, semantic dependency, rollback, and regression evidence.

## Core Exposition

**Begin with logical obligations.** An index definition maps qualifying row versions to keys and payload. An insert creates entries in every applicable index. A delete makes old entries logically ineligible, though physical removal may wait. An update can change indexed key columns, included columns, expression inputs, collation-derived values, or partial-index predicate membership. Moving from outside to inside a predicate inserts; inside to outside deletes; inside to inside may replace key/payload. A uniqueness constraint adds conflict detection and concurrency coordination, not just storage.

The count of physical entry operations is engine-specific. In PostgreSQL's ordinary MVCC path, an update creates a new heap tuple and normally new entries in every index even when key values are unchanged; HOT is the explicit exception under documented eligibility. A clustered engine may update a clustered record and every secondary entry containing the primary key when that identifier changes. Never infer write cost merely from the columns in the SQL `SET` list.

**Define the byte ledger.** Let `L` be committed logical user payload bytes during a stable interval. At the database-host boundary, count data-page bytes `D`, index-page bytes `I`, WAL/redo/undo bytes `G`, background maintenance bytes `M`, and temporary/rebuild bytes `T`. Then

`H = D + I + G + M + T`, and `WA_host = H/L` for `L>0`.

At the storage-media boundary, firmware may write `P` physical bytes, giving `WA_device=P/H`. If the same host byte definition and time attribution feed the device measurement, `WA_end=P/L=WA_host*WA_device`. If one counter is compressed, replicated, cached, delayed, reset, sampled from a different volume, or measured over another window, multiplication is invalid. Report the terms instead of manufacturing precision.

Bytes are not the only cost. Track logical operations, page reads/writes, WAL records/full-page images, fsyncs, CPU, locks/latches, cache evictions, queue time, storage endurance, and replica/network bytes. Fleet amplification may count `H` on the primary plus physical/logical replication and each replica's maintenance. State whether that is the question; do not quietly put replicas in a single-node ratio.

**B-tree insertion and free space.** A leaf insertion searches and modifies a page. If it fits, the dirty page is later written; WAL/redo protects recovery. If it does not, a split allocates a sibling, redistributes entries, installs separator state in the parent, and may cascade. The logical insertion is small, but page and log effects can be large. Sequential keys concentrate work at the right edge; random keys spread it. Concurrency, prefix compression, variable-sized entries, included payloads, and page size alter the result.

Fill factor deliberately leaves space when building/loading an index or table. Lower density can reduce near-term splits or enable same-page new row versions, but increases pages, tree/cache footprint, read I/O, and initial storage. Free space helps only where future mutations land. A universal “80%” rule is indefensible; test key distribution, tuple growth, update rate, cache, read scans, and maintenance cadence.

Deletion rarely shrinks a file immediately. It may mark an index entry dead, delete a leaf item, leave reusable free space, merge/consolidate pages under some implementations, or defer reclamation. Four states must not be conflated: **logically obsolete** (must not qualify), **physically removable** (no permitted reader/recovery point needs it), **internally reusable** (future entries can occupy it), and **returned to filesystem/device**. A large allocated file may contain useful reusable space; a small file may still have poor locality or excessive dead candidates.

**MVCC and horizons.** Multi-version engines retain old row versions so existing snapshots can read them. Index scans may encounter entries for versions that are dead to the current snapshot and rely on table visibility checks. Cleanup can remove an entry only when no relevant transaction can see the represented version, plus engine-specific replica, recovery, or backup constraints. Long-running/abandoned transactions, prepared transactions, logical replication slots, or lagging consumers can hold horizons back. Killing blockers is a policy decision with correctness and availability consequences, not a maintenance shortcut.

PostgreSQL HOT reduces update overhead when indexed values (including relevant expression/predicate inputs under current rules) do not require new index representation and the new tuple version can be placed suitably on the same heap page. Indexes keep pointing to the HOT chain's root and heap traversal finds the visible version. Page pruning can reclaim intermediate versions during normal access. HOT is not in-place mutation, not guaranteed for every non-indexed update, and not a license to ignore vacuum/freeze/horizon management. Lower table fill factor may increase HOT opportunity while costing density.

**Cleanup, vacuum, and rebuild.** Routine cleanup removes reclaimable dead index entries, prunes versions, updates free-space/visibility metadata, and may refresh statistics depending on engine/command. It consumes I/O/CPU/WAL and can contend with queries, yet skipping it accumulates candidates and blocks reuse. Thresholds should respond to modification volume and table/index-specific behavior, not only wall-clock schedules. Anti-wraparound or equivalent safety work has priority distinct from bloat management.

A rebuild scans authoritative data (or an old index where safe), sorts/builds a new representation, handles concurrent changes, validates uniqueness/coverage, publishes atomically, and retires the old generation after readers release it. Offline rebuilds simplify the protocol but block operations. Online/concurrent rebuilds need a change-capture or extra-pass mechanism and may briefly do double index maintenance; failure can leave invalid artifacts requiring explicit cleanup. Reserve source read bandwidth, destination and temporary space, WAL/redo, replica bandwidth, and rollback headroom. “Online” describes allowed concurrency, not zero impact.

Rebuild only with diagnosis: structural corruption, unreusable fragmentation under the target workload, definition/collation change, persistent measured bloat, or a planned physical-layout migration. Routine rebuild schedules can mask horizon or workload defects while creating more writes. Validate logical equivalence and constraints before replacement; retain a rollback path when operationally required.

**Buffered and log-structured maintenance.** Buffering an index change can avoid an immediate random page read/write. MySQL InnoDB's change buffer, for example, applies to eligible secondary-index page changes not currently in the buffer pool and merges them later; it does not cover every index type. PostgreSQL GIN can use a pending-entry list. Queries and recovery must incorporate deferred state according to the engine contract. Growth raises later merge, recovery, and query costs.

LSM-style storage writes a memory table to immutable sorted runs and compacts runs later. Leveled, tiered, hybrid, overlap, size, age, and tombstone policies trade write, read, and space amplification plus delete latency. A logical item may be rewritten across multiple compactions. Sequential I/O and batching can improve throughput while consuming total bytes and causing stalls if ingestion outruns compaction. Monitor debt: immutable-run count/bytes/age, overlap, pending compaction bytes, tombstones, flush/merge throughput, stalls, and headroom.

The maintenance invariant is not “merge immediately.” It is: admitted state is durable or reconstructible; reads consult every required component/generation; newest versions and tombstones resolve deterministically; compaction preserves the logical map; publication is atomic; obsolete inputs remain until readers release them; crash replay is idempotent; and debt stays within an explicit service envelope.

**Logging and lower layers.** A database may log logical/physical changes, write database pages later, and emit full-page protection after checkpoints or equivalent boundaries. One small entry can thus generate log bytes and a page write; a split/rebuild produces more. Filesystems add metadata, journaling, copy-on-write, or replication. SSD flash translation and garbage collection add media amplification. Compression can reduce host/device bytes but spend CPU and change rewrite granularity. These layers compose only when measurements share boundaries.

Dirty-page batching changes timing, not necessarily lifecycle bytes. Checkpoint bursts can align with vacuum, rebuild, backup, replica catch-up, or device garbage collection and create tails. Rate limiting one worker does not guarantee total system headroom if multiple tables or tenants launch maintenance. Coordinate budgets for I/O, CPU, WAL, network, temporary space, and concurrency; cancellation must leave published generations and recovery metadata coherent.

**Index portfolio engineering.** Every additional index has a read purpose and a write/space/recovery cost. Semantically redundant prefixes may still differ through uniqueness, ordering, collation, predicate, included payload, operator class, partition scope, or plan stability. Usage counters can reset, miss standby/reporting traffic, and show zero for rare critical queries. Before removal, inventory constraints and dependencies, capture a representative observation window, inspect query shapes/plans across roles/replicas, estimate write savings, test regressions, deploy reversibly, and monitor.

The executable ledger below is deliberately transparent. It accounts for three foreground events and one later maintenance event. `logical_bytes=0` for cleanup is allowed per event but the aggregate denominator remains the logical bytes whose lifecycle created the debt. Device bytes are an observed boundary, not derived from database internals.

<!-- bijux-verify: {"id":"write-amplification-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"logical_bytes=140\nhost_data_bytes=200\nhost_index_bytes=128\nhost_log_bytes=328\nhost_maintenance_bytes=160\nhost_total_bytes=816\nhost_write_amplification=5.829\ndevice_physical_bytes=979\ndevice_write_amplification=1.200\nend_to_end_write_amplification=6.993\ncomposition_consistent=True\n","stderr":""}} -->
```python
events = (
    {"name": "insert", "logical": 100, "data": 120, "index": 64, "log": 184, "maintenance": 0},
    {"name": "heap_only_update", "logical": 20, "data": 40, "index": 0, "log": 40, "maintenance": 0},
    {"name": "indexed_update", "logical": 20, "data": 40, "index": 64, "log": 104, "maintenance": 0},
    {"name": "later_cleanup", "logical": 0, "data": 0, "index": 0, "log": 0, "maintenance": 160},
)


def total(field: str) -> int:
    return sum(event[field] for event in events)


logical = total("logical")
data = total("data")
index = total("index")
log = total("log")
maintenance = total("maintenance")
host = data + index + log + maintenance
device = 979
host_wa = host / logical
device_wa = device / host
end_to_end_wa = device / logical

print(f"logical_bytes={logical}")
print(f"host_data_bytes={data}")
print(f"host_index_bytes={index}")
print(f"host_log_bytes={log}")
print(f"host_maintenance_bytes={maintenance}")
print(f"host_total_bytes={host}")
print(f"host_write_amplification={host_wa:.3f}")
print(f"device_physical_bytes={device}")
print(f"device_write_amplification={device_wa:.3f}")
print(f"end_to_end_write_amplification={end_to_end_wa:.3f}")
print(f"composition_consistent={abs(host_wa * device_wa - end_to_end_wa) < 1e-12}")
```

Do not interpret the invented byte counts as a product benchmark. The zero index bytes on the named heap-only event model the effect of an eligible optimization, not a promise that a particular engine/workload will obtain it. The model omits page granularity, cache, compression, full-page images, filesystem metadata, replicas, concurrency, crashes, and performance.

**Measure steady state.** Start with an index inventory and hypotheses: which queries/constraints need each index, which DML touches it, and which maintenance path applies. Record engine/version/configuration, schema/index definitions, dataset size/distribution/churn, key locality, row widths, read/write mix, durability, cache state, checkpointing, replication, and storage. Warm to representative state. Run long enough for splits, flushes, vacuum/compaction, checkpoints, and device steady state. Include recovery/rebuild experiments separately.

Observe logical rows/bytes; per-index scans and size; inserted/deleted/dead entries where available; page density/splits; HOT eligibility/success where relevant; table/index changes; WAL/redo/undo and full-page bytes; dirty/flush/checkpoint bytes; vacuum/merge duration and debt; temporary space; replica/network lag; device host/media writes and wear; CPU; locks; I/O queue; throughput; and p50/p95/p99/max DML/query latency. Attribute counter resets and overlapping work. A causal experiment changes one index/policy on representative replay, verifies result/plan correctness, and compares confidence intervals or repeated runs.

## Definitions and Notation

- `L`: committed logical application payload bytes in the declared interval; the exact payload encoding must be stated.
- `D`, `I`, `G`, `M`, `T`: database data, index, logging, background-maintenance, and temporary/rebuild bytes written at the host boundary.
- `H=D+I+G+M+T`: declared host writes; categories must be non-overlapping.
- `P`: physical media bytes written for the same storage scope/attribution interval.
- `WA_host=H/L`, `WA_device=P/H`, `WA_end=P/L`: layered ratios, defined only for positive denominators and compatible measurements.
- `E_i(r)`: multiset of logical entries required by index `i` for visible row version `r`; it includes predicate/expression/payload semantics.
- `S`: a permitted snapshot; `R(S)` is its visible authoritative row versions.
- `C_i(S)`: candidates produced by physical index `i`; final recheck must equal the index predicate over `R(S)` even if `C_i` contains obsolete candidates.
- `h`: oldest horizon required by transactions, replicas, backups, or recovery policy; versions not provably older/irrelevant than `h` are not reclaimable.
- `Q`: queued maintenance debt in bytes/work units; stability requires long-run service capacity to meet admitted maintenance creation, with burst headroom.
- **Internal fragmentation/free space** is allocated but currently unused/reusable space; **external/file bloat** needs an engine-specific baseline and usefulness test.
- **Write stall** is admission delay/throttling caused by dirty, flush, compaction, log, or space debt reaching a limit.

## Mechanisms, Invariants, or Proof Structure

For each committed visible row version `r∈R(S)`, each index must represent exactly `E_i(r)` logically. Physical structures may retain entries for obsolete versions, but query execution must not omit required `E_i(r)` and must filter candidates that do not correspond to visible qualifying rows. This separates logical exactness from immediate physical tidiness.

Cleanup safety is a horizon proof: remove physical evidence for version `v` only after proving no permitted snapshot, recovery point, replica/consumer, uniqueness check, or rebuild catch-up can require it. The proof's inputs—not age intuition—authorize reclamation. Conservative retention costs space/work; premature deletion risks false negatives or recovery failure.

Compaction preservation is a map-equivalence proof. Resolve all input versions/tombstones under declared ordering, emit the same latest logical key/value map into output, checksum/validate output, atomically publish a manifest/generation, and retain inputs until all readers release them. A crash before publication uses old inputs; after publication uses the new manifest; replay recognizes already-applied identities. Interrupted unpublished output is garbage, not authoritative state.

Layer composition is algebra, not an estimate: `(H/L)*(P/H)=P/L` by cancellation only when the `H` is identical and denominators are positive. If maintenance is shifted outside one interval or a compressed/network boundary changes `H`, the equality's premise fails. Report incompatible layers separately.

Maintenance stability is a queue condition, not proof of low latency. If long-run debt creation exceeds service, `Q` diverges until stalls or exhaustion. Even when average service exceeds arrival, bursts, shared resources, and large indivisible splits/merges can violate p99 objectives; explicit headroom and admission control remain necessary.

## Alternatives and Trade-Offs

- **Dense versus reserved free space:** density favors scans/cache/space; reserve favors localized inserts/updates and fewer splits. Benefit depends on where writes land.
- **Immediate versus buffered index changes:** immediate work limits debt and read/recovery merge paths; buffering batches random I/O but adds durable state, query work, and later spikes.
- **Leveled versus tiered compaction:** leveling generally bounds overlapping read components/space more tightly while rewriting more; tiering reduces some merge frequency but raises read/space/tombstone exposure. Exact results depend on implementation/workload.
- **Routine cleanup versus rebuild:** cleanup reuses/removes eligible state incrementally; rebuild can reset physical layout but needs scan, catch-up, publication, double space, and failure handling.
- **Offline versus online rebuild:** offline simplifies consistency and often finishes faster but blocks; online preserves concurrency while adding change capture, interference, and validation complexity.
- **More versus fewer indexes:** more indexes can protect critical reads/constraints; fewer reduce DML, WAL, cache, storage, cleanup, backup, and recovery work.
- **Primary-local versus fleet accounting:** local ratios diagnose engine/storage behavior; fleet totals expose replication, backups, and downstream materialization cost.

## Failure Modes and Misconceptions

- “One row update is one write.” It can create a row version, many index entries, log bytes, page writes, cleanup, replicas, and device rewrites.
- “Unchanged indexed keys mean no index maintenance.” This is engine/path dependent; PostgreSQL normally creates entries for a new tuple version unless HOT applies.
- “HOT updates in place.” HOT still creates tuple versions and depends on indexed-value eligibility and same-page space.
- “Buffering removes amplification.” It defers and batches work; measure merge, recovery, reads, and debt.
- “A big index is bloated.” Size reflects data, key/payload width, fill, reusable space, and structure; compare to a justified baseline and workload effect.
- “A rebuild is harmless because it is online.” It can double writes/space, compete for I/O/locks, lag replicas, and fail during catch-up/publication.
- “Vacuum can delete anything old.” Age is insufficient; active snapshots and recovery/replication horizons govern safety.
- “Low average write latency proves health.” Debt can accumulate until split/merge/checkpoint/stall tails appear.
- “WA is a universal scalar.” It is a ratio at a named boundary/interval; host, media, and fleet values answer different questions.
- “Zero-use counters prove an index is removable.” Counters reset and may omit rare, standby, constraint, incident, or seasonal use.
- “Maintenance scheduling solves overload.” If admitted debt exceeds sustainable service, scheduling only delays the stall.
- “SSD random I/O makes maintenance irrelevant.” Endurance, firmware GC, queueing, WAL, CPU, replicas, and tail latency remain.

## Worked Examples

### Example 1

An insert qualifies for a primary, two secondary, and one partial index, but not a second partial index. The logical fan-out is four entries, not five; uniqueness checks may add reads/locking. Conclusion: derive work from exact predicate/constraint definitions, not total index count.

### Example 2

An update changes an unindexed note. PostgreSQL can use HOT only if current eligibility rules hold and the new tuple fits appropriately on the same heap page; otherwise the new tuple receives ordinary index entries. Conclusion: “unindexed column” is necessary context, not sufficient proof of zero index writes.

### Example 3

Random insertions fill a leaf and cause an 8 KiB sibling allocation plus parent change for a 40-byte logical entry. The event has high instantaneous page/log amplification, but future insertions may use both pages; amortization requires a workload interval. Conclusion: do not divide one split's bytes and call it the index's universal WA.

### Example 4

After mass deletion, an index file remains 20 GiB while internal pages have reusable space. Scans are unchanged and inserts reuse pages. A rebuild would need 20+ GiB headroom and WAL. Conclusion: retained file allocation alone does not prove beneficial rebuild; measure density, reuse, cache/I/O, and growth.

### Example 5

A transaction left idle for hours holds an old snapshot. Cleanup correctly retains dead versions, candidates and files grow, and p99 degrades. Killing the transaction may break user work. Conclusion: expose horizon owners, timeouts, escalation, and product semantics before reclamation action.

### Example 6

An InnoDB workload buffers eligible secondary changes because pages are cold. Foreground random reads fall, but the buffer grows and later merges consume I/O; clustered/full-text/spatial cases follow different rules. Conclusion: measure eligible scope and merge debt, not just improved insert latency.

### Example 7

An LSM benchmark runs 90 seconds, ends before compaction, and reports `WA=1.2`. A steady-state run includes repeated compactions and reports host `WA=7`. Both counters may be arithmetically correct; the first answers admission-window behavior, not lifecycle cost. Conclusion: declare interval and debt at end.

### Example 8

A concurrent rebuild scans, builds, captures changes, validates, and swaps, while old readers keep the prior generation. A crash before swap leaves old authoritative state; after swap recovery selects the durable new manifest; old files wait for reader release. Conclusion: atomic publication plus generation lifetime is the correctness boundary.

### Example 9

The ledger observes host `H=816`, logical `L=140`, and media `P=979` for matched scope. `WA_host=5.82857`, `WA_device=1.19975`, and their product `6.99286=P/L`. Conclusion: composition works because the exact host boundary cancels; mismatched compressed/replicated windows would not.

### Example 10

An index has zero primary scan count for a month but backs a uniqueness constraint and a quarterly incident query on a replica. Dropping it from a counter alone breaks semantics/operations. Conclusion: combine dependencies, all execution roles, observation horizon, replay experiments, reversible rollout, and monitoring.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies B-tree occupancy, amortization, LSM components, tombstones, and compaction invariants.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies durable derived state, backfills, watermarks, reconciliation, and lag/debt control.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies page cache, writeback, scheduling, filesystems, and device queues.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies replication, generations, idempotent replay, lag, and atomic publication.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies resource budgets, observability, maintenance orchestration, and safe rollouts.

## References

1. PostgreSQL Global Development Group, [Index Access Method Interface Definition](https://www.postgresql.org/docs/current/indexam.html), current secondary-index and row-update behavior.
2. PostgreSQL Global Development Group, [Heap-Only Tuples](https://www.postgresql.org/docs/current/storage-hot.html), current HOT eligibility, page-space, pruning, and fill-factor guidance.
3. PostgreSQL Global Development Group, [Routine Vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html), current version reclamation, visibility, autovacuum, and operational guidance.
4. PostgreSQL Global Development Group, [REINDEX](https://www.postgresql.org/docs/current/sql-reindex.html), current rebuild and concurrent-reindex behavior.
5. Oracle, [MySQL 8.4 InnoDB Change Buffer](https://dev.mysql.com/doc/refman/8.4/en/innodb-change-buffer.html), eligible secondary changes, merge lifecycle, limits, and monitoring.
6. SQLite Project, [VACUUM](https://www.sqlite.org/lang_vacuum.html), official rebuild, free-space, transaction, temporary-space, and failure behavior.
7. Patrick O'Neil, Edward Cheng, Dieter Gawlick, and Elizabeth O'Neil, [“The Log-Structured Merge-Tree (LSM-Tree)”](https://doi.org/10.1007/s002360050048), *Acta Informatica* 33, 1996.
8. Subhadeep Sarkar et al., [“Constructing and Analyzing the LSM Compaction Design Space”](https://www.vldb.org/pvldb/vol14/p2216-sarkar.pdf), *PVLDB* 14(11), 2021.
9. Goetz Graefe, [“Modern B-Tree Techniques”](https://doi.org/10.1561/1900000028), *Foundations and Trends in Databases* 3(4), 2011, update, space, logging, concurrency, and maintenance techniques.
10. C. Mohan and Frank Levine, [“ARIES/IM: An Efficient and High Concurrency Index Management Method Using Write-Ahead Logging”](https://research.ibm.com/publications/ariesiim-an-efficient-and-high-concurrency-index-management-method-using-write-ahead-logging), *SIGMOD*, 1992, index structural changes, concurrency, and recovery.

## Exercises

### Exercise 1

Given five indexes (primary; secondary `email`; covering `(tenant,status) INCLUDE(updated_at)`; partial `WHERE deleted_at IS NULL`; expression `lower(name)`), trace entry effects for an insert, email change, status change, soft delete, name change, and unindexed-note change. State engine assumptions and HOT eligibility.

### Exercise 2

A matched interval reports `L=4 GiB`, `D=5`, `I=7`, `G=12`, `M=8`, `T=0 GiB`, and device `P=48 GiB`. Compute layered WA. Then explain why a device counter covering two replicas or a later compaction window cannot be multiplied into the same result.

### Exercise 3

Diagnose a 2 TiB index with falling density, rising dead candidates, low free-space reuse, a long snapshot, replica lag, insufficient temporary space, and nightly p99 spikes. Separate correctness blockers, causal evidence, mitigations, and rebuild prerequisites.

### Exercise 4

Design a crash/concurrency-safe online index rebuild protocol with scan snapshot, concurrent change capture, uniqueness, catch-up, validation, atomic publication, old readers, cancellation, replicas, disk-full, corruption, rollback, and cleanup.

### Exercise 5

Design an unfamiliar production experiment deciding whether to remove two overlapping indexes and change fill factor/maintenance policy. Include workload representativeness, semantic dependencies, steady state, WA boundaries, debt, recovery, security, rollout, and decision criteria.

## Answers to the Exercises

### Answer 1

Declare engine/MVCC/index payload semantics first. Insert creates primary, email, covering, live-partial, and lower-name entries. Email change replaces email representation and ordinarily creates the engine-required new row/index-version effects. Status change changes covering key/payload; soft delete removes logical membership from the partial index while creating the new row version; name change replaces expression output; note change changes none of the logical `E_i` values. In PostgreSQL, ordinary updates still create new entries for all indexes unless HOT applies. HOT for the note change requires no indexed value or relevant predicate/expression input to change and suitable same-page space/current eligibility; it is not guaranteed. The other changes affect indexed representation and are not HOT candidates under these assumptions. Grade exact predicate/expression/INCLUDE reasoning separately from engine physical behavior.

### Answer 2

`H=5+7+12+8=32 GiB`; `WA_host=32/4=8`. `WA_device=48/32=1.5`; matched end-to-end `WA_end=48/4=12`, also `8*1.5=12`. If `P` includes two replicas while `H` is primary-only, its boundary does not cancel. If `M` or device garbage collection is measured later, attribution windows differ; a short host interval may end with debt. Report primary host, per-device/fleet, and cohort/lifecycle values separately or align counters and scope. Units cancel only after verifying compression, network, cache, reset, and volume membership.

### Answer 3

First identify the long snapshot/replication horizons: premature cleanup is forbidden, and killing/advancing them needs owner and recovery semantics. Correlate dead/live entries, density, reusable space, split/update rates, scan/recheck I/O, cache, WAL, cleanup duration/debt, horizon age, replica lag, and p99 timing; file size alone is insufficient. Stop debt growth safely through transaction timeouts/escalation, replica/slot repair, workload/index changes, and tuned rate/concurrency, preserving anti-wraparound work. Rebuild requires diagnosed benefit, verified index definition/collation/constraints, at least new-index plus temporary/WAL/rollback headroom, I/O budgets, catch-up capacity, replica testing, atomic swap, validation, old-reader lifetime, cancellation/crash paths, and rollback. Schedule after horizons and capacity are controlled, or the new index will repeat the defect.

### Answer 4

Create a generation identity and durable build record. Establish a source snapshot/watermark, bulk scan authoritative rows into sorted/checksummed new pages, and capture committed concurrent changes by WAL/log or engine protocol with transaction/order identities. Reapply idempotently through a catch-up watermark while enforcing uniqueness with the engine's documented conflict protocol. Validate definition/version, counts, constraints, sampled/full oracle lookups, page checksums, and change-log completeness. Atomically publish a durable catalog/manifest pointer; replicas must receive state in valid order. Readers bind a generation, so old files remain until reference/snapshot/recovery horizons release them. Before publication, crash/cancel keeps old authority and discards resumable/unpublished output; after publication, recovery selects new authority and completes retirement. Disk-full preserves old state; corruption quarantines new output. Rollback republishes/rebuilds only through a supported generation protocol, never by deleting live files.

### Answer 5

Inventory each index's constraint, predicate, ordering, collation, INCLUDE/payload, query roles, replica/incident/seasonal use, and plan dependencies; “overlap” by leading columns is not proof. Capture a representative replay and production observation window with counter-reset provenance. Establish baseline correctness and p50/p95/p99/max reads/writes, throughput, host component bytes, media/fleet bytes, WAL/replication, cache/I/O, page density/splits, HOT rate, dead/reusable space, vacuum/merge debt, temporary headroom, recovery/rebuild time, and resource failures. Run long enough for steady-state checkpoints/maintenance; vary one index/policy at a time across key distributions and churn. Test failure/recovery and security/tenant queries. Remove invisibly or on a canary where supported, retain reproducible recreation/rollback, then expand with plan and SLO gates. Accept only if semantic and rare-query coverage remain, statistically credible read regressions fit budgets, write/space/debt/recovery benefits materialize, and p99/headroom improve without shifting unbounded work past the window.
