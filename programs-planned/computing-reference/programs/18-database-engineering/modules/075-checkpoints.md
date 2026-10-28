---
module_id: DBE-075
program: Database Engineering
level: 2
module_number: 75
title: Checkpoints
status: complete
last_verified: 2026-09-05
---

# Checkpoints

## One-Page Review

### Governing question

How can a database record enough durable recovery state to bound restart work without pausing all transactions, violating write-ahead logging, or pretending that a checkpoint makes every data page current?

### Essential definitions

A **checkpoint** is a durable recovery summary plus a protocol for locating and trusting that summary. A **quiescent checkpoint** stops updates while it makes the durable database consistent; a **fuzzy checkpoint** records a conservative snapshot while updates and writes continue. A **dirty-page table** (DPT) maps each possibly dirty page to a **recLSN**, the earliest log record that may need redo for that dirty interval. A **transaction table** records active transaction state and normally its latest LSN. A **redo horizon** is the earliest log position from which recovery may have to scan or apply records. A **checkpoint pointer** is durable bootstrap metadata that identifies a complete checkpoint. A **restartpoint** is a recovery-time analogue written while replaying an already generated log. A checkpoint may also drive background writeback and log recycling, but those are separate mechanisms with separate safety frontiers.

### Central model, mechanism, or theorem

Let `D` be the reconstructed set of possibly dirty pages and `recLSN(p)` the earliest update that might be absent from durable page `p`. The conservative redo horizon is

$$
R = \min_{p \in D} recLSN(p),
$$

or the current end of log when `D` is empty. A fuzzy checkpoint can safely bound recovery when its begin/end records, captured DPT and transaction state, concurrent-update merge rules, WAL ordering, checkpoint pointer publication, page identities, and record formats form one proven protocol. `R` can precede both the checkpoint begin and end. Recovery therefore starts from a justified horizon, not simply “the latest checkpoint LSN.”

### Critical invariants

- Publish a checkpoint pointer only after every required checkpoint record is complete, checksummed, and durable.
- Capture or reconstruct every transaction and dirty page that can matter across the checkpoint interval; concurrency may add conservative false positives but not unsafe omissions.
- Preserve the first-dirty `recLSN` until the page version covering that interval is durably written or superseded by a proven equivalent.
- Flush the WAL through a page's `pageLSN` before that page image can become durable.
- Do not equate checkpoint completion with transaction commit, page cleanliness, backup completeness, replica currency, or corruption repair.
- Compute log recycling from the minimum of all recovery, rollback, replication, archive, backup, and decoding obligations.
- Bind checkpoint metadata to database incarnation, log history, format version, page generation, and integrity evidence.
- Make interrupted checkpoints ignorable and checkpoint discovery restartable.

### Common failures

Failures include treating a fuzzy checkpoint as a full cache flush; starting redo at the end-checkpoint record; overwriting a page's first-dirty `recLSN` on every update; removing a DPT entry when a write starts rather than when the intended image is durable; publishing a bootstrap pointer before its checkpoint; scanning an incomplete checkpoint as complete; missing a page dirtied during capture; truncating log needed by an active loser, replica, backup, or decoder; allowing checkpoint I/O to create latency cliffs; trusting metadata from another database incarnation; and declaring recovery safe because restart is fast rather than because committed and aborted effects are correct.

### Compact example

A fuzzy checkpoint begins at LSN 300. Its snapshot contains page P with `recLSN=140`, page Q with `recLSN=220`, and active transaction T7 with `lastLSN=280`. Updates continue; page R first becomes dirty at 340. The end-checkpoint record at 420 incorporates R, and the durable checkpoint pointer is published at 450. Recovery may discover the checkpoint through 450, but its redo horizon is 140, not 300, 420, or 450. If P's page image through its relevant `pageLSN` later becomes durable, P can leave the DPT and the horizon advances to 220. The checkpoint bounds discovery and redo; it did not force every page or commit T7.

### Connections

Retrieve [Dirty Pages and Writeback](028-dirty-pages-and-writeback.md), [Write-Ahead Logging](072-write-ahead-logging.md), [Log Sequence Numbers](073-log-sequence-numbers.md), and [Undo and Redo Logging](074-undo-and-redo-logging.md). Continue through [the program roadmap](../ROADMAP.md) to ARIES analysis/redo/undo, group commit, and crash recovery.

## Governing Question

A log can contain everything necessary for recovery and still be operationally unusable if restart must scan years of history. A database therefore needs a durable statement such as: “for recovery of this incarnation, no page requires redo before R, and these transactions were active near this point.” What protocol makes that statement sound while foreground transactions, page eviction, log insertion, replication, backup, and another crash can all overlap it?

“Write all dirty pages and remember the current LSN” is one answer only for a deliberately quiescent design. It can create a long outage, does not by itself settle active transactions, and can still be wrong if WAL ordering or pointer publication is wrong. Production engines commonly use fuzzy checkpoints: they tolerate a mixed durable page image and record conservative metadata from which recovery can reconstruct the missing work.

## Why This Matters

Checkpoint policy couples correctness, restart time, steady-state latency, write amplification, log retention, and operational capacity. Checkpoint too rarely and recovery scans more log, crash-restart objectives become uncertain, dirty memory and retained WAL grow, and a sudden write storm may be required later. Checkpoint too aggressively and background writes contend with queries, flush queues saturate, full-page-image policies may increase WAL, and storage tail latency can spike.

The word *checkpoint* is overloaded. In ARIES it denotes logged transaction-table and dirty-page-table state used by analysis. PostgreSQL documentation distinguishes checkpoints during normal operation from restartpoints during archive recovery; its redo position may precede the checkpoint record, and its checkpoint process spreads writes to reduce I/O bursts. InnoDB documents fuzzy checkpointing through the oldest dirty-page modification position rather than forcing every page at one instant. SQLite WAL checkpointing copies frames back into the database file and has reader/writer interaction unlike an ARIES DPT checkpoint. A design review must name the product-specific mechanism and the guarantee being claimed.

Current documentation also makes checkpoint tuning a risk decision rather than a speed knob. More retained log can improve restart and replica/backup options but consumes capacity; more frequent checkpoint cycles can shorten a horizon while increasing foreground interference. The correct target is a measured service envelope with explicit recovery-time and durability obligations, not the smallest observed restart time.

## Prerequisites and Retrieval

Retrieve these facts before proceeding:

- a WAL record must become durable before a data-page image whose correctness depends on it;
- `pageLSN` describes the latest logged update represented by one page image, while DPT `recLSN` describes the first update that might need redo in its current dirty interval;
- force/no-force and steal/no-steal determine which committed and loser effects may be absent or present after a crash;
- commit status, page dirtiness, and checkpoint membership are different state dimensions;
- a log position is meaningful only within a database incarnation and log history;
- a write request, completed device command, durable write, and validated page image are different events;
- transaction rollback, replication, backup, archiving, and logical decoding can retain log independently of crash redo;
- recovery must tolerate a crash at every instruction boundary, including while writing or publishing a checkpoint.

DBE-074 established redo, undo, CLRs, and restartable recovery records. This module establishes checkpoint state and ordering. DBE-076 will combine them into the complete ARIES passes.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish quiescent, transaction-consistent, fuzzy, incremental, and restart checkpoints;
2. derive a conservative redo horizon from dirty-page metadata;
3. explain why a checkpoint record LSN and a redo start LSN need not match;
4. design begin/end checkpoint capture under concurrent updates and page writes;
5. prove safe checkpoint-pointer publication and interrupted-checkpoint handling;
6. separate recovery progress from writeback, log recycling, backup, replication, and commit;
7. reason about checkpoint scheduling, completion age, resource reserves, and tail latency;
8. validate checkpoint code with state-machine, crash-injection, adversarial, and recovery-oracle evidence.

## Core Exposition

**Begin with the recovery obligation.** A checkpoint does not eliminate recovery. It reduces the history that recovery must inspect while preserving enough state to interpret that suffix. The required summary follows from the recovery algorithm. An ARIES-style system needs active transaction information for analysis and a DPT for redo. A copy-on-write system may checkpoint by durably publishing a new root and generation. A WAL-indexed embedded database may transfer committed frames into a base file. These mechanisms share a bounding purpose, not an interchangeable implementation.

**Quiescent checkpoints are simple but costly.** A strict quiescent procedure can block new updates, wait for active work or choose a transaction policy, flush required log and pages, write a checkpoint record, synchronize it, and atomically publish a pointer. Its proof is approachable because no state changes during capture. Its cost grows with dirty state and slow transactions, and an all-at-once flush can exceed availability or latency budgets.

A transaction-consistent checkpoint is not automatically page-consistent. Waiting until no transaction is active can still leave committed dirty pages under a no-force policy. Conversely, flushing all pages does not decide transactions or make external effects atomic. State exactly which dimensions are frozen and which are made durable.

**Fuzzy checkpoints trade exactness for concurrency.** A fuzzy checkpoint allows foreground changes and page writes during capture. It records a conservative approximation: extra transactions or pages are acceptable if later analysis filters them, but omission of required state can start recovery too late. The capture protocol must define a linearization or merge rule. For example, hold a short latch while copying table entries, log begin and end markers, and merge first-dirty events occurring during the copy into the end-checkpoint contents or a log range that analysis will scan.

The checkpoint is a distributed snapshot inside one process: logger, transaction manager, buffer manager, checkpointer, and storage layer observe changing state. “Copy two hash tables” is not a protocol until memory ordering, latch ownership, entry lifecycle, and concurrent event coverage are specified.

**Maintain DPT `recLSN` as a first-dirty witness.** When a clean page first becomes dirty because of record L, insert `(page, recLSN=L)`. Later updates change `pageLSN` but must not advance `recLSN`; the earliest missing update may still be L. When a write of page version V completes durably, remove or advance the entry only if concurrency proves that V covers the dirty interval represented by the entry. A page dirtied again while V is in flight needs a new dirty generation or retained entry.

This is the classic lost-redirty race. Suppose P is dirty at 100, writeback copies P, then transaction T modifies P at 180 before the older copy finishes. If completion simply marks P clean, recovery can omit 180. Use a modification generation, copied `pageLSN`, or compare-and-clear protocol: completion clears only the exact dirty generation written. The new generation remains with an appropriate `recLSN`.

**Derive the redo horizon, do not guess it.** Given a correct DPT, the safe start is the minimum `recLSN`. Recovery may scan from this position and test each record against the reconstructed DPT and durable page state. A checkpoint's begin record, end record, pointer, and redo horizon have different roles:

- begin/end delimit a checkpoint protocol;
- the end record carries or completes the captured state;
- the control-file pointer accelerates discovery of a complete checkpoint;
- the redo horizon names the oldest possibly absent page effect.

Because a page may have remained dirty since before checkpoint begin, the horizon can be older than every checkpoint record. Starting at `end_checkpoint` is therefore an unsafe category error.

**Capture active transactions conservatively.** A transaction-table entry normally includes transaction identity plus incarnation, state, lastLSN, and sometimes undo-related status. Transactions can begin, commit, abort, prepare, or end while capture proceeds. The protocol must ensure analysis can reconstruct the truth by combining the checkpoint snapshot with log records before, within, and after the interval. Prepared/in-doubt transactions cannot be silently converted to losers. A transaction omitted because it ended before the relevant boundary must have a durable terminal trail sufficient for analysis.

**Make checkpoint publication a commit protocol.** A durable bootstrap location—often a control record or known page—lets recovery find the newest usable checkpoint without scanning from genesis. Safe publication follows an ordering such as:

1. write a begin-checkpoint record;
2. capture and write all required checkpoint payload records;
3. write the end-checkpoint record with integrity and completeness metadata;
4. flush the log through the complete end record;
5. atomically publish and durably synchronize the checkpoint pointer.

If a crash occurs before step 4, the candidate is incomplete and ignored. If it occurs after step 4 but before step 5, the older pointer remains safe; recovery may optionally discover the newer record by validated scanning. If pointer storage tears, redundant generations, checksums, and atomic-sector assumptions must select an intact record. Never overwrite the sole known-good pointer before its successor is durable.

**Preserve WAL-before-data during checkpoint writes.** Checkpoint-driven writeback does not relax WAL. Before a captured page with `pageLSN=P` becomes durable, the log must be durable through the endpoint required to cover P. Batch scheduling can advance the log flush frontier and then issue many eligible pages. If storage reorders data and log writes, barriers or flush semantics must establish the required persistence order. A page write completed before its log is durable can make a loser effect irrecoverable or a torn update uninterpretable.

**Separate logical completion from physical cleaning.** A fuzzy checkpoint can complete while dirty pages remain. Its metadata says recovery knows how far back it might need to go; background cleaning later moves that horizon forward. Some systems couple checkpoint completion to a target amount of writeback or a maximum retained-log budget, but the invariant is still about the oldest unprotected effect. A metric named `last_checkpoint_lsn` is ambiguous unless it says whether it is a checkpoint record, redo horizon, completed writeback frontier, or control pointer.

**Do not truncate log from the checkpoint alone.** Let `R` be crash-redo need, `U` oldest rollback/undo need, `P_i` physical replica need, `A` archive need, `B` backup need, and `D_j` decoder need. A safe recycle frontier is no later than the minimum applicable obligation, rounded to a reusable segment boundary:

$$
F_{recycle} \le \min(R,U,P_1,\ldots,A,B,D_1,\ldots).
$$

A completed checkpoint may advance R while a stalled replica or large active transaction keeps an older frontier. Deleting to relieve disk pressure is an explicit consumer invalidation or data-loss decision, not checkpoint maintenance.

**Schedule for a service envelope.** Checkpoint work consumes log bandwidth, data-write bandwidth, queue depth, CPU, cache residency, and device endurance. Smooth it across an interval instead of issuing a final burst. Observe dirty bytes and age, redo distance, write rate, completion duration, sync tail, foreground latency, WAL growth, retained bytes by owner, and estimated recovery time. Maintain reserved capacity for checkpoint metadata, WAL, rollback, and emergency operations.

Time-based and volume-based triggers complement each other. A quiet system may need periodic checkpoints to bound recovery by time; a busy system may hit WAL or dirty-byte thresholds sooner. Adaptive control must be stable: reacting to one latency spike by slowing too much can accumulate debt and cause a larger later spike.

**Account for full-page protection and torn writes.** Some recovery designs log a full-page image on the first modification after a checkpoint or another protection boundary so redo can repair a torn page. More frequent checkpoints can therefore increase full-page-image frequency and WAL volume. The exact relationship is engine-specific, but the general lesson holds: checkpoint frequency changes both recovery horizon and logging/write amplification. Tune the combined protocol, not one counter.

**Treat restartpoints separately.** During archive recovery or standby replay, a process cannot invent ordinary future WAL records in the source history merely to announce a checkpoint. A restartpoint records a safe local recovery position derived from replayed checkpoint information and locally flushed state. It can bound a later restart of the recovering node, but it must not claim replay beyond the source history or release WAL needed by recovery, restore, or promotion rules.

**Validate checkpoint recovery end to end.** Unit tests for `min(recLSN)` are necessary but weak. Generate histories with interleaved first-dirty, redirty, page-write, begin/end checkpoint, transaction outcome, and pointer-publication events. Crash after every persistent write and barrier. Recover, then compare against an authoritative committed-state oracle and structural invariants. Add torn records, stale generations, corrupt checksums, unknown formats, very large tables, log wrap/reuse, storage-full conditions, long transactions, prepared work, and repeated crashes during recovery.

The executable model below checks a small conservative DPT and shows why discovery and redo positions differ. It models finite metadata only; it does not model device persistence, concurrent memory ordering, page integrity, or a complete database recovery algorithm.

<!-- bijux-verify: {"id":"checkpoint-horizon-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"checkpoint_begin=300\ncheckpoint_end=420\npublished_pointer=420\nredo_horizon_initial=140\nredo_horizon_after_p_flush=220\nactive_transactions=T7,T9\nrecycle_frontier=120\nlatest_checkpoint_is_redo_start=false\nempty_dpt_horizon=500\nevidence=finite_checkpoint_horizon_model\n","stderr":""}} -->
```python
def redo_horizon(dirty_pages: dict[str, int], log_end: int) -> int:
    if any(lsn < 0 or lsn > log_end for lsn in dirty_pages.values()):
        raise ValueError("recLSN must be inside the known log")
    return min(dirty_pages.values(), default=log_end)

checkpoint_begin = 300
checkpoint_end = 420
log_end = 500
dirty_pages = {"P": 140, "Q": 220, "R": 340}
transactions = {"T7": 280, "T9": 360}

initial = redo_horizon(dirty_pages, log_end)
del dirty_pages["P"]  # durable write proved to cover P's dirty generation
after_p_flush = redo_horizon(dirty_pages, log_end)

other_retention = {
    "rollback": 260,
    "replica": 120,
    "archive": 500,
    "backup": 200,
}
recycle_frontier = min(after_p_flush, *other_retention.values())

print(f"checkpoint_begin={checkpoint_begin}")
print(f"checkpoint_end={checkpoint_end}")
print(f"published_pointer={checkpoint_end}")
print(f"redo_horizon_initial={initial}")
print(f"redo_horizon_after_p_flush={after_p_flush}")
print(f"active_transactions={','.join(sorted(transactions))}")
print(f"recycle_frontier={recycle_frontier}")
print(f"latest_checkpoint_is_redo_start={str(checkpoint_end == initial).lower()}")
print(f"empty_dpt_horizon={redo_horizon({}, log_end)}")
print("evidence=finite_checkpoint_horizon_model")
```

## Definitions and Notation

- `B` and `E`: begin- and end-checkpoint record LSNs.
- `C`: durable bootstrap pointer to a complete checkpoint.
- `D`: dirty-page table reconstructed from checkpoint and log evidence.
- `recLSN(p)`: earliest update that may be missing from durable page `p` in its current dirty interval.
- `pageLSN(p)`: latest logged update represented by the validated durable or buffered page image under the engine's convention.
- `R`: conservative redo horizon, `min recLSN(p)` for nonempty `D`.
- **First-dirty event:** transition of a clean page generation into a dirty interval.
- **Redirty event:** modification that overlaps or follows an in-flight write of an older page image.
- **Complete checkpoint:** candidate whose required records and integrity metadata are durable and discoverable under the publication protocol.
- **Fuzzy snapshot:** conservative state captured without globally stopping relevant mutations.
- **False positive:** page or transaction retained in checkpoint state although later evidence makes it unnecessary; safe but potentially costly.
- **False negative:** required page or transaction omitted; potentially a correctness failure.
- **Checkpoint age:** explicitly named distance—time, log bytes, dirty bytes, or another measure—since a relevant completed frontier.
- **Recovery oracle:** independent construction of the authorized post-recovery state used to test the implementation.

## Mechanisms, Invariants, or Proof Structure

**Horizon safety argument.** Assume every page that might lack a logged update appears in `D`, and its entry is no later than the earliest such update. Then no page update before `R=min recLSN(D)` needs page redo. Scanning from R cannot omit an update that may be absent. The conclusion is conservative: scanning can include irrelevant records, and page-level guards still decide application. If the DPT has a false negative or an advanced `recLSN`, the premise fails and so does the bound.

**Capture coverage invariant.** Every first-dirty and transaction-state transition concurrent with checkpoint capture must be in either the captured payload or a log interval that analysis necessarily scans. Implementations can use latches, epochs, two-copy merging, or begin/end scanning, but must prove the union. Duplicates are tolerable; gaps are not.

**Compare-and-clear invariant.** Let dirty generation `g` be the page image selected for writeback. Completion may clear the DPT entry only if the current dirty generation is still `g` and the durable page passes identity/integrity checks. If the current generation is `g+1`, the entry remains with the earliest LSN of the new uncovered interval.

**Publication invariant.** If durable pointer C names checkpoint E, then the entire required checkpoint through E is durable and validates for the same database incarnation and log history. Recovery may fall back to the previous valid pointer when C is torn, stale, or incompatible.

**Retention invariant.** No segment containing an LSN at or after an outstanding owner's required frontier is recycled. Owners and rounding rules are explicit. An absent heartbeat does not silently advance a frontier.

**Bounded-work claim.** A checkpoint bounds scan distance only under assumptions about checkpoint completion, dirty-page aging, WAL generation, and retained metadata. It does not by itself bound total recovery time: redo selectivity, random I/O, loser undo, page repair, hardware rate, and repeated failure also matter.

## Alternatives and Trade-Offs

| Design | Main advantage | Main cost or risk | Appropriate evidence |
| --- | --- | --- | --- |
| Quiescent full checkpoint | Simple recovery boundary | Foreground pause and write burst | pause distribution, crash matrix, durability trace |
| Fuzzy ARIES-style checkpoint | High concurrency; conservative restart state | Complex capture and redirty races | state-machine proof, DPT oracle, crash injection |
| Incremental writeback checkpoint | Smooths I/O and dirty debt | Longer mixed-state interval | queue/latency traces, generation tests |
| Copy-on-write root publication | Small atomic publication surface | space amplification and tree reclamation | root-generation proof, orphan/reuse tests |
| WAL frame checkpoint into base file | Simple append path and bounded WAL | reader coordination and copy cost | reader/writer schedule tests |
| Time-triggered policy | Bounds quiet-period age | ignores burst volume | recovery-time observations by age |
| Volume-triggered policy | Reacts to generated recovery work | can cluster under bursts | WAL/dirty-byte thresholds and tail latency |
| Adaptive scheduling | Can use available I/O headroom | controller instability and opaque tuning | workload transitions and control-loop analysis |

No row is universally superior. A low-latency database on provisioned storage, an embedded database on flash, and an archival warehouse have different pause, endurance, recovery, and capacity constraints. The choice must include the storage contract and failure domain.

## Failure Modes and Misconceptions

1. **“Checkpoint means every dirty page is on disk.”** A fuzzy checkpoint can complete with dirty pages represented conservatively.
2. **“Redo begins at the checkpoint record.”** It begins at the justified redo horizon, which may be older.
3. **“The newest checkpoint is always usable.”** An incomplete, torn, corrupt, or wrong-incarnation checkpoint is rejected.
4. **“A page can leave the DPT when its write is submitted.”** Only proven durable completion of the intended dirty generation justifies removal.
5. **“Updating `recLSN` on every write is fresher.”** Advancing it can omit an older absent update.
6. **“Stopping transactions makes pages consistent.”** Transaction quiescence and durable-page currency are separate.
7. **“Flushing pages makes transactions committed.”** Commit authority comes from the transaction protocol and durable log evidence.
8. **“A checkpoint permits WAL deletion.”** The oldest of all recovery and consumer obligations governs recycling.
9. **“Fast restart proves correct recovery.”** Only state and invariant oracles test atomicity, durability, and structure.
10. **“More frequent checkpoints always reduce risk.”** They can increase write amplification, full-page logging, and tail latency.
11. **“One checkpoint-age metric is enough.”** Time, log distance, dirty bytes, and estimated recovery work differ.
12. **“The DPT must be exact.”** Conservative extras cost work; missing required entries threaten correctness.
13. **“A restartpoint is an ordinary primary checkpoint.”** It is constrained by already replayed source history and recovery mode.
14. **“Storage completion implies persistence order.”** The proof needs the declared device, filesystem, barrier, and flush semantics.
15. **“Checkpoint tuning is independent of backups and replicas.”** Their retention and I/O compete with the same resources.
16. **“Old binaries can always read a new checkpoint.”** Format compatibility and downgrade rules must be explicit.

## Worked Examples

### Example 1

**Situation.** At checkpoint end, the DPT contains `P:140`, `Q:220`, and `R:340`; the end record is at 420.

**Reasoning.** `R=min(140,220,340)=140`. The end record locates the captured metadata but does not replace the oldest first-dirty witness. Recovery scans from 140 and filters records using the reconstructed DPT and page guards. Starting at 420 would skip a possibly missing update to P. Starting at 140 may scan updates already present, which is safe under correct idempotence guards.

**Conclusion.** The redo horizon is 140. Checkpoint location and redo start are distinct typed positions.

### Example 2

**Situation.** P became dirty at 100. Writeback copied it at pageLSN 160. P was updated at 180 before the write of the older image completed.

**Reasoning.** The completion proves only that the page image through 160 is durable. The buffered page now represents 180 and remains dirty. If the implementation clears P unconditionally, redo could start after 180 and lose that update. A generation comparison observes that the copied generation differs from the current dirty generation. It keeps P in the DPT with `recLSN=180` for the new uncovered interval, assuming the 160 image durably covers the old one.

**Conclusion.** Write completion clears only the version it wrote; redirty state survives with a new conservative first-dirty LSN.

### Example 3

**Situation.** The end-checkpoint record is durable, but the system crashes before updating the control-file pointer.

**Reasoning.** The previous pointer still names a complete older checkpoint. Recovery can use it safely and scan more log. If the format supports discovery scanning, it may find and validate the newer end record, but it must not infer completeness from a fragment. This ordering sacrifices freshness, not correctness. Reversing the order—publishing the pointer before flushing the candidate—could leave the only advertised checkpoint incomplete.

**Conclusion.** Payload-before-pointer publication makes a crash choose an older safe checkpoint rather than an unsafe newer one.

### Example 4

**Situation.** A checkpoint captured T as active with `lastLSN=250`; T commits at 330 while checkpoint capture continues and the end record appears at 400.

**Reasoning.** Retaining T as active in the checkpoint is a conservative false positive. During recovery, analysis scans the log suffix, sees the durable commit at 330, and classifies T as a winner. Omitting T would be safe only if the protocol guarantees that its earlier history is recoverable from another path and that the commit/terminal records are scanned. The merge rule, not wall-clock intuition, decides.

**Conclusion.** Fuzzy metadata may be stale in a conservative direction; later log evidence refines transaction outcome.

### Example 5

**Situation.** A checkpoint advances crash redo to 220, but a physical replica needs WAL from 120 and a backup needs it from 200.

**Reasoning.** The candidate recycle frontier is `min(220,120,200)=120`, then rounded according to segment rules. Recycling at 220 would preserve primary crash recovery but break the replica and backup. If capacity is exhausted, operators may explicitly invalidate a consumer or replace it from a new base backup, but that is a governed availability/data-protection decision.

**Conclusion.** Checkpoint progress is only one retention owner; the lagging replica holds the effective frontier at 120.

### Example 6

**Situation.** A database checkpoints every five minutes. At low load restart takes 20 seconds, but at peak load it takes nine minutes.

**Reasoning.** Equal wall-clock age does not imply equal recovery work. Peak WAL generation, dirty-set size, random page access, loser transactions, and device contention can all grow. Measure log bytes since redo horizon, pages eligible for redo, active rollback debt, replay throughput distributions, and storage tail latency. A volume trigger can complement the time trigger; smooth writeback can prevent the final burst.

**Conclusion.** A time interval alone does not establish an RTO. Checkpoint policy needs workload-sensitive evidence and margins.

### Example 7

**Situation.** More frequent checkpoints unexpectedly double WAL volume.

**Reasoning.** In a design that logs a full-page image on the first modification after a checkpoint-related protection boundary, shortening the interval makes hot pages cross that boundary more often. The added images can increase log bandwidth, archive traffic, replica lag, and checkpoint pressure, partially defeating the intended recovery benefit. Verify the exact engine policy and measure full-page-image contribution rather than assuming causation from frequency alone.

**Conclusion.** Checkpoint frequency can alter logging amplification; tune checkpoint and page-protection mechanisms together.

### Example 8

**Situation.** The newest control record has generation 52 and points to checkpoint 900, but its checksum fails; generation 51 points to checkpoint 700 and validates.

**Reasoning.** Numeric freshness does not override integrity. Recovery rejects generation 52, validates database incarnation and log history for generation 51, and uses checkpoint 700. It scans extra log but retains a sound bootstrap. Operators preserve the corrupt record for diagnosis and investigate whether the assumed atomic-write boundary or storage path failed.

**Conclusion.** Redundant generations turn pointer corruption into bounded extra recovery work instead of an unjustified start position.

### Example 9

**Situation.** A standby in archive recovery wants to reduce its own restart time after replaying source checkpoint record 5,000.

**Reasoning.** It may flush local pages and establish a restartpoint no later than replayed, validated source state. It cannot append an ordinary source-history checkpoint that claims events never received. Retention must still cover archive-recovery and promotion requirements. If the node crashes, it restarts from the proven local restartpoint and resumes replay from the source history.

**Conclusion.** A restartpoint bounds local repeated recovery while respecting the authority and extent of the replayed log.

### Example 10

**Situation.** A crash-injection test boots successfully after every checkpoint cut, but one recovered secondary index silently omits a committed row.

**Reasoning.** Process availability was the wrong oracle. Build the committed logical state independently from accepted transaction outcomes, scan base rows and secondary indexes, check bidirectional membership and ordering invariants, and compare allocation ownership. The missing entry could expose an omitted DPT page, an incorrect `recLSN`, a write-before-WAL violation, or an incomplete structural log record. Minimize the failing schedule and retain exact WAL, pages, checkpoint records, and persistence trace.

**Conclusion.** Successful startup is not recovery correctness; authoritative logical and structural oracles must agree.

## Cross-Program Connections

- **Operating Systems:** writeback, barriers, page cache, direct I/O, device queues, and crash consistency determine persistence claims.
- **Concurrent and Parallel Programming:** checkpoint capture is a concurrent snapshot with latches, epochs, generations, and memory-order obligations.
- **Data Structures Engineering:** DPTs, transaction tables, priority queues, and generation-tagged maps must preserve lifecycle invariants.
- **Distributed Systems:** consistent cuts, replication frontiers, and checkpoint transfer generalize the snapshot and retention problem.
- **Data Engineering:** streaming checkpoints bind source offsets, state snapshots, sinks, and replay, but their exactly-once claims have a different boundary.
- **Data Architecture Engineering:** backup lineage, retention, restore points, and recovery objectives consume checkpoint evidence.
- **Platform Engineering:** I/O budgeting, capacity reserves, telemetry, rollout compatibility, and incident controls make checkpoint policy operable.
- **Security Engineering:** privileged recovery parsers, retained historical data, metadata integrity, and denial-of-service bounds require threat analysis.

## References

1. C. Mohan, D. Haderle, B. Lindsay, H. Pirahesh, and P. Schwarz, “ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging,” *ACM Transactions on Database Systems* 17(1), 1992. Primary fuzzy-checkpoint, dirty-page-table, transaction-table, analysis, redo, and undo design; [IBM Research record](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging), reviewed 2026-09-05.
2. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1993. Durable treatment of logging, restart, checkpoints, and transaction-processing failure models.
3. PostgreSQL Global Development Group, [PostgreSQL 18: WAL Configuration](https://www.postgresql.org/docs/18/wal-configuration.html), reviewed 2026-09-05. Official checkpoint, redo-point, write spreading, restartpoint, and recovery behavior.
4. PostgreSQL Global Development Group, [PostgreSQL 18: Write Ahead Log Settings](https://www.postgresql.org/docs/18/runtime-config-wal.html), reviewed 2026-09-05. Official checkpoint triggers, completion target, full-page-write, and WAL-capacity settings.
5. PostgreSQL Global Development Group, [PostgreSQL 18: Reliability and the Write-Ahead Log](https://www.postgresql.org/docs/18/wal-reliability.html), reviewed 2026-09-05. Official storage flush, ordering, and reliability assumptions.
6. Oracle, [MySQL 8.4 Reference Manual: InnoDB Checkpoints](https://dev.mysql.com/doc/refman/8.4/en/innodb-checkpoints.html), reviewed 2026-09-05. Official InnoDB fuzzy-checkpoint and oldest-dirty-page relationship.
7. Oracle, [MySQL 8.4 Reference Manual: InnoDB Redo Log](https://dev.mysql.com/doc/refman/8.4/en/innodb-redo-log.html), reviewed 2026-09-05. Official redo capacity, checkpoint age, and operational relationships.
8. SQLite Project, [Write-Ahead Logging](https://www.sqlite.org/wal.html), reviewed 2026-09-05. Official WAL checkpoint transfer and reader/writer interaction in SQLite.
9. SQLite Project, [WAL-Mode File Format](https://www.sqlite.org/walformat.html), reviewed 2026-09-05. Official frame, checksum, salt, and checkpoint-related format details.
10. PostgreSQL Global Development Group, [`checkpointer.c`](https://github.com/postgres/postgres/blob/master/src/backend/postmaster/checkpointer.c), source reviewed 2026-09-05. Current implementation surface for checkpoint request, scheduling, and service lifecycle.

## Exercises

### Exercise 1

Define checkpoint begin, checkpoint end, checkpoint pointer, DPT `recLSN`, pageLSN, and redo horizon. Explain which pairs may legitimately differ.

### Exercise 2

A DPT at checkpoint completion is `{A:90, B:150, C:240}` and the end-checkpoint record is 300. A durable write proves A through its current dirty generation, B is redirtied at 330 while an older write is in flight, and C remains dirty. Derive the safe DPT and redo horizon after both writes finish.

### Exercise 3

Design a crash-safe two-slot checkpoint-pointer format and publication protocol. Cover torn writes, generations, checksums, database incarnation, log history, incomplete checkpoint payloads, and downgrade compatibility.

### Exercise 4

Compare quiescent and fuzzy checkpoints for a database with a 99.9th-percentile latency objective, large dirty memory, long transactions, replicas, and a ten-minute restart objective. State the evidence needed to choose.

### Exercise 5

Design a checkpoint validation campaign for an unfamiliar storage engine. Include concurrency schedules, persistence cuts, corruption, resource exhaustion, retention owners, recovery oracles, observability, rollout, and rollback.

## Answers to the Exercises

### Answer 1

Begin and end are log positions delimiting the checkpoint protocol. The pointer is durable bootstrap metadata naming a complete checkpoint, often its end record. DPT `recLSN(p)` is the earliest update that may be absent for p's current dirty interval; pageLSN is the latest logged update represented by a validated page image. The redo horizon is the minimum DPT recLSN, or a defined current position for an empty DPT. Begin can precede end; publication can follow end; a page's recLSN can precede begin; pageLSN normally equals or follows its recLSN; and the redo horizon can precede every checkpoint record. Equality is possible but not required.

### Answer 2

Initially the horizon is 90. Once A's exact dirty generation is durably written, remove A. B's older in-flight write cannot clear the redirty event at 330. If that older image durably covers all changes through the prior dirty interval, retain B with `recLSN=330`; otherwise retain the conservative older 150. C remains at 240. Under the stated successful old-generation write and sound compare-and-clear protocol, the final DPT is `{B:330, C:240}` and the horizon is 240. The end record at 300 does not force the answer to 300. Full credit requires stating the durability, generation, WAL, identity, and integrity assumptions.

### Answer 3

Use two fixed slots containing magic, format version, slot length, database incarnation, log-history identifier, checkpoint LSN, monotonically increasing generation, and checksum covering all fields. Write and durably flush the complete checkpoint payload first. Write the inactive slot with generation `g+1`, synchronize it, then treat it as current; do not destroy the old slot. Recovery validates bounds, checksum, incarnation/history, supported format, and the referenced end record's completeness, then chooses the highest valid compatible generation. A torn or unsupported newer slot falls back to the older slot. Downgrade is allowed only if the older binary understands both pointer and referenced checkpoint/log formats; otherwise fail closed. Acceptable alternatives include an atomic root pointer with equivalent redundancy and evidence.

### Answer 4

A quiescent checkpoint offers simpler state and potentially simpler recovery, but waiting for long transactions and flushing a large dirty set can violate tail-latency or availability objectives. A fuzzy checkpoint preserves concurrency and can spread writes, but requires proven DPT/transaction capture, redirty handling, and more complex recovery. Replicas add retention and I/O competition; the restart objective depends on log distance, redo selectivity, losers, and hardware rather than interval alone. Compare pause and foreground latency distributions, dirty/WAL growth, checkpoint duration and sync tails, full-page/write amplification, recovery distributions under representative crashes, long-transaction rollback, replica/backup frontiers, capacity margins, and crash-injection correctness. Choose only within the measured workload and storage envelope.

### Answer 5

Generate state-machine histories containing first-dirty, repeated update, concurrent write, redirty, transaction begin/commit/abort/prepare, checkpoint begin/capture/end, pointer publication, recycling, and recovery. Crash after every persistent write and barrier; inject torn checkpoint records, corrupt pointers/pages, stale generations, unknown versions, log gaps, full storage, slow or reordered I/O, huge DPTs, long losers, stalled replicas, and interrupted recovery. Verify committed logical state, loser absence/visibility, indexes, allocation, page identities, transaction outcomes, and retained-log sufficiency against independent oracles. Record exact binaries, formats, filesystem/device assumptions, commands, seeds, traces, outputs, and limitations. Canary the new policy with checkpoint age, redo distance, write/sync latency, retained bytes by owner, recovery drills, and rollback-compatible formats; stop or roll back on correctness, capacity, or latency thresholds.
