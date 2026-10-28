---
module_id: DBE-028
program: Database Engineering
level: 1
module_number: 28
title: Dirty Pages and Writeback
status: complete
last_verified: 2026-08-30
---

# Dirty Pages and Writeback

## One-Page Review

### Governing question

How can a database turn modified buffer-pool pages into recoverable persistent state without losing a concurrent update, violating write-ahead logging, or forcing foreground transactions to absorb uncontrolled storage stalls?

### Essential definitions

A **dirty page** differs from the database's persisted page image. **Writeback** copies an eligible dirty page toward its data file; a completed write is not necessarily durable until the required storage flush/barrier has completed. A page's **pageLSN** identifies the latest logged update represented by its current image. The write-ahead rule requires the relevant log through that LSN to be durable before the page image may reach persistent data storage. A **flush list** orders or indexes dirty work, often by oldest recovery-relevant LSN. A **fuzzy checkpoint** advances recovery state while transactions and page updates continue rather than freezing and writing the whole buffer pool at once. **Steal** permits a page containing uncommitted changes to be written; **no-force** permits commit without writing all transaction pages. **Re-dirtying** changes a page while an older captured image is in flight.

### Central model, mechanism, or theorem

Writeback is a versioned state transition, not a dirty-bit clear. Under a content latch, capture a stable page image, identity/generation, and pageLSN. Ensure the WAL durable position is at least that captured pageLSN, issue the data write without holding broad locks, validate its completion, and clear dirty state only if the page still represents the captured version. If it was re-dirtied, the older write may still be useful, but the page remains dirty for another write. Scheduling balances three debts: shortage of clean replacement candidates, accumulated dirty bytes, and recovery/log-reuse distance.

### Critical invariants

- No persisted page image may depend on a log record that is not durable.
- A write uses one internally consistent page image and the correct physical identity.
- Completion of an older image never clears a newer dirty generation.
- Failed, short, misdirected, or uncertain writes never produce a false clean state.
- Pins, latches, I/O ownership, replacement identity, and dirty metadata follow one defined state protocol.
- A checkpoint/recovery horizon advances only from evidence that its required pages/log are safely persisted.
- Background pacing preserves enough clean capacity without monopolizing storage or starving foreground work.
- Metrics distinguish issued, completed, acknowledged, flushed, durable, retried, and recovery-safe work.

### Common failures

Common failures include clearing dirty before successful completion; writing a page before its WAL; holding a page latch across slow I/O; letting two writers own the same page image; losing a re-dirty event; assuming `write()` means power-loss durability; relying on volatile device caches; flushing only by dirty percentage while the oldest page blocks log recycling; repeatedly flushing hot pages; starving writeback behind reads; letting checkpoint bursts destroy tail latency; retrying a permanently failing device forever; treating replica or backup acknowledgement as local data-file durability; and declaring recovery safe from counters whose update ordering is unclear.

### Compact example

Pages A, B, and C have pageLSNs 10, 18, and 25. With durable WAL at 0, A cannot be written. After WAL reaches 18, A can become clean and a snapshot of B at LSN 18 can start. If B is updated to LSN 25 while that snapshot is in flight, completing the old B image advances its persisted image to 18 but must leave B dirty. C also remains blocked until WAL reaches 25. After that, fresh B and C images can be written. The safety result comes from WAL order and generation comparison, not from a single boolean dirty flag.

### Connections

This module extends [DBE-026](026-buffer-pools.md)'s frame lifecycle and [DBE-027](027-buffer-pool-page-replacement.md)'s eligibility/ranking split. It prepares DBE-029 for torn-write detection, DBE-072 for write-ahead logging, and DBE-075 for checkpoint algorithms. Operating systems provide buffered/direct I/O and barriers; concurrent programming supplies versioned state and ownership; distributed systems supplies acknowledgement and failure-domain reasoning.

## Governing Question

The governing question is not merely when to call a write API. It is how to preserve the recovery contract across logical modification, log generation, shared-memory concurrency, kernel/device queues, write completion, durability, eviction, checkpoints, backups, and failures. A production design must answer four questions separately: may this version be written, which page should be written next, when is the write complete, and what durable/recovery claim follows?

## Why This Matters

No-force buffering makes commits fast because transaction pages need not all be forced at commit. Steal makes finite memory practical because uncommitted changes can leave the buffer pool. Together they require WAL/redo and possibly undo semantics: the data files can contain a mixture of old, committed, and uncommitted page states at a crash. Writeback is the continuous mechanism that keeps that mixture recoverable and bounded.

Too little background writeback creates a dirty cliff. Replacement scans find pages but cannot reuse them without synchronous writes; log space approaches a reuse boundary; a checkpoint or shutdown must drain a large backlog; and foreground latency spikes. Too much writeback consumes bandwidth, repeatedly writes hot pages, raises device amplification, interferes with reads and WAL, and can still make little recovery progress if it chooses the wrong pages.

Correctness is subtle because three timelines overlap. The buffer page can change again; WAL durability advances independently; and an asynchronous data write completes later. The dirty bit compresses this history and is therefore insufficient alone. The system needs image/version ownership, a pageLSN, explicit I/O state, and ordering rules. The storage stack adds another boundary: copying bytes to a kernel cache, completing a device command, and surviving power loss are different claims.

Operationally, dirty debt links workload, memory, WAL capacity, checkpoint policy, and storage. A dashboard that shows only dirty-page percentage can appear healthy even when one very old dirty page holds back the recovery horizon or when all reusable candidates require foreground writes. Graduate-level engineering therefore treats writeback as a closed-loop control problem constrained by recovery invariants.

## Prerequisites and Retrieval

Retrieve the frame/tag/page-table, pin/latch, I/O ownership, dirty-state, and error-cleanup model from [DBE-026](026-buffer-pools.md). Retrieve replacement proposal versus atomic eligibility and clean-victim supply from [DBE-027](027-buffer-pool-page-replacement.md). You should already understand transactions, atomic state transitions, file/device I/O, checksums, queues, latency distributions, and crash fault models.

Before continuing, explain why unpinned does not imply writable, why completed does not necessarily imply durable, and why commit durability need not imply every modified data page is current on disk. If those distinctions are unclear, revisit the prerequisite chapters rather than memorizing flush rules.

This chapter models physiological page changes with monotonically comparable LSNs. It does not define a complete log record format, ARIES analysis/redo/undo, full-page-write or doublewrite implementation, or a complete checkpoint protocol. Those mechanisms appear later. Vendor examples illustrate real design choices; they are not portable constants or configuration recommendations.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish dirty, written, flushed, durable, checkpoint-safe, and clean states;
2. derive the WAL-before-data invariant from pageLSN and durable-log position;
3. design a versioned asynchronous write pipeline that preserves re-dirty events;
4. compare eviction, background, checkpoint, and administrative writeback triggers;
5. reason about steal/no-force, fuzzy progress, recovery debt, and log reuse;
6. schedule dirty pages by replacement need, age/LSN, locality, heat, and cost;
7. analyze concurrency, cancellation, partial/torn writes, storage caches, and retry limits;
8. build metrics and tests that support scoped recovery and latency claims; and
9. tune writeback experimentally without confusing throughput, completion, or durability.

## Core Exposition

When a transaction changes a latched buffer page, the engine records enough recovery information, assigns or observes an LSN, changes the bytes, sets pageLSN consistently, and marks the frame dirty before releasing protection. The exact order is engine-specific, but no observer may see a changed page described as safely clean. Repeated changes usually coalesce: five updates can produce one later data-page write, while their required log records remain the recovery source.

Steal/no-force separates transaction commit from page propagation. At commit, the system normally needs the commit/log durability defined by its mode, not a force of every data page. A background writer can later write pages from committed and uncommitted transactions because recovery interprets their log history. This improves throughput but means a data-file image alone is not a transactional snapshot.

The basic WAL rule for a captured page image `I` is `durable_wal_lsn >= I.pageLSN` before `I` may become persistent. The comparison is to the captured image, not necessarily the page's newer current LSN. If B at LSN 18 is captured and then becomes B at LSN 25, WAL through 18 is enough to write the old image; it is not enough to call the current B clean. Implementations may batch WAL advancement for many page writes, but batching cannot invert the dependency.

An asynchronous write pipeline has distinct stages. First, select a dirty candidate under scheduling policy. Second, stabilize identity and content, claim write ownership, capture LSN/generation, and form a coherent image, sometimes in a separate buffer. Third, arrange WAL durability. Fourth, submit data I/O without holding locks that block unrelated access. Fifth, process success or failure. Sixth, under the descriptor protocol, compare identity and dirty generation. Only an unchanged successfully persisted generation can become clean.

There are two common content strategies. A writer can hold a content latch while the storage layer copies the page bytes, then release it while I/O proceeds; this depends on the API's buffer-lifetime semantics. Or it can copy/checksum/encrypt into a dedicated I/O buffer under the latch and submit that immutable image. The second costs memory bandwidth but simplifies concurrent re-dirty reasoning. Neither strategy permits retagging or freeing source state while an API still owns its memory.

Write completion has layers. Submission means queued. A successful system call or asynchronous completion may mean bytes reached the OS or device queue. A flush/barrier/FUA protocol establishes a stronger ordering or durability claim according to the OS, filesystem, controller, device, and failure model. Databases must document which layer protects WAL, data pages, checkpoints, and commit. Hardware that falsely acknowledges persistence defeats software assumptions; testing and operational qualification remain necessary.

Dirty-page scheduling serves several objectives. Replacement cleaning targets cold frames likely to be reused soon. Checkpoint cleaning targets pages necessary to bound restart work and permit old log reuse. Age-based cleaning prevents ancient dirty pages from pinning a recovery horizon. Throughput scheduling batches/sequences writes, respects device queue depth, and may group neighbors when that matches storage. Heat-aware scheduling delays pages likely to be redirtied, but cannot let hot ancient pages block progress indefinitely.

A scheduler therefore often combines signals rather than sorting by one scalar. It may reserve bandwidth for oldest recovery-relevant pages, another budget for imminent replacement candidates, and a bounded share for opportunistic locality. Control inputs include dirty bytes/ratio, redo generation, oldest recLSN/pageLSN, clean-frame demand, eviction-write rate, log occupancy, checkpoint deadline, device latency/queue depth, tenant class, and recent redirty rate.

Fuzzy checkpointing does not require one instant when all buffer pages are clean. Instead it records enough recovery metadata and coordinates page/log progress so recovery can begin from a known point while updates continue. The exact meaning of checkpoint completion is protocol-specific. A dangerous simplification is “checkpoint means flush every dirty page”; another is “checkpoint record alone makes preceding pages safe.” The recorded horizon must be justified by actual persistence and recovery rules.

PostgreSQL documents a background writer that prepares reusable clean buffers and a separate checkpointer. Its settings deliberately trade extra background I/O against the chance that server processes perform their own writes. PostgreSQL also spreads checkpoint work across an interval to reduce I/O bursts. MySQL documents InnoDB page cleaners, dirty-page low/high-water behavior, redo-generation-aware adaptive flushing, and fuzzy checkpoints. These are evidence that production systems use multiple feedback signals, not a mandate to copy defaults across versions or hardware.

Dirty and replacement structures need not be the same. A page can be hot in the replacement policy yet old in the flush list. Ordering dirty work by recovery LSN helps advance log reuse; ordering by replacement position helps create clean victims. Maintaining both views costs metadata and synchronization but avoids conflating independent goals. Any intrusive list membership needs invariants preventing duplicate insertion, lost removal, cycles, stale identity, and lock-order deadlock.

Error handling is part of the state machine. On a definitive write failure, retain dirty state and diagnostic identity/LSN, release I/O ownership, account the failure, and apply a bounded retry/escalation policy. On uncertain completion, do not claim clean unless the storage contract and verification establish safety. Persistent ENOSPC, read-only remount, lost path, checksum/encryption failure, or device timeout may require write admission throttling, failover, shutdown, or operator action rather than infinite retry.

Torn-page defense is related but separate. WAL ordering says the log precedes the page; it does not by itself guarantee an atomic full-page sector write. Full-page images, doublewrite areas, atomic-write guarantees, checksums, and recovery rules address different pieces of that problem and are examined in DBE-029 and DBE-072 through DBE-078. A checksum can detect corruption without supplying a valid replacement image.

Backpressure should begin before a hard cliff. Admission can slow writers as dirty/log debt rises, preserving latency and ensuring cleaners catch up. The control loop needs hysteresis so it does not oscillate between idle and emergency modes. Multi-tenant systems may reserve or weight writeback budgets, but global recovery constraints still require progress. A tenant cannot be allowed to monopolize all dirty capacity or evade its cost through shared cleaners.

Observability must connect causes to outcomes. Record dirtied and cleaned bytes/pages, unique dirty pages, redirty-before-completion, WAL flushes caused by data writes, write source (eviction/background/checkpoint/admin), oldest dirty age/LSN, recovery distance, clean candidates, write latency/error/retry, queue depth, device/cache flush, checkpoint progress, foreground write stalls, and per-class/tenant attribution. Histograms and rates matter more than lifetime totals.

Validation combines deterministic transition models, concurrency stress, crash/power-cut tests on qualified storage, recovery replay, checksum/torn-write injection, I/O error injection, capacity pressure, checkpoints during updates, long transactions/readers, hot-page redirty, log saturation, filesystem full/remount, failover, and performance experiments. A successful process-level test does not establish power-loss durability; a power-cut campaign samples hardware/firmware behavior but does not prove all future failures.

The executable model isolates two invariants: WAL must cover a captured image before its write starts, and completion of an old captured generation must not clear a newer update. It deliberately omits bytes, latches, threads, storage flushes, errors, checkpoints, undo, torn pages, and vendor behavior.

<!-- bijux-verify: {"id":"dirty-writeback-generation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial_dirty=('A:10', 'B:18', 'C:25')\nwrite_A_before_wal=blocked:wal<10\nwal_durable=18\nwrite_A=clean:persisted=10\nwrite_B_after_redirty=dirty:current_lsn=25:persisted=18\nwrite_C_before_wal=blocked:wal<25\nwal_durable=25\nfinal=(('A', False, 10, 10), ('B', False, 25, 25), ('C', False, 25, 25))\ninvariants=wal_before_data=True,no_lost_redirty=True\n","stderr":""}} -->
```python
pages = {
    "A": {"lsn": 10, "generation": 1, "dirty": True, "persisted": 0,
          "inflight_lsn": 0, "inflight_generation": 0},
    "B": {"lsn": 18, "generation": 1, "dirty": True, "persisted": 0,
          "inflight_lsn": 0, "inflight_generation": 0},
    "C": {"lsn": 25, "generation": 1, "dirty": True, "persisted": 0,
          "inflight_lsn": 0, "inflight_generation": 0},
}
wal_durable = 0
write_evidence = []


def start_write(name: str) -> str:
    page = pages[name]
    if wal_durable < page["lsn"]:
        return f"blocked:wal<{page['lsn']}"
    page["inflight_lsn"] = page["lsn"]
    page["inflight_generation"] = page["generation"]
    write_evidence.append((page["inflight_lsn"], wal_durable))
    return f"started:lsn={page['inflight_lsn']}"


def complete_write(name: str) -> str:
    page = pages[name]
    page["persisted"] = page["inflight_lsn"]
    if page["generation"] == page["inflight_generation"]:
        page["dirty"] = False
    page["inflight_lsn"] = 0
    page["inflight_generation"] = 0
    state = "dirty" if page["dirty"] else "clean"
    return f"{state}:persisted={page['persisted']}"


initial_dirty = tuple(f"{name}:{pages[name]['lsn']}" for name in ("A", "B", "C"))
blocked_a = start_write("A")
wal_durable = 18
start_write("A")
written_a = complete_write("A")
start_write("B")
pages["B"]["lsn"] = 25
pages["B"]["generation"] = 2
pages["B"]["dirty"] = True
complete_write("B")
redirty_b = (
    f"dirty:current_lsn={pages['B']['lsn']}:persisted={pages['B']['persisted']}"
)
blocked_c = start_write("C")
wal_durable = 25
start_write("B")
complete_write("B")
start_write("C")
complete_write("C")
final = tuple(
    (name, pages[name]["dirty"], pages[name]["lsn"], pages[name]["persisted"])
    for name in ("A", "B", "C")
)
wal_before_data = all(page_lsn <= durable_lsn for page_lsn, durable_lsn in write_evidence)
no_lost_redirty = pages["B"]["persisted"] == 25 and not pages["B"]["dirty"]

print(f"initial_dirty={initial_dirty}")
print(f"write_A_before_wal={blocked_a}")
print("wal_durable=18")
print(f"write_A={written_a}")
print(f"write_B_after_redirty={redirty_b}")
print(f"write_C_before_wal={blocked_c}")
print("wal_durable=25")
print(f"final={final}")
print(f"invariants=wal_before_data={wal_before_data},no_lost_redirty={no_lost_redirty}")
```

The final clean B state results from a second write of generation 2 after WAL reaches 25. The first successful B write only persisted generation 1 and left generation 2 dirty. The model records WAL position at submission; a real design also needs image immutability, error results, storage ordering, and durability evidence.

## Definitions and Notation

Let page `p` have current generation `g(p)`, current `pageLSN(p)`, and persisted-image LSN `diskLSN(p)` where that metadata is available. Let `W` be the WAL durable position under the engine's log-storage contract. A captured write image is `(tag, generation, image, imageLSN)`.

The core precondition is `W >= imageLSN` before the image may be persisted. Successful completion permits `diskLSN(p)` to advance to `imageLSN`. It permits `dirty(p):=false` only if the tag and generation still match the captured identity/version and no later modification remains unrepresented. Some engines use a dirty sequence or recLSN rather than a simple integer generation; the semantic obligation is the same.

Define dirty debt in bytes/pages, replacement debt as demand for clean reusable frames, and recovery debt as log/recovery distance that cannot yet be retired. A control policy maps observed debt and storage capacity to an issue rate. These variables are measurements with lag and noise, not perfect state.

**Write**, **flush**, **sync**, **barrier**, and **durable** follow the selected platform contract. The chapter never assumes that an API name has identical semantics across filesystems, devices, cloud volumes, or failure domains. **Checkpoint-safe** means the recovery protocol can rely on the recorded persistence state; it is stronger and more specific than “a write completed.”

## Mechanisms, Invariants, or Proof Structure

A defensible page-write path follows this proof-oriented workflow:

1. Select a candidate for an explicit objective: replacement, oldest recovery debt, checkpoint target, or administration.
2. Pin/claim the descriptor and verify tag/generation, dirty state, content state, and absence of conflicting I/O.
3. Under the proper content protocol, capture a coherent image, pageLSN, dirty generation, checksum/encryption context, and physical target.
4. Ensure WAL durability through the captured pageLSN without holding broad buffer locks across storage waits.
5. Submit exactly the captured immutable image; preserve I/O ownership and buffer lifetime until completion.
6. Interpret completion according to the storage contract, detecting short/error/uncertain outcomes.
7. Reacquire descriptor protection and verify the same physical/logical identity.
8. Advance persisted evidence; clear dirty only if no newer generation exists.
9. On failure or re-dirty, retain/requeue the necessary dirty work and release ownership consistently.
10. Update recovery/checkpoint horizons only from protocol-qualified persistence evidence.

The local safety argument is by cases. If the image starts before WAL covers its LSN, WAL safety fails, so submission is forbidden. If the page does not change during I/O and persistence succeeds, generation equality permits clean. If it changes, inequality preserves dirty. If I/O fails or is uncertain, success evidence is absent and dirty remains. Identity mismatch means completion belongs to an older incarnation and cannot mutate the new descriptor state.

Progress is a separate argument. The scheduler must eventually issue eligible writes; WAL must advance; storage must accept/complete; pinned/hot pages must eventually expose a stable image; retry policy must distinguish transient from terminal failure; and admission must slow when production exceeds sustainable cleaning. Safety alone can leave every page dirty forever.

## Alternatives and Trade-Offs

Synchronous eviction writeback is simple but puts full latency on the requester. Background cleaning smooths work and creates clean candidates but may write pages that would soon change again. Checkpoint cleaning bounds recovery/log reuse but can burst. Most systems combine them with different budgets and priorities.

Oldest-LSN ordering advances recovery efficiently; replacement-order cleaning reduces immediate allocation stalls; heat-aware cleaning avoids repeated writes; locality/neighbor batching suits some devices; deadline pacing meets checkpoint targets. No single ordering dominates. SSD/NVMe, network volumes, HDDs, zoned devices, and copy-on-write filesystems have different queueing, amplification, and failure behavior.

Buffered I/O uses OS caching and can coalesce writes but adds another dirty layer and later sync stalls. Direct/unbuffered I/O offers more explicit control and avoids double buffering, but needs alignment, explicit caching/prefetch, asynchronous concurrency, and correct flush semantics. An engine must benchmark the full stack rather than infer durability or speed from one flag.

Copy-before-write simplifies immutable image ownership and re-dirty concurrency but consumes CPU/memory bandwidth and buffers. Holding content protection until the kernel copies the buffer avoids the extra copy but can lengthen latch hold and depends on exact I/O semantics. Blocking page modification until completion simplifies versions but harms hot-page concurrency.

Global cleaning maximizes sharing but creates tenant interference. Per-shard or per-tenant queues reduce contention and improve attribution but can strand capacity and complicate global oldest-LSN progress. Soft quotas with global emergency work are often more robust than absolute isolation.

## Failure Modes and Misconceptions

- “Dirty means uncommitted.” Dirty only means memory differs from the persisted page image; committed and uncommitted changes can coexist.
- “Commit must flush data pages.” No-force systems normally commit through log durability; page propagation is later.
- “A completed write makes the page clean.” Only the same successfully persisted generation can be cleared.
- “WAL can catch up after the page write.” Persistence ordering, not eventual equality, is the invariant.
- “The OS accepted it, so power-loss durability is proved.” Kernel/device acknowledgement depends on the configured stack and fault model.
- “Checkpoint equals a globally clean cache.” Fuzzy checkpoints allow continuing dirty pages under recovery metadata rules.
- “Low dirty percentage means low recovery debt.” One old page can hold back a log/recovery horizon.
- “Always clean oldest.” That may repeatedly write a hot page and starve clean-victim creation.
- “Always clean coldest.” That may leave ancient recovery debt and force a sharp checkpoint.
- “More cleaner threads always help.” Excess queue depth and contention can worsen latency and steal bandwidth from WAL/reads.
- “Retry every error.” Permanent capacity/path/media failures require bounded escalation.
- “Checksums make torn pages recoverable.” Detection does not itself provide a valid replacement image.
- “Replica acknowledgement proves local data-file durability.” Replication and local page propagation have distinct contracts.
- “A benchmark proves safe tuning.” It samples workloads/hardware and cannot prove crash correctness or future tails.

## Worked Examples

### Example 1

Page P has pageLSN 420 while durable WAL is 400. Replacement ranks P first and P is unpinned. It is still not write-eligible under WAL: the system must flush WAL through at least 420 or select a different candidate. Recency and pins do not discharge recovery ordering.

### Example 2

A cleaner captures generation 7 at LSN 500. A transaction changes the page to generation 8 at LSN 530 during I/O. Successful completion persists the generation-7 image, but completion sees generation 8 and retains dirty. Clearing the boolean unconditionally would lose the newer update after eviction.

### Example 3

A 100,000-page pool is only 5% dirty, but the oldest dirty page prevents reuse of a nearly full redo segment. Percentage-based cleaning remains idle. A recovery-debt lane selects that old page, after WAL ordering, allowing the log horizon to advance without flushing all 5,000 pages.

### Example 4

A checkpoint must write 60 GiB in 10 minutes. The naive average is about 102.4 MiB/s, but production must reserve time for fsync/barriers, retries, concurrent dirty generation, and device tails. A controller measures remaining eligible bytes, deadline, and sustainable bandwidth; it does not blindly set the average as a constant.

### Example 5

A hot catalog page changes 2,000 times per second. Cleaning it every second creates repeat writes with little horizon benefit. Deferral reduces amplification, but if its oldest required LSN blocks log reuse, an age/deadline lane eventually overrides heat avoidance. Policy combines objectives.

### Example 6

The data write returns success into a volatile controller cache, then power fails before cache contents reach media. Software that labeled the page durable from completion alone made an invalid claim. The deployment needs an honest flush/FUA and power-protection contract plus fault testing.

### Example 7

An asynchronous writer captures relation R, block 9, generation 12. While it runs, R is dropped and storage identity is reused. Completion must be tied to the old locator/generation; it cannot mark a newly mapped frame clean or direct stale bytes into the new object.

### Example 8

ENOSPC makes every write fail. Infinite retries saturate logs and I/O queues while transactions keep dirtying pages. A bounded policy retains dirty state, stops unsafe log reuse, throttles/rejects writes, surfaces exact capacity/path evidence, and enters the engine's defined fail-safe path.

### Example 9

Tenant A bulk-loads while tenant B serves latency-sensitive reads. A consumes most dirty capacity and cleaner bandwidth, causing B's read misses to wait behind data writes. Per-class accounting and weighted budgets protect B, but a global oldest-LSN lane still prevents A from blocking recovery forever.

### Example 10

Candidate tuning halves checkpoint p99 on one NVMe host but raises total bytes written 40% and performs worse on a network volume. The result supports a host/workload-specific configuration, not a universal default. Rollout uses canaries, recovery drills, latency/error thresholds, and reversible settings.

## Cross-Program Connections

- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies page cache, writeback, direct I/O, barriers, and device queues.
- [Programming Languages — Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies ownership, generation counters, atomics, latches, and asynchronous completion.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) supplies distributed acknowledgement, failure domains, replication, and backpressure reasoning.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies control loops, capacity, observability, overload, and fault injection.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies integrity, encryption context, secure erase, and adversarial storage assumptions.

## References

1. PostgreSQL Global Development Group, [Write-Ahead Logging](https://www.postgresql.org/docs/current/wal-intro.html), current WAL motivation and write-ahead rule.
2. PostgreSQL Global Development Group, [Buffer Page Layout Header](https://github.com/postgres/postgres/blob/master/src/include/storage/bufpage.h), pageLSN and WAL-before-data source invariant.
3. PostgreSQL Global Development Group, [Buffer Manager README](https://github.com/postgres/postgres/blob/master/src/backend/storage/buffer/README), dirty victim, background writer, locking, and scan/bulk-write behavior.
4. PostgreSQL Global Development Group, [Resource Consumption](https://www.postgresql.org/docs/current/runtime-config-resource.html), current background-writer pacing controls and trade-offs.
5. PostgreSQL Global Development Group, [Write Ahead Log Configuration](https://www.postgresql.org/docs/current/runtime-config-wal.html), current checkpoint pacing and recovery-time trade-offs.
6. Oracle, [Configuring InnoDB Buffer Pool Flushing](https://dev.mysql.com/doc/refman/8.4/en/innodb-buffer-pool-flushing.html), MySQL 8.4 page cleaners, dirty thresholds, adaptive flushing, and device-sensitive neighbor flushing.
7. Oracle, [InnoDB Checkpoints](https://dev.mysql.com/doc/refman/8.4/en/innodb-checkpoints.html), MySQL 8.4 fuzzy checkpoint behavior.
8. C. Mohan et al., [ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging](https://web.stanford.edu/class/cs345d-01/rl/aries.pdf), *ACM TODS* 17(1), 1992.
9. SQLite Project, [Write-Ahead Logging](https://www.sqlite.org/wal.html), official checkpoint, synchronization, concurrency, and starvation discussion for SQLite WAL mode.
10. Raghu Ramakrishnan and Johannes Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, buffer and recovery foundations.

## Exercises

### Exercise 1

Trace pages X and Y. X is generation 4/pageLSN 80; Y is generation 2/pageLSN 95; durable WAL is 70. Show blocked writes, WAL advancement to 90, X completion, Y blocking, Y capture after WAL 100, Y re-dirty to generation 3/pageLSN 110 during I/O, completion, and final cleaning after WAL 110.

### Exercise 2

Design descriptor states and transitions for dirtying, capture, asynchronous submission, re-dirty, success, short/error/uncertain completion, retag, and eviction. State safety and progress invariants plus lock/latch boundaries.

### Exercise 3

A checkpoint has 240 GiB eligible at start, a 20-minute deadline, concurrent dirty generation averaging 60 MiB/s, and sustainable data-write bandwidth of 300 MiB/s before latency degrades. Analyze feasibility, headroom, and control actions without assuming all newly dirtied bytes belong to the checkpoint target.

### Exercise 4

Compare oldest-LSN, replacement-position, heat-aware, neighbor/locality, and per-tenant writeback for OLTP plus a bulk load on HDD, local NVMe, and a network volume. Define an experiment and avoid a universal winner.

### Exercise 5

Write a production assurance plan covering WAL order, generation races, partial/torn writes, volatile caches, ENOSPC, path loss, process crash, power cut, fuzzy checkpoint, recovery, backup/replica boundaries, metrics, canary rollout, and rollback.

## Answers to the Exercises

### Answer 1

At WAL 70, both writes are blocked because 70<80 and 70<95. Advancing WAL to 90 permits capture/write of X generation 4 at imageLSN 80; success with unchanged identity/generation makes X clean at persisted LSN 80. Y remains blocked because 90<95. At WAL 100, capture Y generation 2 at 95. Re-dirtying makes current Y generation 3/pageLSN 110. The old completion may advance Y's persisted image to 95 but leaves it dirty. WAL 110 then permits a generation-3 capture; successful unchanged completion advances persisted LSN to 110 and makes Y clean. No step uses a later WAL value retroactively to justify an earlier unsafe submission.

### Answer 2

Use descriptor identity/tag generation, dirty generation or sequence, pageLSN/first-dirty recLSN, pin/content latch, one I/O-owner token, captured generation/LSN, and persisted evidence. Dirtying under content protection advances version and ensures dirty membership. Capture claims I/O, records immutable identity/version/image, then releases broad locks. WAL is forced before submission. Success clears only a matching current generation; re-dirty leaves queued; failure/short/uncertain retains dirty; stale-identity completion cannot touch a replacement. Retag requires no pins/conflicting I/O and safe dirty resolution. Progress requires bounded selection, WAL/storage advancement, retry escalation, admission backpressure, and no locks held across waits that prevent those conditions.

### Answer 3

The initial target requires 240 GiB/1,200 s≈204.8 MiB/s before barriers, retries, and variance. If all 60 MiB/s of concurrent dirties were additionally in-scope, demand would be about 264.8 MiB/s, leaving only 35.2 MiB/s below the 300 MiB/s degradation point—too little resilience for tails. A fuzzy protocol may exclude or track some post-start changes, so classify target bytes rather than add blindly. Start paced work early, reserve sync/retry headroom, monitor remaining target/deadline and sustainable latency, prioritize recovery-old pages, and throttle admission before projected demand exceeds capacity. If safe completion becomes infeasible, extend/escalate under protocol rules rather than claim success.

### Answer 4

Oldest-LSN best advances recovery/log reuse but can rewrite hot pages. Replacement-position supplies clean victims but can leave old debt. Heat-aware reduces amplification but needs an age override. Neighbor batching may reduce HDD seeks but can add needless SSD/network writes. Per-tenant budgets improve fairness but need a global recovery lane. Test equal cache/metadata/log capacity with cold/warm OLTP, bulk phases, checkpoint deadlines, pinned/hot pages, failures, and each storage class. Measure foreground p50/p99, throughput, write bytes/amplification, WAL-for-page flushes, oldest debt, clean shortages, queue latency, device utilization, redirty rate, per-tenant service, and recovery time. Select per deployment with fallback.

### Answer 5

Build deterministic state/model tests for WAL-before-data, one I/O owner, identity/generation equality, and no lost re-dirty. Add thread stress and systematic schedule exploration around capture/update/completion/retag. Inject short writes, errors, timeouts, ENOSPC, read-only remount, path loss, corruption, and process termination; verify dirty/retry/escalation state. On qualified hardware, run controlled power-cut tests across WAL/data/barrier boundaries and recover with page/log validation, while acknowledging finite sampling. Exercise fuzzy checkpoints amid writes, log pressure, backups, replicas, and failover; document which acknowledgement proves which failure domain. Monitor exact write source, debt, horizons, errors, queues, stalls, and durability settings. Canary reversible tuning with latency, recovery, error, and amplification limits; stop/rollback automatically. Require storage, recovery, SRE, security, backup, and disaster-recovery human review before production claims.
